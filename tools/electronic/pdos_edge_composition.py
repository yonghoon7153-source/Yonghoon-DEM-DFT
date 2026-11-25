#!/usr/bin/env python3
"""pdos_edge_composition.py — PDOS CSV 에서 **밴드 가장자리를 누가 만드는가**를 센다.

    python3 tools/electronic/pdos_edge_composition.py \
        --csv db/properties/ndo_lpscl16_n5fu_pdos.csv --label ndo_n5fu
    python3 tools/electronic/pdos_edge_composition.py --selftest

왜 (2026-09-14). 랩 미팅 질문 — *"Nd 가 3가를 유지하는 것과 산화 안정성이 무슨 상관이냐,
분해되는 건 P·S 아니냐"*. 답하려면 **산화가 시작되는 자리(VBM)를 누가 차지하고 있나**를
숫자로 대야 한다. 2026-06 카드에 그 수가 있지만 다른 셀·다른 셋업(4f-in-valence)이라,
지금 셀(n5fu, frozen-4f)에서 다시 세는 경로가 필요했다.

세는 법
  ① VBM = DOS 가 문턱을 넘는 **가장 높은** 점(E ≤ 기준), CBM = 넘는 **가장 낮은** 점(E ≥ 기준).
     기준은 `--ref` (E_minus_Ef 열이 있으면 0, VBM-정렬 CSV 면 0 이 곧 VBM).
  ② 성분 = 선언한 창에서 원소별 적분 / 총합. **창을 반드시 같이 적는다** — 창을 바꾸면 수가 바뀐다.

⛔ 이 도구가 **못 하는 것**
  · **두 계의 VBM 을 절대 비교하지 못한다.** 셀이 다르면 고유값 기준이 달라서 core-level 이나
    진공 준위 정렬이 필요하다. 여기서 나오는 것은 *한 셀 안에서 누가 가장자리를 만드는가* 다.
    "도핑하면 VBM 이 내려간다/올라간다" 는 이 도구로 말할 수 없다.
  · 갭의 크기를 정본으로 내지 않는다. 정본 갭은 fixed-occupation nscf 고유값이다 (CLAUDE.md).
    여기 gap 은 DOS 문턱 판독이라 **과소**로 나온다 (~0.3 eV) — 진단용으로만 쓴다.
  · 스핀을 나누지 않는다. 열이 합쳐진 CSV 를 받는다.
  · 원자당으로 정규화하지 않는다 — 원소 **총** 기여다. 원자 수가 다르면 그대로 반영된다.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
#: DOS 문턱 — 총 DOS 최대값 대비 비율. 판독이 이 값에 딸리므로 결과에 같이 적는다.
DOS_THRESH_FRAC = 0.02
#: 기본 창 (가장자리에서 안쪽으로). 2026-06 Nd 카드가 VBM 을 −2~−0.6 으로 봤다 — 그 관례를 따른다.
VBM_WINDOW_eV = (-2.0, 0.0)
CBM_WINDOW_eV = (0.0, 2.0)


def read_pdos(path):
    """→ (rows, elements, ecol). 열 이름으로 판단한다 — 위치로 추측하지 않는다.

    받는 두 형식
      · `E_eV, E_minus_Ef, total_dos, <원소…>`  (sum_pdos.py 산출)
      · `E_minus_VBM, <원소…>`                   (element_smooth 계열, 이미 VBM 정렬)
    """
    txt = [ln for ln in Path(path).read_text(encoding="utf-8").splitlines()
           if ln.strip() and not ln.lstrip().startswith("#")]
    r = list(csv.reader(txt))
    if len(r) < 3:
        raise ValueError(f"{path}: 데이터 행이 없다")
    hdr = [h.strip() for h in r[0]]
    if "E_minus_Ef" in hdr:
        ecol = hdr.index("E_minus_Ef")
    elif "E_minus_VBM" in hdr:
        ecol = hdr.index("E_minus_VBM")
    else:
        raise ValueError(f"{path}: 에너지 열(E_minus_Ef · E_minus_VBM)이 없다 — "
                         f"열 이름으로만 찾는다 (위치로 추측하지 않는다). 헤더={hdr}")
    skip = {"E_eV", "E_minus_Ef", "E_minus_VBM", "total_dos", "total"}
    els = [h for h in hdr if h not in skip]
    if not els:
        raise ValueError(f"{path}: 원소 열이 하나도 없다 (헤더={hdr})")
    rows = []
    for line in r[1:]:
        if len(line) != len(hdr):
            continue
        try:
            E = float(line[ecol])
            vals = {e: float(line[hdr.index(e)]) for e in els}
        except ValueError:
            continue
        rows.append((E, vals))
    if not rows:
        raise ValueError(f"{path}: 숫자로 읽히는 행이 없다")
    return rows, els, hdr[ecol]


def find_edges(rows, els, thresh_frac=DOS_THRESH_FRAC, ref=0.0, e_lo=-8.0, e_hi=8.0):
    """→ (vbm, cbm, thresh). 기준(ref) 아래 마지막 점 · 위 첫 점. 못 찾으면 None.

    ⚠ 창 밖(깊은 코어·먼 전도대)의 스파이크에 끌리지 않게 [e_lo, e_hi] 안에서만 본다.
      이 창은 **판독 창**이지 성분 창이 아니다 — 둘을 섞지 않는다.
    """
    sub = [(E, sum(v.values())) for E, v in rows if e_lo <= E <= e_hi]
    if not sub:
        return None, None, 0.0
    thresh = thresh_frac * max(t for _, t in sub)
    below = [E for E, t in sub if E <= ref and t > thresh]
    above = [E for E, t in sub if E >= ref and t > thresh]
    return (max(below) if below else None), (min(above) if above else None), thresh


def composition(rows, els, lo, hi):
    """선언한 창 [lo, hi] 의 원소별 적분 비율(%) → (dict, 총적분). 총합 0 이면 None."""
    tot = {e: 0.0 for e in els}
    for E, v in rows:
        if lo <= E <= hi:
            for e in els:
                tot[e] += v[e]
    s = sum(tot.values())
    if s <= 0:
        return None, 0.0
    return {e: 100.0 * tot[e] / s for e in els}, s


def analyze(path, label=None, thresh_frac=DOS_THRESH_FRAC,
            vbm_window=VBM_WINDOW_eV, cbm_window=CBM_WINDOW_eV):
    rows, els, ecol = read_pdos(path)
    vbm, cbm, thresh = find_edges(rows, els, thresh_frac=thresh_frac)
    out = {
        "label": label or Path(path).stem, "csv": str(path), "energy_column": ecol,
        "elements": els, "n_rows": len(rows),
        "dos_threshold_frac_of_max": thresh_frac, "dos_threshold": thresh,
        "VBM_read": vbm, "CBM_read": cbm,
        "gap_read_eV": (None if (vbm is None or cbm is None) else round(cbm - vbm, 4)),
        "⚠_gap": "DOS 문턱 판독이라 정본이 아니다 — 정본 갭은 fixed-occ nscf 고유값이다 (~0.3 eV 과소)",
    }
    for name, (lo, hi), edge in (("VBM", vbm_window, vbm), ("CBM", cbm_window, cbm)):
        if edge is None:
            out[f"{name}_composition_pct"] = None
            out[f"{name}_window_eV"] = None
            out[f"⚠_{name}"] = "가장자리를 못 찾았다 — 성분을 계산하지 않는다 (0 으로 그리지 않는다)"
            continue
        lo_a, hi_a = edge + lo, edge + hi
        comp, integ = composition(rows, els, lo_a, hi_a)
        out[f"{name}_window_eV"] = [round(lo_a, 4), round(hi_a, 4)]
        out[f"{name}_window_rel"] = [lo, hi]
        out[f"{name}_composition_pct"] = (None if comp is None
                                          else {e: round(p, 2) for e, p in sorted(
                                              comp.items(), key=lambda kv: -kv[1])})
        out[f"{name}_integral"] = integ
        if comp is None:
            out[f"⚠_{name}"] = "창 안 적분이 0 이다 — 창이 비었는지 확인해라"
    return out


def _selftest() -> int:
    import tempfile
    n = [0, 0]

    def chk(c, m):
        n[0] += 1
        n[1] += bool(c)
        print(("  ✓ " if c else "  ✗ ") + m)

    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        # 합성: −1..0 은 S 만, 0.5..1.5 는 P 만 → VBM=S 100 %, CBM=P 100 %
        p = d / "synth.csv"
        # ⚠ 격자를 **정수로** 만든다. `E += 0.05` 로 쌓으면 0.5 가 0.5000000000000004 가 되어
        #   경계 비교가 한 칸 밀린다 — 2026-09-14 에 이 시험이 그것으로 빨간불이었다.
        #   시험을 느슨하게 하는 대신 **합성 자료를 정확하게** 만든다.
        lines = ["E_eV,E_minus_Ef,total_dos,Li,P,S"]
        for i in range(-60, 61):                       # i/20 = 0.05 눈금, 0.5 는 i=10 에서 정확
            E = i / 20.0
            li = p_ = s = 0.0
            if -1.0 <= E <= -0.05:
                s = 1.0
            if 0.5 <= E <= 1.5:
                p_ = 1.0
            lines.append(f"{E:.4f},{E:.4f},{li + p_ + s:.3f},{li:.3f},{p_:.3f},{s:.3f}")
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
        r = analyze(p, label="synth")
        chk(abs(r["VBM_read"] - (-0.05)) < 1e-6, f"양성: VBM 판독 {r['VBM_read']} ≈ −0.05")
        chk(abs(r["CBM_read"] - 0.5) < 1e-6, f"양성: CBM 판독 {r['CBM_read']} ≈ 0.5")
        chk(r["VBM_composition_pct"]["S"] > 99.9, "양성: VBM 은 S 100 % 로 나온다")
        chk(r["CBM_composition_pct"]["P"] > 99.9, "양성: CBM 은 P 100 % 로 나온다")
        # ⛔음성 ①: 창을 바꾸면 수가 바뀐다 — 창을 안 적으면 안 되는 이유
        r2 = analyze(p, vbm_window=(-0.2, 0.0))
        chk(r2["VBM_window_eV"] != r["VBM_window_eV"],
            "⛔음성: 창이 다르면 창 기록도 달라진다 (창 없는 성분은 의미가 없다)")
        # ⛔음성 ②: 에너지 열이 없으면 거부 — 위치로 추측하지 않는다
        q = d / "bad.csv"
        q.write_text("A,B,C\n1,2,3\n4,5,6\n", encoding="utf-8")
        try:
            read_pdos(q)
            chk(False, "⛔음성: 에너지 열 없는 CSV 를 거부해야 한다")
        except ValueError as e:
            chk("에너지 열" in str(e), "⛔음성: 에너지 열이 없으면 거부한다")
        # ⛔음성 ③: 원소 열이 없으면 거부
        q2 = d / "noel.csv"
        q2.write_text("E_minus_Ef,total_dos\n-1,0\n0,1\n", encoding="utf-8")
        try:
            read_pdos(q2)
            chk(False, "⛔음성: 원소 열 없는 CSV 를 거부해야 한다")
        except ValueError as e:
            chk("원소 열" in str(e), "⛔음성: 원소 열이 없으면 거부한다")
        # ⛔음성 ④: 전부 0 이면 가장자리를 **못 찾았다**고 말한다 (0 으로 안 그린다)
        q3 = d / "zero.csv"
        q3.write_text("E_minus_Ef,Li,S\n" + "\n".join(f"{x/10:.1f},0,0" for x in range(-30, 31)),
                      encoding="utf-8")
        r3 = analyze(q3)
        chk(r3["VBM_read"] is None and r3["VBM_composition_pct"] is None
            and "⚠_VBM" in r3, "⛔음성: 비어 있으면 '못 찾음' 이라고 적는다 (0 % 로 그리지 않는다)")
        # ⛔음성 ⑤: 창 밖 스파이크에 끌리지 않는다 (깊은 코어 행)
        q4 = d / "spike.csv"
        rows = ["E_eV,E_minus_Ef,total_dos,Li,S", "-42.0,-46.0,9e5,9e5,0"]
        for i in range(-60, 61):
            E = i / 20.0
            s = 1.0 if -1.0 <= E <= -0.05 else 0.0
            rows.append(f"{E:.4f},{E:.4f},{s:.3f},0,{s:.3f}")
        q4.write_text("\n".join(rows) + "\n", encoding="utf-8")
        r4 = analyze(q4)
        chk(r4["VBM_read"] is not None and abs(r4["VBM_read"] - (-0.05)) < 1e-6,
            "⛔음성: 창 밖 코어 스파이크(9e5)가 문턱을 끌어올리지 못한다")

    print(f"selftest {n[1]}/{n[0]} · {'PASS' if n[1] == n[0] else 'FAIL'}")
    return 0 if n[1] == n[0] else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", nargs="+", help="PDOS CSV (여러 개 주면 나란히 센다)")
    ap.add_argument("--label", nargs="+", help="계 이름 (--csv 와 같은 수)")
    ap.add_argument("--out", help="결과 JSON 경로")
    ap.add_argument("--thresh", type=float, default=DOS_THRESH_FRAC)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not a.csv:
        ap.error("--csv 가 필요하다")
    labels = a.label or [None] * len(a.csv)
    if len(labels) != len(a.csv):
        ap.error("--label 수가 --csv 수와 다르다")
    res = [analyze(c, label=l, thresh_frac=a.thresh) for c, l in zip(a.csv, labels)]
    for r in res:
        print(f"\n## {r['label']}  ({r['n_rows']}행 · {', '.join(r['elements'])})")
        print(f"   VBM {r['VBM_read']} · CBM {r['CBM_read']} · gap(판독) {r['gap_read_eV']}")
        for e in ("VBM", "CBM"):
            c = r.get(f"{e}_composition_pct")
            w = r.get(f"{e}_window_eV")
            if c is None:
                print(f"   {e}: 못 찾음 — {r.get('⚠_' + e, '')}")
            else:
                print(f"   {e} 창 {w}: " + " · ".join(f"{k} {v:.1f}%" for k, v in c.items()))
    if a.out:
        Path(a.out).write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n",
                               encoding="utf-8")
        print(f"\n→ {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
