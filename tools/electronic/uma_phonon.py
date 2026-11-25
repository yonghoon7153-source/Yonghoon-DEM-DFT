#!/usr/bin/env python3
"""UMA Gamma-point phonons -> dynamical stability + lowest modes.

Finite-displacement Hessian with the UMA(omat) calculator (ASE Vibrations),
to test whether the B2O3-doped champion is a true local minimum (no/few
imaginary modes) and to list the soft modes. Runs on gabia (UMA + GPU).

  python3 tools/electronic/uma_phonon.py --xyz db/structures/b2o3_relaxV0.xyz \
      --out /data/work/runs/b2o3_phonon
  python3 tools/electronic/uma_phonon.py --selftest          # UMA 없이 해석 퍼텐셜로

768 force evals for 128 atoms (~10-30 min on a shared GPU).

⛔ 2026-11-09 고침 (Codex DU P1-7 · P1-8)
  ① 캐시 결박: ASE Vibrations 는 같은 이름의 캐시가 있으면 **힘을 다시 계산하지 않고** 옛 변위 힘을 쓴다 —
     Codex 재현: 좌표를 최소점 → 안장점으로 바꿔도 같은 --out 이면 힘 계산 0 회 · 옛 안정 스펙트럼 재사용
     (새 --out 이면 −734 cm⁻¹ 검출) · δ 0.02 → 0.01 만 바꿔도 주파수 √2 배. 이제 캐시 옆에 정체성
     (구조 해시 · 모델 · δ · nfree) 을 쓰고, 다르면 멈춘다 (새 --out). 정체성 없는 옛 캐시도 멈춘다
     (--accept_unbound_cache 로만).
  ② 허수 판정: 옛 판은 −30 cm⁻¹ 아래가 없으면 'DYNAMICALLY STABLE (champion is a local minimum)' 이라 찍었다 —
     비병진 허수 −20 cm⁻¹ 셋이 있어도. 이제 병진 모드를 **고유벡터로** 가린다 (모든 원자가 같이 움직이는 정도
     ≥ 0.9 [제안] — 정렬된 첫 세 모드를 버리면 광학 허수를 지울 수 있다) · 비병진 모드를
     < −30 (경보 · UNSTABLE) · −30 ~ −5 (SOFT · 보류) 로 세고, 둘 다 0 일 때만 STABLE 이다.
     −30 은 '큰 불안정' 경보 문턱일 뿐 안정 판정 문턱이 아니다. −5 아래 허수는 수치 잡음으로 본다 [기존 −5].

⛔ 이 도구가 못 하는 것
  · Γ 점만 본다 (셀 안 진동) — 띠 전체 (q ≠ 0) 불안정 · 셀 모양 (탄성) 불안정은 못 본다.
  · STABLE 은 '국소 최소의 필요조건' 이다 — 열적으로 안정하다는 뜻이 아니다 (그건 MD 골격 판정 몫).
  · UMA 퍼텐셜의 정확도를 검증하지 않는다 · 셀은 고정 (주어진 구조 그대로).
"""
import argparse, hashlib, json, sys
from pathlib import Path
import numpy as np
from ase.io import read
from ase.vibrations import Vibrations
from ase import units

ALARM_CM = -30.0      # [기존] 큰 불안정 경보
SOFT_CM = -5.0        # [기존] 이 아래 허수는 판정에 넣는다 (위는 수치 잡음)
TRANS_OVERLAP = 0.9   # [제안 2026-11-09] 병진 모드 판별 — 균일 변위와의 겹침


def struct_hash(atoms):
    h = hashlib.sha256()
    h.update(",".join(atoms.get_chemical_symbols()).encode())
    h.update(np.round(np.asarray(atoms.get_positions()), 6).tobytes())
    h.update(np.round(np.asarray(atoms.cell.array), 6).tobytes())
    h.update(np.round(np.asarray(atoms.get_masses()), 6).tobytes())
    return h.hexdigest()


def cache_identity(atoms, model, delta, nfree):
    idn = {"struct_sha256": struct_hash(atoms), "n_atoms": len(atoms), "model": str(model),
           "delta_A": float(delta), "nfree": int(nfree), "indices": "all",
           "method": "ase.vibrations.Vibrations (finite displacement · Γ)"}
    idn["sha256"] = hashlib.sha256(json.dumps(idn, sort_keys=True).encode()).hexdigest()
    return idn


def translation_overlap(modes):
    """modes (3N, N, 3) 데카르트 변위 (ASE: 질량 가중 고유벡터 × m^-½) → 모드마다 균일 병진과의 겹침 (0–1)."""
    m = np.asarray(modes, float)
    n = m.shape[1]
    num = (m.sum(axis=1) ** 2).sum(axis=1) / n          # Σ_α (Σ_i d_iα)² / N
    den = (m ** 2).sum(axis=(1, 2))
    return np.where(den > 0, num / den, 0.0)


def classify(freqs_cm, overlap):
    """주파수 (cm⁻¹ · 음수 = 허수) + 병진 겹침 → 판정 dict."""
    f = np.asarray(freqs_cm, float)
    trans = overlap >= TRANS_OVERLAP
    nt = ~trans
    n_alarm = int(((f < ALARM_CM) & nt).sum())
    n_soft = int(((f >= ALARM_CM) & (f < SOFT_CM) & nt).sum())
    notes = []
    if int(trans.sum()) != 3:
        notes.append(f"병진 모드 {int(trans.sum())} 개 (Γ 결정은 3 이어야) — 낮은 광학 모드와 섞였을 수 있다")
    if trans.any() and np.abs(f[trans]).max() > abs(ALARM_CM):
        notes.append(f"병진 모드가 0 에서 멀다 (최대 |f| {np.abs(f[trans]).max():.1f} cm⁻¹) — 힘 잡음 · 이완 미수렴 의심")
    if n_alarm:
        verdict = f"UNSTABLE — 비병진 허수 {n_alarm} 개가 {ALARM_CM:g} cm⁻¹ 아래"
    elif n_soft:
        verdict = f"SOFT (보류) — 비병진 허수 {n_soft} 개가 {ALARM_CM:g} ~ {SOFT_CM:g} cm⁻¹ 사이"
    elif notes:
        verdict = "보류 — 병진 모드 판별이 깨끗하지 않다 (notes)"
    else:
        verdict = (f"STABLE — 비병진 허수 없음 ({SOFT_CM:g} cm⁻¹ 기준) · Γ 점 국소 최소의 필요조건 "
                   f"(열적 안정 아님)")
    order = np.argsort(f)
    return {"verdict": verdict, "verdict_code": verdict.split()[0],
            "n_modes": int(len(f)), "n_translational": int(trans.sum()),
            "n_nontrans_below_alarm": n_alarm, "n_nontrans_soft": n_soft,
            "alarm_cm": ALARM_CM, "soft_cm": SOFT_CM, "trans_overlap_min": TRANS_OVERLAP,
            "translational_modes": [{"index": int(i), "freq_cm": round(float(f[i]), 3),
                                     "overlap": round(float(overlap[i]), 4)} for i in np.where(trans)[0]],
            "lowest_nontrans_cm": [round(float(f[i]), 3) for i in order if not trans[i]][:12],
            "notes": notes}


def phonon_report(atoms, calc, out, delta=0.02, model="uma-s-1p1/omat", nfree=2,
                  accept_unbound_cache=False, require_fmax=0.01):
    """캐시 결박 → (입력 힘 검사) → Vibrations → 병진 판별 → 판정. out 은 접두어 (out_cache/ · out_freqs.txt · out_summary.json).

    require_fmax: 입력 구조의 원자 힘 최대가 이보다 크면 멈춘다 — 정지점이 아닌 구조의 조화 진동은 뜻이 없다
      (Codex DU Q9 'fmax 0.01 을 선언이 아니라 실행 조건으로' · 0 이면 검사 안 함 · 셀 응력은 안 본다).
    """
    out = str(out)
    atoms = atoms.copy()
    atoms.calc = calc
    fmax_in = float(np.sqrt((np.asarray(atoms.get_forces()) ** 2).sum(axis=1).max()))
    if require_fmax and fmax_in > require_fmax:
        raise SystemExit(f"⛔ 입력 구조의 최대 힘 {fmax_in:.4f} eV/Å > 요구 {require_fmax} — 먼저 같은 모델로 "
                         f"fmax {require_fmax} 까지 이완하라 (run_anneal.py --time_ps 0 --relax_fmax {require_fmax})")
    cache = Path(out + "_cache")
    idf = Path(out + "_cache.identity.json")
    idn = cache_identity(atoms, model, delta, nfree)
    has_cache = cache.exists() and any(cache.iterdir())
    accepted_unbound = bool(has_cache and not idf.exists())
    if has_cache:
        if not idf.exists():
            if not accept_unbound_cache:
                raise SystemExit(f"⛔ {cache} 에 정체성 없는 옛 캐시가 있다 — 다른 구조 · δ 의 힘일 수 있다. "
                                 f"새 --out 을 쓰거나 --accept_unbound_cache 로 명시하라")
        else:
            old = json.loads(idf.read_text())
            if old.get("sha256") != idn["sha256"]:
                diff = sorted(k for k in idn if k != "sha256" and old.get(k) != idn[k])
                raise SystemExit(f"⛔ {cache} 는 다른 계산의 캐시다 (다른 칸 {diff}) — 새 --out 을 쓰라 "
                                 f"(ASE 가 옛 힘을 그대로 쓴다)")
    else:
        # ⛔ 2026-11-09 (Codex DV P1-3): 빈 캐시로 **새로 시작할 때는 정체성도 새로 쓴다** — 옛 판은 정체성 파일이
        #   있으면 안 건드려서, 캐시만 비우고 다른 구조 (B) 를 돌리면 'A 정체성 + B 힘' 이 되어 A 를 다시 돌릴 때
        #   B 의 힘을 썼다 (거짓 STABLE · Codex 재현).
        cache.parent.mkdir(parents=True, exist_ok=True)
        idf.unlink(missing_ok=True)
    if not idf.exists():
        rec = dict(idn)
        if accepted_unbound:
            rec["⚠_unbound_cache_accepted"] = "정체성 없이 남아 있던 캐시를 --accept_unbound_cache 로 받았다 — 그 힘의 출처는 확인 안 됨"
        idf.write_text(json.dumps(rec, ensure_ascii=False, indent=1) + "\n")
    vib = Vibrations(atoms, delta=delta, nfree=nfree, name=str(cache))
    vib.run()
    energies, modes = vib.get_vibrations().get_energies_and_modes()
    fc = energies / units.invcm
    freqs = np.array([z.real if abs(z.imag) < 1e-6 else -abs(z.imag) for z in fc])
    ov = translation_overlap(modes)
    rep = classify(freqs, ov)
    rep["identity"] = idn
    rep["input_fmax_eV_A"] = fmax_in
    rep["require_fmax_eV_A"] = require_fmax
    rep["cache"] = str(cache)
    rep["unbound_cache_accepted"] = accepted_unbound or "⚠_unbound_cache_accepted" in json.loads(idf.read_text())
    order = np.argsort(freqs)
    np.savetxt(out + "_freqs.txt", np.column_stack([freqs[order], ov[order]]), fmt="%.3f %.4f",
               header="phonon frequencies cm^-1 (negative = imaginary) · translation overlap (>= 0.9 = 병진)")
    Path(out + "_summary.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n")
    return rep


def main():
    if "--selftest" in sys.argv[1:]:
        return _selftest()
    ap = argparse.ArgumentParser()
    ap.add_argument("--xyz", required=True)
    ap.add_argument("--out", default="b2o3_phonon")
    ap.add_argument("--delta", type=float, default=0.02)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--require_fmax", type=float, default=0.01,
                    help="입력 구조 원자 힘 최대 상한 eV/Å (기본 0.01 · 0 = 검사 안 함)")
    ap.add_argument("--accept_unbound_cache", action="store_true",
                    help="정체성 없는 옛 캐시를 쓴다 (표시됨 · 기본은 멈춤)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    atoms = read(args.xyz)
    calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device=args.device),
                              task_name="omat")
    rep = phonon_report(atoms, calc, args.out, delta=args.delta, model="uma-s-1p1/omat",
                        accept_unbound_cache=args.accept_unbound_cache, require_fmax=args.require_fmax)
    print(f"n_modes={rep['n_modes']}  병진 {rep['n_translational']}  "
          f"비병진 허수: < {ALARM_CM:g} {rep['n_nontrans_below_alarm']} · "
          f"{ALARM_CM:g}..{SOFT_CM:g} {rep['n_nontrans_soft']}")
    print("lowest 12 non-translational cm^-1:", rep["lowest_nontrans_cm"])
    for n in rep["notes"]:
        print("  ⚠", n)
    print("verdict:", rep["verdict"])
    print(f"-> {args.out}_freqs.txt · {args.out}_summary.json")
    return 0


def _selftest():
    """해석 퍼텐셜 (원자 둘 · 결합 방향 k_x · 옆 방향 k_t) 로 판정 · 캐시 결박을 본다 — UMA 없이."""
    import tempfile
    from ase import Atoms
    from ase.calculators.calculator import Calculator, all_changes
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1; ok[1] += bool(c)
        print(("  ✔ " if c else "  ✘ ") + m)

    class Pair(Calculator):
        implemented_properties = ["energy", "forces"]

        def __init__(self, kx, kt, d0=2.0, **kw):
            super().__init__(**kw)
            self.kx, self.kt, self.d0, self.calls = kx, kt, d0, 0

        def calculate(self, atoms=None, properties=("energy",), system_changes=all_changes):
            super().calculate(atoms, properties, system_changes)
            self.calls += 1
            p = self.atoms.get_positions()
            d = p[1] - p[0]
            e = 0.5 * self.kx * (d[0] - self.d0) ** 2 + 0.5 * self.kt * (d[1] ** 2 + d[2] ** 2)
            g = np.array([self.kx * (d[0] - self.d0), self.kt * d[1], self.kt * d[2]])
            self.results = {"energy": e, "forces": np.array([g, -g])}

    def dimer():
        a = Atoms("XX", positions=[[5.0, 5.0, 5.0], [7.0, 5.0, 5.0]], cell=[20, 20, 20], pbc=True)
        a.set_masses([50.0, 50.0])
        return a

    mu = 25.0
    k_of = lambda cm: np.sign(cm) * mu * (abs(cm) / 521.4709) ** 2     # ω (cm⁻¹) = 521.47 √(k/μ)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        r_st = phonon_report(dimer(), Pair(5.0, k_of(74.0)), td / "st", model="pair")
        chk(r_st["verdict_code"] == "STABLE" and r_st["n_translational"] == 3,
            f"[양성] 실수 모드만 → STABLE · 병진 3 개를 고유벡터로 찾는다 ({r_st['verdict'][:40]})")
        r_soft = phonon_report(dimer(), Pair(5.0, k_of(-20.0)), td / "soft", model="pair")
        low = sorted(np.loadtxt(td / "soft_freqs.txt")[:, 0])
        chk(r_soft["verdict_code"] == "SOFT" and r_soft["n_nontrans_soft"] == 2 and r_soft["n_nontrans_below_alarm"] == 0,
            f"⛔음성: 비병진 허수 −20 cm⁻¹ 둘 → **SOFT (보류)** — 옛 판은 '−30 아래 0 개 → DYNAMICALLY STABLE' (실제 {r_soft['verdict'][:30]})")
        chk(low[0] < -15 and low[1] < -15,
            "⛔음성: 정렬 첫 셋을 버리면 허수 둘이 사라지는 꼴이다 — 이 판정은 고유벡터로 병진을 가려 안 지운다")
        r_un = phonon_report(dimer(), Pair(5.0, k_of(-100.0)), td / "un", model="pair")
        chk(r_un["verdict_code"] == "UNSTABLE" and r_un["n_nontrans_below_alarm"] == 2,
            f"⛔음성: −100 cm⁻¹ 둘 → UNSTABLE (실제 {r_un['verdict'][:30]})")
        # 캐시 결박
        c1 = Pair(5.0, k_of(74.0))
        phonon_report(dimer(), c1, td / "cache", model="pair")
        c2 = Pair(5.0, k_of(74.0))
        phonon_report(dimer(), c2, td / "cache", model="pair")
        chk(c1.calls > 2 and c2.calls == 1,
            f"[양성] 같은 정체성이면 캐시를 다시 쓴다 (힘 계산 {c1.calls} → {c2.calls} = 입력 힘 검사 1 회뿐)")
        moved = dimer(); moved.positions[1, 1] += 0.3                     # 다른 좌표 (안장점 쪽)
        for label, fn in (("좌표", lambda: phonon_report(moved, Pair(5.0, k_of(-100.0)), td / "cache", model="pair")),
                          ("δ 0.01", lambda: phonon_report(dimer(), Pair(5.0, k_of(74.0)), td / "cache", delta=0.01, model="pair")),
                          ("모델", lambda: phonon_report(dimer(), Pair(5.0, k_of(74.0)), td / "cache", model="other"))):
            try:
                fn(); ok_ = False
            except SystemExit:
                ok_ = True
            chk(ok_, f"⛔음성: 같은 --out 에 **{label}** 이 다르면 옛 힘을 쓰지 않고 멈춘다 (Codex 재현: 힘 계산 0 회 · 옛 스펙트럼)")
        (td / "cache_cache.identity.json").unlink()
        try:
            phonon_report(dimer(), Pair(5.0, k_of(74.0)), td / "cache", model="pair"); ok_ = False
        except SystemExit:
            ok_ = True
        c3 = Pair(5.0, k_of(74.0))
        r3 = phonon_report(dimer(), c3, td / "cache", model="pair", accept_unbound_cache=True)
        chk(ok_ and c3.calls <= 1 and r3["verdict_code"] == "STABLE" and r3["unbound_cache_accepted"],
            "⛔음성: 정체성 없는 옛 캐시는 멈춘다 · --accept_unbound_cache 로만 쓴다")
        off = dimer(); off.positions[1, 0] += 0.1                          # 정지점에서 0.1 Å 늘림 → 힘 0.5 eV/Å
        try:
            phonon_report(off, Pair(5.0, k_of(74.0)), td / "off", model="pair"); ok_ = False
        except SystemExit:
            ok_ = True
        r_off = phonon_report(off, Pair(5.0, k_of(74.0)), td / "off0", model="pair", require_fmax=0)
        chk(ok_ and r_off["input_fmax_eV_A"] > 0.4,
            "⛔음성: 입력 힘이 fmax 0.01 보다 크면 멈춘다 (정지점이 아닌 구조의 포논 · Codex DU Q9) · 0 이면 명시적으로 끈다")

        # Codex DV P1-3 재현: 이중 우물 (옆 방향 dy = 0 안장점 A · dy = ±0.5 최소점 B — 둘 다 힘 0)
        class DW(Calculator):
            implemented_properties = ["energy", "forces"]

            def calculate(self, atoms=None, properties=("energy",), system_changes=all_changes):
                super().calculate(atoms, properties, system_changes)
                p = self.atoms.get_positions(); d = p[1] - p[0]
                a, y0 = 0.5, 0.5
                e = 0.5 * 5.0 * (d[0] - 2.0) ** 2 + a * (d[1] ** 2 - y0 ** 2) ** 2 + 0.5 * 0.5 * d[2] ** 2
                g = np.array([5.0 * (d[0] - 2.0), 4 * a * d[1] * (d[1] ** 2 - y0 ** 2), 0.5 * d[2]])
                self.results = {"energy": e, "forces": np.array([g, -g])}

        sA = dimer()
        sB = dimer(); sB.positions[1, 1] += 0.5
        rA = phonon_report(sA, DW(), td / "dw", model="dw")
        for f in (td / "dw_cache").iterdir():
            f.unlink()                                                     # 힘 캐시만 비움 · 정체성 파일은 남김
        rB = phonon_report(sB, DW(), td / "dw", model="dw")
        try:
            phonon_report(sA, DW(), td / "dw", model="dw"); ok_ = False
        except SystemExit:
            ok_ = True
        chk(rA["verdict_code"] == "UNSTABLE" and rB["verdict_code"] == "STABLE" and ok_,
            "⛔음성: 안장점 A → 캐시만 비움 → 최소점 B → 다시 A 는 **멈춘다** (B 의 힘으로 거짓 STABLE 이 나오지 않는다 · Codex DV P1-3)")
    print("  " + ("✅ selftest 통과" if ok[0] == ok[1] else f"⛔ selftest 실패 {ok[0] - ok[1]}/{ok[0]}"))
    return 0 if ok[0] == ok[1] else 1


if __name__ == "__main__":
    sys.exit(main())
