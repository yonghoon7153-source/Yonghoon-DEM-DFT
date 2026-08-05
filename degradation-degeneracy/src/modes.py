"""modes.py — 열화 모드 → pybamm 파라미터 override 변환.

두 개의 진입점을 제공한다.

1) single_mode_overrides(mode, i, ...)
   원본 update_fn (reference/degrade_mode_sim_original.py L134~L216)과
   **정확히 동일한 dict**를 반환한다. sweep1d(32p 재현)와 회귀 테스트가 사용.
   단, 원본의 완방상태 하드코딩(36.7/3446.3/58439.9) 자리는 자동 산출값으로 대체.

2) build_overrides(lli, lam_pe, lam_ne, ...)
   조합 격자용 중첩 적용. 적용 순서 고정: LAM_PE → LAM_NE → LLI
   (03_ARCHITECTURE.md 4절).

   ★ 조합은 charge_first(완방 시작) 프레임으로 통일한다. 이때:
     - 모든 초기 농도를 완방상태 기준으로 명시 설정한다.
       (03_ARCHITECTURE 스케치는 lam=0인 전극의 농도를 완충 baseline으로 남겨
        전극 간 상태 불일치·재고 이중계상이 발생 — 수정. CHANGELOG 참조)
     - LLI는 NE·PE 농도 모두에 (1−lli)를 곱한다.
       완방 프레임에서 재고는 거의 전부 PE에 있으므로, 스케치대로 NE에만 곱하면
       전체 재고의 ~0.1%만 제거되어 사실상 no-op이 된다. 모든 저장소를 동일
       비율로 줄이면 전체 재고가 정확히 lli 비율만큼 감소한다 (Birkl LLI 정의와 일치).
"""

from __future__ import annotations

from dataclasses import dataclass

from src.baseline import DischargedState

# pybamm 파라미터 이름 (원본 update_fn과 동일 문자열)
P_NE1_INIT = "Primary: Initial concentration in negative electrode [mol.m-3]"
P_NE2_INIT = "Secondary: Initial concentration in negative electrode [mol.m-3]"
P_PE_INIT = "Initial concentration in positive electrode [mol.m-3]"
P_NE_POR = "Negative electrode porosity"
P_NE1_VF = "Primary: Negative electrode active material volume fraction"
P_NE2_VF = "Secondary: Negative electrode active material volume fraction"
P_PE_POR = "Positive electrode porosity"
P_PE_VF = "Positive electrode active material volume fraction"


class InfeasibleConditionError(ValueError):
    """물리적으로 불가능한 조합 (guards 위반). grid에서 failed.csv로 기록."""


@dataclass(frozen=True)
class Baseline:
    """config baseline 절의 값 묶음 (완충 기준)."""

    ne_primary_init_conc: float
    ne_primary_max_conc: float
    ne_secondary_init_conc: float
    ne_secondary_max_conc: float
    pe_init_conc: float
    pe_max_conc: float
    ne_porosity: float
    ne_primary_vf: float
    ne_secondary_vf: float
    pe_porosity: float
    pe_vf: float

    @classmethod
    def from_config(cls, cfg: dict) -> "Baseline":
        return cls(**{k: float(v) for k, v in cfg["baseline"].items()})


# ---------------------------------------------------------------- 1) 원본 1:1

def single_mode_overrides(mode: str, i: float, b: Baseline,
                          d: DischargedState) -> dict:
    """원본 update_fn과 키·수식이 정확히 일치하는 override dict.

    원본과의 대응 (reference/degrade_mode_sim_original.py):
      lli        L136-139 | lam_pe_de  L176-180 | lam_ne_de  L186-193
      lam_pe_li  L199-205 | lam_ne_li  L211-215
    하드코딩 자리 대체: 36.7→d.ne_primary, 3446.3→d.ne_secondary, 58439.9→d.pe
    """
    if mode == "reference":
        return {}

    if mode == "lli":
        return {
            P_NE1_INIT: b.ne_primary_init_conc * (1 - i),
            P_NE2_INIT: b.ne_secondary_init_conc * (1 - i),
        }

    if mode == "lam_pe_de":
        return {
            P_PE_POR: b.pe_porosity + b.pe_vf * i,
            P_PE_VF: b.pe_vf * (1 - i),
            P_PE_INIT: b.pe_init_conc / (1 - i),
        }

    if mode == "lam_ne_de":
        return {
            P_NE_POR: b.ne_porosity + (b.ne_primary_vf + b.ne_secondary_vf) * i,
            P_NE1_VF: b.ne_primary_vf * (1 - i),
            P_NE2_VF: b.ne_secondary_vf * (1 - i),
            P_NE1_INIT: d.ne_primary / (1 - i),
            P_NE2_INIT: d.ne_secondary / (1 - i),
            P_PE_INIT: d.pe,
        }

    if mode == "lam_pe_li":
        return {
            P_PE_POR: b.pe_porosity + b.pe_vf * i,
            P_PE_VF: b.pe_vf * (1 - i),
            P_NE1_INIT: d.ne_primary,
            P_NE2_INIT: d.ne_secondary,
            P_PE_INIT: d.pe,
        }

    if mode == "lam_ne_li":
        return {
            P_NE_POR: b.ne_porosity + (b.ne_primary_vf + b.ne_secondary_vf) * i,
            P_NE1_VF: b.ne_primary_vf * (1 - i),
            P_NE2_VF: b.ne_secondary_vf * (1 - i),
        }

    raise KeyError(f"알 수 없는 모드: {mode}")


# ---------------------------------------------------------------- 2) 조합 격자

def build_overrides(lli: float, lam_pe: float, lam_ne: float,
                    lam_pe_type: str, lam_ne_type: str,
                    b: Baseline, d: DischargedState,
                    guards: dict | None = None) -> dict:
    """조합 격자용 override (charge_first / 완방 프레임 통일).

    적용 순서 고정: LAM_PE → LAM_NE → LLI.
    모든 값 0이면 빈 dict (= reference 조건).

    guards 위반(농도>최대, porosity 초과 등)은 InfeasibleConditionError로 던진다
    — 해당 조합이 고정 cutoff 하에서 물리적으로 성립하지 않는다는 뜻이며,
    grid는 이를 failed.csv에 기록하고 계속 진행한다.
    """
    g = guards or {}
    max_mode = float(g.get("max_mode_value", 0.9))
    max_por = float(g.get("max_porosity", 0.95))
    min_vf = float(g.get("min_vf", 1e-4))

    for name, v in (("lli", lli), ("lam_pe", lam_pe), ("lam_ne", lam_ne)):
        if not 0 <= v <= max_mode:
            raise InfeasibleConditionError(f"{name}={v} 는 [0, {max_mode}] 밖")
    if lam_pe_type not in ("de", "li") or lam_ne_type not in ("de", "li"):
        raise InfeasibleConditionError(
            f"lam type은 de|li 만 지원: pe={lam_pe_type}, ne={lam_ne_type}")

    if lli == 0 and lam_pe == 0 and lam_ne == 0:
        return {}

    ov: dict = {}

    # ── 완방 프레임 시작점: 모든 초기 농도를 완방상태로 명시 ──
    ne1, ne2, pe = d.ne_primary, d.ne_secondary, d.pe

    # 1) LAM_PE
    if lam_pe > 0:
        ov[P_PE_VF] = b.pe_vf * (1 - lam_pe)
        ov[P_PE_POR] = b.pe_porosity + b.pe_vf * lam_pe
        if lam_pe_type == "de":
            pe = pe / (1 - lam_pe)   # 죽은 PE는 비어 있었음 → 남은 PE가 재고 전량 보유

    # 2) LAM_NE
    if lam_ne > 0:
        vf_tot = b.ne_primary_vf + b.ne_secondary_vf
        ov[P_NE1_VF] = b.ne_primary_vf * (1 - lam_ne)
        ov[P_NE2_VF] = b.ne_secondary_vf * (1 - lam_ne)
        ov[P_NE_POR] = b.ne_porosity + vf_tot * lam_ne
        if lam_ne_type == "de":
            ne1 = ne1 / (1 - lam_ne)
            ne2 = ne2 / (1 - lam_ne)

    # 3) LLI — 마지막. 모든 저장소를 (1-lli)배 → 전체 재고가 정확히 lli만큼 감소
    if lli > 0:
        ne1 *= (1 - lli)
        ne2 *= (1 - lli)
        pe *= (1 - lli)

    ov[P_NE1_INIT] = ne1
    ov[P_NE2_INIT] = ne2
    ov[P_PE_INIT] = pe

    # ── guards: 물리적 성립 검증 ──
    problems = []
    if pe > b.pe_max_conc:
        problems.append(
            f"PE 초기농도 {pe:.0f} > c_max {b.pe_max_conc:.0f} "
            f"(줄어든 PE가 완방 재고를 수용 불가 — PE-limited 영역)")
    if ne1 > b.ne_primary_max_conc:
        problems.append(f"NE(Gr) 초기농도 {ne1:.0f} > c_max {b.ne_primary_max_conc:.0f}")
    if ne2 > b.ne_secondary_max_conc:
        problems.append(f"NE(Si) 초기농도 {ne2:.0f} > c_max {b.ne_secondary_max_conc:.0f}")
    for key, por in ((P_PE_POR, ov.get(P_PE_POR)), (P_NE_POR, ov.get(P_NE_POR))):
        if por is not None and por > max_por:
            problems.append(f"{key} = {por:.3f} > {max_por}")
    for key in (P_PE_VF, P_NE1_VF, P_NE2_VF):
        if key in ov and ov[key] < min_vf:
            problems.append(f"{key} = {ov[key]:.2e} < {min_vf}")
    if problems:
        raise InfeasibleConditionError("; ".join(problems))

    return ov
