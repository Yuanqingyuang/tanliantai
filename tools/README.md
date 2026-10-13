# 工程辅助工具（tools）

> 状态：首期骨架

本目录存放**不依赖业务运行时**的工程辅助工具：结构校验、数据校验、脱敏检查、知识库检查等。
工具面向日常开发与 CI，**优先只用标准库**，以保证在任何机器上都能直接运行。

## 一、已有工具

| 工具 | 用途 | 调用方式 | 退出码 |
| --- | --- | --- | --- |
| [check_repo_structure.py](check_repo_structure.py) | 校验仓库必需文件与目录是否齐备；报告 0 字节必需 Markdown | `python3 tools/check_repo_structure.py [--quiet]` | `0` 通过 / `1` 存在缺失或空文件 |
| [check_links.py](check_links.py) | 校验所有 Markdown 的相对链接与图片引用是否可解析（跳过外链、锚点、代码块） | `python3 tools/check_links.py [--quiet]` | `0` 通过 / `1` 存在失效链接 |
| [check_data_safety.py](check_data_safety.py) | 扫描凭据文件（`.env` 及其变体、`*.pem` 等）与疑似真实企业数据；`data/examples`、`data/templates`、`tests/fixtures` 外的数据文件阻塞 | `python3 tools/check_data_safety.py [--quiet]` | `0` 无 BLOCK / `1` 存在 BLOCK |
| [check_doc_sync.py](check_doc_sync.py) | 按 Git 变更集检查改动联动规则 R3（核算口径）与 R6（文档同步） | `python3 tools/check_doc_sync.py [--base <ref>] [--quiet]` | `0` 满足或无法取基线 / `1` 规则未满足 |
| [check_governance.py](check_governance.py) | 校验模板章节、ADR 必备字段与索引一致性、任务台账完整性（ID/状态/更新日期/留痕文件）；`--changed-only` 检查新增内容的「待确认」是否带负责人 | `python3 tools/check_governance.py [--changed-only] [--base <ref>] [--branch <name>] [--quiet]` | `0` 通过 / `1` 未通过 |
| [../environment/scripts/check_environment.py](../environment/scripts/check_environment.py) | 校验开发环境：Python 版本、平台与编码、工作目录、关键路径、Git、`data/` 疑似真实数据 | `python3 environment/scripts/check_environment.py [--quiet]` | `0` 无 FAIL / `1` 存在 FAIL |

以上工具都要求 Python 3.9+、仅标准库、强制 UTF-8 输出，可安全地在 Windows、Linux 与 CI 上运行。

### 日常用法

```bash
# 提交前自检（两条都应为 0）
python3 tools/check_repo_structure.py
python3 environment/scripts/check_environment.py

# CI 日志更简短
python3 tools/check_repo_structure.py --quiet
```

## 二、工具编写约定

| 约定 | 说明 |
| --- | --- |
| 依赖 | 优先纯标准库；确需第三方依赖时必须说明理由，并在环境说明中登记 |
| 编码 | 输出前把 stdout/stderr 切到 UTF-8，避免 Windows GBK 报错 |
| 换行与编码 | 脚本本身 UTF-8 无 BOM、LF 换行 |
| 输出格式 | 逐项输出 `[OK]` / `[WARN]` / `[FAIL]`（或 `[MISSING]`），结尾必须有汇总 |
| 退出码 | `0` 表示通过，`1` 表示存在必须修复的问题；**警告不影响退出码** |
| 参数 | 至少支持 `--quiet`；路径参数默认从脚本位置推导，不依赖调用者所在目录 |
| 安全性 | 只做只读检查；不得删除、移动或改写仓库文件 |
| 幂等 | 同一仓库状态多次运行结果一致 |
| 文档 | 每个工具在 `tools/README.md` 登记用途、调用方式与退出码 |

## 三、规划中的工具

| 工具（规划） | 目标 | 依赖前提 | 状态 |
| --- | --- | --- | --- |
| 数据校验工具 | 按 [../data/templates/README.md](../data/templates/README.md) 校验导入文件的字段、单位与必填项 | 数据字典 V0.1 定稿 | 【待确认】 |
| 知识库检查工具 | 检查 `knowledge/` 下公式、因子、文献条目是否成登记、是否有空条目 | 登记表格式定稿 | 【待确认】 |
| 数据包解析工具 | 解析并校验导出的 `DataPackage` 结构，支持复算 | 数据包规范 V0.1 | 【待确认】 |

规划中的工具在实现前须先确定依赖前提，**不得先写代码再补规范**。

## 四、与 CI 的关系

`.github/workflows/repo-checks.yml` 在 `push` 与 `pull_request` 到 `main` 时执行，拆为 4 个 job：

| job | 执行的命令 | 是否阻塞 |
| --- | --- | --- |
| `structure` | `python tools/check_repo_structure.py`；`python environment/scripts/check_environment.py \|\| true` | 结构检查阻塞；环境自检不阻塞 |
| `data-safety` | `python tools/check_data_safety.py` | 阻塞 |
| `links` | `python tools/check_links.py --quiet` | 阻塞 |
| `change-guard` | `python tools/check_governance.py --changed-only`；`python tools/check_doc_sync.py` | 阻塞 |

`change-guard` 需要完整 Git 历史（`fetch-depth: 0`）与可解析的基线分支；取不到基线时脚本按通过处理，不会误伤。该 job 实质在 **PR 场景**生效——`push` 到 `main` 时基线等于 HEAD、变更集为空，等同空跑（直接推送 `main` 本身由分支保护禁止）。

这套门禁是 [ADR 0002](../docs/decisions/0002-agent-governance-framework.md) 中"分层强制模型"的 L3 层：建议在分支保护中把 `structure`、`data-safety`、`links`、`change-guard` 设为 required status checks。

技术栈【待确认】之前，CI 只做**结构与文档级**检查：不编译、不装依赖、不跑单元测试。

## 五、禁止事项

- 禁止在工具中读取、收集或外传真实企业数据。
- 禁止把工具做成"必须联网才能跑"；网络受限环境下也应能完成结构与文档级检查。
- 禁止用工具掩盖问题：警告项应在 PR 中说明处理结论，而不是长期忽略。

## 六、相关文档

- 环境说明：[../environment/README.md](../environment/README.md)
- 数据安全底线：[../.agents/policies/data-security.md](../.agents/policies/data-security.md)
- 测试规则：[../.agents/policies/testing.md](../.agents/policies/testing.md)
- 知识库入口：[../knowledge/README.md](../knowledge/README.md)
- 契约入口：[../contracts/README.md](../contracts/README.md)
