# 0002. Agent 协作框架：把协作规范落到可执行机制

> 状态：提议
> 日期：2026-10-12
> 决策人：袁青扬（项目负责人）｜复核：全体成员与指导教师 王嘉昀

## 背景与问题

链碳台团队主要由 Agent（AI 编码助手）承担实际产出。仓库已有的治理资产——[AGENTS.md](../../AGENTS.md) 的硬性规则 R1–R9、[collaboration.md](../../.agents/policies/collaboration.md) 的协作约定、[data-security.md](../../.agents/policies/data-security.md) 的数据安全分级——目前**全部是散文形式**，且这些骨架文档多由 AI 快速生成，尚未逐条落地为可执行约束。

在"多 Agent 并行、少量人工把关"的场景下，散文规则有两个结构性缺陷：

1. **服从不可靠**：Agent 对长篇自然语言规则的遵守程度随上下文长度、任务切分方式波动，无法保证每条规则都被执行。
2. **无强制力**：现有 CI 只有一条结构级检查（`check_repo_structure.py`）加一次环境自检，真正能被机器判定并阻断的硬规则不足两条（约 1.5 条）。越界改核算口径、把真实数据或凭据提交进仓库、文档与代码脱节、遗留待确认标记却无人认领——都能"悄悄"合入 main。

问题：如何让这些规范在"由 Agent 干活"的前提下真正生效，而不是停留在纸面？

## 备选方案

| 方案 | 做法 | 优点 | 缺点 |
| --- | --- | --- | --- |
| A. 强化散文 | 把 AGENTS.md 与 policies 写得更细、更长 | 零工程成本 | Agent 对长文规则服从不稳定；无法阻止误操作合入 main；规则越多越容易互相矛盾 |
| B. 引入重型工程平台 | 上测试框架、linter、格式化钩子、审批流 | 覆盖强、生态成熟 | 当前无任何代码、技术栈尚未确定（负责人：袁青扬），等于为不存在的问题先建基础设施 |
| C. 分层强制模型 | 为每条规范寻找它能到达的**最高强制层**，逐条落地 | 就近选择最轻机制；可增量落地；机制与规范一一对应、可核查 | 需要额外写少量检查脚本与 CI 配置 |

## 决策

**采用方案 C：分层强制模型。**

把规范按"可机器判定程度"分派到五个强制层，同一条规范尽量落到它能到达的最高层：

| 层 | 名称 | 形态 | 强制力 | 对应资产 |
| --- | --- | --- | --- | --- |
| L0 | 规范层 | 散文规则 | 靠自觉（最弱） | AGENTS.md、.agents/policies |
| L1 | 模板层 | 结构化声明 | 填错易被发现 | .agents/templates/task.md、delivery-report.md、PR 模板 |
| L2 | 本地检查层 | 提交前自检脚本 | 可拦截、可绕过 | tools/check_*.py |
| L3 | CI 门禁层 | 分支保护 required checks | 不可绕过 | .github/workflows/repo-checks.yml |
| L4 | 平台机制层 | CODEOWNERS 与评审路由 | 结构性约束 | .github/CODEOWNERS、分支保护 |

规范到机制的映射：

| 规则 | 内容 | 到达层 | 落地机制 |
| --- | --- | --- | --- |
| R1 | 不造数 | L1 + 抽检 | 交付报告 §6、任务说明 §9 声明；人工抽样 |
| R2 | AI 不下场算数 | L0 + 抽检 | ADR 0001 约束；架构不变量必测项（[testing.md](../../.agents/policies/testing.md)）；四视角审查 |
| R3 | 无依据不改核算口径 | **L3** | `check_doc_sync.py` 强制同批更新登记表、CHANGELOG 或 ADR |
| R4 | 数据不出门 | **L3** | `check_data_safety.py` 阻塞凭据与真实数据 |
| R5 | 契约先行 | L1 + **L3**（部分） | contracts 变更须伴随 docs/ 或 CHANGELOG（由 `check_doc_sync.py` 的 R6 规则强制）；"先契约后实现"的顺序仍靠人审 |
| R6 | 文档与代码同步 | **L3** | `check_doc_sync.py`（modules、app、contracts 触发） |
| R7 | 不越界修改 | **L4** | CODEOWNERS 评审路由 + 任务说明 §7 影响目录声明 |
| R8 | 可验证 | **L3** + 抽检 | `check_links.py`；交付报告 §4 验证记录 |
| R9 | 留痕 | L1 + L3 代理 | 任务台账的登记与签注；`check_governance.py --changed-only` 检查新增内容的待确认留痕；交付报告 §5 |

配套的协作协议：

1. **文件分区**（collaboration.md §3）由 [CODEOWNERS](../../.github/CODEOWNERS) 承载；开启分支保护并勾选 "Require review from Code Owners" 后生效。
2. **main 必须走 PR 且非作者评审**：分支保护中关闭直接推送，并把 `structure`、`data-safety`、`links`、`change-guard` 设为 required status checks。
3. **结构化交付**：开工用任务说明模板，收尾用交付报告模板，把"做了什么、怎么验证、是否登记、是否含真实数据"变成必填字段。
4. **不确定项留痕**：新增内容里的待确认标记必须同行标注负责人或确认人（`check_governance.py` 在变更集上强制）。
5. **运营闭环**：任务在 [任务台账](../../docs/planning/tasks.md) 登记与流转；文档写作走 [authoring.md](../../.agents/workflows/authoring.md)；人审签注按 [review.md §7](../../.agents/workflows/review.md) 落痕（台账 + 交付报告）。

边界（本 ADR 明确不做的事）：

- 不引入第三方依赖与重型工具；检查脚本一律纯标准库、Python 3.9 及以上。
- 不因"暂无代码"而预置测试或格式化钩子——相关决策仍挂在 [决策索引](README.md) 的 D8，待技术栈确定后再议。
- 语义类规则（例如 R2、R8 中"结论是否成立"）无法机器判定，本框架只做**结构化声明 + 抽样人审**，不假装能自动判定。

## 理由

- **机制优于叮嘱**：Agent 对工具的服从是确定性的——脚本失败即 `exit 1`，CI 红灯即无法合并；对散文的服从是概率性的。把规则从散文升级为机制，是以最小代价换最大确定性。
- **就近选择强制层**：R3–R7 这类"改动联动"规则天然可机器判定（diff 一比对即出结论），直接放到 L3；R1、R2、R8、R9 涉及语义，硬塞进机器只会产生假阳性，因此收敛在 L1 声明加人审。
- **可增量、可回退**：脚本与 CI job 相互独立，任一机制失效不影响其余；技术栈确定前只上线"不依赖运行时"的检查。
- **对答辩与结题友好**：每条规范都有对应的落地机制与运行证据，能直接回答"你们如何保证 Agent 不闯祸"。

## 后果与代价

- 需要维护新增的 4 个脚本与 4 个 CI job；脚本自身的缺陷可能误伤（已通过"基线不可用时按通过处理"等设计降低风险）。
- 首次上线需人工在 GitHub 开启分支保护并配置 required checks 与 Code Owners——**属仓库设置，无法由代码自动完成**，需项目负责人在仓库 Settings 中手工开启。
- `check_governance.py --changed-only` 的待确认检查是**行级**近似：它保证"标注了负责人"，但不保证"负责人真的认领"。语义正确性仍依赖抽样人审。
- 引入少量流程开销：做事前要写任务说明，收尾要写交付报告。

## 影响范围

| 范围 | 影响 |
| --- | --- |
| 目录 | `.github/`（工作流、CODEOWNERS）、`tools/`（4 个新脚本）、`.agents/`（写作流程、签注 SOP）、`docs/decisions/`（本 ADR）、`docs/planning/`（任务台账） |
| 规则 | 落地 [AGENTS.md](../../AGENTS.md) R1–R9；衔接 [collaboration.md](../../.agents/policies/collaboration.md) §3、[data-security.md](../../.agents/policies/data-security.md) |
| 流程 | main 保护、PR 评审、任务与交付模板的使用方式 |
| 工具 | 新增 `check_links.py`、`check_data_safety.py`、`check_doc_sync.py`、`check_governance.py`，并重构 `check_repo_structure.py`（移除重复的警告级扫描） |

## 待确认与开放项

- 【待确认】各模块负责人的 GitHub 用户名（负责人：袁青扬），补全后细化 CODEOWNERS 的路径归属。
- 【待确认】是否启用"必须非作者评审"（负责人：袁青扬）——即本 ADR 的复核结论。
- 分支保护与 required checks 的具体配置需项目负责人在 GitHub 仓库设置中手动开启。

## 复核与重审条件

出现以下任一情况时重审本决策：项目引入正式测试框架与格式化工具（届时 D8 决策落地，L2 与 L3 需扩展）；CODEOWNERS 评审频率过高导致评审成为瓶颈；某条被机器强制的规则被证明产生持续误报；或团队规模变化导致文件分区需要重新划分。
