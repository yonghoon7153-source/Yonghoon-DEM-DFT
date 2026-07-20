# 문헌-앵커 generalizable reference R_int(N) 설계 (Phase 1)

정의일 2026-07-20.  프로젝트 `docs/project_rint_fullcell_cycling.md` Phase 1의 핵심 설계.
앵커 데이터 조사 = `docs/rint_anchor_db_research.md`(Phase 0) — 이 문서는 그 위에 **성장-법칙 + 전이성 설계**를 얹는다.
문헌 근거는 3-에이전트 조사(2026-07-20: 양극성장법칙 / 크기-bimodal전이성 / 모델링파라미터+집전체)로 확보 —
egress 403으로 **web 수치는 대부분 `confirmed_snippet`** (PDF 검증은 WSL); 단 **kim2025는 우리 litdb `pdf_verified`**.

## 0. 발단 (사용자 질문, 2026-07-20)
1. **"R_int을 초반·후반만 앵커하고 사이클 따라 유동적으로 안 되나?"** → 유동적 R_int(N) 궤적.
2. **"이건 SDCP 특이 케이스고, reference는 문헌값으로 하면 안 되나? 앞으로 bimodal 등 여러 개 할 건데."**
   → reference = 문헌 앵커, 특이재료(SDCP)만 실측, **여러 config(bimodal/mono/크기별)로 확장.**

## 1. 왜 2점 앵커만으론 부족한가 (Q1)
pristine·cycled **두 점**만 있으면 사이 곡선은 **무한히 많다**(√N vs 선형 vs 포화).  2점 보간 = "가정한 형태"이지
측정 아님 → §F1 원칙 #2(보간·눈대중 금지) 위반.  **해결: 문헌이 "모양(성장 법칙)"을 준다.**

## 2. ★ 핵심 아키텍처 — 다-항(multi-term) 모델 (에이전트 조사로 정정)

⚠ **정정**: 처음 쓴 단일 `S=coverage_ref/coverage`는 **불완전**.  전이성 에이전트가 문헌에서
**"순수 1/coverage는 아니다"**(Samsung trade-off, §4)를 확인 → **항을 분리**해야 옳다:

```
R_int(config, N) = R_contact(coverage,P) + R_tort(τ,ε) + R_chem(N) + R_collector(N) [+ Δ_special]
                   └── 우리 OUTPUT ──┘   └ 우리 OUTPUT ┘  └ 문헌 shape ┘ └ 문헌+우리셀 ┘  └ 실측 ┘
                     Holm 접촉 (∝a⁻¹)    pore-τ 병목    계면반응 R_ct    집전체 접촉    SDCP
```

- **R_contact(coverage,P)** = 계면 수축(constriction) 접촉 저항.  **ASR ∝ (접촉면적)⁻¹**(Holm), 압력 **∝ P⁻⁰·⁵**.
  MAGNITUDE = **우리 DEM/MPM coverage OUTPUT** + Stage-E 접촉면적.  (전극/LPSCl 직접 측정: `acsenergylett.5c00032`)
- **R_tort(τ,ε)** = 벌크/GB/tortuosity 병목.  MAGNITUDE = **우리 pore-τ OUTPUT**.  ★ coverage와 **반대로** 움직임
  (미세입자 → coverage↑지만 τ↑) → 총 R_int **비단조**.  (Samsung `acsami.4c01322`)
- **R_chem(N)** = 화학 interphase 전하전달 R_ct의 사이클 성장 (§3).  SHAPE = 문헌, LEVEL = **우리 랩 kim2025**.
  형태-클래스(단결정/다결정)별로만 공유.
- **R_collector(N)** = 집전체|Al 접촉 (§3.3).  pristine 문헌 + 성장 shape 문헌 + **우리 셀 endpoint(18→110 등)**.
- **Δ_special** = SDCP 등 특이재료 **실측 delta** (§5).

**"bimodal 여러 config"가 정직하게 커버되는 이유**: 문헌은 *모양*(공통)만, *크기*는 우리가 config마다 이미
뽑는 **coverage AND pore-τ 두 OUTPUT**으로 계산 → 미세입자 trade-off(비단조)까지 자체 지표가 잡음.
날조·보간 없이 새 config(bimodal)로 확장.  SDCP만 예외적 실측 delta.

## 3. Reference 성장-법칙 — 형태 + 앵커

### 3.1 R_chem(N) 형태 — 양극에 따라 갈림 (문헌 합의)
```
R_chem(N) = R_ct,0 + ΔR_form·𝟙(N≥1) + g(N)
  R_ct,0    : pristine R_ct (조성의존, kim2025)
  ΔR_form   : 첫-충전 점프 (interphase 대부분 1st charge — Koerver 2017)
  g(N)      : 완만 성장 — CAM 결정형에 의존:
              · coated/단결정  → √N  (확산-제한 interphase 두께; Pinson-Bazant √t·CEI)
              · bare/다결정    → ~선형 k·N  (균열+접촉손실이 매 사이클 새 반응면 노출; Conforto PC≫SC)
              (포화-지수는 √N/첫점프의 포락선일 뿐 별도 기전 아님)
```
- 첫-충전 dominant: Koerver 2017 (`chemmater.7b00931`), confirmed_snippet.
- √t(확산-제한 필름): Pinson-Bazant JES 2013 (`arXiv:1210.3672`) — "한 개 파라미터 √t", confirmed_snippet.
- 선형 contact-loss: JES 2017 (`10.1149/2.0481711jes`) "capacity ∝ 접촉면적손실, slope~1", confirmed_snippet.
- 일반 사이클: ~20%/1000cyc 선형 후 >800cyc 비선형 가속 (`app152412875`), confirmed_snippet.
- ⏳ **g(N) √N-vs-선형 판별계수 = Conforto 2021 per-cycle R_ct 테이블 (WSL PDF)** — 아직 gap.

### 3.2 절대 앵커 (LEVEL)
★ **최고 앵커 = 우리 랩 자체 (kim2025, `pdf_verified`, litdb/papers/kim2025_impedance_decoupling_tlm_assb.md)**:
| 양 | 62/72/82 wt% NCM811 | 조건 | precision |
|---|---|---|---|
| **R_ct (bare NCM811/LPSCl, full cell)** | **453 / 290 / 382 Ω·cm²** (Table S6) | uncoated, 30°C | **pdf_verified** |
| **R_ct (LNO-coated, full cell)** | **22.4 / 18.2 / 17.2 Ω·cm²** (Table S4, ~20× 낮음) | coated, 30°C | **pdf_verified** |
| R_ct(uncoated) vs T | 30→45→60°C = **289.9→139.6→67.8** | 72wt%, Arrhenius | **pdf_verified** |
| R_ion / C_dl / Warburg 동시분해 | (Table S3–S6) | 대칭+3전극 | **pdf_verified** |
- ★ coated R_ct가 CAM면적↑(82wt%)서 **최저** = **R_ct ∝ 1/반응면적 = coverage-스케일 자체 실측 지지.**
  단 uncoated는 **비단조**(72 최저) = 화학분해항 지배 → §4 "화학항은 coverage-스케일 대상 아님"과 일치.

기타 문헌 앵커(confirmed_snippet):
| 양 | 값 | 조건 | 출처 |
|---|---|---|---|
| pristine SC 계면 바닥 | ≈40 Ω·cm² | SC-NMC/LPSCl 0.2MPa 30°C | acsami.1c07952 |
| 압력 민감도(약함) | 127.6→109.1 Ω (17×P→17%↓) | SC-NMC532/LPSCl | Naik 2025 aenm.202403360 |
| SC vs poly R_ct | SC ≈40% 낮음 (단 6–14× 확산 일부기여) | bimodal 논문 | acsenergylett.5c03923 / Trevisanello 2021 |

### 3.3 R_collector(N) — 집전체 접촉 (문헌 shape + 우리 셀 level)
- pristine: **bare Al ≈10–18.5 Ω·cm² / coated ≈3.5–10 (~5×, 황화물서 5–10×)** (confirmed_snippet).
- 성장 shape: **첫-사이클 step + ~선형 k·N** — Pritzl 2019 (`10.1149/2.0451904jes`): R_contact **≈10(형성)→≈30(50cyc)**
  (~3×), HF passivation + 코팅 delamination.  우리 endpoint(SBE 18→110, DBE 12→46, C-SUS 10→30 @1000cyc 2C)
  = Pritzl contact-loss 영역과 정합(~3–6× rise).
- Al/C 화학안정(argyrodite): SS/Ni/Al/Al-C 안정, Cu/Li 부식 (Nat Commun Chem 2025).

## 4. 전이성 — 성립·한계 (정직, 에이전트 검증)
**성립(coverage 항)**: 전극/LPSCl **ASR ∝ 접촉면적⁻¹**(지수 −1, Holm) + P⁻⁰·⁵ — 직접 측정
(`acsenergylett.5c00032`).  fine-LPSCl R_ct < coarse (Zhou 2025 `acsenergylett.4c03256`, 방향만).
**★ break(순수 1/coverage 아님)**: Samsung `acsami.4c01322` — **CAM 입자↓ → R_ct↓지만 GB/tortuosity 저항↑
→ 총 R_int 비단조**.  = 두 경쟁 항(계면 ∝a⁻¹ ↔ 벌크/τ 반대) → **coverage 하나로 못 잡음** → §2 R_tort 분리 근거.
(우리 σ_thermal multi-pathway 발견과 동형.)

**over-generalization 경고 (무비판 이식 금지, 에이전트 7항 요지)**:
1. √t·"rate∝1/접촉면적"은 **anode(Li/LPSCl) 결과** → cathode CEI에 그대로 X.
2. −1·−0.5 지수는 **이상화 constriction 모델** → 계면항에만, 벌크 τ는 별도.
3. magnitude는 조건-고정(chemistry/areal/T/P) → 이식 금지.
4. LLZO 0.2 Ω·cm²는 Li|garnet → cathode에 절대 X.
5. SC −40% R_ct는 일부 **본질 확산(6–14×)** 기여 → 전부 coverage 몫 아님.
6. CEI √t rate는 chemistry/전압/T가 결정 → 조성·컷오프 넘어 이식 X.
7. 압력 민감도 mid-range 약함(17×P→17%) → 저압 곡선을 접촉면적만으로 고압 재스케일 X.
→ **R_ref shape는 같은 chemistry·CAM결정형 클래스 안에서만 공유; magnitude는 config별 우리 coverage+τ로.**

## 5. SDCP / 특이 케이스 = 실측 delta
- SDCP는 혼성전도 배달부 → 표준 VGCF/PTFE 문헌 reference로 안 잡힘 → **사용자 실측(배영진 펠릿/필름/cell EIS)** 로
  Δ_special / override.  E_bind DFT(gabia)가 물리 근거.
- 우리 endpoint(SBE/DBE/C-SUS 18→110 등) = **user-lab 측정앵커** — R_collector의 절대 스케일을 우리 셀에 고정.

## 6. 두 시간-일관 시나리오 (σ_apparent MIX 해소)
- **pristine (fresh+fresh)**: BOL 구조 + pristine R_int/R_collector(~18/12/10) = R(N=0).
- **cycled (aged)**: 별도 "노화 시나리오" 라벨 + post-cycling(110/46/30) = R(N=large).
현재 σ_apparent = fresh 벌크 + aged 계면 MIX(§project 6.1)을 이 분리로 교정.  R(N)이 두 끝점을 문헌 shape로 연결.

## 7. step4_dyn 배선 — ★ 문헌이 우리 split을 정당화
**핵심(에이전트3)**: 표준 DFN/Newman = 셀V = OCV + **BV 전하전달 과전압(i₀)** + **옴성 강하(직렬 R_film)**.
필름/집전체 = 옴성 저항 → 직렬 ASR (η=i·R), 반응 = BV i₀ — **정확히 우리 `V_term=V_cell−I·R_int` + BV i₀.**
- ★ ASSB-특화 근거: **Choi 2024 `acsami.4c01322`** — 복합양극 계면임피던스 = **r_i,gb + r_i/e**
  (옴성 접촉/GB 항 ↔ 반응 항) → 집전체/필름=**직렬 옴성 `--r-int-ohm-cm2`**, 반응계면(AM|SE, AM|SDCP)=**BV i₀** 분리 정당화.
- 계수 앵커: k_SEI = **1×10⁻¹² m/s** (PyBaMM Chen2020, confirmed_snippet).  ASR 정규화: 단일계면 **ASR=R·A**,
  대칭셀 **R·A/2**.
- 배선 = DB 값을 `--r-int-ohm-cm2`/`--asr-film`로 주입 + 출처 태그.  전극-내부(R_int=0) 기본 유지, 풀셀 축은 명시 옵션.

## 8. §F1 정직 원장
| 입력 | 종류 | 근거 |
|---|---|---|
| R_geom (기하 집전체) | **OUTPUT(모델)** | SBE 1.37e-5 / DBE 9.05e-6 Ω·cm² |
| coverage→R_contact, pore-τ→R_tort | **OUTPUT(모델)** | DEM/MPM Stage-E 접촉면적 + pore-τ (지수 −1, P⁻⁰·⁵) |
| R_ct,0 level·조성의존·T (453/290/382, 22/18/17) | **측정(우리 랩)** | kim2025 pdf_verified |
| R_chem(N) 첫점프+g(N) 모양 | **측정앵커(문헌)** | Koerver/Conforto/Pinson-Bazant, snippet |
| R_collector level·성장 shape | **문헌+우리 셀** | Pritzl snippet + 우리 endpoint |
| ohmic-ASR vs BV-i₀ split | **측정앵커(문헌)** | Choi 2024 / DFN-Newman |
| SDCP Δ_special | **user-lab 측정** | 배영진 EIS (대기) |
| g(N) √N-vs-선형 계수 | **assumed-form (라벨 필수)** | Conforto per-cycle fit 전까지 = 모델 |

## 9. GAP (닫으려면 필요)
- ⏳ **Conforto 2021 per-cycle R_ct 테이블(SC vs PC) — WSL PDF** → g(N) √N-vs-선형 + 첫점프 계수 확정.
- ⏳ **Choi 2024 `acsami.4c01322` r_i,gb/r_i/e 식·수치 — WSL PDF** → ASR 정규화 + 2-항 분리 정량.
- ⏳ **MDPI Inorganics 2025 14(7):180 (open access, 403만 걸림) — WSL** → DRT 5-성분(계면 vs τ) 분리.
- ⏳ O'Kane 2022 SI(k_SEI,D_SEI,β,m2) + LiionDB i₀/D_SEI (WSL/liiondb.com).
- ⏳ pristine 집전체 EIS(사이클 전) + 중간-사이클 EIS → 궤적 직접앵커(없으면 √N/선형 라벨).
- ⏳ SDCP E_bind DFT (gabia) → Δ_special.

## 10. 상태
- 2026-07-20: 설계 확정 (3-에이전트 조사 반영).  **다-항 모델**: R_contact(coverage⁻¹)+R_tort(pore-τ)+R_chem(N)+
  R_collector(N)+Δ_special.  reference=문헌 SHAPE / magnitude=우리 coverage+τ / level=kim2025(우리 랩) / SDCP=실측.
  ohmic-vs-BV split = Choi2024/DFN 문헌 정당화.  **잔여 = WSL PDF 디지타이즈(Conforto/Choi/Inorganics)로 계수 확정.**
