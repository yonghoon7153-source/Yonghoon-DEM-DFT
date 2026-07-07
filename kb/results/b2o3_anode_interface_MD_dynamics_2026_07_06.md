> ⚠️ **SUPERSEDED (2026-07-07)** — 3-seed × 100 ps **통제 campaign**(`b2o3_anode_interface_campaign_2026_07_07.md`)이 이 문서의 "6× 억제"를 **철회**함: 같은 2× 프레임 통제비교에서 b2o3 ≈ 무도핑(PS 손실 22±9 vs 26±0%). 6×는 **얇은 1× 슬랩(modelc62) artifact**였음. 유지되는 결론: **BS₃ 온전·금속 LiB 없음 = 도핑이 계면을 악화시키지 않음**. 아래는 예비(단일시드 50 ps) 기록.

# B₂O₃ champion — anode 계면 **동역학** MLIP-MD: 도핑이 Li-metal 분해를 **억제** (열역학 worst-case 반전)

**날짜** 2026-07-06 · **방법** UMA-s-1p1 MLIP-MD, SE|Li-metal 슬랩, 600 K NVT 50 ps (bottom SE 고정) · **동기** 열역학(평형) 계산은 "b2o3가 Li-metal에서 악화(금속 LiB)"라 했으나 그건 **형태·동역학 미모델**(그 문서가 자인). 실제 반응을 동역학으로 확인.
**도구** `tools/oxidation/{build_li_interface,run_li_interface_md,analyze_interface_decomp}.py` · **데이터** `db/properties/interface_decomp_{b2o3,modelc}.csv` · **그림** `docs/figures/oxidation/interface_decomp_b2o3_vs_undoped.png`

> **한 줄.** 50 ps MLIP-MD에서 **무도핑 LPSCl1.6의 PS₄ 골격이 붕괴**(P–S −47%, P→Li₃P coord 0.8→4.2, S→Li₂S)하는데, **B₂O₃-도핑은 골격을 유지**(P–S −8%, BS₃ 온전, LiB 없음). 모든 지표에서 **b2o3 분해가 무도핑의 16–40%(2.5–6.2× 억제)**. 즉 **평형이 겁준 LiB worst-case는 동역학에서 실현 안 되고, B₂O₃가 오히려 계면을 보호** — 논문의 LPSC-MF(MgS₄ 안 깨짐)와 같은 메커니즘. **kinetics/passivation이 이김.**

---

## 1. 단일-seed 결과 (50 ps, 600 K)
| 지표 | modelc (무도핑) | b2o3 (도핑) | b2o3/modelc |
|---|---|---|---|
| **P–S coord** (PS₄ 온전=4) | 3.80 → 2.00 (**−47%**) | 3.25 → 3.00 (**−8%**) | 0.16 (6.2×↓) |
| **P–Li** (Li₃P 생성) | 0.80 → **4.20** (ΔP–Li 3.40) | 1.00 → 1.62 (Δ0.62) | 0.18 (5.5×↓) |
| **S–Li** (Li₂S 생성) | 3.36 → 5.18 (Δ1.82) | 3.73 → 4.10 (Δ0.37) | 0.20 (4.9×↓) |
| **Li 침투** (초기 표면 하부) | +10 (28→38) | +4 (60→64) | 0.40 (2.5×↓) |
| **B–S** (BS₃≈3) | — | 3.00 → 3.00 **온전** | — |
| **B–Li** (금속 LiB flag) | — | 2.0 → **1.5 감소** (LiB 없음) | — |

**화학:** 무도핑은 Li metal이 PS₄ → PS_n + Li₃P + Li₂S로 분해(argyrodite가 Li-metal에 불안정한 그 알려진 반응). b2o3는 **thioborate BS₃ 온전 + P 거의 안 환원 + Li 표면에 정지** → 얇게 passivate·자기제한.

## 2. 열역학 vs 동역학 — 왜 반대인가
- **열역학**(`b2o3_anode_interface_2026_06_30.md`, open-Li 평형): bare Li-metal(0 V)에서 **금속 LiB** 산물 → "b2o3 악화". **전평형·전조성 투영 = 비관적 상한.**
- **동역학**(본 MD): 얇은 SEI가 먼저 생겨 **자기제한** → B는 LiB로 안 감(B–Li 감소), BS₃ 유지. **Li₃BO₃/passivation 쪽이 kinetically 이김** (Li₃BO₃가 문헌에서 B/borate를 계면 보호막으로 쓰는 이유).
- → 둘은 모순이 아니라 **평형 상한 vs kinetic 실제**. 동역학이 실제 소자 거동에 더 가깝고, **B₂O₃는 보호막 도판트로 작동**.

## 3. Caveat → 완벽 보완 campaign (진행 중)
| caveat | 보완 |
|---|---|
| ① 단일 seed·50 ps·작은 셀 | **3 seed × 100 ps** (`run_interface_campaign.sh`, `--seed`) + 수렴 확인 |
| ② 표면종단 confound (b2o3 128,2× vs modelc 62,1×) | **통제 비교: b2o3 vs `modelc_2x`(124, b2o3의 바로 그 무도핑 원본 frame)** → 같은 표면, 도핑만 차이. modelc_62도 병행해 종단 민감도 교차확인 |
| ③ MLIP 반응상(Li₃P/Li₂S/LiB) 정확도 | **DFT 단발 검증**: 스냅샷 QE SCF → UMA vs DFT 에너지/force (KISTI) |

집계: `aggregate_interface_campaign.py` → `interface_campaign_summary.csv` (계별 mean±std).

## 4. 챔피언 재평가 — 이온 실망 → 계면이 킬러
| 축 | B₂O₃ 효과 | 강도 |
|---|---|---|
| 이온 σ | **O 넣고도 보존**(oxysulfide는 보통 ↓; BVSE 채널 +45%가 O-penalty 상쇄). 3-seed×3T reseed: Ea 0.199≈0.197, σ 비율 1.0 부근 | ✅ 비자명 |
| 기계 | Bulk +13% (EOS 교차검증) | ✅ |
| **anode 계면** | **분해 2.5–6× 억제, 금속 LiB 없음** (동역학) | ✅✅ **킬러(재현 대기)** |
| 전자 | B–S/P–O 공유결합망, host 불변 | 구조 |

## 참고
- `tools/oxidation/build_li_interface.py`(슬랩 빌더), `run_li_interface_md.py`(UMA relax+NVT), `analyze_interface_decomp.py`(지표), `run_interface_campaign.sh`(통제·멀티시드), `aggregate_interface_campaign.py`
- 열역학: `kb/results/b2o3_anode_interface_2026_06_30.md` (open-Li 평형, Li-metal 악화/Li-In 관리가능)
- 이온: `db/properties/b2o3_600K_reseed_errorbar.csv`, `interface_decomp_*.csv`
- 관련 문헌 모티프: LPSC-MF (Mg/F 공도핑, MgS₄ no decomposition) — 사용자 제공 그림
