#!/usr/bin/env python3
"""dft_decomp_check.py — 조성이 다른 두 구조를 **DFT 로** 공정하게 비교한다.

왜 필요한가 (2026-08-26, Y 자리선호):
  자리선호 판정이 전부 UMA 다. 여유 28.3 meV/atom 이 MLIP 오차 규모를 넘었지만
  **한 포텐셜의 답**이고, 우리는 방금 같은 UMA 가 b2o3 골격을 무르게 본다는 것을
  확인했다. DFT 대조가 남은 유일한 축이다.

왜 E_above_hull 을 DFT 로 바로 못 재나:
  MP 엔트리는 VASP PAW PBE(+보정)이고 우리는 QE USPP 다. 섞으면 hull 이 틀린다.
  전 MP 상을 우리 설정으로 다시 계산하는 것은 비현실적이다.

이 도구의 방법 — **공통 분해상 기저**:
  Y 두 모델은 UMA 에서 **같은 5상**으로 분해된다
  (Li3PS4 · Li2S · Li3PO4 · LiYS2 · LiCl). 그리고 두 조성 모두 그 5상의
  **양의 조합으로 정확히** 표현된다(잔차 1e-14, 손검산 확인).
  ⇒ 그 5상 + 두 구조 **7개만** 같은 QE 설정으로 계산하면 비교가 닫힌다. MP 불필요.

    ΔE_decomp(X) = [ Σ nᵢ·E(상ᵢ) − E(X) ] / N_atoms(X)      (클수록 안정)

  두 구조가 **같은 기저**로 재므로 상들의 절대 오차가 상쇄되지는 않지만,
  **같은 방향으로 실려** 비교의 부호를 뒤집기 어렵다.

⛔ 이 도구가 **못 하는 것**
  · E_above_hull 이 아니다. 5상 밖의 더 낮은 분해 경로가 있으면 못 본다
    (그 후보는 UMA hull 이 골라준 것이고, DFT 에서 같다는 보장은 없다).
  · 절대 생성엔탈피를 주지 않는다. **두 구조의 상대 비교**만 한다.
  · 구조를 만들지 않는다. --prepare 는 MP 에서 상 구조를 받아 입력만 쓴다.
  · 계산을 돌리지 않는다. 입력을 쓰고, 나중에 출력을 읽는다.

2026-10-23 확장 (Nd Q2 · 카드 nd_q2_decomp_estimand_2026_10_23.json):
  · --basis <json> — 기저를 파일로 ({"phases": {상: {"formula": {...}, "mp_id": ...}},
    "per_target": {타깃: [상…]}}). 없으면 Y 5 상 그대로.
  · 해가 하나인지 본다 — 기저가 과완비면 (상 수 > 독립 조성 수) lstsq 의 최소 노름 해는
    물리 분해가 아니다 → 거부하고 per_target 을 쓰라고 한다.
  · --phase_structs <폴더> — MP 대신 그 폴더의 <상>.cif 로 입력을 쓴다 (MP 키 불필요) ·
    --save_phase_structs <폴더> — MP 에서 받은 구조를 cif 로 남긴다.
  · --kspacing_phase · --calculation_phase · --smearing · --degauss · --conv_thr · --mixing_beta
    — 상 입력 설정을 넘긴다 (안 주면 예전 값 그대로).
  · --collect --bulk_modulus_GPa B0 --bulk_modulus_range Bmin Bmax — 타깃마다 압력 P 로
    ΔE_V = −P²V/(2B) 어림 (EOS 대신 · CLAUDE.md 2026-10-23 규칙) · --pair A B 로 Y = ΔE_A − ΔE_B ·
    G_V (|P| ≤ 2 GPa · 셀 간 보정 차 ≤ 1 meV/atom) · 분해능 (--resolution_meV) · 상 Pulay 차.

2026-10-26 확장 (Nd Q2 · 카드 §4 G_k_탐침 · 결과 전):
  · --kprobe --runs <본 런 폴더> — 본 런 (잡마다 scf.in · scf.out) 의 이완 끝 기하로 k 탐침 scf 입력을 쓴다.
    상 (기저 안) = 최종 셀 + 좌표 · k 간격 --kspacing_phase · --phase_symmetry 면 nosym = .false. ·
    타깃 (기저 밖) = 좌표만 · k --kpoints · nosym 은 본 입력 그대로. calculation = 'scf' · &IONS · &CELL 을 뺀다.
    기하는 tools/sei/splice_relaxed.py 가 덮어쓴다 (같은 판정 · 같은 실패). 러너 설정 균일성 검사가
    nosym 까지 보므로 <out>/phase · <out>/target 두 폴더로 나눠 쓴다.
  · --kprobe_read --runs <본 런> --probe <탐침 폴더> — 잡마다 |E(탐침) − E(본)| / 원자 를 셈해
    상은 > GK_MAX_MEV 면 '탐침 값을 쓴다' · 타깃은 > GK_MAX_MEV 면 'k 한계' 로 판정한다 (Y 는 안 셈).

  ⛔ 확장이 못 하는 것
    · 압력 어림은 조화 근사다 — |P| 가 크면 (> 2 GPa) 틀어진다 (그래서 G_V 가 EOS 로 넘긴다)
    · 비등방 응력 (모양) 은 안 본다 — P (평균) 만 쓴다
    · V 는 타깃 입력 (<out>/in/<타깃>.in) 의 셀이다 — 고정셀 계산에만 맞다

사용:
  python3 tools/doping/dft_decomp_check.py --selftest
  MP_API_KEY=... python3 tools/doping/dft_decomp_check.py --prepare \\
      --targets a.cif b.cif --out runs/y_dft
  python3 tools/doping/dft_decomp_check.py --collect --out runs/y_dft
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

#: 공통 분해 기저 — UMA hull 이 두 모델 모두에 대해 고른 5상.
#:   ⚠ 이 목록을 바꾸면 비교의 기준이 바뀐다. 바꿀 때는 두 조성이 여전히
#:     **양의 조합으로 정확히** 표현되는지 balance() 가 확인한다.
DEFAULT_BASIS = {
    "Li3PS4": {"Li": 3, "P": 1, "S": 4},
    "Li2S":   {"Li": 2, "S": 1},
    "Li3PO4": {"Li": 3, "P": 1, "O": 4},
    "LiYS2":  {"Li": 1, "Y": 1, "S": 2},
    "LiCl":   {"Li": 1, "Cl": 1},
}
#: MP 에서 받을 때 쓸 대표 mp-id (없으면 조성 검색으로 가장 안정한 것)
BASIS_MPID = {"Li3PS4": None, "Li2S": None, "Li3PO4": None,
              "LiYS2": None, "LiCl": None}

#: MP e_hull 이 이보다 크면 **다른 다형체를 집었을 수 있다**고 보고 경고한다.
#:   ⚠ 2026-08-26 정정 — 처음엔 1e-4 로 잡고 넘으면 거부했는데 **과했다.**
#:     MP 의 e_hull 은 MP 내부 보정 기준(예: Cl₂ gas anion correction)이 섞인
#:     값이라, LiCl 처럼 명백히 안정한 상도 0 이 안 나온다(전 엔트리 최저 0.0039,
#:     암염 mp-22905 는 0.0243). 그리고 **우리는 MP 에너지를 쓰지 않는다** —
#:     구조만 가져와 우리 QE 설정으로 다시 계산하므로 MP e_hull 의 절대값은
#:     비교에 들어가지 않는다. 진짜로 막아야 할 것은 "그 조성의 최저가 아닌 것을
#:     집는 것" 이고, 그건 min(docs) 가 이미 한다. 이 문턱은 **눈에 띄게만** 한다.
OFFHULL_WARN = 0.05

BALANCE_TOL = 1e-8      #: 원소 수지 잔차 허용 (원자 개수 단위)
NEG_TOL = -1e-9         #: 계수 음수 허용 한계


def balance(target: dict, basis: dict = None):
    """target 조성을 basis 상들의 조합으로 푼다. → (coeffs, info)

    ⛔ **풀리지 않으면 풀린 척하지 않는다.** np.linalg.lstsq 는 해가 없어도
      최소제곱 근사를 돌려주므로, 잔차를 재서 BALANCE_TOL 을 넘으면 거부한다.
      이 검사가 없으면 "분해가 성립한다"는 거짓 전제 위에 에너지를 얹게 된다.
    ⛔ 음수 계수도 거부한다 — 음수는 그 상을 **만들어 넣는다**는 뜻이라
      분해가 아니다.
    """
    basis = basis or DEFAULT_BASIS
    els = sorted({e for p in basis.values() for e in p} | set(target))
    A = np.array([[basis[n].get(e, 0) for n in basis] for e in els], float)
    b = np.array([target.get(e, 0) for e in els], float)
    x, *_ = np.linalg.lstsq(A, b, rcond=None)
    resid = float(np.abs(A @ x - b).max())
    neg = [n for n, v in zip(basis, x) if v < NEG_TOL]
    # ⛔ 2026-10-23 — 해가 하나인지. 상 조성이 서로 독립이 아니면 lstsq 는 최소 노름 해를
    #   돌려준다 (물리 분해가 아니다 · 에너지가 그 임의 선택을 따라간다).
    rank = int(np.linalg.matrix_rank(A))
    unique = rank == A.shape[1]
    ok = resid <= BALANCE_TOL and not neg and unique
    info = {"elements": els, "residual_max_atoms": resid,
            "negative_phases": neg, "ok": ok, "rank": rank,
            "n_phases": int(A.shape[1]), "unique": unique,
            "coeffs": {n: float(v) for n, v in zip(basis, x)}}
    if not ok:
        if not unique:
            info["why"] = (f"기저가 과완비다 (상 {A.shape[1]} 개 · 독립 조성 {rank} 개) — "
                           f"분해가 하나로 안 정해진다. 타깃마다 자기 상 목록 (per_target) 을 쓸 것")
        elif resid > BALANCE_TOL:
            info["why"] = (f"원소 수지가 안 맞는다 (잔차 {resid:.3g} 원자 > "
                           f"{BALANCE_TOL:g}) — 이 기저로는 이 조성을 표현할 수 없다")
        else:
            info["why"] = (f"계수가 음수인 상이 있다 {neg} — 분해가 아니라 "
                           f"합성이다")
    return (x if ok else None), info


def decomp_energy(target_comp: dict, target_E: float, phase_E: dict,
                  basis: dict = None):
    """ΔE_decomp = [Σ nᵢ E(상ᵢ) − E(X)] / N_atoms.  클수록 분해에 안정. → dict|None

    ⛔ phase_E 에 기저 상이 하나라도 빠지면 None 을 돌려준다 — 빠진 상을
      0 으로 두면 그 상이 '공짜' 가 되어 값이 통째로 틀린다.
    """
    basis = basis or DEFAULT_BASIS
    missing = [n for n in basis if n not in phase_E]
    if missing:
        return None, {"why": f"상 에너지가 없다: {missing}"}
    x, info = balance(target_comp, basis)
    if x is None:
        return None, info
    nat = sum(target_comp.values())
    e_prod = sum(c * phase_E[n] for c, n in zip(x, basis))
    dE = (e_prod - target_E) / nat
    return {"delta_E_decomp_eV_per_atom": dE,
            "E_products_eV": e_prod, "E_target_eV": target_E,
            "n_atoms": nat, "coeffs": info["coeffs"]}, info


def target_composition(stem: str, out, struct_dir=None):
    """타깃 `stem` 의 조성을 정한다. → (comp|None, 출처, 왜 실패했나)

    **우선순위가 중요하다.** 초판은 `Path(".").glob("**/<stem>.cif")` 로 **현재 디렉터리 밑만**
    뒤졌다 — 구조가 repo 밖(계산 머신의 runs/)에 있으면 조용히 못 찾고 전부 건너뛴다.
    실측 2026-08-26 (kgy): 7/7 계산이 다 끝났는데 타깃 2개가 통째로 빠지고 **빈 결과 JSON 이
    성공처럼** 나왔다.

    그래서 **우리가 직접 만든 QE 입력**(`<out>/in/<stem>.in`)을 1순위로 본다 — 그 계산을
    돌렸다면 반드시 거기 있고, 실제로 계산된 원자 배열 그 자체다. cif 는 보조 경로다.

    ⛔ 이 함수가 못 하는 것
      · 입력과 출력이 같은 계인지 검사하지 않는다 (입력을 바꿔치기하면 못 잡는다).
      · 구조의 옳고 그름을 판정하지 않는다 — 원소 개수만 센다.
    """
    import collections
    from ase.io import read
    from pathlib import Path as _P
    tried = []

    qein = _P(out) / "in" / f"{stem}.in"
    tried.append(str(qein))
    if qein.is_file():
        try:
            at = read(qein, format="espresso-in")
            return (dict(collections.Counter(at.get_chemical_symbols())),
                    f"QE 입력 {qein}", "")
        except Exception as e:                      # 읽기 실패는 **말한다** — 조용히 cif 로 넘어가면
            tried.append(f"  (읽기 실패: {type(e).__name__}: {e})")   # 어느 조성을 썼는지 모르게 된다

    cands = [_P(out) / f"{stem}.cif", _P(out) / "struct" / f"{stem}.cif"]
    if struct_dir:
        cands.append(_P(struct_dir) / f"{stem}.cif")
        cands += list(_P(struct_dir).glob(f"**/{stem}.cif"))
    cands += list(_P(".").glob(f"**/{stem}.cif"))    # 마지막 보루 (초판의 유일한 경로였다)
    for c in cands:
        tried.append(str(c))
        if c.is_file():
            try:
                return (dict(collections.Counter(read(c).get_chemical_symbols())),
                        f"cif {c}", "")
            except Exception as e:
                tried.append(f"  (읽기 실패: {type(e).__name__}: {e})")
    return None, "", ("찾은 곳: " + " · ".join(tried[:6])
                      + (f" … (총 {len(tried)}곳)" if len(tried) > 6 else "")
                      + "  → --struct_dir 로 구조 폴더를 지정할 것")


#: |ΔE_decomp| 이 이보다 크면 **정규화가 틀린 것**으로 보고 거부한다 (eV/atom).
#:  분해 에너지는 물리적으로 수백 meV/atom 규모다. 2026-08-26 실측: 셀당 에너지를
#:  화학식당처럼 써서 **−532 eV/atom** 이 나왔다. 그 값이 화면에 찍혔다는 게 문제였다.
SANITY_MAX_DE_EV = 2.0

#: 2026-10-23 — 압력 어림 · 게이트 문턱 (카드 nd_q2_decomp_estimand_2026_10_23.json §4)
GV_MAX_P_GPA = 2.0          #: G_V — 이보다 크면 조화 어림을 믿지 않는다 (EOS 로)
GV_MAX_PAIR_MEV = 1.0       #: G_V — 두 셀의 원자당 보정 차가 이보다 크면 EOS 로
PULAY_MAX_MEV = 0.5         #: vc-relax 상 — 끝 SCF 와 마지막 BFGS 에너지 차 (원자당)
GK_MAX_MEV = 1.0            #: G_k 탐침 — 본 k 와 탐침 k 의 원자당 에너지 차 문턱 (카드 §4)
#: 러너 run_force_check_scf.sh 의 _UNIFORM_KEYS 에서 nosym 을 뺀 것 — 탐침이 본 입력과 같은 설정인지 본다
_SETTING_KEYS = ("ecutwfc|ecutrho|occupations|smearing|degauss|conv_thr|mixing_mode|mixing_beta|"
                 "electron_maxstep|diagonalization|nspin")
EV_PER_J = 1.0 / 1.602176634e-19


def load_basis(path):
    """--basis 파일 → (basis {상: 조성}, mpids {상: mp-id|None}, per_target {타깃: [상…]}).

    ⛔ 조성이 비었거나 양의 정수가 아니면 거부 · per_target 이 기저 밖 상을 가리키면 거부 —
      반쯤 맞는 기저로 계산을 시작하면 끝에서야 '상 에너지가 없다' 로 멈춘다.
    """
    d = json.loads(Path(path).read_text())
    ph = d.get("phases") or {}
    if not ph:
        raise ValueError(f"{path}: 'phases' 가 비었다")
    basis, mpids = {}, {}
    for name, rec in ph.items():
        f = rec.get("formula") or {}
        if not f or any((not isinstance(v, int)) or v < 1 for v in f.values()):
            raise ValueError(f"{path}: {name} 조성이 양의 정수가 아니다 — {f}")
        basis[name], mpids[name] = dict(f), rec.get("mp_id")
    per = {k: list(v) for k, v in (d.get("per_target") or {}).items()}
    for k, v in per.items():
        bad = [n for n in v if n not in basis]
        if bad:
            raise ValueError(f"{path}: per_target[{k}] 의 {bad} 가 기저에 없다")
    return basis, mpids, per


def parse_qe_pressure_kbar(path):
    """QE 출력의 **마지막** 'total   stress … P=' 압력 (kbar). 없으면 None."""
    try:
        txt = Path(path).read_text(errors="ignore")
    except OSError:
        return None
    hits = re.findall(r"total\s+stress\s+\(Ry/bohr\*\*3\)\s+\(kbar\)\s+P=\s*(-?\d+\.?\d*)", txt)
    return float(hits[-1]) if hits else None


def volume_correction_eV(p_kbar: float, v_A3: float, b_GPa: float) -> float:
    """ΔE_V = −P²V/(2B) (eV) — 그 셀이 제 V₀ 로 갔으면 내려갔을 에너지의 조화 어림 (항상 ≤ 0)."""
    p = p_kbar * 1e8                  # kbar → Pa
    return -(p * p) * (v_A3 * 1e-30) / (2.0 * b_GPa * 1e9) * EV_PER_J


def pulay_gap_meV_per_atom(path, nat: int):
    """vc-relax 출력: 끝 SCF 와 마지막 BFGS 스텝의 에너지 차 (meV/원자).

    끝 SCF = 마지막 'End final coordinates' **뒤의** '!' · 마지막 BFGS = 그 **앞의** 마지막 '!'.
    ⛔ 2026-10-26 — 처음 판은 문구 'A final scf calculation at the relaxed structure' 로 끝 SCF 를 찾았는데,
      QE 7.4.1 은 'Final scf calculation at the relaxed structure.' 로 찍는다 ('A' 없음 · 대문자 F).
      그래서 Nd Q2 의 다섯 상 출력이 전부 None 이 됐고, --collect 는 None 만 있으면 Pulay 줄을 안 찍어서
      **게이트가 조용히 빠졌다** (시험 fixture 가 옛 문구였다). 이제 문구가 아니라 출력 구조로 본다 —
      러너 run_force_check_scf.sh 의 _fc_ok 와 같은 기준이다 (QE 6.x · 7.x 둘 다).
    끝 SCF 가 없으면 (relax · 안 끝남 · nstep 소진) None — 0 으로 두지 않는다.
    """
    try:
        txt = Path(path).read_text(errors="ignore")
    except OSError:
        return None
    k = txt.rfind("End final coordinates")
    if k < 0 or nat < 1 or "bfgs converged" not in txt[:k]:
        return None
    pat = re.compile(r"^!\s+total energy\s+=\s+(-?\d+\.\d+)\s+Ry", re.M)
    before = [float(x) for x in pat.findall(txt[:k])]
    after = [float(x) for x in pat.findall(txt[k:])]
    if not before or not after:
        return None
    return abs(after[-1] - before[-1]) * 13.605693122994 * 1000.0 / nat


def qe_calculation(path) -> str | None:
    """QE 입력의 calculation 값 ('scf' · 'relax' · 'vc-relax' …). 못 읽으면 None."""
    try:
        m = re.search(r"calculation\s*=\s*['\"]([a-z-]+)['\"]", Path(path).read_text(errors="ignore"), re.I)
    except OSError:
        return None
    return m.group(1).lower() if m else None


def _setting_lines(txt: str) -> list:
    return sorted(re.sub(r"\s+", "", ln) for ln in txt.splitlines()
                  if re.match(rf"^\s*({_SETTING_KEYS})\s*=", ln))


def relax_done(out_path) -> tuple:
    """본 런 출력이 끝났나 → (끝남, 무엇으로 봤나). vc-relax = 끝 SCF 까지 · relax = 'bfgs converged' + 최종 좌표."""
    try:
        txt = Path(out_path).read_text(errors="ignore")
    except OSError:
        return False, "출력 없음"
    if "bfgs converged" not in txt or "End final coordinates" not in txt:
        return False, "'bfgs converged' · 'End final coordinates' 없음"
    return True, "bfgs converged + 최종 좌표"


def make_kprobe_input(main_in, main_out, dest, kpts: str | None, spacing: float | None,
                      nosym: bool | None, cell_too: bool):
    """본 입력 · 출력 → 탐침 scf 입력 (dest). → (info|None, why)

    · calculation → 'scf' · &IONS · &CELL 블록을 뺀다 · nosym 은 None 이면 그대로
    · 기하는 splice_relaxed.py 가 덮어쓴다 (cell_too 면 셀까지 · 아니면 --positions_only)
    · k 는 kpts 를 그대로 쓰거나, spacing 이면 **덮어쓴 셀**로 셈한다
    ⛔ 본 입력과 설정 줄 (ecut · smearing · conv_thr · mixing …) 이 하나라도 다르면 거부 · 기하 덮어쓰기가
      실패하면 거부 (반쪽 입력을 남기지 않는다).
    """
    import subprocess
    src = Path(main_in).read_text()
    txt = re.sub(r"(calculation\s*=\s*)['\"][a-z-]+['\"]", r"\1'scf'", src, count=1)
    txt = re.sub(r"^\s*&IONS\b.*?^\s*/\s*\n", "", txt, flags=re.S | re.M | re.I)
    txt = re.sub(r"^\s*&CELL\b.*?^\s*/\s*\n", "", txt, flags=re.S | re.M | re.I)
    if nosym is not None:
        v = ".true." if nosym else ".false."
        txt, n = re.subn(r"^(\s*nosym\s*=\s*)\S+", rf"\g<1>{v}", txt, count=1, flags=re.M | re.I)
        if n == 0:
            txt = re.sub(r"(&SYSTEM[^\n]*\n)", rf"\1    nosym       = {v}\n", txt, count=1, flags=re.I)
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(txt)
    sp = Path(__file__).resolve().parents[1] / "sei" / "splice_relaxed.py"
    r = subprocess.run([sys.executable, str(sp), "--out", str(main_out), "--targets", str(dest)]
                       + ([] if cell_too else ["--positions_only"]), capture_output=True, text=True)
    if r.returncode != 0:
        dest.unlink(missing_ok=True)
        return None, f"기하 덮어쓰기 실패 — {(r.stdout + r.stderr).strip()[-300:]}"
    txt = dest.read_text()
    if spacing:
        from ase.io import read
        kpts = kmesh_from_spacing(read(str(dest), format="espresso-in").cell, spacing)
    txt, nk = re.subn(r"K_POINTS[^\n]*\n[^\n]*\n", f"K_POINTS automatic\n  {kpts} 0 0 0\n", txt, count=1)
    if nk != 1:
        dest.unlink(missing_ok=True)
        return None, "K_POINTS 블록을 못 찾았다"
    dest.write_text(txt)
    if _setting_lines(txt) != _setting_lines(src):
        dest.unlink(missing_ok=True)
        return None, "설정 줄이 본 입력과 다르다 — 쓰지 않았다"
    if re.search(r"^\s*&(IONS|CELL)\b", txt, re.M | re.I) or qe_calculation(dest) != "scf":
        dest.unlink(missing_ok=True)
        return None, "calculation 또는 &IONS · &CELL 정리가 안 됐다"
    km = re.search(r"K_POINTS[^\n]*\n\s*(\d+\s+\d+\s+\d+)", src)
    ns = re.search(r"^\s*nosym\s*=\s*(\S+)", txt, re.M | re.I)
    return {"k_main": km.group(1).split() if km else None, "k_probe": kpts.split(),
            "nosym": ns.group(1) if ns else "(기본 .false.)", "cell_spliced": cell_too}, ""


def kmesh_from_spacing(cell, spacing: float) -> str:
    """k 간격 (Å⁻¹ · 2π 포함) → 'k1 k2 k3' (k_i = ⌈|b_i|/간격⌉ · 최소 1)."""
    b = 2 * np.pi * np.linalg.inv(np.asarray(cell, float)).T
    return " ".join(str(max(1, int(np.ceil(np.linalg.norm(v) / spacing - 1e-9)))) for v in b)


def phase_energy_per_fu(name: str, cell_E: float, out, formula: dict):
    """상의 **셀 총에너지**를 **화학식당** 에너지로 바꾼다. → (E_fu|None, Z|None, 왜)

    왜 필요한가 (2026-08-26 회귀):
      `balance()` 가 돌려주는 계수는 **화학식 단위**(LiCl 8개 …)인데,
      `parse_qe_total` 이 주는 것은 **그 셀 전체**의 에너지다. MP 에서 받은 셀은
      보통 화학식 여러 개(Z>1)를 담고 있어서 그대로 곱하면 Z 배 틀린다.
      실측: LiCl 셀 −96.07 Ry 를 화학식당으로 착각 → ΔE_decomp −532 eV/atom.

    Z 는 셀 조성 ÷ 화학식 조성으로 구하고, **정수가 아니면 거부**한다
    (비정수면 그 셀이 이 화학식의 상이 아니거나 입력이 틀린 것이다).

    ⛔ 이 함수가 못 하는 것
      · 다형체를 구별하지 않는다 — Z 만 본다. 어느 다형체인지는 --prepare 쪽 책임이다.
    """
    comp, src, why = target_composition(name, out, None)
    if comp is None:
        return None, None, f"셀 조성을 못 읽었다 — {why}"
    ratios = []
    for e, n in formula.items():
        if comp.get(e, 0) == 0:
            return None, None, f"셀에 {e} 가 없다 (조성 {comp}, 기대 {formula})"
        ratios.append(comp[e] / n)
    if set(comp) != set(formula):
        return None, None, f"셀 원소가 화학식과 다르다 (셀 {sorted(comp)}, 기대 {sorted(formula)})"
    z = ratios[0]
    if any(abs(r - z) > 1e-9 for r in ratios) or abs(z - round(z)) > 1e-6 or round(z) < 1:
        return None, None, (f"화학식 배수가 정수가 아니다 (셀 {comp} ÷ {formula} → {ratios}) "
                            f"— 이 셀은 {name} 의 상이 아닐 수 있다")
    z = int(round(z))
    return cell_E / z, z, src


def parse_qe_total(path) -> float | None:
    """QE 출력에서 **마지막** 총에너지(Ry→eV). 없으면 None (0 을 지어내지 않는다)."""
    try:
        txt = Path(path).read_text(errors="ignore")
    except OSError:
        return None
    hits = re.findall(r"^!\s+total energy\s+=\s+(-?\d+\.\d+)\s+Ry", txt, re.M)
    if not hits:
        return None
    return float(hits[-1]) * 13.605693122994



def find_pseudo(el: str, pdir: Path, prefer: str = None):
    """pseudo_dir 에서 원소 el 의 UPF 를 찾는다. → (파일명, 사유) | (None, 사유)

    왜 자동 탐색인가 (2026-08-26): 같은 pseudo 인데 머신마다 **구두점 표기가**
      다르다 — KISTI 사본은 `li_pbe_v1_4_uspp_F.UPF`, gabia SSSP 원본은
      `li_pbe_v1.4.uspp.F.UPF`. 이름을 하드코딩하면 머신을 옮길 때마다 깨진다.

    ⛔ 후보가 여럿이면 **고르지 않는다.** 아무거나 집으면 어떤 pseudo 로 계산했는지
      기록이 없어지고, 같은 이름의 다른 판(PAW vs USPP, PBE vs PBEsol)이 섞인다.
      후보를 다 보여주고 사람이 --pseudo_map 으로 정하게 한다.
    """
    if prefer and (pdir / prefer).is_file():
        return prefer, "지정 이름 그대로"
    import re as _re
    pat = _re.compile(rf"^{_re.escape(el)}[._\-]", _re.I)
    cands = sorted(f.name for f in pdir.glob("*.UPF") if pat.match(f.name))
    cands += sorted(f.name for f in pdir.glob("*.upf") if pat.match(f.name))
    # 정확히 원소 기호만인 것(예: 'Y.UPF')도 후보
    cands += [f.name for f in pdir.glob("*.[Uu][Pp][Ff]")
              if f.stem.lower() == el.lower() and f.name not in cands]
    cands = sorted(set(cands))
    if not cands:
        return None, f"{pdir} 에 {el} 로 시작하는 UPF 가 없다"
    if len(cands) > 1:
        return None, f"후보가 {len(cands)}개다 — 사람이 골라야 한다: {cands}"
    return cands[0], "자동 탐색"


def _selftest() -> int:
    n_ok = n_bad = 0

    def chk(c, m):
        nonlocal n_ok, n_bad
        print(("  ✓ " if c else "  ✗ ") + m)
        n_ok, n_bad = n_ok + bool(c), n_bad + (not c)

    # ── 양성: 실제 두 조성이 정확히 풀린다 ──────────────────────────────
    li = {"Li": 42, "Y": 2, "P": 8, "S": 37, "O": 3, "Cl": 8}
    pb = {"Li": 52, "Y": 2, "P": 6, "S": 37, "O": 3, "Cl": 8}
    x1, i1 = balance(li)
    x2, i2 = balance(pb)
    chk(x1 is not None and i1["residual_max_atoms"] < 1e-9,
        "sc_Li_24g 가 5상 기저로 정확히 풀린다")
    chk(x2 is not None and i2["residual_max_atoms"] < 1e-9,
        "sc_P_4b 도 같은 기저로 정확히 풀린다")
    chk(abs(i1["coeffs"]["Li3PS4"] - 7.25) < 1e-9 and
        abs(i2["coeffs"]["Li2S"] - 12.0) < 1e-9,
        "계수가 손검산과 일치 (Li3PS4 7.25 · Li2S 12)")

    # ── ★ 음성: 안 풀리는데 근사해를 내놓지 않는가 ──────────────────────
    bad = {"Li": 42, "Y": 2, "P": 8, "S": 37, "O": 3, "Cl": 8, "Br": 4}
    xb, ib = balance(bad)
    chk(xb is None and "수지가 안 맞는다" in ib.get("why", ""),
        "★ [음성] 기저에 없는 원소(Br)가 있으면 **거부** — lstsq 근사해를 쓰지 않는다")

    # 원소는 다 있는데 조합으로 표현 불가한 경우
    bad2 = {"Li": 1, "Y": 0, "P": 0, "S": 0, "O": 1, "Cl": 0}   # LiO — 불가
    xb2, ib2 = balance(bad2)
    chk(xb2 is None, "[음성] 표현 불가 조성(LiO)도 거부한다")

    # 음수 계수
    neg = {"Li": 0, "P": 1, "S": 4}          # PS4 만 — Li 를 빼야 하므로 음수
    xn, inf_n = balance(neg)
    chk(xn is None and inf_n.get("negative_phases"),
        "[음성] 음수 계수(합성)면 거부한다")

    # ── 에너지 계산 ────────────────────────────────────────────────────
    E = {"Li3PS4": -100.0, "Li2S": -20.0, "Li3PO4": -80.0,
         "LiYS2": -50.0, "LiCl": -10.0}
    r, _ = decomp_energy(li, -1000.0, E)
    want = ((7.25 * -100 + 4 * -20 + 0.75 * -80 + 2 * -50 + 8 * -10) + 1000.0) / 100
    chk(r and abs(r["delta_E_decomp_eV_per_atom"] - want) < 1e-9,
        "ΔE_decomp 산식이 맞다 (손계산 대조)")
    chk(r["n_atoms"] == 100, "원자수로 정규화한다 (조성이 달라도 비교 가능)")

    r2, i3 = decomp_energy(li, -1000.0, {k: v for k, v in E.items() if k != "LiCl"})
    chk(r2 is None and "LiCl" in i3.get("why", ""),
        "★ [음성] 상 에너지가 하나 빠지면 None — 0 으로 채워 '공짜' 로 만들지 않는다")

    # ── 타깃 조성 찾기 (2026-08-26 회귀: 구조를 CWD 밑에서만 찾아 전부 건너뛰었다) ──
    import tempfile, os
    from pathlib import Path as _P
    with tempfile.TemporaryDirectory() as td:
        td = _P(td)
        (td / "in").mkdir()
        # 우리가 만드는 것과 같은 꼴의 최소 QE 입력
        (td / "in" / "tgt.in").write_text(
            "&CONTROL\n calculation='scf'\n/\n&SYSTEM\n ibrav=0\n nat=3\n ntyp=2\n"
            " ecutwfc=60\n/\n&ELECTRONS\n/\n"
            "ATOMIC_SPECIES\n Li 6.94 li.upf\n Cl 35.45 cl.upf\n"
            "CELL_PARAMETERS angstrom\n 5.0 0.0 0.0\n 0.0 5.0 0.0\n 0.0 0.0 5.0\n"
            "ATOMIC_POSITIONS angstrom\n Li 0.0 0.0 0.0\n Li 2.5 0.0 0.0\n Cl 0.0 2.5 0.0\n"
            "K_POINTS gamma\n")
        c, src, why = target_composition("tgt", td, None)
        chk(c == {"Li": 2, "Cl": 1}, "★ 조성을 **QE 입력**에서 읽는다 (구조 파일이 없어도 된다)")
        chk("in" in src and "tgt.in" in src, "조성 출처를 기록한다 (어느 파일을 썼는지)")

        # [음성] 입력도 cif 도 없으면 → None + **어디를 찾았는지** 말한다
        cwd = os.getcwd()
        try:
            os.chdir(td)                      # CWD 밑에도 없게 만든다
            c2, _, why2 = target_composition("nosuch", td, None)
        finally:
            os.chdir(cwd)
        chk(c2 is None, "[음성] 구조를 못 찾으면 None (0 이나 빈 조성을 지어내지 않는다)")
        chk("찾은 곳:" in why2 and "--struct_dir" in why2,
            "★ [음성] 실패 사유에 **찾아본 경로**와 다음 수단을 적는다")

        # ── 셀당 → 화학식당 (2026-08-26 회귀: 이걸 안 해서 -532 eV/atom 이 찍혔다) ──
        def _wr(stem, syms):
            sp = sorted(set(syms))
            (td / "in" / f"{stem}.in").write_text(
                "&CONTROL\n calculation='scf'\n/\n&SYSTEM\n ibrav=0\n"
                f" nat={len(syms)}\n ntyp={len(sp)}\n ecutwfc=60\n/\n&ELECTRONS\n/\n"
                "ATOMIC_SPECIES\n" + "".join(f" {e} 1.0 {e.lower()}.upf\n" for e in sp)
                + "CELL_PARAMETERS angstrom\n 9.0 0.0 0.0\n 0.0 9.0 0.0\n 0.0 0.0 9.0\n"
                "ATOMIC_POSITIONS angstrom\n"
                + "".join(f" {e} {i*0.7:.2f} 0.0 0.0\n" for i, e in enumerate(syms))
                + "K_POINTS gamma\n")

        _wr("LiCl", ["Li"] * 4 + ["Cl"] * 4)          # Z = 4 인 셀
        efu, z, src2 = phase_energy_per_fu("LiCl", -400.0, td, {"Li": 1, "Cl": 1})
        chk(z == 4 and abs(efu - (-100.0)) < 1e-9,
            "★ 셀당 에너지를 화학식당으로 나눈다 (Z=4 → E/4) — 안 하면 Z 배 틀린다")

        _wr("Li2S", ["Li"] * 5 + ["S"] * 2)           # Li:S = 5:2 → 배수 불일치
        e3, z3, why3 = phase_energy_per_fu("Li2S", -10.0, td, {"Li": 2, "S": 1})
        chk(e3 is None and "정수가 아니다" in why3,
            "★ [음성] 화학식 배수가 정수가 아니면 거부 (그 셀은 그 상이 아니다)")

        _wr("LiCl2", ["Li"] * 2 + ["Cl"] * 2 + ["O"])  # 원소가 하나 더 있다
        e4, z4, why4 = phase_energy_per_fu("LiCl2", -10.0, td, {"Li": 1, "Cl": 1})
        chk(e4 is None and "원소" in why4,
            "[음성] 셀에 화학식에 없는 원소가 섞이면 거부")

    # 정신차림 문턱 — 물리적으로 불가능한 크기를 '결과' 로 내보내지 않는다
    chk(SANITY_MAX_DE_EV <= 2.0,
        f"ΔE_decomp 상한이 {SANITY_MAX_DE_EV} eV/atom 로 잡혀 있다 (-532 사고 재발 방지)")
    r_big, _ = decomp_energy(li, -1e6, E)
    chk(abs(r_big["delta_E_decomp_eV_per_atom"]) > SANITY_MAX_DE_EV,
        "★ [음성] 정규화가 틀린 입력은 상한을 넘는다 — collect 가 이걸 보고 죽는다")

    # ── QE 파서 ────────────────────────────────────────────────────────
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "x.out"
        f.write_text("!    total energy              =   -100.5 Ry\n"
                     "!    total energy              =   -101.5 Ry\n")
        chk(abs(parse_qe_total(f) - (-101.5 * 13.605693122994)) < 1e-6,
            "QE 파서: **마지막** 총에너지를 쓴다 (relax 중간값이 아니라)")
        f.write_text("no energy here\n")
        chk(parse_qe_total(f) is None,
            "[음성] 총에너지가 없으면 None — 0 을 지어내지 않는다")
        chk(parse_qe_total(Path(td) / "nope.out") is None,
            "[음성] 없는 파일도 None")

    # ── pseudo 자동 탐색 ────────────────────────────────────────────────
    import tempfile as _tf
    with _tf.TemporaryDirectory() as td:
        d = Path(td)
        (d / "li_pbe_v1.4.uspp.F.UPF").write_text("x")
        (d / "O.pbe-n-kjpaw_psl.0.1.UPF").write_text("x")
        n, why = find_pseudo("Li", d)
        chk(n == "li_pbe_v1.4.uspp.F.UPF",
            "★ 구두점이 달라도 찾는다 (li_pbe_v1_4… ↔ li_pbe_v1.4…)")
        chk(find_pseudo("O", d)[0] == "O.pbe-n-kjpaw_psl.0.1.UPF",
            "대문자 원소도 찾는다")
        chk(find_pseudo("Y", d)[0] is None,
            "[음성] 없으면 None — 아무거나 집지 않는다")
        (d / "Li.pbe-s-kjpaw_psl.1.0.0.UPF").write_text("x")
        n2, why2 = find_pseudo("Li", d)
        chk(n2 is None and "후보가 2개" in why2,
            "★ [음성] 후보가 여럿이면 **거부** — PAW/USPP 가 섞이면 계산이 달라진다")
        chk(find_pseudo("Li", d, prefer="Li.pbe-s-kjpaw_psl.1.0.0.UPF")[0]
            == "Li.pbe-s-kjpaw_psl.1.0.0.UPF",
            "지정 이름이 있으면 그걸 쓴다 (사람이 고른 것 우선)")
        chk(find_pseudo("Li", d, prefer="nope.UPF")[0] is None,
            "[음성] 지정 이름이 없으면 자동으로 넘어가되 모호하면 여전히 거부")

    # ══ 2026-10-23 확장 (Nd Q2) ═══════════════════════════════════════════
    import subprocess
    # 과완비 기저 — Li6PS5Cl = Li3PS4 + Li2S + LiCl 이라 독립이 아니다
    ov = {"Li3PS4": {"Li": 3, "P": 1, "S": 4}, "Li2S": {"Li": 2, "S": 1},
          "LiCl": {"Li": 1, "Cl": 1}, "Li6PS5Cl": {"Li": 6, "P": 1, "S": 5, "Cl": 1}}
    xo, io_ = balance({"Li": 54, "P": 10, "S": 44, "Cl": 16}, ov)
    chk(xo is None and "과완비" in io_.get("why", "") and io_["rank"] == 3,
        "★ [음성] 과완비 기저 (상 4 · 독립 3) 는 **거부** — 최소 노름 해를 분해로 쓰지 않는다")
    # 같은 조성 다형체 둘 (예: Li3PO4 β · γ) — 최소 노름 해가 둘로 **양수로** 나눠 버린다
    #   (음수 계수 검사로는 못 잡는다 · 해 하나 검사만 잡는다)
    poly = {"Li2S": {"Li": 2, "S": 1}, "Li2S_b": {"Li": 2, "S": 1}, "LiCl": {"Li": 1, "Cl": 1}}
    xp, ip = balance({"Li": 5, "S": 2, "Cl": 1}, poly)
    chk(xp is None and "과완비" in ip.get("why", "") and not ip["negative_phases"],
        "★ [음성] 같은 조성 다형체 둘이 기저에 있으면 거부 — 계수가 다 양수여도 (최소 노름 해가 반씩 나눔)")
    h3 = {k: ov[k] for k in ("Li3PS4", "Li2S", "LiCl")}
    xh, ih = balance({"Li": 54, "P": 10, "S": 44, "Cl": 16}, h3)
    chk(xh is not None and ih["unique"] and abs(ih["coeffs"]["Li2S"] - 4) < 1e-9
        and abs(ih["coeffs"]["LiCl"] - 16) < 1e-9,
        "host Li54P10S44Cl16 = 10 Li3PS4 + 4 Li2S + 16 LiCl (손검산)")
    # 압력 어림 — Q1 뒤돌아보기 (카드 §6 · CLAUDE.md 2026-10-23) 를 재현한다
    v1 = 1175.6618475785592
    cMP, cLi = volume_correction_eV(13.10, v1, 30.0), volume_correction_eV(3.37, v1, 30.0)
    chk(abs(cMP + 0.20987) < 5e-5 and abs(cLi + 0.013889) < 5e-6,
        f"ΔE_V = −P²V/2B 손계산 (MP_07 −0.20987 · MLi_04 −0.013889 eV) ← {cMP:.5f} · {cLi:.6f}")
    chk(abs((cMP - cLi) / 2 + 0.0980) < 5e-4,
        f"★ Q1 기록 재현: 압력 어림 보정 −0.098 eV/Nd (EOS −0.100) ← {(cMP - cLi) / 2:.4f}")
    chk(volume_correction_eV(-13.10, v1, 30.0) == cMP and volume_correction_eV(0.0, v1, 30.0) == 0.0,
        "부호와 무관하게 보정은 ≤ 0 (늘이든 줄이든 V₀ 쪽이 낮다) · P = 0 이면 0")
    # k 간격 — 카드 §1b (도핑 k 3 3 1 · host k 3 3 2 가 같은 간격)
    host_cell = [[6.068323323041438, 0.0, 3.5035497376181044],
                 [2.0227744410138127, 5.7212757002319385, 3.5035497376181044],
                 [0.0, 0.0, 35.035511390379995]]
    # 간격 규칙은 **상** 에만 쓴다 — host 는 카드가 k 3 3 2 로 박았다 (도핑 1×1×10 의 k 3 3 1 과
    #   접힘 등가 · 긴 축 2 × 5 = 10 · 간격 규칙만 쓰면 긴 축이 1 로 떨어져 더 성기다)
    chk(kmesh_from_spacing(host_cell, 0.37) == "3 3 1",
        f"host 셀 간격 0.37 → 3 3 1 (긴 축 |b| 0.22 < 0.37) ← {kmesh_from_spacing(host_cell, 0.37)}")
    chk(kmesh_from_spacing(host_cell, 0.11) == "10 10 2", "host 셀 간격 0.11 → 10 10 2 (긴 축 0.2196/0.11 → 2)")
    with tempfile.TemporaryDirectory() as td:
        td = _P(td)
        # load_basis — 양성 · 음성 둘
        good = {"phases": {"Li2S": {"formula": {"Li": 2, "S": 1}, "mp_id": "mp-1153"},
                           "LiCl": {"formula": {"Li": 1, "Cl": 1}, "mp_id": "mp-22905"},
                           "Li3PS4": {"formula": {"Li": 3, "P": 1, "S": 4}, "mp_id": "mp-985583"}},
                "per_target": {"B": ["Li2S", "LiCl", "Li3PS4"]}}
        (td / "b.json").write_text(json.dumps(good))
        bb, mm, pp = load_basis(td / "b.json")
        chk(set(bb) == {"Li2S", "LiCl", "Li3PS4"} and mm["Li2S"] == "mp-1153" and pp["B"][0] == "Li2S",
            "load_basis: 조성 · mp-id · per_target 를 읽는다")
        for bad, why in [({"phases": {"X": {"formula": {"Li": 1.5}}}}, "비정수 조성"),
                         ({"phases": good["phases"], "per_target": {"A": ["NdCl3"]}}, "기저 밖 상")]:
            (td / "x.json").write_text(json.dumps(bad))
            try:
                load_basis(td / "x.json"); ok_ = False
            except ValueError:
                ok_ = True
            chk(ok_, f"★ [음성] load_basis 가 {why} 를 거부한다")
        # 출력 파서 — 압력은 **마지막** 블록 · Pulay 는 끝 SCF 가 있을 때만
        #   ⛔ fixture 는 **QE 7.4.1 실제 꼴**이다 (2026-10-26 — 옛 fixture 는 6.x 문구 'A final scf …' 라서
        #     문구로 찾는 파서가 초록이었고, 실물 7.4.1 출력에서는 None 이 나와 게이트가 조용히 빠졌다)
        head = ("!    total energy              =    -100.00000000 Ry\n"
                "          total   stress  (Ry/bohr**3)                   (kbar)     P=        9.99\n"
                "!    total energy              =    -100.00100000 Ry\n"
                "     bfgs converged in   2 scf cycles and   1 bfgs steps\n"
                "Begin final coordinates\nEnd final coordinates\n\n")
        tail = ("!    total energy              =    -100.00110000 Ry\n"
                "          total   stress  (Ry/bohr**3)                   (kbar)     P=       -1.25\n")
        q74 = ("     Final scf calculation at the relaxed structure.\n"
               "     The G-vectors are recalculated for the final unit cell\n"
               "     Results may differ from those at the preceding step.\n")
        want_g = 0.0001 * 13.605693122994 * 1000 / 10
        (td / "v.out").write_text(head + q74 + tail)
        chk(parse_qe_pressure_kbar(td / "v.out") == -1.25, "압력은 마지막 stress 블록에서 (−1.25 kbar)")
        g = pulay_gap_meV_per_atom(td / "v.out", 10)
        chk(g is not None and abs(g - want_g) < 1e-9,
            f"[양성] QE 7.4.1 꼴 — Pulay 차 = |끝 SCF − 마지막 BFGS| / 원자 ← {g}")
        (td / "v6.out").write_text(head + "     A final scf calculation at the relaxed structure.\n" + tail)
        g6 = pulay_gap_meV_per_atom(td / "v6.out", 10)
        chk(g6 is not None and abs(g6 - want_g) < 1e-9, f"[양성] QE 6.x 문구도 같은 값 ← {g6}")
        (td / "s.out").write_text(head + q74)
        chk(pulay_gap_meV_per_atom(td / "s.out", 10) is None,
            "★ [음성] 'End final coordinates' 뒤에 '!' 가 없으면 (relax · 끝 SCF 없음) Pulay 차는 None — 0 으로 두지 않는다")
        (td / "n.out").write_text((head + q74 + tail).replace("     bfgs converged in   2 scf cycles and   1 bfgs steps\n",
                                                             "     The maximum number of steps has been reached.\n"))
        chk(pulay_gap_meV_per_atom(td / "n.out", 10) is None,
            "★ [음성] 'bfgs converged' 가 없으면 (nstep 소진) None — 안 끝난 vc-relax 를 쓰지 않는다")
        real = _P(__file__).resolve().parents[2] / "db/raw/nd_q2_decomp_2026_10_23/run_kgy/Li2S/scf.out"
        if real.is_file():
            chk(pulay_gap_meV_per_atom(real, 3) is not None,
                "★ [회귀] 실물 QE 7.4.1 vc-relax 출력 (Nd Q2 Li2S) 에서 끝 SCF 를 찾는다 — 옛 파서는 None 이었다")
        # --collect 끝까지 — 상 셋 + 타깃 둘 (A: 압력 작음 · B: 압력 큼)
        cd = td / "c"
        (cd / "in").mkdir(parents=True)

        def _qe_in(name, syms_pos, cell, calc="scf"):
            sp = "".join(f" {s} 1.0 {s.lower()}.upf\n" for s in sorted({s for s, _ in syms_pos}))
            ps = "".join(f" {s} {x} {y} {z}\n" for s, (x, y, z) in syms_pos)
            cl = "".join(f" {r[0]} {r[1]} {r[2]}\n" for r in cell)
            (cd / "in" / f"{name}.in").write_text(
                f"&CONTROL\n calculation='{calc}'\n/\n&SYSTEM\n ibrav=0\n nat={len(syms_pos)}\n"
                f" ntyp={len(sp.splitlines())}\n ecutwfc=60\n/\n&ELECTRONS\n/\n"
                f"ATOMIC_SPECIES\n{sp}CELL_PARAMETERS angstrom\n{cl}ATOMIC_POSITIONS angstrom\n{ps}K_POINTS gamma\n")

        def _qe_out(name, e_ry, p_kbar=None):
            s = f"!    total energy              =    {e_ry:.8f} Ry\n"
            if p_kbar is not None:
                s += f"          total   stress  (Ry/bohr**3)                   (kbar)     P=  {p_kbar:10.2f}\n"
            (cd / f"{name}.out").write_text(s)

        box = [[10.0, 0.0, 0.0], [0.0, 10.0, 0.0], [0.0, 0.0, 10.0]]
        _qe_in("Li2S", [("Li", (0, 0, 0)), ("Li", (1, 1, 1)), ("S", (2, 2, 2))], box)
        _qe_in("LiCl", [("Li", (0, 0, 0)), ("Cl", (2, 2, 2))], box)
        _qe_in("Li3PS4", [("Li", (0, 0, i)) for i in range(3)] + [("P", (3, 3, 3))]
               + [("S", (4, 4, i)) for i in range(4)], box)
        tA = [("Li", (0, 0, i)) for i in range(4)] + [("P", (3, 3, 3))] + [("S", (4, 4, i)) for i in range(5)]
        tA += [("Li", (5, 5, 5)), ("Li", (5, 5, 6)), ("Cl", (6, 6, 6))]   # Li6PS5Cl = Li3PS4 + Li2S + LiCl
        _qe_in("A", tA, box)
        _qe_in("B", tA, box)
        E = {"Li2S": -10.0, "LiCl": -8.0, "Li3PS4": -30.0}   # Ry/셀 (상 셀 = 화학식 하나)
        for n, e in E.items():
            _qe_out(n, e)
        _qe_out("A", -48.10, 3.0)     # 분해보다 0.10 Ry 낮다 · 0.3 GPa
        _qe_out("B", -48.10, 30.0)    # 같은 에너지 · 3 GPa → G_V 불통과
        (cd / "basis.json").write_text(json.dumps({"phases": {
            "Li2S": {"formula": {"Li": 2, "S": 1}}, "LiCl": {"formula": {"Li": 1, "Cl": 1}},
            "Li3PS4": {"formula": {"Li": 3, "P": 1, "S": 4}}}}))
        me = str(Path(__file__).resolve())
        rr = subprocess.run([sys.executable, me, "--collect", "--out", str(cd), "--basis", str(cd / "basis.json"),
                             "--bulk_modulus_GPa", "25", "--bulk_modulus_range", "21.7", "32.5",
                             "--pair", "A", "B"], capture_output=True, text=True)
        res = json.loads((cd / "decomp_result.json").read_text()) if (cd / "decomp_result.json").exists() else {}
        if not res:
            print("    (collect 출력 끝)\n" + rr.stdout[-900:] + rr.stderr[-200:])
            res = {"targets": {"A": {"delta_E_decomp_eV_per_atom": 9e9}}}
        pr = res.get("pair") or {}
        want_raw = 0.10 * 13.605693122994 / 13 * 1000          # meV/atom (13 원자)
        chk(rr.returncode == 0 and abs(res["targets"]["A"]["delta_E_decomp_eV_per_atom"] * 1000 - want_raw) < 1e-6,
            f"--collect --basis: ΔE_decomp(A) = 0.10 Ry / 13 원자 ← rc {rr.returncode}")
        chk(abs(pr.get("Y_raw_meV_per_atom", 9) - 0.0) < 1e-9, "Y (보정 전) = 0 (두 타깃 에너지 같음)")
        vA, vB = volume_correction_eV(3.0, 1000.0, 25.0), volume_correction_eV(30.0, 1000.0, 25.0)
        chk(abs(pr.get("Y_corrected_meV_per_atom", {}).get("25.0", 9) - (-(vA - vB) / 13 * 1000)) < 1e-6,
            "Y (보정) = −(ΔE_V,A − ΔE_V,B)/N — B 셀이 더 내려간 만큼 A 가 상대적으로 덜 안정")
        chk(pr.get("G_V_pass") is False and "G_V 불통과" in rr.stdout,
            "★ [음성] 3 GPa 셀이 끼면 G_V 불통과 — 보정값을 결과로 쓰지 않는다고 찍는다")
        chk("Li3PS4" in res.get("phase_pulay_meV_per_atom", {}) and res["phase_pulay_meV_per_atom"]["Li3PS4"] is None,
            "끝 SCF 없는 상 출력 → Pulay None (지어내지 않는다)")
        _qe_out("B", -48.10)          # 압력 줄 없음 → 보정 못 함 (0 으로 안 둔다)
        rr2 = subprocess.run([sys.executable, me, "--collect", "--out", str(cd), "--basis", str(cd / "basis.json"),
                              "--bulk_modulus_GPa", "25", "--pair", "A", "B"], capture_output=True, text=True)
        res2 = json.loads((cd / "decomp_result.json").read_text())
        chk(res2["targets"]["B"].get("volume_correction", "x") is None and "보정 못 함" in rr2.stdout
            and res2["pair"]["G_V_pass"] is None,
            "★ [음성] 압력 줄이 없으면 보정 None · G_V 판정 None (0 으로 두지 않는다)")
        _qe_out("B", -48.10, 30.0)
        _qe_in("Li3PS4", [("Li", (0, 0, i)) for i in range(3)] + [("P", (3, 3, 3))]
               + [("S", (4, 4, i)) for i in range(4)], box, calc="vc-relax")
        bf = ("!    total energy              =    -30.00000000 Ry\n"
              "     bfgs converged in   1 scf cycles and   0 bfgs steps\n"
              "Begin final coordinates\nEnd final coordinates\n\n" + q74)
        cmd = [sys.executable, me, "--collect", "--out", str(cd), "--basis", str(cd / "basis.json"),
               "--bulk_modulus_GPa", "25", "--pair", "A", "B"]
        (cd / "Li3PS4.out").write_text(bf)                           # 끝 SCF 없음
        r5 = subprocess.run(cmd, capture_output=True, text=True)
        chk(r5.returncode == 3 and "끝 SCF" in r5.stdout and "Li3PS4" in r5.stdout,
            f"★ [음성] vc-relax 상인데 끝 SCF 가 없으면 --collect 가 거부 (끝 3) ← rc {r5.returncode}")
        (cd / "Li3PS4.out").write_text(bf + "!    total energy              =    -30.00000100 Ry\n")
        r6 = subprocess.run(cmd, capture_output=True, text=True)
        res6 = json.loads((cd / "decomp_result.json").read_text())
        g6c = res6.get("phase_pulay_meV_per_atom", {}).get("Li3PS4")
        chk(r6.returncode == 0 and res6.get("G_phase_pass") is True and res6["pair"].get("G_phase_pass") is True
            and g6c is not None and abs(g6c - 1e-6 * 13.605693122994 * 1000 / 8) < 1e-9,
            f"vc-relax 상 · 끝 SCF 차 1e-6 Ry / 8 원자 → G_상_이완 통과 ← rc {r6.returncode} · {g6c}")
        (cd / "Li3PS4.out").write_text(bf + "!    total energy              =    -30.00100000 Ry\n")
        r7 = subprocess.run(cmd, capture_output=True, text=True)
        res7 = json.loads((cd / "decomp_result.json").read_text())
        chk(res7.get("G_phase_pass") is False and res7["pair"].get("G_phase_pass") is False
            and "G_상_이완 불통과" in r7.stdout,
            "★ [음성] 끝 SCF 차 1.7 meV/원자 (> 0.5) → G_상_이완 불통과 · Y 를 결과로 쓰지 않는다고 찍는다")
        # --prepare (MP 없이 --phase_structs) — pseudo_dir 이 이 기계에 없을 때 --pseudo_map 을 쓴다
        try:
            from ase.io import write as _w
            from ase import Atoms as _A
            sd = td / "ps"; sd.mkdir()
            _w(str(sd / "Li2S.cif"), _A("Li2S", positions=[[0, 0, 0], [1.4, 1.4, 1.4], [2.8, 2.8, 0]],
                                        cell=[[0, 2.85, 2.85], [2.85, 0, 2.85], [2.85, 2.85, 0]], pbc=True))
            _w(str(sd / "LiCl.cif"), _A("LiCl", positions=[[0, 0, 0], [2.57, 0, 0]],
                                        cell=[[0, 2.57, 2.57], [2.57, 0, 2.57], [2.57, 2.57, 0]], pbc=True))
            (td / "b2.json").write_text(json.dumps({"phases": {
                "Li2S": {"formula": {"Li": 2, "S": 1}}, "LiCl": {"formula": {"Li": 1, "Cl": 1}}}}))
            _w(str(td / "host.xyz"), _A("Li3SCl", positions=[[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]],
                                        cell=[8, 8, 8], pbc=True), format="extxyz")
            base = [sys.executable, me, "--prepare", "--basis", str(td / "b2.json"), "--phase_structs", str(sd),
                    "--targets", str(td / "host.xyz"), "--pseudo_dir", "/nonexistent/pseudo",
                    "--calculation", "relax", "--calculation_phase", "vc-relax", "--kspacing_phase", "0.25",
                    "--ecutwfc", "70", "--ecutrho", "560", "--conv_thr", "1.0d-9", "--mixing_beta", "0.3"]
            r3 = subprocess.run(base + ["--out", str(td / "p1"), "--pseudo_map", "Li=Li.paw.UPF,S=S.paw.UPF"],
                                capture_output=True, text=True)
            chk(r3.returncode == 3 and not (td / "p1" / "in").exists(),
                "★ [음성] pseudo_dir 이 없는 기계에서 --pseudo_map 에 Cl 이 빠지면 **입력을 안 쓴다** (끝 3)")
            r4 = subprocess.run(base + ["--out", str(td / "p2"),
                                        "--pseudo_map", "Li=Li.paw.UPF,S=S.paw.UPF,Cl=Cl.paw.UPF"],
                                capture_output=True, text=True)
            li2s = (td / "p2" / "in" / "Li2S.in").read_text() if (td / "p2" / "in" / "Li2S.in").exists() else ""
            hst = (td / "p2" / "in" / "host.in").read_text() if (td / "p2" / "in" / "host.in").exists() else ""
            chk(r4.returncode == 0 and "Li.paw.UPF" in li2s and "li_pbe" not in li2s
                and "calculation = 'vc-relax'" in li2s and "calculation = 'relax'" in hst
                and "conv_thr     = 1.0d-9" in li2s and "mixing_beta  = 0.3" in li2s,
                f"--prepare: --pseudo_map 이름 · 상 vc-relax · 타깃 relax · 설정을 그대로 쓴다 ← rc {r4.returncode}")
            kl = [ln for ln in li2s.splitlines() if ln.strip() and ln.strip()[0].isdigit()][-1].split()[:3] if li2s else []
            chk(kl == kmesh_from_spacing([[0, 2.85, 2.85], [2.85, 0, 2.85], [2.85, 2.85, 0]], 0.25).split(),
                f"상 k 를 간격 0.25 로 셈한다 ← {kl}")
        except ImportError:
            chk(False, "ase 가 없어 --prepare 시험을 못 했다")
        # --kprobe · --kprobe_read (2026-10-26 · 카드 §4 G_k) — 합성 본 런 (상 vc-relax 하나 + 타깃 relax 하나)
        kr = td / "kr"
        settings = ("&SYSTEM\n    ibrav       = 0\n    nat         = {nat}\n    ntyp        = {nt}\n"
                    "    ecutwfc     = 70.0\n    ecutrho     = 560.0\n    occupations = 'smearing'\n"
                    "    smearing    = 'mv'\n    degauss     = 0.01\n    nosym       = .true.\n/\n"
                    "&ELECTRONS\n    conv_thr     = 1.0d-9\n    mixing_beta  = 0.3\n/\n")
        (kr / "Li2S").mkdir(parents=True)
        (kr / "Li2S" / "scf.in").write_text(
            "&CONTROL\n    calculation = 'vc-relax'\n    prefix      = 'Li2S'\n/\n" + settings.format(nat=3, nt=2)
            + "&IONS\n    ion_dynamics = 'bfgs'\n/\n&CELL\n    cell_dynamics = 'bfgs'\n    press_conv_thr = 0.5\n/\n"
            "ATOMIC_SPECIES\n  Li  6.9410  Li.paw.UPF\n  S  32.0650  S.paw.UPF\n"
            "CELL_PARAMETERS angstrom\n    4.0456138700    0.0000000000    0.0000000000\n"
            "    2.0228069350    3.5036043853    0.0000000000\n    2.0228069350    1.1678681284    3.3032298926\n"
            "ATOMIC_POSITIONS crystal\n  Li    0.75 0.75 0.75\n  Li    0.25 0.25 0.25\n  S    0.0 0.0 0.0\n"
            "K_POINTS automatic\n  8 8 8 0 0 0\n")
        li2s_out = ("     number of atoms/cell      =            3\n"
                    "!    total energy              =     -96.68000570 Ry\n"
                    "     bfgs converged in   5 scf cycles and   4 bfgs steps\n"
                    "Begin final coordinates\n     new unit-cell volume =    313.02505 a.u.^3 (    46.38553 Ang^3 )\n\n"
                    "CELL_PARAMETERS (angstrom)\n   4.033039692  -0.000000050  -0.000000041\n"
                    "   2.016519802   3.492714829  -0.000000019\n   2.016519798   1.164238261   3.292963074\n\n"
                    "ATOMIC_POSITIONS (crystal)\nLi               0.7500000043        0.7499999487        0.7500000262\n"
                    "Li               0.2500000223        0.2500000469        0.2499999832\n"
                    "S               -0.0000000266        0.0000000043       -0.0000000094\nEnd final coordinates\n\n")
        (kr / "Li2S" / "scf.out").write_text(li2s_out + q74 + "!    total energy              =     -96.67999740 Ry\n")
        (kr / "host").mkdir()
        (kr / "host" / "scf.in").write_text(
            "&CONTROL\n    calculation = 'relax'\n    prefix      = 'host'\n/\n" + settings.format(nat=2, nt=2)
            + "&IONS\n    ion_dynamics = 'bfgs'\n/\n"
            "ATOMIC_SPECIES\n  Li  6.9410  Li.paw.UPF\n  S  32.0650  S.paw.UPF\n"
            "CELL_PARAMETERS angstrom\n    6.0 0.0 0.0\n    0.0 6.0 0.0\n    0.0 0.0 6.0\n"
            "ATOMIC_POSITIONS crystal\n  Li    0.1 0.1 0.1\n  S    0.5 0.5 0.5\n"
            "K_POINTS automatic\n  3 3 2 0 0 0\n")
        (kr / "host" / "scf.out").write_text(
            "     number of atoms/cell      =            2\n!    total energy              =     -50.00000000 Ry\n"
            "     bfgs converged in   3 scf cycles and   2 bfgs steps\nBegin final coordinates\n\n"
            "ATOMIC_POSITIONS (crystal)\nLi               0.1100000000        0.1000000000        0.1000000000\n"
            "S                0.5000000000        0.5000000000        0.5000000000\nEnd final coordinates\n")
        (kr / "b.json").write_text(json.dumps({"phases": {"Li2S": {"formula": {"Li": 2, "S": 1}}}}))
        kcmd = [sys.executable, me, "--kprobe", "--runs", str(kr), "--basis", str(kr / "b.json"),
                "--kspacing_phase", "0.18", "--kpoints", "4 4 2", "--phase_symmetry"]
        r8 = subprocess.run(kcmd + ["--out", str(td / "kp")], capture_output=True, text=True)
        pin = (td / "kp" / "phase" / "Li2S" / "scf.in")
        tin = (td / "kp" / "target" / "host" / "scf.in")
        ptx = pin.read_text() if pin.is_file() else ""
        ttx = tin.read_text() if tin.is_file() else ""
        from ase.io import read as _rd
        want_k = kmesh_from_spacing([[4.033039692, -5e-8, -4.1e-8], [2.016519802, 3.492714829, -1.9e-8],
                                     [2.016519798, 1.164238261, 3.292963074]], 0.18)
        chk(r8.returncode == 0 and "calculation = 'scf'" in ptx and "&IONS" not in ptx and "&CELL" not in ptx
            and "nosym       = .false." in ptx and f"  {want_k} 0 0 0" in ptx and "4.033039692" in ptx
            and "0.7500000043" in ptx and _setting_lines(ptx) == _setting_lines((kr / "Li2S" / "scf.in").read_text()),
            f"--kprobe 상: scf · &IONS/&CELL 뺌 · 대칭 켬 · 최종 셀 + 좌표 · k {want_k} (간격 0.18 · 덮어쓴 셀) · 설정 같음 ← rc {r8.returncode}")
        chk(r8.returncode == 0 and "calculation = 'scf'" in ttx and "&IONS" not in ttx and "nosym       = .true." in ttx
            and "  4 4 2 0 0 0" in ttx and "0.1100000000" in ttx and "    6.0 0.0 0.0" in ttx,
            "--kprobe 타깃: scf · nosym 그대로 · 좌표만 (셀 그대로) · k 4 4 2")
        chk((td / "kp" / "phase" / "SHA256SUMS").is_file() and (td / "kp" / "target" / "MANIFEST.json").is_file(),
            "--kprobe: 폴더마다 SHA256SUMS · MANIFEST.json")
        (kr / "Li2S" / "scf.out").write_text(li2s_out + q74)                # 끝 SCF 없음
        r9 = subprocess.run(kcmd + ["--out", str(td / "kp2")], capture_output=True, text=True)
        chk(r9.returncode == 3 and not (td / "kp2" / "phase").exists() and not (td / "kp2" / "target").exists(),
            f"★ [음성] vc-relax 끝 SCF 가 없으면 탐침 입력을 하나도 안 쓴다 (끝 3) ← rc {r9.returncode}")
        (kr / "Li2S" / "scf.out").write_text(li2s_out + q74 + "!    total energy              =     -96.67999740 Ry\n")
        (td / "kp" / "phase" / "Li2S").mkdir(parents=True, exist_ok=True)       # 앞 시험이 실패해도 여기서 죽지 않게
        (td / "kp" / "target" / "host").mkdir(parents=True, exist_ok=True)
        (td / "kp" / "phase" / "Li2S" / "scf.out").write_text("!    total energy              =     -96.68044000 Ry\n")
        rcmd = [sys.executable, me, "--kprobe_read", "--runs", str(kr), "--basis", str(kr / "b.json"),
                "--probe", str(td / "kp"), "--out", str(td / "kd")]
        r10 = subprocess.run(rcmd, capture_output=True, text=True)
        chk(r10.returncode == 3 and not (td / "kd" / "kprobe_decision.json").exists() and "host" in r10.stdout,
            f"★ [음성] 탐침 출력이 하나라도 없으면 판정 파일을 안 쓴다 (끝 3) ← rc {r10.returncode}")
        (td / "kp" / "target" / "host" / "scf.out").write_text("!    total energy              =     -50.00005000 Ry\n")
        r11 = subprocess.run(rcmd, capture_output=True, text=True)
        kd = json.loads((td / "kd" / "kprobe_decision.json").read_text()) if (td / "kd" / "kprobe_decision.json").is_file() else {"jobs": {}}
        dl = kd["jobs"].get("Li2S", {}).get("dE_probe_minus_main_meV_per_atom", 9e9)
        dh = kd["jobs"].get("host", {}).get("dE_probe_minus_main_meV_per_atom", 9e9)
        chk(r11.returncode == 0 and abs(dl - (-96.68044 + 96.6799974) * 13.605693122994 * 1000 / 3) < 1e-6
            and kd["jobs"]["Li2S"]["decision"] == "탐침 값을 쓴다" and kd["jobs"]["Li2S"]["over_threshold"] is True,
            f"--kprobe_read 상: ΔE = (끝 SCF 대 탐침) / 원자 {dl:+.3f} meV > 1 → '탐침 값을 쓴다'")
        chk(abs(dh - (-0.00005) * 13.605693122994 * 1000 / 2) < 1e-6 and kd["jobs"]["host"]["over_threshold"] is False
            and kd["jobs"]["host"]["decision"].startswith("본 값"),
            f"--kprobe_read 타깃: ΔE {dh:+.3f} meV ≤ 1 → 본 값 (k 한계 없음)")
        # k 는 **덮어쓴 셀**로 센다 — 이완 전 셀이면 11 11 11 · 0.9 배로 줄어든 셀이면 12 12 12 (위 fixture 는 둘이 같아 못 가른다)
        sh = li2s_out.replace("   4.033039692  -0.000000050  -0.000000041\n   2.016519802   3.492714829  -0.000000019\n"
                              "   2.016519798   1.164238261   3.292963074\n",
                              "   3.641052483   0.000000000   0.000000000\n   1.820526242   3.153243947   0.000000000\n"
                              "   1.820526242   1.051081316   2.972906903\n")
        (kr / "Li2S" / "scf.out").write_text(sh + q74 + "!    total energy              =     -96.67999740 Ry\n")
        r13 = subprocess.run(kcmd + ["--out", str(td / "kp3")], capture_output=True, text=True)
        p3 = (td / "kp3" / "phase" / "Li2S" / "scf.in")
        chk(r13.returncode == 0 and p3.is_file() and "  12 12 12 0 0 0" in p3.read_text(),
            "★ [음성] k 를 이완 전 셀 (11 11 11) 이 아니라 덮어쓴 셀 (0.9 배 → 12 12 12) 로 센다")
        (kr / "Li2S" / "scf.out").write_text(li2s_out + q74 + "!    total energy              =     -96.67999740 Ry\n")
        # 설정 줄 가드 — &IONS 의 '/' 가 같은 줄에 있으면 정리 정규식이 &ELECTRONS 까지 먹는다 → 거부해야 한다
        bad_in = (kr / "Li2S" / "scf.in").read_text().replace("&IONS\n    ion_dynamics = 'bfgs'\n/\n&CELL",
                                                               "&CELL").replace(
            "&ELECTRONS\n", "&IONS\n    ion_dynamics = 'bfgs' /\n&ELECTRONS\n")
        (kr / "Li2S" / "scf.in.good").write_text((kr / "Li2S" / "scf.in").read_text())
        (kr / "Li2S" / "scf.in").write_text(bad_in)
        r14 = subprocess.run(kcmd + ["--out", str(td / "kp4")], capture_output=True, text=True)
        chk(r14.returncode == 3 and not (td / "kp4" / "phase").exists() and "설정 줄" in r14.stdout,
            f"★ [음성] 정리 정규식이 설정 줄 (conv_thr · mixing_beta) 을 먹으면 거부 · 아무것도 안 남긴다 ← rc {r14.returncode}")
        (kr / "Li2S" / "scf.in").write_text((kr / "Li2S" / "scf.in.good").read_text())
        real = _P(__file__).resolve().parents[2] / "db/raw/nd_q2_decomp_2026_10_23/run_kgy"
        rb = _P(__file__).resolve().parents[2] / "db/inputs/nd_q2_decomp_2026_10_23/basis.json"
        if real.is_dir() and rb.is_file():
            r12 = subprocess.run([sys.executable, me, "--kprobe", "--runs", str(real), "--basis", str(rb),
                                  "--kspacing_phase", "0.18", "--kpoints", "4 4 2", "--phase_symmetry",
                                  "--out", str(td / "kreal")], capture_output=True, text=True)
            n_in = len(list((td / "kreal").glob("*/*/scf.in")))
            chk(r12.returncode == 0 and n_in == 6, f"[회귀] 실물 Nd Q2 본 런 → 탐침 입력 6 (상 5 · 타깃 1) ← rc {r12.returncode} · {n_in}")

    print(f"selftest {'PASS' if not n_bad else 'FAIL'} — {n_ok} ok, {n_bad} bad")
    return 1 if n_bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--prepare", action="store_true",
                    help="MP 에서 기저 상 구조를 받아 QE relax 입력을 쓴다 "
                         "(--targets 의 구조 입력도 같이). MP_API_KEY 필요")
    ap.add_argument("--collect", action="store_true",
                    help="QE 출력을 읽어 ΔE_decomp 를 계산하고 두 구조를 비교")
    ap.add_argument("--targets", nargs="+", help="비교할 구조 파일 (cif/xyz)")
    ap.add_argument("--struct_dir",
                    help="--collect 이 타깃 구조(cif)를 찾을 폴더. 보통 필요 없다 — "
                         "기본은 우리가 만든 QE 입력 <out>/in/<타깃>.in 에서 조성을 읽는다.")
    ap.add_argument("--out", help="작업 디렉터리")
    ap.add_argument("--ecutwfc", type=float, default=60)
    ap.add_argument("--ecutrho", type=float, default=480)
    ap.add_argument("--kpoints", default="2 2 1")
    ap.add_argument("--pseudo_dir",
                    help="pw.x pseudo_dir. **머신마다 다르다** — gabia "
                         "/data/work/pseudo · KISTI /scratch/x3430a02/kgy/"
                         "manuscript_support/pseudo. 안 주면 KISTI 기본값이고, "
                         "다른 머신에서는 pw.x 가 조용히 죽는다.")
    ap.add_argument("--calculation", default="scf", choices=["scf", "relax"],
                    help="★ 기본 **scf**. 두 타깃은 이미 **같은 UMA 로** 이완돼 있어 "
                         "기하 편향이 비교 가능한 상태다. CPU QE 로 100원자 BFGS 를 "
                         "돌리면 며칠 걸리므로 **먼저 scf 로 부호를 보고**, 필요하면 "
                         "그때 relax 로 다시 돈다. "
                         "⛔ scf 결과는 '기하를 UMA 가 정한 상태에서의 DFT 에너지' 다 — "
                         "부호가 UMA 와 갈리면 relax 없이 결론 내지 말 것.")
    ap.add_argument("--phase_symmetry", action="store_true",
                    help="기저 상은 이상적 결정이라 대칭을 켜면 훨씬 싸다 (nosym=.false.). "
                         "타깃은 무질서라 항상 nosym=.true. 로 둔다.")
    ap.add_argument("--pseudo_map",
                    help="원소=파일명 쉼표 목록 (예 'Li=li_x.UPF,S=s_y.UPF'). "
                         "자동 탐색이 후보를 여럿 찾아 거부할 때 사람이 정한다.")
    ap.add_argument("--allow_offhull_basis", action="store_true",
                    help="기저 상이 MP hull 위가 아니어도 진행 (기본은 거부). "
                         "고에너지 다형체를 기저로 쓰면 비교 전체가 그만큼 밀린다.")
    ap.add_argument("--kpoints_phase", default="4 4 4",
                    help="기저 상은 작아서 k 를 더 촘촘히 (기본 4 4 4)")
    # ── 2026-10-23 확장 (Nd Q2) ────────────────────────────────────────────
    ap.add_argument("--basis", help="기저 파일 (json · phases · per_target) — 없으면 Y 5 상")
    ap.add_argument("--phase_structs", help="상 구조 폴더 (<상>.cif) — 주면 MP 를 안 부른다")
    ap.add_argument("--save_phase_structs", help="MP 에서 받은 상 구조를 <폴더>/<상>.cif 로 남긴다")
    ap.add_argument("--kspacing_phase", type=float,
                    help="상 k 간격 (Å⁻¹ · 2π 포함) — 주면 --kpoints_phase 대신 상마다 셈")
    ap.add_argument("--calculation_phase", choices=["scf", "relax", "vc-relax"],
                    help="상 계산 (안 주면 --calculation 과 같다)")
    ap.add_argument("--smearing", default="mv")
    ap.add_argument("--degauss", type=float, default=0.01)
    ap.add_argument("--conv_thr", default="1.0d-8")
    ap.add_argument("--mixing_beta", type=float, default=0.2)
    ap.add_argument("--bulk_modulus_GPa", type=float,
                    help="--collect: 압력 어림 ΔE_V = −P²V/(2B) 의 중심 B (GPa) — 주면 보정한다")
    ap.add_argument("--bulk_modulus_range", type=float, nargs=2, metavar=("BMIN", "BMAX"),
                    help="--collect: 보정 폭을 볼 B 범위 (GPa)")
    ap.add_argument("--pair", nargs=2, metavar=("A", "B"),
                    help="--collect: Y = ΔE_decomp(A) − ΔE_decomp(B) (meV/atom) 와 G_V · 분해능")
    ap.add_argument("--resolution_meV", type=float, default=2.0,
                    help="--collect --pair: |Y| 가 이 안이면 '구분 못 함' (카드 §4 분해능)")
    ap.add_argument("--kprobe", action="store_true",
                    help="본 런 (--runs) 의 이완 끝 기하로 k 탐침 scf 입력을 --out 에 쓴다 (카드 §4 G_k)")
    ap.add_argument("--kprobe_read", action="store_true",
                    help="본 런 (--runs) 과 탐침 (--probe) 의 원자당 에너지 차로 G_k 를 판정한다 (Y 는 안 셈)")
    ap.add_argument("--runs", help="--kprobe · --kprobe_read: 본 런 폴더 (<잡>/scf.in · scf.out)")
    ap.add_argument("--probe", help="--kprobe_read: 탐침 폴더 (--kprobe 가 쓴 phase/ · target/ 아래 <잡>/scf.out)")
    a = ap.parse_args()

    if a.selftest:
        return _selftest()
    if not a.out:
        print("⛔ --out 이 필요하다")
        return 2
    out = Path(a.out)
    if a.basis:
        try:
            basis, mpids, per_target = load_basis(a.basis)
        except (ValueError, OSError, json.JSONDecodeError) as e:
            print(f"⛔ --basis 를 못 읽었다 — {e}")
            return 2
    else:
        basis, mpids, per_target = DEFAULT_BASIS, BASIS_MPID, {}

    if a.prepare:
        import os
        from ase.io import read
        from generate_dft_inputs import generate_pwin
        key = os.environ.get("MP_API_KEY")
        if not key and not a.phase_structs:
            print("⛔ MP_API_KEY 가 없다 (기저 상 구조를 받아야 한다 — 아니면 --phase_structs)")
            return 2
        if not a.targets:
            print("⛔ --targets 가 필요하다")
            return 2
        from generate_dft_inputs import PSEUDOS, PSEUDO_DIR_KISTI
        offhull, need_pp, pending, mp_used = [], set(), [], {}
        calc_phase = a.calculation_phase or a.calculation

        def _phase_k(at):
            return kmesh_from_spacing(at.cell, a.kspacing_phase) if a.kspacing_phase else a.kpoints_phase
        pdir = Path(a.pseudo_dir or PSEUDO_DIR_KISTI)
        print(f"pseudo_dir = {pdir}"
              + ("" if a.pseudo_dir else "   ⚠ 기본값(KISTI) — 다른 머신이면 --pseudo_dir 를 줄 것"))
        pp_names = dict(x.split("=", 1) for x in (a.pseudo_map or "").split(",") if x)
        if pp_names:
            print(f"  · 수동 지정 {pp_names}")
        if a.phase_structs:
            # MP 를 부르지 않는다 — 폴더의 <상>.cif 를 그대로 쓴다 (키 없는 기계에서 입력을 쓸 때)
            for name in basis:
                f = Path(a.phase_structs) / f"{name}.cif"
                if not f.is_file():
                    print(f"  ⛔ {name}: {f} 가 없다")
                    offhull.append(name)
                    continue
                at = read(str(f))
                pending.append((name, at, _phase_k(at), not a.phase_symmetry))
                mp_used[name] = {"mp_id": mpids.get(name), "n_atoms": len(at), "from": str(f)}
                need_pp.update(at.get_chemical_symbols())
                print(f"  ✓ {name:<8} {mpids.get(name)}  {len(at)} atoms  (← {f.name} · k {_phase_k(at)})")
        else:
          from mp_api.client import MPRester
          from pymatgen.io.ase import AseAtomsAdaptor
          ad = AseAtomsAdaptor()
          with MPRester(key) as mpr:
            for name in basis:
                mpid = mpids.get(name)
                kw = ({"material_ids": [mpid]} if mpid else {"formula": name})
                docs = mpr.materials.summary.search(
                    fields=["material_id", "structure", "energy_above_hull"], **kw)
                if mpid and not docs:
                    print(f"  ⛔ {name}: 지정한 {mpid} 를 못 찾았다")
                    offhull.append(name)
                    continue
                if not docs:
                    print(f"  ⛔ {name}: MP 에서 못 찾았다")
                    continue
                d = min(docs, key=lambda x: x.energy_above_hull)
                # 그 조성에서 **MP 가 가진 것 중 최저**를 골랐다는 것이 요점이다.
                #   e_hull 절대값은 MP 보정 기준이라 우리 비교에 안 들어간다(위 주석).
                if d.energy_above_hull > OFFHULL_WARN:
                    print(f"  {'⚠' if a.allow_offhull_basis else '⛔'} {name:<8} "
                          f"{d.material_id}  MP e_hull {d.energy_above_hull:.4f} "
                          f"eV/atom > {OFFHULL_WARN} — **다른 다형체를 집었을 수 있다** "
                          f"(검색 {len(docs)}건 중 최저)")
                    if not a.allow_offhull_basis:
                        offhull.append(name)
                        continue
                at = ad.get_atoms(d.structure)
                pending.append((name, at, _phase_k(at),
                                not a.phase_symmetry))
                mp_used[name] = {"mp_id": d.material_id, "n_atoms": len(at),
                                 "mp_e_above_hull": float(d.energy_above_hull)}
                if a.save_phase_structs:
                    sd = Path(a.save_phase_structs)
                    sd.mkdir(parents=True, exist_ok=True)
                    d.structure.to(filename=str(sd / f"{name}.cif"))
                    mp_used[name]["saved_cif"] = str(sd / f"{name}.cif")
                need_pp.update(at.get_chemical_symbols())
                print(f"  ✓ {name:<8} {d.material_id}  {len(at)} atoms  "
                      f"(MP e_hull {d.energy_above_hull:.4f})")
        for tf in a.targets:
            at = read(tf)
            stem = Path(tf).stem
            pending.append((stem, at, a.kpoints, True))   # 타깃은 항상 nosym
            need_pp.update(at.get_chemical_symbols())
            print(f"  ✓ {stem:<8} {len(at)} atoms  (target)")

        # ★ pseudo 를 **입력을 쓰기 전에** 전부 해결한다.
        #   반쯤 쓰고 실패하면 '입력이 있으니 돌리면 되겠지' 로 돌렸다가 런타임에 죽는다.
        resolved, unresolved = {}, {}
        if pdir.is_dir():
            for e in sorted(need_pp):
                nm, why = find_pseudo(e, pdir,
                                      prefer=pp_names.get(e) or
                                      (PSEUDOS[e][1] if e in PSEUDOS else None))
                if nm:
                    resolved[e] = nm
                else:
                    unresolved[e] = why
        else:
            # ⛔ 2026-10-23 — 이 기계에 pseudo_dir 이 없을 때 예전엔 --pseudo_map 을 무시하고
            #   PSEUDOS 기본 이름을 조용히 썼다 (Nd 기본값 = 4f 원자가 atompaw — frozen-4f 계산이
            #   다른 PP 로 바뀐다). 이제 --pseudo_map 을 쓰고, 빠진 원소가 있으면 거부한다.
            miss = [e for e in sorted(need_pp) if e not in pp_names]
            if pp_names and not miss:
                resolved = {e: pp_names[e] for e in sorted(need_pp)}
            elif pp_names:
                unresolved = {e: "--pseudo_map 에 없다 (이 기계에 pseudo_dir 이 없어 파일로 못 찾는다)"
                              for e in miss}
            else:
                resolved = {e: PSEUDOS[e][1] for e in sorted(need_pp) if e in PSEUDOS}
                print(f"  ⚠ pseudo_dir 이 이 기계에 없고 --pseudo_map 도 없다 — 기본 이름을 쓴다: {resolved}")

        if unresolved:
            print(f"\n  ⛔ pseudo 를 못 정한 원소 {len(unresolved)}개 — "
                  f"**입력을 하나도 쓰지 않았다**:")
            for e, why in unresolved.items():
                print(f"      {e:<3} {why}")
            print(f"     → --pseudo_map 'Li=…,S=…' 로 지정하거나 파일을 넣을 것")
            return 3
        (out / "in").mkdir(parents=True, exist_ok=True)
        for name, at, kp, nosym in pending:
            txt = generate_pwin(at, name, a.ecutwfc, a.ecutrho, kp,
                                pseudo_dir=str(pdir), pp_names=resolved,
                                calculation=(calc_phase if name in basis else a.calculation),
                                nosym=nosym, conv_thr=a.conv_thr, mixing_beta=a.mixing_beta,
                                smearing=a.smearing, degauss=a.degauss)
            # 쓴 입력의 PP 이름이 정한 것과 같은지 (generate_pwin 의 기본값으로 새지 않았는지)
            sp = re.search(r"ATOMIC_SPECIES\n(.*?)\nCELL_PARAMETERS", txt, re.S).group(1).split("\n")
            got = {ln.split()[0]: ln.split()[2] for ln in sp if ln.strip()}
            if any(got.get(e) != resolved.get(e) for e in got):
                print(f"  ⛔ {name}: 입력의 PP {got} 가 정한 것 {resolved} 와 다르다 — 쓰지 않았다")
                return 3
            (out / "in" / f"{name}.in").write_text(txt)

        if pdir.is_dir():
            print(f"\n  ▸ pseudo 해결 ({len(resolved)}종)")
            for e in sorted(resolved):
                print(f"      {e:<3} {resolved[e]}")
        else:
            print(f"\n  ⚠ pseudo_dir 이 이 머신에 없다({pdir}) — 계산 머신에서 확인할 것")

        if offhull:
            print(f"\n  ⛔ **기저 상 {len(offhull)}개를 건너뛰었다** (hull 위가 아님): {offhull}")
            print(f"     이대로면 --collect 가 '상 에너지가 없다' 로 거부한다. "
                  f"MP 검색을 고치거나 --allow_offhull_basis 로 진행할 것.")
            return 3
        (out / "prepare_provenance.json").write_text(json.dumps({
            "date_note": "생성 시각은 git 커밋으로 추적",
            "pseudo_dir": str(pdir), "pseudos_used": resolved,
            "⚠_pseudo_note": "머신마다 파일명 구두점이 다르고 판(USPP/PAW)도 다를 수 있다. "
                             "gabia SSSP 는 Y 가 USPP(Y_pbe_v1.uspp.F.UPF)이고 우리 "
                             "PSEUDOS 목록의 PAW 와 다르다 — **모든 계산에 같은 것을 쓰므로 "
                             "내부 일관성은 유지되나, 다른 머신 결과와 섞으면 안 된다.**",
            "calculation": a.calculation,
            "⛔_calculation_note": (
                "scf 면 기하는 **UMA 가 정한 것**이다. 두 타깃이 같은 UMA 로 이완됐으므로 "
                "기하 편향이 비교 가능하지만, Y 가 P 자리(빡빡한 사면체)와 Li 자리(느슨한 케이지)에서 "
                "UMA 오차가 다를 수 있다 — **부호가 UMA 와 갈리면 relax 로 다시 확인**해야 한다."
                if a.calculation == "scf" else
                "relax — DFT 가 기하까지 정한다. 수렴 여부를 출력에서 확인할 것."),
            "ecutwfc": a.ecutwfc, "ecutrho": a.ecutrho,
            "kpoints_target": a.kpoints, "kpoints_phase": a.kpoints_phase,
            "basis": basis, "basis_mp": mp_used, "per_target": per_target,
            "basis_file": a.basis, "basis_file_sha256": (
                __import__("hashlib").sha256(Path(a.basis).read_bytes()).hexdigest() if a.basis else None),
            "calculation_phase": calc_phase, "kspacing_phase": a.kspacing_phase,
            "phase_kpoints": {n: k for n, _, k, _ in pending if n in basis},
            "smearing": a.smearing, "degauss": a.degauss, "conv_thr": a.conv_thr,
            "mixing_beta": a.mixing_beta,
            "targets": [str(x) for x in a.targets],
            "⛔_do_not": "E_above_hull 로 인용 금지. 5상 공통기저 안의 상대 비교다.",
        }, indent=2, ensure_ascii=False))
        print(f"\n✓ 입력 → {out/'in'}   (기저 {len(basis)} + 타깃 {len(a.targets)})")
        print(f"✓ 설정 기록 → {out/'prepare_provenance.json'}")
        return 0

    if a.kprobe or a.kprobe_read:
        import hashlib
        runs = Path(a.runs or "")
        jobs = sorted(d.name for d in runs.iterdir() if (d / "scf.in").is_file()) if runs.is_dir() else []
        if not jobs:
            print(f"⛔ --runs {a.runs}: <잡>/scf.in 이 하나도 없다")
            return 2
        if a.kprobe:
            if not a.kspacing_phase:
                print("⛔ --kprobe 는 --kspacing_phase 가 필요하다 (상 k 간격)")
                return 2
            rows, bad = {}, []
            for j in jobs:
                ok_, why = relax_done(runs / j / "scf.out")
                is_ph = j in basis
                vc = qe_calculation(runs / j / "scf.in") == "vc-relax"
                if ok_ and vc and pulay_gap_meV_per_atom(runs / j / "scf.out", 1) is None:
                    ok_, why = False, "vc-relax 끝 SCF 없음"
                if not ok_:
                    bad.append((j, why))
                    continue
                grp = "phase" if is_ph else "target"
                info, why = make_kprobe_input(
                    runs / j / "scf.in", runs / j / "scf.out", out / grp / j / "scf.in",
                    None if is_ph else a.kpoints, a.kspacing_phase if is_ph else None,
                    (False if a.phase_symmetry else None) if is_ph else None, cell_too=vc)
                if info is None:
                    bad.append((j, why))
                    continue
                info.update({"group": grp, "main_in_sha256": hashlib.sha256((runs / j / "scf.in").read_bytes()).hexdigest(),
                             "main_out_sha256": hashlib.sha256((runs / j / "scf.out").read_bytes()).hexdigest()})
                rows[j] = info
                print(f"  ✓ {j:<8} {grp:<6} k {' '.join(info['k_main'] or ['?'])} → {' '.join(info['k_probe'])} · "
                      f"nosym {info['nosym']} · {'셀 + 좌표' if vc else '좌표만'}")
            if bad:
                print(f"⛔ 탐침 입력을 못 쓴 잡 {len(bad)} — 하나도 남기지 않는다:")
                for j, why in bad:
                    print(f"      {j:<8} {why}")
                import shutil
                for grp in ("phase", "target"):
                    shutil.rmtree(out / grp, ignore_errors=True)
                return 3
            for grp in ("phase", "target"):
                gd = out / grp
                if not gd.is_dir():
                    continue
                ins = sorted(gd.glob("*/scf.in"))
                (gd / "SHA256SUMS").write_text("".join(
                    f"{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(gd)}\n" for f in ins))
                (gd / "MANIFEST.json").write_text(json.dumps(
                    {"kind": "kprobe_inputs", "card_gate": "G_k_탐침", "group": grp,
                     "kspacing_phase": a.kspacing_phase if grp == "phase" else None,
                     "kpoints_target": a.kpoints if grp == "target" else None,
                     "jobs": {j: r for j, r in rows.items() if r["group"] == grp}},
                    indent=1, ensure_ascii=False) + "\n")
            print(f"✓ 탐침 입력 {len(rows)} → {out}/phase · {out}/target (폴더마다 SHA256SUMS · MANIFEST.json)")
            return 0
        # --kprobe_read
        pr = Path(a.probe or "")
        res, bad = {}, []
        for j in jobs:
            grp = "phase" if j in basis else "target"
            po = pr / grp / j / "scf.out"
            pi = pr / grp / j / "scf.in"
            e0, e1 = parse_qe_total(runs / j / "scf.out"), parse_qe_total(po)
            if e1 is None or not pi.is_file():
                bad.append((j, f"탐침 출력 {po} 에 '!' 줄이 없다 (안 돌았거나 수렴 안 함)"))
                continue
            if e0 is None:
                bad.append((j, "본 런 에너지가 없다"))
                continue
            from ase.io import read
            nat = len(read(str(pi), format="espresso-in"))
            d = (e1 - e0) / nat * 1000.0
            over = abs(d) > GK_MAX_MEV
            res[j] = {"group": grp, "n_atoms": nat, "dE_probe_minus_main_meV_per_atom": d,
                      "over_threshold": over,
                      "decision": (("탐침 값을 쓴다" if over else "본 값을 쓴다") if grp == "phase"
                                   else ("k 한계를 Y 에 적는다 · 도핑 k 4 4 1 (gabia) 이 재개 조건" if over
                                         else "본 값을 쓴다 (k 한계 없음)"))}
            print(f"  {j:<8} {grp:<6} ΔE(탐침 − 본) {d:+.3f} meV/원자 {'⛔ > ' if over else '≤ '}{GK_MAX_MEV:g} → {res[j]['decision']}")
        if bad:
            print(f"⛔ 판정 못 한 잡 {len(bad)} — 판정 파일을 쓰지 않는다:")
            for j, why in bad:
                print(f"      {j:<8} {why}")
            return 3
        (out).mkdir(parents=True, exist_ok=True)
        (out / "kprobe_decision.json").write_text(json.dumps(
            {"kind": "kprobe_decision", "card_gate": "G_k_탐침", "threshold_meV_per_atom": GK_MAX_MEV,
             "jobs": res, "⛔": "Y 가 아니다 — 잡마다 k 수렴 차다. Y 는 --collect 로 한 번 낸다"},
            indent=1, ensure_ascii=False) + "\n")
        print(f"✓ 판정 → {out/'kprobe_decision.json'}")
        return 0

    if a.collect:
        import collections
        from ase.io import read
        phase_E, phase_Z, missing, badnorm = {}, {}, [], []
        for name, formula in basis.items():
            e = parse_qe_total(out / f"{name}.out")
            if e is None:
                missing.append(name)
                continue
            # ★ 셀 총에너지 → 화학식당. balance() 계수가 화학식 단위이므로 여기서 맞춰야 한다.
            efu, z, why = phase_energy_per_fu(name, e, out, formula)
            if efu is None:
                badnorm.append((name, why))
                continue
            phase_E[name], phase_Z[name] = efu, z
        if missing:
            print(f"⛔ 기저 상 출력이 없다: {missing} — 빠진 상을 0 으로 두면 "
                  f"그 상이 '공짜' 가 되어 값이 통째로 틀린다. 계산을 마치고 다시.")
            return 3
        if badnorm:
            print(f"⛔ 기저 상 {len(badnorm)}개를 **화학식당으로 정규화하지 못했다** — "
                  f"그대로 쓰면 Z 배 틀린 값이 나온다:")
            for n, why in badnorm:
                print(f"      {n:<8} {why}")
            return 3
        print(f"  기저 {len(phase_E)}상 (셀당 → 화학식당, Z = "
              + ", ".join(f"{n}×{phase_Z[n]}" for n in phase_E) + ")")
        # 상 Pulay (vc-relax 끝 SCF 대 마지막 BFGS) — 끝 SCF 가 없으면 None (지어내지 않는다)
        #   ⛔ 2026-10-26 — 입력이 vc-relax 인 상인데 끝 SCF 를 못 찾으면 **거부**한다. 예전엔 None 만 있으면
        #     이 줄을 통째로 안 찍어서 G_상_이완 게이트가 조용히 빠졌다 (QE 7.4.1 문구 · pulay_gap 주석).
        pulay, vcr = {}, {}
        for name in phase_E:
            pc, _, _ = target_composition(name, out, None)
            vcr[name] = qe_calculation(out / "in" / f"{name}.in") == "vc-relax"
            pulay[name] = pulay_gap_meV_per_atom(out / f"{name}.out", sum(pc.values()) if pc else 0)
        lost = sorted(n for n in phase_E if vcr[n] and pulay[n] is None)
        if lost:
            print(f"⛔ vc-relax 상인데 끝 SCF ('End final coordinates' 뒤의 '!') 를 못 찾았다: {lost} — "
                  f"Pulay 게이트를 못 건다 (안 끝났거나 nstep 소진). 계산을 확인하고 다시.")
            return 3
        bad_pulay = {n: v for n, v in pulay.items() if v is not None and v > PULAY_MAX_MEV}
        g_phase = (not bad_pulay) if any(vcr.values()) else None
        if any(vcr.values()):
            print("  상 Pulay (끝 SCF − 마지막 BFGS, meV/원자): "
                  + ", ".join(f"{n} {'—' if v is None else f'{v:.3f}'}" for n, v in pulay.items())
                  + (f"   ⛔ {PULAY_MAX_MEV} 넘음: {sorted(bad_pulay)} — 끝 구조에서 한 번 더" if bad_pulay else "   ✓"))
        Bs = []
        if a.bulk_modulus_GPa:
            Bs = [a.bulk_modulus_GPa] + (list(a.bulk_modulus_range) if a.bulk_modulus_range else [])
        rows = []
        for f in sorted(out.glob("*.out")):
            stem = f.stem
            if stem in basis:
                continue
            E = parse_qe_total(f)
            comp, csrc, cwhy = target_composition(stem, out, a.struct_dir)
            # ⛔ "에너지 또는 구조" 로 뭉뚱그리면 어느 쪽이 없는지 화면에서 알 수 없다.
            #   (실측 2026-08-26: 에너지는 멀쩡한데 cif 를 CWD 밑에서만 찾아 전부 건너뛰었고,
            #    그런데도 종료코드 0 + 빈 결과 JSON 이 나와 '성공' 처럼 보였다.)
            if E is None:
                print(f"  ⛔ {stem}: 총에너지를 못 읽었다 — {f} 에 '!' 줄이 없다 "
                      f"(계산이 안 끝났거나 죽었다)")
                continue
            if comp is None:
                print(f"  ⛔ {stem}: 조성을 못 정했다 — {cwhy}")
                continue
            bsub = ({n: basis[n] for n in per_target[stem]} if stem in per_target else basis)
            r, info = decomp_energy(comp, E, {n: phase_E[n] for n in bsub}, bsub)
            if r is None:
                print(f"  ⛔ {stem}: {info.get('why')}")
                continue
            r["basis_used"] = sorted(bsub)
            if Bs:
                pk = parse_qe_pressure_kbar(f)
                try:
                    vol = float(read(str(out / "in" / f"{stem}.in"), format="espresso-in").get_volume())
                except Exception as e:                       # noqa: BLE001
                    vol, why_v = None, f"{type(e).__name__}"
                r["P_kbar"], r["V_A3"] = pk, vol
                if pk is None or vol is None:
                    r["volume_correction"] = None
                    print(f"  ⚠ {stem}: 압력 {pk} · 부피 {vol} — 보정 못 함 (0 으로 두지 않는다)")
                else:
                    dev = {str(B): float(volume_correction_eV(pk, vol, B)) for B in Bs}
                    r["volume_correction"] = {
                        "B_GPa": Bs, "dE_V_eV": dev,
                        "delta_E_decomp_corrected_eV_per_atom": {
                            k: float(r["delta_E_decomp_eV_per_atom"] - v / r["n_atoms"]) for k, v in dev.items()},
                        "G_V_P_ok": bool(abs(pk) / 10.0 <= GV_MAX_P_GPA)}
            # ★ 정신차림 검사 — 물리적으로 불가능한 크기면 **찍지 말고 죽는다**.
            #   화면에 -532 eV/atom 이 찍히고 '★ 더 안정' 까지 나온 게 실제 사고였다(2026-08-26).
            de = r["delta_E_decomp_eV_per_atom"]
            if abs(de) > SANITY_MAX_DE_EV:
                print(f"  ⛔ {stem}: ΔE_decomp = {de:+.1f} eV/atom — "
                      f"|{SANITY_MAX_DE_EV}| eV/atom 을 넘는다. 분해에너지는 이런 크기가 될 수 없다.")
                print(f"     거의 확실히 **에너지 정규화**가 어긋난 것이다 "
                      f"(셀당 ↔ 화학식당, 또는 pseudo/컷오프가 상마다 다름).")
                return 5
            r["composition_source"] = csrc          # 어느 파일에서 조성을 읽었는지 남긴다
            rows.append((stem, r))
            print(f"  {stem:<24} ΔE_decomp = "
                  f"{r['delta_E_decomp_eV_per_atom']*1000:+8.1f} meV/atom  "
                  f"(원자 {r['n_atoms']} · 조성 ← {csrc})")
        pair = None
        if a.pair and rows:
            R = dict(rows)
            A_, B_ = a.pair
            if A_ not in R or B_ not in R:
                print(f"⛔ --pair {A_} {B_}: 점수를 못 매긴 쪽이 있다 ({sorted(R)})")
                return 4
            ya = float((R[A_]["delta_E_decomp_eV_per_atom"] - R[B_]["delta_E_decomp_eV_per_atom"]) * 1000)
            pair = {"A": A_, "B": B_, "Y_raw_meV_per_atom": ya}
            ca, cb = R[A_].get("volume_correction"), R[B_].get("volume_correction")
            if Bs and ca and cb:
                yc = {k: float((ca["delta_E_decomp_corrected_eV_per_atom"][k]
                                - cb["delta_E_decomp_corrected_eV_per_atom"][k]) * 1000) for k in ca["dE_V_eV"]}
                dd = {k: float(abs(ca["dE_V_eV"][k] / R[A_]["n_atoms"] - cb["dE_V_eV"][k] / R[B_]["n_atoms"]) * 1000)
                      for k in ca["dE_V_eV"]}
                gv = bool(ca["G_V_P_ok"] and cb["G_V_P_ok"] and max(dd.values()) <= GV_MAX_PAIR_MEV)
                pair.update({"Y_corrected_meV_per_atom": yc, "pair_correction_diff_meV_per_atom": dd,
                             "G_V_pass": gv})
                y0 = yc[str(Bs[0])]
            else:
                pair["G_V_pass"] = None
                y0 = ya
            pair["Y_report_meV_per_atom"] = y0
            pair["G_phase_pass"] = g_phase
            if g_phase is False:
                print(f"  ⛔ G_상_이완 불통과 (Pulay > {PULAY_MAX_MEV} meV/원자: {sorted(bad_pulay)}) — "
                      f"이 Y 를 결과로 쓰지 않는다 · 끝 구조에서 한 번 더 (카드 §4)")
            pair["within_resolution"] = bool(abs(y0) <= a.resolution_meV)
            pair["resolution_meV"] = a.resolution_meV
            print(f"\n★ Y = ΔE_decomp({A_}) − ΔE_decomp({B_}) = {ya:+.2f} meV/atom (보정 전)"
                  + (f" · 보정 (B {Bs[0]:g}) {y0:+.2f} · 범위 "
                     + " · ".join(f"B {k}: {v:+.2f}" for k, v in pair['Y_corrected_meV_per_atom'].items())
                     if "Y_corrected_meV_per_atom" in pair else ""))
            if pair["G_V_pass"] is False:
                print(f"  ⛔ G_V 불통과 (|P| > {GV_MAX_P_GPA} GPa 또는 셀 간 보정 차 > {GV_MAX_PAIR_MEV} meV/atom) "
                      f"— 보정값을 결과로 쓰지 않는다 · 그 셀만 EOS (새 결정)")
            print(f"  분해능 {a.resolution_meV:g} meV/atom → "
                  + ("'구분 못 함' 문장만" if pair["within_resolution"]
                     else f"Y < 0 이면 {A_} 의 분해 구동력이 더 크다 · Y > 0 이면 더 작다"))
        if len(rows) >= 2:
            rows.sort(key=lambda x: -x[1]["delta_E_decomp_eV_per_atom"])
            gap = (rows[0][1]["delta_E_decomp_eV_per_atom"]
                   - rows[1][1]["delta_E_decomp_eV_per_atom"]) * 1000
            print(f"\n★ 더 안정: {rows[0][0]}  (차이 {gap:.1f} meV/atom)")
            print(f"  ⚠ 이것은 E_above_hull 이 아니다 — **5상 기저 안에서의** 비교다. "
                  f"기저 밖 더 낮은 분해 경로는 못 본다.")
        # ⛔ 타깃이 0개인데 종료코드 0 을 주면 **빈 결과가 성공처럼** 보인다
        #   (실측 2026-08-26: 7/7 계산이 끝났는데 조성을 못 찾아 0개였고, 그래도 '✓' 가 찍혔다).
        if not rows:
            print(f"\n⛔ **점수를 매긴 타깃이 0개다** — 결과 파일을 쓰지 않았다.")
            print(f"   기저 {len(phase_E)}상은 다 읽혔으니 남은 문제는 **타깃 쪽**이다. "
                  f"위 ⛔ 줄이 어느 단계에서 막혔는지 말해 준다.")
            return 4
        (out / "decomp_result.json").write_text(json.dumps(
            {"phase_E_eV": phase_E, "basis": basis, "per_target": per_target,
             "phase_pulay_meV_per_atom": pulay, "phase_vc_relax": vcr, "G_phase_pass": g_phase,
             "pair": pair,
             "phase_formula_units_Z": phase_Z,
             "phase_E_note": "화학식당(eV/f.u.) 로 정규화된 값이다 — 셀 총에너지가 아니다",
             "targets": {k: v for k, v in rows},
             "n_targets_scored": len(rows),
             "⛔_do_not": "E_above_hull 로 인용 금지. 5상 공통기저 비교다."},
            indent=2, ensure_ascii=False))
        print(f"\n✓ 타깃 {len(rows)}개 → {out/'decomp_result.json'}")
        return 0

    print("⛔ --prepare / --collect / --selftest 중 하나를 골라라")
    return 2


if __name__ == "__main__":
    sys.exit(main() or 0)
