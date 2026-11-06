> **복구판 (11-06)** — 11-05 원본 (잃은 판 안) 은 11-06 새벽 기계 교체로 유실됐다.  이 글은 세션 대화 기록에서 글 그대로 되살린 것이다 (아래 원문 무변경).  본문의 판 번호 · 줄 번호는 잃은 판 (origin 에 없음) 기준이고, 탐침 · 로그 (scratch pa2/) 도 유실됐다.  각 발견이 다시 만든 판의 어디에 놓였는지 = `docs/reviews/rint2_rr2_fix_evidence_20261105/REPORT.md` §7.

# 사전 공격 9 회차 (독립 · diff 만) — Rint ② 회차 ② 고침 (대상 a40aae399 = 본 가지 148197a7f..6308a8a64) · 11-05

- 수행 = 독립 에이전트 (고친 사람 설명 없이 · 1저자 10-20 규칙 ③) · 탐침 · 로그 = scratch pa2/ (리포 반입 = 다음 커밋) · 리포 변경 없음.
- 결론 = 고침은 주장대로 동작 (사슬 457/457 · 끝-끝 51/0 재실행) · 주장 8 중 7 참 (8 = 살아 있는 문서만 참) · 같은 부류 P2 1 · P3 7.

## 1. 발견 (줄 = a40aae399)
| id | 등급 | 자리 | 무엇 | 최소 고침 |
|---|---|---|---|---|
| PA-01 | P2 (RR2-01 과 같은 부류 · 같은 도달성) | `chain_end_failed` 3802-3806 · 3818-3821 · `orphan_cause` 3930-3931 ↔ 3933 / 3941 | 끝 기록 `cause` 칸을 두 길이 다르게 읽는다 — by chain 길: 모르는 · 꼴 틀린 cause (false · 0 · "" · [] · "weird") = (parent_dead, 읽음 False) = 재개 없음 · recover 가 같은 값을 `chain_end` 로 옮기면 (6956-6957) = (parent_dead, 읽음 True) = **재개 허용** (rc 1 + traceback 로그여도) · 재현 pa2/probe_cause_field.py | recover 길: `chain_end` 가 dict 가 아니거나 cause 가 None · run_in_group 이 쓰는 값 (timeout · signal · exception) 밖이면 읽음 False · 문서화된 None / timeout / signal / rc 0 은 그대로 · RC02 · PD13o 줄 보탬 |
| PA-02 | P3 | `load_ladders` 5457-5463 (r0run 거르개) | 예측 단계가 R_j,0 확인 런 기록의 rc 를 안 읽음 (`noop_check` 는 읽음) — rc false · 1 · null · "x" 여도 predict rc 0 · 러너 24 번 호출 (pa2/probe_r0rc.py) · 판정은 뒤에 REPLAY_MISMATCH 로 멈춤 (pa2/probe_r0rc_verdict.py) = 헛 계산 · 틀린 판정 아님 · `RC_ROUTES` 에도 빠짐 | 거르개에 `rc_success` (아니면 LADDER_SET) · RC_ROUTES 보탬 · RC03 줄 |
| PA-03 | P3 (PC6-05 부류 한 층 위) | `read_summary` 5231-5237 · 3998 · 7140 · 단계 요약 쓰기 5223 / 5393 (`write_bytes`) | 있는데 못 읽는 단계 요약 = 없음으로 처리 — 같은 바이트가 읽히면 stopped · chain_exception · 재개 False · 잘림 · 0xff 앞붙임 · 폴더면 interrupted · parent_dead · **재개 True** (pa2/probe_summary_unreadable.py) · 요약 쓰기가 원자적이 아님 · 효과 = 시도 한 번 더 | `read_summary` 세 상태 (ok · 없음 · 못 읽음 → 재개 없음) · 단계 요약 = `write_json_atomic` |
| PA-04 | P3 | `run_log_text` 3836-3845 | 검사 ↔ 읽기 사이 경합 — `is_file()` 뒤 `read_text()` 전에 FIFO 로 바뀌면 영구 대기 (pa2/probe_toctou.py · timeout 6 → 124) · FIFO 가드 (MA08) · 런 전 시간 상한 갈래의 못 읽음 ↔ 없음 (MA10) 시험 없음 | `os.open(O_RDONLY\|O_NONBLOCK)` + `fstat` 정규 파일 확인 + fd 읽기 · FIFO 시험 줄 (하위 프로세스 · 시간 상한) |
| PA-05 | P3 (시험 가드) | `scripts/test_rint_r_chain.py` 12735 (`rc_scan` · RC01) | RC01 "소스 전체" 훑기가 좁다 — 피연산자가 글자 그대로 `rc` · `X.get('rc')` · `X['rc']` · `type()` 일 때만 · 별칭 (`code = er.get('rc'); code == 0`) · 감싼 값 (`int(rc) == 0`) · 참거짓 (`rc or 0` · `not er.get('rc')`) 놓침 · MA03 · 04 · 05 가 RC01 을 지나 기능 시험에서만 잡힘 · 지금 모듈엔 그런 읽기 없음 (pa2/scan_rc.py) | rc 값 읽기 (그 값을 받은 이름 포함) 를 rc_kind 밖에서 전부 표시 (세 판독기 직접 인수 · 단순 복사 제외) |
| PA-06 | P3 (문구) | `docs/reviews/codex_rint2_rr_round1_request_20261024.md` 130 | RR2-02 문장의 표지 없는 사본 하나 ("float 같음 대조는 한 프로세스 안에서만 뜻이 있다 …") · 회차 ② 요청서 374 와 같은 종류 (발송한 요청서) | 같은 11-05 정정 표지 |
| PA-07 | P3 (문구 · RR2-03 이 이름 댄 두 곳 밖) | 원장 RINT2-L01 (제목 + 11-03 넓은 한정어를 코드 한정어로 인용한 메모) · `docs/reviews/codex_rint2_rr_round2_request_20261103.md` 347 | 둘 다 "해석 시험 통과 (… 시험 BAN8)" 에 "같은 두 곧은 나란한 레일에서만" 없음 | 좁힌 한정어 또는 그 자리 가리킴 |
| PA-08 | P3 (고침 전부터 · 안전 쪽) | 4657-4659 + `stop_cause` · `stop_log_ok` | 봉인 그래프 원천 런 중 신호 = 오분류 — 멈춤 RUNNER_RC · 런 이름 `G01_<run>_a<i>` · 원인 찾기가 `s['runs']` (그래프 원천 기록은 다른 자리) 와 `<attempt>/logs/` (로그는 `graph_src/logs/`) 를 봄 → 원인 runner_rc (signal 아님) · 로그 못 읽음 (pa2/probe_gsig.py) · 재개 안 됨 = 안전 쪽 | 선택: G 런 · 로그를 `GRAPH_SRC_DIR` 아래에서 찾기 |

못 찾은 부류: rc 칸 (모든 읽기가 rc_kind · rc_success · runner_rc_failed · NaN · inf · 2**70 · "0" · "" · [] · {} · True · 1.0 · None = 실패) · 로그 이름 · 파일 꼴 공격 (/ · .. · 앞 . · - · 빈 · None · 비글자 · NUL · 줄바꿈 = 이름 없음 · 폴더 · 장치 · FIFO · 그 링크 · 권한 · 252+ 글자 = 못 읽음 · 깨진 링크 = 없음 · 빈 · 비 UTF-8 = 읽음 · Python 3.8.20 · 3.11 · 3.12 · 3.13 같음) · 런 전 시간 상한 예외 (실제로 죽은 런은 못 닿음 — 기록 · 시작 기록 · 로그 셋 다 지우고 원인 칸을 위조해야 · 결과 줄 뒤엔 폴더 지문 · 다시 셈이 거부) · `orphan_cause` "동작 그대로" (사슬이 쓰는 이름에선 참 · 손으로 만든 이름 · FIFO 로그만 다름 · 둘 다 안전 쪽).

## 2. 주장 대조
| 주장 | 판정 | 근거 |
|---|---|---|
| (1) 457/457 | 참 | 재실행 457/457 (681 s · 3.11.15) · 모듈 · 시험 해시 = env.txt |
| (2) 끝-끝 51/0 | 참 | 51 · 0 (1232 s) |
| (3) 판독기 밖 rc 비교 없음 | 참 | 넓은 AST 훑기 (참거짓 포함) 0 · 한정 = PA-02 · PA-05 |
| (4) false · 0.0 · −0.0 만 바뀜 | 참 | JSON 값 22 × 소비자 전부 (pa2/probe_rc_oldnew.py) · "0e0" = 0.0 · `== 0` / `!= 0` 쓰던 다섯 소비자에서만 |
| (5) LG01 56 중 26 True→False · 원인 그대로 | 참 | 커밋된 before_LG.json · 새 LG01 을 고치기 전 모듈로 = 26/56 · 26 줄 원인 · side 같음 · 나머지 30 정확히 같음 |
| (6) q9 출력 바이트 같음 | 참 | docstring 만 · 두 판 재실행 같음 · 커밋된 after 와 같음 |
| (7) BAN8 글 그대로 · 한 번 | 참 | 179 글자 = CJUNC_QUALIFIERS[3] (147–148 · R̄ = U+0052 U+0304) 의 바이트 같은 부분 · 초안에 한 번 |
| (8) 다른 활성 "한 프로세스" 문장 없음 | 살아 있는 문서 · 코드 = 참 · 발송 요청서 포함하면 거짓 | 남은 자리 = 취소선 · 정정됨 · 지적 인용 · 다른 뜻 · 예외 = 회차 ① 요청서 (PA-06) |

## 3. 변이
- 새 시험을 고치기 전 모듈로: RC01–RC04 · LG01 · LG02 = 0/6 (옳은 이유 · pa2/old_RC_LG.out).
- 고친 사람의 mutate_rr2.py 다시: 17/17 잡힘 (같은 실패 검사).
- 독립 변이 17 (RC0 · LG0 · PD13 · 기준 11/11): 14 잡힘 · 3 생존 = MA08 (`is_file()` 가드 뺌) · MA10 (OSError 를 "없음" 으로) · MA12 (시작 기록 검사 = `is_file()` 만).
- 안 돌림 (미확인): kgy 3.8 게이트 (커밋된 로그 = 통과) · check_all.sh.
