# 实践流水线

对应完整案例类型。配置与入口来自已下载仓库的 README/脚本名，**本轮未执行**。

## 共同步骤（研究原型）

1. 明确目标：物种、单位、空间单元、时效、AQI 或浓度。
2. 只使用发报时刻可获得的观测与气象预报；再分析单独做对照实验。
3. 按时间切分；填补与标准化只在训练段拟合。
4. 先跑持续性与统计基线（P-15、P-08），再跑学习模型。
5. 分层报告时效、季节、高污染事件。
6. 保留质量标记与缺测，不要静默填满后再声称「真实监测网」。

## 单站点短期

- 数据：OpenAQ 客户端 P-09 或 EPA pyaqsapi P-10（需密钥，本轮未调用）。
- 模型：statsmodels 时序（P-15）或 LightGBM 滞后特征（P-20）。
- 评测：滚动原点；小时 MAE/RMSE。

## 多站点空间时间

| 项目 | 路径 | 入口（静态） | 数据 |
|---|---|---|---|
| AirFormer | [`projects/yoshall_AirFormer_en/`](../projects/yoshall_AirFormer_en/) | `experiments/airformer/main.py` | tiny zip 需自解压；完整数据未下载 |
| PM2.5-GNN | [`projects/shuowang_PM25_GNN_en/`](../projects/shuowang_PM25_GNN_en/) | `config.yaml` + requirements | KnowAir npy 未下载 |
| HighAir | [`projects/Friger_HighAir_en/`](../projects/Friger_HighAir_en/) | README 极短，脚本待对照源码 | 待仓库文件 |
| Air-DualODE | [`projects/decisionintelligence_AirDualODE_en/`](../projects/decisionintelligence_AirDualODE_en/) | `Run/train.py`、`Run/eval.py` + yaml | Beijing / KnowAir 需自备 |
| PCDCNet | [`projects/shuowang_PCDCNet_en/`](../projects/shuowang_PCDCNet_en/) | `scripts/train.py`、`predict.py`、`evaluate.py` | 自带 BTHSA 2017-01 样本 nc |

PCDCNet demo 是月内切分教学，不是论文基准。AirPhyNet：`main.py` + `configs.yaml` + `requirements.txt`；Google Drive 样本未下载。

## 新站点或跨城市

Air-DualODE 提供 `Run/create_graph.py` 以便换数据集建图。AirQualityBench 论文讨论真实缺测与全球协议；其 GitHub 本轮未做快照。无监测点估计是另一任务（PM2.5-GNN README 指向 SPIN），不要写成预报技能。

## 概率与超标

把点预报接到 MAPIE（P-11）或分位数模型；用 scores（P-16）算 CRPS。阈值必须与目标地区的浓度标准或 AQI 断点一致。事件样本数要报告。

## 数值模式偏差订正

输入：CAMS 或 NAQFC 预报场（S-03、S-12）+ 当时可得观测。方法：P01-002 这类多模式校准。检验：MET/METplus、MONET。不要用 ERA5 代替当时的气象预报去做「业务订正」实验。

## 缺测、延迟、传感器异常

保留质量标记（AQS、EEA e-reporting）。缺测时回退到持续性或上一次成功预报，而不是用未来观测填。AirNow 文档写明数据为初步值。openair（P-08）用于监测诊断，不是预报模型。

MGSFformer（P-07）仅有 `model1/` 模块，L0，不能当作完整流水线。
