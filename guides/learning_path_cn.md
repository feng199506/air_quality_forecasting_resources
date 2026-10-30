# 学习路线

按先修 → 目标定义 → 统计基线 → 学习模型 → 空间时间 → 概率 → 机理融合 → 工程落地。只引用本库已核验资料。

## 1. 大气与监测先修（01、教材、课程）

1. 气象与边界层：[`books/Stull_PracticalMeteorology_v102b_en.pdf`](../books/Stull_PracticalMeteorology_v102b_en.pdf)（B-01）。
2. 大气化学课包：MIT 12.335（C-01）、Harvard ACMG 教育页（C-05）。Jacob 1999 全书本轮未取得（B-04 404）。
3. 扩散与轨迹：[`books/HYSPLIT_UsersGuide_en.pdf`](../books/HYSPLIT_UsersGuide_en.pdf)（B-09，319 页）。
4. 化学输送：CMAQ 1999 科学算法（B-06）、CMAQ 5.3 系统论文（P01-016）、CMAQ 文档站（S-04，C-06，C-10）、GEOS-Chem 首页（S-05）。
5. 美国监管模式清单：Appendix W 2024（B-10）。这是许可扩散模拟，不是站点时序学习。

## 2. 先分清预测什么（02）

- **浓度**（µg m-3 或 ppb）与 **AQI** 不是同一目标。美国日 AQI：B-03 与 C-08（2018 TAD）。欧洲 AQI：S-06。中国 HJ 与 WHO 指导值本轮未取得完整 PDF，不可用美国断点代替。
- 空间单元：单站、城市、网格、个体暴露必须分列。
- 时效：分钟/小时/日；单步与多步；短临与 72 h / 97 h 业务时效。
- 读：AirFormer 72 h 全国站点（P02-001 + 项目 P-01）；NAQFC 72 h 网格（P02-020）；CAMS 区域 97 h 集合（P02-021）。

## 3. 统计基线必须先做（03）

持续性、季节持续性、线性回归、GAM、ARIMA/SARIMAX、VAR、状态空间/Kalman、GPR。库：statsmodels（项目 P-15，L1）、openair（B-08、P-08）。时空 GP 例：P03-009、P03-010。PM2.5-GNN（P03-001 + P-03）是图模型，放在基线对照链里是因为后续论文共用 KnowAir，不把它当成 ARIMA。

## 4. 机器学习与深度学习（04、05）

树模型与提升用 LightGBM 库（P-20）作工具，不是空气质量专用系统。站点树模型论文见 04 目录。深度学习从 LSTM/GRU 到 Transformer：AirFormer（P02-001 / P-01）是全国 72 h 的作者实现。MGSFformer 仓库仅有模型模块（P-07，L0），没有完整训练入口。

## 5. 空间时间（06）

多站点图、层次图（HighAir P04-001 / P-05）、跨城市迁移、无监测点。评测协议见 AirQualityBench（P06-001）。Graph WaveNet（P-17）与 AGCRN（P-18）是交通源对照实现，**不可把原论文的交通结果写成空气质量结果**。

## 6. 概率与超标（07）

分位数、区间、CRPS、覆盖、共形。工具：MAPIE（P-11）、scores（P-16）。映射型共形（P04-004）是空间估计支撑，不是未来预报。

## 7. 机理融合（08）

三条要分开：独立学习预报、模式输出后处理/偏差订正、把模式或再分析当特征。AirPhyNet（P08-001 / P-02）、Air-DualODE（P08-002 / P-04）、PCDCNet（P08-003 / P-06）。业务 CTM：WRF-Chem 实时预报评估（P08-007）、CAMS 全球系统美国评估（P08-008）。CAMS 再分析（P01-017）是事后场。

## 8. 数据与工程（09–11）

数据到达与质量：OpenAQ（S-01、P-09）、EPA AQS（S-02、P-10）、AirNow API（S-11）、EEA（S-06）。预报产品：CAMS ADS（S-03）、NAQFC 门户（S-12）。检验：METplus（S-09）、MET（P-12）、MONET（P-13）。工程论文入口：FuXi-Air（P11-001）。
