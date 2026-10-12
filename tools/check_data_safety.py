#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""链碳台（CHAINPCF）数据安全扫描脚本。

用途
    对全仓库做一次**只读**的数据安全检查，拦截"企业真实数据或凭据被提交进
    Git"这类一旦发生就很难撤回的事故。对应 AGENTS.md 规则 R4「数据不出门」
    与 .agents/policies/data-security.md 的硬性禁止清单。
    该脚本被本地自检与 GitHub Actions（.github/workflows/repo-checks.yml）共用。

判定分两级
    BLOCK（阻塞，退出码 1）
        * 凭据文件：.env（含 .env.local 等变体，.env.example 等模板除外）、
          credentials.json、secrets.json、.token、service-account*、
          *.pem、*.key、*.p12、*.pfx；
        * 文件名含强敏感关键字：真实、客户、供应商、报价、料号；
        * 数据类后缀（.xlsx/.xls/.csv/.docx/.doc/.zip/.rar/.7z）出现在
          data/examples、data/templates、tests/fixtures 之外的目录。
    WARN（仅提示，不阻塞）
        * 文件名含 bom_；
        * 数据类后缀出现在 data/examples、data/templates 或 tests/fixtures 下
          （须人工确认已脱敏）；
        * data/ 与 tests/fixtures/ 下的文本文件内容命中敏感关键字。

约束
    * 仅使用 Python 标准库，兼容 Python 3.9 及以上版本；
    * 只读检查，不修改、不移动任何文件；
    * 不联网。

用法
    python tools/check_data_safety.py
    python tools/check_data_safety.py --quiet
    python tools/check_data_safety.py --repo-root <仓库根目录>

退出码
    0  无 BLOCK 命中（可能有 WARN）
    1  存在 BLOCK 命中，或脚本运行失败
"""

import argparse
import os
import sys
from pathlib import Path

# 遍历时跳过的目录
SKIP_DIR_NAMES = (".git", "__pycache__", ".venv", "venv", "node_modules", ".pytest_cache")

# 凭据文件的精确名（小写比较）与前缀
CREDENTIAL_NAMES = {".env", "credentials.json", "secrets.json", ".token"}
CREDENTIAL_PREFIXES = ("service-account",)
# .env 变体（.env.local / .env.production 等）；以下模板后缀不视为凭据
ENV_VARIANT_PREFIX = ".env."
ENV_VARIANT_ALLOWED_SUFFIXES = (".example", ".sample", ".template")
# 凭据文件的后缀
CREDENTIAL_SUFFIXES = (".pem", ".key", ".p12", ".pfx")

# 文件名中的强敏感关键字（命中即阻塞）
STRONG_KEYWORDS = ("真实", "客户", "供应商", "报价", "料号")
# 文件名中的弱敏感关键字（命中仅提示）
WEAK_KEYWORDS = ("bom_",)

# 数据类文件后缀
DATA_SUFFIXES = (".xlsx", ".xls", ".csv", ".docx", ".doc", ".zip", ".rar", ".7z")

# 允许存放数据类文件的目录（视为脱敏示例/模板/基准，命中仅提示，由人工确认）
ALLOWED_DATA_DIRS = ("data/examples", "data/templates", "tests/fixtures")

# 做内容关键字扫描的目录与关键字
CONTENT_SCAN_DIRS = ("data", "tests/fixtures")
CONTENT_KEYWORDS = ("真实", "客户", "供应商", "报价", "料号")
# 内容扫描的文件大小上限（字节），跳过二进制大文件
CONTENT_SCAN_MAX_BYTES = 2 * 1024 * 1024


def force_utf8_streams():
    """把 stdout/stderr 切到 UTF-8，避免 Windows 控制台 GBK 编码报错。"""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def resolve_repo_root(explicit):
    if explicit:
        return Path(explicit).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


def iter_files(root):
    """产出仓库内所有文件（跳过忽略目录）。"""
    for dirpath, dirnames, filenames in os.walk(str(root)):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        for name in filenames:
            yield Path(dirpath) / name


def rel_posix(path, root):
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def is_under(rel, dirs):
    return any(rel == d or rel.startswith(d + "/") for d in dirs)


def is_credential_name(name_lower):
    """判断文件名是否为疑似凭据（含 .env 变体，排除示例/模板后缀）。"""
    if name_lower in CREDENTIAL_NAMES or name_lower.startswith(CREDENTIAL_PREFIXES):
        return True
    if name_lower.startswith(ENV_VARIANT_PREFIX) and not name_lower.endswith(
        ENV_VARIANT_ALLOWED_SUFFIXES
    ):
        return True
    return False


def filename_blocks(name_lower, rel):
    """返回文件名级的 BLOCK 原因列表。"""
    reasons = []
    if is_credential_name(name_lower):
        reasons.append("疑似凭据文件")
    if name_lower.endswith(CREDENTIAL_SUFFIXES):
        reasons.append("疑似密钥/证书文件")
    for keyword in STRONG_KEYWORDS:
        if keyword in name_lower:
            reasons.append("文件名含强敏感关键字：" + keyword)
            break
    if name_lower.endswith(DATA_SUFFIXES) and not is_under(rel, ALLOWED_DATA_DIRS):
        reasons.append("数据类文件位于非示例/模板目录")
    return reasons


def filename_warns(name_lower, rel):
    reasons = []
    for keyword in WEAK_KEYWORDS:
        if keyword in name_lower:
            reasons.append("文件名含关键字：" + keyword)
            break
    if name_lower.endswith(DATA_SUFFIXES) and is_under(rel, ALLOWED_DATA_DIRS):
        reasons.append("示例/模板目录下的数据文件，请确认已脱敏")
    return reasons


def content_warns(path, rel):
    """对指定目录下的文本文件做敏感关键字扫描。"""
    if not is_under(rel, CONTENT_SCAN_DIRS):
        return []
    try:
        if path.stat().st_size > CONTENT_SCAN_MAX_BYTES:
            return []
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    hits = [kw for kw in CONTENT_KEYWORDS if kw in text]
    if hits:
        return ["内容命中敏感关键字：" + "、".join(hits)]
    return []


def main(argv=None):
    force_utf8_streams()
    parser = argparse.ArgumentParser(
        description="链碳台（CHAINPCF）数据安全扫描：拦截真实企业数据与凭据入库。"
    )
    parser.add_argument("--quiet", action="store_true", help="只打印汇总，不逐条列出")
    parser.add_argument("--repo-root", default=None, help="仓库根目录，默认取本脚本所在仓库")
    args = parser.parse_args(argv)

    try:
        root = resolve_repo_root(args.repo_root)
    except Exception as exc:  # pragma: no cover - 兜底
        print("[FAIL] 无法确定仓库根目录：%s" % exc)
        return 1

    if not root.is_dir():
        print("[FAIL] 仓库根目录不存在或不是目录：%s" % root)
        return 1

    blocks = []
    warns = []
    scanned = 0
    for path in iter_files(root):
        rel = rel_posix(path, root)
        name_lower = path.name.lower()
        scanned += 1
        for reason in filename_blocks(name_lower, rel):
            blocks.append((rel, reason))
        for reason in filename_warns(name_lower, rel):
            warns.append((rel, reason))
        for reason in content_warns(path, rel):
            warns.append((rel, reason))

    blocks.sort()
    warns.sort()

    print("")
    print("===== 数据安全扫描汇总 =====")
    print("仓库根目录        ：%s" % root)
    print("扫描文件数        ：%d" % scanned)
    print("阻塞项（BLOCK）   ：%d" % len(blocks))
    print("警告项（WARN）    ：%d" % len(warns))

    if blocks:
        print("")
        print("-- 阻塞项清单（必须处理）--")
        for rel, reason in blocks:
            print("  [BLOCK ] %s（%s）" % (rel, reason))

    if warns:
        print("")
        print("-- 警告项清单（请在 PR 中说明处理结论）--")
        for rel, reason in warns:
            print("  [WARN  ] %s（%s）" % (rel, reason))

    if blocks:
        print("")
        print("[FAIL] 数据安全检查未通过：存在 %d 项阻塞问题。" % len(blocks))
        print("       企业真实 BOM、工艺、价格、客户信息与任何凭据均不得提交进 Git，")
        print("       处理依据见 .agents/policies/data-security.md。")
        return 1

    print("")
    print("[OK] 数据安全检查通过：未发现凭据或疑似真实企业数据入库。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
