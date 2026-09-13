# COMSOL DFN 재구축 명세 — 마이크로 쇼츠 모델 (6.3 이상, 2026-09-13)

> **이 문서가 답하는 것과 답하지 않는 것을 먼저 분명히 한다.**
>
> - **답하지 않는다**: "규진팀 `.mph` 가 실제로 무엇을 계산했나." 그건 XML 로 이미 끝났다 —
>   두 입자 노드의 `cEeqref_mat = from_mat` 이고 재료 `csmax` 에 dm 이 없다.
>   즉 **LAM 은 `epss` 에서 한 번만 걸리고 `soc(t=0) = x_init` 이다.** M1 은 죽었다.
> - **답한다**: 우리가 통제하는 **깨끗한 forward model**. 잔재(반쪽셀 Li metal · Si · 죽은
>   Events · 0.05C 저장해)가 없고 무엇을 넣었는지 다 안다. 축퇴 띠 sweep 과 휴지 감쇠
>   분리(다음 단계)가 이것을 요구한다.
>
> 원본 값의 출처는 `.mph` 의 `dmodel.xml` 이고 추출기는 `reviews/r14_repros/mph_dump.py` 다.
> 원본 파일과 규진팀 자료는 이 저장소에 없다.

---

## 0. 만들기 전에 정해야 하는 것 두 개

재구축은 **원본의 애매한 자리를 그대로 옮기지 않는다.** 아래 둘은 명시적으로 고른다.

### (a) LAM 을 어디에 적용하나 — **`epss` 한 곳** (권장)

```
epss_el  = epss_el_0  * (1 - LAM_NE)
epss_pos = epss_pos_0 * (1 - LAM_PE)
cs,max   = 재료값 그대로 (dm 곱하지 않는다)
cs,init  = x_init * cs,max
```

원본이 실제로 하는 것이 이것이다 (선택자가 `from_mat` 이므로). 사용자 입력칸에 남아 있는
`cs_max*dm` 은 **선택되지 않은 식**이니 옮기지 않는다.

> LAM 을 "부피분율 + 사이트밀도" 둘로 나눠 넣고 싶으면 그건 **다른 모델**이다.
> 그렇게 하려면 `cs,init` 에도 같은 `dm` 을 곱하고 Li 수지식도 같이 고쳐야 한다 (§5).

### (b) 쇼츠 세기를 무엇으로 파라미터화하나 — **실효 전도도** (권장)

```
pcb1.epss             = 1                (물리 분율 해석을 버리고 유효 계수로 쓴다)
pcb1.ElectricCorrModel = No correction
sigma_short           = 실효 전도도 [S/m]   ← sweep 축
```

원본은 `epss = epsl_sep = 0.45` + Bruggeman 이라 실효값이 `0.302 × sigma_short` 였다.
**원본 baseline 을 재현하려면** sweep 값에 `0.301869177` 을 곱해서 넣는다.

---

## 1. 형상 (Geometry) — 1D

`Component 1 > Geometry 1` → **Interval**, Specify: **Number of layers (len)**

| 층 | 두께 | 도메인 |
|---|---|---|
| 1 | `L_el = 52 [um]` | 음극 |
| 2 | `L_sep = 25 [um]` | 분리막 |
| 3 | `L_pos = 44 [um]` | 양극 |

→ 도메인 1·2·3, 경계 1(x=0)·2·3·4(x=121 µm).
**1D 라 면적 기준은 1 m² 다.** 실제 셀 면적은 후처리·Li 재고 환산에만 쓴다 (§2 `A_cell`).

---

## 2. 파라미터 (`Global Definitions > Parameters 1`)

그대로 붙여넣을 수 있게 이름=식 으로 적는다. **`dm_fNE`·`dm_fPE` 는 넣지 않는다** (§0-a).

```
# ── 형상·면적
L_el              52[um]
L_sep             25[um]
L_pos             44[um]
A_cell            1.53938[cm^2]
electrode_area    A_cell

# ── 열화모드 입력 (규진팀 적합 결과. 이 셋만 바꿔 가며 쓴다)
LAM_PE            0.0296398242
LAM_NE            0.0257219788
LLI               0.0439355
C_lit0_ref1       0.003765381[A*h]

# ── 부피분율
eps_binder_el     0.1
epss_el_0         0.63122
epss_pos_0        0.58803
epss_el           epss_el_0*(1-LAM_NE)
epss_pos          epss_pos_0*(1-LAM_PE)
epsl_el           1-eps_binder_el-epss_el
epsl_pos          1-epss_pos-eps_binder_el
epsl_sep          0.45
epss_Gr           epss_el                 # Si 미사용 (원본의 epss_el*(1-Si_f), Si_f=0)

# ── 재료 상수
cs_Gr_max         31507[mol/m^3]
cs_NCM_max        50707.7[mol/m^3]
rp_Gr             7.5[um]
rp_NCM            10[um]
D_g               7.1e-15[m^2/s]
D_NCM             1e-13[m^2/s]
k_g               2.12e-10[m/s]
k_NCM             9.8e-10[m/s]
K_gr              100[S/m]
K_NCM             0.17[S/m]
b_PE_brugg        2.2                     # ⚠ 적합의 b_PE 와 이름이 겹치지 않게 바꿨다
F_const           96485.33212[C/mol]

# ── 초기 상태와 Li 수지
x_NCM_0           0.927
x_Gr_0            0.01172068149
x_Gr_init         x_Gr_0
nLi_0             epss_pos_0*L_pos*cs_NCM_max*x_NCM_0 + epss_el_0*L_el*cs_Gr_max*x_Gr_0
dLi_LLI           C_lit0_ref1*LLI/F_const/A_cell
nLi_target        nLi_0 - dLi_LLI
x_NCM_init        (nLi_target - epss_el*L_el*cs_Gr_max*x_Gr_init)/(epss_pos*L_pos*cs_NCM_max)

# ── 운전 조건
x_NCM_max         0.927
x_NCM_min         0.215
Q_el              epss_pos_0*L_pos*cs_NCM_max*(x_NCM_max-x_NCM_min)*F_const/3600[s/h]
i_1C              Q_el/1[h]
C_rate            0.1

# ── 마이크로 쇼츠
sigma_short       1e-20[S/m]              # sweep 축
```

> `Q_el` 은 원본에서 `25.036[A*h/m^2]` 로 **박혀 있었다**. 위 식이 그 값과 정확히 같다 (실측).
> 식으로 두면 창을 바꿀 때 자동으로 따라온다.

---

## 3. 재료 (Materials)

| tag | 라이브러리 | 선택 |
|---|---|---|
| 음극 | **Battery Material Library > Graphite, LixC6 MCMB (Negative, Li-ion Battery)** | 도메인 1 |
| 전해질 | **LiPF6 in 3:7 EC:EMC (Liquid, Li-ion Battery)** | 도메인 2 (또는 전체) |
| 양극 | **NMC 811, LiNi0.8Mn0.1Co0.1O2 (Positive, Li-ion Battery)** | 도메인 3 |

> ⚠ **이 라이브러리 곡선이 α·β 적합에 쓴 반쪽셀 곡선과 다르다** (분석 문서 M3).
> 실셀과 맞추려면 나중에 규진팀 곡선으로 갈아 끼워야 하고, 그때 `x_NCM_max/min` ·
> `Q_el` · `x_Gr_0` · `x_NCM_0` 도 그 곡선 기준으로 다시 잡아야 한다.
> 지금은 **라이브러리로 시작한다** (원본과 같은 출발점).

---

## 4. 물리 (Lithium-Ion Battery, `liion`)

### 4-1. 음극 — Porous Electrode (도메인 1)

| 칸 | 값 |
|---|---|
| Electrolyte volume fraction `epsl` | `epsl_el` |
| Electrode volume fraction `epss` | `epss_Gr` |
| Effective conductivity (전해질·고체·확산) | User defined, `epsl_el^2.5` |
| Electrical conductivity | `K_gr` (등방) |

**하위 Particle Intercalation 1**

| 칸 | 값 |
|---|---|
| Particle material | 음극 재료 (mat1) |
| **Maximum concentration** | **From material** ← §0-a. 사용자 식 넣지 않는다 |
| Initial species concentration | `x_Gr_init*cs_Gr_max` |
| Particle radius `rp` | `rp_Gr` |
| Diffusion coefficient | `D_g` |
| Particle concentration | Solve in extra dimension |

**하위 Porous Electrode Reaction 1**: Equilibrium potential **From material**,
Kinetics **Lithium insertion**, Exchange current density **From rate constant**, `k = k_g`,
Active specific surface area **Particle based**.

### 4-2. 양극 — Porous Electrode (도메인 3)

음극과 같되:

| 칸 | 값 |
|---|---|
| `epsl` / `epss` | `epsl_pos` / `epss_pos` |
| Effective conductivity | User defined, `epsl_pos^b_PE_brugg` |
| Electrical conductivity | `K_NCM` |
| Maximum concentration | **From material** |
| Initial species concentration | `x_NCM_init*cs_NCM_max` |
| `rp` / `Ds` / `k` | `rp_NCM` / `D_NCM` / `k_NCM` |

### 4-3. 분리막 — Separator (도메인 2)

`epsl = epsl_sep`, Bruggeman.

### 4-4. **마이크로 쇼츠 — Porous Conductive Binder (도메인 2)**

이것이 쇼츠다. 분리막에 **전자를 흘리는 고체상**을 얹어 두 전극의 `phis` 를 잇는다.

| 칸 | 값 |
|---|---|
| Electrolyte volume fraction | `epsl_sep` |
| **Electrode volume fraction `epss`** | **`1`** ← §0-b |
| **Effective electrical conductivity** | **No correction** ← §0-b |
| Electrical conductivity | `sigma_short` (등방 3×3) |

### 4-5. 경계

| 노드 | 경계 | 설정 |
|---|---|---|
| Electric Ground | 1 (x=0) | — |
| **Charge-Discharge Cycling** | 4 (x=L) | 아래 |

**Charge-Discharge Cycling**

| 칸 | 값 |
|---|---|
| Start with | **Charge** |
| Charge current `Ich` | `i_1C*C_rate*1[m^2]` |
| Discharge current `Idch` | `-i_1C*C_rate*1[m^2]` |
| CV charge | **on**, `Vmax = 4.25[V]`, cutoff `iupper = i_1C*C_rate*1[m^2]*0.1` |
| Open circuit after charge | **on**, `trech = 12[h]` |
| CV discharge / OC discharge | off |
| `Vmin` | `2.7[V]` |

> `trech = 12 h` 는 실험 프로토콜(`0.1C_12h`)과 맞춘 것이고, 휴지 감쇠 관측(다음 단계)이
> 이 구간을 쓴다.

### 4-6. **넣지 않는 것** (원본의 잔재)

- Additional Porous Electrode Material (Silicon) 과 `D_si`·`k_si`·`rp_Si`·`x_Si_*`·`Eeq_Si`
- Electrode Surface + Load Cycle + Lithium Metal 재료 (반쪽셀 대극)
- Electrode Current Density (`cdc1` 로 대체)
- **Events 인터페이스** (`ds1`·`is1`·`impl1`·`impl2`) 와 `CurrentDirection`·`E_switch`·`E_end`
  — 원본에서도 인터페이스째 **DISABLED** 다
- Coefficient Form PDE (`S` 이력 변수) 와 `dSdt`·`K_S`·`U_avg`·`U_offset`
- Global ODE `E_lith`/`E_delith` (반쪽셀 전위를 빼고 있어 의미 없음)
- SOC and Initial Charge Distribution (원본에서 DISABLED)

### 4-7. 넣을 Global ODE 하나 (선택)

누적 전하가 필요하면:

```
Global ODEs and DAEs:  d(Cap,t) - liion.cdc1.Icell/1[m^2] = 0     # 단위 C/m^2
정의 변수:              SOC = Cap/Q_el
```

> 원본은 부호가 `+` 라 충전 중 SOC 가 음수였다. 위처럼 `−` 로 둔다.
> **주의**: 쇼츠가 켜지면 외부 전류 적분은 내부 누설을 빠뜨리므로 물리적 SOC 가 아니다.

---

## 5. 만든 뒤 검산 (계산 전, `Study > Get Initial Value` 후 Global Evaluation)

| 표현식 | 기대값 |
|---|---|
| `liion.pce1.pin1.cEeqref` | **31507** (재료값) |
| `liion.pce2.pin1.cEeqref` | **50707.7** |
| `liion.soc_average_pce1` | `x_Gr_init` = **0.0117207** |
| `liion.soc_average_pce2` | `x_NCM_init` = **0.924064** |
| `epss_el` / `epss_pos` | **0.614984** / **0.570601** |
| `nLi_target` | **1.188226** [mol/m²] |
| `Q_el` | **25.036** [A·h/m²] |
| `E_cell` (t=0) | **≈ 3.0524** [V] |

**`soc_average_pce2` 가 0.924064 로 나오면 §0-a 대로 배선된 것이다.**
0.952290 이 나오면 어딘가에 `dm` 이 한 번 더 들어갔다.

---

## 6. Study

1. **Time Dependent** — `cdc1` 이 시간을 몰므로 출력 시각만 촘촘히 (예: `range(0,60,151200)` s)
2. **Parametric Sweep** (나중) — `sigma_short` 를 축으로. 원본이 쓴 값에 §0-b 계수를 적용하면
   `1e-20 · 4.2e-7 · 1.41e-6 · 4.23e-6` (= `{1e-20, 1.4e-6, 4.67e-6, 1.4e-5} × 0.301869177`)

---

## 7. 이 명세가 담지 않은 것

- 원본의 메시 설정·solver tolerance (기본값으로 시작하고 수렴 확인)
- 전해질 물성 세부 (`Dl = 7.5e-11`, `transpNum = 0.363` 은 원본이 재료 기본값을 덮어쓴 값 —
  라이브러리 기본과 다르면 맞춰야 한다)
- `x_NCM_max/min` 을 라이브러리 곡선에서 다시 유도하는 절차 (§3 경고)
- 규진팀 반쪽셀 OCP 로 교체하는 절차 (분석 문서 §4-3)

---

## 8. v1.1 — 6.3 재구축의 현지 짧은 검증과 그 독립 검토 뒤 보정 (2026-09-13)

사용자 PC 에서 이 명세로 6.3 모델을 만들어 **5초 무부하 · 0.1C 충전 5초**를 돌렸고, 그 인계 ZIP
(`COMSOL63_VALIDATED_SHORT_HANDOFF.zip`, sha256 `fe52f0d7…`) 을 Codex 가 독립 검토했다 — 원문은
`reviews/r14_repros/codex63/COMSOL63_SHORT_REVIEW.md` (ZIP 자체는 이 저장소에 없다). 판정: **제한된 검증은 뒷받침됨 ·
전체 프로토콜 승인은 보류**. 이 명세에 대해 뜻하는 것:

### 8-1. 확인된 것 — §5 검산이 독립 산술로 재현됐다

| §5 의 기대 | 검토자의 독립 계산 (모델 Java 의 표·보정식만으로) |
|---|---|
| `soc_average_pce2` = `x_NCM_init` = **0.924064** → §0-a 대로 배선 | 양극 x = **0.9240638866948166** |
| `soc_average_pce1` = `x_Gr_init` = **0.0117207** | 음극 x = **0.01172068149** |
| (검산표에 없던 것) 초기 OCV | 양극 3.5783867744 − 음극 1.4130534479 = **2.1653333265 V** — CSV 의 2.165333326500236 V 와 일치 |

즉 재구축은 §0-a(LAM 은 `epss` 한 곳) 대로 됐고, 0.952290 이 아니다. 초기 OCV 2.165 V 가 낮은 것은 **MCMB 음극 표의
가파른 구간**(x=0.01 → 1.520893 V · x=0.02 → 0.893923 V)에 초기 조성이 놓여서다 — 부호·정규화 오류가 아니고,
원본의 3.0524 V 에 맞추려고 초기 조성이나 전압 offset 을 조정할 근거도 없다. **이 값은 그대로 둔다.**

### 8-2. 보정 1 — `Vmax = 4.25 V` CV 목표와 양극 OCP 표의 유효 범위가 충돌한다 (§4-5 의 조건부)

고체 Li 재고를 보존하고 양쪽 입자를 균일하게 둔 **평형 산술**(극화 없음)에서:

| 양극 조성 | 음극 조성 | 평형 full-cell 전압 |
|---|---:|---:|
| 0.2228930343 — 현재 양극 OCP 표 **하한** | 0.8976699175 | **4.1856 V** |
| 0.215 — §3 의 조성창 하한 | 0.9076429900 | 4.2064 V |
| 0.1989826227 — 선형 **외삽**으로 4.25 V 를 푼 값 | 0.9278814000 | 4.25 V |

양극 half-cell 표의 4.2568 V 를 full-cell 4.25 V 와 직접 비교하면 음극 전위를 빠뜨린다. 그러므로 §4-5 의
`Vmax = 4.25[V]` 는 실험 프로토콜을 옮긴 값이지 **모델이 표 안에서 도달할 수 있다는 뜻이 아니다.** 유한 전류 극화를
계산하지 않았으므로 CC→CV 가 불가능하다고 단정하지도 않는다. 그래서:

- **OCP 범위 중단 조건을 넣는다** — 두 전극이 OCP 표에 실제로 넣는 **표면 조성**(surface SOC; 6.3 의 변수 이름은
  모델에서 확인)을 공간·시간에서 감시하고, 표 범위를 벗어나면 **중단하고 미완으로 기록**한다. 표 경계에서 멈춘
  실행은 적절한 미완이지 실패도 PASS 도 아니다.
- 외삽을 허용하는 실험은 **별도의 명시적 선택**으로 분리한다 (파라미터 이름에 드러낸다).
- 숫자 목표(4.25 V)를 맞추려고 OCP 표를 연장하지 않는다.

### 8-3. 보정 2 — 종료 조건은 phase 별로 (구현 전 확인 항목)

시작 OCV 2.165 V 는 `Vmin = 2.7 V` 보다 낮다. `Vmin` 은 **방전 phase** 에만 걸려야 하고, 첫 충전을 시작부터 막는
전역 종료 조건으로 배선되지 않았는지 CDC 를 만들 때 **먼저** 시험한다 (아직 CDC 가 없으므로 발견된 버그가 아니라
구현 전 확인 항목이다).

### 8-4. 보정 3 — 시간 간격 (§6 의 보완)

- 짧은 검증의 `maxstep = 0.1 s` 를 12 h 휴지에 그대로 쓰면 휴지만 ≥ 432,000 step 이다. **초기 일관성/전이 주변의
  정밀도**와 **장기 adaptive step** 을 구분하고, 허용오차·출력 간격·전이 오차를 명시한다. 출력 `tlist` 와 실제
  solver step 은 다르다.
- **짧은 mesh · 시간간격 비교**로 전압과 전극 표면 조성의 변화를 본다. 보존량(총 Li) 잔차 하나가 작은 것은
  수치 수렴의 증거가 아니다 (8.3e−16 ~ 8.9e−16 의 끝자리 차이는 산술 정밀도이지 물성 정확도가 아니다).

### 8-5. 순서 (검토자의 권장 그대로 채택)

1. 지금 baseline 은 보존한다. 같은 dataset 에서 Eeq_N/Eeq_P 분해 · 표면/평균 조성 · 전극 과전압 · Li 재고 보존
   OCV 곡선을 export 해 §8-1·8-2 의 산술을 **현지에서** 확인한다.
2. OCP 범위 / 농도 / phase 별 cutoff 중단 조건을 정하고 CDC 를 **별도 모델**로 구현한다. 짧은 mesh·시간간격
   비교와 전이 진단을 먼저.
3. 그 결과로 **범위 감시가 있는 `sigma_short = 1e-20` 단일 프로토콜 진단**을 승인할지 정한다.
4. 실험 해석용 본 계산 · 유한 `sigma_short` · sweep(§6-2) 은 원본/실험 OCP 대조와 추가 검증 뒤 별도 결정.

원본 모델과의 동등성(`docs/COMSOL_CHECK_REQUEST.md` 의 `cEeqref` 실효값)과 실험과의 동등성은 이 검증이 말하지 않는다 —
둘 다 열려 있다.

---

## 9. 현지 사전 진단 (preflight) 결과 — 2026-09-13 밤, 전체 운전은 **보류** 유지

> 출처: 사용자 전달 요약 (근거 자료 `COMSOL63_PREFLIGHT_HANDOFF.zip` 의 `PREFLIGHT_RESULTS_KO.md` · 수정된 `NEXT_RUN_PLAN.md`;
> 별도 리뷰가 ZIP 명세 331 파일의 크기·SHA, 이전 5초 보호 자료 64 개의 바이트 보존, 주요 CSV 수치를 대조했다고 함).
> **ZIP 은 이 세션에 첨부되지 않았다** — 아래는 전달된 숫자를 옮긴 것이고, 리뷰 PC 에서 COMSOL 을 재실행한 것도 아니다.
> 이 절은 전체 모델 검증 완료도, 본 실행 GO 도 아니다.

### 9-1. 확인된 것 (단기 구성·수지·전이)

| 항목 | 값 / 결과 | 뜻·경계 |
|---|---|---|
| 실제 초기 Eeq | 양극 **3.578386774 V** · 음극 **1.413053448 V** · 차 **2.165333326 V** | §8-1 의 독립 산술과 일치. 과거 3.0524 V 에 맞추는 보정은 **하지 않았다** (하지 않는다) |
| 표 내부 평형 OCV 상한 | **4.185561543 V** (현 물성 · Li 재고 보존) | §8-2 그대로. 유한전류 극화로 4.25 V 에 닿을 수 있는지는 **별개**이고, 저전류 CV 완료는 **미검증** |
| 경계 진단 | 양극 **평균** 조성은 표 안인데 **표면** 조성이 이탈하는 상태를 실제로 감지 → 계산 중단 → 후처리 오류 | 원래 job 은 `failed`, 과학적 분류는 **`INCOMPLETE_RANGE_STOP`** 으로 보존 — §8-2 의 "표 경계에서 멈추면 적절한 미완" 이 실제로 일어났다. PASS 로 바꾸지 않는다 |
| 2.7 V 방전 cutoff | 첫 충전을 **막지 않음** 확인 | §8-3 의 구현 전 확인 항목 → 닫힘 |
| CC→CV→휴지→방전 전이 | **축소 조건**에서 확인. `eventtol = 1e-6` 에서 2 초 휴지가 2.000002 초 | 전이 배선은 된다. **실제 4.25 V CV · 12 h 휴지 검증이 아니다** |

### 9-2. 미완인 것

| 항목 | 상태 |
|---|---|
| 메시 수렴 | **미완.** 150/20 → 300/40 의 공통 정수초 최대 전압 차 **2.041557 mV** > 기준 1 mV. 5 초 끝점의 0.828913 mV 만으로 통과시키지 않는다 |
| 전해질 양수 검사 | **후처리**다. 실시간 중단 보호까지 구현됐다고 적지 않는다 |
| 저전류 CV 완료 (4.25 V → 0.01C) | 미검증 (9-1 둘째 행) |
| 원본 6.4 모델 · 실험과의 OCP/물성 대조 | 미완 — **재료·초기 상태의 출처 대조**는 별도 미결로 유지 |
| 전체 프로토콜 · 유한 누설(sigma) 검증 · sigma sweep | 미완 |

### 9-3. 다음 진단 (계획 — 아직 결과가 아니다)

같은 촘촘한 초기 시간표에서 **300/40 · 300/80 · 600/40** 의 5 초 비교로 메시 두 축(물리 요소 / 입자 요소)의 영향을 분리한다.
그 결과가 1 mV 기준 안에 들어야 다음(범위 감시 있는 단일 프로토콜, §8-5 ③)을 논한다.

### 9-4. 하지 않는 것 (재확인)

- OCP 표 외삽이나 초기 조성 조정으로 목표 전압(4.25 V)을 맞추지 않는다.
- 표 경계 중단(`INCOMPLETE_RANGE_STOP`)을 완주 PASS 로 바꾸지 않는다.
- 이 절을 근거로 "모델 검증 완료" 나 "본 실행 GO" 를 적지 않는다.

### 9-5. 원문 확보 뒤 보탠 숫자 (`reviews/r14_repros/codex63/preflight/` — `PREFLIGHT_RESULTS_KO.md` · `NEXT_RUN_PLAN.md`)

| 축 | 원문의 값 |
|---|---|
| 실행 | COMSOL 6.3.0.290 · Battery · 2 cores · job 9 개 중 8 개 완료, 표 경계 시험 1 개는 범위 이탈 미완 |
| 초기 전압 분해 (무부하 0 s) | Eeq 양극 3.57838677442 · 음극 1.41305344792 V · 표면 x = 입자 평균 x (양극 0.924063886695 · 음극 0.01172068149) · η ~1e-15 · `Vcell = ΔEeq + Δη_mid + Δφ_l` 이 자리까지 성립 |
| 충전 5 s | ΔEeq 2.28414 · Δη 0.06005 · Δφ_l 0.00334 → Vcell 2.34753 V · 음극 표면 x 0.013609 vs 평균 0.011849 |
| Li 재고 | 고체 1.188225678534278 mol/m² (보존) · 전해질 ≈ 0.0486772853809121 mol/m² |
| 양극 표 하한점 | 양극 Eeq 4.2568201372 · 음극 Eeq 0.0712585940 V → full-cell **4.1855615431 V**, 4.25 V 보다 **64.4385 mV** 낮다 |
| 소비 함수 범위 | Eeq: 음극 [0, 0.98] · 양극 [0.2228930343076256, 1] / dEeq/dT: 음극 [0, 1] · 양극 [0.220410330184718, 0.983245033354389] → 보호 범위 음극 [0, 0.98] · 양극 [0.2228930343076256, 0.983245033354389]. 진단 복제본만 `extrap=none`; 원 표 숫자는 그대로 |
| 범위 이탈 시험 (`PreflightOcpBoundary1s`, 별도 모델) | 양극 초기 x 를 하한 +1e-5 에 두고 0.1C: t=0.00982002 s 표면 min 0.22289304320739442 (안) → t=0.00986002 s 0.22289300332164555 (밖, guard=1), 그때 **평균** x 0.22290283334175 는 안 — 평균만 감시하면 놓친다. 로그 `OCP surface outside table` → `Nonfinite point4` → job failed · `INCOMPLETE_RANGE_STOP` |
| 메시·시간간격 (공통 0–5 정수초, 기준 1 mV · 표면 x 1e-4) | 75/10→150/20: **9.63726094 mV** · 1.58e-4 (둘 다 초과) / 150/20→300/40: **2.04155706 mV** · 3.34e-5 (전압 초과) / 75/10 maxstep .1→.05 s: 0.00321431735 mV · 5.26e-8 (이내). 저장격자 합집합 보간에서는 t≈0.15749 s 에 5.070573 mV — 정수초 비교가 초기 피크를 놓친다 → 다음 비교는 초기 1 초 안 촘촘한 공통 시점 포함 |
| CDC 시작 | `PreflightCdcStart5s`: 실제 목표(4.25 V / 0.01C / 12 h / 2.7 V) 설정, 5 초만. 시작 V 2.230611555 V < 2.7 V 에서 CC_CH=1, I=+2.503599529 A 로 충전 유지 — 전역 저전압 stop 없음 |
| 축소 전이 시험 (Vmax 2.24 · Vmin 2.10 · CV cutoff 0.08C · 휴지 2 s) | eventtol .01 → 1e-6: CC→CV 0.18536→0.18457 s · CV→휴지 0.46116→0.45740 · 휴지→방전 2.48116→2.45741 · 사이클 완료 2.65428→2.62421 s; 휴지 2.02 → 2.000002 s; cutoff 오차 0.3243 mV → 9.77e-5 mV |
| 다음 단일 진단의 강제 중단 (NEXT_RUN_PLAN §3) | 표면 cs/csmax 의 전극별 공간 min/max (accepted step 뒤 검사, Lagrange 5차 표본) · 고체 0–cmax · 전해질 양수 · 유한값 · Li·전류 수지는 별도 물리 판정 · 목표 미도달은 시간 완료로 PASS 하지 않음 |
| 장기 시간 설계 (NEXT_RUN_PLAN §4, **미검증 후보**) | rtol 1e-6 · BDF · 최초 step 1e-5 s · eventtol 1e-6 · 전이 주변 .05–.1 s · CC/CV 10 s 상한 adaptive · 휴지 1 → 60 → 600 s 상한 · 보고 출력 분리(CC/CV 10 s, 휴지 60–600 s) · 12 h 에 maxstep .1 s 재사용 금지 · 전이 오차 목표: cutoff 1 mV · CV 전류 0.1 % · 휴지 1 s |

`NEXT_RUN_PLAN.md` §2 의 단일 진단 범위(sigma 1e-20 · +0.1C → 4.25 V CV → 0.01C → 12 h 휴지 → −0.1C → 2.7 V · Charge_first ·
ExplicitValue · A_c 1 m² · boundary4 는 CDC 만 · cycle_counter 0→1 에서 종료 · 초기 농도·Li 재고·298.15 K·NMC cmax 50707.7 보존)
는 **사용자가 선택할 때만** 새 source SHA 로 1 회 제출한다 — 이 명세는 그것을 승인하지 않는다.
