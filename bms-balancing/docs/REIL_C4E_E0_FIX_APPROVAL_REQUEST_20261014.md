# REIL C4-E · E0 한정 정정 (C4E-E0-N1 — 다섯 모듈의 신뢰 기대 sha) 승인 요청 · 2026-10-14

> 근거: E0 결과 검토 회신 (상태 문서 §69 · `reviews/review_reil_c4e_e0_result_20261014/`). 회신 원문: "다음에는 **N1 한정 정정 범위·검증안·예산을 먼저
> 제시**하고 사용자 별도 승인 전에는 수정 시험·자동 재시험·E1 fetch/run·C4-A/B·COMSOL을 시작하지 말아 달라. 이 회신은 그 실행 승인이 아니다."
> 이 문서는 승인 요청이다. 승인 전에는 저장소의 코드 · 시험을 바꾸거나 돌리지 않는다 (§1 의 두 파일은 `docs/` 의 고정본이고 pytest 가 모으지 않는다).

## 1. 먼저 고정한 것 (승인 전 · 실행 0)

| 대상 | 파일 | sha256 |
|---|---|---|
| 대조 (시험 6) | `docs/REIL_C4E_E0_FIX_CONTROLS_DRAFT_20261014.py.txt` | `7a09d4386a740e9eba9145372e59ed7e1385ce5523fd7ce38dc095d5e4053bd2` |
| 변경부 (패치 · hunk 12 · +127 / −20) | `docs/REIL_C4E_E0_FIX_PATCH_DRAFT_20261014.diff` | `ed14409a54613e8bc3c309cabebcd564559bc651fbaa38e258d64cdf3e38594f` |
| 패치 전 (지금) | `scripts/reil_c4e_run.py` | `0a9ddb83531a1816e3c9505487fd7f2d1a211d2753be9fdc1c8f5c94866aff1b` (E0 구현 · `57dfe290`) |
| 패치 뒤 기대 | `scripts/reil_c4e_run.py` | `a94f535fd8ab5718b0ed47e0322a067300f808ef42c530cd95668aa77f0a53a9` |

확인은 정적인 것만 했다 (대상 코드 · 시험 실행 0):
- 패치: `git apply --check` 통과 · scratch 사본에 적용한 결과 = 기대 sha · ast parse · symtable 미해결 이름 0 · 모듈 속성 대조 (`e3a.` · `mon.` · `c5.` · `p0.`)
  누락 0 (`__file__` 넷은 모듈 기본 속성이라 검사기의 오탐).
- 대조: ast parse · 미해결 이름 0 · 시험 6 (매개변수화 없음). 대조가 쓰는 `run.*` 21 이름은 패치 뒤 모두 있다.
- E0 시험 21 (`tests/test_reil_c4e.py` · 바이트 그대로 둔다) 이 쓰는 `run.*` 이름 · 키워드 인자는 패치 뒤 서명과 모두 맞는다.

## 2. 신뢰 근거 · 경로 집합 · 누락 거부 (회신이 함께 명시하라고 한 것)

- **목록:** `SOURCES.json` (schema `reil-c4e-sources-v1`) — 다섯 모듈의 sha256 · bytes. 자기 파일에 자기 해시를 넣지 않는다.
- **정확한 경로 집합 (`bms-balancing/` 기준 · 정확히 다섯):** `scripts/reil_c4e_run.py` · `scripts/reil_c4_e3a.py` · `scripts/reil_c4_monitor.py` · `scripts/reil_c5_pilot.py` ·
  `scripts/reil_p0.py` (`MODULE_RELPATHS`). 실행 모듈이 실제로 읽는 집합 (`_module_files()`) 과 다르면 멈춘다.
- **신뢰 근거는 목록 파일이 아니라 목록 바이트의 sha256 이다.**
  1. 이번 정정에서 `seal-sources` 가 구현 커밋의 바이트로 목록을 쓰고, 목록 sha256 과 다섯 sha 를 결과 기록 (§) 에 적는다.
  2. 검토자가 그 다섯 sha 를 고정 커밋의 파일 바이트와 독립 대조한다.
  3. 사용자 E1 승인 기록이 그 목록 sha256 을 인용한다.
  4. E1 run 은 `--sources` · `--sources-sha256` 를 **기본값 없이** 받는다 — 봉인 MANIFEST 를 `--seal-manifest-sha256` 로만 받는 것과 같은 방식이다.
  다섯 모듈 중 하나라도 바뀌면 바이트 대조가 실패하고, 목록을 같이 바꾸면 목록 sha 가 고정값과 달라진다.
- **거부 조건 — 모두 util import · 자료 적재 · 작업자 시작 전에 `E3aStop`:** 목록 / sha 중 하나만 줌 · sha 인자가 소문자 16 진 64 자가 아님 · 목록 바이트 sha ≠ 고정값 ·
  JSON 아님 · schema 다름 · **경로 누락 (기대 항목 누락)** · 목록 밖 경로 · 항목의 sha256 (소문자 16 진 64) / bytes (정수 ≥ 0) 형식 · 실제 모듈 바이트 (sha · 크기) ≠ 목록.
- **수용 판정:** 같은 기대값 (목록) 을 시작 · 끝 표 모두에 넣는다. 필수 행 10 (`REQUIRED_IDENTITY` = 입력 다섯 + 모듈 다섯) 의 행 없음 · 기대 누락 · 시작 표 ≠ 기대 ·
  끝 표 ≠ 기대 · 시작 ≠ 끝 이면 조건 6 이 거짓이고 E3a 는 INCOMPLETE (사전 · 최종) 다.
- **남는 한계:** 실행 모듈 자신이 고의로 바뀌어 자기 대조를 건너뛰면 run 안의 검사로는 막지 못한다 (자기 검사의 한계). 우발적 변경 (다른 커밋 · 덮어쓰기 · 잘못된 판) 은 막는다 —
  run 은 자기 파일 바이트도 다시 읽어 목록과 대조한다. 독립 사전 대조는 E1 단계 실행기에 넣자고 권한다 (§7).

## 3. 생산 변경 — `scripts/reil_c4e_run.py` 한 파일 (감시 · e3a · c5 · p0 · 기존 시험 · E0 증거 그대로)

| 고치는 곳 (패치 뒤 행) | 내용 |
|---|---|
| 상수 (66–71) | `MODULE_RELPATHS` · `SOURCES_SCHEMA` · `INPUT_NAMES` · `REQUIRED_IDENTITY` |
| `load_sources` (504–532 · 새) | §2 의 거부 조건 전부 · 통과하면 다섯 모듈의 기대값 |
| `seal_sources` (535–558 · 새) | 다섯 모듈의 지금 바이트 → 새 폴더의 `SOURCES.json` 하나 (이미 있으면 거부 · 재읽기 확인) |
| `identity_problems` (322–) | 인자 `required` — 필수 행의 행 없음 · 기대 누락을 문제로. 주지 않으면 예전 그대로 (기대 None 은 건너뜀) |
| `pre_verdict` (345–) | 인자 `required` · 조건 6 에 **끝 표의 기대 대조**를 더함 (예전엔 시작 표만) · 반환에 `required_identity` |
| `prepare` (562–) | 인자 `sources` · `sources_sha256` — 하나만 주면 멈춤 · 둘 다 주면 identity 뒤 · 시작 sha 표 앞에서 목록을 읽어 모듈 기대값을 채우고 필수 행을 강제 · 머리말에 `sources` · 반환에 `required` |
| `finalize` · `execute` | `finalize(…, required=())` · `execute` 가 `prep["required"]` 를 넘긴다 |
| `run` | 인자 `sources` · `sources_sha256` 를 `prepare` 로 |
| CLI (`build_parser` 796– · `main`) | `run` 은 `--sources` · `--sources-sha256` 필수 (기본값 없음) · 하위 명령 `seal-sources --out` |

- **legacy:** 라이브러리에서 목록 없이 부르면 (E0 시험 경로) 예전 그대로이고, 머리말 기록에 `legacy` 로 남는다. 기존 시험 파일 (E0 21) 을 고치지 않고 바이트 그대로
  GREEN 에 넣기 위해서다. E1 은 CLI 로만 부르고, CLI 는 목록 없이는 인자 해석 단계에서 거부한다 (n1_e).
- **plan-e 는 바꾸지 않는다** — `identity_ok` 는 환경 + 명시 기대 항목의 통과로만 읽는다 (모듈 출처 확인 아님 · n1_f 가 PLAN_E 의 모듈 행 기대 없음을 고정).

## 4. 대조 6 — 검토 회신의 검증 축 · 지금 코드 (패치 전) 에서의 RED 예상

| ID | 검증 축 | 단언 요지 | RED (패치 전) |
|---|---|---|---|
| n1_a | 정상 기대값 | 실제 다섯 바이트로 만든 목록 → prepare 통과 (순서 identity → 목록 → sha → 경로) · 모듈 행 기대 = 목록 · 필수 행 10 · 같은 기대값으로 끝 재해시 → **실제 finalize** 사전 · 최종 COMPLETE · IDENTITY.json 끝 표에도 같은 기대값 | AttributeError — `load_sources` 없음 |
| n1_b | 기대 항목 누락 · 형식 · 목록 sha | 넷만 · 목록 밖 · sha 63 자 · 대문자 · bytes 음수 · schema 다름 · 목록 sha 불일치 · 목록 / sha 하나만 → 모두 멈춤 · util import 0 · 출력 폴더 없음 · 수용 판정에서 필수 행의 기대 누락 · 행 없음 → INCOMPLETE (required 없으면 예전 그대로) | TypeError — `prepare` 에 `sources` 없음 |
| n1_c | 시작부터 틀렸으나 끝까지 같은 소스 | 목록의 e3a 기대값 ≠ 실제 → prepare 가 util import · 적재 전에 멈춤 · 사유에 경로 · 시작 표 = 끝 표여도 기대와 다르면 INCOMPLETE · C4-A 관문 거짓 | TypeError — `prepare` 에 `sources` 없음 |
| n1_d | 실행 중 변화 | 다섯 모듈 사본 (tmp) · 끝 재해시 직전에 monitor 사본이 바뀜 → **실제 finalize** 사전 · 최종 INCOMPLETE · IDENTITY.json `changed` · 기록 파일 보존 · 바뀐 바이트를 기대에 다시 올린 대조는 COMPLETE | TypeError — `identity_problems` 가 `required` 를 받지 않음 |
| n1_e | CLI 가 목록을 요구 | `run` 에 `--sources` / `--sources-sha256` 가 없거나 하나만이면 argparse 거부 · 둘 다 주면 해석 · `seal-sources` 있음 (해석만 · 실행 경로 0) | AttributeError — `build_parser` 없음 |
| n1_f | 목록 작성 · plan-e 범위 | 새 폴더에 SOURCES.json 하나 · 경로 정확히 다섯 · sha / bytes = 실제 (시험이 따로 계산) · 이미 있는 폴더 거부 · 되읽기 같음 · PLAN_E 의 모듈 행 기대 없음 | AttributeError — `seal_sources` 없음 |

- **RED 예상: 6 실패 = AttributeError 3 (n1_a · n1_e · n1_f) + TypeError 3 (n1_b · n1_c · n1_d).** 다른 종류가 나오면 원문을 보존하고 멈춘다.
- RED 의 한계 (인터페이스 수준) 는 E0 와 같다. 틀린 구현을 잡는 근거는 GREEN 의 음성 대조다.

## 5. 실행 순서와 배정 (승인하면)

1. 승인 기록 (상태 문서 §70) · 보존 규칙 (`evidence/reil_c4e0_fix_20261014/** -text`) 커밋 → 착수 기록 (폴더가 있으면 중지).
2. identity 1 회 (60 s) — E0 와 같은 스크립트 · 인자.
3. 대조 고정본을 `tests/test_reil_c4e_fix.py` 로 바이트 복사 (sha 확인) → **RED 1 회 (600 s)** — 새 6 만.
4. 패치 고정본 `git apply` (적용 뒤 sha = `a94f535f…` 확인) → 정적 검토 → **GREEN 1 회 (600 s)**: `tests/test_reil_c4e.py` (E0 21 · 바이트 그대로) + `tests/test_reil_c4e_fix.py` (6) = **27**.
5. 구현 · GREEN 증거 커밋 → **`seal-sources` 1 회 (60 s · CLI)** → `SOURCES.json` (다섯 sha · 목록 sha256 은 결과 기록에).
6. 끝 기록 · 비밀 검사 · 커밋 · push · 결과 기록 · 재검토 발송문을 쓰고 멈춘다.

- **배정:** 계산 1,320 s (60 + 600 + 600 + 60) · 전체 작업 2 h · 자동 재시험 0.
- **자원:** 사후 관측 (최대 단일 자식 RSS ≤ 4 GiB · 증거 ≤ 64 MiB · 착수 때 디스크 여유 ≥ 5 GiB).
- **참고:** E0 GREEN 의 E0 21 부분은 수 초였다 (E0 180 전체 43 s 의 대부분은 0a · 0b 시험) — 기록값 · 보증 아님.

## 6. GREEN 의 계산 (이번 GREEN 1 회에만 · 새로 묻는 예외)

- **기존 0a · 0b 시험 159 는 넣지 않는다.** 패치가 `reil_c4e_run.py` 하나만 바꾸고 그 시험들은 이 모듈을 import 하지 않는다. 그래서 이번 GREEN 의 실제 pymoo ·
  COBYQA · 보존 util 사본 · Sobol 생성은 0 이다.
- **E0 21 (바이트 그대로):** 실제 fork 세션 5 (m_1 1 · r_6 (a)(b) 2 · s_4 2 · 가짜 작업 / 가짜 util · 상한 6) · 가짜 util 평가 393 (≤ 2,000) · 로컬 git 직접 호출 16 (+ git 의
  하위 프로세스 · GIT_ALLOW_PROTOCOL=file · 네트워크 0) · plan-e 1 (가짜 identity). E0 승인 때와 같은 계산이다.
- **새 6:** fork 0 · optimizer 0 · 가짜 util 적재 (목적 평가 0 — 그 util 의 `run_optimization` 은 부르면 예외) · 다섯 모듈 파일 읽기 · 임시 폴더 기록 · plan-e 1 (가짜 identity).
- **실패 중지:** 600 s 초과 · 예상 밖 실패 → 원문을 보존하고 멈춘다 (자동 수정 · 재시험 0).

## 7. E1 로 넘기는 것 (지금 승인하지 않는다 · E1 승인 요청에 넣는다)

- **E1 단계 실행기의 독립 사전 대조 (권장):** run 프로세스를 띄우기 전에 stdlib 코드 (실행 모듈 밖) 로 `SOURCES.json` sha256 = 승인 고정값 · 다섯 모듈 바이트 = 목록을
  다시 대조한다. 어긋나면 띄우지 않고 meta 에 남긴다. E1 단계 판정 = 이 사전 대조 AND run 최종 판정 AND rc 0 · timeout 없음.
- E1 승인문에 채택할 것: fetch 의 실제 argv / env (이름 있는 origin · `GIT_ALLOW_PROTOCOL=https` · `GIT_TERMINAL_PROMPT=0` · 검토 회신 Q2) · `SOURCES.json` sha256.
- 선택 개선 (검토 회신 · 필수 아님): fetch 의 `TimeoutExpired` 때 부분 argv / 단계 기록 구조화 — 이번 범위 밖.

## 8. 밝힐 것

1. 목록 없는 라이브러리 경로 (legacy) 를 남긴다 — 기존 시험을 고치지 않기 위해서다. E1 CLI 는 목록 없이는 거부한다 (n1_e). 기록에는 legacy 로 남는다.
2. 끝 표의 기대 대조를 `required` 와 관계없이 더한다 — 예전보다 조금 엄격하다. 기존 시험의 판정은 바뀌지 않는다 (정적 확인 — 기존 시험의 표는 기대가 없거나 시작 = 끝).
3. 기록 형식이 조금 늘어난다: 사전 판정의 `required_identity` · prepare 반환의 `required` · 머리말의 `sources`.
4. 목록은 정정 구현 커밋 뒤에 만든다 — 다섯 모듈이 다시 바뀌면 목록과 승인을 다시 해야 한다.
5. 이 정정은 E0 의 PASS · 기록을 소급 변경하지 않는다 (E0 증거 · E0 시험 파일 그대로).
6. GREEN 에서 기존 0a · 0b 시험을 뺀다 (§6) — 그 시험이 보는 코드는 바뀌지 않는다 (패치 대상이 `reil_c4e_run.py` 하나).

## 9. 하지 않는 것

E1 fetch / run · 자료 반입 · 개봉 · 맞춤 · C4-A / B · 설치 · 환경 재구축 · COMSOL · 감시 · e3a · c5 · p0 변경 · 기존 시험 · 증거 수정 · plan-e 재실행.

## 10. 정하실 것

1. **이 정정 범위 그대로 승인** (변경 = §3 · 대조 = §4 의 6 · 순서 · 배정 = §5 · GREEN 계산 = §6) — 권장. 또는 실행 전에 Codex 사전 검토를 먼저 받을 수도 있다
   (이전 한정 보완들은 사용자 승인 → 실행 → 결과 검토 순서였다).
2. **GREEN 에 기존 0a · 0b 159 를 넣지 않음 (권장 · §6)** / 넣음 (E0 §6-2 의 실제 pymoo · COBYQA · Sobol 예외가 다시 필요).
3. **E1 단계 실행기의 독립 사전 대조를 E1 승인 요청에 넣음 (권장 · §7)** / 넣지 않음.
