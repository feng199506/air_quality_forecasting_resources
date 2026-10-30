# 检索与筛选日志（空气质量预测）

检索日：2026-10-30。论文五年窗口：2021-10-30 至 2026-10-30。必要经典单列，不凑数。

## 渠道

同时检索环境/大气（Copernicus GMD/ACP 开放获取）、统计与机器学习（arXiv cs.LG / stat / physics.ao-ph 交叉查询）。查询种子：[`scripts/seeds/queries/01_en.json`](scripts/seeds/queries/01_en.json) … `11_en.json`。论文种子：`scripts/seeds/papers/*_seed_cn.json`。

主集合过滤：标题或摘要须同时出现空气质量/污染物用语与预报/预测未来用语。随机切分的同期浓度估计不称为未来预报。

## 查重兄弟库

脚本 `papers_en.py` 对以下目录的 [`catalog_cn.csv`](catalog_cn.csv) 按 arXiv 标识去重，命中则复制并复验，不移动原件：

- `signal_processing_literature`（关键词空气质量无目录命中）
- `recent_top_conference_research`（目录含 air quality 字样，但本轮已核验论文状态均为「本轮新下载」，**复用计数 0**）
- 其余列出的 GPR / 时序 / MDP 等库在本机不存在或无对应 PDF

不把顶会通用时序论文改称为空气质量预报论文。

## 下载核验

- PDF：`%PDF-` 头、pypdf 可解析、正文可提取、标题匹配、参考文献节。
- 书籍：按页数下限与名称短语。
- 课程：OCW zip 内 PDF 全部可解析；HTML 课包记录实际页面清单。
- 软件文档：wget 离线页 + `PAGES_en.txt`。
- 代码：GitHub 归档 zip 测试、解压、`must_contain`、SNAPSHOT commit；去掉权重/大型 npy；不跑代码。

人工核对通过的条目包括：CAMS 区域系统论文（Colette 等）、部分 GMD 作者栏写成 consortium 的条目。PriSTI（arXiv:2302.09746）拒收：时空填补，不是未来预报。

## 失败类别（不绕过）

| 类型 | 代表 | 原因 |
|---|---|---|
| WAF/403 | NASA Earthdata ARSET 幻灯、部分 NASA 门户 | 边缘 403，不绕过 |
| SPA/非 PDF | WHO IRIS 2021 全球空气质量指导值 | 响应无 `%PDF-` 头 |
| 404 | Jacob 习题 PDF、NOAA STI 旧预报页、若干 arXiv PDF | 链接失效 |
| HTTP None | WRF-Chem Users_guide.pdf（NOAA RUC） | 传输失败 |
| 私有仓 | `openaq/openaq-api-v3` | `git ls-remote` 需登录 |
| 填补任务 | PriSTI | 主集合拒收 |

## 代码比例

已核验论文 119 篇中，静态见到作者仓库或 PDF 内 GitHub 链接并标为官方完整/部分实现的为 32 篇（26.9%）。未达到「至少 70% 已下载论文有作者官方代码」的争取目标。**不为此降低相关性或把第三方套件中的对照方法算作原作者实现。** 其余 81 篇代码状态保持「待全文核实」，6 篇明确无代码（主要为业务 CTM/再分析系统论文）。

## 复用

本轮目录计数：已有复用 0，新下载 162（论文 119 + 教材 6 + 课程 6 + 软件文档 12 + 项目 19）。
