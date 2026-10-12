# 工程辅助工具（tools）

> 状态：首期骨架

本目录存放**不依赖业务运行时**的工程辅助工具：结构校验、数据校验、脱敏检查、知识库检查等。
工具面向日常开发与 CI，**优先只用标准库**，以保证在任何机器上都能直接运行。

## 一、已有工具

| 工具 | 用途 | 调用方式 | 退出码 |
| --- | --- | --- | --- |
| [check_repo_structure.py](check_repo_structure.py) | 校验仓库必需文件与目录是否齐备；报告 0 字节必需 Markdown；提示疑似真实数据 | `python3 tools/check_repo_structure.py [--quiet]` | `0` 通过 / `1` 存在缺失或空文件 |
| [../environment/scripts/check_environment.py](../environment/scripts/check_environment.py) | 校验开发环境：Python 版本、平台与编码、工作目录、关键路径、Git、`data/` 疑似真实数据 | `python3 environment/scripts/check_environment.py [--quiet]` | `0` 无 FAIL / `1` 存在 FAIL |

两者都要求 Python 3.9+、仅标准库、强制 UTF-8 输出，可安全地在 Windows、Linux 与 CI 上运行。

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
| 脱敏检查工具 | 对 `data/examples/` 与 [../tests/fixtures/README.md](../tests/fixtures/README.md) 做敏感关键字与模式扫描 | 脱敏规则清单 | 【待确认】 |
| 数据包解析工具 | 解析并校验导出的 `DataPackage` 结构，支持复算 | 数据包规范 V0.1 | 【待确认】 |

规划中的工具在实现前须先确定依赖前提，**不得先写代码再补规范**。

## 四、与 CI 的关系

`.github/workflows/repo-checks.yml` 在 `push` 与 `pull_request` 到 `main` 时执行：

1. `python tools/check_repo_structure.py` —— 缺失必需路径即失败；
2. `python environment/scripts/check_environment.py || true` —— 环境脚本在 CI 上失败不阻塞，但输出保留。

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
