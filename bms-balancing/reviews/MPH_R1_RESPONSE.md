# 마이크로 쇼츠 mph 분석 — 1차 외부 리뷰 대응 원장 (2026-09-13)

| 항목 | 값 |
|---|---|
| 판정 | **NO-GO** — "M1 은 확정 버그이므로 `cEeqref` 두 줄부터 고친다" 가 당시 증거로 성립하지 않음 |
| 리뷰 대상 | `docs/MICROSHORT_MPH_REVIEW.md` (v1) sha256 `67c58eb7af01…` · git blob `8f497ed2b85d…` |
| 리뷰 대상 요청문 | `reviews/REQ_MPH_MICROSHORT.md` sha256 `6d5e115b50b3…` |
| 대상 커밋 | `94add7b5d48ad5d19448d562a0909b15ce4dc056` |
| 패키지 (원본 보존) | `reviews/r14_repros/codex/MICROSHORT_MPH_REVIEW_PACKAGE.zip` sha256 `e2d74fb8390e63bc5dbd53a12401ea01809f16f78dc015a1756b0cbf14af45fb` (8 파일, 개별 sha256 은 `pkg/` 옆) |
| 우리 대응 | v2 `docs/MICROSHORT_MPH_REVIEW.md` · `reviews/REQ_FIT_RAILS.md` 수정 · `reviews/r14_repros/mph_dump.py` 신설 |
| 우리 실행 | 리뷰어 스크립트 `pkg/mph_review_checks.py` rc 0 재현 · `mph_dump.py --self-test` rc 0 · `.xlsx` 재검증 |

**세 digest 가 우리 tracked 파일과 정확히 일치했다** (실측). 리뷰어는 맞는 바이트를 봤다.

**우리에게 있고 리뷰어에게 없던 것**: 원본 `.mph`/`dmodel.xml`. 그래서 리뷰어가 "원본 확인 필요"
로 남긴 항목 중 **넷을 이번에 닫았다** (R-1 · R-6 · R-9 · R-13). 나머지는 COMSOL 실행이 필요하다.

---

## 1. 수용 — 우리 오류 (v2 에서 고침)

| ID | 지적 | 우리 확인 | 고친 곳 |
|---|---|---|---|
| **R-1** | A1(=`cEeqref` 가 SOC 분모) 에서 "따라서 활성 OCP 가 `x/dm` 을 읽는다" 가 안 나온다. COMSOL 은 사용자 정의 OCP 경로를 지원하고 공식 1D 예제가 `Eeq_neg(cs_surface/csmax_neg)` 를 직접 입력한다 | **맞다.** v1 은 논리 단계를 건너뛰었다. **다만 이 모델은 그 경로가 아니다** — §2 R-1 참조 | v2 §3 M1-2 신설 (실측 4건 + 남은 구멍 + 30초 확인법) · §0 · §5-3 순서 1번 |
| **R-2** | 미사용 `cs_NCM_init` 은 누락의 **단서**이지 의도적 사이트 감소 모델을 배제하는 증거가 아니다 | **맞다.** v1 은 "버그라는 증거" 라고 썼다 | v2 §3 M1-4 — 현상론적 대안 모델을 명시하고 "가르는 것은 LAM 계약 정의" 로 이동 |
| **R-3** | "마지막 6–8 h 기울기는 쇼츠 전용" 은 **반증된다**. (i) 무쇼츠 완화 `20mV·exp(−t/10h)` 가 6h/12h 에 −1.098/−0.602 mV/h · (ii) `C_diff` 가 LLI/LAM 에 의존 · (iii) "일정하면 쇼츠 아님" 도 성립 안 함 | **맞다.** 특히 (ii) 는 **우리 문서 자신의 `dV/dt = −I_leak/C_diff` 식이 갖고 있던 경로**다. 우리가 우리 식을 안 봤다 | v2 §5-2 ② 전면 재작성 — 반증 셋을 그대로 싣고 "쇼츠 전용 축" → "후보 관측량 + 명시된 교란" |
| **R-4** | `tau_short = C_cell·V/i_leak` 은 **V·h** 라 시간 단위가 아니다 | **맞다.** 명백한 차원 오류 | v2 §5-2 ③ — `t_Q = C_cell/I_leak`, `tau_V = R·C_diff`, 비선형이면 단일 시상수 아님, A/m² ↔ 셀단위 짝 맞추기 |
| **R-5** | v1 §7 추출기가 부모를 **첫 `</PhysicsFeature>`** 까지 잘라 (a) 자식 param 을 부모 것으로 (b) 자식 DISABLED 를 부모 것으로 (c) 자식 뒤 부모 param 을 버린다 | **맞다. 반례 재현 완료** — `par1` 이 DISABLED 로, `csinit` 이 부모 것으로, `rp` 가 사라졌다 | `reviews/r14_repros/mph_dump.py` (ElementTree, `--self-test` 가 이 반례 고정) · v2 §7 이 그것을 가리킨다 |
| **R-6** | (R-5 의 귀결) 노드별 활성/소비 관계가 검증됐다고 할 수 없다 | **맞고, 실제로 결론 하나가 틀렸다** — 다시 걸어 보니 **`<Physics tag="ev">` Events 인터페이스 자체가 DISABLED** 다. v1 은 "활성이지만 무력" 이라고 썼다 | v2 §1-2 표 · §3 M5 전면 수정 (`CurrentDirection` 이름 충돌도 해소됨 — 전역 파라미터가 쓰인다) |
| **R-7** | M2 권장안대로 `epss=1` + 보정 제거를 하면 **유효 전도도를 3.3127배 늘린 새 모델**이 된다. `epss=1, epsl=0.45` 는 분율 합 1.45 | **맞다.** v1 은 baseline 보존을 안 따졌다 | v2 §4-2 — `sigma_eff = 0.301869177·sigma_short` 로 계수를 **옮기라**고 명시 |
| **R-8** | cmax-only 대안에서 **BOL 기준 `nLi_0` 까지 aged dm 으로 바꾸라**는 부분은 틀렸다. 기준 재고의 재정의이지 보존을 위한 필수 작업이 아니다. 또 `csinit` 에 `dm` 만 곱하면 Li 재고가 **2.96 % 더** 준다 | **맞다** | v2 §4-1 대안 — 리뷰어가 준 `θ_p,0` 식으로 교체, 2.96 % 수치 명시 |
| **R-9** | M4 는 문자열 등장 횟수로 판정했다. **등장 횟수 ≠ 소비자 수** | **맞다.** live 참조 그래프로 다시 셌다 (`<actions>` 이력 제외) | v2 §3 M4 — `dPE`·`dNE`·`cs_NCM_init`·`cs_Gr_init`·`E_end`·`x_NCM_max`·`x_NCM_min` **live 0**, `i_app` **2 (활성 ge2 포함)** |
| **R-10** | M3 의 "다른 곡선 위의 LAM 은 반드시 이식 불가" 에 반례. `U₂(w)=U₁(a·w+b)` 면 `Q₂=a·Q₁` 이고 정규화 비율에서 `a` 가 상쇄된다 | **맞다.** raw α 의 곡선 의존성과 정규화 LAM 비율을 섞었다 | v2 §3 M3 — 반례를 싣고 주장을 "점검할 가치가 큰 후보" 로 축소. 주원인 순위·라이브러리 원본 여부도 미검증으로 표시 |
| **R-11** | M6 "무의미" 는 과하다. `∫I(V−V₀)dt = W − V₀ΔQ` 는 기준전압 기준 에너지로 정의된다 | **맞다** | v2 §3 M6 — "단자 에너지·효율로 해석할 근거 없음" 으로. 더 강한 검증점(`i_app` 이 CV·휴지 전류와 불일치)을 대신 넣었다 |
| **R-12** | v1 §0·§3 이 OCP 재표본화를 **충전 곡선·ICA 봉우리 변화**로 확대했다. §8 의 한계가 §0·§3 에 적용 안 됐다 | **맞다** | v2 §3 M1-3 끝 문단 + §0 + §8 — "t=0 평형 OCP 차이다. 궤적·봉우리 이동량은 미검증" 을 세 곳에 |
| **R-13** | 요청문에 `LLI`·`C_lit0_ref1` 숫자가 없어 `x_NCM_init = 0.924064` 를 독립 도출할 수 없었다 | **맞다.** 자료 민감도로 뺐는데 그 결과 사슬이 검증 불가가 됐다 | v2 §2 표에 두 값 명시 · §3 M1-5 에 `nLi_target`·`dLi` 도 |
| **R-14** | (별건) `LAM_PE=LAM_NE=1−x_cell` 에서 `LLI=1−x_cell` 은 **안 나온다** | **맞다. 실측 확인** — ref1 난간 행에서 `LLI−(1−x_cell)` = 0.0216 ~ 0.0355 | v2 §2-2 정정 · `reviews/REQ_FIT_RAILS.md` 제목·§2·§3 수정 |
| **R-15** | (별건) `np.allclose` 기본 허용오차는 머신 엡실론 증명이 아니다 | **맞다** | `REQ_FIT_RAILS.md` §5 · v2 §7 — 최대 절대오차를 직접 찍는 코드로 교체 |
| **R-16** | M5 의 "두 지시자가 같은 문턱" 은 오류가 아닐 수 있다 (방향 반대 crossing) · Stop Condition 은 implicit event 를 별도 경로로 선택 가능 | **맞다** | v2 §3 M5 — 단정 제거, Stop Condition 확인 필요를 명시 |
| **R-17** | M7 "음수" 는 `Cap` 초기값도 필요. 부호를 고쳐도 **휴지 중 내부 누설이 빠진 외부전류 적분은 물리적 SOC 가 아니다** | **맞다** | v2 §3 M7 — 초기값 명시 + 내부 누설 문단 추가 |
| **R-18** | M8 은 solution 이름만으로 파라미터를 확정하면 안 된다 | **맞다** | v2 §3 M8 끝에 단서 표시 |
| **R-19** | M2 의 "복붙"·"과대표기" 는 의도/표기 계약 없이 단정 불가. `σ·epss` 가 아니라 `σ·epss^b` 이고, 보정이 없으면 `epss` 가 아예 빠져 축퇴도 사라진다 | **맞다** | v2 §3 M2 — 정정 세 개를 명시 |

---

## 2. 새 증거로 좁힌 것 — 원본 `.mph` 가 우리에게 있다

### R-1 (A1 → 실제 소비 경로) — **v1 때보다 훨씬 강해졌다. 다만 여전히 실행 확인은 아니다**

리뷰어의 반례 경로는 "`Eeq` 를 User defined 로 두고 `Eeq_neg(cs_surface/csmax_neg)` 를 직접
입력" 이다. `mph_dump.py` 로 다시 읽은 결과 **이 모델은 그 경로가 아니다**:

| # | 실측 | 뜻 |
|---|---|---|
| 1 | `pce1/per1.Eeq_mat = from_mat` (`MaterialOption = mat1`) · `pce2/per1.Eeq_mat = from_mat` (`dommat` = mat5) | 사용자 정의 식이 아니다 |
| 2 | `mat1`·`mat5` 의 평형전위 물성이 문자 그대로 `Eeq_int1(soc)+dEeqdT_int1(soc)*(T-298[K])` | 인자가 COMSOL **내장 `soc`** 다 |
| 3 | `per1.cEeqref = 2.5e4[mol/m^3]` 이 **네 반응 노드 전부** 동일 (`pce1/per1`·`pce2/per1`·`addm1/per1`·`es1/er1`) — `es1/er1` 은 `LithiumMetal` 로 화학이 완전히 다르다 | **공장 기본값이고 편집된 적이 없다.** 편집된 것은 `pin1.cEeqref` 쪽뿐 |
| 4 | `per1.cs_ref = liion.csmax/2` — 반응 노드가 자기 `cEeqref` 가 아니라 생성 변수 `liion.csmax` 를 참조 | `csmax` 는 입자 노드가 정의하는 단일 변수 |

대조 증거: **사용자 정의 경로를 실제로 쓰는 노드가 같은 파일에 있다** — `addm1/per1` 은
`Eeq_mat = userdef`, `Eeq = Eeq_Si`. 작성자는 두 경로를 구분해 썼고 두 전극은 `from_mat` 을 골랐다.

**남은 구멍**: `ParticleConcentrationType = SolveinExtraDimension` 에서 COMSOL 이 `soc` 의 분모로
`pin1.cEeqref` 를 쓴다는 것은 위 넷의 정합적 해석이지 실행 확인이 아니다.
**끝내는 방법**: GUI 에서 `liion.pce2.pin1.soc` (또는 `liion.soc_average_pce2`) 의 t=0 값이
`0.924064` 인지 `0.952290` 인지 찍는다. **판정은 이 한 값에 달려 있다.**

### R-6 (노드 활성 상태) — **닫혔고, 결론이 하나 바뀌었다**

`mph_dump.py` 가 자기 flags 와 조상 사슬을 분리해 낸 결과 **`<Physics tag="ev">` = `DISABLED`**.
하위 `ds1`·`is1`·`impl1`·`impl2` 는 자기 flags 가 없다. v1 의 "활성이지만 무력" 은 틀렸다.
귀결: `CurrentDirection` 이산 상태가 존재하지 않으므로 이름 충돌이 **해소**되고 전역 파라미터
(`=1`)가 쓰인다.

### R-9 (소비자 그래프) — **닫혔다**

`<actions>`(이력) 제외 + 식별자 경계 정규식으로 live 참조를 셌다:
`dPE` 0 · `dNE` 0 · `cs_NCM_init` 0 · `cs_Gr_init` 0 · `E_end` 0 · `x_NCM_max` 0 · `x_NCM_min` 0 ·
`i_app` **2** (비활성 `ecd1` 1 + **활성 `ge2` 1**).

### R-13 (x_NCM_init 독립 도출) — **입력을 공개했다**

`LLI = 0.0439355` · `C_lit0_ref1 = 0.003765381 [Ah]` · `A_cell = 1.53938 cm²` ·
`F = 96485.33212 C/mol` → `dLi_LLI = 0.040098 mol/m²` · `nLi_target = 1.188226 mol/m²` →
`x_NCM_init = 0.924064`. 리뷰어가 역산으로 얻은 값과 일치한다.
(COMSOL 이 실제로 그 값을 쓰는지는 여전히 미확인.)

---

## 3. 우리가 실행한 것

| 검사 | 명령 | 결과 |
|---|---|---|
| 리뷰어 스크립트 재현 | `python3 reviews/r14_repros/codex/pkg/mph_review_checks.py` | **rc 0**. `cell_delta_mV = -14.274885033952689` · `lost_host_fraction_ne/pe = 0.0507823/0.0584011` · `fraction_of_01C = 0.0270/0.0901/0.2701` — 전부 우리 v1 값과 일치 |
| 추출기 반례 (R-5) | v1 정규식 추출기를 중첩 XML 에 적용 | **RED 재현** — `par1` DISABLED 오인 · `csinit` 부모 귀속 · `rp` 소실 |
| 교정 추출기 | `python3 reviews/r14_repros/mph_dump.py --self-test` | **rc 0** (`test_extractor_ownership: OK`) |
| 교정 추출기 실행 | `mph_dump.py dmodel.xml --refs …` | `/ev Events DISABLED(own)` · live 참조 표 (§2 R-9) |
| 재료 OCP 인자 | ElementTree 로 `mat1`/`mat5` 물성 | `Eeq_int1(soc)+dEeqdT_int1(soc)*(T-298[K])` |
| LLI 반증 (R-14) | ref1 37행 | `LLI-(1-x_cell)` 난간 행에서 0.0216 ~ 0.0355 |
| 닫힌 형태 최대오차 (R-15) | ref1 | `x_cell 0.000e+00` · `LAM_PE 1.388e-16` · `LAM_NE 5.551e-17` · `LLI 4.163e-17` |
| digest 대조 | `sha256sum` | 리뷰 대상 문서·요청문·git blob 3개 전부 일치 |

---

## 4. 판정 수용

**"확정 버그·수정 지시서로서는 NO-GO" 를 받아들인다.** v2 는

- M1 을 **조건부 진단**으로 재작성했다 (조건 = A1 의 실제 소비 경로, 확인 30초).
- 수정 우선순위 1번을 **"고쳐라" 에서 "`liion.pce2.pin1.soc` 를 찍어라" 로** 바꿨다.
- LAM 계약 정의(`H/H₀ = 1−LAM` 인가)를 2번에 놓았다 — 정의 없이는 §4-1 이 "수정" 인지
  "모델 변경" 인지 정해지지 않는다.
- 반증된 것(휴지 감쇠 전용축)·틀린 것(차원, 세 모드 붕괴, Events 활성)은 정정 표시와 함께
  본문에 남겼다. 지우지 않는다.

**닫지 않은 것** (v2 §8): COMSOL 미실행 · A1 실행 확인 · 버그/설계 판별 · Bruggeman 지수 ·
`sep1`/`pcb1` 합성 여부 · Stop Condition · OCP 라이브러리 원본 대조 · `dPE` 출처 · 원 전압 곡선 ·
MPH sha256 과 study/solution/dataset 기록.

## 5. 이 라운드의 교훈

**분석 도구를 검증하지 않으면 도구가 낸 사실도 못 믿는다.** v1 §7 추출기의 소유권 결함이
M5 의 결론을 틀리게 만들었고(`ev` 가 꺼져 있는데 "활성이지만 무력" 이라고 적었다), 그것을
리뷰어가 **원본 파일 없이 정적 반례만으로** 잡아냈다. 이 저장소가 `reviews/evidence_gate.py`
에 적용하는 규율 — 도구 자신을 봉인하고 반례로 고정한다 — 을 분석 스크립트에는 적용하지
않았다. `mph_dump.py` 는 `--self-test` 를 갖고 태어났다.


---

## 6. 2차 리뷰 (v2 패키지 `reviews/r14_repros/codex_v2/`, zip sha256 `f4e44047f268e96a…`) — V2-1 수용, **M1 철회** (2026-09-13)

| 항목 | 리뷰어 | 우리 |
|---|---|---|
| V2-1 | 입자 노드의 `cEeqref` 값 칸만 읽었다. 선택자 `cEeqref_mat = from_mat` 이면 재료 `csmax` 가 쓰이고 사용자 식은 죽은 문자열이다 | **수용.** `mph_dump_output.txt` 33–34 행(`pce1/pin1`) · 89–90 행(`pce2/pin1`) 에 두 줄이 나란히 있었다 — 도구가 아니라 읽기의 오류. `addm1` 만 `userdef`. 재료 `csmax` 에 dm 없음 → `soc(t=0) = x_init`, LAM 은 `epss` 한 곳 |
| 결과 | M1 "조건부" 도 성립하지 않는다 | **M1 철회.** 문서 v3 (`docs/MICROSHORT_MPH_REVIEW.md` 머리말·§3 M1·§4-1·§5-3·§8 정정). M1-3 의 −14.275 mV 는 반사실로 기록만 |
| 확인 요청 | — | `docs/COMSOL_CHECK_REQUEST.md` 의 `pin1.cEeqref` 실효값 확인은 **필요 없어졌다** (원본 6.4 는 열 수 없고, 답은 XML 에 있다). 6.3 재구축의 독립 산술(양극 x = 0.9240638866948166, `COMSOL_REBUILD_SPEC.md` §8-1)이 같은 쪽 |
| 남는 발견 | — | M3 · M8 · M2 · 정리 항목 (M4~M7). 다음 일은 원본 수정이 아니라 재구축 모델(§8-5 순서) |

교훈 (§5 에 더한다): **필드 값과 선택자는 한 쌍이다.** `<param>` 을 찍는 추출기는 `*_mat` 류 선택자를 같은 줄에 붙여
보여 줘야 하고, 읽는 쪽은 값이 "있다" 와 "쓰인다" 를 구분해야 한다. v1(정규식)·v2(ElementTree) 두 판 모두 도구는
맞는 값을 냈고 사람이 그 옆줄을 안 읽었다.
