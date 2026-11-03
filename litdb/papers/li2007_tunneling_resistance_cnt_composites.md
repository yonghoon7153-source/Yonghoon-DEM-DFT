# Dominant role of tunneling resistance in the electrical conductivity of carbon nanotube–based composites — Li (APL 2007) · 교차 CNT 사이 절연막의 Simmons 터널 저항 + 몬테카를로 퍼콜레이션 망 — 막 1.0 nm ≈ 100 GΩ · 1.8 nm 에서 접촉 저항 10¹⁹ Ω (망이 절연체가 되는 "최대 터널 거리") · 접촉 저항이 망 σ 를 지배

> slug `li2007_tunneling_resistance_cnt_composites` · DOI `10.1063/1.2819690` · type `simulation (Monte-Carlo percolation network of straight CNTs + Simmons tunneling contact resistance through a polymer/ceramic film)` · PDF `4._Dominant_role_of_tunneling_resistance_in_the_electrical_conductivity_of_carbon_nanotube_based_composites.pdf` · digested `2026-11-03` · status ✅
> *Appl. Phys. Lett.* Letter 3 쪽 (+ AIP 표지 1 쪽) · SI 없음 · evidence `fulltext` · 그림 `4/4 육안 확인` (자동 크롭 4 장 모두 온전 · 캡션의 APL 괄호 글리프 (제어문자) 를 괄호로 복원 — `figures.json` `caption_note`) · 약칭 `[Li07]`
> **계기** — Rint ② 접합 검출 허용 (tol_ff = min(u, r_f) · 중심선 기하 근접) 이 **물리 터널 간극이 아니다**는 한정어의 근거 · 단일 R_j,0 가 망 σ 를 어떻게 지배하는가 (1저자 11-03 · 다섯 편 묶음).  ⛔ v0 동결 — 값 채택 없음.
> 수치 등급: **stated** · **figure-read ≈** · **derived(ours)**.

---

## 0. ★ 이 카드가 답하는 것

| 질문 | 이 논문의 답 | 등급 · 자리 |
|---|---|---|
| **(c) 어떤 간극 · 차단 거리 · 장벽 · 식** | **Simmons (1963) 직사각형 장벽 일반식** (Eq. 3–5) · 장벽 높이 φ₀ ≈ CNT 일함수 **5.0 eV** (ref 22) · 막 유전율 **K = 3.98 (에폭시) · 4.5 (알루미나)** · 막 전압 U = e/C = e·t/(A_C·K·ε₀) (Eq. 6) · 터널 비저항 ρ_tunnel = U/J [Ω cm²] · **R_tunnel = ρ_tunnel/A_C** (Eq. 7) · 접촉 면적 **A_C = d²** (직교 교차) | stated · p. 223114-2 |
| (c) 차단 거리 | 막 **1.0 nm 에서 터널 저항 ~100 GΩ** · 망이 절연체 (σ < 10⁻¹² S/m) 가 되는 접촉 저항 **> 10¹⁹ Ω** ↔ 막 **1.8 nm** = *"maximum tunneling distance"* · *"consistent with predictions that the tunneling distance is typically on the order of tens of angstroms"* | stated · p. 223114-2 · Fig. 2 · Fig. 3 |
| (c) 민감도 | 1.0 nm (10¹¹ Ω) → 1.8 nm (10¹⁹ Ω) = **막 0.1 nm 당 ≈ 10 배** · 지름 2–10 nm 는 *"moderate"* (클수록 낮다) · 에폭시 ↔ 알루미나 차이 작다 | 0.1 nm 당 = derived(ours) (stated 두 점의 산술) · 나머지 stated |
| (c) 우리 검출 허용과 비교 | 우리 instance = 중심선 거리 ≤ r_fi + r_fj + tol_ff · **tol_ff = min(u, r_f) ≤ 0.075 µm = 75 nm** (등록 R §2-1) — **차단 거리 1.8 nm 의 ≈ 40 배** · 우리 '접합' 은 MPM 경로 위치 불확도 안의 **기하 근접**이지 터널 간극이 아니다 | derived(ours) · `scripts/ca_ext_cjunc.py:36–49` · 등록 R §2-1 |
| **(b) 크기** | 직접 접촉 (막 없음) 접합 저항으로 **R_direct contact = 4 × 10⁵ Ω** 를 썼다 (Fig. 4 라벨) · 인용: Fuhrer 2000 교차 SWCNT *"100–400 kΩ"* (M/M · S/S) · M/S 두 자릿수 높음 · Buldum & Lu 2001 계산 100 kΩ–3.4 MΩ · Foygel 2005 의 복합체 적합 ~10¹³ Ω | Fig. 4 = stated (그림 라벨) · 인용 = stated (2차 인용 — 원값은 `fuhrer2000_…` 카드) |
| **(d) 망 수준** | p = 0.15 vol% 에서 **σ ∝ 1/R_C** (R_C 10⁷ → 10²⁰ Ω · CNT 고유 σ 10⁴ · 10⁶ S/m 두 곡선이 겹친다 = 튜브 무관) · 막 없는 망은 100 % 외삽 **7.2 × 10⁵ S/m ≈ σ_NT 10⁶ S/m** = 튜브 지배 (CNT 매트) · 막 있는 망은 접촉 지배 (복합체) · 임계 지수 **1.78–2.14** 가 **접촉 저항 수준에 따라 변한다** | stated · Fig. 3 · Fig. 4 · p. 223114-3 · σ ∝ 1/R_C 기울기 = figure-read |
| (a) 길이 법칙 | 해당 없음 — 모든 접합 = 직교 교차 면적 d² · *"assumes the same CRs at all contact points"* | stated |

**한 줄 판정** — 이 논문은 우리 v0 와 **같은 가정 (모든 접점에 같은 접촉 저항)** 으로 망을 풀고, 그 가정 아래 망 σ 가 접촉 저항 하나에 **반비례**함을 보인다 → 단일 R_j,0 보정이 성립하는 영역의 근거다.  동시에 그 접촉 저항이 **막 0.1 nm 에 10 배씩** 움직인다는 것을 보여, 우리 기하 검출 (허용 ~75 nm) 이 그 물리를 가를 수 없음을 수치로 못 박는다.

## 1. 한 줄 요약

델라웨어대 Li · Thostenson · Chou 는 고분자 · 세라믹 기지 안에 무작위로 놓인 곧은 CNT 의 2 층 의사-3D 망 (20 × 20 µm², 지름 2 nm · 길이 2 µm, 종횡비 1000) 을 몬테카를로로 만들고, 교차점마다 접촉 저항 R_C = R_direct contact + R_tunnel 을 두었다.  R_tunnel 은 직교 교차 면적 d² 위 균일 절연막 (두께 t) 의 Simmons 직사각형 장벽 터널 전류로 계산했다 (일함수 5.0 eV · 에폭시 K 3.98 · 알루미나 4.5).  터널 저항은 막 두께에 지수적으로 올라 1.0 nm 에서 ~100 GΩ, 1.8 nm 에서 망을 절연체 (σ < 10⁻¹² S/m) 로 만드는 10¹⁹ Ω 에 이르므로, 이것을 CNT 복합체의 **최대 터널 거리 ≈ 1.8 nm** 로 제안한다.  같은 접촉 저항을 모든 접점에 준 망 σ 는 접촉 저항에 반비례하고 CNT 고유 전도도에는 무관하며 (p = 0.15 vol%), 막이 없는 망 (CNT 매트) 은 튜브 저항이, 막이 있는 망 (복합체) 은 접촉 저항이 지배한다 — 문헌의 복합체 σ 가 10⁻⁵–10² S/m 로 크게 흩어지는 것도 접촉 저항 차이로 설명한다.  임계 지수는 1.78–2.14 로 접촉 저항 수준에 따라 변한다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Chunyu Li** (교신) · Erik T. Thostenson · Tsu-Wei Chou |
| 소속 | Dept. Mechanical Engineering + Center of Composite Materials, University of Delaware |
| 서지 | *Applied Physics Letters* **91**, 223114 (2007) · DOI `10.1063/1.2819690` |
| 일자 | 접수 2007-08-01 · 승인 2007-11-09 · 온라인 2007-11-29 |
| 자금 | US NSF NIRT (0304506) · AFOSR (FA9550-06-1-0489) · ONR (N00014-07-1-0345) |
| 연구유형 | **시뮬레이션** (몬테카를로 망 · Kirchhoff 류 저항망 풀이 · Simmons 터널) — 실험 없음 · 문헌 실험값과의 정성 비교 |
| 같은 묶음 카드 | `fuhrer2000_crossed_nanotube_junctions` (ref 13 — R_direct contact 의 근거) · `banerjee2019_tunneling_tlm_parallel_nanoscale_contacts` (같은 Simmons 식을 나란한 접촉에 · Li 를 ref 24 로 인용) · `nirmalraj2009_…` (실측 망 σ ∝ 1/⟨R_J⟩) |

## 3. 핵심 수치 ★

### 3-1. 모형 입력 (stated)

| 항목 | 값 | 자리 |
|---|---|---|
| 망 | 2D 정사각 영역 **20 × 20 µm²** · CNT 두 층 (의사-3D) · 층 두께 = 2d + 최대 층간 간격 · CNT = 곧은 원통 · 교차점은 겹침 (관통 없음) | p. 223114-1–2 · Fig. 1 |
| CNT | **지름 2 nm · 길이 2 µm · 종횡비 1000** · 고유 σ_NT **10⁶ S/m** (Fig. 3 은 10⁴ 도) | p. 223114-2 · Fig. 3 · Fig. 4 |
| CNT 조각 저항 | **R_NT = 4L_m/(σ_NT·π·d²)** (Eq. 1) · L_m = 접점 사이 조각 길이 | Eq. (1) |
| 접촉 저항 | **R_C = R_direct contact + R_tunnel** (Eq. 2) · 모든 접점 같은 값 | Eq. (2) · p. 223114-2 |
| 접촉 면적 | **A_C = d²** (직교 교차 근사 — 교차 각 무시) | p. 223114-2 · Fig. 1(d) |
| 터널 | Simmons 직사각형 장벽: J = 6.2 × 10¹⁰ (Δt)⁻² [φ·exp(−1.025Δt·φ^½) − (φ + U)·exp(−1.025Δt·(φ + U)^½)] (Eq. 3) · φ = φ₀ − (U/2t)(t₁ + t₂) − (5.75/(KΔt))·ln[t₂(t − t₁)/(t₁(t − t₂))] (Eq. 4) · t₁ = 6/(Kφ₀) · t₂ = t[1 − 46/(3φ₀Kt + 20 − 2UKt)] + 6/(Kφ₀) (Eq. 5) · t 는 Å · Δt = t₂ − t₁ | Eq. (3)–(5) |
| 막 전압 | U = e/C = e·t/(A_C·K·ε₀) (Eq. 6) — 접합을 축전기로 보고 전자 하나의 전압 | Eq. (6) |
| 터널 저항 | ρ_tunnel = U/J [Ω cm² — 부피 비저항 아님] · R_tunnel = ρ_tunnel/A_C (Eq. 7) | Eq. (7) |
| 재료 상수 | φ₀ ≈ CNT 일함수 **5.0 eV** (ref 22) · K = **3.98** (에폭시) · **4.5** (알루미나) | p. 223114-2 |
| 직접 접촉 | **R_direct contact = 4 × 10⁵ Ω** (Fig. 4 맨 위 곡선 라벨) | Fig. 4 |

### 3-2. 결과

| 양 | 값 | 등급 · 자리 |
|---|---|---|
| 막 1.0 nm 의 터널 저항 | **~100 GΩ** ("in the order of 100 GΩ") — 막 없는 CR 보다 수 자릿수 큼 | stated · p. 223114-2 |
| 망이 절연 (σ < 10⁻¹² S/m) 이 되는 CR | **> 10¹⁹ Ω** ↔ 막 **1.8 nm** | stated · Fig. 3 |
| 막 두께 민감도 | 1.0 → 1.8 nm 에서 10¹¹ → 10¹⁹ Ω = **≈ 10 배 / 0.1 nm** | derived(ours) |
| 그림 판독 | t ≳ 0.25 nm 부터 직선 (로그) · 1.8 nm 에서 ≈ 10¹⁸–10¹⁹ Ω (지름 10 → 2 nm) · t ≲ 0.25 nm 는 톱니 (≈ 10⁰–10⁶ Ω) | figure-read ≈ · Fig. 2 |
| 지름 효과 | 2 · 5 · 8 · 10 nm — *"moderate"* · 클수록 낮다 | stated · Fig. 2 |
| 기지 효과 | 에폭시 ↔ 알루미나 *"not important"* (K 차이 작음) · 다만 터널 비저항은 K 와 함께 증가 | stated |
| σ vs R_C (p = 0.15 vol%) | R_C 10⁷ → 10²⁰ Ω 에서 σ ≈ 10⁰ → 10⁻¹³ S/m · **기울기 ≈ −1 (로그–로그)** · σ_NT 10⁴ · 10⁶ S/m 점이 **겹친다** | figure-read ≈ · Fig. 3 |
| σ vs CNT 함량 (σ_NT 10⁶) | 문턱에서 계단 (≈ 0.15 vol%) 뒤 완만 증가 · R_direct 4 × 10⁵ Ω: ≈ 10¹ → 10³ S/m · R_C 10⁸: ≈ 10⁻¹ → 10¹ · 10¹¹: ≈ 10⁻⁴ → 10⁻² · 10¹³: ≈ 10⁻⁶ → 10⁻⁴ S/m (0.15 → 3.8 vol%) | figure-read ≈ · Fig. 4 |
| 막 없는 망의 100 % 외삽 | **≈ 7.2 × 10⁵ S/m** ≈ 개별 CNT 10⁶ S/m → *"the intrinsic resistance of CNTs plays a dominant role in CNT mats"* | stated · p. 223114-3 |
| 임계 지수 γ (σ = σ₀(p − p_c)^γ) | **1.78–2.14** (2D 보편값 1.3 · 3D 2.0 · 문헌 1.2–3.1) · *"the critical exponent depends on the level of contact resistance"* | stated · p. 223114-3 |
| 문헌 맥락 (인용) | 복합체 실측 σ 10⁻⁵–10⁻² S/m (일부 0.01–480 S/m) · CNT 매트 · 버키페이퍼 10³–10⁶ S/m · 개별 CNT 10⁴–10⁷ S/m | stated (인용) |

## 4. 방법 ★
- **망 생성**: 2D 정사각에 곧은 CNT 를 무작위 배치 (ref 20 = 같은 저자 2007 APL 의 퍼콜레이션 모형) · 두 층 · 교차점 = 접점.
- **저항망**: 접점 사이 CNT 조각 = R_NT (Eq. 1) · 접점 = R_C (Eq. 2) · 퍼콜레이션 클러스터만 전도망 · 풀이 = 저항망 (방법 세부 · 실현 수 미기재 → n/a).
- **터널**: §3-1 식 · 접합을 평행판 축전기로 보고 U 를 정한 뒤 ρ_tunnel = U/J.
- **스케일링**: σ = σ₀(p − p_c)^γ 적합 → γ.
- ★ **접합 처리**: 모든 접점 = 직교 교차 · 면적 d² · **같은 막 두께 · 같은 R_C** (분포 없음) · 교차 각 · 접촉력 · 막 두께 분포 없음.

## 5. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a) 다층 나노복합체 (b) 대표층 (c) 교차 CNT 사이 기지막 두께 t (d) 지름 d 인 두 CNT 의 교차 · 접촉 면적 | (d) 의 A_C = d² = 우리 '점 접합' (L_c ≤ L_par) 의 문헌 대응 · (c) 막 = 우리 P1 (PTFE 덮인 접합 절단) 의 연속판 |
| **2** | 터널 저항 vs 막 두께 0–1.8 nm (에폭시 · 알루미나 · 지름 2–10 nm) — 0.25 nm 위 직선 (로그) · 1.8 nm 에서 10¹⁸–10¹⁹ Ω | ★ **(c) 의 근거 그림** — 0.1 nm 당 ≈ 10 배 · 우리 tol_ff (≤ 75 nm) 로는 가를 수 없는 축 |
| **3** | 망 σ vs 접촉 저항 (10⁶–10²⁰ Ω · p = 0.15 vol%) — σ_NT 10⁴ · 10⁶ S/m 두 기호가 겹침 | ★ **(d) 접합 지배 영역**: σ ∝ 1/R_C · 튜브 σ 무관 — 우리 R_j,0 보정이 한 점으로 서는 영역의 그림 |
| **4** | 망 σ vs CNT 함량 (0–3.8 vol%) · R_direct 4 × 10⁵ Ω · R_C 10⁸ · 10¹¹ · 10¹³ Ω | ★ (d) — R_C 가 곡선을 자릿수로 평행이동 · 문턱 뒤 기울기 (γ) 도 R_C 에 따라 다르다 → 조성 전이의 위험 |

## 6. Post-processing ★
- 몬테카를로 망 σ 의 평균 (실현 수 미기재) · 함량별 곡선 · 로그–로그 스케일링 적합 (γ) · 100 % 외삽.
- 불확도 · 실현 간 산포 미기재.

## 7. 우리 DEM+MPM 대비 ★★

> 대상 = Rint ② STEP3 복셀 전자 채널 VGCF–VGCF 접합 v0 (작업 브랜치 HEAD `57f1b2baf`) · frame[5]: MPM 침대 위 수송.  ⚠ 이 논문의 망 (2D 곧은 CNT · 의사-3D) 은 우리 3D 복셀 침대 (AM · SE · VGCF · PTFE · SDCP) 와 다르다 — 값 전이 금지.

### 7-1. 대응표

| 항목 | Li 2007 | 우리 v0 | 판정 |
|---|---|---|---|
| 접점 저항의 분포 | **모든 접점 같은 R_C** | **모든 VV instance 같은 R_j,0** (`CJUNC_QUALIFIERS` 넷째 줄) | **같은 가정** — 실제 분포의 폭 (막 0.1 nm 당 10 배) 은 둘 다 담지 않는다 |
| 접점 판정 | 기하 교차 (2D 겹침) + 층간 간격 ≤ 최대 막 | 중심선 거리 ≤ r_fi + r_fj + tol_ff · tol_ff = min(u, r_f) (≤ 75 nm) | 우리 허용이 Li 차단 거리 (1.8 nm) 의 ≈ 40 배 — **기하 불확도이지 터널 간극이 아니다** (등록 R 한정어 ⑩ 그대로) |
| 막 (기지) | 균일 두께 t 의 터널막 → R_tunnel 연속 | PTFE 덮인 접합: P0 (그대로) · P1 (절단) 이진 · SE · SDCP 막 없음 · SV 융합 (SDCP–VGCF 접촉 저항 0 가정 · 한정어 ⑧) | **P0/P1 = Li 연속 곡선의 두 끝** (t ≈ 0 ↔ t ≳ 1.8 nm) — 사이 (얇은 막의 부분 차단) 는 모형 밖 (한정어 ⑱ 의 *"사이 감쇠는 모형 밖"* 과 같은 말) |
| 튜브 고유 σ | 10⁴ ↔ 10⁶ S/m 무관 (접합 지배일 때) | Endo 단섬유 고정 (7,854 S/cm) · ÷10 감도 팔 (설계 §1-2 #21) | ★ **우리 감도 팔의 기대**: 접합 지배면 ÷10 이 σ_e 를 거의 안 바꾼다 (Fig. 3 과 같은 이유) |
| 망 σ ↔ 접촉 저항 | σ ∝ 1/R_C (p 0.15 vol% · R_C ≥ 10⁷ Ω) | 단자 σ_e ↔ R_j,0 (SBE 보정 · 단조) | 접합 지배 영역이면 **한 점 보정이 정확히 선다** (등록 R §3-2 의 식별성 검사가 보는 것) |
| 임계 지수 | R_C 에 따라 1.78–2.14 | (VGCF wt% 축 없음 · v0) | 조성 (VGCF wt%) 을 바꾸는 미래 런에서 R_j,0 하나가 조성 의존까지 맞춘다는 보장은 없다 |

### 7-2. 우리 침대에서 '막' 은 무엇인가 (추정 · 한정어 후보)
- 건식 황화물 양극의 VGCF 교차 사이에는 **LPSCl (전자 절연)** · **PTFE 피브릴** · DBE 의 **SDCP** 가 낄 수 있다.  Li 의 계산 (K ≈ 4 · φ₀ 5.0 eV) 은 우리 계가 아니지만 **크기의 방향**은 같다: 1–2 nm 넘는 절연막이 낀 교차는 사실상 끊긴 것이고, 0.5 nm 아래는 직접 접촉에 가깝다.
- 우리 v0 는 이 축을 PTFE 하나만 이진 (P0 · P1) 으로, SE 는 0 (탄소–SE 전자 0 · 막 개념 없음), SDCP 는 반대 방향 (c = 1 축약) 으로 다룬다.  ⇒ **SE 막이 VGCF 교차를 끊는 효과**는 R_j,0 에 묶인다 — SBE · DBE 의 SE 배치 차이가 있으면 R_j,0 전이가 흔들린다 (판정 한정어 후보).

### 7-3. 접합 지배인가 — 우리 쪽 산술 (derived(ours) · 가정 의존)
- 우리 섬유 r′ = 56.588 Ω/µm · 접점 간격 ℓ_j ~ 1 µm (가정 — S0 census 로 잴 수 있다) → 조각 저항 ~57 Ω.  R_j,0 ≫ 57 Ω 이면 Li Fig. 3 의 접합 지배 영역이다.
- 현 세대 보정의 묶음 σ_VGCF (SBE 0.347 · DBE 2.618 S/cm) 는 단섬유 직경 보존값 7,853.98 S/cm 의 **1/22,634 · 1/3,000** 이다.  이 결손을 전부 접합이 진다고 보는 접합-사슬 등가 (R_j ≈ (σ_f/σ* − 1)·r′·ℓ_j) 로는 **R_j ~ 1.3 × 10⁶ Ω × (ℓ_j / 1 µm)** (SBE) · **~1.7 × 10⁵ Ω × (ℓ_j / 1 µm)** (DBE) — 접합 지배 영역 깊숙이다.  ⚠ 읽는 눈금일 뿐: 현 세대는 융합 복셀망 (접합 0) 이라 망 위상이 다르고, AM 경로 몫 · 격자 산물이 섞인다 · **사다리 범위 · 문턱을 이것으로 고르지 않는다** (등록 R §3).

## 8. 적용 인사이트
- ① **검출 ≠ 접촉** — 우리 instance 판정 허용 (≤ 75 nm) 은 위치 불확도 규칙이다.  문헌의 '접촉' (≤ 1.8 nm 터널 · 0.34–0.68 nm vdW 창 — `hamasaki2022_…`) 과 두 자릿수 이상 다르므로, R_j,0 는 **"검출된 근접 쌍 전체의 평균 접합 상태"** 다.  간극 분포가 같은 침대 사이에서만 전이된다.
- ② **P0/P1 = 터널 곡선의 두 끝** — 등록 R ⑱ (*"P 는 두 끝만 등록 · 사이 감쇠는 모형 밖"*) 의 물리 근거로 이 그림 (Fig. 2) 이 쓰인다.
- ③ **÷10 섬유 σ 감도 팔의 해석** — 접합 지배면 σ_e 가 거의 안 움직이는 것이 *정상* 이다 (Fig. 3).  크게 움직이면 그 침대는 섬유 지배 · 혼합 영역 → R_j,0 식별이 약해진다.

## 9. 적용 후보 (11-03)

### (가) 지금 v0 안에서 — 값 채택 없음
1. **한정어 (문서)** — 등록 R §7-1 ⑩ (`docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md:278`) 에: *"instance 검출 허용 (tol_ff ≤ r_f = 75 nm) 은 MPM 경로 위치 불확도이지 물리 간극이 아니다 — 문헌 접합 저항은 아-nm 간극에 지수적으로 걸린다 (Li 2007 Fig. 2: 절연막 0.1 nm 당 ≈ 10 배 · 1.8 nm 에서 망 절연) → R_j,0 = 검출 쌍 전체의 간극 · 막 분포 묶음."*
2. **한정어 (문서)** — 등록 R ⑱ 옆에 근거 한 줄: *"P0 · P1 = 터널막 두께 연속 곡선의 두 끝 (막 ≈ 0 · 막 ≳ 1.8 nm) — 얇은 막의 부분 감쇠는 모형 밖."*
3. **진단 (보고 전용 · 기존 기록)** — 보정 침대에서 접합 지배 여부: 이미 기록되는 소산 분담 (`scripts/carbon_junction.py:2683` `dissipation_share` 의 `vv_junction` 몫) 과 섬유 (축방향) 몫의 비를 보고 → 접합 지배면 Li Fig. 3 영역 (σ ∝ 1/R_j,0 · 섬유 σ 무관) · ÷10 감도 팔 (`FIBRE` · 설계 §1-2 #21) 결과와 같은 쪽인지 대조.  코드 변경 없음.
4. **진단 (보고 전용)** — S0 SBE census 에서 접점 간격 ℓ_j (= 섬유 총길이 / VV instance 수 · 같은 원장) 를 내면 §7-3 의 접합-사슬 등가 R_j 눈금을 보정 **전**에 기록할 수 있다 — ⚠ 사다리 · 문턱을 고르는 데 쓰지 않는다는 문장과 함께 · DBE 는 §2-1 개정 뒤.

### (나) 1저자 비준 필요
1. **간극 의존 R_j** (R_j = R_j,0·exp(2κ(d − d₀))) — 간극 d 를 복셀 · MPM 경로 해상도 (u ≈ 경로 점 간격 / 2) 로는 아-nm 로 알 수 없다 → 물리 없는 손잡이.  **권고: 하지 않는다.**
2. **SE 막 덮임 법칙** (PTFE P1 처럼 SE 가 덮은 접합을 감쇠 · 절단) — 새 법칙 · SE 표현 (MPM SE 점 · 구 스탬프) 과 결합 · SBE 에서 식별 불가.  **권고: 장부 (v1 후보)** — 현재는 R_j,0 에 묶인다는 한정어로.
3. **접점마다 R_j 분포** (로그정규 등) — 분포 폭은 새 손잡이 · 한 점 보정으로 식별 불가.  **권고: 하지 않는다** (분포 효과는 오히려 감도 문장으로).

## 10. 인용 가능 문장
- (EN) *"Using Simmons' rectangular-barrier formula for an insulating film between crossing CNTs (work function 5.0 eV, dielectric constant ~4), Li et al. found tunnelling resistances of ~100 GΩ for a 1.0 nm film and ~10¹⁹ Ω — enough to make the network insulating — for 1.8 nm, which they proposed as the maximum tunnelling distance in CNT composites (Appl. Phys. Lett. 91, 223114, 2007)."*
- (EN) *"With equal contact resistances at all junctions, their simulated network conductivity scaled inversely with the contact resistance and was insensitive to the intrinsic CNT conductivity (10⁴ vs 10⁶ S m⁻¹), i.e., the network was junction-controlled."*
- (KR) *"교차 CNT 사이 절연막의 터널 저항은 막 0.1 nm 마다 약 10 배 커져 1.8 nm 에서 망을 끊는다 (Li 2007) — 접합 저항은 아-nm 간극의 함수이고, 복셀 해상도의 기하 근접으로는 가를 수 없다."*

## 11. 주의 / 한계
1. **실험이 아니라 계산** — 실험과는 문헌 σ 범위의 정성 비교뿐.
2. **모든 접점 같은 R_C · 같은 막 두께** — 저자 스스로 명시.  실제 분포의 효과 (가장 좋은 접합 몇 개가 지배) 는 없다.
3. **A_C = d² (직교 교차) · 교차 각 무시 · 2 nm CNT · 2D 의사-3D 망** — 우리 3D 침대 · Ø 0.15 µm 섬유와 다르다.
4. **Simmons 직사각형 장벽 · φ₀ = CNT 일함수 근사 · U = e/C 가정** — 1 nm 아래 얇은 막에서 Fig. 2 의 톱니 (t ≲ 0.25 nm) 는 그 근사가 의미를 잃는 구간으로 보인다 (우리 해석 · 논문 무언급).
5. **"최대 터널 거리 1.8 nm" 는 σ < 10⁻¹² S/m 라는 절연 정의와 이 망 (p · 크기) 에 묶인 값** — 보편 상수가 아니다.
6. **R_direct contact = 4 × 10⁵ Ω** 은 Fuhrer 2000 류 SWCNT 값에서 고른 입력이다 (출처 문장 없음 — 인용 맥락으로 추정).
7. Fuhrer 인용 "100–400 kΩ (M/M · S/S)" 는 원문 (MM 4 단자 99–300 kΩ · SS 2 단자 하한) 의 반올림 — `fuhrer2000_…` §11 ⑤.
8. 실현 수 · 망 풀이 방법 · 오차 미기재.

## 12. 용어 미니-글로서리
- **터널 저항 (tunneling resistance)**: 얇은 절연막을 사이에 둔 두 도체 사이를 전자가 양자 터널로 건너는 경로의 저항 — 막 두께에 지수적.
- **Simmons 공식**: 얇은 절연막 터널 전류 밀도의 고전 근사식 (1963 · 영상력 포함 일반형).
- **직사각형 장벽**: 장벽 높이를 막 두께 방향으로 일정하게 둔 근사.
- **최대 터널 거리**: 이 논문에서 망이 절연체가 되는 접촉 저항 (10¹⁹ Ω) 에 해당하는 막 두께 (1.8 nm).
- **CNT 매트 · 버키페이퍼**: 기지 없이 CNT 만 엉킨 막 — 접점에 절연막이 없어 튜브 저항이 지배.
- **임계 지수 γ**: 퍼콜레이션 문턱 위 σ ∝ (p − p_c)^γ 의 지수 — 이 논문에선 접촉 저항 수준에 따라 1.78–2.14.

## 13. 이 카드가 확인하지 못한 것 (n/a)
- 망 풀이 방법 · 실현 수 · 퍼콜레이션 문턱 p_c 값 (Fig. 4 에서 ≈ 0.15 vol% 근처의 계단만 보인다 — 숫자 미기재) · R_direct contact 4 × 10⁵ Ω 의 선택 근거 문장 · SE (황화물) · PTFE · 흑연 섬유에 대한 어떤 값도 이 논문에 없다.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
