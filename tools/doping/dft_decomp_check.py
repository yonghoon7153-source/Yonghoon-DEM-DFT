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
    ok = resid <= BALANCE_TOL and not neg
    info = {"elements": els, "residual_max_atoms": resid,
            "negative_phases": neg, "ok": ok,
            "coeffs": {n: float(v) for n, v in zip(basis, x)}}
    if not ok:
        if resid > BALANCE_TOL:
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
    a = ap.parse_args()

    if a.selftest:
        return _selftest()
    if not a.out:
        print("⛔ --out 이 필요하다")
        return 2
    out = Path(a.out)

    if a.prepare:
        import os
        from ase.io import read
        from generate_dft_inputs import generate_pwin
        key = os.environ.get("MP_API_KEY")
        if not key:
            print("⛔ MP_API_KEY 가 없다 (기저 상 구조를 받아야 한다)")
            return 2
        if not a.targets:
            print("⛔ --targets 가 필요하다")
            return 2
        from mp_api.client import MPRester
        from pymatgen.io.ase import AseAtomsAdaptor
        from generate_dft_inputs import PSEUDOS, PSEUDO_DIR_KISTI
        ad = AseAtomsAdaptor()
        offhull, need_pp, pending, mp_used = [], set(), [], {}
        pdir = Path(a.pseudo_dir or PSEUDO_DIR_KISTI)
        print(f"pseudo_dir = {pdir}"
              + ("" if a.pseudo_dir else "   ⚠ 기본값(KISTI) — 다른 머신이면 --pseudo_dir 를 줄 것"))
        pp_names = dict(x.split("=", 1) for x in (a.pseudo_map or "").split(",") if x)
        if pp_names:
            print(f"  · 수동 지정 {pp_names}")
        with MPRester(key) as mpr:
            for name in DEFAULT_BASIS:
                mpid = BASIS_MPID.get(name)
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
                pending.append((name, at, a.kpoints_phase,
                                not a.phase_symmetry))
                mp_used[name] = {"mp_id": d.material_id, "n_atoms": len(at),
                                 "mp_e_above_hull": float(d.energy_above_hull)}
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
            resolved = {e: PSEUDOS[e][1] for e in sorted(need_pp) if e in PSEUDOS}

        if unresolved:
            print(f"\n  ⛔ pseudo 를 못 정한 원소 {len(unresolved)}개 — "
                  f"**입력을 하나도 쓰지 않았다**:")
            for e, why in unresolved.items():
                print(f"      {e:<3} {why}")
            print(f"     → --pseudo_map 'Li=…,S=…' 로 지정하거나 파일을 넣을 것")
            return 3
        (out / "in").mkdir(parents=True, exist_ok=True)
        for name, at, kp, nosym in pending:
            (out / "in" / f"{name}.in").write_text(
                generate_pwin(at, name, a.ecutwfc, a.ecutrho, kp,
                              pseudo_dir=str(pdir), pp_names=resolved,
                              calculation=a.calculation, nosym=nosym))

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
            "basis": DEFAULT_BASIS, "basis_mp": mp_used,
            "targets": [str(x) for x in a.targets],
            "⛔_do_not": "E_above_hull 로 인용 금지. 5상 공통기저 안의 상대 비교다.",
        }, indent=2, ensure_ascii=False))
        print(f"\n✓ 입력 → {out/'in'}   (기저 {len(DEFAULT_BASIS)} + 타깃 {len(a.targets)})")
        print(f"✓ 설정 기록 → {out/'prepare_provenance.json'}")
        return 0

    if a.collect:
        import collections
        from ase.io import read
        phase_E, phase_Z, missing, badnorm = {}, {}, [], []
        for name, formula in DEFAULT_BASIS.items():
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
        rows = []
        for f in sorted(out.glob("*.out")):
            stem = f.stem
            if stem in DEFAULT_BASIS:
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
            r, info = decomp_energy(comp, E, phase_E)
            if r is None:
                print(f"  ⛔ {stem}: {info.get('why')}")
                continue
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
            {"phase_E_eV": phase_E, "basis": DEFAULT_BASIS,
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
