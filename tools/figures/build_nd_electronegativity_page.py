#!/usr/bin/env python3
"""CEI/Nd — 실험 쪽 1저자에게 보내는 설명 페이지: Nd 계산 결과 (Q1 자리 · Q2 분해 · Q3 전자 배치 · S 빈자리) + 원고 Fig. 3g 의 Li₃Nd 장벽 인용 범위.

2026-10-26 갱신: 처음 판 (10-20) 은 Q3 (Pauling 전기음성도로 읽은 Bader · ELF) 만 실었다. Q1 판독 (10-23) · Q2 판독 (10-26) ·
S 빈자리 마감 비준 (10-22) · Li₃Nd 장벽 인용 결정 (10-26) 을 같은 규칙 (원자료에서 읽고 기록 글자와 대조) 으로 더했다.

    python3 tools/figures/build_nd_electronegativity_page.py                    # 페이지 + Origin CSV 를 쓴다
    python3 tools/figures/build_nd_electronegativity_page.py --artifact_out X   # Artifact 용 본문 (문서 골격 없음) 도 쓴다
    python3 tools/figures/build_nd_electronegativity_page.py --selftest

숫자는 원자료에서 읽는다 (손으로 옮기지 않는다):
    db/raw/nd_q3_bader_2026_10_19/nd_bader_sites.csv · nd_bader_summary.json · scf_input_copy.in (구조 · Bader SCF 설정)
    db/raw/nd_q3_elf_2026_10_19/nd_elf_bonds_mic.csv · scf.in   (결합 중점 ELF · 최소 이미지 고친 판 · ELF SCF 설정)
    db/properties/modelc_elf_bonds.csv                          (호스트 LPSCl1.6 · 같은 NC 규약 · 같은 도구)
    db/properties/nd_q3_bader_elf_runlog_2026_10_19.json        (호스트 Li Bader · PS₄ 단위 합 재현 기준)
    db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json (1저자 카톡 요지 — Pauling 값 대조)
    (10-26) db/properties/ndo_site_dft_v0_readout_2026_10_23.json (site_dg.py 출력 · Q1 ΔG) · ndo_site_dft_runlog_2026_10_15.json (판독 글자 · 카드 §5 문장)
    (10-26) db/properties/nd_q2_decomp_readout_2026_10_26.json · db/raw/nd_q2_decomp_2026_10_23/collect_2026_10_26/decomp_result.json (Q2 Y)
    (10-26) db/properties/nd_s_vacancy_closed_2026_10_20.json (S 빈자리 확정값 · 허용 서술)
    (10-26) db/properties/citation_hazards.json (HZ-li3nd-neb-si-conditional · HZ-sei-neb-retracted) · db/properties/sei_neb.json (Li₃Nd 장벽)
    (10-26) db/governance/decisions.json (Q1 카드 · Q2 카드 · S 빈자리 마감 · Li₃Nd 인용 결정의 지위)

쓰기 전에 거는 검사 (하나라도 어긋나면 아무것도 쓰지 않고 끝 코드 2):
    ① 구조에서 다시 낸 자리 분류 (결과 전 거리 — summary 의 rules_A) = CSV 분류 · 원소 순서 = 구조
    ② PS₄ 단위 합 (P + 결합 S·O) 이 runlog 값을 재현한다 (Nd 이웃 2 · 없음 6 · POS₃ · PO₂S₂ · ±0.0006 e)
       — 그리고 그 기준값 글자가 runlog 에 그대로 있다 (기준을 몰래 바꾸지 못하게)
    ③ 전자 합 = ZVAL 합 ± 0.05 e      ⑥ 자리마다 net = ZVAL − N (±0.002 e)
    ④ ELF 표에 그릴 다섯 결합과 호스트 P–S 가 있다 · 그림 자료에 Li–X 결합이 없다
    ⑤ Pauling 표의 Nd · P · S · O 가 1저자 카톡 요지에 적힌 값과 같다
    ⑦ Q1 원자료 ΔG (site_dg.py) 가 runlog 판독 글자 (+0.490) 와 카드 §5 문장의 값을 재현한다 — 카드가 active 가 아니면 '잠정' 을 단다
    ⑧ Q2 판독 Y = 원자료 (decomp_result.json) · 분해능 밖 · 부피 · 상 이완 점검 통과 · 허용 문장의 크기 = 원자료 · 카드 active
    ⑨ S 빈자리 확정값 (ΔE · n · 문턱) 이 허용 문장과 같고 마감 결정이 active
    ⑩ Li₃Nd 장벽은 CONDITIONAL 항목 (결정 active) 의 SI 문장으로만 — 그 문장의 값 = NEB 기록 · 나머지 NEB 값은 BLOCKED 그대로
    ⑪ (만든 페이지) Li₂S 장벽 0.305 는 어디에도 없다 · 0.229 는 결속 블록 (data-claim · claim-mark) 안에만 있다

이 도구가 못 하는 것:
    · Nd 가 P 자리에 든 모델의 Bader — 계산이 없다. 그림 3 (a) 는 전기음성도 기대만 그린다.
    · Q1 · Q2 를 Q3 (묘사) 와 인과로 잇지 않는다 (카드 §5) — 절마다 따로 읽게 쓴다. 숫자는 카드 §5 허용 문장의 범위만 싣는다.
    · Q1 (Rietveld 5 f.u. 셀 · GBRV/psl 52/520) 과 Q2 · Q3 (9 월 10 f.u. 셀 · PAW 70/560) 는 셀 · 설정이 달라 같은 표에 놓지 않는다.
    · Li₃Nd 장벽의 물리를 판정하지 않는다 — 원장의 인용 범위 (CONDITIONAL 문장) 를 옮길 뿐이다. Li₂S 장벽은 싣지 않는다 (BLOCKED).
    · PS₄ 안 P · S 자리 전하 — Bader 분할 인공물 (runlog ⚠_분할_인공물) 때문에 그리지 않는다. 단위 합만 쓴다.
    · Li–X 중점 ELF — Li 가 작아 중점이 음이온 껍질 안에 든다 (runlog ⛔_읽지_않는_것). 그리지 않는다.
    · Pauling 이온성 % 의 절대 해석 — 표 보기에만 싣고 순서로만 쓴다.
    · ELF cube 를 다시 읽지 않는다 (cube 는 gabia 에만 있다) — 중점 표만 쓴다.
    · 영어 문장의 문법은 사람이 본다 (예시 문장 · 캡션).
"""
import argparse
import csv
import html
import itertools
import json
import math
import pathlib
import re
import shutil
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]

IN = {
    "sites": "db/raw/nd_q3_bader_2026_10_19/nd_bader_sites.csv",
    "summary": "db/raw/nd_q3_bader_2026_10_19/nd_bader_summary.json",
    "struct": "db/raw/nd_q3_bader_2026_10_19/scf_input_copy.in",
    "elf": "db/raw/nd_q3_elf_2026_10_19/nd_elf_bonds_mic.csv",
    "elf_scf": "db/raw/nd_q3_elf_2026_10_19/scf.in",
    "host_elf": "db/properties/modelc_elf_bonds.csv",
    "runlog": "db/properties/nd_q3_bader_elf_runlog_2026_10_19.json",
    "card": "db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json",
    "q1_readout": "db/properties/ndo_site_dft_v0_readout_2026_10_23.json",
    "q1_runlog": "db/properties/ndo_site_dft_runlog_2026_10_15.json",
    "q2_readout": "db/properties/nd_q2_decomp_readout_2026_10_26.json",
    "q2_raw": "db/raw/nd_q2_decomp_2026_10_23/collect_2026_10_26/decomp_result.json",
    "svac": "db/properties/nd_s_vacancy_closed_2026_10_20.json",
    "hazards": "db/properties/citation_hazards.json",
    "neb": "db/properties/sei_neb.json",
    "decisions": "db/governance/decisions.json",
}
OUT_DIR = "db/properties/cei_figs"
OUT_PAGE = "cei_nd_electronegativity.html"
CSV_PREFIX = "cei_nd_en_"

TITLE = "Nd in LPSCl1.6"
DESCRIPTION = ("Site preference, decomposition and electron distribution of Nd in Nd/O-doped LPSCl1.6, with the citation "
               "range for the Li3Nd barrier, written for the experimental first author.")
FONTS = ("https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600"
         "&family=IBM+Plex+Sans+KR:wght@400;600;700&display=swap")

# Pauling 척도. Nd · P · S · O 는 1저자 카톡 요지의 값과 같아야 한다 (검사 ⑤). Li · Cl 은 같은 표준 표의 값.
PAULING = {"Li": 0.98, "Nd": 1.14, "P": 2.19, "S": 2.58, "Cl": 3.16, "O": 3.44}
FIRST_AUTHOR_EN = ("Nd", "P", "S", "O")

# Δχ 그림 — 음이온별 묶음. 이 셀에 실제로 있는 결합만 (ELF 표의 결합 종류와 같다).
DCHI_GROUPS = (("S", ("P", "Nd", "Li")), ("O", ("P", "Nd", "Li")), ("Cl", ("Nd", "Li")))

# ELF 그림에 싣는 결합. ⛔ Li–X 는 넣지 않는다 (검사 ④).
ELF_PLOT = ("P-S", "O-P", "Nd-S", "Cl-Nd", "Nd-O")

# 재현 기준 — runlog 'Bader_결과_2026_10_19 · 단위_전하_결과_후_추가' 의 값 (검사 ② 가 그 글자도 확인한다).
UNIT_REF = {"near": (-2.442, -2.407), "far_n": 6, "far_min": -2.651, "far_max": -2.585,
            "PO": {"POSSS": -2.447, "POOSS": -2.564}}
UNIT_TOL = 6e-4

SUP = {"S": "S²⁻", "Cl": "Cl⁻", "O": "O²⁻"}


class CheckError(Exception):
    pass


# ── 작은 도우미 ────────────────────────────────────────────────────────────
def esc(s):
    return html.escape(str(s), quote=True)


def mn(s):
    """숫자 글자의 hyphen-minus 를 참 마이너스 (U+2212) 로."""
    return str(s).replace("-", "−")


def fnum(x, nd=2, sign=False):
    return mn(f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}")


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs)


def dchi(cation, anion):
    return round(PAULING[anion] - PAULING[cation], 2)


def ionic_pct(d):
    """Pauling 의 어림식 1 − exp(−Δχ²/4) · 순서로만 쓴다."""
    return 100.0 * (1.0 - math.exp(-d * d / 4.0))


# ── 읽기 ────────────────────────────────────────────────────────────────────
def read_qe_input(path):
    """QE 입력에서 ecut · smearing · K_POINTS · CELL_PARAMETERS · ATOMIC_POSITIONS (angstrom) 를 읽는다."""
    lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
    out = {"ecutwfc": None, "ecutrho": None, "smearing": None, "degauss": None, "k": None,
           "cell": None, "cell_unit": None, "species": [], "cart": [], "pos_unit": None}
    for i, line in enumerate(lines):
        s = line.strip()
        for key in ("ecutwfc", "ecutrho", "degauss"):
            m = re.search(key + r"\s*=\s*([0-9.]+)", s)
            if m:
                out[key] = float(m.group(1))
        m = re.search(r"smearing\s*=\s*'([a-z-]+)'", s)
        if m:
            out["smearing"] = m.group(1)
        if s.startswith("K_POINTS"):
            out["k"] = tuple(int(x) for x in lines[i + 1].split()[:3])
        if s.startswith("CELL_PARAMETERS"):
            out["cell_unit"] = s
            out["cell"] = [[float(x) for x in lines[i + j].split()[:3]] for j in (1, 2, 3)]
        if s.startswith("ATOMIC_POSITIONS"):
            out["pos_unit"] = s
            for l2 in lines[i + 1:]:
                p = l2.split()
                if len(p) < 4 or not re.fullmatch(r"[A-Z][a-z]?", p[0]):
                    break
                out["species"].append(p[0])
                out["cart"].append([float(x) for x in p[1:4]])
    return out


def read_csv_rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(line for line in f if not line.startswith("#")))


def read_sites(path):
    rows = read_csv_rows(path)
    for r in rows:
        r["index"] = int(r["index"])
        for k in ("net_e", "N_bader_e", "V_bader_A3", "N_per_V_e_A3", "d_Nd_min_A"):
            r[k] = float(r[k])
    return rows


# ── 기하 (stdlib · 최소 이미지) ────────────────────────────────────────────
def inv3(m):
    a, b, c = m[0]
    d, e, f = m[1]
    g, h, i = m[2]
    det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    return [[(e * i - f * h) / det, (c * h - b * i) / det, (b * f - c * e) / det],
            [(f * g - d * i) / det, (a * i - c * g) / det, (c * d - a * f) / det],
            [(d * h - e * g) / det, (b * g - a * h) / det, (a * e - b * d) / det]]


def to_frac(cart, ci):
    return [sum(cart[k] * ci[k][j] for k in range(3)) for j in range(3)]


def mic(fa, fb, cell):
    d = [fb[j] - fa[j] for j in range(3)]
    d = [x - round(x) for x in d]
    best = 1e9
    for s in itertools.product((-1, 0, 1), repeat=3):
        v = [d[j] + s[j] for j in range(3)]
        x = [sum(v[k] * cell[k][j] for k in range(3)) for j in range(3)]
        best = min(best, math.sqrt(x[0] ** 2 + x[1] ** 2 + x[2] ** 2))
    return best


def classify(sp, fr, cell, rules):
    """runlog 'Bader_계획_결과_전 · 자리_분류_결과_전' 의 규칙: 거리 하나 (각도 안 봄)."""
    idx = {}
    for k, e in enumerate(sp):
        idx.setdefault(e, []).append(k)

    def near(k, elem, r):
        return any(mic(fr[k], fr[m], cell) < r for m in idx.get(elem, []))

    cats = []
    for k, e in enumerate(sp):
        if e == "S":
            c = ("S_PS4" if near(k, "P", rules["R_PS"]) else "S_free") + ("_nearNd" if near(k, "Nd", rules["R_NdX"]) else "")
        elif e == "Cl":
            c = "Cl" + ("_nearNd" if near(k, "Nd", rules["R_NdX"]) else "")
        elif e == "O":
            c = ("O_P" if near(k, "P", rules["R_PO"]) else "O_free") + ("_nearNd" if near(k, "Nd", rules["R_NdO"]) else "")
        elif e == "P":
            c = "P_withO" if near(k, "O", rules["R_PO"]) else "P_S4"
        else:
            c = e
        cats.append(c)
    return cats


def ps4_units(sp, fr, cell, net, cats, rules):
    units = []
    for p in (k for k, e in enumerate(sp) if e == "P"):
        mem = [k for k, e in enumerate(sp)
               if (e == "S" and mic(fr[p], fr[k], cell) < rules["R_PS"])
               or (e == "O" and mic(fr[p], fr[k], cell) < rules["R_PO"])]
        units.append({"p_index": p + 1, "members": [m + 1 for m in mem],
                      "comp": "P" + "".join(sorted(sp[m] for m in mem)),
                      "total": net[p] + sum(net[m] for m in mem),
                      "near_nd": any(cats[m].endswith("_nearNd") for m in mem)})
    return units


def nd_neighbours(sp, fr, cell, cats, rules):
    out = []
    for k, e in enumerate(sp):
        if e != "Nd":
            continue
        nb = []
        for m, em in enumerate(sp):
            if m == k:
                continue
            d = mic(fr[k], fr[m], cell)
            if (em in ("S", "Cl") and d < rules["R_NdX"]) or (em == "O" and d < rules["R_NdO"]):
                nb.append((d, em, cats[m], m + 1))
        out.append({"index": k + 1, "neighbours": sorted(nb)})
    return out


# ── 검사 + 파생 ─────────────────────────────────────────────────────────────
def check_pauling(card):
    txt = " ".join(card["1저자_카톡_요지_2026_10_14"])
    m = re.search(r"Pauling ([^)]*)\)", txt)
    if not m:
        raise CheckError("⑤ 카드의 1저자 카톡 요지에서 Pauling 값을 못 찾았다")
    got = {e: float(v) for e, v in re.findall(r"\b(Nd|P|S|O) (\d\.\d\d)", m.group(1))}
    for e in FIRST_AUTHOR_EN:
        if e not in got or abs(got[e] - PAULING[e]) > 1e-9:
            raise CheckError(f"⑤ Pauling {e}: 표 {PAULING.get(e)} ≠ 1저자 카톡 요지 {got.get(e)}")
    return got


Q1_CARD = "D-2026-10-14-ndo-site-stability-estimand"
Q2_CARD = "D-2026-10-23-nd-q2-decomp-card"
SVAC_DEC = "D-2026-10-20-nd-s-vacancy-closed"
LI3ND_DEC = "D-2026-10-26-li3nd-neb-si-conditional"
HZ_LI3ND, HZ_NEB = "HZ-li3nd-neb-si-conditional", "HZ-sei-neb-retracted"
NEB_KEY = "v2_ccpath/li3nd"
KB_EV, NU0 = 8.617333262e-5, 1e13          # 홉 수 검산 (D-2026-09-27-barrier-hop-count · ν₀ 가정)


def derive_results(p):
    """Q1 · Q2 · S 빈자리 · Li₃Nd — 원자료에서 읽고 기록 글자와 대조한다 (⑦–⑩). 어긋나면 CheckError."""
    rd = lambda k: json.loads(p(k).read_text(encoding="utf-8"))
    dec = {d["id"]: d for d in rd("decisions")["decisions"]}

    def state(i, tag):
        if i not in dec:
            raise CheckError(f"{tag} 결정 {i} 이 원장에 없다")
        return dec[i].get("decision_state")

    # ⑦ Q1 — site_dg.py 출력 · runlog 판독 · 카드 §5 문장
    nd = rd("q1_readout")["dopants"]["Nd"]
    dg = float(nd["dG_site_eV_per_dopant"])
    rl = rd("q1_runlog")["✅_Q1_EOS_판독_2026_10_23"]
    if f"{dg:+.3f}" not in rl["ΔG_site"]:
        raise CheckError(f"⑦ Q1 원자료 ΔG {dg:+.3f} 이 runlog 판독 글자와 다르다")
    m = re.search(r"'([^']+)'", rl["카드_5_문장"])
    if not m or f"{dg:.2f} eV/Nd" not in m.group(1):
        raise CheckError("⑦ Q1 카드 §5 문장에 원자료 값이 없다")
    cl = nd["closure"]
    q1 = {"dG": dg, "sentence": m.group(1), "provisional": state(Q1_CARD, "⑦") != "active",
          "top": {k: v["top"][0] for k, v in nd["models"].items()}, "a_li2s": cl["a_Li2S"], "b_li3ps4": cl["b_Li3PS4"],
          "n_nd": cl["n_dopant"]}

    # ⑧ Q2 — 판독 · 원자료 decomp_result.json
    r2, raw_all = rd("q2_readout"), rd("q2_raw")
    raw, products = raw_all["pair"], list(raw_all["basis"])
    if len(products) != 5:
        raise CheckError(f"⑧ Q2 생성물이 {len(products)} 개다 — 페이지 문장 (다섯) 과 다르다")
    y = float(r2["Y_meV_per_atom"]["보정_B25"])
    if abs(y - float(raw["Y_report_meV_per_atom"])) > 1e-3:
        raise CheckError(f"⑧ Q2 판독 Y {y} 가 원자료 {raw['Y_report_meV_per_atom']} 와 다르다")
    if raw["within_resolution"] or not raw["G_V_pass"] or not raw["G_phase_pass"]:
        raise CheckError("⑧ Q2 원자료가 분해능 안이거나 부피 · 상 이완 점검을 통과하지 못했다")
    sent2 = r2["허용_문장(카드_§5·구조_결정_①)"]
    if f"{abs(y):.0f} meV/atom" not in sent2:
        raise CheckError("⑧ Q2 허용 문장의 크기가 원자료와 다르다")
    if state(Q2_CARD, "⑧") != "active":
        raise CheckError("⑧ Q2 카드가 active 가 아니다")
    q2 = {"Y": y, "Y_raw": float(raw["Y_raw_meV_per_atom"]), "res": float(raw["resolution_meV"]), "sentence": sent2,
          "products": products}

    # ⑨ S 빈자리 — 마감 확정값 · 허용 서술
    sv = rd("svac")
    fx, st_ = sv["1_확정값"], sv["2_허용_서술(이대로만)"][0]
    de_ = float(fx["ΔE_vac(S)_옆_빼기_먼_eV"])
    if mn(f"{de_:.2f} eV") not in st_ or f"n {fx['n']}" not in st_ or fx["갈래"] != "구분 안 됨":
        raise CheckError("⑨ S 빈자리 확정값과 허용 문장이 맞지 않는다")
    if abs(de_) >= float(fx["문턱_eV"]):
        raise CheckError("⑨ S 빈자리 차가 문턱 밖인데 '구분 안 됨' 으로 적혀 있다")
    if state(SVAC_DEC, "⑨") != "active":
        raise CheckError("⑨ S 빈자리 마감 결정이 active 가 아니다")
    svac = {"dE": de_, "thr": float(fx["문턱_eV"]), "n": fx["n"], "sentence": st_}

    # ⑩ Li₃Nd — CONDITIONAL 항목의 SI 문장으로만
    hz = {h["id"]: h for h in rd("hazards")["hazards"] if "id" in h}
    c, b = hz.get(HZ_LI3ND), hz.get(HZ_NEB)
    if not c or c.get("level") != "CONDITIONAL" or state(LI3ND_DEC, "⑩") != "active":
        raise CheckError("⑩ Li₃Nd 장벽의 인용 항목이 CONDITIONAL (결정 active) 이 아니다 — 페이지에 싣지 않는다")
    if not b or b.get("level") != "BLOCKED":
        raise CheckError("⑩ 나머지 NEB 값 (Li₂S 포함) 의 BLOCKED 항목이 없다")
    ea = float(rd("neb")["results"][NEB_KEY]["Ea_effective_eV"])
    m = re.search(r'"(For a hypothetical[^"]+)"', c["fix"])
    if not m or f"{ea:.3f} eV" not in m.group(1):
        raise CheckError("⑩ CONDITIONAL 항목의 SI 문장 값이 NEB 기록과 다르다")
    rate = NU0 * math.exp(-ea / (KB_EV * 298.0))
    li3nd = {"ea": ea, "si": m.group(1), "rate": rate, "wait": 1.0 / rate}
    return {"q1": q1, "q2": q2, "svac": svac, "li3nd": li3nd}


def derive(root=REPO):
    root = pathlib.Path(root)

    def p(key):
        return root / IN[key]

    summ = json.loads(p("summary").read_text(encoding="utf-8"))
    rules = summ["sites"]["rules_A"]
    zval = summ["zval_used"]
    st = read_qe_input(p("struct"))
    if "angstrom" not in (st["cell_unit"] or "") or "angstrom" not in (st["pos_unit"] or ""):
        raise CheckError("① 구조 입력의 단위가 angstrom 이 아니다")
    rows = read_sites(p("sites"))
    elf = {r["bond"]: r for r in read_csv_rows(p("elf"))}
    host = {r["bond"]: r for r in read_csv_rows(p("host_elf"))}
    runlog = json.loads(p("runlog").read_text(encoding="utf-8"))
    card = json.loads(p("card").read_text(encoding="utf-8"))
    elf_in = read_qe_input(p("elf_scf"))

    check_pauling(card)                                                       # ⑤

    sp, cell = st["species"], st["cell"]
    ci = inv3(cell)
    fr = [to_frac(x, ci) for x in st["cart"]]
    if [r["element"] for r in rows] != sp:                                    # ①
        raise CheckError("① CSV 원소 순서가 구조와 다르다")
    cats = classify(sp, fr, cell, rules)
    bad = [(r["index"], r["category"], c) for r, c in zip(rows, cats) if r["category"] != c]
    if bad:
        raise CheckError(f"① 자리 분류가 구조에서 다시 낸 것과 다르다 ({len(bad)} 개): {bad[:4]}")

    for r in rows:                                                            # ⑥
        if abs(zval[r["element"]] - r["N_bader_e"] - r["net_e"]) > 2e-3:
            raise CheckError(f"⑥ 자리 {r['index']} net ≠ ZVAL − N")
    tot_n = sum(r["N_bader_e"] for r in rows)                                 # ③
    tot_z = sum(zval[r["element"]] for r in rows)
    if abs(tot_n - tot_z) > 0.05:
        raise CheckError(f"③ 전자 합 {tot_n:.4f} ≠ ZVAL 합 {tot_z} (± 0.05)")

    net = [r["net_e"] for r in rows]                                          # ②
    units = ps4_units(sp, fr, cell, net, cats, rules)
    near = sorted(u["total"] for u in units if u["comp"] == "PSSSS" and u["near_nd"])
    far = sorted(u["total"] for u in units if u["comp"] == "PSSSS" and not u["near_nd"])
    ok = (len(near) == 2 and all(abs(a - b) < UNIT_TOL for a, b in zip(near, sorted(UNIT_REF["near"])))
          and len(far) == UNIT_REF["far_n"] and abs(far[0] - UNIT_REF["far_min"]) < UNIT_TOL
          and abs(far[-1] - UNIT_REF["far_max"]) < UNIT_TOL)
    for comp, ref in UNIT_REF["PO"].items():
        got = [u["total"] for u in units if u["comp"] == comp]
        ok = ok and len(got) == 1 and abs(got[0] - ref) < UNIT_TOL
    if not ok:
        raise CheckError(f"② PS₄ 단위 합이 runlog 를 재현하지 못한다: 이웃 {near} · 없음 {far}")
    ref_txt = runlog["Bader_결과_2026_10_19"]["단위_전하_결과_후_추가"]
    for v in (*UNIT_REF["near"], UNIT_REF["far_min"], UNIT_REF["far_max"], *UNIT_REF["PO"].values()):
        if mn(f"{v:.3f}") not in ref_txt:
            raise CheckError(f"② 재현 기준 {v} 이 runlog 글자에 없다 — 기준이 기록과 갈렸다")

    for b in ELF_PLOT:                                                        # ④
        if b not in elf:
            raise CheckError(f"④ ELF 표에 {b} 가 없다")
        if "Li" in b.split("-"):
            raise CheckError(f"④ Li–X 결합 {b} 은 그림에 싣지 않는다 (중점이 음이온 껍질 안)")
    if "P-S" not in host:
        raise CheckError("④ 호스트 ELF 표에 P-S 가 없다")

    m = re.search(r"LPSCl16: Li \+([0-9.]+)", runlog["Bader_결과_2026_10_19"]["사전등록_비교_그대로"])
    if not m:
        raise CheckError("runlog 에서 호스트 Li Bader 값을 못 찾았다")
    host_li = float(m.group(1))

    by = {}
    for r in rows:
        by.setdefault(r["category"], []).append(r)

    # 그림 4 — 음이온 이동 (Li 만 이웃한 같은 종류 평균에서)
    def site_class(name, ref_c, near_c, short):
        ref_v = [(r["net_e"], f"{short} {r['index']}") for r in by[ref_c]]
        near_v = [(r["net_e"], f"{short} {r['index']}") for r in by[near_c]]
        return {"name": name, "ref": ref_v, "near": near_v}

    unit_cls = {"name": "PS₄ unit (P + 4 S)",
                "ref": [(u["total"], f"P {u['p_index']} unit") for u in units if u["comp"] == "PSSSS" and not u["near_nd"]],
                "near": [(u["total"], f"P {u['p_index']} unit") for u in units if u["comp"] == "PSSSS" and u["near_nd"]]}
    shift = [site_class("Free S²⁻", "S_free", "S_free_nearNd", "atom"), unit_cls,
             site_class("Cl⁻", "Cl", "Cl_nearNd", "atom"), site_class("O bonded to P", "O_P", "O_P_nearNd", "atom")]
    for c in shift:
        c["ref_mean"] = mean(v for v, _ in c["ref"])
        c["near_mean"] = mean(v for v, _ in c["near"])
        c["shift"] = c["near_mean"] - c["ref_mean"]

    # 그림 5 — 양이온이 내준 몫
    li_mean = mean(r["net_e"] for r in by["Li"])
    nd_rows = sorted(by["Nd"], key=lambda r: r["index"])
    cation = {"li_mean": li_mean, "li_n": len(by["Li"]), "host_li": host_li,
              "nd": [(r["index"], r["net_e"]) for r in nd_rows], "nd_mean": mean(r["net_e"] for r in nd_rows),
              "li_V": mean(r["V_bader_A3"] for r in by["Li"]), "nd_V": mean(r["V_bader_A3"] for r in nd_rows)}

    # 그림 6 — 밀도 = 전자 수 / Bader 부피
    def dens(ref_c, near_c):
        out = {"n_ref": len(by[ref_c]), "n_near": len(by[near_c])}
        for key, fld in (("N", "N_bader_e"), ("V", "V_bader_A3"), ("NV", "N_per_V_e_A3")):
            a, b = mean(r[fld] for r in by[ref_c]), mean(r[fld] for r in by[near_c])
            out[key] = {"ref": a, "near": b, "pct": 100.0 * (b / a - 1.0)}
        return out

    density = {"S": dens("S_free", "S_free_nearNd"), "Cl": dens("Cl", "Cl_nearNd"), "O": dens("O_P", "O_P_nearNd")}

    elf_rows = [{"bond": b, "n": int(elf[b]["n_bonds"]), "d": float(elf[b]["mean_dist_A"]),
                 "mid": float(elf[b]["ELF_midpoint"]), "sd": float(elf[b]["ELF_mid_std"])} for b in ELF_PLOT]
    host_ps = {"n": int(host["P-S"]["n_bonds"]), "d": float(host["P-S"]["mean_dist_A"]),
               "mid": float(host["P-S"]["ELF_midpoint"]), "sd": float(host["P-S"]["ELF_mid_std"])}

    bonds = []
    for an, cats_ in DCHI_GROUPS:
        for ca in cats_:
            d = dchi(ca, an)
            bonds.append({"anion": an, "cation": ca, "bond": f"{ca}–{an}", "dchi": d, "pct": ionic_pct(d)})

    out = {"rules": rules, "tot_n": tot_n, "tot_z": tot_z, "units": units, "shift": shift, "cation": cation,
           "density": density, "elf": elf_rows, "host_ps": host_ps, "bonds": bonds,
           "nd_nb": nd_neighbours(sp, fr, cell, cats, rules), "bader_in": st, "elf_in": elf_in,
           "n_atoms": len(sp), "formula": formula(sp)}
    out.update(derive_results(p))                                             # ⑦–⑩ (2026-10-26)
    return out


def subf(f):
    """'Li3PS4' → 'Li₃PS₄'."""
    return f.translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))


def formula(sp):
    order = ("Li", "Nd", "P", "O", "S", "Cl")
    sub = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    return "".join(f"{e}{str(sp.count(e)).translate(sub)}" for e in order if sp.count(e))


# ── SVG ─────────────────────────────────────────────────────────────────────
def bar_path(xa, xb, yc, h, r=4.0):
    """막대 — 데이터 끝만 4 px 둥글게, 바닥선 쪽은 각지게."""
    top, bot = yc - h / 2, yc + h / 2
    r = min(r, abs(xb - xa) / 2, h / 2)
    s = 1 if xb >= xa else -1
    return (f"M{xa:.1f},{top:.1f}H{xb - s * r:.1f}Q{xb:.1f},{top:.1f} {xb:.1f},{top + r:.1f}"
            f"V{bot - r:.1f}Q{xb:.1f},{bot:.1f} {xb - s * r:.1f},{bot:.1f}H{xa:.1f}Z")


def hit_open(tip_v, tip_l):
    return (f'<g class="hit" tabindex="0" role="img" aria-label="{esc(tip_l)}, {esc(tip_v)}" '
            f'data-v="{esc(tip_v)}" data-l="{esc(tip_l)}">')


def hbars(rows, *, x0, x1, ticks, tick_text, aria, width=640, label_w=178, right_w=66,
          row_h=34, bar_h=12, header_h=28, top=34, ref_lines=(), axis_label=""):
    """가로 막대. rows: {'header': 글} 또는 {label, sub, value, err, cls, vtext, tip_v, tip_l}."""
    pl, pr = label_w, width - right_w

    def X(v):
        return pl + (v - x0) / (x1 - x0) * (pr - pl)

    base = 0.0 if x0 <= 0 <= x1 else x0
    y, laid = top, []
    for r in rows:
        laid.append(("h" if "header" in r else "b", y, r))
        y += header_h if "header" in r else row_h
    gy0, gy1 = top - 6, y
    H = gy1 + (44 if axis_label else 28)
    o = [f'<svg viewBox="0 0 {width} {H}" role="img" aria-label="{esc(aria)}" xmlns="http://www.w3.org/2000/svg">',
         f"<title>{esc(aria)}</title>"]
    # 격자선 · 기준선은 막대 행 높이에만 긋는다 — 머리 행 글자를 가로지르지 않게
    spans = [(yy, yy + row_h) for kind, yy, _r in laid if kind == "b"]
    for t in ticks:
        cls = "ax0" if abs(t - base) < 1e-12 else "ax"
        for ya, yb in spans:
            o.append(f'<line class="{cls}" x1="{X(t):.1f}" y1="{ya}" x2="{X(t):.1f}" y2="{yb}"/>')
        o.append(f'<text class="tk" x="{X(t):.1f}" y="{gy1 + 18}" text-anchor="middle">{esc(tick_text(t))}</text>')
    if axis_label:
        o.append(f'<text class="tk" x="{(pl + pr) / 2:.1f}" y="{gy1 + 38}" text-anchor="middle">{esc(axis_label)}</text>')
    for v, lab, *anchor in ref_lines:  # (값, 글[, "end"]) — "end" 면 글을 선 왼쪽에 붙인다 (오른쪽 끝 넘침 방지)
        for ya, yb in spans:
            o.append(f'<line class="refline" x1="{X(v):.1f}" y1="{ya}" x2="{X(v):.1f}" y2="{yb}"/>')
        if anchor and anchor[0] == "end":
            o.append(f'<text class="tk" x="{X(v) - 6:.1f}" y="{gy0 - 4}" text-anchor="end">{esc(lab)}</text>')
        else:
            o.append(f'<text class="tk" x="{X(v) + 6:.1f}" y="{gy0 - 4}">{esc(lab)}</text>')
    for kind, yy, r in laid:
        if kind == "h":
            o.append(f'<text class="hd" x="2" y="{yy + 19}">{esc(r["header"])}</text>')
            continue
        cy = yy + row_h / 2
        if r.get("sub"):
            o.append(f'<text class="lb" x="{pl - 12}" y="{cy - 2:.1f}" text-anchor="end">{esc(r["label"])}</text>')
            o.append(f'<text class="lb2" x="{pl - 12}" y="{cy + 12:.1f}" text-anchor="end">{esc(r["sub"])}</text>')
        else:
            o.append(f'<text class="lb" x="{pl - 12}" y="{cy + 4.5:.1f}" text-anchor="end">{esc(r["label"])}</text>')
        v, err = r["value"], r.get("err") or 0.0
        o.append(hit_open(r["tip_v"], r["tip_l"]))
        o.append(f'<rect class="hitbox" x="{pl}" y="{yy}" width="{pr - pl}" height="{row_h}"/>')
        o.append(f'<path class="mk {r["cls"]}" d="{bar_path(X(base), X(v), cy, bar_h)}"/>')
        if err:
            xa, xb = X(v - err), X(v + err)
            o.append(f'<line class="err" x1="{xa:.1f}" y1="{cy:.1f}" x2="{xb:.1f}" y2="{cy:.1f}"/>'
                     f'<line class="err" x1="{xa:.1f}" y1="{cy - 5:.1f}" x2="{xa:.1f}" y2="{cy + 5:.1f}"/>'
                     f'<line class="err" x1="{xb:.1f}" y1="{cy - 5:.1f}" x2="{xb:.1f}" y2="{cy + 5:.1f}"/>')
        o.append("</g>")
        if v >= base:
            o.append(f'<text class="val" x="{X(v + err) + 7:.1f}" y="{cy + 4.5:.1f}">{esc(r["vtext"])}</text>')
        else:
            o.append(f'<text class="val" x="{X(v - err) - 7:.1f}" y="{cy + 4.5:.1f}" text-anchor="end">{esc(r["vtext"])}</text>')
    o.append("</svg>")
    return "\n".join(o)


def dotplot(classes, *, x0, x1, ticks, aria, width=640, label_w=178, right_w=78, row_h=60, top=34):
    """그림 4 — 행 = 음이온 종류, 위 줄 = Li 만 이웃 (빈 원), 아래 줄 = Nd 이웃 (마름모)."""
    pl, pr = label_w, width - right_w

    def X(v):
        return pl + (v - x0) / (x1 - x0) * (pr - pl)

    gy0, gy1 = top - 6, top + row_h * len(classes)
    H = gy1 + 44
    o = [f'<svg viewBox="0 0 {width} {H}" role="img" aria-label="{esc(aria)}" xmlns="http://www.w3.org/2000/svg">',
         f"<title>{esc(aria)}</title>"]
    for t in ticks:
        cls = "ax0" if abs(t) < 1e-12 else "ax"
        o.append(f'<line class="{cls}" x1="{X(t):.1f}" y1="{gy0}" x2="{X(t):.1f}" y2="{gy1}"/>')
        o.append(f'<text class="tk" x="{X(t):.1f}" y="{gy1 + 18}" text-anchor="middle">{esc(fnum(t, 1, sign=t != 0) if t else "0")}</text>')
    o.append(f'<text class="tk" x="{X(0) + 6:.1f}" y="{gy0 - 10}">Li-only mean</text>')
    o.append(f'<text class="tk" x="{(pl + pr) / 2:.1f}" y="{gy1 + 38}" text-anchor="middle">'
             f'Shift in Bader charge (e), positive = fewer electrons on the anion</text>')
    for i, c in enumerate(classes):
        yy = top + i * row_h
        cy = yy + row_h / 2
        o.append(f'<text class="lb" x="{pl - 12}" y="{cy - 2:.1f}" text-anchor="end">{esc(c["name"])}</text>')
        o.append(f'<text class="lb2" x="{pl - 12}" y="{cy + 12:.1f}" text-anchor="end">'
                 f'n {len(c["near"])} vs {len(c["ref"])}</text>')
        if i:
            o.append(f'<line class="ax" x1="0" y1="{yy}" x2="{width}" y2="{yy}"/>')
        y_ref, y_nd = yy + 20, yy + 41
        last, lane = -1e9, 0
        for v, lab in sorted(c["ref"]):
            x = X(v - c["ref_mean"])
            lane = (lane + 1) % 3 if x - last < 7 else 0
            last = x
            yj = y_ref + (0, -4, 4)[lane]
            o.append(hit_open(f"{fnum(v, 3)} e (shift {fnum(v - c['ref_mean'], 3, sign=True)})",
                              f"{c['name']}, Li neighbours only, {lab}"))
            o.append(f'<circle class="hitbox" cx="{x:.1f}" cy="{yj:.1f}" r="12"/>'
                     f'<circle class="mk ring" cx="{x:.1f}" cy="{yj:.1f}" r="4.5"/></g>')
        for v, lab in sorted(c["near"]):
            x = X(v - c["ref_mean"])
            o.append(hit_open(f"{fnum(v, 3)} e (shift {fnum(v - c['ref_mean'], 3, sign=True)})",
                              f"{c['name']}, next to Nd, {lab}"))
            o.append(f'<circle class="hitbox" cx="{x:.1f}" cy="{y_nd:.1f}" r="12"/>'
                     f'<rect class="mk dia" x="{x - 5:.1f}" y="{y_nd - 5:.1f}" width="10" height="10" '
                     f'transform="rotate(45 {x:.1f} {y_nd:.1f})"/></g>')
        xm = X(c["shift"])
        o.append(f'<line class="meanbar" x1="{xm:.1f}" y1="{y_nd - 10:.1f}" x2="{xm:.1f}" y2="{y_nd + 10:.1f}"/>')
        xmax = X(max(v for v, _ in c["near"]) - c["ref_mean"])
        o.append(f'<text class="val" x="{max(xmax, xm) + 12:.1f}" y="{y_nd + 4.5:.1f}">{esc(fnum(c["shift"], 2, sign=True))} e</text>')
    o.append("</svg>")
    return "\n".join(o)


def scale_svg(aria):
    """그림 1 — Pauling 척도 한 줄."""
    width, pl, pr, x0, x1, ay = 640, 40, 600, 0.8, 3.6, 98

    def X(v):
        return pl + (v - x0) / (x1 - x0) * (pr - pl)

    role = {"Nd": "nd", "Li": "host", "P": "host"}
    o = [f'<svg viewBox="0 0 {width} 168" role="img" aria-label="{esc(aria)}" xmlns="http://www.w3.org/2000/svg">',
         f"<title>{esc(aria)}</title>",
         f'<line class="ax0" x1="{pl}" y1="{ay}" x2="{pr}" y2="{ay}"/>']
    t = 1.0
    while t <= 3.5 + 1e-9:
        o.append(f'<line class="ax0" x1="{X(t):.1f}" y1="{ay - 4}" x2="{X(t):.1f}" y2="{ay + 4}"/>')
        t += 0.5
    o.append(f'<text class="tk" x="{pr}" y="160" text-anchor="end">Pauling electronegativity χ (ticks every 0.5)</text>')
    for (a, b) in (("Li", "Nd"), ("Nd", "P")):
        xa, xb = X(PAULING[a]), X(PAULING[b])
        o.append(f'<path class="arrow" d="M{xa:.1f},50 V44 H{xb:.1f} V50"/>')
        o.append(f'<text class="val" x="{(xa + xb) / 2:.1f}" y="37" text-anchor="middle">Δχ {fnum(PAULING[b] - PAULING[a], 2)}</text>')
    last_x, level = -1e9, 0
    for e, v in sorted(PAULING.items(), key=lambda kv: kv[1]):
        x = X(v)
        level = 1 - level if x - last_x < 40 else 0
        last_x = x
        cls = role.get(e)
        mark = (f'<circle class="mk {cls}" cx="{x:.1f}" cy="{ay}" r="8"/>' if cls
                else f'<circle class="mk ring" cx="{x:.1f}" cy="{ay}" r="7"/>')
        o.append(hit_open(f"χ = {v:.2f}", f"{e} (Pauling)"))
        o.append(f'<circle class="hitbox" cx="{x:.1f}" cy="{ay}" r="14"/>{mark}</g>')
        o.append(f'<text class="sym" x="{x:.1f}" y="{ay - 18}" text-anchor="middle">{e}</text>')
        o.append(f'<text class="val" x="{x:.1f}" y="{ay + 26 + 15 * level}" text-anchor="middle">{v:.2f}</text>')
    o.append("</svg>")
    return "\n".join(o)


def cluster(o, cx, cy, center, cls_center, r_c):
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        sx, sy = cx + 46 * math.cos(a), cy + 46 * math.sin(a)
        o.append(f'<line class="bond" x1="{cx:.1f}" y1="{cy:.1f}" x2="{sx:.1f}" y2="{sy:.1f}"/>')
    for ang in (45, 135, 225, 315):
        a = math.radians(ang)
        sx, sy = cx + 46 * math.cos(a), cy + 46 * math.sin(a)
        o.append(f'<circle class="atom-s" cx="{sx:.1f}" cy="{sy:.1f}" r="12"/>'
                 f'<text class="atxt" x="{sx:.1f}" y="{sy + 4.5:.1f}" text-anchor="middle">S</text>')
    o.append(f'<circle class="{cls_center}" cx="{cx}" cy="{cy}" r="{r_c}"/>'
             f'<text class="on" x="{cx}" y="{cy + 5}" text-anchor="middle">{center}</text>')


def replace_svg(kind):
    """그림 3 — Nd 가 무엇을 대신하나 (도식 · 자료 아님)."""
    if kind == "P":
        title, subtitle, old = "(a) Nd on the P site", "Rietveld model (4b)", "P"
        lines = (f"S bonds to Nd instead of P", f"Δχ {dchi('P', 'S'):.2f} → {dchi('Nd', 'S'):.2f} (larger)",
                 "S expected to gain electrons")
        pill, pill_cls = "Not computed yet", "pill-open"
    else:
        title, subtitle, old = "(b) Nd on a Li site", "DFT model on this page", "Li"
        lines = (f"S bonds to Nd instead of Li", f"Δχ {dchi('Li', 'S'):.2f} → {dchi('Nd', 'S'):.2f} (slightly smaller)",
                 "S expected to lose a little")
        pill, pill_cls = "Computed, see Fig. 4", "pill-ok"
    aria = f"{title}. {subtitle}. " + ". ".join(lines) + f". {pill}."
    o = [f'<svg viewBox="0 0 300 262" role="img" aria-label="{esc(aria)}" xmlns="http://www.w3.org/2000/svg">',
         f"<title>{esc(aria)}</title>",
         f'<text class="hd" x="150" y="20" text-anchor="middle">{esc(title)}</text>',
         f'<text class="lb2" x="150" y="37" text-anchor="middle">{esc(subtitle)}</text>']
    cluster(o, 68, 106, old, "atom-c", 17)
    o.append('<path class="arrow" d="M124,106 H170"/><path class="arrowhead" d="M178,106 L168,100 L168,112 Z"/>')
    cluster(o, 232, 106, "Nd", "atom-nd", 19)
    for k, s in enumerate(lines):
        o.append(f'<text class="{"lb" if k < 2 else "hd"}" x="150" y="{186 + 18 * k}" text-anchor="middle">{esc(s)}</text>')
    o.append(f'<rect class="{pill_cls}" x="70" y="232" width="160" height="24" rx="12"/>'
             f'<text class="lb2 pilltxt" x="150" y="248.5" text-anchor="middle">{esc(pill)}</text>')
    o.append("</svg>")
    return "\n".join(o)


def elf_schematic_svg():
    """개념 도식 — 결합선 위 ELF 의 두 꼴 (자료 아님)."""
    pl, pr, yt, yb = 64, 600, 34, 164

    def X(t):
        return pl + t * (pr - pl)

    def Y(v):
        return yb - v * (yb - yt)

    def poly(f):
        pts = [(X(i / 160), Y(f(i / 160))) for i in range(161)]
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

    cov = lambda t: 0.12 + 0.80 * math.exp(-((t - 0.5) / 0.20) ** 2)
    ion = lambda t: 0.08 + 0.80 * math.exp(-((t - 0.78) / 0.25) ** 2)
    aria = ("Schematic, not data. ELF along a bond from cation to anion. A shared pair gives a high value at the "
            "midpoint; in an ionic bond the electrons sit on the anion and the midpoint value is low.")
    o = [f'<svg viewBox="0 0 640 214" role="img" aria-label="{esc(aria)}" xmlns="http://www.w3.org/2000/svg">',
         f"<title>{esc(aria)}</title>"]
    for v in (0, 0.5, 1.0):
        o.append(f'<line class="{"ax0" if v == 0 else "ax"}" x1="{pl}" y1="{Y(v):.1f}" x2="{pr}" y2="{Y(v):.1f}"/>'
                 f'<text class="tk" x="{pl - 10}" y="{Y(v) + 4:.1f}" text-anchor="end">{v:g}</text>')
    o.append(f'<text class="tk" x="{pl - 10}" y="{yt - 14}" text-anchor="end">ELF</text>')
    o.append(f'<line class="refline" x1="{X(0.5):.1f}" y1="{yt - 8}" x2="{X(0.5):.1f}" y2="{yb}"/>'
             f'<text class="tk" x="{X(0.5) + 6:.1f}" y="{yt - 10}">bond midpoint</text>')
    o.append(f'<path class="curve-ref" d="{poly(cov)}"/><path class="curve-nd" d="{poly(ion)}"/>')
    for f, cls in ((cov, "host"), (ion, "nd")):
        o.append(f'<circle class="mk {cls} ringed" cx="{X(0.5):.1f}" cy="{Y(f(0.5)):.1f}" r="5"/>')
    o.append(f'<text class="lb" x="{X(0.30):.1f}" y="{Y(0.95):.1f}" text-anchor="end">shared pair (P–S type)</text>')
    o.append(f'<text class="lb" x="{X(0.78):.1f}" y="{Y(0.88) - 12:.1f}" text-anchor="middle">ionic (Nd–S type)</text>')
    o.append(f'<circle class="atom-c" cx="{pl}" cy="{yb + 26}" r="9"/><text class="lb2" x="{pl + 16}" y="{yb + 30}">cation</text>'
             f'<circle class="atom-s" cx="{pr}" cy="{yb + 26}" r="9"/><text class="lb2" x="{pr - 16}" y="{yb + 30}" text-anchor="end">anion</text>')
    o.append("</svg>")
    return "\n".join(o)


# ── 표 보기 ─────────────────────────────────────────────────────────────────
def table_view(head, rows, num_cols=()):
    th = "".join(f'<th class="n">{esc(h)}</th>' if i in num_cols else f"<th>{esc(h)}</th>" for i, h in enumerate(head))
    trs = []
    for r in rows:
        trs.append("<tr>" + "".join(f'<td class="n">{esc(c)}</td>' if i in num_cols else f"<td>{esc(c)}</td>"
                                    for i, c in enumerate(r)) + "</tr>")
    return (f'<details class="tv"><summary>Table view</summary><div class="tablewrap"><table>'
            f"<thead><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table></div></details>")


# ── 페이지 ──────────────────────────────────────────────────────────────────
CSS = r"""
:root{
  /* Layout: one reading column (max 860px); figures sit in cards and scroll sideways on phones instead of shrinking */
  --bg:#fcfbfd; --card:#ffffff; --ink:#1f2937; --ink-2:#374151; --mut:#6b7280; --line:#e9e4ee; --grid:#ebe8ef; --axis:#9ca3af;
  --nd:#be185d; --nd-soft:#fdf2f8; --c-nd:#db2777; --c-ref:#94a3b8; --c-ref-strong:#64748b; --on-mark:#ffffff;
  --ok:#0f766e; --ok-soft:#e7f5f2; --warn:#92400e; --warn-soft:#fdf6e3; --open:#57534e; --open-soft:#f1f0f4;
  --font-sans:"IBM Plex Sans KR","IBM Plex Sans",system-ui,-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;
  --font-mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#141118; --card:#1f1b24; --ink:#ece8f0; --ink-2:#d4cdd9; --mut:#a39cad; --line:#352e3c; --grid:#2d2733; --axis:#6b6475;
    --nd:#f9a8d4; --nd-soft:#2e1a27; --c-nd:#f472b6; --c-ref:#6b7484; --c-ref-strong:#9aa3b1; --on-mark:#1f1b24;
    --ok:#5eead4; --ok-soft:#12302b; --warn:#fcd34d; --warn-soft:#30260f; --open:#c9c2d1; --open-soft:#2a2530;
    color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#141118; --card:#1f1b24; --ink:#ece8f0; --ink-2:#d4cdd9; --mut:#a39cad; --line:#352e3c; --grid:#2d2733; --axis:#6b6475;
  --nd:#f9a8d4; --nd-soft:#2e1a27; --c-nd:#f472b6; --c-ref:#6b7484; --c-ref-strong:#9aa3b1; --on-mark:#1f1b24;
  --ok:#5eead4; --ok-soft:#12302b; --warn:#fcd34d; --warn-soft:#30260f; --open:#c9c2d1; --open-soft:#2a2530;
  color-scheme:dark;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
body{margin:0;background:var(--bg);color:var(--ink);font:400 16px/1.75 var(--font-sans);-webkit-font-smoothing:antialiased}
.wrap{max-width:860px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:40px 80px}
.eyebrow{font:600 .74rem/1.4 var(--font-mono);letter-spacing:.06em;color:var(--nd);margin:0 0 10px}
h1{font:700 2.05rem/1.25 var(--font-sans);margin:0 0 10px;letter-spacing:-.01em;text-wrap:balance}
.sub{color:var(--ink-2);font-size:1.02rem;margin:0 0 18px}
h2{font:700 1.28rem/1.4 var(--font-sans);margin:52px 0 12px;text-wrap:balance}
h3{font:600 1rem/1.4 var(--font-sans);margin:0 0 6px}
p,li{max-width:68ch}
p{margin:0 0 12px}
b,strong{font-weight:600}
a{color:var(--nd)}
.toc{display:flex;flex-wrap:wrap;gap:4px 16px;font-size:.86rem;margin:0}
.toc a{color:var(--ink-2);text-decoration:none;border-bottom:1px solid var(--line)}
.toc a:hover,.toc a:focus-visible{color:var(--nd);border-color:var(--nd)}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:16px 0}
.answer{background:var(--nd-soft);border-color:transparent;margin-top:28px}
.answer h2{margin:0 0 10px}
.sum{margin:0;padding-left:1.3em;display:grid;gap:10px}
.qlabel{font:600 .74rem/1.4 var(--font-mono);letter-spacing:.05em;color:var(--mut);margin:0 0 6px}
.qhead{font-weight:600;margin:0 0 6px}
.quote ol{margin:0;padding-left:1.3em;display:grid;gap:4px}
.trio{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:12px 0}
.concept{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;min-width:0}
.concept p{font-size:.94rem;margin:0}
figure{margin:18px 0;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 16px 12px;min-width:0}
.chart{overflow-x:auto}
.chart svg{display:block;width:100%;min-width:520px;max-width:780px;height:auto;margin:0 auto}
.duo{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.duo svg{display:block;width:100%;max-width:380px;height:auto;margin:0 auto}
.legend{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:.84rem;color:var(--ink-2);margin:0 0 6px}
.legend span{display:inline-flex;align-items:center;gap:7px}
.sw{width:12px;height:12px;border-radius:3px;display:inline-block;flex:none}
.sw-nd{background:var(--c-nd)}
.sw-ref{background:var(--c-ref)}
.sw-host{background:var(--c-ref-strong)}
.sw-ring{background:var(--card);border:2px solid var(--c-ref-strong);border-radius:50%}
.sw-dia{background:var(--c-nd);transform:rotate(45deg);border-radius:2px;width:10px;height:10px}
figcaption{font-size:.84rem;line-height:1.6;color:var(--mut);margin-top:10px}
figcaption b{color:var(--ink)}
details.tv{margin-top:8px}
details.tv summary{cursor:pointer;font-size:.82rem;color:var(--nd);width:max-content}
.tablewrap{overflow-x:auto}
table{border-collapse:collapse;font-size:.86rem;margin:8px 0;width:100%}
th,td{border-bottom:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}
th{font-weight:600;color:var(--ink-2);background:var(--bg)}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;font-family:var(--font-mono);white-space:nowrap}
.claims td:first-child{font-weight:600;min-width:8.5em}
.claims td:last-child{white-space:nowrap}
.cmp td:first-child{white-space:nowrap;font-weight:600}
.chip{display:inline-block;font:600 .72rem/1.6 var(--font-mono);padding:1px 8px;border-radius:999px;white-space:nowrap}
.chip-ok{background:var(--ok-soft);color:var(--ok)}
.chip-part{background:var(--warn-soft);color:var(--warn)}
.chip-open{background:var(--open-soft);color:var(--open)}
.note{font-size:.92rem;color:var(--ink-2)}
.nb{margin:8px 0 14px;padding-left:1.3em;font-size:.95rem;display:grid;gap:4px}
.ex{display:grid;gap:12px;margin:10px 0 0;padding-left:1.3em}
.ex .en{display:block;font-size:.9rem;color:var(--ink-2);margin-top:3px}
.dont{display:grid;gap:8px;padding-left:1.3em;margin:10px 0 0}
dl.meth{display:grid;grid-template-columns:max-content 1fr;gap:8px 18px;font-size:.88rem;margin:12px 0 0}
dl.meth dt{font-weight:600;color:var(--ink-2)}
dl.meth dd{margin:0;min-width:0;overflow-wrap:anywhere}
details.methods summary{cursor:pointer;font-weight:600}
code{font-family:var(--font-mono);font-size:.84em;overflow-wrap:anywhere}
footer{margin-top:48px;font-size:.8rem;color:var(--mut)}
svg text{font-family:var(--font-sans);fill:var(--ink)}
svg .tk{font:12px var(--font-mono);fill:var(--mut)}
svg .lb{font-size:13.5px;fill:var(--ink)}
svg .lb2{font:11.5px var(--font-mono);fill:var(--mut)}
svg .hd{font-size:13px;font-weight:600;fill:var(--ink-2)}
svg .sym{font-size:15px;font-weight:700;fill:var(--ink)}
svg .val{font:12.5px var(--font-mono);fill:var(--ink)}
svg .atxt{font-size:11.5px;font-weight:600;fill:var(--ink-2)}
svg .on{font-size:13px;font-weight:700;fill:var(--on-mark)}
svg .pilltxt{fill:var(--ink-2)}
svg .ax{stroke:var(--grid);stroke-width:1}
svg .ax0{stroke:var(--axis);stroke-width:1}
svg .refline{stroke:var(--mut);stroke-width:1}
svg .nd{fill:var(--c-nd)}
svg .ref{fill:var(--c-ref)}
svg .host{fill:var(--c-ref-strong)}
svg .ringed{stroke:var(--card);stroke-width:2}
svg .ring{fill:var(--card);stroke:var(--c-ref-strong);stroke-width:2}
svg .dia{fill:var(--c-nd);stroke:var(--card);stroke-width:2}
svg .err{stroke:var(--ink-2);stroke-width:1.5}
svg .meanbar{stroke:var(--c-nd);stroke-width:2.5}
svg .hitbox{fill:transparent}
svg .hit{outline:none}
svg .hit:hover .mk,svg .hit:focus-visible .mk{filter:brightness(1.1)}
svg .hit:focus-visible .hitbox{fill:var(--nd-soft)}
svg .bond{stroke:var(--c-ref);stroke-width:2.5}
svg .atom-s{fill:var(--card);stroke:var(--c-ref-strong);stroke-width:1.8}
svg .atom-c{fill:var(--c-ref-strong)}
svg .atom-nd{fill:var(--c-nd)}
svg .arrow{stroke:var(--mut);stroke-width:1.5;fill:none}
svg .arrowhead{fill:var(--mut)}
svg .pill-open{fill:var(--open-soft)}
svg .pill-ok{fill:var(--nd-soft)}
svg .curve-ref{stroke:var(--c-ref-strong);stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}
svg .curve-nd{stroke:var(--c-nd);stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}
#tip{position:fixed;z-index:30;pointer-events:none;background:var(--ink);color:var(--bg);padding:6px 10px;border-radius:6px;font:12px/1.45 var(--font-mono);max-width:300px;box-shadow:0 4px 14px rgba(0,0,0,.2)}
#tip strong{display:block;font-weight:600}
.claim-mark{display:inline-block;font:600 .74rem/1.5 var(--font-mono);letter-spacing:.03em;color:var(--warn);background:var(--warn-soft);padding:1px 8px;border-radius:999px}
.bound{border-color:var(--warn)}
.caution{background:var(--warn-soft);border-color:transparent}
.caution .qhead{color:var(--warn)}
table.qs td:first-child{font-weight:600}
@media (max-width:560px){h1{font-size:1.72rem}.card{padding:16px}figure{padding:12px}dl.meth{grid-template-columns:1fr;gap:2px 0}dl.meth dd{margin-bottom:8px}}
"""

JS = r"""
(() => {
  const tip = document.getElementById('tip');
  if (!tip) return;
  const place = (x, y) => {
    const r = tip.getBoundingClientRect();
    let left = x + 14, top = y - r.height - 12;
    if (left + r.width > window.innerWidth - 8) left = x - r.width - 14;
    if (left < 8) left = 8;
    if (top < 8) top = y + 18;
    tip.style.left = left + 'px';
    tip.style.top = top + 'px';
  };
  const show = (el, x, y) => {
    const v = document.createElement('strong');
    v.textContent = el.getAttribute('data-v') || '';
    const l = document.createElement('span');
    l.textContent = el.getAttribute('data-l') || '';
    tip.replaceChildren(v, l);
    tip.hidden = false;
    place(x, y);
  };
  const hide = () => { tip.hidden = true; };
  document.querySelectorAll('[data-v]').forEach((el) => {
    el.addEventListener('pointermove', (e) => show(el, e.clientX, e.clientY));
    el.addEventListener('pointerdown', (e) => show(el, e.clientX, e.clientY));
    el.addEventListener('pointerleave', hide);
    el.addEventListener('focus', () => { const b = el.getBoundingClientRect(); show(el, b.left + b.width / 2, b.top); });
    el.addEventListener('blur', hide);
  });
  window.addEventListener('scroll', hide, { passive: true });
})();
"""


def figure(svg, caption, legend="", table="", cls="chart"):
    leg = f'<div class="legend">{legend}</div>' if legend else ""
    return (f'<figure>{leg}<div class="{cls}">{svg}</div>'
            f"<figcaption>{caption}</figcaption>{table}</figure>")


def sci(x):
    """1.34e9 → '1.3 × 10⁹' (위첨자 지수)."""
    e = int(math.floor(math.log10(abs(x))))
    sup = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return f"{x / 10 ** e:.1f} × 10{str(e).translate(sup)}"


CLAIM_OPEN, CLAIM_CLOSE = f"<!--claim:{HZ_LI3ND}-->", "<!--/claim-->"


def page_body(D):
    Q1, Q2, SV, LN = D["q1"], D["q2"], D["svac"], D["li3nd"]
    sh = {c["name"]: c for c in D["shift"]}
    fs, cl, un, ox = sh["Free S²⁻"], sh["Cl⁻"], sh["PS₄ unit (P + 4 S)"], sh["O bonded to P"]
    ca, de, el = D["cation"], D["density"], {r["bond"]: r for r in D["elf"]}
    li_share, nd_share = 100 * ca["li_mean"], 100 * ca["nd_mean"] / 3
    sh_lo = min(fs["shift"], cl["shift"], un["shift"])
    sh_hi = max(fs["shift"], cl["shift"], un["shift"])
    v_lo, v_hi = -max(de["S"]["V"]["pct"], de["Cl"]["V"]["pct"]), -min(de["S"]["V"]["pct"], de["Cl"]["V"]["pct"])
    nv_lo, nv_hi = min(de["S"]["NV"]["pct"], de["Cl"]["NV"]["pct"]), max(de["S"]["NV"]["pct"], de["Cl"]["NV"]["pct"])
    o_lo, o_hi = min(v for v, _ in ox["near"] + ox["ref"]), max(v for v, _ in ox["near"] + ox["ref"])
    nd_mid = [el["Nd-S"]["mid"], el["Cl-Nd"]["mid"], el["Nd-O"]["mid"]]
    ps_mid, po_mid = el["P-S"]["mid"], el["O-P"]["mid"]
    d_lis, d_nds, d_ps, d_po = dchi("Li", "S"), dchi("Nd", "S"), dchi("P", "S"), dchi("P", "O")
    d_licl, d_ndcl = dchi("Li", "Cl"), dchi("Nd", "Cl")
    pct_lis = ionic_pct(d_lis)

    # Nd 이웃 문장
    kname = {"O_P_nearNd": "O", "S_free_nearNd": "자유 S²⁻", "Cl_nearNd": "Cl⁻", "S_PS4_nearNd": "PS₄ 의 S"}
    nb_lines = []
    for i, nd in enumerate(D["nd_nb"]):
        groups = {}
        for d, _e, c, _m in nd["neighbours"]:
            groups.setdefault(kname.get(c, c), []).append(d)
        parts = []
        for k in ("O", "자유 S²⁻", "Cl⁻", "PS₄ 의 S"):
            if k in groups:
                ds = groups[k]
                dtxt = " · ".join(f"{d:.2f}" for d in ds) if len(ds) <= 2 else f"{min(ds):.2f}–{max(ds):.2f}"
                parts.append(f"{k} {len(ds)} 개 ({dtxt} Å)")
        nb_lines.append(f"<li>Nd {'①②'[i]} 은 {', '.join(parts)} 와 닿아 있어요.</li>")

    # ── 그림들 ──
    fig_scale = figure(
        scale_svg("Pauling electronegativity of Li, Nd, P, S, Cl and O on one line. Nd at 1.14 sits next to Li at 0.98 "
                  "and far below P at 2.19."),
        "<b>Fig. 1. Pauling electronegativity of the six elements in the cell.</b> Nd (1.14) sits next to Li (0.98) and "
        "far below P (2.19). The values for Nd, P, S, and O are the ones in the first author's message; Li and Cl come "
        "from the same standard table.",
        legend='<span><i class="sw sw-nd"></i>Nd</span><span><i class="sw sw-host"></i>Cations that Nd can replace (Li, P)</span>'
               '<span><i class="sw sw-ring"></i>Anions</span>',
        table=table_view(("Element", "χ (Pauling)", "Role here", "Source"),
                         [(e, f"{v:.2f}", {"Nd": "dopant", "Li": "cation (Nd site in this model)", "P": "cation (Nd site in the Rietveld model)"}.get(e, "anion"),
                           "first author's message" if e in FIRST_AUTHOR_EN else "same standard table")
                          for e, v in sorted(PAULING.items(), key=lambda kv: kv[1])], num_cols=(1,)))

    brows = []
    for an, _cats in DCHI_GROUPS:
        brows.append({"header": f"Bonds to {SUP[an]}"})
        for b in (x for x in D["bonds"] if x["anion"] == an):
            brows.append({"label": b["bond"], "value": b["dchi"], "cls": "nd" if b["cation"] == "Nd" else "ref",
                          "vtext": f"{b['dchi']:.2f}", "tip_v": f"Δχ = {b['dchi']:.2f}",
                          "tip_l": f"{b['bond']} ({b['cation']} {PAULING[b['cation']]:.2f}, {b['anion']} {PAULING[b['anion']]:.2f})"})
    fig_dchi = figure(
        hbars(brows, x0=0, x1=2.6, ticks=(0, 0.5, 1.0, 1.5, 2.0, 2.5), tick_text=lambda t: f"{t:.1f}",
              aria="Electronegativity difference for each bond type in the cell, grouped by anion. Bonds to Nd highlighted.",
              axis_label="Δχ (Pauling), larger = electrons sit more on the anion", label_w=150),
        f"<b>Fig. 2. Electronegativity difference Δχ for each bond type in the cell, grouped by anion.</b> A larger Δχ "
        f"means the bonding electrons sit more on the anion. Bonds to Nd are highlighted. For S, Nd–S ({d_nds:.2f}) lies far "
        f"above P–S ({d_ps:.2f}) and just below Li–S ({d_lis:.2f}).",
        legend='<span><i class="sw sw-nd"></i>Bonds to Nd</span><span><i class="sw sw-ref"></i>Other bonds in the cell</span>',
        table=table_view(("Bond", "Δχ", "Pauling ionic character (%)", "Note"),
                         [(b["bond"], f"{b['dchi']:.2f}", f"{b['pct']:.1f}", "1 − exp(−Δχ²/4); used for ordering only")
                          for b in D["bonds"]], num_cols=(1, 2)))

    fig_replace = figure(
        replace_svg("P") + replace_svg("Li"),
        "<b>Fig. 3. What Nd replaces sets the direction (schematic, not data).</b> (a) Nd on the P site, as in the Rietveld "
        f"model. The S partner changes from P to Nd and Δχ rises from {d_ps:.2f} to {d_nds:.2f}, so electronegativity "
        "predicts more electrons on S. Not computed yet. (b) Nd on a Li site, as in the DFT model on this page. The partner "
        f"changes from Li to Nd and Δχ falls slightly from {d_lis:.2f} to {d_nds:.2f}, so electronegativity predicts slightly "
        "fewer electrons on S. Computed in Fig. 4.",
        cls="duo")

    fig_elfschem = figure(
        elf_schematic_svg(),
        "<b>Schematic, not data.</b> ELF along a bond from a cation (left) to an anion (right). A shared electron pair "
        "gives a high value at the bond midpoint (P–S type). In an ionic bond the electrons sit on the anion and the "
        "midpoint value is low (Nd–S type).",
        legend='<span><i class="sw sw-host"></i>Shared pair</span><span><i class="sw sw-nd"></i>Ionic</span>')

    fig_shift = figure(
        dotplot(D["shift"], x0=-0.06, x1=0.30, ticks=(0, 0.1, 0.2, 0.3),
                aria="Shift in Bader charge of anions next to Nd, measured from the mean of the same anion with Li "
                     "neighbours only. All four classes shift to less negative values."),
        "<b>Fig. 4. Bader charge of anions next to Nd, measured from the mean of the same anion with Li neighbours "
        "only.</b> Positive means less negative, that is, fewer electrons on the anion. Each marker is one anion or one "
        f"PS₄ unit; n gives the count next to Nd vs with Li neighbours only. Free S²⁻ {fnum(fs['shift'], 2, True)} e, PS₄ unit {fnum(un['shift'], 2, True)} e, "
        f"Cl⁻ {fnum(cl['shift'], 2, True)} e, and O bonded to P {fnum(ox['shift'], 2, True)} e (only one O without an Nd "
        "neighbour, so that reference is a single atom).",
        legend='<span><i class="sw sw-dia"></i>Anion next to Nd</span><span><i class="sw sw-ring"></i>Same anion, Li neighbours only</span>',
        table=table_view(("Anion class", "Group", "Site", "Bader net charge (e)", "Shift from Li-only mean (e)"),
                         [(c["name"], g, lab, fnum(v, 3), fnum(v - c["ref_mean"], 3, True))
                          for c in D["shift"] for g, vals in (("Li only", c["ref"]), ("next to Nd", c["near"]))
                          for v, lab in sorted(vals)], num_cols=(3, 4)))

    crow = [{"label": "Li, this cell", "sub": f"mean of {ca['li_n']} sites", "value": li_share, "cls": "ref",
             "vtext": f"{li_share:.0f} %", "tip_v": f"{fnum(ca['li_mean'], 3)} e of +1 ({li_share:.1f} %)", "tip_l": "Li, this cell"},
            {"label": "Li, undoped LPSCl1.6", "sub": "same method", "value": 100 * ca["host_li"], "cls": "ref",
             "vtext": f"{100 * ca['host_li']:.0f} %", "tip_v": f"{fnum(ca['host_li'], 3)} e of +1", "tip_l": "Li, undoped LPSCl1.6"}]
    for k, (idx, v) in enumerate(ca["nd"]):
        crow.append({"label": f"Nd {'①②'[k]}", "sub": f"site {idx}", "value": 100 * v / 3, "cls": "nd",
                     "vtext": f"{100 * v / 3:.0f} %", "tip_v": f"{fnum(v, 3)} e of +3 ({100 * v / 3:.1f} %)", "tip_l": f"Nd, site {idx}"})
    fig_cation = figure(
        hbars(crow, x0=0, x1=100, ticks=(0, 25, 50, 75, 100), tick_text=lambda t: f"{t:.0f} %",
              aria="Share of the formal charge each cation gives away. Li about 88 percent, Nd about 65 percent.",
              axis_label="Bader charge as a share of the formal charge (Li +1, Nd +3)"),
        f"<b>Fig. 5. Share of the formal charge each cation gives away, from Bader charges.</b> Li keeps the same share "
        f"as in undoped LPSCl1.6 computed the same way ({fnum(ca['host_li'], 2, True)} e). Nd gives "
        f"{fnum(ca['nd_mean'], 2, True)} e of its formal +3.",
        legend='<span><i class="sw sw-nd"></i>Nd</span><span><i class="sw sw-ref"></i>Li</span>',
        table=table_view(("Cation", "Bader net charge (e)", "Formal charge", "Share (%)"),
                         [("Li, this cell (mean)", fnum(ca["li_mean"], 3), "+1", f"{li_share:.1f}"),
                          ("Li, undoped LPSCl1.6", fnum(ca["host_li"], 3), "+1", f"{100 * ca['host_li']:.1f}")]
                         + [(f"Nd, site {i}", fnum(v, 3), "+3", f"{100 * v / 3:.1f}") for i, v in ca["nd"]],
                         num_cols=(1, 3)))

    drows = []
    for an, nm in (("S", "Free S²⁻"), ("Cl", "Cl⁻")):
        dd = de[an]
        drows.append({"header": f"{nm}  (n {dd['n_near']} next to Nd · {dd['n_ref']} Li only)"})
        for key, lab in (("N", "Electrons in basin"), ("V", "Basin volume"), ("NV", "Electron density")):
            q = dd[key]
            unit = {"N": "e", "V": "Å³", "NV": "e/Å³"}[key]
            nd_ = 3 if key != "V" else 1
            drows.append({"label": lab, "value": q["pct"], "cls": "nd" if key == "NV" else "ref",
                          "vtext": f"{fnum(q['pct'], 0, True)} %",
                          "tip_v": f"{fnum(q['pct'], 1, True)} % ({q['ref']:.{nd_}f} → {q['near']:.{nd_}f} {unit})",
                          "tip_l": f"{nm}, {lab.lower()}"})
    fig_density = figure(
        hbars(drows, x0=-30, x1=30, ticks=(-20, -10, 0, 10, 20), tick_text=lambda t: mn(f"{t:+.0f} %") if t else "0",
              aria="Change next to Nd for free sulfide and chloride. Electron count barely moves, basin volume shrinks, "
                   "electron density rises.",
              axis_label="Change next to Nd, relative to the same anion with Li neighbours only"),
        f"<b>Fig. 6. Change next to Nd, relative to the same anion with Li neighbours only.</b> The electron count in "
        f"the Bader basin barely moves ({fnum(de['S']['N']['pct'], 0)} % for free S²⁻, {fnum(de['Cl']['N']['pct'], 0)} % "
        f"for Cl⁻) while the basin shrinks ({fnum(de['S']['V']['pct'], 0)} %, {fnum(de['Cl']['V']['pct'], 0)} %), so the "
        f"electron density rises ({fnum(de['S']['NV']['pct'], 0, True)} %, {fnum(de['Cl']['NV']['pct'], 0, True)} %).",
        legend='<span><i class="sw sw-nd"></i>Electron density (claim 2)</span><span><i class="sw sw-ref"></i>Its two parts</span>',
        table=table_view(("Anion", "Quantity", "Li only (mean)", "Next to Nd (mean)", "Change (%)"),
                         [(nm, lab, f"{de[an][k]['ref']:.4f}", f"{de[an][k]['near']:.4f}", fnum(de[an][k]["pct"], 1, True))
                          for an, nm in (("S", "Free S²⁻"), ("Cl", "Cl⁻"), ("O", "O bonded to P (reference n 1)"))
                          for k, lab in (("N", "electrons (e)"), ("V", "volume (Å³)"), ("NV", "density (e/Å³)"))],
                         num_cols=(2, 3, 4)))

    lab = {"P-S": "P–S", "O-P": "P–O", "Nd-S": "Nd–S", "Cl-Nd": "Nd–Cl", "Nd-O": "Nd–O"}
    erows = [{"header": "Bonds to P (shared electron pair)"}]
    for b in ("P-S", "O-P"):
        r = el[b]
        erows.append({"label": lab[b], "sub": f"n {r['n']} · {r['d']:.2f} Å", "value": r["mid"], "err": r["sd"], "cls": "ref",
                      "vtext": f"{r['mid']:.2f}", "tip_v": f"ELF {r['mid']:.3f} ± {r['sd']:.3f}", "tip_l": f"{lab[b]}, this cell"})
    hp = D["host_ps"]
    erows.append({"label": "P–S, undoped", "sub": f"n {hp['n']} · LPSCl1.6", "value": hp["mid"], "err": hp["sd"], "cls": "host",
                  "vtext": f"{hp['mid']:.2f}", "tip_v": f"ELF {hp['mid']:.3f} ± {hp['sd']:.3f}",
                  "tip_l": "P–S in undoped LPSCl1.6, same settings"})
    erows.append({"header": "Bonds to Nd"})
    for b in ("Nd-S", "Cl-Nd", "Nd-O"):
        r = el[b]
        erows.append({"label": lab[b], "sub": f"n {r['n']} · {r['d']:.2f} Å", "value": r["mid"], "err": r["sd"], "cls": "nd",
                      "vtext": f"{r['mid']:.2f}", "tip_v": f"ELF {r['mid']:.3f} ± {r['sd']:.3f}", "tip_l": f"{lab[b]}, this cell"})
    fig_elf = figure(
        hbars(erows, x0=0, x1=1.0, ticks=(0, 0.25, 0.5, 0.75, 1.0), tick_text=lambda t: f"{t:g}",
              aria="ELF at the bond midpoint. P–S and P–O near 0.93; bonds to Nd between 0.31 and 0.47.",
              axis_label="ELF at the bond midpoint (mean ± s.d. over bonds)", ref_lines=((0.5, "0.5 = uniform electron gas"),),
              top=44),
        f"<b>Fig. 7. ELF at the bond midpoint.</b> P–S and P–O keep a shared pair ({po_mid:.2f}–{ps_mid:.2f}); bonds to Nd "
        f"do not ({min(nd_mid):.2f}–{max(nd_mid):.2f}). The darker gray bar is P–S in undoped LPSCl1.6 computed with the "
        f"same settings ({hp['mid']:.3f}). The line at 0.5 marks the uniform electron gas value, a reference rather than "
        "a bond threshold. Li–S and Li–Cl are left out on purpose (see text).",
        legend='<span><i class="sw sw-nd"></i>Bonds to Nd</span><span><i class="sw sw-ref"></i>Bonds to P</span>'
               '<span><i class="sw sw-host"></i>Undoped LPSCl1.6</span>',
        table=table_view(("Bond", "Cell", "Bonds (n)", "Mean length (Å)", "ELF midpoint", "s.d."),
                         [(lab[r["bond"]], "Nd-doped (this page)", r["n"], f"{r['d']:.3f}", f"{r['mid']:.3f}", f"{r['sd']:.3f}") for r in D["elf"]]
                         + [("P–S", "undoped LPSCl1.6", hp["n"], f"{hp['d']:.2f}", f"{hp['mid']:.3f}", f"{hp['sd']:.3f}")],
                         num_cols=(2, 3, 4, 5)))

    # 그림 8 — Q1 자리 에너지 (Li 자리 모델 기준)
    fig_site = figure(
        hbars([{"label": "Nd on a Li site", "value": 0.0, "cls": "ref", "vtext": "0 (reference)",
                "tip_v": "0 eV per Nd (reference)", "tip_l": "Nd on a Li site"},
               {"label": "Nd on the P site (4b)", "value": Q1["dG"], "cls": "nd", "vtext": fnum(Q1["dG"], 2, True),
                "tip_v": f"{fnum(Q1['dG'], 3, True)} eV per Nd", "tip_l": "Nd on the P site (Rietveld 4b)"}],
              x0=0, x1=0.6, ticks=(0, 0.2, 0.4, 0.6), tick_text=lambda t: f"{t:.1f}",
              aria=f"Site energy per Nd. The P-site model is {Q1['dG']:.2f} eV per Nd above the Li-site model.",
              axis_label="Energy relative to the Li-site model (eV per Nd)"),
        f"<b>Fig. 8. Site energy (Q1{', provisional' if Q1['provisional'] else ''}).</b> Energy of the model with Nd on the "
        f"P site (Rietveld 4b) relative to the model with Nd on a Li site, per Nd, after balancing the composition "
        f"difference with Li₂S and Li₃PS₄ ({Q1['a_li2s']} Li₂S − {-Q1['b_li3ps4']} Li₃PS₄ per {Q1['n_nd']} Nd). Lowest "
        "candidate of each model, volume fitted at fixed cell shape, then ions relaxed; frozen-4f PBE; Nd/(Nd+P) = 0.40.",
        legend='<span><i class="sw sw-nd"></i>Nd on the P site</span><span><i class="sw sw-ref"></i>Reference: Nd on a Li site</span>',
        table=table_view(("Model", "Nd site", "Lowest cell", "Energy relative to the Li-site model (eV per Nd)"),
                         [("M_Li", "Li", Q1["top"]["MLi"], "0 (reference)"),
                          ("M_P", "P (4b)", Q1["top"]["MP"], fnum(Q1["dG"], 3, True))], num_cols=(3,)))

    # 그림 9 — Q2 분해 구동력 차 (분해능과 함께)
    fig_decomp = figure(
        hbars([{"label": "Doped − undoped", "sub": "Y, B = 25 GPa", "value": Q2["Y"], "cls": "nd",
                "vtext": f"{fnum(Q2['Y'], 1, True)} meV/atom", "tip_v": f"Y = {fnum(Q2['Y'], 2, True)} meV/atom",
                "tip_l": "Nd₂O₃@LPSCl1.6 minus LPSCl1.6"}],
              x0=-40, x1=5, ticks=(-40, -30, -20, -10, 0), tick_text=lambda t: mn(f"{t:.0f}"),
              aria=f"Decomposition driving force difference Y = {Q2['Y']:.1f} meV per atom, far outside the "
                   f"plus or minus {Q2['res']:.0f} meV resolution.",
              axis_label="Y = ΔE_decomp(doped) − ΔE_decomp(undoped)  (meV/atom)",
              ref_lines=((-Q2["res"], f"±{Q2['res']:.0f} meV/atom resolution", "end"), (Q2["res"], ""))),
        "<b>Fig. 9. Decomposition driving force (Q2).</b> Difference between the Nd₂O₃-doped cell and undoped LPSCl1.6 in the "
        "energy released per atom on splitting into the same five products (closed system, 0 K, frozen-4f PBE). A negative "
        f"Y means the doped cell leans further toward the products. The thin lines mark ±{Q2['res']:.0f} meV/atom, the "
        "resolution set before the calculation. Correcting for the computed cell pressures changes Y by "
        f"{abs(Q2['Y'] - Q2['Y_raw']):.3f} meV/atom.",
        legend='<span><i class="sw sw-nd"></i>Doped minus undoped</span>',
        table=table_view(("Quantity", "Value (meV/atom)"),
                         [("Y, pressure-corrected (B = 25 GPa)", fnum(Q2["Y"], 2, True)), ("Y, uncorrected", fnum(Q2["Y_raw"], 2, True)),
                          ("Resolution set before the calculation", f"±{Q2['res']:.0f}")], num_cols=(1,)))

    # ── 비교표 ──
    def chip(kind, text):
        sym = {"ok": "✓", "part": "△", "open": "○"}[kind]
        return f'<span class="chip chip-{kind}">{sym} {text}</span>'

    cmp_rows = [
        ("Li–S → Nd–S", "이번 모델", f"Δχ {d_lis:.2f} → {d_nds:.2f}, S 쪽 전자가 조금 준다",
         f"자유 S²⁻ {fnum(fs['ref_mean'])} → {fnum(fs['near_mean'])} e (덜 음)", chip("ok", "같은 방향")),
        ("Li–Cl → Nd–Cl", "이번 모델", f"Δχ {d_licl:.2f} → {d_ndcl:.2f}, Cl 쪽 전자가 조금 준다",
         f"Cl⁻ {fnum(cl['ref_mean'])} → {fnum(cl['near_mean'])} e (덜 음)", chip("ok", "같은 방향")),
        ("Li → Nd (양이온 쪽)", "이번 모델", f"χ {PAULING['Li']:.2f} → {PAULING['Nd']:.2f}, Nd 가 전자를 덜 내준다",
         f"형식 전하 가운데 내준 몫 Li {li_share:.0f} %, Nd {nd_share:.0f} %", chip("ok", "같은 방향") + " 형식 전하 +3 영향도 섞임"),
        ("P–S → Nd–S", "Rietveld 모델", f"Δχ {d_ps:.2f} → {d_nds:.2f}, S 쪽 전자가 는다", "아직 계산하지 않았어요", chip("open", "계산 전")),
        ("P–S → P–O", "두 모델 공통", f"Δχ {d_ps:.2f} → {d_po:.2f}, O 쪽 전자가 더 많다",
         f"P 에 붙은 O 는 {fnum(o_lo)} ~ {fnum(o_hi)} e 로 자유 S²⁻ 보다 더 음이에요. PS₄ 안 S 와의 직접 비교는 못 해요.",
         chip("part", "방향만")),
        ("결합 성격", "이번 모델", "Nd–S 는 P–S 보다 훨씬 이온성이고 Li–S 보다 조금 덜",
         f"중점 ELF P–S {ps_mid:.2f}, Nd–S {el['Nd-S']['mid']:.2f}. Bader 와 합치면 주로 이온 결합이고 Li–음이온보다 공유성이 조금 더 있어요.",
         chip("ok", "같은 방향")),
    ]
    cmp_html = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>" for a, b, c, d, e in cmp_rows)

    # ── 2026-10-26: Q1 · Q2 · S 빈자리 · Li₃Nd ──
    prov = Q1["provisional"]
    prov_chip = chip("part", "잠정") if prov else ""
    n_near, n_far = re.findall(r"\d+", SV["n"])[:2]
    bg_html = f"""<section id="bg">
<h2>배경 — 무엇을 물었나</h2>
<p>실험에서는 LPSCl1.6 에 Nd₂O₃ 를 조금 넣었어요. Nd 는 P 자리에, O 는 S 자리에 들어간다고 보고, Rietveld 정련도 Nd 를 P 자리 (4b) 에 두었어요. 목표 조성은 x = 0.02 예요. 계산으로는 세 가지를 물었어요.</p>
<div class="tablewrap"><table class="qs">
<thead><tr><th>질문</th><th>계산 셀</th><th>짧은 답</th></tr></thead>
<tbody>
<tr><td>Q1. Nd 는 어느 자리에서 에너지가 낮을까</td><td>Rietveld 셀 (5 화학식 단위 · Nd/(Nd+P) 0.40)</td><td>Li 자리{' (잠정)' if prov else ''}</td></tr>
<tr><td>Q2. Nd 를 넣으면 분해 쪽으로 더 기울까</td><td>9 월 셀 (10 화학식 단위 · Nd 는 Li 자리)</td><td>더 기울어요</td></tr>
<tr><td>Q3. Nd 옆 전자는 어디에 있나</td><td>Q2 와 같은 셀</td><td>음이온 쪽 전자가 조금 적고, 주로 이온 결합이에요</td></tr>
</tbody></table></div>
<p class="note">Q1 과 Q2 · Q3 는 계산 셀과 설정이 달라서 숫자를 서로 견주지 않아요. 전자 배치 (Q3) 로 자리나 분해 (Q1 · Q2) 를 설명하지도 않아요. 세 질문 모두 실험 조성보다 Nd 가 10–20 배 많은 셀에서 계산했어요.</p>
</section>"""
    site_html = f"""<section id="site">
<h2>Q1. Nd 는 어느 자리에서 에너지가 더 낮을까 {prov_chip}</h2>
<p>같은 양의 Nd · O 를 넣되, Nd 를 P 자리 (Rietveld 4b) 에 둔 모델과 Li 자리에 둔 모델을 만들어 어느 쪽 에너지가 낮은지 견줬어요.</p>
<ul class="nb">
<li><b>조성을 맞춘 방법.</b> 두 모델은 Li 수가 달라요. Nd 가 P 자리에 들어가면 전하를 맞추려고 Nd 하나당 Li 2 개를 더 넣고, Li 자리에 들어가면 Nd 하나당 Li 3 개 몫을 빼요 (Nd 하나 + 빈자리 둘). 이 차이를 Li₂S · Li₃PS₄ 로 메워서 (Nd {Q1['n_nd']} 개당 Li₂S {Q1['a_li2s']} 개 − Li₃PS₄ {-Q1['b_li3ps4']} 개) 같은 원자들끼리 견줬어요.</li>
<li><b>배치 고르기.</b> 모델마다 후보 배치 10 개를 만들어 기계학습 퍼텐셜로 고르고, 가장 낮은 셀을 DFT 로 다시 계산했어요.</li>
<li><b>DFT.</b> 셀 모양은 그대로 두고 부피를 바꿔 가며 에너지를 재서 가장 낮은 부피를 찾은 뒤, 그 부피에서 원자 위치를 이완했어요.</li>
</ul>
{fig_site}
<p>Nd 가 P 자리에 있는 모델이 Nd 하나당 {Q1['dG']:.2f} eV 높아요. 이 계산 조건에서는 Li 자리가 더 안정해요. Li 자리 모델 쪽은 O 배치를 덜 훑었는데, 더 훑으면 Li 자리 쪽 에너지가 내려갈 수만 있어요. 그래서 이 차이는 '적어도 이만큼' 으로 읽어요.</p>
<div class="card caution">
<p class="qhead">Rietveld 결과 (4b) 와 반대 방향이에요</p>
<p style="margin:0">조건이 실험과 달라서 이 결과를 Rietveld 정련을 반박하는 근거로 쓰지 않아요. 계산 셀은 Nd 농도가 목표의 약 20 배 (Nd/(Nd+P) 0.40 대 0.02) 이고, Nd 의 4f 전자를 핵심부에 고정한 단순화 계산이에요. 모델마다 후보 10 개 안에서 가장 낮은 것끼리 견줬고, 조성은 Li₂S · Li₃PS₄ 한 가지로만 맞췄어요.</p>
</div>
{'<p class="note">잠정이에요. 이 결과를 원고 문장으로 옮기기 전에 1저자 동의를 받기로 했어요.</p>' if prov else ''}
</section>"""
    decomp_html = f"""<section id="decomp">
<h2>Q2. Nd 를 넣으면 분해 쪽으로 더 기울까</h2>
<p>Nd₂O₃ 를 넣은 셀과 넣기 전 LPSCl1.6 셀이 각각 분해 생성물로 쪼개진다고 할 때 에너지가 원자당 얼마나 내려가는지 구해서, 두 셀을 견줬어요. 더 많이 내려갈수록 분해 쪽으로 더 기운 거예요.</p>
<ul class="nb">
<li><b>생성물은 정해진 대로.</b> Materials Project 상도가 두 조성에 대해 고른 생성물 다섯 ({' · '.join(subf(x) for x in Q2['products'])}) 을 썼어요. 결과를 보고 고른 게 아니에요.</li>
<li><b>모두 같은 조건으로.</b> 두 셀과 생성물 다섯을 같은 DFT 설정으로 직접 계산했어요.</li>
<li><b>미리 정한 점검.</b> 계산 전에 정한 점검 여섯 (골격 · 생성물 집합 · 힘 · 생성물 이완 · 부피 · k 점) 을 모두 통과했어요.</li>
</ul>
{fig_decomp}
<p>도핑 셀이 원자당 {abs(Q2['Y']):.0f} meV 더 내려가요. 같은 조건에서 견주면 도핑 셀 쪽이 분해 생성물 쪽으로 더 기울어 있어요. 이 계산의 분해능 (원자당 {Q2['res']:.0f} meV) 의 약 {abs(Q2['Y']) / Q2['res']:.0f} 배예요.</p>
<div class="card caution">
<p class="qhead">'불안정하다' 는 뜻은 아니에요</p>
<p style="margin:0">0 K 에너지 비교라 온도 · 무질서 효과와 분해 속도가 들어 있지 않고, 생성물 다섯 밖의 다른 분해 경로도 보지 못해요. 그래서 '분해된다' · '불안정하다' 가 아니라 '같은 조건에서 견주면 도핑 셀이 더 기운다' 까지만 말해요. Li 가 드나드는 전기화학 조건 (전압 · 계면 반응) 의 얘기도 아니에요.</p>
</div>
<p class="note">이 셀은 Nd 를 Li 자리에 둔 9 월 모델로, 아래 전자 배치 (Q3) 와 같은 셀이에요. Nd · O 배치는 하나만 봤어요.</p>
</section>"""
    svac_html = f"""<section id="svac">
<h2>Nd 옆 S 는 더 단단히 붙잡혀 있나</h2>
<p>Q2 · Q3 와 같은 셀에서 Nd 옆의 자유 S 와 Nd 에서 먼 자유 S 를 하나씩 빼 보고, 빼는 데 드는 에너지를 견줬어요. 빈자리는 전하를 띠지 않게 두고 격자는 고정했어요.</p>
<p>이 표본으로는 <b>구분되지 않아요</b>. 두 쪽 차이가 {fnum(SV['dE'], 2)} eV 로 미리 정한 문턱 {SV['thr']:.1f} eV 안이고, Nd 옆 {n_near} 개 · 먼 쪽 {n_far} 개라 흩어짐과 겹쳐요. 네 계산 모두 전자가 부분적으로 차는 금속성 상태로 나왔다는 점도 같이 적어 둬요.</p>
</section>"""
    li3nd_html = f"""<section id="li3nd">
<h2>원고 Fig. 3g — Li₃Nd 장벽은 이렇게만 써 주세요</h2>
<p>원고 Fig. 3g 에는 우리가 계산한 Li 이동 장벽 두 개 (Li₂S · Li₃Nd) 가 들어가 있어요. Li₃Nd 계산을 다시 점검했고, 그 결과에 맞춰 쓸 수 있는 범위를 정했어요.</p>
<ul class="nb">
<li><b>점검에서 본 것.</b> 장벽 계산 (NEB) 의 출발 · 도착 구조, 곧 Li 하나를 뺀 Li₃Nd 를 이완하면 격자가 셀당 1 eV 넘게 내려가며 크게 재배열해요. 그래서 이 장벽은 '재배열된 작은 셀 (2 × 2 × 2) 위의 값' 이에요.</li>
<li><b>큰 셀로 확인하지 못하는 이유.</b> 3 × 3 × 3 셀에서는 장벽 계산이 수렴하지 않았고, 셀 자체도 이완하면서 크게 재배열했어요. 셀 크기를 키워 값을 확인하는 보통의 방법이 막혀 있어서, 같은 방식으로 다시 돌리지는 않기로 했어요.</li>
<li><b>Li₃Nd 는 이론 구조예요.</b> Materials Project 에서 Li–Nd 에는 안정한 화합물이 없어요.</li>
</ul>
{CLAIM_OPEN}
<div class="card bound" data-claim="{HZ_LI3ND}">
<p class="qlabel"><span class="claim-mark">조건부 인용 · SI 에만 · 단서와 함께</span></p>
<p>SI 에 쓸 수 있는 문장이에요. 뜻을 줄이지 않는 다듬기만 해 주세요.</p>
<p lang="en">{esc(LN['si'])}</p>
<p class="note" style="margin:0">같이 적는 차수 검산 한 줄: 298 K 에서 ν₀ = 10¹³ s⁻¹ 를 가정하면 Γ ≈ {sci(LN['rate'])} s⁻¹ (평균 대기 ≈ {LN['wait'] * 1e9:.1f} ns) 예요. 확산계수나 전도도는 아니에요.</p>
</div>
{CLAIM_CLOSE}
<h3 style="margin-top:18px">이렇게는 쓰지 않아요</h3>
<ul class="dont">
<li><b>본문이나 그림에 장벽 숫자를 싣는 것.</b> 특히 Li₂S 장벽과 나란히 놓고 "Li–Nd 합금이 Li₂S 보다 Li 이동을 돕는다" 고 순위를 매기는 문장이요. 두 계산은 셀 크기와 빈자리 전하가 다르고, 둘 다 셀 크기 수렴을 확인하지 못했어요.</li>
<li><b>Li₂S 장벽 숫자.</b> 아직 인용하지 않는 값이에요.</li>
<li><b>이 장벽을 수렴된 Li₃Nd 의 물성으로 쓰거나, 실험 · 문헌 값과 나란히 놓는 문장.</b></li>
</ul>
</section>"""
    open_html = f"""<section id="open">
<h2>아직 남은 것</h2>
<ul class="nb">
{'<li><b>Q1 은 잠정이에요.</b> 원고 문장으로 옮기기 전에 1저자 동의를 받기로 했어요.</li>' if prov else ''}
<li><b>Nd 가 P 자리에 든 모델의 전자 배치</b> (그림 3a) 는 아직 계산하지 않았어요.</li>
<li><b>목표 조성 (x = 0.02) 에서의 크기는</b> 세 질문 모두 확인하지 않았어요.</li>
</ul>
<p>안정성을 다른 뜻으로 생각하셨다면 알려 주세요.</p>
</section>"""
    ex_more = f"""<li>(Q1{' · 잠정, 1저자 동의 전' if prov else ''}) {esc(Q1['sentence'])}
<span class="en" lang="en">With the Li₃PS₄/Li₂S exchange as the reference, in a cell with Nd/(Nd+P) = 0.40 and with frozen-4f PBE, the Nd@4b model is {Q1['dG']:.2f} eV per Nd higher in energy than the Nd@Li model. Other reservoirs and the magnitude at x = 0.02 were not examined.</span></li>
<li>(Q2) {esc(Q2['sentence'])}
<span class="en" lang="en">For our lowest-energy screening model (Nd on a Li site), with the same set of decomposition products selected by the Materials Project hull, in a closed system at 0 K and with frozen-4f PBE, the decomposition driving force of the Nd₂O₃@LPSCl1.6 cell (Nd on a Li site, 10 formula units, one configuration, nominal Nd/(Nd+P) = 0.2) is {abs(Q2['Y']):.0f} meV/atom larger than that of undoped LPSCl1.6.</span></li>
<li>(S 빈자리) {esc(SV['sentence'])}
<span class="en" lang="en">In the same cell, with a frozen lattice and neutral (closed-shell) vacancies, the vacancy energies of free S next to Nd and far from Nd cannot be distinguished with this sample (n = {n_near} vs {n_far}; difference {fnum(SV['dE'], 2)} eV; all four partially occupied, metallic).</span></li>
"""
    dont_more = """<li><b>"Nd 는 Li 자리에 있다" 처럼 조건 없이 쓰는 문장.</b> Q1 은 Li₂S · Li₃PS₄ 로 조성을 맞춘 한 가지 조건과 높은 Nd 농도에서 나온 결과예요.</li>
<li><b>"Nd₂O₃ 를 넣으면 분해된다 · 불안정하다", 또는 상도 위 거리 (E_above_hull) 라고 부르는 문장.</b> Q2 는 0 K 에서 같은 생성물로 견준 상대 비교예요.</li>
<li><b>Q1 과 Q2 숫자를 한 표에 놓거나 서로 견주는 문장.</b> 셀과 계산 설정이 달라요.</li>
"""
    meth_more = f"""<dt>Q1 자리</dt><dd>Quantum ESPRESSO PBE · GBRV USPP (Li · S · Cl) · pslibrary (P · O) · Nd 는 4f 를 핵심부에 둔 PAW · 52 / 520 Ry · mv smearing 0.01 Ry · k 2 × 2 × 1 · Rietveld 셀 (5 화학식 단위). 셀 모양을 고정하고 부피를 바꿔 가며 에너지를 잰 뒤 (EOS) 가장 낮은 부피에서 원자 이완. 조성 차는 Li₂S · Li₃PS₄ 로 맞춤. 가장 낮은 셀 {Q1['top']['MLi']} · {Q1['top']['MP']}.</dd>
<dt>Q2 분해</dt><dd>PBE · PAW (pslibrary) · 70 / 560 Ry · mv smearing 0.01 Ry. 생성물 다섯은 셀까지 이완, 도핑 전 LPSCl1.6 셀은 셀을 고정하고 원자 이완, 도핑 셀은 9 월 구조 그대로. 생성물 집합은 Materials Project 상도 (GGA/GGA+U) 로 결과 보기 전에 정함. 부피 효과는 계산된 압력으로 어림해 보정. k 를 한 단계 올린 점검에서 원자당 1 meV 안.</dd>
<dt>S 빈자리</dt><dd>Q2 와 같은 도핑 셀 · 격자 고정 · 중성 빈자리 SCF 넷 (Nd 옆 {n_near} · 먼 쪽 {n_far}).</dd>
<dt>Li₃Nd 장벽</dt><dd>PBE · Li₃Nd (Materials Project mp-976264 · BiF₃ 형) 2 × 2 × 2 셀 · 중성 빈자리 · 가장 가까운 c → c 경로 CI-NEB · 출발 · 도착 구조 이완.</dd>
"""

    bi, ei = D["bader_in"], D["elf_in"]
    nb_html = "\n".join(nb_lines)
    toc = [("summary", "요약"), ("bg", "배경"), ("site", "Q1 자리"), ("decomp", "Q2 분해"), ("q", "Q3 전자 배치"),
           ("concepts", "개념"), ("pauling", "Pauling 으로 보면"), ("replace", "무엇을 대신하나"), ("bader", "Bader 전하"),
           ("density", "밀도"), ("elf", "ELF"), ("table", "한 표로"), ("svac", "S 빈자리"), ("li3nd", "Fig. 3g 장벽"),
           ("write", "원고에 옮길 때"), ("open", "남은 것"), ("methods", "계산 조건")]
    toc_html = "".join(f'<a href="#{a}">{b}</a>' for a, b in toc)

    return f"""<div class="wrap">
<header>
<p class="eyebrow">CEI · Nd/O 공도핑 LPSCl1.6 · 계산 결과 설명 · 2026-10-26 갱신 (처음 2026-10-20)</p>
<h1>Nd 를 넣으면 무엇이 달라지나</h1>
<p class="sub">자리 (Q1) · 분해 (Q2) · 전자 배치 (Q3) 계산 결과를 처음 보는 사람도 읽을 수 있게 풀었어요. 전자 배치는 Pauling 전기음성도로 본 기대와 DFT (Bader 전하 · ELF) 를 나란히 놓았어요. 원고 Fig. 3g 의 Li₃Nd 장벽을 쓸 수 있는 범위도 같이 적었어요.</p>
<nav class="toc" aria-label="Sections">{toc_html}</nav>
</header>

<section id="summary" class="card answer">
<h2>요약</h2>
<ol class="sum">
<li><b>Q1 자리{' (잠정)' if prov else ''}.</b> 이 계산 조건에서는 Nd 가 Li 자리에 있을 때 에너지가 낮아요. P 자리 (Rietveld 4b) 모델이 Nd 하나당 {Q1['dG']:.2f} eV 높아요. 농도와 4f 처리 같은 조건이 실험과 달라서, Rietveld 결과를 반박하는 근거로는 쓰지 않아요.</li>
<li><b>Q2 분해.</b> 같은 조건에서 견주면 Nd₂O₃ 를 넣은 셀이 넣기 전보다 분해 생성물 쪽으로 원자당 {abs(Q2['Y']):.0f} meV 더 기울어 있어요. '불안정하다' 는 뜻은 아니에요.</li>
<li><b>Q3 전자 배치.</b> 방향은 Nd 가 무엇을 대신하느냐로 정해지고, 이번 Li 자리 모델은 전기음성도가 말하는 방향 그대로 나왔어요. Nd 와 닿은 S²⁻ · Cl⁻ · PS₄ 단위는 Li 만 이웃한 같은 종류보다 {sh_lo:.2f}–{sh_hi:.2f} e 덜 음전하이고, Nd 는 형식 전하 +3 가운데 {nd_share:.0f} % 만 내줬어요 (Li 는 {li_share:.0f} %). Nd–음이온 결합은 주로 이온 결합이고, Li–음이온보다 공유성이 조금 더 있어요.</li>
<li><b>Nd 옆 S 가 더 단단히 붙잡혀 있는지는</b> 이 계산으로 구분되지 않아요.</li>
<li><b>원고 Fig. 3g 의 Li₃Nd 장벽은</b> 본문에서 빼고, SI 에 단서 문장과 함께만 써 주세요. Li₂S 와 순위를 매기지 않아요.</li>
</ol>
</section>

{bg_html}

{site_html}

{decomp_html}

<section id="q">
<h2>Q3. 전자 배치 — 1저자가 정리한 질문</h2>
<div class="card quote">
<p class="qlabel">1저자 카톡 요지 · 2026-10-14</p>
<p class="qhead">Nd/O 치환에 의해 전해질 격자 구조 내에서 전자 배치가 바뀐다</p>
<ol>
<li>P–S 결합보다 Nd–S 와 P–O 결합에서 모두 전자가 음이온에 더 많이 배치된다 (Pauling Nd 1.14 · P 2.19 · S 2.58 · O 3.44)</li>
<li>전자 구름의 부피가 아닌 전자 구름의 밀도가 중요</li>
<li>전해질 자체만 놓고 생각하기에 전기화학적 개념이 아님</li>
<li>이온 결합보다 전자의 배치가 중요</li>
</ol>
</div>
<p>주장마다 이번 계산으로 본 것을 먼저 짧게 적고, 아래에서 그림으로 하나씩 풀어요.</p>
<div class="tablewrap"><table class="claims">
<thead><tr><th>주장</th><th>짧은 답</th><th>그림</th></tr></thead>
<tbody>
<tr><td>전자 배치가 바뀐다</td><td>바뀌어요. Nd 와 닿은 음이온은 전자가 조금 적고 ({sh_lo:.2f}–{sh_hi:.2f} e), Bader 영역이 {v_lo:.0f}–{v_hi:.0f} % 작아요.</td><td>4 · 6</td></tr>
<tr><td>1. Nd–S · P–O 에서 음이온 쪽 전자가 더</td><td>P–S 와 견주면 전기음성도로는 맞는 방향이에요. 다만 이번 모델의 Nd 는 Li 를 대신해서 Nd–S 의 비교 상대가 Li–S 이고, 그 비교에서는 조금 덜해요. 이 비교에서도 전기음성도와 DFT 는 같은 방향이에요. P 에 붙은 O 는 이 셀의 S²⁻ 보다 음전하가 커요.</td><td>2 · 3 · 4</td></tr>
<tr><td>2. 부피가 아니라 밀도</td><td>Nd 옆 S²⁻ · Cl⁻ 의 전자 밀도가 {nv_lo:.0f}–{nv_hi:.0f} % 높아요. 전자가 늘어서가 아니라 영역이 줄어서예요.</td><td>6</td></tr>
<tr><td>3. 전기화학 개념이 아님</td><td>같은 생각이에요. 이 계산은 전해질 셀 하나의 바닥 상태만 봐요 (전압 · Li 출입 · 계면 없음).</td><td>—</td></tr>
<tr><td>4. 이온 결합보다 전자 배치</td><td>전자 배치로 보면 Nd–음이온은 주로 이온 결합이고 Li–음이온보다 공유성이 조금 더 있어요. 이 묘사만으로 안정성을 말하지는 않아요.</td><td>5 · 7</td></tr>
</tbody></table></div>
</section>

<section id="concepts">
<h2>먼저 개념 세 가지</h2>
<div class="trio">
<div class="concept"><h3>전기음성도 χ (Pauling)</h3><p>원자가 결합 전자를 자기 쪽으로 끌어당기는 세기예요. 결합한 두 원자의 차 Δχ 가 클수록 전자가 χ 가 큰 쪽 (음이온) 으로 더 쏠려요. Δχ 가 작으면 전자를 나눠 갖는 공유 결합에, 크면 이온 결합에 가까워요.</p></div>
<div class="concept"><h3>Bader 전하</h3><p>계산한 전자 밀도를 원자마다 나눠서 (밀도가 가장 옅은 골짜기 면이 경계) 각 원자 몫의 전자를 센 값이에요. + 는 전자를 내준 것, − 는 받은 것이에요. 형식 전하 (Li⁺ = +1, S²⁻ = −2) 보다 작게 나오는 게 보통이라, 같은 계산 안에서 원자끼리 견줄 때 의미가 있어요.</p></div>
<div class="concept"><h3>ELF (전자 국재 함수)</h3><p>전자쌍이 한 곳에 모여 있는 정도를 0–1 로 나타내요. 공유 결합이면 두 원자 사이 가운데에 전자쌍이 있어서 결합 중점 값이 높고 (0.9 안팎), 이온 결합이면 전자가 음이온에 붙어 있어 중점 값이 낮아요.</p></div>
</div>
{fig_elfschem}
</section>

<section id="pauling">
<h2>Pauling 전기음성도로 보면</h2>
<p>1저자가 쓴 값 (Nd 1.14 · P 2.19 · S 2.58 · O 3.44) 에 같은 Pauling 표의 Li {PAULING['Li']:.2f} · Cl {PAULING['Cl']:.2f} 를 더해 한 줄에 놓았어요. Nd 는 Li 바로 옆에 있고 P 와는 멀어요.</p>
{fig_scale}
<p>결합 하나의 극성은 두 원자의 차 Δχ 로 봐요. 아래는 이 셀에 있는 결합들의 Δχ 예요.</p>
{fig_dchi}
<p>1저자 1 번 주장은 이 그림에서 바로 나와요. P–S 의 Δχ 는 {d_ps:.2f}, P–O 는 {d_po:.2f}, Nd–S 는 {d_nds:.2f} 라서 셋 가운데 P–S 결합의 전자가 음이온 쪽으로 가장 덜 쏠려요.</p>
<p class="note">Pauling 은 Δχ 로 이온성 퍼센트 (percent ionic character) 를 어림하는 식 1 − e<sup>−Δχ²/4</sup> 도 줬어요. 그림 2 의 표 보기에 같이 적었지만, 이 % 를 그대로 읽으면 Li₂S 의 Li–S 도 {pct_lis:.0f} % 로 절반만 이온성이 돼요. 그래서 여기서는 결합끼리 순서를 보는 데만 써요.</p>
</section>

<section id="replace">
<h2>방향은 Nd 가 대신하는 원자가 정해요</h2>
<p>Nd 가 들어가면 원래 그 자리에 있던 원자 대신 Nd 가 음이온과 결합해요. 그래서 음이온 쪽 전자가 늘었는지는 Nd–S 를 무엇과 견주느냐에 달려 있어요.</p>
{fig_replace}
<p>1저자의 Rietveld 정련은 Nd 를 P 자리 (4b) 에 두었고 (그림 3a), 이 페이지의 DFT 모델은 Nd 를 Li 자리에 둔 모델이에요 (그림 3b). 이 모델에서 Nd 하나는 Li 셋의 몫을 맡아요. 한 자리에는 Nd 가 앉고, 두 자리는 전하를 맞추려고 비워 뒀어요. 자리별 에너지는 위 Q1 에서 따로 견줬어요{' (잠정)' if prov else ''}.</p>
</section>

<section id="bader">
<h2>DFT 결과 1. Nd 옆 음이온은 전자가 조금 적어요</h2>
<p>같은 셀 안에서 Nd 와 닿은 음이온과, Li 만 이웃한 같은 종류의 음이온을 견줬어요. 닿았다고 보는 거리는 결과를 보기 전에 정했어요 (Nd–S · Nd–Cl {D['rules']['R_NdX']:.1f} Å, Nd–O {D['rules']['R_NdO']:.1f} Å). 이 셀의 Nd 두 개는 각각 음이온 여섯과 닿아 있어요.</p>
<ul class="nb">
{nb_html}
</ul>
{fig_shift}
<p>Nd 와 닿은 자유 S²⁻ 는 {fnum(fs['near_mean'])} e, Li 만 이웃한 자유 S²⁻ 는 {fnum(fs['ref_mean'])} e 예요. 결합 상대가 Li 에서 Nd 로 바뀌면 Δχ 가 {d_lis:.2f} 에서 {d_nds:.2f} 로 조금 줄어서 S 쪽 전자가 조금 줄 거라는 기대와 방향이 같아요. Cl⁻ ({fnum(cl['ref_mean'])} → {fnum(cl['near_mean'])} e) 도 같아요.</p>
<p class="note">PS₄ 는 P 와 S 넷을 더한 단위 전하로 견줬어요. 이번 Bader 계산에서는 P–S 결합 사이의 전자 일부가 P 나 S 한쪽에 통째로 붙는 분할 문제가 있어서, PS₄ 안의 P · S 값은 하나씩 쓰지 않아요. 단위 합은 이 문제에 흔들리지 않아요. 이 지표는 결과를 본 뒤에 골랐어요.</p>
{fig_cation}
<p>양이온 쪽에서 보면 Nd 는 {fnum(ca['nd_mean'], 2, True)} e 로 형식 전하 +3 가운데 {nd_share:.0f} % 만 내줬고, Li 는 {fnum(ca['li_mean'], 2, True)} e 로 {li_share:.0f} % 를 내줬어요. Li 는 Nd 를 넣기 전 LPSCl1.6 (같은 방법 {fnum(ca['host_li'], 2, True)} e) 과 그대로예요. χ 가 Li 보다 큰 Nd 가 전자를 덜 내주는 것은 전기음성도와 같은 방향이에요. 다만 Nd 는 형식 전하가 +3 이라는 점도 이 비율에 들어가서, 이 차이를 전기음성도만의 효과로 읽지는 않아요.</p>
</section>

<section id="density">
<h2>DFT 결과 2. 밀도는 높아지는데, 전자가 늘어서가 아니에요</h2>
<p>1저자 2 번 주장 (부피가 아니라 밀도) 은 Bader 영역 안의 전자 수를 영역 부피로 나눈 값으로 봤어요.</p>
{fig_density}
<p>Nd 옆 자유 S²⁻ 는 전자 수가 {fnum(-de['S']['N']['pct'], 0)} % 줄고 영역 부피가 {fnum(-de['S']['V']['pct'], 0)} % 줄어서 밀도가 {fnum(de['S']['NV']['pct'], 0)} % 높아요. Cl⁻ 도 {fnum(-de['Cl']['N']['pct'], 0)} % · {fnum(-de['Cl']['V']['pct'], 0)} % · {fnum(de['Cl']['NV']['pct'], 0)} % 로 같은 꼴이에요. 밀도로 보면 Nd 옆이 뚜렷하게 다르고, 전자 수로 보면 거의 같아요. Nd 의 Bader 영역이 Li 보다 훨씬 커서 ({ca['nd_V']:.1f} Å³, Li {ca['li_V']:.1f} Å³) 이웃 음이온의 공간을 가져가서 생긴 차이예요. 원고에 밀도를 쓸 때는 전자 수와 부피를 같이 적으면 오해가 없어요.</p>
</section>

<section id="elf">
<h2>DFT 결과 3. Nd–음이온 결합 가운데에는 공유 전자쌍이 없어요</h2>
<p>결합 중점에서 ELF 를 견줬어요. P–S · P–O 는 {po_mid:.2f}–{ps_mid:.2f} 로 가운데에 공유 전자쌍이 있고, Nd–S · Nd–Cl · Nd–O 는 {min(nd_mid):.2f}–{max(nd_mid):.2f} 로 없어요.</p>
{fig_elf}
<p>Bader 와 ELF 는 다른 것을 재요. Bader 는 Nd 가 Li 보다 전자를 덜 내줬다는 것을, 중점 ELF 는 Nd–S 가 P–S 꼴 공유 결합은 아니라는 것을 보여 줘요. 둘을 합치면 주로 이온 결합이고 Li–음이온보다 공유성이 조금 더 있다는 그림이에요. ELF 는 그 공유성이 얼마나 되는지는 재지 못해서, ELF 결과는 Bader 를 확인했다기보다 어긋나지 않는다는 데까지예요.</p>
<p class="note">두 가지는 일부러 그림에서 빼거나 읽지 않았어요. Li–S · Li–Cl 의 중점 ELF 는 0.89–0.93 으로 높게 나오는데, Li 가 작아서 결합 중점이 S · Cl 의 전자 껍질 안에 들어가기 때문이에요. 공유 결합이라는 뜻이 아니어서 그림에서 뺐어요. 그리고 Nd–S · Nd–Cl · Nd–O 의 중점 값 순서가 전기음성도 순서와 같아 보이지만, 결합 길이가 달라서 ({el['Nd-S']['d']:.2f} · {el['Cl-Nd']['d']:.2f} · {el['Nd-O']['d']:.2f} Å) 이 값으로 이온성 순서를 매기지 않아요.</p>
</section>

<section id="table">
<h2>전기음성도와 DFT 를 한 표로</h2>
<div class="tablewrap"><table class="cmp">
<thead><tr><th>비교</th><th>모델</th><th>전기음성도 기대</th><th>DFT (이 셀)</th><th>판정</th></tr></thead>
<tbody>{cmp_html}</tbody></table></div>
</section>

{svac_html}

{li3nd_html}

<section id="write">
<h2>원고에 옮길 때</h2>
<h3>이렇게 쓸 수 있어요 (예)</h3>
<ol class="ex">
{ex_more}<li>(Q3) 같은 셀 · 같은 설정에서 Nd 와 닿은 자유 S²⁻ 의 Bader 전하는 Li 만 이웃한 자유 S²⁻ 보다 {fs['shift']:.2f} e 덜 음이다 (각 {len(fs['near'])} 개).
<span class="en" lang="en">In the same cell and with the same settings, free S²⁻ in contact with Nd carries a Bader charge {fs['shift']:.2f} e less negative than free S²⁻ coordinated only by Li (two sites each).</span></li>
<li>(Q3) Pauling 전기음성도 차는 Nd–S ({d_nds:.2f}) 가 Li–S ({d_lis:.2f}) 보다 조금 작고 P–S ({d_ps:.2f}) 보다 훨씬 크다. Li 자리 모델의 Bader 전하는 Nd 가 Li 를 대신할 때 기대되는 방향을 따른다.
<span class="en" lang="en">The Pauling electronegativity difference is slightly smaller for Nd–S ({d_nds:.2f}) than for Li–S ({d_lis:.2f}) and much larger than for P–S ({d_ps:.2f}). The Bader charges of the Li-site model follow the direction expected when Nd replaces Li.</span></li>
<li>(Q3) 결합 중점 ELF 는 P–S {ps_mid:.2f}, Nd–S {el['Nd-S']['mid']:.2f} 로, Nd–S 에는 P–S 와 같은 공유 전자쌍이 없다.
<span class="en" lang="en">The ELF at the bond midpoint is {ps_mid:.2f} for P–S but {el['Nd-S']['mid']:.2f} for Nd–S, so Nd–S has no shared electron pair of the P–S type.</span></li>
</ol>
<h3 style="margin-top:22px">이렇게는 쓰지 않아요</h3>
<ul class="dont">
{dont_more}<li><b>"전자 배치가 바뀌어서 안정하다."</b> Bader · ELF 는 묘사예요. 안정성은 에너지 계산 (자리 · 분해) 이 답하고, 둘을 원인과 결과로 잇지 않아요.</li>
<li><b>"Nd 옆 S 는 전자를 더 받는다."</b> 이번 Li 자리 모델에서는 반대로 나왔어요. 이 문장은 P 자리 모델에서만 시험할 수 있고, 아직 계산하지 않았어요.</li>
<li><b>ELF 중점 값으로 Nd–S · Nd–Cl · Nd–O 의 이온성 순서를 매기는 문장.</b> 결합 길이가 달라서 중점이 음이온에서 떨어진 거리가 달라요.</li>
<li><b>"Li–S 는 공유 결합이다 (ELF 0.93)."</b> Li 가 작아서 중점이 S 껍질 안에 들어가 생긴 값이에요.</li>
<li><b>"ELF 가 0.5 근처라 결합이 없다."</b> 0.5 는 균일 전자기체의 값이라 결합이 있고 없음을 가르는 문턱이 아니에요.</li>
<li><b>계산 셀의 숫자를 실험 조성으로 옮기는 문장.</b> Q2 · Q3 셀은 화학식 단위당 Nd 0.2 개로 목표 조성 (0.02) 의 10 배, Q1 셀은 약 20 배예요.</li>
<li><b>Nd 4f 전자에 관한 문장.</b> 계산에서 4f 전자는 핵심부에 얼려 뒀어요.</li>
<li><b>이 결과로 이온 전도도 변화를 설명하는 문장.</b></li>
<li><b>Pauling 이온성 % 를 절대 이온성으로 쓰는 문장.</b></li>
</ul>
</section>

{open_html}

<section id="methods">
<h2>계산 조건과 자료</h2>
<details class="methods card"><summary>펼쳐 보기</summary>
<dl class="meth">
<dt>구조</dt><dd>{D['formula']} ({D['n_atoms']} 원자). LPSCl1.6 10 화학식 단위에 Nd₂O₃ 1 단위를 넣은 셀이고, Nd 는 Li 자리, O 는 PS₄ 의 S 자리에 있어요. 6 월에 만든 모델을 9 월에 새 Nd PP (4f 핵심부) 로 다시 이완한 구조예요 (부피 −0.15 %). 화학식 단위당 Nd 0.2 개.</dd>
<dt>Bader</dt><dd>Quantum ESPRESSO PBE · PAW 전전자 가전자 밀도 (pp.x plot_num 17) · SCF {bi['ecutwfc']:.0f} / {bi['ecutrho']:.0f} Ry · k {' × '.join(map(str, bi['k']))} · {bi['smearing']} smearing {bi['degauss']} Ry · Henkelman bader 코드 · 순 전하 = 원자가 전자 수 − 센 전자 수 · 전자 합 {D['tot_n']:.3f} (원자가 전자 합 {D['tot_z']:.0f}).</dd>
<dt>이웃 판정</dt><dd>결과 전에 정한 거리 하나 (각도 안 봄): S–P {D['rules']['R_PS']:.1f} Å, O–P {D['rules']['R_PO']:.1f} Å, Nd–S · Nd–Cl {D['rules']['R_NdX']:.1f} Å, Nd–O {D['rules']['R_NdO']:.1f} Å. 3.0–3.6 Å 사이에 애매한 원자는 없었어요.</dd>
<dt>ELF</dt><dd>같은 구조로 노름 보존 PP SCF 를 새로 돌림 (Li · P · S · Cl · O 는 SG15, Nd 는 PseudoDojo 4f 핵심부 PP 를 UPF 로 옮김) · {ei['ecutwfc']:.0f} / {ei['ecutrho']:.0f} Ry · k {' × '.join(map(str, ei['k']))} · pp.x ELF (plot_num 8) · 결합 중점 값 (최소 이미지). 호스트 LPSCl1.6 은 같은 규약 · 같은 도구로 낸 표예요.</dd>
<dt>전기음성도</dt><dd>Pauling 척도. Nd · P · S · O 는 1저자 메시지의 값과 같고, Li {PAULING['Li']:.2f} · Cl {PAULING['Cl']:.2f} 는 같은 표준 표의 값이에요. 이온성 % 식은 L. Pauling, <i>The Nature of the Chemical Bond</i> (3rd ed., 1960) 의 어림식이에요.</dd>
{meth_more}<dt>자료</dt><dd><code>db/raw/nd_q3_bader_2026_10_19/</code> · <code>db/raw/nd_q3_elf_2026_10_19/</code> · 기록 <code>db/properties/nd_q3_bader_elf_runlog_2026_10_19.json</code> · Q1 <code>db/properties/ndo_site_dft_v0_readout_2026_10_23.json</code> · Q2 <code>db/properties/nd_q2_decomp_readout_2026_10_26.json</code> · S 빈자리 <code>db/properties/nd_s_vacancy_closed_2026_10_20.json</code> · Li₃Nd 인용 범위 <code>db/properties/citation_hazards.json</code> · 그림 숫자 <code>db/properties/cei_figs/{CSV_PREFIX}*.csv</code> · 생성기 <code>tools/figures/build_nd_electronegativity_page.py</code></dd>
</dl>
</details>
</section>

<footer>2026-10-26 갱신 (처음 2026-10-20) · 숫자는 원자료 파일에서 생성기가 뽑았어요 (손으로 옮기지 않았어요). 한계: Q3 · S 빈자리는 Nd 두 개 · 구조 하나, Q1 은 모델마다 후보 10 개, Q2 는 Nd · O 배치 하나.</footer>
</div>
"""


def assemble(D, standalone):
    head = (f"<title>{TITLE}</title>\n"
            '<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'<meta name="description" content="{esc(DESCRIPTION)}">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            f'<link rel="stylesheet" href="{FONTS}">\n'
            f"<style>{CSS}</style>\n")
    body = page_body(D) + '<div id="tip" role="tooltip" hidden></div>\n' + f"<script>{JS}</script>\n"
    if not standalone:
        return head + body
    return ('<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + "</head>\n<body>\n" + body + "</body>\n</html>\n")


def check_page(html_text, ea):
    """⑪ 만든 페이지 — Li₂S 장벽 (BLOCKED) 은 어디에도 없고, Li₃Nd 장벽은 결속 블록 안에만 있다."""
    if "0.305" in html_text or "0.31 eV" in html_text:
        raise CheckError("⑪ Li₂S 장벽 (BLOCKED) 이 페이지에 있다")
    v = f"{ea:.3f}"
    i, j = html_text.find(CLAIM_OPEN), html_text.find(CLAIM_CLOSE)
    if html_text.count(CLAIM_OPEN) != 1 or i < 0 or j < i:
        raise CheckError("⑪ Li₃Nd 결속 블록이 하나가 아니다")
    blk = html_text[i:j]
    if f'data-claim="{HZ_LI3ND}"' not in blk or 'class="claim-mark"' not in blk:
        raise CheckError("⑪ 결속 블록에 data-claim · claim-mark 가 없다")
    if blk.count(v) < 1 or html_text.count(v) != blk.count(v):
        raise CheckError(f"⑪ Li₃Nd 장벽 {v} 가 결속 블록 밖에 있다")


# ── Origin CSV ──────────────────────────────────────────────────────────────
def write_csvs(D, outdir):
    outdir = pathlib.Path(outdir)
    files = {}

    def w(name, head, rows):
        path = outdir / f"{CSV_PREFIX}{name}.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            cw = csv.writer(f)
            cw.writerow(head)
            cw.writerows(rows)
        files[name] = path

    w("fig1_pauling", ("element", "chi_pauling", "source"),
      [(e, v, "first_author_message" if e in FIRST_AUTHOR_EN else "same_standard_table")
       for e, v in sorted(PAULING.items(), key=lambda kv: kv[1])])
    w("fig2_delta_chi", ("bond", "anion", "cation", "delta_chi", "pauling_ionic_character_pct_ordering_only"),
      [(b["bond"].replace("–", "-"), b["anion"], b["cation"], b["dchi"], round(b["pct"], 2)) for b in D["bonds"]])
    w("fig4_anion_shift", ("anion_class", "group", "site", "bader_net_e", "shift_from_li_only_mean_e"),
      [(c["name"], g, lab, round(v, 4), round(v - c["ref_mean"], 4))
       for c in D["shift"] for g, vals in (("li_only", c["ref"]), ("next_to_nd", c["near"])) for v, lab in sorted(vals)])
    ca = D["cation"]
    w("fig5_cation_share", ("cation", "site", "bader_net_e", "formal_charge", "share_pct"),
      [("Li", f"mean_of_{ca['li_n']}", round(ca["li_mean"], 4), 1, round(100 * ca["li_mean"], 2)),
       ("Li_undoped_LPSCl1.6", "runlog", ca["host_li"], 1, round(100 * ca["host_li"], 2))]
      + [("Nd", i, v, 3, round(100 * v / 3, 2)) for i, v in ca["nd"]])
    w("fig6_density", ("anion", "quantity", "li_only_mean", "next_to_nd_mean", "change_pct", "n_li_only", "n_next_to_nd"),
      [(an, q, round(D["density"][an][k]["ref"], 5), round(D["density"][an][k]["near"], 5),
        round(D["density"][an][k]["pct"], 2), D["density"][an]["n_ref"], D["density"][an]["n_near"])
       for an in ("S", "Cl", "O") for k, q in (("N", "electrons_e"), ("V", "volume_A3"), ("NV", "density_e_per_A3"))])
    q1, q2 = D["q1"], D["q2"]
    w("fig8_site_energy", ("model", "nd_site", "lowest_cell", "energy_rel_li_site_model_eV_per_Nd", "status"),
      [("M_Li", "Li", q1["top"]["MLi"], 0.0, "reference"),
       ("M_P", "P_4b", q1["top"]["MP"], round(q1["dG"], 4), "provisional" if q1["provisional"] else "final")])
    w("fig9_decomp_difference", ("quantity", "value_meV_per_atom", "resolution_meV_per_atom"),
      [("Y_pressure_corrected_B25GPa", round(q2["Y"], 3), q2["res"]), ("Y_uncorrected", round(q2["Y_raw"], 3), q2["res"])])
    hp = D["host_ps"]
    w("fig7_elf_midpoint", ("bond", "cell", "n_bonds", "mean_dist_A", "elf_midpoint", "elf_sd"),
      [(r["bond"], "Nd_doped", r["n"], r["d"], r["mid"], r["sd"]) for r in D["elf"]]
      + [("P-S", "undoped_LPSCl1.6", hp["n"], hp["d"], hp["mid"], hp["sd"])])
    return files


# ── 시험 ────────────────────────────────────────────────────────────────────
def selftest():
    passed = 0

    def ok(cond, msg):
        nonlocal passed
        if not cond:
            raise AssertionError(msg)
        passed += 1

    D = derive(REPO)
    ok(abs(dchi("Nd", "S") - 1.44) < 1e-9 and abs(dchi("P", "S") - 0.39) < 1e-9, "Δχ")
    ok(abs(ionic_pct(1.60) - 47.27) < 0.05, "Pauling % 식")
    sh = {c["name"]: c for c in D["shift"]}
    ok(abs(sh["Free S²⁻"]["shift"] - 0.2195) < 1e-3 and abs(sh["Cl⁻"]["shift"] - 0.0806) < 1e-3, "음이온 이동")
    ok(abs(sh["PS₄ unit (P + 4 S)"]["shift"] - 0.1978) < 1e-3, "PS₄ 단위 이동")
    ok(abs(D["density"]["S"]["NV"]["pct"] - 21.19) < 0.05 and abs(D["density"]["Cl"]["NV"]["pct"] - 16.61) < 0.05, "밀도 %")
    ok(abs(D["cation"]["nd_mean"] - 1.95875) < 1e-4 and abs(D["cation"]["host_li"] - 0.883) < 1e-9, "양이온")
    ok(sorted(len(n["neighbours"]) for n in D["nd_nb"]) == [6, 6], "Nd 이웃 여섯씩")
    ok(all("Li" not in r["bond"].split("-") for r in D["elf"]), "ELF 그림에 Li–X 없음")
    page, body = assemble(D, True), assemble(D, False)
    ok(page.startswith("<!DOCTYPE html>") and "<body>" in page, "단독 문서 골격")
    ok("<!DOCTYPE" not in body and "<body" not in body and "<html" not in body, "Artifact 본문엔 골격 없음")
    ok(all(f"Fig. {k}." in page for k in range(1, 10)), "그림 1–9 캡션")
    ok(page.count('class="tv"') == 8, "표 보기 8 개")
    ok("S_PS4" not in page, "PS₄ 안 S 자리 값이 페이지에 없다")
    q1, q2, sv, ln = D["q1"], D["q2"], D["svac"], D["li3nd"]
    ok(abs(q1["dG"] - 0.4899) < 1e-3 and q1["top"] == {"MP": "MP_07", "MLi": "MLi_04"} and (q1["a_li2s"], q1["b_li3ps4"]) == (8, -2), "Q1 원자료")
    ok(abs(q2["Y"] + 22.259) < 0.01 and q2["res"] == 2.0 and "22 meV/atom" in q2["sentence"], "Q2 원자료")
    ok("Li₃PS₄ · Li₂S · LiCl · Li₃PO₄ · Nd₂S₃" in page, "Q2 생성물 이름을 원자료에서")
    ok(sv["dE"] == -0.11 and sv["thr"] == 0.3, "S 빈자리 확정값")
    ok(abs(ln["ea"] - 0.228981) < 1e-6 and 1e9 < ln["rate"] < 2e9, "Li₃Nd 장벽 · 홉 수 검산")
    for doc in (page, body):
        check_page(doc, ln["ea"])
    ok(True, "⑪ 만든 페이지 (단독 · Artifact 본문) 통과")
    # Q1 지위 표지 — 양쪽을 본다: 카드가 proposed 면 일곱 자리 전부에 있고, active 로 바꾸면 전부 빠진다
    ok(q1["provisional"] and page.count("잠정") == 7 and "Q1, provisional" in page, "Q1 잠정 표지 7 자리 (카드 proposed)")
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        for key, rel in IN.items():
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(REPO / rel, root / rel)
        dp = root / IN["decisions"]
        dd = json.loads(dp.read_text(encoding="utf-8"))
        hit = [d for d in dd["decisions"] if d.get("id") == Q1_CARD]
        ok(len(hit) == 1, "Q1 카드 결정이 원장에 하나")
        hit[0]["decision_state"] = "active"
        dp.write_text(json.dumps(dd, ensure_ascii=False), encoding="utf-8")
        D2 = derive(root)
        p2 = assemble(D2, True)
        ok(not D2["q1"]["provisional"] and "잠정" not in p2 and "provisional" not in p2,
           "Q1 카드를 active 로 바꾸면 잠정 표지가 전부 빠진다")
    ok(page.index('id="site"') < page.index('id="decomp"') < page.index('id="q"') < page.index('id="svac"') < page.index('id="li3nd"'), "절 순서")
    for tag_, doc_, want_ in (("Li₂S 0.305 를 넣음", page.replace("</footer>", " 0.305 eV</footer>"), "⑪"),
                              ("0.229 를 블록 밖에 둠", page.replace("<footer>", "<footer>0.229 eV · "), "⑪"),
                              ("claim-mark 를 뺌", page.replace('class="claim-mark"', 'class="x"'), "⑪")):
        try:
            check_page(doc_, ln["ea"])
            raise AssertionError(f"{tag_}: 못 잡았다")
        except CheckError as e:
            ok(str(e).startswith(want_), f"{tag_}: 다른 검사 — {e}")
    with tempfile.TemporaryDirectory() as td:
        out = write_csvs(D, td)
        ok(len(out) == 8 and all(p.stat().st_size > 0 for p in out.values()), "CSV 8 개")
        ok("−" not in "".join(p.read_text(encoding="utf-8") for p in out.values()), "CSV 는 ASCII 마이너스")

    # ── 음성 경로: 틀린 입력을 잡는가 ──
    def mutated(tag, edit, expect):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            for key, rel in IN.items():
                (root / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(REPO / rel, root / rel)
            edit(root)
            try:
                derive(root)
            except CheckError as e:
                ok(str(e).startswith(expect), f"{tag}: 다른 검사가 걸렸다 — {e}")
                return
            raise AssertionError(f"{tag}: 틀린 입력을 못 잡았다")

    def edit_sites(fn):
        def run(root):
            path = root / IN["sites"]
            rows = list(csv.DictReader(open(path, encoding="utf-8")))
            fn(rows)
            with open(path, "w", newline="", encoding="utf-8") as f:
                cw = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                cw.writeheader()
                cw.writerows(rows)
        return run

    def relabel(rows):
        for r in rows:
            if r["index"] == "51":
                r["category"] = "S_free"

    def shift_pair(rows):            # 전자 합 · net=ZVAL−N 은 그대로, P86 단위 합만 바뀐다
        for r in rows:
            if r["index"] == "86":
                r["net_e"] = f"{float(r['net_e']) + 0.1:.4f}"
                r["N_bader_e"] = f"{float(r['N_bader_e']) - 0.1:.4f}"
            if r["index"] == "1":
                r["net_e"] = f"{float(r['net_e']) - 0.1:.4f}"
                r["N_bader_e"] = f"{float(r['N_bader_e']) + 0.1:.4f}"

    def total_off(rows):
        for r in rows:
            if r["index"] == "1":
                r["net_e"] = f"{float(r['net_e']) - 0.2:.4f}"
                r["N_bader_e"] = f"{float(r['N_bader_e']) + 0.2:.4f}"

    def net_only(rows):
        for r in rows:
            if r["index"] == "60":
                r["net_e"] = f"{float(r['net_e']) + 0.05:.4f}"

    def drop_nds(root):
        path = root / IN["elf"]
        path.write_text("".join(line for line in path.read_text(encoding="utf-8").splitlines(True)
                                if ",Nd-S," not in line), encoding="utf-8")

    def card_typo(root):
        path = root / IN["card"]
        path.write_text(path.read_text(encoding="utf-8").replace("Nd 1.14", "Nd 1.41"), encoding="utf-8")

    def runlog_ref(root):
        path = root / IN["runlog"]
        path.write_text(path.read_text(encoding="utf-8").replace("−2.442", "−2.452"), encoding="utf-8")

    mutated("분류 바꿈", edit_sites(relabel), "①")
    mutated("단위 합 바꿈", edit_sites(shift_pair), "②")
    mutated("runlog 기준 글자 바꿈", runlog_ref, "②")
    mutated("전자 합 어긋남", edit_sites(total_off), "③")
    mutated("Nd-S 행 빠짐", drop_nds, "④")
    mutated("카드 Pauling 오기", card_typo, "⑤")
    mutated("net 만 바꿈", edit_sites(net_only), "⑥")

    def text_edit(key, old, new):
        def run(root):
            path = root / IN[key]
            t = path.read_text(encoding="utf-8")
            assert old in t, (key, old)
            path.write_text(t.replace(old, new), encoding="utf-8")
        return run

    def json_edit(key, fn):
        def run(root):
            path = root / IN[key]
            d = json.loads(path.read_text(encoding="utf-8"))
            fn(d)
            path.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        return run

    def y_off(d):  # 반올림 (22 meV/atom) 은 그대로 — 허용 문장 대조가 아니라 원자료 대조가 잡아야 한다
        d["Y_meV_per_atom"]["보정_B25"] = -22.4

    def hz_blocked(d):
        for h in d["hazards"]:
            if h.get("id") == HZ_LI3ND:
                h["level"] = "BLOCKED"

    mutated("Q1 runlog 글자 바꿈", text_edit("q1_runlog", "+0.490", "+0.500"), "⑦")
    mutated("Q2 판독 Y 바꿈", json_edit("q2_readout", y_off), "⑧")
    mutated("Q2 생성물 하나 뺌", json_edit("q2_raw", lambda d: d["basis"].pop("Nd2S3")), "⑧")
    mutated("S 빈자리 허용 문장 값 바꿈", text_edit("svac", "차 −0.11 eV", "차 −0.21 eV"), "⑨")
    mutated("Li₃Nd 항목을 BLOCKED 로", json_edit("hazards", hz_blocked), "⑩")
    global ELF_PLOT
    keep = ELF_PLOT
    try:
        ELF_PLOT = keep + ("Li-S",)
        try:
            derive(REPO)
            raise AssertionError("Li–S 를 그림에 넣었는데 못 잡았다")
        except CheckError as e:
            ok(str(e).startswith("④"), f"Li–S 린트: {e}")
    finally:
        ELF_PLOT = keep
    print(f"selftest {passed}/{passed} 통과 (음성 16 포함)")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out_dir", default=OUT_DIR, help="페이지 · CSV 를 쓸 곳 (저장소 기준)")
    ap.add_argument("--artifact_out", help="Artifact 용 본문 (문서 골격 없음) 을 쓸 경로")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        D = derive(REPO)
    except CheckError as e:
        print(f"⛔ {e} — 아무것도 쓰지 않았다", file=sys.stderr)
        return 2
    page_html, body_html = assemble(D, True), assemble(D, False)
    try:
        check_page(page_html, D["li3nd"]["ea"])
        check_page(body_html, D["li3nd"]["ea"])
    except CheckError as e:
        print(f"⛔ {e} — 아무것도 쓰지 않았다", file=sys.stderr)
        return 2
    outdir = REPO / a.out_dir
    outdir.mkdir(parents=True, exist_ok=True)
    page = outdir / OUT_PAGE
    page.write_text(page_html, encoding="utf-8")
    files = write_csvs(D, outdir)
    print(f"✓ 검사 ①–⑪ 통과 · 페이지 {page.relative_to(REPO)} ({page.stat().st_size:,} B) · CSV {len(files)} 개")
    if a.artifact_out:
        ap_ = pathlib.Path(a.artifact_out)
        ap_.parent.mkdir(parents=True, exist_ok=True)
        ap_.write_text(body_html, encoding="utf-8")
        print(f"✓ Artifact 본문 {ap_}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
