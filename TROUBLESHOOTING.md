# 🔧 TROUBLESHOOTING — 건식 후막 bimodal 전고체 복합양극

> **살아있는 문서.** 실험/공정/모델에서 막히는 문제를 진단·가설·증거·해결·검증실험으로 누적.
> 새 사실이 나오면 해당 이슈에 append + 상단 표 상태 갱신 + 하단 업데이트 로그에 날짜 기록.
> 명명: No.1=NCM_2(매끈) · No.2=NCM_3(satellite) · Poly=대립 다결정 · P=Poly, S=Single.
> 데이터 출처: `db/`, 문헌: `litdb/`, 과제 이슈: `docs/project/05_ISSUES_AND_FIXES.md`.

## 🎯 현재 초점 (2026-06-26): **공정 문제 (T2)**
전기화학·전달(T1) 분석은 **잠시 보류**. 지금 막힌 건 **공정** — Poly-rich(7:3) 합제가 cold 도우가 안 되고,
핫롤해도 떡전극이 안 되고 **갈라져 나옴**. 전극 자체가 제대로 안 만들어지므로 **여기를 먼저 깊게 판다.**

## 이슈 현황
| # | 이슈 | 상태 | 핵심 진단 |
|---|---|---|---|
| **T2** | **★ Poly-rich(7:3) 전극 제작 실패** — cold 도우 X → 핫롤해도 갈라짐(crack) | 🔬 **집중 진단 중** | 트리거 = **Poly 입자 단독**(SE·파쇄 배제). 단결정 부족 → PTFE 섬유망 결착 부족 → 필름 무결성 실패 |
| T1 | 6 mAh/cm² bimodal 후막 전극 성능 안 나옴 | ⏸ 보류 | (공정 해결 후) 후막 두께방향 이온(+전자) 전달 병목 |
| T3 | 모델 σ vs 실측 σ 불일치 | 📝 기록됨 | `05_ISSUES_AND_FIXES.md #2` 참조 |

상태: 🔬 진단 중 · 🧪 실험 대기 · ✅ 해결 · 📝 기록

---

## T1. 6 mAh/cm² bimodal 후막 전극이 안 돈다  ⏸ 보류
> **보류 사유:** 전극이 애초에 제대로 안 만들어짐(T2). **공정(T2) 해결 후** 전기화학 재평가. 아래는 기존 분석 보존.

**증상 (프로파일):** powder 대비 방전 비용량 큰 손실 · 충전 초기 IR 점프 + 기울어진 plateau +
CV 구간 비대(CC 분율↓) + CC 조기종료 · 고율에서 급격한 용량 감소. (transport-limited 후막의 전형)

**진단 — 후막에서 전달이 두께를 못 따라감** (1차 모델이 8 mAh에서 보인 메커니즘에 6 mAh도 진입):
1. **이온 병목(1순위):** 복합양극 유효 σ_ion = **0.057 mS/cm**(PTFE 1%, `db/electrochemistry/ptfe_conductivity.csv`)
   = LPSCl 자체(2.0)의 ~1/35. 후막 두께 **~250–420 µm**(`db/porosity/`)에서 분리막측 병목 → 집전체측 미활용.
2. **전자도 낮음:** σ_e = **0.04–0.05 mS/cm**(VGCF 1%). σ_e ≈ σ_ion ≈ 0.05 → dual bottleneck.
3. **대립 GB 저항 + 입자내 확산 제한:** P:S 7:3(Poly多)에서 집전체측 대립 미활용.
4. **Porosity ~20% = catholyte 불연속:** SE percolation 마진 부족.
5. **PTFE가 SE 접촉 차단:** PTFE 2%서 σ_ion 0.057→0.019 급감이 증거.

**해결 방향:** ① 다층/구배(분리막측 catholyte↑·집전체측 AM↑, 5/12 설계안) ② SE bimodal(large SE ~4µm)
③ 전자망 보강(VGCF↑/SWCNT) ④ 소립 집전체측·대립 bulk측 배치 ⑤ 면용량 단계상승(4→6)으로 한계점 특정.

**검증 실험:** 대칭셀 EIS로 두께별 R_ion/R_int 분리(6/18 측정 시작, `db/electrochemistry/eis_symmetric_cells/`)
→ ①이 지배인지 수치 확정 → 다층 설계로 검증.

**문헌:** Lee2025(PTFE σ 페널티) · Minnmann2021(σ_ion/τ 앵커) · Koo2026(후막 SWCNT) — `litdb/DRY_THICKFILM_INDEX.md`.

---

## T2. Poly/7:3에서 씽키 후 도우(떡)가 안 만들어진다

**Controlled 관찰 (변수 분리됨):**
- **단결정만** → 씽키(PTFE 포함) 후 **매번 도우 형성** ✅
- **Poly 추가(특히 7:3)** → 씽키 후 **도우 안 됨** ❌
- 단, **파우더 상태여도 85°C 핫롤링하면 전극은 형성됨** ✅

**확정된 사실 (가설에서 배제):**
- ❌ **파쇄 아님** — 대립 Thinky 2000rpm은 검증됨, Poly 안 깨짐 (사용자 확인).
- ❌ **공정 드리프트 단독 아님** — 변수가 Poly 추가로 깔끔히 분리됨.
- ❌ **SE 감소(27→18)도 아님** — ★ **같은 80:18에서 단결정은 도우 잘 됨** (사용자 확인). SE 18%는 단결정엔 충분.
- ✅ **트리거 = Poly 입자 자체** — 동일 80:18:1:1에서 단결정 → 도우 / Poly → 실패. **조성비가 아니라 입자 특성**.
- ✅ **★ Poly% 문턱 존재** — **3:7(Poly 30%) 도우 OK / 7:3(Poly 70%) 실패** (사용자 확인). 문턱이 30~70% 사이
  → **"단결정 backbone percolation" 확정** (단결정=섬유화 agent가 일정 비율 이상이어야 도우 형성).
- ✅ **★ 2nd Thinky 시간(time) 무효** — **5분 = 10분, 차이 없음** (사용자 확인). → **"양(time)"이 아니라 "강도(intensity) 문턱" 문제.**
  섬유화는 per-event shear가 문턱을 넘어야 일어남 → 강도가 문턱 아래면 시간 늘려도 분산만 반복(누적 안 됨).
- ✅ **★★ Ball mill = Poly-rich 도우 "부분적으로" 됨 (Thinky는 전혀 안 됨)** — 사용자 확인. **단, Poly 많으면 완전 도우는 X(gradient).**
  **★ 둘 다 지르코니아 볼 들어감**(Thinky 5pi×6+3pi×9 / ball-mill 5pi×5+2pi×15) → 차이는 **미디어 유무 아니라 거동(dynamics):**
  - **ball-mill = 볼이 tumbling/cascade → impact(충격)** → per-event 전단↑ → PTFE 직타 → Poly여도 부분 섬유화.
  - **Thinky = 강한 원심력에 볼이 벽으로 pinned → flow/press shear**(저강도·분산) → 무른 Poly가 쿠션 흡수 → 문턱 미달(전혀 안 됨).
  - ⚠ 함의: Thinky rpm↑ = 원심력↑ = 볼이 *더* 눌림 → 충격이 오히려 안 늘 수도 (Thinky로는 한계인 물리적 이유).
  → **도우 완성도 = gradient = f(전단강도, 단결정%, −Poly%).** ball-mill이 Thinky보다 강도↑로 **Poly 허용치를 높이나, 70% Poly는 ball-mill 충격으로도 full-dough 문턱 미달.**
  → "강도 문턱" 모델이 ball-mill(부분)>Thinky(0)·시간무효·단결정OK·Poly↑록 악화 를 전부 설명.
- ✅ **★★★ ball-mill 부분 도우 → 2nd Thinky 거치면 다시 파우더** (사용자 확인) = **Thinky가 도우를 *부순다*.**
  Thinky = (a) flow shear 섬유화(build, 하드 입자만) + (b) 고-g 분산(tear, 덩어리 풀어헤침) **동시 작용.**
  단결정: build>tear→도우 / **Poly: build≈0(쿠션)·tear 지배 → ball-mill 약한 도우 파괴 → 파우더.** (Poly 도우는 망 약해 resilience 0)
  ⇒ **★ actionable: Poly-rich엔 2nd Thinky 생략** (도우 파괴 방지). = 회의노트 "2nd Thinky 없이 ball-mill 2h" fallback의 *이유*.
- ✅ **온도가 섬유화 핵심 손잡이** — 85°C 롤링이 PTFE 모듈러스↓로 섬유화 완성
  (Lee2025: 30→120°C서 균일·바인더 모듈러스 −67%; Nam2026: 섬유화 = shear·온도·시간).
- ✅ **★ 전 실험 85°C 핫롤링 공통** (사용자 확인) — 단/3:7·7:3 **모두 85°C 핫롤**. 그런데 **결과가 다름:**
  단결정/3:7(cold 도우 O) → **정상 떡전극**, **7:3(cold 도우 X) → 핫롤해도 갈라져 나옴(crack/split)**.
  → **핫롤은 Poly-rich를 구제 못 함.** cold 도우 cohesion이 **crack-free 필름의 전제조건**. ("핫롤이 구제한다"던 앞 가정 폐기)

**메커니즘 (단일 후보로 수렴) — 도우 = PTFE 섬유화 = 미세접점의 국부 전단. Poly가 그 전단을 못 만듦:**
1. **단결정(3–4 µm, 단단·치밀) = micro-shearing agent** — 촘촘한 접점 + 강한 국부 전단으로 PTFE 섬유화 → 도우.
2. **Poly(10 µm, 무른 다공성)** — (a) 큰 입자 → 미세접점 밀도↓, (b) 무르고 다공성 → 전단을 쿠션처럼 흡수
   → PTFE 전단 문턱 미달. 7:3(Poly 70%)은 단결정(섬유화 backbone) 30%로 percolation 미달.
3. (가능, BET로 확인) Poly 표면적이 크면 **PTFE 예산 희석**도 보조 기여.

### T2-a. SE 가설 — ❌ 배제됨
- 처음엔 SE 27→18(부피 46→34%) 감소를 의심했으나, **단결정이 80:18에서 도우가 잘 되므로 SE는 트리거 아님.**
- 남은 별개 질문: **"SE↑가 Poly의 도우 실패를 *구제*하나?"** (트리거는 아니지만 완화책일 수는 있음 — 우선순위 낮음).
- 참고 tension(유효): 에너지밀도(AM↑) ↔ 건식 가공성. 단 SE 18%는 단결정엔 문제없음.

**⚠ 원래 최적 70:27:2:1 + PVDF 관련:** 바인더 PVDF↔PTFE는 거대 변수(PTFE만 전단 섬유화).
**❓ 미해결: 원래 PVDF 공정이 건식인가 습식(NMP)인가?** (현재 PTFE 건식과 비교 가능성 결정 — 단, SE는 이미 배제돼 우선순위↓)

**해결 방향 (우선순위):**
1. **PTFE 선(先)섬유화 masterbatch** — 단결정+VGCF(+SE 일부)로 섬유망 backbone 먼저, Poly는 마지막에 약하게. (메커니즘상 가장 직접)
2. **섬유화 단계 전단·온도↑** — ball-mill 200rpm은 약함; kneading 전단/온도/시간↑.
3. **고-Poly엔 PTFE 약간↑**(1→1.5%, σ_ion 페널티 감수).
4. (보조) SE 보충이 구제하는지 확인.

**검증 실험 (우선순위 재조정):**
- ★ **Poly% sweep — 진행 중:** PTFE 1% 고정. **3:7 도우 OK ✅ · 7:3 실패 ❌** → **다음: 5:5 테스트로 문턱 국소화**
  (5:5 도우 되면 문턱 50~70% Poly, 안 되면 30~50% Poly).
- ★ **Poly BET 측정** — Poly BET ≫ 단결정(0.56)이면 PTFE예산 기여, 비슷/낮으면 **순수 입자크기·전단**으로 확정.
- **PTFE% sweep:** 7:3 고정, PTFE 1/1.5/2% → 섬유화 PTFE 문턱.
- (강등) SE sweep — SE가 Poly 도우를 *구제*하는지만.

### T2-c. 공정 함의 — porosity 최적점(7:3)이 곧 제작 실패 영역
- **7:3 = Furnas dip 최소 porosity(19.7%, `db/porosity/`) = packing 최적** = **동시에 crack-free 필름 제작 실패 영역**.
- ⇒ **설계 최적(Poly-rich)과 건식 제작성이 정면 충돌.** 단일층 7:3은 현재 공정으로 **온전한 전극이 안 나옴**(갈라짐).
- **공정이 1차 관문.** 전기화학(T1) 이전에 **"갈라지지 않는 7:3 필름을 어떻게 만드나"**가 먼저.

---

## ★ T2 심층: 공정(건식 제작) 분석 — "어디서 깨지나"

### (1) 공정 단계 맵 (PTFE 섬유화·필름 결착 관점) — 현재 레시피 `db/.../composite_recipe.csv`, PDF_B
| 단계 | 동작 | 역할 | 전단 | 온도 | Poly-rich 7:3에서 |
|---|---|---|---|---|---|
| 1 | 핸드믹싱 | 1차 분산 | 저 | RT | OK |
| 2 | Thinky 2000rpm 5min (PTFE 전, 지르코니아) | 분산 | 중 | RT | ✅ 검증(안 깨짐) |
| 3 | +PTFE → ball mill 200rpm 1h | **분산**(PTFE 균일 분포) | 저~중 | RT(+발열) | 분산은 됨 |
| 4 | **2nd Thinky (+PTFE 추가)** | **★ shear → 섬유화 → 도우 (의도된 도우 단계)** | **고(shear)** | RT | ❌ **shear가 Poly cushioning에 막혀 도우 미형성** |
| 5 | 핸드믹싱 → (떡) → **핫롤 85°C** (8방향×5단계×5회) | 성형·마무리 | 고 | 85°C | ❌ **도우 없는 분말 압연 → 갈라짐** |
| 6 | 추가 롤링 → 타발 | 두께/로딩 | 고 | 85°C | ❌ |

→ **실패 지점:** 표준 루트는 **2nd Thinky(flow shear)에 최종 도우를 의존** — 단결정엔 OK, **Poly엔 무력**. Poly는 **ball-mill impact(2h)** 가 부분 도우. 도우 부족 상태로 5 압연 → **갈라짐**. 핫롤도 *없는* 망 새로 못 만듦.

### (2) 통합 메커니즘 — 왜 Poly는 안 되나 (★ 정정: CAM 경도 의존)
섬유화 = **per-event shear > 문턱.** 전단 2종: **(i) Thinky flow/press shear**(하드 입자가 PTFE에 전달) · **(ii) ball-mill 미디어 impact.**
- **단결정(하드):** Thinky flow shear를 PTFE에 잘 전달 → **Thinky서 도우** (+ball-mill 도움).
- **Poly(소프트·다공성):** Thinky flow shear를 쿠션 흡수 → **Thinky 미달**; **ball-mill IMPACT에 의존 → 부분 도우**(2h 필요, 70%는 부분). 7:3은 단결정 30%로 percolation 미달.
- 둘 다 지르코니아 有, 단 **Thinky 미디어=원심 pinned(저impact)·ball-mill=tumbling(고impact).**
- ⚠ **peak 전단 ≠ rpm (Thinky 2000 vs ball-mill 200):** rpm 숫자가 아니라 *전달 모드*가 peak를 정함.
  Thinky 2000rpm = 고 g → flow/press(연속·중간 peak) + 고g가 **미디어 pin**. Ball-mill 200rpm = cascade → **discrete IMPACT**(점타격·고 strain-rate = 고 peak).
  **역설(critical speed):** 볼밀은 임계속도 이상이면 미디어가 원심으로 벽에 붙어 cascade 멈춤(밀링 X). Thinky 2000rpm은 그 영역 위 → **미디어 pinned → impact≈0, flow만.** ⇒ **더 빠른 rpm이 오히려 peak impact를 죽임.** (블렌더 vs 망치 비유) ※ 메커니즘 추론(실측 전단값 없음); 관찰=ball-mill 도우/Thinky X가 ground truth.

### ★ 핵심 합성 (synthesis) — 단계 역할은 CAM 경도에 의존
- **단결정:** 2nd Thinky(flow shear) = 도우 단계.
- **Poly-rich:** Thinky flow shear 부족 → **ball-mill IMPACT가 섬유화 엔진**(2h 부분 도우). 2nd Thinky는 Poly엔 거의 무력.
**레버 (Poly-rich 도우, 우선순위):**
- **★ 0순위(공짜): Poly-rich엔 2nd Thinky 생략** — Thinky가 ball-mill 도우를 *tear*하므로. ball-mill → 바로 롤링.
- **★ ball-mill(impact) = Poly 섬유화의 맞는 도구** (Thinky 아님). 시간↑ 누적(문턱 위, 2h). 단 70%는 부분.
- **★ 온도↑(문턱↓)** = ball-mill **+ 외부가열**로 7:3 full dough 시도 (가장 유망한 단일층).
- Thinky rpm↑ = **Poly엔 약함/해로움**(flow shear 부족 + tear + rpm↑이 미디어 더 pinned). 단결정엔만 유효.
- 그래도 부분이면 → **다층/조성**(도우층 Poly% 낮춤).

### ★ Poly에서 2nd Thinky rpm↑의 효과 분해
1. **★ shear force↑ → 섬유화 drive↑** — 2nd Thinky의 본 목적. **도우의 직접 동인**(단결정은 이걸로 충분).
2. **단, Poly가 shear 흡수** — 크고 무른 다공성이 충격을 변형·재배열로 먹음 → 전환효율 단결정 > Poly. 천장까지 올려도 문턱 못 넘을 수.
3. **마찰열↑ → 문턱↓ (보너스)** — rpm↑=발열↑→PTFE 모듈러스↓. → 고rpm이 도우면 shear+열 합작.
➕ 역효과: Poly 표면 기공으로 PTFE 밀려들어가 낭비 가능.
⇒ **2nd Thinky rpm↑은 도우의 직접 레버(맞음).** 관건 = **Thinky shear 천장 vs Poly cushioning.** 이기면 도우, 지면 → 온도(A)로 문턱 낮춰 보완.
⇒ rpm sweep 시 **합제 온도 필수 측정** = shear 효과 vs 열 효과 분리.

### (3) ★ 공정 knobs (DOE — 이걸 깊게 판다)

> **핵심 trade-off = 섬유화 강도 ↔ 균일도.** "한번에 섞고 섬유화"는 균일하나 Poly-rich서 섬유화 부족,
> "선섬유화 masterbatch"는 섬유화 강하나 **Poly 나중 투입 시 분산 불량(균일도↓)**. → **둘 다 잡는 레버 = 온도(A).**

**A. ★★ 섬유화 단계 온도 — 단, "외부 가열된 kneading"으로 (1순위 검증):** PTFE 섬유화는 온도 의존(Lee2025: 온도↑→모듈러스 −67%).
   가온하면 같은 shear로도 문턱 넘어 섬유화 기대 + **균일도 유지**(masterbatch 회피).
   - ⚠ **Thinky 자가발열은 plateau** — 마찰열=방열 steady-state에 수분 내 도달 → **오래 돌려도 더 안 뜨거움**(= 5=10분 시간무효의 한 원인). **자가발열은 고정 baseline, 레버 아님.**
   - ⚠⚠ **핫롤 85°C도 7:3 실패(이미 관찰)** → **"열만 주면 된다"가 단순 성립 X.** 해석: fibrillation은 **kneading(2nd Thinky 3D 전단) geometry**서 일어나야 하고, **롤링(2D 면내)은 없는 망을 새로 못 만듦**(85°C여도).
   - ⇒ 진짜 테스트 = **2nd Thinky(3D 전단)를 외부가열로 온도 고정(60–70°C)** 했을 때 도우 잡히나. (자가발열 plateau 위 + 롤링 아닌 kneading 단계) → 핫플레이트/가열자켓/예열. **IR로 Thinky plateau 온도 먼저 측정.**
   - **솔직 가능성:** 가열 kneading도 실패 시 → 7:3 단일층은 이 공정으로 본질적 불가 영역 → **다층/조성 변경**(85°C 롤링 실패가 이미 신호).
**B. ★★ 2nd Thinky rpm (= 도우의 shear 레버, native knob):** 2nd Thinky가 **shear로 섬유화→도우 만드는 단계**.
   rpm↑ → **shear 직접↑ = 섬유화 drive↑** + 마찰열↑(문턱↓ 보너스). → **도우 문제의 직접 1순위 knob.** rpm↓는 불리.
   관건 = **Thinky shear 천장이 Poly cushioning을 이기나** (못 이기면 온도 A로 보완).
   ⚠ **시간(time)은 무효 확인됨** (5=10분) — 강도 문턱 문제라 시간 누적 안 됨. → **rpm(강도)만 의미, 시간 늘리기 X.**
   진단: 합제가 *불균일*=분산 문제(1st Thinky/ball-mill) / *균일한데 안 뭉침*=2nd Thinky shear 강도 부족 / *고rpm서 공처럼 뭉침/벽 타고 오름*=섬유화 onset(좋은 징조).
   - **1st Thinky·ball-mill(200rpm)은 분산 단계** — 시간↑/rpm↑ = 균일도↑이지 도우 주레버 아님. 파쇄 리스크 낮음(200rpm 저속; PC 균열은 300–500 MPa 가압 — Lee2025).
   - ⚠ **섬유화 window (과전단 주의):** PTFE 섬유화는 부족→망없음 / **과다(over-fibrillation·over-kneading)→fibril 끊김·balling·MW저하**
     로 망 저하. **단, 지금 Poly-rich는 under 상태**(도우 X)라 당장은 부족이 문제 → rpm↑ 시도 OK. 가드: **점진적↑ + 도우 뭉치면 즉시 정지**
     (max·장시간 금지; 시간이 rpm보다 over의 주범). 과전단 신호 = balling / 뭉쳤다 다시 부슬 / 과열 / Poly 균열. (Nam2026 kneading-time = 최적 존재)
**C. ⬇강등 PTFE 선(先)섬유화 masterbatch:** 단결정+PTFE+VGCF로 그물 먼저 → Poly 나중. agent percolation은 확보되나
   **★ 굳은 그물에 다수 Poly(70%)를 나중에 섞어 균일도 불량 위험**(사용자 지적). 쓰려면 **Poly 분할투입 + EDS 맵/단면으로 균일도 검증** 필수.
**D. PTFE 양/첨가법:** Poly-rich엔 PTFE↑(1→1.5%) 또는 분할/투입시점 조정.
**E. 롤링 파라미터:** 온도↑(85→100+?), **1회 압하량↓(천천히)**, 패스 수·방향 — 갈라짐은 과한 1회 변형률일 수도.

### (4) 다음에 *관찰/측정* 할 것 (진단 데이터)
- **합제 실제 온도** 측정: ball-mill 발열, kneading, 롤 표면 (A 검증의 핵심).
- **섬유화 단계 후 SEM**: PTFE fibril 유무·밀도 (단결정 vs 7:3) — 어디서 그물이 없는지 눈으로.
- **갈라진 필름 엣지/단면 관찰**: 어디서·어떻게 갈라지나(층분리? 입자경계? 엣지부터?).
- **Poly BET / 입도**: agent 희석 정량.

### (5) 검증 실험 (공정 우선)
- ★★ **온도 sweep (A) — 1순위:** 7:3 고정, 섬유화 단계 RT / 40 / 60°C → cold 도우 잡히는 온도 문턱. (균일도 유지 레버)
- **Poly% sweep:** PTFE 1% 고정. **3:7 OK ✅ · 7:3 ❌** → **5:5 테스트로 문턱 국소화**.
- **PTFE% sweep:** 7:3 고정, 1/1.5/2%.
- **롤링 압하량 sweep (E):** 1회 변형률↓ → 갈라짐 완화되나.
- (조건부) **masterbatch (C):** 한번에 vs 선섬유화 비교 — **단 EDS 맵/단면으로 균일도 같이 평가**(균일도 깨지면 기각).

**문헌(공정 관점):** Lee2025(PTFE 섬유화 5단계 모식·온도→모듈러스·co-rolling) · Nam2026(DPE 섬유화 = **shear·온도·kneading time**,
4단계 공정) · Koo2025/2026(건식 병목=분산, 단결정 맞춤 공정) · Lim2025(virtual calendering). **※ "Poly라서 도우/필름 안 됨"
직접 논문은 litdb에 없음 — 우리 고유 관찰.** → 이 주제로 새 PDF 있으면 "논문 에이전트"로 먹이면 됨.

---

## T3. 모델 σ vs 실측 σ 불일치
모델 가정 σ_ion 0.25 / σ_e 10 mS/cm vs 실측 0.057 / 0.05. 상세·수정은 `docs/project/05_ISSUES_AND_FIXES.md #2`. 2차년도 재보정 대상.

---

## 타임테이블 개선점 (6/25 계획 기준, `docs/project/meetings/2026-06-25.md`)
1. 면용량 2만 말고 **2→4→6 두께 사다리** 병행(후막 breakdown 지점 탐색).
2. **GITT** 필수항목인데 미포함 → 일정에.
3. **3:7/5:5/7:3 대칭셀 EIS 우선순위 상향**(이온전달 1순위 의심).
4. **기준온도 고정**(30 vs 60°C 혼재 — 후막 transport는 온도 민감).
5. **후막에서도 C-rate sweep**.
6. **Poly 분산 정량 go/no-go**.
7. 양극 스크리닝 중 **음극 한쪽 고정**(In-Li vs Li).

---

## 📅 업데이트 로그
- **2026-06-26** — 문서 생성. T1(후막 transport 병목) / T2(Poly·SE 도우 실패, 파쇄 배제·온도 핵심 확정) /
  T3(모델 σ) / 타임테이블 정리.
- **2026-06-26 (갱신)** — T2: ★ **SE 가설 배제** (단결정은 80:18에서도 도우 잘 됨 — 사용자 확인).
  트리거 = **Poly 입자(크기/형태) 단독**으로 확정, 메커니즘 단일 후보(shear-agent 부족)로 수렴.
  검증 우선순위 재조정: Poly% sweep + Poly BET 우선, SE sweep 강등.
- **2026-06-26 (갱신 2)** — T2: ★ **3:7 도우 OK / 7:3 실패 확인** → 문턱 30~70% Poly,
  **단결정 backbone percolation 확정**. T2-c 추가: **porosity 최적(7:3) = 도우 실패 영역**. 다음: **5:5 도우 테스트** + Poly BET.
- **2026-06-26 (갱신 3)** — ★ **전 실험 85°C 핫롤 공통**(사용자 확인) → "7:3만 열등 루트" 가설 **철회**.
- **2026-06-26 (갱신 4)** — ★★ **문제 재정의 = 공정.** Poly-rich(7:3)는 cold 도우 X → **핫롤해도 갈라져 나옴**
  (핫롤이 구제 못 함). **전기화학(T1) 보류, 공정(T2) 집중.** T2 심층 섹션 추가: 공정 단계 맵(실패 지점 = 3·4 섬유화 생성)
  + 공정 knobs(온도·전단·masterbatch·PTFE·롤링압하) + 관찰/측정 항목 + 공정 DOE.
  다음 1순위: **섬유화 단계 온도 sweep(7:3 @ RT/40/60°C)** + 합제온도/SEM 관찰.
  미해결: ① 섬유화 온도 문턱 ② 5:5 도우 ③ Poly BET ④ 합제 실제온도 ⑤ 갈라짐 양상.
- **2026-06-26 (갱신 5)** — 사용자 지적: **masterbatch(C)는 균일도 희생** (굳은 그물에 다수 Poly 나중 투입 → 분산 불량).
  → **trade-off 명시(섬유화↔균일도)**, **온도(A)를 단독 1순위로** 승격(단일공정 유지 = 균일도 보존하며 섬유화). masterbatch는 강등(쓰면 균일도 검증 필수).
- **2026-06-26 (갱신 6)** — 사용자: ball-mill·1st Thinky = 분산. 파쇄 리스크 낮음(정정).
- **2026-06-26 (갱신 7)** — ★ **공정 역할 재정정:** **2nd Thinky = shear로 도우 만드는 단계**(사용자). "전용 섬유화 단계 부재" 철회.
  단계맵·synthesis·knob B 정정: **2nd Thinky rpm = 도우의 직접 shear 레버(B)**, 온도(A)는 문턱↓ 보완 → **rpm↔온도 한 쌍.**
- **2026-06-26 (갱신 8)** — ★ **2nd Thinky 시간 무효 확인**(5=10분, 사용자) → **강도(intensity) 문턱 문제**(양 아님).
  **시간 레버 제외.** 남은 레버 = rpm(강도↑) / 온도(문턱↓).
- **2026-06-26 (갱신 9)** — 사용자: Thinky 자가발열? → **plateau(수분 내 steady-state)라 시간↑로 더 안 뜨거움**(시간무효 한 원인).
  ★ 교차검증: **핫롤 85°C도 7:3 실패** → "열만 주면 됨" 단순 X. 해석: fibrillation은 **kneading 3D 전단**서 일어나야, **롤링 2D는 없는 망 못 만듦**(85°C여도).
  → 온도 테스트 재정의: **2nd Thinky 외부가열(60–70°C) kneading** (자가발열 plateau 위, 롤링 아님). 실패 시 7:3 단일층 본질 불가 → 다층/조성.
  다음: ① Thinky plateau 온도 IR 측정 ② rpm sweep ③ 외부가열 kneading.
- **2026-06-26 (갱신 10)** — ★★ **ball-mill은 Poly 도우 (부분) 됨 / Thinky는 X** (사용자) = 진단 핵심.
  메커니즘 통합: 섬유화=shear>문턱, 전단 2종(Thinky flow / ball-mill impact). 단결정=Thinky flow로 도우, Poly=ball-mill impact 의존(부분, 70%는 gradient).
  정정들: **둘 다 지르코니아 有**(차이=거동, impact vs 원심pinned) · **단계역할 CAM경도 의존**(Poly엔 ball-mill이 섬유화 엔진) ·
  **peak전단≠rpm**(Thinky 2000>ball 200이어도 critical-speed 위라 미디어 pinned→impact 죽음) · **ball-mill도 70% Poly엔 부분 도우(gradient)**.
  레버 재정리(Poly-rich): ① ball-mill(impact) ② +외부가열(문턱↓) ③ 그래도 부분이면 다층/조성. Thinky rpm은 Poly엔 약함.
- **2026-06-26 (갱신 11)** — ★★★ 사용자: **ball-mill 부분 도우가 2nd Thinky서 다시 파우더** → **Thinky가 도우를 부순다(tear).**
  build(섬유화)vs tear(분산) 모델: 단결정 build>tear→도우 / Poly build≈0·tear지배→파괴. **actionable: Poly-rich엔 2nd Thinky 생략(0순위·공짜)** =
  회의노트 "2nd Thinky 없이 ball-mill 2h" fallback의 이유 규명. 경로: ball-mill(±가열)→바로 롤링.
