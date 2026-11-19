# 任务说明：T-0011 数据字典 V0.1

> 状态：已完成

## 1. 基本信息

| 项 | 内容 |
|---|---|
| 任务名称 | 数据字典 V0.1（基于 T-0008 案例产品基线） |
| 任务类型 | 数据字典 / 契约 |
| 提出人 | 项目团队 |
| 执行人 / Agent | R2 知识库维护 |
| 确认人 | 袁青扬（@Yuanqingyuang） |
| 关联里程碑 | 2026.10—11 需求与标准 |
| 是否触及核算口径 | 是（字段定义直接影响数据采集与核算正确性） |

## 2. 目标

- 基于 T-0008 案例产品基线（BOM 模板、工序路线、分摊策略）定义核心实体字段
- 字段含义、单位（UNIT-xxx）、质量等级、必填性、校验规则完整覆盖
- 与 T-0004 术语/单位/公式、T-0005 工序链、T-0007 验收指标保持一致
- 供 T-0012 契约、T-0015 导入模板、T-0022 核算引擎直接使用

## 3. 范围

- 本次要做：
  - 核心实体：Product、BOMItem、Process、ActivityData、EmissionFactor、CalculationRun、DataPackage
  - 每实体：字段名、中文名、类型、单位（UNIT-xxx）、必填、质量等级、校验规则、TERM 引用
  - 枚举值定义：物料类别、工序 ID、质量等级、因子来源等级、边界类型
  - 版本管理：字典版本、实体版本、字段版本
- 本次明确不做：
  - 不生成 SQL DDL（属 T-0022 实现）
  - 不做数据库迁移脚本（属 T-0019 技术集成）

## 4. 非目标

- 不编写业务代码
- 不实现核算引擎

## 5. 输入资料

| 资料 | 路径或来源 | 是否已存在 |
|---|---|---|
| T-0008 案例产品基线 | docs/product/case-product-baseline.md | 是 |
| T-0004 术语/单位/公式 | knowledge/domain/TERM-001-glossary.md 等 | 是 |
| T-0005 PCBA-SMT 工序链 | knowledge/domain/pcba-smt-processes.md | 是 |
| T-0007 验收指标 | tests/acceptance/acceptance-criteria.md | 是 |

## 6. 验收标准

| # | 判定条件（可观测） | 验证方式 |
|---|---|---|
| 1 | 7 个核心实体字段定义完整 | 逐实体检查字段表 |
| 2 | 所有字段有单位（UNIT-xxx）、TERM 引用、质量等级 | 逐字段核对 |
| 3 | 枚举值定义完整（物料类别、工序 ID、质量等级等） | 枚举表检查 |
| 4 | 版本管理字段齐全 | 版本字段检查 |
| 5 | 自动化校验通过 | check_repo_structure.py / check_links.py |

## 7. 影响目录

| 目录/文件 | 变更性质 | 是否受控 |
|---|---|---|
| contracts/data-dictionary.md | 新增 | 是（T1） |
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
| 数据字典 V0.1 | Markdown | contracts/data-dictionary.md |

## 11. 未决事项

| # | 问题 | 需要谁确认 | 阻塞程度 |
|---|---|---|---|
| 1 | 真实企业扩展字段需求 | T-0016 企业数据采集后 | 不阻塞 V0.1 |
