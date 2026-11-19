# 任务说明：T-0004 术语、单位与公式基线

> 状态：已完成

## 1. 基本信息

| 项 | 内容 |
| --- | --- |
| 任务名称 | 术语、单位与公式基线（R2 知识库与指标主体建设） |
| 任务类型 | 知识库 / 文档（见 [context-map.md](../../../../.agents/context-map.md)） |
| 提出人 | 项目团队 |
| 执行人 / Agent | R2 知识库维护 |
| 确认人 | 袁青扬（@Yuanqingyuang） |
| 关联里程碑 | 2026.10—11 需求与标准 |
| 是否触及核算口径 | 是 |

## 2. 目标

- 统一全项目的用词、单位与验收口径
- 建立 TERM-xxx / UNIT-xxx / F-<域>-<三位序号> 三套 ID 规范
- 补全 GB/T 24067-2024 条款号、标准值来源（GB/T 2589-2020、IPCC AR6）、区域电网因子来源
- 明确分摊(Apportionment)与分配(Allocation)口径区别，本项目仅做分摊

## 3. 范围

- 本次要做：
  - 第 1 周（10.29–11.04）：建立 TERM/UNIT/F-<域> 骨架（TERM-001-glossary.md, UNIT-001-units.md, formula-register.md, acceptance-criteria.md）
  - 第 2 周（11.05–11.11）：合并去重现有 glossary.md、carbon-footprint.md、allocation-methods.md、bibliography.md，分配 ID、补定义、标出处条款号
  - 第 3 周（11.12–11.18）：全表查重、常量溯源、与 R4(T-0008) 交叉、自检清单、交付报告

## 4. 非目标

- 本次明确不做：
  - 不编写业务代码、不实现核算引擎
  - 不决定具体产品边界与功能单位（属 T-0008）
  - 不采集企业真实数据（属 T-0016）

## 5. 输入资料

| 资料 | 路径或来源 | 是否已存在 |
| --- | --- | --- |
| 旧版术语表 | knowledge/domain/glossary.md | 是 |
| 旧版单位换算 | knowledge/domain/units-and-conversions.md | 是 |
| 旧版碳足迹公式 | knowledge/formulas/carbon-footprint.md | 是 |
| 旧版分摊方法 | knowledge/formulas/allocation-methods.md | 是 |
| 旧版书目 | knowledge/references/bibliography.md | 是 |
| GB/T 24067-2024 公开元数据 | 国家标准信息公开平台 | 是 |
| GB/T 2589-2020 标准煤当量 | 国家标准信息公开平台 | 是 |
| IPCC AR6 GWP 取值 | IPCC 官网 | 是 |
| 中国区域电网因子 | 生态环境部官网 | 是 |

## 6. 验收标准（对照自检清单 ①–⑧）

| # | 判定条件（可观测） | 验证方式 |
| --- | --- | --- |
| ① | 三类 ID 全局唯一（TERM/UNIT/F- 前缀无冲突） | 逐表统计 ID 列去重计数 |
| ② | 每条可追溯（抽 10 条核对 R-xxx + 条款号） | 抽样检查出处字段 |
| ③ | 单位换算方向明确（非定义性换算均有来源/版本） | 检查 UNIT 表来源/版本列 |
| ④ | 无未登记系数（公式表不含具体数值，系数均指向 factor-register.md） | 检查 formula-register 表达式列 |
| ⑤ | 指标无较高/较好模糊表述（acceptance-criteria 已量化阈值） | 检查 acceptance-criteria 阈值列 |
| ⑥ | 实验卡含失败判定（A/B/C/D 四卡均有失败判定行） | 检查 acceptance-criteria 实验卡 |
| ⑦ | 四组实验沿用 A/B/C/D 定义，未重新定义实验 | 对照 tests/acceptance/README.md |
| ⑧ | 容差与每组最少样本量、统计口径齐全 | 检查 acceptance-criteria 指标表 |

## 7. 影响目录

| 目录/文件 | 变更性质 | 是否受控 |
| --- | --- | --- |
| knowledge/domain/TERM-001-glossary.md | 新增 / 重写 | 是（T1） |
| knowledge/domain/UNIT-001-units.md | 新增 / 重写 | 是（T1） |
| knowledge/formulas/formula-register.md | 新增 / 重写 | 是（T1） |
| knowledge/references/bibliography.md | 修改 / 补全 | 是（T1） |
| tests/acceptance/acceptance-criteria.md | 已有，未改动 | 是（T1） |
| docs/planning/tasks.md | 更新台账 | 否 |

- [x] 已确认改动不触碰禁止区
- [x] 涉及核算口径，确认人与负责人不同人
- [x] 与其他并行任务无文件冲突

## 8. 测试要求

| 层级 | 要求 |
| --- | --- |
| unit | 不适用（文档类任务） |
| integration | 不适用 |
| acceptance | 自检清单 ①–⑧ 全绿 |
| fixtures | 不新增 |

- [x] 涉及核算：需同输入同结果与指纹稳定性验证（本任务为基线文档，不涉及运行）
- [x] 涉及因子或公式：需登记表更新与对照案例复算（已完成登记表更新）

## 9. 数据与安全

- [x] 本次是否接触企业真实数据：否
- [x] 交付物中不含可识别企业信息

## 10. 交付物

| 交付物 | 形式 | 归档位置 |
| --- | --- | --- |
| 任务说明 | Markdown | 本文件 |
| 交付报告 | Markdown | [delivery-report.md](delivery-report.md) |
| 术语表 | Markdown | knowledge/domain/TERM-001-glossary.md |
| 单位表 | Markdown | knowledge/domain/UNIT-001-units.md |
| 公式登记表 | Markdown | knowledge/formulas/formula-register.md |
| 书目表 | Markdown | knowledge/references/bibliography.md |

## 11. 未决事项

| # | 问题 | 需要谁确认 | 阻塞程度 |
| --- | --- | --- | --- |
| 1 | GB/T 24067-2024 条款号精确核对（当前为公开元数据推断） | 核算负责人 / R1 | 不阻塞，标注待确认 |
| 2 | 企业蒸汽参数、压缩空气口径、燃气热值、负载率来源 | 企业计量清单 | 不阻塞，标注待确认 |
| 3 | 多因素法权重确定方法 | 实验 B 方案与复核人 | 不阻塞，标注待确认 |
| 4 | 运输排放是否纳入默认边界 | 标准要求与客户模板 | 不阻塞，标注待确认 |
| 5 | R4(T-0008) 案例产品边界与术语/单位覆盖交叉 | T-0008 负责人 | 需 T-0008 启动后交叉 |
