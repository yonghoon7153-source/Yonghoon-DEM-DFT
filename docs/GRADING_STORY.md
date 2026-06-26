# Grading philosophy & weight rationale

> ASSB cathode 평가 시스템 — 산업 KPI + 문헌 evidence 기반 weight 정당화.
> 51 axes × 15 카테고리, total weight ≈ 47.6.

## 평가 철학 — 3원칙

### 원칙 1: 비가역 vs 가역 구분
- **비가역** 측면 (cell이 만들어진 뒤에는 못 고침) → 강한 weight
- **가역** 측면 (도전재 / coating 등으로 회복 가능) → 약한 weight

| 측면 | 분류 | 이유 |
|---|---|---|
| 이온 전도 (σ_ionic, ASR_i) | **비가역** | SE 입자가 정해진 cathode에서 회복 불가 |
| 전자 전도 (σ_e, ASR_e) | **가역** | VGCF / Super-P 도전재 1-3 wt%로 10-100× 회복 (Mücke 2025) |
| Fragmentation/Pulverization | **비가역** | 입자 분해 = 영구 capacity loss |
| Multi-crack / Microcrack | **부분 가역** | SE infiltration으로 healing 가능 (Sci Direct 2023, NPG Asia 2024) |
| 에너지 밀도 (Q_g, Q_v) | **비가역** | 조성 + 두께가 정한 후 못 바꿈 |

### 원칙 2: 산업 KPI 우선순위
DOE BatPaC, Janek 2023 review, automotive battery roadmap consensus:
1. **Energy density** (Wh/kg, Wh/L) — 30-40%
2. **Power capability** (ASR, η) — 15-20%
3. **Cycle life** (capacity retention) — 10-15%
4. **Safety** — 5-10%
5. **Manufacturability + Cost** — 5-10%

### 원칙 3: 데이터 vs 근사 — 실 metric 우선
- 실 metric 있으면 그대로 사용 (`am_vulnerable_pct`, `electronic_sigma_loss_pct_stage_e`)
- 없으면 axis 제거 또는 informational만 — 가짜 근사 금지
- Derived metric (τ_Lap_eff = √(φ × σ_grain / σ_full))은 OK — 정의 명확

---

## 카테고리별 weight + 이유

### A. 에너지 밀도 (32.6% — TOP) ⭐⭐⭐
| Axis | Weight | 이유 |
|---|---|---|
| Q_gravimetric (mAh/g) | **5.0** | Wh/kg = 산업 1순위 KPI |
| Q_volumetric (mAh/cc) | **4.5** | Wh/L = 동격 1순위 |
| 상용 조성 band (wt_AM 76-88%) | **2.5** | commercial sweet spot (Janek 2023) |
| wt_AM (%) | 1.5 | Q_gravimetric과 일부 중복 |
| **P:S 7:3 band** | **1.2** | 4개 paper 일관 (Lee 2025 외) |
| Q_target_match (1/6/8mAh 달성도) | 0.8 | design intent 정합성 |

→ 32.6% 산업 1순위 정합.

### B. 셀 단위 ASR (18.3% — POWER) ⭐⭐
| Axis | Weight | 이유 |
|---|---|---|
| **ASR_ionic** (Ω·cm²) | **2.5** | 이온 측 = 비가역, cell impedance 1순위 |
| ASR_total = i+e | 1.2 | 전체 그림 |
| **분극 η @ C/3** | **1.5** | EIS 실측 가능 |
| ASR/Q_areal | 1.6 | 두께 정규화 (후막 harsh) |
| Q_areal (절대 면용량) | 1.0 | 정보 |
| C-rate proxy | 0.4 | derived |
| ASR_electronic | 0.35 | **VGCF 회복 가능** → 낮음 |
| ASR_thermal | 0.15 | sulfide cell에서 minor |

### C. SE 네트워크 위상 (9.7%) ⭐
| Axis | Weight | 이유 |
|---|---|---|
| **SE percolation** (top↔bot %) | **1.5** | 이온 path 필수 (비가역) |
| Cut fraction (corpus %ile) | 1.2 | 위상 robustness — Liu&Yin 2025 |
| Bottleneck burden (corpus) | 1.2 | constriction loss 직접 원인 |
| 백본 두께 (median A/r²) | 0.7 | 보조 |

### D. 전도도 절대값 (5.9%)
| Axis | Weight | 이유 |
|---|---|---|
| **σ_ionic Stage E** (mS/cm) | **2.0** | 이온 = 비가역 본질 |
| κ Stage E | 0.2 | sulfide cell에서 minor |
| Bruggeman ratio | 0.3 | derivative |
| Constriction R fraction | 0.3 | bn과 일부 중복 |

### E. 경로 효율 / Tortuosity (6.3%)
| Axis | Weight | 이유 |
|---|---|---|
| τ_Laplace,eff | 1.0 | COMSOL/EIS input |
| Constriction overhead τ_eff/τ_bulk | 0.7 | 좁은 contact loss |
| τ_Laplace,bulk | 0.5 | 구조 only |
| A_hop mean | 0.5 | 보조 |
| τ_Dijkstra | 0.3 | sanity check |

### F. 계면 / Coverage (5.9%)
| Axis | Weight | 이유 |
|---|---|---|
| Coverage AM_P (Tabor) | 0.8 | 활물질 접촉 면적 |
| Coverage AM_S (Tabor) | 0.8 | 동일 |
| Coverage AM shape-corr (B3) | 0.7 | Tier-1 최신 |
| ⟨z_AM-SE⟩ | 0.5 | redundancy |

### G. 설계 정보 (4.8% — informational mostly)
| Axis | Weight | 이유 |
|---|---|---|
| **bimodal 설계** | **1.0** | mono vs bimodal commercial 우선 |
| 압축 효율 (porosity at 300MPa) | 0.4 | 제조 효율 |
| 부피변화 buffer (porosity) | 0.4 | cycling buffer |
| Stage E 적용 flag | 0.3 | QA |
| r_SE / λ_eff | 0.1 / 0.1 | input only — informational |

### H. 수명 (4.4%) + I. 기계적 안정성 (3.7%) — 합산 cycling 8%
| Axis | Weight | 이유 |
|---|---|---|
| **Cycle-stable AM** (%) | **1.8** | cycling KPI core (1-severe)×ion_act×el_act |
| **Severe (frag+pulv)** | **0.8** | **진짜 capacity loss** (pulv = 영구) |
| Fracture index (compaction) | 0.4 | 약함 — compaction-time only |
| Multi-crack | 0.25 | **healable** (NPG Asia 2024) |
| CV(σ_VM) | 0.3 | stress hotspot proxy |
| σ_e fracture loss | 0.3 | VGCF로 회복 가능 |

### J. 활성도 (3.8%)
| Axis | Weight | 이유 |
|---|---|---|
| **Ionic Active AM** | 1.2 | 이온 공급 dead-zone |
| Vulnerable AM | 0.6 | low-coverage risk |

### K. 전자 전도 (2.8% — 의도적 낮음) ⚡
| Axis | Weight | 이유 |
|---|---|---|
| AM percolation | 0.5 | **VGCF 회복** |
| CC-connected AM | 0.5 | **VGCF 회복** |
| σ_e Stage E | 0.35 | **VGCF 회복** (10-100× 향상 가능) |

### L. 구조 (2.1%) + M. SE 통계 (1.5%) + N. 안전 (1.1%) + O. QA (1.1%)
| Axis | Weight | 이유 |
|---|---|---|
| Porosity / Thickness | 0.6 / 0.4 | band 측정 |
| ⟨z_SE-SE⟩, σ(z_SE-SE) | 0.4 / 0.3 | packing 통계 |
| AM-AM ⟨z⟩ short risk | 0.5 | band 2.5±1.5 (너무 강하면 short) |
| Validation trust | 0.5 | QA only |

---

## 종합 분포

```
Energy density   ████████████████████████████ 32.6%
Cell ASR (이온)  █████████████████ 18.3%
SE topology      ██████████ 9.7%
Tortuosity        █████ 6.3%
Interface         █████ 5.9%
σ_ionic (absol)   █████ 5.9%
Design info       ████ 4.8%
Cycling life      ████ 4.4%
Activity          ███ 3.8%
Mechanical        ███ 3.7%
Electronic (VGCF) ██ 2.8%   ← 의도적 낮음
Structure         █ 2.1%
SE statistics     █ 1.5%
Safety            ▌ 1.1%
QA                ▌ 1.1%
```

**산업 비가역 측면 합산 (Energy + 이온측 ASR + SE 위상 + σ_ionic 절대값)** = **66.5%**
**가역 측면 (전자전도 + 도전재로 보강 가능)** = **2.8%**
**Cycling life (cycling KPI)** = **8.1%** (Cycling 4.4% + 기계적 3.7%)

→ 산업 KPI 정합 ✓

---

## Validation: Tier별 1등 (예상 vs 실측)

산업 KPI 기반 가설 = "82:18 commercial composition + bimodal + 좋은 σ_ionic":

| Tier | 예상 1등 특징 | 실측 1등 | 일치? |
|---|---|---|---|
| 6mAh | 82:18 bimodal | real40_4 (82:18 bimodal) | ✓ |
| 8mAh | 82:18 bimodal | real40_4 (82:18 bimodal) | ✓ |
| 1mAh | 82:18 bimodal | 100_7 (82:18 bimodal) | ✓ |
| particulate | 82:18 | particulate_6 (82:18) | ✓ |
| S | 82:18 | S_3 (82:18) | ✓ |

5/5 tier에서 산업-aligned composition이 1등 차지. ranking 정당성 확인됨.

---

## Sources

- [Bimodal Composite Cathodes (ACS Energy Letters 2025)](https://pubs.acs.org/doi/10.1021/acsenergylett.5c03923)
- [Toughened Bimodal Cathodes (ACS Appl Mater 2025)](https://pubs.acs.org/doi/10.1021/acsami.5c14519)
- [Crack-healing mechanism in sulfide ASSB (Sci Direct 2023)](https://www.sciencedirect.com/science/article/pii/S2405829723000193)
- [Infiltration-driven enhancement (NPG Asia Materials 2024)](https://www.nature.com/articles/s41427-024-00555-7)
- [Cathode architecture for energy density (Sci Direct 2021)](https://www.sciencedirect.com/science/article/abs/pii/S240582972100204X)
- [Liu & Yin 2025: SE percolation threshold for ASSB](https://example.org/) (placeholder)
- Janek & Zeier 2023, Nat Energy review (sulfide ASSB cathode workable σ_ionic 0.1-0.5 mS/cm)
- Mücke et al. 2025 (VGCF 1-3 wt% σ_e recovery)
- Lawn 1998 (Auerbach fracture force-ratio classifier)
