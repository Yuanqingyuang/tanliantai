# Brightway 备选方案源码（临时收录）

> 状态：临时备选，未批准并入；不得作为运行时依赖
> 日期：2026-11-20

## 这是什么

本目录是 [Brightway](https://github.com/brightway-lca) LCA 计算框架的源码快照，仅用于评估「自研确定性核算内核」与「Brightway + 自建国内因子」两种技术路线的取舍。**它不是项目依赖，也没有被任何代码引用。**

是否并入正式技术栈，由项目负责人与技术负责人在 T-0010 技术验证后决定；决定前请勿在 `app/`、`modules/` 中 import 本目录。

## 为什么放在仓库里

1. 团队网络访问 GitHub / PyPI 不稳定，源码留在库内可避免重复下载失败；
2. 供评审者直接翻阅实现，而不是只看许可证与版本号；
3. 需要时可离线解压安装，不依赖上游仓库可用性。

## 目录内容

| 路径 | 说明 |
| --- | --- |
| `sources/<包名>/` | 各包源码，保留其原始 LICENSE 与 `pyproject.toml` |
| `requirements.lock.txt` | 本次实测环境的完整依赖锁定（99 行），用于复现 |
| `smoke_test.py` | 最小验证脚本：自定义因子 + 自定义方法 |

收录包与版本：

| 包 | 版本 | 许可证 |
| --- | --- | --- |
| brightway25 | 1.1.1 | BSD-3-Clause |
| bw2calc | 3.1.0 | BSD-3-Clause |
| bw2data | 4.8 | BSD-3-Clause |
| bw2parameters | 1.1.0 | BSD-3-Clause |
| bw_migrations | 0.2 | BSD-3-Clause |
| bw_processing | 1.6 | BSD-3-Clause |
| bw_simapro_csv | 0.5 | MIT |
| matrix_utils | 0.9 | BSD-3-Clause |
| mrio_common_metadata | 0.2.1 | BSD-3-Clause |
| multifunctional | 1.1.2 | BSD-3-Clause |
| randonneur | 0.7.2 | 见包内 `pyproject.toml` |
| stats_arrays | 4.0 | BSD-3-Clause |

**未收录**（体积或用途原因，需要时另行下载）：

- `bw2io` 0.9.17：源码包 26.3 MB，是数据导入器，核算内核不需要；
- `ecoinvent_interface` 3.1、`randonneur_data` 0.8：面向 ecoinvent，本项目不使用；
- `bw2analyzer` 0.11.8：镜像站无对应 sdist，且仅用于结果分析。

## 实测数据（2026-11-20，Windows x64 / Python 3.15.0）

| 指标 | 结果 |
| --- | --- |
| 全量安装（`pip install brightway25`） | 181.1 s，占 513.3 MB，约 70 个依赖 |
| `import bw2data` 冷启动 | 2.2 s |
| 自定义因子验证 | 1.2 kWh × 0.5810 = **0.6972**（与手算一致，浮点误差约 7.8e-9，脚本容差取 1e-6） |
| 已知问题 | 未装快速稀疏求解器时警告 `No fast sparse solver found`；构造 LCA 时传入不存在的 LCIA 方法会报 `ValueError`；SQLite 存储，多用户并发写会锁库 |

## 如何复现

```powershell
python -m venv .venv-brightway
.venv-brightway\Scripts\python -m pip install -r vendor\brightway-option\requirements.lock.txt
.venv-brightway\Scripts\python vendor\brightway-option\smoke_test.py
```

## 为通过仓库门禁所做的删减

- 删除上游 `bw_processing` 的 2 个示例 zip、`matrix_utils` 的 4 个测试 fixture zip：本仓库 `check_data_safety.py` 禁止在 `data/examples`、`data/templates`、`tests/fixtures` 之外出现数据类文件（`.zip` 等），这些文件与核算内核无关；
- 删除 `bw2calc/CHANGES.md` 与 `mrio_common_metadata/README.md`：上游正文含失效链接，会导致 `check_links.py` 失败；
- 其余源码未作任何改动，许可证文件保留在各包目录内。

## 使用边界（重要）

- 本目录**不得**被 `app/`、`modules/`、`tools/` 引用，也不得写入 `requirements.txt` 之类的运行时清单；
- 其中的因子示例（0.5810）是**占位值**，不是真实排放因子，不得复制进 `knowledge/emission-factors/factor-register.md`；
- 本目录不改变任何核算口径；如后续采用 Brightway，需走 ADR 与 T-0010 验证流程。

## 如何删除

```powershell
git rm -r vendor/brightway-option
```

删除后不影响仓库其余部分；本目录自始至终未被引用。

## 待确认

- 【待确认】是否将 Brightway 并入技术栈（确认人：袁青扬、赵天志）。
- 【待确认】若并入，采用「服务器端计算 + 临时 project 串行化」还是其他并发方案（确认人：王靖锴）。
