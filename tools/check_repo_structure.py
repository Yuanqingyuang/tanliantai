#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""链碳台（CHAINPCF）仓库结构校验脚本。

用途
    按仓库目录约定检查必需的文件与目录是否齐备，输出分类报告与缺失计数汇总。
    该脚本被本地自检与 GitHub Actions（.github/workflows/repo-checks.yml）共同复用。

约束
    * 仅使用 Python 标准库，兼容 Python 3.9 及以上版本；
    * 技术栈【待确认】，因此只做“结构与文档级”检查，不安装依赖、不编译、不执行单元测试；
    * 必需路径清单内联在本文件中，不读取任何外部清单文件。

用法
    python tools/check_repo_structure.py
    python tools/check_repo_structure.py --quiet
    python tools/check_repo_structure.py --repo-root <仓库根目录>

退出码
    0  全部必需路径存在，且没有 0 字节的必需 Markdown 文件
    1  存在缺失路径、0 字节的必需 Markdown 文件，或脚本运行失败
"""

import argparse
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 必需路径清单（与仓库目录约定一一对应，共 66 条）
# ---------------------------------------------------------------------------
REQUIRED_FILES = [
    # 仓库根
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    ".gitignore",
    ".editorconfig",
    # Agent 规则层
    ".agents/README.md",
    ".agents/context-map.md",
    ".agents/workflows/development.md",
    ".agents/workflows/bugfix.md",
    ".agents/workflows/calculation-change.md",
    ".agents/workflows/review.md",
    ".agents/workflows/release.md",
    ".agents/policies/boundaries.md",
    ".agents/policies/testing.md",
    ".agents/policies/data-security.md",
    ".agents/policies/collaboration.md",
    ".agents/templates/task.md",
    ".agents/templates/delivery-report.md",
    # 开发容器
    ".devcontainer/devcontainer.json",
    ".devcontainer/Dockerfile",
    # 环境
    "environment/README.md",
    "environment/scripts/check_environment.py",
    # 文档
    "docs/product/README.md",
    "docs/architecture/README.md",
    "docs/development/README.md",
    "docs/planning/README.md",
    "docs/decisions/README.md",
    "docs/decisions/0001-deterministic-calculation-vs-ai-copilot.md",
    # 知识库
    "knowledge/README.md",
    "knowledge/domain/README.md",
    "knowledge/domain/glossary.md",
    "knowledge/domain/pcba-smt-processes.md",
    "knowledge/domain/units-and-conversions.md",
    "knowledge/formulas/README.md",
    "knowledge/formulas/carbon-footprint.md",
    "knowledge/formulas/allocation-methods.md",
    "knowledge/formulas/formula-register.md",
    "knowledge/emission-factors/README.md",
    "knowledge/emission-factors/factor-register.md",
    "knowledge/references/README.md",
    "knowledge/references/bibliography.md",
    # 应用层
    "app/README.md",
    "app/startup/README.md",
    "app/shell/README.md",
    # 业务模块
    "modules/project/README.md",
    "modules/manufacturing/README.md",
    "modules/data_dictionary/README.md",
    "modules/activity_data/README.md",
    "modules/emission_factors/README.md",
    "modules/calculation/README.md",
    "modules/data_review/README.md",
    "modules/analysis/README.md",
    "modules/data_package/README.md",
    # 契约
    "contracts/README.md",
    # 数据
    "data/examples/README.md",
    "data/templates/README.md",
    # 测试
    "tests/unit/README.md",
    "tests/integration/README.md",
    "tests/acceptance/README.md",
    "tests/fixtures/README.md",
    # 工具与资源
    "tools/README.md",
    "tools/check_repo_structure.py",
    "resources/链碳台_logo.png",
    # CI 与协作模板
    ".github/workflows/repo-checks.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
]

# 关键路径：以上清单的子集，缺失时必须失败（此处冗余显式声明，便于人工核对）
CRITICAL_FILES = [
    ".github/workflows/repo-checks.yml",
    "docs/decisions/0001-deterministic-calculation-vs-ai-copilot.md",
]

# 疑似真实企业数据的扫描范围与规则（只提示，不失败）
SUSPICIOUS_SCAN_DIRS = ("data", "tests/fixtures")
SUSPICIOUS_SUFFIXES = (".xlsx", ".xls", ".csv", ".docx", ".doc", ".zip", ".rar", ".7z")
SUSPICIOUS_KEYWORDS = ("真实", "客户", "供应商", "报价", "bom_", "料号")
SKIP_DIR_NAMES = (".git", "__pycache__", ".venv", "venv", "node_modules", ".pytest_cache")


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


def print_line(quiet, text):
    if not quiet:
        print(text)


def check_required(root, quiet):
    """返回 (missing, empty_files, ok_count)。"""
    missing = []
    empty_files = []
    ok_count = 0
    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.exists():
            missing.append(rel)
            print_line(quiet, "[MISSING] " + rel)
            continue
        ok_count += 1
        if path.is_file() and path.suffix.lower() == ".md" and path.stat().st_size == 0:
            empty_files.append(rel)
            print_line(quiet, "[EMPTY  ] " + rel)
        else:
            print_line(quiet, "[OK     ] " + rel)
    return missing, empty_files, ok_count


def scan_suspicious(root):
    """扫描 data/ 与 tests/fixtures/ 下疑似真实企业数据的文件，仅用于提示。"""
    hits = []
    for rel_dir in SUSPICIOUS_SCAN_DIRS:
        base = root / rel_dir
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(str(base)):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
            for name in filenames:
                lower = name.lower()
                if not lower.endswith(SUSPICIOUS_SUFFIXES):
                    continue
                reason = "扩展名疑似真实数据文件"
                for keyword in SUSPICIOUS_KEYWORDS:
                    if keyword in lower:
                        reason = "文件名含敏感关键字：" + keyword
                        break
                full = Path(dirpath) / name
                try:
                    shown = full.relative_to(root).as_posix()
                except ValueError:
                    shown = full.as_posix()
                hits.append((shown, reason))
    hits.sort()
    return hits


def main(argv=None):
    force_utf8_streams()
    parser = argparse.ArgumentParser(
        description="链碳台（CHAINPCF）仓库结构校验：检查必需文件与目录是否齐备。"
    )
    parser.add_argument("--quiet", action="store_true", help="只打印汇总，不逐条列出路径")
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

    print_line(args.quiet, "[OK     ] 仓库根目录：%s" % root)
    print_line(args.quiet, "-------- 必需路径逐项检查 --------")

    missing, empty_files, ok_count = check_required(root, args.quiet)

    critical_missing = [rel for rel in CRITICAL_FILES if rel in missing]
    suspicious = scan_suspicious(root)

    print("")
    print("===== 链碳台仓库结构校验汇总 =====")
    print("仓库根目录            ：%s" % root)
    print("必需路径总数          ：%d" % len(REQUIRED_FILES))
    print("已存在                ：%d" % ok_count)
    print("缺失                  ：%d" % len(missing))
    print("空文件（0 字节 .md）  ：%d" % len(empty_files))
    print("关键路径缺失          ：%d" % len(critical_missing))
    print("数据安全提示（WARN）  ：%d" % len(suspicious))

    if missing:
        print("")
        print("-- 缺失路径清单 --")
        for rel in missing:
            print("  [MISSING] " + rel)

    if empty_files:
        print("")
        print("-- 0 字节必需 Markdown 清单 --")
        for rel in empty_files:
            print("  [EMPTY  ] " + rel)

    if suspicious:
        print("")
        print("-- 数据安全提示（仅警告，不阻塞） --")
        for rel, reason in suspicious:
            print("  [WARN   ] %s（%s）" % (rel, reason))
        print("  提示：企业真实 BOM 与工艺数据不得提交进 Git，")
        print("        请参照 .agents/policies/data-security.md 与 data/examples/README.md 处理。")

    print("")
    if missing or empty_files:
        print("[FAIL] 仓库结构校验未通过：缺失 %d 项，空文件 %d 项。"
              % (len(missing), len(empty_files)))
        print("       并行协作阶段缺失属正常现象，请补齐后重跑本脚本。")
        return 1

    print("[OK] 仓库结构校验通过：全部必需路径存在且无空 Markdown 文件。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
