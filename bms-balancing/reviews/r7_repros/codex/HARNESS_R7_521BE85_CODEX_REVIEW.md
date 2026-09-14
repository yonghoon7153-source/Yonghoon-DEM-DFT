# α·β 검증 하네스 R7 — Codex 최종 리뷰

## 판정: NO-GO

대상: **`521be85e74acef80feec45bd147dd339e25b8d0a`**, 브랜치 `claude/bms-alpha-beta-verify`, `bms-balancing/`만. 첨부 `R7_REQUEST (1).md`와 저장소 요청문이 일치함을 확인했다. 코드 수정 커밋은 `4396a54`이고, 그 위 요청문·재현 패키지가 추가된 HEAD를 검토했다.

**R6의 원래 반례들은 닫혔다. 그러나 개별 snapshot을 올바르게 읽은 다음 단계에서 전체 결론·잡음 진단·기준 입력 출처가 아직 이어지지 않는다.** 새 P1은 세 조건이다. 보조 P2는 세 건이며, 질문 전제 오류 한 건은 별도로 정정한다.

이번 NO-GO는 **하네스의 일반 성공 판정을 그대로 새 모델의 확정 설계 근거로 채택하는 것**에 대한 판단이다. 커밋된 수치 관측이 틀렸다고 소급 판정하지 않는다. §5의 한정어를 유지한 **새 모델 요구서 초안은 지금 진행 가능**하다. 이전 degradation 게이트나 보안·실물 운용 승인과는 별건이다.

## 1. 직접 실행한 증거

원본 소스는 수정하지 않았다. 별도 fresh checkout에서 LF를 유지했고, 최종 실행 전·후 대상은 clean이다. 변이 감사는 **별도 임시 Git 사본**에서만 실행했다. 입력 교체는 저장소 생성기로 만든 합성 XLSX/CSV에만 했다.

| 실행 | 직접 관측 |
|---|---|
| 전체 회귀 | **139 passed**, 실패 0 |
| `matlab/tests/run_all.sh` | rc 0, 단계 4·5 통과. **이 환경에는 Octave가 없어 1–3은 미실행** |
| 실제 `compare_states` | rc 0 |
| 독립 snapshot 경계 대조 | JSON/CSV × 읽기 전후 등 5경계 × 완전/부분 게시 = **20개 순서**, 모두 A/A·B/B·미완 |
| 현행 metadata 미완 | 없음/옛 meta를 세 독자가 모두 거부. 정상 묶음·진짜 legacy 양성 대조 통과 |
| 실제 `build` 입력 | 풀셀·반쪽전지·문헌 Si·Gr 각각 한 번 읽고, 재-export 중에도 배열/해시 A/A |
| 자체 변이 감사 | **8/8 CAUGHT**, 복구 후 7 passed |
| 적응판 변이 감사 | **5/5 CAUGHT**, 복구 후 6/6 |
| 적응판 재생 | 올바른 과거 baseline 지정 시 **6/6**. 요청문 그대로 환경 미지정 시 **5/6·rc 1** — R7-05 |
| precision/Q3 선택 회귀 | **9 passed** |

Python 3.12.3 / NumPy 2.5.3 / SciPy 1.18.1 / pandas 3.0.5 / openpyxl 3.1.5 / pytest 9.1.1, WSL에서 실행했다. 원자료·원본 MATLAB을 독립 재실행한 것은 아니다. 요청문의 Octave 실측과 이 환경의 단계 4·5 실행을 합쳐 “독립 MATLAB 전수 통과”로 쓰지 않았다.

[최종 원시 로그](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_replay_results.json)에 명령·시간·stdout/stderr·정확한 SHA·재현 파일 해시·실행 중 파일 불변 여부를 보관했다. 재현 스크립트 rc 0은 **예상한 반례도 관측했다**는 뜻이지 GO가 아니다.

## 2. 새 P1 세 조건

### R7-01 [P1 · 집계 결론] 반례인 상태가 미완으로 제외되면 “아니오”가 “예”로 바뀐다

위치: [compare_states.py:122](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/scripts/compare_states.py:122), [126](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/scripts/compare_states.py:126), [180](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/scripts/compare_states.py:180), [184](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/scripts/compare_states.py:184).

재현: [execution 스크립트](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_execution_repros.py)의 `aggregate_incomplete_counterexample`.

```bash
python /path/to/review/harness_r7_execution_repros.py \
  --target /path/to/521be85/bms-balancing
```

실제 atomic JSON writer와 `run_states.sh`의 실제 metadata helper로 다음 두 정상 상태를 만든다. 반례용 공개 스키마 수치이며 실제 전지의 관측이라고 주장하지 않는다.

| 상태 | LAM_PE 폭 | LAM_NE 폭 | LLI 폭 |
|---|---:|---:|---:|
| 100 | 2 | 3 | 1 |
| 200 | 1 | 2 | 9 |

두 묶음이 정상일 때 실제 공개 CLI는 **“LLI가 항상 가장 좁은가: 아니오”**, rc 0이다.

그 뒤 상태 200의 다른 정상 시도가 **data만 게시**하고 meta 전에 멈춘다. 수치 자체는 그대로다. `read_unit`는 이 미완을 정확히 거부한다. 그런데 상위 보고서는 200을 제외하고 다음을 출력한다.

```text
stderr: degeneracy_200_Li.json … 묶음 불일치/미완 … 표에서 뺀다
stdout: A 축에서 LLI 가 **항상 가장 좁은가**: 예
exit code: 0
```

meta를 완성하면 같은 CLI가 다시 **아니오**, rc 0이다. 빈 디렉터리도 “예”, rc 0이라는 보조 대조를 확인했다.

이는 F01b의 “이전 정상 묶음을 복원하지 않는다”와 다르다. **이전 묶음을 보존하지 않아도 된다. 다만 현재 비교가 미완임을 전체 결론까지 전달해야 한다.** 현재 코드는 성공 플래그를 True로 시작하고, 거부된 상태를 지운 뒤 남은 부분집합만으로 전체처럼 읽히는 긍정 판정을 한다. 경고가 존재한다는 사실은 인정하지만, 최종 판정·종료 상태가 그 미완을 표현하지 않는다.

**최소 닫힘 조건:** 후보/요구 대상, 검증한 대상, 제외한 대상을 구분하여 집계한다. 미완 상태가 있거나 관측이 0개면 전체 “항상 예” 판정을 내리지 말고 미완/부분 판정과 그에 맞는 반환 상태를 낸다. 부분집합 분석을 지원한다면 그 범위·n을 명시하고 전체 조건의 성공과 구분한다. 위 일정은 **아니오 → 미완 → 아니오**여야 하며, 과거 묶음 자동 복원은 필수 해법이 아니다.

### R7-02 [P1 · 입력 결속] noise가 A 적합 잔차를 B의 잡음으로 나눈다

위치: [verify.py:1700](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/bms_balancing/verify.py:1700), [1703](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/bms_balancing/verify.py:1703), [1728](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/bms_balancing/verify.py:1728), [1735](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/bms_balancing/verify.py:1735).

재현: [claims 스크립트](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_claims_repros.py).

```bash
python /path/to/review/harness_r7_claims_repros.py \
  --target /path/to/521be85/bms-balancing --case noise
```

GITT/Li/상태 200/w=0, starts=2, seed=0의 합성 입력에서 실제 `cmd_noise`, Objective, SciPy 최적화를 실행했다. 적합 반환값을 임의 수치로 대체하지 않았다.

`build(A)`가 끝난 직후 같은 풀셀 workbook의 상태 200 전압에 seed 731·σ=0.020 V의 합성 잡음을 더해 정상 재-export B를 한다. `cmd_noise`는 이후 경로를 다시 열어 B로 잡음을 계산한다.

| 직접 관측 | A/A | 중간 재-export A/B | B/B |
|---|---:|---:|---:|
| misfit RMSE (V) | 0.02887618 | **0.02887618** | 0.02594162 |
| σ at k=1 (V) | 0.0000133473 | **0.0181957740** | 0.0181957740 |
| misfit/σ | 2163.4511 | **1.5869717** | 1.4256947 |

중간 산출은 A의 분자와 B의 분모이며 **어느 일관된 실행의 값도 아니다**. 진단 문장도 “거짓으로 좁은 구간”에서 “likelihood 기반 구간을 논의할 여지”로 바뀐다. 단 B/B도 후자의 분기이므로, 그 분기 자체가 정상 B의 판정과 반대라고 주장하지 않는다. 확인한 것은 입력 혼합과 그 혼합이 표시되지 않는다는 점이다.

`InputBytes`는 한 로더 호출 안에서는 맞게 작동한다. 그러나 호출자가 다른 `load_full_cell()`을 실행하므로 첫 Objective의 snapshot과 두 번째 raw noise의 snapshot이 분리된다. noise JSON에는 이 두 입력의 identity도 없다.

**최소 닫힘 조건:** 같은 풀셀 snapshot에서 Objective용 배열과 잡음용 원시 capacity/voltage를 함께 공급하고 그 identity를 기록한다. 잡음용 원시 배열을 평활·재표본 배열로 대체하여 계산 정의를 바꾸면 안 된다. 위 경계의 정상 재-export에서 A/A 또는 명시적 재시작만 허용한다. 두 별개 관측을 의도적으로 섞는 모드라면 각각의 입력·의미를 명시해야 하며, 현재의 “같은 측정에 대한 진단”과 구별해야 한다.

### R7-03 [P1 · 기준 입력 출처] matrix 행은 reference를 소비하지만 그 입력 서명을 보존하지 않는다

위치: [verify.py:1366](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/bms_balancing/verify.py:1366), [1374](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/bms_balancing/verify.py:1374), [1382](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/bms_balancing/verify.py:1382).

```bash
python /path/to/review/harness_r7_claims_repros.py \
  --target /path/to/521be85/bms-balancing --case matrix
```

실제 최적화를 GITT/Li/w=0 한 조합으로 제한하여 두 일정을 재현했다.

**① 기준 전용 파일 변경:** target 입력 네 개는 그대로 두고 pristine half-cell의 PE만 +20mV 재-export한다. CSV의 target `inputs_sha`는 같지만 LAM_NE는 **2.84975495 → 3.84787136%**, LAM_PE는 **10.35858680 → 11.06478725%**로 바뀐다. 내부 reference `inputs_sha`는 변했으나 행에는 reference 입력 서명/identity 필드가 없다.

**② 공유 workbook 중간 재-export:** pristine A를 만든 직후 같은 풀셀 workbook의 pristine 전압 열만 +20mV 바꾸고, target 200은 B에서 읽는다. 이후 B/B로 일관되게 한 번 더 실행한다.

| 직접 관측 | reference A / target B | B/B |
|---|---:|---:|
| target a_NE | 1.1045322378 | 1.1045322378 |
| reference a_NE | 1.0111329056 | 1.0380391314 |
| LAM_NE (%) | **2.8497549512** | **5.3679128420** |
| 게시된 target inputs_sha | **같은 B 서명** | **같은 B 서명** |

**target digest가 틀렸거나 해시 충돌이 난 것이 아니다.** target 서명은 맞고, 행의 다른 계산 입력인 reference 출처가 빠졌다. reference parameter·점수는 어떤 원자료 export를 소비했는지 대신 증명하지 않는다. 서로 다른 export 사용을 허용하는 설계도 가능하지만, 그 경우에도 입력 역할별 구분이 남아야 한다.

같은 target-only 기록은 [profile 경로:1551](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/bms_balancing/verify.py:1551)에도 정적으로 있다. profile 최적화까지 새로 재현했다고 세지 않는다. 반대로 [degeneracy JSON:518](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/bms_balancing/verify.py:518)은 `consumed_inputs`·`ref_consumed_inputs`를 둘 다 보존하며 이 양성 경로를 인정한다.

**최소 닫힘 조건:** matrix/profile에 target/ref 각각의 실제 소비 snapshot identity, 또는 둘 모두를 회수할 수 있는 입력 묶음을 보존한다. 공유 입력의 동일 export가 계약이면 같은 snapshot을 재사용/검사한다. 다른 export를 허용하면 양쪽을 명시한다. 위 두 일정에서 reference provenance가 달라져야 한다. 과거 누락된 기록을 현재 pathname 해시로 소급 채우면 안 된다.

## 3. 보조 P2 세 건

### R7-04 [P2 · 대조 정본] `--old`의 현행 디렉터리에도 역사 `_vN` 우선 규칙이 적용된다

위치: [check_u14.py:34](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/scripts/check_u14.py:34), [115](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/scripts/check_u14.py:115), [248](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/scripts/check_u14.py:248).

재현: [inference 스크립트](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_inference_repros.py)의 `--case baseline`.

```bash
python /path/to/review/harness_r7_inference_repros.py \
  --target /path/to/521be85/bms-balancing --case baseline
```

현재 디렉터리에는 정상 unversioned A, 남아 있는 `_v2`에는 B, 재실행 디렉터리에는 정상 unversioned B를 둔다. B의 LLI max·span을 함께 1%p 높여 범위 산술도 유지했다.

- 실제 현행 reader: `_v2`를 경고·제외하고 A의 span **0.5736895851**을 선택.
- `check_u14 --new rerun --old current`: `_v2`의 span **1.5736895851**을 선택하여 **“숫자: 정본과 전부 같다”**, rc 0.
- 출력은 여전히 “compare_states와 같은 규칙”이라고 한다.
- `_v2` 하나만 제거하면 같은 A/B 대조가 차이 2건, rc 1로 바뀐다.

현재 커밋의 `_v2`는 archive로 이동되어 있으므로 보존된 12개 산출의 동일성은 유지된다. 문제는 **두 선택 규칙의 실행상 구분이 아니라 docstring만 구분**되어 있다는 것이다.

최소 수정: 현행 `--old`에는 unversioned 규칙이나 sibling 거부를 적용하고, 명시된 역사 리비전 모드에서만 highest-version을 쓴다. 두 모드의 실제 선택 정책을 출력하고 각각 시험한다.

### R7-05 [P2 · 재생 명령] 과거 baseline을 지정하지 않으면 현재 디렉터리를 baseline으로 쓴다

위치: [replay_codex_r6_adapted.py:222](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/reviews/r6_repros/codex/replay_codex_r6_adapted.py:222).

```bash
env -u R6_OLD_OUT python3 reviews/r6_repros/codex/replay_codex_r6_adapted.py --target .
```

요청문에 있는 기본 호출은 이 환경에서 **5/6·rc 1**이다. 빈 환경 문자열을 `Path("")`로 바꾸면 `.`가 되고, 현재 디렉터리가 존재하므로 full inference를 `--old .`로 부른다. `old_m is not None` assertion이 실패한다.

같은 사본에서 `R6_OLD_OUT`을 실제 `bfc4623^/bms-balancing/out`으로 지정하면 **6/6·rc 0**이다. 따라서 이 실패를 R6 수정의 재개방이라고 해석하지 않았다.

최소 수정: 환경 문자열 부재를 경로 변환 전에 검사하고, full 재생은 실제 baseline을 명시적으로 요구한다. 부분 재생을 지원한다면 full 6/6과 구분한다. 요청문에 baseline 준비·지정 방법을 넣는다.

### R7-06 [P2 · 자동 검증] 변이 감사가 `MISSED: 1`이어도 rc 0이다

위치: [codex_r6_mutation_audit.py:42](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/reviews/r6_repros/codex_r6_mutation_audit.py:42), [49](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r7-target/bms-balancing/reviews/r6_repros/codex_r6_mutation_audit.py:49).

[port 스크립트](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_port_repros.py)의 `--case controls`가 독립 임시 사본에서 재현한다.

```bash
python /path/to/review/harness_r7_port_repros.py \
  --target /path/to/521be85/bms-balancing --case controls
```

감사 목록에 의도적으로 잡히지 않는 한 후보를 주는 음성 대조다. 현재 등록부가 no-op이라는 주장이 아니다. 원래 실행·복구·집계 흐름에서 결과는 다음과 같다.

```text
baseline: 0 7 passed
MISSED | Q3 … | 1 passed
restored: 0 7 passed
MISSED: 1
process rc: 0
```

최소 수정: 놓친 변이가 있거나 복구 후 회귀가 실패하면 비영 종료한다. collection/setup 오류와 해당 assertion 실패도 구분한다. **현재 실제 8개는 모두 CAUGHT였으므로 이 발견으로 그 8/8 관측을 취소하지 않는다.**

## 4. R6 대응과 회귀의 실제 강도

| R6 조건 | R7 판정 | 직접 근거 |
|---|---|---|
| 01 검증한 snapshot만 소비 | **원래 반례 닫힘** | 20개 순서에서 A/A·B/B·미완만. 별도 상위 집계 문제는 R7-01 |
| 02 현행 미완을 legacy로 소비 금지 | **닫힘** | meta 없음/옛 meta 모두 세 독자 거부. 진짜 legacy는 호환 |
| 03 실제 읽은 입력을 해시 | **build·ne_shape 원래 반례 닫힘 / 전체 소비는 부분** | 네 입력과 다중 소비는 한 번 읽음. noise 재개방·reference 기록 누락은 R7-02·03 |
| 04 현행 정본 선택 | **현행 reader 닫힘** | unversioned 선택·archive 경고·실제 12개 unit True. 재실행 comparator는 R7-04 |
| 05 arrow 파일명 분류 | **닫힘** | arrow·한글 출력 모두 정확히 output 분류 |
| 06 γ profile 시작 수 | **25회 정정 닫힘** | 84행 전부 n_tried=25, 실제 코드와 일치 |
| Q3 정밀도 충돌 문구 | **닫힘** | 같은 값 complete/다른 값을 느슨한 옵션이 흡수하면 partial, 문구·회귀 일치 |

변이 증거는 전체를 “공허하다”고 판정하지 않았다. 다만 다음 두 한정은 필요하다.

- `test_c6_01`의 주입을 꺼도 단일 시험은 통과한다. `{A,B} & seen`은 두 결과를 모두 요구하지 않는다. **적응판은 switched/published를 검사하고 실제 변이도 잡으므로** 묶음 증거가 이를 보완한다. 단일 회귀에는 주입 발생·필요 관측을 직접 assert하는 것이 좋다.
- 자체 감사의 c6_04 변이는 stale 수치가 소비되어 틀린 값을 잡은 것이 아니라, filename 처리 때문에 state가 사라져 `KeyError`로 잡혔다. 8개 모두 collection/setup 오류는 아니지만, 이 한 출력을 “옛 값을 실제 소비한 반례 검출”로 확대하면 안 된다.

R3 §5/R5 §4로 되돌아가면, 원인·표현의 주요 철회와 192 원시값 회귀는 유지된다. 비교 schema/precision의 확인한 지원 범위도 유지된다. **실행 결과·소비 입력의 결속 및 집계 완결성은 새 P1 세 조건 때문에 부분**이다.

## 5. 보존된 관측과 질문 답변

### 이번에도 유지된 수치

| 대조 | 직접 확인 |
|---|---|
| 현행 U14 data 12개 | `d431404`와 **바이트 동일**, 현행 unit 검증 모두 True |
| matrix 공통 수치 | 역사 baseline과 **2,240칸 정확히 동일** |
| degeneracy 폭 | **12개 span 정확히 동일** |
| FINDINGS §5 인쇄 표 | **35칸** 현재 CSV 반올림과 일치 |
| γ profile | **84행, γ당 25회 시도** |
| §5-1 | n=6/10/12/13, γ 범위 동일. 폭·최악 비는 **인쇄 자릿수에서 동일** |
| U13 | 18줄·54 metric, eps_rel 약 4.74e−16~1.71e−15. root 집합 독립 증명은 아님 |

과거 profile 개별 행의 차이나 U16 원인 미확정을 없앤 것은 아니다. 25회였다는 사실만으로 “시작 예산이 충분했다”거나 “실제 차이는 ULP 때문”이라고 단정할 수 없다. `FINDINGS`·원장에 남은 확정형 문구는 다음처럼 좁히는 것이 맞다.

> 두 산출의 γ profile은 모두 25회 시작을 사용했다. 같은 예산 아래 일부 행이 달랐고 원인은 U16 미확정이다. 보존된 두 실행에서 본문 인쇄 정밀도의 해당 집계는 유지됐다.

이는 U16을 새 발견으로 다시 세는 것이 아니라, 신고한 불확실성과 확정 문구를 일치시키라는 권고다.

### Q1 — read_unit의 snapshot 규약은 닫혔는가?

검사한 정상 게시 일정에서는 **닫혔다**. 검증 후 B가 게시되어도 반환된 A/A를 소비하는 것이 올바르다. “항상 최신 파일”까지 요구할 필요는 없다. 다만 성공한 개별 묶음만 남긴 후 전체를 성공으로 판정하는 R7-01은 별도로 닫아야 한다.

### Q2 — 남은 입력 재개방과 사전 hash의 권위는?

남은 실제 경로는 R7-02이고, 다른 입력 역할의 기록 누락은 R7-03이다.

질문의 **“run_states.sh의 실행 직전 inputs_sha”는 현재 코드에 없다.** 해당 문자열은 0회이며, 실행 직전에는 `LAST_PRE_PV`의 Git 상태·시각을 채집한다. 입력 서명은 각 `build()`가 실제 소비 snapshot으로 만든다. 따라서 현행 코드에 존재하지 않는 두 hash의 충돌을 만들어 판정할 수는 없다. 이 전제 정정은 독립 코드 결함 수에 추가하지 않았다. 향후 사전 입력 승인을 설계한다면 소비 snapshot과의 연결을 별도 계약으로 정의해야 한다.

### Q3 — F01b, 마지막 온전한 묶음 보존까지 필요한가?

**아니다.** 재실행 비용을 수용하고 미완이 독자·집계·공개 판정까지 전파되면, 이전 묶음 자동 복원은 가용성 개선이며 새 GO 전제가 아니다. 이번 R7-01을 “그러니 불변 generation부터 만들어야 한다”로 확대하지 않는다.

### Q4 — 두 정본 선택 규칙의 공존은 가능한가?

목적과 호출 모드가 분리되면 가능하다. 현행은 unversioned, 역사 리비전은 당시 규칙으로 읽는 것이 자연스럽다. 현재는 일반 `--old`에서도 역사 규칙을 쓰므로 R7-04를 고쳐야 “분리되어 있다”고 할 수 있다.

### Q5 — U17 스키마를 위해 지금 재실행해야 하는가?

**설계 초안보다 앞선 의무 실행으로 요구하지 않는다.** 현재는 탐색 하한·끝점 재확인으로 인용한다. 다음 계획된 실행에서 parameter·J·limit·제약 잔차·seed·실제 입력 identity를 함께 보존하면 된다.

지금 재실행한다면 기존 정본을 먼저 덮지 말고 별도 위치에서 비교한다. “스키마 추가뿐이니 어떤 환경에서도 수치가 반드시 비트 동일”하다는 일반 보장은 없다. 같은 입력·환경·시작점 조건을 고정하고 동등성을 측정해야 한다.

### Q6 — 다섯 관측을 요구서에 옮겨도 되는가?

**한정어를 그대로 붙인 관측 열은 지금 작성 가능하다.**

1. 192 raw값의 경험적 일치 / 사용자 원본 식 대조 / U13 scale 상대근사는 서로 다른 증거 층.
2. 음수 LAM_NE는 공개 5행·고정 reference의 부호 산술. 경계 변경 재적합의 인과는 미확립.
3. 파우치 순위는 지정 네 상태·소스·설정의 탐색 하한 순위. 정확도·식별성 보증 아님.
4. 원통형/PE는 집합·분모·raw max/max 10.5를 명시한 기술값.
5. 잔차/γ는 선택된 쌍·고정 reference의 표집·진폭 증인·끝점 재확인. 원인·보상 경로·모양 적합·독립 수렴의 증명이 아님.

관측 옆에 후보 모델 변경, 대안 가설, 구분 실험 및 채택/기각 기준을 별도 항목으로 둔다. 특정 새 모델의 필요성이나 우월성을 이미 확정한 전제로 쓰지 않는다.

## 6. GO를 위한 최소 다음 조건

1. **R7-01:** 현행 산출이 미완/제외되면 전체 집계도 미완이며, 부분집합 또는 빈 집합을 전체 “예”로 인증하지 않는다.
2. **R7-02:** noise의 적합·잡음 계산이 동일한 원시 입력 snapshot을 소비하고 이를 기록한다.
3. **R7-03:** matrix/profile의 target와 reference 양쪽 실제 입력 출처를 보존한다.

P2 세 건과 질문 전제·인과 문구는 작은 코드/문서 수정으로 정리할 수 있다. 원자료가 없다는 이유로 새 큰 실행을 먼저 요구하지 않는다.

**최종 NO-GO.** 원래 수정의 닫힘은 인정하며, 새로 확인한 것은 그 다음 소비·집계 단계다. 한정된 다섯 관측에 기반한 설계 요구서 초안은 병행 가능하다.

## 재현 패키지

[통합 재생](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_replay.py)은 대상 SHA를 검사하고, 실행 전후 원본 상태 및 재현 스크립트 해시가 달라지지 않았는지 확인한다. 다음은 Linux/WSL에서 의존성을 설치·활성화한 상태의 호출이다.

```bash
python /path/to/review/harness_r7_replay.py \
  --target /path/to/521be85/bms-balancing \
  --old /path/to/extracted-bfc4623-parent/bms-balancing/out \
  --previous /path/to/d431404/bms-balancing \
  --output /tmp/r7-review.json
```

`--old`는 `bfc4623^`에서 Git archive로 추출한 **out 디렉터리**다. `--previous`는 12개 파일의 R6 대비 바이트 대조용이다. 이 환경에서는 이전 리뷰에서 추출해 둔 읽기 전용 baseline과 R6 checkout을 사용했다. `--baseline-only`는 기본 회귀·스모크만 실행하는 축소 모드이며 전체 리뷰 재생으로 표시하면 안 된다.

- [원시 통합 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_replay_results.json)
- [독자·집계 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_execution_repros.py)
- [입력·reference 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_claims_repros.py) · [담당 보고](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_claims_review.md)
- [수치·정본 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_inference_repros.py) · [담당 보고](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_inference_review.md)
- [적응판·변이 재현](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_port_repros.py) · [담당 보고](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r7_port_review.md)

변이 원문 pytest와 probe 출력도 통합 결과의 port 항목에 들어 있다. 담당 보고서의 분야별 번호와 집계는 별개이며, **최종 발견 번호·심각도·승인 조건은 이 문서의 R7-01~06**이 정본이다. 입력 담당의 C3는 질문 전제 정정으로 분류했다.
