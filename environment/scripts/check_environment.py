#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""链碳台（CHAINPCF）开发环境自检脚本。

用途
    在开发容器或本地机器上确认“能正常开工”的最小条件：Python 版本、编码、工作目录、
    仓库关键路径、Git 可用性、以及 data/ 下是否存在疑似真实企业数据。
    被 .devcontainer/devcontainer.json 的 postCreateCommand 与
    .github/workflows/repo-checks.yml 复用。

约束
    * 仅使用 Python 标准库，兼容 Python 3.9 及以上版本；
    * 技术栈【待确认】，因此不检查语言/框架/数据库，也不安装任何依赖；
    * 只读检查，不修改仓库文件。

用法
    python3 environment/scripts/check_environment.py
    python3 environment/scripts/check_environment.py --quiet

退出码
    0  无 FAIL 项（WARN 不影响退出码）
    1  存在 FAIL 项
"""

import argparse
import locale
import os
import platform
import shutil
import sys
from pathlib import Path

MIN_PYTHON = (3, 9)

# 必需目录（顶层约定）
REQUIRED_DIRS = [
    ".agents",
    ".devcontainer",
    ".github",
    "app",
    "contracts",
    "data",
    "docs",
    "environment",
    "environment/scripts",
    "knowledge",
    "modules",
    "resources",
    "tests",
    "tests/acceptance",
    "tests/fixtures",
    "tests/integration",
    "tests/unit",
    "tools",
]

# 关键文件（仓库能否自我校验的最小集合）
KEY_FILES = [
    "README.md",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    ".gitignore",
    ".editorconfig",
    ".agents/context-map.md",
    ".devcontainer/devcontainer.json",
    ".devcontainer/Dockerfile",
    "environment/scripts/check_environment.py",
    "tools/check_repo_structure.py",
    "tools/README.md",
    ".github/workflows/repo-checks.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
]

# 只警告、不失败的文件（.editorconfig 已在 KEY_FILES 中作为必需文件）
ADVISORY_FILES = [".gitattributes"]

SUSPICIOUS_SUFFIXES = (".xlsx", ".xls", ".csv", ".docx", ".doc", ".zip", ".rar", ".7z")
SUSPICIOUS_KEYWORDS = ("真实", "客户", "供应商", "报价", "bom_", "料号")
SKIP_DIR_NAMES = (".git", "__pycache__", ".venv", "venv", "node_modules")

RESULTS = []


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


def record(level, title, detail=""):
    RESULTS.append((level, title, detail))
    return level


def emit(level, title, detail):
    line = "[%s] %s" % (level, title)
    if detail:
        line += " —— " + detail
    print(line)


def check_python_version():
    version = sys.version_info
    shown = "%d.%d.%d" % (version.major, version.minor, version.micro)
    if (version.major, version.minor) >= MIN_PYTHON:
        record("OK", "Python 版本满足要求：%s" % shown,
               "最低要求 %d.%d；技术栈未定，最终版本【待确认】" % MIN_PYTHON)
    else:
        record("FAIL", "Python 版本过低：%s" % shown,
               "需要 >= %d.%d" % MIN_PYTHON)


def check_platform_and_encoding():
    record("OK", "操作系统平台：%s %s" % (platform.system(), platform.release()),
           "Python 实现 %s" % platform.python_implementation())

    preferred = locale.getpreferredencoding(False)
    fs_encoding = sys.getfilesystemencoding()
    record("OK", "首选文本编码：%s" % preferred, "locale.getpreferredencoding(False)")
    record("OK", "文件系统编码：%s" % fs_encoding, "sys.getfilesystemencoding()")

    if preferred.lower().replace("-", "") not in ("utf8", "utf8mb4", "cp65001"):
        record("WARN", "首选文本编码不是 UTF-8：%s" % preferred,
               "在 Windows 上请执行 chcp 65001，或设置 PYTHONUTF8=1 / PYTHONIOENCODING=utf-8")
    if fs_encoding.lower().replace("-", "") not in ("utf8", "utf8mb4", "cp65001"):
        record("WARN", "文件系统编码不是 UTF-8：%s" % fs_encoding,
               "中文路径可能出错，建议改用 UTF-8 环境")

    stdout_encoding = getattr(sys.stdout, "encoding", None)
    record("OK", "标准输出编码：%s" % stdout_encoding, "已尝试切换为 UTF-8")


def check_working_directory():
    cwd = Path.cwd()
    has_readme = (cwd / "README.md").is_file()
    has_agents = (cwd / ".agents").is_dir()

    if has_readme and has_agents:
        record("OK", "当前工作目录是仓库根目录：%s" % cwd, "已找到 README.md 与 .agents/")
    else:
        missing_bits = []
        if not has_readme:
            missing_bits.append("README.md")
        if not has_agents:
            missing_bits.append(".agents/")
        record("FAIL", "当前工作目录不是仓库根目录：%s" % cwd,
               "缺少 " + "、".join(missing_bits) + "；请切换到仓库根目录后重跑")
    return cwd


def check_paths(root, quiet):
    missing_dirs = [rel for rel in REQUIRED_DIRS if not (root / rel).is_dir()]
    missing_files = [rel for rel in KEY_FILES if not (root / rel).is_file()]

    if missing_dirs:
        record("FAIL", "必需目录缺失 %d 个" % len(missing_dirs), "、".join(missing_dirs))
    else:
        record("OK", "必需目录齐备：%d 个" % len(REQUIRED_DIRS), "见仓库目录约定")

    if missing_files:
        record("FAIL", "关键文件缺失 %d 个" % len(missing_files), "、".join(missing_files))
    else:
        record("OK", "关键文件齐备：%d 个" % len(KEY_FILES), "可支撑结构与环境自检")

    for rel in ADVISORY_FILES:
        path = root / rel
        if path.is_file():
            record("OK", "存在 %s" % rel, "换行符与编码约定生效")
        else:
            record("WARN", "缺少 %s" % rel,
                   "不阻塞开工；建议补充以统一 LF 换行与文件编码")
    return missing_dirs, missing_files


def check_git():
    git_path = shutil.which("git")
    if git_path:
        record("OK", "Git 可用：%s" % git_path, "请在本地配置 user.name / user.email 与凭据")
    else:
        record("FAIL", "未找到 Git 可执行文件",
               "开发容器内应由 .devcontainer/ 安装；本地请安装 Git 后重试")


def scan_suspicious_data(root):
    hits = []
    base = root / "data"
    if not base.is_dir():
        record("WARN", "未找到 data/ 目录，跳过疑似真实数据扫描", "【待确认】目录约定是否变化")
        return hits
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
    if hits:
        record("WARN", "data/ 下发现 %d 个疑似真实企业数据文件" % len(hits),
               "；".join("%s（%s）" % (a, b) for a, b in hits[:5]))
    else:
        record("OK", "data/ 未发现疑似真实企业数据文件", "请继续保持：真实数据不得提交进 Git")
    return hits


def main(argv=None):
    force_utf8_streams()
    parser = argparse.ArgumentParser(
        description="链碳台（CHAINPCF）开发环境自检：Python、编码、目录、Git 与数据安全。"
    )
    parser.add_argument("--quiet", action="store_true", help="只打印汇总")
    args = parser.parse_args(argv)

    print("===== 链碳台（CHAINPCF）开发环境自检 =====")
    print("技术栈【待确认】，本脚本只检查通用环境条件，不检查语言 / 框架 / 数据库。")
    print("")

    check_python_version()
    check_platform_and_encoding()
    root = check_working_directory()
    check_paths(root, args.quiet)
    check_git()
    scan_suspicious_data(root)

    print("")
    print("----- 检查明细 -----")
    counts = {"OK": 0, "WARN": 0, "FAIL": 0}
    for level, title, detail in RESULTS:
        counts[level] = counts.get(level, 0) + 1
        if not args.quiet or level != "OK":
            emit(level, title, detail)

    print("")
    print("----- 汇总 -----")
    print("工作目录：%s" % Path.cwd())
    print("Python  ：%d.%d.%d" % (sys.version_info.major, sys.version_info.minor,
                                  sys.version_info.micro))
    print("[OK] %d 项  [WARN] %d 项  [FAIL] %d 项"
          % (counts.get("OK", 0), counts.get("WARN", 0), counts.get("FAIL", 0)))

    if counts.get("FAIL", 0) > 0:
        print("")
        print("[FAIL] 环境自检未通过：请按上方 FAIL 项逐条修复后重跑本脚本。")
        print("       骨架尚未补齐时出现 FAIL 属预期，补齐后应全部转为 OK。")
        return 1

    print("")
    print("[OK] 环境自检通过，可以开始开发。")
    if counts.get("WARN", 0) > 0:
        print("     WARN 项不阻塞开工，但建议按 environment/README.md 处理。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
