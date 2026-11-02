#!/usr/bin/env python3
"""T-0010 数据库最小验证：NUMERIC 精度 / JSONB 快照 / 并发 / 越权。

只使用合成数据，不接触企业真实数据。每个测试都在独立表上执行，
可对 PostgreSQL 16/17/18 重复运行。

用法：
    python environment/spike/scripts/db_checks.py --dsn "host=127.0.0.1 port=5433 user=postgres password=spike_local_only dbname=spike"
    python environment/spike/scripts/db_checks.py --json-out results/pg16.json

输出为 JSON，便于跨版本对比。
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal

import psycopg
from psycopg import sql

DEFAULT_DSN = os.environ.get(
    "T0010_DSN",
    "host=127.0.0.1 port=5433 user=postgres password=spike_local_only dbname=spike",
)

# NUMERIC(18,6)：整数位最多 12 位，小数 6 位
NUMERIC_CASES = [
    ("min_scale", Decimal("0.000001")),
    ("max_value", Decimal("999999999999.999999")),
    ("negative", Decimal("-123456789012.123456")),
    ("round_half_up", Decimal("1.0000005")),
    ("tenth", Decimal("0.1")),
]

EXPECTED_EXPORT = {
    "min_scale": "0.000001",
    "max_value": "999999999999.999999",
    "negative": "-123456789012.123456",
    "round_half_up": "1.000001",
    "tenth": "0.100000",
}

SYNTHETIC_SNAPSHOT = {
    "schema_version": "spike-1",
    "meta": {
        "product_code": "SYNTH-DEMO-001",
        "line": "SMT-A",
        "batch": "B-001",
        "note": "合成数据，仅用于结构验证",
    },
    "items": [
        {"seq": 1, "process": "SMT-01", "qty": 120, "unit": "pcs", "factor_id": "TBD"},
        {"seq": 2, "process": "SMT-02", "qty": 80, "unit": "pcs", "factor_id": "TBD"},
        {"seq": 3, "process": "REFLOW-01", "qty": 2, "unit": "kWh", "factor_id": "TBD"},
    ],
    "totals": {"a": 0.1, "b": 0.2},
}


def canonical(value) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def fingerprint(value) -> str:
    import hashlib

    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def mask_dsn(dsn: str) -> str:
    return " ".join(
        "password=***" if part.startswith("password=") else part for part in dsn.split()
    )


def numeric_suite(conn) -> dict:
    with conn.transaction():
        conn.execute("DROP TABLE IF EXISTS spike_numeric")
        conn.execute(
            "CREATE TABLE spike_numeric ("
            " id serial PRIMARY KEY,"
            " label text NOT NULL,"
            " amount numeric(18,6) NOT NULL)"
        )
        for label, value in NUMERIC_CASES:
            conn.execute(
                "INSERT INTO spike_numeric (label, amount) VALUES (%s, %s)",
                (label, value),
            )

    stored = dict(
        conn.execute("SELECT label, amount FROM spike_numeric").fetchall()
    )
    rounding_ok = stored["round_half_up"] == Decimal("1.000001")

    # 0.1 累加十次：NUMERIC 应精确等于 1，浮点会留下误差
    with conn.transaction():
        conn.execute("DELETE FROM spike_numeric WHERE label = 'tenth'")
        for _ in range(10):
            conn.execute(
                "INSERT INTO spike_numeric (label, amount) VALUES ('tenth', 0.1)"
            )
        numeric_sum = conn.execute(
            "SELECT sum(amount) FROM spike_numeric WHERE label = 'tenth'"
        ).fetchone()[0]

    float_sum = 0.0
    for _ in range(10):
        float_sum += 0.1

    overflow_rejected = False
    overflow_error = ""
    try:
        with conn.transaction():
            conn.execute(
                "INSERT INTO spike_numeric (label, amount) VALUES ('overflow', %s)",
                (Decimal("1234567890123.000000"),),
            )
    except psycopg.errors.NumericValueOutOfRange as exc:
        overflow_rejected = True
        overflow_error = str(exc).strip().splitlines()[0]

    export_rows = []
    with conn.cursor() as cur:
        with cur.copy(
            "COPY (SELECT label, amount FROM spike_numeric"
            " WHERE label <> 'tenth' ORDER BY id) TO STDOUT WITH CSV HEADER"
        ) as copy:
            chunks = []
            for chunk in copy:
                chunks.append(bytes(chunk))
    text = b"".join(chunks).decode("utf-8")
    export_rows = list(csv.DictReader(io.StringIO(text)))

    export_ok = all(
        row["amount"] == EXPECTED_EXPORT[row["label"]] for row in export_rows
    )

    return {
        "stored": {key: str(value) for key, value in stored.items() if key != "tenth"},
        "round_half_up_ok": rounding_ok,
        "numeric_sum": str(numeric_sum),
        "numeric_sum_exact_one": numeric_sum == Decimal("1.000000"),
        "python_float_sum_repr": repr(float_sum),
        "python_float_error": repr(Decimal("1") - Decimal(float_sum)),
        "overflow_rejected": overflow_rejected,
        "overflow_error": overflow_error,
        "csv_export": export_rows,
        "csv_export_ok": export_ok,
        "pass": bool(
            rounding_ok
            and numeric_sum == Decimal("1.000000")
            and overflow_rejected
            and export_ok
        ),
    }


def jsonb_suite(conn) -> dict:
    before = fingerprint(SYNTHETIC_SNAPSHOT)
    payload = json.dumps(SYNTHETIC_SNAPSHOT, ensure_ascii=False)

    with conn.transaction():
        conn.execute("DROP TABLE IF EXISTS spike_snapshot")
        conn.execute(
            "CREATE TABLE spike_snapshot ("
            " id bigserial PRIMARY KEY,"
            " run_label text NOT NULL,"
            " snapshot jsonb NOT NULL)"
        )
        conn.execute(
            "INSERT INTO spike_snapshot (run_label, snapshot) VALUES ('spike', %s::jsonb)",
            (payload,),
        )

    read_back = conn.execute(
        "SELECT snapshot FROM spike_snapshot WHERE run_label = 'spike'"
    ).fetchone()[0]
    after = fingerprint(read_back)

    field_value = conn.execute(
        "SELECT snapshot #>> '{meta,line}' FROM spike_snapshot WHERE run_label = 'spike'"
    ).fetchone()[0]
    contained = conn.execute(
        "SELECT snapshot @> %s::jsonb FROM spike_snapshot WHERE run_label = 'spike'",
        ('{"meta":{"line":"SMT-A"}}',),
    ).fetchone()[0]
    item_count = conn.execute(
        "SELECT jsonb_array_length(snapshot->'items') FROM spike_snapshot WHERE run_label = 'spike'"
    ).fetchone()[0]
    total_sum = conn.execute(
        "SELECT (snapshot->'totals'->>'a')::numeric + (snapshot->'totals'->>'b')::numeric"
        " FROM spike_snapshot WHERE run_label = 'spike'"
    ).fetchone()[0]
    sizes = conn.execute(
        "SELECT pg_column_size(snapshot), pg_column_size(snapshot::text),"
        " pg_total_relation_size('spike_snapshot')"
        " FROM spike_snapshot WHERE run_label = 'spike'"
    ).fetchone()

    return {
        "fingerprint_before": before,
        "fingerprint_after": after,
        "fingerprint_match": before == after,
        "field_query_line": field_value,
        "containment_ok": bool(contained),
        "item_count": item_count,
        "jsonb_numeric_sum": str(total_sum),
        "jsonb_numeric_sum_is_0_3": total_sum == Decimal("0.3"),
        "size": {
            "jsonb_bytes": sizes[0],
            "text_bytes": sizes[1],
            "table_total_bytes": sizes[2],
        },
        "pass": bool(before == after and contained and item_count == 3 and total_sum == Decimal("0.3")),
    }


def concurrency_suite(conn, dsn: str, workers: int = 10, inserts_per_worker: int = 50) -> dict:
    with conn.transaction():
        conn.execute("DROP TABLE IF EXISTS spike_concurrency")
        conn.execute(
            "CREATE TABLE spike_concurrency ("
            " id bigserial PRIMARY KEY,"
            " worker int NOT NULL,"
            " seq int NOT NULL,"
            " payload text NOT NULL,"
            " created_at timestamptz NOT NULL DEFAULT now())"
        )

    max_connections = int(
        conn.execute("SHOW max_connections").fetchone()[0]
    )
    baseline_connections = conn.execute(
        "SELECT count(*) FROM pg_stat_activity WHERE datname = current_database()"
    ).fetchone()[0]

    results = []
    lock_samples = []
    connection_samples = []

    def worker(index: int) -> dict:
        started = time.perf_counter()
        errors = []
        count = 0
        try:
            with psycopg.connect(dsn, autocommit=True) as own:
                for seq in range(inserts_per_worker):
                    own.execute(
                        "INSERT INTO spike_concurrency (worker, seq, payload)"
                        " VALUES (%s, %s, %s)",
                        (index, seq, f"synthetic-{index}-{seq}"),
                    )
                    count += 1
        except Exception as exc:  # noqa: BLE001 - 记录后继续汇总
            errors.append(f"{type(exc).__name__}: {exc}")
        return {
            "worker": index,
            "inserts": count,
            "errors": errors,
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
        }

    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(worker, index) for index in range(workers)]
        while not all(future.done() for future in futures):
            try:
                active, waiting = conn.execute(
                    "SELECT count(*), count(*) FILTER (WHERE wait_event_type = 'Lock')"
                    " FROM pg_stat_activity WHERE datname = current_database()"
                ).fetchone()
                connection_samples.append(active)
                lock_samples.append(waiting)
            except psycopg.Error:
                pass
            time.sleep(0.02)
        results = [future.result() for future in futures]

    total_rows = conn.execute("SELECT count(*) FROM spike_concurrency").fetchone()[0]
    peak_connections = max(connection_samples) if connection_samples else baseline_connections
    errors = [error for result in results for error in result["errors"]]
    worker_times = [result["elapsed_ms"] for result in results]

    return {
        "workers": workers,
        "inserts_per_worker": inserts_per_worker,
        "expected_rows": workers * inserts_per_worker,
        "actual_rows": total_rows,
        "errors": errors,
        "max_connections": max_connections,
        "baseline_connections": baseline_connections,
        "peak_connections": peak_connections,
        "peak_lock_waiting": max(lock_samples) if lock_samples else 0,
        "lock_samples": len(lock_samples),
        "worker_elapsed_ms": {
            "min": min(worker_times),
            "median": statistics.median(worker_times),
            "max": max(worker_times),
        },
        "pass": bool(total_rows == workers * inserts_per_worker and not errors),
    }


def privilege_suite(conn) -> dict:
    with conn.transaction():
        conn.execute("DROP TABLE IF EXISTS spike_ledger")
        conn.execute("DROP TABLE IF EXISTS spike_audit")
        conn.execute(
            "CREATE TABLE spike_ledger ("
            " id bigserial PRIMARY KEY,"
            " owner_role text NOT NULL,"
            " amount numeric(18,6) NOT NULL)"
        )
        conn.execute(
            "CREATE TABLE spike_audit ("
            " id bigserial PRIMARY KEY,"
            " event text NOT NULL)"
        )

    for role in ("spike_reader", "spike_writer"):
        exists = conn.execute(
            "SELECT 1 FROM pg_roles WHERE rolname = %s", (role,)
        ).fetchone()
        if exists:
            conn.execute(
                sql.SQL("ALTER ROLE {} WITH LOGIN PASSWORD {}").format(
                    sql.Identifier(role), sql.Literal(role + "_pw")
                )
            )
        else:
            conn.execute(
                sql.SQL("CREATE ROLE {} LOGIN PASSWORD {}").format(
                    sql.Identifier(role), sql.Literal(role + "_pw")
                )
            )

    conn.execute("GRANT SELECT, INSERT ON spike_ledger TO spike_writer")
    conn.execute(
        "GRANT USAGE, SELECT ON SEQUENCE spike_ledger_id_seq TO spike_writer"
    )
    conn.execute("GRANT SELECT ON spike_audit TO spike_reader")
    conn.execute("INSERT INTO spike_audit (event) VALUES ('synthetic event')")

    host = conn.info.host or "127.0.0.1"
    port = conn.info.port or 5432
    dbname = conn.info.dbname or "spike"

    checks = {}

    try:
        with psycopg.connect(
            host=host, port=port, user="spike_reader", password="spike_reader_pw",
            dbname=dbname, autocommit=True,
        ) as reader:
            reader.execute("SELECT count(*) FROM spike_audit").fetchone()
            checks["reader_can_read_audit"] = True
            try:
                reader.execute(
                    "INSERT INTO spike_ledger (owner_role, amount) VALUES ('reader', 1.0)"
                )
                checks["reader_insert_ledger_denied"] = False
            except psycopg.errors.InsufficientPrivilege as exc:
                checks["reader_insert_ledger_denied"] = True
                checks["reader_denied_message"] = str(exc).strip().splitlines()[0]
    except Exception as exc:  # noqa: BLE001
        checks["reader_error"] = f"{type(exc).__name__}: {exc}"

    try:
        with psycopg.connect(
            host=host, port=port, user="spike_writer", password="spike_writer_pw",
            dbname=dbname, autocommit=True,
        ) as writer:
            writer.execute(
                "INSERT INTO spike_ledger (owner_role, amount) VALUES ('writer', 1.0)"
            )
            checks["writer_can_insert_ledger"] = True
            try:
                writer.execute("SELECT count(*) FROM spike_audit").fetchone()
                checks["writer_read_audit_denied"] = False
            except psycopg.errors.InsufficientPrivilege as exc:
                checks["writer_read_audit_denied"] = True
                checks["writer_denied_message"] = str(exc).strip().splitlines()[0]
    except Exception as exc:  # noqa: BLE001
        checks["writer_error"] = f"{type(exc).__name__}: {exc}"

    checks["pass"] = bool(
        checks.get("reader_can_read_audit")
        and checks.get("reader_insert_ledger_denied")
        and checks.get("writer_can_insert_ledger")
        and checks.get("writer_read_audit_denied")
    )
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="T-0010 PostgreSQL 最小验证")
    parser.add_argument("--dsn", default=DEFAULT_DSN)
    parser.add_argument("--json-out", default="")
    args = parser.parse_args()

    started_at = datetime.now(timezone.utc).isoformat()
    started = time.perf_counter()

    with psycopg.connect(args.dsn, autocommit=True) as conn:
        version = conn.execute("SHOW server_version").fetchone()[0]
        version_num = conn.execute("SHOW server_version_num").fetchone()[0]
        report = {
            "run": {
                "started_at": started_at,
                "dsn": mask_dsn(args.dsn),
                "python": sys.version.split()[0],
            },
            "server": {"version": version, "version_num": version_num},
            "numeric": numeric_suite(conn),
            "jsonb": jsonb_suite(conn),
            "concurrency": concurrency_suite(conn, args.dsn),
            "privilege": privilege_suite(conn),
        }
        report["run"]["duration_ms"] = round((time.perf_counter() - started) * 1000, 2)
        report["pass"] = all(
            report[section]["pass"]
            for section in ("numeric", "jsonb", "concurrency", "privilege")
        )

    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as handle:
            handle.write(output + "\n")
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
