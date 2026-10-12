# 开发文档

> 状态：首期骨架
> 子目录：开发、测试、协作约定

本目录约定"在本仓库里怎么干活"：目录职责、编码与文档规范、测试要求、提交与评审方式。协作红线见 [AGENTS.md](../../AGENTS.md) 与 [CONTRIBUTING.md](../../CONTRIBUTING.md)。

## 一、目录职责速查

| 目录 | 放什么 | 不放什么 |
| --- | --- | --- |
| `docs/` | 产品、架构、开发、规划、决策文档 | 运行时代码、真实数据 |
| `knowledge/` | 术语、公式、因子来源、文献依据（人可读、有来源） | 无来源数值、代码实现 |
| `app/` | 应用外壳：启动、导航、工作台编排 | 业务算法 |
| `modules/` | 业务功能模块实现 | 跨模块共享的内部结构 |
| `contracts/` | 跨模块接口与数据结构定义 | 具体实现 |
| `data/` | 可公开的示例与导入模板（脱敏） | 真实企业数据、密钥 |
| `tests/` | 单元、集成、验收测试与基准数据 | 生产数据 |
| `tools/` | 工程辅助脚本（校验、检查、转换） | 业务逻辑 |
| `environment/` | 环境说明与初始化、自检脚本 | 业务逻辑 |
| `resources/` | 品牌与应用静态资源 | 生成的构建产物 |

## 二、代码规范

- 命名：文件与目录用英文小写短横线（`activity_data/` 这类模块目录按既定结构保留下划线）；变量与函数见名知意；不在文件名中使用中文（`resources/` 的品牌资源除外）。
- 文本：UTF-8 无 BOM、LF 换行、文件末尾留空行（见 [.editorconfig](../../.editorconfig)）。
- 注释：解释**为什么**而不是复述**做什么**；核算相关代码必须标注所依据的公式 ID（对应 [公式登记表](../../knowledge/formulas/formula-register.md)）与因子来源。
- 禁止：在代码中硬编码排放因子数值、把 AI 输出直接写为核算结果、用浮点累加掩盖单位换算错误。
- 数值与单位：任何参与核算的量都必须携带单位与来源；单位换算集中在数据字典层，不在算法中零散处理。
- 【待确认】具体语言与代码风格工具（语言、格式化器、静态检查器）待技术选型后补充。

## 三、测试要求

| 层级 | 目录 | 要求 |
| --- | --- | --- |
| 单元 | [tests/unit](../../tests/unit/README.md) | 公式、单位换算、分摊算法、校验规则必须有测试；不依赖外部服务 |
| 集成 | [tests/integration](../../tests/integration/README.md) | 覆盖跨模块链路与契约一致性 |
| 验收 | [tests/acceptance](../../tests/acceptance/README.md) | 完整业务流程与四组对照实验 A/B/C/D 的判定 |
| 基准 | [tests/fixtures](../../tests/fixtures/README.md) | 固定输入与期望结果、容差、版本；发布后不得随意改动 |

- 确定性核算的**复算一致性**是必测项：同一输入与规则版本重复运行，结果与指纹必须一致。
- 涉及核算规则或因子的改动，必须提供改动前后的对照复算结果。
- 【待确认】覆盖率目标与自动化运行时机（本地钩子 / CI）。

## 四、文档要求

- 行为变了，文档必须同提交更新：`README.md`、`docs/`、`contracts/`、`knowledge/` 中受影响的条目。
- 每个文档第二行标注状态：首期骨架 / 草案 / 评审中 / 已定稿 / 已废弃。
- 结论性内容要给出依据（标准号、文献、实测）；无依据只能标【待确认】。
- 用户可见变化写入 [CHANGELOG.md](../../CHANGELOG.md)。

## 五、提交与评审

```text
分支：feat/*  fix/*  docs/*  chore/*
提交：类型(范围): 简述    例：feat(calculation): 支持按设备时间分摊共因能耗
```

- 提交前自检：`python tools/check_repo_structure.py`、`python environment/scripts/check_environment.py`。
- PR 必须填写 [PR 模板](../../.github/PULL_REQUEST_TEMPLATE.md)，说明影响目录、是否涉及核算/因子/数据字典、验证方式与结果。
- 涉及核算口径、因子入库、数据包格式的改动需要成员人工复核；AI 不得自审自批。
- 评审视角与清单见 [.agents/workflows/review.md](../../.agents/workflows/review.md)。

## 六、环境

- 首选开发容器（见 [.devcontainer](../../.devcontainer/devcontainer.json)），本地开发见 [environment/README.md](../../environment/README.md)。
- 环境自检：`python environment/scripts/check_environment.py`。
- 提交前确认不会把真实企业数据带进暂存区（见 [.agents/policies/data-security.md](../../.agents/policies/data-security.md)）。

## 七、待确认项

- 【待确认】编程语言、框架、数据库与打包方式（决定本节第二部分的工具链）。
- 【待确认】是否引入 pre-commit 钩子与自动化格式化。
- 【待确认】测试覆盖率目标与是否要求集成测试在 CI 中执行（当前 CI 仅做结构级检查）。
