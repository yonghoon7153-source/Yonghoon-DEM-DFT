# REIL C4-E · E1 정정 범위안 v5 (사용자 채택 요청) — v4 ultra 사전 검토 V4-01 · V4-N1 · 자체 발견 S6 · 2026-10-27 KST

> **범위 채택을 요청하는 문서다 (초안 작성 · 실행 0).** v4 사전 검토 회신 (상태 문서 §80 · `reviews/review_reil_c4e_e1_v4_prereview_20261021/originals/`) 은
> `implementation_approval: false` 다 — 정정 구현도 승인하지 않았다. 이 범위를 채택하신 뒤에만 비활성 초안 v5 · 승인 요청 v5 · 발송문 v5 를 쓴다. 채택해도
> 시험 · Git fixture · driver · 탐침 · 읽기 경로 · fetch · run 은 시작하지 않는다.

## 0. 구조 — 바뀌지 않는다

- 흐름: 비활성 정정안 v5 → Codex 재검토 → **사용자의 E1-0 한정 승인** → E1-0 → 결과 검토 → E1-1–3 별도 요청 (FUTURE-01 · E1-0b 포함).
- 회신이 정적으로 수용한 것은 그대로 둔다:
  - V3-01 정리 기한 · V3-02 `entry_exists` · V3-03 /proc 바이트 읽기 · V3-04 A (수동 Git 기록 없음 · 절차 Git 이름 확인) · V3-N1 `errors` 항목 셋.
  - 수 21 + 6 + 27 + 11 = 65 · driver 8 · 봉인 · 단계 배정 · 예산.
  - Q5 — v2 인터페이스 RED 의 제한을 공개한 그대로 둔다. 새 v3 재현 단계는 요구되지 않았다.

## 1. 지적별 정정

### V4-01 (P2) l27 · r11 의 Git fixture 가 비 UTF-8 stdout 을 만들지 못한다

- **원인 (v4):** 두 fixture 는 ff fe 가 든 메시지를 기본 `git commit -F` 로 저장한다. Git 2.43.0 은 commit 단계의 `verify_utf8` 에서 잘못된 바이트를 Latin-1 로
  보고 UTF-8 (c3 bf c3 be = ÿþ) 로 바꿔 저장한다 (회신의 공식 소스 판단 · 이 저장소도 실행하지 않았다). 그래서 `log --format=%B` 출력이 유효한 UTF-8 이 되고,
  wrapper 의 U+FFFD 기대가 성립하지 않는다. v4 작성 때 log 쪽 재인코딩만 보고 commit 쪽 정규화를 놓쳤다 — 요청서 v4 §8 의 6 의 전제가 틀렸다.
- **정정 (권장 A — Git 객체 바이트를 그대로 내보내는 경로):**

  | 부분 | v5 |
  |---|---|
  | 입력 생산자 | 정해진 바이트 `b"fixture \xff\xfe not utf-8\n"` 를 tmp 파일에 쓰고 `git hash-object -w --no-filters <파일>` 로 blob 을 만든다. blob 내용에는 커밋 메시지 같은 인코딩 정규화가 없고, `--no-filters` 가 정리 필터도 끈다 |
  | wrapper 호출 | launcher `git_run(["-C", repo, "cat-file", "blob", sha])` · 실행기 `git(["cat-file", "blob", sha], cwd=repo)`. `cat-file blob` 은 객체 내용을 바이트 그대로 내보낸다 |
  | fixture 자기 확인 (wrapper 를 거치지 않음) | 같은 명령의 stdout 을 바이트로 받아 확인한다: (1) 정확히 그 바이트다 · (2) 엄격 UTF-8 디코딩이 `UnicodeDecodeError` 다. 입력 생산자가 실제로 잘못된 UTF-8 을 내는지를 시험 안에서 먼저 확인한다 — V4-01 같은 fixture 결함이 다시 숨지 않게 |
  | wrapper 기대 | `out == 그 바이트.decode("utf-8", "replace")` (U+FFFD 둘 포함 · 정확한 문자열) · rc 0 · `error` 없음. U+FFFD 검사는 유지하고 더 좁힌다 |
  | 근거의 성격 | `cat-file` · `hash-object --no-filters` 의 의미는 Git 의 공개 의미에 기댄 설계 판단이다 (이번에 실행 0). 맞는지는 E1-0 GREEN 에서 위 자기 확인이 먼저 본다 — 틀리면 그 자리에서 AssertionError 로 멈춘다 |

- **대안 B (설명만 · 권장하지 않음):** 커밋 메시지 경로를 유지하고 저장 인코딩 (`-c i18n.commitEncoding=ISO-8859-1`) 과 출력 인코딩 (`log --encoding=ISO-8859-1`)
  을 함께 고정한다. Git 의 인코딩 변환 두 단계와 iconv 에 기대므로, A 보다 가정이 많다.
- **지우지 않는 것:** U+FFFD 검사 (회신 — 삭제하거나 ÿþ 기대로 바꾸면 S5 대조가 사라진다).
- **대조:** l27 · r11 의 Git 부분만 바뀐다. /proc 부분 · 사례 수 · 함수 이름은 그대로다. RED 종류도 그대로다 — l27 은 첫 `L.proc_members` 에서
  NotImplementedError, r11 은 첫 줄 `R.observe` 에서 AttributeError 이고, Git 부분은 RED 에서 실행되지 않는다.

### S6 (자체 · V4-01 의 "Python 디코딩 환경") wrapper 의 디코딩이 locale 에 기댄다

- **원인:** launcher `git_run` (v4 l.384) 과 실행기 `git` (v4 l.144) 은 `subprocess.run(…, text=True, errors="replace")` 만 쓰고 `encoding` 을 정하지 않는다.
  그래서 디코더가 실행 환경의 locale 인코딩이다. UTF-8 이 아닌 locale 이면 ff fe 가 U+FFFD 없이 다른 문자로 읽힌다. 회신이 말한 "의도한 UTF-8 디코딩" 이
  코드에 고정돼 있지 않다.
- **정정 (권장 — 포함):**
  - 두 wrapper 에 `encoding="utf-8"` 을 명시한다 (`errors="replace"` 는 그대로). git 출력의 해석이 locale 에 기대지 않게 된다 — HEAD · porcelain · config 목록도
    같은 디코더로 읽는다.
  - l27 · r11 은 Git 부분에서 wrapper 의 `subprocess.run` 호출 키워드 (`text=True` · `encoding="utf-8"` · `errors="replace"`) 를 AST 로 확인한다. 위 정확한 문자열
    기대와 함께 decoder 경로를 고정한다.
- **제외안:** locale 에 맡기고, E1-0 환경의 locale 을 요청서에 기록만 한다. 비 UTF-8 locale 에서는 l27 · r11 의 정확한 문자열 기대가 깨져 멈춘다
  (fail-closed). 그러나 E1-1–3 의 기록 해석이 환경에 따라 달라진다.

### V4-N1 (P3) 요청서 v4 l.274–275 의 문구

- "E1-0 은 launcher 를 대조 안에서만 부르므로 실제 정리 경로가 아니며" → "E1-1–3 실자료 운영 실행은 아니지만, E1-0 대조 (l11 · l19) 는 실제 가짜 자식
  프로세스의 정리를 일부 수행한다" 로 좁힌다. launcher 운영 정리 정책은 여전히 E1-1–3 요청의 몫이다 (회신 — 이번 범위로 끌어오지 않는다).

### 회신의 주의를 요청서 v5 에 반영 (문서만)

다음을 요청서 v5 의 밝힐 것에 더한다.

- V3-02 의 lstat 거부는 검사 뒤 경쟁 변경까지 막는 원자적 보호가 아니다.
- V3-04 A 는 `GIT_CONFIG_KEY / VALUE` 의 내용과 모든 설정 원천을 격리하지 않는다.
- 소비자는 최상위 `first_error=null` 만 보고 정리 오류가 없다고 판단하지 않는다 — `cleanup.status` · `cleanup.errors` 를 본다.
- 정리 기한 대조는 가짜 시계로 한 것이지, 실제 /proc 지연 상한의 관측이 아니다.

## 2. 다시 봉인할 것 · 총수 · RED 선언 (계획 — 초안에서 확정)

| 초안 | v5 에서 바뀌는 것 |
|---|---|
| launcher v5 | `git_run` 의 `encoding="utf-8"` (S6) · `REQUEST` = 승인 요청 v5 · docstring |
| RED 골격 v5 | `REQUEST` 상수 · docstring (`make_skeleton` 정적 변환 — 함수 35 · 서명 · import / 상수 동일) |
| launcher 대조 v5 | l27 의 Git 부분 (V4-01 · S6) · l14 의 승인 문구 경로 v5 |
| 외곽 실행기 대조 v3 | r11 의 Git 부분 (V4-01 · S6) |
| 외곽 실행기 v5 | `git` 의 `encoding="utf-8"` (S6) · 봉인 표 `EXPECT` 다시 채움 (위 넷의 sha · bytes) |
| 승인 요청 v5 · 발송문 v5 | §1-1 sha 표 · §4-4 EXPECT · §6 의 l27 · r11 행 (입력 · 기대 · 이유 · 호출 경로) · §8 의 6 (blob 경로로 고침) · §8 의 18 (V4-N1) · 회신의 주의 넷 |

- **총수 (바뀌지 않음):** launcher 대조 27 · 외곽 실행기 대조 11 · GREEN 65 (E0 21 + N1 6 + 27 + 11 · 건너뜀 0) · driver 8.
- **RED 선언 (바뀌지 않음):**
  - RED-L: 골격에서 27 실패 · 모두 NotImplementedError.
  - RED-R: v2 실행기에서 11 실패 — r1 AssertionError · r2 · r3 · r9 · r10 `cleanup` · r4 `base_env` · r5 `source_table` · r6–r8 `run_step` · r11 `observe`
    (모두 AttributeError).
- **예산 (바뀌지 않음):** RED-L 120 s · RED-R 120 s · GREEN 600 s · 정리 ≤ 15 s (공통 기한) + 기록 · E1-0 ≤ 2 h.
- **새로 정적 검사로 볼 것:** 정정 두 대조의 Git 부분이 commit · log 를 부르지 않는다 · `hash-object` 에 `--no-filters` 가 있다 · 두 wrapper 의 `encoding="utf-8"`
  (AST) · v4 대비 diff 가 위 표의 자리에만 있다.

## 3. 바뀌지 않는 것

다섯 모듈 · SOURCES.json · S1 의 두 파일 · 기존 시험 · 기존 증거 · 봉인 · TARGETS 14 · v2 실행기 초안 (RED-R 대상) · 정리 규칙 (V3-01) · `entry_exists` · /proc
바이트 읽기 · 절차 Git 규칙 (V3-04 A) · Git 금지 키 · fetch 사후 대조 · FUTURE-01 경계. v1–v4 문서와 초안은 지우지 않는다.

## 4. 정하실 것

1. **이 범위 채택** — 채택하시면 위 초안 · 요청서 v5 · 발송문 v5 까지 쓰고 멈춘다 (권장). 정적 검사만 하고, Git fixture 를 포함한 실행은 0 이다.
2. **V4-01 의 입력 생산자** — **A: blob (`hash-object -w --no-filters` + `cat-file blob`) + fixture 자기 확인 (권장)** / B: 커밋 메시지의 저장 · 출력 인코딩 고정.
3. **S6 디코딩 고정** — **포함: 두 wrapper 에 `encoding="utf-8"` + AST 확인 (권장)** / 제외: locale 에 맡기고 기록만.
