# Codex 발송 프롬프트 — REIL C4-E · E1 실행 승인 요청 사전 검토 · 2026-10-15 KST

> E0 한정 정정 결과 검토 회신 (상태 문서 §72 — E1 승인 요청서 작성 허용 · 실행 승인 아님) 의 조건 1–5 를 반영한 E1 승인 요청이다.
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부할 것은 없다 (검토자가 저장소에서 읽는다).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

REIL C4-E · E1 (원자료 반입 · E3a 66 호출) 실행 승인 요청을 사용자 승인 전에 사전 검토해 주세요. 지난 회신 (§72) 대로 요청서만 썼고, launcher 복사 ·
시험 · 읽기 경로 확보 · fetch · 자료 개봉 · run 은 모두 0 회입니다. 초안 셋은 `.py.txt` 로 고정했고 정적 검사 (AST 파싱 · 이름 검사 · 비밀 검사) 만 했습니다.
브랜치 `claude/14-gate-code-review-9qkx05` 의 최신 HEAD (이 발송문이 든 커밋) 를 기준으로 보시면 됩니다.

## 1. 볼 것

| 파일 (bms-balancing 기준) | sha256 | 무엇 |
|---|---|---|
| `docs/REIL_C4E_E1_APPROVAL_REQUEST_20261015.md` | (이 커밋의 바이트) | E1 승인 요청 — §72 조건 1–5 의 고정 · 순서 · 예산 · 중지 · 제출 경계 · 밝힐 것 |
| `docs/REIL_C4E1_LAUNCHER_DRAFT_20261015.py.txt` | `c5bc40a474372e282706ad9069405fbb8bd9238ca26908478056bca2c20f30ff` | launcher 고정 구현 (stdlib · 실행 모듈 밖) → `scripts/reil_c4e1_launch.py` |
| `docs/REIL_C4E1_LAUNCHER_SKELETON_DRAFT_20261015.py.txt` | `d202a716b652ffcbcd12250474ee80b67000b7355542882d53cd431593a4b458` | RED 골격 (import · 상수 동일 · 함수 26 개 = NotImplementedError) |
| `docs/REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_20261015.py.txt` | `0b06905a289b78ba788faa859acb433448465b0eba073dee22c87e7bf4b2fca4` | 대조 14 → `tests/test_reil_c4e1_launch.py` |
| `docs/REIL_PREREQUISITES_STATUS_20261004.md` §72 | — | 지난 회신의 접수 기록 (보존 `reviews/review_reil_c4e_e0_fix_20261015/`) |

## 2. 요청서의 뼈대 (§72 조건 ↔ 요청서)

| §72 조건 | 요청서 | 요지 |
|---|---|---|
| 1 식별 | §1 | SOURCES.json `2a7b2b49…` · 다섯 파일 · 구현 커밋 `61b9037e` · 실행 경로 / cwd · 초안 셋 · helper (`92bb3bca…`) · 자료 · 봉인 · venv |
| 2 독립 사전 대조 | §2 | 세 자식 (identity · fetch · run) 모두 앞 · 목록 · 다섯 모듈 (일반 파일 · resolve 일치) · 실행 스크립트 · 해석기 플래그 · `-c` 탐침의 sys.path 섀도 검사 · 자료 · 실패하면 자식 0 + `launched false` 기록 · 연결 사슬 (§2-3: argv 경로 · run 의 sys.path[0] · 네임스페이스 · 섀도 없음 · `-B -X pycache_prefix` · `IDENTITY.json` 결속) |
| 3 단계 수용 | §4 | precheck_ok AND child_ok (run = `ok` AND `final.complete`) AND rc 0 AND timeout false AND **postcheck_ok (더한 항)** · run 모듈의 `stage_verdict` 는 사전 대조를 포함하지 않아 쓰지 않음 |
| 4 fetch argv / env | §3-2 · §3-3 · §3-4 | 고정 argv · git 다섯 단계 (URL · 커밋 · 두 경로 · no-checkout · named origin · `GIT_ALLOW_PROTOCOL=https` · `GIT_TERMINAL_PROMPT=0`) · env 에서 토큰 · `GIT_CONFIG_*` · ASKPASS 제거 · 프록시 · CA 유지 · 실패 시 대체 출처 · 재시도 0 |
| 5 범위 · 예산 · 출력 · 중지 · 제출 | §5 · §6 | E1-0 (launcher RED 120 s · GREEN 600 s) → identity 60 → `add_repo` → fetch 300 → run 10,800 s · 계산 합 ≤ 12,060 s · 전체 6 h · 첫 예상 밖 실패에서 멈춤 · `SP/c4e1/` (자료 · git · pycache) 커밋 0 · 50 MB 규칙 |

## 3. 밝힐 것 (요청서 §8 의 요지)

1. launcher 는 새 검증 코드다 — 근거는 대조 14 와 정적 검토뿐이고, 실제 환경의 첫 실행이 E1-1 이다.
2. 단계 판정에 사후 대조 (모듈 · 자료 재해시 · `IDENTITY.json` 결속 · pycache 0 · 그룹 0) 를 더했다 (§72 의 넷보다 엄격).
3. TOCTOU (사전 대조 ↔ import · 시작 대조 ↔ 끝 재해시) 는 연속 감시가 아니다. 해석기 · stdlib · site-packages · sitecustomize · `.pth` 는 launcher 밖
   (C4-ENV identity 범위).
4. identity 를 fetch 앞으로 옮겼다 (v3 §7 과 다름).
5. 이전 라운드의 `-I` 자식은 `-B` 없이 돌아 `scripts/__pycache__/` 에 바이트코드를 남겼다 (7 개 · 지우지 않음). E1 자식은 `-X pycache_prefix=<새 빈 폴더>` 로
   그것을 읽지 않는다.
6. 네트워크 성공 · 지연 blob 읽기 · 프록시 정책은 미검증 — 실패하면 멈추고 다른 출처로 바꾸지 않는다.

## 4. 질문

- Q1. §72 조건 1–5 가 요청서에 빠짐없이 고정됐는가.
- Q2. launcher 의 사전 대조와 §2-3 의 연결 사슬이 "run 프로세스 시작 전 · 실행 모듈 밖 · checker / 명령 / 입력 고정 · 실제 실행 / 적재 경로와 대조 경로의
  연결" 을 충족하는가. 남는 틈 (§8 의 3 · 4) 의 경계가 맞는가.
- Q3. 대조 14 · RED 선언 (14 실패 · 모두 NotImplementedError) · GREEN 41 이 launcher 의 실패 분기를 충분히 덮는가. 빠진 음성 대조가 있는가.
- Q4. fetch 의 env 처리 (제거 · 유지 목록) 와 실패 시 멈춤 규칙이 맞는가.
- Q5. 사후 대조 항을 단계 판정에 더한 것 · identity 를 fetch 앞으로 옮긴 것을 받아들일 수 있는가.
- Q6. E1 을 한 번의 승인 (E1-0 → E1-4 · 첫 예상 밖 실패에서 멈춤) 으로 진행해도 되는가, 아니면 E1-0 결과 검토를 먼저 거쳐야 하는가.

## 5. 경계

이 발송은 실행 지시가 아닙니다. 초안 · 시험 · 자료 · 네트워크 fetch · run · C4-A / B · COMSOL 은 모두 0 회이고, E1 은 이 사전 검토 뒤 사용자의 별도 승인이
있어야만 시작합니다.

---
