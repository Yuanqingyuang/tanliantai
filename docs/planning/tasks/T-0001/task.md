# 任务说明：T-0001 建立 Agent 协作框架

> 状态：评审中

## 1. 基本信息

| 项 | 内容 |
| --- | --- |
| 任务名称 | 建立 Agent 协作框架（确定性检查 + CI 门禁 + 协作/写作流程） |
| 任务类型 | 工程配置 / 仓库治理（见 [context-map.md](../../../../.agents/context-map.md)） |
| 提出人 | 赵天志（@55msi） |
| 执行人 / Agent | Agent（监督：赵天志） |
| 确认人 | 袁青扬（@Yuanqingyuang） |
| 关联里程碑 | 2026.10—11 需求与标准 |
| 是否触及核算口径 | 否 |

## 2. 目标

- 把"多 Agent 并行、少量人工把关"的协作规范落到可执行机制：确定性检查脚本 + CI 门禁 + 协作/写作流程文档，降低"因 AI 导致混乱"的风险。

## 3. 范围

- 本次要做：
  - 新增 `tools/` 下确定性检查脚本（check_links / check_data_safety / check_doc_sync / check_governance）；
  - 扩展 CI 为多 job 门禁，新增 `CODEOWNERS`；
  - 新增文档写作流程、任务台账与人审签注 SOP；撰写 ADR 0002。

## 4. 非目标

- 本次明确不做：
  - 不引入第三方依赖或测试框架；
  - 不实现业务代码与核算引擎；
  - 不代为开启 GitHub 分支保护（属仓库设置，由负责人手工完成）。

## 5. 输入资料

| 资料 | 路径或来源 | 是否已存在 |
| --- | --- | --- |
| 仓库现有规范 | `AGENTS.md`、`CONTRIBUTING.md`、`.agents/` | 是 |
| 分层强制模型设计 | [ADR 0002](../../../decisions/0002-agent-governance-framework.md) | 是 |
| 模板 | `.agents/templates/task.md`、`delivery-report.md` | 是 |

## 6. 验收标准

| # | 判定条件（可观测） | 验证方式 |
| --- | --- | --- |
| 1 | 4 个检查脚本在干净仓库运行退出码为 0 | 逐条运行，检查退出码 |
| 2 | 注入违规时脚本退出码为 1 | 隔离副本构造违规场景 |
| 3 | CI 的 4 个 job 显示名与文档声明的 required checks 一致 | 比对 `repo-checks.yml` 与 ADR/CONTRIBUTING |
| 4 | 全量检查（含 `--changed-only`）在本变更集上全绿 | 运行 6 项检查 |

## 7. 影响目录

| 目录/文件 | 变更性质 | 是否受控（见 [boundaries.md](../../../../.agents/policies/boundaries.md)） |
| --- | --- | --- |
| `.github/` | 新增 / 修改 | 是（T2） |
| `tools/` | 新增 / 修改 | 是（T1） |
| `.agents/` | 新增 / 修改 | 是（T2） |
| `docs/` | 新增 | 是 |
| `README.md`、`AGENTS.md`、`CONTRIBUTING.md`、`CHANGELOG.md` | 修改 | 是 |

- [x] 已确认改动不触碰禁止区
- [x] 涉及选型的改动已有 ADR（ADR 0002）
- [x] 与其他并行任务无文件冲突（见 [collaboration.md](../../../../.agents/policies/collaboration.md)）

## 8. 测试要求

| 层级 | 要求 |
| --- | --- |
| unit | 不适用（脚本以端到端场景验证） |
| integration | 隔离副本注入违规场景，验证门禁拦截 |
| acceptance | 6 项检查在干净仓库全绿 |
| fixtures | 不新增；仅复用 `tests/fixtures/` 既有基准 |

- [x] 不涉及核算，无需同输入同结果验证
- [x] 不涉及因子或公式

## 9. 数据与安全

- [x] 本次是否接触企业真实数据：否
- [x] 交付物中不含可识别企业信息

## 10. 交付物

| 交付物 | 形式 | 归档位置 |
| --- | --- | --- |
| 任务说明 | Markdown | 本文件 |
| 交付报告 | Markdown | [delivery-report.md](delivery-report.md) |
| 框架设计 | ADR | [ADR 0002](../../../decisions/0002-agent-governance-framework.md) |

## 11. 未决事项

| # | 问题 | 需要谁确认 | 阻塞程度 |
| --- | --- | --- | --- |
| 1 | CODEOWNERS 的真实用户名（团队分工未定） | 项目负责人（袁青扬） | 不阻塞 |
| 2 | 是否启用"非作者评审"分支保护 | 项目负责人（袁青扬） | 不阻塞 |
