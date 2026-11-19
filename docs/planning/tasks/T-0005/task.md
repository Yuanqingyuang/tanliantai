# 任务说明：T-0005 PCBA-SMT 工序链与设备清单

> 状态：已完成

## 1. 基本信息

| 项 | 内容 |
|---|---|
| 任务名称 | PCBA-SMT 工序链与设备清单（对齐新规范 TERM/UNIT/F-<域> ID） |
| 任务类型 | 知识库 / 调研 |
| 提出人 | 项目团队 |
| 执行人 / Agent | R2 知识库维护 |
| 确认人 | 袁青扬（@Yuanqingyuang） |
| 关联里程碑 | 2026.10—11 需求与标准 |
| 是否触及核算口径 | 是 |

## 2. 目标

- 将现有 pcba-smt-processes.md 升级到新 ID 规范
- 引用 TERM-xxx、UNIT-xxx、F-<域>-<三位序号> 标准 ID
- 补齐分摊方法 F-AL-001~004 与单位 UNIT-xxx 映射
- 建立映射表，便于后续数据字典与核算引擎开发使用

## 3. 范围

- 本次要做：
  - 12 道工序表：补充 UNIT ID、F-AL 方法 ID、TERM 引用
  - 公用工程表：标注分摊方法 F-AL ID、关联单位 UNIT ID
  - 边界建议：引用 TERM-004-BAS 系统边界
  - 新增第 5 节：与新规范的映射表（26 项）
- 本次明确不做：
  - 不采集企业真实设备参数（属 T-0016）
  - 不决定具体产品工艺路线（属 T-0008）

## 4. 非目标

- 不编写业务代码
- 不实现核算引擎

## 5. 输入资料

| 资料 | 路径或来源 | 是否已存在 |
|---|---|---|
| 旧版工序清单 | knowledge/domain/pcba-smt-processes.md | 是 |
| 术语表 | knowledge/domain/TERM-001-glossary.md | 是 |
| 单位表 | knowledge/domain/UNIT-001-units.md | 是 |
| 公式登记 | knowledge/formulas/formula-register.md | 是 |
| 分摊方法 | knowledge/formulas/allocation-methods.md | 是

## 6. 验收标准

| # | 判定条件（可观测） | 验证方式 |
|---|---|---|
| 1 | 12 道工序表每行均有 UNIT ID、F-AL ID、TERM 引用 | 逐行检查表格第 4、6 列 |
| 2 | 公用工程表标注 F-AL 方法 ID 与 UNIT ID | 检查第 3 表第 4、5 列 |
| 3 | 边界建议引用 TERM-004-BAS | 检查第 4 节第 1 条 |
| 4 | 映射表覆盖 TERM/UNIT/F- 核心 ID | 检查第 5 表 26 行 |
| 5 | 自动化校验通过 | check_repo_structure.py / check_governance.py / check_links.py |

## 7. 影响目录

| 目录/文件 | 变更性质 | 是否受控 |
|---|---|---|
| knowledge/domain/pcba-smt-processes.md | 重写 / 对齐 | 是（T1） |
| docs/planning/tasks.md | 更新台账 | 否 |

## 8. 测试要求

| 层级 | 要求 |
|---|---|
| unit | 不适用 |
| integration | 不适用 |
| acceptance | 自动化校验全通过 |
| fixtures | 不新增

## 9. 数据与安全

- [x] 本次是否接触企业真实数据：否
- [x] 交付物中不含可识别企业信息

## 10. 交付物

| 交付物 | 形式 | 归档位置 |
|---|---|---|
| 任务说明 | Markdown | 本文件 |
| 交付报告 | Markdown | [delivery-report.md](delivery-report.md) |
| 工序链文档 | Markdown | knowledge/domain/pcba-smt-processes.md |

## 11. 未决事项

| # | 问题 | 需要谁确认 | 阻塞程度 |
|---|---|---|---|
| 1 | 企业实际设备功率、负载率、蒸汽焓值等参数 | T-0016 企业数据采集 | 不阻塞，标注【待确认】 |
| 2 | 具体产品工艺路线（决定用哪几道工序） | T-0008 案例产品边界 | 需 T-0008 启动后确认 |
