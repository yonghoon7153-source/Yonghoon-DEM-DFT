# Case naming convention reference

> **이 문서는 case_summary.csv (86 case ground truth)에서 추론한 명명 체계입니다.**
> 새로운 case 추가시 갱신하세요.  grade_engine + dashboard tooltip이
> 참조합니다 — 잘못된 추측 (이전 "real40 = high pressure" 같은) 방지용
> single source of truth.

## 1. 기본 구조

```
input_<CAPACITY>_<RVE_VARIANT>_<CONFIG_INDEX>[_<SEED>|_<SUFFIX>]
```

예시:
- `input_6mAh_real_4`        → 6 mAh/cm², RVE 50×50, config #4
- `input_6mAh_real40_4`      → 6 mAh/cm², RVE 40×40, config #4 (RVE-only twin)
- `input_1mAh_9_S3`          → 1 mAh/cm², config #9, seed #3
- `input_8mAh_5_AMP`         → 8 mAh/cm², config #5, AM_P-only
- `input_particulate_12_S3`  → SE-size sweep config #12, seed #3

## 2. 토큰 분류

### 2.1 Areal capacity target (`1mAh` / `6mAh` / `8mAh`)
Target = areal capacity (mAh/cm²) → thickness 결정.  CSV 실측:

| Token | thickness range (μm) | 용도 |
|---|---|---|
| `1mAh`  | 15–21 | 박막 (thin) |
| `6mAh`  | 110–120 | 후막 (thick, 상용 수준) |
| `8mAh`  | 140–185 | 초후막 (high-capacity, 도전적) |

> capacity가 클수록 같은 ASR이라도 cell-level 분극이 커짐 → harsh test.

### 2.2 RVE size variant (`_real` / `_real40` / `_100` / default)

| Token | RVE (μm²) | 메모 |
|---|---|---|
| (`_real`) | **50×50 = 2500** | 6mAh / 8mAh 기본 (real cathode-like) |
| `_real40` | **40×40 = 1600** | smaller RVE → finite-size noise ↑ |
| `_100`    | **100×100 = 10000** | 1mAh 큰 RVE — finite-size 줄임 |
| (1mAh basic) | **50×50 = 2500** | 1mAh 기본 |
| `particulate` | **30×30 = 900** | 가장 작은 RVE, SE-size sweep용 |

**중요**: `real40` ≠ "high-pressure sintering 40 atm".  RVE 크기만 다름.
real_X ↔ real40_X 같은 trailing number는 **동일 물리 input의 RVE-only twin**.

### 2.3 Config index (`_1`, `_2`, ..., `_15`)
Trailing number는 input parameter set 식별자.  같은 capacity tier 안에서
`_X` 끼리 config (P:S 비율, AM/SE 입자 반경, etc.) 다름.

6mAh / 8mAh 시리즈의 config 정보 (CSV 추론):

| Config | r_SE (μm) | ps_ratio | r_AM_P / r_AM_S (μm) |
|---|---|---|---|
| _1, _2, _3, _4, _5 | 0.5 | varies | 6.0 / 2.0 |
| _6 (standard AMS)   | 0.5 | 0:10 | – / 2.0 |
| _7, _8, _9          | **1.5** (큰 SE) | varies | 6.0 / 2.0 |
| _10 (standard AMP)  | 1.5 | 10:0 | 6.0 / – |

1mAh 시리즈도 _1..._9 + _S1..._S5 + _AMP / _AMS 동일 구조.

### 2.4 Seed variation (`_S1`, `_S2`, `_S3`, `_S4`, `_S5`)
**같은 input parameter, 다른 random seed 5회 반복**.  Statistical
replicate.  `_S1`..`_S5` 평균/표준편차로 신뢰도 평가 가능.

예: `input_1mAh_6_S1`..`_S5` 모두 `ps_ratio=7:3`, `r_SE=0.5μm`, RVE 50×50,
80:20 AM:SE 동일 — 차이는 seed뿐.

### 2.5 Pure mono-AM cathode (`_AMP` / `_AMS`)
Bimodal config를 mono로 단순화한 baseline:
- `_AMP`: ps_ratio **10:0** → AM_P (대입자) only standard mode
- `_AMS`: ps_ratio **0:10** → AM_S (소입자) only standard mode

같은 config의 _AMP / _AMS / (bimodal 7:3 등) 비교로 입자 크기 분포 효과
정량화.

### 2.6 Particulate series (SE 크기 매트릭스)
**전부 AM_S only standard mode (P:S = 0:10), RVE 30×30 μm**.  Config
번호는 다음 매트릭스로 결정:

|        | 62:38 (low AM)  | 72:28 (med AM) | 82:18 (high AM) |
|---|---|---|---|
| r_SE 0.5μm | _1, _4      | _5             | _6 |
| r_SE 1.0μm | _7          | _8             | _9 |
| r_SE 1.5μm | _10         | _11            | _12 |

추가:
- `particulate_9_E05`, `particulate_9_E15` — **추정**: ε(porosity) target
  변형 (E05 → final ε≈14%, E15 → final ε≈20%).  확실치 않음, 사용자 확인 필요.
- `particulate_12_S1..S5` — config 12의 seed 5회 반복.

### 2.7 S series (`S_1` / `S_2` / `S_3`)
**AM_S only standard, RVE 30×30, r_SE=0.5μm**.  Trailing number =
**AM:SE 비율 변화** (62, 72, 82).  CSV에는 r_AM_S 값이 빈칸 — input
schema 차이일 가능성. (사용자 확인 필요)

## 3. 분석 사용시 주의사항

### 3.1 직접 비교 가능한 쌍 (RVE-only twin)
다음 케이스들은 **동일 물리 input의 RVE 크기만 다른 finite-size 쌍**:
- input_6mAh_real_2  ↔ input_6mAh_real40_2  (r_SE=0.5)
- input_6mAh_real_4  ↔ input_6mAh_real40_4  (r_SE=0.5)
- input_6mAh_real_7  ↔ input_6mAh_real40_7  (r_SE=1.5)
- input_6mAh_real_9  ↔ input_6mAh_real40_9  (r_SE=1.5)
- input_8mAh_2..9 ↔ input_8mAh_real40_2..9  (같은 패턴)

σ_ionic / ASR 차이는 **statistical noise**, 본질적 차이 아님.

### 3.2 Seed group (statistical replicates)
- input_1mAh_6_S1..S5  (5 seeds, ps=7:3, 80:20 AM:SE)
- input_1mAh_9_S1..S5  (5 seeds, ps=7:3, 85:15 AM:SE)
- input_particulate_12_S1..S5  (5 seeds, r_SE=1.5μm, 82:18)

평균 ± σ 보고가 honest comparison.

### 3.3 직접 비교 부적합한 쌍
- 다른 capacity tier (1mAh vs 6mAh) → thickness 차이 본질적
- 다른 r_SE (config _4 vs _7) → SE 크기 변형 본질적
- particulate vs full cathode → AM 입자 단분산 vs 다분산

## 4. 코드에서 사용

- `scripts/grade_engine.py::_rve_area_um2()` — RVE 면적 추출 (finite-size 신뢰도)
- `scripts/grade_engine.py::detect_unit_cell()` — 단위셀 자동 감지 (엄격 조건)
- `scripts/grade_engine.py::build_overall_grade()` → `composite.base_case`
  - `real_X` ↔ `real40_X` 같은 `_rveX_X` base로 묶음
  - 다른 케이스는 각자 distinct (capacity / config / seed 보존)

## 5. Reference 데이터

이 문서의 ground truth: `docs/case_summary.csv` (86 cases × 308 cols).
사용자가 새 case 추가하면 다음 명령으로 갱신:

```bash
cd ~/Yonghoon-DEM-DFT && python3 -c "
import json, csv
from pathlib import Path
rows = []
for d in sorted(Path('webapp/uploads').iterdir()):
    if not d.is_dir(): continue
    cid = d.name
    row = {'case_id': cid}
    for fp, p in [(d/'meta.json', 'meta'),
                   (Path('webapp/results')/cid/'input_params.json', 'ip'),
                   (Path('webapp/results')/cid/'full_metrics.json',  'fm')]:
        if fp.exists():
            try:
                for k, v in json.load(open(fp)).items():
                    if isinstance(v, (int, float, str, bool)) and len(str(v)) < 200:
                        row[f'{p}__{k}'] = v
            except: pass
    rows.append(row)
keys = sorted({k for r in rows for k in r.keys()})
csv.DictWriter(open('docs/case_summary.csv','w',newline=''), fieldnames=keys).writerows(
    [dict.fromkeys(keys,'')] + rows)  # header via writeheader logic
print(f'{len(rows)} cases')
"
```

(또는 더 간단히: scripts/dump_case_summary.py 헬퍼 스크립트 만들면 좋음 — TODO)
