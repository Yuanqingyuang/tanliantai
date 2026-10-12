# 导入模板（data/templates）

> 状态：首期骨架

本目录存放**导入模板**：企业用户与内部测试据其准备数据，工具按同一套规则解析与校验。
模板是数据进入系统的唯一入口，字段与校验规则必须与数据字典一致；
**当前字段为骨架设计，最终以数据字典 V0.1 为准**（相关条目标【待确认】）。

## 一、模板清单

| 模板 | 目标实体 | 用途 | 导入模块 | 状态 |
| --- | --- | --- | --- | --- |
| 活动数据导入模板 | `ActivityData` | 录入工序的活动数据（用量、期间、来源） | `modules/activity_data` | 规划中 |
| BOM 导入模板 | `BOMItem`、`Product` | 建立产品结构：物料、用量、关联工序 | `modules/manufacturing` | 规划中 |
| 因子导入模板 | `EmissionFactor` | 登记排放因子及其依据与适用边界 | `modules/emission_factors` | **【待确认】**是否开放给用户导入 |

模板文件命名：`<模板名>_v<主版本>.<次版本>.csv`（例：`activity_data_v0.1.csv`）；
编码 UTF-8 无 BOM，换行 LF，首行为字段名，不含合并单元格与批注。

## 二、BOM 导入模板字段

| 字段名 | 含义 | 单位 | 是否必填 | 校验规则 |
| --- | --- | --- | --- | --- |
| `product_code` | 产品编码 | — | 必填 | 非空、同表内唯一标识产品 |
| `product_name` | 产品名称 | — | 必填 | 非空 |
| `functional_unit` | 功能单位 | 见单位字典 | 必填 | 取值属于单位字典【待确认】 |
| `item_code` | 物料编码 | — | 必填 | 非空；同产品内不得重复 |
| `item_name` | 物料名称 | — | 必填 | 非空 |
| `quantity` | 单位产品用量 | 件 / 克 / 千克 / 米 / 平方米 | 必填 | 数值 > 0 |
| `unit` | 用量单位 | 同上 | 必填 | 属于单位字典【待确认】 |
| `process_code` | 关联工序编码 | — | 必填 | 必须能在工序表中找到；找不到须进入人工映射 |

## 三、活动数据导入模板字段

| 字段名 | 含义 | 单位 | 是否必填 | 校验规则 |
| --- | --- | --- | --- | --- |
| `activity_code` | 活动数据编码 | — | 必填 | 非空、同批次唯一（防重复计量） |
| `process_code` | 所属工序 | — | 必填 | 必须存在对应 `Process` |
| `product_code` | 归属产品 | — | 必填 | 必须存在对应 `Product` |
| `activity_name` | 活动数据名称 | — | 必填 | 非空 |
| `amount` | 数量 | 按类型定（kWh / kg / m³ 等） | 必填 | 数值 ≥ 0；单位须与因子单位可换算 |
| `unit` | 数量单位 | 同上 | 必填 | 属于单位字典【待确认】 |
| `period_start` | 统计期间起 | 日期 | 必填 | 合法日期；不晚于 `period_end` |
| `period_end` | 统计期间止 | 日期 | 必填 | 合法日期；覆盖核算所属期间 |
| `source` | 数据来源 | — | 必填 | 枚举或简短说明（如电表、台账、估算）【待确认】 |

## 四、因子导入模板字段

| 字段名 | 含义 | 单位 | 是否必填 | 校验规则 |
| --- | --- | --- | --- | --- |
| `factor_code` | 因子编码 | — | 必填 | 非空、全局唯一 |
| `factor_name` | 因子名称 | — | 必填 | 非空 |
| `value` | 因子数值 | kgCO2e / 单位活动数据 | 必填 | 数值 ≥ 0 |
| `unit` | 因子单位 | 同上 | 必填 | 必须与活动数据单位可换算 |
| `scope` | 适用边界 / 范围 | — | 必填 | 与系统边界定义一致 |
| `source_reference` | 依据出处 | — | 必填 | 指向标准条款或文献；缺失即拒绝导入 |
| `valid_from` | 生效起始 | 日期 | 必填 | 合法日期 |
| `version` | 因子版本 | — | 必填 | 变更必须升版本，旧版本保留 |

## 五、版本与变更规则

1. 模板与数据字典**联动升版**：字段增删改必须先改 `modules/data_dictionary`，再改模板。
2. 破坏性变更（删字段、改含义、改单位）须走 ADR，见 [../../docs/decisions/README.md](../../docs/decisions/README.md)。
3. 旧模板在过渡期内必须仍可解析，或在导入时**明确报错**并提示迁移方式，不得静默丢弃字段。
4. 每次模板变更须在案例与文档中记录：模板版本、生效范围、迁移说明。

## 六、与模块的对应关系

| 模块 | 关系 |
| --- | --- |
| [../../modules/activity_data/README.md](../../modules/activity_data/README.md) | 活动数据导入模板的解析、校验与落库由该模块负责 |
| `modules/data_dictionary` | 字段名、单位、枚举与校验规则的**唯一来源** |
| `modules/emission_factors` | 因子导入模板的校验与版本管理 |
| `modules/manufacturing` | BOM 导入模板的解析与工序映射 |
| [../../contracts/README.md](../../contracts/README.md) | 导入结果的跨模块数据结构以此为准 |

## 七、相关文档

- 公开示例数据：[../examples/README.md](../examples/README.md)
- 基准数据规范：[../../tests/fixtures/README.md](../../tests/fixtures/README.md)
- 工程工具：[../../tools/README.md](../../tools/README.md)
- 环境与模板编码约定：[../../environment/README.md](../../environment/README.md)
