# 环境说明（environment）

> 状态：首期骨架

本目录规定「链碳台」（CHAINPCF）的开发与运行环境约定，并提供可复用的环境自检脚本。
**技术栈【待确认】**（语言、框架、数据库均未定），因此这里只固化「通用工具链 + 编码规范 + 检查方式」，
不锁定任何业务运行时，也不写未经验证的命令与依赖版本。

## 一、目标环境

| 环境 | 定位 | 载体与说明 |
| --- | --- | --- |
| 开发容器（主） | 团队统一环境 | 由 `.devcontainer/` 定义；基础镜像 `mcr.microsoft.com/devcontainers/base:ubuntu-24.04` |
| 本地环境（次） | 临时调试 | 自行保证与容器一致的 Python 版本与 UTF-8 编码，见「常见问题」 |
| CI 环境 | 结构与文档级检查 | `ubuntu-latest` + Python 3.12，见 `.github/workflows/repo-checks.yml` |

Python 3.12 只是首期骨架取值，**【待确认】：最终版本须与选定技术栈保持一致**；
一致后同步修改 `.devcontainer/devcontainer.json` 与 `.github/workflows/repo-checks.yml`。

## 二、快速开始

1. 安装 VS Code 与 Dev Containers 扩展。
2. 用 VS Code 打开**仓库根目录**（不要打开子目录），选择 `Reopen in Container`。
3. 等待镜像构建完成；容器创建后会自动执行 `postCreateCommand`。
4. 在容器终端手动复跑自检：

   ```bash
   python3 environment/scripts/check_environment.py
   python3 tools/check_repo_structure.py
   ```

5. 两条命令都返回退出码 `0` 即表示环境与结构就绪；此时再按
   [../docs/development/README.md](../docs/development/README.md) 开始开发。

> 首期骨架尚未补齐时，自检会报 `[FAIL] 缺失文件`，属预期现象。

## 三、目录说明

```text
environment/
├── README.md                     本文件：环境约定与排障
└── scripts/
    └── check_environment.py      环境自检脚本（仅标准库）
```

| 文件 | 作用 | 调用方式 |
| --- | --- | --- |
| [scripts/check_environment.py](scripts/check_environment.py) | 检查 Python 版本、平台与编码、工作目录、关键路径、Git、疑似真实数据 | `python3 environment/scripts/check_environment.py [--quiet]` |
| [../tools/check_repo_structure.py](../tools/check_repo_structure.py) | 检查仓库必需文件与目录是否齐备 | `python3 tools/check_repo_structure.py [--quiet]` |

## 四、自检脚本的输出含义

| 前缀 | 含义 | 是否影响退出码 |
| --- | --- | --- |
| `[OK]` | 检查项通过 | 否 |
| `[WARN]` | 建议优化项（如编码非 UTF-8、缺少 `.gitattributes`、`data/` 下有疑似真实数据） | 否 |
| `[FAIL]` | 必须修复项（Python 版本过低、工作目录不是仓库根、必需目录或关键文件缺失、Git 不可用） | 是 |

退出码约定：**无 `FAIL` 返回 `0`，存在 `FAIL` 返回 `1`**。
`--quiet` 只打印明细中的非 `[OK]` 项与汇总，适合 CI 日志。

## 五、常见问题

| 现象 | 原因 | 处理方式 |
| --- | --- | --- |
| 中文显示为乱码 | 终端编码不是 UTF-8（Windows 常见 `cp936`） | 执行 `chcp 65001`；设置 `PYTHONUTF8=1`、`PYTHONIOENCODING=utf-8`；确认 `LANG`/`LC_ALL` 为 `C.UTF-8` |
| 每行末尾多出 `^M`，diff 全是改动 | 换行符为 CRLF | 统一使用 LF；`.editorconfig` 已声明，建议补充 `.gitattributes` |
| 脚本报 `UnicodeEncodeError: 'gbk'` | 中文输出遇到 GBK 控制台 | 两个自检脚本内部已强制 UTF-8 输出；自定义脚本请照做 |
| Git 提示需要用户名/邮箱 | 容器内未配置身份 | 在容器内配置 `user.name` / `user.email`，**不要**把凭据或令牌写入仓库文件 |
| 拉取依赖超时或失败 | 网络受限 | 使用镜像源或企业代理；**不要**把镜像源地址与凭据提交进 Git |
| 无法打开 `docs/product/` 下的 PDF / PPTX | 容器内未安装 LibreOffice | 在宿主机用本地 Office 打开；或在 `.devcontainer/Dockerfile` 中启用 LibreOffice 安装（**是否安装【待确认】**） |
| 自检提示 `data/` 下疑似真实数据 | 可能误放了企业文件 | 立即按 [../.agents/policies/data-security.md](../.agents/policies/data-security.md) 处理，真实数据不得提交进 Git |

## 六、待确认项

| 编号 | 待确认内容 | 影响范围 |
| --- | --- | --- |
| E-1 | 技术栈（语言 / 框架 / 数据库） | 决定镜像内需要追加的运行时与依赖 |
| E-2 | Python 最终版本 | 开发容器 feature 与 CI `setup-python` 的版本 |
| E-3 | 是否在容器内安装 LibreOffice | 镜像体积与文档查看体验 |
| E-4 | 是否需要数据库服务与端口转发 | `devcontainer.json` 的服务与 `forwardPorts` 配置 |

以上任一确定后，请同步更新本文件、`.devcontainer/` 与 `.github/workflows/repo-checks.yml`。

## 七、相关文档

- 全局规则与加载顺序：[../AGENTS.md](../AGENTS.md)
- 开发流程：[../docs/development/README.md](../docs/development/README.md)
- 数据安全底线：[../.agents/policies/data-security.md](../.agents/policies/data-security.md)
- 工具说明：[../tools/README.md](../tools/README.md)
