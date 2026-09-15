# 63차 게이트 리뷰 작업 상태 (정본)

판정: **NO-GO** (2026-09-15 접수 · 리뷰어 제목은 "62차 묶음 5 — 방어적 코드·회귀
검토" 이나 우리 원장 번호로는 **63차**다 — `GATE62_REQUEST.md` 에 대한 답).
검토 head `22e240e31191a5d0311f6a836a8d0ec7d1a3cfdf` · 판정 대상 RUN_SCOPE
`0dcbc17aa73ef1fc8ac681e2b0617da68a86ceb4` · `source_digest fd7c90edbc56ff1f`
(리뷰어 실측 일치). 새 **P1 3 · P2 1 = 4건** + 증거 공백 **E1 · E2**.

리뷰어가 스스로 좁힌 범위: 선택 회귀 42건(41/1) · 계약 시험 7건(2/5) · 정적
검토. 전체 pytest · strict smoke · 변이 전수 재생은 **미실행**. 새 P0 는 입증
안 됨. 접수 원장은 `docs/08_REVIEW_RESPONSE.md` §77.

## 발견 원장

| ID | 무엇이 틀렸나 | 자리 (판정 시점) | 묶음 | 상태 |
|---|---|---|---|---|
| F1 (P1) | `bundle` 의 두 lock: 둘째 acquire 실패 → 첫 lock 미해제 · 첫 release 예외 → 둘째 미해제 | `tools/archive_bundle.py:545,550` | θ | 코드 ✔ |
| F2 (P1) | `-X importtime` 의 이름 목록을 "성공한 import" 로 취급 → `site` 의 실패한 선택적 import(`apport_python_hook`)를 "올렸다 지운 module" 로 오분류 → 기본 Ubuntu 가 `failed` | `mutation_replay.py:5100,5140` (`_ENV_PROBE_BODY` 안 `_measure_history`) | ι | 코드 ✔ |
| F3 (P1) | 부모의 customization 탐색이 `이름.py` 만 보고 package `이름/__init__.py` 를 안 본다 → Python resolver 와 다른 digest → 정상 환경 거부 | `mutation_replay.py:5392,5407` (`_parent_customization_view`) | ι | 코드 ✔ |
| F4 (P2) | `_HEX16` 을 `re.match` + `$` 로 검사 → 후행 LF 17자 통과 | `mutation_replay.py:5555,5610` (`_schema_mismatch`) | ι | 코드 ✔ |
| E1 | 3.12 `type_params` 의 bound/default 를 `_definition_head` 가 열거하지 않는다 (identity 변화는 미입증 — 공백) | `row_projection.py:1539,1565` | κ | 코드 ✔ |
| E2 | lock-lifetime 시험이 경로 exists 만 보고, smoke namespace 라 claim=None → 실제 planned phase 기록 + 커널 배타를 관측한 적 없다 (공백) | `tests/test_lock_lifetime_62.py:87` · `tests/conftest.py:134` | κ | 코드 ✔ |

상태 열: RED = 재현 시험이 실패하는 것을 봤다 · 코드 ✔ = 고치고 GREEN ·
fixture ✔ = fixture 감사까지. RED 관측: `tests/test_gate63_defensive.py` 첫 실행
**10 failed · 12 passed** (F1×3 · F3 · F4 · F2×2 · E1×2 · E2). GREEN: 21 passed ·
1 xfailed(⑦) · E2 는 dirty 면 skip (clean 커밋에서 실측 — 마감 절).

## 묶음과 순서

| 순서 | 묶음 | 축 | 발견 |
|---|---|---|---|
| 1 | θ | 자원 정리 — 취득 즉시 등록 · 부분 취득/정리 예외에서도 전부 해제 · 원래 오류 보존 | F1 |
| 2 | ι | 증거 영수증 — 시도/성공/확인불가 3분 증거 모델 · 부모 탐색을 `PathFinder` 로 · scalar `fullmatch` | F2 · F3 · F4 |
| 3 | κ | 증거 공백 — type_params head · 실제 planned lifecycle 에서 phase 기록 중 커널 잠금 관측 | E1 · E2 |

ι 의 F2 설계: 손자를 `-X importtime -v` 로 띄운다. `importtime` 은 **시도**
전부를(실패한 것도) 찍고, `-v` 의 `import 'X' # <loader>` 줄은 **성공한 로드만**
찍는다 (이 컨테이너 실측: `try: import nope_optional_63 / except ImportError:
pass` 를 둔 sitecustomize 에서 importtime 줄은 있고 `-v` 줄은 없다). 그래서
이름마다 셋 중 하나다 — 성공 로드(지금 찾아 해시; 못 찾으면 **failed** = 올렸다
지움) · 시도만(`attempted_not_loaded` 에 이름을 남기고 measured 유지) · 둘의
불일치(`-v` 는 로드인데 customization 은 `<absent>`) → failed. 이름 하나를
예외 목록에 넣는 수정이 아니다.

## 재현 시험

리뷰어 `test_gate62_defensive_contracts.py` 7건을 이 저장소 경로로 옮겨
`tests/test_gate63_defensive.py` 에 그대로 고정했다 (+ F2 의 정상 사례 3건,
E1 의 3.11 합성 AST 판, E2 의 실제 planned lifecycle 관측 + 탐침 대조군).

## 문서 정정 (리뷰어 지적, P2 아님)

요청문 머리의 "신고 5건" ≠ 본문 ①–⑦. 63차 요청문은 **7건** 으로 적는다.

## 남는 것 (리뷰어 재심 조건 6)

§0 의 독립 GO 전제(producer 결속 · trusted launcher · typed 보존 영수증 소비 ·
독립 replay)는 이번 묶음이 닫지 않는다 — 요청문 §0 에 그대로 신고한다.

## 고치며 드러난 것

- **분석기가 자기 규칙에 걸렸다.** E1 첫 수정판의 `getattr(tp, attr, None)` 는
  이름을 계산해서 건네는 식이라 producer 닫힘 분석이 `row_projection.py` 자신을
  fail-closed 로 거부했다 (`test_scope_model_62` 6건 빨강). 리터럴 이름 둘로 풀었다.
- **62차 축 둘이 죽었다.** F1 refactor 로 `promotion-checks-derived-freshness-g62` ·
  `promotion-holds-the-run-locks-g62` 의 preimage 가 0회 — `--check-preimages` 가
  잡았고 새 자리로 재조준했다.
- **§0 ⑦ 이 실측으로 재현됐다.** 저장소 밖 입력의 staging 이 `SameFileError` 로
  죽는다. 고치지 않고 strict xfail 로 고정 (`…_outside_the_repo_is_still_unsupported`).
- **E2 는 clean 커밋에서만 돈다.** 진짜 producer 가 git 상태를 적고 fit 검증
  (F74/F85)이 dirty 곡선을 거부한다 — smoke 와 같은 규칙. skip 사유를 출력에 남긴다.

## 변이 등록부 (63차)

새 축 8 (`-g63`): archive 2 (F1) · startup-history 2 + schema 1 (F2) ·
path-finder 1 (F3) · fullmatch 1 (F4) · type-params 1 (E1). 재조준 2 (g62 archive).
MR 자기 참조 preimage 5 건은 `\uXXXX` escape. `--check-preimages` rc 0
("모든 변이 지점이 정확히 한 번 나타난다").
