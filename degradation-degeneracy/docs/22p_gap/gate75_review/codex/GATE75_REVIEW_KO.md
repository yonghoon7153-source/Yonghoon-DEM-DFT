# Gate75 독립 검토 — 부분 수용, 전체 종결 보류

2026-09-27. **잔여 P1 1건·P2 2건. 새 본 실행 GO를 심사하거나 부여한 문서가 아니다.**

기존 Gabia 결과·보존 묶음의 제한 수용은 유지한다. R1/R2 기록, 고정 캐시 진입 정책, 영수증의 producer/validator 구분은 수용한다. 진단 전용 분류의 방향과 현재 원장 배치도 수용하지만 잘못된 실행 자리의 소비 검사가 남았다. archive index에는 실패 반환과 중복 키 처리 두 공백이 남아 여섯 항목 전체를 종결할 수 없다. **이 결함들이 현재 저장 결과를 손상시켰다는 관측은 없다. 새 grid/fit 계산도 필요하지 않다.**

## 1. 고정 대상과 검토 범위

| 항목 | 고정값 |
|---|---|
| 요청 HEAD | `ef6689bbe296e545df57dc481e45ec98c2b9ea3b` |
| RUN_SCOPE 코드 | `ebfb853d1b3dff0678f5f67985003498a3476982` |
| 독립 source digest | `27390883eb132941` — 57 파일 |
| 코드→요청 HEAD | RUN_SCOPE diff 0 bytes |
| 비교한 이전 HEAD | `a49a021833282e0bd04c4565591668dc323e9630` |
| 검토 checkout | `C:/Users/Administrator/Documents/Codex/g75_20260927` |

수신 발송문을 읽고 고정 커밋을 별도 checkout하여 코드·원장·영수증·묶음을 데이터로 대조했다. 대상 모듈 전체를 import하거나 제공된 suite/분석 프로그램을 실행하지 않았다. 검토자가 작성한 검사에서는 화이트리스트 AST 판정 함수, index heredoc 및 shell 반환 경계만 분리해 자기 fixture에서 검사했다. `src.io.source_digest`는 독립 계산한 고정 digest를 제공하는 adapter로 대체했다. 실제 archive/restore/attach/publisher/validator/재채점/fit/COMSOL은 0회다.

최종 독립 사례는 **23개 고유 사례**다. shell 2개는 검토 환경의 Git 유틸리티 PATH를 바로잡아 별도로 재확인했다. 검토자 보조 코드의 추출·범위 가정 오류와 재확인 이력도 [REVIEWER_CHECK_HISTORY.md](REVIEWER_CHECK_HISTORY.md)에 보존했다. 이를 송신자의 41-node 회귀·전체 1,922 PASS에 합산하지 않는다.

## 2. 여섯 항목별 종결

| 항목 | 판정 | 근거 / 남은 조건 |
|---|---|---|
| 1 R1 추가 resume | 수용 | 별도 사전 재승인 없음과 한도 밖 호출을 인정하고 해석을 철회했다. 대화 출처·시점은 송신자의 후속 기록이며 수신자가 그 세션 원본을 직접 감사한 것은 아니다. 소급 승인으로 바꾸지 않는다. |
| 2 R2 문구 | 수용 | feasible 완료 0과 계산 0, VM 부팅 관측과 원인 가설, cache 유지 조건, finalize와 attach, loky 원인 불확실성을 분리했다. |
| 3 진단 전용 계약 | 부분 수용 / 종결 보류 | 현재 `no_active_claim`·역할 없음·실행 명부 분리는 적합하다. 단 **G75-N3**: 새 증거 소비자는 `out`의 존재만 보고 다른 실행 자리도 통과시킨다. |
| 4 고정 캐시 | 수용 | 실제 진입 `_assert_prospective_plan_is_startable`이 소문자 hex64/분류를 강제한다. null·짧은 값·비hex·대문자·숫자·축/분류 부재 거부를 별도 확인했다. 기존 live spec 비교를 지우지 않았다. |
| 5 index 보존 | 종결 보류 | 정상 병합·충돌 거부·원자 교체 방향은 맞다. **G75-N1/N2**: 쓰기 실패의 최종 rc 전파와 중복 YAML 키 거부가 빠졌다. |
| 6 보존 / validator 식별 | 수용 | 두 옛 receipt는 history에 바이트 동일. 새 receipt 변경은 validator digest/core SHA/stamp뿐이고 validation/outputs 값은 같다. producer digest·묶음·등록부·투영을 바꾸지 않았다. |

## 3. 잔여 발견 — 유한 목록

### G75-N1 · P1 — index 갱신 실패가 archive 성공(rc 0)으로 반환됨

좌표: `scripts/archive_results.sh:294`, `:401–405`, `:425` (고정 HEAD).

최종 index Python 호출을 `if ! ...` 등으로 검사하지 않는다. 스크립트는 `set -uo pipefail`이고 `-e`는 꺼져 있다. `_tmp.write_text`/`os.replace`/직렬화 등이 실패해도 `n_bad`는 증가하지 않는다. 마지막 반환은 오직 `n_bad`/`n_missing`에 달려 있다. 이미 묶음 승격과 `n_ok` 증가가 끝난 뒤라, 옛 index와 새 묶음이 어긋난 상태에서도 성공 안내를 출력할 수 있다.

독립 확인:

- `W01_replace_failure`: **실제 index heredoc**의 `os.replace`만 자기 fixture에서 실패 주입. OSError, 기존 index SHA 불변. 이는 atomic index 교체 자체의 보호를 확인한 것이지 전체 보관 성공이 아니다.
- `S17`: index 명령을 rc 17로 대체하고 **원래 shell if/footer/최종 predicate**를 유지한 검토용 경계 스크립트 → 부모 shell **rc 0**, 불완전 0, commit 안내 출력. 온전 rc 0 대조군도 rc 0. Git 유틸리티를 정상 제공한 별도 확인은 stderr 없음.
- 실제 묶음 승격/복원은 실행하지 않았다. 전체 프로그램 E2E 실측이 아니라 소스에 결속한 반환 경계 재현이다.

최소 수정: 최종 index 호출의 실패를 즉시 nonzero·명시적 미완으로 전파하고 성공 안내를 차단한다. 승격이 이미 일어난 경우 이를 숨기지 말고 index와 묶음의 불일치/정리 필요 상태를 보존한다. 기존 index를 비우거나 무조건 재시도하지 않는다. tmp write 실패와 replace 실패를 넣은 제한 회귀에서 부모 rc, index SHA, 이미 승격된 상태의 표기를 함께 확인한다. 자동 rollback/복구를 추가하려면 그 변경 범위는 따로 명시한다.

### G75-N2 · P2 — 중복 YAML 키가 파싱에서 사라져 무관 항목을 잃을 수 있음

좌표: `scripts/archive_results.sh:70`, `:225`, `:313`.

새 preflight는 `yaml.safe_load` 후 dict 모양만 검사한다. 중복 키는 이 시점에 이미 뒤 값으로 접힌다. 다음 입력은 의미가 불명확한데 preflight rc 0이다.

```yaml
runs:
  preserved: {payload_index_sha256: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
runs: {}
```

`I02_duplicate_runs`는 `runs={}`로 통과했다. `W02_duplicate_input_rewrite`에서 같은 최종 heredoc의 read/serialize 경로를 적용하면 `preserved`가 없는 index로 다시 써진다. 이 writer 검사는 bundle loop를 비우고 index 처리만 분리했다. 실제 다음 묶음 승격에서는 사라진 기존 항목이 새 항목에 더해 복구되지 않는다. 같은 run 이름 중복(`I03`)·동일 entry의 identity 키 중복(`I04`)도 rc 0이었다. 기존 malformed shape 대조군(`I01`)은 rc 1이었다.

최소 수정: index 진입·동명 비교·병합에서 중복 mapping 키를 거부하는 동일한 해석 규칙을 사용한다. top-level `runs`, run 이름, identity 키 중복을 각각 회귀로 고정하고, 모호한 원문은 **첫 승격 전 거부·index 바이트 불변**으로 남긴다. YAML merge key를 허용한다면 그 충돌 정책도 명시한다. 이는 새로운 공격 모델 추가가 아니라 이번 “불명확한 index → 중지” 약속의 누락 경계다.

### G75-N3 · P2 — 진단 전용 소비자의 out 결속이 생산자보다 약함

좌표: `tests/test_docs_lint.py:2502`, `:2521–2554`; 정상 생산자 대조: `tools/preserve.py:8007`, `:8093`.

현재 receipt·묶음·hash는 전부 그대로 두고 원장 사본에서 `grid_fit_v5.evidence.out` **한 값만** `results/OTHER_RUN`으로 바꿨다.

| 검사 | 온전 사본 D00 | 잘못된 out 사본 D01 |
|---|---|---|
| `_scope_problems` + `_no_active_claim_evidence_problems` | 오류 0 | **오류 0** |
| 기존 `test_full_bundle_claims_are_backed_by_a_real_bundle` 본문 | 통과 | **통과** |
| 기존 `_assert_ledger_run_bound`, receipt/bundle의 실제 bound run 사용 | 통과 | **거부** |

새 helper는 `out`이 비어 있지 않은 문자열인지만 본다. typed receipt 검사는 receipt 내부의 자기정합을 확인할 뿐 외부 원장의 `out`을 전달받지 않는다. 영수증/묶음에 결속된 run과 원장 run의 비교가 소비 경로에 없다. 기존 회귀 `_drop_out`은 부재만 시험해 이 반례를 놓쳤다. core hash 변경·분류 오류 음성 대조는 정상 거부됐다.

최소 수정: 새 진단 증거 소비자가 typed core와 실물 묶음의 run 결속을 읽고, 기존 `_assert_ledger_run_bound`와 같은 규칙으로 원장 out을 대조하도록 한다. 양성·부재·공백·다른 비어 있지 않은 out을 이유별 회귀로 고정한다. 검사 실패 시 원장/receipt를 소급 수정하지 않는다. **기존 attach 보호가 깨졌다는 뜻은 아니다**—그 경로는 이 반례를 이미 거부하며 그대로 보존한다.

## 4. 요청 §5에 대한 답

### ① 항목 1–6

위 표대로 1/2/4/6 수용, 3/5 잔여 한정 보완. 전체 종결은 아직 아니다. R1 편차를 정직하게 기록한 것과 당시 모든 호출이 승인 범위였다는 것은 다른 주장이다.

### ② row_projection.py 불변

**이번 진단 전용 종결 범위에서는 수용한다.** 실제 g18 투영 명부는 `paired_fixed5_v4` 하나이며 `grid_fit_v5`는 실행 명부에만 있다. publisher/g18 바이트는 이전과 동일하다. 이번에 projection 재생성·복원·게시를 요구하지 않는다.

다만 publisher 자체가 새 `claim_scope`/`executed_legs`를 검사한다는 주장은 하지 않는다. 그 코드는 새 필드를 읽지 않으며 원장의 투영 명부를 직접 읽는다. `planned_index`·lint가 다른 경로에서 거부하는 것만으로 모든 publisher 직접 호출의 검사를 증명할 수 없다. 코드/시험의 “row_projection도 같은 분류를 거부” 주석은 좁혀야 한다. 향후 진단 자료를 claim/투영에 편입하려는 변경은 별도 승인·검토이며 이 수용을 재사용하지 않는다.

### ③ current_validated 이름

**유지 가능하다.** 계약 §8은 검증 축과 추론 용도 축을 분리한다. 이 경우 producer `c2ef1a811e70bb4c`, validator `27390883eb132941`, `inference_role=diagnostic`, `claim_scope=no_active_claim`을 함께 명시한다. “현행 코드로 재계산됨/현행 과학 주장 지지/수렴 증명”으로 읽지 않는다. `paired_fixed5_v4`의 기존 `historical_validated`를 이 판단으로 자동 승격하지 않는다.

### ④ 새 gate 아래 한정 본 실행

**이번 세 잔여를 닫으려고 새 grid/fit 계산을 할 필요는 없다.** 순수 소비자·격리 index 파일·shell 반환의 제한 회귀로 확인할 수 있다. 원래 데이터는 보존한다. 미래 실제 계산은 과학적 필요·사용자 새 승인·고정 코드와 계획·캐시·출력·resume 한도·보존 절차를 별도 확정한 뒤에만 가능하다. 캐시 사전 생성도 이번 검토가 승인한 계산이 아니다.

## 5. 독립 대조 결과와 증거 한계

- 57-file source digest 및 코드→HEAD RUN_SCOPE 0 확인. 2,789 tracked 파일의 전후 보존은 최종 `PRESERVATION_AFTER.json`에 기록한다.
- 기존 artifact index와 각 bundle, `_exec_class`, publisher, g18 projection, CLAIM_STATUS는 Gate74 HEAD 대비 불변이다. artifacts README 문구 변경은 결과 바이트 변경과 구별했다.
- grid_fit_v5: 29개/27,313,017 bytes, paired_fixed5_v4: 26개/23,863,555 bytes. payload 집합·각 SHA·receipt bundle 수/크기/요약/복원 위치 대조 완료. 별도 restore/재채점은 하지 않았다.
- 두 history receipt는 이전 HEAD 원문과 바이트 동일. 새 receipt core SHA를 독립 재계산했고 원장 값과 일치했다. 33/34 검사 결과와 output 필드는 이전과 같다. 실제 검사·재채점을 이번에 다시 했다는 뜻은 아니다.
- Gate74 원본 ZIP은 959,344 bytes / `eb03012cf4fbbf45f8e3bc354b14878f21c459a5913f6ba00a728d91d3a2adac`, 102 payload+manifest의 CRC/집합/크기/SHA 일치.
- 송신 전체 1,922 PASS·2 xfail/43:57/rc0는 **7ec4e234**에서의 보고로 기록한다. 첫 8765068a의 3 failed·1,919 passed·2 xfail은 §103에 남아 있다. 전체 suite·smoke·mutation을 수신자가 재실행하지 않았다. SEND 발송문 첫 괄호의 `8765068a`는 최종 PASS의 checkout처럼 읽히므로 `7ec4e234`로 정정해야 한다.
- “무관 index entry 바이트 그대로”는 실제 구현/시험이 보장하는 **파싱된 필드 값 보존**으로 좁힌다. safe_load/dump는 공백·인용·주석까지 바이트 보존하지 않는다. 이번 실제 기존 index 바이트가 불변인 사실과는 별개다.
- plan_leg의 선제 null 거부와 production의 엄격한 hex64 gate는 같은 정책에 정합적이지만, planner가 `_assert_prospective_plan_is_startable`을 직접 호출하는 구현은 아니다. “같은 함수 공유”라고 확대하지 않는다.

## 6. 다음 유한 범위

새 승인안은 G75-N1/N2/N3와 위 문구 정정만 대상으로 한다. 원래 결과·실패·R1 편차·옛 영수증을 보존한다. RUN_SCOPE가 바뀌면 validator 식별은 달라질 수 있으므로, 새 receipt 검증이 필요할 때는 기존 원문을 남긴 별도 승인 검증으로 취급한다. producer digest를 바꾸지 않는다.

이 검토는 수정·재시험·receipt 재생성·archive 게시·복원·class 변경·projection 게시·본 실행을 승인하지 않는다. 사용자에게 다음 범위의 승인을 받은 뒤 진행한다.

주요 근거: [DATA_AUDIT.json](DATA_AUDIT.json), [DECISION_PROBES.json](DECISION_PROBES.json), [SHELL_BOUNDARY_CHECK.json](SHELL_BOUNDARY_CHECK.json), [원장 변경](G74_TO_G75_LEDGER.diff), [생산 코드 변경](G74_TO_G75_SCOPE.diff), [소비자 변경](G74_TO_G75_LINT.diff). 모든 코드 좌표는 위 고정 HEAD의 `degradation-degeneracy/` 상대경로다.
