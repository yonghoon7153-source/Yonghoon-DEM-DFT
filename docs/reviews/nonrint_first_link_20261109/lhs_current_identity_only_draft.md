# LHS O1 — 현재 덱 한 파일의 신원 수령 명령 초안

**O1 선택 승인 수령 / 문서 초안만 / 명령 실행·시험·구문 검사 없음 / 실행 당시 신원 NOT_ESTABLISHED / 전체 HOLD.** 1저자는 O1을 권고대로 선택했다. 기존 Q1의 제공자=1저자(WSL)와 비결과 범위 비준을 재질문하지 않는다. 이 문서는 1저자가 실제 대상·예산을 확인한 뒤 WSL에서 사용할 새 초안이며, 이번 작성 중에는 파일 접근이나 명령 실행을 하지 않았다. Q2 실제 정본/구간·A/C, Q3 실제 동결, Q4 값 GO는 계속 미승인이다.

## 1. 근거와 이전 초안의 구분

| 근거 | 이번 문서에서 쓰는 범위 |
|---|---|
| 최신 확인 B `e91bd1c94` | 이 작업의 원격 B 바탕. 예고된 19:00 대응표/반입 핀은 확인하지 않은 것으로 두며 추정하지 않음 |
| `476e736e2`, `docs/reviews/lhs_q1_remaining_options_20261109.md` §3 O1; 이 가지의 원문 사본 `b492a2062` | 현재 덱의 별칭·종류·크기·SHA256·관측 시각만 받는 제안. 그 문서의 당시 ‘미선택’은 역사 상태이며 이번 사용자 O1 선택이 후속 결정 |
| `6b9d8e149170`, `docs/reviews/nonrint_approved_preparation_20261109/lhs_nonresult_intake_form.md` §1–3·§6; 이 가지의 원문 사본 `43eb8a28c` | Q1 담당·비결과 범위, 현재 hash와 실행 당시 사용의 구분, Q2–Q4 미승인 경계 |
| `9c061aafd083`, `docs/data/lhs_wsl30_inventory_20261108/README.md` §「무엇을 누가 했는가」·§「충족한 재고 계약」 | WSL30 라벨 `lhs00_100`–`lhs00_129`. 아래 라벨 검사는 이 범위의 문자열 검사이며 실제 파일/실행/적격 표본과의 연결을 인증하지 않음 |

기존 `lhs_wsl_readonly_command_draft.md`는 실행 영수증·17키 메타 사본 전제가 미충족돼 **미실행**인 채 보존한다. 이번은 목적이 다른 **CURRENT_IDENTITY_ONLY** 초안이다. 실행 영수증, 과거 기대 SHA, 17키 사본을 요구하거나 만들어 채우지 않는다. 현재 SHA를 과거 봉인/영수증으로 소급하는 우회도 아니다.

## 2. 지정 대상과 출력의 뜻

한 번에 1저자가 지정한 **현재 덱 정규 파일1개**만 읽는다. 승인한 작업 디렉터리 안의 상대경로를 로컬 명령 사본에 적으며, 실제 기계 위치·주소·포트는 리포나 전달 결과에 넣지 않는다. WSL30 전체 자동 순회, 추가 파일 검색, include/restart/dump/STL/로그/done/표 열람, 덱 실행·해석은 하지 않는다.

| 출력 | 의미 | 증명하지 않는 것 |
|---|---|---|
| `alias=current_deck_<WSL30 label>` | 1저자가 선언한 케이스의 안전한 수령 별칭 | 파일 내용·실제 실행에 의해 확인한 case/run/segment 아님 |
| `kind=deck` | 1저자가 지정한 역할 | 내용을 읽어 덱 종류·문법·실제 사용을 인증하지 않음 |
| `bytes`·`sha256` | 지정 파일의 현재 바이트 길이와 SHA256 | 실행 당시 입력 신원, include 폐쇄, 재개 사슬, 원로그 신원 아님 |
| `observed_utc` | 해시·변경 점검을 마친 때의 WSL 시계 UTC | 파일 생성/실행 시각, 독립적으로 인증된 시간 아님 |
| 상태·rc | 현재 신원 한정 출력과 프로세스 완료 여부 | 실제 정본/동결/값 GO·과학 자격의 승인 아님 |

hash 계산은 파일 바이트를 읽지만 내용을 출력·파싱하지 않는다. 역할/파일 매핑은 1저자가 기존에 확인한 비결과 목록으로 지정하며, 명령은 원로그 또는 덱 본문을 검사해서 그 지정을 인증하지 않는다.

## 3. 1저자 확인과 중단 조건

- `lhs_case`, `lhs_deck`, 시간·파일 크기 예산을 실제 범위로 정한다. `lhs_confirm` 문자열은 그 지정 확인을 위한 실수 방지란이며 승인 토큰이나 추가 Q1 비준이 아니다. placeholder가 남으면 중단한다.
- 지정 작업 디렉터리와 파일을 다른 작업이 바꾸지 않는 창을 확보한다. 기존 경로 구성요소의 symlink는 거부한다. 작업 디렉터리/그 상위의 신뢰·권한은 1저자가 확인한다. 링크·bind mount·적대적 경합 전부를 방어하는 도구가 아니다.
- 파일당 양의 바이트 상한을 확인한 뒤 읽는다. 현재 파일 하나를 두 번 해시하므로 읽는 총 바이트 수가 파일 크기 한 번과 같지는 않다. 파일 수 범위는 여전히1개다. 변경 점검의 내부 stat 값은 출력하지 않는다.
- `lhs_term_seconds`는 **내부 작업에 TERM을 보내는 시한(초)**이다. 종료하지 않으면 최대 추가5초 뒤 KILL을 요청한다. 바깥 준비/출력 전달·커널 응답까지 포함한 엄밀한 전체 소요시간 보장은 아니다. 시간/크기 한도는 1저자가 정하는 작업 예산이며 과학 합격선이 아니다.
- 접근/해시/변경 점검 실패, 시간 초과, Ctrl-C 또는 출력 단절은 완료가 아니다. 성공 전까지 stdout을 보류한다. 자동 재시도·원본 수정·복구·새 manifest 생성은 없다. 예산을 바꾸거나 다른 파일로 진행할 때도 범위와 변경 여부를 다시 확인한다.

## 4. ASCII 명령 블록 — 미실행 초안

POSIX `sh`와 WSL의 `timeout`, `stat`, `sha256sum`, `date`를 전제로 한 문서다. 구문 검사나 합성 실행으로 확인한 코드가 아니다. 실제 경로는 이 문서에 채우지 않고, 1저자가 실행할 로컬 사본에서만 상대경로로 지정한다. 원본에 쓰는 명령이나 새 결과 파일 생성은 없다.

```sh
(
set -fu
LC_ALL=C
export LC_ALL
lhs_term_seconds='REPLACE_POSITIVE_SECONDS'
case "$lhs_term_seconds" in ''|*[!0-9]*) printf '%s\n' 'STOP: set a positive TERM deadline in seconds' >&2; exit 2;; esac
[ "${#lhs_term_seconds}" -le 6 ] && [ "$lhs_term_seconds" -gt 0 ] || exit 2
command -v timeout >/dev/null 2>&1 || exit 2
lhs_output=$(
timeout --signal=TERM --kill-after=5s "${lhs_term_seconds}s" sh <<'LHS_CURRENT_IDENTITY_ONLY'
set -fu
lhs_confirm='NO'
lhs_case='REPLACE_WSL30_CASE_LABEL'
lhs_deck='REPLACE_CURRENT_DECK_RELATIVE_PATH'
lhs_max_file_bytes='REPLACE_POSITIVE_BYTES'
stop() { printf '%s\n' 'STOP: target, budget, access or change check unresolved' >&2; exit 2; }
[ "$lhs_confirm" = 'AUTHOR_CONFIRMED_CURRENT_DECK_AND_BUDGET' ] || stop
case "$lhs_case" in lhs00_1[012][0-9]) ;; *) stop;; esac
case "$lhs_max_file_bytes" in ''|*[!0-9]*) stop;; esac
[ "${#lhs_max_file_bytes}" -le 12 ] && [ "$lhs_max_file_bytes" -gt 0 ] || stop
for lhs_tool in stat sha256sum date; do command -v "$lhs_tool" >/dev/null 2>&1 || stop; done
check_deck() {
  case "$lhs_deck" in ''|REPLACE*|/*|-*|*..*|*//*|*[!A-Za-z0-9_./-]*) stop;; esac
  lhs_part=''
  lhs_saved_ifs=$IFS
  IFS=/
  for lhs_component in $lhs_deck; do
    lhs_part=${lhs_part:+$lhs_part/}$lhs_component
    [ ! -L "$lhs_part" ] || stop
  done
  IFS=$lhs_saved_ifs
  [ -f "$lhs_deck" ] && [ -r "$lhs_deck" ] || stop
  lhs_bytes=$(stat -c '%s' -- "$lhs_deck" 2>/dev/null) || stop
  case "$lhs_bytes" in ''|*[!0-9]*) stop;; esac
  [ "$lhs_bytes" -le "$lhs_max_file_bytes" ] || stop
}
hash_deck() {
  lhs_hash_line=$(sha256sum -- "$lhs_deck" 2>/dev/null) || stop
  printf '%s' "${lhs_hash_line%% *}"
}
check_deck
lhs_before=$(stat -c '%d:%i:%s:%y:%z' -- "$lhs_deck" 2>/dev/null) || stop
lhs_size=$lhs_bytes
lhs_hash=$(hash_deck) || stop
check_deck
[ "$lhs_size" = "$lhs_bytes" ] || stop
[ "$(hash_deck)" = "$lhs_hash" ] || stop
lhs_after=$(stat -c '%d:%i:%s:%y:%z' -- "$lhs_deck" 2>/dev/null) || stop
[ "$lhs_before" = "$lhs_after" ] || stop
lhs_observed_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null) || stop
printf 'alias=current_deck_%s\nkind=deck\nbytes=%s\nsha256=%s\nobserved_utc=%s\n' "$lhs_case" "$lhs_size" "$lhs_hash" "$lhs_observed_utc"
printf '%s\n' 'record_type=CURRENT_IDENTITY_ONLY' 'execution_identity_status=NOT_ESTABLISHED' 'origin_execution_proven=false' 'value_access_go=NONE' 'whole_gate=HOLD'
LHS_CURRENT_IDENTITY_ONLY
)
lhs_rc=$?
if [ "$lhs_rc" -ne 0 ]; then
  printf 'STOP: command_rc=%s; partial or timed-out work is not complete; no automatic retry\n' "$lhs_rc" >&2
  exit "$lhs_rc"
fi
printf '%s\n' "$lhs_output"
printf '%s\n' 'command_rc=0'
)
```

## 5. 수령 기록과 다음 경계

1저자는 완전한 stdout와 실제 프로세스 rc를 전달한다. 별칭에 대응하는 로컬 경로는 현장에 보존하고 전달 결과에는 넣지 않는다. 다른 파일이나 원문을 붙이지 않는다. 완전 출력/rc0가 없으면 `NOT_RECEIVED` 또는 실패/부분 상태로 기록하며 실제 hash 값을 추정하지 않는다.

Codex는 그 결과를 **현재 바이트 신원 관측**으로만 받는다. 현재 이 문서의 실제 별칭·크기·SHA·관측 시각은 모두 미수령이며 생성하지 않았다. 앞뒤 stat·재해시는 발견한 변경을 거부하기 위한 제한된 점검으로, 원자적 snapshot이나 실행 당시 바이트의 증명이 아니다.

기존 영수증 미확보와 실행 신원 `NOT_ESTABLISHED`는 O1 출력 성공 뒤에도 유지한다. 두 로그의 헤더/step·연결/겹침, done 기록의 역사 출처, 실제 include/재개 사슬은 이 블록의 출력이 아니다. O2/O3를 선택·수행하거나 기존17키 사본을 대신한 것으로 보지 않는다. Q2–Q4는 다시 묻거나 자동 승인하지 않으며, 현재 덱 hash로 정본·동결·값 GO를 결정하지 않는다. 전체 HOLD를 유지한다.
