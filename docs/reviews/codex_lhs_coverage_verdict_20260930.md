# LHS 피복률 두 묶음 — 병합 전 적대 리뷰

작성: 2026-09-30. **묶음 전체 HOLD. 새 P1 두 건.** 원장 번호는 부여하지 않았고, 생산 코드·원장은 수정하지 않았다.

## 0. 대상과 판정의 의미

- 사용자 최종 핀: **`2e57dff90e7eebead7a446478f97e2c414176c28`**. 이후 브랜치 HEAD는 사용하지 않았다.
- 이 커밋의 요청서·패치 7개를 취득했다. 검증 대상은 요청서대로 **`da4670594 + 제출 패치 0001–0007`**이다. 패치 SHA256 7/7 일치, 별도 소스 사본에 순서대로 적용 성공. 패치 대상 8개 파일은 적용 전 `da4670594`와 사용자 핀에서 바이트가 같았다.
- 여기서 **GO는 선언된 진단/병기 코드를 합칠 수 있다는 뜻**이다. 물리적 피복률 검증, 인계 열 채택, 130/64 실데이터 적격성 승인이 아니다. 이미 알려진 근사를 새로운 발견으로 세지 않았다.
- 실 DEM/MPM 시뮬레이션, ibb 작업, 원본 저장소의 checkout·fetch·병합은 하지 않았다. 합성 입력에 실제 계산 함수·CLI·파이프라인 함수를 실행했다. 파이프라인 수명주기 시험의 계산 subprocess 대역과 Windows 호환용 시험 대역은 아래에 구분했다.
- 근거: [소스·패치 해시](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_evidence_20260930/source_manifest.json), [계산 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_evidence_20260930/audit_results.json), [파이프라인 반례](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_evidence_20260930/pipeline_results.json), [실제 CLI 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_evidence_20260930/cli_results.json).

## 1. 커밋별 판정

| 패치 / 원 커밋 | 판정 | 결론과 경계 |
|---|---|---|
| 0001 / `1dfae6661` | **GO** | 수확기 벽 분류 소비자들은 같은 `depth > 0` 함수를 쓴다. 반올림 전 실제 접촉 여부를 식별한다는 보증은 아니다. |
| 0002 / `a2b0b5369` | **GO** | **분모만 보정하는 장부 proxy와 벽별 진단**의 추가로서 GO. 정확한 ROI/벽 제외 피복률로의 해석은 반증됨. 알려진 교차 미처리를 새 결함으로 중복 계상하지 않는다. |
| 0003 / `69d7cb678` | **HOLD — P2** | 반올림 전 영역 보증 반례와 AST 금지 경로 우회가 있다. 원래 피복률 값은 바뀌지 않으므로 P1로 올리지 않는다. §4의 입력·출력 참조. |
| 0004 / `7d8f696fc` | **GO** | 정식 `harvest()` 경로에서 중복/자기쌍은 피복률 계산 전에 거부한다. 고아 수는 JSON에도 남는다. 단일 영상 접촉을 전제하는 LHS 계약이지 모든 주기 시스템의 보편 규칙은 아니다. |
| 0005 / `166b59724` | **GO** | 명시한 **불연속 cap-우선 후보 연산자**를 구현하고 길이 단위를 맞춘다. 전체 물리 접촉면적의 타당성·연속 탄소성 모델·ML 정답 승인은 아님. |
| 0006 / `d65afca14` | **HOLD — P1** | 분모 무효/비유한 입자 입력이 정상 피복률 `0.0`, 상태 `ok`로 바뀐다. §2. |
| 0007 / `59a0e1ecf` | **HOLD — P1** | atoms-only 조기 반환이 요청한 coverage 필수 단계를 우회한다. 반면 정식 standard/bimodal의 옛 v2 키 재사용 반례는 차단됨. §3. |

GO 항목을 분리 병합할 때는 의존 순서를 지켜야 한다. 이 표는 실패한 뒤 패치까지 포함한 묶음 전체를 승인하지 않는다.

## 2. P1 — v2 분모 무효가 관측된 0으로 바뀐다 [0006]

위치: [coverage_physics_vs_hertzian.py:298](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:298), [307](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:307), [342](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:342).

`free = max(surface − sum(A_v2_AMAM), 0)` 뒤 `free > 0`이 아니면 **`cov=0.0`**이다. `n_free_surface_nonpositive`는 세지만 `keys()`의 무효 사유에는 넣지 않는다. 출력이 유한하므로 `_all_finite`도 구제하지 못한다.

### 실제 함수 반례

1. AM 네 개, 모두 반경 **1 µm**, 정사면체 변 길이 **0.8 µm**. AM–AM 여섯 접촉은 각각 겹침 **1.2 µm**, v2 `geom` 결속. SE 한 개가 AM 하나와 **0.1 µm** 겹치는 접촉도 넣었다. 모든 입력값은 유한하고 중복/자기쌍은 없다.
2. 각 AM에서 세 개의 `2πr²`를 빼므로 분모는 음수다. 실제 `compute_case()` 결과:

```text
n_am = 4
n_free_surface_nonpositive = 4
area_AM전체_SE_total_physics_v2 = 0.79 µm²
coverage_AM_mean_physics_v2 = 0.0 %
coverage_status_physics_v2 = "ok"
```

**기대:** 정의되지 않은 비율, 빈칸과 사유. **실제:** 전 AM이 피복 0인 정상 침대로 표시된다. 이 깊은 겹침은 경계 스트레스 시험이지 실제 코퍼스에서 관측됐다는 주장이 아니다.

더 작은 반례도 있다. **고립 AM 하나의 radius=NaN, 접촉 0개**를 주면 접촉별 입력검사를 아예 안 지나고 같은 `0.0 · ok`가 나온다. 잘못된 반경을 가진 입자가 0 피복 입자로 세어진다.

재현:

```bash
python3 lhs_coverage_evidence_20260930/audit.py
# audit_results.json: denominator_zero, nan_isolated_radius
```

**무너지는 결론:** “v2는 무효 입력/정의 불능을 정상 숫자로 조용히 대체하지 않는다.” 기존 legacy 값 보존은 이 반례로 무너지지 않는다.

**최소 해제:** v2 전용으로 모든 포함 입자의 반경·표면적을 먼저 검증하고, 유효하지 않은 분모를 0 피복으로 넣지 말 것. 침대 전체 빈칸 또는 명시적 유효 부분집합 통계 중 계약을 정하되, 제외 수·분모·상태를 함께 내야 한다. 위 두 반례가 `ok/0`이 되지 않고, **정상 양의 분모+접촉 0**은 진짜 0으로 남는 양성 대조가 필요하다. legacy 경로를 함께 고치라는 요청은 아니다.

## 3. P1 — coverage 요청이 atoms-only 성공으로 우회된다 [0007]

위치: [app.py:3280](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/webapp/app.py:3280), [CSV-only 분기:3287](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/webapp/app.py:3287), [3303](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/webapp/app.py:3303).

입력 폴더에 유효한 `atoms.csv`만 두고 다음 **실제 함수**를 호출했다. 이 경로에는 계산 subprocess 대역도 필요 없다.

```python
run_pipeline(case, 'standard', '1:AM,2:SE', 1000,
             figures=False, auto_db=False, stop_after='coverage')
```

**기대:** 접촉/coverage 부재이므로 명시적 실패. **실제:**

```json
{"success": true, "atoms_only": true, "log": [{"step": "Parse (atoms.csv only)", "rc": 0}]}
```

`full_metrics.json`에는 `has_contacts:false`와 viewer용 설명만 있다. v2 판정 키도 `stopped_after`도 없다. 기존 호출자식 `status or ('done' if success else 'failed')`은 이를 `done`으로 읽는다.

**한정:** LHS `stage_case()`는 원 contact 파일의 존재·해시를 선행 검사하므로 **이 입력이 현재 130건 배치 입구까지 통과했다고 주장하지 않는다.** 새 공개 `run_pipeline(stop_after='coverage')`의 계약이 기존 viewer-only 조기 반환과 충돌하는 결함이다. 정상 `None` 모드의 viewer-only 기능은 유지해도 된다.

재현: `python3 lhs_coverage_evidence_20260930/audit_pipeline.py` → `atoms_only`.

**최소 해제:** `contact/coverage` 같은 분석 단계가 명시적으로 요청되면 두 atoms-only 조기 반환에서 실패하도록 분기하고, `None` viewer 모드는 성공하는 양성 대조를 둔다. raw-atom-only와 CSV-only를 모두 시험할 것.

### P2 — 내용 검증이 상태 스키마까지 보증하지 않는다

[app.py:3180](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/webapp/app.py:3180)의 검사는 문자열 여부뿐이다. `coverage_status_physics_v2=""`와 `"not_run"`도 `_coverage_v2_written()`이 **True**를 반환한다. 제출 producer가 현재 이 문자열을 정상 생성한다는 반례는 아니다. 검사기의 불완전 writer 검출 공백이다. `ok` 또는 사유가 비지 않은 `blank: …` 및 각각의 필수 값/진단 스키마를 검사하라.

## 4. P2 — 0003의 검사 범위가 주장보다 좁다

### 4-1. 반올림만으로 FLAG, 다른 곳에서는 치환을 놓친다

위치: [lhs_descriptor_harvest.py:361](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/lhs_descriptor_harvest.py:361), 특히 374–377의 **각 축을 따로 흔든 변화량의 합**.

반올림 전 실제 입력과 함수로 계산한 면적:

```text
r1 = 0.002, r2 = 0.0010000049, delta = 0.0020000051 [sim length]
A  = 5.90620349109427e-11 [sim length²]
```

네 값을 각각 `format(x, '.6g')`로만 출력·되읽기:

```text
r1 = 0.002, r2 = 0.001, delta = 0.00200001, A_dump = 5.9062e-11
A_recalc = 0
abs(diff) = 5.9062e-11
tolerance = 5.0139289433549014e-17
diff/tolerance = 1,177,958.4566765053 → FLAG
```

**기대:** 순수 반올림 입력을 허용. **실제:** FLAG. 포함/비포함 경계에서 반경과 δ를 **동시에** 움직이면 교차 원판이 생기는데, 축별 탐침 합은 이를 놓친다. `1.001` 배는 다변수 구간 보증이 아니다.

반대 방향 반례: `r1=r2=0.0005`, `δ=0.000999999`에서 기준 면적은 `7.85398163396663e-7`, 허용폭은 `1.5723676220916433e-6`. Hertz 치환 `7.85397e-7`도, `+3e-5` 상대오차 치환 `7.85422e-7`도 통과한다.

**한정:** 두 반례는 매우 깊은 겹침/포함 경계이다. 130/64에 이런 접촉이 있다는 증거가 아니다. 별도 무작위 **15,000건** (`r1,r2=10^-4…10^-2 sim`, `δ/R*=10^-5…1`, seed `20260930`)은 순수 반올림 오탐 **0**, `3e-5` 치환 누락 **0**이었다. 제출 3,000건의 성적을 부정하지 않지만 **“모두”로 확장할 수 없다.**

재현: `audit.py` → `rounding_only_false_alarm`, `hertz_miss`, `3e-5_miss_deep`, `rounding_sweep`.

**최소 해제:** 지원 기하 범위를 명시하고 범위 밖을 “면적 불일치”와 구별하거나, 공동 반올림 구간을 포괄하는 경계 계산을 구현할 것. 전역 상수를 넓혀 오탐만 없애는 방식은 판별력을 더 낮춘다. 모든 상태를 여전히 진단 기록으로만 쓰는 범위는 유지한다.

### 4-2. 평범한 import 두 가지가 금지 경로를 연다

위치: [lhs_descriptor_harvest.py:441](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/lhs_descriptor_harvest.py:441).

아래 두 입력 모두 `_plastic_coverage_uses()`가 **`(set(), [])`**를 반환한다. 실제 `exec`에서는 Physics 함수를 호출한다.

```python
from scripts import plastic_coverage as pc
pc.film_area_from_overlap(.1, .5)
```

```python
from importlib import import_module as im
pc = im("plastic_coverage")
pc.film_area_from_overlap(.1, .5)
```

첫째는 `ImportFrom.module == 'scripts'`, 둘째는 호출 이름이 `im`이라 검사 분기를 피한다. 현행 수확기 본문이 이 우회를 쓰고 있다는 뜻은 아니다. “여섯 모양을 잡는다”는 시험은 통과하지만 **Physics 호출 금지 계약을 보증하지 않는다.**

**최소 해제:** 패키지에서 모듈을 가져오는 형태와 import alias 추적을 포함하고 두 음성 대조를 상주시켜라. 더 단순한 구조는 순수 기하 함수를 별도 작은 모듈로 분리해 수확기에서 Physics 모듈 의존 자체를 없애는 것이다. AST를 임의 Python 실행의 완전한 안전 증명으로 부르지 말 것.

## 5. Q1–Q9 답

### Q1 — 벽 규칙: 구현 통일 CONFIRMED, 반올림 안정성 보증 없음

[592](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/lhs_descriptor_harvest.py:592)의 거리 → [601](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/lhs_descriptor_harvest.py:601)의 벽 함수가 `_wall_side`, `wall_touch_fractions`, `coverage_wall`에 공통이다. τ의 슬래브 선택 부등식은 다른 양이므로 단순히 `<=`가 남았다는 이유로 결함으로 세지 않았다. 알려진 열 사전의 옛 문구는 새 finding이 아니다.

규칙은 **저장 좌표에서 양의 cap 깊이**이지 반올림 전 실제 접촉 분류가 아니다. 깊이 `r−z+z_wall`의 불확실폭은 각 토큰의 반올림 반폭 합으로 잡고, `|depth|≤그 폭`인 수를 상·벽별로 보고해야 한다. STL의 정밀도는 atom dump의 6자리 가정을 그대로 복제하지 말고 따로 읽어야 한다.

분류 하나가 움직이면 해당 상의 비율은 `1/N_phase` 움직인다. cap 면적은 연속이지만 벽 제외 분모가 0에 가까우면 피복률 민감도는 작다고 보장할 수 없다. **130/64 원 dump가 이 리뷰에 없으므로 near-tangent 실측 수·코퍼스 민감도는 미측정**이다.

### Q2 — 벽 제외: 식은 맞게 구현됐지만 ROI 피복률은 아니다

[coverage_wall:853](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/lhs_descriptor_harvest.py:853)은 벽 cap을 **분모에서만** 뺀다. numerator는 `_coverage_sums`의 원 AM–SE 합이다.

실제 반례: AM `r=1,z=-0.9`, SE `r=0.5,z=-2.3`, floor=0, plate=10. 교차 원판은 `z=-1.867857142857…` 평면에 있어 **전부 ROI 밖**이다. 그 면적 `0.19871374960652743`을 남긴 채 작은 분모로 나누어 **31.626275510204017% · OK**가 나온다. ROI 안 이 접촉의 몫은 0이다. `audit.py:wall_outside_numerator`.

고정된 유효 입자 집합에서 ① 중복 차감은 분모를 과소화하고 ② 바깥 분자 잔존은 분자를 과대화하므로 두 효과는 위쪽이다. 100% clip 뒤에도 오차가 작다는 보증은 없고 참값 0에서는 상대오차 상한도 없다. **분모≤0 입자 제외 뒤 모집단 평균의 편향 방향은 어느 쪽도 가능**하다. 집계 함수에 두 AM과 면적 장부를 직접 넣은 대조에서는 바깥 AM의 옛 값 25%가 제외되어 남은 평균이 0%가 된다(이 두 번째 대조의 좌표·면적은 물리적 접촉 침대를 구성한 것이 아니라 선택 산술을 시험한 입력이다). 반대로 낮은 값을 제외하면 평균은 오른다.

제외는 JSON의 `counts`, `n_free_surface_invalid`, 분할의 `n_valid_wallexcl`에 기록되므로 문자 그대로 “조용히 아무 기록 없이” 버리는 것은 아니다. 다만 `OK`는 **남은 유효 입자 평균의 계산 상태**다.

**병합 가능한 해석:** “원 AM–SE 면적합 / AM–AM 및 두 벽 cap 차감 장부 분모, 유효 입자 평균”. 이를 “벽 안 SE가 덮은 순수 면적”으로 읽으면 반증된다. [문서 문자열:843](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/lhs_descriptor_harvest.py:843)의 “분자·분모 모두에서 뺀 값”은 정확히는 **벽 자체 접촉을 numerator에 더하지 않았다는 뜻**으로 고쳐야 한다. 밖의 particle-contact numerator를 잘랐다는 뜻이면 거짓이다.

floor/plate를 따로 내는 것은 타당하다. 다만 두 표의 `mean_wallexcl_pct`는 각각 한 벽만 교정한 값이 아니라 **두 벽을 모두 뺀 동일 입자값을 서로 다르게 분류한 평균**이다. 바닥의 SE 물성은 분리막 전도/유효 반응 면적을 측정했다는 증거가 아니며, 이번 기하 코드도 그것을 계산하지 않는다.

### Q3 — 반올림/AST: 부분, §4의 두 반례로 전역 보증 REFUTED

진단의 정상 범위 성적은 좋지만 오차 구간 증명이 아니다. AST는 종전 머리말 문자열 검사보다 일부 경로에서 강해졌으나 새로운 형태까지 완전히 닫지는 않았다. 기존 target 값에 직접 쓰지 않는다는 점은 유지된다.

### Q4 — 접촉 문: 정식 수확 경로 CONFIRMED, 주기 일반화는 제한

[harvest:1115](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/lhs_descriptor_harvest.py:1115)에서 gate 뒤에만 피복률·면적 대조가 돈다. 그 앞의 φ 계산은 피복률이 아니고, 거부되면 정상 수확 결과로 반환되지 않는다. 공개 저수준 `coverage_hertz()/coverage_wall()` 자체는 gate를 호출하지 않으므로 직접 호출자에게까지 보장한다고 쓰면 안 된다.

**고아 JSON 부재라는 전제는 틀렸다.** [1244](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/lhs_descriptor_harvest.py:1244)의 `contact_gate`에 `n_orphan_rows/n_orphan_ids`가 직렬화된다. 현재 고아 정책은 **제외하고 수를 남기는 부분집합 통계**이지 원자료 완전성 통과가 아니다.

LIGGGHTS 공식 설명은 local 출력이 프로세서 전체의 **상호작용**을 나열하며 periodic flag는 주기 경계를 통한 상호작용 표시라고 한다. MPI ghost 존재 자체가 동일 물리 접촉 두 행을 정상화하는 근거는 아니다. 다만 이 문서는 unordered **ID 쌍의 전역 유일성**을 선언하지 않는다. [공식 pair/gran/local 문서](https://www.cfdem.com/media/DEM/docu/compute_pair_gran_local.html).

기하적 예외: 길이 L의 주기 방향에 두 입자가 0.45L 떨어지고 반경합이 0.6L이면 거리 0.45L와 0.55L의 **서로 다른 영상 접촉 두 개**가 가능하다. 이때 ID 쌍만으로 합치거나 거부하는 것은 일반 알고리즘이 아니다. 대상의 단일 영상 영역(예: 각 접촉 반경합 < 최단 주기 길이/2)을 raw box·radii로 확인하거나, 더 큰 입자에 확장할 때 영상 구분자를 계약에 넣어야 한다. **현재 LHS에 실제 과잉 거부가 발생했다고 주장하지 않는다.** 130의 과거 감사 0건을 64의 증거로 옮기지도 않는다.

### Q5 — cap v2: 연산자 구현 CONFIRMED, 검증된 전체 피복률로의 승격은 불가

[film_area_physics_v2:504](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/plastic_coverage.py:504) 이후는 선언한 식을 따른다. `H_FILM_MIN * length_scale`은 맞다. 길이가 SI×1000이면 부피는 ×10⁹, 막 두께는 ×1000이므로 면적은 ×10⁶이다. 실제 동일 기하 재계산에서 sim/SI 면적비 **999999.9999998804**, 결속은 동일했다.

반경 0.5 µm의 같은 두 구에서:

```text
DR_YIELD_ONSET = 0.0011314801509618464
delta_onset = 2.828700377404616e-10 m
바로 아래 A = 2.221656081215254e-16 m²
개시점 A    = 1.2567613678604604e-17 m²
비          = 0.05656867318424044  (약 94.3431% 하락)
```

이는 같은 코드의 자가 신고가 아니라 직접 두 입력을 넣은 결과다. 단위 교정으로 cap이 작동하게 됐지만, **`V_lens/h_min`을 전체 접촉면적의 상한으로 삼는 물리 가정**까지 증명된 것은 아니다. `L>U`에서 U를 선택하면 하한 조건은 버린 것이다. 기존 상·하한 모순을 동시에 충족하도록 “해결”한 것이 아니다.

따라서 이 병기판은 **불연속 체적-budget 기반 후보 디스크립터**로 계산·감도 비교할 수 있다. 측정된 물리 피복률이나 검증된 연속 탄소성 해로 부를 수 없다. 임의 smoothing만으로 물리성이 생기지 않는다. 전체 접촉면적과 추가로 퍼진 면적의 역할, 탄성 가지와의 연결을 먼저 결정해야 한다. 물성 상수값 변경이나 인계 열 선택은 이 리뷰에서 요구하지 않는다.

### Q6 — 침대 빈칸/legacy/폴더 수정

한 접촉의 면적이 미정이면 완전 접촉 집합의 합도 미정이므로 **v2 전체 빈칸**은 방어 가능한 fail-closed 정책이다. legacy 및 다른 디스크립터까지 지우는 정책은 아니다. 완화하려면 유효 부분합/제외 수를 별개 양으로 등록해야 한다. 문제는 엄격함 자체보다 **분모/입자 검사에는 그 정책이 적용되지 않는 §2의 비대칭**이다.

legacy 핀은 요청된 세 출력, 즉 JSON legacy 키·값·순서, LF 정규화 CSV, 반환값을 실제로 포함한다. 별도 이전 코드와의 비교도 **6 변형×3종 모두 동일**했다. 단 합성 표본의 보존 증거이지 모든 가능한 입력·실행 실패까지의 수학적 동등성 증명은 아니다.

외부 `WEBAPP_*_FOLDER` 배치에서 실제 case-id CLI를 실행해 v2와 legacy 키가 **둘 다 새로 쓰임**을 재현했다. 이는 입력 파일이 같을 때 기존 계산식이 바뀐 것이 아니라 **종전 skip이 실행으로 바뀐 행위 변경**이다. [export_master_csv.py:102](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/export_master_csv.py:102)는 full_metrics 전체를 펼치므로 새 값과 열이 소비자에게 보인다. “wall 두 예외 외에는 어떤 관측도 안 바뀐다”는 표현은 넓게 쓰면 틀리다. 같은 데이터 디렉터리의 기존 정상 계산값 보존과, 그동안 실행되지 않던 디렉터리의 신규 계산을 구분해야 한다.

### Q7 — 옛 산출/모드 관문

**정상 두 경로에서 옛 v2 도장만으로 done이 되는 반례는 실패했다.** 옛 full_metrics에 `ok/999`를 심고 contact가 새 파일을 생성하게 한 뒤 coverage가 rc=0·아무것도 쓰지 않게 했다. standard·bimodal 모두 **failed**, 최종 metrics에는 옛 키가 없었다. contact 단계의 실제 causal stash가 원인이다. 이 시험은 orchestration 실제 함수 + 계산 subprocess 대역이다.

세 정상 모드의 여섯 혼합 방향은 모두 시험에 있고 거부됐다. 다만 [lhs_webapp_batch.py:244](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/lhs_webapp_batch.py:244)의 보증은 **정상 schema의 status.json이 있는 출력 폴더**에 한정된다. 도장이 없거나 다른 schema인 비어 있지 않은 폴더까지 검사한다는 뜻은 아니다. 재개도 기존 done/partial을 자동 재검증하지 않는다. 이번에는 새 모드·새 출력 폴더를 사용해야 한다.

별도의 조기 반환과 불완전 상태 문자열 문제는 §3이다.

### Q8 — 충돌 해결: 상태 복원 CONFIRMED

[lhs_webapp_batch.py:556](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/lhs_webapp_batch.py:556)에서 `FakeA.mode='bimodal'`, 560에서 수확 JSON을 `_hj()` 3-type으로 되돌리고, `_run14`의 마지막 호출이 `FakeTMR.m`도 3-type으로 돌린다. 그 다음 coverage 시험으로 넘어간다. 이 순서에 숨은 2-type 잔존 반례는 발견하지 못했다.

Windows symlink 권한 때문에 원형 배치 selftest는 실행 준비에서 멈췄다. **시험 내 symlink만 byte copy로 대체**한 통제 실행에서는 본문 그대로 **29/29** 통과했다. 이것을 Linux 배포 symlink 성공으로 세지 않는다. 번호 변경 자체의 결함은 아니다.

### Q9 — 남은 skip과 보존 주장의 정확한 범위

- 수확기 정상 입력 **15 호출**에서 기준 코드와 같은 입력을 대조했으며, 의도한 wall 두 키를 제외한 **36 legacy 키의 차이 0**. 8개 golden fixture도 LF 통제 아래 통과한다.
- 중복/자기쌍 입력은 새로 거부되므로 당연히 기존 정상 JSON과 같지 않다. 이것은 0004의 명시적 개입이지 숨은 변경이 아니다.
- CLI의 “조용한 skip을 모두 없앴다”는 해석은 틀리다. `--all`은 nested archive를 재귀 발견한 후 basename만 넘기고, `find_case_dir`는 깊이 1만 찾는다. 실제 `archive/category/nested` fixture에서 **rc=0, `[skip] nested`, v2 미작성**을 재현했다. [1027](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:1027), [101](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:101).
- 손상된 full_metrics JSON도 실제 `--case-dir` 실행에서 경고만 내고 **rc=0**, 파일은 손상 상태 그대로였다. [662](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:662). **둘 다 기존 CLI에서 이어진 경로**로, 이번 패치가 새로 만들었다고 세지 않는다. 새 required pipeline은 이와 달리 산출 판정 부재를 거부한다. 직접 CLI 사용자에게 rc=0이 완료 증서라고 안내해서는 안 된다.

## 6. 재현 범위와 selftest 결과

환경: Windows, Python 3.12.14, NumPy 2.3.5, pandas 3.0.1, SciPy 1.16.3, NetworkX 3.7. 누락 라이브러리는 리뷰 전용 폴더에만 준비했다.

| 시험 | 독립 실행 결과 |
|---|---|
| plastic_coverage | 27/27 PASS |
| coverage_physics_vs_hertzian | 13/13 PASS |
| pipeline_provenance | 198/198 PASS |
| lhs_design_dataset | 113/113 PASS |
| lhs_descriptor_harvest | 원형 137/139. LF fixture 통제 후 138/139. 아래 설명 |
| lhs_webapp_batch | 원형은 Windows symlink 권한 오류. copy 대역 통제 29/29 |
| check_all 전체 | **독립 재실행하지 않음**. 제출된 gate.log의 74줄 초록을 내 실행 결과로 인용하지 않는다. |

수확기 두 실패를 이번 수치 회귀로 오인하지 말 것. 하나는 fixture raw 파일의 Windows CRLF가 SHA 핀과 다른 문제로, LF 쓰기 통제에서 사라졌다. 남은 τ median은 기준·후보 모두 **2.080532952769607**, 핀은 **2.0805329527696066**이다(약 4.44e-16, 1 ULP). 같은 환경의 기준/후보 τ 결과는 완전히 같았다. 이를 빌미로 과학적 허용오차를 넓히라는 요청은 아니다. 플랫폼 독립 수치 검증과 raw-byte 보존 검증을 분리하면 된다.

재현 스크립트:

```bash
# LHS_REVIEW_REPO: da4670594 + 고정 핀의 패치 7개를 적용한 별도 사본
# LHS_REVIEW_BASELINE: da4670594의 원본 파일 사본
python3 lhs_coverage_evidence_20260930/audit.py
python3 lhs_coverage_evidence_20260930/audit_pipeline.py
python3 lhs_coverage_evidence_20260930/audit_harvest.py
python3 lhs_coverage_evidence_20260930/audit_cli.py
```

스크립트는 자신이 만든 합성 fixture만 쓰고, 그 결과를 증거 폴더에 저장한다. pipeline 시험은 원격 저장소 설정을 비우고 계산/solver 실행을 대역으로 막는다. CLI 시험은 실제 coverage CPU 후처리를 실행한다.

## 7. 병합 전 최소 수정 목록

1. **0006:** v2의 비유한 입자/분모≤0을 `0.0 · ok`로 내지 않기. 무효 분모·고립 NaN·정상 접촉 0의 세 대조를 포함한다.
2. **0007:** 명시적 coverage/contact 요청에서 atoms-only 성공 우회를 막기. viewer 전용 기본 모드는 보존한다. 상태 내용 검증은 빈 문자열/임의 문자열도 거부하도록 보완한다.
3. **0003:** 포함 경계 반올림 반례를 검사 범위 계약 또는 공동 구간 계산으로 처리하고, 두 import 우회에 대한 회귀를 추가한다. 일반 15,000건의 성적을 전역 보증으로 쓰지 않는다.

문서·인계 전 명료화: `wallexcl`은 분모 보정 proxy이며 분자 교차는 계산하지 않음, v2는 미검증 후보 연산자임, `OK`의 계산 상태와 물리 적격성은 다름, 실제 reharvest는 **새 디렉터리**에 수행. 130/64 전체의 접선 근처 수·무효 분모율·cap 충돌률·입자 제외율은 이후 원자료 계산에서 보고할 것. 현재 보지 않은 코퍼스 값을 추정으로 채우지 않는다.

**최종: HOLD — 0003·0006·0007 수정 후 해당 반례 재검증.**
