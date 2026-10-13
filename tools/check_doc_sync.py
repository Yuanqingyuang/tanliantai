#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""链碳台（CHAINPCF）文档联动校验脚本。

用途
    基于 Git 变更集，检查"改了 A 就必须同批改 B"这类**改动联动**规则是否被满足。
    这类规则（AGENTS.md R3、R6）是少数可以完全机器判定的规范——只要拿到
    变更文件清单，一次比对即可得出结论，因此把它们放到 CI 门禁层强制。
    R5（契约先行）只有"contracts 变更须伴随文档"这一可判定部分纳入本脚本，
    "先契约后实现"的顺序仍需人工评审。
    该脚本被 GitHub Actions（.github/workflows/repo-checks.yml）调用。

检查规则
    R3 无依据不改核算口径
        变更集触及 knowledge/formulas/ 或 knowledge/emission-factors/ 时，必须
        同批更新以下之一：
          * knowledge/formulas/formula-register.md
          * knowledge/emission-factors/factor-register.md
          * CHANGELOG.md
          * docs/decisions/ 下新增的 ADR 文件
    R6 文档与代码同步
        变更集触及 modules/、app/ 或 contracts/ 时，必须同批更新 docs/ 或
        CHANGELOG.md。（contracts 的联动只由本条负责，不在 R3 中重复。）

基线选择
    优先取 --base；其次取环境变量 GITHUB_BASE_REF（拼成 origin/<ref>）；
    否则取 origin/main。若 Git 不可用或基线无法解析，则打印提示并**按通过处理**
    （退出码 0），避免在缺少历史的环境里误伤。

约束
    * 仅使用 Python 标准库，兼容 Python 3.9 及以上版本；
    * 只读：只调用 git 的查询子命令，不修改工作区。

用法
    python tools/check_doc_sync.py
    python tools/check_doc_sync.py --base origin/main
    python tools/check_doc_sync.py --quiet --repo-root <仓库根目录>

退出码
    0  规则均满足，或无法取得基线（按通过处理）
    1  存在未满足的联动规则，或脚本运行失败
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# R3：触发目录与被认可的配套登记（contracts 的联动由 R6 负责，不在此重复）
R3_TRIGGERS = ("knowledge/formulas/", "knowledge/emission-factors/")
R3_REGISTERS = (
    "knowledge/formulas/formula-register.md",
    "knowledge/emission-factors/factor-register.md",
)
R3_ALSO_OK = ("CHANGELOG.md",)
R3_ADR_DIR = "docs/decisions/"

# R6：触发目录与被认可的同步目标
R6_TRIGGERS = ("modules/", "app/", "contracts/")
R6_ALSO_OK = ("CHANGELOG.md",)
R6_DOC_DIR = "docs/"


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


def run_git(root, args):
    """执行 git 子命令；返回 (returncode, stdout)。失败返回 (None, "")。"""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root)] + list(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except Exception:
        return None, ""
    out = proc.stdout.decode("utf-8", errors="replace")
    return proc.returncode, out


def resolve_base(root, explicit):
    if explicit:
        return explicit
    ref = os.environ.get("GITHUB_BASE_REF")
    if ref:
        return "origin/" + ref
    return "origin/main"


def changed_files(root, base):
    """返回变更文件清单 (rel, status)。基线不可用时返回 None。"""
    code, _ = run_git(root, ["rev-parse", "--verify", "--quiet", base])
    if code != 0:
        return None
    code, out = run_git(root, ["diff", "--name-status", "--diff-filter=ACMR", base + "...HEAD"])
    if code != 0:
        return None
    entries = []
    for line in out.splitlines():
        line = line.rstrip("\n")
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        status = parts[0].strip()
        path = parts[-1].strip()
        entries.append((path, status))
    return entries


def is_under(rel, prefixes):
    return any(rel.startswith(p) for p in prefixes)


def evaluate(entries):
    """返回 (violations, notes)。"""
    relations = {rel for rel, _ in entries}
    added_paths = {rel for rel, status in entries if status.startswith("A")}
    violations = []

    # R3
    if any(is_under(rel, R3_TRIGGERS) for rel in relations):
        ok = (
            any(reg in relations for reg in R3_REGISTERS)
            or any(p in relations for p in R3_ALSO_OK)
            or any(p.startswith(R3_ADR_DIR) and p.endswith(".md") for p in added_paths)
        )
        if not ok:
            violations.append(
                "R3：修改了核算口径相关文件（knowledge/formulas 或 knowledge/emission-factors），"
                "但未同批更新公式/因子登记表、CHANGELOG.md 或新增 ADR。"
            )

    # R6
    if any(is_under(rel, R6_TRIGGERS) for rel in relations):
        ok = any(rel.startswith(R6_DOC_DIR) for rel in relations) or any(
            p in relations for p in R6_ALSO_OK
        )
        if not ok:
            violations.append(
                "R6：修改了 modules/、app/ 或 contracts/，但未同批更新 docs/ 或 CHANGELOG.md。"
            )

    return violations


def main(argv=None):
    force_utf8_streams()
    parser = argparse.ArgumentParser(
        description="链碳台（CHAINPCF）文档联动校验：检查改动联动规则 R3 / R6 是否满足。"
    )
    parser.add_argument("--base", default=None, help="比较基线（如 origin/main），默认自动推断")
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

    base = resolve_base(root, args.base)
    entries = changed_files(root, base)

    if entries is None:
        print("[WARN] 无法解析比较基线 %s（可能未执行 git fetch 或缺历史）。" % base)
        print("       本检查依赖 Git 变更集，跳过本次联动校验（按通过处理）。")
        print("[OK] 文档联动校验跳过。")
        return 0

    if not args.quiet:
        print("比较基线：%s" % base)
        print("变更文件数：%d" % len(entries))
        for rel, status in entries:
            print("[CHANGE] %s %s" % (status, rel))

    violations = evaluate(entries)

    print("")
    print("===== 文档联动校验汇总 =====")
    print("仓库根目录        ：%s" % root)
    print("比较基线          ：%s" % base)
    print("变更文件数        ：%d" % len(entries))
    print("未满足规则数      ：%d" % len(violations))

    if violations:
        print("")
        print("-- 未满足的联动规则 --")
        for v in violations:
            print("  [FAIL  ] " + v)
        print("")
        print("[FAIL] 文档联动校验未通过：请补齐配套登记或文档后重试。")
        return 1

    print("")
    print("[OK] 文档联动校验通过：变更集满足 R3 与 R6。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
