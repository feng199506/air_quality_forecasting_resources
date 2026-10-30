#!/usr/bin/env python3
"""Search arXiv, filter true air-quality *forecast* papers, write seed JSON.

  PYTHONUNBUFFERED=1 python3 -I scripts/select_papers_en.py search
  PYTHONUNBUFFERED=1 python3 -I scripts/select_papers_en.py write
"""
import json
import re
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import SEEDS, save, load, WINDOW_START, window_status
from papers_en import API, parse_entries, meta_file, get_meta, CAND_DIR, http

QUERIES = [
    ("02", "目标与时效",
     'ti:"air quality" AND (all:forecast OR all:forecasting OR all:prediction)'),
    ("02", "PM2.5预报",
     "(ti:PM2.5 OR ti:\"PM 2.5\") AND (all:forecast OR all:forecasting) AND (all:hourly OR all:station OR all:spatiotemporal)"),
    ("02", "臭氧预报",
     'ti:ozone AND (all:forecast OR all:forecasting) AND (all:"air quality" OR all:MDA8 OR all:surface)'),
    ("03", "统计预报",
     "(all:ARIMA OR all:SARIMAX OR all:Kalman OR all:\"gaussian process\" OR all:GAM) AND (all:PM2.5 OR all:\"air quality\") AND (all:forecast OR all:forecasting)"),
    ("04", "机器学习",
     '(all:"random forest" OR all:XGBoost OR all:LightGBM OR all:"gradient boosting" OR all:"support vector") AND (all:PM2.5 OR all:"air quality") AND (all:forecast OR all:prediction)'),
    ("05", "深度学习",
     "(all:LSTM OR all:GRU OR all:Transformer OR all:TCN) AND (all:PM2.5 OR all:\"air quality\") AND (all:forecast OR all:forecasting)"),
    ("06", "图与时空",
     '(all:"graph neural" OR all:spatiotemporal OR all:"spatio-temporal") AND (all:PM2.5 OR all:"air quality") AND (all:forecast OR all:prediction)'),
    ("07", "概率",
     '(all:probabilistic OR all:quantile OR all:"conformal prediction" OR all:CRPS OR all:exceedance) AND (all:"air quality" OR all:PM2.5 OR all:ozone) AND (all:forecast OR all:prediction)'),
    ("08", "机理混合",
     '(all:"bias correction" OR all:post-processing OR all:"data assimilation" OR all:"physics-guided" OR all:"neural ODE" OR all:CMAQ) AND (all:"air quality" OR all:PM2.5) AND (all:forecast OR all:prediction OR all:machine)'),
    ("09", "数据质量",
     '(all:PurpleAir OR all:"low-cost sensor" OR all:OpenAQ OR all:missing OR all:calibration) AND (all:PM2.5 OR all:"air quality")'),
    ("10", "评测基准",
     '(all:benchmark OR all:evaluation OR all:verification OR all:KnowAir) AND all:"air quality" AND (all:forecast OR all:forecasting)'),
    ("11", "业务系统",
     '(all:operational OR all:NAQFC OR all:CAMS OR all:"real-time") AND all:"air quality" AND all:forecast'),
    ("01", "CTM与排放",
     '(all:CMAQ OR all:"WRF-Chem" OR all:"GEOS-Chem" OR all:CAMS) AND (all:forecast OR all:evaluation) AND all:"air quality"'),
    ("06", "AirFormer等",
     "all:AirFormer OR all:AirPhyNet OR all:KnowAir OR all:HighAir OR all:PCDCNet OR all:\"Air-DualODE\""),
    ("05", "会议深度学习",
     'ti:"air quality" AND (all:LSTM OR all:Transformer OR all:"deep learning") AND (all:forecast OR all:prediction)'),
]

FORECAST_RE = re.compile(
    r"\b(forecast|forecasting|predicting|prediction|nowcast|lead time|hours ahead|days ahead|horizon)\b",
    re.I)
AQ_RE = re.compile(
    r"\b(air quality|pm2\.5|pm10|ozone|no2|so2|\bco\b|pollutant|pollution|aqi|cmaq|cams|naqfc)\b",
    re.I)
NOT_MAIN_RE = re.compile(
    r"\b(interpolat|kriging|land[- ]use regression|missing value|imputation|inversion|retrieval of|"
    r"aod[- ]pm|satellite retrieval|spatial mapping without temporal|reconstruct historical)\b",
    re.I)
CODE_RE = re.compile(r"github\.com/[\w.\-]+/[\w.\-]+", re.I)

CAT_DIR = {
    "01": "domain_foundations", "02": "targets_horizons", "03": "statistical_baselines",
    "04": "machine_learning", "05": "deep_learning", "06": "spatiotemporal",
    "07": "probabilistic_forecasting", "08": "physics_hybrid", "09": "data_quality_features",
    "10": "evaluation_reproducibility", "11": "practical_projects",
}


def search(per=50):
    from common_en import WINDOW_END
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    cands = load(CAND_DIR / "all_en.json", {})
    win = f"submittedDate:[{WINDOW_START.replace('-', '')}0000 TO {WINDOW_END.replace('-', '')}2359]"
    for cat, sub, q in QUERIES:
        qq = f"({q}) AND {win}"
        url = API + urllib.parse.urlencode({"search_query": qq, "start": 0, "max_results": per,
                                           "sortBy": "relevance", "sortOrder": "descending"})
        st, body, _, _ = http(url, accept="application/atom+xml", tries=4)
        if st != 200:
            print(f"  [{st}] {sub}: {q[:80]}", flush=True)
            continue
        ents = parse_entries(body)
        for rank, (aid, m) in enumerate(ents.items()):
            save(meta_file(aid), m)
            c = cands.setdefault(aid, {"hits": [], "cats": []})
            c["hits"].append({"cat": cat, "subtopic": sub, "q": q, "rank": rank})
            if cat not in c["cats"]:
                c["cats"].append(cat)
        print(f"  {len(ents):3d}  {cat} {sub}", flush=True)
        save(CAND_DIR / "all_en.json", cands)
    print("candidates", len(cands), flush=True)


def classify(m):
    blob = (m.get("title", "") + " " + m.get("abstract", "") + " " + m.get("comment", "")).lower()
    scores = {c: 0 for c in CAT_DIR}
    rules = [
        ("08", r"cmaq|wrf-chem|geos-chem|bias correction|post-process|data assimilation|physics-guid|neural ode|pinn|hybrid physics"),
        ("07", r"conformal|quantile|probabilistic|crps|exceedance|uncertainty|ensemble forecast|prediction interval"),
        ("06", r"graph neural|spatiotemporal|spatio-temporal|multi-station|nationwide|transfer learning|unmonitored"),
        ("05", r"lstm|gru|transformer|tcn|deep learning|cnn"),
        ("04", r"random forest|xgboost|lightgbm|gradient boosting|support vector|machine learning"),
        ("03", r"arima|sarimax|kalman|gaussian process|gam |persistence|var\b|state.space"),
        ("09", r"purpleair|low-cost|openaq|missing|calibrat|quality flag|era5|aod"),
        ("10", r"benchmark|evaluation protocol|reproducib|fairmode|verification"),
        ("11", r"operational|naqfc|real-time system|deploy|airnow"),
        ("02", r"aqi|exceedance|peak|episode|nowcast|horizon|72-hour|72 h|mda8"),
        ("01", r"emission|dispersion|chemistry|transport model|cams reanalysis"),
    ]
    for cat, pat in rules:
        if re.search(pat, blob):
            scores[cat] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] else "05"


def is_forecast(m):
    t = m.get("title", "")
    a = m.get("abstract", "")
    if not AQ_RE.search(t + " " + a):
        return False
    if not FORECAST_RE.search(t + " " + a):
        return False
    return True


def write_seeds(target_min=85, target_max=115):
    cands = load(CAND_DIR / "all_en.json", {})
    ids = list(cands)
    metas = get_meta(ids)
    must = [
        ("02", "2211.15979"), ("08", "2402.03784"), ("08", "2410.19892"),
        ("08", "2505.19842"), ("03", "2002.12898"), ("04", "2101.04264"),
        ("09", "2504.10014"),
    ]
    chosen = {}
    for cat, aid in must:
        m = metas.get(aid) or get_meta([aid]).get(aid)
        if m:
            chosen[aid] = cat
    scored = []
    for aid, c in cands.items():
        m = metas.get(aid)
        if not m or aid in chosen:
            continue
        if not is_forecast(m):
            continue
        best = min((h["rank"] for h in c["hits"]), default=99)
        n = len(c["hits"])
        gh = 1 if CODE_RE.search(m.get("comment", "") + m.get("abstract", "")) else 0
        scored.append((gh, n, -best, aid, m, c))
    scored.sort(reverse=True)
    for gh, n, nb, aid, m, c in scored:
        if len(chosen) >= target_max:
            break
        cat = classify(m)
        # keep category sizes somewhat even
        counts = {k: 0 for k in CAT_DIR}
        for v in chosen.values():
            counts[v] += 1
        if counts[cat] >= 14:
            # put overflow in a needy cat among hits
            for h in sorted(c["hits"], key=lambda x: x["rank"]):
                if counts.get(h["cat"], 0) < 12:
                    cat = h["cat"]
                    break
        chosen[aid] = cat
    if len(chosen) < target_min:
        print("WARN only", len(chosen), "forecast papers after filter", flush=True)

    # Copernicus OA papers (not on arXiv necessarily)
    oa = {
        "01": [
            {"pdf_url": "https://gmd.copernicus.org/articles/14/2867/2021/gmd-14-2867-2021.pdf",
             "title": "The Community Multiscale Air Quality (CMAQ) model versions 5.3 and 5.3.1: system updates and evaluation",
             "authors": ["K. Wyat Appel", "Jesse O. Bash", "Kathleen M. Fahey", "Kristen M. Foley"],
             "date": "2021-05-20", "date_basis": "GMD published 20 May 2021",
             "venue": "Geosci. Model Dev., 14, 2867–2897, 2021",
             "doi": "10.5194/gmd-14-2867-2021",
             "landing": "https://gmd.copernicus.org/articles/14/2867/2021/",
             "subtopic": "CMAQ系统", "type": "原始研究论文",
             "classic_reason": "2021-05 略早于五年窗口，CMAQ 5.3 系统说明。",
             "reason": "CMAQ 科学更新的开放获取系统论文，机理预报先修。",
             "summary": "CMAQ 5.3/5.3.1 气溶胶、化学、沉降与排放处理更新及 O3/PM2.5 评估。",
             "summary_basis": "GMD 摘要",
             "task": "supporting_ctm", "spatial_unit": "grid", "target": "O3 MDA8; PM2.5 daily",
             "code_url": "https://github.com/USEPA/CMAQ", "code_kind": "official_full"},
            {"pdf_url": "https://acp.copernicus.org/articles/19/3515/2019/acp-19-3515-2019.pdf",
             "title": "The CAMS reanalysis of atmospheric composition",
             "authors": ["Antje Inness", "Melanie Ades", "Anna Agusti-Panareda"],
             "date": "2019-03-20", "date_basis": "ACP published 20 Mar 2019",
             "venue": "Atmos. Chem. Phys., 19, 3515–3556, 2019",
             "doi": "10.5194/acp-19-3515-2019",
             "landing": "https://acp.copernicus.org/articles/19/3515/2019/",
             "subtopic": "CAMS再分析支撑", "type": "原始研究论文",
             "classic_reason": "2019 CAMS 再分析系统论文。再分析不是可部署预报。",
             "reason": "官方再分析说明，单列为支撑资料。",
             "summary": "同化卫星 O3/CO/NO2/AOD 的全球成分再分析。",
             "summary_basis": "ACP 摘要",
             "task": "reanalysis_support", "spatial_unit": "grid", "target": "O3; CO; NO2; AOD",
             "code_kind": "none", "meteo": "reanalysis"},
        ],
        "02": [
            {"pdf_url": "https://gmd.copernicus.org/articles/15/3281/2022/gmd-15-3281-2022.pdf",
             "title": "Development and evaluation of an advanced National Air Quality Forecasting Capability using the NOAA Global Forecast System version 16",
             "authors": ["Patrick C. Campbell"],
             "date": "2022-04-20", "date_basis": "GMD 2022（日待全文核对）",
             "venue": "Geosci. Model Dev.", "landing": "https://gmd.copernicus.org/articles/15/3281/2022/",
             "doi": "10.5194/gmd-15-3281-2022",
             "subtopic": "NAQFC 72小时", "type": "原始研究论文",
             "reason": "美国业务 GFS–CMAQ 72 小时 O3/PM2.5 预报。",
             "summary": "NACC-CMAQ 2021-07-20 业务化，野火/沙尘与 72 小时评估。",
             "summary_basis": "GMD 摘要",
             "task": "future_forecast", "spatial_unit": "grid", "target": "O3; PM2.5",
             "horizon": "72h", "meteo": "nwp_forecast_at_issue", "code_kind": "official_partial"},
            {"pdf_url": "https://gmd.copernicus.org/articles/18/6835/2025/gmd-18-6835-2025.pdf",
             "title": "Copernicus Atmosphere Monitoring Service – Regional Air Quality Production System v1.0",
             "authors": ["CAMS Regional consortium"],
             "date": "2025-01-01", "date_basis": "GMD 18, 6835, 2025（日待全文核对）",
             "venue": "Geosci. Model Dev.", "landing": "https://gmd.copernicus.org/articles/18/6835/2025/",
             "subtopic": "CAMS区域97小时集合", "type": "原始研究论文",
             "reason": "欧洲 11 模式集合业务预报官方说明。",
             "summary": "0.1°、97 小时、19 物种与 ENSEMBLE 中位数。",
             "summary_basis": "GMD 摘要",
             "task": "future_forecast", "spatial_unit": "grid", "target": "多污染物浓度",
             "horizon": "97h hourly", "meteo": "nwp_forecast_at_issue", "code_kind": "none"},
        ],
        "03": [
            {"pdf_url": "https://gmd.copernicus.org/articles/16/6029/2023/gmd-16-6029-2023.pdf",
             "title": "A standardized methodology for the validation of air quality forecast applications (F-MQO): lessons learnt from its application across Europe",
             "authors": ["FAIRMODE F-MQO authors"],
             "date": "2023-10-24", "date_basis": "GMD 16, 6029, 2023（日待全文核对）",
             "venue": "Geosci. Model Dev.", "landing": "https://gmd.copernicus.org/articles/16/6029/2023/",
             "doi": "10.5194/gmd-16-6029-2023",
             "subtopic": "持续性基线与F-MQO", "type": "原始研究论文",
             "reason": "以持续性模型为基准的欧洲预报检验协议，含超标与 AQI。",
             "summary": "突变、阈值超标、AQI 再现与持续性对照。",
             "summary_basis": "GMD 摘要",
             "task": "evaluation_protocol", "spatial_unit": "station", "target": "浓度; 超标; AQI",
             "code_kind": "none"},
        ],
        "08": [
            {"pdf_url": "https://gmd.copernicus.org/articles/15/4129/2022/gmd-15-4129-2022.pdf",
             "title": "Evaluation of WRF-Chem model (v3.9.1.1) real-time air quality forecasts over the Eastern Mediterranean",
             "authors": ["WRF-Chem Eastern Mediterranean authors"],
             "date": "2022-05-20", "date_basis": "GMD 15, 4129, 2022（日待全文核对）",
             "venue": "Geosci. Model Dev.", "landing": "https://gmd.copernicus.org/articles/15/4129/2022/",
             "subtopic": "WRF-Chem实时预报", "type": "原始研究论文",
             "reason": "在线耦合 3 日实时预报，对照 CAMS。",
             "summary": "NO2/O3/PM2.5，嵌套网格，塞浦路斯站点。",
             "summary_basis": "GMD 摘要",
             "task": "future_forecast", "spatial_unit": "station", "target": "NO2; O3; PM2.5",
             "horizon": "3d", "meteo": "online_coupled_nwp", "code_kind": "none"},
            {"pdf_url": "https://gmd.copernicus.org/articles/15/4657/2022/gmd-15-4657-2022.pdf",
             "title": "Regional evaluation of the performance of the global CAMS chemical modeling system over the United States (IFS cycle 47r1)",
             "authors": ["CAMS US evaluation authors"],
             "date": "2022-06-15", "date_basis": "GMD 15, 4657, 2022（日待全文核对）",
             "venue": "Geosci. Model Dev.", "landing": "https://gmd.copernicus.org/articles/15/4657/2022/",
             "subtopic": "CAMS全球预报美国评估", "type": "原始研究论文",
             "reason": "全球 CAMS 预报在美国的评估，对照 NAQFC。",
             "summary": "IFS 47r1 全球空气质量预报评估。",
             "summary_basis": "GMD 摘要",
             "task": "future_forecast", "spatial_unit": "grid", "target": "O3; PM",
             "code_kind": "none"},
        ],
        "09": [
            {"pdf_url": "https://gmd.copernicus.org/articles/16/509/2023/gmd-16-509-2023.pdf",
             "title": "Comparing Sentinel-5P TROPOMI column observations with the CAMS regional air quality ensemble",
             "authors": ["TROPOMI-CAMS authors"],
             "date": "2023-01-18", "date_basis": "GMD 16, 509, 2023（日待全文核对）",
             "venue": "Geosci. Model Dev.", "landing": "https://gmd.copernicus.org/articles/16/509/2023/",
             "subtopic": "卫星柱浓度支撑", "type": "原始研究论文",
             "reason": "遥感柱浓度与预报集合对比，单列为支撑，不是地面浓度未来预报。",
             "summary": "TROPOMI 与 CAMS 区域集合的 NO2 等比较。",
             "summary_basis": "GMD 摘要",
             "task": "inversion_support", "spatial_unit": "grid", "target": "NO2 column",
             "code_kind": "none"},
        ],
        "10": [
            {"pdf_url": "https://gmd.copernicus.org/articles/14/3489/2021/gmd-14-3489-2021.pdf",
             "title": "The GEOS-CF system and its evaluation (placeholder title; verified on download)",
             "authors": ["Christoph A. Keller"],
             "date": "2021-06-16", "date_basis": "GMD 14, 3489, 2021（待下载核验标题）",
             "venue": "Geosci. Model Dev.", "landing": "https://gmd.copernicus.org/articles/14/3489/2021/",
             "subtopic": "GEOS-CF系统", "type": "原始研究论文",
             "classic_reason": "若确为 GEOS-CF 系统文则保留；否则下载失败不计数。",
             "reason": "NASA 全球成分预报系统候选文档。",
             "summary": "待全文核实标题与任务。",
             "summary_basis": "GMD 卷期",
             "task": "future_forecast", "spatial_unit": "grid", "code_kind": "official_partial",
             "reserve": True},
        ],
    }

    buckets = {c: [] for c in CAT_DIR}
    for aid, cat in chosen.items():
        m = metas.get(aid) or get_meta([aid]).get(aid)
        if not m:
            continue
        comment = m.get("comment") or ""
        abs_ = m.get("abstract") or ""
        gh = CODE_RE.search(comment + " " + abs_)
        item = {
            "arxiv": aid,
            "subtopic": (cands.get(aid, {}).get("hits") or [{"subtopic": CAT_DIR[cat]}])[0]["subtopic"],
            "type": "原始研究论文",
            "level": "硕士",
            "difficulty": "中级",
            "reason": "arXiv 检索命中且标题/摘要同时含空气质量与预报用语。",
            "summary": (abs_[:280] + "…") if len(abs_) > 280 else abs_,
            "summary_basis": "arXiv 摘要",
            "task": "future_forecast" if is_forecast(m) else "待全文核实",
            "code_kind": "official_partial" if gh else "待全文核实",
        }
        if gh:
            item["code_url"] = "https://" + gh.group(0)
        if window_status(m["v1_date"]) != "近五年":
            item["classic_reason"] = f"窗口外 v1={m['v1_date']}，因方法代表性保留。"
        buckets[cat].append(item)

    for cat, items in oa.items():
        buckets.setdefault(cat, []).extend(items)

    outdir = SEEDS / "papers"
    outdir.mkdir(parents=True, exist_ok=True)
    total = 0
    for cat, slug in CAT_DIR.items():
        items = buckets.get(cat, [])
        path = outdir / f"{cat}_{slug}_seed_cn.json"
        path.write_text(json.dumps(items, ensure_ascii=False, indent=1))
        n_main = sum(1 for x in items if not x.get("reserve"))
        total += n_main
        print(f"{cat} {slug}: {len(items)} seeds (main {n_main})", flush=True)
    print("main papers", total, flush=True)


if __name__ == "__main__":
    cmd = (sys.argv[1:] or ["search"])[0]
    if cmd == "search":
        search(int(sys.argv[2]) if len(sys.argv) > 2 else 50)
    elif cmd == "write":
        write_seeds()
    else:
        print(__doc__)
