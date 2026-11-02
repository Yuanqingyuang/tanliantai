# T-0010 技术验证环境（spike）

> 状态：草案

本目录只服务 T-0010 技术选型验证，不是产品运行环境。所有数据为合成数据，密码为本地临时值。

## 一、包含内容

| 文件 | 作用 |
| --- | --- |
| [docker-compose.yml](docker-compose.yml) | 同时启动 PostgreSQL 16 / 17 / 18，用于同组测试对照 |
| [scripts/db_checks.py](scripts/db_checks.py) | NUMERIC 精度、JSONB 快照、10 并发写入、两角色越权的最小验证 |
| [scripts/ai_provider.py](scripts/ai_provider.py) | `AIProvider` 三态（mock / local / cloud）与 `AI_PROVIDER` 切换演示 |
| [scripts/model_bench.py](scripts/model_bench.py) | 本地嵌入模型四项指标实测：加载耗时、单条检索延迟、内存峰值、冷启动 |
| [requirements.txt](requirements.txt) | 数据库验证脚本依赖（psycopg） |
| [requirements-model.txt](requirements-model.txt) | 本地模型实测依赖（sentence-transformers、psutil），仅模型测试需要 |

## 二、前置条件

- Docker Desktop 已启动，`docker info` 可用。
- Python 3.12（与 CI 一致），建议用 uv 建独立虚拟环境。
- 端口 `5433` / `5434` / `5435` 未被占用。

```powershell
uv venv .venv --python 3.12
uv pip install --python .venv\Scripts\python.exe -r environment/spike/requirements.txt
```

## 三、启动与停止

```powershell
docker compose -f environment/spike/docker-compose.yml up -d
docker compose -f environment/spike/docker-compose.yml ps
docker compose -f environment/spike/docker-compose.yml down
```

| 实例 | 宿主地址 | 数据库 | 用户 | 密码 |
| --- | --- | --- | --- | --- |
| PostgreSQL 16 | `127.0.0.1:5433` | `spike` | `postgres` | `spike_local_only` |
| PostgreSQL 17 | `127.0.0.1:5434` | `spike` | `postgres` | `spike_local_only` |
| PostgreSQL 18 | `127.0.0.1:5435` | `spike` | `postgres` | `spike_local_only` |

密码只用于本地验证，不得写入任何部署配置或提交到其他环境。

## 四、运行验证

对三个版本各跑一次同一脚本：

```powershell
python environment/spike/scripts/db_checks.py --dsn "host=127.0.0.1 port=5433 user=postgres password=spike_local_only dbname=spike" --json-out results/pg16.json
python environment/spike/scripts/db_checks.py --dsn "host=127.0.0.1 port=5434 user=postgres password=spike_local_only dbname=spike" --json-out results/pg17.json
python environment/spike/scripts/db_checks.py --dsn "host=127.0.0.1 port=5435 user=postgres password=spike_local_only dbname=spike" --json-out results/pg18.json
```

退出码 `0` 表示该类测试全部通过；`1` 表示存在失败项，详见 JSON 中的 `pass` 字段。

## 五、测试内容

| 类别 | 验证点 |
| --- | --- |
| NUMERIC | `numeric(18,6)` 边界值、六位舍入、十次 0.1 求和、超范围拒绝、CSV 导出 |
| JSONB | 嵌套快照写入、字段查询、包含查询、体积、读出后指纹复算 |
| 并发 | 10 个连接各写 50 行，记录行数、错误、锁等待与连接峰值 |
| 越权 | `spike_reader` 读审计表可、写台账不可；`spike_writer` 写台账可、读审计表不可 |

脚本会重建 `spike_*` 表与两个本地角色，可重复运行。

## 五、AIProvider 三态切换

```powershell
# 默认 mock，无模型依赖
python environment/spike/scripts/ai_provider.py --text "回流焊炉后做外观检查"

# 三态对照：mock 正常返回；local / cloud 未配置时显式返回 unavailable（不静默降级）
python environment/spike/scripts/ai_provider.py --compare --text "回流焊炉后做外观检查"

# 切到本地模型
$env:AI_PROVIDER = "local"; $env:AI_LOCAL_MODEL = "D:\models\bge-m3"
python environment/spike/scripts/ai_provider.py --text "回流焊炉后做外观检查"

# 切到云端：密钥只从环境变量读，不写入仓库
$env:AI_PROVIDER = "cloud"; $env:AI_CLOUD_BASE_URL = "<OpenAI 兼容基址>"
$env:AI_CLOUD_API_KEY = "<测试密钥>"; $env:AI_CLOUD_MODEL = "<模型名>"
```

Provider 只输出候选、依据与置信度，不输出任何核算数值（规则 R2）；置信度仅用于排序。

## 六、本地模型实测

模型权重约 2.2 GB，**不进仓库**，按需下载到仓库之外：

```powershell
pip install -r environment/spike/requirements-model.txt
modelscope download --model BAAI/bge-m3 --local_dir D:\models\bge-m3

python environment/spike/scripts/model_bench.py --model-dir D:\models\bge-m3 --label bge-m3 --json-out results/model-bge-m3.json
```

脚本跑 100 条**合成文本**，输出四项数字：模型加载耗时、单条编码/检索延迟（中位、p95、最大）、进程内存峰值（含加载与编码）、冷启动（含解释器与库导入的派生进程墙钟时间）。

阈值（初始参考值）：单条编码 ≤ 500 ms、内存 ≤ 2.5 GB、冷启动 ≤ 10 s。换机器跑出的数字只作备注，阈值判定以基准机为准。

回退模型把 `--model-dir` 指向 m3e 目录即可，脚本不变。

## 七、清理

```powershell
docker compose -f environment/spike/docker-compose.yml down -v
```

`-v` 会删除三个测试数据卷，仅在本目录的临时验证场景使用。模型目录在仓库外，自行决定是否删除。
