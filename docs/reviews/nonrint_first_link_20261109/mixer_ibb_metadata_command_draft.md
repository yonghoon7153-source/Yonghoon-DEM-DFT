# 믹서 ibb 현재 메타 수집 명령 초안 — 실행 확인 전

**DRAFT_NOT_RUN / 전체 HOLD.** 1저자가 초안을 본 뒤 대상·읽기 범위·시간/크기 예산을 별도로 확인해야 한다. Codex의 접속·대행 실행 지시가 아니다. 이번에는 문서만 작성했으며 명령 실행·구문 검사·시험·실제 메타 조회를 하지 않았다. 믹서 Q2 운영 봉인, Q3 host/wave·pilot, Q5 발사·배포 GO는 미승인이다.

바탕 B는 `e91bd1c948362712def3f16b5b995027cc10011f`다. 기존 준비 사본 `43eb8a28c`의 `docs/reviews/nonrint_approved_preparation_20261109/mixer_ibb_qualification_receipt_plan.md` §1·§3–5를 사용한다. 그 문서의 “명령은 작성하지 않음”은 당시 범위이고, 이번 지시로 이 **읽기 전용 문서 초안**만 추가한다. 원 계획·운영 파일은 바꾸지 않는다. 예고된 19:00/`1f71…` 반입은 여기서 완료로 가정하지 않는다.

## 1. 자동 수집과 수동/추가 자격의 분리

| 범위 | 이 초안이 하는 일 | 하지 않는 일 / 남는 상태 |
|---|---|---|
| 대상 | 1저자가 확인한 ibb Linux/SLURM 한 설치를 별칭으로 지정 | hostname·주소·현재 디렉터리·실제 경로를 출력하거나 ibb 실체를 자동 인증하지 않음 |
| 설치 메타 | 지정 디렉터리의 mode·소유 UID/GID·device/inode 및 해당 FS의 용량/가용 블록·inode 수 | 최종 경로 요소가 symlink면 STOP. **조상 링크·ACL·bind mount·공유 FS·변경통제 자격은 UNKNOWN** |
| binary/MPI 파일 | 지정한 regular file 두 역할의 크기·현재 SHA256·mode·UID/GID·device/inode·mtime/ctime | 대상 파일 실행, `--version`/`--help`, `mpirun`, library 로딩/호환 검사 없음. 파일의 출처·역할/물리 호환을 hash만으로 인증하지 않음 |
| 시간 | 수집 전/후 UTC 표시와 1저자가 고른 TERM 시한 | 기계 시계의 신뢰성·runtime/walltime 자격·합격 수치·실행 기한을 정하지 않음 |
| Slurm·예약·cap | 출력에는 `NOT_QUERIED`/`UNKNOWN`만 표시 | `squeue`/`scontrol`/제출/예약 조작 없음. 본인 전체 queue나 타인 자료를 dump하지 않음. 승인된 범위의 수동 영수증이 별도 필요 |
| quota·회수·STOP | FS 가용 블록/inode의 시점 관측과 quota·회수 등의 미확인을 구분 | 가용량을 quota·실제 writable budget·충분한 공간으로 바꾸지 않음. quota/회수 예산/수치 STOP 문턱은 UNKNOWN |

설치·binary·MPI의 **입력 역할 3개**를 지정하지만 서로 다른 객체 수를 인증하지 않는다. 자동 탐색·재귀 목록·원로그/결과 파일·모듈/환경 전체 출력·네트워크 접속 도구·sudo·패키지 설치·module load·출력/임시 파일을 만드는 명령은 없다. 아래에 없는 현장 조회를 자동 덧붙이지 않는다. 지정 경로가 실제 어떤 마운트/공유 FS인지와 허용된 읽기 범위는 1저자가 사전에 확인해야 한다.

## 2. 붙여넣기 전 확인할 빈 값

| 항목 | 현재 상태 | 확인 방법/제한 |
|---|---|---|
| 1저자 명령 확인 | PENDING | 아래 확인 문자열은 실수 방지란이지 승인 토큰이 아니다. 확인 전 실행하지 않음 |
| 설치 별칭·읽기 대상 3역할 | null | 이미 알고 승인한 안전한 작업 디렉터리 기준 상대경로만 로컬 초안에 기입. 실제 경로는 리포나 반환문에 넣지 않음 |
| 기초 도구/셸 | 미확인 | POSIX `sh`, GNU `timeout`/`stat`/`sha256sum`, `id`, `date` 전제. 명령 유무 확인은 버전·신뢰성·동작 시험을 대신하지 않음 |
| 파일 크기 한도·TERM 시한 | null | 1저자가 입력 두 파일의 읽기 예산을 확인해 양의 수로 지정. TERM 뒤 최대5초 KILL 요청 유예가 있고 준비/출력·커널 응답까지의 엄밀한 전체 상한이 아님 |
| 원본 변경 금지 창 | 미확인 | 읽는 동안 지정 입력을 변경하지 않는 범위를 먼저 확인. 앞뒤 stat 비교는 적대적 경합이나 원자적 스냅샷 증명이 아님 |

절대경로·공백·상위 `..`·중복/끝 슬래시·일반적인 경로 외 문자는 이 좁은 초안에서 거부한다. 거부 시 경로 표기를 바꿔 우회하거나 실제 입력을 이동/복사/재생성하지 않는다. 현재 파일이 symlink이면 자동 dereference하지 않고 지정 방식과 읽기 범위를 다시 확인한다. 기존 비활성 검증기의 Windows extended/device/UNC 거부를 완화하는 명령이 아니다.

## 3. ASCII 블록 — stdout 대화 텍스트만

```sh
(
set -fu
LC_ALL=C
export LC_ALL
mix_wall_seconds='REPLACE_POSITIVE_SECONDS'
case "$mix_wall_seconds" in ''|*[!0-9]*) printf '%s\n' 'STOP: confirm the time budget' >&2; exit 2;; esac
[ "${#mix_wall_seconds}" -le 6 ] && [ "$mix_wall_seconds" -gt 0 ] || exit 2
command -v timeout >/dev/null 2>&1 || exit 2
mix_output=$(
timeout --signal=TERM --kill-after=5s "${mix_wall_seconds}s" sh <<'MIXER_METADATA_DRAFT'
set -fu
mix_confirm='NO'
mix_install_alias='REPLACE_INSTALLATION_ALIAS'
mix_install='REPLACE_INSTALLATION_RELATIVE_PATH'
mix_binary='REPLACE_BINARY_FILE_RELATIVE_PATH'
mix_mpi='REPLACE_MPI_LAUNCHER_FILE_RELATIVE_PATH'
mix_max_file_bytes='REPLACE_POSITIVE_BYTES'
stop() { printf '%s\n' 'STOP: scope, source or metadata incomplete' >&2; exit 2; }
[ "$mix_confirm" = 'AUTHOR_CONFIRMED_THIS_METADATA_COMMAND' ] || stop
case "$mix_install_alias" in ''|REPLACE*|*[!A-Za-z0-9_.-]*) stop;; esac
case "$mix_max_file_bytes" in ''|*[!0-9]*) stop;; esac
[ "${#mix_max_file_bytes}" -le 12 ] && [ "$mix_max_file_bytes" -gt 0 ] || stop
for mix_tool in stat sha256sum id date; do command -v "$mix_tool" >/dev/null 2>&1 || stop; done
for mix_path in "$mix_install" "$mix_binary" "$mix_mpi"; do
  case "$mix_path" in ''|REPLACE*|/*|-*|*..*|*//*|*/|*[!A-Za-z0-9_./-]*) stop;; esac
  [ ! -L "$mix_path" ] || stop
done
[ -d "$mix_install" ] && [ -r "$mix_install" ] && [ -x "$mix_install" ] || stop
mix_started=$(date -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null) || stop
mix_uid=$(id -u 2>/dev/null) || stop
mix_install_stat=$(stat -c '%a %u %g %d %i' -- "$mix_install" 2>/dev/null) || stop
mix_fs=$(stat -f -c '%t %S %b %f %a %c %d' -- "$mix_install" 2>/dev/null) || stop
file_receipt() {
  mix_role=$1
  mix_file=$2
  [ ! -L "$mix_file" ] && [ -f "$mix_file" ] && [ -r "$mix_file" ] || stop
  mix_bytes=$(stat -c '%s' -- "$mix_file" 2>/dev/null) || stop
  case "$mix_bytes" in ''|*[!0-9]*) stop;; esac
  [ "$mix_bytes" -le "$mix_max_file_bytes" ] || stop
  mix_before=$(stat -c '%a %u %g %d %i %s %Y %Z' -- "$mix_file" 2>/dev/null) || stop
  mix_hash_line=$(sha256sum -- "$mix_file" 2>/dev/null) || stop
  mix_hash=${mix_hash_line%% *}
  [ "${#mix_hash}" -eq 64 ] || stop
  case "$mix_hash" in *[!0-9a-f]*) stop;; esac
  [ ! -L "$mix_file" ] && [ -f "$mix_file" ] || stop
  mix_after=$(stat -c '%a %u %g %d %i %s %Y %Z' -- "$mix_file" 2>/dev/null) || stop
  [ "$mix_before" = "$mix_after" ] || stop
  printf '%s.stat_mode_uid_gid_device_inode_bytes_mtime_ctime=%s\n' "$mix_role" "$mix_before"
  printf '%s.current_file_sha256=%s\n' "$mix_role" "$mix_hash"
}
mix_binary_receipt=$(file_receipt binary "$mix_binary") || stop
mix_mpi_receipt=$(file_receipt mpi_launcher "$mix_mpi") || stop
mix_finished=$(date -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null) || stop
printf 'target_alias=ibb\ninstallation_alias=%s\noperator_uid=%s\n' "$mix_install_alias" "$mix_uid"
printf 'captured_start_utc=%s\ncaptured_end_utc=%s\n' "$mix_started" "$mix_finished"
printf 'installation.stat_mode_uid_gid_device_inode=%s\n' "$mix_install_stat"
printf 'filesystem.typehex_blockbytes_blocks_total_free_avail_inodes_total_free=%s\n' "$mix_fs"
printf '%s\n' "$mix_binary_receipt" "$mix_mpi_receipt"
printf '%s\n' 'input_role_count=3' 'target_identity_authenticated=NO' 'final_component_symlink=NOT_OBSERVED_AT_CHECKS'
printf '%s\n' 'ancestor_links=UNKNOWN' 'acl_and_change_control=UNKNOWN' 'mount_and_shared_filesystem=UNKNOWN'
printf '%s\n' 'binary_or_mpi_invocations=0' 'binary_build_and_mpi_compatibility=UNKNOWN' 'clock_authority=UNVERIFIED'
printf '%s\n' 'slurm_query_status=NOT_QUERIED' 'allocation_live_jobs_reservations_and_cap=UNKNOWN' 'quota=UNKNOWN'
printf '%s\n' 'runtime_storage_retrieval_and_stop_qualification=UNKNOWN' 'qualification=NO_GO' 'whole_gate=HOLD'
MIXER_METADATA_DRAFT
)
mix_rc=$?
if [ "$mix_rc" -ne 0 ]; then
  printf 'STOP: command_rc=%s; incomplete receipt; no automatic retry\n' "$mix_rc" >&2
  exit "$mix_rc"
fi
printf '%s\n' "$mix_output"
printf '%s\n' 'receipt_kind=CURRENT_FILE_AND_FILESYSTEM_METADATA_ONLY' 'command_rc=0'
)
```

표준 출력은 내부 명령이 rc0로 끝난 뒤에만 반환한다. 시간 초과·오류·부분 출력·단절은 완전 수령이 아니다. Ctrl-C로 중단할 수 있으며 원본 수정·정리·재시도·후속 명령을 자동 수행하지 않는다. 1저자는 **rc와 완전한 stdout 텍스트만** 대화로 제공하고 실제 위치·원본 파일·전체 환경은 붙이지 않는다. `installation_alias`에도 주소/경로/결과값을 넣지 않는다. ASCII 형식 제한이 별칭의 의미상 적절성을 인증하지는 않는다.

## 4. 해석과 반환 한계

`stat` mode는 octal, UID/GID·device/inode·bytes·mtime/ctime은 해당 도구의 수치 표현이다. FS 열은 type의 hex ID, 블록 bytes, total/free/사용자 가용 blocks, total/free inodes 순이다. 도구가 특수/미지원 수치를 반환하면 이를 충분한 공간이나 정상으로 바꾸지 않는다. FS 블록과 inode 관측은 quota·실제 쓰기 가능성·dump/restart 예산·회수 공간을 입증하지 않는다.

최종 요소 symlink를 관측하지 않았다는 것과 조상 경로 전체·ACL·마운트·실제 링크 거부 자격은 다르다. 설치/FS와 두 파일의 수집 시점도 원자적으로 같지 않다. 소유 UID·mode·현재 SHA만으로 저자 승인·운영자 권한·빌드 출처·binary/MPI 동작·로그 호환·과학 자격을 확정하지 않는다. 과거 43/86 사본의 한정 수용을 이 현장 파일로 옮기지 않는다.

출력은 [고정 자격 계획 빈틀](mixer_ibb_fixed_qualification_plan.md)에 후보 근거로 연결한다. 실제 수령 전에는 모든 측정값이 `null`이며, 수령 뒤에도 미확인 필드는 `UNKNOWN/PROBE_NEEDED`로 남는다. 계획 검토 전과 필수 자격/승인 부재 시 모두 **NO_GO/HOLD**다. NP20·초기 E0 1팔·자격+별도 wave 승인 뒤 최대2팔·기존 순서는 유지한다. 최종 ZIP은 지금 보내지 않고 최종 발사 묶음 검토 때 함께 전달하며 Claude 미수령 상태를 유지한다.
