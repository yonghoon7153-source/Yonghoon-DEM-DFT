# R17 회신 — Codex 17차 (대상 `dfc1fc78`) NO-GO · P1 5 · P2 2 — 코드 6 건 닫음 · 과학 문장 좁힘 · chain rule 은 계약 제안

> ## ★ 발송 전 갱신 (2026-09-22) — ⑥ chain rule 계약은 **제안이 아니라 구현**이다
>
> 아래 본문은 작성 시점(계약 제안 단계) 그대로 둔다. 그 뒤 사용자 승인이 나와 같은 날
> 구현했으므로, 바뀐 사실만 여기 적는다 — 본문의 "제안" 표현은 지우지 않는다.
>
> | 항목 | 갱신 값 |
> |---|---|
> | **이 회신의 코드** | **`7c8f61f9`** — 이 커밋이 판정 대상이다. 이후 `bms-balancing/` 의 **파이썬 변경 0건** (`git diff --name-only 7c8f61f9..HEAD -- bms-balancing \| grep '\.py$'` → 빈 출력, 문서만 바뀌었다) |
> | §4 chain rule | **구현 완료.** `Objective(..., *, objective_version)` 기본값 없음 · `schema.OBJECTIVE_VERSIONS` 검증 · `cycles.fit_cycles` 와 `scripts/fit_cycles.py --objective-version` 필수(choices 고정, 빠뜨리면 rc 2) · 행·sidecar·`COMPARED_SETTINGS` 에 기록 · 파이프라인은 **명시적으로** `legacy_matlab` 을 넘긴다(호출 16곳 전부) |
> | §5 표의 "chain rule / 계약 제안" 줄 | **"구현 완료"** 로 읽어 달라. 단 같은 줄의 **"실데이터 A/B 는 사용자 승인 뒤"** 는 **그대로 유효**하다 — 실데이터 재계산은 **여전히 하지 않았다** |
> | §7 전수 회귀 | 본문의 `1 failed · 416 passed` → (그 실패는 개수 계약 갱신) → 이후 ⑥ 이 시험 9 건을 더해 **`426 passed in 638.13s (0:10:38)` · EXIT=0** (`python3 -m pytest tests/ -q -p no:cacheprovider`, `7c8f61f9` 트리에서 방금 실행). 개수 계약도 417 → **426** 으로 갱신했다 |
> | 회수 실측 (부수 관찰, 계약 아님) | LAM_NE 오차 — legacy `−3.39 / −7.49 / −3.12 %p` vs chain_rule_v2 `−0.0171 / −0.0577 / −0.0078 %p` (합성 truth 3종, `tests/test_chain_rule_contract.py` cr_04). 리뷰어 ②를 그대로 받아 **"200 배" 를 계약 회귀로 못 박지 않았다** — 회귀는 analytic 항등식 + `a=1` 대조군이다. ⚠ 셋째 값은 후속 회신에서 `+0.68 → −0.0078` 로 **정정**됐다 (잡음 배열을 두 버전이 공유하지 않던 것을 고쳤다 — 후속 §2) |
>
> 새 시험 9 건(cr_01~07)은 계약 부재 시 **9 failed → 구현 뒤 9 passed**. cr_07 은 첫 판에서
> 두 fixture 의 `w_dqdv` 가 같아 "축이 같다" guard 에 먼저 걸렸다 — A(legacy,w0)·B(v2,w1)·
> C(v2,w0) 세 fixture 로 고쳤다. validator 가 조여지면서 `test_widths` 의 W-16~21 fixture(자리표시
> 영수증)와 w15(점이 구간 밖)가 먼저 깨졌고, 의도를 유지하며 진짜 바인딩 키로 채웠다.
>
> RUN_SCOPE 밖(`bms-balancing/`)이므로 degradation-degeneracy 의 `source_digest` 는 움직이지
> 않았다 — 게이트 트랙과 섞지 않는다는 경계는 그대로다.

> 기계용 회신. 리뷰 원본은 `reviews/r17_repros/codex/pkg/R17_REVIEW.md` (패키지 zip sha256
> `ef14d6a82693266c6a89e6dd17152020ca96970f152a95f2c68cb5db85fedf2d`, 48,525 B, 28 파일).
> 리뷰어가 인용한 식별을 **우리 쪽에서 확인**했다: 요청문 `git show dfc1fc78:bms-balancing/reviews/R17_REQUEST.md | sha256sum`
> = `a434a10358536acba11cc03fc9b58d3a811d1ec4a3ef3a8d1b489ce76f723f76` · `out` 트리 = `1da2e9f5600dc5f91dd0a989188ef7b0ecb19437`.
> **둘 다 REVIEW_IDENTITY.json 과 일치** — 리뷰어는 우리가 보낸 바로 그 커밋을 봤다.

| 항목 | 값 |
|---|---|
| 리뷰 대상 | `dfc1fc78b3396c95709650860f1502c0e83ead40` |
| 이 회신의 코드 | 브랜치 head (커밋 SHA 는 push 후 확정 — 요청문 규칙 그대로) |
| 판정 수용 | **R17 NO-GO — 그대로 받는다.** P1 5 · P2 2 전부 인정. 과학 값은 하나도 다시 계산하지 않았고 실데이터 A/B 도 돌리지 않았다 |
| 판정 경계 | 게이트 리뷰(63·64·65차) · COMSOL 트랙과 **섞지 않는다** — 리뷰어가 적은 대로 |

## 0. 먼저 — 요청문의 틀린 문장 하나 (리뷰어 §1)

`R17_REQUEST.md` §0 의 "직전 라운드 | **R14 GO** — 대상 `1bb45b3`" 는 **틀렸다.** 우리 원장 `R14_RESPONSE.md` 첫 줄이
"대상 `1bb45b3` **NO-GO** · P2 3건" 이고, 회신 코드 `098728c` 를 담은 `3aca0906` 에서 잔여가 종결되어 GO 가 됐다.
요청문 본문은 리뷰된 그대로 두고(sha `a434a103…`) **머리에 정정 블록**을 붙였다. 옛 실패 시점을 GO 기준으로 소급하지 않는다.

## 1. 발견별 대응 — 코드 여섯 (P1-01~04 · P2-01 · P2-02)

리뷰어 반례를 **그대로** 회귀로 옮겼다: `tests/test_r17_codex.py` (27 시험). docstring 첫 줄이 리뷰어 항목 번호다.

| # | 리뷰어 반례 (실측) | 원인 | 고침 | 회귀 |
|---|---|---|---|---|
| **P1-01** | `partial/matrix/A/{100,200}` + `B/100`, `--keep 1 --apply` → rc 0 으로 **A 통째 삭제**, 200 의 유일한 결과 소실 | 보관은 (kind, artifact) · 삭제는 (kind, attempt) 디렉터리 — **두 모델** | `scripts/gc_partial.py`: 삭제 단위를 **index 항목 = 파일 하나**로 내림. 시도 디렉터리는 retained 항목이 **하나도** 참조하지 않을 때만 정리. index 도 같은 항목 단위. index `path` 가 partial 밖이면 rc 2 (모르면 안 지운다) | `test_r17_01` (200 의 A 가 남고 100 의 A 만 index 에서 빠진다) · `test_r17_02` (dry-run 도 파일 단위로 말한다) |
| **P1-02** | `publish_target(canonical, "partial", run_id=str(canonical.parent))` → **canonical 자체** 반환 | `Path / 절대경로` 가 앞 성분을 버린다. attempt-id 문법 검사 없음 | `bms_balancing/verify.py::publish_target`: `run_id` 는 **단일 경로 성분** `[A-Za-z0-9][A-Za-z0-9._-]{0,127}` 만. 해석된 목적지가 `partial/` root 아래이고 canonical 과 다른지 **첫 mkdir 전에** 확인 | `test_r17_03` (절대경로·`../`·구분자·빈 값·`.`·`..` 여섯 → `ValueError`, 디렉터리 생성 0) · `test_r17_04` (리뷰어 호출 그대로) |
| **P1-03** | 현행 `out` 사본에서 sidecar·run_id 만 지운 `--old <dir>` → rc 4 + **`legacy_transition_approved=true`** | `old_rev_full=None` 이면 (c) 비교를 **건너뛰었다** — None 이 wildcard 였다 | `scripts/check_u14.py::legacy_transition`: `old_rev_full` 이 없으면 승인 **없음**. 기록이 이름한 exact revision 과 대조했을 때만 승인. `--old <dir>` 비교 자체는 그대로 허용(rc 4, 승격 false) | `test_r17_05` (함수: 정상·다른 rev·None 셋) · `test_r17_06` (CLI: 리뷰어 fixture 그대로 → 승인 false) |
| **P1-04** | 설정 20 개를 채운 대조군에서 입력 SHA 변경·cycle 누락·cycle 중복·NaN 끝점·빈 tol 이 **전부 rc 0** | 일반 validator 를 안 탔다. 열거 설정만 견줬고 키 부재는 `None == None`. cycle 은 교집합·dict 축약 | `scripts/width_report.py`: ① `schema.check_rows("cycles")` 를 **먼저** 탄다(스키마·유한·receipt·union·중복 key) ② sidecar 필수 + `REQUIRED_META`(`sha256`·`run_id`·`cycles` + `BOUND_IDENTITY`) + `COMPARED_SETTINGS` **전부 존재** 요구 ③ 본문 bytes ↔ sidecar `sha256` ④ 행 receipt ↔ sidecar `consumed_inputs`/digest ⑤ 본문 cycle 집합 == sidecar 선언 (exact) ⑥ 비교 시 `BOUND_IDENTITY = (git_commit, env, consumed_inputs, dataset_manifest)` 동일 + 두 파일 cycle 집합 **exact** (교집합 없음) | `test_r17_07` (양성 rc 0 · seed 음성 rc 2 대조군) · `test_r17_08` (다섯 반례 전부 rc 2) |
| **P2-01** | `width_is_lower_bound="banana"`/`"False"`, `width_tol=-0.5`, `lo>hi` 가 `check_rows` 통과. `_width_fields(tol=-0.5)` 가 빈 허용집합을 **`measured`/폭 0** 으로 | union 이 **있고 없음**만 봤다. `near_optimal_extrema` 가 feasible 비면 `best` 를 복구값으로 넣었다 | `schema.check_width_union`: measured 면 태그 정확히 `True` · tol 유한 비음수 · lo ≤ hi 유한 · **점추정 ∈ 구간**. `verify.near_optimal_extrema`: tol/best_val 유한성·best 상자 안 검사 → `ValueError`; feasible 비면 `RuntimeError`(값을 지어내지 않는다) → `_width_fields` 가 `failed` 로 적는다 | `test_r17_09` (일곱 변형 거부 + 정상 대조군 통과) · `test_r17_10` (리뷰어 producer 호출 → `failed`) · `test_r17_11` (core 가 예외) |
| **P2-02** | code/instrument/signature 만 있는 receipt → **`verified=true`**, `receipt_version=null` | 서명·ancestry·tree 만 봤다 — 완전성을 안 봤다 | `scripts/verify_run_receipt.py`: 필수 8 키(`receipt_version`·`code`·`instrument`·`package`·`materialized`·`runtime`·`produced_utc`·`signature`) + 지원 version(`r16.1`) + `package.digest` 비공백을 **먼저** 검사. 빠지면 `verified=false`·rc 3. 코드 참조만 맞은 것은 **`code_reference_verified`** 라는 별도 상태 | `test_r17_12` |

리뷰어 표현을 그대로 받아 과장하지 않는다: P1-03 은 "일반 승격 우회가 아니라 **사용자 승인의 범위**가 넓어진 결함" 이고,
P2-02 는 "암호학적 위조가 아니라 **typed 완전성**의 결함" 이다. 둘 다 `promotion_eligible=false` 와 rc 는 그대로였다.

## 2. RED → GREEN 관측 (고치기 전에 눈으로 봤다)

```
# dfc1fc78 (리뷰 대상) 에 새 시험 파일을 얹어 실행 — reviews/r17_repros/ours/RED_at_dfc1fc78.txt
22 failed, 5 passed          # 통과한 5 는 전부 대조군 (dry-run · 빈 run_id · seed 음성/양성 · schema 의 NaN 검사 둘)

# 고친 뒤 (브랜치 head)
tests/test_r17_codex.py tests/test_widths.py → 50 passed in 140.21s
tests/test_r17_codex.py tests/test_widths.py tests/test_r16_partial_lifetime.py tests/test_r15_open_items.py
  tests/test_r16_run_receipt.py tests/test_cycles.py → 99 passed · 1 failed (아래 fixture) → fixture 정정 뒤 전부 통과
```

**validator 를 강화하면 fixture 가 먼저 깨져야 정상이다 — 이번에 둘이 깨졌다** (CLAUDE.md 규율 2 의 실측):

| fixture | 무엇을 가리고 있었나 | 어떻게 고쳤나 |
|---|---|---|
| `test_widths._fake_widths_csv` (W-16~W-21) | `inputs_sha="s"` · `consumed_inputs="{}"` **자리표시 receipt**, sidecar 에 `sha256`·`git_commit`·`env`·`consumed_inputs` 없음 — 결속 없는 CSV 로 "비교가 성립한다" 를 시험하고 있었다 | 실제 `fit_cycles` → `sidecar_dict` 모양으로 올렸다 (유효 receipt · 결속 키 전부). 시험 의도(W-16 성립 · W-17/W-21 거부)는 그대로 |
| `test_w15` 의 `ok_on` 행 | 점추정 **1.0** 에 구간 **[0.01, 0.01]** 을 "정상 measured 행" 으로 | 점추정을 구간 안(0.01)으로. union 의 있고/없음 의도는 그대로 |

## 3. P1-05 — 과학 결론을 관측이 지지하는 만큼으로 좁혔다

`BML_R1_RESPONSE.md` 의 해당 절에 **원문을 지우지 않고 `R17 정정` 블록을 덧붙였다** (반론 보존). 요지:

| 절 | 철회하는 문장 | 수용 가능한 문장 |
|---|---|---|
| §12-6 | "다른 설정은 원인이 아니고 비식별성이다" · "multistart 가 같으므로 진짜 전역 최소다" — 리뷰어의 `J=‖p−a‖²` (Hessian 2I, 유일해) 반례에서 같은 현상이 나온다 | "시험한 두 γ 시작/하한 변경은 LAM 차이를 설명하지 못했다." 두 모델 차이는 **model discrepancy** 일 수 있다. §12-2 결론의 근거 자리를 **§13·§14 폭 측정**으로 옮긴다 |
| §14-1 | "`width_report` rc 0 이 그 자체로 증거다" — P1-04 로 무효 | 그 시점 rc 0 은 "설정 20 개가 같다" 까지. `git_commit`·`env`·입력은 **사람이** 대조했고 기계가 증명하지 않았다. 두 파일은 결속 키(`dataset_manifest`, R16 축 ②) 이전 산출이라 새 reader 로 읽히지 않는다 → **조건 동일성 "미검증"** 으로 내림. "두 파일이 실제로 달랐다" 는 주장이 아니다 |
| §14-3 (·§14-4) | "dQ/dV 를 넣어 LAM_NE 의 부호 식별을 **잃었다**" · "참 폭이 넓어졌다" · "LLI 가 **참으로** 가장 좁다" | 폭은 **하한**이다. 관측 하한 2.439/7.099 는 참 폭 20/8 과 양립한다. **말할 수 있는 것**: B 에서 유효한 양·음 witness 를 찾았다 → B 의 부호는 모호. "찾은 하한이 2.91 배". **말할 수 없는 것**: A 의 부호 식별(양수 witness 만 찾은 것은 하한). `J ≤ 1.01·J_min` 은 최소값 비례 허용이라 신뢰구간·정보량으로 읽지 않는다. 다음 측정부터 **signed witness 의 p 와 J 를 저장**한다 |
| §15-6 | 가설 셋 "**배제**" · "optimizer·방향·범위는 배제됐고 포팅 버그가 아니다" | "검토한 합성 변형에서는 영향이 없었다." 방향 규약·측정 범위·포팅은 **열린 원인**. 닫으려면 실데이터의 통제된 방향/범위 변형 + native 구현의 같은 입력 중간 배열 대조. 세 자릿수 RMSE 차이는 관측이지 원인 서명이 아니다 |
| §12 제목 | "**정답 있는 데이터**" | "**외부 도구 참조값이 있는 자료**" — pyDMA 는 모델 기반 도구이고 구현 간 일치 ≠ 물리 truth. `WORKING_STATE.md` 의 같은 문구도 정정 |

## 4. chain rule — 리뷰어 §4 답을 받는다. **계약을 제안했고, 사용자 승인(2026-09-22) 뒤 같은 날 구현했다**

리뷰어 답 넷을 그대로 채택한다. 아래 표의 "제안" 이 그대로 구현됐다 — RED `tests/test_chain_rule_contract.py`
**9 failed → 9 passed**, 회수 실측은 `FINDINGS.md` §1-2-b. **실데이터 재계산은 여전히 하지 않았다** (승인된 계산이 아니다).

| 리뷰어 답 | 우리가 세울 계약 (제안) |
|---|---|
| ① 1/a 는 수학적으로 고쳐야 한다. 충실 포팅은 **명시 legacy 모드**로 보존 | `objective_version ∈ {"legacy_matlab", "chain_rule_v2"}`. **신규 실행은 명시 선택 필수** (기본값 없음 — 침묵 기본값으로 알려진 잘못된 미분을 권하지 않는다). 기존 재현 작업은 `legacy_matlab` 을 **명시**해서 돈다 |
| 값이 **행·sidecar·receipt·비교기**에 전달되고 섞이지 않아야 | `CYCLES_ROW` 에 `objective_version` 열 · sidecar 키 · `width_report.BOUND_IDENTITY` 에 추가(두 버전을 견주면 rc 2) · `check_u14` 의 controls 축에 포함 |
| ② "200 배" 를 계약 회귀로 못 박지 말 것 | 회귀는 **analytic chain-rule 항등식**(`E_PE=3+x²`, `E_NE=0.2+0.3x²` 류, `a≠1`) + `a=1` 대조군 + 복수 truth/잡음/평활/bound 의 회수 정확도. 리뷰어 독립 확인(legacy 최대 오차 0.370833 → 수정 4.03e−10)을 그 형태로 고정. 우리 200 배는 **보조 관측**으로만 기록 |
| ③ 편향 ≠ 폭. B 의 폭 방향은 미지수 | B 로 baseline/target/scales/witness 를 **전부 새로** 계산한 뒤에만 폭을 말한다. 현행 폭은 pristine `ref_p` 고정의 **조건부 폭**이라 기준 상태 불확실성을 덮는다고 적지 않는다 |
| ④ `w_dvdq=1` + 잘못된 미분은 신규 추정의 안전한 기본값이 아니다 | 신규 진단은 pOCV-only ↔ corrected derivative 를 **나란히** 비교한 뒤 기본을 정한다. dV/dQ 는 같은 전압의 변환이므로 0 으로 두는 것을 "독립 정보 상실" 로 단순 해석하지 않는다. `w_dqdv` 는 별개 항 — 바꿔서 고친 것으로 기록하지 않는다 |

## 5. 리뷰어 §5 조건별 — 이 회신 뒤의 상태

| 조건 | 리뷰어 판정 | 이 회신 |
|---|---|---|
| legacy_transition 별도 승인 | 미종결 | **닫음** (P1-03) |
| partial 수명/GC | 미종결 | **닫음** (P1-01 · P1-02) |
| width tagged union/비교 | 미종결 | **닫음** (P1-04 · P2-01). ⚠ §14 의 두 실데이터 파일은 새 reader 로 읽히지 않는다 — 결속된 재실행 전까지 "미검증" |
| run receipt | 부분 | **닫음** (P2-02) — 완전성 검사 + 부분 상태 분리 |
| C 의 비식별성·폭·γ 원인 결론 | 재작성 필요 | **좁혔다** (§3). 근거의 자리를 옮기고 철회 문장을 명시 |
| chain rule | 알려진 미구현 | **계약 제안** (§4). 구현·실데이터 A/B 는 사용자 승인 뒤 |
| unknown 사유 셋의 문서 표류 | 개선 필요 | **미착수** — `UNKNOWN_BLOCKERS` 를 기계 정본으로 결정 기록 스키마·보고 템플릿을 생성/대조하는 것은 다음 라운드 |
| preserve_handoff 실전 shell · fcntl 시험 | 환경 미완 | 이 컨테이너(Linux)에서 전수 회귀로 확인 — §7 |

## 6. 하지 않은 것

- **실데이터 A/B 를 돌리지 않았다.** 리뷰어: "아직 요청/승인된 계산이 아니다."
- **chain rule 을 구현하지 않았다.** §4 는 계약이다.
- **§14 의 숫자를 다시 만들지 않았다.** 그 파일들은 결속 키 이전 산출이고, 새 reader 로는 읽히지 않는다는 사실을 그대로 적었다.
- **`UNKNOWN_BLOCKERS` 기계 정본화**는 미착수.
- 과학 값·산출 bytes 는 이번에도 건드리지 않았다.

## 7. 회귀 (이 컨테이너 · Linux · fcntl/Bash 있음)

- `tests/test_r17_codex.py` + `tests/test_widths.py` → **50 passed** (140.21 s)
- 여섯 파일 표적 (`test_r17_codex` · `test_widths` · `test_r16_partial_lifecycle` · `test_r15_open_items` · `test_r16_run_receipt` · `test_cycles`) → **100 passed** (fixture 정정 뒤)
- 전체 `python3 -m pytest tests/ -q`: **아래 줄에 실측으로 채운다 — 채워지기 전에는 390 재확인을 주장하지 않는다.**

```
$ python3 -m pytest tests/ -q -p no:cacheprovider                    # 이 컨테이너 · Linux · 2026-09-22
1 failed, 416 passed in 611.33s (0:10:11)                            # rc 1
FAILED tests/test_r6_internal.py::test_i6d_04_working_state_test_count_matches_the_collection
  AssertionError: ('# 390 passed 기대', 417)
```

그 하나는 **문서 계약**이다 — `WORKING_STATE.md` 의 "N passed 기대" 가 수집 개수와 같아야 하는데(R6 내부 DF-04),
이 라운드가 27 시험을 더해 390 → **417** 이 됐고 전수가 도는 중에 문서를 고쳤다. 그 시험만 다시 돌렸다:

```
$ python3 -m pytest tests/test_r6_internal.py::test_i6d_04_working_state_test_count_matches_the_collection -q
1 passed in 4.57s
```

즉 **417 수집 · 417 통과** 다 — 다만 "417 passed 한 줄" 은 두 실행을 합친 것이라 그렇게 적지 않는다. 실측은 위 둘이다.
R14 대상 시점 277 → 286 → 326 → 332 → 390 → **417**.

리뷰어 환경의 3 failed(Bash 1 · fcntl 2)는 이 환경에서는 조건이 달라 그대로 재현되지 않는다 — 그것은 "통과" 가 아니라
"다른 환경" 이다. Windows 재현이 필요하면 fcntl 없는 경로의 skip 사유 출력을 별도 항목으로 연다.

## 8. 증거 파일

- 리뷰 패키지 원문: `reviews/r17_repros/codex/R17_REVIEW_PACKAGE.zip` + `pkg/` (bytes 그대로)
- 수정 전 BAD 출력 (대상 커밋에 새 시험을 얹어 실행): `reviews/r17_repros/ours/RED_at_dfc1fc78.txt`
- 수정 후 의도한 거부: `tests/test_r17_codex.py` 27 시험 자체가 그 출력이다 (각 assert 메시지가 리뷰어 항목을 인용)
