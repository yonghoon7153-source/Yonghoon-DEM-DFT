# Codex 재검증 4 요청 — 접촉망 세대 2 · G2RR3-01 · 02 수정 (10-07)

- **대상**: 브랜치 `claude/stoic-knuth-NObVQ` · **이 요청서가 들어간 커밋** (핀은 1저자가 보낼 때 그 커밋 sha 로).
- **앞 판정**: `docs/reviews/codex_review_gen2_network_reverify3_20261007.md` (핀 `0801d4ceb` · 194 · v1.3 HOLD · 새 P1 없음 · 새 P2 `G2RR3-01` · `G2RR3-02`) ·
  우리 트리 재현 = 판정값 차이 0 (`docs/reviews/codex_gen2_network_reverify3_evidence_20261007/_README_import.md` §2).
- **1저자 비준**: 10-07 *"ㄱㄱ"* (판정문 §3 · §4 최소 해결 증거 그대로 고치는 계획).
- **봉인**: 32 파일 · `code_fp e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` **그대로** — 고친 파일 = 실행기 (`scripts/run_network_194_parallel.py`) ·
  다시 읽기 (`scripts/g2_network_reread.py` · 인계 도구 지문 = 발사 때 기록) · 배포 생성기 (`scripts/lhs_release_build.py`) · 시험.
- **이 요청에 붙일 것 (1저자 · WSL)**: 등록 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` §1 사전 점검 전체 로그 — 각 단계 **원 프로세스 rc 와 전체 출력**
  (tail · grep 만이 아니라 · 판정문 §8-4) · 시범 3 케이스 `--observe-imports` 의 영수증 폴더 · audit JSON · 다시 읽기 JSON v3.

## 1. G2RR3-01 — v1.3 배포 관문 (`3f9f86f59`)

| 판정문 최소 해결 증거 | 구현 |
|---|---|
| ① 배포에서 증거 부재 · 손상 · 타입 결손 거부 · 옛 기록은 비배포 진단 모드로 | 관문 함수 하나 `v13_batch_gate_problems` — `seal_audit.json` · `reread.json` 둘 다 필수 · 없음 · `{` · null · {} · 타입 · 실패 = `ReleaseError`.  옛 기록 = `--diagnostic-batch-gate` (README 첫 줄 · 빌드 manifest `NOT FOR RELEASE` · 리포 안 · `--dry-run` 과 함께 거부 · 배포 check 거부) |
| ② 감사 = 해시만이 아니라 자격 · 실패 predicate · 등록 집합 · 실행 신원 | eligibility current · refused 아님 · 봉인 상태 **SEALED 만** · merged 차이 0 · 세대 · 입력 · import 문제 0 · code_root_changed_now 0 · 감사 `launch_sha` = manifest · 감사 행 = 등록 production194 ID 지문 · 요약 수 = 행 재계수 |
| ③ 다시 읽기 = 이번 ROOT · 봉인의 증거 | `g2_network_reread` JSON v3 = `launcher_root` · 읽은 바이트의 `manifest_sha256` · `seal_fp` · `launch_sha` → 관문이 배치 뿌리 realpath · manifest · `seal.code_fp` (= `code_fp(code_hashes)`) · git sha 와 대조 |
| ④ build · check 같은 관문 · 6 변이 거부 · 정상 생성 | build_v13 · stage_handovers_v13 · check_v13 가 같은 함수 · check = 빌드에 기록된 배치 뿌리에서 재평가 (기록 sha256 ≠ 지금 · batch_gate 없음 · 뿌리 없음 = 실패) |

- 시험: `scripts/test_lhs_release_v13.py` 새 시험이 옛 코드에서 81/135 → **135/135** (V17a 결합된 정상 생성 · V17b · V17c = Codex 여섯 + 명시 n_fail=1 + 같은 부류 26 변이 build · check 둘 다 거부) ·
  `g2_network_reread --selftest` 15/17 → 17/17.  Codex `docs/reviews/codex_gen2_network_reverify3_evidence_20261007/probes/release_gate.py` 무변경 = 8 변이 전부 거부 (그 `pass_control` 도 — 옛 결합 없는 모양이라 · 새 계약의 정상 대조 = V17a).

## 2. G2RR3-02 — import 관측 완결성 (`66c09ef68`)

| 판정문 최소 해결 증거 | 구현 |
|---|---|
| ① 완료 케이스 · 시도 · 단계 ↔ 관측 프로세스 시작 · 종료 영수증 결합 | 훅 = 시작 영수증 `<pid>-<8hex>.start.json` + 끝 `<pid>-<8hex>.txt` (JSON 머리 + 모듈) · 신원 `NP194_OBS_RUN_ID` · `RUN_NO` · `CASE` · `ATTEMPT` (run_queue 가 시도마다 · 하위 프로세스 상속 · manifest `import_obs_run_id`) |
| ② 원자적 최종화 · 신원 · 필수 핵심 모듈 | 둘 다 tmp + `os.replace` · 훅은 예외를 내지 않는다 · 필수 역할 = 워커 (`scripts/lhs_webapp_batch.py`) · 망 솔버 (`scripts/network_conductivity.py` 가 `__main__`) |
| ③ 빈 · 무효 · 누락을 실제 audit 로 거부 | 빈 · 머리 없음 · 잘림 · 짝 없음 · 남의 신원 · 코드 뿌리 밖 줄 · 완료 시도의 미최종 · 필수 역할 누락 = rc 1 · CODE_FILES 밖 모듈 (그대로) |

- 시험: 실행기 `--selftest` 82/82 → 새 시험이 옛 코드에서 84/100 → **100/100** — Codex 다섯 변이 rc 1 (전: 1 · 0 · 0 · 1 · 0) · 새 형식 아홉 변이 rc 1 ·
  망 솔버 없는 완료 시도 rc 1 · 정상 rc 0 · ㉟d 실제 `run_pipeline(stop_after='network')` 통과 · ㉟d2 시작 4 = 최종 4 · 단계 하위 프로세스까지 신원 전파.
  Codex `docs/reviews/codex_gen2_network_reverify3_evidence_20261007/probes/new_gates.py` 무변경 = IMPORT 다섯 전부 rc 1.
- 덤 발견: CPython 은 `sys.exit` 없이 끝나는 스크립트의 `__main__.__file__` 을 atexit 전에 지운다 → 옛 훅은 그 프로세스의 자기 스크립트 (망 CLI · 피복 단계) 를 빠뜨렸다 → 시작 때 `sys.argv[0]` 로 넣는다.

## 3. 질문

- **Q1.** 봉인 상태 = **SEALED 만** (실행기 audit 가 rc 0 을 주는 `SEALED_DIRTY_ALLOWED` · `SEALED_LEGACY` 도 배포는 거부 — 등록 §5-2 "기록 전부 SEALED").  동의하나?
- **Q2.** 완료되지 **않은** 시도 (SIGKILL · 중단 · 실패) 의 미최종 영수증 = 기록만 (거부 안 함) — OOM 한 번이 성공한 재시도 뒤 감사를 막지 않게 (시험 = 충돌 → 재시도 rc 0).  "완료 시도" = `worker.json` outcome done/partial + 지금 레코드를 쓴 시도.  이 좁힘이 판정문 ③ 과 맞나?
- **Q3.** 남는 틈: `-I` · `-E` 로 뜬 프로세스는 훅을 건너뛴다 (필수 역할 누락은 잡힌다) · fork 뒤 import 는 못 본다 (생산 경로에 multiprocessing 없음).  194 본 실행도 관측을 켜는 것 (판정문 §4-5 권고) 을 등록에 넣는다 — 충분한가?
- **Q4.** 빌드 manifest 가 배치 뿌리 **절대 경로** 하나를 적는다 (check 가 그 자리에서 재평가 · 옮긴 뿌리는 관문 실패 = 설계).  이 결합 방식에 이의가 있나?
- **Q5.** 붙인 WSL 사전 점검 로그 (등록 §1) 로 판정문 §8-4 를 닫을 수 있나 — 남는 것이 있으면 발사 전 최소 목록.
