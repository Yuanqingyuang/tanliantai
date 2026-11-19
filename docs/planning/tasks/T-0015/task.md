# 任务说明：T-0015 导入模板设计

> 状态：已完成

## 1. 基本信息

| 项 | 内容 |
|---|---|
| 任务名称 | 导入模板设计（基于 T-0011 数据字典、T-0008 案例产品基线） |
| 任务类型 | 数据 / 模板 |
| 提出人 | 项目团队 |
| 执行人 / Agent | R2 知识库维护 |
| 确认人 | 袁青扬（@Yuanqingyuang） |
| 关联里程碑 | 2026.10—11 需求与标准 |
| 是否触及核算口径 | 否（模板层面） |

## 2. 目标

- 基于 T-0011 数据字典（BOMItem、Process）设计 Excel/CSV 导入模板
- 模板含：字段名、中文名、单位（UNIT-xxx）、必填、示例值、校验规则、下拉选项
- 支持 AI 候选映射列（字段映射、因子匹配）
- 供 T-0016 数据采集、T-0020 导入与人工审核闭环使用

## 3. 范围

- 本次要做：
  - BOM 导入模板：基于 BOMItem 实体，含 AI 映射辅助列
  - 工序路线导入模板：基于 Process 实体
  - 活动数据录入模板：基于 ActivityData 实体
  - 因子匹配模板：基于 EmissionFactor 实体，含 AI 候选列
- 本次明确不做：
  - 不实现导入解析代码（属 T-0020）
  - 不采集真实数据（属 T-0016）

## 4. 非目标

- 不编写业务代码
- 不实现核算引擎

## 5. 输入资料

| 资料 | 路径或来源 | 是否已存在 |
|---|---|---|
| T-0011 数据字典 | contracts/data-dictionary.md | 是 |
| T-0008 案例产品基线 | docs/product/case-product-baseline.md | 是 |
| T-0004 术语/单位 | knowledge/domain/TERM-001-glossary.md 等 | 是 |

## 6. 验收标准

| # | 判定条件（可观测） | 验证方式 |
|---|---|---|
| 1 | 4 个模板文件存在（.xlsx/.csv） | 文件存在性检查 |
| 2 | 每模板含：字段名、中文名、单位、必填、示例、校验、下拉 | 逐表检查 |
| 3 | 单位引用 UNIT-xxx，术语引用 TERM-xxx | 逐列核对 |
| 4 | 含 AI 映射辅助列（字段映射、因子候选） | 列存在性检查 |
| 5 | 自动化校验通过 | check_repo_structure.py / check_links.py |

## 7. 影响目录

| 目录/文件 | 变更性质 | 是否受控 |
|---|---|---|
| data/templates/bom_import_template.xlsx | 新增 | 是（T1） |
| data/templates/process_import_template.xlsx | 新增 | 是（T1） |
| data/templates/activity_data_template.xlsx | 新增 | 是（T1） |
| data/templates/ef_matching_template.xlsx | 新增 | 是（T1） |
| docs/planning/tasks.md | 更新台账 | 否 |

## 7. 影响目录

| 目录/文件 | 变更性质 | 是否受控 |
|---|---|---|
| data/templates/bom_import_template.xlsx | 新增 | 是（T1） |
| data/templates/process_import_template.xlsx | 新增 | 是（T1） |
| data/templates/activity_data_template.xlsx | 新增 | 是（T1） |
| data/templates/ef_matching_template.xlsx | 新增 | 是（T1） |
| docs/planning/tasks.md | 更新台账 | 否 |

## 8. 测试要求

| 层级 | 要求 |
|---|---|
| unit | 不适用 |
| integration | 不适用 |
| acceptance | 自动化校验全通过 |
| fixtures | 不新增 |

## 9. 数据与安全

- [x] 本次是否接触企业真实数据：否
- [x] 交付物中不含可识别企业信息

## 10. 交付物

| 交付物 | 形式 | 归档位置 |
|---|---|---|
| 任务说明 | Markdown | 本文件 |
| 交付报告 | Markdown | [delivery-report.md](delivery-report.md) |
| BOM 导入模板 | Excel | data/templates/bom_import_template.xlsx |
| 工序路线导入模板 | Excel | data/templates/process_import_template.xlsx |
| 活动数据录入模板 | Excel | data/templates/activity_data_template.xlsx |
| 因子匹配模板 | Excel | data/templates/ef_matching_template.xlsx |

## 11. 未决事项

| # | 问题 | 需要谁确认 | 阻塞程度 |
|---|---|---|---|
| 1 | 企业特有字段扩展 | T-0016 企业数据采集后 | 不阻塞 V0.1 |
