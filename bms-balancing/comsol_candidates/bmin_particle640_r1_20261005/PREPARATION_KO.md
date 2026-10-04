# B-min 오프라인 후보 r1 — 준비 검토의 국소 보완 (BMIN-N1 · BMIN-N2 · C1)

상태: **r1 작성 · 정적 대조만 함 · 변경부 기능 검증 미실행 · native 미승인.** 후보 코드의 import · 구문 해석 · 컴파일 · 실행, JVM · COMSOL 호출은 0 회다.
모든 승인 플래그는 false.

근거: v1 (`../bmin_particle640_20261004/` · manifest `3722a51f…` · 고정 커밋 `74502af93`) 의 준비 검토 회신 `LOCAL_CORRECTIONS_REQUIRED`
(`reviews/r14_repros/codex63/comsol_bmin_candidate_review_20261005/` · SPEC §48) 과 사용자의 국소 보완 지시 (§48-2 — §45 범위 안). 검토가 정한 범위
그대로 N1 · N2 · C1 만 고쳤다. Java · entry · 물리 · 시간 목록 · 좌표 · 기준 CSV · 한도 · 예산 · 경로 · 식별자는 v1 그대로다.

## 1. 식별

| 항목 | 값 |
|---|---|
| r1 CODE_MANIFEST SHA-256 | **`9dcb47f0ec3ec346b491d90c2836e3b30f54eb88fd5e4fbd216fc34782275cdb`** (이전 = v1 `3722a51f…`) |
| run_id · 실행 기계 root | v1 과 같다 — `bmin_particle640_candidate_001` · `outputs/bmin_particle640_offline_preparation_20261004/` (v1 은 배치 · 승인된 적이 없다 · 승인은 manifest SHA 에 결속) |
| 바뀐 파일 | `PARENT_COMMAND.ps1` (CRLF · 24,469 B) · `src/diagnostic_consumer.py` (CRLF · 26,065 B) · `CONTRACT.json` (문구 하나) · 봉인 셋 (manifest SHA) |
| 그대로 | `src/Bmin640Candidate.java` · `src/candidate_entry.py` (v1 과 바이트 동일) |
| v1 문서 중 그대로 유효 | `BASELINE_IDENTITIES.json` · `RESOURCE_BUDGET_KO.md` · `LITERAL_CHANGE_MAP.json` · `CHANGE_BOUNDARIES.json` (NORMAL480 → v1) — r1 은 그 위의 국소 변경이다 |

## 2. 무엇을 고쳤나

| 발견 | r1 의 변경 | 자리 |
|---|---|---|
| **BMIN-N1** (P2) — 부모가 확인된 정상 native 종료를 구성 / 분석 / 전달 실패 때 `NOT_ESTABLISHED` 로 합쳤다 | 새 함수 `GNativeAxis` — 부모가 **스스로** native 자식 반환 (returned · rc 0 · 예외 / 새 오류 없음) · 결과의 run / manifest 결속 · 종료 증거 (GDecision 과 같은 구조 검사: 보고 / 끝 / 안전 접두 시각 · 저장 시각 수 · guard · 정지 사유 · 정상 150 s 또는 정합한 보호 중단) 를 확인한 뒤 consumer 라벨이 같은지 본다. 실패하면 `NOT_ESTABLISHED` + 원인 (`NATIVE_CHILD_RETURN_MISSING_OR_ERROR` · `NATIVE_CHILD_RC` · `TERMINATION_EVIDENCE_MISSING` · `RESULT_IDENTITY` · `TERMINATION_EVIDENCE_INVALID` · `CONSUMER_NATIVE_LABEL_MISMATCH`). `GFields` 는 이 축을 비교 · 증거 · 분석 · 전달 결과와 상관없이 그대로 싣고, 부모가 받아들인 정상 결과 (AWAITING 라벨 + NORMAL 축) 만 consumer 의 비교 판정을 싣는다 — 나머지는 `evidence_validity` INVALID · `mesh_comparison` INCONCLUSIVE. consumer 문자열을 확인 없이 옮기지 않는다 | 부모 `GNativeAxis` · `GFields` (블록) · `$bNativeAxis` 초기화 · GDecision 바로 뒤 한 번 계산 · `GFields` 호출 셋 (PARENT_LOCAL_DECISION · FINAL_BOUNDARY · POST_WRITE 콘솔) |
| **BMIN-N2** (P2) — `mesh_evidence` 가 DOF 문구가 없어도 PASS · 초기화 DOF 만으로도 PASS | 단일 Time-Dependent Solver 구간 (native_stop 이 이미 한 번만 있기를 요구하는 같은 표식) 안의 `Number of degrees of freedom` 줄이 **정확히 하나 · 형식이 맞고 · solved > 0** 이어야 한다. 없음 · 구간 밖 (Stationary 1202+12) 만 · 둘 이상 · 형식 불일치는 `TRANSIENT_DOF_READBACK_COUNT` / `_FORMAT` / `_VALUE` → I-3 미완. 예상 156,925+12 와 다른 유효값은 값 · 차이 · 검토 사유 (`review_note`) 를 남기되 **실패시키지 않는다**. 부모 GDecision 도 `mesh_readback.transient_dof.solved` 가 양의 정수인지 본다 | consumer `mesh_evidence` (블록) · 부모 GDecision 한 조건 · CONTRACT `expected_transient_dof.status` = `OBSERVATION_REQUIRED_DIFFERENCE_RECORD_ONLY` |
| **C1** (비차단) — PS01-03 / 04 를 decimal 자릿수 경계 시험처럼 적었다 | 문구를 실제 범위로 좁혔다: **PS01-03 / 04 는 한도 부근 값과 라벨 일치 검사일 뿐**이다. 대신 명시 사례 PS01-16 을 더했다 — 소수 30 자리 문자열 (.NET decimal 의 28 자리를 넘는다) 은 반올림되든 해석에 실패하든 부모가 INCOMPLETE 로 닫는다 (불일치 = 미완 원칙 · 정밀도 보증이 아니다) | 이 문서 · 검증안 · 요청문 |

**알려 둔 한계 (r1 에서 바꾸지 않은 것):** entry 는 v1 그대로라, native 실행 뒤 보존 · 정책 · 정리 검사가 실패해도 rc 1 을 낸다 — 부모는 그것을 native
실패와 구분하지 못하므로 그런 실행은 `NOT_ESTABLISHED` (`NATIVE_CHILD_RC`) 로 보수적으로 남는다 (각 오류의 단계는 `NATIVE_STATE.json` 에 있다).
`GNativeAxis` 가 보는 것은 consumer 의 구조화된 종료 출력이다 (GDecision 과 같은 수준) — 원 로그는 consumer 가 읽는다.

## 3. 정적 대조 (`STATIC_AUDIT.json` · `tools/static_audit_r1.py`)

- v1 꾸러미 = 검토받은 커밋 `74502af93` 의 바이트 · v1 의 정적 대조 (81 항목) 를 다시 돌려 v1 → NORMAL480 사슬이 그대로임 · 그 결과 파일도 바이트 그대로.
- **r1 → v1 역재구성:** `R1_CHANGE_BOUNDARIES.json` 의 순서대로 선언 변경만 되돌리면 consumer · 부모가 v1 바이트와 정확히 같다 · Java · entry 는 바이트 동일.
- consumer 는 `mesh_evidence` 외 모든 함수 · 부모의 `BHash` · `BRef` · `BRead` · `BSave` · `BInvoke` 가 v1 과 바이트 동일 · `GNativeAxis` 의 세 보조 함수는
  GDecision 의 것과 글자까지 같다 · GDecision 은 선언한 DOF 조건 하나만 다르다 · CONTRACT 는 상태 문구 하나만 다르다 · COMMAND_MAP · FIELD_SPEC 은
  manifest SHA 만 다르다 · 검증안 · 문서가 r1 manifest 에 결속.

재현: r1 꾸러미 루트에서 `python3 tools/build_candidate_r1.py --check` · `python3 tools/static_audit_r1.py`.

## 4. 판정 문장 (SPEC §44-2 그대로)

한도와 같으면 허용한다 (≤). 모든 유효 조건이 성립할 때 max \|ΔV\| ≤ 0.001 V **그리고** 두 전극 max \|Δx_surface\| ≤ 1e−4 이면
`WITHIN_LIMITS_THIS_WINDOW`, 어느 하나라도 **엄격히 크면** `EXCEEDS_LIMITS` 다. 앞 두 필드 (native 종료 · 증거 유효) 중 하나라도 성립하지 않으면
`INCONCLUSIVE` 다 — r1 에서는 native 종료가 확인됐는데 증거 · 분석 · 전달이 실패하면 `native_completion` 은 그대로 남고 비교만 `INCONCLUSIVE` 가 된다.

## 5. 변경부 검증안 · 다음

`LIMITED_VALIDATION_PLAN.json` — 9 군 **54 사례** (v1 41 + N1 7 · N2 5 · C1 1 · PS01-05 / 07 / 09 기대값 갱신 · PY03-05 분리) · 예산 제안 1,530 s.
`VALIDATION_REQUEST_KO.md` · `NATIVE_BMIN640_APPROVAL_DRAFT_KO.md` 는 비활성 초안이다.

다음 (각각 별도 사용자 결정 · 자동 시작 없음): ① r1 준비 재검토 → ② 변경부 검증 승인 · 수행 · 수용 → ③ native 최대 1 회 승인 → ④ 결과 수신 검토.
하지 않은 것: 컴파일 · 기능 시험 · harness · JVM · COMSOL · native · 정책 변경 · 실제 승인 파일 생성 · 실행 기계 접근 · 유한 σ · 960 s.
