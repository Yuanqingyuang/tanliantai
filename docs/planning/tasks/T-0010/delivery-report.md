# T-0010 交付报告

> 状态：草案（待确认人签注）

## 1. 基本信息

| 项 | 内容 |
| --- | --- |
| 任务名称 | T-0010 技术选型验证（PostgreSQL 三版本 / 本地模型 / AIProvider） |
| 对应任务说明 | [task.md](task.md) |
| 执行人 / Agent | 赵天志（@55msi），由 AI Agent 辅助执行 |
| 交付范围 | 技术验证报告、版本锁定清单、spike 编排与脚本、环境 README 同步、CHANGELOG |
| 遵守的流程 | development（技术验证 spike，非业务代码） |

## 2. 变更摘要

- 做了什么：用 `docker compose` 同时起 PostgreSQL 16.15 / 17.11 / 18.6，在三个版本上跑同一组 NUMERIC、JSONB、10 并发写入与两角色越权测试；实现 `AIProvider` 三态并实测本地嵌入模型；产出验证报告与版本锁定清单。
- 为什么这么做：阶段一需要尽早确认 ADR 0003 的拟选方案能否支撑"确定性核算 + AI 副驾驶"，不能用"可以"代替数字。
- 对使用者可见的影响：新增 `environment/spike/` 可复现验证环境；`environment/version-lock.md` 给出可直接使用的版本清单与数据库锁定建议。
- 对核算结果的影响：无。本任务不涉及公式、因子与核算口径。

## 3. 涉及文件

| 文件 | 变更性质 | 说明 |
| --- | --- | --- |
| [docs/planning/tasks/T-0010/task.md](../../../../docs/planning/tasks/T-0010/task.md) | 新增 | 任务说明 |
| [docs/development/T-0010-技术验证报告.md](../../../../docs/development/T-0010-技术验证报告.md) | 新增 | 四类能力结论与数字、阈值判定、回退方案 |
| [environment/version-lock.md](../../../../environment/version-lock.md) | 新增 | 工具链与数据库版本清单、锁定理由 |
| [environment/spike/docker-compose.yml](../../../../environment/spike/docker-compose.yml) | 新增 | PostgreSQL 三版本编排 |
| [environment/spike/scripts/db_checks.py](../../../../environment/spike/scripts/db_checks.py) | 新增 | 数据库四类最小验证 |
| [environment/spike/scripts/ai_provider.py](../../../../environment/spike/scripts/ai_provider.py) | 新增 | AIProvider 三态与切换 |
| [environment/spike/scripts/model_bench.py](../../../../environment/spike/scripts/model_bench.py) | 新增 | 模型四项指标实测 |
| [environment/spike/README.md](../../../../environment/spike/README.md) | 新增 | 换机照做的操作说明 |
| [environment/spike/requirements.txt](../../../../environment/spike/requirements.txt) | 新增 | 数据库验证依赖 |
| [environment/spike/requirements-model.txt](../../../../environment/spike/requirements-model.txt) | 新增 | 模型实测依赖（可选） |
| [environment/README.md](../../../../environment/README.md) | 修改 | 目录树与文件表同步新增内容 |
| [CHANGELOG.md](../../../../CHANGELOG.md) | 修改 | 记录新增验证环境与报告 |

- [x] 所有改动均在任务说明的「影响目录」内
- [x] 未触碰禁止区（见 [boundaries.md](../../../../.agents/policies/boundaries.md)）
- [x] 受控区改动已完成配套登记（`environment/README.md` 已同步）

## 4. 验证方式与结果

| # | 验证内容 | 方式（命令/步骤） | 结果 | 证据位置 |
| --- | --- | --- | --- | --- |
| 1 | 三版本数据库编排可启动 | `docker compose up -d`，三容器 healthy | 通过 | [spike/README.md](../../../../environment/spike/README.md) |
| 2 | NUMERIC / JSONB / 并发 / 越权 | `db_checks.py` 对 5433 / 5434 / 5435 各跑一次 | 三版本全部 `pass=true` | [验证报告 §3–§6](../../../../docs/development/T-0010-技术验证报告.md) |
| 3 | 清空卷后从零重建 | `compose down -v` 后 `up -d`，再跑 5433 | 通过（`pass=true`） | 报告 §10 |
| 4 | AIProvider 三态切换 | `ai_provider.py --compare` | mock 正常；local / cloud 未配置时显式 `unavailable` | 报告 §8 |
| 5 | 本地模型四项指标 | `model_bench.py`，100 条合成文本，BGE-M3 与 m3e-base 各一次 | BGE-M3 编码 122.9 ms、内存 1.870 GB、冷启动 11.086 s（超阈值）；m3e-base 36.1 ms / 0.800 GB / 8.831 s（全部达标） | 报告 §7 |
| 6 | 仓库门禁 | `check_repo_structure.py` / `check_links.py` / `check_data_safety.py` / `check_doc_sync.py` / `check_governance.py` | 全部通过（数据安全仅 2 条既有 WARN，非本次引入） | 本地执行记录 |

- 同输入同结果：AIProvider mock 模式为确定性关键词匹配，同一输入重复运行结果一致。
- 结果指纹：JSONB 快照写入—读出 SHA-256 指纹前后一致（`f28f1ed81fe6…b4e42f`）。
- 对照案例复算：不适用（不涉及核算规则）。
- 因子快照：不适用（未引入任何因子数值）。

## 5. 登记与留痕

| 登记对象 | 是否更新 | 位置 |
| --- | --- | --- |
| `knowledge/formulas/formula-register.md` | 不适用 | — |
| `knowledge/emission-factors/factor-register.md` | 不适用 | — |
| `contracts/` | 不适用 | 本任务为 spike，未定义产品契约 |
| `tests/fixtures/` | 不适用 | 合成数据只存在脚本内部，未进 fixtures |
| `CHANGELOG.md` | 是 | 新增「T-0010 技术验证骨架」条目 |
| 文档（`docs/`） | 是 | 验证报告与任务说明 |
| 任务台账 `docs/planning/tasks.md` | 否 | 由 R3 统一登记，不在本分支修改 |

- [ ] 人工确认记录已留痕（待袁青扬跑一遍 README 后签注）
- [x] AI 参与环节保留模型版本、候选列表与确认记录（`ai_provider.py` 输出含 provider / model / 候选 / 依据 / 置信度）
- [ ] 数据包相关变更已说明版本与兼容性（不适用）

## 6. 数据安全确认

- [x] 交付物中不含真实企业 BOM、工艺、价格、客户或可识别信息
- [x] 示例与测试数据均为合成数据（文本、工序表、快照均标注「合成」）
- [x] 未提交截图与附件
- [x] 云端密钥只从环境变量读取，仓库内无密钥
- [x] 模型权重不进仓库，放在仓库外目录

## 7. 未决问题

| # | 问题 | 需要谁确认 | 影响 | 阻塞程度 |
| --- | --- | --- | --- | --- |
| 1 | 基准机是哪台，模型阈值以谁的结果为准 | 袁青扬 | 本次数字只能作备注 | 阻塞阈值判定 |
| 2 | 云端 provider 与测试密钥 | 袁青扬 | cloud 只能验证「未配置时显式不可用」 | 不阻塞本阶段 |
| 3 | PostgreSQL 17.11 的 ADR 修订与签注（已于 2026-11-02 选定） | 袁青扬 | 记录版本变更 | 不阻塞其余工作 |
| 4 | 是否默认锁定 m3e-base（BGE-M3 冷启动超标） | 袁青扬 | 决定本地模型默认值与启动策略 | 不阻塞第一周其余工作 |

## 8. 已知风险与局限

| 风险/局限 | 说明 | 缓解方式 |
| --- | --- | --- |
| 测试机不是基准机 | 16 GB 内存、个人开发机，结论只对本机成立 | 基准机复测后更新报告数字 |
| 并发测试无锁竞争 | 写入互不冲突，未覆盖行锁、唯一约束、外键等待 | 留给 T-0019 集成阶段 |
| 越权只到表权限 | 完整 RBAC、租户隔离、接口鉴权未验证 | 明确留给 T-0036 |
| 云端 provider 未实测 | 无密钥，仅验证未配置时的显式失败 | 取得密钥后补测 |
| 合成工序表非正式字典 | 仅用于接口验证 | 正式工序字典随数据字典任务建立 |

## 9. 下一步

| # | 建议后续任务 | 建议负责人 | 依赖 |
| --- | --- | --- | --- |
| 1 | 在基准机复跑模型四项指标并回填 | R5 | 基准机确认 |
| 2 | T-0019 集成阶段补充锁竞争与连接池上限 | R5 | 本任务结论 |
| 3 | T-0024 量化 BGE-M3 与 m3e 的召回率差异 | R2/R5 | 检索实验设计 |
| 4 | 若采纳 PG 17.11，按 ADR 0003 修订条款记录版本变更 | R3/R5 | 袁青扬确认 |

## 10. 交付结论

- 总体结论：有条件交付（条件：确认人在另一台机器按 [spike/README.md](../../../../environment/spike/README.md) 跑通；模型阈值以基准机复测为准）。
- 审查情况：尚未完成四视角审查；确认人签注待补。
