# Gate77 — 단계 3 계약 v4 구현 전 재심사

2026-09-27 · 독립 정적·데이터 검토. 과학 계산·COMSOL·제공 프로그램·회귀 suite·복원·재채점·class/투영/원장 수정은 하지 않았다.

## 결론

**단계 3 재심사를 다음 과제로 고른 방향은 수용한다. 그러나 현 문구의 “단계 12 전체 완료 → 단계 13 일괄 착수”는 그대로 수용하지 않는다.** 아래 **설계 정정 3건(N1·N2·N3)**을 반영한 제한 오프라인 구현 라운드를 권고한다. 실제 착수는 사용자의 별도 범위 승인에 따른다. pilot/본 계산 GO는 없다.

76차의 **74차 항목 1–6 + 75차 잔여 종결은 유지**한다. 새 결함으로 그 목록을 다시 열지 않는다. 이번 판단은 그 유한 종결을 아직 미구현인 Stage3 전체 계약의 완료로 확대할 수 있느냐에 관한 것이다.

`grid_fit_v5`는 `full_bundle/current_validated/diagnostic/no_active_claim`인 실물 근거다. 원자료와 로컬 보관·복원 영수증의 가치는 인정하되, 외부 보존 provider·v6 실험·primary 결과의 증거로 바꾸지 않는다.

## 1. 고정 대상과 이번에 직접 확인한 것

| 항목 | 관측 |
|---|---|
| 요청 HEAD | `ebbcf04ed6cd4f5c2f71b4ebd28031c5fd441002` |
| 코드 기준 | `23c361edbfc92fefcfbf0639b5ac40f61f7ebec7` |
| 독립 source digest | `1c67a748598baadb` / RUN_SCOPE 58파일 |
| 코드→HEAD / Gate76→Gate77 RUN_SCOPE diff | 둘 다 0 bytes |
| Gate76 이후 원장·CLAIM_STATUS·영수증·artifacts·시험·기존 투영/게시기 | diff 0 |
| Gate76 원본 리뷰 ZIP | SHA `b532543bfc9a2e2ef435d7cc6536ae23ec4c388c574c225ec70db93e0db4aa61`; 87 payload+manifest, 수신 사본 87개도 바이트 일치 |
| grid_fit_v5 실물 묶음 | 29파일 / 27,313,017 bytes / 구성원 SHA·정확 집합 일치 |
| 현재 receipt | core SHA `ae614af28efc8f9e8315198d348b935cf0f32c6f1ab83885ba58e38cc4e83a5b`; 원장·묶음·out·두 출력 digest 결속 확인 |
| 보존 backend 명세 / 보존 transaction index / sentinel 파일 | `preserve_backend.yaml`, `preserve_index`, `sentinel_panel.yaml`은 이 고정 checkout에 없음 |
| 검토 checkout | tracked 2,958파일. 전후 식별과 최종 clean 상태는 `PRESERVATION_AFTER.json`에 기록 |

자세한 관측은 `DATA_AUDIT.json`, 시작 목록은 `SOURCE_BEFORE.json`에 있다. receipt의 33검사·복원·재채점은 **기존 기록을 대조한 것**이지 이번에 다시 실행한 검사가 아니다. 송신한 1,944 passed / 2 xfailed 및 docs-lint 358 passed도 송신 측 기록이며, 이번 독립 실행 수에 더하지 않는다.

## 2. 설계 정정 — 유한 목록 3건

### G77-N1 · P1 — 실제 로컬 보관 완주와 실물 retention provider를 같은 것으로 취급했다

**자리:** `GATE77_REQUEST.md:37`(묶음 9), `:47`(단계 12), `:63–64`(질문 1·2).

요청은 `grid_fit_v5`를 “실물 provider 어댑터는 이제 있다”의 근거로 제안한다. 그런데 다음은 서로 다른 경로다.

| 실물로 확인된 경로 | 아직 같은 증거로 확인할 수 없는 경로 |
|---|---|
| 계획/실행 lifecycle → 로컬 `artifacts/grid_fit_v5` → archive 복원/validator/재채점 receipt → 원장 결속 | §13.2의 backend 소유 CAS → CAS만으로 복원 → durable registration → 운영 provider의 retention/version 상태 검증 |

근거:

- 현재 receipt `core.bundle.uri=artifacts/grid_fit_v5`, 복원 명령은 `tools.archive_bundle.restore`다. `LEG_PRESERVATION.yaml:1005`도 같은 로컬 URI다.
- `tools/preserve.py:49–52`는 실제 운영 backend canary를 첫 pilot 전 별도 gate로 남긴다. `CasBackend.ENFORCEMENT`는 advisory(`:493–508`)이고 `probe_enforcement()`도 advisory를 반환한다(`:531–540`). 이것은 보관 자체가 없다는 뜻이 아니라 강제 수준이 다르다는 뜻이다.
- `tests/test_docs_lint.py:4034–4039`의 canonical backend/index 자리 두 개가 실제로 없다. `:4164–4186`의 registered-generation 검사는 여전히 `registered == {}`를 기대한다. 원장에 `registered_receipt`를 주장하는 leg도 없다.
- RUN_SCOPE Python의 정적 named-call 목록에서 `run_transaction`/backend 생성자를 `preserve.py` 밖에서 부르는 자리를 찾지 못했다. 이는 정적 목록이며 외부 배포 전체의 부재 증명은 아니다. 위 URI·빈 canonical 자리·회귀 계약과 함께 판단한다.

**영향:** 로컬 실물 완주를 운영 provider canary로 읽으면, 남은 보존 요구가 상태표에서 사라진 채 pilot 조건이 충족된 것으로 오인된다. E1/E2/E4 라벨은 이 별개의 backend 증거를 대신하지 않는다.

**최소 정정:** 단계 12를 “로컬/협조적 환경의 실행·보관 경로는 실물 확인, 전체 운영 보존 profile는 부분”으로 나눈다. 묶음 8·9의 local sub-scope와 provider/registration 잔여를 각각 적는다. 선택지는 둘이다.

1. 기존 retention 계약을 유지한다면, 실제 배포 profile·backend URI/권한·회수 및 retention canary의 합격 기준을 **pilot 전 별도 gate**로 남긴다.
2. 협조적 로컬 보존으로 범위를 줄일 생각이면, 사용자에게 그 한계와 계약 변경을 명시 승인받는다. 기존 실물 결과를 WORM/object-lock 증거라고 재명명하지 않는다.

지금 클라우드 구축이나 canary 실행을 요구하는 것이 아니다. 이 경계를 정확히 남긴 채 비계산 코드·schema 구현은 진행할 수 있다.

**종결 기준:** 수정 상태표/단계 위치/질문 1·2에서 두 경로가 분리되고, 첫 pilot의 보존 profile 선택 및 증거 gate가 빠지지 않는다. 새 grid 재실행 불필요.

### G77-N2 · P1 — primary의 arm과 endpoint가 기존 계약에 충분히 결속되지 않았다

**자리:** `GATE77_REQUEST.md:54,57` ↔ `STAGE3_CONTRACT.md:431–490`; `CLAIM_STATUS.yaml:173–178`.

요청은 `equal_start_count_base_retained`를 primary arm으로 제안하고 “transition table을 primary로 확정”한다. 그러나 계약 §7의 고정 내용은 다음이다.

- grid reference, `p_ini=null`, **warm 없이** 동일 base·bank·후보 수로 33p/34p를 비교한다.
- 하나의 primary scalar는 `Δ=(pass→fail − fail→pass)/n`이다. 전이표 네 칸은 같은 estimand의 필수 분해이며 별도 두 번째 endpoint가 아니다(§7.1).
- warm을 넣고 random 하나를 빼는 `equal_start_count_base_retained`는 §7.2에서 **secondary ablation**이다.
- CLAIM_STATUS의 해당 항목은 v6·`requires_leg=false`와 승격 금지를 적을 뿐, arm·분모·scalar를 다시 정의하지 않는다. “이미 문장이 있다”만으로 새 제안을 사전 등록 완료로 볼 수 없다.

`candidate_mode` 이름 자체를 금지하는 것은 아니다. 같은 mode 라벨에 **warm=false**를 붙여 primary의 실제 후보가 `[base]+bank[:B-1]`라면 양립 가능하다. 현재 요청은 그 boolean과 실제 후보 배열을 쓰지 않아, warm arm으로 읽히는 제안을 그대로 승인할 수 없다. `B`가 목적함수마다 다르면 동일 후보 수 primary도 달라지므로 이 축도 고정해야 한다.

**권고 기본값:** 기존 §7을 유지한다. primary는 grid/no-warm/동일 총 B/같은 bank prefix, scalar Δ와 전이표 분해. warm base-retained 및 legacy replacement는 별도 secondary; union은 이번 계획에서 제외한다. secondary를 실제로 계산할지는 별도 leg·비용표에서 정한다.

정말 warm 운영 성능을 primary로 바꾸려면 “기존 estimand 유지”라고 하지 말고 연구 질문·estimand·endpoint·claim을 명시 변경한다. 어느 쪽이 더 유리한 결과를 내는지 보고 고르면 안 된다.

**종결 기준:** primary 한 행에 reference, 두 warm flag, p_ini, 두 objective의 실제 후보 구성/총수, pairing key, scalar·분모·실패/누락 처리, transition 분해를 적는다. secondary와 섞이지 않아야 한다. 새 수치 결과 불필요.

### G77-N3 · P2 — “pilot 전 예산 숫자 없음”과 독립적인 필드 구현 순서는 실행 가능한 의존 관계가 아니다

**자리:** `GATE77_REQUEST.md:55,65`; `STAGE3_CONTRACT.md:307–350,362–429,691–714`.

최종 채택 B를 plateau 결과 뒤 정하는 것은 맞다. 그러나 **탐색 ladder/최대 B/중단 규칙/수치 floor 측정 단계/계산 예산**까지 미정으로 두면 pilot 자체가 승인 가능한 계획이 아니다. 요청의 다음 행은 이미 `[5,10,20,40]`를 제안하므로 “숫자를 적지 않는다”를 **최종 채택값은 미정**으로 좁히면 된다.

또한 `candidate_id`는 §4의 design→pair→bank→candidate 결속과 warm-provider payload를 필요로 한다. §9.4의 다섯 필드 전체를 “작고 독립”으로 먼저 완성했다고 할 수 없다. 현재 `src/fitting.py:284–288`의 restart serializer는 `p/J/i/source/warm`만 남긴다. fit 행의 `converged/n_eval`은 이미 존재하지만(`:430`), 각 restart의 값과 동일하지 않다.

**최소 구현 의존표:**

1. N1·N2 상태/estimand 정정과 새 v6 writer·historical reader의 버전 경계를 먼저 고정한다. 기존 기록의 필드를 소급 삭제하지 않는다.
2. 로깅·오류 처리 중 독립 가능한 부분(`converged`, 종료 사유, restart별 `n_eval`, parquet 읽기 실패의 구조화)을 한정 구현한다. candidate/bank 연결은 아직 완료로 세지 않는다.
3. 묶음 1·2의 planned/realized schema와 ID preimage, 묶음 3의 provider DAG/map을 연결한다. primary의 no-warm 경로는 명시적 null/no-provider 분기로 둔다. 여기서 후보 ID/인덱스·수량과 실제 serializer/validator를 끝까지 잇는다.
4. 같은 schema에서 묶음 6의 신규 writer 구필드 제거와 consumer별 linkage 음성 시험을 붙인다. v5/v6_prep read-only dispatch와 과거 봉인은 유지한다.
5. sentinel 선택 규칙·stratum·ladder/max B·실패시 미채택·`mono_tol`와 material tolerance 역할을 고정한 뒤 묶음 4·5를 연결한다. 경험적 hard는 선택 자료와 독립 확인 자료를 구분한다.
6. 승인 대상 고유 leg/provider/floor/smoke/holdout 목록과 비용표 → 오프라인 구현 독립 검토 → 필요한 보존 profile 확인 → 별도 pilot 승인으로 간다.

numerical floor는 기존 적합한 자료가 없으면 **별도로 한정 승인받는 측정 단계**다. floor를 보고 tolerance를 봉인한 뒤 budget-adoption 결과를 판정한다. 지금 임의 tolerance 숫자를 발명하거나 측정 승인 없이 반복 계산하지 않는다.

**종결 기준:** 위 의존 관계와 사전 고정/측정 후 결정 항목이 한 표로 연결된다. 60이라는 전체 개수만 적는 대신 exact 조건·reference·noise seed·objective·arm별 strata와 분모, empirical holdout/treatment 포함 여부를 명시할 작업 범위를 고정한다. 새 suite 전량 재실행이나 실제 pilot을 이번 정정의 증거로 요구하지 않는다.

## 3. 요청 §4의 다섯 질문에 대한 답

| 질문 | 답 |
|---|---|
| ① 8·9의 실물 provider 증거인가 | **로컬 production lifecycle/보관/복원 receipt 증거는 예. 외부 retention provider/registered transaction canary 증거는 아니오.** N1의 경계로 표를 고친다. |
| ② 12 종료 → 13 착수인가 | **그 전제 그대로는 아니오.** 12 전체 종료를 선언하지 않고 N1–N3를 반영한 제한 오프라인 구현의 설계 적합성은 조건부 수용 가능하다. 실제 구현은 별도 사용자 범위 승인, pilot은 다시 별도다. |
| ③ 순서와 라운드 끝 영수증 1회인가 | 순서는 N3처럼 dependency를 반영한다. 영수증은 **최종 코드가 고정된 라운드 끝에 필요한 leg별 1회** 재생성하는 운영 원칙은 조건부 수용한다. 세부 조건은 아래. |
| ④ 지금 고정할 여섯 결정은 | §4 표의 권고. primary와 탐색/실패 규칙은 먼저, 최종 B·새 수치는 측정 뒤다. |
| ⑤ 새 실행 GO 아님 / 기존 결과 진단 전용인가 | **예.** 새 계산·복원·class/투영 게시 승인 없음. `grid_fit_v5`의 no_active_claim 유지. |

영수증의 “끝에 한 번” 조건:

- 중간 RUN_SCOPE 변경 중 기존 receipt는 그때의 validator identity를 가진 역사적 증거다. 파일을 안 지우되 새 코드 검증을 이미 통과한 것처럼 쓰지 않는다.
- 최종 clean 코드 identity·대상 leg를 고정하고 기존 원문을 history에 보존한다. producer 식별/실제 산출은 소급 교체하지 않는다.
- `make_receipt.py`는 단순 SHA 라벨 편집기가 아니다. restore·validate·재채점을 수행한다. 따라서 **이번 읽기 전용 리뷰에서는 실행할 수 없고**, 다음 코드 라운드의 명시적 검증 범위에 포함되어야 한다. 실패하면 새 검증 완료로 붙이지 않는다.
- 재생성 뒤 RUN_SCOPE가 다시 바뀌면 그 영수증은 새 identity의 완료 근거가 아니다. 후속 이동을 숨긴 채 “1회 약속”을 맞추지 않는다.
- “한 번”은 코드 라운드마다 대상 leg별 완료 검증을 뜻하며, 두 leg를 하나의 새 receipt로 합치거나 일부 성공만으로 전체를 통과시키는 뜻이 아니다.

## 4. 여섯 사용자 결정에 대한 권고

| 결정 | 지금 고정할 것 | 이후 결정할 것 |
|---|---|---|
| 1. 후보 정책 | primary grid/no-warm, 같은 base·bank·총 B. warm base-retained와 legacy는 secondary, union 제외 | secondary별 실제 실행 leg·B는 비용/범위 확정 뒤 |
| 2. 예산/provider | ladder `[5,10,20,40]`는 **제안값**으로 명시 수용 여부 결정; 최대치·미도달시 미채택·provider/floor 단계 분리. primary는 p_ini/warm-provider 없음 | 실제 map은 허용된 계산 뒤 봉인. 최종 채택 B는 사전 gate 통과 결과로 정함 |
| 3. panel | 60은 최소 비교 구조. exact 좌표/ID·seed·bounds/reference digest·stratum·holdout 선택 규칙을 파일로 고정할 의무 | 아직 없는 SHA를 계획값으로 가장하지 않음. 확대/추가 치료축은 새 범위·비용에 표시 |
| 4. estimand | 기존 §7의 단일 Δ와 네 칸 분해, 결정론적 격자 기술통계. 실패/누락을 유리하게 제외하지 않는 규칙 | 실제 관측 전이 건수. 기존 recorded 값은 설계 prior이지 새 primary 결과가 아님 |
| 5. 목록/비용 | 고유 leg/provider/floor/smoke/holdout를 중복 제거하고 wall/CPU 비용·최대 예산 분리. 산출 전 실행 승인 없음 | 환경·실행 수에 따른 견적. `833×28`은 점유 core-time 근사이지 측정 CPU 사용량/새 코드 비용 보증 아님 |
| 6. 잃은 7다리 | recorded_projection/unvalidated 유지, 과거 복원·승격 없음 | 새 v6가 생겨도 지지할 수 있는 claim만 새로 등록. 다른 estimand의 옛 주장까지 자동 대체하지 않음 |

이 표는 **검토 권고**이며 사용자의 여섯 선택을 대신 완료했다는 기록이 아니다.

## 5. §13.1 상태 갱신 권고

| 묶음 | 이번 판정 | 한정 근거/남은 범위 |
|---|---|---|
| 1 | 부분 | 실물 계획·phase·out·receipt 연결은 있음. v6 stage×objective×arm budget/count와 실제 consumer 연결은 남음 |
| 2 | 부분 | design_wire·golden 기반 존재. NFC 검사 코드도 있음. 이번에 그 회귀를 재실행하지 않았고 v6 실행 E2E는 없음 |
| 3 | 미착수 | 과학 provider DAG/arm별 p_ini map. 저장소 retention provider와 이름만 같으니 구분 |
| 4 | 미착수 | tolerance·stratum·adoption·max-failure의 실제 v6 소비 |
| 5 | 미착수 | 고정 checkout에 sentinel_panel.yaml 없음 |
| 6 | 미착수/기반 존재 | 변이 틀과 일부 ID 기반 존재는 인정. v6 writer/reader의 구필드 정리·per-key 연결 완료 아님 |
| 7 | 부분 | 기존 세 축/claim_scope/lifecycle의 수용 범위 유지. v6 새 protocol/등록 세대 연결은 검증 전 |
| 8 | 부분, 로컬 하위 범위 수용 | 실물 묶음·엄격 index·typed receipt·history. 외부 backend/회수·보관 profile와 동일하지 않음 |
| 9 | 부분, 기존 lifecycle 하위 범위 수용 | 실물 실행/원장 경로와 기존 격리 회귀. provider transaction 등록·운영 canary와 구분 |
| 10 | 부분 | 기존 cohort/frozen/history 범위 유지, 새 v6 cohort/dispatch/게시 E2E는 없음 |

상태표를 보수적으로 유지하는 것은 76차를 미종결로 되돌리는 것이 아니다. **이전 결함 목록의 종결, 구성요소 구현, 새 세대 E2E, 과학 주장 성립**은 서로 다른 판정이다.

## 6. 비차단 문구 정정과 검토 한계

- 요청 §0/원장 §107의 “같은 코드라 산출이 같다”는 바이트 동일 보증으로 쓰지 않는다. **같은 설계를 반복해도 v6의 새 대조/주장을 얻지 못한다**가 재실행을 권고하지 않는 충분한 이유다. 실제 grid_fit_v5 producer digest는 `c2ef1a811e70bb4c`, 현재 validator/code는 `1c67a748598baadb`로 다르다. 그 이후 변경이 주로 보존 구현이라는 사실과 새 실행 바이트 동일은 별개의 주장이다.
- Gate76 접수문이 바로잡은 첫 RED 18건과 history 3+현행 1/leg 정정은 수용한다. 과거 원문을 다시 고치거나 시험을 재현하지 않는다. 등록부의 현재 369와 사용자 요약의 옛 367 혼선은 이번 새 차단 사유로 삼지 않는다.
- data_audit는 reviewer 소유 코드로 파일·Git·ZIP·YAML·AST만 읽었다. 반환되는 PASS는 무결성/고정성 대조의 통과이지 실험·backend·v6 구현 PASS가 아니다.
- 초기 보조 조회 1회에서 잘못된 작업 디렉터리로 소스 경로를 찾지 못했고, 올바른 고정 checkout에서 읽었다. 이 read-only 조회 오류는 제품 시험 실패로 분류하지 않았다.
- 이 리뷰는 기존 Windows/원격 전체 프로세스·저장소·외부 provider를 계측하지 않았다. checkout 보존은 검사한 tracked 파일 범위다.

## 다음 최소 행동

**N1 상태 범위, N2 primary 한 행, N3 구현 의존/사전고정 표를 한 번에 정정한 코드 라운드 범위를 제출하라.** 이 세 정정만으로 이번 설계 잔여를 대조할 수 있다. 같은 1,944개 suite·grid_fine 실행·COMSOL·보존 회귀를 지금 반복할 필요는 없다.

사용자에게는 그 수정된 **오프라인 구현 범위**만 승인받고, 실제 provider canary·floor/pilot·본 계산·복원/receipt 재생성은 각 승인 범위를 명시한다. 현재 리뷰는 그 행동을 실행하지 않으며 실행 GO도 발급하지 않는다.
