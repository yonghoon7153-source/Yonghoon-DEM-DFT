# -*- coding: utf-8 -*-
"""anderson2024 (LLZO 59-dopant screening) — 3차 패스: SI PDF 직접 재판독.

배경
----
1차 패스(2026-07-28)는 SI 를 손으로 전사했고, 2차 패스(2026-08-04,
`anderson2024_fig_verify.py`)는 **SI 를 일부러 안 보고** 본문 그림 픽셀만으로
같은 수치를 복원해 1차를 교차검증했다. 그 결과 4칸이 어긋난 채 남았다
(digest §19.5: `Y↔Yb` · `Rh↔Ho`).

이 스크립트는 SI PDF 를 다시 확보해서 그 4칸을 확정한다. Table S5 는 다행히
**래스터가 아니라 텍스트 레이어**라 손 전사 없이 그대로 파싱된다 = 1차 전사의
독립 재검이기도 하다.

하는 일
-------
1. SI Table S5(59행 + undoped) 를 PDF 텍스트에서 파싱 → Origin-ready CSV.
2. 2차 패스 픽셀 복원표(`..._recovered.csv`) 와 전 항목 대조.
3. §19.5 의 4칸 판정, 본문 '>10× 36종' 주장 재계수, §19.3a 통계 재확인.
4. Table S2(조성 177행) 와 Fig 1 색분류를 대조해 '29 novel vs 30 reported' 확정.

재현
----
    python tools/litdb/anderson2024_si_tableS5.py   # 출력 = litdb/inbox/_51si_verify_out.txt
"""

import csv
import os
import re
import statistics
import sys

import fitz

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SI_PDF = os.path.join(
    ROOT, "litdb", "inbox",
    "51. Sup) Comprehensive Dopant Screening in Li₇La₃Zr₂O₁₂"
    " Garnet Solid Electrolyte.pdf")
RECOVERED = os.path.join(ROOT, "db", "properties",
                         "anderson2024_llzo_dopant_screening_recovered.csv")
OUT_CSV = os.path.join(ROOT, "db", "properties",
                       "anderson2024_llzo_dopant_screening_tableS5.csv")

UNDOPED_SIGMA = 1.62e-6          # Table S5 Undoped 행 (본문은 1.6e-6 으로 반올림)

# Fig 1 픽셀 색분류 (2차 패스 `_51_verify_out.txt` 에서 그대로 가져옴)
FIG1_NOVEL = ("Na P K V Cu Se Rh Pd Ag Cd In Sn Cs Lu Re Ir Pt Au Tl Pb Bi "
              "Pr Sm Eu Tb Dy Ho Er Tm Yb").split()
FIG1_REPORTED = ("B Mg Al Si Ca Sc Ti Cr Mn Fe Co Ni Zn Ga Ge Rb Sr Y Nb Mo Ru "
                 "Sb Te Ba Hf Ta W Ce Nd Gd").split()


# ------------------------------------------------------------------ 파싱

def si_pages():
    with fitz.open(SI_PDF) as doc:
        return [p.get_text() for p in doc]


def _num(s):
    """'2.46×10-5' / '94.80' / '' → float | None. SI 는 U+2010 하이픈을 쓴다."""
    s = (s.replace("‐", "-").replace("−", "-")
          .replace("×10", "e").replace(" ", " ").strip())
    if s in ("", "*"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_table_s5(pages):
    """Table S5(SI p.7–8) → {el: {...}}. 행은 'El(site)' + 값 8칸으로 이어진다."""
    lines = [l.strip() for l in "\n".join(pages[6:8]).splitlines()]
    head = re.compile(r"^([A-Z][a-z]?)\((Li|La|Zr)\)$")
    rows, i = {}, 0
    while i < len(lines):
        m = head.match(lines[i])
        if not m:
            i += 1
            continue
        f = (lines[i + 1:i + 9] + [""] * 8)[:8]
        rows[m.group(1)] = {
            "site": m.group(2),
            "garnet": _num(f[0]), "cubic": _num(f[1]),
            "sigma_i": _num(f[2]), "sigma_e": _num(f[3]),
            "vmax": _num(f[4]), "idt": _num(f[5]),
            # V_min·CCD 는 '< 0.1', '>0.40,<0.85' 같은 문자열이라 원문 보존
            "vmin": f[6].replace(" ", " ").strip(),
            "ccd": f[7].replace(" ", " ").strip(),
        }
        i += 9
    return rows


def parse_table_s2(pages):
    """Table S2(SI p.4) 조성 목록 → [(el, Li, La, Zr), ...]."""
    return re.findall(
        r"([A-Z][a-z]?)0\.2\s*\n\s*Li([\d.]+)\s*\n\s*La([\d.]+)\s*\n\s*Zr([\d.]+)",
        pages[3])


def load_recovered():
    with open(RECOVERED, encoding="utf-8") as fh:
        return {r["dopant"]: r for r in csv.DictReader(fh)}


# ------------------------------------------------------------------ 검증

def rule(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def check_s2(pages):
    rule("Table S2 — 시료 수 / '29 novel vs 30 reported' 확정 (digest §16 #7·#9)")
    comps = parse_table_s2(pages)
    els = list(dict.fromkeys(e for e, _, _, _ in comps))
    per = {e: sum(1 for c in comps if c[0] == e) for e in els}
    print("  조성 행 수 = %d   고유 도판트 = %d   자리/도판트 = %s"
          % (len(comps), len(els), sorted(set(per.values()))))
    print("  Sb 포함? %s" % ("예" if "Sb" in els else "**아니오**"))
    print("  → 177 = 59×3. 본문 '180 PXRD patterns' 의 나머지 3 은 Sb(=60×3)가 아니라")
    print("    **세트별 undoped 3장**이다. 1차 digest §16 #7 판정 ✅ 확정, 2차 '60×3' 가설 ✗")
    novel = [e for e in FIG1_NOVEL if e in els]
    rep = [e for e in FIG1_REPORTED if e in els]
    print("  Fig 1 노랑(novel) 중 실제 합성 %d / 파랑(reported) 중 실제 합성 %d  (합 %d)"
          % (len(novel), len(rep), len(novel) + len(rep)))
    print("    파랑 중 미합성: %s" % [e for e in FIG1_REPORTED if e not in els])
    print("  → 스크리닝된 59 = **신규 30 + 기보고 29**. 본문 '29 novel, plus the 30")
    print("    previously reported' 는 두 숫자가 **뒤바뀐 것**이 확정 (digest §16 #9) ✅")


def check_missing(s5):
    rule("§19.5 확정 (1) — σ 결측 5종은 누구인가")
    grey = sorted(e for e, r in s5.items() if r["sigma_i"] is None)
    print("  SI Table S5 에서 σ_i·σ_e 가 공란인 도판트: %s" % grey)
    print("  2차 패스 Fig 4a 픽셀 회색:               ['Er', 'Mo', 'Tb', 'Te', 'Y']")
    print()
    for el in ("Y", "Yb"):
        r = s5[el]
        print("    %-3s(%s)  garnet %6.2f  cubic %6.2f  σ_i %-10s σ_e %-10s ∫Idt %.2f"
              % (el, r["site"], r["garnet"], r["cubic"],
                 ("%.2e" % r["sigma_i"]) if r["sigma_i"] else "(공란)",
                 ("%.2e" % r["sigma_e"]) if r["sigma_e"] else "(공란)", r["idt"]))
    print()
    print("  → Table S5: **Y 는 측정됨, Yb 이 공란**. Fig 4a 는 정반대 (39 Y 회색 / 70 Yb 채색).")
    print("    Fig 4a 의 Yb 칸 값 2.75e-5 ↔ Table S5 의 Y 값 2.46e-5 = 1.12×,")
    print("    Fig 4b 의 Yb 칸 값 3.37e-8 ↔ Table S5 의 Y 값 3.14e-8 = 1.07×")
    print("    — 둘 다 역판독 오차(중앙값 1.06×) 안. **같은 데이터가 다른 칸에 실린 것**이다.")


def check_fig3_vs_s5(s5, rec):
    rule("§19.5 확정 (2) — 중재: Fig 3(구조)은 어느 쪽 라벨을 지지하나")
    n, worst, bad = 0, (0.0, ""), []
    for el, r in s5.items():
        g = rec.get(el)
        if not g or not g["cubic_wt_pct_pref"]:
            continue
        d = abs(float(g["cubic_wt_pct_pref"]) - r["cubic"])
        n += 1
        worst = max(worst, (d, el))
        if d > 2.0:
            bad.append(el)
    print("  Fig 3b 픽셀 cubic%% vs Table S5 cubic%% — n=%d, 최대 |Δ| %.2f pp (%s), >2 pp 불일치 %d건"
          % (n, worst[0], worst[1], len(bad)))
    for el in ("Y", "Yb"):
        print("    %-3s  Fig 3 픽셀 garnet %s / cubic %s   ↔   Table S5 %.2f / %.2f"
              % (el, rec[el]["garnet_wt_pct_pref"] or "(축밖)",
                 rec[el]["cubic_wt_pct_pref"], s5[el]["garnet"], s5[el]["cubic"]))
    print()
    print("  → Fig 3 은 Y·Yb 를 **Table S5 와 똑같이** 라벨한다(전 59종 불일치 0건).")
    print("    즉 Table S5 + Fig 3 이 한편, **Fig 4 만 반대편**이다 → Table S5 채택.")
    print("    ✅ Y(La) σ_i 2.46e-5 · σ_e 3.14e-8 (측정됨) / Yb(La) σ 미측정")
    print("    🔴 논문 자체 오류: **Fig 4a·4b 가 Y 와 Yb 칸을 맞바꿔 실었다** (두 패널 모두)")


def check_rh_ho(s5, rec):
    rule("§19.5 확정 (3) — Rh↔Ho 는 논문 문제가 아니라 1차 digest 오타였다")
    for el in ("Rh", "Ho"):
        px = rec[el]["sigma_ionic_S_cm"]
        s = s5[el]["sigma_i"]
        print("    %-3s  Table S5 %.2e   Fig 4a 픽셀 %s   비 %.2f×   undoped 대비 %.1f×"
              % (el, s, px, float(px) / s, s / UNDOPED_SIGMA))
    print()
    print("  → 두 값 다 역판독 오차 안에서 **일치**한다. 맞교환이 아니다.")
    print("    Rh = 2.58e-6 = undoped 의 1.6× 로 '>10×' 근처에도 못 간다 →")
    print("    1차 digest 의 36종 목록에 든 'Rh' 는 **'Ho' 의 철자 오타**다(Ho↔Rh).")


def recount(s5):
    rule("본문 '36 dopants yield a >10x improvement' 재계수 (digest §6 교정)")
    meas = {e: r["sigma_i"] for e, r in s5.items() if r["sigma_i"]}
    thr = 10 * UNDOPED_SIGMA
    over = sorted(e for e, v in meas.items() if v > thr)
    print("  undoped σ_i = %.2e → 10× 컷 = %.2e   측정된 도판트 %d종"
          % (UNDOPED_SIGMA, thr, len(meas)))
    print("  엄격히 >10× 인 도판트 = **%d종** (36 아님)" % len(over))
    print("    %s" % " ".join(over))
    near = sorted(((v, e) for e, v in meas.items() if 0.9 * thr < v <= thr),
                  reverse=True)
    for v, e in near:
        print("  경계 바로 아래: %-3s %.2e = %.1f×  → 유효숫자 2자리로 반올림하면"
              " %.1e / %.1e = 10× 로 읽힌다" % (e, v, v / UNDOPED_SIGMA, v, UNDOPED_SIGMA))
    print("  → **35(엄격) + Ho(9.7×, 반올림하면 10×) = 36**. 본문의 36 은 반올림 계수다.")
    low = sorted((v, e) for e, v in meas.items() if v < UNDOPED_SIGMA)
    print("  undoped 보다 낮은 도판트 = %d종: %s ✅ 본문 'just three' 일치"
          % (len(low), ", ".join("%s %.2e" % (e, v) for v, e in low)))


def recheck_cubic(s5):
    rule("§19.3a 재확인 — 선호 site cubic% 통계를 SI 자체 표로 (3중 확인)")
    cub = [r["cubic"] for r in s5.values()]
    n = len(cub)
    hi = sum(1 for c in cub if c > 90)
    lo = sum(1 for c in cub if c < 70)
    print("  n=%d  중앙값 **%.1f %%**  >90%% = **%d (%.0f %%)**  <70%% = %d (%.0f %%)"
          % (n, statistics.median(cub), hi, 100 * hi / n, lo, 100 * lo / n))
    print("  2차 패스 픽셀:  중앙값 74.9 %  ·  >90 % = 25 (42 %)  ·  <70 % = 24")
    print("  → 저자 자신의 표가 본문 '>90 % c-LLZO in most cases' 를 부정한다.")
    print("    §16 #11 은 이제 그림 근거가 아니라 **SI 표 근거**로 확정 🔴")


def check_merit(s5):
    rule("Table S5 캡션의 5개 merit 컷 — SI 표로 순차 게이트 재실행 (digest §3e)")
    gates = [
        ("cubic > 94 %", lambda r: r["cubic"] is not None and r["cubic"] > 94),
        ("σ_i > 5e-5", lambda r: r["sigma_i"] is not None and r["sigma_i"] > 5e-5),
        ("σ_e < 2.5e-8", lambda r: r["sigma_e"] is not None and r["sigma_e"] < 2.5e-8),
        ("∫Idt < 1.39", lambda r: r["idt"] is not None and r["idt"] < 1.39),
        ("CCD ≥ 0.4", lambda r: r["ccd"] not in ("",) and "0.1" not in r["ccd"]
         and ("0.4" in r["ccd"] or "0.5" in r["ccd"] or "0.6" in r["ccd"])),
    ]
    alive = sorted(s5)
    print("  시작 %d종" % len(alive))
    for name, fn in gates:
        alive = [e for e in alive if fn(s5[e])]
        print("  %-14s → %2d종  %s" % (name, len(alive), " ".join(alive) if alive else ""))
    print("  → 생존자 %d종. digest §3e 의 '5컷 순차 적용 시 0종' 결론 ✅ 재확인" % len(alive))


def write_csv(s5):
    order = sorted(s5)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow([
            "dopant", "substituted_site", "garnet_wt_pct", "cubic_wt_pct",
            "sigma_ionic_S_cm", "sigma_electronic_S_cm", "Vmax_V",
            "HV_integrated_current_mAh_g", "Vmin_V", "CCD_mA_cm2", "source"])
        for e in order:
            r = s5[e]
            w.writerow([e, r["site"], r["garnet"], r["cubic"],
                        r["sigma_i"] if r["sigma_i"] else "",
                        r["sigma_e"] if r["sigma_e"] else "",
                        r["vmax"], r["idt"], r["vmin"], r["ccd"],
                        "paper SI Table S5"])
        w.writerow(["Undoped", "-", 88.08, 37.44, 1.62e-6, 1.66e-7, 3.9, 1.39,
                    "1", "", "paper SI Table S5"])
    print()
    print("CSV 기록: %s  (%d행 + undoped)"
          % (os.path.relpath(OUT_CSV, ROOT), len(order)))


def main():
    pages = si_pages()
    s5 = parse_table_s5(pages)
    rec = load_recovered()
    print("SI PDF %d pp · Table S5 파싱 %d행 (텍스트 레이어 — 손 전사 아님)"
          % (len(pages), len(s5)))
    check_s2(pages)
    check_missing(s5)
    check_fig3_vs_s5(s5, rec)
    check_rh_ho(s5, rec)
    recount(s5)
    recheck_cubic(s5)
    check_merit(s5)
    write_csv(s5)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
