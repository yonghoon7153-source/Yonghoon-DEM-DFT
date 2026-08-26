#!/usr/bin/env python3
"""bench_against_dft.py — MLIP 를 **DFT 라벨이 붙은 구조집합**에 대고 잰다.

왜 (2026-08-19). 우리는 UMA-s-1p1(omat) 을 황화물 전고체 전반에 쓰면서
**그 오차를 우리 계에서 직접 잰 적이 없다.** 하루 종일 다음이 되풀이됐다:
  · cascade 부피축이 뒤집힌 것이 UMA 편향인가 미수렴인가 (→ 미수렴이었다)
  · NEB 0.528 eV 가 UMA 탓인가 단일 경로 탓인가 (→ 아직 미확정)
  · preflight 이 "UMA sulfide PES softening" 을 알리바이로 썼다
전부 **참값이 없어서** 생긴 논쟁이다.

PET-MAD 논문(lab-cosmo)이 **Li₃PS₄ 의 DFT 라벨 데이터셋**(train 1940 / val 243 /
test 243, 16–64 원자, energy + forces)을 공개했다. ⇒ **DFT 를 한 판도 안 돌리고**
우리 모델의 오차를 황화물에서 잴 수 있다.

이 도구가 **하는 것**
  ① 힘 오차 — 참조계 무관. **이게 MD·NEB 에 직결되는 양이다.**
  ② 에너지 오차 — 원소별 **선형 참조 보정** 뒤. ⚠ 보정 없이는 무의미하다(아래).
  ③ **상대에너지 RRMSE** — 구조쌍 에너지차의 오차. 장벽·안정성 순위가 여기 달렸다.
  ④ 평균만이 아니라 **분포와 최악 사례** — 평균 RMSE 가 낮아도 목표 물성이 틀릴 수 있다는
     것이 이 분야의 반복 교훈이다(Kauwe 2021 §2.5 · Zhang npj 2026 RRMSE 22.8 %).

⭐ **에너지 참조 보정이 왜 필수인가**
  MLIP 가 배운 DFT(UMA=OMat24/PBE)와 이 데이터셋의 DFT 는 **코드·유사퍼텐셜·cutoff 가
  다르다.** 그래서 절대 총에너지는 상수만큼이 아니라 **원소별 상수만큼** 어긋난다:
      E_MLIP − E_DFT ≈ Σ_el n_el · e_el
  이 선형항을 최소제곱으로 빼내지 않으면 에너지 MAE 가 수 eV 로 나오고 **아무 의미도 없다.**
  보정은 **train 에서 적합해 test 에 적용**한다(자기적합 값도 같이 찍어 차이를 보인다).

이 도구가 **못 하는 것**
  · 응력을 안 잰다 (이 데이터셋에 stress 라벨이 없다).
  · **장벽을 안 잰다.** 힘·에너지가 맞아도 NEB 장벽이 맞는다는 보장은 없다 — 오히려
    그게 안 된다는 것이 위 문헌의 요지다. 장벽은 NEB 로 따로 재라.
  · 데이터셋 자체의 DFT 설정을 검증하지 않는다. 그쪽이 틀리면 이 값도 틀린다.
  · 여러 MLIP 를 한 번에 못 돌린다 — `--model` 로 한 번에 하나. (committee 는 각각 돌려 합친다)

  python3 tools/mlip/bench_against_dft.py --selftest
  python3 tools/mlip/bench_against_dft.py \
      --train <경로>/Li3PS4/train.xyz --test <경로>/Li3PS4/test.xyz --tag li3ps4_uma
"""
import argparse, json, os, subprocess, sys, time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / "db" / "properties"
#: 같은 GPU 를 쓰는 QE 바이너리 (kgy·gabia 공통 규약 — CLAUDE.md)
QE_BINS = ("pw.x", "neb.x", "cp.x", "ph.x")


def running_qe():
    out = []
    for b in QE_BINS:
        try:
            r = subprocess.run(["pgrep", "-x", b], capture_output=True, text=True)
            if r.stdout.strip():
                out.append(b)
        except FileNotFoundError:
            return []
    return out


def guard_gpu(allow_share=False):
    busy = running_qe()
    if not busy:
        return
    if allow_share:
        print(f"⚠ QE 가 돌고 있다: {', '.join(busy)} — 사용자 허용으로 같이 실행한다")
        return
    raise SystemExit(f"⛔ {', '.join(busy)} 가 돌고 있다 — VRAM 충돌. "
                     f"끝나고 실행하거나 --allow_gpu_share")


# ── 참조 보정 ────────────────────────────────────────────────────────────────
def element_matrix(structs, elements):
    """구조 × 원소 개수 행렬 (선형 참조 적합용)."""
    M = np.zeros((len(structs), len(elements)))
    for i, a in enumerate(structs):
        s = a.get_chemical_symbols()
        for j, e in enumerate(elements):
            M[i, j] = s.count(e)
    return M


def fit_reference(dE, structs, elements):
    """ΔE = E_MLIP − E_DFT 를 **원소 개수의 선형결합**으로 적합.

    반환 (계수, 적합 후 잔차, R²). 계수는 원소당 eV — 코드·유사퍼텐셜 차이의 흡수항이다.
    ⚠ 이 항을 빼지 않은 에너지 오차는 인용하면 안 된다 (모듈 docstring 참조).
    """
    M = element_matrix(structs, elements)
    coef, *_ = np.linalg.lstsq(M, dE, rcond=None)
    resid = dE - M @ coef
    ss_tot = float(((dE - dE.mean()) ** 2).sum())
    r2 = 1.0 - float((resid ** 2).sum()) / ss_tot if ss_tot > 0 else float("nan")
    return coef, resid, r2


def rrmse(pred, ref):
    """상대 RMSE (%) — Zhang npj 2026 규약: RMSE ÷ 참값의 제곱평균.

    ⚠ 절대 RMSE 와 다르다. 상대에너지처럼 **평균이 0 근처인 양**에서 절대 RMSE 는
    작아 보이지만 신호 대비로는 클 수 있다.
    """
    ref = np.asarray(ref, float)
    denom = float(np.sqrt((ref ** 2).mean()))
    if denom == 0:
        return float("nan")
    return 100.0 * float(np.sqrt(((np.asarray(pred, float) - ref) ** 2).mean())) / denom


# ── 실행 ─────────────────────────────────────────────────────────────────────
def predict(structs, model="uma-s-1p1", task="omat", device="cuda", batch_note=200):
    """(E_pred, F_pred 목록). 실패한 구조는 None 으로 남기고 계속한다."""
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    pred = pretrained_mlip.get_predict_unit(model, device=device)
    calc = FAIRChemCalculator(pred, task_name=task)
    E, F = [], []
    t0 = time.time()
    for i, a in enumerate(structs):
        b = a.copy()
        b.calc = calc
        try:
            E.append(float(b.get_potential_energy()))
            F.append(np.asarray(b.get_forces(), float))
        except Exception as ex:
            E.append(None); F.append(None)
            print(f"  ⚠ [{i}] {type(ex).__name__}: {str(ex)[:70]}")
        if (i + 1) % batch_note == 0:
            print(f"   {i+1}/{len(structs)}  ({time.time()-t0:.0f}s)")
    return E, F, time.time() - t0


# extxyz 의 라벨 이름은 데이터셋마다 다르다. 우리가 붙이는 이름을 강요하지 말고 찾아서 쓴다.
# (2026-08-19 kgy 실측: PET-MAD Li₃PS₄ 세트가 `forces` 가 아닌 이름을 쓴다 — raw 오류로 멈췄다)
FORCE_ALIASES = ("forces", "force", "REF_forces", "ref_forces", "DFT_forces", "dft_forces",
                 "forces_ref", "F", "gradients")
ENERGY_ALIASES = ("energy", "REF_energy", "ref_energy", "DFT_energy", "dft_energy",
                  "free_energy", "TotEnergy", "total_energy", "E")


def force_key(atoms):
    """이 구조의 힘 라벨 이름. 없으면 None.

    ⚠ **표준 extxyz 는 `arrays` 에 안 들어간다.** ASE 는 `Properties=…:forces:R:3` 을
    읽으면 SinglePointCalculator 로 보낸다 (energy 도 마찬가지로 info 가 아니라 calc).
    2026-08-19 kgy 실측: PET-MAD 세트가 정확히 이 경우였고, arrays 만 보던 탐지가
    "forces 가 없다"고 잘못 말했다. → `calc` 경로를 반드시 같이 본다.
    `gradients` 는 dE/dR 이라 부호가 반대다.
    """
    for k in FORCE_ALIASES:
        if k in atoms.arrays:
            return k
    try:
        atoms.get_forces()
        return "calc"
    except Exception:
        return None


def get_forces_label(atoms, key):
    """DFT 힘 라벨을 꺼낸다. `gradients` = dE/dR 이므로 부호를 뒤집는다."""
    if key == "calc":
        return np.asarray(atoms.get_forces(), float)
    v = np.asarray(atoms.arrays[key], float)
    return -v if key == "gradients" else v


def energy_key(atoms):
    """이 구조의 에너지 라벨 이름. calculator 가 붙어 있으면 'calc'. 없으면 None."""
    try:
        atoms.get_potential_energy()
        return "calc"
    except Exception:
        pass
    for k in ENERGY_ALIASES:
        if k in atoms.info:
            return k
    return None


def get_energy_label(atoms, key):
    return float(atoms.get_potential_energy()) if key == "calc" else float(atoms.info[key])


def evaluate(structs, E_pred, F_pred, coef, elements, label, fkey="forces", ekey="calc"):
    """참조 보정된 에너지·힘·상대에너지 지표."""
    ok = [i for i, e in enumerate(E_pred) if e is not None]
    S = [structs[i] for i in ok]
    Ep = np.array([E_pred[i] for i in ok])
    Ed = np.array([get_energy_label(s, ekey) for s in S])
    nat = np.array([len(s) for s in S], float)
    shift = element_matrix(S, elements) @ coef
    dE = (Ep - shift) - Ed                       # 보정 후 잔차 (총에너지)
    dE_at = dE / nat
    # 상대에너지 — 첫 구조 기준 (원소별 항은 조성이 같으면 저절로 상쇄된다)
    relp, reld = (Ep - shift) - (Ep - shift)[0], Ed - Ed[0]
    Fp = np.concatenate([F_pred[i].ravel() for i in ok])
    Fd = np.concatenate([get_forces_label(S[k], fkey).ravel() for k in range(len(S))])
    dF = Fp - Fd
    # 원소별 힘 오차 — Li 가 우리에게 제일 중요하다
    per_el = {}
    for e in elements:
        m = np.concatenate([np.repeat([s.get_chemical_symbols()[k] == e
                                       for k in range(len(s))], 3) for s in S])
        if m.any():
            per_el[e] = {"MAE": round(float(np.abs(dF[m]).mean()), 5),
                         "RMSE": round(float(np.sqrt((dF[m] ** 2).mean())), 5),
                         "n_components": int(m.sum())}
    worst = np.argsort(-np.abs(dE_at))[:5]
    return {
        "set": label, "n_structures": len(S), "n_failed": len(structs) - len(S),
        "energy_after_reference_correction": {
            "MAE_eV_per_atom": round(float(np.abs(dE_at).mean()), 5),
            "RMSE_eV_per_atom": round(float(np.sqrt((dE_at ** 2).mean())), 5),
            "max_abs_eV_per_atom": round(float(np.abs(dE_at).max()), 5),
            "median_eV_per_atom": round(float(np.median(np.abs(dE_at))), 5)},
        "relative_energy": {
            "RRMSE_pct": round(rrmse(relp, reld), 2),
            "RMSE_eV": round(float(np.sqrt(((relp - reld) ** 2).mean())), 5)},
        "forces": {
            "MAE_eV_per_A": round(float(np.abs(dF).mean()), 5),
            "RMSE_eV_per_A": round(float(np.sqrt((dF ** 2).mean())), 5),
            "max_abs_eV_per_A": round(float(np.abs(dF).max()), 5),
            # ★ 참조 RMS 로 정규화한 상대오차 (Shapeev 2016 관례).
            #   같은 0.05 eV/Å 도 딱딱한 계에선 훌륭하고 무른 계에선 형편없다.
            "rms_ref_eV_per_A": round(float(np.sqrt((Fd ** 2).mean())), 5),
            "rel_MAE_pct": (round(float(np.abs(dF).mean() / np.sqrt((Fd ** 2).mean()) * 100), 2)
                            if (Fd ** 2).mean() > 0 else None),
            "pearson_r": (round(float(np.corrcoef(Fd, Fp)[0, 1]), 5) if Fd.size > 2 else None),
            # ★★ softening 기울기 (2026-08-26 신설) — OMat24 보충자료의 `force_softening` 과 같은 척도.
            #   s = Σ(F_ref·F_pred)/Σ(F_ref²), 원점을 지나는 최소제곱 기울기.
            #   s < 1 = 예측힘이 참조보다 작다 = PES 가 무르다.
            #   ⛔ **r 로는 원리적으로 못 본다** — r 은 척도불변이라 힘을 전부 절반으로 줄여도 1 이다.
            #   실측 2026-08-26 (같은 시험셋 lips.xyz 251프레임):
            #     UMA-s-1p1(OMat24)  0.9874   ↔   SevenNet-0(MPtrj)  0.7899
            #   ⇒ OMat24 논문의 "softening 은 아키텍처가 아니라 훈련셋" 이 우리 화학계에서 재현.
            "softening_slope": (round(float((Fd * Fp).sum() / (Fd ** 2).sum()), 5)
                                if (Fd ** 2).sum() > 0 else None),
            "per_element": per_el},
        "worst5_structures": [{"index": int(ok[i]), "n_atoms": int(nat[i]),
                               "dE_eV_per_atom": round(float(dE_at[i]), 5)}
                              for i in worst],
    }


def _softening_slope(Fd, Fp):
    """원점을 지나는 최소제곱 기울기. evaluate() 와 **같은 식**을 쓰도록 분리해 둔다.

    ⛔ 이 함수가 못 하는 것: 유의성을 판정하지 않는다. 기울기 하나만 돌려준다.
    """
    Fd, Fp = np.asarray(Fd, float).ravel(), np.asarray(Fp, float).ravel()
    return float((Fd * Fp).sum() / (Fd ** 2).sum()) if (Fd ** 2).sum() > 0 else None


def selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok &= bool(c)

    # ── softening 기울기 (2026-08-26 병합) ──
    ref = np.array([1.0, -2.0, 0.5, 0.0, 3.0, -1.0])
    chk(abs(_softening_slope(ref, ref) - 1.0) < 1e-12, "완전 일치면 softening 기울기 1")
    chk(abs(_softening_slope(ref, ref * 0.5) - 0.5) < 1e-12,
        "★ 힘을 절반으로 줄이면 기울기 0.5 — **이것이 softening 이다**")
    chk(abs(float(np.corrcoef(ref, ref * 0.5)[0, 1]) - 1.0) < 1e-12,
        "★ [음성] 그런데 그때도 **r 은 1** — r 로는 softening 을 원리적으로 못 본다")
    chk(_softening_slope(np.zeros(6), ref) is None,
        "[음성] 참조힘이 전부 0이면 None (0 나눗셈을 지어내지 않는다)")
    chk(_softening_slope(ref, ref * 1.2) > 1.0,
        "기울기 >1 도 나온다 (과대예측 = 과경직) — 1 을 상한으로 자르지 않는다")

    from ase import Atoms
    els = ["Li", "P", "S"]
    rng = np.random.default_rng(0)
    ss = []
    for _ in range(40):
        n = {"Li": int(rng.integers(4, 12)), "P": int(rng.integers(1, 4)),
             "S": int(rng.integers(2, 8))}
        sym = sum([[e] * n[e] for e in els], [])
        ss.append(Atoms(sym, positions=rng.normal(0, 5, (len(sym), 3)), cell=np.eye(3) * 12,
                        pbc=True))
    # 양성 — 정확히 원소별 상수만큼 어긋난 경우를 완전히 걷어내야 한다
    true = {"Li": 0.7, "P": -1.3, "S": 0.4}
    dE = np.array([sum(true[e] * s.get_chemical_symbols().count(e) for e in els) for s in ss])
    coef, resid, r2 = fit_reference(dE, ss, els)
    chk(np.allclose(coef, [true[e] for e in els], atol=1e-8),
        f"[양성] 원소별 상수 오프셋을 정확히 복원한다 {np.round(coef,4)}")
    chk(float(np.abs(resid).max()) < 1e-8 and r2 > 0.999999,
        f"[양성] 보정 뒤 잔차 ≈ 0 (max {np.abs(resid).max():.2e}, R² {r2:.6f})")
    # ★ 음성 — 조성과 무관한 잡음은 **못 없애야** 한다 (없앤다면 과적합이다)
    noise = rng.normal(0, 0.5, len(ss))
    _, resid2, r2b = fit_reference(dE + noise, ss, els)
    chk(float(np.std(resid2)) > 0.2,
        f"[음성] 조성 무관 잡음은 안 없어진다 (잔차 σ {np.std(resid2):.3f}, 넣은 σ 0.5)")
    chk(r2b < 0.9999, f"[음성] 잡음이 있으면 R² 가 1 이 아니다 ({r2b:.4f})")
    # ★ 음성 — 보정을 **안 하면** 오차가 크게 남는다 (보정이 필수임을 못박는다)
    chk(float(np.abs(dE).mean()) > 1.0,
        f"[음성] 보정 전 |ΔE| 평균이 {np.abs(dE).mean():.2f} eV — 보정 없이 인용 금지")
    # RRMSE
    chk(abs(rrmse([1.0, 2.0], [1.0, 2.0])) < 1e-9, "[양성] 완전 일치면 RRMSE 0 %")
    chk(abs(rrmse([1.1, 2.2], [1.0, 2.0]) - 10.0) < 1e-6,
        "[양성] 10 % 어긋나면 RRMSE 10 %")
    chk(np.isnan(rrmse([0.1], [0.0])), "[음성] 참값이 전부 0 이면 nan (0 나눗셈 안 한다)")
    # ── 라벨 이름 탐지 (2026-08-19: PET-MAD 세트가 `forces` 를 안 쓴다)
    lab = Atoms("LiPS", positions=rng.normal(0, 2, (3, 3)), cell=np.eye(3) * 8, pbc=True)
    chk(force_key(lab) is None, "[음성] 힘 라벨이 없으면 None (0 을 비교하지 않는다)")
    chk(energy_key(lab) is None, "[음성] 에너지 라벨이 없으면 None")
    lab.arrays["REF_forces"] = np.ones((3, 3))
    lab.info["REF_energy"] = -7.5
    chk(force_key(lab) == "REF_forces", "[양성] 별칭 REF_forces 를 찾는다")
    chk(energy_key(lab) == "REF_energy", "[양성] 별칭 REF_energy 를 찾는다")
    chk(abs(get_energy_label(lab, "REF_energy") + 7.5) < 1e-12, "[양성] 별칭 에너지 값이 맞다")
    chk(np.allclose(get_forces_label(lab, "REF_forces"), 1.0), "[양성] 별칭 힘 값이 맞다")
    # ★ 음성 — gradients 는 dE/dR 이라 **부호를 뒤집어야** 한다 (안 뒤집으면 힘이 통째로 반대)
    grad = Atoms("LiPS", positions=rng.normal(0, 2, (3, 3)), cell=np.eye(3) * 8, pbc=True)
    grad.arrays["gradients"] = np.full((3, 3), 2.0)
    chk(np.allclose(get_forces_label(grad, "gradients"), -2.0),
        "[음성] gradients 는 부호를 뒤집는다 (그냥 쓰면 힘이 반대)")
    # ★ 음성 — 우선순위: forces 가 있으면 별칭보다 forces 를 쓴다
    both = Atoms("LiPS", positions=rng.normal(0, 2, (3, 3)), cell=np.eye(3) * 8, pbc=True)
    both.arrays["gradients"] = np.full((3, 3), 2.0)
    both.arrays["forces"] = np.full((3, 3), 5.0)
    chk(force_key(both) == "forces", "[음성] forces 가 있으면 별칭에 안 뺏긴다")
    # ★★ 표준 extxyz 경로 — ASE 는 forces/energy 를 arrays/info 가 아니라 **calc** 에 넣는다.
    #    (2026-08-19 kgy 실측 재현: 이걸 안 보면 라벨이 있는데 "없다"고 말한다)
    from ase.calculators.singlepoint import SinglePointCalculator
    spc = Atoms("LiPS", positions=rng.normal(0, 2, (3, 3)), cell=np.eye(3) * 8, pbc=True)
    spc.calc = SinglePointCalculator(spc, energy=-9.25, forces=np.full((3, 3), 0.3))
    chk(sorted(spc.arrays) == ["numbers", "positions"],
        "[음성] extxyz forces 는 arrays 에 없다 — arrays 만 보면 놓친다")
    chk(force_key(spc) == "calc", "[양성] calculator 에 있는 힘을 찾는다")
    chk(energy_key(spc) == "calc", "[양성] calculator 에 있는 에너지를 찾는다")
    chk(np.allclose(get_forces_label(spc, "calc"), 0.3), "[양성] calc 힘 값이 맞다")
    chk(abs(get_energy_label(spc, "calc") + 9.25) < 1e-12, "[양성] calc 에너지 값이 맞다")
    # guard
    try:
        guard_gpu(); chk(True, "[음성] QE 없으면 guard 통과")
    except SystemExit:
        chk(False, "[음성] QE 없는데 guard 가 막았다")
    _real = globals()["running_qe"]
    try:
        globals()["running_qe"] = lambda: ["pw.x"]
        try:
            guard_gpu(); chk(False, "[음성] QE 도는데 통과시켰다")
        except SystemExit:
            chk(True, "[음성] QE 돌면 guard 가 막는다")
    finally:
        globals()["running_qe"] = _real
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", required=False, help="참조 보정을 적합할 집합 (DFT 라벨)")
    ap.add_argument("--test", required=True, help="평가할 집합 (DFT 라벨)")
    ap.add_argument("--model", default="uma-s-1p1")
    ap.add_argument("--task", default="omat")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--limit", type=int, help="앞에서 N 개만 (시범)")
    ap.add_argument("--allow_gpu_share", action="store_true")
    ap.add_argument("--tag", default="bench")
    ap.add_argument("--out", default=None)
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    a = ap.parse_args()
    guard_gpu(a.allow_gpu_share)

    from ase.io import read
    # ⚠ 없는 파일을 ASE 역추적으로 던지지 않는다 — 무엇이 없고 뭘 해야 하는지 말한다
    #   (2026-08-19 kgy 실측: 데이터셋을 아직 안 올려서 raw FileNotFoundError 가 났다)
    for lab, pth in (("--test", a.test), ("--train", a.train)):
        if pth and not os.path.isfile(pth):
            raise SystemExit(
                f"⛔ {lab} 파일이 없다: {pth}\n"
                f"   이 도구는 **DFT 라벨이 붙은 extxyz**(energy + forces)를 받는다.\n"
                f"   PET-MAD 의 Li₃PS₄ 세트를 쓸 거면 그 기계에 먼저 올려야 한다:\n"
                f"     scp Li3PS4.zip <host>:~/work/  &&  unzip ~/work/Li3PS4.zip -d ~/work/\n"
                f"   그 뒤 --train ~/work/Li3PS4/train.xyz --test ~/work/Li3PS4/test.xyz")
    te = read(a.test, index=(f":{a.limit}" if a.limit else ":"))
    tr = read(a.train, index=(f":{a.limit}" if a.limit else ":")) if a.train else None
    # 라벨이 진짜 있는지 — 없으면 조용히 0 을 비교하게 두지 않는다.
    # 이름은 데이터셋마다 다르므로 별칭을 찾고, 못 찾으면 **거기 뭐가 있는지 찍어 준다**.
    probe = te[0]
    fkey = force_key(probe)
    if fkey is None:
        raise SystemExit(
            f"⛔ {a.test} 에서 힘 라벨을 못 찾았다 — 이 도구는 힘을 1순위로 잰다.\n"
            f"   찾아본 이름: {', '.join(FORCE_ALIASES)}  (+ SinglePointCalculator)\n"
            f"   이 파일의 per-atom 배열: {sorted(probe.arrays)}\n"
            f"   구조당 info 키: {sorted(probe.info)}\n"
            f"   calculator: {type(probe.calc).__name__ if probe.calc else '없음'}"
            f" · 담긴 값 {sorted(getattr(probe.calc, 'results', {}) or {})}\n"
            f"   → 맞는 이름이 위에 있으면 FORCE_ALIASES 에 추가한다 (한 줄).")
    ekey = energy_key(probe)
    if ekey is None:
        raise SystemExit(
            f"⛔ {a.test} 에서 에너지 라벨을 못 찾았다.\n"
            f"   찾아본 이름: {', '.join(ENERGY_ALIASES)}\n"
            f"   구조당 info 키: {sorted(probe.info)}")
    if a.train:
        ptr = tr[0]
        if force_key(ptr) != fkey or energy_key(ptr) != ekey:
            raise SystemExit(f"⛔ train 과 test 의 라벨 이름이 다르다 — 참조 보정이 섞인다.\n"
                             f"   test: forces={fkey} energy={ekey} / "
                             f"train: forces={force_key(ptr)} energy={energy_key(ptr)}")
    print(f"   라벨: forces=`{fkey}` energy=`{ekey}`"
          + ("  ⚠ gradients = dE/dR 이므로 부호를 뒤집어 쓴다" if fkey == "gradients" else ""))
    elements = sorted({e for s in (tr or []) + te for e in s.get_chemical_symbols()})
    print(f"── {a.model}/{a.task}   원소 {elements}")
    print(f"   test  {len(te)}구조 ({min(len(s) for s in te)}–{max(len(s) for s in te)} 원자)"
          + (f" · train {len(tr)}구조" if tr else " · train 없음 → **자기적합**만"))

    print("   test 예측…")
    Ete, Fte, t1 = predict(te, a.model, a.task, a.device)
    ok_te = [i for i, e in enumerate(Ete) if e is not None]
    dE_te = np.array([Ete[i] - get_energy_label(te[i], ekey) for i in ok_te])

    # 참조 보정 — train 에서 적합해 test 에 적용 (자기적합도 같이 낸다)
    coef_self, _, r2_self = fit_reference(dE_te, [te[i] for i in ok_te], elements)
    if tr:
        print("   train 예측 (참조 보정 적합용)…")
        Etr, Ftr, t2 = predict(tr, a.model, a.task, a.device)
        ok_tr = [i for i, e in enumerate(Etr) if e is not None]
        dE_tr = np.array([Etr[i] - get_energy_label(tr[i], ekey) for i in ok_tr])
        coef, _, r2 = fit_reference(dE_tr, [tr[i] for i in ok_tr], elements)
    else:
        coef, r2, t2 = coef_self, r2_self, 0.0

    res = evaluate(te, Ete, Fte, coef, elements, "test", fkey, ekey)
    res_self = evaluate(te, Ete, Fte, coef_self, elements, "test(자기적합 — 낙관치)", fkey, ekey)
    rec = {
        "what": "MLIP evaluated against a DFT-labelled structure set.",
        "model": a.model, "task": a.task,
        "test_file": a.test, "train_file": a.train,
        "elements": elements,
        "reference_correction": {
            "note": "E_MLIP - E_DFT fitted as a linear combination of element counts. "
                    "Absolute energies of two different DFT setups are NOT comparable "
                    "without this; quoting an uncorrected energy error is meaningless.",
            "fitted_on": "train" if tr else "test(self)",
            "coefficients_eV_per_atom": {e: round(float(c), 5)
                                         for e, c in zip(elements, coef)},
            "fit_R2": round(float(r2), 6),
            "self_fit_R2": round(float(r2_self), 6)},
        "results": res, "results_self_fit": res_self,
        "seconds": {"test": round(t1, 1), "train": round(t2, 1)},
        "caveats": ["Forces need no reference correction - they are the directly "
                    "comparable quantity and the one that drives MD and NEB.",
                    "A low mean error does NOT guarantee a correct migration barrier; "
                    "measure the barrier separately."],
    }
    out = Path(a.out or (OUTDIR / f"mlip_bench_{a.tag}.json"))
    out.write_text(json.dumps(rec, ensure_ascii=False, indent=2))

    e, f = res["energy_after_reference_correction"], res["forces"]
    print(f"\n■ 참조 보정 (원소당 eV): "
          + " · ".join(f"{k} {v:+.3f}" for k, v in
                       rec['reference_correction']['coefficients_eV_per_atom'].items())
          + f"   적합 R² {r2:.4f}")
    print(f"■ 에너지 (보정 후)  MAE {e['MAE_eV_per_atom']:.4f} · RMSE {e['RMSE_eV_per_atom']:.4f} eV/atom"
          f"   최악 {e['max_abs_eV_per_atom']:.4f}")
    print(f"■ 상대에너지        RRMSE {res['relative_energy']['RRMSE_pct']:.1f} %"
          f"   (장벽·순위가 여기 달렸다)")
    print(f"■ **힘**            MAE {f['MAE_eV_per_A']:.4f} · RMSE {f['RMSE_eV_per_A']:.4f} eV/Å"
          f"   최악 {f['max_abs_eV_per_A']:.3f}")
    # ⛔ JSON 에만 넣고 화면에 안 찍으면 **없는 것과 같다** (2026-08-26 실측: softening 을
    #    dict 에는 넣었는데 print 를 안 고쳐서 사용자가 못 봤다).
    if f.get("rel_MAE_pct") is not None:
        print(f"     참조 RMS {f['rms_ref_eV_per_A']:.3f} eV/Å  →  **상대 {f['rel_MAE_pct']:.2f} %**"
              f"   r={f['pearson_r']:.5f}")
    sl = f.get("softening_slope")
    if sl is not None:
        tag = ("✅ 경직/중립" if sl >= 0.995 else
               "⚠ 약한 softening" if sl >= 0.97 else "🔴 softening")
        print(f"     **softening 기울기 {sl:.4f}**  ({tag})"
              f"  — 1 보다 작으면 예측힘이 참조보다 작다. **r 로는 원리적으로 안 보인다**")
        print(f"     📏 같은 시험셋 대조(lips 251프레임): UMA(OMat24) 0.9874 ↔ SevenNet-0(MPtrj) 0.7899")
    for el, d in f["per_element"].items():
        print(f"     {el:3s} MAE {d['MAE']:.4f} · RMSE {d['RMSE']:.4f} eV/Å")
    print(f"\n→ {out}")


if __name__ == "__main__":
    main()
