# 🗣 용어 대장 — 우리 말 → 필드 표준어 → 근거

> **왜 이 파일이 있나** (2026-08-06 신설)
> 발표·원고에서 **용어 하나가 틀리면 첫 질문에서 무너진다.** 우리끼리 쓰는 축약어를
> 그대로 슬라이드에 올리면 (a) 청중이 못 알아듣거나 (b) 아는 사람이 "그건 그 뜻이 아닌데" 로 잡는다.
> 그래서 **쓰는 말마다 필드 표준어와 근거를 짝지어 둔다.**
>
> ⚠⚠ **근거 규율** — 여기 적는 출처는 **우리가 실물을 가진 것만**이다
> (`litdb/papers/<slug>.md` 가 있는 것). 기억으로 서지를 지어내지 않는다.
> 실물이 없으면 `⚠ 원전 미보유` 로 표시하고, 발표 전에 PDF 를 확보해서 채운다.
> (CLAUDE.md: "레퍼런스는 링크가 아니라 **로컬 PDF/litdb digest 기준**으로 작성")

---

## A. 표면·계면 (SDCP 캠페인에서 오늘 정정된 것)

| 우리가 쓰던 말 | 필드 표준어 | 왜 그게 맞나 | 근거 |
|---|---|---|---|
| ⛔ "화학흡착" (Li 가 뽑혀 나온 경우) | **surface Li⁺ abstraction / extraction** | 기질 원자가 흡착종 착물로 **편입**되면 adsorption 이 아니다. 흡착은 계면에서의 농축이지 기질 조성의 변화가 아니다 | IUPAC Gold Book — *adsorption* / *chemisorption*. ⚠ 원전 미보유(웹 정의) |
| ⛔ "E_bind (결합에너지)" (같은 경우) | **reaction energy** | E_ads 는 기질 조성이 보존될 때만 성립. 표면에서 Li 가 빠지면 반응식이 달라진다 | 동일 |
| ✅ "표면 이완" | **surface relaxation** | 층간 거리만 변하고 **면내 주기는 보존** | 표준 표면과학 |
| ✅ "재구성" | **surface reconstruction** | 면내 **주기가 바뀐다** — relaxation 과 구별해서 쓸 것 | 표준 표면과학 |
| "흡착 자세" | **adsorption configuration / binding motif** | pose 는 도킹(생물) 용어. 무기 표면에선 configuration/motif | ⚠ 원전 미보유 |
| "코팅이 접촉을 끊는다" | **physical separation + self-stability against both sides** | "chemical potential gradient 가 구동력을 낮춘다" 는 부정확 — 구동력은 두 끝 상이 정한다 | `richards2016_interface_stability_pseudobinary` (Chem. Mater. 2016) · 우리 리뷰 노트 A34 |
| "계면 반응성" | **pseudo-binary interfacial reaction energy** | 닫힌계 pseudo-binary 로 정의되는 양 | `richards2016_…` |

> 🔴 **2026-08-06 실측 사례** — Phase-A 를 슬랩 자유로 풀었더니 E = −1.465 eV 가 나왔는데,
> 구조를 보니 **표면 Li 2개가 2.33 / 0.89 Å 이동해 sulfonate O 에 1.91–2.05 Å 로 배위**했다.
> 분자는 안 깨졌다(결합 35→35). 즉 **흡착이 아니라 Li⁺ 추출·배위**다.
> ⚠ 그리고 **LiNiO₂ 에서 Li⁺ 를 빼려면 전하 보상(Ni³⁺→Ni⁴⁺ 산화)이 따른다.**
> UMA 는 산화상태를 명시적으로 다루지 않으므로 그 대가를 안 물었을 수 있다 → **과대평가 가능**.
> **결과가 아니라 가설**이며 DFT+U 로만 판정한다. 검증 도구: `tools/sdcp/check_adsorption_sanity.py`

---

## B. 전자구조

| 우리 말 | 표준어 | 주의 | 근거 |
|---|---|---|---|
| "밴드갭" | **fundamental band gap** (VBM–CBM) | ⚠ **optical gap 과 다르다.** 그리고 우리 값은 **fixed-occupation nscf 고유값** 기준 — DOS-threshold 판독은 ~0.3 eV 과소 (CLAUDE.md 규율) | `he2019_dft_for_battery_materials_review` (EEM 2019) |
| "PBE 가 갭을 과소평가" | **band-gap underestimation of semi-local functionals (derivative discontinuity)** | 청중이 반드시 묻는다. "PBE 라서" 가 아니라 **XC 의 미분 불연속 부재** 때문 | `he2019_…` |
| "U 값" | **Hubbard U correction (DFT+U)** | 어느 원자·어느 오비탈에 걸었는지 명시 (우리: Ni 3d, U = 6.2 eV) | ⚠ 원전 미보유(Dudarev) |
| "결합 세기" | **−ICOHP (integrated crystal orbital Hamilton population)** | ⚠ **ICOHP 는 부호가 음수일 때 결합성**. 크기를 말할 땐 \|ICOHP\| 로 | ⚠ 원전 미보유(Dronskowski/LOBSTER) |
| "전하" | **Bader charge** (분할 기준 명시) | 절대값은 분할법 의존 — **같은 방법 내 비교만** | ⚠ 원전 미보유 |
| "전자 국재" | **ELF (electron localization function)** | 0–1 무차원. 절대값 인용 시 등가면 기준 명시 | ⚠ 원전 미보유 |

---

## C. 수송 (여기가 defense 에서 제일 위험하다)

| 우리 말 | 표준어 | 주의 | 근거 |
|---|---|---|---|
| "확산영역 게이트" | **diffusive-regime criterion** — log-log MSD 기울기 β = d log⟨r²⟩/d log t → 1 | 이게 없으면 **케이지 구간의 기울기를 D 로 착각**한다 | ⚠ 2026-08-06 정정: **β 판정과 0.8 문턱은 우리 것**이다(`tools/ionic/msd_diffusive_check.py`). Kahle 이 한 것은 창 길이 검증·블록분산·자동수렴이므로 그쪽을 근거로 대면 "Kahle 에 그런 기준 없다"로 반박된다 |
| "게이트 실패" | **sub-diffusive (caged) regime** | β < 0.8 이면 D 가 정의되지 않는다 | 동일 |
| "σ" | **Nernst–Einstein conductivity, σ_NE (Haven ratio = 1 가정)** | ⚠ **상관 운동이 있으면 H_R ≠ 1.** 아지로다이트는 협동 홉의 전형이라 **σ_NE 는 근사** | `famprikis2019_fundamentals_inorganic_sse` (Nat. Mater. 2019) — Eq.(3) 타당성 논쟁 명시 |
| "Ea" | **activation energy from Arrhenius fit of D(T)** | 온도점·창·시드 수를 같이 적어야 값이 성립 | `kahle2020_…` |
| "MLIP-MD" | **machine-learned interatomic potential molecular dynamics** | 모델명·버전·task 를 반드시 (우리: UMA-s-1p1, task=omat) | ⚠ 원전 미보유(UMA/FAIRChem) |
| "prefactor" | **Arrhenius prefactor D₀ = (1/6) z a₀² ν₀ exp(ΔS_m/k_B)** ⚠ 2026-08-06 정정: 캐리어 밀도 n 은 **σ₀ 식에만** 들어간다(σ₀ = z(nq²/k_B)e^{ΔS_m/k_B}α₀²ν₀). n 을 남기면 차원이 m⁻¹s⁻¹ 가 되어 D₀(m²/s)가 아니다 | ⚠ **연질 골격은 Ea 를 낮추지만 ν₀·ΔS_m 을 낮춰 D₀ 를 깎는다** — Ea 만 보면 안 된다 | `famprikis2019_…` Eq.(2) |

> ⛔ **σ 절대값 인용 금지** (CLAUDE.md). 비율도 **멀티시드 판정만**.
> 근거는 우리 실측(단일시드 1.33× 철회, 2026-07-09) + 문헌(그룹 간 재현성 1자릿수 산포,
> `famprikis2019_…`). 발표에서 이걸 **먼저** 말하면 "왜 σ 를 안 보여주나" 질문이 무력화된다.

---

## D. 역학

| 우리 말 | 표준어 | 주의 | 근거 |
|---|---|---|---|
| "탄성계수" | **elastic constants C_ij → VRH average (E, G, B)** | clamped-ion vs **relaxed-ion** 구분 필수 — 우리 계에서 clamped 는 실험의 ~2.3배 | `deng2016_elastic_superionic_electrolytes_dft` (JES 2016) · `famprikis2019_…` |
| "B₀" | **bulk modulus from Birch–Murnaghan EOS fit** | ⚠ **B_VRH(harmonic)와 다른 양** — 둘 다 보고하되 섞지 말 것 | Birch, *Phys. Rev.* 71, 809 (1947) ⚠ **원전 미보유** (덱에 인용한 것은 실물 보유가 아니다 — 이 파일의 규율 위반이었다, 2026-08-06 정정) |
| "연성/취성" | **Pugh's ratio B/G** (> 1.75 ductile) | ⚠ **금속 경험칙**이다. 이온성 세라믹에 그대로 적용하면 안 되고, 아지로다이트의 실용적 "무름"은 **분말 압축 성형성**이지 단결정 연성이 아니다 | Pugh, *Phil. Mag.* 45, 823 (1954) — ⚠ 원전 미보유 |
| "이방성" | **Zener anisotropy A = 2C₄₄/(C₁₁−C₁₂)** | ⚠ 셀이 완전 입방이 아니면 **triplet 마다 값이 다르다.** A−1 의 부호를 triplet 명시 없이 인용 금지 (`elastic.json` `_Zener_A_convention`) | — |
| "파괴인성" | **fracture toughness K_IC** | ⚠⚠ **탄성계수와 다른 급의 양이고 우리는 못 낸다.** 치밀도·입경·불순물·기공에 강하게 의존하는 **시편 물성**이라 실험 결정 | `famprikis2019_…` (명시) |
| "변형에너지가 인성을 넘으면" | ⛔ **차원이 안 맞는다** → **G ≥ G_c** (둘 다 J/m²) 또는 **K ≥ K_IC** | 심사 중 리뷰 원고의 실제 오류 (우리 코멘트 §3.5) | Griffith 이론 — ⚠ 원전 미보유 |

---

## E. 스크리닝·계산 전략

| 우리 말 | 표준어 | 근거 |
|---|---|---|
| "cascade" | **tiered / funnel screening** (cheap descriptor → expensive validation) | `sendek2017_ml_screening_12k_conductors` (EES 2017) · `xiao2019_cathode_coating_screening` |
| "ESW" | **electrochemical stability window from grand-potential phase diagram** (μ_Li 기준) | `zhu2015_esw_grand_potential_origin` |
| "hull" | **energy above the convex hull, E_hull** (준안정성 지표) | `zhu2015_…` · `richards2016_…` |
| "공기안정성 축" | **hydrolysis reaction free energy ΔG_hyd at specified partial pressures** | `zhu2020_air_stable_se_design_principles` (Angew. 2020) — SI 전수 전사 보유 |
| "AI 계산" | ⛔ **쓰지 말 것.** MLIP 는 AI 가 아니라 **회귀 대체 모델**이다 | — (지도 피드백 반영, 2026) |
| "champion" | **lowest-energy configuration** (또는 best-scoring candidate) | — |

---

## F. 발표 전 체크리스트

1. **슬라이드마다 처음 나오는 약어는 우상단에 풀어 쓴다** (이 랩 템플릿 관례).
2. **수치에는 계산 조건을 붙인다** — pseudo · ecut · k-mesh · 시드 수 · 창.
3. **"우리 값" 과 "문헌 소환값" 을 같은 표에 넣지 않는다.** 넣어야 하면 열을 나누고 방법을 병기.
4. **못 하는 것을 먼저 말한다** — K_IC, μm 입자 역학, 공간전하층 정량. 이걸 선제하면
   질문이 공격이 아니라 논의가 된다.
5. ⚠ **이 파일에서 `원전 미보유` 인 항목을 발표에 인용하려면 PDF 를 먼저 확보**한다.
   기억으로 서지를 쓰지 않는다.
