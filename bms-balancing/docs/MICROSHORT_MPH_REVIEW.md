# 마이크로 쇼츠 COMSOL 모델 검토 — `ICA_degradation_mode.mph` (v2, 2026-09-13)

> **v2 = 1차 외부 리뷰 반영판.** 1차 판정은 **NO-GO** — "M1 은 확정 버그이므로 `cEeqref` 두 줄부터
> 고친다" 는 결론이 당시 증거로 성립하지 않았다. 패키지는
> `reviews/r14_repros/codex/` 에 원본 그대로 보존했다 (zip sha256
> `e2d74fb8390e63bc5dbd53a12401ea01809f16f78dc015a1756b0cbf14af45fb`).
> 대응 원장은 `reviews/MPH_R1_RESPONSE.md`. v1 에서 **바뀐 결론 다섯 개**:
>
> | v1 | v2 |
> |---|---|
> | "M1 은 버그다 → 두 줄 고쳐라" | **조건부 진단.** 조건(A1)은 v1 때보다 훨씬 강해졌지만 (§3 M1-2) COMSOL 확인 1회가 남아 있다 |
> | "세 열화모드가 용량 감소율 하나로 붕괴" | **틀렸다.** 붕괴하는 것은 **LAM_PE·LAM_NE 둘**뿐이다. LLI 는 `1-c_lit/c_lit₀` 로 독립이다 (§2-2) |
> | "12 h 휴지 후반 기울기는 쇼츠 전용 신호축" | **반증됐다.** `C_diff` 가 LLI/LAM 에 의존하고 완화는 6–8 h 뒤에도 남는다 (§5-2) |
> | "Events 는 활성이지만 무력" | **`ev` 인터페이스 자체가 DISABLED** 다 (§3 M5). v1 의 정규식 추출기가 `<Physics>` 컨테이너를 안 봐서 놓쳤다 |
> | `tau_short = C_cell·V/i_leak` | **차원이 틀렸다** (V·h). 고쳤다 (§5-2 ③) |
>
> **원본 파일은 이 저장소에 없다.** 공개 저장소라 `.mph` 와 규진팀 `.xlsx` 는 커밋하지 않는다.
> 좌표는 `.mph`(=ZIP) 안 `dmodel.xml` 의 노드 태그·파라미터 이름이며 COMSOL GUI 에서 같은 이름으로 찾는다.
> **이 문서의 숫자는 사본이다.** 정본은 규진팀이 가진 `.mph` 와 `result_L_*.xlsx`.
>
> 대상: `ICA_degradation mode.mph` · COMSOL 6.4.0.293 · 최종 계산 2026-09-12 22:27 UTC (8.314 s)
> 추출 도구: `reviews/r14_repros/mph_dump.py` (ElementTree 기반 — v1 의 정규식 추출기는 폐기)

---

## 0. 한 문단 요약

이 모델은 **열화모드(LLI·LAM_PE·LAM_NE)를 파라미터로 주입한 full-cell DFN 에 분리막 전자전도를
얹어 마이크로 쇼츠를 켜고 끄는** 1D 모델이다. 회의에서 나온 "레퍼런스 셀과 안 맞는다" 에 대해
**구조적 후보 원인 셋**을 찾았고, 셋 다 열화모드 파라미터를 건드리지 않고 확인·수정할 수 있다.

1. **M1 (조건부, 최우선)** — LAM 이 `epss`(부피분율)와 `cs,max`(사이트밀도) 양쪽에 걸려 있고,
   `cs,max` 의 짝인 `cs,init` 에는 안 걸려 있다. **이 정규화를 활성 OCP 가 소비한다면** 초기 평형
   OCP 차가 −14.27 mV 이고 호스트 사이트가 (1−LAM)² 로 준다. 소비 경로는 §3 M1-2 에서 강하게
   지지되지만 **COMSOL 확인 1회가 남아 있다.**
2. **M3** — OCP 가 COMSOL 내장 라이브러리 곡선인데 열화모드 값을 만든 α·β 적합은 자체 반쪽셀
   곡선 위에서 돌았다. 두 곡선을 겹쳐 그리는 것만으로 판정된다.
3. **M8** — 저장된 해는 0.05C 인데 파라미터 표는 0.1C 다. "안 맞는다" 판정 전에 정리해야 한다.

**아직 "버그" 라고 부르지 않는다.** M1 은 의도적 설계(부피와 사이트밀도를 동시에 줄이고 Li 재고는
따로 지정하는 현상론적 모델)와도 양립한다 (§3 M1-4). 무엇을 LAM 이라 부르기로 했는지 —
`H/H₀ = 1−LAM` 인가, 두 기작을 묶은 값인가 — 를 **먼저 정의**해야 수정 방향이 정해진다.

---

## 1. 처음 보는 사람을 위한 모델 지도

### 1-1. 형상 — 1D, 도메인 3개

```
 경계1          도메인1            경계2   도메인2   경계3       도메인3           경계4
   │◀────────── 52 um ──────────▶│◀── 25 um ──▶│◀──────── 44 um ────────▶│
   │      음극 (흑연, pce1)       │  분리막      │     양극 (NCM811, pce2)  │
   │                             │ sep1 + pcb1  │                          │
 접지                                                                    전류 인가
 egnd1                                                                    cdc1
 phis = 0                                                          충방전 사이클링
```

- `E_cell = intop_cc2(phis) - intop_cc(phis)` = 경계4 고체전위 − 경계1 고체전위.
- 1D 라서 **면적 기준은 1 m²**. 실제 셀 면적 `A_cell = 1.53938 cm²` 는 **후처리 환산에만** 쓰인다.
  전류 경계조건은 `i_1C*C_rate*1[m^2]`.

### 1-2. 살아 있는 것 / 죽어 있는 것

이 파일은 **반쪽셀(Li metal) 모델을 full-cell 로 개조한 것**이고 개조 전 부품이 남아 있다.
아래 표는 `mph_dump.py` 가 **자기 flags 와 조상 사슬을 나눠서** 낸 결과다 (v1 표는 정규식
추출기가 자식 flags 를 부모로 전파해 일부가 틀렸다).

| 노드 | 상태 | 무엇 |
|---|---|---|
| `pce1` 음극 (흑연) | 활성 | `epss = epss_Gr`, `rp_Gr = 7.5 um`, `Ds = D_g` |
| `pce1/pin1` 입자 | 활성 | `csinit = x_Gr_init*cs_Gr_max` · `cEeqref = cs_Gr_max*dm_fNE` |
| `pce1/per1` 반응 | 활성 | `Eeq_mat = from_mat` · `MaterialOption = mat1` · `LithiumInsertion` |
| `pce2` 양극 (NCM811) | 활성 | `epss = epss_pos`, `rp = 10 um`, Bruggeman 지수 `b_PE = 2.2` |
| `pce2/pin1` 입자 | 활성 | `csinit = x_NCM_init*cs_NCM_max` · `cEeqref = cs_NCM_max*dm_fPE` |
| `sep1` 분리막 | 활성 (선택 없음 = 기본 도메인) | `epss = 0.4` · `epsl = epsl_sep`(0.45) · Bruggeman |
| `pcb1` Porous Conductive Binder | 활성 | **σ = `sigma_short` — 마이크로 쇼츠** · `epss = epsl_sep`(0.45) · Bruggeman |
| `cdc1` Charge-Discharge Cycling | 활성 | **실제 제어기.** 충전 먼저, CV 충전 on, Vmax 4.25 / Vmin 2.7, 충전 후 휴지 `trech = 12 h` |
| `egnd1` Electric Ground (경계1) | 활성 | 기준 전위 |
| `ge` Global ODE `Cap` | 활성 | 누적 전하. `SOC = Cap/Q_el` |
| `ge2` Global ODE `E_lith`/`E_delith` | 활성 | 진단용. `i_app`·`CurrentDirection` 을 읽는다 (§3 M6) |
| `c` / `cfeq1` Coefficient Form PDE | 활성이지만 무력 | `f = dSdt`, `dSdt = 0` → S ≡ 1. Si 이력 잔재 |
| **`ev` Events 인터페이스** | **DISABLED (자기 flags)** | 하위 `ds1`·`is1`·`impl1`·`impl2` 는 자기 flags 가 없지만 **인터페이스가 꺼져 있어 안 돈다** (§3 M5) |
| `addm1` 실리콘 | DISABLED | 게다가 `Si_m_f = 0` → `epss_Si = 0`. **이중으로 꺼짐** |
| `es1` Electrode Surface + `lc1` (경계3, Li metal `mat3`) | DISABLED | 반쪽셀 대극. `es1/er1` 은 `LithiumMetal` kinetics |
| `ecd1` Electrode Current Density | DISABLED | `cdc1` 로 대체 |
| `socicd1`(+ 하위), `nfr1`, `dcont1`×2 | DISABLED | 미사용 |
| Parametric Sweep (`param`) | DISABLED | 목록은 `C_rate = 0.05` × `sigma_short = {1e-20, 1.4e-6, 4.67e-6, 1.4e-5}` |

**지금 이 파일을 그냥 Compute 하면**: 단일점 `C_rate = 0.1`, `sigma_short = 1e-20`(쇼츠 없음),
실리콘 없는 순수 흑연 음극, CC-CV 충전 후 12 h 휴지, **이벤트 제어 없음**.

### 1-3. 마이크로 쇼츠가 걸리는 방식

분리막 도메인에 **전자를 흘리는 고체상**(`pcb1`)을 얹는다. 그 상의 전도도가 `sigma_short`.
음극(경계2)과 양극(경계3)의 고체전위가 이 상을 통해 이어지므로 셀 전압에 비례하는 누설 전류가
생긴다 — 마이크로 쇼츠의 등가회로다.

`ElectricCorrModel = Bruggeman` 이므로 실효 전도도는 `sigma_short × epss^b`. `b = 1.5` 라면
계수 `0.45^1.5 = 0.301869177` (역수 3.3126933). **지수와 적용 여부는 GUI 확인 대상이다**
(§3 M2).

| `sigma_short` | 셀 환산 저항 | 4 V 누설 / 0.1C 인가전류 |
|---|---|---|
| `1e-20` (현재값) | ~5.4e19 Ω | ~0 % — **쇼츠 꺼짐** |
| `1.4e-6` | 3.84e5 Ω | 2.70 % |
| `4.67e-6` | 1.15e5 Ω | 9.01 % |
| `1.4e-5` | 3.84e4 Ω | 27.0 % |

(`epss = 0.45`, `b = 1.5` 를 받아들였을 때. 1차 리뷰가 독립 재현했다.)

---

## 2. 파라미터가 어디서 오는가 — α·β 적합과의 연결 고리

`.mph` 의 열화모드 파라미터는 **`result_L_ref1__0.1C_12h__charge.xlsx` cycle 2 한 줄**에서 왔다.
네 파일(ref1·ref2·PE1·PE5, 37행) 전수 대조로 확인했다.

| `.mph` 파라미터 | 출처 |
|---|---|
| `LAM_PE = 0.0296398242` · `LAM_NE = 0.0257219788` · `LLI = 0.0439355` | ref1 cycle 2 |
| `C_lit0_ref1 = 0.003765381 [Ah]` | ref1 cycle 0 의 `c_lit` |
| `dNE = -0.00302481525` | ref1 cycle 0 의 `b_NE` |
| `dm_fNE = 0.97427802` / `dm_fPE = 0.97036018` | `1-LAM_NE` / `1-LAM_PE` 를 손계산해 8자리에서 자른 값 (차 1.2e-9 / −4.2e-9) |
| `dPE = 0.0101000283` | **네 파일 어디에도 없음 — 출처 불명** |

### 2-1. 적합 출력의 열화모드는 독립 측정량이 아니다

37행 전부에서 다음이 성립한다 (실측 최대 절대오차 `LAM_PE` 2.6e-16 · `LAM_NE` 1.6e-16 ·
`LLI` 5.6e-17 · `x_cell` 0):

```
x_cell = C_cell / C_cell₀
LAM_PE = 1 - x_cell · a_PE/a_PE₀       LAM_NE = 1 - x_cell · a_NE/a_NE₀
LLI    = 1 - c_lit / c_lit₀
```

적합이 실제로 푼 것은 `a_PE, b_PE, a_NE, b_NE, c_lit` (α·β) 이고 열화모드 셋은 그 후처리다.

### 2-2. α 들이 난간(rail)에 붙어 있다 — 다만 **붕괴하는 것은 두 LAM 뿐이다**

| 파일 | `a_NE` | `a_PE` 가 cycle-0 값에 비트 동일인 행 | `LAM_PE ≈ LAM_NE` (rtol 1e-9) |
|---|---|---|---|
| ref1 | 전 사이클 **비트 동일** | 8 / 10 | 8 / 10 (같은 행) |
| ref2 | 전 사이클 **비트 동일** | 6 / 10 | 6 / 10 (같은 행) |
| PE1 | 전 사이클 **비트 동일** | 9 / 10 | 9 / 10 (같은 행) |
| PE5 | 전 사이클 **비트 동일** | **7 / 7** | **7 / 7** |

`b_NE` 는 cycle 0 을 빼면 전 행에서 정확히 0, `a_PE` 는 **한 번도 cycle-0 값을 넘지 않는다**
(argmax = cycle 0). `a_PE` 가 그 값에 붙으면 `a_PE/a_PE₀ = 1` 이므로 §2-1 에서 정확히

```
LAM_PE = LAM_NE = 1 - x_cell
```

> **v1 정정.** v1 은 여기서 "**세** 열화모드가 용량 감소율 하나로 붕괴한다" 고 적었다. **틀렸다.**
> `LLI = 1 - c_lit/c_lit₀` 는 `c_lit` 에서 오고 `x_cell` 과 다른 양이다. ref1 난간 행에서
> `LLI - (1-x_cell)` 은 **0.0216 ~ 0.0355** 로 붕괴하지 않는다. 붕괴하는 것은
> **LAM_PE 와 LAM_NE 둘**, 즉 **전극 사이의 구분**이다. LLI 축은 살아 있다.

읽는 방법: `a_NE` 는 고정되어 있고 `a_PE` 는 상한에 눌려 있다 — 그 행에서 **LAM 을 전극별로
가르는 정보가 없다.** 다만 상한의 존재는 출력에서 역추론한 것이고 MATLAB 원본을 보지 못했다.
"물리적으로 PE 용량이 늘 이유가 없으니 상한 = 초기값" 은 **합리적 제약**일 수 있다 — 그렇다면
난간은 버그가 아니라 **모델 선택의 귀결**이다. 별건 요청문 `reviews/REQ_FIT_RAILS.md` 참조.

> **이 모델이 고른 ref1 cycle 2 는 ref1 에서 `a_PE` 가 난간에서 떨어진 단 두 행(cycle 1, 2) 중
> 하나다.** 고를 수 있는 것 중 나은 쪽이다. 다만 cycle 3 부터는 전극 구분 정보가 없으므로 같은
> 방식으로 사이클을 따라가면 cycle 3 이후는 같은 축퇴점 반복이 된다.

---

## 3. 발견

심각도 순. `결론이_바뀜` = 그래프 모양·판정이 바뀜, `숫자가_바뀜` = 값만, `정리` = 오해 유발.

### M1 — LAM 이 두 번 곱해지고 그 짝이 안 맞는다 · `결론이_바뀜` (조건부) · **최우선**

#### M1-1. 실측한 값

```
전역 파라미터:
  epss_el  = epss_el_0*(1-LAM_NE)        epss_pos = epss_pos_0*(1-LAM_PE)
  epss_Gr  = epss_el*(1-Si_f)            Si_f = 0
  cs_NCM_init = x_NCM_init*cs_NCM_max*dm_fPE     ← 정의만 되고 live 참조 0

물리 노드 (직계 param, mph_dump.py):
  pce1/pin1   cEeqref = cs_Gr_max*dm_fNE      csinit = x_Gr_init*cs_Gr_max
  pce2/pin1   cEeqref = cs_NCM_max*dm_fPE     csinit = x_NCM_init*cs_NCM_max
```

COMSOL 은 `soc = cs/cs,max` 로 평형전위를 읽는다. 그러면

```
soc(t=0) = csinit / cEeqref = x_init / dm_f      (음극 +2.64 % · 양극 +3.05 %)
```

#### M1-2. 이 정규화를 활성 OCP 가 소비하는가 — 1차 리뷰가 연 구멍, v2 의 답

1차 리뷰의 지적은 정확했다: COMSOL 은 **사용자 정의 OCP 경로**도 지원한다. 공식 1D 예제는
`Eeq_neg(liion.cs_surface/csmax_neg)` 를 직접 입력하고, 그 경로에서는 입자 노드의 `cEeqref` 와
**다른** 파라미터로 정규화할 수 있다. `pin1.cEeqref` 만 보고 "모든 Eeq 가 `x/dm` 을 읽는다" 고
결론 낼 수 없다.

**이 모델은 그 경로가 아니다.** 실측 넷:

| # | 실측 | 뜻 |
|---|---|---|
| 1 | `pce1/per1.Eeq_mat = from_mat`, `MaterialOption = mat1` · `pce2/per1.Eeq_mat = from_mat`, `MaterialOption = dommat`(mat5) | 사용자 정의 식이 **아니다**. 재료가 준다 |
| 2 | `mat1`·`mat5` 의 평형전위 물성이 **문자 그대로** `Eeq_int1(soc)+dEeqdT_int1(soc)*(T-298[K])` | 인자가 COMSOL **내장 `soc`** 다. 손으로 쓴 `cs/무언가` 가 아니다 |
| 3 | `per1.cEeqref = 2.5e4[mol/m^3]` 이 **네 반응 노드 전부** 동일 — `pce1/per1` · `pce2/per1` · `addm1/per1` · `es1/er1`(LithiumMetal, 화학이 완전히 다름) | 공장 기본값이고 **아무도 편집한 적이 없다.** 편집된 것은 `pin1.cEeqref` 쪽뿐이다 |
| 4 | `per1.cs_ref = liion.csmax/2` — 반응 노드가 자기 `cEeqref` 가 아니라 **생성 변수 `liion.csmax`** 를 참조 | `csmax` 는 입자 노드가 정의하는 단일 변수다 |

대조: 사용자 정의 경로를 **실제로 쓰는** 노드가 이 파일에 있다 — `addm1/per1` 은
`Eeq_mat = userdef`, `Eeq = Eeq_Si`. 즉 작성자는 두 경로를 구분해 썼고, 두 전극은 `from_mat` 을
골랐다.

**남은 구멍**: `ParticleConcentrationType = SolveinExtraDimension` 일 때 COMSOL 이 `soc` 의 분모로
`pin1.cEeqref` 를 쓴다는 것은 위 넷의 **정합적 해석**이지 실행 확인이 아니다.
**이것을 끝내는 방법은 하나** — GUI 에서 `liion.pce2.pin1.soc` (또는 `liion.soc_average_pce2`)
의 t=0 값을 찍어 `0.924064` 인지 `0.952290` 인지 본다. 30초면 된다.

#### M1-3. 조건이 참일 때의 수치

내장 OCP 보간표(선형, 88점/100점)에서:

| | 의도 soc | as-built soc | OCP |
|---|---|---|---|
| 음극 (흑연) | 0.011721 → 0.513439 V | 0.012030 → 0.508899 V | **−4.540 mV** |
| 양극 (NCM) | 0.924064 → 3.565805 V | 0.952290 → 3.546990 V | **−18.815 mV** |
| **셀 t=0** | **3.052365 V** | **3.038090 V** | **−14.275 mV** |

호스트 사이트: 음극 **−5.078 %** · 양극 **−5.840 %** (선언값 2.572 % · 2.964 % 의 약 두 배).
1차 리뷰가 독립 재현했다 (`reviews/r14_repros/codex/pkg/mph_review_checks_results.json`).

**이 수치가 말하지 않는 것**: 이것은 **t=0 평형 OCP 차**다. 충전 궤적과 ICA 봉우리 이동량은
**미검증**이다. 셀 전압에는 두 전극의 x(q), 과전압, 확산, CC/CV 제어가 함께 들어간다.
최대농도 변경은 삽입 반응의 자유 사이트·반응속도에도 영향을 줄 수 있으므로 "OCP 눈금만 틀렸다"
역시 너무 좁다. v1 이 이 구분을 §8 에만 적고 §0·§3 에서는 단정한 것은 과장이었다.

참고로 `soc = x/dm_f` 는 **OCP 표 끝에 일찍 닿는다** — 흑연 표 끝 0.993 에 실제 x = 0.9675 에서,
NCM 표 끝 0.99 에 x = 0.9607 에서 닿는다 (그 뒤는 외삽).

#### M1-4. 버그인가 설계인가 — 아직 못 가른다

미사용 `cs_NCM_init` 은 **단서**이지 증거가 아니다 (v1 은 "버그라는 증거" 라고 썼다 — 과장).
다음 현상론적 모델은 인용한 모든 식과 양립한다:

> 접근 가능한 활성 부피는 `f = 1−LAM` 배, 남은 재료의 유효 사이트 밀도는 `d = dm` 배,
> 활성 Li 재고는 `nLi_target` 으로 **따로** 지정한다. 이때 `x` 는 pristine 최대농도에 대한
> 농도 좌표이고 현재 점유율이 `x/d` 인 것은 **의도와 일치**한다.

두 점유율(0.01203, 0.95229) 모두 0–1 안이라 이 해석이 수치적으로 막히지도 않는다.
미사용 변수는 폐기된 초기화 대안으로도 설명된다.

**가르는 것은 외부 계약이다**: 입력 LAM 이 "전극 전체 호스트 용량 감소율이고 한 번만 적용한다"
(`H/H₀ = 1−LAM`) 이면 현재 구현 `(1−LAM)·dm` 은 그 계약과 불일치다. **먼저 정의해야 한다.**

#### M1-5. Li 수지는 맞다 (범위를 좁혀서)

`nLi_0`·`x_NCM_init`·`csinit` 이 전부 맨 `cs_*_max` 를 쓰므로 **활성 고체 Li 재고의 대수적
항등식**은 성립한다. 그래서 용량 검산으로는 안 걸린다. 다만 이것은 전 원소 수지나 실측 `c_lit`
의 정의까지 입증한 것은 아니다.

`x_NCM_init = 0.924064` 는 우리가 Li 수지식을 푼 값이다 (`LLI = 0.0439355`,
`C_lit0_ref1 = 0.003765381 Ah` 로 `nLi_target = 1.188226 mol/m²`, `dLi = 0.040098 mol/m²`).
COMSOL 이 실제로 그 값을 쓰는지는 확인하지 못했다.

---

### M2 — 쇼츠 상의 부피분율과 보정 · `숫자가_바뀜`

```
sep1 (기본 도메인)  epss = 0.4          epsl = epsl_sep (0.45)   Bruggeman
pcb1 (분리막 전자상) epss = epsl_sep(0.45) epsl = epsl_sep (0.45)  Bruggeman
```

`pcb1.epss` 가 전해질 분율과 **같은 심볼**을 쓴다. 분리막 부피의 45 % 가 전자 도체라는 뜻이 되고,
`sep1.epss = 0.4` 까지 세면 분율 합이 1을 넘는다 (두 노드가 합성인지 덮어쓰기인지는 GUI 확인 대상).
물리적으로 마이크로 쇼츠는 **가느다란 필라멘트**다.

> **v1 정정 둘.**
> (a) v1 은 "복붙" 이라고 단정했다 — 의도 증거가 없으므로 **"같은 심볼을 쓴다"** 로 낮춘다.
> (b) v1 은 "sweep 값이 3.3배 과대표기" 라고 했다 — 작성자가 **intrinsic 전도도를 쓸었다고
> 선언했다면** 이는 정상적인 intrinsic→effective 변환이지 오표기가 아니다. 표기 계약을
> 확인해야 판정할 수 있다.
> (c) v1 은 "`epss` 와 `sigma_short` 가 **곱**으로만 들어가 축퇴" 라고 했다 — 정확히는
> `σ·epss^b` 다. 보정이 **없으면** `epss` 가 전도도 식에서 아예 빠지므로 축퇴도 사라진다.

1차 리뷰가 확인해 준 것: Porous Conductive Binder 는 **전극상 전도도에도 공극 보정을 적용한다**
(COMSOL 공식 설명). 따라서 "binder 에는 전자 전도도 보정이 없다" 는 반론은 성립하지 않는다.
남은 확인 대상은 **지수 값과 실제 보정식**이다.

---

### M3 — OCP 가 COMSOL 내장 라이브러리 곡선이다 · `결론이_바뀜` (조건부)

| 도메인 | 재료 | 표 |
|---|---|---|
| 1 (음극) | `Graphite, LixC6 MCMB (Negative, Li-ion Battery)` | 88점, soc 0.0082–0.993, 0.041–0.565 V |
| 3 (양극) | `NMC 811, LiNi0.8Mn0.1Co0.1O2 (Positive, Li-ion Battery)` | 100점, soc 0.18–0.99, 3.517–4.380 V |

보간함수 이름이 `Eeq_int1`/`dEeqdT_int1`/`dVOLdSOL` (라이브러리 기본), 재료 이름도 라이브러리
이름이다. **다만 표가 덮어써지지 않았다는 증거는 아니다** — 라이브러리 원본과 대조하지 못했다.

`Q_el = 25.036 Ah/m²` 는 `epss_pos_0*L_pos*cs_NCM_max*(x_NCM_max-x_NCM_min)*F/3600` 과 정확히
일치한다. 이는 **용량 기준을 그 창에서 만들었다**는 증거이지 OCP 표의 출처를 입증하지는 않는다.

> **v1 정정.** v1 은 "α 는 기준 곡선과 분리 불가능하므로 다른 곡선 위의 LAM 은 **반드시** 이식
> 불가" 라고 했다. **반례가 있다.** `U₂(w) = U₁(a·w+b)` 처럼 같은 물리를 공통 affine 좌표로
> 바꾼 경우 전극 용량은 `Q₂ = a·Q₁` 이고 정규화 비율 `1 - Q_aged/Q_BOL` 에서 `a` 가 상쇄된다.
> 즉 **raw α 의 곡선 의존성**과 **정규화된 LAM 비율**은 구분해야 한다. 실제 비선형 형상 차이는
> 검증 대상이고, LLI 의 원점 문제까지 이 불변성을 확장할 수는 없다.

또 "가장 큰 단일 원인" 이라는 순위도 미검증이다 — 두 원곡선과 실험 전압이 없다.
남는 것은 **점검할 가치가 큰 후보**라는 것: 두 곡선을 겹쳐 그리는 것만으로 판정되고,
열화모드 파라미터를 건드리지 않는다.

OCP 를 교체한다면 BOL 전극 밸런스·사용 창·온도·방향·capacity 좌표와 재고의 변환을 **먼저
정의**해야 한다. 표만 갈아 끼우고 끝낼 일이 아니다.

---

### M4 — `dPE`·`dNE` 는 죽은 파라미터다 · `정리` — **live 참조 그래프로 확인**

v1 은 문자열 등장 횟수로 판정했다 (1차 리뷰: "등장 횟수 ≠ 소비자 수"). v2 는 `<actions>`(이력)를
제외한 **live 표현식에서 식별자 참조**만 센다 (`mph_dump.py --refs`):

| 이름 | live 참조 |
|---|---|
| `dPE` · `dNE` | **0** |
| `cs_NCM_init` · `cs_Gr_init` | **0** |
| `E_end` | **0** |
| `x_NCM_max` · `x_NCM_min` | **0** |
| `i_app` | **2** — 비활성 `ecd1` 1 + **활성 `ge2` 1** |

액션 로그를 보면 예전에는 `x_NCM_init = x_NCM_max - dPE*(x_NCM_max-x_NCM_min)` 이었고 지금은
Li 수지식으로 대체됐다. `x_NCM_max`/`x_NCM_min` 도 이제 live 소비자가 없다 (`Q_el` 은 그 값에서
계산된 **상수**로 박혀 있다).

"수정 불가" 목록에 `dPE`·`dNE` 가 들어 있다면 **그 제약은 아무것도 제약하지 않는다.**
협의할 때 구분할 가치가 있다. (`dNE` 는 ref1 cycle 0 의 `b_NE` 와 값이 같다. 값 일치가 유일한
출처를 증명하지는 않는다. `dPE` 는 네 파일 어디에도 없다.)

---

### M5 — Events 인터페이스가 **꺼져 있다** · `정리` — **v1 정정**

> **v1 은 "활성이지만 무력" 이라고 썼다. 틀렸다.** `mph_dump.py` 로 다시 보면
> **`<Physics tag="ev">` 자체가 `DISABLED`** 다. 하위 `ds1`·`is1`·`impl1`·`impl2` 는 자기
> flags 가 없지만 인터페이스가 꺼져 있어 돌지 않는다. v1 의 정규식 추출기가 `PhysicsFeature`
> 만 걷고 `<Physics>` 컨테이너를 안 봐서 놓쳤다 — 1차 리뷰 §2.6 이 그 추출기를 지적하지
> 않았다면 못 찾았을 것이다.

그래서:

- 실제 제어는 전부 `cdc1` (Vmax 4.25 / Vmin 2.7 / CV 충전 / 휴지 12 h).
- `CurrentDirection` **이름 충돌은 해소된다** — 이산 상태가 존재하지 않으므로 전역 파라미터
  (`= 1`)가 쓰인다. `ge2` 는 항상 delithiation 가지로 간다.
- `E_switch = E_max_pos - E_min_el = 4.178 V`, `E_end = E_min_pos - E_max_el = 3.042 V` 는
  **full-cell 양극 한계와 반쪽셀 음극 한계를 섞은 식**이고, `E_end` 는 live 참조 0 이다.

남는 지적 하나: 두 지시자(`switch`/`end`)가 같은 문턱 `E_switch` 를 쓴다. v1 은 이것을 오류로
단정했으나 **방향이 반대인 crossing 에 같은 문턱을 쓰는 것은 정상 관용구**다. 어느 쪽이든
인터페이스가 꺼져 있어 지금은 효과가 없다.

> 확인 필요: COMSOL Stop Condition 은 표현식과 **별도로** implicit event 를 선택하는 경로가
> 있다. `stopcondarr` 가 비어 있다는 것만으로 모든 중단 경로를 배제할 수는 없다.

---

### M6 — `ge2` 의 에너지 적분 · `정리`

```
d(E_lith,t)   = if(CurrentDirection == -1,  i_app*(E_cell - E_max_el), 0)
d(E_delith,t) = if(CurrentDirection ==  1, -i_app*(E_cell - E_max_el), 0)
```

`E_max_el = 0.502 V` 는 흑연 반쪽셀의 0 % SOC 전위다.

> **v1 정정.** v1 은 "무의미" 라고 했다. `∫I(V−V₀)dt = W − V₀ΔQ` 는 **기준전압에 대한 에너지**로
> 정의 가능하다. 정확한 표현은 **"단자 에너지·효율로 해석할 근거가 없다"** 이다.

더 강한 검증점은 따로 있다: `i_app = i_1C*C_rate*CurrentDirection` 이 **`cdc1` 의 실제 CC/CV/휴지
전류와 일치하지 않는다.** CV 구간과 휴지 구간에서 `cdc1` 은 전류를 바꾸는데 `i_app` 은 상수다.
따라서 `ge2` 의 적분은 CC 구간 밖에서 실제 전류를 쓰지 않는다.

---

### M7 — 충전 중 `SOC` 부호 · `정리`

`ge`: `d(Cap,t) + liion.cdc1.Icell/1[m^2] = 0`, 초기값 `Cap(0) = 0`. 양극 CDC 의 **충전 양수**
규약(공식 예제의 `liion.cdc1.Icell>0` 필터로 확인)에서 충전 중 `Cap` 은 감소 → `SOC = Cap/Q_el`
이 음수가 된다.

부호를 뒤집어도 남는 문제: **외부 전류만 적분하면 휴지 중 내부 누설이 빠진다.** 쇼츠가 켜진
경우 이 `SOC` 는 물리적 SOC 가 아니다. 쇼츠 연구에서는 특히 중요하다.

---

### M8 — 파일 상태가 파라미터 표와 어긋난다 · `정리`

- 저장된 해는 `C_rate = 0.05`, `sigma_short ∈ {1e-20, 1.4e-6, 4.67e-6, 1.4e-5}` (2026-09-03).
  현재 파라미터는 `C_rate = 0.1`, `sigma_short = 1e-20`, 최종 계산은 2026-09-12 단일점.
- Parametric Sweep 노드는 **DISABLED**, 목록도 `C_rate = 0.05` 그대로.
- 업로드된 실험 데이터는 **0.1C, 12 h**. `cdc1.trech = 12 h` 는 이 프로토콜과 맞다.
- Sweep 의 "Save each solution as model file" 에 **다른 사람의 Windows 로컬 경로**가 박혀 있다.
  그 PC 밖에서는 sweep 을 켜는 순간 저장이 실패한다.

**파일을 열어 그림을 그리면 0.05C 결과가 보이는데 파라미터 표에는 0.1C 라고 적혀 있다.**
"모델이 데이터와 안 맞는다" 를 판단하기 전에 여기부터 정리해야 한다.

> 단서일 뿐이다 — solution 이름만으로 모든 해의 파라미터를 확정해서는 안 된다.
> 원본 해 metadata 로 재확인이 필요하다.

---

## 4. 수정안 — 열화모드 파라미터를 건드리지 않는 범위

> 제약: `LAM_PE`, `LAM_NE`, `LLI`, `dPE`, `dNE` 는 수정 불가.
> 아래는 전부 그 제약 안이다 — 값이 아니라 **값을 쓰는 방법**만 바꾼다.
> **단, §4-1 을 실행하기 전에 §3 M1-2 의 GUI 확인 1회와 M1-4 의 LAM 계약 정의가 선행되어야 한다.**

### 4-1. M1 — LAM 을 `epss` 한 곳에만 (계약이 `H/H₀ = 1−LAM` 일 때)

| 노드 | 필드 | 지금 | 바꿀 것 |
|---|---|---|---|
| `pce1/pin1` | `cEeqref` | `cs_Gr_max*dm_fNE` | **`cs_Gr_max`** |
| `pce2/pin1` | `cEeqref` | `cs_NCM_max*dm_fPE` | **`cs_NCM_max`** |

`csinit`·`epss_el`·`epss_pos`·`x_NCM_init`·`nLi_0` 는 **그대로**. `soc(t=0) = x_init` 이 정확히
성립하고 Li 재고는 이미 맞으므로 유지된다.

**이것은 모델 선택이다.** "남은 입자의 `cs,max` 는 일정하고 활성 부피만 준다" 는 가정이 맞을 때
적절하다. `cmax`-only 와는 비표면적·수송·반응속도 효과가 달라 같은 capacity 비율이어도
동역학적으로 동등하지 않다. COMSOL 열화 예제도 활성 부피분율 감소를 쓰되 전해질 부피분율
유지와 확산계수 변화를 **따로** 설정한다 — 공극률 변화를 자동 추론해서는 안 된다.

**검산 한 줄**: 수정 후 `liion.pce2.pin1.soc` 의 t=0 값이 `x_NCM_init` 과 같은지 찍는다
(수정 전에는 `x_NCM_init/dm_fPE` 여야 한다 — 이 값이 §3 M1-2 의 확인과 같은 검사다).

**대안 (LAM 을 `cs,max` 에만)** — v1 의 지시는 틀렸다. **`nLi_0` 의 BOL 기준까지 aged `dm` 으로
바꾸라고 적었는데 그것은 보존을 위해 필수인 작업이 아니라 기준 재고의 재정의다.**
BOL 재고를 고정한 채 현재 점유율을 풀어야 한다:

```
θ_p,0 = ( nLi_0 - dLi_LLI - ε_n⁰·L_n·c_n⁰·d_n·θ_n,0 ) / ( ε_p⁰·L_p·c_p⁰·d_p )
c_i,init = c_i⁰ · d_i · θ_i,0
```

그리고 **"짝을 맞추자" 는 자동으로 보존적이지 않다** — 인용된 `x` 를 유지한 채 두 `csinit` 에
`dm` 만 곱하면 Li 재고가 **0.035173 mol/m² (현재 재고의 약 2.96 %)** 더 줄어든다.

### 4-2. M2 — 쇼츠 파라미터화

`pcb1.epss` 를 `epsl_sep` 에서 떼어낸다. 다만 **baseline 을 보존하려면 계수를 옮겨야 한다**:

```
지금:      pcb1.epss = epsl_sep (0.45), Bruggeman   →  σ_eff = 0.301869177 · sigma_short
바꾼 뒤:   pcb1.epss = f_short (필라멘트 면적비),  ElectricCorrModel = No correction
           sigma_eff = 0.301869177 · sigma_short   ← 이 계수를 반드시 옮긴다
```

> **v1 정정.** v1 은 "`epss = 1` 로 두고 보정을 끄라" 고만 적었다. **값을 그대로 두고 보정만
> 끄면 유효 전도도를 3.3127배 늘린 새 모델**이 된다 (분리막 양끝 전위차가 같을 때 누설전류도
> 그 배율로 증가). 또 `epss = 1, epsl = 0.45` 는 분율 합이 1.45 라 물리적 분율 해석을 버리게
> 된다. 물리적 분율을 유지한 채 `No correction` + `sigma_eff` 정의를 분리하는 쪽이 명확하다.

### 4-3. M3 — OCP 를 α·β 적합이 쓴 곡선으로 (선행 정의가 필요)

`mat1`/`mat5` 의 `Eeq` 보간표를 MATLAB 적합에 들어간 반쪽셀 곡선으로 바꾼다. 같이 다시 잡을 것:
`x_NCM_max`/`x_NCM_min` (사용 창) · `E_max_el`/`E_min_el` · `Q_el` · `x_Gr_0`/`x_NCM_0`.
**열화모드 파라미터가 아니라 기준 곡선이다 — 제약 밖이다.** 다만 §3 M3 의 정정대로
"이식 불가" 를 일반 명제로 쓰지 말고, 두 곡선의 실제 형상 차이를 먼저 재야 한다.

### 4-4. 정리 (결과 안 바뀜, 오독 방지)

- `ev`(이미 DISABLED) · `cfeq1` · `ge2` 삭제 또는 주석 — 전부 반쪽셀/Si 잔재.
- `es1`·`lc1`·`ecd1`·`mat3`(Li metal) 삭제.
- `addm1`·`mat4`(Si) 와 `D_si`·`k_si`·`rp_Si`·`x_Si_*`·`S_init`·`K_S`·`U_avg`·`U_offset`·
  `Eeq_Si`·`dx_Sidt`·`dSdt` — 쓸 계획이 없으면 삭제, 있으면 **왜 꺼져 있는지 주석**.
- `dm_fNE`/`dm_fPE` → `1-LAM_NE`/`1-LAM_PE` (값 불변, 추종성 확보).
- Sweep 의 Windows 로컬 저장 경로 제거.
- `SOC` 부호 정정 + 휴지 중 내부 누설이 빠진다는 주석.
- Sweep 목록을 `C_rate = 0.1` 로, 저장된 0.05C 해는 삭제하거나 이름표.

---

## 5. 더 좋은 방향성

### 5-1. 지금 방향의 구조적 한계

회의 내용은 "α·β / LAM / LLI 를 넣고 마이크로 쇼츠가 없었다면 전압 곡선이 사이클마다 어떻게
갔을지 본다. 그러려면 레퍼런스 셀과 맞아야 한다" 였다. 이 방향은 **모델이 한 점을 정확히
재현해야 성립**한다. 그런데 §2-2 대로 입력의 **전극 구분** 정보가 대부분의 사이클에서 사라진다
(LLI 축은 살아 있다). 한 점을 맞춰도 그 점이 유일하지 않으면 맞았다는 사실이 아무것도 증명하지
않는다. 그리고 파라미터는 수정 불가다.

### 5-2. 제안

**① 점 예측기 → 띠(band) 예측기**

§2-1 의 닫힌 형태 덕분에 축퇴 방향을 안다: `a_PE` 가 난간에 붙으면 `LAM_PE → LAM_NE`.
난간에서 떨어진 `a_PE` 범위를 잡아 `(LAM_PE, LAM_NE)` 쌍 집합을 만들고 **그 집합 전체를 sweep**
한다 (LLI 는 독립이므로 별도 축). 출력은 곡선이 아니라 **띠**다.

- 띠가 좁으면 → 파라미터 불확실성이 결론에 영향 없음. **못 고쳐도 된다.**
- 띠가 넓으면 → 못 고치는 한 이 모델로 답이 안 나온다는 것이 **보인다.**
  보수적인 그룹에 할 말은 "당신 값이 틀렸다" 가 아니라 **"당신 값의 불확실성이 결론을 덮는다"** 다.

**② 휴지 전압 감쇠 — 쇼츠 전용 축이 아니다. 후보 관측량으로 쓴다**

> **v1 정정.** v1 은 "LLI/LAM 은 휴지 감쇠에 레버리지가 없으므로 마지막 6–8 h 기울기가
> **쇼츠 전용 신호축**" 이라고 했다. **반증됐다.**

반증 셋:

1. **완화가 6–8 h 뒤에도 남는다.** 무쇼츠 수동 완화 `V = V∞ + 20 mV·exp(−t/10 h)` 는 6 h 와
   12 h 에서 각각 **−1.098 / −0.602 mV/h** 의 기울기를 준다. 실험 문헌도 전압 감쇠법에
   12–20 h 의 완화 교란을 보고한다 (Roth et al., JES 2023).
2. **`C_diff` 가 LLI/LAM 에 의존한다.** 문서 자신의 식이 그 경로를 갖고 있다:
   ```
   V(q) = U_p(y₀ − q/Q_p) − U_n(x₀ + q/Q_n)
   dV/dq = −U'_p/Q_p − U'_n/Q_n
   dV/dt = −I_leak / C_diff ,   C_diff = dq/dV
   ```
   LAM 은 `Q_p`/`Q_n` 을, LLI 와 밸런스는 OCP 기울기를 읽는 **위치**를 바꾼다. 같은 쇼츠·같은
   전압에서 `C_diff` 가 절반이면 기울기 크기는 **두 배**다.
3. **"일정하면 쇼츠 아님" 도 성립하지 않는다.** 같은 기존 쇼츠 + 같은 시작 상태를 여러 사이클에
   반복하면 기울기가 일정할 수 있다. 기울기 증가도 쇼츠 성장만의 증거가 아니다.

그러므로 후반 휴지는 **유용한 후보 관측량**으로 유지하되, 판정에는 시간창·SOC·온도·`C_diff`·
완화 모델·비쇼츠 자기방전(오버행·부반응·열 드리프트)의 불확실성을 함께 넣어야 한다.
σ≈0 에서 LLI/LAM 을 쓸어 평탄한 결과를 얻어도 σ>0 에서의 `C_diff` 민감도를 배제한 것은 아니다.

**③ 쇼츠 세기를 측정 가능한 양으로 — 차원을 맞춰서**

> **v1 정정.** v1 의 `tau_short = C_cell·V_nom/i_leak` 은 **차원이 V·h 라 시간이 아니다.**

```
전하 소모 시간:        t_Q   = C_cell / I_leak                    [Ah]/[A] = h
저항성 전압 감쇠 시간:  tau_V = R_short · C_diff = C_diff · V / I_leak      (C_diff 는 Ah/V)
```

비선형 OCV 에서는 단일 시상수가 아니다 — `t = R ∫ C_diff(V)/V dV`.
또 `sigma_eff·V/L_sep` 는 **A/m²** 다. 셀 단위로 쓰려면 `I = A_cell·sigma_eff·V/L_sep` 와
셀 단위 `C_diff` 를 짝지어야 한다.

### 5-3. 우선순위 (v1 에서 바뀌었다)

| 순서 | 할 일 | 비용 | 왜 |
|---|---|---|---|
| **1** | **`liion.pce2.pin1.soc` 의 t=0 값 확인** (0.924064 인가 0.952290 인가) | **30초** | M1 전체가 여기 달려 있다. v1 은 이 단계를 건너뛰고 수정부터 지시했다 |
| **2** | LAM 계약 정의 — `H/H₀ = 1−LAM` 인가, 두 기작을 묶은 값인가 | 회의 1회 | 정의 없이는 §4-1 이 "수정" 인지 "모델 변경" 인지 정해지지 않는다 |
| **3** | M8 정리 (0.05C 저장해 vs 0.1C 파라미터) + MPH sha256·study/solution/dataset 기록 | 30분 | "안 맞는다" 판정이 이 불일치 때문일 수 있다 |
| **4** | M3 진단 — 적합이 쓴 반쪽셀 곡선과 라이브러리 곡선을 겹쳐 그린다 | 1시간 | 그림 한 장. 파라미터 안 건드림 |
| 5 | 1·2 가 끝난 뒤에 §4-1 수정 + 원본/수정본의 `cs`·`cmax`·`Eeq` 입력값·양극/음극 OCP·Li 재고 대조 | 반나절 | |
| 6 | §5-2 ①의 띠 sweep | 반나절 | |
| 7 | M2 수정(계수 이전 포함) 후 쇼츠 sweep | 반나절 | baseline 유효 전도도 보존 확인 필수 |
| 8 | M4~M7 정리 | 1시간 | 결과 안 바뀜. 다음 사람을 위한 것 |

---

## 6. 우리가 쌓은 것 중 여기에 쓸 수 있는 것

| 우리 자산 | 쓸 수 있나 | 어떻게 |
|---|---|---|
| `degradation-degeneracy/` 의 LLI/LAM 축퇴 판별 | **그대로** | §5-2 ①. 이 `.mph` 를 forward model 로 놓으면 절차가 돈다. 축퇴 방향은 §2-1 로 해석적으로 안다 |
| `bms-balancing/` α·β 검증 하네스 | **바로** | 네 `.xlsx` 가 그 대상이다. §2-2 의 난간은 **지금 하네스가 안 잡는다 — 검사 추가 대상** |
| role-bound receipt | 부분 | "어느 `.xlsx` 의 어느 행이 어느 `.mph` 파라미터가 되었나" 는 어디에도 기록이 없었다. §2 가 처음 적은 것이다 |
| "처음부터 통과하는 테스트는 fixture 가 진실을 가린 것" | 개념으로 | M1 이 그 패턴이다 — **Li 수지 검산은 통과한다** (§3 M1-5). 검산 통과가 모델 정확을 뜻하지 않는다 |
| typed exit code / fail-closed / 게이트 | 아니다 | 우리 파이프라인 내부 규율 |

**이번 라운드가 준 교훈 하나 더**: v1 의 §7 추출기 결함(자식 flags 를 부모로 전파)이
**M5 의 결론을 틀리게 만들었다.** 도구를 검증하지 않으면 도구가 낸 사실도 못 믿는다 —
이 저장소가 `evidence_gate` 에 쓰는 규율과 같은 것을 분석 스크립트에도 적용해야 했다.

---

## 7. 재현 — COMSOL 없이 된다

```bash
unzip -o "ICA_degradation mode.mph" -d mph/
python3 reviews/r14_repros/mph_dump.py --self-test          # 소유권 반례 (1차 리뷰 §2.6)
python3 reviews/r14_repros/mph_dump.py mph/dmodel.xml \
        --refs dPE,dNE,cs_NCM_init,cs_Gr_init,E_end,x_NCM_max,x_NCM_min,i_app
```

> **v1 의 정규식 추출기는 쓰지 마라.** 부모 `PhysicsFeature` 를 **첫 번째** `</PhysicsFeature>`
> 까지 잘라서 (a) 자식 param 을 부모 것으로 출력하고 (b) 자식의 `DISABLED` 를 부모 것으로
> 오인하고 (c) 자식 뒤 부모 자신의 param 을 버렸다. `mph_dump.py --self-test` 가 그 반례를
> 고정한다.

전역 파라미터·OCP 표는 정규식으로도 안전하다 (중첩이 없다):

```python
import re
s = open('mph/dmodel.xml', encoding='utf-8', errors='replace').read()
for m in re.finditer(r'<expressions T="31" name="([^"]*)" expr="([^"]*)"', s):
    print(m.group(1), '=', m.group(2))
for tag in ('mat1', 'mat5'):                       # OCP 보간표
    m = re.search(r'<Material op="[^"]*" tag="%s"' % tag, s)
    blk = s[m.start():s.find('</Material>', m.start())]
    i = blk.find('Eeq_int1')
    p = re.search(r'"((?:[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?[,\s|\']{1,4}){15,})"',
                  blk[max(0, i-500):i+9000])
    print(tag, re.findall(r"'([^']*)','([^']*)'", p.group(1))[:3], '...')
```

`.xlsx` 쪽 §2-1 검증 — **`np.allclose` 기본 허용오차(rtol 1e-5)는 머신 엡실론 증명이 아니다.**
최대 절대오차를 직접 찍는다:

```python
import pandas as pd, numpy as np
d = pd.read_excel('result_L_ref1__0.1C_12h__charge.xlsx')
x = d.C_cell / d.C_cell.iloc[0]
for lbl, err in (('x_cell', d.x_cell - x),
                 ('LAM_PE', d.LAM_PE - (1 - x*d.a_PE/d.a_PE.iloc[0])),
                 ('LAM_NE', d.LAM_NE - (1 - x*d.a_NE/d.a_NE.iloc[0])),
                 ('LLI',    d.LLI    - (1 - d.c_lit/d.c_lit.iloc[0]))):
    print(f'{lbl:7s} max|err| = {np.abs(err).max():.3e}')
print('a_PE 난간:', [int(c) for c, v in zip(d.cycle, d.a_PE) if v == d.a_PE.iloc[0]])
print('LLI-(1-x_cell) 범위:', float((d.LLI-(1-x)).min()), float((d.LLI-(1-x)).max()))
```

**우리가 실행해 확인했다** (2026-09-13). `mph_dump.py --self-test` rc 0,
`--refs` 출력은 §3 M4 표와 일치, `.xlsx` 최대 절대오차는 §2-1 값과 일치.

---

## 8. 이 문서가 하지 않은 것

1. **COMSOL 미실행.** §3 M1-3 의 −14.275 mV 는 t=0 평형 OCP 차이지 해(solution) 비교가 아니다.
   충전 궤적·ICA 봉우리 이동량은 **미검증**이다.
2. **M1 의 조건(A1)이 실행으로 확인되지 않았다.** §3 M1-2 의 실측 넷은 강한 정합적 근거이지
   COMSOL 평가가 아니다. `liion.pce2.pin1.soc` 한 번이면 끝난다.
3. **M1 이 버그인지 설계인지 못 갈랐다** (§3 M1-4). LAM 계약 정의가 선행되어야 한다.
4. M2 의 Bruggeman **지수 값**, `sep1`/`pcb1` 합성 여부, M5 의 Stop Condition 은 GUI 확인 대상.
5. OCP 보간표를 COMSOL 라이브러리 원본과 대조하지 못했다 (M3 의 약한 고리).
6. `dPE` 출처 미상.
7. 실험 전압 곡선 자체를 못 봤다 — 받은 `.xlsx` 는 적합 **결과**만 담고 원 곡선이 없다.
   M3 를 그림으로 확정하려면 원 곡선이 필요하다.
8. MPH 의 sha256, 선택된 study/solution/dataset/paramValues 를 기록하지 않았다 (§5-3 3번).
