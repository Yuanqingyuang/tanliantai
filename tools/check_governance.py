#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""链碳台（CHAINPCF）治理结构校验脚本。

用途
    校验支撑"结构化声明 + 抽样人审"的治理骨架是否完整：模板章节是否被删改、
    ADR 是否具备必备字段与索引条目、以及新增内容里的「待确认」是否按其要求
    带上了负责人/确认人。对应 AGENTS.md 规则 R1「不造数」与 R9「留痕」所能
    达到的确定性部分（其语义部分仍需人工抽检）。
    该脚本被 GitHub Actions（.github/workflows/repo-checks.yml）调用。

检查项
    1. 模板完整性：.agents/templates/task.md 必须保留 `## 1.`~`## 11.`；
       .agents/templates/delivery-report.md 必须保留 `## 1.`~`## 10.`。
    2. ADR 字段：docs/decisions/NNNN-*.md 必须含 `> 状态：`、`## 背景与问题`、`## 决策`。
    3. ADR 索引一致性：每个 ADR 文件都必须出现在 docs/decisions/README.md 中。
    4. 待确认留痕（仅 --changed-only）：本次新增的 Markdown 行若含「【待确认】」，
       则该行须同时出现「负责人」或「确认人」，否则判失败。
    5. 任务台账完整性：docs/planning/tasks.md 的每一行须为合法任务 ID（T-0001）、
       状态取值合法、更新日期为 YYYY-MM-DD；状态为「已完成」须填「确认」列；
       状态为「待评审/已完成」须存在留痕文件 docs/planning/tasks/<ID>/{task.md,delivery-report.md}。
       另：若分支名含 T-xxxx，则该编号须已登记在台账中。

约束
    * 仅使用 Python 标准库，兼容 Python 3.9 及以上版本；
    * 只读检查，不修改任何文件。

用法
    python tools/check_governance.py
    python tools/check_governance.py --changed-only
    python tools/check_governance.py --changed-only --base origin/main --quiet

退出码
    0  全部检查项通过
    1  存在未通过的检查项，或脚本运行失败
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIR_NAMES = (".git", "__pycache__", ".venv", "venv", "node_modules", ".pytest_cache")

TASK_TEMPLATE = ".agents/templates/task.md"
DELIVERY_TEMPLATE = ".agents/templates/delivery-report.md"
TASK_SECTIONS = 11
DELIVERY_SECTIONS = 10

ADR_DIR = "docs/decisions"
ADR_INDEX = "docs/decisions/README.md"
ADR_FILE_RE = re.compile(r"^\d{4}-.*\.md$")
ADR_REQUIRED_FIELDS = ("## 背景与问题", "## 决策")

# 待确认标记：兼容裸形式与带对象形式（项目规范见 knowledge/README.md §5）
PENDING_MARKS = ("【待确认】", "【待确认：")
PENDING_OWNER_MARKS = ("负责人", "确认人")

SECTION_RE = re.compile(r"^##\s+(\d+)\.", re.MULTILINE)

# 行内代码（反引号）内容不参与「待确认」匹配，避免文档中引用该格式时误报
INLINE_CODE_RE = re.compile(r"`[^`]*`")

TASK_LEDGER = "docs/planning/tasks.md"
TASK_ARTIFACT_DIR = "docs/planning/tasks"
TASK_ID_RE = re.compile(r"^T-\d{4}$")
TASK_STATUSES = ("待认领", "进行中", "待评审", "已完成", "已取消")
TASK_NEED_ARTIFACTS = ("待评审", "已完成")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EMPTY_CELLS = ("", "—", "-")


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


def read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def check_template_sections(root, rel, expected, violations):
    path = root / rel
    if not path.is_file():
        violations.append("%s 不存在" % rel)
        return
    nums = {int(m) for m in SECTION_RE.findall(read_text(path))}
    missing = [n for n in range(1, expected + 1) if n not in nums]
    if missing:
        violations.append(
            "%s 缺少章节：%s" % (rel, "、".join("## %d." % n for n in missing))
        )


def check_adr(root, violations):
    adr_dir = root / ADR_DIR
    if not adr_dir.is_dir():
        violations.append("%s 目录不存在" % ADR_DIR)
        return
    index_text = read_text(root / ADR_INDEX)
    adr_files = sorted(
        p.name for p in adr_dir.iterdir() if p.is_file() and ADR_FILE_RE.match(p.name)
    )
    if not adr_files:
        violations.append("%s 下未发现任何 ADR 文件" % ADR_DIR)
        return
    for name in adr_files:
        text = read_text(adr_dir / name)
        if "> 状态：" not in text:
            violations.append("%s/%s 缺少 `> 状态：` 字段" % (ADR_DIR, name))
        if "> 日期：" not in text:
            violations.append("%s/%s 缺少 `> 日期：` 字段" % (ADR_DIR, name))
        for field in ADR_REQUIRED_FIELDS:
            if field not in text:
                violations.append("%s/%s 缺少 `%s` 章节" % (ADR_DIR, name, field))
        if name not in index_text:
            violations.append("%s/%s 未登记在 %s 索引中" % (ADR_DIR, name, ADR_INDEX))


def run_git(root, args):
    try:
        proc = subprocess.run(
            ["git", "-C", str(root)] + list(args),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except Exception:
        return None, ""
    return proc.returncode, proc.stdout.decode("utf-8", errors="replace")


def resolve_base(explicit):
    if explicit:
        return explicit
    ref = os.environ.get("GITHUB_BASE_REF")
    if ref:
        return "origin/" + ref
    return "origin/main"


def check_pending_changed(root, base, violations):
    """仅检查本次新增的 Markdown 行里的「待确认」是否带负责人/确认人。"""
    code, _ = run_git(root, ["rev-parse", "--verify", "--quiet", base])
    if code != 0:
        print("[WARN] 无法解析比较基线 %s，跳过「待确认」留痕检查。" % base)
        return
    code, out = run_git(
        root, ["diff", "--unified=0", "--diff-filter=ACMR", base + "...HEAD", "--", "*.md"]
    )
    if code != 0:
        print("[WARN] 无法获取 Markdown 变更集，跳过「待确认」留痕检查。")
        return
    current_file = "(未知文件)"
    for line in out.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:].strip()
            continue
        if line.startswith("+++"):
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        added = line[1:]
        probe = INLINE_CODE_RE.sub("", added)
        if any(m in probe for m in PENDING_MARKS) and not any(m in probe for m in PENDING_OWNER_MARKS):
            violations.append(
                "新增「待确认」未标注负责人/确认人：%s → %s"
                % (current_file, added.strip())
            )


def resolve_branch(explicit, root):
    if explicit:
        return explicit
    ref = os.environ.get("GITHUB_HEAD_REF")
    if ref:
        return ref
    code, out = run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    if code == 0:
        name = out.strip()
        if name and name != "HEAD":
            return name
    return ""


def check_task_ledger(root, branch, violations):
    """校验任务台账自身的完整性与留痕文件是否存在。"""
    path = root / TASK_LEDGER
    if not path.is_file():
        violations.append("%s 不存在" % TASK_LEDGER)
        return
    rows = []
    for raw in read_text(path).splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 10:
            continue
        if cells[0] == "ID" or set(cells[0]) <= set("-: "):
            continue
        rows.append(cells)
    seen = set()
    for cells in rows:
        tid, status, confirm, updated = cells[0], cells[5], cells[8], cells[9]
        if not TASK_ID_RE.match(tid):
            violations.append("%s 任务 ID 不合规：%s" % (TASK_LEDGER, tid))
            continue
        if tid in seen:
            violations.append("%s 任务 ID 重复：%s" % (TASK_LEDGER, tid))
        seen.add(tid)
        if status not in TASK_STATUSES:
            violations.append("%s/%s 状态不合规：%s" % (TASK_LEDGER, tid, status))
        if not DATE_RE.match(updated):
            violations.append("%s/%s 更新日期应为 YYYY-MM-DD：%s" % (TASK_LEDGER, tid, updated))
        if status == "已完成" and confirm in EMPTY_CELLS:
            violations.append("%s/%s 状态为已完成但「确认」列为空" % (TASK_LEDGER, tid))
        if status in TASK_NEED_ARTIFACTS:
            for artifact in ("task.md", "delivery-report.md"):
                rel = "%s/%s/%s" % (TASK_ARTIFACT_DIR, tid, artifact)
                if not (root / rel).is_file():
                    violations.append("%s/%s 缺少留痕文件：%s" % (TASK_LEDGER, tid, rel))
    if branch:
        match = re.search(r"T-\d{4}", branch)
        if match and match.group(0) not in seen:
            violations.append("分支 %s 引用的任务 %s 未登记在 %s" % (branch, match.group(0), TASK_LEDGER))


def main(argv=None):
    force_utf8_streams()
    parser = argparse.ArgumentParser(
        description="链碳台（CHAINPCF）治理结构校验：模板、ADR 与「待确认」留痕。"
    )
    parser.add_argument("--changed-only", action="store_true",
                        help="额外检查本次新增内容里的「待确认」是否带负责人/确认人")
    parser.add_argument("--base", default=None, help="比较基线（如 origin/main），默认自动推断")
    parser.add_argument("--branch", default=None, help="当前分支名，用于校验分支引用的任务号是否已登记")
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

    violations = []
    check_template_sections(root, TASK_TEMPLATE, TASK_SECTIONS, violations)
    check_template_sections(root, DELIVERY_TEMPLATE, DELIVERY_SECTIONS, violations)
    check_adr(root, violations)
    check_task_ledger(root, resolve_branch(args.branch, root), violations)
    if args.changed_only:
        check_pending_changed(root, resolve_base(args.base), violations)

    print("")
    print("===== 治理结构校验汇总 =====")
    print("仓库根目录        ：%s" % root)
    print("检查模式          ：%s" % ("变更集（--changed-only）" if args.changed_only else "全量"))
    print("未通过项数        ：%d" % len(violations))

    if violations:
        print("")
        print("-- 未通过项清单 --")
        for v in violations:
            print("  [FAIL  ] " + v)
        print("")
        print("[FAIL] 治理结构校验未通过：请修复上述问题后重试。")
        return 1

    print("")
    print("[OK] 治理结构校验通过：模板、ADR、任务台账与「待确认」留痕均符合约定。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
