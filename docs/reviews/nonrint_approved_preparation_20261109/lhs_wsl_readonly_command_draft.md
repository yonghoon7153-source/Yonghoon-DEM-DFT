# WSL30 비결과 수령용 읽기 전용 명령 초안 — 미실행

**문서 초안 / 실행·시험·구문 검사 없음 / 1저자 명령 확인 전 / 전체 HOLD.** Q1 제공자=1저자(WSL)와 비결과 신원·구간·겹침/노출 메타 범위는 비준됐다. 실제 파일 매핑·출처·예산을 1저자가 확인한 뒤 본인이 실행할 초안이며, Codex 실행 지시가 아니다. Q2 실제 정본/A/C, Q3 실제 동결, Q4 값 GO는 미승인이다.

기준과 수령 표는 [lhs_nonresult_intake_form.md](lhs_nonresult_intake_form.md) §1–6을 따른다. 결정표 `b7ec640bc216`, `docs/reviews/nonrint_next_decisions_20261109.md` §5「LHS」 Q1의 구체화다. 기존 실행 당시 봉인/영수증과 현재 신원의 분리 계약을 재사용하며 새 원로그 판독기를 구현하지 않는다.

## 1. 한 번에 읽을 고정 대상과 중단 조건

이 초안은 1저자가 이미 알고 지정한 안전한 작업 디렉터리를 기준으로 **상대경로로 지정한 입력 역할 3개만** 읽는다. 서로 다른 파일시스템 객체 3개임을 인증하는 것은 아니다. 디렉터리 위치를 출력하지 않는다. 자동 탐색·목록 재귀·WSL30 전체 반복·네트워크·전송·결과 파일 생성은 없다. 허용 라벨 `lhs00_100`–`lhs00_129`는 `9c061aafd083:docs/data/lhs_wsl30_inventory_20261108/README.md` §충족한 재고 계약에 근거하며, 라벨 일치만으로 실제 파일의 실행 신원을 확정하지 않는다.

| 별칭 | 대상 | 허용된 처리 |
|---|---|---|
| `execution_receipt` | 이미 승인된 비결과 실행 당시 봉인/영수증 사본 | 현재 파일 길이·SHA256만. 실행 당시 SHA/연결은 1저자가 이 영수증의 기존 허용 메타를 수령 표에 별도 기입 |
| `boundary_metadata` | 이미 승인된 두 로그 비결과 메타 사본 | 기존 고정 SHA 대조 후 아래 허용 키만 출력. 원로그를 입력으로 삼지 않음 |
| `current_input` | 명시적으로 지정한 deck/include/restart 한 파일 | 종류·현재 길이·현재 SHA256만. 실행·내용 출력·해석·의존 자동 확장 없음 |

현재 입력 한 파일의 SHA 수령은 전체 입력/재개 사슬 대조 완료가 아니다. 추가 파일은 실제 목록과 예산을 확인한 별도 범위로만 다룬다. 자동 반복/재시도는 없다. 시간·파일 크기 예산은 1저자가 정하며 과학 합격선이 아니다. 원본과 사본을 변경하지 않는 창을 먼저 확보한다. 아래 링크 검사·재해시가 적대적 동시 변경이나 bind mount의 범용 방어를 보증하지 않는다.

`execution_receipt`와 `boundary_metadata`의 기대 SHA는 이미 승인된 출처에 있어야 한다. 확인되지 않은 사본을 먼저 열거나 현재 SHA만 복사해 기대값을 만들지 않는다. SHA 일치는 바이트 결속 확인이며 승인자 진위·실행 당시 사용·실행 연속성의 증명이 아니다. **헤더·step의 비결과 메타는 이미 허용됐으며**, 1저자가 그 출처·사본·고정 해시로 제공한다. 원로그 본문 제외를 지키기 위해 **이 명령은 원로그에서 헤더·step을 자동 추출하지 않는다**. 사본/고정 SHA/필수 메타가 없으면 UNKNOWN/STOP이고 실행 신원은 미확정이다. 허용 메타 자체의 금지가 아니라 이 초안의 수령 방식 한계이며, 압력 열을 지나가며 원로그를 파싱하는 우회는 하지 않는다.

## 2. 허용 메타 사본의 좁은 형식

이미 승인된 사본이 아래 **17행 TSV(key, TAB, value)** 형태인 경우만 명령 출력 대상으로 삼는다. 이는 수령 출력의 제한이며 새로운 저장소 등록 schema가 아니다. 기존 형식이 다르면 이 초안으로 변환하거나 원로그에서 생성하지 않고 STOP 후 기존 자료 형식과 허용 범위를 따로 제시한다. 이 조건 때문에 출처가 아직 없는 케이스는 자동 수집되지 않는다.

- 허용 키: `scope_id`, `case_id`, `receipt_ref`, `log_a_identity_ref`, `log_a_run_id`, `log_a_segment_id`, `log_a_header_ref`, `log_a_first_step`, `log_a_last_step`, `log_b_identity_ref`, `log_b_run_id`, `log_b_segment_id`, `log_b_header_ref`, `log_b_first_step`, `log_b_last_step`, `restart_parent_ref`, `restart_child_ref`.
- 모든 키가 정확히 한 번 있어야 한다. 값은 안전한 ASCII 별칭 또는 `UNKNOWN`; step 두 종류는 음이 아닌 정수 문자열 또는 `UNKNOWN`만 받는다. 양 로그의 run/segment가 같다고 가정하지 않는다. `scope_id`·`case_id`는 1저자가 지정한 범위와 같아야 한다.
- 자유 텍스트 헤더·경로·주소·포트·압력/힘/KE/N/porosity/tau·실제 입자 필드는 출력하지 않는다. `header_ref`는 이미 승인된 비결과 참조 별칭이지 원 헤더 줄이 아니다. 의미상 비결과 메타인지와 출처 승인은 1저자가 사전에 확인해야 하며 문자열 형식 검사가 대신하지 않는다.
- 겹침/노출은 이 명령으로 추정하지 않는다. 1저자가 수령 양식 §5에 출처와 증언을 구분해 적는다. 실제 선택/동결/값 GO 필드는 만들지 않는다.

## 3. ASCII 명령 블록 — 1저자 확인 뒤만

다음 placeholder를 실제 승인 범위로 바꾸기 전에는 중단한다. 파일명은 리포에 채워 넣지 않고 실행할 로컬 사본에서만 상대경로로 지정한다. `lhs_confirm`은 실수 방지 확인란이며 새 승인 토큰이 아니다. POSIX `sh`와 WSL의 `timeout`, `stat`, `sha256sum`, `awk`를 전제로 하지만 이 환경에서 구문·동작을 확인한 것은 아니다.

`lhs_wall_seconds`는 내부 수령 명령에 TERM을 요청할 양의 시간 한도이고, `lhs_max_file_bytes`는 입력 역할당 파일 크기 한도다. timeout은 TERM 뒤5초에도 끝나지 않으면 KILL을 요청한다. 따라서 종료 유예와 외부 셸의 준비/출력 시간을 포함한 전체 블록의 엄밀한 상한은 아니다. 3개 역할의 사전 확인 크기 합은 최대 파일 한도의3배이고, 각 파일을 앞뒤로 재해시하므로 실제 읽는 바이트는 그 합보다 많다. 메타 사본은 별도로8192 bytes 이하로 제한한다. 접근/해시 실패·시간 초과·변경·추가/중복 키 등은 stdout의 부분 자료를 반환하지 않고 STOP한다. 강제 종료/단절 때는 완결 stdout와 rc0를 받지 못한 상태로 기록하며 자동 재시도하지 않는다.

```sh
(
set -fu
LC_ALL=C
export LC_ALL
lhs_wall_seconds='REPLACE_POSITIVE_SECONDS'
case "$lhs_wall_seconds" in ''|*[!0-9]*) printf '%s\n' 'STOP: set a positive wall-clock budget' >&2; exit 2;; esac
[ "${#lhs_wall_seconds}" -le 6 ] && [ "$lhs_wall_seconds" -gt 0 ] || exit 2
command -v timeout >/dev/null 2>&1 || exit 2
lhs_output=$(
timeout --signal=TERM --kill-after=5s "${lhs_wall_seconds}s" sh <<'LHS_READONLY_DRAFT'
set -fu
lhs_confirm='NO'
lhs_scope='REPLACE_SCOPE_ALIAS'
lhs_case='REPLACE_WSL30_CASE_LABEL'
lhs_max_file_bytes='REPLACE_POSITIVE_BYTES'
lhs_receipt='REPLACE_APPROVED_RECEIPT_RELATIVE_PATH'
lhs_meta='REPLACE_APPROVED_METADATA_RELATIVE_PATH'
lhs_current='REPLACE_CURRENT_INPUT_RELATIVE_PATH'
lhs_kind='REPLACE_deck_include_OR_restart'
lhs_receipt_expected='REPLACE_EXISTING_APPROVED_RECEIPT_SHA256'
lhs_meta_expected='REPLACE_EXISTING_APPROVED_METADATA_SHA256'
stop() { printf '%s\n' 'STOP: scope, source, budget or metadata unresolved' >&2; exit 2; }
[ "$lhs_confirm" = 'AUTHOR_CONFIRMED_THIS_COMMAND_SCOPE' ] || stop
case "$lhs_scope" in ''|REPLACE*|*[!A-Za-z0-9_.-]*) stop;; esac
case "$lhs_case" in lhs00_1[012][0-9]) ;; *) stop;; esac
case "$lhs_kind" in deck|include|restart) ;; *) stop;; esac
case "$lhs_max_file_bytes" in ''|*[!0-9]*) stop;; esac
[ "${#lhs_max_file_bytes}" -le 12 ] && [ "$lhs_max_file_bytes" -gt 0 ] || stop
for lhs_tool in stat sha256sum awk; do command -v "$lhs_tool" >/dev/null 2>&1 || stop; done
for lhs_digest in "$lhs_receipt_expected" "$lhs_meta_expected"; do
  [ "${#lhs_digest}" -eq 64 ] || stop
  case "$lhs_digest" in *[!0-9a-f]*) stop;; esac
done
check_file() {
  case "$1" in ''|REPLACE*|/*|-*|*..*|*//*|*[!A-Za-z0-9_./-]*) stop;; esac
  lhs_part=''
  lhs_saved_ifs=$IFS
  IFS=/
  for lhs_component in $1; do
    lhs_part=${lhs_part:+$lhs_part/}$lhs_component
    [ ! -L "$lhs_part" ] || stop
  done
  IFS=$lhs_saved_ifs
  [ -f "$1" ] && [ -r "$1" ] || stop
  lhs_bytes=$(stat -c '%s' -- "$1" 2>/dev/null) || stop
  case "$lhs_bytes" in ''|*[!0-9]*) stop;; esac
  [ "$lhs_bytes" -le "$lhs_max_file_bytes" ] || stop
}
digest_file() {
  lhs_line=$(sha256sum -- "$1" 2>/dev/null) || stop
  printf '%s' "${lhs_line%% *}"
}
for lhs_file in "$lhs_receipt" "$lhs_meta" "$lhs_current"; do check_file "$lhs_file"; done
lhs_meta_bytes=$(stat -c '%s' -- "$lhs_meta" 2>/dev/null) || stop
[ "$lhs_meta_bytes" -le 8192 ] || stop
lhs_receipt_bytes=$(stat -c '%s' -- "$lhs_receipt" 2>/dev/null) || stop
lhs_receipt_hash=$(digest_file "$lhs_receipt") || stop
lhs_meta_hash=$(digest_file "$lhs_meta") || stop
[ "$lhs_receipt_hash" = "$lhs_receipt_expected" ] || stop
[ "$lhs_meta_hash" = "$lhs_meta_expected" ] || stop
lhs_current_bytes=$(stat -c '%s' -- "$lhs_current" 2>/dev/null) || stop
lhs_current_hash=$(digest_file "$lhs_current") || stop
lhs_meta_output=$(awk -F '\t' -v scope="$lhs_scope" -v case_id="$lhs_case" '
BEGIN {
  n=split("scope_id case_id receipt_ref log_a_identity_ref log_a_run_id log_a_segment_id log_a_header_ref log_a_first_step log_a_last_step log_b_identity_ref log_b_run_id log_b_segment_id log_b_header_ref log_b_first_step log_b_last_step restart_parent_ref restart_child_ref", keys, " ")
  for (i=1;i<=n;i++) allowed[keys[i]]=1
}
{
  if (NF!=2 || !($1 in allowed) || seen[$1]++ || $2 !~ /^[A-Za-z0-9_.-]+$/) bad=1
  if ($1 ~ /_(first|last)_step$/ && $2!="UNKNOWN" && $2 !~ /^[0-9]+$/) bad=1
  values[$1]=$2
}
END {
  if (NR!=n || values["scope_id"]!=scope || values["case_id"]!=case_id) bad=1
  for (i=1;i<=n;i++) if (seen[keys[i]]!=1) bad=1
  if (bad) exit 2
  for (i=1;i<=n;i++) printf "metadata.%s=%s\n",keys[i],values[keys[i]]
}' "$lhs_meta" 2>/dev/null) || stop
for lhs_file in "$lhs_receipt" "$lhs_meta" "$lhs_current"; do check_file "$lhs_file"; done
[ "$(digest_file "$lhs_receipt")" = "$lhs_receipt_hash" ] || stop
[ "$(digest_file "$lhs_meta")" = "$lhs_meta_hash" ] || stop
[ "$(digest_file "$lhs_current")" = "$lhs_current_hash" ] || stop
printf 'scope_id=%s\ncase_id=%s\nfile_role_count=3\n' "$lhs_scope" "$lhs_case"
printf 'execution_receipt.bytes=%s\nexecution_receipt.current_sha256=%s\n' "$lhs_receipt_bytes" "$lhs_receipt_hash"
printf 'boundary_metadata.bytes=%s\nboundary_metadata.current_sha256=%s\n' "$lhs_meta_bytes" "$lhs_meta_hash"
printf 'current_input.kind=%s\ncurrent_input.bytes=%s\ncurrent_input.sha256=%s\n' "$lhs_kind" "$lhs_current_bytes" "$lhs_current_hash"
printf '%s\n' "$lhs_meta_output"
printf '%s\n' 'receipt_status=SCOPED_METADATA_ONLY' 'execution_identity_status=NOT_ESTABLISHED_BY_THIS_COMMAND' 'value_access_go=NONE' 'whole_gate=HOLD'
LHS_READONLY_DRAFT
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

## 4. 수령·중단과 남는 한계

1저자는 rc와 완전한 stdout만 전달하고, 입력·출력의 기계 위치나 원본 파일을 붙이지 않는다. 중단이 필요하면 Ctrl-C로 중단하고 rc/완전 출력 미확보를 기록한다. timeout·종료·부분을 완료로 세지 않으며 원본 수정·복구·재생성·자동 재시도는 하지 않는다. 숫자 예산을 바꾼 재시도도 파일 범위와 변경 여부를 다시 확인한 뒤 별도 판단한다.

기존 영수증에 있는 실행 당시 hash/순서 있는 의존·재개 관계는 수령 양식 §3에 그 출처와 함께 별도로 제공한다. 겹침·노출은 §5의 1저자 증언이다. stdout의 현재 hash를 그 칸에 자동 복사하지 않는다. 메타 stdout은 정본/구간/연결 관계의 후보 근거이며 사실 확정·자동 정본 선택이나 과학 자격이 아니다. step 정수만으로 동일 run/segment/물리 시간·harvest 사건을 인증하지 않는다.

이 초안은 실제 WSL 환경에서 작동한다는 확인, 전체 30개 신원 수집 완료, 실제 독립성·평형·압력/N의 확인을 주장하지 않는다. 시간 상한은 OS의 프로세스 종료 기능을 전제로 하며 파일시스템 응답/커널 상태까지 무조건 보증하지 않는다. 앞뒤 재해시도 읽는 동안 원본이 전혀 바뀌지 않았다는 원자적 증명이 아니다. 실제 자료 접근 전 지정 원본/사본의 변경 금지와 승인 출처 확인을 유지한다.
