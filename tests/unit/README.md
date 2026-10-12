# 单元测试（tests/unit）

> 状态：首期骨架

本目录存放**最小粒度**的自动化测试：单个公式、单次换算、单条校验规则的输入输出。
单元测试必须能脱离数据库、网络与界面独立运行，任何需要外部服务的验证都不属于本层。

## 一、测试范围

| 范围 | 说明 | 对应知识/模块 |
| --- | --- | --- |
| 核算公式 | 产品碳足迹计算、活动数据 × 排放因子、汇总与边界内求和 | `knowledge/formulas/carbon-footprint.md`、[../../modules/calculation/README.md](../../modules/calculation/README.md) |
| 单位换算 | 质量、能量、面积、件数的换算与量纲校验 | `knowledge/domain/units-and-conversions.md` |
| 分摊算法 | 共用工序/共用资源的分配，分配后守恒性 | `knowledge/formulas/allocation-methods.md` |
| 校验规则 | 必填字段、数值范围、单位匹配、日期区间、枚举取值 | `modules/data_dictionary`、`modules/activity_data` |
| 字段映射 | BOM 物料 → 工序 → 活动数据的映射判定与候选排序 | `modules/manufacturing`、`modules/data_dictionary` |

## 二、必须覆盖的行为

1. **确定性**：同一输入重复执行，结果完全一致（数值与结果指纹都不变）。
2. **守恒性**：分摊前后总量相等，误差不超过基准数据声明的容差。
3. **幂等性**：重复导入同一份活动数据不产生重复计量。
4. **失败可解释**：非法输入必须报错并给出可读原因，而不是静默取默认值。
5. **边界条件**：零值、负值、空集合、超长小数、单位缺省。

## 三、约定

| 项目 | 约定 |
| --- | --- |
| 命名 | 与被测对象同名加后缀，例如 `calc_carbon_footprint` → `test_calc_carbon_footprint` |
| 放置 | 与被测实现同层镜像；跨模块的用例不放本目录 |
| 粒度 | 一个用例只断言一件事；断言失败信息须包含输入值与期望值 |
| 数据 | 只使用 `tests/fixtures/` 下的脱敏样例或用例内联构造的数据 |
| 依赖 | **禁止**依赖外部服务、真实企业数据、随机数（如需随机须固定种子） |
| 时长 | 单个用例应在毫秒级完成；慢用例应下沉或标注原因 |

## 四、运行方式

**【待确认】**：技术栈（语言 / 框架 / 数据库）未定，因此测试框架与运行命令尚未固化。
确定后须在本节补上**可直接复制执行**的命令，并同步：

- `.devcontainer/devcontainer.json` 的 `postCreateCommand`（如需预热环境）；
- `.github/workflows/repo-checks.yml`（如仍需保持"结构级"检查则只追加注释说明）。

当前可先运行仓库级自检确认环境就绪：

```bash
python3 environment/scripts/check_environment.py
python3 tools/check_repo_structure.py
```

## 五、禁止事项

- 禁止把真实企业 BOM、工艺参数、客户名与价格写进用例或期望值。
- 禁止在单元测试中调用大模型接口：AI 只给候选，不是确定性计算的依赖。
- 禁止为了让用例通过而放宽容差；容差必须来自 `tests/fixtures/` 的基准声明。

## 六、相关文档

- 测试总规则：[../../.agents/policies/testing.md](../../.agents/policies/testing.md)
- 数据安全底线：[../../.agents/policies/data-security.md](../../.agents/policies/data-security.md)
- 集成测试：[../integration/README.md](../integration/README.md)
- 验收测试：[../acceptance/README.md](../acceptance/README.md)
- 基准数据规范：[../fixtures/README.md](../fixtures/README.md)
