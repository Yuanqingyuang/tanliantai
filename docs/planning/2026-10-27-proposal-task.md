# 详细技术方案与申报内容重写任务
> 状态：草案

## 基本信息

- 日期：2026-10-27；提出人：项目负责人；执行人：Codex。
- 类型：写产品/需求文档，兼准备答辩材料；执行 development 与 review 文档流程。
- 确认人：项目负责人与指导教师；对应里程碑：2026.10—11 需求与标准。
- 目标：形成用户要求的八部分完整建议稿，明确语言、框架、模块、实验、排期与成果依据。

## 范围与非目标

- 范围：基于现有计划书和仓库，补充官方来源与研究文献；提出技术选型 ADR；形成可直接用于申报材料改写的正文。
- 非目标：不实现软件、不改正式数据契约、不启用或修改核算公式、因子、系统边界、分摊基线，不覆盖原 PDF/PPT，不承诺未经验证的效果。
- 涉及核算内容的性质：只描述研究和复核任务，已读取 calculation-change 流程；不形成核算口径决议，因此本次不改两张核算登记表。

## 输入资料

- AGENTS.md、context-map、development/review/calculation-change 流程及边界、协作、数据安全规则。
- docs/product/README.md、原计划书 PDF、docs/planning/README.md。
- docs/architecture/README.md、contracts/README.md、ADR 0001。
- knowledge 下术语与工序、公式登记、因子登记、来源登记；tests/acceptance/README.md。
- 官方标准信息、主管部门动态、作者/期刊页面及框架官方文档，检索日期 2026-10-27。

## 可验证步骤与验收标准

1. 核对已有基础：区分文件实物、原计划书自述和未完成成果。
2. 完成方案：正文包含用户列出的八部分；技术选型逐项说明用途、理由与替代方案。
3. 完成依据核验：研究现状包含国内外实际研究，不仅列政策；提供可核查链接，不捏造条款、数值和成果。
4. 形成验收路径：四组实验有对象、对照、指标、局限；数据包有回放、缺口和许可策略。
5. 检查交付：结构与环境自检、Markdown 本地链接、Git 差异；明确未执行的实现级验证。

## 影响文件

- docs/product/technical-research-proposal-2026.md（新增正文）、docs/product/README.md（索引）。
- docs/decisions/0002-proposed-local-web-stack.md（新增提议 ADR）、docs/decisions/README.md（索引与提议状态）。
- docs/planning/2026-10-27-proposal-task.md（本任务）、docs/planning/2026-10-27-proposal-delivery.md（交付报告）。
- CHANGELOG.md（文档交付记录）。

## 测试、安全与未决

- 本次无业务代码、无新测试基准，unit/integration/acceptance 业务测试不适用；不得据文档自检声称软件已通过测试。
- 不接触真实企业数据；不在新稿中复制计划书个人电话、学号等无关信息。
- 技术栈以提议 ADR 呈现，团队确认后方可作为实施基线。
- 人员姓名在原 PDF 与部分 Markdown 中有差异，新稿使用岗位分工，姓名以团队正式名单确认。
- 学校成果认定、预算到账、设备与数据库授权、实际调研记录均由负责人核验；不阻塞建议稿交付。
