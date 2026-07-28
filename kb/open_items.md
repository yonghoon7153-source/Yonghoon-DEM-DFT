# 미결 리스트 (Open Items)

> 세션이 바뀌어도 유지되는 미결 사항 추적. 닫을 때 날짜+근거를 남기고 ✅로 옮긴다.
> 등록: 2026-07-27 (MAX 감사 후속).

## 🔴 판정 대기

### 1. modelc(LPSCl1.6) MD Ea 정본 — 0.2235(단일 deck) vs 0.197±0.032(3-seed)
- **상태**: OPEN. 양쪽 파일(comp2_md_arrhenius.json ↔ b2o3_vs_lpscl16_conductivity.csv)에
  충돌 블록 + "확정 인용 금지" 표기됨 (MAX 감사 discipline-6).
- **통계적 사실**: 0.2235 ∈ [0.165, 0.229] = 3-seed 1σ 구간 안 — **물리적 모순이 아니라
  '어느 프로토콜 값을 인용하나'의 충돌**이다. 임시 규칙: 조성 간 비교는 같은 시드
  프로토콜끼리만 (단일 deck: comp1 0.253 ↔ modelc 0.2235 / 멀티시드: modelc 0.197±0.032
  ↔ b2o3 0.199±0.034 ↔ LPSOCl 0.271±0.033).
- **닫는 방법 (판정 2026-07-27): AIMD 불필요.** 이유:
  1. 충돌이 UMA 내부(시드 통계) 문제라 AIMD는 질문이 다르다 — AIMD 1궤적을 추가하면
     같은 ~15% 시드 잡음을 가진 **제3의 값**이 하나 늘 뿐, 통계 충돌은 그대로다.
  2. 비용 비대칭: AIMD 3-T Arrhenius(52at, 각 ≥100 ps)는 주 단위 / UMA 시드 추가는 시간 단위.
  3. 우리 규율상 MLIP 절대값은 어차피 인용 금지 — 절대 정확도가 걸린 항목이 아니다.
  → **정공법 = comp1 멀티시드 보강**: comp1 600/800/1000 K × 추가 2 seed (6 run,
  ~15 h GPU, gabia disorder 캠페인 종료 후). 전 조성이 멀티시드로 통일되면
  0.197±0.032를 modelc 정본으로 확정하고 단일 deck 앵커는 SUPERSEDED 처리.
  UMA 자체 검증이 필요해지면(리뷰어 요구 시) full AIMD가 아니라 **UMA 궤적 스냅샷
  DFT single-point 스팟체크**(힘/에너지 상관)로 족하다.

### 2. comp2 disorder ensemble — Ea 0.087(cfg0) 아티팩트 여부
- cfg0 600 K MSD가 확산 영역인지 log-log 기울기(≈1) 확인 전까지 **인용 금지**.
  600→1000 K에서 D 2.0×(0.276 eV라면 8.5× 기대)라 케이지 잔류 의심.
- cfg1/cfg2 완료 후 config 산포로 판정 (단일 config 판정 금지 규율).

### 3. VGCF 2×2 barrier 행렬 — kgy NEB 체인
- Li_in_gallery_gr2L(2L|1L) → Li_in_gallery_2L(1L|2L) → Li_on_graphene_2L 진행 중.
- 완료 시: 209 meV 층수 효과의 VGCF/h-BN 몫 분해 + 2L 수렴 판정 + 기준선 층수 정합.
  결과에 따라 "gallery가 표면보다 ~2× 빠름" 문구의 배수 재계산.

### 4. SDCP complex_doped_v2 DFT relax — k 2×2×1 재실행 수렴 여부
- k 1×1×1 정체(150 iter, 0.0837 Ry) → 2×2×1로 재시작. accuracy가 0.08을 뚫고
  내려가는지 확인 필요. VRAM 46.9/48 GB로 임계 (OOM 시 diago_david_ndim=2).
- reference_dft(절대 binding 기준)는 0 ionic step이라 from-scratch 별도 결정 필요.

### 5. h-BN 시트 굴곡 0.27–0.37 Å (vgcf_hbn_neb.json flag_hbn_corrugation)
- 자유 h-BN 단층은 <0.01 Å 평면이어야 정상. Li-유도 pucker인지 4×4 셀 리플인지
  relax 미완인지 미해결 — h-BN 표면 수치(7 meV) 정량 인용 전 확인.

## 📄 PDF 확보 대기 (원전 미보유 — 웹/재인용 딱지 상태)

| # | 서지 | DOI | 왜 필요한가 |
|---|---|---|---|
| ~~1~~ | ✅ **확보·다이제스트 완료 (2026-07-28)** de Klerk et al. | 10.1021/acs.chemmater.6b03630 | digest: deklerk2016_diffusion_site_disorder_argyrodite.md — 75%는 min-rate 지표·비단조·단일 배열이었음이 판명. ✅ SI 통합 완료(2026-07-28) — Tables S1-S3 전표 수록, figure-read 값 SI 정밀값으로 교정(75/50 비 1.99x 확정, 300K σ* Cl 최대 교정) |
| 2 | Adeli et al., Angew. Chem. Int. Ed. 58, 8681 (2019) | 10.1002/anie.201814222 | Li5.5PS4.5Cl1.5 실험 원전 (9.4 mS/cm) — modelc Cl-rich Rietveld 점유율 ground truth |
| 3 | Deng, Wang, Chu, Luo, Ong, J. Electrochem. Soc. 163, A67 (2016) | 10.1149/2.0061602jes | SQS 반례 원전 (A=0.92) — ordered_vs_disordered 문서 '경계 사례' 논증의 원본 |
| ~~4~~ | ✅ **확보·다이제스트 완료 (2026-07-28)** Kim et al., Nano Energy 124, 109436 | 10.1016/j.nanoen.2024.109436 | **신규성 판정 완료**: enumerate 6 특성배열+단일 random supercell, config-분산 오차막대 **없음** → 우리 다중 config×멀티시드 산포 보고는 신규 기여로 원고 기재 가능 (digest: kim2024_mtp_argyrodite_disorder_gb.md) |
| ~~5~~ | ✅ **확보·다이제스트 완료 (2026-07-28) — 단 귀속 오류 판명** Schlem et al. AEM 1903719 | 10.1002/aenm.201903719 | 실물 = **Li3MCl6(Y,Er) 기계화학 논문, LPSCl 데이터 0건** → 'ordered 0.25' 앵커 철회, li_transport 정정 완료. '무질서=공정변수'의 최정밀 외부 실증(Er 무질서 88→2.5% 연속 조절)으로 가치 전환. **신규 미결: LPSCl 0.25/0.22의 진짜 원전 추적** (후보: Schlem 2019 계열 argyrodite 논문 — 서지 확인 필요) |
| (6) | Kim rapid-thermal (10.2 mS/cm, liu2022 재인용) | liu2022 참고문헌에서 확인 | 공정–무질서 관계 보강 (우선순위 낮음) |

확보 시 "논문 에이전트"(litdb-curator)로 다이제스트 → 서베이 ⚠딱지 승격.
진행: #1 de Klerk·#2 Adeli·#3 Deng·#35쌍·#36쌍(Schlem 추정) — 2026-07-28 큐레이터 5기 가동.

### 스크리닝 방법론 논문 위시리스트 (지도 피드백 "co-doping screening develop" 지원)

| # | 서지 | DOI | 왜 |
|---|---|---|---|
| S1 | Xiao, Wang, Ceder et al., *Joule* 3, 1252 (2019) "Computational screening of cathode coatings" | 10.1016/j.joule.2019.02.006 | **cascade의 직계 조상** — 양극 코팅 HT 스크리닝의 표준 프레임 (안정성+ESW+수송 게이트) |
| S2 | Zhu, He, Mo, *ACS Appl. Mater. Interfaces* 7, 23685 (2015) | 10.1021/acsami.5b07517 (구기재 5b01004는 오기 — PDF 실물 확인) | **grand-potential ESW 방법 원전** — 우리 oxidation CSV가 쓰는 바로 그 방법 |
| S3 | Richards, Ong, Ceder et al., *Chem. Mater.* 28, 266 (2016) "Interface stability" | 10.1021/acs.chemmater.5b04082 | pseudo-binary 계면 반응성 — MLIP 캠페인 ①(Li\|SE)의 열역학 짝 |
| S4 | Sendek et al., *Energy Environ. Sci.* 10, 306 (2017) "12k candidates" | 10.1039/C6EE02697D | **ML 스크리닝 대표작** — TabPFN 노선의 선행, 발표 인용 앵커 |
| S5 | Kahle, Marcolongo, Marzari, *EES* 13, 928 (2020) HT-AIMD 스크리닝 | 10.1039/C9EE02457C | AIMD 기반 HT의 방법 규율 (수렴·통계) — 우리 MD 규율과 대조 |
| S6 | Fujimura et al., *Adv. Energy Mater.* 3, 980 (2013) | 10.1002/aenm.201300060 | ML×전도도 예측의 원조 — 역사 앵커 |
| S7 | Ong et al., *EES* 6, 148 (2013) Li₁₀±₁MP₂X₁₂ family | 10.1039/C2EE23355J | 조성족 치환 스크리닝 원형 (LGPS M/X 스캔) |

## 🧠 ML 후속 (트리거 대기 — 데이터 나오면 전체 진행)

> 랩 PPT(TabPFN) 판독에서 나온 계획: kb/projects/ml_opportunities_from_lab_ppt_2026_07.md.
> 각 항목은 **트리거 조건**이 충족되면 착수한다.

### M1. TabPFN 벤치 — codoping 비선형 타깃
- **트리거**: 없음 (지금 가능 — 로컬 WSL/kgy GPU 반나절).
- 내용: champions Δe_post_anneal · litransport bvs proxy를 조성 특징에서 TabPFN으로
  예측, 현행 numpy ridge와 LOOCV 성능표 비교 → 사이트 ML 탭에 병기.
  근거: litdb hollmann2025 (≤10k행/500특징 스윗스팟, 튜닝 0).
  + [Sendek17 선례 이식] X-randomization(랜덤 대비 농축배수로 보고) + cR²_p
  유의성 — 소표본(그들 40 ≈ 우리 47) 정직성 지표의 인용 선례 확보.

### M2. pair CV를 leave-one-dopant-out으로 (codoping_ml v2.1)
- **트리거**: 없음 (코드 수정만).
- 내용: 같은 도펀트를 공유하는 쌍(A–B, A–C)은 비독립 — pair 단위 CV는 누수.
  랩 PPT의 Group-CV 관행 대조에서 발견한 우리 구멍.

### M3. TabPFN 역설계 루프 1회전 → 첫 실측 라벨
- **트리거**: M1 완료 + gabia GPU 여유 (comp1 seeds 종료 후).
- 내용: 가상 후보(1081쌍 × 농도축) TabPFN 스코어링 → 불확실성 페널티로 상위 5쌍
  선별(winner's curse 완화 — [Sendek17]의 적용영역 d/ε/A 3지표가 기성 구현체,
  P_LR vs d 그림 양식 그대로 이식) → UMA 공동치환 슈퍼셀 검증 = codoping 첫 라벨.
  mlip_next_campaigns ①(Li|SE 계면)과 후보 공유.

### M4. disorder 서러게이트 (active learning)
- **트리거**: disorder ensemble d×cfg 표본 ≥ 9 (현재 3). ~~Kim 2024 PDF~~ ✅ 확보 완료(2026-07-28) — 기술자 설계 시 그들 E_rel·Boltzmann 가중 방식 참조 가능.
- 내용: 배열 기술자(anti-site 분포·Ewald·BVS 채널%) → D 예측, 다음 cfg 선택에 사용.

### M7. MD 프로토콜 업그레이드 2건 (Kahle 2020 이식)
- **트리거**: comp1 멀티시드 수확 시 함께 적용 (코드 반나절).
- 내용: ① MSD 피팅창 t'-스캔 1회 검증(우리 2-50 ps 고정창이 창 길이에 둔감함을
  데이터로 입증 — Kahle Fig S3 양식) ② Ea에 Bayesian 오차 전파(현행 시드 std 보완).
  근거: kahle2020 digest §3 — per-material 자동 수렴판정·블록 분산 SE의 원전.

### ~~M6~~. ✅ cascade 양극 반응성 게이트 (2026-07-28 완료 — 결과 회수 대기)
- **검증 통과**: 닫힌계 pseudo-binary ΔE_rxt로 LPSCl/LCO **만충 −322.7 (Xiao −339, 0.95×) /
  반충 −454.9 (−493, 0.92×)**, 리튬화 순서(반충이 더 발열)까지 재현.
  반응식도 `Li₂S + Li₃PO₄ + Co₉S₈` 로 물리적으로 타당.
- **교훈(기록용)**: 초판을 개방계 `GrandPotentialInterfacialReactivity` + 전위 스캔으로 짰다가
  −810~−1544 meV/atom 이 나왔고, V=4.30 반응식이 `Li6PS5Cl -> 6 Li + SCl + 0.5 P2S7 + 0.5 S` 로
  **양극이 아예 빠진 자체분해**였다. Li 저장소를 열면 코팅 탈리튬 분해가 상호반응을 압도한다.
  xiao2019 digest 227번 줄이 ΔE_rxt를 "**닫힌계**"로, 222번 줄이 만충/반충을 **조성 축**으로
  명시하고 있었다. → **개방계는 Li 음극 쪽 도구, 양극 F4 게이트는 닫힌계**.
- **전수 완주**: 47 코팅 × {LiCoO₂, Li₀.₅CoO₂} = **94쌍** (gabia, 2026-07-28).
- **남은 것**: gabia의 `db/properties/cathode_reactivity_cascade.csv` 를 repo로 회수 →
  cascade 깔때기에 **G6 계면 반응성** 게이트로 조인. 판정 기준은 "몇 종이 100 meV를 통과했나"가
  아니라 **"host LPSCl(−323)보다 계면 반응성이 완화되는 코팅이 있는가"** (S1 성공조건 ②).
  ⚠ 컷 근처 ±20 meV 순위 주장 금지 (Xiao 100 meV는 관례컷 + Sundar 2025의 "분해산물 전자전도도
  미고려" 비판을 그대로 받음).

### M5. P2D 물성 export 인터페이스 (랩 P2D 데이터셋과 동기화)
- **트리거**: 랩 후막 전고체 P2D 데이터셋 스키마 확정 (다음주 랩 계획).
- 내용: db/properties(σ·E·ESW)를 P2D 입력 파라미터 포맷으로 내보내는 export —
  DFT(우리)→P2D(랩)→TabPFN 멀티스케일 연결. ⚠ σ는 MLIP 상한임을 명시 필수.

## 🎤 심포지엄 대응 (2026-07-28 신설 — T1–T8)

전지기술 심포지엄 2026 기술세션 3-3(이상욱, 성균관대) · 3-4(문장혁, 중앙대) 덱 분석에서 나온 실행 항목.
전체 근거·좌표는 **`kb/projects/symposium_2026_competitive_analysis.md`**,
digest는 `litdb/talks/`, 벤치마크 수치는 `db/properties/external_benchmarks_symposium_2026.json`.

| ID | 항목 | 왜 (우리 약점/기회) | 비용 | 우선 |
|---|---|---|---|---|
| **T1** | **UMA 외삽 대리지표 설계** (재정의 2026-07-28) | 우리 MLIP-MD는 **스냅샷 수준 외삽 판정이 전무**하다. ⚠ 이상욱 랩의 γ(=γ_select 2 / γ_break 10→5→2)는 **MTP 선형 기저 위 maxvol·D-optimality 정의라 UMA(비선형 등변 GNN)에는 정의 자체가 없다** — 숫자 이식 불가. 이식할 것은 논리뿐: ①대리지표 하나 정한다 ②**선별 문턱과 중단 문턱을 분리** ③중단 문턱을 조여 수렴 판정. 후보 대리지표: 궤적 스냅샷 UMA vs DFT 단일점 오차 분포 / 앙상블 분산 | 중 | **1** |
| **T7** | **3계층 스킬 로딩** (Level 1 YAML 메타 ~100토큰 신설) | 우리는 Level 2만 있다(CLAUDE.md + tools/). 매 세션 전체를 훑는 구조적 이유 | 소 | **1** |
| **T2** | **ICOHP 기반 P–S 약화 기술자** | `air_hsab` 정성 tier를 정량으로. 그들은 양성자화 시 ICOHP −6.43 → −4.69 eV (27% 약화) | 중 | 2 |
| **T4** | **반응좌표 기반 검증셋** | pre-mixing→reactants→TS→products 단계별 UMA vs DFT 단일점. 학습이 아니라 **검증**으로 전용 | 소 | 2 |
| **T5** | **영역분해 MSD** | 계면/벌크 구획 마스크로 D 분리. 기존 파이프라인 확장만 | 소 | 2 |
| **T3** | **Li\|LPSCl 반응 MD (UMA)** — 프로토콜 확정 | 완전 공백 축. **셀** Li(100)‖LPSCl(100) 직접접촉, 횡단면 ~3 nm², Li 6 nm ‖ LPSCl 10 nm (~7,000원자), NVT **350 K**, **≥20 ns**. ⚠ **우리 표준 200 ps로는 결정 핵생성(11 ns)을 절대 못 본다 = 결과가 없다.** 비용 초과 시 [두께 절반 + 20 ns] > [두께 유지 + 2 ns]. **1순위 관측량은 D가 아니라 잔존 PS₄ 층수 vs 시간**(z-bin + P–S 거리컷). 착수 전 게이트: 1 ns UMA MD → 20 ps 스냅샷 → QE 단일점 대조 (UMA는 Li 금속‖황화물 반응 영역에서 검증된 적이 없다 — Li₃N 편향 전례). 벤치마크: interphase ~11 nm · Li₂S 결정화 · D비 0.36 | 대 | **2** |
| **T8** | **P2D 파라미터 export** (=M5) | 문장혁 랩 발표로 **소비자가 특정됨**. 우리가 파라미터 생산, 그들이 셀 스케일 소비 | 중 | 3 |
| **T6** | **litdb 그래프층** | 멀티홉 가설 생성 부재. digest **위에** 얹기(대체 아님) — 방법 맥락·인용금지 규칙 보존이 조건 | 중 | 4 |

**하지 않기로 한 것**: CSP(문제설정 다름) · 자체 MLIP 학습(UMA 횡단 속도가 우리 강점) ·
셀 스케일 FEM(상하류 관계 유지).

### T9–T12 — 이상욱 랩 논문 실물에서 추가된 항목 (2026-07-28)

| ID | 항목 | 근거 (논문 실물) | 비용 | 우선 |
|---|---|---|---|---|
| ~~**T9**~~ | ✅ **완료 (2026-07-28)** — 계면 상대 5종 {양극 만충/반충, **SE(LPSCl)**, **Li 음극**, LiNbO₃ 대조} 47종 전수 | **M6의 'vacuous' 판정을 우리 데이터로 확정 반증.** 축별 탈락: 양극 만충 **2** · 반충 **3** · **SE 29** · **Li 음극 35** · LNO 4. 코어 생존자 **11 → 3종**(CaF₂·LiF·MgO). 앵커 재현도 정확 — LPSCl vs Li −541.5 (Lee 2024 Li₆PS₅I −539.2, 0.4% 차) · vs LNO −108.8 (−107.5, 1.2%). 상세: **판정 이력 V1** | — | ✅ |
| ~~**T10**~~ | ⛔ **폐기 (2026-07-28)** — E_hull 필터가 우리 풀에서 무력 | **예측이 빗나갔다.** hull ≥ 50 meV 탈락 **0종**(최대 CrO₃ 46, 나머지 ~0). 원인은 기준이 아니라 **풀**이다 — 47종이 애초에 안정한 흔한 이성분 화합물로 큐레이션돼 있어 어떤 열역학 안정성 기준도 통과한다. → 음성 결과를 `pool_provenance` 논증의 **정량 근거**로 전환. ⚠ '안정성이 안 중요하다'가 **아니다** — 발견 깔때기(Kim 2026은 ECW에서 94.3% 제거)에선 압도적으로 센 게이트고, 우리 풀은 그 단계를 이미 통과한 상태에서 시작할 뿐. 상세: **판정 이력 V2** | — | ⛔ |
| **T11** | 🔶 **부분 완료 (2026-07-28)** — pseudo-binary ΔE_H₂S 47종 계산됨 | 최악군이 전부 알칼리·알칼리토 산화물(Na₂O −192 · BaO −160 · SrO −116 · Li₂O −108 · CaO −74 meV/atom)로 화학적으로 타당. 불화물은 전부 0 근처. Li₂O·CaO는 SE 축에서도 탈락 = 두 축이 같은 화학을 다른 각도에서 본다. **⚠ 남은 것: host LPSCl 자체의 ΔE_H₂S 기준선** — 없으면 '개선인지'를 말할 수 없다. ⚠ 이상욱 랩 반응 MD(SevenNet 500 ps, ICOHP, Sn 유인)와 **같은 것이 아니다**(0 K 열역학 vs 동역학) | 소 | **1** |
| **T12** | **van Hove 상관함수** MSD 파이프라인 추가 | Lee 2024 Fig 3e: "cage에 갇힘 vs 자유 확산"을 MSD 기울기가 아니라 **거리–시간 지도**로 판별. 우리 disorder_ensemble의 "ordered frozen" 판정을 선명하게 | 소 | 2 |

> 🔑 **T9·T10·T11은 셋 다 비용이 작고 셋 다 우리 깔때기의 약점을 직접 친다.** M6 인프라를
> 그대로 재사용하므로 묶어서 한 번에 돌리는 것이 맞다.

### ⚠ σ 절대값 규율 — 근거 재정의 (2026-07-28)

지금까지 "MLIP σ 절대값 인용 금지"의 근거는 `kim2024`(훈련 functional에 따라 σ₈₀%가 **8배** 갈림)
하나였다. `lee2024` ESI Table S1이 **반대 방향의 데이터**를 준다:

| 조성 | AIMD | MTP_optB88 | 실험 |
|---|---:|---:|---:|
| Li₆PS₅I | 0.84 | **0.001** | **0.001** |
| Li₆PS₅Cl | 4.6 | **2.46** | **2.3–2.5** |
| Li₃YCl₆ | 14 | **0.56** | **0.51** |

**optB88-MTP는 8개 계에서 실험과 잘 맞고, 크게 틀리는 쪽은 AIMD다**(Li₆PS₅I에서 840배).

→ 정확한 명제: **"MLIP σ 절대값은 (a) 훈련 functional이 그 계에 맞고 (b) 같은 물질군에서
실험 검증을 거친 경우에만 신뢰할 수 있다."**
**우리 UMA는 둘 다 미충족**(OMat24 = PBE 계열이라 optB88 아님 · 우리 계 실험 대조 없음)
→ **인용 금지 규율 유지. 단 이유가 "MLIP는 원래 못 믿는다"가 아니라 "우리 설정이 검증되지
않았다"로 바뀐다.** 규율이 약해지는 게 아니라 정확해지는 것이고, **T1의 필요성이 커진다**.

### 이상욱 랩 논문 확보 위시리스트 (사용자가 탐색·제공 예정)
| 순위 | 논문 | 왜 |
|---|---|---|
| 1 | **Nano Convergence 2026, 13, 27** — 코팅 스크리닝 (17,233 Li-P-S-O) | 우리 cascade/M6의 **직접 대조군**. S6 감사가 대기 |
| 2 | **Adv. Funct. Mater.** (revision) — argyrodite 가수분해 SevenNet | T2 방법 원본 |
| 3 | **Chem. Eng. J.** (under review) — Li\|argyrodite 계면 MTP | T3 프로토콜 원본 |
| 4 | JACS 2025, 147, 47381 — 준안정 3기술자 | metastable 고찰 보강 |
| 5 | **Adv. Energy Mater.** (revision) — Dynamic properties 후속 | **Q5: config-variance 오차막대 추가됐나** — 우리 신규성 주장의 유효범위가 걸림 |
| 6 | Rare Metals 2025, 44, 2366 | CSP 보조 |
| 7 | arXiv:2601.04746 — BEARS 스킬 3계층 | T7 실측치 |

### 🔁 판정 정정 이력 (우리가 냈다가 뒤집은 판정)

웹앱 **`/benchmarks` → 판정 정정 이력**에 ①주장 →②무엇이 틀렸나 →③어떻게 알았나 →④지금 무엇을 아나
형식으로 전문 수록. 여기엔 색인만 둔다.

| ID | 무엇을 뒤집었나 | 근거 |
|---|---|---|
| **V1** | M6 계면 게이트 'vacuous' 판정 철회 — 가장 쉬운 상대(양극)만 계산한 결과였다 | Kim 2026 Table S1 + 우리 T9 전수 |
| **V2** | T10(E_hull) 예측 빗나감 — 원인은 기준이 아니라 큐레이션된 풀 | 우리 T10 전수 (음성 결과) |
| **V3** | σ 규율 근거 재정의 — kim2024만으론 절반. AIMD가 840× 틀리는 쪽이다 | lee2024 ESI Table S1 |
| **V4** | T1을 'γ 확보' → 'UMA용 대리지표 설계'로 재정의 — γ는 MTP 전용이라 정의 자체가 없다 | kim2026 SEI 실물 |

> 📌 **덱 정정 원장(외부 6건)과 나란히 둔다.** 한쪽만 있으면 정직성이 아니라 남 탓이 된다.

### 🧪 T1 진행 — 모델 위원회 (UMA + MACE-MP-0 + SevenNet-0)

- 도구 `tools/ionic/mlip_committee.py` (sample → predict×3 → analyze). **새 MD 불필요**, 기존 궤적 후처리.
- 문턱은 임의 상수를 만들지 않고 **표본 분포에서 유도**: 선별 = 중앙값×2 · 중단 = p95.
  (kim2026의 γ_select/γ_break **논리 구조만** 차용)
- 기준선 대상: `/data/work/b2o3md/modelc_full/d0.00_cfg0/T600/traj.xyz` (2000 프레임 × 62원자).
- **CPU 실행** — comp2 disorder MD가 GPU를 쓰고 있어 충돌 회피. 단일점만 하므로 CPU로 충분.
- ⛔ **이 지표는 절대 정확도를 말하지 않는다.** 세 모델이 전부 PBE 계열이라 V3의 functional 각인
  문제를 풀지 못한다 — **일치해도 절대 σ 인용 금지는 그대로**. 재는 것은 "이 배열이 훈련 분포에서
  이상한가"뿐이고, 그 목적에는 같은 functional 계열인 것이 오히려 무해하다.
- **✅ 기준선 교정 완료 (2026-07-28)** — modelc 600 K, 62원자, 200/2000 프레임, 3엔진 CPU.
  프레임 단위 중앙 **0.3175** · p95 **0.3669** eV/Å → `db/properties/mlip_committee_baseline.json`
- ⚠ **위원회 독립성이 보이는 것보다 낮다**: 쌍별 mace|sevennet **0.202** < sevennet|uma 0.215 <
  mace|uma **0.317**. **가장 잘 맞는 쌍이 훈련셋을 공유한다(MPtrj)** — UMA만 OMat24.
  불일치를 지배하는 것은 아키텍처가 아니라 **훈련 데이터**이고, 실질 **3명이 아니라 2진영**이다.
- **원소별(정규화 후)**: P 0.333 > S 0.277 > Li 0.235 > Cl 0.182.
  원시 절대값으로는 P/Cl = 5.9배였는데 정규화하면 **1.8배**로 압축된다 — 원시 순위의 대부분이
  **힘 크기**였다. 단 **순서는 살아남는다**: 모델들이 **PS₄ 골격에서 가장 덜 합의**한다.
- 🔑 **T3에 직결**: T3의 1순위 관측량이 **잔존 PS₄ 층수**인데 위원회가 가장 덜 합의하는 게 바로 그
  PS₄다. → T3 착수 게이트를 **벌크가 아니라 Li 계면 구조에서** 다시 잡아야 하고, QE 단일점 대조를
  병행해야 한다(대리지표는 DFT를 대체하지 않는다).
- 다음: ① 정적 구조(comp1 V0) 기준선 — 평형에서의 하한 ② **Li 계면 슬랩 탐지 모드** (T3 게이트)
  ③ 훈련셋이 다른 4번째 엔진 검토 ④ QE 단일점 대조 ~20 스냅샷

### ⏳ 발표 구술 txt 대기
두 발표 모두 구술 내용 txt를 받기로 함. 받으면 각 digest `§99` 를 채우고
미해결 질문(lee Q1–Q6 / moon Q1–Q6)을 닫는다. **이 항목은 닫지 말 것.**

## ✅ 닫힌 항목
- (여기로 이동)
