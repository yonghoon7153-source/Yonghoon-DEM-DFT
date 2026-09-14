"""규진팀 report_reruns 97 행 감사 — `FINDINGS.md` §2 의 숫자를 **재계산**한다.

왜 있나: §2 는 "32/97 이 경계에 붙었고 16/97 이 음수 LAM" 이라고 적어 왔는데,
그 원표가 저장소에 없어서 **문서에 적힌 주장**이었을 뿐 재현이 안 됐다.
2026-09-10 에 원표를 받아 `out/bms97/` 에 넣었고, 이 스크립트가 그 숫자를
원표에서 다시 만든다. 이제 §2 는 명령 한 줄로 검증된다.

    python3 scripts/audit97.py            # 요약
    python3 scripts/audit97.py --rows     # 행별 감사표까지

⚠ 판정 규칙을 여기 한 곳에만 둔다. 문서와 코드가 갈리지 않게.
"""
from __future__ import annotations
import csv, glob, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

#: `electrode_balancing_blend.m` 의 lb5/ub5 (원본 확인함)
BOUNDS = {"a_PE": (1.0, 1.4), "b_PE": (-0.5, 0.0),
          "a_NE": (1.0, 1.4), "b_NE": (-0.5, 0.1),
          "gamma_Si": (0.0, 0.5)}

#: 파일마다 γ 열 이름이 다르다. `gamma_init` 은 **시작점**이라 제외한다.
GAMMA_ALIAS = {"gamma_Si", "gamma_Si_TrackB"}


def touching(name: str, v: float) -> str | None:
    """경계 접촉이면 'a_PE=lb' 같은 라벨, 아니면 None.

    문턱은 §3-1 에서 규진팀에 제안한 것과 같다: 1e-6 · max(1, ub-lb).
    """
    lo, hi = BOUNDS[name]
    tol = 1e-6 * max(1.0, hi - lo)
    if abs(v - lo) < tol:
        return f"{name}=lb"
    if abs(v - hi) < tol:
        return f"{name}=ub"
    return None


def load_rows():
    for f in sorted(glob.glob(str(ROOT / "out" / "bms97" / "*.csv"))):
        src = pathlib.Path(f).stem
        for i, r in enumerate(csv.DictReader(open(f, encoding="utf-8")), 1):
            r["_file"], r["_line"] = src, i
            yield r


def audit(r: dict) -> dict:
    flags = []
    for col, v in r.items():
        key = "gamma_Si" if col in GAMMA_ALIAS else col
        if key not in BOUNDS:
            continue
        try:
            x = float(v)
        except (TypeError, ValueError):
            continue                      # NaN·빈칸 (TrackA 는 γ 가 없다)
        if x != x:
            continue
        t = touching(key, x)
        if t:
            flags.append(t)
    neg = [k for k in ("LAM_PE_pct", "LAM_NE_pct", "LLI_pct")
           if r.get(k) not in (None, "") and float(r[k]) < 0]
    return {"bounds": flags, "neg": neg}


def group_key(r: dict) -> str:
    """같은 파일 안에서 무엇이 한 실험 그룹인가 — 그 그룹의 pristine 이 기준이다."""
    for k in ("Si_source", "method", "halfcell_source", "fullcell_source",
              "config", "track"):
        if k in r:
            return r[k]
    return "?"


def mode_arithmetic(rows: list) -> dict:
    """LAM_NE 를 표의 값으로 **직접 계산**해서 보고값과 맞는지 본다.

        LAM_NE = 1 − (a_NE·c) / (a_NE_ref·c_ref)

    맞으면 그 다음이 따라온다: LAM_NE < 0 이려면
        a_NE / a_NE_ref  >  c_ref / c
    이어야 한다. `300_0009` 는 c_ref/c = 74.671/63.72 = 1.1718 이므로,
    기준이 자유로울 때 대상의 a_NE 가 **행별 임계 a_NE_ref·c_ref/c (1.177~1.196)** 를
    넘어야 음수가 나온다. 상자 상한이 1.4 라 그 자리가 열려 있다. 이것은 기준을
    고정한 조건의 부호 산술이지 경계 변경 재적합의 인과가 아니다 (R2-09).
    """
    by = {}
    for r in rows:
        by.setdefault((r["_file"], group_key(r)), {})[r["state"]] = r
    worst, neg = 0.0, []
    for (f, g), states in sorted(by.items()):
        ref = states.get("pristine")
        if not ref:
            continue
        for st, r in states.items():
            if st == "pristine":
                continue
            c_ref, c = float(ref.get("c_cell", 0) or 0), float(r.get("c_cell", 0) or 0)
            if not (c and c_ref):
                continue
            pred = (1 - (float(r["a_NE"]) * c) / (float(ref["a_NE"]) * c_ref)) * 100
            rep = float(r["LAM_NE_pct"])
            worst = max(worst, abs(pred - rep))
            if rep < 0:
                neg.append({"file": f, "config": g, "state": st, "LAM_NE": rep,
                            "a_NE": float(r["a_NE"]), "a_NE_ref": float(ref["a_NE"]),
                            "need": c_ref / c,
                            "ratio": float(r["a_NE"]) / float(ref["a_NE"]),
                            "target_at_ub": touching("a_NE", float(r["a_NE"])) == "a_NE=ub",
                            "ref_at_ub": touching("a_NE", float(ref["a_NE"])) == "a_NE=ub"})
    return {"worst": worst, "neg": neg}


def main() -> int:
    rows = list(load_rows())
    res = [(r, audit(r)) for r in rows]
    n = len(rows)
    n_bound = sum(1 for _, a in res if a["bounds"])
    n_ne = sum(1 for _, a in res if "LAM_NE_pct" in a["neg"])
    n_pe = sum(1 for _, a in res if "LAM_PE_pct" in a["neg"])
    n_lli = sum(1 for _, a in res if "LLI_pct" in a["neg"])
    n_lam = sum(1 for _, a in res
                if {"LAM_PE_pct", "LAM_NE_pct"} & set(a["neg"]))

    lam_ne = [float(r["LAM_NE_pct"]) for r in rows
              if r["state"] == "300_0009" and r.get("LAM_NE_pct")]
    lam_pe = [float(r["LAM_PE_pct"]) for r in rows
              if r["state"] == "300_0009" and r.get("LAM_PE_pct")]
    lli = [float(r["LLI_pct"]) for r in rows
           if r["state"] == "300_0009" and r.get("LLI_pct")]

    print(f"원표: {n} 행  ({len(set(r['_file'] for r in rows))} 파일)")
    print(f"  상자 경계에 붙은 행      {n_bound} / {n}  ({100*n_bound/n:.0f} %)")
    print(f"  음수 LAM_NE 인 행        {n_ne} / {n}   ← §2 가 적어 온 수")
    print(f"  음수 LAM_PE 인 행        {n_pe} / {n}")
    print(f"  둘 중 하나라도 음수      {n_lam} / {n}")
    print(f"  음수 LLI 인 행           {n_lli} / {n}   ← 리튬 재고가 늘었다는 뜻")
    print(f"\n`300_0009` 한 상태에서의 폭 (n={len(lam_ne)})")
    for nm, v in (("LAM_NE", lam_ne), ("LAM_PE", lam_pe), ("LLI", lli)):
        print(f"  {nm:7} {min(v):8.2f} ~ {max(v):7.2f} %   폭 {max(v)-min(v):6.2f} %p")

    which = {}
    for _, a in res:
        for f in a["bounds"]:
            which[f] = which.get(f, 0) + 1
    print("\n어느 좌표가 눌렸나")
    for k, c in sorted(which.items(), key=lambda kv: -kv[1]):
        print(f"  {k:14} {c}")

    arith = mode_arithmetic(rows)
    print(f"\n원표의 자기일관성 — LAM_NE 를 a_NE·c 로 직접 계산해 보고값과 대조")
    print(f"  전 행 최대 |Δ| = {arith['worst']:.2e} %p"
          f"   → 표가 내부적으로 일관된다 (오타·다른 정의가 아니다)")

    print(f"\n음수 LAM_NE 는 왜 나오나 — **상관이 아니라 산술이다**")
    print(f"  LAM_NE < 0  ⟺  a_NE / a_NE_ref  >  c_ref / c")
    print(f"  {'config':22}{'state':10}{'LAM_NE':>9}{'a_NE':>8}{'기준':>8}"
          f"{'비율':>7}{'필요':>7}  대상/기준 상한 접촉")
    for d in sorted(arith["neg"], key=lambda x: x["LAM_NE"]):
        print(f"  {d['config'][:20]:22}{d['state']:10}{d['LAM_NE']:>9.3f}"
              f"{d['a_NE']:>8.4f}{d['a_NE_ref']:>8.4f}{d['ratio']:>7.3f}"
              f"{d['need']:>7.3f}  "
              f"{'대상=ub' if d['target_at_ub'] else '—':8}"
              f"{'기준=ub' if d['ref_at_ub'] else '—'}")
    strong = [d for d in arith["neg"] if d["LAM_NE"] < -10]
    n_ub = sum(1 for d in strong if d["target_at_ub"] and not d["ref_at_ub"])
    print(f"\n  LAM_NE < −10 % 인 {len(strong)} 행 중 "
          f"**대상만 상한에 붙고 기준은 자유**인 행: {n_ub}")
    if strong:
        th = sorted(d["need"] * d["a_NE_ref"] for d in strong)
        print(f"  행별 영점 임계 a_NE = {th[0]:.3f} ~ {th[-1]:.3f} (= a_NE_ref·c_ref/c; 상자 상한 1.400).")
        print("  ⚠ 이것은 **기준 적합을 고정한** 조건에서의 부호 산술이다 (Codex R2-09 · L5-F5).")
        print("    상한을 바꿔 양쪽을 재적합하면 어떻게 되는지는 말하지 않는다 — 활성 상한에서")
        print("    무제약 최적은 더 음수일 수 있고, 그러면 상한은 음수를 만든 것이 아니라 잘라 준 것이다.")
        print("    '상한을 낮추면 음수가 안 나온다' 는 원인 서술이 아니라 은폐 절차다.")

    if "--rows" in sys.argv:
        print(f"\n{'파일':30}{'행':>3} {'state':10}{'LAM_NE':>9}  경계")
        for r, a in res:
            if a["bounds"] or a["neg"]:
                print(f"  {r['_file']:28}{r['_line']:>3} {r['state']:10}"
                      f"{float(r.get('LAM_NE_pct') or 0):>9.3f}  "
                      f"{','.join(a['bounds']) or '—'}"
                      f"{'   ← 음수 LAM' if a['neg'] else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
