# Doux 2020 (Adv. Energy Mater. 10, 1903253) — Stack Pressure: 작동압력(operating) vs 제조압력(fabrication)의 정전적(canonical) LPSCl 앵커

> slug `doux2020_stack_pressure_assb` · DOI `10.1002/aenm.201903253` · type `DEM` · digested `2026-07-28` · status ✅
>
> ⓘ **정본 승격 2026-07-28** — 원본 `claude/stoic-knuth-NObVQ:docs/lit_doux2020_stack_pressure_assb.md`.
> 단일-서랍 규칙(CLAUDE.md)에 따라 이관 — 그전까지 DFT webapp 목록에 안 떴다.


**인용:** Jean-Marie Doux, Han Nguyen, Darren H. S. Tan, Abhik Banerjee, Xuefeng Wang,
Erik A. Wu, Chiho Jo, Hedi Yang, Ying Shirley Meng\*, "Stack Pressure Considerations for
Room-Temperature All-Solid-State Lithium Metal Batteries," *Advanced Energy Materials*
**2020**, *10*, 1903253. DOI 10.1002/aenm.201903253. UCSD (Y. S. Meng / SPEC).
Communication (6쪽) + SI (8쪽). Received 2019-10-04 / Revised 2019-11-06 / Published online
2019-11-25. ⚠ 저널 표기는 **2020** vol.10 이지만 online-first 는 **2019** (인용 시 둘 다 통용).

**소재:** **Li₆PS₅Cl (LPSCl argyrodite)** SE (NEI Corp.) + **Li-metal 음극** + (full cell)
**LNO-coated NCA** (LiNi₀.₈Co₀.₁₅Al₀.₀₅O₂, Toda) 양극. ★ **SE 가 우리와 정확히 같은 LPSCl** —
따라서 **SE 의 압력-σ·압력-역학(creep)은 직접 전사 가능**. 단 ⚠ **이 논문의 주제는 Li-metal 음극의
단락(shorting) 거동**이지 *복합 양극 미세구조*가 아니다 → **양극 microstructure 수치는 전사 금지**,
**SE 압력-역학만** 가져온다 (§10 한계 참조).

동반 데이터 파일:
- `docs/data/doux2020_stack_pressure.csv` — Fig 4c 임피던스-vs-압력 + 압력별 단락시간 + 펠릿 밀도
  (본문 stated 값 위주, Fig 디지타이즈는 TREND 플래그).

**같은 stack-pressure 패밀리 안에서의 위치:**
- **Cronau 2021** (`docs/lit_cronau2021_*`) = stack pressure 가 **σ 측정의 신뢰성**을 어떻게 좌우하나
  (측정 protocol, 황화물 일반).
- **Doux 2020** (본 digest) = stack pressure 가 **Li-metal 단락·접촉·작동성**을 어떻게 좌우하나
  (셀 운용, LPSCl 구체).
- **Minnmann 2021 JES** = 압밀 380 MPa / 측정 40 MPa (압력 3종 구분의 EIS-TLM 앵커).
세 논문이 합쳐 **제조압(fabrication, ~300–490 MPa) ≠ 측정/작동압(stack/operating, ~5–70 MPa)** 의
3종 압력 구분을 완성한다 — 이게 본 digest 의 우리 모델에 대한 핵심 기여.

---

## ★★★ §0. 한 줄 결론 — 이게 왜 우리 모델의 "작동압력 앵커"인가 ★★★

우리 DEM/MPM 은 **제조압(300 MPa cold-press, Heckel P_y=138 MPa)** 으로 미세구조를 만든다.
하지만 실제 셀은 그보다 훨씬 낮은 **작동 stack pressure(수~수십 MPa)** 에서 사이클된다.
Doux 2020 은 **LPSCl 시스템에서 그 작동압 창(window)을 실험으로 못박은 정전적(canonical) 논문**이다:

> **낮은 stack pressure(≈5 MPa)** 가 Li-metal 음극을 **신뢰성 있게 1000 h+ 사이클**시키고
> (full cell >200 cycle), **높은 stack pressure(≥25 MPa)** 는 오히려 **Li 가 SE 공극으로
> creep → 단락**시킨다. 최적 = **5 MPa**. 단락은 *전기화학*이 아니라 *기계적(mechanical)* 현상.

그리고 그 메커니즘의 뿌리는 **펠릿이 18 % porosity** 라는 점 (370 MPa cold-press 후에도 잔류) —
즉 **SE 펠릿 안에 빈 공극망이 있고, soft 한 Li 가 압력을 받으면 그 공극으로 흘러든다.**
→ 이 두 가지(**porosity 가 압력으로 못 다 닫힌다** + **soft 상이 공극으로 흐른다**)는 정확히
우리 **E_eff 18× 연화 프록시**와 **MPM 소성 void-fill flow** 가 모델링하는 물리다.
LPSCl 자체가 압력에 민감한 soft/creep 거동을 보인다는 본 논문의 증거가 **연화-모듈러스 프록시를
실험적으로 정당화**한다 (단, *creep 주체는 Li metal* 이고 LPSCl 은 *공극을 가진 다공성 매질* 역할 —
§10 정밀 구분).

---

## 1. 동기 / 핵심 질문 (Intro)

ASSB + Li-metal 음극은 부피에너지밀도를 크게 높일 수 있다. 통설은 "SE 가 기계적으로 충분히 강하면
(Monroe–Neumann 기준: SE 의 전단탄성률이 Li 의 2배 이상) Li dendrite 전파를 막는다"였다. 그러나
**현실은 거의 완벽히 조밀한 단결정 산화물 SE(LLZO 등)에서도 dendrite 가 침투해 몇 사이클 만에 단락**
한다 — 기준을 만족해도 내부 dendrite 가 생긴다. 본 논문의 질문:

> **"무엇이 Li-metal ASSB 의 단락을 일으키며, applied stack pressure 가 거기서 어떤 역할을 하나?"**

핵심 물리 배경 (본문 인용):
- **Li 의 항복강도 ≈ 0.8 MPa** (Masias et al. / Tariq et al.), 그 이상에서 **creep(소성 흐름)** 시작.
  LePage et al. — 상온에서 Li 의 항복은 **creep-지배(creep-dominated)**.
- 이 Li 항복강도를 **셀에 가하는 stack pressure 와 비교**해야 음극 역학을 이해할 수 있다 →
  본 논문의 출발점. (스포일러: 가장 낮은 5 MPa 조차 Li 항복 0.8 MPa 의 **~6×**, 75 MPa 는 **~100×**.)
- 액체전해질과 달리 SE 는 **사이클 중 새로 생기는 표면을 적시지(wet) 못함** → **일정 접촉을 유지하려면
  압력이 필요**. 그러나 압력이 과하면 soft Li 가 SE 공극으로 흐른다 → **딜레마**.

---

## 2. 실험 셋업 (Methods + SI)

### 2.1 소재·셀 제작 (SI Methods)
- **SE:** Li₆PS₅Cl, **NEI Corp.** 구매품 그대로 (as-is). Ar 글러브박스(H₂O<0.1, O₂<0.5 ppm).
- **펠릿:** 분말 **200 mg** → **13 mm PEEK die** → **370 MPa** 유압프레스 cold-press →
  두께 **~1 mm** → **σ_ion = 2–2.5 mS/cm** (EIS). ★ 이게 **bulk LPSCl 펠릿 σ 앵커** (cold-press,
  GB·잔류공극 포함).
- **Li 대칭셀:** Li foil 0.5 mm(FMC), 솔로 표면산화 제거, **12.7 mm disc** 양면, **25 MPa 로 압착**
  (초기 접촉 형성) → 이후 stack pressure 를 **5/10/15/20/25/75 MPa** 로 설정해 plate/strip 시험.
  전류 **75 µA/cm²**, **1 h plate / 1 h strip** step.
- **Full cell:** 양극 composite = LNO-coated NCA : LPSCl : carbon black = **11 : 16 : 1 wt%**,
  agate 막자로 혼합, 펠릿 한쪽에 **370 MPa** 압착(12 mg). 음극 = Li disc(12.7 mm, **25 MPa**) 또는
  Li-In 분말(70 mg, **120 MPa**). **C/10, 2.5–4.3 V vs Li/Li⁺**. 활물질 로딩 **3.55 mg/cm²**.
- ★ **LNO coating** 이유: LPSCl 과 고전압 NCA 의 계면반응 방지 (Trevisanello/Sakuda 류 보호층).

### 2.2 압력 모니터·제어 (Fig 2a, SI) — in-situ 압력셀
- 특수 셀 홀더: **3-ton load cell** 을 셀 축(axis) 아래에 장착 → 사이클 중 **0–220 MPa stack
  pressure 를 실측·제어**. 100 kN Instron 5982 로 교정. ★ **이게 본 논문의 "in-situ
  characterization"** — 압력을 끄지 않고(나사 조임으로) 정밀 튜닝하며 EIS·전압을 동시 측정.
- 절연 spacer 로 외부 단락 차단.

### 2.3 X-ray 단층촬영(tomography) + XRD (Fig 5, SI) — buried Li 직접 관찰
- 별도 고해상 셀: 3.2 mm PC 봉에 **2 mm 내경** 보어 → **2 mm 강철 플런저**. LPSCl 5 mg →
  **370 MPa** 펠릿(~2 mm). Li strip 양면 **25 MPa**, 양쪽 >5 mm Li(플런저 X선 흡수 아티팩트 방지).
- **Zeiss/Xradia Versa 510**, 80 kV/6.5 W, LE2 필터, 4× 대물, 1601 projection → 해상도 **~1.18 µm**.
  Amira 2019.1 + Fiji 재구성.
- **XRD:** Cu Kα 는 투과모드 부족 → **Mo Kα (λ=0.70932 Å)**, Bruker Apex II Ultra 투과모드 +
  2D CCD. FullProf profile matching.
- ★ "고해상 morphology imaging + 화학종 식별 + in-situ buried interface" 를 한 셀에서 결합 —
  본 논문이 강조한 도구적 신규성.

---

## 3. 핵심 결과 ① — Stack pressure ↔ Li 단락 시간 (Fig 2b, SI Fig S3/S4)

**가장 중요한 표.** Li 대칭셀(75 µA/cm², 1h/1h)을 각 stack pressure 에서 plate/strip 하며
**단락(short-circuit)까지 걸린 시간**:

| stack pressure | 단락까지 시간 | 거동 / 메커니즘 | source |
|---|---|---|---|
| **75 MPa** | **0 h (압착 즉시)** | plating 전부터 **기계적 단락** — Li 가 압착만으로 공극 관통 | Fig 2b/4f, S6 |
| **25 MPa** | **~48 h** | plate/strip 중 Li 가 grain 사이로 creep → dendrite → 단락 | Fig 2b/4e |
| **20 MPa** | **~190 h** | 〃 (압력↓ → 시간↑) | Fig 2b/S4 |
| **15 MPa** | **~272 h** | 〃 | Fig 2b/S4 |
| **10 MPa** | **~474 h** | 〃 | Fig 2b/S4 |
| **5 MPa** | **>1000 h, 단락 無** ✓ | Li creep 부족 → 공극 침투 안 함 → **안정** | Fig 2b/S4/S5 |
| **2 MPa** | (안정, ~165 h 시현) | 더 낮춰도 작동 — 5 MPa 가 하한 근처임을 보강 | SI Fig S3 |

핵심 narrative:
- **명확한 추세:** stack pressure ↑ → 단락까지 시간 ↓ (75→0, 25→48, 20→190, 15→272, 10→474,
  5→∞). **단조(monotonic)**. ★ 단락은 **압력의 함수인 기계적 현상** (전기화학 dendrite 핵생성이
  아님).
- **25 MPa 특이점:** plate/strip **하는** 동안만 단락. **압력만 25 MPa 로 걸고 plate/strip 안 하면
  단락 안 함** → "Li creep-유발 단락은 25 MPa 자체로는 안 일어나고, plating 의 추가 응력이 더해져야
  dendrite 가 자란다." (Fig 4e)
- **모든 셀에서 과전압(overpotential) 일정** → 안정한 Li–LPSCl 계면 형성, 단락 직전까지 정상.

---

## 4. 핵심 결과 ② — Stack pressure ↔ 셀 임피던스(접촉) (Fig 4c) ★ 우리 σ-vs-P 비교 핵심

Li 대칭셀 임피던스가 **압력에 강하게 의존** (= 계면 접촉면적의 압력 의존성). 본문 stated 값:

| stack pressure | 셀 임피던스 | 비고 |
|---|---|---|
| **1 MPa** | **>500 Ω** | 접촉 빈약 (보이드 다수) |
| **5 MPa** | **≈110 Ω** | |
| **10 MPa** | **≈50 Ω** | |
| **15 MPa** | **≈40 Ω** | |
| **20 MPa** | **35 Ω** | |
| **25 MPa** | **32 Ω** | 거의 포화(plateau) |
| **→ 5 MPa 로 release** | **≈50 Ω** | ★ **초기 5 MPa(110 Ω)의 절반 이하** — **비가역(irreversible)** |

★★ **두 가지 핵심 물리:**
1. **포화(saturation):** 임피던스가 **압력↑ → 급감 후 ~20–25 MPa 에서 plateau**
   (500→110→50→40→35→32 Ω). 즉 **접촉면적 증가가 ~25 MPa 부근에서 수확체감**. ← 이게
   **σ-vs-P 의 무릎(knee)·포화** = 우리 Heckel P_y / Bazzoun σ-포화@400 MPa 와 같은 계열의
   "압력으로 접촉이 좋아지다가 포화" 곡선 (단 여긴 Li/SE *계면* 접촉, 우리·Bazzoun 은 SE/SE *벌크망*).
2. **이력(hysteresis)·비가역:** 25 MPa 까지 올렸다 5 MPa 로 내리면 임피던스가 **초기 5 MPa 의
   절반 이하(110→50 Ω)** 로 유지. **한 번 높은 압력으로 다진 접촉은 압력을 낮춰도 안 풀린다**
   (Fig 4b: 25 MPa 압착 → 계면 보이드 소멸, SI Fig S1 사진으로 확인). → **"높은 압력으로 초기
   접촉을 만들고 낮은 압력으로 운용"** 이라는 실용 전략의 근거. ★ 이 **압밀의 비가역성(소성)** 은
   우리 MPM 소성(영구 형상변화·overlap 잔류)·Heckel(비가역 압밀)의 거시 증거.

---

## 5. 핵심 결과 ③ — Full cell 작동성 (Fig 1, Fig 3) — 5 MPa 가 실제로 쓸 수 있다

- **Li | LPSCl | LNO-NCA full cell @ 5 MPa, C/10, 상온:**
  - **>200 cycle (229 cycle)** 단락 없이 사이클. **100 cycle 에서 80.9 % 용량유지**.
  - **평균 CE 98.86 %** (229 cycle 평균). **1st cycle 150 mAh/g, 1st CE 69 %**.
  - 활물질 로딩 3.55 mg/cm². ★ **상온 Li-metal ASSB 가 합리적(낮은) stack pressure 에서 가능함을 시현**.
- **대조 — Li-In 음극 full cell @ 25 MPa (Fig 1):** 1st 방전 **140 mAh/g**, **1st CE 66.5 %**,
  이후 CE>99 %, 단락 없음. (Li-In 은 합금이라 creep 거동·계면이 Li-metal 과 달라 25 MPa 에서도 OK.)
- **Li-metal @ 25 MPa full cell (Fig 2c):** 1st charge 에서 전압 강하 후 **충전 실패** →
  Li-metal 특유의 plating 단락. **같은 25 MPa 라도 Li-metal 은 단락, Li-In 은 정상** →
  단락은 **Li-metal 의 기계적(creep) 특성** 때문이라는 결정적 대조.
- Fig 2c: **5 MPa Li-metal full cell 은 1st cycle 정상 충방전** (150 mAh/g, 1st CE 69 %).

---

## 6. 핵심 결과 ④ — 단락 메커니즘 모델 (Fig 4) + porosity 18 % ★ 연화-프록시 연결고리

본 논문의 **종합 메커니즘 그림(Fig 4)** — 3가지 압력 시나리오:

**Fig 4a→b (제작 단계):**
- (a) Li 를 펠릿 양면에 얹기만 하면 계면 접촉 빈약(보이드 많음).
- (b) **25 MPa 로 압착 → 계면 보이드 소멸**, 초기 임피던스 급감. PC die 로 보이드 사라짐을 육안 확인
  (SI Fig S1 사진). ★ **압력으로 계면을 다지는 것은 (전압-비가역) 소성 압밀**.

**Fig 4c (임피던스 vs 압력):** §4 의 곡선 — 1 MPa 500 Ω → 25 MPa 32 Ω, release 5 MPa 50 Ω(비가역).

**Fig 4d (5 MPa):** 접촉 유지에 충분하나 Li creep 유발엔 부족 → **>1000 h 단락 없음**. 5 MPa 에선
Li 가 **펠릿 표면에만** plating (공극으로 못 들어감).

**Fig 4e (25 MPa):** Li 가 SE **grain 사이 공극으로 천천히 creep** → 두 전극 간 거리 단축 →
그 돌출부(protuberance)가 과전압 낮은 **선호 plating 점** → dendrite 성장 → **~48 h 후 단락**.

**Fig 4f (75 MPa):** Li 가 펠릿을 **관통(creep through) → 심한 균열 → plate/strip 전 즉시 기계적
단락** (SI Fig S6: 1 mm 스케일 균열 tomography).

★★ **porosity 핵심 수치 (Table S2):** 4개 LPSCl 펠릿의 상대밀도 = **80.3 / 84.9 / 80.3 / 83.0 %
→ 평균 82.1 %** (이론밀도 1.860 g/cm³ 기준, 실측 1.522 g/cm³). 즉 **porosity ≈ 18 %**
(본문도 "A porosity of 18% within the electrolyte provides connecting pathways" 라 명시).

이 **18 %** 가 메커니즘의 뿌리:
- **370 MPa cold-press 후에도** 펠릿에 **18 % 잔류 공극**이 있다 = **압력으로 공극을 다 못 닫는다.**
  ★ 이건 우리 "**~20 % 가 강체-구 floor, 소성 흐름 없으면 못 넘음**" 과 **정확히 같은 수치대**
  (실험 LPSCl 펠릿 18 % ≈ 우리 rigid-sphere floor ~20 %).
- 그 **연결된 공극망**이 soft Li 의 creep 경로를 제공 → **전자 percolation 경로 형성 → 단락**.
- **75 MPa 가 Li 항복(0.8 MPa)의 ~100×**, 가장 낮은 5 MPa 도 ~6× → **어떤 작동압이든 Li 는
  소성 영역**에 있고, 차이는 "공극으로 흘러들 만큼 충분한 응력이냐"이다.

---

## 7. 핵심 결과 ⑤ — X-ray tomography + XRD (Fig 5) — buried dendrite·SEI 직접 관찰

**25 MPa 셀, plate/strip 전/후 비교:**
- **전(pristine):** SE 영역엔 **LPSCl 회절피크만**, 전극영역엔 **Li-metal 피크만**. Li-LPSCl 계면
  평탄, 보이드 없음. tomography 로 Li 가 펠릿 안엔 **없음** 확인.
- **후(plate/strip):** tomography 에 **저밀도(low-density) dendrite 구조가 SE 내부에 대량** —
  **grain boundary 따라 전파**하다 국소 확장. XRD 에 **새 상: LiCl, Li₂S, 환원된 P 종(Li₃P 등)** =
  **Li 가 LPSCl 과 접촉해 생긴 SEI** (Li⁺ + Li₆PS₅Cl → LiCl + Li₂S + Li₃P …). Li-metal 자체는
  양·적은 산란으로 XRD 직접검출 안 됨(SEI 산물로 간접 확인).
- ★ **같은 셀에서 tomography(형상) + XRD(화학종)** → dendrite 성장과 그 계면 분해산물을 **직접 동시
  관찰** (전기화학 측정의 단락 해석과 일치).
- **보이드 형성 완화 팁:** 최근 보고된 **stripping 중 Li-SE 계면 보이드(3.5–7 MPa)** 문제는
  **초기 고압(25 MPa)으로 균질 접촉 형성 후 작동압(5 MPa)로 release** 하면 완화 — 본 논문 시료엔
  보이드 없었음. ★ **고압-제작 + 저압-운용** 전략의 또 다른 근거.

---

## 8. 핵심 결과 ⑥ — 펠릿 자체는 압력에 안 변한다 (mechanical decoupling) ★ 중요한 구분

본문 명시: **"5/25/75 MPa stack pressure 의 (펠릿 자체) 기계적 성질은 단락 메커니즘에 영향을
주지 않을 것으로 본다 — 펠릿은 이미 370 MPa 로 cold-press 되어 있기 때문."**

★★ 이게 본 논문이 **제조압 vs 작동압을 분리**하는 결정적 문장:
- **펠릿의 압밀(densification)·역학은 제작 시 370 MPa 에서 이미 결정**됨 (비가역 소성).
- 작동 stack pressure(5–75 MPa)는 펠릿을 **더 압밀하지 않는다** (370 ≫ 75). 작동압이 바꾸는 건
  **(i) Li/SE 계면 접촉** 과 **(ii) Li 의 공극-creep** 뿐.
- 즉 **압밀 물리(porosity·E·Heckel)는 제조압의 영역**, **계면접촉·creep·단락은 작동압의 영역** —
  두 압력이 **다른 물리를 지배**. ⇒ 우리 모델의 "**300 MPa 제조 = porosity/Heckel**, 작동압 = 별도"
  분리와 **개념적으로 1:1**.

(주의: 75 MPa 에서 Li 가 펠릿을 관통-균열시키는 것은 *펠릿이 압밀되어서*가 아니라 *soft Li 가
공극으로 흘러 SE 를 쪼개서* — SE 의 압밀상태가 아니라 **Li 의 creep + SE 의 공극**이 주체.)

---

## 9. Figure / SI 전수 (각 그림이 무엇을·우리가 뭘 쓰나)

### 본문 Figure
| Fig | 내용 | 핵심 수치 | 우리가 쓸 점 |
|---|---|---|---|
| **1** | Li-metal vs Li-In full cell 첫 2사이클 voltage (둘 다 25 MPa) | Li-In 140 mAh/g·1stCE 66.5 %; Li-metal 25 MPa 충전실패(단락) | 같은 25 MPa 라도 음극재질로 단락 갈림 = 단락이 Li-metal 역학 탓 |
| **2a** | in-situ 압력셀 모식 (load cell 축방향) | 0–220 MPa 실측 | **압력 in-situ 모니터링 셋업** 참고 |
| **2b** | 압력별 단락시간 막대 | **75→0, 25→48, 20→190, 15→272, 10→474, 5→∞ h** | ★ **압력-vs-단락시간 정량표** (§3) |
| **2c** | full cell voltage: 5 MPa(정상) vs 25 MPa(단락) | 5 MPa 150 mAh/g·1stCE 69 % | 작동압 창 시현 |
| **3a** | 5 MPa full cell 1·2·5·10 사이클 voltage | 안정 profile | 5 MPa 장기안정 |
| **3b** | 5 MPa full cell 사이클수명 + CE | **229 cycle, 80.9 %@100cyc, CE 98.86 %** | ★ 작동성 앵커 |
| **4a–f** | 단락 메커니즘 모식 (제작→5/25/75 MPa) | **porosity 18 %**; 임피던스 곡선 | ★ §4·§6 메커니즘 + porosity floor |
| **4c** | 셀 임피던스 vs 압력 (+release 이력) | **500→110→50→40→35→32 Ω; release 5 MPa=50 Ω** | ★★ **σ/접촉-vs-P 포화+비가역** (§4) |
| **5a** | tomography+XRD, plate/strip **전** | LPSCl·Li 피크만, 계면 평탄 | 기준상태 |
| **5b** | tomography+XRD, plate/strip **후(25 MPa)** | dendrite 다량; **LiCl/Li₂S/Li₃P (SEI)** | ★ dendrite·SEI 직접관찰 |

### SI Figure / Table
| SI | 내용 | 핵심 수치 | 우리가 쓸 점 |
|---|---|---|---|
| **Fig S1** | 25 MPa 압착 전/후 Li/SE 계면 사진 | 보이드 소멸 | 압착=계면 보이드 제거(육안) |
| **Fig S2** | 25 MPa 셀 Nyquist (0/10/20 h plate/strip) | Z' 28→43 Ω 대역, 1 kHz/1 Hz | EIS 시간변화 |
| **Fig S3** | **2 MPa** 대칭셀 전압 (~165 h) | ±~6–7 mV, 안정 | 5 MPa 보다 더 낮아도 작동(하한 보강) |
| **Fig S4** | 5/10/15/20/25 MPa 대칭셀 전압 풀곡선 | 단락시점 = Fig 2b | 압력별 raw 데이터 |
| **Fig S5** | 5 MPa tomography 전/후(92 h) + 전압 | 보이드/dendrite 無 | 5 MPa 깨끗함 직접확인 |
| **Fig S6** | **75 MPa** 기계적 단락 tomography | **1 mm 스케일 균열** | 고압 SE 균열 |
| **Table S1** | 문헌 Li-metal ASSB 사이클 요약 | LPSCl/Li₂S-P₂S₅/Li₃PS₄ 74/50/79 % | 맥락 |
| **Table S2** | LPSCl 펠릿 4개 상대밀도 | **80.3/84.9/80.3/83.0 → 평균 82.1 % (porosity 18 %)** | ★★ **porosity 앵커** (§6) |

---

## 10. ★ 비교 vs 우리 DEM+MPM (focused §) → `litdb/our_dem_baseline.md`

> 핵심 원칙: **SE(LPSCl)의 압력-역학·porosity·σ-vs-P 포화만 가져온다.** 양극 microstructure·
> 용량·Li-metal 단락 수치는 우리 *복합 양극* 과 다른 시스템 → 전사 금지.

| 축 | Doux 2020 | 우리 | 차이 / 매핑 (정직) |
|---|---|---|---|
| **소재(SE)** | **LPSCl** | **LPSCl 동일 ✓** | SE 물리 **직접 전사 가능** (halide·LIB 와 달리) |
| **제조압(fab)** | **370 MPa** cold-press, σ 2–2.5 mS/cm | **300 MPa** cold-press, Heckel P_y=138 | 같은 cold-press 영역(300↔370) — **제조압 정합** |
| **펠릿 porosity** | **18 %** (rel.dens 82.1 %, @370 MPa) | rigid-sphere floor **~20 %**; pure-SE **~10 %**(연화+소성) | ★ **18 % ≈ 우리 강체-구 floor** — 압력으로 못 닫는 잔류공극 실험 확증 |
| **작동압(operating)** | **5 MPa 최적** (≥25 단락) | 작동 수~수십 MPa(별도 영역) | ★ **작동압 창을 실험으로 못박음** (우리가 부족했던 앵커) |
| **σ/접촉 vs P** | 임피던스 500→32 Ω, **~25 MPa 포화**, **release 비가역** | Heckel knee P_y=138; Bazzoun σ-포화@400 | **압력↑→접촉↑→포화** 같은 계열 (단 Doux=Li/SE *계면*, 우리=SE/SE *벌크망*) |
| **soft 상 creep** | **Li 가 SE 공극으로 creep**(0.8 MPa 항복, 작동압이 ~6–100×) | **E_eff 18× 연화**(SE 압밀 럼핑) + **MPM 소성 void-fill** | ★ **soft 상이 공극으로 흐른다**는 거시물리 일치 — 단 **주체가 다름**(Doux=Li, 우리=SE) → §아래 |
| **압밀 비가역성** | 25→5 MPa 임피던스 이력(비가역) | MPM 소성 영구변형·overlap 잔류; Heckel 비가역 | 압밀=소성(비가역)의 거시 증거 ✓ |
| **단락/dendrite** | Li-metal 음극 핵심 주제 | (우리 모델 범위 밖 — 양극 microstructure) | **전사 금지** (§한계) |

### ★ "soft 상이 공극으로 흐른다"의 정밀 구분 (over-claim 방지의 핵심)
- Doux: **흐르는 주체 = Li metal**(음극), **공극을 제공하는 매질 = LPSCl 펠릿**(다공성, 18 %).
  Li 가 LPSCl 의 *기존* 공극으로 creep.
- 우리 MPM: **흐르는 주체 = LPSCl SE 입자 자신**(소성 void-fill), 공극은 SE-SE 입자간.
- ⇒ **물리 메커니즘(soft 소성상 → 공극 충전)은 같은 종류**지만, **Doux 는 Li 의 creep, 우리는 SE 의
  creep** 이다. Doux 가 우리 MPM 소성을 "직접" 검증하는 건 아니고, **(a) LPSCl 시스템에 18 % 잔류
  공극이 실재**하고 **(b) soft 상이 그 공극으로 흐르는 게 실제 물리**임을 **같은 소재계에서 보증**한다.
  우리 *SE 자체*의 creep/소성은 별도 근거(Minnmann pure-SE 10 %, MPM SEM morphology, So 2021
  H-cap)로 정당화 — Doux 는 그 **간접 보강**(LPSCl 은 압력에 민감한 soft/다공 시스템).

### ★ 우리 "300 MPa 제조 vs 작동압" 분리에 대한 직접 기여
- 본 논문 §8 의 명문장 — **"펠릿은 이미 370 MPa 로 cold-press 되어 작동 stack pressure 의 역학은
  단락에 영향 없다"** — 은 **제조압(압밀·porosity·Heckel)과 작동압(계면·creep)이 다른 물리를
  지배**함을 실험으로 분리. ⇒ 우리 코드의 "300 MPa = 제조(cold-press) / 작동 = 별도" 인식의
  **권위 있는 LPSCl 근거**. Heckel P_y=138 MPa(우리 DEM) 도 *제조압* 곡선의 무릎이지 작동압이 아님 —
  이 구분이 흐려지지 않게 cite.

---

## 11. 적용 인사이트 (내 연구에 어떻게)

- ① **작동압 앵커 확보:** "LPSCl Li-metal 셀 **최적 작동 stack pressure ≈ 5 MPa**, ≥25 단락" —
  우리가 제조압(300 MPa)만 있고 부족했던 **작동압 창**의 실험 앵커. 우리 σ_ionic/σ_e 가 *작동압*에서
  어떻게 변할지 논할 때 (그리고 양극이 아니라 *셀 운용* 맥락) 인용.
- ② **porosity 18 % ≈ 강체-구 floor 실험 확증:** 370 MPa cold-press LPSCl 펠릿이 **18 % 잔류공극** =
  우리 "rigid-sphere ~20 % floor, 소성 흐름 없으면 못 넘음" 의 **same-material 실측 지지**. 우리
  pure-SE 10 %(연화+소성)는 *이 18 % 아래로* 도달 → **연화/소성이 floor 를 깬다**는 논증의 대조점.
  `docs/data/densification_porosity_db.csv` 에 LPSCl 18 %@370 MPa 행 추가 가치.
- ③ **σ/접촉-vs-P 포화 + 비가역:** 임피던스 500→32 Ω(@25 MPa 포화) + release 비가역(110→50) →
  (i) **압력으로 접촉이 좋아지다 포화**(우리 Heckel knee / Bazzoun σ-포화 계열), (ii) **압밀=비가역
  소성**(MPM 영구변형) 의 거시 증거. 단 Doux 는 *계면* 접촉(Li/SE) → 우리 *벌크망*(SE/SE) σ 와는
  추세만 비교.
- ④ **제조/작동 압력 분리:** §8 문장으로 **"우리 300 MPa 는 제조압(porosity·Heckel), 작동은 다른
  영역"** 을 cite — 압력 3종(제조 ~300–490 / 측정~작동 5–70) 구분을 Cronau·Minnmann 과 합쳐 완성.

---

## 12. 인용 가능 문장 (deck/paper용)

- "For our Li₆PS₅Cl system, Doux et al. (2020) established that cold-pressed pellets retain
  ≈18 % residual porosity even at 370 MPa, and that the optimal **operating** stack pressure for
  a Li-metal cell is ≈5 MPa — high pressures (≥25 MPa) drive soft-phase creep into the pore
  network and cause mechanical shorting. This experimentally anchors our distinction between the
  ~300 MPa **fabrication** pressure (which sets porosity and the Heckel P_y) and the much lower
  **operating** pressure, and supports the ~20 % rigid-sphere porosity floor that our softened
  modulus and plastic void-fill flow are designed to break."
- "Doux et al. show the LPSCl cell impedance falls from >500 Ω at 1 MPa to ~32 Ω at 25 MPa and
  then plateaus, and that this contact gain is irreversible on pressure release (110→50 Ω) —
  macroscopic evidence of a pressure-driven, plastic (irreversible) densification consistent with
  our MPM permanent-deformation picture."

---

## 13. ★ 주의 / 한계 (over-claim 방지) — 정직 목록

- ⚠ **이건 Li-metal 음극 단락 논문이다, 복합 양극 미세구조 논문이 아니다.** 단락시간·용량(150 mAh/g)·
  CE·dendrite 수치는 **우리 양극 RVE 와 무관** → 전사 금지. 가져올 것은 **SE(LPSCl) 의 압력-역학·
  porosity·σ-vs-P** 뿐.
- ⚠ **creep 주체 = Li metal**, 우리 MPM 소성 주체 = SE 입자. Doux 의 "soft 상이 공극으로 흐른다"는
  **같은 종류의 물리**지만 **다른 상(Li≠SE)** — Doux 가 우리 SE 소성을 *직접* 검증하는 게 아니라
  *간접 보강*(§10 정밀구분). "Doux 가 우리 MPM void-fill 을 검증" 식 과장 금지.
- ⚠ **σ 가 아니라 임피던스(Ω)** 를 측정 — Fig 4c 는 *계면 접촉저항* 변화이지 SE *벌크 σ-vs-P* 가
  아니다 (벌크 σ-vs-P 의 직접 데이터는 **Bazzoun(RNM)·Cronau(측정 protocol)** 가 가짐). Doux 임피던스
  포화는 "압력→접촉→포화" *추세*만 우리·Bazzoun σ-포화와 같은 계열로 비교.
- ⚠ **실험(no simulation):** DEM/MPM 비교는 *물리 앵커*로서지, 모델-대-모델(frame[4]) 교차검증이
  아님 (Bazzoun 과 다른 성격). 우리 Kirchhoff/Holm·삼중항·MPM morphology 우위는 그대로 유지.
- ⚠ **porosity 18 % 는 펠릿(separator) 값**, *복합 양극* porosity 아님 (Minnmann 복합 14 % 와 구분).
  단 우리 *rigid-sphere floor* 비교엔 pure-SE/펠릿 값이 맞는 대조 (우리 pure-SE 10 % 와 같은 범주).
- ⚠ **digitized 주의:** Fig 2b 단락시간(48/190/272/474 h)·Fig 4c 임피던스(500/110/50/40/35/32 Ω)는
  **본문 stated** (신뢰). 그 외 그림 세부(전압 mV 등)는 TREND.
- ⚠ **σ_ion 2–2.5 mS/cm** 는 *cold-press 펠릿*(GB·공극 포함) — Cronau µC-Br plateau ~2.4, Lee
  pristine 2.19, Bazzoun pellet 1.02, 우리 채택 σ_grain 3.0(단결정-라벨) 사이의 **또 하나의 LPSCl
  bulk 앵커**. 측정·입자·GB 차 스프레드로만, 절대 직접대조 금지.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
