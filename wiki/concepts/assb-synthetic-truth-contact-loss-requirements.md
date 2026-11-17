---
title: ASSB 합성 truth 의 접촉 손실 요구 — 카드 물음을 truth 단계에서 미리 답하지 않으려면
description: "Requirements for an ASSB synthetic truth in which contact loss is NOT pre-identified with LAM_PE: a separate capacity-multiplying θ, Li-holding disconnected particles, dead volume that does not become electrolyte, θ-only manipulation, area-proportional double layer, relaxation time as a truth parameter, φ vs u distinction, and θ(N) shape as an explicit assumption"
created: 2026-09-23
updated: 2026-11-17
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/neumann2020_interfacial-effects-thiophosphate-assb-model.md, raw/papers/ruess2020_ncm-cracking-kinetics-liquid-vs-solid-electrolyte.md, raw/papers/tian2017_contact-area-loss-assb-simulation.md, raw/papers/barai2021_cathode-llzo-delamination-lattice-spring-capacity-fade.md, raw/papers/danilov2008_liquid-electrolyte-transport-electroneutrality-dissociation.md, raw/papers/deng2021_assb-reduced-order-model-pade-polynomial.md, raw/papers/raijmakers2020_thin-film-assb-model-double-layer-dc-ac-joint-fit.md, raw/papers/schmidt2024_nitsche-contact-delamination-resolved-ssb-cathode.md, raw/papers/bielefeld2023_useful-models-ssb-simplicity-perspective.md, raw/papers/jiao2023_electro-chemo-mechanical-se-modulus-conductivity-intergranular-czm.md, raw/papers/chen2013_sofc-miec-composite-electrode-percolation-theory.md, raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd-si.md, raw/papers/li2024_assb-composite-cathode-model-contact-area-edl.md, raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md, raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md, raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd.md, raw/papers/sakka2022_pressure-3d-structure-composite-cathode-xct.md, raw/papers/ren2023_oxide-ssb-composite-cathode-architecture-perspective.md, raw/papers/bielefeld2022_voids-kinetics-morphology-composite-cathode-fem.md, raw/papers/bielefeld2020_effective-ionic-conductivity-binder-composite-cathode.md, raw/papers/asheri2023_data-driven-multiscale-ssb-delamination-surrogate.md, raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: prescriptive
evidenceScope: multi-source-mixed
---

# ASSB 합성 truth 의 접촉 손실 요구

> **무엇인가**: [[assb-contact-loss-vs-lampe]] 카드의 물음은 "접촉 손실과 `LAM_PE` 가 OCV
> 적합에서 갈리는가" 다. 이 물음을 [[degradation-degeneracy]] 식 **합성 truth** 로 시험하려면,
> truth 를 만드는 모델이 **두 원인을 처음부터 같은 파라미터로 두지 않아야** 한다. 이 페이지는
> 흡수한 논문들이 그 조건을 하나씩 드러낸 것을 한곳에 모은 **요구 목록**이다.
>
> **2026-09-23 사용자 결정 (마)** 으로 카드의 "새 제약"(37호) 에서 분리했다. 원래 다섯 조건은
> 37호(Li 2024)가 적었고, 뒤의 편들이 붙인 것을 합쳤다.
>
> ⚠ **전부 `[추론]` 이다.** 우리 코드에서 확인한 것이 아니다. RUN_SCOPE(`src/ tools/ configs/
> scripts/`)는 건드리지 않았다. 우리 `LAM_PE` 코드의 형태는 `degradation-degeneracy/docs/07_LAM_LLI.md`
> §2 가 정본이다. 수치는 각 digest 의 사본이며 인용 근거가 아니다.

## 왜 필요한가 — 동어반복이 truth 단계에서 생긴다

모델이 접촉 손실을 넣는 자리는 지금까지 **두 곳뿐**이었다 ([[assb-lampe-contact-product-degeneracy]]).

| 자리 | 모델 | 결과 |
|---|---|---|
| 활물질 분율 `ε_p` (입자 통째 비연결 `u`) | 27호 Sinzig P2D (오프셋 `1−u`) · 28호 Bizeray SPM 묶음 `Q_th` · 37호 Li 2024 · **58호 Asheri** (박리 `⟨d⟩` 가 식 (32) `a·(1−⟨d⟩)` 로만 들어가고 입자 유입은 손상 무관) · **106호 Tian & Qi 2017**(1D · 접촉 면적비 γ 가 용량 채널(식 18 — '최악의 경우 물질 손실')과 i₀(γ·k_pos — 식 17)에 같이 — 면적형 LAM_PE 와 항등 `[재현·대수]` · 계보 첫 정량 접촉 손실 모형) | `LAM_PE` 와 **정의상 같다** |
| 유효 계면 면적 `A_eff` (표면 피복 `φ`) | 37호 Li 2024 · 50호 Miß (기하 `a_v` 고정) · 56호 Bielefeld 2022 (반구 void) · **93호 Bielefeld 2023 제안**(결론 "evolution of the porosity, tortuosity and specific surface area upon cycling" 을 수정 Newman 에 — 계산 0 · 통째 고립이 갈 자리 없음) · **94호 Schmidt 2024**(3D 해상 · Nitsche 접촉 — `φ` 를 역학이 계산 · 박리 면 BV 0 · j₀ 고정 · 무접착 가역 법칙) · **105호 Barai 2021**(2D 격자 스프링 — 계면 요소가 변형 에너지 문턱을 넘으면 제거 · 식 (1) R_ct = (A₀/A_f)·RT/(i₀F) · **비가역 · 10 사이클 누적** · 평면 양극 판이라 고립 0) · **109호 Neumann 2020**(3D 해상 · CT 재구성 — 표면 복셀 비활성 = `φ` 형 · i00 면적당 상수를 θ = 1 로 첫 사이클 뒤 EIS(R_Ca 66 Ω cm²)에 손 맞춤 · 통째 고립 가정 제외 · 호 증가는 균일 곱의 1/5–1/19 `[재현·가정]`) | 반응 상수 `k` 와 **곱으로만** 들어간다 — OCV·용량에 안 보이고 계면 화학 열화와 항등(37호). 3D 해상 모델에서는 이 항등이 **부분적으로만** 성립(56호 모델 명제) · 94호 `[재현·가정]`: 면적 손실의 전압 몫이 BV(≈6 mV)보다 입자 안 확산 분극(≈67 mV)으로 — 고정 컷오프에서 용량 결손처럼 보이는 η 형 · 105호 `[재현·대수]`: 전압 몫이 계면 BV 에 있고 NMC 는 Tafel 영역(i/i₀ 5–35)이라 (2RT/F)·ln(A₀/A_f) — 율 무관 상수 이동(율 쓸기로 물질 손실과 안 갈림 · 선형 영역 i ≪ i₀·A_f/A₀ 에서만 율 의존) |
| (참고) **자리 없음** — CAM\|SE 불파괴 · 손상은 입계에만 | 83호 Jiao 2023 (3D 복합 양극: SI 가정 "(5) … assumed as perfect and couldn't be damaged" · 2D 입계 CZM: 손상 > 80 % → 그 영역 σ_ion 0 · 용량 계산 0) | 카드 물음의 기구(박리 → 접촉 손실)가 모델에 없다 — "SE 탄성률은 전기화학에 영향 없음" 같은 결론이 이 부재의 귀결이 된다. 합성 truth 로는 **접촉 항 0 의 음성 대조판** |

어느 자리로 넣든 truth 가 카드 물음에 **미리 답한다**. 아래 요구는 그것을 피하기 위한 것이다.

## 요구 목록

| ID | 요구 | 출처 (assb 호) | 상태 |
|---|---|---|---|
| **R1** | **용량에 곱해지되 `ε_p` 와 별개인 `θ`** 를 둔다 | 37호 · **100호 Deng 2021**(37호가 물은 축약 모형 — 확인) | 계보의 모든 모델이 위반(27·28·37·58호) · 83호는 CAM\|SE 접촉 항 자체가 없다(가정) · 100호 축약 모형(ROM)도 위반 — θ · ε_p 둘 다 0 · 면적 A 한 값이 용량 극 · 수송 이득 · i₀(A·k_pos)에 같이 들어간다(37호 A_eff 는 그 꼴 위의 BV 분모 추가) · **105호 Barai 2021**(계보가 `θ(N)` 원전으로 기다린 모형)도 위반 — 접촉 손실 = 계면 면적 A_f 하나 · i₀ 와 곱 · `θ` · `ε_p` 0 · **106호 Tian & Qi 2017**(계보 첫 정량 모형)은 위반을 저자가 가정으로 인쇄 — "in the worst case, the loss of contact between electrode and solid-electrolyte interface would cause the loss of LiCoO2 material" · 한계 "the worst scenario" · 2D/3D 필요 · **109호**도 위반 쪽 — 통째 고립을 가정으로 제외("prevent full contact loss of the active material") · θ 자리 0 |
| **R2** | **비연결 입자가 자기 SOC 의 Li 를 붙든다** — 끊긴 순간의 리튬화 상태가 재고에서 빠진다(LLI 와도 얽힘) | 37호 | 계보 측정 0 (38호 Conforto 도 "inactive" 로만) · 106호 — 잃은 물질 (1−γ) 의 Li 상태 0 (식 18 은 남은 접촉으로 양극 유속을 1/γ 배 할 뿐) |
| **R3** | **죽은 부피가 전해질이 되지 않는다** — 비연결 입자·void 가 이온 경로로 바뀌지 않게 | 37호 · 56호(검증 구조가 void 14 % 를 SE 로 채움) · 57호 · **93호**(원칙 인쇄 — "The assumption that all volume that is not filled with CAM contains electrolyte no longer applies" · 같은 저자 56호 검증 구조는 위반) · **109호**(박리 틈을 **전도하는 SE 층**으로 — "the transport across and through the passivating solid electrolyte is kept unchanged" · CT 이진화를 이론 AMSVF 에 맞춰 공극 0 — `[재현·외부 값]` 상대 밀도 ≈95 %) | 56호가 정확히 이것을 위반 · 109호도 구성상 위반 |
| **R4** | **`θ` 에만 반응하는 조작** 을 truth 에 둔다 (압력 되돌림 등) | 37호 · 39호 Sakka (압력이 `φ` ×1.10 · `R_ct` ×14 — 여러 인자를 같이 움직임) · 57호 (바인더 한 손잡이가 경로와 접촉 두 곱을 같이 깎음) · 56호 (`φ` 스윕은 θ-전용 아님) · 94호 (모형 — OCV · i₀ 응력 의존을 무시해 압력이 구성상 접촉만 움직이나, 움직이는 것은 `θ` 가 아니라 `φ`) · 105호 (모형 — 조작 = 입도 · 상한 전압 · 전류 · i₀; **i₀ 쓸기는 박리 분율을 안 바꾸는 'k 전용' 조작**(그림 S4 — R4 의 짝) · θ-전용 0) · 106호 (모형 — 압력이 Persson γ 하나만 움직이나 γ ≡ 물질 (최악의 경우) 이라 θ-전용이 아니라 'LAM 되돌림' 조작 · 압력 사상은 같은 편 식 (22)–(23) 과 지수가 다른 1제곱 식 (26)) | 실측·모델 모두 **θ-전용 조작 0** — [[assb-pressure-reapplication-separation-test]] 설계 조건 참조 |
| **R5** | **면적에 비례하는 이중층** `C_dl ∝ A` | 37호 (원형 모델 `c_dl` 은 면적 무관 상수) · 43·48·51호 (여러 호의 `C` 가 이중층 상한을 수백–수천 배 넘음) · 51호 (전자 접촉 호의 `C` 는 비접촉 여집합에 앉을 수 있음) · **98호 Raijmakers 2020**(37호가 '조상' 으로 매단 편 — `c_dl` 은 **기하 면적당** F cm⁻² · 실제 계면 면적 변수 0 · 숨은 면적 인자가 k · `c_dl` 에 같은 배수(R·C 불변) · 값은 DC + AC 적합 · `c^n_dl` 등가 유전 두께 0.67–2.2 µm `[재현·가정]` — 37호 F(전극 전체) 꼴은 조상에 없는 변형) · **107호 Ruess 2020**(`C ∝ 면적` 을 쓰지 않는 두 번째 면적 채널 — Warburg 겉보기 D ∝ A² — 의 실측 · C_dl 증가 = 균열 면적은 인용(Oswald 2020 [71] — 미흡수)) | 곱 축퇴 처방 1단계의 전제 — **검증 없이 가정하면 1단계가 truth 에서 거짓** · 조상(98호)도 'C ∝ 실제 접촉 면적' 을 시험하지 않았다(면적 하나 · 열화 0) |
| **R6** | **OCV 관측의 이완 시간을 truth 파라미터로** 둔다 | 38호 Conforto (1 h 이완 ↔ 자기 `τ=L²/D` 로 13–17 h) · 38호 SI(S3): 방전 뒤도 1 h · 기준 곡선은 **2 h** 휴지 · 충전 가지 · **4.19 V 에서 끝**(high-V 초기 여섯 사이클이 범위 밖) — 게이지 ↔ 눈금의 이완 불일치 · 범위 밖 외삽도 파라미터로 · **107호**(GITT 이완 2 h ↔ ASSB τ > 200 h — 그림 4 · SI-3 의 'V_OC' 는 평형 아님 · 56 → 02호 OCV 가 이 LEB 곡선) | 이완 부족이면 동역학 손실이 질량 채널로 샌다 |
| **R7** | **표면 피복 `φ` 와 통째 비연결 `u` 를 별개 변수로** 둔다 | 37호 · 39호 (CT 가 잰 것은 `φ`) · 55호 Hlushkou (void 경로 효과만) · 56호 (`φ` 자리만) · **68호 Chen 2013**(SOFC 좌표수 해석식 — `u = 1 − P^e` 와 `φ_cov = Z·sin²θ/4` 가 한 식 안의 두 인자, `[재현]`) · **94호**(`φ` 만 동적 계산 — 같은 연구실 27호의 `u` 와 두 편에 따로) · **105호**(`φ` 만 — 사이클 축 비가역 누적의 첫 모형판 · `u` ≡ 0(평면 판 하나)) · **106호**(표면 피복형 변수 γ 를 '최악의 경우' 정의로 통째 비연결 `u` 처럼 — `φ` ↔ `u` 를 정의로 합침) · **107호**(한 셀에서 W(θ 쪽) 비 ≥0.91 ↔ Warburg(θφ 쪽) 비 0.59–0.83 — 106호가 정의로 합친 두 변수를 다른 채널이 따로 본다는 실측 방향 · 우리 재현 · 가정 넷) · **109호**(`φ` 형 표면 박리 + 집전체 전자 접촉 — 둘을 한 3D 구조에서 계산했으나 `u` 0 · 전자 접촉은 CAM\|SE 밖의 셋째 자리) | 두 효과를 한 **시뮬레이션** 구조에서 같이 계산한 편 0 · 68호 해석식은 둘을 따로 주지만 **정적 · SOFC · 검증 0** 이고 반응 속도에서는 곱 · 22호 세 점 대조 실패 |
| **R8** | **`θ(N)` 의 형태를 명시적 가정으로 적는다** — 계단형(첫 충전만) vs 점진형 | 23호 Koerver 원문("contact loss should only occur during the initial charge") ↔ 33·53호가 이것을 **역전 인용** · **105호 Barai 2021**(흡수 2026-11-17 — 원장 ★★★★ '유일한 `θ(N)` 모델 원전' · 판정: **비가역 결합 제거형** 누적(사이클당 하중 = SOC 스윙 · 문턱 확률 — 분포 미인쇄 · 정변위 x 구속) · 첫 충전 큰 계단(NMC 150 nm · 4.5 V 분율 0.57–0.86) + 사이클별 이산 증분 · **`θ(N)` 곡선 인쇄 0 — 10 사이클은 용량만**(계단 + 멈춤 · LCO 큰 입자 끝 셋 평탄) · 용량 ↔ 면적 사상이 로그(Tafel — 용량 궤적 ≠ 면적 궤적) · 한 실현 · '포화 없이'(53호)는 이 편 문장 아님) · 83호(입계 피로 CZM 의 N 축 — 파괴 사이클 95–1545 · 파라미터 0 · 모양 후보만 · CAM\|SE 판 아님) · 93호(결론 제안 — ε · τ · 비표면적의 사이클 진화를 수정 Newman 에 · 형태 · 자료 0) · 94호(이력 없는 가역 접촉 법칙 — N 축 누적 구성상 0 · 충전마다 열리고 방전마다 닫히는 "SoC 주기형" 이 셋째 후보 · 반 사이클 하나만 계산) · 106호(결론 "the contact area would be decreased continuously because of the volume change of the electrodes" — 점진형 서술 · N 축 모형 0 · '사이클 뒤' = 손으로 고른 거칠기 (m, I) 네 단계) · **107호**(첫 사이클 충 → 방 Warburg 면적 ≥0.92 — 23호 '첫 충전 계단' 이 이 셀(LPSCl · 70 MPa · 무탄소 · 4.3 V)에서는 ≈8 % 해상도 아래 · N = 1 · 셀 하나) · **109호**(서사 = 첫 사이클 계단 27 %(인용 [28] · [56]) + 점진 'suggests'(100 사이클 선형 −0.434 mAh g⁻¹/사이클 `[도표·벡터]`) · 계산 0) | ⚠ **미결정** — 두 형태를 다 돌릴지는 사용자 결정 대기(원장 §3-b) |

## 목록 밖 메모 — SE 전해질 수송 모형 · 중성종 닫음 (2026-10-03 · 101호 · 요구로 올리지 않음)

- `[인쇄]` 계보(26 · 91 · 98 · 99 · 100호)의 SE 수송 식은 액체 유기 전해질 원전(101호 Danilov & Notten 2008 — Li⁺ · PF₆⁻ · 움직이는 중성 LiPF₆ 이온쌍)의 꼴이다 — 'SE 에 농도 구배 · 이온 + 공공' 은 원전이 아니라 91 · 98호의 이식(n⁻ = nBO 전하 · 고정 Li⁰ · 공공 · 국소 닫음)이다(101호 digest 중심 표 — ✅ 11 · 부분 2 · ❌ 4).
- `[재현·가정]` 같은 식 · 같은 (액체) 매개변수에서 중성종 닫음만 바꿔도 전해질 과전압의 농도 항이 74.0 → 7.4 mV · 이원 가정 몫(같은 σ 단일 이온 대비)이 72 → 17 % 로 움직인다(δ 0.8 · 50 min — 반사실).
- `[해석]` 접촉 손실 truth 에서 SE 전해질 과전압은 '전해질 수송 ↔ 계면 · 접촉' 배정의 상대 몫을 정한다 — truth 설계 문서에 **SE 전해질 모형(이원 해리 ↔ 단일 이온)과 중성종 닫음(확산 ↔ 고정 ↔ 국소 보존)** 을 R1–R8 표 옆에 적어 두는 것이 이 메모의 전부다. ⚠ 요구(R9)로 올리지 않는다 — 새 판단 거리(원장 §3-b · 글자는 호출자)이고 결정 대기다.

## 목록 밖 메모 — θ 라벨의 모형 꼴 의존 (2026-11-17 · 109호 · 요구로 올리지 않음)

- `[재현·가정]` 같은 11 사이클 임피던스 증가(+45 Ω cm²)에 균일 모형(R_ct ∝ 1/θ)은 θ ≈0.6(면적 −40 %), 109호 3D 해상 모형은 면적 −80 % 를 붙인다(75 % 시나리오 +38.4 Ω cm²).
- `[해석]` truth 와 적합 모형의 꼴(3D ↔ 균일)이 다르면 θ 가 모형 차만으로 ×2 움직일 수 있다 — truth 설계 문서에 'θ 를 정의한 모형 꼴' 을 R1–R8 표 옆에 적는 것이 이 메모의 전부다. ⚠ R9 로 올리지 않는다(새 판단 거리 1 · 결정 대기).

## 쓰는 법

- truth 설계 문서에 **R1–R8 각각의 충족 여부를 표로 적는다.** 충족하지 못한 요구가 있으면 그 truth
  로 낸 "접촉 손실과 `LAM_PE` 는 갈린다/안 갈린다" 결론에 **그 요구 ID 를 조건으로 붙인다.**
- R1 을 못 지키는 모델(현재 PyBaMM P2D·SPM 포함)은 **음성 대조**로만 쓴다 — "이 모델에서는
  정의상 같다" 를 확인하는 용도.
- 곱 축퇴 처방([[assb-lampe-contact-product-degeneracy]])의 각 단계는 이 요구가 truth 에 들어 있을
  때만 합성 데이터로 시험할 수 있다 (예: 1단계는 R5, 압력 연산자는 R4).

## 이 페이지가 주장하지 않는 것

- R1–R8 을 **동시에** 만족하는 모델이 존재한다거나 만들 수 있다고 주장하지 않는다.
- 요구 목록이 완전하다고 주장하지 않는다 — 흡수가 이어지면 늘어난다.
- 어떤 요구도 우리 코드·합성 실행으로 검증하지 않았다.
- 93호의 R3 원칙 인쇄를 R3 가 검증됐다는 뜻으로 쓰지 않는다 — 저자 문장(1차 자료 0)이고, 같은 저자 56호 검증 구조는 위반했다.
- 94호를 R4 · R7 충족 표본으로 쓰지 않는다 — 압력이 구성상 접촉만 움직이는 것은 무시 가정의 결과이고, 계산된 것은 `φ` 하나(`θ` · `u` 0)이며, 실험 대조 0 인 모형이다.
- 98호를 R5 충족 표본으로 쓰지 않는다 — 기하 면적당 꼴은 형식이고, 실제 계면 면적 · 면적 변화 · 노화가 지면에 없다. 등가 유전 두께는 ε_r 를 기하 축전기에서 역산한 가정 위의 우리 계산이다.
- 100호를 R1 위반의 측정 표본으로 쓰지 않는다 — 신품 축약 모형의 구조(인쇄 식 · 표)이고 열화를 다루지 않았다. 'A 를 줄이면 용량 · 수송 · i₀ 가 함께 움직인다' 는 그 구조 위의 우리 대수다.
- 101호를 SE 전해질 모형 선택(이원 ↔ 단일 이온)의 근거로 쓰지 않는다 — 액체 원전이고 고체에 대해 말하지 않으며, 닫음 비교는 액체 매개변수 위의 반사실이다.
- 105호를 R8 형태 결정의 근거로 쓰지 않는다 — 박리 분율의 사이클 궤적이 인쇄되지 않았고(용량만), 용량 궤적은 Tafel 로그 사상을 거친 한 실현이다. '결합 제거형' 은 후보 목록에 한 줄을 더한 것까지다. R7 의 '`φ` 비가역 누적 첫 모형판' 도 모형 구성(측정 0)이다.
- 106호를 R4 · R7 충족 표본으로 쓰지 않는다 — 압력이 γ 하나만 움직이는 것은 무시 가정의 결과이고, γ 는 φ 와 u 를 정의로 합친 변수(최악의 경우 물질 손실)이며, 압력 사상은 같은 편 식 (22)–(23) 과 지수가 다른 식 (26) 위에 있다.
- 107호를 R7 · R8 충족 · 반례의 측정으로 쓰지 않는다 — 첫 사이클 · 셀 하나 · 역모형 채널(W · Warburg)의 우리 재현이다.
- 109호를 R3 · R7 위반의 측정 표본으로 쓰지 않는다 — 모형 구성(가정)의 기술이고, θ 라벨 ×2 는 우리 대조(균일 곱 기준선 가정) 위다.

## 관련

- [[assb-contact-loss-vs-lampe]] — 닻 카드 (원래 "새 제약" 에 있던 자리)
- [[assb-lampe-contact-product-degeneracy]] — 곱 축퇴와 처방 표
- [[assb-pressure-reapplication-separation-test]] — R4 의 실측 쪽
- [[composite-cathode-percolation-utilization]] · [[assb-apparent-capacity-decomposition]] — `θ_AM` 의 정의
- [[degradation-degeneracy]] — 합성 truth 프로젝트
