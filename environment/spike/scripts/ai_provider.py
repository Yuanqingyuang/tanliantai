#!/usr/bin/env python3
"""T-0010 AIProvider 三态最小实现：mock / local / cloud。

设计约束（对应 AGENTS.md 规则 R2）：
- Provider 只返回**候选、依据与置信度**，不返回任何可进入核算的数值；
- 置信度仅用于排序，不参与核算，也不写进核算结果；
- 未配置或加载失败的 Provider 必须显式返回 `unavailable`，不得静默降级到 mock。

环境变量：
    AI_PROVIDER        mock | local | cloud（默认 mock）
    AI_LOCAL_MODEL     本地模型目录（local 模式必填）
    AI_CLOUD_BASE_URL  云端 OpenAI 兼容接口基址（cloud 模式必填）
    AI_CLOUD_API_KEY   云端密钥（cloud 模式必填，不写入仓库）
    AI_CLOUD_MODEL     云端模型名（可选）

用法：
    python environment/spike/scripts/ai_provider.py --text "回流焊后做外观检查"
    python environment/spike/scripts/ai_provider.py --compare --text "..."
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Callable, Sequence

# 合成工序表：仅用于验证候选召回与切换机制，不是正式工序字典，也不含因子数值。
PROCESS_DICTIONARY: list[dict[str, str]] = [
    {"code": "SMT-01", "label": "锡膏印刷", "keywords": "印刷 锡膏 钢网 stencil"},
    {"code": "SMT-02", "label": "贴片贴装", "keywords": "贴片 贴装 元件 电阻 电容 SMT"},
    {"code": "REFLOW-01", "label": "回流焊", "keywords": "回流焊 回流 炉温 reflow"},
    {"code": "AOI-01", "label": "自动光学检测", "keywords": "光学检测 外观 AOI 目检"},
    {"code": "THT-01", "label": "插件", "keywords": "插件 通孔 THT 插装"},
    {"code": "WAVE-01", "label": "波峰焊", "keywords": "波峰焊 波峰 wave"},
    {"code": "CLEAN-01", "label": "清洗", "keywords": "清洗 水洗 助焊剂残留"},
    {"code": "TEST-01", "label": "功能测试", "keywords": "功能测试 通电 ICT FCT"},
    {"code": "PACK-01", "label": "包装", "keywords": "包装 装箱 打包"},
]

SYNTHETIC_NOTE = "合成工序表，仅用于接口验证；不可作为正式工序字典或核算输入。"


@dataclass
class Candidate:
    code: str
    label: str
    confidence: float
    evidence: list[str] = field(default_factory=list)


@dataclass
class ProviderResponse:
    provider: str
    model: str
    status: str  # ok | unavailable | error
    candidates: list[Candidate] = field(default_factory=list)
    latency_ms: float = 0.0
    reason: str = ""
    detail: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "provider": self.provider,
            "model": self.model,
            "status": self.status,
            "latency_ms": self.latency_ms,
            "reason": self.reason,
            "candidates": [c.__dict__ for c in self.candidates],
            "detail": self.detail,
        }


class AIProvider:
    name = "base"

    def propose(self, text: str, top_k: int = 3) -> ProviderResponse:
        raise NotImplementedError

    def meta(self) -> dict:
        raise NotImplementedError


class MockProvider(AIProvider):
    """确定性关键词匹配：无模型依赖，用于跑通接口与离线演示。"""

    name = "mock"
    model_name = "keyword-rules-v1"

    def propose(self, text: str, top_k: int = 3) -> ProviderResponse:
        started = time.perf_counter()
        lowered = text.lower()
        scored: list[Candidate] = []
        for entry in PROCESS_DICTIONARY:
            hits = [word for word in entry["keywords"].split() if word.lower() in lowered]
            if not hits:
                continue
            scored.append(
                Candidate(
                    code=entry["code"],
                    label=entry["label"],
                    confidence=round(min(1.0, 0.35 + 0.15 * len(hits)), 4),
                    evidence=[f"关键词命中：{word}" for word in hits],
                )
            )
        scored.sort(key=lambda item: item.confidence, reverse=True)
        return ProviderResponse(
            provider=self.name,
            model=self.model_name,
            status="ok",
            candidates=scored[:top_k],
            latency_ms=round((time.perf_counter() - started) * 1000, 3),
            detail={"note": SYNTHETIC_NOTE, "scanned": len(PROCESS_DICTIONARY)},
        )

    def meta(self) -> dict:
        return {
            "provider": self.name,
            "model": self.model_name,
            "deterministic": True,
            "requires": "无（仅标准库）",
            "note": SYNTHETIC_NOTE,
        }


Embedder = Callable[[Sequence[str]], list[list[float]]]


class LocalProvider(AIProvider):
    """本地嵌入模型：编码查询与工序标签，按余弦相似度排序。

    embedder 由调用方注入（见 load_sentence_transformer），本类不负责下载模型；
    embedder 为 None 时返回 unavailable，不降级。
    """

    name = "local"

    def __init__(self, embedder: Embedder | None, model_name: str, load_seconds: float = 0.0):
        self._embedder = embedder
        self.model_name = model_name
        self.load_seconds = load_seconds
        self._label_vectors: list[list[float]] | None = None

    def _ensure_vectors(self) -> None:
        if self._label_vectors is None:
            texts = [f"{entry['label']} {entry['keywords']}" for entry in PROCESS_DICTIONARY]
            self._label_vectors = self._embedder(texts)

    def propose(self, text: str, top_k: int = 3) -> ProviderResponse:
        started = time.perf_counter()
        if self._embedder is None:
            return ProviderResponse(
                provider=self.name,
                model=self.model_name,
                status="unavailable",
                reason="本地模型未加载：请设置 AI_LOCAL_MODEL 指向已下载的模型目录",
                latency_ms=round((time.perf_counter() - started) * 1000, 3),
            )
        try:
            self._ensure_vectors()
            query = self._embedder([text])[0]
        except Exception as exc:  # noqa: BLE001 - 显式暴露失败原因
            return ProviderResponse(
                provider=self.name,
                model=self.model_name,
                status="error",
                reason=f"{type(exc).__name__}: {exc}",
            )
        scored = []
        for entry, vector in zip(PROCESS_DICTIONARY, self._label_vectors):
            similarity = _cosine(query, vector)
            scored.append(
                Candidate(
                    code=entry["code"],
                    label=entry["label"],
                    confidence=round(similarity, 4),
                    evidence=[f"向量相似度 {similarity:.4f}（合成工序表）"],
                )
            )
        scored.sort(key=lambda item: item.confidence, reverse=True)
        return ProviderResponse(
            provider=self.name,
            model=self.model_name,
            status="ok",
            candidates=scored[:top_k],
            latency_ms=round((time.perf_counter() - started) * 1000, 3),
            detail={"note": SYNTHETIC_NOTE, "load_seconds": self.load_seconds},
        )

    def meta(self) -> dict:
        return {
            "provider": self.name,
            "model": self.model_name,
            "loaded": self._embedder is not None,
            "load_seconds": self.load_seconds,
            "note": SYNTHETIC_NOTE,
        }


class CloudProvider(AIProvider):
    """云端 OpenAI 兼容接口：只用环境变量取密钥，不回显、不落盘。"""

    name = "cloud"

    def __init__(self, base_url: str, api_key: str, model_name: str):
        self.base_url = base_url.rstrip("/")
        self._api_key = api_key
        self.model_name = model_name

    def propose(self, text: str, top_k: int = 3) -> ProviderResponse:
        started = time.perf_counter()
        if not self.base_url or not self._api_key:
            missing = [
                name
                for name, value in (
                    ("AI_CLOUD_BASE_URL", self.base_url),
                    ("AI_CLOUD_API_KEY", self._api_key),
                )
                if not value
            ]
            return ProviderResponse(
                provider=self.name,
                model=self.model_name,
                status="unavailable",
                reason=f"缺少环境变量：{', '.join(missing)}",
                latency_ms=round((time.perf_counter() - started) * 1000, 3),
            )

        prompt = (
            "你是工序识别助手。只从下列合成工序表中挑选最多 "
            f"{top_k} 项，输出 JSON："
            '{"candidates":[{"code":"...","label":"...","confidence":0-1,"evidence":["..."]}]}。'
            "不要给出任何排放数值。工序表："
            + json.dumps(
                [{"code": e["code"], "label": e["label"]} for e in PROCESS_DICTIONARY],
                ensure_ascii=False,
            )
            + f"。待识别文本：{text}"
        )
        body = json.dumps(
            {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            content = payload["choices"][0]["message"]["content"]
            parsed = json.loads(_strip_code_fence(content))
            candidates = [
                Candidate(
                    code=str(item["code"]),
                    label=str(item["label"]),
                    confidence=float(item.get("confidence", 0.0)),
                    evidence=[str(e) for e in item.get("evidence", [])],
                )
                for item in parsed.get("candidates", [])[:top_k]
            ]
        except (urllib.error.URLError, KeyError, ValueError, json.JSONDecodeError) as exc:
            return ProviderResponse(
                provider=self.name,
                model=self.model_name,
                status="error",
                reason=f"{type(exc).__name__}: {exc}",
                latency_ms=round((time.perf_counter() - started) * 1000, 3),
            )
        return ProviderResponse(
            provider=self.name,
            model=self.model_name,
            status="ok",
            candidates=candidates,
            latency_ms=round((time.perf_counter() - started) * 1000, 3),
            detail={"note": "云端返回，需人工复核；不可直接作为核算输入"},
        )

    def meta(self) -> dict:
        return {
            "provider": self.name,
            "model": self.model_name,
            "base_url": self.base_url or "",
            "api_key_present": bool(self._api_key),
            "note": "密钥仅从环境变量读取",
        }


def _cosine(a: Sequence[float], b: Sequence[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


def _strip_code_fence(content: str) -> str:
    text = content.strip()
    if text.startswith("```"):
        lines = text.splitlines()[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return text


def load_sentence_transformer(model_dir: str) -> tuple[Embedder | None, str, float]:
    """加载本地模型，返回 (编码函数, 模型名, 加载耗时秒)。失败时返回 (None, 目录名, 0)。"""
    import time as _time

    started = _time.perf_counter()
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        print(f"[WARN] 未安装 sentence-transformers：{exc}")
        return None, os.path.basename(model_dir), 0.0
    model = SentenceTransformer(model_dir, device="cpu")
    elapsed = _time.perf_counter() - started

    def embed(texts: Sequence[str]) -> list[list[float]]:
        vectors = model.encode(list(texts), normalize_embeddings=False, convert_to_numpy=True)
        return [vector.tolist() for vector in vectors]

    return embed, os.path.basename(model_dir.rstrip("\\/")), round(elapsed, 3)


def build_provider(name: str | None = None) -> AIProvider:
    name = (name or os.environ.get("AI_PROVIDER", "mock")).strip().lower()
    if name == "mock":
        return MockProvider()
    if name == "local":
        model_dir = os.environ.get("AI_LOCAL_MODEL", "").strip()
        if not model_dir:
            return LocalProvider(None, "unset")
        embedder, model_name, load_seconds = load_sentence_transformer(model_dir)
        return LocalProvider(embedder, model_name, load_seconds)
    if name == "cloud":
        return CloudProvider(
            base_url=os.environ.get("AI_CLOUD_BASE_URL", "").strip(),
            api_key=os.environ.get("AI_CLOUD_API_KEY", "").strip(),
            model_name=os.environ.get("AI_CLOUD_MODEL", "unset"),
        )
    raise ValueError(f"未知 AI_PROVIDER：{name}（可选 mock / local / cloud）")


def main() -> int:
    parser = argparse.ArgumentParser(description="AIProvider 三态切换演示")
    parser.add_argument("--text", default="回流焊炉后做外观检查，再通电做功能测试")
    parser.add_argument("--provider", choices=["mock", "local", "cloud"], default=None)
    parser.add_argument("--compare", action="store_true", help="依次运行三种实现并对比")
    args = parser.parse_args()

    names = ["mock", "local", "cloud"] if args.compare else [args.provider or os.environ.get("AI_PROVIDER", "mock")]
    reports = []
    for name in names:
        provider = build_provider(name)
        response = provider.propose(args.text)
        reports.append({"meta": provider.meta(), "response": response.to_dict()})
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    return 0 if all(r["response"]["status"] != "error" for r in reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
