# Codex 발송 프롬프트 — REIL C4-E · E1 승인 요청 v3 (E1-0 한정) 사전 검토 · 2026-10-21 KST

> v2 사전 검토 회신 (상태 문서 §76 — 정정 필요 V2-01–05 · 미래 E1-2 한정 FUTURE-01) 과 사용자의 정정 범위 v3 채택 (§77) 에 따라 쓴 비활성 초안과 수정
> 승인 요청이다. 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부할 것은 없다 (검토자가 저장소에서 읽는다).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

REIL C4-E · E1 승인 요청 v3 를 사용자 승인 전에 사전 검토해 주세요. 지난 회신 (§76) 의 V2-01–05 와 자체 발견 S2–S4 를 반영한 **비활성 초안 다섯과 수정
승인 요청**입니다. 승인 대상은 여전히 **E1-0 뿐**이고, FUTURE-01 은 회신대로 E1-0 범위를 넓히지 않고 E1-1–3 요청의 선행 조건 (그 승인의 첫 단계 E1-0b) 으로
적었습니다. 초안 작성은 사용자의 범위 v3 채택 (§77) 뒤에 했고, 정적 검사 (AST 파싱 · 이름 검사 · 골격 상수 · 서명 일치 · 대조가 쓰는 이름 · 봉인 표와 실제
바이트 · 비밀 검사) 만 했습니다. launcher · 실행기 · 시험 · driver · 탐침 · 읽기 경로 · fetch · run 은 모두 0 회입니다. 브랜치
`claude/14-gate-code-review-9qkx05` 의 최신 HEAD (이 발송문이 든 커밋) 를 기준으로 보시면 됩니다.

## 1. 볼 것

| 파일 (bms-balancing 기준) | sha256 | 무엇 |
|---|---|---|
| `docs/REIL_C4E_E1_APPROVAL_REQUEST_v3_20261021.md` | (이 커밋의 바이트) | 수정 승인 요청 — E1-0 한정 · 정정 대응표 · 정확한 명령 셋 · RED-L / RED-R / GREEN 기준 · 원천 해시 · 활동 범위 · E1-1–3 계획 (FUTURE-01 선행) · 밝힐 것 17 |
| `docs/REIL_C4E1_LAUNCHER_DRAFT_v3_20261021.py.txt` | `124a154dfbd662aaa49fcf21327bf48a08e190da5bd9d02ae28cf86072b71503` | launcher v3 (stdlib · 실행 모듈 import 0) |
| `docs/REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v3_20261021.py.txt` | `b77c6aa87cb7468063c258665a6b85765eab9f04e2607eb856444362b7374030` | RED 골격 (import · 상수 동일 · 함수 34 = NotImplementedError) |
| `docs/REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v3_20261021.py.txt` | `f00ba0fb9e333fe77cae275507203e8ced086d6e80d6c08a7aec5d98860ce002` | launcher 대조 26 |
| `docs/REIL_C4E1_RUNNER_CONTROLS_DRAFT_20261021.py.txt` | `555263464f2eddad1df1b1f9d201c947e990d026bb29bc4c95a74256c2a0ddfc` | 외곽 실행기 대조 8 (새) |
| `docs/REIL_C4E1_STEP_RUNNER_DRAFT_v3_20261021.py.txt` | `7454a0de4e221945958e1a99ab4a3f44a5eb7808f2b8c5997f7a82d5f097fbf3` | E1-0 외곽 실행기 v3 (봉인 표 EXPECT 포함) |
| `docs/REIL_C4E_E1_REVISION_SCOPE_v3_20261021.md` · 상태 문서 §76 · §77 | — | 정정 범위 v3 · 회신 접수 · 사용자 채택 |

## 2. 지적 ↔ 정정 (요청서 §2 의 요지)

| ID | 정정 | 대조 |
|---|---|---|
| V2-01 | 실행기의 /proc 관측은 모두 `proc_table` 하나 · 반복마다 관측 1 회를 회수와 자손 판정에 같이 씀 · 관측 · 회수 · kill 오류를 단계 하나의 ledger 에 쌓고 하나라도 있으면 끝 상태 unknown (뒤의 정상 empty 가 지우지 않음 · `first_error`) | r1 (회신의 반례 그대로) · r2 · r8 |
| V2-02 | 실행기 `base_env` (launcher `child_env` 와 같은 규칙) 를 준비의 첫 동작으로 — 자기 Git 기록과 pytest env 의 바탕 · 실행기 `git` · launcher `git_out` 은 env 필수 (기본값 없음) · 대조 둘의 fixture git 은 launcher 와 독립인 `_git_env()` (모든 GIT_* · 비밀 형태 제거 + 설정 격리) | l25 · r4 · r6 |
| V2-03 | 정리 = 공통 절대 기한 15 s 하나 (timeout 7 + 3 + 5 · 정상 3 + 12) · 어떤 sleep · wait 도 남은 시간을 넘지 않음 (0.1 s 하한 없음) · `deadline_hit` · `child_s` / `cleanup_s` / `records_s` / `total_s` · 기록은 별도 배정 | r3 · r8 |
| V2-04 | launcher · 실행기 모두 준비를 기록 단계 `prepare` 안으로 · 의도된 거부는 만들기 전 SystemExit (`except Exception` 이 잡지 않음) · 끝 관측 실패도 오류 · meta 불가 → stderr JSON (첫 오류) · 반환 4 · 실행기 반환 0 / 1 / 3 / 4 | l26 · r7 · l12 |
| V2-05 | 실행기가 만든다 — 고정 목록 14 · 봉인 표 `EXPECT[단계]` · 자식 전 `<단계>.source_sha256.txt` (다르면 자식 0 · 반환 3) · 끝 기록 뒤 `_end.txt` (다르면 runner_ok false) · 수동 기록의 고정 명령도 적음 | r5 · r6 · r7 |
| S2 · S3 · S4 (자체) | launcher `wait_s` / `cleanup_s` · fixture git 설정 격리 (사용자 설정에 서명 키 이름이 있음 — 이름만 읽음) · 시작 Git 기록 실패면 자식 0 (회신 §5 의 언급) | l19 · l25 · l21 · r7 |

## 3. 새 대조 · 명령 · 예산 (회신의 요구대로 따로 제시)

- launcher 대조 26 (v2 24 + l25 · l26 · l12 · l14 · l19 · l21 수정) · 외곽 실행기 대조 8 (새 파일) · GREEN 61 = E0 21 + N1 6 + 26 + 8 — 이전 24 / 51 에 숨기지
  않았습니다.
- 단계 셋 (요청서 §4-1 · §4-2): `01_red_launcher` (골격 · 26 · 120 s) · `02_red_runner` (v2 실행기 바이트 · 8 · 120 s) · `03_green` (61 · `-x` · 600 s) — 각
  정리 ≤ 15 s (공통 기한) + 기록 (git 넷 × ≤ 60 s · 해시 둘) · E1-0 전체 ≤ 2 h. 실행기 대조가 시험할 파일은 argv 의 `/usr/bin/env REIL_C4E1_RUNNER_UNDER_TEST=…`.
- RED 기준: RED-L 26 실패 모두 NotImplementedError · RED-R 8 실패 = r1 AssertionError (v2 의 empty — V2-01 재현) + r2–r8 AttributeError (v3 인터페이스 없음).

## 4. 밝힐 것 (요청서 §8 의 요지)

1. RED-R 의 일곱은 인터페이스 수준이다 — 행동 재현은 r1 하나.
2. 외곽 실행기의 실제 timeout 경로는 r8 의 driver 인스턴스로 시험한다 (E1-0 단계 자신이 timeout 되지 않으면 그 인스턴스의 경로는 관측되지 않는다).
3. driver 는 자기 subreaper 가 되고, 남긴 자손은 외곽 실행기 밑으로 와서 끝 상태를 바꾼다 (fail-closed).
4. /proc 스캔은 비원자적이고 PID kill 은 생성 신원을 보장하지 않는다 — 연속 소유 증명이 아니다.
5. 기록용 git 은 저장소 · 사용자 · 시스템 설정을 읽는다 — 키 이름만 확인 (fsmonitor · hooksPath · includeIf 없음 · 환경 변수의 command-line 설정은 정제 env 에서
   빠짐). 설정 격리는 새 대조의 fixture 에만 (기존 E0 시험은 `-c commit.gpgsign=false` 를 직접 줌).
6. FUTURE-01 (조건부 · 템플릿 설정) 은 E1-1–3 요청에서 닫는다 — v3 고정본으로 E1-2 실행 가능하다고 적지 않았다.

## 5. 질문

- Q1. V2-01–05 각 정정이 지적을 닫는가 — 특히 r1 · r2 · r3 · r8 이 회신이 요구한 "오류 뒤 정상 관측 · 정리 기한" 의 정확 기대 결과로 충분한가.
- Q2. V2-02 의 제거 정책 (실행기 · launcher 기록 · fixture 의 첫 호출 전) 과 음성 대조 (l25 · r4 · r6) 가 충분한가.
- Q3. 새 대조 34 · RED 선언 (RED-L / RED-R) · GREEN 61 · 예산 · 원천 해시 (생성 주체 · 대상 · 시점 · 실패 기준) 가 충분한가. 빠진 음성 대조가 있는가.
- Q4. 회신 밖 S2–S4 를 받아들일 수 있는가 — 특히 S4 (시작 기록 실패 시 자식 0) 와 S3 (fixture 설정 격리).
- Q5. E1-0 한정 승인으로 넘어가도 되는가 (요청서 §4). FUTURE-01 을 E1-1–3 요청의 E1-0b 로 둔 처리 (§7) 가 회신과 맞는가.

## 6. 경계

이 발송은 실행 지시가 아닙니다. launcher · 실행기 · 시험 · driver · 탐침 · 읽기 경로 · fetch · 자료 개봉 · run · C4-A / B · COMSOL 은 모두 0 회이고, E1-0 은
이 사전 검토 뒤 사용자의 별도 승인이 있어야만 시작합니다. E1-0 승인은 E1-0b · E1-1–3 을 허용하지 않습니다.

---
