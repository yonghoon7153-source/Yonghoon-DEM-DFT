# 접촉망 세대 2 — 재검증 5 판정 (2026-10-07)

## 0. 결론과 범위

**194 생산·v1.3 배포는 아직 HOLD. 새 P1은 발견하지 않았다.**

직전 세 수정은 실제로 진전됐다. 다시 읽기 상세의 필수 검사·케이스 집합 검사는 작동하고, 실행 단계의 영수증 쌍이 통째로 사라지는 반례도 감사 CLI가 잡는다. 제출된 옛·새 시범 기록을 무효라고 판정하지 않는다. 그러나 **배포 시 단계 결합의 내용 미검사**, **case15의 다른 실행 실패를 정상 음성대조로 오인**, **S0b가 실패/누락 상세를 PASS 요약으로 덮는 경로**가 남는다. 모두 아래에서 정상 대조군을 먼저 통과시킨 뒤 재현했다.

- 리뷰 핀: `aa7ec7fe98e8684f1a2138665f9eba978366c229` — 요청서의 WSL 증거 반입까지 포함. 브랜치 `claude/stoic-knuth-NObVQ`.
- WSL 사전 점검 핀: `839dbac6bf6185f7bc7f1b7a08d21b6b469a04ef`. 두 핀의 **scripts/·webapp/ Git blob 차이 0**. 봉인된 수치 코드 32개도 manifest와 바이트 일치.
- 독립 사본 469파일을 Git blob SHA-1·SHA-256으로 확인했다. 현재 작업 폴더는 Git checkout이 아니므로 원격의 핀별 파일을 읽어 검증한 사본이다. checkout·fetch·rebase·원장 수정·생산 코드 수정은 하지 않았다.
- 실행 범위: 합성 관문/감사 시험, 이미 존재하는 case15 덤프의 CPU 후처리, 그 경로에 대한 오류 주입. **DEM/MPM 시뮬레이션·194 생산·S3 실행은 하지 않았다.**
- 등록 §3b·§4·§9-4는 요청서대로 **저자 비준 전 제안**이다. 이 리뷰 승인이나 WSL 점검 성공을 그 비준 또는 발사 승인으로 해석하지 않는다.

### 직전 항목의 상태

| 항목 | 판정 | 무엇이 닫혔고 무엇이 남았는가 |
|---|---|---|
| G2RR4-01 | **부분** | 원래의 M2 false·cases 결손·관측 내부 problems/outside 은 거부. 새로 필수화한 stage_binding의 시도별 내용은 배포 관문이 읽지 않음 → G2RR5-01 |
| G2RR4-02 | **감사 생산 경로 닫힘** | 단계별 쌍 결손·중복 대체·미분류 단계·Stage E·계획 결손/불일치 거부. 정상·CSV 생략·옛 현재기록 대체·허용 재시도는 통과. 배포까지 포함한 보증은 G2RR5-01이 남음 |
| G2RR4-03 | **코드의 관측 필수화 닫힘 / 등록 부분** | production194 관측 OFF 거부, pilot3 선택 허용. 비준은 미결. 추가된 case15/S0b에는 G2RR5-02·03, 제안의 집계 문구에는 G2RR5-04 |

## 1. G2RR5-01 · P2 — stage_binding이 비거나 실패해도 배포된다

**위치:** `scripts/lhs_release_build.py:1340–1350` (`v13_audit_observation_problems`). 생산자가 실패 상세를 만드는 곳은 `scripts/run_network_194_parallel.py:615–628`.

관문은 `stage_binding.schema`, `attempts`의 dict 여부, 그 **키 집합**과 completed_attempts의 일치까지만 본다. 각 값이 dict인지, `expected`와 `observed`의 단계·수가 같은지는 보지 않는다.

상세 production194 정상 픽스처 위에서 다음을 각각 넣었다. 실제 194를 실행한 시험이 아니라 **배포 증거 관문 시험**이다.

| 입력 | build | check_v13 |
|---|---|---|
| 상세 정상 대조군 | 생성 | `[]` |
| 첫 시도의 binding 값만 `null` | 생성 | `[]` |
| expected parser=1을 두고 observed parser 키만 삭제 | 생성 | `[]` |
| observed parser=0 | 생성 | `[]` |
| 관측에 계획 밖 프로세스 추가 | 생성 | `[]` |
| 원래 반례: M2 ok=false / cases=[] / 내부 problems·outside | 거부·산출 없음 | 실패 |

이를 임의 JSON 모양 문제로만 두지 않았다. 별도 **실제 audit CLI**에서 parser 시작·끝 영수증을 함께 지우면 rc=1이고, 그 감사가 실제로 내는 상세는 `expected parser=1`, `observed parser 없음`, `import_observation.problems=[]`다. 단계 부족 사유는 최상위 `import_observation_problems`에만 실린다. 이 **실제 생성된 실패 binding**을 상세 194 픽스처에 넣으면:

1. 최상위 실패 목록 유지 → ReleaseError, 산출 없음.
2. **최상위 실패 목록 하나만 `[]`로 변경** → build 성공, check `[]`.

따라서 “새 감사 CLI도 못 잡는다”는 판정은 아니다. CLI는 잡는다. **배포 경계가 요약과 모순되는 새 상세를 거르지 않는다**는 판정이다. 제출된 시범이 훼손됐거나 σ가 틀렸다는 증거도 아니다. 모든 원자료·영수증·도장을 일관되게 위조한 사례가 아니라, 한 기록 내부의 결손/모순이다.

기존 배포물의 증거 파일을 수정하고 캐시된 해시를 그대로 두면 파일 해시 검사는 잡는다. 위 핵심 반례는 **잘못된 기록을 처음 입력받아 새로 만드는 경로**라 그 사후 무결성 검사로 막히지 않는다.

**무너지는 결론:** “생산194 배포는 시도별 단계 결합 상세까지 통과한 기록만 받는다.”

**최소 해결 증거:** 공용 배포 관문에서 시도 값의 구조, 필요한 expected/observed 카운터, bool이 아닌 유효 정수 개수, 단계·개수의 일치를 검사한다. null·parser 결손·0·계획 밖 프로세스와 실제 실패 binding/빈 요약을 build와 check 모두 거부하고 정상 상세는 통과해야 한다. 전체 원자료 재계산이나 전면 서명 체계는 요구하지 않는다. 재시도 때문에 전체 started=finalized를 강제해서도 안 된다.

재현(새 이름 사용): `python run_checks.py r5_release_contract -- --output-name rerun_release`, 이어 `python run_checks.py r5_release_real_binding -- --output-name rerun_binding`.

증거: `evidence/r5_release_contract/results.json`, `evidence/r5_release_real_binding/results.json`, `evidence/r5_observation_run2/pair_missing_parse_liggghts/audit.json`.

## 2. G2RR5-02 · P2 — 망 실행이 PermissionError여도 case15 음성대조 4개가 PASS

**위치:** `scripts/wsl_network_smoke.py:568–595`, `:617–619`; 별도 원자료 탐침 호출은 `:325–328`.

①은 failed·실패 단계 이름·게시 없음만 본다. ③·④는 파이프라인 뒤 별도로 실행한 `case15_channel_probe`를 본다. **실제 파이프라인의 이번 실패가 지정한 물리/입력 거부였는지 결합하지 않는다.**

단순 수작업 보고서가 아닌 다음 실행으로 재현했다.

- 커밋된 case15 atom/contact/STL/deck를 실제 `smoke.child_case`에 넣었다. 네 원자료 SHA 일치.
- Parse·Contact Analysis·Coverage Physics vs Hertzian은 실제 원래 코드로 실행, 모두 rc=0.
- `pipeline_service._RUNNER`의 **network_conductivity.py 하위 프로세스 호출 한 곳만** `PermissionError`로 거부했다. 소스 파일은 수정하지 않았다.
- 실제 보고: Network stage rc=1, per-mode 산출물 없음, attempt reason=`PermissionError … 파일 없음; per-mode 산출물이 하나도 없다`, 게시/반환 run id 없음, τ 세 모드 NOT_COMPUTED.
- 이후 독립 원자료 탐침은 정상적으로 계산된다. **평가기 결과 6/6 PASS = 자식 정상 종료·원자료 SHA 2개 + 음성대조 4개**, 실패 0.

즉 물리적 거부를 검사하려는 스모크가 **솔버를 한 번도 실행하지 못한 환경/호출 오류**를 같은 성공으로 받는다. 모든 기록의 위조가 아니며, 실제 실행 경계의 오류 주입이다.

**무너지는 결론:** “case15 음성대조 PASS가 이번 생산 파이프라인에서 지정된 거부 원인이 실제 발화했음을 증명한다.” 별도 함수에서 원인을 재현한다는 더 좁은 결론은 살아 있다.

**최소 해결 증거:** 독립 원자료 탐침을 유지하되, 실제 시도에도 구분 가능한 결과를 요구한다. 지정된 입력/채널 거부와 `PermissionError`, 실행파일 없음, timeout, traceback 등 실행 실패를 별도 상태로 나누고 후자는 TECH/FAIL로 남긴다. 이번 시도 신원·입력과 결합된 구조화 사유/산출 증거를 쓰는 것이 좋다. 잘린 300자 문자열을 확장해서 grep하는 것만으로 의미 계약을 대신하지 않는다. 정상 case15, 위 호출 거부, 누락 산출물, 다른 예외를 각각 넣어 지정한 거부만 PASS인지 보여야 한다.

**제출된 WSL 실행을 무효화하지 않는다.** 받은 case15 stage/attempt에는 실제 `boundary_overlap`와 Physics 열의 음수 면적 거부가 남아 있다. 이 finding은 그 정상 사례가 아니라 검사기의 오수용 반례다. 수치 솔버나 194 경계 규약을 바꿀 근거도 아니다.

재현: `python run_checks.py r5_case15_pipeline_fault`

증거: `evidence/r5_case15_pipeline_fault.json`, `.log`; 주입된 호출·실제 단계·attempt·검사 6개를 모두 보존했다.

## 3. G2RR5-03 · P2 — S0b가 상세 실패를 다시 PASS로 만든다

**위치:** `scripts/g2_network_reread.py:548–565`.

S0b는 truthy `negative_control`이면 종류를 가리지 않고 S0에서 제외한다. 해당 이름 접두어의 PASS 행이 **4개 이상**인지 볼 뿐, 네 서로 다른 필수 검사인지·등록 marker인지·해당 보고 상세와 일치하는지는 확인하지 않는다. 원자료 SHA·자식 프로세스 실패는 그 접두어 밖이라 보지 않는다.

정상 관통/비관통/clamp 게시 폴더는 실제 합성 생산 코드로 만들고 K1–K7을 통과시켰다. case15만 변이했다.

| 변이/대조 | `--smoke-root` rc · S0b |
|---|---|
| 제출된 정상 case15 기록 | 0 · PASS |
| 음성대조 PASS 행 **하나를 네 번 반복** | 0 · PASS |
| marker를 등록되지 않은 문자열로 교체 | 0 · PASS |
| `negctl` 상세 삭제, PASS 행 유지 | 0 · PASS |
| τ에 수치 추가 / 이온 잔차를 기준 밖으로 변경, PASS 행 유지 | 0 · PASS |
| `raw_sha_ok=false`로 바꾸고 **evaluate를 새로 실행** → 원자료 SHA FAIL, 음성대조 4개 PASS | **0 · PASS** |
| PASS 행 하나를 FAIL / 3개만 남김 / marker 제거 | rc=1 — 올바른 거부 |

특히 SHA 사례는 “요약을 일부러 거짓 PASS로 만든 것”도 아니다. **현재 생산 평가기가 실제로 실패 판정을 낸 보고서를 S0b가 성공으로 재분류**한다.

**무너지는 결론:** “S0b 성공이면 등록된 case15의 원자료·지정 원인·이온 정상·비노출 증거가 함께 갖춰졌다.” G2RR5-02를 고쳐도 이 소비자 쪽 구멍은 별도로 남는다.

**최소 해결 증거:** 등록 marker/kind/범위만 허용하고, 필수 검사에는 안정된 ID와 정확한 cardinality를 둔다. case15의 프로세스·원자료 신원 필수 검사도 포함한다. 소비자가 공유 검증 함수로 상세를 다시 판정하고 기록된 검사/요약과 대조해야 한다. unknown marker·중복 검사·상세 결손·수치 모순·실제 SHA FAIL을 거부하면서 정상 미퍼콜 대조군은 계속 통과해야 한다. 무조건 모든 실패 케이스를 면제하거나 숫자 4를 다른 숫자로 늘리는 처방은 답이 아니다.

재현: `python run_checks.py r5_case15`

증거: `evidence/r5_case15_results.json`, `evidence/r5_case15_s0b_*.json`.

## 4. G2RR5-04 · P3 — 등록 제안의 총수 등식은 허용 재시도와 맞지 않는다

**위치:** `docs/reviews/lhs_network_batch_registration_20261007_g2.md:217`; 코드 예외는 `scripts/run_network_194_parallel.py:578–628`.

“시작=끝맺음·완료 시도194·stage_binding194”는 **재시도 없는 깨끗한 1회 실행의 기대**로는 맞다. 모든 적법한 실행의 합격선으로는 틀리다. 실제 audit CLI 합성 재시도 시험:

| 한 최종 케이스의 이력 | started/finalized | completed/bound | audit |
|---|---:|---:|---|
| 미완료 시도1의 시작 영수증 + 성공 시도2 | 6/5 | 1/1 | rc0 · SEALED1 · 미완료 1개 정보 |
| 성공 시도1 + 성공 시도2, 각각 stage 사본 | 10/10 | 2/2 | rc0 · SEALED1 |
| 앞 성공의 단계 증거까지 없음 | 10/10 | 2/1 | rc1 — 올바른 거부 |

**권고 문안:** “최종 등록 케이스 집합은 194이고 모두 요구 봉인을 만족한다. 완료 시도 **전체의 키 집합**과 단계 결합 키 집합이 같고, 각 시도의 expected=observed이다. 완료 시도의 미최종 영수증은 없어야 한다. 비완료 시도의 미최종 영수증은 Q2 규칙으로 따로 보고한다. 재시도 없는 경우에 한하여 전체 시작=끝맺음, 완료·결합 시도194를 기대한다.”

집계 등식 때문에 정상 중단 이력을 삭제하거나 이미 성공한 수치 계산을 재실행시키지 말 것. **문서 수정 항목이지 현재 감사 코드의 과잉차단은 아니다.**

재현(새 이름 사용): `python run_checks.py r5_observation -- --output-name rerun_audit`, 이어 `python run_checks.py r5_observation_retry -- --baseline-output rerun_audit --output-name rerun_retry`.

증거: `evidence/r5_observation_retry/results.json`.

## 5. 제출 증거의 독립 검산 — 살아 있는 근거

받은 tar SHA-256=`41a755974d99aa0d1c8315cf3454cd15a7eeabdca31062c999f25c67118d2939`, 54,375 bytes, 디렉터리 포함 78 entries. 안전한 경로·일반 파일만 추출했다. **단계별 stdout 10개·rc 10개**가 있으며 rc는 모두 0이다. rc가 있다는 것과 그 의미까지 통과했다는 것은 구분했다.

`probes/submitted_verify.py`의 독립 대조 **61/61**:

- 새 pilot의 시작/끝 영수증 15쌍: proc·pid·실행/케이스/run/attempt 신원 일치. 단계별 실물 = 각 케이스 워커1+파서1+접촉분석1+피복1+망1. 2 bimodal·1 mono 경로.
- 실제 관측된 리포 Python 모듈 30개 ⊆ 봉인32. 코드 파일들의 현재 bytes와 manifest hash도 32/32 일치. `code_fp=e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`.
- 세 `out/status.json`의 canonical JSON SHA를 직접 다시 계산 → attempts[].seal.record_sha와 일치. stages 전체 → 새 시도 사본과 일치. audit expected/observed도 실제 영수증 재계수와 일치.
- 옛·새 pilot reread JSON은 각각 meta10·cases3·n_fail0, 새 상세 계약 통과. 옛 결합 출처는 현재 기록, 새 결합 출처는 시도 사본이라는 구분도 맞다.
- 단, **옛 ROOT 전체가 이번에 다시 제공된 것은 아니며**, 게시 dual/full_metrics 원파일도 새 tar에 없다. 이번 검산을 “WSL 원 ROOT를 이 기계에서 전부 재실행·재감사했다”로 표현하지 않는다. 옛 full record 대체 경로 자체는 합성 CLI 시험과 받은 재감사 기록으로 교차검토했다.

### case15 원자료 재계산

상자100×100 µm, 판 간격19.1455 µm, 원자65,970개·접촉182,995개. 압축 푼 atom/contact/STL/deck SHA 모두 기준과 일치. 실제 build_network/solve_network 6조합 결과:

| 채널 | 결과 |
|---|---|
| ionic Hertz | q=`0.0003263508259103751`; conservation=`3.0024201089821724e-9`; residual=`9.838873256790492e-11` |
| ionic Physics | q=`0.00036224724452177176`; conservation=`6.322933781612321e-9`; residual=`9.556129760264176e-11` |
| electronic Hertz/Physics, thermal Hertz | `not_computed/boundary_overlap`; B∩T IDs=`24,40,57,103` |
| thermal Physics | ValueError: `(31,29241)`의 `ligg_area < 0 (-0.186036)` µm² |

음수 면적은 두 행: `(31,29241) −0.186036 µm²`, `(38,29241) −0.186264 µm²`. Physics가 첫 행에서 중단한다는 설명이 맞다. **SELF-94 정정은 수용.**

8자리 q 기준은 이 고정 fixture의 회귀 비교로 적절하다. 반올림 반칸 `5e-9`는 현재 q 대비 약 `1.53e-5`·`1.38e-5` 상대범위이며, 실험 오차막대나 모형 정확도를 뜻하지 않는다. 증서는 별도 판정해야 하고 유한·비음수 잔차/보존오차를 엄격히 읽는 것이 좋다. 새 잔차 문턱 또는 수치 모델 변경은 이번 반례의 해결책이 아니다.

## 6. Q1–Q8 직접 답

**Q1 — 부분.** 생산자 검사 ID를 한 곳에 둔 shared contract, 모르는 ID 거부, K1b 선택, strict bool, 상세 실패 재계수, 등록 집합 일치는 적절하다. 정상 상세 fixture도 실제 통과한다. 다만 이는 **검사 결과 기록의 구조 계약**이지 K1–K7의 의미 정확성까지 독립 증명하는 것은 아니다. 종전 상세 결손 반례는 닫혔으나 새 observation stage 상세 보증은 G2RR5-01이 남는다.

**Q2 — 현재 봉인 경로에서는 동의.** stages는 import 훅과 다른 호출부가 남기며, 실제 이름별 기대 프로세스를 형성한다. 실행 단계와 영수증 두 벌 중 영수증만 동시 소실하는 기존 부류는 닫혔다. 모든 단계를 기록에서 같이 없애고 해당 SHA·사본까지 맞춰 고치는 부류까지 막는 독립 관측계는 아니다. 그 한계를 인정하되 이를 이유로 이번 4/4·2/2 반례의 닫힘을 부정하지 않는다.

**Q3 — 제한적으로 수용.** 현재 기록을 실제로 쓴 시도와 record_sha가 결합될 때만 대체한다. 다른 과거 성공 시도에 현재 기록을 빌려주면 안 된다. 시험상 현재 시도 fallback은 통과, 앞 성공 시도의 계획 결손은 거부한다. 새 사본≠현재 stages도 거부한다. 옛 시범을 사본 부재만으로 전부 다시 돌릴 필요는 없다.

**Q4 — 동의.** `stop_after='network'`에 한정한 닫힌 표가 맞다. 이 실행기에서 Stage E가 나타나면 rc1로 거부하는 시험도 통과했다. 스모크 일반 경로의 Stage E를 이유로 표를 느슨하게 넓힐 필요가 없다.

**Q5 — 현 핀·현 경로에 한정해 동의.** 검사한 봉인32에 fork/process-pool 사용은 없고, 단계 훅 우회로 영수증이 없어지면 현재 이름별 결합이 잡는다. 정적 정규식 자체는 보편적 금지 증명이 아니다: `from os import fork`, os 별칭, getattr 형태를 inert fixture에 적으면 탐지하지 못한다(실행하지 않음). 현재 코드에 그 경로가 있다는 증거는 없으므로 이를 새 P1/P2나 이번 발사 차단 근거로 올리지 않는다. 코드 변경 시 봉인·호출경로 재검토 필요. C 확장·외부 프로세스까지 Python 훅이 전부 관측한다고 주장하면 안 된다.

**Q6 — 관측 필수화 제안은 비준하면 닫힐 수 있으나 전체 §7-3은 아직 부분.** 생산194 관측 OFF는 발사/감사/배포에서 거부하고 시범3 선택 경로와 구분한다. 다만 새 스모크 기대를 뒷받침하는 G2RR5-02·03, 배포 상세 G2RR5-01, 재시도 문구 G2RR5-04를 처리해야 한다. 원 실패 보존·변경 이력·비준 분리는 올바르다.

**Q7 — 측정 내용/기준은 수용, 통합 성공 판정은 반례.** 원자료 6조합과 숫자 자체는 재현됐다. 물리/입력 음성대조의 범위도 타당하다. 하지만 별도 원자료 탐침 성공은 실패한 실제 하위 프로세스의 원인 증서가 아니다. G2RR5-02·03을 닫기 전에는 “음성대조 4PASS”만을 발사 자격으로 쓰지 않는다.

**Q8 — 추가 잔여가 있다.** 아래 최소 목록을 닫고 별도 저자 비준·발사 승인을 받아야 한다. 현재 시범 전체/기존 수치 배치를 다시 계산하라는 요구가 아니다. 새 결함의 정상·음성 회귀와 영향받은 검사 경로 재확인이 먼저다. 완료 뒤의 SEALED194·상세 다시 읽기·인계/배포 검사는 여전히 필수이며, 발사 전 리뷰가 그 사후검사를 대체하지 않는다.

## 7. 최소 해제 목록 — 범위를 늘리지 않는다

1. **배포 관문:** 시도별 stage_binding 내용 검사와 G2RR5-01 정상/변이 회귀. 원 수치 재계산 불필요.
2. **스모크 생산자:** 실제 망 호출 실패와 지정된 내용 거부를 구분. PermissionError 반례를 FAIL/TECH로, 진짜 case15는 PASS로.
3. **스모크 소비자:** 등록 marker·서로 다른 필수 검사·원자료/프로세스 신원·상세를 함께 검증. 실제 SHA FAIL 보고서를 S0b가 성공으로 바꾸지 않게.
4. **등록:** §217 집계 등식을 재시도 예외와 합치고, §3b·§4·§9-4 제안을 저자가 명시 비준. 그 뒤 활성 명령이 무엇인지 분명히 보존.
5. 영향받은 경로의 정상+음성 대조를 재확인한 뒤 **별도 발사 승인·새 ROOT**, 이번과 같은 관측 ON·코드 봉인 유지. 수정이 검사 도구에 한정되면 수치 코드32의 봉인이 바뀌는지 따로 계산한다. 인계 도구 지문 변경은 기록한다.
6. 실행 뒤 최종 등록194·SEALED·전체 완료 시도 결합·audit·production194 상세 재독해·인계/배포 관문. S3는 이 판정과 별개이며 실행 승인하지 않는다.

## 8. 시험 장부와 재현 한정

| 검증 | 결과 |
|---|---|
| 로컬 reread selftest | 20/20 |
| 로컬 publication/handover | 32/32 |
| 로컬 role contract | 44/44 |
| 로컬 release 전체 | 171 PASS / 2 FAIL |
| 독립 staged audit CLI | 17/17 기대 결과 |
| 독립 retry audit CLI | 4/4 기대 결과 |
| 제출 증거 독립 대조 | 61/61 |
| case15 원자료6조합 + 실제 파이프라인 오류 주입 | 정상 수치 재현 + 잘못된 6/6 PASS 반례 |

release 2FAIL은 V10a(Windows 경로 표현 vs `/H/lhsx` POSIX 기대), V16a(Git archive 사본에 `.git` 없음)다. 숨기거나 전체 로컬 초록으로 쓰지 않는다. 받은 WSL 자체 시험은 reread20·runner117·smoke14/14 rc0이며, 이를 내가 로컬에서 runner117을 재실행한 것으로 쓰지 않는다.

배포 탐침은 커밋된 상세194 fixture를 쓰고 `v13_reread_tau`만 시험용으로 대체한다. build/check/상세 판정 함수는 원 코드다. 따라서 **관문 증거의 수용/거부**만 검증하며 실제194 수치·전 원자료를 인증하지 않는다. 반대로 G2RR5-02의 최종 탐침은 실제 case15 스모크 경로를 사용하고 망 하위 프로세스 실행 경계만 거부했다.

재현 명령은 이 묶음의 루트(`run_checks.py`가 있는 폴더) 기준이다. 재실행은 새 출력 폴더를 쓰고 기존 제출/증거를 덮지 말 것. Python·numpy·scipy·networkx·Flask·matplotlib가 필요하다. 런처 발사가 아닌 합성 감사 CLI 및 기존 덤프 후처리만 호출한다. `README_REVIEW.md`에 순서·보존 범위를 적었다.

**HOLD — 새 수치 P1 없음. 검사 경계의 P2 세 건과 등록 집계 문구를 닫은 뒤 재판정.**
