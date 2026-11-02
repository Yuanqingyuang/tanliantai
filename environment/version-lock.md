# T-0010 版本锁定清单

> 状态：草案（数据库、工具链与本地模型已实测；待确认人签注）
> 日期：2026-11-02
> 范围：T-0010 技术验证环境，不代表产品最终发布版本

## 一、工具链

| 组件 | 实测版本 | 获取方式 | 备注 |
| --- | --- | --- | --- |
| Docker Desktop | 29.9.2 | 官方安装包 | 引擎运行于 WSL2 |
| Docker Compose | v5.6.1 | 随 Docker Desktop | `docker compose version` |
| WSL | 2.7.14.0（内核 6.18.33.2） | `winget install --id Microsoft.WSL` | 需重启后生效 |
| Python | 3.12.16 | `uv python install 3.12` | 与 CI 一致，不覆盖系统 Python 3.14 |
| psycopg | 3.3.6（binary） | `uv pip install "psycopg[binary]"` | 三版本连接均通过 |
| torch | 2.15.0+cpu | `pip install sentence-transformers` | 仅模型实测需要；CPU 版 |
| sentence-transformers | 6.2.0 | 同上 | 模型加载与编码 |
| transformers | 5.22.1 | 同上 | 随 sentence-transformers 安装 |

## 二、PostgreSQL 候选版本

| 版本 | 实测小版本 | 镜像摘要 | 测试结果 |
| --- | --- | --- | --- |
| 16 | 16.15 | `postgres@sha256:5db6dac2ef5dcff512f4f00a009c3c332b9f2f28f24277175bf3e4a3d02ef83a` | NUMERIC / JSONB / 并发 / 越权 全部通过 |
| 17 | 17.11 | `postgres@sha256:3b0cda93be7c8dba2ed484d19393d93845dc3dafb88973e248ba8e6d99d784e1` | 同上，全部通过 |
| 18 | 18.6 | `postgres@sha256:3a4264520e121176619f54ff867d12774bc81e95e7b84db58d63bccdb6144b81` | 同上，全部通过 |

三个版本在同一组测试上结果一致，差异不在功能，而在运维风险与生命周期。

## 三、锁定建议

**已选定 PostgreSQL 17.11**（2026-11-02 团队选定；待确认人袁青扬签注）。

| 候选 | 支持理由 | 风险 |
| --- | --- | --- |
| **17.11（建议）** | 测试全部通过；发布已满一个版本周期，运维资料与扩展生态成熟；比 16 新一个主版本，避免刚锁定就面临升级 | 需同步修订 ADR 0003（原文写的是 16.x） |
| 16.15 | 与 ADR 0003 现状一致，无需修订；测试全部通过 | 已是两个主版本之前，项目周期内会较早遇到升级压力 |
| 18.6 | 最新版本，测试全部通过；新项目无历史包袱 | 发布较晚，团队无运维经验；镜像数据目录与默认校验和设置有变化，部署脚本需额外验证 |

若确定改为 17.11，按 ADR 0003 的修订条款补一条版本变更记录，不新开 ADR。

## 四、本地模型

100 条合成文本，CPU 推理、fp32 未量化；数字来自本机（非基准机），阈值判定仍以基准机为准。

| 模型 | 体积 | 单条编码（中位 / p95） | 内存峰值 | 冷启动 | 判定 |
| --- | --- | --- | --- | --- | --- |
| BGE-M3 | 2191.1 MB | 122.9 / 161.7 ms | 1.870 GB | 11.086 s | 编码与内存达标，**冷启动超标** |
| m3e-base | 390.7 MB | 36.1 / 40.6 ms | 0.800 GB | 8.831 s | 全部达标 |

**建议锁定 m3e-base**【待确认：袁青扬】作为阶段一默认本地嵌入模型；BGE-M3 作为可选升级，需基准机复测达标或采用延迟加载（模型移出启动路径）。两者召回率差异待 T-0024 量化，本清单不预设数值。

GPU 未参与测试；CPU 与 GPU 结果不可混比。

## 五、环境限制

| 项 | 实测值 | 影响 |
| --- | --- | --- |
| 宿主机内存 | 16 GB | 同时跑三个数据库与模型会紧张 |
| Docker 可用内存 | 8.2 GB | 三库并行时约占用数百 MB，模型测试建议单独进行 |
| 宿主机 GPU | RTX 5070 Laptop 8 GB | 是否启用 GPU 需在报告中注明，CPU/GPU 结果不可混比 |

## 六、复现命令

```powershell
docker compose -f environment/spike/docker-compose.yml up -d
python environment/spike/scripts/db_checks.py --dsn "host=127.0.0.1 port=5433 user=postgres password=spike_local_only dbname=spike"
docker image inspect postgres:16 postgres:17 postgres:18 --format "{{index .RepoDigests 0}}"
```
