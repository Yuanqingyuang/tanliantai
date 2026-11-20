#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Brightway 备选方案最小验证脚本。

用途
    验证 Brightway 可以完全使用自建因子（不依赖 ecoinvent）完成一次确定性计算：
    登记一个自定义流、写入自定义方法、构造一条产品活动，最后核对得分。

预期输出
    score = 0.6972...（= 1.2 kWh × 0.5810）

注意
    0.5810 是**占位值**，用于验证计算链路，不代表任何真实排放因子；
    不得复制进 knowledge/emission-factors/factor-register.md。

运行
    python smoke_test.py
"""

import bw2data as bd
import bw2calc as bc

PROJECT = "chainpcf_brightway_smoke"
PLACEHOLDER_FACTOR = 0.5810  # kgCO2e/kWh，占位值，非真实因子
ACTIVITY_KWH = 1.2


def main():
    try:
        bd.projects.delete_project(PROJECT, delete_dir=True)
    except Exception:
        pass
    bd.projects.set_current(PROJECT)

    # 1) 自建因子登记为生物圈流
    bio = bd.Database("bio")
    bio.register()
    grid = bio.new_activity(
        code="EF-ELEC-NORTH-2024-PLACEHOLDER",
        name="华北电网电力（占位）",
        unit="kWh",
        type="emission",
    )
    grid.save()

    # 2) 产品活动
    db = bd.Database("demo")
    db.register()
    product = db.new_activity(code="PCBA-A", name="PCBA A", unit="pcs", type="process")
    product.save()
    product.new_exchange(input=grid, amount=ACTIVITY_KWH, type="biosphere").save()
    product.new_exchange(input=product, amount=1.0, type="production").save()

    # 3) 自定义方法承载自建因子
    method = ("CHAINPCF", "GWP", "custom")
    bd.Method(method).register()
    bd.Method(method).write([(grid.key, PLACEHOLDER_FACTOR)])

    # 4) 计算并核对
    lca = bc.LCA({product: 1}, method)
    lca.lci()
    lca.lcia()

    expected = ACTIVITY_KWH * PLACEHOLDER_FACTOR
    print("bw2data", bd.__version__, "/ bw2calc", bc.__version__)
    print("score    =", lca.score)
    print("expected =", expected)
    print("abs_diff =", abs(lca.score - expected))

    # 稀疏矩阵运算存在约 1e-8 量级的浮点误差，容差取 1e-6
    assert abs(lca.score - expected) < 1e-6, "计算结果与手算不一致"
    print("OK: Brightway 可用自建因子完成计算，未使用 ecoinvent")


if __name__ == "__main__":
    main()
