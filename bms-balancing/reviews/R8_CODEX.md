# α·β 검증 하네스 R8 — 최종 Codex 리뷰 (원문, 2026-09-12 수신)

> 대상 `a22da3380338f97b8eed2f600ffefad1e398c6c3`. 받은 재현 패키지(`reviews/r8_repros/codex/`, sha256 10/10 OK)의
> `HARNESS_R8_A22DA338_CODEX_REVIEW.md` **그대로**다 (본문 링크의 `C:/Users/...` 는 Codex 쪽 로컬 경로 — 같은 스크립트가
> `reviews/r8_repros/codex/` 에 있다). 대응은 `R6_LEDGER.md` 의 "Codex R8" 절.


## 판정: NO-GO

대상은 브랜치 `claude/bms-alpha-beta-verify`의 **`a22da3380338f97b8eed2f600ffefad1e398c6c3`**, 범위는 `bms-balancing/`이다. 첨부 `R8_REQUEST.md`와 저장소의 `reviews/R8_REQUEST.md`가 같은 요청임을 확인했다.

**R7의 원래 여섯 반례를 겨냥한 수정은 상당 부분 작동한다. 그러나 “검증된 개별 묶음 → 완전한 모집단 → 전체 결론”의 합성이 아직 닫히지 않았다.** 새 P1은 4건, 새 P2는 4건이다. c6_04는 여전히 값 비교가 아니라 `KeyError`로 실패한다. c6_01은 전체 주입 OFF는 잡지만 metadata 두 schedule의 개별 주입을 증명하지 못한다.

이 NO-GO는 `FINDINGS.md + out/`을 일반적인 새 모델 설계 근거로 승인하는 것에 대한 판정이다. 커밋된 12개 data 파일이 R7와 바이트 동일하고 현재 data/meta 묶음 검증을 통과한다는 사실은 인정한다. 다섯 관측을 한정어와 함께 **조건부 요구서 초안**에 옮기는 일까지 금지하는 판정은 아니다.

## 1. 직접 실행한 증거

원본 소스·정본 산출·원자료는 수정하지 않았다. 변이는 별도 임시 Git 사본에서만 실행했다. 대상은 실행 전후 clean이었다.

| 실행 | 직접 관측 |
|---|---|
| 전체 회귀 | **146 passed in 58.46s**, 실패 0 |
| `matlab/tests/run_all.sh` | rc 0, 단계 4·5 통과. **이 환경에는 Octave가 없어 1–3은 미실행** |
| 현행 정본 집계 | 4/4, `LLI 항상 가장 좁다: 예`, rc 0 |
| 현행 `check_u14 --new out --old out` | 12개, “스키마 전부 갖춤·숫자 전부 같음”, rc 0. 아래 R8-02 때문에 완전성 증거로는 불충분 |
| 수치·집계 반례 묶음 | rc 0: 3개 기존 회귀 + 새 반례 4개 모두 예상 관측 |
| 입력 snapshot·출처 묶음 | rc 0: 실제 SciPy optimizer로 noise/matrix 닫힘과 profile 반례 재현 |
| 포팅·변이 증거 묶음 | rc 0: 8개/5개 등록 변이와 양성·음성 대조, 아래 P2 재현 |

Python 3.12.3, NumPy 2.5.3, SciPy 1.18.1, pandas 3.0.5, openpyxl 3.1.5, pytest 9.1.1의 WSL 환경이다. 원본 MATLAB·비공개 xlsx를 독립 재실행한 것은 아니다.

[통합 원시 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r8_replay_results.json)에는 명령·종료 코드·stdout/stderr·환경·스크립트 해시·대상 전후 상태가 있다. 재현 스크립트의 rc 0은 **예상한 반례까지 관측했다**는 뜻이지 GO가 아니다.

## 2. 새 P1 네 조건

### R8-01 · P1 · 집계 모집단 — 정상 관측이 state key에서 사라지고, 요청한 root도 전건으로 세지 않는다

위치: [compare_states.py:68](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/compare_states.py:68), [82](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/compare_states.py:82), [137](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/compare_states.py:137), [199](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/compare_states.py:199), [203](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/compare_states.py:203).

재현:

```bash
python outputs/r8_inference_repros.py --target <a22da338/bms-balancing> --case aggregate
```

같은 state 100에 하네스가 지원하는 서로 다른 Si의 정상 묶음 둘을 만든다. 두 파일은 각각 `read_unit=True`다.

| 파일 | LAM_PE 폭 | LAM_NE 폭 | LLI 폭 |
|---|---:|---:|---:|
| `degeneracy_100_Kunz.json` | 1 | 2 | 9 |
| `degeneracy_100_Li.json` | 2 | 3 | 1 |

- Kunz만 있으면 실제 CLI는 **1/1, 아니오, rc 0**이다.
- Li를 추가하면 둘 다 정상인데 `out[m.group(1)]`에서 Li가 Kunz를 덮는다. 실제 CLI는 여전히 **1/1**, 제외 0, **예, rc 0**이다.
- `good=<정상 root> empty=<빈 root>` 또는 존재하지 않는 두 번째 root를 명시해도 **1/1, 예, rc 0**이다. 빈 root 단독만 0/0·미완·rc 2다.

R7-01은 “존재하는 후보를 검증하다 제외한 경우”만 센다. inventory를 만들기 전에 state만의 dict로 축소하고, 아예 비어 있는 요청 root는 후보가 되지 않으므로 전건성이 합성되지 않는다.

**최소 닫힘 조건:** 파일 inventory를 축소 전에 만들고 `(root, state, half-cell source, Si, 실행 설정)`의 필요한 identity를 보존한다. 중복/모호함은 명시적으로 거부하거나 모델 층별 관측으로 남긴다. 명시한 root마다 expected/available/verified/excluded를 세는 roster 또는 manifest를 소비한다. 위 입력은 두 관측 또는 명시적 부분/모호함이어야 하며 `1/1·예`가 아니어야 한다.

### R8-02 · P1 · 정본 승인 — `check_u14`가 data B/meta A의 중단 상태와 낡은 provenance schema를 성공으로 인증한다

위치: [check_u14.py:19](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/check_u14.py:19), [109](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/check_u14.py:109), [114](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/check_u14.py:114), [121](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/check_u14.py:121), [129](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/check_u14.py:129).

재현:

```bash
python outputs/r8_inference_repros.py --target <a22da338/bms-balancing> --case unit
```

1. 정상 A/A data/meta를 준비하면 checker와 `read_unit` 모두 성공한다.
2. 같은 수치의 다른 정상 실행 B가 실제 atomic writer로 **data만** 교체하고 meta 전에 멈춘다.
3. `read_unit`은 `False: meta run_id와 JSON run_id 불일치`를 반환한다.
4. 같은 공개 checker는 **“새 스키마: 전부 갖췄다”, “숫자: 전부 같다”, rc 0**이다.
5. B meta를 완성하면 다시 정상이다.

checker는 data와 meta를 독립 pathname에서 읽고 필드 존재만 본다. 검증된 동일 묶음의 bytes를 소비하지 않는다. 또 `MATRIX_COLS`와 `PROFILE_COLS`가 R8 producer의 새 reference provenance 필드를 요구하지 않는다. 실제 current `out/`의 matrix 4개에는 `ref_inputs_sha`, `consumed_inputs`, `ref_consumed_inputs`가 없고 profile 4개에는 `ref_inputs_sha`가 없지만 checker는 “스키마 전부 갖춤”이라고 한다. R7와 data bytes가 같다는 관측은 맞지만, 그것은 새 schema가 현재 정본에 생겼다는 뜻이 아니다.

**최소 닫힘 조건:** current 산출은 `read_unit`이 한 번에 돌려준 동일 data/meta snapshot만으로 schema와 수치를 검사한다. `run_id`, artifact hash, meta binding 불일치는 nonzero다. producer schema와 checker의 required schema를 한 정본에서 생성하거나 대조한다. 과거 누락을 현재 pathname 해시로 소급 채우지 말고, 실제 새 실행으로 별도 destination에 만든 뒤 비교·승격하거나 current 정본을 명시적으로 provenance-incomplete로 제한한다.

### R8-03 · P1 · 부분집합 결론 — `ne_shape`가 100 mV를 기록하고도 stdout에서 “측정 최대 10 mV”로 요약하고 rc 0으로 끝난다

위치: [ne_shape.py:247](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/ne_shape.py:247), [264](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/ne_shape.py:264), [328](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/ne_shape.py:328), [334](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/ne_shape.py:334), [340](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/ne_shape.py:340), [397](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/ne_shape.py:397).

재현:

```bash
python outputs/r8_inference_repros.py --target <a22da338/bms-balancing> --case shape
```

실제 reader·Blend·집계·CSV/meta publisher를 사용하고 전극 로더만 결정적 합성 입력으로 바꿨다. state100의 측정 변화는 10 mV이고 matrix gamma pair가 있다. state200의 측정 변화는 100 mV지만 matrix만 아직 없다.

```text
CSV: state100 measured=10, gamma=.25
CSV: state200 measured=100, gamma=<빈칸>
요약: 측정된 음극 모양 변화 최대 10.00 mV
process rc=0, 게시 unit read_unit=True
```

state200 matrix pair만 추가하면 같은 측정에서 요약이 100 mV가 된다. 코드는 `ok = ratio가 NaN이 아닌 행`을 만든 뒤 **측정값의 최대까지 그 부분집합에서** 계산한다. CSV에 누락 행이 보인다는 점은 인정하지만, 최종 성공 요약은 paired subset의 범위를 말하지 않는다.

**최소 닫힘 조건:** 측정 통계는 모든 측정 row에서 계산하고, gamma-paired 통계는 requested/available/paired 상태 수와 목록을 별도로 표시한다. 요청된 paired 분석에 누락이 있으면 partial/nonzero 또는 계약된 명시적 부분 모드여야 한다. 미계산과 합법 범위를 탐색했으나 증인이 없는 상태도 구분한다.

### R8-04 · P1 · provenance 보존 — profile의 전체 입력 identity가 실패 재시도 한 번에 사라지는 `.log`에만 있다

위치: [verify.py:1557](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/bms_balancing/verify.py:1557), [1571](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/bms_balancing/verify.py:1571), [1595](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/bms_balancing/verify.py:1595), [run_states.sh:145](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/run_states.sh:145), [154](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/run_states.sh:154), [218](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/run_states.sh:218).

재현:

```bash
python outputs/r8_claims_repros.py --target <a22da338/bms-balancing> --case profile
```

실제 optimizer로 정상 profile 3행을 만든다. CSV에는 target/ref aggregate hash 두 개만 있고, 각 입력 파일의 역할·path·sha256 전체 mapping은 stdout의 `SUMMARY`에만 있다. wrapper는 이를 고정 `.csv.log`에 쓴다. 다음 정상 재시도가 입력 root 부재로 rc 1이 되면 redirect가 먼저 log를 잘라낸다. 이전 CSV/meta는 보존되고 `read_unit=True`지만, 그 묶음을 만든 target/ref 전체 identity는 더 이상 회수할 수 없다.

이는 숫자가 틀렸다는 반례가 아니라 **R7-03이 요구한 출처를 검증 묶음 밖에 둔 반례**다. aggregate hash만으로는 어떤 원시 입력 역할의 어떤 bytes였는지 복원·감사할 수 없다. 현재 canonical `out/`에는 profile log도 없다.

**최소 닫힘 조건:** target/ref 전체 input identity를 CSV 자체, 검증된 meta, 또는 CSV와 함께 atomic하게 게시·검증되는 typed sidecar에 둔다. 실행 log를 durable receipt로 사용하지 않는다. 실패 재시도 뒤에도 기존 정상 unit과 그 receipt가 함께 남거나, 둘 모두 명시적 미완이어야 한다.

## 3. 새 P2 네 조건

### R8-05 · P2 · 수치 비교 증거 — 중복 row가 달라진 수치를 숨긴다

위치: [check_u14.py:70](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/check_u14.py:70), [140](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/scripts/check_u14.py:140).

재현:

```bash
python outputs/r8_inference_repros.py --target <a22da338/bms-balancing> --case rows
```

정본 matrix 32행에 같은 `(half_cell, si, w_dqdv)` key의 행을 하나 더 넣되, 먼저 오는 중복행의 LLI를 +3%p 바꾼 33행 정상 unit을 만든다. 실제 `compare_states`의 GITT LLI 폭은 **1.2650629 → 3.6914520**로 움직인다. `check_u14`는 dict comprehension이 마지막 원본행으로 앞의 변경행을 지워 **“숫자 전부 같다”, rc 0**이다. 마지막 원본 중복행만 제거하면 같은 변경을 잡아 rc 1이 된다.

**최소 조건:** dict 변환 전에 key 유일성·행 수·exact key set을 검사한다. 반복이 합법이면 replicate identity를 schema에 넣고 모든 행을 비교한다.

### R8-06 · P2 · 변이 감사 — 선택된 시험 0개를 CAUGHT로 인증한다

위치: [codex_r6_mutation_audit.py:48](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/reviews/r6_repros/codex_r6_mutation_audit.py:48), [58](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/reviews/r6_repros/codex_r6_mutation_audit.py:58).

실제 감사의 MUTATIONS를 임시 사본에서 한 개의 무해한 주석 변이와 존재하지 않는 selector `c6_DOES_NOT_EXIST`로 제한했다.

```text
pytest: 52 deselected, rc 5
auditor: CAUGHT ... 52 deselected
MISSED: 0
process rc: 0
```

같은 무해한 변이에 실제 `c6_04` selector를 주면 1 passed → MISSED 1 → rc 1이다. 현재 등록된 8개는 실제로 모두 pytest rc 1이었으므로 그 숫자를 부정하지 않는다. 문제는 앞으로 생길 selector 오타·rename·수집 실패를 assertion 검출과 구분하지 못한다는 것이다.

**최소 조건:** 선택·수집된 시험 수가 0보다 큼을 확인하고, pytest rc 5 및 수집/실행 오류를 CAUGHT가 아닌 감사 오류로 분류한다. 기대 node ID와 실패 원인을 transcript에 남긴다.

### R8-07 · P2 · 재현 문서 — 보관 probe는 SHA를 올바르게 거부하지만 post-fix 폐쇄 주장을 재생할 명령이 없다

위치: [harness_r7_port_repros.py:23](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/reviews/r7_repros/codex/harness_r7_port_repros.py:23), [163](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/reviews/r7_repros/codex/harness_r7_port_repros.py:163), [R8_REQUEST.md:32](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/reviews/R8_REQUEST.md:32), [48](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/reviews/R8_REQUEST.md:48), [52](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/reviews/R8_REQUEST.md:52).

R8 checkout에서 요청문 명령을 그대로 실행했다.

```bash
python3 reviews/r7_repros/codex/harness_r7_port_repros.py --target . --case controls
```

runner가 R7 SHA `521be85…`를 고정해 두었으므로 현재 SHA `a22da338…`에서 첫 SHA assertion으로 rc 1이다. 이는 보관된 pre-fix probe의 올바른 동작이며 요청문 32행도 pre-fix 재현에는 521 worktree가 필요하다고 말한다. 문제는 같은 요청문 48·52행이 “위 다섯 명령을 수정 뒤에 재실행했고 각자 자기 반례 assertion에서 실패했다”고 주장하지만, 그 **post-fix 폐쇄 주장을 재생할 명령은 제공하지 않는다는 것**이다. `--case controls`도 baseline 기본값을 재는 R7-05 경로는 아니다. 독립 adapter와 `test_d7_05/d7_06`으로 수정 자체가 닫혔음은 별도로 확인했다.

**최소 조건:** 원본 R7 pinned probe는 보존하고, R8용 closure runner를 따로 제공한다. 대상 검증 뒤 실제 case에 도달했는지, 반례 assertion에서 실패했는지, positive closure가 성립했는지를 별도 상태로 기록한다.

### R8-08 · P2 · 경쟁순서 증거 — c6_01의 metadata 두 schedule은 callback을 꺼도 통과한다

위치: [test_r6_internal.py:964](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/tests/test_r6_internal.py:964), [1017](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/tests/test_r6_internal.py:1017), [1028](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r8-target-wsl/bms-balancing/tests/test_r6_internal.py:1028).

임시 사본에서 `_hook_open`의 callback만 다음처럼 제한했다.

```python
if n["v"] == k and not target_name.endswith(".meta.json"):
    on_k()
```

metadata data/meta 경계의 두 게시 callback이 실행되지 않지만 `test_c6_01`은 **1 passed, rc 0**이다. 전체 callback을 모두 끄면 `seen={'attempt-A'}`에서 실패하므로 R7이 지적한 “주입 전부 OFF도 통과” 문제는 닫혔다. 남은 문제는 `fired["v"]`가 callback 횟수가 아니라 read 횟수여서 metadata schedule의 무실행을 증명하지 못하고, 다른 schedule이 필요한 B/B·미완 관측을 대신 채운다는 점이다.

이는 새 production TOCTOU 반례가 아니라 각 경쟁 schedule을 실행했다는 증거의 false-positive다.

**최소 조건:** callback에서 별도 publication count/flag를 세고 각 case가 자신의 callback을 정확히 실행했음을 assert한다. schedule별 예상 publication ID와 관측을 따로 기록해 다른 case의 합집합이 가리지 못하게 한다.

## 4. R7 조건별 판정

| R7 조건 | R8 판정 | 근거 |
|---|---|---|
| R7-01 집계 미완 전파 | **부분** | 기존 `아니오→미완→아니오`와 단일 빈 root는 닫힘. 같은-state Si collision과 여러 요청 root의 부재는 모집단에서 사라짐(R8-01) |
| R7-02 noise 같은 snapshot | **닫힘** | 실제 optimizer에서 build A 뒤 정상 B re-export를 해도 전체 noise JSON이 A/A와 동일. B/B는 수치와 digest가 함께 변함 |
| R7-03 target/ref 출처 | **부분** | future matrix 행은 실제 A/B build identity를 모두 정확히 기록. profile 전체 identity는 소모성 log뿐(R8-04), current canonical은 새 열 미보유인데 checker가 완전이라 함(R8-02) |
| R7-04 current/historical policy | **닫힘** | 두 정책이 실제로 갈리고 선택 정책·건너뛴 sibling을 출력. 손으로 푼 역사 디렉터리의 의도를 자동 추측하지 못하는 것은 아래 정책 권고 |
| R7-05 baseline 부재 | **닫힘** | 미지정은 명시적 부분 5+1, 올바른 baseline 지정은 full 6/6. 현재 API로 독립 재현 |
| R7-06 MISSED 종료 코드 | **닫힘, 감사 분류는 부분** | 실제 선택된 no-op은 MISSED·rc 1. 단 시험 0개/rc 5도 CAUGHT·rc 0(R8-06) |

R8이 같이 닫았다고 한 증거 강화 두 주장에는 한정이 남는다.

- c6_04 mutant는 아직 stale 값 `222`와 정상 `111`의 수치 assertion까지 가지 않고 `KeyError: '100'`에서 실패한다. `_v2` 이름이 parser에서 state를 없애기 때문이다. R7에서 이미 지적한 축이므로 새 발견으로 재계수하지 않았지만, “이제 값으로 잡힌다”는 R8 주장은 실제 transcript와 다르다.
- `test_c6_01`의 남은 개별 schedule false-positive는 새 P2 R8-08로 계수했다.

## 5. 요청문의 질문에 대한 답

1. **미완 전파가 빠진 소비자:** `compare_states`의 full identity/roster, `ne_shape`의 paired subset, `check_u14`의 atomic unit·schema·duplicate가 빠졌다. 정적 문서 표는 생성 경로가 모집단 receipt를 소비하지 않는 한 코드 회귀만으로 완전성이 증명되지 않는다.
2. **두 번 읽기:** R7-02의 noise와 기존 build 네 입력, `ne_shape`의 half-cell 값/용량/identity는 같은 bytes로 닫혔다. 새로 확인한 핵심은 profile receipt의 내구성이다. 과거 matrix γ를 현재 다른 literature export에 대입하는 `ne_shape`는 양쪽 직접 입력을 정직하게 기록하지만 재적합하지 않는다. 이는 아래 정책을 명시해야 할 sensitivity 경계이지 이번에 별도 P1로 세지 않았다.
3. **target/reference export 정책:** 같은 실험의 기본 비교는 공유 workbook/literature에 대해 **공통 snapshot을 강제**하는 편이 맞다. 서로 다른 export는 명시적 sensitivity/counterfactual 모드에서만 허용하고, 양쪽의 회수 가능한 receipt와 라벨을 durable unit에 보존한다. 조용한 혼합은 허용하지 않는다.
4. **`baseline-policy=auto`:** 손으로 푼 옛 `out/`을 `--old`로만 주면 current로 분류할 수 있다. 현재는 정책을 출력하고 시험한 예에서는 차이를 잡으므로 새 P1은 아니다. 그래도 `--old-rev` 없는 외부 baseline은 explicit policy를 요구하거나 baseline manifest의 revision을 읽는 편이 안전하다.
5. **U16·U17 순서:** 원인 귀속을 써야 하는 결정이 임박했다면 U16 구판 환경 통제 재실행을 먼저 하되 source·environment·input·seed·budget receipt를 보존한다. U17 endpoint-witness schema는 다음 계획 실행에 추가한다. U16과 한정된 요구서 초안을 전체 U17 구현의 독립 선행조건으로 만들 필요는 없으며, 어느 재실행도 current canonical을 바로 덮지 않는다.
6. **다섯 관측을 요구서로 옮길 때:** 각 행에 모집단/roster와 completeness, target/reference 입력 receipt, 관측 범위, 후보 모델 변경, 대안 가설, 구분 실험, 채택·기각 임계값, 실패/미계산 의미, evidence version을 둔다. 포팅 일치·부호 산술·탐색 하한·기술 통계·γ 진폭 증인은 서로 다른 증거 층이며 원인·식별성·수렴 증명으로 승격하지 않는다.

## 6. GO를 위한 최소 조건과 다음 순서

다음 1–5가 이번 판정의 GO 조건이다.

1. R8-01의 모집단 identity와 explicit roster를 넣고, 두 정상 Si collision 및 `good+empty`가 조용한 전건 성공이 아님을 회귀로 고정한다.
2. `check_u14`가 verified snapshot만 소비하게 하고 data/meta crash schedule, required provenance schema, duplicate key를 fail-closed로 만든다.
3. `ne_shape`의 measured 전체와 gamma-paired 부분집합을 분리하고 incomplete 상태를 결과 schema와 종료 코드까지 전파한다.
4. profile의 full target/ref input identity를 atomic durable unit에 넣는다. current canonical의 provenance 누락은 실제 재실행으로 보강하거나 명시적으로 historical/incomplete로 범위를 제한한다.
5. mutation auditor의 no-tests 상태와 R8용 replay 도달 증거를 고친다. c6_04는 실제 stale 수치 비교에 도달하고 c6_01은 callback별 주입을 증명해야 한다.
1–5 전에는 일반 **GO가 아니다**. 단, §5의 한정어와 위 미결을 요구사항으로 명시한 설계 문서 초안은 진행 가능하다.

GO와 별개의 다음 실행 조건으로, 다음 계획된 production 실행에는 U17 endpoint-witness schema를 얹는다. 결정이 임박한 U16 통제 재실행은 최소 source/environment/input/seed/budget receipt와 별도 destination을 갖추고 먼저 수행할 수 있다.

## 7. 재현물

- [통합 재생기](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r8_replay.py)
- [통합 원시 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r8_replay_results.json)
- [수치·집계 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r8_inference_repros.py) · [독립 검토](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r8_inference_review.md)
- [입력·출처 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r8_claims_repros.py) · [독립 검토](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r8_claims_review.md)
- [포팅·변이 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r8_port_repros.py) · [독립 검토](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/r8_port_review.md)
