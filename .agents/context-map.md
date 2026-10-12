# 任务类型 → 必读资料映射表

> 状态：首期骨架

用法：开工前先在下表定位任务类型，按"必读顺序"读完资料，再进入对应 workflow。表中"对应 workflow"列为空表示按 [`workflows/development.md`](workflows/development.md) 或 [`workflows/review.md`](workflows/review.md) 处理。

## 0. 全局前置（任何任务都要读）

1. [`AGENTS.md`](../AGENTS.md)
2. [`.agents/README.md`](README.md)
3. 与任务相关的 [`docs/decisions/README.md`](../docs/decisions/README.md) 条目（选型未定则不得自行假设）
4. 涉及功能交付的，读 [`contracts/README.md`](../contracts/README.md)

## 1. 映射表

| 任务类型 | 必读资料（按序） | 产出物 | 对应 workflow |
| --- | --- | --- | --- |
| 写产品/需求文档 | [`docs/product/README.md`](../docs/product/README.md) → [`docs/planning/README.md`](../docs/planning/README.md) → [`.agents/policies/collaboration.md`](policies/collaboration.md) | 需求文档、范围与非目标、验收标准 | development |
| 改核算规则（公式/边界/单位/分摊） | [`knowledge/formulas/formula-register.md`](../knowledge/formulas/formula-register.md) → [`knowledge/README.md`](../knowledge/README.md) → [`docs/architecture/README.md`](../docs/architecture/README.md) → [`tests/fixtures/README.md`](../tests/fixtures/README.md) | 依据说明、登记表更新、对照案例复算记录、版本与指纹变化说明 | calculation-change |
| 改数据字典（物料/工序/活动数据字段） | [`docs/architecture/README.md`](../docs/architecture/README.md) → [`data/examples/README.md`](../data/examples/README.md) → [`contracts/README.md`](../contracts/README.md) | 字段口径变更说明、字段映射表、示例数据更新 | development |
| 改排放因子库 | [`knowledge/emission-factors/factor-register.md`](../knowledge/emission-factors/factor-register.md) → [`knowledge/README.md`](../knowledge/README.md) → [`knowledge/formulas/formula-register.md`](../knowledge/formulas/formula-register.md) | 因子快照、来源/区域/版本/单位四重校验记录 | calculation-change |
| 做 AI 候选匹配 | [`docs/architecture/README.md`](../docs/architecture/README.md) → [`data/examples/README.md`](../data/examples/README.md) → [`knowledge/emission-factors/factor-register.md`](../knowledge/emission-factors/factor-register.md) | 候选输出格式（含依据与置信度）、评测记录（Top-1/Top-3/修正率） | development |
| 做前端界面（Web 工作台） | [`docs/architecture/README.md`](../docs/architecture/README.md) → [`contracts/README.md`](../contracts/README.md) → [`docs/development/README.md`](../docs/development/README.md) → [`environment/README.md`](../environment/README.md) | 界面与交互说明、人工确认交互记录点 | development |
| 做数据包（DataPackage） | [`contracts/README.md`](../contracts/README.md) → [`docs/architecture/README.md`](../docs/architecture/README.md) → [`data/examples/README.md`](../data/examples/README.md) → [`tests/fixtures/README.md`](../tests/fixtures/README.md) | 数据包结构、缺口与质量等级、指纹与修改记录 | development / release |
| 写测试 | [`.agents/policies/testing.md`](policies/testing.md) → [`tests/fixtures/README.md`](../tests/fixtures/README.md) → [`contracts/README.md`](../contracts/README.md) | 分层测试用例、复算一致性用例、基准数据说明 | development |
| 准备答辩材料 | [`docs/product/README.md`](../docs/product/README.md) → [`docs/planning/README.md`](../docs/planning/README.md) → [`.agents/policies/collaboration.md`](policies/collaboration.md) | 材料大纲、图表与数据口径核对表、结论与依据对照 | review / release |
| 发版 | [`.agents/workflows/release.md`](workflows/release.md) → [`contracts/README.md`](../contracts/README.md) → [`tests/fixtures/README.md`](../tests/fixtures/README.md) | CHANGELOG、版本号、数据包规范版本、冻结清单 | release |
| 接触企业真实数据 | [`.agents/policies/data-security.md`](policies/data-security.md) → [`data/examples/README.md`](../data/examples/README.md) | 脱敏方案、访问与操作日志、本地部署选项说明 | development |
| 新增/调整环境与工具链 | [`environment/README.md`](../environment/README.md) → [`tools/README.md`](../tools/README.md) → [`docs/decisions/README.md`](../docs/decisions/README.md) | 环境说明更新、ADR（若涉及选型） | development |

## 2. 按任务类型补充的强制动作

| 若任务触及 | 必须额外做的动作 |
| --- | --- |
| 目标、边界、分摊、单位、因子取值 | 走 [`workflows/calculation-change.md`](workflows/calculation-change.md)，缺依据不得合入 |
| 核心实体字段（Product / BOMItem / Process / ActivityData / EmissionFactor / Mapping / CalculationRun / DataPackage） | 先改 [`contracts/README.md`](../contracts/README.md)，后改实现 |
| 结果指纹或计算可回放性 | 提供同输入同结果证据，并在交付报告中写明验证命令与结果 |
| 权限、脱敏、日志 | 走 [`.agents/policies/data-security.md`](policies/data-security.md) 检查清单 |
| 任何跨目录大范围改动 | 在 [`templates/task.md`](templates/task.md) 中先声明"影响目录" |

## 3. 产出物归档位置

| 产出物 | 归档位置 |
| --- | --- |
| 需求与产品文档 | [`docs/product/`](../docs/product/README.md) |
| 架构、字段口径、字典 | [`docs/architecture/`](../docs/architecture/README.md) |
| 开发与评测说明 | [`docs/development/`](../docs/development/README.md) |
| 里程碑与计划 | [`docs/planning/`](../docs/planning/README.md) |
| 选型决策 | [`docs/decisions/`](../docs/decisions/README.md) |
| 公式与因子登记 | [`knowledge/`](../knowledge/README.md) |
| 接口与数据契约 | [`contracts/`](../contracts/README.md) |
| 测试与基准数据 | [`tests/fixtures/`](../tests/fixtures/README.md) |
| 示例（脱敏）数据 | [`data/examples/`](../data/examples/README.md) |
| 脚本与工具 | [`tools/`](../tools/README.md) |

## 4. 查表失败时的处理

- 任务类型不在表中：**不要猜测**，先在任务说明中标注「【待确认】任务类型归属」，由项目负责人确认后再开工。
- 必读资料尚未创建：标注「【待确认】资料缺失：<路径>」，说明需要谁补齐，可在不依赖该资料的部分先行推进。
