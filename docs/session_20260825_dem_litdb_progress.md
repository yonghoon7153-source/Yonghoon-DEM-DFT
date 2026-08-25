# 2026-08-25 세션 — DEM 접촉모델 문헌 흡수 + 원고 방어 준비

> ⚠ **압축 전 대피소.**  이 문서의 가치는 **한정어**에 있다 ("하한", "방향만", "크기는 n/a",
> "인용 금지").  요약하지 말 것 — 요약은 한정어부터 깎는다.
> 정본 카드는 전부 `claude/friendly-meitner-lldvar` 의 `litdb/papers/` 에 있다.

## 0. 발단

지도교수(BML 강준희) 심사 질문 8개.  핵심 둘:
- **"이 값들이 합리적인가 / 잘 아는 사람이 보면 허무맹랑한 값 아닌가"**
- **"일반적으로 DEM 할 때 porosity 기준 calibration 해서 물성값을 뽑아 기재하기도 하는가"**

우리 상태: LIGGGHTS `hooke/hysteresis`, LPSCl 실물 E 22–24 GPa → **E_eff 1.35 GPa (18× 연화)**,
보정 타깃 = Minnmann pure-SE porosity ~10 % @ 300 MPa.  MPM: E 1.53 · ν 0.49 · σ_y 0.30.

---

## 1. ⚠⚠ 내가 사용자에게 잘못 말한 것 (정정 완료, 재발 방지용 기록)

| 내가 한 말 | 사실 | 출처 |
|---|---|---|
| "Coetzee 리뷰는 <10 kPa 영역" | **논문에 그런 진술 없음** (`kPa` 유효 매치 0). 응용 응력 크기 **미명시**. 나는 다른 문헌(2023 chapter) 스니펫을 이 논문 것으로 옮겼다 | Coetzee 카드 Q6 |
| "Coetzee 가 Heckel 을 표준시험으로 든다" | **`Heckel` 0회 등장.** 우리 Heckel 축은 이 리뷰 밖이고 별도 앵커가 필요하다 | 같음 |
| "DEM 으로 ASSB bottom-up 은 못 하고 대부분 XCT top-down" (사용자가 준희에게 한 말) | **사실과 반대.** So 2021/2022 · Bazzoun 2026 · Varkey 2026 · Zunker 2025 전부 bottom-up, XCT 없음 | 다수 |
| "영률 연화로 소성을 묘사하는 문헌 없다" | 표현이 위험. **연화는 소성의 *묘사*가 아니라 거시밀도 calibration** 이고, 그 방법론엔 이름(bulk calibration approach)과 전용 리뷰가 있다 | Coetzee |

---

## 2. Coetzee 2017 (Powder Tech. 310:104–142) — 보정 정당성

**인용 가능 문장 (준희 Q5·Q6 직답):**
- p.106 *"a calibration approach in the **true sense of the word**"*
- p.138 *"The bulk calibration approach is **by far the most popular** approach"*
- §9 결론 *"the particle shape can be simplified and assumptions in terms of the contact model
  can be made. The calibration process will then reduce the effect that these simplifications...
  since **the other parameters will compensate for it.**"*  ← **우리 E_eff 인식론과 같은 문장**

**★★ 최강 논거 = "500 µm".**  직접측정 학파 실적이 *"millimetre and above"*, 최소 사례가
500 µm 입자의 접촉마찰[218].  **우리 LPSCl SE 는 1–3 µm = 2–3 자릿수 아래** ⇒ 역보정은
선택이 아니라 **유일한 가용 경로**이고, 이건 우리 주장이 아니라 **리뷰 인용**이다.

**★★ 두 번째 — 우리가 쓴 시험이 하필 강성을 고립시키는 시험이다.**
§5.5 *"the **confined uniaxial compression test was only influenced by the particle stiffness**
while the particle-particle friction coefficient had **no significant effect**... The relation
between the particle stiffness and the bulk stiffness was found to be **linear**."*
Table 3 `Confined bulk stiffness (oedometer)` 행에서 조사된 유일한 파라미터가 접촉강성.

**⚠ E 를 낮추는 두 갈래를 섞지 말 것:**
- (a) **계산속도용** (Lommen/Cleary/Paulick 등, 조건 = "벌크가 안 변할 것", 가드레일 오버랩 0.1–4 %)
- (b) **벌크를 맞추려는 보정** ← **우리는 여기**
(a) 로 우리를 방어하면 **잘못된 인용**이고, (a) 가드레일로 우리를 재는 것도 **범주 오류**.
⇒ 우리 오버랩 ⟨δ⟩ ≈ 직경의 11–12 % (반지름의 22–24 %) 가 Paulick ≤1 % 의 22배인 것은
**범주 차이**이지 위반이 아니다.  단 두 사실은 남는다: ① 접촉법칙의 소변형 가정 밖 운용
② ε_sphere↔ε_union 규약차가 커짐 (우리 실측 1.251 %p) → **porosity 규약 명시 필수**.

**⚠ (b) 사례는 이 리뷰에 0건.**  다만 인식론은 승인 (Li[189] 형상 결손을 마찰로 럼핑 명시 승인).
**연화의 *방향*엔 기전 있음** (Van Lew Weibull-E → softer; Molenda μ 분포 → softer) — **배수는 n/a**.

**⚠ 우리 취약점 (F-C1~C7 로 `comparison_vs_ours_DEM.md` 등재):**
- **F-C1 유일성 미시험** — "구속압축은 마찰에 둔감"이 **남의 계(파쇄암·옥수수·저응력)에서 빌려온 가정**
- **F-C2 검증이 "충분히 다르지" 않다** — Heckel 4압력=같은 시험 다른 하중 / Cronau=같은 런 다른 관측량 /
  MPM=§8 이 허용하되 frame[4] 조건 병기 필수
- **F-C2′ ⚠ 탈출구가 막힐 수 있다** — 검증시험은 그 파라미터에 **민감해야** 하는데 우리 실측이
  *"σ_ionic 은 E 가 아니라 porosity 를 따른다"*, *"E 1.35 ≡ 1.5 동일 regime"*
- **F-C3 강성↔배위수 결합 미측정** (Ng&Asce: 강성↓→배위수↑; 우리는 1.35↔1.5 구간만 확인)
- **F-C5** 구 + rolling friction 없음 → 전단강도 원리적 과소, 그 결손도 E_eff 로 흘러듦

---

## 3. ⚠⚠⚠ Giannis 2021 (Granular Matter 23:17) — **우리 원장의 부호가 틀렸다**

`litdb/elasto_plastic_feasibility.md §경로B` 와 `varkey2026 §7`(본문 표)이
*"F_mc = 치밀영역 과강성을 고치는, 우리 18× 연화와 같은 증상의 다른 처방"* 이라고 적어 뒀다.
**부호가 반대다.**

원전 결론 *"able to provide a **higher force** at a given displacement than the classical DEM."*
Fig 7·9: MC-stress 가 최대겹침을 **가장 작게** 만든다.
- MC-stress = 침대를 **뻣뻣하게** → 같은 압력에서 porosity **↑**
- 우리 18× 연화 = 침대를 **무르게** → porosity **↓**

**우리 침대 대입 (에이전트 유도, 논문 수치 아님):** `ΔF/F = k·β·ν·C·(δ/d)`, k=0.25–1.5(규약 모호성)
| 침대 | δ/d | ΔF/F | 필요 연화 18× → |
|---|---|---|---|
| pure-SE (⟨δ⟩≈11 % of d) | 0.11 | +11 … +205 % | **20× … 55×** |
| production 복합 (⟨δ⟩ 1.75 %) | 0.0175 | +2 … +33 % | 18× … 24× |

⇒ **경로 B 는 18× 연화를 제거하지 못하고 늘린다.**  production 복합에서는 **사실상 무시 수준**
(AM 차폐로 ⟨δ⟩ 작음 — 우리 AM-shielding 과 자기일관).  의미 있는 곳은 pure-SE 펠릿뿐.
⇒ **"경로 A vs B 택일" 프레임 폐기, "A → (필요시) B 순차"** 가 맞다.
(Varkey SI 는 이미 옳게 적혀 있었다 — 본문 표와 SI 가 모순이었고 SI 가 맞다.)

**★ 재프레이밍 — 우리 연화의 진짜 약점:**
β 도 fudge 다 (저자 표현 *"adjustable dimensionless empirical geometric prefactor"*).
차이는 개수가 아니라 **위치**다:
| | 우리 E_eff | 그들 β |
|---|---|---|
| 위치 | ⚠ **측정된 물성 E 의 자리를 덮어씀** | 별도 항 — E·ν 는 실측값 유지 |
| 오염 | ⚠ **E 를 쓰는 모든 하위 계산** (Hertz 접촉반경·k_n·k_t·파속·timestep·Stage-E 입력) | 그 항 안에 격리 |
⇒ 약점은 *"경험적"* 이 아니라 **"물성 자리를 점유해 하위 계산을 오염시킨다"**.
그걸 없애는 건 **경로 A(항복캡, 자유변수 0, real E 유지)** 이지 B 가 아니다.

**기타 정정:** Giannis 는 **LIGGGHTS 구현**(우리 문서는 "상용/C++ 커스텀" — 틀림) ·
논문에 **소성이 없다**("elasto-plastic" 이라는 단어가 안 나온다; Varkey 가 TN 을 붙여서야 탄소성) ·
**최대 45 MPa** 로 우리 300 의 **6.7× 밖** · porosity·배위수·상대밀도 **보고 0**
("ρ>0.7 유효" 는 **Varkey 의 서술이지 Giannis 것이 아니다").

**★ 가설 (우리 재분석, 논문 주장 아님):** β 와 ν 는 항상 곱으로만 등장.
β·ν = 0.787 / 0.800 / 0.825 / 1.241 (E 가 2.8×10⁶배 변하는 동안 **1.58× 폭**, 셋은 ±2.4 %).
남는 1.5× 는 **배위수 C** 귀속 가능성 — 논문이 C 를 한 번도 보고하지 않아 **저자는 분리 불가**,
**우리는 C 를 안다**.  성공 시 결론 = "β 는 유도량(≈0.8/ν)" → 우리 LPSCl(ν=0.37) **β ≈ 2.1–3.4**.
⚠ 4점·3재료·C 미보고 — **인용 시 "우리 재분석"으로 표기 필수**.

---

## 4. Zunker & Kamrin 3부작 (JMPS 183:105492·105493 + Powder Tech 2025)

**★★★ 층(3) 판정은 철회가 아니라 정정.**  **층(2.75) 신설**:
겉보기 반지름 R(스칼라 1개) + 접촉별 δ_max → 절단구 형상이 **살아 있는 상태변수**.
힘을 올리고, **상대변위 0인 이차 접촉을 만들고**, `A_free/A_tot` 로 공극폐쇄를 발동시키고,
FEM 과 대조 가능하게 재구성된다.  사후 역맞춤도 자유흐름도 아니다.
**우리(MPM)에 남는 것**: 비축대칭 흐름 · 이방성 배럴링 · 실제 물질수송 · 오목한 이완형상 ·
**파괴** · 내부 응력/변형장.  ⇒ `our_dem_baseline.md §3` 을 그만큼 **좁혀야** 한다.

**⚠⚠ 우리에게 불리한 것:** 완전소성 영역에서 `F ≈ p_Y(δ)·A_geo(δ)` — **E 가 사라진다.**
항복캡 없는 선형 법칙은 `F ∝ E·δ` 라 겹침을 늘리는 길이 E 를 낮추는 것뿐.
그들 eq(41)을 우리 LPSCl(E 22.1, ν 0.37 → E*_c 12.80 GPa)에 넣으면 항복 겹침
**0.13 / 1.12 / 4.12 %·R** (σ_y 0.05/0.15/0.30).  우리 실측 겹침은 **14.8 %(복합) · 22 %(pure-SE)**
= **3.6×–169× 항복 초과**(중간 σ_y 에서 13×).
⇒ 우리 18× 연화는 **"빠진 항복캡의 대역"** 으로 읽는 것이 가장 간명하다 —
*"granular 재배열 lumping"* 이 아니라.  (전부 **우리 유도**, 카드에 그렇게 표기됨)

**치명적이지 않은 이유 3개:**
1. 우리 **MPM 은 항복캡이 있는데도**(J2, σ_y 0.15–0.30) 연화가 필요했다 (E=24 → porosity 33–38 %).
2. **세 논문 모두 porosity 를 한 번도 보고하지 않는다.**  *"연화 없이 실험 porosity"* 를 보인
   사람이 **없다** ⇒ 우리 *결론*은 반증되지 않았고 *설명*만 흔들린다.
3. **MCC ≠ LPSCl** (연성 유기물 vs 취성 세라믹) · **그들 모델엔 파괴가 없다**
   (LPSCl 은 3 µm 위에서 파쇄, Fan 2026 §3.5).

**★ 노브 회계 (공정하게 — 불편하지만 중요):** 그들이 노브가 **더 많다**
(Y fitted, ψ_b 0.08→0.5, µ_t 0.7, µ_wall 0.1, µ_roll 0.6, t_p 50, overlap cap 0.75, CoR).
**그러나 어느 것도 물성을 왜곡하지 않는다.**
⇒ 옳은 요약: ~~"그들은 무보정, 우리는 보정"~~ →
**"노브는 적지만 하나가 물성을 왜곡하는 우리 vs 노브는 많지만 어느 것도 안 건드리는 그들"**

**★ 유리한 것:** 그들의 부피 부기(`ΔV = −ΔV_e`, 절단구 + R 증가)가 **우리 ε_sphere(=ΣV₀)가
보존하는 바로 그 양**이다 (300 MPa 에서 tr(ε̄) ≈ 1 % 이내).
⇒ **ε_sphere 가 외부 지지를 받고 ε_union 은 강등**된다.  그들 방식도 우리와 **같은 자리에서
깨진다**(고구속에서 cap 교차 → 그들은 R 동결, 우리는 음수).

**★★ 런 없이 이번 주에 흡수 가능한 것 2개:**
1. Stage-E 의 **상수 Tabor 경도 → δ-의존 곡선** `H_eff(δ) = Y(1.75·e^{−4.4(δ/2)/R} + 1)`.
   우리 겹침에서 **2.08–2.26 Y** (2.8–3.0 이 아님) → `A_tabor = F/H` 가 **24–44 % 과소** →
   σ ∝ √cov 이므로 **σ_ionic 이 12–20 % 낮게 나오고 있다.**
   ⚠ Jackson–Green 2005 가 이미 같은 방향 = **독립 2출처**.
   ⚠ 착수 전 `network_conductivity.py` 가 실제로 쓰는 H 상수부터 확인할 것.
2. **`A_free/A_tot` 판독 추가** (LIGGGHTS 덤프로 충분).  우리 침대가 bulk-elastic 체제에
   들어갔는지 알려 주고, coverage 의 두 번째 분모가 되며, MPM `d_h/dx` 채널폭 축과 상관될 것.

**★★★ 미실행 결정 실험 (제안):** 그들 LAMMPS `mdr` 브랜치는 **단일 재료만** 지원 —
그게 정확히 우리 **pure-SE** 문제다.  real E=22.1 · ν=0.37 · σ_y ∈ {0.05, 0.15, 0.30} ·
κ = 우리 DFT B₀ 26.23 GPa · 100/200/300/600 MPa.
사전등록: **h0** porosity ≤ 12 % @300 → 연화 *서사*를 다시 써야 한다 /
**h1** porosity ≥ 18 % → 연화가 항복캡으로 안 되는 무언가를 담고 있고 그 크기를 처음 정량화.
비용: `Δt ≈ 9×10⁻¹¹ s` (0.5 µm SE), real E 로 가면 Rayleigh 로 ~4배 스텝.
> *"연화가 불가피하다고 논문에 쓰면서 이걸 안 돌리면, 그 문장이 리뷰어의 첫 표적이다."*

**⚠ 함정 2개:** (i) 그들 `Δγ = 450 J/m²` 는 K_Ic 에서 역산한 **유효 파괴에너지** —
우리 DFT `W_ad = 1.107 J/m²` 를 그 자리에 넣으면 **400배 오류**.  `G_c = K_Ic²(1−ν²)/E ≈ 3.24 J/m²` 를 쓸 것.
(ii) 그들 topological penalty 는 **우리 겹침에서 비활성**(동일크기 발동 δ/R > 0.30, 우리는 0.15–0.22)
= 우리 겹침이 through-particle 인공물을 만들지 않는다는 **인용 가능한 방어**.
⚠ 단 **강한 다분산**에서 거리 기반 centrality 가 크기맹목: 6 µm AM 두 개 사이 홈에 낀 0.5 µm SE 가
α≈137° 로 "central" 로 라벨돼 **정당한 AM–AM 접촉을 0 으로 만든다** → 우리 force chain·σ_e 망 파괴.
12:4:1 에 쓰기 전 **크기 인지 centrality 수정** 필요 (우리가 주장할 수 있는 방법론 기여).

---

## 5. PyCompact 2025 (SoftwareX) — DEM→MPFEM, 우리와 같은 architecture

**★★ 제3자 진술 3종 확보** (우리 원고 핵심 논거의 외부 근거):
- DEM 은 *"assumptions of rigid or simplified particle shapes that **neglect internal deformation**"*
- MPFEM 은 *"each particle is modeled as a **deformable finite element body**"*, 고압밀에 *"essential"*
- **대칭으로** 균질화 FEM 은 *"**overlooks the discrete nature** of particles … low-density stages
  where particle rearrangement dominates"*
  ★ 세 번째가 특히 값지다 — 우리 CORRECTION 2(소성 MPM 이 Furnas dip 재현 실패)의 문헌 짝이고
  **frame[5] 분업이 우리 편의가 아니라 방법론의 구조**임을 외부 문장으로 닫는다.

**MPFEM 이 층(3)을 한다 — 명백히** (PEEQ 1.3 = 130 %, 구→다면체).
그리고 이 논문은 **접촉 LAW 층(우리 "경로 A")을 통째로 우회**한다.
⇒ 층 지도에 붙일 한 줄: **"층 3 에 도달하는 길은 둘뿐 — 입자마다 연속체를 메시하거나(MPFEM),
입자 없는 연속체로 상 전체를 흘리거나(MPM).  접촉 LAW 를 아무리 정교화해도 층 3 에는 못 간다."**

**우리가 MPFEM 을 안 쓴 것의 방어 = 규모이지 물리 우위가 아니다.**
그들 실측 569 입자 = 9 h/24 CPU, 입자수 스케일 지수 1.34–2.43.
우리 real_14 SE 32,832 개 → 입자수만으로 22–164일, ⌀1 µm explicit dt 벌금 ×16 → **약 1년**(요소 65.7 M).
방어 가능한 문장: *"MPM 을 고른 이유는 침대 규모와 대변형 견고성이지 접촉 표현의 우수성이 아니다."*
⚠ 불리한 사실: **MPFEM 은 접촉과 형상소성을 한 이산화 안에서 동시에** 갖는다.
우리 DEM 은 형상소성이 없어 Stage-E 로, 우리 MPM 은 접촉이 없어 기하 coverage 로 우회한다.
MPFEM 은 원리적으로 변형된 실접촉면적 a(δ) 위에서 **Holm 협착저항을 바로** 계산할 수 있다
(단 이 논문은 전달물성을 한 번도 계산하지 않았으므로 가능성이지 실증은 아니다).

**⚠⚠ 새 구멍 — springback.**  탄성 회복 P/E:
그들 **1.2 %** · 우리 MPM(K=25.5 GPa @ν0.49) 체적 **1.2 %** ✓ ·
우리 **DEM(E_eff 1.35, ν0.3 ⇒ K 1.125 GPa) 체적 26.7 %**.
⇒ **ν=0.49 stiff-bulk 선택이 제하 축에서 실재 분말과 같은 자리에 있고, DEM 의 18× 연화는
제하를 풀면 무너진다.**  지금은 제하를 안 풀어 노출되지 않은 잠재 한계.
⇒ **미해결 질문: Minnmann 10 % · Cronau 11–12 % 가 가압 중 값인가 해압 후 값인가?**
후자면 우리 DEM porosity 를 **다른 규약의 값**에 맞춘 셈이다.

**훔칠 것:** porosity–pressure **하중+제하 루프** 그림 형식 (우리는 점으로만 보고 — 루프로 그리면
springback 이 보인다) · 민감도 3종(요소·마찰·RVE)+비용표 형식 (⚠ 단 그들의 "convergence" 라벨은
훔치지 말 것 — Fig 3(e)는 단조 감소이고 평탄부가 없는데 "수렴"이라 적었다; 실제 선택 근거는
36 h vs 9 h) · **소형 SE-only REV(100–500 입자)를 OpenRadioss MPFEM 으로 한 번 돌려 a(δ) 를 뽑아
Stage-E 를 외부 검증** (그들 스케일로 수 시간~하루, 실행 가능).

⚠ 그들 정확도 표기 주의: 초록 "2.5 %"는 **상대값**이고 절대로는 **2.1 %p** (83.3 exp vs 85.4 sim).
⚠ frame[4] 등급: 실험·ABAQUS 참조·재료상수가 **전부 같은 그룹 선행 논문** — 외부 독립 앵커 아님.

---

## 6. 준희 질문 ↔ 근거 배치 (완성 대기)

| 질문 | 근거 | 상태 |
|---|---|---|
| ④ 이 값들이 합리적인가 | `wang2026_dryprocess…` **AFM 실측 1.3–3.1 GPa**(건식 황화물 복합막; ⚠ 카드가 *"막 압입 ≠ 입자 접촉강성, '일치' 표현 금지"* 경고) + σ_y 0.30 = 문헌 범위 **상단** + ν 0.49 → K 25.5 ≈ **우리 DFT B₀ 26.23 (−2.8 %)** | ✅ |
| ⑤ porosity 기준 보정이 일반적인가 | **Coetzee 2017** | ✅ |
| ⑥ source 를 calibrated 로 써도 되나 | **Coetzee 2017** — measured/calibrated/assumed 구분 · 물성 vs 모델파라미터 분리 · **코드·접촉모델 병기** · 검증 별도 보고.  ⚠ 코드마다 **입자강성 지정 vs 접촉강성 지정**이 달라 후자는 **절반** → `E_eff=1.35` 이 **재료(입자) 입력값**임을 표에 못 박을 것 | ✅ |
| ② E/ν/σ_y/전단탄성률 출처 | 3층 분리 · **G 는 입력이 아니라 유도값**(μ = E/2(1+ν) = 0.51 GPa) | ✅ |
| "DEM 은 형상소성 못 한다" | **PyCompact 제3자 진술 3종** + **MPFEM Demirtas**(진행 중) | ✅ |
| "왜 연화 말고 항복캡을 안 썼나" | So 2021 + **Zunker–Kamrin** — 답: *"LIGGGHTS 기본 접촉법칙에 항복캡이 없고 구현은 이 논문 범위 밖.  대신 독립 앵커로 검증"* + **노브 회계 프레임** | ✅ |
| ⑦ NCM811 σ_e "effective" 의 뜻·출처 | **Amin & Chiang** (진행 중).  ⚠ `σ_AM = 50 mS/cm` 이 *"NCM811 literature reference"* 라 라벨돼 있는데 **출처 미특정**; 검색이 내놓는 intrinsic ~10⁻⁵ S/cm 와 자릿수 격차.  σ_S 10 · σ_P 5 는 **코퍼스 적합 끝점**으로 정직하게 라벨돼 있음 | ⏳ |
| ① 제작압 ≠ DEM 압력 | DEM 압력은 **보정 앵커에 묶여** 있다(300 에서 10 % 를 내도록 정함) → 바꾸면 재보정 동반.  SBE·DBE 가 같은 300 이라 **비교는 공통모드 상쇄**, 영향은 절대값뿐 | ✅ |
| ⑧ 수식이 없다 | 접촉 힘법칙 · J2 항복 · `∇·(σ∇φ)=0` 3개 추가 | ✅ |

---

## 7. 산출물

- `scripts/gen_dem_oat_sweep.py` (selftest 22/22) → `dem_scripts/oat_sweep/` 입력 12 + 러너 + 매니페스트
  ⚠ **구조 변경 1건**: 원본이 atom type 1개라 **μ_pw 가 μ_pp 에 묶여 독립 노브가 아니었다** →
  type 2 로 분리.  그래서 **`base` 런이 음성 대조** — 재현 못 하면 OAT 전체 무효.
- litdb 정본 카드 (`claude/friendly-meitner-lldvar`): coetzee2017 · giannis2021 · zunker2024 ×2 ·
  zunker2025 · pycompact2025 (+ 진행 중: paulick2015 · gonzalez2012 · demirtas2021 · aminchiang2016 · vanlew2015)
- ⚠ **DEM 축 인덱스 정본은 `INDEX_DEM.md`** (자동생성).  `INDEX.md` 는 argyrodite/SE 축.
  비교표는 `comparison_vs_ours_DEM.md` (§F 에 F-C1~C7).

## 8. 다음

1. **⚠ 부호 정정 반영** — `litdb/elasto_plastic_feasibility.md §경로B` 와
   `litdb/contact_models_layer_map.md` 가 **동결 스냅샷에만** 있고 **틀린 부호를 담고 있다**.
   어느 브랜치에 어떻게 고칠지 **사용자 결정 필요**.  (규율 ④: 수치를 철회하는 커밋은 같은
   커밋에서 파생 문서를 고친다)
2. **Stage-E H 상수 확인 → δ-의존 경도** (σ_ionic 12–20 % 영향)
3. **OAT 스윕 로컬 실행** (기준선 음성 대조 먼저)
4. **Minnmann/Cronau 규약 확인** (가압 중 vs 해압 후)
5. pure-SE `mdr` 런 사전등록
