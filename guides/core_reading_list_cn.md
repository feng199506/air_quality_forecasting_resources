# 核心阅读

近五年优先，经典单列。路径相对 `/root/air_quality_forecasting_resources/`。

## 教材与官方文本

| 角色 | 编号 | 路径 |
|---|---|---|
| 气象全书 | B-01 | [`books/Stull_PracticalMeteorology_v102b_en.pdf`](../books/Stull_PracticalMeteorology_v102b_en.pdf) |
| 美国 AQI 算法 | B-03 | [`books/EPA_AQI_TechnicalAssistanceDocument_2018_en.pdf`](../books/EPA_AQI_TechnicalAssistanceDocument_2018_en.pdf) |
| 扩散轨迹手册 | B-09 | [`books/HYSPLIT_UsersGuide_en.pdf`](../books/HYSPLIT_UsersGuide_en.pdf) |
| 监管模式指南 | B-10 | [`books/EPA_AppendixW_Guideline_AirQualityModels_2024_en.pdf`](../books/EPA_AppendixW_Guideline_AirQualityModels_2024_en.pdf) |
| CMAQ 科学算法（经典） | B-06 | [`books/CMAQ_ScienceDocumentation_1999_en/`](../books/CMAQ_ScienceDocumentation_1999_en/) |
| 监测分析手册 | B-08 | [`books/Carslaw_openair_CRAN_manual_en.pdf`](../books/Carslaw_openair_CRAN_manual_en.pdf) |

WHO 2021 指导值、WRF-Chem 用户指南、Jacob 习题本轮未核验通过，不列入。

## 课程

- C-01 MIT 12.335 实验大气化学课包（zip）
- C-05 Harvard ACMG 大气化学教育页
- C-06 / C-10 EPA 与 CMAS 的 CMAQ 文档/社区
- C-07 CAMS 空气质量服务页
- C-08 AirNow AQI 基础

NASA ARSET 幻灯 403，未计入。

## 业务与机理预报（主集合）

| 编号 | 题 | 本地 PDF |
|---|---|---|
| P02-020 | NAQFC / GFS–CMAQ 72 h | [`02_targets_horizons/papers/2022_Campbell_DevelopmentEvaluationAdvancedNational_en.pdf`](../02_targets_horizons/papers/2022_Campbell_DevelopmentEvaluationAdvancedNational_en.pdf) |
| P02-021 | CAMS 区域 97 h 集合系统 | [`02_targets_horizons/papers/2025_consortium_CopernicusAtmosphereMonitoringService_en.pdf`](../02_targets_horizons/papers/2025_consortium_CopernicusAtmosphereMonitoringService_en.pdf) |
| P01-016 | CMAQ 5.3 系统更新 | [`01_domain_foundations/papers/2021_Appel_CommunityMultiscaleAirQuality_en.pdf`](../01_domain_foundations/papers/2021_Appel_CommunityMultiscaleAirQuality_en.pdf) |
| P08-007 | WRF-Chem 东地中海实时预报 | [`08_physics_hybrid/papers/2022_authors_EvaluationWRFChemModel_en.pdf`](../08_physics_hybrid/papers/2022_authors_EvaluationWRFChemModel_en.pdf) |
| P01-002 | CAMS 多模式预报校准 | [`01_domain_foundations/papers/2022_Casciaro_CalibratingCAMSEuropeanMulti_en.pdf`](../01_domain_foundations/papers/2022_Casciaro_CalibratingCAMSEuropeanMulti_en.pdf) |

支撑（再分析，非部署预报）：P01-017 CAMS reanalysis。

## 学习模型 + 官方代码（已下载）

| 编号 | 题 | PDF | 代码 |
|---|---|---|---|
| P02-001 | AirFormer 全国 72 h | [`02_targets_horizons/papers/2022_Liang_AirFormer_en.pdf`](../02_targets_horizons/papers/2022_Liang_AirFormer_en.pdf) | P-01 L1 |
| P03-001 | PM2.5-GNN / KnowAir（经典） | [`03_statistical_baselines/papers/2020_Wang_PM25GNN_en.pdf`](../03_statistical_baselines/papers/2020_Wang_PM25GNN_en.pdf) | P-03 L1 |
| P04-001 | HighAir 层次图（经典） | [`04_machine_learning/papers/2021_Chen_HighAir_en.pdf`](../04_machine_learning/papers/2021_Chen_HighAir_en.pdf) | P-05 L1 |
| P08-001 | AirPhyNet | [`08_physics_hybrid/papers/2024_Hettige_AirPhyNet_en.pdf`](../08_physics_hybrid/papers/2024_Hettige_AirPhyNet_en.pdf) | P-02 L1 |
| P08-002 | Air-DualODE | [`08_physics_hybrid/papers/2024_Tian_AirQualityPredictionPhysics_en.pdf`](../08_physics_hybrid/papers/2024_Tian_AirQualityPredictionPhysics_en.pdf) | P-04 L1 |
| P08-003 | PCDCNet | [`08_physics_hybrid/papers/2025_Wang_PCDCNet_en.pdf`](../08_physics_hybrid/papers/2025_Wang_PCDCNet_en.pdf) | P-06 L1 |
| P06-001 | AirQualityBench | [`06_spatiotemporal/papers/2026_Xu_AirQualityBench_en.pdf`](../06_spatiotemporal/papers/2026_Xu_AirQualityBench_en.pdf) | 作者仓未快照 |
| P11-001 | FuXi-Air | [`11_practical_projects/papers/2025_Geng_FuXiAir_en.pdf`](../11_practical_projects/papers/2025_Geng_FuXiAir_en.pdf) | 待全文核实代码 |

## 统计、概率与检验

- 时空 GP：P03-009、P03-010
- 分位数：P07-004
- 共形：P07-005（机制论文）；空间制图共形 P04-004 为支撑
- 代码工具：P-15 statsmodels、P-11 MAPIE、P-16 scores、P-12 MET、P-13 MONET、P-08 openair

## 阅读顺序建议

Stull 选读边界层与扩散 → B-03/S-06 分清 AQI → P02-020 或 P02-021 看业务时效 → 持续性/ARIMA 基线 → AirFormer 或 PM2.5-GNN → AirPhyNet/PCDCNet 看再分析标签 → AirQualityBench 看评测协议。
