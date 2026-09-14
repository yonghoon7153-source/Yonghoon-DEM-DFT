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
| 회귀 | `python3 -m pytest tests/ -q` → **284 passed** (리뷰 대상 시점 277) |
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
| `legacy_transition_approved` 판정 (리뷰어 §7-2) | 열림 — 게이트 계약 변경. 이번 이관은 이미 기록된 일회성 예외로 두고, 설계는 다음 라운드 |
| 기록용 CLI 의 output-root 인자 필수화 (리뷰어 §7-4) | 열림 — P2-1 은 닫혔으므로 급하지 않다. 호환성 판단 필요 |
| **U18-05** — 승격 묶음의 `git_commit` 혼재 | 열림. 리뷰어 권고대로 **기본은 단일 commit**. 이번 자료는 `0668665…`(9 개) + `419c1ab…`(4 개) 혼재이고 그 사이 `*.py`·`*.sh` diff 가 0 인 범위 한정 예외로 기록한다 — `.m`·설정·의존성까지 일반적으로 덮지 못한다는 지적을 받아들인다 |
| 조건 6(동적 인증) · 조건 8(다섯 축) | 열림 — 리뷰어도 새 발견으로 세지 않았다 |
| `openpyxl` 이 `ENV_KEYS` 에 없음 | 열림 — 별도 라운드 (P2-2 와 분리하라는 지적 그대로) |
| r11 `publish:profile_partial_stdout` 대체 증거 없음 | 열림 — `closed_with_substitutes: false` 로 그대로 |
| Octave 1~3 단계 · 동적 우회 재생 10 건 | 리뷰어 기계에서 미실행. 우리 쪽 277→284 전수 통과를 리뷰어의 재확인으로 쓰지 않는다 |

## 6. 우리가 고치지 않은 것 하나 — `R14_REQUEST.md`

요청문 §2 에도 같은 `--old-rev HEAD` 문맥 오류가 있다. **그 파일은 고치지 않는다** — 리뷰어가 sha256
`17995cfd…` 로 고정해 심사한 원본이고, 고치면 그 식별이 깨진다. 정정은 이 회신과 §1 P2-3 의 두 문서(현행
`R13_RESPONSE.md` · 증거 README)에 둔다. 다음 요청문부터 **승격 전/후 명령을 구분하고 기준을 full commit 으로**
적는다.
