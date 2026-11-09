<!-- digest 표준 양식. COMPREHENSIVE / paper-level STANDALONE digest. 모체 카드와 겹치는 서술은 짧게 넘기고 이 판에만 있는 것을 자세히. -->
# 무른 + 강체 입자 혼합물의 미시역학 압밀 모델 — 학회 단편 (Powders & Grains 2021) · PRE 2020 판의 요약 + 시작 상태 표 (φ0 · Z0) · NSCD contact dynamics + FE 2D — Cárdenas-Barrantes, Cantor, Barés, Renouf, Azéma (EPJ Web of Conferences 2021)

> slug `cardenasbarrantes2021_soft_rigid_mix_compaction_proceedings` · DOI `10.1051/epjconf/202124902008` · type `NSCD+FEM 2D 다입자 (LMGC90 — 강체 + neo-Hookean 비압축 FE 원판 혼합, 등방 압축, μ 0 · 0.2) + 미시역학 압밀 이론 — 학회 단편 (4 쪽)` · PDF `d42d682a-3._A_micro-mechanical_compaction_model_for_granular_mix_of_soft_and_rigid_particles.pdf` · digested `2026-11-09` · status ✅
>
> ⚠ **이 판의 지위**: 같은 저자 · 같은 계산 · 같은 이론을 4 쪽으로 줄인 **학회 발표 단편**이다 (모체 =
> `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd`, PRE 102, 032904 (2020)).  **모체에 없는 것 셋만** 이 판의 고유
> 가치다 — ① **Table 1: 시작 (jammed) 상태의 φ0 · Z0 를 κ · μ 별로** ② 변형 원판의 **FE 메시 삽도**가 있는 스냅숏 (그림 1)
> ③ 식 (5) 와 Platzer 모델을 **한 그림에 겹친** 비교 (그림 2 · 3).  나머지는 모체 카드를 정본으로 본다.
>
> ⚠⚠ 전이 금지 (모체와 같음): **2D 원판 · 평면변형률 · 초탄성 (가역) · P/E 무차원** — 절대값 0 건 전이.
>
> **같은 그룹 3 편 묶음**: 모체 PRE 2020 (위) · **이 카드** (학회 단편) · `cardenasbarrantes2022_soft_hard_grains_compaction_experiment_dic`
> (2D 실험 검증 · 일축 확장).  ⚠ 이 판의 참고문헌에는 **모체 PRE 2020 이 없다** — "previous work [17]" 는 순수 변형 입자 원판의
> Cantor et al. PRL 124, 208003 (2020) 을 가리킨다.

---

## 0. 왜 우리에게 (짧게 — 상세는 모체 카드 §0)

- 모체와 같은 이유: **강체 (= 우리 NCM) + 무른 (= 우리 SE) 혼합의 입자 해상 압밀** — 재설계 후보 **B (NSCD + FE)** 의 실례이며,
  φ(P) · K(φ) · Z(φ) · 단일 입자 시험이라는 **재설계 공통 검증축**을 준다.
- **이 판만의 쓸모**: 압밀 법칙 식 (5) 의 **입력인 시작 상태 (φ0, Z0) 를 표로** 적어 두었다 — 재설계 모델의 출력 곡선을 이 형식으로
  비교할 때 "시작 상태를 무엇으로 기록해야 하는가" 의 견본.  그리고 **두 모델 (식 5 · Platzer) 이 같은 곡선을 똑같이 잘 맞춘다**는
  것을 한 그림으로 보여 준다 — **φ(P) 곡선 적합만으로는 모델을 가를 수 없다**는 교훈.

---

## 1. 한 줄 요약

**KR:** 2D 비정칙 접촉 동역학 (NSCD, LMGC90) 으로 강체 + 비압축 neo-Hookean 원판 (FE 92 삼각형) 혼합 1500 입자를 jammed 상태에서
등방 압축해, φ 가 φ0 에서 φmax 로 포화하고 K 가 φmax 에서 발산하며 Z − Z0 = ξ(φ − φ0)^α (ξ ∼ 5.1, α ∼ 0.5) 가 κ · μ 무관함을 보이고,
입상 응력 텐서 + 단일 입자 상자 압축 (b ≃ 0.14) 으로 **φmax(κ) 하나만 거시 적합하는 압밀식 (5)** 을 제시한 학회 단편.  시작 상태는
φ0 = 0.805–0.815, Z0 = 3.3–3.7 (Table 1).

**EN:** A four-page Powders & Grains 2021 version of the authors' PRE 2020 study: 2D NSCD (LMGC90) isotropic compaction of 1500 rigid +
incompressible neo-Hookean FE disks; φ saturates at φmax, K diverges, Z − Z0 = ξ(φ − φ0)^α (ξ ∼ 5.1, α ∼ 0.5) independent of κ and μ;
granular stress tensor + single-particle box law (b ≃ 0.14) give a compaction equation (Eq. 5) with φmax(κ) as the only macroscopic
fit.  Adds a table of initial jammed states (φ0 = 0.805–0.815, Z0 = 3.3–3.7) and a figure overlaying Eq. (5) with the Platzer model.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | A micro-mechanical compaction model for granular mix of soft and rigid particles |
| 저자 | **Manuel Cárdenas-Barrantes**¹, **David Cantor**², **Jonathan Barés**¹, **Mathieu Renouf**¹, **Emilien Azéma**¹˒³ |
| 소속 | ¹ LMGC, Université de Montpellier, CNRS, 163 rue Auguste Broussonnet, Montpellier, France · ² Department of Civil, Geological and Mining Engineering, Polytechnique Montréal, 2500 Chemin de Polytechnique, Québec, Canada · ³ Institut Universitaire de France (IUF), Paris, France |
| 출판 | **EPJ Web of Conferences 249, 02008 (2021)** — *Powders and Grains 2021* |
| DOI | 10.1051/epjconf/202124902008 |
| 날짜 | 접수 · 게재일 [미확인] (PDF 에 없음) |
| 판권 | © The Authors, EDP Sciences · **CC BY 4.0** 공개 |
| 영상 | "A video is available at https://doi.org/10.48448/cevr-fq53" (1 쪽 각주) |
| 코드 | LMGC90 (refs [19–21]) |
| 분량 | 4 쪽 · 그림 5 · 표 1 · 식 5 · 참고문헌 32 |
| 소재 | ⛔ SE · CAM 아님 — 모델 소재 (강체 원판 + neo-Hookean 비압축 원판) |
| 연구유형 | 수치 (NSCD + FEM, 2D) + 해석 이론 — 학회 단편 |

---

## 3. 핵심 수치 — stated / digitized

### 3-1. ★ Table 1 — jammed 시작 상태 (stated · **이 판에만 있음**)

| | κ = 0.2 | κ = 0.5 | κ = 0.8 | κ = 1 |
|---|---|---|---|---|
| **φ0**, μs = 0.0 | 0.815 | 0.811 | 0.807 | 0.807 |
| **φ0**, μs = 0.2 | 0.814 | 0.811 | 0.807 | 0.805 |
| **Z0**, μs = 0.0 | 3.4 | 3.6 | 3.5 | 3.4 |
| **Z0**, μs = 0.2 | 3.3 | 3.7 | 3.5 | 3.5 |

읽는 법:
- **φ0 는 κ 가 클수록 아주 조금 낮다** (0.815 → 0.807, μ 0) — 무른 입자를 교체한 뒤에도 출발이 사실상 같은 강체 패킹이라는 뜻
  (교체 뒤 다시 jam 시켰는지는 [미확인]).
- **μs = 0 인데 Z0 = 3.4–3.6** — 모체 본문은 "원판에서 μs → 0 이면 Z0 → 4" (문헌) 라 쓴다.  등방 (isostatic) 값 4 보다 낮은 이유
  (rattler 포함 · 준비 이력 등) 는 [미확인].  ⚠ **이 표를 인용할 때 Z0 정의 (rattler 포함 여부) 를 함께 [미확인] 으로 표기**.
- φ0 가 마찰에 거의 무관 (≤ 0.002) — 모체의 "φ0 · φmax 가 마찰로 조금 내려간다" 중 **φ0 쪽은 이 시료에서 거의 0**.

### 3-2. 입력 · 결과 (stated — 모체와 같은 값)

| 양 | 값 |
|---|---|
| Np | **1500** (강체 원판, "small size polydispersity") → 상자에 무작위 배치 → **"gently compressed to reach the jammed state"** |
| 교체 | 부피 **κVp** 를 무른 원판 (**92 삼각형**) 으로 균질 교체, κ ∈ **[0.2, 0.5, 0.8, 1.0]** |
| 구성식 | neo-Hookean **비압축**, **ν = 0.495**, 영률 E (강체 E → ∞) |
| 마찰 | **μ = 0.0 · 0.2** (이 판은 κ = 1 의 μ 0.4–0.8 계열 없음) |
| 벽 마찰 · 중력 | 0 · 0 |
| 안정 판정 | φ 변화 **< 0.01 %** |
| 관성수 | **I ≪ 10⁻⁴** 를 매 단계 강제 (벽 속도 제어) — 모체 표현은 "below 10⁻⁴" |
| 배위수 법칙 | Z − Z0 = ξ(φ − φ0)^α, **ξ ∼ 5.1, α ∼ 0.5**, κ · μ 무관 |
| 단일 입자 | φp,0 = **π/4**, **b ≃ 0.14** |

### 3-3. 그림에서 읽은 값 (digitized — TREND)

- 그림 1: κ = 0.5, μ = 0.2 에서 **P/E = 2.0 × 10⁻²** (원판 대부분 둥긂) · **2.0 × 10⁻¹** (다각형화, 강체 사이 작은 공극) — 인쇄값.
- 그림 2: φ0 ≈ 0.80–0.82 → κ = 1 (μ 0) 은 P/E ≈ 0.25 에서 ≈ 0.97, κ = 0.2 는 P/E ≈ 0.4 에서 ≈ 0.88 (μ 0) / ≈ 0.86 (μ 0.2).
- 그림 3: K/E 가 κ 0.2 에서 φ ≈ 0.85 (μ 0.2) · 0.87 (μ 0) 부근 발산, κ 1 은 φ ≈ 0.96–0.98.
- 그림 4: Z − Z0 최대 ≈ 2.1–2.2 @ φ − φ0 ≈ 0.145.
- 그림 5: φp 는 Pp/E ≈ 10⁻⁴ 에서 ≈ 0.785 (= π/4), Pp/E ≈ 0.75 에서 ≈ 0.99.

### 3-4. 이 판에 **없는** 것 (모체에는 있음)

Secondi · Zhang 식 대조 · Table I (P0(κ)/E) · **φmax vs κ 그림과 상분리 식 (모체 식 14 · 15)** · Voigt 근사 (모체 식 8) · κ = 1 의
μ 0.4–0.8 계열 · 부록 (Platzer 다시 쓰기) · 메시 수렴에서 "E 변화 vs Pp 변화" 비교 (모체 그림 8b 빨강).  계산 비용 · Δt · E 절대값은
모체와 마찬가지로 없음.

---

## 4. 방법 ★ (모체와 같은 방법 — 차이만 자세히)

- **NSCD** (ref [18] Jean 1999): FE 와 접촉 동역학 결합, **비관통 (non-penetrability) + 건조 마찰 (dry friction)** 접촉 법칙.
- **LMGC90** (refs [19–21]).
- 준비: 강체 원판 1500 개 무작위 배치 → **부드럽게 압축해 jammed 상태로** (모체: "simple geometrical rules … to build a dense
  system") → 부피 κVp 를 무른 원판으로 교체.
- 하중: jammed 상태에서 경계에 응력 P 를 점진 · 준정적 등방 인가 (하중 단계) · 안정 = φ 변화 < 0.01 % · **벽 속도를 관성수로 제어해
  매 단계 I ≪ 10⁻⁴**.
- 정의: φ = Vp/V · K(φ) = (dP/dφ)(dφ/dεv), εv = −ln(φ0/φ).
- 이론 (이 판의 식 번호):
  - (1) `P = (Zφ/π) σℓ`, σℓ = ⟨f^c · ℓ^c⟩_c / ⟨d⟩² (입상 응력 텐서 σij = (1/V) Σ f_i^c ℓ_j^c = (N_c/V)⟨f_i^c ℓ_j^c⟩_c, 평균 응력 = (σ1 + σ2)/2 · Z = 2N_c/N_p · ref [25])
  - (2) `Pp/E = −b ln[(φp,max − φp)/(φp,max − φp,0)]`, φp,0 = π/4, **b ≃ 0.14** — ⚠ 이 판은 b 를 **"a constant of proportionality called
    the yield stress"** 라 부른다 (초탄성 입자인데 "항복응력" — 모체는 이 이름을 쓰지 않는다; 무차원 상수다).
  - Kp(φp) = (dPp/dφp)(dφp/dεv,p), εv,p = −ln(φp,0/φp)
  - (3) `K ≡ (Zφ/2π) Kp + 𝒪` · (4) `P ≃ (Zφ/2π) Pp`
  - (5) ★ `P(φ, κ)/E ≃ −(bφ/2π){Z0 + ξ(φ − φ0)^α} ln[(φmax(κ) − φ)/(φmax(κ) − φ0)]` — 모체 식 (12) 와 같다.
  - Platzer 모델 (본문 2 쪽): `P = −P0(κ) ln[(φmax − φ)/(φmax − φ0)]` — **음수 부호 있음** (모체 본문 식 (4) 의 부호 누락과 대조).
- **입자 처리**: 모체 카드 §4-6 과 같다 — 무른 입자는 **진짜 형상 변화 (초탄성, 가역)**, 강체는 재배열, 접촉은 비관통 + 마찰 (μ 하나),
  크기비 없음, 2D.

---

## 5. 결과 — 절별 (모체와 같은 결론 · 이 판의 서술 차이 표시)

1. **압밀 곡선 (그림 2)**: φ 는 잘 알려진 φ0 에서 출발해 φmax 로 점근 · 마찰이 커지면 φ0 · φmax 가 조금 내려간다 (이유: 마찰 없는
   경우 재배열이 더 잦음, refs [23, 24]) · 식 (5) 와 Platzer 모두 그린다.
2. **체적탄성률 (그림 3)**: K 가 φ 와 함께 오르고 φmax 에서 발산 — "there is no more void space and the assembly of grains starts to behave
   as a continuous and rigid material".  식 (3) 예측과 Platzer 미분을 함께 그린다.
3. **연결성 (그림 4)**: Z − Z0 = ξ(φ − φ0)^α, ξ ∼ 5.1 · α ∼ 0.5, 혼합비 · 마찰 무관 → 이원 혼합으로 확장.
4. **단일 입자 (그림 5)**: φp–Pp 가 다체 φ–P 와 비슷 · 식 (2) 로 잘 기술 · 메시 Ne = 92 → 968.
5. **압밀식 (5)**: 구조 매개변수 (Z0, φ0 = 초기 상태 · b = 단일 입자 · ξ, α = φ–Z 사상) 로 정해지고 **φmax 만 거시 자료에 맞춘다** (κ · μ 별).
6. **결론**: 혼합 압밀의 본질은 **단일 입자 특성 + 연결성 진화**로 잡힌다 · 다음 길 = **3D 계 · 더 실제적인 형상의 혼합 · 다른 압밀
   조건**.

---

## 그림별 (원 캡션 요지 + MPM 관점)

> 파일: `litdb/figures/cardenasbarrantes2021_soft_rigid_mix_compaction_proceedings/` · 300 dpi 손 크롭 (캡션 제외 · 테두리 잉크 0 · 전부
> 열어 확인).  표 `tab_1.png` · 식 `eq_05_mixture_compaction_law.png` 포함.

| 파일 | 원 캡션 요지 | MPM 관점 (재설계가 재현해야 할 것 · 후보 대응) |
|---|---|---|
| `fig_1.png` | 그림 1 — κ = 0.5 · μ = 0.2, 서로 다른 환원 압력 P/E 의 화면; 삽도 = 사용한 FE 메시; 강체 = 회색 | κ = 0.5 · μ = 0.2 침대의 두 압력 (P/E = 2.0 × 10⁻² · 2.0 × 10⁻¹) 스냅숏과 변형 원판의 FE 메시 (92 삼각형) 삽도 — 입자 하나당 요소 ~100 개로도 다각형 형상 변화가 그려진다는 해상도 감각을 준다.  후보 B (입자별 FE) 의 해상도 하한 참고값이고, MPM 이라면 SE 한 알당 격자 칸 수가 같은 역할 (우리 n_grid 384 · dx ≈ 141 nm 에서 ⌀1 µm SE ≈ 7 칸 — 파생 산술). |
| `fig_2.png` | 그림 2 — φ vs P/E (κ 0.2–1, μ 0 · 0.2) + 미시역학 식 (5) 예측 + Platzer 모델 | 같은 자료 (PRE 2020 그림 3a · 9a) 위에 식 (5) (파선) 와 Platzer 식 (점선) 을 한 판에 겹쳤다 — 둘 다 곡선을 잘 따르므로 'φ(P) 곡선이 맞는다' 만으로는 모델을 가를 수 없다.  재설계 후보 비교도 φ(P) 하나가 아니라 Z(φ) · K(φ) · φmax(κ) 같은 2차 관측량까지 맞춰야 판별된다. |
| `fig_3.png` | 그림 3 — K/E vs φ (κ 별, μ 0 · 0.2) + 식 (3) 예측 + Platzer 모델에서 계산한 K | K/E 의 φmax 근처 발산을 식 (3) (단일 입자 Kp × Zφ/2π) 과 Platzer 미분이 함께 따라간다 — 다체계 강성이 '단일 입자 벌크 응답 × 연결성' 으로 환산된다는 이 그룹 논지의 그림.  재설계 MPM 에서 SE 단일 입자 응답과 침대 응답을 따로 재어 이 환산이 성립하는지 확인할 수 있다 (후보 C 의 벌크탄성 처방과 같은 방향). |
| `tab_1.png` | Table 1 — 혼합 시료들의 jammed 상태 φ · Z 값 | 시작 상태 기록: φ0 = 0.805–0.815 · Z0 = 3.3–3.7 (κ · μ 별) — 식 (5) 의 입력이며 재설계 모델도 압밀 곡선과 함께 '시작 패킹의 φ0 · Z0' 를 기록해야 비교가 된다.  본문은 'μ → 0 이면 Z0 → 4' 라는데 μ = 0 에서 Z0 = 3.4–3.6 (rattler 포함 여부 [미확인]) — 본문은 이 표를 'Tab. 2' 로 부른다 (번호 불일치). |
| `fig_4.png` | 그림 4 — Z − Z0 vs φ − φ0 (모든 κ, μ); 파선 = 거듭제곱 Z − Z0 = ξ(φ − φ0)^α | Z − Z0 = ξ(φ − φ0)^α, ξ ≈ 5.1 · α ≈ 0.5 가 κ · μ 무관 (PRE 2020 그림 6 과 같은 자료, 표지만 다름).  단일 속도장 MPM 은 Z 를 정의할 수 없어 이 법칙을 쓰려면 입자 정체성이 남는 방법 (A′ · B · C · C′ · D0) 이 필요하다. |
| `fig_5.png` | 그림 5 — 입자에 가한 환원 압력 vs 충전률, 메시 해상도 Ne 별 | 단일 입자 상자 압축의 메시 수렴 (Ne = 92 → 968) — 결과가 거의 안 변하므로 2D 원판 하나당 ~100 요소면 충분하다는 근거.  재설계 B (입자별 FE) 의 요소 수 · MPM 의 SE 한 알당 칸 수를 정할 때 같은 형식의 수렴 시험을 먼저 하라는 선례. |

**모체 그림과의 대응**: 그림 2 ≈ 모체 그림 3a + 9a (두 모델 겹침) · 그림 3 ≈ 모체 그림 4 + 7 (식 3 vs 모체 식 13) · 그림 4 = 모체 그림 6 ·
그림 5 = 모체 그림 8b (빨강 계열 없음).  이 판의 그림 3 은 **원 = μ 0 · 마름모 = μ 0.2** 로 표식을 바꿔 그렸고, κ = 0.2 에서 μ 0 이
더 높은 φ 에서 발산한다 — 모체 그림 4 · 7 의 표식 범례 (채움/빈) 가 뒤바뀌었다는 모체 카드의 판단을 뒷받침한다.

---

## 7. Post-processing ★

모체와 같다 (φ = Vp/V · K = 압밀 곡선 미분 · Z = 2N_c/N_p · 입상 응력 텐서 · 단일 입자 φp(Pp/E) · φmax 만 비선형 적합).  수송 · 피복 ·
힘사슬 · 탈압 없음.

---

## 8. 우리 DEM + MPM 대비 (짧게 — 상세는 모체 카드 §8)

- **같은 점**: 무른상 거의 비압축 (ν 0.495 ↔ 우리 MPM ν 0.49) · "강체가 많을수록 최대 밀도 낮음" 방향.
- **다른 점**: 2D · 초탄성 (가역) · 등방 · 크기비 없음 · 점착 없음 — 우리 3D · J2 소성 · 일축 · AM ≫ SE · (MPM) 융합.
- **Table 1 의 쓰임**: 우리 재설계는 **느슨한 패킹에서 출발** (1저자 11-09) — 출발 상태를 φ0 · Z0 (와 겹침 0 확인) 로 기록하는 형식을
  이 표에서 빌린다.  ⚠ 2D 값 (φ0 ≈ 0.81, Z0 ≈ 3.5) 은 우리 3D 로 옮기지 않는다.
- **frame[4]**: 식 (5) 의 상수는 같은 시뮬레이션 안에서 정해진다 — 우리 후보들은 각자 랩 기공률에 보정하고 이 형식은 비교 축으로만.

---

## 9. 깊은 통찰 (이 판에서 새로 얻는 것만)

1. **"두 식이 같은 곡선을 똑같이 잘 맞춘다" (그림 2) = 곡선 적합은 모델 판별력이 약하다.**  [DEM 우선 (수영)] 후보 비교를 φ(P)
   한 장으로 끝내면 안 된다 — K(φ) · Z(φ) · φmax(κ) · 국소 관측량 (2022 실험판) 까지 같이 본다.
2. **시작 상태 표는 압밀 비교의 필수 머리말이다.**  같은 압밀식도 φ0 · Z0 가 다르면 다른 곡선이 된다 — 재설계 후보마다 출발 패킹의
   φ0 · Z0 (와 겹침) 를 결과 전에 기록하라.
3. **이름이 물리를 바꾸지는 않는다** — 이 판이 b 를 "yield stress" 라 부르지만 초탄성 입자의 무차원 비례상수다.  우리 J2 소성 SE 로
   옮길 때 진짜 항복응력 σ_y 가 들어갈 자리와 혼동하지 말 것.

---

## 10. [DEM 우선 (수영)] 트랙 — 함의 + 행동 (모체 카드 §10 을 정본으로, 이 판의 추가분만)

| 후보 | 이 판이 더하는 것 |
|---|---|
| A · A′ | 출발 상태 기록 형식 (φ0 · Z0) — A′ 는 Z0 를 정의할 수 있고 A 는 못 한다 |
| **B** | **입자당 ~92 요소의 메시 삽도 + 메시 수렴 (92 → 968)** — 입자별 FE 의 해상도 하한 참고 |
| C · C′ · D0 | Table 1 형식으로 출발 패킹 (φ0 · Z0) 을 기록하면 식 (5) 형식 비교가 가능 |

행동:
1. 재설계 등록 문서의 "출발 상태" 칸에 **φ0 · Z0 · 겹침 (≈ 0 확인) · 준비 방식** 을 결과 전에 적는다 (Table 1 형식).
2. 후보 비교 그림은 **φ(P) + K(φ) + Z(φ) (정의되는 후보)** 를 한 세트로 — 그림 2 의 교훈.
3. [문헌] 학회 영상 (`doi.org/10.48448/cevr-fq53`) 은 시료 준비 · 압축 과정 확인용 (내용 미확인).

---

## 11. 인용 가능 문장 (원문 그대로)

- (p. 2) *"The modulus K increases with φ and diverges as it approaches to φmax. This comes from the fact that there is no more void space
  and the assembly of grains starts to behave as a continuous and rigid material."*
- (p. 4) *"The model shows that the essential behavior of the compaction of this mixture (which also covers completely deformable systems)
  is captured from the characterization of a single particle, together with the evolution of particle connectivity."*
- (p. 4) *"The natural path of this work is the analysis of more real systems, such as 3D systems, composite assemblies of particles with
  more realistic geometries, all under different compaction conditions."*

---

## 12. 주의 / 한계 / PDF 가 말하지 않는 것

- **학회 단편** — 동료심사 · 상세 방법은 모체 (PRE 2020) 가 정본.  수치 인용은 가능하면 모체에서, Table 1 만 이 판에서.
- **내부 불일치**: 본문이 시작 상태 표를 **"Tab. 2"** 로 부르는데 실제 표는 **Table 1** 하나뿐 · b 를 "yield stress" 라 부름 (§4) ·
  자기 모체 (PRE 2020) 를 인용하지 않음.
- **Z0 정의**: μ = 0 에서 Z0 = 3.4–3.6 < 4 — rattler 처리 [미확인].
- 2D · 초탄성 · 등방 · 크기비 없음 · 계산 비용 없음 · 접수/게재일 없음.

---

## 13. 기법 미니 용어집

모체 카드 §13 과 같다 (NSCD · Signorini · LMGC90 · neo-Hookean · κ · φ0 · Z0 · φmax · ξ · α · b · σℓ · I).  이 판에서 덧붙일 것:
**Powders & Grains** = 입상체 분야의 정기 국제 학회 (이 판은 그 2021 회 발표 단편).

---

## 14. 관련 카드

- **모체 (정본)**: `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd`.
- **실험 검증**: `cardenasbarrantes2022_soft_hard_grains_compaction_experiment_dic`.
- **경/연 혼합 압밀**: `bouvard2000_hard_soft_powder_densification` · `martinbouvard2003_dem_composite_cold_compaction`.
- **후보 B 형제 (MPFEM)**: `demirtas2021_mpfem_hollow_sphere_die_compaction` · `pycompact2025_dem_mpfem_workflow`.
- **후보 C**: `zunker2024_bulk_elastic_partII` (벌크탄성 구간 — 식 (3) 의 "단일 입자 벌크 응답" 과 같은 방향).

---

## 🗨️ Q&A 로그

- (2026-11-09 digest — 아직 질문 없음)
