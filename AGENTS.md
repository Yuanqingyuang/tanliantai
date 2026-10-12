# AGENTS.md — Agent 全局规则与上下文加载入口

> 状态：首期骨架
> 适用范围：本仓库内所有 AI Agent（含人机协作、自动化脚本与 CI 触发的 Agent）

本文件是 Agent 进入本仓库的**唯一入口**。任何任务开始前，先读本文件，再按 [.agents/context-map.md](.agents/context-map.md) 加载该任务所需的资料，最后按 [.agents/workflows](.agents/workflows/development.md) 中对应流程执行。

## 一、加载顺序（不可跳过）

1. 本文件 `AGENTS.md`（全局规则）
2. [.agents/context-map.md](.agents/context-map.md)（任务 → 必读资料映射）
3. `.agents/workflows/` 下与本任务对应的流程文件
4. `.agents/policies/` 下与本次改动相关的规则文件
5. 任务涉及领域时：`knowledge/` 下的术语、公式、因子与文献依据
6. 任务涉及代码时：`contracts/` 与 `docs/architecture/`

## 二、项目上下文速览

- 项目：**链碳台（CHAINPCF）**，AI 辅助的 PCBA-SMT 工序级碳数据字典、核算工具与数据包。
- 目标：让中小电子制造企业以最低门槛，产出可复核、可交付的**产品碳足迹**数据（口径依据 GB/T 24067-2024）。
- 产品三层：AI 副驾驶（只给候选与依据）+ 确定性核算发动机（同一输入 → 同一结果）+ 结构化碳数据包交付物。
- 核心实体：`Product`、`BOMItem`、`Process`、`ActivityData`、`EmissionFactor`、`Mapping`、`CalculationRun`、`DataPackage`。
- 当前状态：文档与结构阶段，**尚无代码**；技术栈、数据包格式、`app/` 形态（桌面外壳 vs Web 工作台）均【待确认】，以 `docs/decisions/` 的 ADR 为准。

## 三、硬性规则（违反即回退）

| # | 规则 | 说明 |
| --- | --- | --- |
| R1 | **不造数** | 不得编造排放因子数值、标准条款细节、市场规模数字、文献页码。不确定就写「【待确认】」并写清需要谁确认或查哪份标准 |
| R2 | **AI 不下场算数** | AI 只输出候选、依据与置信度；正式核算数值只能由确定性核算引擎依据已登记的规则与因子计算 |
| R3 | **无依据不改核算** | 公式、因子、系统边界、分摊方法的任何改动都必须有标准/文献/实测依据，并同步更新 `knowledge/formulas/formula-register.md`、`knowledge/emission-factors/factor-register.md` 与变更记录 |
| R4 | **数据不出门** | 企业真实 BOM 与工艺数据属敏感数据：不得提交进 Git、不得写入示例、不得在报告中出现可识别信息；示例数据必须脱敏 |
| R5 | **契约先行** | 跨模块接口与数据结构变更，先改 `contracts/`，再改实现；破坏性变更需 ADR + 版本号 + 迁移说明 |
| R6 | **文档与代码同步** | 改行为就要改文档；同一提交内完成，不允许"稍后补文档" |
| R7 | **不越界修改** | 只改任务范围内的文件；不确定边界时先看 [.agents/policies/boundaries.md](.agents/policies/boundaries.md)，仍不确定就问，不要猜 |
| R8 | **可验证** | 每次交付都要说明"怎么验证的、结果如何"；无法验证时明确写出缺口 |
| R9 | **留痕** | 关键决策、AI 候选与人工确认过程都要可追溯；核算结果必须带版本与指纹信息 |

## 四、任务执行约定

- 开工前：把任务拆成可验证的步骤，明确**目标 / 范围 / 非目标 / 验收标准 / 影响目录**（模板见 [.agents/templates/task.md](.agents/templates/task.md)）。
- 执行中：小步提交；同一时间只改自己负责的文件范围；需要与他人并行时先划分文件范围（见 [.agents/policies/collaboration.md](.agents/policies/collaboration.md)）。
- 收尾时：按 [.agents/templates/delivery-report.md](.agents/templates/delivery-report.md) 输出交付报告；在 `CHANGELOG.md` 记录用户可见的变化。

## 五、常见任务入口

| 任务 | 入口 |
| --- | --- |
| 开发新功能 | [.agents/workflows/development.md](.agents/workflows/development.md) |
| 修缺陷 | [.agents/workflows/bugfix.md](.agents/workflows/bugfix.md) |
| 改核算规则 / 公式 / 因子 / 分摊 | [.agents/workflows/calculation-change.md](.agents/workflows/calculation-change.md) |
| 代码或文档评审 | [.agents/workflows/review.md](.agents/workflows/review.md) |
| 发版 / 结题材料冻结 | [.agents/workflows/release.md](.agents/workflows/release.md) |
| 查"该读哪些资料" | [.agents/context-map.md](.agents/context-map.md) |
| 人怎么和 Agent 协作 | [CONTRIBUTING.md](CONTRIBUTING.md) |

## 六、禁止事项

- 禁止在未读对应 workflow 的情况下改动 `knowledge/`、`contracts/`、`tests/fixtures/` 下的内容。
- 禁止把 `tools/`、`environment/scripts/` 的自检脚本当作"可选"——结构与环境自检必须通过或明确记录例外。
- 禁止使用真实企业数据做示例、截图或答辩演示（含截图中的料号、客户名、价格）。
- 禁止在文档中承诺未经验证的指标结论（如"可以降低 80% 成本"）。
