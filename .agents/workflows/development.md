# 工作流：功能开发

> 状态：草案

适用：新增功能、新增模块、新增接口、新增字段口径。总原则是**先定契约再写实现**；本项目的一切输出都必须可复核、可交付。

## 0. 前置检查

- [ ] 已按 [`.agents/README.md`](../README.md) 的顺序加载规则
- [ ] 已在 [`context-map.md`](../context-map.md) 定位任务类型与必读资料
- [ ] 已用 [`templates/task.md`](../templates/task.md) 写出任务说明（含范围与非目标）
- [ ] 任务是否触及核算口径？若触及，改走 [`calculation-change.md`](calculation-change.md)

## 1. 需求澄清

| 项 | 要求 |
| --- | --- |
| 用户与场景 | 明确服务于谁（如无专职碳管理岗的中小供应商），对应哪个痛点 |
| 输入 | 明确数据从哪来：BOM 文件、工时记录、设备能耗、辅材用量 |
| 输出 | 明确产出物形态：界面展示、结构化数据、碳数据包字段 |
| 验收标准 | 可观测、可判定；不允许"体验更好"这类标准 |
| 非目标 | 明确列出本次不做的内容，防止范围蔓延 |
| 选型依赖 | 若依赖未定的选型（语言/框架/桌面壳 vs Web 工作台），标注「待确认」并指向 `docs/decisions/` |

## 2. 设计

- [ ] 划清三层归属：智能层（候选/依据/置信度）、核算层（确定性计算）、交付层（数据包）
- [ ] 确认不存在"AI 直接产生核算数值"的路径
- [ ] 列出受影响的核心实体字段（Product / BOMItem / Process / ActivityData / EmissionFactor / Mapping / CalculationRun / DataPackage）
- [ ] 说明数据版本化与结果指纹是否受影响；若受影响，写明影响方式

## 3. 契约先行

1. 先在 [`contracts/README.md`](../../contracts/README.md) 更新字段名、类型、单位、必填性、来源。
2. 再同步 [`docs/architecture/README.md`](../../docs/architecture/README.md) 的字段口径说明。
3. 涉及字典内容时同步 [`data/examples/README.md`](../../data/examples/README.md) 的脱敏示例。
4. 契约冻结后再动实现代码；契约未定不得先写"临时字段"并长期保留。

## 4. 实现

- [ ] 改动范围与任务说明"影响目录"一致，未越界
- [ ] 遵守 [`.agents/policies/boundaries.md`](../policies/boundaries.md)
- [ ] 凡涉及企业数据的读写路径，遵守 [`.agents/policies/data-security.md`](../policies/data-security.md)（最小权限、日志、脱敏）
- [ ] AI 相关实现只输出候选与依据，保留模型版本与候选列表，供审计追溯
- [ ] 不引入无出处的默认因子或默认范围值

## 5. 测试

按 [`.agents/policies/testing.md`](../policies/testing.md) 分层补齐：

- unit：字段校验、单位换算、规则约束
- integration：BOM→工序映射、因子选取、计算链路
- acceptance：端到端产出数据包，含缺口与质量等级
- fixtures：使用 [`tests/fixtures/README.md`](../../tests/fixtures/README.md) 中的基准数据，不新增未登记基准

确定性要求：同一输入必须得到同一结果，且结果指纹稳定。

## 6. 文档

- [ ] 用户可见行为变化写入 [`docs/development/README.md`](../../docs/development/README.md)
- [ ] 字段口径变化写入 `docs/architecture/`
- [ ] 选型或架构决策写入 [`docs/decisions/README.md`](../../docs/decisions/README.md)（ADR）
- [ ] 新增脚本/工具在 [`tools/README.md`](../../tools/README.md) 登记
- [ ] 环境或依赖变化在 [`environment/README.md`](../../environment/README.md) 登记

## 7. 评审

- [ ] 按 [`review.md`](review.md) 四视角自查：代码、文档、知识与依据、数据安全
- [ ] 用 [`templates/delivery-report.md`](../templates/delivery-report.md) 输出交付报告
- [ ] 未决问题逐条列出并标注「待确认」及确认人

## 8. 退出条件

| 条件 | 判定 |
| --- | --- |
| 契约已更新且与实现一致 | 必达 |
| 分层测试通过，含确定性复算 | 必达 |
| 文档与登记表同步 | 必达 |
| 无未登记的依据性数字 | 必达 |
| 交付报告完成 | 必达 |
