# 10차 적대적 리뷰 — α·β 검증 하네스

## 판정

**NO-GO — 새 P1 8건, P2 7건.**

대상은 `bd6ba4749a92f8d441b4d9176eb876bfc6cc287c`이며, 코드 정본은 `554dad66`; 두 커밋의 차이는 닫힘 재생 JSON 2개뿐이다. 이 리뷰는 요청문 §5에 이미 신고된 export 계약, typed `(root,state,si)` identity, 미실행 U18을 새 발견으로 다시 세지 않았다. 그 항목들을 제외해도 잘못된 canonical 게시, 자기대조, provenance/조건 우회, 허위 closure 증거가 실행 반례로 남아 있으므로 설계 근거 승격은 불가하다.

## 검증 환경과 기준선

| 검사 | 관측 |
|---|---|
| 첨부 `R10_REQUEST.md` | 저장소 정본과 SHA256 동일: `8321f216a87d0ebc71a976da802f678df332c2eb36f0709678667ec35ffaef46` |
| 대상/코드 커밋 | `bd6ba474…`; `git diff 554dad66 HEAD`는 evidence JSON 2개뿐 |
| 전체 Python 회귀 | `167 passed in 94.23s` |
| R9 집중 회귀 | `12 passed in 19.87s` |
| R7 닫힘 재생 | 정상 환경에서 6/6 `도달:true`, `반례 소멸`, package digest OK, rc 0 |
| R9 닫힘 재생 | 정상 환경에서 12/12 `도달:true`, `반례 소멸`, package digest OK, rc 0 |
| 현행 `out/` 검사 | schema-only와 self-check 모두 rc 2; 요청문과 같은 provenance 열 누락 24건 |
| MATLAB 스모크 | 스크립트 rc 0이나 이 환경에는 Octave가 없어 1~3단계는 skip, 4~5단계만 통과. 요청문 컨테이너의 full-Octave 주장은 여기서 독립 재현하지 못함 |
| 대상 상태 | 모든 reviewer repro 뒤 clean |

정상 회귀가 초록이라는 사실은 인정한다. 아래 반례는 그 회귀가 보지 않는 가장자리다.

## P1 반례

### P1-1 — 독립 MATLAB 파일을 출력으로 덮은 뒤 Python이 자기 자신과 비교한다

- 자리: `bms_balancing/verify.py:1083-1091`, `:1093-1098`, `:1142`.
- 상태/호출: 독립 MATLAB 비교 파일 `X`를 일부러 invalid로 만든 뒤 `eval --out X --compare X`와 동등한 production `cmd_eval`을 실행한다.
- 기대: 출력과 비교 근거가 같은 object면 거부하거나, 적어도 비교 근거를 출력 전에 snapshot해야 한다.
- 실제: `args.out`이 `X`를 먼저 교체한 뒤 comparator가 처음 읽는다. 원본 SHA `c3dabc9d…`가 `3d18405e…`로 바뀌고, 16/16 anchor와 32/32 RMSE가 일치한다며 `complete`, rc 0.
- 무효화: R9-07의 “한 immutable snapshot”은 읽기 횟수만 닫았을 뿐 snapshot 절단면이 출력 뒤라 포팅 identity를 닫지 못한다.
- 최소 조건: `--compare`가 있으면 모든 쓰기 전에 `DdEvalText`를 읽고 그 typed snapshot만 comparator에 넘긴다. path 문자열 비교가 아니라 object identity/alias도 다뤄야 한다.

### P1-2 — `ne_shape --states`가 authority roster를 줄이고 축소본을 canonical complete로 게시한다

- 자리: `scripts/ne_shape.py:264-275`, `:384-401`.
- 상태/호출: 선언 상태 `100,200`의 2행 complete canonical을 먼저 만든 뒤 같은 destination에 `--states 100`을 실행한다. 별도 대조로 `--states 100,100`도 실행했다.
- 기대: canonical completeness는 versioned authority roster에 상대적이어야 한다. subset/duplicate는 canonical에 갈 수 없다.
- 실제: `--states 100`은 rc 0/status `complete`로 기존 2행 파일을 1행으로 교체한다. `100,100`은 requested/paired `2/2`, duplicate 2행, rc 0 complete.
- 무효화: R9-04의 requested population과 R9-06의 “complete만 canonical” 합성. caller 입력이 complete의 뜻 자체를 바꾼다.
- 최소 조건: source별 정본 roster 또는 versioned allowlist/digest와 exact equality를 canonical 조건으로 삼고 duplicate/unknown을 거부한다. subset은 별도 identity와 nonpromotion status로만 남긴다.

### P1-3 — profile 일부 gamma 실패가 canonical에 게시되고 실제 wrapper 서명도 통과한다

- 자리: `bms_balancing/verify.py:1535-1576`, `:1603-1642`.
- 상태/호출: gamma 2개 중 하나의 optimizer만 실패하도록 한다.
- 기대: requested gamma roster가 하나라도 빠지면 typed partial, nonzero, `partial/`에 게시되어야 한다.
- 실제: 실패 gamma는 행에서 빠지고 1행만 canonical을 교체한다. producer rc 0, `schema.check_rows=[]`. 실제 `run_states.sh`의 `write_meta`를 거쳐 서명한 뒤 production `provenance.py --verify-unit`도 `일치`를 반환했다.
- 무효화: 부분 결과 보존/승격 경계. missing 목록은 disposable stdout summary에만 있다.
- 최소 조건: gamma roster를 계산 전에 고정하고 requested/succeeded/missing을 artifact에 봉인한다. exact complete만 canonical; 나머지는 typed partial/failed와 비영 종료.

### P1-4 — matrix 전 조합 실패가 기존 canonical을 파괴하고 process success가 된다

- 자리: `bms_balancing/verify.py:1404-1407`, `:1512-1515`.
- 상태/호출: 모든 `build`를 실패시킨다.
- 기대: 기존 canonical을 보존하고 failed artifact를 별도 위치에 쓰며 비영 종료해야 한다.
- 실제: 16개의 4-field error row (`error,half_cell,si,w_dqdv`)가 기존 complete canonical을 교체한다. schema 문제 36건인데 함수가 `None`으로 끝나 process rc 0. wrapper는 뒤에서 run_id가 없다고 거부하지만 손상은 이미 일어났다.
- 무효화: 게시 전 판정과 canonical 보존.
- 최소 조건: expected combination roster와 typed status를 게시 전에 계산한다. exact success schema/roster만 canonical로 atomic replace한다.

### P1-5 — 임의의 `error` 열 하나가 U18 행 검증 전체를 끈다

- 자리: `bms_balancing/schema.py:114-136`, 특히 `:120-121`; `scripts/check_u14.py:186-241`, `:447-448`.
- 상태/호출: 정상 수치 행에 extra `error=skip`을 붙이고 `inputs_sha`, `ref_inputs_sha`, 두 receipt를 모두 비운 뒤 data/meta를 다시 서명한다.
- 기대: success row는 exact schema여야 하고 provenance가 비면 rc 2여야 한다.
- 실제: truthy `error`가 필수 셀/숫자/receipt 검사를 전부 `continue`한다. extra 열은 informational `added`일 뿐 실패가 아니다. full U18 gate가 “스키마 전부 갖춤”, “숫자 전부 같다”, rc 0.
- 무효화: R9-03 content/provenance closure.
- 최소 조건: success/error exact tagged union. success에는 `error` 금지; error row가 하나라도 있으면 enclosing unit은 nonpromotable partial/failed.

### P1-6 — receipt의 실제 역할이 사라져도 decoy가 provenance로 승인된다

- 자리: `bms_balancing/schema.py:44-52`, `:80-110`.
- 상태/호출: target/ref receipt를 `{"decoy":{"path":"nowhere","sha256":"aa…"}}` 하나로 바꾸고 12-hex aggregate를 재계산한다. 별도 대조로 half-cell/full-cell 역할을 서로 바꿨다.
- 기대: artifact kind와 target/ref별 exact 역할(`half_cell`, `full_cell`, `literature.gr`, `literature.si`)을 요구하고 역할까지 digest에 묶어야 한다.
- 실제: decoy-only receipt가 validator 문제 0, full gate rc 0이다. digest는 SHA 값만 정렬하므로 역할 swap도 같은 `76be1dcab00e`이고 둘 다 valid다.
- 무효화: R9-03이 주장한 receipt “역할”과 U18 provenance completeness.
- 최소 조건: versioned exact nested role schema를 먼저 검사하고 `(role, object identity/path, sha256)` canonical manifest 전체를 hash한다.

### P1-7 — 환경 변경과 control 삭제가 같은 실행으로 승인된다

- 자리: `scripts/check_u14.py:37-40`, `:195-212`.
- 상태/호출 A: candidate meta의 Python/NumPy/SciPy 환경을 전혀 다른 값으로 바꾼다. B: candidate에서 `state`/`starts`를 삭제한다.
- 기대: 조건/env가 다르거나 필수 control이 없으면 승격 불가.
- 실제: `env`는 존재만 요구하고 비교하지 않는다. control 비교는 양쪽에 key가 있을 때만 하므로 삭제하면 검사가 잠든다. 두 경우 모두 rc 0, “전부 같다”, 조건 불일치 0.
- 무효화: R9-03 condition closure와 R10 §3/Q5의 same controls/env 조건.
- 최소 조건: artifact kind별 필수 control exact schema, canonical environment signature를 숫자 비교 전에 강제한다. 의도적 환경 drift는 별도 sensitivity/nonpromotion 모드로 분리한다.

### P1-8 — candidate와 baseline이 같은 directory여도 독립 재현으로 인증된다

- 자리: `scripts/check_u14.py:325-362`.
- 상태/호출: 동일한 signed directory를 `--new`와 `--old`에 함께 준다.
- 기대: 독립 baseline과 candidate가 samefile/manifest identity면 승격 gate가 거부해야 한다.
- 실제: rc 0, roster 1/1, “정본(candidate)과 전부 같다”. baseline을 이미 덮었거나 애초에 없었던 상태를 구별하지 못한다.
- 무효화: R9-02 exact comparison을 promotion predicate로 쓰는 것.
- 최소 조건: resolved/samefile identity를 거부하고 서로 다른 immutable candidate/baseline manifest digest에 보고서를 결속한다. `--old-rev`의 immutable bytes는 허용 가능하다.

## P2 반례

### P2-1 — `--subset`의 “승격 불가”가 텍스트일 뿐 rc는 성공이다

정본 2개, candidate 1개에 `check_u14 --subset`을 실행하면 “부분, 승격 아님”을 출력하지만 rc 0이다. 자동 소비자는 full equality와 구분할 구조가 없다. 부분 검사는 허용해도 rc 3 또는 typed `promotion_eligible:false`를 내고, subset manifest를 봉인해야 한다.

### P2-2 — invalid degeneracy stdout artifact가 rc 0이다

`bms_balancing/verify.py:560-568`은 `--out`에서만 schema를 강제한다. stdout 모드는 receipt와 `inputs_sha`가 빠진 parseable JSON을 내고 stderr 경고 뒤 rc 0이다. sink가 stdout이라는 사실은 semantic validity 경계가 아니다. invalid면 항상 비영 종료하고 bare artifact 대신 typed diagnostic을 써야 한다.

### P2-3 — “exact argv”는 `$*` 문자열이고 회귀는 production 결속을 실행하지 않는다

- 자리: `scripts/run_states.sh:171-173`; 회귀 `tests/test_r9_codex.py:285-302`.
- 서로 다른 argv `['cmd','a b','c']`와 `['cmd','a','b c']`가 같은 `cmd a b c`로 기록된다.
- named test는 `run()`을 부르지 않고 `LAST_ARGV`를 직접 주입한다. production 줄을 `LAST_ARGV="FORGED-BY-MUTANT"`로 바꿔도 `1 passed`.
- 조건: `"$@"` 경계를 JSON array로 기록하고, 회귀가 실제 `run()`+shim producer를 통과해야 한다.

### P2-4 — closure runner는 `python -O`에서 실패한 pytest를 closed로 인증한다

- 자리: R7 `replay_codex_r7.py:80-91`; R9 `replay_codex_r9.py:94-105`, `:245-252`.
- 재현: `PYTHONOPTIMIZE=1 PYTEST_ADDOPTS=--definitely-invalid-option ...replay_codex_r9.py --probes P2-4`.
- 실제: delegated pytest는 usage error인데 모든 runtime check가 `assert`라 제거된다. runner rc 0, `closed:true`, P2-4 `반례 소멸`; summary 자체에는 invalid option이 남는다.
- 조건: runtime evidence 판정에 `assert`를 쓰지 않고 명시적 분기/예외와 subprocess rc/fingerprint를 final predicate에 값으로 묶는다. optimize mode도 fail-closed한다.

### P2-5 — HEAD+porcelain은 실행 bytes를 봉인하지 않고 status 오류도 clean으로 바꾼다

- 자리: R7 `dirty_paths:68-71`, R9 `dirty_paths:62-65`와 HEAD/dirty preflight.
- 반례 A: `GIT_INDEX_FILE=<directory>`에서 직접 `git status` rc 128인데 runner는 `dirty:false`, `closed:true`, rc 0.
- 반례 B: `verify.py`를 `assume-unchanged`로 둔 뒤 marker를 삽입하면 porcelain은 빈 값인데 수정 source가 실행되고 closed rc 0.
- 반례 C: source mtime/size에 맞춘 ignored `__pycache__/verify.cpython-312.pyc`가 실행되어도 clean/closed rc 0.
- 조건: status rc 비영은 즉시 오류. 증거 실행은 expected commit에서 새로 materialize한 격리 snapshot을 사용하고 tracked blob을 tree와 대조하며 index skip flags/ignored importable bytes를 배제한다.

### P2-6 — package digest 집행 삭제 변이가 회귀를 통과한다

R7 runner의 `package_digest()`를 mismatch에도 `True`로 만드는 변이가 `test_d9_08...`에서 `1 passed`였다. 실제 checksum 대상 파일을 손상시킨 뒤에도 JSON은 `mismatch`와 동시에 `package_digest_ok:true`, `closed:true`, rc 0이 됐다. 테스트는 source에 문자열이 있는지만 볼 것이 아니라 실제 package byte를 바꿔 runner 비영/probe 미실행을 검증해야 한다.

### P2-7 — “wrapper가 none/partial을 가른다”는 production path가 없다

`tests/test_r9_codex.py:305-315`와 adapted replay는 `ne_shape.main()`을 직접 부르고 meta/status 및 문서 문자열만 본다. production shell에서 `ne_shape` rc 1/3 또는 meta status를 소비하는 wrapper는 0개다. producer의 typed status 자체는 닫혔지만 caller 소비 주장은 닫히지 않았다. 실제 caller를 만들고 회귀에서 실행하거나 주장 범위를 producer contract로 좁혀야 한다.

## R9 조건별 판정

| 조건 | 판정 | 근거 |
|---|---|---|
| R9-01 duplicate labels | 닫힘(신고한 문법 경계) | explicit/implicit duplicate label 거부를 확인. typed physical root identity는 이미 신고된 미구현이라 재계수하지 않음 |
| R9-02 exact artifact roster | **부분** | 서로 다른 root의 missing/extra는 잡지만 self-comparison(P1-8)과 subset rc 0(P2-1)이 남음 |
| R9-03 schema/receipt/controls | **안 닫힘** | P1-5, P1-6, P1-7 |
| R9-04 requested population | **안 닫힘** | caller의 `--states`가 authority roster를 축소(P1-2) |
| R9-05 duplicate matrix keys | 닫힘(해당 축) | 두 행 순서 모두 중복 거부. duplicate requested state는 새 roster 축 |
| R9-06 complete-only canonical | **안 닫힘** | 축소 roster, partial profile, all-error matrix가 canonical을 교체(P1-2~4) |
| R9-07 single dd_eval snapshot | **부분** | compare 내부 one-read는 맞지만 snapshot을 output overwrite 뒤에 얻음(P1-1) |
| P2-1 probe names | 닫힘 | 빈/오타/중복/unknown 혼합 거부 및 요청 key 유지 확인 |
| P2-2 target/dirty/package | **부분** | 정상 mismatch는 막지만 P2-5/P2-6이 증거 identity와 회귀를 깨뜨림 |
| P2-3 mutation rc classifier | 좁은 축은 닫힘 | rc 1+failed만 CAUGHT는 맞음. 다만 wrapper 전체는 P2-4로 허위 closure 가능 |
| P2-4 sidecar roster/argv | **부분** | roster snapshot은 개선, argv는 비가역이며 named test가 production binding을 안 돎 |
| P2-5 typed none/partial | **부분** | producer/meta/canonical 분기는 존재. 주장한 wrapper 소비가 없음 |

## 질문에 대한 답

1. **`--subset`**: 부분 진단은 허용해도 된다. 다만 현재 rc 0은 안전하지 않다. rc 3 + typed `promotion_eligible:false` + signed expected-subset manifest가 최소 경계다.
2. **degeneracy stdout**: 우회로다. semantic invalid는 sink와 무관하게 nonzero여야 한다. 테스트용 incomplete object는 lower-level API로 만든다.
3. **`ne_shape --states`**: `requested_from` 기록만으로는 부족하다. 지금 옵션이 complete의 authority를 바꾼다. source별 versioned allowlist/roster digest와 exact equality, duplicate/unknown 거부가 필요하다.
4. **dirty runner**: 개발용 `--allow-dirty`는 가능하지만 결과에 구조적 `evidence_eligible:false`를 강제하고 evidence 소비자가 거부해야 한다. status 오류는 무조건 fail-closed; 신뢰 증거는 clean materialized snapshot에서만 만든다.
5. **export 계약**: build 경계 typed snapshot 방향은 맞다. shared full-cell뿐 아니라 선택한 literature gr/si도 한 번 읽은 role-keyed manifest로 ref/target 양쪽에 주입하고, snapshot 모드에서는 pathname fallback을 없앤다. sensitivity는 A/B 두 complete manifest digest로 표현한다.

## GO를 위한 최소 조건

1. P1-1~8의 각 reproduction이 기대한 비영/별도 namespace/검증 실패로 뒤집히고, 그 이유를 단일축 mutation이 물어야 한다.
2. matrix/profile/ne_shape의 expected roster와 typed completion을 게시 전에 정하고 exact complete만 canonical로 보낸다.
3. artifact kind·target/ref별 exact receipt role schema, role-aware manifest digest, 필수 control/env 비교를 U18 gate에 묶는다.
4. candidate/baseline 독립 identity와 compare-before-write snapshot을 구조로 강제한다.
5. P2-3~6의 evidence runner/sidecar 변이가 named regression을 통과하지 못하고, closure runner가 실제 subprocess result와 실제 실행 bytes를 봉인한다.
6. P2-1/2/7의 상태를 machine-readable하게 만들고 실제 caller 경로를 회귀로 실행한다.
7. 그 뒤 요청문 §5의 이미 신고된 독립 전제(export snapshot 계약, typed root identity, 실제 U18 및 남은 U16/U17)를 닫거나 명시적으로 비승격 범위로 격리한다.

## 재현 명령

workspace root에서:

```bash
python outputs/r10_snapshot_repros.py --target work/harness-r10-target-wsl/bms-balancing --case all
python outputs/r10_u18_shape_repros.py --target work/harness-r10-target-wsl/bms-balancing --output outputs/r10_u18_shape_results.json
python outputs/r10_evidence_repros.py --target work/harness-r10-target-wsl/bms-balancing --case all
```

세 묶음 모두 bad-state assertion을 통과했다. 상세 raw 결과는 각 `*_results.json`, 축별 설명은 `r10_snapshot_review.md`, `r10_u18_shape_report.md`, `r10_evidence_review.md`에 있다.
