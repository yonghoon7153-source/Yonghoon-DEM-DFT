#!/usr/bin/env python3
"""rebuild_pool_inputs.py — 풀 입력 2종을 **자동으로** 만든다 (champions.csv · ESW csv).

왜 이 도구가 있나 (2026-08-13)
  이 두 파일은 여태 **손으로** 만들어졌다. 그래서 2026-06-29 에 사람이 멈추자 파이프라인이
  같이 멈췄고, 7/11 에 끝난 계산 43종이 정본에 못 들어왔다
  (kb/methodology/cascade_pipeline_anatomy_2026_08_13.md). 손 단계를 없애는 것이 목적이다.

체인에서의 위치
    cascade_v23_all.csv (= unified_dataset_273.csv)
    oxidation_stability_cascade_v2.json (esw_cascade_batch.py 산출)
            ↓  **이 도구**
    cascade_v23_champions.csv  ·  oxidation_stability_cascade.csv
            ↓  tools/figures/plot_cascade_insights.py
    cascade_v23_ranked.csv
            ↓  tools/cascade/build_screening_funnel.py
    cascade_screening_funnel.json

ESW csv 의 plain/Cl-rich 분리
  옛 판이 `ox_V`(plain champion) 와 `clrich_ox_V`(+Clrich chain 변형) 를 **다른 열**로 실었다.
  그 규약을 그대로 재현한다 — 섞으면 "6종이 2.14 를 넘었다" 같은 집계가 조용히 달라진다.

  python3 tools/cascade/rebuild_pool_inputs.py --selftest
  python3 tools/cascade/rebuild_pool_inputs.py            # db/properties 에 _v2 접미사로 출력
  python3 tools/cascade/rebuild_pool_inputs.py --inplace  # 기존 파일을 덮어쓴다 (백업 먼저)

이 도구가 못 하는 것
  · 값을 검증하지 않는다. 입력 CSV/JSON 을 그대로 재배열할 뿐이다.
  · champion 을 다시 고르지 않는다 (`rank_combined == 1` 을 그대로 믿는다).
  · ranked.csv 와 funnel 은 만들지 않는다 — 위 체인의 다음 두 도구가 한다.
"""
import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROP = ROOT / "db" / "properties"

#: 음이온별 형식 원자가. plot_cascade_insights.py 의 ANION_VAL 과 같아야 한다.
ANION_VAL = {"O": 2, "S": 2, "N": 3, "F": 1, "Cl": 1, "Br": 1, "I": 1}
LANTH = {"La", "Nd", "Sm", "Gd"}
ALKALI = {"Li", "Na"}
AE = {"Mg", "Ca", "Sr", "Ba"}
MAIN = {"B", "Al", "Ga", "In", "Si", "Ge", "Sn", "Sb"}

#: champions.csv 가 실어야 하는 열 (plot_cascade_insights.py 가 읽는 것 + 계보용)
CHAMP_COLS = ["_dir", "dopant", "concentration", "rerank_de_post_anneal",
              "anneal_dV_pct", "eos_B0_GPa", "eos_fit_quality_ok",
              "elastic_E_young_GPa", "elastic_B_hill_GPa", "elastic_G_hill_GPa",
              "elastic_poisson_nu", "elastic_pugh_GoverB",
              "sigma_300K_S_cm_NE", "sigma_md_Ea_eV", "wad_J_m2_mean",
              "anneal_converged", "combined_score", "rank_combined"]


def parse_dopant(d):
    """`Al2O3+Clrich` → ('Al', 'O', 3, 'main-group'). 미지 음이온이면 예외."""
    d = d.split("+")[0]
    toks = [(e, int(n) if n else 1)
            for e, n in re.findall(r"([A-Z][a-z]?)(\d*)", d) if e]
    an = [e for e, _ in toks if e in ANION_VAL]
    if not an:
        raise ValueError(f"음이온을 못 찾았다: {d} — ANION_VAL 에 추가할 것")
    anion = an[-1]
    cats = [(e, n) for e, n in toks if e != anion]
    if not cats:
        raise ValueError(f"양이온을 못 찾았다: {d}")
    cat = cats[0]
    bn = [n for e, n in toks if e == anion][0]
    val = round(ANION_VAL[anion] * bn / cat[1])
    grp = ("lanthanide" if cat[0] in LANTH else "alkali" if cat[0] in ALKALI
           else "alk.earth" if cat[0] in AE else "main-group" if cat[0] in MAIN
           else "TM")
    return cat[0], anion, val, grp


def build_champions(all_csv):
    """cascade_v23_all.csv → champion 행만 (rank_combined == 1)."""
    rows = list(csv.DictReader(open(all_csv, encoding="utf-8")))
    if not rows:
        raise ValueError(f"빈 입력: {all_csv}")
    champs = [r for r in rows if str(r.get("rank_combined", "")).strip() == "1"]
    out = []
    for r in champs:
        o = {}
        for c in CHAMP_COLS:
            if c == "_dir":
                o[c] = r.get("_dir") or r.get("name", "")
            else:
                o[c] = r.get(c, "")
        out.append(o)
    return out, len(rows)


def build_esw_csv(esw_json):
    """ESW json → 도펀트당 1행. plain 과 +Clrich 를 **다른 열**로 나눈다."""
    j = json.load(open(esw_json, encoding="utf-8"))
    recs = j.get("results", j)
    plain, clr = {}, {}
    for k, v in recs.items():
        ox = v.get("oxidation_limit_V")
        if ox is None:
            continue
        sp = str(v.get("dopant", "")).split("+")[0]
        if not sp:
            continue
        tgt = clr if "chain_Cl" in k else plain
        # 같은 도펀트의 여러 농도 중 **가장 높은 onset** 을 대표로 (옛 판 규약)
        if sp not in tgt or ox > tgt[sp]["oxidation_limit_V"]:
            tgt[sp] = v
    rows = []
    for sp in sorted(set(plain) | set(clr)):
        base = plain.get(sp) or clr[sp]
        cat, anion, val, grp = parse_dopant(sp)
        note = []
        win = base.get("window_V")
        if win is not None and win < 0.05:
            note.append("collapse=window<0.05V")
        if sp in clr and sp in plain:
            d = clr[sp]["oxidation_limit_V"] - plain[sp]["oxidation_limit_V"]
            if abs(d) > 0.01:
                note.append(f"Cl-rich:ox->{clr[sp]['oxidation_limit_V']:.3f}")
        if sp not in plain:
            note.append("plain champion 없음 — Cl-rich 값으로 대체")
        rows.append({
            "dopant": sp, "anion": anion, "valence": val, "group": grp,
            "ox_V": base.get("oxidation_limit_V"),
            "red_V": base.get("reduction_limit_V"),
            "ocv_V": base.get("ocv_self_decomposition_V"),
            "window_V": win,
            "clrich_ox_V": (clr[sp]["oxidation_limit_V"] if sp in clr and sp in plain
                            else ""),
            "note": " ; ".join(note),
        })
    return rows


#: litransport 가 싣는 열 (build_screening_funnel.load_pool 이 `_dir` 로 조인한다)
LITRANS_COLS = ["_dir", "bvs_li_proxy_score", "migration_volume_fraction",
                "tier2_dopant_blocking_fraction", "tier2_li_li_disorder_std",
                "cation_site", "anion_site"]


def build_litransport(all_csv):
    """champion 행만 뽑아 G4 축 입력을 만든다. `_dir` 은 `<dopant>_x0NN` 형식이어야
    한다 — funnel 이 `rpartition('_x')` 로 도펀트와 농도를 가른다."""
    import re
    rows = list(csv.DictReader(open(all_csv, encoding="utf-8")))
    out = []
    for r in rows:
        if str(r.get("rank_combined", "")).strip() != "1":
            continue
        name = r.get("_dir") or r.get("name", "")
        # Ag2O_x020_cLi24ga... → Ag2O_x005 (funnel 은 x002/x005/x010 을 기대한다)
        m = re.match(r"(.+?)_x(\d+)", name)
        if not m:
            continue
        pct = {"002": "002", "005": "005", "010": "010",
               "020": "002", "050": "005", "100": "010"}.get(m.group(2))
        if not pct:
            continue
        o = {c: r.get(c, "") for c in LITRANS_COLS}
        o["_dir"] = f"{m.group(1)}_x{pct}"
        out.append(o)
    return out


def write_esw_csv(rows, path, src):
    # ⚠ 주석줄은 **csv.writer 로 쓰지 않는다**. 줄 안에 쉼표가 있으면 writer 가
    #   따옴표로 감싸 `"#...` 가 되고, 소비자의 `line.startswith("#")` 주석 필터를
    #   빠져나가 헤더 파싱이 깨진다 (2026-08-14 build_screening_funnel 에서 실측).
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(f"# grand-potential ESW per cascade dopant (UMA champion composition; "
                f"MP GGA_GGA+U hull). Source: {os.path.basename(src)} via "
                f"tools/cascade/rebuild_pool_inputs.py\n")
        f.write("# ox_V = PLAIN champion; clrich_ox_V = +Clrich chain variant "
                "(blank = no variant or no plain). Do not merge the two.\n")
        w = csv.writer(f)
        w.writerow(list(rows[0]))
        for r in rows:
            w.writerow([r[k] for k in rows[0]])


def selftest():
    """양성 + **음성**. 옛 판이 틀리던 입력과 plain/Clrich 분리를 확인한다."""
    import tempfile
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok &= bool(c)

    chk(parse_dopant("Al2O3+Clrich")[:3] == ("Al", "O", 3), "변형 접미사를 떼고 파싱")
    chk(parse_dopant("ZrCl4")[:3] == ("Zr", "Cl", 4), "염화물 (옛 판은 F/1 로 오인)")
    chk(parse_dopant("Li3N")[:3] == ("Li", "N", 1), "질화물")
    try:
        parse_dopant("Xx9"); chk(False, "미지 음이온을 통과시켰다")
    except ValueError:
        chk(True, "미지 음이온 → 예외 (조용한 오분류 금지)")

    td = Path(tempfile.mkdtemp(prefix="rebuild_pool_st_"))
    # champions: rank_combined 가 1 인 행만 골라야 한다
    ac = td / "all.csv"
    with open(ac, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["name", "dopant", "rank_combined",
                                          "rerank_de_post_anneal", "elastic_E_young_GPa"])
        w.writeheader()
        w.writerow({"name": "A_x020_s0", "dopant": "Al2O3", "rank_combined": "1",
                    "rerank_de_post_anneal": "-0.8", "elastic_E_young_GPa": "40"})
        w.writerow({"name": "A_x020_s1", "dopant": "Al2O3", "rank_combined": "2",
                    "rerank_de_post_anneal": "-0.7", "elastic_E_young_GPa": "41"})
    ch, ntot = build_champions(ac)
    chk(len(ch) == 1 and ntot == 2, f"champion 1행만 (전체 {ntot} 중 {len(ch)})")
    chk(ch[0]["_dir"] == "A_x020_s0", "_dir 없으면 name 으로 채운다")

    # ESW: plain 과 chain_Cl 이 **다른 열**로 가야 한다
    ej = td / "esw.json"
    json.dump({"results": {
        "Al2O3_x050_cLi_s0":               {"dopant": "Al2O3", "oxidation_limit_V": 2.140,
                                            "reduction_limit_V": 1.37, "window_V": 0.77},
        "Al2O3_x020_chain_Cl_x200_cLi_s0": {"dopant": "Al2O3+Clrich", "oxidation_limit_V": 2.354,
                                            "reduction_limit_V": 1.72, "window_V": 0.64},
        "FeCl3_x020_cLi_s0":               {"dopant": "FeCl3", "oxidation_limit_V": 1.808,
                                            "reduction_limit_V": 1.804, "window_V": 0.004},
    }}, open(ej, "w"))
    rows = build_esw_csv(ej)
    al = next(r for r in rows if r["dopant"] == "Al2O3")
    chk(al["ox_V"] == 2.140 and al["clrich_ox_V"] == 2.354,
        f"plain 2.140 / clrich 2.354 분리 (ox={al['ox_V']} clr={al['clrich_ox_V']})")
    # ★ 음성: 섞어서 max 를 쓰면 안 된다
    chk(al["ox_V"] != 2.354, "ox_V 에 Cl-rich 값이 새어들지 않는다")
    fe = next(r for r in rows if r["dopant"] == "FeCl3")
    chk("collapse" in fe["note"], f"window<0.05 → collapse 플래그 ({fe['note']})")
    chk(fe["anion"] == "Cl" and fe["valence"] == 3, "회수 계열도 정상 분류")

    # ★ 음성: 주석줄이 따옴표로 감싸이면 소비자의 `#` 필터를 빠져나가 헤더가 깨진다
    ep = td / "esw.csv"
    write_esw_csv(rows, ep, "x.json")
    lines = open(ep, encoding="utf-8").read().splitlines()
    chk(all(l.startswith("#") for l in lines[:2]),
        f"주석줄이 따옴표 없이 '#' 로 시작 ({lines[0][:12]!r})")
    parsed = list(csv.DictReader(l for l in open(ep, encoding="utf-8")
                                 if not l.startswith("#")))
    chk(parsed and "dopant" in parsed[0],
        f"'#' 필터만으로 헤더가 잡힌다 ({list(parsed[0])[:3] if parsed else '실패'})")

    import shutil
    shutil.rmtree(td, ignore_errors=True)
    print("selftest " + ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all_csv", default=str(PROP / "cascade_v23_all.csv"))
    ap.add_argument("--esw_json", default=str(PROP / "oxidation_stability_cascade_v2.json"))
    ap.add_argument("--inplace", action="store_true",
                    help="기존 champions.csv / oxidation_stability_cascade.csv 를 덮는다")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    suf = "" if a.inplace else "_v2"
    ch, ntot = build_champions(a.all_csv)
    p1 = PROP / f"cascade_v23_champions{suf}.csv"
    with open(p1, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CHAMP_COLS)
        w.writeheader()
        w.writerows(ch)
    print(f"[champions] {p1}  {len(ch)}행 (전체 {ntot}행 중 rank_combined==1)")

    lit = build_litransport(a.all_csv)
    p3 = PROP / f"cascade_v23_litransport{suf}.csv"
    with open(p3, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LITRANS_COLS)
        w.writeheader()
        w.writerows(lit)
    print(f"[litransport] {p3}  {len(lit)}행")

    rows = build_esw_csv(a.esw_json)
    p2 = PROP / f"oxidation_stability_cascade{suf}.csv"
    write_esw_csv(rows, p2, a.esw_json)
    n_clr = sum(1 for r in rows if r["clrich_ox_V"] != "")
    print(f"[esw]       {p2}  {len(rows)}종 · Cl-rich 비교 가능 {n_clr}종")
    print("다음: python3 tools/figures/plot_cascade_insights.py "
          "→ cascade_v23_ranked.csv → tools/cascade/build_screening_funnel.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
