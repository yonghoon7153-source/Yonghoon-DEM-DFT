# Codex 발송 프롬프트 — REIL C4-E · E1 승인 요청 v5 (E1-0 한정) 사전 검토 · 2026-10-27 KST

> v4 ultra 사전 검토 회신 (상태 문서 §80 — 정정 필요 V4-01 · 문구 V4-N1 · 주의 다섯) 과 사용자의 정정 범위 v5 채택 (§81 · V4-01 = A · S6 포함) 에 따라
> 쓴 비활성 초안과 수정 승인 요청이다. 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부할 것은 없다 (검토자가 저장소에서 읽는다).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

REIL C4-E · E1 승인 요청 v5 를 사용자 승인 전에 사전 검토해 주세요. 지난 회신 (§80) 의 V4-01 · V4-N1 · 주의 다섯과 자체 발견 S6 을 반영한 **비활성 초안
다섯과 수정 승인 요청**입니다. 승인 대상은 여전히 **E1-0 뿐**이고, FUTURE-01 은 E1-1–3 요청의 선행 조건 (E1-0b) 으로 그대로 두었습니다.

- 초안은 사용자가 범위 v5 를 채택한 (§81) 뒤에 썼습니다.
- 한 것은 정적 검사뿐입니다: AST 파싱 · 이름 검사 · ruff pyflakes 규칙 · 골격 상수 · 서명 일치 · wrapper 호출 키워드 (AST) · 대조가 쓰는 이름 · 봉인 표와
  실제 바이트 · 비밀 검사.
- launcher · 실행기 · 시험 · Git fixture · driver · 탐침 · 읽기 경로 · fetch · run 은 모두 0 회입니다. V4-01 정정이 쓰는 Git 명령 (`hash-object` ·
  `cat-file`) 도 이 저장소에서 실행하지 않았습니다.
- 브랜치 `claude/14-gate-code-review-9qkx05` 의 최신 HEAD (이 발송문이 든 커밋) 를 기준으로 보시면 됩니다. v4 와 비교하실 때는 지난 검토의 고정 커밋
  `3d3ee8c1` 를 쓰시면 됩니다.

## 1. 볼 것

| 파일 (bms-balancing 기준) | sha256 | 무엇 |
|---|---|---|
| `docs/REIL_C4E_E1_APPROVAL_REQUEST_v5_20261027.md` | `18db9f15cff07a0336d52bbc014f23759f82dc7fe24d0408870b3c0f746d5d69` | 수정 승인 요청 — 정정 대응표 (§2) · 정적 검사 (§1-1 — v4 와 같은 것 · v5 에서 더한 것) · 명령 · RED / GREEN 기준 (v4 와 같음) · l27 · r11 의 입력 / 기대 / 이유 / 호출 경로 (§6) · 밝힐 것 26 (§8) |
| `docs/REIL_C4E1_LAUNCHER_DRAFT_v5_20261027.py.txt` | `2269d775f1701e2f657d386f42bc950d26a6b56bd37323611dd6ab4cc1a75396` | launcher v5 (stdlib · 실행 모듈 import 0) |
| `docs/REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v5_20261027.py.txt` | `e6f72de2245a41a4a80e0bb7adcc7734991f0b95fb1c1764ea6bfda579849182` | RED 골격 (import · 상수 동일 · 함수 35 = NotImplementedError) |
| `docs/REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v5_20261027.py.txt` | `4720585c86f555bb0f9cfea3e12aab5b283f8ee4243a3ef257f77849759b777d` | launcher 대조 27 |
| `docs/REIL_C4E1_RUNNER_CONTROLS_DRAFT_v3_20261027.py.txt` | `ae42d8e8c0fb0c680d324348d2e1edc8f11865bd6bedea7cb0becf9b00fe6042` | 외곽 실행기 대조 11 |
| `docs/REIL_C4E1_STEP_RUNNER_DRAFT_v5_20261027.py.txt` | `f6070f9776baa7dfc9b5e26ac5e6f378dd2969e7628566e5baa3c02685814a2a` | E1-0 외곽 실행기 v5 (봉인 표 EXPECT 포함) |
| `docs/REIL_C4E_E1_REVISION_SCOPE_v5_20261027.md` · 상태 문서 §80 · §81 | — | 정정 범위 v5 · 회신 접수 · 사용자 채택 |

v4 대비 diff 는 다음 자리에만 있습니다: 머리말 · `REQUEST` · git wrapper 둘 · l14 문구 · l27 / r11 의 Git 부분 · 봉인 표 (요청서 §1-1).

## 2. 지적 ↔ 정정 (요청서 §2 · §6 · §8 의 요지)

| ID | 정정 | 대조 · 자리 |
|---|---|---|
| V4-01 | 커밋 메시지를 쓰지 않습니다. 정해진 바이트 `b"fixture \xff\xfe not utf-8\n"` 를 tmp 파일에 쓰고 `git -C <repo> hash-object -w --no-filters <파일>` 로 blob 을 만든 뒤, wrapper 가 `cat-file blob <sha>` 를 부릅니다. **fixture 자기 확인:** wrapper 를 거치지 않은 같은 명령의 stdout 바이트가 정확히 그 바이트이고, 엄격 UTF-8 디코딩이 `UnicodeDecodeError` 인지 먼저 봅니다. **기대:** `out == 그 바이트.decode("utf-8", "replace")` (U+FFFD 둘 · 정확한 문자열) · rc 0 · `error` 없음. U+FFFD 검사는 남겼습니다 | l27 (launcher 대조 v5 l.787–799) · r11 (실행기 대조 v3 l.562–574) |
| S6 (자체 · 회신의 "Python 디코딩 환경") | launcher `git_run` · 실행기 `git` 의 `subprocess.run` 에 `encoding="utf-8"` 을 명시했습니다 (`text=True` · `errors="replace"` 는 그대로). git 출력 (HEAD · porcelain · config 목록 포함) 의 해석이 실행 환경 locale 에 기대지 않습니다 | launcher v5 l.385 · 실행기 v5 l.146. l27 · r11 이 시험할 파일의 AST 에서 그 함수의 `subprocess.run` 호출 하나의 상수 키워드 (`text` · `encoding` · `errors`) 를 확인합니다 (도우미 `_run_keywords` — launcher 대조 l.111 · 실행기 대조 l.152) |
| V4-N1 | "실제 정리 경로가 아니며" → "E1-1–3 실자료 운영 실행은 아니지만, E1-0 대조 (l11 · l19) 는 실제 가짜 자식 프로세스의 정리를 일부 수행한다" | 요청서 §8 의 18 |
| 주의 다섯 (§80) | 밝힐 것으로 옮겼습니다: lstat 거부는 원자적 보호가 아님 (§8 의 22) · `GIT_CONFIG_KEY / VALUE` 내용과 설정 원천은 격리 밖 (19) · 최상위 `first_error=null` 만 보지 말 것 (20) · 기한 대조는 가짜 시계 (2) · v4 는 GREEN l27 에서 멈췄을 것이나 관측으로 기록하지 않음 (24) | 문서 |

## 3. 바뀌지 않은 것

- 수: launcher 대조 27 · 외곽 실행기 대조 11 · GREEN 65 = E0 21 + N1 6 + 27 + 11 (건너뜀 0) · driver 8 회 (r6 1 · r7 6 · r8 1). 새 대조는 없고, 고친
  대조는 l14 (승인 문구의 요청서 경로) · l27 · r11 (Git 부분 — /proc 부분은 그대로) 셋입니다.
- 단계 셋 · 명령 · 예산: `01_red_launcher` (골격 · 27 · 120 s) · `02_red_runner` (v2 실행기 바이트 · 11 · 120 s) · `03_green` (65 · `-x` · 600 s) — 각 정리
  ≤ 15 s (공통 기한) + 기록 · E1-0 전체 ≤ 2 h.
- RED 기준: RED-L 27 실패 모두 NotImplementedError · RED-R 11 실패 = r1 AssertionError + r2 · r3 · r9 · r10 (`cleanup`) · r4 (`base_env`) · r5
  (`source_table`) · r6–r8 (`run_step`) · r11 (`observe`) AttributeError. Git 부분은 RED 에서 실행되지 않습니다 — l27 은 첫 `L.proc_members` 에서,
  r11 은 첫 줄 `R.observe` 에서 멈춥니다.
- V3-01–04 · V3-N1 · S5 의 정정 (§80 의 정적 수용 범위) · 절차 Git 규칙 · 봉인 대상 열넷 · FUTURE-01 경계.

## 4. 밝힐 것 (요청서 §8 의 요지 — v5 에서 새로 쓰거나 고친 것)

1. v4 요청서 §8 의 6 은 "커밋 메시지가 바이트 그대로 출력된다" 는 틀린 전제를 적었습니다 (§8 의 6 · §80). v4 작성 때 log 쪽 재인코딩만 보고 commit 쪽
   정규화를 보지 못했습니다.
2. blob (`hash-object -w --no-filters`) 과 `cat-file blob` 이 내용을 바이트 그대로 다룬다는 것은 Git 의 공개 의미에 기댄 설계 판단입니다 (실행 0). 판단이
   틀리면 GREEN 에서 wrapper 보다 먼저 fixture 자기 확인이 AssertionError 로 멈춥니다 (§8 의 6).
3. S6 은 시험 대상 wrapper 둘에만 적용했습니다. 두 대조 파일의 fixture 도우미 `_git` 은 `encoding` 없이 `text=True` 만 둡니다 (v4 와 같음). 그 출력을
   쓰는 곳은 `rev-parse HEAD` · `hash-object` 의 객체 이름 (16 진수) 뿐이고, 비 UTF-8 바이트를 다루는 자기 확인은 바이트로 받습니다 (§8 의 26).
4. v4 를 실행하지 않았으므로 "l27 실패를 관측했다" 나 "나머지는 통과했다" 로 적지 않았습니다 (§8 의 24).
5. 대조 l14 의 `§80` 은 `build_argv` 의 형식 예시이고, 상태 문서 §80 의 내용과 관계없습니다 (§8 의 25).

## 5. 질문

- Q1. V4-01 정정 (blob 입력 · fixture 자기 확인 · 정확한 대체 문자열 기대) 이 지적을 닫습니까? 특히 `hash-object -w --no-filters` + `cat-file blob` 이 Git
  2.43.0 에서 바이트를 그대로 내보낸다는 설계 판단과, 그 판단이 틀릴 때 자기 확인이 먼저 멈추는 구조가 충분한지 봐 주세요.
- Q2. S6 (두 wrapper 의 `encoding="utf-8"` + AST 확인) 이 회신이 말한 "Python 디코딩 환경" 을 닫습니까? HEAD · porcelain · config 목록 해석에 부작용이
  없는지, AST 확인의 모양 (그 함수 안의 `subprocess.run` 호출 하나 · 상수 키워드) 이 충분한지, fixture 도우미 `_git` 을 그대로 둔 처리 (밝힐 것 3) 를 받아들일
  수 있는지 봐 주세요.
- Q3. V4-N1 문구 (§8 의 18) 와 주의 다섯의 반영 (§8 의 2 · 19 · 20 · 22 · 24) 이 회신의 뜻과 맞습니까?
- Q4. 다시 봉인한 초안 다섯 · 봉인 표 · RED 선언 (변화 없음) · GREEN 65 · 예산으로 E1-0 한정 승인에 넘어가도 됩니까?

## 6. 경계

이 발송은 실행 지시가 아닙니다. launcher · 실행기 · 시험 · Git fixture · driver · 탐침 · 읽기 경로 · fetch · 자료 개봉 · run · C4-A / B · COMSOL 은 모두
0 회입니다. E1-0 은 이 사전 검토 뒤 사용자의 별도 승인이 있어야만 시작합니다. E1-0 승인은 E1-0b · E1-1–3 을 허용하지 않습니다.

---
