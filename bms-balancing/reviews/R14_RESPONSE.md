# R14 회신 — Codex 14차 (대상 `1bb45b3`) NO-GO · P2 3 건 — 전부 닫음

> 기계용 회신. 리뷰 원본은 `reviews/r14_repros/codex/pkg/HARNESS_R14_1BB45B35_CODEX_REVIEW.md`
> (패키지 zip sha256 `72f9556e2230e7c3638303176b9bf6b9a7364f27c8273427f5a628c7450114bd`).
> 리뷰어가 인용한 식별을 **우리 쪽에서 확인**했다: 요청문 `reviews/R14_REQUEST.md` 의 sha256 =
> `17995cfd90cd838c1cc1a1df43b6cceecf59ecc615878a75c491e7fea04f9f77` · 대상 tree = `git rev-parse 1bb45b3^{tree}` =
> `128fc38539fb7d996610f843b996855bd7f7b99d`. **둘 다 일치** — 리뷰어는 우리가 보낸 바로 그 커밋을 봤다.

| 항목 | 값 |
|---|---|
| 리뷰 대상 | `1bb45b358db4850c73e185d5f851e35fbcff9ad6` |
| 이 회신의 코드 | 아래 §4 (커밋 SHA 는 push 후 확정) |
| 회귀 | `python3 -m pytest tests/ -q` → **286 passed** (리뷰 대상 시점 277) |
| 판정 수용 | R14 NO-GO · **U18b 이관 수용 · 재계산 불필요** — 그대로 받는다. 과학 값은 하나도 다시 계산하지 않았고 옛 sidecar 도 고치지 않았다 |

## 1. 발견별 대응

| # | 리뷰어 반례 (실측) | 원인 | 수정 | 회귀 |
|---|---|---|---|---|
| **P2-1** | 새 합성 저장소에서 `OUT=reports/out_u18` 에 CSV 하나 → `git_dirty: true` · `git_modified_code: ["reports/"]`. 얕은 `out_alt` 는 false | `git status --untracked-files=normal` 이 untracked 디렉터리를 **상위 하나로 접는다**(`?? reports/`). 접힌 상위는 지정 root 안이 아니므로 코드로 분류됐다. 시작·끝에 같은 OUT 을 넘기는 U18-02 의 고침으로는 안 닫힌다 | `scripts/provenance.py` — 접힌 untracked 항목이 **지정 root 를 품고 있으면** 그 경로만 `git status -uall -- <dir>` 로 다시 물어 **실제 파일**로 펴서 분류한다 (`_untracked_files`). 저장소 전체를 `-uall` 로 바꾸지 않는다: 큰 untracked 트리에서 sidecar 의 `git_modified_code` 가 수천 줄이 된다 | `test_h01` 3 케이스 — 얕은 OUT false · **중첩 OUT false** · 중첩 OUT + root 밖 sibling **true 이고 `git_modified_code` 가 접힌 `reports/` 가 아니라 `reports/notes.txt` 를 지목** |
| **P2-2** | 현행 정본 사본에서 `env={"python": …}` 만 남겨도 matrix·profile·shape·degeneracy 넷 다 `--schema-only` **rc 0** | 검사가 "비어 있지 않은 dict 인가" 까지만 봤다. `ENV_KEYS` 다섯 축 검사는 **baseline 비교 경로**에만 있었다 (R13 P2-4 의 범위 잔존) | `scripts/check_u14.py` — baseline 과 **무관하게** 새 sidecar 전부에 다섯 축의 존재·비공백을 요구한다. 옛 정본의 부재는 그대로 비교 경로의 `env_uncomparable`(rc 4)이고 이 검사와 섞이지 않는다 | `test_h02` 네 종류 × (온전 rc 0 대조군 · **다섯 축을 하나씩 뺀 다섯 케이스 각각 rc 2** · python 만 남긴 리뷰어 반례 rc 2 · env 자체 없음 rc 2) |
| **P2-3** | 대상 HEAD 에서 `--old-rev HEAD` → rc **2** · `alias 13` (문서는 rc 4 라고 적었다). 증거 README 의 `git diff ef8e8f6 HEAD … '*.py' '*.sh'` → **17 개** | 승격 커밋 **뒤**에는 HEAD 의 `out/` 이 이미 새 정본이라 같은 run_id 13 개와 자기대조가 된다. 도구의 거부가 맞는 동작이고 **문서의 문맥이 틀렸다**. README 명령도 옛 코드 정본에서 이어받은 범위였다 | 기준을 **full commit 으로 고정**: `R13_RESPONSE.md` §8-1 은 `--old-rev 42314198e0beee59834d394cdba2757183503b59`(= `37a889b^`) → rc 4 로 적고, 승격 뒤 `--old-rev HEAD` 는 rc 2 · `alias 13` 이며 그것이 맞는 동작이라고 함께 적는다. 증거 README 의 코드 동일성 명령은 `df6413d…` → `1bb45b3…` 범위로 정정 | 문서 정정 (코드 변경 없음). 우리 쪽 실측 재현은 §2 |

## 2. 우리 쪽 재현 (고치기 전 · 방금 실행)

```
# P2-3 — 리뷰어 관측 그대로 재현된다
$ python3 scripts/check_u14.py --new out --old-rev HEAD
rc 2 · blocked_by {alias: 13, numbers: 0, 나머지 0}
$ python3 scripts/check_u14.py --new out --old-rev 42314198e0beee59834d394cdba2757183503b59
rc 4 · blocked_by {inputs_uncomparable: 17, env_uncomparable: 1, 나머지 0}
$ git diff ef8e8f6 1bb45b3 --name-only -- '*.py' '*.sh' | wc -l     → 17
$ git diff df6413d 1bb45b3 --name-only -- '*.py' '*.sh' | wc -l     → 0
```

P2-1·P2-2 는 `test_h01`·`test_h02` 가 리뷰어 스크립트를 그대로 옮긴 것이고, **고치기 전 6 건 실패**(얕은 OUT
1 건만 통과)를 눈으로 확인한 뒤 고쳤다. 리뷰 패키지 원문은 `reviews/r14_repros/codex/` 에 bytes 그대로 보존했다.

## 3. 리뷰어 답(§7)에 대한 우리 처리

| 리뷰어 답 | 우리 처리 |
|---|---|
| 1. `env_uncomparable` 분류 수용 · 새 candidate 독립 env 검사는 P2-2 로 완성 | **그대로 했다** (P2-2). 옛 baseline 부재는 rc 4·비승격 유지, 새 sidecar 부분 기록은 rc 2 |
| 2. 포괄적 `--accept-uncomparable` 대신 `legacy_transition_approved` 별도 판정 · `promotion_eligible:false` 유지 | **동의한다. 이번 회신에서는 구현하지 않았다** — 게이트 계약 변경이라 다음 라운드의 설계 항목으로 연다 (§5). 이번 이관은 리뷰어 표현대로 **일회성 legacy 이관**으로 기록되어 있고 승격 커밋 본문이 rc 4 와 `promotion_eligible:false` 를 그대로 담고 있다 |
| 3. 기본은 단일 commit · 이번 혼재는 범위 한정 예외로 기록 | **그렇게 기록한다** (§5 의 U18-05). 두 full commit `0668665…` · `419c1ab…` 와 그 사이 코드 동등성 검토 범위를 고정해 둔다. 일반 허용 규칙으로 만들지 않는다 |
| 4. 기록용 CLI 에서 인자 생략을 오류로 · 단 P2-1 은 그것으로 안 닫힌다 | P2-1 은 접힌 경로 쪽을 고쳐 닫았다. **인자 필수화는 하지 않았다** — 호환성 판단이 필요하고 리뷰어도 별도 명시 모드를 대안으로 둔다. 열린 항목 (§5) |
| 5. 실제 역사 bytes 유지 | **유지한다.** `out/archive/legacy_r6_u14/` 는 그대로이고 `test_d8_02`·`test_f26` 이 그 경로를 표본으로 쓴다 |

## 4. 검증 — 방금 실행 (clean 트리)

```
$ PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider
284 passed                                    # 리뷰 대상 277 → +7 (test_h01 3 · test_h02 4)
$ python3 scripts/check_u14.py --new out --schema-only                      → rc 0 (변화 없음)
$ python3 scripts/check_u14.py --new out/archive/legacy_r6_u14 --schema-only → rc 2 · 40·25·6·1 (변화 없음)
```

**과학 값·산출 bytes 는 건드리지 않았다.** P2-1 은 provenance 분류, P2-2 는 게이트 검사, P2-3 은 문서다.

## 5. 열린 것 (이번 회신이 닫지 않은 것)

| 항목 | 상태 |
|---|---|
| `legacy_transition_approved` 판정 (리뷰어 §7-2) | **닫음 (R15, 2026-09-15)** — §8 |
| 기록용 CLI 의 output-root 인자 필수화 (리뷰어 §7-4) | **닫음 (R15, 2026-09-15)** — §8 |
| **U18-05** — 승격 묶음의 `git_commit` 혼재 | **닫음 (R15, 2026-09-15)** — §8. 리뷰어 권고대로 **기본은 단일 commit**. 이번 자료는 `0668665…`(9 개) + `419c1ab…`(4 개) 혼재이고 그 사이 `*.py`·`*.sh` diff 가 0 인 범위 한정 예외로 기록한다 — `.m`·설정·의존성까지 일반적으로 덮지 못한다는 지적을 받아들인다 |
| 조건 6(동적 인증) · 조건 8(다섯 축) | 열림 — 리뷰어도 새 발견으로 세지 않았다 |
| `openpyxl` 이 `ENV_KEYS` 에 없음 | 열림 — 별도 라운드 (P2-2 와 분리하라는 지적 그대로) |
| r11 `publish:profile_partial_stdout` 대체 증거 없음 | 열림 — `closed_with_substitutes: false` 로 그대로 |
| Octave 1~3 단계 · 동적 우회 재생 10 건 | 리뷰어 기계에서 미실행. 우리 쪽 277→284 전수 통과를 리뷰어의 재확인으로 쓰지 않는다 |

## 6. 우리가 고치지 않은 것 하나 — `R14_REQUEST.md`

요청문 §2 에도 같은 `--old-rev HEAD` 문맥 오류가 있다. **그 파일은 고치지 않는다** — 리뷰어가 sha256
`17995cfd…` 로 고정해 심사한 원본이고, 고치면 그 식별이 깨진다. 정정은 이 회신과 §1 P2-3 의 두 문서(현행
`R13_RESPONSE.md` · 증거 README)에 둔다. 다음 요청문부터 **승격 전/후 명령을 구분하고 기준을 full commit 으로**
적는다.

---

## 7. 후속 확인 (`f21cb648`) 에 대한 2 차 회신 — P2-2 의 공백값 잔여 닫음

리뷰어가 `f21cb648` 을 다시 봤다: **P2-1 종결 · P2-3 종결 · P2-2 부분**. 남은 것 하나는 우리 잘못이 맞다.

| 항목 | 리뷰어 실측 | 원인 | 수정 | 회귀 |
|---|---|---|---|---|
| P2-2 잔여 | `env.scipy` 가 `""`·`null` 이면 rc 2 인데 **`"   "`·`"\t\n"` 이면 rc 0** | 우리 검사가 `in (None, "")` 였다 — 회신과 주석에 적은 **"존재·비공백"** 이 절반만 구현됐다. degeneracy **본문** 검사는 이미 `str(v or "").strip()` 로 재고 있었으므로 **규칙이 두 벌**이었다는 뜻이기도 하다 | 규칙을 **한 자리**로: `schema.env_axes_missing(env)` 를 만들고 본문 검사와 sidecar 검사가 **같은 함수**를 부른다. `str(… or "")` 가 None·빈값을 흡수하고 `.strip()` 이 유니코드 공백(NBSP 포함)까지 깎는다 | `test_h02` 확장 — 네 종류 × 다섯 축 × **다섯 빈값**(`""` · `"   "` · `"\t\n"` · NBSP · `null`) 전부 rc 2. 기존 축(키 누락 · python 만 · env 전체 부재 · 온전 대조군 rc 0)은 그대로 |

리뷰어가 종결로 본 둘은 우리 쪽에서도 그대로 둔다 — `_untracked_files()` 와 root 밖 sibling 회귀(P2-1),
full commit 기준 고정과 자기대조 rc 2 기록(P2-3).

검증 (방금 실행): **286 passed** · `check_u14 --new out --schema-only` rc 0 · legacy archive rc 2 (40·25·6·1) —
과학 값·산출 bytes 는 이번에도 건드리지 않았다. 리뷰 패키지 원문은 `reviews/r14_repros/codex/followup_f21cb648/`
(zip sha256 `f1d39ff1d5fe1797b2d3de0932fb6febb62acc8b7b05bef38d4e08c66df0fef7`).

열린 것은 §5 그대로였다 (`legacy_transition_approved` · 기록용 CLI 인자 필수화 · U18-05 · 조건 6·8 ·
openpyxl · r11 대체 증거). 리뷰어도 그것들을 이번 종결의 차단 사유로 세지 않았다.
**그 셋을 2026-09-15 에 닫았다 — §8.** 남은 것은 조건 6·8 · openpyxl · r11 대체 증거 셋이다.

---

## 8. R15 — 리뷰어 §7 의 답 2·3·4 를 구현으로 닫는다 (2026-09-15)

§5 가 "다음 라운드" 로 미뤄 둔 셋이다. 리뷰어가 종결의 차단 사유로 세지 않았으므로 급하지는
않았지만, 미루면 다음 승격에서 같은 자리가 다시 열린다. **셋 다 재현 시험부터 닫았다** —
`tests/test_r15_open_items.py` 첫 실행 **12 failed · 2 passed** (통과한 둘은 "바뀌지 않는다" 를
재는 대조군이다).

### 8-1. U18-05 — 묶음 commit 혼재 (리뷰어 §7-3)

전 판은 sidecar 마다 `git_commit_at_start` 가 40-hex 인지만 봤다. **묶음 전체가 한 코드
상태에서 나왔는가는 아무도 안 봤다.** 우리가 손으로 diff 를 떠서 무해함을 확인했을 뿐이고,
리뷰어의 지적("`.m`·설정·의존성을 `*.py`·`*.sh` 만으로 일반적으로 덮을 수 없다")이 정확히
그 확인 방식을 겨눈 것이다.

`check_u14` 가 이제 후보 묶음의 커밋 집합을 모아 **혼재를 계약 위반(rc 2)으로** 센다.
`blocked_by.bundle_commits` 가 그 수이고, 사람용 출력은 어느 커밋이 몇 개인지 이름으로 적는다.

예외는 **일반 허용 규칙이 아니라 기록**이다 — `reviews/PROMOTION_DECISIONS.json` 에
두 full commit·산출 명부·코드 동등성 검토 범위를 적고, `check_u14` 는 **정확히 같은 커밋
집합**에만 그 기록을 건다. 짧은 sha·와일드카드·빈 목록은 형식 검사에서 거부된다.

이번에 코드 동등성 근거를 **다시 쟀다**. R14 요청문은 `-- '*.py' '*.sh'` 필터판(0 개)을
인용했는데, 리뷰어 지적을 받아 필터를 빼고 전체 diff 를 적는다:

```
git diff --name-only 066866595ab71827ef2d98e7a6cf26136df21495 419c1abaeec9fa981d7f5829d5803167288f7f1e
→ 5 개, 전부 문서·증거 목록
   bms-balancing/WORKING_STATE.md · docs/COMSOL_REBUILD_SPEC.md · reviews/R13_RESPONSE.md
   reviews/r14_repros/codex63/time_caps/FULL_LISTING.tsv · …/ZIP_SHA256.txt
```

필터 없이도 계산에 쓰이는 파일은 하나도 없다. 그것이 이 예외를 기록으로 둘 수 있는 근거다.

**fail-closed 실측**: 기록 파일을 치우고 정본을 다시 재면 `rc 2 · bundle_commits 1` 이고
`066866595ab7 (9 개) · 419c1abaeec9 (4 개)` 를 지목한다. 예외가 사라지면 조용히 넘어가지
않는다는 뜻이다.

### 8-2. `legacy_transition_approved` (리뷰어 §7-2)

포괄 `--accept-uncomparable` 로 rc 0 을 만들지 않았다 — 그런 플래그는 **만들지도 않았다.**
대신 `PROMOTION` JSON 에 판정 둘을 더했다: `legacy_transition_approved` · `legacy_transition`.

승인 조건은 넷이다. 막는 것이 `inputs_uncomparable`·`env_uncomparable` 뿐이고 그중 하나
이상이 실제로 있을 것 · 새 묶음의 명부가 기록과 같을 것 · 코드 커밋 집합이 기록과 같을 것 ·
기록이 이름한 옛 리비전과 대조했을 것. 계약 위반이 하나라도 있으면 승인은 **없다**.

실측 (`python3 scripts/check_u14.py --new out --old-rev 42314198`):

```
rc 4 · promotion_eligible false · legacy_transition_approved true · legacy_transition U18B-2026-09-14
blocked_by  inputs_uncomparable 17 · env_uncomparable 1 · 나머지 전부 0
```

리뷰어가 요구한 그대로다 — **`promotion_eligible: false` 를 지우지 않았고 rc 도 4 그대로다.**

### 8-3. 기록용 CLI 의 산출 root 인자 (리뷰어 §7-4)

U18-02 는 **부르는 쪽**을 고쳤고 CLI 자신은 여전히 침묵으로 `out` 을 가정했다. 이제:

| 부름 | 결과 |
|---|---|
| `provenance.py <art>` | **rc 2** — 산출 root 를 명시하라고 말한다 |
| `provenance.py <art> ""` | **rc 2** — 빈 문자열(미설정 `$OUT`)은 root 가 아니다 |
| `provenance.py --default-out-diagnostic <art>` | rc 0 · `output_roots_mode: "default-out-diagnostic"` |
| `provenance.py <art> "$OUT"` | rc 0 (production 경로) |

`--verify-unit`·`--check-run-id` 는 기록 모드가 아니므로 계약을 안 바꿨다.
`run_states.sh` 는 `"${OUT:-out}"` 를 **확정된 `"$OUT"`** 로 바꿨다 — 기본값이 두 자리에
생기면 시작·끝이 어긋날 수 있고, 그 어긋남이 U18-02 였다.

### 8-4. 실전에서 하나 더 — 스크립트가 흡수된 브랜치로 push 하라고 찍고 있었다

사용자가 `preserve_handoff.sh` 로 COMSOL `physical600_b` 원문을 보존한 뒤(163 항목 전수 일치 ·
111 보존 · 복사 뒤 재대조 111/111), 스크립트가 마지막에 찍은 안내가 **본진이 흡수한 서브
브랜치로 push 하라**고 말하고 있었다. 그대로 따랐으면 새 커밋을 얹지 않기로 한 브랜치(루트
`CLAUDE.md` 하드룰 1)에 1 GB 짜리 묶음의 보존 커밋이 올라갔을 것이다.

요청문 쪽은 `test_review_request_clones_the_branch_that_owns_bms_balancing` 이 이미 막고
있었고 **스크립트 쪽은 아무도 안 봤다.** 2026-08-20 에 이 저장소의 여덟 곳이 대체된 이름을
붙들고 있던 것과 같은 형태다. 이름을 루트 `CLAUDE.md` 의 브랜치 표에서 **읽게** 고치고,
`scripts/*.sh`·`*.py` 전체를 훑는 회귀로 고정했다
(`test_no_script_tells_the_operator_to_push_to_a_retired_branch`). 표를 못 읽으면 지금
브랜치로 적되 경고를 찍는다.

주석에도 옛 이름을 적지 않는다 — 첫 수정판이 주석에 그 이름을 남겼다가 자기 회귀에 걸렸다.
**이름을 옮겨 적지 않는 것**이 규칙이고, 규칙은 주석에도 걸린다.

같은 안내문에서 하나 더 나왔다. 재대조 python 블록이 **저장소 루트 기준** 경로를 쓰는데 그
명령을 찍는 자리는 `bms-balancing/` 안이다 — 사용자가 복사해 치자 `FileNotFoundError` 였다.
블록 앞에 루트로 옮기는 줄을 넣었다(그 위 git 세 줄은 이 디렉터리 기준이라 그대로 둔다).
회귀가 그 순서까지 고정한다: 루트로 옮기는 줄이 `git push` 안내보다 앞이면 그 세 줄이 깨진다.

**안내문은 사람이 그대로 붙여 넣는 코드다.** 두 결함 다 "사람이 알아서 고쳐 치겠지" 를 전제로
남아 있던 자리이고, 둘 다 실전에서 터졌다.

### 8-5. physical600_b 보존 완료 (2026-09-15)

COMSOL 물리축 B 원문이 저장소에 들어왔다 — manifest 명세 163 전수 일치 · 보존 111 · 제외 52
(mph·로그·java·그림·py·중첩 ZIP·8 MiB 초과 CSV) · 복사 뒤 재대조 111/111 · **커밋 안 bytes
재대조도 111/111 불일치 0** (manifest self-SHA `7945b6a7785ced88…`). 줄끝 정규화는 안 먹었다.
이제 §19 의 "전달값" 배너를 우리 실측으로 바꿀 수 있다 (COMSOL 문서 쪽 작업).

### 8-6. 보존 스크립트의 셋째 결함 — manifest 이름 규약

`desktop_postproc` 묶음을 보존하려다 4 단계에서 멈췄다: "전달값 `134ceb89…` 를 가진 manifest 가
ZIP 안에 없다". **실제로는 있었다.** 그 묶음의 manifest 는 이름이 `manifest.json` 이고 해시가
정확히 그 값인데, 스크립트는 `package_manifest.json` 만 찾았다 — 찾아낸 하나는 재사용 증거로
딸려 온 **이전 묶음(physical600_b)의** 것이었다.

멈춘 것 자체는 옳다. 엉뚱한 manifest 로 보존하면 무엇을 대조한 것인지 알 수 없다. 고칠 것은
**후보 집합**이고, 고르는 규칙(`--expect-manifest-sha` 로 해시 일치)은 그대로 둔다 — 그래서
이름을 넓혀도 fail-closed 다. 이름에 manifest 가 들어간 것을 **전부** 담지는 않는다
(`normal_raw_csv_manifest.json` 처럼 다른 층의 것이 있다). 회귀는 스크립트의 `find` 표현식을
소스에서 꺼내 임시 트리에서 **실제로 돌려** 세 후보 중 둘만 잡히는지 잰다.

세 결함(브랜치 이름 · 작업 디렉터리 · manifest 이름) 다 **다른 사람이 실제로 쓰다가** 걸렸다.
이 스크립트는 우리 기계에서만 돌려 본 적이 있고, 사용자 기계에서 처음 돈 것이 이번이다.

### 8-7. 넷째 — manifest 의 **항목 목록 키**가 묶음마다 다르다

manifest 이름을 고친 뒤 desktop_postproc 은 통과했다 (명세 82 전수 일치 · 보존 50 · 커밋 안
bytes 재대조 50/50). 그런데 **그 다음 세 묶음이 또 멈췄다** — 5 단계에서 `manifest 에 entries
가 없다`. ZIP 크기·SHA·manifest 해시는 셋 다 전달값과 **정확히 일치**했다.

다른 것은 자료가 아니라 **키 이름**이었다.

| 묶음 | 목록 키 |
|---|---|
| `desktop_postproc` | `entries` |
| `electrolyte_guard` · `physical600_b_review` | `files` |
| `electrolyte_recovery` | `payload` |

항목 모양은 셋 다 같다 (`path` · `bytes` · `sha256`). 판별을 `scripts/handoff_manifest.py`
한 자리로 뺐다 — bash heredoc 안에 두면 시험할 수 없고, 시험할 수 없는 규칙은 다음에 또 갈린다.
계약은 셋이다: 항목마다 `path`·`sha256` 이 **둘 다** 있을 것 · 쓸 만한 후보 키가 **둘 이상**이면
고르지 않고 멈출 것 · 모르는 모양은 계속 멈출 것. 새 묶음이 또 다른 이름을 쓰면 `ENTRY_KEYS` 에
**한 줄**을 늘리고 회귀를 같이 넣는다.

**네 결함의 공통 원인은 하나다.** 이 스크립트는 우리 기계에서만 돌아 봤고, 사용자 기계에서 처음
돈 것이 이번이다. 브랜치 이름 · 작업 디렉터리 · manifest 이름 · 목록 키 — 넷 다 "우리 환경에서는
한 가지 모양만 봤다" 에서 나왔다.

**그리고 첫 수정판이 반만 고쳤다.** 5 단계만 바꿨더니 세 묶음이 전부 **6 단계**에서
`KeyError: 'entries'` 로 죽었다 — 5 단계는 통과한 뒤였다 (명세 76/37/8 전수 일치 · 보존
41/21/8). 소비 자리는 셋이다: 5 단계 대조 · 6 단계 복사 뒤 재대조 · 사람이 그대로 치는 안내문.

**시험이 철자 하나만 보고 있었다.** `m.get("entries")` 는 막았는데 `m["entries"]` 는 안
막았다. "규칙이 두 벌이면 언젠가 갈린다" 고 적어 놓고 시험은 한 벌만 세고 있었던 셈이다.
이제 철자가 아니라 **접근 자리 전부**를 센다 (`entry_list(` 가 세 번 이상 나와야 한다).

주석에 그 철자를 적었다가 자기 시험에 또 걸렸다 — R15-b 에서 브랜치 이름으로 겪은 것과
같은 자리다. 이름을 옮겨 적지 않는 규칙은 주석에도 걸린다.

### 8-8. 회귀

`tests/test_r15_open_items.py` **21 passed**. 전체 **332 passed**.

전수 실행이 **이번 라운드와 무관한 빨강 둘**을 드러냈다. 둘 다 고쳤다.

| 무엇 | 왜 | 고침 |
|---|---|---|
| `test_review_request_clones_the_branch_that_owns_bms_balancing` | `CODEX_REVIEW_REQUEST.md` 가 흡수된 서브 브랜치를 clone 하라고 적고 있었다 — 2026-09-15 흡수 뒤 아무도 전수를 안 돌려서 안 드러났다 | 본진 브랜치 이름으로 정정 (정본은 루트 `CLAUDE.md` 하드룰 1) |
| `test_i6d_04_working_state_test_count_matches_the_collection` | 시험을 14 개 더해 `WORKING_STATE.md` 의 기대 개수가 낡았다 | 311 → 325 |

과학 값·산출 bytes 는 이번에도 건드리지 않았다.
