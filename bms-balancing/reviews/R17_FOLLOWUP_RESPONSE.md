# R17 후속 회신 — Codex 후속 재검토 (대상 `7c8f61f9`) NO-GO · P1 3 · P2 2 — 다섯 건 전부 코드에서 닫음

> 기계용 회신. 리뷰 원본은 `reviews/r17_followup/codex/` (패키지 zip sha256
> `7b574770aeea901618425759ac3aeada984812b989e8c69a2622f494b0457cc7`, 273,873 B, 53 파일).
> **리뷰어 식별을 우리 쪽에서 확인했다**: `REVIEW_IDENTITY.json` 의
> `reviews/R17_RESPONSE.md` sha256 `9b86873680ea6095773f0836485ce5c139f48a2af621825ed25668f447bae32f`
> = `git show 7c8f61f9:bms-balancing/reviews/R17_RESPONSE.md | sha256sum` 의 값. 대상 tree
> `1da2e9f5600dc5f91dd0a989188ef7b0ecb19437` 도 같다 — **우리가 보낸 바로 그 커밋을 봤다.**

| 항목 | 값 |
|---|---|
| 리뷰 대상 | `7c8f61f943199c3782bf3c3d81f6b573aa0a1b79` |
| 이 회신의 코드 | 브랜치 head (커밋 SHA 는 push 후 확정 — 요청문 규칙 그대로) |
| 판정 수용 | **NO-GO — 그대로 받는다.** P1 3 · P2 2 전부 인정. 과학 값은 하나도 다시 계산하지 않았고 실데이터 A/B 도 돌리지 않았다 |
| 판정 경계 | 게이트 리뷰(65·66차) · COMSOL 트랙과 **섞지 않는다** — 리뷰어가 적은 대로 |
| 한 줄 요약 | **검사한 것과 사용한 것이 달랐다** (경로 · 선언 · witness · digest), 그리고 **부재를 닫았더니 `null` 로 옮겨 갔다** |

## 0. 먼저 — 리뷰어 재현기를 우리 Linux 에서 돌렸다

`reviews/r17_followup/codex/repro_followup.py` 를 **수정 없이** 실행했다 (대상은 우리 트리).

**수정 전** — 다섯 건이 전부 재현됐고 대조군도 정상이었다:

```
gc_cleanup_escape        rc 0   (partial 밖 victim 삭제됨)      ← 기대 rc 2
gc_duplicate             rc 0   (보존 항목의 payload unlink)     ← 기대 보존
width_body_version       rc 0   / body_mixed_version rc 0 / body_tol rc 0 / body_cell rc 0
width_body_run           rc 0   / width_fractional_cycles rc 0
width_null_identity      rc 0   / width_null_settings rc 0
receipt_null_runtime     rc 0   / bad_runtime 0 / bad_materialized 0 / bad_date 0 / non_digest 0
width_out_of_box_seed    observed / width_infeasible_best observed
── 대조군 ──
gc_control 0 · gc_old_cross_artifact 0 · width_positive 0
width_seed_negative 2 · width_meta_version_negative 2 · receipt_missing_runtime_negative 3
```

**수정 후** — 같은 스크립트가 **자기 첫 assert 에서 멈춘다**:

```
AssertionError: repro_followup.py:69
  assert pair('width_body_version', ...)[0].returncode == 0
```

그 assert 가 고정한 것이 "결함이 있다(rc 0)" 이므로, 실패가 곧 그 결함이 사라졌다는 뜻이다.
⚠ 스크립트는 **assert 식 안에서** 실제 실행을 하므로 `-O` 로 assert 만 걷으면 케이스 자체가 돌지
않는다(실측: `KeyError: 'gc_old_cross_artifact'`). 그래서 **뒤 케이스들의 rc 를 이 스크립트로는
한 번에 받지 못했다** — 스크립트를 고치지 않기 위해 거기서 멈췄다. 다섯 건의 독립 확인은 아래
우리 회귀가 맡는다.

## 1. 발견별 대응

| ID | 리뷰어 반례 | 고침 (`파일:함수`) | 이제 어디에 걸리나 | 회귀 |
|---|---|---|---|---|
| **P1-01 A** | `path` 는 partial 안, `kind=".."`·`attempt="victim"` → rc 0 으로 `out/victim/sentinel.txt` 삭제 | `gc_partial.py` — ① **모든 항목을 typed 로 먼저 읽고** `kind`/`attempt`/`artifact` 가 경로 성분인지 검증(`.`·`..`·구분자·절대경로 거부) ② **지울 대상 전체**(파일 + 시도 디렉터리)의 정규 경로를 **첫 삭제 전에** containment 검사 ③ 삭제 루프가 그 **검증된 경로**를 쓴다(다시 만들지 않는다) | 경로 성분 검증에서 rc 2, 바이트 불변 | `test_fu_01_gc_refuses_an_index_whose_attempt_escapes_partial` |
| **P1-01 B** | 같은 payload 를 가리키는 index 둘 → 보존 항목의 파일이 `unlink` | 같은 파일 — `retained_files` 를 만들어 삭제 대상과 **겹치면 rc 2** (fail-closed). `retained_dirs` 로 디렉터리 보호도 경로 기준으로 바꿨다 | 겹침 검출에서 rc 2 | `test_fu_02_gc_does_not_unlink_a_payload_a_retained_entry_still_references` |
| **P1-02** | 행만 v2 / 파일 안 혼합 / `width_tol` `.90` / `cell` / `run_id` 불일치 → rc 0. `cycle` 0.9 가 `int(float())` 로 0 | `width_report.py` — `BODY_META_BOUND` = (`objective_version`·`cell`·`width_tol`·`run_id`) 를 **행 ↔ sidecar** 로 결속하고, 한 파일 안에서 **하나**여야 한다. `cycles_key` 로 접기 **전에** 정수성 검사 | 각 축마다 rc 2 (숫자 표기 차이 `0.01`↔`"0.01"` 는 값으로 견준다) | `test_fu_06[...]` ×4 · `test_fu_07` · `test_fu_08` |
| **P1-03** | 양쪽 `git_commit/env/dataset_manifest=null` 또는 `seed/lb/ub/initial/objective_version=null` → rc 0 + "동일 확인" | `width_report.py:_typed_meta_problems()` — 필수 값의 **타입·형식**을 본다 (40/64-hex · 비지 않은 객체 · 정수 · 수 목록 · enum). `gamma_lb` 는 **넣지 않았다** | rc 2, "동일 확인" 출력 없음 | `test_fu_09[...]` ×2 · 대조군 `test_fu_10_width_keeps_a_legitimate_nullable_field` |
| **P2-01 A** | 상자 밖 seed(`a_PE=10`) 가 witness → `LAM_PE min −733 %p` (참 ±16.67) | `verify.py:near_optimal_extrema` — `_in_box()` 술어를 **모든 후보**(seed · 복원점)에 적용. 상자 밖은 시작점으로도 안 쓴다 | 하한이 참 범위 안 | `test_fu_11_a_seed_outside_the_box_can_not_become_a_witness` |
| **P2-01 B** | stale `best_val` → 제약 밖 `best` 가 `vals` 에 재삽입 → `min −16.67` (참 +8.33), `_width_fields` 는 `measured` | 같은 함수 — `obj(best)` 를 직접 재서 `limit` 밖이면 **RuntimeError** (기준값과 기준점이 어긋난 것은 호출자의 버그다) | RuntimeError → `_width_fields` 가 `failed` | `test_fu_12` · `test_fu_14` · 대조군 `test_fu_13` |
| **P2-02 타입** | `runtime=null`/문자열 · `materialized=17` · `produced_utc="not-a-date"` · `package.digest="not-a-digest"` 가 전부 `verified=true` | `verify_run_receipt.py:_typed_problems()` — 생산자(`evidence_gate.run_receipt`)가 실제로 내는 모양을 nested schema 로 고정. **`materialized=None` 은 합법으로 남겼다** (리뷰어 단서 그대로) — 막는 것은 뜻을 알 수 없는 타입이다 | `complete=false` → rc 3 | `test_fu_16[...]` ×5 · 대조군 `test_fu_15` |
| **P2-02 digest** | 실제 writer 가 `package_digest()` 의 **상태 dict** 를 `str()` 해서 digest 에 넣는다 → bytes 가 다른 두 패키지가 같은 `{'one.txt': 'ok'}` | `evidence_gate.package_content_digest()` 신설 (이름 정렬 + `sha256(bytes)  이름` 정규화 + 재해시, 없는 파일은 `<missing>`) · `replay_codex_r11.py` 가 receipt 에 **그것**을 싣고 상태는 `package_status` 로 따로 낸다 | bytes 가 다르면 digest 가 다르다 | `test_fu_18` · 상태의 성질을 고정하는 `test_fu_17` |

## 2. 시험 감사 — 리뷰어가 짚은 둘 (발견으로 세지 않았다고 했으나 고쳤다)

**`cr_04` 의 잡음이 버전마다 달랐다.** `fit()` 안에서 `make()` 를 불러 **버전 루프마다 RNG 를 다시
소비**했다 — legacy 와 v2 가 서로 다른 잡음 실현을 적합했다. 입력 배열을 먼저 만들어 두 버전이
공유하도록 고쳤다. 그 결과 **잡음 행의 숫자가 바뀌었고 정정한다**:

| truth | 판 | LAM_PE | **LAM_NE** | LLI |
|---|---|---:|---:|---:|
| A (1 mV 잡음) | `legacy_matlab` | +0.7983 | **−3.1224** | +0.7618 |
| A (1 mV 잡음) | `chain_rule_v2` (전) | −0.3525 | **+0.6819** | −0.0297 |
| A (1 mV 잡음) | `chain_rule_v2` (**공유 뒤**) | +0.0419 | **−0.0078** | −0.0009 |

무잡음 두 행은 RNG 를 안 쓰므로 영향이 없다. `FINDINGS.md` §1-2-b 와 `R17_RESPONSE.md` 의 갱신
블록에 정정을 적었다. **두 판의 오차 차이를 "1/a 한 축의 효과" 로 읽으려면 입력이 같아야 한다**는
리뷰어의 지적이 옳았고, 전 판의 잡음 행은 그 조건을 만족하지 않았으므로 축 효과의 근거로 인용하지
않는다. 잡음 조건이 하나뿐이고 평활·상자를 바꾼 전수 강건성 시험이 아니라는 지적도 그대로 받는다.

**`test_r17_11` 은 공집합 분기를 직접 시험하지 않는다.** `tol=-.5` 가 먼저 걸려 objective 호출이
0회라는 관측을 그대로 받는다. 리뷰어가 독립 확인한 "정상 tol 의 진짜 공집합 → RuntimeError" 는
우리 쪽 `test_fu_12` 가 같은 경로를 탄다(`obj(best)` 가 한계 밖 → RuntimeError). `test_r17_11` 의
이름은 그대로 두되 **공집합 회귀로 세지 않는다**.

## 3. fixture 가 먼저 깨졌다 (CLAUDE.md 규율 2)

validator 를 조이자 **기존 fixture 둘이 먼저 빨개졌다** — 이 저장소에서 다섯 번째로 실측된 패턴이고,
안 깨졌으면 그것이 위조 통로였다는 뜻이다.

| fixture | 무엇이 가려져 있었나 | 고침 |
|---|---|---|
| `test_r17_codex.py::_width_pair` | 행의 `run_id` 가 채움값 `"1"` 인데 sidecar 는 `"r0"` — production(`cycles.py:224`)은 **행에 진짜 run_id 를 쓴다**. 결속 검사를 넣자 정상 대조군이 먼저 깨졌다 | 행의 `run_id` 를 sidecar 선언과 맞췄다 (의도 유지) |
| `test_r16_run_receipt.py::_receipt` | `instrument` 값이 `"0"*64` — 실제 `gate.instrument_digests()` 는 **40자리 git blob** 을 낸다. 이 시험이 `--skip-instrument` 라 대조를 건너뛰어 자리표시가 드러나지 않았다 | `"0"*40` 으로 고쳤다 |

## 4. 실측

```
tests/test_r17_followup.py                        26 passed         (신규 회귀 — 다섯 발견 + 대조군)
tests/test_r17_codex.py + r16 + followup          62 passed
tests/test_chain_rule_contract.py                  9 passed         (잡음 공유 뒤)
전수 python3 -m pytest tests/ -q                  451 passed · 1 failed  (524.06s)
  1 failed = test_i6d_04 (개수 계약 426 ↔ 수집 452) — 이번 라운드가 시험 26개를 더했다.
  WORKING_STATE 의 기대값을 452 로 갱신한 뒤 재실행: tests/test_r6_internal.py 52 passed.
```

수정 전 RED 관측: 같은 파일이 **19 failed · 7 passed** 였다 (통과한 7 은 전부 대조군 —
GC 원 반례 보존 · 정상 비교 · 두 번째 축 거부 · 합법 nullable · 일관된 best · 정상 영수증 ·
"상태는 내용 주소가 아니다"). 첫 판에서 시험 자신의 버그 둘(`near_optimal_extrema` 의 반환
모양, `_width_fields` 서명)을 고쳐 **이유가 맞는 빨강**으로 만든 뒤 production 을 고쳤다.

## 5. 하지 않은 것 · 경계

- **실데이터 재적합은 하지 않았다.** 이 회신은 그 승인을 요청하지 않는다. 리뷰어가 적은 대로
  목적·축·입력·version·자원·종료 조건을 고정한 **별도 승인안**이 필요하고, "한 항의 미분 수정이
  기존 실데이터의 LAM 부호·참 폭·물리 정답까지 자동 인증하지 않는다" 는 문장을 그대로 받는다.
- **`UNKNOWN_BLOCKERS` 기계 정본화** — 미착수 유지 (이미 신고된 항목).
- **원인 미확정 9건** — 리뷰어 Windows 환경의 108 실패 중 9건이 미확정으로 남았다. 우리가 그것을
  환경 문제로 단정하지 않는다. 이 회신은 **Linux 전수 로그를 첨부**하는 것으로 답하되, 그 로그가
  Windows 의 9건을 설명한다고 주장하지 않는다 — 두 환경의 숫자를 섞지 않는다.
- **GC 정책 하나는 아직 열려 있다**: "원장에 없는 파일을 디렉터리째 지우는 정책" 은 현재도
  `unknown` 검출에서 rc 2 로 멈추는 쪽이다. 리뷰어가 "명시적으로 정해야 한다" 고 한 축이라
  **문장으로 고정**하되 동작은 바꾸지 않았다.

  > **정정 (R17 후속 2차, 2026-09-22)** — 이 문장은 **코드와 달랐다.** 그때의 `unknown` 검사는
  > 시도 **디렉터리**만 열거했고 그 안의 파일은 보지 않았다 — 정상 index 의 디렉터리에 미등록
  > 파일을 하나 넣으면 `rmtree` 로 **같이 지워졌다** (리뷰어 실측 rc 0, `gc_unknown_file`).
  > 지금은 사실이다: `③ 모르면 안 지운다` 를 파일 단위까지 내렸고(rc 2), `rmtree` 자체를
  > 코드에서 없앴다 (검증한 파일만 unlink + 빈 디렉터리만 rmdir). **문장이 아니라 코드를 고쳐서**
  > 맞췄다 — 자세한 것은 `R17_FOLLOWUP2_RESPONSE.md` §2 F2-01.

## 6. 질문

1. **P1-01 의 겹침을 "거부(rc 2)" 로 했다.** 리뷰어의 최소 조건은 "거부하거나 보존을 우선한다"
   였다. 우리는 fail-closed 쪽을 골랐다 — 중복 index 자체가 producer 의 버그 신호라고 봤기
   때문이다. "보존 우선(그 항목만 건너뛰고 나머지는 지운다)" 이 의도였다면 되돌릴 수 있다.
2. **P1-02 의 결속 목록을 네 축**(`objective_version`·`cell`·`width_tol`·`run_id`)으로 했다.
   행에 있는 다른 공통 열(예: `si_source`)까지 넓혀야 하는가? 우리는 "행이 선언하고 sidecar 도
   선언하는 축" 만 넣었다.
3. **P2-02 의 `runtime`** 을 "비지 않은 객체" 로 요구했다. 생산자는 항상 채우지만, 빈 객체를
   허용해야 하는 경로가 있다면 알려 달라 (그 경우 `complete` 를 부분 상태로 가르는 쪽이 맞다).
4. **`package_content_digest` 의 정규화**를 "이름 정렬 + `sha256  이름` 줄 + 재해시" 로 했고,
   없는 파일은 `<missing>` 으로 적는다(ok 로 접지 않는다). payload/hash manifest 의 정규 내용
   digest 로 이 정의가 충분한가?

   > **정정 (R17 후속 2차, 2026-09-22)** — 위 "이름 정렬" 은 **구현과 달랐다.** 구현은
   > `sha256(bytes)  이름` **줄 전체**를 정렬한다 (해시가 앞이므로 사실상 해시 순). 리뷰어가
   > "결정성은 있으므로 새 버그로 세지 않는다" 고 판단한 그것이고, 우리는 **문서를 구현에 맞췄다**
   > (`evidence_gate.package_content_digest` docstring). 같이 적어 둔다: 이 값은 **그 목록이 이름
   > 붙인 파일들의 내용 주소**일 뿐이고, 실제 실행·독립 replay·디렉터리의 모든 파일·manifest
   > 원문을 인증하지 않는다. 목록의 누락·중복·범위 밖 이름의 계약은 **아직 정하지 않았다.**
   > 아래 §5 의 GC 문장 정정도 같이 볼 것.
