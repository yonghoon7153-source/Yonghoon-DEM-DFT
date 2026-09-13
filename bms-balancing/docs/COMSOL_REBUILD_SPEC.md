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
