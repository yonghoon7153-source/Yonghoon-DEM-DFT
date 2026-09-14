# α·β 검증 하네스 R11 — Codex 리뷰 (원문, 2026-09-13 수신)

> 대상 `2add074cf0c3ebfaa02b22d2311dd4330f0879b0` (코드 정본 `665c87e195007fb72f55f58f4c71ada81275c0c6`). 받은 재현
> 패키지(`reviews/r11_repros/codex/`, sha256 13/13 OK)의 `HARNESS_R11_2ADD074_CODEX_REVIEW.md` **그대로**다.
> 대응은 `R6_LEDGER.md` 의 "Codex R11" 절.

# 11차 α·β 검증 하네스 적대적 리뷰

## 판정

**NO-GO — 새 반례 P1 12건, P2 6건.**

대상은 증거 커밋 `2add074cf0c3ebfaa02b22d2311dd4330f0879b0`, 코드 정본은
`665c87e195007fb72f55f58f4c71ada81275c0c6`이다. 마지막 확인에서 대상 작업트리는 clean이었고,
`665c87e..2add074c` 사이 `.py`/`.sh` 변경은 0개였다.

R11이 먼저 신고한 미구현 항목(공통 export snapshot, 경로를 뺀 receipt digest, unsigned subset manifest,
typed `(root,state,si)`, U16/U17/U18, 현행 `out/`의 provenance 불완전, partial 수명)은 새 발견 수에 넣지 않았다.
아래는 그 목록 밖에서 실제 실행으로 재현된 반례다.

## 검증 환경과 양성 대조

- WSL Ubuntu, Python `/home/yonghoon71/ddvenv/bin/python`
- `python -m pytest tests/ -q` → **183 passed in 147.56s**
- `bash matlab/tests/run_all.sh` → Octave 부재로 1–3단계 skip, 4–5단계 PASS, rc 0. 따라서 Octave 전체 통과로는 세지 않았다.
- R7 재생 → 6/6 closed, `evidence_eligible:true`, `instrument_sealed:true`, package digest 정상
- R9 재생 → 12/12 closed, 같은 표면상 봉인 결과
- R10 closure 재생 → 22/22 closed로 출력되지만, 아래 P1-11/P1-12 때문에 그 출력 자체가 신뢰할 수 없다.
- `check_u14.py --new out --schema-only` → rc 2, promotion false. 요청문이 신고한 현행 산출의 불완전성과 일치한다.
- R10 집중 회귀 `d10_02..d10_11` → 10 passed

## P1 반례

### P1-1 — baseline과 candidate가 서로 다른 입력 bytes여도 승격된다

**자리:** `bms_balancing/schema.py:51-52,128-164`, `scripts/check_u14.py:44-49,244-258,479-490`

각각 내부적으로 유효한 role receipt를 만들되 old/new의 target·reference SHA를 모두 다르게 했다. 과학 숫자,
control, env, run id는 같게 두었다.

```bash
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case receipt_identity
```

**관측:** target `9d6ace08c3d4 → 48cf03a6b6b8`, reference `d789ce826bcd → e9a7ac3dea7c`, 네 digest가
모두 달랐지만 rc 0, `blocked_by` 전부 0, `promotion_eligible:true`였다.

각 receipt의 자기 일관성만 확인한 뒤 `ROW_SKIP`이 입력 identity를 old↔new 비교에서 제외하기 때문이다.

**최소 조건:** 양쪽 receipt를 정확한 `{logical_role: full_sha256}`로 정규화해 비교하고, 하나라도 다르면 숫자 비교 전에
input/control mismatch로 막는다.

### P1-2 — matrix 진단 옵션이 정본 authority를 줄이고도 canonical을 게시한다

**자리:** `bms_balancing/verify.py:1445-1456,1505-1508,1581-1586,1924-1925`

```bash
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case matrix_subset
```

**관측:** 실제 authority는 `2 sources × 8 Si × 2 weights = 32`인데 `--only-source --only-wdqdv`가 8개만
요청하고 이를 `complete`, canonical, rc 0으로 게시했다. 독립 toy fixture에서도 8→2 canonical 교체가 재현됐다.

**최소 조건:** canonical roster를 옵션 적용 전에 고정한다. 진단 selector가 하나라도 authority를 줄이면 `subset`, rc 3,
run-id partial namespace만 허용하고 exact requested/succeeded/missing tuple roster를 봉인한다.

### P1-3 — `--grid 1`이 1점 profile을 완전한 canonical로 만든다

**자리:** `bms_balancing/verify.py:1612,1683-1690,1725-1736,1926`

```bash
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case profile_grid
```

**관측:** γ 한 점만 계산하고 `requested:1, succeeded:1`, `status:complete`, canonical write, rc 0이었다.
모든 span은 당연히 0.0이었다. production canonical grid는 21점이다.

**최소 조건:** exact γ 값과 개수를 포함한 signed canonical grid를 코드/계약에 고정한다. 다른 `--grid`는 subset·rc 3·partial이다.

### P1-4 — 오래된 부재 allowlist가 실제로 생긴 측정을 조용히 숨긴다

**자리:** `bms_balancing/data.py:30-36,58-65`, `bms_balancing/verify.py:1445-1456,1505-1508,1581-1586`

```bash
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case allowlist
```

**관측:** `GITT/300_0147.xlsx`와 step 파일이 둘 다 존재했지만 `HALF_CELL_ABSENT`가 GITT를 먼저 제거했다.
그 결과 32개가 아니라 step-only 16개를 `complete`, canonical, rc 0으로 게시했다.

**최소 조건:** 부재 선언을 versioned dataset manifest와 결속한다. 최소한 “부재 선언된 경로가 실제 존재”하면 invalid rc 2로
실패해야 한다.

### P1-5 — 서로 다른 디렉터리의 old/new 파일이 같은 inode여도 독립 증거로 승인된다

**자리:** `scripts/check_u14.py:88-95,213-217,381-384`

```bash
python outputs/r11_publish_schema_repros.py
```

**관측:** 디렉터리는 `samefile:false`지만 data와 meta 파일 각각은 hardlink로 `samefile:true`였다. 비교는 rc 0,
`promotion_eligible:true`였다.

**최소 조건:** 모든 paired data/meta object에 대해 samefile/hardlink/symlink alias를 거부하거나, 한쪽을 immutable revision에서
owned regular file로 materialize한 뒤 identity를 재검사한다.

### P1-6 — `--schema-only`가 baseline도 비교도 없이 promotion certificate를 만든다

**자리:** `scripts/check_u14.py:211-212,368,479-490`

```bash
python outputs/r11_root_repros.py --target work/harness-r11-target-wsl/bms-balancing
```

**관측:** old=`null`, old roster 0, compared 0인데 rc 0과 `promotion_eligible:true`였다. 별도 재현에서는 candidate meta의
control·argv·roster를 지워도 같았다.

**최소 조건:** schema-only는 구조상 언제나 `promotion_eligible:false`여야 한다. 독립 exact schema 검증은 하되
`baseline_absent/schema_only`를 명시적인 blocker로 둔다.

### P1-7 — 공용 validator가 실패로 판정한 matrix error row를 production `ne_shape`가 소비한다

**자리:** `bms_balancing/schema.py:167-208`, `scripts/ne_shape.py:108-147`

```bash
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case shape_reader
```

**관측:** `error="optimizer failed"`가 있는 unit-signed row를 `S.check_rows()`는 실패로 판정했지만,
`fitted_pair_info()`는 그 row의 `(gamma_Si, ref_gamma_Si)=(0.4,0.2)`를 정상 과학 입력으로 반환했다.

**최소 조건:** production reader가 exact header와 함께 shared validator를 통과한 unit만 고르고, 선택 row의 cohort/receipt가
현재 shape run과 결속됐는지도 확인한다.

### P1-8 — 비유한/비숫자 과학 값이 유효 스키마로 승격된다

**자리:** `bms_balancing/schema.py:193-197,211-219`, `scripts/check_u14.py:156-162`

```bash
python outputs/r11_root_repros.py --target work/harness-r11-target-wsl/bms-balancing
```

**관측:** matrix `obj=inf`, degeneracy JSON `best_obj=Infinity`, profile `a_NE="not-a-number"`가 스키마 문제 0,
숫자 차이 0, rc 0, promotion true였다.

**최소 조건:** 모든 scientific scalar/array에 exact type·shape와 `math.isfinite()`를 적용하고, JSON parser/emitter는
NaN/Infinity를 거부한다. producer와 consumer 모두 같은 검사를 써야 한다.

### P1-9 — 명시적으로 더러운 provenance와 실제 untracked 실행 코드가 승격된다

**자리:** `scripts/check_u14.py:39-40,200-212,223-229,479-489`, `scripts/provenance.py:68`

```bash
python outputs/r11_evidence_gate_repros.py --target /tmp/r11-evidence-clean/bms-balancing --case u18-dirty-meta
python outputs/r11_evidence_gate_repros.py --target /tmp/r11-evidence-clean/bms-balancing --case untracked-sitecustomize
```

**관측 1:** candidate가 `git_dirty:true`, 변경된 `verify.py`, bogus start commit,
`git_state_changed_during_run:true`를 명시해도 rc 0/promotion true였다.

**관측 2:** untracked repository-root `sitecustomize.py`가 실제 실행돼 marker를 썼지만 provenance는 정확한 HEAD,
`git_dirty:false`, `git_modified_code:[]`를 기록했다. `--untracked-files=no`가 importable code도 숨긴다.

**최소 조건:** promotion 시 safe 값 자체를 강제하고 full canonical expected commit과 대조한다. output root만 별도 분류하고
그 밖 untracked executable/importable path는 code dirtiness로 보며, 실제 module origin/digest도 receipt에 묶는다.

### P1-10 — “격리 materialize + instrument seal”이 실제 실행 bytes를 봉인하지 않는다

**자리:** R7 runner `:25-26,159`, R9 `:22-23,330`, R10 `:21-22,135`,
`reviews/evidence_gate.py:83-117,133-150`

```bash
python outputs/r11_evidence_gate_repros.py --target /tmp/r11-evidence-clean/bms-balancing --case early-gate-pyc
python outputs/r11_evidence_gate_repros.py --target /tmp/r11-evidence-clean/bms-balancing --case materialize-smudge
```

**관측 A:** timestamp/size-valid ignored `reviews/__pycache__/evidence_gate.cpython-312.pyc`가 source보다 먼저 load되어
marker를 실행했다. source와 status는 clean인데 runner rc 0, `instrument_sealed`, `package_digest_ok`,
`evidence_eligible`, `closed`가 모두 true였다.

**관측 B:** committed `.gitattributes`와 repository-local smudge driver가 materialized `verify.py` bytes를 바꿨다.
그 변형 코드가 실행됐는데도 같은 네 값이 모두 true였다.

**최소 조건:** gate import 전에 isolated bootstrap/re-exec한다. checkout transformation을 완전히 끄거나 materialized tree의
모든 executable tracked object를 expected Git tree와 byte/mode로 재대조한다. 실제 loaded module origin/code digest와 runtime을
receipt에 묶는다.

### P1-11 — R10 parent가 rc 7인 evidence child 일곱 개를 모두 closed로 인증한다

**자리:** `reviews/r10_repros/replay_codex_r10.py:193-206`

```bash
python outputs/r11_evidence_gate_repros.py --target /tmp/r11-evidence-clean/bms-balancing --case r10-child-rc
```

**관측:** 각 checksum-listed child의 직접 rc는 7이었지만 기대 boolean만 출력하자 parent rc 0,
22-case closed, `evidence_eligible:true`, package/instrument seal true가 됐다.

**최소 조건:** child rc 0을 payload parse보다 먼저 강제하고, timeout/signal/nonzero/missing/extra case는 unresolved로 둔다.
exact child schema와 stdout/stderr fingerprint도 parent receipt에 포함한다.

### P1-12 — R10 classifier가 무관한 `AssertionError`를 반례 소멸로 바꾼다

**자리:** `reviews/r10_repros/replay_codex_r10.py:60-76,215-219`

```bash
python outputs/r11_evidence_gate_repros.py --target /tmp/r11-evidence-clean/bms-balancing --case r10-assertion-alias
```

**관측:** `schema.inputs_digest`가 `AssertionError("UNRELATED production invariant")`를 내게 하자 parent는 rc 0,
`도달:true`, `상태:"반례 소멸"`로 기록했다.

**최소 조건:** inverted assertion 대신 typed observation의 명시적 positive predicate를 쓴다. legacy assertion이면 case별 exact
file/line/source fingerprint를 봉인하고 그 밖 예외는 error다.

## P2 반례

### P2-1 — profile partial의 rc가 sink 유무에 따라 달라진다

**자리:** `bms_balancing/verify.py:1689,1725-1742`

`grid=2`, γ 하나 성공·하나 실패, `out=None`으로 실행하면 summary는 `partial`, roster는 1/2인데 rc 0이다.

**최소 조건:** semantic status에서 rc를 먼저 결정하고 sink 처리 뒤 공통 return한다.

### P2-2 — `shape_step`이 stale artifact를 읽고 outer wrapper가 partial을 전체 성공으로 세탁한다

**자리:** `scripts/run_states.sh:211-236,297-317`

```bash
python outputs/r11_data_contract_repros.py --target work/harness-r11-target-wsl/bms-balancing --case shape_wrapper
```

fresh partial과 stale canonical을 함께 두면 wildcard `ls | head -1`이 stale status를 고른다. 실제 rc 3도 outer wrapper의
`FAIL_COUNT`를 늘리지 않아 “전부 통과”, rc 0이 된다. rc 0 + meta partial인 shim도 “complete”로 출력됐다.

**최소 조건:** producer가 exact attempt manifest/path를 반환하고 wrapper가 `rc↔status↔namespace↔run-id`를 대조한다.
partial은 top-level 성공으로 변환하지 않는다.

### P2-3 — receipt role cardinality가 set 검사라 중복 의미 role이 통과한다

**자리:** `bms_balancing/schema.py:58-86,128-164`

nested `literature.gr`와 top-level dotted `"literature.gr"`를 서로 다른 SHA로 함께 두어도 validator가 문제 0을 반환했다.

**최소 조건:** 한 exact typed tree만 허용하고 flatten 전에 unknown/nonleaf/duplicate logical role을 거부하며 각 필수 role의
cardinality를 정확히 1로 검사한다.

### P2-4 — profile `gamma_roster`는 non-empty 문자열이면 통과한다

**자리:** `bms_balancing/schema.py:18-24,167-208`

유효 profile row의 `gamma_roster="not-json"`이 문제 없이 통과했다.

**최소 조건:** roster를 exact JSON schema로 parse하고 모든 row 동일성, unique finite gamma, requested/succeeded/missing 산술,
row key set, canonical authority를 함께 검증한다.

### P2-5 — 실제 `skip-worktree` 플래그를 evidence gate가 놓친다

**자리:** `reviews/evidence_gate.py:153-156`

```bash
python outputs/r11_evidence_gate_repros.py --target /tmp/r11-evidence-clean/bms-balancing --case skip-worktree
```

Git은 `S reviews/evidence_gate.py`를 출력했지만 `index_skip_flags()`는 빈 목록이었다. R7 runner는 rc 0,
eligible/closed true였다.

**최소 조건:** lowercase assume-unchanged와 대문자 `S` skip-worktree를 실제 index 명령 회귀로 각각 검출한다.

### P2-6 — exact expected commit 규약이 7자 prefix를 받는다

**자리:** R7 `:147-152`, R9 `:318-323`, R10 `:125-129`

```bash
python outputs/r11_evidence_gate_repros.py --target /tmp/r11-evidence-clean/bms-balancing --case abbreviated-head
```

`2add074`만 넘겨도 rc 0, 그 짧은 값이 expected head로 기록되고 eligible/closed true였다.

**최소 조건:** 입력 object를 commit으로 resolve해 full canonical object id와 tree id를 기록하고 exact 비교한다. 계약이 full SHA라면
abbreviation 자체를 거부한다.

## R10 15개 조건의 현 상태

| R10 조건 | R11 판정 | 근거 |
|---|---|---|
| P1-1 compare-before-write | 닫힘 | snapshot-before-write와 same object 거부가 유지된다. |
| P1-2 `ne_shape --states` authority | 좁은 축 닫힘 / 형제 열림 | 해당 states 축은 닫혔지만 matrix/profile authority가 caller 옵션으로 다시 줄어든다. |
| P1-3 failed γ partial | 부분 | 파일 sink는 partial이지만 stdout mode rc 0, caller가 grid 자체를 줄일 수 있다. |
| P1-4 matrix all errors | 부분 | error는 막았지만 selector/부재 선언이 authority 자체를 축소한다. |
| P1-5 error tagged union | 부분 | checker는 닫혔지만 production `ne_shape` reader가 shared validator를 우회한다. |
| P1-6 role receipt | 부분 | role digest는 생겼으나 old/new input bytes를 비교하지 않고 duplicate flattened role이 통과한다. |
| P1-7 env/control | 부분 | unsafe provenance 값, body/meta 불일치, argv/roster 누락을 promotion gate가 허용한다. |
| P1-8 same directory | 부분 | directory alias만 막고 paired data/meta hardlink는 통과한다. |
| P2-1 subset rc | 닫힘 | 명시적 `--subset`의 rc 3은 유지된다. |
| P2-2 degeneracy stdout | 닫힘 | invalid stdout rc 처리는 유지된다. |
| P2-3 argv vector | 부분 | writer는 좋아졌지만 promotion gate가 argv를 필수/대조하지 않는다. |
| P2-4 `-O` | 좁은 축 닫힘 | `-O`는 거부하지만 pre-import bytecode와 replay classifier/child rc가 증거를 다시 위조한다. |
| P2-5 git identity | 안 닫힘 | pre-import pyc, checkout smudge, untracked importable code가 실행 identity를 깨뜨린다. |
| P2-6 package digest | 좁은 축 닫힘 | listed package corruption은 막지만 gate startup과 production snapshot bytes는 봉인 밖이다. |
| P2-7 wrapper typed status | 안 닫힘 | stale wildcard selection과 outer rc 세탁이 남았다. |

## 요청문 질문에 대한 답

1. **receipt digest와 path:** “같은 role bytes는 relocation돼도 같은 과학 실행”이라는 전제는 유지해도 된다. 다만
   baseline↔candidate의 role→full SHA map은 반드시 비교해야 한다. logical locator/path/parser selector는 별도 무결성 필드로
   묶는다. 확장자·sheet·parser 선택처럼 해석을 바꾸는 locator 부분은 semantic identity다.
2. **부재 allowlist:** versioned dataset-side manifest가 맞다. 코드 상수는 과도기적으로만 허용하되 실제 파일과 모순되면
   반드시 hard-fail해야 한다. 현재처럼 조용히 빼는 것은 승인할 수 없다.
3. **export scope:** full-cell과 문헌 gr/si는 한 공통 immutable snapshot을 강제한다. half-cell은 상태별로 다른 것이 맞으므로
   `(source,state,sha)` role snapshot으로 묶고, 이를 모으는 batch/cohort manifest를 둔다.
4. **`evidence_eligible`:** code/evidence 두 커밋 자체는 가능하다. run receipt가 code commit/tree, runner/gate blob 또는 실제
   code digest, package, runtime을 묶고, consumer가 뒤의 evidence blob과 허용된 ancestry를 검증해야 한다. 현재는 import-before-isolate와
   checkout filter 때문에 그 규약을 충족하지 못한다. 도구를 별도 versioned axis로 빼는 것도 가능하다.
5. **partial 수명:** fixed-name 덮어쓰기는 부족하다. `partial/<producer>/<attempt-or-content-id>/` immutable unit과 명시적인
   retention/GC/index가 필요하다. wildcard로 “첫 파일”을 소비하면 안 된다.

## GO를 위한 최소 조건

1. P1-1~P1-12의 false promotion/canonical/evidence-closure 경로를 모두 닫고, 각 반례를 그대로 RED→GREEN 회귀로 넣는다.
2. P2-1~P2-6의 rc/status/schema/identity ambiguity를 닫는다.
3. 요청문이 이미 신고한 공통 export typed snapshot 계약을 구현하고, pristine/target/state별 role manifest를 실제 production
   reader에 배선한다.
4. 새 규칙으로 U18을 별도 output에 재실행하여 exact roster·receipt·env/control·independence gate를 통과시킨다.
5. Octave가 있는 환경에서 MATLAB 전체 단계를 완주하고, 모든 증거는 실제 실행 bytes가 Git tree와 일치하는 봉인된 runner로
   다시 생성한다.

현재 상태에서는 “정본이 새 모델의 설계 근거로 쓸 만한가”에 **아니오**다. 특히 input identity가 바뀌어도 승격되고,
1점 profile/축소 matrix가 canonical이 되며, evidence runner가 commit 밖 bytes와 실패 child를 closed로 인증한다.

## 재현 산출물

- `outputs/r11_root_repros.py`, `outputs/r11_root_results.json`
- `outputs/r11_data_contract_repros.py`, `outputs/r11_data_contract_results.json`, `outputs/r11_data_contract_review.md`
- `outputs/r11_publish_schema_repros.py`, `outputs/r11_publish_schema_results.json`, `outputs/r11_publish_schema_review.md`
- `outputs/r11_evidence_gate_repros.py`, `outputs/r11_evidence_gate_results.json`, `outputs/r11_evidence_gate_review.md`
