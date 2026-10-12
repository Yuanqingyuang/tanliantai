# 任务台账

> 状态：草案

本文件是团队**运行中任务的唯一台账**：谁在做、做到哪一步、谁确认、改了哪些目录、对应哪个 PR。它把散落在文档与对话里的「谁在何时确认了什么」（`AGENTS.md` 规则 R9「留痕」）收敛成一处可查记录，并为并行协作提供共享事实（见 [collaboration.md §3](../../.agents/policies/collaboration.md)）。

- 里程碑与阶段产出见 [README.md](README.md)。
- 单个任务的完整说明用 [.agents/templates/task.md](../../.agents/templates/task.md)；交付用 [.agents/templates/delivery-report.md](../../.agents/templates/delivery-report.md)。
- 任务的类型取值见 [.agents/context-map.md](../../.agents/context-map.md)。

## 一、任务 ID

```text
T-<四位序号>          例：T-0001、T-0002（全项目连续编号，不复用）
```

一个任务从提出到归档只用一个 ID；提交信息与 PR 标题在末尾附 `[T-0001]`，便于把改动追回任务。

## 二、状态机

```text
待认领 → 进行中 → 待评审 → 已完成
   └────────┴────────┴──────→ 已取消
```

| 状态 | 含义 | 进入条件 |
| --- | --- | --- |
| 待认领 | 已提出，尚无负责人 | 提出人登记一行 |
| 进行中 | 已有负责人，正在做 | 负责人认领并填写「影响目录」 |
| 待评审 | 已交付，等待确认人复核 | 交付报告完成（见 [review.md §7](../../.agents/workflows/review.md)） |
| 已完成 | 确认人签注通过 | 确认人在「确认」列留下签注 |
| 已取消 | 不再进行 | 在「确认」列说明原因 |

## 三、字段说明

| 列 | 说明 |
| --- | --- |
| ID | 见上 |
| 标题 | 一句话，可判定 |
| 类型 | 见 [.agents/context-map.md](../../.agents/context-map.md) 的任务类型 |
| 负责人 | 执行人；由 Agent 执行时写「Agent」，并填监督人 |
| 确认人 | 「待确认」与验收的裁定人；**核算口径类任务不得与负责人为同一人** |
| 状态 | 见状态机 |
| 影响目录 | 本次允许改动的目录，作为并行文件分区的依据 |
| 关联 PR | PR 编号或链接 |
| 确认 | 确认人的签注（`通过` / `有条件通过` / `退回` + 日期） |
| 更新 | 最近一次更新日期 |

## 四、台账

| ID | 标题 | 类型 | 负责人 | 确认人 | 状态 | 影响目录 | 关联 PR | 确认 | 更新 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-0001 | 建立 Agent 协作框架（确定性检查 + CI 门禁 + 协作/写作流程） | 工程配置 / CI | Agent（监督：赵天志） | 袁青扬（@Yuanqingyuang） | 待评审 | `.github/`、`tools/`、`.agents/`、`docs/`、`README.md`、`AGENTS.md`、`CONTRIBUTING.md`、`CHANGELOG.md` | 待填 | — | 2026-10-12 |

> 新增任务时复制上一行、改内容即可；**不要删除历史行**，历史行的状态变更即留痕。

## 五、留痕文件位置

- 每个任务的**任务说明**与**交付报告**归档在 `docs/planning/tasks/<任务 ID>/`：
  - `task.md`：按 [.agents/templates/task.md](../../.agents/templates/task.md) 填写；
  - `delivery-report.md`：按 [.agents/templates/delivery-report.md](../../.agents/templates/delivery-report.md) 填写。
- 状态进入「待评审」后，这两份文件必须已存在——`check_governance.py` 会校验（见 [tools/README.md](../../tools/README.md)）。
- 台账行的「关联 PR」在 PR 开出后回填；「确认」由确认人在签注时填写（缺一不算完成，见 [review.md §7](../../.agents/workflows/review.md)）。
