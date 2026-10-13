# .agents 目录说明：Agent 工作方式总述

> 状态：首期骨架

本目录是「链碳台（CHAINPCF）」项目中人机协作的**规则入口**。它不存放产品知识本身，只规定：Agent 在什么任务下读什么资料、按什么流程做事、在哪些边界内改动文件、以什么形式交付结果。

项目定位：AI 辅助的 PCBA-SMT 工序级碳数据字典、核算工具与数据包。核算依据 GB/T 24067-2024。任何 Agent 行为都不得削弱"可复核、可交付、同一输入→同一结果"这一底线。

## 1. 加载顺序（每次任务开始必须按序执行）

| 顺序 | 文件 | 读取目的 |
| --- | --- | --- |
| 1 | [`AGENTS.md`](../AGENTS.md) | 仓库级硬性规则与禁止项，优先级最高 |
| 2 | [`.agents/context-map.md`](context-map.md) | 用任务类型查出本次必读资料清单与产出物 |
| 3 | 任务对应的 [`workflows/`](workflows/development.md) 文件 | 按步骤推进，不跳步 |
| 4 | [`.agents/policies/`](policies/boundaries.md) 中受影响的策略 | 确认改动边界、测试与安全要求 |
| 5 | [`.agents/templates/`](templates/task.md) 对应模板 | 用统一格式开工与交付 |

补充规则：

- 加载顺序不可颠倒。`context-map.md` 是"读什么"的唯一索引，不要在未查表的情况下凭记忆找资料。
- 若 `AGENTS.md` 与本目录任何文件冲突，以 `AGENTS.md` 为准，并回报冲突点。
- 任务涉及核算口径（公式、因子、边界、分摊）时，**必须**额外加载 [`.agents/workflows/calculation-change.md`](workflows/calculation-change.md)，无论任务看起来多小。
- 仓库通用贡献约定见 [`CONTRIBUTING.md`](../CONTRIBUTING.md)；技术选型结论只在 [`docs/decisions/README.md`](../docs/decisions/README.md) 下有效，不得在文档中自行断言选型。

## 2. 文件清单与用途

### 2.1 context-map

| 文件 | 用途 |
| --- | --- |
| [`context-map.md`](context-map.md) | 任务类型 → 必读资料 → 产出物 的映射表，覆盖需求文档、核算规则、数据字典、因子库、AI 匹配、前端、数据包、测试、答辩材料、发版 |

### 2.2 workflows（做事流程）

| 文件 | 用途 | 触发场景 |
| --- | --- | --- |
| [`workflows/development.md`](workflows/development.md) | 功能开发流程：需求澄清→设计→契约先行→实现→测试→文档→评审 | 新增功能、新增模块、新增接口 |
| [`workflows/bugfix.md`](workflows/bugfix.md) | 缺陷修复流程：复现→定位→修复→回归→记录 | 结果不符、报错、字段错位、一致性失败 |
| [`workflows/calculation-change.md`](workflows/calculation-change.md) | 核算变更流程：依据→登记→复算→版本与指纹→评审（本项目最敏感流程） | 公式/因子/边界/分摊方法任何改动 |
| [`workflows/review.md`](workflows/review.md) | 审查流程：代码、文档、知识与依据、数据安全四视角检查清单 | 合并前、对外交付前、结题前 |
| [`workflows/release.md`](workflows/release.md) | 发布流程：版本号、CHANGELOG、数据包规范版本、答辩材料冻结 | 打标签、交付数据包、提交结题材料 |
| [`workflows/authoring.md`](workflows/authoring.md) | 文档写作流程：定位与依据→大纲→起草→依据核对→一致性→状态标注→人审 | 撰写产品/需求文档、报告、材料、规范 |

### 2.3 policies（边界与底线）

| 文件 | 用途 |
| --- | --- |
| [`policies/boundaries.md`](policies/boundaries.md) | 可改 / 需 ADR / 禁止改动的目录清单，以及变更分级（T0/T1/T2）与必备动作，防止越界与过度流程 |
| [`policies/testing.md`](policies/testing.md) | unit / integration / acceptance / fixtures 四层职责与确定性核算的回归要求 |
| [`policies/data-security.md`](policies/data-security.md) | 企业 BOM 与工艺数据的敏感数据规则：最小权限、脱敏、本地部署、日志、禁止入库真实数据 |
| [`policies/collaboration.md`](policies/collaboration.md) | 人对 Agent 的指令要求、不确定性处理、并行任务文件分区、冲突处理、交付报告要求 |

### 2.4 templates（统一格式）

| 文件 | 用途 |
| --- | --- |
| [`templates/task.md`](templates/task.md) | 任务说明模板：目标、范围、非目标、输入资料、验收标准、影响目录、测试要求 |
| [`templates/delivery-report.md`](templates/delivery-report.md) | 交付报告模板：变更摘要、涉及文件、验证方式与结果、未决问题、下一步 |

## 3. 三层分离原则（所有工作流共享的约束）

| 层 | 允许产出 | 禁止产出 |
| --- | --- | --- |
| 智能层（AI 副驾驶） | 候选、依据、置信度、缺口与异常提示 | 任何正式核算数值 |
| 核算层（确定性发动机） | 规则约束下的人工确认结果、可回放计算、结果指纹 | 依赖模型"猜测"的参数 |
| 交付层（碳数据包） | 核算结果、活动数据、因子来源与版本、缺口与质量等级、修改记录与字段映射、指纹 | 无来源、无版本、不可复算的数据 |

## 4. 事实与不确定性处理

- 唯一事实来源是本目录与 `docs/`、`knowledge/`、`contracts/` 中已登记的内容；Agent 不得新增未提供的数字、结论、人名或标准条款。
- 不确定处统一写「【待确认】」，并注明需要谁确认（如：指导教师、项目负责人、核算规则负责人）。
- 编程语言/框架、桌面壳 vs Web 工作台等选型【待确认】，以 `docs/decisions/` 下的 ADR 为准。

## 5. 治理层自身的变更控制

`AGENTS.md` 与本目录（`.agents/`）就是规则本身，改动它们属于**敏感变更（T2，见 [`policies/boundaries.md`](policies/boundaries.md) 第 5 节）**。

- 规则的新增、删除或语义修改，必须：① 在 [任务台账](../docs/planning/tasks.md) 登记；② 记入 [CHANGELOG.md](../CHANGELOG.md)；③ 涉及强制力或协作方式的改动（新增检查、改变评审规则等）须先有 ADR。
- 仅措辞、排版、失效链接修正可降为 T0/T1，但仍需记 CHANGELOG。
- 规则冲突仍按第 1 节的裁决顺序处理，不因改动者身份而变。

## 6. 相关入口

- 任务台账：[`docs/planning/tasks.md`](../docs/planning/tasks.md)
- 架构与字段口径：[`docs/architecture/README.md`](../docs/architecture/README.md)
- 产品与需求：[`docs/product/README.md`](../docs/product/README.md)
- 开发指南：[`docs/development/README.md`](../docs/development/README.md)
- 计划与里程碑：[`docs/planning/README.md`](../docs/planning/README.md)
- 知识与登记表：[`knowledge/README.md`](../knowledge/README.md)、[`knowledge/formulas/formula-register.md`](../knowledge/formulas/formula-register.md)、[`knowledge/emission-factors/factor-register.md`](../knowledge/emission-factors/factor-register.md)
- 契约：[`contracts/README.md`](../contracts/README.md)
- 测试基准数据：[`tests/fixtures/README.md`](../tests/fixtures/README.md)
- 示例数据：[`data/examples/README.md`](../data/examples/README.md)
- 工具脚本：[`tools/README.md`](../tools/README.md)
- 环境说明：[`environment/README.md`](../environment/README.md)
