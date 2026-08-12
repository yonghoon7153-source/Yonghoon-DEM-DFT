#!/usr/bin/env python3
"""vasp_cost_estimate.py — 외주 번들의 실행 비용을 **실측 기준으로** 추산한다 (stdlib).

왜 필요한가 (2026-08-12)
  v3 README 에 "슬랩 relax 잡당 64코어 기준 수 시간~하루" 라고 적었는데 **틀렸다**.
  근거는 손으로 잡은 감이었고, 정작 실측이 repo 안에 있었다:

    runs/sdcp_phaseB_vasp_v1_2026_08_08/slab/OUTCAR.gz
      192원자 · NKPTS 4 · NBANDS 900 · 48코어 · LREAL=Auto · ISMEAR=1 · EDIFF 1e-5
      → **단일점** SCF 58 전자스텝에 30,438 s (= 8.45 h, 스텝당 525 s)

  그건 단일점이다. v3 는 거기에 이완(수십 이온스텝) + 촘촘한 k + LREAL=.FALSE. 를
  얹었으므로 잡당 비용이 자릿수로 다르다. 감으로 적으면 외주 견적이 통째로 틀어진다.

  python3 tools/sdcp/vasp_cost_estimate.py                     # 기본 시나리오
  python3 tools/sdcp/vasp_cost_estimate.py --manifest <경로>    # 실제 번들에서 잡 수 회수
  python3 tools/sdcp/vasp_cost_estimate.py --concurrent 20     # 동시 실행 20잡 가정
  python3 tools/sdcp/vasp_cost_estimate.py --scenario lean     # 절감안 비교
  python3 tools/sdcp/vasp_cost_estimate.py --selftest

이 도구가 **못 하는 것**
  · 벤치마크가 아니다. 스케일링 **모형**이라 ±2배는 예상 범위다.
    확정하려면 대표 잡 하나를 4상 전부 돌려 실측하는 수밖에 없다 (--pilot 안내 참조).
  · 병렬 효율(코어를 늘렸을 때의 감쇠)을 모형에 안 넣었다 — 같은 코어 수 가정이다.
  · 이온스텝 수는 구조·시작점에 따라 크게 흔들린다. 여기서는 가정값이고
    **이 가정이 총비용을 지배한다** (n_ionic 을 바꿔 보면 바로 보인다).
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys

# ── 실측 기준선 (납품 Phase-B) ──────────────────────────────────────────────
BASE = {"atoms": 192, "nkpts": 4, "cores": 48, "sec_per_estep": 525.0,
        "source": "runs/sdcp_phaseB_vasp_v1_2026_08_08/slab/OUTCAR.gz "
                  "(30438 s / 58 전자스텝)"}

# ── 스케일링 인자 (전부 근사. 바꿔 보라고 밖에 꺼내 둔다) ────────────────────
F_ATOMS_EXP = 1.5      # 비용 ∝ N^exp — FFT/직교화 혼합이라 1.5 근처
F_LASPH = 1.08         # LASPH=.TRUE. (납품은 F)
F_ADDGRID = 1.15       # ADDGRID=.TRUE.
F_LREAL_FALSE = 2.5    # 실공간→역공간 투영 (static/dense)
F_SMEAR = 1.20         # ISMEAR 0/0.05 는 1/0.2 보다 전자스텝이 더 든다
#: 상별 전자스텝 수 가정. relax 는 (첫 스텝 + 이온스텝 × 스텝당)
ESTEP = {"pre": 60, "relax_first": 20, "relax_per_ionic": 10, "static": 75, "dense": 75}
N_IONIC = 60           # ⚠ 총비용을 지배하는 가정. 자유원자 수에 따라 30~100.
KMESH_N = {"2 3 1": 6, "3 4 1": 12, "4 6 1": 24, "1 1 1": 1}
TR_REDUCE = 0.6        # ISYM=0 이어도 시간반전으로 k 가 줄어드는 비율(근사)


def outcar_baseline(path):
    """납품 OUTCAR 에서 (원자수, NKPTS, 코어, 스텝당 초) 를 회수한다."""
    try:
        op = gzip.open if path.endswith(".gz") else open
        t = op(path, "rt", errors="ignore").read()
    except OSError:
        return None
    g = lambda p: (re.search(p, t) or [None, None])[1] if re.search(p, t) else None
    nat = g(r"NIONS\s*=\s*(\d+)")
    nk = g(r"NKPTS\s*=\s*(\d+)")
    cores = g(r"running on\s+(\d+)\s+total cores")
    el = g(r"Elapsed time \(sec\):\s*([\d.]+)")
    n_est = len(re.findall(r"Iteration\s+\d+\(", t))
    if not (nat and nk and el and n_est):
        return None
    return {"atoms": int(nat), "nkpts": int(nk),
            "cores": int(cores) if cores else BASE["cores"],
            "sec_per_estep": float(el) / n_est, "source": path}


def nk_eff(mesh):
    n = KMESH_N.get(str(mesh).strip())
    if n is None:
        try:
            n = 1
            for x in str(mesh).split():
                n *= int(x)
        except ValueError:
            n = 1
    return max(1.0, n * TR_REDUCE)


def phase_hours(ph, atoms, mesh, base, lreal_false, n_ionic=N_IONIC):
    """상 하나의 벽시계 시간 [h] (기준선과 같은 코어 수 가정)."""
    f = (atoms / base["atoms"]) ** F_ATOMS_EXP
    f *= nk_eff(mesh) / max(1.0, base["nkpts"])
    f *= F_LASPH * F_ADDGRID
    if lreal_false:
        f *= F_LREAL_FALSE
    sec_step = base["sec_per_estep"] * f
    if ph == "relax":
        n = ESTEP["relax_first"] + n_ionic * ESTEP["relax_per_ionic"]
    else:
        n = ESTEP[ph]
    return n * F_SMEAR * sec_step / 3600.0


#: 상별 k·전자스텝을 시나리오가 덮어쓸 수 있게 한다 (이완은 싸게, 평가는 정확하게)
SCENARIOS = {
    "delta": {"desc": "권장 — 이완은 싸게(2×2×1·EDIFF 1e-4·EDIFFG −0.05), 평가는 static. "
                      "수렴 검사는 대표 3잡만 (ΔE 에서 상쇄되므로)",
              "phases": ("relax", "static"), "dense_jobs": 3,
              "static_mesh": "3 4 1", "dense_mesh": "4 6 1", "lreal_false": False,
              "relax_mesh": "2 2 1", "relax_estep": 7, "n_ionic": 35, "n_slab": 74},
    "v3": {"desc": "현행 v3 — pre/relax/static(LREAL=F)/dense, dense=tier1 전 pm1",
           "phases": ("pre", "relax", "static"), "dense_jobs": 20,
           "static_mesh": "3 4 1", "dense_mesh": "4 6 1", "lreal_false": True,
           "n_ionic": N_IONIC, "n_slab": 74},
    "lean": {"desc": "절감안 — static 도 LREAL=Auto · static k 2×3×1 · dense 는 탐침만",
             "phases": ("pre", "relax", "static"), "dense_jobs": 4,
             "static_mesh": "2 3 1", "dense_mesh": "3 4 1", "lreal_false": False,
             "n_ionic": N_IONIC, "n_slab": 74},
    "sp": {"desc": "단일점안 — 이완 없이 UMA 기하에 static 만 (납품 Phase-B 방식)",
           "phases": ("static",), "dense_jobs": 4,
           "static_mesh": "3 4 1", "dense_mesh": "4 6 1", "lreal_false": True,
           "n_ionic": 0, "n_slab": 74},
    "champion": {"desc": "Wave 1 (현행) — 조각당 챔피언 1쌍 · 단일점 · dense 는 보정자 조각만 "
                         "· clean 자기 대조군 2 · 기체 기준계 없음",
                 "phases": ("static",), "dense_jobs": 4,
                 "static_mesh": "2 3 1", "dense_mesh": "3 4 1", "lreal_false": False,
                 "n_ionic": 0, "n_slab": 22},
    "tier1": {"desc": "tier1 만 — PTFE 8쌍 + refs (SDCP 는 다음 판으로)",
              "phases": ("pre", "relax", "static"), "dense_jobs": 16,
              "static_mesh": "3 4 1", "dense_mesh": "4 6 1", "lreal_false": True,
              "n_ionic": N_IONIC, "n_slab": 34},
}


def schedule_makespan(job_hours, m):
    """LPT 리스트 스케줄링으로 makespan [h] 을 낸다.

    ★ 왜 "총시간 ÷ 동시실행" 이 아닌가 (Codex 6차 §7)
      한 잡 안의 상(static→dense)은 **직렬**이다 — dense 가 static 의 CHGCAR 를
      승계하므로 쪼갤 수 없다. 그래서 잡 하나는 '분할 불가 작업 하나' 이고,
      전체는 고전적인 P||Cmax 문제가 된다. 산술 하한(총÷m)은 **도달 불가능한**
      경우가 흔하다: 가장 긴 잡보다 짧아질 수 없기 때문이다.
    """
    m = max(1, int(m))
    free = [0.0] * m
    for h in sorted(job_hours, reverse=True):      # LPT — 긴 것부터
        i = min(range(m), key=lambda k: free[k])
        free[i] += h
    return max(free) if free else 0.0


def manifest_jobs(path, base, atoms_fallback):
    """MANIFEST.json(+같은 폴더의 job.json)에서 **실제 계획**을 회수한다.

    반환 [(상대경로, 총시간h, {상: h})]. job.json 이 있으면 원자수·k·LREAL 을
    잡마다 정확히 읽고, 없으면 planned 의 상 목록 + --atoms 가정으로 후퇴한다
    (그때는 후퇴했다고 **말한다** — 조용히 가정하지 않는다).
    """
    from glob import glob
    with open(path) as fh:
        man = json.load(fh)
    root = os.path.dirname(os.path.abspath(path))
    jps = sorted(glob(os.path.join(root, "*", "*", "job.json")))
    out, mode = [], "job.json (정확)"
    if jps:
        for jp in jps:
            with open(jp) as fh:
                meta = json.load(fh)
            # ⚠ 기체 기준계 잡에는 magmom_poscar 가 없다(슬랩 전용 필드). 그러면
            #   조용히 atoms_fallback(=222)로 후퇴해 **분자를 슬랩처럼 계상**한다.
            #   2026-08-12: 기체 8잡이 96 h 로 잡혀 총액이 570 → 714 h 로 부풀었다.
            n_at = (len(meta.get("magmom_poscar") or [])
                    or sum((meta.get("counts") or {}).values())
                    or len(meta.get("species_order") or [])
                    or atoms_fallback)
            km = meta.get("kmesh") or {}
            inc = meta.get("incar_expected") or {}
            ph_h = {}
            for ph in meta.get("phases") or []:
                lr = str((inc.get(ph) or {}).get("LREAL", ".TRUE.")).upper()
                # ⚠ 이온스텝 수는 계 크기에 크게 의존한다. 기체 분자(수십 원자)를
                #   슬랩과 같은 60 스텝으로 잡으면 과대계상된다.
                _ni = N_IONIC if n_at > 60 else 25
                ph_h[ph] = phase_hours(
                    ph if ph in ESTEP else "static", n_at,
                    km.get(ph, "3 4 1"), base,
                    lr.startswith(".F"), _ni)
            out.append((os.path.relpath(os.path.dirname(jp), root),
                        sum(ph_h.values()), ph_h))
    else:
        mode = f"planned 만 (원자수 {atoms_fallback} **가정**)"
        for rel, p in (man.get("planned") or {}).items():
            ph_h = {ph: phase_hours(ph if ph in ESTEP else "static", atoms_fallback,
                                    "3 4 1", base, True, N_IONIC)
                    for ph in (p.get("phases") or [])}
            out.append((rel, sum(ph_h.values()), ph_h))
    return man, out, mode


def estimate(sc, atoms, base, concurrent):
    ph_h = {}
    for ph in sc["phases"]:
        mesh = {"pre": "2 3 1", "relax": sc.get("relax_mesh", "2 3 1"),
                "static": sc["static_mesh"]}[ph]
        old = ESTEP["relax_per_ionic"]
        ESTEP["relax_per_ionic"] = sc.get("relax_estep", old)
        ph_h[ph] = phase_hours(ph, atoms, mesh, base,
                               sc["lreal_false"] and ph in ("static", "dense"),
                               sc["n_ionic"])
        ESTEP["relax_per_ionic"] = old
    d_h = phase_hours("dense", atoms, sc["dense_mesh"], base, sc["lreal_false"])
    per_job = sum(ph_h.values())
    total = per_job * sc["n_slab"] + d_h * sc["dense_jobs"]
    return {"per_phase_h": ph_h, "dense_h": d_h, "per_job_h": per_job,
            "total_h": total, "core_h": total * base["cores"],
            "wall_days": total / max(1, concurrent) / 24.0}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outcar", default="runs/sdcp_phaseB_vasp_v1_2026_08_08/slab/OUTCAR.gz")
    ap.add_argument("--atoms", type=int, default=222, help="자세 잡 원자수 (슬랩 192 + 조각)")
    ap.add_argument("--concurrent", type=int, default=8, help="외주처 동시 실행 잡 수")
    ap.add_argument("--n_ionic", type=int, default=None,
                    help="이온스텝 수를 전 시나리오에 강제 (기본: 시나리오별 값)")
    ap.add_argument("--scenario", default="all")
    ap.add_argument("--manifest", default=None,
                    help="번들 MANIFEST.json — **실제 계획**에서 비용을 낸다 "
                         "(같은 폴더의 job.json 이 있으면 원자수·k·LREAL 을 잡마다 정확히 읽음)")
    ap.add_argument("--cores", type=int, default=None,
                    help="잡당 코어 수 (기본: 기준선과 동일). README 예시가 64 면 여기도 64.")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    base = outcar_baseline(a.outcar) or dict(BASE)
    if a.manifest:
        return report_manifest(a, base)
    print(f"기준선: {base['atoms']}원자 · NKPTS {base['nkpts']} · {base['cores']}코어 · "
          f"전자스텝당 {base['sec_per_estep']:.0f} s")
    print(f"  출처 {base['source']}")
    print(f"가정: 자세 {a.atoms}원자 · 이온스텝 "
          + (f"{a.n_ionic} (강제)" if a.n_ionic is not None else "시나리오별")
          + f" · 동시 {a.concurrent}잡 (코어 수는 기준선과 동일)\n")
    names = list(SCENARIOS) if a.scenario == "all" else [a.scenario]
    print(f"{'시나리오':8s} {'잡당(h)':>9s} {'총 벽시계(h)':>12s} {'코어시간':>12s} "
          f"{'동시%d잡 일수' % a.concurrent:>14s}")
    rows = {}
    for n in names:
        sc = dict(SCENARIOS[n])
        if a.n_ionic is not None:
            sc["n_ionic"] = a.n_ionic
        r = estimate(sc, a.atoms, base, a.concurrent)
        rows[n] = r
        print(f"{n:8s} {r['per_job_h']:9.0f} {r['total_h']:12.0f} "
              f"{r['core_h']:12.0f} {r['wall_days']:13.1f}일")
    print()
    for n in names:
        sc = SCENARIOS[n]
        print(f"  {n:8s} {sc['desc']}")
        if n in rows:
            ph = "  ".join(f"{k} {v:.0f}h" for k, v in rows[n]["per_phase_h"].items())
            print(f"           상별 {ph}  · dense {rows[n]['dense_h']:.0f}h "
                  f"× {sc['dense_jobs']}잡")
    print("\n⚠ 이건 모형이다 — ±2배는 예상 범위다. 총비용을 지배하는 건 **이온스텝 수**다:")
    for ni in (20, 60, 100):
        sc = dict(SCENARIOS["v3"]); sc["n_ionic"] = ni
        print(f"     이온스텝 {ni:3d} → v3 잡당 "
              f"{estimate(sc, a.atoms, base, a.concurrent)['per_job_h']:.0f} h")
    print("\n★ 확정하는 법 — 대표 잡 **하나**를 4상 전부 돌려 실측한 뒤 곱한다:")
    print("     tier1/ptfe_c10__fib00_r090__Litop__afm2424_pm1 (탐침·dense 포함)")
    print("     외주처에 이 잡만 먼저 돌려 상별 Elapsed time 을 달라고 하면 된다.")
    return 0


def report_manifest(a, base) -> int:
    """실제 번들 계획 기반 보고 — 산술 하한과 **스케줄링 makespan** 을 같이 낸다."""
    if not os.path.isfile(a.manifest):
        print(f"⛔ MANIFEST 가 없다: {a.manifest}")
        return 2
    man, jobs, mode = manifest_jobs(a.manifest, base, a.atoms)
    if not jobs:
        print(f"⛔ {a.manifest} 에 계획된 잡이 0개 — 비용을 낼 수 없다")
        return 2
    cores = a.cores or base["cores"]
    hs = [h for _r, h, _p in jobs]
    total = sum(hs)
    lo = max(total / max(1, a.concurrent), max(hs))     # 도달 가능한 하한
    mk = schedule_makespan(hs, a.concurrent)            # LPT 근사
    n_ph = sum(len(p) for _r, _h, p in jobs)
    by_ph: dict = {}
    for _r, _h, p in jobs:
        for k, v in p.items():
            by_ph[k] = by_ph.get(k, 0.0) + v
    print(f"기준선: {base['atoms']}원자 · NKPTS {base['nkpts']} · {base['cores']}코어 · "
          f"전자스텝당 {base['sec_per_estep']:.0f} s")
    print(f"  출처 {base['source']}")
    print(f"MANIFEST: {a.manifest}")
    print(f"  회수 방식 {mode} · 잡 {len(jobs)} · VASP 실행 {n_ph}회 · "
          f"모드 {man.get('contract_mode', '(기본)')} · wave {man.get('wave', '?')}")
    print(f"  dense 보정자 {man.get('dense_calibrators') or '(없음)'}")
    print()
    print(f"  상별 합계   " + "  ".join(f"{k} {v:.0f}h" for k, v in sorted(by_ph.items())))
    print(f"  총 벽시계   {total:.0f} h        (모든 상을 한 줄로 세운 값)")
    print(f"  코어시간    {total * cores:.0f}  ({cores} 코어/잡 가정)")
    print(f"  가장 긴 잡  {max(hs):.1f} h      ← **이보다 짧아질 수 없다** (상이 직렬)")
    print(f"  산술 하한   {total / max(1, a.concurrent) / 24:.2f} 일  "
          f"(총 ÷ 동시 {a.concurrent})")
    print(f"  도달 하한   {lo / 24:.2f} 일  (max(산술하한, 가장 긴 잡))")
    print(f"  ★ 추정      {mk / 24:.2f} 일  (LPT 스케줄링 · 동시 {a.concurrent}잡)")
    if mk > total / max(1, a.concurrent) * 1.05:
        print(f"     ⚠ 산술 하한보다 {mk / (total / max(1, a.concurrent)):.2f}배 — "
              f"잡 길이가 고르지 않아 하한에 도달하지 못한다")
    print()
    print("  동시 실행별:")
    for m in (4, 8, 12, 20, 40):
        print(f"     {m:3d}잡 → {schedule_makespan(hs, m) / 24:5.2f} 일"
              + ("   (여기부터는 가장 긴 잡이 지배)"
                 if schedule_makespan(hs, m) <= max(hs) * 1.001 else ""))
    print("\n  가장 비싼 잡 5개:")
    for rel, h, p in sorted(jobs, key=lambda t: -t[1])[:5]:
        print(f"     {h:6.1f} h  {rel}  "
              + " ".join(f"{k}:{v:.0f}" for k, v in sorted(p.items())))
    print("\n⚠ 이건 모형이다 — **±2배는 예상 범위**다. 계약값이 아니라 계획용 수치다.")
    print("   확정하려면 대표 잡 하나를 전 상 돌려 실측한 뒤 곱한다.")
    return 0


def selftest() -> int:
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok &= bool(c)

    b = dict(BASE)
    # 양성: 기준선과 같은 조건이면 단일점 시간이 재현돼야 한다
    h = phase_hours("static", b["atoms"], "2 3 1", b, False)
    ref = ESTEP["static"] * F_SMEAR * b["sec_per_estep"] / 3600.0 * \
        (nk_eff("2 3 1") / b["nkpts"]) * F_LASPH * F_ADDGRID
    chk(abs(h - ref) < 1e-6, f"기준 조건 재현 {h:.1f} h")
    # 단조성: 원자·k·이온스텝이 늘면 비용도 는다
    chk(phase_hours("static", 300, "2 3 1", b, False) > h, "원자 늘면 비용 증가")
    chk(phase_hours("static", 192, "4 6 1", b, False) > h, "k 늘면 비용 증가")
    chk(phase_hours("static", 192, "2 3 1", b, True) > h, "LREAL=F 면 비용 증가")
    chk(phase_hours("relax", 192, "2 3 1", b, False, 100)
        > phase_hours("relax", 192, "2 3 1", b, False, 20), "이온스텝 늘면 비용 증가")
    # 음성: 단일점안은 이완이 없으므로 v3 보다 **반드시** 싸야 한다
    e3 = estimate(dict(SCENARIOS["v3"]), 222, b, 8)
    es = estimate(dict(SCENARIOS["sp"]), 222, b, 8)
    chk(es["total_h"] < e3["total_h"] * 0.5,
        f"단일점안이 v3 의 절반 미만 ({es['total_h']:.0f} vs {e3['total_h']:.0f} h)")
    el = estimate(dict(SCENARIOS["lean"]), 222, b, 8)
    chk(el["total_h"] < e3["total_h"], f"절감안이 v3 보다 쌈 ({el['total_h']:.0f} h)")
    t1 = estimate(dict(SCENARIOS["tier1"]), 222, b, 8)
    chk(t1["total_h"] < e3["total_h"], f"tier1 만이 더 쌈 ({t1['total_h']:.0f} h)")
    ed = estimate(dict(SCENARIOS["delta"]), 222, b, 8)
    chk(ed["total_h"] < e3["total_h"] * 0.35,
        f"권장안이 v3 의 1/3 미만 ({ed['total_h']:.0f} vs {e3['total_h']:.0f} h)")
    # ⚠ "권장안 > 단일점" 은 **성립하지 않는다** — 단일점안은 이완이 없는 대신 static 을
    #   LREAL=.FALSE. + 촘촘한 k 로 잡는다. 즉 비싼 건 이완이 아니라 static 설정이다.
    #   비교는 **같은 조건에서 이완만 켜고 끄는** 것으로 해야 의미가 있다.
    d0 = dict(SCENARIOS["delta"]); d0["phases"] = ("static",); d0["n_ionic"] = 0
    chk(estimate(d0, 222, b, 8)["total_h"] < ed["total_h"],
        "같은 조건에서 이완을 켜면 비싸진다 (조건을 섞어 비교하지 않는다)")
    chk(es["total_h"] > estimate(d0, 222, b, 8)["total_h"],
        f"단일점안이 권장안의 static 보다 비싸다 — LREAL=F·촘촘한 k 때문 "
        f"({es['total_h']:.0f} vs {estimate(d0, 222, b, 8)['total_h']:.0f} h)")
    # 음성: 동시 실행이 늘면 일수는 줄되 코어시간은 안 변한다
    a1 = estimate(dict(SCENARIOS["v3"]), 222, b, 1)
    a8 = estimate(dict(SCENARIOS["v3"]), 222, b, 8)
    chk(abs(a1["core_h"] - a8["core_h"]) < 1e-6 and a8["wall_days"] < a1["wall_days"],
        "동시 실행은 일수만 줄인다 (코어시간 불변)")
    # 음성: OUTCAR 가 없으면 조용히 0 을 내면 안 된다
    chk(outcar_baseline("/nonexistent/OUTCAR") is None, "없는 OUTCAR → None (기본값 후퇴)")
    chk(outcar_baseline(__file__) is None, "OUTCAR 아닌 파일 → None")

    # ── 스케줄링 (Codex 6차 §7) ─────────────────────────────────────────────
    chk(abs(schedule_makespan([10.0] * 8, 8) - 10.0) < 1e-9, "고른 8잡/8슬롯 → 10 h")
    chk(abs(schedule_makespan([10.0] * 8, 4) - 20.0) < 1e-9, "고른 8잡/4슬롯 → 20 h")
    # ★ 음성: **산술 하한은 도달 불가능할 수 있다** — 이게 이 함수를 만든 이유다.
    #   긴 잡 하나 + 짧은 잡 여럿이면 총÷m 보다 반드시 길어진다.
    uneven = [100.0] + [1.0] * 20
    lb = sum(uneven) / 8
    chk(schedule_makespan(uneven, 8) > lb * 1.5,
        f"불균등 부하 → 산술 하한 {lb:.0f} h 도달 불가 "
        f"(실제 {schedule_makespan(uneven, 8):.0f} h — 가장 긴 잡이 지배)")
    chk(schedule_makespan(uneven, 1000) >= max(uneven) - 1e-9,
        "슬롯이 아무리 많아도 **가장 긴 잡보다 짧아질 수 없다**")
    chk(schedule_makespan([], 8) == 0.0, "잡 0개 → 0 h (예외 아님)")

    # ── --manifest 회수 (있다고 광고만 하고 없던 기능) ────────────────────────
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        jd = os.path.join(td, "tier1", "j1")
        os.makedirs(jd)
        with open(os.path.join(jd, "job.json"), "w") as fh:
            json.dump({"phases": ["static", "dense"],
                       "magmom_poscar": [0.0] * 222,
                       "kmesh": {"static": "2 3 1", "dense": "3 4 1"},
                       "incar_expected": {"static": {"LREAL": "Auto"},
                                          "dense": {"LREAL": "Auto"}}}, fh)
        mp = os.path.join(td, "MANIFEST.json")
        with open(mp, "w") as fh:
            json.dump({"planned": {"tier1/j1": {"phases": ["static", "dense"]}},
                       "contract_mode": "champion"}, fh)
        _man, jl, mode = manifest_jobs(mp, b, 222)
        chk(len(jl) == 1 and "job.json" in mode, f"MANIFEST → 잡 1개 회수 ({mode})")
        chk(set(jl[0][2]) == {"static", "dense"}, f"상 2개 회수 {sorted(jl[0][2])}")
        chk(jl[0][2]["dense"] > jl[0][2]["static"],
            "dense 가 static 보다 비싸다 (k 가 촘촘하다)")
        # ★ 음성: 기체 잡(magmom_poscar 없음)을 **슬랩으로 계상하지 않는지**
        #   2026-08-12: 이것 때문에 기체 8잡이 96 h 로 잡혀 총액이 25% 부풀었다.
        gd = os.path.join(td, "refs", "mol__x")
        os.makedirs(gd, exist_ok=True)
        with open(os.path.join(gd, "job.json"), "w") as fh:
            json.dump({"phases": ["relax", "static"], "counts": {"C": 2, "F": 4},
                       "kmesh": {"relax": "1 1 1", "static": "1 1 1"},
                       "incar_expected": {"relax": {"LREAL": "Auto"},
                                          "static": {"LREAL": ".FALSE."}}}, fh)
        with open(mp, "w") as fh:
            json.dump({"planned": {"tier1/j1": {"phases": ["static", "dense"]},
                                   "refs/mol__x": {"phases": ["relax", "static"]}}}, fh)
        _m3, jl3, _md3 = manifest_jobs(mp, b, 222)
        _gas = [x for x in jl3 if "mol__" in x[0]][0]
        chk(_gas[1] < 1.0,
            f"기체 6원자 잡이 1 h 미만 ({_gas[1]:.2f} h) — 슬랩(222원자)으로 안 센다")
        os.remove(os.path.join(gd, "job.json"))
        # ★ 음성: job.json 이 없으면 **후퇴했다고 말해야** 한다 (조용한 가정 금지)
        os.remove(os.path.join(jd, "job.json"))
        _m2, jl2, mode2 = manifest_jobs(mp, b, 222)
        chk(len(jl2) == len(json.load(open(mp))["planned"]) and "가정" in mode2,
            f"job.json 없음 → planned 후퇴를 **명시** ({mode2}, {len(jl2)}잡)")
        # ★ 음성: 없는 MANIFEST 는 0 이 아니라 exit 2
        class _A:
            manifest, atoms, concurrent, cores = "/nonexistent/MANIFEST.json", 222, 8, None
        chk(report_manifest(_A(), b) == 2, "없는 MANIFEST → exit 2 (조용한 0 아님)")
        with open(mp, "w") as fh:
            json.dump({"planned": {}}, fh)
        class _B:
            manifest, atoms, concurrent, cores = mp, 222, 8, None
        chk(report_manifest(_B(), b) == 2, "계획 0잡 → exit 2 (0 h 를 내지 않는다)")
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
