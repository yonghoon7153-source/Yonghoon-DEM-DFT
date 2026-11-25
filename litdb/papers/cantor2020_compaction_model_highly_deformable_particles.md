<!-- digest 표준 양식. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 꼴 · 절 번호 = cardenasbarrantes2022_soft_spheres_3d_compaction_nscd.md -->
# 매우 무른 (초탄성) 원판 집합의 2D 등방 압밀과 미시역학 압밀 식의 원전 — non-smooth contact dynamics (NSCD) + 입자별 FE (원판 1500 개 × 삼각형 92 개, LMGC90) · 입자 간 마찰 0–0.8 · 압밀 식 P(φ) = (Zφ/2π) × 단일 입자 상자 법칙 · 체적탄성률 K(φ) 의 발산 — ★★ 같은 그룹 압밀 법칙 계열 (혼합 · 3D · 실험) 의 출발점 · "접촉 변형만으로 세운 닫음 (Hertz–Mindlin · 유효 매질) 은 조밀 영역에서 틀린다" 의 2D 근거 — Cantor, Cárdenas-Barrantes, Preechawuttipong, Renouf, Azéma (Phys. Rev. Lett. 2020)

> slug `cantor2020_compaction_model_highly_deformable_particles` · DOI `10.1103/PhysRevLett.124.208003` · type `NSCD+FEM 2D 다입자 (LMGC90 — neo-Hookean 비압축 FE 원판 1500 개 × 삼각형 92 개 · 등방 압축 · 입자 간 μ 0–0.8 · 마찰 없는 벽 상자) + 단일 입자 상자 시험 (메시 6 종) + 미시역학 압밀 이론 (식 1–7)` · PDF `8cfacf47-9._Compaction_model_for_highly_deformable_particle_assemblies.pdf` · digested `2026-11-10` · status ✅
>
> ⚠⚠ **먼저 읽을 것 — 네 겹의 전이 금지**: ① **2D 원판 · 평면변형률** (3D 구가 아니다) · ② 입자가 **초탄성** (neo-Hookean ·
> 비압축 · 하중을 빼면 되돌아옴 · **소성 없음**) ≠ 우리 SE 의 소성 · ③ 모든 압력이 **P/E 무차원** (E 절대값 미기재) — 우리
> 300 MPa 로 옮길 축이 없다 · ④ 무른 원판만 (강체 · 크기비 없음) · 등방 하중 · **하중 쪽만** (탈압 없음).
> ⇒ **절대값 전이 0 건.**  가져오는 것 = (a) 압밀 법칙의 **형식과 유도의 가정** (b) "국소 변형을 접촉 변형만으로 정의하는 닫음은
> 조밀 영역에서 틀린다" 는 **원문 진술과 그 크기** (c) **단일 입자 상자 시험**이라는 단위 시험 형식 (d) 관측량 목록
> (φ(P) · Z(φ) · K(φ)).
>
> ⚠ **본문 상수를 그대로 쓰지 말 것** — 그림의 이론선이 본문 값과 다르다 [판독 + 카드 산술 · §3-3 · §12-B]:
> (i) **b**: 본문 · 그림 5 범례 **0.12** ↔ 그림 4 · 5 의 선 **0.15** · (ii) **φmax (μ 0.8)**: 본문 **0.968** ↔ 같은 논문 자료점
> 0.973 (P/E 0.5) ↔ 그림 4 의 선 0.978 ↔ 그림 6 의 선 0.981 · (iii) **Z0 · φ0 는 본문에 숫자가 없다** (그림에서 역산하면 μ 0 에서
> Z0 ≈ 3.9 · φ0 ≈ 0.81) — 식 (6) 은 이 PDF 의 글만으로는 계산할 수 없다.
>
> **같은 그룹 묶음** (LMGC Montpellier · 같은 틀):
> **이 카드 = 2D 원전** (무른 원판만 · 2020-05) →
> `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` = 2D 강체 + 무른 혼합 (PRE 2020 · 이 논문이 그 ref [62]) ·
> `cardenasbarrantes2021_soft_rigid_mix_compaction_proceedings` = 그 학회 단편 (이 논문이 그 "previous work [17]") ·
> `cardenasbarrantes2022_soft_spheres_3d_compaction_nscd` = 3D 판 (Soft Matter 2022 · 이 논문이 그 ref [57]) ·
> `cardenasbarrantes2022_soft_hard_grains_compaction_experiment_dic` = 2D 실험 검증 (PRE Letter 2022 · 이 논문이 그 SM ref [6]).
> 오각형 판 (PRE 103, 062902, 2021) 은 2026-11-10 현재 inbox 에 PDF 가 있고 카드는 따로 들어온다.
>
> 쪽 표기: 이 카드의 **p. N = 208003-N** (PRL 논문 번호 쪽 · 본문 p. 1–5 · 참고문헌 p. 5–6).

---

## 0. 이 논문이 우리에게 *왜* 중요한가 (한눈 positioning)

[DEM 우선 (수영)] 트랙은 **AM + SE 를 가압부터 탈압까지 한 모델로** 누르는 것을 요구한다.  그 문헌 묶음에서 같은 그룹의 네
카드 (혼합 · 학회판 · 3D · 실험) 가 모두 같은 틀의 **"압밀 식"** 을 쓰고, 그 틀 (미시 구조식 · 배위수 법칙 · 큰 변형의 로그 닫음) 을
"앞선 논문" 에서 가져온다.  이 PRL 이 그 **앞선 논문**이다 — 식이 어디서 나왔고, 무엇을 가정했고, 몇 개를 맞췄는지는 여기서만
확인할 수 있다.

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| **압밀 법칙의 원전** — 식 · 가정 · 맞춘 값 | 식 (6) `P/E = −(bφ/2π){Z0 + k(φ − φ0)^α} ln[(φmax − φ)/(φmax − φ0)]`.  재료 셋 = 입상 응력 텐서 (식 1) · 배위수 법칙 Z − Z0 = k(φ − φ0)^α · 단일 입자 상자 법칙 (식 5) 과 그 척도화 `P ≡ (Zφ/2π)Pp` (식 4).  맞춘 값 = 압밀 곡선에 **φmax 하나** (마찰마다) + 같은 계산의 보조 자료에서 **b** (단일 입자) · **k · α** (Z–φ) |
| "점접촉 (접촉 변형) 닫음은 큰 변형에서 틀린다" 의 **근거 문장과 크기** | p. 3: 작은 변형 틀 (Hertz–Mindlin · 유효 매질) 과 같은 부류의 K1 (식 2) 은 작은 변형에서만 "fair" 하고 φ → 1 에서 어긋남이 커진다 → *"defining local strains only by means of the contact deflections … should be reconsidered"*.  크기 [판독 + 카드 산술]: K1 ÷ 측정 K = **1.8** (jammed) → 0.9 (φ 0.86) → **0.23** (φ 0.966) → **0.06** (φ 0.986) |
| 단위 시험 형식 (우리 U1) | **네 강체 벽 사이의 원판 하나** — 다입자 계와 같은 변형 증분 · 메시 6 종 (92 – 968 요소) · φp(Pp/E) 를 로그 법칙으로 요약 |
| 후보 B (입자별 FE + 접촉) 의 **2D 규모** | 원판 **1500 개** × 삼각형 **92 개** = 요소 138,000 개 [카드 산술] · 마찰 다섯 수준 · 하중 11 수준 [판독] · 계산 시간 · 코어 수 [미확인] |
| 마찰의 효과 | 양 끝만 움직인다 — jammed φ0 0.808 → 0.795 · P/E 0.5 에서 φ 0.985 → 0.973 (μ 0 → 0.8 · 판독).  Z–φ 법칙은 마찰 무관 |
| 재설계 모델이 낼 관측량 | φ(P/E) (두 점근 φ0 · φmax) · Z − Z0 = k(φ − φ0)^α · K(φ) (φmax 에서 발산) · 단일 입자 φp(Pp/E) |

⚠ 하중 쪽만 다룬다 (탈압 없음) · 초탄성이라 소성 잔류가 원리적으로 없다 · 강체 입자가 없다 (혼합은 PRE 2020 판) · 2D.

### 0-1. 이 묶음의 네 질문에 대한 답 (원문 위치와 함께)

| 질문 | 원문 | 카드 정리 |
|---|---|---|
| **(i) DEM (단단한 구 · 점접촉) 의 한계** | p. 1 서론: *"Such body distortions are often dismissed or simplified by considering either the rigid body kinematics as the primary source of deformation or standing on the small-strain framework. However, explicitly describing the particles' large strains is essential…"* · p. 3: *"This equation is reminiscent of those given in Refs. [44–51] deduced upon a small-strain framework (i.e., Hertz-Mindlin contact law) and the effective medium theory. … fair predictions of bulk modulus result for the small-strain domain when standing on the equivalent medium approach. Yet, we observe an increasing mismatch as the solid fraction tends to unity since the assembly of grains starts to behave as a nondeformable solid (i.e., the corresponding bulk modulus diverges). This observation suggests that defining local strains only by means of the contact deflections (i.e., σl = Eεv,ℓ) should be reconsidered."* · p. 2: *"Note that the NSCD approach does not introduce regularization coefficients for the contact laws as other discrete element approaches do…"* | 이 PRL 은 DEM 을 **직접 돌려 견주지 않았다** (그 대조는 3D 판 카드에 있다).  한계 진술의 대상은 "국소 변형 = 접촉 변형" 이라는 닫음 — 겹침 δ 로 변형을 재는 점접촉 DEM 이 쓰는 바로 그 가정이다.  크기 (그림 4 · 판독 + 카드 산술): K1 이 jammed 에서 측정의 1.8 배 · φ ≈ 0.86 에서 만나고 · φ 0.966 에서 1/4.4 · φ 0.986 에서 1/16.  "믿을 수 있는 충전율의 상한" 을 저자가 숫자로 적지는 않았다 |
| **(ii) 소성 · 큰 변형이 왜 어려운가 / 이 논문의 우회 · 비용** | 초록: *"existing models that seek to find the relationship between the confining pressure P and solid fraction φ end up settling for empirical strategies or fitting parameters."* · p. 1: *"We can summarize the limitations of current models by the use of nonphysical parameters, the lack of accuracy at extreme pressures, and the missing physical derivation of the compaction equations. … such a venture should admittedly rely on a proper description of the compaction process while taking into account the multicontact nature of the assembly and the particles' deformability."* · p. 5: *"this approach could be generalized to different material models (elastic, hyperelastic, plastic, etc.) … These alternative mechanical considerations may lead to distinct functional forms, other than logarithmic…"* | 우회 = **소성을 넣지 않았다** (초탄성 · 비압축) + 입자별 FE 로 형상 변화를 직접 풂 + 비정칙 접촉 (접촉 매개변수 = μ 하나).  값 = 원판 1500 개 · 요소 92 개/입자 · 맞춘 값은 φmax (압밀 곡선) + b (단일 입자) + k (Z–φ) · 검증은 **같은 계산 자료뿐** (실험 대조 없음) · 계산 비용 미기재.  소성은 결론의 확장 과제이고, 그때는 **식의 꼴이 로그가 아닐 수 있다**고 저자가 적는다 |
| **(iii) 2D 인가 3D 인가 · 2D → 3D 전이** | **2D**.  p. 1: *"we analyze the compaction of two-dimensional highly deformable particles"* · p. 2: *"neo-Hookean incompressible material model under plane strain conditions"* | 3D 에 대한 말은 **없다** — 확장 과제로 든 것은 다른 재료 모델 · oedometric 하중 · 입자 모양 · 탄성 성질이 다른 물체의 혼합 · 전단 (p. 5).  3D 는 같은 그룹 2022 판이 다뤘고 **식의 꼴이 바뀐다** (`cardenasbarrantes2022_soft_spheres_3d_compaction_nscd` §5-4) — 이 PRL 의 단일 입자 법칙이 jammed 에서 **유한한 기울기**를 갖는 것이 2D 의 성질이기 때문이다 (§9-4) |
| **(iv) 압력을 뺄 때의 거동** | 없음 — *"A set of loading steps were then undertaken targeting stable values of applied pressure and solid fraction"* (p. 2) | 하중 단계만 계산했다.  탈압 · 되돌아옴 · 이력의 근거로 쓸 수 없다.  입자가 초탄성이라 뺀 뒤 형상이 남는 현상 자체가 모델에 없다 |

---

## 1. 한 줄 요약

**KR:** 비압축 neo-Hookean **원판 1500 개** (2D · 평면변형률 · 원판당 삼각형 요소 92 개) 를 LMGC90 의 non-smooth contact dynamics
(NSCD · 비관통 + 건조 마찰 μ = 0 – 0.8 · 접촉 정칙화 없음) 로 **등방 압축**하면, 충전율 φ 가 jammed 값 φ0 에서 비선형으로 올라
**φmax (< 1) 로 점근**하고, 배위수가 마찰과 무관하게 **Z − Z0 = k(φ − φ0)^α** (α ≃ 0.5 · k ≃ 5.1) 를 따르며, 체적탄성률 K 가 φmax
에서 **발산**한다.  기존 압밀 식 (Heckel · Kim–Carroll · Zhang · Nezamabadi) 은 두 점근 가운데 하나를 놓치거나 중간에서 어긋난다.
입상 응력 텐서 `P = (φZ/π)σℓ` 에서 출발해, 접촉 변형만으로 닫은 K1 (식 2) 이 조밀 영역에서 실패함을 보이고, 대신 **네 벽 사이의
입자 하나**의 압축 법칙 `Pp/E = −b ln[(φp,max − φp)/(φp,max − φp,0)]` (b ≃ 0.12) 을 `P ≡ (Zφ/2π)Pp` 로 척도화해 **압밀 식 (6)** 과
체적탄성률 식 (7) 을 얻는다.  φmax 는 식 (6) 을 자료에 맞춰 0.998 (μ 0) · 0.968 (μ 0.8) 로 적었다.

**EN:** 1500 incompressible neo-Hookean disks (plane strain; 92 triangular elements each; frictionless rigid walls) are compressed
isotropically with non-smooth contact dynamics (LMGC90) for interparticle friction μ = 0–0.8.  φ rises from the jammed value φ0 and
saturates at φmax < 1; Z − Z0 = k(φ − φ0)^α with α ≃ 0.5, k ≃ 5.1 independent of friction; the bulk modulus diverges at φmax.  A
contact-deflection closure (Eq. 2, effective-medium like) fails at high density.  Scaling the compaction law of a single particle
between four rigid walls (Eq. 5, b ≃ 0.12) by Zφ/2π gives the compaction equation (Eq. 6) and a bulk-modulus expression (Eq. 7);
φmax is obtained by fitting Eq. (6) (0.998 for μ = 0, 0.968 for μ = 0.8 as printed).

**우리에게 왜 중요한가 (3 줄):** ① **압밀 법칙 계열의 원전** — 형제 카드 넷이 쓰는 식 · 상수 · 닫음의 출처이고, "매개변수
없음" 이 실제로는 **φmax 맞춤 + 보조 맞춤 둘 (b · k)** 임을 여기서 센다.  ② **접촉 변형만의 닫음이 조밀 영역에서 실패한다는
2D 정량 근거** — 강성이 jammed 에서는 1.8 배 과대, φ 0.986 에서는 16 배 과소 [판독 + 카드 산술] 라 **영률 하나를 고쳐서는
양 끝을 동시에 못 맞춘다** (우리 DEM 연화 영률이 "한 압력의 대리" 인 이유).  ③ **단일 입자 시험 = 국소 법칙** — 입자 하나의
압축 곡선에 배위수를 곱해 다체 압력을 쓰는 틀은 재료 모델과 무관하게 후보끼리 견주는 공통 언어가 된다 (단 소성이면 꼴이
바뀐다고 저자가 적는다).

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | Compaction Model for Highly Deformable Particle Assemblies |
| 저자 | **David Cantor**¹˒\*, **Manuel Cárdenas-Barrantes**²˒†, **Itthichai Preechawuttipong**¹˒‡, **Mathieu Renouf**²˒§, **Emilien Azéma**²˒∥ (다섯 명 모두 전자우편 표기 — 교신 저자 표시는 따로 없음) |
| 소속 | ¹ Department of Mechanical Engineering, Chiang Mai University, 239 Huay Kaew Road, 50200 Chiang Mai, Thailand · ² LMGC, Université de Montpellier, CNRS, 34090 Montpellier, France |
| 저널 | **Physical Review Letters 124, 208003 (2020)** · 6 쪽 (208003-1 – 208003-6 · 발행 정보 줄 "0031-9007/20/124(20)/208003(6)" = 20 호) · **Editors' Suggestion** |
| DOI | 10.1103/PhysRevLett.124.208003 |
| 날짜 | Received 13 February 2020 · revised manuscript received 9 April 2020 · accepted 4 May 2020 · **published 20 May 2020** |
| 판권 | © 2020 American Physical Society |
| 코드 | **LMGC90** — "free, open-source simulation platform" (ref [37] = https://git-xen.lmgc.univ-montp2.fr/lmgc90/lmgc90_user/wikis/home) · 방법 상세는 refs [34] (Jean 1999) · [38] (Dubois, Acary, Jean 2018) 로 넘김 |
| 계산 자원 | High-Performance Computing Platform **MESO@LR** (감사의 글) · **CPU 시간 · 코어 수 · 병렬 여부 [미확인]** |
| 감사 | Jonathan Barés ("fruitful discussions") · D. C. = Chiang Mai University 박사후 연구원 지원 · Franny McGill |
| 자금 | [미확인] (PDF 에 과제 번호 없음) |
| 그림 · 표 · 식 · 문헌 | 그림 **6** · 표 **0** · 식 **(1)–(7)** · 참고문헌 **52** |
| SI | **미수령 · 있는지 [미확인]** — 본문 · 참고문헌 어디에도 Supplemental Material 언급이 없고 inbox 에 보충 PDF 가 없다 |
| 소재 | **모델 소재** — 비압축 neo-Hookean 원판.  응용 동기 = 분말 (세라믹 · 금속 · 제약) · 점토 · 고무 입자 · 세포 · 거품 · 겔, 콘크리트 · 포장에 넣는 고무, 혈구 흐름 (서론).  ⛔ SE · CAM 아님 |
| 연구유형 | 수치 (NSCD + FEM, **2D**) + 해석 이론 (미시역학 압밀 식 · 체적탄성률 식).  실험 없음 |

**1저자 메모의 서지와 대조**: 저자 5 명과 순서 · 제목 · Phys. Rev. Lett. 124, 208003 (2020) · DOI — 전부 원문과 같다 (다른 점 없음).
메모에 없던 것 = Editors' Suggestion 표지 · 날짜 넷.

---

## 3. 핵심 수치 — 본문 / 판독 / 카드 산술 구분

> 표기: **본문** = 본문 · 캡션 · 범례에 인쇄된 값 (쪽 표기) · **[판독]** = 그림에서 읽음 · **[카드 산술]** = 카드가 논문 숫자로 계산
> (식 병기) · **[미확인]** = 원문에 없음.
> ★ 이 논문은 본문에 인쇄된 숫자가 적다 (Np · 요소 수 · μ · 0.05 % · α · k · b · φmax 둘 · π/4 가 거의 전부).  φ0 · Z0 · 곡선의
> 값 · K 의 값은 **그림에서만** 얻을 수 있다.

### 3-1. 입력 · 설정 (전부 본문 · p. 2)

| 양 | 값 | 비고 |
|---|---|---|
| 차원 · 기하 | **2D** · 원판 · 상자 ("boxes" · "the volume V enclosed by the rigid walls") | 주기 경계 아님 · 상자 모양 · 종횡비 [미확인] |
| 입자 수 | **Np = 1500** | 시료 수 (마찰마다 한 개인지) [미확인] — 그림에 오차막대 없음 |
| 크기 분포 | "a slight size dispersion around an average diameter d to avoid crystallization" | 범위 · 꼴 [미확인] (형제 PRE 2020 판은 [0.8d, 1.2d]) |
| 메시 | 원판당 "**92** triangular similar-size finite elements" | 단일 입자 시험은 N_e = 92 (두 방식) · 116 · 174 · 272 · 572 · 968 (그림 5 범례) · 요소 차수 [미확인] |
| 재료 | "hyperelastic … **neo-Hookean incompressible** material model under **plane strain** conditions" (refs [11,36]) · 영률 E | E 값 · ν 미기재 ("incompressible" 로만 · 형제 PRE 2020 판은 ν 0.495) |
| 마찰 | 입자 간 **μ = 0 · 0.2 · 0.4 · 0.6 · 0.8** ("in the interval [0, 0.8], in steps of 0.2") · 입자–벽 **0** · 중력 **0** | |
| 준비 | 단순 기하 규칙의 침적 알고리즘 [39] 으로 원판을 상자에 쌓음 → "relatively dense configuration, yet not in contact" → 마찰 지정 | 출발 = 서로 닿지 않은 조밀한 배치 (겹침 0) |
| 하중 | **등방 압축** · "A set of loading steps … targeting stable values of applied pressure and solid fraction" · 압력을 "gradually applied" | μ = 0 에서는 등방과 oedometric 하중이 "indistinct" (refs [40,41]) |
| 안정 판정 | 주어진 압력에서 φ 변화가 **0.05 %** 아래 | 형제 PRE 2020 판은 0.01 % |
| 무차원 하중 | **P/E** | 11 수준 = 1 · 5 × 10⁻⁴ · 1 · 5 × 10⁻³ · 1 · 2.5 · 5 · 7.5 × 10⁻² · 1 · 2.5 · 5 × 10⁻¹ [판독 — 표식 가로 위치] · 스냅숏 5 × 10⁻⁴ · 5 × 10⁻¹ (그림 1 캡션) |
| 기준 상태 | P/E → 0 = "the corresponding jammed state for the rigid assembly" → 첨자 0 (φ0 · Z0) | 값은 본문에 없다 |
| 풀이 | NSCD — unilateral contact + dry friction · time-stepping · "does not introduce regularization coefficients for the contact laws" | Δt · 반복 수 · 허용오차 · 벽 속도 · 관성수 [미확인] |
| 감쇠 | "the particle-to-particle interaction and the particles' bulk rapidly damped the kinetic energy and elastic waves had little influence on the particle reorganization" | 수치 감쇠를 따로 넣었는지 [미확인] |

### 3-2. 결과 숫자 (본문)

| 양 | 값 | 위치 |
|---|---|---|
| 배위수 법칙 | (Z − Z0) = k(φ − φ0)^α · **α ≃ 0.5** (문헌 [11,16,44]) · **k ≃ 5.1** · 마찰 무관 | p. 3 · 그림 3 |
| k 의 뜻 | "a structural parameter fully defined as the P/E → ∞, and φ and Z reach maximal values" — 즉 k = (Zmax − Z0)/(φmax − φ0)^α [카드 풀이 · 형제 카드들의 표기와 같음] | p. 3 |
| 국소–거시 변형 | ε_v,ℓ = 2 ln(⟨ℓ^c⟩/d) · **ε_v = 2 ε_v,ℓ** ("Our numerical simulations also revealed") | p. 3 |
| 단일 입자 시작 충전율 | **φp,0 = π/4** (Pp/E → 0) | p. 4 |
| 단일 입자 상수 | **b ≃ 0.12** ("found to be") · 그림 5 범례도 "Local model (b ≃ 0.12)" | p. 4 · 그림 5 |
| φmax | **0.998** (마찰 0) · **0.968** (μ = 0.8) — "Simple fitting of Eq. (6) reveals" | p. 4 |
| 마찰의 효과 | "the coefficient of friction essentially modifies the maximal and minimal solid fraction since sliding mobilization is increasingly limited with μ" | p. 2 |
| K 에 대한 마찰의 효과 | "little influence on the macroscopic bulk modulus for the small deformation domain, but then its effects increase for larger strains" | p. 4 |
| 스냅숏 압력 | P/E = 5 × 10⁻⁴ · 5 × 10⁻¹ (마찰 0) | 그림 1 |

### 3-3. ★ 그림 정밀 판독

> **방법**: 그림 2 – 6 은 PDF 안에서 **벡터** 다 (그림 1 만 래스터 749 × 945 px).  쪽을 1200 dpi 로 그린 뒤 축 틀과 **눈금 선**의 픽셀
> 위치로 선형 · 로그 사상을 세웠다 (예: 그림 6 — P/E 눈금 10⁻⁴ · 10⁻³ · 10⁻² · 10⁻¹ = x 973 · 1723 · 2473 · 3223 px = 750 px/decade,
> 오른쪽 틀 = 1; φ 눈금 0.80 · 0.85 · 0.90 · 0.95 = y 1638 · 1262 · 885 · 508 px; 축 위 끝은 φ = 1.001 로 읽힌다).
> **선** = 파선 조각 (대시) 의 중심을 모아 읽음 — 세로 1 px = φ 0.00013, 선 중심 ±0.0003–0.0005.
> **표식** = 마찰 0 의 빈 원은 고리 맞춤 (그림 2 와 6 을 따로 읽어 차 ≤ 0.001), 나머지는 순색 픽셀의 위 · 아래 끝 중점 (겹친 곳은
> 확대해 눈으로) — **±0.001–0.002**.  K (그림 4) 의 표식은 로그 축에서 눈으로 읽어 **±10 %**.
> **검증**: 표식의 가로 위치가 P/E = 1 · 5 · 10 · … 의 둥근 값에 1–3 % 안에서 떨어진다 · 그림 3 의 가로값 (φ − φ0) 이 그림 2 의
> φ − 0.808 과 0.001 안에서 같다 · 그림 4 의 회색 선과 그림 5 의 파선이 해당 식에 0.2 % · 5 × 10⁻⁵ 로 맞는다 (아래 (c)).
> 전부 **[판독]** 이다 — 원저자 수치 파일이 아니다.

**(a) 그림 2 · 6 — 압밀 곡선 φ(P/E), 마찰별**

| P/E | μ = 0 | μ = 0.2 | μ = 0.4 | μ = 0.6 | μ = 0.8 |
|---|---|---|---|---|---|
| 1 × 10⁻⁴ | 0.808 | 0.800 | 0.797 | 0.794 | 0.795 |
| 5 × 10⁻⁴ | 0.809 | 0.801 | 0.798 | 0.796 | 0.796 |
| 1 × 10⁻³ | 0.814 | 0.803 | 0.800 | 0.798 | 0.798 |
| 5 × 10⁻³ | 0.826 | 0.814 | 0.810 | 0.808 | 0.808 |
| 1 × 10⁻² | 0.840 | 0.825 | 0.820 | 0.818 | 0.818 |
| 2.5 × 10⁻² | 0.864 | 0.848 | 0.843 | 0.841 | 0.841 |
| 5 × 10⁻² | 0.887 | 0.880 | 0.871 | 0.870 | 0.870 |
| 7.5 × 10⁻² | 0.900 | 0.889 | 0.884 | 0.881 | 0.880 |
| 1 × 10⁻¹ | 0.914 | 0.904 | 0.899 | 0.897 | 0.896 |
| 2.5 × 10⁻¹ | 0.966 | 0.955 | 0.952 | 0.950 | 0.949 |
| 5 × 10⁻¹ | 0.985 | 0.977 | 0.975 | 0.974 | 0.973 |

- **jammed φ0** (P/E 10⁻⁴ 의 값): 0.808 (μ 0) → 0.800 → 0.797 → 0.794 → 0.795 (μ 0.8).  마찰 0.6 과 0.8 은 전 구간에서 구별되지 않는다
  (차 ≤ 0.001).
- **자료의 끝**: P/E 0.5 에서 φ 0.985 (μ 0) – 0.973 (μ 0.8).  거시 체적 변형 ε_v = ln(φ/φ0) ≈ **0.20** (두 마찰 모두) [카드 산술].
- **★ μ 0.8 의 마지막 자료점 0.973 은 본문의 φmax 0.968 보다 높다.**
- 자료가 매끈하지 않은 곳 [카드 산술]: 기울기 dφ/d ln(P/E) 가 P/E 0.05 – 0.075 구간에서만 꺼진다 (세 구간 0.025 → 0.05 → 0.075 → 0.1
  에서 μ 0.8: 0.042 · **0.025** · 0.056, μ 0: 0.033 · **0.032** · 0.049) — P/E 0.05 의 점이 높거나 0.075 의 점이 낮다.  원인 [미확인].

**(b) 그림 6 — "모델" 선 (식 6) 과 자료 · 본문 상수로 계산한 식 (6)**

| P/E | μ 0 자료 | μ 0 선 | 식 (6) b 0.12 | 식 (6) b 0.15 | μ 0.8 자료 | μ 0.8 선 | 식 (6) b 0.12 · φmax 0.968 | 식 (6) b 0.15 · φmax 0.978 |
|---|---|---|---|---|---|---|---|---|
| 1 × 10⁻⁴ | 0.808 | 0.811 | 0.810 | 0.810 | 0.795 | 0.793 | 0.793 | 0.793 |
| 1 × 10⁻³ | 0.814 | 0.815 | 0.813 | 0.812 | 0.798 | 0.795 | 0.796 | 0.795 |
| 5 × 10⁻³ | 0.826 | 0.826 | 0.823 | 0.821 | 0.808 | 0.804 | 0.806 | 0.804 |
| 1 × 10⁻² | 0.840 | 0.836 | 0.834 | 0.829 | 0.818 | 0.812 | 0.816 | 0.813 |
| 2.5 × 10⁻² | 0.864 | 0.858 | 0.859 | 0.851 | 0.841 | 0.833 | 0.841 | 0.836 |
| 5 × 10⁻² | 0.887 | 0.883 | 0.890 | 0.879 | 0.870 | 0.858 | 0.870 | 0.863 |
| 7.5 × 10⁻² | 0.900 | 0.901 | 0.912 | 0.899 | 0.880 | 0.877 | 0.891 | 0.884 |
| 1 × 10⁻¹ | 0.914 | 0.915 | 0.929 | 0.915 | 0.896 | 0.893 | 0.907 | 0.900 |
| 2.5 × 10⁻¹ | 0.966 | 0.963 | 0.978 | 0.968 | 0.949 | 0.944 | 0.952 | 0.951 |
| 5 × 10⁻¹ | 0.985 | 0.989 | 0.995 | 0.992 | 0.973 | 0.973 | **0.966** | 0.973 |
| 선의 끝 (P/E ≈ 0.98) | — | **0.998** | — | — | — | **0.981** | (0.968 을 넘지 못함) | (0.978 을 넘지 못함) |

- 열 3 · 4 · 8 · 9 = **[카드 산술]**: 식 (6) 에 k 5.1 · α 0.5 와 **그림에서 역산한** Z0 3.9 · φ0 0.810 (μ 0) / Z0 3.75 · φ0 0.793 (μ 0.8) 을
  넣어 φ 를 풀었다 (Z0 · φ0 가 본문에 없어 다른 길이 없다 — 역산은 (c)).  b 0.12 = 본문 · b 0.15 = 그림 4 · 5 의 선이 쓰는 값.
- **선 ↔ 자료**: μ 0 은 차 ≤ 0.006 (rms 0.003).  μ 0.8 은 P/E 0.005 – 0.05 에서 선이 0.004 – 0.012 **낮고** 나머지는 ≤ 0.004
  (rms 0.005).  본문 표현은 "outstanding for any pressure".
- **본문 상수의 식 (6) ↔ 자료 (μ 0)**: b 0.12 는 P/E 0.075 – 0.5 에서 +0.010 – +0.015 **높다** (rms 0.008) · b 0.15 는 P/E 0.005 – 0.05 에서
  0.006 – 0.012 **낮다** (rms 0.006).  어느 쪽도 그림의 선 (rms 0.003) 만큼 붙지 않는다.
- **선은 어떤 상수의 식 (6) 인가** (식 (6) 에 k 5.1 · α 0.5 를 두고 φmax · φ0 만 선에 맞춰 견줌):
  - 본문 상수 **b 0.12** (Z0 3.9 / 3.75): 선과 최대 **0.017** (μ 0 · rms 0.005) · **0.023** (μ 0.8 · rms 0.008) 어긋난다 — 선이 더 뻣뻣하다.
  - 그림 4 · 5 의 선이 쓰는 **b 0.15**: 최대 **0.006** (μ 0 · rms 0.0025) · **0.011** (μ 0.8 · rms 0.0035) — 선 굵기 (φ 로 0.003) 의 두세 배.
  - 판독 잡음 (rms 0.0004) 까지 맞추려면 중괄호 자리의 값이 달라져야 한다: 선을 `−φ{A + B(φ − φ0)^0.5} ln[…]` 로 맞추면
    (A, B, φmax, φ0) = **μ 0: (0.031, 0.319, 0.9985, 0.8102) · μ 0.8: (0.089, 0.193, 0.982, 0.793)** 인데, 식 (6) 이 주는
    (A, B) = (bZ0/2π, bk/2π) 는 μ 0 에서 (0.074, 0.097) (b 0.12) · (0.093, 0.122) (b 0.15) 다.
  - ⇒ 그림 6 의 선은 **b ≈ 0.15 근처의 식 (6)** 으로 보이지만 정확히 어떤 상수로 그렸는지는 PDF 로 가릴 수 없다.  분명한 것은 둘:
    **b 0.12 가 아니다 · μ 0.8 의 φmax 는 0.968 이 아니다 (선의 끝이 0.981).**

**(c) 그림 3 · 4 · 5 의 이론선 — 어떤 상수로 그려졌나 (선을 읽어 식에 맞춤)**

| 선 | 맞춘 식 | 결과 [판독 맞춤] | 본문 값 |
|---|---|---|---|
| 그림 3 파선 (대시 30 개) | Z − Z0 = k(φ − φ0)^α | **k = 5.20 · α = 0.500** (rms 0.0004) | k ≃ 5.1 · α ≃ 0.5 |
| 그림 4 회색 실선 K1 | 식 (2) | **Z0 = 3.91 · k = 5.08 · φ0 = 0.809** (ln K 의 rms 0.002) · 선은 φ 0.8086 에서 시작 | Z0 · φ0 미기재 |
| 그림 4 검정 점선 K2 (μ 0 · 대시 22 개) | 식 (7) | b·Z0 = 0.587 · b·k = 0.760 · **φmax = 0.9980** (rms 0.001) → k 5.1 이면 **b = 0.149 · Z0 = 3.94** | b ≃ 0.12 · φmax 0.998 |
| 그림 4 주황 점선 K2 (μ 0.8 · 대시 20 개) | 식 (7) | b·Z0 = 0.551 · b·k = 0.750 · **φmax = 0.9780** (rms 0.001) → k 5.1 이면 **b = 0.147 · Z0 = 3.75** | b ≃ 0.12 · φmax **0.968** |
| 그림 5 파선 (대시 31 개) | 식 (5) | **b = 0.150 · φp,max = 1.000 · φp,0 = 0.786** (rms 5 × 10⁻⁵) · b 를 0.12 로 묶으면 rms 0.006 | b ≃ 0.12 · φp,0 = π/4 = 0.785 |

- ⇒ **그림 4 · 5 의 선은 b ≈ 0.15 로 서로 맞고** (0.147 – 0.150), 본문 · 범례의 0.12 와 다르다.  예: 식 (5) 에 b 0.12 를 넣으면 Pp/E 0.1 에서
  φp = 0.907 인데 그림의 선은 0.890 을 지난다 (b 0.15 → 0.890) [카드 산술].
- ⇒ **φmax (μ 0.8) 는 셋이다**: 본문 0.968 · 그림 4 의 선 0.978 · 그림 6 의 선 0.981 넘게 (맞추면 0.982).  마찰 0 은 셋 다 0.998 근처.
- ⇒ **Z0 ≈ 3.9 (μ 0) · ≈ 3.75 (μ 0.8)** 는 이 역산으로만 얻는다 (뒤 값은 b 가 두 마찰에서 같다는 가정 위).

**(d) 그림 4 — 체적탄성률 K/E (마찰 0)**

| φ | 측정 (빈 원) | 찬 원 (ZφKp/2π · 식 3) | K1 (식 2 선) | K1 ÷ 측정 | K2 (식 7 선) | K2 ÷ 측정 |
|---|---|---|---|---|---|---|
| 0.808 | 0.28 | — | 0.51 | **1.8** | 0.32 | 1.15 |
| 0.826 | 0.32 | 0.43 | 0.66 | 2.1 | 0.43 | 1.35 |
| 0.839 | 0.42 | 0.48 | 0.72 | 1.7 | 0.50 | 1.2 |
| 0.863 | 0.9 | 0.67 | 0.82 | 0.9 | 0.67 | 0.74 |
| 0.886 | 1.15 | 0.85 | 0.92 | 0.8 | 0.89 | 0.77 |
| 0.913 | 1.6 | 1.35 | 1.02 | 0.64 | 1.30 | 0.81 |
| 0.966 | 5.3 | 4.0 | 1.21 | **0.23** | 4.1 | 0.78 |
| 0.986 | 21 | 11 | 1.29 | **0.06** | 11.7 | 0.56 |

- 측정 · 찬 원 = [판독 ±10 %] · K1 · K2 = 선에 맞춘 식의 값 [(c) 의 상수].
- **K1 (접촉 변형 닫음)**: 0.51 (φ0) → 1.34 (φ = 1) 로 2.6 배 오를 뿐이다.  측정 K 는 같은 구간에서 75 배 오른다.  ⇒ jammed 에서
  1.8 배 과대 · φ ≈ 0.86 에서 교차 · φ 0.966 에서 1/4.4 · φ 0.986 에서 1/16.
- **K2 (식 7)** 는 찬 원 (단일 입자 척도화) 과 거의 겹친다 — 둘 다 같은 단일 입자 법칙에서 나오기 때문.  측정과는 φ ≤ 0.84 에서
  +15 – +35 % · φ 0.86 – 0.97 에서 **−19 – −26 %** · 마지막 점에서 −44 %.  본문 표현은 "perfectly reproducing the evolution of K
  throughout the deformation" (로그 세 자릿수 축에서는 붙어 보인다).
- 마찰이 있는 계 (μ 0.2 – 0.8 · 판독): 빈 표식 ≈ 0.4 – 0.55 (φ 0.795 – 0.80) · ≈ 4.6 – 5.2 (φ 0.950 – 0.955) · ≈ 22 – 23 (φ 0.974 – 0.978),
  찬 표식은 뒤 두 곳에서 ≈ 3.0 – 3.6 · ≈ 9.5 – 10.5 (측정의 0.45 – 0.7 배).  **μ > 0 의 자료가 φ 0.974 – 0.978 까지 있다** — 본문
  φmax 0.968 (μ 0.8) 보다 높은 자리다.

**(e) 그림 5 — 단일 입자 상자 시험 φp(Pp/E)**

| Pp/E | N_e 92 (검은 원 · E 고정) | N_e 92 (빨간 네모 · Pp 고정) | N_e 116 – 572 | N_e 968 | 파선 (b 0.15 로 읽힘) | 식 (5) b 0.12 [카드 산술] |
|---|---|---|---|---|---|---|
| 1 × 10⁻⁴ | ≈ 0.792 | ≈ 0.792 | 0.786 – 0.790 | ≈ 0.784 | 0.786 | 0.786 |
| 1 × 10⁻² | 0.803 | 0.803 | 0.800 – 0.806 | 0.810 | 0.800 | 0.803 |
| 2.5 × 10⁻² | — | — | 0.821 – 0.832 | 0.836 | 0.818 | 0.826 |
| 3.2 × 10⁻² | 0.829 | 0.829 | 0.838 – 0.842 | 0.846 | 0.827 | 0.836 |
| 5 × 10⁻² | — | — | 0.851 – 0.862 | 0.865 | 0.846 | 0.859 |
| 1 × 10⁻¹ | 0.895 | 0.895 | 0.889 – 0.898 | 0.903 | 0.890 | 0.907 |
| 2.5 × 10⁻¹ | — | — | 0.947 – 0.950 | 0.957 | 0.960 | 0.973 |
| 3.2 × 10⁻¹ | **0.955** | **0.978** | 0.961 – 0.967 | 0.970 | 0.975 | 0.985 |
| 5 × 10⁻¹ | — | — | 0.977 – 0.981 | 0.986 | 0.992 | 0.997 |

- 표식 = [판독 ±0.002 – 0.003 · 겹친 곳은 확대해 눈으로] · 파선 = 대시 중심.
- **메시 의존**: 같은 압력에서 메시 사이의 φp 차 = 0.009 – 0.023 (Pp/E 0.05 – 0.5).  가장 고운 968 이 거의 늘 가장 높다 (무르다) —
  92 요소 (검은 원) 는 968 보다 0.017 (Pp/E 0.032) · 0.008 (0.1) · 0.015 (0.32) 낮다.  치밀화량 φp − φp,0 으로 보면 92 요소가 968 보다
  **28 % · 7 % · 8 % 적게** 눌린다 [카드 산술: (0.829 − 0.785)/(0.846 − 0.785) 등].  본문 표현 = "has no major effect".
- **하중 방식 의존**: 같은 92 요소인데 Pp/E 0.32 에서 E 를 바꿔 누른 쪽 (빨간 네모) 0.978 ↔ Pp 를 바꾼 쪽 (검은 원) 0.955 — 차 0.023.
- **작은 압력의 시작값**: 92 요소는 ≈ 0.792 로 π/4 (0.785) 보다 높다 (거친 다각형 메시의 면적 · 접촉 탓으로 보인다 — [미확인]).
- **b 는 한 값이 아니다** [카드 산술 · 식 (5) 를 φp,max = 1 로 거꾸로 풂]: 자료 범위가 주는 b = 0.11 – 0.14 (Pp/E 0.05) · 0.13 – 0.15 (0.1) ·
  0.16 – 0.18 (0.25) · 0.18 – 0.22 (0.5).  ⇒ 본문 0.12 는 낮은 압력 쪽, 그림의 선 0.15 는 전 구간 절충, 형제 PRE 2020 판 본문 0.14 는
  그 사이.  파선은 Pp/E 0.01 – 0.1 에서 자료보다 0 – 0.02 **낮고** 0.25 위에서 0.003 – 0.015 **높다** (Pp/E 0.32 의 빨간 네모만 선 위).

**(f) 그림 2 — 기존 모델 넷의 선 (마찰 0 자료에 맞춘 것 · 대시 중심 판독)**

| P/E | 자료 (μ 0) | Heckel (1961) | Zhang et al. | Kim–Carroll (1987) | Nezamabadi et al. (2019) |
|---|---|---|---|---|---|
| 1 × 10⁻⁴ | 0.808 | ≈ 0.811 (평탄) | 0.800 | 축 아래 | ≈ 0.811 (평탄) |
| 1 × 10⁻² | 0.840 | 0.830 | 0.850 | 축 아래 | 0.827 |
| 2.5 × 10⁻² | 0.864 | 0.854 | 0.874 | 축 아래 (선이 P/E ≈ 0.025 – 0.03 에서 올라옴) | 0.850 |
| 5 × 10⁻² | 0.887 | 0.887 | 0.897 | ≈ 0.877 | 0.888 |
| 1 × 10⁻¹ | 0.914 | 0.930 | 0.922 | 0.936 | 0.951 |
| 2.5 × 10⁻¹ | 0.966 | 0.985 | 0.956 | 0.975 | 축 위 (P/E ≈ 0.14 에서 φ = 1) |
| 5 × 10⁻¹ | 0.985 | 0.998 | ≈ 0.976 | ≈ 0.987 | 축 위 |

- 본문 평: 자료에는 수평 점근이 둘 (φ0 · φmax) 있다 · Kim–Carroll 은 첫째를, Nezamabadi 는 둘째를 못 잡는다 · Heckel 과 Zhang 은 둘 다
  있지만 중간 압력에서 "slightly mismatch" · 넷 다 맞춤 매개변수에 기댄다 (p. 2).
- 판독으로 본 Heckel 선의 차: −0.010 (P/E 0.01 · 0.025) → 0 (0.05) → +0.016 (0.1) → +0.019 (0.25).  Zhang: +0.008 – +0.010 (0.01 – 0.1) → −0.010 (0.25).
- 이 선들에 쓴 맞춤값은 본문에 없다 [미확인].

### 3-4. [카드 산술] 확인 계산

| 계산 | 결과 | 쓰임 |
|---|---|---|
| 요소 수 = 1500 × 92 | **138,000** 삼각형 | 3D 판 (구 50 · 100 × 사면체 808 = 40,400 · 80,800) 과 같은 자릿수 — 3D 로 가며 입자 수가 1/15 |
| 식 (1) 검산: Np πd²/4 = φV → nc = Nc/V = (Z/2)(4φ/πd²) = 2φZ/πd² · P = (σ1 + σ2)/2 = (nc/2)⟨f ℓ⟩ | `P = (φZ/π)·⟨f⟩⟨ℓ⟩/d²` — 인쇄 꼴과 같다 | 식 (1) 은 자기일관 (힘이 가지 방향이고 f · ℓ 가 무상관일 때) |
| 식 (2) 검산: P/E = (φZ/2π) ln(φ/φ0) [σℓ = Eε_v,ℓ · ε_v = 2ε_v,ℓ] → K = φ dP/dφ → ln(φ/φ0) ≈ 1 − φ0/φ · α = 1/2 | `K1/E = (Zφ/π)(5/4 − φ0/2φ) − Z0φ/4π` — 인쇄 꼴과 **정확히** 같다 | 식 (2) 의 "first-order Taylor expansion" 은 ln(φ/φ0) ≈ 1 − φ0/φ 이고 α = 1/2 이 이미 들어가 있다 |
| K1(φ0) = Z0φ0/2π | Z0 3.9 · φ0 0.809 → **0.50** | 그림 4 회색 선의 시작 0.51 과 맞음 · 측정 ≈ 0.28 의 1.8 배 |
| K1(φ = 1) (Z0 3.9 · k 5.1 · φ0 0.809) | **1.34** | 접촉 변형 닫음은 발산하지 않는다 |
| 식 (7) 검산: 식 (6) 을 미분 → K = bφ²Z/[2π(φmax − φ)] − (b/2π)φ(Z + φZ′)ln[…] · 뒤 항 (양수) 을 버림 | 정확한 미분 ÷ K2 = **1.07** (φ 0.82) · 1.13 (0.85) · **1.17** (0.90) · 1.15 (0.95) · 1.09 (0.98) · 1.05 (0.99) | "neglecting high-order terms" 의 크기 — K2 는 식 (6) 의 강성을 5 – 17 % 낮게 준다 |
| K2(φ0) = bφ0²Z0/[2π(φmax − φ0)] (Z0 3.9 · φ0 0.810 · φmax 0.998) | b 0.12 → **0.26** · b 0.15 → **0.33** | 측정 ≈ 0.28 – 0.30 · K1 0.50 |
| 단일 입자 초기 강성 Kp(φp,0)/E = b·φp,0/(φp,max − φp,0), φp,max = 1 | b 0.12 → **0.44** · b 0.15 → **0.55** | 2D 단일 입자 법칙은 jammed 에서 유한한 기울기 (§9-4) |
| 식 (4) 의 배율 Zφ/2π | jammed (Z 3.9 · φ 0.81) **0.50** · 가장 조밀 (Z 6.2 · φ 0.985) **0.97** | 다체 압력 ≈ 0.5 – 1 × 단일 입자 압력 |
| 식 (1) 을 정사각 격자의 단일 입자 칸에 쓰면 (Z = 4 · φp = πd²/4L² · σℓ = F L/d²) | P = F/L = Pp, 즉 σℓ = (π/4φp)Pp (0.79 – 1.0 Pp) | 식 (4) 는 σℓ ≡ Pp/2 를 뜻한다 — 다입자 계의 접촉 응력이 같은 충전율의 정사각 칸의 **0.5 – 0.64 배** 라는 경험 대응 (유도 아님) |
| 식 (5) → (6) 의 사상을 같은 변형으로 엄밀히 하면 φp = (π/4)(φ/φ0) | φmax = (4φ0/π)·φp,max = **1.031** φp,max (μ 0) · 1.012 φp,max (μ 0.8) | φp,max = 1 이면 다체 계가 유한한 압력에서 φ = 1 을 넘는다 → 그래서 φmax 를 **맞춤 양**으로 둔 것 (기호를 바꿔 넣은 것이지 변수 변환이 아니다) |
| Zmax = Z0 + k√(φmax − φ0) | 3.9 + 5.1·√0.188 = **6.1** (μ 0) · 3.75 + 5.1·√0.185 = **5.9** (μ 0.8) | 면을 채운 2D 다각형의 평균 이웃 수 6 (세 칸이 한 꼭짓점에서 만날 때 · 카드 추론) 과 맞는다 → k ≈ (6 − Z0)/√(φmax − φ0) = 4.8 – 5.2 |
| 거시 체적 변형 (P/E 0.5) = ln(φ/φ0) | ln(0.985/0.808) = **0.198** · ln(0.973/0.795) = 0.202 | "highly deformable" 의 크기 |
| 92 요소 ↔ 968 요소의 치밀화량 비 (그림 5) | 0.72 (Pp/E 0.032) · 0.93 (0.1) · 0.92 (0.32) | 다입자 계산 (92 요소) 의 압밀 곡선이 수렴값보다 뻣뻣할 수 있는 정도 |
| 300 MPa ÷ E (우리 값 · 주 리포) | 실제 SE E 22 – 24 GPa → **0.0125 – 0.0136** · DEM 연화 E 1.35 → **0.22** · MPM E 1.53 → **0.20** | §8-5 — 한정어와 함께만 읽을 것 |
| 위 P/E 에서의 이 논문 자료 (μ 0 · log 보간) | 0.0125 – 0.0136 → φ ≈ **0.846 – 0.848** (φ − φ0 ≈ 0.04) · 0.20 – 0.22 → φ ≈ **0.95 – 0.96** | 〃 |

### 3-5. ★ 이 논문에 **없는** 값 (찾으러 갔다가 없다고 확인)

- **φ0 · Z0 의 숫자** (마찰별) — 식 (6) · (7) · (2) 의 입력인데 본문 · 캡션 어디에도 없다 (형제 학회판 Table 1 에는 혼합 계의 값이 있다).
- **φp,max 의 숫자** · 기존 모델 넷 (그림 2) 의 맞춤값 · 그림 6 의 선에 실제로 넣은 상수.
- **계산 시간 · 코어 수 · 병렬 여부 · 메모리** (감사의 글에 HPC 플랫폼 이름만).
- **E · ρ · d 의 절대값**, 벽 속도, 관성수, Δt, 반복 수 · 허용오차, 접촉 탐색 방식, 요소 차수, ν, 크기 분포의 범위.
- **시료 수 · 반복 · 오차막대** · rattler 처리 · 벽 접촉을 Z 에 넣었는지 · 상자 모양.
- **탈압 · 이력 · 잔류 변형** · 접촉력 분포 · 접촉 길이 · 입자 형상 지표 · 입자 안 응력 분포 (뒤 셋은 실험판 · 3D 판에 있다).
- **DEM 과의 직접 대조** · **실험 대조** · **3D** · **소성 · 점착 · 파쇄 · 강체 혼합 · 크기비**.

---

## 4. 방법 ★

### 4-1. Non-smooth contact dynamics (NSCD) (p. 2)

- *"We simulated assemblies of incompressible deformable particles undergoing isotropic compression in the frame of the contacts
  dynamic and finite element methods. This numerical coupling, also known as nonsmooth contact dynamics (NSCD) [34,35], considers
  unilateral contact conditions and dry friction between particles previously discretized in finite elements. Contact forces and body
  deformations are then systematically solved within a time-stepping scheme."*
- ★ *"Note that the NSCD approach does not introduce regularization coefficients for the contact laws as other discrete element
  approaches do, making this numerical scheme robust and stable."* ⇒ **접촉 강성 같은 정칙화 계수가 없다** — 접촉 매개변수는 μ 하나이고,
  변형은 FE 몸체의 E 로만 들어가며 겹침은 0 이다.
- 구현 = 오픈소스 **LMGC90** [37].  풀이 알고리즘 이름 (Gauss–Seidel 등) · Δt 는 이 논문에 없다 (3D 판 카드 §4-1 이 "nonlinear
  Gauss–Seidel" 로 적었다).

★ **우리 DEM 과의 결정적 차이** (형제 카드와 같음): LIGGGHTS 는 겹침 δ 에 비례하는 벌칙 힘으로 접촉을 정칙화하고 그 강성이 압밀
결과를 바꾼다.  NSCD 에는 접촉 강성이 없다.

### 4-2. 저자의 지도 — 수치 방법과 기존 압밀 식 (p. 1)

| 저자 분류 | 저자 설명 | 우리 후보 |
|---|---|---|
| meshless 방법 [14–16] | 변형 입상체를 탐구하게 해 준 최근 수치 접근 (Boromand 외 · Nezamabadi 외) | A · A′ (ref [16] = Nezamabadi 외, Comput. Phys. Commun. 237, 17 (2019) — litdb `nezamabadi2022_mpm_cd_plastic_particle_compaction` 카드가 암시적 MPM + CD 계보의 문헌으로 적은 것 · 우리 미열람) |
| discrete element method [17,18] | 〃 | D0 · C · C′ |
| coupled finite element–discrete element [11,19–24] | 〃 (Vu 외 [11] · Procopio & Zavaliangos [19] · Güner 외 · Abdelmoula 외 · Huang 외 · Mollon · Loidolt 외) | **B** |

| 기존 압밀 식 | 저자 평 (p. 1) |
|---|---|
| **Heckel** [2] — `P ∝ −ln(1 − φ)` | 압밀을 화학 반응에 견준 유비 · "yields fair predictions" · **상수 둘 (K · B) 이 "not clearly related to physical or mechanical properties"** |
| **Kim & Carroll** [3] — 금속 분말 · 비슷한 꼴 | 상수 셋 (Y0 · μ · γ) 을 실험 · 맞춤으로 정해야 한다 |
| **Nezamabadi et al.** [16] — `P ∝ −φ ln(φ)` | 평균 압력의 증분 정식화 + 거시 유효 P 파 탄성률 · 맞춤 상수 (c1 · c2) |
| **Zhang et al.** [25] — MPFEM + 이중 로그 식 | 곡선은 잘 재현하나 "the origin of such a relation is not identified" |
| 그 밖 [5,26–33] | "none of them is entirely satisfactory" |

⇒ 저자의 요약 (p. 1): 기존 모델의 한계 = **비물리 매개변수 · 극한 압력에서의 부정확 · 압밀 식의 물리적 유도 부재**.
★ 우리 쪽: 우리 DEM Heckel 적합 (P_y 138 MPa) 의 두 상수도 같은 평을 받는 부류다 — 물성으로 인용하지 않는다.

### 4-3. 단일 입자 상자 시험 — 메시 검사이자 "국소 법칙" (p. 4 · 그림 5)

- 조건: *"an analogous elementary system composed of a single particle between four rigid walls following the multiparticle boundary
  conditions"* — 다입자 계와 **같은 변형 증분** (ε_v ≡ ε_v,p) 을 준다.  벽 마찰은 다입자 경계 조건을 따른다고 했으므로 0 으로 읽힌다.
- 관측: φp (원판 넓이 / 상자 넓이) vs Pp/E.  φp,0 = π/4.  Kp(φp) = (dPp/dφp)(dφp/dε_v,p), ε_v,p = −ln(φp,0/φp).
- 메시: N_e = 92 (두 방식 — Pp 고정 · E 변화 / E 고정 · Pp 변화) · 116 · 174 · 272 · 572 · 968 (나머지는 E 고정 · Pp 변화).
- 판정 (본문): 단일 입자 곡선이 다입자 곡선과 "roughly akin" · 메시 해상도는 "at least for the element densities tested, has no major
  effect on the results" → 다입자 계산은 **92 요소**.  판독값은 §3-3 (e) — 차 0.009 – 0.023, 968 이 가장 무른 쪽.
- 요약식 (식 5): `Pp/E = −b ln[(φp,max − φp)/(φp,max − φp,0)]`, b ≃ 0.12 — "obtained from the corresponding loss of void space analogous
  to the collapse of a cavity within an elastic medium under isotropic compression [52]" (Carroll & Kim 1984).
- ⚠ 3D 판은 이 시험을 하지 않고 Hertz 로 닫았다 (형제 카드 §8-3).  ⚠ 해석해와의 대조는 없다 — 기준은 "메시끼리 비슷한가" 뿐.

### 4-4. 시료 · 하중 (p. 2)

1. 원판 Np = 1500 개 (평균 지름 d · 약한 크기 분산) 를 기하 규칙 침적 알고리즘 [39] 으로 상자에 쌓는다.  원판당 삼각형 92 개.
2. 침적 뒤 = "relatively dense configuration, yet not in contact".  이 상태에서 입자 간 μ 를 0 · 0.2 · 0.4 · 0.6 · 0.8 로 지정
   (입자–벽 마찰 0 · 중력 0).  ⇒ 다섯 마찰이 **같은 침적 배치**에서 출발하는 것으로 읽힌다 (명시는 없음).
3. 하중 단계를 차례로 걸어 압력 · 충전율의 안정값을 얻는다.  안정 = φ 변화 < 0.05 %.  압력을 천천히 올려 운동 에너지가 곧 감쇠.
4. P/E → 0 의 상태 = 강체 집합의 jammed 상태 → φ0 · Z0.

### 4-5. 정의식 · 압밀 식 (전사 — 식 크롭은 그림 폴더의 `eq_*.png`)

| 식 | 내용 (인쇄 그대로) | 카드 주 |
|---|---|---|
| — p. 3 | `σij = nc⟨f_i^c ℓ_j^c⟩` · `nc = Nc/V` · `Pσ = (σ1 + σ2)/2` · "It is evident that P = Pσ" | 입상 응력 텐서 [44] · ℓ^c = 접촉한 두 입자의 **도심**을 잇는 벡터 · V = 강체 벽이 둘러싼 넓이 |
| — p. 3 | `nc = 2φZ/πd²` · `Z = 2Nc/Np` → `σij = (2φZ/πd²)⟨f_i^c ℓ_j^c⟩` | "considering a small particle size dispersion around diameter d" |
| (1) p. 3 | `P = (φZ/π) σℓ` , `σℓ = ⟨f^c⟩⟨ℓ^c⟩/d²` | "taking into account that contact forces and branches are not correlated" · refs [45–47] |
| — p. 3 | `(Z − Z0) = k(φ − φ0)^α` · α ≃ 0.5 · k ≃ 5.1 | 마찰 무관 (그림 3) |
| — p. 3 | `ε_v = −ln(φ0/φ)` · `K(φ) = (dP/dφ)(dφ/dε_v)` · `ε_v,ℓ = 2 ln(⟨ℓ^c⟩/d)` · `ε_v = 2ε_v,ℓ` · 가정 `σℓ = Eε_v,ℓ` | 연속체 · 균질 변형 · 스프링 [47].  ⚠ 압축에서 ε_v,ℓ 은 음수 · ε_v 는 양수 — 크기로 읽는다 |
| (2) p. 3 | `K1(φ)/E = (Zφ/π)(5/4 − φ0/2φ) − Z0φ/4π` | 접촉 변형 닫음 · 형제 PRE 2020 카드의 `(Zφ/2π)(5/2 − φ0/φ) − Z0φ/4π` 와 같은 식 (묶는 법만 다름) |
| — p. 3 | `ε_c,ℓ = −ln(V_ℓ/V_ℓ,0)` (V_ℓ = 입자를 감싼 Voronoi 칸의 부피) · "by construction, ε_v = ε_c,ℓ" | 접촉 변형 대신 **입자를 감싼 칸의 부피** 로 국소 변형을 정의 → 단일 입자 상자로 넘어가는 다리 |
| — p. 4 | `Kp(φp) = (dPp/dφp)(dφp/dε_v,p)` · `ε_v,p = −ln(φp,0/φp)` · `φp,0 = π/4` | 단일 입자 |
| (3) p. 4 | `K ≡ (Zφ/2π) Kp + O` | "O negligible high-order terms" · "O … is simply related to the derivatives (dZφPp + ZdφPp)" |
| (4) p. 4 | `P ≡ (Zφ/2π) Pp` | 식 (1) 의 재해석 ("Supported on Eq. (3), we can also reinterpret Eq. (1)") |
| (5) p. 4 | `Pp/E = −b ln[(φp,max − φp)/(φp,max − φp,0)]` | b ≃ 0.12 · 공동 붕괴 유비 [52] |
| (6) p. 4 ★ | `P/E = −(bφ/2π){Z0 + k(φ − φ0)^α} ln[(φmax − φ)/(φmax − φ0)]` | "noting that φ can be mapped to φp (since ε_v ≡ ε_p,v)" · φmax 는 맞춤 |
| (7) p. 4 | `K2(φ)/E ≃ bφ²/[2π(φmax − φ)] · {Z0 + k(φ − φ0)^α}` | 식 (6) 의 미분에서 "high-order terms (e.g., in the form of φ^(α+1) ln φ)" 를 버림 |

**식 (6) 의 유도 흐름과 가정 (본문 순서 + 카드 정리)**

1. **입상 응력 텐서 → 식 (1)**: 크기 분산이 작다 (nc 를 d 하나로 씀) · 접촉력과 가지 길이가 무상관.
2. **배위수 법칙**: Z − Z0 = k(φ − φ0)^α, 마찰과 무관.
3. **첫 닫음 (K1 · 식 2) — 버려진다**: 연속체 · 균질 변형 · 스프링 · σℓ = Eε_v,ℓ · ε_v = 2ε_v,ℓ.  작은 변형에서는 "fair", φ → 1 에서 실패
   → *"defining local strains only by means of the contact deflections … should be reconsidered."*
4. **둘째 닫음 — Voronoi 칸 → 단일 입자 상자**: 국소 변형을 입자를 감싼 칸의 부피 변화로 정의하고, 그 칸의 거동을 "네 강체 벽
   사이의 입자 하나" 로 대신한다.  그림 4 에서 K 가 (Zφ/2π)Kp 처럼 오르는 것을 보고 **식 (3) · (4) 로 "재해석"** 한다 — 이 두 식은
   유도가 아니라 관찰에 붙인 척도화다 (`≡` 로 쓴다).
5. **단일 입자 법칙 (식 5)**: 로그 꼴 · b 는 단일 입자 자료에서.
6. **합침 → 식 (6)**: 식 (5) 와 Z(φ) 를 식 (4) 에 넣고 φp → φ, φp,0 → φ0, φp,max → φmax 로 기호를 바꾼다.  φmax 는 압밀 곡선에 맞춘다.
7. **성립 범위 (저자 말)**: *"accurately predicts the sample density ranging from the granular jamming point, up to solids fractions close
   to the unity for any interparticle coefficient of friction"* (p. 1–2) · *"outstanding for any pressure capturing the asymptotes for
   vanishing and extremely high pressures"* (p. 4).  자료 범위 = P/E 10⁻⁴ – 0.5 · φ 0.795 – 0.985 [판독].  틀 밖 = 재료 모델이 다른
   경우 ("may lead to distinct functional forms, other than logarithmic") · oedometric · 다른 모양 · 혼합 · 전단 (p. 5).

**맞춘 값은 몇 개이고 무엇에 맞췄나**

| 상수 | 본문 값 | 어디서 | 성격 |
|---|---|---|---|
| **φmax** | 0.998 (μ 0) · 0.968 (μ 0.8) | 압밀 곡선 φ(P/E) 에 "simple fitting of Eq. (6)" — 마찰마다 | **거시 곡선에 맞춘 값 (1 개 / 마찰)** |
| **b** | ≃ 0.12 | 단일 입자 상자 시험의 φp(Pp/E) | 보조 계산에 맞춘 값 (재료 모델 + 상자 기하에 묶임) |
| φp,max | 미기재 | 〃 ("maximal solid fraction attainable") | 〃 |
| **k** | ≃ 5.1 | Z–φ 자료 (그림 3) | 보조 자료에 맞춘 값 (= (Zmax − Z0)/(φmax − φ0)^α) |
| α | ≃ 0.5 | 문헌 [11,16,44] + 그림 3 | 문헌값 |
| Z0 · φ0 | 미기재 | jammed 상태 (P/E → 0) | 잰 값 (맞춤 아님 · 준비 방법과 마찰에 달림) |
| φp,0 | π/4 | 기하 | 맞춤 아님 |

⇒ 초록의 *"free from ad hoc parameters"* 는 "임의로 넣은 매개변수가 없다" 는 뜻으로 읽어야 한다 — **같은 계산의 자료에 맞춘 값이
셋 (φmax · b · k)** 이고 그 가운데 φmax 는 예측하려는 곡선 자신에 맞췄다.

### 4-6. ★ 입자 처리 — **진짜 형상 변형인가?**

| 질문 | 이 논문 | 우리 DEM (D0) | 우리 MPM |
|---|---|---|---|
| 무른 입자 형상이 진짜 바뀌나 | **예** — 2D FE 메시가 변형, 원 → 다각형 (그림 1) | 아니오 — 강체 구 + 겹침 | 예 (J2 소성 흐름) |
| 그 변형의 종류 | **초탄성 (가역)** · 비압축 | (접촉 법칙 hooke/hysteresis) | 소성 (비가역) · ν 0.49 |
| 입자 경계가 남나 | **예** — 비관통 · 마찰 · 분리 가능 | 예 (구 접촉) | 아니오 — 단일 속도장 (닿으면 붙음) |
| 강체 입자 | 없음 (무른 원판만) | NCM 구 (움직임) | AM = 얼린 장애물 |
| 접촉 매개변수 | **μ 하나** (0 – 0.8 스윕) | E_eff · ν · μ · COR … | (격자 암묵) |
| 크기비 | 없음 (약한 분산) | AM ⌀4–9 µm · SE ⌀~1 µm | DEM 씨앗 |
| 입자 수 | **1500** | 수만 | 씨앗 수만 |
| 경계 | 마찰 없는 강체 벽 상자 (등방) | 주기 (x · y) + 판 (z) | 판 (z) |
| 차원 | **2D** (평면변형률) | 3D | 3D |
| 탈압 | 없음 | 진행 중 | 부분 |

---

## 5. 결과 — 절별 상세

> PRL 이라 절 제목이 없다.  아래는 본문 순서대로 묶은 것이다.

### 5-1. 압밀 곡선과 기존 모델 (그림 1 · 2 · p. 2)

- 스냅숏 (마찰 0): P/E 5 × 10⁻⁴ 에서는 원이 거의 그대로이고 변형 (색) 이 접촉점에 몰린다.  P/E 5 × 10⁻¹ 에서는 다각형으로 바뀌어
  공극이 세 입자 사이의 작은 틈으로만 남는다.
- φ(P/E): 두 수평 점근 — "one for the perfectly rigid granular assembly (φ0) and the other for extremely high pressures (φmax)".
- μ = 0 에서는 등방과 oedometric 하중이 구별되지 않는다 (refs [40,41] — Peyneau & Roux · Khalili 외).
- 기존 모델 넷을 마찰 0 자료에 맞춰 겹쳐 그림 → 어느 것도 두 점근과 중간 구간을 함께 못 맞춘다 (§3-3 (f)).
- 마찰: "essentially modifies the maximal and minimal solid fraction since sliding mobilization is increasingly limited with μ [42,43]".
  [판독] 양 끝이 0.012 – 0.013 내려가고 μ ≥ 0.6 에서 포화.

### 5-2. 미시 구조식과 배위수 (식 1 · 그림 3 · p. 3)

- *"Keeping in mind the discrete nature of these assemblies, an adequate compaction model should rely on the physical phenomena taking
  place at the particles and contacts scales."*
- 식 (1) `P = (φZ/π)σℓ` — *"reveals the joint relation between P and φ and the granular microstructure in terms of particle connectivity
  and force transmission."*
- 배위수: 더 조밀한 배치가 더 높은 Z 를 준다 · 문헌에서 거듭 보고된 Z − Z0 = k(φ − φ0)^α (α ≃ 0.5) 를 **마찰과 무관하게** 다시
  얻었다.  [판독] 마찰 0 의 최대 Z − Z0 = 2.29 (φ − φ0 0.178), 다른 마찰은 2.0 – 2.2 (φ − φ0 0.157 – 0.182).

### 5-3. 접촉 변형 닫음 K1 과 그 실패 (식 2 · 그림 4 · p. 3)

- 충전체를 연속체로 보고 접촉을 스프링으로 바꿔 σℓ = Eε_v,ℓ 를 가정 → 식 (2).
- *"This equation is reminiscent of those given in Refs. [44–51] deduced upon a small-strain framework (i.e., Hertz-Mindlin contact law)
  and the effective medium theory."* (refs = Andreotti 외 교재 · Agnolin & Roux · Khalili 외 · Bathurst & Rothenburg · Walton · Goddard ·
  Makse 외 · La Ragione & Magnanimo)
- 결과: 작은 변형에서는 "fair predictions", φ → 1 에서 "an increasing mismatch" — 입자 집합이 "a nondeformable solid" 처럼 굴어 K 가
  발산하기 때문.  [판독] §3-3 (d).
- 결론 문장: *"This observation suggests that defining local strains only by means of the contact deflections (i.e., σl = Eεv,ℓ) should be
  reconsidered."*

### 5-4. Voronoi 칸 → 단일 입자 → 척도화 (식 3 – 5 · 그림 4 · 5 · p. 3 – 4)

- 대안: 거시 변형을 입자별 Voronoi 칸의 부피 변화 ε_c,ℓ = −ln(V_ℓ/V_ℓ,0) 의 기여로 쌓는다.  물음 = *"to what extent can the volumetric
  behavior of such a local configuration be related to the bulk modulus of the multiparticle system?"*
- 답: 네 강체 벽 사이의 입자 하나.  그 압축 곡선이 다입자 곡선과 "roughly akin" → *"supporting the idea of a deep relation between the
  two systems."*
- 그림 4 의 찬 표식 = ZφKp/2π.  *"the macroscopic bulk modulus of the assembly K increases as the relation (Zφ/2π) does, allowing us to
  reinterpret the micromechanical origin of the bulk modulus as K ≡ (Zφ/2π)Kp + O."*
- *"Equation (3) suggests that the single-particle configuration is no other than the smallest representative scale in our multiparticle
  system."* · *"Equations (3) and (4) reveal that the elastic and compaction properties of a deformable particle assembly are scalable
  from the behavior of an individual particle."*
- [판독] 찬 표식 ÷ 빈 표식 = 1.1 – 1.35 (φ ≤ 0.84) · 0.74 – 0.84 (φ 0.86 – 0.966) · 0.52 (φ 0.986) (마찰 0) — "O negligible" 은 그림에서
  ±25 % – 2 배 수준의 차로 읽힌다.

### 5-5. 압밀 식과 K2 (식 6 · 7 · 그림 6 · 4 · p. 4)

- 식 (5) 와 Z(φ) 를 식 (4) 에 넣어 식 (6).  그림 6: μ 0 · 0.8 두 선.  *"the predictions given by Eq. (6) are outstanding for any pressure
  capturing the asymptotes for vanishing and extremely high pressures and the effect of the coefficient of friction."*
- *"Our compaction equation also allows us to predict the saturation of solid fraction as μ increases. Simple fitting of Eq. (6) reveals
  that φmax = 0.998 for the frictionless case, while φmax = 0.968 for μ = 0.8."*
- 식 (6) 을 미분해 식 (7).  *"Fig. 4 presents the above relation perfectly reproducing the evolution of K throughout the deformation for
  the cases μ = 0 and μ = 0.8."*  마찰은 작은 변형의 K 에는 거의 영향이 없고 큰 변형에서 커진다.
- *"Such a high-quality capacity of prediction also supports, a posteriori, the validity of our analysis."* — 척도화 (식 3 · 4) 의 근거가
  **사후 일치**임을 저자가 적는다.
- [판독 + 카드 산술] 실제 차이는 §3-3 (b) · (c) · (d).

### 5-6. 결론 · 저자가 적은 확장 (p. 4 – 5)

- 요약: *"we developed a compaction model whose ingredients are deeply encoded in the evolution of grain connectivity and the bulk
  behavior of a representative single particle."*  ad hoc 매개변수 없이 "well-defined quantities (i.e., solid fraction, coordination
  number, and applied pressure)" 위에 선다.
- 범위의 한정: *"Although our compaction model is deduced in the frame of the neo-Hookean material model, our purpose is also to present a
  methodical and micromechanically based approach…"*
- 확장: *"this approach could be generalized to different material models (elastic, hyperelastic, plastic, etc.) or to other loading
  configurations such as the oedometric compression test. These alternative mechanical considerations may lead to distinct functional
  forms, other than logarithmic, but certainty linked to the behavior of individual particles."*
- 다음 과제: *"to extend this work using different grain shapes, to consider mixtures of bodies with varying elastic properties, and to
  characterize the shear behavior."*  (모양 = 오각형 판 PRE 2021 · 혼합 = PRE 2020 · 3D = Soft Matter 2022 · 일축 실험 = PRE Letter 2022 로
  이어졌다 — 뒤 셋은 형제 카드.)

---

## 그림별 (원 캡션 요지 + MPM 관점)

> 파일: `litdb/figures/cantor2020_compaction_model_highly_deformable_particles/` · 300 dpi.  그림 6 장은 `extract_figures.py` 로 자르고
> 전부 열어 확인했다 — 그림 1 · 5 · 6 은 쪽 머리의 저널 괘선이 섞여 그래픽 경계 + 3 pt 로 다시 잘랐다 (`recrop`).  이 논문에는
> **표가 없고 보충 자료는 받지 못했다** (본문에 언급 없음).  식 7 개와 본문 식 문단 7 개는 PDF 글자 층이 분수 · 첨자 · 등호를
> 깨뜨려 손으로 잘랐다 (`eq_*.png` · `manual_crop`).  테두리 잉크 검사 0.  캡션도 글자 층이 `=` 를 `¼` 로, `/` 를 `=` 로 적어
> 쪽 그림을 보고 다시 적었다.  "MPM 관점" = figures.json 의 `mpm_note_ko` 와 같은 글.

| 파일 | 원 캡션 요지 | MPM 관점 (재설계가 재현해야 할 것 · 후보 대응) |
|---|---|---|
| `fig_1.png` | 그림 1 — 마찰 0 시료의 스냅숏: (a) P/E = 5 × 10⁻⁴ · (b) P/E = 5 × 10⁻¹; 색의 세기 = 입자 안 체적 변형 | 원판 1500 개 (그림은 그 일부) 가 P/E 5 × 10⁻⁴ (jammed 직후 · 변형이 접촉점에만) 에서 5 × 10⁻¹ (φ ≈ 0.985 · 판독) 로 가면 원이 다각형이 되고 공극은 세 입자가 만나는 자리의 작은 틈으로만 남는다 — 입자 경계 (검은 선) 는 끝까지 유지된다 (입자별 유한요소 + 접촉 = 후보 B 의 2D 실물).  우리 단일 속도장 MPM 은 이 경계선 (SE–SE 계면) 을 그리지 못한다.  색 눈금이 없고, 재료가 '비압축' 인데 색이 체적 변형이라고 적혀 있다 (근사 비압축으로 보임 — 형제 PRE 2020 판은 ν 0.495).  탄성이라 하중을 빼면 되돌아간다 (탈압 계산 없음). |
| `fig_2.png` | 그림 2 — 충전율 φ vs P/E (마찰 0 · 0.2 · 0.4 · 0.6 · 0.8) + 마찰 0 자료에 맞춘 기존 모델 넷 (Heckel · Zhang et al. · Kim–Carroll · Nezamabadi et al.); 삽도 = 선형 축 | 재설계 후보의 1차 관측량 = 이 S 자 곡선: jammed φ0 (마찰 0 → 0.8 에서 0.808 → 0.795) 에서 올라 P/E 0.5 에서 0.985 → 0.973 (판독 ±0.002).  마찰은 양 끝을 0.012–0.013 내릴 뿐 곡선 모양은 같고, 마찰 0.6 과 0.8 은 구별되지 않는다.  기존 모델 넷은 마찰 0 자료에 맞춘 것인데도 어긋난다 (판독): Kim–Carroll 선은 낮은 압력 점근이 없고 (P/E ≈ 0.03 아래에서 축 밖), Nezamabadi 식은 포화가 없어 P/E ≈ 0.14 에서 φ = 1 에 닿으며, Heckel 은 P/E 0.01–0.025 에서 0.010 낮고 0.1–0.25 에서 0.016–0.019 높고, Zhang 은 0.01–0.1 에서 0.008–0.010 높다.  우리 Heckel (φmax = 1 고정) 은 이 그림의 Heckel 선과 같은 부류다.  ⚠ 2D 원판 · 초탄성 · P/E 무차원 — 값을 3D 소성 SE 로 옮기지 않는다.  ※ 범례의 'Zhang et al (2014)' 는 참고문헌 [25] (2015) 와 연도가 다르다. |
| `fig_3.png` | 그림 3 — 배위수 초과분 Z − Z0 vs 충전율 초과분 φ − φ0 (모든 마찰 · 삽도 log–log); 파선 = 거듭제곱 Z − Z0 = k(φ − φ0)^α (범례 α = 0.5) | 배위수 증가가 마찰과 무관하게 Z − Z0 = k(φ − φ0)^α 하나로 접힌다 (본문 k ≃ 5.1 · α ≃ 0.5; 파선은 k = 5.20 · α = 0.500 으로 읽힌다 · 판독 맞춤) — 압밀 식 (6) 의 구조 입력.  마찰 0 자료는 작은 φ − φ0 에서 선 아래 (0.031 에서 0.78 ↔ 선 0.92), 큰 쪽에서 선 위 (0.178 에서 2.29 ↔ 2.19) 다 (판독).  최대 Z − Z0 ≈ 2.3 → Z ≈ 6.2 (Z0 ≈ 3.9 는 그림 4 의 선에서 역산 · 카드 산술) = 면을 다 채운 2D 다각형의 평균 이웃 수 6 근처.  단일 속도장 MPM 에서는 Z 가 정의되지 않는다 — 입자 경계를 유지하는 후보 (A′ · B · C · C′ · D0) 에서만 잴 수 있다.  D0 (LIGGGHTS) 압축 궤적에서 새 런 없이 지수 · 계수를 재 볼 수 있다 (2D 값 5.1 은 기대값으로 쓰지 않는다). |
| `fig_4.png` | 그림 4 — 체적탄성률 K/E vs φ: 측정 (빈 표식) · 식 (3) 의 미시 구조 기원 ZφKp/2π (찬 표식) · 회색 실선 = 식 (2) K1 (μ 0) · 검정 / 주황 점선 = 식 (7) K2 (μ 0 / μ 0.8) | 측정 K/E (빈 표식) 는 jammed 에서 ≈ 0.3 (마찰 0 · 판독) 이고 φmax 로 가며 20 넘게 발산한다.  접촉 변형만으로 세운 K1 (식 2 · 회색 선 — Hertz–Mindlin / 유효 매질류와 같은 부류) 은 0.51 → 1.34 로 거의 평평해 jammed 에서 1.8 배 높고 φ 0.986 에서 16 배 낮다 (판독 + 카드 산술) — '접촉 변형 (점접촉) 닫음은 조밀 영역에서 틀린다' 의 2D 근거.  단일 입자 상자 시험의 Kp 를 Zφ/2π 배 한 값 (찬 표식 · 식 3) 은 추세는 따르지만 φ ≥ 0.95 에서 측정의 0.45–0.75 배다 (판독 · 본문은 차이 O 를 'negligible' 이라 한다).  K2 (식 7) 의 두 선은 b ≈ 0.15 · φmax 0.998 (μ 0) / 0.978 (μ 0.8) 일 때의 식과 0.1 % 안에서 같다 (판독 맞춤 · k 5.1 가정) — 본문의 b ≃ 0.12 · φmax 0.968 과 다르다.  마지막 마찰 0 점 (φ 0.986) 에서는 측정 ≈ 21 ↔ K2 선 ≈ 11.7 (판독).  우리 쪽: 조밀 영역의 강성 발산은 입자 벌크 응답에서 온다 → 접촉 법칙 후보 (C · C′) 를 볼 때 φ(P) 와 함께 K(φ) 를 본다. |
| `fig_5.png` | 그림 5 — 입자 하나의 압밀 곡선 φp vs Pp/E, 메시별 (N_e 92 · 92 · 116 · 174 · 272 · 572 · 968); 빨간 네모 = Pp 고정 · E 변화, 검은 원 = E 고정 · Pp 변화 (둘 다 92 요소); 파선 = 국소 모델 식 (5) (범례 b ≃ 0.12); 삽도 = N_e 968 스냅숏 (색 = 체적 변형) | 네 강체 벽 사이의 원판 하나 = 이 논문의 '가장 작은 대표 척도' 이자 메시 검사 (우리 단위 시험 U1 과 같은 꼴 · 2D).  φp 가 π/4 근처에서 시작해 로그 법칙 (식 5) 으로 포화한다.  메시 92–968 요소 사이의 φp 차이는 Pp/E 0.05–0.5 에서 0.009–0.023 (판독) 이고 가장 고운 968 이 거의 늘 가장 무른 쪽이다 (φp 가 높다) — 본문 표현은 'no major effect'.  다입자 계산에 쓴 92 요소 (검은 원 · E 고정) 는 968 보다 0.008–0.017 낮고 (Pp/E 0.032 · 0.1 · 0.32), 같은 92 요소인데 E 를 바꿔 누른 쪽 (빨간 네모) 은 Pp/E 0.32 에서 0.978 로 검은 원 (0.955) 보다 0.023 높다 (판독) — 무차원 곡선이 하중 방식에 따라서도 갈린다.  ⚠ 파선은 b = 0.150 · φp,max = 1.000 · φp,0 = 0.786 의 식 (5) 와 일치한다 (대시 31 개 맞춤 · rms 5 × 10⁻⁵ · 판독) — 범례 · 본문의 b ≃ 0.12 로는 Pp/E 0.1 에서 φp 0.907 이어야 하는데 선은 0.890 이다.  자료 자체도 한 b 로 안 맞는다 (압력별로 b 0.11–0.22 · 카드 산술).  재설계 MPM (또는 B) 이 SE 입자 하나에 대해 먼저 통과할 시험 — 3D 대응의 시작값은 구 / 외접 정육면체 π/6 이고, 소성이면 로그 꼴이 아닐 수 있다 (저자 결론). |
| `fig_6.png` | 그림 6 — 압밀 곡선 (그림 2 와 같은 자료) + 식 (6): μ = 0 (검정 파선) · μ = 0.8 (주황 파선); 삽도 = 선형 축 | 식 (6) '모델' 선과 자료.  선은 jammed 평탄부 0.811 (μ 0) · 0.793 (μ 0.8) 에서 0.998 · 0.981 로 포화한다 (판독).  선 ↔ 자료: μ 0 은 ±0.006 안, μ 0.8 은 P/E 0.005–0.05 에서 선이 0.004–0.012 낮다 (판독).  ⚠ 선은 본문 상수로 재현되지 않는다: 식 (6) 에 b 0.12 · k 5.1 · α 0.5 · φmax 0.998 (Z0 3.9 · φ0 0.810 은 그림 역산) 을 넣으면 P/E 0.075–0.25 에서 φ 가 선보다 0.011–0.015 높고 (φ 0.90–0.97 에서 같은 φ 의 압력이 18–28 % 낮다), μ 0.8 의 본문 φmax 0.968 은 선의 끝 (0.981) 과 자료점 (P/E 0.5 에서 0.973) 보다 낮다 (카드 산술 + 판독).  그림 4 · 5 의 선이 쓰는 b 0.15 로는 선과의 차가 최대 0.006 (μ 0) · 0.011 (μ 0.8) 으로 준다.  ⇒ 법칙은 형식 비교에만 쓰고 계수는 옮기지 않는다.  재설계 후보의 φ(P) 를 같은 형식으로 적합해 b · k · φmax 를 견줄 수 있다. |
| `eq_01a_stress_tensor_definitions.png` | 본문 문단 p. 3 — 입상 응력 텐서 · 접촉 밀도 · 배위수 정의 (식 (1) 의 재료) | 입상 응력 텐서 σij = nc⟨f_i ℓ_j⟩ · 접촉 밀도 nc = 2φZ/πd² · Z = 2Nc/Np · P = (σ1 + σ2)/2 — 식 (1) 의 재료.  우리 DEM 의 Love–Weber 응력과 같은 정의 계열 (벽 반력이 아니라 접촉력 × 가지 벡터).  본문은 'P = Pσ 는 자명' 이라고만 쓰고 벽 압력과의 수치 대조는 싣지 않았다. |
| `eq_01_pressure_micro.png` | 식 (1) p. 3 — 미시 구조식 P = (φZ/π)σℓ | 압력 = 충전율 × 배위수 × 평균 접촉 응력 (2D).  접촉력과 가지 길이가 상관없다고 보고 ⟨f ℓ⟩ 를 ⟨f⟩⟨ℓ⟩ 로 나눈 꼴이다.  입자 경계가 없는 단일 속도장 MPM 에서는 Z · σℓ 가 정의되지 않는다 — 이 분해는 입자를 푸는 후보 (A′ · B · C · C′ · D0) 의 공통 언어. |
| `eq_01b_sigma_l_and_z_phi_power_law.png` | 본문 문단 p. 3 — σℓ 정의 · 배위수 거듭제곱 법칙 (α ≃ 0.5 · k ≃ 5.1 · 마찰 무관) | σℓ = ⟨f⟩⟨ℓ⟩/d² 정의 + 배위수 법칙 (Z − Z0) = k(φ − φ0)^α: α ≃ 0.5 (문헌 [11,16,44]) · k ≃ 5.1 ('P/E → ∞ 에서 φ · Z 가 최대값에 닿는 것으로 완전히 정해지는 구조 매개변수' = (Zmax − Z0)/(φmax − φ0)^α).  마찰과 무관하다고 적는다.  ※ 본문은 자기 계산을 'our experiments' 라고 부른다 (실험은 없다). |
| `eq_02a_k1_closure_assumptions.png` | 본문 문단 p. 3 — K1 을 세우는 가정 (연속체 · 균질 변형 · 스프링 · ε_v,ℓ = 2 ln(⟨ℓ⟩/d) · ε_v = 2ε_v,ℓ · σℓ = Eε_v,ℓ) | K1 을 세우는 가정: 충전체를 연속체로 보고 · 변형이 균질하며 · 접촉을 평균 길이 ⟨ℓ⟩ 의 스프링으로 바꾸고 · 국소 체적 변형 ε_v,ℓ = 2 ln(⟨ℓ⟩/d) · σℓ = E ε_v,ℓ.  여기에 수치 관찰 ε_v = 2 ε_v,ℓ (거시 체적 변형이 접촉 길이에서 셈한 값의 두 배 → 선형 접촉 변형으로는 4 배) 가 들어간다.  겹침 δ 로 변형을 재는 점접촉 DEM 과 같은 정보만 쓰는 닫음이다.  ※ 압축에서 ε_v,ℓ = 2 ln(⟨ℓ⟩/d) 는 음수, ε_v = −ln(φ0/φ) 는 양수라 등식은 크기로 읽어야 한다 (부호 규약이 섞여 있다). |
| `eq_02_bulk_modulus_k1.png` | 식 (2) p. 3 — 접촉 변형 닫음의 체적탄성률 K1 | 접촉 변형만으로 세운 체적탄성률 (작은 변형 · 유효 매질류).  카드 검산: 위 가정 + α = 1/2 + ln(φ/φ0) ≈ 1 − φ0/φ 로 인쇄 꼴이 정확히 나온다; φ → φ0 에서 Z0φ0/2π (≈ 0.50 — Z0 3.9 · φ0 0.81).  그림 4 의 회색 선은 Z0 = 3.91 · k = 5.08 · φ0 = 0.809 일 때의 이 식과 0.2 % 안에서 같다 (판독 맞춤) — 본문이 Z0 · φ0 를 적지 않아 이 역산이 이 PDF 에서 얻을 수 있는 유일한 값이다. |
| `eq_02b_small_strain_mismatch.png` | 본문 문단 p. 3 — ★ 작은 변형 (Hertz–Mindlin · 유효 매질) 닫음의 한계 문장 | ★ 이 논문의 '점접촉 한계' 문장.  작은 변형 틀 (Hertz–Mindlin 접촉 법칙 · 유효 매질 이론) 에서 나온 식들은 작은 변형에서만 'fair' 하고, φ → 1 로 가면 입자 집합이 변형할 수 없는 고체처럼 굴어 (K 발산) 어긋남이 커진다 → '국소 변형을 접촉 변형만으로 정의하는 것을 다시 생각해야 한다'.  우리 DEM (겹침 = 변형) 이 조밀 영역의 강성을 접촉 법칙만으로 못 따라가는 이유의 문헌 근거 (2D · 초탄성 한정 · DEM 을 직접 돌려 견준 것은 아니다 — 그 대조는 3D 판에 있다). |
| `eq_03a_single_particle_test_and_kp.png` | 본문 문단 p. 4 — 단일 입자 시험의 조건 · Kp 정의 · φp,0 = π/4 · 메시 문장 | 단일 입자 시험의 조건: 다입자 계와 같은 변형 증분 (ε_v ≡ ε_v,p) · Kp = (dPp/dφp)(dφp/dε_v,p) · ε_v,p = −ln(φp,0/φp) · φp,0 = π/4 (원 / 외접 정사각형).  '메시 해상도가 큰 영향을 주지 않는다' 는 문장의 자리 — 그림 5 판독으로는 φp 차 0.009–0.023 이고 968 요소가 가장 무른 쪽이다.  단일 입자 곡선이 다입자 곡선과 'roughly akin' 이라는 것이 척도화 (식 3 · 4) 의 출발 관찰이다. |
| `eq_03_k_single_particle_scaling.png` | 식 (3) p. 4 — K ≡ (Zφ/2π)Kp + O | 거시 체적탄성률 = 연결성 (Zφ/2π) × 단일 입자 체적탄성률 + O.  유도가 아니라 그림 4 의 관찰에서 '재해석' 한 척도화다.  판독으로는 우변 (찬 표식) 이 φ ≥ 0.95 에서 측정 K 의 0.45–0.75 배 — O 가 무시할 만하다는 것은 그림에서 확인되지 않는다 (본문은 O 가 d(Zφ) 꼴 미분 항이라고만 적는다). |
| `eq_04_p_single_particle_scaling.png` | 식 (4) p. 4 — P ≡ (Zφ/2π)Pp | 거시 압력 = 연결성 × 단일 입자 압력.  식 (1) 과 맞추면 σℓ ≡ Pp/2 라는 대응이다 (카드 풀이).  배율 Zφ/2π 는 jammed 에서 ≈ 0.50, 가장 조밀한 상태에서 ≈ 0.97 (Z0 3.9 · Z 6.2 · 카드 산술).  어느 후보든 '입자 하나의 압축 곡선 × 배위수' 로 다체 압력을 다시 써 볼 수 있다 — 단 소성 입자는 하중 이력이 남아 Pp 가 φp 만의 함수가 아니다. |
| `eq_05_single_particle_law.png` | 식 (5) p. 4 — 단일 입자 상자 법칙 | 단일 입자 상자 법칙 — 탄성 매질 속 공동 붕괴 (Carroll–Kim [52]) 유비의 로그 꼴.  φp,0 에서 유한한 기울기 Kp/E = b·φp,0/(φp,max − φp,0) ≈ 0.44 (b 0.12) – 0.55 (b 0.15) 를 갖는다 (카드 산술) — 2D 접촉이 거의 선형이라는 성질이고, 3D (Hertz 3/2 제곱) 에서는 이 꼴이 안 되어 3D 판이 √(φ − φ0) 인자를 넣었다 (형제 카드). |
| `eq_05b_b_value_cavity_analogy.png` | 본문 문단 p. 4 — b ≃ 0.12 · φp,max · 공동 붕괴 유비 | b ≃ 0.12 ('found to be') · φp,max = 'the maximal solid fraction attainable' (값 미기재 — 그림 5 의 선은 1.000 으로 읽힌다).  b 는 물성이 아니라 '정사각 상자 속 원판 하나 + neo-Hookean' 에 묶인 맞춤 상수다 — 같은 논문 그림의 선은 0.15, 형제 PRE 2020 판 본문은 0.14. |
| `eq_06_compaction_equation.png` | 식 (6) p. 4 — ★ 압밀 식 (원전) | ★ 압밀 식의 원전.  입력 = b (단일 입자 시험) · Z0 · φ0 (jammed 상태) · k · α (Z–φ 사상) · φmax (압밀 곡선에 맞춤).  저자가 든 성립 범위 = jammed 점부터 1 에 가까운 충전율까지 · 모든 마찰.  ⚠ 탄성 (가역) 원판의 식이다 — 소성 입자에 그대로 맞추지 않는다 (결론: 재료 모델이 바뀌면 로그가 아닌 꼴이 될 수 있다).  ⚠ 본문 상수 (b 0.12 · φmax 0.968) 는 그림의 선과 다르다 — 형식만 쓴다. |
| `eq_06b_phimax_fit_values.png` | 본문 문단 p. 4 — φmax 맞춤값 (0.998 · 0.968) 과 'outstanding' 문장 | 'Simple fitting of Eq. (6)' 으로 φmax = 0.998 (μ 0) · 0.968 (μ 0.8) — 초록의 'free from ad hoc parameters' 와 나란히 읽을 것 (압밀 곡선에 맞춘 값이 하나 있다).  0.968 은 같은 논문의 자료점 (μ 0.8 · P/E 0.5 에서 φ ≈ 0.973 · 판독) 보다 낮다; 그림 4 의 K2 선은 0.978 에서 발산하고, 그림 6 의 선은 0.981 까지 간다 (판독) — 오식으로 보이나 PDF 로 가릴 수 없다. |
| `eq_07_bulk_modulus_k2.png` | 식 (7) p. 4 — 체적탄성률 K2 (식 (6) 의 미분 · 고차항 버림) | 식 (6) 을 미분하고 로그가 붙은 항을 버린 체적탄성률 — φmax 에서 발산한다.  버린 항은 양수라 K2 는 식 (6) 의 정확한 미분보다 5–17 % 낮다 (φ 0.82–0.99 · 카드 산술).  jammed 에서 K2 ≈ 0.26E (b 0.12) – 0.33E (b 0.15) ↔ 측정 ≈ 0.3E ↔ K1 0.50E (카드 산술 + 판독).  φ 0.986 (μ 0) 에서는 측정 ≈ 21E ↔ 선 ≈ 11.7E (판독) — 본문 표현은 'perfectly reproducing'. |

**그림 · 본문의 잔결함 (원문)** — 인용 · 재사용 전에 볼 것:
- **b**: 본문 · 그림 5 범례 0.12 ↔ 그림 4 · 5 의 선 0.15 [판독].
- **φmax (μ 0.8)**: 본문 0.968 ↔ 자료점 0.973 ↔ 그림 4 의 선 0.978 ↔ 그림 6 의 선 0.981 [판독].
- **k**: 본문 ≃ 5.1 ↔ 그림 3 의 파선 5.20 [판독] (2 % · "≃" 안).
- **Z0 · φ0 · φp,max 의 값이 없다** · 그림 6 의 선은 본문 상수 (b 0.12) 의 식 (6) 과 최대 0.017 – 0.023 다르다 (b 0.15 로는 0.006 – 0.011) [카드 산술 + 판독].
- p. 3 "ε_v = 2ε_v,ℓ" 의 부호 (ε_v,ℓ = 2 ln(⟨ℓ⟩/d) 는 압축에서 음수) · 같은 쪽 끝 문장의 "σl" (다른 곳은 σℓ).
- p. 3 "in our **experiments**" (계산을 가리킴) · p. 2 "Kim and **Carrol**" · p. 5 "but **certainty** linked" · 그림 2 범례 "Zhang et al
  (**2014**)" ↔ ref [25] (2015).
- 그림 1 · 5 의 색 = "volumetric deformation / strain" 인데 재료는 "incompressible" · 색 눈금 없음.
- 참고문헌 표기 (인쇄 그대로 · 원 서지 [미확인]): [7] "Rev. Sci. Instrum. 88. 051807" · [21] "J. Mech. Phys. Solids 10-9, 142" ·
  [10] 쪽 번호 없음 · [42] "van Hecke J. Condens. Matter Phys." · [43] "T. C. Hasley".

---

## 7. Post-processing ★

| 무엇 | 어떻게 (본문) | 우리와의 대응 |
|---|---|---|
| 충전율 φ | "the ratio between the volume of the particles V_s over the volume of the container V" (p. 1) · 변형 뒤 입자 넓이를 다시 재는지 [미확인] (비압축이라 차이는 작다) | 우리 질량 기준 기공률과 같은 계열 |
| 압력 | 가한 압력 P (하중 단계) · 입상 응력 텐서의 주응력 평균 Pσ 와 "자명하게 같다" | 우리 DEM 의 Love–Weber 응력 · MPM 의 판 반력 (wallP) |
| 거시 변형 | ε_v = −ln(φ0/φ) | — |
| 체적탄성률 | K = (dP/dφ)(dφ/dε_v) = φ dP/dφ — 11 개 하중 수준에서 어떻게 미분했는지 [미확인] | 우리 Heckel 기울기와 같은 2차량 · 차분 방식에 민감 |
| 배위수 | Z = 2Nc/Np · Z − Z0 vs φ − φ0 (선형 · log–log) | 우리 DEM CN |
| 접촉 변형 | ε_v,ℓ = 2 ln(⟨ℓ^c⟩/d) (가지 길이의 평균) ↔ ε_v — 비 2 만 적고 그림은 없다 | 우리 DEM 겹침 δ/d (새 런 없이 계산 가능) |
| 단일 입자 | 상자 압축 φp(Pp/E) · 메시 6 종 · Kp | 우리에게 없는 단위 시험 (U1 로 등록 예정) |
| 압밀식 맞춤 | 식 (6) 의 φmax 를 "simple fitting" — 방법 · 구간 · 가중 [미확인] | 우리 Heckel = φmax 1 고정판 |
| 기존 모델 맞춤 | 넷을 마찰 0 자료에 "set to best fit" — 값 [미확인] | — |
| 통계 | 반복 · 오차막대 없음 | 우리 시드 반복 |
| ⛔ 없는 후처리 | 접촉력 분포 · 접촉 길이 · 입자 형상 지표 · 입자 안 응력 통계 · 방향별 응력 · 에너지 · 탈압 | — |

---

## 8. 우리 DEM + MPM 대비  →  `comparison_vs_ours_DEM.md` · `our_dem_baseline.md`

> ⚠ `litdb/our_dem_baseline.md` 는 정본 브랜치에서 값 없는 자리표시다.  아래 우리 숫자는 주 리포 `CLAUDE.md` 의 해당 절
> (E_SE 보정 · 3D MPM · SE-DUMP scaffold) 에서 가져왔다.

### 8-0. 나란히 표

| 축 | 이 논문 | 우리 DEM (D0) | 우리 MPM (지금) |
|---|---|---|---|
| 차원 · 기하 | **2D** 원판 · 벽 상자 · Np 1500 | 3D 구 · 주기 + 판 · 수만 | 3D 격자 (MLS-MPM) |
| 무른상 | **초탄성** neo-Hookean · 비압축 · E 미기재 | SE 구 · E_eff 1.35 GPa (실제 ~22–24 의 ~18× 연화) · ν 0.30 · 겹침 | **J2 소성** · E 1.53 GPa · ν 0.49 · σ_y 0.30 GPa |
| 강체상 | 없음 | NCM 구 (움직임) | 얼린 장애물 |
| 접촉 | 비관통 + Coulomb μ 0–0.8 · 겹침 0 | hooke/hysteresis 벌칙 | 격자 암묵 (붙음) |
| 하중 | **등방** · 응력 단계 (안정 판정 0.05 %) | 일축 판 · 300 MPa | 일축 판 (servo / hold) |
| 출발 | 침적 (닿지 않은 조밀 배치) → jammed | 느슨한 삽입 → 압축 | DEM 끝 상태 씨앗 |
| 해상도 | 원판당 삼각형 92 개 (968 까지 시험) | (해당 없음) | SE ⌀1 µm ≈ 7 셀/지름 (n_grid 384 · dx 0.141 µm) |
| 관측 | φ · Z · K · 단일 입자 | φ · CN · 접촉망 σ | φ · 형상 · 소성 변형 · 응력장 · 복셀 σ |
| 탈압 | 없음 | 진행 중 | 부분 |

### 8-1. 같은 점

- **무른상 비압축**: 이 논문 "incompressible" · 우리 MPM ν 0.49.  치밀화가 재료의 부피 감소가 아니라 **모양 바꿔 공극 채우기**로
  일어난다는 모델링 선택이 같다 (재료 값 정합이 아니라 방법 수준).
- **φ(P) 를 두 점근 (φ0 · φmax) 으로 읽는 형식**: 우리 압밀 곡선에도 그대로 쓸 수 있는 형식이다 (아직 이 형식으로 적합해 보지
  않았다 — §10-3 행동 4).
- **Z − Z0 ∝ (φ − φ0)^0.5**: 우리 DEM 은 Z 를 잴 수 있다 (새 런 없이 대조 가능 — 지수만, 계수는 2D 값이라 견주지 않는다).
- **"접촉 변형만으로는 조밀 영역의 강성을 못 준다"**: 우리 DEM 이 실제 영률로는 300 MPa 에서 실험 기공률에 못 가고 영률을 고쳐
  써야 하는 사정과 같은 방향의 문헌 진술 (§8-5 · 한정어 필수).

### 8-2. 다른 점 — 그리고 왜 (방법 인공물 vs 실제 차이)

| 차이 | 종류 | 설명 |
|---|---|---|
| 초탄성 vs 소성 | **구성식 차이 (실제)** | 이 논문 입자는 φ 0.985 (거시 체적 변형 0.20) 까지 탄성으로 버틴다.  분말 재료는 그 훨씬 전에 항복한다 → 같은 형상 변화가 훨씬 낮은 P/E 에서 일어난다 — P/E 축을 옮기지 않는 이유.  저자도 재료 모델이 바뀌면 식의 꼴이 달라질 수 있다고 적는다 |
| 2D vs 3D | **차원 (실제)** | φ0 ≈ 0.81 · k 5.1 · b · Zmax ≈ 6 은 2D 의 수.  3D 판에서는 φ0 0.50–0.51 (벽 상자) · 계수 8.5 · 닫음 (Hertz) 과 **식의 꼴**까지 바뀐다 (형제 카드) |
| 등방 vs 일축 | **경계조건** | μ 0 에서는 구별 없음 (저자) · 마찰이 있으면 다르다 — 일축 확장은 실험판이 다뤘다 |
| 강체 · 크기비 없음 | **범위 밖** | 우리 침대의 핵심 (AM 골격 · SE ≪ AM) 이 없다 — 혼합은 PRE 2020 판 |
| 재료 이력 | **없음** | 초탄성이라 재료의 이력이 없다 (마찰 접촉의 이력은 남을 수 있으나 탈압을 하지 않아 보이지 않는다) |
| 메시 92 요소 | **방법 인공물 (크기 추정 가능)** | 단일 입자 시험에서 968 요소보다 7 – 28 % 덜 눌린다 [판독 + 카드 산술] — 다입자 곡선에 같은 방향의 치우침이 있을 수 있다 (평가 없음) |

### 8-3. ★ 원전 ↔ 후속판 한 표 (같은 그룹 · 같은 틀)

| 양 | **이 PRL (2D 원판)** | PRE 2020 (2D 혼합) | Soft Matter 2022 (3D 구) | 출처 (후속판 값) |
|---|---|---|---|---|
| 입자 | 무른 원판 1500 | 강체 + 무른 원판 1500 (무른 비율 κ 0.2 – 1) | 무른 구 50 · 100 | `cardenasbarrantes2020_…` §3-1 · `cardenasbarrantes2022_soft_spheres_…` §3-1 |
| 입자당 요소 | 삼각형 92 | 삼각형 92 | 사면체 808 | 〃 |
| 재료 | neo-Hookean "incompressible" | neo-Hookean · ν 0.495 | "elastic" · ν 0.495 | 〃 |
| 마찰 | 0 – 0.8 (다섯) | 혼합 0 · 0.2 / κ 1 은 0 – 0.8 | 0.3 하나 | 〃 |
| 안정 판정 | φ 변화 < **0.05 %** | < 0.01 % | (속도 제어 · jammed 판정 < 0.01 %) | 〃 |
| 하중 범위 | P/E 10⁻⁴ – 0.5 [판독] | P/E 10⁻⁵ – 0.5 | P/E\* 2 × 10⁻⁴ – 0.7 [판독] | 〃 |
| Z − Z0 법칙 | k ≃ **5.1** · α ≃ 0.5 (그림 선 5.20) | ξ ∼ 5.1 · α ∼ 0.5 | ψ ≈ 8.5 · 1/2 (그림 선 ≈ 9.0) | `…2020…` §3-2 · `…3d…` §3-2 · §3-3 |
| 국소–거시 변형 | ε_v = 2ε_v,ℓ (선형 접촉 변형 기준 Γ = 4) | 같음 | Γ ∼ 4.4 | 〃 |
| 큰 변형 닫음 | **단일 입자 상자 법칙** (식 5) | 같음 (식 9) | 연속 조건 + Hertz (단일 입자 상자 시험 없음) | `…2020…` §4-5 · `…3d…` §8-3 |
| **b** | 본문 **≃ 0.12** · 그림 선 0.15 [판독] | 본문 ≃ **0.14** | (해당 없음) | `…2020…` §3-2 |
| **φmax** (무른 입자만) | 본문 0.998 (μ 0) · 0.968 (μ 0.8) · 그림 선 0.998 / 0.978 – 0.982 [판독] | 식 (12) 적합 0.994 (μ 0) · 0.982 (μ 0.2) [그 카드 판독] · Secondi 적합 0.97 · 0.96 | 0.95 (모델) · 0.965 (Heckel–Secondi) | `…2020…` §3-2 · §3-3 · `…3d…` §3-2 |
| jammed φ0 · Z0 | 본문 미기재 · φ0 0.808 – 0.795 [판독] · Z0 ≈ 3.9 (μ 0 · 역산) | 학회판 Table 1: κ 1 에서 φ0 0.807 (μ 0) · 0.805 (μ 0.2) · Z0 3.4 · 3.5 | φ0 0.50 · 0.51 · Z0 ≃ 3.5 ("size effects") | `cardenasbarrantes2021_…` §3-1 · `…3d…` §3-2 |
| "매개변수" 에 대한 말 | 초록 "free from ad hoc parameters" · 본문 φmax 맞춤 | φmax 하나만 거시 적합 | "only one parameter, the maximum packing fraction φmax, is unknown" | 〃 |
| DEM 과의 직접 대조 | **없음** (K1 로 간접) | 없음 (Voigt K1) | 있음 (YADE Hertz DEM) | `…3d…` §5-1 |

⇒ 원전과 후속판 사이에 **같은 양의 값이 조금씩 다르다** (b 0.12 ↔ 0.14 · φmax 0.998 ↔ 0.994 · μ 0.2 의 φ0 0.800 [이 카드 판독] ↔ 0.805
[학회판 표] · Z0 3.9 [역산] ↔ 3.4 [학회판 표]).  같은 계산을 다시 쓴 것인지 새로 돌린 것인지는 어느 PDF 에도 적혀 있지 않다
[미확인] — **상수를 어느 한 판에서 뽑아 "그 그룹의 값" 으로 쓰지 않는다.**

### 8-4. 압밀 식 계열을 우리 Heckel 과 나란히 놓으면

| 식 | 꼴 | 점근 | 맞춘 값 |
|---|---|---|---|
| Heckel (우리 DEM 적합) | ln[1/(1 − D)] = K·P + A | φmax = 1 고정 · 출발값은 A 가 흡수 | 2 (K · A) |
| Heckel–Secondi · Platzer (형제 카드) | P = −A ln[(φmax − φ)/(φmax − φ0)] | φ0 · φmax | 2 (A · φmax) |
| **이 PRL 식 (6)** | P = −(bEφ/2π)·Z(φ)·ln[(φmax − φ)/(φmax − φ0)] | φ0 · φmax | φmax (+ b · k 는 보조 자료) |

- 식 (6) = Heckel–Secondi 의 상수 A 를 **A(φ) = bEφZ(φ)/2π** 로 바꾼 것 [카드 풀이].  jammed 에서 A ≈ 0.12·0.81·3.9/2π·E = **0.06E**,
  가장 조밀한 곳에서 0.12·0.985·6.2/2π·E = **0.12E** (b 0.12 기준) — 형제 카드의 Secondi 적합 A 0.05E (μ 0) · 0.079E (μ 0.8) 와 같은
  자릿수 (아래 끝 근처) 다.  ⇒ 이 식이 Heckel 류와 다른 점은 "상수가 배위수를 따라 두 배쯤 변한다" 를 넣은 것이다.
- 우리 쪽 함의: 우리 압밀 곡선을 다시 적합한다면 **φ0 와 φmax 를 둘 다 남긴 꼴**이 먼저다 (형제 카드의 권고와 같음).

### 8-5. ★ 우리 DEM 이 도는 자리를 이 논문의 그림 4 에 놓으면 (유비 · 산술 — 논문 주장 아님)

- 이 논문에서 "접촉 변형 닫음" K1 이 맞는 구간과 틀리는 구간 [판독 + 카드 산술]: P/E ≈ 0.025 (φ ≈ 0.86) 근처에서 측정과 만나고,
  그 아래에서는 과대 (최대 2 배), 그 위에서는 과소 (P/E 0.25 에서 1/4.4 · 0.5 에서 1/16).
- [카드 산술] 300 MPa ÷ E: 실제 SE (E 22–24 GPa) → **0.013** (φ ≈ 0.85 · K1 이 ≈ 1.4 배 과대인 구간) · 우리 DEM 연화 영률 (1.35 GPa) →
  **0.22** (φ ≈ 0.96 · K1 이 1/4 쯤으로 과소인 구간).
- 읽는 법: 접촉 변형 닫음의 강성 오차는 **부호가 바뀐다** — 한쪽 끝에서 과대, 다른 끝에서 과소.  그러므로 영률을 한 배수로
  고쳐서는 전 구간을 맞출 수 없고, 한 압력 (우리는 300 MPa) 에 맞춘 연화 영률은 **그 압력의 대리**일 뿐 다른 압력 · 탈압으로
  옮겨 가지 않는다 [카드 추론].
- ⚠ 한정: 이 논문은 2D · 초탄성 · 등방 · K1 은 DEM 계산이 아니라 해석 닫음 · 우리 접촉은 Hertz 가 아니라 hooke/hysteresis · 우리
  치밀화의 주 기전은 탄성 변형이 아니라 소성 · 재배열 · 복합 침대에서는 AM 골격이 하중을 가린다.  **수치 대응이 아니라 방향의
  해석**이다.  같은 유비의 3D 판 (Hertz DEM 을 실제로 겹쳐 그린 그림) 은 `cardenasbarrantes2022_soft_spheres_3d_compaction_nscd` §8-5.

### 8-6. frame 규율 재확인

- **frame[4]**: 이 논문의 식 (6) 은 **같은 시뮬레이션 안에서** 잰 Z0 · φ0 와 맞춘 b · k · φmax 로 닫힌다 — 실험 앵커가 없다 (실험 대조는
  2022 실험판).  우리는 각 후보를 **실험** 에 따로 보정하고, 이 논문의 P ≡ (Zφ/2π)Pp · Z(φ) · K(φ) **형식**은 비교 축으로만 쓴다.
- **frame[5]**: 접촉 (입자 경계) 과 형상 변화를 한 이산화에 담은 2D 실물이다.  우리 분업 (DEM = 패킹 · 수송, MPM = 소성 형상) 을
  반박하지 않는다 — 한 이산화에 담으면 2D 1500 입자 · 탄성 · 비용 미기재라는 범위가 된다는 것을 보여 준다.

---

## 9. 깊은 통찰 (deep insights)

1. **압밀 법칙 = (연결성) × (입자 하나의 벌크 응답).**  식 (4) `P ≡ (Zφ/2π)Pp` 가 이 계열의 뼈대이고, 로그 꼴은 **단일 입자 응답**
   에서, √ 꼴은 **배위수**에서 온다.  재료가 바뀌면 바꿔 끼울 것은 Pp(φp) 하나다 — 그래서 저자는 소성이면 "로그가 아닌 꼴" 이
   될 수 있다고 적는다.  우리 쪽: 단위 시험 U1 (입자 하나 압축) 은 해상도 검사일 뿐 아니라 **그 모델의 국소 법칙을 재는 시험**이다.
2. **접촉 변형 닫음의 오차는 부호가 바뀐다.**  K1 은 jammed 에서 1.8 배 과대, 조밀 영역에서 16 배까지 과소 [판독 + 카드 산술].
   과대 쪽 원인 = 균질 변형 가정이 재배열을 못 봄, 과소 쪽 원인 = 접촉 변형에는 "입자가 더 못 눌린다" 는 정보가 없음 (풀이는 카드
   해석).  ⇒ 점접촉 틀에 필요한 보정은 상수 배수가 아니라 **밀도에 따라 커지는 강성** (다접촉 · 벌크 응답) 이다.
3. **"매개변수 없음" 은 세어 봐야 한다.**  거시 곡선에 맞춘 φmax + 보조 자료에 맞춘 b · k.  게다가 b 는 본문 0.12 · 그림 0.15 ·
   후속판 0.14 로 움직이고 단일 입자 자료 자체가 압력에 따라 0.11 – 0.22 를 요구한다 [카드 산술].  ⇒ b 는 상수라기보다 **로그 꼴이
   자료를 얼마나 못 따라가는지의 표지**다.
4. **단일 입자 법칙의 유한한 초기 기울기는 2D 의 성질이다.**  식 (5) 는 φp,0 에서 Kp ≈ 0.44 – 0.55E 로 바로 선다 [카드 산술] — 원판
   접촉은 힘이 접근량에 거의 비례하기 때문이다.  3D 구는 Hertz (힘 ∝ δ^(3/2)) 라 초기 기울기가 0 이고, 그래서 3D 판은 같은 꼴을
   못 쓰고 √(φ − φ0) 인자를 넣었다 (형제 카드 §5-4).  ⇒ **2D 로 세운 압밀 식을 3D 에 옮기지 말라**는 근거가 원전의 식 안에 이미
   들어 있다.  (소성 접촉은 3D 에서도 힘이 접근량에 거의 비례하므로 다시 다른 꼴이 될 것이다 — 카드 추론 · 논문 밖.)
5. **k 는 보편 상수가 아니라 양 끝의 함수다.**  k = (Zmax − Z0)/(φmax − φ0)^α 이고 2D 에서 Zmax ≈ 6 (면을 채운 다각형) 이므로
   k ≈ (6 − Z0)/√(φmax − φ0) [카드 추론].  Z0 (준비 · 마찰) 나 φ0 가 달라지면 k 도 달라진다 — "마찰 무관" 은 이 시료들의 Z0 · φ0 가
   비슷했다는 뜻으로 읽는 것이 안전하다.
6. **해상도 검사를 "큰 영향 없음" 으로 닫지 말 것.**  92 ↔ 968 요소의 차는 치밀화량으로 7 – 28 % 이고 방향이 일정하다 (거칠수록
   뻣뻣).  같은 메시라도 하중 방식에 따라 0.023 이 갈린다.  이 차는 b 의 0.12 ↔ 0.15 차와 같은 크기다 — 상수의 흔들림이 해상도에서
   올 수 있다.
7. **마찰은 출발 상태를 바꾼다.**  마찰이 곡선에 주는 효과는 φ0 · φmax 의 평행 이동 (0.012 – 0.013) 이고 Z–φ 법칙 · 작은 변형의 K 는
   거의 그대로다.  ⇒ 후보 모델을 견줄 때 **출발 패킹 (φ0 · Z0) 을 먼저 맞추거나 기록**하지 않으면 접촉 표현의 차이와 섞인다.

---

## 10. [DEM 우선 (수영)] 트랙 — 후보별 함의 + 구체 행동

### 10-1. 후보별 판정

| 후보 | 이 논문이 지지 / 불리 | 이유 |
|---|---|---|
| **D0** (지금의 DEM · 연화 영률) | **한계의 2D 근거 (간접)** | 접촉 변형만으로 세운 닫음이 jammed 에서 과대 · 조밀 영역에서 과소 (그림 4).  DEM 을 직접 돌린 대조는 아니다 — 그 그림은 3D 판에 있다 |
| **B** (입자별 FE + 접촉) | **2D 실례 = 이 논문 · 원판 1500 개** | 형상 변화 · 입자 경계 · 마찰을 한 번에 풀지만 2D · 탄성뿐 · 비용 미기재 · 메시 92 요소가 덜 수렴 |
| **A′** (MPM · 입자별 속도장) | **기준 문제를 준다 (2D)** | 원판 · 마찰 없는 벽 · μ 0 – 0.8 · 비압축 초탄성의 φ(P/E) (표 3-3 (a)) 와 단일 입자 φp(Pp/E) (표 3-3 (e)) = 2D 코드 검증용 (보정 아님 · 판독값) — 계획 단계 3 (2D 에서 접촉 표현만 바꿔 견주는 시험) 의 외부 대조로 쓸 수 있다 |
| **C** (큰 변형 접촉 법칙 DEM) | **시험대를 준다** | K(φ) 의 발산을 접촉 법칙이 내는지 — 그림 4 의 측정 K 가 견줄 대상 (2D · 탄성 한정) |
| **C′** (항복 캡 탄소성 접촉 DEM) | 중립 | 항복이 없는 계 |
| **A** (MPM · 강체 AM + 단일 속도장) | 중립 | 강체가 없는 계 · Z · σℓ 는 단일 속도장에서 정의되지 않는다 |
| **M0** (균질화 압밀 모델) | **형식 한 줄** | 두 점근 (φ0 · φmax) 을 남긴 로그 꼴 + 밀도에 따라 변하는 계수 A(φ) ∝ φZ(φ) (§8-4) |

### 10-2. 계획의 자리 (단계 · 단위 시험 · 조건)

| 자리 | 이 논문에서 가져올 것 |
|---|---|
| **U1** (입자 하나 압축과 해상도) | 그림 5 의 형식 — 입자 하나를 강체 벽 상자에서 다입자 계와 같은 변형 증분으로 누름 · 해상도 여러 수준 · 하중 방식 둘.  ⚠ 이 논문이 안 한 것을 넣는다: 해상도 차의 **수치 기준** ("큰 영향 없음" 이 아니라 치밀화량의 % ) · 해석해 대조 · 소성 재료의 기준 해 |
| **U6** (작은 조밀 충전 압축의 해상도 수렴) | 다입자 계에서는 해상도 시험을 하지 않았다 (단일 입자로 대신) — 우리는 다입자에서도 본다 |
| **단계 0** (기공률을 세는 연산자 · 판정 기준) | φ = 입자 부피 / 용기 부피 · 안정 판정 0.05 % 라는 기록 형식.  출발 상태 (φ0 · Z0) 를 결과 전에 적는다 (이 논문은 값을 안 적어 식을 다시 계산할 수 없다 — 반면교사) |
| **단계 3** (2D 접촉 표현 비교) | 2D 외부 대조 자료 (판독값 ±0.002) · 마찰 0 – 0.8 |
| **단계 4 · 5** (3D) | 해당 없음 — 2D 값을 3D 로 옮기지 않는다 (§9-4) |
| **단계 6** (탈압) | 해당 없음 — 탈압을 계산하지 않았다 |
| **조건 R3** (SE 입자 경계 기억) · **R6** (SE 형상 변형) | 둘 다 만족하는 2D 계산의 실례 (단 탄성) |
| **조건 R4** (탈압) · **R1** (AM 하중 분담) · **R7** (AM 파괴) | 다루지 않음 |
| **조건 R5** (맞추는 값은 모델마다 하나) | 이 식도 "거시 곡선에 맞춘 값은 φmax 하나" — 단 b · k 를 같은 계산의 보조 자료에서 정한다 (예측이 아니라 재서술에 가깝다) |
| **결과 전 대조 항목** | 값은 없음 (2D · 탄성 · 무차원).  형식만: 배위수 지수 0.5 · K(φ) 가 포화 근처에서 발산하는지 · 단일 입자 곡선 × 배위수로 다체 압력이 다시 써지는지 |

### 10-3. 구체 행동 (비용 낮은 것부터)

1. **[보고 · 원고 문장]** "국소 변형을 접촉 변형만으로 정의하는 닫음 (Hertz–Mindlin · 유효 매질) 은 조밀 영역에서 어긋난다" 의 근거로
   p. 3 문장과 그림 4 를 인용한다 (§11 · 한정어 = 2D · 초탄성 원판 · 등방 · 해석 닫음).  DEM 을 직접 겹친 그림은 3D 판을 함께 인용.
2. **[D0 · 새 런 0]** 기존 LIGGGHTS 압축 궤적에서 (a) Z − Z0 vs φ − φ0 의 지수 · 계수 (b) K(φ) = φ dP/dφ 를 잰다.  K 가 포화 근처에서
   오르는지 · 접촉 법칙이 그 오름을 내는지가 정보다 (2D 값 k 5.1 은 기대값으로 쓰지 않는다).
3. **[U1 등록]** 재설계 MPM 의 단일 입자 상자 시험을 결과 전에 적는다: 해상도 수준 · 하중 방식 · 통과 기준 (치밀화량 차의 % 와
   단조 수렴).  이 논문의 92 ↔ 968 요소 차 (7 – 28 %) 와 "하중 방식에 따라 0.023" 을 참고값으로 적어 둔다.
4. **[M0 · 새 런 0]** 우리 순수 SE φ(P) 를 `P = −A(φ) ln[(φmax − φ)/(φmax − φ0)]` 꼴 (φ0 · φmax 를 남김) 로 다시 적합해 Heckel
   (φmax 1 고정) 과 견준다 — 형제 카드의 권고와 같은 일이므로 한 번에 한다.
5. **[식 (6) 을 쓰려면]** 형식만 쓴다.  b · k · φmax · Z0 · φ0 는 **견주려는 모델 자신의** 단일 입자 시험 · Z–φ · 압밀 곡선에서 정한다.
6. **⛔ 하지 말 것**: P/E 값을 300 MPa 로 환산해 LPSCl 기공률을 읽기 · φ0 0.81 · k 5.1 · b 0.12 · φmax 0.998 을 3D 나 우리 재료의 수로
   옮기기 · "parameter-free 압밀 법칙" 으로 인용하기 · 본문 상수로 식 (6) 을 다시 그려 그림 6 과 견주기 (재현되지 않는다) · 탈압 ·
   소성의 근거로 쓰기.

---

## 11. 인용 가능 문장 (deck · paper 용 — 원문 그대로, 쪽 표기)

- (p. 1, 초록) *"The compaction behavior of deformable grain assemblies beyond jamming remains bewildering, and existing models that seek to
  find the relationship between the confining pressure P and solid fraction φ end up settling for empirical strategies or fitting
  parameters."*
- (p. 1, 서론 — **강체 · 작은 변형 가정**) *"Such body distortions are often dismissed or simplified by considering either the rigid body
  kinematics as the primary source of deformation or standing on the small-strain framework. However, explicitly describing the
  particles' large strains is essential for the development of technological applications…"*
- (p. 1 — **Heckel 상수**) *"Although this model yields fair predictions, it relies upon two constants (K and B) not clearly related to
  physical or mechanical properties."*
- (p. 1 — **기존 모델의 한계**) *"We can summarize the limitations of current models by the use of nonphysical parameters, the lack of
  accuracy at extreme pressures, and the missing physical derivation of the compaction equations."*
- (p. 1) *"…such a venture should admittedly rely on a proper description of the compaction process while taking into account the
  multicontact nature of the assembly and the particles' deformability."*
- (p. 2 — **접촉 정칙화**) *"Note that the NSCD approach does not introduce regularization coefficients for the contact laws as other
  discrete element approaches do, making this numerical scheme robust and stable."*
- (p. 3) *"Keeping in mind the discrete nature of these assemblies, an adequate compaction model should rely on the physical phenomena
  taking place at the particles and contacts scales."*
- (p. 3 — **★ 접촉 변형 닫음의 한계**) *"As also noted in previous studies, fair predictions of bulk modulus result for the small-strain
  domain when standing on the equivalent medium approach. Yet, we observe an increasing mismatch as the solid fraction tends to unity
  since the assembly of grains starts to behave as a nondeformable solid (i.e., the corresponding bulk modulus diverges). This
  observation suggests that defining local strains only by means of the contact deflections (i.e., σl = Eεv,ℓ) should be reconsidered."*
- (p. 4 — **단일 입자 = 대표 척도**) *"Equations (3) and (4) reveal that the elastic and compaction properties of a deformable particle
  assembly are scalable from the behavior of an individual particle. More precisely, a description of a single-particle compression
  should be a central ingredient for the description of the behavior of the assembly."*
- (p. 4 — **φmax 는 맞춤**) *"Simple fitting of Eq. (6) reveals that φmax = 0.998 for the frictionless case, while φmax = 0.968 for
  μ = 0.8."*
- (p. 5 — **소성이면 꼴이 바뀔 수 있다**) *"Indeed, this approach could be generalized to different material models (elastic, hyperelastic,
  plastic, etc.) or to other loading configurations such as the oedometric compression test. These alternative mechanical
  considerations may lead to distinct functional forms, other than logarithmic, but certainty linked to the behavior of individual
  particles."*

⚠ 인용 때 붙일 한정어: **2D · 초탄성 (가역) 원판 · 등방 · 원판 1500 개 벽 상자 · 실험 대조 없음** — "DEM 일반" 이나 "소성 분말" 의
결론으로 쓰지 않는다.  p. 3 의 한계 문장은 **해석 닫음 (K1)** 에 대한 것이지 DEM 계산 결과에 대한 것이 아니다.  저자는 한계의
**수치 문턱**을 적지 않았다 (배수 1.8 · 1/4.4 · 1/16 은 카드 판독 + 산술).

---

## 12. 주의 / 한계 / PDF 가 말하지 않는 것

### 12-A. 우리에게 옮길 때의 한계

- **2D · 평면변형률** — φ0 · Zmax · k · b · 식의 꼴이 차원에 묶였다 (3D 판에서 바뀐다).
- **초탄성 (가역)** — 소성 잔류 · 탈압 뒤 기공 유지 · 가공 경화 · 재료의 소성 이력이 없다.  우리 공정 (냉간 가압 뒤 탈압) 의 핵심이
  범위 밖.
- **P/E 무차원 · E 미기재** — 300 MPa 로 옮길 축이 없다.
- **무른 원판만** — 강체 · 크기비 · 점착 · 파쇄 없음.  **등방** — 다이 (일축) 아님.
- **하중 쪽만** — 탈압 없음.
- **실험 대조 없음** · 시료 반복 · 오차막대 없음.

### 12-B. ★ 이 논문 자체의 약점 · 불일치 (비판적으로)

1. **"free from ad hoc parameters" (초록 · 결론) vs "Simple fitting of Eq. (6) reveals that φmax = …" (p. 4)** — 거시 곡선에 맞춘 값이
   하나 있고, b · k 도 같은 계산의 보조 자료에 맞춘 값이다 (§4-5 표).
2. **b: 본문 · 범례 0.12 ↔ 그림의 선 0.15** [판독 · §3-3 (c)].  그림 5 의 파선과 그림 4 의 K2 선 둘이 독립적으로 0.147 – 0.150 을 준다.
3. **φmax (μ 0.8): 본문 0.968 ↔ 자료점 0.973 ↔ 그림 4 의 선 0.978 ↔ 그림 6 의 선 0.981** [판독].  본문 값은 같은 논문의 자료점
   (그림 2 · 6 의 P/E 0.5 · 그림 4 의 φ 0.974 – 0.978) 보다 낮아 식 (6) 에 넣으면 그 자료에 닿을 수 없다 — 오식으로 보이나 PDF 로
   가릴 수 없다.
4. **그림 6 의 "모델" 선이 본문 상수의 식 (6) 이 아니다** [카드 산술 + 판독 · §3-3 (b)].  b 0.12 로는 선과 최대 0.017 (μ 0) ·
   0.023 (μ 0.8) 어긋나고, 그림 4 · 5 의 선이 쓰는 b 0.15 로는 최대 0.006 · 0.011 (선 굵기의 두세 배) 까지 붙지만 판독 잡음 안으로는
   들어오지 않는다.  같은 논문의 그림 4 · 5 의 선은 해당 식에 0.2 % 안에서 맞으므로 판독 문제가 아니다.  "식이 자료를 예측한다" 는
   주장의 계수 수준 검증은 이 PDF 만으로는 따라갈 수 없다.
5. **식의 입력 Z0 · φ0 · φp,max 가 인쇄되지 않았다** — 식 (2) · (6) · (7) 을 글만으로 계산할 수 없다.
6. **식 (3) · (4) 는 유도가 아니라 "재해석"** 이고 근거는 그림 4 의 사후 일치다 (저자: "supports, a posteriori, the validity of our
   analysis").  판독으로는 찬 표식이 빈 표식의 0.45 – 1.35 배 — "O negligible" 은 조밀 영역에서 성립하지 않는다.
7. **"perfectly reproducing" (K2)** — 마찰 0 에서 K2 ÷ 측정 = 1.15 – 1.35 (φ ≤ 0.84) · 0.74 – 0.81 (0.86 – 0.97) · 0.56 (0.986) [판독 ±10 %].
8. **메시 "no major effect"** — φp 차 0.009 – 0.023 · 가장 고운 메시가 가장 무른 쪽 · 다입자 계산에 쓴 92 요소는 치밀화량이 7 – 28 %
   적다 [판독 + 카드 산술].  다입자 계에서의 메시 시험은 없다.  같은 메시 · 다른 하중 방식의 차 0.023 은 언급이 없다.
9. **식 (5) → (6) 의 사상** — "φ can be mapped to φp (since ε_v ≡ ε_p,v)" 를 엄밀히 하면 φmax = (4φ0/π)φp,max > 1 이 된다 [카드 산술].
   실제로 한 일은 기호 바꿔 넣기 + φmax 맞춤이다.
10. **단일 입자 법칙이 자료를 한 b 로 못 따라간다** — 파선은 Pp/E 0.01 – 0.1 에서 0 – 0.02 낮고 0.25 위에서 높다 [판독]; 자료가
    요구하는 b 는 0.11 – 0.22 [카드 산술].
11. **검증이 닫힌 고리다** — 식의 상수를 정한 계산과 식을 검증한 계산이 같다.  실험 · 다른 코드 · 다른 시료와의 대조가 없다 (실험은
    2022 판에서).  시료가 마찰마다 하나인지도 적혀 있지 않다.
12. **계산 비용이 없다** — 시간 · 코어 · 반복 수 · 시간 간격이 하나도 없어 재현 · 비용 추정이 안 된다.
13. 표기 잔결함: ε_v,ℓ 의 부호 · "experiments" · "Carrol" · "certainty" · 범례 연도 · "비압축" 인데 색 = 체적 변형 · 참고문헌 표기
    (그림별 절 끝).

### 12-C. [미확인] 목록 (PDF 에 없음)

**보충 자료 (Supplemental Material) — 미수령 · 존재 여부 미확인** · φ0 · Z0 의 값 (마찰별) · φp,max 의 값 · 그림 6 의 선에 넣은 상수 ·
기존 모델 넷의 맞춤값 · 식 (6) 맞춤의 방법 · 구간 · 계산 시간 · 코어 수 · 병렬 여부 · 메모리 · E · ρ · d 의 절대값 · ν · 크기 분포의
범위 · 꼴 · 요소 차수 · Δt · 반복 수 · 허용오차 · 벽 속도 · 관성수 · 수치 감쇠 · 접촉 탐색 · 상자 모양 · 종횡비 · 시료 수 · 반복 ·
rattler 처리 · 벽 접촉의 Z 산입 · K 의 수치 미분 방식 · 변형 뒤 φ 를 재는 법 · 단일 입자 시험의 벽 마찰 · 92 요소의 φp 시작값이 π/4
보다 높은 이유 · 본문 0.968 과 그림의 차이의 원인 · 자금 · 탈압 거동 · 이 PRL 과 PRE 2020 판 (κ = 1) 이 같은 계산인지.

---

## 13. 기법 미니 용어집 (이 카드 안에서만)

| 용어 | 뜻 |
|---|---|
| **NSCD** (non-smooth contact dynamics) | 접촉 동역학 (CD) 을 유한요소 변형체로 확장한 것.  접촉을 벌칙 강성으로 정칙화하지 않고 비관통 + 건조 마찰 조건으로 풀며 접촉 매개변수는 μ 하나 |
| **LMGC90** | Montpellier 의 오픈소스 접촉 동역학 플랫폼 |
| **neo-Hookean (비압축 · 평면변형률)** | 큰 변형에서도 탄성 (가역) 인 고무류 구성식 — 이 논문의 원판 재료 |
| **φ0 · Z0** | P/E → 0 (강체 집합의 jammed 상태) 의 충전율 · 배위수 (값 미기재 · 판독 φ0 0.808 – 0.795 · 역산 Z0 ≈ 3.9) |
| **φmax** | 압력이 무한대로 갈 때의 점근 충전율 — 식 (6) 을 자료에 맞춰 얻는 양 |
| **k · α** | Z − Z0 = k(φ − φ0)^α 의 계수 · 지수 (5.1 · 0.5, 2D).  후속판은 k 를 ξ (2D 혼합) · ψ (3D) 로 쓴다 |
| **σℓ** | 평균 접촉 응력 ⟨f^c⟩⟨ℓ^c⟩/d² |
| **ε_v · ε_v,ℓ** | 거시 체적 변형 −ln(φ0/φ) · 접촉 (가지 길이) 에서 셈한 국소 체적 변형 2 ln(⟨ℓ^c⟩/d).  이 계에서 ε_v = 2ε_v,ℓ (크기) |
| **K1 · K2** | 체적탄성률의 두 식 — K1 (식 2) = 접촉 변형 닫음 · K2 (식 7) = 식 (6) 의 미분 (고차항 버림) |
| **단일 입자 상자 시험** | 네 강체 벽 사이의 원판 하나를 다입자 계와 같은 변형 증분으로 누르는 시험.  φp · Pp · Kp · φp,0 = π/4 |
| **b** | 단일 입자 법칙 (식 5) 의 비례 상수 (본문 0.12 · 그림의 선 0.15 · 후속판 본문 0.14) |
| **O** | 식 (3) 의 "고차항" — 본문은 무시할 만하다고 하나 그림 4 에서는 조밀 영역에서 측정의 절반까지 |
| **Voronoi 칸 변형 ε_c,ℓ** | 입자를 감싼 Voronoi 칸의 부피 변화로 정의한 국소 변형 −ln(V_ℓ/V_ℓ,0) — 접촉 변형의 대안 |

---

## 14. 관련 카드 (중복 서술 금지 — 겹치면 넘김)

- **같은 그룹 · 이 식을 이어 쓴 판**: `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` (2D 강체 + 무른 혼합 · φmax(κ) ·
  b 0.14) · `cardenasbarrantes2021_soft_rigid_mix_compaction_proceedings` (그 학회 단편 · φ0 · Z0 표) ·
  `cardenasbarrantes2022_soft_spheres_3d_compaction_nscd` (3D · Hertz DEM 대조 · 식의 꼴이 바뀜) ·
  `cardenasbarrantes2022_soft_hard_grains_compaction_experiment_dic` (2D 실험 · 일축 확장).  오각형 판 (PRE 103, 062902) 은 카드가
  들어오면 여기에 slug 를 더한다.
- **★ 형제 카드가 이 PRL 을 가리켜 적은 곳과 원문의 차이** (형제 카드는 고치지 않았다 — 읽을 때 참고):
  `cardenasbarrantes2022_soft_spheres_3d_compaction_nscd` §8-3 표의 "단일 입자 상자 법칙 (b ≃ 0.14 · PRL/PRE 2020)" — **PRL 의 인쇄값은
  0.12** 다 (0.14 는 PRE 2020 판) · 같은 표의 2D "φmax 0.96 – 0.99" — PRL 인쇄값 0.998 (μ 0) 은 그 범위 밖 · 같은 표의 2D "Z0 3.3 – 3.7"
  (학회판 표) — PRL 그림에서 역산한 값은 ≈ 3.9 (μ 0).  나머지 (선형 접촉 변형 기준 Γ = 4 · k 5.1 · K1 의 꼴) 는 원문과 맞는다.
- **같은 문제의 다른 방법 (이 논문이 인용)**: ref [16] Nezamabadi 외 2019 와 같은 저자 무리의 후속 =
  `nezamabadi2022_mpm_cd_plastic_particle_compaction` (입자별 격자 MPM + CD · 2D · **소성** 입자 — 그 카드가 ref [16] 의 문헌을
  자기 방법 계보로 적는다) · `nguyen2017_mpm_bpm_deformable_particle_compaction` (같은 계열의 MPM vs BPM).
- **후보 B (MPFEM) 형제 · 3D 비용**: `demirtas2021_mpfem_hollow_sphere_die_compaction` · `pycompact2025_dem_mpfem_workflow` ·
  `zunker2025_dem_large_deformation_compaction`.
- **점접촉의 한계 · 보정**: `giannis2021_stress_based_multicontact_dem` · `zunker2024_mdr_contact_model_partI` ·
  `zunker2024_bulk_elastic_partII` · `gonzalez2012_nonlocal_contact_confined_granular`.
- **우리 소재 Heckel 실측**: `lee2025_heckel_argyrodite_powder_densification_nanoindentation`.

---

## 🗨️ Q&A 로그

- (2026-11-10 digest — 아직 질문 없음)
