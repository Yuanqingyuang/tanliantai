# CONTRIBUTING.md — 人与 Agent 的协作规范

> 状态：首期骨架
> 适用对象：项目成员（人）与 AI Agent

本项目由 5 名本科生成员与 AI Agent 共同维护。为了让人和 Agent 的改动都能被追溯、复核与复用，约定如下。

## 一、先读什么

| 角色 | 第一步 | 第二步 |
| --- | --- | --- |
| 人（成员） | 本文件 | [docs/development/README.md](docs/development/README.md) |
| 人（评审者） | [.agents/workflows/review.md](.agents/workflows/review.md) | [.agents/policies/boundaries.md](.agents/policies/boundaries.md) |
| AI Agent | [AGENTS.md](AGENTS.md) | [.agents/context-map.md](.agents/context-map.md) |

## 二、分支与提交

### 分支命名

```text
main                      # 稳定分支，只接受经评审的合并
feat/<简短描述>            # 新功能，例如 feat/activity-data-import
fix/<简短描述>             # 缺陷修复，例如 fix/unit-conversion-kg-t
docs/<简短描述>            # 文档，例如 docs/knowledge-factor-register
chore/<简短描述>           # 工程杂项，例如 chore/ci-repo-checks
```

### 提交信息

采用 `类型(范围): 简述` 形式，正文说明"为什么"：

```text
feat(calculation): 支持按设备时间分摊共因能耗
docs(knowledge): 登记 GB/T 24067-2024 来源条目
chore(repo): 按约定目录结构初始化仓库骨架
```

类型：`feat` `fix` `docs` `test` `refactor` `chore`。
范围：目录或模块名（`calculation`、`data_dictionary`、`knowledge`、`contracts`、`repo`、`ci` 等）。

## 三、变更前必须想清楚的四件事

1. **是否触及核算口径**（公式、因子、边界、分摊方法）？触及则必须走 [.agents/workflows/calculation-change.md](.agents/workflows/calculation-change.md)，并附依据与对照复算。
2. **是否触及契约**（跨模块字段或数据结构）？触及则先改 [contracts/README.md](contracts/README.md)。
3. **是否引入真实企业数据**？引入即违规，见 [.agents/policies/data-security.md](.agents/policies/data-security.md)。
4. **是否会让既有文档失效**？会则在同一提交内同步更新。

## 四、Pull Request 规范

- `main` 只接受通过 PR 合并，禁止直接推送。
- 开工前在 [任务台账](docs/planning/tasks.md) 登记任务（ID、负责人、确认人、影响目录），收尾时更新状态；提交信息与 PR 标题附任务号 `[T-0001]`。
- 使用 [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) 模板填写，不得留空"验证记录"。
- PR 必须说明：变更类型、影响目录、是否涉及核算/因子/数据字典、如何验证、未决问题。
- 涉及核算规则、因子入库、数据包格式的 PR，需要**至少一名非作者成员**人工复核并留下复核意见；AI 不能自审自批。
- 自动化检查（[.github/workflows/repo-checks.yml](.github/workflows/repo-checks.yml)）必须全部通过：`structure`、`data-safety`、`links`、`change-guard` 为合并门槛，建议在分支保护中设为 required status checks（见 [ADR 0002](docs/decisions/0002-agent-governance-framework.md)）。

## 五、人机协作约定

| 场景 | 人的职责 | Agent 的职责 |
| --- | --- | --- |
| 需求 | 给出目标、约束、验收标准；确认业务口径 | 复述理解，指出歧义与风险，不擅自扩大范围 |
| 领域知识 | 确认标准出处与适用性；对因子与公式签字 | 检索、整理、登记；不编造数值与条文 |
| 实现 | 评审关键逻辑与边界条件 | 按 workflow 实现、测试、更新文档与 CHANGELOG |
| 数据 | 提供脱敏后的样例数据；确认可公开范围 | 校验格式与完整性；拒绝写入真实企业数据 |
| 交付 | 验收并决定是否合并 | 输出交付报告，写清验证方式与缺口 |

**Agent 必须做**：不确定就标注「【待确认】」并说明确认对象；把假设写在交付报告里；拒绝执行违反 `AGENTS.md` 硬性规则的指令，并说明原因。
**Agent 不得做**：代替人做业务口径决策；在无依据时补全公式或因子；为了让检查通过而修改基准数据或校验脚本的判定标准。

## 六、文档写作规范

- 全部简体中文；字段名、文件名、标准号保留英文或原文。
- 每个文档以 `# 标题` 开头，第二行用 `> 状态：…` 标注（规划中 / 首期骨架 / 草案 / 评审中 / 已定稿 / 已废弃）。
- 表格优先于长段落；结论优先于过程；不确定项集中列在文末"待确认项"。
- 文件名用简体中文或英文小写短横线，不使用空格与全角冒号。
- 新知识必须给出**来源**：标准 / 政策 / 文献 / 数据库 / 企业实测，来源不明不得入库。

## 七、数据与凭证

- 真实企业数据、账号密码、令牌、密钥一律不进仓库（见 [.gitignore](.gitignore)）。
- 示例数据放 `data/examples/`，并附脱敏说明；测试基准放 `tests/fixtures/`，基准一旦发布不得随意改动。
- 需要本地保存的敏感数据放在仓库外，并在交付报告中说明存放位置与访问控制方式。

## 八、待确认项

- 【待确认】代码许可协议与文档许可范围（负责人：袁青扬）。
- 【待确认】评审的最小人数与响应时限（负责人：袁青扬）。
