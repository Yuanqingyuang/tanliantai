# CHANGELOG

本文件记录链碳台（CHAINPCF）仓库的用户可见变更。
格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增
- 技术基线决策：[ADR 0003](docs/decisions/0003-local-web-workbench-baseline.md)（已接受）——确定本地 Web 客户端、Vue 3/FastAPI/PostgreSQL、内网多用户（角色权限前置）、开发期云端 API + 真实数据本地处理。
- 任务分解：[docs/planning/wbs.md](docs/planning/wbs.md)——按交付物切分五阶段 35 项任务，负责人统一留「待认领」，并在 [任务台账](docs/planning/tasks.md) 登记 T-0002–T-0036。
- 决策清单：更新 [docs/decisions/README.md](docs/decisions/README.md) 的 D1–D16，标注已形成 ADR 提案与未启动项。
- Agent 协作框架提案：[ADR 0002](docs/decisions/0002-agent-governance-framework.md)——用"分层强制模型"把 AGENTS.md 规则 R1–R9 从散文规范落到可执行机制（L0 规范 / L1 模板 / L2 本地检查 / L3 CI 门禁 / L4 平台机制）。
- 确定性检查工具 4 个：[check_links.py](tools/check_links.py)（相对链接）、[check_data_safety.py](tools/check_data_safety.py)（凭据与真实数据）、[check_doc_sync.py](tools/check_doc_sync.py)（改动联动 R3/R6）、[check_governance.py](tools/check_governance.py)（模板/ADR/待确认留痕）。
- 文件分区机制：[.github/CODEOWNERS](.github/CODEOWNERS)，落地 collaboration.md §3 与规则 R7（需在分支保护中启用 "Require review from Code Owners"）。
- CI 门禁扩展：[repo-checks](.github/workflows/repo-checks.yml) 由单 job 拆为 `structure`、`data-safety`、`links`、`change-guard` 四个 job。
- 任务台账：[docs/planning/tasks.md](docs/planning/tasks.md)——登记任务的 ID、负责人、确认人、影响目录与状态，作为留痕与并行分区的共享事实。
- 文档写作流程：工作流 [authoring.md](.agents/workflows/authoring.md)——依据清单→大纲→起草→依据核对→一致性→状态标注→人审，复用 `knowledge/` 的来源与审核状态模型。
- 人工确认与签注 SOP：[review.md §7](.agents/workflows/review.md)——定义必审范围、抽样比例与签注落点（任务台账 + 交付报告）。
- 变更分级与必备动作：[boundaries.md §5](.agents/policies/boundaries.md)——按 T0/T1/T2 决定流程成本，避免"改错别字"与"改公式"同成本。
- R2 的机器可验证形式：新增"架构不变量"必测项（[testing.md §3](.agents/policies/testing.md)），断言 AI 输出永不进入核算输入路径。
- 治理层自身的变更控制：[.agents/README.md §5](.agents/README.md)——`AGENTS.md` 与 `.agents/` 的规则性改动按敏感变更管理（台账 + CHANGELOG + 必要时 ADR）。
- 任务留痕的落点与校验：以 [docs/planning/tasks/T-0001/](docs/planning/tasks/T-0001/task.md) 作为任务说明与交付报告的归档实例；`check_governance.py` 新增任务台账完整性校验（ID、状态、更新日期、留痕文件是否存在，以及分支名与任务号的关联）。
- 阶段一排期建议稿：[阶段一任务书](docs/planning/phase-1-task-book.md)——按角色 R1–R5 组织九项任务的交付物、人日与逐周行动参考，明确 T-0005 的 a/b 交付段、五个角色的确认人建议与阶段一关口材料。

### 变更
- [check_repo_structure.py](tools/check_repo_structure.py)：移除重复的警告级敏感数据扫描（改由 `check_data_safety.py` 承担阻塞职责），并把新增的脚本、CODEOWNERS 与 ADR 0002 纳入必需路径清单。
- [WBS](docs/planning/wbs.md)：按阶段一实际排期修正依赖——T-0005 不再依赖 T-0003、T-0006 与 T-0005 解耦（取 a 段初稿为非阻塞输入）、T-0007 改依 T-0003 与 T-0010、T-0008 只依赖 T-0005 a 段（T-0004 为术语参考）；T-0008 验收口径改为只由指导教师签注。

### 修复
- 治理检查：[check_governance.py](tools/check_governance.py) 现可识别带对象的 `【待确认：…】`（此前只认裸形式，导致知识库写法普遍漏检）；ADR 校验新增 `> 日期：` 必备字段，并补齐 [ADR 0001](docs/decisions/0001-deterministic-calculation-vs-ai-copilot.md) 的日期。
- 联动检查：[check_doc_sync.py](tools/check_doc_sync.py) 的 R3 报错文案去掉已不属其触发范围的 `contracts`；`change-guard` 明确"仅 PR 场景生效"。
- 一致性：统一 Python 下限为 3.9（[check_environment.py](environment/scripts/check_environment.py) 由 3.10 下调）；[.gitignore](.gitignore) 放行 `.env.sample`/`.env.template`；文档状态词表补"规划中"；CHANGELOG 分组词表补"计划中/已知缺口"；修正 [CONTRIBUTING.md](CONTRIBUTING.md) 任务号的自相矛盾与 [review.md §7](.agents/workflows/review.md) 的引用。
- 归属回填：[任务台账](docs/planning/tasks.md) 中 T-0001 负责人更正为赵天志（@55msi）并回填 PR #1，T-0002 补确认人袁青扬（@Yuanqingyuang）；两份任务的说明与交付报告同步执行人。台账「确认」列仍为「—」，合并 PR 不等于签注。

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
