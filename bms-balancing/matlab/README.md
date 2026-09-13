# MATLAB 쪽에서 돌릴 것 — 명령어

이 파일들을 **규진팀 프로젝트 루트**(`electrode_balancing_blend.m` 이 있는
폴더)에 복사해 두고 돌린다. 기존 함수를 고치지 않고 그대로 호출하므로,
여기서 나오는 값은 **그들 파이프라인의 값**이다.

```
degradation mode/                ← 여기가 루트 (여기서 실행)
├── electrode_balancing_blend.m
├── electrode_ocv.m
├── build_blend_functions.m
├── differential.m
├── extractMyData.m
├── averageDuplicates.m
├── dd_verify.m                  ← 복사
├── dd_eval.m                    ← 복사
├── fit_cycles_driver.m          ← 복사 (사이클별 재적합 드라이버 — BML_R1_RESPONSE §10, MATLAB+GADS 필요)
├── dd_shims/                    ← 폴더째 복사 (sgolayfilt.m · quantile.m · findpeaks.m)
└── data/
    ├── half_cell/{GITT,step_005C}/
    ├── full_cell/large_cell_033C/
    └── literature/{Si_Gr_literature_OCP.xlsx, Si_OCP_sources/*.csv}
```

`main_blend_final.m` 첫머리의 `cd('C:\Users\ga117\...')` 는 **지우거나 주석
처리**해야 한다 (수정 제안 #7). `dd_verify.m`·`dd_eval.m` 은 `cd` 를 안 한다 —
현재 폴더 기준 상대경로만 쓴다.

---

## 먼저: 이 기계의 툴박스 상태 — **라이선스는 있고 설치가 안 돼 있다**

사용자 기계(R2026a, Windows) 실측 (2026-09-10).

| 함수 | 어느 툴박스 | 설치 | 라이선스 |
|---|---|---|---|
| `fmincon` | Optimization | ✗ | **있음** |
| `MultiStart` · `createOptimProblem` | Global Optimization | ✗ | **있음** |
| `sgolayfilt` · `findpeaks` | Signal Processing | ✗ | **있음** |
| `quantile` | Statistics and Machine Learning | ✓ | 있음 |

두 가지를 정정한다.

1. 전 판은 "툴박스가 하나도 없다" 고 적었는데 **틀렸다** — `quantile` 은
   실제로 있다. `dd_verify('check')` 에서 `sgolayfilt` 는 FAIL 인데
   `quantile` 은 통과했고, 그때 `dd_shims` 는 경로에 없었다.
2. 나머지 셋도 **살 필요가 없다.** `license('test', ...)` 가 `Optim_Toolbox`·
   `GADS_Toolbox`·`Signal_Toolbox`·`Statistics_Toolbox` 넷 다 `1` 을 돌려줬다.
   즉 자격은 이미 있고 **설치만 안 된 상태**다. MATLAB 홈 탭 → 애드온 →
   애드온 탐색기에서 설치하면 된다 (제품 페이지의 "무료로 사용해 보기" 는
   라이선스가 **없는** 사람용 평가판이므로 누르지 말 것 — 별도 평가판
   라이선스가 붙어 30일 뒤 끊긴다).

**즉 설치 전까지는 `main_blend_final.m` 자체가 이 기계에서 안 돈다.** 그래서
길을 둘로 나눠 두었다. 설치가 끝나면 `-end` 규약 덕분에 아래 대체품은
자동으로 물러나고 진짜 함수가 이긴다 — 그때가 **MathWorks 구현과 우리 정의의
차이를 처음 재는 순간**이다 (같은 명령을 다시 돌려 CSV 두 개를 비교하면 된다).

- `dd_shims/` — `sgolayfilt` · `quantile` · `findpeaks` 를 기본 MATLAB 만으로
  다시 쓴 것.
  그들 코드를 **한 줄도 안 고치고** 돌리려는 것이다 (MATLAB 이 경로를 먼저
  보므로 그들 `differential.m` 이 이 파일을 부른다).
  ⚠ MathWorks 구현이 아니다. 그래서 조용히 켜지지 않게 `addpath` 로 **명시적
  으로** 올려야 하고, 반드시 **`'-end'`** 를 붙인다:

  ```matlab
  addpath('dd_shims','-end')   % ← '-end' 없으면 있는 툴박스 함수까지 가린다
  ```

  `addpath('dd_shims')` 는 경로 **앞**에 붙어서 이 기계에 실제로 있는
  `quantile` 까지 우리 대체품으로 가려 버린다. `'-end'` 면 MATLAB 것이 이기고
  **없는 것만** 메워진다. `dd_eval` 은 어느 쪽이 잡혔는지 화면과 CSV 앞머리
  (`# impl_sgolayfilt,...` · `# impl_quantile,...` · `# impl_findpeaks,...`)에
  기록한다.
- `dd_eval.m` — **적합 없이** 주어진 파라미터에서 목적함수만 찍는다.
  포팅 대조에 정말 필요한 건 최적화기가 아니라 **모델**이기 때문이다:
  같은 p 에서 MATLAB 과 Python 이 같은 RMSE 를 내는지가 핵심이고,
  그건 `fmincon` 없이 잴 수 있다.

### `findpeaks` 대체품 (2026-09-10 추가)

`w_dqdv = 0`(그들 기본 설정)에서는 dQ/dV 항이 목적함수에 안 들어가지만, 항
자체는 계산할 수 있어야 대조가 끝난다. 그래서 `dd_shims/findpeaks.m` 을 썼다.

- 지원 범위는 그들이 쓰는 형태 하나뿐: `findpeaks(x,'MinPeakProminence',t)`.
  다른 옵션은 **조용히 무시하지 않고 에러를 낸다** (무시하면 다른 답이 나온다).
- 검증: 8 벡터 × prominence 5 종 = **40/40 조합이 scipy `find_peaks` 와 일치**.
- ⚠ Octave core 에도 `findpeaks` 가 없다. 그래서 이 함수만은 3자 대조가 안 되고
  **shim ↔ scipy 2자** 대조다 — 제3의 독립 구현으로 확인한 것이 아니다.
- ⚠ **평탄 꼭대기(plateau)** 규약이 MathWorks 와 다를 수 있다. 우리는 scipy 처럼
  가운데 인덱스를 봉우리로 잡는다 (우리 포팅이 scipy 를 쓰기 때문). MathWorks
  구현은 평탄 꼭대기를 봉우리로 안 볼 수 있다. 툴박스를 설치한 뒤 같은
  `dd_eval` 을 다시 돌려 `n_peaks` 앵커를 비교하면 그 차이가 바로 보인다.

---

## 0. `check` — 몇 초, 제일 먼저

경로·툴박스·데이터·배관을 한 번에 확인한다. **첫 실패에서 멈추지 않고 전부
세서** 요약을 낸다.

```matlab
cd 'D:\가형 관련\degradation mode'
dd_verify('check')
```

> 이건 사용자 기계에서 이미 정상 실행됐다 (2026-09-10).

찍히는 것: 그들 함수 6개가 경로에 있는가 · 툴박스 함수 5종이 있는가 ·
반쪽전지 상태 파일 개수 · 풀셀 워크북의 상태별 `c_cell` 5개 · 문헌 Si 8종 ·
그리고 실제로 한 번 읽어 `E_PE(0.5) − E_NE(0.5, γ=0.25)` 를 계산한 값.

마지막 값이 **2.5~4.5 V 밖이면** 방향 규약(어느 쪽이 lithiation 인가)이
우리 가정과 다른 것이므로 그 자리부터 봐야 한다.

`c_cell` 다섯 개가 이 값과 다르면 워크북이 우리가 본 것과 다른 판이다:

    pristine 74.671 · 100 71.631 · 200 69.571 · 300_0009 63.720 · 300_0147 67.369

---

## 1. 포팅 대조 — **지금 할 것** (툴박스 불필요)

```matlab
cd 'D:\가형 관련\degradation mode'
addpath('dd_shims','-end')   % ← '-end' 로. 없으면 진짜 quantile 까지 가린다
dd_eval('State','pristine','SiSource','Li','Out','dd_eval_pristine_Li.csv')
```

수십 초 안에 끝난다 (적합을 안 하므로). 나오는 CSV 는 이렇게 생겼다:

```
# dd_eval  state=pristine  halfcell=data/half_cell/GITT/  Si=Li  w_dqdv=0
# c_cell,74.670999999999999
# dv_lo,0.149298597...
  … 앵커 16개 …
a_PE,b_PE,a_NE,b_NE,gamma_Si,rmse_pocv,rmse_dvdq,rmse_dqdv,rmse_dqdv_w
1.077218,-0.022949,1.001342,0.000309,0.295099,…,…,…,…
  … 8행 …
```

앞머리 `#` 열여섯 개가 **이분(bisection) 앵커**다. 갈렸을 때 어느 단계가
범인인지 좁히는 값들이라 화면뿐 아니라 CSV 에도 같이 적는다 — 화면에만 찍으면
CSV 만 보내 왔을 때 이분할 근거가 사라진다.

| 앵커 | 무엇이 갈렸다는 뜻인가 |
|---|---|
| `c_cell` | 풀셀 적재 · `averageDuplicates` · 방향 정규화 |
| `dv_lo`·`dv_hi`·`dv_n` | 풀셀 `differential` + `quantile(0.15/0.85)` |
| `dq_lo`·`dq_hi`·`dq_n` | 풀셀 `differential` + `quantile(0.05/0.95)` |
| `n_peaks` | `findpeaks` — 평탄 꼭대기 규약이 갈리면 여기서 보인다 |
| `w_peak_sum`·`w_peak_max` | 피크 가중 (`peak_weight` 7 · `sigma_ratio` 0.03) |
| `dq_nuniq_p1` | 첫 행 p 에서 `unique(v_smooth)` 뒤 남은 점 — 모델 전압이 |
|  | 단조가 아니면 원본이 점을 **조용히 버린다** |
| `dq_nin_p1` | 첫 행 p 에서 보간 범위에 든 실측 점 — 5 미만이면 원본이 1e6 |
| `E_PE(0.5)`·`E_NE(0.5,0.25)` | 반쪽전지·문헌 적재와 블렌드 |
| `dv_PE(0.5)`·`dv_NE(0.5,0.25)` | 각각의 `differential` |

⚠ 뒤 두 열(`rmse_dqdv`·`rmse_dqdv_w`)만은 성격이 다르다. 그들
`compute_dqdv_rmse_blend`·`build_peak_weights_local` 은
`electrode_balancing_blend.m` 안의 **로컬 함수**라 밖에서 부를 수 없어서
**옮겨 적었다**. 앞 두 열은 그들 함수를 그대로 호출하지만 이 두 열은 아니다.
그래서 이 두 열의 일치는 「그들 코드 ↔ 우리 포팅」이 아니라 「우리 전사 ↔
우리 포팅」이다 — **규진팀이 그 두 함수를 눈으로 대조해 주면** 그때 메워진다.

**그 CSV 파일 하나만 보내면 된다.** 이쪽에서:

```bash
export BMS_DATA_ROOT=/…/electrode_balancing_blend
python -m bms_balancing.verify eval --state pristine --si-source Li \
       --compare dd_eval_pristine_Li.csv
```

앵커 16개 + rmse 32개(8행 × 4열)를 대조하고, **갈린 첫 앵커의 단계 이름**을
말한다. process 종료 코드가 판정이다 — 0 complete · 1 갈림(앵커/목적함수) · 2 미완
(행 누락·격자 불일치·NaN) · 3 부분(옛 스키마: 앵커·열 누락; `--allow-partial` 을 주면
0). CSV 의 정밀도는 **옵션 → 선언 → 추정** 순이다: `--precision g17|fixed:N|sig:N` 이
있으면 그것, 없으면 `dd_eval.m` 이 적는 `# printed_format,%.17g` 선언, 둘 다 없으면 값의
자리수에서 추정한다. 추정은 탐색이라 결과가 맞아도 complete 가 아니라 partial(종료 3)이고
`--allow-partial` 로도 0 이 되지 않는다 — 선언이 없는 옛 파일은 형식을 알면 `--precision`
으로 명시할 것. 반올림 구간은 토큰의 반 단위(`%.10f` 면 5e-11)이고 그 초과분만 수치 차이로
센다 — `%g` 는 대칭 반 단위가 아니라 **같은 형식으로 실제로 찍은 문자열**로 구간을 정한다 (R5-01).
옵션이 선언보다 느슨하면 partial, 해석 못 하는 선언(옵션으로 대체 가능)·두 번째 선언·같은 이름의
열·앵커·숫자 아닌 앵커·이름/순서가 다른 파라미터 열은 invalid (Codex R3-05~07 · R4-02~04 · R5-01~03).
(예: "`E_NE_0p5_0p25` 에서 처음 갈린다 → 범인 단계는 「문헌 적재 +
build_blend_functions」"). 그 앞 앵커가 맞았으면 그 앞 단계는 용의선상에서 빠진다.

조건을 바꿔 몇 개 더 뽑으면 대조가 튼튼해진다:

```matlab
dd_eval('State','300_0009','SiSource','Li',  'Out','dd_eval_300_Li.csv')
dd_eval('State','pristine', 'SiSource','Kunz','Out','dd_eval_pristine_Kunz.csv')
dd_eval('HalfCellDir','data/half_cell/step_005C/','State','pristine', ...
        'SiSource','Li','Out','dd_eval_pristine_Li_005c.csv')
```

임의의 파라미터를 직접 넣어 볼 수도 있다:

```matlab
dd_eval('P', [1.10 -0.05 1.10 -0.01 0.15; 1.10 -0.05 1.10 -0.01 0.30])
```

**툴박스를 설치한 뒤에는 같은 명령을 한 번 더** 돌려서 다른 이름으로 저장해
달라 — 앞머리의 `# impl_sgolayfilt` 가 `dd_shims` 에서 `matlab` 으로 바뀌고,
두 CSV 를 비교하면 **MathWorks 구현과 우리 정의의 차이**가 측정된다.

2026-09-10 에 이 대조를 했다 (`FINDINGS.md` §1-7). `quantile` 과 `findpeaks`
는 **완전히 같고**(각각 16 값 · 12 값), `sgolayfilt` 는 도함수에서 상대
1.33e-13 갈린다. rmse 128 값에서는 `rmse_pocv` 가 32/32 완전 동일,
`rmse_dvdq` 2.80e-14, `rmse_dqdv` **1.78e-12** — dQ/dV 항이 같은 평활 차이를
64 배 증폭한다 (평활된 전압의 도함수로 나누기 때문).

```matlab
dd_eval('State','pristine','SiSource','Li','Out','dd_eval_pristine_Li_TB.csv')
```

---

## 2~4. 적합이 필요한 것들 — **툴박스가 생기면**

아래는 `fmincon` + `MultiStart` 가 있어야 돈다. 지금 기계에서는 그 자리에서
에러가 난다 (조용히 다른 답을 내지는 않는다).

### 2. `dump` — Si 소스 8종 전수 재적합

```matlab
dd_verify('dump', 'State','300_0009', 'WDqdv',0, 'Out','dd_dump_gitt_w0.csv')
```

우리 Python 이 같은 조건에서 낸 값 (**정본: `out/matrix_300_0009.csv`** — U14 재실행이 옛 `_v2` 를 비트 단위로 재현한 것):

| Si 소스 | LAM_PE % | LAM_NE % | LLI % | 대상 경계 | **기준 경계** |
|---|---|---|---|---|---|
| Baggetto | 7.02 | 14.67 | 16.09 | a_NE=lb, γ=lb | b_PE=ub, a_NE=lb, γ=lb |
| Friedrich | 9.32 | 14.67 | 16.50 | a_NE=lb, γ=lb | b_PE=ub, a_NE=lb, γ=lb |
| Jiang | 6.77 | 5.79 | 15.75 | — | — |
| Kunz | 7.19 | 6.36 | 15.81 | — | — |
| Li | 6.36 | 7.90 | 15.70 | — | — |
| Lu | 6.61 | 8.23 | 15.63 | — | a_NE=lb |
| Sethuraman | 5.65 | 7.84 | 15.47 | — | b_PE=ub |
| Wetjen | 7.43 | 16.67 | 15.63 | — | b_PE=ub, a_NE=ub |

> **2026-09-10: 이 대조는 끝났다** (`FINDINGS.md` §1-9). 양쪽 다 경계에 안 붙은
> 세 조합(Jiang·Kunz·Li)의 최대 차이가 **0.1663 %p** 로 판정선 1 %p 안이다.
> 가장 큰 차이 둘(Baggetto·Friedrich 의 LAM_PE +0.65/+0.48 %p)은 기준이 세
> 좌표나 경계에 눌린 조합이었다 — §4-2 가 예측한 그대로다.

**차이가 1 %p 안쪽이면** 포팅이 맞다고 본다 — 단 **경계 열이 비어 있는 행만**
그렇게 볼 수 있다. 경계에 붙은 행의 좌표는 데이터가 아니라 상자가 정한 값이라,
두 구현이 같은 상자를 쓰면 그 자리는 자동으로 같아지고 다르면 크게 다르다.
위 8 행 중 **기준이 자유로운 것은 Jiang·Kunz·Li 셋뿐**이다 (§4-2).

> ⚠ 이 표는 `multistart` 수정 **뒤**(v2) 값이다. 그 전 판(v1)과 LAM_NE 가
> 최대 1.6 %p 다르다 (Wetjen 15.04 → 16.67, Jiang 6.11 → 5.79). v1 표를
> 들고 대조하면 없는 불일치가 나온다.

### 3. `profile` — γ_Si 프로파일 (결정론적 민감도 곡선 — 오차막대가 **아니다**, FINDINGS §0-2)

```matlab
dd_verify('profile', 'State','300_0009', 'SiSource','Li', 'WDqdv',0, ...
          'Gammas',0:0.025:0.5, 'Out','dd_profile_Li.csv')
```

우리 Python 이 낸 값 (같은 조건):

| γ_Si | pOCV RMSE | a_NE | LAM_NE | LLI |
|---|---|---|---|---|
| 0.050 | 9.47 mV | 1.209 | **−3.00 %** | 16.33 % |
| 0.150 | **5.59 mV** | 1.146 | 2.33 % | 15.91 % |
| 0.250 | 8.00 mV | 1.073 | 8.58 % | 15.70 % |
| 0.325 | 11.00 mV | 1.021 | **13.00 %** | 15.29 % |

**보아야 할 것**: `a_NE` 가 γ 와 반대로 움직이는가, 그리고 RMSE 12 mV
(원전 Schmitt 2022 가 "좋은 재구성"이라 부른 문턱) 안에서 LAM_NE 가 몇 %p 를
훑는가.

> **2026-09-10: 돌렸다** (§1-9). 21 점 중 18 점이 0.03 %p 안에서 일치하고,
> 갈린 두 점(γ=0.150 · 0.450)에서는 **MATLAB 쪽이 더 좋은 해**를 찾았다 —
> 특히 γ=0.450 에서 pOCV RMSE 17.5 vs 우리 40.6 mV 로 **우리가 골짜기를
> 놓쳤다.** 우리 1 % 띠에 든 두 행(γ=0.225·0.250)은 0.003 %p 안에서 같으므로
> §3 결론은 안 흔들린다.

### 4. `scalenoise` — 목적함수의 난수 의존 (수정 제안 #4 를 눈으로)

```matlab
dd_verify('scalenoise', 'State','300_0009', 'Out','dd_scalenoise.csv')
```

`electrode_balancing_blend.m` 은 목적함수 scale 을 `rand` 50개로 잡는데
**seed 가 없다.** 결과가 seed 마다 다르면 "같은 데이터·같은 설정으로 두 번
돌리면 답이 다르다" 가 실물로 확인된다.

> **2026-09-10: 확인됐다** (§1-9). seed 0·1·2·4 는 서로 0.0115 %p 안에서 같고
> **seed 3 하나만 0.54 %p 떨어진 다른 해**에 앉는다. 잔떨림이 아니라 다섯 번에
> 한 번 골짜기를 갈아탄다.

> `dd_verify` 는 비교를 위해 매 적합 앞에 `rng(0,'twister')` 를 건다.
> `main_blend_final.m` 은 안 건다 — 그것이 발견 #4 다.

한 번의 적합이 MultiStart 20회 + 사전 적합 10회다. `dump` 는 16회, `profile`
은 21회 적합이므로 각각 십수 분~한 시간을 잡아 두면 된다.

---

## 이 파일들은 어디까지 검사됐나

`tests/` 에서 GNU Octave 8.4 로 실제 실행해 봤다 (`tests/run_all.sh`).
구문·shim 수치·`dd_eval.m` 배관까지는 통과했고, **MATLAB 자체에서 돈다는
증명은 아니다.** 무엇이 닫혔고 무엇이 열려 있는지는 `tests/README.md`.

에러가 나면 그 텍스트를 그대로 주면 된다 — 그게 제일 빠르다.
