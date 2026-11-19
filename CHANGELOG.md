# CHANGELOG

本文件记录链碳台（CHAINPCF）仓库的用户可见变更。
格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 新增
- R2 知识库与指标主体建设（T-0004）：术语表 TERM-xxx（44 条）、单位表 UNIT-xxx（20 条）、公式登记 F-<域>-<三位序号>（15 条）、书目表 R-xxx（13 条）四大基线文档，补全 GB/T 24067-2024 条款号、GB/T 2589-2020 标准煤当量、IPCC AR6 GWP、区域电网因子来源，明确分摊/分配口径区别。

### 变更
- 任务台账：T-0004 状态更新为“已完成”，填写负责人 R2、确认人 袁青扬、更新日期 2026-11-20.

### 新增
- 技术基线决策：[ADR 0003](docs/decisions/0003-local-web-workbench-baseline.md)（已接受）确定本地 Web 客户端、Vue 3/FastAPI/PostgreSQL、内网多用户（角色权限前置）、开发期云端 API + 真实数据本地处理。
- 任务分解：[docs/planning/wbs.md](docs/planning/wbs.md)按交付物切分五阶段 35 项任务，负责人统一留待认领，并在 [任务台账](docs/planning/tasks.md) 登记 T-0002T-0036。
- 决策清单：更新 [docs/decisions/README.md](docs/decisions/README.md) 的 D1D16，标注已形成 ADR 提案与未启动项。
- Agent 协作框架提案：[ADR 0002](docs/decisions/0002-agent-governance-framework.md)用分层强制模型把 AGENTS.md 规则 R1R9 从散文规范落到可执行机制（L0 规范 / L1 模板 / L2 本地检查 / L3 CI 门禁 / L4 平台机制）。
- 确定性检查工具 4 个：[check_links.py](tools/check_links.py)（相对链接）、[check_data_safety.py](tools/check_data_safety.py)（凭据与真实数据）、[check_doc_sync.py](tools/check_doc_sync.py)（改动联动 R3/R6）、[check_governance.py](tools/check_governance.py)（模板/ADR/待确认留痕）。
- 文件分区机制：[.github/CODEOWNERS](.github/CODEOWNERS)，落地 collaboration.md 3 与规则 R7（需在分支保护中启用 Require review from Code Owners）。
- CI 门禁扩展：[repo-checks](.github/workflows/repo-checks.yml) 由单 job 拆为 structure、data-safety、links、change-guard 四个 job。
- 任务台账：[docs/planning/tasks.md](docs/planning/tasks.md)登记任务的 ID、负责人、确认人、影响目录与状态，作为留痕与并行分区的共享事实。
- 文档写作流程：工作流 [authoring.md](.agents/workflows/authoring.md)依据清单大纲起草依据核对一致性状态标注人审，复用 knowledge/ 的来源与审核状态模型。
- 人工确认与签注 SOP：[review.md 7](.agents/workflows/review.md)定义必审范围、抽样比例与签注落点（任务台账 + 交付报告）。
- 变更分级与必备动作：[boundaries.md 5](.agents/policies/boundaries.md)按 T0/T1/T2 决定流程成本，避免改错别字与改公式同成本。
- R2 的机器可验证形式：新增架构不变量必测项（[testing.md 3](.agents/policies/testing.md)），断言 AI 输出永不进入核算输入路径。
- 治理层自身的变更控制：[.agents/README.md 5](.agents/README.md)AGENTS.md 与 .agents/ 的规则性改动按敏感变更管理（台账 + CHANGELOG + 必要时 ADR）。
- 任务留痕的落点与校验：以 [docs/planning/tasks/T-0001/](docs/planning/tasks/T-0001/task.md) 作为任务说明与交付报告的归档实例；check_governance.py 新增任务台账完整性校验（ID、状态、更新日期、留痕文件是否存在，以及分支名与任务号的关联）。

### 变更
- [check_repo_structure.py](tools/check_repo_structure.py)：移除重复的警告级敏感数据扫描（改由 check_data_safety.py 承担阻塞职责），并把新增的脚本、CODEOWNERS 与 ADR 0002 纳入必需路径清单。

### 修复
- 治理检查：[check_governance.py](tools/check_governance.py) 现可识别带对象的 【待确认:…】（此前只认裸形式，导致知识库写法普遍漏检）；ADR 校验新增 > 日期： 必备字段，并补齐 [ADR 0001](docs/decisions/0001-deterministic-calculation-vs-ai-copilot.md) 的日期。
- 联动检查：[check_doc_sync.py](tools/check_doc_sync.py) 的 R3 报错文案去掉已不属其触发范围的 contracts；change-guard 明确仅 PR 场景生效。
- 一致性：统一 Python 下限为 3.9（[check_environment.py](environment/scripts/check_environment.py) 由 3.10 下调）；[.gitignore](.gitignore) 放行 .env.sample/.env.template；文档状态词表补规划中；CHANGELOG 分组词表补计划中/已知缺口；修正 [CONTRIBUTING.md](CONTRIBUTING.md) 任务号的自相矛盾与 [review.md 7](.agents/workflows/review.md) 的引用。

