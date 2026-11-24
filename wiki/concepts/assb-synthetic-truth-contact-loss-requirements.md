---
title: ASSB 합성 truth 의 접촉 손실 요구 — 카드 물음을 truth 단계에서 미리 답하지 않으려면
description: "Requirements for an ASSB synthetic truth in which contact loss is NOT pre-identified with LAM_PE: a separate capacity-multiplying θ, Li-holding disconnected particles, dead volume that does not become electrolyte, θ-only manipulation, area-proportional double layer, relaxation time as a truth parameter, φ vs u distinction, and θ(N) shape as an explicit assumption"
created: 2026-09-23
updated: 2026-11-24
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/shao2022_coupled-electrochemical-mechanical-contact-loss-pressure-assb.md, raw/papers/jung2020_ni-rich-compliant-microstructure-ncm-assb.md, raw/papers/han2021_single-vs-polycrystalline-nca-sulfide-halide-se.md, raw/papers/neumann2020_interfacial-effects-thiophosphate-assb-model.md, raw/papers/ruess2020_ncm-cracking-kinetics-liquid-vs-solid-electrolyte.md, raw/papers/tian2017_contact-area-loss-assb-simulation.md, raw/papers/barai2021_cathode-llzo-delamination-lattice-spring-capacity-fade.md, raw/papers/danilov2008_liquid-electrolyte-transport-electroneutrality-dissociation.md, raw/papers/deng2021_assb-reduced-order-model-pade-polynomial.md, raw/papers/raijmakers2020_thin-film-assb-model-double-layer-dc-ac-joint-fit.md, raw/papers/schmidt2024_nitsche-contact-delamination-resolved-ssb-cathode.md, raw/papers/bielefeld2023_useful-models-ssb-simplicity-perspective.md, raw/papers/jiao2023_electro-chemo-mechanical-se-modulus-conductivity-intergranular-czm.md, raw/papers/chen2013_sofc-miec-composite-electrode-percolation-theory.md, raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd-si.md, raw/papers/li2024_assb-composite-cathode-model-contact-area-edl.md, raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md, raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md, raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd.md, raw/papers/sakka2022_pressure-3d-structure-composite-cathode-xct.md, raw/papers/ren2023_oxide-ssb-composite-cathode-architecture-perspective.md, raw/papers/bielefeld2022_voids-kinetics-morphology-composite-cathode-fem.md, raw/papers/bielefeld2020_effective-ionic-conductivity-binder-composite-cathode.md, raw/papers/asheri2023_data-driven-multiscale-ssb-delamination-surrogate.md, raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md]
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
| 활물질 분율 `ε_p` (입자 통째 비연결 `u`) | 27호 Sinzig P2D (오프셋 `1−u`) · 28호 Bizeray SPM 묶음 `Q_th` · 37호 Li 2024 · **58호 Asheri** (박리 `⟨d⟩` 가 식 (32) `a·(1−⟨d⟩)` 로만 들어가고 입자 유입은 손상 무관) · **106호 Tian & Qi 2017**(1D · 접촉 면적비 γ 가 용량 채널(식 18 — '최악의 경우 물질 손실')과 i₀(γ·k_pos — 식 17)에 같이 — 면적형 LAM_PE 와 항등 `[재현·대수]` · 계보 첫 정량 접촉 손실 모형) · **116호 Shao 2022 *Energy***(1D 박막 · κ = A/A₀ — 106호 꼴을 따라 전극 유속 ×1/κ(이 지면 인쇄 0 — 그림으로 읽힘) → 정규화 확산 κ·c^m 묶음 = 면적형 `LAM_PE` 와 같은 열 `[재현·대수]` · 그러나 동역학은 i₀/κ — 106호 γ·k_pos(곱)와 반대로 접촉 손실이 과전압을 줄인다) | `LAM_PE` 와 **정의상 같다** |
| 유효 계면 면적 `A_eff` (표면 피복 `φ`) | 37호 Li 2024 · 50호 Miß (기하 `a_v` 고정) · 56호 Bielefeld 2022 (반구 void) · **93호 Bielefeld 2023 제안**(결론 "evolution of the porosity, tortuosity and specific surface area upon cycling" 을 수정 Newman 에 — 계산 0 · 통째 고립이 갈 자리 없음) · **94호 Schmidt 2024**(3D 해상 · Nitsche 접촉 — `φ` 를 역학이 계산 · 박리 면 BV 0 · j₀ 고정 · 무접착 가역 법칙) · **105호 Barai 2021**(2D 격자 스프링 — 계면 요소가 변형 에너지 문턱을 넘으면 제거 · 식 (1) R_ct = (A₀/A_f)·RT/(i₀F) · **비가역 · 10 사이클 누적** · 평면 양극 판이라 고립 0) · **109호 Neumann 2020**(3D 해상 · CT 재구성 — 표면 복셀 비활성 = `φ` 형 · i00 면적당 상수를 θ = 1 로 첫 사이클 뒤 EIS(R_Ca 66 Ω cm²)에 손 맞춤 · 통째 고립 가정 제외 · 호 증가는 균일 곱의 1/5–1/19 `[재현·가정]`) | 반응 상수 `k` 와 **곱으로만** 들어간다 — OCV·용량에 안 보이고 계면 화학 열화와 항등(37호). 3D 해상 모델에서는 이 항등이 **부분적으로만** 성립(56호 모델 명제) · 94호 `[재현·가정]`: 면적 손실의 전압 몫이 BV(≈6 mV)보다 입자 안 확산 분극(≈67 mV)으로 — 고정 컷오프에서 용량 결손처럼 보이는 η 형 · 105호 `[재현·대수]`: 전압 몫이 계면 BV 에 있고 NMC 는 Tafel 영역(i/i₀ 5–35)이라 (2RT/F)·ln(A₀/A_f) — 율 무관 상수 이동(율 쓸기로 물질 손실과 안 갈림 · 선형 영역 i ≪ i₀·A_f/A₀ 에서만 율 의존) |
| (참고) **자리 없음** — CAM\|SE 불파괴 · 손상은 입계에만 | 83호 Jiao 2023 (3D 복합 양극: SI 가정 "(5) … assumed as perfect and couldn't be damaged" · 2D 입계 CZM: 손상 > 80 % → 그 영역 σ_ion 0 · 용량 계산 0) | 카드 물음의 기구(박리 → 접촉 손실)가 모델에 없다 — "SE 탄성률은 전기화학에 영향 없음" 같은 결론이 이 부재의 귀결이 된다. 합성 truth 로는 **접촉 항 0 의 음성 대조판** |

어느 자리로 넣든 truth 가 카드 물음에 **미리 답한다**. 아래 요구는 그것을 피하기 위한 것이다.

## 요구 목록

| ID | 요구 | 출처 (assb 호) | 상태 |
|---|---|---|---|
| **R1** | **용량에 곱해지되 `ε_p` 와 별개인 `θ`** 를 둔다 | 37호 · **100호 Deng 2021**(37호가 물은 축약 모형 — 확인) | 계보의 모든 모델이 위반(27·28·37·58호) · 83호는 CAM\|SE 접촉 항 자체가 없다(가정) · 100호 축약 모형(ROM)도 위반 — θ · ε_p 둘 다 0 · 면적 A 한 값이 용량 극 · 수송 이득 · i₀(A·k_pos)에 같이 들어간다(37호 A_eff 는 그 꼴 위의 BV 분모 추가) · **105호 Barai 2021**(계보가 `θ(N)` 원전으로 기다린 모형)도 위반 — 접촉 손실 = 계면 면적 A_f 하나 · i₀ 와 곱 · `θ` · `ε_p` 0 · **106호 Tian & Qi 2017**(계보 첫 정량 모형)은 위반을 저자가 가정으로 인쇄 — "in the worst case, the loss of contact between electrode and solid-electrolyte interface would cause the loss of LiCoO2 material" · 한계 "the worst scenario" · 2D/3D 필요 · **109호**도 위반 쪽 — 통째 고립을 가정으로 제외("prevent full contact loss of the active material") · θ 자리 0 · **116호 Shao 2022 *Energy***도 위반 쪽 — `LAM` 손잡이 0 · κ 가 유속 척도(용량 스케일)이자 i₀/κ(동역학 반전) — 정규화 확산에서 c^m 스케일과 같은 열 |
| **R2** | **비연결 입자가 자기 SOC 의 Li 를 붙든다** — 끊긴 순간의 리튬화 상태가 재고에서 빠진다(LLI 와도 얽힘) | 37호 | 계보 측정 0 (38호 Conforto 도 "inactive" 로만) · 106호 — 잃은 물질 (1−γ) 의 Li 상태 0 (식 18 은 남은 접촉으로 양극 유속을 1/γ 배 할 뿐) · 113호 — ex situ (003) 방전 상태 이동 · 이봉(P/LYC 100 사이클 높이비 ≈0.7 : 1) — 해체 뒤 Li 원천 0 이라 η 와 고립이 같은 서명 · 이봉 지속은 두 집단 사이 Li 교환 없음 쪽 단서(채취 · 휴지 미인쇄 — 측정 아님) · 114호 — 첫 사이클 30 °C 방전 뒤 격자에 안 들어간 Li 를 ex situ (003) 로 봄: NCA80 단일 봉우리 18.57° · 폭 0.15 → 0.20 → 70 °C 회수 방전(다른 셀)에서 18.69° · 폭 0.16(`[재현·가정]` 격자 x 0.26 → 0.12 ↔ 쿨롱 x 0.23 · 0.12) — 첫 사이클의 '붙든 Li' 는 끊긴 입자의 별도 모집단보다 느린 회수 쪽으로 읽힘(소수 모집단 ≲10 % 는 폭으로 배제 못 함 · N > 1 측정 인쇄 0) |
| **R3** | **죽은 부피가 전해질이 되지 않는다** — 비연결 입자·void 가 이온 경로로 바뀌지 않게 | 37호 · 56호(검증 구조가 void 14 % 를 SE 로 채움) · 57호 · **93호**(원칙 인쇄 — "The assumption that all volume that is not filled with CAM contains electrolyte no longer applies" · 같은 저자 56호 검증 구조는 위반) · **109호**(박리 틈을 **전도하는 SE 층**으로 — "the transport across and through the passivating solid electrolyte is kept unchanged" · CT 이진화를 이론 AMSVF 에 맞춰 공극 0 — `[재현·외부 값]` 상대 밀도 ≈95 %) | 56호가 정확히 이것을 위반 · 109호도 구성상 위반 |
| **R4** | **`θ` 에만 반응하는 조작** 을 truth 에 둔다 (압력 되돌림 등) | 37호 · 39호 Sakka (압력이 `φ` ×1.10 · `R_ct` ×14 — 여러 인자를 같이 움직임) · 57호 (바인더 한 손잡이가 경로와 접촉 두 곱을 같이 깎음) · 56호 (`φ` 스윕은 θ-전용 아님) · 94호 (모형 — OCV · i₀ 응력 의존을 무시해 압력이 구성상 접촉만 움직이나, 움직이는 것은 `θ` 가 아니라 `φ`) · 105호 (모형 — 조작 = 입도 · 상한 전압 · 전류 · i₀; **i₀ 쓸기는 박리 분율을 안 바꾸는 'k 전용' 조작**(그림 S4 — R4 의 짝) · θ-전용 0) · 106호 (모형 — 압력이 Persson γ 하나만 움직이나 γ ≡ 물질 (최악의 경우) 이라 θ-전용이 아니라 'LAM 되돌림' 조작 · 압력 사상은 같은 편 식 (22)–(23) 과 지수가 다른 1제곱 식 (26)) · 113호 (실험 — 조작 = SC ↔ PC(면적 ×2.85 + 균열 성향 + PSD · 잔류 Li 묶음) · LYC ↔ LPSX(화학 + σ + 밀도) · SE 과량 · LYZC · **Li⁺ 불활성 RuO₂ 호스트 = SE 부반응 전용**(CAM 부피 변화 끔 — R4 의 짝 · 105호 'k 전용' 과 같은 줄) · 영변형 LTO 상대극 = 상대극 몫 끔 · θ-전용 0) · 114호 (실험 — 조작 = 상한 전압 4.1 ↔ 4.3 V(변형률 · 전위창을 같이 바꿈) · 회수 방전 0.05 C · 70 °C · CV 0.01 C(η 제거 조작 — 셋 동시 · 다른 셀 · 첫 사이클) · 두 재료(미세구조 + 공변 노브 다섯) · θ-전용 0) · 116호(모형 — 압력이 0.4 MPa 아래 κ_x1 · κ_x2 를 함께(s 0.0777 ↔ 0.0769 MPa) 움직이고 위에서는 V^r 열 상수 이동(16.8 µV/MPa)만 — θ-전용 아님 · 그 κ 자체가 용량 스케일 + 반전 동역학) | 실측·모델 모두 **θ-전용 조작 0** — [[assb-pressure-reapplication-separation-test]] 설계 조건 참조 |
| **R5** | **면적에 비례하는 이중층** `C_dl ∝ A` | 37호 (원형 모델 `c_dl` 은 면적 무관 상수) · 43·48·51호 (여러 호의 `C` 가 이중층 상한을 수백–수천 배 넘음) · 51호 (전자 접촉 호의 `C` 는 비접촉 여집합에 앉을 수 있음) · **98호 Raijmakers 2020**(37호가 '조상' 으로 매단 편 — `c_dl` 은 **기하 면적당** F cm⁻² · 실제 계면 면적 변수 0 · 숨은 면적 인자가 k · `c_dl` 에 같은 배수(R·C 불변) · 값은 DC + AC 적합 · `c^n_dl` 등가 유전 두께 0.67–2.2 µm `[재현·가정]` — 37호 F(전극 전체) 꼴은 조상에 없는 변형) · **107호 Ruess 2020**(`C ∝ 면적` 을 쓰지 않는 두 번째 면적 채널 — Warburg 겉보기 D ∝ A² — 의 실측 · C_dl 증가 = 균열 면적은 인용(Oswald 2020 [71] — 미흡수)) | 곱 축퇴 처방 1단계의 전제 — **검증 없이 가정하면 1단계가 truth 에서 거짓** · 조상(98호)도 'C ∝ 실제 접촉 면적' 을 시험하지 않았다(면적 하나 · 열화 0) |
| **R6** | **OCV 관측의 이완 시간을 truth 파라미터로** 둔다 | 38호 Conforto (1 h 이완 ↔ 자기 `τ=L²/D` 로 13–17 h) · 38호 SI(S3): 방전 뒤도 1 h · 기준 곡선은 **2 h** 휴지 · 충전 가지 · **4.19 V 에서 끝**(high-V 초기 여섯 사이클이 범위 밖) — 게이지 ↔ 눈금의 이완 불일치 · 범위 밖 외삽도 파라미터로 · **107호**(GITT 이완 2 h ↔ ASSB τ > 200 h — 그림 4 · SI-3 의 'V_OC' 는 평형 아님 · 56 → 02호 OCV 가 이 LEB 곡선) | 이완 부족이면 동역학 손실이 질량 채널로 샌다 |
| **R7** | **표면 피복 `φ` 와 통째 비연결 `u` 를 별개 변수로** 둔다 | 37호 · 39호 (CT 가 잰 것은 `φ`) · 55호 Hlushkou (void 경로 효과만) · 56호 (`φ` 자리만) · **68호 Chen 2013**(SOFC 좌표수 해석식 — `u = 1 − P^e` 와 `φ_cov = Z·sin²θ/4` 가 한 식 안의 두 인자, `[재현]`) · **94호**(`φ` 만 동적 계산 — 같은 연구실 27호의 `u` 와 두 편에 따로) · **105호**(`φ` 만 — 사이클 축 비가역 누적의 첫 모형판 · `u` ≡ 0(평면 판 하나)) · **106호**(표면 피복형 변수 γ 를 '최악의 경우' 정의로 통째 비연결 `u` 처럼 — `φ` ↔ `u` 를 정의로 합침) · **107호**(한 셀에서 W(θ 쪽) 비 ≥0.91 ↔ Warburg(θφ 쪽) 비 0.59–0.83 — 106호가 정의로 합친 두 변수를 다른 채널이 따로 본다는 실측 방향 · 우리 재현 · 가정 넷) · **109호**(`φ` 형 표면 박리 + 집전체 전자 접촉 — 둘을 한 3D 구조에서 계산했으나 `u` 0 · 전자 접촉은 CAM\|SE 밖의 셋째 자리) · **114호**(실측 — 원장이 '두 노브의 원전' 으로 지목한 라벨 'Ionically loosened / isolated' 가 **한 원 · 한 라벨 · 'and/or'** — 원전은 φ ↔ u 를 가르지 않는다 · 첫 사이클 회수 시험은 결손이 η 형(부분 접촉 φ · 고상 경로 · k 쪽 — 셋은 안 갈림)임을 지지 · u 측정 인쇄 0) · 116호(정의 = `φ`(A/A₀ · Persson) · 효과 = 용량 스케일(`u` · θ 형 — 유속 ×1/κ) — 한 변수에 두 효과) | 두 효과를 한 **시뮬레이션** 구조에서 같이 계산한 편 0 · 68호 해석식은 둘을 따로 주지만 **정적 · SOFC · 검증 0** 이고 반응 속도에서는 곱 · 22호 세 점 대조 실패 · 원장이 '실측 쪽' 으로 기다린 114호도 φ · u 측정 인쇄 0 |
| **R8** | **`θ(N)` 의 형태를 명시적 가정으로 적는다** — 계단형(첫 충전만) vs 점진형 | 23호 Koerver 원문("contact loss should only occur during the initial charge") ↔ 33·53호가 이것을 **역전 인용** · **105호 Barai 2021**(흡수 2026-11-17 — 원장 ★★★★ '유일한 `θ(N)` 모델 원전' · 판정: **비가역 결합 제거형** 누적(사이클당 하중 = SOC 스윙 · 문턱 확률 — 분포 미인쇄 · 정변위 x 구속) · 첫 충전 큰 계단(NMC 150 nm · 4.5 V 분율 0.57–0.86) + 사이클별 이산 증분 · **`θ(N)` 곡선 인쇄 0 — 10 사이클은 용량만**(계단 + 멈춤 · LCO 큰 입자 끝 셋 평탄) · 용량 ↔ 면적 사상이 로그(Tafel — 용량 궤적 ≠ 면적 궤적) · 한 실현 · '포화 없이'(53호)는 이 편 문장 아님) · 83호(입계 피로 CZM 의 N 축 — 파괴 사이클 95–1545 · 파라미터 0 · 모양 후보만 · CAM\|SE 판 아님) · 93호(결론 제안 — ε · τ · 비표면적의 사이클 진화를 수정 Newman 에 · 형태 · 자료 0) · 94호(이력 없는 가역 접촉 법칙 — N 축 누적 구성상 0 · 충전마다 열리고 방전마다 닫히는 "SoC 주기형" 이 셋째 후보 · 반 사이클 하나만 계산) · 106호(결론 "the contact area would be decreased continuously because of the volume change of the electrodes" — 점진형 서술 · N 축 모형 0 · '사이클 뒤' = 손으로 고른 거칠기 (m, I) 네 단계) · **107호**(첫 사이클 충 → 방 Warburg 면적 ≥0.92 — 23호 '첫 충전 계단' 이 이 셀(LPSCl · 70 MPa · 무탄소 · 4.3 V)에서는 ≈8 % 해상도 아래 · N = 1 · 셀 하나) · **109호**(서사 = 첫 사이클 계단 27 %(인용 [28] · [56]) + 점진 'suggests'(100 사이클 선형 −0.434 mAh g⁻¹/사이클 `[도표·벡터]`) · 계산 0) · 113호(실험 — poly 균열 면적 분율이 SOC 에 따라 열리고 닫힘: 첫 충전 3.93 · 3.69 → 첫 방전 1.33 · 0.90 % · N 축은 방전 상태 두 점(1 · 100) — 균열 · 틈을 `θ(N)` 대리로 쓸 때의 같은 SOC 비교 조건 · 형태 판정 입력 아님) · **114호**(실측 · 정성 · 한 시야씩 — NCA80 '첫 충전 계단'(입계 균열 · 방전 뒤 남음 · 압력계 충전 중간 ΔP 되오름은 <4.1 V 시작 단서) → 100 사이클 1차 입자로 붕괴 · FCG75 CAM\|SE 계면 틈이 첫 충전에 열리고 첫 방전 뒤 닫힘('SoC 주기형' 쪽 — 94호 셋째 후보 · 113호의 입자 속 균열 면적 개폐와 같은 축의 다른 대상) + 반복 사이클 느슨 주장(R3 2.6 → 146 Ω · 순 ΔP +0.067 — 접촉 측정 인쇄 0) · `θ(N)` 곡선 0) · 116호(κ 정적 · 첫 충전 하나 · 그림 9 '사이클 → void → 압력 회복' 은 모식 — N 축 인쇄 0) | 형태 후보 넷 — 계단(첫 충전) · 점진 · SoC 주기형(94 · 114호) · 비가역 누적형(83호 피로 CZM 입계판 · 105호 결합 제거 CAM\|SE 판) — 누적형의 모양은 사이클당 하중(부피 변화 · SOC 스윙) · 피로 · 문턱 파라미터(분포) · 고장 정의(요소 제거 · 파괴)가 정한다(메모 — 2026-11-17 §3-b (키) · 코드 이식은 RUN_SCOPE 별도 승인) · ~~⚠ **미결정** — 두 형태를 다 돌릴지는 사용자 결정 대기(원장 §3-b 에 행 없음 → 2026-11-17 일괄 문단의 사용자 결정 목록)~~ → ✅ **결정 (2026-11-24 사용자 · 권고대로): 계단 · 점진 두 형태 — 설계서 §2** (`followups/assb-contact-truth/DESIGN_v1.md` §2-7 — 같은 끝 상태 · 다른 경로 짝 · 첫 실행 C1 은 정적이라 미사용) |

## 목록 밖 메모 — SE 전해질 수송 모형 · 중성종 닫음 (2026-10-03 · 101호 · 요구로 올리지 않음)

- `[인쇄]` 계보(26 · 91 · 98 · 99 · 100호)의 SE 수송 식은 액체 유기 전해질 원전(101호 Danilov & Notten 2008 — Li⁺ · PF₆⁻ · 움직이는 중성 LiPF₆ 이온쌍)의 꼴이다 — 'SE 에 농도 구배 · 이온 + 공공' 은 원전이 아니라 91 · 98호의 이식(n⁻ = nBO 전하 · 고정 Li⁰ · 공공 · 국소 닫음)이다(101호 digest 중심 표 — ✅ 11 · 부분 2 · ❌ 4).
- `[재현·가정]` 같은 식 · 같은 (액체) 매개변수에서 중성종 닫음만 바꿔도 전해질 과전압의 농도 항이 74.0 → 7.4 mV · 이원 가정 몫(같은 σ 단일 이온 대비)이 72 → 17 % 로 움직인다(δ 0.8 · 50 min — 반사실).
- `[해석]` 접촉 손실 truth 에서 SE 전해질 과전압은 '전해질 수송 ↔ 계면 · 접촉' 배정의 상대 몫을 정한다 — truth 설계 문서에 **SE 전해질 모형(이원 해리 ↔ 단일 이온)과 중성종 닫음(확산 ↔ 고정 ↔ 국소 보존)** 을 R1–R8 표 옆에 적어 두는 것이 이 메모의 전부다. ⚠ 요구(R9)로 올리지 않는다 — ✅ 2026-11-17 §3-b (혀) 결정: 표기 의무(truth 설계 문서 R 표 옆 한 줄) · 요구 R9 아님 · 출처 보강 104호(강 — 단일 이온 SE 에 해리 이원 수송 이식) · 115 · 116호(중).

## 목록 밖 메모 — θ 라벨의 모형 꼴 의존 (2026-11-17 · 109호 · 요구로 올리지 않음)

- `[재현·가정]` 같은 11 사이클 임피던스 증가(+45 Ω cm²)에 균일 모형(R_ct ∝ 1/θ)은 θ ≈0.6(면적 −40 %), 109호 3D 해상 모형은 면적 −80 % 를 붙인다(75 % 시나리오 +38.4 Ω cm²).
- `[해석]` truth 와 적합 모형의 꼴(3D ↔ 균일)이 다르면 θ 가 모형 차만으로 ×2 움직일 수 있다 — truth 설계 문서에 'θ 를 정의한 모형 꼴' 을 R1–R8 표 옆에 적는 것이 이 메모의 전부다. ⚠ R9 로 올리지 않는다(새 판단 거리 1 → ✅ 2026-11-17 §3-b 일괄: 표기 의무 · R9 아님 — (혀) 와 같은 처리).

## 설계 선택지 기록 (2026-11-17 원장 §3-b 일괄 결정 — 요구(R) 아님 · 코드 0)

> 선택지다 — 요구 R1–R8 로 올리지 않는다. 코드 0 · 실행 0 · 코드로 옮기면 `degradation-degeneracy` RUN_SCOPE 가 움직인다(별도 승인 · 게이트 대상). forward 를 돌릴지는 원장 §3-b (차)(처)(~~실행 권고 · 사용자 승인 대기~~ → ✅ 2026-11-24 사용자 결정 — 첫 실행 후보 · 사전 등록 설계 = 설계서 `followups/assb-contact-truth/DESIGN_v1.md` §5).

| 선택지 | §3-b | truth 설계 문서에 적을 것 | 근거 (호) |
|---|---|---|---|
| θ → `LAM_PE` 결합 항 | (러) | 결합 계수 c ∈ [0, 1](통째 고립 θ 손실 중 ε_p 로 넘어가는 몫) — **기본 c = 0 = R1** · c = 1 은 '정의상 합침' 대조군(106호 γ ≡ 최악의 물질 손실 · 116호 κ = 용량 스케일) · c > 0 truth 는 R1 위반 대조군 · ⚠ 용량 채널만으로 c 를 검증하지 않는다(78호) · θ 로 옮기기 전 시간 궤적 조건([[assb-apparent-capacity-decomposition]] 정식 목록 — (두)) · 측면 `η(r)` 이 부분 이용처럼 보일 수 있다(80호) | c = 1: 106 · 116 · 정적 사상: 68 · 77 · 95 · c = 0: 105 · 109 · 경고: 74 · 78 · 79 · 80 |
| `j₀(x)` 모양 | (무) | √ 꼴(PyBaMM `Chen2020` 계열 · 유효 지수 ≈0.5) ↔ 원전형 지수(74호 1–3 · 107호 ASSB 첫 충전 a ≈1.7–2.1 (x 0.72–0.92) · ≈4.5–6 (x 0.21–0.32)) ↔ MSMR 갤러리형(96호) — 선택이 방전 끝 `R_kin` 봉우리 · 창 식별성(95호)을 정한다 | 74 · 75 · 91 · 95 · 96 · 99 · 105 · 106 · 107 |
| Wa 영역 선결 | (투) | 면적 ↔ `j₀` 노브를 따로 흔들기 전에 옴 지배(Wa ≪ 1) 여부 · 확산 길이 축(94호) · 신호가 보일 율(109호 — 0.1 C 에서 ≤2 %)을 먼저 적는다 · 형제 줄(105호): 율 판별은 동역학 영역 i/i₀(남은 면적 기준)을 같이 — Tafel 영역이면 면적형 손실이 율 무관 상수 이동 | 76(`[재현]` Wa 0.008–0.1) · 94 · 105 · 109 |
| 신품 `θ₀` 폭 | (그) | 한 값이 아니라 출처 넷의 폭 — DEM 지도(77호) · 해석식(68호, SE 거울판) · 첫 충전 비 하한 · 입도 대표값 선택(82호) · 조건: 율 하한 빼기(83호) · SE 산화 전하 보정(112호 — 비 > 1) | 65 · 68 · 77 · 82 · 83 · 112 · 114 |
| 측면(반경) 축 | (프) | 측면 균일(1D)로 둘 때 측면 `η(r)` 이 `LAM` · 저항 파라미터로 흡수될 수 있음을 적는다 | 80(`[해석]`) · 106(저자 한계 인쇄) |
| 실측 LLI 대조 | (브)(츠) | truth LLI(재고 = C)와 실측 LLI 를 맞댈 때 정의(A · B · C) · 영점 · CE 결손의 구조 채널 대조 — 정본 [[reference-electrode-halfcell-dma]] 규약 ①–④ | 78 · 79 · 89 · 90 · 107 · 113 · 114 |
| 양극 부피 변화 입력 | (노) | 한 값이 아니라 폭 [격자 −5.1 % ↔ 입자 −7.8 %(69호)] + 층위 라벨(격자 · 입자 · 깊이 · 전극 평균) — 격자 층위 안 연구실 · 프로토콜 폭(72 · 78호 ×1.1–2.6)은 따로 · 깊이(79호)는 경고 — 정본 [[assb-operando-pressure-signal-attribution]] 층위 결정 | 69 · 72 · 78 · 79 · 83 · 87 · 94 · 97 · 103 · 105 · 113 |

## 쓰는 법

- truth 설계 문서에 **R1–R8 각각의 충족 여부를 표로 적는다.** 충족하지 못한 요구가 있으면 그 truth
  로 낸 "접촉 손실과 `LAM_PE` 는 갈린다/안 갈린다" 결론에 **그 요구 ID 를 조건으로 붙인다.**
- R1 을 못 지키는 모델(현재 PyBaMM P2D·SPM 포함)은 **음성 대조**로만 쓴다 — "이 모델에서는
  정의상 같다" 를 확인하는 용도.
- 곱 축퇴 처방([[assb-lampe-contact-product-degeneracy]])의 각 단계는 이 요구가 truth 에 들어 있을
  때만 합성 데이터로 시험할 수 있다 (예: 1단계는 R5, 압력 연산자는 R4).
- 문헌 값 · 명제를 truth 입력으로 옮길 때는 카드 [[assb-contact-loss-vs-lampe]] '옮길 때의 표기 규칙'(2026-11-17)을 쓴다 — 저압 값 · 입도는 (미)(비) · 압력 값은 [[assb-stack-pressure-operating-window]] '압력 값 표기 칸'.
- **설계서 v1** (2026-11-24 · 문서만 · 검토 대기): `followups/assb-contact-truth/DESIGN_v1.md` — R1–R8 충족 표(§2-8) · 노브 정의(§2) · 첫 실행 C1 = 원장 §3-b (차)(처) 사전 등록(§5) · 상태판 `followups/assb-contact-truth/STATUS.md`. 수치는 그쪽 실행 기록이 정본이고 이 페이지로 옮기지 않는다.

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
- 113호를 R4 충족 표본으로 쓰지 않는다 — RuO₂/LPSX 는 SE 부반응 전용 대조(CAM 부피 변화 0)이지 θ 전용 조작이 아니고, 효과는 압력 · 형태의 정성(틈 폭 · 분율 0)이다. 균열 면적의 SOC 개폐도 R8 형태가 아니라 측정 설계 조건이다.
- 114호를 R7 · R8 충족 · 결정의 근거로 쓰지 않는다 — 두 낱말은 한 라벨이고(φ · u 측정 인쇄 0), 'SoC 주기형' · '첫 충전 계단' 은 상태마다 한 시야의 정성 영상이며 `θ(N)` 궤적이 아니다. R2 쪽 '느린 회수' 읽기도 첫 사이클 · 다른 셀 · LE c(x) 곡선을 옮긴 가정 위다.
- 116호를 R1 · R4 · R7 표본으로 쓰지 않는다 — 1D 유속 척도 구성 위의 대수 · κ 측정 0 · 압력 → κ 는 106호에서 옮긴 Persson 사상이다. 'κ·c^m = `LAM_PE` 열' 도 이 모형 구성의 귀결이지 실셀 명제가 아니다.
- 설계 선택지 기록(2026-11-17)을 구현 · 검증으로 쓰지 않는다 — 코드 0 · 실행 0 · 선택지는 흡수한 편의 인쇄 · 우리 재현에서 왔다.
- 설계서 v1(`followups/assb-contact-truth/DESIGN_v1.md`)의 R1–R8 충족 표를 truth 의 검증으로 쓰지 않는다 — 문서만 · 실행 0 이고, '충족' 은 설계상의 처리다(R5 · R8 등은 가정으로 넣는 것).

## 관련

- [[assb-contact-loss-vs-lampe]] — 닻 카드 (원래 "새 제약" 에 있던 자리)
- [[assb-lampe-contact-product-degeneracy]] — 곱 축퇴와 처방 표
- [[assb-pressure-reapplication-separation-test]] — R4 의 실측 쪽
- [[composite-cathode-percolation-utilization]] · [[assb-apparent-capacity-decomposition]] — `θ_AM` 의 정의
- [[degradation-degeneracy]] — 합성 truth 프로젝트
