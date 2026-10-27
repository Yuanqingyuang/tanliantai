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
| T-0002 | 技术基线 ADR 0003（应用形态/技术栈/部署/模型） | 架构决策 | Agent（监督：待定） | 待确认 | 待评审 | `docs/decisions/`、`docs/architecture/`、`docs/planning/`、`CHANGELOG.md` | — | — | 2026-10-27 |
| T-0003 | 标准与政策梳理（GB/T 24067-2024 等） | 文档/标准 | 待认领 | 待确认 | 待认领 | `knowledge/references/` | — | — | 2026-10-27 |
| T-0004 | 术语、单位与公式基线 | 知识库 | 待认领 | 待确认 | 待认领 | `knowledge/domain/`、`knowledge/formulas/` | — | — | 2026-10-27 |
| T-0005 | PCBA-SMT 工序链与设备清单 | 调研/知识库 | 待认领 | 待确认 | 待认领 | `knowledge/domain/` | — | — | 2026-10-27 |
| T-0006 | 企业需求调研 | 调研 | 待认领 | 待确认 | 待认领 | `docs/product/`、`docs/planning/` | — | — | 2026-10-27 |
| T-0007 | 指标体系与四组实验定义 | 测试/实验设计 | 待认领 | 待确认 | 待认领 | `tests/acceptance/` | — | — | 2026-10-27 |
| T-0008 | 案例产品与核算边界基线 | 产品/核算 | 待认领 | 待确认 | 待认领 | `docs/product/`、`knowledge/domain/` | — | — | 2026-10-27 |
| T-0009 | 数据许可与来源清单 | 文档/合规 | 待认领 | 待确认 | 待认领 | `knowledge/references/`、`docs/decisions/` | — | — | 2026-10-27 |
| T-0010 | 技术选型验证 spike | 技术验证 | 待认领 | 待确认 | 待认领 | `docs/development/`、`environment/` | — | — | 2026-10-27 |
| T-0011 | 数据字典 V0.1 | 数据字典 | 待认领 | 待确认 | 待认领 | `modules/data_dictionary/`、`contracts/` | — | — | 2026-10-27 |
| T-0012 | 契约 V0.1（User/Role 必进，Rule/Evidence 待定） | 契约 | 待认领 | 待确认 | 待认领 | `contracts/` | — | — | 2026-10-27 |
| T-0013 | 碳数据包规范 V0.1 | 规范 | 待认领 | 待确认 | 待认领 | `modules/data_package/`、`contracts/` | — | — | 2026-10-27 |
| T-0014 | 系统设计（分层/模块/接口/存储） | 架构 | 待认领 | 待确认 | 待认领 | `docs/architecture/` | — | — | 2026-10-27 |
| T-0015 | 导入模板设计 | 数据/模板 | 待认领 | 待确认 | 待认领 | `data/templates/` | — | — | 2026-10-27 |
| T-0016 | 数据集采集（公开/合成/脱敏） | 数据建设 | 待认领 | 待确认 | 待认领 | `data/examples/`、`tests/fixtures/` | — | — | 2026-10-27 |
| T-0017 | 标注规范与标注 | 标注 | 待认领 | 待确认 | 待认领 | `tests/fixtures/` | — | — | 2026-10-27 |
| T-0018 | 数据集复核与测试集冻结 | 数据/测试 | 待认领 | 待确认 | 待认领 | `tests/fixtures/` | — | — | 2026-10-27 |
| T-0019 | 最小技术集成（前后端+DB+AIProvider） | 工程 | 待认领 | 待确认 | 待认领 | `app/`、`modules/`、`environment/` | — | — | 2026-10-27 |
| T-0020 | 导入与人工审核闭环 | 开发 | 待认领 | 待确认 | 待认领 | `app/`、`modules/manufacturing/`、`modules/data_dictionary/` | — | — | 2026-10-27 |
| T-0021 | 规则检索与人工确认 | 开发/AI | 待认领 | 待确认 | 待认领 | `modules/data_review/` | — | — | 2026-10-27 |
| T-0022 | 确定性核算引擎 | 开发/核算 | 待认领 | 待确认 | 待认领 | `modules/calculation/` | — | — | 2026-10-27 |
| T-0023 | 分摊四方法实现与对照 | 开发/核算 | 待认领 | 待确认 | 待认领 | `modules/calculation/`、`knowledge/formulas/` | — | — | 2026-10-27 |
| T-0024 | 语义/融合检索与消融 | 开发/AI | 待认领 | 待确认 | 待认领 | `modules/data_review/` | — | — | 2026-10-27 |
| T-0025 | 接口文档与契约同步 | 文档/契约 | 待认领 | 待确认 | 待认领 | `contracts/`、`docs/development/` | — | — | 2026-10-27 |
| T-0026 | 数据包、审计与回放 | 开发/数据包 | 待认领 | 待确认 | 待认领 | `modules/data_package/` | — | — | 2026-10-27 |
| T-0027 | 结果分析与图表 | 开发/分析 | 待认领 | 待确认 | 待认领 | `app/`、`modules/analysis/` | — | — | 2026-10-27 |
| T-0028 | 四组实验执行 A/B/C/D | 实验 | 待认领 | 待确认 | 待认领 | `tests/acceptance/`、`tests/fixtures/` | — | — | 2026-10-27 |
| T-0029 | 评测报告与敏感性分析 | 报告 | 待认领 | 待确认 | 待认领 | `docs/development/` | — | — | 2026-10-27 |
| T-0030 | 案例数据包与系统测试 | 测试/数据 | 待认领 | 待确认 | 待认领 | `data/examples/`、`tests/` | — | — | 2026-10-27 |
| T-0031 | 字典/规范 V1.0 冻结 | 规范/文档 | 待认领 | 待确认 | 待认领 | `knowledge/`、`contracts/`、`docs/` | — | — | 2026-10-27 |
| T-0032 | 软著材料与登记 | 申报 | 待认领 | 待确认 | 待认领 | `docs/product/`、`app/` | — | — | 2026-10-27 |
| T-0033 | 研究报告/论文 | 文档/研究 | 待认领 | 待确认 | 待认领 | `docs/planning/`、`docs/development/` | — | — | 2026-10-27 |
| T-0034 | 商业计划书 | 申报/文档 | 待认领 | 待确认 | 待认领 | `docs/product/` | — | — | 2026-10-27 |
| T-0035 | 结题与答辩材料 | 结题 | 待认领 | 待确认 | 待认领 | `docs/product/` | — | — | 2026-10-27 |
| T-0036 | 认证、角色与权限管理（登录/权限矩阵/审计） | 开发/安全 | 待认领 | 待确认 | 待认领 | `app/`、`modules/`、`contracts/` | — | — | 2026-10-27 |

> 新增任务时复制上一行、改内容即可；**不要删除历史行**，历史行的状态变更即留痕。

## 五、留痕文件位置

- 每个任务的**任务说明**与**交付报告**归档在 `docs/planning/tasks/<任务 ID>/`：
  - `task.md`：按 [.agents/templates/task.md](../../.agents/templates/task.md) 填写；
  - `delivery-report.md`：按 [.agents/templates/delivery-report.md](../../.agents/templates/delivery-report.md) 填写。
- 状态进入「待评审」后，这两份文件必须已存在——`check_governance.py` 会校验（见 [tools/README.md](../../tools/README.md)）。
- 台账行的「关联 PR」在 PR 开出后回填；「确认」由确认人在签注时填写（缺一不算完成，见 [review.md §7](../../.agents/workflows/review.md)）。
