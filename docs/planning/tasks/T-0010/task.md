# T-0010 任务说明：技术选型验证 spike

> 状态：草案

## 1. 基本信息

| 项 | 内容 |
| --- | --- |
| 任务名称 | 技术选型验证 spike |
| 任务类型 | 技术验证 / 新增或调整环境与工具链（见 [context-map.md](../../../../.agents/context-map.md)） |
| 提出人 | 袁青扬（项目负责人） |
| 执行人 / Agent | 赵天志（@55msi） |
| 确认人 | 袁青扬（按《阶段一任务书》7.1，确认方式为“跑一遍 README”） |
| 关联里程碑 | 2026.10—11 需求与标准 |
| 是否触及核算口径 | 否 |

## 2. 目标

- 把 ADR 0003 的拟选方案（PostgreSQL + 本地嵌入模型 + AIProvider 三态）在真实机器上实测一遍。
- 四类能力各给出结论与数字：① `NUMERIC` 精度 ② `JSONB` 快照 ③ 本地模型延迟与内存 ④ `AIProvider` 三态切换。
- 给出 PostgreSQL 16/17/18 的锁定建议，以及达不到阈值时的回退方案与代价。

## 3. 范围

- 本次要做：
  - `docker compose` 起 PostgreSQL 16/17/18，各跑同一组精度、快照、并发与越权测试。
  - 编写最小 `AIProvider` 抽象（`cloud` / `local` / `mock`），用环境变量切换。
  - 本地嵌入模型（BGE-M3 一类）100 条文本的加载、延迟、内存、冷启动实测。
  - 输出技术验证报告、版本锁定清单、启动脚本与 README。

## 4. 非目标

- 本次明确不做：
  - 不做产品功能，不实现业务模块（留给 T-0019 及之后）。
  - 不做完整 RBAC 与租户隔离，只做最小越权验证（完整方案留给 T-0036）。
  - 不替 ADR 做最终选型决定；若建议改版本，另走 ADR 修订记录。
  - 不引入真实企业数据；全部测试数据为合成数据。

## 5. 输入资料

| 资料 | 路径或来源 | 是否已存在 |
| --- | --- | --- |
| 阶段一任务书 R5 段 | 《阶段一任务书》R5 段（见 `docs/phase1-plan-sync` 分支的 `phase-1-task-book.md`，该分支尚未合并） | 是 |
| 选型决策 | [ADR 0003](../../../decisions/0003-local-web-workbench-baseline.md) | 是 |
| T-0002 交付报告（技术前置） | [delivery-report.md](../T-0002/delivery-report.md) | 是 |
| 环境约定 | [environment/README.md](../../../../environment/README.md) | 是 |
| 任务台账 | [tasks.md](../../tasks.md) | 是 |

## 6. 验收标准

| # | 判定条件（可观测） | 验证方式 |
| --- | --- | --- |
| 1 | 四类能力各有结论与数字 | 报告四节，每节附实测值 |
| 2 | 达阈值（单条编码 ≤500ms / 内存 ≤2.5GB / 冷启动 ≤10s）或给出回退方案与代价 | 阈值判定表 + m3e 回退实测 |
| 3 | 并发与越权验证有结论（10 并发、连接池上限、越权被拒） | 测试脚本输出与拒绝记录 |
| 4 | 换一台机器可从零启动 | 清空卷后按 README 重建并记录步骤 |
| 5 | 版本清单可直接用，且写明 PostgreSQL 16/17/18 的锁定理由 | version-lock 表 |

## 7. 影响目录

| 目录/文件 | 变更性质 | 是否受控（见 [boundaries.md](../../../../.agents/policies/boundaries.md)） |
| --- | --- | --- |
| `docs/development/` | 新增验证报告 | 否 |
| `environment/spike/` | 新增编排、脚本与说明 | 是（环境受控区，需同步 README） |
| `environment/version-lock.md` | 新增版本锁定清单 | 是（同上） |
| `docs/planning/tasks/T-0010/` | 新增任务说明与交付报告 | 否 |
| `CHANGELOG.md` | 修改 | 否 |

- [x] 已确认改动不触碰禁止区
- [x] 涉及选型的改动已有 ADR 或已标注「待确认」
- [x] 与其他并行任务无文件冲突

## 8. 测试要求

| 层级 | 要求 |
| --- | --- |
| unit | 不适用（本任务无业务代码） |
| integration | PostgreSQL 三版本上的 NUMERIC / JSONB / 并发 / 越权最小验证 |
| acceptance | 按验收标准 1–5 逐条对照 |
| fixtures | 新增合成数据，不接触真实企业数据 |

## 9. 数据与安全

- [x] 本次是否接触企业真实数据：否
- [x] 测试数据全部为合成数据，连接密码仅为本地临时值
- [x] 交付物中不含可识别企业信息

## 10. 交付物

| 交付物 | 形式 | 归档位置 |
| --- | --- | --- |
| 技术验证报告 | Markdown | `docs/development/T-0010-技术验证报告.md` |
| 版本锁定清单 | Markdown | `environment/version-lock.md` |
| 编排与脚本 | Compose + Python | `environment/spike/` |
| 交付报告 | Markdown | `docs/planning/tasks/T-0010/delivery-report.md` |

## 11. 未决事项

| # | 问题 | 需要谁确认 | 阻塞程度 |
| --- | --- | --- | --- |
| 1 | 【待确认：基准机是哪一台，阈值只认基准机结果】 | 确认人袁青扬 | 阻塞模型阈值判定 |
| 2 | 【待确认：云端 AIProvider 用哪家、是否提供测试密钥】 | 确认人袁青扬 | 阻塞 cloud 实测 |
| 3 | 【待确认：本地模型最终选型（BGE-M3 vs m3e 回退）】 | 确认人袁青扬（赵天志提建议） | 不阻塞 |
