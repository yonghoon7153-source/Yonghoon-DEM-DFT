---
title: ASSB 합성 truth 의 접촉 손실 요구 — 카드 물음을 truth 단계에서 미리 답하지 않으려면
description: "Requirements for an ASSB synthetic truth in which contact loss is NOT pre-identified with LAM_PE: a separate capacity-multiplying θ, Li-holding disconnected particles, dead volume that does not become electrolyte, θ-only manipulation, area-proportional double layer, relaxation time as a truth parameter, φ vs u distinction, and θ(N) shape as an explicit assumption"
created: 2026-09-23
updated: 2026-10-03
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/deng2021_assb-reduced-order-model-pade-polynomial.md, raw/papers/raijmakers2020_thin-film-assb-model-double-layer-dc-ac-joint-fit.md, raw/papers/schmidt2024_nitsche-contact-delamination-resolved-ssb-cathode.md, raw/papers/bielefeld2023_useful-models-ssb-simplicity-perspective.md, raw/papers/jiao2023_electro-chemo-mechanical-se-modulus-conductivity-intergranular-czm.md, raw/papers/chen2013_sofc-miec-composite-electrode-percolation-theory.md, raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd-si.md, raw/papers/li2024_assb-composite-cathode-model-contact-area-edl.md, raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md, raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md, raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd.md, raw/papers/sakka2022_pressure-3d-structure-composite-cathode-xct.md, raw/papers/ren2023_oxide-ssb-composite-cathode-architecture-perspective.md, raw/papers/bielefeld2022_voids-kinetics-morphology-composite-cathode-fem.md, raw/papers/bielefeld2020_effective-ionic-conductivity-binder-composite-cathode.md, raw/papers/asheri2023_data-driven-multiscale-ssb-delamination-surrogate.md, raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md]
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
| 활물질 분율 `ε_p` (입자 통째 비연결 `u`) | 27호 Sinzig P2D (오프셋 `1−u`) · 28호 Bizeray SPM 묶음 `Q_th` · 37호 Li 2024 · **58호 Asheri** (박리 `⟨d⟩` 가 식 (32) `a·(1−⟨d⟩)` 로만 들어가고 입자 유입은 손상 무관) | `LAM_PE` 와 **정의상 같다** |
| 유효 계면 면적 `A_eff` (표면 피복 `φ`) | 37호 Li 2024 · 50호 Miß (기하 `a_v` 고정) · 56호 Bielefeld 2022 (반구 void) · **93호 Bielefeld 2023 제안**(결론 "evolution of the porosity, tortuosity and specific surface area upon cycling" 을 수정 Newman 에 — 계산 0 · 통째 고립이 갈 자리 없음) · **94호 Schmidt 2024**(3D 해상 · Nitsche 접촉 — `φ` 를 역학이 계산 · 박리 면 BV 0 · j₀ 고정 · 무접착 가역 법칙) | 반응 상수 `k` 와 **곱으로만** 들어간다 — OCV·용량에 안 보이고 계면 화학 열화와 항등(37호). 3D 해상 모델에서는 이 항등이 **부분적으로만** 성립(56호 모델 명제) · 94호 `[재현·가정]`: 면적 손실의 전압 몫이 BV(≈6 mV)보다 입자 안 확산 분극(≈67 mV)으로 — 고정 컷오프에서 용량 결손처럼 보이는 η 형 |
| (참고) **자리 없음** — CAM\|SE 불파괴 · 손상은 입계에만 | 83호 Jiao 2023 (3D 복합 양극: SI 가정 "(5) … assumed as perfect and couldn't be damaged" · 2D 입계 CZM: 손상 > 80 % → 그 영역 σ_ion 0 · 용량 계산 0) | 카드 물음의 기구(박리 → 접촉 손실)가 모델에 없다 — "SE 탄성률은 전기화학에 영향 없음" 같은 결론이 이 부재의 귀결이 된다. 합성 truth 로는 **접촉 항 0 의 음성 대조판** |

어느 자리로 넣든 truth 가 카드 물음에 **미리 답한다**. 아래 요구는 그것을 피하기 위한 것이다.

## 요구 목록

| ID | 요구 | 출처 (assb 호) | 상태 |
|---|---|---|---|
| **R1** | **용량에 곱해지되 `ε_p` 와 별개인 `θ`** 를 둔다 | 37호 · **100호 Deng 2021**(37호가 물은 축약 모형 — 확인) | 계보의 모든 모델이 위반(27·28·37·58호) · 83호는 CAM\|SE 접촉 항 자체가 없다(가정) · 100호 축약 모형(ROM)도 위반 — θ · ε_p 둘 다 0 · 면적 A 한 값이 용량 극 · 수송 이득 · i₀(A·k_pos)에 같이 들어간다(37호 A_eff 는 그 꼴 위의 BV 분모 추가) |
| **R2** | **비연결 입자가 자기 SOC 의 Li 를 붙든다** — 끊긴 순간의 리튬화 상태가 재고에서 빠진다(LLI 와도 얽힘) | 37호 | 계보 측정 0 (38호 Conforto 도 "inactive" 로만) |
| **R3** | **죽은 부피가 전해질이 되지 않는다** — 비연결 입자·void 가 이온 경로로 바뀌지 않게 | 37호 · 56호(검증 구조가 void 14 % 를 SE 로 채움) · 57호 · **93호**(원칙 인쇄 — "The assumption that all volume that is not filled with CAM contains electrolyte no longer applies" · 같은 저자 56호 검증 구조는 위반) | 56호가 정확히 이것을 위반 |
| **R4** | **`θ` 에만 반응하는 조작** 을 truth 에 둔다 (압력 되돌림 등) | 37호 · 39호 Sakka (압력이 `φ` ×1.10 · `R_ct` ×14 — 여러 인자를 같이 움직임) · 57호 (바인더 한 손잡이가 경로와 접촉 두 곱을 같이 깎음) · 56호 (`φ` 스윕은 θ-전용 아님) · 94호 (모형 — OCV · i₀ 응력 의존을 무시해 압력이 구성상 접촉만 움직이나, 움직이는 것은 `θ` 가 아니라 `φ`) | 실측·모델 모두 **θ-전용 조작 0** — [[assb-pressure-reapplication-separation-test]] 설계 조건 참조 |
| **R5** | **면적에 비례하는 이중층** `C_dl ∝ A` | 37호 (원형 모델 `c_dl` 은 면적 무관 상수) · 43·48·51호 (여러 호의 `C` 가 이중층 상한을 수백–수천 배 넘음) · 51호 (전자 접촉 호의 `C` 는 비접촉 여집합에 앉을 수 있음) · **98호 Raijmakers 2020**(37호가 '조상' 으로 매단 편 — `c_dl` 은 **기하 면적당** F cm⁻² · 실제 계면 면적 변수 0 · 숨은 면적 인자가 k · `c_dl` 에 같은 배수(R·C 불변) · 값은 DC + AC 적합 · `c^n_dl` 등가 유전 두께 0.67–2.2 µm `[재현·가정]` — 37호 F(전극 전체) 꼴은 조상에 없는 변형) | 곱 축퇴 처방 1단계의 전제 — **검증 없이 가정하면 1단계가 truth 에서 거짓** · 조상(98호)도 'C ∝ 실제 접촉 면적' 을 시험하지 않았다(면적 하나 · 열화 0) |
| **R6** | **OCV 관측의 이완 시간을 truth 파라미터로** 둔다 | 38호 Conforto (1 h 이완 ↔ 자기 `τ=L²/D` 로 13–17 h) · 38호 SI(S3): 방전 뒤도 1 h · 기준 곡선은 **2 h** 휴지 · 충전 가지 · **4.19 V 에서 끝**(high-V 초기 여섯 사이클이 범위 밖) — 게이지 ↔ 눈금의 이완 불일치 · 범위 밖 외삽도 파라미터로 | 이완 부족이면 동역학 손실이 질량 채널로 샌다 |
| **R7** | **표면 피복 `φ` 와 통째 비연결 `u` 를 별개 변수로** 둔다 | 37호 · 39호 (CT 가 잰 것은 `φ`) · 55호 Hlushkou (void 경로 효과만) · 56호 (`φ` 자리만) · **68호 Chen 2013**(SOFC 좌표수 해석식 — `u = 1 − P^e` 와 `φ_cov = Z·sin²θ/4` 가 한 식 안의 두 인자, `[재현]`) · **94호**(`φ` 만 동적 계산 — 같은 연구실 27호의 `u` 와 두 편에 따로) | 두 효과를 한 **시뮬레이션** 구조에서 같이 계산한 편 0 · 68호 해석식은 둘을 따로 주지만 **정적 · SOFC · 검증 0** 이고 반응 속도에서는 곱 · 22호 세 점 대조 실패 |
| **R8** | **`θ(N)` 의 형태를 명시적 가정으로 적는다** — 계단형(첫 충전만) vs 점진형 | 23호 Koerver 원문("contact loss should only occur during the initial charge") ↔ 33·53호가 이것을 **역전 인용** · Barai 2021(원장 ★★★★, 사이클 축 박리 모델 — 미흡수) · 83호(입계 피로 CZM 의 N 축 — 파괴 사이클 95–1545 · 파라미터 0 · 모양 후보만 · CAM\|SE 판 아님) · 93호(결론 제안 — ε · τ · 비표면적의 사이클 진화를 수정 Newman 에 · 형태 · 자료 0) · 94호(이력 없는 가역 접촉 법칙 — N 축 누적 구성상 0 · 충전마다 열리고 방전마다 닫히는 "SoC 주기형" 이 셋째 후보 · 반 사이클 하나만 계산) | ⚠ **미결정** — 두 형태를 다 돌릴지는 사용자 결정 대기(원장 §3-b) |

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

## 관련

- [[assb-contact-loss-vs-lampe]] — 닻 카드 (원래 "새 제약" 에 있던 자리)
- [[assb-lampe-contact-product-degeneracy]] — 곱 축퇴와 처방 표
- [[assb-pressure-reapplication-separation-test]] — R4 의 실측 쪽
- [[composite-cathode-percolation-utilization]] · [[assb-apparent-capacity-decomposition]] — `θ_AM` 의 정의
- [[degradation-degeneracy]] — 합성 truth 프로젝트
