# 적대적 리뷰 요청 — 14차 · α·β 검증 하네스 (`bms-balancing/`)

읽는 쪽은 LLM 리뷰어다. 밀도 우선, 완충 문장 없음. **요청문은 증거가 아니다** — 아래 명령을 재실행해 검증하는 것을
전제로 쓴다. 우리 환경에서만 되는 것은 그렇게 밝힌다.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | `1bb45b358db4850c73e185d5f851e35fbcff9ad6` (2026-09-14T06:32:39Z) |
| 브랜치 | `claude/bms-alpha-beta-verify` (경로 소유: `bms-balancing/` **만**) |
| 직전 라운드 | R13 (대상 `94add7b`) — 발견 9 + §5 Q6, 회신 `reviews/R13_RESPONSE.md` |
| 이 라운드의 범위 | R13 **GO 조건 7**(실데이터 재실행)을 닫는 과정과 그것이 드러낸 발견 **4 건** |
| 트리 | `git status --porcelain` → **0 줄** (실측) |

R13 회신 시점(`ef8e8f6`) 이후 이 브랜치의 커밋 26 개 중 이 요청의 대상은 8 개다:
`3e4f060`(U18-01) · `0668665`(U18-02·03) · `c005343`(회신 §8) · `37a889b`(U18b 승격) · `df6413d`(U18-04) ·
`1bb45b3`(증거 재생성·회신 확정). 나머지는 COMSOL 트랙 문서·보존(§8 에서 범위를 따로 적는다).

## 1. 검증 — 방금 실행 (`1bb45b3`, clean 트리)

```
$ PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider
277 passed in 473.86s (0:07:53)                      # rc 0

$ python3 scripts/check_u14.py --new out --schema-only            # 현행 정본
rc 0 · blocked_by {schema 0, provenance_cols 0, content 0, unit 0, controls 0, env 0, numbers 0,
                   alias 0, provenance 0, inputs 0, inputs_uncomparable 0, env_uncomparable 0,
                   stale 0, baseline_absent 1}

$ python3 scripts/check_u14.py --new out/archive/legacy_r6_u14 --schema-only   # 얼린 옛 정본
rc 2 · blocked_by {schema 40, provenance_cols 25, content 6, provenance 1, baseline_absent 1, 나머지 0}
```

증거 묶음 `reviews/r13_repros/replay_ours_after_fixes/` 는 `df6413d` 에서 재생성했다. `df6413d..1bb45b3` 의
`git diff --name-only -- '*.py' '*.sh'` 는 **0 개**(문서·증거만) — 그래서 이 요청의 코드 identity 는 증거의 것과 같다.

| 파일 | 결과 (전부 `target_head df6413d6…` · `evidence_eligible`·`instrument_sealed`·`package_digest_ok` true) |
|---|---|
| `replay_codex_r7.json` | 5/6 · 제외 1 · closed **false** · with_substitutes true |
| `replay_codex_r9.json` | 12/12 · closed **true** |
| `replay_codex_r10.json` | 20/22 · 제외 2 · closed **false** · with_substitutes true |
| `replay_codex_r11.json` | 32/37 · 제외 5 · closed **false** · with_substitutes **false** (`publish:profile_partial_stdout` 대체 없음) |
| `replay_codex_r6_adapted.json` | `"mode": "full"` 6/6 (`R6_OLD_OUT = git archive bfc4623^ out`, 26 파일) |
| `codex_r6_mutation_audit.txt` · `mutation_adapted.txt` | 8/8 · 5/5 CAUGHT, MISSED 0 |
| `matlab_smoke.txt` | Octave 전 단계 전부 통과 (rc 0) |

**leaf 별 판정은 `ef8e8f6` 판과 동일하다.** 이 라운드의 코드 변경도 승격도 러너 결과를 움직이지 않았다.

## 2. 조건 7 을 닫은 경로 — 실데이터 2 회 + 승격

R13 조건 7: "기존 provenance-incomplete `out/` 는 보존하고 **별도 출력에 실제 재실행**". 합성 완주는 `test_g25` 로
닫혀 있었고, 실데이터는 원자료가 있는 사용자 기계에서 돌았다 (우리 컨테이너에는 원자료가 없다 — 아래 숫자 중
`STATES` 실행은 **그 기계의 출력**이고, 승격 후 검증은 이 컨테이너에서 **다시** 돌린 것이다).

| 회차 | 무엇 | 결과 |
|---|---|---|
| U18 (1 차) | `OUT=out_u18 STATES='100 200 300_0009 300_0147' STARTS=24` | 13/13 게시 · `--old out` 이 `numbers 0` · **승격 안 함** (아래 U18-01·02·03) |
| U18b (2 차) | 같은 설정, 고친 wrapper·checker, 깨끗한 트리 | rc **4** · `numbers 0` · 명부 13/13/13 · 계약 축 전부 0 · `inputs_uncomparable 17` · `env_uncomparable 1` **만** |
| 승격 `37a889b` | 옛 정본 26 파일 → `out/archive/legacy_r6_u14/` (얼림), 새 묶음이 `out/` | 승격 후 `--schema-only` 가 **사용자 기계와 이 컨테이너(fresh clone) 둘 다 rc 0** |

부수 확인: `--old-rev HEAD` rc 4 · 13/13 · `numbers 0` (3 단계와 같은 판정) · `compare_states.py out` 이 degeneracy
4/4 사용·제외 0·"A 축에서 LLI 가 항상 가장 좁은가: 예"·묶음 불일치 경고 없음.

**숫자는 이 라운드 내내 한 번도 안 움직였다.** 바뀐 것은 게시·서명 계약뿐이다.

## 3. 발견별 대응 — 이 라운드가 스스로 찾은 4 건

| # | 실측 반례 | 원인 (`파일:자리`) | 수정 | 회귀 |
|---|---|---|---|---|
| **U18-01** | 13 산출 중 shape 가 `ne_shape_step_005C_Li.csv` 로 게시됨 (정본 이름은 `ne_shape_GITT_Li.csv`) | `scripts/run_states.sh` main 의 `--source "${SHAPE_SRC:-${SRC:-GITT}}"` — `SRC` 는 상태 loop 변수라 **마지막 상태**(`300_0147`=step_005C 전용)가 샜다. `test_g25` 는 `shape_step` 을 `--source GITT` 로 직접 불러 이 줄을 지나지 않는다 | shape 소스를 loop 와 분리(`SHAPE_SRC` 아니면 GITT), 요약 줄에 출력 | `test_g27` — production 스크립트를 **통째로** 돈다 (적합 3 명령은 PATH shim 이 rc 7 로 즉시 실패, `ne_shape` 호출은 argv 만 기록). 고치기 전 RED 로 `--source=step_005C` 재현 |
| **U18-02** | 13 중 **11** 이 `git_state_changed_during_run: true`. 트리는 깨끗했다 | `run` 의 시작 provenance 가 `python3 scripts/provenance.py "$art"` → CLI 기본 `output_roots=("out",)`. `OUT=out_u18` 은 그 밖의 **untracked 디렉터리**라 코드 변경으로 분류 → `git_dirty_at_start true`. 끝 상태는 `write_meta` 가 `output_roots=(out_dir,"out")` 로 물어 false → "실행 중 변경". 첫 산출만 clean(그때 디렉터리가 비어 git 이 보고하지 않는다) | CLI 가 둘째 인자부터를 산출 root 로 받고(`out` 은 늘 포함), `run` 이 `"${OUT:-out}"` 을 넘긴다 | `test_g28` — 산출 둘을 연달아 게시해 둘째의 `git_modified_code_at_start == ['out_alt/']` 재현 |
| **U18-03** | 대조가 rc **2**(계약 위반)를 냈고 근거는 정본 `ne_shape_GITT_Li.csv.meta` 에 `env` 가 없다는 것 **하나** | 옛 정본의 **나이**를 새 산출의 위반으로 청구. `env` 계약은 R10 P1-7 뒤에 생겼다 | `scripts/check_u14.py` 에 `env_uncomparable` 버킷 — 정본이 안 적었으면 대조 불가(rc 불변·승격만 불가), **새 산출**이 안 적으면 그대로 rc 2 | `test_g29` + 대조군(새 산출에서 `env` 제거 → rc 2 · `schema` blocker) |
| **U18-04** | 승격 직후 전체 테스트 **7 건** 실패 | (a) `tests/test_review_findings.py:_ne_shape_csv` 의 텍스트 열 목록이 `schema` 와 **별개 사본** → 새 22 열 정본의 `inputs_sha` 를 `float()` 로 읽음 (b) `test_f26`·`test_d8_02` 가 **살아 있는 정본**을 옛 스키마 표본으로 씀 (c) `test_d8_07` 은 우리가 같은 `replay_codex_r7.py` 를 동시에 돌린 탓 | (a) 목록을 `schema.SHAPE_NON_NUMERIC` 에서 유도 (b) 표본을 `out/archive/legacy_r6_u14/` 로 + `d8_02` 에 "현행 정본은 rc 0" 을 같이 고정 (c) 코드 변경 없음, 증거 README 에 경고 | 기존 6 개가 그대로 회귀다 (`f26`·`d8_02`·`i6w_07`·§1-12 표 2 · R3-03) |

U18-02 는 위조 방향이 아니라 **거짓 양성**이다. 다만 `scripts/provenance.py` 머리말이 경고하는 고장("플래그가 늘
켜져 정보가 사라진다")을 wrapper 가 재현한 것이라 그 축의 신호는 죽어 있었다. **1 차 산출은 승격하지 않았다** —
고침은 다음 실행의 서명을 고칠 뿐이고, 그 위에 `matrix_100` 은 실행 중 **실제로** 커밋이 바뀌었다(`d07a77a`→`c9dd822`).
사면 규칙을 만들지 않고 다시 돌렸다.

## 4. 정본 상태 변화

| | R13 시점 | 지금 |
|---|---|---|
| `out/` `--schema-only` | rc 2 · 40 · 25 · 6 · 1 | **rc 0** · 전부 0 (`baseline_absent` 1 만) |
| 옛 묶음 | `out/` 그 자체 | `out/archive/legacy_r6_u14/` — **같은 네 수를 그대로 낸다** (§1 실측) |
| 표본을 쓰는 회귀 | `out/` 을 가리킴 | archive 를 가리킴 (`test_f26` · `test_d8_02`) |

`out/archive/README.md` 가 그 디렉터리가 왜 얼어 있는지 적는다 (승격 커밋에서 같이 갱신).

## 5. 닫지 않은 것 — 신뢰 경계

| 항목 | 상태 |
|---|---|
| **조건 6** 동적 인증 | 열림. `test_g10` 은 AST 순서 검사이지 **우회 재현이 아니다** |
| **조건 8** 다섯 축 (공통 snapshot · dataset manifest · run receipt · partial 수명 · locator 무결성) | 열림. 이번 라운드도 손대지 않았다 |
| **U18-05 후보 (우리가 찾고 안 닫음)** | 승격된 묶음의 산출들이 **서로 다른 `git_commit`** 을 가질 수 있고 `check_u14` 는 그것을 안 본다. 이번 실제 사례: `matrix_300_0147` 만 재게시돼 그 상태 3 개 + shape 가 `419c1ab`, 나머지 9 개가 `0668665`. 우리는 `git diff --name-only 0668665 419c1ab -- '*.py' '*.sh'` = **0** 으로 무해함을 확인했지만, **게이트는 그 확인을 강제하지 않는다** |
| r11 `publish:profile_partial_stdout` | 미실행(그룹 중단) · **대체 증거 없음** → `closed_with_substitutes: false` 로 정직하게 남아 있다 |
| C34 `receipt_paths` 소비자 · C25 before-evidence 40-hex | 열림 (C25 는 보관 패키지라 안 고친다) |
| `openpyxl` 이 `env_signature`/`ENV_KEYS` 에 없음 | 열림 — 넣으면 세 종류 sidecar 계약과 fixture 가 같이 바뀌므로 별도 라운드 |
| C28 none 회귀가 rc 1 만 봄 · C31 | 열림 |
| 원자료 | 이 저장소·컨테이너에 없다. `STATES` 실행 숫자는 사용자 기계 출력이고, 승격 후 검증만 이쪽에서 재실행했다 |

## 6. fixture 감사 — 열세·열네 번째

| 회 | 무엇이 거짓이었나 |
|---|---|
| 13 (U18-03) | `test_g29` 의 첫 fixture 가 3 행짜리 matrix 를 canonical 이름에 뒀다 — R13 P1-1 의 자리 규칙(좁힌 실행은 정본이 아니다)에 걸려 env 축에 닿기 전에 content 로 막혔다. 정본 자리에는 정본 모집단(`_canonical_combo_rows`) |
| 14 (U18-04) | `_ne_shape_csv` 가 `schema` 와 **별개의 텍스트 열 목록**을 들고 있었다. `test_i6w_07` 이 2026-09-12 에 "커밋된 산출이 아직 옛 스키마라 fixture 가 진실을 가린다" 고 적어 둔 그 고장이 승격으로 실제로 터졌다 — 2 년치 경고가 실현된 셈이다. 목록을 정본에서 유도하도록 바꿔 같은 축의 재발을 막았다 |

## 7. 리뷰어에게 묻는 것 (되돌릴 수 있는 선택들)

1. **`env_uncomparable` (U18-03)** — 옛 정본이 `env` 를 안 적은 것을 계약 위반(rc 2)에서 "대조 불가"(rc 4)로 내렸다.
   근거: C16 이 입력 identity 축에서 확립한 비대칭 + 새 산출의 `env` 존재는 `--schema-only` 가 따로 강제한다.
   **반대 의견이면 되돌린다** — "옛 baseline 을 상대로는 아예 승격 대조를 금지한다" 가 더 안전한가?
2. **승격의 근거를 사람이 적은 결정으로 둔 것** — 옛 정본에 receipt 가 없어 `promotion_eligible` 은 **구조적으로
   영원히 false** 다. 우리는 런북에 조건(numbers 0 · 계약 축 0 · 두 uncomparable 만 > 0)을 미리 적고 커밋 본문에
   `PROMOTION` 줄을 붙였다. 도구가 스스로 감사 가능한 판정을 내게 해야 하는가 (예: `--accept-uncomparable` 이
   조건을 검사하고 전용 rc·필드를 내는 방식)? 지금은 글자로만 남는다.
3. **U18-05 (§5)** — 승격 묶음의 `git_commit` 혼재를 게이트가 막아야 하는가? 후보 규칙 둘: (a) 단일 커밋 강제
   (b) "코드 파일 diff 가 비었을 때만 허용". (b) 는 도구가 git 을 더 깊이 보게 된다. 어느 쪽인가?
4. **U18-02 의 고침 범위** — CLI 가 산출 root 를 인자로 받게 했다. 기본값 `("out",)` 을 **없애고** 인자가 없으면
   거부(fail-closed)하는 편이 나은가? 지금은 인자를 빠뜨린 호출자가 조용히 옛 동작을 얻는다.
5. **U18-04 의 표본** — 회귀가 **커밋된 실제 산출**(archive)에 의존한다. 합성 fixture 로 바꾸면 경로 의존이 없어지지만,
   이 저장소에서 네 번 이상 실측된 "fixture 가 진실을 가림" 패턴이 되돌아온다. 실제 bytes 표본을 유지하는 것이 맞는가?

## 8. COMSOL 6.3 트랙 — 이번 라운드에서 **리뷰 범위 밖**으로 두는 이유

같은 브랜치에 마이크로쇼츠 COMSOL 재구축 문서(`docs/COMSOL_REBUILD_SPEC.md` §8~§12)가 있으나 이 요청에 **넣지
않는다.** 판단 근거:

| 절 | 근거 자료 위치 | 리뷰 가능한가 |
|---|---|---|
| §10 (메시 축별) | `reviews/r14_repros/codex63/mesh_axes/` — 원문 90 파일 bytes 보존, `package_manifest.json` 대조 완료, 원시 CSV 로 최대값·분해·step 재계산 | **가능** — 저장소만으로 "우리 전사가 원문과 맞는가"를 검증할 수 있다 |
| §11 (초기 시간상한) · §12 (반경 300/160) | 없음. ZIP 이 세션에 첨부되지 않았다 | **불가** — 전달 요약의 전사일 뿐이고 절 머리에 그렇게 적혀 있다 |

§11·§12 의 원문이 저장소에 들어오면 §10 과 같은 방식(manifest 대조 + 원시 CSV 재계산)으로 확정한 뒤, 그때
"전사가 원문과 맞는가 · 우리가 어디서 과다 주장했는가" 를 한 번에 묻는 것이 싸다. **COMSOL 결론은 이 요청과
무관하게 그대로다**: 반경축 전압 기준 미충족 · 전체 메시 수렴 미완 · 장시간 본 실행 보류 · GO 아님.

## 9. GO 시 다음 실행 계획

이 라운드는 **비싼 본 실행을 요구하지 않는다** (조건 7 의 실데이터 재실행은 이미 끝났고 승격됐다). GO 의 뜻은
"이 승격과 네 발견의 처리를 받아들인다" 이고, 그 다음 순서는:

1. 조건 6(동적 인증) 설계 — `test_g10` 을 AST 검사에서 **실제 우회 재현**으로 올린다
2. 조건 8 의 다섯 축을 하나씩 (공통 snapshot → dataset manifest → run receipt → partial 수명 → locator)
3. §7 의 질문에서 나온 결정을 반영 (특히 2·3 은 게이트 계약 변경이라 이 순서보다 앞선다)

보존할 증거: `reviews/r13_repros/replay_ours_after_fixes/` (이 커밋 판) · `out/archive/legacy_r6_u14/` (옛 정본
26 파일, 조건 7 의 보존 대상) · `reviews/r14_repros/codex63/mesh_axes/` (COMSOL 원문).

## 10. 재현 명령

```bash
git fetch origin claude/bms-alpha-beta-verify && git checkout 1bb45b358db4850c73e185d5f851e35fbcff9ad6
cd bms-balancing
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ -q -p no:cacheprovider          # 277 passed
python3 scripts/check_u14.py --new out --schema-only                               # rc 0
python3 scripts/check_u14.py --new out/archive/legacy_r6_u14 --schema-only         # rc 2 · 40·25·6·1
HEAD=$(git rev-parse HEAD)
for n in 7 9 10 11; do python3 reviews/r${n}_repros/replay_codex_r${n}.py --target . --expected-head "$HEAD" --output /tmp/r$n.json; done
#   ⚠ 위 러너와 `pytest tests/` 를 **동시에 돌리지 않는다** — `test_d8_07` 이 같은 replay_codex_r7.py 를 부른다 (U18-04)
R6_OLD_OUT="$(mktemp -d)"; git archive bfc4623^ out | tar -x -C "$R6_OLD_OUT"; export R6_OLD_OUT="$R6_OLD_OUT/out"
python3 reviews/r6_repros/codex/replay_codex_r6_adapted.py --target . --output /tmp/r6a.json   # mode full 6/6
bash matlab/tests/run_all.sh                                                       # Octave 필요
```

원자료(`BMS_DATA_ROOT`)가 필요한 것은 `scripts/run_states.sh` 뿐이고 위 명령에는 없다.
