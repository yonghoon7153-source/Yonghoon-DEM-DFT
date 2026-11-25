# A Two Dimensional Tunneling Resistance Transmission Line Model for Nanoscale Parallel Electrical Contacts — Banerjee (Sci. Rep. 2019) · 부분 겹친 나란한 접촉의 전송선 모형 (TLM) — 전달 길이 λ₀ = √(ρc/(Rsh1+Rsh2)) · 끝으로 쏠리는 전류 · 터널 계면의 전압 의존 (CNT–진공–CNT 예: Rc 5 kΩ–10 MΩ)

> slug `banerjee2019_tunneling_tlm_parallel_nanoscale_contacts` · DOI `10.1038/s41598-019-50934-2` · type `theory (2D transmission-line model + Simmons tunneling, self-consistent · COMSOL FEM check) — parallel contact resistance · current crowding · CNT–CNT / CNT–metal contacts` · PDF `2._A_two_dimensional_tunneling_resistance_transmission_line_model_for_nanoscale_parallel_electrical_contacts.pdf` · digested `2026-11-03` · status ✅
> SI 없음 (본문 14 pp · 판 머리 "Published: xx xx xxxx" = 출판 직전 판 PDF) · evidence `fulltext` · 그림 `10/10 육안 확인` (**Fig. 5 재크롭** — 자동 크롭이 Fig. 6 영역을 Fig. 5 로 냈다 · **Fig. 6 재크롭** — 캡션 폭 때문에 오른쪽 절반이 빈 칸) · 캡션의 깨진 수식 (윗줄 · x̄ · 지수) 은 렌더한 쪽에서 복원 (`figures.json` `caption_note`) · 약칭 `[Bane19]`
> **계기** — Rint ② 탄소 접합 길이 법칙 v0 (`G_j = max(1, L_c/L_par)/R_j,0` · 분산판 v0) 의 *"전달 길이 미검증"* (`scripts/carbon_junction.py:145`) 에 문헌 식을 붙이기 (1저자 11-03 · 다섯 편 묶음 — `hamasaki2022_single_parallel_contact_mwcnt_conductivity` 와 짝).  ⛔ v0 동결 — 값 채택 없음.
> 수치 등급: **stated** · **figure-read ≈** · **derived(ours)**.

---

## 0. ★ 이 카드가 답하는 것

| 질문 | 이 논문의 답 | 등급 · 자리 |
|---|---|---|
| **(a) 선형인가 포화인가 · 문턱 길이** | 일정한 계면 비저항 ρc 에서 정확해: q = L/λ₀ = √((1 + R̄sh2)/ρ̄c) · **L ≪ λ₀ 이면 Rc ∝ 1/L (컨덕턴스 ∝ L)**, **L ≫ λ₀ 이면 접합 몫이 포화** (Rsh2 → 0 극한 R̄c = coth q / q · Eq. 9) · CNT–진공–CNT 계산에서 *"As L increases, the dependence of contact resistance on L becomes less significant"* | stated · Eq. (7)–(9) · p. 4–5 · p. 9 · Fig. 4 · Fig. 8(a) |
| (a) λ₀ 의 차원식 | **λ₀ = √(ρc / (Rsh1 + Rsh2))** [ρc = Ω·m² · Rsh = Ω/□] — 논문의 정규화 (ρc0 = V₀wL/I₀ = Rsh1·L²) 를 풀면 나온다 · 같은 두 도체 (R̄sh2 = 1) 의 Eq. (8) = **Rc = (Rsh/w)·[L/2 + λ₀·coth(L/2λ₀)]** | derived(ours) (논문 식의 대수 정리) |
| (a) 논문의 CNT 예에서 λ₀ 는 얼마인가 | 논문은 숫자를 **주지 않는다** → Fig. 8(a) 판독값에 위 식을 맞추면 **λ₀ ≈ 0.10 · 0.16 · 0.25 · 0.40 µm** (진공 간극 D 0.50 · 0.55 · 0.60 · 0.65 nm · V₀ 1 V) | derived(ours) · figure-read 기반 · §3-4 |
| (a) Ø0.15 µm 섬유로 옮기면 · L_par 는 | 같은 ρc (1.3 × 10⁻¹² – 1.9 × 10⁻¹¹ Ω m²) 를 VGCF (r′ 56.588 Ω/µm) 에 두면 **λ ≈ 0.27–1.1 µm** (접촉 폭 w = 지름 150 nm) · **≈ 1.0–4.1 µm** (w = 간극 창 10 nm) — 우리 L_par 0.30 µm 는 **그 밴드의 아래 끝 · 이하** (단 L_par 는 전달 길이가 아니라 접합 instance 의 단위 길이) | derived(ours) · §7-2 |
| **(b) 접합 하나의 저항 크기** | SWCNT (Ø 3 nm · ρ_L 20 kΩ/µm) 진공 터널 나란한 접촉 · L 10–100 nm · D 0.5–0.8 nm: **Rc 5 kΩ – 10 MΩ** ("agrees with previously reported experimental and theoretical works") · 계산값 (측정 아님) | stated · p. 9 · Fig. 8 |
| **(c) 터널 간극** | Simmons (1963) 공식 · 영상력 포함 · 진공 (εr 1 · χ 0) · CNT 일함수 4.5 eV · **D = 0.5–0.8 nm** (Fig. 8(b)) — Rc 는 D 0.05 nm 마다 ≈ 2–2.7 배 (Fig. 8(a)(b) figure-read) · V₀ < 0.3 V 에서는 전압 무관 (옴성) | stated · Eq. (10)(11) · p. 8–9 · figure-read |
| **(d) 망 수준** | *"The parallel tunneling contact … may be considered as the basic building block to better understand the macroscopic electrical conductivity of CNT fibers"* — 망은 다루지 않는다 | stated · p. 11 |

**한 줄 판정** — 우리 분산판 v0 (접합 간선 k 개 + 섬유 축저항 복셀) 는 이 논문 Fig. 1(d) 의 **이산 판 전송선**이다.  그러므로 *"길이 비례 · 포화 없음"* 은 국소 길이당 컨덕턴스의 법칙이고, **실효 컨덕턴스의 포화는 우리 풀이가 이미 만든다** — 그 길이는 보정된 R_j,0 가 정한다 (λ_model = √(R_j,0·L_par/(r′_i + r′_j))).

## 1. 한 줄 요약

미시간주립대 Banerjee · Luginsland · Zhang 은 두 나노선 (또는 박막) 이 길이 L 만큼 부분적으로 겹치고 얇은 계면층 (저항층 또는 터널 절연층, 두께 D) 을 사이에 둔 **나란한 접촉**을 2D 집중정수 전송선 (TLM) 으로 쓰고, 계면 비저항 ρc(x) 가 위치에 따라 변하는 경우까지 풀었다 — ① ρc 일정 (해석해 · COMSOL 2D 검증) ② ρc 선형 변화 ③ **Simmons 터널 전류를 국소 전압 V_g(x) 와 자기무모순으로 결합** (수치).  ρc 가 작을수록 전류가 접촉 **양 끝으로 쏠리고** (current crowding), 접촉 저항은 L 이 전달 길이를 넘으면 L 에 둔감해진다.  CNT–진공–CNT (SWCNT Ø 3 nm · Rsh 60 Ω/□ · 일함수 4.5 eV) 예에서 Rc 는 D 에 지수적으로 오르고 (0.5 → 0.8 nm 에서 ~3 자릿수), L 이 늘면 줄며, V₀ > 0.3 V 에서는 터널 비선형으로 급감한다 — 1D (위치 무관) 터널 모형은 얇은 간극 · 큰 전압에서 틀린다.  CNT–금속 (Ca · Al · Cu · Au) 접촉도 같은 틀로 계산했다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | Sneha Banerjee¹ · John Luginsland¹˒² · **Peng Zhang**¹ (교신) |
| 소속 | ¹ Dept. Electrical and Computer Engineering, Michigan State University · ² (현) Confluent Sciences, LLC |
| 서지 | *Scientific Reports* **9**, 14484 (2019) · DOI `10.1038/s41598-019-50934-2` · Open Access CC BY 4.0 |
| 일자 | 접수 2019-03-14 · 승인 2019-09-23 · PDF 머리 게재일 "xx xx xxxx" (출판 전 판) |
| 자금 | AFOSR YIP FA9550-18-1-0061 · 이해상충 없음 |
| 연구유형 | **이론 + 수치** (TLM 해석해 · 사격법 (shooting) 수치해 · COMSOL 2D FEM 검증) · 실험 없음 · DEM/MPM 없음 |
| 기여 | Zhang · Luginsland 착상 · Zhang · Banerjee 정식화 · Banerjee 계산 |
| 같은 묶음 카드 | `hamasaki2022_single_parallel_contact_mwcnt_conductivity` (같은 기하의 실측) · `li2007_tunneling_resistance_cnt_composites` (이 논문 ref 24 · 교차 접합 터널) · `fuhrer2000_crossed_nanotube_junctions` (ref 26 은 같은 그룹의 Physica E 판) |

## 3. 핵심 수치 ★

### 3-1. 정식화 (stated · Eq. 1–4)
- 계면 PQNM 의 미소 구간 Δx 에 Kirchhoff: `I₁(x) − I₁(x+Δx) = (V₁ − V₂)·Δx·w/ρc(x)` · `V₁(x) − V₁(x+Δx) = I₁·Rsh1·Δx/w` (도체 2 도 같은 꼴) → `∂I₁/∂x = −wJc` · `∂V₁/∂x = −I₁Rsh1/w` · `Jc = V_g/ρc` · `V_g = V₁ − V₂` · `I₁ + I₂ = I_tot` 일정.
- 경계: V₁(0) = V₀ · I₂(0) = 0 · I₁(L) = 0 · V₂(L) = 0 → **접촉 저항 Rc = (V₁(0) − V₂(L))/I_tot = V₀/I_tot** (Eq. 4) = 도체 1 의 왼쪽 끝 → 도체 2 의 오른쪽 끝 (겹침 구간 안의 도체 저항 포함).
- 정규화: x̄ = x/L · ρ̄c = ρc/ρc0 · R̄sh2 = Rsh2/Rsh1 · I₀ = wV₀/(Rsh1L) · ρc0 = V₀wL/I₀ · Rc0 = Rsh1L/w.
- w = "effective transverse dimension" (나노선이면 지름 — 이 논문의 CNT 예는 w = 3 nm).

### 3-2. 해석해 — ρc 일정 (stated · Eq. 7–9)
- **Eq. (8)** `R̄c = [(1 + R̄sh2²)·cosh q + R̄sh2·(2 + q·sinh q)] / [(1 + R̄sh2)·q·sinh q]`, `q = L/λ₀ = √((1 + R̄sh2)/ρ̄c)`.
- **Eq. (9)** (R̄sh2 → 0) `R̄c = coth q / q` — 금속–반도체 접촉의 고전식과 같다 (refs 10, 42).
- 같은 두 도체 (R̄sh2 = 1): Jc · V_g 가 접촉 가운데에 대해 대칭 · 최소는 x̄ = 0.5 · 최대는 양 끝 (Fig. 2(a)(d)) · **ρc 가 작을수록 끝으로 더 쏠린다**.
- 다른 두 도체: R̄sh2 < 1 이면 최대가 x̄ = 0, > 1 이면 x̄ = 1 (Fig. 3).
- Rc 는 ρc 와 R̄sh2 둘 다에 따라 오르지만 **ρc 에 더 강하게** 의존 (Fig. 4).
- COMSOL 2D 검증 (Fig. 4 의 ×): 도체 길이 20 nm · 높이 10 nm · 계면층 0.5 nm · 도체 저항률 10⁻⁹–10⁻⁷ Ω m · 계면층 저항률 10⁻⁹–10⁻⁵ Ω m · 수렴 오차 < 10⁻⁹ — "excellent agreement".

### 3-3. 선형 ρc 와 터널 (stated)
- **선형** ρ̄c(x̄) = 1 + A·x̄ (A = −0.9 … 1): A ↑ → Rc ↑ · 최대 V_g 는 ρc 가 큰 끝 · 최대 Jc 는 ρc 가 작은 끝 · R̄sh2 가 클수록 A 의존이 강하다 (Fig. 5 · Fig. 6).
- **터널** (Case 3): 계면 절연막 두께 균일 · 전하 포획 무시 · Simmons 식 (Eq. 10, 같은 · 다른 재료 · 순 · 역 바이어스 · 영상력 λ = 2.49/(εr·D[Å]·eV₀[eV]) 꼴) → ρc(x) = V_g(x)/Jc(x) 를 TLM 에 넣어 자기무모순.  옴 극한 (V_g → 0) 은 Eq. (11).
- **CNT–진공–CNT 입력**: SWCNT 선저항 **ρ_L = 20 kΩ/µm** (refs 53, 54) · 지름 = w = **3 nm** → **Rsh1 = Rsh2 = ρ_L·w = 60 Ω/□** · 일함수 **W₁ = W₂ = 4.5 eV** (ref 55) · 진공 (**εr = 1.0 · χ = 0**).
- Fig. 7: L 30 · 50 · 70 · 90 nm (V₀ 1 V · D 0.5 nm) · D 0.5 · 0.55 · 0.60 · 0.65 nm (V₀ 1 V · L 50 nm) · V₀ 1 · 2 · 3 · 4 V (D 0.55 nm · L 50 nm).
- **Rc 범위 (Fig. 8) = 5 kΩ – 10 MΩ** · D 가 커지면 매우 빨리 증가 · L 이 커지면 감소 · **V₀ < 0.3 V 에서는 V₀ 에 거의 무관** · V₀ > 0.3 V 에서 급감 (터널 비선형).
- 결론 문장: 옴 근사 (Eq. 11) 는 *"in general … not reliable"* · 1D 모형 (V_g = V₀ 로 놓은 Eq. 10) 은 D 나 εr 가 크고 V₀ 가 작을 때만 좋다.
- **CNT–절연막–금속**: 일함수 Ca 2.9 · Al 4.08 · Cu 4.7 · Au 5.1 eV · 저항률 Ca 3.36 · Al 2.7 · Cu 1.68 · Au 2.2 × 10⁻⁸ Ω m · 금속 단면 3 nm × 3 nm · Fig. 9(c)(d) εr 1 → 3.9 (V₀ 3 V) · Fig. 10(d) 도체 2 저항률 2.0 × 10⁻⁸ Ω m — Rc 는 D · εr · W₂ 와 함께 오르고 L 과 함께 준다.

### 3-4. Fig. 8 판독과 λ₀ 역산 — derived(ours)
Fig. 8(a) (V₀ = 1 V · 실선 = 자기무모순) 판독 (로그 축 · 판독 ±15–20 %) 에 §0 의 식 Rc = ρ_L·[L/2 + λ₀·coth(L/2λ₀)] (ρ_L = 20 Ω/nm) 을 로그 최소제곱으로 맞췄다 (L = 10 · 20 · 50 · 100 nm 네 점).

| D (nm) | Rc(L = 10) ≈ | Rc(100) ≈ | **λ₀ (적합)** | 비 Rc(10)/Rc(100) 관측 · 적합 | ρc = λ₀²·(Rsh1 + Rsh2) |
|---|---|---|---|---|---|
| 0.50 | 4.0 × 10⁴ Ω | 6.0 × 10³ Ω | **≈ 0.10 µm** | 6.7 · 7.6 | ≈ 1.3 × 10⁻¹² Ω m² |
| 0.55 | 1.0 × 10⁵ | 1.15 × 10⁴ | **≈ 0.16 µm** | 8.7 · 8.8 | ≈ 3.0 × 10⁻¹² |
| 0.60 | 2.5 × 10⁵ | 2.7 × 10⁴ | **≈ 0.25 µm** | 9.3 · 9.5 | ≈ 7.5 × 10⁻¹² |
| 0.65 | 6.5 × 10⁵ | 6.8 × 10⁴ | **≈ 0.40 µm** | 9.6 · 9.8 | ≈ 1.9 × 10⁻¹¹ |

- 순수 1/L 이면 비 = 10 — **간극이 얇을수록 (ρc 작을수록) λ₀ 가 짧아 100 nm 안에서 이미 포화가 보인다** (D 0.50 nm 비 6.7).
- ⚠ V₀ 1 V 는 Fig. 8(c)(d) 에서 옴 평탄 (≲ 0.3 V) 의 끝을 조금 넘는다 → λ₀ 는 **유효값** (전압 의존 ρc 를 상수로 본 근사).

## 4. 방법 ★
- **TLM (Fig. 1(d))**: 두 도체 = 직렬 저항 사다리 (Rsh1 · Rsh2) · 계면 = 병렬 저항 ρc(x)/(wΔx) · 2D (두께 방향 · 폭 방향 변화 없음 — 폭 효과는 유효 Rsh 에 넣는다).
- **수치법**: α (정규화 총전류) 를 추정 → Eq. (5b) 를 사격법으로 → Eq. (5a) → V̄₁(1) = V̄g(1) 될 때까지 α 반복 → Eq. (5c) 로 Ī₁ · Ī₂.
- **검증**: ρc 일정 해석해 ↔ COMSOL 2D (Fig. 4 의 ×).
- **한계 (저자)**: 공간전하 · 교환상관 무시 · 전하 포획 무시 · 2D (가로 방향 무시) · TLM 은 모서리 근처 전류 쏠림 · 가장자리 장을 다 담지 못한다 (장 해법 필요 — refs 10, 49, 50, 58) · 계면층 안의 평행 전류 성분 무시.
- ★ **접합 처리**: 나란한 겹침 하나 · 계면층 두께 균일 · 접촉력 · 변형 없음 · 도체 = 균일 시트저항 (CNT 의 다벽 · 반경 방향 구조 없음).

## 5. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| **1** | (a) 나노선 1 · 2 의 부분 겹침 (b) 박막판 (c) 옆모습 (L · D · εr) (d) **TLM — Rsh1 · Rsh2 사다리 + 계면 ρc(x) 다리** | ★ 우리 분산판 v0 (접합 간선 k 개 = ρc 다리 · 섬유 복셀 = Rsh 사다리) 의 **그림판 정의** |
| 2 | 같은 두 도체 · ρ̄c 0.01–100 · V̄g · V̄₁ · V̄₂ · J̄c · Ī₁ · Ī₂ 분포 — ρ̄c 가 작을수록 J̄c 가 양 끝에 몰린다 (ρ̄c = 0.01 에서 끝값 ≈ 12 · 가운데 ≈ 0.5, figure-read ≈) | ★ **전류 쏠림 = 실효 컨덕턴스 포화의 기전** — 접합 간선 전류를 분산판에서 위치별로 보면 같은 U 자가 나와야 한다 (시험 아이디어) |
| 3 | 다른 두 도체 (R̄sh2 0.01–100) · ρ̄c = 1 — 쏠림이 저항 작은 쪽 끝으로 | 두 섬유 r′ 가 다를 때 (우리 = 단분산 Ø0.15 → 해당 없음) |
| **4** | R̄c vs ρ̄c (a) · vs R̄sh2 (b) — 해석해 (선) + COMSOL (×) · 점선 = Eq. (9) | ★ **(a) 의 해석 기준** — 같은 R̄sh2 에서 ρ̄c ↓ 이면 R̄c 가 ρ̄c^½ 기울기로 (포화 영역) 바뀐다 (로그 축 판독) · 우리 이산 TLM 시험의 기대값 |
| 5 | 선형 ρ̄c = 1 + Ax̄ (A −0.5 … 0.5) · 같은 두 도체의 분포 | 접합 따라 계면이 고르지 않을 때 (예: PTFE 가 접촉 일부만 덮음) 전류가 어디로 가나 — 우리 '간선마다 PTFE 덮임' 규칙의 문헌 그림 · ⚠ 재크롭 (자동 = Fig. 6 영역) |
| 6 | R̄c vs A (R̄sh2 0.1 · 1 · 10 · 100) | 같은 · ⚠ 재크롭 (오른쪽 빈 칸) |
| 7 | CNT–진공–CNT 터널: V_g(x) · J_c(x) — L 30–90 nm · D 0.5–0.65 nm · V₀ 1–4 V · 실선 = 자기무모순 · 파선 = V_g = V₀ 상수 ρc · 점선 = 옴 극한 | J_c ~10⁷–10⁸ A/cm² 자릿수 (figure-read) · 1D 근사가 언제 틀리나 |
| **8** | **Rc vs L (a) · vs D (b) · vs V₀ (c)(d)** — CNT–진공–CNT | ★ **(b)(c) 의 근거 그림** — Rc 5 kΩ–10 MΩ · D 에 지수 · L 에 포화 · V₀ < 0.3 V 옴 · §3-4 λ₀ 역산의 원자료 |
| 9 | CNT–절연막–금속 (Ca · Al · Cu · Au) V_g · J_c · εr 1–3.9 | 비대칭 접촉 — 우리 탄소–집전체 · 탄소–SDCP 쪽 (v0 밖) |
| 10 | CNT–절연막–금속 Rc vs L · D · εr · W₂ | 같은 |

## 6. Post-processing ★
- 정규화 변수로 전 분포를 그리고, Rc 를 해석해 · 수치해 · 1D 근사 · 옴 근사로 나란히 비교 (Fig. 7 · Fig. 8 의 실선 · 파선 · 점선).
- 도구: 사격법 수치해 (구현 언어 미기재) · COMSOL Multiphysics (FEM).  불확도 · 민감도 표 없음.

## 7. 우리 DEM+MPM 대비 ★★

> 대상 = Rint ② STEP3 복셀 전자 채널의 VGCF–VGCF 접합 v0 (`scripts/carbon_junction.py` · `scripts/ca_ext_cjunc.py` · 설계 v1 §4 · 등록 R §2-1 · 작업 브랜치 HEAD `57f1b2baf`).  frame[5]: MPM 침대 위 수송.

### 7-1. 대응표

| TLM (이 논문) | 우리 분산판 v0 | 메모 |
|---|---|---|
| 계면 다리 ρc/(wΔx) | 간선 하나 = R_j,0·k/m (m = max(1, L_c/L_par) · k = ⌈L_c/L_par⌉) | 길이당 컨덕턴스 g = w/ρc ↔ **1/(R_j,0·L_par)** (L_c > L_par 일 때) |
| 도체 사다리 Rsh/w | 섬유 복셀 사슬 (σ 7,854 S/cm · vox 0.15 µm → **r′ = 56.588 Ω/µm**) | 설계 §1-2 #2 (직경 보존 · Endo 단섬유) |
| Δx → 0 연속 | 간선 간격 L_c/k ∈ (L_par/2, L_par] · 포트 = 기하 정준 셀 (`carbon_junction.py:53` 이하) | 이산화 오차 = k 정수 경계의 σ 계단 (등록 R 한정어 ⑫) |
| λ₀ = √(ρc/(Rsh1 + Rsh2)) | **λ_model = √(R_j,0·L_par/(r′_i + r′_j))** | 같은 식 · 우리 쪽은 보정된 R_j,0 가 정한다 |
| Rc 정의 = 끝 → 끝 (겹친 도체 포함) | 단자 σ_e 하나 (전극 전체) | 접합만의 Rc 는 우리 기록에 없다 → 진단으로 만들 수 있다 (§9 (가)) |
| 터널 ρc(V_g) (비선형) | R_j,0 일정 (옴) | DC 분극의 접합당 전압은 mV 대 (추정) → 이 논문 기준 옴 영역 (< 0.3 V) |

### 7-2. 수치로 옮기기 (derived(ours))
- **모형 쪽**: λ_model (r′_i = r′_j = 56.588 Ω/µm · L_par 0.30 µm) = 0.515 (R_j,0 10² Ω) · 1.628 (10³) · 5.149 (10⁴) · 16.28 (10⁵) · 51.49 µm (10⁶).
- **문헌 쪽**: 이 논문 CNT 예의 ρc (≈ 1.3 × 10⁻¹² – 1.9 × 10⁻¹¹ Ω m², §3-4) 를 VGCF 에 두면 λ = √(ρc/(2w·r′)):
  - w = 지름 150 nm (이 논문의 규약: w = 지름) → **λ ≈ 0.27–1.07 µm**
  - w = 간극 창 호 길이 10.1 nm (Hamasaki SI 의 기하 · `hamasaki2022_…` §3-5) → **λ ≈ 1.05–4.1 µm**
- 두 카드를 합친 VGCF 환산 λ 밴드 ≈ **0.3–4 µm** (가정 다수 · 측정 아님).  우리 L_par (0.30 µm) 는 그 **아래 끝**이다 — L_par 는 접합 instance 의 단위 길이이고 간선 간격이므로, λ 보다 짧다는 것은 **전송선이 분해된다**는 뜻이다 (포화 재현에 유리).
- 실침대에서 포화가 판정에 영향을 주는지는 **L_c 분포 ↔ λ_model** 비교로만 답이 난다 (S0 census · 보정 뒤).

### 7-3. 터널 · 전압
- 이 논문의 Rc 는 V₀ < 0.3 V 에서 상수 (Fig. 8(c)(d)) — 우리 전극 DC 분극 (실측 앵커 SBE 1.63 · DBE 4.68 mS/cm) 에서 섬유 접합 하나에 걸리는 전압은 mV 이하일 것 (전극 두께 수십 µm · 인가 전압 · 접합 수 — **측정 조건 미확인** (CLAUDE.md 10-12 · 10-16 앵커 줄)) ⇒ **옴 R_j,0 가정은 이 논문 기준으로 안전한 쪽** (추정).

### 7-4. frame 메모
- 이 논문은 **접합 한 개 (나란한 겹침) 의 수송 이론**만 소유한다 — 망 · 교차 접합 · 압밀 · 접촉력 · 실측 없음.  ⇒ R_j,0 의 값과 비교할 대상이 아니라 **분산판 v0 의 구조 (이산 TLM) 를 검증할 해석해**다 (frame[4]: 해석해 대조 = 독립 검사).

## 8. 적용 인사이트
- ① **분산판 v0 = 이산 TLM** 이라는 사실을 문장으로 고정하자 — *"긴 접촉 · 포화 없는 선형 법칙"* 이 Codex · 심사자 눈에 비물리로 보이는 것을 막는다: 포화는 법칙이 아니라 **풀이가 만든다** (Fig. 2(d) 의 끝 쏠림이 우리 간선 전류에도 나와야 한다).
- ② **Eq. (8) 은 우리 시험의 해석 기준**이다 — 두 평행 복셀 섬유 + 분산판 간선의 단자 저항을 Eq. (8) (R̄sh2 = 1) 과 대조하면 이산화 오차 (Δ/λ)² 와 포화 재현을 한 번에 확인한다.  "보장마다 작은 해석 반례" (CLAUDE.md) 의 정석 꼴.
- ③ 간극 (D) 0.05 nm 마다 Rc ≈ ×2–2.7 (Fig. 8(a)(b) figure-read · L 20 nm 에서 D 0.5 → 0.8 nm 가 ≈ 2 × 10⁴ → ≈ 7 × 10⁶ Ω) — **우리 검출 허용 (tol_ff ≤ 75 nm) 이 가를 수 없는 간극이 접합 저항을 자릿수로 바꾼다** → R_j,0 는 간극 분포의 묶음 (`li2007_…` 카드와 같은 결론).

## 9. 적용 후보 (11-03)

### (가) 지금 v0 안에서 — 값 채택 없음
1. **해석 시험 (물리 변경 없음 · 게이트 대상)** — `scripts/test_carbon_junction.py` 에 "두 평행 섬유 + 분산판 간선 ↔ Eq. (8) (R̄sh2 = 1)" 대조: ① λ_model ≫ 간선 간격 → 단자 저항이 Eq. (8) 과 O((Δ/λ)²) 안 일치 ② L_c ≫ λ_model → 접합 몫이 rλ 로 포화 ③ 간선별 전류가 양 끝으로 쏠림 (Fig. 2(d)).  대가 = 시험 추가 (게이트 · Codex 회차에 포함) · 값 · 법칙 불변.
2. **한정어 (문서)** — 등록 R §7-1 ⑫ (`docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md:278`) 에: *"분산판 v0 는 이산 전송선이다 — 접합 간선 (길이당 컨덕턴스 1/(R_j,0·L_par)) 과 섬유 축저항 (r′ 56.588 Ω/µm) 이 전달 길이 λ_model = √(R_j,0·L_par/(r′_i + r′_j)) 를 정하고, L_c ≫ λ_model 인 접촉의 실효 컨덕턴스는 풀이 안에서 포화한다 (Banerjee 2019 Eq. 8–9)."*  코드 상수 `CJUNC_QUALIFIERS` 에 넣는 것은 게이트를 거치는 코드 변경 (`scripts/ca_ext_cjunc.py:466` 이 대조) — 문서 먼저.
3. **진단 (보고 전용)** — 보정된 R_j,0 로 λ_model 을 내고 S0 L_c 분포 (`scripts/ca_s0_census.py:776–786`) 와 비교 — L_c > λ_model · > 2λ_model 인 instance 수 · 그 접합 전류 몫 (분산판 간선 전류는 이미 `res['_cjunc']` dof 원장에 있다 · `carbon_junction.py` 머리말 "solve_sigma_z(…, cjunc=plan) → res['_cjunc']").  ⚠ DBE 는 등록 R §2-1 개정 커밋 뒤.
4. **장부** — "옴 R_j 가정 = 접합당 전압 < 0.3 V 에서 Banerjee 기준 안전 (추정 · DC 분극 측정 조건 미확인)" 한 줄 (설계 §4-5 한계 목록).

### (나) 1저자 비준 필요
1. **전압 의존 (터널) R_j** — Simmons 결합 · 비선형 풀이 · 새 손잡이 (간극 · 일함수 · εr) · VGCF–VGCF 계면 값 없음.  **권고: 하지 않는다** (DC 분극의 접합 전압이 옴 영역일 것이므로 이득 없음 · 단 측정 조건을 확인하면 장부에서 닫는다).
2. **명시적 포화 법칙** (lumped G_j = (2λ/L_par)·tanh(L_c/2λ)/R_j,0) — 분산판 v0 와 **이중 계상** · Codex RCA-05 결정 (분산판 v0) 과 충돌 · λ 새 손잡이.  **권고: 하지 않는다.**
3. **위치별 계면 불균일 (Case 2 꼴)** — 예: PTFE 가 접촉의 일부만 덮을 때 간선별 ρc 를 연속으로 (지금 = 간선마다 P0/P1 이진) — 새 법칙 · PTFE 두께 정보 필요.  **권고: v1 후보로 장부만.**

## 10. 인용 가능 문장
- (EN) *"For a partially overlapped parallel contact with uniform specific contact resistivity ρc, the transmission-line solution gives a transfer length λ₀ = √(ρc/(Rsh1 + Rsh2)); for overlaps much shorter than λ₀ the contact conductance grows linearly with the overlap, whereas for much longer overlaps the junction contribution saturates because current crowds at the contact edges (Banerjee, Luginsland & Zhang, Sci. Rep. 9, 14484, 2019)."*
- (EN, 크기) *"Self-consistent Simmons-tunnelling TLM calculations for SWCNT–vacuum–SWCNT parallel contacts (L = 10–100 nm, gap 0.5–0.8 nm) give contact resistances of 5 kΩ–10 MΩ, nearly independent of bias below 0.3 V."*
- (KR) *"Banerjee 등 (2019) 의 전송선 모형에서 나란한 접촉의 컨덕턴스는 겹침이 전달 길이보다 짧을 때만 길이에 비례하고, 길어지면 전류가 접촉 끝으로 쏠려 포화한다."*

## 11. 주의 / 한계 (over-claim 방지)
1. **이론 · 계산뿐** — 측정 대조는 *"agrees with previously reported experimental and theoretical works"* 한 문장 (refs 24, 26, 29) 이 전부.
2. **λ₀ 숫자는 논문에 없다** — §3-4 의 0.10–0.40 µm 는 우리가 Fig. 8(a) 판독에 Eq. (8) 을 맞춘 값 (유효값 · V₀ 1 V).
3. **w (가로 치수) 규약** — 나노선 지름을 w 로 둔다.  원통 접촉의 실제 접촉 폭 (Hamasaki 의 C = 3.2 nm @ Ø 15 nm) 과 다르다 → VGCF 환산 λ 가 w 선택에 따라 4 배 움직인다 (§7-2).
4. **도체 = 균일 시트** — 다벽 · 반경 방향 (c 축) 저항 · 껍질만 흐르는 전류가 없다.
5. **Simmons 공식의 적용 범위** — 저자 스스로 *"reliable only when the barrier height is relatively high and the gap voltage is low"* · 공간전하 · 교환상관 · 포획 무시.
6. **진공 간극 · 접촉력 없음** — 압밀 전극의 섬유 접합 (SE · PTFE 막 · 변형) 과 다르다.
7. SWCNT ρ_L 20 kΩ/µm 은 문헌 인용값 (refs 53, 54) — 이 논문의 측정 아님.

## 12. 용어 미니-글로서리
- **TLM (transmission line model)**: 두 도체의 길이 방향 저항을 사다리로, 계면을 병렬 다리로 둔 집중정수 회로 — 나란한 접촉의 표준 모형.
- **비접촉 비저항 ρc (specific contact resistivity)**: 계면 단위 면적당 저항 [Ω m²].
- **시트저항 Rsh**: 두께를 묶은 2D 저항 [Ω/□] — 나노선은 Rsh = ρ_L·w.
- **전달 길이 λ₀**: √(ρc/(Rsh1 + Rsh2)) — 전류가 한 도체에서 다른 도체로 넘어가는 특성 길이.
- **전류 쏠림 (current crowding)**: 계면 저항이 작을수록 전류가 접촉 끝에 몰리는 것.
- **Simmons 공식**: 얇은 절연막을 사이에 둔 두 전극의 터널 전류 밀도 (1963) — 영상력 · 장벽 높이 · 두께 · 전압의 함수.
- **자기무모순 (self-consistent)**: 국소 전압 → 터널 ρc → TLM 분포 → 국소 전압을 맞물려 푼다.
- **λ_model**: 우리 분산판 v0 의 내부 전달 길이 √(R_j,0·L_par/(r′_i + r′_j)).

## 13. 이 카드가 확인하지 못한 것 (n/a)
- 수치 코드 (언어 · 공개 여부) · Fig. 4 의 COMSOL 점 개수 · 판 PDF 의 최종 게재일 (머리 "xx xx xxxx") · Eq. (10) 의 상수 전부 (텍스트 층이 깨져 렌더 쪽에서 꼴만 확인 — 수치 대입은 하지 않았다) · VGCF 나 흑연 섬유에 대한 어떤 계산도 이 논문에 없다.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
