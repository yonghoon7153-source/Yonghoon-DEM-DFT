---
title: "Liu, Roters, Raabe 2024 — Role of grain-level chemo-mechanics in composite cathode degradation of solid-state lithium batteries (Nature Communications 15, 7970)"
source_url: local-upload/03._Role_of_grain-level_chemo-mechanics_in_composite_cathode_degradation_of_solid-state_lithium_batteries.pdf
source_url_si: local-upload/03._Sup_Role_of_grain-level_chemo-mechanics_in_composite_cathode_degradation_of_solid-state_lithium_batteries.pdf
source_doi: 10.1038/s41467-024-52123-w
pdf_sha256_main: 0835168b00b55fc325c0c845453290ce36c6b9c2573bc1e7fba1477e3c2d1d8d
pdf_sha256_si: 46b8d56fb2e7892f863913a8a9ed47a83a0c4ecfb911e392640679109103e14c
ingested: 2026-09-16
sha256: d1d5a69cda8ef2514b198fae97fcbbb7ae0783636f7c58ed5ba6d1837270e594
---

# 수집 목적

Chuanlai Liu (교신), Franz Roters, Dierk Raabe (교신),
**"Role of grain-level chemo-mechanics in composite cathode degradation of
solid-state lithium batteries"**, *Nature Communications* **15** (2024) 7970,
doi `10.1038/s41467-024-52123-w` 의 **절별 해체분석** — 본문 PDF 18 쪽(논문 쪽번호
1–14 + 참고문헌) + Supplementary 10 쪽.

**이 위키 `assb` 섹션의 3호 논문이다.** 액체셀 계열(현재 `raw/papers/` 20 편)과
**섞지 않는다** — 음극 축이 다르다.

흡수 이유는 하나다. 닻([[assb-contact-loss-vs-lampe]])의 가장 큰 공백이
**`θ` 의 시간축**이었고, `assb` 1호(Bielefeld 2019, 기하)·2호(Clausnitzer 2023, 수송)
**2/2 편이 그것을 주지 않았다**. 이 논문은 제목에 *degradation* 이 있고 축이 **역학**이다.
그래서 물어야 할 것이 정해져 있었다: **접촉 손실이 사이클과 함께 어떻게 자라는가.**

> ★ **먼저 답부터 적는다 — 이 논문도 `θ(N)` 을 주지 않는다.**
> 시뮬레이션은 **방전 1 회**(Fig. 4f 만 방전 1 회 + 곧이은 충전 1 회)이고, 사이클 수를
> 축으로 쓴 그림이 **0 장**이다. 더 결정적으로, 이 모델에는 **접촉 손실이라는 변수가
> 없다** — 파괴도 디본딩도 구현되지 않았고(논문이 스스로 인쇄한다), 있는 것은
> **계면 최대주응력**(GPa)뿐이다. 즉 이 논문은 `θ` 가 아니라 **`θ` 를 떨어뜨릴
> 구동력**을 준다. `assb` **3/3 편이 시간축을 주지 않았다.**

대신 이 논문이 **주는 것**이 세 가지 있고, 그중 둘은 `assb` 섹션 최초다:

1. ★ **OCV 곡선이 처음 들어왔다** (SI Fig. S2, GITT 측정 NMC811 반쪽전지 OCV,
   3.0 → 4.4 V vs Li/Li⁺). 2호는 전압축은 줬지만 OCV 곡선은 없었다.
2. ★ **율 스윕이 처음 들어왔다** (SI Fig. S4: 0.25C·0.5C·1C·2C·5C × 입자 4 크기,
   전압–용량 곡선 20 장). [[assb-apparent-capacity-decomposition]] 이 2호 두 문장에서
   **추론만** 했던 "율이 세 항 중 동역학 하나만 지운다" 를 **직접 볼 수 있는 자료**다.
3. **용량 손실을 논문 스스로 두 항으로 쪼갠다** — `[인쇄]` "thermodynamic capacity loss
   due to the irreversible loss of active materials" + "kinetically induced capacity loss".
   우리 3항 분해와 이름이 겹치므로 **좌표 대조가 필요하다** (§15).

**표기 규칙** (이 위키 관례 3구분 + 1):
- `[인쇄]` — 논문 본문/식/표/그림 안에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (**원 데이터가 아니다**; `figure-read ≈`)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 원문 값을 이 세션에서 산술로 옮긴 것 (계산식을 함께 적는다)

> ⛔ **인용 금지.** 이 파일의 숫자는 **사본**이다. 인용 근거는 원문 PDF 이고,
> 우리 연구 수치의 정본은 artifact + `degradation-degeneracy/docs/RESULTS*.md` 다.
> 여기 적힌 수치를 논문·보고서에 옮기려면 원문을 다시 확인한다.
>
> ⚠ **모집단 경고.** 이 논문의 결론은 **NMC811 이차입자 1 개**(지름 2–12 µm, 기본 12 µm,
> 일차입자 200 개 무작위 방위)가 **균질 고체전해질 블록 안에 박혀 있는** 대표체적요소,
> **완전 접합 가정**(계면 파괴·디본딩 없음), **전자 전도는 탄소 바인더로 집전체에
> 연결됐다고 가정**, **고체전해질 안의 Li 수송은 아예 모델링하지 않음**,
> **정전류 방전 1 회**(3 V 컷오프), **구조 실현 1 개**(반복 없음) — 이 한 조합의 것이다.
> **셀 실험 0 개 · 사이클링 0 회 · 스택 압력 0 회**다.
>
> ⚠ **★ 가장 무거운 모집단 경고**: 이 모델의 전압–용량 곡선에는 **고체전해질 물성이
> 하나도 들어가지 않는다** (`[인쇄]` "Li-ion transport inside the solid electrolyte is not
> considered explicitly"). 따라서 Fig. 3h·4a·6h·S4 의 **모든 용량 예측은 "고체전해질
> 안의 NMC811 입자" 가 아니라 "완벽한 리튬 공급원에 잠긴 NMC811 입자" 의 것**이다
> (`[해석]`). 제목의 *solid-state* 가 이 결과들에 들어오는 통로는 **역학(탄성률·항복강도)
> 뿐**이다.
>
> ⚠ **`[도표]` 경고.** 이 논문은 **결과 수치표가 0 개**다 (숫자표는 Supplementary
> Table S1 의 **입력 파라미터**뿐). 아래 결과 수치는 대부분 **그림에서 눈으로 읽은 값**
> 이며 ±5~10 % 오차를 가진다. 모두 `[도표]` 로 표시했다.

- 원본 파일 (로컬 업로드, 저장소에 바이너리를 넣지 않는다):
  - 본문 `03._Role_of_grain-level_chemo-mechanics_in_composite_cathode_degradation_of_solid-state_lithium_batteries.pdf`
    (18 쪽, PDF sha256 `0835168b00b55fc325c0c845453290ce36c6b9c2573bc1e7fba1477e3c2d1d8d`).
    PDF 메타데이터: `title` = 논문 제목, `author` = Chuanlai Liu,
    `subject` = `Nature Communications, doi:10.1038/s41467-024-52123-w`,
    `creator` = Springer, `creationDate` 2024-09-12.
  - SI `03._Sup_Role_of_grain-level_chemo-mechanics_...pdf`
    (10 쪽, PDF sha256 `46b8d56fb2e7892f863913a8a9ed47a83a0c4ecfb911e392640679109103e14c`),
    `creator` = LaTeX with hyperref, `producer` = pdfTeX-1.40.25, `creationDate` 2024-07-30.
- 크로핑한 그림: `wiki/raw/figures/liu2024_grain-level-chemo-mechanics-composite-cathode-degradation/`
  (`figures.json` 에 캡션·좌표). **본문 Fig. 4 · Fig. 7 과 SI 전체는 캡션 자동 검출이
  실패해서**(`Fig. S.1` 처럼 번호에 점이 있다) 이 세션에서 쪽 렌더로 따로 만들었다 —
  `fig_4.png` `fig_7.png` `fig_S1..S8`, 확대본 `fig_4a.png` `fig_5def.png` `fig_6h.png`
  `fig_3c.png` `fig_6_full.png`. 이들은 `figures.json` 에 없다(수동 산출).

---

## 원문에 없어서 확인이 필요한 것 (먼저 적는다)

1. **Fig. 5d–f 의 용량 손실이 무엇에 대한 비인지 원문에 없다.** 같은 12 µm·1C 조건에서
   Fig. 4a/S4c 의 방전 곡선은 정규화 용량 `[도표]` ≈0.68 (손실 0.32)인데 Fig. 5d 의
   "total normalised capacity loss" 는 `[도표]` ≈0.215–0.235 다. **두 수가 같은 축일 수 없다.**
   → §13 D4. **이 좌표가 안 풀리면 Fig. 5·7 의 숫자는 우리가 쓸 수 없다.**
2. **"kinetically induced capacity loss" 가 최소 두 가지 다른 양을 가리킨다** (§13 D5).
3. **Fig. 4a 의 실험 곡선이 어느 셀·어느 기준전극의 전압인지 없다.** 출처(ref 62)의
   제목은 **Si 음극 + 황화물 고체전해질**인데 축은 4.5 V 까지 간다 (§13 D11).
4. **구조 실현(무작위 방위 배열)의 산포가 없다.** 본문은 `[인쇄]` "the **random
   arrangement** of primary particles in the secondary particle play a critical role in
   dislocation heterogeneity" 라고 적고도 **실현 1 개**만 돌린다. `seed`·`standard
   deviation`·`error bar` 각 **0 회**.
5. **12 % 소성전단 문턱의 불확실성이 없다.** 이 한 수가 "loss of active materials" 축
   전체를 정한다(§10). 문턱을 바꾸면 Fig. 5d·5e·7b 가 전부 움직이는데 민감도 시험이 없다.
6. **접촉 손실의 정량이 없다.** 면적 분율도, 임계 응력도, 파괴 인성도 없다 — 응력
   분포뿐이다. 따라서 `θ` 로의 변환 계수를 이 논문에서 얻을 수 없다.
7. **스택 압력이 없다** (`pressure` 는 본문에서 argyrodite 전도도 논의와 참고문헌
   제목에만 나온다). 계면 접촉을 다루면서 압력이 없는 것은 `assb` **3/3 편 공통**이다.

---

## 0. 서지사항 (직접 확인)

| 항목 | 값 |
|---|---|
| 저자 | **Chuanlai Liu**¹ (교신), **Franz Roters**¹, **Dierk Raabe**¹ (교신) |
| 소속 ¹ (본문) | `[인쇄]` **Max Planck Institute for Sustainable Materials**, Max-Planck-Str. 1, Düsseldorf 40237, Germany |
| 소속 (SI 표제지) | `[인쇄]` **Max-Planck-Institut für Eisenforschung GmbH**, 같은 주소 |
| 교신 이메일 | `c.liu@mpie.de` · `d.raabe@mpie.de` |
| 저널 | *Nature Communications* (2024) **15**:7970 |
| DOI | `10.1038/s41467-024-52123-w` |
| 접수/수리 | `[인쇄]` Received 9 February 2024 · Accepted 23 August 2024 |
| 참고문헌 | 116 개 (본문) + 13 개 (SI) |

`[해석]` 소속 이름이 본문과 SI 에서 다르다. 같은 기관의 **개명**이다 (MPIE →
Max Planck Institute for Sustainable Materials, 2024). 코드 접근 허가의 주체는
**옛 이름(MPIE GmbH)** 으로 적혀 있다 (§6).

---

## 1. 초록 — 무엇을 주장하는가

`[인쇄]` 전문(요지):

> "Solid-state Li-ion batteries, based on Ni-rich oxide cathodes and Li-metal anodes,
> can theoretically reach a high specific energy of **393 Wh kg⁻¹** … Here, we present a
> **microstructure-sensitive chemo-mechanical model** … We reveal that **crystalline
> anisotropy, state-of-charge-dependent Li diffusion rates, and lattice dimension changes
> drive dislocation formation in cathodes and contact loss at the cathode/electrolyte
> interface.** These dislocations induce large lattice strain and **trigger oxygen loss and
> structural degradation preferentially near the surface area** of cathode particles.
> Moreover, **contact loss is caused by the micromechanics** resulting from the crystalline
> anisotropy of cathodes and the mechanical properties of solid electrolytes, **not just
> operating conditions.**"

`[해석]` 초록의 네 주장을 모델 안의 양으로 옮기면 이렇게 된다 — **셋은 모델이 계산하고
하나는 계산하지 않는다**:

| 초록의 주장 | 모델 안의 양 | 계산되나 |
|---|---|---|
| 이방성·SOC 의존 확산이 **불균일 Li 분포**를 만든다 | `θ(x,t)` 장 | **예** |
| 그것이 **전위(dislocation)** 를 만든다 | 소성전단 `γ` | **예** |
| 전위가 **산소 손실·구조 열화**를 부른다 | `γ > 0.12` 인 영역 = 산소결핍상 | **문턱 규칙** (계산 아님, §10) |
| 그것이 **접촉 손실**을 부른다 | — | **아니오** (파괴·디본딩 없음, §3) |

★ **"contact loss is caused by …" 는 이 논문이 계산한 것이 아니다.** 본문이 스스로
인쇄한다 — `[인쇄]` "the current model **does not explicitly account for mechanical
fracture**" · "While the present study uses the **maximum principal stress distribution**
to analyse contact mechanics problems". 즉 **응력이 크다 → 접촉이 떨어질 것이다** 라는
한 걸음이 초록에서 생략돼 있다. §13 D3.

또 `393 Wh kg⁻¹` 은 **출처 표시가 없고 본문에 다시 나오지 않는다** (§13 D2).

---

## 2. 서론 — 이 논문이 서 있는 자리 (p1–p2)

핵심 논지는 **"계면 부반응 탓이 아닐 수도 있다"** 이다:

- `[인쇄]` Ni-rich 층상 산화물 양극은 "suffer from contact loss, and irreversible
  layered-to-spinel or disordered rock-salt-like phase transition".
- `[인쇄]` 기존 설명은 계면 부반응 기원의 산소 손실·TM 이동이다. 그러나 표면 코팅이
  **벌크 구조열화를 못 막는다** → `[인쇄]` "This dilemma raises the suspicion that the
  electrochemical instability of the cathode/electrolyte interface **may not be the main
  cause** behind the progressive capacity degradation observed over cycling."
- `[인쇄]` NMC811 의 부피 변화 **7.8 %** (refs 8,18,19). ⚠ 자기 Fig. 3b 적합으로
  [재현]하면 ≈6.3 % 다 (§13 D8).
- `[인쇄]` 10 % 인장변형에서 산소공공 형성에너지가 **1.06 eV → 0.24 eV** 로 떨어진다(ref 4).
- 빈자리 선언: `[인쇄]` "the assessment of how microstructure and (dis)charging protocols
  affect the formation of crystal defects … **at the grain level in composite cathodes
  remains unexplored**."

`[해석]` 이 논문의 인과 사슬은 **불균일 Li → 전위 → 격자변형 → 산소 손실 → rock-salt →
(a) 활물질 손실 + (b) Li 경로 차단** 이고, **계면 접촉 손실은 이 사슬의 옆가지**로
응력만 계산된다. 우리 관심(접촉 손실 ↔ `LAM_PE` 분리)에서 보면 **주가지가 오히려
`LAM_PE` 의 생성 기구**를 준다 — 뒤에서 이것이 이 논문의 실제 기여임이 드러난다(§15).

---

## 3. Methods — 대표체적요소(RVE)와 세 단계 (p3, Fig. 2, Fig. S1)

`[인쇄]` 절차 3 단계:

**(1) 미시구조.** "an isolated Ni-rich **NMC811 polycrystal particle, consisting of 200
randomly oriented primary particles, is embedded in the uniform solid electrolyte.**"
`[인쇄]` "The polycrystalline cathode particle **maintains electrical neutrality as it is
assumed to be connected to the current collector via the carbon binder** of the composite
cathode."

★ `[도표]` **Fig. S1 을 직접 봤다**: RVE 는 **정육면체 고체전해질 블록 안의 구 1 개**다.
(a) 입계 없음 · (b) 입계 있음(입자 사이 2 층 요소). **전극도, 공극도, 탄소도, 다른
입자도 없다.** `[해석]` → **이 논문의 "복합양극" 은 1호·2호의 복합양극과 길이 척도가
다르다.** 1호·2호는 전극(수십 µm 두께, 수천 입자, 퍼콜레이션)이고, 이 논문은
**입자 1 개 + 그것을 감싼 전해질**이다. `θ_AM` 은 이 RVE 에서 **정의상 1** 이다
(입자가 하나이고 탄소로 집전체에 붙어 있다고 **가정**되므로).

**(2) 화학–역학 구성모형.** `[인쇄]` Cahn–Hilliard 반응–확산으로 계면 반응과 Li 삽입을
기술. ★ `[인쇄]` **"Li-ion transport inside the solid electrolyte is not considered
explicitly since we only simulate (dis)charge processes at constant currents."**
`[인쇄]` 정전류 = 이차입자 표면에 **일정한 Li 유속**. 응력 없는 기준상태는 방전 시
`θ = 0.1`, 충전 시 `θ = 0.9`. 층상 구조라 **Li 확산은 basal(a–b) 면에만**,
확산계수는 SOC 의존. 격자 치수 변화에 맞추려 **misfit 전위**가 생기고 이를
**결정소성**으로 기술. 고체전해질은 **등방 탄성만**(뒤에서 J2 소성 추가).
★ `[인쇄]` **"the current model does not explicitly account for mechanical fracture."**

**(3) 산소결핍상.** `[인쇄]` "material domains with a **plastic shear exceeding 12 %** in
cathode particles after discharge are categorised as the oxygen-deficient phase. This
threshold is determined based on the atomic-scale calculations and **by fitting the
predicted distribution of oxygen-deficient phase in the secondary particle to experimental
characterisation⁵**." `[인쇄]` 이 상은 이후 사이클의 **Li 삽입 경로를 막는다**.

★ `[해석]` **이 문턱이 이 논문에서 유일한 "적합된 라벨"이고, `LAM` 축 전체를 정한다.**
게다가 맞춘 대상(ref 5 = Csernica et al., *Nat. Energy* 2021)은 **Li-rich 층상 산화물**
이고 모델은 **NMC811** 이다 — 화학이 다르다 (§13 D9).

용량 정의 `[인쇄]`:
- `Q` (practical absolute discharge capacity of NMC811) = **203 mAh g⁻¹** (ref 56)
- **normalised capacity = 3 V 컷오프까지의 방전 용량 / 203 mAh g⁻¹**
- `[인쇄]` "The **total normalized capacity loss** at a specific current consists of two
  components: **thermodynamic capacity loss due to the irreversible loss of active
  materials** and **kinetically induced capacity loss, which arises from non-uniform Li
  distribution within the particles**, characterized by Li-rich peripheries and Li-poor cores."
- `[인쇄]` 평균 Li 점유 **0.1 = 완전 탈리튬**, **0.99 = 완전 리튬화**.

★ 이 인쇄 정의가 Fig. 5f 의 캡션과 충돌한다 (§13 D5) — **이 digest 의 가장 중요한 발견 중 하나.**

---

## 4. Methods — 지배방정식 (p12–p13, 식 1–21)

| 식 | 내용 |
|---|---|
| (1) | `ψ(c_Li, F) = ψ_chem(c_Li) + ψ_mech(c_Li, F)` |
| (2) | `∂c_Li/∂t = C_max ∂θ/∂t = −∇·j + R(θ, η)` — Cahn–Hilliard 반응–확산 |
| (3) | `∇·P = 0` — 역학 평형(준정적) |
| (4) | `R = −n·j_r` — 반응면 질량보존 |
| (5) | **`R = nQρ V_NMC / A_NMC`** — `n`C 방전 시 표면 유속 (`Q` = 203 mAh g⁻¹, `ρ` = 4.78 g cm⁻³) |
| (6) | `ψ_chem = C_max[kT(θlnθ + (1−θ)ln(1−θ)) + E₁θ + E₁₁θ²]` — 정규용액 모형 |
| (7) | `j = −C_max M·∇μ` |
| (8) | `μ = kT ln(θ/(1−θ)) + E₁ + 2E₁₁θ + μ_mech` |
| (10) | **`F = F_e F_c F_p`** — 탄성 · **조성 고유변형** · 전위 소성의 곱분해 |
| (11)(12) | `F_c = I + V_c`, `V_c = diag(ν_a, ν_b, ν_c)` (결정 좌표계) |
| (13)–(16) | 결정소성 유동법칙 `L_p = Σ γ̇^α m^α⊗n^α`, 멱법칙 `γ̇^α = γ̇₀(τ^α/g^α)^n sgn(τ^α)`, 경화 |
| (17)–(20) | `ψ_mech = ½E_e·C E_e`, `S = C E_e`, `P = F_e F_c S F_p^T` |
| (21) | **`μ_mech = −(1/C_max) F_c S · ∂V_c/∂θ`** — 응력이 화학퍼텐셜에 되먹이는 항 |
| (22) | `E_O[V_O] = E_total[V_O] − E_total[P] + μ_O` — 산소공공 형성에너지 (원자 계산은 인용) |

`[해석]` **식 (21) 이 이 모델의 핵심 커플링**이다 — 응력이 Li 화학퍼텐셜을 바꾸므로
역학이 전압에 들어온다. 우리 좌표로 옮기면: **OCV 자체가 응력 의존**이 된다. 액체셀
축의 [[halfcell-ocp-shape-invariance]]("모양 불변") 가정이 ASSB 에서 깨지는 **두 번째
경로**다 (첫 번째는 2호의 동역학 항). ⚠ 단 **논문은 이 효과의 크기를 따로 보고하지
않는다** — `μ_mech` 를 끈 대조군이 없다.

수치해법 `[인쇄]`: DAMASK **v2.0.2** 안에 구현, **PETSc 기반 대규모 병렬 유한요소
솔버를 developed**, 약형식 (23)–(26), 후진 오일러 (27), 두 장(변형·화학퍼텐셜)을
**staggered** 로 자기일관 반복, 역학은 inexact Newton + secant line search, 확산은
Newton + backtracking, 선형해는 **flexible GMRES + smoothed-aggregation AMG**.

---

## 5. Methods — 파라미터화 (p14 + Table S1)

| 무엇 | 출처 | 값 |
|---|---|---|
| 화학 자유에너지 `E₁`, `E₁₁` | **GITT OCV 적합** (ref 18 = Märker et al., *Chem. Mater.* 2019) | `E₁ = −4.15×10⁵`, `E₁₁ = 3.8×10⁴` J mol⁻¹ |
| `C_max` | ref 56 | **49 200 mol m⁻³** |
| 확산계수 `D_Li(θ)` | **고체 NMR** (refs 18,57), 5 차 지수 다항 적합 (식 31) | `D_ref = 1×10⁻⁸`, `D₀..D₅ = −17.94, 202.3, −782.6, 1483, −1362, 473.6` |
| 격자 치수 변화 `ν_{a,b}(θ)`, `ν_c(θ)` | **operando 싱크로트론 XRD** (refs 8,18,19), 5 차·4 차 다항 | 계수 SI Table S1 |
| 결정소성 | **압입 시험** (ref 112 = Stallard et al. 2022) | `γ̇₀ = 1×10⁻³ s⁻¹`, `n = 20`, `g₀ = 39 MPa`, `g∞ = 86 MPa`, `a = 2.25`, `h₀ = 75 MPa`, `h_αβ = 1` |
| NMC811 탄성상수 (리튬화) | 나노압입 + 제일원리 (refs 58–60) | `C₁₁ 1.95e11`, `C₃₃ 1.77e11`, `C₄₄ 7.41e10`, `C₁₂ 1.34e11`, `C₁₃ 1.19e10` Pa |
| NMC811 (탈리튬) | 〃 | `C₁₁ 2.8e11`, `C₃₃ 1.8e10`, `C₄₄ 1.5e10`, `C₁₂ 7.5e10`, `C₁₃ 0.8e10` Pa |
| 산화물 SE | refs 10,11 (LLZO·LLTO) | `C₁₁ 1.97e11`, `C₁₂ 8.03e10`, `C₄₄ 5.81e10` Pa |
| 황화물 SE | ref 12 | `C₁₁ 3.87e10`, `C₁₂ 1.58e10`, `C₄₄ 1.14e10` Pa |
| 폴리머 SE | ref 13 (PVC–PEO) | `C₁₁ 1.31e9`, `C₁₂ 5.35e8`, `C₄₄ 3.88e8` Pa |

★ `[재현]` 등방 근사 `E = (C₁₁−C₁₂)(C₁₁+2C₁₂)/(C₁₁+C₁₂)` 로 SE 의 Young 률을 계산하면
**산화물 150 GPa · 황화물 29.5 GPa · 폴리머 1.0 GPa** 이고, 이것이 Fig. 4f 의 x 축 위치
(`[도표]` ≈150 · ≈30 · ≈1)와 **정확히 맞는다**. → Fig. 4f 의 x 축은 SE 의 Young 률이 맞다.

★★ **Fig. 3c 의 범례 색이 Table S1 과 뒤바뀌어 있다** (§13 D1). `[도표]` Fig. 3c 에서
주황 막대는 `C₃₃ ≈178, C₄₄ ≈74, C₁₂ ≈134, C₁₃ ≈12` 로 **Table S1 의 리튬화 값**인데
범례는 주황을 **"Fully delithiated"** 라고 적는다. 파랑 막대는 `C₃₃ ≈18, C₄₄ ≈15,
C₁₂ ≈74, C₁₃ ≈8` = **탈리튬 값**인데 **"Fully lithiated"** 라고 적혀 있다. 5 쌍 중 4 쌍에서
확인된다. **독립 확인**: Fig. 6a 의 방향별 탄성률 곡면(리튬화 = 둥근 덩어리, 탈리튬 =
납작한 4 엽 별, 눈금 18–260 GPa)은 **Table S1 과 일치**한다 — 즉 **틀린 것은 Fig. 3c 의
범례**다. (`[해석]` Fig. 6a 와 Table S1 은 서로 다른 두 경로이므로 이 확인은 독립이다.)

`[인쇄]` "The elastic stiffness at a **fully lithiated state was used here**" — 즉 기본
계산은 리튬화 상수 고정이고, 탈리튬 상수는 Fig. 6a,b 의 **감도 시험에서만** 쓰인다.

---

## 6. ★ 코드·데이터 가용성 — 재현 가능성 원장 (p14–p15)

`[인쇄]` 그대로:

> "The open-source code for **DAMASK v2.0.2** version is available at
> `https://github.com/damask-multiphysics/DAMASK/tree/v2.0.2`. **The specific code used in
> this study can be accessed at** `https://git.damask-multiphysics.org` (branch:
> **plasticity_chemo_mechanics**, commit: **a987e05f8241fb1ef7d8ff913769ea09ac2cd1a3**)
> **with the permission of Max-Planck-Institut für Eisenforschung GmbH.** Access to the
> repository requires **registration via email at damask-CLA@mpie.de and approval of the
> Contributor Licence Agreement.**"

`[인쇄]` Data availability: "All data to evaluate the conclusions are present in the
manuscript, and the Supplementary Material. **Raw data are available from the corresponding
authors on request.**"

★ 이 위키가 세어 온 계열 — **"재현 가능하다고 적혀 있는데 접근 가능한 것은 다른
것"** — 의 새 표본이다. 공개된 v2.0.2 를 **이 세션 계열에서 clone 해 훑은 결과**
(`[해석]`; 이 digest 는 그 확인을 인계받아 적는다 — 원 확인은 이 파일 밖에서 이뤄졌다):

| 확인 항목 | 결과 |
|---|---|
| `src/` 규모 | **71 파일 · 50 208 줄 Fortran**, 커밋 `7f0275eb`, **2018-05-22** (논문은 2024) |
| `lithium` · `intercalat` 문자열 | **0 건** — Li 화학이 아예 없다 |
| 화학종 수송 골격 | Cahn–Hilliard 는 있다 (`vacancyflux_cahnhilliard`, `hydrogenflux_cahnhilliard`) |
| 독립 FEM 솔버 | **없다** — spectral 솔버 + 상용코드(Marc/Abaqus) 인터페이스뿐. 논문은 PETSc 기반 대규모 병렬 **FEM 솔버를 "developed"** 라고 적는다 |
| 라이선스 | **GPL** |

`[해석]` 즉 **공개 저장소에는 이 논문의 물리(Li 삽입 화학–역학)도, 이 논문이 만들었다고
한 솔버도 없다.** 실제 코드는 별 저장소 + **기관 허가 + CLA 승인**이 있어야 한다.
Nature Communications 의 "Code availability" 절이 형식상 채워졌지만 **재현 경로는
닫혀 있다.** 우리 저장소의 인용 게이트 기준(`provenance-fail-closed-verification`)으로
보면 이것은 **fail-open** 이다.

⚠ **주의**: 이것은 저자의 부정직을 뜻하지 않는다. CLA 는 MPIE 의 기관 정책이고 논문이
그 사실을 **정확히 밝혔다**. 원장에 남기는 것은 **"밝혔다"와 "재현된다"가 다르다**는
관측이며, 우리 자신에게도 같은 잣대를 댄다.

---

## 7. RESULTS 1 — 이방성·농도의존 물성의 역할 (p4–p5, Fig. 3)

설정: `[인쇄]` NMC811 **지름 12 µm**, **Li₆.₆La₃Ta₀.₄Zr₁.₆O₁₂**(Ta 치환 LLZO) 안에 박힘.
세 경우: (i) 등방·상수 물성, (ii) 단결정, (iii) 다결정(이방·농도의존).

**입력 곡선 (직접 봤다)**
- `[도표]` **Fig. 3a**: `D_Li` 가 `θ ≈ 0.35–0.5` 에서 ≈13×10⁻¹² cm² s⁻¹ 로 봉우리, `θ > 0.8`
  에서 급락. `[인쇄]` "drops sharply, **over two orders of magnitude**, as the Li content
  exceeds 80 %".
- `[도표]` **Fig. 3b**: 격자 `a` 는 `θ=0.1`→`1` 에서 0 → **+2.1 %** 단조 증가,
  격자 `c` 는 `θ≈0.35` 에서 **+4.05 %** 봉우리 후 `θ=1` 에서 **+1.95 %** 로 붕괴.
  XRD 점과 모델선이 거의 겹친다. `[재현]` 부피변화 = `1.021²×1.0195 − 1` ≈ **6.3 %**
  (서론의 7.8 % 와 다르다, §13 D8).
- `[도표]` **Fig. 3c**: 위 §5 의 **범례 뒤바뀜** 항목.

**결과**
- `[도표]` **Fig. 3d–g** (θ=0.5 단면): 등방은 매끈한 동심 분포. 단결정은 **basal 면
  방향성** 때문에 Li 가 적도 띠로 들어오고 전단이 **X 자**로 집중. 다결정은 Li 분포가
  **울퉁불퉁**하고 전단이 **입계를 따라** 망을 이룬다. 충전(g)에서는 입계 전단이 훨씬
  강하고 응력도 커진다.
- `[도표]` **Fig. 3h** (1C, x 축은 **정규화 용량이 아니라 `θ`**): 3 V 컷오프 도달 시
  `θ_end ≈` 등방 **0.88** · 단결정 **0.77** · 다결정 **0.71**. 충전 곡선(다결정)은
  방전보다 위에 있고 3.6 V 에서 끝난다.
  `[재현]` `(θ_end − 0.1)/0.89` → 0.876 / 0.753 / 0.685 → 등방 대비 손실 **0.123 · 0.191**
  ≈ `[인쇄]` "**0.12** for single crystal … **0.18** for polycrystal cathodes at 1 C,
  comparing to the isotropic case". ✔ **정합** — 그리고 이것이 Fig. 3h 의 `θ` 축을
  용량 축으로 바꾸는 **변환 규칙**을 확정해 준다.
- `[도표]` **Fig. 3i** (1C, θ=0.5): 가장자리로부터 거리별 평균 전단. 다결정 방전은
  **1.5 µm 에서 ≈0.12 봉우리**, 다결정 충전은 **가장자리에서 ≈0.147**, 단결정 방전은
  **가장자리 ≈0.055** 후 단조 감소. 6 µm(중심)에서 셋 다 ≈0.
  ⚠ `[해석]` 본문은 `[인쇄]` "accumulate prominently near the **exterior**" 라고 하지만
  다결정 방전의 최대는 **표면이 아니라 1.5 µm 안쪽**이다.
- `[도표]` **Fig. 3j** (상자+바이올린, 계면 최대주응력): 등방 중앙값 ≈0.2 GPa(아주 좁음) ·
  단결정 ≈0.55 (−1.8 ~ +2.3) · 다결정 방전 ≈0.35 (−1.0 ~ +1.9) · **다결정 충전 ≈1.65
  (최대 >4 GPa)**.
  ★ `[해석]` 이 "statistical variability" 는 **한 구조 안의 계면 점들에 대한 공간 분포**
  이지 **구조 실현 간 산포가 아니다.** 1호가 준 종류의 산포(무작위 배열을 바꿔 가며 잰
  폭)는 이 논문에 **없다**.

---

## 8. RESULTS 2 — 미시구조와 운전조건 (p5–p6, Fig. 4 · S4 · S5 · S6 · S7)

★ **Fig. 4a — 이 계보 최초의 "모델 vs 측정" 전압–용량 대조** (직접 봤다):

| 율 | 전류밀도 `[인쇄]` | 실험 종점 `[도표]` | 모델 종점 `[도표]` |
|---|---|---|---|
| 0.1C | 0.2 mA cm⁻² | ≈0.98 | ≈0.99 |
| 0.5C | 1 mA cm⁻² | ≈0.81 | ≈0.855 |
| 1C | 2 mA cm⁻² | ≈0.685 | ≈0.68 |
| 2C | 4 mA cm⁻² | ≈0.49 | ≈0.53 |

`[재현]` 2 mA cm⁻² = 1C ⇒ **면적 용량 2 mAh cm⁻²**.
`[인쇄]` "The **good agreement** between simulations and experiments confirms the
effectiveness of the developed physics-based chemo-mechanical model."
⚠ `[해석]` 저율에서 모델이 실험보다 **위**(0.5C 에서 +0.045, 2C 에서 +0.04)이고 곡선
모양(중간 전압대)도 다르다. "good agreement" 는 정성적 표현이고 **잔차·오차 지표가
하나도 없다.** 그리고 실험 출처(ref 62)는 **Si 음극 + 황화물 SE** 셀이다 (§13 D11).

★★ **Fig. S4 — 율 × 입자크기 전압곡선 20 장** (직접 봤다). 3 V 컷오프 정규화 용량:

| | 2 µm | 4 µm | 8 µm | 12 µm |
|---|---|---|---|---|
| **0.25C** | ≈0.99 | ≈0.98 | ≈0.98 | **≈0.95** |
| 0.5C | ≈0.99 | ≈0.98 | ≈0.96 | ≈0.83 |
| 1C | ≈0.96 | ≈0.945 | ≈0.90 | **≈0.69** |
| 2C | ≈0.97 | ≈0.95 | ≈0.80 | ≈0.62 |
| 5C | ≈0.95 | ≈0.86 | ≈0.60 | **≈0.35** |

(전부 `[도표]`, ±0.02. 2C 열의 2 µm 이 1C 보다 높게 읽히는 것은 읽기 오차로 본다.)

★★★ `[해석]` **이것이 [[assb-apparent-capacity-decomposition]] 이 예언한 그림이다.**
`i → 0` 에서 **모든 크기의 곡선이 ≈1 로 수렴한다.** 이 모델에는 재료 손실도(첫 방전에는
없다) 기하 손실도(`θ_AM ≡ 1`) 없으므로, **관측된 용량 손실 전부가 `η(i)` 한 항**이고
그것이 율과 함께 사라진다. → **3 항 분해의 "율이 동역학 항만 지운다" 가 독립 모델에서
확인됐다** (2호에서는 두 문장에서 추론만 했다).

- `[도표]` **Fig. 4b** (다결정 용량 등고선, x=C-rate 0.5–5, y=입자 2–12 µm): 등고선
  0.95 / 0.90 / 0.80 / 0.70 / 0.60. 좌하(작은 입자·저율) 빨강 ≈1.0, 우상 파랑 ≈0.4.
- `[도표]` **Fig. S5** (단결정판): 등고선 0.99 / 0.90 / 0.81 / 0.71 / 0.61 / 0.50 / 0.40.
  같은 (5C, 12 µm) 에서 단결정 <0.40, 다결정 ≈0.35–0.4 — **크게 다르지 않다**.
- `[도표]` **Fig. 4c** (전단 vs Li 농도 산점도, 1C): 단결정(주황)은 Li 농도와 **양의
  상관**(점선 추세, 최대 ≈0.1), 다결정(파랑)은 **Li 농도와 무관하게 0.35 까지 흩어진다**.
  `[인쇄]` "relatively high dislocation activity is observed in the polycrystalline
  particle, **irrespective of Li content**."
- `[도표]` **Fig. 4d**: 다결정 전단은 0.25C 에서 **입자 전체에 넓게** ≈0.05 (5C 는
  가장자리 0.088 후 급감), 단결정은 5C 0.094 → 0.25C 0.025 로 **율에 단조**.
  ★ `[해석]` **다결정에서는 저율이 전위를 줄이지 못한다** — 저율 곡선이 2 µm 이후로
  오히려 고율 곡선 **위**에 있다. 이것이 "율을 낮추는 것이 해가 아니다" 의 실체다.
  ⚠ 이 패널에는 **SOC 라벨이 없다** (§13 D12).
- `[도표]` **Fig. 4e** (계면 최대주응력 분포, θ=0.2): 다결정 5C/0.25C, 단결정 5C/0.25C
  네 경우의 중앙값이 모두 ≈0.7–0.9 GPa, 범위 −2 ~ +3.5 GPa. **율을 20 배 바꿔도 거의
  안 움직인다.** `[인쇄]` "the reduction of the discharge rate is **not a solution** for
  alleviating this persistent tensile stress at interfaces."
- `[도표]` **Fig. 4f**: SE Young 률(1 → 30 → 150 GPa)에 따라 **계면 응력**(파랑, 왼 축)은
  ≈0.05 → 0.28 → 0.38 GPa(리튬화) / 0.55 GPa(탈리튬)로 **증가**하고, **벌크 응력**(보라,
  오른 축)은 +0.75 → −0.2 → −1.5 GPa 로 **감소(압축화)** 한다. `[인쇄]` 산화물 전해질에서
  평균 계면응력이 **방전 378 MPa → 충전 580 MPa**. ✔ 도표와 일치(0.38/0.58 GPa).

★ `[해석]` **Fig. 4f 가 이 논문에서 우리에게 가장 쓸모 있는 그림이다**: 같은 양극·같은
운전조건에서 **전해질 물성만 바꿔도 계면 응력이 8 배** 달라진다. 접촉 손실이 응력의
함수라면, **`θ(N)` 은 양극의 성질이 아니라 (양극 × 전해질) 쌍의 성질**이다.
→ 우리 forward model 에 `θ` 를 넣을 때 **전해질을 상태변수에 넣어야 한다.**

---

## 9. RESULTS 3 — 전위 유발 구조열화와 용량 손실 (p7–p8, Fig. 5)

- `[도표]` **Fig. 5b**: 방전 후 소성전단 분포(왼쪽)와 그로부터 나온 **rock-salt 상**
  (오른쪽, 진홍). rock-salt 는 **입계를 따라 망 모양**으로 표면뿐 아니라 **내부 깊숙이**
  분포한다.
- `[도표]` **Fig. 5c**: 모델(검정, 상단축 = **O vacancy fraction %**)과 실험(진홍 ×,
  하단축 = **Mn³⁺ fraction %**)을 **서로 다른 두 축에 겹쳐** 놓았다. 둘 다 가장자리
  (거리 0)에서 최대(≈25–30 % / ≈25 %)이고 0.2 안쪽부터 평평(≈13–17 % / ≈13 %).
  ⚠ `[해석]` **다른 양·다른 화학(ref 5 는 Li-rich)** 을 축 눈금을 맞춰 겹친 것이다.
  정성적 일치 이상으로 읽으면 안 된다 (§13 D9).
- ★★ `[도표]` **Fig. 5d/e/f — 이 논문의 분해**:

| C-rate | | 0.25C | 0.5C | 1C | 2C | 5C |
|---|---|---|---|---|---|---|
| **5d 총 정규화 용량 손실** | 12 µm | 0.165 | 0.175 | 0.235 | 0.285 | **0.475** |
| | 8 µm | 0.145 | 0.17 | 0.205 | 0.215 | 0.39 |
| | 4 µm | 0.10 | 0.105 | 0.105 | 0.11 | 0.155 |
| | 2 µm | 0.085 | 0.083 | 0.08 | 0.072 | 0.095 |
| **5e 활물질 손실**(열역학) | 12 µm | 0.093 | 0.10 | 0.125 | 0.13 | **0.185** |
| | 8 µm | 0.088 | 0.10 | 0.115 | 0.128 | 0.163 |
| | 4 µm | 0.078 | 0.078 | 0.08 | 0.078 | 0.132 |
| | 2 µm | 0.078 | 0.077 | 0.075 | 0.067 | 0.088 |
| **5f 동역학 용량 손실** | 12 µm | 0.045 | 0.078 | 0.135 | 0.16 | **0.29** |
| | 8 µm | 0.04 | 0.075 | 0.105 | 0.11 | 0.225 |
| | 4 µm | ≈0.02 | ≈0.02 | ≈0.02 | ≈0.02 | ≈0.025 |
| | 2 µm | ≈0.012 | ≈0.012 | ≈0.01 | ≈0.01 | ≈0.01 |

`[재현]` **가법성 확인**: 12 µm·5C 에서 `0.185 + 0.29 = 0.475` = 5d 값. ✔
→ **`총 손실 = 활물질 손실 + 동역학 손실`** 이 그림 안에서 성립한다.

- `[도표]` **Fig. 5e 의 실험점**(별 9 µm · 마름모 11 µm · 삼각 16 µm, refs 67–71):
  0.15C ≈0.03 → 0.5C ≈0.083 → 6C ≈0.16 → 9C ≈0.20 (9 µm), 3C 에서 11 µm ≈0.166 ·
  16 µm ≈0.22. `[인쇄]` "increasing the charging rate from **0.5 C to 6 C** leads to an
  increase in the loss of active material from **8.5 % to 16 %**." ✔ 도표와 일치.
- ★★ `[인쇄]` **"the experimental analysis of active cathode material loss generally
  involves the formation of rock-salt phase AND isolated cathode materials induced by
  intergranular fracture. Since this study does not explicitly consider crack formation,
  only qualitative comparisons are made."**

  ★ `[해석]` **이 한 문장이 닻 질문의 심장이다.** 논문이 스스로 인쇄한다 —
  **실험이 보고하는 "활물질 손실" 은 (진짜 재료 손실) + (기하적 고립 = 접촉 손실)의
  합이고, 그 둘은 그 측정으로 안 갈라진다.** 우리가 `LAM_PE ↔ 접촉 손실` 이라고 부르는
  축퇴가 **그대로 인쇄됐다.** 그리고 이 논문은 그중 **앞 항만** 모델링하면서 뒤 항까지
  포함한 실험값과 대조한다 — 즉 **모델이 체계적으로 과소예측해야 정상**인데 Fig. 5e 의
  모델선과 실험점은 겹친다.
- `[인쇄]` 8 µm 초과 · 1C 초과에서 **활물질 10 % 이상 손실**, 총 손실 **0.2–0.4**.
- `[인쇄]` ref 71: 평균 11 µm 입자 셀의 용량감쇠가 16 µm 셀의 **22.1 % → 16.6 %**.
  ⚠ 이 실험들(refs 67–71)은 **전부 액체 전해질 Li-ion 셀**이다 (§13 D10).

---

## 10. RESULTS 4 — "모델 개발에 대한 예비 통찰" 절 (p8–p10, Fig. 6)

이 절은 사실상 **한계 목록 + 감도 시험**이다. `[인쇄]` 단순화·무시한 것:
계면·입계 **균열 생성**, **농도 의존 탄성률**, 고체전해질의 **소성**, 이산 전위와
입계의 Li 확산 역할, 현미경 자료로부터의 미시구조 생성.

1. **균열.** `[인쇄]` "Loss of interfacial contact within the cell **obstructs Li transport**
   … which subsequently results in **resistance increase, capacity loss, and rate
   performance deterioration**. While this study effectively captures the heterogeneous
   stress response …, **it does not account for crack formation.**" 넣는 방법으로
   cohesive zone · spring analogy · continuum damage · phase-field damage 를 나열한다.
2. **농도 의존 탄성률.** `[도표]` Fig. 6a,b: 탈리튬 상수를 쓰면 전단 분포 봉우리가
   `[인쇄]` **0.09 → ≈0.03** 으로 줄지만, **계면 최대주응력 분포는 거의 안 변한다**.
3. **SE 소성.** J2 소성, 항복강도 `[인쇄]` 산화물 **2 GPa** · 결정성 황화물 **450 MPa** ·
   비정질 황화물 **200 MPa**. `[도표]` Fig. 6d: 산화물은 영향 없음(곡선 완전 겹침).
   `[도표]` Fig. 6f: 황화물은 **전단 분포는 그대로**인데 **계면 응력 분포가 통째로
   왼쪽으로** 이동(봉우리 +0.25 → 0.0 → −0.25 GPa). ★ **인장이 압축으로 바뀐다.**
4. **입계 확산.** `D_GB = 0.05 ~ 20 × D_bulk`, 입계는 `[인쇄]` "two layers of elements".
   ★ `[도표]` **Fig. 6h** (1C, 정규화 용량 종점):

   | `D_GB/D_bulk` | 0.05 | 0.1 | 0.2 | **1** | 5 | 10 | 20 |
   |---|---|---|---|---|---|---|---|
   | 정규화 용량 | ≈0.48 | ≈0.55 | ≈0.615 | **≈0.68** | ≈0.93 | ≈0.96 | ≈0.985 |

   `[인쇄]` "A **fivefold increase** in Li diffusivity along grain boundaries results in a
   **20 % increase** in capacity, while a corresponding fivefold decrease leads to an
   **8 % capacity fade**."
   ⚠ `[재현]` 도표로는 5 배 증가가 `0.93 − 0.68 = +0.25` (**+25 %p**, 상대 +37 %)이고
   5 배 감소가 `0.68 − 0.615 = −0.065` (**−6.5 %p**). **감소 쪽은 맞고 증가 쪽이 안 맞는다**
   (§13 D7).
   `[도표]` Fig. 6g vs 6i: `0.1 D_bulk` 는 중심이 새파랗게(Li 결핍) 남고, `10 D_bulk` 는
   입자 전체가 균일해진다. **계면 응력은 두 경우 모두 그대로** (`[인쇄]` "high tensile
   stresses exist at the interfaces … **regardless of** Li transport kinetics along grain
   boundaries").
   `[인쇄]` 실험 대조: 입계에 고체전해질을 넣으면 200 사이클 후 용량유지가
   **79 % → 91.6 %** (ref 84 — 남의 실험, **액체셀**).

★★ `[해석]` **입계 확산도가 용량을 0.48 ↔ 0.985 로 두 배 넘게 흔든다.** 재료도 기하도
같은데 **겉보기 용량이 2 배**다. 이것은 2호의 `R_GB` 반례(입계 저항만으로 겉보기
`LAM_PE` 72 %)와 **같은 종류의 관측이 다른 길이척도(이차입자 내부 입계)에서 재현된 것**
이다. → **`η(i)` 의 지배 인자가 전극 척도(2호)와 입자 척도(3호) 둘 다에 있다.**

---

## 11. Discussion (p10–p12, Fig. 7)

- `[인쇄]` NMC111 은 ≈4.6 V, **NMC811 은 ≈4.2 V** 부터 산소 손실이 시작된다(refs 88,89).
- `[인쇄]` 처방: **이차입자 지름 4 µm 미만**, **단결정 양극**, **복합 도핑(Ti, Mg, Nb, Mo)**,
  **하이브리드 전해질(산화물 + 폴리머)**.
- `[인쇄]` "Reducing the diameter of secondary particles **from 9 µm to below 4 µm** enables
  the increase of the discharge rate **from 1 C to 5 C** while maintaining the **same 90 %
  usable capacity**."
- `[도표]` **Fig. 7a** ("10 % kinetics-related capacity loss" 등고선): 경계가
  (0.4C, 12 µm) → (1C, 9 µm) → (2C, 6 µm) → (5C, ≈3.7 µm). **다결정(검정)과 단결정(빨강)이
  거의 겹친다.**
- `[도표]` **Fig. 7b** ("10 % active materials loss" 등고선, 다결정만): (0.45C, 12 µm) →
  (3C, ≈4 µm) → (5C, ≈2.5 µm). **단결정은 별표 하나로 우상단(≈4.8C, 11.5 µm)에 찍혀 있다**
  — 즉 `[해석]` **단결정은 이 창 안에서 10 % 활물질 손실에 도달하지 않는다.**
- ★★ ⚠ **두 패널 모두 채워진 영역에 "Operating window, ≥ 90 % usable capacity" 라고
  적혀 있는데, 두 손실은 가법이다**(§9 의 5d = 5e + 5f). 예: 8 µm·0.5C 는 두 창에 **모두**
  들어가지만 Fig. 5d 의 총 손실이 `[도표]` ≈0.17 → **사용 가능 용량 83 %** 다.
  **라벨이 자기 그림(5d)과 어긋난다** (§13 D6). 그리고 위 인쇄 문장의 "same 90 % usable
  capacity" 는 Fig. 7a 안에서만 성립한다 — 4 µm·5C 의 총 손실은 `[도표]` **0.155**
  (사용 가능 84.5 %).
- `[도표]` **Fig. 7c** (벌크 응력 vs 계면 응력, 점 = 0.25C~5C 스윕): 세 무리가 **직선상에
  반비례**한다 — 폴리머(계면 ≈0.03–0.07 GPa, 벌크 **+0.35~+0.55**) · 황화물(≈0.25–0.35,
  **−0.1~−0.25**) · 산화물(0.5–0.95, **−1.0~−1.7**). 같은 무리 안에서 **율에 따른 산포는
  작다.** 단결정(○)이 다결정(×)보다 **계면 응력이 높다**(산화물에서 0.72–0.92 vs 0.5–0.6).
  `[인쇄]` "using a **single type** of solid electrolytes **cannot simultaneously mitigate**
  the large tensile stress buildup in NMC cathodes and on the interfaces" → 하이브리드 제안.
  ⚠ `[해석]` **단결정이 계면 응력에서 더 나쁘다는 것은 본문이 말하지 않는다** — 본문의
  처방("단결정을 써라")과 이 그림이 **같은 방향이 아니다.**
- `[인쇄]` 결론 요지: "Ni-rich cathodes experience extensive dislocation formation
  (**over 12 % plastic shear locally**) during discharge … **Reduction in current densities
  proves insufficient** to alleviate the persistent tensile stress and contact loss at the
  interface."

---

## 12. 그림별 열람 기록 (무엇을 봤고 무엇을 안 봤나)

| 그림 | 봤나 | 비고 |
|---|---|---|
| Fig. 1 (개념도) | **아니오** | 캡션만. 결론을 떠받치지 않는다 |
| Fig. 2 (워크플로) | **아니오** | 본문 서술이 패널을 전부 설명한다 |
| **Fig. 3 (a–j)** | **예** | 전문 + `fig_3c.png` 확대 |
| **Fig. 4 (a–f)** | **예** | 쪽 렌더 + `fig_4a.png` 확대 |
| **Fig. 5 (a–f)** | **예** | 전문 + `fig_5def.png` 확대 |
| **Fig. 6 (a–j)** | **예** | 자동 크롭은 g,i 만 잡혀서 쪽 렌더 + `fig_6h.png` 확대 |
| **Fig. 7 (a–d)** | **예** | 쪽 렌더 |
| **Fig. S1, S2, S3, S4, S5, S8** | **예** | 쪽 렌더 |
| Fig. S6, S7 | **아니오** | 캡션만 (Fig. 4d,e 의 3D 판) |
| Table S1 | **예** (텍스트) | 이미지로 읽지 않았다 — PDF 텍스트가 정확 |

---

## 13. 본문 · 그림 · 캡션 어긋남 원장 (18 건)

| # | 무게 | 내용 |
|---|---|---|
| **D1** | **높음** | **Fig. 3c 의 범례 색이 Supplementary Table S1 과 뒤바뀌었다.** `[도표]` 주황 = `C₃₃178/C₄₄74/C₁₂134/C₁₃12` = **표의 리튬화 값**인데 범례는 "Fully delithiated". 5 쌍 중 4 쌍에서 확인. **독립 확인**: Fig. 6a 의 탄성률 곡면(18–260 GPa)은 표와 일치 → 틀린 것은 Fig. 3c 범례. 파급: 본문 `[인쇄]` "delithiation results in a **reduction** of the elastic modulus (Fig. 3c)" 는 표 기준으로도 `C₁₁` (195 → 280 GPa, **증가**)에 대해 틀리다 |
| **D2** | 중간 | 초록의 **`393 Wh kg⁻¹`** — **출처 없음**, 본문 재등장 **0 회**. 이 논문의 유일한 셀 수준 수치다 |
| **D3** | **높음** | 초록·결론이 `[인쇄]` "**contact loss is caused by** the micromechanics …" 라고 단정하지만, 본문이 `[인쇄]` "the current model **does not explicitly account for mechanical fracture**" 라고 적는다. **모델에 접촉 손실 변수가 없다** — 응력뿐 |
| **D4** | **높음** | **Fig. 5d–f 의 손실 기준이 방전 곡선과 화해되지 않는다.** 12 µm·1C: Fig. 4a/S4c/6h/3h 는 정규화 용량 `[도표]` ≈0.68–0.69 (손실 ≈0.31)인데 Fig. 5d 의 "total normalised capacity loss" 는 `[도표]` ≈0.235. **기준이 원문 어디에도 없다** |
| **D5** | **높음** | **"kinetically induced capacity loss" 가 세 곳에서 다른 뜻이다.** Methods `[인쇄]` "arises from **non-uniform Li distribution**" / Fig. 5f 캡션 `[인쇄]` "arising from the **impediment of Li-ion intercalation pathways**"(= 열화 후) / Fig. 7a 캡션 `[인쇄]` "due to **anisotropic and concentration-dependent diffusion**". 값도 다르다 (12 µm·1C: 0.31 vs 0.135) |
| **D6** | **높음** | **Fig. 7a·7b 의 "Operating window, ≥ 90 % usable capacity" 라벨이 Fig. 5d 와 모순.** 두 손실이 가법인데 각 패널은 **한 성분만** 10 % 로 자른다. 8 µm·0.5C 는 두 창 모두 안쪽이지만 총 손실 `[도표]` ≈0.17 (사용 가능 83 %). 4 µm·5C 도 0.155 (84.5 %) |
| **D7** | 중간 | `[인쇄]` "fivefold increase … **20 % increase** in capacity" vs `[도표]` Fig. 6h `0.68 → 0.93` = **+25 %p** (상대 +37 %). 5 배 감소(−8 %)는 도표(−6.5 %p)와 맞는다 |
| **D8** | 낮음 | 서론 `[인쇄]` NMC811 부피변화 **7.8 %** vs 자기 Fig. 3b 적합의 `[재현]` **≈6.3 %** (`1.021²×1.0195`) |
| **D9** | 중간 | **Fig. 5c 는 서로 다른 두 양을 두 x 축에 겹친다** — 모델은 **O vacancy fraction**, 실험은 **Mn³⁺ fraction**. 게다가 실험(ref 5)은 **Li-rich** 층상 산화물이고 모델은 **NMC811**. 12 % 전단 문턱도 이 자료에 맞췄다 |
| **D10** | **높음** | **Fig. 5e 의 실험점(refs 67–71)은 전부 액체 전해질 Li-ion 셀**이다 (Tanim 2019 · Chinnam 2021 · Strehle 2021 · Zhang 2017 · Song 2023). 논문 제목은 *solid-state* 이고 "활물질 손실" 축의 유일한 실측 대조가 이것이다 |
| **D11** | **높음** | **Fig. 4a 의 실험 곡선은 ref 62 = Tan et al., "Carbon-free high-loading silicon anodes enabled by sulfide solid electrolytes", *Science* 373 (2021)** 에서 왔다 — **Si 음극 + 황화물 SE**. 모델은 **LLZO + (음극 미모델링)**. 전압축이 4.5 V 까지 가는 것으로 보아 `[해석]` Li/Li⁺ 기준 양극 전위로 변환된 것 같은데 **변환 절차도 셀 구성도 논문에 없다** |
| **D12** | 낮음 | **Fig. 4d 에 SOC 라벨이 없다.** 같은 12 µm·1C·다결정인데 Fig. 3i(θ=0.5)의 최대 전단 `[도표]` 0.12 vs Fig. 4d 의 0.065. (SI S6/S7 이 "average Li site concentration 40 %" 라고 적으므로 θ=0.4 일 가능성 — 본문은 안 적는다) |
| **D13** | 낮음 | Table S1 단위 오식 2 건: `D_ref (m⁻²s⁻¹)` (→ `m² s⁻¹` 이어야) · `h_αβ (MPa) 1` (무차원 경화행렬) |
| **D14** | 낮음 | Table S1 이 `k_B (J mol⁻¹K⁻¹) 8.314` — **기호는 볼츠만, 값은 기체상수**. 본문은 `[인쇄]` "k_B is the **universal gas constant**" 라고 적으므로 계산은 일관하고 기호만 남용 |
| **D15** | 낮음 | `[인쇄]` 응력 없는 기준상태 `θ = 0.1` 또는 **0.9** vs 완전 리튬화 정의 `θ = **0.99**`. 두 수의 관계가 설명되지 않는다 |
| **D16** | **높음** | **코드 가용성**: 공개 `v2.0.2` ≠ 이 연구가 쓴 코드. 별 저장소 + 기관 허가 + CLA. 인계받은 확인에 따르면 공개본에는 `lithium`·`intercalat` 이 **0 건**이고 **독립 FEM 솔버도 없다** (§6) |
| **D17** | 낮음 | `[도표]` Fig. 4b 등고선으로 읽은 12 µm·1C ≈0.74 vs Fig. 4a/S4c 의 0.68–0.69. **내 읽기 오차(±0.2 C)** 안일 수 있다 — 약한 항목으로 남긴다 |
| **D18** | 낮음 | `[인쇄]` "1.06 eV → 0.24 eV" vs `[도표]` Fig. S3 막대 ≈1.07 → ≈0.21 eV |

★ 이 원장에서 **가장 무거운 것은 D3·D4·D5·D6 의 묶음**이다: 논문의 처방(Fig. 7 의 운전
창)이 **정의가 흔들리는 두 양** 위에 서 있고, 그중 하나(접촉 손실)는 **모델에 존재하지
않는다**. 2호에서 가장 무거웠던 어긋남과 **같은 형태**다 — 본문이 자기 그림과 충돌하는데
그 문장이 **결론을 떠받친다**.

---

## 14. 닻 질문 Q1–Q8 (`questions/assb-contact-loss-vs-lampe.md` 의 수집 지침)

| # | 이 논문의 답 |
|---|---|
| **Q1 접촉 손실 정량** | ⚠ **없다.** 접촉 손실의 **양(분율·면적)을 계산하지 않는다.** 대리로 **계면 최대주응력**(GPa) 분포를 준다 — 상자그림·바이올린·빈도분포로 네 그림(3j, 4e, 6b/d/f/j, 7c). **단위가 다르고(Pa vs 무차원)** 응력→분리 전환 규칙(임계응력·인성)이 없으므로 **`θ` 로 변환 불가**. 대신 `[인쇄]` 평균 계면응력 **378 MPa(방전) → 580 MPa(충전)**, 전해질 Young 률 1→150 GPa 에서 **0.05 → 0.55 GPa** |
| **Q2 독립 관측** | **없다** — **자기 실험 0 개** (3/3 편 공통). 인용 실험만: GITT OCV(ref 18) · NMR 확산(18,57) · XRD 격자(8,18,19) · 나노압입(58–60) · 방전곡선(62, **Si/황화물 셀**) · X선 현미경 산소결핍(5, **Li-rich**) · 활물질 손실(67–71, **액체셀**). ★ 그러나 **부정적 정보 하나가 값지다**: `[인쇄]` 실험의 활물질 손실은 rock-salt + **입계 파괴로 고립된 활물질**을 **둘 다 포함**한다 — 즉 **실험 라벨이 우리가 가르려는 두 항의 합임을 논문이 인정** |
| **Q3 라벨 층위** | **computed-mechanical + fitted-threshold.** 활물질 손실 라벨 = `소성전단 > 12 %` 영역의 부피분율이고, **12 %는 ref 5 의 실험 분포에 맞춘 값**(`[인쇄]` "by fitting"). **오차 막대 0 개 · 문턱 민감도 0 회 · 구조 실현 1 개** |
| **Q4 유일성·식별성** | **없다.** 순수 forward. `identifiab`·`uniqueness`·`uncertain` 각 **0 회**. → `assb` **3/3 편이 안 쟀다** |
| **Q5 Li-In 기준 전위** | **없다.** `indium` **0 회**. 음극을 **아예 모델링하지 않는다** — 전압은 양극 입자 표면 평균 전위(vs Li/Li⁺)다 |
| **Q6 압력** | **없다.** 작동 중 스택 압력 **0 회** (`pressure` 는 argyrodite 전도도 논의와 참고문헌 제목에만). → `assb` **3/3 편이 0 회**. ⚠ 접촉 역학을 정면으로 다루면서 **압력이 없다**는 것이 이 논문에서 가장 두드러진다 |
| **Q7 dead Li / SEI Li** | **없다.** 음극 없음 |
| **Q8 양극 화학 · OCP 기울기** | ★★ **있다, 그리고 이 계보 최초로 OCV 곡선이 들어왔다.** **NMC811**(+ Ta 치환 LLZO). `[도표]` **Fig. S2**: GITT 측정 OCV, `1−θ` 0 → 1 에서 **≈3.0 → 4.4 V vs Li/Li⁺**, `1−θ ≈ 0.05–0.35` 에서 완만한 어깨(≈3.5–3.75 V), 0.4–0.6 에서 기울기 꺾임, 이후 단조 상승. **전 구간 기울기가 있다**(LFP 형 평탄 구간 없음). 적합은 **2 파라미터 정규용액**(`E₁`, `E₁₁`)이고 `[도표]` 0.3–0.6 구간의 구조를 **못 따라간다**. 컷오프 **3.0 V**, 운전 상단 ≈4.3 V |

### 수집 현황 — 누적

| 논문 | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 |
|---|---|---|---|---|---|---|---|---|
| Bielefeld 2019 (1호) | 부분 (`θ`) | 없다 | computed-geometric | 없다 | 없다 | 없다 | 없다 | 부분 |
| Clausnitzer 2023 (2호) | 부분 (`Connectivity`) | 부분 (타 재료계 EIS) | computed × 2, 오차막대 0 | 없다 | 없다 | 없다 | 없다 | **있다**(전압축) |
| **Liu 2024 (3호)** | **없다** (응력 대리, 변환 불가) | **없다** (자기 실험 0) — 단 **"실험 라벨은 합"** 인쇄 | **fitted 문턱**(12 %, 타 화학에 적합) | **없다** | **없다** | **없다** | **★ 있다 — OCV 곡선 + 기울기** |

`[해석]` **누적 ≈2.5 → ≈3.0 칸.** 3호가 실제로 채운 칸은 **Q8 하나**(2호가 남긴 "OCV
곡선 0 편" 단서를 닫았다)이고, **Q3 에 새 층위("fitted 문턱")를 열었다.**
**Q4·Q5·Q6·Q7 은 3/3 편 0 이다.** 특히:

- **Q6(압력)**: 접촉 역학 논문이 압력을 안 쓴다 — `assb` 축의 "모두가 빠뜨린 변수"
  원장에서 가장 강한 항목이 됐다.
- **Q1**: 3 편이 **세 개의 다른 양**을 "접촉 손실" 이라 부른다 (기하 분율 · 연결성 ·
  계면 인장응력). **앞의 둘은 같은 양이고, 셋째는 다른 차원이다** (§15).

---

## 15. ★ 1호·2호와의 정면 대조 — 좌표 변환이 되는가

| 축 | Bielefeld 2019 (1호) | Clausnitzer 2023 (2호) | **Liu 2024 (3호)** |
|---|---|---|---|
| 길이척도 | **전극** (두께 20–140 µm, 수천 입자) | **전극** (50 µm, 25×25×50 복셀) | **입자 1 개** (2–12 µm) + 감싼 SE |
| 무엇이 랜덤인가 | 입자 충전 배열 | 입자 충전 배열 | **일차입자 결정 방위** (200 개) |
| 접촉 손실의 좌표 | `θ = V_c/V_ν` (무차원 분율) | `Connectivity = 1 − n_iso/n_tot` (무차원) | **최대주응력** (GPa) |
| 그 양의 시간축 | 없음 (pristine) | 없음 (방전 1 회) | **없음** (방전 1 회 + 충전 1 회) |
| 전압축 | **없음** | 있음 (부하 곡선) | **있음 + OCV 곡선** |
| 율 스윕 | 없음 | **없음** (단일 1 mA cm⁻²) | ★ **있음** (0.25–5C × 4 크기) |
| SE 안의 이온 수송 | 퍼콜레이션만 | **명시적**(굴곡도·입계저항) | ★ **아예 없음** |
| 역학 | 없음 | `[인쇄]` "does not incorporate mechanics" | **본체** |
| 파괴·디본딩 | 없음 | 없음 | **없음** (`[인쇄]` 명시) |
| 산포 보고 | **있음** (이봉 30 ↔ 70 %) | 없음 (점당 구조 1 개) | **없음** (실현 1 개) |

★★ `[해석]` **결론: 1·2호의 `θ` 와 3호의 응력은 같은 양이 아니고, 이 논문만으로는
변환도 안 된다.** 이유 셋:

1. **분모가 없다.** `θ` 는 분율이므로 "전체 활물질" 이라는 분모가 필요하다. 3호의 RVE 는
   입자 **1 개**이고 그 입자는 **정의상 집전체에 연결돼 있다**(탄소 바인더 가정) —
   `θ_AM ≡ 1` 인 세계다.
2. **차원이 다르다.** 응력(Pa) → 분리 분율(무차원) 변환에는 **파괴 판정 규칙**(임계
   응력·에너지 방출률·계면 인성)이 필요한데 **논문에 없다**. 논문 스스로 cohesive zone /
   phase-field damage 를 **앞으로 넣을 것**으로 나열한다.
3. **경계조건이 반대다.** 1·2호는 SE 를 **이온 전도 매질**로만 보고 역학이 없다.
   3호는 SE 를 **역학 매질**로만 보고 이온 수송이 없다. **두 모델은 서로의 영점에서
   작동한다.**

`[해석]` 그래도 **세 편을 한 식에 꽂을 자리는 있다** — [[assb-apparent-capacity-decomposition]]
의 3 항 분해에 3호를 넣으면:

```
Q_apparent = θ_AM(기하; 1·2호) · η(i; 전극 수송 2호 + 입자내 수송·입계 3호) · Q_material(3호가 갉아먹는 것)
                ↑ 3호에서는 ≡1                                                    ↑ 3호의 "loss of active materials"
```

★ **3호의 실제 기여는 `θ` 가 아니라 `Q_material` 쪽이다.** 이 논문은
**진짜 활물질 손실(재료가 rock-salt 로 바뀌어 없어지는 것)의 생성 기구와 그 율·크기
의존**을 준다 — 즉 **우리가 `LAM_PE` 라고 부르는 항의 물리**를. 그리고 그 항이
**율에 의존한다**는 것을 보여 준다 (Fig. 5e: 12 µm 에서 0.093 → 0.185, 0.25C → 5C).

⚠⚠ `[해석]` **이것이 우리 분리 시험에 붙는 새 제약이다.** [[assb-apparent-capacity-decomposition]]
의 처방은 "**최소 두 율에서 적합하고 `a_PE` 차이를 보면 동역학 성분의 하한이 나온다**"
였고, 그 전제는 **`Q_material` 과 `θ_AM` 이 율에 무관**하다는 것이었다. 3호가 그 전제의
절반을 깬다:

> **고율 방전 자체가 진짜 활물질 손실을 더 만든다** (`[도표]` Fig. 5e, 12 µm 에서
> 0.25C 0.093 → 5C 0.185, **2 배**). 즉 `Q_material = Q_material(i, N)` 이다.

→ **율 스윕 분리 시험은 "같은 셀에 두 율" 로는 안 된다.** 율을 바꾸는 행위가 라벨을
바꾼다. `[해석]` 살아남는 설계는 둘이다: (a) **낮은 율에서만** 두 점을 잡고 그 사이
차이를 쓰거나, (b) **율을 바꾼 뒤 다시 기준 율로 돌아와** 이력(hysteresis)을 재서
비가역분을 빼는 것. 후자가 더 안전하다. **이 제약은 3호가 없었으면 못 봤다.**

---

## 16. 우리 프로젝트에 대한 시사점 (전부 `[해석]`)

1. ★★ **`θ(N)` 은 여전히 0/3 이다. 그리고 이제 그 이유를 안다.** 세 편 모두
   **파괴·디본딩 모형이 없다.** 1·2호는 pristine 기하를 주고, 3호는 그 기하를 깨뜨릴
   **구동력**까지 주고 멈춘다. → **비어 있는 것은 논문이 아니라 모형의 한 조각**
   (cohesive zone / phase-field damage)이다. 이것은 **우리가 DEM 으로 메울 수 있는
   자리**이기도 하다 (`dem-mpm` 계열이 바로 그 조각을 갖고 있다).
2. ★★ **율 스윕 분리 시험이 좁아졌다** (§15 끝). `Q_material` 이 율 의존이므로 두 율의
   `a_PE` 차이는 **동역학 성분의 하한이 아니라 (동역학 + 율유발 재료손실)의 합**이다.
   → [[assb-apparent-capacity-decomposition]] 의 처방에 **"저율 쌍 또는 왕복 이력"**
   단서를 붙여야 한다.
3. ★ **`θ` 는 (양극 × 전해질) 쌍의 함수다** (Fig. 4f·7c). 폴리머 ↔ 산화물에서 계면
   응력이 **8 배** 다르다. → 우리 forward model 에서 접촉 손실을 넣을 때 **전해질 탄성률·
   항복강도가 상태변수**에 들어가야 한다. 이는 [[composite-cathode-percolation-utilization]]
   의 `θ` 를 **재료 쌍마다 다시 재야 한다**는 뜻이다 (그 페이지의 닫힌 형태는 SE 물성이
   없다).
4. ★ **OCV 가 처음 생겼다** (Fig. S2). `assb` 축에서 우리 아핀 창 매개화
   (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1)를 **처음으로 실물 곡선 위에서** 시험할
   수 있다. NMC811 OCP 는 전 구간 기울기가 있으므로 LFP 형 `(X1, X3)` 축퇴는 안 온다.
   ⚠ 단 이 OCV 는 **액체 반쪽전지 GITT**(ref 18)에서 온 것이고 ASSB 셀의 것이 아니다.
5. ★ **식 (21) 이 새 위험을 연다**: `μ_mech` 때문에 **OCV 자체가 응력 의존**이다.
   [[halfcell-ocp-shape-invariance]] 의 "모양 불변" 가정이 ASSB 에서 깨지는 **두 번째
   경로**(첫째는 2호의 동역학). ⚠ 논문이 크기를 안 재므로 **우리가 재야 한다** —
   `μ_mech` 항의 전압 기여는 우리가 싸게 추정할 수 있다 (`F_c S ∂V_c/∂θ / C_max`).
6. ★ **산포 규율이 3/3 편에서 안 지켜졌다.** 1호만 실현 간 폭을 쟀다. 3호는
   **"무작위 배열이 결정적"이라고 본문에 적고도 실현 1 개**다. → 우리가 N 개 실현으로
   **싸게 무효화/검증할 수 있는 자리**가 하나 더 늘었다 (Fig. 3j·4e 의 분포는 공간
   분포이지 실현 분포가 아니다).
7. ★ **"실험 활물질 손실 = 재료 손실 + 고립 손실" 이 인쇄됐다** (§9). 닻 질문이
   **문헌의 문장으로 확인**된 것은 이번이 처음이다. Evidence For 에 넣는다.
8. **재현 가능성 원장에 새 표본** (§6). 우리 파이프라인의 fail-closed 규율과 대비된다.
9. **입계가 `η` 의 지배 인자다** — 전극 척도(2호 `R_GB`)와 입자 척도(3호 `D_GB`) **둘 다**.
   `[도표]` 3호에서 `D_GB` 를 0.05 ↔ 20 배로 바꾸면 용량이 **0.48 ↔ 0.985**. 우리가
   합성 truth 를 만들 때 **입계 파라미터 하나가 겉보기 `LAM_PE` 를 절반으로 만든다**는
   뜻이고, 그것은 **OCV 로 안 보인다**.

---

## 17. 후속 논문 후보 (이 논문이 가리키는 것)

1. ★ **Koerver et al., *Chem. Mater.* 2017, 29, 5574** (여기 ref 7 · 1호 ref 7):
   "Capacity fade in solid-state batteries: interphase formation and chemomechanical
   processes in nickel-rich layered oxide cathodes and lithium thiophosphate solid
   electrolytes" — **접촉 손실의 실험 원전 + 용량축 + 사이클**. 3 편이 모두 인용한다.
   **`θ(N)` 을 얻을 유일한 길이 실험 쪽**임이 이제 분명하다.
2. ★ **Strauss et al., *ACS Energy Lett.* 2018, 3, 992** (여기 ref 90 · 1호 ref 13):
   1호가 `1 − θ_AM` 의 **measured 라벨** 후보로 지목했고 여기서도 입자 크기 논의에
   인용된다. **세 편의 공통 참조점.**
3. **Shin et al., *Adv. Energy Mater.* 2023, 13, 2301220** (여기 ref 11):
   "New consideration of degradation accelerating of all-solid-state batteries under a
   **low-pressure** condition" — **Q6(압력)을 채울 첫 후보**. `assb` 3/3 편 0 회인 축이다.
4. **Stallard et al., *Joule* 2022 (ref 100) / *JES* 2022, 169, 040511 (ref 112)**:
   양극 재료의 역학 물성 · NMC811 단결정 전단강도 — 3호의 소성 파라미터 원전.
5. **Xu et al., *Joule* 2022, 6, 2535 (ref 57)**: operando 가시화로 **입자 안 Li
   불균일**을 직접 본다 — `η(i)` 의 measured 라벨 후보.
6. 균열을 실제로 넣은 화학–역학 논문 (ref 43,44,72 계열, phase-field damage) —
   **`θ(N)` 을 계산으로 얻으려면 여기로 가야 한다**.

---

## 18. 이 digest 가 주장하지 않는 것

- **이 논문이 접촉 손실을 계산했다고 주장하지 않는다.** 계산한 것은 **계면 최대주응력**
  이고, 파괴·디본딩은 명시적으로 빠져 있다 (논문 스스로 인쇄).
- **`θ(N)` 을 얻었다고 주장하지 않는다.** 사이클 축은 없다.
- **Fig. 5d–f 의 숫자를 우리 좌표로 옮길 수 있다고 주장하지 않는다.** 기준이 미확정이다
  (§13 D4·D5). 그 전에 쓰면 안 된다.
- **D1(범례 뒤바뀜)을 저자의 계산 오류라고 주장하지 않는다.** Table S1 과 Fig. 6a 가
  일치하므로 **계산은 표대로 됐고 Fig. 3c 의 라벨만 틀렸을 가능성**이 가장 높다.
  (이 위키의 규칙: 원전이 스스로 예고한 것을 반증으로 쓰지 않는다 — 이 건은 원전이
  예고하지 않았고, 두 독립 경로로 확인했다.)
- **"good agreement"(Fig. 4a)를 검증이라고 주장하지 않는다.** 잔차 지표가 0 개이고
  대조 자료가 **다른 셀 화학**에서 왔다.
- 이 수치들은 **NMC811 이차입자 1 개 · LLZO(또는 황화물/폴리머) 매질 · 완전 접합 ·
  SE 이온수송 없음 · 방전 1 회 · 구조 실현 1 개**라는 한 모집단의 것이다.

---

## 관련 위키 페이지

- [[assb-contact-loss-vs-lampe]] — 닻. 이 digest 가 Q8 을 채우고 Q1 에 **다른 차원의 좌표**를 추가한다.
- [[assb-apparent-capacity-decomposition]] — 3 항 분해. 이 논문이 **율 스윕으로 `η(i)→1` 을
  직접 보여 주고**, 동시에 **`Q_material` 의 율 의존**으로 분리 시험에 단서를 붙인다.
- [[composite-cathode-percolation-utilization]] — `θ_AM`. 이 논문의 RVE 에서는 **`θ ≡ 1`**
  이고, 대신 `θ` 를 떨어뜨릴 **구동력(계면 응력)** 과 그것의 **전해질 의존**을 준다.
- [[halfcell-ocp-shape-invariance]] — 식 (21) `μ_mech` 가 여는 두 번째 파괴 경로.
- [[fitting-degeneracy]] · [[near-optimal-set-width-measurement]] — 이 논문은 forward
  전용이라 만나지 않은 문제.
