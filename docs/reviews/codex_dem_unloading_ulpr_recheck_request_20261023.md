# Codex 재확인 요청 — 언로딩 ULPR-01–04 수정 (2026-10-23 · 새 실제 런 0건 · 발송 = 1저자)

- **이번에 닫는 것:** ULPR-01–04의 코드·회귀시험·문서 정합을 재확인하고 `claimed_fixed`를 `verified`로 올릴 수 있는지 판정해 주세요. 이어 돌림에서 옛 관측을 새 관측으로 잘못 승인하는 문제, 관련 시험의 변이 감지, G2 덤프 구조/시점 검사, G2c 필수 열 결손 분류가 대상입니다.
- **이번에 닫지 않는 것:** 외부 검토 GO, 본 실행·물리 타당성·논문 결과·R_int, LHS214 또는 다른 연구 트랙, 새 DEM 실행, 임의 파손 파일 전체의 차단, 동시 파일 쓰기의 원자성, RESUME 정수 문법 전체는 이번 수정으로 닫았다고 주장하지 않습니다. 기존 이력/문법 시험의 실제 실행 결과도 이번에 새로 실행한 결과가 아닙니다.

**발송 전 초안:** ULPR-01–04는 본 요청의 `claimed_fixed` 제안입니다. 공유 원장의 현재 `open` 상태를 이 문서만으로 바꾸지 않으며, 독립 외부 판정/GO는 아직 없습니다. 내부의 새 문맥 diff-only 코드 재확인 v2는 검토·재현 범위에서 신규 차단 결함이 없다고 보고했지만 문서·봉인은 별도 `dem_unloading_ulpr_fix_evidence_20261023/independent/PACKAGE-REVIEW.md`에서 대조했습니다. 전체 게이트 최종 결과와 발송 pin/ZIP은 별도로 확정합니다.

## 1. 검토 대상과 고정 방법

| 항목 | 대상 |
|---|---|
| 작업 가지 | `codex/unloading-ulpr` — 이 가지를 검토/선별 반영 대상으로 유지 |
| 출발점 | `7799a2ff64ba462b42ce05edd3e63b7c2854d557` (`claude/sdcp-dem-manuscript-si-pqwtv8`에서 분기) |
| 최종 review pin | 전달 ZIP의 외부 `PIN.txt`에 최종 전체 commit SHA를 기록한다. 이 문서에 자신을 포함하는 새 commit SHA를 쓰지 않음 |
| 발송 검증 | 전달 ZIP의 외부 `PIN.txt` + `MANIFEST.sha256` + 해당 pin의 Git blob으로 묶음을 대조한다 |
| 코드 | `docs/data/ps45_unload_20261009/ul_reader.py`, `ul_gates.py` |
| 동반 정합 | 같은 키트의 README·`seal_kit.py`·`active_rules.json`·`SHA256SUMS`, 등록 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` §14-12 |
| 근거 묶음 | `docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/` (아래 근거 경로는 이 요청서 위치 기준) |
| 원 지적 | `docs/reviews/findings.json` ULPR-01–04, 인계서 §5-4 및 기존 재확인2 요청서 |

물리 기준·파라미터·생성 덱·history 키트와 LHS 외부 러너의 32개 봉인 대상 파일은 변경하지 않습니다. ULPR 키트의 코드/설명에 대응하는 정식 봉인 갱신은 이 별도 32개 봉인의 변경을 뜻하지 않습니다. 바이트 대조는 `dem_unloading_ulpr_fix_evidence_20261023/scope-verification.json`에 기록했습니다. 기준 스냅샷은 `dem_unloading_ulpr_fix_evidence_20261023/baseline_files_sha256.json`입니다.

## 2. 고쳤다고 주장하는 내용

| ID | 원 문제와 이번 동작 | 직접 근거 |
|---|---|---|
| ULPR-01 (P2) | 승인된 RESUME 뒤 새 시도가 새 단 행을 쓰기 전에 끝나도 옛 단 행을 정상 새 관측으로 채택하지 않도록 사건·창·단을 함께 조정합니다. 새 관측이 확인되는 정상 재개는 유지하고, 옛/새 소속이 확인되지 않는 꼬리는 진단을 남겨 유효한 앞부분과 구분합니다. | R37, `dem_unloading_ulpr_fix_evidence_20261023/probes/repro-tail-scope/results.json`, 독립 생성 덱/후속 CLI 재현 |
| ULPR-02 (P3) | 기존 여섯 사유/조건 줄의 변이를 해당 R38 단언이 검출하게 합니다. 앞 세 변이는 승인 거부를 유지한 채 사유 줄만 제거하고, 뒤 세 변이는 조건/가드를 제거합니다. 승인 밖 RESUME, k/step 비수치, 상태 불일치, 사건 되감기의 k 경계, 봉인 목록 판독기 해시, 재판독 프로세스 rc를 각각 검사합니다. | `dem_unloading_ulpr_fix_evidence_20261023/mutations/resume-six/results.json` 및 개별 전체 selftest 로그 |
| ULPR-03 (P3) | G2가 덤프 전체 구조·행 수·유한 값·고유 ID/열·정확한 헤더·BOX 형식·시점을 검사합니다. 복원 호출은 S0 또는 R_M에 결합합니다. 등록 열의 원 문자열 동일성은 유지하여 수치가 같아도 토큰이 다르면 불일치입니다. | C5/C6, R16/R35, `dem_unloading_ulpr_fix_evidence_20261023/independent/v2/restore-probe/restore_probe.json` |
| ULPR-04 (P3) | G2c 필수 26열 중 결손이 있으면 `NOT_COMPUTED`와 사유를 내고 복원은 `UNCONFIRMED`입니다. 필수 열을 갖춘 관측의 구조/시점 위반 또는 값 불일치는 FAIL/`VALUE_MISMATCH`, 별도 기술 실패의 `SYNTAX_FAIL` 우선순위는 유지합니다. G2c도 S0/R_M 요청 시점에 결합합니다. | C4/C6, R35, 동일 독립 복원 재현의 c26 결손/오시점 대조 |

### 이어 돌림의 구분과 남는 정보

등록된 한 번의 재개 승인 범위는 그대로입니다. 사건 되감기·창 기록 교체·단의 완료 창 수/마지막 시점과 완료 사건을 근거로 옛 꼬리를 제외하거나 새 단을 인정합니다. 덱의 쓰기 순서(단 기록 → 완료 사건 → 다음 단)에 맞는 새 CROSS/RM 등 완료 사건은 CSV 역행이 없는 정상 재개도 인정할 근거가 됩니다. 새 attempt 식별자를 덱/CSV에 추가한 것은 아니므로 어떤 파손에서도 옛/새 시도를 완전히 식별한다고 보장하지 않습니다.

초기 반례의 TIMEOUT, GUARD, 이동 중 TIMEOUT 및 같은 창 수 재시도에서 잘못 나온 `rho=0.2026077873428664%`는 더 이상 승인되지 않습니다. 교차 전의 옛 마지막 단이 하한을 부풀리던 재현은 `0.27014371645715524%`에서 새 시도 대조와 같은 `0.225119763714296%`로 바뀝니다. 소속을 결정할 관측이 부족한 경우 임의의 주 값이나 하한을 만들지 않습니다.

반대로 UB에서 첫 교차와 확인 둘이 승인 경계 이전에 이미 완료되었다면, 그 뒤 불명확한 꼬리 때문에 완료한 주 값을 버리지 않습니다. 해당 앞부분에 기존 끝점/S3/확인 검사를 다시 적용하며 원 CSV와 `read_run`의 기록은 보존합니다. 판독 결과에는 `resume_tail.status=UNCONFIRMED`, 경계 및 제외 행 진단을 남깁니다. 교차나 확인에 불명확한 단이 필요하면 계속 `UNIDENTIFIED`입니다.

이때 앞부분에서 성립하는 첫 주 값·끝점/M·0→M 보조 적분은 각 기존 관측 요건에 따라 판단하지만, 전체 궤적의 교차 합집합(`union_bracket_pct`)·비단조 여부·최종 분리·표면 관측은 미확인으로 남깁니다. `rank_eligible=True`만으로 순위 관계가 인증되는 것은 아닙니다. 실제 쌍 비교는 union도 요구하며, 독립 UB 재현의 관련 네 쌍은 모두 `UNIDENTIFIED`였습니다. 승인 경계 앞 교차 끝점의 fz를 NaN으로 바꾸는 대조는 여전히 주 값 `UNIDENTIFIED/rho=null`과 S3 사유를 냅니다.

### 정상 재개와 R10 양성 fixture

독립 검토가 초기 수정의 정상 재개 오거부를 발견하여 별도 시험을 먼저 실패시킨 뒤 수정했습니다. 생성 UT 덱의 실제 RESUME 제어 분기 k=0/1/2/3은 모두 RM_STOP, abort 없음이며 실제 arm CLI 네 건은 모두 OK (`rho=0.20260778734286913%`)입니다. 이 제어 흐름 재현은 합성 실행기로 수행했으며 LIGGGHTS 실행이 아닙니다.

R10의 기존 합성 CSV는 RESUME을 새 CROSS/RM 뒤에 붙여 실제 생성 덱 순서와 달랐습니다. RESUME을 새 완료 사건 앞에 옮겼고 창/단 CSV 바이트, 기존 `rho` 동일성 및 옛 행 두 개 제거 양성 단언은 유지했습니다. 고친 fixture는 수정 전·후 판독기 모두에서 같은 주 값으로 통과합니다. `dem_unloading_ulpr_fix_evidence_20261023/probes/r10-evidence/{before,after}/`와 `dem_unloading_ulpr_fix_evidence_20261023/probes/repro-tail-scope/results.json`에 전후 CSV·해시·판정이 있습니다.

### G2c 분류 정정의 범위

이 요청은 `codex_dem_unloading_kit_fix_recheck2_request_20261015.md` **§5 Q3의 “G2c 열 결손을 기존 FAIL로 둘지” 질문과 그에 대응하는 기존 분류 설명을 대체**합니다. 1저자의 ULPR-04 승인에 따라 필수 열 결손은 관측 미확인으로 처리했습니다. 같은 옛 문서에서 “Q3”로 부르던 문법 원자료 재판독 기능을 취소하거나 약화한 뜻은 아닙니다.

`UNCONFIRMED`는 모든 malformed 입력을 통과시키는 분류가 아니며 다음 제출 승인이 아닙니다. c26 결손 재현은 복원/UB gate 모두 rc2입니다. 필수 열이 있는 잘못된 BOX·가짜 ATOMS 헤더·다른 시점은 `VALUE_MISMATCH`/rc2이고 정상 대조만 RESTORED/rc0입니다. 덤프 검증의 범위는 완료되어 바뀌지 않는 직교 덤프입니다. BOX 수치나 PBC 표지의 물리적 동일성, 동시 쓰기 중인 파일의 원자적 읽기까지 인증하지 않습니다.

## 3. 시험 및 독립 재확인 — 단계별 수를 구분

초기 실패 시험, 구현자가 실행한 6개 변이, 최신 독립 검토자의 4개 변이는 서로 다른 증거입니다. 아래 수를 합쳐 전체 결함 공간을 검증했다고 주장하지 않습니다. 독립 v1의 이전 12종 변이와 구현자 G2 보강 단계의 변이도 최신 v2에서 모두 재실행한 결과로 세지 않습니다.

| 단계 | 실제 관찰 | 근거 |
|---|---|---|
| ULPR-01 첫 시험, production 수정 전 | 196개 중 5 실패 (191 통과) | `dem_unloading_ulpr_fix_evidence_20261023/tests_first/resume.log` |
| ULPR-03/04 첫 시험, production 수정 전 | gates 57개 중 17 실패; reader 183개 중 6 실패 | `dem_unloading_ulpr_fix_evidence_20261023/tests_first/dump-tests-first-{gates,reader}.log` |
| 독립 지적 정상 재개 회귀, 보정 전 | reader 201개 중 1 실패 | `dem_unloading_ulpr_fix_evidence_20261023/tests_first/resume-review-fix-test-first.log` |
| UB 완료 주 값 보존, 격리 수정 전 | reader 205개 중 1 실패; 깨끗이 분리한 UB fixture로 다시 확인 | `dem_unloading_ulpr_fix_evidence_20261023/tests_first/resume-tail-scope-test-first.log` |
| BOX 구조·G2c 시점 보강, 수정 전 | gates 202개 중 96 실패; reader 191개 중 5 실패 | `dem_unloading_ulpr_fix_evidence_20261023/tests_first/dump-tests-first-box-g2c-{gates,reader}.log` |
| **ULPR-02 구현자 변이 6개** | 최종 reader에서 앞 3개 거부 사유 줄 제거·뒤 3개 조건/가드 제거 모두 rc1, 각 R38 단언 실패; 예상 밖 실패 없음 | `dem_unloading_ulpr_fix_evidence_20261023/mutations/resume-six/results.json` |
| **최신 독립 v2 자체 시험** | **reader 214/214, gates 202/202**, 각 rc0·실패 0 | `dem_unloading_ulpr_fix_evidence_20261023/independent/v2/{reader,gates}-baseline.log` |
| **최신 독립 v2 추가 변이 4개** | `resume_uncertain` 생성 제거: R37 1 실패; 전체 union/nonmonotone 미확인화 제거: R37 1 실패; BOX 비유한 검사 제거: C6 36 실패; BOX 하한<상한 제거: C6 6 실패. 모두 예외 없이 의도한 단언에서 실패 | `dem_unloading_ulpr_fix_evidence_20261023/independent/v2/focused-mutations/focused_mutations.json` |
| 최종 문서/봉인 독립 감사 및 실제 승인 조건 3변이 | 문서·원자료·봉인 정합 확인. 승인 밖·비수치·상태 일치 조건을 실제 제거한 3변이가 R38 1/2/1 실패(상태 변이는 같은 가드의 R28 2개도 실패). 비수치는 다른 가드가 거부를 유지해 사유 단언 실패이며, 예외·무관 실패 0 | `dem_unloading_ulpr_fix_evidence_20261023/independent/PACKAGE-REVIEW.md`, `dem_unloading_ulpr_fix_evidence_20261023/independent/package/authorization-mutations-final/results.json` |
| 최종 통합 덤프 후속 변이/복원 | 구현자 재현: 10개 변이 모두 지정된 행동 시험으로 검출, 예외·무관 실패 0; 독립 원형 복원 probe 12개 기대 결과 | `dem_unloading_ulpr_fix_evidence_20261023/dump-final/SUMMARY.md` 및 원 로그/JSON |
| 최종 통합 키트 13개 명령 | **13개 모두 rc0**, reader 214/214·gates 202/202. 정식 봉인 검사 76파일·24규칙·문제 0 | `dem_unloading_ulpr_fix_evidence_20261023/final/summary.json` 및 13개 원 로그 |
| 최종 저장소 fullgate | `dem_unloading_ulpr_fix_evidence_20261023/full_gate_receipt.json`의 최종 상태/rc로 확인. PASS 전에는 전달 불가 | 같은 receipt가 가리키는 전체 원 로그 |
| 비변경 대상 바이트/봉인 | 생성 덱 64개·history 16파일·파라미터·LHS 봉인 대상 32개가 출발점과 동일 | `dem_unloading_ulpr_fix_evidence_20261023/baseline_files_sha256.json`, `dem_unloading_ulpr_fix_evidence_20261023/scope-verification.json` |

테스트 수가 단계마다 다른 이유는 첫 red 뒤 양성 대조·모든 필수 열·독립 반례를 추가했기 때문입니다. 최종 214/202개 전체가 최초 red 단계에 존재했다고 주장하지 않습니다. 초기 전체 환경 gate의 Python 환경 실패 로그는 보존하고, 최종 fullgate 판정과 구분합니다.

내부 독립 v2의 입력은 코드 diff와 실제 코드이며 구현자 노트를 읽지 않았습니다. 승인 없이 구현자 주장을 받아들인 검토는 아니지만 외부 독립 리뷰를 대신하지 않습니다. 검토 사본과 최종 발송 코드의 일치는 다음 해시 및 외부 pin으로 확인해 주세요.

| v2 검토 사본 | SHA256 |
|---|---|
| `dem_unloading_ulpr_fix_evidence_20261023/independent/v2/ul_reader.reviewed.py` | `34b46ebcf4530989917493f20d2d953043209e36d89e6b8282a2d629050a078d` |
| `dem_unloading_ulpr_fix_evidence_20261023/independent/v2/ul_gates.reviewed.py` | `c8d45a9cf75f0806e612d810942d23adea4b40feaa5f31f7d279eb8386358de6` |

보고서는 `dem_unloading_ulpr_fix_evidence_20261023/independent/RECHECK-v2.md`입니다. 정상 재개, 복원, edge, 실제 downstream `arm/select/report/gate UVa/gate G_UB` 로그·JSON은 `dem_unloading_ulpr_fix_evidence_20261023/independent/v2/` 아래에 보존했습니다. downstream 재현에서 원 CSV 세 개의 SHA256은 불변입니다. 이는 별도 합성 UB 사례이며 UTc의 새 물리 궤적을 실행한 결과가 아닙니다. 이번 수정·검토에서 새 LIGGGHTS/외부 GPU/물리 실행은 **0건**입니다.

## 4. 남겨 둔 항목과 재현

기존 `_i`/사건 파싱은 RESUME k=`3.49`를 사전에 반올림하여 `(3,3410000)` 승인으로 읽는 잔여가 있습니다. v2에서도 관찰되었고 이번 수정이 새로 도입한 동작은 아닙니다. NaN/inf/넘침 거부와 별개이며 R38을 소수·유니코드 입력 전체의 정수 문법 검증으로 해석하면 안 됩니다. `edge_probe`는 승인 집합을 관찰했을 뿐 이 입력으로 잘못된 최종 물리값이 승인된 것을 입증하지 않았습니다. 후속 처리 범위·우선순위는 별도로 판정해 주세요.

아래 `$REPO`는 review pin의 checkout, `$E`는 그 checkout의 근거 폴더, `$OUT`은 checkout 밖 새 출력 폴더입니다. 실행 환경은 Python 3.11.17을 사용했습니다. 원 로그를 덮어쓰지 말고 새 OUT으로 재현해 주세요.

```bash
KIT="$REPO/docs/data/ps45_unload_20261009"
E="$REPO/docs/reviews/dem_unloading_ulpr_fix_evidence_20261023"
python -I "$E/tools/mutation_check.py" --kit "$KIT" --out "$OUT/resume-six"
python -I "$E/independent/deck_probe.py" --repo "$REPO" --out "$OUT/deck-probe"
python -I "$E/independent/restore_probe.py" --repo "$REPO" --out "$OUT/restore-probe"
python -I "$E/independent/edge_probe.py" --repo "$REPO" --out "$OUT/edge-probe" --fixtures "$OUT"
python -I "$E/independent/v2/downstream_probe.py" --repo "$REPO" --out "$OUT/downstream"
python -I "$E/independent/v2/focused_mutations.py" --repo "$REPO" --out "$OUT/focused-mutations"
python -I "$E/tools/run_suite.py" "$KIT" "$OUT/suite"
```

변이 재현기는 대상 소스 문자열을 확인합니다. 다른 판에서 해당 문자열이 달라 멈춘 경우를 결함이 시험에 검출된 결과로 세면 안 됩니다. 원 ULPR 발송 전 사전 리뷰의 옛 scratch 폴더를 이번에 재입수했다고 주장하지 않으며, 현재 근거는 보존한 ledger 지적에서 새로 구성한 재현과 독립 검토 재현입니다.

## 5. 리뷰어에게 부탁드리는 판정

1. **ULPR-01:** 등록된 한 번의 RESUME 승인 아래 사건·창·단의 근거가 일관되게 결합되는지, 부분 쓰기/같은 시점 충돌/새 창 없음에서 소속 불명인 자료가 새 정상 관측으로 승인되는 반례가 남는지 확인해 주세요.
2. **정상 재개/R10:** CSV 꼬리 없는 k=0/1/2/3 실제 생성 덱 재개와 R10 사건 순서 교정이 양성 의미를 보존하는지, 단언을 낮춰 회귀를 가린 부분이 없는지 확인해 주세요.
3. **완료 주 값과 꼬리:** UB의 이미 완료한 주 값은 유지하되 불명확한 꼬리를 필요로 하는 주 값·교차 합집합·비단조·최종 분리/표면은 승인하지 않는지, selection/gate/report의 소비와 `rank_eligible`의 한정이 서로 맞는지 확인해 주세요.
4. **ULPR-02:** 6개 변이가 각각 문제 조건 때문에 실패하는지, 해시/재판독 rc 보호가 유지되는지 확인해 주세요. 기존 k=`3.49` 반올림은 별도 잔여로 두어도 되는지, 발송 전 추가 차단 사유인지 구분해 주세요.
5. **ULPR-03:** 고유 ID·완전한 구조·헤더/BOX·S0/R_M 시점 결합·원 토큰 비교가 정상 대조를 보존하면서 지적 반례를 차단하는지, 완료된 직교 덤프라는 보장 범위를 문서가 넘지 않는지 확인해 주세요.
6. **ULPR-04:** 필수 열 결손만의 `NOT_COMPUTED/UNCONFIRMED`와 구조·시점/값 위반의 `VALUE_MISMATCH`, 기술 실패의 `SYNTAX_FAIL` 우선순위가 등록 취지와 맞는지 확인해 주세요. 기존 재확인2 §5 Q3을 이 분류로 대체하는 데 동의하는지도 부탁드립니다.
7. **최종 묶음:** 13개 명령/fullgate 확정 로그, 검토 사본/최종 pin, 문서·규칙·정식 봉인 및 비변경 대상 대조가 일치하는지 확인한 뒤 ULPR-01–04 각각 `verified` 가능/추가 수정/미확인을 나눠 주세요. 코드 재확인 통과와 새 실제 실행·물리 GO는 별도로 판정해 주세요.

추가 finding에는 재현 입력·명령·실제/기대 출력과 적용 pin을 부탁드립니다. 외부 발송 및 원장 최종 상태 반영은 1저자/원장 담당자가 수행합니다.
