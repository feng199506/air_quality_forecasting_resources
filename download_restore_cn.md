# 空气质量预测资源库：下载、解压与离线阅读说明

本 Release 是 `air_quality_forecasting_resources` 资源库的完整发布包，快照日期为 2026-10-30。内容如下：

- 162 条目录记录：119 篇论文（arXiv 与 Copernicus 开放获取期刊），6 份教材与官方手册，6 门课程与讲义，12 套官方软件与数据文档的离线网页，19 个参考项目的源码快照。
- 目录、数据集说明、代码可用性、评测审计、进度与失败记录（CSV 格式）。
- 中文指南 7 篇、检索日志和续跑脚本。

## 1. 下载哪些文件

所有 tar 包都**不压缩**，可以各自独立解压。解压到同一个目录后，就能还原完整的目录树。

| 包 | 内容 | 是否需要 |
|---|---|---|
| `air_quality_forecasting_resources_20261030_batch001_cn_en.tar`（1.44 GiB） | 离线首页、目录 CSV、指南、脚本、全部论文、教材、课程、文档网页，以及大部分项目源码 | **必需** |
| `air_quality_forecasting_resources_20261030_batch002_cn_en.tar`（18 MiB） | `projects/statsmodels_statsmodels_en` 的后半部分 | 需要 statsmodels 源码时下载 |
| `air_quality_forecasting_resources_20261030_batch003_code_nolicense_cn_en.tar`（83 MiB） | **未声明许可证**的 3 个项目快照：AirFormer、Air-DualODE、MGSFformer | 按需，见第 5 节 |

每个文件在哪个包里，可以在 `archive_index_cn.csv` 中查（用 Excel 打开，按“相对路径”列搜索）。

## 2. Windows 下解压（请解压到短路径）

网页镜像中有几个很深的样式目录，包内最长的相对路径有 200 个字符。Windows 资源管理器默认只能处理 260 个字符以内的完整路径，所以**请解压到短目录**，例如 `D:\aqf\`。不要解压到“下载”文件夹下很深的子目录里。

**方法 A：PowerShell（Windows 10 1803 及以上自带 `tar`）**

把下载的 tar 包放进同一个文件夹，在该文件夹中打开 PowerShell，执行：

```powershell
mkdir D:\aqf -Force
Get-ChildItem *.tar | ForEach-Object { tar -xf $_.FullName -C D:\aqf }
```

**方法 B：7-Zip**

1. 全选 tar 包，右键选择“7-Zip → 提取文件…”。
2. 目标填 `D:\aqf\`。
3. 取消勾选“按压缩包名创建子文件夹”（如果有这个选项）。

**Linux / macOS**

```bash
mkdir -p ~/aqf && for f in *.tar; do tar -xf "$f" -C ~/aqf; done
```

## 3. 离线阅读

用浏览器（Edge、Chrome 或 Firefox）打开 `D:\aqf\index_cn.html`，不需要联网。

- 首页按资料类型列出全部 162 条记录。“本地文件”一栏直接打开本地 PDF、离线网页或源码目录；网页文档有多页的，后面列出“其他已保存页面”。“在线”一栏是原始地址，需要联网。
- `README_cn.html`、`search_log_cn.html` 和 `guides/*.html` 是对应 Markdown 文档的 HTML 版本。文中的文件路径都可以点击。
- 打开源码目录（例如 `projects/...`）时，浏览器显示的是文件列表，源码文件可以直接点开。
- CSV 文件带 BOM，用 Excel 直接打开，中文不会乱码。
- 离线网页里的站内链接：已保存的页面之间离线跳转；指向未保存页面的链接改成了原站网址，联网时可以打开。
- 发布前做过静态检查：首页、指南和 17 套网页镜像中，3,506 个本地链接全部能解析到包内文件，网页镜像里没有失效的本地链接。还有 98 个失效链接，都在 statsmodels、MONET 两个项目源码自带的旧 HTML 文档里，属上游原样。**没有在 Windows 真机浏览器上做渲染测试。**

## 4. 发布包相对本机原件的改动

只改了发布副本，本机原件没有改动。全部明细见 `windows_rename_map_cn.csv`。

- **Windows 兼容改名，292 个文件，都在网页镜像中。**
  - 网页资源名里的 `?查询串` 是 Windows 不允许的字符，改为 `_`。如果原名在 `?` 前已有真实扩展名，例如 `logo.svg?v=1`，就改成 `logo_<8位哈希>.svg`，保证浏览器能按扩展名识别图片和样式。
  - 完整路径超过 200 个字符的，把较长的名字截短为“前 12 个字符 + 原名哈希”。
  - 29 个网页和样式表中对这些文件的引用已同步改写。没有只差大小写的重名文件。
- **离线化（只改网页镜像，正文不变）：**
  - 原站的样式、脚本、字体和图片，有 754 个当初没有保存（约 54 MiB），这次补下载到镜像目录里。957 处引用改成了包内相对路径。
  - 原站已失效（404/403）的 94 个资源无法补齐，相应的图标或字体在离线时可能缺失，正文不受影响。
  - wget 写坏或指向未保存尺寸的响应式图片地址（`srcset`）共 71 个，已删去，浏览器改用已保存的图片。
  - Copernicus 数据门户（Next.js）和 EEA 网站（Volto）的前端应用脚本共 56 个，改为不执行。这些脚本在本地打开时找不到路由，会清空页面；停用后显示保存时的页面正文。页面上的交互功能（如切换标签、搜索）在离线时不可用。
  - 统计、聊天助手、广告类脚本保持原样，离线时不加载，不影响阅读。
- **新增文件：**离线首页 `index_cn.html`；9 个 Markdown 文档的 HTML 版本（Markdown 原文中 61 处路径改为相对链接）；3 个无许可证项目目录里的 `_NO_LICENSE_NOTICE_cn.txt`。
- **未打包：**
  - 资料库自身的 `.git/`。
  - 11 个空目录 `NN_.../{papers}/`：构建脚本中没有展开的花括号留下的，里面没有文件。

  见 `release_excluded_cn.csv`。除此之外没有遗漏的资料文件。

## 5. 版权与许可

- **论文 PDF**：版权归作者或出版方所有。来源是 arXiv 和 Copernicus 系开放获取期刊（GMD、ACP，CC BY），仅供个人学习研究。
- **教材与手册**：
  - Stull《Practical Meteorology》是 CC BY-NC-SA 4.0。
  - EPA、NOAA 的文件（AQI 技术文件、Appendix W、HYSPLIT 手册、CMAQ 科学文档）是美国政府公有领域资料。
  - openair 手册来自 CRAN，随 openair 包的许可（MIT）。
- **课程**：
  - MIT OCW 12.335 是 CC BY-NC-SA 4.0。
  - 其余为各机构网站页面的离线副本，以原站声明为准。
- **官方文档网页**：
  - EPA、NOAA、NASA、AirNow 的页面是美国政府资料。
  - Copernicus（CAMS/C3S）和 EEA 的页面按其网站的再利用政策使用。
  - readthedocs 文档按各项目许可使用。
- **有许可证的项目源码**（batch001–002 中的 16 个仓库）：按各仓库自带的 LICENSE 使用，其中有 MIT、BSD、Apache 等。
- **未声明许可证的项目源码**（batch003 中的 3 个仓库）：抓取时仓库里没有任何开源许可证。按著作权法默认规则，作者保留全部权利。这些快照仅供个人学习研究时对照论文阅读，请勿再分发、修改后发布或商用。每个目录里有 `_NO_LICENSE_NOTICE_cn.txt`，写明了来源地址和提交号。
- 源码快照只做了下载，没有运行过。数据集与模型权重都没有下载，见 `datasets_catalog_cn.csv` 和 `project_readiness_cn.csv`。

## 6. 附件一览

| 附件 | 说明 |
|---|---|
| `*_batch001…003_*.tar` | 资料本体（见第 1 节） |
| `archive_index_cn.csv` | 每个文件所在的包、路径、大小、改动备注 |
| `windows_rename_map_cn.csv` | Windows 改名、引用改写与离线化改动明细 |
| `release_excluded_cn.csv` | 未打包或单独打包的内容 |
| `download_restore_cn.md` | 本说明 |
| `upload_report_cn.md` | 上传结果报告 |
