#!/usr/bin/env python3
"""argyrodite_cage_neb.py — argyrodite **벌크 Li 공공 hop** 의 CI-NEB (UMA).

왜 새 파일인가 (2026-08-19, 코드 규율 사다리 ①~④ 확인)
  `tools/neb_diffusion/` 의 기존 NEB 는 전부 **Li₃N / LiC6 표면 adatom** 용이다
  (`li3n_seeded_neb.py`, `adatom_diffusion.py`, `li3n_uma_investigate.py`).
  거기엔 슬래브 고정·adatom 3-DOF 가 박혀 있어 벌크 공공 hop 에 못 쓴다.
  `tools/sei/run_sei_neb.sh` 는 QE `neb.x` (DFT) 라 다른 엔진이다.
  `tools/ionic/cage_jump_descriptors.py` 는 **케이지 기하 기술자**(NEB 없음) —
  케이지 판정 규약(PS4 결합 2.30 Å, 자유 음이온 = 케이지 중심)은 거기서 가져왔다.

무엇을 하나
  ① 케이지 중심(자유 S + Cl)을 잡고 Li 를 케이지에 배정
  ② **intra-cage**(같은 케이지) / **inter-cage**(다른 케이지) hop 짝을 고른다
  ③ 공공 하나(Li 제거) + 이웃 Li 를 그 자리로 → 두 끝점을 **위치만** 이완
  ④ IDPP 보간 → NEB → CI-NEB, 장벽 = max(E) − E(시작)

⭐ **셀은 절대 이완하지 않는다.** 2026-08-19 실측: UMA 는 canonical Li₆PS₅Cl 셀을
   +32.7 %(27.478 Å³/atom) 로 부풀린다. argyrodite 장벽은 부피에 극도로 민감해서
   (Wu 2026 이 26 % 팽창 격자에서 NEB 를 돌린 것을 우리가 지적했다) 셀을 풀면
   장벽이 의미를 잃는다. **DFT V0 셀에서 출발하고 고정한다.**

⛔⛔ **이미지 거리 지표 정정 (2026-08-20).** 이 도구는 2026-08-19 작성 시
   **면 높이(수직폭) `V/|a_j×a_k|`** 를 게이트로 썼는데, 그건 2026-08-16 에
   **Codex 리뷰로 이미 철회된 지표**다 (`kb/methodology/defect_cell_size_metric_2026_08_16.md`).
   점결함·확산 이온의 자기 이미지는 격자 **평면**이 아니라 격자 **병진** 위에 있다:

     정본 지표 λ₁ = min |n₁a + n₂b + n₃c|   (최단 비영 격자 병진)

   실측 차이가 판정을 뒤집는다 — Li₃Nd 2×2×2 면높이 **8.469 → λ₁ 10.372** (10 Å 통과).
   면 높이는 **보수적 하한**으로만 쓰고 "실제 이미지 거리" 라고 부르지 않는다.
   산식은 `tools/sei/build_neb_inputs.py:shortest_translation` **하나만** 쓴다 —
   **fallback 재구현 금지**(import 실패 = hard fail, 2026-08-20 Codex 2차).
   둘 다 찍되 **게이트는 λ₁ 로** 건다.

이 도구가 **못 하는 것**
  · DFT 가 아니다. UMA-s-1p1(omat) 이다. 절대 장벽을 DFT/실험과 등가로 인용 금지.
  · **단일 배열·단일 경로**다. 무질서계의 유효 장벽은 배열 앙상블의 최소경로가
    지배한다 — Wu 2026 의 NEB 0.59 eV vs 자기 EIS 0.32 eV 불일치가 그 사례다.
    앙상블은 `--seeds` 로 여러 짝을 돌려 **분포**로 보고할 것.
  · 전하 보상을 하지 않는다(UMA 는 전하를 모른다). Li 하나를 그냥 뺀다.
  · 케이지 배정은 **최근접 자유음이온**이다. 경계 Li 는 애매할 수 있다 —
    `cage_margin` 으로 애매한 짝을 걸러낸다.
  · 협동 이동(다중 Li 동시)을 못 본다. 단일 Li 경로만 본다.
  · ⚠ **b2o3 형(P 를 골격에서 빼낸 계)에서는 케이지 개념이 묽어진다.** P 10→8 로 PS₄ 둘이
    사라지며 그 황이 자유 음이온이 되어 케이지 중심이 28개(자유 S 12 + Cl 16)가 된다.
    Li 58개를 28 케이지에 나누면 케이지당 ~2 로, argyrodite 의 3–6 과 다르다.
    골격 자체는 온전하다(P 배위수 전부 4) — **막지는 않되, 케이지당 Li 수를 같이 찍는다.**
    이 계의 intra/inter 구분은 다른 셋보다 약하게 해석할 것.

  python3 tools/neb_diffusion/argyrodite_cage_neb.py --selftest
  # 셀 수렴 시험 (comp1, cubic)
  python3 tools/neb_diffusion/argyrodite_cage_neb.py \
      --struct db/structures/comp1_V0_k444.cif --kind inter \
      --supercell 1 1 1 --tag conv_111        # comp1 은 λ₁ 10.06 이라 --force 불필요
"""
import argparse, json, os, sys, time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUTDIR = ROOT / "db" / "properties"

#: cage_jump_descriptors.py 와 같은 값 — P–S 결합 판정 (PS4 는 2.04–2.11 Å)
PS_BOND = 2.30
#: 이미지 거리 하한 — **λ₁ 기준** (defect_cell_size_metric_2026_08_16 정본).
#: ⚠ 이 게이트를 통과해도 **셀 수렴은 별개**다 (sei_neb.json 의 cell_convergence_status).
MIN_WIDTH_A = 10.0
#: NEB 기본값
N_IMAGES = 7          # 내부 이미지 (끝점 제외)
FMAX_ENDPOINT = 0.03
FMAX_NEB = 0.05
FMAX_CI = 0.03
STEPS_NEB = 400
SPRING_K = 0.1
#: ⚠ ASE 3.29 는 기본 탄젠트가 'aseneb'(비권장, 밴드가 자주 망가짐)라고 스스로 경고한다.
#: 명시적으로 improvedtangent 를 쓴다 (Henkelman 2000). 재현성을 위해 기록도 남긴다.
NEB_METHOD = "improvedtangent"
#: 이웃 이미지 간 에너지 도약 한계. 물리적 밴드는 매끄럽다 — 이보다 뛰면 이미지가 터진 것.
MAX_IMAGE_JUMP_EV = 0.8


# ── 기하 ─────────────────────────────────────────────────────────────────────
def perp_widths(cell):
    """면간 **수직거리** d_i = V / |a_j × a_k| — **보수적 하한으로만 쓴다.**

    ⛔ 이것은 격자 **평면** 사이 거리라 슬랩 분리에 맞는 양이고 **점-이미지 거리가 아니다**
      (2026-08-16 Codex 리뷰). 게이트는 `lambda1()` 로 건다. 이 함수는 참고 표시용이다.
    """
    c = np.asarray(cell, float)
    V = abs(np.linalg.det(c))
    return np.array([V / np.linalg.norm(np.cross(c[(i + 1) % 3], c[(i + 2) % 3]))
                     for i in range(3)])


def lambda1(cell, R=3):
    """최단 비영 격자 병진 λ₁ [Å] — **점결함 이미지 거리의 정본 지표.**

    ⛔⛔ 2026-08-20 (Codex 2차) — **fallback 을 없앴다.** 앞 판은 canonical import 가
      실패하면 `except BaseException` 으로 같은 수식을 여기서 다시 구현했는데,
      그게 **규약 역행을 허용하는 가장 전형적인 구조**다(두 구현이 갈라져도 아무도 모른다).
      이제 import 실패는 **hard fail** 이다 — 정본을 못 읽으면 계산을 하지 않는다.
    """
    import importlib.util
    src = ROOT / "tools" / "sei" / "build_neb_inputs.py"
    if not src.exists():
        raise RuntimeError(
            f"⛔ λ₁ 정본 구현을 못 찾았다: {src}\n"
            f"   fallback 으로 여기서 다시 구현하지 않는다 — 두 구현이 갈라지면 "
            f"규약 역행이 조용히 통과한다 (2026-08-20 Codex 리뷰).")
    spec = importlib.util.spec_from_file_location("_bni_lambda1", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)                     # 실패하면 그대로 올린다
    return float(mod.shortest_translation(cell, R=R))


def mic_vec(atoms, i, j):
    """i → j 최소이미지 벡터 (데카르트)."""
    c = np.array(atoms.cell)
    d = atoms.positions[j] - atoms.positions[i]
    f = np.linalg.solve(c.T, d)
    f -= np.round(f)
    return f @ c


def hop_distance(ini, fin, j2):
    """두 끝점에서 **이동 Li(j2) 가 실제로 옮겨간 거리** (최소이미지).

    ⚠ 2026-08-20 정정. 처음엔 "심화 이완이 홉을 바꾼다" 고 적었는데 **대조 실행으로 반증됐다** —
    `--shallow_endpoints`(한 번 이완)에서도 똑같이 3.504 → 4.369 Å 가 됐다(심화는 4.356, 차 0.013).
    즉 이건 탈출의 부작용이 아니라 **이완된 홉 거리가 이상격자 거리와 원래 다르다**는 것이고,
    크게 벌어지면 **목표 자리가 그 Li 의 국소 최소가 아니었다**는 신호다 —
    경로 위에 중간 최소가 있어 **elementary 경로가 아닐** 가능성이 크고,
    밴드 발산·"중간이 끝점보다 낮음" 이 같이 뜬다.
    ⚠ 이것을 협동 이동(다중 Li 동시)으로 읽지 않는다 — 초판이 그렇게 썼다가 철회했다
    (단일 Li 로 전부 설명된다. 협동이 없다는 뜻은 아니고 이 데이터로는 못 가른다).
    """
    c = np.array(ini.cell)
    d = fin.positions[j2] - ini.positions[j2]
    f = np.linalg.solve(c.T, d)
    f -= np.round(f)
    return float(np.linalg.norm(f @ c))


def cage_assign(atoms):
    """(케이지중심 인덱스, Li 인덱스, Li→케이지 배정, Li–중심 거리).

    케이지 중심 = **자유 음이온** = P 와 결합하지 않은 S + 모든 Cl (+Br/I/O 는
    할라이드 자리에 있을 수 있으므로 같이 센다). cage_jump_descriptors 규약.
    """
    sym = np.array(atoms.get_chemical_symbols())
    P = np.where(sym == "P")[0]
    S = np.where(sym == "S")[0]
    HAL = np.where(np.isin(sym, ["Cl", "Br", "I"]))[0]
    Li = np.where(sym == "Li")[0]
    if len(Li) == 0:
        raise ValueError("Li 가 없다 — argyrodite 가 아니다")
    bonded = set()
    if len(P) and len(S):
        D = atoms.get_all_distances(mic=True)
        for p in P:
            bonded.update(int(s) for s in S[D[p, S] < PS_BOND])
    freeS = np.array([s for s in S if s not in bonded], int)
    centers = np.concatenate([freeS, HAL]).astype(int)
    if len(centers) == 0:
        raise ValueError("케이지 중심(자유 음이온)이 없다 — PS_BOND 를 확인할 것")
    # 2026-08-19 자기리뷰. 처음엔 "자유 S 가 P 보다 많으면 골격이 깨진 것" 으로 막았는데
    # **그게 틀렸다** — comp1(정상, 자유 S 4 = P 4)까지 막혔다. b2o3 의 자유 S 12개도
    # 버그가 아니라 치환의 실제 결과다(P 10→8 로 PS₄ 두 개가 사라지며 그 황이 풀렸다).
    # 진짜 판정은 **P 배위수**다: 모든 P 가 음이온 4개와 결합해야 골격이 온전하다.
    bondedP = [(D[q][np.isin(sym, ["S", "O", "Se"])] < PS_BOND).sum() for q in P] \
        if len(P) else []
    bad = [int(x) for x in bondedP if x != 4]
    if bad:
        raise ValueError(f"P 배위수가 4 가 아닌 것이 {len(bad)}개 있다 {bad[:5]} — "
                         f"PS₄ 골격이 온전하지 않아 '자유 음이온 = 케이지 중심' 규약이 "
                         f"성립하지 않는다. PS_BOND({PS_BOND} Å) 를 의심하거나 구조를 볼 것")
    D = atoms.get_all_distances(mic=True)
    sub = D[np.ix_(Li, centers)]
    assign = np.argmin(sub, axis=1)
    return centers, Li, assign, sub[np.arange(len(Li)), assign]


def find_hops(atoms, kind, rmax=5.0, cage_margin=0.3):
    """(i, j, 거리) 후보 목록. kind: 'intra' 같은 케이지 · 'inter' 다른 케이지.

    `cage_margin`: 두 케이지 중심까지 거리 차가 이보다 작은 Li 는 **배정이 애매**하므로
    뺀다 (경계 Li 를 inter/intra 로 잘못 부르지 않기 위해).
    """
    centers, Li, assign, _ = cage_assign(atoms)
    D = atoms.get_all_distances(mic=True)
    sub = D[np.ix_(Li, centers)]
    srt = np.sort(sub, axis=1)
    ambiguous = (srt[:, 1] - srt[:, 0]) < cage_margin if sub.shape[1] > 1 else \
        np.zeros(len(Li), bool)
    out = []
    for a in range(len(Li)):
        if ambiguous[a]:
            continue
        for b in range(a + 1, len(Li)):
            if ambiguous[b]:
                continue
            d = D[Li[a], Li[b]]
            if d > rmax:
                continue
            same = assign[a] == assign[b]
            if (kind == "intra") != same:
                continue
            out.append((int(Li[a]), int(Li[b]), float(d)))
    out.sort(key=lambda t: (round(t[2], 4), t[0], t[1]))
    return out


def build_endpoints(atoms, i_vac, j_mig):
    """(시작, 끝). 시작 = Li_i 제거. 끝 = 거기서 Li_j 를 i 자리로 옮긴 것.

    **원자 목록·인덱스가 두 끝점에서 동일**해야 NEB 보간이 성립한다. 그래서
    한쪽에서만 원자를 빼고, 다른 쪽은 그 결과를 복사해 위치만 바꾼다.
    이동은 **최소이미지 벡터**로 하므로 셀 경계를 가로지르는 hop 도 짧은 길로 간다.
    """
    if atoms.get_chemical_symbols()[i_vac] != "Li" or \
       atoms.get_chemical_symbols()[j_mig] != "Li":
        raise ValueError("i_vac · j_mig 는 둘 다 Li 여야 한다")
    if i_vac == j_mig:
        raise ValueError("같은 원자를 공공이자 이동체로 쓸 수 없다")
    v = mic_vec(atoms, j_mig, i_vac)          # j → i (짧은 길)
    ini = atoms.copy()
    del ini[i_vac]
    j2 = j_mig - 1 if j_mig > i_vac else j_mig   # 삭제로 밀린 인덱스
    fin = ini.copy()
    fin.positions[j2] = ini.positions[j2] + v
    return ini, fin, j2, float(np.linalg.norm(v))


# ── 실행 ─────────────────────────────────────────────────────────────────────
def load_calc(device="cuda"):
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)
    return FAIRChemCalculator(pred, task_name="omat")


def relax_positions(atoms, calc, fmax=FMAX_ENDPOINT, steps=800):
    """⭐ **위치만** 이완한다. 셀은 절대 건드리지 않는다 (모듈 docstring 참조)."""
    from ase.optimize import FIRE
    atoms = atoms.copy()
    atoms.calc = calc
    opt = FIRE(atoms, logfile=None)
    opt.run(fmax=fmax, steps=steps)
    return atoms, bool(opt.converged()), int(opt.get_number_of_steps())


# ── 끝점 심화 이완 ───────────────────────────────────────────────────────────
# 왜 (2026-08-19 실측). comp1 2×1×1/2×2×1 에서 band_health 가 같은 병을 잡았다:
#   "중간 이미지가 두 끝점 중 낮은 쪽보다 −0.244 eV 낮다 — 끝점이 국소 최소가 아니다."
# 만석 Li 격자에 공공을 하나 뚫으면 부격자가 통째로 재배열하려 드는데, FIRE 는
# **얕은 분지 바닥에서 fmax 를 만족해 멈춘다.** 그 위에서 NEB 를 돌리면
#   ① 장벽이 통째로 틀리고 (기준선이 잘못됨)
#   ② 중간 이미지가 끝점보다 낮아 프로파일이 물리적으로 말이 안 된다.
# 처방: 이완 → 흔들기 → 재이완 을 되풀이해 **더 낮은 분지가 없을 때까지** 내려간다.
ESCAPE_AMP_A = 0.12      # 흔들기 진폭 (Å). 결합을 깨지 않으면서 얕은 안장은 넘는 크기
ESCAPE_GAIN_EV = 0.005   # 이만큼 못 내려가면 더 안 판다


def relax_endpoint_deep(atoms, calc, fmax=FMAX_ENDPOINT, steps=800,
                        tries=4, amp=ESCAPE_AMP_A, seed=0,
                        track_idx=None, max_track_drift=0.6):
    """이완 → rattle → 재이완 을 되풀이해 **진짜 분지 바닥**을 찾는다.

    돌려주는 값: (atoms, info)
      info = {'E','E_first','gain_eV','n_escapes','n_rejected','converged','steps','track_drift_A'}

    ⭐ `track_idx` 를 주면 그 원자가 `max_track_drift` 넘게 움직인 후보는 **버린다.**
      왜 (2026-08-19 실측): 추적 없이 돌렸더니 시작 끝점이 55 meV 낮은 분지로 내려가면서
      **홉 거리가 3.504 → 4.356 Å 로 바뀌었다.** 더 낮은 최소를 찾은 건 맞지만
      **그건 다른 홉의 끝점**이라 장벽을 그 이름으로 db 에 넣으면 안 된다.
      ⇒ "더 낮은 분지" 와 "같은 홉" 을 **동시에** 요구한다.

    이 함수가 **못 하는 것**
      · 전역 최소를 보장하지 않는다. rattle 이 넘을 수 있는 안장만 넘는다.
      · track_idx 를 안 주면 홉이 바뀌어도 못 막는다(호출자가 hop_distance 로 확인해야 한다).
      · amp 가 너무 크면 결합을 깬다. 기본 0.12 Å 는 열진동 크기 수준이다.
    """
    rng = np.random.default_rng(seed)
    best, conv, nsteps = relax_positions(atoms, calc, fmax=fmax, steps=steps)
    e_first = e_best = float(best.get_potential_energy())
    ref = best.get_positions()[track_idx].copy() if track_idx is not None else None
    n_esc = n_rej = 0
    drift = 0.0
    for _ in range(tries):
        cand = best.copy()
        cand.set_positions(cand.get_positions()
                           + rng.normal(0.0, amp, cand.get_positions().shape))
        cand, c2, s2 = relax_positions(cand, calc, fmax=fmax, steps=steps)
        e = float(cand.get_potential_energy())
        nsteps += s2
        if e >= e_best - ESCAPE_GAIN_EV:
            break                      # 한 번 실패하면 더 파도 대개 안 나온다
        if ref is not None:
            d = float(np.linalg.norm(cand.get_positions()[track_idx] - ref))
            if d > max_track_drift:
                # 더 낮지만 **추적 원자가 자리를 옮겼다** — 다른 홉이므로 채택하지 않는다
                n_rej += 1
                continue
            drift = d
        best, e_best, conv, n_esc = cand, e, c2, n_esc + 1
    return best, {"E": e_best, "E_first": e_first, "gain_eV": e_first - e_best,
                  "n_escapes": n_esc, "n_rejected": n_rej, "track_drift_A": drift,
                  "converged": bool(conv), "steps": int(nsteps)}


def band_health(E):
    """프로파일이 물리적인가. (문제목록, 지표) — **조용히 넘어가지 않는다.**

    2026-08-19 실측에서 잡은 두 병리:
      · 이미지 하나만 +2.3 eV 로 솟고 나머지는 0 근처 → **터진 이미지**(밴드 미수렴 위에서
        climb 를 켜면 그 이미지가 능선으로 밀린다)
      · 중간 이미지가 두 끝점보다 **낮다** → 끝점이 국소 최소가 아니다. 만석 Li 격자에
        공공을 하나 뚫으면 부격자가 통째로 재배열하려 든다.
    """
    rel = np.asarray(E) - E[0]
    inner = rel[1:-1]
    probs = []
    spike = float(inner.max())
    others = float(np.sort(inner)[-2]) if len(inner) > 1 else 0.0
    # ⭐ 판정은 **이웃 이미지 간 도약**으로 한다. 처음엔 "최고/차고 비율 > 3" 으로 짰는데
    #   실측 폭주 판(최고 2.378 / 차고 0.818, 비율 2.9×)이 아슬하게 빠져나갔다.
    #   물리적 밴드는 매끄럽다 — 이미지 간격 ~0.5 Å 에서 0.5 eV 장벽이면 이미지당 ~0.17 eV 다.
    #   폭주는 불연속으로 나타난다(실측 +1.70, +2.31 eV). 0.8 eV 를 문턱으로 둔다.
    jump = float(np.abs(np.diff(rel)).max()) if len(rel) > 1 else 0.0
    if jump > MAX_IMAGE_JUMP_EV:
        probs.append(f"이웃 이미지 사이가 {jump:.2f} eV 뛴다(문턱 {MAX_IMAGE_JUMP_EV}) — "
                     f"밴드가 불연속이다. 최고 {spike:+.2f} / 차고 {others:+.2f}")
    # ⛔ 2026-08-19 실측에서 잡은 **내 버그**. 처음엔 `min(inner) − max(0, rel[-1])` 로 쟀는데
    #   그러면 **끝점 비대칭**(한쪽이 +256 meV 높은 것)을 "중간이 낮다" 로 오인한다.
    #   실제 comp1 inter 판에서 중간 최소가 시작점보다 32 meV 낮을 뿐인데 −288 meV 로
    #   계산돼 멀쩡한 결과에 가짜 경보가 붙었다. **더 낮은 쪽 끝점**과 비교해야 맞다.
    below = float(inner.min()) - min(0.0, float(rel[-1]))
    if below < -0.05:
        probs.append(f"중간 이미지가 **두 끝점 중 낮은 쪽**보다 {below:.3f} eV 낮다 — "
                     f"끝점이 국소 최소가 아니다")
    # ⚠ 끝점 비등가는 **결함이 아니다.** 무질서 argyrodite 에서 두 Li 자리가 다른 것은
    #   정상이고, 그래서 Ea(정) ≠ Ea(역) 이 된다. 문제로 세지 않고 **주석으로만** 남긴다
    #   (2026-08-19 자기리뷰 — 처음엔 실패로 셌다).
    notes = []
    if abs(float(rel[-1])) > 0.15:
        notes.append(f"두 끝점 차 {1000*float(rel[-1]):+.0f} meV — 등가 자리가 아니다"
                     f"(비대칭 hop, 정상일 수 있음). Ea 는 정·역 둘 다 보고할 것")
    return probs, {"spike_eV": round(spike, 4), "max_image_jump_eV": round(jump, 4),
                   "notes": notes,
                   "second_highest_eV": round(others, 4),
                   "min_interior_rel_eV": round(float(inner.min()), 4)}


def run_neb(ini, fin, calc, n_images=N_IMAGES, steps=STEPS_NEB, log=None):
    """1단계(밴드) → **수렴했을 때만** 2단계(climbing image).

    ⛔ 2026-08-19: 앞 판은 1단계 수렴을 **안 보고** climb 를 켰다. 400스텝 상한에 걸린
       밴드 위에서 CI 를 켜니 그 이미지가 +2.3 eV 로 밀려 올라가 장벽이 통째로 가짜가 됐다.
       (comp1 intra/inter 둘 다 같은 증상.) 이제 미수렴이면 **CI 를 안 켜고 그렇게 보고한다.**
    """
    from ase.mep import NEB
    from ase.optimize import FIRE
    images = [ini] + [ini.copy() for _ in range(n_images)] + [fin]
    for im in images:
        im.calc = calc
    neb = NEB(images, k=SPRING_K, climb=False, method=NEB_METHOD,
              allow_shared_calculator=True)
    neb.interpolate("idpp", apply_constraint=False)
    # ⚠ 한 판이 25분~3시간 간다. logfile=None 이면 밖에서 **수렴 중인지 제자리인지** 알 길이
    #   없다(2026-08-19 실측 — 한 시간 넘게 깜깜했다). 스텝별 fmax 를 파일로 남긴다.
    opt = FIRE(neb, logfile=(str(log) if log else None))
    opt.run(fmax=FMAX_NEB, steps=steps)
    conv1, n1 = bool(opt.converged()), int(opt.get_number_of_steps())
    E_band = np.array([im.get_potential_energy() for im in images])
    conv2, n2 = False, 0
    if conv1:
        neb.climb = True
        opt2 = FIRE(neb, logfile=(str(log) if log else None))
        opt2.run(fmax=FMAX_CI, steps=steps)
        conv2, n2 = bool(opt2.converged()), int(opt2.get_number_of_steps())
    E = np.array([im.get_potential_energy() for im in images]) if conv1 else E_band
    info = {"band_converged": conv1, "ci_ran": conv1, "ci_converged": conv2,
            "steps_band": n1, "steps_ci": n2,
            "band_only_profile_eV": [round(float(x - E_band[0]), 4) for x in E_band]}
    info["band_tail"] = fmax_trend(log)
    return images, E, info


# ⚠ 2026-08-20 (1저자 지적). "400스텝 미수렴" 만으로는 **느리게 수렴 중인지 발산 중인지**
#   구분이 안 된다. comp1 2×1×1 은 마지막 4스텝에서 에너지와 fmax 가 **둘 다 상승**하고 있었고
#   (E −429.268 → −429.215, fmax 0.192 → 0.218), 그 경우 `--neb_steps` 를 늘리는 것은
#   처방이 아니다. 판정은 아무것도 바꾸지 않고 **꼬리 추세만 보고**한다.
TAIL_N = 12                    # 추세를 볼 마지막 스텝 수
TAIL_RISE_FRAC = 0.6           # 이 비율 넘게 오르면 '상승'


def fmax_trend(log, n=TAIL_N):
    """FIRE 로그 꼬리의 fmax 추세. 로그가 없거나 짧으면 None.

    돌려주는 값: {'n','first','last','verdict','rising_frac'}
      verdict: 'converging'(내려간다) · 'rising'(올라간다 = 스텝을 늘려도 소용없다) ·
               'flat'(정체 = 상한에 걸린 게 아니라 갇힌 것)

    이 함수가 **못 하는 것**: 발산의 *원인*은 말하지 못한다(끝점 비대칭인지 경로 위상인지).
      그건 프로파일과 band_health 가 볼 몫이다.
    """
    if not log:
        return None
    try:
        lines = [ln.split() for ln in Path(log).read_text(errors="ignore").splitlines()
                 if ln.startswith("FIRE")]
    except OSError:
        return None
    vals = []
    for parts in lines[-n:]:
        try:
            vals.append(float(parts[-1]))
        except (ValueError, IndexError):
            continue
    if len(vals) < 4:
        return None
    ups = sum(1 for a, b in zip(vals, vals[1:]) if b > a)
    frac = ups / (len(vals) - 1)
    if frac >= TAIL_RISE_FRAC:
        v = "rising"
    elif vals[-1] < vals[0] * 0.98:
        v = "converging"
    else:
        v = "flat"
    return {"n": len(vals), "first": round(vals[0], 4), "last": round(vals[-1], 4),
            "rising_frac": round(frac, 2), "verdict": v}


def fmax_trend_text(t):
    if not t:
        return ""
    return {
        "rising": (f"⛔ 마지막 {t['n']}스텝에서 fmax 가 **오르고 있다** "
                   f"({t['first']} → {t['last']}, 상승 {t['rising_frac']:.0%}) — "
                   f"**--neb_steps 를 늘려도 소용없다.** 끝점 비대칭이나 경로 위상을 볼 것"),
        "flat": (f"⚠ 마지막 {t['n']}스텝 fmax 가 **정체**다 ({t['first']} → {t['last']}) — "
                 f"상한에 걸린 게 아니라 갇힌 것이다"),
        "converging": (f"⭕ 마지막 {t['n']}스텝 fmax 가 내려가는 중 "
                       f"({t['first']} → {t['last']}) — 스텝을 늘리면 될 수 있다"),
    }.get(t["verdict"], "")


def one_run(args):
    from ase.io import read, write
    base = read(args.struct if os.path.isabs(args.struct) else str(ROOT / args.struct))
    sc = tuple(args.supercell)
    atoms = base.repeat(sc) if sc != (1, 1, 1) else base.copy()
    W = perp_widths(atoms.cell)
    L1 = lambda1(atoms.cell)                      # ★ 정본 지표 (점결함 이미지 거리)
    print(f"── {Path(args.struct).name}  ×{sc}  n={len(atoms)}  "
          f"**λ₁ {L1:.2f} Å** (면높이 최소 {W.min():.2f} — 보수적 하한)")
    if L1 < args.min_width and not args.force:
        raise SystemExit(
            f"⛔ λ₁ {L1:.2f} Å < {args.min_width} Å — 이동 Li 가 자기 이미지와 겹친다. "
            f"슈퍼셀을 키우거나 --force (수렴시험 목적이면 정당하다).\n"
            f"   (면높이 최소 {W.min():.2f} Å 는 보수적 하한일 뿐 게이트 기준이 아니다 — "
            f"kb/methodology/defect_cell_size_metric_2026_08_16.md)")

    cands = find_hops(atoms, args.kind, rmax=args.rmax, cage_margin=args.cage_margin)
    if not cands:
        raise SystemExit(f"⛔ '{args.kind}' hop 후보가 없다 (rmax={args.rmax})")
    if args.pair:
        i_vac, j_mig = (int(x) for x in args.pair.split(","))
        d = float(atoms.get_distance(i_vac, j_mig, mic=True))
    else:
        i_vac, j_mig, d = cands[args.pick]
    print(f"   후보 {len(cands)}개 · 선택 ({i_vac}, {j_mig}) d={d:.3f} Å  [{args.kind}]")

    ini0, fin0, j2, hop = build_endpoints(atoms, i_vac, j_mig)
    assert ini0.get_chemical_symbols() == fin0.get_chemical_symbols()

    calc = load_calc(args.device)
    t0 = time.time()
    if args.shallow_endpoints:
        ini, c1, s1 = relax_positions(ini0, calc)
        fin, c2, s2 = relax_positions(fin0, calc)
        ep_i = {"gain_eV": 0.0, "n_escapes": 0, "converged": c1, "steps": s1}
        ep_f = {"gain_eV": 0.0, "n_escapes": 0, "converged": c2, "steps": s2}
    else:
        # ⭐ 2026-08-19 — 기본을 **심화 이완**으로 바꿨다. comp1 2×1×1/2×2×1 에서
        #   "중간 이미지가 끝점보다 낮다"가 반복해 잡혔고, 그건 끝점이 얕은 분지에
        #   걸려 멈춘 것이었다. 옛 동작은 --shallow_endpoints 로 남겨 둔다.
        # ⭐ 이동 Li(j2) 를 추적한다 — 탈출이 그 원자를 옮겨 버리면 **다른 홉**이 된다.
        #   (2026-08-19 실측: 추적 없이 돌렸더니 홉이 3.504 → 4.356 Å 로 바뀌었다.)
        ini, ep_i = relax_endpoint_deep(ini0, calc, seed=args.seed,
                                        track_idx=j2, max_track_drift=args.max_ep_drift)
        fin, ep_f = relax_endpoint_deep(fin0, calc, seed=args.seed + 1,
                                        track_idx=j2, max_track_drift=args.max_ep_drift)
        s1, s2 = ep_i["steps"], ep_f["steps"]
    c1, c2 = ep_i["converged"], ep_f["converged"]
    E_i, E_f = ini.get_potential_energy(), fin.get_potential_energy()
    print(f"   끝점 이완: {s1}/{s2} steps  ΔE(끝−시작) = {1000*(E_f-E_i):+.1f} meV")
    if ep_i["n_escapes"] or ep_f["n_escapes"]:
        print(f"   ⭐ 얕은 분지 탈출: 시작 {ep_i['n_escapes']}회({1000*ep_i['gain_eV']:+.0f} meV) · "
              f"끝 {ep_f['n_escapes']}회({1000*ep_f['gain_eV']:+.0f} meV)")
        print(f"      → 옛 방식이었으면 이만큼 높은 끝점 위에서 NEB 를 돌렸다는 뜻이다.")
    # 심화 이완이 **홉 자체를 바꿔버리지 않았는지** 확인한다 (다른 자리로 도망가면 다른 홉이다).
    # ⚠⚠ 2026-08-20 대조 실행으로 **문구를 정정했다.** 처음엔 "심화 이완이 홉을 바꿨다" 로
    #   적었는데, --shallow_endpoints 에서도 **똑같이** 바뀐다(3.504 → 4.369 vs 4.356, 차 0.013 Å).
    #   즉 탈출이 아니라 **첫 이완**에서 이미 그렇게 된다 — 이완된 홉 거리는 이상격자 거리와
    #   원래 다르다. 크게 벌어지면 그건 "가드 실패" 가 아니라 **이웃 Li 가 같이 움직인다**는
    #   신호이고, 그 경우 단일 Li NEB 자체가 성립하지 않는다(밴드 발산으로 드러난다).
    d_after = hop_distance(ini, fin, j2)
    if abs(d_after - hop) > 0.5:
        print(f"   ⚠ 이완 뒤 홉 거리 {hop:.3f} → {d_after:.3f} Å (이상격자 대비 "
              f"{d_after - hop:+.3f}) — 이웃 Li 가 같이 움직인다는 뜻일 수 있다.")
        print(f"      **협동 이동이면 단일 Li NEB 가 성립하지 않는다** — 밴드 불연속·"
              f"'중간이 끝점보다 낮음' 이 같이 뜨는지 볼 것 (2026-08-20 comp1 inter 실측 사례)")
    logf = OUTDIR / f"neb_{args.tag or 'run'}.log"
    print(f"   NEB 진행 로그 → {logf}   (tail -f 로 볼 것)")
    images, E, nebinfo = run_neb(ini, fin, calc, args.n_images, args.neb_steps, log=logf)
    split_rec = None
    if args.split:
        images, E, nebinfo, split_rec = run_split_neb(
            images, E, nebinfo, calc, args, logf)
    probs, health = band_health(E)
    Ea_f = float(E.max() - E[0])
    Ea_r = float(E.max() - E[-1])
    dt = time.time() - t0

    if split_rec:
        rec_extra = {"split": split_rec}
    else:
        rec_extra = {}
    tag = args.tag or f"{Path(args.struct).stem}_{args.kind}_{sc[0]}{sc[1]}{sc[2]}"
    xyz = OUTDIR / f"neb_{tag}.xyz"
    write(str(xyz), images)
    rec = {
        "tag": tag, "struct": args.struct, "supercell": list(sc),
        "n_atoms": len(atoms), "n_atoms_neb": len(ini),
        "lambda1_A": round(float(L1), 3),
        "cell_size_gate_metric": "lambda1 >= min_width (defect_cell_size_metric_2026_08_16)",
        "perp_widths_A": [round(float(x), 3) for x in W],
        "perp_widths_note": "보수적 하한 — 점-이미지 거리가 아니다(게이트에 쓰지 않는다)",
        "min_perp_width_A": round(float(W.min()), 3),
        "kind": args.kind, "pair": [i_vac, j_mig],
        "pair_distance_A": round(d, 4), "hop_distance_A": round(hop, 4),
        "n_hop_candidates": len(cands),
        "Ea_forward_eV": round(Ea_f, 4), "Ea_reverse_eV": round(Ea_r, 4),
        "dE_endpoints_meV": round(1000 * (E_f - E_i), 2),
        "energies_eV": [round(float(x), 6) for x in E],
        "profile_eV_rel": [round(float(x - E[0]), 4) for x in E],
        "n_images_total": len(images),
        "endpoint_converged": [c1, c2], "seconds": round(dt, 1),
        **nebinfo, **health,
        "neb_converged": bool(nebinfo["ci_converged"]),
        "band_problems": probs,
        "trustworthy": bool(nebinfo["ci_converged"] and not probs),
        **rec_extra,
        "engine": "uma-s-1p1(omat)", "cell_relaxed": False,
        "neb_method": NEB_METHOD, "spring_k": SPRING_K,
        "fmax": {"endpoint": FMAX_ENDPOINT, "neb": FMAX_NEB, "ci": FMAX_CI},
        "images_file": str(xyz),
    }
    _ci = ("수렴" if nebinfo["ci_converged"]
           else ("미수렴" if nebinfo["ci_ran"] else "미실행"))
    _bd = "수렴" if nebinfo["band_converged"] else "미수렴"
    print(f"   **Ea(정) {Ea_f:.4f} eV**  Ea(역) {Ea_r:.4f} eV   "
          f"(밴드 {nebinfo['steps_band']}스텝 {_bd} · CI {nebinfo['steps_ci']}스텝 {_ci}, "
          f"{dt:.0f}s)")
    print(f"   프로파일: {[round(float(x - E[0]), 3) for x in E]}")
    if not nebinfo["band_converged"]:
        _t = fmax_trend_text(nebinfo.get("band_tail"))
        if _t:
            print(f"   {_t}")
    if probs:
        print("   ⛔ 이 값은 믿으면 안 된다:")
        for q in probs:
            print(f"      · {q}")
    for q in health.get("notes", []):
        print(f"   ⓘ {q}")
    return rec


# ── split NEB (inter-cage 처방) ───────────────────────────────────────────────
def find_intermediate(E):
    """밴드에서 **내부 국소최소** 위치를 찾는다. 없으면 None.

    반환 (idx, depth_eV) — depth 는 양옆 이웃 중 낮은 쪽 대비 얼마나 파였는지.
    끝점(0, -1)은 후보가 아니다. 여러 개면 **가장 깊은** 것.

    왜 이걸 쓰나 (2026-08-20)
      comp1 inter_211_deepep 밴드가
        [0.0, -0.267, -0.018, 0.432, -0.462, 0.247, -0.079, -0.179, -0.005]
      였다. 이미지 4 가 **시작점보다 0.462 eV 낮다** — 즉 이 경로는 하나의 홉이 아니라
      중간에 별개의 안정 자리를 거친다. 그런 밴드에서 max−E[0] 를 '장벽' 이라 부르면
      틀린다. 중간 자리를 실제 극소로 이완한 뒤 **두 구간으로 쪼개서** 각각 NEB 해야 한다.
    """
    import numpy as _np
    e = _np.asarray(E, float)
    if len(e) < 5:
        return None, 0.0
    best, best_d = None, 0.0
    for m in range(1, len(e) - 1):
        if e[m] < e[m - 1] and e[m] < e[m + 1]:
            d = float(min(e[m - 1], e[m + 1]) - e[m])
            if d > best_d:
                best, best_d = m, d
    return best, best_d


def run_split_neb(images, E, nebinfo, calc, args, logf):
    """중간자리 식별 → 두 구간 NEB. 합성 프로파일·유효 장벽을 함께 돌려준다.

    이 함수가 **못 하는 것**
      · 중간 자리가 물리적으로 의미 있는 자리인지 판정하지 않는다. 극소이기만 하면 쓴다.
      · 세 자리 이상을 거치는 경로를 한 번에 못 쪼갠다 (한 번만 쪼갠다).
        구간 밴드에 또 내부 극소가 뜨면 **그 사실을 기록만** 하고 더 쪼개지 않는다.
      · 유효 장벽은 합성 프로파일의 최댓값−시작이다. 이건 **경로 상한**이지
        앙상블 유효 장벽이 아니다.
    """
    import numpy as _np
    # ⛔ 2026-08-20: 첫 밴드가 **미수렴**이면 그 위에서 극소를 고르는 건 모래 위에 짓는 것이다.
    #   FIRE 가 400스텝을 다 쓰고 fmax 가 오히려 오르는 중이면 "이미지 4가 극소" 라는 판독
    #   자체가 신뢰할 수 없다. 막지는 않되(진단 가치가 있다) **결과에 낙인을 찍는다.**
    base_unconverged = not nebinfo.get("band_converged")
    if base_unconverged:
        print("   ⛔ 쪼개기 전 밴드가 **미수렴**이다 — 중간자리 판독의 근거가 약하다.")
        print("      아래 값은 진단용이며 **장벽으로 인용하면 안 된다.**")
    m, depth = find_intermediate(E)
    if m is None:
        print("   ⓘ --split: 내부 국소최소가 없다 — 쪼갤 게 없어 단일 NEB 로 둔다.")
        return images, E, nebinfo, {"split_done": False, "reason": "no_interior_minimum",
                                    "base_band_unconverged": base_unconverged}
    print(f"   ★ --split: 이미지 {m} 가 내부 극소 (양옆 대비 {1000*depth:+.0f} meV, "
          f"시작 대비 {1000*(E[m]-E[0]):+.0f} meV) → 중간자리로 잡는다")

    mid0 = images[m].copy()
    mid0.calc = calc
    mid, cm, sm = relax_positions(mid0, calc)
    E_m = mid.get_potential_energy()
    print(f"   중간자리 이완: {sm} steps {'수렴' if cm else '미수렴'}  "
          f"E(중간)−E(시작) = {1000*(E_m - E[0]):+.1f} meV")
    if not cm:
        print("   ⚠ 중간자리가 이완 수렴하지 않았다 — 아래 두 구간 값은 잠정이다.")

    # 이완이 중간자리를 끝점 중 하나로 굴려버렸으면 쪼갠 의미가 없다.
    d_i = float(_np.abs(mid.get_positions() - images[0].get_positions()).max())
    d_f = float(_np.abs(mid.get_positions() - images[-1].get_positions()).max())
    collapsed = (d_i < 0.3) or (d_f < 0.3)
    if collapsed:
        print(f"   ⛔ 이완 뒤 중간자리가 끝점으로 붕괴했다 (max 변위 {d_i:.2f}/{d_f:.2f} Å) "
              f"— 별개 자리가 아니다. 쪼개지 않는다.")
        return images, E, nebinfo, {"split_done": False, "reason": "intermediate_collapsed",
                                    "base_band_unconverged": base_unconverged,
                                    "max_disp_to_endpoints_A": [round(d_i, 3), round(d_f, 3)]}

    nseg = max(3, args.n_images // 2)
    segs = []
    for k, (a, b) in enumerate(((images[0], mid), (mid, images[-1])), start=1):
        lg = logf.with_name(logf.stem + f"_seg{k}.log")
        print(f"   구간 {k}/2 NEB (이미지 {nseg}) → {lg}")
        im_k, E_k, info_k = run_neb(a, b, calc, nseg, args.neb_steps, log=lg)
        Ea_k = float(E_k.max() - E_k[0])
        sub_m, _ = find_intermediate(E_k)
        print(f"      Ea(구간 {k}) = {Ea_k:.4f} eV   밴드 "
              f"{'수렴' if info_k['band_converged'] else '미수렴'} · CI "
              f"{'수렴' if info_k['ci_converged'] else ('미수렴' if info_k['ci_ran'] else '미실행')}")
        if sub_m is not None:
            print(f"      ⚠ 구간 {k} 안에 또 내부 극소(이미지 {sub_m})가 있다 — "
                  f"세 자리 이상을 거치는 경로다. 이 도구는 더 안 쪼갠다.")
        segs.append({"segment": k, "Ea_eV": round(Ea_k, 4),
                     "energies_eV": [round(float(x), 6) for x in E_k],
                     "profile_eV_rel": [round(float(x - E[0]), 4) for x in E_k],
                     "further_minimum_at": sub_m,
                     "band_converged": info_k["band_converged"],
                     "ci_converged": info_k["ci_converged"],
                     "steps_band": info_k["steps_band"], "steps_ci": info_k["steps_ci"]})
        segs[-1]["_images"] = im_k

    # 합성: 구간1 전체 + 구간2의 (중간자리 중복 제거) 나머지
    im_all = segs[0]["_images"] + segs[1]["_images"][1:]
    E_all = _np.concatenate([_np.array(segs[0]["energies_eV"]),
                             _np.array(segs[1]["energies_eV"])[1:]])
    for s in segs:
        s.pop("_images")
    Ea_eff = float(E_all.max() - E_all[0])
    print(f"   ★★ 합성 유효 장벽 = {Ea_eff:.4f} eV  "
          f"(구간 {segs[0]['Ea_eV']:.4f} / {segs[1]['Ea_eV']:.4f})")
    print(f"      ⓘ 이건 **이 경로의 상한**이다. 앙상블 유효 장벽이 아니다.")

    info_all = {
        "band_converged": bool(segs[0]["band_converged"] and segs[1]["band_converged"]),
        "ci_ran": True,
        "ci_converged": bool(segs[0]["ci_converged"] and segs[1]["ci_converged"]),
        "steps_band": segs[0]["steps_band"] + segs[1]["steps_band"],
        "steps_ci": segs[0]["steps_ci"] + segs[1]["steps_ci"],
        "band_only_profile_eV": [round(float(x - E_all[0]), 4) for x in E_all],
    }
    split_rec = {
        "split_done": True,
        "intermediate_image_index_in_first_band": int(m),
        "intermediate_depth_eV": round(depth, 4),
        "intermediate_relaxed": bool(cm), "intermediate_relax_steps": int(sm),
        "E_intermediate_minus_start_eV": round(float(E_m - E[0]), 4),
        "segments": segs,
        "Ea_effective_eV": round(Ea_eff, 4),
        "Ea_effective_meaning": "합성 프로파일 최댓값 − 시작. 이 경로의 상한이며 앙상블 유효 장벽이 아니다.",
        "single_neb_Ea_eV_SUPERSEDED": round(float(_np.max(E) - E[0]), 4),
        "base_band_unconverged": base_unconverged,
        "citable": bool(not base_unconverged
                        and segs[0]["ci_converged"] and segs[1]["ci_converged"]),
        "not_citable_because": (
            [] if (not base_unconverged and segs[0]["ci_converged"] and segs[1]["ci_converged"])
            else ([] if not base_unconverged else ["쪼개기 전 밴드가 미수렴 — 중간자리 판독의 근거가 약하다"])
                 + [f"구간 {s['segment']} CI 미수렴" for s in segs if not s["ci_converged"]]),
        "why": "inter-cage 단일 NEB 가 elementary 가 아니었다 (중간 극소). 2026-08-20 처방.",
    }
    return im_all, E_all, info_all, split_rec


# ── selftest ─────────────────────────────────────────────────────────────────
def selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok &= bool(c)

    # band_health 회귀 — **실측 프로파일**로 못 박는다 (2026-08-19)
    good = [0.0, -0.032, 0.423, 0.35, 0.528, 0.216, 0.256]   # comp1 inter, 수렴 후 실측
    pb, hh = band_health(good)
    chk(not pb, f"[양성] 정상 프로파일에 경보가 없다 (얻은 것 {pb})")
    chk(any("끝점 차" in n for n in hh["notes"]),
        "[양성] 끝점 비대칭은 **주석**으로만 나온다 (실패로 세지 않는다)")
    spiked = [0.0, -0.157, 0.400, 0.066, 0.678, 2.378, 0.818, 0.332, 0.257]  # CI 폭주 실측
    chk(any("불연속" in q for q in band_health(spiked)[0]),
        "[음성] 폭주 밴드(intra 실측, 도약 1.70 eV)를 잡는다")
    spiked2 = [0.0, -0.124, -0.239, -0.008, -0.001, 2.307, -0.250, -0.211, 0.255]
    chk(any("불연속" in q for q in band_health(spiked2)[0]),
        "[음성] 폭주 밴드(inter 실측, 도약 2.31 eV)도 잡는다")
    chk(band_health(good)[1]["max_image_jump_eV"] < MAX_IMAGE_JUMP_EV,
        f"[양성] 정상 밴드의 최대 도약은 문턱 아래 "
        f"({band_health(good)[1]['max_image_jump_eV']:.3f} < {MAX_IMAGE_JUMP_EV})")
    low = [0.0, -0.30, 0.1, 0.2, 0.1, -0.25, 0.05]
    chk(any("낮은 쪽" in q for q in band_health(low)[0]),
        "[음성] 중간이 두 끝점보다 정말 낮으면 잡는다")
    # 수직폭 — 양성/음성. 60° 셀에서 |a| 를 쓰면 틀린다는 것을 못 박는다.
    cube = np.eye(3) * 10.0
    chk(np.allclose(perp_widths(cube), 10.0), "[양성] 정육면체 수직폭 = 모서리 길이")
    a = 6.984
    rh = np.array([[a, 0, 0], [a * .5, a * np.sqrt(3) / 2, 0],
                   [a * .5, a / (2 * np.sqrt(3)), a * np.sqrt(2. / 3)]])
    W = perp_widths(rh)
    chk(W.min() < a * 0.95,
        f"[음성] 60° 셀은 수직폭이 |a| 보다 **작다** ({W.min():.2f} < {a})")

    try:
        from ase.io import read
        f = ROOT / "db" / "structures" / "comp1_V0_k444.cif"
        chk(f.exists(), "[전제] comp1_V0_k444.cif 가 있다")
        at = read(f)
        chk(abs(perp_widths(at.cell).min() - 10.06) < 0.05,
            f"[양성] comp1 수직폭 10.06 Å (얻은 것 {perp_widths(at.cell).min():.2f})")
        cen, Li, asg, _ = cage_assign(at)
        # ★ 양성 — 네 계 전부 P 배위수 4 라 통과해야 한다 (자기리뷰에서 가드를 한 번 잘못 걸었다)
        for nm, ff in (("modelC", "modelC_DFT_EOS_V0.cif"), ("lpsocl", "lpsocl_relaxV0.xyz"),
                       ("b2o3", "b2o3_relaxV0.cif")):
            try:
                cc2, ll2, _, _ = cage_assign(read(ROOT / "db" / "structures" / ff))
                chk(True, f"[양성] {nm} 통과 (케이지 {len(cc2)} · Li {len(ll2)}, "
                          f"케이지당 {len(ll2)/len(cc2):.1f})")
            except ValueError as e:
                chk(False, f"[음성] {nm} 을 막았다: {str(e)[:50]}")
        # ★ 음성 — PS₄ 를 실제로 깨면 막아야 한다.
        #   ⚠ P 를 빼는 것으로는 안 깨진다(남은 P 는 여전히 S 4개) — 자기리뷰에서
        #   이 음성시험을 한 번 잘못 짰다. **결합한 S 를 빼야** 그 P 가 3배위가 된다.
        broken = read(ROOT / "db" / "structures" / "comp1_V0_k444.cif")
        _sy = np.array(broken.get_chemical_symbols()); _D = broken.get_all_distances(mic=True)
        _p0 = int(np.where(_sy == "P")[0][0])
        _s0 = int([k for k in np.where(_sy == "S")[0] if _D[_p0, k] < PS_BOND][0])
        del broken[_s0]
        try:
            cage_assign(broken); chk(False, "[음성] PS₄ 가 깨진 구조를 통과시켰다")
        except ValueError as e:
            chk("배위수" in str(e), "[음성] PS₄ 를 깨면(결합 S 제거) 사유와 함께 막는다")
        # ★ 양성 — P 를 통째로 빼는 것은 **깨진 게 아니다**(남은 PS₄ 는 온전).
        okp = read(ROOT / "db" / "structures" / "comp1_V0_k444.cif")
        del okp[int(np.where(np.array(okp.get_chemical_symbols()) == "P")[0][0])]
        try:
            cage_assign(okp); chk(True, "[양성] P 하나 제거는 통과 — 남은 PS₄ 는 온전하다")
        except ValueError:
            chk(False, "[양성] P 제거를 잘못 막았다")
        chk(len(cen) == 8 and len(Li) == 24,
            f"[양성] 케이지 8개(자유 S 4 + Cl 4) · Li 24 (얻은 것 {len(cen)}, {len(Li)})")
        # ★ 음성 — PS4 의 S 를 케이지 중심으로 세면 안 된다
        chk(len(cen) < (np.array(at.get_chemical_symbols()) == "S").sum(),
            "[음성] PS₄ 결합 S 는 케이지 중심에서 빠진다")
        intra = find_hops(at, "intra"); inter = find_hops(at, "inter")
        chk(len(intra) > 0 and len(inter) > 0,
            f"[양성] intra {len(intra)}개 · inter {len(inter)}개 후보")
        chk(intra[0][2] < inter[0][2],
            f"[양성] 최단 intra({intra[0][2]:.2f}) < 최단 inter({inter[0][2]:.2f}) — "
            "케이지 안이 더 가깝다")
        # 끝점 — 조성 보존 + 인덱스 정렬
        i, j, _ = inter[0]
        ini, fin, j2, hop = build_endpoints(at, i, j)
        chk(ini.get_chemical_symbols() == fin.get_chemical_symbols(),
            "[양성] 두 끝점의 원자 목록이 같다 (NEB 보간 전제)")
        chk(len(ini) == len(at) - 1, "[양성] 공공이 정확히 하나 생긴다")
        moved = np.linalg.norm(fin.positions - ini.positions, axis=1)
        chk(int((moved > 1e-8).sum()) == 1,
            f"[양성] 움직인 원자가 정확히 하나 (얻은 것 {int((moved>1e-8).sum())})")
        chk(abs(moved.max() - hop) < 1e-6 and hop < 5.0,
            f"[양성] 이동거리 = 최소이미지 hop ({hop:.3f} Å)")
        # ★ 음성 — 잘못된 입력을 막아야 한다
        for bad, why in (((i, i), "같은 원자"), ):
            try:
                build_endpoints(at, *bad); chk(False, f"[음성] {why} 를 막지 못했다")
            except ValueError:
                chk(True, f"[음성] {why} 는 ValueError 로 막는다")
        p_idx = int(np.where(np.array(at.get_chemical_symbols()) == "P")[0][0])
        try:
            build_endpoints(at, p_idx, j); chk(False, "[음성] Li 아닌 원자를 막지 못했다")
        except ValueError:
            chk(True, "[음성] Li 가 아닌 자리는 ValueError 로 막는다")
        # ★ 음성 — Li 없는 구조는 케이지 배정이 죽어야 한다
        noli = at[[k for k, s in enumerate(at.get_chemical_symbols()) if s != "Li"]]
        try:
            cage_assign(noli); chk(False, "[음성] Li 없는 구조를 통과시켰다")
        except ValueError:
            chk(True, "[음성] Li 없는 구조는 ValueError")
        # ★ 음성 — 좁은 셀 거부 로직 (min_width 비교 자체)
        _mc = read(ROOT / "db" / "structures" / "modelC_DFT_EOS_V0.cif").cell
        chk(lambda1(_mc) < MIN_WIDTH_A,
            f"[음성] modelC 원본 셀은 λ₁ {lambda1(_mc):.2f} < {MIN_WIDTH_A} Å 로 걸린다")
        # ★★ 지표 정정 회귀시험 (2026-08-20) — 면 높이로 게이트를 걸면 **판정이 뒤집힌다**
        _fcc = np.array([[0, 7.3339, 7.3339], [7.3339, 0, 7.3339], [7.3339, 7.3339, 0]])
        chk(abs(lambda1(_fcc) - 10.372) < 0.01,
            f"[양성] Li₃Nd 2×2×2 λ₁ = {lambda1(_fcc):.3f} (정본 카드 10.372 와 일치)")
        chk(abs(perp_widths(_fcc).min() - 8.469) < 0.01,
            f"[양성] 같은 셀 면높이 = {perp_widths(_fcc).min():.3f} (8.469)")
        chk(lambda1(_fcc) >= MIN_WIDTH_A and perp_widths(_fcc).min() < MIN_WIDTH_A,
            "[음성] ★ 면높이로 게이트를 걸면 **통과할 셀을 거부한다** — 지표를 되돌리면 여기서 깨진다")
        chk(lambda1(_fcc) > perp_widths(_fcc).min(),
            "[음성] 비직교 셀에서 면높이는 λ₁ 의 하한이다 (역전되면 정의가 틀린 것)")
        _cub = np.eye(3) * 10.06
        chk(abs(lambda1(_cub) - perp_widths(_cub).min()) < 1e-6,
            "[양성] 직교 셀에서는 둘이 일치한다 (comp1 계열에서 판정이 안 바뀐 이유)")
        # ★★ codex 2차 반례 — 고정 R=3 은 기운 셀에서 틀린다 (2.492 vs 실제 0.402)
        _skew = np.array([[10.0, 0, 0], [2.49, 0.1, 0], [0, 0, 10.0]])
        chk(abs(lambda1(_skew) - 0.402) < 0.01,
            f"[음성] ★ 기운 셀 λ₁ = {lambda1(_skew):.4f} (고정 R=3 이면 2.492 로 틀린다)")
        # fallback 재구현이 없다는 것 자체를 고정한다
        import inspect as _insp
        # docstring 은 빼고 **코드 본문만** 본다 — 설명문에 'except BaseException' 이 나온다
        _srcL = _insp.getsource(lambda1)
        _body = _srcL.split('"""')[-1] if _srcL.count('"""') >= 2 else _srcL
        chk("itertools" not in _body and "np.linalg.norm" not in _body,
            "[음성] ★ lambda1 이 λ₁ 을 **재구현하지 않는다** (fallback 되살리면 깨진다)")
        chk("RuntimeError" in _body,
            "[음성] ★ 정본을 못 읽으면 **hard fail** 한다 (조용히 다른 값을 내지 않는다)")
    except ImportError:
        print("  ⚠ ase 없음 — 구조 시험 건너뜀")

    # ── 끝점 심화 이완 (EMT 로 검증 — UMA 없이 돈다) ──────────────────────
    try:
        from ase.build import bulk
        from ase.calculators.emt import EMT
        rng = np.random.default_rng(3)
        base = bulk("Cu", "fcc", a=3.6, cubic=True) * (2, 2, 2)

        # ★★ [양성] **탈출이 실제로 발동하는지**를 이중우물로 확인한다.
        #    EMT/Cu 만으로는 rattle 이 넘을 얕은 분지가 없어 gain 이 늘 0 이었고,
        #    그건 "통과했지만 아무것도 보증 못 하는" 양성이다 (2026-08-19 자체 지적).
        from ase.calculators.calculator import Calculator
        from ase import Atoms as _A

        class DoubleWell(Calculator):
            """원자 0 의 x 에 이중우물. 최소 x=±W, x<0 쪽이 TILT 만큼 깊다."""
            implemented_properties = ["energy", "forces"]
            W, K, TILT = 0.15, 60.0, 0.20

            def calculate(self, atoms=None, properties=None, system_changes=None):
                Calculator.calculate(self, atoms, properties, system_changes)
                p = atoms.get_positions()
                x = p[0, 0]
                u = x * x - self.W ** 2
                e = self.K * u * u + self.TILT * x + 0.5 * (p[:, 1:] ** 2).sum()
                f = np.zeros_like(p)
                f[0, 0] = -(self.K * 4.0 * x * u + self.TILT)
                f[:, 1:] = -p[:, 1:]
                self.results = {"energy": float(e), "forces": f}

        # 얕은 쪽(x>0) 에서 출발 → 한 번 이완은 거기 갇히고, 심화 이완은 깊은 쪽으로 넘어야 한다
        dw = _A("H2", positions=[[+0.15, 0, 0], [3.0, 0, 0]], cell=[9, 9, 9], pbc=True)
        one, _, _ = relax_positions(dw, DoubleWell(), fmax=0.01, steps=300)
        e_one = float(one.get_potential_energy())
        deep, info = relax_endpoint_deep(dw, DoubleWell(), fmax=0.01, steps=300,
                                         tries=6, amp=0.5, seed=1)
        chk(one.get_positions()[0, 0] > 0,
            "[음성] 한 번 이완은 얕은 우물(x>0)에 갇힌다 — 갇혀야 시험이 성립한다")
        chk(info["n_escapes"] >= 1,
            f"[양성] ★ 심화 이완이 **실제로 탈출한다** ({info['n_escapes']}회, "
            f"gain {1000*info['gain_eV']:+.0f} meV)")
        chk(deep.get_positions()[0, 0] < 0,
            "[양성] 탈출 뒤 깊은 우물(x<0)에 앉는다")
        chk(info["E"] < e_one - 1e-6, "[양성] 탈출한 에너지가 한 번 이완보다 낮다")
        chk(info["E_first"] >= info["E"] - 1e-9, "[양성] gain 은 음수가 될 수 없다")

        # [음성] 흔들어 놓은 실제 결정에서도 한 번 이완보다 높아지지 않는다
        shaken = base.copy()
        shaken.set_positions(shaken.get_positions()
                             + rng.normal(0, 0.25, shaken.get_positions().shape))
        one2, _, _ = relax_positions(shaken, EMT(), fmax=0.05, steps=200)
        _, info1 = relax_endpoint_deep(shaken, EMT(), fmax=0.05, steps=200, seed=1)
        chk(info1["E"] <= float(one2.get_potential_energy()) + 1e-9,
            "[음성] 심화 이완이 한 번 이완보다 높아지는 일은 없다")

        # [음성] **이미 바닥인 구조에서는 헛돌지 않는다** — 탈출 0회여야 한다
        flat, info2 = relax_endpoint_deep(base, EMT(), fmax=0.05, steps=200, seed=2)
        chk(info2["n_escapes"] == 0,
            "[음성] 완전한 결정에서는 얕은 분지 탈출이 0회다 (헛돌면 비용만 든다)")

        # ★★ [음성] 추적 원자가 자리를 옮기는 탈출은 **더 낮아도 버려야 한다**
        #    (2026-08-19 실측: 홉이 3.504 → 4.356 Å 로 바뀐 채 값이 나왔다)
        _, free = relax_endpoint_deep(dw, DoubleWell(), fmax=0.01, steps=300,
                                      tries=6, amp=0.5, seed=1)
        kept, guard = relax_endpoint_deep(dw, DoubleWell(), fmax=0.01, steps=300,
                                          tries=6, amp=0.5, seed=1,
                                          track_idx=0, max_track_drift=0.05)
        chk(free["n_escapes"] >= 1 and guard["n_escapes"] == 0,
            "[음성] 추적 원자가 0.05 Å 넘게 움직이는 탈출은 채택하지 않는다")
        chk(guard["n_rejected"] >= 1, "[음성] 버린 횟수를 n_rejected 로 보고한다")
        chk(kept.get_positions()[0, 0] > 0,
            "[음성] 가드가 걸리면 원래(얕은) 우물에 남는다 — 홉이 안 바뀐다")
        # 여유롭게 주면 통과해야 한다 (가드가 항상 막기만 하면 쓸모없다)
        _, loose = relax_endpoint_deep(dw, DoubleWell(), fmax=0.01, steps=300,
                                       tries=6, amp=0.5, seed=1,
                                       track_idx=0, max_track_drift=5.0)
        chk(loose["n_escapes"] >= 1 and loose["n_rejected"] == 0,
            "[양성] 허용치가 넉넉하면 탈출을 그대로 채택한다")

        # [음성] hop_distance 가 **최소이미지**로 재는지 — 셀을 가로지르면 짧은 길
        a1 = base.copy(); a2 = base.copy()
        L = float(np.array(base.cell)[0, 0])
        a2.positions[0] = a1.positions[0] + np.array([L - 0.7, 0.0, 0.0])
        chk(abs(hop_distance(a1, a2, 0) - 0.7) < 1e-6,
            "[음성] 셀을 가로지르는 이동을 L−0.7 이 아니라 0.7 Å 로 잰다")

        # ── fmax 꼬리 추세 (2026-08-20) — **판정을 안 바꾸는 순수 보고**
        import tempfile as _tf, os as _os
        def _mk(vals):
            fd, path = _tf.mkstemp(suffix=".log"); _os.close(fd)
            Path(path).write_text(
                "".join(f"FIRE:  {i:4d} 00:00:0{i%10}   -429.0{i:04d}   {v:.6f}\n"
                        for i, v in enumerate(vals)))
            return path
        # ★ 실측 재현: comp1 2×1×1 의 마지막 4스텝은 fmax 가 단조 상승했다
        rise = _mk([0.192, 0.203, 0.211, 0.218, 0.226, 0.231])
        chk(fmax_trend(rise)["verdict"] == "rising",
            "[양성] ★ 오르는 꼬리를 'rising' 으로 (comp1 실측 재현)")
        chk("소용없다" in fmax_trend_text(fmax_trend(rise)),
            "[양성] rising 이면 '스텝 늘려도 소용없다' 를 말한다")
        drop = _mk([0.50, 0.44, 0.39, 0.33, 0.28, 0.24])
        chk(fmax_trend(drop)["verdict"] == "converging",
            "[음성] 내려가는 꼬리를 rising 으로 오판하지 않는다")
        flat = _mk([0.300, 0.299, 0.301, 0.300, 0.299, 0.300])
        chk(fmax_trend(flat)["verdict"] == "flat",
            "[음성] 정체를 수렴으로도 발산으로도 읽지 않는다")
        chk(fmax_trend(None) is None and fmax_trend("/nonexistent.log") is None,
            "[음성] 로그가 없으면 None — 없는 것을 '수렴 중' 으로 말하지 않는다")
        chk(fmax_trend(_mk([0.3, 0.2])) is None,
            "[음성] 스텝이 4개 미만이면 판정하지 않는다")
        chk(fmax_trend_text(None) == "", "[음성] None 이면 빈 문자열 (출력에 안 낀다)")
        for _p in (rise, drop, flat):
            _os.unlink(_p)
    except ImportError:
        print("  ⚠ ase 없음 — 심화 이완 시험 건너뜀")

    # ── split NEB: 중간자리 식별 (음성 경로 포함) ────────────────────────────
    # 실측 밴드 (comp1 inter_211_deepep) — 이미지 4 가 시작보다 0.462 eV 낮다.
    real = [0.0, -0.2669, -0.0175, 0.4322, -0.462, 0.2468, -0.0793, -0.179, -0.0045]
    m, d = find_intermediate(real)
    chk(m == 4, f"[양성] 실측 inter 밴드의 가장 깊은 내부 극소 = 이미지 4 (얻은 값 {m})")
    # 양옆은 0.4322(왼) / 0.2468(오) — **낮은 쪽**(오)을 기준으로 잰다 = 0.2468−(−0.462)
    chk(abs(d - (0.2468 + 0.462)) < 1e-6, f"[양성] 극소 깊이 = 양옆 낮은 쪽 대비 {d:.4f} eV")

    # 단조 증가/감소 밴드에는 내부 극소가 없다
    chk(find_intermediate([0.0, 0.1, 0.2, 0.3, 0.2, 0.1])[0] is None,
        "[음성] 단봉(정상 홉) 밴드에서는 쪼갤 자리를 만들지 않는다")
    chk(find_intermediate([0.0, 0.2, 0.5, 0.9, 1.2])[0] is None,
        "[음성] 단조 증가 밴드에서 내부 극소를 지어내지 않는다")
    chk(find_intermediate([0.0, 0.5, 0.0])[0] is None,
        "[음성] 이미지 5개 미만이면 판정하지 않는다")
    # 끝점은 후보가 아니다 — 시작이 최저여도 index 0 을 돌려주면 안 된다
    chk(find_intermediate([0.0, 0.4, 0.8, 0.6, 0.9])[0] == 3,
        "[음성] 끝점(0/-1)을 중간자리로 잡지 않는다")
    # 봉우리(국소 최대)를 극소로 오독하면 안 된다
    chk(find_intermediate([0.0, 0.9, 0.2, 0.9, 0.1])[0] == 2,
        "[음성] 국소 최대를 극소로 오독하지 않는다")
    # 극소가 둘이면 더 깊은 쪽
    chk(find_intermediate([0.0, 0.9, 0.3, 0.9, -0.4, 0.9, 0.2])[0] == 4,
        "[양성] 극소가 여럿이면 가장 깊은 것을 고른다")

    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--struct", default="db/structures/comp1_V0_k444.cif")
    ap.add_argument("--supercell", nargs=3, type=int, default=[1, 1, 1])
    ap.add_argument("--kind", choices=["intra", "inter"], default="inter")
    ap.add_argument("--pick", type=int, default=0, help="후보 목록에서 몇 번째 (0=최단)")
    ap.add_argument("--pair", help="'i,j' 로 짝을 직접 지정 (재현·앙상블용)")
    ap.add_argument("--n_images", type=int, default=N_IMAGES)
    ap.add_argument("--neb_steps", type=int, default=STEPS_NEB)
    ap.add_argument("--rmax", type=float, default=5.0)
    ap.add_argument("--cage_margin", type=float, default=0.3)
    ap.add_argument("--min_width", type=float, default=MIN_WIDTH_A)
    ap.add_argument("--force", action="store_true", help="좁은 셀도 실행 (수렴시험용)")
    ap.add_argument("--split", action="store_true",
                    help="밴드에 내부 극소가 있으면 그 자리를 이완해 **두 구간 NEB** 로 쪼갠다 "
                         "(inter-cage 처방: 단일 NEB 가 elementary 가 아니다)")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--tag")
    ap.add_argument("--max_ep_drift", type=float, default=0.6,
                    help="끝점 심화 이완에서 **이동 Li 가 이만큼(Å) 넘게 움직이면 그 탈출을 "
                         "버린다**. 더 낮은 분지라도 홉이 바뀌면 다른 사건이다 "
                         "(2026-08-19 실측: 3.504 → 4.356 Å 로 바뀐 적이 있다).")
    ap.add_argument("--seed", type=int, default=0,
                    help="끝점 심화 이완의 rattle 시드")
    ap.add_argument("--shallow_endpoints", action="store_true",
                    help="옛 동작 — 끝점을 한 번만 이완한다(심화 이완 끔). "
                         "심화 이완이 홉을 바꿔버린 것 같을 때 대조용.")
    ap.add_argument("--out", default=str(OUTDIR / "argyrodite_cage_neb.json"))
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    a = ap.parse_args()
    rec = one_run(a)
    p = Path(a.out)
    db = json.loads(p.read_text()) if p.exists() else {
        "what": "UMA-s-1p1(omat) CI-NEB for a single Li vacancy hop in bulk "
                "argyrodite. Cell is NEVER relaxed - see module docstring.",
        "caveat": "Single arrangement, single path. NOT a percolation barrier. "
                  "Absolute values are MLIP, not DFT.",
        "runs": []}
    db["runs"] = [r for r in db.get("runs", []) if r.get("tag") != rec["tag"]] + [rec]
    p.write_text(json.dumps(db, ensure_ascii=False, indent=2))
    print(f"\n→ {p}   (누적 {len(db['runs'])}건)")


if __name__ == "__main__":
    main()
