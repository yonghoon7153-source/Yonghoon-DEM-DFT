# 57차 작업 상태 (진행 중 — 파일이 정본이다)

56차 판정 **NO-GO**. 이 문서는 진행 좌표의 정본이다 — 재개할 때 `src/io.py`
나 `row_projection.py` 를 처음부터 다시 읽지 않아도 되도록 유지한다.

56차 verdict 가 못 박은 **종결이 아닌 수정 3종** (이 라운드의 판단 기준):

1. authority 경로 blacklist 를 더 늘리는 수정은 새로운 sink 하나를 남기므로
   종결이 아니다.
2. 문자열 철자 blacklist 증설은 불충분하다.
3. mountinfo 행 순서와 pathname depth 로 stacked top 을 추측하면 안 된다.

## 진행표

| # | 반례 | RED | 수정 | GREEN | 자리 |
|---|---|---|---|---|---|
| B | lifecycle 신뢰 경계가 어디에도 적히지 않았다 | — | ○ | ○ | `preserve.py` `_TRUST_BOUNDARY` · `STAGE3_CONTRACT.md` §13.3.4 |
| P0-1 | caller 가 지정한 attempt 경로가 authority 를 덮는 sink | ○ | ○ | ○ | `preserve.py` — 경로 인자를 **없앴다** (`attempt_path_for()` 유도) |
| P0-5 | 55차 형태 durable state 에 `attempt_verifier` 가 없다 | ○ | ○ | ○ | `preserve.py` `migrate_legacy_finalized_leg()` |
| P0-6/7 | producer closure 가 철자 blacklist 였다 · import-time 계산이 밖 | ○ | ○ | ○ | `row_projection.py` `_namespace_capabilities()` · `_import_time_heads()` |
| P0-2/3/4 · P1-4 | mount 정체를 행 순서·깊이로 **추측**했다 | ○ | ○ | ○ | `row_projection.py` `_kernel_mount_id()` · `_fs_identity()` · `_names_for()` |
| P1-2/P1-3 | 시험 환경 정화 + finalize 선형화 | — | — | — | 미착수 |

## P0-2/3/4 · P1-4 — 무엇을 어떻게 닫았는가

### 반례 (RED, 실측)

`tests/test_docs_lint.py::test_a_stacked_mount_is_identified_by_the_kernel_not_by_row_order`

무해한 bind 를 먼저 깔고 **같은 mountpoint 위에** 얼린 child 를 덮으면:

```
DID NOT RAISE SystemExit      ← _assert_writable(alias) 가 통과했다
```

56차의 `_deepest_mount_for()` 는 mountpoint **깊이**가 더 클 때만 교체한다
(`>`). 겹쳐 쌓인 두 mount 는 mountpoint 가 같아 깊이도 같으므로 mountinfo 에서
**먼저 나온 행**, 즉 **아래** mount 가 선택된다. 실제로 보이는 것은 위 mount 다.

### 수정 — 추측을 정교화하지 않고 **없앴다**

| 지운 것 | 이유 |
|---|---|
| `_deepest_mount_for()` | "가장 깊은 것을 고른다" 는 규칙 자체가 P0-2 로 무너졌다 |
| `_through_bind_mounts()` | 이름을 **되돌리는** 설계였고 세 라운드에서 세 번 틀렸다 (P0-5 escape · P0-6 깊이 · P0-7 root 좌표계) |

| 새 자리 | 무엇 |
|---|---|
| `_kernel_mount_id(path)` | 경로를 `O_PATH` 로 열고 `/proc/self/fdinfo/<fd>` 의 `mnt_id` 를 읽는다. 겹침·전파·순서는 커널이 이미 푼 문제다 |
| `_fs_identity(path)` | `(major:minor, 그 filesystem 안의 경로)` — 이름이 아니라 **대상**의 좌표. bind·겹침·symlink·개명에 불변 |
| `_names_for(dev, fs, table)` | 그 좌표를 보여 주는 **모든** 이름. 하나 고르지 않는다 — 각 후보를 커널에 되물어 확인하므로 덮어씌운 mount 로 가려진 이름은 떨어진다 |

`_assert_writable()` 은 이제 두 자리에서 묻는다 (심층 방어라 변이는 MULTI):

1. 원장·journal 이 아는 frozen 디렉터리와 **좌표로** 비교 (`ffs in fs.parents`)
2. 좌표의 조상마다 **모든 이름**으로 marker 순회 (원장 밖에서 얼린 tree)

목적지가 **아직 없을 수 있다** (새 cohort 디렉터리를 만들기 직전이 정상 용례).
그래서 존재하는 가장 깊은 조상에게 커널에 묻고 없는 나머지를 좌표 뒤에 붙인다 —
없는 이름 위에는 아무 것도 mount 되어 있지 않으므로 그 이어붙임에 추측이 없다.

### 회귀 (5건 전부 GREEN)

```
test_a_bind_mounted_alias_of_a_frozen_child_is_not_writable          (55차 P0-4)
test_a_frozen_alias_whose_path_has_a_space_is_not_writable           (56차 P0-5)
test_overlapping_binds_resolve_to_the_mount_the_kernel_reports       (56차 P0-6, 개명)
test_a_bind_from_a_separate_filesystem_is_resolved_by_the_mount_graph (56차 P0-7)
test_a_stacked_mount_is_identified_by_the_kernel_not_by_row_order    (57차 P0-2, 신규)
```

`test_the_deepest_mount_wins_when_binds_overlap` 은 이름이 **거짓이 됐으므로**
개명했다 (이제 가장 깊은 것을 고르지 않는다). 반례 자체는 회귀로 남긴다.

### 변이 등록부 재결속

| 이름 | 상태 |
|---|---|
| `deepest-mount-is-chosen` | → `mount-identity-comes-from-the-kernel` 로 대체 (지킬 규칙이 "깊이" 가 아니라 "커널에게 묻는다" 로 바뀌었다) |
| `mount-root-is-filesystem-relative` | `_fs_identity()` 의 `fs = Path(m["root"]) / rel` 로 재결속 |
| `destination-is-resolved-through-mounts` | 자리가 둘이 됐으므로 `MULTI` 의 `destination-is-compared-in-filesystem-coordinates` 로 이동 |
| `mountinfo-octal-escape-is-decoded` | 그대로 — `m["mp"]` 를 목적지에 맞출 때 여전히 load-bearing |

## 남은 부채 (마감 전 반드시)

### 죽은 변이 preimage (`--check-preimages` 실측)

57차의 앞선 수정들이 코드를 옮기면서 등록부 anchor 가 끊겼다. **재결속하거나
은퇴 사유를 적어야** 한다 — 끊긴 채로 두면 "전수 재생 성공" 이 거짓이 된다.

```
module-gate-before-side-effects        grid.py           preimage 0회
precheck-tells-new-from-resume         preserve.py       preimage 0회
finalize-requires-the-credential       preserve.py       preimage 0회
release-returns-the-plan               preserve.py       preimage 0회
closure-refuses-dynamic-resolution     row_projection.py preimage 0회
token-path-is-disjoint-from-authority  preserve.py       preimage 0회   ← P0-1 이 구조적으로 지운 검사
token-file-is-bound-to-its-leg         preserve.py       preimage 0회
attempt-path-is-exclusive              preserve.py       preimage 0회   ← 위와 같음
token-path-alias-is-refused            preserve.py       preimage 0회
ledger-hardlink-is-refused             preserve.py       preimage 2회   ← 중복 anchor (1회여야 한다)
```

### 그 밖

- P1-2 / P1-3 미착수 (환경 정화 + authoritative input manifest · finalize 선형화)
- g11 → g12 산출물 재생성 (~28분) · 12조각 전수 재생 + 합집합
- `--emit-expect` 로 바뀐 변이의 EXPECT 재생성
- 전체 시험 + strict smoke → push → `GATE57_REQUEST.md`
- e2e 2건은 컨테이너 커널 교체(fc-v22 → fc-v24)가 52차 P0-5 fail-closed cache
  검사를 건드린 것 — 이 라운드의 수정과 무관하다는 것을 요청문에 적는다
