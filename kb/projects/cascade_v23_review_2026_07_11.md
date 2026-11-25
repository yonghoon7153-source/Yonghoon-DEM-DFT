# Cascade v23 전체 리뷰 — 의도 지도 · 빠진 것 점검 · 후보군 구축 (2026-07-11)

> 목적: v23 캠페인(91 화합물 × x=0.02/0.05/0.10 = 273 cascades)의 **코드 의도를 전체적으로 복기**하고,
> 사용자 질문 3건 — (1) LPSCl(정형 1.0)만 고집한 이유, (2) co-doping 시너지 분류, (3) 과잉도핑 판정 —
> 에 답한 뒤, **논문거리 데이터 목록**과 **DFT-EOS 승격 후보군**을 확정한다.
> 근거 소스: `kb/projects/MULTI_CATEGORY_BATCH_PLAN_v22.md`(273 설계), `docs/cascade/cascade_dopants_2026_06_09.md`
> (41-champion 검증표), `db/properties/doping_cascade_verified.json`(TjDCB 브랜치에서 갱신 반입),
> `db/literature/lpscl_doping_precursor_compounds_review.md`(Type A–D 메커니즘).
> 분석기: `scripts/doping/cascade_v23_candidates.py` (unified_dataset_273.csv → 5부 리포트).

---

## 0. 캠페인 의도 지도 (코드가 하려던 것)

```
master_batch_273.sh (v4.5.20)
 ├─ host = 화학량론 Li6PS5Cl 52-atom 정형셀 (F-43m; Li 24g/48h, P 4b, S 4a/16e, Cl 4c)
 ├─ 91 compounds × 3 농도 = 273 cascade
 │   Tier A 산화물 12 + Tier B 할라이드 6 + Tier C 황/질화물 2 + Tier D 할라이드-rich 2 + 확장 …
 ├─ cascade = 자리 열거(치환 후보 생성) → UMA relax → anneal → champion 선정
 │   변형 체인: 순수 치환 / +Clrich(여분 Cl seed) / Type-B(음이온 치환)
 └─ 산출: champion 구조 + dE_post(형성) + ΔV(변형) + UMA EOS B0 + 탄성 E_VRH
```

- **1차 목적 (논문 #2)**: Layer-2 descriptor의 cold-start 교차검증 — "몇 개 화합물의 cascade 결과로
  나머지 카테고리를 예측할 수 있는가" (LOCO R² 게이트: Tier A ≥0.3, Tier B ≥0.2, cross-category R²).
- **2차 목적 (현대 과제)**: 저탄성(low E_VRH) soft-contact/coating 후보 발굴 — `coating_candidates_ranked_by_E_VRH`.
- **파이프라인 v2 원칙**: vc-relax 없음. UMA 스크리닝 → UMA EOS → (승격 시) KISTI 고정셀 volume grid
  → `llm_fitting_bm.py` BM 피팅. 즉 **DFT는 후보군 확정 후에만** 투입 — 지금이 그 시점.

### 완료/미완 현황
| 항목 | 상태 |
|---|---|
| 273 cascade 실행 | **완료** (273/273; As₂S₃ 3종은 stage-01 `n_structures: 0` 정직 종료 = "cascade가 seed조차 못 만드는 hard-dopant 클래스" 데이터포인트) |
| 41-champion 정밀 검증 (14종 × 3x) | 완료 (06-09 audit; verified.json) |
| unified_dataset_273.csv 통합 분석 | **미실행** ← `cascade_v23_candidates.py`가 이번에 수행 |
| DFT 교차검증 | **전무 (전부 UMA)** ← 이번 EOS 승격의 존재 이유 |
| Sc2O3 x005/x010 | 미실행 (챔피언인데 x002만 존재) |
| 챔피언의 Cl-rich host(modelc-1.6) 재검 | 미실행 ← §1의 갭 |

---

## 1. Q1 — 왜 LPSCl 1.0 정형셀만 고집했나 (1.5/1.6 치환도 되는데)

**설계상 의도된 선택이다. 이유 세 가지:**

1. **자리부기(Wyckoff bookkeeping)의 유일성.** 정형 Li₆PS₅Cl은 Li 24g/48h, P 4b, S 4a/16e, Cl 4c가
   결정학적으로 확정 → 치환 자리 열거가 **결정론적**이고 91종 전체에서 **동일 기준**으로 비교 가능.
   Cl-rich(Li₅.₄PS₄.₄Cl₁.₆ 등)는 S/Cl 부분점유 무질서가 본질 → 화합물마다 무질서 샘플링을 따로 깔아야
   해서 273 스케일에서 조합 폭발 + descriptor 비교 가능성(논문 #2의 핵심) 상실.
2. **Cl-rich 물리를 버린 게 아니라 두 갈래로 우회 커버했다.**
   - `+Clrich` 변형 체인(여분 Cl seed): **Sc2O3_x002, Al2O3_x010, MgO_x002/x005의 챔피언이 전부 +Clrich에서 나옴**
     — "양이온 도펀트 + Cl 풍부화가 순수 산화물 치환보다 안정" = 논문 #1의 Cl-enrichment 결론과 정합.
   - Tier D: LiCl-rich/LiBr-rich Type-B 치환으로 Cl 1.6급 조성 자체를 별도 검증.
3. **기준셀 고정 = dE_post의 공통 baseline.** 273개 cascade의 형성에너지가 전부 같은 undoped 기준 대비라
   랭킹이 성립한다. host를 섞으면 랭킹이 무너진다.

**남은 갭 (이번에 메울 것):** 챔피언들이 **실전 조성(modelc-1.6, Li₅.₃₈₄PS₄.₄Cl₁.₆) host에서 재현되는지**는
아직 아무도 안 봤다. → EOS 승격 프로토콜에 "modelc-1.6 브리지 재치환" 단계를 넣는다(§5).
이는 lpsocl 트랙이 이미 KISTI에서 돌리고 있는 프로토콜과 정확히 동일 — 체인/피팅 인프라 재사용.

---

## 2. Q2 — co-doping 시너지 분류 (좋은 영향 요소들, 같이 시너지 나는 것)

단일 도펀트 성능을 **4개 직교 축**으로 분해하면 상보 페어링이 보인다:

| 축 | 지표 | 단독 최강 (verified-41) | 물리 의미 |
|---|---|---|---|
| 형성 favorability | dE_post 최저 | **Sc2O3_x002 −0.974** ≫ Al2O3군 −0.79~−0.82 ≫ MnO −0.66 | 열역학적 안정 도핑 |
| 연성 (soft-contact) | E_VRH 최저 | **Sc2O3_x002 18.7**, Al2O3_x005 29.3, Li2O_x005 32.4 | 저탄성 코팅 목표 |
| 저변형 | \|ΔV\| 최소 | **SrO_x005 −1.20%**, MnO_x010 −0.46%, CaO_x005 −2.11% | 격자 스트레인 최소 = 계면 정합 |
| 자리 다양성 | champion site | 38/41 Li_24g, **3/41 Li_48h**(Li2O 전농도, Cu2O/Na2O/Ag2O 일부), **0/41 P_4b** | P-사면체는 불가침 → 골격 보존 보장 |

### 시너지 후보 (기대 근거 순)

**(i) 실측 근거 있는 1순위 — cation + Cl-enrichment (Type-C의 캐스케이드 내부 증거):**
- **Sc + Cl↑**, **Al + Cl↑**, **Mg + Cl↑** — 캐스케이드가 스스로 `+Clrich` 체인을 챔피언으로 뽑았다.
  이건 "co-doping이 단독보다 낫다"의 **이미 확보된 계산 증거**이며, modelc-1.6 host 재검(§1 갭)이
  곧 이 3종의 co-doping 검증 실험이 된다. → **승격 1순위와 겹침 = 일석이조.**

**(ii) 문헌 Type-C (precursor review) 명시 조합:**
- **Al@Li + Cl@S**: Li₅.₄Al₀.₁PS₄.₇Cl₁.₃ 문헌 실재 — (i)의 Al+Clrich와 독립적으로 수렴.
- **Mg@Li + F@Cl**: MgF₂가 Tier-B 재료로 이미 배치에 존재 — 한 화합물이 co-doping 전구체 역할.

**(iii) 메커니즘 상보 페어링 (축 교차; 분석기 §4가 자동 생성):**
- **형성강자 × 저변형**: Sc2O3(−0.974, 그러나 ΔV −3.5%) + SrO(ΔV −1.2%) — 에너지 이득 + 스트레인 상쇄.
- **연성 × 저변형**: Al2O3_x005(E 29.3) + MnO(ΔV −0.5~−2.4%) — soft coating인데 격자 정합.
- **자리 분산**: Li_24g 점유자(Sc/Al/Mn) + Li_48h 점유자(Li2O/Cu2O) — 서로 다른 Li 부격자 자리를 써서
  경쟁 없이 공존 가능 → Li2O는 "Li 보충 + 48h 점유"라는 독특한 역할 (단, x010 과잉도핑 주의 §3).
- 주의: (iii)은 **가설 생성기**다. 실제 시너지(비가산성)는 co-doped cascade 또는 DFT로만 확정된다.

---

## 3. Q3 — 과잉도핑(over-doping) 판정 기준과 현재 진단

**판정 기준 4종** (분석기 §2가 자동 플래그):
1. **dE 비단조 / x010 후퇴**: x 증가에 dE가 나빠지면 용해한계 초과 신호.
2. **\|ΔV\| > 6% @ x010**: 격자가 흡수 못 하는 변형 = PS₄ 골격 왜곡 위험.
3. **EOS 피팅 실패 (B0=0)**: E(V) 곡선이 BM 형태를 잃음 = 구조 다중 우물/붕괴 신호.
4. **E_VRH 경화**: soft 목표와 역행하는 x-추세.

**verified-41 기준 현재 진단:**
| 화합물 | 증상 | 판정 |
|---|---|---|
| Li2O_x010 | ΔV **−9.69%** + dE 비단조(−0.553/−0.531/−0.550) | **과잉도핑 확정적** — x002~x005 상한 |
| MgO_x010 | ΔV **−9.12%** (Clrich 변형도 x005에서 −8.64%) | **과잉도핑 확정적** |
| MnO | x005 −0.662 → x010 −0.639 후퇴 (+x002 B0=0) | **최적점 x005** — 전형적 볼케이노 |
| CoO_x010, ZnO_x010 | B0=0 피팅 실패 + dE 단조 하락 | x010 신뢰 불가, x002~x005만 사용 |
| NiO | x005 −0.569 → x010 −0.551 후퇴 | 최적점 x005 |
| Cu2O_x005 | ΔV −8.55% (x002/x010보다 큼, 비단조) | 변형-불안정, 승격 부적격 |
| ZnO_x005 | E_VRH **59.9** (캐스케이드 최경질) | soft 목표와 역행 |
| Al2O3 | 3농도 전부 단조 개선(−0.791→−0.809→−0.818), ΔV ≤5.7% | **과잉도핑 없음** — 가장 강건 |
| SrO, CaO, BaO, Na2O | dE 평탄, ΔV < 5% | 여유 있음 (성능은 중위) |

**종합 규칙**: 이 host에서 산화물 도핑의 실용 상한은 대체로 **x ≈ 0.05**. x010이 이득인 화합물은
Al2O3, BaO 정도 — "많이 넣을수록 좋다"는 성립하지 않음 (논문 고찰 §로 그대로 쓸 수 있는 결론).

---

## 4. 논문거리 데이터 목록 (뽑아서 DFT로 가져갈 것)

| # | 데이터 | 출처 | 논문 용도 |
|---|---|---|---|
| P1 | 41-champion 지도 (dE/E_VRH/ΔV/site) | verified.json | 단일도핑 스크리닝 본표 |
| P2 | 자리 선호 통계 38/41 Li_24g · 0/41 P_4b | 동일 | "P 사면체 불가침" 주장 — 골격보존 도핑 원리 |
| P3 | +Clrich 챔피언 3종 (Sc/Al/Mg) | cascade 변형 체인 | **co-doping 시너지의 무감독 발견** — 하이라이트 |
| P4 | 과잉도핑 문턱 (dE 후퇴 + ΔV>6% + B0=0 동시 발생 패턴) | §3 | 용해한계 고찰 |
| P5 | 카테고리 일반화 (산화물 지배; As₂S₃류 seed 불가) | 273 전수 | descriptor 학습의 화학적 근거 |
| P6 | LOCO 교차검증 R² (Tier A→B 예측) | unified_dataset_273 | 논문 #2 본론 |
| P7 | **top-N 챔피언의 DFT-EOS (B0, V0)** — UMA vs DFT 검증 | ← 이번 승격 | UMA 신뢰구간 확립 = 전체 랭킹의 방법론 방어 |

P7이 없으면 P1~P6 전부가 "UMA 말로는"에 머문다 — **DFT EOS 승격이 논문 방어선.**

---

## 5. DFT-EOS 승격 후보군 (잠정 — v23 통합분석 출력으로 최종 확정)

건강 필터(§3 무플래그) + 축별 대표성 + co-doping 검증 겸용을 기준으로 **5+1종**:

| 순위 | 후보 | 선정 이유 | 비고 |
|---|---|---|---|
| 1 | **Sc2O3_x002 (+Clrich)** | 형성·연성 동시 1위 (−0.974 / 18.7) | co-doping 증거 겸용; **x005/x010 후속 cascade 필요** |
| 2 | **Al2O3_x005** | 전농도 단조·무플래그 최강건; 문헌 루트 | E 29.3 / B0 18.1 — soft coating 대표 |
| 3 | **MnO_x005** | dE −0.662 + ΔV −2.4% 균형 | 볼케이노 정점 표본 (x010 후퇴의 대조군) |
| 4 | **SrO_x005** | ΔV −1.20% 캐스케이드 최소 변형 | 저변형 축 대표; co-doping 파트너 후보 |
| 5 | **Li2O_x005** | E 32.4 연성 + 유일 Li_48h 자리 | 자리 다양성 대표 (x010은 과잉도핑이라 x005 고정) |
| +α | Al2O3_x010(+Clrich) | Al+Cl Type-C 문헌 조합의 계산 대응물 | 여력 있으면 — (i)열 co-doping 재검 확장 |

**승격 프로토콜 (pipeline v2, 기존 인프라 그대로):**
```
champion.xyz (cascade 산출)
  → [브리지] modelc-1.6 host 재치환 (동일 자리 클래스; +Clrich 3종은 Cl-rich host가 본향이라 자연스러움)
  → UMA EOS로 volume grid 산정 (±6%, 7점)
  → KISTI 고정셀 relax 체인: scripts/doping/sbatch_dft_eos_lpsocl_chain.sh 패턴 복제
      (carry-geometry 패치 + forc_conv_thr 1e-3 — Sisyphus 수정 그대로)
  → scripts/doping/llm_fitting_bm.py (BM 피팅 + basin check, v??? 자동탐지)
  → verified.json에 DFT_B0/DFT_V0 컬럼 추가 → P7 완성
```

### 실행 순서 (오늘)
1. gabia에서 `cascade_v23_candidates.py --schema` → 컬럼 확인 → 본 실행 → 5부 리포트 회수.
2. 리포트의 §5(건강 필터 통과 랭킹)와 위 잠정 5+1을 대조 → 최종 후보 확정.
3. Sc2O3 x005/x010 추가 cascade 발사 (gabia, 캐스케이드 러너 재사용).
4. KISTI EOS 체인 생성 (v094~ 패턴; LPSOCl 트랙 완료 후 큐 투입).
