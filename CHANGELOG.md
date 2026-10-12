# CHANGELOG

本文件记录链碳台（CHAINPCF）仓库的用户可见变更。
格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 计划中
- 数据字典 V0.1 与碳数据包规范 V0.1（2026.12—2027.01）
- 确定性核算引擎原型与核心算法（2027.02—04）

## [0.1.0] - 2026-10-12

### 新增
- 按约定建立仓库目录骨架：`.agents/`、`.devcontainer/`、`environment/`、`docs/`、`knowledge/`、`app/`、`modules/`、`contracts/`、`data/`、`tests/`、`tools/`、`resources/`、`.github/`。
- 根级治理文件：[README.md](README.md)、[AGENTS.md](AGENTS.md)、[CONTRIBUTING.md](CONTRIBUTING.md)、[.editorconfig](.editorconfig)。
- Agent 工作体系：工作方式索引、任务上下文映射、5 个流程（开发、修复、核算变更、审查、发布）、4 项规则（修改边界、测试、数据安全、协作）、2 个模板（任务说明、交付报告）。
- 碳核算知识库骨架：领域术语与 PCBA-SMT 工序、单位换算、核算公式与资源分摊方法、公式登记表、因子库说明与因子登记表、来源登记规则与书目。
- 产品与工程文档骨架：产品定位与 MVP、四层架构与数据流、开发约定、五阶段版本规划、设计决策记录（含 ADR 0001：确定性核算与 AI 副驾驶的边界）。
- 应用与模块骨架：应用外壳、启动、主窗口与工作台，以及 9 个业务模块（项目、制造、数据字典、活动数据、排放因子、核算、数据审核、分析、数据包）的职责与接口约定；跨模块数据契约清单。
- 工程设施：开发容器配置、环境自检脚本 `environment/scripts/check_environment.py`、仓库结构校验脚本 `tools/check_repo_structure.py`、GitHub Actions 工作流 `repo-checks`、PR 模板。
- 测试体系骨架：单元、集成、验收测试范围与基准数据（fixtures）规范。
- 资料归位：品牌标识移入 `resources/`；项目计划书与答辩材料移入 `docs/product/`。

### 变更
- `.gitignore` 扩充为覆盖 Python、Node.js、编辑器、密钥与本项目数据目录的忽略规则。

### 移除
- 删除仓库根目录下的空文件 `笔记.txt` 与 `新建 文本文档.txt`（内容为空，属临时文件）。

### 已知缺口
- 尚无任何可运行代码；技术栈、数据包交换格式、`app/` 形态（桌面外壳 vs Web 工作台）均【待确认】，见 [docs/decisions/README.md](docs/decisions/README.md)。
- 排放因子登记表与公式登记表只有结构，具体数值与条款细节待查证后由人工复核入库。
