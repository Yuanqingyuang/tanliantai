# 任务说明：T-0002 技术基线 ADR 0003

> 状态：待评审

## 1. 基本信息

| 项 | 内容 |
| --- | --- |
| 任务名称 | 技术基线 ADR 0003（应用形态/技术栈/部署/模型） |
| 任务类型 | 架构决策 / 文档（见 [context-map.md](../../../../.agents/context-map.md)） |
| 提出人 | 项目团队 |
| 执行人 / Agent | Agent（监督：待指定） |
| 确认人 | 项目负责人、指导教师（待确认） |
| 关联里程碑 | 2026.10—11 需求与标准 |
| 是否触及核算口径 | 否 |

## 2. 目标

- 将应用形态、技术栈与数据库、部署并发、模型运行四项决策固化为 ADR 0003，作为后续实施的基线。

## 3. 范围

- 本次要做：
  - 起草并收口 [ADR 0003](../../../decisions/0003-local-web-workbench-baseline.md)；
  - 更新决策索引、架构文档的待确认项与 CHANGELOG；
  - 在 WBS 与任务台账中补充认证权限任务与对应依赖。

## 4. 非目标

- 本次明确不做：
  - 不编写业务代码、不搭建数据库或模型环境；
  - 不决定 D4–D16 中的其他事项；
  - 不替代 T-0010 的技术验证实测。

## 5. 输入资料

| 资料 | 路径或来源 | 是否已存在 |
| --- | --- | --- |
| 原项目计划书 | [docs/product/链碳台_项目计划书_v1.pdf](../../../product/链碳台_项目计划书_v1.pdf) | 是 |
| 现行架构与待确认项 | [docs/architecture/README.md](../../../architecture/README.md) | 是 |
| 决策清单与 ADR 模板 | [docs/decisions/README.md](../../../decisions/README.md) | 是 |
| 外部技术方案稿 | 技术方案建议稿（未入库） | 是 |
| 团队讨论结论 | 2026-10-27 讨论（Web 客户端、PostgreSQL、内网多用户、分阶段混合） | 是 |

## 6. 验收标准

| # | 判定条件（可观测） | 验证方式 |
| --- | --- | --- |
| 1 | ADR 含四项决策、备选方案、理由、后果、影响范围与重审条件 | 逐节检查 ADR 0003 |
| 2 | 决策索引、架构待确认项、CHANGELOG 与 ADR 状态一致 | 检查对应文件 |
| 3 | 治理、链接、结构检查无失败项 | 运行 `tools/check_governance.py`、`check_links.py`、`check_repo_structure.py` |
| 4 | 确认人复核并签注 | 任务台账“确认”列 |

## 7. 影响目录

| 目录/文件 | 变更性质 | 是否受控（见 [boundaries.md](../../../../.agents/policies/boundaries.md)） |
| --- | --- | --- |
| `docs/decisions/` | 新增 / 修改 | 否 |
| `docs/architecture/README.md` | 修改 | 否 |
| `docs/planning/wbs.md`、`docs/planning/tasks.md` | 修改 | 否 |
| `CHANGELOG.md` | 修改 | 否 |

- [x] 已确认改动不触碰禁止区
- [x] 涉及选型的改动已有 ADR（本任务）
- [x] 与其他并行任务无文件冲突

## 8. 测试要求

| 层级 | 要求 |
| --- | --- |
| unit | 不适用，本任务无代码 |
| integration | 不适用 |
| acceptance | 文档一致性检查与治理门禁通过 |
| fixtures | 不适用 |

- [ ] 若涉及核算：需要同输入同结果与指纹稳定性验证（本任务不涉及）
- [ ] 若涉及因子或公式：需要登记表更新与对照案例复算（本任务不涉及）

## 9. 数据与安全

- [x] 本次是否接触企业真实数据：否
- [x] 交付物中不含可识别企业信息

## 10. 交付物

| 交付物 | 形式 | 归档位置 |
| --- | --- | --- |
| ADR 0003 | Markdown | [docs/decisions/0003-local-web-workbench-baseline.md](../../../decisions/0003-local-web-workbench-baseline.md) |
| 决策索引、架构与 CHANGELOG 更新 | Markdown | `docs/decisions/README.md`、`docs/architecture/README.md`、`CHANGELOG.md` |
| WBS 与台账更新 | Markdown | `docs/planning/wbs.md`、`docs/planning/tasks.md` |

## 11. 未决事项

| # | 问题 | 需要谁确认 | 阻塞程度 |
| --- | --- | --- | --- |
| 1 | 指导教师复核意见待补录 | 指导教师 | 不阻塞 |
| 2 | PostgreSQL、本地模型与权限矩阵的实测由 T-0010 验证 | 技术验证负责人 | 阻塞实施，不阻塞 ADR 收口 |
| 3 | D4–D16 不在本任务范围 | 项目团队 | 不阻塞 |
| 4 | T-0002 监督人待指定 | 项目负责人 | 不阻塞 |
