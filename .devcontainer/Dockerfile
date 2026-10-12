# =============================================================================
# 链碳台 CHAINPCF —— 开发容器镜像
# 基础镜像：mcr.microsoft.com/devcontainers/base:ubuntu-24.04
# 说明：本镜像只固化“通用工具链 + UTF-8 中文环境 + 非 root 用户”，
#       语言 / 框架 / 数据库均【待确认】，不在本文件里安装任何业务运行时。
# =============================================================================

FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

ARG DEBIAN_FRONTEND=noninteractive

# -----------------------------------------------------------------------------
# 1. 系统级依赖
#    git / curl / wget 为版本控制与下载所需；build-essential 供后续编译型依赖使用；
#    locales 与 tzdata 用于中文 UTF-8 环境与时间戳一致性；ca-certificates 供 HTTPS 访问。
# -----------------------------------------------------------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        curl \
        wget \
        build-essential \
        ca-certificates \
        locales \
        tzdata \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# 2. 中文与英文 UTF-8 locale
#    生成 zh_CN.UTF-8 与 en_US.UTF-8，二者同时存在，避免中文文档在容器内出现乱码。
#    运行时默认 locale 取 C.UTF-8（见下方 ENV），需要中文排序/日期时再切换：
#      export LANG=zh_CN.UTF-8
# -----------------------------------------------------------------------------
RUN locale-gen zh_CN.UTF-8 \
    && locale-gen en_US.UTF-8 \
    && update-locale --no-checks

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    LANGUAGE=zh_CN:zh:en_US:en \
    PYTHONIOENCODING=utf-8 \
    PYTHONUTF8=1

# -----------------------------------------------------------------------------
# 3. LibreOffice（可选，【待确认】是否安装）
#    若需要在容器内直接打开 docs/product/ 下的 PDF 与答辩 PPTX，请取消下面 RUN 的注释；
#    不安装时请在宿主机用本地 Office 查看，或在 VS Code 中只读预览，
#    相关取舍与替代方案见 environment/README.md 的“常见问题”。
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends libreoffice \
#     && rm -rf /var/lib/apt/lists/*
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# 4. 非 root 用户 vscode
#    基础镜像通常已内置 vscode 用户，存在则直接复用，不存在才创建；
#    工作区目录 /workspaces 归属该用户，避免容器内写文件时需要 sudo。
# -----------------------------------------------------------------------------
RUN if ! id -u vscode > /dev/null 2>&1; then \
        useradd --create-home --shell /bin/bash --uid 1000 vscode; \
    fi \
    && mkdir -p /workspaces \
    && chown -R vscode:vscode /workspaces

USER vscode
WORKDIR /workspaces

# -----------------------------------------------------------------------------
# 5. 无害自检
#    仅打印版本信息，任何一项失败都不应导致构建失败；
#    Python 由 devcontainer feature（ghcr.io/devcontainers/features/python:1）安装，
#    构建阶段可能尚不存在，因此用 || true 兜底。
# -----------------------------------------------------------------------------
RUN python3 --version || true; \
    git --version || true; \
    locale -a || true
