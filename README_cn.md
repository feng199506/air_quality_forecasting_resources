# 空气质量预测资源库

独立目录：`/root/air_quality_forecasting_resources/`。覆盖统计基线、机器学习、深度学习、空间时间建模、概率预测、机理融合与工程应用。检索日 **2026-10-30**；论文五年窗口 **2021-10-30 至 2026-10-30**，必要经典单列。

本轮只收集整理：不安装依赖、不下载大型原始数据或模型权重、不运行实验、不部署、不上传 GitHub、不删除资料。

## 子方向

| 目录 | 内容 |
|---|---|
| [`01_domain_foundations/`](01_domain_foundations/) | 大气污染与气象、排放、输送、扩散、化学、监测误差 |
| [`02_targets_horizons/`](02_targets_horizons/) | PM2.5/PM10/O3/NO2/SO2/CO、AQI 与时效 |
| [`03_statistical_baselines/`](03_statistical_baselines/) | 持续性、回归、ARIMA/SARIMAX、状态空间、GPR |
| [`04_machine_learning/`](04_machine_learning/) | 树模型、提升、SVR、集成与公平对照 |
| [`05_deep_learning/`](05_deep_learning/) | RNN/LSTM/GRU、TCN、Transformer、混合结构 |
| [`06_spatiotemporal/`](06_spatiotemporal/) | 多站点、图模型、空间 GP、迁移与无监测区 |
| [`07_probabilistic_forecasting/`](07_probabilistic_forecasting/) | 分位数、区间、校准、共形、超标预警 |
| [`08_physics_hybrid/`](08_physics_hybrid/) | CTM/数值模式、后处理、同化、机理–学习融合 |
| [`09_data_quality_features/`](09_data_quality_features/) | 质量标记、缺测、气象/排放/遥感与发布时刻可得性 |
| [`10_evaluation_reproducibility/`](10_evaluation_reproducibility/) | 时间切分、滚动评测、空间留出、指标与复现 |
| [`11_practical_projects/`](11_practical_projects/) | 训练–评测–接口–更新与回退 |

论文在各目录 `papers/`。教材、课程、软件文档、项目分别在 [`books/`](books/)、[`courses/`](courses/)、[`software_docs/`](software_docs/)、[`projects/`](projects/)。

## 登记文件

- [`catalog_cn.csv`](catalog_cn.csv) 已核验条目
- [`datasets_catalog_cn.csv`](datasets_catalog_cn.csv) 官方数据与基准说明（本轮不下载原始网格/观测库）
- [`code_availability_cn.csv`](code_availability_cn.csv) 论文代码归属
- [`evaluation_audit_cn.csv`](evaluation_audit_cn.csv) 评测与泄漏检查
- [`progress_cn.csv`](progress_cn.csv) 分方向进度
- [`download_failures_cn.csv`](download_failures_cn.csv) 失败与拒收
- [`project_readiness_cn.csv`](project_readiness_cn.csv) 代码 L0/L1（本轮不执行）
- [`search_log_cn.md`](search_log_cn.md) 检索、筛选与复用说明
- [`guides/`](guides/) 学习与工程路线（中文）

独立自建文件在扩展名前标 `_cn` 或 `_en`。上游源码内部文件名保持原样。

## 指南

- [`guides/learning_path_cn.md`](guides/learning_path_cn.md)
- [`guides/methods_comparison_cn.md`](guides/methods_comparison_cn.md)
- [`guides/datasets_and_availability_cn.md`](guides/datasets_and_availability_cn.md)
- [`guides/leakage_and_evaluation_cn.md`](guides/leakage_and_evaluation_cn.md)
- [`guides/practical_pipeline_cn.md`](guides/practical_pipeline_cn.md)
- [`guides/deployment_reference_cn.md`](guides/deployment_reference_cn.md)
- [`guides/core_reading_list_cn.md`](guides/core_reading_list_cn.md)

## 完整性规则（摘要）

只计核验通过的完整资料。PDF 须可解析且正文完整。摘要/试读/残章不计。课程按完整资料包计。HTML 保存为离线页并记录范围（见各目录 `PAGES_en.txt`）。源码保留结构、许可证、`SNAPSHOT_en.txt`（含 commit）。不下载大数据集、模型权重。不绕过付费墙、登录墙或 WAF。

主集合要求真正预测**未来**空气质量。当前时刻空间估计、遥感反演、插值、历史重建和缺失填补单列为支撑。AQI 与单一污染物浓度分开登记。美国/欧洲/中国指数公式不可混用。

## 断点续跑

```bash
cd /root/air_quality_forecasting_resources
python3 -I scripts/materials_en.py status
python3 -I scripts/papers_en.py status
python3 -I scripts/materials_en.py fetch books --retry-failed
python3 -I scripts/materials_en.py fetch courses --retry-failed
python3 -I scripts/materials_en.py fetch software --retry-failed
python3 -I scripts/materials_en.py fetch projects --retry-failed
python3 -I scripts/papers_en.py download NN --retry-failed   # NN = 01..11
python3 -I scripts/build_catalog_en.py
```

已核验条目不会覆盖。工作缓存：`/root/.cache/aqf_lit/`。arXiv 与兄弟文献库共享 `arxiv.org` 锁。

## 代码等级

- **L0**：已下载快照。
- **L1**：入口、配置或依赖清单已静态核对。
- 本轮不运行，不声称复现或业务效果。
