# 57차 게이트 리뷰 요청 — 묶음 9 (실행 전 승인 · 보존 lifecycle)

**대상 커밋**: `47a2763e` (브랜치 `claude/14-gate-code-review-9qkx05`) — 코드·시험·산출물(g12)·변이 전수 증거를 전부 담은 커밋이다. 그 뒤 커밋은 이 요청문과 `webapp/`(위키 열람기) 뿐이고 `degradation-degeneracy/` 를 건드리지 않는다.
**직전 판정**: 56차 **NO-GO** — P0 7건 · P1 4건

---

## §0 먼저 — 이번 라운드가 **하지 않은** 것

| 조건 | 상태 |
|---|---|
| **P0-1** producer 결속 — 닫힌 typed manifest 파싱 · 두 payload 압축해제 재해시 · producer 발행 영수증 | **미착수** (49차부터 **아홉 라운드째**) |
| **P0-8** 경로 무관 typed·sealed 실행 class marker | **미착수** |
| trusted launcher 의 source 측정 | **미착수** |
| **P0-4** typed 보존 영수증 **소비** | **부분** |
| 변이 증거의 **독립 replay** | **미착수** — 57차는 checker 가 영수증을 소비하게 했을 뿐(P1-1), 스스로 재생하지는 않는다 |
| baseline·sweep1d·wsweep 계획 gate · 실물 object-lock adapter · power-loss 모델 · publisher 전용 OS principal · 외적타당도 #48/#49/#50 | **미착수** |

55·56차 판정문의 마지막 문단에 동의한다 — 위 항목들은 반례와 **별개의 독립 GO
전제**로 그대로 남는다.

### 이번 라운드가 스스로 신고하는 것 셋

**① 57차 리뷰어 원문이 이 저장소에 없다.** `docs/22p_gap/` 에는
`GATE56_REQUEST.md` 까지만 있다. 판정의 개수(P0 7 · P1 4)와 P0-1·P0-2/3/4·
P0-5·P0-6/7·P1-1 의 내용은 커밋 시점에 원문을 보고 적었지만, **P1-2 와 P1-3
은 56차 요청문의 §3-6 과 §3-3 에서 재구성한 것**이다. 두 반례는 실제로
재현했고 그 출력을 아래 §1 에 적었다. 다만 **리뷰어가 P1-2 / P1-3 으로 적은
것과 같은 발견인지는 원문 대조가 필요하다.** 다르면 그 둘은 아직 열려 있는
것으로 취급해 주기 바란다.

**② 전체 회귀가 초록이 아니다** — `tests/test_lifecycle_e2e.py` 2건이 빨갛다.
원인은 이 라운드의 수정이 아니라 **컨테이너 커널 교체**다 (§2-1).

**③ 남아 있는 표면** (56차 신고분 + 이번에 확인한 것):

- 원장·journal·anchor·`.FROZEN` 전부에 쓸 수 있는 주체는 역사를 다시 쓸 수 있다.
  이것은 계약 §13.3.4 로 **명문화**했다 (B) — 없앤 것이 아니라 적은 것이다.
- 소유 증명 token(0600)은 같은 uid 의 다른 process 가 읽는다.
- 변이 증거의 **pytest report 자체를 손으로 위조**하면 checker 를 통과한다.
- lock 은 여전히 같은 파일시스템의 `flock` 이다.
- mount 판정은 이제 커널에 묻지만, `/proc/self/fdinfo` 와 `/proc/self/mountinfo`
  를 읽을 수 있는 Linux 를 전제한다. 못 읽으면 거부한다(fail-closed).
- `migrate_legacy_finalized_leg()` 가 인증에 쓰는 근거는 **원장 봉인보다 약하다**
  (디스크의 소유 증명 파일). 그래서 `evidence.verifier_origin` 을 남긴다 — 숨기지
  않지만 약한 것은 사실이다.

---

## §1 56차 반례 11건 — 전부 재현한 뒤 고쳤다

| # | 56차 반례 | 재현 | 고친 자리 |
|---|---|---|---|
| B | lifecycle 경로의 신뢰 경계가 **어디에도 적혀 있지 않다** (자체 발견) | — | `preserve.py` `_TRUST_BOUNDARY` · 계약 §13.3.4 — 무엇을 전제로 빼고 무엇을 결함으로 남기는지 표로 |
| P1-1 | 실행 영수증을 **쓰기만 하고 안 읽는다** — 12조각에서 `binding.execution`·`execution_digest` 를 전부 지워도 rc 0 | ○ | `mutation_replay.py` `_assert_execution_is_current()` 를 `check_coverage()` 가 부른다 (있는가 · 본문이 그 digest 로 해시되는가 · 지금 환경과 같은가) |
| P0-1 | caller 가 지정한 attempt 경로가 authority 를 덮는 sink | ○ | **경로 인자를 없앴다** — `attempts_root_for_ledger()` · `attempt_path_for()` 가 자리를 유도하고, 공개 API 5개에서 `token_file` 을 제거 |
| P0-2 | 겹쳐 쌓인 mount 에서 **아래** 것이 뽑힌다 (`DID NOT RAISE SystemExit`) | ○ | `_deepest_mount_for()` 를 **지웠다** · `_kernel_mount_id()` 가 `/proc/self/fdinfo/<fd>` 의 `mnt_id` 를 읽는다 |
| P0-3 | 같은 모델의 다른 얼굴 — 이름을 되돌리는 설계 | ○ | `_through_bind_mounts()` 를 **지웠다** · `_fs_identity()` 가 `(major:minor, filesystem 안의 경로)` 좌표로 비교 |
| P0-4 | 같은 모델의 세 번째 얼굴 — 목적지가 아직 없을 때 | ○ | 존재하는 가장 깊은 조상을 커널에 묻고 없는 꼬리를 좌표 뒤에 잇는다 (없는 이름 위에는 아무것도 mount 되어 있지 않다) |
| P0-5 | 56차 이전 durable state 에 `attempt_verifier` 가 없어 **닫을 수도 되돌릴 수도 없는 다리**가 된다 | ○ | `_already_finalized()` 가 그 모양을 알아보고 **말한다** · `migrate_legacy_finalized_leg()` 를 사람이 한 번 명시적으로 부른다 (인증은 면제하지 않는다) |
| P0-6 | `MODULE_EFFECTS` 가 import 시 **실행되는** 노드 5종을 안 덮는다 (대입 우변·데코레이터·기본 인자·class base·class body) — 전부 digest 를 안 움직였다 | ○ | 그 노드들을 `MODULE_EFFECTS` 에 묶고 class body 는 `_visit` 로 훑는다 (`_import_time_heads()`) |
| P0-7 | namespace guard 가 호출 대상의 **철자**를 본다 — 우회 4종이 전부 통과 (`GET = getattr` · 별칭의 별칭 · `operator.attrgetter` · `sys.modules[__name__]`) | ○ | `_namespace_capabilities()` — module-level 별칭을 **고정점까지** 따라간다 · `attrgetter` 는 닫힘 안에서 거부 · `sys.modules[...]` 는 Subscript 규칙 |
| P1-2 | 재생이 pytest 에 환경을 지정하지 않아 **부모 환경이 통째로** 샌다 (재구성 — §0-①) | ○ | `replay_env()` — 필요한 것과 선언한 것만 남기고 지운다 · `PYTHONHASHSEED=0` · 영수증의 `env` 가 "중요한 목록" 에서 "**전부였다**" 는 사실로 |
| P1-3 | 멱등성 물음이 임계 구역 **밖**이라 동시 finalize 하나가 `FileNotFoundError` 로 떨어진다 (재구성 — §0-①) | ○ | `_already_finalized()`·`resume_claim()` 을 `_lifecycle_locks()` **안**으로. 락 앞의 중복 분기는 없앴다 |
| P1-4 | 그 좌표를 보여 주는 이름 중 **하나를 골랐다** | ○ | `_names_for()` — 모든 이름을 돌려주고 각 후보를 커널에 되물어 확인한다 (가려진 이름은 거기서 떨어진다) |

### 이번 라운드의 형태 하나 — 56차 verdict 가 못 박은 **종결이 아닌 수정 3종**

56차 판정은 고칠 자리만이 아니라 **고치는 방식**을 거절했다:

1. authority 경로 blacklist 를 더 늘리는 수정은 새 sink 하나를 남기므로 종결이 아니다.
2. 문자열 철자 blacklist 증설은 불충분하다.
3. mountinfo 행 순서와 pathname depth 로 stacked top 을 추측하면 안 된다.

셋 다 **검사를 정교하게 만드는 대신 물음 자체를 바꿔서** 닫았다.

| 반례 | 51~56차가 하던 것 | 57차가 한 것 |
|---|---|---|
| P0-1 | 금지할 경로를 하나씩 추가 (원장·claim·남의 token·symlink·hardlink) | **caller 의 pathname 이 sink 에 닿지 않게** — 인자를 없앴다 |
| P0-6/7 | 금지할 이름을 하나씩 추가 (`getattr`·`__import__`·…) | 이름이 아니라 **capability 를 따라간다** (별칭의 고정점) |
| P0-2/3/4 | 행 순서 → 깊이 → root 좌표계, 세 라운드에 세 번 | **커널에게 묻는다** (`mnt_id`) — 겹침·전파·순서는 커널이 이미 푼 문제다 |
| P1-2 | `BOUND_ENV` 목록을 늘린다 | 환경을 **강제**한다 — 목록 밖 변수는 증거를 안 움직이는 게 아니라 run 에 **닿지 못한다** |
| P1-3 | (해당 없음 — 새 발견) | 술어와 행위를 같은 임계 구역에 (`_lifecycle_locks()` 자신의 규칙을 멱등성 물음에도) |

**"수정이 도달 불가 코드를 만들면 그 코드를 지운다."** P0-1 이 경로 인자를
없애자 `token-path-is-disjoint-from-authority` 와 `attempt-path-is-exclusive`
두 검사가 preimage 0회가 됐다 — 막던 것이 존재할 수 없게 됐기 때문이다.
남겨 두면 "전수 재생 성공" 이 거짓이 되므로 은퇴시켰다 (§2-3).

---

## §2 증거

### 2-1 전체 회귀 — **1427 passed · 1 xfailed · 2 failed** (467.91s)

빨간 2건은 둘 다 `tests/test_lifecycle_e2e.py` 이고 **같은 원인**이다:

```
RuntimeError: 승인한 완방상태 캐시가 이 실행과 다른 runtime 로 계산됐습니다
  ({… 'platform': 'Linux-6.18.44-fc-v22-x86_64-with-glibc2.39' …}
 ≠ {… 'platform': 'Linux-6.18.44-fc-v24-x86_64-with-glibc2.39' …}).
  승인이 이 바이트를 가리키므로 재계산으로 넘어갈 수 없습니다 (52차 P0-5).
```

두 runtime dict 는 **`platform` 한 필드만 다르다** (python·pybamm·
pybammsolvers·casadi·scipy·numpy 전부 동일). 실행 컨테이너의 커널이
`fc-v22` → `fc-v24` 로 바뀌었고, 52차 P0-5 의 fail-closed 캐시 검사가 그것을
물었다. **이 라운드의 수정과 무관하며, 오히려 그 검사가 설계대로 문 것이다.**
승인 digest 가 그 바이트를 가리키므로 조용한 재계산은 금지다 — 캐시를 다시
만들고 계획의 `discharged_cache_sha256` 을 갱신하는 것은 승인 절차 안에서 할
일이라 이 라운드에서 하지 않았다.

라운드 진행 중 실패 추이 (전부 실측): 9 → 7 → 5 → 3 → **2**.

### 2-2 strict smoke — **rc 0 · 52 ✅ · 0 ❌**

strict 였음을 같이 실측했다 (`git_info(".")["git_dirty"] = False`) — 즉
`SMOKE_DIRTY` 가 서지 않아 `clean_worktree` 와 `코드_identity` 를 **건너뛰지
않았다**. 범위 밖(`git_dirty_out_of_scope`)으로 빠진 것은 `mode-observability/`
의 README 둘이고 RUN_SCOPE 가 아니다.

### 2-3 변이 전수 — 등록부 **170 scenario** (executable 161 · declared 9)

176 → 170. 이 라운드가 코드를 옮기면서 **끊긴 anchor 14개**를 `--check-preimages`
가 먼저 잡았고, 재결속 8 · 은퇴 6 으로 처리했다.

| 처리 | 예 | 사유 |
|---|---|---|
| 재결속 | `mount-root-is-filesystem-relative` | 자리가 `_fs_identity()` 의 `fs = Path(m["root"]) / rel` 로 옮겨갔을 뿐 규칙은 살아 있다 |
| 개명 | `deepest-mount-is-chosen` → `mount-identity-comes-from-the-kernel` | 지킬 규칙이 "깊이" 에서 "커널에게 묻는다" 로 **바뀌었다** |
| MULTI 승격 | `destination-is-compared-in-filesystem-coordinates` (2-site) | `_assert_writable()` 이 두 자리에서 묻는 심층 방어라 한 자리만 꺼도 다른 쪽이 잡는다 |
| 은퇴 | `token-path-is-disjoint-from-authority` · `attempt-path-is-exclusive` | P0-1 이 **구조적으로 지운** 검사 — 막던 것이 존재할 수 없다 |
| 은퇴 | `finalize-requires-the-credential` | anchor 를 잘못 잡았다 (그 자리의 guard 시험은 항상 `token=` 을 명시로 넘겨 안 문다). 회귀는 `resume-compares-the-verifier` 의 selector 로 옮겼다 |

12조각을 **HEAD 를 고정한 채** 끝까지 돌렸고 조각별 문제는 0건이다.

```
모든 변이 지점이 정확히 한 번 나타난다
등록부 scenario 170 (executable 161 · declared 9) · 조각 12개에서 관측 170
조각 합집합이 등록부 전체를 정확히 덮었다
```

**정본은 커밋된 증거 파일이다** — `docs/22p_gap/mutation_coverage/s1..s12.json`
과 그 옆의 `reports/`.

### 2-4 증거 층이 잡은 것 넷

**① 새 시험이 처음부터 초록이면 fixture 가 진실을 가린 것이다.**
`mountinfo-octal-escape-is-decoded` 변이가 안 물길래 손으로 적용해 보니
`1 passed`. 원인은 코드가 아니라 **시험**이었다 — 거부 메시지에 `"frozen"` 이
들어 있는지를 부분문자열로 봤는데, pytest 의 `tmp_path` 이름이 시험 함수
이름에서 나오므로(`…/test_a_frozen_alias_whose_path_ha0/…`) 경로가 오류
문자열에 실리기만 하면 **어떤 이유로 거부해도** 통과했다.
`_assert_refused_as_frozen()` 을 두고 거부의 **이유**를 묻게 바꿨다.

**② 시험이 vacuous 해진 것을 변이가 알려 줬다.** `token-path-alias-is-refused`
가 안 물었다. P0-1 이 caller 경로를 없앤 뒤 그 시험은 아무도 안 보는 symlink
하나를 심어 놓고 `assert before == after` 를 하고 있었다 — 통과해도 아무 뜻이
없다. `attempt_path_for("L")` **자리에** symlink 를 심도록 다시 썼고, 증인은
`OSError: [Errno 40] Too many levels of symbolic links` 가 됐다.

**③ 등록부를 스크립트로 고치면 옆칸이 다친다.** 은퇴 처리 스크립트가 인접
항목(`release-cleanup-holds-the-attempt-path`)의 kexpr 꼬리를 잘라 먹었다.
커밋 전에 MUTANTS/MULTI/EXPECT 전체를 HEAD 와 diff 해서 잡았고
`git show HEAD:` 로 복구했다. **등록부 편집은 diff 로 검산한다**가 이 라운드의
교훈이다.

**④ P1-2 의 환경 결속이 실제로 문다 — 이 요청문을 쓰다가 실측했다.**
위키 열람기 폰트를 만들려고 `pip install brotli` 를 했더니 곧바로:

```
✗ …/s1.json: 증거가 가리키는 실행 환경이 지금과 다르다
   (다른 항목: ['packages']) — 그 환경에서 다시 재생해야 한다
```

`pip uninstall brotli` 로 되돌리자 합집합 증명이 다시 통과했다. 손으로 적은
목록이었으면 이 설치는 **증거를 전혀 움직이지 않았을 것**이다.

### 2-5 산출물 — g11 을 얼리고 g12 로

계약 §13.3.2 는 pin 을 cohort lifetime 동안 고정으로 둔다. 이 라운드가
`preserve.py`·`row_projection.py` 를 고쳐 identity 가 움직였으므로 g10 → g11
과 같은 형태다.

| 값 | 56차 (g11) | 57차 (g12) |
|---|---|---|
| `compute_sha256` | `872ca5b9046ca703` | `044a87204bfca078` |
| `producer_semantic_sha256` | `eb4555abd9490dd0` | `ad36d111337abd39` |
| `row_projection_py_sha256` | `b9d895261c7a9df1` | `ad1349257095cbd1` |
| `src_scoring_py_sha256` | `69e69cb046f4b4ae` | 같음 |
| 영수증 core_sha | `79ed20cd3fd34034…` | `8609f0074ac43197…` |
| validator identity | `9c7e5e71cbef8f05` | `ea35ff4f39b97489` |
| 투영 | `proj_g11` | `proj_g12` |

**행 바이트는 안 움직였다** — 재생성 출력이 `proj ad598fe77e75afec` 로
g4~g11 과 동일하다. 이 라운드의 변경은 신뢰 경계 선언 · 경로 유도 · capability
닫힘 · mount 좌표 · 환경 정화 · 임계 구역이고 **계산식이 아니다.** 움직인 것은
identity 의 **정의**다. cross-cohort 비교는 여전히 금지다 — 같은 바이트라는
사실은 회귀가 확인하는 것이지 인용의 근거가 아니다.

---

## §3 무엇을 반증해 주기 바라는가

우선순위 순. **§0 에 신고한 것을 다시 적는 것은 이미 아는 사실의 재확인이다.**

1. **커널 mount ID 를 믿는 것의 남은 축.** `_kernel_mount_id()` 는
   `O_PATH` 로 연 fd 의 `mnt_id` 를 읽는다 — 그 값이 우리가 묻는 질문에
   **답이 아닌** 구성이 있는가. mount namespace 가 분리된 자식, `/proc` 이
   다른 namespace 의 것으로 mount 된 경우, `mnt_id` 재사용(unmount 후 같은
   ID 재할당), `fdinfo` 에 `mnt_id` 가 없는 커널. 그리고 `_fs_identity()` 가
   목적지가 없을 때 **꼬리를 잇는** 자리 — 그 사이에 mount 가 생기는 TOCTOU.
2. **`_names_for()` 가 이름을 다 못 찾는 구성.** 좌표를 보여 주는 창이
   mountinfo 에 안 나타나는 경우(다른 namespace, `--rbind` 하위, overlayfs 의
   lower/upper). 못 찾으면 marker 순회가 조용히 짧아지는가, 거부하는가.
3. **경로를 없앤 뒤 남은 alias.** caller 는 이제 `leg_id` 만 준다.
   `check_id()` 의 도메인 안에서 두 leg 가 **같은 파일**로 유도되는 입력이
   있는가 (유니코드 정규화, 대소문자 무시 파일시스템, 길이 절단).
   `attempts_root_for_ledger()` 자체를 bind mount 로 덮으면?
4. **capability 고정점의 남은 계보.** `_namespace_capabilities()` 는
   module-level 별칭을 따라간다 — 함수 안 지역 별칭, class attribute,
   dict/list 에 담아 꺼내기, `functools.partial`, decorator 가 돌려주는 것.
   반대로 **너무 넓어** producer 자신의 정상 코드를 막는 자리.
5. **`migrate_legacy_finalized_leg()`.** 사람이 부르는 한 번의 창.
   그 검사(계획 executed · 실행 기록 있음 · claim 없음 · verifier 없음)를
   만족시키면서 **남의 다리**를 넘길 수 있는가. `verifier_origin` 이 붙은
   기록이 나중에 정상 기록과 구분되지 않는 경로.
6. **임계 구역 안으로 옮긴 뒤의 순서.** `_already_finalized()` 가 lock 안에
   있다 — `LOCK_ORDER = (attempt_path, claim, ledger)` 를 지키면서 deadlock
   이나 lock 승격이 생기는 조합. `resume_claim()` 이 lock 을 안 잡는 순수
   읽기라는 주장이 틀리는 자리.
7. **강제한 환경의 구멍.** `replay_env()` 가 지우지 못하는 것 — 상속되는
   fd, cwd, umask, resource limit, locale 을 결정하는 다른 경로, `PATH` 로
   들어오는 실행 파일의 내용. 목록이 "전부였다" 는 주장이 어디서 깨지는가.
8. **증거를 소비한다는 주장.** `_assert_execution_is_current()` 가 셋을
   본다 — 두 필드가 있는가 · 본문이 그 digest 로 해시되는가 · 지금 환경과
   같은가. 셋을 다 만족시키면서 **다른 실행**의 증거를 제출할 수 있는가.

---

## §4 검증 명령

```
python -m pytest tests/ -q
./scripts/smoke_e2e.sh
python3 docs/22p_gap/mutation_replay.py --check-preimages
python3 docs/22p_gap/mutation_replay.py --slice I/12 --emit-coverage docs/22p_gap/mutation_coverage/sI.json
python3 docs/22p_gap/mutation_replay.py --check-coverage docs/22p_gap/mutation_coverage/s*.json
python -m pytest tests/test_lifecycle_e2e.py -q
```

원자료(`results/`)는 gitignored 이므로 clean checkout 에서는 artifact 대조가
계산 불가로 실패할 수 있다. 지원 인터프리터가 하나뿐이면 정규형 회귀 2건이
`len(seen) >= 2` 로 실패한다. mount 회귀 다섯은 bind mount 를 만들 수 없는
환경에서 skip 한다. lifecycle E2E 는 `tqdm` 이 필요하다
(`pip install -r requirements.txt` 를 먼저 부탁한다).

**`--check-coverage` 는 이제 실행 환경까지 본다** (P1-2). 검토 환경의 설치
패키지가 다르면 조각을 그 환경에서 다시 재생해야 한다 — 그것이 결함이 아니라
이번에 고친 것이다.
