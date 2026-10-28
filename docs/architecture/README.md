# 架构文档

> 状态：首期骨架
> 子目录：架构、模块职责、依赖与数据流

本目录描述链碳台的整体分层、模块边界、依赖方向与数据流。**技术栈尚未决策**，凡未定项均标【待确认】并指向 [设计决策记录](../decisions/README.md)。

## 一、架构原则

| # | 原则 | 含义 |
| --- | --- | --- |
| P1 | **AI 不下场算数** | 智能层只输出候选、依据与置信度；正式数值只能来自确定性核算层 |
| P2 | **确定性优先** | 同一输入 + 同一规则版本 + 同一因子版本 → 同一结果与同一指纹 |
| P3 | **可回放** | 任何一次核算都能用输入快照、规则版本与因子快照重放 |
| P4 | **契约先行** | 模块之间只通过 [contracts/](../../contracts/README.md) 定义的接口与数据结构交互 |
| P5 | **数据可分版本** | 物料、工序、活动数据、因子、审计记录都可版本化与追溯 |
| P6 | **合规内建** | 最小权限、脱敏、访问与操作日志贯穿所有层，而非事后补丁 |
| P7 | **知识可核查** | 公式与因子来自 [knowledge/](../../knowledge/README.md)，代码不得内嵌无来源的数值 |

## 二、四层架构

```text
┌──────────────────────────────────────────────────────────────┐
│ 应用外壳 app/                                                 │
│  启动初始化 · 主窗口/导航 · 工作台视图编排                      │
├──────────────────────────────────────────────────────────────┤
│ 智能层（AI 副驾驶）                                           │
│  物料语义理解 · 工序与因子候选 · 缺口与异常提示 · 自然语言问询   │
│  只输出：候选、依据、置信度  →  绝不产生正式核算数值             │
├──────────────────────────────────────────────────────────────┤
│ 数据层（可版本化）                                            │
│  Product · BOMItem · Process · ActivityData · EmissionFactor  │
│  Mapping · CalculationRun · DataPackage · 审计记录             │
├──────────────────────────────────────────────────────────────┤
│ 核算层（可回放）                                              │
│  规则约束 → 人工确认 → 确定性计算 → 版本与结果指纹             │
│  边界 · 单位 · 规则 · 分摊 · 指纹                              │
├──────────────────────────────────────────────────────────────┤
│ 合规内建（纵向贯穿）                                          │
│  最小权限 · 脱敏 · 访问与操作日志 · 本地部署选项                │
└──────────────────────────────────────────────────────────────┘
```

## 三、模块职责

| 模块 | 目录 | 职责一句话 |
| --- | --- | --- |
| 项目 | [modules/project](../../modules/project/README.md) | 项目、产品、核算任务与边界定义 |
| 制造 | [modules/manufacturing](../../modules/manufacturing/README.md) | PCBA-SMT 工序链、设备与生产信息 |
| 数据字典 | [modules/data_dictionary](../../modules/data_dictionary/README.md) | 字段、单位与口径的注册与映射 |
| 活动数据 | [modules/activity_data](../../modules/activity_data/README.md) | 活动数据录入、导入、校验与质量等级 |
| 排放因子 | [modules/emission_factors](../../modules/emission_factors/README.md) | 运行时因子入库、四重校验与快照 |
| 核算 | [modules/calculation](../../modules/calculation/README.md) | 确定性核算、分摊切换、指纹与回放 |
| 数据审核 | [modules/data_review](../../modules/data_review/README.md) | AI 候选呈现、人工确认与留痕 |
| 分析 | [modules/analysis](../../modules/analysis/README.md) | 结果构成、对比与敏感性分析 |
| 数据包 | [modules/data_package](../../modules/data_package/README.md) | 数据包生成、解析与版本兼容 |

## 四、依赖方向

```text
app/  ──►  modules/*  ──►  contracts/  ◄──  modules/* 之间只经契约交互
                            │
                            ├─►  knowledge/（公式与因子的依据，只读）
                            └─►  data/（示例与模板，只读样例）
```

- 依赖方向**单向**：上层可依赖下层，下层不得反向依赖上层。
- `knowledge/` 是**依据库**（人可读的公式、因子来源、文献），`modules/emission_factors` 与 `modules/calculation` 是**运行时实现**；实现不得偏离依据，偏差必须走 [核算变更流程](../../.agents/workflows/calculation-change.md)。
- 模块之间禁止直连内部数据结构；跨模块访问一律经 `contracts/`。

## 五、核心实体与数据流

| 实体 | 关键字段 | 角色 |
| --- | --- | --- |
| `Product` | 产品编码、规格、核算边界与单位 | 定义核算对象与边界 |
| `BOMItem` | 料号、描述、封装、数量、单位 | 统一物料口径 |
| `Process` | 工序 ID、名称、设备 | 把工序链结构化 |
| `ActivityData` | 活动量、单位、期间、来源、质量等级 | 让数据可追溯、可分级 |
| `EmissionFactor` | 因子值、单位、区域、来源、版本 | 让因子可复核 |
| `Mapping` | 候选、评分、依据、人工确认 | AI 与人工的交接面 |
| `CalculationRun` | 输入快照、规则版本、结果、指纹 | 支撑复算与审计 |
| `DataPackage` | 结果、证据、缺口、字段映射 | 面向交付与复用 |

```text
BOM 导入 ──► BOMItem ──┐
                       ├─► Mapping（AI 候选 + 人工确认）──► 口径统一
工序建模 ──► Process ──┘
                       │
活动数据 ──► ActivityData ──┐
                            ├─► CalculationRun（规则+因子+分摊）──► 结果 + 指纹
因子库 ──► EmissionFactor ──┘                                        │
                                                                     ▼
                                                              DataPackage（交付）
```

字段级定义与稳定性约定见 [contracts/README.md](../../contracts/README.md)。

## 六、风险与控制（架构级）

| 风险 | 控制机制 | 留下的证据 |
| --- | --- | --- |
| AI 幻觉 | 检索增强 + 规则约束 + 人工确认 | 模型版本、候选列表、确认记录 |
| 因子选错 | 来源、单位、区域、版本四重校验 | 因子快照 |
| 数据异常 | 范围规则 + 统计异常检测 | 异常记录与处理说明 |
| BOM 敏感 | 最小权限、脱敏、本地部署选项 | 访问与操作日志 |
| 结果不可复现 | 输入快照 + 规则版本 + 确定性计算 | 结果指纹与回放记录 |

## 七、待确认项

- 【待确认】数据包交换格式与是否对齐客户模板（影响 `data_package` 契约）；负责人：数据包负责人；确认人：待确认。
- 技术栈、`app/` 形态、部署并发与模型调用方式已由 [ADR 0003](../decisions/0003-local-web-workbench-baseline.md) 确定：Web 客户端、Vue 3 + TypeScript / FastAPI / PostgreSQL、内网多用户、开发期云端 + 真实数据本地。
