#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""链碳台（CHAINPCF）Markdown 相对链接校验脚本。

用途
    扫描仓库内所有 Markdown 文件，检查其中的**相对链接与图片引用**是否指向
    真实存在的文件或目录。用于兑现 AGENTS.md 规则 R8「可验证」与 R6「文档与
    代码同步」：文档里的路径一旦写错，本地与 CI 都能立刻发现。
    该脚本被本地自检与 GitHub Actions（.github/workflows/repo-checks.yml）共用。

判定范围
    * 只检查相对引用；以下一律跳过：外部链接（http/https/ftp/mailto/tel/data）、
      以 `#` 开头的纯锚点、以及围栏代码块与行内代码中的内容。
    * 目标里的 `#锚点` 会被剥离，只校验其前面的路径部分。
    * 目标若带标题（`"..."` / `'...'`）或尖括号包裹，会先剥离再校验。
    * 存在性判断**区分大小写**（逐段比对真实目录项），保证 Windows 本地与
      Linux CI 结论一致。

约束
    * 仅使用 Python 标准库，兼容 Python 3.9 及以上版本；
    * 只读检查，不修改任何文件；
    * 路径参数默认从脚本位置推导，不依赖调用者所在目录。

用法
    python tools/check_links.py
    python tools/check_links.py --quiet
    python tools/check_links.py --repo-root <仓库根目录>

退出码
    0  全部相对链接均可解析
    1  存在失效链接，或脚本运行失败
"""

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

# 遍历时跳过的目录
SKIP_DIR_NAMES = (".git", "__pycache__", ".venv", "venv", "node_modules", ".pytest_cache")

# 围栏代码块起始/结束标记
FENCE_RE = re.compile(r"^\s*(```|~~~)")
# Markdown 链接与图片引用：[文本](目标) 或 ![替代文本](目标)
# 目标允许一层嵌套圆括号（如 foo_(1).md），避免在首个 ')' 处截断
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^()]*(?:\([^()]*\)[^()]*)*)\)")
# 行内代码：`...`
INLINE_CODE_RE = re.compile(r"`[^`]*`")
# 链接目标末尾的标题： "..." 或 '...'
TITLE_RE = re.compile(r"""\s+("[^"]*"|'[^']*')\s*$""")
# 需要跳过的外部协议前缀
EXTERNAL_PREFIXES = ("http://", "https://", "ftp://", "mailto:", "tel:", "data:", "//")


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


def iter_markdown_files(root):
    """产出仓库内所有 Markdown 文件路径。"""
    for dirpath, dirnames, filenames in os.walk(str(root)):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        for name in filenames:
            if name.lower().endswith(".md"):
                yield Path(dirpath) / name


def extract_targets(text):
    """从 Markdown 文本中提取相对链接目标（已剥离标题与锚点前的原始目标）。"""
    targets = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = INLINE_CODE_RE.sub("", line)
        for match in LINK_RE.finditer(line):
            raw = match.group(1).strip()
            if not raw:
                continue
            if raw.startswith("<") and raw.endswith(">"):
                raw = raw[1:-1].strip()
            raw = TITLE_RE.sub("", raw).strip()
            if raw:
                targets.append(raw)
    return targets


def is_external(target):
    return target.lower().startswith(EXTERNAL_PREFIXES) or target.startswith("#")


def exists_exact(path):
    """按大小写精确判断路径是否存在。

    跨平台一致：Windows 文件系统大小写不敏感，直接用 Path.exists() 会把
    `Readme.md` 这类错误大小写判为存在，导致本地通过而 Linux CI 失败。
    这里逐段用 os.scandir 比对真实目录项名称，确保大小写完全一致。
    """
    try:
        norm = Path(os.path.normpath(str(path)))
    except Exception:
        return Path(path).exists()
    if not norm.anchor:
        return norm.exists()
    current = Path(norm.anchor)
    for part in norm.parts[1:]:
        matched = None
        try:
            with os.scandir(str(current)) as entries:
                for entry in entries:
                    if entry.name == part:
                        matched = entry.name
                        break
        except OSError:
            return False
        if matched is None:
            return False
        current = current / matched
    return norm.exists()


def main(argv=None):
    force_utf8_streams()
    parser = argparse.ArgumentParser(
        description="链碳台（CHAINPCF）Markdown 相对链接校验：检查文档中的路径引用是否有效。"
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

    checked = 0
    broken = []
    md_files = sorted(iter_markdown_files(root))
    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:  # pragma: no cover - 兜底
            print("[FAIL] 无法读取文件：%s（%s）" % (md, exc))
            return 1
        for target in extract_targets(text):
            if is_external(target):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            path_part = unquote(path_part)
            checked += 1
            if not args.quiet:
                print("[CHECK ] %s -> %s" % (md.relative_to(root).as_posix(), target))
            if not exists_exact(md.parent / path_part):
                try:
                    shown = md.relative_to(root).as_posix()
                except ValueError:
                    shown = md.as_posix()
                broken.append((shown, target))
                if not args.quiet:
                    print("[FAIL  ] %s -> %s" % (shown, target))

    print("")
    print("===== Markdown 链接校验汇总 =====")
    print("仓库根目录        ：%s" % root)
    print("扫描 Markdown 数  ：%d" % len(md_files))
    print("校验相对链接数    ：%d" % checked)
    print("失效链接数        ：%d" % len(broken))

    if broken:
        print("")
        print("-- 失效链接清单 --")
        for shown, target in broken:
            print("  [FAIL  ] %s -> %s" % (shown, target))
        print("")
        print("[FAIL] 链接校验未通过：存在 %d 条失效链接，请修正路径或文件。" % len(broken))
        return 1

    print("")
    print("[OK] 链接校验通过：全部相对链接均可解析。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
