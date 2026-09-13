# 마이크로 쇼츠 COMSOL 모델 검토 — `ICA_degradation_mode.mph` (2026-09-13)

> **원본 파일은 이 저장소에 없다.** 이 저장소는 공개이고, `.mph` 와 규진팀 적합 결과 `.xlsx` 는
> 커밋하지 않는다. 이 문서는 **구조 분석 결과만** 담는다. 좌표는 전부 `.mph`(= ZIP) 안
> `dmodel.xml` 의 노드 태그·파라미터 이름이며, COMSOL GUI 에서 같은 이름으로 찾을 수 있다.
>
> **이 문서의 숫자는 사본이다.** 정본은 규진팀이 가진 `.mph` 와 `result_L_*.xlsx`.
> 인용 근거로 쓰지 말고, 아래 §7 의 재현 절차로 각자 다시 뽑아서 쓴다.
>
> 검토 대상: `ICA_degradation mode.mph` · COMSOL 6.4.0.293 · 최종 계산 2026-09-12 22:27 UTC (8.3 s)

---

## 0. 한 문단 요약

이 모델은 **열화모드(LLI·LAM_PE·LAM_NE)를 파라미터로 주입한 full-cell DFN 에 분리막 전자전도를
얹어 마이크로 쇼츠를 켜고 끄는** 1D 모델이다. 회의에서 나온 "레퍼런스 셀과 안 맞는다" 는 증상의
원인은 **주입한 열화모드 값이 아니라 주입하는 배선**에 있다. LAM 이 두 군데에 동시에 곱해져 있고
(`epss` 와 `cs,max`), 그중 한 군데의 짝인 `cs,init` 에는 안 곱해져 있어서 **OCP 를 잘못된
화학량론 위치에서 읽는다**. 그 결과 t=0 셀전압이 약 −14 mV, 충전 구간 전체에서 −5 ~ −20 mV
**비균일하게** 어긋난다. ICA(dQ/dV) 로 보려는 모델에서 봉우리 위치가 그만큼 밀린다는 뜻이라
치명적이다. 게다가 이 모델이 쓰는 OCP 는 COMSOL 내장 라이브러리 곡선(MCMB 흑연·NMC811)인데,
열화모드 값을 만든 α·β 적합은 규진팀 자체 반쪽셀 곡선 위에서 돌았다 — **다른 자 위에서 잰 눈금을
그대로 옮겨 놓은 셈**이다. **아래 수정안은 열화모드 파라미터(LAM_PE·LAM_NE·LLI·dPE·dNE)를
하나도 건드리지 않는다.**

---

## 1. 처음 보는 사람을 위한 모델 지도

### 1-1. 형상 — 1D, 도메인 3개

```
 경계1          도메인1            경계2   도메인2   경계3       도메인3           경계4
   │◀────────── 52 um ──────────▶│◀── 25 um ──▶│◀──────── 44 um ────────▶│
   │      음극 (흑연, pce1)       │  분리막(pcb1) │     양극 (NCM811, pce2)  │
   │                             │              │                          │
 접지                          (전해질)      (전해질)                    전류 인가
 egnd1                                                                    cdc1
 phis = 0                                                          충방전 사이클링
```

- 셀 전압 `E_cell = intop_cc2(phis) - intop_cc(phis)` = 경계4 고체전위 − 경계1 고체전위.
- 1D 라서 **면적은 1 m² 가 기준**이다. 실제 셀 면적 `A_cell = 1.53938 cm²` 는 **후처리에서만**
  쓰인다 (측정 Ah ↔ mol/m² 환산). 전류 경계조건은 `i_1C*C_rate*1[m^2]` 로 들어간다.

### 1-2. 살아 있는 것 / 죽어 있는 것

이 파일은 **반쪽셀(Li metal) 모델에서 full-cell 로 개조된 것**이고, 개조 전 부품이 그대로 남아
있다. 처음 보는 사람이 가장 헷갈리는 지점이라 먼저 적는다.

| 노드 | 상태 | 무엇 |
|---|---|---|
| `pce1` 음극 (흑연) | **활성** | `epss = epss_Gr`, 입자반경 `rp_Gr = 7.5 um`, `Ds = D_g` |
| `pce2` 양극 (NCM811) | **활성** | `epss = epss_pos`, `rp = 10 um`, Bruggeman 지수 `b_PE = 2.2` |
| `pcb1` Porous Conductive Binder (분리막) | **활성** | **σ = `sigma_short` — 이것이 마이크로 쇼츠다** |
| `cdc1` Charge-Discharge Cycling (경계4) | **활성** | 실제 제어기. 충전 먼저, CV 충전 on, Vmax 4.25 / Vmin 2.7, 충전 후 휴지 `trech = 12 h` |
| `egnd1` Electric Ground (경계1) | **활성** | 기준 전위 |
| `ge` Global ODE `Cap` | 활성 | 누적 전하. `SOC = Cap/Q_el` |
| `addm1` 실리콘 | **비활성** | 게다가 `Si_m_f = 0` → `Si_f = 0` → `epss_Si = 0`. **이중으로 꺼져 있다** |
| `es1` Electrode Surface + `lc1` Load Cycle (경계3, Li metal `mat3`) | **비활성** | 반쪽셀 시절의 대극 |
| `ecd1` Electrode Current Density (경계4) | **비활성** | `cdc1` 로 대체됨 |
| `socicd1`, `nfr1`, `negebs1`, `posebs1` | 비활성 | 미사용 |
| `ev` Events (`ds1`/`is1`/`impl1`/`impl2`) | 활성이지만 **무력** | §3 M5 |
| `c` Coefficient Form PDE (`cfeq1`) | 활성이지만 **무력** | `f = dSdt`, `dSdt = 0` → S ≡ 1. Si 이력(hysteresis) 잔재 |
| `ge2` Global ODE `E_lith`/`E_delith` | 활성이지만 **의미 없음** | §3 M6 |
| Parametric Sweep (`param`) | **비활성** | 목록은 `C_rate = 0.05` × `sigma_short = {1e-20, 1.4e-6, 4.67e-6, 1.4e-5}` |

즉 **지금 이 파일을 그냥 Compute 하면**: 단일점 `C_rate = 0.1`, `sigma_short = 1e-20`(= 쇼츠 없음),
실리콘 없는 순수 흑연 음극, CC-CV 충전 후 12 h 휴지.

### 1-3. 마이크로 쇼츠가 걸리는 방식

분리막 도메인에 **전자를 흘리는 고체상을 하나 얹는다**(`pcb1`). 그 고체상의 전도도가
`sigma_short`. 음극(경계2)과 양극(경계3)의 고체전위가 이 상을 통해 이어지므로, 셀 전압에
비례하는 누설 전류가 생긴다 — 이것이 마이크로 쇼츠의 등가회로다.

셋업 전류와 비교하면 (쇼츠 실효 전도도 = `sigma_short * epss^1.5`, §3 M2 참조):

| `sigma_short` | 쇼츠 저항(셀 환산) | 4 V 에서 누설 / 0.1C 인가전류 |
|---|---|---|
| `1e-20` (현재값) | ~1e19 Ω | 0 % — **쇼츠 꺼짐** |
| `1.4e-6` | ~3.8e5 Ω | ~2.7 % |
| `4.67e-6` | ~1.2e5 Ω | ~9.0 % |
| `1.4e-5` | ~3.8e4 Ω | ~27 % |

(`epss = 0.45` 를 그대로 받아들였을 때. M2 를 고치면 이 표가 바뀐다.)

---

## 2. 파라미터가 어디서 오는가 — α·β 적합과 이 모델의 연결 고리

이 부분이 이 검토의 핵심이다. `.mph` 의 열화모드 파라미터는 **규진팀 α·β 적합 출력
`result_L_ref1__0.1C_12h__charge.xlsx` 의 cycle 2 행 한 줄**에서 그대로 옮겨 온 것이다.
네 파일(ref1·ref2·PE1·PE5, 총 37행)을 전수 대조해서 확인했다.

| `.mph` 파라미터 | 출처 |
|---|---|
| `LAM_PE` | ref1 `LAM_PE` [cycle 2] |
| `LAM_NE` | ref1 `LAM_NE` [cycle 2] |
| `LLI` | ref1 `LLI` [cycle 2] |
| `C_lit0_ref1` | ref1 `c_lit` [cycle 0] |
| `dNE` | ref1 `b_NE` [cycle 0] |
| `dm_fNE` / `dm_fPE` | `1 - LAM_NE` / `1 - LAM_PE` 를 손으로 계산해 8자리에서 잘라 넣은 값 |
| `dPE` | **네 파일 어디에도 없음** — 출처 불명 |

### 2-1. 적합 출력의 세 "열화모드" 는 독립 측정량이 아니다

37행 전부에서 **머신 엡실론 수준으로** 다음이 성립한다:

```
x_cell = C_cell / C_cell(cycle 0)
LAM_PE = 1 - x_cell * a_PE / a_PE(cycle 0)
LAM_NE = 1 - x_cell * a_NE / a_NE(cycle 0)
LLI    = 1 - c_lit  / c_lit(cycle 0)
```

즉 LAM 은 **α(전극 용량 스케일)의 변화율**을 용량 유지율로 다시 쓴 것이다. 실제로 적합이 푼 것은
`a_PE, b_PE, a_NE, b_NE, c_lit` 이고, 열화모드 셋은 그 후처리다.

### 2-2. 그런데 그 α 들이 난간(rail)에 붙어 있다

| 파일 | `a_NE` | `a_PE` 가 cycle-0 값에 정확히 붙은 행 | `LAM_PE == LAM_NE` 인 행 |
|---|---|---|---|
| ref1 | 전 사이클 **비트 단위로 동일** | 8 / 10 | 8 / 10 |
| ref2 | 전 사이클 **비트 단위로 동일** | 6 / 10 | 6 / 10 |
| PE1 | 전 사이클 **비트 단위로 동일** | 9 / 10 | 9 / 10 |
| PE5 | 전 사이클 **비트 단위로 동일** | **7 / 7** | **7 / 7** |

또 `b_NE` 는 cycle 0 을 빼면 전 행에서 정확히 `0`, `a_PE` 는 **한 번도 cycle-0 값을 넘지 않는다**
(cycle-0 값이 곧 최댓값). 읽는 방법은 하나다 — **`a_NE` 는 고정되어 있고 `a_PE` 는 상한에 눌려
있다.** `a_PE` 가 상한에 붙는 순간 `LAM_PE = LAM_NE = 1 - x_cell` 이 되어, 세 열화모드가 전부
**용량 감소율 하나를 세 번 이름만 바꿔 부른 것**이 된다. PE5 는 전 사이클이 그 상태다.

이건 `degradation-degeneracy/` 가 PyBaMM 합성 truth 로 잡아낸 **LLI/LAM 축퇴의 실데이터
지문**이다. 여기서는 축퇴가 "여러 해가 같은 잔차를 준다" 가 아니라 **"최적화기가 난간에 눌려
한 해로 붕괴했다"** 는 더 나쁜 형태로 나타난다.

> **이 모델이 고른 ref1 cycle 2 는 ref1 에서 `a_PE` 가 난간에서 떨어져 있는 단 두 행(cycle 1, 2)
> 중 하나다.** 그래서 `LAM_PE ≠ LAM_NE` 인, 전극 구분 정보가 살아 있는 드문 행이다. 의도였든
> 운이었든 고를 수 있는 행 중 나은 쪽이다. 다만 **cycle 3 부터는 그 정보가 사라지므로, 같은
> 방식으로 사이클을 따라가며 모델을 돌리면 cycle 3 이후는 전부 같은 축퇴점을 반복하게 된다.**

---

## 3. 발견

심각도 순. `결론이_바뀜` = 그래프 모양·판정이 바뀜, `숫자가_바뀜` = 값만, `정리` = 오해 유발.

### M1 — LAM 이 두 번 곱해지고, 그 짝이 안 맞는다 · `결론이_바뀜` · **최우선**

**무엇**

```
파라미터:   epss_el  = epss_el_0  * (1-LAM_NE)      ← LAM 1회차 (부피분율)
           epss_pos = epss_pos_0 * (1-LAM_PE)

pce1/pin1:  cEeqref (= cs,max) = cs_Gr_max  * dm_fNE  ← LAM 2회차 (최대농도)
            csinit             = x_Gr_init  * cs_Gr_max        ← dm_fNE 없음 (!)

pce2/pin1:  cEeqref (= cs,max) = cs_NCM_max * dm_fPE  ← LAM 2회차
            csinit             = x_NCM_init * cs_NCM_max       ← dm_fPE 없음 (!)
```

COMSOL 은 평형전위를 `Eeq(soc)`, `soc = cs / cs,max` 로 읽는다. 따라서

```
soc(t=0) = csinit / cEeqref = x_init / dm_f   ≠   x_init
```

**의도한 화학량론보다 음극 +2.64 %, 양극 +3.05 % 높은 지점에서 OCP 를 읽는다.**

**결과 (내장 OCP 표로 직접 계산)**

| | 의도한 soc | 실제 읽는 soc | OCP 차이 |
|---|---|---|---|
| 음극 (흑연) | 0.011721 | 0.012030 | −4.5 mV |
| 양극 (NCM) | 0.924064 | 0.952290 | −18.8 mV |
| **셀 전압 t=0** | **3.0524 V** | **3.0381 V** | **−14.3 mV** |

충전 구간 전체에서 양극 OCP 가 −5 ~ −20 mV **비균일하게** 밀린다 (`x = 0.9 → −18.9`,
`0.7 → −14.3`, `0.5 → −19.3`, `0.3 → −5.0 mV`). 균일 오프셋이면 ICA 봉우리 위치가 통째로
밀릴 뿐이지만, **비균일하면 봉우리 사이 간격이 바뀐다** — dQ/dV 로 열화모드를 읽으려는 모델에서
이건 측정하려는 신호와 같은 크기의 왜곡이다.

추가로 **용량이 (1−LAM)² 로 줄어든다**: 호스트 사이트 수가 `epss × cs,max` 이므로
실효 LAM_NE 2.57 % → **5.08 %**, LAM_PE 2.96 % → **5.84 %**. 주입했다고 믿는 값의 두 배다.

그리고 `soc = x/dm_f` 때문에 **OCP 표 끝에 일찍 닿는다**: 흑연 표는 soc 0.993 에서 끝나는데
실제 x = 0.9675 에서 벌써 닿는다 (그 뒤는 외삽). NCM 도 x = 0.9607 에서 표 끝(0.99).

**이게 버그라는 증거**: 파라미터 표에 `cs_NCM_init = x_NCM_init * cs_NCM_max * dm_fPE` 가
**정의되어 있지만 어느 물리 노드도 그걸 참조하지 않는다.** 누군가 짝을 맞추려고 파라미터를
만들어 놓고, `pce2/pin1` 의 `csinit` 필드는 손으로 친 옛 식 그대로 두었다.

**Li 수지 자체는 맞다** — 여기가 헷갈리는 부분이다. `nLi_0` 도 `x_NCM_init` 도 **맨** `cs_*_max`
를 쓰고, 물리 노드의 `csinit` 도 맨 `cs_*_max` 를 쓴다. 그래서 모델 안의 리튬 총량은 의도대로
`nLi_0 − dLi_LLI` 다. **틀어진 것은 리튬 양이 아니라 OCP 를 읽는 눈금뿐이다.** 그래서 더
찾기 어렵다 — 용량 수지 검산으로는 안 걸린다.

---

### M2 — 마이크로 쇼츠 상(相)의 부피분율이 전해질 분율로 복사돼 있다 · `숫자가_바뀜`

`pcb1` (분리막의 전자전도 상):

```
epsl = epsl_sep      (= 0.45)   ← 전해질 부피분율. 맞다
epss = epsl_sep      (= 0.45)   ← 전자전도 상 부피분율. 같은 값이 들어갔다
```

분리막 부피의 45 % 가 전자 도체라는 뜻이 된다. 물리적으로 마이크로 쇼츠는 **가느다란 필라멘트**
이고, 값을 정할 근거가 없더라도 `epsl_sep` 을 그대로 쓴 것은 복붙이다. 게다가
`ElectricCorrModel = Bruggeman` 이라 실효 전도도가 `sigma_short * 0.45^1.5 = 0.302 * sigma_short`
로 줄어든다 — **sweep 에 적은 `sigma_short` 값은 실제 쇼츠 세기의 3.3배 과대표기**다.

`epss` 와 `sigma_short` 가 곱으로만 들어가므로 **둘은 서로 축퇴다.** 하나를 고정하고 하나만
쓸어야 한다. 권장: `epss` 를 필라멘트 면적비로 쓰되 명시적 파라미터(`f_short`)로 빼고,
sweep 은 `sigma_short` 로만 한다. 또는 `epss` 를 1 로 두고 `sigma_short` 를 **실효 전도도**로
정의한다 (해석이 제일 깔끔하다).

> 확인 필요: Bruggeman 보정이 `pcb1` 의 고체 전도도에 실제로 걸리는지는 XML 의
> `ElectricCorrModel = Bruggeman` 로부터 추론했다. GUI 에서 `liion.pcb1.sigmaeff` 를 찍어
> 0.302·`sigma_short` 인지 한 번 확인하면 끝난다.

---

### M3 — 이 모델의 OCP 는 COMSOL 내장 라이브러리 곡선이다 · `결론이_바뀜`

| 도메인 | 재료 | 출처 | 표 |
|---|---|---|---|
| 1 (음극) | `Graphite, LixC6 MCMB (Negative, Li-ion Battery)` | COMSOL Battery Material Library | 88점, soc 0.0082–0.993, 0.041–0.565 V |
| 3 (양극) | `NMC 811, LiNi0.8Mn0.1Co0.1O2 (Positive, Li-ion Battery)` | COMSOL Battery Material Library | 100점, soc 0.18–0.99, 3.517–4.380 V |

**그런데 `LAM_PE`·`LAM_NE`·`LLI` 를 만든 α·β 적합은 규진팀 자체 반쪽셀 곡선 위에서 돌았다.**
α·β 는 "이 전극 곡선을 얼마나 늘이고 밀면 셀 곡선이 되는가" 라서 **어느 전극 곡선을 썼는지와
분리할 수 없는 양**이다. 다른 곡선 위에서 잰 α 를 이 모델에 넣는 것은 눈금이 다른 자의 눈금값을
옮겨 적는 것과 같다.

**회의에서 나온 "모델이 레퍼런스 셀과 안 맞는다" 의 가장 큰 단일 원인이 이것일 가능성이 높다.**
그리고 이 수정은 **열화모드 파라미터를 건드리지 않는다** — 바꾸는 것은 `mat1`/`mat5` 의 `Eeq`
보간표뿐이다.

또한 `x_NCM_max = 0.927` / `x_NCM_min = 0.215` 와 `E_max_el = 0.502 V` / `E_min_el = 0.078 V`
(흑연 반쪽셀 창) 도 라이브러리 곡선 기준으로 정해진 값이다. `Q_el = 25.036 Ah/m²` 는
`epss_pos_0 * L_pos * cs_NCM_max * (x_NCM_max − x_NCM_min) * F / 3600` 과 **정확히** 일치한다 —
즉 C-rate 와 SOC 의 기준 용량도 라이브러리 곡선에서 유도된 것이다. 곡선을 바꾸면 이 셋도
같이 따라와야 한다.

---

### M4 — `dPE`·`dNE` 는 죽은 파라미터다 · `정리`

두 값 모두 **현행 모델의 어느 식에서도 소비되지 않는다.** 액션 로그를 보면 예전에는

```
x_NCM_init = x_NCM_max - dPE*(x_NCM_max - x_NCM_min)
x_Gr_init  = x_Gr_min  + dNE*(x_Gr_max  - x_Gr_min)
```

였고, 지금은 각각 **Li 수지식**과 `x_Gr_0` 로 대체되었다. 파라미터만 남았다.

남아 있는 것 자체는 해가 없지만, "이 파라미터는 수정 불가" 목록에 `dPE`·`dNE` 가 들어 있다면
**그 제약은 아무것도 제약하지 않는다** — 이미 모델에 영향을 주지 않는다. 협의할 때 구분해서
말할 가치가 있다. (`dNE` 는 ref1 cycle 0 의 `b_NE`, `dPE` 는 네 적합 파일 어디에도 없다.)

---

### M5 — Events 인터페이스가 무력하다 (반쪽셀 잔재) · `정리`

```
is1 지시자:  switch = -(E_cell - E_switch)     end = E_cell - E_switch
impl1:      switch > 0  → CurrentDirection := 1
impl2:      end    > 0  → (재초기화 대상 없음)
E_switch = E_max_pos - E_min_el = 4.256 - 0.078 = 4.178 V
E_end    = E_min_pos - E_max_el = 3.544 - 0.502 = 3.042 V   ← 어디서도 안 쓰임
```

문제 셋:

1. **두 지시자가 같은 문턱(`E_switch`)을 쓴다.** `end` 는 `E_end` 를 봐야 할 자리로 보인다.
2. `impl2` 는 재초기화 대상이 없고, 시간 의존 solver 에 **활성 Stop Condition 이 없다.**
   → `end` 이벤트는 아무것도 하지 않는다.
3. `impl1` 이 세팅하는 `CurrentDirection` 은 **전역 파라미터 `CurrentDirection = 1` 과 이름이
   겹치는 이산 상태**(초기값 −1)다. 이걸 읽는 것은 `i_app` 과 `ge2` 뿐인데 `i_app` 을 쓰던
   `ecd1` 은 비활성이다.
4. `E_switch`·`E_end` 는 **full-cell 양극 한계와 반쪽셀 음극 한계를 섞은 식**이다 — 개조 잔재.

실제 제어는 전부 `cdc1` 이 한다 (Vmax 4.25 / Vmin 2.7). 따라서 **당장 결과를 바꾸지는
않지만**, 파일을 처음 보는 사람은 "4.178 V 에서 끊기겠구나" 로 오독하기 딱 좋다. 지우거나
비활성화하는 게 맞다.

> 확인 필요: "활성 Stop Condition 이 없다" 는 XML 에서 `stopcondarr` 가 비어 있는 것으로
> 판단했다. GUI 의 Time Dependent Solver → Stop Condition 노드에서 한 번 확인.

---

### M6 — `ge2` 의 에너지 적분은 의미 없는 값을 낸다 · `정리`

```
d(E_lith,t)   = if(CurrentDirection == -1,  i_app*(E_cell - E_max_el), 0)
d(E_delith,t) = if(CurrentDirection ==  1, -i_app*(E_cell - E_max_el), 0)
```

`E_max_el = 0.502 V` 는 **흑연 반쪽셀의 0 % SOC 전위**다. full-cell 전압에서 그걸 빼는 것은
물리적 의미가 없다. `i_app` 도 비활성 `ecd1` 의 잔재. 진단용이라 결과에 영향은 없지만,
이 값을 보고 에너지 효율을 논하면 안 된다.

---

### M7 — `SOC` 가 충전 중에 음수다 · `정리`

`ge`: `d(Cap,t) + liion.cdc1.Icell/1[m^2] = 0` → 충전 중 `Icell > 0` 이므로 `Cap` 이 감소.
`SOC = Cap/Q_el` 이므로 **충전할수록 SOC 가 내려간다.** 후처리 전용이지만 그래프를 그대로 쓰면
부호를 뒤집어야 한다.

---

### M8 — 파일 상태가 파라미터 표와 어긋난다 · `정리`

- 저장된 해(solution)는 전부 **`C_rate = 0.05`**, `sigma_short ∈ {1e-20, 1.4e-6, 4.67e-6, 1.4e-5}`
  (2026-09-03 계산). 그런데 현재 파라미터는 **`C_rate = 0.1`**, `sigma_short = 1e-20`,
  최종 계산은 2026-09-12 의 단일점이다.
- Parametric Sweep 노드는 **비활성**이고, 목록도 `C_rate = 0.05` 그대로다.
- 업로드된 실험 데이터는 **0.1C, 12 h** 조건이다. `cdc1` 의 `trech = 12 h` 는 이 프로토콜과 맞다.
- Sweep 의 "Save each solution as model file" 에 **다른 사람 Windows 로컬 경로**가 박혀 있다.
  그 PC 밖에서는 sweep 을 켜는 순간 저장이 실패한다. 지워야 한다.

**즉 파일을 열어 그림을 그리면 0.05C 결과가 보이는데 파라미터 표에는 0.1C 라고 적혀 있다.**
"모델이 데이터와 안 맞는다" 를 판단하기 전에 여기부터 정리해야 한다.

---

### 그 외 확인 필요 (XML 만으로는 단정 못 함)

| 항목 | 내용 |
|---|---|
| `per1` 의 `rp = 10 um` | 음극 반응 노드에도 `rp` 가 있는데 `pce1/pin1` 은 `rp_Gr = 7.5 um`. `ActiveSpecificSurfaceAreaType = ParticleBasedArea` 면 입자 노드 값을 쓰므로 무해할 가능성이 높지만, `liion.pce1.Av` 를 찍어 `3*epss_Gr/rp_Gr` 인지 확인 |
| `per1` 음극의 `AdsorbingDesorbingSpecies = ads1` | `nfr1`(Nonfaradaic Reactions)이 비활성이라 무해할 것으로 보이나 확인 |
| `dm_fNE`/`dm_fPE` 를 손계산으로 박아 넣음 | `1-LAM_NE` 와 1.2e−9 차이. 지금은 무해하지만 **`1-LAM_NE` 로 바꿔 쓰면 파생값이 자동 추종**한다 (파라미터 값은 안 바뀜) |
| `Q_el`·`A_cell` 대 실측 | `Q_el * A_cell = 3.854 mAh` 인데 ref1 cycle 0 실측 `C_cell` 은 약 3.90 mAh (−1.2 %). 기준 용량이 실셀과 1 % 어긋난 채 C-rate 와 SOC 를 정의하고 있다 |

---

## 4. 수정안 — 열화모드 파라미터를 하나도 건드리지 않는 버전

> 제약: `LAM_PE`, `LAM_NE`, `LLI`, `dPE`, `dNE` 는 수정 불가.
> 아래 수정은 **전부 그 제약 안**이다 — 값이 아니라 **값을 쓰는 방법**만 고친다.

### 4-1. M1 수정 — LAM 을 `epss` 한 곳에만 (권장, 편집 2줄)

DFN 의 표준 규약이고 편집이 제일 작다.

| 노드 | 필드 | 지금 | 바꿀 것 |
|---|---|---|---|
| `pce1 / pin1` | `cEeqref` | `cs_Gr_max*dm_fNE` | **`cs_Gr_max`** |
| `pce2 / pin1` | `cEeqref` | `cs_NCM_max*dm_fPE` | **`cs_NCM_max`** |

`csinit`, `epss_el`, `epss_pos`, `x_NCM_init`, `nLi_0` 는 **그대로 둔다.**

- LAM 은 `epss` 에서 1회만 적용 → 실효 LAM 이 선언값과 일치.
- `soc(t=0) = x_init` 정확히 성립 → OCP 를 제 위치에서 읽는다.
- Li 수지는 이미 맞았으므로 그대로 유지.
- **왜 이쪽인가**: LAM(활물질 손실)은 "입자 수가 준 것"이지 "남은 입자의 결정 격자가 쪼그라든
  것"이 아니다. 격자 사이트 손실은 다른 열화모드이고, 지금 모델은 그 둘을 같은 값으로
  동시에 걸고 있다.

**대안 (비권장)**: LAM 을 `cs,max` 에만 걸려면 `epss_el = epss_el_0`, `epss_pos = epss_pos_0`
로 되돌리고, `csinit` 에 `dm_f` 를 곱하고, `nLi_0`·`x_NCM_init` 의 `cs_*_max` 를
`cs_*_max*dm_f` 로 전부 바꿔야 한다 (안 그러면 Li 수지가 깨진다). 편집이 6곳이고 공극률
거동도 바뀐다.

**어느 쪽이든 검산 한 줄**: 수정 후 `liion.pce2.pin1.soc` 의 t=0 값이 `x_NCM_init` 과
같은지 찍는다. 지금은 `x_NCM_init/dm_fPE` 가 나온다.

### 4-2. M2 수정 — 쇼츠 축퇴 제거

`pcb1.epss` 를 `epsl_sep` 에서 떼어낸다. 새 파라미터 하나:

```
f_short = 1        (쇼츠 상의 부피분율; 1 로 두면 sigma_short 가 곧 실효 전도도)
pcb1.epss = f_short
pcb1.ElectricCorrModel = No correction   (또는 f_short 를 그대로 유효분율로 해석)
```

이러면 sweep 값이 그대로 실효 쇼츠 세기가 되고, `epss × sigma_short` 축퇴가 사라진다.

### 4-3. M3 수정 — OCP 를 α·β 적합이 쓴 곡선으로 교체

`mat1`/`mat5` 의 `Eeq` 보간표를 **MATLAB 적합에 들어간 그 반쪽셀 곡선**으로 바꾼다.
동시에 그 곡선 기준으로 다시 잡아야 하는 것:

| 파라미터 | 다시 잡는 법 |
|---|---|
| `x_NCM_max` / `x_NCM_min` | 새 양극 곡선의 사용 창 |
| `E_max_el` / `E_min_el` | 새 음극 곡선의 0 % / 100 % SOC 전위 |
| `Q_el` | `epss_pos_0*L_pos*cs_NCM_max*(x_NCM_max-x_NCM_min)*F/3600` 재계산 |
| `x_Gr_0`, `x_NCM_0` | 새 곡선에서 BOL 상태 |

**이건 열화모드 파라미터가 아니다** — 기준 곡선이다. 제약 밖이다.

### 4-4. 정리 작업 (결과 안 바뀜, 오독 방지)

- `ev`(Events), `cfeq1`, `ge2` 비활성화 또는 삭제 — 전부 반쪽셀 잔재.
- `es1`·`lc1`·`ecd1`·`mat3`(Li metal) 삭제.
- `addm1`·`mat4`(Si) 와 `D_si`·`k_si`·`rp_Si`·`x_Si_*`·`Si_ocv`·`S_init`·`K_S`·`U_avg`·
  `U_offset`·`Eeq_Si`·`dx_Sidt`·`dSdt` — 실리콘을 쓸 계획이 없으면 삭제, 쓸 계획이면
  **왜 지금 꺼져 있는지 주석**을 남긴다.
- `dm_fNE`/`dm_fPE` 를 `1-LAM_NE`/`1-LAM_PE` 로 (값 불변, 추종성 확보).
- Sweep 의 Windows 로컬 저장 경로 제거.
- `SOC` 부호 정정 또는 설명 주석.
- Sweep 목록을 `C_rate = 0.1` 로 (실험 조건과 맞춤), 저장된 0.05C 해는 지우거나 이름표를 단다.

---

## 5. 더 좋은 방향성 — "맞추는 모델" 대신 "가르는 모델"

### 5-1. 지금 방향의 구조적 한계

회의 내용은 "α·β / LAM / LLI 를 넣고, 마이크로 쇼츠가 없었다면 전압 곡선이 사이클마다 어떻게
갔을지 본다. 그러려면 레퍼런스 셀과 맞아야 한다" 였다. 이 방향은 **모델이 한 점을 정확히
재현해야 성립**한다. 그런데 §2-2 에서 본 대로 입력 파라미터가 축퇴 난간에 붙어 있다 —
ref1 에서 8/10, PE5 에서 7/7 사이클이 `LAM_PE = LAM_NE = 1 − x_cell` 로 붕괴한다.
**한 점을 정확히 맞춰도 그 점이 유일하지 않다면 맞았다는 사실이 아무것도 증명하지 않는다.**

그리고 파라미터는 수정 불가다. 그렇다면 **파라미터를 고치는 대신 파라미터의 불확실성을
입력으로 받는 쪽**으로 방향을 바꾸는 것이 남은 유일한 정직한 길이다.

### 5-2. 제안 — 세 단계

**① 모델을 점 예측기에서 띠(band) 예측기로 바꾼다**

§2-1 의 닫힌 형태 덕분에 축퇴 방향을 **정확히 안다**: `a_PE` 가 난간에 붙으면
`LAM_PE → 1 − x_cell`. 그러니 난간에서 떨어진 `a_PE` 값의 범위를 잡아
`(LAM_PE, LAM_NE, LLI)` 삼중항 집합을 만들고, **그 집합 전체를 sweep** 한다.
출력은 곡선 하나가 아니라 **띠**다.

- 띠가 좁으면 → 파라미터 불확실성이 결론에 영향 없음. **파라미터를 못 고쳐도 된다.**
- 띠가 넓으면 → 파라미터를 못 고치는 한 이 모델로는 답이 안 나온다는 것이 **증명**된다.
  보수적인 그룹을 설득할 근거는 "당신 값이 틀렸다" 가 아니라 **"당신 값의 불확실성이
  결론을 덮는다"** 다. 후자는 파라미터를 공격하지 않으므로 훨씬 통과하기 쉽다.

이건 `degradation-degeneracy/` 가 이미 만들어 둔 것과 같은 구조다 (§6).

**② 관측량을 충전 곡선에서 휴지 전압 감쇠로 옮긴다 — 이게 핵심이다**

마이크로 쇼츠와 LLI/LAM 은 **물리적으로 다른 종류의 신호**를 낸다:

| | LLI / LAM | 마이크로 쇼츠 |
|---|---|---|
| 하는 일 | OCP 조성을 재배치 (전하 보존) | 전압에 비례하는 **누설 전류** |
| 충전 곡선 | 길이·모양 변화 | 길이 변화 (겉보기 용량 감소) |
| **개방회로 휴지** | **전압 유지** (확산 완화 후 평탄) | **전압이 계속 내려간다** |
| 시간 의존성 | 없음 | **있다 — 휴지 길이에 비례** |

**LLI/LAM 축퇴는 휴지 감쇠에 아무 레버리지가 없다.** 그래서 축퇴가 아무리 심해도
휴지 감쇠는 쇼츠만의 신호다. 그리고 이 모델은 **이미 그 프로토콜을 갖고 있다** —
`cdc1.trech = 12 h`, 업로드된 데이터도 `0.1C_12h`. 지금은 쓰고 있지 않을 뿐이다.

구체적으로:

```
관측량:  dV/dt   (휴지 구간, 확산 완화가 끝난 뒤 — 대략 마지막 6~8 h 구간의 기울기)
예측:    dV/dt ≈ -(i_leak / C_diff),  i_leak = sigma_eff * V / L_sep  (V 에 선형)
판정:    기울기가 사이클에 따라 커지면 쇼츠 성장, 일정하면 쇼츠 아님
```

**이 축에서는 파라미터 수정 불가 제약이 아프지 않다.** LLI/LAM 을 어떤 값으로 넣든
휴지 기울기는 거의 안 변하기 때문이다. 먼저 그것부터 모델로 확인하면 된다 —
`sigma_short = 1e-20` 고정하고 LLI/LAM 을 축퇴 집합 전체로 쓸었을 때 휴지 기울기가
얼마나 벌어지는가. 그 폭이 쇼츠 신호보다 작으면 **분리 가능**이 증명된다.

**③ 4-2 를 먼저 하고 쇼츠 세기 축을 실측 단위로 다시 잡는다**

지금 sweep 의 `sigma_short` 값은 (a) Bruggeman 3.3배와 (b) `epss = 0.45` 때문에
실효 세기와 직접 대응하지 않는다. 쇼츠를 **자기방전 시간상수** 같은 측정 가능한 양으로
파라미터화하면 실험과 바로 비교된다:

```
tau_short = C_cell * V_nom / i_leak     [h]
```

12 h 휴지에서 볼 수 있는 범위는 대략 `tau_short` 가 수십~수백 h 인 구간이다.
그 구간에 대응하는 `sigma_short` 만 쓸면 계산도 아낀다.

### 5-3. 우선순위

| 순서 | 할 일 | 비용 | 왜 먼저 |
|---|---|---|---|
| 1 | **M1 수정** (`cEeqref` 2줄) | 5분 | 이거 안 고치면 다른 모든 비교가 −14 mV 편향 위에 쌓인다 |
| 2 | **M8 정리** (0.05C 저장해 vs 0.1C 파라미터) | 10분 | "안 맞는다" 판정이 이 불일치 때문일 수 있다 |
| 3 | **M3 진단** — 적합이 쓴 반쪽셀 곡선과 라이브러리 곡선을 겹쳐 그린다 | 1시간 | 차이가 크면 이게 주범이다. 그림 한 장으로 끝난다 |
| 4 | **②의 분리 가능성 검증** — 쇼츠 끄고 축퇴 집합 sweep → 휴지 기울기 폭 | 반나절 | 이 결과가 이후 방향 전체를 정한다 |
| 5 | M2 수정 후 쇼츠 sweep 재실행 | 반나절 | 4번이 분리 가능하다고 나온 뒤에 |
| 6 | M4~M7 정리 | 1시간 | 결과 안 바뀜. 다음 사람을 위한 것 |

---

## 6. 우리가 쌓은 것 중 여기에 바로 쓸 수 있는 것

| 우리 자산 | 이 모델에 쓸 수 있나 | 어떻게 |
|---|---|---|
| `degradation-degeneracy/` 의 **LLI/LAM 축퇴 판별** | **그대로 쓸 수 있다** | §5-2 ①. 합성 truth 대신 이 `.mph` 를 forward model 로 놓으면 같은 절차가 그대로 돈다. 축퇴 방향은 §2-1 닫힌 형태로 이미 해석적으로 안다 |
| `bms-balancing/` 의 **α·β 검증 하네스** | **바로 쓸 수 있다** | 이 네 `.xlsx` 가 정확히 그 하네스의 대상이다. §2-2 의 난간(`a_NE` 고정, `a_PE` 상한, `b_NE = 0`)은 하네스가 자동으로 잡아야 할 축이다 — **지금은 안 잡는다. 검사 추가 대상** |
| **role-bound receipt / authority roster** | 부분적 | `.mph` 는 서명 대상이 아니지만, "어느 `.xlsx` 의 어느 행이 어느 `.mph` 파라미터가 되었는가" 는 지금 **아무 데도 기록이 없다.** 이 문서가 그걸 처음 적은 것이다. receipt 로 고정할 가치가 있다 |
| **"처음부터 통과하는 테스트는 fixture 가 진실을 가린 것"** | 개념으로 쓸 수 있다 | M1 이 정확히 그 패턴이다 — Li 수지 검산은 **통과한다**. 수지는 맞고 OCP 눈금만 틀렸기 때문. 검산이 통과했다고 모델이 맞는 게 아니다 |
| **typed exit code / fail-closed** | 아니다 | COMSOL 쪽엔 해당 없음 |

**정리**: 축퇴 판별과 α·β 하네스는 그대로 얹힌다. 나머지(서명·게이트)는 우리 파이프라인
내부 규율이라 COMSOL 파일에 옮길 것이 아니다. **대신 `.xlsx` 행 → `.mph` 파라미터 사슬을
기록으로 고정하는 것 하나는 지금 바로 가치가 있다** — 지금은 그 사슬이 사람 머릿속에만 있고,
이번에 37행 전수 대조를 해서야 ref1 cycle 2 라는 걸 알아냈다.

---

## 7. 재현

`.mph` 는 ZIP 이다. 파라미터·물리 노드는 전부 그 안 `dmodel.xml` 에 텍스트로 들어 있다.
COMSOL 없이 확인할 수 있다.

```bash
unzip -o "ICA_degradation mode.mph" -d mph/
cd mph/
```

```python
import re
s = open('dmodel.xml', encoding='utf-8', errors='replace').read()

# (1) 전역 파라미터 전부
for m in re.finditer(r'<expressions T="31" name="([^"]*)" expr="([^"]*)"', s):
    print(m.group(1), '=', m.group(2))

# (2) 물리 노드의 실제 값 (M1 은 여기서 보인다)
for m in re.finditer(r'<PhysicsFeature op="([^"]+)" tag="([^"]+)" name="([^"]*)"', s):
    blk = s[m.start():s.find('</PhysicsFeature>', m.start())]
    flag = re.search(r'<entityFlags T="51">([^<]*)</entityFlags>', blk)
    print(m.group(2), m.group(1), 'DISABLED' if flag and 'DISABLED' in flag.group(1) else 'active')
    for p in re.finditer(r'<param T="33" param="(csinit|cEeqref|epss|epsl|sigma|rp|Ds)" value="([^"]*)"', blk):
        print('   ', p.group(1), '=', p.group(2))

# (3) OCP 보간표
for tag in ('mat1', 'mat5'):
    m = re.search(r'<Material op="[^"]*" tag="%s"' % tag, s)
    blk = s[m.start():s.find('</Material>', m.start())]
    i = blk.find('Eeq_int1')
    p = re.search(r'"((?:[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?[,\s|\']{1,4}){15,})"', blk[max(0,i-500):i+9000])
    print(tag, re.findall(r"'([^']*)','([^']*)'", p.group(1))[:3], '...')
```

`.xlsx` 쪽 §2-1 닫힌 형태 검증:

```python
import pandas as pd, numpy as np
d = pd.read_excel('result_L_ref1__0.1C_12h__charge.xlsx')
x = d.C_cell / d.C_cell.iloc[0]
assert np.allclose(d.x_cell, x)
assert np.allclose(d.LAM_PE, 1 - x*d.a_PE/d.a_PE.iloc[0])
assert np.allclose(d.LAM_NE, 1 - x*d.a_NE/d.a_NE.iloc[0])
assert np.allclose(d.LLI,    1 - d.c_lit/d.c_lit.iloc[0])
print('a_PE 난간:', [int(c) for c, v in zip(d.cycle, d.a_PE) if v == d.a_PE.iloc[0]])
```

---

## 8. 이 문서가 하지 않은 것

- **COMSOL 을 실제로 돌려 보지 않았다.** 모든 수치는 `dmodel.xml` 의 식과 내장 OCP 표에서
  직접 계산한 것이다. §3 M1 의 −14.3 mV 는 t=0 OCP 차이이지 **해(solution) 비교가 아니다.**
  실제 전압 궤적 차이는 확산·과전압이 섞이므로 돌려 봐야 안다.
- **M5 의 Stop Condition, M2 의 Bruggeman 적용 여부는 XML 추론이다.** GUI 확인이 남아 있다.
- `dPE` 의 출처를 못 찾았다. 네 `.xlsx` 어디에도 없다.
- 실험 곡선(전압 vs 용량) 자체를 못 봤다 — 받은 `.xlsx` 는 적합 **결과**만 담고 있고
  원 곡선이 없다. M3 를 그림으로 확정하려면 원 곡선이 필요하다.
