<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. WISHLIST Tier-2 #16 (DMT). -->
# Effect of Contact Deformations on the Adhesion of Particles (DMT 이론) — Derjaguin, Muller, Toporov (J. Colloid Interface Sci. 1975)

> slug `dmt1975_adhesion_contact_deformation` · DOI `10.1016/0021-9797(75)90018-1` · type `continuum (점착 접촉역학 이론)` · PDF `DMT_DerjaguinMullerToporov_1975_JCIS_ContactDeformations_AdhesionParticles.pdf` · digested `2026-06-26` · status ✅

> ★★ **이 논문 = DMT 점착 이론의 원전.** 탄성 구–평면 점착에서 **van der Waals 인력이 접촉면 *바깥*의
> 고리(ring) 영역에서 작용**한다고 보고, pull-off(떼어내는) 힘 **F = 2πRγ**를 유도한다(JKR의 1.5πRΓ와 짝).
> ★ **우리 SE 입자는 작고(0.5 µm) 비교적 단단 → JKR이 아니라 DMT 체제** = 우리 SE-SE cohesion의 물리적
> 극한. F=2πRγ ↔ 우리 LIGGGHTS `coefficientAdhesionStiffness`(k_c=1e6) / MPM `--coh`(backlog A3)의
> 물리적 크기 앵커. WISHLIST Tier-2 #16. (JKR 1971 = 유료/접근 불가 → DMT가 *우리 체제이자 접근 가능한* 짝.)

---

## 1. 한 줄 요약
탄성 구(반경 R)–단단한 평면의 점착을 **열역학(가상변위)법**으로 엄밀히 풀어, **접촉을 떼어내는 힘은
접촉 변형이 생겨도 증가하지 않고 점접촉(미변형) 값과 같음**을 증명한다. 정전기 성분이 없을 때 그 힘은
**입자 반경의 1차에 비례**하고 **단위면적당 점착일 γ에 비례** → **F = 2πRγ** (= DMT pull-off). vdW 인력은
**접촉원 둘레의 고리(ring) 영역**에서 작용(접촉면 *밖*) — 이것이 JKR(접촉면 *안* 표면에너지)과의 본질적 차이.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| B.V. Derjaguin, V.M. Muller, Yu.P. Toporov (Dept. of Surface Phenomena, Inst. of Physical Chemistry, **Academy of Sciences, U.S.S.R., Moscow**) | J. Colloid Interface Sci. **53(2) 314–326 (1975)** | 10.1016/0021-9797(75)90018-1 | **해당 없음** — 보편 점착 접촉역학 이론 (워크드 예시 = 폴리스티렌–강철) | 이론 (continuum, 열역학+Hertz) |

- 접수 1974-10-10, 채택 1975-04-30. 분야 무관 정초 논문(수만 인용급); 우리에겐 점착(k_c/`--coh`)의 *이론 정의*.
- Derjaguin가 **1934년에 이미 이 문제를 제기**(ref 3)했고(가상변위+Hertz로 잉여 접촉변형 계산), 이 논문이
  그 1934 가정("접촉변형이 점착력을 증가시키지 않는다")을 **비접촉 고리 점착에너지를 명시적으로 넣어 엄밀 증명**.

## 3. 핵심 물성 (수치)
> ⚠ 이 논문엔 우리 표의 porosity/σ_ionic/Heckel 류 데이터가 **없다** (점착 접촉역학 이론). 핵심 "수치"는
> **pull-off 공식 자체 + 워크드 예시(폴리스티렌–강철)의 접촉면적·α/ε 표**다.

| 물성/양 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **DMT pull-off F₀** | **2πRγ** (= 2πR·φ(ε)) | 점접촉(α=0), 정전기 無 | **stated (eq 41/51)** | ★ 핵심 결과. R의 1차·γ의 1차 |
| F₀ (Hamaker 형) | **A·R / (6ε²)** | ε=최소 gap 3–4 Å | stated (eq 51) | A=Hamaker 상수, φ(H)=A/(12πH²) |
| 접촉영역 포화힘 F_s′ | **πRγ = F₀/2** | 큰 평탄화(α≫ε) | stated (eq 48) | 접촉-영역 성분만; pull-off는 여전히 2πRγ |
| 접촉반경²–접근 관계 | **a² = αR** | — | stated (eq 27) | Hertz 기하 |
| 점착 접촉면적 | **S = παR = πa²** | 무하중에서도 유한 | stated (eq 60) | 외력 없어도 vdW로 접촉면적 존재 |
| Hertz 탄성 반발력 | **F_e = 4R^½E/(3(1−σ²))·α^{3/2}** | — | stated (eq 49) | =kα^{3/2}, 표준 Hertz |
| 워크드 예시 | 폴리스티렌–강철: E=3×10¹⁰ dyne/cm²(=3 GPa), σ=0.33, A=10⁻¹² erg, ε=3 Å | Table II | stated | R 0.03–30 µm |
| Table II 결과 | R=0.03/0.3/3/30 µm → α/ε=2.1/4.5/10/21, S=7e-13/1.5e-11/3.2e-10/7e-9 cm² | — | stated | **작은 입자(30 nm)도 α/ε>1** |
| Table I | F_s/F₀ vs α/ε: 1e-5→0.997, 0.1→0.690, 1.0→0.738, 10→0.551, ∞→0.5005 | — | stated | 평탄화↑ → F_s가 F₀→F₀/2 로 감소 |

- E_SE/σ_y/ν: **n/a** (특정 소재 아님; 예시만 폴리스티렌).
- σ_ionic/σ_e/σ_thermal/porosity/Heckel/coverage/Z/PSD: **n/a** (점착 이론 — 전달·압밀 데이터 없음).

## 4. 시뮬레이션 방법 ★
> 시뮬레이션이 아니라 **해석 이론**이다. "방법"=수학적 유도 체계.

- **code / version**: 없음 (순수 해석). 모든 결과는 닫힌형/적분.
- **DEM 접촉법칙**: 해당 없음 — 그러나 **이 논문이 정의하는 점착이 DEM 점착항(k_c)의 이론 극한**이다.
- **이론 틀 (핵심)**:
  1. **변형장**: Hertz 압력분포 P_s(ρ)=3F/(2πa²)·(1−ρ²/a²)^{1/2}(**eq 1**)를 가정하고, 접촉면 *바깥*
     점들의 변형 w(r), 간극 z(r)을 적분으로 구함(eq 3→15→22→23). 결론: 접촉면 밖 간극은
     **z(r)=1/(πR)·[a(r²−a²)^{1/2}−(2a²−r²)·arctan((r²/a²−1)^{1/2})]+ε** (**eq 23a**, ε=최소 gap).
  2. **에너지 분해(열역학)**: 전체 자유에너지 = **탄성 부피에너지 W_e**(eq 24) + **표면에너지 W_s**(eq 25,
     `W_s=∫φ(H)·2πr dr`). W_s를 다시 *접촉영역* W_s′(eq 26·28, `W_s′=πaRφ(ε)`)와 *비접촉 고리* W_s″(eq 30·31)로 나눔.
  3. **일반화 힘(가상변위)**: F_s=dW_s/dα = F_s′+F_s″ (**eq 33**). 접촉성분 F_s′=πRφ(ε)는 α에 무관(상수),
     비접촉(고리)성분 F_s″를 명시적으로 적분.
  4. **점접촉 극한(α→0)**: F_s″(α=0)=πRφ(ε)(eq 40) → **F_s(α=0)=2πRφ(ε)=2πRγ** (**eq 41**). ★ 이게 DMT.
  5. **포텐셜 대입**: φ(H)=A/(12πH²)(Hamaker, eq 50) → F₀=AR/(6ε²)(eq 51). Table I/II는 이걸 수치화.
- **재료 파라미터**: E(탄성계수), σ(Poisson), A(Hamaker), ε(최소 gap 3–4 Å), γ=φ(ε)(점착일/면적).
- **입자 처리** ★ (DEM판 "무질서 처리"): **단일 탄성 구–평면**(두 구 R₁,R₂는 R→R₁R₂/(R₁+R₂)로 환원).
  형상=구. PSD 없음(단일 R). **점착이 있어도 형상은 Hertz 프로파일 유지**(접촉면 안은 안 건드림) — DMT의 정의.
  ⇒ **rigid도 진짜-SHAPE-소성도 아닌, "탄성+표면력" 연속체** 한 쌍. (소성은 아예 없음; JKR/DMT 둘 다 탄성.)
- **특이사항**: **체제 명시** — `E_ball/E_surf ≪ 1`(구가 절대 단단 평면에 접촉, 단 E가 너무 작으면 안 됨)을
  명시적으로 채택(p.315). 즉 **"높은 탄성계수 + 작은 매끈한 입자"**가 이 분석의 적용 영역이라고 직접 못박음.
  반대로 ref 2(저자들 Johnson 등)는 *매우 작은 E*(무른 큰 입자) 극한 = JKR 쪽이라고 대비.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | 탄성 구–강체 평면 접촉변형 계산 모식: 반경 R, 접촉반경 a, 중심접근 α, 접촉밖 점 (r,z), 거리 R′ | **변형장 기하의 정의도.** 우리 Holm 접촉반경 r_c·overlap δ와 같은 a·α 기하 (우리 a²=αR ↔ r_c=√(r²−(r−δ)²)) |
| **2** | 구–평면 상호작용 모식 (변형 *없을* 때): 간극 H, 최소거리 H₀, R, r. H≈r²/(2R)+H₀ | **점접촉(미변형) 극한** = pull-off 기준 상태. 비접촉 고리 점착의 출발 도식 |
| **3 (★)** | **상호작용 힘 vs 접근 α**: 탄성반발 F_e(↑, kα^{3/2}), 분자인력 F_d(↓), 합력(tearing-off) — F_s가 처음 감소 후 평탄(F₀→F₀/2) | ★ **점착의 힘–변위 도식.** pull-off 최대가 **점접촉(α=0)**에서 발생(=2πRγ)·평탄화하면 접촉성분이 F₀/2로 감소. 우리 SE-SE 접촉의 "떼기힘은 점접촉에서 최대" 물리 |

- Table I = 식 [52]/[54]/[59] 세 근사의 F_s/F₀ vs α/ε 일치 검증(점접촉 0.997 → 큰 변형 0.5).
- Table II = 폴리스티렌–강철 워크드 예시 (R별 α/ε·접촉면적 S) — **작은 입자에서도 변형이 무시 불가**임을 수치로 제시.

## 6. Post-processing ★
- **무엇**: 해석적 적분 평가(완전 타원적분 K(eq 6), 오일러 Γ·B 함수 eq 11, 급수 eq 8·13). 점착은
  **Hamaker 포텐셜 φ(H)=A/(12πH²)**(eq 50, Lifshitz 거시이론과 일치)로 구체화 → F₀=AR/(6ε²).
- **도구**: 손계산(타원적분·급수·Eulerian 함수 표; ref 7 Gradstein–Ryzhik, ref 8 Dwight 적분표 사용).
- **수치화·플롯**: Table I(3 근사 교차검증), Table II(R-의존 접촉면적), Fig 3(힘–접근 정성도).

## ★ 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
> ⚠ 멀티 에이전트 동시 작업 중 — `INDEX.md`·`comparison_vs_ours.md`는 건드리지 않고 여기 INLINE으로 작성.

| 항목 | 이 논문 (DMT) | 우리 | 차이 / 이유 (체제·매핑) |
|---|---|---|---|
| **점착 pull-off** | **F₀ = 2πRγ** (점접촉 극한) | LIGGGHTS `coefficientAdhesionStiffness` k_c (SE-SE **1e6**=10×AM-AM 1e5) / MPM `--coh`(A3) | **DMT가 k_c·`--coh`의 *물리적 크기 목표*.** 우리 k_c는 선형 점착분기 기울기(Luding eq6); DMT는 그 점착의 *연속체 표면력 극한*. γ↔k_c 환산 기준 |
| **체제(JKR vs DMT)** | **DMT = 단단·작은 입자·낮은 γ** (작은 Tabor μ) | **SE: R≈0.25 µm(D1 ~0.5µm), 상대적으로 단단** | ★ **우리는 DMT 체제** (JKR 아님). Tabor μ=(Rγ²/E*²ε³)^{1/3} 작음 → 접촉 *밖* vdW 고리 지배 |
| 점착 위치 | 접촉면 **바깥** 고리(ring) | (해당 정밀 위치는 모델 안 함; k_c는 overlap δ의 선형항) | DMT는 점착을 *비접촉 고리*로; 우리 k_c는 *접촉 overlap*에 — DMT가 작은 단단입자엔 더 물리적 |
| 형상/소성 | **탄성만**(Hertz 프로파일 유지, 소성 無) | DEM=rigid+CONTACT 탄소성 / MPM=진짜 SHAPE J2 소성 | DMT는 *탄성 점착 정초*; 소성은 Thornton–Ning(JKR+p_y캡)/우리 MPM이 담당(frame [5]) |
| F vs R 의존성 | **F ∝ R¹** (반경 1차) | (전달은 R과 packing으로; 점착력 자체는 미사용) | DMT 결론: pull-off는 R의 **1차**(Dahnneke의 R² 주장 반박 — ref 4) |
| 데이터 종류 | porosity/σ **없음** (점착 이론) | porosity·σ 삼중항·Heckel | **상보 아님 — 토대.** DMT는 *왜 SE가 cold-weld로 붙는가*의 pair-scale 이유 |

★ **JKR(1.5πRΓ) vs DMT(2πRγ)**: 두 식의 계수차(1.5 vs 2)는 **점착 위치 가정의 차이**다.
- **JKR(Thornton–Ning eq50, 우리 digest됨)**: 표면에너지가 **접촉면 안**에서 작용 → 접촉이 *목(neck)*을 만들며
  늘어남(접촉반경 a가 무하중에서 유한, jump-off 시 a=a_∞). pull-off P_c=**1.5πRΓ** (Γ=Dupré 일=2γ_표면).
  **무르고 큰 입자**(큰 Tabor μ).
- **DMT(이 논문)**: vdW가 **접촉면 밖** 고리에서만 → 접촉 프로파일은 Hertz 그대로(목 없음). pull-off=**2πRγ**.
  **단단하고 작은 입자**(작은 Tabor μ). → **우리 SE-SE가 정확히 이 쪽.**
- 두 계수(1.5↔2)는 **Tabor μ로 연속 보간**(Maugis–Dugdale): μ→0은 DMT(2), μ→∞은 JKR(1.5). 같은 물리의 양 극한.

★ **`adhesionStiffness`(k_c) 물리 앵커** (사용자 핵심 요청):
- 우리 SE-SE `coefficientAdhesionStiffness=1e6`(=10×AM-AM 1e5)이 인코딩해야 하는 *실제 점착력 크기*가
  **DMT F₀=2πRγ**. SE의 cold-weld(소결성 황화물)+vdW를 R≈0.25 µm로 평가 → k_c 보정 목표값.
- Luding eq6의 선형 점착분기 `−k_c·δ`의 **최대 인력** `f_min=−(k₂−k₁)δ_max/(k₂+k_c)` (우리 Luding digest CSV)이
  **DMT pull-off와 동차원** → k_c를 γ로 보정할 때 두 식을 맞추면 됨. (선형↔연속체 표면력의 다리.)
- **MPM `--coh`(backlog A3)**: 연속체 SE의 attractive σ. DMT/JKR이 그 점착의 *pair-contact 정의*(pull-off 크기·
  R-의존성) → `--coh` 도입 시 물리 타당성 기준. (우리 scaffold 실험: `--coh`는 wallP만 바꾸고 porosity는
  jamming 기하에 고정 — 점착이 porosity를 직접 안 움직임을 이미 확인.)

## 7. 적용 인사이트 (내 연구에 어떻게)
- ① ★ **SE-SE cohesion은 DMT 체제로 정당화** — R≈0.25 µm·상대적 단단함 → Tabor μ 작음 → **JKR 아닌 DMT**가
  맞는 극한. 우리 k_c(=1e6, 10×AM-AM)의 "왜 SE가 더 끈끈한가"를 *접촉면 밖 vdW 고리*로 물리화. (JKR 1971이
  유료라 못 봐도 **DMT가 우리 체제이므로 손해 없음** — 오히려 정답.)
- ② **k_c / `--coh` 보정 목표 = 2πRγ**. γ(SE 표면/계면 점착일)를 문헌에서 잡으면 F₀가 나오고, Luding f_min과
  맞춰 k_c를, MPM `--coh` 자기력을 *물리적 magnitude*로 고정 가능 (현재는 SE-SE 10×AM-AM 휴리스틱).
- ③ **pull-off는 R의 1차(2πRγ)** — Dahnneke의 R² 주장(ref 4·Krupp ref 18, "소성 접촉 가정")을 DMT가 명시 반박.
  우리 SE는 **탄성 점착**(소성은 압밀 후 별도)이므로 R¹ 스케일이 맞음 → 크기 sweep에서 점착 기여 ∝R.
- ④ **JKR↔DMT 다리(Tabor μ)는 EEPA/Pasha/Thornton–Ning과 한 묶음**: DMT(탄성 점착 정초)→Thornton–Ning(JKR+소성
  캡)→EEPA(면적의존 점착, Thakur)→Pasha(미세분말 선형 점착). 우리 점착 이론 스택의 *가장 바닥(탄성·작은입자)*이 DMT.

## 8. 인용 가능 문장 (deck/paper용)
- "For our sulfide SE particles (R ≈ 0.25 µm, relatively stiff), the adhesion sits in the **DMT regime**
  (small Tabor parameter), where van der Waals attraction acts in the ring *outside* the Hertzian contact;
  the corresponding pull-off force is **F = 2πRγ** (Derjaguin–Muller–Toporov 1975), the physical anchor for
  our LIGGGHTS `coefficientAdhesionStiffness` (SE-SE k_c) and the MPM `--coh` cohesion term."
- "DMT shows the tearing-off force does **not** increase with contact flattening — it stays at its
  point-contact value **2πRγ** and is **proportional to the first power of the particle radius**, in
  contrast to a plastic-contact (R²) assumption."
- "The JKR (1.5πRΓ) and DMT (2πRγ) pull-off limits differ only by the assumed location of the adhesive
  interaction (inside vs outside contact) and are the soft-large vs stiff-small ends of one
  Tabor-parameter continuum; our small stiff SE is the DMT end."

## 9. 주의/한계 (over-claim 방지)
- **탄성 점착 이론 — 소성·전달·압밀 데이터 없음.** porosity/σ_ionic/Heckel/coverage 류는 **전무**(n/a). 이 논문은
  *왜 SE가 pair-scale에서 붙는가*의 토대일 뿐, 우리 압밀·전달 절대값을 주지 않는다.
- **워크드 예시는 폴리스티렌–강철**(E=3 GPa). LPSCl/NMC811 아님 → **γ·A 절대값은 우리 소재로 다시 잡아야** 함.
  Table I/II 수치는 *체제(α/ε>1, R¹ 스케일)의 예시*이지 우리 SE 점착력 절대값이 아님.
- **DMT는 탄성 가정** — 우리 SE는 압밀 시 소성 흐름(MPM)·CONTACT 소성(DEM k₂/φ_f)도 함. DMT는 *점착의 탄성 극한*만;
  깊이 압밀된 SE-SE의 plastic pull-off 증가는 Thornton–Ning(eq77, P_cr=1.5πΓR_p*)가 다룸.
- **γ vs Γ 규약 주의**: DMT γ=단위면적당 점착일(=φ(ε)), JKR Γ=Dupré 일(=2×표면에너지). 1.5πRΓ와 2πRγ를
  *직접 계수 비교*하려면 같은 규약(work of adhesion)으로 환산 후 비교 — 그러면 DMT/JKR 비는 4/3(=2/1.5).
- **F₀는 ε(최소 gap 3–4 Å)에 매우 민감**(F₀∝1/ε²) — atomic-scale cutoff라 절대값은 ε 선택에 좌우. 추세(R¹·γ¹)는 robust.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
