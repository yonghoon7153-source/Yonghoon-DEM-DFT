#!/usr/bin/env python3
"""melt_quench_uma.py — LPSCl@Li₂S **1층**: 비정질 계면상 후보를 UMA NPT melt-quench 로 만들고 판정 지표를 찍는다.

카드: db/properties/lpscl_li2s_interphase_prereg_2026_09_11.json
      §2 ⭐_1층_개정_2026_09_11b (타깃·판정 지표) · §4 ⭐_1층_게이트 G1–G4

후보 (조성은 복합체 x 와 무관 — LPSCl 1 f.u. → Li₃PS₄ + LiCl, Li₂S 는 소모되지 않는다)
  A              Li₄PS₄Cl × n_fu(40) = 400 원자   a-Li₃PS₄·LiCl 균질 (Cl 이 유리망 안에)
  B              Li₃PS₄  × n_fu(50) = 400 원자   a-Li₃PS₄ 단독 (Cl 은 결정 LiCl 로 빠졌다는 가정)
  control_li7ps6 Li₇PS₆  × n_fu(28) = 392 원자   대조잡 — 1저자 원가설. 스스로 Li₃PS₄-like + Li₂S-like 로 갈라지나

절차 (G2 담금질 속도 선언 · G3 시드 ≥ 5 · G4 NPT 0 GPa, 밀도는 결과)
  ① 무작위 셀 — PS₄ 사면체(P–S 2.05 Å)를 **단위로** 무작위 배치(무작위 회전) + 자유 S·Li·Cl 무작위, 서로 다른 원자쌍 최소거리
     2.0 Å, 시작 밀도 1.2 g/cm³ (NPT 가 고친다)
  ② 짧은 FIRE 완화 (fmax 1.0 eV/Å · ≤ 200 스텝) — 겹침만 푼다
  ③ NPT Berendsen 0 GPa: T_melt(1200 K) 유지 --melt_ps → **선형 담금질** T_melt → T_final(300 K), 속도 --quench_rate [K/s]
     (10¹² K/s 면 900 ps) → T_final 유지 --hold_ps
  ④ 최종 FIRE 완화 (fmax 0.05) → final.xyz + final.vasp (VESTA 규율: xyz+POSCAR 쌍) + traj.xyz(--save_ps 간격) + result.json

판정 지표 (문턱은 카드에 있다 — 이 도구는 **값만 찍는다**)
  · PS₄ 보존율 = P 중 S 이웃(≤ 2.6 Å)이 정확히 4개인 비율 · P–S–P 가교 S 수 · P–P(≤ 2.4 Å) 수
  · Cl 환경 = Cl 의 Li 배위수(≤ 3.0 Å) 분포 · 6-배위 분율 · Cl–Cl 최근접 거리 분포와 3.4–3.9 Å 창 분율
  · Li₂S 국소질서 = S 중 Li 이웃(≤ 2.8 Å)이 8개 이상인 비율
  · 밀도 · 부분 g(r) (P–S · S–S · Li–S · Li–Cl · Cl–Cl) → Origin-ready CSV

⛔ 이 도구가 못 하는 것
  · 판정하지 않는다 — 지표를 찍고, 문턱 대조는 카드·사람이 한다.
  · UMA 오차를 모른다 — G1(QE 단일점 대조)은 별도 도구·별도 잡이다.
  · 담금질 속도가 물리적으로 타당한지 보증 못 한다 — 선언하고 기록할 뿐이다 (G2).
  · 결정화 여부를 못 가른다 — g(r)·배위수만 준다. XRD 지문은 tools/xrd/phase_fingerprint.py.
  · 2층(전도)을 하지 않는다 — 최종 구조를 넘길 뿐이다. 시드 하나만 돌리며, 앙상블 통계는 호출자가 모은다 (G3).
  · Berendsen 은 앙상블이 엄밀하지 않다 — 구조 생성용이지 수송 계산용이 아니다.
  · **밀도가 낮게 나온 원인을 스스로 못 가른다** — 배선인지 UMA·구조인지는 --npt_control 대조 잡이 가른다.
    그 대조도 "배로스탯이 ρ_UMA(0K) 를 지키나" 까지만 말한다. UMA 자신의 밀도 오차는 그 판정 밖이다.

  python3 tools/ionic/melt_quench_uma.py --system A --seed 1 --quench_rate 1e12 --out_root /data/work/runs/li2s_layer1
  python3 tools/ionic/melt_quench_uma.py --npt_control db/structures/sei_li2s_mp-1153.vasp --out_root /data/work/runs/li2s_layer1
  python3 tools/ionic/melt_quench_uma.py --seed_gate <run_dir> [<run_dir> ...]   # 시드 게이트 입력 · 원시/relax 두 판 · md_init_raw.xyz
  python3 tools/ionic/melt_quench_uma.py --melt_window_check <run_dir>   # li2s-2 녹음 판정 (창 안 원점 · 0 통과 · 2 미충족 · 3 미완 · 4 무효)
  python3 tools/ionic/melt_quench_uma.py --stage1_verdict <run_dir> …    # li2s-2 1 단계 시드 판정 (카드 필드 직접 · stage1_verdict.json)
  python3 tools/ionic/melt_quench_uma.py --stage1_summary <out_root>     # li2s-2 1 단계 묶음 판정 · 2 단계 시드 (stage1_summary.json)
    ⭐ 회신 DG (2026-11-03): 시드 판정에 원자료 · 카드 값 · 도구 지문 · 최종 구조 대조 · 첫 시드 녹음 미충족 = closes_system ·
       묶음은 지문을 다시 재고 선언된 시드 전부 판정 끝 · 비용 장부 상한 · 카드 값 검사 (validate_li2s2_values)
    ⭐ 회신 DH (2026-11-03): --run_id (러너가 주는 실행 식별자 → plan.json) · 시드 판정 = 폴더 (계, 시드) · plan · run_id 대조 ·
       판정을 덮어쓰기 전에 이전 판정 전체 · 지문 변화 · 사유를 stage1_verdict_history.jsonl 에 · 묶음은 장부를 판정과 대조
       (ledger_check: 누락 · 음수 · 근거 없음 · run_id 중복 · 다른 시드 = 무효 · 안 끝난 런 = 대기)
  python3 tools/ionic/melt_quench_uma.py --selftest

⚠ final.xyz 는 **relax 본**이다 (④ · plan.json 게이트_입력.final_relax). 담금질 원시는 traj.xyz 마지막 프레임뿐이고,
  `--seed_gate` 가 그것을 md_init_raw.xyz 로 뽑는다. (2026-09-24 — 카드 문구가 반대로 적은 적이 있다)

⭐ 2026-11-03 `--fix_density ρ` (li2s-2 카드 db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json §1b):
  ③ 을 **NVT** 로 바꾼다 — 열욕은 NVTBerendsen 에 같은 taut (BARO taut_fs) · 바로스탯만 없다. melt 첫 --compress_ps 동안
  시작 밀도 → ρ 로 **밀도에 선형으로 등방 압축** (50 스텝마다 셀·좌표를 같이 늘임) 한 뒤 나머지 melt · 담금질 · 유지는 ρ 고정.
  plan.json 게이트_입력 의 앙상블이 NVT 로 내려가고 `--gate_check` 는 압력 대신 **밀도 = ρ** 를 본다 (압력은 기록).
  ⛔ 못 하는 것: 고정 밀도라 UMA 셀에 남는 내부 압력을 없애지 않는다 (thermo.csv P 로 **기록만**) · ρ 가 물리적으로
     맞는지 모른다 (목표 밀도는 카드가 정한다) · 압축 중 겹침을 따로 막지 않는다 (1200 K 액체에서 압축한다 — melt_check 가
     압축 **뒤** 반쪽 창 [melt_ps/2, melt_ps] 에서 골격 확산을 본다) · 옵션을 안 주면 옛 NPT 경로와 바이트까지 같은 동작이다.
"""
from __future__ import annotations
import argparse
import base64, datetime, hashlib, json, math, numbers, os, pathlib, re, sys, time
import numpy as np

MASS = {"Li": 6.94, "P": 30.974, "S": 32.06, "Cl": 35.45}
EV_A3_TO_GPA = 160.21766208
# ⭐ 배로스탯 설정은 여기 한 곳에만 있다 — 대조 잡(--npt_control)이 생산 런과 **같은 설정**을 쓰지 않으면
#    아무것도 증명하지 못한다. 바꾸려면 여기서 바꾸고, 두 경로가 같이 따라간다.
BARO = {"taut_fs": 100.0, "taup_fs": 1000.0, "compressibility_au": 8.0}   # 8.0 Å³/eV ≈ 1/(20 GPa)
# ⭐ 앙상블 **선언** — G4("담금질은 NPT(0 GPa)")가 읽을 값이다. 실제로 쓰는 자리(run_melt_quench)와
#    같은 상수에서 plan.json 으로 내려가고, --gate_check 가 그것을 다시 읽어 thermo.csv 와 대조한다.
#    2026-09-14 추가: 이 필드가 없어서 seed1 의 앙상블을 thermo 에서 **역추적**해야 했다 —
#    게이트가 읽을 값이 기록에 없는 것은 9/13 에 부류로 정리한 '조용히 틀린 경로' 다.
ENSEMBLE = {"ensemble": "NPT", "thermostat": "Berendsen", "barostat": "Berendsen",
            "target_pressure_GPa": 0.0, "barostat_params": dict(BARO),
            "⛔_엄밀성": "Berendsen 은 부피 변동을 정확한 NPT 분포로 표본화하지 않는다 "
                        "(Bernetti–Bussi 2020) — 구조 생성용이지 앙상블 통계용이 아니다."}
def ensemble_fixed_density(rho_g_cm3, compress_ps):
    """`--fix_density` 의 앙상블 **선언** — ENSEMBLE 과 같은 자리 (plan.json 게이트_입력) 로 내려간다.
    읽는 곳: `gate_check` (ensemble == "NVT" 면 압력 대신 밀도를 본다)."""
    return {"ensemble": "NVT", "thermostat": "Berendsen", "barostat": None,
            "target_density_g_cm3": float(rho_g_cm3),
            "thermostat_params": {"taut_fs": BARO["taut_fs"]},
            "compress": {"over_ps": float(compress_ps), "kind": "등방 · 밀도에 선형 · melt 첫 구간 · 50 스텝마다"},
            "⛔_엄밀성": "고정 밀도 — 내부 압력은 결과다 (thermo.csv P · 기록만). Berendsen 열욕은 구조 생성용."}


def validate_fix_density(rho_g_cm3, compress_ps, melt_ps):
    """`--fix_density` 입력 검사 — 틀리면 시작하지 않는다 (조용히 고치지 않는다)."""
    if rho_g_cm3 is None:
        return
    if not (rho_g_cm3 > 0 and math.isfinite(rho_g_cm3)):
        raise SystemExit(f"⛔ --fix_density 는 양수여야 한다 (받은 값 {rho_g_cm3})")
    if not (compress_ps > 0 and math.isfinite(compress_ps)):
        raise SystemExit(f"⛔ --compress_ps 는 양수여야 한다 (받은 값 {compress_ps})")
    if compress_ps > melt_ps:
        raise SystemExit(f"⛔ --compress_ps {compress_ps} 가 --melt_ps {melt_ps} 보다 길다 — 압축은 melt 안에서 끝나야 한다")
    if compress_ps > melt_ps / 2.0 + 1e-9:   # 회신 DF Q-DF-8 — 녹음 판정 창 [melt/2, melt] 과 겹치지 않게
        raise SystemExit(f"⛔ --compress_ps {compress_ps} 가 녹음 판정 창 시작 (melt_ps/2 = {melt_ps/2:g} ps) 보다 늦게 끝난다 — "
                         "압축은 판정 창 전에 끝나야 한다")


def scale_to_density(atoms, rho_g_cm3):
    """셀과 좌표를 같이 등방으로 늘여 밀도를 ρ 로 맞춘다 (속도는 그대로). 맞춘 밀도를 돌려준다."""
    s = (density_g_cm3(atoms) / float(rho_g_cm3)) ** (1.0 / 3.0)
    atoms.set_cell(np.asarray(atoms.get_cell()) * s, scale_atoms=True)
    return density_g_cm3(atoms)


FINAL_RELAX = {"kind": "FIRE", "fmax_eV_A": 0.05, "cell": "fixed",
               "⛔": "밀도는 **마지막 NPT 셀**의 값이고 구조 지표는 그 셀을 고정한 완화 구조의 값이다 "
                     "(개정 ③ — '300 K 평형 유리의 평균값' 이 아니다)."}
FINAL_RELAX_NVT = {"kind": "FIRE", "fmax_eV_A": 0.05, "cell": "fixed",
                   "⛔": "밀도는 **고정 밀도 셀** (NVT · 카드 목표 ρ) 의 값이고 구조 지표는 그 셀을 고정한 완화 구조의 값이다 "
                         "('300 K 평형 유리의 평균값' 이 아니다 · 회신 DG P2 — NVT plan 에 'NPT 셀' 이라 적던 것)."}


def final_relax_decl(fix_density=None):
    """plan.json 게이트_입력.final_relax — 앙상블에 맞는 설명 (FIRE 설정은 같다)."""
    return FINAL_RELAX if fix_density is None else FINAL_RELAX_NVT
BAND_CARD = "db/properties/lpscl_li2s_layer1_amendment_2026_09_12.json"
BAND_PATH = ("1_바꾸는_것", "⑤_밴드_산수_정정")   # → 중심 · 밴드_±15%
P_TOL_GPA = 0.10        # --gate_check: |⟨P⟩| 허용 (npt_control 의 --control_p_tol 과 같은 눈금)
SYSTEMS = {                       # 식단위 조성 · 기본 n_fu
    "A":              ({"Li": 4, "P": 1, "S": 4, "Cl": 1}, 40),
    "B":              ({"Li": 3, "P": 1, "S": 4, "Cl": 0}, 50),
    "control_li7ps6": ({"Li": 7, "P": 1, "S": 6, "Cl": 0}, 28),
}
PS_BOND = 2.05          # Å — PS₄ 단위 초기 P–S
MIN_DIST = 2.0          # Å — Li 가 낀 쌍의 최소거리
MIN_DIST_ANION = 3.0    # Å — P·S·Cl 끼리(다른 단위) 최소거리: P 에 제3의 S 가 2.6 Å 안에 못 들어온다 (PS₄ 보존율 정의와 정합)
R_PS, R_PP, R_CLLI, R_SLI = 2.6, 2.4, 3.0, 2.8     # 지표 컷오프 (카드 §2 판정_지표)
CLCL_WIN = (3.4, 3.9)   # LiCl 결정 Cl–Cl 3.63 Å 창

# ───────────────────────── 기하 유틸 (numpy · MIC · 직교/비직교 셀) ─────────────────────────
def mic_dists(A, B, cell):
    """A(n,3) 와 B(m,3) 사이 최소상 거리 행렬 (n,m)."""
    cinv = np.linalg.inv(cell)
    d = A[:, None, :] - B[None, :, :]
    f = d @ cinv
    f -= np.round(f)
    return np.linalg.norm(f @ cell, axis=2)


def counts_within(A, B, cell, rcut, exclude_self=False):
    D = mic_dists(A, B, cell)
    if exclude_self:
        np.fill_diagonal(D, np.inf)
    return (D <= rcut).sum(axis=1), D


# ───────────────────────── ① 무작위 셀 ─────────────────────────
def _tetra_vertices(rng):
    """정사면체 4 꼭짓점(단위벡터)에 무작위 회전."""
    v = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float) / math.sqrt(3)
    q = rng.normal(size=4); q /= np.linalg.norm(q)            # 무작위 단위 사원수 → 회전행렬
    a, b, c, d = q
    R = np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                  [2*(b*c+a*d), a*a-b*b+c*c-d*d, 2*(c*d-a*b)],
                  [2*(b*d-a*c), 2*(c*d+a*b), a*a-b*b-c*c+d*d]])
    return v @ R.T


def build_random_cell(system, seed, density_g_cm3=1.2, n_fu=None, min_dist=MIN_DIST, max_tries=60000):
    """PS₄ 단위 + 자유 원자를 무작위로 채운 입방 셀. → (symbols list, positions (N,3), cell (3,3))"""
    if system not in SYSTEMS:
        raise SystemExit(f"⛔ 모르는 계 {system!r} — 카드에 있는 것: {sorted(SYSTEMS)}")
    comp, n_default = SYSTEMS[system]
    n_fu = int(n_fu or n_default)
    counts = {k: v * n_fu for k, v in comp.items() if v}
    mass_g = sum(MASS[k] * v for k, v in counts.items()) / 6.02214076e23
    L = (mass_g / density_g_cm3 * 1e24) ** (1.0 / 3.0)                 # Å
    cell = np.eye(3) * L
    rng = np.random.default_rng(seed)
    n_P = counts.get("P", 0)
    n_S_free = counts.get("S", 0) - 4 * n_P
    if n_S_free < 0:
        raise SystemExit(f"⛔ S 가 PS₄ 를 만들기에 모자란다 ({counts})")
    sym, pos = [], []
    def ok(new, new_sym):
        if not pos:
            return True
        D = mic_dists(np.asarray(new), np.asarray(pos), cell)
        heavy_new = np.array([s != "Li" for s in new_sym])[:, None]
        heavy_old = np.array([s != "Li" for s in sym])[None, :]
        need = np.where(heavy_new & heavy_old, MIN_DIST_ANION, min_dist)
        return bool((D >= need).all())
    tries = 0
    for _ in range(n_P):                                                 # PS₄ 단위
        while True:
            tries += 1
            if tries > max_tries:
                raise SystemExit(f"⛔ {system} 밀도 {density_g_cm3} g/cm³ 에 {max_tries}회 안에 못 채웠다 — 밀도를 낮춰라")
            p = rng.uniform(0, L, 3)
            unit = np.vstack([p, p + PS_BOND * _tetra_vertices(rng)])
            if ok(unit, ["P", "S", "S", "S", "S"]):
                sym += ["P", "S", "S", "S", "S"]; pos += unit.tolist(); break
    for el, n in (("S", n_S_free), ("Cl", counts.get("Cl", 0)), ("Li", counts.get("Li", 0))):
        for _ in range(n):
            while True:
                tries += 1
                if tries > max_tries:
                    raise SystemExit(f"⛔ {system} 밀도 {density_g_cm3} g/cm³ 에 {max_tries}회 안에 못 채웠다 — 밀도를 낮춰라")
                p = rng.uniform(0, L, 3)
                if ok([p], [el]):
                    sym.append(el); pos.append(p.tolist()); break
    return sym, np.asarray(pos), cell


# ───────────────────────── 판정 지표 ─────────────────────────
def indicators(sym, pos, cell):
    sym = np.asarray(sym); pos = np.asarray(pos, float); cell = np.asarray(cell, float)
    P = pos[sym == "P"]; S = pos[sym == "S"]; Li = pos[sym == "Li"]; Cl = pos[sym == "Cl"]
    out = {}
    if len(P) and len(S):
        nS, D_PS = counts_within(P, S, cell, R_PS)
        out["PS4_fraction"] = float((nS == 4).mean())
        out["P_S_coord_hist"] = {int(k): int(v) for k, v in zip(*np.unique(nS, return_counts=True))}
        nP_per_S = (D_PS.T <= R_PS).sum(axis=1)
        out["bridging_S_P2S7_like"] = int((nP_per_S >= 2).sum())
        nPP, _ = counts_within(P, P, cell, R_PP, exclude_self=True)
        out["P_P_bonds_P2S6_like"] = int(nPP.sum() // 2)
    if len(Cl):
        nLi, _ = counts_within(Cl, Li, cell, R_CLLI) if len(Li) else (np.zeros(len(Cl), int), None)
        out["Cl_Li_coord_hist"] = {int(k): int(v) for k, v in zip(*np.unique(nLi, return_counts=True))}
        out["Cl_6coord_fraction"] = float((nLi == 6).mean())
        if len(Cl) > 1:
            Dcc = mic_dists(Cl, Cl, cell); np.fill_diagonal(Dcc, np.inf)
            nn = Dcc.min(axis=1)
            out["ClCl_nearest_A"] = {"median": float(np.median(nn)), "min": float(nn.min()),
                                     "in_window_fraction": float(((nn >= CLCL_WIN[0]) & (nn <= CLCL_WIN[1])).mean()),
                                     "window_A": list(CLCL_WIN)}
    if len(S) and len(Li):
        nLiS, _ = counts_within(S, Li, cell, R_SLI)
        out["S_Li8_fraction_Li2S_like"] = float((nLiS >= 8).mean())
        out["S_Li_coord_hist"] = {int(k): int(v) for k, v in zip(*np.unique(nLiS, return_counts=True))}
    vol = abs(np.linalg.det(cell))
    if all(x in MASS for x in sym):
        mass_g = sum(MASS[x] for x in sym) / 6.02214076e23
    else:                                    # 카드 밖 원소(B 등) — ASE 질량
        from ase.data import atomic_masses, atomic_numbers
        mass_g = sum(atomic_masses[atomic_numbers[x]] for x in sym) / 6.02214076e23
    out["density_g_cm3"] = float(mass_g / (vol * 1e-24))
    out["n_atoms"] = int(len(sym)); out["cell_A"] = cell.tolist()
    return out


def partial_gr(sym, pos, cell, pairs=(("P", "S"), ("S", "S"), ("Li", "S"), ("Li", "Cl"), ("Cl", "Cl")), rmax=8.0, dr=0.05):
    sym = np.asarray(sym); pos = np.asarray(pos, float); vol = abs(np.linalg.det(cell))
    edges = np.arange(0, rmax + dr, dr); rc = 0.5 * (edges[1:] + edges[:-1])
    cols = {"r_A": rc}
    for a, b in pairs:
        A = pos[sym == a]; B = pos[sym == b]
        if not len(A) or not len(B):
            continue
        D = mic_dists(A, B, cell)
        if a == b:
            np.fill_diagonal(D, np.inf)
        h, _ = np.histogram(D[D < rmax], bins=edges)
        shell = 4 * math.pi * rc ** 2 * dr
        cols[f"g_{a}{b}"] = h / (len(A) * len(B) / vol) / shell
    return cols


# ───────────────────────── ③ MD ─────────────────────────
def make_calc(device="cuda", turbo=False):
    """UMA-s-1p1 · omat. turbo=True 면 fairchem 의 MD 용 inference_settings="turbo" 를 시도한다
    (원자 수·조성이 고정된 MD 전용 · 보통 ~2배). 이 fairchem 판에 없으면 **기본으로 내려가고 화면에 적는다** —
    조용히 다른 설정으로 돌지 않는다 (결과 파일 plan.json 에 실제 모드를 남긴다)."""
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    mode = "default"
    if turbo:
        try:
            pu = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device, inference_settings="turbo"); mode = "turbo"
        except Exception as e:
            print(f"⚠ turbo 불가 ({type(e).__name__}: {e}) — 기본 모드로 돈다")
            pu = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)
    else:
        pu = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)
    calc = FAIRChemCalculator(pu, task_name="omat"); calc._mq_mode = mode
    return calc


def pressure_GPa(atoms, include_ideal_gas=True):
    """순간 압력 [GPa] = -tr(σ)/3.

    ⛔ 기본으로 **운동 항(ideal-gas)을 포함한다** — ASE 의 NPTBerendsen 이 제어하는 양이 그것이다.
    virial 만 찍으면 81원자·300 K·1283 Å³ 에서 NkT/V = 0.26 GPa 를 빠뜨려, 목표가 0 GPa 인데
    −0.30 으로 보인다. 2026-09-12 에 그 때문에 **배로스탯이 고장난 줄 알았다** (실제 총 압력은
    −0.05 GPa 로 정상이었다). 응력을 못 주는 계산기면 0 이 아니라 NaN.
    """
    try:
        try:
            sig = np.asarray(atoms.get_stress(voigt=True, include_ideal_gas=include_ideal_gas), float)
            return float(-(sig[0] + sig[1] + sig[2]) / 3.0 * EV_A3_TO_GPA)
        except TypeError:                                   # 구버전 ASE — 손으로 더한다
            sig = np.asarray(atoms.get_stress(voigt=True), float)
            P = -(sig[0] + sig[1] + sig[2]) / 3.0 * EV_A3_TO_GPA
            if include_ideal_gas:                           # P_kin = (2/3)·E_kin/V = NkT/V
                P += 2.0 / 3.0 * atoms.get_kinetic_energy() / atoms.get_volume() * EV_A3_TO_GPA
            return float(P)
    except Exception:
        return float("nan")


def cell_widths_A(cell):
    """셀의 **면간거리** (각 축에 수직인 폭) = V / |a_j × a_k|.

    ⛔ 원자 수가 아니라 이 값이 MIC 의 기준이다 — 이게 컷오프보다 작으면 원자가 자기 이미지를
    본다. primitive 셀은 원자 수가 같아도 폭이 훨씬 작다 (2026-09-12: Li₂S primitive ×2³ 는
    24 원자에 폭 6.6 Å 였고, 나는 conventional 을 가정해 96 원자로 알고 있었다).
    """
    C = np.asarray(cell, float)
    V = abs(np.linalg.det(C))
    return np.array([V / np.linalg.norm(np.cross(C[(i + 1) % 3], C[(i + 2) % 3])) for i in range(3)])


def auto_repeat(cell, min_width_A):
    """각 축 면간거리가 min_width 이상이 되도록 필요한 반복수 (1 이상)."""
    w = cell_widths_A(cell)
    return tuple(int(max(1, math.ceil(min_width_A / x - 1e-9))) for x in w)


def density_g_cm3(atoms):
    """g/cm³. 카드 밖 원소(대조 잡에 아무 결정이나 넣을 수 있다)는 ASE 질량으로 — MASS 는 4원소뿐이라
    예전 같으면 KeyError 로 죽었다. 생산 런 경로는 MASS 를 그대로 쓰므로 숫자가 안 바뀐다."""
    sy = atoms.get_chemical_symbols()
    m = sum(MASS[x] for x in sy) if all(x in MASS for x in sy) else float(atoms.get_masses().sum())
    return float(m / 6.02214076e23 / (atoms.get_volume() * 1e-24))


def _flushing_print(*a, **k):
    print(*a, **k); sys.stdout.flush()          # ⛔ 로그 리다이렉트 시 블록 버퍼링 (CLAUDE.md 규율)


def run_npt_control(atoms, calc, out, *, T_K, ps, dt_fs, save_ps=1.0, tol=0.03, p_tol=0.10,
                    min_width_A=9.0, cell_relax=True, max_relax_dV=0.10, log=_flushing_print):
    """⭐ 배로스탯 **대조 잡** — 알려진 결정을 같은 NPT 배선에 넣어 밀도를 지키는지 본다.

    비정질 밀도가 낮게 나왔을 때 원인이 두 갈래다: (ⓐ 우리 배선·단위가 틀렸다 / ⓑ UMA 또는 구조가 그렇다).
    이 잡이 그 둘을 가른다 — 결정을 **UMA 0 K 가변셀로 먼저 완화**해 ρ_UMA(0K) 를 얻고(= UMA 자신의 답),
    그 구조로 **생산 런과 같은 BARO 설정** NPT 를 돌려 ρ_NPT 를 얻는다.
      · **판정은 압력이다**: |⟨P_total⟩| ≤ p_tol (기본 0.10 GPa) 이면 배로스탯이 목표를 지킨다.
      · 밀도 drift(0 K → T_K)는 **열팽창이라 판정이 아니다** — 관측값으로만 적는다.
        2026-09-12 에 drift 3 % 를 배선 고장으로 읽은 적이 있다(실제 총 압력 −0.02 GPa).
    ρ_UMA(0K) 와 파일 밀도의 차이는 **UMA 자신의 오차**라 tol 판정에 넣지 않는다 — 따로 찍어서 사람이 본다.
    """
    from ase import units
    from ase.md.nptberendsen import NPTBerendsen
    from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary
    from ase.io import write
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    w0 = cell_widths_A(atoms.get_cell())
    log(f"  [대조] {len(atoms)} 원자 · 면간거리 {w0[0]:.2f}/{w0[1]:.2f}/{w0[2]:.2f} Å (최소 {w0.min():.2f})")
    if w0.min() < min_width_A:
        log(f"  ⚠ 최소 면간거리 {w0.min():.2f} Å < {min_width_A} Å — MIC 여유가 얇다. "
            f"drift 가 문턱 근처로 나오면 배로스탯 탓인지 셀 탓인지 **못 가른다**.")
    atoms.calc = calc
    rho_file = density_g_cm3(atoms)
    ind_file = indicators(atoms.get_chemical_symbols(), atoms.get_positions(), np.asarray(atoms.get_cell()))
    rho_0K = P_0K = None; relax_note = "skipped"
    if cell_relax:
        try:
            from ase.filters import FrechetCellFilter as _CF
        except ImportError:
            from ase.constraints import ExpCellFilter as _CF        # 구버전 ASE
        from ase.optimize import LBFGS
        # ⛔ FIRE + 셀 필터는 셀 자유도에 큰 걸음을 내딛어 발산한다 (2026-09-12: Li₆PS₅Cl 이
        #    부피 +34 %, a 10.25 → 11.3 Å). LBFGS + maxstep 제한으로 바꿨다.
        opt = LBFGS(_CF(atoms), logfile=str(out / "cellrelax.log"), maxstep=0.05)
        opt.run(fmax=0.02, steps=500)
        rho_0K = density_g_cm3(atoms); P_0K = pressure_GPa(atoms)
        dV = rho_file / rho_0K - 1.0
        write(str(out / "relaxed_0K.xyz"), atoms, format="extxyz")
        ind_0K = indicators(atoms.get_chemical_symbols(), atoms.get_positions(), np.asarray(atoms.get_cell()))
        relax_note = f"steps={opt.get_number_of_steps()} fmax_reached={opt.converged()}"
        log(f"  [대조] ρ(파일) {rho_file:.3f} → ρ_UMA(0K) {rho_0K:.3f} g/cm³ "
            f"(부피 {100*dV:+.1f} % · P {P_0K:+.3f} GPa · {relax_note})")
        if ind_file.get("PS4_fraction") is not None:
            log(f"  [대조] PS₄ 보존 {ind_file['PS4_fraction']:.3f} → {ind_0K.get('PS4_fraction'):.3f}")
            if ind_0K.get("PS4_fraction", 1.0) < ind_file["PS4_fraction"] - 0.05:
                raise SystemExit("⛔ 0 K 완화에서 PS₄ 가 깨졌다 — 이 구조로는 밀도 대조가 성립하지 않는다. 멈춘다.")
        if abs(dV) > max_relax_dV:
            raise SystemExit(
                f"⛔ 0 K 완화가 부피를 {100*dV:+.1f} % 바꿨다 (허용 ±{100*max_relax_dV:.0f} %) — "
                "**이만큼 움직이면 대조가 아니다**. 시작 구조나 최적화를 먼저 고쳐라. "
                "NPT 만으로 판정하려면 --control_no_cellrelax 를 써라 (그때 기준은 파일 밀도다).")
    else:
        log(f"  [대조] ρ(파일) {rho_file:.3f} g/cm³ · 0 K 완화 건너뜀 — 기준은 **파일 밀도**다")
    MaxwellBoltzmannDistribution(atoms, temperature_K=T_K, rng=np.random.default_rng(0)); Stationary(atoms)
    dt = dt_fs * units.fs
    dyn = NPTBerendsen(atoms, dt, temperature_K=T_K, pressure_au=0.0,
                       taut=BARO["taut_fs"] * units.fs, taup=BARO["taup_fs"] * units.fs,
                       compressibility_au=BARO["compressibility_au"])
    n = int(round(ps * 1000 / dt_fs)); save_int = max(1, int(round(save_ps * 1000 / dt_fs))); _t0 = time.time()
    tlog = open(out / "thermo.csv", "w"); tlog.write("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
    rows = []
    for step in range(n + 1):
        if step % save_int == 0:
            r, P = density_g_cm3(atoms), pressure_GPa(atoms)
            rows.append((step * dt_fs / 1000, r, P))
            tlog.write(f"{step*dt_fs/1000:.3f},{atoms.get_temperature():.1f},{T_K:.1f},{r:.4f},"
                       f"{atoms.get_volume():.2f},{atoms.get_potential_energy():.4f},{P:.4f},"
                       f"{pressure_GPa(atoms, include_ideal_gas=False):.4f}\n"); tlog.flush()
            if step and step % max(save_int, n // 10 or 1) == 0:
                log(f"  [대조] {step*dt_fs/1000:6.2f}/{ps:.0f} ps  ρ {r:.4f}  P {P:+.3f} GPa  "
                    f"({(time.time()-_t0)/60:.1f} min)")
        if step < n:
            dyn.run(1)
    tlog.close()
    half = [x for x in rows if x[0] >= rows[-1][0] / 2] or rows
    rho_npt = float(np.mean([x[1] for x in half])); P_npt = float(np.mean([x[2] for x in half]))
    ref, ref_name = ((rho_0K, "rho_UMA_0K") if rho_0K is not None else (rho_file, "rho_file"))
    drift = rho_npt / ref - 1.0
    res = {"kind": "npt_barostat_control", "T_K": T_K, "ps": ps, "dt_fs": dt_fs, "baro": dict(BARO),
           "cell_widths_A": [float(x) for x in w0], "min_cell_width_A": float(w0.min()),
           "min_width_required_A": min_width_A, "cell_wide_enough": bool(w0.min() >= min_width_A),
           "n_atoms": len(atoms), "composition": {e: atoms.get_chemical_symbols().count(e) for e in sorted(set(atoms.get_chemical_symbols()))},
           "rho_file_g_cm3": rho_file, "rho_UMA_0K_g_cm3": rho_0K, "P_UMA_0K_GPa": P_0K,
           "cell_relax": bool(cell_relax), "cell_relax_note": relax_note,
           "reference_for_drift": ref_name, "PS4_fraction_file": ind_file.get("PS4_fraction"),
           "rho_NPT_mean_last_half_g_cm3": rho_npt, "P_NPT_mean_last_half_GPa": P_npt,
           "drift_vs_UMA_0K": drift, "tol": tol,
           # ⭐ 배선 판정은 **압력**이다 (2026-09-12 재설계). 밀도 drift 로 판정하면 0 K 기준과
           #    300 K MD 사이의 **열팽창**을 배선 고장으로 읽는다 — 실제로 그렇게 오판했다
           #    (Li₂S: drift −3.0 % 인데 총 압력은 −0.02 GPa 로 정상이었다).
           "P_tol_GPa": p_tol, "plumbing_ok": bool(abs(P_npt) <= p_tol),
           "density_drift_is_thermal_expansion": ("0 K 기준 → %.0f K NPT 의 밀도 변화다. "
                                                  "판정이 아니라 관측값이다." % T_K),
           "alpha_V_apparent_per_K": (float(-drift / T_K) if T_K else None),
           "drift_tol_legacy_not_a_gate": True,
           "UMA_vs_file": (rho_0K / rho_file - 1.0) if rho_0K is not None else None,
           "⛔": "판정은 배선(배로스탯·단위)에 한정된다. UMA 자신의 밀도 오차(UMA_vs_file)는 이 판정 밖이다."}
    (out / "control.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    return res


def npt_msd(sym, pos, cells, dt_ps):
    """**NPT** 궤적의 원소별 MSD [Å²]. 셀이 프레임마다 변하므로 분수좌표에서 unwrap 한다.

    NVT 용 도구(framework_site_census.py 등)를 여기 쓰면 안 된다 — 그쪽은 셀이 변하면 멈춘다.
    절차: 분수좌표 차분 → MIC(round 빼기) → 그 프레임 셀로 실공간 증분 → 누적 → **전체 평균
    병진(드리프트) 제거** → 원소별 평균 제곱변위.
    """
    sym = np.asarray(sym); pos = np.asarray(pos, float); cells = np.asarray(cells, float)
    T, N, _ = pos.shape
    frac = np.einsum("tnj,tjk->tnk", pos, np.linalg.inv(cells))
    df = np.diff(frac, axis=0)
    df -= np.round(df)
    steps = np.einsum("tnj,tjk->tnk", df, cells[1:])
    disp = np.concatenate([np.zeros((1, N, 3)), np.cumsum(steps, axis=0)])
    disp -= disp.mean(axis=1, keepdims=True)
    t = np.arange(T) * dt_ps
    return t, {str(e): ((disp[:, sym == e] ** 2).sum(-1)).mean(-1) for e in sorted(set(sym))}


def fit_D(t, msd, t_from, t_to):
    """자유절편 선형맞춤 msd = 6 D t + c → D [cm²/s] (1 Å²/ps = 1e-4 cm²/s)."""
    m = (t >= t_from) & (t <= t_to)
    if m.sum() < 4:
        return None, None
    a, c = np.polyfit(t[m], msd[m], 1)
    return float(a / 6.0 * 1e-4), float(c)


def melt_check(run_dir, *, d_melt_cm2s=1e-6, log=print):
    """⭐ **녹았나** — melt 구간에서 P 골격이 확산했는지 본다 (관측 후 진단, 사전등록 게이트 아님).

    안 녹았으면 담금질은 초기 무작위 충전의 채움밀도를 그대로 얼린 것이고, 그때 밀도는
    물리가 아니라 생성기 설정이다. G4 밴드를 논하기 **전에** 이걸 먼저 가른다.

    ⛔ 못 하는 것: 결정화 여부를 못 본다(g(r)·XRD 가 따로 있다) · 문턱 1e-6 cm²/s 는
    액체/고체를 가르는 **진단값**이고 카드 문턱이 아니다 · 시드 하나로 판정하지 않는다.
    """
    from ase.io import read
    run = pathlib.Path(run_dir)
    plan = json.loads((run / "plan.json").read_text(encoding="utf-8"))
    if plan.get("fix_density_g_cm3") is not None:   # 회신 DF P0 · P2 — 누적 원점 판정 · '밀도는 물리다' 출력이 고정 밀도에 안 맞는다
        raise SystemExit("⛔ 고정 밀도 (--fix_density) 런이다 — 옛 --melt_check (0 ps 누적 원점) 대신 --melt_window_check 를 쓴다")
    frames = read(str(run / "traj.xyz"), index=":")
    if len(frames) < 8:
        raise SystemExit(f"⛔ 프레임이 {len(frames)}개뿐이다 — MSD 를 못 낸다")
    dt_ps = plan["save_ps"] if "save_ps" in plan else None
    if dt_ps is None:                       # 옛 plan.json — 전체 길이에서 유도한다
        total = plan["melt_ps"] + plan["quench_ps"] + plan["hold_ps"]
        dt_ps = total / (len(frames) - 1)
        log(f"  ⚠ plan.json 에 save_ps 가 없다 — 전체 {total:.0f} ps / {len(frames)-1} 구간 = {dt_ps:.3f} ps 로 유도")
    sym = frames[0].get_chemical_symbols()
    pos = np.array([f.get_positions() for f in frames])
    cells = np.array([np.asarray(f.get_cell()) for f in frames])
    t, msd = npt_msd(sym, pos, cells, dt_ps)
    melt_ps = float(plan["melt_ps"])
    half = melt_ps / 2.0
    out = {"kind": "melt_check", "run": str(run), "n_frames": len(frames), "dt_ps": dt_ps,
           "melt_ps": melt_ps, "fit_window_ps": [half, melt_ps], "T_melt_K": plan.get("T_melt_K"),
           "d_melt_threshold_cm2_s": d_melt_cm2s, "per_element": {}}
    for e, m in msd.items():
        i = int(np.searchsorted(t, melt_ps))
        D, c = fit_D(t, m, half, melt_ps)
        out["per_element"][e] = {"msd_at_melt_end_A2": float(m[min(i, len(m) - 1)]),
                                "D_melt_cm2_s": D, "intercept_A2": c}
        log(f"  [melt] {e:2s}  MSD({melt_ps:.0f} ps) {m[min(i,len(m)-1)]:8.2f} Å²  "
            f"D {('%.3e' % D) if D is not None else '—':>10s} cm²/s")
    P = out["per_element"].get("P", {})
    DP = P.get("D_melt_cm2_s")
    out["framework_diffused"] = bool(DP is not None and DP > d_melt_cm2s)
    out["verdict"] = ("melted" if out["framework_diffused"] else "not_melted_framework_frozen")
    out["⛔"] = ("진단이다. 'melted' 가 구조가 좋다는 뜻이 아니고, 'not_melted' 면 그 담금질의 밀도는 "
                 "물리가 아니라 생성기 채움밀도다 — G4 밴드를 논하기 전에 이걸 고친다.")
    return out


# ───────────────────────── li2s-2 (카드 lpscl_glass_dense_window) — 회신 DF P0 · P1-2 · P1-3 · 회신 DG P1-4 · P1-5 · P1-7 ─────────────────────────
#: ⛔ 2026-11-03 회신 DF P0 — 옛 `melt_check` 는 0 ps 부터 **누적한** 변위로 MSD 를 만들고 회귀 점만 [melt/2, melt] 로 잘랐다.
#:   그래서 압축 · 초기 재배열 때 생긴 변위와 뒤 변위의 교차항이 판정에 남는다 (창 좌표가 같아도 이력만 달라 21 배 · 70 ps 에서
#:   끊긴 궤적도 '창 [50, 100]' 으로 기록). 아래 `melt_window_check` 는 **창 안 프레임만** 읽고 **창 안 시간원점만** 쓴다.
#:   문턱 (1e-6 cm²/s) 은 옛 진단값을 승계한다 — 그 승계는 카드 · 결정에 결과 전에 적었다. 옛 진단 결과는 덮지 않는다.
#: ⛔ 2026-11-03 회신 DG — 판정이 원자료에 안 묶여 있었다: final.xyz 에 5 원자 PS₄ 를 넣어도 통과 · 판정 파일만 남은 폴더도
#:   통과 · 다섯째 시드가 미완이어도 묶음 통과 · 녹음 상태 'unknown' 통과 · plan 밀도 NaN 통과 · 소프트웨어 반쪽 기록 통과 ·
#:   virial 열을 지워도 '압력 기록' · 카드 estimator 이름을 바꿔도 window_mto_v1 실행 · 0 번 프레임의 종 배치만 바꿔도 판정이 바뀜.
#:   아래는 그 구멍을 막는다: 카드 값 검사 (`validate_li2s2_values`) · 비교 전 유한성 (`_same`) · 프레임 종 일치 · 최종 구조 대조
#:   (`final_structure_check`) · 판정에 원자료 지문 (`run_provenance`) · 묶음은 지문을 다시 재고 선언된 시드 **전부** 판정 끝 ·
#:   첫 시드 녹음 미충족은 **그 계를 닫는 사건** (`closes_system`) 으로 판정 파일에 남긴다 (일반 시드 탈락과 가른다 · DG P0-1) ·
#:   비용 장부의 합이 상한을 넘으면 통과로 올리지 않는다 (DG P0-3 의 소비자 쪽).
LI2S2_CARD = "db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json"
MELT_WINDOW_ESTIMATOR = "window_mto_v1"
STAGE1_RC = {"pass": 0, "fail": 2, "incomplete": 3, "invalid": 4}
SUMMARY_RC = {"stage1_pass": 0, "stop_track": 2, "pending": 3, "invalid": 4, "cap_incomplete": 5}
LI2S2_STATUSES = ("pass", "fail", "incomplete", "invalid")
DENSITY_REL_TOL = 1e-4          # 고정 밀도 대조 (gate_check NVT · 최종 구조) — 한 곳에서만 정한다
PROVENANCE_FILES = ("plan.json", "thermo.csv", "traj.xyz", "final.xyz", "result.json")
ATTEMPT_NAME = "stage1_attempt.json"  # 러너가 실행 전에 쓰는 식별 기록 — 보존 폴더도 비용 검사 대상
#: ⭐ 회신 DQ P1-1 — 판정이 **읽는** 파일 전부를 지문에 묶는다. PROVENANCE_FILES (원자료 다섯 · 실행 전 판정의 '전부 없음' 기준은 그대로) 에 더해
#:   md_init_raw.xyz (seed_gate 가 이미 있으면 읽고 traj 원시와 대조 · 없으면 traj 에서 만든다 — 파생) · stage1_attempt.json (identity_check 가
#:   **보존 폴더 seed<N>.<붙임> 에서만** 읽는다 — 그 폴더에서만 묶는다 · _judge_reads_attempt). G4 밴드 카드 · 카드 값 · 도구 · 실행 환경은
#:   provenance 의 다른 칸 (band_sha16 · card_values_sha16 · driver_sha16 · runtime) 이 묶는다.
JUDGE_DERIVED_FILES = ("md_init_raw.xyz",)       # = SEED_GATE_RAW (selftest 가 대조) — 판정이 처음 만들 수 있는 파일
JUDGE_FILES = PROVENANCE_FILES + JUDGE_DERIVED_FILES               # 모든 폴더에서 판정이 읽는 파일
BOUND_FILES = JUDGE_FILES + (ATTEMPT_NAME,)                        # 판정이 읽을 수 있는 파일 전부 (보존 폴더면 실행 전 기록까지)


def _judge_reads_attempt(run):
    """identity_check 가 실행 전 기록 (stage1_attempt.json) 을 읽는 폴더인가 — 보존 폴더 seed<N>.<붙임> 꼴 (그 함수와 같은 조건)."""
    return re.fullmatch(r"seed(\d+)\.(.+)", pathlib.Path(run).name) is not None
LEDGER_NAME = "stage1_ledger.json"   # li2s2_stage1_runner.py 가 쓰는 비용 장부 — stage1_summary 가 상한을 여기서 다시 잰다
RUN_ID_RE = re.compile(r"^[0-9a-f]{32}$")   # 회신 DH P0-2 — 러너가 담금질마다 주는 실행 식별자 (plan.json run_id · 장부 run_id)
RETRY_BIND_CODES = {"invalid": ("invalid",), "interrupted": ("interrupted", "abnormal", "resume", "cap")}   # 재시도 확인 STOP 의 code (종류별)
VERDICT_HISTORY = "stage1_verdict_history.jsonl"   # 회신 DH P1-5 — 판정을 덮어쓰기 전 이전 판정 전체 · 지문 변화 · 사유
COST_BASES = ("measured", "upper_bound", "attested_upper_bound")    # 장부 런 비용 근거 — 측정 · 보수 상한 · 사람이 근거를 보고 적은 상한 (재부팅 고아 런 · --attest_cost) —  시작)


def _fin(x):
    """유한한 수인가 — 수 타입 (int · float · numpy 수) 만. None · NaN · inf · bool · **숫자 글자 ('12.5')** · float 로 못 바꾸는 큰 정수는
    아니다 (⭐ DO 전 리뷰 · 회신 DN P1 — 글자를 수로 바꿔 읽지 않는다)."""
    if isinstance(x, bool) or not isinstance(x, numbers.Real):
        return False
    try:
        return math.isfinite(float(x))
    except (OverflowError, ValueError, TypeError):
        return False


def _same(a, b, rel=1e-9, abs_=0.0):
    """둘 다 유한하고 |a − b| ≤ max(abs_, rel·max(1, |b|)) — NaN · None 은 '다르다' (회신 DG P1-7: NaN 이 비교를 빠져나가던 것)."""
    if not (_fin(a) and _fin(b)):
        return False
    a, b = float(a), float(b)
    return abs(a - b) <= max(float(abs_), float(rel) * max(1.0, abs(b)))


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def values_sha16(v):
    """카드 기계_판독_값의 지문 — 판정이 **어느 카드 값으로** 났는지 묶는다."""
    return hashlib.sha256(json.dumps(v, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]


def driver_sha16():
    return _sha256_file(__file__)[:16]


#: ⭐ DR 전 5차 리뷰 P2 — 판정 (stage1_verdict 와 그 아래 combine_stage1 · melt_window_check · final_structure_check) 이 **읽는** 카드 기계_판독_값 열쇠.
#:   상한 (stage1_cap_gpu_h) · 재시도 · 증언 · 시드 · 2 단계 칸은 판정이 안 읽는다 — 문서대로 상한을 올려도 판정 규칙은 그대로다. selftest 가 판정이 이 밖의
#:   열쇠를 읽지 않는지 본다 (읽기 추적).
JUDGE_VALUE_KEYS = ("composition", "first_seed", "fix_density_g_cm3", "gate_check", "melt_window", "schedule", "seed_gate", "software_required",
                    "thermo_required_columns", "uma_inference_mode")


def judge_values_sha16(v):
    """⭐ DR 전 5차 리뷰 P2 — 판정 규칙의 지문 (JUDGE_VALUE_KEYS 만) — 보존 폴더의 과학적 판정 기록이 지금 규칙으로 났는지 가른다 (_run_kind)."""
    return values_sha16({k: v.get(k) for k in JUDGE_VALUE_KEYS})


NONFILE_STATES = ("nonfile:dir", "nonfile:symlink", "nonfile:other")   # ⭐ 회신 DR P1-2 — 경로는 있는데 정상 파일이 아니다 (디렉터리 · 깨진 링크 · 특수 파일)
_SHA256_RE = re.compile(r"[0-9a-f]{64}")


def path_state(p):
    """⭐ 회신 DR P1-2 — 판정 입력 경로 하나의 상태 (지문 칸의 값): 없음 → None · 정상 파일 (링크 아님) → sha256 · 파일을 가리키는 링크 →
    'link:' + 그 내용의 sha256 (내용이 바뀌면 잡힌다 · 정상 파일과는 다르다) · 그 밖 (디렉터리 · 깨진 링크 · 디렉터리를 가리키는 링크 · 특수 파일) →
    NONFILE_STATES 중 하나. 진짜 부재와 '경로는 있는데 파일이 아님' 을 같은 None 으로 접지 않는다 (파생 파일 생성 예외가 부재 → 정상 파일에만 걸리게)."""
    p = pathlib.Path(p)
    if p.is_symlink():
        return ("link:" + _sha256_file(p)) if p.is_file() else "nonfile:symlink"
    if p.is_file():
        return _sha256_file(p)
    if os.path.lexists(p):
        return "nonfile:dir" if p.is_dir() else "nonfile:other"
    return None


def path_state_problem(h):
    """지문 칸 값의 꼴 — None · 64 자리 16진수 · 'link:' + 64 자리 16진수 · NONFILE_STATES 만 받는다 (아니면 이유 · 받으면 None)."""
    if h is None or h in NONFILE_STATES:
        return None
    if isinstance(h, str) and (_SHA256_RE.fullmatch(h) or (h.startswith("link:") and _SHA256_RE.fullmatch(h[5:]))):
        return None
    return f"지문 ({str(h)[:20]!r}) 이 64 자리 16진수 글자도 경로 상태 (link: · nonfile:) 도 아니다"


def run_provenance(run):
    """판정이 기댄 파일의 지문 (회신 DG P1-4 · ⭐ DQ P1-1 — 원자료 다섯 + 판정이 읽는 파생 · 실행 전 기록 = BOUND_FILES) — 경로 상태 (path_state):
    없음 → None ('없음' 도 지문이다) · 정상 파일 → sha256 · 링크 · 디렉터리 · 특수 파일은 따로 (⭐ 회신 DR P1-2). 판정 **뒤** 의 상태다 (판정이
    md_init_raw.xyz 를 처음 만들었으면 만든 것의 지문 · 그 사실은 derived_written)."""
    run = pathlib.Path(run)
    names = JUDGE_FILES + ((ATTEMPT_NAME,) if _judge_reads_attempt(run) else ())   # 판정이 읽는 것만 (현재 폴더의 실행 전 기록은 판정이 안 읽는다)
    return {f: path_state(run / f) for f in names}


def _band_card_path(card=BAND_CARD):
    """read_band 와 같은 경로 해석 (repo 루트 상대 — 도구가 어디서 불리든 같은 카드)."""
    q = pathlib.Path(card)
    return q if q.exists() else pathlib.Path(__file__).resolve().parents[2] / card


BAND_NOT_READ = "not_read"    # ⭐ DR 전 리뷰 P3-B — 판정이 G4 밴드 카드를 안 읽었다 (li2s-2 고정 밀도 NVT 는 gate_check 가 밴드 전에 돌아간다)


def band_card_sha16(card=BAND_CARD):
    """⭐ 회신 DQ P1-1 — gate_check 가 read_band 로 읽는 G4 밴드 카드 파일의 지문 (못 읽으면 None — 같다고 보지 않는다).
    판정은 gate_check 가 **실제로 밴드를 읽었을 때만** 이 지문을 적는다 (아니면 BAND_NOT_READ — 안 읽은 파일을 묶어 작업 폴더에 따라 낡음이 되지 않게)."""
    try:
        return _sha256_file(_band_card_path(card))[:16]
    except OSError:
        return None


def judge_runtime():
    """⭐ 회신 DQ P1-1 — 판정을 낸 실행 환경 (파이썬 · ase · numpy 판). 같은 바이트라도 판독 라이브러리가 바뀌면 판정이 달라질 수 있다 —
    자동 대체의 '같은 도구' 조건에만 쓴다 (묶음 판정의 '지금과 같은가' 대조에는 안 쓴다 · 다른 기계에서 요약할 수 있게)."""
    from importlib import metadata
    out = {"python": sys.version.split()[0], "numpy": getattr(np, "__version__", None)}
    try:
        out["ase"] = metadata.version("ase")
    except Exception as e:
        out["ase"] = f"?({type(e).__name__})"
    return out


def validate_li2s2_values(v):
    """카드 `기계_판독_값` 검사 — 문제 목록 (빈 목록이면 통과). 이 도구가 구현하지 않은 판독량 · 비유한 값 · 꼴 오류를 거부한다."""
    bad = []
    try:
        mw = v["melt_window"]
        if mw.get("estimator") != MELT_WINDOW_ESTIMATOR:
            bad.append(f"melt_window.estimator {mw.get('estimator')!r} ≠ 이 도구가 구현한 {MELT_WINDOW_ESTIMATOR!r}")
        a_, b_ = mw["t_from_frac_of_melt"], mw["t_to_frac_of_melt"]
        if not (_fin(a_) and _fin(b_) and 0.0 <= float(a_) < float(b_) <= 1.0):
            bad.append(f"melt_window 창 비율 [{a_!r}, {b_!r}]")
        lo, hi = mw["lag_fit_ps"]
        if not (_fin(lo) and _fin(hi) and 0.0 < float(lo) < float(hi)):
            bad.append(f"melt_window.lag_fit_ps [{lo!r}, {hi!r}]")
        if not (_fin(mw["D_threshold_cm2_s"]) and float(mw["D_threshold_cm2_s"]) > 0):
            bad.append(f"melt_window.D_threshold_cm2_s {mw['D_threshold_cm2_s']!r}")
        if not isinstance(mw.get("element"), str) or mw["element"] not in MASS:
            bad.append(f"melt_window.element {mw.get('element')!r}")
        sched = v["schedule"]
        for k in ("T_melt_K", "T_final_K", "melt_ps", "quench_rate_K_s", "hold_ps", "dt_fs", "save_ps", "compress_ps", "n_atoms"):
            if not (_fin(sched.get(k)) and float(sched[k]) > 0):
                bad.append(f"schedule.{k} {sched.get(k)!r}")
        if all(_fin(sched.get(k)) for k in ("compress_ps", "melt_ps")) and float(sched["compress_ps"]) > float(sched["melt_ps"]) / 2 + 1e-9:
            bad.append("schedule.compress_ps > melt_ps/2 (판정 창과 겹친다)")
        comp = v.get("composition")
        for s_ in ("A", "B"):
            rho = (v.get("fix_density_g_cm3") or {}).get(s_)
            if not (_fin(rho) and float(rho) > 0):
                bad.append(f"fix_density_g_cm3.{s_} {rho!r}")
            c = (comp or {}).get(s_)
            if (not isinstance(c, dict) or not c or any(e not in MASS or isinstance(n, bool) or not isinstance(n, int) or n <= 0
                                                       for e, n in c.items())
                    or not _fin(sched.get("n_atoms")) or sum(c.values()) != int(sched["n_atoms"])):
                bad.append(f"composition.{s_} {c!r} (원소 · 양의 정수 · 합 = n_atoms)")
        if not isinstance(v.get("uma_inference_mode"), str):
            bad.append(f"uma_inference_mode {v.get('uma_inference_mode')!r}")
        req = v.get("software_required")
        if (not isinstance(req, dict) or not all(isinstance(req.get(k), str) and req.get(k) for k in ("model", "task"))
                or not isinstance(req.get("versions_present"), list) or not req["versions_present"]):
            bad.append(f"software_required {req!r} (model · task · versions_present)")
        cols = v.get("thermo_required_columns")
        if not isinstance(cols, list) or not {"t_ps", "T_set_K", "density_g_cm3", "P_GPa", "P_virial_GPa"} <= set(cols):
            bad.append(f"thermo_required_columns {cols!r} (t_ps · T_set_K · density_g_cm3 · P_GPa · P_virial_GPa 포함)")
        sg = v["seed_gate"]
        if sg.get("version") not in ("relaxed", "raw") or not _fin(sg.get("PS4_fraction_min")) or not _fin(sg.get("min_pair_excl_PS_A_gt")):
            bad.append(f"seed_gate {sg!r}")
        if not (_fin(v["gate_check"].get("win_ps")) and float(v["gate_check"]["win_ps"]) > 0):
            bad.append(f"gate_check.win_ps {v['gate_check'].get('win_ps')!r}")
        seeds = v["seeds"]
        if (not isinstance(seeds, list) or not seeds or any(isinstance(x, bool) or not isinstance(x, int) for x in seeds)
                or len(set(seeds)) != len(seeds) or seeds != sorted(seeds)):
            bad.append(f"seeds {seeds!r} (서로 다른 정수 · 오름차순)")
        need = v["stage1_need_pass"]
        if isinstance(need, bool) or not isinstance(need, int) or not (1 <= need <= len(seeds or [])):
            bad.append(f"stage1_need_pass {need!r}")
        if not isinstance(seeds, list) or not seeds or v.get("first_seed") != seeds[0]:
            bad.append(f"first_seed {v.get('first_seed')!r} ≠ seeds[0] — 첫 시드 녹음 판정의 '첫' 을 카드가 정한다")
        m = v["stage2_machines"]
        if not isinstance(m, list) or len(m) < 2 or not all(isinstance(x, str) and x for x in m):
            bad.append(f"stage2_machines {m!r}")
        cap = v.get("stage1_cap_gpu_h")
        if not (_fin(cap) and float(cap) > 0):
            bad.append(f"stage1_cap_gpu_h {cap!r}")
        rr_ = v.get("retry_reasons")
        if (not isinstance(rr_, dict) or set(rr_) != {"invalid", "interrupted"}
                or not all(isinstance(x, list) and x and all(isinstance(y, str) and y for y in x) for x in rr_.values())):
            bad.append(f"retry_reasons {rr_!r} (invalid · interrupted 각각 허용 사유 목록 — 결과와 무관한 사건만)")
        for gone in ("outage_reasons", "stage1_outage_extra_budget_gpu_h"):   # 회신 DK — 정전 추가 예산은 없앴다 (카드 v3)
            if gone in v:
                bad.append(f"{gone} — 카드 개정 v3 (회신 DK) 에서 없앤 값이다 (정전 손실은 상한을 늘리지 않는다)")
        cr = v.get("cap_retry_reasons")
        if not (isinstance(cr, list) and cr and isinstance(rr_, dict) and set(cr) <= set(rr_.get("interrupted") or [])
                and set(cr) != set(rr_.get("interrupted") or [])):
            bad.append(f"cap_retry_reasons {cr!r} (interrupted 사유의 진부분집합 — 상한으로 멈춘 런에만)")
        af = v.get("attestation_required_fields")
        if not (isinstance(af, list) and {"event", "time_reference", "uncertainty_h", "derivation", "confirmer", "confirmed_at"} <= set(af)):
            bad.append(f"attestation_required_fields {af!r}")
        mr = v.get("stage1_max_interrupt_retries_per_seed")
        if isinstance(mr, bool) or not isinstance(mr, int) or mr < 0:
            bad.append(f"stage1_max_interrupt_retries_per_seed {mr!r} (0 이상 정수 — 끊긴 런 재시도 한도 · 정전 복구 개정)")
    except (KeyError, TypeError, ValueError, AttributeError) as e:
        bad.append(f"꼴 오류 {type(e).__name__}: {e}")
    return bad


def read_li2s2_values(card=LI2S2_CARD):
    """li2s-2 카드의 `기계_판독_값` — 이 도구는 그 카드의 문턱 · 일정 · 목표 밀도를 **자체 보관하지 않는다**.
    값이 이 도구가 구현한 것과 안 맞으면 (estimator 이름 · 비유한 값 · 빠진 필드) **읽기에서 죽는다** (회신 DG P1-7)."""
    d = loads_strict(pathlib.Path(card).read_text(encoding="utf-8"))   # ⭐ 회신 DO P1 — 카드도 같은 열쇠 둘을 받지 않는다
    v = d.get("기계_판독_값")
    if not v:
        raise KeyError(f"{card} 에 '기계_판독_값' 이 없다 — 카드 없이 판정하지 않는다")
    bad = validate_li2s2_values(v)
    if bad:
        raise ValueError(f"{card} 기계_판독_값 거부 — " + " · ".join(bad))
    return v


def software_versions(mode):
    """plan.json 에 남길 실행 소프트웨어 (회신 DF Q-DF-6: 기계 이름이 아니라 판 · 체크포인트 · 추론 설정을 고정한다)."""
    from importlib import metadata
    out = {"model": "uma-s-1p1", "task": "omat", "inference": mode}
    for pkg in ("fairchem-core", "torch", "ase"):
        try:
            out[pkg] = metadata.version(pkg)
        except Exception as e:
            out[pkg] = f"?({type(e).__name__})"
    return out


def _leading_frames(traj_path, n_need):
    """traj.xyz 의 앞 n_need 프레임만 읽는다 — 쓰는 중인 파일이면 끝의 반쪽 프레임에서 멈춘다 (멈춘 이유를 돌려준다)."""
    from ase.io import iread
    frames, why = [], None
    try:
        for fr in iread(str(traj_path), index=slice(0, n_need)):
            frames.append(fr)
    except Exception as e:
        why = f"{type(e).__name__}: {e}"
    return frames, why


def window_mto_msd(sym, pos, cells, lags):
    """창 안 프레임들로 원소별 **다중 시간원점** MSD [Å²] — 원점은 창 안에서만 고른다.

    분수좌표 차분 → MIC → 그 프레임 셀로 실공간 증분 → 창 첫 프레임 기준 누적 → 전체 평균 병진 제거 (npt_msd 와 같은 꼴)
    → 지연 k 마다 모든 (j, j+k) 쌍 평균. 창 밖 이력은 들어갈 길이 없다."""
    sym = np.asarray(sym); pos = np.asarray(pos, float); cells = np.asarray(cells, float)
    T, N, _ = pos.shape
    frac = np.einsum("tnj,tjk->tnk", pos, np.linalg.inv(cells))
    df = np.diff(frac, axis=0); df -= np.round(df)
    steps = np.einsum("tnj,tjk->tnk", df, cells[1:])
    disp = np.concatenate([np.zeros((1, N, 3)), np.cumsum(steps, axis=0)])
    disp -= disp.mean(axis=1, keepdims=True)
    out = {}
    for e in sorted(set(sym.tolist())):
        d = disp[:, sym == e]
        out[str(e)] = np.array([((d[k:] - d[:-k]) ** 2).sum(-1).mean() if 0 < k < T else np.nan for k in lags])
    return out


def _species_check(frames, plan, values):
    """프레임마다 원자 수 · 종 순서가 같고, plan · 카드 조성과 맞는가 (회신 DG P1-7: 종을 frames[0] 에서만 가져오던 것).
    문제 목록을 돌려준다 — 이런 파일은 다른 물리 판정을 내릴 것이 아니라 **무효**다."""
    why = []
    if not frames:
        return why
    syms = [tuple(f.get_chemical_symbols()) for f in frames]
    if len(set(syms)) > 1:
        i = next(k for k, x in enumerate(syms) if x != syms[0])
        why.append(f"프레임마다 원자 수 · 종 순서가 다르다 (프레임 0 대 {i})")
    s0 = syms[0]
    comp = {e: s0.count(e) for e in sorted(set(s0))}
    if plan.get("n_atoms") is not None and len(s0) != plan.get("n_atoms"):
        why.append(f"traj 원자 수 {len(s0)} ≠ plan {plan.get('n_atoms')}")
    if plan.get("composition") is not None and comp != plan["composition"]:
        why.append(f"traj 조성 {comp} ≠ plan {plan['composition']}")
    if "composition" in values:
        want = (values.get("composition") or {}).get(plan.get("system"))
        if want is None or comp != want:
            why.append(f"traj 조성 {comp} ≠ 카드 {plan.get('system')} {want}")
    return why


def melt_window_check(run_dir, *, values=None, card=LI2S2_CARD, log=print):
    """⭐ li2s-2 녹음 판정 — 압축 **뒤** 창 [melt_ps·a, melt_ps·b] 안 프레임 · 창 안 시간원점만 쓰는 P 골격 D (회신 DF P0).

    verdict: pass (D_P > 문턱) · fail · incomplete (plan · traj 가 아직 없다 · 창 전체가 없다 · 쓰는 중) ·
             invalid (카드 estimator ≠ 구현 · 고정 밀도 plan 아님 · 압축이 창과 겹침 · 좌표 비유한 · 프레임 종 · 원자 수 불일치).
    ⛔ 못 하는 것: 'pass' 는 '이 밀도 · 온도 · 시간에서 사전 정의한 P 골격 이동 기준을 충족했다' 까지다 — 평형 액체의 인증이
       아니다. 'fail' 은 '1200 K 에서 액체가 없다' 가 아니다 (회신 DF Q-DF-3 문구). 결정화 · 구조는 안 본다.
       겹치는 시간원점들은 독립 표본이 아니다 (회신 DG ①) — D 는 운영 판독량이지 오차막대가 붙은 측정이 아니다."""
    v = values if values is not None else read_li2s2_values(card)
    mw = v["melt_window"]
    run = pathlib.Path(run_dir)
    out = {"kind": "melt_window_check", "estimator": MELT_WINDOW_ESTIMATOR, "estimator_card": mw.get("estimator"), "run": str(run),
           "estimator_def": "창 안 프레임만 · 창 안 시간원점 (다중 원점) · 창 첫 프레임 기준 unwrap · 전체 병진 제거 · "
                            "지연 [lag_fit] 자유절편 선형맞춤 MSD = 6Dτ + c",
           "overlap_ok": None, "coverage_ok": None, "finite_ok": None, "species_ok": None, "window_used_ps": None,
           "per_element": {}, "D_framework_cm2_s": None}
    def done(verdict, msg):
        out["verdict"] = verdict; out["message"] = msg; log(f"  [melt_window] {verdict} — {msg}"); return out
    if mw.get("estimator") != MELT_WINDOW_ESTIMATOR:     # 회신 DG P1-7 — 카드가 다른 판독량을 부르면 이 이름으로 돌리지 않는다
        return done("invalid", f"카드 estimator {mw.get('estimator')!r} ≠ 이 도구가 구현한 {MELT_WINDOW_ESTIMATOR!r}")
    try:                                                  # 회신 DG P0-2 — 담금질 시작 직후에는 plan.json 이 아직 없다
        plan = loads_strict((run / "plan.json").read_text(encoding="utf-8"))   # ⭐ 회신 DO P1 — 같은 열쇠 둘은 예외 (호출자가 보류)
    except FileNotFoundError:
        return done("incomplete", "plan.json 이 아직 없다 (담금질 시작 직후) — 기다린다")
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return done("incomplete", f"plan.json 을 아직 못 읽는다 ({type(e).__name__} · 쓰는 중일 수 있다) — 기다린다")
    if plan.get("fix_density_g_cm3") is None:
        return done("invalid", "고정 밀도 plan 이 아니다 (fix_density_g_cm3 없음) — 이 판독량은 li2s-2 고정 밀도 런 전용")
    if not (_fin(plan.get("melt_ps")) and _fin(plan.get("save_ps")) and float(plan["save_ps"]) > 0):
        return done("invalid", f"plan 의 melt_ps · save_ps 가 유한한 양수가 아니다 ({plan.get('melt_ps')!r} · {plan.get('save_ps')!r})")
    melt_ps, save_ps = float(plan["melt_ps"]), float(plan["save_ps"])
    t_from, t_to = float(mw["t_from_frac_of_melt"]) * melt_ps, float(mw["t_to_frac_of_melt"]) * melt_ps
    lag_lo, lag_hi = (float(x) for x in mw["lag_fit_ps"])
    comp = float(plan.get("compress_ps")) if _fin(plan.get("compress_ps")) else float("nan")
    thr, el = float(mw["D_threshold_cm2_s"]), str(mw["element"])
    out.update({"window_declared_ps": [t_from, t_to], "lag_fit_ps": [lag_lo, lag_hi], "compress_end_ps": comp,
                "element": el, "D_threshold_cm2_s": thr, "threshold_source": mw.get("threshold_source"),
                "overlap_ok": bool(comp <= t_from + 1e-9)})
    if not out["overlap_ok"]:
        return done("invalid", f"압축 끝 {comp:g} ps 가 판정 창 시작 {t_from:g} ps 보다 늦다 (또는 비유한) — 창이 강제 압축과 겹친다")
    if not (run / "traj.xyz").is_file():
        return done("incomplete", "traj.xyz 가 아직 없다 — 기다린다")
    n_need = int(round(t_to / save_ps)) + 1
    frames, why = _leading_frames(run / "traj.xyz", n_need)
    out["n_frames_read"], out["read_stop"] = len(frames), why
    if why is not None and len(frames) < n_need:            # ⭐ DP 전 리뷰 (둘째) F5 — 앞 프레임 하나가 깨지면 '쓰는 중' 으로 영원히 기다리지 않는다
        try:
            n_whole, io_err = _xyz_frames(run / "traj.xyz"), None
        except OSError as e_:
            n_whole, io_err = None, f"{type(e_).__name__}"
        out["n_frames_whole"] = n_whole
        if io_err is not None:
            out["io_error"] = f"traj 프레임 세기 {io_err}"   # ⭐ 회신 DQ P1-1 — 판정 도중 예외 (stage1_verdict 가 judge_nature.errors 로 모은다)
        if io_err is None and (n_whole is None or n_whole > len(frames)):
            return done("invalid", f"궤적 앞부분이 깨졌다 — 온전한 프레임 {n_whole if n_whole is not None else '(머리 깨짐 · 못 셈)'} 중 "
                                   f"{len(frames)} 번째에서 못 읽는다 ({why[:80]}) · 쓰는 중인 꼬리가 아니다")
    sp_why = _species_check(frames, plan, v)
    out["species_ok"] = not sp_why
    if sp_why:
        return done("invalid", " · ".join(sp_why))
    times = np.arange(len(frames)) * save_ps
    sel = np.where((times >= t_from - 1e-6) & (times <= t_to + 1e-6))[0]
    if sel.size:
        out["window_used_ps"] = [float(times[sel[0]]), float(times[sel[-1]])]
    out["coverage_ok"] = bool(sel.size >= 2 and times[sel[0]] <= t_from + 1e-6 and times[sel[-1]] >= t_to - 1e-6)
    if not out["coverage_ok"]:
        return done("incomplete", f"창 [{t_from:g}, {t_to:g}] ps 가 다 없다 — 읽은 프레임 {len(frames)} · 쓴 창 {out['window_used_ps']}")
    sym = frames[sel[0]].get_chemical_symbols()            # 종도 **창 안** 프레임에서 (프레임 종 일치는 위에서 봤다)
    pos = np.array([frames[i].get_positions() for i in sel]); cells = np.array([np.asarray(frames[i].get_cell()) for i in sel])
    out["finite_ok"] = bool(np.isfinite(pos).all() and np.isfinite(cells).all())
    if not out["finite_ok"]:
        return done("invalid", "창 안 좌표 · 셀에 유한하지 않은 값이 있다")
    k_lo, k_hi = int(math.ceil(lag_lo / save_ps - 1e-9)), int(math.floor(lag_hi / save_ps + 1e-9))
    lags = list(range(max(1, k_lo), k_hi + 1))
    msd = window_mto_msd(sym, pos, cells, lags)
    tau = np.array(lags) * save_ps
    for e, m in msd.items():
        ok = np.isfinite(m)
        if ok.sum() < 4:
            out["per_element"][e] = {"D_cm2_s": None}; continue
        a, c = np.polyfit(tau[ok], m[ok], 1)
        out["per_element"][e] = {"D_cm2_s": float(a / 6.0 * 1e-4), "intercept_A2": float(c),
                                 "msd_at_lag_hi_A2": float(m[ok][-1])}
    D = out["per_element"].get(el, {}).get("D_cm2_s")
    out["D_framework_cm2_s"] = D
    if D is None or not math.isfinite(D):
        return done("invalid", f"{el} 의 D 를 못 냈다 (지연 점 부족)")
    if D > thr:
        return done("pass", f"이 밀도 · 온도 · 시간에서 사전 정의한 {el} 골격 이동 기준을 충족했다 (D {D:.2e} > {thr:g} cm²/s) — 평형 액체 인증 아님")
    return done("fail", f"이 밀도 · 온도 · 시간에서 사전 정의한 {el} 골격 이동 기준을 충족하지 못했다 (D {D:.2e} ≤ {thr:g} cm²/s) — '액체가 없다' 가 아님")


def final_structure_check(run, plan, values, raw_last=None):
    """⭐ 회신 DG P1-4 — final.xyz 가 **이 런의** 최종 구조인가: 원자 수 · 조성 (카드 · plan) · 종 순서 (traj 마지막 프레임과) ·
    셀 (traj 마지막 셀과 — 고정 셀 FIRE) · 밀도 (카드 목표, 상대 DENSITY_REL_TOL). 문제가 있으면 ok False + 이유.
    ⛔ 못 하는 것: final.xyz 가 '그 traj 에서 FIRE 로 나온 것' 인지까지는 모른다 — 같은 원자 수 · 조성 · 셀의 다른 구조로 바꿔치면
       못 잡는다 (원시와의 변위는 seed_gate 가 기록만 한다). 일관된 전면 위조는 막지 않는다 (회신 DG 도 그 가정은 안 했다)."""
    from ase.io import read
    run = pathlib.Path(run)
    res = {"ok": False, "why": []}
    try:
        fa = read(str(run / "final.xyz"))
    except Exception as e:
        res["why"].append(f"final.xyz 를 못 읽었다 ({type(e).__name__}: {e})")
        res["judge_errors"] = [f"final.xyz 읽기 {type(e).__name__}: {str(e)[:80]}"]   # ⭐ 회신 DQ P1-1 — 판정 도중 예외
        return res
    sym = fa.get_chemical_symbols()
    sysname = plan.get("system")
    comp = {e: sym.count(e) for e in sorted(set(sym))}
    rho = density_g_cm3(fa) if all(e in MASS for e in sym) and fa.get_volume() > 0 else float("nan")
    res.update({"n_atoms": len(sym), "composition": comp, "density_g_cm3": rho})
    want_n = values["schedule"]["n_atoms"]
    if not (_same(len(sym), want_n) and _same(len(sym), plan.get("n_atoms"))):
        res["why"].append(f"원자 수 {len(sym)} ≠ 카드 {want_n} · plan {plan.get('n_atoms')}")
    want_comp = (values.get("composition") or {}).get(sysname)
    if want_comp is None or comp != want_comp:
        res["why"].append(f"조성 {comp} ≠ 카드 {sysname} {want_comp}")
    if plan.get("composition") is not None and comp != plan["composition"]:
        res["why"].append(f"조성 {comp} ≠ plan {plan['composition']}")
    tgt = (values.get("fix_density_g_cm3") or {}).get(sysname)
    dev = abs(rho / float(tgt) - 1.0) if (_fin(tgt) and _fin(rho)) else float("nan")
    res["density_rel_dev"] = dev
    if not (dev <= DENSITY_REL_TOL):
        res["why"].append(f"밀도 {rho} ≠ 카드 {tgt} (상대 차 {dev:.1e} > {DENSITY_REL_TOL:g})")
    if raw_last is None:
        res["why"].append("traj 마지막 프레임이 없다 — 종 순서 · 셀을 대조하지 못했다")
    else:
        same_order = list(raw_last.get_chemical_symbols()) == list(sym)
        res["species_order_same_as_traj_last"] = same_order
        if not same_order:
            res["why"].append("종 순서 · 원자 수가 traj 마지막 프레임과 다르다")
        dc = float(np.abs(np.asarray(raw_last.get_cell()) - np.asarray(fa.get_cell())).max())
        res["cell_vs_traj_last_max_A"] = dc
        if not (dc <= 1e-6):
            res["why"].append(f"고정 셀인데 final 셀이 traj 마지막 셀과 {dc:.2e} Å 다르다")
    res["ok"] = not res["why"]
    return res


def combine_stage1(plan, values, gate, melt, seedg, files, checks=None):
    """li2s-2 1 단계 시드 판정 — 카드가 요구하는 필드를 **직접** 읽는다 (회신 DF P1-2: 종료코드를 합쳐 판정하지 않는다).

    입력은 이미 계산된 dict (plan.json · gate_check · melt_window_check · seed_gate · 파일 존재 · checks) — 순수 함수라 시험이 가볍다.
    checks (회신 DG): thermo_header · traj_frames · final_structure · seed_gate_error — 있으면 본다.
    우선순위: invalid (카드와 다른 실행 · 기록 꼴 · 원자료 불일치) > [첫 시드 녹음 미충족 = 그 계를 닫는 사건] > incomplete > fail > pass.
    ⭐ 회신 DG P0-1 — 계의 첫 시드 (카드 first_seed) 녹음 미충족은 일반 시드 탈락이 아니라 **그 계를 닫는 사건**이다:
       closes_system True · 상태 fail (러너가 멈춰서 일정이 미완이어도). 다른 invalid 이유가 있으면 닫지 않고 invalid (카드 런이 아니다)."""
    checks = checks or {}
    reasons = {"invalid": [], "incomplete": [], "fail": []}
    sched, sysname = values["schedule"], plan.get("system")
    tgt = (values.get("fix_density_g_cm3") or {}).get(sysname)
    if not _same(plan.get("fix_density_g_cm3"), tgt, rel=0.0, abs_=1e-6):
        reasons["invalid"].append(f"고정 밀도 {plan.get('fix_density_g_cm3')!r} ≠ 카드 {tgt!r} ({sysname}) — 비유한 값도 '다름'")
    for k, want in sched.items():
        if not _same(plan.get(k), want):
            reasons["invalid"].append(f"일정 {k} {plan.get(k)!r} ≠ 카드 {want!r}")
    want_comp = (values.get("composition") or {}).get(sysname)
    if want_comp is None or plan.get("composition") != want_comp:
        reasons["invalid"].append(f"조성 plan {plan.get('composition')} ≠ 카드 {sysname} {want_comp}")
    sw = plan.get("software") or {}
    req = values.get("software_required") or {}
    sw_bad = [] if req else ["카드 software_required 없음"]
    if sw.get("inference") != values.get("uma_inference_mode"):
        sw_bad.append(f"inference {sw.get('inference')!r} ≠ {values.get('uma_inference_mode')!r}")
    for k in ("model", "task"):
        if sw.get(k) != req.get(k):
            sw_bad.append(f"{k} {sw.get(k)!r} ≠ {req.get(k)!r}")
    for k in req.get("versions_present") or []:
        x = sw.get(k)
        if not isinstance(x, str) or not x or x.startswith("?"):
            sw_bad.append(f"{k} 판 {x!r}")
    if sw_bad:
        reasons["invalid"].append("소프트웨어 기록이 카드 요구와 다르다 — " + " · ".join(sw_bad))
    for f, ok in files.items():
        if not ok:
            reasons["incomplete"].append(f"{f} 없음")
    th = checks.get("thermo_header")
    if th is not None and not th.get("ok"):
        reasons["invalid"].append(f"thermo.csv 열 {th.get('missing')} 없음 — 이 드라이버가 쓰는 꼴이 아니다")
    sched_done = bool(gate and gate.get("schedule_complete"))
    if gate is None:
        if th is None or th.get("ok"):
            reasons["incomplete"].append("gate_check 없음")
    elif gate.get("error"):
        reasons["incomplete"].append(f"gate_check 오류 ({gate['error']}) — 쓰는 중일 수 있다")
    else:
        if gate.get("thermo_columns_ok") is False:
            reasons["invalid"].append(f"thermo 압력 열이 다 있지 않다 ({gate.get('pressure_columns')}) — 총압 · virial 둘 다 있어야 한다")
        if not _same(gate.get("target_density_g_cm3"), tgt, rel=0.0, abs_=1e-6):
            reasons["invalid"].append(f"gate_check 목표 밀도 {gate.get('target_density_g_cm3')!r} ≠ 카드 {tgt!r}")
        if not sched_done:
            reasons["incomplete"].append("계획한 일정 (melt · 담금질 · 유지) 을 다 돌지 않았다")
        for k, why in (("window_in_hold", "판정 창이 300 K 유지 구간 안이 아니다"), ("density_ok", "밀도 ≠ 목표"),
                       ("pressure_recorded", "압력 기록이 없다 (NaN · 빈 칸) — '기록했다' 와 '없다' 를 가른다")):
            if sched_done and not gate.get(k):
                reasons["fail"].append(why)
    mv = None if melt is None else melt.get("verdict")
    if mv is None or mv == "incomplete":
        reasons["incomplete"].append(f"녹음 판정 {mv}")
    elif mv == "invalid":
        reasons["invalid"].append(f"녹음 판정 invalid — {melt.get('message')}")
    elif mv == "fail":
        reasons["fail"].append(melt.get("message"))
    elif mv != "pass":                                     # 회신 DG P1-7 — 모르는 상태를 통과로 떨어뜨리지 않는다
        reasons["invalid"].append(f"녹음 판정 상태 {mv!r} 를 모른다 (허용: {', '.join(LI2S2_STATUSES)})")
    if checks.get("seed_gate_error"):
        reasons["invalid"].append(f"시드 게이트를 못 냈다 — {checks['seed_gate_error']}")
    sg, rel = values["seed_gate"], (seedg or {}).get(values["seed_gate"]["version"])
    if not rel:
        if not checks.get("seed_gate_error"):
            reasons["incomplete"].append(f"시드 게이트 {values['seed_gate']['version']} 판 없음")
    else:
        if not (_fin(rel.get("PS4_fraction")) and float(rel["PS4_fraction"]) >= float(sg["PS4_fraction_min"]) - 1e-12):
            reasons["fail"].append(f"PS₄ 보존율 {rel.get('PS4_fraction')} < {sg['PS4_fraction_min']}")
        if not (_fin(rel.get("min_pair_excl_PS_A")) and float(rel["min_pair_excl_PS_A"]) > float(sg["min_pair_excl_PS_A_gt"])):
            reasons["fail"].append(f"최단 원자간 (P–S 제외) {rel.get('min_pair_excl_PS_A')} ≤ {sg['min_pair_excl_PS_A_gt']} Å")
    tf = checks.get("traj_frames")
    if tf is not None:
        n, want = tf.get("n"), tf.get("expected")
        if n is None:
            reasons["invalid"].append("traj 프레임 수를 못 셌다 (줄 수가 원자수+2 의 배수가 아니다)")
        elif want is not None and n != want:
            (reasons["invalid"] if (sched_done or n > want) else reasons["incomplete"]).append(
                f"traj 프레임 {n} ≠ 계획 {want}" + (" — thermo 는 끝났는데 traj 가 다르다" if sched_done else ""))
    fs = checks.get("final_structure")
    if fs is not None and not fs.get("ok"):
        reasons["invalid"].append("최종 구조가 이 런과 안 맞는다 — " + " · ".join(fs.get("why") or ["?"]))
    idc = checks.get("identity")
    if idc is not None and not idc.get("ok"):
        reasons["invalid"].append("실행 식별이 안 맞는다 — " + " · ".join(idc.get("why") or ["?"]))
    first = values.get("first_seed")
    closes = bool(first is not None and plan.get("seed") == first and mv == "fail" and not reasons["invalid"])
    if reasons["invalid"]:
        status = "invalid"
    elif closes or mv == "fail":                         # ⭐ DO 전 리뷰 — 녹음 창이 다 찼고 fail 이면 결과가 정해졌다 (일정 미완 · 최종 파일 없음이어도)
        status = "fail"
    else:
        status = next((s for s in ("incomplete", "fail") if reasons[s]), "pass")
    return {"status": status, "reasons": reasons, "system": sysname, "seed": plan.get("seed"), "software": sw,
            "run_id": plan.get("run_id"), "closes_system": closes,
            "closing_event": ("계의 첫 시드 녹음 판정 미충족 — 그 계를 닫는다 (카드 S1 ② · 일반 시드 탈락과 다르다)" if closes else None)}


def folder_identity(run_dir):
    """<out_root>/<계>/seed<S>/ 의 (계, 시드) — 꼴이 아니면 (None, None)."""
    run = pathlib.Path(run_dir)
    m = re.fullmatch(r"seed(\d+)", run.name)
    return (run.parent.name, int(m.group(1))) if m else (None, None)


def identity_check(run_dir, plan):
    """⭐ 회신 DH P0-2 — 폴더 (계, 시드) = plan (계, 시드) · plan 에 러너의 실행 식별자 (run_id · 32 hex) 가 있다.
    폴더를 통째로 복사하면 (A11 → A12) plan 의 시드가 폴더와 달라 여기서 무효가 된다 · plan 시드까지 고치면 run_id 가 겹치거나
    장부의 그 run_id 런이 다른 시드라서 묶음 (stage1_summary) 에서 무효가 된다."""
    fs, fsd = folder_identity(run_dir)
    why, preserved, read_err = [], False, None
    if fs is None:                                           # ⭐ DO 전 리뷰 (소비자 P0) — 보존 폴더 seed<N>.<붙임> 은 실행 전 기록으로 묶이면 받는다
        rd_ = pathlib.Path(run_dir)
        m_ = re.fullmatch(r"seed(\d+)\.(.+)", rd_.name)      # = _judge_reads_attempt (그 폴더에서만 실행 전 기록을 읽고 · 지문에 묶는다)
        att_ = None
        if m_:
            try:
                att_ = loads_strict((rd_ / ATTEMPT_NAME).read_text(encoding="utf-8"))
            except (OSError, ValueError, RecursionError) as e_:
                att_ = None
                read_err = f"{ATTEMPT_NAME} 읽기 {type(e_).__name__}: {str(e_)[:80]}"   # ⭐ 회신 DQ P1-1 — 판정 도중 예외 (같은 바이트면 다시 같다)
        if (m_ and isinstance(att_, dict) and att_.get("system") == rd_.parent.name and type(att_.get("seed")) is int
                and att_.get("seed") == int(m_.group(1)) and isinstance(plan.get("run_id"), str) and att_.get("run_id") == plan.get("run_id")):
            fs, fsd, preserved = rd_.parent.name, int(m_.group(1)), True
        else:
            why.append(f"폴더 이름 {rd_.name!r} 이 seed<번호> 꼴이 아니다 (보존 폴더 seed<번호>.<붙임> 은 실행 전 기록의 계 · 시드 · "
                       "run_id 가 plan 과 같아야 한다)")
    if fs is None:
        pass
    elif (plan.get("system"), plan.get("seed")) != (fs, fsd):
        why.append(f"폴더 ({fs}, {fsd}) ≠ plan ({plan.get('system')}, {plan.get('seed')}) — 다른 시드의 폴더를 옮겨 왔거나 잘못 회수했다")
    rid = plan.get("run_id")
    if not (isinstance(rid, str) and RUN_ID_RE.match(rid)):
        why.append(f"plan.json 에 실행 식별자 run_id 가 없다 ({rid!r}) — 러너 밖에서 돌린 담금질은 장부에 안 잡힌다")
    return {"folder": [fs, fsd], "plan": [plan.get("system"), plan.get("seed")], "run_id": rid, "ok": not why, "why": why,
            "preserved": preserved, **({"judge_errors": [read_err]} if read_err else {})}


def _append_history(run, prev, res, reason):
    """⭐ 회신 DH P1-5 — 판정을 덮어쓰기 전에 이전 판정 **전체** 와 지문 변화 · 사유를 한 줄 덧붙인다 (지우지 않는다)."""
    pp, npv = (prev.get("provenance") or {}), (res.get("provenance") or {})
    pf, nf = (pp.get("files_sha256") or {}), (npv.get("files_sha256") or {})
    rec = {"at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "reason": reason,
           "prev_status": prev.get("status"), "new_status": res.get("status"),
           "changed": {"status": prev.get("status") != res.get("status"),
                       "files": sorted(k for k in set(pf) | set(nf) if pf.get(k) != nf.get(k)),
                       "card_values": pp.get("card_values_sha16") != npv.get("card_values_sha16"),
                       "driver": pp.get("driver_sha16") != npv.get("driver_sha16"),
                       "run_id": prev.get("run_id") != res.get("run_id")},
           "prev_provenance": pp, "new_provenance": npv, "prev": prev,
           "new_closes_system": res.get("closes_system") is True}   # ⭐ DR 전 3차 리뷰 P2
    with open(pathlib.Path(run) / VERDICT_HISTORY, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
        _fsync_handle(fh)                                    # ⭐ DO 전 리뷰 P2-14 — 판정 기록도 저장장치까지 (정전 뒤 사라지지 않게 · 보증은 아님)
    _fsync_dir(pathlib.Path(run))
    return rec


def _append_history_first(run, res, reason):
    """⭐ DQ 전 5차 리뷰 P2 — 앞 판정 파일이 없을 때 쓰는 판정도 이력에 한 줄 (first) — 이력이 판정 쓰기 전부를 적는 덧붙이기 기록이 되어, 판정 파일이
    지워져도 첫 판정이 기록 사슬 (folder_verdict_chain) 에 남는다. 앞 판정이 없으니 prev 는 없다 (_verdict_records 가 first 줄로 따로 읽는다).
    ⭐ 회신 DQ P1-2 — 정본 없이 이력이 이미 있던 폴더 (첫 판정 쓰기가 끊긴 뒤 사람이 --stage1_verdict 로 다시 판정) 면 그 줄 수를
    history_lines_before 로 적는다 (러너는 이런 폴더를 판정하지 않는다 — 이 길은 사람의 손 판정뿐이다)."""
    rec = {"at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "reason": reason, "first": True,
           "new_status": res.get("status"), "new_provenance": res.get("provenance") or {},
           "new_closes_system": res.get("closes_system") is True}   # ⭐ DR 전 3차 리뷰 P2 — 첫 시드 닫힘도 이력 줄에 (정본이 없어도 장부에 옮길 수 있게)
    hp_ = pathlib.Path(run) / VERDICT_HISTORY
    if hp_.is_file():
        n_ = sum(1 for ln in hp_.read_text(encoding="utf-8", errors="replace").split("\n") if ln.strip())
        if n_:
            rec["history_lines_before"] = n_
    with open(pathlib.Path(run) / VERDICT_HISTORY, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
        _fsync_handle(fh)
    _fsync_dir(pathlib.Path(run))
    return rec


def stage1_verdict(run_dir, *, values=None, card=LI2S2_CARD, log=print, reason="수동 (--stage1_verdict)"):
    """li2s-2 1 단계 시드 판정을 **원자료에서 새로 계산해서** 낸다 (gate_check · melt_window_check · seed_gate · 최종 구조 ·
    traj 프레임 수 · thermo 열 · 실행 식별) → stage1_verdict.json. 판정에는 원자료 지문 · 카드 값 지문 · 도구 지문을 같이 적는다
    (회신 DG P1-4). 이미 판정이 있으면 덮어쓰기 **전에** 그 판정 전체와 지문 변화 · 사유를 stage1_verdict_history.jsonl 에 남긴다 (회신 DH P1-5)."""
    from ase.io import read
    v = values if values is not None else read_li2s2_values(card)
    run = pathlib.Path(run_dir)
    if os.path.lexists(run / "stage1_verdict.json.tmp"):     # ⭐ DP 전 리뷰 (둘째) F2 — 앞 판정 쓰기가 끊긴 흔적을 덮지 않는다
        msg = ("판정 임시 파일 (stage1_verdict.json.tmp) 이 남았다 — 앞 판정 쓰기가 끊겼다 · 그 안에 완료 판정이 있을 수 있어 "
               "덮지 않는다 (아무것도 안 썼다 · 사람이 그 파일을 보고 옮긴 뒤 다시)")
        log(f"  [stage1] {run} → invalid (쓰지 않음) — {msg}")
        return {"status": "invalid", "written": False, "closes_system": False, "run": str(run), "reasons": {"invalid": [msg]},
                "reason": reason}
    plan = None
    try:
        plan = loads_strict((run / "plan.json").read_text(encoding="utf-8"))   # ⭐ 회신 DO P1 — 같은 열쇠 둘은 마지막 값으로 읽지 않는다
        if not isinstance(plan, dict):
            raise ValueError("plan.json 이 객체가 아니다")
    except FileNotFoundError:
        res = {"status": "incomplete", "reasons": {"incomplete": ["plan.json 없음"]}, "run": str(run)}
    except (ValueError, UnicodeDecodeError, RecursionError) as e:
        plan = None
        res = {"status": "incomplete", "reasons": {"incomplete": [f"plan.json 을 못 읽는다 ({type(e).__name__})"]}, "run": str(run)}
    judge_err, input_mismatch, derived_written = [], [], []   # ⭐ 회신 DQ P1-1 — 앞 판정의 성격 (자동 대체는 판정 도중 예외만 · 입력 불일치는 사람)
    band_read = False
    if plan is not None:
        files = {f: (run / f).is_file() for f in ("result.json", "final.xyz", "thermo.csv", "traj.xyz")}
        checks = {}
        if files["thermo.csv"]:
            with open(run / "thermo.csv", encoding="utf-8", errors="replace") as fh:
                hdr = fh.readline().strip().split(",")
            miss = [c for c in v["thermo_required_columns"] if c not in hdr]
            checks["thermo_header"] = {"columns": hdr, "missing": miss, "ok": not miss}
        gate = melt = seedg = None
        if files["thermo.csv"] and checks["thermo_header"]["ok"]:
            try:
                gate = gate_check(run, win_ps=float(v["gate_check"]["win_ps"]), log=lambda *a: None)
            except Exception as e:
                gate = {"schedule_complete": None, "error": f"{type(e).__name__}: {e}"}   # 모름 — False 로 적지 않는다 (DO 전 리뷰)
                judge_err.append(f"gate_check {type(e).__name__}: {str(e)[:80]}")
            if isinstance(gate, dict) and "band_center" in gate:   # ⭐ DR 전 리뷰 P3-B — gate_check 가 G4 밴드 카드를 읽었다 (그때만 묶는다)
                band_read = True
        if files["traj.xyz"]:
            melt = melt_window_check(run, values=v, log=lambda *a: None)
            for k_ in ("read_stop", "io_error"):             # 녹음 판정이 traj 를 읽다 멈춘 예외 (같은 바이트면 다시 같다 · 지문이 가른다)
                if isinstance(melt, dict) and melt.get(k_):
                    judge_err.append(f"melt_window_check {k_}: {str(melt[k_])[:80]}")
            n_fr = _xyz_frames(run / "traj.xyz")
            want = None
            if all(_fin(plan.get(k)) for k in ("melt_ps", "quench_ps", "hold_ps", "save_ps")) and float(plan["save_ps"]) > 0:
                want = int(round((float(plan["melt_ps"]) + float(plan["quench_ps"]) + float(plan["hold_ps"])) / float(plan["save_ps"]))) + 1
            checks["traj_frames"] = {"n": n_fr, "expected": want}
        if files["final.xyz"] and files["traj.xyz"]:
            raw_before = os.path.lexists(run / SEED_GATE_RAW)   # ⭐ 회신 DQ P1-1 — '이 판정이 처음 만들었다' 는 전후 존재로 (seed_gate 가 쓴 뒤 예외가 나도)
            try:
                seedg = seed_gate(run, write_raw=True, log=lambda *a: None)
            except SystemExit as e:                       # md_init_raw.xyz 가 다르다 — 그 자리에서 죽지 않고 판정에 싣는다
                checks["seed_gate_error"] = str(e)
                input_mismatch.append(f"{SEED_GATE_RAW} 가 이미 있고 traj 원시와 다르다 (판정이 끝까지 보고 찾은 입력 불일치 — 판정 도중 오류가 아니다)")
            except Exception as e:
                checks["seed_gate_error"] = f"{type(e).__name__}: {e}"
                judge_err.append(f"seed_gate {type(e).__name__}: {str(e)[:80]}")
            if not raw_before and (run / SEED_GATE_RAW).is_file():
                derived_written.append(SEED_GATE_RAW)       # 이 판정이 처음 만들었다 (앞에 없던 파생 파일) — 자동 대체의 '처음 만듦' 예외가 이것만 본다
        checks["identity"] = identity_check(run, plan)
        judge_err += list(checks["identity"].get("judge_errors") or [])
        if files["final.xyz"]:
            raw_last = None
            if files["traj.xyz"]:
                try:
                    raw_last = read(str(run / "traj.xyz"), index=-1)
                except Exception as e:
                    raw_last = None                          # final_structure_check 가 '대조하지 못했다' 로 invalid 를 낸다
                    judge_err.append(f"traj 마지막 프레임 읽기 {type(e).__name__}: {str(e)[:80]}")
            checks["final_structure"] = final_structure_check(run, plan, v, raw_last)
            judge_err += list(checks["final_structure"].get("judge_errors") or [])
        res = combine_stage1(plan, v, gate, melt, seedg, files, checks=checks)
        res.update({"run": str(run), "gate_check": gate, "melt_window_check": melt, "checks": checks,
                    "seed_gate_view": (seedg or {}).get(v["seed_gate"]["version"])})
    res["provenance"] = {"files_sha256": run_provenance(run), "card_values_sha16": values_sha16(v), "driver_sha16": driver_sha16(),
                         "judge_values_sha16": judge_values_sha16(v),   # ⭐ DR 전 5차 리뷰 P2 — 판정 규칙만의 지문
                         "band_sha16": band_card_sha16() if band_read else BAND_NOT_READ, "runtime": judge_runtime(),
                         "folder": [run.parent.name, run.name], "derived_written": derived_written,   # ⭐ DR 전 리뷰 P3-A — 폴더 이름도 판정 입력 (식별)
                         "judge_nature": {"errors": judge_err, "input_mismatch": input_mismatch},
                         "⛔": "묶음 판정 (stage1_summary) 이 이 지문을 지금 파일 · 카드 값 · 도구 · G4 밴드 카드와 다시 잰다 — 안 맞으면 그 시드는 "
                               "무효 (다시 판정) · 비과학적 판정을 과학적 판정이 자동 대체하는 것은 judge_nature.errors 가 있고 input_mismatch 가 "
                               "없고 판정이 읽은 입력 전부가 같을 때만 (supersede_block · 회신 DQ P1-1)"}
    res["reason"] = reason
    vf = run / "stage1_verdict.json"
    if vf.is_file():
        try:                                                 # ⭐ 회신 DO P1 — 엄격히 읽는다 · 못 읽으면 원문 그대로 이력에 (마지막 값으로 정규화하지 않는다)
            prev = loads_strict(vf.read_text(encoding="utf-8"))
            if not isinstance(prev, dict):
                raise ValueError("이전 판정이 객체가 아니다")
        except (ValueError, UnicodeDecodeError, RecursionError) as e:
            raw_ = vf.read_bytes()                           # ⭐ DP 전 리뷰 (둘째) — 원문은 바이트 그대로 (base64 · 글자 치환으로 잃지 않는다)
            prev = {"status": None, "⛔": f"이전 판정 파일을 못 읽었다 ({type(e).__name__}: {str(e)[:60]}) — 원문을 raw_b64 (바이트 그대로) 로 남긴다",
                    "raw_b64": base64.b64encode(raw_).decode("ascii"), "raw_sha256": hashlib.sha256(raw_).hexdigest(),
                    "raw_text_head": raw_.decode("utf-8", errors="replace")[:400]}
        h = _append_history(run, prev, res, reason)
        res["history"] = {"file": VERDICT_HISTORY, "prev_status": h["prev_status"], "changed": h["changed"]}
    else:
        _append_history_first(run, res, reason)              # ⭐ DQ 전 5차 리뷰 P2 — 첫 판정도 이력에 (판정 파일이 지워져도 사슬에 남는다)
    tmp = vf.with_name(vf.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(res, ensure_ascii=False, indent=1, default=str))
        _fsync_handle(fh)
    os.replace(tmp, vf)
    _fsync_dir(run)
    log(f"  [stage1] {run} → {res['status']}" + (" · ⛔ 그 계를 닫는 사건" if res.get("closes_system") else "") + "  "
        + "; ".join(str(x) for k in ("invalid", "incomplete", "fail") for x in res["reasons"].get(k, [])))
    return res


def summarize_stage1(verdicts, values, cost=None):
    """li2s-2 1 단계 묶음 판정 (회신 DF P1-3 · 회신 DG P0-1 · P0-3 · P1-5) — verdicts: {(계, 시드): stage1_verdict dict 또는 None}.

    계마다: invalid 가 있으면 invalid · 첫 시드 녹음 미충족 (closes_system) 이면 그 계 닫힘 · 탈락이 (시드 수 − need) 를 넘으면 탈락 ·
    **선언된 시드가 전부 판정 끝 (pass · fail)** 이고 pass ≥ need 면 통과 · 아니면 대기 (missing · incomplete 가 남음).
    허용 상태 밖 ('unknown' 등) 은 invalid. 한쪽 계라도 닫힘 · 탈락이면 비교 트랙 전체 멈춤.
    cost = {"total_h", "cap_h"} (러너 비용 장부) — total > cap 이면 '상한 · 미완결' (통과로 올리지 않는다) · None 이면 상한을 확인하지
    못했으므로 두 계가 통과여도 1 단계 통과로 올리지 않는다 (대기). 두 계 통과면 2 단계 시드 = 두 계 **모두** 통과한 시드 중 작은 둘 ·
    기계는 그 순서로 (카드 stage2_machines)."""
    seeds, need = list(values["seeds"]), int(values["stage1_need_pass"])
    per, sw_seen, unknown, ident = {}, {}, [], []
    rid_at = {}
    for (s, sd), vv in verdicts.items():                  # 회신 DH P0-2 — 같은 실행을 여러 시드로 세지 않는다
        if vv is not None and vv.get("run_id"):
            rid_at.setdefault(vv["run_id"], []).append(f"{s}{sd}")
    dup = {k: x for k, x in rid_at.items() if len(x) > 1}
    led_closing = [(x[0], x[1]) for x in ((cost or {}).get("closing") or []) if isinstance(x, (list, tuple)) and len(x) >= 2]
    for s in ("A", "B"):
        st, closed = {}, sorted({sd for (s_, sd) in led_closing if s_ == s and sd == values.get("first_seed")})
        for sd in seeds:
            vv = verdicts.get((s, sd))
            x = "missing" if vv is None else vv.get("status")
            if x not in LI2S2_STATUSES and x != "missing":
                unknown.append(f"{s}{sd}={x!r}"); x = "invalid"
            if vv is not None and x != "missing":
                if vv.get("system") is not None and (vv.get("system"), vv.get("seed")) != (s, sd):
                    ident.append(f"{s}{sd} 자리의 판정이 ({vv.get('system')}, {vv.get('seed')}) 런이다"); x = "invalid"
                if vv.get("run_id") in dup:
                    ident.append(f"{s}{sd} 의 run_id 가 {dup[vv['run_id']]} 와 같다 (한 실행을 여러 시드로)"); x = "invalid"
            st[sd] = x
            if vv is not None and vv.get("closes_system") is True and sd != values.get("first_seed"):   # ⭐ DQ 전 리뷰 P2-D — 첫 시드만 닫는다
                ident.append(f"{s}{sd} 판정에 closes_system 이 있다 — 첫 시드 ({values.get('first_seed')}) 가 아니다 (기록 오류)"); st[sd] = "invalid"
            elif vv is not None and vv.get("closes_system") is True and sd not in closed:
                closed.append(sd)
        n_pass = sum(1 for x in st.values() if x == "pass")
        n_fail = sum(1 for x in st.values() if x == "fail")
        n_bad = sum(1 for x in st.values() if x == "invalid")
        n_open = sum(1 for x in st.values() if x in ("missing", "incomplete"))
        status = ("invalid" if n_bad else "closed" if closed else "fail" if n_fail > len(seeds) - need
                  else "pass" if (n_open == 0 and n_pass >= need) else "pending")
        per[s] = {"status": status, "per_seed": st, "n_pass": n_pass, "n_fail": n_fail, "n_open": n_open,
                  "closed_by_first_seed": closed}
        for sd in seeds:
            vv = verdicts.get((s, sd)) or {}
            if vv.get("status") == "pass":
                sw = {k: x for k, x in (vv.get("software") or {}).items()}
                sw_seen[json.dumps(sw, sort_keys=True)] = sw
    out = {"per_system": per, "software_variants": list(sw_seen.values()), "stage2": None, "unknown_status": unknown,
           "identity_problems": ident, "cost": cost}
    led_bad = list((cost or {}).get("invalid") or [])
    led_open = list((cost or {}).get("pending") or [])
    over = bool(cost is not None and not (_fin(cost.get("total_h")) and _fin(cost.get("cap_h"))
                                         and float(cost["total_h"]) <= float(cost["cap_h"])))
    if any(per[s]["status"] == "invalid" for s in per) or len(sw_seen) > 1 or led_bad:
        out["track"] = "invalid"
        out["why"] = ("카드와 다른 실행 · 원자료와 안 맞는 판정 · 실행 식별 불일치 · 모르는 판정 상태 · 장부 불완전 · 또는 통과 시드의 소프트웨어 판이 "
                      "둘 이상 — 자료 · 기록 오류 (과학적 판정 아님) · 고친 뒤 다시"
                      + (f" (모르는 상태 {unknown})" if unknown else "") + (f" (식별 {ident})" if ident else "")
                      + (f" (장부 {led_bad})" if led_bad else ""))
    elif any(per[s]["status"] == "closed" for s in per):
        out["track"] = "stop_track"
        out["why"] = ("계의 첫 시드 녹음 판정 미충족 → 그 계 닫힘 → 두 계 비교 트랙 전체 멈춤 (회신 DG P0-1 · 재시작으로 다시 열지 않는다) — "
                      + " · ".join(f"{s}{per[s]['closed_by_first_seed']}" for s in per if per[s]["closed_by_first_seed"]))
    elif any(per[s]["status"] == "fail" for s in per):
        out["track"] = "stop_track"; out["why"] = "한쪽 계가 1 단계에서 닫혔다 → 두 계 비교 트랙 전체 멈춤 (회신 DF P1-3)"
    elif over:
        out["track"] = "cap_incomplete"
        out["why"] = (f"비용 장부 {cost.get('total_h')} h > 상한 {cost.get('cap_h')} h (또는 비유한) — 1 단계 미완결 · "
                      "그때 끝난 시드만 골라 판정하지 않는다 (회신 DG P0-3)")
    elif all(per[s]["status"] == "pass" for s in per):
        common = sorted(sd for sd in seeds if per["A"]["per_seed"][sd] == "pass" and per["B"]["per_seed"][sd] == "pass")
        if cost is None:
            out["track"] = "pending"; out["why"] = "두 계 모두 통과지만 비용 장부를 못 봤다 — 상한 안인지 확인 전에는 1 단계 통과로 올리지 않는다"
        elif led_open:
            out["track"] = "pending"; out["why"] = f"두 계 모두 통과지만 장부에 비용이 확정 안 된 런이 있다 ({led_open}) — 통과로 올리지 않는다"
        elif len(common) < 2:
            out["track"] = "stop_track"; out["why"] = f"두 계 공통 통과 시드가 {len(common)} 개 — 2 단계에 둘이 필요하다"
        else:
            m = list(values["stage2_machines"])
            out["track"] = "stage1_pass"
            out["stage2"] = {"seeds": common[:2], "machines": {str(sd): m[i] for i, sd in enumerate(common[:2])},
                             "common_pass_seeds": common, "rule": "두 계 모두 통과한 시드 중 작은 둘 · 기계는 그 순서"}
            out["why"] = "두 계 모두 통과 (선언된 시드 전부 판정 끝 · 비용 상한 안)"
    else:
        out["track"] = "pending"
        out["why"] = "시드 판정이 덜 끝났다 (미판정 · 미완이 남으면 통과로 올리지 않는다 — 회신 DG P1-5)"
    ts_ = (cost or {}).get("terminal_stop")
    if ts_ and out["track"] != "stop_track":                # ⭐ DQ 전 리뷰 P2-D — 닫는 STOP 인데 기록 판정은 닫힘이 아니다 = 기록이 안 맞는다
        out.update(track="invalid", stage2=None,
                   why=f"STOP 은 닫힘 ({ts_}) 인데 기록으로 낸 묶음 판정은 {out['track']} — 기록이 안 맞는다 (STOP · 장부 · 판정 · 사람이 본다)")
    return out


def attempt_inventory(out_root):
    """현재 · 보존된 시드 폴더의 실행을 읽는다. plan 이 아직 없어도 실행 전 기록으로 장부와 잇는다.
    기록을 모두 지우거나 root 밖으로 옮긴 실행을 복원하는 도구는 아니다. 기존 plan-only 실행은 신원을 읽되 추정하지 않는다.
    """
    found, invalid = {}, []
    root = pathlib.Path(out_root)
    for system in ("A", "B"):
        parent = root / system
        if not parent.is_dir():
            continue
        for rd in sorted(parent.iterdir()):
            if not rd.is_dir():
                continue
            ids, att_rec = [], None
            for name in (ATTEMPT_NAME, "plan.json"):
                p = rd / name
                if not p.is_file():
                    continue
                try:
                    rec = loads_strict(p.read_text(encoding="utf-8"))   # ⭐ 회신 DO P1
                    rid, sysn, seed = rec.get("run_id"), rec.get("system"), rec.get("seed")
                    if not (isinstance(rid, str) and RUN_ID_RE.fullmatch(rid)
                            and sysn == system and type(seed) is int):
                        raise ValueError("실행 식별 필드 불일치")
                except (OSError, ValueError, AttributeError, RecursionError) as e:
                    invalid.append(f"{p}: 실행 신원을 못 읽음 ({type(e).__name__})")
                    continue
                ids.append((rid, sysn, seed))
                if name == ATTEMPT_NAME:
                    att_rec = {k: rec.get(k) for k in ("retry_of", "retry_stop_id", "retry_kind")}
            if len(set(ids)) > 1:
                invalid.append(f"{rd}: 실행 전 기록과 plan 신원이 다름")
            for rid, sysn, seed in set(ids):
                if rid in found:
                    invalid.append(f"run_id {rid} 산출물 폴더가 둘: {found[rid]['path']} · {rd}")
                found[rid] = {"system": sysn, "seed": seed, "path": str(rd), "attempt": att_rec}
    return found, invalid


MD_DONE_NAME = "md_done.json"   # 회신 DK P0-1 · P1-1 — run_melt_quench 가 MD 루프 직후 (FIRE 전) 원자적으로 쓰는 완료 기록
MD_DONE_TMP = MD_DONE_NAME + ".tmp"   # 회신 DL P0 — 이것이 남아 있으면 기록 도중 끊김 (완료로 승인하지 않고 보류)
NON_MD_FILES = frozenset({ATTEMPT_NAME, ATTEMPT_NAME + ".tmp", "stage1_verdict.json", "stage1_verdict.json.tmp", VERDICT_HISTORY})
MID_RUN_FILES = frozenset({"plan.json", "initial.xyz", "prerelax.log", "traj.xyz", "thermo.csv"}) | NON_MD_FILES
# ⭐ DO 전 리뷰 F1 — plan 이 있는데 완료 기록이 없는 폴더에 있어도 되는 것 = 드라이버가 MD 루프가 끝나기 전에 쓰는 것 + 실행 전 · 판정 기록.
#   그 밖의 것 (md_init_raw.xyz · gate_check.json · seed_gate.json · final.vasp · gr_partials.csv · 모르는 파일) 이 하나라도 있으면 보류
#   — MD 뒤 산출물에는 일정 끝이 적혀 있을 수 있다.
# ⭐ 회신 DL P0 — plan.json 이 없는 폴더에 있어도 되는 것 = MD 산출물이 아닌 기록 (러너의 실행 전 기록 · 판정 기록). 그 밖의 것이 하나라도 있으면 보류


PLAN_NUM_MAX = 1.0e7   # ps · fs — 일정 값이 이보다 크면 손상으로 본다 (스텝 수가 넘치는 것을 막는다)


def _plan_num(plan, k, *, positive=False):
    """plan 의 일정 값 하나 — 수 타입 · 유한 · (positive 면 > 0 · 아니면 ≥ 0) · ≤ PLAN_NUM_MAX. 아니면 ValueError (보류 갈래로).
    ⭐ DO 전 리뷰 F5 — '1' · true · ' 2 ' 를 수로 바꿔 읽지 않고 · save_ps 0 · 음수 dt · hold 를 받아 주지 않는다."""
    x = plan.get(k) if isinstance(plan, dict) else None
    if not _fin(x) or not (float(x) > 0 if positive else float(x) >= 0) or float(x) > PLAN_NUM_MAX:
        raise ValueError(f"plan {k} = {x!r} — {'양수' if positive else '0 이상'} 수가 아니다 (글자 · 참거짓 · 비유한 · 너무 큰 값 안 받음)")
    return float(x)


def planned_md_steps(plan):
    """plan 의 일정에서 MD 스텝 수 — run_melt_quench 와 같은 셈 (단계마다 반올림한 스텝 수의 합). 일정 값이 수가 아니면 ValueError."""
    dt = _plan_num(plan, "dt_fs", positive=True)
    return sum(int(round(_plan_num(plan, k) * 1000.0 / dt)) for k in ("melt_ps", "quench_ps", "hold_ps"))


def save_interval_steps(plan):
    """plan 의 저장 간격 (스텝) — run_melt_quench 의 save_int 와 같은 셈. 일정 값이 수가 아니거나 0 이하면 ValueError."""
    return max(1, int(round(_plan_num(plan, "save_ps", positive=True) * 1000.0 / _plan_num(plan, "dt_fs", positive=True))))


def _fsync_file(path):
    """파일 내용을 저장장치로 보낸다 (fsync). Windows 는 쓰기 핸들이 있어야 해서 O_RDWR 로 연다 — 내용은 안 바꾼다."""
    fd = os.open(str(path), os.O_RDWR | getattr(os, "O_BINARY", 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _fsync_handle(fh):
    """열린 파일을 비우고 저장장치로 (flush + fsync)."""
    fh.flush()
    os.fsync(fh.fileno())


def _fsync_dir(path):
    """디렉터리 항목 (이름 교체) 을 저장장치로. ⛔ Windows 에는 디렉터리 fsync 가 없다 — 건너뛰고 False (생산은 Linux 뿐)."""
    if os.name == "nt":
        return False
    fd = os.open(str(path), os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    return True


def write_md_done(out, *, run_id, n_steps_planned, n_steps_done):
    """MD 루프가 끝난 **직후** (FIRE 전) 의 완료 기록 — run_id · 계획 · 실제 스텝 · traj.xyz · thermo.csv 해시.
    ⭐ 회신 DK: MD 완료의 증거는 이 기록이다 (프레임 수가 아니다 — 저장 간격이 스텝을 못 나누면 마지막 저장 뒤 구간을 못 가른다).
    ⭐ 회신 DL P1-1 — 순서: traj.xyz · thermo.csv fsync → 해시 → 임시 기록 쓰기 · fsync → os.replace → 부모 디렉터리 fsync.
      어느 단계든 실패하면 예외가 그대로 올라간다 (드라이버가 죽는다 = FIRE 안 함). 그때 폴더는 셋 중 하나이고 셋 다 보류다
      (folder_stage): 임시 기록만 남음 · 기록 있음 (md_complete) · 둘 다 없음 + 마지막 저장이 끝 경계 (완료 여부 불명).
    ⛔ 못 하는 것: fsync 가 실제 저장장치에 닿는지는 파일시스템 · 장치 쓰기 캐시에 달렸다 — kgy 에서 전원을 끊어 확인한 적이 없으니
      정전 뒤 기록이 남는다고 보증하지 않는다 (손실 확률 · 창 길이를 주장하지 않는다). 기록이 없을 때의 판독 (끝 경계 → 보류) 이 그 빈자리를 맡는다.
      Windows 에서는 디렉터리 fsync 를 건너뛴다.
      저장 간격이 스텝 수를 못 나누면 궤적 끝 프레임은 MD 끝 구조가 아니다 (회신 DL Q1 · 카드의 1 ps 일정은 끝점이 저장된다) —
      완료 사실의 확인과 종료 구조의 복구는 별개다."""
    out = pathlib.Path(out)
    for nm in ("traj.xyz", "thermo.csv"):
        if (out / nm).is_file():
            _fsync_file(out / nm)
    rec = {"run_id": run_id, "n_steps_planned": int(n_steps_planned), "n_steps_done": int(n_steps_done),
           "traj_sha256": _sha256_file(out / "traj.xyz") if (out / "traj.xyz").is_file() else None,
           "thermo_sha256": _sha256_file(out / "thermo.csv") if (out / "thermo.csv").is_file() else None,
           "at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")}
    tmp = out / MD_DONE_TMP
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False))
        _fsync_handle(fh)
    os.replace(tmp, out / MD_DONE_NAME)
    _fsync_dir(out)
    return rec


def _junk(line):
    """NUL · 공백뿐인 줄 (정전 뒤 파일 꼬리에 생기는 모양) — 건너뛴다. 그래서 NUL 만 남은 꼬리는 진행량에 안 들어간다 (복원하지 못한다 · 회신 DN P2)."""
    return not line.strip("\x00 \t\r")


def _thermo_last_step(path, plan):
    """thermo.csv 에서 **시작된** 마지막 기록의 스텝 — (스텝 | None, 문제 | None).
    온전한 행은 시각이 저장 간격대로 (t_k = k · 저장 간격) 이고 줄이 이어져야 한다. 꼬리가 아닌 자리에서 깨지면 문제 (보류).
    ⭐ 회신 DM P0-1 — 마지막 비어 있지 않은 줄 (꼬리) 은 '온전하지만 순서가 다른 행' 과 '덜 써진 행' 을 가른다:
      · 첫 칸 (시각) 이 다 써졌다 (쉼표가 있다) → 그 시각이 다음 기록 시각이어야 시작된 기록으로 센다 · 다르면 **보류**
        (그 줄에 남은 시각이 끝 시각일 수 있다 — 버리지 않는다)
      · 첫 칸이 쓰이다 말았다 (쉼표 없음) → 다음 기록 시각 문자열 (드라이버 꼴 '%.3f') 의 앞부분이어야 센다 · 아니면 보류
      · NUL 뒤에 다른 글자가 있다 · 앞 줄과 이어지지 않는다 → 보류"""
    save_int, dt = save_interval_steps(plan), _plan_num(plan, "dt_fs", positive=True)
    raw = path.read_bytes()
    lines = raw.decode("utf-8", errors="replace").split("\n")
    idx = [i for i, ln in enumerate(lines) if not _junk(ln)]
    if not idx:
        if raw:                                        # ⭐ DO 전 리뷰 F7 — 크기는 있는데 읽을 줄이 없다 (NUL · 공백뿐) → 진행량을 모른다
            return None, f"thermo.csv 가 비어 있지 않은데 ({len(raw)} B) 읽을 줄이 없다 (NUL · 공백뿐) — 진행량을 복원하지 못한다"
        return None, None
    if idx[0] != 0 or lines[0].split(",")[0].strip() != "t_ps":
        return None, "thermo.csv 첫 줄이 머리 (t_ps,…) 가 아니다"
    t_of = lambda k: k * save_int * dt / 1000.0
    n, prev, body = 0, 0, idx[1:]
    for j, i in enumerate(body):
        ln = lines[i]
        try:
            t = float(ln.split(",")[0])
            ok = ("\x00" not in ln and math.isfinite(t) and i == prev + 1 and abs(t - t_of(n)) <= 1.5e-3)
        except ValueError:
            ok = False
        if ok:
            n, prev = n + 1, i
            continue
        if j < len(body) - 1:
            return None, f"thermo.csv {i + 1} 번째 줄이 깨졌다 (꼬리가 아니다) — 진행량을 못 읽는다"
        if i != prev + 1:                              # ── 꼬리 (마지막 비어 있지 않은 줄)
            return None, f"thermo.csv 마지막 줄 ({i + 1}) 이 앞 줄과 이어지지 않는다 — 진행량을 못 정한다"
        frag, _, rest = ln.partition("\x00")
        if rest.strip("\x00 \t\r"):
            return None, "thermo.csv 마지막 줄에 NUL 뒤 글자가 있다 — 진행량을 못 정한다"
        head, want = frag.rstrip("\r").split(",", 1)[0].strip(), f"{t_of(n):.3f}"
        if "," in frag:
            try:
                tt = float(head)
            except ValueError:
                return None, f"thermo.csv 마지막 줄 첫 칸 {head!r} 을 못 읽는다 — 진행량을 못 정한다"
            if not (math.isfinite(tt) and abs(tt - t_of(n)) <= 1.5e-3):
                return None, (f"thermo.csv 마지막 줄 시각 {head} 이 다음 기록 시각 ({want}) 과 다르다 — "
                              "남은 시각을 버리지 않는다 (끝 시각일 수 있다)")
        elif not (head and want.startswith(head)):
            return None, f"thermo.csv 마지막 줄 조각 {head!r} 이 다음 기록 시각 ({want}) 의 앞부분이 아니다 — 진행량을 못 정한다"
        n += 1                                         # 다음 기록이 시작됐다 (덜 써진 행 · 첫 칸이 맞다)
        break
    return ((n - 1) * save_int if n else None), None


def _traj_last_step(path, plan):
    """traj.xyz (extxyz) 에서 **시작된** 마지막 프레임의 스텝 — (스텝 | None, 문제 | None). 프레임 수로 완료를 승인하지 않는다
    (회신 DK P1-1) — 이것은 '끝까지 갔을 수도 있다' 를 가려 보류하는 데만 쓴다 (회신 DL Q2). 덜 써진 마지막 프레임도 시작된 기록으로 센다."""
    save_int = save_interval_steps(plan)
    raw = path.read_bytes()
    lines = raw.decode("utf-8", errors="replace").split("\n")
    last = max((i for i, ln in enumerate(lines) if not _junk(ln)), default=-1)
    if last < 0 and raw:                                 # ⭐ DO 전 리뷰 F7 — 크기는 있는데 읽을 줄이 없다
        return None, f"traj.xyz 가 비어 있지 않은데 ({len(raw)} B) 읽을 줄이 없다 (NUL · 공백뿐) — 진행량을 복원하지 못한다"
    i, n, nat0 = 0, 0, None
    while i <= last:
        try:
            nat = int(lines[i].strip())
        except ValueError:
            nat = None
        if nat is None or nat <= 0 or (nat0 is not None and nat != nat0):
            if nat0 is not None and last - i + 1 < nat0 + 2:   # 덜 써진 마지막 프레임 (머리째 잘림)
                n += 1
                break
            return None, f"traj.xyz {i + 1} 번째 줄에서 프레임 머리가 깨졌다 (꼬리가 아니다) — 진행량을 못 읽는다"
        if i + nat + 1 > last:                           # 덜 써진 마지막 프레임
            n += 1
            break
        nat0, n, i = nat, n + 1, i + nat + 2
    return ((n - 1) * save_int if n else None), None


def md_last_recorded_step(folder, plan):
    """완료 기록이 없을 때만 쓰는 **보조** 판독 (회신 DL Q2) — 보류 판단용이지 완료 승인용이 아니다.
    thermo.csv · traj.xyz 에서 시작된 마지막 기록의 스텝 (둘 중 큰 값 — 보수적). 반환 (스텝 | None (MD 기록 전), 문제 | None).
    ⛔ 못 하는 것: 정전으로 저장 안 된 꼬리 (fsync 전 쓰기) 는 사라진다 — 그러면 실제보다 앞에서 끊긴 것으로 읽힌다 (회신 DL Q2 가 받아들인 한계) ·
    NUL 만 남은 꼬리도 진행량을 복원하지 못한다 (시각의 유효한 앞부분이 남은 꼬리만 센다 · 회신 DN P2) · 두 파일 중 큰 값은 보수적 판독이지
    두 파일의 완전성 증명이 아니다 (회신 DN Q2)."""
    f, best = pathlib.Path(folder), None
    for nm, fn in (("thermo.csv", _thermo_last_step), ("traj.xyz", _traj_last_step)):
        p = f / nm
        if not os.path.lexists(p):
            continue
        try:
            st, prob = fn(p, plan)
        except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError) as e:
            return None, f"{nm} 를 못 읽는다 ({type(e).__name__})"
        if prob:
            return None, prob
        if st is not None:
            best = st if best is None else max(best, st)
    return best, None


PRE_RUN_VERDICT_KEYS = frozenset({"status", "reasons", "run", "provenance", "reason", "history"})   # stage1_verdict 가 plan 없는 폴더에 쓰는 열쇠
PRE_RUN_PROVENANCE_KEYS = frozenset({"files_sha256", "card_values_sha16", "driver_sha16", "⛔",
                                     "band_sha16", "runtime", "derived_written", "judge_nature", "folder", "judge_values_sha16"})   # ⭐ 회신 DQ P1-1 · DR 전 리뷰 — 판정 입력 · 성격 칸


def _verdict_is_pre_run(v):
    """plan 전 끊김에서만 생기는 판정인가 — stage1_verdict 가 plan.json 없는 폴더에 쓰는 꼴 그대로 (회신 DM P0-2):
    status incomplete · 이유가 정확히 {"incomplete": ["plan.json 없음"]} (다른 열쇠 · 빈 값 · 다른 타입이 섞이면 아니다 — 회신 DN P1) ·
    원자료 지문 (PROVENANCE_FILES) 이 전부 있고 전부 None."""
    if not isinstance(v, dict) or v.get("status") != "incomplete" or not set(v) <= PRE_RUN_VERDICT_KEYS:
        return False                                          # ⭐ DO 전 리뷰 F3 — 진짜 함수가 안 쓰는 열쇠 (gate_check · checks 등) 가 붙으면 아니다
    if not all(v.get(k) is None or isinstance(v.get(k), str) for k in ("run", "reason")):
        return False
    hs = v.get("history")
    if hs is not None and not (isinstance(hs, dict) and hs.get("prev_status") in (None, "incomplete")):
        return False                                          # 재판정 요약에 이전 과학적 판정 · 다른 꼴이 적혀 있으면 plan 전 판정이 아니다
    rs = v.get("reasons")
    if rs != {"incomplete": ["plan.json 없음"]}:
        return False
    pv = v.get("provenance")
    if not (isinstance(pv, dict) and set(pv) <= PRE_RUN_PROVENANCE_KEYS):
        return False
    fs = pv.get("files_sha256")
    return isinstance(fs, dict) and set(PROVENANCE_FILES) <= set(fs) and all(fs.get(x) is None for x in PROVENANCE_FILES)


def _verdict_records(folder):
    """판정 기록 — 현재 판정 · 이력 줄마다 이전 판정 (전체) 과 새 판정 (상태 · 지문만) · (목록 [(어디, 기록, 부분인가)], 문제 | None).
    판정 임시 파일이 남았거나 (그 안에 완료 판정이 있을 수 있다) 못 읽는 기록이 있으면 문제 (회신 DM P0-2)."""
    f = pathlib.Path(folder)
    vf = f / "stage1_verdict.json"
    if os.path.lexists(vf.with_name(vf.name + ".tmp")):
        return [], "판정 임시 파일 (stage1_verdict.json.tmp) 이 남았다 — 판정 도중 끊김 · 그 안에 완료 판정이 있을 수 있다"
    recs = []
    if os.path.lexists(vf):
        try:                                                 # ⭐ 회신 DO P1 — 같은 열쇠 둘 (n 130 · 71) 을 마지막 값으로 읽지 않는다
            v = loads_strict(vf.read_text(encoding="utf-8"))
        except (OSError, ValueError, RecursionError) as e:
            return [], f"판정 파일을 못 읽는다 ({type(e).__name__}: {str(e)[:60]})"
        recs.append(("현재 판정", v, False))
    hp = f / VERDICT_HISTORY
    if os.path.lexists(hp):
        try:
            hl = hp.read_text(encoding="utf-8").split("\n")    # ⭐ DP 전 리뷰 (둘째) — splitlines 는 글자 안의 U+2028 · U+0085 에서도 자른다
        except (OSError, ValueError):
            return [], "판정 이력을 못 읽는다"
        for k, ln in enumerate(hl, 1):
            if not ln.strip():
                continue
            try:
                h = loads_strict(ln)                             # ⭐ 회신 DO P1
            except (ValueError, RecursionError) as e:
                return [], f"판정 이력 {k} 번째 줄을 못 읽는다 ({type(e).__name__}: {str(e)[:60]})"
            if not isinstance(h, dict):
                return [], f"판정 이력 {k} 번째 줄이 객체가 아니다"
            if "new_closes_system" in h and type(h.get("new_closes_system")) is not bool:   # ⭐ DR 전 3차 리뷰 P2 — 닫힘 표시는 참거짓만
                return [], f"판정 이력 {k} 번째 줄의 new_closes_system {h.get('new_closes_system')!r} 가 참거짓이 아니다 — 해석할 수 없는 기록"
            if h.get("first") is True:                       # ⭐ DQ 전 5차 리뷰 P2 — 첫 판정 줄 (앞 판정 없음 · prev 가 있으면 해석할 수 없다)
                if "prev" in h or h.get("new_status") not in LI2S2_STATUSES:
                    return [], f"판정 이력 {k} 번째 줄 (첫 판정) 의 꼴이 아니다 (prev 가 있거나 상태 {h.get('new_status')!r} 를 모른다)"
                recs.append((f"판정 이력 {k} 의 첫 판정", {"status": h.get("new_status"), "provenance": h.get("new_provenance"),
                                                         "closes_system": h.get("new_closes_system")}, True))
                continue
            pv_ = h.get("prev")
            if not isinstance(pv_, dict):                    # ⭐ DQ 전 리뷰 P2-C — prev 없음 · null · 객체 아님 = 해석할 수 없는 기록 (_run_kind 와 같은 판독)
                return [], f"판정 이력 {k} 번째 줄의 prev 가 객체가 아니다 ({type(pv_).__name__}) — 해석할 수 없는 기록"
            if pv_.get("status") is not None and pv_.get("status") not in LI2S2_STATUSES:
                return [], f"판정 이력 {k} 번째 줄의 이전 판정 상태 {pv_.get('status')!r} 를 모른다 — 해석할 수 없는 기록"
            if h.get("new_status") not in LI2S2_STATUSES:
                return [], f"판정 이력 {k} 번째 줄의 새 판정 상태 {h.get('new_status')!r} 를 모른다 — 해석할 수 없는 기록"
            if ("prev_status" in h and h.get("prev_status") != pv_.get("status")
                                          or "prev_provenance" in h and h.get("prev_provenance") != (pv_.get("provenance") or {})):
                return [], f"판정 이력 {k} 번째 줄의 prev_status · prev_provenance 가 prev 와 다르다 — 해석할 수 없는 기록"   # ⭐ DO 전 리뷰 F4
            recs.append((f"판정 이력 {k} 의 이전 판정", pv_, False))
            recs.append((f"판정 이력 {k} 의 새 판정", {"status": h.get("new_status"),   # 지문은 그대로 — 타입이 틀리면 검사가 보류한다 (회신 DN P1)
                                                   "provenance": h.get("new_provenance"), "closes_system": h.get("new_closes_system")}, True))
    return recs, None


def _completion_fields_problem(r, partial, where):
    """⭐ 회신 DN P1 — 완료 판단에 쓰는 판정 기록 필드의 꼴 (도중 끊김 후보에서). 반환: 문제 | None.
    없음 · None 은 허용 (그 흔적이 없다) · **있는데 타입이 다르거나 값이 말이 안 되면 해석할 수 없는 기록** (보류). 정수로 바꿔 읽지 않는다
    (n:"130" 은 130 이 아니라 못 읽는 값 · True 는 정수 자리에서 타입 오류).
      provenance → dict · files_sha256 → dict · final.xyz · result.json 지문 → 경로 상태 (없음 · 64 자리 16진수 · link: · nonfile: — path_state_problem)
      (전체 기록만) gate_check → dict · schedule_complete → bool · checks → dict · traj_frames → dict · n → 0 이상 정수 · expected → 1 이상 정수"""
    def bad(d, key, kinds, at):
        v = d.get(key)
        if v is None:
            return None
        if (isinstance(v, bool) and bool not in kinds) or not isinstance(v, kinds):
            return f"{at} 의 {key} 타입이 {type(v).__name__} 이다 (기대 {' · '.join(k.__name__ for k in kinds)}) — 해석할 수 없는 기록"
        return None
    p = bad(r, "provenance", (dict,), where)
    if p:
        return p
    pv = r.get("provenance") or {}
    p = bad(pv, "files_sha256", (dict,), f"{where} 의 provenance")
    if p:
        return p
    fs = pv.get("files_sha256") or {}
    for x in ("final.xyz", "result.json"):
        ph_ = path_state_problem(fs.get(x))                  # ⭐ 회신 DR P1-2 — 경로 상태 (link: · nonfile:) 도 알려진 값이다
        if ph_:
            return f"{where} 의 {x} {ph_} — 해석할 수 없는 기록"
    if partial:
        return None
    for key in ("gate_check", "checks", "history"):
        p = bad(r, key, (dict,), where)
        if p:
            return p
    p = bad(r.get("gate_check") or {}, "schedule_complete", (bool,), f"{where} 의 gate_check")
    if p:
        return p
    if (r.get("gate_check") or {}).get("error"):            # ⭐ DO 전 리뷰 (소비자 P1) — gate 오류 = 일정 끝 여부를 모른다 ('False' 로 읽지 않는다)
        return f"{where} 의 gate_check 에 오류가 적혀 있다 ({str(r['gate_check']['error'])[:60]}) — 일정 끝 여부를 모른다 · 해석할 수 없는 기록"
    p = bad(r.get("history") or {}, "prev_status", (str,), f"{where} 의 history")
    if p:
        return p
    ck = r.get("checks") or {}
    p = bad(ck, "traj_frames", (dict,), f"{where} 의 checks")
    if p:
        return p
    tf = ck.get("traj_frames") or {}
    for key, lo in (("n", 0), ("expected", 1)):
        p = bad(tf, key, (int,), f"{where} 의 traj_frames")
        if p:
            return p
        v = tf.get(key)
        if v is not None and v < lo:
            return f"{where} 의 traj_frames {key} = {v} 이 말이 안 된다 (≥ {lo} 이어야) — 해석할 수 없는 기록"
    return None


def _verdict_evidence(folder, pre_run_only):
    """판정 기록이 재시도 갈래 (plan 전 끊김 · 명확한 도중 끊김) 와 맞는가 — 맞지 않으면 그 이유 (보류 · 회신 DM P0-2).
      pre_run_only (no_plan 후보): 모든 기록이 plan 전 끊김의 판정이어야 한다 (_verdict_is_pre_run · 이력의 새 판정은 상태 · 지문으로)
      그 밖 (md_incomplete 후보): 모든 기록이 status incomplete · invalid 여야 하고 (pass · fail · 못 읽은 이전 판정 · 모르는 상태 = 보류 ·
        invalid 는 과학적 판정이 아니고 원인을 고친 재시도 경로가 있다) ·
        어느 기록에도 최종 산출물 (final.xyz · result.json) 지문이 없고 · 전체 기록 (현재 판정 · 이력의 이전 판정) 에 'MD 가 끝났다' 의
        흔적 (gate_check schedule_complete · 궤적 프레임 n ≥ 계획) 이 없어야 한다 — MD 완료 · FIRE 미완 폴더의 판정은 incomplete 인데 그 흔적을 담는다 ·
        그 흔적을 읽는 필드가 있는데 타입이 틀리면 (n:"130" 등) 해석할 수 없는 기록으로 보류 (_completion_fields_problem · 회신 DN P1)
    ⛔ 못 하는 것: 이력 파일 자체가 통째로 지워졌으면 모른다 (없는 기록은 못 읽는다) — '과거 완료가 없었다' 의 증명이 아니다 (회신 DN Q4)."""
    recs, prob = _verdict_records(folder)
    if prob:
        return prob
    plan_frames = None                                       # ⭐ DO 전 리뷰 F4 — 기록에 expected 가 없으면 plan 에서 (stage1_verdict 와 같은 셈)
    try:
        pl_ = loads_strict((pathlib.Path(folder) / "plan.json").read_text(encoding="utf-8"))
        if all(_fin(pl_.get(k)) for k in ("melt_ps", "quench_ps", "hold_ps", "save_ps")) and float(pl_["save_ps"]) > 0:
            plan_frames = int(round((float(pl_["melt_ps"]) + float(pl_["quench_ps"]) + float(pl_["hold_ps"])) / float(pl_["save_ps"]))) + 1
    except (OSError, ValueError, AttributeError, OverflowError, RecursionError):
        plan_frames = None
    for where, r, partial in recs:
        if not isinstance(r, dict):
            return f"{where} 을 못 읽는다"
        pv = r.get("provenance")
        fs = pv.get("files_sha256") if isinstance(pv, dict) else None
        st = r.get("status")
        if pre_run_only:
            ok = (st == "incomplete" and isinstance(fs, dict) and set(PROVENANCE_FILES) <= set(fs)
                  and all(fs.get(x) is None for x in PROVENANCE_FILES)) if partial else _verdict_is_pre_run(r)
            if not ok:
                return f"{where} 이 plan 전 끊김의 판정이 아니다 (상태 {st} · 이유 · 원자료 지문)"
        else:
            if st in ("pass", "fail"):
                return f"{where} 에 과학적 판정 ({st}) 이 있다"
            if st not in ("incomplete", "invalid"):          # 못 읽은 이전 판정 (status None · raw_b64 · 옛 raw_text) · 모르는 상태 — invalid 는 과학적
                return f"{where} 의 상태를 해석할 수 없다 ({st!r}) — 판정 기록을 못 읽은 채 도중 끊김으로 단정하지 않는다"   # 판정이 아니다 (재시도 경로)
            tp = _completion_fields_problem(r, partial, where)   # ⭐ 회신 DN P1 — 완료 판단 필드가 있는데 타입이 틀리면 해석할 수 없는 기록
            if tp:
                return tp
            if isinstance(fs, dict) and any(fs.get(x) for x in ("final.xyz", "result.json")):
                return f"{where} 에 최종 산출물 지문이 있다 (끝까지 돌았던 흔적)"
            if not partial:                                  # 전체 기록 — 'MD 는 끝났다' 의 흔적 (FIRE 미완 판정은 incomplete 다)
                gc = r.get("gate_check")
                if isinstance(gc, dict) and gc.get("schedule_complete"):
                    return f"{where} 에 일정 끝 (gate_check schedule_complete) 이 적혀 있다 — MD 가 끝났던 흔적"
                ck = r.get("checks")
                tf = ck.get("traj_frames") if isinstance(ck, dict) else None
                n_, ex_ = (tf.get("n"), tf.get("expected")) if isinstance(tf, dict) else (None, None)
                if type(n_) is int and type(ex_) is int and ex_ > 0 and n_ >= ex_:
                    return f"{where} 에 궤적 프레임이 다 찼다고 적혀 있다 ({n_}/{ex_}) — MD 가 끝났던 흔적"
                if type(n_) is int and ex_ is None and plan_frames and n_ >= plan_frames:
                    return f"{where} 에 궤적 프레임 {n_} 이 적혀 있다 (plan 계획 {plan_frames} 이상) — MD 가 끝났던 흔적"
                ck_ = r.get("checks") or {}
                for k_, why_ in (("final_structure", "최종 구조 판정"), ("seed_gate_error", "시드 게이트 오류")):
                    if ck_.get(k_) is not None:
                        return f"{where} 에 {why_} ({k_}) 이 적혀 있다 — final.xyz 가 있던 흔적"
                if r.get("seed_gate_view") is not None:
                    return f"{where} 에 시드 게이트 값 (seed_gate_view) 이 적혀 있다 — final.xyz 가 있던 흔적"
                if (r.get("history") or {}).get("prev_status") in ("pass", "fail"):
                    return f"{where} 의 재판정 요약에 이전 과학적 판정 ({r['history']['prev_status']}) 이 적혀 있다"
    return None


def folder_stage_detail(folder):
    """⭐ 회신 DJ Q2 · DK P0-1 · P1-1 · DL P0 · Q2 — 실행 폴더의 완료 단계와 그 이유 (재시도 자격 · 소비자가 같이 쓴다):
      'final'         result.json · final.xyz 가 있다 (재시도가 아니라 판정)
      'md_complete'   MD 완료 기록 (md_done.json) 이 맞다 — run_id = plan · 계획 = 실제 스텝 = plan 일정 · traj · thermo 해시 일치 (FIRE 미완 → 보류)
      'md_incomplete' **명확한 도중 끊김만** — plan 이 있고 · 완료 기록 · 임시 기록 · FIRE 로그가 없고 · 시작된 마지막 기록이 끝 경계
                      (계획 스텝 안의 마지막 저장 스텝) 보다 앞이거나 MD 기록이 아예 없다
      'no_plan'       plan.json 이 없고 폴더에 MD 산출물이 아닌 기록 (NON_MD_FILES) 밖의 것이 없고 · **판정 기록이 내용으로도 plan 전 것**
                      (현재 판정 · 이력의 이전 판정 = status incomplete · 'plan.json 없음' · 원자료 지문 전부 None · 판정 임시 파일 없음 — 회신 DM P0-2)
      'unreadable'    보류 — plan 을 못 읽음 · 완료 기록을 못 읽음 · 기록이 plan 과 다름 · 기록 뒤 궤적 · thermo 가 바뀜 ·
                      **임시 기록이 남음** · **plan 없이 산출물이 남음** · **FIRE 로그가 있는데 기록 없음** ·
                      **기록 없이 마지막 저장이 끝 경계에 닿음 (완료 여부 불명)** · 진행량을 못 읽음 (thermo 마지막 줄 시각이 다음 기록과
                      다름 포함 — 회신 DM P0-1) · **판정 기록에 과학적 판정 · 해석할 수 없는 상태 (못 읽은 이전 판정 포함) ·
                      최종 산출물 지문 · MD 완료 흔적 (일정 끝 · 프레임 다 참) · 임시 판정이 있음** (회신 DM P0-2) ·
                      **그 흔적의 필드가 있는데 타입이 틀림** (회신 DN P1)
    프레임 · 시각은 완료 승인에 안 쓴다 (회신 DK P1-1) — 끝까지 갔을 수도 있는 실행을 보류하는 데만 쓴다 (회신 DL Q2).
    ⭐ DO 전 리뷰 — plan 이 있는 도중 끊김 후보도 폴더의 파일 목록을 본다 (MID_RUN_FILES 밖이면 보류 · F1) · result.json · final.xyz 자리에
       파일이 아닌 것 (디렉터리 · 깨진 링크) 은 보류 (F2) · 판독 중 예외 (깊은 JSON 의 RecursionError · OverflowError 등) 는 분류 대신
       죽지 않고 보류 (F6)."""
    try:
        return _folder_stage_detail(folder)
    except Exception as e:                                   # ⭐ DO 전 리뷰 F6 — 판독 예외는 보류 (러너 · 소비자가 멈춰 서지 않게)
        return "unreadable", f"판독 예외 ({type(e).__name__}) — 보류"


def _folder_stage_detail(folder):
    f = pathlib.Path(folder)
    if any((f / x).is_file() for x in ("result.json", "final.xyz")):
        return "final", "result.json · final.xyz 가 있다"
    if any(os.path.lexists(f / x) for x in ("result.json", "final.xyz")):
        return "unreadable", "result.json · final.xyz 자리에 파일이 아닌 것 (디렉터리 · 깨진 링크) 이 있다 — 보류"
    if not (f / "plan.json").is_file():
        try:
            extra = sorted(p.name for p in f.iterdir() if p.name not in NON_MD_FILES)
        except OSError as e:
            return "unreadable", f"폴더를 못 읽는다 ({type(e).__name__})"
        if extra:
            return "unreadable", f"plan.json 없이 실행 산출물이 남았다 ({' · '.join(extra[:4])}) — 보류"
        ev = _verdict_evidence(f, pre_run_only=True)          # ⭐ 회신 DM P0-2 — 판정 기록은 이름이 아니라 내용으로
        if ev:
            return "unreadable", f"plan.json 이 없는데 {ev} — 보류"
        return "no_plan", "실행 전 · 판정 기록뿐 (plan 전에 끊김 · MD 산출물 없음 · 판정 기록도 plan 전 것)"
    try:
        plan = loads_strict((f / "plan.json").read_text(encoding="utf-8"))   # ⭐ 회신 DO P1 — 같은 열쇠 둘 = 못 읽음 (보류)
        want = planned_md_steps(plan)
        save_int = save_interval_steps(plan)
    except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError, AttributeError, OverflowError, RecursionError):
        return "unreadable", "plan.json 을 못 읽는다 (일정 · 저장 간격 — 수가 아닌 값 포함)"
    if os.path.lexists(f / MD_DONE_TMP):
        return "unreadable", "MD 완료 기록 임시 파일이 남았다 — 기록 도중 끊김 (완료로 승인하지 않고 보류)"
    md = f / MD_DONE_NAME
    if os.path.lexists(md):
        try:
            rec = loads_strict(md.read_text(encoding="utf-8"))
            rid = plan.get("run_id")
            ok = (isinstance(rec, dict) and isinstance(rid, str) and rid and rec.get("run_id") == rid
                  and type(rec.get("n_steps_planned")) is int and type(rec.get("n_steps_done")) is int
                  and rec["n_steps_planned"] == want and rec["n_steps_done"] == want
                  and (f / "traj.xyz").is_file() and rec.get("traj_sha256") == _sha256_file(f / "traj.xyz")
                  and (f / "thermo.csv").is_file() and rec.get("thermo_sha256") == _sha256_file(f / "thermo.csv"))
        except (OSError, ValueError, AttributeError):
            return "unreadable", "MD 완료 기록을 못 읽는다"
        return ("md_complete", "MD 완료 기록이 맞다 (FIRE 미완)") if ok else \
               ("unreadable", "MD 완료 기록이 plan · 궤적 · thermo 와 안 맞는다 (기록 뒤 바뀜 포함)")
    if os.path.lexists(f / "final_relax.log"):
        return "unreadable", "FIRE 로그가 있는데 MD 완료 기록이 없다 — 보류"
    try:
        extra = sorted(x.name for x in f.iterdir() if x.name not in MID_RUN_FILES)
    except OSError as e:
        return "unreadable", f"폴더를 못 읽는다 ({type(e).__name__})"
    if extra:                                                # ⭐ DO 전 리뷰 F1 — MD 뒤 산출물 · 모르는 파일
        return "unreadable", (f"완료 기록은 없는데 MD 중 기록 밖의 파일이 있다 ({' · '.join(extra[:4])}{' …' if len(extra) > 4 else ''}) — "
                              "MD 뒤 산출물 (seed_gate · g(r) · final.vasp 등) 일 수 있다 · 보류")
    last, prob = md_last_recorded_step(f, plan)
    if prob:
        return "unreadable", prob + " — 보류"
    end = (want // save_int) * save_int
    if last is not None and last >= end:
        return "unreadable", (f"완료 기록이 없는데 시작된 마지막 기록 (스텝 {last}) 이 끝 경계 (스텝 {end} · 계획 {want}) 에 닿았다 — "
                              "완료 여부 불명 (보류)")
    ev = _verdict_evidence(f, pre_run_only=False)            # ⭐ 회신 DM P0-2 — 판정 기록에 완료 흔적이 있으면 재시도 아님
    if ev:
        return "unreadable", f"진행 기록은 도중이지만 {ev} — 보류"
    if last is None:
        return "md_incomplete", "MD 기록 전에 끊김 (사전 이완 · 시작)"
    return "md_incomplete", f"명확한 도중 끊김 (시작된 마지막 기록 스텝 {last} < 끝 경계 {end})"


def folder_stage(folder):
    """완료 단계만 — folder_stage_detail 의 첫 값 (러너 · 소비자가 같이 쓴다)."""
    return folder_stage_detail(folder)[0]


def verdict_file_status(folder):
    """판정 파일 상태 — None (파일 없음) · 허용 상태 · 'unreadable' (있는데 못 읽음 · 모르는 상태). 회신 DJ P0-2: 없음과 판독 불가를 가른다."""
    vf = pathlib.Path(folder) / "stage1_verdict.json"
    if not vf.is_file():
        return None
    try:
        st = loads_strict(vf.read_text(encoding="utf-8")).get("status")
    except Exception:                                        # OSError · ValueError · AttributeError · RecursionError (DO 전 리뷰 F6)
        return "unreadable"
    return st if st in LI2S2_STATUSES else "unreadable"


RUN_STATUSES_ENDED = ("ended", "invalid")   # 장부 status — 끝난 런 · 러너가 녹음 invalid 로 멈춘 런 (이 둘의 invalid 판정만 실행 종류 invalid)


def run_kind(row, folder, values=None):
    """⭐ 회신 DK P0-2 · DO 전 리뷰 — 한 실행의 종류를 **한 곳에서** 정한다 (러너 재시도 자격 · 확인 때 선언 검사 · 소비자 이력 검사).
      'scientific'  장부 verdict · closes_system · melt_check (러너가 첫 시드 녹음 fail 로 멈춤) · 폴더 판정 기록 (현재 · 이력의 이전 · 새 판정)
                    어디든 pass · fail · (values 를 주면) 보존 폴더의 녹음 창이 다 찼고 fail
      'unreadable'  판정 기록 · 장부 값을 못 읽음 · 모르는 값 · 판정 임시 파일 · 판독 예외
      'invalid'     러너가 녹음 invalid 로 멈춤 (melt_check invalid) · **끝난 런 (status ended · invalid)** 의 invalid 판정 ·
                    (values) 보존 폴더의 녹음 판정 invalid
      'interrupted' 그 밖 — 끊긴 런 (interrupted · orphaned · stop_failed · cap …) 의 폴더를 판정해 invalid 가 나와도 종류는 끊긴 런이다
                    (일찍 끊긴 폴더 · 덜 써진 꼬리 · 보존 이름은 판정이 invalid 로 낼 수 있다 — 그것으로 끊긴 런 한도를 우회하지 않는다)"""
    return run_kind_detail(row, folder, values)[0]


MELT_OBSERVED_KEYS = ("verdict", "message", "D_framework_cm2_s", "window_used_ps", "n_frames_read", "estimator")


def run_kind_detail(row, folder, values=None):
    """⭐ 회신 DO P0 — run_kind 와 **같은 분류** + 그 분류를 정한 근거. 반환 (kind, detail).
      detail["source"]: ledger (장부 verdict · closes_system · melt_check) · folder_verdict (판정 기록) · folder_melt_window (보존 폴더의
      녹음 판정을 지금 계산) · unreadable · default · exception
      detail["melt"]: source 가 folder_melt_window 일 때 그 판정 (MELT_OBSERVED_KEYS) — 러너가 거부하기 **전에** 장부에 적는다
      (복구 · 확인 경로가 본 과학적 결과를 버리지 않게 · 실시간 감시 경로와 같은 보존)."""
    try:
        return _run_kind(row, folder, values)
    except Exception as e:
        return "unreadable", {"source": "exception", "error": f"{type(e).__name__}: {str(e)[:80]}"}


def provenance_current_problems(pv, folder, values):
    """⭐ 회신 DQ P1-1 — 판정 기록의 지문이 **지금** 파일 (BOUND_FILES) · 카드 값 · 도구 · G4 밴드 카드와 같은가 (묶음 판정 · _run_kind 가 같이
    쓴다). 문제 목록 (빈 목록 = 같다). 실행 환경 (runtime) 은 보지 않는다 — 다른 기계에서 요약해도 판정은 그대로 묶여 있다 (자동 대체만
    같은 환경을 요구한다 · same_judge_inputs)."""
    pv = pv if isinstance(pv, dict) else {}
    bad = []
    if pv.get("files_sha256") != run_provenance(folder):
        bad.append("원자료 지문이 지금 파일과 다르다 (판정 뒤 파일이 바뀌었거나 판정만 복사됐다 · md_init_raw.xyz · 실행 전 기록까지)")
    cur_vals, cur_drv = values_sha16(values), driver_sha16()
    if pv.get("card_values_sha16") != cur_vals:
        bad.append(f"카드 값 지문 {pv.get('card_values_sha16')} ≠ 지금 {cur_vals}")
    if pv.get("driver_sha16") != cur_drv:
        bad.append(f"도구 지문 {pv.get('driver_sha16')} ≠ 지금 {cur_drv}")
    if pv.get("band_sha16") != BAND_NOT_READ:                # ⭐ DR 전 리뷰 P3-B — 판정이 밴드 카드를 읽었을 때만 지금 카드와 대조한다
        cur_band = band_card_sha16()
        if cur_band is None or pv.get("band_sha16") != cur_band:
            bad.append(f"G4 밴드 카드 지문 {pv.get('band_sha16')} ≠ 지금 {cur_band}")
    fo_ = pathlib.Path(folder)
    if pv.get("folder") != [fo_.parent.name, fo_.name]:      # ⭐ DR 전 리뷰 P3-A — 판정을 낸 폴더 이름 (식별 입력) 이 지금과 다르다 (옮김 · 보존 폴더로 이름 바꿈)
        bad.append(f"판정을 낸 폴더 {pv.get('folder')} ≠ 지금 {[fo_.parent.name, fo_.name]} (폴더 이름도 판정 입력이다)")
    return bad


def _run_kind(row, folder, values):
    if not isinstance(row, dict):
        return "unreadable", {"source": "unreadable"}
    v, mc, cs = row.get("verdict"), row.get("melt_check"), row.get("closes_system")
    if v not in (None, "pass", "fail", "invalid", "incomplete"):
        return "unreadable", {"source": "unreadable"}
    if mc is not None and not (isinstance(mc, dict) and mc.get("verdict") in ("fail", "invalid")):
        return "unreadable", {"source": "unreadable"}
    if cs is not None and not isinstance(cs, bool):
        return "unreadable", {"source": "unreadable"}
    if row.get("melt_check_history") is not None and not isinstance(row.get("melt_check_history"), list):   # ⭐ DP 전 리뷰 F4
        return "unreadable", {"source": "unreadable"}
    if v in ("pass", "fail") or cs is True or (mc or {}).get("verdict") == "fail":
        return "scientific", {"source": "ledger"}
    recs, prob = _verdict_records(folder) if folder else ([], None)
    if prob:
        return "unreadable", {"source": "unreadable"}
    sts = [r_.get("status") if isinstance(r_, dict) else "?" for _, r_, _ in recs]
    sci = [r_ for _, r_, _ in recs if isinstance(r_, dict) and r_.get("status") in ("pass", "fail")]
    if sci and values is not None:                           # ⭐ DR 전 4 · 5차 리뷰 P2 — 과학적 판정 기록은 **지금 판정 규칙** (판정이 읽는 카드 값 · 도구) 으로 난 것만 쓴다
        cv_, jv_, cd_ = values_sha16(values), judge_values_sha16(values), driver_sha16()
        def _now_rules(r_):                                  # 판정 규칙 지문 (상한 · 재시도 칸 제외) · 도구 — 옛 꼴 기록은 카드 값 전체가 같으면
            pv_r = r_.get("provenance")
            if not (isinstance(pv_r, dict) and pv_r.get("driver_sha16") == cd_):
                return False
            return pv_r.get("judge_values_sha16") == jv_ if "judge_values_sha16" in pv_r else pv_r.get("card_values_sha16") == cv_
        sci_now = [r_ for r_ in sci if _now_rules(r_)]
        if not sci_now:                                      # 다른 규칙 (손 판정의 다른 카드 · 다른 checkout · 옛 도구) 의 결과 · 닫힘은 장부로 옮기지 않는다 —
            return "unreadable", {"source": "unreadable",      # ⭐ DR 전 7차 리뷰 P0: 과학적 판정 기록이 (어떤 규칙이든) 있는 폴더에서는 재시도할 수 있는 종류를
                                  "why": "과학적 판정 기록이 모두 다른 판정 규칙 (카드 판정 값 · 도구 · 또는 지문 없음) 으로 났다 — 지금 카드 · "   # 끌어내지 않는다
                                         "도구로 그 폴더를 --stage1_verdict 로 다시 판정해 과학적 판정 (pass · fail) 이 나오면 그것으로 읽는다 · 끊긴 런 "
                                         "(다시 판정해도 incomplete) 은 사람이 본다"}
        sci = sci_now                                        # 지금 규칙의 과학적 기록이 있으면 다른 규칙의 기록은 무시한다 (그 둘이 다르면 장부에 적을 때 폴더 기록 규칙이 충돌로 막는다)
    if sci:                                                  # ⭐ DP 전 리뷰 F1 · F2 — 판정 기록으로 본 과학적 결과도 러너가 거부 전에 장부에 적는다
        st_sci = "fail" if any(r_.get("status") == "fail" for r_ in sci) else "pass"
        cur_ = next((r_ for w_, r_, _ in recs if w_ == "현재 판정"), None)       # ⭐ DQ 전 2차 리뷰 N3 — 지금 판정이 그 상태면 그 지문 (아니면 없음 = 대체 못 함)
        ok_cur = isinstance(cur_, dict) and cur_.get("status") == st_sci
        pv_cur = cur_.get("provenance") if ok_cur else None
        if not (isinstance(pv_cur, dict) and values is not None                  # ⭐ 3차 P3 · 회신 DQ P1-1 — 기록된 지문이 지금 파일 · 카드 · 도구 ·
                and not provenance_current_problems(pv_cur, folder, values)):    # G4 밴드 카드와 같을 때만
            pv_cur = None
        return "scientific", {"source": "folder_verdict", "status": st_sci,
                              "closes_system": any(r_.get("closes_system") is True for r_ in sci),
                              "provenance": pv_cur, "prior": folder_verdict_chain(folder)}
    if any(x is None for x in sts):                          # ⭐ DP 전 리뷰 F1 — 못 읽은 이전 판정 (raw_b64 자리 · 상태 없음) = 판독 불가 (흔적 없음이 아니다)
        return "unreadable", {"source": "unreadable"}
    if any(x not in LI2S2_STATUSES for x in sts):
        return "unreadable", {"source": "unreadable"}
    st_ = row.get("status_before_orphan") or row.get("status")
    if values is not None and folder and os.path.lexists(pathlib.Path(folder) / "traj.xyz"):
        mw = melt_window_check(folder, values=values, log=lambda *a: None)     # ⭐ DO 전 리뷰 S1d · t12 — 녹음 결과가 이미 정해졌나
        if mw.get("verdict") == "fail":
            return "scientific", {"source": "folder_melt_window", "melt": {k: mw.get(k) for k in MELT_OBSERVED_KEYS}}
        if mw.get("verdict") == "invalid" and st_ in RUN_STATUSES_ENDED:   # ⭐ DP 전 리뷰 F3 — 끊긴 런의 녹음 invalid 는 끊긴 런 (한도를 우회하지 않게)
            return "invalid", {"source": "folder_melt_window"}
    if (mc or {}).get("verdict") == "invalid":
        return "invalid", {"source": "ledger"}
    if (v == "invalid" or "invalid" in sts) and st_ in RUN_STATUSES_ENDED:
        return "invalid", {"source": "ledger" if v == "invalid" else "folder_verdict"}
    return "interrupted", {"source": "default"}


def declaration_problems(decl, kind, values, rejudge_needed=False, prev_status=None):
    """⭐ 회신 DJ Q1 · Q4 — 재시도 선언 (확인 STOP 에 붙인 것) 검사: 그 종류에 허용된 **결과와 무관한** 사유 (카드 retry_reasons) ·
    상한으로 멈춘 런 (장부 상태 'cap') 은 카드 cap_retry_reasons 만 · 그 사유는 상한 런에만 · 사건 · 근거 · 선언자 · 선언 시각 ·
    (MD 까지 · 끝까지 돈 invalid 런이면) 있는 파일을 고쳐 다시 판정할 수 없다는 이유. 문제 목록 (빈 목록 = 통과).
    ⛔ 못 하는 것: 사람이 적은 사건이 참인지 · 결과를 보고 멈춘 것이 아닌지는 모른다 — 기록 (사건 · 근거 · 선언자) 을 남겨 감사할 수 있게 할 뿐."""
    if not isinstance(decl, dict):
        return ["재시도 선언이 없다 (사유 · 사건 · 근거 · 선언자 — 결과와 무관한 설비 · 운영 사건만 · Ctrl-C · abnormal · resume 는 사유가 아니다)"]
    why = []
    allowed = list(((values.get("retry_reasons") or {}).get(kind)) or [])
    cap_r = list(values.get("cap_retry_reasons") or [])
    reason = decl.get("reason")
    if reason not in allowed:
        why.append(f"사유 {reason!r} 는 {kind} 재시도에 허용된 사유 {allowed} 가 아니다")
    elif prev_status == "cap" and reason not in cap_r:
        why.append(f"상한으로 멈춘 런의 재시도 사유는 {cap_r} 뿐이다 ({reason!r} 아님 — 정전 사유로 상한을 늘리지 않는다)")
    elif reason in cap_r and prev_status != "cap":
        why.append(f"사유 {reason!r} 는 상한으로 멈춘 런 (장부 상태 cap) 에만 — 앞 런 상태 {prev_status!r}")
    for k in ("event", "evidence", "declared_by", "declared_at"):
        if not (isinstance(decl.get(k), str) and decl[k].strip()):
            why.append(f"선언 {k} 없음")
    if rejudge_needed and not (isinstance(decl.get("rejudge_impossible_reason"), str) and decl["rejudge_impossible_reason"].strip()):
        why.append("MD 까지 (또는 끝까지) 돈 invalid 런 — 있는 파일을 고쳐 다시 판정할 수 없다는 이유 (rejudge_impossible_reason) 가 없다")
    return why


def _no_dup_pairs(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise ValueError(f"같은 열쇠 {k!r} 가 둘")
        d[k] = v
    return d


def loads_strict(text):
    """JSON — 같은 열쇠가 둘이면 ValueError (뒤 값이 조용히 이기지 않게 · DO 전 리뷰)."""
    return json.loads(text, object_pairs_hook=_no_dup_pairs)


RECORD_TMP_NAMES = (LEDGER_NAME + ".tmp", "STOP.json.tmp")   # ⭐ 회신 DP P1-2 — 러너의 원자 쓰기가 끊기면 남는 임시 파일 (그 안이 더 새 기록일 수 있다)


def ledger_shape_problems(led):
    """⭐ 회신 DP P1-2 — 장부 꼴 검사 한 곳 (러너 · 소비자가 같이 쓴다): 객체 · runs 와 stop_history 가 **있고** 둘 다 객체 목록.
    없는 열쇠를 [] 로 채워 읽지 않는다 (러너는 거부하는데 소비자는 통과시키던 갈래 — stop_history 누락)."""
    if not isinstance(led, dict):
        return ["장부가 객체가 아니다"]
    out = []
    for k in ("runs", "stop_history"):
        if k not in led:
            out.append(f"장부에 {k} 가 없다")
        elif not isinstance(led[k], list):
            out.append(f"장부 {k} 가 목록이 아니다")
        elif not all(isinstance(x, dict) for x in led[k]):
            out.append(f"장부 {k} 원소가 객체가 아니다")
        elif k == "stop_history":                            # ⭐ 회신 DQ P2-1 — 확인 기록도 같은 STOP 꼴 검사 (모르는 코드 · 닫는 코드 · terminal 모순)
            for i_, h_ in enumerate(led[k]):
                sh_ = stop_shape_problem(h_, acked=True)
                if sh_:
                    out.append(f"장부 stop_history {i_} 번째 확인 기록 — {sh_}")
                    break
    return out


LEDGER_VERDICTS = (None, "pass", "fail", "invalid", "incomplete")   # 장부 행 verdict 의 허용 값 (러너 persist · _run_kind · _ledger_check 가 같이 쓴다)
STOP_TERMINAL_CODES = ("melt", "track")                  # ⭐ DQ 전 리뷰 P2-D — 닫는 STOP (러너 TERMINAL_STOPS 와 같아야 한다 · 러너 selftest 가 대조)
#: ⭐ 회신 DQ P2-1 — 러너가 STOP.json 에 쓰는 코드 전부 (러너 RC 의 pass · refused 를 뺀 것과 같아야 한다 · 러너 selftest 가 대조)
STOP_CODES = ("abnormal", "cap", "interrupted", "invalid", "melt", "pending", "resume", "track")


def stop_shape_problem(d_, acked=False):
    """⭐ 회신 DQ P2-1 — STOP 기록 하나의 꼴 · 일관성 (러너의 확인 · 소비자 stop_record · 장부 stop_history 가 **같은 함수** 를 쓴다). 문제 | None.
    stop_id · code 가 글자 · code 가 STOP_CODES 안 · terminal 이 참거짓이고 code 와 맞는다 (닫는 코드만 true — 'interrupted' + true 같은 모순된
    기록 · 모르는 코드는 받지 않는다: 요약은 invalid · 러너는 확인으로 지우지 않는다). acked (장부 stop_history 원소) 면 닫는 코드가 있으면 문제
    (닫는 STOP 은 확인으로 넘길 수 없다) · terminal 은 없어도 된다 (확인 기록의 옛 꼴)."""
    if not isinstance(d_, dict):
        return "객체가 아니다"
    if not (isinstance(d_.get("stop_id"), str) and d_["stop_id"].strip() and isinstance(d_.get("code"), str) and d_["code"].strip()):
        return "stop_id · code 가 글자가 아니다"
    code_ = d_["code"]
    if code_ not in STOP_CODES:
        return f"모르는 코드 {code_!r} (러너가 쓰는 코드 {list(STOP_CODES)})"
    term_ = d_.get("terminal")
    if acked:
        if code_ in STOP_TERMINAL_CODES:
            return f"닫는 코드 {code_!r} 가 확인 기록에 있다 (닫는 STOP 은 확인으로 넘길 수 없다)"
        if "terminal" in d_ and term_ is not False:
            return f"확인 기록의 terminal {term_!r} — 확인할 수 있는 STOP 은 terminal false 뿐이다"
        return None
    if type(term_) is not bool:
        return f"terminal {term_!r} 이 참거짓이 아니다"
    if term_ != (code_ in STOP_TERMINAL_CODES):
        return (f"terminal {term_} 이 코드 {code_!r} 와 안 맞는다 (닫는 코드 {list(STOP_TERMINAL_CODES)} 만 true) — 모순된 기록 "
                "(닫힘인지 확인할 멈춤인지 정할 수 없다)")
    return None


JUDGE_INPUT_KEYS = ("driver_sha16", "band_sha16", "runtime", "folder")   # files_sha256 · 판정 규칙 밖의 판정 입력 칸 (⭐ 회신 DQ P1-1 · DR 전 리뷰 P3-A)


def same_judge_inputs(a, b):
    """⭐ DQ 전 2차 리뷰 N3 · ⭐ 회신 DQ P1-1 — 두 판정 (a = 앞 · b = 새) 이 판정이 **읽은 입력 전부** 가 같은 상태에서 났는가:
    files_sha256 (BOUND_FILES 전부 — 원자료 다섯 · md_init_raw.xyz · stage1_attempt.json) · 판정 규칙 (judge_values_sha16 — 둘 다 있으면 · 아니면 카드 값 전체) ·
    도구 · G4 밴드 카드 · 실행 환경 · 폴더 이름이
    **다 있고** 같을 때만 True. 기록이 없거나 하나라도 다르면 False (확인할 수 없다 = 같다고 보지 않는다).
    파생 파일 (JUDGE_DERIVED_FILES) 하나만 예외 — 앞 판정 뒤에 없었고 (None) 지금 있으면 같다고 본다: 앞 판정은 그 파일을 읽지 않았고,
    새 판정이 과학적 (pass · fail — 이 함수를 부르는 supersede_block 은 그때만 불린다) 이면 그 seed_gate 가 파일을 묶인 traj 원시와 대조해 맞다고 봤거나
    (안 맞으면 입력 불일치로 invalid) 아예 읽지 않았다 (final.xyz 없음 — 그 판정의 입력이 아니다). 누가 만들었는지 (이 판정 · 중간 판정 · 사람의
    --seed_gate) 는 보지 않는다 (⭐ DR 전 리뷰 P2-A — '이 판정이 만들었을 때만' 은 중간 판정 한 번 · 재판정 뒤 Ctrl-C 로 일시 오류 회복을 영구 보류로
    굳혔다). 앞 판정 뒤에 **있던** 파일이 바뀌었거나 사라졌으면 다르다 (회신 DQ P1-1 재현: 다른 md_init_raw.xyz 를 옮기고 다시 만든 것).
    ⭐ 회신 DR P1-2 — 예외는 **진짜 부재 (None) → 정상 파일 (64 자리 16진수)** 에만: 그 자리에 디렉터리 · 링크 · 특수 파일이 있었다가 (path_state)
    치우고 다시 만든 것은 입력 상태를 복구한 것이라 다르다 (사람이 본다)."""
    if not (isinstance(a, dict) and isinstance(b, dict)):
        return False
    fa, fb = a.get("files_sha256"), b.get("files_sha256")
    if not (isinstance(fa, dict) and isinstance(fb, dict) and set(fa) == set(fb) and set(JUDGE_FILES) <= set(fa)):
        return False
    for k in JUDGE_INPUT_KEYS:
        if a.get(k) is None or b.get(k) is None or a.get(k) != b.get(k):
            return False
    if a.get("judge_values_sha16") is not None and b.get("judge_values_sha16") is not None:   # ⭐ DR 전 6차 리뷰 P2 — 판정 규칙 지문 (상한 · 재시도 칸을 올려도
        if a["judge_values_sha16"] != b["judge_values_sha16"]:                                # 판정 규칙은 그대로 — 그 사이 문서대로 상한을 올린 회복을 막지 않게)
            return False
    elif a.get("card_values_sha16") is None or a.get("card_values_sha16") != b.get("card_values_sha16"):   # 옛 기록 — 카드 값 전체
        return False
    for f in fa:
        if fa[f] == fb[f]:
            continue
        if f in JUDGE_DERIVED_FILES and fa[f] is None and isinstance(fb[f], str) and _SHA256_RE.fullmatch(fb[f]):
            continue                                         # ⭐ 회신 DR P1-2 — 진짜 부재 → 정상 파일만 (디렉터리 · 링크 · 특수 파일을 치운 복구는 다르다)
        return False
    return True


def supersede_block(prior, new):
    """⭐ 회신 DQ P1-1 · Q5 — 앞 비과학적 판정 (invalid · incomplete) 을 새 과학적 판정이 **자동으로** 대체해도 되는가. 되면 None, 아니면 이유.
    둘 다 있어야 한다: ① 판정이 읽은 입력 전부가 같다 (same_judge_inputs) ② 앞 판정이 **판정 도중 예외** 로 못 끝났다 (judge_nature.errors 가 있다)
    그리고 끝까지 보고 찾은 입력 불일치가 없다 (judge_nature.input_mismatch 가 빈 목록). 성격 기록이 없는 앞 판정은 대체하지 않는다 (사람이 본다).
    ⛔ 못 하는 것: 예외의 원인 (일시 I/O 인지 · 같은 바이트에서 다시 나는 파싱 오류인지) 은 가르지 않는다 — 같은 입력에서 결과가 달라졌다는 것
    자체가 그 예외가 비결정적이었다는 뜻이고, 입력이 하나라도 다르면 ① 이 막는다."""
    if not (isinstance(prior, dict) and isinstance(new, dict)):
        return "앞 판정 또는 지금 판정의 지문이 없다 — 같은 입력이라고 확인할 수 없다"
    if not same_judge_inputs(prior, new):
        return ("판정이 읽은 입력 (원자료 · md_init_raw.xyz · 실행 전 기록 · 폴더 이름 · 카드 값 · 도구 · G4 밴드 카드 · 실행 환경) 이 그때와 같다고 "
                "확인할 수 없다 (지문이 다르거나 없다 — 입력이 바뀌었거나 복구됐을 수 있다)")
    jn = prior.get("judge_nature")
    if not (isinstance(jn, dict) and isinstance(jn.get("errors"), list) and isinstance(jn.get("input_mismatch"), list)
            and all(isinstance(x, str) for x in jn["errors"] + jn["input_mismatch"])):
        return "앞 판정에 판정 성격 기록 (judge_nature) 이 없다 — 판정 도중 오류였는지 모른다"
    if jn["input_mismatch"]:
        return f"앞 판정은 입력 불일치를 찾은 판정이다 ({'; '.join(jn['input_mismatch'])[:120]}) — 판정 도중 오류가 아니다 (복구는 사람이 본다)"
    if not jn["errors"]:
        return "앞 판정은 판정 도중 예외 없이 끝난 판정이다 — 같은 입력에서 결과가 달라질 이유가 없다 (사람이 본다)"
    return None


def pre_anchor_exempt(rec):
    """⭐ 회신 DR P1-1 — 장부 판정 자신의 기록 **앞** 의 비과학적 판정 기록 중 대체 규칙을 받지 않는 것: 판정이 스스로 '덜 끝남' 으로 분류한
    incomplete (실제 진행 중 — 실행 중 사람이 들여다본 판정) 이고 입력 불일치를 찾지 않은 것뿐 (판정 성격 기록이 없는 옛 꼴 incomplete 도).
    완료된 판정 (invalid — 입력 불일치 · 결정적 실패 · 일시 오류) 은 앞에 있어도 뒤 기록과 같은 대체 규칙을 받는다 — 입력 불일치는 앞뒤와 무관하게
    보류 근거로 남는다."""
    if not (isinstance(rec, dict) and rec.get("status") == "incomplete"):
        return False
    pv_ = rec.get("provenance")
    jn_ = pv_.get("judge_nature") if isinstance(pv_, dict) else None
    return jn_ is None or (isinstance(jn_, dict) and jn_.get("input_mismatch") == [])


def ledger_verdict_conflict(row, folder_status, recorded=True, folder_provenance=None, folder_prior=None):
    """⭐ DQ 전 리뷰 P1-A · 2차 N3 — 같은 실행의 장부 행과 폴더 판정이 어긋나는가 (러너 ①-4 · persist · 소비자 _ledger_check 가 **같은 함수** 를 쓴다).
    반환: 문제 글 | None. 규칙:
      · 장부 verdict 가 허용 값 밖이면 문제.
      · 폴더 판정이 pass · fail 일 때 — 장부가 pass · fail 인데 다르면 충돌 (과학적 결과가 바뀌었다) · 장부가 invalid · incomplete 면 **supersede_block 이
        None 일 때만** 충돌 아님 — 장부에 적힌 그 판정의 지문 (verdict_provenance) 과 지금 폴더 판정의 지문이 판정이 읽은 입력 전부 (원자료 ·
        md_init_raw.xyz · 실행 전 기록 · 카드 값 · 도구 · G4 밴드 카드 · 실행 환경) 에서 같고, 앞 판정이 판정 도중 예외로 못 끝났고 입력 불일치를
        찾지 않았을 때 (⭐ 회신 DQ P1-1 · Q5). 아니면 충돌 (원자료 복구 · 추가 · 수동 변경일 수 있다 — 사람이 본다 · 회신 DP Q2).
      · 장부 녹음 fail 인데 폴더 판정 pass 면 충돌.
      · ⭐ 3차 · 4차 P1 — 장부 판정이 **없으면** (판정을 쓴 뒤 장부에 적기 전에 SIGKILL · 정전 · 러너가 죽은 뒤 끝난 담금질을 사람이 판정 ·
        상한 기록용 판정) — ⭐ DR 전 2차 리뷰 P1: 장부 판정이 **비과학적 (invalid · incomplete) 일 때도** (러너의 재판정이 입력 불일치를 봤는데 장부엔
        안 적힌 채 사람이 파일을 고친 경우 · 재판정 fail 을 쓰고 장부에 적기 전에 끊긴 경우) — 그 폴더의 판정 기록 **전체** (folder_prior =
        folder_verdict_chain — 판정을 쓴 순서) 를 기준으로 (⭐ DR 전 3 · 4 · 5차 리뷰 — 장부 판정이 비과학적이면 장부 판정 자신의 기록 (같은 상태 · 지문 · 첫 것) 을
        찾아 그 **앞** 의 진행 중 incomplete (실행 중 들여다본 판정 · 입력 불일치 없음 — pre_anchor_exempt) 는 막지 않고 그 밖의 비과학적 기록 (그 **뒤** 의
        기록 · ⭐ 회신 DR P1-1 그 앞이어도 완료된 invalid · 입력 불일치) 은 하나하나 대체 규칙을 받는다 —
        그 뒤 재판정이 본 입력 변경 · 불일치를 되돌린 복구는 보류 · 장부 판정의 기록을 못 찾으면 전부 대체 규칙):
        못 읽는 판정 (상태 없음) 이 있으면 충돌 · pass · fail 판정이 하나라도 지금과 다르면 충돌 · invalid · incomplete 판정이 하나라도 지금 판정으로
        자동 대체할 수 없으면 (supersede_block — 위와 같은 규칙) 충돌. 한 단계 이력만 보면 다시 판정 한 번 (사람의 --stage1_verdict · 끊긴 재시작) 이 앞
        판정을 밀어내 증거가 안 보인다 (4차 리뷰 재현).
      · recorded 면 장부에 적힌 충돌 관측 (verdict_observed_conflict) 도 충돌.
    ⛔ 못 하는 것 (⭐ 회신 DQ Q5 · 회신 DR P2-1 문구): 장부 판정이 pass · fail 로 확정돼 있으면 그 장부 판정과 지금 폴더 판정을 우선한다 · 장부
       판정이 없거나 invalid · incomplete 면 위 폴더 판정 기록 규칙을 적용한다 — 모든 과거 수동 판정 사이의 충돌을 영구히 보류한다는 보장은 아니다
       (시험된 정책). 충돌을 푸는 명령은 없다 (Q7 — 실제 사건이 생기면 절차를 정한다)."""
    v_ = row.get("verdict")
    if v_ not in LEDGER_VERDICTS:
        return f"장부 판정 {v_!r} 를 모른다 (허용 {list(LEDGER_VERDICTS)})"
    if folder_status in ("pass", "fail"):
        if v_ in ("pass", "fail") and v_ != folder_status:
            return f"장부 판정 {v_} ≠ 폴더 판정 {folder_status}"
        if v_ in ("invalid", "incomplete"):
            sb_ = supersede_block(row.get("verdict_provenance"), folder_provenance)   # ⭐ 회신 DQ P1-1 — 입력 전부 같음 + 앞 판정이 판정 도중 예외
            if sb_ is not None:
                return f"장부 판정 {v_} → 폴더 판정 {folder_status} — 자동 대체 조건이 아니다 ({sb_})"
        mc_ = row.get("melt_check")
        if folder_status == "pass" and isinstance(mc_, dict) and mc_.get("verdict") == "fail":
            return "장부 녹음 fail ↔ 폴더 판정 pass"
        if (v_ is None or v_ in ("invalid", "incomplete")) and isinstance(folder_prior, list):   # ⭐ 3차 · 4차 P1 · DR 전 2차 리뷰 P1 — 장부가 비었거나
                                                                                                    # 비과학적이면 폴더 판정 기록 전체를 기준으로
            vp_ = row.get("verdict_provenance")             # ⭐ DR 전 4 · 5차 리뷰 — 장부 판정 자신의 기록 (같은 상태 · 같은 지문 · **첫** 것 — 장부의 쓰기가 가장 이르다 ·
                                                            # 뒤에 같은 바이트의 판정이 또 생겨도 기준이 밀리지 않게) 이 어디인가 (순서 기록)
            k_ = (min((i_ for i_, r_ in enumerate(folder_prior) if isinstance(r_, dict) and r_.get("status") == v_ and r_.get("provenance") == vp_),
                      default=None) if (v_ is not None and isinstance(vp_, dict)) else None)
            for i_, rec_ in enumerate(folder_prior):
                st_ = rec_.get("status") if isinstance(rec_, dict) else None
                if st_ is None or (st_ not in LI2S2_STATUSES):
                    return f"장부 판정 {v_!r} · 폴더 판정 기록에 못 읽는 판정이 있다 — 비교할 수 없다"
                if st_ in ("pass", "fail") and st_ != folder_status:
                    return f"장부 판정 {v_!r} · 폴더 판정 기록의 {st_} ≠ 지금 {folder_status} (끊긴 뒤 원자료 · 도구가 바뀌었을 수 있다)"
                if st_ in ("invalid", "incomplete") and (k_ is None or i_ > k_ or (i_ < k_ and not pre_anchor_exempt(rec_))):
                    sb_ = supersede_block(rec_.get("provenance"), folder_provenance)   # ⭐ DR 전 4차 리뷰 P1 — 장부가 비었거나 · 장부 판정의 기록을 못 찾았거나 ·
                    if sb_ is not None:                              # 그 **뒤** 의 기록이면 · ⭐ 회신 DR P1-1 그 **앞** 이어도 진행 중 incomplete 가 아니면
                        return (f"장부 판정 {v_!r} · 폴더 판정 기록의 {st_} 판정"     # (완료된 판정 · 입력 불일치) 하나하나 같은 대체 규칙 (같은 입력 + 판정 도중 예외)
                                + (" (장부 판정의 기록 앞 · 진행 중 incomplete 아님)" if (k_ is not None and i_ < k_) else "")
                                + f" 을 지금 {folder_status} 판정이 대체할 수 없다 ({sb_})")
                # 장부 판정 자신 · 그 **앞** 의 진행 중 incomplete (실행 중 들여다본 판정 · 입력 불일치 없음) 는 막지 않는다 — 입력이 장부 판정 때와 같은지는
                # 위 장부 규칙이 본다 (⭐ 회신 DR P1-1 — 앞에 있어도 완료된 입력 불일치 판정은 보류 근거로 남는다)
    if recorded and row.get("verdict_observed_conflict"):
        return "장부에 같은 실행의 다른 판정 관측이 있다 (verdict_observed_conflict)"
    return None


def unresolved_first_write(folder):
    """⭐ 회신 DQ P1-2 — 정본 판정 (stage1_verdict.json) 이 **없는데** 판정 기록 (판정 이력 · 판정 임시 파일) 이 남은 폴더 = 첫 판정 쓰기가
    끊겼거나 정본이 지워졌다 → 이유 (러너는 아무것도 띄우지 않고 · 묶음 판정은 invalid · 자동 승격 · 다시 판정 안 함 · 사람이 본다).
    정본 자리에 파일이 아닌 것 (디렉터리 · 깨진 링크) 이 있어도 같다. 아무 판정도 시도하지 않은 폴더 (기록 없음 — 정상 미완료) 와 정본이 있는 폴더는
    None (정본이 있는 폴더의 이력 · 임시 파일은 _verdict_records 가 본다). 판정 쓰기 순서는 이력 줄 → 임시 파일 → 교체라서 어느 자리에서 끊겨도
    흔적이 하나는 남는다 (이력 파일을 열기 전 끊김은 흔적이 없다 = 판정을 시도하지 않은 것과 같다)."""
    f = pathlib.Path(folder)
    vf = f / "stage1_verdict.json"
    if vf.is_file():
        return None
    if os.path.lexists(vf):
        return "정본 판정 자리 (stage1_verdict.json) 에 파일이 아닌 것이 있다 — 판정을 읽을 수 없다 (사람이 본다)"
    left = [n for n in (vf.name + ".tmp", VERDICT_HISTORY) if os.path.lexists(f / n)]
    if not left:
        return None
    return (f"정본 판정 (stage1_verdict.json) 없이 판정 기록 {left} 이 남았다 — 첫 판정 쓰기가 끊겼거나 정본이 지워졌다 "
            "(그 안에 과학적 결과가 있을 수 있다 · 자동 승격 · 다시 판정하지 않는다 · 사람이 본다)")


def folder_record_problem(folder):
    """⭐ DR 전 2차 리뷰 P2-B — 한 폴더의 판정 기록이 미해결 · 판독 불가인가 (이유 | None): 정본 없는 판정 기록 (unresolved_first_write) ·
    _verdict_records 의 문제 (판정 임시 파일 · 못 읽는 판정 · 이력 줄) · 상태 없는 (원문만 남은) 판정 · 모르는 상태 ('PASS' 등) — _run_kind 가
    '판독 불가' 로 보는 판정 기록과 같은 기준이다. 기록이 없는 폴더는 None."""
    why_ = unresolved_first_write(folder)
    if why_:
        return why_
    recs_, prob_ = _verdict_records(folder)
    if prob_:
        return prob_
    sts_ = [r_.get("status") if isinstance(r_, dict) else "?" for _, r_, _ in recs_]
    if any(x_ is None or x_ not in LI2S2_STATUSES for x_ in sts_):
        return f"판정 기록에 못 읽는 · 모르는 상태가 있다 ({sts_}) — 판정 없음으로 읽지 않는다"
    return None


def preserved_unresolved(out_root, seeds=None):
    """⭐ DR 전 리뷰 P2-B · 2차 P2-B — 현재 시드 폴더 (<계>/seed<카드 시드>) 가 **아닌** 모든 폴더 (사람이 옆으로 옮긴 보존 폴더 — 이름 꼴과 무관:
    seed14.moved · seed14_moved · old14 …) 의 미해결 · 판독 불가 판정 기록 (folder_record_problem). seeds 가 없으면 seed<N> 꼴 이름을 모두 현재
    폴더로 본다. 목록 [(계, 시드 | None, 폴더 이름, 이유)]. 러너는 시작에서 · 요약은 장부 검사에서 하나라도 있으면 막는다 (그 폴더에 닿기 전에 다른
    시드를 돌리지 않게 · 통과로 올리지 않게)."""
    out, cur_ = [], ({f"seed{x_}" for x_ in seeds} if seeds is not None else None)
    for s_ in ("A", "B"):
        d_ = pathlib.Path(out_root) / s_
        if not d_.is_dir():
            continue
        for p_ in sorted(d_.iterdir()):
            if not p_.is_dir():
                continue
            if (p_.name in cur_) if cur_ is not None else re.fullmatch(r"seed\d+", p_.name):
                continue
            why_ = folder_record_problem(p_)
            if why_:
                m_ = re.match(r"seed(\d+)", p_.name)            # ⭐ DR 전 3차 리뷰 P3 — 시드는 seed<N> 꼴 이름에서만 (backup_2026_11_05 를 시드 2026 으로 읽지 않는다)
                out.append((s_, int(m_.group(1)) if m_ else None, p_.name, why_))
    return out


def folder_verdict_chain(folder):
    """⭐ 4차 P1 · DR 전 4차 리뷰 P1 — 폴더 판정 기록 전체를 **판정을 쓴 순서대로** [{"status", "provenance"}] 로: 이력 줄마다 그때 쓴 새 판정
    (첫 판정 줄 · 바꿈 줄의 새 판정) · 이력 맨 앞 줄이 바꿈 줄이면 그 앞 판정을 맨 앞에 · 바꿈 줄의 앞 판정이 바로 앞 쓰기와 다르면 (판정 밖에서
    바뀐 판정) 그 자리에 · 지금 판정이 마지막 쓰기와 다르면 (이력 없이 쓴 판정) 끝에. 순서가 있어야 장부 판정 자신의 기록 앞 (앞선 상태) 과 뒤
    (그 뒤의 재판정 · 손 판정) 를 가를 수 있다 (ledger_verdict_conflict). 기록을 못 읽으면 (임시 파일 · 깨진 줄 · 꼴) [{"status": None}] — 비교할 수
    없다 (충돌로 읽힌다). 폴더가 없거나 판정 기록이 없으면 []."""
    if not folder or not os.path.isdir(folder):
        return []
    recs, prob = _verdict_records(folder)
    if prob:
        return [{"status": None, "why": prob}]
    sp_ = lambda r_: {"status": r_.get("status"), "provenance": r_.get("provenance")} if isinstance(r_, dict) else {"status": None}
    writes, cur = [], None
    for where_, r_, _ in recs:
        x_ = sp_(r_)
        if where_ == "현재 판정":
            cur = x_
        elif where_.endswith("의 이전 판정"):
            if not writes or writes[-1] != x_:               # 앞 줄의 새 판정과 같으면 겹침 (보통) · 다르면 판정 밖에서 바뀐 판정 — 남긴다
                writes.append(x_)
        else:
            writes.append(x_)                                # 첫 판정 줄 · 바꿈 줄의 새 판정 = 그때 쓴 판정
    if cur is not None and (not writes or writes[-1] != cur):
        writes.append(cur)                                   # 이력 없이 쓴 지금 판정 (옛 꼴 · 손 편집)
    return writes


def stop_record(out_root):
    """⭐ DQ 전 리뷰 P2-D — run_root 의 STOP.json (러너의 멈춤 기록) 을 소비자도 읽는다. 반환 (상태, 내용 | 이유):
    ("absent", None) · ("unreadable", 이유) · ("terminal", stop) · ("open", stop) — open = 확인 안 된 다른 멈춤 (러너는 invalid 코드를 기록 오류에도
    '과학적 결과가 있어 재시도 거부' 같은 운영 멈춤에도 쓴다 — 그래서 코드로 기록 오류를 가르지 않고, 통과로 올리지 않는 것 (pending) 만 한다)."""
    sp_ = pathlib.Path(out_root) / "STOP.json"
    if not os.path.lexists(sp_):
        return "absent", None
    try:
        d_ = loads_strict(sp_.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeDecodeError, RecursionError) as e:
        return "unreadable", f"{type(e).__name__}: {str(e)[:60]}"
    sh_ = stop_shape_problem(d_)                          # ⭐ 회신 DQ P2-1 — 모르는 코드 · terminal 모순은 판독 불가 (러너도 같은 함수로 확인을 거부)
    if sh_:
        return "unreadable", sh_
    if d_["code"] in STOP_TERMINAL_CODES:
        return "terminal", d_
    return "open", d_


def record_tmp_problems(out_root):
    """⭐ 회신 DP P1-2 — run_root 에 남은 장부 · STOP 임시 파일 = 미해결 기록 (러너는 시작을 거부한다 · 소비자도 통과시키지 않는다 · 자동 승격 안 함)."""
    return [f"{n} 이 남았다 — 앞 쓰기가 끊겼다 · 그 안이 더 새 기록일 수 있다 (사람이 내용과 계보를 보고 정리)"
            for n in RECORD_TMP_NAMES if os.path.lexists(pathlib.Path(out_root) / n)]


def ledger_check(out_root, verdicts, values):
    """장부 검사 — 판독 예외가 나도 죽지 않고 invalid 로 돌린다 (DO 전 리뷰 F6). 아래 _ledger_check 의 설명을 본다."""
    try:
        return _ledger_check(out_root, verdicts, values)
    except Exception as e:
        return {"total_h": float("nan"), "cap_h": float(values["stage1_cap_gpu_h"]), "invalid": [f"장부 판독 예외 ({type(e).__name__})"],
                "pending": [], "runs": 0, "attested": [], "closing": [], "source": str(pathlib.Path(out_root) / LEDGER_NAME)}


def _ledger_check(out_root, verdicts, values):
    """⭐ 회신 DH P0-1 · DI · DJ — 장부 = **실행 목록**. 장부가 없으면 None (확인 못 함 → 통과 안 됨).
    invalid: 장부 꼴 · run_id 꼴 · 중복 · 비용이 유한한 비음수가 아님 · 근거가 측정 · 보수 상한 · 증언 상한이 아님 · 증언 상한의 근거 필드
             (카드 attestation_required_fields) · 하한 (유한 · heartbeat 이상 · 증언 때 하한과 같음) · 폴더 ↔ 장부 양쪽 (보존 누락 포함) ·
             재시도 이력 (두 번째 실행부터: retry_of = 바로 앞 실행 · retry_kind = 앞 실행 종류 · retry_stop_id = 그 앞 실행에 묶여 확인된 STOP ·
             그 STOP 의 선언 · stage1_attempt.json 의 재시도 필드 = 장부 · 과학적 판정 · 판독 불가 판정 · 끝까지 / MD 까지 돈 런 뒤 재시도 ·
             끊긴 런 재시도 수 (앞 실행 종류로 센다) > 카드 한도) · 판정 ↔ 장부.
    pending: 끝나지 않은 런 (heartbeat 는 하한일 뿐). total_h = 확정 비용 합 · cap_h = 카드 상한 (정전 손실로 늘리지 않는다 — 회신 DK · 카드 v3)."""
    p = pathlib.Path(out_root) / LEDGER_NAME
    if not p.is_file():
        return None
    invalid, pending, by_id, attested = [], [], {}, []
    try:
        led = loads_strict(p.read_text(encoding="utf-8"))
        shp_ = ledger_shape_problems(led)                    # ⭐ 회신 DP P1-2 — 러너와 같은 꼴 검사 (없는 열쇠를 채우지 않는다)
        if shp_:
            raise ValueError(" · ".join(shp_))
        runs, stop_hist = led["runs"], led["stop_history"]
    except (ValueError, UnicodeDecodeError, AttributeError, RecursionError) as e:
        return {"total_h": float("nan"), "cap_h": float(values["stage1_cap_gpu_h"]), "invalid": [f"장부를 못 읽었다 ({type(e).__name__}: {str(e)[:60]})"],
                "pending": [], "runs": 0, "attested": [], "closing": [], "source": str(p)}
    invalid.extend(record_tmp_problems(out_root))            # ⭐ 회신 DP P1-2 — 장부 · STOP 임시 파일 = 미해결 기록
    invalid.extend(f"보존 폴더 {s_}/{nm_} 의 미해결 판정 기록 — {why_}"                # ⭐ DR 전 리뷰 P2-B · 2차 (이름 꼴과 무관 · 판독 불가 기준)
                   for s_, _, nm_, why_ in preserved_unresolved(out_root, values.get("seeds")))
    if led.get("card_values_sha16") != values_sha16(values):  # ⭐ DQ 전 리뷰 P2-G — 장부를 쓴 러너의 카드 값 · 도구와 지금 판정에 쓰는 것이 같아야 한다
        invalid.append(f"장부의 카드 값 지문 {led.get('card_values_sha16')!r} ≠ 지금 {values_sha16(values)} — 다른 카드로 낸 묶음 판정은 받지 않는다")
    if led.get("driver_sha16") != driver_sha16():
        invalid.append(f"장부의 도구 지문 {led.get('driver_sha16')!r} ≠ 지금 {driver_sha16()} — 러너를 이 도구로 다시 시작해 재판정한 뒤 다시")
    st_k, st_v = stop_record(out_root)                       # ⭐ DQ 전 리뷰 P2-D — 러너가 멈춰 있으면 소비자도 통과로 올리지 않는다
    terminal_stop = None
    if st_k == "unreadable":
        invalid.append(f"STOP.json 을 못 읽는다 ({st_v}) — 러너도 시작하지 않는다 (사람이 본다)")
    elif st_k == "terminal":
        terminal_stop = st_v["code"]
    elif st_k == "open":
        pending.append(f"확인 안 된 멈춤 (STOP {st_v['code']} · {str(st_v.get('reason'))[:80]}) — 러너가 멈춰 있다 · 확인 (--ack_stop) 뒤 다시 판정")
    req_att = list(values.get("attestation_required_fields") or [])
    tot, closing = 0.0, []
    for r in runs:
        if not isinstance(r, dict):
            invalid.append("장부 runs 원소가 객체가 아니다"); continue
        key = f"{r.get('system')}{r.get('seed')}"
        rid = r.get("run_id")
        if not (isinstance(rid, str) and RUN_ID_RE.match(rid)):
            invalid.append(f"{key} 런의 run_id {rid!r} 꼴이 아니다 — 폴더 · 판정과 못 잇는다"); continue
        if rid in by_id:
            invalid.append(f"장부에 run_id {rid[:8]} 가 둘 ({key})")
        by_id[rid] = r
        if r.get("system") not in ("A", "B") or type(r.get("seed")) is not int:          # ⭐ DO 전 리뷰 — 계 · 시드 꼴 (12.0 · '12' 안 받음)
            invalid.append(f"{key} 런의 계 · 시드 꼴이 아니다 ({r.get('system')!r} · {r.get('seed')!r})"); continue
        cs, mc = r.get("closes_system"), r.get("melt_check")
        if cs is not None and not isinstance(cs, bool):
            invalid.append(f"{key} 런의 closes_system {cs!r} — 참거짓이 아니다"); continue
        if r.get("verdict") not in LEDGER_VERDICTS:          # ⭐ DQ 전 리뷰 P1-A — 러너 persist · _run_kind 와 같은 허용 값
            invalid.append(f"{key} 런의 verdict {r.get('verdict')!r} 를 모른다"); continue
        vc_ = r.get("verdict_observed_conflict")             # ⭐ DQ 전 리뷰 P2-B — 러너가 적은 충돌 관측 (같은 실행의 다른 판정)
        if vc_ is not None and not (isinstance(vc_, list) and all(isinstance(x_, dict) for x_ in vc_)):
            invalid.append(f"{key} 런의 verdict_observed_conflict {str(vc_)[:40]!r} — 목록이 아니다"); continue
        if vc_:
            invalid.append(f"{key} 런에 같은 실행의 다른 판정 관측이 있다 ({len(vc_)} 건 · 장부 판정 {r.get('verdict')!r}) — 사람이 본다")
        vp_, vs_ = r.get("verdict_provenance"), r.get("verdict_superseded")   # ⭐ DQ 전 2차 리뷰 N3 — 장부 판정의 지문 · 대체 기록 꼴
        if vp_ is not None and not isinstance(vp_, dict):
            invalid.append(f"{key} 런의 verdict_provenance {str(vp_)[:40]!r} — 객체가 아니다"); continue
        if vs_ is not None and not (isinstance(vs_, list) and all(isinstance(x_, dict) and x_.get("from") in ("invalid", "incomplete")
                                                                   and x_.get("to") in ("pass", "fail") for x_ in vs_)):
            invalid.append(f"{key} 런의 verdict_superseded {str(vs_)[:60]!r} — 비과학적 판정 → 과학적 판정의 목록이 아니다"); continue
        if mc is not None and not (isinstance(mc, dict) and mc.get("verdict") in ("fail", "invalid")):
            invalid.append(f"{key} 런의 melt_check {str(mc)[:40]!r} — 꼴이 아니다"); continue
        mh = r.get("melt_check_history")                    # ⭐ DP 전 리뷰 F4 — 앞 녹음 판정의 보관 목록
        if mh is not None and not (isinstance(mh, list) and all(isinstance(x_, dict) for x_ in mh)):
            invalid.append(f"{key} 런의 melt_check_history {str(mh)[:40]!r} — 목록이 아니다"); continue
        if cs is True and r["seed"] != values.get("first_seed"):   # ⭐ DQ 전 리뷰 P2-D — 카드: 첫 시드 녹음만 계를 닫는다 (러너 ①-3 과 같은 규칙)
            invalid.append(f"{key} 런에 closes_system 이 있다 — 첫 시드 ({values.get('first_seed')}) 가 아니다 · 기록 오류 (사람이 본다)")
        elif cs is True:                                  # ⭐ DO 전 리뷰 P0 — 첫 시드 녹음 fail 은 장부에도 남는다 (판정이 없어도 그 계를 닫는다)
            closing.append((r["system"], r["seed"], rid))
        if r.get("end") is None:
            pending.append(f"{key} 런이 끝나지 않았다 (상태 {r.get('status')} · 비용 미확정 — heartbeat {r.get('wall_h_so_far')} h 는 하한)")
            continue
        if not (isinstance(r.get("end"), str) and r["end"].strip()):
            invalid.append(f"{key} 런의 end {r.get('end')!r} — 끝 시각 글자가 아니다 (False · 0 · 빈 글자를 '끝남' 으로 세지 않는다)"); continue
        w = r.get("wall_h")
        if not (_fin(w) and float(w) >= 0.0):
            invalid.append(f"{key} 런 비용 {w!r} — 유한한 비음수가 아니다"); continue
        hb_, lo_ = r.get("wall_h_so_far"), r.get("wall_h_lower")
        if r.get("cost_basis") in ("measured", "upper_bound"):      # ⭐ DO 전 리뷰 P2-17 — 측정 · 보수 상한도 자기 하한과 대조 (증언 상한은 아래에서 따로)
            if any(x is not None and not (_fin(x) and float(x) >= 0) for x in (hb_, lo_)):
                invalid.append(f"{key} 런 heartbeat · 하한 ({hb_!r} · {lo_!r}) — 유한한 비음수가 아니다"); continue
            if any(x is not None and float(w) < float(x) - 1e-9 for x in (hb_, lo_)):
                invalid.append(f"{key} 런 비용 {w} h 가 자기 하한 (heartbeat {hb_} · 하한 {lo_}) 보다 작다"); continue
        if r.get("cost_basis") not in COST_BASES:
            invalid.append(f"{key} 런 비용 근거 {r.get('cost_basis')!r} — 측정 · 보수 상한 · 증언 상한이 아니면 확정 비용이 아니다"); continue
        if r.get("cost_basis") == "attested_upper_bound":       # 정전 복구 · 회신 DJ P0-3 · Q3 — 증언 상한
            at, lo, hb = r.get("attestation"), r.get("wall_h_lower"), r.get("wall_h_so_far")
            bad = []
            if r.get("status") != "orphaned":
                bad.append(f"증언 상한은 재부팅 고아 런 (orphaned) 에만 — 상태 {r.get('status')!r}")
            if not isinstance(at, dict):
                bad.append("근거 (attestation) 없음"); at = {}
            for f_ in req_att:
                x = at.get(f_)
                ok_ = (_fin(x) and float(x) >= 0) if f_ == "uncertainty_h" else (isinstance(x, str) and x.strip())
                if not ok_:
                    bad.append(f"근거 {f_} 없음")
            if not (_fin(lo) and _fin(hb) and float(lo) >= 0 and float(hb) >= 0 and float(lo) >= float(hb) - 1e-9):
                bad.append(f"하한이 미상 · 잘못 (하한 {lo!r} · heartbeat {hb!r}) — 하한 미상이면 비용도 미상")
            elif not (_same(at.get("lower_at_attest"), lo, rel=0.0, abs_=1e-9) and _same(at.get("heartbeat_at_attest"), hb, rel=0.0, abs_=1e-9)):
                bad.append(f"증언 때 하한 · heartbeat ({at.get('lower_at_attest')!r} · {at.get('heartbeat_at_attest')!r}) ≠ 장부 ({lo!r} · {hb!r})")
            elif float(w) < float(lo):
                bad.append(f"증언 상한 {w} h < 하한 {lo} h")
            if not float(w) > 0:                               # 회신 DK P1-2 — 증언 상한은 양수 (측정 비용 0 은 따로 허용)
                bad.append(f"증언 상한 {w} h 가 양수가 아니다")
            if bad:
                invalid.append(f"{key} 런 증언 상한 — " + " · ".join(bad)); continue
            attested.append(f"{key} {float(w):g} h ({str(at.get('event'))[:40]} · {at.get('confirmer')})")
        tot += float(w)
    inventory, inventory_bad = attempt_inventory(out_root)
    invalid.extend(inventory_bad)
    for rid, rec in inventory.items():
        r = by_id.get(rid)
        if r is None:
            invalid.append(f"보존 포함 실행 {rid} ({rec['path']}) 이 장부에 없다")
        elif (r.get("system"), r.get("seed")) != (rec["system"], rec["seed"]):
            invalid.append(f"실행 {rid} 의 산출물 · 장부 계/시드가 다름")
    for rid, r in by_id.items():                              # 회신 DJ P0-2 — 장부 → 보존 폴더 방향
        if rid not in inventory:
            invalid.append(f"장부의 {r.get('system')}{r.get('seed')} 런 ({rid[:8]}) 폴더가 run_root 의 계 폴더 안에 없다 (보존 누락 · 지우거나 밖으로 옮김)")
    hist = {}
    for h in stop_hist:                                       # ⭐ DP 전 리뷰 (둘째) — 같은 stop_id 둘을 뒤 것으로 덮지 않는다
        if not isinstance(h, dict):
            invalid.append("장부 stop_history 원소가 객체가 아니다"); continue
        if h.get("stop_id"):
            if h["stop_id"] in hist:
                invalid.append(f"장부 stop_history 에 stop_id {str(h['stop_id'])[:16]} 가 둘")
            hist[h["stop_id"]] = h
    seen = {}
    for r in runs:
        if isinstance(r, dict) and isinstance(r.get("run_id"), str):
            seen.setdefault((r.get("system"), r.get("seed")), []).append(r)
    max_int = int(values["stage1_max_interrupt_retries_per_seed"])      # 카드 검사가 0 이상 정수를 보장 — 없으면 여기서 멈춘다 (검사를 끄지 않는다)
    fields = ("retry_of", "retry_stop_id", "retry_kind")
    for k, rr_ in seen.items():
        tag = f"{k[0]}{k[1]}"
        n_int = 0
        for i_, r in enumerate(rr_):
            inv_rec = inventory.get(r.get("run_id"))
            att = (inv_rec or {}).get("attempt")
            if inv_rec is not None and att is None:
                invalid.append(f"{tag}: 실행 {r['run_id'][:8]} 폴더에 실행 전 기록 ({ATTEMPT_NAME}) 이 없다 — 재시도 필드를 대조할 수 없다")
            elif att is not None and any(att.get(f_) != r.get(f_) for f_ in fields):
                invalid.append(f"{tag}: 실행 {r['run_id'][:8]} 의 {ATTEMPT_NAME} 재시도 필드가 장부와 다르다")
            if i_ == 0:
                if any(r.get(f_) for f_ in fields):
                    invalid.append(f"{tag}: 첫 실행 {r['run_id'][:8]} 에 재시도 필드가 있다")
                continue
            p_ = rr_[i_ - 1]
            pf = (inventory.get(p_.get("run_id")) or {}).get("path")
            pfs = verdict_file_status(pf) if pf else None
            pk = run_kind(p_, pf, values)                  # 회신 DK P0-2 — 러너와 같은 분류 (DO 전 리뷰 — 보존 폴더 녹음 판정까지)
            if pk == "scientific":
                invalid.append(f"{tag}: 과학적 판정 ({p_.get('verdict') or pfs}) 뒤에 같은 시드를 다시 돌렸다"); continue
            if pk == "unreadable":
                invalid.append(f"{tag}: 앞 실행 {str(p_.get('run_id'))[:8]} 판정을 못 읽는데 (판정 파일 · 장부 값) 다시 돌렸다"); continue
            kind = pk
            if kind == "interrupted":
                n_int += 1
            if r.get("retry_of") != p_.get("run_id"):
                invalid.append(f"{tag}: 실행 {r['run_id'][:8]} 의 retry_of {str(r.get('retry_of'))[:8]} ≠ 바로 앞 실행 {str(p_.get('run_id'))[:8]}")
            if r.get("retry_kind") != kind:
                invalid.append(f"{tag}: 실행 {r['run_id'][:8]} 의 retry_kind {r.get('retry_kind')!r} ≠ 앞 실행 종류 {kind!r}")
            h = hist.get(r.get("retry_stop_id"))
            if not (h and h.get("acked_at") and h.get("run_id") == p_.get("run_id") and h.get("code") in RETRY_BIND_CODES[kind]):
                invalid.append(f"{tag}: 실행 {r['run_id'][:8]} 이 앞 실행에 묶여 확인된 STOP ({' · '.join(RETRY_BIND_CODES[kind])}) 과 안 묶인다")
            else:
                st_ = folder_stage(pf) if pf else None
                dp = declaration_problems(h.get("declaration"), kind, values, prev_status=p_.get("status_before_orphan") or p_.get("status"),
                                          rejudge_needed=(kind == "invalid" and st_ in ("final", "md_complete")))
                if dp:
                    invalid.append(f"{tag}: 재시도 선언 — " + " · ".join(dp))
            st_p, st_pw = folder_stage_detail(pf) if pf else (None, None)
            if st_p == "unreadable":
                invalid.append(f"{tag}: 앞 실행 {str(p_.get('run_id'))[:8]} 폴더의 완료 단계를 못 읽는데 다시 돌렸다 ({st_pw})")
            elif kind == "interrupted" and st_p in ("final", "md_complete"):
                invalid.append(f"{tag}: 앞 실행이 끝까지 (또는 MD 까지) 돌았는데 다시 돌렸다 — 판정 · FIRE 복구 대상")
        if n_int > max_int:
            invalid.append(f"{tag}: 끊긴 런 재시도 {n_int} 번 > 카드 한도 {max_int} (앞 실행 종류로 셈)")
    for r in runs:                                            # 실패를 보존 폴더로 옮겨 새 실행으로 대체해도 과학적 탈락은 사라지지 않는다
        if not isinstance(r, dict) or not (r.get("verdict") == "fail"
                                           or (isinstance(r.get("melt_check"), dict) and r["melt_check"].get("verdict") == "fail")):
            continue                                          # ⭐ DP 전 리뷰 (둘째) — 장부에 적힌 녹음 fail (복구 때 관측 포함) 도 과학적 fail
        vv = verdicts.get((r.get("system"), r.get("seed")))
        if vv is not None and vv.get("run_id") != r.get("run_id"):
            invalid.append(f"{r.get('system')}{r.get('seed')}: 과학적 fail 실행을 다른 실행으로 대체했다")
    for (s, sd), vv in verdicts.items():
        if vv is None:
            continue
        rid = vv.get("run_id")
        if not (isinstance(rid, str) and rid):
            (pending if vv.get("status") == "incomplete" else invalid).append(f"{s}{sd} 판정에 run_id 가 없다 — 장부와 못 잇는다")
            continue
        r = by_id.get(rid)
        if r is None:
            invalid.append(f"{s}{sd} 판정의 run_id {rid[:8]} 가 장부에 없다 — 비용이 안 잡힌 실행")
        elif (r.get("system"), r.get("seed")) != (s, sd):
            invalid.append(f"{s}{sd} 판정의 run_id {rid[:8]} 는 장부에서 {r.get('system')}{r.get('seed')} 런이다")
        else:                                                 # ⭐ 회신 DP P1-2 · DQ 전 리뷰 P1-A — 같은 실행의 판정 충돌 (러너 ①-4 와 같은 함수)
            cf_ = ledger_verdict_conflict(r, vv.get("status"), recorded=False, folder_provenance=vv.get("provenance"),
                                          folder_prior=(folder_verdict_chain(pathlib.Path(out_root) / s / f"seed{sd}")
                                                        if r.get("verdict") in (None, "invalid", "incomplete") else None))   # ⭐ DR 전 2차 리뷰 P1
            if cf_:
                invalid.append(f"{s}{sd}: 같은 실행 {rid[:8]} — {cf_} · 원자료 · 도구가 바뀌었거나 덮인 기록 (사람이 본다)")
    return {"total_h": tot, "cap_h": float(values["stage1_cap_gpu_h"]), "invalid": invalid, "pending": pending,
            "runs": len(runs), "attested": attested, "closing": closing, "terminal_stop": terminal_stop, "source": str(p)}


VERDICT_SHAPE = (("status", (str,)), ("run_id", (str,)), ("system", (str,)), ("seed", (int,)), ("closes_system", (bool,)),
                 ("provenance", (dict,)), ("reasons", (dict,)), ("software", (dict,)), ("checks", (dict,)), ("history", (dict,)),
                 ("gate_check", (dict,)), ("melt_window_check", (dict,)), ("seed_gate_view", (dict,)))


def _verdict_shape_problem(vv):
    """⭐ 회신 DO P2 — 묶음 판정이 쓰는 판정 기록 필드의 꼴. 없음 · None 은 허용 · 있는데 타입이 다르면 문제 (그 시드는 invalid · 정수로 바꿔 읽지 않는다).
    provenance 안 (files_sha256 · 카드 값 · 도구 지문) · reasons 의 값 (목록) · checks 의 identity 까지 본다."""
    for k, kinds in VERDICT_SHAPE:
        x = vv.get(k)
        if x is not None and (not isinstance(x, kinds) or (isinstance(x, bool) and bool not in kinds)):
            return f"{k} 타입이 {type(x).__name__} 이다 (기대 {' · '.join(t.__name__ for t in kinds)})"
    pv = vv.get("provenance") or {}
    for k, kinds in (("files_sha256", (dict,)), ("card_values_sha16", (str,)), ("driver_sha16", (str,)), ("judge_values_sha16", (str,)),
                     ("band_sha16", (str,)), ("runtime", (dict,)), ("derived_written", (list,)), ("judge_nature", (dict,))):   # ⭐ 회신 DQ P1-1
        x = pv.get(k)
        if x is not None and not isinstance(x, kinds):
            return f"provenance 의 {k} 타입이 {type(x).__name__} 이다"
    jn = pv.get("judge_nature")
    if jn is not None and not all(isinstance(jn.get(k), list) and all(isinstance(e, str) for e in jn[k]) for k in ("errors", "input_mismatch")):
        return "provenance 의 judge_nature 가 errors · input_mismatch 글자 목록이 아니다"
    fo = pv.get("folder")
    if fo is not None and not (isinstance(fo, list) and len(fo) == 2 and all(isinstance(x, str) for x in fo)):
        return "provenance 의 folder 가 [계 폴더, 시드 폴더] 글자 둘이 아니다"
    for k, x in (vv.get("reasons") or {}).items():
        if not isinstance(x, list):
            return f"reasons 의 {k} 가 목록이 아니다 ({type(x).__name__})"
    idn = (vv.get("checks") or {}).get("identity")
    if idn is not None and not isinstance(idn, dict):
        return f"checks 의 identity 타입이 {type(idn).__name__} 이다"
    return None


def _summary_failed(why):
    """⭐ 회신 DO P2 — 묶음 판정이 예외로 끝나면 이 꼴로 (invalid) — 이전 stage1_summary.json (예 stage1_pass) 이 남지 않게."""
    per = {s: {"status": "invalid", "per_seed": {}, "n_pass": 0, "n_fail": 0, "n_open": 0, "closed_by_first_seed": []} for s in ("A", "B")}
    return {"per_system": per, "software_variants": [], "stage2": None, "unknown_status": [], "identity_problems": [], "cost": None,
            "track": "invalid", "why": f"묶음 판정 중 예외 ({why}) — 판정 · 장부 기록의 꼴이 틀렸을 수 있다 · 이전 요약을 남기지 않는다 (fail-closed)",
            "stale_verdicts": [], "error": why}


def mark_summary_not_current(out_root, why):
    """⭐ DQ 전 리뷰 P2-F — 러너가 이 run_root 로 시작하면 이전 묶음 요약이 **통과 (stage1_pass) 이거나 못 읽는 것** 이면 '지금 기록의 판정이 아님'
    (track pending · not_current) 으로 바꾼다 — 시작 점검에서 거부 · 멈춰도 낡은 통과 요약이 남지 않게 (다시 판정하면 새 요약이 덮는다).
    통과가 아닌 요약 (stop_track · invalid · pending) 은 그대로 둔다 (낡아도 통과로 읽히지 않는다 · 2차 리뷰). 요약 파일이 없으면 아무것도 안 한다 (False).
    쓰기가 실패하면 이전 요약을 지우고 다시 던진다 (_summary_write_or_drop)."""
    q = pathlib.Path(out_root) / "stage1_summary.json"
    if not os.path.lexists(q):
        return False
    try:                                                     # ⭐ DQ 전 2차 리뷰 — 통과가 아닌 요약 (stop_track · invalid · pending) 은 그대로 둔다 (낡아도 통과로 읽히지 않는다)
        old_ = loads_strict(q.read_text(encoding="utf-8"))
        if isinstance(old_, dict) and old_.get("track") != "stage1_pass":
            return False
    except (OSError, ValueError, UnicodeDecodeError, RecursionError):
        pass                                                 # 못 읽는 요약은 '지금 판정 아님' 으로 바꾼다
    per = {s_: {"status": "pending", "per_seed": {}, "n_pass": 0, "n_fail": 0, "n_open": 0, "closed_by_first_seed": []} for s_ in ("A", "B")}
    _summary_write_or_drop(q, {"per_system": per, "software_variants": [], "stage2": None, "unknown_status": [], "identity_problems": [],
                               "cost": None, "track": "pending", "not_current": True, "stale_verdicts": [],
                               "why": f"이 요약은 지금 기록의 판정이 아니다 — {why} (러너가 다시 판정해 덮거나 --stage1_summary 로 다시 낸다)"})
    return True


def _summary_write_or_drop(q, res):
    """⭐ DP 전 리뷰 (둘째) F3 — 요약을 임시 파일 → 이름 교체로 쓴다. 쓰기가 실패하면 (임시 자리가 디렉터리 · 공간 없음 · 신호) 이전 요약을 지우고
    다시 던진다 — 낡은 stage1_pass 가 남지 않게 (fail-closed). 임시 파일은 우리가 만든 것만 지운다."""
    q_tmp = q.with_name(q.name + ".tmp")
    made = False
    try:
        fd = os.open(str(q_tmp), os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0), 0o644)
        made = True
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(res, ensure_ascii=False, indent=1, default=str))
            _fsync_handle(fh)
        os.replace(q_tmp, q)
    except BaseException:
        try:
            if made:
                os.unlink(q_tmp)
        except OSError:
            pass
        try:
            os.unlink(q)
        except OSError:
            pass
        raise


def stage1_summary(out_root, *, values=None, card=LI2S2_CARD, log=print):
    """<out_root>/<A|B>/seed<S>/stage1_verdict.json 을 모아 묶음 판정 → <out_root>/stage1_summary.json.
    ⭐ 회신 DG P1-4 — 판정 파일을 그대로 믿지 않는다: 지문 (원자료 · 카드 값 · 도구) 을 지금 것과 다시 잰다 → 안 맞으면 그 시드는
    invalid ('다시 판정하라'). 비용 장부 (러너) 로 상한을 다시 잰다 (DG P0-3).
    ⭐ 회신 DO P2 — 판정 기록의 중첩 꼴이 틀리면 그 시드는 invalid · 그래도 예외가 나면 invalid 요약을 쓴다 (이전 통과 파일을 남기지 않는다) ·
    요약 파일은 임시 파일 → 이름 교체로 쓴다."""
    root = pathlib.Path(out_root)
    q = root / "stage1_summary.json"
    try:
        v = values if values is not None else read_li2s2_values(card)
        res = _stage1_summary_core(root, v)
    except Exception as e:
        res = _summary_failed(f"{type(e).__name__}: {str(e)[:160]}")
    except BaseException as e:                               # ⭐ DP 전 리뷰 (둘째) F3 — Ctrl-C · 신호도: 이전 요약 (예 stage1_pass) 을 남기지 않고 다시 던진다
        _summary_write_or_drop(q, _summary_failed(f"{type(e).__name__} (중단)"))
        raise
    _summary_write_or_drop(q, res)
    log(f"  [stage1 묶음] {res['track']} — {res['why']} · " +
        " · ".join(f"{s} {res['per_system'][s]['status']} ({res['per_system'][s]['n_pass']} 통과)" for s in ("A", "B")) +
        (f" · 2 단계 시드 {res['stage2']['seeds']} {res['stage2']['machines']}" if res.get("stage2") else "") +
        (f" · 비용 {res['cost']['total_h']:.1f}/{res['cost']['cap_h']:g} h" if res.get("cost") and _fin(res["cost"].get("total_h")) else "") +
        (f" · ⛔ 판정 무효 (지문 · 미해결 기록 · 꼴) {res.get('stale_verdicts')}" if res.get("stale_verdicts") else ""))
    return res


def _stage1_summary_core(root, v):
    ver = {}
    cur_vals, cur_drv = values_sha16(v), driver_sha16()
    stale = []
    for s in ("A", "B"):
        for sd in v["seeds"]:
            rd = root / s / f"seed{sd}"
            p = rd / "stage1_verdict.json"
            if not p.is_file():
                ur_ = unresolved_first_write(rd)                # ⭐ 회신 DQ P1-2 — 정본이 없어도 이력 · 임시 파일을 먼저 본다 (첫 판정 쓰기 끊김 ≠ 판정 안 함)
                if ur_:
                    ver[(s, sd)] = {"status": "invalid", "system": s, "seed": sd, "closes_system": False,
                                    "reasons": {"invalid": [f"미해결 판정 기록 — {ur_}"]}}
                    stale.append(f"{s}{sd}")
                else:
                    ver[(s, sd)] = None
                continue
            try:
                vv = loads_strict(p.read_text(encoding="utf-8"))
                if not isinstance(vv, dict):
                    raise ValueError("판정이 객체가 아니다")
            except (ValueError, UnicodeDecodeError, RecursionError) as e:     # ⭐ DO 전 리뷰 — 잘린 판정에 죽지 않는다
                ver[(s, sd)] = {"status": "invalid", "system": s, "seed": sd, "closes_system": False,
                                "reasons": {"invalid": [f"판정 파일을 못 읽는다 ({type(e).__name__}) → --stage1_verdict 로 다시 판정"]}}
                stale.append(f"{s}{sd}")
                continue
            recs_, rprob_ = _verdict_records(rd)              # ⭐ 회신 DP P1-1 — 현재 폴더의 미해결 기록 (판정 임시 파일 · 깨진 이력 · 원문만 남은 판정)
            if rprob_ is None and any(isinstance(r_, dict) and r_.get("status") is None for _, r_, part_ in recs_ if not part_):
                rprob_ = ("판정 이력에 못 읽은 이전 판정 (상태 없음 · 원문만) 이 있다 — 그 원문이 과학적 판정이었는지 모른다 · 최신 판정으로 "
                          "자동 해제하지 않는다 (사람이 원문을 보고 정한다)")
            if rprob_:
                ver[(s, sd)] = {"status": "invalid", "system": s, "seed": sd, "closes_system": vv.get("closes_system") is True,
                                "run_id": vv.get("run_id") if isinstance(vv.get("run_id"), str) else None,
                                "reasons": {"invalid": [f"미해결 판정 기록 — {rprob_}"]}}
                stale.append(f"{s}{sd}")
                continue
            shp = _verdict_shape_problem(vv)                  # ⭐ 회신 DO P2 — 중첩 꼴 (provenance [1] · software [1] · run_id {} …)
            if shp:
                ver[(s, sd)] = {"status": "invalid", "system": s, "seed": sd, "closes_system": vv.get("closes_system") is True,
                                "reasons": {"invalid": [f"판정 기록 꼴이 틀렸다 ({shp}) → --stage1_verdict 로 다시 판정"]}}
                stale.append(f"{s}{sd}")
                continue
            bad = provenance_current_problems(vv.get("provenance"), rd, v)   # ⭐ 회신 DQ P1-1 — _run_kind 와 같은 대조 (G4 밴드 카드 · 파생 · 실행 전 기록 포함)
            if bad:
                stale.append(f"{s}{sd}")
                vv = {**vv, "status": "invalid", "closes_system": vv.get("closes_system") is True,
                      "reasons": {**(vv.get("reasons") or {}), "invalid": list((vv.get("reasons") or {}).get("invalid", []))
                                  + [f"⛔ 판정이 원자료에 안 묶였다 — {' · '.join(bad)} → --stage1_verdict 로 다시 판정"]}}
            ver[(s, sd)] = vv
    res = summarize_stage1(ver, v, cost=ledger_check(root, ver, v))
    res["stale_verdicts"] = stale
    return res


def schedule(T_melt, T_final, quench_rate_K_s, dt_fs):
    if quench_rate_K_s is None or quench_rate_K_s <= 0:
        raise SystemExit("⛔ --quench_rate [K/s] 를 주어라 (G2: 담금질 속도는 결과 보기 전에 선언한다). 기본값은 없다.")
    quench_ps = (T_melt - T_final) / quench_rate_K_s * 1e12
    n = int(round(quench_ps * 1000.0 / dt_fs))
    return quench_ps, n


def run_melt_quench(atoms, calc, out, *, seed, T_melt, T_final, melt_ps, quench_rate, hold_ps, dt_fs, save_ps,
                    pre_relax=True, fix_density=None, compress_ps=20.0, log=print, run_id=None):
    from ase import units
    from ase.io import write
    from ase.md.nptberendsen import NPTBerendsen
    from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary
    from ase.optimize import FIRE
    validate_fix_density(fix_density, compress_ps, melt_ps)
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    atoms.calc = calc
    if pre_relax:
        FIRE(atoms, logfile=str(out / "prerelax.log")).run(fmax=1.0, steps=200)
    MaxwellBoltzmannDistribution(atoms, temperature_K=T_melt, rng=np.random.default_rng(seed)); Stationary(atoms)
    dt = dt_fs * units.fs
    if fix_density is None:
        dyn = NPTBerendsen(atoms, dt, temperature_K=T_melt, pressure_au=0.0,
                           taut=BARO["taut_fs"] * units.fs, taup=BARO["taup_fs"] * units.fs,
                           compressibility_au=BARO["compressibility_au"])
    else:   # ⭐ li2s-2 — 같은 열욕 (taut) · 바로스탯 없음 · melt 첫 compress_ps 동안 밀도를 ρ 로 끌어올린다
        from ase.md.nvtberendsen import NVTBerendsen
        dyn = NVTBerendsen(atoms, dt, temperature_K=T_melt, taut=BARO["taut_fs"] * units.fs)
        rho0 = density_g_cm3(atoms)
        n_c = max(1, int(round(compress_ps * 1000 / dt_fs)))
    quench_ps, n_q = schedule(T_melt, T_final, quench_rate, dt_fs)
    n_m = int(round(melt_ps * 1000 / dt_fs)); n_h = int(round(hold_ps * 1000 / dt_fs))
    save_int = max(1, int(round(save_ps * 1000 / dt_fs)))
    trj = out / "traj.xyz"; trj.unlink(missing_ok=True)
    tlog = open(out / "thermo.csv", "w"); tlog.write("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
    step = 0; t0 = time.time()
    def record(T_set):
        nonlocal step
        if step % save_int == 0:
            write(str(trj), atoms, format="extxyz", append=True)
            vol = atoms.get_volume(); rho = sum(MASS[s] for s in atoms.get_chemical_symbols()) / 6.02214076e23 / (vol * 1e-24)
            tlog.write(f"{step*dt_fs/1000:.3f},{atoms.get_temperature():.1f},{T_set:.1f},{rho:.4f},{vol:.2f},"
                       f"{atoms.get_potential_energy():.4f},{pressure_GPa(atoms):.4f},"
                       f"{pressure_GPa(atoms, include_ideal_gas=False):.4f}\n"); tlog.flush()
    chunk = 50
    for phase, n_steps, Tfun in (("melt", n_m, lambda i: T_melt),
                                 ("quench", n_q, lambda i: T_melt - (T_melt - T_final) * i / max(1, n_q)),
                                 ("hold", n_h, lambda i: T_final)):
        i = 0
        while i < n_steps:
            T_set = Tfun(i); dyn.set_temperature(temperature_K=T_set)
            k = min(chunk, n_steps - i)
            if fix_density is not None and phase == "melt" and i < n_c:
                # 이 덩어리가 끝날 때의 목표 밀도로 먼저 맞춘다 — 마지막 덩어리에서 정확히 ρ 에 닿는다
                scale_to_density(atoms, rho0 + (float(fix_density) - rho0) * min(1.0, (i + k) / n_c))
            for _ in range(k):
                record(T_set); dyn.run(1); step += 1
            i += k
            if (i // chunk) % 200 == 0:
                log(f"  [{phase}] {i}/{n_steps} T_set={T_set:.0f} K T={atoms.get_temperature():.0f} K "
                    f"ρ={sum(MASS[s] for s in atoms.get_chemical_symbols())/6.02214076e23/(atoms.get_volume()*1e-24):.3f} "
                    f"({(time.time()-t0)/60:.1f} min)")
                sys.stdout.flush()   # ⛔ 로그 리다이렉트 시 블록 버퍼링 — 안 하면 진행 줄이 몇 시간 뒤에 뜬다
    record(T_final); tlog.close()
    if fix_density is not None:
        rho_end = density_g_cm3(atoms)
        if abs(rho_end / float(fix_density) - 1.0) > 1e-9:   # 압축이 덜 끝났거나 셀이 움직였다 — 조용히 넘기지 않는다
            raise SystemExit(f"⛔ --fix_density {fix_density}: 담금질 끝 밀도 {rho_end:.6f} 가 목표와 다르다")
    write_md_done(out, run_id=run_id, n_steps_planned=n_m + n_q + n_h, n_steps_done=step)   # ⭐ 회신 DK — MD 완료의 증거 (FIRE 전)
    FIRE(atoms, logfile=str(out / "final_relax.log")).run(fmax=0.05, steps=2000)
    write(str(out / "final.xyz"), atoms, format="extxyz")
    write(str(out / "final.vasp"), atoms, format="vasp", direct=True, sort=True)
    info = {"quench_ps": quench_ps, "n_steps": {"melt": n_m, "quench": n_q, "hold": n_h}, "wall_min": (time.time() - t0) / 60}
    if fix_density is not None:
        info["fix_density"] = {"target_g_cm3": float(fix_density), "start_g_cm3": rho0, "compress_steps": n_c,
                               "final_g_cm3": density_g_cm3(atoms)}
    return info


def write_gr_csv(cols, path):
    keys = list(cols)
    with open(path, "w") as f:
        f.write(",".join(keys) + "\n")
        for i in range(len(cols["r_A"])):
            f.write(",".join(f"{cols[k][i]:.5f}" for k in keys) + "\n")


def build_plan(system, seed, sym, density, T_melt, T_final, melt_ps,
               quench_rate, quench_ps, hold_ps, dt_fs, save_ps, fix_density=None, compress_ps=20.0):
    """plan.json 의 내용. **게이트가 읽을 값이 여기서 들어간다** — 읽는 곳은 `--gate_check`.
    `fix_density` 를 주면 게이트_입력 의 앙상블이 NVT (ensemble_fixed_density) 로 바뀐다 — 옵션이 없으면 옛 plan 과 같은 키다."""
    ens = ENSEMBLE if fix_density is None else ensemble_fixed_density(fix_density, compress_ps)
    extra = {} if fix_density is None else {"fix_density_g_cm3": float(fix_density), "compress_ps": float(compress_ps),
                                            "card_fix_density": "db/properties/lpscl_glass_dense_window_estimand_2026_11_03.json"}
    return {"system": system, "seed": seed, "n_atoms": len(sym), **extra,
            "composition": {e: sym.count(e) for e in sorted(set(sym))},
            "start_density_g_cm3": density, "T_melt_K": T_melt, "T_final_K": T_final, "melt_ps": melt_ps,
            "quench_rate_K_s": quench_rate, "quench_ps": quench_ps, "hold_ps": hold_ps, "dt_fs": dt_fs,
            "save_ps": save_ps,   # ⛔ 빠뜨리면 --melt_check 가 dt 를 **유도**한다 (2026-09-12)
            "G2_declared_before_results": True,
            "card": "db/properties/lpscl_li2s_interphase_prereg_2026_09_11.json",
            # ⭐ 게이트가 읽는 값 — 누가 읽나: `--gate_check`. 없으면 그 모드가 **기록없음** 으로 fail-closed 한다.
            "게이트_입력": {"G2_quench_rate_K_s": quench_rate, **ens, "final_relax": final_relax_decl(fix_density),
                         "G4_band_card": BAND_CARD, "읽는_곳": "melt_quench_uma.py --gate_check <run_dir>"}}


# ───────────────────────── --mode_stress: 실행모드별 **응력** 대조 (회신 BR Q4) ─────────────────────────
KAPPA_PER_GPA = 1.0 / 20.0      # BARO compressibility_au 8.0 Å³/eV ≈ 1/(20 GPa). 환산 규칙이지 문턱이 아니다.


def read_frame_card(card):
    """봉인된 프레임 표본을 카드에서 읽는다. 도구가 프레임을 **고르지 않는다**.

    ⛔ 못 하는 것: 카드가 없거나 t_ps 목록이 없으면 죽는다 — 기본 표본을 지어내지 않는다."""
    q = pathlib.Path(card)
    if not q.exists():
        q = pathlib.Path(__file__).resolve().parents[2] / card
    d = json.loads(q.read_text(encoding="utf-8"))
    try:
        want = list(d["1_프레임_표본_봉인"]["t_ps"])
    except (KeyError, TypeError):
        raise KeyError(f"{q}: `1_프레임_표본_봉인.t_ps` 가 없다 — 표본을 도구가 지어내지 않는다")
    if not want or len(set(want)) != len(want):
        raise ValueError(f"{q}: t_ps 가 비었거나 중복이다 ({want})")
    return [float(x) for x in want], str(q)


def frame_index_map(traj_path, thermo_path):
    """traj 프레임 수와 thermo 행 수가 같은지 확인하고 t_ps ↔ 색인 대응을 만든다.

    ⛔ 다르면 **멈춘다**. '아마 같은 간격일 것' 으로 넘어가면 엉뚱한 프레임을 재게 된다."""
    from ase.io import iread
    n_traj = sum(1 for _ in iread(str(traj_path), index=":", format="extxyz"))
    t = read_thermo(thermo_path)
    n_thermo = len(t["t_ps"])
    if n_traj != n_thermo:
        raise ValueError(f"⛔ traj 프레임 {n_traj} ≠ thermo 행 {n_thermo} — 색인 대응을 만들 수 없다")
    return {float(v): i for i, v in enumerate(t["t_ps"])}, n_traj


def stress_report(atoms, calc):
    """같은 **미완화** 셀·좌표에서 potential/virial 응력과 힘. (운동 항 없음 — 비교 규칙)"""
    atoms = atoms.copy(); atoms.calc = calc
    sig = np.asarray(atoms.get_stress(voigt=False))          # eV/Å³
    F = np.asarray(atoms.get_forces())
    return {"P_virial_GPa": float(-np.trace(sig) / 3.0 * EV_A3_TO_GPA),
            "sigma_GPa": sig * EV_A3_TO_GPA, "F": F,
            "sigma_rms_GPa": float(np.sqrt(((sig * EV_A3_TO_GPA) ** 2).mean())),
            "F_rms_eVA": float(np.sqrt((F ** 2).mean()))}


def mode_stress(run, card, device="cuda", log=print):
    """봉인된 프레임에서 turbo − default 의 **응력·힘** 차이를 찍는다. 새 MD 0.

    ⛔ 이 함수가 못 하는 것
      · 합격/불합격을 정하지 않는다 — 카드 §3 이 '문턱을 정하지 않는다' 고 봉인했다.
      · UMA 가 맞는지 모른다 — 그것은 G1(QE 참조)이다.
      · 작은 차이를 **전체 담금질 경로의 승인**으로 읽지 않는다 (그 프레임들의 일치까지다).
    """
    run = pathlib.Path(run)
    want, card_path = read_frame_card(card)
    idx, n_traj = frame_index_map(run / "traj.xyz", run / "thermo.csv")
    missing = [w for w in want if w not in idx]
    if missing:
        raise ValueError(f"⛔ 봉인된 프레임 중 traj 에 없는 것: {missing}")
    from ase.io import iread
    wanted_i = {idx[w]: w for w in want}
    frames = {}
    for i, at in enumerate(iread(str(run / "traj.xyz"), index=":", format="extxyz")):
        if i in wanted_i:
            frames[wanted_i[i]] = at
        if len(frames) == len(want):
            break
    log(f"카드: {card_path}")
    log(f"봉인된 프레임 {len(want)}개 · traj {n_traj} 프레임에서 색인 대조 통과")
    cal_d = make_calc(device, turbo=False)
    cal_t = make_calc(device, turbo=True)
    if getattr(cal_t, "_mq_mode", "default") != "turbo":
        log("⛔ turbo 를 못 켰다 — 두 모드가 같은 것이라 비교가 성립하지 않는다. 멈춘다.")
        raise SystemExit(3)
    rows = []
    for w in want:
        at = frames[w]
        rd, rt = stress_report(at, cal_d), stress_report(at, cal_t)
        dP = rt["P_virial_GPa"] - rd["P_virial_GPa"]
        dsig = float(np.abs(rt["sigma_GPa"] - rd["sigma_GPa"]).max())
        dF = float(np.abs(rt["F"] - rd["F"]).max())
        rows.append({"t_ps": w, "P_default_GPa": rd["P_virial_GPa"], "P_turbo_GPa": rt["P_virial_GPa"],
                     "dP_GPa": dP, "dV_over_V_pct": 100.0 * dP * KAPPA_PER_GPA,
                     "max_dsigma_GPa": dsig, "sigma_rms_GPa": rd["sigma_rms_GPa"],
                     "max_dF_eVA": dF, "F_rms_eVA": rd["F_rms_eVA"]})
        log(f"  t={w:7.1f} ps  P_def {rd['P_virial_GPa']:+8.4f}  P_tur {rt['P_virial_GPa']:+8.4f}  "
            f"ΔP {dP:+.4f} GPa (ΔV/V {100.0*dP*KAPPA_PER_GPA:+.3f} %)  "
            f"max|Δσ| {dsig:.4f}  max|ΔF| {dF:.2e} (|F|rms {rd['F_rms_eVA']:.3f})")
    res = {"card": card_path, "run": str(run), "n_frames": len(rows), "frames": rows,
           "max_abs_dP_GPa": max(abs(r["dP_GPa"]) for r in rows),
           "max_abs_dV_over_V_pct": max(abs(r["dV_over_V_pct"]) for r in rows),
           "max_dsigma_GPa": max(r["max_dsigma_GPa"] for r in rows),
           "max_dF_eVA": max(r["max_dF_eVA"] for r in rows),
           "⛔_문턱": "카드 §3 — 이 잡은 문턱을 정하지 않는다. 앵커는 G1 의 default − QE 응력 차이다.",
           "⛔_작은_차이의_뜻": "이 프레임들의 일치일 뿐 전체 담금질 경로의 승인이 아니다."}
    log(f"\n  max|ΔP| {res['max_abs_dP_GPa']:.4f} GPa → ΔV/V {res['max_abs_dV_over_V_pct']:+.3f} % "
        f"· max|Δσ| {res['max_dsigma_GPa']:.4f} GPa · max|ΔF| {res['max_dF_eVA']:.2e} eV/Å")
    log("  ⛔ 문턱 없음 — 보고만 한다. 작은 차이는 이 프레임들의 일치이지 경로 전체의 승인이 아니다.")
    return res


# ───────────────────────── --gate_check: 기록이 게이트를 먹여주는가 ─────────────────────────
def read_thermo(path):
    """thermo.csv → {열이름: np.array}. 열이 없으면 **죽는다** (없는 값을 0 으로 그리지 않는다)."""
    lines = [ln for ln in pathlib.Path(path).read_bytes().decode("utf-8", errors="replace").split("\n") if not _junk(ln)]
    lines = [ln.rstrip("\r") for ln in lines]                 # 정전 꼬리 (NUL · 빈 줄) 는 건너뛴다 · 덜 써진 줄은 그대로 (그러면 실패 → 오류)
    if len(lines) < 2:
        raise ValueError(f"{path}: 자료 줄이 없다")
    keys = lines[0].split(",")
    cols = np.array([[float(x) for x in ln.split(",")] for ln in lines[1:] if ln.strip()])
    return {k: cols[:, i] for i, k in enumerate(keys)}


def read_band(card=BAND_CARD):
    """G4 밴드를 **카드에서** 읽는다 — 도구가 숫자를 자체 보관하지 않는다.
    절이나 키가 없으면 KeyError 로 죽는다: '못 찾음' 을 기본값으로 채우지 않는다."""
    q = _band_card_path(card)                # repo 루트 상대 (도구가 어디서 불리든 같은 카드 · band_card_sha16 과 같은 해석)
    d = loads_strict(q.read_text(encoding="utf-8"))          # ⭐ 회신 DO P1 — G4 밴드 카드도 같은 열쇠 둘을 받지 않는다
    for k in BAND_PATH:
        if not isinstance(d, dict) or k not in d:
            raise KeyError(f"{q}: 밴드 절 '{k}' 가 없다 — 밴드를 도구가 지어내지 않는다")
        d = d[k]
    lo, hi = d["밴드_±15%"]
    return float(d["중심"]), float(lo), float(hi)


def hold_segment(t):
    """thermo 의 **마지막 연속 T_set 일정 구간**(= 300 K 유지)의 불리언 마스크.

    ⚠ 담금질 램프의 **마지막 프레임은 T_set 이 이미 T_final** 이라 유지 구간에 포함된다. 의도한 선택이다
    (그 순간부터 목표 온도다). 프레임 하나 차이이고, 배제하려면 호출부가 t 범위를 직접 자른다.

    ⛔ 이 함수가 못 하는 것: 유지 구간이 평형인지 말하지 않는다. 어디까지가 유지인지만 고른다."""
    if "T_set_K" not in t:
        raise KeyError("thermo.csv 에 T_set_K 가 없다 — 유지 구간을 **추측하지 않는다**")
    ts = t["T_set_K"]
    last = ts[-1]
    m = np.isclose(ts, last)
    # 마지막 연속 구간만 (담금질 램프가 지나가며 같은 값을 스칠 수 있다)
    i = len(m) - 1
    while i > 0 and m[i - 1]:
        i -= 1
    out = np.zeros_like(m); out[i:] = True
    return out


def hold_trend(t, n_blocks=5):
    """유지 구간 **전체**를 n 블록으로 나눠 블록별 ⟨P⟩·⟨ρ⟩ 와 ρ 표류를 찍는다. 새 계산 0.

    ⛔ 판정이 아니다 — 표류는 '유지시간이 모자랐다' 의 근거가 되고, 무표류는 **그 구간의 안정**만 지지한다.
    ⛔ 블록 평균의 산포는 표본 표준편차이지 평균의 신뢰구간이 아니다 (자기상관이 크다)."""
    m = hold_segment(t)
    tt, P, rho = t["t_ps"][m], t["P_GPa"][m], t["density_g_cm3"][m]
    if len(tt) < n_blocks:
        n_blocks = max(1, len(tt))
    idx = np.array_split(np.arange(len(tt)), n_blocks)
    blocks = [{"t_from_ps": float(tt[k[0]]), "t_to_ps": float(tt[k[-1]]), "n": int(len(k)),
               "P_mean_GPa": float(P[k].mean()), "rho_mean": float(rho[k].mean())} for k in idx if len(k)]
    span = float(tt[-1] - tt[0])
    slope = float(np.polyfit(tt, rho, 1)[0]) if len(tt) > 1 and span > 0 else 0.0
    return {"hold_from_ps": float(tt[0]), "hold_to_ps": float(tt[-1]), "hold_len_ps": span,
            "n_frames": int(len(tt)), "n_blocks": len(blocks), "blocks": blocks,
            "rho_slope_per_ps": slope, "rho_drift_pct_over_hold": float(100.0 * slope * span / rho.mean()),
            "block_rho_spread_pct": float(100.0 * (max(b["rho_mean"] for b in blocks)
                                                   - min(b["rho_mean"] for b in blocks)) / rho.mean()),
            "⛔": "관측이지 평형 검정이 아니다. 표류 없음은 **이 구간의 안정**만 지지한다."}


def gate_check(run, band_card=BAND_CARD, win_ps=10.0, p_tol=P_TOL_GPA, n_blocks=5, log=print):
    """plan.json 의 **앙상블 선언**이 있는지 보고, 있으면 thermo.csv 로 대조한 뒤 G4(밀도 밴드)를 찍는다.

    ⛔ 이 함수가 못 하는 것
      · 판정하지 않는다 — G4 가 '밴드 밖' 으로 발화하는지까지만 말하고, 원인(UMA·셀·담금질)은 안 가른다.
      · ⟨P⟩≈0 을 정확한 NPT 표본화의 증명으로 읽지 않는다 (Berendsen).
      · 기록이 없는 옛 런에서 thermo 로 **역추적**은 하되, 그것을 기록으로 승격하지 않는다.
    """
    run = pathlib.Path(run)
    plan = loads_strict((run / "plan.json").read_text(encoding="utf-8"))   # ⭐ 회신 DO P1 (예외 → 판정이 '모름' 으로 적는다)
    g = plan.get("게이트_입력")
    res = {"run": str(run), "record_has_gate_input": bool(g),
           "출처": "plan.json 선언" if g else "thermo.csv 역추적 (기록 아님)"}
    if not g:
        log("⛔ plan.json 에 `게이트_입력` 이 없다 — G4 가 요구하는 앙상블·목표압력이 **기록에 없다**.")
        log("   2026-09-12 이전 실행이다. 아래 수치는 thermo 에서 역추적한 것이고, 기록이 아니다.")
    t = read_thermo(run / "thermo.csv")
    tail = t["t_ps"] >= t["t_ps"].max() - win_ps
    P, rho, T = t["P_GPa"][tail], t["density_g_cm3"][tail], t["T_K"][tail]
    res.update({"win_ps": win_ps, "n_frames": int(tail.sum()),
                "★_통계의_뜻": {
                  "P_sd_GPa": "저장된 표본의 **표준편차**다. 평균의 신뢰구간이 아니고 자기상관이 크다.",
                  "rho_flat_pct": "(최대−최소)/평균이다. **표류·평형을 검정한 값이 아니다.**",
                  "P_GPa": "**운동 항을 포함한 총 수압**이다. 평균이 0에 가까워도 응력텐서 전체가 0은 아니다."},
                "T_mean_K": float(T.mean()),
                "P_mean_GPa": float(P.mean()), "P_sd_GPa": float(P.std(ddof=1)) if tail.sum() > 1 else 0.0,
                "rho_mean": float(rho.mean()), "rho_min": float(rho.min()), "rho_max": float(rho.max()),
                "rho_last": float(t["density_g_cm3"][-1])})
    res["rho_flat_pct"] = 100.0 * (res["rho_max"] - res["rho_min"]) / res["rho_mean"]
    if g and g.get("ensemble") == "NVT":
        # ⭐ li2s-2 고정 밀도 런 — 압력은 결과 (기록) · 게이트는 '밀도 = 선언값' · 옛 G4 밴드 (1층 카드) 는 해당 없음
        rt = float(g["target_density_g_cm3"])
        dev = max(abs(res["rho_min"] / rt - 1.0), abs(res["rho_max"] / rt - 1.0), abs(res["rho_last"] / rt - 1.0))
        rho_ok = bool(dev <= DENSITY_REL_TOL)   # ⭐ 한 곳에서만 정한다 — density_ok 와 gate_ok 가 갈리면 깨기 시험이 못 본다 (11-03 실측)
        # ⭐ 회신 DF P1-2 — 밀도만 맞으면 통과하던 구멍 셋을 막는다: ① 계획한 일정 끝까지 ② 판정 창이 실제 유지 구간 안
        #   ③ 압력이 **기록돼 있다** (크기는 판정 아님 · NaN · 빈 칸이면 '압력이 없다' 로 가른다)
        total = float(plan["melt_ps"]) + float(plan.get("quench_ps") or 0.0) + float(plan["hold_ps"])
        sched_ok = bool(float(t["t_ps"].max()) >= total - float(plan["save_ps"]) - 1e-6)
        T_fin = float(plan["T_final_K"])
        in_hold = bool(tail.sum() > 0 and np.allclose(t["T_set_K"][tail], T_fin))
        try:
            ht = hold_trend(t, n_blocks)
        except KeyError as e:
            ht = {"⛔": str(e)}
        hold_ok = bool(in_hold and ht.get("hold_len_ps", 0.0) >= 0.9 * float(plan["hold_ps"]) - 1e-9)
        # ⛔ 회신 DG P1-7 — virial 열을 지워도 '기록 있음' 이던 구멍: 두 압력 열이 **다 있고** 유한해야 기록이다
        p_cols = [c for c in ("P_GPa", "P_virial_GPa") if c in t]
        cols_ok = len(p_cols) == 2 and all(c in t for c in ("t_ps", "T_set_K", "density_g_cm3"))
        p_tail = np.concatenate([t[c][tail] for c in p_cols]) if p_cols else np.array([])
        p_rec = bool(cols_ok and p_tail.size > 0 and np.isfinite(p_tail).all())
        gate_ok = bool(rho_ok and sched_ok and hold_ok and p_rec)
        res.update({"mode": "NVT_fixed_density", "target_density_g_cm3": rt, "density_max_rel_dev": dev,
                    "density_ok": rho_ok, "pressure_ok": None, "target_pressure_GPa": None,
                    "schedule_complete": sched_ok, "planned_total_ps": total, "window_in_hold": hold_ok,
                    "pressure_recorded": p_rec, "pressure_columns": p_cols, "thermo_columns_ok": cols_ok, "hold_trend": ht,
                    "gate_ok": gate_ok, "G4_fires": None, "G4_role": "해당 없음 (고정 밀도 · 1층 밴드 카드 밖)",
                    "P_role": "기록 — 고정 밀도에서 UMA 셀에 남는 내부 압력 (크기는 판정 아님 · 기록 유무는 판정)"})
        log(f"  NVT 고정 밀도 — 목표 {rt:.4f} · 마지막 {win_ps:g} ps ρ {res['rho_min']:.5f}–{res['rho_max']:.5f} "
            f"(최대 상대 차 {dev:.1e} → {'같음' if rho_ok else '⛔ 다름'}) · 일정 {'끝' if sched_ok else '⛔ 미완'} "
            f"({float(t['t_ps'].max()):g}/{total:g} ps) · 창 {'유지 구간 안' if hold_ok else '⛔ 유지 구간 밖'} · "
            f"⟨P⟩ {res['P_mean_GPa']:+.3f} GPa ({'기록' if p_rec else '⛔ 기록 없음'})")
        return res
    tgt = float(g["target_pressure_GPa"]) if g else 0.0
    res["target_pressure_GPa"] = tgt
    res["pressure_ok"] = abs(res["P_mean_GPa"] - tgt) <= p_tol
    res["gate_ok"] = res["pressure_ok"]
    c, lo, hi = read_band(band_card)
    res.update({"band_center": c, "band_lo": lo, "band_hi": hi, "band_card": str(band_card),
                "dev_pct_vs_center": 100.0 * (res["rho_last"] / c - 1.0),
                "in_band": bool(lo <= res["rho_last"] <= hi)})
    res["G4_fires"] = not res["in_band"]
    res["G4_role"] = "alert"        # ⭐ 합격선이 아니다 (D-2026-09-14-li2s-layer1-density-alert)
    res["G4_원인_지정"] = None       # 게이트는 원인을 지정하지 않는다 (셀·모델·후보상 어느 것도)
    res["허용_서술"] = ("마지막 {:.0f} ps 에서 목표 근처의 총 수압 평균과 좁은 밀도 범위가 관측됐다. "
                     "충분한 밀도 이완·준비 이력 소멸·모델의 압력–부피 정확성은 아직 확인되지 않았다."
                     ).format(win_ps)
    try:
        res["hold_trend"] = hold_trend(t, n_blocks)
    except KeyError as e:
        res["hold_trend"] = {"⛔": str(e)}
    log(f"  앙상블 기록 {'있음' if g else '⛔없음'} · {res['출처']}")
    log(f"  마지막 {win_ps:.0f} ps ({res['n_frames']} 표본): ⟨P_총수압⟩ {res['P_mean_GPa']:+.3f} GPa "
        f"(표본 sd {res['P_sd_GPa']:.3f}, 목표 {tgt:+.2f}, 허용 ±{p_tol}) "
        f"→ {'목표 근처' if res['pressure_ok'] else '목표에서 벗어남'}")
    log(f"  ρ {res['rho_min']:.4f}–{res['rho_max']:.4f} (범위/평균 {res['rho_flat_pct']:.2f} %) · "
        f"마지막 {res['rho_last']:.4f} g/cm³")
    ht = res.get("hold_trend", {})
    if "blocks" in ht:
        log(f"  유지 구간 {ht['hold_from_ps']:.0f}–{ht['hold_to_ps']:.0f} ps 를 {ht['n_blocks']} 블록으로:")
        for b in ht["blocks"]:
            log(f"    {b['t_from_ps']:7.1f}–{b['t_to_ps']:7.1f} ps (n={b['n']:4d})  "
                f"⟨P⟩ {b['P_mean_GPa']:+.3f} GPa  ⟨ρ⟩ {b['rho_mean']:.4f}")
        log(f"    ρ 표류 {ht['rho_drift_pct_over_hold']:+.3f} % / 유지 전체 · "
            f"블록 산포 {ht['block_rho_spread_pct']:.3f} %")
    else:
        log(f"  ⛔ 유지 구간 블록 추세 없음: {ht.get('⛔', '계산 안 됨')}")
    log(f"  밴드 [{lo:.4f}, {hi:.4f}] 중심 {c:.4f} → {res['dev_pct_vs_center']:+.2f} % · "
        + ("G4 **경보**" if res["G4_fires"] else "밴드 안"))
    log("  ⛔ G4 는 **합격선이 아니라 적정성 경보**다 — 셀 오류·모델 오류·후보상 기각 중 아무것도 확정하지 않는다.")
    log("  ⛔ 위 수치는 **단기 안정성**이다. 밀도 이완·준비 이력 소멸·모델의 압력–부피 정확성은 확인되지 않았다.")
    return res


# ───────────────────────── --seed_gate: 시드 게이트 입력을 **원시·relax 두 판**으로 ─────────────────────────
#: ⛔ 2026-09-24 발견 — 소셀 유리 MD 카드(`lpscl_smallcell_glass_md_estimand_2026_09_21.json`) 해명 1 은
#:   *"final.xyz = 담금질 마지막 프레임, 원시 (relax 안 한다)"* 라고 적었다. **이 파일과 안 맞는다** —
#:   `run_melt_quench` 는 FIRE(fmax 0.05 · 고정셀) **뒤에** final.xyz 를 쓴다 (FINAL_RELAX · 개정 ③ 이 이미 그렇게 적는다).
#:   원시는 traj.xyz 의 **마지막 프레임**뿐이다. 그래서 이 모드는 두 판을 **나란히** 찍고, 게이트를 어느 판으로
#:   잴지는 정하지 않는다 (카드·사람 몫 · 정오 기록 `lpscl_smallcell_glass_md_gateA_erratum_2026_09_24.json`).
#:   MD 초기구조로 쓸 원시 판은 `md_init_raw.xyz` 로 떨군다 — 이름이 곧 내용이다.
SEED_GATE_RAW = "md_init_raw.xyz"


def _min_pair(sym, pos, cell, skip=()):
    """최소상 최단 원자간 거리와 그 쌍의 원소. `skip` 의 원소쌍은 뺀다."""
    sym = np.asarray(sym)
    D = mic_dists(pos, pos, cell)
    np.fill_diagonal(D, np.inf)
    for a_el, b_el in skip:
        ia, ib = sym == a_el, sym == b_el
        D[np.ix_(ia, ib)] = np.inf
        D[np.ix_(ib, ia)] = np.inf
    i, j = np.unravel_index(np.argmin(D), D.shape)
    return float(D[i, j]), "-".join(sorted((str(sym[i]), str(sym[j]))))


def _gate_view(at):
    """시드 게이트가 보는 값만 — PS₄ · 다리 S · P–P · 최단 원자간(전체 · P–S 제외) · 밀도."""
    sym, pos, cell = at.get_chemical_symbols(), at.get_positions(), np.asarray(at.get_cell())
    ind = indicators(sym, pos, cell)
    v = {k: ind[k] for k in ("PS4_fraction", "P_S_coord_hist", "bridging_S_P2S7_like",
                             "P_P_bonds_P2S6_like", "density_g_cm3", "n_atoms") if k in ind}
    v["min_pair_A"], v["min_pair_kind"] = _min_pair(sym, pos, cell)
    v["min_pair_excl_PS_A"], v["min_pair_excl_PS_kind"] = _min_pair(sym, pos, cell, skip=(("P", "S"),))
    return v


def _xyz_frames(path):
    """extxyz **온전한** 프레임 수 — 프레임마다 (원자수 + 2) 줄. 꼬리의 NUL · 빈 줄과 덜 써진 마지막 프레임은 세지 않는다
    (끊긴 · 멈춘 런의 정상 모양 — ⭐ DO 전 리뷰: 전에는 None → invalid 로 첫 시드 닫힘까지 꺼졌다). 꼬리가 아닌 자리에서 머리 (원자수) 가
    깨지거나 원자수가 바뀌면 None (세지 못함 ≠ 0)."""
    lines = pathlib.Path(path).read_bytes().decode("utf-8", errors="replace").split("\n")
    last = max((i for i, ln in enumerate(lines) if not _junk(ln)), default=-1)
    i, n, nat0 = 0, 0, None
    while i <= last:
        try:
            nat = int(lines[i].strip())
        except ValueError:
            nat = None
        if nat is None or nat <= 0 or (nat0 is not None and nat != nat0):
            if nat0 is not None and last - i + 1 < nat0 + 2:   # 꼬리에서 머리째 덜 써짐 — 세지 않는다
                return n
            return None
        if i + nat + 1 > last:                               # 덜 써진 마지막 프레임 — 세지 않는다
            return n
        nat0, n, i = nat, n + 1, i + nat + 2
    return n


def seed_gate(run, write_raw=True, log=print):
    """시드 게이트의 **입력값**을 원시(traj 마지막 프레임)와 relax 본(final.xyz) 양쪽에서 찍는다.

    ⛔ 이 함수가 못 하는 것
      · 판정하지 않는다 — 어느 판으로 잴지, 문턱이 무엇인지는 카드·사람이 정한다.
      · 원시가 없으면(traj.xyz 없음) **final.xyz 로 대신하지 않는다** — 원시 칸을 비우고 이유를 적는다.
      · 마지막 프레임이 유지 구간 끝인지는 plan.json 길이와 **프레임 수로만** 대조한다 — traj 가 잘렸으면
        경보하고 그대로 둔다 (버리지 않는다). 프레임 헤더에 t 가 없어서 시각을 직접 읽지는 못한다.
      · `md_init_raw.xyz` 가 이미 있고 다르면 **덮어쓰지 않고 멈춘다** — 그 파일로 MD 가 이미 돌았을 수 있다.
    """
    import hashlib
    from ase import Atoms
    from ase.io import read, write
    run = pathlib.Path(run)
    res = {"run": str(run), "raw": None, "relaxed": None, "raw_vs_relaxed": None, "warnings": [],
           "⛔": "판정 아님 — 게이트를 어느 판으로 잴지는 카드·사람 몫 (이 도구의 final.xyz 는 relax 본이다)"}
    plan = loads_strict((run / "plan.json").read_text(encoding="utf-8")) if (run / "plan.json").exists() else {}
    fr = (plan.get("게이트_입력") or {}).get("final_relax")
    res["final_xyz_is"] = ("relax 본 (plan.json 게이트_입력.final_relax: "
                           + ", ".join(f"{k}={fr[k]}" for k in ("kind", "fmax_eV_A", "cell") if k in fr) + ")"
                           if fr else "relax 본 (plan.json 에 기록 없음 — 2026-09-12 이전 런 · 코드상 FIRE 뒤에 쓴다)")
    raw_at = None
    traj = run / "traj.xyz"
    if traj.exists():
        n_fr = _xyz_frames(traj)
        raw_at = read(str(traj), index=-1)
        save_ps = plan.get("save_ps")
        res["raw"] = {"source": "traj.xyz", "frame": (n_fr - 1) if n_fr else None,
                      "t_ps": (n_fr - 1) * float(save_ps) if (n_fr and save_ps) else None, **_gate_view(raw_at)}
        if n_fr and save_ps and all(k in plan for k in ("melt_ps", "quench_ps", "hold_ps")):
            want = int(round((plan["melt_ps"] + plan["quench_ps"] + plan["hold_ps"]) / float(save_ps))) + 1
            res["raw"]["frames_expected"] = want
            if n_fr < want:
                res["warnings"].append(f"traj 가 잘렸다 ({n_fr}/{want} 프레임) — 마지막 프레임이 유지 구간 끝이 아니다")
        elif not n_fr:
            res["warnings"].append("traj 프레임 수를 못 셌다 (줄 수가 원자수+2 의 배수가 아니다) — 시각 미상")
    else:
        res["raw_why"] = "traj.xyz 없음 — 원시를 못 구했다 (final.xyz 로 대신하지 않는다)"
    rel_at = None
    if (run / "final.xyz").exists():
        rel_at = read(str(run / "final.xyz"))
        res["relaxed"] = {"source": "final.xyz", **_gate_view(rel_at)}
    else:
        res["relaxed_why"] = "final.xyz 없음"
    if raw_at is not None and rel_at is not None:
        if raw_at.get_chemical_symbols() == rel_at.get_chemical_symbols():
            cell = np.asarray(raw_at.get_cell())
            d = (rel_at.get_positions() - raw_at.get_positions()) @ np.linalg.inv(cell)
            d = np.linalg.norm((d - np.round(d)) @ cell, axis=1)
            res["raw_vs_relaxed"] = {"disp_max_A": float(d.max()), "disp_rms_A": float(np.sqrt((d ** 2).mean())),
                                     "cell_max_abs_diff_A": float(np.abs(cell - np.asarray(rel_at.get_cell())).max())}
            if d.max() < 1e-6:
                res["warnings"].append("final.xyz 가 원시와 같다 — relax 가 안 됐거나 다른 도구가 쓴 파일이다")
        else:
            res["raw_vs_relaxed_why"] = "원자 수·순서가 달라 변위를 못 쟀다"
            res["warnings"].append(res["raw_vs_relaxed_why"])
    if raw_at is not None and write_raw:
        clean = Atoms(symbols=raw_at.get_chemical_symbols(), positions=raw_at.get_positions(),
                      cell=raw_at.get_cell(), pbc=True)
        clean.wrap()
        clean.info = {"source": "traj.xyz", "frame": res["raw"]["frame"], "t_ps": res["raw"]["t_ps"],
                      "raw": True, "wrapped": True, "made_by": "melt_quench_uma.py --seed_gate"}
        out = run / SEED_GATE_RAW
        if out.exists():
            old = read(str(out))
            same = (old.get_chemical_symbols() == clean.get_chemical_symbols()
                    and np.abs(np.asarray(old.get_cell()) - np.asarray(clean.get_cell())).max() < 1e-8)
            if same:
                dd = (old.get_positions() - clean.get_positions()) @ np.linalg.inv(np.asarray(clean.get_cell()))
                same = np.linalg.norm((dd - np.round(dd)) @ np.asarray(clean.get_cell()), axis=1).max() < 1e-6
            if not same:
                raise SystemExit(f"⛔ {out} 이 이미 있고 지금 뽑은 원시와 다르다 — 덮어쓰지 않는다 "
                                 "(그 파일로 MD 가 이미 돌았을 수 있다. 사람이 확인한다)")
            status = "이미 있음 · 같음"
        else:
            tmp_ = out.with_name(out.name + ".tmp")          # ⭐ 회신 DQ P1-1 — 임시 → 교체 (쓰다 끊긴 반쪽 파생 파일이 다음 판정에 '불일치' 로 남지 않게)
            with open(tmp_, "w", encoding="utf-8") as fh_:
                write(fh_, clean, format="extxyz")
                _fsync_handle(fh_)
            os.replace(tmp_, out)
            _fsync_dir(run)
            status = "썼다"
        res["md_init_raw"] = {"path": str(out), "status": status,
                              "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}

    def _row(tag, v):
        return (f"  {tag:<12s} {v['PS4_fraction']:.4f}  {v['bridging_S_P2S7_like']:>3d}  {v['P_P_bonds_P2S6_like']:>3d}"
                f"   {v['min_pair_A']:.3f} ({v['min_pair_kind']:<5s})  {v['min_pair_excl_PS_A']:.3f} "
                f"({v['min_pair_excl_PS_kind']:<5s})  {v['density_g_cm3']:.4f}")
    log(f"[{run.parent.name}/{run.name}] final.xyz = {res['final_xyz_is']}")
    log("               PS4   다리S  P–P   최단 (쌍)        최단·P–S 제외     ρ g/cm³")
    if res["raw"]:
        t = res["raw"]["t_ps"]
        log(_row(f"원시 t={t:.0f}" if t is not None else "원시 t=?", res["raw"]))
    else:
        log(f"  원시         —  ({res['raw_why']})")
    log(_row("relax", res["relaxed"]) if res["relaxed"] else f"  relax        —  ({res['relaxed_why']})")
    if res["raw_vs_relaxed"]:
        rv = res["raw_vs_relaxed"]
        log(f"  원시↔relax 변위 max {rv['disp_max_A']:.3f} · rms {rv['disp_rms_A']:.3f} Å · "
            f"셀 차 {rv['cell_max_abs_diff_A']:.1e} Å")
    if res.get("md_init_raw"):
        log(f"  → {SEED_GATE_RAW} {res['md_init_raw']['status']} (sha256 {res['md_init_raw']['sha256'][:16]})")
    for w in res["warnings"]:
        log(f"  ⚠ {w}")
    return res


# ───────────────────────── --gb2: G-B2 겹침 (소셀 ↔ 400 원자) ─────────────────────────
#: 판정량은 카드 §4 G-B2 가 정한다 — 도구가 쌍을 고르지 않는다.
GB2_CARD = "db/properties/lpscl_smallcell_uma_qe_force_estimand_2026_09_16.json"
GB2_PAIRS = (("P", "S"), ("Li", "S"), ("Li", "Cl"), ("S", "S"))
GR_FLOOR = 1.0          # 첫 봉우리 탐색 바닥 — g > 1 (무상관 밀도 위). 잡음 스파이크 배제용.

#: 문턱 산문에서 숫자를 캐는 패턴. **사본을 만들지 않는다** (아래 docstring).
GB2_PATS = {
    "gr_first_peak_A": r"첫 봉우리 위치가\s*\*{0,2}([0-9.]+)\s*Å\s*이내",
    "coord_mean":      r"배위수 평균이\s*\*{0,2}([0-9.]+)\s*이내",
    "ps4_pp":          r"PS₄ 보존율 차이가\s*\*{0,2}([0-9.]+)\s*%p\s*이내",
    "r_window_A":      r"r\s*≤\s*\*{0,2}([0-9.]+)\s*Å",
}


def read_gb2_thresholds(card=GB2_CARD):
    """G-B2 문턱 넷을 **봉인된 산문에서 직접** 판다.

    왜 옮겨 적지 않나: 카드의 문턱은 산문 한 줄이다. 기계용으로 전사하면 **두 벌**이 되고
    둘이 갈라진다 — 원장이 이기는데 도구는 사본을 본다. 그래서 사본을 만들지 않고 원문을 판다.
    넷 중 하나라도 못 찾으면 **죽는다**: 기본값을 지어내지 않는다.
    """
    q = pathlib.Path(card)
    if not q.exists():
        q = pathlib.Path(__file__).resolve().parents[2] / card
    d = json.loads(q.read_text(encoding="utf-8"))
    try:
        prose = d["4_검증_게이트_결과_보기_전에_정한다"]["G-B2_겹침_🔴_이_카드의_핵심"]["문턱"]
        why_r = d["4_검증_게이트_결과_보기_전에_정한다"]["G-B2_겹침_🔴_이_카드의_핵심"]["왜_r_≤_5_Å"]
    except (KeyError, TypeError):
        raise KeyError(f"{q}: G-B2 `문턱` 절이 없다 — 도구가 문턱을 지어내지 않는다")
    src = f"{prose}\n{why_r}"
    th = {}
    for k, pat in GB2_PATS.items():
        m = re.search(pat, src)
        if not m:
            raise ValueError(f"⛔ {q}: G-B2 문턱 '{k}' 를 산문에서 못 찾았다 — "
                             f"카드 문구가 바뀌었으면 **도구를 고치고 시험을 다시 친다**. "
                             f"기본값으로 넘어가지 않는다.\n  판 문장: {src[:200]}")
        th[k] = float(m.group(1))
    return th, str(q)


def first_peak_A(r, g, rmax, floor=GR_FLOOR):
    """r ≤ rmax 안에서 **첫 국소최대**의 위치 [Å]. 최대봉우리 위치도 같이 준다.

    ⛔ '첫 봉우리' 와 '최대 봉우리' 가 다르면 그 사실을 **올린다** — 조용히 하나를 고르지 않는다.
       (이 계의 P–S·Li–S 는 보통 같지만, S–S 는 다를 수 있다.)
    ⛔ 봉우리가 아예 없으면 None — 0.0 으로 그리지 않는다."""
    r = np.asarray(r, float); g = np.asarray(g, float)
    m = r <= rmax
    r, g = r[m], g[m]
    if len(r) < 3 or not np.isfinite(g).any():
        return None
    g = np.nan_to_num(g, nan=0.0, posinf=0.0, neginf=0.0)
    gi = int(np.argmax(g))
    if g[gi] < floor:
        return None                      # 전부 무상관 — 봉우리가 **없다** ("못 찾음" 과 구분)
    fi = None
    for i in range(1, len(g) - 1):
        if g[i] >= floor and g[i] >= g[i - 1] and g[i] > g[i + 1]:
            fi = i
            break
    fallback = fi is None
    if fallback:
        fi = gi                          # 국소최대가 없다(단조 상승) → 최대점을 쓰고 **표시한다**
    return {"first_A": float(r[fi]), "global_A": float(r[gi]),
            "g_first": float(g[fi]), "g_global": float(g[gi]),
            "first_is_global": bool(fi == gi), "no_local_max": bool(fallback)}


def _coord_mean(hist):
    """배위수 히스토그램 {배위수: 개수} → 평균. 비면 None (0.0 으로 그리지 않는다)."""
    if not hist:
        return None
    n = sum(hist.values())
    return (sum(int(k) * v for k, v in hist.items()) / n) if n else None


def _gb2_frames(run, want, log=print):
    """봉인된 t_ps 프레임만 뽑는다. 색인 대응은 frame_index_map 이 검증한다."""
    run = pathlib.Path(run)
    idx, n_traj = frame_index_map(run / "traj.xyz", run / "thermo.csv")
    missing = [w for w in want if w not in idx]
    if missing:
        raise ValueError(f"⛔ {run}: 봉인된 프레임 중 traj 에 없는 것 {missing} — "
                         f"다른 프레임으로 **대체하지 않는다** (카드 §6 무효 조건)")
    from ase.io import iread
    wanted = {idx[w]: w for w in want}
    out = {}
    for i, at in enumerate(iread(str(run / "traj.xyz"), index=":", format="extxyz")):
        if i in wanted:
            out[wanted[i]] = (list(at.get_chemical_symbols()),
                              np.asarray(at.get_positions(), float),
                              np.asarray(at.get_cell(), float))
        if len(out) == len(want):
            break
    log(f"  {run.name}: traj {n_traj} 프레임 → 봉인 {len(out)} 프레임 회수")
    return out


# ═══ NEB 끝점 게이트 (카드 §0b-②-4) ══════════════════════════════════════
NEB_CARD = "db/properties/lpscl_smallcell_neb_estimand_2026_09_18.json"
NEB_PATS = {
    "gate_A_li_min_A":  r"두 위치 차\(MIC\)\s*≥\s*\*{0,2}([0-9.]+)\s*Å",
    "gate_B_rmsd_max_A": r"RMSD\(두 끝점 사이, MIC\)\s*≤\s*\*{0,2}([0-9.]+)\s*Å",
}


def read_neb_gate_thresholds(card=NEB_CARD):
    """게이트 A/B 문턱을 **봉인된 산문에서 직접** 판다 (read_gb2_thresholds 와 같은 규약).

    사본을 만들지 않는다 — 두 벌이 되면 갈라지고, 원장이 이기는데 도구는 사본을 본다.
    둘 중 하나라도 못 찾으면 **죽는다**: 기본값을 지어내지 않는다.
    """
    q = pathlib.Path(card)
    if not q.exists():
        q = pathlib.Path(__file__).resolve().parents[2] / card
    d = json.loads(q.read_text(encoding="utf-8"))
    try:
        g = d["0b_경로선택·집계_규칙_제안_2026_09_18"]["②_경로_선택_규칙"][
            "4_★_끝점_게이트_두_개_다_통과해야_후보다"]
        src = g["게이트_A_서로_다른_최소"] + "\n" + g["게이트_B_골격이_안_바뀜"]
    except (KeyError, TypeError):
        raise KeyError(f"{q}: §0b-②-4 끝점 게이트 절이 없다 — 도구가 문턱을 지어내지 않는다")
    th = {}
    for k, pat in NEB_PATS.items():
        m = re.search(pat, src)
        if not m:
            raise ValueError(f"⛔ {q}: 게이트 문턱 '{k}' 를 산문에서 못 찾았다 — "
                             f"카드 문구가 바뀌었으면 **도구를 고치고 시험을 다시 친다**.")
        th[k] = float(m.group(1))
    return th


def mic_dist(a, b, cell):
    """두 점 사이 최소상 거리 [Å]."""
    f = (np.asarray(b) - np.asarray(a)) @ np.linalg.inv(cell)
    f -= np.round(f)
    return float(np.linalg.norm(f @ cell))


def non_li_rmsd(at0, at1):
    """비-Li 원자의 MIC RMSD [Å]. 골격이 재배열했는지 본다.

    ⛔ 못 하는 것: 전체 병진을 빼지 않는다. 셀 고정 이완이라 병진 자유도가 없다
      (있었다면 이 값이 병진으로 부풀었을 것이고, 그건 다른 시험이 필요하다).
    """
    sym = np.array(at0.get_chemical_symbols())
    m = sym != "Li"
    cell = np.array(at0.get_cell())
    p0, p1 = at0.get_positions()[m], at1.get_positions()[m]
    d = np.array([mic_dist(x, y, cell) for x, y in zip(p0, p1)])
    return float(np.sqrt((d ** 2).mean())), int(m.sum()), float(d.max())


def endpoint_gate(events_dir, out_json=None, card=NEB_CARD, device="cuda",
                  turbo=False, fmax=None, steps=2000, log=print):
    """§0b-②-4 끝점 게이트 — **UMA 탐침**.

    ⛔ 이 함수가 하지 않는 것
      · 비준된 게이트를 **집행하지 않는다**. §0b 는 이완을 QE(G1 §3)로 적었다.
        여기 결과는 `gate_engine: "UMA(탐침)"` 로 표시되고, 판정도 `provisional_*` 이다.
      · 장벽을 계산하지 않는다.
      · 사건을 고르지 않는다 — events.json 에 있는 것을 전부 본다.
    """
    from ase.io import read as ase_read
    from ase.optimize import FIRE
    ev_dir = pathlib.Path(events_dir)
    meta = json.loads((ev_dir / "events.json").read_text(encoding="utf-8"))
    th = read_neb_gate_thresholds(card)
    # 이완 설정은 이 궤적을 만든 것과 **같은 것**을 쓴다 (새 눈금을 만들지 않는다)
    fm = float(FINAL_RELAX["fmax_eV_A"]) if fmax is None else float(fmax)
    log(f"[endpoint_gate] 사건 {len(meta['events'])} 건 · 문턱 A ≥ {th['gate_A_li_min_A']} Å · "
        f"B ≤ {th['gate_B_rmsd_max_A']} Å · FIRE fmax {fm} (셀 고정, FINAL_RELAX 승계)")
    calc = make_calc(turbo=turbo, device=device)
    rows, n_a, n_b = [], 0, 0
    for e in meta["events"]:
        tag, ai = e["tag"], int(e["atom_index"])
        got = {}
        for side in ("i", "f"):
            at = ase_read(ev_dir / f"{tag}_{side}.xyz")
            at.calc = calc
            opt = FIRE(at, logfile=None)
            opt.run(fmax=fm, steps=steps)
            #: ⭐ 이완된 구조와 **에너지**를 남긴다 (2026-09-18).
            #   전에는 판정만 하고 버렸는데, ⓑ 카드 §2 가 E_i·E_f 를 요구하고
            #   NEB 는 **이완된** 끝점에서 출발해야 한다. 다시 이완하면 같은 값이
            #   나오겠지만, 그건 '같을 것이다' 라는 가정이고 파일이 증거다.
            e_tot = float(at.get_potential_energy())
            rel_dir = ev_dir / "relaxed"; rel_dir.mkdir(exist_ok=True)
            at.write(str(rel_dir / f"{tag}_{side}_relaxed.xyz"))
            got[side] = (at, opt.get_number_of_steps(), bool(opt.converged()), e_tot)
        (a0, s0, c0, E_i), (a1, s1, c1, E_f) = got["i"], got["f"]
        cell = np.array(a0.get_cell())
        dLi = mic_dist(a0.get_positions()[ai], a1.get_positions()[ai], cell)
        rmsd, n_fw, dmax = non_li_rmsd(a0, a1)
        okA, okB = dLi >= th["gate_A_li_min_A"], rmsd <= th["gate_B_rmsd_max_A"]
        n_a += okA; n_b += okB
        why = [] if (okA and okB) else (
            (["A: 이완 후 같은 최소로 모였다"] if not okA else []) +
            (["B: 골격이 재배열했다 — 같은 계가 아니다"] if not okB else []))
        rows.append({"tag": tag, "atom_index": ai, "disp_md_A": e["disp_A"],
                     #: ⓑ 카드 §2 의 원시량. ⛔ 장벽이 아니다 — 끝점 에너지다.
                     "E_i_eV": round(E_i, 6), "E_f_eV": round(E_f, 6),
                     "dE_f_minus_i_eV": round(E_f - E_i, 6),
                     "relaxed_xyz": [f"relaxed/{tag}_i_relaxed.xyz",
                                     f"relaxed/{tag}_f_relaxed.xyz"],
                     "li_sep_after_relax_A": round(dLi, 4),
                     "non_li_rmsd_A": round(rmsd, 4), "non_li_max_A": round(dmax, 4),
                     "n_framework_atoms": n_fw,
                     "gate_A_pass": bool(okA), "gate_B_pass": bool(okB),
                     "survives": bool(okA and okB), "rejected_because": why,
                     "relax_steps": [s0, s1], "relax_converged": [c0, c1]})
        log(f"  {tag:14s} MD {e['disp_A']:.2f} Å → 이완 후 Li {dLi:.2f} Å "
            f"({'A✓' if okA else 'A✗'}) · 골격 RMSD {rmsd:.3f} Å "
            f"({'B✓' if okB else 'B✗'}) · {'생존' if okA and okB else '기각'}")
    surv = [r for r in rows if r["survives"]]
    res = {
        "date": time.strftime("%Y-%m-%d"), "kind": "endpoint_gate_probe",
        "⛔_gate_engine": "UMA(탐침) — **비준된 §0b 는 이완을 QE(G1 §3)로 적었다.** "
                          "이 결과는 기각률을 먼저 알아 QE 예산을 정하기 위한 것이고, "
                          "게이트를 **집행하지 않는다**. 판정은 provisional 이다.",
        "card": card, "thresholds": th,
        "relax": {"kind": "FIRE", "fmax_eV_A": fm, "cell": "fixed",
                  "uma_mode": getattr(calc, "_mq_mode", "?"), "승계": "FINAL_RELAX"},
        "n_events": len(rows), "provisional_n_survive": len(surv),
        "provisional_reject_rate": round(1 - len(surv) / len(rows), 4) if rows else None,
        "gate_A_pass": int(n_a), "gate_B_pass": int(n_b),
        "rows": rows,
        "⇒_§0b_②_5": ("**전부 기각** — §0b-②-5 에 따라 장벽 분포를 내지 않는다. "
                       "⚠ 단 이 판정은 UMA 이완 기준이다. QE 로 확정하려면 1저자 결정이 필요하다."
                       if not surv else
                       f"생존 {len(surv)} 건 — 이들에 대해서만 QE 예산을 잡는다."),
    }
    if out_json:
        pathlib.Path(out_json).write_text(json.dumps(res, ensure_ascii=False, indent=1),
                                          encoding="utf-8")
        log(f"  → {out_json}")
    log(f"  ⇒ 생존 {len(surv)}/{len(rows)} (A 통과 {n_a} · B 통과 {n_b}) — {res['⇒_§0b_②_5']}")
    return res


def gb2_compare(run_small, run_big, card=GB2_CARD, frame_card=None, log=print):
    """G-B2 — 소셀과 400 원자의 **같은 t_ps 프레임**에서 국소환경이 겹치는가. 새 계산 0.

    판정 규칙 (결과 보기 전에 선언 · 2026-09-18)
      · 같은 t_ps 끼리 **짝지어** 재고, 10 짝의 **최댓값**으로 판정한다.
        담금질 속도가 같아 같은 t_ps 는 같은 온도다 — 융체는 융체와, 유리는 유리와 비교한다.
        (프레임을 뭉쳐 평균내면 융체와 유리가 섞여 봉우리가 뭉개진다.)
      · 평균차·풀링 g(r) 도 **같이 찍지만 판정에 쓰지 않는다** — 최댓값 이탈이 통계잡음인지
        사람이 보라고 내는 정보다.

    ⛔ 이 도구가 **못 하는 것**
      · 단일 프레임 g(r) 의 **통계잡음을 문턱과 분리하지 못한다.** 120 원자에서 Li–Cl 은
        48×12 쌍뿐이라 첫 봉우리가 dr 한두 칸 흔들릴 수 있다. 그래서 풀링 값을 같이 낸다.
      · 힘이 같다고 말하지 않는다 — 구조가 겹쳐도 힘이 같다는 보증은 없다 (카드 §4).
      · 전이를 승인하지 않는다. 통과는 **전이의 근거**이고, 판단은 사람이 한다.
      · 밀도를 판정하지 않는다 — 카드가 "밀도는 문턱이 아니다" 로 봉인했다. **보고만** 한다.
    """
    th, card_path = read_gb2_thresholds(card)
    want, fcard = read_frame_card(frame_card or
                                  "db/properties/li2s_layer1_g2_mode_stress_prereg_2026_09_14.json")
    log(f"문턱 카드: {card_path}")
    log(f"  첫봉우리 ≤ {th['gr_first_peak_A']} Å · 배위수평균 ≤ {th['coord_mean']} · "
        f"PS₄ ≤ {th['ps4_pp']} %p · 창 r ≤ {th['r_window_A']} Å")
    log(f"프레임 카드: {fcard} — 봉인 {len(want)} 점 (도구가 고르지 않는다)")
    S = _gb2_frames(run_small, want, log)
    B = _gb2_frames(run_big, want, log)

    rows, acc = [], {}
    for w in want:
        ss, sp, sc = S[w]; bs, bp, bc = B[w]
        i_s, i_b = indicators(ss, sp, sc), indicators(bs, bp, bc)
        g_s = partial_gr(ss, sp, sc, pairs=GB2_PAIRS)
        g_b = partial_gr(bs, bp, bc, pairs=GB2_PAIRS)
        row = {"t_ps": w, "n_small": i_s["n_atoms"], "n_big": i_b["n_atoms"],
               "rho_small": i_s["density_g_cm3"], "rho_big": i_b["density_g_cm3"]}
        # ① 부분 g(r) 첫 봉우리
        row["peaks"] = {}
        for a, b in GB2_PAIRS:
            key = f"g_{a}{b}"
            if key not in g_s or key not in g_b:
                row["peaks"][f"{a}{b}"] = {"d_A": None, "왜": "그 쌍이 한쪽에 없다"}
                continue
            ps = first_peak_A(g_s["r_A"], g_s[key], th["r_window_A"])
            pb = first_peak_A(g_b["r_A"], g_b[key], th["r_window_A"])
            if ps is None or pb is None:
                row["peaks"][f"{a}{b}"] = {"d_A": None, "왜": "봉우리 없음 (무상관)"}
                continue
            d = abs(ps["first_A"] - pb["first_A"])
            row["peaks"][f"{a}{b}"] = {
                "small_A": ps["first_A"], "big_A": pb["first_A"], "d_A": d,
                "⚠_첫봉우리≠최대봉우리": (not ps["first_is_global"]) or (not pb["first_is_global"]),
                "⚠_국소최대없음": ps["no_local_max"] or pb["no_local_max"]}
            acc.setdefault(f"peak_{a}{b}", []).append(d)
        # ② 배위수 평균 (Cl–Li · S–Li)
        row["coord"] = {}
        for name, hk in (("Cl_Li", "Cl_Li_coord_hist"), ("S_Li", "S_Li_coord_hist")):
            ms, mb = _coord_mean(i_s.get(hk)), _coord_mean(i_b.get(hk))
            if ms is None or mb is None:
                row["coord"][name] = {"d": None, "왜": "히스토그램이 비었다"}
                continue
            row["coord"][name] = {"small": ms, "big": mb, "d": abs(ms - mb)}
            acc.setdefault(f"coord_{name}", []).append(abs(ms - mb))
        # ③ PS₄ 보존율
        fs, fb = i_s.get("PS4_fraction"), i_b.get("PS4_fraction")
        if fs is None or fb is None:
            row["PS4"] = {"d_pp": None, "왜": "P 또는 S 가 없다"}
        else:
            row["PS4"] = {"small": fs, "big": fb, "d_pp": abs(fs - fb) * 100.0}
            acc.setdefault("PS4_pp", []).append(abs(fs - fb) * 100.0)
        rows.append(row)
        log(f"  t={w:7.1f} ps  PS₄ Δ{row['PS4'].get('d_pp', float('nan')):5.1f} %p  " +
            "  ".join(f"{k} Δ{(v['d_A'] if v.get('d_A') is not None else float('nan')):.3f}"
                      for k, v in row["peaks"].items()))

    def _worst(keys, lim):
        bad = []
        for k in keys:
            v = acc.get(k)
            if not v:
                bad.append((k, None, "잰 프레임이 없다"))
                continue
            mx = max(v)
            if mx > lim:
                bad.append((k, mx, f"> {lim}"))
        return bad

    peak_keys = [f"peak_{a}{b}" for a, b in GB2_PAIRS]
    fails = (_worst(peak_keys, th["gr_first_peak_A"])
             + _worst(["coord_Cl_Li", "coord_S_Li"], th["coord_mean"])
             + _worst(["PS4_pp"], th["ps4_pp"]))
    #: ⛔ 잰 프레임이 아예 없는 항목은 **통과가 아니다** — 미판정이다.
    unmeasured = [k for k, mx, _ in fails if mx is None]
    verdict = ("미판정" if unmeasured else ("탈락" if fails else "통과"))
    res = {"card": card_path, "frame_card": fcard, "thresholds": th,
           "run_small": str(run_small), "run_big": str(run_big),
           "판정_규칙": "같은 t_ps 짝의 **최댓값**으로 판정 (2026-09-18 선언 · 결과 보기 전)",
           "요약": {k: {"max": max(v), "mean": float(np.mean(v)), "n": len(v)} for k, v in acc.items()},
           "frames": rows, "판정": verdict,
           "실패항목": [{"항목": k, "max": mx, "왜": why} for k, mx, why in fails],
           "⛔_밀도는_문턱이_아니다": "카드 §4 — 국소환경을 요구하고 밀도는 보고만 한다.",
           "⛔_통과가_뜻하지_않는_것": "구조가 겹쳐도 힘이 같다는 보증은 아니다. 전이는 G-B3 통과와 "
                                    "함께, 그리고 **통과 방향으로만** 흐른다 (카드 §5-b)."}
    log(f"\n  판정: **{verdict}**")
    for k, mx, why in fails:
        log(f"    ⛔ {k}: {mx if mx is not None else '미측정'} {why}")
    if verdict == "통과":
        log("  ⛔ 통과는 **전이의 근거**이지 승인이 아니다 — 판단은 사람이 한다 (카드 §5-b).")
    return res


# ───────────────────────── selftest ─────────────────────────
# ───────────────────────── 모델 검증 카드: 0 K 등방 경로 (UMA) ─────────────────────────
MC_CARD = "db/properties/lpscl_smallcell_glass_model_check_estimand_2026_10_19.json"


def read_mc_values(card=MC_CARD):
    """모델 검증 카드의 `기계_판독_값` — 키가 없으면 KeyError 로 죽는다 (숫자를 지어내지 않는다)."""
    q = pathlib.Path(card)
    if not q.exists():                       # repo 루트 상대 (도구가 어디서 불리든 같은 카드)
        q = pathlib.Path(__file__).resolve().parents[2] / card
    return json.loads(q.read_text(encoding="utf-8"))["기계_판독_값"], q


def eos_label(path):
    """…/<A|B>/seed<N>/<파일> → 'A_s<N>' — 경로에서 계 · 시드를 읽는다 (못 읽으면 죽는다 · 추측 안 한다)."""
    p = pathlib.Path(path)
    m = re.fullmatch(r"seed(\d+)", p.parent.name)
    if not m or p.parent.parent.name not in ("A", "B"):
        raise SystemExit(f"⛔ {path}: '…/<A|B>/seed<N>/<파일>' 꼴이 아니다 — 라벨을 추측하지 않는다")
    return f"{p.parent.parent.name}_s{int(m.group(1))}"


def eos_topology(atoms, rPS, rSS):
    """(P–S ≤ rPS 결합 수, S–S ≤ rSS 쌍 수) — 카드 토폴로지 규칙의 입력 (최소상 · 직교 셀)."""
    sym = np.array(atoms.get_chemical_symbols()); pos = atoms.get_positions(); cell = atoms.cell.array
    P, S = pos[sym == "P"], pos[sym == "S"]
    nPS = int((mic_dists(P, S, cell) <= rPS).sum()) if len(P) and len(S) else 0
    nSS = 0
    if len(S) > 1:
        D = mic_dists(S, S, cell); np.fill_diagonal(D, np.inf); nSS = int((D <= rSS).sum() // 2)
    return nPS, nSS


def eos_path(structs, out_dir, which="main", device="cuda", card=MC_CARD, calc=None, log=print):
    """모델 검증 카드 §1b 경로 — 구조마다 등방 스케일 점 (분율 좌표 유지) 에서 UMA **default** 고정셀 FIRE 이완.

    점마다 <out>/<라벨>/x<0.85>.xyz (기하만) 와 <out>/<라벨>/uma_path.json
    (E · virial P (운동 항 없음) · σ · Fmax · 스텝 · 수렴 · P–S/S–S 수 · 기하 sha256).
    which = 'main' (path_scales) · 'ext_low' · 'ext_high' (카드 연장 점 — 판독 도구가 연장 규칙을 말할 때만).
    json 에 이미 있는 점은 건너뛴다 (재개 · 같은 입력 sha 일 때만).

    ⛔ 못 하는 것: QE · D3 · BM3 를 하지 않는다 (판독 도구 몫) · turbo 를 안 쓴다 (카드 uma_mode) ·
      셀 모양을 안 바꾼다 (등방 스케일만) · 카드 밖 격자를 받지 않는다 (결과 보고 격자를 넓히지 않는다) ·
      점마다 스케일된 원본에서 따로 시작한다 (연쇄 아님 — 카드 §1b).
    """
    import hashlib
    from ase.io import read, write
    from ase.optimize import FIRE
    v, card_path = read_mc_values(card)
    key = {"main": "path_scales", "ext_low": "path_ext_low", "ext_high": "path_ext_high"}[which]
    scales = [float(x) for x in v[key]]
    fmax, steps = float(v["relax_fmax_eV_A"]), int(v["relax_max_steps"])
    rPS, rSS = float(v["topo_PS_A"]), float(v["topo_SS_A"])
    if v["uma_mode"] != "default":
        raise SystemExit(f"⛔ 카드 uma_mode = {v['uma_mode']} — 이 경로는 default 만 안다")
    if calc is None:
        calc = make_calc(device, turbo=False)
    mode = getattr(calc, "_mq_mode", None)
    if mode != "default":
        raise SystemExit(f"⛔ 계산기 모드 {mode!r} — default 여야 한다 (카드 §1b)")
    try:
        import fairchem
        fc_ver = getattr(fairchem, "__version__", "?")
    except Exception:
        fc_ver = None
    out = pathlib.Path(out_dir)
    res = {}
    for sp in structs:
        lab = eos_label(sp)
        at0 = read(str(sp))
        d = out / lab; d.mkdir(parents=True, exist_ok=True)
        jp = d / "uma_path.json"
        src_sha = hashlib.sha256(pathlib.Path(sp).read_bytes()).hexdigest()
        if jp.exists():
            J = json.loads(jp.read_text(encoding="utf-8"))
            if J["meta"]["source_sha256"] != src_sha:
                raise SystemExit(f"⛔ {jp}: 다른 입력 구조의 경로다 (sha 다름) — 섞지 않는다")
        else:
            J = {"meta": {"label": lab, "source": str(sp), "source_sha256": src_sha,
                          "card": str(card_path), "card_sha256": hashlib.sha256(card_path.read_bytes()).hexdigest(),
                          "uma": "uma-s-1p1 · task omat", "mode": mode, "fairchem": fc_ver, "device": device,
                          "relax": {"kind": "FIRE", "cell": "fixed", "fmax_eV_A": fmax, "max_steps": steps},
                          "V_final_A3": float(at0.get_volume()),
                          "⛔": "P_virial 은 운동 항 없음 (0 K 정적) · 기하는 UMA 이완본 — QE 단일점의 입력"},
                 "points": []}
        done = {round(p["x"], 4) for p in J["points"]}
        for x in scales:
            if round(x, 4) in done:
                log(f"  {lab} x={x:.2f} 이미 있음 — 건너뜀"); continue
            at = at0.copy()
            at.set_cell(at0.cell.array * x ** (1.0 / 3.0), scale_atoms=True)
            at.calc = calc
            opt = FIRE(at, logfile=None)
            t0 = time.time()
            conv = opt.run(fmax=fmax, steps=steps)
            F = at.get_forces(); fm = float(np.linalg.norm(F, axis=1).max())
            conv = bool(conv) if isinstance(conv, (bool, np.bool_)) else (fm <= fmax)
            E = float(at.get_potential_energy())
            sig = np.asarray(at.get_stress(voigt=False)) * EV_A3_TO_GPA
            nPS, nSS = eos_topology(at, rPS, rSS)
            g = at.copy(); g.calc = None
            fx = d / f"x{x:.2f}.xyz"
            write(str(fx), g, format="extxyz")
            pt = {"x": x, "V_A3": float(at.get_volume()), "E_eV": E,
                  "P_virial_GPa": float(-np.trace(sig) / 3.0), "sigma_GPa": sig.tolist(),
                  "Fmax_eV_A": fm, "steps": int(opt.nsteps), "converged": conv,
                  "n_PS": nPS, "n_SS": nSS, "geom": fx.name,
                  "geom_sha256": hashlib.sha256(fx.read_bytes()).hexdigest(), "wall_s": round(time.time() - t0, 1)}
            J["points"].append(pt)
            J["points"].sort(key=lambda p: p["x"])
            jp.write_text(json.dumps(J, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            log(f"  {lab} x={x:.2f} V={pt['V_A3']:.1f} E={E:.4f} P={pt['P_virial_GPa']:+.3f} GPa "
                f"Fmax={fm:.3f} steps={pt['steps']} conv={conv} P–S={nPS} S–S={nSS} ({pt['wall_s']} s)")
        res[lab] = J
    return res


def _selftest():
    ok = bad = 0
    def chk(c, m):
        nonlocal ok, bad
        print(("  ⭕ " if c else "  ⛔ ") + m); ok += c; bad += (not c)
    # ① 무작위 셀
    for sysname, n_exp in (("A", 400), ("B", 400), ("control_li7ps6", 392)):
        sym, pos, cell = build_random_cell(sysname, seed=1)
        comp, n_fu = SYSTEMS[sysname]
        cnt = {e: sym.count(e) for e in set(sym)}
        chk(len(sym) == n_exp and all(cnt.get(k, 0) == v * n_fu for k, v in comp.items()), f"{sysname}: 원자 {n_exp} · 조성 정확")
        D = mic_dists(pos, pos, cell); np.fill_diagonal(D, np.inf)
        P = np.where(np.asarray(sym) == "P")[0]
        ps = np.array([sorted(D[i])[:4] for i in P])
        chk(abs(ps - PS_BOND).max() < 1e-6, f"{sysname}: 모든 P 의 최근접 4 S 가 {PS_BOND} Å (PS₄ 단위)")
        # 단위 밖 최소거리
        unit = -np.ones(len(sym), int)
        for u, i in enumerate(P): unit[i:i+5] = u
        mask = (unit[:, None] != unit[None, :]) | (unit[:, None] < 0)
        heavy = np.array([x != "Li" for x in sym])
        hh = heavy[:, None] & heavy[None, :]
        chk(D[mask & hh].min() >= MIN_DIST_ANION - 1e-9 and D[mask & ~hh].min() >= MIN_DIST - 1e-9,
            f"{sysname}: 단위 밖 최소거리 — 음이온·P 끼리 ≥ {MIN_DIST_ANION} Å · Li 쌍 ≥ {MIN_DIST} Å")
    ind = indicators(sym, pos, cell)
    chk(abs(ind["density_g_cm3"] - 1.2) < 0.02, "밀도 지표가 시작 밀도 1.2 를 재현한다")
    try:
        build_random_cell("A", seed=1, density_g_cm3=6.0, max_tries=3000); ok_d = False
    except SystemExit as e:
        ok_d = "밀도" in str(e)
    chk(ok_d, "⛔음성: 6 g/cm³ 는 못 채우고 멈춘다 (조용히 겹치게 두지 않는다)")
    try:
        build_random_cell("Z", seed=1); ok_z = False
    except SystemExit:
        ok_z = True
    chk(ok_z, "⛔음성: 카드에 없는 계 이름은 거부")
    try:
        schedule(1200, 300, None, 2.0); ok_q = False
    except SystemExit as e:
        ok_q = "quench_rate" in str(e)
    chk(ok_q, "⛔음성: 담금질 속도를 안 주면 시작하지 않는다 (G2)")
    qp, nq = schedule(1200, 300, 1e12, 2.0)
    chk(abs(qp - 900.0) < 1e-9 and nq == 450000, "10¹² K/s · 1200→300 K = 900 ps = 450000 스텝 @ 2 fs")
    # ② 지표 — 합성 구조
    symA, posA, cellA = build_random_cell("A", seed=3)
    iA = indicators(symA, posA, cellA)
    chk(iA["PS4_fraction"] == 1.0 and iA["bridging_S_P2S7_like"] == 0, "무작위 PS₄ 단위 셀: PS₄ 보존율 1.0 · 가교 0")
    first_S = next(i for i, x in enumerate(symA) if x == "S")
    symB = [x for i, x in enumerate(symA) if i != first_S]; posB = np.delete(posA, first_S, axis=0)   # S 하나를 없앤다
    chk(abs(indicators(symB, posB, cellA)["PS4_fraction"] - (1 - 1 / 40)) < 1e-9, "⛔음성: S 하나를 없애면 보존율 39/40")
    a = 5.13; n = 3; rs = []; rsym = []                                    # 암염 LiCl
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for base, el in (((0, 0, 0), "Cl"), ((0.5, 0.5, 0), "Cl"), ((0.5, 0, 0.5), "Cl"), ((0, 0.5, 0.5), "Cl"),
                                 ((0.5, 0, 0), "Li"), ((0, 0.5, 0), "Li"), ((0, 0, 0.5), "Li"), ((0.5, 0.5, 0.5), "Li")):
                    rs.append(((np.array(base) + [i, j, k]) * a).tolist()); rsym.append(el)
    iL = indicators(rsym, np.array(rs), np.eye(3) * a * n)
    chk(iL["Cl_6coord_fraction"] == 1.0 and iL["ClCl_nearest_A"]["in_window_fraction"] == 1.0
        and abs(iL["ClCl_nearest_A"]["median"] - a / math.sqrt(2)) < 1e-6, "암염 LiCl: Cl 6-배위 1.0 · Cl–Cl 3.63 Å 창 분율 1.0")
    a2 = 5.71; qs = []; qsym = []                                          # 반형석 Li₂S
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for base in ((0, 0, 0), (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5)):
                    qs.append(((np.array(base) + [i, j, k]) * a2).tolist()); qsym.append("S")
                for base in ((.25, .25, .25), (.75, .75, .75), (.75, .25, .25), (.25, .75, .75),
                             (.25, .75, .25), (.75, .25, .75), (.25, .25, .75), (.75, .75, .25)):
                    qs.append(((np.array(base) + [i, j, k]) * a2).tolist()); qsym.append("Li")
    iQ = indicators(qsym, np.array(qs), np.eye(3) * a2 * 2)
    chk(iQ["S_Li8_fraction_Li2S_like"] == 1.0, "반형석 Li₂S: S 의 Li 8-배위 분율 1.0")
    chk(iA["S_Li8_fraction_Li2S_like"] < 0.2, "무작위 A 셀은 Li₂S 국소질서가 거의 없다 (< 0.2)")
    gr = partial_gr(symA, posA, cellA)
    chk("g_PS" in gr and abs(gr["r_A"][int(np.argmax(gr["g_PS"]))] - PS_BOND) < 0.06, "g_PS 첫 봉우리가 2.05 Å")
    # ③ MD 연기 시험 — fairchem 없이 LJ 로 배선만 (n_fu 2 · 몇 스텝)
    import tempfile
    from ase import Atoms
    from ase.calculators.lj import LennardJones
    symS, posS, cellS = build_random_cell("A", seed=5, n_fu=2, density_g_cm3=0.8)
    at = Atoms(symbols=symS, positions=posS, cell=cellS, pbc=True)
    with tempfile.TemporaryDirectory() as td:
        info = run_melt_quench(at, LennardJones(sigma=2.5, epsilon=0.05, rc=6.0), td, seed=5, T_melt=600, T_final=300,
                               melt_ps=0.02, quench_rate=3e14, hold_ps=0.02, dt_fs=2.0, save_ps=0.004, pre_relax=False, log=lambda *a: None)
        n_frames = open(os.path.join(td, "traj.xyz")).read().count("Lattice=")
        chk(info["n_steps"]["quench"] == 500 and n_frames >= 5, f"LJ 연기: 담금질 500 스텝 · 궤적 {n_frames} 프레임 기록")
        chk(os.path.isfile(os.path.join(td, "final.xyz")) and os.path.isfile(os.path.join(td, "final.vasp"))
            and os.path.isfile(os.path.join(td, "thermo.csv")), "final.xyz + final.vasp + thermo.csv 생성 (xyz·POSCAR 쌍)")
        mdd = json.loads(open(os.path.join(td, MD_DONE_NAME), encoding="utf-8").read())
        pl_lj = {"melt_ps": 0.02, "quench_ps": info["quench_ps"], "hold_ps": 0.02, "dt_fs": 2.0, "save_ps": 0.004,
                 "run_id": mdd["run_id"] or "7" * 32}
        if mdd["run_id"] is None:                            # 이 연기 시험은 run_id 없이 돌렸다 — 판독 시험용으로 기록 · plan 을 같은 값으로 맞춘다
            mdd["run_id"] = pl_lj["run_id"]; open(os.path.join(td, MD_DONE_NAME), "w", encoding="utf-8").write(json.dumps(mdd))
        open(os.path.join(td, "plan.json"), "w", encoding="utf-8").write(json.dumps(pl_lj))
        st_lj_final = folder_stage(td)
        os.remove(os.path.join(td, "final.xyz"))
        st_lj_fire = folder_stage(td)
        chk(mdd["n_steps_done"] == mdd["n_steps_planned"] == planned_md_steps(pl_lj) == sum(info["n_steps"].values())
            and mdd["traj_sha256"] == _sha256_file(pathlib.Path(td) / "traj.xyz") and st_lj_final == "final" and st_lj_fire == "md_complete",
            f"회신 DK: 진짜 MD 루프가 FIRE 전에 완료 기록을 쓴다 (스텝 {mdd['n_steps_done']} = 계획 · 궤적 해시) · final.xyz 를 지우면 MD 완료 ({st_lj_final} → {st_lj_fire})")
        hdr = open(os.path.join(td, "thermo.csv")).readline().strip().split(",")
        row = open(os.path.join(td, "thermo.csv")).readlines()[1].strip().split(",")
        chk(hdr[-2:] == ["P_GPa", "P_virial_GPa"] and len(row) == len(hdr)
            and row[-1] not in ("", "nan") and row[-2] != row[-1],
            f"thermo.csv 에 총 압력과 virial 을 **둘 다** 기록하고 서로 다르다 ({row[-2]} / {row[-1]} GPa)")
    # ⭐ 회신 DL P1-2 — FIRE 진입 순간에 완료 기록이 이미 맞는지 (진짜 MD 루프 · LJ) — 기록 호출을 FIRE 뒤로 옮기면 여기서 빨개진다
    import ase.optimize as _aopt
    class _AtFire(Exception):
        pass
    _RealFIRE, seen_fire = _aopt.FIRE, []
    class _FireProbe(_RealFIRE):
        def __init__(self, atoms_, *a_, logfile=None, **k_):
            if logfile is not None and str(logfile).endswith("final_relax.log"):
                dd_ = pathlib.Path(str(logfile)).parent
                seen_fire.append((folder_stage(dd_), (dd_ / MD_DONE_NAME).is_file(), (dd_ / "final.xyz").exists()))
                raise _AtFire()
            super().__init__(atoms_, *a_, logfile=logfile, **k_)
    with tempfile.TemporaryDirectory() as tdF:
        qps_, _ = schedule(600, 300, 3e14, 2.0)
        RIDP = "4" * 32
        open(os.path.join(tdF, "plan.json"), "w", encoding="utf-8").write(json.dumps(
            {"melt_ps": 0.02, "quench_ps": qps_, "hold_ps": 0.02, "dt_fs": 2.0, "save_ps": 0.004, "run_id": RIDP}))
        at2 = Atoms(symbols=symS, positions=posS, cell=cellS, pbc=True)
        _aopt.FIRE, stopped = _FireProbe, False
        try:
            run_melt_quench(at2, LennardJones(sigma=2.5, epsilon=0.05, rc=6.0), tdF, seed=5, T_melt=600, T_final=300,
                            melt_ps=0.02, quench_rate=3e14, hold_ps=0.02, dt_fs=2.0, save_ps=0.004, pre_relax=False,
                            log=lambda *a: None, run_id=RIDP)
        except _AtFire:
            stopped = True
        finally:
            _aopt.FIRE = _RealFIRE
        chk(stopped and seen_fire == [("md_complete", True, False)],
            f"⛔음성 DL P1-2: FIRE 진입 순간 이미 MD 완료 기록이 맞다 (folder_stage = md_complete · final 없음) — "
            f"기록 호출을 FIRE 뒤로 옮기면 빨개진다 ({seen_fire})")
    # ③b li2s-2 --fix_density — NVT 고정 밀도 경로 (LJ 배선) · 옵션이 없으면 옛 plan 과 같은 키
    #     (회신 DF Q-DF-8 뒤: 압축은 melt/2 전에 끝나야 한다 → melt 0.8 · 압축 0.3 ps)
    symF, posF, cellF = build_random_cell("A", seed=5, n_fu=2, density_g_cm3=0.8)
    with tempfile.TemporaryDirectory() as td:
        atF = Atoms(symbols=symF, positions=posF, cell=cellF, pbc=True)
        infoF = run_melt_quench(atF, LennardJones(sigma=2.5, epsilon=0.05, rc=6.0), td, seed=5, T_melt=600, T_final=300,
                                melt_ps=0.8, quench_rate=3e14, hold_ps=0.02, dt_fs=2.0, save_ps=0.004, pre_relax=False,
                                fix_density=1.2, compress_ps=0.3, log=lambda *a: None)
        thF = read_thermo(os.path.join(td, "thermo.csv"))
        rhoF, tF = thF["density_g_cm3"], thF["t_ps"]
        chk(abs(density_g_cm3(atF) / 1.2 - 1.0) < 1e-9 and abs(infoF["fix_density"]["final_g_cm3"] / 1.2 - 1.0) < 1e-9
            and abs(infoF["fix_density"]["start_g_cm3"] - 0.8) < 0.02,
            f"고정 밀도: 0.8 에서 시작해 담금질 · 완화 끝 밀도가 1.2 (1e-9) — 끝 {infoF['fix_density']['final_g_cm3']:.6f}")
        ramp, after = rhoF[tF < 0.3 - 1e-9], rhoF[tF >= 0.3 - 1e-9]
        chk(ramp.size >= 3 and rhoF[0] < 1.15 and np.all(np.diff(ramp) >= -1e-9) and len(set(np.round(ramp, 4))) >= 3,
            f"고정 밀도: 압축 구간 밀도가 단계적으로 오른다 ({rhoF[0]:.3f} → … · 단계 {len(set(np.round(ramp, 4)))})")
        chk(after.size > 50 and np.all(np.abs(after - 1.2) < 1e-3), "고정 밀도: 압축 뒤 (melt 나머지 · 담금질 · 유지) 밀도가 1.2 에 머문다")
        planF = build_plan("A", 5, list(symF), 0.8, 600, 300, 0.8, 3e14, 1.0, 0.02, 2.0, 0.004, fix_density=1.2, compress_ps=0.3)
        gF = planF["게이트_입력"]
        chk(gF["ensemble"] == "NVT" and gF["barostat"] is None and gF["target_density_g_cm3"] == 1.2
            and "target_pressure_GPa" not in gF and planF["fix_density_g_cm3"] == 1.2,
            "고정 밀도 plan: 게이트_입력 앙상블 = NVT · 목표 밀도 1.2 · 목표 압력 키 없음")
        (pathlib.Path(td) / "plan.json").write_text(json.dumps(planF, ensure_ascii=False), encoding="utf-8")
        gcF = gate_check(td, win_ps=0.015, log=lambda *a: None)
        chk(gcF["mode"] == "NVT_fixed_density" and gcF["gate_ok"] and gcF["pressure_ok"] is None and gcF["schedule_complete"]
            and gcF["window_in_hold"] and gcF["pressure_recorded"] and math.isfinite(gcF["P_mean_GPa"]),
            "--gate_check: 고정 밀도 런 — 일정 완주 · 창이 유지 구간 안 · 압력 기록 · 밀도 = 목표 → 통과")
        tp = pathlib.Path(td) / "thermo.csv"
        orig = tp.read_text(encoding="utf-8")
        lines = orig.splitlines()
        cols = lines[-3].split(","); cols[3] = "1.2500"; lines[-3] = ",".join(cols)
        tp.write_text("\n".join(lines) + "\n", encoding="utf-8")
        chk(not gate_check(td, win_ps=0.015, log=lambda *a: None)["gate_ok"],
            "⛔음성: 유지 구간 한 줄의 밀도를 1.25 로 바꾸면 --gate_check 가 잡는다")
        # 회신 DF P1-2 반례 ① — 담금질 · 유지 없이 melt 기록만 (밀도는 맞음)
        keep = [ln for ln in orig.splitlines()[1:] if float(ln.split(",")[0]) <= 0.79]
        tp.write_text(orig.splitlines()[0] + "\n" + "\n".join(keep) + "\n", encoding="utf-8")
        gm = gate_check(td, win_ps=0.015, log=lambda *a: None)
        chk(not gm["gate_ok"] and not gm["schedule_complete"],
            "⛔음성 DF: melt 기록만 있으면 (일정 미완 · 창이 유지 구간 밖) 밀도가 맞아도 통과 못 한다")
        # 회신 DF P1-2 반례 ② — 압력 열을 NaN 으로
        rows = [orig.splitlines()[0]] + [",".join(c[:-2] + ["nan", "nan"]) for c in (ln.split(",") for ln in orig.splitlines()[1:])]
        tp.write_text("\n".join(rows) + "\n", encoding="utf-8")
        gn = gate_check(td, win_ps=0.015, log=lambda *a: None)
        chk(not gn["gate_ok"] and not gn["pressure_recorded"] and gn["density_ok"],
            "⛔음성 DF: 압력이 NaN 이면 '압력 기록 없음' 으로 통과 못 한다 (압력 크기는 판정하지 않는다)")
        # 회신 DG P1-7 — virial 열을 지우면 (총압만 남음) '기록 있음' 이던 구멍
        rows = [",".join(c[:-1]) for c in (ln.split(",") for ln in orig.splitlines())]
        tp.write_text("\n".join(rows) + "\n", encoding="utf-8")
        gv = gate_check(td, win_ps=0.015, log=lambda *a: None)
        chk(not gv["gate_ok"] and not gv["pressure_recorded"] and gv["thermo_columns_ok"] is False and gv["pressure_columns"] == ["P_GPa"],
            "⛔음성 DG P1-7: thermo 에서 virial 압력 열을 지우면 '압력 기록 없음' · 열 꼴 불일치 (통과 못 한다)")
        chk(planF["게이트_입력"]["final_relax"]["⛔"].startswith("밀도는 **고정 밀도 셀**")
            and build_plan("A", 5, list(symF), 0.8, 600, 300, 0.4, 3e14, 1.0, 0.02, 2.0, 0.004)["게이트_입력"]["final_relax"] is FINAL_RELAX,
            "DG P2: NVT plan 의 final_relax 설명은 '고정 밀도 셀' · NPT plan 은 옛 설명 그대로")
        tp.write_text(orig, encoding="utf-8")
        try:
            melt_check(td, log=lambda *a: None); legacy_refused = False
        except SystemExit as e:
            legacy_refused = "--melt_window_check" in str(e)
        chk(legacy_refused, "⛔음성 DF: 고정 밀도 런에 옛 --melt_check (0 ps 누적 원점) 를 쓰면 거부하고 --melt_window_check 를 가리킨다")
    plan0 = build_plan("A", 5, list(symF), 0.8, 600, 300, 0.4, 3e14, 1.0, 0.02, 2.0, 0.004)
    chk("fix_density_g_cm3" not in plan0 and plan0["게이트_입력"]["ensemble"] == "NPT"
        and plan0["게이트_입력"]["target_pressure_GPa"] == 0.0 and plan0["게이트_입력"]["barostat"] == "Berendsen",
        "옵션이 없으면 plan 은 옛 NPT 0 GPa 그대로 (fix_density 키 없음)")
    for nm, args in (("밀도 0", (0.0, 20.0, 100.0)), ("밀도 음수", (-1.9, 20.0, 100.0)), ("압축 0 ps", (1.9, 0.0, 100.0)),
                     ("압축이 melt 보다 김", (1.9, 120.0, 100.0)), ("밀도 nan", (float("nan"), 20.0, 100.0)),
                     ("압축이 판정 창 (melt/2) 에 걸림 — DF", (1.9, 60.0, 100.0))):
        try:
            validate_fix_density(*args); refused = False
        except SystemExit:
            refused = True
        chk(refused, f"⛔음성: --fix_density 입력 거부 — {nm}")
    try:
        validate_fix_density(None, 0.0, 0.0); validate_fix_density(1.9, 50.0, 100.0); off_ok = True
    except SystemExit:
        off_ok = False
    chk(off_ok, "옵션을 안 주면 (None) 검사하지 않고 · 압축이 판정 창 시작 (50/100) 에 딱 끝나면 받는다")
    # ③c li2s-2 녹음 판정 (회신 DF P0) — 합성 궤적: 창 [50, 100] 좌표가 같고 앞 이력만 다른 둘 · 70 ps 에서 끊긴 것 · 겹침 · NaN
    from ase.io import write as _w
    VAL = {"melt_window": {"t_from_frac_of_melt": 0.5, "t_to_frac_of_melt": 1.0, "lag_fit_ps": [2.0, 25.0], "element": "P",
                           "D_threshold_cm2_s": 1e-6, "threshold_source": "selftest"},
           "fix_density_g_cm3": {"A": 1.91347, "B": 1.88},
           "schedule": {"T_melt_K": 1200.0, "T_final_K": 300.0, "melt_ps": 100.0, "quench_rate_K_s": 1e12, "hold_ps": 50.0,
                        "dt_fs": 2.0, "save_ps": 1.0, "compress_ps": 20.0, "n_atoms": 120},
           "uma_inference_mode": "turbo", "seed_gate": {"version": "relaxed", "PS4_fraction_min": 1.0, "min_pair_excl_PS_A_gt": 2.0},
           "gate_check": {"win_ps": 10.0}, "seeds": [11, 12, 13, 14, 15], "stage1_need_pass": 4, "stage2_machines": ["kgy", "gabia"],
           # 회신 DG — 카드에 더한 값 (T 는 합성 궤적용 8 원자 계 · 실제 카드에는 A · B 만)
           "composition": {"A": {"Cl": 12, "Li": 48, "P": 12, "S": 48}, "B": {"Li": 45, "P": 15, "S": 60}, "T": {"P": 4, "S": 4}},
           "software_required": {"model": "uma-s-1p1", "task": "omat", "versions_present": ["fairchem-core", "torch", "ase"]},
           "thermo_required_columns": ["t_ps", "T_K", "T_set_K", "density_g_cm3", "P_GPa", "P_virial_GPa"],
           "first_seed": 11, "stage1_cap_gpu_h": 230.0, "stage1_max_interrupt_retries_per_seed": 1,
           "retry_reasons": {"interrupted": ["power_outage", "host_crash_or_reboot", "hardware_fault", "budget_cap_raised"],
                             "invalid": ["invalid_cause_fixed"]},
           "cap_retry_reasons": ["budget_cap_raised"],
           "attestation_required_fields": ["event", "time_reference", "uncertainty_h", "derivation", "confirmer", "confirmed_at"]}
    VAL["melt_window"]["estimator"] = MELT_WINDOW_ESTIMATOR
    rng = np.random.default_rng(7); L = 12.0
    base = rng.uniform(1, L - 1, (8, 3)); symW = ["P"] * 4 + ["S"] * 4
    win = [base.copy()]
    for _ in range(50):
        nxt = win[-1].copy(); nxt[:4] += rng.normal(0, 0.6, (4, 3)); win.append(nxt)          # t = 50 … 100 · P 만 움직임
    pre_moving = [win[0].copy()]
    for _ in range(50):
        prv = pre_moving[-1].copy(); prv[:4] += rng.normal(0, 0.9, (4, 3)); pre_moving.append(prv)
    pre_moving = pre_moving[::-1]                                                               # t = 0 … 50 · 끝이 창 첫 프레임
    def _mk_win(td_, frames, plan_extra=None, syms=None):
        pl = {"melt_ps": 100.0, "save_ps": 1.0, "fix_density_g_cm3": 1.2, "compress_ps": 20.0,
              "system": "T", "n_atoms": 8, "composition": {"P": 4, "S": 4}}; pl.update(plan_extra or {})
        (pathlib.Path(td_) / "plan.json").write_text(json.dumps(pl), encoding="utf-8")
        _w(str(pathlib.Path(td_) / "traj.xyz"), [Atoms(symbols=(syms or {}).get(i, symW), positions=f, cell=np.eye(3) * L, pbc=True)
                                                 for i, f in enumerate(frames)], format="extxyz")
    with tempfile.TemporaryDirectory() as ta, tempfile.TemporaryDirectory() as tb, tempfile.TemporaryDirectory() as tc:
        _mk_win(ta, pre_moving[:-1] + win)                       # 앞 50 ps 크게 움직임 → 창
        _mk_win(tb, [win[0]] * 50 + win)                         # 앞 50 ps 얼어 있음 → 같은 창
        ra = melt_window_check(ta, values=VAL, log=lambda *a: None); rb = melt_window_check(tb, values=VAL, log=lambda *a: None)
        chk(ra["D_framework_cm2_s"] is not None and ra["D_framework_cm2_s"] == rb["D_framework_cm2_s"] and ra["verdict"] == rb["verdict"]
            and ra["window_used_ps"] == [50.0, 100.0],
            f"DF 반례: 창 [50, 100] 좌표가 같으면 앞 이력과 무관하게 D 가 같다 ({ra['D_framework_cm2_s']:.3e} · {ra['verdict']})")
        chk(ra["verdict"] == "pass", "합성 확산 창 (P 이동) 은 통과")
        _mk_win(tc, pre_moving[:-1] + [win[0]] * 51)            # 앞은 크게 움직였지만 창 안은 얼어 있음
        rc = melt_window_check(tc, values=VAL, log=lambda *a: None)
        chk(rc["verdict"] == "fail", f"⛔음성 DF: 창 안이 얼어 있으면 앞 이력이 커도 '미충족' ({rc['D_framework_cm2_s']:.1e})")
    with tempfile.TemporaryDirectory() as td:
        _mk_win(td, (pre_moving[:-1] + win)[:71])                # 70 ps 에서 끊김
        rt = melt_window_check(td, values=VAL, log=lambda *a: None)
        chk(rt["verdict"] == "incomplete" and rt["window_used_ps"] == [50.0, 70.0] and not rt["coverage_ok"],
            "⛔음성 DF: 70 ps 에서 끊긴 궤적은 '미완' — 실제 쓴 창 [50, 70] 을 그대로 적는다")
        with open(pathlib.Path(td) / "traj.xyz", "a") as fh:
            fh.write("8\nLattice=\"12 0 0 0 12 0 0 0 12\" Properties=species:S:1:pos:R:3\nP 1.0 2.0")   # 쓰는 중 반쪽 프레임
        rt2 = melt_window_check(td, values=VAL, log=lambda *a: None)
        chk(rt2["verdict"] == "incomplete" and rt2["n_frames_read"] == 71, "쓰는 중인 반쪽 프레임에서 멈추고 '미완' (죽지 않는다)")
    with tempfile.TemporaryDirectory() as td:
        _mk_win(td, pre_moving[:-1] + win, plan_extra={"compress_ps": 60.0})
        chk(melt_window_check(td, values=VAL, log=lambda *a: None)["verdict"] == "invalid",
            "⛔음성 DF: 압축 끝 (60 ps) 이 판정 창 시작 (50 ps) 보다 늦으면 '무효'")
    with tempfile.TemporaryDirectory() as td:
        badf = [f.copy() for f in pre_moving[:-1] + win]; badf[80][0, 0] = np.nan
        _mk_win(td, badf)
        chk(melt_window_check(td, values=VAL, log=lambda *a: None)["verdict"] == "invalid", "⛔음성 DF: 창 안 좌표가 NaN 이면 '무효'")
    # 회신 DG P0-2 — 시작 직후 (plan · traj 없음 · plan 쓰는 중) 는 예외가 아니라 '미완' · P1-7 — estimator 이름 · 종 배치
    with tempfile.TemporaryDirectory() as td:
        r0 = melt_window_check(td, values=VAL, log=lambda *a: None)
        (pathlib.Path(td) / "plan.json").write_text('{"melt_ps": 100.0, "save_', encoding="utf-8")
        r1 = melt_window_check(td, values=VAL, log=lambda *a: None)
        (pathlib.Path(td) / "plan.json").write_text(json.dumps({"melt_ps": 100.0, "save_ps": 1.0, "fix_density_g_cm3": 1.2,
                                                                "compress_ps": 20.0, "system": "T", "n_atoms": 8,
                                                                "composition": {"P": 4, "S": 4}}), encoding="utf-8")
        r2 = melt_window_check(td, values=VAL, log=lambda *a: None)
        chk(r0["verdict"] == r1["verdict"] == r2["verdict"] == "incomplete",
            f"⛔음성 DG P0-2: plan.json 없음 · 쓰는 중 · traj 없음 → 예외가 아니라 '미완' ({r0['verdict']} · {r1['verdict']} · {r2['verdict']})")
    with tempfile.TemporaryDirectory() as td:
        _mk_win(td, pre_moving[:-1] + win)
        VALx = json.loads(json.dumps(VAL)); VALx["melt_window"]["estimator"] = "window_mto_v2"
        chk(melt_window_check(td, values=VALx, log=lambda *a: None)["verdict"] == "invalid",
            "⛔음성 DG P1-7: 카드 estimator 를 다른 이름으로 바꾸면 window_mto_v1 을 돌리지 않고 '무효'")
        chk(any("estimator" in x for x in validate_li2s2_values(VALx)), "⛔음성 DG P1-7: 카드 값 검사가 모르는 estimator 를 거부한다")
    with tempfile.TemporaryDirectory() as td:
        sw_ = ["S"] + symW[1:4] + ["P"] + symW[5:]                 # 0 번 프레임만 P·S 자리를 바꿈 (조성은 같다)
        _mk_win(td, pre_moving[:-1] + win, syms={0: sw_})
        r_sp = melt_window_check(td, values=VAL, log=lambda *a: None)
        chk(r_sp["verdict"] == "invalid" and r_sp["species_ok"] is False,
            f"⛔음성 DG P1-7: 0 번 프레임의 종 배치만 바꾸면 판정이 바뀌지 않고 '무효' ({r_sp['verdict']})")
    with tempfile.TemporaryDirectory() as td:
        _mk_win(td, pre_moving[:-1] + win, plan_extra={"n_atoms": 9})
        chk(melt_window_check(td, values=VAL, log=lambda *a: None)["verdict"] == "invalid", "⛔음성 DG: traj 원자 수 ≠ plan → '무효'")
    with tempfile.TemporaryDirectory() as td:                # ⭐ DP 전 리뷰 (둘째) F5 — 앞 프레임 한 곳이 깨지면 '쓰는 중' (미완) 이 아니라 '무효'
        _mk_win(td, pre_moving[:-1] + win)
        tp_ = pathlib.Path(td) / "traj.xyz"
        ln0_ = tp_.read_text(encoding="utf-8").split("\n")
        ln_ = list(ln0_); prt_ = ln_[5 * 10 + 2].split(); prt_[1] = prt_[1] + "x"; ln_[5 * 10 + 2] = " ".join(prt_)
        tp_.write_text("\n".join(ln_), encoding="utf-8")
        r_bad = melt_window_check(td, values=VAL, log=lambda *a: None)
        ln_ = list(ln0_); ln_[5 * 10] = "8x"
        tp_.write_text("\n".join(ln_), encoding="utf-8")
        r_hdr = melt_window_check(td, values=VAL, log=lambda *a: None)
        chk(r_bad["verdict"] == "invalid" and "앞부분이 깨졌다" in str(r_bad.get("message")) and r_bad.get("n_frames_whole") == 101
            and r_hdr["verdict"] == "invalid" and "앞부분이 깨졌다" in str(r_hdr.get("message")),
            f"⛔음성 DP 전 리뷰 (둘째) F5: 6 번째 프레임 좌표 · 머리 한 곳이 깨지면 (온전한 프레임은 더 있음) '무효' — 영원히 '미완' 으로 기다리지 않는다 "
            f"({r_bad['verdict']} · {r_bad.get('n_frames_whole')} · {r_hdr['verdict']})")
        import subprocess as _sp_cli                            # ⭐ DP 전 리뷰 (둘째) — 녹음 판정 CLI 는 런 폴더에 파일을 남기지 않는다
        tp_.write_text("\n".join(ln0_), encoding="utf-8")
        before_ = sorted(x.name for x in pathlib.Path(td).iterdir())
        _cli = _sp_cli.run([sys.executable, __file__, "--melt_window_check", td], capture_output=True, text=True, timeout=300)
        after_ = sorted(x.name for x in pathlib.Path(td).iterdir())
        chk(before_ == after_ and '"verdict"' in _cli.stdout,
            f"⛔음성 DP 전 리뷰 (둘째): --melt_window_check CLI 는 판정을 화면에만 내고 런 폴더에 파일을 안 남긴다 (모르는 파일 = 폴더 판독 보류) "
            f"({sorted(set(after_) - set(before_))} · rc {_cli.returncode})")
    # ③d li2s-2 1 단계 시드 판정 · 묶음 판정 (회신 DF P1-2 · P1-3) — 순수 함수
    SW_OK = {"model": "uma-s-1p1", "task": "omat", "inference": "turbo", "fairchem-core": "2.21.0", "torch": "2.8.0", "ase": "3.26.0"}
    plan_ok = {"system": "A", "seed": 12, "fix_density_g_cm3": 1.91347, "n_atoms": 120, "composition": dict(VAL["composition"]["A"]),
               "software": dict(SW_OK), **VAL["schedule"]}
    plan_ok.pop("n_atoms"); plan_ok["n_atoms"] = 120
    g_ok = {"schedule_complete": True, "window_in_hold": True, "density_ok": True, "pressure_recorded": True,
            "thermo_columns_ok": True, "target_density_g_cm3": 1.91347}
    m_ok = {"verdict": "pass"}; s_ok = {"relaxed": {"PS4_fraction": 1.0, "min_pair_excl_PS_A": 2.31}}
    f_ok = {"result.json": True, "final.xyz": True, "thermo.csv": True, "traj.xyz": True}
    chk(combine_stage1(plan_ok, VAL, g_ok, m_ok, s_ok, f_ok)["status"] == "pass", "1 단계 시드 판정: 모두 맞으면 통과")
    for nm, kw, want in (("PS₄ 0.9167", {"seedg": {"relaxed": {"PS4_fraction": 11 / 12, "min_pair_excl_PS_A": 2.31}}}, "fail"),
                         ("최단 원자간 1.98 Å", {"seedg": {"relaxed": {"PS4_fraction": 1.0, "min_pair_excl_PS_A": 1.98}}}, "fail"),
                         ("녹음 미충족", {"melt": {"verdict": "fail", "message": "x"}}, "fail"),
                         ("녹음 미완", {"melt": {"verdict": "incomplete"}}, "incomplete"),
                         ("일정 미완", {"gate": dict(g_ok, schedule_complete=False)}, "incomplete"),
                         ("압력 기록 없음", {"gate": dict(g_ok, pressure_recorded=False)}, "fail"),
                         ("final.xyz 없음", {"files": dict(f_ok, **{"final.xyz": False})}, "incomplete"),
                         ("밀도 1.9 로 돌림", {"plan": dict(plan_ok, fix_density_g_cm3=1.9)}, "invalid"),
                         ("melt 80 ps 로 돌림", {"plan": dict(plan_ok, melt_ps=80.0)}, "invalid"),
                         ("소프트웨어 기록 없음", {"plan": {k: x for k, x in plan_ok.items() if k != "software"}}, "invalid"),
                         # 회신 DG P1-7 표 — 모르는 상태 · NaN · 반쪽 소프트웨어 · virial 열 없음 · 조성 · 최종 구조 · traj 프레임
                         ("녹음 상태 'unknown' (DG)", {"melt": {"verdict": "unknown"}}, "invalid"),
                         ("plan 목표 밀도 NaN (DG)", {"plan": dict(plan_ok, fix_density_g_cm3=float("nan"))}, "invalid"),
                         ("plan melt_ps NaN (DG)", {"plan": dict(plan_ok, melt_ps=float("nan"))}, "invalid"),
                         ("소프트웨어 fairchem·inference 만 (DG)", {"plan": dict(plan_ok, software={"inference": "turbo", "fairchem-core": "2.21.0"})}, "invalid"),
                         ("torch 판이 ?(오류) (DG)", {"plan": dict(plan_ok, software=dict(SW_OK, torch="?(PackageNotFoundError)"))}, "invalid"),
                         ("virial 열 없음 (DG)", {"gate": dict(g_ok, thermo_columns_ok=False, pressure_recorded=False)}, "invalid"),
                         ("thermo 머리줄에 virial 없음 (DG)", {"checks": {"thermo_header": {"ok": False, "missing": ["P_virial_GPa"]}}, "gate": None}, "invalid"),
                         ("gate 목표 밀도 NaN (DG)", {"gate": dict(g_ok, target_density_g_cm3=float("nan"))}, "invalid"),
                         ("조성 다름 (DG)", {"plan": dict(plan_ok, composition={"Li": 45, "P": 15, "S": 60})}, "invalid"),
                         ("final.xyz 가 5 원자 (DG)", {"checks": {"final_structure": {"ok": False, "why": ["원자 수 5 ≠ 120"]}}}, "invalid"),
                         ("thermo 끝났는데 traj 잘림 (DG)", {"checks": {"traj_frames": {"n": 900, "expected": 1051}}}, "invalid"),
                         ("traj 프레임 수를 못 셈 (DG)", {"checks": {"traj_frames": {"n": None, "expected": 1051}}}, "invalid"),
                         ("일정 미완 · traj 짧음 (DG)", {"gate": dict(g_ok, schedule_complete=False), "checks": {"traj_frames": {"n": 900, "expected": 1051}}}, "incomplete"),
                         ("md_init_raw 불일치 (DG)", {"checks": {"seed_gate_error": "⛔ 이미 있고 다르다"}, "seedg": None}, "invalid")):
        args = {"plan": plan_ok, "gate": g_ok, "melt": m_ok, "seedg": s_ok, "files": f_ok, "checks": None}; args.update(kw)
        got = combine_stage1(args["plan"], VAL, args["gate"], args["melt"], args["seedg"], args["files"], checks=args["checks"])["status"]
        chk(got == want, f"⛔음성 DF/DG: 1 단계 시드 판정 — {nm} → {want} (받음 {got})")
    # 회신 DG P0-1 — 계의 첫 시드 녹음 미충족은 '그 계를 닫는 사건' (러너가 멈춰 일정 미완이어도) · 둘째 시드는 일반 탈락
    c_first = combine_stage1(dict(plan_ok, seed=11), VAL, dict(g_ok, schedule_complete=False), {"verdict": "fail", "message": "x"},
                             None, dict(f_ok, **{"final.xyz": False, "result.json": False}))
    c_second = combine_stage1(plan_ok, VAL, g_ok, {"verdict": "fail", "message": "x"}, s_ok, f_ok)
    c_bad = combine_stage1(dict(plan_ok, seed=11, fix_density_g_cm3=1.9), VAL, g_ok, {"verdict": "fail", "message": "x"}, s_ok, f_ok)
    chk(c_first["status"] == "fail" and c_first["closes_system"] and not c_second["closes_system"] and c_second["status"] == "fail"
        and c_bad["status"] == "invalid" and not c_bad["closes_system"],
        "DG P0-1: 첫 시드 (11) 녹음 미충족 → fail + closes_system (일정 미완이어도) · 둘째 시드는 일반 탈락 · 카드와 다른 런이면 닫지 않고 무효")
    c_m2 = combine_stage1(plan_ok, VAL, dict(g_ok, schedule_complete=False), {"verdict": "fail", "message": "x"}, None,
                          dict(f_ok, **{"final.xyz": False, "result.json": False}))
    c_m2_pass = combine_stage1(plan_ok, VAL, dict(g_ok, schedule_complete=False), {"verdict": "pass", "message": "x"}, None,
                               dict(f_ok, **{"final.xyz": False, "result.json": False}))
    chk(c_m2["status"] == "fail" and not c_m2["closes_system"] and c_m2_pass["status"] == "incomplete",
        "⛔음성 DO 전 리뷰 (규칙 M): 둘째 시드도 녹음 창이 다 찼고 fail 이면 일정 미완 · 최종 파일 없음이어도 fail (결과가 정해졌다 — 끊긴 뒤 재시도로 "
        f"지우지 않는다) · 녹음 pass 면 미완 그대로 ({c_m2['status']} · {c_m2_pass['status']})")
    def _v(st, fc="2.21.0"):
        return {"status": st, "software": {"inference": "turbo", "fairchem-core": fc}}
    ver = {("A", 11): _v("fail"), ("A", 12): _v("pass"), ("A", 13): _v("pass"), ("A", 14): _v("pass"), ("A", 15): _v("pass"),
           ("B", 11): _v("pass"), ("B", 12): _v("pass"), ("B", 13): _v("pass"), ("B", 14): _v("pass"), ("B", 15): _v("fail")}
    COST = {"total_h": 150.0, "cap_h": 230.0}
    sm = summarize_stage1(ver, VAL, cost=COST)
    chk(sm["track"] == "stage1_pass" and sm["stage2"]["seeds"] == [12, 13] and sm["stage2"]["machines"] == {"12": "kgy", "13": "gabia"},
        f"DF P1-3: A11 · B15 탈락이어도 4/5 씩 통과 → 2 단계 시드 = 공통 통과 중 작은 둘 {sm['stage2'] and sm['stage2']['seeds']} (11 고정 아님)")
    sm2 = summarize_stage1({**ver, ("A", 12): _v("fail")}, VAL, cost=COST)
    chk(sm2["track"] == "stop_track" and sm2["per_system"]["A"]["status"] == "fail" and sm2["stage2"] is None,
        "⛔음성 DF: 한쪽 계가 1 단계에서 닫히면 (A 3/5) 다른 계가 통과해도 비교 트랙 전체가 멈춘다")
    sm3 = summarize_stage1({k: (None if k in (("B", 14), ("B", 15)) else x) for k, x in ver.items()} | {("B", 15): None}, VAL, cost=COST)
    chk(sm3["track"] == "pending", "시드 판정이 덜 끝났으면 (B 3 통과 · 2 없음) 대기")
    sm4 = summarize_stage1({**ver, ("B", 13): _v("pass", fc="2.19.0")}, VAL, cost=COST)
    chk(sm4["track"] == "invalid", "⛔음성 DF: 통과 시드의 fairchem 판이 둘 이상이면 무효 (기계 이름이 아니라 판을 고정)")
    all4 = {(s_, sd): _v("pass") for s_ in ("A", "B") for sd in (11, 12, 13, 14)}
    sm5 = summarize_stage1({**all4, ("A", 15): _v("incomplete"), ("B", 15): _v("incomplete")}, VAL, cost=COST)
    sm6 = summarize_stage1({**all4, ("A", 15): None, ("B", 15): None}, VAL, cost=COST)
    chk(sm5["track"] == "pending" and sm6["track"] == "pending" and sm5["stage2"] is None,
        f"⛔음성 DG P1-5: 11–14 통과 · 15 미완 (또는 판정 없음) 이면 묶음은 통과가 아니라 대기 ({sm5['track']} · {sm6['track']})")
    sm7 = summarize_stage1({**ver, ("A", 13): _v("unknown")}, VAL, cost=COST)
    chk(sm7["track"] == "invalid" and bool(sm7["unknown_status"]), "⛔음성 DG P1-7: 판정 상태 'unknown' 은 통과 · 대기가 아니라 무효")
    closed = {**{k: None for k in ver}, ("A", 11): dict(_v("fail"), closes_system=True)}
    closed.update({("B", sd): _v("pass") for sd in (11, 12, 13, 14, 15)})
    closed.update({("A", sd): _v("pass") for sd in (12, 13, 14, 15)})
    sm8 = summarize_stage1(closed, VAL, cost=COST)
    chk(sm8["track"] == "stop_track" and sm8["per_system"]["A"]["status"] == "closed",
        "⛔음성 DG P0-1: A11 이 계를 닫으면 (첫 시드 녹음 미충족) 나머지 아홉이 통과해도 (A 4/5) 트랙 멈춤 — 일반 탈락과 다르다")
    allp = {(s_, sd): _v("pass") for s_ in ("A", "B") for sd in (11, 12, 13, 14, 15)}
    sm_ts = summarize_stage1(allp, VAL, cost={**COST, "terminal_stop": "melt"})
    sm_ts2 = summarize_stage1(closed, VAL, cost={**COST, "terminal_stop": "melt"})
    sm_nf = summarize_stage1({**allp, ("A", 12): dict(_v("pass"), closes_system=True)}, VAL, cost=COST)
    chk(sm_ts["track"] == "invalid" and sm_ts["stage2"] is None and sm_ts2["track"] == "stop_track"
        and sm_nf["track"] == "invalid" and any("첫 시드" in x_ for x_ in sm_nf["identity_problems"]),
        f"⛔음성 DQ 전 리뷰 P2-D: 닫는 STOP 인데 기록 판정은 통과 → invalid (2 단계 없음) · 기록도 닫힘이면 stop_track 그대로 · "
        f"첫 시드 아닌 판정의 closes_system → invalid ({sm_ts['track']} · {sm_ts2['track']} · {sm_nf['track']})")
    sm9 = summarize_stage1(ver, VAL, cost={"total_h": 240.0, "cap_h": 230.0})
    sm10 = summarize_stage1(ver, VAL, cost=None)
    sm11 = summarize_stage1(ver, VAL, cost={"total_h": float("nan"), "cap_h": 230.0})
    chk(sm9["track"] == "cap_incomplete" and sm10["track"] == "pending" and sm11["track"] == "cap_incomplete" and not sm9["stage2"],
        f"⛔음성 DG P0-3: 비용 240 > 상한 230 → 미완결 · 장부 없음 → 대기 · 비유한 → 미완결 ({sm9['track']} · {sm10['track']} · {sm11['track']})")
    chk(validate_li2s2_values(VAL) == [] or [x for x in validate_li2s2_values(VAL) if "composition.T" not in x] == [],
        f"카드 값 검사: 시험 값은 통과 ({validate_li2s2_values(VAL)})")
    # 회신 DH P0-2 — 실행 식별: 자리 (계, 시드) ≠ 판정 · run_id 중복 · 장부 불완전 (invalid) · 장부 미확정 (pending)
    RID = lambda k: f"{k:032x}"
    vid = {(s_, sd): dict(_v("pass"), system=s_, seed=sd, run_id=RID(100 * (s_ == "A") + sd)) for s_ in ("A", "B") for sd in (11, 12, 13, 14, 15)}
    chk(summarize_stage1(vid, VAL, cost=COST)["track"] == "stage1_pass", "실행 식별이 다 맞으면 (자리 = 판정 · run_id 서로 다름) 통과")
    cp = dict(vid); cp[("A", 12)] = dict(vid[("A", 11)])
    sm_cp = summarize_stage1(cp, VAL, cost=COST)
    allc = {k: dict(vid[(k[0], 11)]) for k in vid}
    sm_all = summarize_stage1(allc, VAL, cost=COST)
    ed = dict(vid); ed[("A", 12)] = dict(vid[("A", 11)], seed=12)
    sm_ed = summarize_stage1(ed, VAL, cost=COST)
    chk(sm_cp["track"] == "invalid" and sm_all["track"] == "invalid" and sm_ed["track"] == "invalid" and bool(sm_cp["identity_problems"]),
        f"⛔음성 DH P0-2: A11 판정을 A12 자리에 · 모든 자리에 · 시드만 고쳐서 (run_id 같음) → 한 실행을 여러 시드로 못 센다 ({sm_cp['track']} · {sm_all['track']} · {sm_ed['track']})")
    swp = dict(vid); swp[("A", 12)], swp[("A", 13)] = vid[("A", 13)], vid[("A", 12)]
    chk(summarize_stage1(swp, VAL, cost=COST)["track"] == "invalid",
        "⛔음성 DH P0-2: A12 · A13 판정 파일이 서로 자리를 바꾸면 (run_id 는 각자 하나) 자리 ≠ 판정 이라 무효")
    sm_li = summarize_stage1(vid, VAL, cost=dict(COST, invalid=["A12 판정의 run_id 가 장부에 없다"]))
    sm_lp = summarize_stage1(vid, VAL, cost=dict(COST, pending=["A11 런이 끝나지 않았다"]))
    chk(sm_li["track"] == "invalid" and sm_lp["track"] == "pending",
        f"⛔음성 DH P0-1: 장부 불완전 (누락 · 음수 · 근거 없음) → 무효 · 비용 미확정 런 → 대기 ({sm_li['track']} · {sm_lp['track']})")
    with tempfile.TemporaryDirectory() as td_:
        rd_ = pathlib.Path(td_) / "A" / "seed12"; rd_.mkdir(parents=True)
        ic_ok = identity_check(rd_, {"system": "A", "seed": 12, "run_id": RID(5)})
        ic_cp = identity_check(rd_, {"system": "A", "seed": 11, "run_id": RID(5)})
        ic_no = identity_check(rd_, {"system": "A", "seed": 12})
        ic_bad = identity_check(pathlib.Path(td_) / "A" / "s12", {"system": "A", "seed": 12, "run_id": RID(5)})
    chk(ic_ok["ok"] and not ic_cp["ok"] and not ic_no["ok"] and not ic_bad["ok"],
        "⛔음성 DH P0-2: 폴더 seed12 에 plan 시드 11 → 무효 · run_id 없음 → 무효 · 폴더 이름 꼴 아님 → 무효 (맞으면 통과)")
    chk(combine_stage1(plan_ok, VAL, g_ok, m_ok, s_ok, f_ok, checks={"identity": ic_cp})["status"] == "invalid",
        "⛔음성 DH P0-2: 시드 판정이 실행 식별 불일치를 무효로")
    for nm_, mut in (("재시도 한도 -1", {"stage1_max_interrupt_retries_per_seed": -1}), ("재시도 한도 없음", {"stage1_max_interrupt_retries_per_seed": None}),
                     ("first_seed 12 (seeds[0] 아님)", {"first_seed": 12}), ("상한 NaN", {"stage1_cap_gpu_h": float("nan")}),
                     ("조성 합 ≠ n_atoms", {"composition": {"A": {"Li": 48}, "B": VAL["composition"]["B"]}}),
                     ("software_required 없음", {"software_required": None}), ("밀도 NaN", {"fix_density_g_cm3": {"A": float("nan"), "B": 1.88}}),
                     ("압력 열 목록에 virial 없음", {"thermo_required_columns": ["t_ps", "T_set_K", "density_g_cm3", "P_GPa"]})):
        chk(validate_li2s2_values({**VAL, **mut}) != [], f"⛔음성 DG: 카드 값 검사가 거부한다 — {nm_}")
    # 회신 DJ — 재시도 사유 · 실효 상한 · 증언 필드 (카드 값) · 완료 단계 · 판정 파일 상태 · 선언 검사 (드라이버 단위)
    for nm_, mut in (("retry_reasons 없음", {"retry_reasons": None}), ("retry_reasons 한 종류만", {"retry_reasons": {"interrupted": ["power_outage"]}}),
                     ("retry_reasons 빈 목록", {"retry_reasons": {"interrupted": [], "invalid": ["invalid_cause_fixed"]}}),
                     ("없앤 정전 추가 예산이 남음 (카드 v3)", {"stage1_outage_extra_budget_gpu_h": 45.0}),
                     ("없앤 outage_reasons 가 남음 (카드 v3)", {"outage_reasons": ["power_outage"]}),
                     ("증언 필드에 확인자 없음", {"attestation_required_fields": ["event", "time_reference", "uncertainty_h", "derivation", "confirmed_at"]}),
                     ("상한 사유가 interrupted 밖", {"cap_retry_reasons": ["user_ctrl_c"]}),
                     ("상한 사유가 interrupted 사유 전부", {"cap_retry_reasons": ["power_outage", "host_crash_or_reboot", "hardware_fault", "budget_cap_raised"]}),
                     ("상한 사유 없음", {"cap_retry_reasons": None})):
        chk(validate_li2s2_values({**VAL, **mut}) != [], f"⛔음성 DJ: 카드 값 검사가 거부한다 — {nm_}")
    with tempfile.TemporaryDirectory() as td_:
        RIDF = "5" * 32
        PLAN0 = {"melt_ps": 2.0, "quench_ps": 1.0, "hold_ps": 1.0, "save_ps": 1.0, "dt_fs": 2.0, "run_id": RIDF}
        FR = lambda n, nat="2": "".join(f"{nat}\nLattice=\"5 0 0 0 5 0 0 0 5\"\nLi 0 0 0\nLi 1 1 1\n" for _ in range(n))
        def TH(n, pl=PLAN0):
            """thermo.csv — 진짜 머리 + 저장 간격대로 n 행 (traj 프레임과 같은 수)."""
            si = save_interval_steps(pl) * float(pl["dt_fs"]) / 1000.0
            return ("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n"
                    + "".join(f"{k * si:.3f},300.0,300.0,1.8000,1000.00,-500.0000,0.1000,0.1000\n" for k in range(n)))
        def _fs(name, plan=True, traj=5, thermo="same", final=False, done=False, after=None, attempt=True):
            """done: MD 완료 기록을 실제 쓰기 함수 (write_md_done) 로 · after: 기록 뒤에 폴더를 건드림 (손상 재현) ·
            thermo: 'same' = traj 와 같은 행 수 · None = 파일 없음 · 정수 = 그 행 수. attempt: 러너의 실행 전 기록."""
            d = pathlib.Path(td_) / name; d.mkdir()
            pl = PLAN0 if plan is True else plan
            if attempt:
                (d / ATTEMPT_NAME).write_text(json.dumps({"run_id": RIDF}), encoding="utf-8")
            if isinstance(pl, dict):
                (d / "plan.json").write_text(json.dumps(pl), encoding="utf-8")
            elif isinstance(pl, str):
                (d / "plan.json").write_text(pl, encoding="utf-8")
            try:                                             # 손상된 plan (글자 · 0 · 너무 큰 값) 이면 thermo 는 정상 plan 꼴로 쓴다 (판독이 plan 을 보고 보류하는지 본다)
                plq = pl if isinstance(pl, dict) and save_interval_steps(pl) and planned_md_steps(pl) >= 0 else PLAN0
            except (ValueError, TypeError, KeyError, AttributeError, OverflowError):
                plq = PLAN0
            if traj is not None:
                (d / "traj.xyz").write_text(FR(traj), encoding="utf-8")
            nth = (traj or 0) if thermo == "same" else thermo
            if nth is not None:
                (d / "thermo.csv").write_text(TH(nth, plq), encoding="utf-8")
            if done:
                dd = done if isinstance(done, dict) else {}
                st_ = planned_md_steps(plq)
                write_md_done(d, run_id=dd.get("run_id", RIDF), n_steps_planned=dd.get("planned", st_), n_steps_done=dd.get("done", st_))
            if after:
                after(d)
            if final:
                (d / "final.xyz").write_text("x", encoding="utf-8")
            return folder_stage(d)
        def _tmp_only(d):                                    # 회신 DL P0 반례 2 — 기록을 임시 이름으로만 (os.replace 직전 끊김)
            (d / MD_DONE_TMP).write_text(json.dumps({"run_id": RIDF, "n_steps_planned": 2000, "n_steps_done": 2000}), encoding="utf-8")
        P07 = {**PLAN0, "save_ps": 0.7}
        # ⭐ DO 전 리뷰 — 수 · 프레임 · thermo · 보존 폴더 단위 시험
        num_ok = (not _fin("12.5") and not _fin(True) and not _fin(10 ** 400) and _fin(np.float64(1.5)) and _fin(3)
                  and not _same("100.0", 100.0) and _same(100, 100.0))
        chk(num_ok, "⛔음성 DO 전 리뷰 P1-3: 수 판정은 수 타입만 — '12.5' · True · 10**400 은 수가 아니다 · numpy 수는 수 · '100.0' 은 100 과 같지 않다")
        tdx = pathlib.Path(td_) / "_frames"; tdx.mkdir()
        (tdx / "full_nul.xyz").write_bytes(FR(5).encode() + b"\x00" * 64)
        (tdx / "torn.xyz").write_text(FR(5) + "2\nLattice=\"5 0", encoding="utf-8")
        (tdx / "mid_bad.xyz").write_text(FR(2) + "x\n" + FR(2), encoding="utf-8")
        fr_ = {k: _xyz_frames(tdx / f"{k}.xyz") for k in ("full_nul", "torn", "mid_bad")}
        (tdx / "th.csv").write_bytes(TH(3).encode() + b"\x00" * 40)
        th_rows = len(read_thermo(tdx / "th.csv")["t_ps"])
        chk(fr_ == {"full_nul": 5, "torn": 5, "mid_bad": None} and th_rows == 3,
            "⛔음성 DO 전 리뷰 (소비자 P1 · P0 t9): 프레임 수는 NUL 꼬리 · 덜 써진 마지막 프레임을 빼고 온전한 것만 센다 (끊긴 런이 invalid 로 "
            f"새지 않게) · 중간이 깨지면 None · thermo 의 NUL 꼬리는 건너뛴다 ({fr_} · {th_rows})")
        pz = pathlib.Path(td_) / "_ident" / "A"; pz.mkdir(parents=True)
        idn = {}
        for nm_, att_ in (("seed11.cut1", {"system": "A", "seed": 11, "run_id": RIDF}), ("seed11.cut2", None),
                          ("seed11.cut3", {"system": "A", "seed": 12, "run_id": RIDF}), ("seed11", None)):
            dz = pz / nm_; dz.mkdir()
            if att_ is not None:
                (dz / ATTEMPT_NAME).write_text(json.dumps(att_), encoding="utf-8")
            r_ = identity_check(dz, {"system": "A", "seed": 11, "run_id": RIDF})
            idn[nm_] = (r_["ok"], r_.get("preserved"))
        chk(idn == {"seed11.cut1": (True, True), "seed11.cut2": (False, False), "seed11.cut3": (False, False), "seed11": (True, False)},
            "⛔음성 DO 전 리뷰 (소비자 P0 a): 보존 폴더 seed<N>.<붙임> 은 실행 전 기록의 계 · 시드 · run_id 가 plan 과 같을 때만 같은 실행으로 "
            f"식별 (판정이 이름 때문에 invalid 로 새지 않게) · 기록이 없거나 다르면 아니다 ({idn})")
        dz4 = pz / "seed11.cut4"; dz4.mkdir()                 # ⭐ 회신 DO P1 — 실행 전 기록의 run_id 가 둘 (마지막 값이 plan 과 같아도) → 식별 안 함
        (dz4 / ATTEMPT_NAME).write_text('{"system": "A", "seed": 11, "run_id": "' + "0" * 32 + '", "run_id": "' + RIDF + '"}', encoding="utf-8")
        r4_ = identity_check(dz4, {"system": "A", "seed": 11, "run_id": RIDF})
        vfs_ = pathlib.Path(td_) / "_vfs"; vfs_.mkdir()
        (vfs_ / "stage1_verdict.json").write_text('{"status": "pass", "status": "incomplete"}', encoding="utf-8")
        inv_root = pathlib.Path(td_) / "_inv"; (inv_root / "A" / "seed11").mkdir(parents=True)     # ⭐ 회신 DO P1 — 실행 전 기록 목록도 엄격히
        (inv_root / "A" / "seed11" / ATTEMPT_NAME).write_text('{"system": "A", "seed": 11, "run_id": "' + "0" * 32 + '", "run_id": "' + RIDF + '"}',
                                                             encoding="utf-8")
        inv_f, inv_bad = attempt_inventory(inv_root)
        chk(RIDF not in inv_f and "0" * 32 not in inv_f and any("실행 신원을 못 읽음" in x for x in inv_bad),
            f"⛔음성 회신 DO P1: 실행 전 기록 목록 (attempt_inventory) 은 같은 열쇠 둘인 기록을 마지막 값으로 묶지 않고 못 읽음으로 적는다 ({list(inv_f)} · {inv_bad})")
        chk((r4_["ok"], r4_.get("preserved")) == (False, False) and verdict_file_status(vfs_) == "unreadable",
            "⛔음성 회신 DO P1: 실행 전 기록 · 판정 파일의 같은 열쇠 둘은 마지막 값으로 읽지 않는다 (보존 폴더 식별 안 함 · 판정 상태 판독 불가) "
            f"({(r4_['ok'], r4_.get('preserved'))} · {verdict_file_status(vfs_)})")
        # 판정 함수 쪽 (쓰는 쪽) — gate_check 가 예외면 판정 기록에 '모름' (None + 오류) 으로 적고, 그 기록은 보류로 읽힌다 (깨기 DO19 가 드러낸 시험 구멍)
        _fs("xgw", traj=2)
        _gc0 = globals()["gate_check"]
        def _gc_boom(*a_, **k_):
            raise RuntimeError("selftest gate boom")
        globals()["gate_check"] = _gc_boom
        try:
            vgw = stage1_verdict(pathlib.Path(td_) / "xgw", values=VAL, log=lambda *a: None, reason="selftest — gate 예외")
        finally:
            globals()["gate_check"] = _gc0
        gw_, stg_gw = (vgw.get("gate_check") or {}), folder_stage_detail(pathlib.Path(td_) / "xgw")
        chk(gw_.get("schedule_complete") is None and "boom" in str(gw_.get("error")) and stg_gw[0] == "unreadable"
            and any(e_.startswith("gate_check RuntimeError") for e_ in vgw["provenance"]["judge_nature"]["errors"]),   # ⭐ 회신 DQ P1-1 — 판정 도중 예외로 모은다
            "⛔음성 DO 전 리뷰 P1 (소비자 t4): 판정 중 gate_check 예외는 False 가 아니라 모름 (None + 오류) 으로 적고, 그 판정 기록이 남은 도중 끊김 "
            f"폴더는 보류 (재시도 아님) — 쓰는 쪽까지 ({gw_} · {stg_gw})")
        PASSV = {"status": "pass", "reasons": {}, "run_id": RIDF,
                 "provenance": {"files_sha256": {"plan.json": "a" * 64, "thermo.csv": "b" * 64, "traj.xyz": "c" * 64,
                                                 "final.xyz": "d" * 64, "result.json": "e" * 64}}}
        MIDV = {"status": "incomplete", "reasons": {"incomplete": ["상한 멈춤 (기록용 · 미완)"]},
                "provenance": {"files_sha256": {"plan.json": "a" * 64, "thermo.csv": "b" * 64, "traj.xyz": "c" * 64,
                                                "final.xyz": None, "result.json": None}}}
        def _dangling_result(d):                             # result.json 자리에 깨진 링크 — 링크를 못 만드는 기계 (Windows 권한) 는 디렉터리로 같은 검사 ('파일이 아닌 것')
            try:
                os.symlink(str(d / "nowhere.json"), str(d / "result.json"))
            except (OSError, NotImplementedError, AttributeError):
                (d / "result.json").mkdir()
        def _wv(d, v):                                       # 판정 파일을 그 값으로 (손상 재현)
            (d / "stage1_verdict.json").write_text(json.dumps(v), encoding="utf-8")
        def _judge_prerun(d):                                # 진짜 판정 함수로 plan 전 끊긴 폴더를 판정 (이미 있으면 이력이 생긴다)
            stage1_verdict(d, values=VAL, log=lambda *a: None, reason="selftest")
        def PRERUN(d):
            return stage1_verdict(d, values=VAL, log=lambda *a: None, reason="selftest")
        def _rejudged_after_pass(d):                         # 회신 DM P0-2 반례 1 — pass 판정이 있던 폴더에서 원자료가 없어진 뒤 진짜 재판정
            (d / "stage1_verdict.json").write_text(json.dumps(PASSV), encoding="utf-8")
            stage1_verdict(d, values=VAL, log=lambda *a: None, reason="selftest — 원자료 소실 뒤 재판정")
        fs_ = {"final": _fs("f", final=True), "md_complete": _fs("c", done=True),
               # 회신 DL Q2: 기록 없이 시작된 마지막 기록이 끝 경계 (4 ps = 2,000 스텝) 에 닿음 → 완료 여부 불명 → 보류
               "no_marker_end_reached": _fs("i", traj=5),
               "no_marker_cut_mid": _fs("i2", traj=2),          # 1 ps 에서 끊김 — 명확한 도중 끊김 → 미완 (재시도 대상)
               "nothing_recorded": _fs("i3", traj=None, thermo=None),   # plan 만 — MD 기록 전 끊김
               "header_only": _fs("i4", traj=None, thermo=0),
               "no_plan": _fs("n", plan=False, traj=None, thermo=None),
               "no_plan_no_attempt": _fs("n2", plan=False, traj=None, thermo=None, attempt=False),
               "no_plan_attempt_tmp": _fs("n3", plan=False, traj=None, thermo=None,
                                          after=lambda d: (d / (ATTEMPT_NAME + ".tmp")).write_text("{", encoding="utf-8")),
               "no_plan_judged": _fs("n4", plan=False, traj=None, thermo=None, after=_judge_prerun),   # 러너가 plan 전 끊긴 런을 판정한 기록 (진짜 판정)
               "no_plan_fake_judged": _fs("n5", plan=False, traj=None, thermo=None,   # 지문 없는 'incomplete' 한 줄 — plan 전 판정 꼴이 아니다
                                          after=lambda d: (d / "stage1_verdict.json").write_text('{"status": "incomplete"}', encoding="utf-8")),
               # 회신 DL P0 반례 1 — 완료 기록 · 궤적 · thermo 는 정상이고 plan.json 만 없음 → 보류 (no_plan 아님)
               "plan_gone_after_done": _fs("pg", done=True, after=lambda d: (d / "plan.json").unlink()),
               "no_plan_with_traj": _fs("pt", plan=False, traj=2),
               "no_plan_unknown_file": _fs("pu", plan=False, traj=None, thermo=None,
                                           after=lambda d: (d / "notes.txt").write_text("x", encoding="utf-8")),
               # 회신 DL P0 반례 2 — 임시 기록만 (궤적은 도중이어도 — 임시 기록 하나로 보류)
               "tmp_only_mid": _fs("t1", traj=2, after=_tmp_only),
               "tmp_and_done": _fs("t2", done=True, after=_tmp_only),
               "fire_log_no_marker": _fs("fl", traj=2, after=lambda d: (d / "final_relax.log").write_text("FIRE", encoding="utf-8")),
               "unreadable_plan": _fs("u", plan='{"melt_ps": 2'),
               "plan_no_save": _fs("u2", plan={k: v for k, v in PLAN0.items() if k != "save_ps"}, traj=2),
               # 회신 DK P0-1 재현: 완료 기록 뒤 첫 원자 수만 바꿈 · 첫 줄을 NUL 로 → 손상된 완료 궤적은 보류 (재담금질 아님)
               "atomcount_changed": _fs("a", done=True, after=lambda d: (d / "traj.xyz").write_text(FR(5).replace("2\n", "3\n", 1), encoding="utf-8")),
               "first_line_nul": _fs("z", done=True, after=lambda d: (d / "traj.xyz").write_bytes(b"\x00" + FR(5).encode()[1:])),
               "thermo_changed": _fs("h", done=True, after=lambda d: (d / "thermo.csv").write_text(TH(4), encoding="utf-8")),
               "traj_gone": _fs("g", done=True, after=lambda d: (d / "traj.xyz").unlink()),
               "marker_other_run": _fs("o", done={"run_id": "6" * 32}),
               "marker_short": _fs("s", done={"done": planned_md_steps(PLAN0) - 1}),
               "marker_cut": _fs("x", done=True, after=lambda d: (d / MD_DONE_NAME).write_text('{"run_id": "', encoding="utf-8")),
               "plan_no_run_id": _fs("r", plan={k: v for k, v in PLAN0.items() if k != "run_id"}, done=True),
               # 회신 DK P1-1 · DL Q2: save 0.7 ps 를 1,750 스텝 (= 끝 경계) 에서 끊음 → 완료 여부 불명 → 보류 · 700 ps 쪽은 미완
               "save07_end": _fs("k", plan=P07, traj=6), "save07_mid": _fs("k2", plan=P07, traj=3),
               "save07_done": _fs("l", plan=P07, traj=6, done=True),
               "no_dt": _fs("d", plan={k: v for k, v in PLAN0.items() if k != "dt_fs"}, done=True),
               # 진행량 판독 — 시각의 유효한 앞부분이 남은 꼬리는 시작된 기록으로 세고 · NUL 만 남은 꼬리는 건너뛴다 (복원 못 함) · 꼬리가 아닌 깨짐은 보류
               "thermo_nul_tail": _fs("q1", traj=2, after=lambda d: open(d / "thermo.csv", "ab").write(b"\x00" * 64)),
               "thermo_partial_mid": _fs("q2", traj=2, after=lambda d: open(d / "thermo.csv", "a").write("1.0")),   # '1.0' ≠ '2.000' 앞부분 → 보류
               # ⭐ 회신 DM P0-1 재현 — 완료 기록 없음 · 궤적 앞부분만 · thermo 에 온전한 0 · 1 · 4 ps (= 끝) 행 → 남은 끝 시각을 버리지 않는다
               "thermo_end_row_kept": _fs("e1", traj=2, after=lambda d: (d / "thermo.csv").write_text(
                   "".join(TH(5).splitlines(keepends=True)[i] for i in (0, 1, 2, 5)), encoding="utf-8")),
               "thermo_last_row_wrong": _fs("e2", traj=2, after=lambda d: open(d / "thermo.csv", "a").write(
                   "2.500,300.0,300.0,1.8000,1000.00,-500.0000,0.1000,0.1000\n")),
               "thermo_tail_prefix_ok": _fs("e3", traj=2, after=lambda d: open(d / "thermo.csv", "a").write("2.0")),      # 대조: 덜 써진 다음 기록
               "thermo_tail_bad_prefix": _fs("e4", traj=2, after=lambda d: open(d / "thermo.csv", "a").write("12")),
               "thermo_tail_row_nul_ok": _fs("e5", traj=2, after=lambda d: open(d / "thermo.csv", "ab").write(b"2.000,300.0\x00\x00")),
               "thermo_tail_nul_text": _fs("e6", traj=2, after=lambda d: open(d / "thermo.csv", "ab").write(b"2.0\x00x")),
               "thermo_tail_gap": _fs("e7", traj=2, after=lambda d: open(d / "thermo.csv", "ab").write(
                   b"\x00\x00\x00\n2.000,300.0,300.0,1.8000,1000.00,-500.0000,0.1000,0.1000\n")),
               # ⭐ 회신 DM P0-2 재현 — 판정 기록은 이름이 아니라 내용으로 (plan 없는 폴더)
               "no_plan_history_pass": _fs("v1", plan=False, traj=None, thermo=None, after=_rejudged_after_pass),
               "no_plan_verdict_tmp_pass": _fs("v2", plan=False, traj=None, thermo=None,
                                               after=lambda d: (d / "stage1_verdict.json.tmp").write_text(json.dumps(PASSV), encoding="utf-8")),
               "no_plan_verdict_other": _fs("v3", plan=False, traj=None, thermo=None, after=lambda d: (d / "stage1_verdict.json").write_text(
                   json.dumps({**PRERUN(d), "reasons": {"incomplete": ["traj 프레임 3 ≠ 계획 5"]}}), encoding="utf-8")),
               "no_plan_history_garbled": _fs("v4", plan=False, traj=None, thermo=None,
                                              after=lambda d: [_judge_prerun(d), (d / VERDICT_HISTORY).write_text("{\n", encoding="utf-8")]),
               "no_plan_judged_real": _fs("v5", plan=False, traj=None, thermo=None, after=lambda d: [_judge_prerun(d), _judge_prerun(d)]),
               # 이력 줄의 '새 판정' 이 pass 인데 그 뒤 줄이 없다 (앞뒤가 안 맞는 이력) — 이전 판정이 plan 전 것이어도 보류
               "no_plan_history_new_pass": _fs("v9", plan=False, traj=None, thermo=None, after=lambda d: [
                   _judge_prerun(d), (d / VERDICT_HISTORY).write_text(json.dumps(
                       {"prev": json.loads((d / "stage1_verdict.json").read_text(encoding="utf-8")), "prev_status": "incomplete",
                        "new_status": "pass", "new_provenance": PASSV["provenance"]}) + "\n", encoding="utf-8")]),
               # 판정 기록의 완료 흔적은 plan 이 있는 도중 끊김 폴더에서도 재시도를 막는다 · 대조: 상한 멈춤 판정 (MD 지문만) 은 그대로 미완
               "mid_history_pass": _fs("v6", traj=2, after=lambda d: [(d / "stage1_verdict.json").write_text(json.dumps(MIDV), encoding="utf-8"),
                                                                    _append_history(d, PASSV, MIDV, "selftest")]),
               "mid_verdict_tmp": _fs("v7", traj=2, after=lambda d: (d / "stage1_verdict.json.tmp").write_text(json.dumps(MIDV), encoding="utf-8")),
               "mid_cap_verdict_ok": _fs("v8", traj=2, after=lambda d: (d / "stage1_verdict.json").write_text(json.dumps(MIDV), encoding="utf-8")),
               # 판정 꼴은 plan 전 것인데 원자료 지문 (궤적) 이 남았다 — 판정 때는 MD 산출물이 있었다 → 보류
               "no_plan_verdict_had_traj": _fs("w1", plan=False, traj=None, thermo=None, after=lambda d: (d / "stage1_verdict.json").write_text(
                   json.dumps({**PRERUN(d), "provenance": {"files_sha256": {**{x: None for x in PROVENANCE_FILES}, "traj.xyz": "c" * 64}}}),
                   encoding="utf-8")),
               # invalid 판정인데 최종 산출물 지문이 있다 (끝까지 돈 뒤 최종 파일 소실) · pass 인데 최종 지문은 없다 → 둘 다 보류
               "mid_verdict_invalid_final": _fs("w2", traj=2, after=lambda d: (d / "stage1_verdict.json").write_text(
                   json.dumps({"status": "invalid", "reasons": {"invalid": ["x"]}, "provenance": PASSV["provenance"]}), encoding="utf-8")),
               "mid_history_pass_nofinal": _fs("w3", traj=2, after=lambda d: [(d / "stage1_verdict.json").write_text(json.dumps(MIDV), encoding="utf-8"),
                   _append_history(d, {**PASSV, "provenance": MIDV["provenance"]}, MIDV, "selftest")]),
               # 같은 갈래 (회신 DM P0-2 최소 수정 '완료 흔적이나 해석할 수 없는 기록이 있으면 보류') — 도중 끊김 후보도 판정 기록을 내용으로:
               #   못 읽은 이전 판정 (진짜 _append_history 꼴 · raw_text 에 pass) · 모르는 상태 · incomplete 인데 일정 끝 · 프레임 다 참
               #   (MD 완료 · FIRE 미완 폴더의 판정 꼴) → 보류 / 대조: invalid (흔적 없음 — 원인을 고친 재시도 경로) · 일정 미완이 적힌 incomplete → 미완
               "mid_history_unreadable_prev": _fs("w4", traj=2, after=lambda d: [(d / "stage1_verdict.json").write_text(json.dumps(MIDV), encoding="utf-8"),
                   _append_history(d, {"status": None, "⛔": "이전 판정 파일을 못 읽었다 (JSONDecodeError)", "raw_text": '{"status": "pass", "reaso'},
                                   MIDV, "selftest")]),
               "mid_verdict_unknown_status": _fs("w5", traj=2, after=lambda d: (d / "stage1_verdict.json").write_text(
                   json.dumps({**MIDV, "status": "maybe"}), encoding="utf-8")),
               "mid_verdict_sched_done": _fs("w6", traj=2, after=lambda d: (d / "stage1_verdict.json").write_text(
                   json.dumps({**MIDV, "gate_check": {"schedule_complete": True}}), encoding="utf-8")),
               "mid_history_frames_full": _fs("w7", traj=2, after=lambda d: [(d / "stage1_verdict.json").write_text(json.dumps(MIDV), encoding="utf-8"),
                   _append_history(d, {**MIDV, "checks": {"traj_frames": {"n": 5, "expected": 5}}}, MIDV, "selftest")]),
               "mid_invalid_ok": _fs("w8", traj=2, after=lambda d: (d / "stage1_verdict.json").write_text(
                   json.dumps({"status": "invalid", "reasons": {"invalid": ["x"]}, "provenance": MIDV["provenance"]}), encoding="utf-8")),
               "mid_verdict_open_ok": _fs("w9", traj=2, after=lambda d: (d / "stage1_verdict.json").write_text(json.dumps(
                   {**MIDV, "gate_check": {"schedule_complete": False}, "checks": {"traj_frames": {"n": 2, "expected": 5}}}), encoding="utf-8")),
               # ⭐ 회신 DN P1 — 완료 판단 필드가 있는데 타입이 틀리면 보류 (정수로 바꿔 읽지 않는다) / 없음 · None 은 허용 (대조 yd)
               "mid_frames_n_str": _fs("y1", traj=2, after=lambda d: [_wv(d, MIDV),
                   _append_history(d, {**MIDV, "checks": {"traj_frames": {"n": "5", "expected": 5}}}, MIDV, "selftest")]),
               "mid_frames_exp_str": _fs("y2", traj=2, after=lambda d: _wv(d, {**MIDV, "checks": {"traj_frames": {"n": 5, "expected": "5"}}})),
               "mid_frames_n_bool": _fs("y3", traj=2, after=lambda d: _wv(d, {**MIDV, "checks": {"traj_frames": {"n": True, "expected": 1}}})),
               "mid_frames_exp_zero": _fs("y4", traj=2, after=lambda d: _wv(d, {**MIDV, "checks": {"traj_frames": {"n": 2, "expected": 0}}})),
               "mid_sched_str": _fs("y5", traj=2, after=lambda d: _wv(d, {**MIDV, "gate_check": {"schedule_complete": "true"}})),
               "mid_gate_not_dict": _fs("y6", traj=2, after=lambda d: _wv(d, {**MIDV, "gate_check": "done"})),
               "mid_checks_not_dict": _fs("y7", traj=2, after=lambda d: _wv(d, {**MIDV, "checks": ["traj_frames"]})),
               "mid_tf_not_dict": _fs("y8", traj=2, after=lambda d: _wv(d, {**MIDV, "checks": {"traj_frames": 5}})),
               "mid_prov_not_dict": _fs("y9", traj=2, after=lambda d: _wv(d, {**MIDV, "provenance": "x"})),
               "mid_fs_not_dict": _fs("ya", traj=2, after=lambda d: _wv(d, {**MIDV, "provenance": {"files_sha256": "x"}})),
               "mid_final_hash_empty": _fs("yb", traj=2, after=lambda d: _wv(d, {**MIDV, "provenance": {"files_sha256": {
                   **MIDV["provenance"]["files_sha256"], "final.xyz": ""}}})),
               "mid_hist_new_prov_bad": _fs("yc", traj=2, after=lambda d: [_wv(d, MIDV), (d / VERDICT_HISTORY).write_text(json.dumps(
                   {"prev": MIDV, "prev_status": "incomplete", "new_status": "incomplete", "new_provenance": "x"}) + "\n", encoding="utf-8")]),
               "mid_none_fields_ok": _fs("yd", traj=2, after=lambda d: _wv(d, {**MIDV, "gate_check": None,
                                                                              "checks": {"traj_frames": {"n": None, "expected": None}}})),
               "no_plan_reasons_extra": _fs("ye", plan=False, traj=None, thermo=None, after=lambda d: (d / "stage1_verdict.json").write_text(
                   json.dumps({**PRERUN(d), "reasons": {"incomplete": ["plan.json 없음"], "fail": ""}}), encoding="utf-8")),
               # ⭐ DO 전 리뷰 F1 — 완료 기록 없는 폴더의 MD 뒤 산출물 · 모르는 파일 → 보류 / MD 중 파일만 → 미완 (대조 x5)
               "post_md_raw": _fs("x1", traj=2, after=lambda d: (d / SEED_GATE_RAW).write_text("x", encoding="utf-8")),
               "post_md_gr": _fs("x2", traj=2, after=lambda d: (d / "gr_partials.csv").write_text("r,g\n", encoding="utf-8")),
               "post_md_vasp": _fs("x3", traj=2, after=lambda d: (d / "final.vasp").write_text("x", encoding="utf-8")),
               "mid_unknown_file": _fs("x4", traj=2, after=lambda d: (d / "gate_check.json").write_text("{}", encoding="utf-8")),
               "mid_allowed_files_ok": _fs("x5", traj=2, after=lambda d: [(d / "initial.xyz").write_text("x", encoding="utf-8"),
                                                                          (d / "prerelax.log").write_text("x", encoding="utf-8")]),
               # F2 — final · result 자리에 파일이 아닌 것
               "final_is_dir": _fs("x6", traj=2, after=lambda d: (d / "final.xyz").mkdir()),
               "result_dangling": _fs("x7", traj=2, after=_dangling_result),
               # F5 — plan 일정 값의 타입 · 범위
               "plan_save_str": _fs("x8", plan={**PLAN0, "save_ps": "1"}, traj=2),
               "plan_dt_bool": _fs("x9", plan={**PLAN0, "dt_fs": True}, traj=2),
               "plan_save_zero": _fs("xa", plan={**PLAN0, "save_ps": 0}, traj=2),
               "plan_hold_neg": _fs("xb", plan={**PLAN0, "hold_ps": -3.0}, traj=2),
               "plan_huge": _fs("xc", plan={**PLAN0, "melt_ps": 1e308}, traj=2),
               # F6 — 깊은 JSON (RecursionError) 은 죽지 않고 보류
               "plan_deep": _fs("xd", plan="[" * 100000 + "]" * 100000, traj=2),
               "verdict_deep": _fs("xe", traj=2, after=lambda d: (d / "stage1_verdict.json").write_text("[" * 100000 + "]" * 100000,
                                                                                                      encoding="utf-8")),
               # F7 — 크기는 있는데 NUL 뿐
               "thermo_all_nul": _fs("xf", traj=None, after=lambda d: (d / "thermo.csv").write_bytes(b"\x00" * 4096)),
               "traj_all_nul": _fs("xg", traj=2, thermo=None, after=lambda d: (d / "traj.xyz").write_bytes(b"\x00" * 4096)),
               # 판정 기록의 흔적 (소비자 P1 · F4)
               "mid_gate_error": _fs("xh", traj=2, after=lambda d: _wv(d, {**MIDV, "gate_check": {"schedule_complete": None, "error": "x"}})),
               "mid_final_structure": _fs("xi", traj=2, after=lambda d: _wv(d, {**MIDV, "checks": {"final_structure": {"ok": True}}})),
               "mid_seed_gate_view": _fs("xj", traj=2, after=lambda d: _wv(d, {**MIDV, "seed_gate_view": {"PS4_fraction": 1.0}})),
               "mid_frames_plan": _fs("xk", traj=2, after=lambda d: _wv(d, {**MIDV, "checks": {"traj_frames": {"n": 5, "expected": None}}})),
               "mid_frames_plan_ok": _fs("xl", traj=2, after=lambda d: _wv(d, {**MIDV, "checks": {"traj_frames": {"n": 2, "expected": None}}})),
               "mid_hist_line_mismatch": _fs("xm", traj=2, after=lambda d: [_wv(d, MIDV), (d / VERDICT_HISTORY).write_text(json.dumps(
                   {"prev": MIDV, "prev_status": "pass", "new_status": "incomplete", "new_provenance": MIDV["provenance"]}) + "\n",
                   encoding="utf-8")]),
               "mid_hist_summary_pass": _fs("xn", traj=2, after=lambda d: _wv(d, {**MIDV, "history": {"prev_status": "pass"}})),
               "mid_hist_summary_badtype": _fs("xq", traj=2, after=lambda d: _wv(d, {**MIDV, "history": {"prev_status": 1}})),
               # ⭐ 회신 DO P1 — 같은 열쇠 둘 (마지막 값으로 읽으면 완료 흔적이 사라지거나 일정이 바뀐다) = 해석할 수 없는 기록 (보류)
               "mid_dup_frames_n": _fs("xr", traj=2, after=lambda d: (d / "stage1_verdict.json").write_text(
                   json.dumps({**MIDV, "checks": {"traj_frames": {"n": 5, "expected": 5}}}).replace('{"n": 5,', '{"n": 5, "n": 1,', 1),
                   encoding="utf-8")),
               "mid_dup_hist_sched": _fs("xs", traj=2, after=lambda d: [_wv(d, MIDV), (d / VERDICT_HISTORY).write_text(json.dumps(
                   {"prev": {**MIDV, "gate_check": {"schedule_complete": True}}, "prev_status": "incomplete", "new_status": "incomplete",
                    "new_provenance": MIDV["provenance"]}).replace('"schedule_complete": true', '"schedule_complete": true, "schedule_complete": false', 1)
                   + "\n", encoding="utf-8")]),
               "plan_dup_hold": _fs("xt", plan=json.dumps(PLAN0).replace('"hold_ps": 1.0', '"hold_ps": 1.0, "hold_ps": 1000.0', 1), traj=2),
               "md_done_dup": _fs("xu", done=True, after=lambda d: (d / MD_DONE_NAME).write_text(re.sub(
                   r'"n_steps_done": (\d+)', r'"n_steps_done": 1, "n_steps_done": \1', (d / MD_DONE_NAME).read_text(encoding="utf-8"), count=1),
                   encoding="utf-8")),
               # ⭐ DP 깨기 DO7 (살아남음) — 안쪽에서 안 잡는 판독 예외 (MD 완료 기록의 깊은 JSON = RecursionError) 는 바깥 F6 이 보류로
               "md_done_deep": _fs("xv", done=True, after=lambda d: (d / MD_DONE_NAME).write_text("[" * 100000 + "]" * 100000, encoding="utf-8")),
               # F3 — plan 전 판정에 진짜 함수가 안 쓰는 열쇠 · 재판정 요약의 과학적 판정
               "no_plan_extra_key": _fs("xo", plan=False, traj=None, thermo=None, after=lambda d: (d / "stage1_verdict.json").write_text(
                   json.dumps({**PRERUN(d), "gate_check": {"schedule_complete": True}}), encoding="utf-8")),
               "no_plan_hist_summary_pass": _fs("xp", plan=False, traj=None, thermo=None, after=lambda d: (d / "stage1_verdict.json").write_text(
                   json.dumps({**PRERUN(d), "history": {"prev_status": "pass"}}), encoding="utf-8")),
               # 덜 써진 마지막 줄 — 첫 칸부터 NUL 이 섞인 조각 (온전한 행으로 읽히면 꼬리 규칙을 안 거친다 · DL 깨기 N6 이 잡은 시험 구멍)
               "thermo_partial_end": _fs("q3", traj=4, after=lambda d: open(d / "thermo.csv", "ab").write(b"4.0\x00\x00\x00")),
               "thermo_garbage_mid": _fs("q4", traj=3, after=lambda d: (d / "thermo.csv").write_text(
                   TH(3).replace("1.000,", "x.000,", 1), encoding="utf-8")),
               "thermo_bad_cadence": _fs("q5", traj=3, after=lambda d: (d / "thermo.csv").write_text(
                   TH(3).replace("1.000,", "1.500,", 1), encoding="utf-8")),
               "thermo_no_header": _fs("q6", traj=2, after=lambda d: (d / "thermo.csv").write_text(
                   "".join(TH(2).splitlines(keepends=True)[1:]), encoding="utf-8")),
               # 머리 이름이 다르다 (첫 칸이 t_ps 가 아님) — 꼬리 시각 규칙으로는 안 걸린다 (행 시각은 맞다 · DM 깨기 N18 이 드러낸 시험 구멍)
               "thermo_wrong_header": _fs("q6b", traj=2, after=lambda d: (d / "thermo.csv").write_text(
                   TH(2).replace("t_ps,", "time_ps,", 1), encoding="utf-8")),
               "traj_partial_end": _fs("q7", traj=4, thermo=4, after=lambda d: open(d / "traj.xyz", "a").write("2\nLattice=\"5 0 0")),
               "traj_garbage_mid": _fs("q8", traj=3, after=lambda d: (d / "traj.xyz").write_text(
                   FR(1) + "garbage\n" + FR(2), encoding="utf-8")),
               "traj_nul_tail": _fs("q9", traj=2, after=lambda d: open(d / "traj.xyz", "ab").write(b"\x00" * 64))}
        exp_fs = {"final": "final", "md_complete": "md_complete", "no_marker_end_reached": "unreadable", "no_marker_cut_mid": "md_incomplete",
                  "nothing_recorded": "md_incomplete", "header_only": "md_incomplete",
                  "no_plan": "no_plan", "no_plan_no_attempt": "no_plan", "no_plan_attempt_tmp": "no_plan", "no_plan_judged": "no_plan",
                  "no_plan_fake_judged": "unreadable",
                  "plan_gone_after_done": "unreadable", "no_plan_with_traj": "unreadable", "no_plan_unknown_file": "unreadable",
                  "tmp_only_mid": "unreadable", "tmp_and_done": "unreadable", "fire_log_no_marker": "unreadable",
                  "unreadable_plan": "unreadable", "plan_no_save": "unreadable",
                  "atomcount_changed": "unreadable", "first_line_nul": "unreadable",
                  "thermo_changed": "unreadable", "traj_gone": "unreadable", "marker_other_run": "unreadable", "marker_short": "unreadable",
                  "marker_cut": "unreadable", "plan_no_run_id": "unreadable", "save07_end": "unreadable", "save07_mid": "md_incomplete",
                  "save07_done": "md_complete", "no_dt": "unreadable",
                  "thermo_nul_tail": "md_incomplete", "thermo_partial_mid": "unreadable", "thermo_partial_end": "unreadable",
                  "thermo_end_row_kept": "unreadable", "thermo_last_row_wrong": "unreadable", "thermo_tail_prefix_ok": "md_incomplete",
                  "thermo_tail_bad_prefix": "unreadable", "thermo_tail_row_nul_ok": "md_incomplete", "thermo_tail_nul_text": "unreadable",
                  "thermo_tail_gap": "unreadable",
                  "no_plan_history_pass": "unreadable", "no_plan_verdict_tmp_pass": "unreadable", "no_plan_verdict_other": "unreadable",
                  "no_plan_history_garbled": "unreadable", "no_plan_judged_real": "no_plan", "no_plan_history_new_pass": "unreadable",
                  "mid_history_pass": "unreadable", "mid_verdict_tmp": "unreadable", "mid_cap_verdict_ok": "md_incomplete",
                  "no_plan_verdict_had_traj": "unreadable", "mid_verdict_invalid_final": "unreadable", "mid_history_pass_nofinal": "unreadable",
                  "mid_history_unreadable_prev": "unreadable", "mid_verdict_unknown_status": "unreadable", "mid_verdict_sched_done": "unreadable",
                  "mid_history_frames_full": "unreadable", "mid_invalid_ok": "md_incomplete", "mid_verdict_open_ok": "md_incomplete",
                  "mid_frames_n_str": "unreadable", "mid_frames_exp_str": "unreadable", "mid_frames_n_bool": "unreadable",
                  "mid_frames_exp_zero": "unreadable", "mid_sched_str": "unreadable", "mid_gate_not_dict": "unreadable",
                  "mid_checks_not_dict": "unreadable", "mid_tf_not_dict": "unreadable", "mid_prov_not_dict": "unreadable",
                  "mid_fs_not_dict": "unreadable", "mid_final_hash_empty": "unreadable", "mid_hist_new_prov_bad": "unreadable",
                  "mid_none_fields_ok": "md_incomplete", "no_plan_reasons_extra": "unreadable",
                  "post_md_raw": "unreadable", "post_md_gr": "unreadable", "post_md_vasp": "unreadable", "mid_unknown_file": "unreadable",
                  "mid_allowed_files_ok": "md_incomplete", "final_is_dir": "unreadable", "result_dangling": "unreadable",
                  "plan_save_str": "unreadable", "plan_dt_bool": "unreadable", "plan_save_zero": "unreadable", "plan_hold_neg": "unreadable",
                  "plan_huge": "unreadable", "plan_deep": "unreadable", "verdict_deep": "unreadable", "thermo_all_nul": "unreadable",
                  "traj_all_nul": "unreadable", "mid_gate_error": "unreadable", "mid_final_structure": "unreadable",
                  "mid_seed_gate_view": "unreadable", "mid_frames_plan": "unreadable", "mid_frames_plan_ok": "md_incomplete",
                  "mid_hist_line_mismatch": "unreadable", "mid_hist_summary_pass": "unreadable", "mid_hist_summary_badtype": "unreadable",
                  "no_plan_extra_key": "unreadable", "mid_dup_frames_n": "unreadable", "mid_dup_hist_sched": "unreadable",
                  "plan_dup_hold": "unreadable", "md_done_dup": "unreadable", "md_done_deep": "unreadable",
                  "no_plan_hist_summary_pass": "unreadable",
                  "thermo_garbage_mid": "unreadable", "thermo_bad_cadence": "unreadable", "thermo_no_header": "unreadable", "thermo_wrong_header": "unreadable",
                  "traj_partial_end": "unreadable", "traj_garbage_mid": "unreadable", "traj_nul_tail": "md_incomplete"}
        chk(fs_ == exp_fs,
            "⛔음성 DJ Q2 · DK P0-1 · P1-1 · DL P0 · Q2: 완료 단계 = MD 완료 기록으로 (프레임을 안 센다) — 최종 · 기록 맞음 = MD 완료 · "
            "기록 없이 끝 경계 (1 ps 일정 4 ps · 0.7 ps 일정 1,750 스텝) = 완료 여부 불명 → 보류 · 끝 경계 앞 (도중) · MD 기록 전 = 미완 · "
            "plan 없고 실행 전 기록뿐 = no_plan · **plan 만 지운 완료 폴더 · plan 없는 궤적 · 모르는 파일 · 임시 기록 · FIRE 로그만** = 보류 · "
            "기록 뒤 원자 수 · NUL · thermo 바뀜 · 궤적 없음 · 다른 run_id · 스텝 모자람 · 기록 잘림 · plan run_id · dt · save 없음 = 보류 · "
            "시각의 유효한 앞부분이 남은 꼬리는 시작된 기록으로 세고 (NUL 만 남은 꼬리는 건너뛴다 — 진행량을 복원하지 못한다) · "
            "꼬리가 아닌 깨짐 · 시각 어긋남 · 머리 없음 = 보류 · "
            "판정 기록 (회신 DM P0-2): 못 읽은 이전 판정 · 모르는 상태 · 일정 끝 · 프레임 다 참이 적힌 판정 = 보류 · invalid · 일정 미완 판정 = 미완 "
            f"({ {k: fs_[k] for k in fs_ if fs_[k] != exp_fs[k]} })")
        rs_dn = {k: folder_stage_detail(pathlib.Path(td_) / k)[1] for k in ("y1", "y4", "y5", "y9", "yb", "yc")}
        want_dn = {"y1": "n 타입이 str", "y4": "말이 안 된다", "y5": "schedule_complete 타입이 str", "y9": "provenance 타입이 str",
                   "yb": "64 자리 16진수", "yc": "provenance 타입이 str"}
        chk(all(want_dn[k] in (rs_dn[k] or "") for k in want_dn),
            "⛔음성 DN P1: 완료 판단 필드가 있는데 타입이 틀리면 (n:\"5\" · expected 0 · schedule_complete:\"true\" · provenance 글자 · 빈 지문 · "
            f"이력의 새 판정 지문 글자) '해석할 수 없는 기록' 이유로 보류한다 — 다른 갈래의 보류와 구별 ({rs_dn})")
        rs_ct = {k: folder_stage_detail(pathlib.Path(td_) / k)[1] for k in ("y6", "y7")}   # mid_gate_not_dict · mid_checks_not_dict
        chk(all("타입이" in (r_ or "") for r_ in rs_ct.values()),
            "⛔음성 회신 DN P1 (이유): 판정 기록의 gate_check · checks 가 객체가 아니면 '타입 오류' 로 보류한다 (판독 예외로 새지 않는다 · "
            f"깨기 DN8 이 드러낸 시험 구멍) ({rs_ct})")
        sm_res = {}                                          # ⭐ 회신 DO P2 (Codex 재현) — 판정 기록의 중첩 꼴 · 예외 → invalid 요약 (이전 통과 파일을 안 남긴다)
        for nm_, bad_ in (("provenance_list", {"provenance": [1]}), ("software_list", {"software": [1]}), ("run_id_dict", {"run_id": {}}),
                          ("reasons_list", {"reasons": []}), ("prov_fs_list", {"provenance": {"files_sha256": [1]}})):
            rs_ = pathlib.Path(td_) / f"_sum_{nm_}"; (rs_ / "A" / "seed11").mkdir(parents=True)
            (rs_ / "stage1_summary.json").write_text(json.dumps({"track": "stage1_pass"}), encoding="utf-8")
            (rs_ / "A" / "seed11" / "stage1_verdict.json").write_text(json.dumps({"status": "pass", **bad_}), encoding="utf-8")
            try:
                r_ = stage1_summary(rs_, values=VAL, log=lambda *a: None); ok_ = True
            except Exception:
                r_, ok_ = {}, False
            sm_res[nm_] = (ok_, r_.get("track"), json.loads((rs_ / "stage1_summary.json").read_text(encoding="utf-8")).get("track"),
                           ((r_.get("per_system") or {}).get("A") or {}).get("per_seed", {}).get(11))
        rsx = pathlib.Path(td_) / "_sum_raise"; rsx.mkdir()
        (rsx / "stage1_summary.json").write_text(json.dumps({"track": "stage1_pass"}), encoding="utf-8")
        _ss0 = globals()["summarize_stage1"]
        def _ss_boom(*a_, **k_):
            raise RuntimeError("selftest summary boom")
        globals()["summarize_stage1"] = _ss_boom
        try:
            rx_ = stage1_summary(rsx, values=VAL, log=lambda *a: None)
        finally:
            globals()["summarize_stage1"] = _ss0
        fx_ = json.loads((rsx / "stage1_summary.json").read_text(encoding="utf-8"))
        chk(all(v_ == (True, "invalid", "invalid", "invalid") for v_ in sm_res.values()) and rx_["track"] == fx_["track"] == "invalid"
            and "boom" in str(fx_.get("error")),
            "⛔음성 회신 DO P2 (Codex 재현): 판정 기록의 중첩 꼴 (provenance [1] · software [1] · run_id {} · reasons [] · files_sha256 [1]) → "
            "그 시드 invalid · 요약이 죽지 않고 invalid 로 이전 stage1_pass 파일을 덮는다 · 요약 중 예외가 나도 invalid 요약 (fail-closed) "
            f"({ {k: v for k, v in sm_res.items() if v != (True, 'invalid', 'invalid', 'invalid')} } · {rx_['track']} · {fx_.get('error')})")
        # ⭐ DP 전 리뷰 (둘째) F3 — 요약 쓰기 실패 (임시 자리가 디렉터리) · 신호 (KeyboardInterrupt) 도 fail-closed: 이전 통과 요약을 안 남긴다
        rs_w = pathlib.Path(td_) / "_sum_write_fail"; (rs_w / "A").mkdir(parents=True)
        (rs_w / "stage1_summary.json").write_text(json.dumps({"track": "stage1_pass"}), encoding="utf-8")
        (rs_w / "stage1_summary.json.tmp").mkdir()
        try:
            stage1_summary(rs_w, values=VAL, log=lambda *a: None); w_raised = False
        except OSError:
            w_raised = True
        w_gone = not (rs_w / "stage1_summary.json").exists() and (rs_w / "stage1_summary.json.tmp").is_dir()
        rs_k = pathlib.Path(td_) / "_sum_signal"; (rs_k / "A").mkdir(parents=True)
        (rs_k / "stage1_summary.json").write_text(json.dumps({"track": "stage1_pass"}), encoding="utf-8")
        _core0 = globals()["_stage1_summary_core"]
        def _core_ki(*a_, **k_):
            raise KeyboardInterrupt("selftest 신호")
        globals()["_stage1_summary_core"] = _core_ki
        try:
            stage1_summary(rs_k, values=VAL, log=lambda *a: None); k_raised = False
        except KeyboardInterrupt:
            k_raised = True
        finally:
            globals()["_stage1_summary_core"] = _core0
        k_after = json.loads((rs_k / "stage1_summary.json").read_text(encoding="utf-8"))
        chk(w_raised and w_gone and k_raised and k_after.get("track") == "invalid" and not (rs_k / "stage1_summary.json.tmp").exists(),
            "⛔음성 DP 전 리뷰 (둘째) F3: 요약 쓰기가 실패하면 (임시 자리가 디렉터리) 이전 stage1_pass 를 지우고 예외를 다시 던진다 (남의 임시 자리는 안 지운다) · "
            f"요약 중 신호 (KeyboardInterrupt) 면 invalid 요약을 쓰고 다시 던진다 ({w_raised} · {w_gone} · {k_raised} · {k_after.get('track')})")
        # ⭐ DP 전 리뷰 (둘째) F2 — 판정 임시 파일이 남았으면 판정을 쓰지 않는다 (임시 · 현재 · 이력 그대로)
        rv_ = pathlib.Path(td_) / "_verdict_tmp_left"; rv_.mkdir()
        (rv_ / "stage1_verdict.json.tmp").write_text('{"status": "pass"}', encoding="utf-8")
        (rv_ / "stage1_verdict.json").write_text('{"status": "incomplete"}', encoding="utf-8")
        vt_ = stage1_verdict(rv_, values=VAL, log=lambda *a: None)
        chk(vt_["status"] == "invalid" and vt_.get("written") is False
            and (rv_ / "stage1_verdict.json.tmp").read_text(encoding="utf-8") == '{"status": "pass"}'
            and (rv_ / "stage1_verdict.json").read_text(encoding="utf-8") == '{"status": "incomplete"}' and not (rv_ / VERDICT_HISTORY).exists(),
            f"⛔음성 DP 전 리뷰 (둘째) F2: 판정 임시 파일이 남은 폴더는 다시 판정해도 아무것도 안 쓴다 (앞 쓰기의 흔적을 덮지 않는다) ({vt_['status']})")
        # ⭐ 회신 DP P2-2 — 직접 진입 엄격 판독: 카드 기계_판독_값 · G4 밴드 카드 · gate_check · seed_gate 의 plan 에 같은 열쇠 둘 (마지막 값이 정본이어도) = 거부
        def _raises_dup(fn_):
            try:
                fn_(); return False
            except ValueError as e_:
                return "같은 열쇠" in str(e_)
        card_t = LI2S2_CARD.read_text(encoding="utf-8") if hasattr(LI2S2_CARD, "read_text") else pathlib.Path(LI2S2_CARD).read_text(encoding="utf-8")
        cdup_ = pathlib.Path(td_) / "_card_dup.json"
        cdup_.write_text(card_t.replace('"기계_판독_값": ', '"기계_판독_값": {"x": 1}, "기계_판독_값": ', 1), encoding="utf-8")
        band_q = pathlib.Path(BAND_CARD) if pathlib.Path(BAND_CARD).exists() else pathlib.Path(__file__).resolve().parents[2] / BAND_CARD
        bdup_ = pathlib.Path(td_) / "_band_dup.json"
        bdup_.write_text(band_q.read_text(encoding="utf-8").replace(f'"{BAND_PATH[0]}": ', f'"{BAND_PATH[0]}": {{"x": 1}}, "{BAND_PATH[0]}": ', 1), encoding="utf-8")
        gdup_ = pathlib.Path(td_) / "_gate_plan_dup"; gdup_.mkdir()
        (gdup_ / "plan.json").write_text('{"melt_ps": 100.0, "melt_ps": 1.0}', encoding="utf-8")
        dd_ = {"card": _raises_dup(lambda: read_li2s2_values(cdup_)), "band": _raises_dup(lambda: read_band(bdup_)),
               "gate_check": _raises_dup(lambda: gate_check(gdup_, log=lambda *a: None)),
               "seed_gate": _raises_dup(lambda: seed_gate(gdup_, write_raw=False, log=lambda *a: None))}
        chk(all(dd_.values()) and card_t.count('"기계_판독_값"') == 1,
            f"⛔음성 회신 DP P2-2: 직접 진입에서도 같은 열쇠 둘을 받지 않는다 — 카드 기계_판독_값 · G4 밴드 카드 · gate_check · seed_gate 의 plan ({dd_})")
        # ⭐ DP 깨기 DP18 (살아남음) — 판정의 plan 읽기도 같은 열쇠 둘 = 못 읽음 (마지막 값으로 판정하지 않는다)
        rp_ = pathlib.Path(td_) / "_verdict_plan_dup"; rp_.mkdir()
        (rp_ / "plan.json").write_text('{"melt_ps": 100.0, "melt_ps": 1.0, "save_ps": 1.0}', encoding="utf-8")
        vp2_ = stage1_verdict(rp_, values=VAL, log=lambda *a: None)
        chk(vp2_["status"] == "incomplete" and any("plan.json 을 못 읽는다 (ValueError)" in x for x in (vp2_.get("reasons") or {}).get("incomplete", [])),
            "⛔음성 회신 DO P1 (판정): plan.json 에 같은 열쇠 둘이면 판정은 '못 읽음' (미완) — 마지막 값으로 판정하지 않는다 (깨기 DP18 이 드러낸 시험 구멍) "
            f"({vp2_['status']} · {(vp2_.get('reasons') or {}).get('incomplete')})")
        # ⭐ DP 전 리뷰 (둘째) — 못 읽은 이전 판정의 원문은 바이트 그대로 (UTF-8 아닌 바이트 포함)
        rb_ = pathlib.Path(td_) / "_verdict_raw_bytes"; rb_.mkdir()
        raw0 = b'{"status": "pass", "n": 130, "n": 71, "x": "\xff\xfe"}'
        (rb_ / "stage1_verdict.json").write_bytes(raw0)
        stage1_verdict(rb_, values=VAL, log=lambda *a: None, reason="selftest 원문 보존")
        h_rb = loads_strict((rb_ / VERDICT_HISTORY).read_text(encoding="utf-8").split("\n")[0])
        chk(base64.b64decode(((h_rb.get("prev") or {}).get("raw_b64")) or "") == raw0 and h_rb.get("prev_status") is None,
            "⛔음성 DP 전 리뷰 (둘째): 못 읽은 이전 판정 (같은 열쇠 둘 · UTF-8 아닌 바이트) 은 이력에 바이트 그대로 (raw_b64) · 상태 없음")
        # ⭐ DP 전 리뷰 (둘째) — 이력은 \n 으로만 나눈다 (글자 안의 U+2028 · U+2029 · U+0085 는 줄이 아니다)
        ru_ = pathlib.Path(td_) / "_hist_u2028"; ru_.mkdir()
        (ru_ / "stage1_verdict.json").write_text('{"status": "incomplete"}', encoding="utf-8")
        _append_history(ru_, {"status": "incomplete", "note": "a\u2028b\u2029c\u0085d", "provenance": {}},
                        {"status": "incomplete", "provenance": {}}, "sel\u2028ftest")
        recs_u, prob_u = _verdict_records(ru_)
        chk(prob_u is None and len(recs_u) == 3,
            f"⛔음성 DP 전 리뷰 (둘째): 이력 글자 안의 U+2028 · U+2029 · U+0085 에서 줄을 자르지 않는다 ({prob_u} · {len(recs_u)})")
        # ⭐ DP 전 리뷰 (둘째) — 소비자: 장부의 녹음 fail 실행을 다른 실행으로 대체 · stop_history 의 stop_id 둘
        rl_ = pathlib.Path(td_) / "_led_consumer"; rl_.mkdir()
        r1_, r2_ = "a" * 32, "b" * 32
        (rl_ / LEDGER_NAME).write_text(json.dumps({"runs": [
            {"system": "A", "seed": 12, "run_id": r1_, "end": "x", "wall_h": 1.0, "cost_basis": "measured", "status": "ended",
             "melt_check": {"verdict": "fail", "observed_in": "selftest"}},
            {"system": "A", "seed": 12, "run_id": r2_, "end": "x", "wall_h": 1.0, "cost_basis": "measured", "status": "ended"},
            {"system": "B", "seed": 13, "run_id": "c" * 32, "end": "x", "wall_h": 1.0, "cost_basis": "measured", "status": "ended",
             "melt_check": {"verdict": "fail"}, "melt_check_history": "x"}],
            "stop_history": [{"stop_id": "s1", "code": "resume"}, {"stop_id": "s1", "code": "invalid"}]}), encoding="utf-8")
        lc_ = ledger_check(rl_, {("A", 12): {"run_id": r2_, "status": "pass"}}, VAL)
        lc_inv = " | ".join(lc_["invalid"])
        chk("과학적 fail 실행을 다른 실행으로 대체했다" in lc_inv and "stop_id s1 가 둘" in lc_inv and "B13 런의 melt_check_history" in lc_inv,
            f"⛔음성 DP 전 리뷰 (둘째): 소비자 — 장부에 녹음 fail (판정 없이) 로 적힌 실행을 다른 실행으로 대체해도 잡는다 · 같은 stop_id 둘 · melt_check_history 가 목록이 아님 = invalid ({lc_inv[:300]})")
        # ⭐ DQ 전 리뷰 (독립 · 2026-11-05) — 러너와 같이 쓰는 함수를 직접: 같은 실행 충돌 규칙 · STOP 판독 · 이력 꼴 · 낡은 요약 표시
        FS0 = {f_: ("c" * 64 if f_ == "traj.xyz" else None) for f_ in BOUND_FILES}   # ⭐ 회신 DQ P1-1 — 판정이 읽는 파일 전부 · 판정 입력 칸 · 성격
        PV = {"files_sha256": FS0, "card_values_sha16": "1" * 16, "driver_sha16": "2" * 16, "band_sha16": "3" * 16, "runtime": {"python": "x"},
              "folder": ["A", "seed12"], "derived_written": [], "judge_nature": {"errors": ["seed_gate OSError: selftest"], "input_mismatch": []}}
        PV2 = {**PV, "files_sha256": {**FS0, "traj.xyz": "d" * 64}}
        cf_t = {"none_pass": ({}, "pass", True), "pass_pass": ({"verdict": "pass"}, "pass", True), "inv_pass": ({"verdict": "invalid"}, "pass", True),
                "inc_fail": ({"verdict": "incomplete"}, "fail", True), "PASS_none": ({"verdict": "PASS"}, None, True),
                "fail_pass": ({"verdict": "fail", "verdict_provenance": PV}, "pass", True),
                "melt_pass": ({"melt_check": {"verdict": "fail"}}, "pass", True), "melt_fail": ({"melt_check": {"verdict": "fail"}}, "fail", True),
                "pass_incomplete": ({"verdict": "pass"}, "incomplete", True),
                "rec_on": ({"verdict_observed_conflict": [{"status": "fail"}]}, None, True),
                "rec_off": ({"verdict_observed_conflict": [{"status": "fail"}]}, None, False)}
        got_cf = {k_: ledger_verdict_conflict(r_, f_, recorded=rc_, folder_provenance=PV) is not None for k_, (r_, f_, rc_) in cf_t.items()}
        got_cf.update({"inv_same_prov": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV) is not None,
                       "inc_same_prov": ledger_verdict_conflict({"verdict": "incomplete", "verdict_provenance": PV}, "fail", folder_provenance=PV) is not None,
                       "inv_prov_diff": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV2) is not None,
                       "inv_prov_nocard": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": {**PV, "card_values_sha16": None}}, "pass",
                                                                  folder_provenance={**PV, "card_values_sha16": None}) is not None,
                       "inv_folder_noprov": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=None) is not None,
                       "none_prior_flip": ledger_verdict_conflict({}, "pass", folder_provenance=PV, folder_prior=[{"status": "fail", "provenance": PV}]) is not None,
                       "none_prior_same_sci": ledger_verdict_conflict({}, "pass", folder_provenance=PV, folder_prior=[{"status": "pass", "provenance": PV2}]) is not None,
                       "none_prior_nonsci_changed": ledger_verdict_conflict({}, "pass", folder_provenance=PV, folder_prior=[{"status": "invalid", "provenance": PV2}]) is not None,
                       "none_prior_nonsci_driver": ledger_verdict_conflict({}, "fail", folder_provenance=PV,
                                                                           folder_prior=[{"status": "incomplete", "provenance": {**PV, "driver_sha16": "9" * 16}}]) is not None,
                       "none_prior_nonsci_same": ledger_verdict_conflict({}, "pass", folder_provenance=PV, folder_prior=[{"status": "invalid", "provenance": PV}]) is not None,
                       "none_prior_noprov": ledger_verdict_conflict({}, "pass", folder_provenance=PV, folder_prior=[{"status": "invalid"}]) is not None,
                       "none_prior_unreadable": ledger_verdict_conflict({}, "pass", folder_provenance=PV, folder_prior=[{"status": None}]) is not None,
                       "none_prior_unknown": ledger_verdict_conflict({}, "pass", folder_provenance=PV, folder_prior=[{"status": "garbage", "provenance": PV}]) is not None,
                       "none_prior_multi_step": ledger_verdict_conflict({}, "pass", folder_provenance=PV2, folder_prior=[{"status": "fail", "provenance": PV},
                                                                        {"status": "pass", "provenance": PV2}, {"status": "pass", "provenance": PV2}]) is not None,
                       "none_prior_all_same": ledger_verdict_conflict({}, "pass", folder_provenance=PV, folder_prior=[{"status": "invalid", "provenance": PV},
                                                                      {"status": "pass", "provenance": PV}, {"status": "pass", "provenance": PV}]) is not None,
                       "set_ledger_ignores_prior": ledger_verdict_conflict({"verdict": "pass"}, "pass", folder_provenance=PV,
                                                                           folder_prior=[{"status": "fail", "provenance": PV}]) is not None})
        RAW_ = JUDGE_DERIVED_FILES[0]                        # ⭐ 회신 DQ P1-1 — 입력 복구 · 성격 · 판정 입력 칸 (음성) 과 처음 만듦 (양성)
        def _inv(prior_, new_):
            return ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": prior_}, "pass", folder_provenance=new_) is not None
        PVM = {**PV, "judge_nature": {"errors": [], "input_mismatch": [f"{RAW_} 불일치 (selftest)"]}}
        PVR_old = {**PV, "files_sha256": {**FS0, RAW_: "e" * 64}}
        PVMID = {"status": "incomplete", "provenance": {**PV, "files_sha256": {**FS0, "traj.xyz": "9" * 64},
                                                        "judge_nature": {"errors": [], "input_mismatch": []}}}   # 실행 중 들여다본 판정
        PVDET = {"status": "invalid", "provenance": {**PV, "files_sha256": {**FS0, "final.xyz": "8" * 64},
                                                     "judge_nature": {"errors": [], "input_mismatch": []}}}     # 입력이 바뀐 채 낸 결정적 invalid (그 뒤 되돌림)
        PVR_new = {**PV, "files_sha256": {**FS0, RAW_: "f" * 64}, "derived_written": [RAW_]}
        PVR_first = {**PV, "files_sha256": {**FS0, RAW_: "f" * 64}, "derived_written": [RAW_]}
        PVR_other = {**PV, "files_sha256": {**FS0, RAW_: "f" * 64}, "derived_written": []}
        got_dq = {"inv_mismatch": _inv(PVM, PV), "inv_mismatch_and_err": _inv({**PVM, "judge_nature": {"errors": ["x"], "input_mismatch": ["y"]}}, PV),
                  "inv_noerr": _inv({**PV, "judge_nature": {"errors": [], "input_mismatch": []}}, PV),
                  "inv_nonature": _inv({k_: v_ for k_, v_ in PV.items() if k_ != "judge_nature"}, PV),
                  "inv_nature_badshape": _inv({**PV, "judge_nature": {"errors": "x", "input_mismatch": []}}, PV),
                  "inv_raw_repaired": _inv(PVR_old, PVR_new), "inv_raw_gone": _inv(PVR_old, PV),
                  "inv_raw_first_made": _inv(PV, PVR_first), "inv_raw_first_other": _inv(PV, PVR_other),   # DR 전 리뷰 P2-A — 중간 판정 · 사람이 만든 것도
                  "inv_raw_same": _inv(PVR_old, {**PVR_old, "derived_written": []}),
                  "inv_band": _inv(PV, {**PV, "band_sha16": "4" * 16}), "inv_band_none": _inv({**PV, "band_sha16": None}, {**PV, "band_sha16": None}),
                  "inv_band_notread": _inv({**PV, "band_sha16": BAND_NOT_READ}, {**PV, "band_sha16": BAND_NOT_READ}),
                  "inv_band_read_vs_not": _inv({**PV, "band_sha16": BAND_NOT_READ}, PV),
                  "inv_folder": _inv(PV, {**PV, "folder": ["A", "seed12.moved"]}), "inv_folder_none": _inv({**PV, "folder": None}, {**PV, "folder": None}),
                  "inv_runtime": _inv(PV, {**PV, "runtime": {"python": "y"}}),
                  "inv_attempt": _inv(PV, {**PV, "files_sha256": {**FS0, ATTEMPT_NAME: "a" * 64}}),
                  "inv_oldfmt": _inv({**PV, "files_sha256": {"traj.xyz": "c" * 64}}, {**PV, "files_sha256": {"traj.xyz": "c" * 64}}),
                  "chain_mismatch": ledger_verdict_conflict({}, "pass", folder_provenance=PV, folder_prior=[{"status": "invalid", "provenance": PVM}]) is not None,
                  "chain_raw_repaired": ledger_verdict_conflict({}, "pass", folder_provenance=PVR_new,
                                                                folder_prior=[{"status": "invalid", "provenance": PVR_old}]) is not None,
                  # ⭐ DR 전 2차 리뷰 P1 — 장부 판정이 비과학적이어도 폴더 판정 기록 전체를 본다 (그 사이 입력 불일치 · 다른 과학적 판정)
                  "inv_ledger_chain_mismatch": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                       folder_prior=[{"status": "invalid", "provenance": PV},
                                                                                     {"status": "invalid", "provenance": PVM},
                                                                                     {"status": "pass", "provenance": PV}]) is not None,
                  "inv_ledger_chain_fail": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                   folder_prior=[{"status": "invalid", "provenance": PV}, {"status": "fail", "provenance": PV},
                                                                                 {"status": "pass", "provenance": PV}]) is not None,
                  "inv_ledger_chain_ok": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                 folder_prior=[{"status": "invalid", "provenance": PV}, {"status": "pass", "provenance": PV}]) is not None,
                  "inc_ledger_chain_unreadable": ledger_verdict_conflict({"verdict": "incomplete", "verdict_provenance": PV}, "fail", folder_provenance=PV,
                                                                         folder_prior=[{"status": None}]) is not None,
                  "sci_ledger_ignores_chain": ledger_verdict_conflict({"verdict": "pass", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                      folder_prior=[{"status": "invalid", "provenance": PVM}]) is not None,
                  # ⭐ DR 전 3차 리뷰 P3 — 장부 판정이 비과학적이면 폴더 기록의 앞선 incomplete (실행 중 들여다봄 · 예외 없음 · 다른 원자료) 는 막지 않는다 ·
                  #    장부가 비면 그대로 엄격 · 성격을 모르는 기록은 막는다
                  "inv_ledger_chain_midrun": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                     folder_prior=[PVMID, {"status": "invalid", "provenance": PV},
                                                                                   {"status": "pass", "provenance": PV}]) is not None,
                  "none_ledger_chain_midrun": ledger_verdict_conflict({}, "pass", folder_provenance=PV,
                                                                      folder_prior=[PVMID, {"status": "invalid", "provenance": PV},
                                                                                    {"status": "pass", "provenance": PV}]) is not None,
                  "inv_ledger_chain_nonature": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                       folder_prior=[{"status": "incomplete", "provenance": {"files_sha256": FS0}},
                                                                                     {"status": "pass", "provenance": PV}]) is not None,
                  # ⭐ DR 전 4차 리뷰 P1 — 순서: 장부 판정 자신의 기록 뒤의 비과학적 기록은 하나하나 대체 규칙 (되돌린 입력 변경 · 결정적 invalid → 보류) ·
                  #    그 뒤의 일시 오류 (같은 입력) 는 대체 · 장부 기록을 못 찾으면 전부 대체 규칙
                  "inv_after_det_invalid": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                   folder_prior=[{"status": "invalid", "provenance": PV}, PVDET,
                                                                                 {"status": "pass", "provenance": PV}]) is not None,
                  "inv_after_transient": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                 folder_prior=[{"status": "invalid", "provenance": PV},
                                                                               {"status": "invalid", "provenance": {**PV, "judge_nature": {"errors": ["again"], "input_mismatch": []}}},
                                                                               {"status": "pass", "provenance": PV}]) is not None,
                  "inv_anchor_missing": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                folder_prior=[PVMID, {"status": "pass", "provenance": PV}]) is not None,
                  "inv_det_before_anchor": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                   folder_prior=[PVDET, {"status": "invalid", "provenance": PV},
                                                                                 {"status": "pass", "provenance": PV}]) is not None,
                  # ⭐ DR 전 6차 리뷰 P2 — 자동 대체도 판정 규칙 지문으로: 그 사이 상한만 올린 카드 (카드 값 다름 · 판정 규칙 같음) 는 같은 입력 · 판정 규칙이 다르면 충돌
                  "inv_cap_raised": _inv({**PV, "judge_values_sha16": "7" * 16}, {**PV, "card_values_sha16": "6" * 16, "judge_values_sha16": "7" * 16}),
                  "inv_rules_differ": _inv({**PV, "judge_values_sha16": "7" * 16}, {**PV, "judge_values_sha16": "5" * 16}),
                  "inv_old_rec_card": _inv(PV, {**PV, "card_values_sha16": "6" * 16, "judge_values_sha16": "7" * 16}),
                  "inv_anchor_first": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                  folder_prior=[{"status": "invalid", "provenance": PV}, PVDET, {"status": "invalid", "provenance": PV},
                                                                                {"status": "pass", "provenance": PV}]) is not None,
                  # ⭐ 회신 DR P1-1 — 장부 판정 자신의 기록 **앞** 이어도 완료된 invalid (입력 불일치 · 결정적) 는 대체 규칙 · 입력 불일치는 앞뒤 무관 보류 ·
                  #    진행 중 incomplete (입력 불일치 없음 · 옛 꼴) 만 막지 않는다 · 앞의 일시 오류 (같은 입력) 는 대체
                  "inv_mismatch_before_anchor": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                        folder_prior=[{"status": "invalid", "provenance": PVM}, {"status": "invalid", "provenance": PV},
                                                                                      {"status": "pass", "provenance": PV}]) is not None,
                  "inc_mismatch_before_anchor": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                        folder_prior=[{"status": "incomplete", "provenance": {**PVMID["provenance"], "judge_nature": {
                                                                            "errors": [], "input_mismatch": ["y"]}}},
                                                                                      {"status": "invalid", "provenance": PV}, {"status": "pass", "provenance": PV}]) is not None,
                  "inv_transient_before_anchor": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                         folder_prior=[{"status": "invalid", "provenance": {**PV, "judge_nature": {"errors": ["once"],
                                                                                                                                                     "input_mismatch": []}}},
                                                                                       {"status": "invalid", "provenance": PV}, {"status": "pass", "provenance": PV}]) is not None,
                  "inc_oldfmt_before_anchor": ledger_verdict_conflict({"verdict": "invalid", "verdict_provenance": PV}, "pass", folder_provenance=PV,
                                                                      folder_prior=[{"status": "incomplete", "provenance": {k_: v_ for k_, v_ in PVMID["provenance"].items()
                                                                                                                             if k_ != "judge_nature"}},
                                                                                    {"status": "invalid", "provenance": PV}, {"status": "pass", "provenance": PV}]) is not None,
                  # ⭐ 회신 DR P1-2 — 파생 파일 생성 예외는 진짜 부재 → 정상 파일만 (디렉터리를 치운 복구 · 링크 · 특수 파일은 다르다)
                  "inv_raw_dir_repaired": _inv({**PV, "files_sha256": {**FS0, RAW_: "nonfile:dir"}}, PVR_first),
                  "inv_raw_link_made": _inv(PV, {**PV, "files_sha256": {**FS0, RAW_: "link:" + "f" * 64}}),
                  "inv_raw_nonfile_made": _inv(PV, {**PV, "files_sha256": {**FS0, RAW_: "nonfile:other"}}),
                  "inv_raw_dir_same": _inv({**PV, "files_sha256": {**FS0, RAW_: "nonfile:dir"}}, {**PV, "files_sha256": {**FS0, RAW_: "nonfile:dir"}})}
        want_dq = {"inv_mismatch": True, "inv_mismatch_and_err": True, "inv_noerr": True, "inv_nonature": True, "inv_nature_badshape": True,
                   "inv_raw_repaired": True, "inv_raw_gone": True, "inv_raw_first_made": False, "inv_raw_first_other": False, "inv_raw_same": False,
                   "inv_band": True, "inv_band_none": True, "inv_band_notread": False, "inv_band_read_vs_not": True,
                   "inv_folder": True, "inv_folder_none": True, "inv_runtime": True, "inv_attempt": True, "inv_oldfmt": True,
                   "chain_mismatch": True, "chain_raw_repaired": True, "inv_ledger_chain_mismatch": True, "inv_ledger_chain_fail": True,
                   "inv_ledger_chain_ok": False, "inc_ledger_chain_unreadable": True, "sci_ledger_ignores_chain": False,
                   "inv_ledger_chain_midrun": False, "none_ledger_chain_midrun": True, "inv_ledger_chain_nonature": True,
                   "inv_after_det_invalid": True, "inv_after_transient": False, "inv_anchor_missing": True, "inv_det_before_anchor": True,   # 회신 DR P1-1 (앞이어도 완료된 invalid)
                   "inv_anchor_first": True, "inv_cap_raised": False, "inv_rules_differ": True, "inv_old_rec_card": True,
                   "inv_mismatch_before_anchor": True, "inc_mismatch_before_anchor": True, "inv_transient_before_anchor": False,
                   "inc_oldfmt_before_anchor": False, "inv_raw_dir_repaired": True, "inv_raw_link_made": True, "inv_raw_nonfile_made": True,
                   "inv_raw_dir_same": False}   # DR 전 5차 — 같은 바이트의 판정이 뒤에 또 있어도 기준은 첫 기록 (그 사이 결정적 invalid → 충돌)
        chk(got_dq == want_dq and JUDGE_DERIVED_FILES == (SEED_GATE_RAW,) and set(PROVENANCE_FILES) < set(BOUND_FILES),
            "⛔음성 회신 DQ P1-1: 자동 대체는 판정이 읽은 입력 전부 (원자료 · md_init_raw.xyz · 실행 전 기록 · G4 밴드 카드 · 카드 값 · 도구 · 실행 환경) 가 "
            "같고 앞 판정이 판정 도중 예외 (입력 불일치 없음) 일 때만 — 다른 md_init_raw.xyz 를 옮기고 다시 만든 것 · 입력 불일치 판정 · 성격 기록 없음 · "
            "(DR 전 2차) 장부 판정이 비과학적이어도 폴더 기록 사이의 입력 불일치 · 다른 과학적 판정 · 못 읽는 판정은 충돌 (장부 판정이 과학적이면 장부 우선 — Q5) · "
            "밴드 · 환경 · 실행 전 기록 · 폴더 이름 다름 · 옛 꼴 지문은 충돌 · 앞에 없던 파생 파일이 지금 있으면 (누가 만들었든) 같다 · 둘 다 밴드를 안 읽었으면 같다 "
            f"({ {k_: v_ for k_, v_ in got_dq.items() if v_ != want_dq[k_]} })")
        # ⭐ 회신 DR P1-2 — 경로 상태: 없음 · 정상 파일 · 파일을 가리키는 링크 (내용 지문) · 디렉터리 · 깨진 링크 · 디렉터리 링크 · 특수 파일을 가른다
        #    (링크 · FIFO 를 못 만드는 OS 면 그 하위 항목만 빠진다 — 시험 수는 같다) · 지문 칸 값의 꼴 (link: · nonfile: 도 알려진 값) · 완료 필드 검사가 받는다
        import tempfile as _tf_ps, shutil as _sh_ps
        ps_root = pathlib.Path(_tf_ps.mkdtemp())
        try:
            (ps_root / "f").write_text("abc", encoding="utf-8"); (ps_root / "d").mkdir()
            got_ps = {"absent": path_state(ps_root / "x"), "file": path_state(ps_root / "f"), "dir": path_state(ps_root / "d")}
            want_ps = {"absent": None, "file": _sha256_file(ps_root / "f"), "dir": "nonfile:dir"}
            try:
                os.symlink(ps_root / "f", ps_root / "lf"); os.symlink(ps_root / "nowhere", ps_root / "lb"); os.symlink(ps_root / "d", ps_root / "ld")
                got_ps.update(link_file=path_state(ps_root / "lf"), link_broken=path_state(ps_root / "lb"), link_dir=path_state(ps_root / "ld"))
                want_ps.update(link_file="link:" + _sha256_file(ps_root / "f"), link_broken="nonfile:symlink", link_dir="nonfile:symlink")
            except (OSError, NotImplementedError, AttributeError):
                pass
            if hasattr(os, "mkfifo"):
                os.mkfifo(ps_root / "p"); got_ps["fifo"] = path_state(ps_root / "p"); want_ps["fifo"] = "nonfile:other"
            okv_ = [None, "a" * 64, "link:" + "b" * 64, *NONFILE_STATES]
            badv_ = ["", "nonfile:x", "link:abc", "A" * 64, 123, ["x"]]
            cf_ok = _completion_fields_problem({"provenance": {"files_sha256": {"final.xyz": "nonfile:dir", "result.json": "link:" + "c" * 64}}}, True, "t")
            cf_bad = _completion_fields_problem({"provenance": {"files_sha256": {"final.xyz": "nonfile:x"}}}, True, "t")
            chk(got_ps == want_ps and all(path_state_problem(v_) is None for v_ in okv_) and all(path_state_problem(v_) for v_ in badv_)
                and cf_ok is None and bool(cf_bad) and run_provenance(ps_root)[SEED_GATE_RAW] is None,
                "⛔음성 회신 DR P1-2: 경로 상태 — 없음 None · 정상 파일 sha256 · 디렉터리 nonfile:dir · 파일 링크 link:+내용 지문 · 깨진 링크 · 디렉터리 링크 "
                "nonfile:symlink · FIFO nonfile:other (진짜 부재와 '있는데 파일 아님' 을 같은 None 으로 접지 않는다) · 지문 칸 값 꼴 · 완료 필드 검사가 경로 "
                f"상태를 받는다 ({ {k_: (got_ps.get(k_), want_ps.get(k_)) for k_ in set(got_ps) | set(want_ps) if got_ps.get(k_) != want_ps.get(k_)} } · "
                f"{[v_ for v_ in okv_ if path_state_problem(v_)]} · {[v_ for v_ in badv_ if not path_state_problem(v_)]} · {cf_ok} · {cf_bad})")
        finally:
            _sh_ps.rmtree(ps_root, ignore_errors=True)
        # ⭐ 회신 DQ P1-1 — 진짜 판정 함수가 성격 · 처음 만듦을 적는가 (입력 불일치 = input_mismatch · 판정 도중 예외 = errors) · 그 기록으로 대체 규칙이 가르는가
        from ase.io import read as _rd_dq, write as _wr_dq
        _u3 = 2.05 / math.sqrt(3.0)                         # P–S 사면체 하나 + Li (seed_gate 의 PS₄ 판독이 서는 최소 구조 — FR 의 Li 둘은 seed_gate 로그에서 KeyError)
        _lps = [("P", 5, 5, 5)] + [("S", 5 + _u3 * a_, 5 + _u3 * b_, 5 + _u3 * c_) for a_, b_, c_ in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))] \
            + [("Li", 1, 1, 1), ("Li", 8, 2, 3), ("Li", 2, 8, 7)]
        _lps_fr = f"{len(_lps)}\nLattice=\"10 0 0 0 10 0 0 0 10\"\n" + "".join(f"{e_} {x_:.6f} {y_:.6f} {z_:.6f}\n" for e_, x_, y_, z_ in _lps)
        def _dq_run(nm_):
            _fs(nm_, traj=5)
            d_ = pathlib.Path(td_) / nm_
            (d_ / "traj.xyz").write_text(_lps_fr * 5, encoding="utf-8")
            _wr_dq(str(d_ / "final.xyz"), _rd_dq(str(d_ / "traj.xyz"), index=-1))
            return d_
        def _jv(d_, why_):
            return stage1_verdict(d_, values=VAL, log=lambda *a: None, reason=f"selftest DQ P1-1 {why_}")
        RAWN = SEED_GATE_RAW
        d_mm = _dq_run("dq_mm")
        v_mm1 = _jv(d_mm, "첫 판정")                         # 파생 파일을 처음 만든다
        raw_sha1 = (v_mm1["provenance"]["files_sha256"] or {}).get(RAWN)
        from ase.io import read as _rd2
        at_ = _rd2(str(d_mm / RAWN)); at_.positions[0] += 0.5   # 다른 좌표의 md_init_raw.xyz (회신 DQ P1-1 재현 1)
        _wr_dq(str(d_mm / RAWN), at_, format="extxyz")
        v_mm2 = _jv(d_mm, "불일치")
        (d_mm / RAWN).rename(d_mm / (RAWN + ".kept"))       # 재현 2 — 다른 이름으로 보존
        v_mm3 = _jv(d_mm, "다시 만듦")                        # 재현 3 — 다시 생긴다
        nat1, nat2, nat3 = (x_["provenance"]["judge_nature"] for x_ in (v_mm1, v_mm2, v_mm3))
        _sg0_dq = globals()["seed_gate"]
        n_dq = {"left": 1}
        def _sg_once(run_, *a_, **k_):
            if n_dq["left"]:
                n_dq["left"] -= 1
                raise OSError("selftest — 판정 도중 일시 오류")
            return _sg0_dq(run_, *a_, **k_)
        d_tr = _dq_run("dq_tr")
        globals()["seed_gate"] = _sg_once
        try:
            v_tr1 = _jv(d_tr, "일시 오류")                    # 파생 파일을 만들기 전 예외
        finally:
            globals()["seed_gate"] = _sg0_dq
        v_tr2 = _jv(d_tr, "다시")
        v_tr3 = _jv(d_tr, "한 번 더 (중간 판정 뒤)")             # ⭐ DR 전 리뷰 P2-A — 파생 파일을 앞 판정이 만들었어도
        d_tg = _dq_run("dq_tg")                              # ⭐ DR 전 리뷰 P2-A (FH5) — 일시 오류 뒤 사람이 --seed_gate (파생 파일을 씀) 로 들여다보고 다시 판정
        n_dq["left"] = 1
        globals()["seed_gate"] = _sg_once
        try:
            v_tg1 = _jv(d_tg, "일시 오류")
        finally:
            globals()["seed_gate"] = _sg0_dq
        seed_gate(d_tg, write_raw=True, log=lambda *a: None)
        v_tg2 = _jv(d_tg, "사람이 --seed_gate 뒤")
        _fsc0 = globals()["final_structure_check"]
        def _fsc_err(*a_, **k_):
            return {"ok": False, "why": ["selftest"], "judge_errors": ["final.xyz 읽기 OSError: selftest"]}
        d_ta = _dq_run("dq_ta")
        globals()["final_structure_check"] = _fsc_err
        try:
            v_ta1 = _jv(d_ta, "파생을 만든 뒤 예외")
        finally:
            globals()["final_structure_check"] = _fsc0
        v_ta2 = _jv(d_ta, "다시")
        sb_ = {"mm_repair": supersede_block(v_mm2["provenance"], v_mm3["provenance"]),
               "mm_first_vs_mm3": supersede_block(v_mm1["provenance"], v_mm3["provenance"]),
               "tr": supersede_block(v_tr1["provenance"], v_tr2["provenance"]), "ta": supersede_block(v_ta1["provenance"], v_ta2["provenance"])}
        chk(raw_sha1 and v_mm1["provenance"]["derived_written"] == [RAWN] and nat1["input_mismatch"] == []
            and v_mm2["status"] == "invalid" and nat2["input_mismatch"] and not any("seed_gate" in e_ for e_ in nat2["errors"])
            and v_mm2["provenance"]["files_sha256"][RAWN] not in (None, raw_sha1) and v_mm2["provenance"]["derived_written"] == []
            and v_mm3["provenance"]["derived_written"] == [RAWN] and v_mm3["provenance"]["files_sha256"][RAWN] == raw_sha1 and not nat3["input_mismatch"]
            and v_mm1["provenance"]["band_sha16"] == band_card_sha16() and isinstance(v_mm1["provenance"]["runtime"].get("python"), str)
            and not os.path.lexists(d_mm / (RAWN + ".tmp"))
            and any("seed_gate OSError" in e_ for e_ in v_tr1["provenance"]["judge_nature"]["errors"])
            and v_tr1["provenance"]["files_sha256"][RAWN] is None and v_tr2["provenance"]["derived_written"] == [RAWN]
            and v_ta1["provenance"]["derived_written"] == [RAWN] and any("final.xyz 읽기" in e_ for e_ in v_ta1["provenance"]["judge_nature"]["errors"])
            and v_ta2["provenance"]["derived_written"] == [] and v_ta2["provenance"]["files_sha256"][RAWN] == v_ta1["provenance"]["files_sha256"][RAWN]
            and sb_["mm_repair"] is not None and "입력 불일치" in str(supersede_block(v_mm2["provenance"], v_mm2["provenance"]))
            and nat1["errors"] == [] and sb_["mm_first_vs_mm3"] is not None and "예외 없이" in sb_["mm_first_vs_mm3"]
            and sb_["tr"] is None and sb_["ta"] is None and v_tr1["provenance"]["judge_nature"]["errors"] == ["seed_gate OSError: selftest — 판정 도중 일시 오류"]
            and v_tr3["provenance"]["derived_written"] == [] and supersede_block(v_tr1["provenance"], v_tr3["provenance"]) is None
            and v_tg2["provenance"]["derived_written"] == [] and v_tg2["status"] == v_tr2["status"] and supersede_block(v_tg1["provenance"], v_tg2["provenance"]) is None
            and v_mm1["provenance"]["folder"] == [d_mm.parent.name, d_mm.name],
            "⛔음성 회신 DQ P1-1 (진짜 판정 함수): 다른 md_init_raw.xyz = 입력 불일치 (판정 도중 오류 아님) · 보존 뒤 다시 만든 판정으로 자동 대체 불가 · "
            "판정이 처음 만든 파생 파일은 derived_written (임시 파일 안 남김) · 지문에 G4 밴드 카드 · 실행 환경 · 일시 예외 (파생을 만들기 전 · 만든 뒤) "
            "의 재판정은 대체 가능 · (DR 전 리뷰 P2-A) 중간 판정 한 번 · 사람의 --seed_gate 뒤의 재판정도 대체 가능 "
            f"({sb_} · {nat2} · {v_tr1['provenance']['judge_nature']} · {v_ta1['provenance']['judge_nature']} · "
            f"{supersede_block(v_tr1['provenance'], v_tr3['provenance'])} · {supersede_block(v_tg1['provenance'], v_tg2['provenance'])})")
        # ⭐ 회신 DQ P1-1 — 묶는 범위 · 성격을 모으는 자리 하나씩 (보존 폴더의 실행 전 기록 · G4 밴드 카드 · 쓴 뒤 예외 · 파생 교체 실패 · 마지막 프레임 · 녹음 판독)
        (pathlib.Path(td_) / "_dqp" / "A").mkdir(parents=True)
        _fs("_dqp/A/seed11.dq", traj=5)
        d_pa = pathlib.Path(td_) / "_dqp" / "A" / "seed11.dq"
        v_pa = _jv(d_pa, "보존 폴더")
        pa_ok0 = provenance_current_problems(v_pa["provenance"], d_pa, VAL)
        (d_pa / ATTEMPT_NAME).write_text(json.dumps({"run_id": RIDF, "system": "A", "seed": 11}), encoding="utf-8")
        pa_bad = provenance_current_problems(v_pa["provenance"], d_pa, VAL)
        (d_pa / ATTEMPT_NAME).write_text("{not json", encoding="utf-8")
        v_pa2 = _jv(d_pa, "실행 전 기록 깨짐")
        bc_tmp = pathlib.Path(td_) / "_band_copy.json"
        bc_tmp.write_bytes(_band_card_path().read_bytes() + b" ")
        def _sg_after(run_, *a_, **k_):                      # 파생 파일을 쓴 **뒤** 예외
            _sg0_dq(run_, *a_, **k_)
            raise RuntimeError("selftest — 쓴 뒤 예외")
        d_sa = _dq_run("dq_sa")
        globals()["seed_gate"] = _sg_after
        try:
            v_sa = _jv(d_sa, "쓴 뒤 예외")
        finally:
            globals()["seed_gate"] = _sg0_dq
        import types as _ty_dq
        _os_dq = globals()["os"]
        osx_dq = _ty_dq.SimpleNamespace(**{k_: getattr(_os_dq, k_) for k_ in dir(_os_dq) if not k_.startswith("__")})
        def _rep_fail(src_, dst_):
            if str(dst_).endswith(SEED_GATE_RAW):
                raise OSError("selftest — 파생 교체 실패")
            return _os_dq.replace(src_, dst_)
        osx_dq.replace = _rep_fail
        d_rf = _dq_run("dq_rf")
        globals()["os"] = osx_dq
        try:
            v_rf1 = _jv(d_rf, "파생 교체 실패")
        finally:
            globals()["os"] = _os_dq
        rf_gone = not os.path.lexists(d_rf / SEED_GATE_RAW)
        v_rf2 = _jv(d_rf, "다시")
        import ase.io as _aio_dq
        _rd0 = _aio_dq.read
        def _rd_last_fail(f_, *a_, **k_):
            if str(f_).endswith("traj.xyz") and k_.get("index") == -1:
                raise OSError("selftest — 마지막 프레임 읽기 실패")
            return _rd0(f_, *a_, **k_)
        d_rl = _dq_run("dq_rl")
        _aio_dq.read = _rd_last_fail
        try:
            v_rl = _jv(d_rl, "마지막 프레임")
        finally:
            _aio_dq.read = _rd0
        _lf0 = globals()["_leading_frames"]
        globals()["_leading_frames"] = lambda *a_, **k_: ([], "OSError: selftest — 녹음 판독 실패")
        d_ml = _dq_run("dq_ml")                              # 녹음 판정이 traj 를 읽는 자리까지 가는 plan (고정 밀도 · 압축 0)
        (d_ml / "plan.json").write_text(json.dumps({**PLAN0, "fix_density_g_cm3": 1.2, "compress_ps": 0.0}), encoding="utf-8")
        try:
            v_ml = _jv(d_ml, "녹음 판독")
        finally:
            globals()["_leading_frames"] = _lf0
        er_ = lambda v_: v_["provenance"]["judge_nature"]["errors"]
        chk(ATTEMPT_NAME in v_pa["provenance"]["files_sha256"] and ATTEMPT_NAME not in v_mm1["provenance"]["files_sha256"] and pa_ok0 == [] and pa_bad
            and any("stage1_attempt.json 읽기" in e_ for e_ in er_(v_pa2)) and band_card_sha16(str(bc_tmp)) not in (None, band_card_sha16())
            and v_sa["provenance"]["derived_written"] == [SEED_GATE_RAW] and any("seed_gate RuntimeError" in e_ for e_ in er_(v_sa))
            and rf_gone and any("seed_gate OSError" in e_ for e_ in er_(v_rf1)) and v_rf1["provenance"]["files_sha256"][SEED_GATE_RAW] is None
            and v_rf2["provenance"]["derived_written"] == [SEED_GATE_RAW] and not os.path.lexists(d_rf / (SEED_GATE_RAW + ".tmp"))
            and supersede_block(v_rf1["provenance"], v_rf2["provenance"]) is None
            and any("traj 마지막 프레임 읽기" in e_ for e_ in er_(v_rl)) and any("melt_window_check read_stop" in e_ for e_ in er_(v_ml)),
            "⛔음성 회신 DQ P1-1 (묶는 범위 · 성격 수집): 보존 폴더만 실행 전 기록을 묶고 (바뀌면 지금과 안 맞음 · 깨지면 판정 도중 예외) · 현재 폴더는 안 묶는다 · "
            "G4 밴드 카드 바이트가 바뀌면 지문이 바뀐다 · seed_gate 가 쓴 뒤 예외여도 '처음 만듦' · 파생 교체가 실패하면 파생 파일이 안 남고 (임시 → 교체) "
            "다음 판정이 처음 만든다 (대체 가능) · 마지막 프레임 · 녹음 판독 예외도 판정 도중 예외로 모은다 "
            f"({pa_bad} · {er_(v_pa2)} · {er_(v_sa)} · {er_(v_rf1)} · {er_(v_rl)} · {er_(v_ml)})")
        d_fg = _dq_run("dq_fg"); (d_fg / "final.xyz").write_text("x", encoding="utf-8")     # final.xyz 를 못 읽는다 → 판정 도중 예외
        v_fg = _jv(d_fg, "final 못 읽음")
        _xf0 = globals()["_xyz_frames"]
        n_xf = {"left": 1}
        def _xf_once(*a_, **k_):                             # 녹음 판정의 프레임 세기만 한 번 OSError (판정 본문의 세기는 그대로)
            if n_xf["left"]:
                n_xf["left"] -= 1
                raise OSError("selftest — 프레임 세기 실패")
            return _xf0(*a_, **k_)
        d_io = _dq_run("dq_io")
        (d_io / "plan.json").write_text(json.dumps({**PLAN0, "fix_density_g_cm3": 1.2, "compress_ps": 0.0}), encoding="utf-8")
        globals()["_leading_frames"] = lambda *a_, **k_: ([], "OSError: selftest — 녹음 판독 실패")
        globals()["_xyz_frames"] = _xf_once
        try:
            v_io = _jv(d_io, "녹음 프레임 세기")
        finally:
            globals()["_leading_frames"], globals()["_xyz_frames"] = _lf0, _xf0
        d_hr = _dq_run("dq_hr")                              # 숨은 복구 — 다른 md_init_raw.xyz 가 있었는데 seed_gate 가 읽기 전 예외 → 사람이 지우고 다시 판정
        at_hr = _rd2(str(d_hr / "traj.xyz"), index=-1); at_hr.wrap(); at_hr.positions[0] += 0.5
        _wr_dq(str(d_hr / RAWN), at_hr, format="extxyz")
        n_dq["left"] = 1
        globals()["seed_gate"] = _sg_once
        try:
            v_hr1 = _jv(d_hr, "읽기 전 예외")
        finally:
            globals()["seed_gate"] = _sg0_dq
        (d_hr / RAWN).unlink()
        v_hr2 = _jv(d_hr, "지운 뒤")
        chk(any(e_.startswith("final.xyz 읽기") for e_ in er_(v_fg)) and any("melt_window_check io_error" in e_ for e_ in er_(v_io))
            and er_(v_hr1) == ["seed_gate OSError: selftest — 판정 도중 일시 오류"] and v_hr1["provenance"]["judge_nature"]["input_mismatch"] == []
            and v_hr1["provenance"]["files_sha256"][RAWN] not in (None, v_hr2["provenance"]["files_sha256"][RAWN])
            and supersede_block(v_hr1["provenance"], v_hr2["provenance"]) is not None,
            "⛔음성 회신 DQ P1-1 (성격 · 숨은 복구): 못 읽는 final.xyz · 녹음 판정의 프레임 세기 OSError 도 판정 도중 예외로 모은다 · 다른 md_init_raw.xyz 가 있던 채 "
            "seed_gate 가 읽기 전에 예외가 난 판정 (불일치를 못 찾음) 뒤 그 파일을 지우고 다시 만든 판정은 — 앞 판정이 판정 도중 예외여도 — 파생 파일 지문이 달라 "
            f"자동 대체 불가 ({er_(v_fg)} · {er_(v_io)} · {er_(v_hr1)} · {supersede_block(v_hr1['provenance'], v_hr2['provenance'])})")
        # ⭐ DR 전 리뷰 P3-B · P3-A — 밴드 카드는 판정이 읽었을 때만 묶는다 (li2s-2 고정 밀도 NVT 는 안 읽는다 — 작업 폴더 · 카드가 달라도 낡음이 아니다) ·
        #    폴더 이름은 판정 입력 (이름을 바꾸면 그 전 판정은 지금이 아니다)
        def _gc_nvt(*a_, **k_):                               # NVT 길처럼 밴드를 안 읽고 끝나는 gate_check
            return {"schedule_complete": None, "error": None, "thermo_columns_ok": True}
        d_nv = _dq_run("dq_nv")
        globals()["gate_check"] = _gc_nvt
        try:
            v_nv = _jv(d_nv, "밴드 안 읽음")
        finally:
            globals()["gate_check"] = _gc0
        _bcs0 = globals()["band_card_sha16"]
        globals()["band_card_sha16"] = lambda *a_, **k_: "f" * 16    # 지금 밴드 카드가 (다른 작업 폴더에서) 다르게 보인다
        try:
            nv_cur = provenance_current_problems(v_nv["provenance"], d_nv, VAL)
            rd_cur = provenance_current_problems(v_mm3["provenance"], d_mm, VAL)
        finally:
            globals()["band_card_sha16"] = _bcs0
        d_rn = d_mm.with_name("dq_mm.moved"); d_mm.rename(d_rn)
        rn_cur = provenance_current_problems(v_mm3["provenance"], d_rn, VAL)
        d_rn.rename(d_mm)
        chk(v_nv["provenance"]["band_sha16"] == BAND_NOT_READ and v_mm1["provenance"]["band_sha16"] == band_card_sha16() and nv_cur == []
            and any("G4 밴드" in x_ for x_ in rd_cur) and any("판정을 낸 폴더" in x_ for x_ in rn_cur)
            and provenance_current_problems(v_mm3["provenance"], d_mm, VAL) == [],
            "⛔음성 DR 전 리뷰 P3-B · P3-A: 밴드를 안 읽은 판정 (NVT 길) 은 밴드 지문을 not_read 로 적고 지금 밴드 카드와 대조하지 않는다 · 읽은 판정은 대조한다 · "
            f"폴더 이름을 바꾸면 그 전 판정은 지금이 아니다 ({nv_cur} · {rd_cur} · {rn_cur})")
        # ⭐ DR 전 리뷰 P2-B — 옆으로 옮긴 보존 폴더의 미해결 판정 기록도 막는다 (러너 시작 · 요약 장부 검사)
        rp_ = pathlib.Path(td_) / "_dq_pres"
        (rp_ / "A").mkdir(parents=True); (rp_ / "B").mkdir()
        (rp_ / "A" / "seed14.moved").mkdir(); (rp_ / "A" / "seed14.moved" / VERDICT_HISTORY).write_text('{"first": true, "new_status": "fail"}\n', encoding="utf-8")
        (rp_ / "B" / "seed13.cut1").mkdir(); (rp_ / "B" / "seed13.cut1" / "stage1_verdict.json").write_text('{"status": "pass"}', encoding="utf-8")
        (rp_ / "B" / "seed13.cut1" / "stage1_verdict.json.tmp").write_text('{"status": "fail"}', encoding="utf-8")
        (rp_ / "B" / "seed12.ok").mkdir(); (rp_ / "B" / "seed12.ok" / "stage1_verdict.json").write_text('{"status": "invalid"}', encoding="utf-8")
        (rp_ / "A" / "seed11").mkdir(); (rp_ / "A" / "seed11" / VERDICT_HISTORY).write_text("", encoding="utf-8")   # 현재 폴더는 이 함수가 안 본다
        (rp_ / "B" / "old14").mkdir(); (rp_ / "B" / "old14" / VERDICT_HISTORY).write_text('{"first": true, "new_status": "fail"}\n', encoding="utf-8")
        (rp_ / "B" / "seed15_moved").mkdir(); (rp_ / "B" / "seed15_moved" / "stage1_verdict.json").write_text('{"status": "PASS"}', encoding="utf-8")
        (rp_ / "A" / "seed12-old").mkdir(); (rp_ / "A" / "seed12-old" / "stage1_verdict.json").write_text('{"status": "pass"}', encoding="utf-8")
        (rp_ / "A" / "seed12-old" / VERDICT_HISTORY).write_text('{"prev": {"status": null, "raw_b64": ""}, "new_status": "pass"}\n', encoding="utf-8")
        (rp_ / "A" / "notes").mkdir()                        # 판정 기록이 없는 폴더는 미해결이 아니다
        pu_ = preserved_unresolved(rp_, VAL["seeds"])
        (rp_ / LEDGER_NAME).write_text(json.dumps({"runs": [], "stop_history": [], "card_values_sha16": values_sha16(VAL), "driver_sha16": driver_sha16()}),
                                       encoding="utf-8")
        lc_pu = " | ".join(ledger_check(rp_, {}, VAL)["invalid"])
        chk(sorted(((s_, sd_, nm_) for s_, sd_, nm_, _ in pu_), key=lambda x_: (x_[0], x_[2]))
            == [("A", 12, "seed12-old"), ("A", 14, "seed14.moved"), ("B", None, "old14"), ("B", 13, "seed13.cut1"), ("B", 15, "seed15_moved")]
            and "보존 폴더 A/seed14.moved" in lc_pu and "보존 폴더 B/seed13.cut1" in lc_pu and "보존 폴더 B/old14" in lc_pu and "seed12.ok" not in lc_pu
            and "notes" not in lc_pu and folder_record_problem(rp_ / "B" / "seed12.ok") is None,
            "⛔음성 DR 전 리뷰 P2-B · 2차: 현재 시드 폴더가 아닌 모든 폴더 (이름 꼴과 무관 — seed14.moved · old14 · seed15_moved · seed12-old) 의 정본 없는 "
            "판정 기록 · 정본 옆 판정 임시 파일 · 모르는 상태 ('PASS') · 원문만 남은 이전 판정은 미해결 기록 (목록 · 요약 장부 검사 invalid) · "
            f"깨끗한 보존 폴더 · 현재 폴더는 이 목록에 안 든다 ({[x_[:3] for x_ in pu_]} · {lc_pu[:200]})")
        # ⭐ DR 전 3차 리뷰 P2 — 이력 줄도 새 판정의 계 닫힘 (closes_system) 을 적는다 → 정본 없이 이력만 남아도 _run_kind 가 닫힘을 장부로 넘긴다
        d_cl = pathlib.Path(td_) / "dq_cl"; d_cl.mkdir()
        _append_history_first(d_cl, {"status": "fail", "closes_system": True, "provenance": {"files_sha256": {}}}, "selftest — 첫 시드 닫힘")
        rk_cl = _run_kind({}, d_cl, None)
        d_cl2 = pathlib.Path(td_) / "dq_cl2"; d_cl2.mkdir()
        (d_cl2 / VERDICT_HISTORY).write_text(json.dumps({"first": True, "new_status": "fail", "new_closes_system": "yes"}) + "\n", encoding="utf-8")
        # ⭐ DR 전 4차 리뷰 P1 · P2 — 판정 기록은 쓴 순서 (판정 밖에서 바뀐 앞 판정도 그 자리에) · 다른 카드 값 · 도구의 과학적 판정 기록은 판독 불가
        d_or = pathlib.Path(td_) / "dq_or"; d_or.mkdir()
        PA_, PB_, PC_ = ({"files_sha256": {"traj.xyz": x_ * 64}} for x_ in "abc")
        _append_history_first(d_or, {"status": "invalid", "provenance": PA_}, "selftest 1")
        _append_history(d_or, {"status": "incomplete", "provenance": PB_}, {"status": "pass", "provenance": PC_}, "selftest 2 — 앞 판정이 판정 밖에서 바뀜")
        (d_or / "stage1_verdict.json").write_text(json.dumps({"status": "pass", "provenance": PC_}), encoding="utf-8")
        ch_or = folder_verdict_chain(d_or)
        d_or2 = pathlib.Path(td_) / "dq_or2"; d_or2.mkdir()       # 보통의 두 번 쓰기 (첫 줄 → 바꿈 줄) — 바꿈 줄의 앞 판정은 겹침이라 한 번만
        _append_history_first(d_or2, {"status": "invalid", "provenance": PA_}, "selftest 1")
        _append_history(d_or2, {"status": "invalid", "provenance": PA_}, {"status": "pass", "provenance": PC_}, "selftest 2")
        (d_or2 / "stage1_verdict.json").write_text(json.dumps({"status": "pass", "provenance": PC_}), encoding="utf-8")
        ch_or2 = folder_verdict_chain(d_or2)
        d_al = pathlib.Path(td_) / "dq_al"; d_al.mkdir()
        PVal_ = {"files_sha256": {}, "card_values_sha16": "0" * 16, "driver_sha16": driver_sha16()}
        (d_al / "stage1_verdict.json").write_text(json.dumps({"status": "fail", "closes_system": True, "provenance": PVal_}), encoding="utf-8")
        rk_al = _run_kind({}, d_al, VAL)
        (d_al / "stage1_verdict.json").write_text(json.dumps({"status": "fail", "closes_system": True,
                                                              "provenance": {**PVal_, "card_values_sha16": values_sha16(VAL)}}), encoding="utf-8")
        rk_al2 = _run_kind({}, d_al, VAL)
        # ⭐ DR 전 5차 리뷰 P2 — 판정 규칙 지문 (상한 · 재시도 칸 제외) · 지금 규칙의 기록이 있으면 다른 규칙 기록은 무시 (한 줄이 폴더를 영영 막지 않게)
        VALcap = {**VAL, "stage1_cap_gpu_h": float(VAL.get("stage1_cap_gpu_h") or 0) + 99.0}
        VALthr = {**VAL, "melt_window": {**VAL["melt_window"], "D_threshold_cm2_s": float(VAL["melt_window"]["D_threshold_cm2_s"]) * 2}}
        d_al3 = pathlib.Path(td_) / "dq_al3"; d_al3.mkdir()          # 상한만 다른 카드로 낸 fail + 닫힘 (문서대로 상한을 올린 뒤의 재시도)
        PVcap_ = {"files_sha256": {}, "card_values_sha16": values_sha16(VALcap), "judge_values_sha16": judge_values_sha16(VALcap), "driver_sha16": driver_sha16()}
        (d_al3 / "stage1_verdict.json").write_text(json.dumps({"status": "fail", "closes_system": True, "provenance": PVcap_}), encoding="utf-8")
        rk_al3 = _run_kind({}, d_al3, VAL)
        d_al4 = pathlib.Path(td_) / "dq_al4"; d_al4.mkdir()          # 다른 녹음 문턱의 fail (이력) + 지금 규칙의 pass (정본) → 지금 규칙만
        PVthr_ = {"files_sha256": {}, "card_values_sha16": values_sha16(VALthr), "judge_values_sha16": judge_values_sha16(VALthr), "driver_sha16": driver_sha16()}
        PVnow_ = {"files_sha256": {}, "card_values_sha16": values_sha16(VAL), "judge_values_sha16": judge_values_sha16(VAL), "driver_sha16": driver_sha16()}
        _append_history_first(d_al4, {"status": "fail", "closes_system": True, "provenance": PVthr_}, "selftest — 다른 카드 손 판정")
        _append_history(d_al4, {"status": "fail", "closes_system": True, "provenance": PVthr_}, {"status": "pass", "provenance": PVnow_}, "selftest — 지금 카드")
        (d_al4 / "stage1_verdict.json").write_text(json.dumps({"status": "pass", "provenance": PVnow_}), encoding="utf-8")
        rk_al4 = _run_kind({}, d_al4, VAL)
        d_al5 = pathlib.Path(td_) / "dq_al5"; d_al5.mkdir()          # ⭐ DR 전 7차 리뷰 P0 — 다른 규칙의 fail + 지금 규칙으로 다시 판정한 비과학적 판정 → 판독 불가 (재시도 아님)
        _append_history_first(d_al5, {"status": "fail", "closes_system": True, "provenance": PVthr_}, "selftest — 다른 카드 손 판정")
        _append_history(d_al5, {"status": "fail", "closes_system": True, "provenance": PVthr_}, {"status": "incomplete", "provenance": PVnow_}, "selftest — 지금 카드")
        (d_al5 / "stage1_verdict.json").write_text(json.dumps({"status": "incomplete", "provenance": PVnow_}), encoding="utf-8")
        rk_al5 = _run_kind({}, d_al5, VAL)
        acc_ = set()
        class _TrackVals(dict):                              # 판정이 카드 값의 어느 열쇠를 읽는가 (JUDGE_VALUE_KEYS 밖을 읽으면 지문이 판정 규칙을 다 못 묶는다)
            def __getitem__(self, k_):
                acc_.add(k_); return dict.__getitem__(self, k_)
            def get(self, k_, *d_):
                acc_.add(k_); return dict.get(self, k_, *d_)
        d_tk = _dq_run("dq_tk")
        stage1_verdict(d_tk, values=_TrackVals(VAL), log=lambda *a: None, reason="selftest — 읽는 열쇠")
        chk(judge_values_sha16(VALcap) == judge_values_sha16(VAL) and judge_values_sha16(VALthr) != judge_values_sha16(VAL)
            and rk_al3[0] == "scientific" and rk_al3[1].get("closes_system") is True
            and rk_al4[0] == "scientific" and rk_al4[1].get("status") == "pass" and rk_al4[1].get("closes_system") is False
            and rk_al5[0] == "unreadable" and "다시 판정해 과학적 판정" in rk_al5[1].get("why", "")
            and acc_ and acc_ <= set(JUDGE_VALUE_KEYS),
            "⛔음성 DR 전 5차 리뷰 P2: 판정 규칙 지문은 판정이 읽는 카드 값만 (상한을 올려도 같고 · 녹음 문턱이 다르면 다르다) · 상한만 다른 카드로 낸 fail · 닫힘은 "
            "과학적 판정 그대로 · 다른 문턱의 손 판정 (이력) 과 지금 규칙의 판정 (정본) 이 같이 있으면 지금 규칙만 (닫힘을 옮기지 않는다) · 판정은 JUDGE_VALUE_KEYS "
            f"밖의 카드 열쇠를 읽지 않는다 · (7차 P0) 다른 규칙의 fail 뒤 지금 규칙으로 다시 판정한 비과학적 판정 (incomplete · invalid) 이 있어도 판독 불가 — "
            f"과학적 판정 기록이 있는 폴더에서 재시도할 수 있는 종류를 끌어내지 않는다 "
            f"({rk_al3} · {rk_al4} · {rk_al5[0]} · {sorted(acc_ - set(JUDGE_VALUE_KEYS))})")
        chk([x_["status"] for x_ in ch_or] == ["invalid", "incomplete", "pass"] and ch_or[1]["provenance"] == PB_ and len(ch_or) == 3
            and ch_or2 == [{"status": "invalid", "provenance": PA_}, {"status": "pass", "provenance": PC_}]
            and rk_al[0] == "unreadable" and rk_al2[0] == "scientific" and rk_al2[1].get("closes_system") is True,
            "⛔음성 DR 전 4차 리뷰 P1 · P2: 폴더 판정 기록은 쓴 순서대로 (겹침 없이 · 판정 밖에서 바뀐 앞 판정도 그 자리에) · 다른 카드 값으로 낸 과학적 판정 기록 "
            f"(손 판정 · 다른 checkout) 은 판독 불가 — 그 결과 · 닫힘을 장부로 옮기지 않는다 · 같은 카드면 그대로 ({ch_or} · {rk_al} · {rk_al2[0]})")
        d_cl3 = pathlib.Path(td_) / "dq_cl3"; d_cl3.mkdir()          # 바꿈 줄 (앞 판정 → 새 판정) 의 닫힘 — 새 판정을 쓰기 전에 끊겨 정본이 앞 판정 그대로/없음
        _append_history(d_cl3, {"status": "incomplete", "provenance": {"files_sha256": {}}},
                        {"status": "fail", "closes_system": True, "provenance": {"files_sha256": {}}}, "selftest — 바꿈 줄 닫힘")
        rk_cl3 = _run_kind({}, d_cl3, None)
        chk(rk_cl[0] == "scientific" and rk_cl[1].get("closes_system") is True and rk_cl[1].get("status") == "fail"
            and rk_cl3[0] == "scientific" and rk_cl3[1].get("closes_system") is True
            and loads_strict((d_cl / VERDICT_HISTORY).read_text(encoding="utf-8").strip()).get("new_closes_system") is True
            and _verdict_records(d_cl2)[1] is not None and _run_kind({}, d_cl2, None)[0] == "unreadable",
            "⛔음성 DR 전 3차 리뷰 P2: 이력 줄 (첫 판정 · 바꿈) 이 새 판정의 closes_system 을 적고 판정 기록이 그것을 읽는다 — 정본 없이 이력만 남은 첫 시드의 닫힘이 "
            f"장부로 넘어간다 · 참거짓이 아닌 표시는 해석할 수 없는 기록 ({rk_cl} · {_verdict_records(d_cl2)[1]})")
        # ⭐ 회신 DQ P1-2 — 정본 없이 판정 기록만 남은 폴더 (첫 판정 쓰기 끊김) ≠ 판정 안 한 폴더 · 묶음 판정 invalid · 손 판정은 그 사실을 이력에 적는다
        ru_ = pathlib.Path(td_) / "_dq_unres"
        for s_ in ("A", "B"):
            for sd_ in VAL["seeds"]:
                (ru_ / s_ / f"seed{sd_}").mkdir(parents=True)
        s0_ = VAL["seeds"][0]
        (ru_ / "A" / f"seed{s0_}" / VERDICT_HISTORY).write_text(json.dumps({"first": True, "new_status": "fail", "new_provenance": {}}) + "\n", encoding="utf-8")
        (ru_ / "B" / f"seed{s0_}" / "stage1_verdict.json.tmp").write_text('{"status": "fail"}', encoding="utf-8")
        (ru_ / "A" / f"seed{VAL['seeds'][1]}" / "stage1_verdict.json").mkdir()
        (ru_ / "B" / f"seed{VAL['seeds'][1]}" / VERDICT_HISTORY).write_text("", encoding="utf-8")   # 빈 이력 파일도 흔적 (열고 못 쓴 채 끊김)
        uf_ = {f"{s_}{sd_}": unresolved_first_write(ru_ / s_ / f"seed{sd_}") is not None for s_ in ("A", "B") for sd_ in VAL["seeds"][:3]}
        smu_ = _stage1_summary_core(ru_, VAL)
        want_uf = {f"{s_}{sd_}": False for s_ in ("A", "B") for sd_ in VAL["seeds"][:3]}
        want_uf.update({f"A{s0_}": True, f"B{s0_}": True, f"A{VAL['seeds'][1]}": True, f"B{VAL['seeds'][1]}": True})
        d_hf = pathlib.Path(td_) / "dq_hf"; d_hf.mkdir()    # 정본 없이 이력이 있는 폴더를 사람이 손으로 다시 판정 → 그 사실을 첫 줄에
        (pathlib.Path(d_hf) / VERDICT_HISTORY).write_text(json.dumps({"first": True, "new_status": "fail", "new_provenance": {}}) + "\n", encoding="utf-8")
        stage1_verdict(d_hf, values=VAL, log=lambda *a: None, reason="selftest 손 판정")
        h_hf = [loads_strict(x_) for x_ in (pathlib.Path(d_hf) / VERDICT_HISTORY).read_text(encoding="utf-8").split("\n") if x_.strip()]
        chk(uf_ == want_uf and sorted(smu_["stale_verdicts"]) == sorted([f"A{s0_}", f"B{s0_}", f"A{VAL['seeds'][1]}", f"B{VAL['seeds'][1]}"])
            and smu_["track"] == "invalid" and len(h_hf) == 2 and h_hf[-1].get("first") is True and h_hf[-1].get("history_lines_before") == 1
            and [x_.get("status") for x_ in folder_verdict_chain(d_hf)][-2:] == ["fail", h_hf[-1]["new_status"]][-2:],
            "⛔음성 회신 DQ P1-2: 정본 판정 없이 이력 (빈 파일 포함) · 판정 임시 파일 · 정본 자리의 디렉터리가 남은 폴더는 미해결 기록 (묶음 판정 invalid · "
            "stale) · 기록이 없는 폴더는 판정 안 함 (pending) · 손 판정은 앞 이력 줄 수를 첫 줄에 적고 사슬에 둘 다 남는다 "
            f"({ {k_: v_ for k_, v_ in uf_.items() if v_ != want_uf[k_]} } · {smu_['stale_verdicts']} · {smu_['track']} · {h_hf[-1:]})")
        want_cf = {"none_pass": False, "pass_pass": False, "inv_pass": True, "inc_fail": True, "PASS_none": True, "fail_pass": True, "melt_pass": True,
                   "melt_fail": False, "pass_incomplete": False, "rec_on": True, "rec_off": False,
                   "inv_same_prov": False, "inc_same_prov": False, "inv_prov_diff": True, "inv_prov_nocard": True, "inv_folder_noprov": True,
                   "none_prior_flip": True, "none_prior_same_sci": False, "none_prior_nonsci_changed": True, "none_prior_nonsci_driver": True,
                   "none_prior_nonsci_same": False, "none_prior_noprov": True, "none_prior_unreadable": True, "none_prior_unknown": True,
                   "none_prior_multi_step": True, "none_prior_all_same": False, "set_ledger_ignores_prior": False}
        chk(got_cf == want_cf, f"⛔음성 DQ 전 리뷰 P1-A · 2차 N3: 같은 실행 충돌 규칙 (러너 ①-4 · persist · 요약이 같이 쓴다) 진리표 — 비과학적 장부 판정은 "
                               "그때 지문 = 지금 (판정 입력 전부 다 있고 같음 · 앞 판정이 판정 도중 예외) 일 때만 대체 "
                               f"({ {k_: v_ for k_, v_ in got_cf.items() if v_ != want_cf[k_]} })")
        rsr_ = pathlib.Path(td_) / "_stop_rec"; rsr_.mkdir()
        sr_ = {"absent": stop_record(rsr_)[0]}
        SJ_ = lambda code_, **kv: json.dumps({"code": code_, "stop_id": "x", **kv})
        for nm_, txt_ in (("trunc", '{"code": "melt", "stop_id": "a'), ("terminal", SJ_("melt", terminal=True)), ("track", SJ_("track", terminal=True)),
                          ("term_contra", SJ_("cap", terminal=True)), ("interrupted_term", SJ_("interrupted", terminal=True)),
                          ("melt_noterm", SJ_("melt", terminal=False)), ("no_term", SJ_("invalid")), ("term_str", SJ_("invalid", terminal="false")),
                          ("bogus", SJ_("bogus", terminal=False)), ("invalid", SJ_("invalid", terminal=False)), ("open", SJ_("interrupted", terminal=False)),
                          ("term_int0", SJ_("invalid", terminal=0)), ("term_int1", SJ_("melt", terminal=1)),
                          ("no_id", json.dumps({"code": "melt", "terminal": True})), ("dup", '{"code": "melt", "code": "invalid", "stop_id": "x", "terminal": false}')):
            (rsr_ / "STOP.json").write_text(txt_, encoding="utf-8")
            sr_[nm_] = stop_record(rsr_)[0]
        want_sr = {"absent": "absent", "trunc": "unreadable", "terminal": "terminal", "track": "terminal", "term_contra": "unreadable",
                   "interrupted_term": "unreadable", "melt_noterm": "unreadable", "no_term": "unreadable", "term_str": "unreadable", "bogus": "unreadable",
                   "invalid": "open", "open": "open", "no_id": "unreadable", "dup": "unreadable", "term_int0": "unreadable", "term_int1": "unreadable"}
        sh_ack = {nm_: stop_shape_problem(d_, acked=True) is None for nm_, d_ in (
            ("ack_ok", {"code": "interrupted", "stop_id": "x", "terminal": False, "acked_at": "t"}), ("ack_noterm", {"code": "resume", "stop_id": "x"}),
            ("ack_melt", {"code": "melt", "stop_id": "x", "acked_at": "t"}), ("ack_term_true", {"code": "invalid", "stop_id": "x", "terminal": True}),
            ("ack_bogus", {"code": "bogus", "stop_id": "x"}))}
        lsp_ = {nm_: bool(ledger_shape_problems({"runs": [], "stop_history": h_})) for nm_, h_ in (
            ("ok", [{"code": "resume", "stop_id": "x", "terminal": False}]), ("melt", [{"code": "melt", "stop_id": "x", "terminal": True}]),
            ("bogus", [{"code": "bogus", "stop_id": "x"}]), ("contra", [{"code": "cap", "stop_id": "x", "terminal": True}]))}
        chk(sr_ == want_sr and sh_ack == {"ack_ok": True, "ack_noterm": True, "ack_melt": False, "ack_term_true": False, "ack_bogus": False}
            and lsp_ == {"ok": False, "melt": True, "bogus": True, "contra": True},
            f"⛔음성 DQ 전 리뷰 P2-D · 회신 DQ P2-1: 소비자의 STOP 판독 — 잘림 · 열쇠 없음 · 같은 열쇠 둘 · 모르는 코드 · terminal 없음 · 참거짓 아님 · "
            f"코드와 모순 (interrupted + true · melt + false) = 못 읽음 · 닫는 코드 + true = 닫힘 · 그 밖 + false = 확인 안 된 멈춤 · 장부 확인 기록도 "
            f"같은 함수 (닫는 코드 · 모르는 코드 · terminal true = 장부 꼴 문제) ({sr_} · {sh_ack} · {lsp_})")
        rhs_ = pathlib.Path(td_) / "_hist_shape"; rhs_.mkdir()
        (rhs_ / "stage1_verdict.json").write_text('{"status": "pass"}', encoding="utf-8")
        hres_ = {}
        for nm_, ln_ in (("prev_null", '{"prev": null, "new_status": "pass"}'), ("no_prev", '{"new_status": "pass"}'),
                         ("prev_bad", '{"prev": {"status": "garbage"}, "new_status": "pass"}'),
                         ("new_bad", '{"prev": {"status": "pass"}, "new_status": "x"}'),
                         ("ok", '{"prev": {"status": "incomplete"}, "new_status": "pass"}'),
                         ("ok_raw", '{"prev": {"status": null, "raw_b64": ""}, "new_status": "pass"}'),
                         ("first_ok", '{"first": true, "new_status": "pass", "new_provenance": {}}'),
                         ("first_with_prev", '{"first": true, "prev": {"status": "fail"}, "new_status": "pass"}'),
                         ("first_bad_status", '{"first": true, "new_status": "x"}')):
            (rhs_ / VERDICT_HISTORY).write_text(ln_ + "\n", encoding="utf-8")
            hres_[nm_] = _verdict_records(rhs_)[1] is None
        want_h = {"prev_null": False, "no_prev": False, "prev_bad": False, "new_bad": False, "ok": True, "ok_raw": True,
                  "first_ok": True, "first_with_prev": False, "first_bad_status": False}
        chk(hres_ == want_h, "⛔음성 DQ 전 리뷰 P2-C: 이력 줄의 prev 없음 · null · 모르는 이전 상태 · 모르는 새 상태 = 해석할 수 없는 기록 "
                             f"(상태 없는 원문 판정은 기록으로 남겨 요약이 따로 본다) ({hres_})")
        rmq_ = pathlib.Path(td_) / "_mark_summary"; rmq_.mkdir()
        m0_ = mark_summary_not_current(rmq_, "selftest")
        (rmq_ / "stage1_summary.json").write_text(json.dumps({"track": "stage1_pass", "stage2": {"seeds": [11, 12]}}), encoding="utf-8")
        m1_ = mark_summary_not_current(rmq_, "selftest")
        sm_m = json.loads((rmq_ / "stage1_summary.json").read_text(encoding="utf-8"))
        (rmq_ / "stage1_summary.json").write_text(json.dumps({"track": "stop_track", "why": "selftest"}), encoding="utf-8")
        m2_ = mark_summary_not_current(rmq_, "selftest")
        st_m2 = json.loads((rmq_ / "stage1_summary.json").read_text(encoding="utf-8"))["track"]
        (rmq_ / "stage1_summary.json").write_text('{"track": "stage1_pass", "track": "x"', encoding="utf-8")
        m3_ = mark_summary_not_current(rmq_, "selftest")
        st_m3 = json.loads((rmq_ / "stage1_summary.json").read_text(encoding="utf-8"))["track"]
        chk(m0_ is False and m1_ is True and sm_m["track"] == "pending" and sm_m["not_current"] is True and sm_m["stage2"] is None
            and not (rmq_ / "stage1_summary.json.tmp").exists() and m2_ is False and st_m2 == "stop_track" and m3_ is True and st_m3 == "pending",
            f"⛔음성 DQ 전 리뷰 P2-F · 2차: 낡은 통과 요약 · 못 읽는 요약을 '지금 판정 아님' (pending · not_current · 2 단계 없음) 으로 바꾼다 · 통과가 아닌 요약 "
            f"(stop_track) 은 그대로 · 요약이 없으면 안 만든다 ({m0_} · {m1_} · {sm_m['track']} · {m2_} · {st_m2} · {m3_} · {st_m3})")
        # 장부 지문 — 같은 카드 · 도구면 그 이유로 막지 않고, 다르면 막는다 (P2-G)
        rfp_ = pathlib.Path(td_) / "_led_fp"; rfp_.mkdir()
        led_fp = {"runs": [], "stop_history": [], "card_values_sha16": values_sha16(VAL), "driver_sha16": driver_sha16()}
        (rfp_ / LEDGER_NAME).write_text(json.dumps(led_fp), encoding="utf-8")
        fp_ok = ledger_check(rfp_, {}, VAL)["invalid"]
        (rfp_ / LEDGER_NAME).write_text(json.dumps({**led_fp, "card_values_sha16": "0" * 16}), encoding="utf-8")
        fp_c = ledger_check(rfp_, {}, VAL)["invalid"]
        (rfp_ / LEDGER_NAME).write_text(json.dumps({**led_fp, "driver_sha16": "0" * 16}), encoding="utf-8")
        fp_d = ledger_check(rfp_, {}, VAL)["invalid"]
        chk(fp_ok == [] and any("카드 값 지문" in x_ for x_ in fp_c) and any("도구 지문" in x_ for x_ in fp_d),
            f"⛔음성 DQ 전 리뷰 P2-G: 장부의 카드 값 · 도구 지문이 지금과 다르면 invalid (같으면 그 이유로 안 막는다) ({fp_ok} · {len(fp_c)} · {len(fp_d)})")
        rs_fl = folder_stage_detail(pathlib.Path(td_) / "fl")[1]                         # fire_log_no_marker
        chk("FIRE 로그" in (rs_fl or ""),
            "⛔음성 회신 DL Q3: FIRE 로그만 있고 MD 완료 기록이 없으면 그 이유로 보류한다 (MD 중 파일 목록 검사와 구별 · 사람이 보는 보류 이유 · "
            f"깨기 N5 가 드러낸 시험 구멍) ({rs_fl})")
        rs_f2 = {k: folder_stage_detail(pathlib.Path(td_) / k)[1] for k in ("x6", "x7")}   # final_is_dir · result_dangling
        chk(all("파일이 아닌 것" in (r_ or "") for r_ in rs_f2.values()),
            "⛔음성 DO 전 리뷰 F2: final · result 자리에 디렉터리 · 깨진 링크가 있으면 그 이유로 보류한다 (MD 중 파일 목록 검사와 구별 · 사람이 보는 "
            f"보류 이유 · 깨기 DO6 이 드러낸 시험 구멍) ({rs_f2})")
        rs_pf = {k: folder_stage_detail(pathlib.Path(td_) / k)[1] for k in ("v6", "w3")}   # mid_history_pass · mid_history_pass_nofinal
        chk(all("과학적 판정 (pass)" in (r_ or "") for r_ in rs_pf.values()),
            "⛔음성 DM P0-2: 도중 끊김 후보의 pass 이력은 '과학적 판정' 이유로 보류한다 — 해석할 수 없는 상태와 구별 (사람이 보는 보류 이유 · "
            f"DM 깨기 O12 가 드러낸 시험 구멍) ({rs_pf})")
        # ⭐ 회신 DL P1-1 — 완료 기록 쓰기 순서 (데이터 fsync → 임시 기록 fsync → 교체 → 디렉터리 fsync) · 어디서 실패해도 보류
        g_ = globals()
        real_ff, real_fh, real_fd = g_["_fsync_file"], g_["_fsync_handle"], g_["_fsync_dir"]
        def _probe(name, fail_at=None):
            d = pathlib.Path(td_) / name; d.mkdir()
            (d / "plan.json").write_text(json.dumps(PLAN0), encoding="utf-8")
            (d / "traj.xyz").write_text(FR(5), encoding="utf-8"); (d / "thermo.csv").write_text(TH(5), encoding="utf-8")
            seq_ = []
            def ff(p):
                seq_.append(("file", pathlib.Path(p).name, (d / MD_DONE_TMP).exists() or (d / MD_DONE_NAME).exists()))
                if fail_at == "file":
                    raise OSError("주입: 데이터 fsync 실패")
                real_ff(p)
            def fh(h):
                seq_.append(("handle", (d / MD_DONE_TMP).exists(), (d / MD_DONE_NAME).exists()))
                if fail_at == "handle":
                    raise OSError("주입: 임시 기록 fsync 실패")
                real_fh(h)
            def fd(p):
                seq_.append(("dir", (d / MD_DONE_TMP).exists(), (d / MD_DONE_NAME).exists()))
                if fail_at == "dir":
                    raise OSError("주입: 디렉터리 fsync 실패")
                return real_fd(p)
            g_["_fsync_file"], g_["_fsync_handle"], g_["_fsync_dir"] = ff, fh, fd
            err = None
            try:
                write_md_done(d, run_id=RIDF, n_steps_planned=planned_md_steps(PLAN0), n_steps_done=planned_md_steps(PLAN0))
            except OSError as e:
                err = str(e)
            finally:
                g_["_fsync_file"], g_["_fsync_handle"], g_["_fsync_dir"] = real_ff, real_fh, real_fd
            return seq_, err, folder_stage(d)
        sq_ok, e_ok, st_ok = _probe("fs_ok")
        chk(e_ok is None and st_ok == "md_complete"
            and sq_ok == [("file", "traj.xyz", False), ("file", "thermo.csv", False), ("handle", True, False), ("dir", False, True)],
            f"회신 DL P1-1: 완료 기록 순서 = traj · thermo fsync (기록 전) → 임시 기록 fsync (교체 전) → 교체 → 디렉터리 fsync ({sq_ok})")
        fails = {k: _probe("fs_" + k, fail_at=k) for k in ("file", "handle", "dir")}
        chk(all(v[1] and v[2] in ("unreadable", "md_complete") for v in fails.values())
            and fails["file"][2] == "unreadable" and fails["handle"][2] == "unreadable" and fails["dir"][2] == "md_complete",
            "⛔음성 DL P1-1: 저장 단계 어디서 실패해도 예외가 올라가고 (FIRE 안 함) 폴더는 보류 — 데이터 fsync 실패 = 끝 경계 보류 · "
            f"임시 기록 fsync 실패 = 임시 기록 보류 · 디렉터리 fsync 실패 = MD 완료 보류 ({ {k: v[2] for k, v in fails.items()} })")
        vd = pathlib.Path(td_) / "v"; vd.mkdir()
        v_none = verdict_file_status(vd)
        (vd / "stage1_verdict.json").write_text('{"status": "pass"}', encoding="utf-8"); v_pass = verdict_file_status(vd)
        (vd / "stage1_verdict.json").write_text('{"status": "pa', encoding="utf-8"); v_cut = verdict_file_status(vd)
        (vd / "stage1_verdict.json").write_text('{"status": "maybe"}', encoding="utf-8"); v_unk = verdict_file_status(vd)
        (vd / "stage1_verdict.json").write_text('[1, 2]', encoding="utf-8"); v_list = verdict_file_status(vd)
    chk(v_none is None and v_pass == "pass" and v_cut == v_unk == v_list == "unreadable",
        f"⛔음성 DJ P0-2: 판정 파일 없음 (None) 과 있는데 못 읽음 (잘림 · 모르는 상태 · 객체 아님 = unreadable) 을 가른다 ({v_none} · {v_pass} · {v_cut} · {v_unk} · {v_list})")
    D_ = lambda **k: {"reason": "power_outage", "event": "kgy 정전 (selftest)", "evidence": "UPS 로그 (selftest)", "declared_by": "selftest",
                      "declared_at": "2026-11-03 00:00:00", **k}
    dp = {"none": declaration_problems(None, "interrupted", VAL), "ok": declaration_problems(D_(), "interrupted", VAL),
          "ctrl_c": declaration_problems(D_(reason="user_ctrl_c"), "interrupted", VAL),
          "inv_reason_for_int": declaration_problems(D_(reason="invalid_cause_fixed"), "interrupted", VAL),
          "inv_ok": declaration_problems(D_(reason="invalid_cause_fixed"), "invalid", VAL),
          "no_by": declaration_problems(D_(declared_by=" "), "interrupted", VAL),
          "rejudge_missing": declaration_problems(D_(reason="invalid_cause_fixed"), "invalid", VAL, rejudge_needed=True),
          "rejudge_ok": declaration_problems(D_(reason="invalid_cause_fixed", rejudge_impossible_reason="traj 0 번 프레임 종이 바뀜 (selftest)"),
                                             "invalid", VAL, rejudge_needed=True),
          "cap_outage": declaration_problems(D_(), "interrupted", VAL, prev_status="cap"),
          "cap_ok": declaration_problems(D_(reason="budget_cap_raised"), "interrupted", VAL, prev_status="cap"),
          "raise_noncap": declaration_problems(D_(reason="budget_cap_raised"), "interrupted", VAL, prev_status="interrupted")}
    chk(all(dp[k] for k in ("none", "ctrl_c", "inv_reason_for_int", "no_by", "rejudge_missing", "cap_outage", "raise_noncap"))
        and not any(dp[k] for k in ("ok", "inv_ok", "rejudge_ok", "cap_ok")),
        "⛔음성 DJ Q1 · Q4: 재시도 선언 — 없음 · 허용 밖 사유 (Ctrl-C) · 다른 종류 사유 · 선언자 없음 · 다시 판정 못 하는 이유 없음 · "
        "상한 런에 정전 사유 · 상한 아닌 런에 상한 사유 → 거부 (맞는 선언은 통과)")
    with tempfile.TemporaryDirectory() as td_:                # 회신 DK P0-2 — 실행 상태는 장부 · 폴더 판정을 같이 본다 (어디에 적었든 같은 답)
        def _vf(name, txt):
            d = pathlib.Path(td_) / name; d.mkdir()
            if txt is not None:
                (d / "stage1_verdict.json").write_text(txt, encoding="utf-8")
            return str(d)
        END = {"status": "ended"}                              # invalid 판정은 끝난 런의 것이어야 실행 종류 invalid (DO 전 리뷰)
        rk = {"none": run_kind({}, _vf("a", None)), "ledger_invalid": run_kind({**END, "verdict": "invalid"}, _vf("b", None)),
              "folder_invalid": run_kind(END, _vf("c", '{"status": "invalid"}')),
              "both_invalid": run_kind({**END, "verdict": "invalid"}, _vf("d", '{"status": "invalid"}')),
              "folder_pass": run_kind({}, _vf("e", '{"status": "pass"}')), "ledger_fail": run_kind({"verdict": "fail"}, _vf("f", None)),
              "folder_cut": run_kind({}, _vf("g", '{"status": "in')), "ledger_unknown": run_kind({"verdict": "maybe"}, _vf("h", None)),
              "incomplete": run_kind({"verdict": "incomplete"}, _vf("i", '{"status": "incomplete"}')), "no_folder": run_kind({}, None),
              # ⭐ DO 전 리뷰 — 끊긴 런 (status interrupted · orphaned) 폴더의 invalid 판정은 종류를 바꾸지 않는다 (한도 우회 막기)
              "cut_folder_invalid": run_kind({"status": "interrupted"}, _vf("j", '{"status": "invalid"}')),
              "orphan_was_ended": run_kind({"status": "orphaned", "status_before_orphan": "ended", "verdict": "invalid"}, _vf("k", None)),
              "melt_invalid_kill": run_kind({"status": "orphaned", "melt_check": {"verdict": "invalid"}}, _vf("l", None)),
              # 첫 시드 녹음 fail 은 판정이 없어도 과학적 (장부 melt_check · closes_system)
              "melt_fail_kill": run_kind({"status": "stop_failed", "melt_check": {"verdict": "fail"}}, _vf("m", None)),
              "closes_true": run_kind({"status": "orphaned", "closes_system": True}, _vf("n", None)),
              "closes_str": run_kind({"closes_system": "true"}, _vf("o", None)),
              "melt_check_bad": run_kind({"melt_check": "fail"}, _vf("p", None)),
              # 꼴이 틀린 melt_check (러너는 fail · invalid 일 때만 dict 로 쓴다) — 끊긴 런으로 새지 않는다 (깨기 DO24 가 드러낸 시험 구멍)
              "melt_check_pass_dict": run_kind({"status": "interrupted", "melt_check": {"verdict": "pass"}}, _vf("s", None)),
              "melt_check_empty": run_kind({"status": "interrupted", "melt_check": []}, _vf("t", None)),
              "melt_check_zero": run_kind({"status": "interrupted", "melt_check": 0}, _vf("u", None)),
              # 판정 이력의 과학적 판정 (현재 판정이 incomplete 여도)
              "history_fail": run_kind({}, _vf("q", '{"status": "incomplete"}')),
              "verdict_tmp": run_kind({}, _vf("r", None))}
        _append_history(pathlib.Path(td_) / "q", {"status": "fail", "provenance": {}}, {"status": "incomplete", "provenance": {}}, "selftest")
        rk["history_fail"] = run_kind({}, str(pathlib.Path(td_) / "q"))
        (pathlib.Path(td_) / "r" / "stage1_verdict.json.tmp").write_text('{"status": "pass"}', encoding="utf-8")
        rk["verdict_tmp"] = run_kind({}, str(pathlib.Path(td_) / "r"))
        rk["bad_row"] = run_kind(["not", "a", "row"], None)
    exp_rk = {"none": "interrupted", "ledger_invalid": "invalid", "folder_invalid": "invalid", "both_invalid": "invalid",
              "folder_pass": "scientific", "ledger_fail": "scientific", "folder_cut": "unreadable", "ledger_unknown": "unreadable",
              "incomplete": "interrupted", "no_folder": "interrupted", "cut_folder_invalid": "interrupted", "orphan_was_ended": "invalid",
              "melt_invalid_kill": "invalid", "melt_fail_kill": "scientific", "closes_true": "scientific", "closes_str": "unreadable",
              "melt_check_bad": "unreadable", "melt_check_pass_dict": "unreadable", "melt_check_empty": "unreadable", "melt_check_zero": "unreadable",
              "history_fail": "scientific", "verdict_tmp": "unreadable", "bad_row": "unreadable"}
    with tempfile.TemporaryDirectory() as td_:                # ⭐ DP 전 리뷰 F1 · F3 · F4 — 판정 기록으로 본 과학적 결과는 근거 (상태 · 닫힘) 를 같이 돌려준다 ·
        def _vf2(name, txt):                                  #   못 읽은 이전 판정 (raw_b64 자리 · 상태 없음) = 판독 불가 · 끊긴 런의 녹음 invalid = 끊긴 런 · 보관 목록 꼴
            d = pathlib.Path(td_) / name; d.mkdir()
            if txt is not None:
                (d / "stage1_verdict.json").write_text(txt, encoding="utf-8")
            return str(d)
        fv_fail = run_kind_detail({}, _vf2("a", '{"status": "fail", "closes_system": true}'))
        fv_pass = run_kind_detail({}, _vf2("b", '{"status": "pass"}'))
        d_raw = _vf2("c", '{"status": "incomplete"}')
        _append_history(pathlib.Path(d_raw), {"status": None, "raw_b64": "e30=", "⛔": "못 읽음 (selftest)"},
                        {"status": "incomplete", "provenance": {}}, "selftest")
        raw_unr = run_kind_detail({}, d_raw)
        mh_bad = run_kind_detail({"status": "interrupted", "melt_check_history": "x"}, _vf2("d", None))
        mh_ok = run_kind_detail({"status": "interrupted", "melt_check_history": [{"verdict": "invalid"}]}, _vf2("e", None))
        d_mi = _vf2("f", None)                                # 녹음 판정 invalid 폴더 (고정 밀도 plan 아님) + 궤적
        (pathlib.Path(d_mi) / "plan.json").write_text(json.dumps({"melt_ps": 10.0, "save_ps": 1.0}), encoding="utf-8")
        (pathlib.Path(d_mi) / "traj.xyz").write_text("1\n\nP 0 0 0\n", encoding="utf-8")
        mi_cut = run_kind_detail({"status": "interrupted"}, d_mi, VAL)
        mi_end = run_kind_detail({"status": "ended"}, d_mi, VAL)
        mi_orph = run_kind_detail({"status": "orphaned", "status_before_orphan": "running"}, d_mi, VAL)
    chk(fv_fail[0] == "scientific" and fv_fail[1] == {"source": "folder_verdict", "status": "fail", "closes_system": True, "provenance": None,
                                                      "prior": [{"status": "fail", "provenance": None}]}
        and fv_pass[0] == "scientific" and fv_pass[1].get("status") == "pass" and fv_pass[1].get("closes_system") is False
        and raw_unr[0] == "unreadable" and mh_bad[0] == "unreadable" and mh_ok[0] == "interrupted"
        and mi_cut[0] == "interrupted" and mi_end == ("invalid", {"source": "folder_melt_window"}) and mi_orph[0] == "interrupted",
        "⛔음성 DP 전 리뷰 F1 · F3 · F4: 폴더 판정 fail · pass 는 근거 (상태 · closes_system) 를 같이 → 러너가 장부에 적는다 · 못 읽은 이전 판정 "
        "(상태 없음) = 판독 불가 · 끊긴 런 (고아 마감 전 running 포함) 의 녹음 invalid 는 끊긴 런 (한도 우회 막기) · 끝난 런이면 invalid · "
        f"melt_check_history 가 목록이 아니면 판독 불가 ({[fv_fail, fv_pass, raw_unr[0], mh_bad[0], mh_ok[0], mi_cut[0], mi_end, mi_orph[0]]})")
    with tempfile.TemporaryDirectory() as td_:                # ⭐ DQ 전 2차 리뷰 N3 — 관측에 실리는 지문 (_vf2 는 지금 td_ 를 쓴다)
        PVk = {"files_sha256": {"traj.xyz": "c" * 64}, "card_values_sha16": "1" * 16, "driver_sha16": "2" * 16}
        d_pv = _vf2("pv", None)
        PVreal = {"files_sha256": run_provenance(d_pv), "card_values_sha16": values_sha16(VAL), "driver_sha16": driver_sha16(),
                  "band_sha16": band_card_sha16(),                 # ⭐ 회신 DQ P1-1 — 지금과의 대조에 G4 밴드 카드 (읽었을 때) ·
                  "folder": [pathlib.Path(d_pv).parent.name, pathlib.Path(d_pv).name]}   # 폴더 이름 (DR 전 리뷰 P3-A) 도 든다
        d_pb = _vf2("pb", None)                              # ⭐ 회신 DQ P1-1 (음성) — 밴드 카드 지문만 다른 판정은 지금과 안 맞는다
        (pathlib.Path(d_pb) / "stage1_verdict.json").write_text(json.dumps({"status": "pass", "provenance": {**PVreal, "files_sha256": run_provenance(d_pb),
                                                                                                         "band_sha16": "0" * 16}}), encoding="utf-8")
        fv_prov_band = run_kind_detail({}, d_pb, VAL)
        (pathlib.Path(d_pv) / "stage1_verdict.json").write_text(json.dumps({"status": "pass", "provenance": PVreal, "history": {"prev_status": "incomplete"}}),
                                                               encoding="utf-8")
        fv_prov = run_kind_detail({}, d_pv, VAL)
        fv_prov_noval = run_kind_detail({}, d_pv)
        d_fk = _vf2("fk", json.dumps({"status": "pass", "provenance": PVk}))            # 지금 파일과 안 맞는 (꾸민 · 낡은) 지문
        fv_prov_fake = run_kind_detail({}, d_fk, VAL)
        d_pm = _vf2("pm", json.dumps({"status": "pass", "provenance": PVk}))         # 지금 판정 pass · 이력의 이전 판정 fail
        _append_history(pathlib.Path(d_pm), {"status": "fail", "provenance": PVk}, {"status": "pass", "provenance": PVk}, "selftest")
        fv_prov_mix = run_kind_detail({}, d_pm)
        d_fr = _vf2("fr", None)                                                     # 앞 판정 파일 없음 → 첫 판정 줄
        r_fr = stage1_verdict(d_fr, values=VAL, log=lambda *a: None, reason="selftest 첫 판정")
        h_fr = [loads_strict(x_) for x_ in (pathlib.Path(d_fr) / VERDICT_HISTORY).read_text(encoding="utf-8").split("\n") if x_.strip()]
        (pathlib.Path(d_fr) / "stage1_verdict.json").unlink()                          # 판정 파일을 지워도
        ch_fr = folder_verdict_chain(d_fr)
        d_ff = _vf2("ff", None)                                                     # 판정 파일은 지워졌고 이력에 첫 판정 fail 만 남은 폴더
        _append_history_first(pathlib.Path(d_ff), {"status": "fail", "provenance": PVk}, "selftest — 지워진 첫 판정")
        cf_fr = ledger_verdict_conflict({}, "pass", folder_provenance=PVk, folder_prior=folder_verdict_chain(d_ff))
        d_tm = _vf2("tm", '{"status": "pass"}')
        (pathlib.Path(d_tm) / "stage1_verdict.json.tmp").write_text('{"status": "fail"}', encoding="utf-8")
        ch_tm, ch_none = folder_verdict_chain(d_tm), folder_verdict_chain(str(pathlib.Path(td_) / "nope"))
        chk(fv_prov[1].get("provenance") == PVreal and fv_prov[1].get("prior") == [{"status": "pass", "provenance": PVreal}]
            and folder_verdict_chain(d_pm) == [{"status": "fail", "provenance": PVk}, {"status": "pass", "provenance": PVk}]   # DR 전 4차 — 쓴 순서 (겹침 없이)
            and len(ch_tm) == 1 and ch_tm[0].get("status") is None and ch_none == []
            and len(h_fr) == 1 and h_fr[0].get("first") is True and "prev" not in h_fr[0] and ch_fr == [{"status": r_fr["status"], "provenance": r_fr["provenance"]}]
            and cf_fr is not None
            and fv_prov_noval[1].get("provenance") is None
            and fv_prov_fake[1].get("provenance") is None and fv_prov_mix[1].get("status") == "fail" and fv_prov_mix[1].get("provenance") is None
            and fv_prov_band[1].get("provenance") is None and fv_prov_band[1].get("status") == "pass",
            "⛔음성 DQ 전 2차 리뷰 N3: 폴더 판정 관측에 지금 판정의 지문이 실린다 (재시도 · 확인 경로도 ①-4 와 같은 대체 규칙) · 관측 상태 (이력의 fail) 가 "
            f"지금 판정 (pass) 과 다르면 지문을 싣지 않는다 (대체 못 함) · (3차 P3) 지문은 지금 파일 · 카드 · 도구와 같을 때만 · (4차) 폴더 판정 기록 전체를 싣는다 "
            f"({fv_prov[1].get('provenance') == PVreal} · {fv_prov_noval[1].get('provenance')} · {fv_prov_fake[1].get('provenance')} · {fv_prov_mix[1]})")
    chk(rk == exp_rk,
        "⛔음성 DK P0-2 · DO 전 리뷰: 실행 상태 한 곳 (run_kind) — 끝난 런의 invalid 판정은 장부 · 폴더 어디든 invalid · 끊긴 런 폴더의 invalid "
        "판정은 끊긴 런 · 고아 마감 전 상태로 · 녹음 invalid 로 멈춤 = invalid · 녹음 fail · closes_system · 이력의 fail = 과학적 · 꼴이 틀린 "
        f"값 · 임시 판정 = 판독 불가 ({ {k: rk[k] for k in rk if rk[k] != exp_rk[k]} })")
    # ④ 배로스탯 대조 잡 — LJ 결정(fcc)으로 배선만. 같은 BARO 를 쓰는지까지 본다
    from ase.build import bulk
    with tempfile.TemporaryDirectory() as td:
        cr = bulk("Li", "fcc", a=4.3, cubic=True).repeat(2)
        # LJ 파라미터가 Li 격자와 안 맞아 0 K 완화가 20 %대로 움직인다 — 여기선 **배선**만 본다
        res = run_npt_control(cr, LennardJones(sigma=3.0, epsilon=0.20, rc=8.0), td,
                              T_K=50, ps=0.4, dt_fs=2.0, save_ps=0.02, max_relax_dV=0.5,
                              log=lambda *a: None)
        chk(res["baro"] == BARO, "대조 잡이 생산 런과 **같은** BARO 상수를 쓴다 (다르면 아무것도 증명 못 한다)")
        chk(math.isfinite(res["rho_UMA_0K_g_cm3"]) and math.isfinite(res["P_NPT_mean_last_half_GPa"])
            and os.path.isfile(os.path.join(td, "control.json")),
            f"대조 잡 배선: ρ(0K) {res['rho_UMA_0K_g_cm3']:.3f} · P_NPT {res['P_NPT_mean_last_half_GPa']:+.3f} GPa · control.json")
        chk(abs(res["P_UMA_0K_GPa"]) < 0.5, f"가변셀 완화가 0 GPa 근처로 간다 (P_0K {res['P_UMA_0K_GPa']:+.3f} GPa)")
        chk(res["cell_relax"] and "steps=" in res["cell_relax_note"] and res["reference_for_drift"] == "rho_UMA_0K",
            f"0 K 완화 기록이 남는다 ({res['cell_relax_note']})")
        chk(res["cell_wide_enough"] is False and abs(res["min_cell_width_A"] - 8.6) < 0.01,
            f"⛔음성: 폭 {res['min_cell_width_A']:.2f} Å < 9 Å 인 셀을 **조건부**로 표시한다 (조용히 통과 안 시킨다)")
    # ⑤ 면간거리 — 원자 수가 아니라 이게 MIC 기준이다
    cub = np.eye(3) * 10.0
    chk(np.allclose(cell_widths_A(cub), 10.0), "입방 셀 면간거리 = 변 길이")
    prim = np.array([[0., 2., 2.], [2., 0., 2.], [2., 2., 0.]])          # fcc primitive (a=4)
    wp = cell_widths_A(prim)
    chk(abs(wp.min() - 4.0 / math.sqrt(3)) < 1e-9,
        f"fcc primitive(a=4): 벡터 길이 2.83 인데 폭은 a/√3 = {wp.min():.3f} Å — 원자 수로는 안 보이는 값")
    r = auto_repeat(prim, 9.0)
    chk(cell_widths_A((np.diag(r) @ prim)).min() >= 9.0,
        f"auto_repeat 가 폭 문턱을 채운다 ×{r} → {cell_widths_A((np.diag(r) @ prim)).min():.2f} Å")
    # ⛔음성: 0 K 완화가 부피를 많이 바꾸면 멈춘다 (그만큼 움직이면 대조가 아니다)
    with tempfile.TemporaryDirectory() as td:
        cr2 = bulk("Li", "fcc", a=3.2, cubic=True).repeat(2)      # 일부러 압축해 둔 격자
        try:
            run_npt_control(cr2, LennardJones(sigma=3.0, epsilon=0.20, rc=8.0), td,
                            T_K=50, ps=0.2, dt_fs=2.0, save_ps=0.02, max_relax_dV=0.02,
                            log=lambda *a: None)
            g = False
        except SystemExit as e:
            g = "대조가 아니다" in str(e)
        chk(g, "⛔음성: 0 K 완화 부피변화가 허용 밖이면 조용히 진행하지 않고 멈춘다")
    # 0 K 완화를 건너뛰면 기준이 파일 밀도로 바뀐다
    with tempfile.TemporaryDirectory() as td:
        cr3 = bulk("Li", "fcc", a=4.3, cubic=True).repeat(2)
        r3 = run_npt_control(cr3, LennardJones(sigma=3.0, epsilon=0.20, rc=8.0), td,
                             T_K=50, ps=0.2, dt_fs=2.0, save_ps=0.02, cell_relax=False, log=lambda *a: None)
        chk(r3["reference_for_drift"] == "rho_file" and r3["rho_UMA_0K_g_cm3"] is None
            and r3["UMA_vs_file"] is None,
            "--control_no_cellrelax: 기준이 파일 밀도로 바뀌고 0 K 항목은 None (0 으로 안 채운다)")
    # ⛔음성: 압력을 못 주는 계산기는 0 이 아니라 NaN
    class _NoStress(LennardJones):
        implemented_properties = ["energy", "forces"]
        def get_stress(self, atoms=None):
            raise RuntimeError("stress 없음")
    at2 = bulk("Li", "fcc", a=4.3, cubic=True); at2.calc = _NoStress()
    chk(math.isnan(pressure_GPa(at2)), "⛔음성: 응력을 못 주면 NaN — 0 GPa 로 조용히 적지 않는다")
    # ⑥ 운동 항 — 배로스탯이 보는 압력은 virial 이 아니다 (2026-09-12 오독)
    from ase.md.velocitydistribution import MaxwellBoltzmannDistribution as _MB
    hot = bulk("Li", "fcc", a=4.3, cubic=True).repeat(3)
    hot.calc = LennardJones(sigma=3.0, epsilon=0.2, rc=8.0)
    _MB(hot, temperature_K=300)
    _v, _t = pressure_GPa(hot, include_ideal_gas=False), pressure_GPa(hot)
    _kin = 2.0 / 3.0 * hot.get_kinetic_energy() / hot.get_volume() * EV_A3_TO_GPA
    chk(abs((_t - _v) - _kin) < 1e-9 and _kin > 0.05,
        f"총 압력 − virial = NkT/V ({_kin:+.4f} GPa) — 이걸 빼먹으면 0 GPa 목표가 −0.3 으로 보인다")
    cold = bulk("Li", "fcc", a=4.3, cubic=True).repeat(2)
    cold.calc = LennardJones(sigma=3.0, epsilon=0.2, rc=8.0)
    chk(abs(pressure_GPa(cold) - pressure_GPa(cold, include_ideal_gas=False)) < 1e-12,
        "속도 0 이면 두 값이 같다 — 차이는 순전히 운동 항이다")
    # ⑦ NPT MSD — 셀이 숨쉬는 것을 확산으로 읽지 않는지 (이게 핵심 음성시험)
    rng = np.random.default_rng(7)
    N, T = 40, 60
    f0 = rng.uniform(0, 1, (N, 3))
    L = np.linspace(20.0, 18.0, T)                       # 셀이 10 % 수축한다
    cells_b = np.array([np.eye(3) * x for x in L])
    pos_b = np.array([f0 @ cells_b[i] for i in range(T)])  # 분수좌표 고정 = 강체
    symb = ["P"] * N
    _t, m_b = npt_msd(symb, pos_b, cells_b, 1.0)
    naive = ((pos_b - pos_b[0]) ** 2).sum(-1).mean(-1).max()
    chk(m_b["P"].max() < 1e-16 < naive and naive > 1.0,
        f"⛔음성: 셀 10 % 수축 + 분수좌표 고정 → MSD {m_b['P'].max():.2e} Å² (실공간 순진계산은 {naive:.1f} Å²)")
    # 전체 병진(드리프트)도 확산이 아니다
    pos_d = pos_b + (np.arange(T)[:, None, None] * np.array([0.3, 0.0, 0.0]))
    _t, m_d = npt_msd(symb, pos_d, cells_b, 1.0)
    chk(m_d["P"].max() < 1e-12, f"⛔음성: 전체 병진 {0.3*T:.0f} Å 를 확산으로 읽지 않는다 ({m_d['P'].max():.2e} Å²)")
    # 자유절편 맞춤이 D 를 되찾는다
    tt = np.arange(0, 101.0, 1.0); Dtrue = 2.5e-5
    D_hat, c_hat = fit_D(tt, 6 * (Dtrue * 1e4) * tt + 3.0, 50.0, 100.0)
    chk(abs(D_hat / Dtrue - 1) < 1e-9 and abs(c_hat - 3.0) < 1e-6,
        f"fit_D 가 D={Dtrue:.1e} 와 절편 3.0 을 되찾는다 (D̂ {D_hat:.3e} · ĉ {c_hat:.3f})")
    # 실제로 움직이면 잡아낸다 — 한 원소만 무작위걷기
    step = 0.25
    walk = np.cumsum(rng.normal(0, step, (T, N, 3)), axis=0)
    pos_w = pos_b + walk
    _t, m_w = npt_msd(symb, pos_w, cells_b, 1.0)
    chk(m_w["P"][-1] > 3.0, f"움직이는 골격은 잡아낸다 (MSD {m_w['P'][-1]:.2f} Å²)")
    # ⑧ --gate_check: 기록 ↔ 실행 ↔ 게이트 (2026-09-14)
    import tempfile, inspect
    def _mkrun(d, plan, rows):
        d = pathlib.Path(d); d.mkdir(parents=True, exist_ok=True)
        (d / "plan.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        with open(d / "thermo.csv", "w") as f:
            f.write("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
            for r in rows:
                f.write(",".join(f"{x:.4f}" for x in r) + "\n")
        return d
    def _rows(rho_tail, p_tail):
        out = []
        for i in range(100):                      # 앞 50 프레임은 **일부러 거칠게** 둔다 (창 시험)
            calm = i >= 50
            out.append((float(i), 300.0 if calm else 1200.0, 300.0 if calm else 1200.0,
                        rho_tail if calm else 1.2000, 8000.0, -1000.0,
                        (p_tail + 0.02 * ((-1) ** i)) if calm else 5.0,
                        0.0))
        return out
    sym_A, _pos, _cell = build_random_cell("A", seed=1)
    plan_ok = build_plan("A", 1, sym_A, 1.2, 1200.0, 300.0, 100.0, 1e12, 900.0, 50.0, 2.0, 1.0)
    gi = plan_ok.get("게이트_입력", {})       # ⛔ 필드가 사라지면 **빨간불**이지 예외가 아니다
    chk(gi.get("ensemble") == "NPT" and gi.get("target_pressure_GPa") == 0.0,
        "build_plan 이 앙상블·목표압력을 plan 에 **기록**한다 (G4 가 읽을 값)")
    src = inspect.getsource(run_melt_quench)
    chk("NPTBerendsen" in src and "pressure_au=0.0" in src
        and ENSEMBLE["barostat"] == "Berendsen" and ENSEMBLE["target_pressure_GPa"] == 0.0,
        "선언(ENSEMBLE) 이 실행 경로(NPTBerendsen · pressure_au=0.0)와 같은 것을 말한다")
    c0, lo0, hi0 = read_band()
    chk(abs(c0 - 1.91347) < 1e-4 and abs(lo0 / c0 - 0.85) < 1e-4 and abs(hi0 / c0 - 1.15) < 1e-4,
        f"read_band 가 카드에서 중심 {c0:.5f} · ±15 % 밴드를 읽는다 (도구가 숫자를 안 갖는다)")
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        r = gate_check(_mkrun(td / "good", plan_ok, _rows(1.9000, 0.00)), win_ps=10.0, log=lambda *a: None)
        chk(r["record_has_gate_input"] and r["pressure_ok"] and r["in_band"] and not r["G4_fires"],
            "정상 런: 기록 있음 · ⟨P⟩≈0 · 밴드 안 → G4 침묵")
        chk(abs(r["P_mean_GPa"]) < 0.05,
            f"⛔음성: 창이 **마지막 {10:.0f} ps 만** 본다 — 앞 50 ps 의 P=5 GPa 가 안 섞인다 (⟨P⟩ {r['P_mean_GPa']:+.3f})")
        plan_old = {k: v for k, v in plan_ok.items() if k != "게이트_입력"}
        r2 = gate_check(_mkrun(td / "old", plan_old, _rows(1.9000, 0.00)), win_ps=10.0, log=lambda *a: None)
        chk(r2["record_has_gate_input"] is False and "역추적" in r2["출처"],
            "⛔음성: 게이트_입력 없는 옛 plan 을 **기록없음** 으로 잡고 역추적이라고 이름 붙인다")
        r3 = gate_check(_mkrun(td / "poff", plan_ok, _rows(1.9000, 0.50)), win_ps=10.0, log=lambda *a: None)
        chk(not r3["pressure_ok"], f"⛔음성: ⟨P⟩ {r3['P_mean_GPa']:+.2f} GPa 가 목표 0 에서 벗어난 것을 잡는다")
        r4 = gate_check(_mkrun(td / "thin", plan_ok, _rows(1.5717, 0.00)), win_ps=10.0, log=lambda *a: None)
        chk(r4["G4_fires"] and abs(r4["dev_pct_vs_center"] + 17.86) < 0.02,
            f"⛔음성: 밴드 밖 밀도에 G4 가 발화한다 ({r4['dev_pct_vs_center']:+.2f} %)")
        bad_card = td / "nocard.json"
        bad_card.write_text(json.dumps({"1_바꾸는_것": {}}, ensure_ascii=False), encoding="utf-8")
        try:
            read_band(bad_card); hit = False
        except KeyError:
            hit = True
        chk(hit, "⛔음성: 밴드 절이 없는 카드에서 기본값으로 때우지 않고 죽는다")
        empty = td / "empty"; empty.mkdir()
        (empty / "thermo.csv").write_text("t_ps,T_K\n", encoding="utf-8")
        try:
            read_thermo(empty / "thermo.csv"); hit2 = False
        except ValueError:
            hit2 = True
        chk(hit2, "⛔음성: 자료 줄 없는 thermo.csv 를 빈 배열로 넘기지 않는다")
    # ⑨ 회신 BR 이행: 유지 구간 블록 추세 · 통계 라벨 · G4 는 경보 (2026-09-14)
    def _rows_hold(rho_start, rho_end, n_hold=60):
        """melt(T_set 1200) → 램프 → hold(T_set 300). hold 동안 ρ 가 선형으로 rho_start→rho_end."""
        out = []
        for i in range(20):                              # melt
            out.append((float(i), 1200.0, 1200.0, 1.2000, 8000.0, -1000.0, 5.0, 0.0))
        for i in range(20):                              # 담금질 램프 (마지막 프레임이 T_set=300 이다)
            Tset = 1200.0 - (1200.0 - 300.0) * (i + 1) / 20.0
            out.append((float(20 + i), Tset, Tset, 1.4000 + (rho_start - 1.4000) * (i + 1) / 20.0,
                        8000.0, -1000.0, 1.0, 0.0))
        for i in range(n_hold):                          # hold
            f = i / max(1, n_hold - 1)
            out.append((float(40 + i), 300.0, 300.0, rho_start + (rho_end - rho_start) * f,
                        8000.0, -1000.0, 0.01 * ((-1) ** i), 0.0))
        return out
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        flat = gate_check(_mkrun(td / "flat", plan_ok, _rows_hold(1.9000, 1.9000)),
                          win_ps=10.0, n_blocks=5, log=lambda *a: None)
        ht = flat["hold_trend"]
        chk(ht["hold_from_ps"] == 39.0 and ht["n_frames"] == 61 and ht["n_blocks"] == 5,
            f"유지 구간을 담금질 램프와 갈라 잡는다 — 램프의 **마지막 프레임(T_set 이 이미 300)**을 포함한다 "
            f"({ht['hold_from_ps']:.0f}–{ht['hold_to_ps']:.0f} ps · {ht['n_frames']} 표본)")
        chk(abs(ht["rho_drift_pct_over_hold"]) < 1e-9 and abs(ht["block_rho_spread_pct"]) < 1e-9,
            "표류 없는 유지 구간은 표류 0 으로 나온다")
        drift = gate_check(_mkrun(td / "drift", plan_ok, _rows_hold(1.9000, 1.8620)),
                           win_ps=10.0, n_blocks=5, log=lambda *a: None)
        hd = drift["hold_trend"]
        chk(abs(hd["rho_drift_pct_over_hold"] + 2.0) < 0.15 and hd["rho_drift_pct_over_hold"] < -1.0,
            f"⛔음성: 유지 전체에 걸친 −2 % ρ 표류를 잡아낸다 ({hd['rho_drift_pct_over_hold']:+.3f} %)")
        chk(drift["rho_flat_pct"] < abs(hd["rho_drift_pct_over_hold"]) / 3.0,
            f"⛔음성: **10 ps 창이 표류를 축소해 보여준다** (창 범위/평균 {drift['rho_flat_pct']:.3f} % vs "
            f"유지 전체 {hd['rho_drift_pct_over_hold']:+.2f} %, {abs(hd['rho_drift_pct_over_hold'])/drift['rho_flat_pct']:.1f}배) "
            f"— 창만 보면 '평탄' 으로 오독한다")
        chk(hd["blocks"][0]["rho_mean"] > hd["blocks"][-1]["rho_mean"],
            "블록 평균이 표류 방향을 보여준다 (첫 블록 > 마지막 블록)")
        chk(flat["G4_role"] == "alert" and flat["G4_원인_지정"] is None,
            "G4 는 **경보**로 표시되고 원인을 지정하지 않는다 (D-2026-09-14-li2s-layer1-density-alert)")
        chk("확인되지 않았다" in flat["허용_서술"] and "총 수압" in flat["허용_서술"],
            "허용 서술이 '단기 관측 · 이완/이력/압력-부피 정확성 미확인' 을 달고 나간다")
        chk("표준편차" in flat["★_통계의_뜻"]["P_sd_GPa"] and "신뢰구간이 아니" in flat["★_통계의_뜻"]["P_sd_GPa"]
            and "검정한 값이 아니" in flat["★_통계의_뜻"]["rho_flat_pct"],
            "통계 라벨이 결과에 같이 실린다 (sd ≠ 신뢰구간 · 범위 ≠ 평형검정)")
        noTset = td / "noTset"; noTset.mkdir()
        (noTset / "plan.json").write_text(json.dumps(plan_ok, ensure_ascii=False), encoding="utf-8")
        with open(noTset / "thermo.csv", "w") as f:
            f.write("t_ps,T_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
            for i in range(30):
                f.write(f"{float(i):.4f},300.0,1.9,8000.0,-1000.0,0.0,0.0\n")
        r5 = gate_check(noTset, win_ps=10.0, log=lambda *a: None)
        chk("⛔" in r5["hold_trend"] and "T_set_K" in r5["hold_trend"]["⛔"],
            "⛔음성: T_set_K 없는 thermo 에서 유지 구간을 **추측하지 않고** 없다고 말한다")
    # ⑩ --mode_stress: 봉인된 프레임 표본 · 색인 대조 (2026-09-14, 회신 BR Q4)
    from ase import Atoms as _A
    from ase.io import write as _w
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        want, cpath = read_frame_card("db/properties/li2s_layer1_g2_mode_stress_prereg_2026_09_14.json")
        chk(want == [20.0, 50.0, 80.0, 200.0, 400.0, 700.0, 900.0, 1005.0, 1025.0, 1045.0],
            f"프레임 표본을 **카드에서** 읽는다 ({len(want)}점, 도구가 고르지 않는다)")
        badcard = td / "nocard.json"
        badcard.write_text(json.dumps({"1_프레임_표본_봉인": {}}, ensure_ascii=False), encoding="utf-8")
        try:
            read_frame_card(badcard); hit = False
        except KeyError:
            hit = True
        chk(hit, "⛔음성: t_ps 없는 카드에서 기본 표본을 지어내지 않고 죽는다")
        dupcard = td / "dup.json"
        dupcard.write_text(json.dumps({"1_프레임_표본_봉인": {"t_ps": [10, 10, 20]}}, ensure_ascii=False), encoding="utf-8")
        try:
            read_frame_card(dupcard); hit2 = False
        except ValueError:
            hit2 = True
        chk(hit2, "⛔음성: 중복된 프레임 목록을 거부한다")
        def _mk(n_traj, n_thermo, d):
            d.mkdir(parents=True, exist_ok=True)
            ats = [_A("Li2", positions=[[0, 0, 0], [1.5, 0, 0]], cell=np.eye(3) * 6, pbc=True)
                   for _ in range(n_traj)]
            (d / "traj.xyz").unlink(missing_ok=True)
            for a_ in ats:
                _w(str(d / "traj.xyz"), a_, format="extxyz", append=True)
            with open(d / "thermo.csv", "w") as f:
                f.write("t_ps,T_K,T_set_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
                for i in range(n_thermo):
                    f.write(f"{float(i):.3f},300.0,300.0,1.9,216.0,-1.0,0.0,0.0\n")
            return d
        good = _mk(6, 6, td / "ok")
        m, n = frame_index_map(good / "traj.xyz", good / "thermo.csv")
        chk(n == 6 and m[3.0] == 3 and m[0.0] == 0,
            f"프레임 수와 thermo 행 수가 맞으면 t_ps ↔ 색인을 만든다 ({n} 프레임)")
        mis = _mk(5, 6, td / "mismatch")
        try:
            frame_index_map(mis / "traj.xyz", mis / "thermo.csv"); hit3 = False
        except ValueError:
            hit3 = True
        chk(hit3, "⛔음성: traj 프레임 수 ≠ thermo 행 수면 **멈춘다** (간격을 추측하지 않는다)")
    # ⑪ --gb2: G-B2 겹침 (2026-09-18) — **음성 경로가 본체다**
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)

        # ⓐ 진짜 카드가 파싱되는가 — 사본을 안 만들기로 했으니 이게 배선의 전부다
        th, cpath = read_gb2_thresholds()
        chk(th == {"gr_first_peak_A": 0.05, "coord_mean": 0.3, "ps4_pp": 10.0, "r_window_A": 5.0},
            f"봉인된 카드 산문에서 G-B2 문턱 넷을 판다 {th}")

        raw = json.loads(pathlib.Path(cpath).read_text(encoding="utf-8"))
        g = raw["4_검증_게이트_결과_보기_전에_정한다"]["G-B2_겹침_🔴_이_카드의_핵심"]
        mang = td / "mangled.json"
        mang.write_text(json.dumps({"4_검증_게이트_결과_보기_전에_정한다": {
            "G-B2_겹침_🔴_이_카드의_핵심": {
                "문턱": g["문턱"].replace("PS₄ 보존율 차이가 **10 %p 이내**", "PS₄ 는 적당히"),
                "왜_r_≤_5_Å": g["왜_r_≤_5_Å"]}}}, ensure_ascii=False), encoding="utf-8")
        try:
            read_gb2_thresholds(mang); hitA = False
        except ValueError:
            hitA = True
        chk(hitA, "⛔음성: 문턱 하나가 산문에서 사라지면 **죽는다** (기본값을 지어내지 않는다)")

        noseg = td / "noseg.json"
        noseg.write_text(json.dumps({"4_검증_게이트_결과_보기_전에_정한다": {}}, ensure_ascii=False), encoding="utf-8")
        try:
            read_gb2_thresholds(noseg); hitB = False
        except KeyError:
            hitB = True
        chk(hitB, "⛔음성: G-B2 절이 없는 카드를 통과시키지 않는다")

        # ⓑ first_peak_A — 없는 것을 0 으로 그리지 않는다
        rr = np.arange(0.025, 8.0, 0.05)
        chk(first_peak_A(rr, np.zeros_like(rr), 5.0) is None,
            "⛔음성: 봉우리가 없으면 None — **0.0 으로 그리지 않는다**")
        gg = np.zeros_like(rr)
        gg[(rr > 2.0) & (rr < 2.1)] = 2.0          # 첫 봉우리 2.05 (낮음)
        gg[(rr > 4.0) & (rr < 4.1)] = 9.0          # 최대 봉우리 4.05
        pk = first_peak_A(rr, gg, 5.0)
        chk(pk is not None and abs(pk["first_A"] - 2.025) < 0.06 and abs(pk["global_A"] - 4.025) < 0.06
            and not pk["first_is_global"],
            "첫 봉우리 ≠ 최대 봉우리를 **구분해서 올린다** (조용히 하나를 고르지 않는다)")

        # ⓒ 합성 궤적 — 지표를 내가 정한 값으로 만든다
        _TET = np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]], float)
        _TET = _TET / np.linalg.norm(_TET[0])

        def _fix(scale=1.0, drop_S=False, li_on_cl=3):
            L = 14.0 * scale
            sym, pos = [], []
            for k, c in enumerate([(3.0, 3.0, 3.0), (3.0, 10.0, 10.0), (10.0, 3.0, 10.0)]):
                c = np.array(c, float) * scale
                sym.append("P"); pos.append(c)
                for j, v in enumerate(_TET):
                    r = 4.5 if (drop_S and k == 0 and j == 0) else 2.05
                    sym.append("S"); pos.append(c + v * r * scale)
            for m, cc in enumerate([(10.0, 10.0, 3.0), (7.0, 7.0, 12.0)]):
                cc = np.array(cc, float) * scale
                sym.append("Cl"); pos.append(cc)
                for q in range(li_on_cl):           # Cl 둘레 Li — 배위수를 손으로 정한다
                    ang = 2 * math.pi * q / max(li_on_cl, 1)
                    sym.append("Li")
                    pos.append(cc + np.array([math.cos(ang), math.sin(ang), 0.3]) * 2.5 * scale)
            return sym, np.array(pos, float), np.eye(3) * L

        FRAMES = [10.0, 20.0, 30.0]
        fcard = td / "frames.json"
        fcard.write_text(json.dumps({"1_프레임_표본_봉인": {"t_ps": FRAMES}}, ensure_ascii=False), encoding="utf-8")

        def _run(d, **kw):
            d = pathlib.Path(d); d.mkdir(parents=True, exist_ok=True)
            sym, pos, cell = _fix(**kw)
            (d / "traj.xyz").unlink(missing_ok=True)
            for _ in FRAMES:
                _w(str(d / "traj.xyz"), _A(sym, positions=pos, cell=cell, pbc=True),
                   format="extxyz", append=True)
            with open(d / "thermo.csv", "w") as f:
                f.write("t_ps,T_K,density_g_cm3,volume_A3,E_pot_eV,P_GPa,P_virial_GPa\n")
                for t in FRAMES:
                    f.write(f"{t:.3f},300.0,1.9,{abs(np.linalg.det(cell)):.1f},-1.0,0.0,0.0\n")
            return d

        _q = lambda *a, **k: None
        base = _run(td / "base")
        same = _run(td / "same")
        r_ok = gb2_compare(base, same, card=cpath, frame_card=fcard, log=_q)
        chk(r_ok["판정"] == "통과" and r_ok["요약"]["PS4_pp"]["max"] == 0.0,
            "[양성] 같은 구조 두 벌 → **통과** · 모든 차이 0")

        r_ps4 = gb2_compare(base, _run(td / "dropS", drop_S=True), card=cpath, frame_card=fcard, log=_q)
        chk(r_ps4["판정"] == "탈락" and r_ps4["요약"]["PS4_pp"]["max"] > 10.0,
            f"⛔음성: PS₄ 보존율이 {r_ps4['요약']['PS4_pp']['max']:.0f} %p 벌어지면 막는다")

        r_gr = gb2_compare(base, _run(td / "scaled", scale=1.06), card=cpath, frame_card=fcard, log=_q)
        chk(r_gr["판정"] == "탈락" and r_gr["요약"]["peak_PS"]["max"] > 0.05,
            f"⛔음성: g(r) 첫 봉우리가 {r_gr['요약']['peak_PS']['max']:.3f} Å 밀리면 막는다")

        r_cn = gb2_compare(base, _run(td / "moreLi", li_on_cl=6), card=cpath, frame_card=fcard, log=_q)
        chk(r_cn["판정"] == "탈락" and r_cn["요약"]["coord_Cl_Li"]["max"] > 0.3,
            f"⛔음성: Cl–Li 배위수 평균이 {r_cn['요약']['coord_Cl_Li']['max']:.2f} 벌어지면 막는다")

        badf = td / "badframes.json"
        badf.write_text(json.dumps({"1_프레임_표본_봉인": {"t_ps": [10.0, 999.0]}}, ensure_ascii=False),
                        encoding="utf-8")
        # ⚠ 다른 예외(KeyError 등)를 **통과로도, 죽음으로도** 두지 않는다 — 빨간줄로 만든다.
        #   깨보기 실측 2026-09-18: 가드를 빼면 뒤늦게 KeyError 가 나 selftest 전체가 죽었다.
        #   시험이 죽으면 그 뒤 시험이 안 돌아 — "빨간불 확인" 이 성립하지 않는다.
        hitC = None
        try:
            gb2_compare(base, same, card=cpath, frame_card=badf, log=_q); hitC = "통과시켰다"
        except ValueError:
            hitC = True
        except Exception as e:
            hitC = f"엉뚱한 예외 {type(e).__name__} — 가드가 아니라 뒤늦은 붕괴다"
        chk(hitC is True,
            "⛔음성: 봉인된 프레임이 traj 에 없으면 **대체하지 않고 ValueError 로 죽는다** (카드 §6)"
            + ("" if hitC is True else f"  ← {hitC}"))

        chk(r_ok["판정_규칙"].startswith("같은 t_ps 짝의"),
            "판정 규칙(짝지어 최댓값)을 결과 파일에 **적어서** 내보낸다")

    # ── NEB 끝점 게이트 (§0b-②-4) — UMA 없이 되는 부분만 ──────────────────
    #   ⛔ 이완 자체는 UMA 가 있어야 돌므로 여기서 안 친다. 대신 **판정 산수**와
    #     **문턱 판독**을 친다 — 조용히 틀릴 수 있는 곳이 거기다.
    th = read_neb_gate_thresholds("db/properties/lpscl_smallcell_neb_estimand_2026_09_18.json")
    chk(th == {"gate_A_li_min_A": 1.0, "gate_B_rmsd_max_A": 0.5},
        f"끝점 게이트 문턱을 **카드 산문에서** 읽는다 {th}")
    # ⛔음성 — 절이 없으면 **죽는다**. 기본값을 지어내지 않는다.
    import tempfile as _tf
    _bad = pathlib.Path(_tf.mkdtemp()) / "nocard.json"
    _bad.write_text('{"제목": "문턱 절이 없는 카드"}', encoding="utf-8")
    try:
        read_neb_gate_thresholds(str(_bad)); _died = False
    except KeyError:
        _died = True
    chk(_died, "⛔음성: 게이트 절이 없는 카드면 **죽는다** (기본값을 지어내지 않는다)")
    # ⛔음성 — 문구는 있는데 숫자가 없으면 죽는다
    _bad2 = pathlib.Path(_tf.mkdtemp()) / "nonum.json"
    _bad2.write_text(json.dumps({"0b_경로선택·집계_규칙_제안_2026_09_18": {"②_경로_선택_규칙": {
        "4_★_끝점_게이트_두_개_다_통과해야_후보다": {
            "게이트_A_서로_다른_최소": "두 위치 차가 충분히 크면 통과",
            "게이트_B_골격이_안_바뀜": "골격이 그대로면 통과"}}}}, ensure_ascii=False),
        encoding="utf-8")
    try:
        read_neb_gate_thresholds(str(_bad2)); _died2 = False
    except ValueError:
        _died2 = True
    chk(_died2, "⛔음성: 산문에 숫자가 없으면 **죽는다** (문구만 보고 통과시키지 않는다)")

    # mic_dist — 셀 경계를 넘는 짝
    _c = np.eye(3) * 10.0
    chk(abs(mic_dist([0.5, 0, 0], [9.5, 0, 0], _c) - 1.0) < 1e-9,
        "mic_dist: 경계를 넘는 짝을 **1.0 Å** 로 본다 (9.0 이 아니다)")

    # non_li_rmsd — Li 를 **빼고** 잰다
    from ase import Atoms as _A
    _s = ["Li", "Li", "P", "S"]
    _p0 = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]], float)
    _p1 = _p0.copy(); _p1[0, 0] += 5.0                       # Li 만 크게 움직인다
    r, n, dm = non_li_rmsd(_A(_s, positions=_p0, cell=_c, pbc=True),
                           _A(_s, positions=_p1, cell=_c, pbc=True))
    chk(abs(r) < 1e-9 and n == 2,
        f"⛔음성: Li 가 5 Å 움직여도 골격 RMSD 는 **0** 이다 (n_framework={n}, rmsd={r:.4f})")
    _p2 = _p0.copy(); _p2[3, 0] += 1.0                       # S 가 움직인다
    r2, _, _ = non_li_rmsd(_A(_s, positions=_p0, cell=_c, pbc=True),
                           _A(_s, positions=_p2, cell=_c, pbc=True))
    chk(abs(r2 - (1.0 / np.sqrt(2))) < 1e-9,
        f"골격 원자 하나가 1 Å 움직이면 RMSD = 1/√2 = {r2:.4f} (2 원자 중 하나)")

    # ── endpoint_gate **본문**을 탄다 (UMA 대신 stub 계산기) ─────────────
    #   ⛔ 2026-09-18 실측: 위 시험들은 헬퍼만 불렀고 함수 본문은 한 번도 안 탔다.
    #     그래서 본문의 `_today()` NameError 가 **kgy 에서 9 건을 다 돌린 뒤에야**
    #     JSON 쓰기 직전에 터졌다. 이 파일이 같은 실패(함수만 시험, 배선은 안 탐)를
    #     겪은 세 번째다. stub 계산기로 전 경로를 태운다.
    from ase import Atoms as _A2
    from ase.calculators.lj import LennardJones as _LJ
    _td = pathlib.Path(_tf.mkdtemp()) / "events"; _td.mkdir(parents=True)
    _cell = np.eye(3) * 12.0
    _sym2 = ["Li", "Li", "P", "S", "S", "Cl"]
    _base = np.array([[1, 1, 1], [5, 1, 1], [3, 3, 3], [3, 5, 3], [5, 3, 3], [8, 8, 8]], float)
    _evs = []
    for k, (ai, dx) in enumerate([(0, 2.0), (1, 0.2)], 1):
        tag = f"ev{k:02d}_atom{ai}"
        for side, shift in (("i", 0.0), ("f", dx)):
            q = _base.copy(); q[ai, 0] += shift
            _A2(_sym2, positions=q, cell=_cell, pbc=True).write(str(_td / f"{tag}_{side}.xyz"))
        _evs.append({"tag": tag, "atom_index": ai, "disp_A": dx,
                     "t_start_ps": 0.0, "t_end_ps": 5.0})
    (_td / "events.json").write_text(json.dumps({"events": _evs}, ensure_ascii=False),
                                     encoding="utf-8")
    _real_make_calc = make_calc
    try:
        globals()["make_calc"] = lambda turbo=False, device="cuda": _LJ(epsilon=0.01, sigma=2.5)
        _r = endpoint_gate(str(_td), out_json=str(_td / "g.json"),
                           card="db/properties/lpscl_smallcell_neb_estimand_2026_09_18.json",
                           steps=2, log=lambda *a, **k: None)
    finally:
        globals()["make_calc"] = _real_make_calc
    chk(_r["n_events"] == 2, f"[배선] endpoint_gate 본문이 끝까지 돈다 (사건 {_r.get('n_events')})")
    chk((_td / "g.json").exists(), "[배선] 결과 JSON 을 **쓴다** (여기서 _today() NameError 가 났었다)")
    _need = {"date", "kind", "⛔_gate_engine", "thresholds", "rows",
             "provisional_n_survive", "provisional_reject_rate", "⇒_§0b_②_5"}
    chk(_need <= set(_r), f"[배선] 결과에 필수 키가 다 있다 (빠진 것: {_need - set(_r)})")
    chk("게이트를 **집행하지 않는다**" in _r["⛔_gate_engine"],
        "⛔음성: 결과가 스스로 **비준된 게이트가 아님**을 말한다")
    _rows = {r["tag"]: r for r in _r["rows"]}
    chk(_rows["ev01_atom0"]["li_sep_after_relax_A"] > _rows["ev02_atom1"]["li_sep_after_relax_A"],
        "[배선] 많이 움직인 쪽이 이완 후에도 더 벌어져 있다 (자리를 안 뒤바꾼다)")
    chk(all(isinstance(r["rejected_because"], list) for r in _r["rows"]),
        "기각 사유를 사건마다 **적는다** (빈 리스트라도 자리가 있다)")
    # ⓑ 카드 §2 가 요구하는 원시량 — 전에는 판정만 하고 **버렸다**
    _r0 = _r["rows"][0]
    chk({"E_i_eV", "E_f_eV", "dE_f_minus_i_eV"} <= set(_r0),
        f"[배선] 끝점 에너지 E_i·E_f·ΔE 를 남긴다 (ⓑ 카드 §2 원시량)")
    chk(abs(_r0["dE_f_minus_i_eV"] - (_r0["E_f_eV"] - _r0["E_i_eV"])) < 1e-6,
        "ΔE 가 E_f − E_i 와 일치한다 (부호를 뒤집지 않는다)")
    _rx = [_td / x for x in _r0["relaxed_xyz"]]
    chk(all(q.exists() for q in _rx),
        f"[배선] **이완된** 끝점 구조를 파일로 남긴다 (NEB 출발점이다)")
    # ⛔음성 — 저장된 것이 이완 **전** 구조면 안 된다
    from ase.io import read as _rd
    _a_raw = _rd(str(_td / f"{_r0['tag']}_i.xyz"))
    _a_rel = _rd(str(_rx[0]))
    chk(np.abs(_a_raw.get_positions() - _a_rel.get_positions()).max() > 1e-6,
        "⛔음성: 저장된 것이 **이완 후** 구조다 (원본을 그대로 복사하지 않는다)")

    # ── --seed_gate: 원시(traj 마지막 프레임)·relax 본(final.xyz) 두 판 (2026-09-24) ──
    import tempfile as _tf
    from ase import Atoms as _At
    from ase.io import write as _wsg, read as _rsg
    _q = lambda *a, **k: None
    _sym, _pos, _cell = build_random_cell("A", seed=3, n_fu=4)
    _rng = np.random.default_rng(7)
    _frames = [_At(_sym, positions=_pos + _rng.normal(0, 0.05, _pos.shape), cell=_cell, pbc=True) for _ in range(3)]
    _frames[-1].positions[0] += _cell[0]        # 원시 NPT 궤적처럼 셀 밖 좌표 — 뽑을 때 감겨야 한다
    _plan = {"melt_ps": 1.0, "quench_ps": 0.0, "hold_ps": 1.0, "save_ps": 1.0,
             "게이트_입력": {"final_relax": FINAL_RELAX}}

    def _mk_sg(name, traj=True, final="relaxed", plan=_plan):
        d = pathlib.Path(_tf.mkdtemp()) / "A" / name
        d.mkdir(parents=True)
        if traj:
            for f in _frames:
                _wsg(str(d / "traj.xyz"), f, format="extxyz", append=True)
        fin = _frames[-1].copy()
        if final == "relaxed":
            fin.positions += np.random.default_rng(11).normal(0, 0.03, _pos.shape)
        _wsg(str(d / "final.xyz"), fin, format="extxyz")
        (d / "plan.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        return d

    _d1 = _mk_sg("seed9")
    _g1 = seed_gate(_d1, log=_q)
    chk(bool(_g1["raw"]) and bool(_g1["relaxed"]), "--seed_gate: 원시·relax 두 판을 다 찍는다")
    chk(_g1["raw"]["frame"] == 2 and _g1["raw"]["t_ps"] == 2.0 and not _g1["warnings"],
        "--seed_gate: 원시 = traj **마지막** 프레임 (프레임 2 · t 2 ps · 길이 plan 과 일치)")
    chk(_g1["raw_vs_relaxed"]["disp_max_A"] > 1e-3,
        "⛔음성: relax 본과 원시를 **구분**한다 (변위 > 0 — final.xyz 를 원시로 읽으면 0 이 된다)")
    _rf = _rsg(str(_d1 / SEED_GATE_RAW))
    _dd = (_rf.get_positions() - _frames[-1].get_positions()) @ np.linalg.inv(_cell)
    _sp = _rf.get_scaled_positions(wrap=False)
    chk(np.linalg.norm((_dd - np.round(_dd)) @ _cell, axis=1).max() < 1e-6
        and _sp.min() > -1e-9 and _sp.max() < 1 + 1e-9,
        "--seed_gate: md_init_raw.xyz = 원시 마지막 프레임 (최소상 동일 · 셀 안으로 감김)")
    chk(bool(_rf.info.get("raw")) and int(_rf.info.get("frame")) == 2,
        "--seed_gate: md_init_raw.xyz 가 출처(원시 · 프레임 번호)를 달고 있다")
    chk(_g1["raw"]["min_pair_excl_PS_kind"] != "P-S",
        "--seed_gate: '최단·P–S 제외' 에 P–S 쌍이 안 들어간다")
    _g1b = seed_gate(_d1, log=_q)
    chk(_g1b["md_init_raw"]["status"] == "이미 있음 · 같음",
        "--seed_gate: 다시 돌려도 같은 원시면 그대로 둔다 (멱등)")
    _d2 = _mk_sg("seed8", traj=False)
    _g2 = seed_gate(_d2, log=_q)
    chk(_g2["raw"] is None and "대신하지 않는다" in _g2.get("raw_why", "") and not (_d2 / SEED_GATE_RAW).exists(),
        "⛔음성: traj 가 없으면 원시 칸을 비운다 — final.xyz 를 원시로 쓰지도, md_init_raw.xyz 를 만들지도 않는다")
    _g3 = seed_gate(_mk_sg("seed7", final="same"), log=_q)
    chk(any("원시와 같다" in w for w in _g3["warnings"]),
        "⛔음성: final.xyz 가 원시와 똑같으면 경보한다 (relax 본이어야 할 파일)")
    _g4 = seed_gate(_mk_sg("seed6", plan=dict(_plan, hold_ps=8.0)), log=_q)
    chk(any("잘렸다" in w for w in _g4["warnings"]),
        "⛔음성: traj 가 plan 길이보다 짧으면 경보한다 (마지막 프레임 ≠ 유지 끝)")
    _bad = _rf.copy()
    _bad.positions[0] += 0.5
    _wsg(str(_d1 / SEED_GATE_RAW), _bad, format="extxyz")
    try:
        seed_gate(_d1, log=_q)
        _ok_ow = False
    except SystemExit as e:
        _ok_ow = "덮어쓰지 않는다" in str(e)
    chk(_ok_ow, "⛔음성: 이미 있는 md_init_raw.xyz 가 다르면 덮어쓰지 않고 멈춘다")

    # ── 모델 검증 경로 (--eos_path) — 가짜 계산기 (LJ) 로 배선만 본다 (UMA 아님) ──
    import tempfile as _tf
    from ase import Atoms as _At
    from ase.calculators.lj import LennardJones as _LJ
    chk(eos_label("x/A/seed3/final.xyz") == "A_s3" and eos_label("y/B/seed12/final.xyz") == "B_s12",
        "--eos_path: 경로에서 라벨 (A_s3 · B_s12)")
    try:
        eos_label("x/C/seed3/final.xyz"); _ok_l = False
    except SystemExit:
        _ok_l = True
    chk(_ok_l, "⛔음성: <A|B>/seed<N> 꼴이 아니면 라벨을 추측하지 않고 멈춘다")
    _mv, _ = read_mc_values()
    with _tf.TemporaryDirectory() as _td:
        _td = pathlib.Path(_td)
        _sd = _td / "B" / "seed9"; _sd.mkdir(parents=True)
        _at = _At("PS4LiCl", positions=[[4, 4, 4], [5.2, 5.2, 5.2], [2.8, 2.8, 5.2], [2.8, 5.2, 2.8], [5.2, 2.8, 2.8],
                                        [1.0, 1.0, 1.0], [6.8, 1.2, 6.8]], cell=[8.0, 8.0, 8.0], pbc=True)
        from ase.io import write as _w
        _w(str(_sd / "final.xyz"), _at, format="extxyz")
        _lj = _LJ(sigma=2.0, epsilon=0.01, rc=5.0); _lj._mq_mode = "default"
        _q = lambda *a, **k: None
        _r = eos_path([_sd / "final.xyz"], _td / "out", calc=_lj, log=_q)["B_s9"]
        _xs = [p["x"] for p in _r["points"]]
        chk(_xs == sorted(float(x) for x in _mv["path_scales"]), f"--eos_path: 카드 격자 그대로 {_xs}")
        _V0 = _r["meta"]["V_final_A3"]
        chk(all(abs(p["V_A3"] / _V0 - p["x"]) < 1e-9 for p in _r["points"]), "--eos_path: 점마다 V/V_final = x (등방 스케일)")
        chk(all(p["converged"] and p["Fmax_eV_A"] <= float(_mv["relax_fmax_eV_A"]) + 1e-12 for p in _r["points"]),
            "--eos_path: 점마다 카드 fmax 로 수렴")
        chk(_r["meta"]["mode"] == "default" and _r["meta"]["relax"]["cell"] == "fixed", "--eos_path: 모드 default · 고정셀 기록")
        chk(all((_td / "out" / "B_s9" / p["geom"]).is_file() for p in _r["points"]), "--eos_path: 점마다 기하 파일")
        _logs = []
        eos_path([_sd / "final.xyz"], _td / "out", calc=_lj, log=lambda m: _logs.append(m))
        chk(len(_logs) == len(_xs) and all("이미 있음" in m for m in _logs), "--eos_path: 다시 부르면 다 건너뛴다 (재개)")
        _lj2 = _LJ(sigma=2.0, epsilon=0.01, rc=5.0); _lj2._mq_mode = "turbo"
        try:
            eos_path([_sd / "final.xyz"], _td / "out2", calc=_lj2, log=_q); _ok_t = False
        except SystemExit:
            _ok_t = True
        chk(_ok_t, "⛔음성: turbo 계산기면 멈춘다 (카드 default)")
        _at.positions[0] += 0.3
        _w(str(_sd / "final.xyz"), _at, format="extxyz")
        try:
            eos_path([_sd / "final.xyz"], _td / "out", calc=_lj, log=_q); _ok_s = False
        except SystemExit:
            _ok_s = True
        chk(_ok_s, "⛔음성: 입력 sha 가 바뀐 구조를 옛 경로 json 에 섞지 않고 멈춘다")
        (_td / "c.json").write_text(json.dumps({"x": 1}), encoding="utf-8")
        try:
            read_mc_values(str(_td / "c.json")); _ok_c = False
        except KeyError:
            _ok_c = True
        chk(_ok_c, "⛔음성: 기계_판독_값 없는 카드 → KeyError")

    print(f"selftest: ⭕ {ok} · ⛔ {bad}")
    return 0 if bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description="LPSCl@Li₂S 1층 melt-quench (UMA NPT)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--system", choices=sorted(SYSTEMS), help="A · B · control_li7ps6 (카드 §2)")
    ap.add_argument("--seed", type=int, help="담금질 시드 (G3: ≥ 5개, 호출마다 하나)")
    ap.add_argument("--n_fu", type=int, help="식단위 수 (기본: A 40 · B 50 · control 28)")
    ap.add_argument("--density", type=float, default=1.2, help="시작 밀도 g/cm³ (NPT 가 고친다; 음이온 3 Å 배제라 1.5 도 못 채운다)")
    ap.add_argument("--T_melt", type=float, default=1200.0)
    ap.add_argument("--T_final", type=float, default=300.0)
    ap.add_argument("--melt_ps", type=float, default=100.0)
    ap.add_argument("--quench_rate", type=float, help="K/s — G2 선언값. 기본값 없음 (예: 1e12 → 900 ps)")
    ap.add_argument("--hold_ps", type=float, default=50.0)
    ap.add_argument("--dt_fs", type=float, default=2.0)
    ap.add_argument("--save_ps", type=float, default=1.0)
    ap.add_argument("--run_id", default=None,
                    help="⭐li2s-2: 러너가 담금질마다 주는 실행 식별자 (32 hex · plan.json run_id · 장부 run_id 와 묶는다 — 회신 DH P0-2)")
    ap.add_argument("--fix_density", type=float, default=None,
                    help="⭐li2s-2: 담금질을 NVT 로 — melt 첫 --compress_ps 동안 이 밀도 [g/cm³] 로 압축한 뒤 고정 "
                         "(같은 Berendsen 열욕 · 바로스탯 없음). 안 주면 옛 NPT 0 GPa 그대로")
    ap.add_argument("--compress_ps", type=float, default=20.0, help="--fix_density 압축 구간 [ps] (melt 안 · 기본 20)")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--turbo", action="store_true", help="fairchem inference_settings='turbo' 시도 (없으면 기본으로 내려가고 기록)")
    ap.add_argument("--out_root", help="출력 루트 → <out_root>/<system>/seed<seed>/")
    ap.add_argument("--pcheck", nargs="+", metavar="STRUCT",
                    help="⭐구조 파일들의 **단일점 압력**을 UMA 로 찍는다 (완화 없음). "
                         "고정 셀 MD 가 어떤 내부 압력에서 돌고 있는지 보는 용도")
    ap.add_argument("--melt_window_check", metavar="RUN_DIR",
                    help="⭐li2s-2 녹음 판정 (회신 DF P0) — 압축 뒤 창 안 프레임 · 창 안 시간원점만 · 카드 문턱. 종료 0 통과 · 2 미충족 · 3 미완 · 4 무효")
    ap.add_argument("--stage1_verdict", nargs="+", metavar="RUN_DIR",
                    help="⭐li2s-2 1 단계 시드 판정 (일정 완주 · 유지 구간 · 압력 기록 · 밀도 · 녹음 · 시드 게이트 · 카드 일정) → stage1_verdict.json")
    ap.add_argument("--stage1_summary", metavar="OUT_ROOT",
                    help="⭐li2s-2 1 단계 묶음 판정 (판정 지문 다시 잼 · 선언 시드 전부 판정 끝 · 첫 시드 녹음 미충족 = 그 계 닫힘 · "
                         "한쪽 탈락 = 트랙 멈춤 · 비용 장부 > 상한 = 미완결 · 2 단계 시드 = 공통 통과 중 작은 둘). "
                         "종료 0 통과 · 2 멈춤 · 3 대기 · 4 무효 · 5 상한 미완결")
    ap.add_argument("--li2s2_card", default=LI2S2_CARD, help="li2s-2 카드 (기계_판독_값 출처 — 도구가 문턱을 자체 보관하지 않는다)")
    ap.add_argument("--melt_check", metavar="RUN_DIR",
                    help="⭐이미 끝난 런에서 melt 구간 P 골격이 확산했는지 본다 (새 계산 없음)")
    ap.add_argument("--d_melt_cm2_s", type=float, default=1e-6, help="--melt_check 액체 판정 진단 문턱")
    ap.add_argument("--npt_control", metavar="STRUCT",
                    help="⭐배로스탯 대조 잡: 결정 구조 파일(.vasp/.cif/.xyz)을 같은 NPT 배선에 넣어 밀도 유지 확인")
    ap.add_argument("--control_repeat", type=int, default=None,
                    help="--npt_control 셀 반복을 손으로 고정 (기본: --control_min_width 를 채우도록 자동)")
    ap.add_argument("--control_min_width", type=float, default=9.0,
                    help="--npt_control 최소 면간거리 [Å] — 원자 수가 아니라 이 폭이 MIC 기준이다 (기본 9.0)")
    ap.add_argument("--control_ps", type=float, default=20.0, help="--npt_control NPT 길이 [ps]")
    ap.add_argument("--control_no_cellrelax", action="store_true",
                    help="--npt_control 에서 0 K 가변셀 완화를 건너뛴다 (기준이 **파일 밀도**로 바뀐다)")
    ap.add_argument("--control_max_relax_dV", type=float, default=0.10,
                    help="0 K 완화가 부피를 이보다 더 바꾸면 멈춘다 — 그만큼 움직이면 대조가 아니다 (기본 0.10)")
    ap.add_argument("--control_p_tol", type=float, default=0.10,
                    help="배선 통과 문턱 |⟨P_total⟩| [GPa] — **판정은 압력이다** (밀도 drift 는 열팽창)")
    ap.add_argument("--control_tol", type=float, default=0.03, help="--npt_control 통과 문턱 |Δρ/ρ_UMA(0K)|")
    ap.add_argument("--control_out", help="--npt_control 출력 폴더 (기본 <out_root>/npt_control)")
    ap.add_argument("--dry_run", action="store_true", help="셀만 만들고 계획을 찍는다 (UMA 안 부름)")
    ap.add_argument("--gate_check", metavar="RUN_DIR",
                    help="plan.json 의 앙상블 선언 + thermo.csv 대조 + G4 밴드 (판정 아님, 기록 점검)")
    ap.add_argument("--seed_gate", nargs="+", metavar="RUN_DIR",
                    help="시드 게이트 입력(PS₄·다리 S·P–P·최단 원자간·밀도)을 **원시(traj 마지막 프레임)·relax 본"
                         "(final.xyz)** 두 판으로 찍고, 원시 판을 md_init_raw.xyz 로 떨군다 (판정 안 함 · seed_gate.json)")
    ap.add_argument("--no_write_raw", action="store_true",
                    help="--seed_gate 에서 md_init_raw.xyz 를 쓰지 않는다 (읽기만)")
    ap.add_argument("--band_card", default=BAND_CARD, help="--gate_check G4 밴드 출처 카드")
    ap.add_argument("--gate_win_ps", type=float, default=10.0, help="--gate_check 평균 창 [ps]")
    ap.add_argument("--mode_stress", metavar="RUN_DIR",
                    help="⭐봉인된 프레임에서 turbo − default 의 응력·힘 차이 (새 MD 0, 회신 BR Q4)")
    ap.add_argument("--frame_card", default="db/properties/li2s_layer1_g2_mode_stress_prereg_2026_09_14.json",
                    help="--mode_stress 프레임 표본 카드 (도구가 프레임을 고르지 않는다)")
    ap.add_argument("--eos_path", nargs="+", metavar="STRUCT",
                    help="모델 검증 카드 §1b — …/<A|B>/seed<N>/final.xyz 마다 등방 경로 UMA default 고정셀 이완 (--eos_out 필요)")
    ap.add_argument("--eos_out", help="--eos_path 출력 루트 → <eos_out>/<A_sN>/uma_path.json · x<..>.xyz")
    ap.add_argument("--eos_which", choices=("main", "ext_low", "ext_high"), default="main",
                    help="--eos_path 격자: 카드 path_scales (기본) · 연장 점 (판독 도구가 연장 규칙을 말할 때만)")
    ap.add_argument("--gb2", nargs=2, metavar=("RUN_SMALL", "RUN_BIG"),
                    help="G-B2 겹침 — 소셀 런디렉터리와 400 원자 런디렉터리. 새 계산 0")
    ap.add_argument("--gb2_card", default=GB2_CARD,
                    help="--gb2 문턱 출처 카드 (도구가 문턱을 자체 보관하지 않는다)")
    ap.add_argument("--gb2_out", help="--gb2 결과 JSON 경로 (기본 <RUN_SMALL>/gb2_overlap.json)")
    ap.add_argument("--endpoint_gate", metavar="EVENTS_DIR",
                    help="NEB 끝점 게이트 A/B **UMA 탐침** (카드 §0b-②-4). "
                         "⛔ 비준된 게이트(QE)를 집행하지 않는다 — 기각률을 먼저 본다")
    ap.add_argument("--endpoint_gate_out", help="--endpoint_gate 결과 JSON 경로")
    ap.add_argument("--neb_card", default=NEB_CARD,
                    help="--endpoint_gate 문턱 출처 카드 (도구가 문턱을 자체 보관하지 않는다)")
    ap.add_argument("--hold_blocks", type=int, default=5,
                    help="--gate_check 유지 구간을 몇 블록으로 나눠 추세를 볼지 (회신 BR Q3: 제일 싼 첫 단계)")
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if a.eos_path:
        if not a.eos_out:
            raise SystemExit("⛔ --eos_path 는 --eos_out 이 필요하다")
        for s in a.eos_path:
            if not pathlib.Path(s).is_file():
                raise SystemExit(f"⛔ 구조 파일이 없다: {s}")
        r = eos_path(a.eos_path, a.eos_out, which=a.eos_which, device=a.device, log=_flushing_print)
        n_bad = sum(1 for J in r.values() for p in J["points"] if not p["converged"])
        print(f"■ 끝 — 구조 {len(r)} · 점 {sum(len(J['points']) for J in r.values())} · 미수렴 {n_bad}")
        raise SystemExit(0 if n_bad == 0 else 2)
    if a.endpoint_gate:
        r = endpoint_gate(a.endpoint_gate,
                          out_json=a.endpoint_gate_out or
                          str(pathlib.Path(a.endpoint_gate).parent / "endpoint_gate_uma.json"),
                          card=a.neb_card, device=a.device, turbo=a.turbo)
        raise SystemExit(0 if r["n_events"] else 3)
    if a.gb2:
        r = gb2_compare(a.gb2[0], a.gb2[1], a.gb2_card, a.frame_card)
        out = pathlib.Path(a.gb2_out) if a.gb2_out else pathlib.Path(a.gb2[0]) / "gb2_overlap.json"
        out.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"→ {out}")
        #: 통과 0 · 탈락 2 · 미판정 3 — **미판정을 통과로 내보내지 않는다**
        raise SystemExit({"통과": 0, "탈락": 2}.get(r["판정"], 3))
    if a.mode_stress:
        r = mode_stress(a.mode_stress, a.frame_card, a.device)
        out = pathlib.Path(a.mode_stress) / "mode_stress.json"
        out.write_text(json.dumps({k: v for k, v in r.items()}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"→ {out}")
        return
    if a.gate_check:
        r = gate_check(a.gate_check, a.band_card, a.gate_win_ps, n_blocks=a.hold_blocks)
        (pathlib.Path(a.gate_check) / "gate_check.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        raise SystemExit(0 if (r["record_has_gate_input"] and r["gate_ok"]) else 2)
    if a.seed_gate:
        rows = []
        for rd in a.seed_gate:
            r = seed_gate(rd, write_raw=not a.no_write_raw)
            (pathlib.Path(rd) / "seed_gate.json").write_text(json.dumps(r, ensure_ascii=False, indent=1),
                                                             encoding="utf-8")
            rows.append(r)
            print()
        print("⛔ 판정하지 않았다 — 게이트를 원시·relax 어느 판으로 잴지, 문턱이 무엇인지는 카드·사람 몫이다.")
        #: 0 = 두 판 다 찍음 · 2 = 한 판이라도 비었음 (**비었음을 통과로 내보내지 않는다**)
        raise SystemExit(0 if all(x["raw"] and x["relaxed"] for x in rows) else 2)
    if a.pcheck:
        from ase.io import read
        calc = make_calc(a.device, a.turbo)
        print(f"UMA {getattr(calc, '_mq_mode', 'default')} · 단일점 (완화 없음) — 우리 MD 셀의 내부 압력")
        for f in a.pcheck:
            at = read(f); at.calc = calc
            w = cell_widths_A(at.get_cell())
            print(f"  {pathlib.Path(f).name:40s} {len(at):4d}원자 ρ {density_g_cm3(at):.3f} g/cm³ "
                  f"폭 {w.min():5.2f} Å  P(virial, 0 K) {pressure_GPa(at, include_ideal_gas=False):+7.3f} GPa")
        print("  ⛔ 이건 **그 셀에서의 압력**이다. 양수면 UMA 가 더 큰 셀을 원한다는 뜻이고, "
              "그 자체가 구조가 틀렸다는 뜻은 아니다 (DFT 로 완화한 셀이면 UMA-DFT 차이다).")
        return
    if a.melt_window_check:
        res = melt_window_check(a.melt_window_check, card=a.li2s2_card)
        print(json.dumps({k: res.get(k) for k in ("verdict", "message", "D_framework_cm2_s", "window_used_ps", "n_frames_read")},
                         ensure_ascii=False))                 # ⭐ DP 전 리뷰 (둘째) — 런 폴더에 쓰지 않는다 (MID_RUN_FILES 밖 파일 = 폴더 판독 보류)
        raise SystemExit({"pass": 0, "fail": 2, "incomplete": 3}.get(res["verdict"], 4))
    if a.stage1_verdict:
        rcs = [STAGE1_RC.get(stage1_verdict(rd, card=a.li2s2_card)["status"], 4) for rd in a.stage1_verdict]
        raise SystemExit(max(rcs))
    if a.stage1_summary:
        res = stage1_summary(a.stage1_summary, card=a.li2s2_card)
        raise SystemExit(SUMMARY_RC.get(res["track"], 4))
    if a.melt_check:
        res = melt_check(a.melt_check, d_melt_cm2s=a.d_melt_cm2_s)
        (pathlib.Path(a.melt_check) / "melt_check.json").write_text(
            json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(json.dumps({k: res[k] for k in ("verdict", "framework_diffused", "fit_window_ps",
                                              "d_melt_threshold_cm2_s")}, ensure_ascii=False))
        print("⭕ 녹았다 — 밀도는 물리다. G4 밴드 쪽을 본다" if res["framework_diffused"]
              else "⛔ 안 녹았다 — 이 담금질의 밀도는 생성기 채움밀도다. melt 조건을 먼저 고친다")
        return
    if a.npt_control:
        if not os.path.isfile(a.npt_control):
            raise SystemExit(f"⛔ 구조 파일이 없다: {a.npt_control}")
        from ase.io import read
        at = read(a.npt_control)
        rep = ((a.control_repeat,) * 3 if a.control_repeat else auto_repeat(at.get_cell(), a.control_min_width))
        at = at.repeat(rep); at.pbc = True
        cout = pathlib.Path(a.control_out or (pathlib.Path(a.out_root or ".") / "npt_control"))
        _w = cell_widths_A(at.get_cell())
        print(f"[대조 잡] {a.npt_control} ×{rep} = {len(at)} 원자 · 면간거리 최소 {_w.min():.2f} Å "
              f"({'자동' if not a.control_repeat else '손지정'}) · {a.T_final:.0f} K · {a.control_ps:.0f} ps → {cout}", flush=True)
        calc = make_calc(a.device, a.turbo)
        res = run_npt_control(at, calc, cout, T_K=a.T_final, ps=a.control_ps, dt_fs=a.dt_fs,
                              tol=a.control_tol, p_tol=a.control_p_tol, min_width_A=a.control_min_width,
                              cell_relax=not a.control_no_cellrelax,
                              max_relax_dV=a.control_max_relax_dV)
        res["repeat"] = list(rep)
        res["uma_inference_mode"] = getattr(calc, "_mq_mode", "default")
        res["structure_file"] = a.npt_control
        (cout / "control.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
        print(json.dumps({k: res[k] for k in ("rho_file_g_cm3", "rho_UMA_0K_g_cm3", "P_UMA_0K_GPa",
                                              "rho_NPT_mean_last_half_g_cm3", "P_NPT_mean_last_half_GPa",
                                              "drift_vs_UMA_0K", "alpha_V_apparent_per_K",
                                              "reference_for_drift", "UMA_vs_file", "P_tol_GPa",
                                              "plumbing_ok", "min_cell_width_A", "cell_wide_enough",
                                              "cell_relax", "cell_relax_note", "PS4_fraction_file")},
                         ensure_ascii=False, indent=1))
        if not res["cell_wide_enough"]:
            print(f"⚠ 셀 폭 {res['min_cell_width_A']:.2f} Å < {a.control_min_width} Å — 이 판정은 조건부다")
        print(f"⭕ 배선 정상 — ⟨P⟩ {res['P_NPT_mean_last_half_GPa']:+.3f} GPa 가 0 을 지킨다"
              if res["plumbing_ok"] else
              f"⛔ 배선 이상 — ⟨P⟩ {res['P_NPT_mean_last_half_GPa']:+.3f} GPa (허용 ±{res['P_tol_GPa']})")
        print(f"   밀도 {res['rho_file_g_cm3']:.3f}(파일) → "
              f"{('%.3f' % res['rho_UMA_0K_g_cm3']) if res['rho_UMA_0K_g_cm3'] else '—'}(0K) → "
              f"{res['rho_NPT_mean_last_half_g_cm3']:.3f}({a.T_final:.0f}K) · "
              f"0K→T 변화 {100*res['drift_vs_UMA_0K']:+.2f} % = **열팽창, 판정 아님**")
        return
    if not (a.system and a.seed is not None and a.out_root):
        ap.error("--system · --seed · --out_root 가 필요하다")
    quench_ps, n_q = schedule(a.T_melt, a.T_final, a.quench_rate, a.dt_fs)
    validate_fix_density(a.fix_density, a.compress_ps, a.melt_ps)
    sym, pos, cell = build_random_cell(a.system, a.seed, a.density, a.n_fu)
    out = pathlib.Path(a.out_root) / a.system / f"seed{a.seed}"; out.mkdir(parents=True, exist_ok=True)
    plan = build_plan(a.system, a.seed, sym, a.density, a.T_melt, a.T_final, a.melt_ps,
                      a.quench_rate, quench_ps, a.hold_ps, a.dt_fs, a.save_ps,
                      fix_density=a.fix_density, compress_ps=a.compress_ps)
    if a.run_id is not None and not RUN_ID_RE.match(a.run_id):
        raise SystemExit(f"⛔ --run_id {a.run_id!r} 는 32 자리 소문자 hex 여야 한다 (러너가 준다)")
    plan["run_id"] = a.run_id
    (out / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    from ase import Atoms
    from ase.io import write
    at = Atoms(symbols=sym, positions=pos, cell=cell, pbc=True)
    write(str(out / "initial.xyz"), at, format="extxyz")
    print(f"[{a.system} seed{a.seed}] {len(sym)} 원자 · 셀 {cell[0,0]:.2f} Å · 담금질 {quench_ps:.0f} ps ({n_q} 스텝) → {out}", flush=True)
    print(("  앙상블: NPT Berendsen 0 GPa (옛 경로)" if a.fix_density is None else
           f"  앙상블: NVT 고정 밀도 {a.fix_density:.5f} g/cm³ (melt 첫 {a.compress_ps:g} ps 동안 압축 · 같은 열욕)"), flush=True)
    if a.dry_run:
        print("dry_run — 여기서 멈춘다"); return
    calc = make_calc(a.device, a.turbo)
    plan["uma_inference_mode"] = getattr(calc, "_mq_mode", "default")
    plan["software"] = software_versions(plan["uma_inference_mode"])   # 회신 DF Q-DF-6 — 판 · 모델 · 추론 설정을 기록
    (out / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    print(f"UMA inference mode: {plan['uma_inference_mode']}", flush=True)
    info = run_melt_quench(at, calc, out, seed=a.seed, T_melt=a.T_melt, T_final=a.T_final, melt_ps=a.melt_ps,
                           quench_rate=a.quench_rate, hold_ps=a.hold_ps, dt_fs=a.dt_fs, save_ps=a.save_ps,
                           fix_density=a.fix_density, compress_ps=a.compress_ps, run_id=a.run_id)
    ind = indicators(at.get_chemical_symbols(), at.get_positions(), np.asarray(at.get_cell()))
    gr = partial_gr(at.get_chemical_symbols(), at.get_positions(), np.asarray(at.get_cell()))
    write_gr_csv(gr, out / "gr_partials.csv")
    res = {"plan": plan, "run": info, "indicators": ind, "E_final_eV": float(at.get_potential_energy()),
           "files": ["initial.xyz", "traj.xyz", "thermo.csv", "final.xyz", "final.vasp", "gr_partials.csv"],
           "⛔": "지표만 찍었다 — 문턱 대조는 카드 §2 판정_지표. 이 시드 하나로 판정하지 않는다 (G3)."}
    (out / "result.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(json.dumps({"indicators": ind, "wall_min": round(info["wall_min"], 1)}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
