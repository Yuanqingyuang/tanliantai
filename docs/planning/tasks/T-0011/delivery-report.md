# 交付报告：T-0011 数据字典 V0.1

> 状态：基线确定 v1.0

## 1. 基本信息

| 项 | 内容 |
|---|---|
| 任务 ID | T-0011 |
| 任务名称 | 数据字典 V0.1 |
| 执行人 | R2 知识库维护 |
| 确认人 | 袁青扬（@Yuanqingyuang） |
| 执行日期 | 2026-11-20 |
| 交付日期 | 2026-11-20 |

## 2. 交付摘要

基于 T-0008 案例产品基线，定义 7 个核心实体、30+ 字段、7 类枚举、7 条校验规则，全引用 TERM/UNIT/F- 标准 ID。

**核心产出：**
- contracts/data-dictionary.md：Product、BOMItem、Process、ActivityData、EmissionFactor、CalculationRun、DataPackage 7 实体

## 3. 验收标准执行结果

| # | 验收项 | 结果 | 证据 |
|---|---|---|---|
| 1 | 7 个核心实体字段定义完整 | ✅ | Product、BOMItem、Process、ActivityData、EmissionFactor、CalculationRun、DataPackage |
| 2 | 所有字段有单位、TERM 引用、质量等级 | ✅ | 30+ 字段全覆盖 UNIT-xxx、TERM-xxx、质量等级 |
| 3 | 枚举值定义完整 | ✅ | 7 类枚举：物料类别(9)、质量等级(3)、因子来源(3)、边界(2)、阶段(5)、表面处理(4)、运行类型(4) |
| 4 | 版本管理字段齐全 | ✅ | 每实体含 version、created_at、updated_at |
| 5 | 校验规则 7 条 | ✅ | VR-001~007 覆盖单位一致性、必填、外键、版本、指纹、质量等级 |

## 4. 交叉引用一致性

| 引用基线 | 覆盖情况 |
|---|---|
| TERM-xxx | 44 个术语全覆盖，实体表 TERM 引用列全填 |
| UNIT-xxx | 20 个单位全覆盖，字段单位列全填 UNIT ID |
| F-<域>-<三位> | 15 个公式全覆盖，Process.allocation_method_id 引用 F-AL-xxx |
| T-0008 基线 | BOM 模板字段、Process 工序 ID、分摊方法 ID 全对齐 |

## 4. 变更文件清单

| 文件 | 变更类型 | 主要变更 |
|---|---|---|
| contracts/data-dictionary.md | 新增 | 7 实体、30+ 字段、7 类枚举、7 条校验规则 |

## 5. 后续动作

1. 等待确认人签注（任务台账确认列）
2. T-0012 契约 V0.1 基于此字典编制
3. T-0015 导入模板基于 BOMItem、Process 字典制作
4. T-0022 核算引擎按校验规则实现

## 6. 签注

| 角色 | 人员 | 签注 | 日期 |
|---|---|---|---|
| 执行人 | R2 知识库维护 | 基线确定 v1.0 | 2026-11-20 |
| 确认人 | 袁青扬（@Yuanqingyuang） | 待签注 | — |
