#!/usr/bin/env python3
"""Build catalog_cn.csv, progress_cn.csv, download_failures_cn.csv,
code_availability_cn.csv, evaluation_audit_cn.csv, datasets_catalog_cn.csv,
and project_readiness_cn.csv.
"""
import csv
import json
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common_en import ROOT, STATE, SEEDS, CATS, cat_label, load, window_status, SEARCH_DATE

PAPER_STATE = STATE / "papers"
MAT_STATE = STATE / "materials"

CAT_FIELDS = [
    "编号", "资料类型", "主分类", "交叉分类", "标题", "作者", "学校或出版社或渠道", "资料角色",
    "首次公开日期", "首次公开依据", "时间窗口", "三年前或经典保留理由", "语言", "标识符",
    "原始来源", "下载地址", "本地路径", "完整性", "核验说明", "来源性质", "复用来源", "许可证",
    "版本", "维护状态", "可运行性等级", "缺失依赖", "选入理由", "简介", "简介依据",
]


def paper_rows():
    rows, fails = [], []
    for cat in CATS:
        slug = CATS[cat][0]
        seeds = load(SEEDS / "papers" / f"{cat}_{slug}_seed_cn.json", [])
        st = load(PAPER_STATE / f"{cat}_en.json", {})

        def key(s):
            return "arxiv:" + s["arxiv"] if s.get("arxiv") else "url:" + s["pdf_url"]

        for i, s in enumerate(seeds, 1):
            k = key(s)
            rec = st.get(k, {})
            status = rec.get("status", "pending")
            ident = f"P{cat}-{i:03d}"
            title = s.get("title") or ""
            authors = "; ".join(s.get("authors") or [])
            date = s.get("date", "")
            pdf = s.get("pdf_url") or (f"https://arxiv.org/pdf/{s['arxiv']}" if s.get("arxiv") else "")
            landing = s.get("landing") or (f"https://arxiv.org/abs/{s['arxiv']}" if s.get("arxiv") else pdf)
            from papers_en import entry_meta
            try:
                m = entry_meta(s) or {}
            except Exception:
                m = {}
            title = title or m.get("title", "")
            if not authors:
                authors = "; ".join(m.get("authors") or [])
            date = date or m.get("date", "")
            basis = s.get("date_basis") or m.get("date_basis", "")
            win = window_status(date)
            note = rec.get("note", "")
            ok = status == "ok"
            row = {
                "编号": ident,
                "资料类型": "论文/综述/教程",
                "主分类": cat_label(cat),
                "交叉分类": s.get("subtopic", ""),
                "标题": title,
                "作者": authors,
                "学校或出版社或渠道": m.get("journal_ref") or s.get("venue") or ("arXiv" if s.get("arxiv") else ""),
                "资料角色": s.get("type", ""),
                "首次公开日期": date,
                "首次公开依据": basis,
                "时间窗口": win if not s.get("classic_reason") else ("五年前（经典补充）" if win == "五年前" else win),
                "三年前或经典保留理由": s.get("classic_reason", ""),
                "语言": "en",
                "标识符": (f"arXiv:{s['arxiv']}" if s.get("arxiv") else s.get("doi", "")),
                "原始来源": landing,
                "下载地址": rec.get("pdf") or pdf,
                "本地路径": rec.get("path", ""),
                "完整性": "完整（核验通过）" if ok else ("残缺/失败" if status == "fail" else status),
                "核验说明": note,
                "来源性质": "已有复用" if rec.get("source") == "reuse" else ("本轮新下载" if ok else ""),
                "复用来源": f"{rec.get('reuse_lib', '')} {rec.get('reuse_id', '')}".strip(),
                "许可证": "见原文版权页/arXiv 许可",
                "版本": m.get("version", ""),
                "维护状态": "",
                "可运行性等级": "",
                "缺失依赖": "",
                "选入理由": s.get("reason", ""),
                "简介": s.get("summary", ""),
                "简介依据": s.get("summary_basis", ""),
            }
            row["_seed"] = s
            row["_key"] = k
            row["_cat"] = cat
            if ok:
                rows.append(row)
            else:
                fails.append({"编号": ident, "资料类型": "论文/综述/教程", "标题": title,
                              "状态": status, "说明": note, "地址": pdf})
    return rows, fails


def mat_rows():
    rows, fails = [], []
    for setname, typ, prefix in [
        ("books", "教科书/专著/参考书", "B"),
        ("courses", "大学课程/讲义", "C"),
        ("software", "官方软件文档", "S"),
        ("projects", "参考项目/实验", "P"),
    ]:
        items = []
        for p in sorted((SEEDS / "materials").glob(f"{setname}*_cn.json")):
            items += load(p, [])
        for it in items:
            if it.get("exclude"):
                continue
            mid = it["mid"]
            rec = load(MAT_STATE / f"{mid}.json", {})
            status = rec.get("status", "pending")
            paths = "; ".join(f.get("path", "") for f in rec.get("files", []))
            role = it.get("book_role") or it.get("pack_type") or it.get("count_as") or ""
            row = {
                "编号": mid,
                "资料类型": typ,
                "主分类": cat_label(it.get("group", "11")),
                "交叉分类": ";".join(it.get("related") or []),
                "标题": it.get("title", ""),
                "作者": it.get("authors", ""),
                "学校或出版社或渠道": it.get("institution", ""),
                "资料角色": role,
                "首次公开日期": it.get("orig_year") or it.get("edition_year", ""),
                "首次公开依据": "出版/课程页",
                "时间窗口": "教材/课程允许经典版本" if typ.startswith("教科书") else "课程优先近期版本",
                "三年前或经典保留理由": it.get("reason", "") if str(it.get("orig_year", "")) < "2023" else "",
                "语言": it.get("lang", "en"),
                "标识符": it.get("identifier") or it.get("code") or it.get("edition", ""),
                "原始来源": it.get("landing") or it.get("index_url") or it.get("url") or it.get("repo", ""),
                "下载地址": it.get("url") or it.get("index_url") or it.get("repo", ""),
                "本地路径": paths,
                "完整性": "完整（核验通过）" if status == "verified" else ("残缺/失败" if status == "failed" else "待核验"),
                "核验说明": rec.get("note", ""),
                "来源性质": "已有复用" if rec.get("reuse") or it.get("kind") == "reuse" else ("本轮新下载" if status == "verified" else ""),
                "复用来源": f"{it.get('src_lib', '')} {it.get('src_id', '')}".strip(),
                "许可证": it.get("license", ""),
                "版本": it.get("edition") or it.get("edition_year") or rec.get("commit", ""),
                "维护状态": it.get("maintain", ""),
                "可运行性等级": "L0/L1（本轮不执行外部代码）" if typ.startswith("参考项目") else "",
                "缺失依赖": "",
                "选入理由": it.get("reason", ""),
                "简介": it.get("summary", ""),
                "简介依据": it.get("summary_basis", "种子说明"),
            }
            if status == "verified":
                rows.append(row)
            else:
                fails.append({"编号": mid, "资料类型": typ, "标题": it.get("title", ""),
                              "状态": status or "pending", "说明": rec.get("note", ""), "地址": row["下载地址"]})
    return rows, fails


def code_rows(pr):
    out = []
    for r in pr:
        s = r.get("_seed") or {}
        kind = s.get("code_kind") or "待全文核实"
        url = s.get("code_url") or ""
        # map to required labels
        label = {
            "official_full": "官方完整实现",
            "official_partial": "官方部分代码",
            "third_party": "第三方复现",
            "to_be_released": "待发布",
            "none": "无代码",
        }.get(kind, "待全文核实")
        out.append({
            "论文编号": r["编号"],
            "标题": r["标题"],
            "代码状态": label,
            "代码地址": url,
            "对应项目编号": "",
            "许可证": r["许可证"],
            "版本或commit": r["版本"],
            "核验级别": "",
            "缺失": "本轮未运行；大型数据与权重未下载" if label.startswith("官方") else "",
            "备注": s.get("task", ""),
        })
    return out


def eval_rows(pr):
    out = []
    for r in pr:
        s = r.get("_seed") or {}
        unk = "待全文核实"
        out.append({
            "编号": r["编号"],
            "标题": r["标题"],
            "任务类型": s.get("task", unk),
            "目标变量": s.get("target", unk),
            "空间单元": s.get("spatial_unit", unk),
            "预报发布时刻": s.get("issue_time", unk),
            "输入窗": s.get("input_window", unk),
            "预测跨度": s.get("horizon", unk),
            "输出频率": s.get("output_freq", unk),
            "数据切分": s.get("split", unk),
            "气象来源": s.get("meteo", unk),
            "是否事后再分析或修订数据": s.get("post_hoc", unk),
            "预处理是否仅训练集拟合": s.get("preprocess_fit", unk),
            "泄漏风险": s.get("leakage", unk),
            "基线是否公平": s.get("baselines", unk),
            "多步方式": s.get("multi_step", unk),
            "分项表现": s.get("breakdown", unk),
            "点预测指标": s.get("metrics", unk),
            "概率指标": s.get("prob_metrics", unk),
            "高污染事件": s.get("extremes", unk),
            "多次运行与计算成本": s.get("uncertainty_cost", unk),
        })
    return out


def dataset_rows():
    items = load(SEEDS / "materials" / "datasets_cn.json", [])
    rows = []
    for it in items:
        rows.append({
            "编号": it.get("did"),
            "名称": it.get("name"),
            "机构": it.get("agency"),
            "说明页": it.get("landing"),
            "获取方式": it.get("access"),
            "污染物": it.get("pollutants"),
            "单位": it.get("units"),
            "时区": it.get("timezone"),
            "频率": it.get("frequency"),
            "站点或网格": it.get("stations"),
            "覆盖年份": it.get("years"),
            "质量标记": it.get("qc_flags"),
            "发布延迟": it.get("latency"),
            "修订机制": it.get("revision"),
            "许可": it.get("license"),
            "预报发布时刻是否可用": it.get("usable_at_issue"),
            "备注": it.get("notes"),
            "本轮是否下载原始数据": "否（仅文档）",
        })
    return rows


def main():
    pr, pf = paper_rows()
    mr, mf = mat_rows()
    cat_pr = [{k: v for k, v in r.items() if not k.startswith("_")} for r in pr]
    rows = cat_pr + mr
    fails = pf + mf
    catp = ROOT / "catalog_cn.csv"
    with catp.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAT_FIELDS)
        w.writeheader()
        w.writerows(rows)
    fp = ROOT / "download_failures_cn.csv"
    ff = ["编号", "资料类型", "标题", "状态", "说明", "地址"]
    with fp.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=ff)
        w.writeheader()
        w.writerows(fails)
    prog = []
    for cat in CATS:
        papers = [r for r in cat_pr if r["编号"].startswith(f"P{cat}-")]
        n = len(papers)
        n_recent = sum(1 for r in papers if r["时间窗口"].startswith("近五年"))
        n_reuse = sum(1 for r in papers if r["来源性质"] == "已有复用")
        n_fail = sum(1 for r in fails if r["编号"].startswith(f"P{cat}-"))
        books = sum(1 for r in mr if r["资料类型"].startswith("教科书") and r["主分类"].startswith(cat))
        courses = sum(1 for r in mr if r["资料类型"].startswith("大学") and r["主分类"].startswith(cat))
        sw = sum(1 for r in mr if r["资料类型"].startswith("官方") and r["主分类"].startswith(cat))
        proj = sum(1 for r in mr if r["资料类型"].startswith("参考") and r["主分类"].startswith(cat))
        pct = f"{(100 * n_recent / n):.1f}%" if n else "-"
        prog.append({
            "子方向": cat, "名称": CATS[cat][1],
            "论文已核验": n, "论文近五年占比": pct, "其中已有复用": n_reuse,
            "教材已核验": books, "课程已核验": courses, "软件已核验": sw, "项目已核验": proj,
            "失败/待核验": n_fail, "状态": "本轮收集进行中",
        })
    pp = ROOT / "progress_cn.csv"
    with pp.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(prog[0].keys()) if prog else [])
        w.writeheader()
        w.writerows(prog)

    ready = []
    for r in mr:
        if not r["资料类型"].startswith("参考"):
            continue
        rec = load(MAT_STATE / f"{r['编号']}.json", {})
        note = rec.get("note", "")
        missing = ""
        if "发现可能的 LFS" in note:
            missing = "可能有未保存的 LFS 对象，见核验说明"
        nfiles = 0
        if rec.get("files"):
            nfiles = rec["files"][0].get("files") or len(rec.get("files") or [])
        thin = nfiles and nfiles < 5
        if thin:
            missing = (missing + "；" if missing else "") + "配套仓库文件过少"
        has_entry = rec.get("status") == "verified" and not thin and (
            "README" in note or "应有文件" in note or "commit" in note.lower() or True)
        level = "L1" if rec.get("status") == "verified" and not thin else (
            "L0" if rec.get("status") == "verified" else "L0/未完成")
        ready.append({
            "编号": r["编号"], "项目": r["标题"], "本地路径": r["本地路径"],
            "可运行性等级": level,
            "静态核对": "入口/许可证/应有路径见核验说明" if rec.get("status") == "verified" else "未完成",
            "缺失依赖": missing or "本轮未安装运行依赖；未执行测试",
            "后续验证条件": "新建隔离环境，按 SNAPSHOT 与 README 安装依赖后做小型预测；禁止把上游 README 演示结果当作本机复现",
            "许可证": r["许可证"], "版本/commit": r["版本"],
        })
        # also fill code availability project number
    rp = ROOT / "project_readiness_cn.csv"
    with rp.open("w", encoding="utf-8-sig", newline="") as f:
        fields = ["编号", "项目", "本地路径", "可运行性等级", "静态核对", "缺失依赖", "后续验证条件", "许可证", "版本/commit"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(ready)

    cr = code_rows(pr)
    # attach project ids by github path
    proj_by_repo = {}
    for it in load(SEEDS / "materials" / "projects_cn.json", []):
        repo = (it.get("repo") or "").rstrip("/").lower()
        proj_by_repo[repo] = it["mid"]
    for row in cr:
        u = (row.get("代码地址") or "").rstrip("/").lower()
        if u in proj_by_repo:
            row["对应项目编号"] = proj_by_repo[u]
        for rec in ready:
            if rec["编号"] == row.get("对应项目编号"):
                row["核验级别"] = rec["可运行性等级"]
    cp = ROOT / "code_availability_cn.csv"
    with cp.open("w", encoding="utf-8-sig", newline="") as f:
        fields = ["论文编号", "标题", "代码状态", "代码地址", "对应项目编号", "许可证", "版本或commit", "核验级别", "缺失", "备注"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(cr)

    er = eval_rows(pr)
    ep = ROOT / "evaluation_audit_cn.csv"
    with ep.open("w", encoding="utf-8-sig", newline="") as f:
        fields = list(er[0].keys()) if er else ["编号"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(er)

    dr = dataset_rows()
    dp = ROOT / "datasets_catalog_cn.csv"
    with dp.open("w", encoding="utf-8-sig", newline="") as f:
        fields = list(dr[0].keys()) if dr else []
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(dr)

    print(f"catalog {len(rows)} verified; failures {len(fails)}; papers {len(pr)}; projects {len(ready)}; "
          f"code {len(cr)}; eval {len(er)}; datasets {len(dr)}")


if __name__ == "__main__":
    main()
