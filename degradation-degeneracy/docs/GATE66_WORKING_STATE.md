# 66차 게이트 리뷰 작업 상태 (정본)

판정: **NO-GO (부분 수용)** — 2026-09-22 접수. 리뷰어가 고정한 HEAD
`fa947cc9b17cdbeffbb39447c99159bc2c831e6e` · 직전 리뷰 `5e4cf1038f0f26a6a624d9984386cfd046657ac3`
· 과학 정본 `743f65bead671bf353ce38027c2e8e457738ec08` · `source_digest e9ee7475dea7de1d`
(우리 실측과 일치). 새 **P1 1 · P2 2 = 3건**.

새 P0 없음. 접수 원장은 `docs/08_REVIEW_RESPONSE.md` §83, 대응은 §84. 리뷰 패키지 원본은
`docs/22p_gap/gate66_review/` (zip 바이트 그대로 + `codex/` 풀어 둔 것, zip sha256
`aa2cde592d28c4cfd0654e1f968dc3ad66fca452388ded5acc4cc62978c0a0ec`).

## 발견 원장

| ID | 무엇이 틀렸나 | 자리 | 상태 |
|---|---|---|---|
| G66-N1 (P1) | **사후 resolver 후보 ≠ startup 이 올린 origin.** 부모가 startup 완료 뒤의 `sys.path` 에서 `find_spec` 를 다시 해 과거 import 를 판정한다. `-c` 의 `sys.path[0]=''` 는 본문 실행 직전에 붙으므로 startup 이 안 읽은 cwd 파일이 후보가 된다(A) · 정상 startup 이 자기 경로를 지우면 거부(B) · 다른 후보를 앞에 넣어도 거부(C). **한 원인, P1 하나** | `mutation_replay.py` `_replay_context` · `_parent_customization_view` | 코드 ✔ |
| G66-T1 (P2) | 전제 시험이 `make_interpreter()` 의 skip 을 우회하고, 생성·측정 subprocess 가 외부 env 를 물려받는다 → `PYTHONNOUSERSITE=1` 에서 skip 이 아니라 **실패** | `tests/interpreter_fixture.py` · `test_gate65_defensive.py` | 시험 ✔ |
| G66-R1 (P2) | 직전 리뷰 SHA → HEAD 에서 **기존 sealed 175건이 실제 삭제**됐는데 "무변경" 설명에 빠졌다 | `GATE66_REQUEST.md` §2-6 · `GATE65_WORKING_STATE.md` | **기록 ✔ · 복원은 승인 대기** |
| 정적 관측 | `ctx=None` 경로가 보조 인터프리터를 **두 번** 띄운다 ("한 번 측정한 하나의 문맥" 이라고 적어 놓고) | `_assert_customization_matches_parent` | 코드 ✔ |

**RED 관측**: `tests/test_gate66_defensive.py` 첫 실행 **5 failed · 7 passed** → 실제 기록은
**5 failed · 5 passed** (통과한 다섯은 대조군: 바이트 변경 거부 · 세탁 `<absent>` 거부 ·
origin 없는 ModuleType `failed` · 깨끗한 env 의 전제 시험 · 활성 옵션 제거 변이 검출).
수정 뒤 **10 passed**.

**리뷰어 재현기를 먼저 돌렸다** (`gate66_review/codex/repro_startup.py`, 수정 없이):

```
수정 전  plain              child df1b7ec0… parent df1b7ec0…  ACCEPTED
        cwd_on_pythonpath  child cb4c3880… parent cb4c3880…  ACCEPTED
        cwd_only_candidate child e3b0c442… parent cb4c3880…  REJECTED  ← N1 A
        remove_loaded_path child e4d83544… parent e3b0c442…  REJECTED  ← N1 B
수정 후  넷 다 parent = child · 전부 ACCEPTED
```

## 한 줄 요약

**찾을 수 있는 후보와 올렸던 origin 은 다른 자료다** (N1) · **전제는 만들고 재되 무엇을 못
만들었는지까지 갈라야 한다** (T1) · **"무변경" 은 시간 범위를 적어야 참이 된다** (R1).

## 고침

### N1 — 부모가 로드 시점의 origin 을 읽는다

`_replay_context()` 가 `sys.path` 뿐 아니라 **그 순간 올라와 있는 customization 의 origin**
(`{loaded, origin, locations}`)을 같이 잰다. `_parent_customization_view(ctx)` 는 `PathFinder`
탐색을 판정 근거로 쓰지 않고, **측정된 origin 의 바이트를 부모가 직접 읽는다**. 올라오지 않은
이름은 `<absent>` 이고 그것이 정상이다. 파일이 아닌 origin(zip)은 그 origin 을 담은 자리에서
loader 에게 묻되 **spec.origin 이 측정값과 같을 때만** 받는다.

신뢰 경계는 64차 선언 그대로 — 문맥 탐침도 같은 startup 코드를 도는 보조 인터프리터다. 부모가
독립적으로 믿는 것은 **자기가 읽은 바이트**이고, 그래서 실행 뒤 파일을 갈아 끼우면 여전히
거부된다. `search_path` 는 진단용으로만 남겼다.

### T1 — 통제 env 와 사유 분리

`interpreter_fixture.controlled_env()` 가 `PYTHONNOUSERSITE` 를 걷은 env 를 만들고 venv 생성·
측정이 그것을 쓴다. 통제 뒤에도 기대와 다르면 이 기계의 정책이므로 `pytest.skip` 사유에 실측값과
(있다면) 바깥 변수 이름을 적는다. **활성 옵션을 빼는 변이는 여전히 실패**한다 — "전부 skip" 으로
숨기지 않았다.

### R1 — 사실과 명부 (복원은 하지 않았다)

| 커밋 | 제목 | `_exec_class` |
|---|---|---|
| `01695bbe` (01:07) | "등록부가 회귀 1회마다 ~175 자란다 — ⑩ 으로 신고" | **211건 추가** (그 커밋의 다른 파일은 요청문 1개) |
| `d60f2539` (02:01) | "bms: Codex R17 NO-GO 대응 …" | 그중 **175건 삭제** — 제목과 무관하고 문서화 안 함 |

삭제분 175 전부 `sealed: true` · `canonical`, evidence 분포 `leg=L grid` 88 + `fixture` 87
(리뷰어 집계와 일치). `conftest` 정리는 **세션 시작 때 없던 파일만** 지우므로(`tests/conftest.py:180–188`)
원인이 아니다 — 원인은 우리 커밋이다. `GATE66_REQUEST.md` §2-6 의 "기존 sealed 기록은 하나도
건드리지 않았다" 는 **라운드 간 창에서 틀렸다**.

**복원하지 않았다.** 리뷰어가 자동 복원·class 변경을 승인하지 않았고 등록부 계약 변경은 별도
승인 대상이다. 삭제 전 바이트는 `5e4cf103` 트리에 그대로 있어 복원은 언제든 가능하다.

## 변이 등록부 (66차)

코드 이동으로 preimage 둘이 죽어 **자리를 옮겼다**:

| 축 | 옛 자리 | 새 자리 |
|---|---|---|
| `parent-customization-uses-the-path-finder-g63` | `spec = _PF.find_spec(n, dirs)` | `out[n] = _d(origin)` (부모가 바이트를 읽는 자리) |
| `search-path-comes-from-the-replay-context-g65` | `dirs = list(ctx["search_path"])` | `_replay_context` 의 `cwd=str(cwd)` (문맥을 **어느 cwd** 에서 재는가) · `-k` 도 상대 경로 두 시험으로 좁혔다 |

새 축 3 (`-g66`):

```
parent-compares-the-loaded-origin-g66      MR   G66-N1   (측정 origin → 사후 PathFinder 로 되돌림)
the-premise-uses-a-controlled-env-g66      IF   G66-T1   (controlled_env 에서 killswitch 제거를 뺌)
the-replay-context-is-measured-once-g66    MR   정적관측  (문맥을 두 번 재도록 되돌림)

--check-preimages   모든 변이 지점이 정확히 한 번 나타난다 (rc 0)
-k g63   8/8 물었다 · rc 0      -k g64   3/3 물었다 · rc 0
-k g65   5/5 물었다 · rc 0      -k g66   3/3 물었다 · rc 0
```

### 축이 "안 물었다" 로 나왔을 때 무엇을 했나

세 축이 처음에 안 물었고, **`-k` 를 넓히는 대신 성질이 어디로 옮겨갔는지 확인해 자리를 옮겼다.**

- `parent-customization-uses-the-path-finder-g63` · `search-path-comes-from-the-replay-context-g65`
  — 겨냥하던 코드가 N1 수정으로 사라졌다. 성질(부모가 정상 package 를 child 와 같게 본다 /
  문맥을 재생 cwd 에서 잰다)은 그대로이므로 새 자리로 옮겼고, g65 는 `-k` 도 상대 경로 두
  시험으로 좁혔다 (`the_parents_sys_path_is_not_the_childs_search_path` 는 이제 cwd 를 바꿔도
  안 빨개진다 — 그 성질을 origin 대조가 대신 지키기 때문이다).
- `usercustomize-follows-the-startup-activation-g64` — `auto` 가 지키던 "비활성+미로드" 는 이제
  **측정된 `loaded`** 가 더 강하게 지킨다. 그 분기에 **남은 역할**은 *이력에 파일로 안 잡히는*
  경우(표준 namespace)의 세탁 거부인데 **그것을 덮는 대조군이 없었다** — 그래서
  `test_g66_05b_a_forged_absent_namespace_is_still_rejected` 를 새로 만들고 축을 거기로
  겨냥했다 (변이 뒤 증인 `Failed: DID NOT RAISE _ReplayError`).

⚠ 등록부를 고치는 **도중에 돌던 확인 재생은 버렸다** — 재생은 그때의 파일을 sandbox 로 복사하므로
중간에 바뀌면 결과가 무효다 (64차 "회귀 도중 HEAD 이동" 과 같은 부류).

## 이 라운드가 하지 않은 것

- **⑩ 등록부 격리** — 별도 계약, 미착수. R1 의 삭제본 복원도 **승인 전에는 하지 않는다**.
- **Q6 F50b** — 리뷰어 권고대로 **(b) 다음 RUN_SCOPE 변경에 묶고, 그때까지 "같은 commit 에서
  resume" 을 운영 제약으로 명시**한다. 리뷰어가 덧붙인 구분(`실행중_코드불변` = 한 attempt 안,
  `start_파일_일치` = attempt 사이)을 받아, 고칠 때 doc-only resume 허용 여부를 계약으로 정하고
  source/input/env/recipe 변경 거부와 doc-only 대조를 **각각** 회귀로 고정한다.
- **Linux native 커널 검증** — 리뷰어 환경에서 미실행. 우리 쪽 출력을 다음 요청문에 싣는다.
- `source_digest` 는 `e9ee7475dea7de1d` 그대로 — 이번 고침도 전부 RUN_SCOPE 밖.
**본 실행 GO 는 요청하지 않는다.**

---

> **정정 (67차, 2026-09-22)** — 위 §고침 N1 의 제목 *"부모가 로드 시점의 origin 을 읽는다"* 는
> **과한 주장이었다.** 탐침이 주는 것은 startup 이 끝난 뒤 `sys.modules` 의
> `__file__`/`__spec__.origin` 이고, Python 은 그 둘의 자동 동기화를 보장하지 않으며 런타임
> 수정도 가능하다 (67차 리뷰어 Q1). 참인 문장은 **"부모가 *관측된* origin 의 바이트를
> 읽는다"** 다. *로드 순간의 봉인된 출처*는 trusted launcher / immutable input bundle 이
> 필요하고 **미착수**다. 코드 주석도 같이 고쳤다 (`mutation_replay.py`).
> 그리고 이 문서의 §고침 N1 이 말한 보호에는 **구멍이 있었다** — 67차 G67-N1: `auto` 가
> 부재 위조의 마지막 방어였고 user site OFF + 명시 import namespace 조합을 빠져나갔다.
> 자세한 것은 `docs/GATE67_WORKING_STATE.md`.
