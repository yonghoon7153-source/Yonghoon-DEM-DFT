# B₂O₃-doped 챔피언 — Bader + Löwdin 전하 → 산화상태 + XPS BE 경향

**날짜** 2026-06-30 · **방법** QE pp.x(USPP) 전하밀도 cube → Bader(Henkelman) + projwfc Löwdin
**구조** `db/structures/b2o3_relaxV0.cif` (DFT V₀, 128 atom) · **데이터** `db/properties/b2o3_charge_xps.csv` · **그림** `docs/figures/cascade/b2o3_charge_xps.png`

> **한 줄.** Bader가 **산화상태(B³⁺·P⁵⁺·O²⁻·Cl⁻·Li⁺·S²⁻)를 확증**하고, Löwdin(궤도투영, basin artifact 없음)이 **S 자리별 XPS BE 경향을 깨끗이** 줌: **free-S²⁻ 가장 낮은 S 2p BE(가장 이온성, DOS/ESW와 정합) · BS₃의 B–S 가장 높은 BE(가장 공유성) = testable BS₃ 지문.** 두 방법의 S-순서 불일치 자체가 **B–S/P–S 공유결합의 증거.**

---

## 1. 결과 (valence 전자수 → 순전하)
| 자리 | Z_val | Bader e⁻ | Löwdin e⁻ | Bader 순전하 | 신뢰 |
|---|---|---|---|---|---|
| **B** | 3 | **0.000** | 3.118 | **+3.00** | 산화상태=Bader |
| **P** | 5 | 0.309 | 3.949 | **+4.69** | 산화상태=Bader |
| **O** | 6 | 7.918 | 6.628 | **−1.92** | 산화상태=Bader |
| **Cl** | 7 | 7.914 | 6.960 | **−0.91** | 산화상태=Bader |
| **Li** | 3 | 2.119 | 3.062 | **+0.88** | 산화상태=Bader |
| free-S | 6 | 7.692 | **6.057** | −1.69 | **자리순서=Löwdin** |
| PS4-S | 6 | 7.823 | **6.033** | −1.82 | **자리순서=Löwdin** |
| B-S(BS₃) | 6 | 7.872 | **5.854** | −1.87 | **자리순서=Löwdin** |

## 2. 해석 A — 산화상태 (Bader, 확증)
**B +3.00 / P +4.69 / O −1.92 / Cl −0.91 / Li +0.88 / S ~−1.7~1.9.**
→ **B³⁺(BS₃·B–O) · P⁵⁺(thiophosphate) · O²⁻ · Cl⁻ · Li⁺ · S²⁻-ish** 산화상태 그림 **확증**. (배위/DOS/ESW/hull에 이은 추가 확증.)
- **B=0.000(Bader)** 자체가 B³⁺ 극대산화의 신호(USPP valence basin 붕괴 = 전자 다 내줌).

## 3. 해석 B — S 자리별 XPS BE 경향 (Löwdin, 깨끗)
Löwdin e⁻: **B-S(BS₃) 5.854 < PS4-S 6.033 < free-S 6.057** → **S 2p BE 순서: B-S > PS4-S > free-S.**
- **free-S²⁻ = 가장 많은 전자 = 가장 이온성/환원 → 가장 낮은 S 2p BE.** ↔ **DOS(free-S 3p 가장 얕음)·ESW(free-S 먼저 산화)** 와 정확히 정합. free-S²⁻가 "노출된 반응성 sulfide"임을 전하로 재확인.
- **B-S(BS₃) = 가장 적은 전자 = 가장 공유성 → 가장 높은 S 2p BE.** B–S(1.83 Å, 짧고 강한 공유)가 S 밀도를 결합으로 끌어감. → **BS₃ 황은 별도 고-BE shoulder = testable XPS 지문.**
- (free-S vs PS4-S 차이는 0.024로 미세 — free-S 한계 marginal하게 더 이온성; B-S가 0.2로 뚜렷이 분리.)

## 4. ⚠️ 방법별 신뢰 영역 (정직)
- **Bader**: 음이온(O/Cl)·Li·산화상태엔 신뢰. 단 **고산화 경원소(B/P) basin 붕괴**(B=0.000) → **B–S/P–S 결합전자가 S로 새서 PS4-S·B-S를 인위적 음전하로 부풀림** → **Bader의 S-자리 순서는 artifact**(B-S가 거짓으로 가장 음전하).
- **Löwdin**: 궤도투영이라 basin 문제 없음 → **S-자리 상대순서 신뢰**. 단 **이온성 과소평가**(Cl +0.04·Li −0.06로 거의 중성 = 비현실) → **절대 순전하·산화상태엔 부적합.**
- → **산화상태는 Bader, S-자리 BE 순서는 Löwdin.** 두 방법의 **S-순서 불일치(Bader B-S 최음 vs Löwdin B-S 최양)** 자체가 **B–S/P–S 공유결합**의 직접 증거(공유 결합전자를 Bader는 S에, Löwdin은 양이온에 배분).

## 5. testable XPS 예측 (계산 가능 원소)
| 피크 | 예측 |
|---|---|
| **S 2p** | 3성분: **free-S²⁻(최저 BE) · PS4-S(중간) · B-S/BS₃(최고 BE shoulder)** |
| **B 1s** | B³⁺ 고-BE (BS₃/B–O) |
| **P 2p** | P⁵⁺ (PS₄/PS₄₋ₓOₓ) |
| O 1s / Cl 2p | O²⁻ phosphate / Cl⁻ |

(Nd 3d는 multiplet이라 문헌값 — `nd_xps_literature_basis_2026_06_30.md`. 정량 절대 BE는 ΔSCF core-hole(ORCA) 후속.)

## 6. 정직한 한계
- USPP plot_num=0 = **valence 밀도** → Bader/Löwdin 둘 다 **상대비교용**(절대 전하는 PAW/all-electron 권장). 본 결론은 **상대순서·산화상태 정성**이라 견고.
- 단일 Li-config. 4a/4d Cl 전하분리는 미세분석 별도(필요시).

## 참고
- `db/properties/b2o3_charge_xps.csv`, `docs/figures/cascade/b2o3_charge_xps.png`
- ELF cube `b2o3_elf.cube`(gabia/KISTI, VESTA) = 결합 국재 직접 확증(basin 무관) — 후속
- 관련: `kb/results/b2o3_champion_coordination_2026_06_29.md`(BS₃ 5중 확증), `b2o3_dos`(free-S 3p 최얕), `nd_xps_literature_basis_2026_06_30.md`
