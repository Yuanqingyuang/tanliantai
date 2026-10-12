# 集成测试（tests/integration）

> 状态：首期骨架

本目录验证**跨模块链路**能否打通：数据从导入到导出，是否在模块边界处保持契约一致。
集成测试允许使用临时数据库或临时文件，但**禁止**依赖真实企业数据与外部在线服务。

## 一、主链路

核心链路（每个环节都应有对应的集成用例）：

```text
BOM 导入 → 工序映射 → 活动数据录入 → 排放因子匹配 → 确定性核算运行 → 数据包导出
```

| 环节 | 关注点 | 涉及模块 |
| --- | --- | --- |
| BOM 导入 | 模板解析、必填校验、错误行定位、重复料号处理 | `modules/manufacturing` |
| 工序映射 | 候选生成、人工确认结果落库、映射版本留痕 | `modules/manufacturing`、`modules/data_dictionary` |
| 活动数据 | 单位一致性、期间覆盖、与工序的关联完整性 | `modules/activity_data` |
| 因子匹配 | 因子版本选择、适用边界校验、缺因子时的显式失败 | `modules/emission_factors` |
| 核算运行 | 规则约束 → 人工确认 → 确定性计算 | [../../modules/calculation/README.md](../../modules/calculation/README.md) |
| 数据包导出 | 字段完整、结构合法、可被重新解析并复算 | `modules/data_package` |

## 二、契约一致性测试

契约是跨模块的唯一接口定义，见 [../../contracts/README.md](../../contracts/README.md)。
本层必须覆盖：

1. **字段级一致**：契约中声明的必填字段在导出物中全部存在，命名与大小写完全一致。
2. **枚举级一致**：状态、单位、边界类型等枚举取值只能来自契约定义，不允许自由文本。
3. **版本级一致**：数据包中记录的契约版本 / 数据字典版本 / 因子版本与实际使用的一致。
4. **可复算**：用导出的数据包重新驱动核算，结果与原核算一致（复算一致率的目标见验收测试）。
5. **破坏性变更**：契约发生破坏性变更时，旧版本数据包仍应可解析或明确报错，不得静默错算。

## 三、约定

| 项目 | 约定 |
| --- | --- |
| 数据来源 | 只使用 [../fixtures/README.md](../fixtures/README.md) 约定的脱敏案例 |
| 环境隔离 | 每个用例使用独立的临时目录 / 临时库，结束后清理，不污染工作区 |
| 外部依赖 | 大模型、网络、邮件等一律打桩或跳过；AI 候选链路可用固定候选集代替 |
| 失败定位 | 断言失败须能指出是链路哪一环、哪条记录出了问题 |
| 时长 | 单次集成测试应控制在分钟级 |

## 四、运行方式

**【待确认】**：技术栈未定，集成测试的运行命令与所需服务（数据库等）尚未固化。
确定后须在本节补齐命令、前置服务启动方式与数据准备步骤，并同步 `docs/development/README.md`。

当前可先确认结构与环境就绪：

```bash
python3 tools/check_repo_structure.py
python3 environment/scripts/check_environment.py
```

## 五、禁止事项

- 禁止在集成测试里写入真实企业的 BOM、工艺参数或客户信息。
- 禁止依赖需要手动准备的本地数据；一切输入必须来自 `tests/fixtures/`。
- 禁止把"通过集成测试"当成"核算口径正确"的证明——口径正确性由知识库与评审保证。

## 六、相关文档

- 测试总规则：[../../.agents/policies/testing.md](../../.agents/policies/testing.md)
- 单元测试：[../unit/README.md](../unit/README.md)
- 验收测试：[../acceptance/README.md](../acceptance/README.md)
- 模块入口：[../../modules/calculation/README.md](../../modules/calculation/README.md)
- 活动数据模块：[../../modules/activity_data/README.md](../../modules/activity_data/README.md)
