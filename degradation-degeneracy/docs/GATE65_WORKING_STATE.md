# 65차 게이트 리뷰 작업 상태 (정본)

판정: **NO-GO (부분 수용)** — 2026-09-22 접수. "64차 접수 셋 전부 종결" 은 **불수용**, 기존
수정은 부분 수용. 리뷰어가 고정한 HEAD `5e4cf1038f0f26a6a624d9984386cfd046657ac3` · 과학
코드 정본 `743f65bead671bf353ce38027c2e8e457738ec08` · `source_digest e9ee7475dea7de1d`
(셋 다 일치, RUN_SCOPE diff 빈 출력). 새 **P1 3 · P2 1 = 4건** + E2-R 보류 1.

새 P0 없음. 접수 원장은 `docs/08_REVIEW_RESPONSE.md` §81, 대응은 §82. 리뷰 패키지 원본은
`docs/22p_gap/gate65_review/` (zip 바이트 그대로 + `codex/` 풀어 둔 것).

## 발견 원장

| ID | 무엇이 틀렸나 | 자리 | 상태 |
|---|---|---|---|
| G65-N1a (P1) | 부모가 user site 비활성이면 origin 을 보기도 전에 `usercustomize = <absent>`. 정상 `sitecustomize` 의 `import usercustomize` 는 평범한 import 인데 그 정상 영수증이 거부됐다 — "자동 import 안 함" 을 "로드 안 됨" 으로 바꿔 읽은 것 | `mutation_replay.py` `_parent_customization_view` → 판정은 `_assert_customization_matches_parent` | 코드 ✔ |
| G65-N1b (P1) | 부모가 상대 `PYTHONPATH` 를 **자기 cwd** 로 풀고 **자기 `sys.path`** 를 child 검색 경로로 씀. child 는 sandbox cwd 에서 뜬다. 보조 user-site 탐침도 cwd=ROOT | `_parent_customization_view` · `_parent_user_site_enabled` | 코드 ✔ (`_replay_context`) |
| G65-N2b (P1) | 표준 namespace package(`__file__ None`)를 `<absent>` 로 접고, 이력 검사가 "올렸다는데 `<absent>`" 를 모순으로 봐 **정상 customization 이 failed** | `_ENV_PROBE_BODY` cust · history 검사 | 코드 ✔ |
| G65-T1 (P2) | 활성 대조군이 활성을 **만들지 않는다** — 환경변수 하나 지우고 가정. 일반 venv 에서 시험이 자기 전제에서 죽음 | `tests/test_gate64_defensive.py` | 시험 ✔ (`tests/interpreter_fixture.py`) |
| E2-R 후속 (보류) | 실제 lifecycle 이 쓰는 token 탐침 `_kernel_lock_held(tok)` 은 True 쪽만 시험. 상수 True 로 바꿔도 커밋된 대조군 둘이 통과 | `tests/test_gate63_defensive.py` | 시험 ✔ |

**RED 관측** (`tests/test_gate65_defensive.py` 첫 실행, 수정 전): **10 failed · 7 passed**.
통과한 일곱은 대조군이다 (fixture 전제 실측 ×2 · 활성 바이트 대조 · 비활성+바이트 변경 거부 ·
비활성+미로드 · token 탐침의 같은-token 음성 · ZIP/읽기실패 축). 실패 열 중 하나
(`test_a_constant_true_token_probe…`)는 첫 판에서 `tmp_path/"a"` 를 안 만들어 이유가 틀린
빨강이었다 — 그 시험만 고쳐 제대로 빨개진 뒤 production 을 고쳤다.

**리뷰어 재현기를 이 Linux 에서 먼저 돌렸다** (`docs/22p_gap/gate65_review/codex/`):
`repro_imports.py` → `disabled_but_explicit_import` REJECTED (child `42bd17d9…` · parent
`<absent>`) · `relative_pythonpath` REJECTED (두 digest 다름) — **N1a·N1b 재현**.
`normal_namespace_package` 는 이 기계에서 ACCEPTED — Debian 의 `/usr/lib/python3.11/
sitecustomize.py`(0 바이트) 가 namespace 를 가리기 때문 (Python 은 정규 module 을 먼저 찾는다).
그래서 N2b 시험은 자유로운 이름 `usercustomize` + 활성 인터프리터로 만들었다.
`repro_e2_linux_NOT_RUN.py` (리뷰어가 Windows 에서 못 돌린 후속) → `same_token_baseline
[true, false]` · **상수 True token 탐침으로 바꿔도 커밋된 대조군 둘 PASS** — 리뷰어의 보류
사항이 이 기계에서 실측으로 확정됐다.

## 한 줄 요약

**세 상태를 가른다** (N1a: 비활성+미로드 · 비활성+정상 명시 로드 · 활성+자동 로드) ·
**재생 문맥은 하나다** (N1b: cwd·argv·env·정규화된 검색 경로) · **코드 없는 module 은
미로드도 읽기 실패도 아니다** (N2b) · **전제는 만들고 잰다** (T1) · **판정 함수는 하나만**
(E2-R). 넷 다 정상 입력에서 우리 층이 거부하거나 실패한 것이고 위조 성공이 아니다.

## 고침

### N1a — 조건 + 후보 + 이력, 셋으로 판정한다

`_parent_customization_view(ctx)` 는 이제 **후보**만 돌려준다 — 재생 검색 경로에서 resolver
가 찾는 것(hex16 · `<namespace>:hex16` · `<absent>`). 조건으로 `<absent>` 를 미리 넣지 않는다.
판정은 `_assert_customization_matches_parent(receipt, ctx)` 가 이름마다:

- child `<absent>` → 이력에 없어야 하고, 자동 import 대상(`sitecustomize` 항상 ·
  `usercustomize` 는 활성일 때)에 후보가 있으면 거부 (64차까지의 규칙 그대로)
- child hex16 → **후보와 같아야** 하고 이력이 올렸다고 해야 한다 — 비활성이어도 명시 import
  면 정상 (여기가 N1a)
- child namespace → 후보와 같아야 한다 (이력은 unfiled)
- 그 밖(`<built-in>`·`<frozen>`·모르는 값) → 대조할 바이트가 없다 → 거부

child 가 준 digest 를 정답으로 쓰지 않는다 — 후보와 같아야만 받고, **이력과 어긋나면
`<absent>` 도 받지 않는다** (세탁본 회귀: 명시 import 영수증의 usercustomize 를 `<absent>`
로 바꾸면 거부). 바이트 변경 거부 대조군 유지.

### N1b — `_replay_context(cwd)`

탐침·재생·부모 대조가 공유하는 **하나의 문맥**: 같은 실행 파일 · 같은 argv 모양(`-c`) ·
같은 env(`replay_env()`) · 같은 cwd(기본 `_sandboxed(ROOT)`) 로 인터프리터를 하나 띄워
`ENABLE_USER_SITE` · `sys.path` · `os.getcwd()` · `site.__file__` 을 받고, `sys.path` 를
child cwd 기준 절대 경로로 정규화한다 (`''` → cwd, 상대 → `join(cwd, p)`). 부모 프로세스의
`sys.path` 는 쓰지 않는다. `_parent_user_site_enabled()` 는 이 문맥의 한 필드로 남겼다.
신뢰 경계는 64차와 같다 — 보조 인터프리터도 같은 startup 코드를 실행한다; 부모가
독립적으로 믿는 것은 그 경로 위의 **바이트를 부모가 직접 읽은 값**이다 (docstring 에 명시).

### N2b — 상태 넷

child(`_ENV_PROBE_BODY`): 안 올라왔다 `<absent>` · 바이트 있다 hex16(파일·ZIP, `_hash_origin`)
· 코드 없다 `<namespace>:hex16` (`__file__ None` 이고 `submodule_search_locations` 있음) ·
origin 도 검색 위치도 없다 → `_Unreadable` → typed `failed` (startup 코드가 `sys.modules` 에
빈 ModuleType 을 심은 경우 — "origin 없는 module 은 전부 정상" 으로 넓히지 않는다).
namespace identity 는 **종류 + 검색 위치**(절대 경로 정규화 후 sha256[:16]) — 다른 자리의 빈
디렉터리는 다른 값. child 와 부모가 **같은 문자열**(`_NAMESPACE_IDENTITY_SRC`)을 실행한다.
schema: `customization.{sitecustomize,usercustomize}` 에 `_NAMESPACE_ID`·`_UNSUPPORTED_ORIGIN`
추가. 이력 검사의 "올렸다는데 `<absent>`" 는 그대로 — namespace 는 이제 `<absent>` 가 아니다.

### T1 — `tests/interpreter_fixture.py`

`python -m venv --without-pip [--system-site-packages]` 로 활성/비활성 인터프리터를 **만들고**,
그 인터프리터를 띄워 `ENABLE_USER_SITE` 를 **실측**한 뒤에야 시험이 돈다. 기대와 다르면
`pytest.skip` 에 기대값·실측값을 그대로 적는다 (미측정으로 보고 — 다른 환경으로 조용히
바꾸지 않는다). 64차의 활성 대조군은 이 fixture 위로 옮겼고 **활성 확인 assertion 은 지우지
않았다**. 비활성은 venv 판과 env 변수(`PYTHONNOUSERSITE=1`) 판 둘 다 남겼다.

### E2-R 후속 — 판정 함수 하나

`_flock_reports_held(fd)` 하나를 token 판(`_kernel_lock_held`)과 경로 판(`_kernel_lock_held_at`)
이 공유한다. 커밋된 대조군에 **같은 token · 같은 inode 에서** `LOCK_UN` → False → 다시 쥐면
True 를 넣었다. 새 회귀: token 탐침을 상수 True 로 바꾸면 대조군이 빨개진다 (AST 로도 token
판의 `is False` 존재를 고정).

### fixture 가 먼저 깨졌다 (규율 2)

`tests/receipt_fixture.py` 의 완전한 영수증은 이력이 customization 과 양립해야 한다 — 바이트를
낸 이름은 `startup_history.modules` 에 있어야 한다. 부모 판정이 이력을 보기 시작하자 fixture 가
먼저 깨졌고, 의도를 유지하며 채웠다. `test_gate64_defensive` 의
`want["usercustomize"] == "<absent>"` 는 틀린 등식("비활성 = absent")을 그대로 적은
assertion 이었다 — 판정 함수로 바꿨다.

## 변이 등록부 (65차)

g64 N1·N2 의 변이 지점이 코드 이동으로 사라져 **preimage 를 옮겼다** (N1: 판정 함수의
`auto = …` → `auto = True`; N2: 새 `elif f:` 분기의 `_hash_origin` → `_d(f)`). 새 축 5 (`-g65`):

```
explicit-import-is-an-ordinary-import-g65        MR    N1a  (hex 분기에 `or not auto` 를 되돌림)
search-path-comes-from-the-replay-context-g65    MR    N1b  (dirs ← 부모 sys.path)
namespace-is-loaded-code-free-not-absent-g65     MR    N2b  (namespace → <absent>)
the-fixture-measures-its-premise-g65             IF    T1   (실측 → 상수 True)
the-token-probe-negative-is-asserted-g65         G63T  E2-R (token is False → in (True, False))

--check-preimages   모든 변이 지점이 정확히 한 번 나타난다 (rc 0)
-k g64              3/3 물었다 (call 단계) · EXPECT 일치 · rc 0
-k g65              5/5 물었다 (call 단계) · EXPECT 일치 · rc 0
```

첫 재생에서 둘이 **안 물었다**: (i) g64 E2-R 축 — 경로 판 음성을 지워도 AST 대조군이 token 판의
`is False` 를 세어 통과했다 → 탐침별로 세게 고쳤다 (그래서 g65 token 축은 g64 AST 대조군도
같이 빨개진다 — 선언에 넣었다). (ii) T1 축 — 실측 함수를 상수 True 로 바꾸면 fixture 가 **skip**
해서 실패가 아니었다 → 변이를 "활성 조건(`--system-site-packages`)을 만들지 않는다" 로, 전제
시험을 검증 없는 `build_interpreter` 위로 옮겼다. 관측한 EXPECT 는 `--emit-expect` 출력을
그대로 이식했다 (증인 8건 전부 시험의 고정 문구, `Failed: DID NOT RAISE AssertionError` 포함).

```
(등록부 요약 끝)
```

## 이 라운드가 하지 않은 것

- **⑩ 등록부 격리** — 별도 계약. ★ 이번 라운드에 **현행범 관측**: 게이트 회귀가 도는 중
  `docs/22p_gap/_exec_class/` 에 `class: canonical` · `sealed: true` 기록 하나가 생겼다
  (`5a0c2090…a30.json`, `recorded_at 2026-09-22T05:52:29Z`, evidence `leg=L phase=grid
  class=canonical`). conftest 의 세션 말 정리가 지우지 않는다. **커밋하지 않고** 스크래치패드로
  옮겨 실행 전 상태로 되돌렸다 (tracked 366 = 디스크 366 확인). 기존 sealed 기록은 하나도
  건드리지 않았다. 상세는 `GATE66_REQUEST.md` §2-6. 권고 "둘 다": 임시 등록부 주입 + 운영 등록부 불변 확인
  · synthetic 을 canonical 권한으로 유입시키지 않기 · reader 가 읽는지·authority 를 주는지 같이
  고정 · 기존 기록은 append-only supersession). 기존 class/삭제 계약 변경은 별도 승인 대상 —
  이번 라운드에 손대지 않았다.
- **Q4 권고(`error_code`·검사 단계 구조화 매트릭스)** — 착수 안 함. 이번 증인 문구는 전부 시험의
  고정 문구로 두었다(production reason·digest·경로 없음).
- §0 의 독립 GO 전제(producer 결속 · trusted launcher · typed 보존 영수증 소비 · 독립 replay ·
  immutable bundle) — 그대로 신고. **본 실행 GO 는 별도이며 이번에 요청하지 않는다.**
- `source_digest` 는 `e9ee7475dea7de1d` 그대로다 — 이번 고침도 전부 RUN_SCOPE 밖.
