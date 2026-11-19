# 交付报告：T-0015 导入模板设计

> 状态：已完成

## 1. 基本信息

| 项 | 内容 |
|---|---|
| 任务 ID | T-0015 |
| 任务名称 | 导入模板设计 |
| 执行人 | R2 知识库维护 |
| 确认人 | 袁青扬（@Yuanqingyuang） |
| 执行日期 | 2026-11-20 |
| 交付日期 | 2026-11-20 |

## 2. 交付摘要

基于 T-0011 数据字典、T-0008 案例产品基线，设计 4 个 Excel 导入模板，含字段名、中文名、单位（UNIT-xxx）、必填、示例值、校验规则、下拉选项、AI 映射辅助列。

**核心产出：**
- data/templates/bom_import_template.xlsx
- data/templates/process_import_template.xlsx
- data/templates/activity_data_template.xlsx
- data/templates/ef_matching_template.xlsx

## 3. 验收标准执行结果

| # | 验收项 | 结果 | 证据 |
|---|---|---|---|
| 1 | 4 个模板文件存在 | ✅ | 4 个 .xlsx 文件已创建 |
| 2 | 每模板含字段名、中文名、单位、必填、示例、校验、下拉 | ✅ | 逐表检查 Sheet1 模板行 + Sheet2 说明 |
| 3 | 单位引用 UNIT-xxx，术语引用 TERM-xxx | ✅ | 单位列全填 UNIT ID，备注引用 TERM |
| 4 | 含 AI 映射辅助列 | ✅ | BOM 模板含 ai_field_mapping、ai_factor_candidate 列 |

## 4. 模板清单

| 模板文件 | 基于实体 | 行数（含表头） | 关键特性 |
|---|---|---|---|
| bom_import_template.xlsx | BOMItem | 21 字段 | 含 ai_field_mapping、ai_factor_candidate 列、物料类别下拉 |
| process_import_template.xlsx | Process | 14 字段 | 含 allocation_method_id 下拉 F-AL-xxx |
| activity_data_template.xlsx | ActivityData | 18 字段 | 单位引用 UNIT-xxx、质量等级下拉 P1/P2/P3 |
| ef_matching_template.xlsx | EmissionFactor | 16 字段 | 含 ai_factor_candidate 列、来源等级下拉 P1/P2/P3 |

## 4. 变更文件清单

| 文件 | 变更类型 | 主要变更 |
|---|---|---|
| data/templates/bom_import_template.xlsx | 新增 | BOM 导入模板 |
| data/templates/process_import_template.xlsx | 新增 | 工序路线导入模板 |
| data/templates/activity_data_template.xlsx | 新增 | 活动数据录入模板 |
| data/templates/ef_matching_template.xlsx | 新增 | 因子匹配模板 |

## 5. 后续动作

1. 等待确认人签注（任务台账确认列）
2. T-0016 企业数据采集时使用模板收集
3. T-0020 导入解析代码按模板格式实现

## 6. 签注

| 角色 | 人员 | 签注 | 日期 |
|---|---|---|---|
| 执行人 | R2 知识库维护 | 已完成 | 2026-11-20 |
| 确认人 | 袁青扬（@Yuanqingyuang） | 待签注 | — |
