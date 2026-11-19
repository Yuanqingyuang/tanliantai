# 数据字典 V0.1

> 状态：基线确定 v1.0
> 版本：v1.0 | 日期：2026-11-20 | 关联任务：T-0011
> 依据基线：T-0004 术语/单位/公式、T-0005 PCBA-SMT 工序链、T-0007 验收指标、T-0008 案例产品基线

## 1. 版本管理

| 字段 | 说明 |
|---|---|
| 字典版本 | v1.0（语义化版本，主版本.次版本.补丁版本） |
| 发布日期 | 2026-11-20 |
| 适用范围 | MVP 阶段：单一 PCBA 产品、cradle-to-gate 边界、10 道工序 |
| 兼容性 | 与 TERM-001-glossary.md v1.0、UNIT-001-units.md v1.0、formula-register.md v1.0、acceptance-criteria.md v1.0 兼容 |

## 2. 核心实体定义

### 2.1 Product（产品实体）

| 字段名 | 中文名 | 类型 | 单位（UNIT ID） | 必填 | 质量等级 | 校验规则 | TERM 引用 | 说明 |
|---|---|---|---|---|---|---|---|---|
| product_id | 产品 ID | STRING(32) | — | 是 | P1 | 非空、唯一、格式 PCBA-XXXX-XXX | TERM-307-PRJ | 内部唯一标识 |
| product_name | 产品名称 | STRING(128) | — | 是 | P1 | 非空 | — | 如 4层 FR-4 双面贴装控制板 |
| product_code | 产品代号 | STRING(32) | — | 是 | P1 | 非空、唯一、格式 PCBA-DEMO-XXX | TERM-307-PRJ | 如 PCBA-DEMO-001 |
| layer_count | 层数 | INTEGER | — | 是 | P1 | >0、≤32 | — | 如 4 |
| thickness_mm | 板厚 | DECIMAL(5,2) | mm | 是 | P1 | >0、≤5.0 | UNIT-301-ARE | 如 1.60 |
| width_mm | 板宽 | DECIMAL(7,2) | mm | 是 | P1 | >0 | UNIT-301-ARE | 单板宽度 |
| height_mm | 板高 | DECIMAL(7,2) | mm | 是 | P1 | >0 | UNIT-301-ARE | 单板高度 |
| panelization | 拼板方式 | STRING(16) | — | 是 | P1 | 正则 ^\d+x\d+$ | — | 如 2x2 |
| surface_finish | 表面处理 | ENUM | — | 是 | P1 | 枚举值见下 | — | HASL/ENIG/OSP/沉锡 |
| min_line_width_mm | 最小线宽 | DECIMAL(5,2) | mm | 否 | P2 | >0 | UNIT-301-ARE | 如 0.15 |
| min_hole_mm | 最小孔径 | DECIMAL(5,2) | mm | 否 | P2 | >0 | UNIT-301-ARE | 如 0.30 |
| functional_unit | 功能单位 | ENUM | — | 是 | P1 | 枚举：piece/m2/kpoints | TERM-005-BAS | 如 piece |
| fu_qty_per_unit | 功能单位换算量 | DECIMAL(10,4) | 视 FU | 是 | P1 | >0 | TERM-005-BAS | 如 1.0 (piece) / 0.0096 (m2) |
| system_boundary | 系统边界 | ENUM | — | 是 | P1 | 枚举：cradle-to-gate/cradle-to-grave | TERM-004-BAS | 如 cradle-to-gate |
| lifecycle_stages | 纳入生命周期阶段 | ARRAY[ENUM] | — | 是 | P1 | 子集：raw_material/transport/manufacturing/use/eol | TERM-007-BAS | 如 [raw_material, transport, manufacturing] |
| version | 实体版本 | STRING(16) | — | 是 | P1 | 语义化版本 | — | v1.0 |
| created_at | 创建时间 | TIMESTAMP | — | 是 | P1 | 自动生成 | — | |
| updated_at | 更新时间 | TIMESTAMP | — | 是 | P1 | 自动更新 | — | |

### 2.2 BOMItem（物料清单项）

| 字段名 | 中文名 | 类型 | 单位（UNIT ID） | 必填 | 质量等级 | 校验规则 | TERM 引用 | 说明 |
|---|---|---|---|---|---|---|---|---|
| bom_item_id | BOM 项 ID | STRING(32) | — | 是 | P1 | 非空、唯一 | — | |
| product_id | 关联产品 ID | STRING(32) | — | 是 | P1 | 外键引用 Product.product_id | TERM-307-PRJ | |
| material_id | 物料内部编码 | STRING(64) | — | 是 | P1 | 非空 | — | 企业内部编码 |
| supplier_pn | 供应商料号 | STRING(64) | — | 是 | P1 | 非空 | — | |
| description | 物料描述 | STRING(256) | — | 是 | P1 | 非空 | — | |
| category | 物料类别 | ENUM | — | 是 | P1 | 枚举：IC/RESISTOR/CAPACITOR/CONNECTOR/PCB_BASE/SOLDER_PASTE/FLUX/CLEANING_AGENT/PACKAGING | — | 物料分类 |
| qty_per_board | 单板用量 | DECIMAL(12,4) | 视类别 | 是 | P1 | >0 | UNIT-101/102/202/301/401 | 单位随类别变化 |
| loss_rate | 损耗率 | DECIMAL(5,4) | % | 是 | P2 | 0~1.0 | — | 如 0.0200 |
| unit_mass_kg | 单件质量 | DECIMAL(12,6) | kg | 否 | P1 | >0 | UNIT-101-MAS | IC/大件必填 |
| unit_area_m2 | 单件面积 | DECIMAL(12,6) | m² | 否 | P1 | >0 | UNIT-301-ARE | PCB基板必填 |
| supplier_name | 供应商名称 | STRING(128) | — | 是 | P1 | 非空 | — | |
| supplier_region | 供应商地区 | STRING(64) | — | 是 | P1 | 非空（用于运输距离） | — | 省/市级 |
| ef_id | 排放因子 ID | STRING(32) | — | 是 | P1 | 外键引用 EmissionFactor.ef_id | TERM-102-CAL | |
| ef_source | 因子来源等级 | ENUM | — | 是 | P1 | 枚举：P1/P2/P3 | TERM-113/114-CAL | P1=实测、P2=数据库、P3=估算 |
| ef_region | 因子适用区域 | STRING(32) | — | 是 | P1 | 非空 | TERM-102-CAL | 如 CN/华东/华南 |
| ef_year | 因子数据年份 | INTEGER | 年 | 是 | P1 | 2020~当前年份 | TERM-102-CAL | 如 2024 |
| remarks | 备注 | STRING(512) | — | 否 | P3 | — | — | 替代料、特殊要求等 |
| version | 实体版本 | STRING(16) | — | 是 | P1 | 语义化版本 | — | v1.0 |
| created_at | 创建时间 | TIMESTAMP | — | 是 | P1 | 自动生成 | — | |
| updated_at | 更新时间 | TIMESTAMP | — | 是 | P1 | 自动更新 | — | |

### 2.3 Process（工序实体）

| 字段名 | 中文名 | 类型 | 单位（UNIT ID） | 必填 | 质量等级 | 校验规则 | TERM 引用 | 说明 |
|---|---|---|---|---|---|---|---|---|
| process_id | 工序 ID | STRING(16) | — | 是 | P1 | 格式 PCBA-\d{2}-[A-Z]{3} | TERM-307-PRJ | 如 PCBA-04-SMT |
| process_name | 工序名称 | STRING(64) | — | 是 | P1 | 非空 | — | 如 贴片 SMT |
| process_order | 工序顺序 | INTEGER | — | 是 | P1 | >0、唯一 | — | 1~12 |
| equipment_type | 典型设备类型 | STRING(128) | — | 是 | P1 | 非空 | — | 如 高速贴片机 |
| energy_types | 涉及能源类型 | ARRAY[ENUM] | — | 是 | P1 | 子集：electricity/gas/steam/compressed_air/nitrogen | UNIT-001/002/004/005-ENG | |
| material_types | 涉及物耗类型 | ARRAY[ENUM] | — | 是 | P1 | 子集：solder_paste/flux/cleaning_agent/packaging | — | |
| is_core | 是否核心工序 | BOOLEAN | — | 是 | P1 | — | — | SMT/RFL 为 true |
| included | 是否纳入核算 | BOOLEAN | — | 是 | P1 | — | — | false 则排除 |
| allocation_method_id | 分摊方法 ID | STRING(16) | — | 否 | P1 | 引用 F-AL-xxx | F-AL-001~004 | 仅公用工程相关工序填 |
| version | 实体版本 | STRING(16) | — | 是 | P1 | 语义化版本 | — | v1.0 |
| created_at | 创建时间 | TIMESTAMP | — | 是 | P1 | 自动生成 | — | |
| updated_at | 更新时间 | TIMESTAMP | — | 是 | P1 | 自动更新 | — | |

### 2.4 ActivityData（活动数据实体）

| 字段名 | 中文名 | 类型 | 单位（UNIT ID） | 必填 | 质量等级 | 校验规则 | TERM 引用 | 说明 |
|---|---|---|---|---|---|---|---|---|
| activity_id | 活动数据 ID | STRING(32) | — | 是 | P1 | 非空、唯一 | TERM-101-CAL | |
| product_id | 关联产品 ID | STRING(32) | — | 是 | P1 | 外键 Product.product_id | TERM-307-PRJ | |
| process_id | 关联工序 ID | STRING(16) | — | 是 | P1 | 外键 Process.process_id | TERM-307-PRJ | |
| period_start | 核算期开始 | DATE | — | 是 | P1 | — | TERM-101-CAL | 核算期间 |
| period_end | 核算期结束 | DATE | — | 是 | P1 | ≥ period_start | TERM-101-CAL | |
| quantity | 活动量值 | DECIMAL(18,6) | 视类型 | 是 | P1 | >0 | TERM-101-CAL | 如 1500.00 |
| unit | 活动量单位 | STRING(16) | — | 是 | P1 | 必与 UNIT-xxx 标准符号一致 | UNIT-xxx | 如 kWh/h/kg/Nm3 |
| quantity_raw | 原始活动量值 | DECIMAL(18,6) | 原始单位 | 否 | P2 | — | — | 保留原始单位值 |
| unit_raw | 原始单位 | STRING(16) | — | 否 | P2 | — | — | 如 度/吨/立方米 |
| conversion_factor | 换算系数 | DECIMAL(18,6) | — | 否 | P2 | >0 | UNIT-xxx | 原始→标准单位 |
| source | 数据来源 | ENUM | — | 是 | P1 | 枚举：meter/mes/manual/estimate | TERM-113/114-CAL | P1=实测、P2=系统、P3=估算 |
| quality_grade | 质量等级 | ENUM | — | 是 | P1 | 枚举：P1/P2/P3 | TERM-106-CAL | |
| gap_flag | 缺口标记 | BOOLEAN | — | 是 | P1 | true=有缺口 | TERM-305-PRJ | |
| gap_reason | 缺口原因 | STRING(256) | — | 否 | P2 | gap_flag=true 时必填 | TERM-305-PRJ | |
| version | 实体版本 | STRING(16) | — | 是 | P1 | 语义化版本 | — | v1.0 |
| created_at | 创建时间 | TIMESTAMP | — | 是 | P1 | 自动生成 | — | |
| updated_at | 更新时间 | TIMESTAMP | — | 是 | P1 | 自动更新 | — | |

### 2.5 EmissionFactor（排放因子实体）

| 字段名 | 中文名 | 类型 | 单位（UNIT ID） | 必填 | 质量等级 | 校验规则 | TERM 引用 | 说明 |
|---|---|---|---|---|---|---|---|---|
| ef_id | 因子 ID | STRING(32) | — | 是 | P1 | 非空、唯一 | TERM-102-CAL | |
| name | 因子名称 | STRING(128) | — | 是 | P1 | 非空 | — | 如 华东电网2024年平均因子 |
| category | 因子类别 | ENUM | — | 是 | P1 | 枚举：electricity/gas/steam/compressed_air/material/transport | — | |
| sub_category | 子类别 | STRING(64) | — | 否 | P2 | — | — | 如 华东/华南/煤电/气电 |
| value | 因子数值 | DECIMAL(18,6) | kgCO2e/单位 | 是 | P1 | >0 | TERM-102-CAL | |
| unit | 因子单位 | STRING(16) | — | 是 | P1 | 必与 UNIT-xxx 标准符号一致 | UNIT-xxx | 如 kgCO2e/kWh |
| region | 适用区域 | STRING(32) | — | 是 | P1 | 非空 | TERM-102-CAL | 如 CN/华东/华南 |
| year | 数据年份 | INTEGER | 年 | 是 | P1 | 2020~当前年份 | TERM-102-CAL | 如 2024 |
| source | 来源 | ENUM | — | 是 | P1 | 枚举：grid_avg/clcd/ecoinvent/supplier/measured | TERM-113/114-CAL | |
| source_detail | 来源详情 | STRING(256) | — | 是 | P1 | 具体文献/数据库版本/供应商名 | TERM-113/114-CAL | 如 CLCD v1.2/供应商实测报告 |
| gwp_version | GWP 版本 | STRING(16) | — | 是 | P1 | 如 IPCC AR6 100a | TERM-103-CAL | |
| quality_grade | 质量等级 | ENUM | — | 是 | P1 | 枚举：P1/P2/P3 | TERM-106-CAL | |
| uncertainty | 不确定度 | DECIMAL(5,2) | % | 否 | P2 | 0~100 | — | 如 15.00 |
| version | 实体版本 | STRING(16) | — | 是 | P1 | 语义化版本 | — | v1.0 |
| created_at | 创建时间 | TIMESTAMP | — | 是 | P1 | 自动生成 | — | |
| updated_at | 更新时间 | TIMESTAMP | — | 是 | P1 | 自动更新 | — | |

### 2.6 CalculationRun（核算运行实体）

| 字段名 | 中文名 | 类型 | 单位（UNIT ID） | 必填 | 质量等级 | 校验规则 | TERM 引用 | 说明 |
|---|---|---|---|---|---|---|---|---|
| run_id | 运行 ID | STRING(32) | — | 是 | P1 | 非空、唯一 | TERM-304-PRJ | 结果指纹输入 |
| product_id | 关联产品 ID | STRING(32) | — | 是 | P1 | 外键 Product.product_id | TERM-307-PRJ | |
| run_type | 运行类型 | ENUM | — | 是 | P1 | 枚举：formal/trial/sensitivity/audit | — | 正式/试算/敏感性/审计 |
| rule_version | 规则版本 | STRING(16) | — | 是 | P1 | 引用 formula-register 版本 | F-xxx | 如 v1.0 |
| factor_version | 因子版本快照 | STRING(16) | — | 是 | P1 | 因子表版本哈希 | TERM-102-CAL | |
| boundary_version | 边界版本 | STRING(16) | — | 是 | P1 | 系统边界版本 | TERM-004-BAS | 如 v1.0 |
| total_emission_kgco2e | 总排放量 | DECIMAL(18,6) | kgCO2e | 是 | P1 | ≥0 | UNIT-501-EQU | F-CF-006 结果 |
| fu_emission_kgco2e | 单位产品排放 | DECIMAL(18,6) | kgCO2e/FU | 是 | P1 | ≥0 | UNIT-502-EQU | F-CF-007 结果 |
| fingerprint | 结果指纹 | STRING(64) | — | 是 | P1 | SHA-256(输入快照+规则版本+结果) | TERM-304-PRJ | |
| input_snapshot_hash | 输入快照哈希 | STRING(64) | — | 是 | P1 | SHA-256(所有输入实体) | TERM-304-PRJ | |
| status | 运行状态 | ENUM | — | 是 | P1 | 枚举：success/failed/partial | — | |
| gap_count | 缺口数量 | INTEGER | — | 是 | P1 | ≥0 | TERM-305-PRJ | |
| created_at | 创建时间 | TIMESTAMP | — | 是 | P1 | 自动生成 | — | |
| created_by | 执行人 | STRING(64) | — | 是 | P1 | 非空 | — | |
| version | 实体版本 | STRING(16) | — | 是 | P1 | 语义化版本 | — | v1.0 |

### 2.7 DataPackage（数据包实体）

| 字段名 | 中文名 | 类型 | 单位（UNIT ID） | 必填 | 质量等级 | 校验规则 | TERM 引用 | 说明 |
|---|---|---|---|---|---|---|---|---|
| package_id | 数据包 ID | STRING(32) | — | 是 | P1 | 非空、唯一 | TERM-303-PRJ | |
| run_id | 关联运行 ID | STRING(32) | — | 是 | P1 | 外键 CalculationRun.run_id | TERM-304-PRJ | |
| package_version | 数据包版本 | STRING(16) | — | 是 | P1 | 语义化版本 | — | v1.0 |
| schema_version | 结构版本 | STRING(16) | — | 是 | P1 | 如 v1.0 | — | |
| results | 结果集 | JSON | — | 是 | P1 | 含 total_emission, fu_emission, breakdown | TERM-303-PRJ | |
| evidence | 证据链 | JSON | — | 是 | P1 | 含因子来源、活动数据来源、分摊方法 | TERM-303-PRJ | |
| gaps | 缺口清单 | JSON | — | 是 | P1 | 含字段、原因、影响评估 | TERM-305-PRJ | |
| audit_trail | 审计链 | JSON | — | 是 | P1 | 含人/时间/规则/因子版本/操作 | TERM-303-PRJ | |
| checksum | 校验和 | STRING(64) | — | 是 | P1 | SHA-256(全包内容) | TERM-304-PRJ | 防篡改 |
| exported_at | 导出时间 | TIMESTAMP | — | 是 | P1 | 自动生成 | — | |
| exported_by | 导出人 | STRING(64) | — | 是 | P1 | 非空 | — | |
| version | 实体版本 | STRING(16) | — | 是 | P1 | 语义化版本 | — | v1.0 |

## 3. 枚举值定义

### 3.1 物料类别

| 代码 | 中文名 | 说明 |
|---|---|---|
| IC | 集成电路 | MCU、存储器、电源管理等 |
| RESISTOR | 电阻 | 贴片电阻、排阻 |
| CAPACITOR | 电容 | 陶瓷电容、钽电容、电解电容 |
| CONNECTOR | 连接器 | 排针、排母、FPC连接器 |
| PCB_BASE | PCB 基板 | FR-4、铝基板等 |
| SOLDER_PASTE | 锡膏 | 含铅/无铅 |
| FLUX | 助焊剂 | 免洗/水洗 |
| CLEANING_AGENT | 清洗剂 | 酒精/专用清洗剂 |
| PACKAGING | 包装材料 | 吸塑盘、防静电袋、珍珠棉 |

### 3.2 质量等级

| 代码 | 含义 | 说明 |
|---|---|---|
| P1 | 优先级最高 | 企业实测、实时监测、带校验记录 |
| P2 | 优先级次之 | 数据库值、行业平均、供应商提供 |
| P3 | 优先级最低 | 估算值、行业经验值、工程判断 |

### 3.3 因子来源等级

| 代码 | 含义 | 典型来源 |
|---|---|---|
| P1 | 一手数据 | 企业实测、供应商实测报告、实时监测 |
| P2 | 二手数据 | CLCD、Ecoinvent、行业数据库、政府发布因子 |
| P3 | 三手数据 | 文献估算、工程经验、类比法 |

### 3.4 系统边界

| 代码 | 含义 | 纳入阶段 |
|---|---|---|
| cradle-to-gate | 摇篮到大门 | 原料获取 + 来料运输 + 生产制造 |
| cradle-to-grave | 摇篮到坟墓 | 全生命周期（含使用、报废） |

### 3.5 生命周期阶段

| 代码 | 中文名 |
|---|---|
| raw_material | 原料获取 |
| transport | 运输 |
| manufacturing | 生产制造 |
| use | 使用 |
| eol | 报废处理 |

### 3.6 表面处理

| 代码 | 中文名 |
|---|---|
| HASL | 热风整平 |
| ENIG | 沉金 |
| OSP | 有机保焊膜 |
| IMMERSION_TIN | 沉锡 |

### 3.7 运行类型

| 代码 | 中文名 |
|---|---|
| formal | 正式核算 |
| trial | 试算 |
| sensitivity | 敏感性分析 |
| audit | 审计复算 |

## 4. 校验规则汇总

| 规则 ID | 规则描述 | 涉及实体 | 触发条件 | 动作 |
|---|---|---|---|---|
| VR-001 | 单位一致性校验 | ActivityData ↔ EmissionFactor | ActivityData.unit ≠ EmissionFactor.unit | 报错拒绝计算 |
| VR-002 | 质量等级完整性 | 所有实体 | quality_grade 为空 | 报错 |
| VR-003 | 必填字段非空 | 所有实体 | 必填字段为空 | 报错 |
| VR-004 | 外键引用完整性 | 所有实体 | 外键引用不存在 | 报错 |
| VR-005 | 版本一致性 | CalculationRun | rule_version 与 formula-register 不符 | 警告 |
| VR-006 | 指纹一致性 | DataPackage | checksum 校验失败 | 报错拒绝导入 |
| VR-007 | 质量等级一致性 | ActivityData ↔ EmissionFactor | 等级差异 >1 级 | 警告 |

## 5. 变更记录

| 版本 | 日期 | 变更人 | 变更摘要 |
|---|---|---|---|
| v1.0 | 2026-11-20 | R2知识库维护 | 基线确定：7 个核心实体、30+ 字段、7 类枚举、7 条校验规则，全引用 TERM/UNIT/F- 标准 ID |
