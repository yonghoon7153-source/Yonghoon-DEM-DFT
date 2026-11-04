# REIL C4-E · E1-1–3 승인 요청 정정 범위안 v2 (E113_PRE_01–06 · C1 + 보완 셋 E113_FIX_SCOPE_01–03) — 사용자 채택 요청 · 2026-11-04 KST

> **정정 범위의 채택을 요청하는 문서다 (실행 0).** 정정 범위안 v1 (`docs/REIL_C4E_E1_1_3_PRE_FIX_SCOPE_20261104.md` · `b6642003…` · 그대로 둔다) 의 검토 회신
> (상태 문서 §108 · `reviews/review_reil_c4e_e1_1_3_pre_fix_scope_review_20261104/originals/`) 은 `REVISION_SCOPE_DIRECTION_ACCEPTABLE_CLARIFICATIONS_REQUIRED_NOT_ADOPTED`
> 이다 — 정정 방향은 맞고, PRE_03 · PRE_05 의 설명 보완 셋을 이 범위안과 v2 초안에 넣으라고 했다. 채택하신 뒤에만 요청서 v2 · 초안 v2 셋 · 발송문 v2 를 쓴다
> (새 경로 · 정적 검사만). 채택해도 초안 · 탐침 · E1-1–3 의 어느 것도 실행하지 않는다.

## 0. 회신이 정한 것 (§108)

- **방향 수용 (v1 그대로 · §1):** PRE_01 · PRE_02 · PRE_04 · PRE_06 · C1. A 를 전제한 정상 수 b 14 · c 17 · e 16 · f 24 — 이 v2 는 감시 호출 기록 때문에 c · e · f 에
  하나씩 더한다 (§5).
- **보완 셋:** FIX_SCOPE_01 (P1 · 기한 안의 반환 관측) · FIX_SCOPE_02 (P1 · 감시 중단 · 재진입 · 지연 착수) · FIX_SCOPE_03 (P2 · 종결 기록의 쓰기 실패).
- **PRE_03 은 A 권고.** B 는 최초 감시 실패를 보존하지 않아 종결 대안이 아니라고 했으므로 이 v2 는 B 를 빼고 A 만 적는다.
- **R = 1,800 s** 는 정책 제안이다 (증명 아님 · 미채택). g3 까지 예산을 주장하려면 push 의 실제 반환 경계가 따로 필요하다 (§4).
- **v1 의 문구 넷은 내 결함이다:** `published` 를 launcher 종료 시각으로 정한 것 · "도구에 끊긴 감시는 기록을 남기지 않으므로 다시 걸 수 있다" · "`06_end.json` 은
  늘 쓴다" · "다시 읽지 않는다 → 다른 시점의 바이트가 섞이지 않음". 아래에서 각각 지우거나 고친다 (§2-1 · §2-2 · §3).

## 1. 바뀌지 않는 정정 (v1 의 방향 · 검토가 붙인 확인만 더함)

| 지적 | 정정 (v1 그대로) | 검토가 더한 확인 → v2 반영 |
|---|---|---|
| PRE_01 | b3 을 한 물리 줄로 · 바로 뒤 확인 (묶음 반환 0 · `00_start.txt` 의 sha 행 정확히 20) · 명령은 한 줄 = 한 완전한 명령 | sha 행 20 은 b 커밋 수 (14) 와 다른 집합이다 — `00_overall.json` 은 b 커밋에 들고 해시 행에는 넣지 않는다 (21 이 아니다) |
| PRE_02 | 판정기 기대 집합 여덟 · 요청서 · 발송문의 "아홉" 정정 · `SOURCES.json` 은 기존 입력 봉인으로만 | 고정 run · monitor 를 바꿔 아홉을 만드는 우회는 없다 |
| PRE_04 | T_a · T_end = T_a + 21,600 (a → g3) · `00_overall.json` · wrapper 착수 조건 | R 은 정책 (§8 의 사용자 결정) · 단계 기한은 관측 상한이지 반환 보장이 아니다 · g3 반환 경계 (§4) |
| PRE_06 | 실제 커밋할 파일 목록에 공개 검사 (정상 / F3) · 부적합은 보존하고 커밋 중지 · b 의 `00_*.py` 넷은 고정 sha 행 | 검사한 목록 = `git diff --cached --name-only` 의 집합 · 각 파일의 staged blob = 검사한 바이트의 blob (검사 뒤 바뀌지 않음) — 어긋나면 커밋하지 않고 멈춘다 |
| C1 | `first_error` 키가 있고 null | 모든 필수 필드에서 누락 (거짓) 과 명시적 null 을 나눈다 — null 이 허용되는 필드는 요청서에 이름으로 적는다 |

## 2. PRE_03 — A 와 보완 (FIX_SCOPE_01 · 02)

v1 의 A (기산점 · 끝 기록 · 감시 기록 + 판정기 필수) 를 유지하되, 감시 기록을 **호출 기록 (begin) · 비종결 조각 기록 (slice) · 단일 끝 기록 (watch)** 으로 나누고,
시작 기록의 경로를 wrapper 와 감시의 단일 경합 지점으로 쓴다. 감시는 여전히 run 에 개입하지 않는다 (신호 · launcher 파일 쓰기 없음 — 묘비는 시작 기록이 없을 때만
생길 수 있고, 시작 기록이 없으면 launcher 는 아직 없다).

### 2-1. 시각을 나눈다 — 정상 수용은 관측 시각 하나에만 (FIX_SCOPE_01)

| 시각 | 기록 (쓰는 주체) | 찍는 때 | 쓰임 |
|---|---|---|---|
| `launch_epoch` | `<name>.launch_epoch.txt` (띄우는 셸 줄 · `set -C` 배타 · `date -u +%s` 정수) | `setsid` 앞 | 시작 창 [launch_epoch, launch_epoch + 60] 의 원점 · 다시 걸어도 그대로 |
| `epoch` · `deadline_epoch` | `outer_start.json` (wrapper) | 시작 기록을 link 하기 직전 | 단계 기한 = `epoch` + ALLOW_S · 재진입으로 다시 세지 않는다 |
| `launcher_exit_epoch` | `outer_end.json` (wrapper) | launcher 반환 직후 | 순서 검사만 |
| `end_snapshot_epoch` | `outer_end.json` (wrapper) | 그 파일을 쓰기 직전 | 순서 검사만 — **그 뒤 `outer_end` · `outer_rc` 의 게시 완료를 증명하지 않는다** |
| `observed_epoch` | `watch.json` (감시) | rc · `outer_end` 를 읽고 검증을 마친 직후 | **정상 수용의 유일한 시각: `observed_epoch ≤ deadline_epoch`** |

- **wrapper 의 순서:** launcher 반환 → `outer_end.json` 게시 (임시 → fsync → 배타 link) → `outer_rc.txt` 게시. `outer_end` 게시가 실패하면 `outer_error.json`
  (phase `end_publish`) · rc 는 게시하지 않는다 · 반환 4. 그래서 rc 가 보이면 `outer_end` 는 이미 완전하다.
- **감시의 관측 (매 poll):** `outer_error.json` 이 있으면 → `outer_error` (rc 가 있어도). 없고 rc 가 있으면 → rc 한 번 읽기 (형식 `^[0-9]+\n$` · 아니면
  `malformed`) → `outer_end` 한 번 읽기 · 검증 (kind · 단계 · `start_sha256` = 감시가 읽은 시작 기록 바이트의 sha · `rc` = rc 파일 값 ·
  `epoch ≤ launcher_exit_epoch ≤ end_snapshot_epoch` · 없음 / 불일치면 `end_invalid`) → 그 직후 `observed_epoch` → **≤ 기한이면 `published` · 넘으면 `late`.**
  둘 다 없고 지금 ≥ 기한이면 `deadline`.
- **반례 (정적):** 기한 900 · 종료 899 · 게시 901 → rc 는 900 뒤에야 보이므로 첫 관측 ≥ 901 → `late` (차단). 종료 899 는 이것을 구제하지 못한다. 파일 시각 같은
  다른 근거로 앞선 게시를 추정하지 않는다 — 기한 뒤 첫 관측은 늘 `late` 다.
- **보수적이다:** poll 간격 (5 s) 때문에 898 에 게시돼도 902 에 처음 보면 `late` 다 — 거짓 실패는 가능하고 거짓 수용은 없다. launcher 의 자식 상한 (60 / 300 /
  10,800 s) 은 감시 여유 (900 / 1,800 / 12,600 s) 보다 한참 안쪽이라 (요청서 v1 §9) 정상 실행이 기한 경계에 닿을 일은 드물다 (보증 아님).
- **최초 실패는 풀리지 않는다:** 끝 기록이 하나 생기면 두 번째 끝 상태는 없다 (§2-2). 그 뒤의 rc 0 · 잔류 0 은 그것을 바꾸지 못하고, 판정기는 `published` 만
  정상으로 본다.
- **스스로의 미래 쓰기를 인증하지 않는다:** `observed_epoch` 는 감시가 자기 기록을 쓰기 전에 찍은 시계 값이다. `watch.json` 은 관측 직후 게시하고 게시 완료 시각을
  주장하지 않는다. v1 의 "게시 뒤 wrapper 종료 대기 (≤ 10 s)" 는 `watch.json` 게시 **뒤**로 옮기고 그 결과는 stdout 에만 둔다 (프로세스 증거는 `observe … 1` 이
  맡는다).

### 2-2. 감시의 중단 · 재진입 · 소유권 (FIX_SCOPE_02 앞 절반)

- **v1 문구 삭제:** "도구에 끊긴 감시는 기록을 남기지 않으므로 다시 걸 수 있다" 를 지운다. 게시 (임시 쓰기 → fsync → link → 임시 제거) 의 어디서 끊기느냐에 따라
  ① 아무것도 없음 (끝 상태를 관측한 뒤 게시 전 포함) ② 부분 임시 파일 ③ 완전한 최종 + 임시 ④ 완전한 최종이 모두 가능하다. 기록이 없다는 것만으로 이전 감시가
  실패를 보지 않았다고 볼 수 없다.
- **감시 기록 셋 (같은 게시 방식 · 모두 배타):**
  - `<name>.watch_<k>.begin.json` — 호출 k (1, 2, …) 의 시작. 무엇을 관측하기 **전에** 게시한다. `k` · 시각 · pid · `prev_sha256` (k ≥ 2 면 `slice_<k−1>` 의 sha ·
    k = 1 이면 null).
  - `<name>.watch_<k>.slice.json` — **확인된 비종결 끝은 이것 하나뿐이다.** 호출 k 가 자기 조각 (`WAIT_SLICE_S` = 6,600 s — 셸 도구 배경 실행의 상한 7,200 s 보다
    짧게) 을 끝 상태 없이 다 쓰면 스스로 게시하고 반환 15 (`state` "continue" · 마지막 poll 시각 · 기한 · `begin_sha256` · `start_sha256`).
  - `<name>.watch.json` — 단일 끝 기록 (`published` · `late` · `deadline` · `malformed` · `end_invalid` · `outer_error` · `start_missing` · `start_unreadable` ·
    `watch_error`).
- **호출 k 의 진입 규칙 (아무것도 쓰기 전에 · 위에서부터):**
  0. `launch_epoch.txt` 가 없거나 형식 (`^[0-9]{10}\n$`) 이 틀리면 → 쓰지 않는다 → 반환 2 (거부 · 띄우는 줄보다 먼저 감시를 걸지 않는다 — 그래서 `begin_1` 은
     늘 `launch_epoch` 뒤다).
  1. `watch.json` 이 있으면 → 쓰지 않는다. 읽히고 맞으면 그 내용을 stdout 에 그대로 내고 반환 20 (기존 끝 상태의 소비 — 단계는 그 상태대로 간다) · 못 읽으면
     반환 16.
  2. 없고 감시 기록의 임시 파일 (`watch*.tmp`) 이 있으면 → 쓰지 않는다 → 반환 16 (불명).
  3. 있는 호출 기록 1 … m 이 이어져 있고, 각 i ≤ m 에 완전하고 맞는 `slice_<i>` (`continue` · `begin_sha256` 일치) 가 있어야 한다. `begin_<m>` 뒤에 `slice_<m>`
     도 `watch.json` 도 없으면 → 이전 호출의 결과 불명 → 쓰지 않는다 → 반환 16. **정상 재감시가 아니다 → 실패 종결 (요청서 §6 의 잔류 관측 · R1 · F3 · 미완).**
  4. 그때만 k = m + 1 의 `begin_<k>` 를 배타 게시한다. 실패하면 (다른 감시가 먼저) → 반환 16 — 그 호출이 남긴 임시 파일은 지우지 않고, 판정기는 임시 파일이
     있으면 정상으로 보지 않는다.
- **단일 소유권:** `begin_<k>` 를 게시한 호출만 `slice_<k>` · `watch.json` 을 쓸 수 있고, 호출 k + 1 은 `slice_<k>` 가 있어야 시작한다 → 살아 있는 감시는 늘
  하나다. 모든 호출은 같은 `launch_epoch` 와 시작 기록의 같은 기한을 읽는다 (k ≥ 2 는 시작 기록의 sha 를 `slice_<k−1>` 의 `start_sha256` 과 대조).
- **재진입 책임:** 다음 호출은 실행자가 반환 15 를 본 뒤에만 띄운다 — 요청서 v1 §4 · §6-1 의 "도구에 끊기면 같은 명령을 다시" 를 이것으로 바꾼다. 도구가 조각 기록
  전에 감시를 끊으면 (돌아오지 않음 · 강제 종료) 불명이다 → run 이 정상이어도 그 단계는 실패 종결된다. 거짓 수용 대신 거짓 실패를 택한다.
- **게시 실패:** 끝 상태나 조각 끝을 관측했으나 그 기록의 게시가 실패하면 → stdout 한 줄 (관측 상태 · 실패 단계 · 오류) · 반환 19 · 부분 임시 파일은 그대로
  (지우지 · 고치지 · 다시 하지 않는다) → 실패 종결 · 미완. 다음 호출은 규칙 2 · 3 에서 16 이다.
- **③ 의 남은 임시 이름:** 최종이 완전해도 임시 이름이 남으면 판정기는 정상으로 보지 않는다 (규칙을 단순하게 · 거짓 실패 쪽).
- **호출 수:** `begin_1` 은 `launch_epoch` 뒤이고 시작 기록의 `epoch` 는 `launch_epoch` + 60 안이므로, 첫 조각 끝 ≥ `epoch` + 6,540 s · 둘째 조각 끝 ≥ `epoch` +
  13,140 s 다. 그래서 c · e (기한 900 · 1,800 s) 는 한 번 (`slice` 가 있으면 정상 아님) · f (12,600 s) 는 많아야 두 번이다. run 의 기대 경과 35–45 분이면 한 번
  (보증 아님). 호출 사이의 틈은 거짓 수용을 만들지 않는다 (관측 시각을 여전히 기한과 견준다).

### 2-3. 시작 실패 뒤 지연 착수 차단 — 경합 순서 (FIX_SCOPE_02 뒤 절반)

- **단일 경합 지점 = `<name>.outer_start.json` 경로.** 쓰는 주체는 둘이다.
  - wrapper: 시작 기록을 임시 → fsync → `os.link` (배타 — 있으면 실패).
  - 감시: 시작 창이 끝날 때 (`launch_epoch` + 60) 시작 기록이 없으면 같은 경로에 **묘비** (kind `REIL_E113_START_MISSING`) 를 `O_CREAT | O_EXCL` 로 직접 만든다
    (임시 없음 · 있으면 실패).
  - 같은 경로를 배타로 만드는 둘 중 **하나만** 성공한다.
- **wrapper 의 착수 전 확인 (순서대로 · 모두 launcher 를 띄우기 전):**
  1. 이 단계의 외곽 기록 (시작 · 끝 · 반환 · 오류 · 그 임시 · `outer_stdout` · `outer_stderr`) 이나 감시의 끝 기록 (`watch.json`) 이 이미 있으면 거부 (반환 2 ·
     아무것도 쓰지 않음 — 메시지는 셸이 연 `wrapper_output.txt` 에). 감시의 호출 기록 (`begin`) 은 조건이 아니다 — 띄우는 셸 줄 (c1) 과 감시 (c2) 는 따로 뜨므로
     그 순서를 조건으로 걸면 정상 실행이 자기 경합으로 막힌다.
  2. `launch_epoch.txt` (`^[0-9]{10}\n$`) · `00_overall.json` (필수 키 · `T_end = T_a + 21,600` · §NN) · launcher sha 를 읽어 대조한다.
  3. `t = time.time()` 에서 `0 ≤ t − launch_epoch ≤ 60` 이고 `t + ALLOW_S ≤ T_end − R`.
  4. 시작 경로의 소유: 시작 기록 (`epoch` = t · `deadline_epoch` = t + ALLOW_S · `launch_epoch` · `overall_sha256` · §NN) 을 link 한다. 감시가 묘비로 그 경로를 먼저
     가졌으면 EEXIST 로 실패한다.
  5. **link 가 성공했을 때만** launcher 를 띄운다. 2–4 의 실패 (link 의 EEXIST 포함) 는 `outer_error.json` (phase · 사유) · launcher 를 띄우지 않음 · 반환 3.
- **감시의 시작 대기:** 1 s 마다 본다 — 시작 기록이 보이면 읽어 검증한다 (kind · 단계 · `deadline_epoch` = `epoch` + ALLOW_S · `launch_epoch` 일치 · 아니면
  `start_unreadable`). `outer_error.json` 이 보이면 `outer_error`. 창이 끝나도 시작 기록이 없으면 묘비 → 성공이면 `start_missing` (끝 기록) · EEXIST 면 그사이
  wrapper 가 이긴 것이므로 다시 읽어 시작 기록이면 정상 진행 · 그 밖이면 `start_unreadable`.
- **왜 경합이 닫히는가:** launcher 는 wrapper 의 link 성공 뒤에만 뜨고, 묘비는 감시의 `O_EXCL` 성공 때만 있으며, 둘은 같은 경로다. 그러므로 **`start_missing` 확정
  ⇒ wrapper 의 link 는 실패 ⇒ launcher 없음** — 늦게 살아난 wrapper 가 몇 초 뒤에 오든 같다. 감시가 아예 돌지 않은 경우는 wrapper 자신의 창 확인 (3) 이 막는다
  (60 s 뒤의 wrapper 는 link 하지 않는다). 사전 검사 (3) 만으로 경합이 닫혔다고 쓰지 않는다 — 닫는 것은 같은 경로의 배타 생성이다.
- **기대는 것 (밝힘):** 같은 호스트의 실시간 시계 (`time.time()` · `date +%s`) — 시계가 뛰면 창이 틀어질 수 있고, 이것은 기록될 뿐 막지 못한다. 로컬 POSIX 파일
  시스템의 원자적 `link` · `O_EXCL` 의 공개 의미 (이 컨테이너 파일 시스템의 실제 동작을 이 문서가 관측한 것은 아니다). link 와 launcher 띄우기 사이의 시간은 묶지
  않는다 (기한은 link 직전 t 에서 세므로 짧아지는 쪽 — 보수적).
- **부분 묘비:** 감시가 묘비를 쓰다 끊기면 부분 파일이 경로를 차지한다 → wrapper 는 link 하지 못한다 (실패 쪽으로 닫힘) · 감시 · 판정기는 못 읽음 → 실패.

### 2-4. 판정기 (A · 필수 입력 · 순서)

정상은 아래가 모두 참일 때뿐이다 (키 없음 = 거짓 · null 은 이름으로 허용한 곳만):

- `00_overall.json`: `kind` · `section` (= §NN) · `T_a` (정수 · 승인 기록 §의 값과 같음 — 수동 판정) · `T_end` = `T_a` + 21,600 · `R` (= 채택값). 각 시작 기록의
  `overall_sha256` = 그 파일의 sha.
- `launch_epoch.txt` = `^[0-9]{10}\n$` · `T_a ≤ launch_epoch`.
- 시작 기록: kind `REIL_E113_OUTER_START` (묘비 아님) · `launch_epoch` = 파일 값 · `0 ≤ epoch − launch_epoch ≤ 60` · `deadline_epoch` = `epoch` + ALLOW_S ·
  `deadline_epoch ≤ T_end − R` · `section` = §NN · v1 의 항목 (argv · sha · `pid = sid = pgid` 등).
- `outer_end.json`: `start_sha256` = 시작 기록의 sha · `rc` = `outer_rc.txt` 값 (0) · `epoch ≤ launcher_exit_epoch ≤ end_snapshot_epoch`.
- 감시 사슬: `launch_epoch ≤` `begin_1` 의 시각 · `begin_1 … begin_n` 이 이어져 있고, `slice_1 … slice_(n−1)` 은 `continue` · `begin_sha256` · 다음 begin 의 `prev_sha256` 이 맞으며, `slice_n` ·
  `begin_(n+1)` 이 없다. `watch.json` 은 `state` "published" · `k` = n · `begin_sha256` = `begin_n` 의 sha · `start_sha256` · `end_sha256` = `outer_end` 의 sha ·
  `rc` · `end_snapshot_epoch ≤ observed_epoch ≤ deadline_epoch`.
- 외곽 · 감시 기록의 임시 파일 0 · `outer_error.json` 없음.
- 잔류 관측: `sid` 는 정수 (bool 아님) · > 1 · 시작 기록의 `sid` 와 같음 · `sid_error` 키가 있고 null (`observe` 는 `sid_error` 가 있으면 반환 1 — v1 그대로).

### 2-5. `wait` 의 반환 (요청서 v1 §6-1 을 바꾼다)

| 반환 | 상태 | 새로 쓰는 것 | 다음 |
|---|---|---|---|
| 0 | `published` | `watch.json` | `observe … 1` |
| 15 | `continue` (조각 끝 · 비종결 확인) | `slice_<k>` | 같은 `wait` 를 다시 (호출 k + 1) — **재진입은 이것 뒤에만** |
| 10 · 17 | `deadline` · `late` | `watch.json` | 실패 종결 |
| 11 · 18 | `malformed` · `end_invalid` | `watch.json` | 실패 종결 |
| 12 | `outer_error` | `watch.json` | 실패 종결 |
| 13 · 14 | `start_missing` (묘비 확정) · `start_unreadable` | (묘비) · `watch.json` | 실패 종결 |
| 21 | `watch_error` (관측 중 예상 밖 예외) | `watch.json` | 실패 종결 |
| 19 | 관측했으나 그 기록의 게시 실패 | (부분 임시 · stdout 에 관측 상태) | 실패 종결 · 미완 |
| 16 | 이전 호출 불명 · 부분 기록 · 소유권 경합 | 없음 | 실패 종결 (정상 재감시 없음) |
| 20 | 끝 기록이 이미 있음 (소비) | 없음 | 기록된 상태대로 |
| 2 | 인자 · 위치 · `launch_epoch.txt` 없음 / 형식 거부 | 없음 | 멈춤 |
| (돌아오지 않음 · 도구가 끊음) | 불명 | — | 실패 종결 (다음 호출은 16) |

## 3. PRE_05 — 종결 기록의 쓰기 시도와 실패 (FIX_SCOPE_03)

- **v1 문구 정정:** "`06_end.json` 은 늘 쓴다" 를 지운다. 바뀐 뜻: 항목 · 단계마다 오류를 사유로 모아 **배타 생성을 시도한다** (임시 → fsync → link). 기록 자체가
  실패하면 (임시 생성 · 쓰기 · fsync · link 어느 단계든) stdout 한 줄 (`{"end_written": false, "phase": …, "error": …}`) · 반환 5 · 부분 임시 파일은 그대로 →
  **미완.** 도구 채널 (stdout · 반환) 마저 쓸 수 없으면 **미확인이지 성공이 아니다.** 자동 재시도 · 부분 파일 삭제 / 수정 · 정상 판정 승격은 없다.
- **그다음 절차:** `06_end.json` 이 없거나 못 읽으면 g2 의 커밋 · g3 의 push 로 가지 않고 그 자리에서 멈춘다 — 도구 반환을 결과 §에 그대로 적고 사용자에게 묻는다
  (첫 예상 밖 결과에서 멈춘다 · push 는 바깥 동작이다).
- **한 번 읽기의 뜻 (v1 의 "다른 시점의 바이트가 섞이지 않음" 정정):** 파일마다 한 번의 보호된 읽기가 돌려준 **같은 버퍼**에서 sha · bytes · (작은 파일이면) 본문 ·
  실패 사유를 만든다. 그 버퍼가 쓰는 중인 원본의 한 시점이라는 뜻은 아니다 (쓰는 중인 파일은 한 번의 읽기 안에서도 섞일 수 있다). F3 의 비원자 사본 한계는
  그대로이고, 목록 없는 `frozen_<name>/` 의 파일별 기록도 그 한계 안의 관측이다.
- **freeze (v1 그대로):** 파일마다 읽기 · 쓰기 예외를 잡아 행에 (성공 / 실패 · 사유 · 읽은 시각) · 목록은 같은 게시 방식 · 목록 게시가 실패하면 stdout 한 줄 ·
  반환 5 · 부분 사본은 지우거나 고치지 않고 다시 하지 않는다.
- **작성기가 모을 새 기록:** `launch_epoch.txt` · `outer_end.json` · `watch_<k>.begin.json` · `watch_<k>.slice.json` · `watch.json` · 묘비 (시작 경로의 kind) · 외곽 ·
  감시 기록의 임시 파일 — 모두 같은 한 번 읽기로.

## 4. 전체 예산 · g3 의 실제 반환 경계 (PRE_04 의 연결)

- **경계:** T_a (a 의 이름 확인 직전 `date -u +%s` · 승인 기록 §) → **g3 의 push 가 실제로 돌아온 시각.** T_end = T_a + 21,600 s. 총예산은 늘리지 않는다.
- **R (정책 · 사용자 결정):** 마지막 단계의 기한 뒤 종결 (잔류 관측 · R1 · F3 · 판정 · 공개 검사 · 커밋 · 끝 기록 · g) 에 남기는 몫이다. 권장 1,800 s 는 정리 ·
  I/O · 네트워크 · 반환의 물리 상한 증명이 아니다. wrapper 착수 조건 `epoch + ALLOW_S ≤ T_end − R` 때문에 R = 1,800 s 면 **f 는 T_a + 7,200 s 안에 시작해야
  한다** (21,600 − 1,800 − 12,600) — 넘으면 wrapper 가 띄우지 않고 f 는 미완이다.
- **단계 기한 = 관측 상한:** `deadline_epoch ≤ T_end − R` 은 기한 값의 관계이지 launcher 가 그 안에 돌아온다는 보장이 아니다 (v1 의 "단계 마감은 늘 T_end − R
  이하" 를 이 뜻으로 좁힌다).
- **g3 반환 기록:** g3 의 push 와 같은 셸 줄에서, push 가 돌아온 직후 반환과 `date -u +%s` 를 `<E>/07_g3_return_<i>.txt` (`set -C` 배타 · i = 시도 번호) 와 stdout
  에 남긴다. push 전에 쓴 `06_end.json` 은 이것을 담을 수 없으므로 준수 판정에 쓰지 않는다. 이 파일은 다음 (결과 §) 커밋에 넣는다.
- **재시도:** 원격 · 네트워크 오류면 저장소 규칙대로 최대 4 번 다시 한다 (2 · 4 · 8 · 16 s 뒤) — 매번 이름 확인을 앞에 두고 i 를 늘린다. 이 회신의 보존 push 도
  원격 `Internal Server Error` 로 네 번 거부된 뒤 다섯 번째 시도에서 성공했다 (§108) — push 의 반환은 미리 알 수 없다.
- **준수 주장:** 어떤 시도 i 가 반환 0 이고 그 반환 시각 ≤ T_end 일 때만 "a → g3 ≤ 6 h" 를 적는다. 넘거나 · 모두 실패하거나 · 반환을 확인하지 못하면 **미완 ·
  준수 주장 없음** (실제 시각을 그대로 적는다). g3 뒤의 결과 § · 발송문은 예산 밖의 문서이고 실행이 없다.

## 5. 다시 맞출 수 (정상 경로 · 요청서 §7-1)

| 커밋 | 요청서 v1 | 범위안 v1 (A) | v2 | 차이 (범위안 v1 대비) |
|---|---:|---:|---:|---|
| b | 13 | 14 | 14 | 없음 (b3 의 sha 행은 20) |
| c identity | 14 | 17 | 18 | + `watch_1.begin.json` |
| e fetch | 13 | 16 | 17 | 같음 |
| f run | 22 | 24 | 25 · 27 | + `watch_1.begin.json` · 감시 호출이 두 번이면 `slice_1` · `begin_2` 를 더해 27 |
| g | 1 | 1 | 1 | `06_end.json` (`07_g3_return_*.txt` 는 결과 § 커밋) |

- 정상 경로의 수다. 실패 · 부분 산출 (묘비 · 임시 · `outer_error` · `kill` · `leftover_2` · `frozen_*` 등) 은 있는 그대로 커밋하고 수를 결과 §에 적는다 — 정상 수에
  억지로 맞추지 않는다.

## 6. 바뀌지 않는 것

사용자 선택 (§105 — A · R1 · P1 · 판정 A · 공개 A · 절차 Git 권장안) · 순서 (a → p → b → c → d → e → f → g) · 탐침 명세 (p1–p5) · 감시 여유 (900 / 1,800 /
12,600 s) · 시작 창 60 s · poll 5 s · 전체 6 h · launcher v6 와 run · 다섯 모듈 · 봉인 · 신뢰 목록 · 요청서 v1 · 초안 셋 · 범위안 v1 (그대로 둔다).

## 7. 채택 뒤 순서

요청서 v2 (`docs/REIL_C4E_E1_1_3_APPROVAL_REQUEST_v2_20261104.md`) · 초안 v2 셋 (`…OUTER_DRAFT_v2_…` · `…JUDGE_DRAFT_v2_…` · `…END_WRITER_DRAFT_v2_…`) 작성 →
정적 검사 (AST · 이름 검사 · ruff · 비밀 검사 · 명령 줄의 물리 줄 검사 · 판정기 · 작성기 · 요청서 §7-1 의 파일 집합 대조) → 원장 § → 발송문 v2 → 커밋 · push →
재검토 → 별도 사용자 실행 승인. 초안 실행 0 — 정적 검사 통과는 동작 보장이 아니다.

## 8. 정하실 것

1. **이 정정 범위 v2 채택** — 채택하시면 §7 대로 쓰고 멈춘다 (권장).
2. **PRE_03 의 방식 = A + 보완 (§2)** — 검토 권고. B 는 검토가 PRE_03 종결 대안이 아니라고 해서 이번에는 고를 거리로 두지 않는다.
3. **종결 reserve R** — **1,800 s (권장 · 정책)** / 다른 값. R 은 f 의 마지막 시작 시각 (T_a + 21,600 − R − 12,600) 을 정한다.
