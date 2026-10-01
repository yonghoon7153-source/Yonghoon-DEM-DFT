"""inventory.py — reference 셀의 리튬 재고 분배 (LLI 환산 상수).

────────────────────────────────────────────────────────────────────────
LLI 환산식 유도 ★

전하 보존으로 각 전극의 화학량론을 x(정규화 용량)로 표현하면

    s = (x − β)/α ,   α_PE = (1−LAM_PE)/r ,  α_NE = (1−LAM_NE)/r ,  r = Q_deg/Q_ref

이고, β는 시작 화학량론의 차이를 담는다. 절대 용량 단위로 정리하면

    β_PE·Q_deg = −(y0_deg − y0_ref)·C_PE_deg          (PE: 방전 중 리튬화)
    β_NE·Q_deg = +(z0_deg − z0_ref)·C_NE_deg          (NE: 방전 중 탈리튬화)

전체 재고 n_Li = y0·C_PE + z0·C_NE 에 대입하면

    n_Li_deg = α_PE·r·(y0_ref·C_PE_ref) + α_NE·r·(z0_ref·C_NE_ref)
             + (β_NE − β_PE)·r·Q_ref

따라서 LLI = 1 − n_Li_deg/n_Li_ref 는

    ★ LLI = 1 − r·[ w_PE·α_PE + w_NE·α_NE + κ·(β_NE − β_PE) ]

      w_PE, w_NE : reference 재고 중 각 전극이 가진 비율 (합 = 1)
      κ          : Q_ref / n_Li_ref   (기준 용량 / 기준 총재고)

21p 식과는 **두 군데**가 다르다.
  (a) 가중치: 21p는 w_PE=1, w_NE=0, κ=1 — "재고가 전부 양극에 있고 총재고 =
      셀 용량". 이 셀은 기준 상태에서 재고의 71%가 음극에 있고 총재고(8.1 Ah)가
      가용용량(5.72 Ah)의 1.4배라 성립하지 않는다.
  (b) β 항의 부호: 유도 결과는 +(β_NE − β_PE)인데 21p는 +(β_PE − β_NE)다.
      원본 코드 주석의 "기존 부호가 반대였음"이 같은 지점을 가리킨다.
      가중치를 21p와 같게 두고 부호만 바꿔도 |오차|가 0.128 → 0.076으로 준다.

검증 (합성 격자 95조건, 정답 기준 평균 |오차|):
    21p 식 0.128 / 원본 코드 식 0.200 / 경험적 NE기준 0.031 / **유도식 0.012**
자유 최소제곱의 하한이 0.0097이므로 유도식은 사실상 그 한계에 근접한다.
회귀로 얻은 상수(w_PE 0.313, w_NE 0.607, κ 0.715)도
유도값(0.291 / 0.709 / 0.706)과 일치한다.
────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

F_CONST = 96485.0   # C/mol

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ReferenceInventory:
    """LLI 환산에 필요한 reference 셀 상수."""

    n_pe_ah: float          # 기준 상태에서 양극이 가진 리튬 [Ah]
    n_ne_ah: float          # 음극이 가진 리튬 [Ah]
    q_ref_ah: float         # 기준 셀 방전용량 [Ah]

    @property
    def n_total_ah(self) -> float:
        return self.n_pe_ah + self.n_ne_ah

    @property
    def w_pe(self) -> float:
        return self.n_pe_ah / self.n_total_ah

    @property
    def w_ne(self) -> float:
        return self.n_ne_ah / self.n_total_ah

    @property
    def kappa(self) -> float:
        return self.q_ref_ah / self.n_total_ah

    def as_dict(self) -> dict:
        return {"n_pe_ah": self.n_pe_ah, "n_ne_ah": self.n_ne_ah,
                "q_ref_ah": self.q_ref_ah, "w_pe": self.w_pe,
                "w_ne": self.w_ne, "kappa": self.kappa}


def reference_inventory(cfg: dict, q_ref_ah: float) -> ReferenceInventory:
    """config baseline + 파라미터셋 기하로 reference 재고를 계산한다.

    q_ref_ah: 실측 reference 방전용량 [Ah] (grid 결과에서 가져온다)
    """
    import pybamm

    b = cfg["baseline"]
    p = pybamm.ParameterValues(cfg["parameter_set"])
    area = p["Electrode height [m]"] * p["Electrode width [m]"]
    l_pe = p["Positive electrode thickness [m]"]
    l_ne = p["Negative electrode thickness [m]"]
    k = F_CONST * area / 3600.0        # mol/m3 · m → Ah

    n_pe = k * b["pe_init_conc"] * b["pe_vf"] * l_pe
    n_ne = k * (b["ne_primary_init_conc"] * b["ne_primary_vf"]
                + b["ne_secondary_init_conc"] * b["ne_secondary_vf"]) * l_ne

    inv = ReferenceInventory(n_pe_ah=float(n_pe), n_ne_ah=float(n_ne),
                             q_ref_ah=float(q_ref_ah))
    log.info("reference 재고: PE %.3f Ah, NE %.3f Ah (w_PE=%.3f, w_NE=%.3f, κ=%.3f)",
             inv.n_pe_ah, inv.n_ne_ah, inv.w_pe, inv.w_ne, inv.kappa)
    return inv
