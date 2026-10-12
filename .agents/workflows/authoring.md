# 工作流：文档写作

> 状态：草案

适用：撰写或大改任何**面向他人阅读**的文档——产品/需求文档、架构与设计说明、研究报告、综述、商业计划书、答辩材料、README 与各类规范。目标：让 AI 辅助写作**既快又不失真**——不编造数值与条文，依据可查，术语一致，改动可追溯。

不适用：纯代码实现（走 [development.md](development.md)）；核算口径变更（走 [calculation-change.md](calculation-change.md)）。

## 0. 前置检查

- [ ] 已在 [任务台账](../../docs/planning/tasks.md) 登记任务并填「影响目录」
- [ ] 已按 [context-map.md](../context-map.md) 定位任务类型与必读资料
- [ ] 涉及核算结论时，结论以 [calculation-change.md](calculation-change.md) 走完的口径为准，本文只引用、不自行下结论

## 1. 定位与依据清单

- 先写清：写给谁、解决什么问题、范围与非目标（对应 [templates/task.md](../templates/task.md)）。
- 列出本文要用到的**依据来源**，逐条给可核查标识：标准号 + 条款、政策文号、文献题录、数据源名称 + 版本。
- 无法核实的一律标注为待确认并写明对象（形如 `待确认：<需查什么 / 问谁>`，格式见 [knowledge/README.md §5](../../knowledge/README.md)），**不得先写成断言**。

## 2. 大纲先行

- 先定章节结构与每节要点，确认无缺口后再写正文。
- 结论性内容先标"待核实"，正文阶段再逐条补依据。

## 3. 起草（AI 可参与）

- AI 只产出**候选文本与依据**，不杜撰数值、条款细节、文献页码、市场数字（规则 R1）。
- 涉及数值或结论的句子，必须能指向第 1 步依据清单中的某一条。

## 4. 依据核对（关键关卡）

- 逐条比对：文中每个数字、每句"标准规定…"、每处引用，是否都能回溯到依据清单。
- 对不上的：补依据、改为待确认标记，或删除。**不允许"看起来对"就留下。**
- 涉及核算数值的，只能引用确定性核算结果，不得由 AI 文本生成（规则 R2）。

## 5. 一致性与规范

- 术语以 [knowledge/domain/glossary.md](../../knowledge/domain/glossary.md) 为准；新增术语先登记。
- 来源条目按 [knowledge/references/README.md](../../knowledge/references/README.md) 与 [bibliography.md](../../knowledge/references/bibliography.md) 登记。
- 排版与写作细节遵循 [CONTRIBUTING.md §六](../../CONTRIBUTING.md)（简体中文、`> 状态：…` 标注、表格优先、文末集中列待确认）与 [docs/development §四](../../docs/development/README.md)，不在此重复。

## 6. 状态标注

- 每个文档第二行标 `> 状态：…`，取值用 [CONTRIBUTING.md §六](../../CONTRIBUTING.md) 的词表：规划中 / 首期骨架 / 草案 / 评审中 / 已定稿 / 已废弃。
- 与之区分：`knowledge/` 条目的**证据审核状态**用其自有的 `draft / review / verified / deprecated`（见 [knowledge/README.md §3](../../knowledge/README.md)）。两套词表各管各的，不混用。

## 7. 自审与他审

- 自审用 [review.md](review.md) 的「文档审查」与「知识与依据审查」两个视角。
- 对外材料、含核算结论的文档，须经**非作者**按 [review.md §7](review.md) 签注。

## 8. 出口条件

| 条件 | 判定 |
| --- | --- |
| 文中数字、条款、引用均可回溯到依据清单 | 必达 |
| 无未标注来源的断言；不确定项均已标注并指明确认对象 | 必达 |
| 术语与 glossary 一致，来源已在书目登记 | 必达 |
| 文档状态已标注，需要时已记 CHANGELOG | 必达 |
| 对外或含核算结论的文档已取得非作者签注 | 必达 |
