# R6 최종 정본 독립 검토 — d431404

대상: `d4314048c63605fb4613f8b0a91859271fddda98`, `work/harness-r6-d431404/bms-balancing`.
`R6_REQUEST_d431404.md`를 완독하고 새 소스를 읽은 뒤 다시 실행했다. **1049894 판의 발견을 자동 합산하지 않는다.** 아래 결과가 이 담당 범위의 최종 검토다.

재현: [harness_r6_final_claims_repros.py](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r6_final_claims_repros.py).

```text
python outputs/harness_r6_final_claims_repros.py --target work/harness-r6-d431404/bms-balancing
exit code 0
target d4314048c63605fb4613f8b0a91859271fddda98
```

Python 3.12.3·numpy 2.5.3·scipy 1.18.1·pandas 3.0.5/WSL에서 실행했다. 실제 workbook/CSV 로더, HalfCell, Blend, `build`, Objective, `ne_shape.main`을 사용했다. 모든 자료는 임시 디렉터리의 합성 수치이며 optimizer는 돌리지 않았다. 파일 export가 특정 읽기 경계에서 완료되는 순서를 hook으로 고정했다. 대상 코드와 실제 원자료는 수정하지 않았다.

## 1. P1 — F03은 닫혔지만 같은 byte 결속이 `build.inputs_sha`와 다른 측정 입력에는 없다

문제의 핵심은 파일 누락이 아니다. **계산은 A의 배열을 쓰는데 `consumed_inputs`·`inputs_sha`는 나중에 그 pathname에 있는 B를 가리킨다.** 다음 두 경로는 같은 최소 수정 조건이므로 한 P1으로 묶는다.

### 1a. 새 F4 `build`의 풀셀 입력 서명 — 동일한 inputs_sha, 다른 실제 전압과 RMSE

위치:

- [verify.py:174](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/bms_balancing/verify.py:174): 풀셀 workbook에서 c/v 배열을 읽는다.
- [verify.py:175](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/bms_balancing/verify.py:175): 그 배열로 Objective·scale을 계산한다.
- [verify.py:184](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/bms_balancing/verify.py:184): 이후 pathname을 다시 읽어 full-cell SHA를 기록한다.
- [verify.py:190](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/bms_balancing/verify.py:190): 이 기록으로 inputs_sha를 만든다.

재현 상태: 저장소의 `matlab/tests/gen_synth_xlsx.py`로 실제 로더가 읽는 합성 workbook 트리를 만든다. `build(..., GITT, 200, Li, w_dqdv=1, seed=0)`의 실제 `load_full_cell`이 A 배열을 반환하기 직전에, 200 상태 전압만 +20mV한 새 workbook B를 원자적으로 같은 pathname에 게시한다. 읽은 배열은 수정하지 않는다. 이후 같은 B로 정상 build도 한 번 실행한다.

관측:

```text
교체 경계 실행의 실제 voltage 배열 = 원래 A와 완전히 동일
교체 경계 실행의 consumed_inputs   = 정상 B 실행의 consumed_inputs
교체 경계 실행의 inputs_sha        = 정상 B 실행의 inputs_sha
두 Objective의 실제 전압 최대 차이 = 0.020000000000000018 V
8개 고정 p에서 rmse_pocv 최대 차이  = 0.01424704410442132 V
```

현재 새 서명은 B workbook을 정확히 hash했지만 **B로 계산하지 않은 Objective에도 그 서명을 붙였다**. 실제 입력 snapshot identity라는 목적을 달성하지 못한다. 20mV 차이는 실제 CSV/workbook 로더와 Objective에서 관측했다. 이것은 고정 파라미터 평가이며 최적화 결과 차이를 실측했다는 주장은 아니다.

### 1b. 최신 `ne_shape`의 half-cell 기록도 같은 순서다

위치: [ne_shape.py:229](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/ne_shape.py:229)에서 HalfCell을 읽고, 234에서 raw capacity, 235에서 문헌을 읽은 뒤 [248](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/ne_shape.py:248)부터 `_input_identity()`로 파일을 재개방한다.

합성 pristine/100 워크북을 실제 HalfCell로 읽힌다. 모든 half-cell 및 capacity 읽기가 끝난 뒤, 문헌 로더가 반환하는 경계에서 target의 PE만 +20mV한 workbook B를 게시한다. 그 상태로 실제 `ne_shape.main()`이 성공한다.

```text
결과 pe_shape_max_mV                       0.000000
consumed_inputs.100.half_cell               B의 경로·hash
기록한 B로 정상 재실행 pe_shape_max_mV       20.000000
두 실행에 기록된 half-cell identity         완전히 동일
```

CSV와 meta의 게시 잠금이 있어도, 게시 전 이미 **A 수치 + B 입력 표식**이 만들어졌으므로 이 오류는 막지 못한다. Publisher/reader의 묶음 경주와는 별개인 계산 입력 결속 문제다.

### 최소 수정·닫힘 조건

Matrix에 적용한 F03과 같은 원칙을 다른 입력으로 확장한다. 입력별 byte snapshot 하나를 읽고, **그 동일한 bytes**로 파싱·hash를 수행한다. HalfCell와 raw capacity처럼 같은 파일의 여러 소비자도 동일 snapshot을 공유한다. Objective에 붙는 `consumed_inputs`는 로더가 실제 소비한 snapshot에서 반환받는다.

최소 회귀 조건은 위 두 경계에서 재-export가 일어나도 다음 셋 중 하나뿐이어야 한다는 것이다: **A 값/A 서명, B 값/B 서명, 명시적인 중단**. A 값/B 서명의 성공은 없어야 한다. 이 반례는 과거 실제 자료가 잘못 기록됐다는 증명이나 모든 관측값 무효화가 아니라, 새 출처 서명의 재현성 보장에 대한 반례다.

## 2. P2 — 새 NUL 경로를 후단의 옛 `" -> "` 처리로 다시 훼손한다

위치: [provenance.py:89](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r6-d431404/bms-balancing/scripts/provenance.py:89).

Linux 임시 git 저장소에서 **rename이 아닌 정상 이름** `out/a -> b.csv`를 커밋하고 숫자 하나만 수정한다. NUL porcelain은 정확한 이름을 반환하지만 `.split(" -> ")[-1].strip()`가 이를 `b.csv`로 잘라낸다.

```text
실제 추가 변경 출력      out/a -> b.csv
보고 git_dirty          true
보고 git_modified_code  ["b.csv"]
보고 modified_outputs   실제 arrow 파일 누락
```

기대값은 원래 이름이 출력 변경 목록에 있고 코드 변경은 없다는 것이다. 이 경로는 Linux/WSL에서 정상 파일명이다. 수치 오염이 아니라 provenance의 코드/출력 역할 오진이므로 P2다.

최소 수정: NUL 레코드에서 얻은 path를 그대로 사용한다. 다시 사람이 읽는 porcelain 문자열로 합쳐서 옛 rename 구분자로 나누거나 실제 경로 양끝의 공백을 `strip()`하지 않는다.

## 3. 새 커밋에서 실행으로 인정한 닫힘

- **내부 F03**: 실제 `fitted_pair_info`가 A bytes를 읽어 `StringIO`를 만든 뒤 pathname을 B로 교체했다. 반환 γ는 .16이고 hash도 **A**였다. 현재 pathname은 B여도 계산값과 hash는 같은 snapshot이므로 닫혔다. 구판의 matrix read/hash 반례는 이번 발견 목록에서 제외한다.
- **R5-05의 고정 v2 선택**: tracked matrix_100.csv(.16) 뒤 untracked matrix_100_v2.csv(.45)를 추가하면 실제 선택 파일·서로 다른 올바른 hash를 남긴다. 원래의 untracked 입력 누락은 닫혔다.
- **R5-11의 한글 경로**: `out/측정.csv` 수정은 `git_dirty=false`, 출력 목록에 정확한 이름, 코드 목록 빈 배열이다. Unicode quoted-path 수정 자체는 닫혔다.
- **풀셀의 역할**: `ne_shape` 직접 실행은 풀셀 폴더 없이 성공했다. 반면 위 실제 `build`는 풀셀을 소비하므로 full-cell identity 추가 자체는 타당하다. 둘을 혼동해 "ne_shape의 직접 입력 누락"으로 보고하지 않는다.

## 4. 출처·γ·다섯 관측 Q6의 범위

최종 FINDINGS의 S-02와 γ 한정은 유지된다(1385–1396): 100의 두 Δγ는 같은 방향이고 크기가 약40배, 200은 반대, 증인 없음은 선택 ref 고정·501×400 표집 기준이며 정규화 후 진폭과 모양 일치가 다르다. 이 설명을 뒤집는 새 결과를 찾지 못했다.

FINDINGS의 `raw max/max 10.5배`와 상태별 비의 분리, §0-1의 보존 192 출력 경험적 일치 한정, §3-4의 독립 수렴 철회는 내부 정정으로 인정한다. 그 정정문을 다시 발견으로 세지 않는다. 다섯 관측을 요구서에 옮길 때는 고정 기준 산술·탐색 하한·명시 분모·원인 미확정의 한정어를 그대로 보존해야 한다. Profile의 새 수치와 scale 비교기의 상세 판단은 다른 담당 검토 범위다.

`ne_shape.py` 386–387의 "다른 γ에서도 잔차가 남는지는 (d)의 증인 열"이라는 문장과 옛 인과 주석은 계속 남아 있다. 이는 R5부터 알려 준 **Q6 문구 정리 권고**로만 유지하며 새 P1로 합산하지 않는다. (d)는 진폭 존재만 말하므로 "다른 γ에서의 모양 잔차는 직접 제약 적합 등 별도 시험이 필요하다"가 맞다. U9·S-04·U16 등 신고한 미결의 존재도 새 발견으로 다시 세지 않았다.

본 담당의 새 발견은 **P1 한 조건(두 실제 입력 경로) + P2 한 조건**이다. GO는 새 모델 설계 요구서의 근거 적합성을 뜻하며 본 실행 승인·외부 배포 승인·연속 모델 가족의 전역 증명이 아니다.
