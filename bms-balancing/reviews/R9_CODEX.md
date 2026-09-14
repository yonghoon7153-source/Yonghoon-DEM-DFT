# α·β 검증 하네스 R9 — Codex 리뷰 (원문, 2026-09-12 수신)

> 대상 `29ef5058e68c0c64dba840ecc5a7495644cb092e`. 받은 재현 패키지(`reviews/r9_repros/codex/`, sha256 11/11 OK)의
> `HARNESS_R9_29EF5058_CODEX_REVIEW.md` **그대로**다. 대응은 `R6_LEDGER.md` 의 "Codex R9" 절.


## 판정

**NO-GO — P1 7건 · P2 5건.**

대상은 `claude/bms-alpha-beta-verify`의
`29ef5058e68c0c64dba840ecc5a7495644cb092e`로 고정했다. 요청문 원본과 저장소의
`reviews/R9_REQUEST.md`는 SHA-256이 같았고, 검토 뒤 대상 worktree는 clean이다.

R8의 여덟 수정은 모두 허상이 아니다. 검증 snapshot 소비, profile 영수증 내구성,
중복행의 일반 대조, callback 게시 횟수, `c6_04`의 값 `222` 관측은 실제로 닫혔다.
그러나 "모집단을 먼저 세고, 검증 snapshot만 검사하고, 부분은 부분이라 말한다"는
R9의 제목은 아직 production 전체의 불변식이 아니다. 인자 파싱, U18 승격, `ne_shape`
입력·게시, `dd_eval` 검증에서 각각 그 불변식을 우회할 수 있다.

## 최소 반증 조건

### R9-01 — P1 — 같은 root label이 앞의 요청을 지운다

- 자리: `scripts/compare_states.py:134-139`.
- 반례: `compare_states.py same=<없는-root> same=<정상-root>`.
- 실제: 두 번째 dict 대입이 첫 요청을 지운다. `요청한 root 1개`, `1/1`,
  `항상 가장 좁은가: 예`, rc 0이다. label을 다르게 주는 대조군은 두 root를 세고 rc 2다.
- 무효화: R8-01의 "명시한 root 하나하나가 후보"라는 모집단 보장.
- 최소 수정: 인자를 ordered list로 유지하고 중복 label을 사전에 거부한다. 여러
  unlabelled 인자도 모두 `out`이 되므로 거부하거나 고유 label을 부여해야 한다.

### R9-02 — P1 — U18은 새 디렉터리에 있는 파일만 세므로 1/12도 전수로 승인한다

- 자리: `scripts/check_u14.py:125-155`, 성공 반환 `:295-348`.
- 반례: old에 서명된 산출 12개를 두고 new에는 동일한
  `degeneracy_100_Li.json{,.meta.json}` 한 묶음만 둔 뒤 일반 대조를 실행한다.
- 실제: `산출 1개`, `새 스키마 전부`, `숫자 전부 같다`, rc 0이다. old에만 있는
  11개는 순회되지 않는다.
- 무효화: U18을 별도 destination에서 비교한 뒤 승격한다는 완전성 조건.
- 최소 수정: 서명된 실행 manifest나 old/new canonical basename의 합집합으로 exact
  artifact roster를 정하고 missing·extra를 모두 거부한다. 부분 재실행은 명시적 subset
  계약과 그 범위를 출력해야 한다.

### R9-03 — P1 — U18은 receipt의 이름만 보고 내용·과학 열·실행 조건을 보지 않는다

- 자리: `scripts/check_u14.py:19-35`, CSV header만 보는 `:139-149`, 교집합만
  비교하는 `:165-180`.
- 반례 A: 서명된 matrix에서 `LLI_pct`를 삭제한다. 반례 B: 12개를 모두 두되
  `ref_inputs_sha`, `consumed_inputs`, `ref_consumed_inputs` 값을 전부 비운다. 반례 C:
  degeneracy의 `{n_starts,seed,n_grid,n_samples,tol}`을
  `{24,0,21,400,1%}`에서 `{1,731,999,1,50%}`로 바꿔 다시 서명한다.
- 실제: 세 경우 모두 rc 0이며 `전부 갖췄다` / `게시·서명만 바뀌었다`고 한다.
  빈 matrix도 production `read_unit`은 서명 일치로 읽는다. `--schema-only`에서는 중복
  row key 검사까지 건너뛴다(`:150-151`).
- 무효화: R8-02·05와 U18의 provenance 및 동일 실행 조건 승격 보장.
- 최소 수정: producer에서 파생한 artifact별 exact schema를 한 정본으로 사용한다.
  필수 셀의 nonempty/type, JSON receipt 역할·path·64-hex digest, 재계산한 aggregate
  digest, data/meta controls를 검증하고 열의 합집합과 exact row-key set을 비교한다.
  구조 검사는 schema-only에서도 항상 실행한다.

### R9-04 — P1 — `ne_shape`가 없는 반쪽전지 상태를 requested 전에 지운다

- 자리: `scripts/ne_shape.py:222-227`, requested 산출 `:335-339`, 판정 `:346-415`.
- 반례: 선언 상태를 `pristine,100,200`으로 두고 200 half-cell만 없애며 100 matrix
  pair는 제공한다.
- 실제: 200은 모집단에 들어가기 전에 사라진다. meta는
  `{requested:[100],paired:[100],missing:[]}`, stdout은 `1/1`, rc 0이다.
- 무효화: R8-03의 "측정은 requested 전부"와 미계산 상태의 명시적 전파.
- 최소 수정: 파일 존재 확인 전에 requested state roster를 고정하고
  `requested/available/missing_input/paired/missing_pair`를 각각 기록한다. 알려진 의도적
  부재는 source별 명시적 allowlist로 표현한다.

### R9-05 — P1 — `ne_shape`는 중복 matrix key의 첫 행을 과학 결과로 쓴다

- 자리: `scripts/ne_shape.py:89-117`, 특히 첫 match 즉시 반환 `:108-116`.
- 반례: 서명된 `matrix_100.csv`에 `(GITT,Li,0)` 두 행을 넣고 `gamma_Si`를 각각
  0.10과 0.40으로 둔 뒤 행 순서만 뒤집는다.
- 실제: 두 실행 모두 paired 1/1, rc 0이다. 그러나 선택 gamma는 0.10→0.40,
  gamma shape 변화는 17.59→35.73 mV로 바뀐다.
- 무효화: R8-05 중복 key 방어가 실제 downstream 소비자까지 닫혔다는 주장.
- 최소 수정: production reader 자체에서 정규화한 `(half_cell,si,numeric w_dqdv)`가
  정확히 한 행인지 강제한다. 선택적 사전 checker에 의존하지 말고 U18과 같은 typed
  validator를 공유한다.

### R9-06 — P1 — rc 3을 내기 전에 기존 완전 산출을 부분 산출로 덮는다

- 자리: 게시 `scripts/ne_shape.py:340-343`, 부분 판정 `:413-415`.
- 반례: 100·200 pair가 모두 있는 완전 실행을 같은 canonical 경로에 게시한 뒤 200
  pair를 없애고 다시 실행한다.
- 실제: 두 번째 실행은 rc 3이지만 이미 첫 완전 CSV/meta를 교체했다. 새 부분 묶음도
  `read_unit == (True,"일치")`다.
- 무효화: "부분은 부분이라 말한다"는 종료 코드가 canonical 보존까지 보장한다는 전제.
- 최소 수정: 완전성 판정을 게시보다 먼저 하고, partial은 별도 attempt namespace에
  typed 상태로 보존한다. canonical 승격은 complete만 허용한다.

### R9-07 — P1 — `eval --compare`가 검사한 bytes와 소비한 bytes가 다를 수 있다

- 자리: 최초 parse `bms_balancing/verify.py:1116`, precision 재열기 `:1117`, audit
  재열기 `:1148-1150`.
- 반례: 첫 read에는 중복 header가 있는 malformed snapshot A를 주고, 그 직후 같은
  path에 정상 snapshot B를 원자 교체한다.
- 실제: 단독 A는 `invalid`지만 race에서는 SHA 순서가 A/B/B가 되고, comparator는
  A의 32셀을 B의 precision/audit로 승인해 `complete`를 돌려준다.
- 무효화: 검증 snapshot만 소비한다는 R8-02의 상위 비교 경로 보장.
- 최소 수정: 한 번 읽은 immutable bytes/text와 digest를 parse, precision resolve,
  audit, compare 전부에 전달하고 검증 뒤 pathname을 다시 열지 않는다.

## P2 증거·계약 결함

1. **R7 closure runner의 공허 성공.** `replay_codex_r7.py:100-107,124-136`은 알 수
   없는 `--probes DOES_NOT_EXIST`를 조용히 버리고 `"probes": {}`, rc 0을 낸다.
   빈·오타·중복·valid+unknown을 거부하고 출력 key가 요청 집합과 정확히 같아야 한다.
2. **R7 replay의 evidence identity 미집행.** runner는 `target_head`를 기록하지만
   expected SHA, clean 상태, replay package bytes와 대조하지 않는다. 임의 HEAD에서도
   `반례 소멸`, rc 0이 가능하다. `--expected-head`와 source digest를 필수로 하고
   mismatch·dirty·`재현`·`오류` 중 하나라도 있으면 nonzero여야 한다.
3. **mutation audit의 종료 코드 분류.** `codex_r6_mutation_audit.py:18-30`은 같은
   `1 failed` summary에 대해 pytest rc 2·3·4도 `CAUGHT`로 분류한다. CAUGHT는 rc 1과
   기대 node/failure fingerprint에만 허용하고 2/3/4/5·signal·timeout은 audit error로
   분리해야 한다.
4. **matrix sidecar의 범위가 본문과 모순된다.** `run_states.sh:45-70`의 sidecar는
   singular `GITT/Li`를 적지만 matrix 호출 `:211-215`와 `verify.py:1361-1368`은
   2 half-cell × 8 Si × 2 weights = 32행을 낸다. exact roster와 argv를 본문에서
   유도해 sidecar에 봉인해야 한다.
5. **all-pairs-missing 종료 계약 불일치.** 요청문과 원장은 "missing pair면 rc 3"이라고
   하나 pair가 전부 없으면 `ne_shape.py:352-355`가 먼저 rc 1을 낸다. 이는 false
   success는 아니지만 wrapper가 typed 상태를 잃는다. zero-pair를 hard failure 1로 둘
   수는 있으나, 그렇다면 계약과 wrapper가 1/3을 명시적으로 구분해야 한다.

## R8 조건별 판정

| R8 조건 | 판정 | 근거 |
|---|---|---|
| R8-01 모집단·root roster | **부분** | same-state/different-Si와 고유 label root는 닫혔지만 중복/unlabelled label이 요청을 삭제한다. |
| R8-02 verified snapshot·출처 schema | **부분** | `read_unit` snapshot은 닫혔지만 U18은 roster·receipt 내용·`dd_eval` 단일 snapshot을 보장하지 않는다. |
| R8-03 requested/paired/missing·rc3 | **부분** | 입력이 존재할 때는 닫혔지만 missing input을 먼저 제거하고 partial이 canonical을 덮는다. |
| R8-04 profile receipt 내구성 | **닫힘** | 실제 optimizer 경로의 모든 CSV 행에서 target/ref full receipt를 회수했고 log를 비워도 남았다. |
| R8-05 duplicate row key | **부분** | 일반 U18 대조는 잡지만 schema-only와 `ne_shape` production reader가 우회한다. |
| R8-06 mutation audit 오류 분리 | **부분** | 선택 0/rc5는 닫혔지만 rc2/3/4를 CAUGHT로 오인한다. |
| R8-07 post-fix replay | **부분** | 실제 여섯 probe는 도달했지만 runner가 빈/오타 선택과 잘못된 target을 성공으로 낼 수 있다. |
| R8-08 publication counter·`c6_04` | **닫힘** | schedule별 게시 횟수를 실행했고 `c6_04`는 KeyError가 아니라 값 222 소비로 잡힌다. |

## 요청문 질문에 대한 답

1. **`state|si` 규칙:** 서로 다른 Si는 모델 층별 관측으로 보존해도 된다. 내부 identity는
   문자열 합성보다 typed `(root,state,si)`가 안전하며 같은 identity는 거부해야 한다.
   무엇보다 root label 중복이 그 전에 관측을 없애지 못하게 해야 한다.
2. **현재 다섯 관측의 초안 사용:** `provenance-incomplete`인 탐색적·잠정 관측으로만
   옮길 수 있다. GO, 승격, 원인·출처 주장, normative requirement의 근거로는 쓰지 않는다.
3. **공통 snapshot 강제 위치:** command/build 경계에서 공유 workbook·문헌 bytes를
   한 번 읽어 typed snapshot으로 reference/target 양쪽에 전달한다. `run_states`는 campaign
   manifest를 봉인하되 path pre-hash만으로 소비를 대신 증명하지 않는다. 다른 export는
   명시적 sensitivity mode와 A/B digest로 분리한다.
4. **rc 3:** wrapper는 typed `PARTIAL`로 보존하되 GO에서는 non-success여야 한다. hard
   failure 1과 partial 3을 합치지 말고, partial artifact는 canonical을 먼저 덮지 않는다.
5. **U18 승격:** exact 12-artifact manifest, 검증된 receipt, 동일 input/control/env를 먼저
   강제한 뒤 정의된 수치 projection의 exact equality를 본다. profile 행이 움직이면 승격하지
   말고 후보 evidence version으로 보존한 뒤 pinned old 환경 재현과 U16 attribution을 한다.

## 실행 증거와 한계

- 전체 Python 회귀: **155 passed**, rc 0.
- MATLAB smoke: 이 환경에는 Octave가 없어 1~3단계는 skip; 4~5단계만 통과했다. 따라서
  요청문의 Octave 전수 통과는 여기서 독립 재현했다고 세지 않는다.
- 현재 `out/` schema 점검: 산출 12개, provenance 누락 24건, 내부 rc 2 — 요청문의
  `provenance-incomplete` 신고는 정직하다.
- exact target의 R7 여섯 probe는 모두 도달했고 반례 소멸 상태를 냈다.
- 격리된 mutation audit는 baseline 7 passed, 8/8 CAUGHT, 복구 뒤 7 passed,
  `MISSED: 0`, rc 0. 다만 위 P2 분류 반례는 별개다.
- 독립 반례 스크립트 `r9_root_repros.py`의 다섯 묶음은 모두 assertion을 통과했다.
- 원자료·MATLAB·Octave가 없는 이 환경에서 실제 U18 계산 재실행은 하지 않았다. 이번
  NO-GO는 합성 fixture가 production parser/publisher/checker를 직접 호출해 만든 구조 반례다.

## GO를 위한 최소 조건

1. root와 artifact와 state의 expected roster를 실행 전에 고정하고 축소·dict 변환 전에
   missing/duplicate/extra를 거부한다.
2. U18을 exact typed schema + receipt 내용 + control/env + exact row-key validation으로
   바꾸고, 12개 전체를 한 manifest로 비교·승격한다.
3. `ne_shape` production reader가 duplicate를 거부하고, input absence를 별도 상태로
   기록하며, complete 판정 뒤에만 canonical을 게시한다.
4. `dd_eval`의 세 path read를 하나의 immutable snapshot read로 합친다.
5. evidence runner가 빈/오타/잘못된 SHA 및 pytest audit-error를 성공으로 내지 않게 한다.
6. 위 조건 각각의 기존 반례를 RED→GREEN 회귀와 변이로 고정한 뒤 U18을 실행한다.

따라서 **새 모델 설계 근거의 정본 승격과 GO는 보류**한다.
