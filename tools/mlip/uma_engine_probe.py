#!/usr/bin/env python3
"""uma_engine_probe.py — MLIP **엔진 자체**를 잰다 (화학 없음, DFT 0회).

왜 (2026-08-19). `bench_against_dft.py` 로 UMA 힘 오차를 재고 나니
(Li₃PS₄ 30.0 meV/Å — `kb/results/uma_force_accuracy_li3ps4_2026_08_19.md`)
**힘의 크기가 아니라 힘의 성질**을 묻는 질문 셋이 남았다. 셋 다 새 DFT 가 필요 없다:

  ① `--conservative`  힘이 에너지의 gradient 인가?
       PET-MAD `Fig. S5`: **비보존(직접힘) 모델만** LBFGS 가 9–11 % 미수렴했다.
       `Fig. S16/S17`: 비보존이면 종별 온도가 갈라지고(Cl>2000 K) MSD 가 자릿수로 부푼다.
       우리 fmax 0.05 미수렴·D 과대 의심이 같은 증상이라 **먼저 이것부터 봐야 한다.**
  ② `--timing`        셀을 키우면 벽시계가 정말 비례해 늘어나나?
       PET-MAD `Fig. 3` 좌단: 30–60 원자 구간은 **원자당 비용이 아니라 스텝당 고정
       오버헤드가 지배**한다. 우리 52원자 셀이 GPU 를 놀리고 있을 수 있다.
  ③ `--against`       DFT 로 이완된 구조에서 MLIP 힘이 0 인가?
       DFT 최소점은 MLIP 도 최소점이어야 한다. 잔여력이 크면 **그 계에서 두 PES 가 다르다** —
       라벨 한 줄 없이도 불일치를 잡는다. **Li₃P(= Li₃N 과 같은 Li-rich 프닉타이드,
       UMA Li₃N 사용금지 2026-06) 검증의 무료 1단계.**

이 도구가 **못 하는 것**
  · **장벽을 안 잰다.** ①②③ 전부 통과해도 NEB 장벽이 맞는다는 보장은 없다.
  · **③ 은 참조 구조가 있어야 한다.** 없으면 못 돈다 (rattle 해서 QE 를 새로 돌리는 건
    이 도구 밖의 일 — 그건 `bench_against_dft.py` 의 영역이다).
  · **① 은 "비보존"을 증명하지 못한다.** 유한차분과 해석힘이 갈리면 원인이
    비보존일 수도, 에너지가 수치적으로 시끄러운 것일 수도 있다 → 그래서 δ 를 2개 쓴다.
    두 δ 에서 **같은 크기로** 갈리면 비보존, δ 를 줄일 때 커지면 잡음이다.
  · 응력을 안 본다.

  python3 tools/mlip/uma_engine_probe.py --selftest
  python3 tools/mlip/uma_engine_probe.py --conservative --struct <구조.xyz>
  python3 tools/mlip/uma_engine_probe.py --timing --struct <구조.xyz> --reps 1 2
  python3 tools/mlip/uma_engine_probe.py --against <dft_relaxed.xyz>
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "db" / "properties"

QE_BINS = ("pw.x", "neb.x", "cp.x", "ph.x")
# 유한차분 δ 2개 — 하나로는 "갈렸다"의 원인(비보존 vs 잡음)을 못 가른다.
DELTAS_A = (1e-3, 5e-3)
# 판정선. 상대편차 = |F_analytic − F_finitediff| / max(|F|, F_FLOOR)
CONS_WARN = 0.02      # 2 % 넘게 갈리면 경고
CONS_FAIL = 0.10      # 10 % 넘으면 비보존 의심 (δ 둘 다에서 나야 한다)
F_FLOOR_EVA = 0.05    # 힘이 이보다 작은 성분은 상대오차가 의미 없다 → 분모 바닥


def running_qe():
    """지금 QE 가 돌고 있나 (GPU 공유 사고 방지)."""
    busy = []
    for b in QE_BINS:
        try:
            if subprocess.run(["pgrep", "-x", b], capture_output=True).returncode == 0:
                busy.append(b)
        except OSError:
            pass
    return busy


def guard_gpu(allow_share=False):
    busy = running_qe()
    if not busy:
        return
    if allow_share:
        print(f"⚠ QE 가 돌고 있다: {', '.join(busy)} — 공유 실행(--allow_gpu_share)")
        return
    raise SystemExit(
        f"⛔ {', '.join(busy)} 가 돌고 있다. VRAM 이 겹치면 둘 다 죽는다.\n"
        f"   같이 돌리려면 --allow_gpu_share 를 줄 것.")


# ───────────────────────── ① 보존성 ─────────────────────────

def conservativeness(atoms, calc, n_atoms_probe=4, deltas=DELTAS_A, rng=None):
    """유한차분 힘 vs 해석 힘.

    돌려주는 값: {delta: {'rel_max','rel_mean','pairs':[(F_ana,F_fd),…]}}

    ⚠ 이 함수는 **원자 몇 개만** 본다 (전 원자는 6N 번의 에너지 계산이라 비싸다).
      그래서 "통과"는 *표본이 통과*라는 뜻이지 전 원자 보증이 아니다.
    """
    rng = rng or np.random.default_rng(0)
    a = atoms.copy()
    a.calc = calc
    F0 = np.asarray(a.get_forces(), float)
    n = len(a)
    idx = rng.choice(n, size=min(n_atoms_probe, n), replace=False)
    out = {}
    for d in deltas:
        pairs, rels = [], []
        for i in idx:
            for ax in range(3):
                p = a.get_positions()
                p[i, ax] += d
                a.set_positions(p)
                ep = a.get_potential_energy()
                p[i, ax] -= 2 * d
                a.set_positions(p)
                em = a.get_potential_energy()
                p[i, ax] += d
                a.set_positions(p)
                f_fd = -(ep - em) / (2 * d)
                f_an = F0[i, ax]
                pairs.append((float(f_an), float(f_fd)))
                rels.append(abs(f_an - f_fd) / max(abs(f_an), F_FLOOR_EVA))
        out[d] = {"rel_max": float(np.max(rels)), "rel_mean": float(np.mean(rels)),
                  "n_components": len(rels), "pairs": pairs}
    return out


def conservativeness_verdict(res):
    """δ 2개를 같이 보고 판정한다.

    · 둘 다 FAIL 이상, 그리고 δ 를 키워도 편차가 안 줄면 → **비보존 의심**
    · 작은 δ 에서만 크면 → **에너지 잡음**(비보존 아님)
    · 둘 다 WARN 아래 → 보존적으로 행동한다
    """
    ds = sorted(res)
    small, large = res[ds[0]], res[ds[-1]]
    s, l = small["rel_mean"], large["rel_mean"]
    if s < CONS_WARN and l < CONS_WARN:
        return "conservative", "⭕ 보존적 — 유한차분과 해석힘이 일치한다"
    if s >= CONS_FAIL and l >= CONS_FAIL:
        return "non_conservative_suspect", (
            "⛔ **비보존 의심** — δ 를 키워도 편차가 남는다. "
            "PET-MAD Fig. S5/S16/S17 의 증상(기하최적화 미수렴·종별 온도 분리·MSD 과대)을 "
            "우리 계에서도 의심해야 한다")
    if s > l * 2:
        return "energy_noise", (
            "⚠ 작은 δ 에서만 갈린다 → **에너지 수치잡음**이지 비보존이 아니다. "
            "δ 를 키워 다시 볼 것")
    return "borderline", "⚠ 경계 — 표본을 늘려(--probe_atoms) 다시 볼 것"


# ───────────────────────── ② 타이밍 ─────────────────────────

def timing(atoms, calc, reps=(1, 2), n_steps=20, warmup=3):
    """셀 크기별 µs/atom·step. 원자당 비용이 평평하면 오버헤드 지배 구간이다."""
    rows = []
    for r in reps:
        a = (atoms * (r, r, r)).copy()
        a.calc = calc
        for _ in range(warmup):                 # 컴파일·캐시 워밍업은 재지 않는다
            a.get_forces()
        t0 = time.time()
        for _ in range(n_steps):
            a.set_positions(a.get_positions() + 1e-4)   # 캐시 무효화
            a.get_forces()
        dt = time.time() - t0
        rows.append({"rep": r, "n_atoms": len(a),
                     "s_per_step": dt / n_steps,
                     "us_per_atom_step": dt / n_steps / len(a) * 1e6})
    return rows


def timing_verdict(rows):
    """가장 작은 셀 대비 원자당 비용이 얼마나 떨어지나."""
    if len(rows) < 2:
        return "n/a", "셀이 하나뿐 — 비교 불가"
    a, b = rows[0], rows[-1]
    drop = a["us_per_atom_step"] / max(b["us_per_atom_step"], 1e-12)
    grow = b["s_per_step"] / max(a["s_per_step"], 1e-12)
    natoms = b["n_atoms"] / a["n_atoms"]
    msg = (f"원자 {natoms:.0f}배 → 스텝당 벽시계 {grow:.1f}배 "
           f"(원자당 비용 {drop:.1f}배 싸짐)")
    if drop >= 1.5:
        return "overhead_bound", ("⭕ " + msg + " ⇒ **작은 셀은 오버헤드 지배**. "
                                  "셀을 키우면 통계가 거의 공짜로 늘어난다")
    return "compute_bound", ("⚠ " + msg + " ⇒ 이미 연산 지배. 셀을 키우면 그만큼 비싸진다")


# ───────────────────────── ③ DFT 최소점 잔여력 ─────────────────────────

def residual_at_reference(atoms, calc):
    """DFT 로 이완된 구조에서 MLIP 이 느끼는 힘. 작을수록 두 PES 가 같은 최소점을 본다."""
    a = atoms.copy()
    a.calc = calc
    F = np.asarray(a.get_forces(), float)
    mag = np.linalg.norm(F, axis=1)
    per_el = {}
    for el in sorted(set(a.get_chemical_symbols())):
        m = np.array([s == el for s in a.get_chemical_symbols()])
        per_el[el] = {"fmax": float(mag[m].max()), "frms": float(np.sqrt((mag[m] ** 2).mean())),
                      "n": int(m.sum())}
    return {"n_atoms": len(a), "fmax_eV_per_A": float(mag.max()),
            "frms_eV_per_A": float(np.sqrt((mag ** 2).mean())), "per_element": per_el}


def residual_verdict(r):
    fmax = r["fmax_eV_per_A"]
    if fmax < 0.05:
        return "agrees", "⭕ DFT 최소점에서 MLIP 힘이 거의 0 — 두 PES 가 같은 자리를 본다"
    if fmax < 0.15:
        return "mild", "⚠ 잔여력이 보인다 — 유사퍼텐셜/범함수 차이 수준일 수 있다"
    return "disagrees", ("⛔ **DFT 최소점이 MLIP 최소점이 아니다.** 이 계에서 두 PES 가 "
                         "다르다 — 구조·에너지 인용 전에 이유를 밝혀야 한다")


# ───────────────────────── 계산기 ─────────────────────────

def load_calc(model, task, device):
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit(model, device=device)
    return FAIRChemCalculator(predictor, task_name=task)


def read_struct(path):
    from ase.io import read
    p = Path(path).expanduser()
    if not p.exists():
        raise SystemExit(f"⛔ 구조 파일이 없다: {p}")
    return read(str(p))


# ───────────────────────── selftest ─────────────────────────

def selftest():
    """양성 + **음성** 경로. 음성이 핵심이다 — 비보존을 통과로 읽으면 이 도구는 무용지물이다."""
    from ase.build import bulk
    from ase.calculators.emt import EMT
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        print(("  ⭕ " if cond else "  ⛔ ") + name)
        ok, fail = ok + bool(cond), fail + (not cond)

    a = bulk("Cu", "fcc", a=3.6, cubic=True) * (2, 2, 2)
    rng = np.random.default_rng(1)
    a.set_positions(a.get_positions() + rng.normal(0, 0.08, a.get_positions().shape))

    # ── 양성: EMT 는 보존적이다 (해석힘 = −dE/dx)
    res = conservativeness(a, EMT(), n_atoms_probe=3, rng=np.random.default_rng(0))
    v, _ = conservativeness_verdict(res)
    chk(f"[양성] EMT 는 보존적으로 판정된다 (rel_mean {res[DELTAS_A[0]]['rel_mean']:.2e})",
        v == "conservative")

    # ── 음성 ①: 힘에 회전항(curl≠0)을 섞으면 **반드시** 잡혀야 한다
    class NonConservative(EMT):
        """F ← F + c·(z, x, y). 어떤 스칼라의 gradient 도 아니다 (curl ≠ 0)."""
        def calculate(self, atoms=None, properties=None, system_changes=None):
            super().calculate(atoms, properties, system_changes)
            p = atoms.get_positions()
            self.results["forces"] = self.results["forces"] + 0.5 * p[:, [2, 0, 1]]

    res_nc = conservativeness(a, NonConservative(), n_atoms_probe=3,
                              rng=np.random.default_rng(0))
    v_nc, _ = conservativeness_verdict(res_nc)
    chk(f"[음성①] 비보존 힘이 잡힌다 (판정 '{v_nc}')", v_nc == "non_conservative_suspect")
    chk("[음성①] 비보존 편차가 보존 대비 훨씬 크다",
        res_nc[DELTAS_A[0]]["rel_mean"] > 20 * res[DELTAS_A[0]]["rel_mean"])

    # ── 음성 ②: 상수 힘 오프셋은 **회전이 없어도** gradient 가 아니다 → 잡혀야 한다
    class ShiftedForce(EMT):
        def calculate(self, atoms=None, properties=None, system_changes=None):
            super().calculate(atoms, properties, system_changes)
            self.results["forces"] = self.results["forces"] + np.array([0.4, 0.0, 0.0])

    v_sf, _ = conservativeness_verdict(
        conservativeness(a, ShiftedForce(), n_atoms_probe=3, rng=np.random.default_rng(0)))
    chk(f"[음성②] 상수 힘 오프셋도 잡힌다 (판정 '{v_sf}')",
        v_sf == "non_conservative_suspect")

    # ── 음성 ③: 판정 함수가 잡음과 비보존을 **구분**한다
    fake_noise = {1e-3: {"rel_mean": 0.30, "rel_max": 0.5, "n_components": 9, "pairs": []},
                  5e-3: {"rel_mean": 0.02, "rel_max": 0.05, "n_components": 9, "pairs": []}}
    chk("[음성③] 작은 δ 에서만 큰 편차는 '잡음' 으로 분류된다",
        conservativeness_verdict(fake_noise)[0] == "energy_noise")

    # ── 잔여력
    clean = bulk("Cu", "fcc", a=3.59, cubic=True)      # EMT 평형 근처 = 힘이 작다
    chk("[양성] 평형 구조의 잔여력은 작다",
        residual_verdict(residual_at_reference(clean, EMT()))[0] == "agrees")
    chk("[음성④] 흔든 구조는 '불일치' 로 잡힌다",
        residual_verdict(residual_at_reference(a, EMT()))[0] == "disagrees")

    # ── 타이밍 판정 (합성 입력 — 실제 시간을 재지 않는다)
    over = [{"rep": 1, "n_atoms": 32, "s_per_step": 0.010, "us_per_atom_step": 312.5},
            {"rep": 2, "n_atoms": 256, "s_per_step": 0.020, "us_per_atom_step": 78.1}]
    comp = [{"rep": 1, "n_atoms": 32, "s_per_step": 0.010, "us_per_atom_step": 312.5},
            {"rep": 2, "n_atoms": 256, "s_per_step": 0.080, "us_per_atom_step": 312.5}]
    chk("[양성] 원자당 비용이 4배 싸지면 '오버헤드 지배'",
        timing_verdict(over)[0] == "overhead_bound")
    chk("[음성⑤] 원자당 비용이 그대로면 '연산 지배' — 셀 키우기 처방을 내면 안 된다",
        timing_verdict(comp)[0] == "compute_bound")
    chk("[음성⑥] 셀이 하나뿐이면 판정하지 않는다", timing_verdict(over[:1])[0] == "n/a")

    # ── GPU 가드
    chk("[음성⑦] QE 가 없으면 guard 통과", (guard_gpu() is None))

    print(f"\nselftest: {ok} 통과 / {fail} 실패")
    return 1 if fail else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--struct", help="구조 파일 (xyz/cif/POSCAR …)")
    ap.add_argument("--against", help="DFT 로 이완된 참조 구조 — 잔여력 모드")
    ap.add_argument("--conservative", action="store_true", help="보존성 유한차분 점검")
    ap.add_argument("--timing", action="store_true", help="셀 크기별 µs/atom·step")
    ap.add_argument("--reps", type=int, nargs="+", default=[1, 2],
                    help="--timing 에서 쓸 supercell 배수 (기본 1 2)")
    ap.add_argument("--steps", type=int, default=20, help="--timing 의 스텝 수")
    ap.add_argument("--probe_atoms", type=int, default=4,
                    help="--conservative 에서 볼 원자 수 (6N 번 에너지 계산)")
    ap.add_argument("--model", default="uma-s-1p1")
    ap.add_argument("--task", default="omat")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--allow_gpu_share", action="store_true")
    ap.add_argument("--tag", default="probe")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if not (a.conservative or a.timing or a.against):
        ap.error("--conservative / --timing / --against 중 하나는 있어야 한다 (또는 --selftest)")
    if (a.conservative or a.timing) and not a.struct:
        ap.error("--conservative / --timing 은 --struct 가 필요하다")

    guard_gpu(a.allow_gpu_share)
    calc = load_calc(a.model, a.task, a.device)
    out = {"model": a.model, "task": a.task, "tag": a.tag}

    if a.conservative:
        at = read_struct(a.struct)
        print(f"── 보존성  {a.struct}  ({len(at)} 원자, 표본 {a.probe_atoms} 원자 × 3축 × δ 2개)")
        res = conservativeness(at, calc, n_atoms_probe=a.probe_atoms)
        v, msg = conservativeness_verdict(res)
        for d in sorted(res):
            r = res[d]
            print(f"   δ={d:g} Å   상대편차 평균 {r['rel_mean']:.3%} · 최대 {r['rel_max']:.3%}"
                  f"  ({r['n_components']} 성분)")
        print(f"\n{msg}")
        out["conservativeness"] = {
            "struct": a.struct, "verdict": v, "message": msg,
            "by_delta": {str(k): {kk: vv for kk, vv in val.items() if kk != "pairs"}
                         for k, val in res.items()},
            "limitation": ("표본 원자만 본다 — 통과는 '표본이 통과'라는 뜻이다. "
                           "갈릴 때 원인이 비보존인지 에너지 잡음인지는 δ 2개의 비로 가른다."),
        }

    if a.timing:
        at = read_struct(a.struct)
        print(f"\n── 타이밍  {a.struct}  reps={a.reps} · {a.steps} 스텝")
        rows = timing(at, calc, reps=tuple(a.reps), n_steps=a.steps)
        for r in rows:
            print(f"   {r['n_atoms']:>5} 원자   {r['s_per_step']*1e3:8.1f} ms/step   "
                  f"{r['us_per_atom_step']:8.1f} µs/atom·step")
        v, msg = timing_verdict(rows)
        print(f"\n{msg}")
        out["timing"] = {"struct": a.struct, "rows": rows, "verdict": v, "message": msg,
                         "limitation": "힘 호출만 잰다 — 서모스탯·I/O·MSD 계산은 안 들어간다."}

    if a.against:
        at = read_struct(a.against)
        print(f"\n── DFT 최소점 잔여력  {a.against}  ({len(at)} 원자)")
        r = residual_at_reference(at, calc)
        v, msg = residual_verdict(r)
        print(f"   fmax {r['fmax_eV_per_A']:.4f} · frms {r['frms_eV_per_A']:.4f} eV/Å")
        for el, d in r["per_element"].items():
            print(f"     {el:<3} fmax {d['fmax']:.4f} · frms {d['frms']:.4f}  (n={d['n']})")
        print(f"\n{msg}")
        out["residual_at_dft_minimum"] = {
            "struct": a.against, **r, "verdict": v, "message": msg,
            "limitation": ("참조 구조가 정말 그 DFT 설정의 최소점이어야 한다. "
                           "이완이 덜 됐으면 이 잔여력은 MLIP 탓이 아니다."),
        }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p = OUT_DIR / f"mlip_engine_probe_{a.tag}.json"
    # ⚠⚠ 2026-08-20 실측 — 옛 코드는 통째로 덮어썼다. 같은 --tag 로 --conservative 를
    #   돌린 뒤 --timing 을 돌리면 **보존성 결과가 조용히 사라진다**(실제로 날아갔다).
    #   모드마다 따로 돌리는 게 정상 사용법이므로, 있는 파일에 **합친다**.
    if p.exists():
        try:
            old = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(old, dict):
                for k, v in old.items():
                    out.setdefault(k, v)      # 이번에 잰 절은 새 값이 이긴다
        except (OSError, ValueError):
            print(f"⚠ 기존 {p.name} 을 못 읽어 새로 쓴다 (덮어씀)")
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    have = [k for k in ("conservativeness", "timing", "residual_at_dft_minimum") if k in out]
    print(f"\n→ {p}   (담긴 절: {', '.join(have) or '없음'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
