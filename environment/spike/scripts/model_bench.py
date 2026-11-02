#!/usr/bin/env python3
"""T-0010 本地嵌入模型实测：加载耗时 / 单条检索延迟 / 内存峰值 / 冷启动。

只用合成文本，不接触企业数据。结果为 JSON，供验证报告与版本锁定清单引用。

用法：
    python environment/spike/scripts/model_bench.py --model-dir D:\\models\\bge-m3 --label bge-m3
    python environment/spike/scripts/model_bench.py --model-dir ... --json-out results/model-bge-m3.json

冷启动由本脚本自己派生一个子进程测量：子进程从解释器启动到完成首次编码的墙钟时间。
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import subprocess
import sys
import threading
import time
from pathlib import Path

THRESHOLDS = {"encode_ms": 500.0, "memory_gb": 2.5, "cold_start_seconds": 10.0}

SYNTHETIC_TEMPLATES = [
    "合成工单 {i}：SMT 产线贴装 0603 电阻 {n} 颗",
    "合成样本 {i}：回流焊炉温曲线复核，批号 SYN-{i:03d}",
    "合成记录 {i}：锡膏印刷后目检，钢网编号 SYN-{n}",
    "合成工序 {i}：波峰焊后清洗助焊剂残留",
    "合成批次 {i}：插件段通孔元件 {n} 只，随后功能测试",
    "合成数据 {i}：自动光学检测复判，缺陷类型为假点",
    "合成工单 {i}：包装段装箱 {n} 箱，附合成标签",
    "合成样本 {i}：贴片机换料，料盘为合成料号 SYN-{n}",
]


def synthetic_texts(count: int) -> list[str]:
    texts = []
    for index in range(count):
        template = SYNTHETIC_TEMPLATES[index % len(SYNTHETIC_TEMPLATES)]
        texts.append(template.format(i=index + 1, n=(index % 7) + 1))
    return texts


def cpu_name() -> str:
    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
        ) as key:
            return str(winreg.QueryValueEx(key, "ProcessorNameString")[0]).strip()
    except Exception:  # noqa: BLE001 - 非 Windows 或读取失败时退回通用值
        return platform.processor() or "unknown"


def dir_size_bytes(path: str) -> int:
    return sum(file.stat().st_size for file in Path(path).rglob("*") if file.is_file())


def package_versions() -> dict:
    versions = {}
    for name in ("torch", "transformers", "sentence_transformers", "numpy"):
        try:
            module = __import__(name)
            versions[name] = getattr(module, "__version__", "unknown")
        except ImportError:
            versions[name] = "not installed"
    return versions


class RssSampler:
    """后台采样进程 RSS，用于记录加载与编码期间的内存峰值。"""

    def __init__(self, interval: float = 0.02):
        import psutil

        self._process = psutil.Process()
        self._interval = interval
        self._stop = threading.Event()
        self._peak = 0
        self._baseline = self._process.memory_info().rss
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self) -> None:
        while not self._stop.is_set():
            self._peak = max(self._peak, self._process.memory_info().rss)
            time.sleep(self._interval)

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *exc_info):
        self._stop.set()
        self._thread.join(timeout=1)
        self._peak = max(self._peak, self._process.memory_info().rss)

    def report(self) -> dict:
        return {
            "baseline_gb": round(self._baseline / 1024 ** 3, 3),
            "peak_gb": round(self._peak / 1024 ** 3, 3),
            "delta_gb": round((self._peak - self._baseline) / 1024 ** 3, 3),
        }


def cold_start(model_dir: str, timeout: float = 300.0) -> dict:
    command = [
        sys.executable,
        os.path.abspath(__file__),
        "--model-dir",
        model_dir,
        "--cold-start-child",
    ]
    started = time.perf_counter()
    completed = subprocess.run(
        command, capture_output=True, text=True, timeout=timeout, encoding="utf-8"
    )
    elapsed = time.perf_counter() - started
    return {
        "seconds": round(elapsed, 3),
        "child_returncode": completed.returncode,
        "child_stdout": completed.stdout.strip()[-200:],
        "child_stderr": completed.stderr.strip()[-400:],
    }


def cold_start_child(model_dir: str) -> int:
    from sentence_transformers import SentenceTransformer

    started = time.perf_counter()
    model = SentenceTransformer(model_dir, device="cpu")
    vector = model.encode([synthetic_texts(1)[0]], convert_to_numpy=True)
    print(
        json.dumps(
            {
                "load_seconds": round(time.perf_counter() - started, 3),
                "dim": int(vector.shape[1]),
            }
        )
    )
    return 0


def bench(model_dir: str, label: str, text_count: int) -> dict:
    import numpy as np
    import psutil
    from sentence_transformers import SentenceTransformer

    texts = synthetic_texts(text_count)
    stats = {
        "label": label,
        "model_dir": model_dir,
        "data": {"kind": "synthetic", "count": text_count},
        "machine": {
            "cpu": cpu_name(),
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(),
            "ram_gb": round(psutil.virtual_memory().total / 1024 ** 3, 2),
            "platform": platform.platform(),
            "device": "cpu",
            "quantized": False,
        },
        "packages": package_versions(),
        "model_size_mb": round(dir_size_bytes(model_dir) / 1024 ** 2, 1),
    }

    with RssSampler() as sampler:
        started = time.perf_counter()
        model = SentenceTransformer(model_dir, device="cpu")
        stats["metrics"] = {
            "model_load_seconds": round(time.perf_counter() - started, 3)
        }

        # 工序标签向量在建索引阶段一次算好，检索耗时不重复计入
        label_vectors = model.encode(LABELS, convert_to_numpy=True)
        stats["metrics"]["embedding_dim"] = int(label_vectors.shape[1])

        encode_times = []
        retrieve_times = []
        similarity_top1 = []
        for text in texts:
            tick = time.perf_counter()
            vector = model.encode([text], convert_to_numpy=True)[0]
            encode_times.append((time.perf_counter() - tick) * 1000)

            tick = time.perf_counter()
            norm = float(np.linalg.norm(vector)) or 1.0
            scores = [
                float(vector @ candidate) / (norm * float(np.linalg.norm(candidate)) or 1.0)
                for candidate in label_vectors
            ]
            retrieve_times.append((time.perf_counter() - tick) * 1000)
            similarity_top1.append(LABEL_CODES[scores.index(max(scores))])

    def summarize(values: list[float]) -> dict:
        ordered = sorted(values)
        return {
            "median_ms": round(statistics.median(values), 3),
            "p95_ms": round(ordered[max(0, int(len(ordered) * 0.95) - 1)], 3),
            "min_ms": round(ordered[0], 3),
            "max_ms": round(ordered[-1], 3),
        }

    metrics = stats["metrics"]
    metrics["encode_ms"] = summarize(encode_times)
    metrics["retrieve_ms"] = summarize(retrieve_times)
    metrics["memory"] = sampler.report()
    metrics["cold_start"] = cold_start(model_dir)
    metrics["embedding_dim"] = int(model.encode(["合成"], convert_to_numpy=True).shape[1])
    metrics["top1_distribution"] = {
        code: similarity_top1.count(code) for code in sorted(set(similarity_top1))
    }

    verdict = {
        "encode": metrics["encode_ms"]["median_ms"] <= THRESHOLDS["encode_ms"],
        "memory": metrics["memory"]["peak_gb"] <= THRESHOLDS["memory_gb"],
        "cold_start": metrics["cold_start"]["seconds"] <= THRESHOLDS["cold_start_seconds"],
    }
    stats["thresholds"] = THRESHOLDS
    stats["verdict"] = {**verdict, "all": all(verdict.values())}
    return stats


# 合成工序标签：与 ai_provider.PROCESS_DICTIONARY 同源，仅用于检索耗时测量。
LABEL_CODES = [
    "SMT-01",
    "SMT-02",
    "REFLOW-01",
    "AOI-01",
    "THT-01",
    "WAVE-01",
    "CLEAN-01",
    "TEST-01",
    "PACK-01",
]
LABELS = [
    "锡膏印刷 印刷 锡膏 钢网 stencil",
    "贴片贴装 贴片 贴装 元件 电阻 电容 SMT",
    "回流焊 回流 炉温 reflow",
    "自动光学检测 光学检测 外观 AOI 目检",
    "插件 通孔 THT 插装",
    "波峰焊 波峰 wave",
    "清洗 水洗 助焊剂残留",
    "功能测试 通电 ICT FCT",
    "包装 装箱 打包",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="本地嵌入模型四项指标实测")
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--label", default="local-model")
    parser.add_argument("--texts", type=int, default=100)
    parser.add_argument("--json-out")
    parser.add_argument("--cold-start-child", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.cold_start_child:
        return cold_start_child(args.model_dir)

    stats = bench(args.model_dir, args.label, args.texts)
    text = json.dumps(stats, ensure_ascii=False, indent=2)
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(text + "\n", encoding="utf-8")
        print(
            f"[OK] {args.label}: 编码中位 {stats['metrics']['encode_ms']['median_ms']}ms,"
            f" 内存峰值 {stats['metrics']['memory']['peak_gb']}GB,"
            f" 冷启动 {stats['metrics']['cold_start']['seconds']}s -> {args.json_out}"
        )
    else:
        print(text)
    return 0 if stats["verdict"]["all"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
