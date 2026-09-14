# α·β 검증 하네스 R6 — 최종 Codex 리뷰

## 판정: NO-GO

대상은 **`d4314048c63605fb4613f8b0a91859271fddda98`**, `claude/bms-alpha-beta-verify`의 `bms-balancing/`이다. 사용자 첨부 `R6_REQUEST_d431404.md`를 정본으로 삼았다. 이전 `1049894` 검토를 자동 합산하지 않았다.

**수치표의 주요 결론은 유지됐지만, “검증한 결과 묶음”과 “실제로 소비한 입력”의 동일성이 아직 보장되지 않는다.** 새 발견은 **P1 3조건·P2 3조건**이다. 독립 GO 전제처럼 신고된 미결을 다시 세거나, 원자료가 없다는 이유로 NO-GO를 준 것이 아니다.

여기서 NO-GO는 R3 §5와 R5 §4에 따른 **정본·하네스의 성공 판정을 그대로 새 모델 설계의 확정 근거로 채택하는 것**에 대한 판정이다. 범위를 붙인 다섯 관측으로 **설계 요구서 초안을 작성하는 일은 진행 가능**하다. 배터리 본 실행이나 이전 `degradation-degeneracy` 게이트의 판정이 아니다.

## 1. 실행 증거와 한계

Fresh checkout에서 LF를 유지했다. 대상 코드는 수정하지 않았으며, 최종 통합 재생의 대상 상태는 실행 전·후 모두 clean이다. 합성 입력은 임시 디렉터리에만 만들었다.

| 검사 | 직접 관측 |
|---|---|
| 전체 회귀 | **132 passed**, 실패 0 |
| `matlab/tests/run_all.sh` | rc 0. **Octave 부재로 1–3단계 미실행**, 4·5단계 통과 |
| 실제 `compare_states.py` | rc 0 |
| 새 비교기 검사 | 36개 합성 사례: helper와 별도 process의 실제 eval dispatcher 결과가 기대한 0/1/2/3과 일치 |
| 로컬 형식 대조 | Python–libc `snprintf` 533건, 불일치 0. **MATLAB 실행이 아님** |
| 기존 반례 선택 재생 | R5 영점·parameter 이름·예외 개수·matrix 감사 4건의 옛 assertion이 이제 실패. 실패 이유도 확인 |
| 새 입력·독자·수치 재현 | 세 담당 스크립트 모두 rc 0; 아래 반례와 양성 대조를 확인 |

환경은 Python 3.12.3, NumPy 2.5.3, SciPy 1.18.1, pandas 3.0.5, openpyxl 3.1.5, pytest 9.1.1 / WSL이다. 실제 소요 시간·명령·stdout/stderr·소스 SHA는 [원시 실행 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_replay_results.json)에 있다. 재현 스크립트의 rc 0은 **예상한 반례까지 관측했다는 뜻이지 GO가 아니다.**

첫 환경 설정 시 하위 shell이 가상환경 밖의 `python3`를 사용하여 환경 서명 시험 1건이 실패했다(131 passed·1 failed). PATH를 동일 인터프리터로 맞춘 뒤 전수 132건이 통과했다. 이는 코드 반례로 세지 않았다. 또 통합 실행을 재현 파일 하나가 저장되기 전에 시작한 회차는 로그 생성에 실패했으며, 완료 증거로 쓰지 않았다. 최종 파일들은 모두 준비·고정한 뒤 다시 재생했다.

비공개 MATLAB·실측 XLSX·문헌 원자료는 독립 실행하지 않았다. 사용자 U15는 한 MATLAB 판·표본 둘이라는 신고 범위로 인정한다. U14는 **커밋된 새 산출과 `bfc4623^`에서 추출한 구 산출의 직접 대조**이지, 이 환경에서 비공개 원자료로 최적화를 다시 돌렸다는 뜻이 아니다.

## 2. 새 P1 — GO 전에 닫아야 하는 세 조건

### R6-01 [P1 · 결과 결속] 독자가 검증한 bytes와 표가 소비한 bytes가 다르다

위치: [compare_states.py:63](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/compare_states.py:63), [같은 파일:68](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/compare_states.py:68), [같은 파일:84](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/compare_states.py:84). 검증 함수는 [provenance.py:138](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/provenance.py:138).

재현은 [execution 스크립트](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_execution_repros.py)의 `snapshot_metadata_mix`·`matrix_after_verification`이다. 실제 atomic writer와 `run_states.sh`의 실제 metadata helper를 쓴다. Hook은 파일 읽기 경계에 정상적인 두 번째 게시가 끼는 순서만 고정한다. A/B는 서로 다른 ID이며 ID 복사·metadata 위조는 없다.

```bash
python /path/to/review/harness_r6_final_execution_repros.py \
  --target /path/to/d431404/bms-balancing
```

첫 순서:

1. A JSON/meta의 정상 묶음을 게시한다.
2. `load_degeneracy()`가 A JSON bytes를 읽는다.
3. 다른 정상 시도 B가 B JSON/meta의 정상 묶음을 게시한다.
4. 독자가 pathname의 **B/B**를 검증하고, 저장해 둔 **A JSON**에 **B meta**를 붙인다.

```text
loaded_data_run_id = attempt-A
loaded_value       = 1.0
loaded_meta_run_id = attempt-B
loaded_meta_starts = 24
disk_value         = 20.0
disk_unit          = [true, "일치"]
```

두 번째 순서는 matrix의 반대 순서다. 실제 검사에서 A의 LLI 폭 3.0을 검증한 직후 B의 CSV만 게시하면, 독자는 B의 폭 **79.0**을 읽어 표에 넣는다. 그 순간 디스크 묶음을 재검사하면 B data/A meta라 **false**다.

현재 검사는 “이 경로가 검사할 때 맞았는가”만 반환한다. 그 뒤/앞에 따로 읽은 bytes를 보증하지 않는다. 검사를 한 번 더 붙이는 것으로 동일성이 생기지 않는다. 내부 F07의 **고정된 혼합 묶음 거부는 실제로 고쳐졌지만**, 독자가 그 검증 대상과 다른 snapshot을 소비한다.

**최소 닫힘 조건:** 독자에게 검증한 data bytes와 meta snapshot을 함께 반환하고, 표·후속 계산은 그것만 소비하게 한다. 동일 게시 잠금 안에서 둘을 캡처하거나, 완성된 불변 묶음 하나를 선택한 뒤 읽는다. 위 두 순서의 결과는 A/A, B/B, 명시적 미완 중 하나여야 한다. **A/B나 검증하지 않은 B의 성공 소비는 금지**한다.

### R6-02 [P1 · 실행 완결성] 새 산출의 첫 게시 중단이 “옛 파일” 예외로 통과한다

위치: [provenance.py:144](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/provenance.py:144), [compare_states.py:44](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/compare_states.py:44), [ne_shape.py:98](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/ne_shape.py:98).

위 execution 명령의 `missing_modern_meta`가 재현한다.

- 비어 있는 출력 디렉터리에 실제 `atomic_write_json`·`atomic_write_csv`로 **`run_id`가 있는 현행 산출**을 게시한다.
- 최초 `write_meta` 전에 중단한다. 기존 metadata를 지우거나 조작하지 않는다.
- `verify_unit`는 `(None, "meta 없음")`을 반환한다.
- `compare_states`의 JSON·CSV 독자와 `ne_shape.fitted_pair_info`가 **셋 다 소비에 성공**한다.

```text
modern_record_has_run_id = true
degeneracy_accepted      = true
matrix_accepted         = true
fitted_pair_accepted    = true
```

양성/음성 대조도 실행했다. 올바른 metadata를 붙이면 true이고, 이후 다른 ID의 CSV만 게시하면 false 및 표 제외가 된다. 따라서 “옛 파일을 허용한다”는 규칙 자체의 재보고가 아니라 **현행 생산자의 미완 상태와 실제 역사 산출을 구분하지 못하는 문제**다. 원장에 설명한 예외는 pre-R5 산출 호환이고, 요청문 §4는 새 시도의 metadata 미완을 완료로 소비한다고 신고하지 않았다.

**최소 닫힘 조건:** 현행 schema의 산출에는 현행 metadata가 필수여야 한다. legacy 호환은 실제 legacy schema/명시된 역사 자료로 제한한다. 위 첫 게시 중단에서 세 독자가 모두 미완을 알리고 제외·거부해야 하며, 진짜 legacy fixture는 의도한 호환 경로로 계속 읽혀야 한다.

### R6-03 [P1 · 소비 입력 결속] A로 계산하고 B의 `inputs_sha`를 기록한다

위치: [verify.py:174](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/bms_balancing/verify.py:174)의 실제 풀셀 읽기와 [184](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/bms_balancing/verify.py:184)의 사후 해시, [ne_shape.py:229](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/ne_shape.py:229)의 측정 읽기와 [248](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/ne_shape.py:248)의 사후 identity.

재현: [claims 스크립트](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_claims_repros.py).

```bash
python /path/to/review/harness_r6_final_claims_repros.py \
  --target /path/to/d431404/bms-balancing
```

**실제 `build()` 경로:** 합성 XLSX A를 실제 `load_full_cell`로 읽은 뒤, 같은 pathname에 전압을 +20mV한 유효 XLSX B를 재-export한다. Objective는 A 배열로 만들지만 `consumed_inputs`·`inputs_sha`는 다시 읽은 B를 기록한다. B로 정상 재실행한 Objective와 비교했다.

```text
두 실행의 consumed_inputs / inputs_sha = 동일
실제 Objective 전압 배열 최대 차이      = 0.020000000000000018 V
8개 고정 p의 rmse_pocv 최대 차이         = 0.01424704410442132 V
```

최적화 결과 차이를 주장한 것이 아니라 **실제 loader·Objective·고정 p 계산의 차이**를 측정했다.

**실제 `ne_shape.main()` 경로:** PE가 같은 A를 읽은 후 측정 workbook을 PE +20mV인 B로 교체하면 `pe_shape_max_mV=0.000000`이면서 B의 hash가 기록된다. 기록된 B로 정상 재실행하면 **20.000000mV**다. 두 번 모두 기록된 half-cell identity는 같다.

두 경로는 같은 구조와 수정 조건이므로 **P1 한 건으로 묶었다.** Matrix가 읽은 buffer 자체를 parse/hash하도록 고친 내부 F03은 재현 대조에서 닫혔다. 그 수정을 풀셀·half-cell 등으로 확장하지 않은 자리다.

**최소 닫힘 조건:** 입력별 immutable byte snapshot을 한 번 잡고 **그 bytes로 parsing과 hashing을 함께** 한다. 같은 workbook을 읽는 HalfCell·raw capacity 등도 snapshot을 공유한다. 로더가 소비한 identity를 반환받아 Objective·meta에 싣는다. 재-export가 위 두 경계에 끼어도 **A값/A서명, B값/B서명, 명시적 중단**만 허용해야 한다.

이 반례는 과거 보존 산출이 실제로 오염됐다는 증명이 아니다. 새 출처 기록이 “이 입력으로 계산했다”를 보증한다는 주장에 대한 반례다.

## 3. 새 P2 — 기록·정본 선택의 정확성

### R6-04 [P2 · 정본 선택] U14 새 산출이 있어도 실제 reader는 옛 `_v2`를 고른다

위치: [compare_states.py:26](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/compare_states.py:26), [36](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/compare_states.py:36). execution 재현의 `old_version_selected`는 **현재 커밋의 실제 out**을 그대로 읽는다.

```text
degeneracy_selected = degeneracy_300_0009_Li_v2.json
matrix_selected     = matrix_300_0009_v2.csv
선택된 두 파일의 unit 판정 = None, "meta 없음"
U14의 새 unversioned 두 파일의 unit 판정 = True, "일치"
```

“가장 높은 `_vN`” 규칙 때문에 U14 재생성 후에도 해당 상태는 옛 schema를 소비한다. 현재 공통 숫자는 동일하므로 **표 수치가 틀렸다는 발견은 아니다**. 새 서명·환경 필드를 가진 정본이 실제 소비 경로에 반영되지 않는다는 문제다.

최소 수정: 신규 정본/역사 산출을 구별하는 선택 규칙을 하나로 정리한다. 구판을 역사 위치로 옮기거나 명시적인 정본 목록을 사용하고, 독자가 선택한 파일명·run ID·입력 서명까지 시험한다. 파일의 수정 시각만으로 “최신”을 추정하지 않는다.

### R6-05 [P2 · 출처 분류] 정상 파일명 `out/a -> b.csv`를 코드 경로로 센다

위치: [provenance.py:89](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/provenance.py:89). claims 재현의 임시 Linux Git 저장소에서 rename이 아닌 정상 파일명 `out/a -> b.csv`의 수치 하나만 수정한다.

```text
git_dirty           = true
git_modified_code   = ["b.csv"]
git_modified_outputs에 실제 파일 누락
```

NUL porcelain으로 정확하게 읽은 경로를 후단의 `.split(" -> ")[-1].strip()`가 다시 훼손한다. 기존 한글 경로 반례는 고쳐진 것을 확인했다. 그와 다른 정상 경로 경계다.

최소 수정: NUL 레코드의 path 필드를 그대로 유지한다. 사람이 읽는 rename 표기로 다시 분해하거나 실제 경로의 앞뒤 공백을 제거하지 않는다.

### R6-06 [P2 · 실험 설정 설명] γ profile이 “적은 시작”이었다는 설명은 산출·실행 경로와 다르다

위치: [R6_REQUEST.md:117](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/reviews/R6_REQUEST.md:117), [R6_LEDGER.md:151](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/reviews/R6_LEDGER.md:151), 실제 [verify.py:1517](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/bms_balancing/verify.py:1517).

[inference 스크립트](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_inference_repros.py)의 `--case u14`로 구·신 산출과 계산 경로를 대조했다.

```text
각 γ의 requested random starts = 24
각 γ의 실제 n_tried             = 25
네 상태 84행 모두               = 25
실제 경로                       = best[:4] + random 24개, 4변수 L-BFGS-B
```

γ를 제거한 4변수 profile과 다른 mode의 SLSQP 등식 profile을 섞어 설명하고 있다. “다른 것은 24-start인데 γ profile은 적은 시작이어서 차이가 났다”는 비교 전제가 맞지 않는다.

최소 수정: 실제 예산 **γ당 25회**와 알고리즘을 적고 “적은 시작 때문에”라는 설명을 제거한다. 원인이 SciPy인가라는 U16의 미확정 상태는 그대로 둔다. 추가 실험은 multistart를 처음 넣는 것이 아니라 **기존 예산을 늘리는 실험**이다. 이것 자체가 §5의 집계를 반전시키지는 않는다.

## 4. 기존 조건 재판정

### R5 열한 조건

“원래 반례가 닫힘”과 “그보다 넓은 불변식도 닫힘”을 구별했다.

| R5 | R6 판정 | 근거 |
|---|---|---|
| 01 `%g` 반올림 구간 | 원래 반례 닫힘 | 영점·decade·0자리 오류 거부, 정상 반올림 통과 |
| 02 선언·앵커 역할 | 닫힘 | 중복 선언·비숫자 앵커 invalid/2, V6 관련 추가 대조도 작동 |
| 03 parameter 이름 | 닫힘 | 이름 교환 invalid/2, 비교 0 |
| 04 결과/meta 소유 | **부분** | 원래 경쟁·stdout inode 수정은 막음. 소비 snapshot·최초 미완은 R6-01·02 |
| 05 실제 소비 입력 | **부분** | 선택 matrix와 untracked 입력 hash는 남음. 읽은 입력/사후 hash의 불일치는 R6-03 |
| 06 scale 충분조건 | 닫힘 | tiny·zero·Inf·NaN·exception을 동치로 표시하지 않음. U13과 raw192의 범위 분리도 인정 |
| 07 matrix 감사 배선 | 닫힘 | 실제 cmd_matrix에서 target만/기준만 Inf36을 각각 기록하고 소비 scale과 대조 |
| 08 단일 run ID·필드 검사 | 원래 반례 닫힘 | 명령 ID 고정·필드 검사 회귀 통과. 현재 경쟁은 서로 다른 정상 ID로도 발생 |
| 09 U12 범위 | 정정 닫힘 | 보고 순서/측정 범위 한정. U13의 18줄·54 metric도 확인 |
| 10 예외 표본 개수 | 닫힘 | 둘째 metric에 예외 50회: 각 metric n=50, 실패 항 n_exception=50 |
| 11 한글 경로 분류 | 원래 반례 닫힘 | 한글 출력 정확히 분류. 다른 경로 문법의 문제는 R6-05 |

내부 F03의 **matrix buffer parse/hash 동일성**, V6의 확인한 schema·정밀도 방어, DF-01·03·05·07 등의 과장 정정, U14의 LF 게시·보존 수치 대조를 인정한다. 이미 고친 항목을 새 발견 수에 넣지 않았다.

### R3 §5의 다섯 GO 조건

| 조건 | 재판정 |
|---|---|
| 1 원인·표현 주장 | **신고 범위에서 닫힘**. 원인·전역 수렴을 관측으로 낮춘 정정 인정. 예산 설명 R6-06은 정리 필요 |
| 2 표의 identity | 분모·역할·소스 집합의 기존 정정은 유지. **현행 소비 경로는 부분**: R6-01·03·04 |
| 3 비교 성공 조건 | **검토한 지원 범위에서 닫힘**. 36개 대조에서 새 잘못된 수치 일치 인증 없음. 충돌 문구는 아래 Q3 |
| 4 실행 결과 소유 | **안 닫힘**. R6-01·02·03 |
| 5 기록을 지키는 시험 | **192 원시값 조건은 닫힘 유지**. 새 snapshot 조건은 별도 회귀 필요 |

## 5. 유지된 수치 근거와 질문 여섯 개

### 유지된 근거

U14 대조는 새 unversioned 산출 12개를 명시적으로 읽었다. R6-04의 자동 선택 오류와 섞지 않았다.

| 직접 대조 | 결과 |
|---|---|
| matrix 공통 수치 | **2,240셀 전부 정확히 동일** |
| degeneracy 세 mode span × 네 상태 | **12개 전부 정확히 동일** |
| γ profile | 84행 중 일부 변동. state100·γ=.125의 LAM_NE 최대 차이 약 **0.281136 %p** |
| FINDINGS §5 표 | 35개 수치가 현재 CSV의 해당 반올림 자리와 일치 |
| §5-1 문턱 | n=6/10/12/13 및 γ 범위 동일. 폭·최악 비는 **문서 인쇄 자릿수에서 동일** |

“표의 숫자가 모두 원시 float까지 같다”는 뜻은 아니다. 예를 들어 10mV 문턱의 LAM_NE 폭은 `13.585981898 → 13.585947105 %p`다. 보존된 두 실행의 해당 기술 집계가 안정적이라는 증거이며 모든 환경·seed의 보증은 아니다.

### Q1. 현재 게시 규약으로 동시 실행을 허용해도 되는가?

**현재 구현으로는 ‘마지막 온전한 묶음’ 및 그 묶음의 소비를 주장할 수 없다.** 고유 임시파일/잠금 수정은 유효하지만 R6-01·02가 남았다. 동시 실행을 원천 금지해야만 하는 것은 아니다. 완성 묶음을 한 번에 게시하고 독자가 그 snapshot을 소비하게 하면 된다.

충돌 시 거부를 택해도 이미 열린 독자와 단일 시도의 crash 문제는 별도다. 단순한 “동시 writer 거부”만으로 R6-01·02의 모든 조건이 닫히지는 않는다. 마지막 정상 묶음을 crash 후에도 유지하겠다면 시도별 불변 data/meta 묶음과 하나의 원자적인 선택 지점 등으로 그 보존 성질을 시험해야 한다.

### Q2. 공개 run ID를 복사하는 producer까지 막아야 하는가?

**현재 선언한 ‘각자 다른 UUID를 쓰는 정상 시도’ 경계에서는 추가 GO 전제로 만들지 않는다.** 이번 P1은 그 경계 안에서 재현된다.

producer가 **자기 보관 bytes의 digest**를 전용 결과로 넘기고 wrapper가 그 bytes와 대조하는 방식은 정상 시도 간 착오를 줄이는 데 유용하다. 다만 digest 전달은 동일성 증거이지, 비신뢰 producer의 신원·정직성을 인증하는 증거는 아니다. 그런 다른 목표로 이번 리뷰를 확대하지 않았다.

### Q3. 옵션/선언 규칙에 역전이 남았는가?

내부 V6-02의 긴 토큰/옵션 사례는 invalid/2가 되고, 유효한 짧은 토큰 대조는 complete/0였다. 확인한 사례에서는 옛 수치 오인증이 재현되지 않았다.

다만 “충돌이면 항상 partial”이라는 문구는 실제와 다르다. `%.17g` 선언·`fixed:1` 옵션에서 `.125`와 `.125`는 conflict=true지만 complete/0, `.125`와 `.126`은 partial/3이다. 코드는 **옵션이 실제 차이를 선언보다 더 흡수했을 때** partial을 준다. 전자는 엄격한 선언으로도 같은 값이라 새 수치 오인증으로 세지 않았다. 현재 의미를 문서에 적거나 정책을 무조건 충돌 거부로 통일하면 된다.

### Q4. 끝점 재확인만으로 1.0832를 인용해도 되는가?

**탐색 하한으로는 가능**하다. 독립 수렴이라는 주장을 철회한 것은 타당하다. 동일 끝점을 넣은 격자를 독립 재발견으로 세지 않는 한, 힌트 없는 재실행은 그 제한된 하한 인용의 필수조건이 아니다.

이 환경에서 endpoint의 목적함수를 원자료로 재계산하지는 않았다. endpoint parameter·J·limit·제약 잔차를 함께 보존하면 하한 witness의 직접 검토가 더 쉬워진다. 정확한 폭·신뢰구간·전역 수렴으로 확대해서는 안 된다.

### Q5. γ profile이 움직였어도 §5·§5-1을 인용해도 되는가?

**현재 인쇄 정밀도의 기술 집계는 인용 가능**하다. 실제로 재대조했다. 정확한 γ별 parameter·분기 위치·최적점 안정성을 주장하려면 추가 seed/예산 실험이 필요하다. 현재도 γ당 25회이므로 “multistart가 없어서”로 설명하지 않는다. 원인 분리 U16은 신고된 미결로 유지한다.

### Q6. 다섯 관측을 새 모델 요구서에 넣어도 되는가?

**다음 한정어를 붙인 관측 열은 지금 작성해도 된다.**

1. 포팅: 보존 네 조합 192값의 경험적 일치, 사용자 원본 식 대조, scale 상대근사는 서로 다른 증거 층.
2. 음수 LAM_NE: 공개 5행·고정 기준의 부호 산술. 경계 변경 재적합의 인과는 미확립.
3. 파우치 폭: 해당 네 상태·소스·설정의 탐색 하한 순위. 정확도/식별성 보증 아님.
4. 원통형·PE: 집합·분모·`raw max/max 10.5`라는 통계량을 함께 적은 기술값.
5. 잔차·γ: 선택된 쌍과 고정 reference의 표집·진폭 증인 및 끝점 재확인. 원인·보상 경로·모양 적합의 증명 아님.

이 관측은 후보 모델과 **구분 실험**을 설계할 출발점이다. 특정 새 전극 표현이 필요하거나 옳다는 결론은 그 실험에서 별도로 채택해야 한다.

## 6. 닫는 순서와 재현

GO 전 최소 조건은 아래 **세 개**다. P2는 위 최소 수정대로 기록·선택 정확성을 정리하되, 수치 결론 반전과 동일시하지 않는다.

1. **R6-01:** 반환된 표/후속 입력이 검증한 동일 data·meta snapshot만 소비한다.
2. **R6-02:** 현행 산출의 metadata 미완을 legacy 완료로 소비하지 않는다.
3. **R6-03:** 계산 입력과 기록한 hash가 동일 bytes에서 나온다.

세 조건 모두 “검사를 지우면 시험이 실패한다”만 보지 말고, 이 보고서의 실제 파일 교체·최초 게시 중단 순서에서도 허용 결과가 A/A·B/B·명시적 미완으로 제한되는지 시험해야 한다.

통합 재현은 ZIP을 풀어 스크립트들을 같은 디렉터리에 두고, 의존성을 설치·활성화한 Linux/WSL 환경에서 실행한다. Git checkout은 정확한 대상 SHA여야 하며 `bfc4623^` 이력도 있어야 한다.

```bash
python /path/to/review/harness_r6_final_replay.py \
  --target /path/to/d431404/bms-balancing \
  --output /tmp/r6-review.json
```

구판 out을 미리 Git archive로 추출했다면 `--old /path/to/bfc4623-parent/bms-balancing/out`을 추가한다. 재생은 대상 소스를 고치지 않는다. 이 환경에서는 Windows Git의 alternate 경로 때문에 native Git으로 구판 ZIP을 추출한 후 이 옵션을 사용했다.

큰 유한 값(`1e308`)으로 comparator/scale helper에 생기는 overflow도 관측했지만, 실제 raw-RMSE가 그 크기를 생산하는 경로는 입증하지 못했다. **합성 Objective stress를 production 반례로 바꿔 세지 않았다.** F08·F2·U16·U2~U10 같은 신고 경계도 발견 수에 재합산하지 않았다.

**최종 NO-GO — 출처 결속 세 조건을 먼저 닫는다. 다섯 관측을 한정한 설계 요구서 초안은 병행 가능하다.**

## 첨부 구성

- [통합 재생](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_replay.py) · [stdout/stderr 원문·환경·SHA 기록](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_replay_results.json)
- [결과 소비 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_execution_repros.py)
- [입력/출처 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_claims_repros.py) · [담당 보고](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_claims_review.md)
- [수치/추론 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_inference_repros.py) · [담당 보고](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_inference_review.md)
- [비교기 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_port_repros.py) · [담당 보고](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_port_review.md)

담당 보고서의 번호는 분야별 번호다. 최종 발견 집계·심각도·GO 조건은 **이 문서의 R6-01~06**이 정본이다.

