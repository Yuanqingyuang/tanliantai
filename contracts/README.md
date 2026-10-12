# contracts/ — 跨模块接口与数据契约

> 状态：规划中（首期骨架）

本目录是模块间协作的**唯一合法通道**。任何跨模块的数据结构与接口，都必须先在此登记，再落到实现（R5：契约先行）。

## 一、契约清单

| 实体 | 提供方模块 | 消费方模块 | 关键字段 | 单位与口径 | 版本 | 稳定性 |
| --- | --- | --- | --- | --- | --- | --- |
| Product | `modules/project/` | `calculation`、`data_package`、`analysis` | 产品编码、规格、核算边界与单位 | 口径以边界声明为准，必须显式 | 【待确认】 | 稳定 |
| BOMItem | `modules/manufacturing/`【待确认：BOM 归属模块，或将由独立 BOM 模块提供】 | `data_review`、`calculation` | 料号、描述、封装、数量、单位 | 数量与单位须在字典注册 | 【待确认】 | 稳定 |
| Process | `modules/manufacturing/` | `activity_data`、`calculation`、`data_package` | 工序 ID、名称、设备 | 口径依据 `knowledge/domain/pcba-smt-processes.md` | 【待确认】 | 稳定 |
| ActivityData | `modules/activity_data/` | `calculation`、`analysis`、`data_package` | 活动量、单位、期间、来源、质量等级 | 活动量与单位成对，期间不可重叠 | 【待确认】 | 稳定 |
| EmissionFactor | `modules/emission_factors/` | `data_review`、`calculation`、`data_package` | 因子值、单位、区域、来源、版本 | 单位/区域/来源/版本四重校验，缺一不可用 | 【待确认】 | 稳定 |
| Mapping | `modules/data_review/` | `calculation`、`data_package` | 候选、评分、依据、人工确认 | 未确认不得进入核算 | 【待确认】 | 稳定 |
| CalculationRun | `modules/calculation/` | `analysis`、`data_package` | 输入快照、规则版本、结果、指纹 | 同一输入 → 同一结果；版本必须随结果记录 | 【待确认】 | 稳定 |
| DataPackage | `modules/data_package/` | 第三方工具、评审方 | 结果、证据、缺口、字段映射 | 字段完整率与可复算率为验收口径 | 【待确认】 | 稳定 |

说明：

- "版本"列的取值待 ADR 确认；在未定之前，跨模块引用一律以【待确认】标记，不得假定具体版本号。
- 稳定性含义：稳定 = 允许新增可选字段，不允许无迁移地改动已有字段语义。
- 每个实体的字段语义与单位定义以 `modules/data_dictionary/` 为单一事实来源。

## 二、契约变更规则

| 变更类型 | 判定 | 要求 |
| --- | --- | --- |
| 破坏性变更 | 删除/重命名字段、改类型、改单位、改语义、收紧必填 | ADR + 主版本号递增 + 迁移说明 + 消费方改造清单 |
| 兼容性变更 | 新增可选字段、新增枚举值（消费方须容忍未知值） | 次版本号递增 + 变更说明 |
| 文档性变更 | 注释、示例、措辞 | 补丁版本号 + 记录 |

流程要求：

1. 先改本文件与 `docs/decisions/` 的 ADR，再改实现（R5）。
2. 单位或口径变更同时更新 `knowledge/formulas/formula-register.md` 或 `knowledge/emission-factors/factor-register.md`（R3、R6）。
3. 变更须说明对历史 CalculationRun 的影响（能否复算、是否需要重算）。
4. 涉及数据包字段的变更必须评估版本兼容与迁移路径。

## 三、命名与单位约定

| 约定项 | 规则 |
| --- | --- |
| 字段名 | 英文；同一概念在全部实体中同名，禁止同义异名 |
| 实体名 | 英文单数、首字母大写（如 `ActivityData`） |
| 标识符 | 稳定、唯一、不随显示名变化（工序 ID、产品编码） |
| 数值字段 | 必须成对携带单位；严禁无单位裸数值 |
| 期间 | 显式起止，禁止用"本月"等相对表述存储 |
| 版本 | 每个可引用对象具备版本标识；参考系（字典/规则/因子）版本必须随结果保存 |
| 时间 | 统一存储口径【待确认：时区与格式】 |
| 空缺 | 用显式空值表示，禁止用 0 代替"未采集" |

## 四、禁止事项

- 模块间**不得绕过契约直连内部数据结构**（直读他人表、共享可变全局状态、依赖未登记字段）。
- 不得以"临时字段"为名在契约外传递数据；需要就登记，不需要就删除。
- 不得在消费方复制提供方的业务规则（避免双份真相）。
- 不得让 AI 组件成为契约的提供方；AI 输出只能作为候选数据经人工确认后进入 Mapping。
- 不得在契约中承载核算公式；公式依据只在 `knowledge/formulas/formula-register.md`。
- 不得写入真实企业数据作为示例（R4：数据不出门），示例见 `data/examples/README.md`。

## 相关文档

`docs/architecture/README.md`、`docs/development/README.md`、`docs/decisions/README.md`、`tests/fixtures/README.md`、`tools/README.md`、`knowledge/README.md`。
