# 사전 공격 10 회차 (독립 · diff 만) — Rint ② 회차 ② 고침 `f5b00a838` (바탕 `18bb6a2e4`)

- 탐침 커밋 = **`69a08d094`** (가지 `worktree-agent-ae3d6733798aef8f9` · push 안 함) · 폴더 `docs/reviews/rint2_rr2_fix_evidence_20261105/preattack10/`
- 코드 판: 고친 판 `d3775ca8…` · 바탕 `eff2b4b4…` · 시험 `583b7c3d…`. 고친 사람의 `code_sha256.txt` 와 같습니다 (관찰).
- 가볍게 돌렸습니다. 사슬 전체 · 끝-끝 · kgy 판 · `check_all.sh` 는 돌리지 않았습니다. Python 3.11.18 만 썼고, 한 번에 프로세스 하나 · `python3 -I` · 임시 폴더로 돌렸습니다.

**결론:** 고침은 주장한 반례를 실제로 막습니다 (false · 0.0 · −0.0 rc · 로그 없음 · FIFO 로그 · 못 읽는 요약). 새 시험 12 개 + PE03u 는 고친 판 13/13, 바탕 판 0/13 이고, 바탕 판의 실패도 옳은 까닭입니다. 독립 변이 6 개도 6/6 잡혔습니다. 그러나 **같은 부류의 P2 가 하나 남습니다.** rc `null` 을 소비자마다 반대로 읽기 때문에, RR2-01 과 같은 전제 (첫 recover 전 한 칸 편집) 에서 Traceback 런이 재실행 자격을 얻습니다. 실제 git 원장 경로에서 관찰했습니다. 이번 고침의 새 시험 RC04 · PE03u · LG01 이 그 허용을 기대값으로 박아 두었습니다.

## §1 발견

| id | 등급 | 자리 (`f5b00a838`) | 무엇 | 최소 고침 |
|---|---|---|---|---|
| **PB-01** | **P2** (RR2-01 · PA-01 과 같은 부류 · 같은 전제) | `rint_r_chain.py:3804–3808` `chain_end_failed` · `:3912–3916` `stop_cause` GROUP_UNCONFIRMED · `:3961` recover 가지 ↔ `:3966–3967` by chain 가지 | **상태:** "러너가 스스로 끝남" (원인 None) 인데 rc 가 null — 생산자가 만들지 않는 상태입니다 (`run_in_group`: 원인 None ⇒ rc = `Popen.wait` 정수 · `_execute`: 원인 None 이면 그 정수). by chain 끝 기록 (원인 None · rc null) 은 runner_rc · 재실행 없음으로 읽힙니다 (RC02 가 박음).
**반대로 읽는 세 자리:**
ⓐ 같은 끝 기록이 미확인이라 recover 가 `chain_end` 로 옮기면 → `runner_rc_failed(None)` = False → parent_dead · 읽음 True
ⓑ 요약 있는 길 GROUP_UNCONFIRMED + 런 기록 {rc null · group_cause null} → group_unconfirmed
ⓒ 같은 멈춤에 그 런 기록이 없거나, group_cause 칸이 없음 (옛 판 꼴) → 재실행 자격
**실경로 관찰** (실제 git 원장 · Traceback 로그 · `probe_ledger_new.json`):
ⓐ recover 전 `orphan_cause` = runner_rc → recover 뒤 결과 줄 parent_dead · `resume_ok` True → `--add --resume` **rc 0 (허용)**. 대조 rc 1 = rc 3 RESUME_NOT_ALLOWED.
ⓑ group_unconfirmed · rc 0 (허용). 대조 rc 1 = rc 3.
ⓒ 단위 관찰 (G5 · G6).
**고침 전부터 있음** — 바탕 판 단위 탐침 R2 · G2 가 같은 값입니다. | 원인 None / group_cause None 자리에서는 정확한 정수 0 만 성공으로 봅니다. 'none' 은 실패 (by chain 과 같게 기본 runner_rc) 또는 읽음 False 로 둡니다.
· `chain_end_failed` = `cause is None and not rc_success(rc)`
· GROUP_UNCONFIRMED: 런 기록 없음 · group_cause 칸 없음 · 모르는 값 = 읽음 False. group_cause None + 성공 아님 = runner_rc 낱말 규칙. rc null 은 group_cause ∈ {timeout · signal · signal_after} 일 때만 "사슬이 죽인 런".
· RC04 · PE03u · LG01 기대값을 고치고, ⓐ ⓑ ⓒ 실경로 시험 (→ rc 3) 을 더합니다. |
| PB-02 | P3 (A2b 가 바꾼 범위 · 보고 밖) | `:6418–6421` `_verdict_compute` (+ `:5283–5287` `read_summary`) | `read_summary` 가 객체 아닌 JSON 을 None 으로 바꾼 탓에 판정 입력의 "단계 요약 하나" 검사가 느슨해졌습니다. 예측 요약 + `ladder_summary.json` = `[]` · `0` · `true` 인 폴더가 옛 판은 Stop INPUT_NOT_STAGE ("요약 2 개") 였는데 새 판은 통과합니다 (V1 · V2 · V4 관찰). 잘린 JSON 은 옛 판부터 무시했습니다 (V3). 판정값이 틀어지는 경로는 못 찾았습니다 (추정: 원장 판정은 폴더 sha 대조로 막힘). 같은 바뀜이 하나 더 있습니다: 합치기의 남은 런 목록 (`:6005`) 이 옛 판은 예외, 새 판은 조용히 건너뜁니다 (보고만 영향). | 판정 입력은 `read_summary_state` 로 읽고, 'unreadable' 이 하나라도 있으면 INPUT_NOT_STAGE 로 멈춥니다. REPORT §5 에 이 바뀜을 적습니다. |
| PB-03 | P3 (PA-04 와 같은 부류 · 고침 범위 밖) | `:3708–3714` `_read_group_json` · `:3303–3307` `read_attempt` · `:4023–4026` · `:7204–7206` (rejected.json `is_file` 뒤 `read_bytes`) | 그룹 끝 기록 · 시작 기록 · attempt.json 이 FIFO 이면 `orphan_cause` · `attempt_groups_problem` · `read_attempt` 가 **6 s 상한까지 막힙니다** (F1–F4 · 포크한 자식 · 관찰). 단계 요약 FIFO 는 막히지 않습니다 (F5 = 고침 동작). recover 가 멈출 수 있지만 재실행이 열리지는 않습니다 (가용성 문제). | 셋 다 `read_regular_file` 로 읽고 FIFO 시험 줄을 더합니다. |
| PB-04 | P3 (시험 가드) | `test_rint_r_chain.py:12765–12844` `rc_scan` (RC01) | 대조 5 꼴 (별칭 · 참거짓 · `int()` · walrus · 별칭 return) 은 잡습니다. 그러나 만든 반례 **17 꼴 중 16 을 놓칩니다**: dict 값 · `dict(kw)` · 다른 열쇠 첨자에 담았다가 비교 · `.rc` 속성 · `dict.get(er,'rc')` · pop · setdefault · itemgetter · match 열쇠 · 변수 열쇠 · 클로저 별칭 · `*args` · `getattr('get')` · `items()` 고리 · f-글 비교 · JSON 글. 지금 원천에는 그런 꼴이 없습니다 (독립 전수: 'rc' 자리 38 곳 = 판독 인자 · 기록 옮김 · f-글 · 생산자). | 'rc' 상수 · 키워드 · 속성 자리 전수를 허용 문맥 목록과 대조하고 (모르는 문맥 = 실패), 위 꼴을 `RC_SCAN_BAD` 에 넣습니다. |
| PB-05 | P3 (문구 · 범위) | `:3961` · 시험 CE01 제목 `:13194–13197` | A1b 의 "두 길 같은 답" 은 재실행 자격 (읽음 False) 만 같습니다. 원인 글은 다릅니다 (C1–C4 · 둘 다 자격 False):
· 모르는 원인 + MemoryError 로그: by chain parent_dead ↔ recover resource
· 모르는 원인 + ILLEGAL_ADDRESS 로그: by chain parent_dead ↔ recover runner_rc | 문장을 "재실행 자격이 같다 (원인 글은 로그 낱말에 따라 다를 수 있다)" 로 고칩니다. |
| PB-06 | P3 (굳히기) | `:3880–3884` `stop_log_readable` | 런 전 TIME_LIMIT 예외가 시작 기록 자리만 봅니다. 런 기록 · 시작 기록 · 로그는 없고 `<run>.end.json` 만 있으면 자격 True 입니다 (T4 관찰). 생산자는 끝 기록을 시작 기록 뒤에만 쓰므로 손 편집이 여러 번 필요합니다 (추정 · 위험 낮음). | 예외 조건에 끝 기록 · 런 폴더 흔적 없음을 더합니다. |
| PB-07 | P3 (문구) | 커밋 메시지 A1b 줄 | "CE01 · CE02 0/3 → 3/3" 의 셋째는 PE03u 입니다 (`logs/before_A1b_CE.log` = FAILED [PE03u, CE01, CE02]). | 이름 셋을 적습니다. |

## §2 주장 대조

| 주장 | 판정 | 근거 |
|---|---|---|
| 사슬 463/463 · 바탕 451 → 463 (+5 +2 +3 +2) | 참 (로그 · 3.11) | `final_chain_full_py311.log` · `before_chain_full_py311.log` · 산술 맞음. 다시 돌리지 않음 (제약). |
| 끝-끝 51 PASS · 0 FAIL / kgy 판 3.8.20 11 묶음 | 참 (로그만) | `final_e2e_py311.log` · `check_kgy_py38.out` · `py38/*.log` |
| RC 0/5→5/5 · CE 0/3→3/3 · LG 0/3→3/3 · SU 0/2→2/2 | 참 | 로그 + 내 실행: 새 시험 12 + PE03u = 고친 판 13/13 (11.4 s) · 바탕 판 0/13. 바탕 판 실패 사유는 동작 차이 (resume rc 0 ↔ 3 등) |
| 변이 40/40 | 참 (로그) | `mutation_rr2fix.json` = KILLED 40 · 생존 0 |
| Codex 탐침 310/311 · 다른 1 행 = 고친 결과 | 참 | `compare.json`: `known_PC6_05_summary_missing_log_resume` 만 다름 |
| SHA256SUMS 61 | 참 | `sha256sum -c` 61/61 OK · 파일 61 개 |
| 원장 무변경 (978) | 참 | findings 978 · diff 에 없음 |
| LG01 56 · CE01 27 · SU01 18 · LG03 8 · PE03u 나머지 43 | 참 | 변이 출력의 n (56 · 27 · 18 · 키 8 · 44) |
| "판독 함수 밖 rc 읽기 0" (RC01) | 지금 원천 = 참 / 가드 = 범위 한정 | 독립 전수 38 곳 · 스캐너는 세 꼴만 봄 (PB-04) |
| "rc 칸을 판독 한 함수로 · 소비자 전부" | **범위 한정** | 분류는 한 함수이지만 'none' 의 성공/실패가 소비자마다 반대 (PB-01) |
| "읽기가 바뀐 값은 false · 0.0 · −0.0 셋뿐" | 참 (기존 소비자) | RC05 표 · 변이 N1. `load_ladders` 는 새로 읽는 자리 (REPORT §5 에 적힘) |
| A1b "두 길 같은 답" | **범위 한정** | 자격만 같고 원인 글은 다름 (PB-05). rc null 은 자격도 다름 (PB-01) |
| "한 번 연 fd · FIFO · 바꿔치기에 막히거나 속지 않는다" | 참 (로그 · 단계 요약) / **범위 한정** | F5 · LG03 · N2 잡힘. 그룹 기록 · attempt.json 은 막힘 (PB-03) |
| 로그 상태 ok = 일반 파일을 읽음 | 참 (링크는 따라감) | `linkout` = ok. 링크는 `folder_digest` 가 결과 줄을 거부함 (코드 읽기) |
| 단계 요약 원자적 쓰기 · 바이트 = 옛 `write_json` | 참 | 두 경로 모두 `canon_bytes(_clean(s))` (코드) · W 탐침 같음 · tmp 파일 안 남음 |
| 못 읽는 요약 ≠ 요약 없음 | 참 (결과 줄 · 다시 셈 · recover) / 범위 한정 | SU 탐침. 판정 입력 · 합치기 목록은 옛 읽기 (PB-02) |
| "범위 바뀜 (모두 보수 쪽)" | **거짓** | V1 · V2 · V4: 판정 입력이 거부 → 통과 (PB-02) |
| 단계 요약 칸 꼴 틀림 = 옛 그대로 예외 (재실행 안 열림) | 참 (예외 관찰) · "안 열림" = 추정 | S1–S3 AttributeError. `recover_ledger` 는 Stop · OSError · ValueError 만 잡음 |
| RR2-02 문서 | 참 | 남은 "한 프로세스" 자리 = 취소선 · 11-05 표지 · 인용뿐 (grep) |
| RR2-03 ⑫ = 코드 한정어 바이트 그대로 | 참 | `verify_rr2_03_quote.py .` 다시 = ok (기록과 같음) |
| PA-01–07 고침 · PA-08 한정만 | 대체로 참 | PA-04 같은 부류 남음 (PB-03) · PA-05 빈틈 남음 (PB-04) |

## §3 변이 (리포 밖 git 없는 사본 · 한 번에 하나 · 되돌림 확인 True)

기준선 = RC05 · CE01 · LG01 · SU01 · SU02 5/5 PASS (6.4 s).

| 변이 | 바꾼 것 | 결과 |
|---|---|---|
| N1 | `rc_kind`: 실수 → 'none' | RC05 FAIL (0.0 · −0.0 · 1.0 · nan 행) — 잡힘. RC02 는 통과 (by chain 길에서는 'none' 도 runner_rc 이기 때문) |
| N2 | `O_NONBLOCK` 뺌 | LG03 FAIL (fifo_direct · fifo_orphan · fifo_summary 시간 초과) — 잡힘 |
| N3 | TIME_LIMIT 예외가 no_run 도 받음 | LG01 FAIL (TIME_LIMIT/no_run 등) — 잡힘 |
| N4 | `stage_summary_read` 의 status 검사 뺌 | SU01 FAIL (`{}` 행) — 잡힘 |
| N5 | `write_summary` → 비원자 `write_json` | SU02 FAIL — 잡힘 |
| N6 | recover 가지가 원인 `""` 를 아는 원인으로 | CE01 FAIL (`bad/recover/empty` 행) — 잡힘 |
| P1 (PB-01 고침 넣기) | `chain_end_failed` = 원인 None + `not rc_success` | **PE03u (`none_rcNone` 행) · RC04 (`chain_end_failed` 표) 만 FAIL** — 그 두 시험이 허용을 박아 둔 것을 확인 |
| P2 (PB-01 고침 넣기) | GROUP_UNCONFIRMED: 런 기록 없음 · group_cause None + 성공 아님 = 실패 | **LG01 `norecord_GROUP_UNCONFIRMED/clean` 만 FAIL** |

## §4 확인하지 못한 것

- 사슬 전체 · 끝-끝 · kgy 3.8 · check_all — 제약 때문에 로그로만 대조했습니다. 제 탐침은 3.11 에서만 돌렸습니다.
- 실제 SIGKILL · flock 경쟁 · 비root `/proc` · hidepid · GPU · NFS/FUSE 에서 막히는 읽기 · 아주 큰 파일의 메모리.
- PB-02 가 원장 판정 끝-끝에서 실제 판정에 영향이 있는지 (추정 = 폴더 sha 대조가 막음 · 실행 안 함).
- 단계 요약 칸 꼴 예외의 recover · `--add --resume` 끝-끝 경로 (예외 이름만 관찰).
- 이미 공개된 한정 (새 발견 아님):
  - `_src_done` 이 원인 None · 확인을 보지 않습니다. 복사한 팔은 `read_run` 이 다시 대조합니다.
  - 끝 기록이 없는 recover (`chain_end` 없음) = parent_dead (R8) 는 문서화된 옛 규칙입니다.
  - PA-08 은 한정만 둔 그대로입니다.
