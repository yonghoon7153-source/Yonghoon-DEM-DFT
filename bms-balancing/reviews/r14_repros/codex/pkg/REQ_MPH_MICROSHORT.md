# 적대적 리뷰 요청 — 마이크로 쇼츠 COMSOL 모델 구조 분석 (하네스 라운드와 별건)

대상은 `bms-balancing/docs/MICROSHORT_MPH_REVIEW.md` 의 **주장**이다. 코드가 아니라 **분석**을 턴다.
물음 하나: **COMSOL 을 돌리지 않고 `dmodel.xml` 만으로 낸 "M1 은 버그다" 가 성립하는가.**

M1 이 반증되면 문서의 §0·§3-M1·§4-1·§5-3 이 통째로 무너진다. **그것을 최우선으로 시도해 주기 바란다.**

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | 이 파일이 든 커밋 (`git log -1`). 분석 문서는 `26c477c` 에서 들어왔다 |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 만 |
| 리뷰 대상 문서 | `bms-balancing/docs/MICROSHORT_MPH_REVIEW.md` (574 행) |
| 저장소에 **없는** 것 | `ICA_degradation mode.mph` (47 MB) · `result_L_{ref1,ref2,PE1,PE5}__0.1C_12h__charge.xlsx`. 공개 저장소라 커밋 안 한다 |
| 원본 소유 | 규진팀. COMSOL 6.4.0.293 · BATTERYDESIGN · 최종 계산 2026-09-12 22:27 UTC (8.314 s) |
| 이 분석이 한 것 | `.mph`(=ZIP) 를 풀어 `dmodel.xml`(2.6 MB) 의 노드·파라미터·보간표를 읽고 산술 |
| 이 분석이 **안** 한 것 | **COMSOL 실행 0회.** 모든 수치는 XML 의 식 + 내장 OCP 표에서 직접 계산 |

## 1. 핵심 주장 (M1) — 이것만 깨면 된다

### 1-1. 실측한 XML 값 (재현 명령은 §5)

```
전역 파라미터 (<expressions T="31">):
  epss_el   = epss_el_0*(1-LAM_NE)          epss_pos  = epss_pos_0*(1-LAM_PE)
  epss_Gr   = epss_el*(1-Si_f)              Si_f      = 0   (Si_m_f = 0)
  dm_fNE    = 0.97427802                    dm_fPE    = 0.97036018
  LAM_NE    = 0.0257219788                  LAM_PE    = 0.0296398242
  x_Gr_init = x_Gr_0 = 0.01172068149
  x_NCM_init = (nLi_target - epss_el*L_el*cs_Gr_max*x_Gr_init)/(epss_pos*L_pos*cs_NCM_max)
  nLi_0     = epss_pos_0*L_pos*cs_NCM_max*x_NCM_0 + epss_el_0*L_el*cs_Gr_max*x_Gr_0
  nLi_target= nLi_0 - dLi_LLI               dLi_LLI = C_lit0_ref1*LLI/F_const/A_cell
  cs_NCM_init = x_NCM_init*cs_NCM_max*dm_fPE          ← 정의만 되고 소비자 0
  cs_Gr_max = 31507 mol/m^3                 cs_NCM_max = 50707.7 mol/m^3
  L_el = 52 um · L_sep = 25 um · L_pos = 44 um · eps_binder_el = 0.1
  epss_el_0 = 0.63122 · epss_pos_0 = 0.58803 · x_NCM_0 = 0.927 · b_PE = 2.2

물리 노드 (<param T="33">, PhysicsFeature 안):
  pce1 (PorousElectrode, 도메인 1, 활성)   epss = epss_Gr
    └ pin1  cEeqref = cs_Gr_max*dm_fNE     csinit = x_Gr_init*cs_Gr_max
  pce2 (PorousElectrode, 도메인 3, 활성)   epss = epss_pos
    └ pin1  cEeqref = cs_NCM_max*dm_fPE    csinit = x_NCM_init*cs_NCM_max
  pcb1 (PorousConductiveBinder, 도메인 2, 활성)
            sigma = sigma_short (등방 3x3)  epsl = epsl_sep   epss = epsl_sep
            ElectricCorrModel = Bruggeman
```

`1-LAM_NE = 0.9742780212` vs `dm_fNE = 0.97427802` (차 1.2e-9) · `1-LAM_PE = 0.9703601758` vs
`dm_fPE = 0.97036018` (차 −4.2e-9) → `dm_f*` 는 `1-LAM_*` 를 손계산해 잘라 넣은 값.

### 1-2. 주장 사슬

| # | 주장 | 근거 | 깨는 법 |
|---|---|---|---|
| A1 | COMSOL Particle Intercalation 의 `cEeqref` 는 `Eeq(soc)` 의 `soc = cs/cEeqref` 분모다 | COMSOL 6.4 Battery Design Module 문서 · GUI 필드명 "Maximum concentration" | **`cEeqref` 가 SOC 분모가 아니거나 `Eeq` 가 `cs` 를 직접 받으면 A1 부터 무너진다** |
| A2 | 따라서 `soc(t=0) = csinit/cEeqref = x_init/dm_f` | A1 + §1-1 실측값 | 산술 |
| A3 | LAM 이 `epss`(부피분율)와 `cEeqref`(사이트밀도) 양쪽에 걸려 호스트 사이트 수가 `(1-LAM)²` | `epss_el` 정의 + `cEeqref` 정의 | **`cEeqref` 가 사이트 수 총량과 무관하면 A3 만 무너지고 A2 는 남는다** |
| A4 | `csinit` 에 `dm_f` 가 없는 것은 의도가 아니라 누락 | `cs_NCM_init` 이 `dm_fPE` 를 포함한 채 정의돼 있는데 **어느 노드도 참조하지 않는다** (문자열 `cs_NCM_init` 14회, 전부 정의/액션로그/미사용) | **의도된 "사이트는 줄되 초기 리튬은 안 준다" 모델이라는 반론이 가능하다 — 그러면 M1 은 버그가 아니라 미문서화 설계다** |
| A5 | Li 총량은 맞다 (`nLi_0`·`x_NCM_init`·`csinit` 이 전부 맨 `cs_*_max`) | §1-1 | 산술 |

### 1-3. 수치 — 리뷰어가 손으로 검산할 수 있게 괄호점을 붙였다

내장 OCP 보간표(선형)에서:

```
음극 mat1 (Graphite LixC6 MCMB, 88점):
  soc 0.01172068  괄호 (0.008183898, 0.56533) — (0.016367829, 0.445258)  → 0.513439 V
  soc 0.01203012  같은 구간                                              → 0.508899 V   차 -4.54 mV

양극 mat5 (NMC 811, 100점):
  soc 0.92406389  괄호 (0.916363636, 3.57093827) — (0.924545455, 3.56548357) → 3.565805 V
  soc 0.95228958  괄호 (0.949090909, 3.54922689) — (0.957272727, 3.54350457) → 3.546990 V  차 -18.81 mV

E_cell(t=0):  의도 3.05237 V   as-built 3.03809 V   차 -14.27 mV
x_NCM_init = 0.924064  (Li 수지에서, §1-1 식으로 계산)
실효 LAM:  NE 2.5722 % -> 5.0782 %   PE 2.9640 % -> 5.8401 %   (1-(1-LAM)^2)
```

**이 산술이 틀렸으면 지적해 달라.** 특히 `x_NCM_init = 0.924064` 는 우리가 Li 수지식을 손으로 푼 값이고
COMSOL 이 실제로 그 값을 쓰는지는 **확인하지 못했다** (COMSOL 미실행).

## 2. 나머지 주장 — 심각도 순, 각각 독립으로 깨도 된다

| ID | 주장 | 실측 근거 | 우리가 약하다고 보는 곳 |
|---|---|---|---|
| M2 | `pcb1.epss = epsl_sep`(0.45)은 복붙. `ElectricCorrModel = Bruggeman` 이라 실효 σ = `0.45^1.5 * sigma_short = 0.302*sigma_short` → sweep 값이 3.3배 과대표기. `epss`×`sigma_short` 가 곱으로만 들어가 **서로 축퇴** | XML 값 직접 인용 | **Bruggeman 이 `PorousConductiveBinder` 의 고체 전도도에 실제로 걸리는지 확인 못 했다** (GUI `liion.pcb1.sigmaeff` 미확인). 안 걸리면 3.3배 주장만 무너지고 축퇴 주장은 남는다 |
| M3 | OCP 가 COMSOL 내장 라이브러리 곡선(`Graphite, LixC6 MCMB` 88점 / `NMC 811` 100점)인데 열화모드 값을 만든 α·β 적합은 **자체 반쪽셀 곡선** 위에서 돌았다 → α 는 기준 곡선과 분리 불가능한 양이라 이식 불가 | 재료 이름이 라이브러리 이름 · 보간함수명이 `Eeq_int1`/`dEeqdT_int1`/`dVOLdSOL`(라이브러리 기본) · `Q_el = 25.036 Ah/m²` 가 `epss_pos_0*L_pos*cs_NCM_max*(x_NCM_max-x_NCM_min)*F/3600` 과 **정확히 일치** | **보간표가 라이브러리 원본인지 그 위에 덮어쓴 것인지 대조 못 했다** (COMSOL 라이브러리 원본 미보유). 이름만으로 판단했다 |
| M4 | `dPE`·`dNE` 는 죽은 파라미터 (소비자 0) | `dPE` 4회 · `dNE` 3회 등장, 전부 정의 + 액션로그 | 액션로그가 과거 이력인지 활성 설정인지 오독 가능성 |
| M5 | Events(`ev`)가 무력: 두 지시자(`switch`/`end`)가 **같은 문턱** `E_switch` 를 쓰고, `E_end` 소비자 0, `impl2` 는 reInit 없음, 활성 Stop Condition 없음 | `is1.g = ['-(E_cell-E_switch)', 'E_cell-E_switch']` · `impl2.reInitName = 0` · `stopcondarr` 비어 있음 | **Stop Condition 판단이 XML 추론이다.** GUI 확인 안 함 |
| M6 | `ge2` 가 full-cell 전압에서 반쪽셀 전위 `E_max_el`(0.502 V)을 뺀다 → 에너지 값 무의미 | `d(E_lith,t) = if(CurrentDirection==-1, i_app*(E_cell-E_max_el), 0)` | 없음 (식 그대로) |
| M7 | 충전 중 `SOC` 음수 | `d(Cap,t) + liion.cdc1.Icell/1[m^2] = 0`, 충전 시 `Icell > 0` | `Icell` 부호 규약을 COMSOL 문서로 확인 안 함 |
| M8 | 저장된 해는 `C_rate=0.05`(4개 sigma_short), 현재 파라미터는 `C_rate=0.1`, sweep 노드 **비활성** | `SolverSequence` 이름 · `paramVals` · `<entityFlags>DISABLED` | 없음 |

## 3. 파라미터 출처 사슬 (별건 리뷰 `REQ_FIT_RAILS.md` 와 겹침)

`.mph` 값 ← `result_L_ref1__0.1C_12h__charge.xlsx` **cycle 2** 한 줄. 네 파일 37행 전수 대조.

| `.mph` | 출처 |
|---|---|
| `LAM_PE` · `LAM_NE` · `LLI` | ref1 cycle 2 |
| `C_lit0_ref1` | ref1 cycle 0 의 `c_lit` |
| `dNE` | ref1 cycle 0 의 `b_NE` |
| `dPE` | **네 파일 어디에도 없음 — 출처 불명** |

## 4. 닫지 않은 것 / 우리가 못 한 것

1. **COMSOL 미실행.** −14.27 mV 는 t=0 OCP 차이이지 해(solution) 비교가 아니다. 실제 궤적 차이는
   확산·과전압이 섞이므로 돌려 봐야 안다. **"−14 mV 만큼 곡선이 밀린다" 고는 주장하지 않았다.**
2. M2 의 Bruggeman, M5 의 Stop Condition 은 XML 추론이다 (GUI 확인 필요).
3. `dPE` 출처 미상.
4. 실험 전압 곡선 자체를 못 봤다 — 받은 xlsx 는 적합 **결과**만 담고 원 곡선이 없다. M3 를 그림으로
   확정하려면 원 곡선이 필요하다.
5. OCP 보간표를 COMSOL 라이브러리 원본과 대조 못 했다 (M3 의 약한 고리).

## 5. 재현 — COMSOL 없이 된다

```bash
unzip -o "ICA_degradation mode.mph" -d mph/ && cd mph/
```

```python
import re
s = open('dmodel.xml', encoding='utf-8', errors='replace').read()

# 전역 파라미터 93개
for m in re.finditer(r'<expressions T="31" name="([^"]*)" expr="([^"]*)"', s):
    print(m.group(1), '=', m.group(2))

# 물리 노드의 실제 값 + 활성 여부  ← M1 은 여기서 눈으로 보인다
for m in re.finditer(r'<PhysicsFeature op="([^"]+)" tag="([^"]+)" name="([^"]*)"', s):
    blk = s[m.start():s.find('</PhysicsFeature>', m.start())]
    flag = re.search(r'<entityFlags T="51">([^<]*)</entityFlags>', blk)
    print(m.group(2), m.group(1), 'DISABLED' if flag and 'DISABLED' in flag.group(1) else 'active')
    for p in re.finditer(r'<param T="33" param="(csinit|cEeqref|epss|epsl|sigma|rp|Ds)" value="([^"]*)"', blk):
        print('   ', p.group(1), '=', p.group(2))

# OCP 보간표
for tag in ('mat1', 'mat5'):
    m = re.search(r'<Material op="[^"]*" tag="%s"' % tag, s)
    blk = s[m.start():s.find('</Material>', m.start())]
    i = blk.find('Eeq_int1')
    p = re.search(r'"((?:[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?[,\s|\']{1,4}){15,})"', blk[max(0,i-500):i+9000])
    print(tag, re.findall(r"'([^']*)','([^']*)'", p.group(1))[:3], '...')
```

**우리가 실행해 확인했다** (2026-09-13): 위 세 블록 전부 동작, 출력이 §1-1 과 일치.

## 6. 리뷰어에게 묻는 것

| Q | 내용 |
|---|---|
| Q1 | A1(=`cEeqref` 가 SOC 분모) 이 COMSOL 6.4 에서 맞는가. **틀리면 M1 이 통째로 무너진다** |
| Q2 | A4 의 반론 — "사이트는 줄되 초기 리튬은 안 준다" 가 의도된 설계일 수 있는가. 그렇다면 §4-1 수정안(=`cEeqref` 를 맨 `cs_max` 로)이 **오히려 모델을 바꾸는** 것이 된다 |
| Q3 | §4-1 (LAM 을 `epss` 에만) 대 대안 (LAM 을 `cEeqref` 에만) — DFN 관례상 어느 쪽이 LAM 인가. 우리는 전자를 골랐고 근거는 "LAM 은 입자 수 감소이지 격자 수축이 아니다" 하나뿐이다 |
| Q4 | M2 의 Bruggeman 3.3배가 맞는가 (`PorousConductiveBinder` 의 `ElectricCorrModel` 적용 대상) |
| Q5 | §5 의 방향 제안 — "LLI/LAM 은 휴지 전압 감쇠에 레버리지가 없으므로 12 h 휴지 기울기가 쇼츠 전용 신호축" 이 성립하는가. **반례: LAM 이 확산·과전압을 바꿔 휴지 완화 시상수를 바꾸면 초반 기울기는 오염된다.** 우리는 "확산 완화가 끝난 뒤 마지막 6~8 h" 로 피하려 했는데 그 회피가 충분한가 |
| Q6 | 놓친 노드가 있는가. 특히 `socicd1`(SOC and Initial Charge Distribution, 비활성)이 활성이었다면 초기 조건을 덮어썼을 텐데, 비활성 확인만 하고 그 이상 안 팠다 |
