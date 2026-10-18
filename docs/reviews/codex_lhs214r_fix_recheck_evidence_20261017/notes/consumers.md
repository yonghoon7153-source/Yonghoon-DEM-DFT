# L214R 소비자·배포 독립 재확인

코드 핀 `60ba39e224aff48a030dccfe750342f3bf9db61f`, 기준 `6cb2569569ec74b7f5a96e0ef19494e872da5272`. 고정 `source/`·`base/`, 생산 코드·Git·등록·원장 무변경. 실제 214 생산/재계산/배포가 아닌 작은 합성 생산자와 선언된 합성 배포 fixture다.

## 판정

- **L214R-02 원 반례 닫힘:** 실제 생산자의 L0/L1/L2 H0 FULL 모형 한계 모두 독립 표지로 인계되고 실제 `build_v13`가 HOLD 한다. 띠 표시 우선순위는 그대로다. 제출 47/47 및 독립 원 탐침이 일치한다.
- **L214R-11 닫힘:** `10**400` 장부 수 네 종류를 실제 게시 폴더 사본에 넣어 stop·reread를 호출했다. 전부 사유로 거부, 수 변환 예외 없음. 숫자 형식 판정도 bool·str·NaN·inf·큰 정수를 거부한다.
- **새 L214RR-01 P2:** 숫자로 재구성되는 H0 q>1.5를 `computed` 라벨로 되살리면 모형 한계 표지가 False가 되고 실제 stop/P0–P4/다시 읽기/인계/배포가 통과한다. 수치 담당자가 찾은 반례를 아래 실제 소비 경로로 확장했다. 원 L214R-02의 BAND_FALLBACK 누락과는 별개다.
- 알려진 K5/K8은 아래 한정 하에 그 자체로 새 GO 차단 사유를 추가하지 않는다. 다만 `check_v13`가 원천을 새로 읽는 검사라고 설명하면 틀린다.

## 원 탐침 재사용과 L214R-02

`probes/consumer_chain_derivative.py`는 이전 `../lhs214_fix_reverify_20261015/probes/l214_consumers.py`가 있으면 그 원문을 읽고, 없으면 동봉한 `probes/l214_consumers_20261015.py.b64`를 메모리에서 복호해 실행한다. 두 경로 모두 실행 전에 원 SHA256 `804de03d58902862f74006afaf1e24dfed97a42a254d02b86a4cc98797de243a`를 강제 대조한다. 이전 검토 폴더 없이도 원 탐침을 재현할 수 있다. 변경은 `__file__`을 새 검토 폴더로 결합하고 임시 경로 한 줄을 `review/tmp`로 바꾸며 외부 의존성 경로를 공급하는 것뿐이다. 판정식·수치·생산 함수는 바꾸지 않았다.

실제 작은 생산자 → 웹 게시 → `load_tau_results(expected_generation='g2')` P0–P4 → `build_handover(webapp_groups='tau')`를 재실행했다.

| 사례 | H0 원 수치 q | H0 τ 표시 | 독립 표지 | 주 타깃 관문·실제 build |
|---|---:|---|---|---|
| ml_hertz / L0 | 1.6231747351909995 | NOT_COMPUTED / full_over_conduction | True | HOLD |
| independent_l1_h0 | 8.927503013108073 | BAND_FALLBACK / 공란 | True | HOLD |
| independent_l2_h0 | 35.710012052432674 | BAND_FALLBACK / 공란 | True | HOLD |
| ml_physics | H0 정상, Physics만 한계 | H0 OK | False | 주 타깃 문제 없음 |
| ml_el | 이온 정상, 전자 한계 | H0 OK | False | 주 타깃 문제 없음 |

근거: `evidence/consumers_probe.json`, `consumers_handover_rows.json`, `consumers_release_probe.json`. 새 표지는 `source/scripts/tau_flux.py:399`의 공용 판정과 `:1295` 독립 생성에서 온다. 배포 주 타깃 gate `source/scripts/lhs_release_build.py:693`은 상태 또는 문자열 표지를 읽고 누락·알 수 없는 값·모순을 거부한다. 같은 함수가 build `:2288`과 check `:2497`에서 쓰인다.

제출 `scripts/test_l214r02_model_limit_flag.py`는 수정 없이 실행하여 **47/47, rc 0**. 특히 L1_none/L1_phys/L2_h12의 실제 build/check 통과로 BAND_FALLBACK 전체를 과잉 차단하지 않음을 확인한다. `evidence/consumer_submitted_r02.json`·`.log`.

이전 일곱 음성 변이도 실제 content/record/stop/reread/P4 조합으로 재실행했다. CF 잔차·bulk_model 결손은 record/stop에서, 잘못된 withheld q·다른 채널 실패·모르는 FULL 사유·Physics에 H12 증서 역할은 stop에서 거부한다. 모든 변이의 인계는 거부된다. `evidence/consumers_negative_paths.json`.

## L214RR-01 P2 — H0 q 상한을 라벨 변경으로 통과

근거 위치: `source/scripts/tau_flux.py:234` computed 레코드 기술 검사, `:743` `_cert_published_problem`, `:787`–`:812` q·차원 σ 재구성/반올림 비교, `:399`–`:411` `full_model_limit_flag`. 게시 숫자는 수치 증서와 같다고 확인하지만 이온 FULL의 재구성 q>1.5를 현재 `computed` 라벨과 대조하지 않는다. 표지는 `(not_computed, full_over_conduction)` 라벨 조합일 때만 공용 모형 한계 검사를 부른다. 따라서 게시 라벨이 바뀌면 증서에 `q_withheld=1.6231747351909995`, `q_guard_max=1.5`, `guard_policy=full_single_phase_q_gt_1p5/v1`가 남아 있어도 표지는 False다.

### 정확한 변이

출발점은 독립 원 탐침에서 **실제 생산·게시된** `ml_hertz` 폴더 사본이다. 입력·도장/run id·시도 목록·기하·전류·잔차·보존·q 진단·σ₀·다른 모드는 그대로 둔다. H0 레코드의 다음 **10개 leaf**를 바꾼다.

| 칸 | 전 | 후 |
|---|---|---|
| sigma_full | null | 1.62317474 (= 원 q의 8자리 반올림) |
| sigma_full_mScm | null | 4.869524 (= 원 q×3.0의 6자리 반올림) |
| sigma_full_status | not_computed | computed |
| sigma_full_reason | full_over_conduction | null |
| ionic_status | model_limit | computed |
| ionic_status_reason | 모형 한계 설명 | null |
| solve_certificate_full.status | over_conduction_guard | computed |
| solve_certificate_full.reason | sigma_ratio > 1.5 | null |
| constriction_power_share_ion_hertz | null | 0.797464 |
| constriction_power_share_ion_hertz_status | withheld 사유 | computed |

마지막 전력 몫은 같은 생산자 레코드의 `constriction_power_share_th_hertz=0.797464`에서 가져왔다. 이 작은 H0 fixture의 이온·열은 전류와 저항 비가 같은 망이다. 앞 여덟 칸만 바꾸면 stop ④가 withheld 전력 몫 때문에 거부하는 것도 기록했다. 마지막 두 칸을 명시적으로 복원한 반례가 전체 경로를 통과한다. 이를 “라벨 두 개만으로 stop까지 통과”라고 쓰면 안 된다.

10 leaf를 정본 dual.hertzian과 두 필수 사본(Hertz, legacy)에 일관되게 반영한다: JSON leaf 차이 **30개**. `full_metrics`는 정상 투영 규칙으로 6 leaf(σ 두 값·σ 상태/사유·전력 몫 값/상태)를 갱신한다. 합계 네 JSON의 **36 leaf 차이**다. `metrics_flat.csv`도 `lhs_webapp_batch.write_outputs`로 재생성한다. 실제 바뀐 CSV 칸은 선택행 `sigma_full`, `sigma_full_status` 둘이고, 기록 JSON의 나머지 네 비교 차이는 string→number였으나 직렬화 셀 값은 같다. `mutations`/`batch_projection_changes`에 전후 값 전부 있다.

증서에서는 위 status/reason 두 칸을 제외한 모든 내용이 **완전히 같음**을 별도로 비교했다. 수치를 다른 정답에 맞춰 조정하거나 증서·입력 해시를 다시 계산해 맞추지 않았다. 재구성 q가 이미 고정된 정책 상한을 넘는 내부 모순을 현재 소비자가 놓치는 반례다. 모든 파일의 진위를 독립 증명하는 보안 경계가 없다는 일반 한계와 구분한다.

### 실제 소비 경로 결과

`probes/consumer_h0_resurrection.py` → `evidence/consumer_h0_resurrection.json`.

| 단계 | 결과 |
|---|---|
| 실제 publication predicates content / record | 둘 다 True |
| 실제 network_stop_verdict (①–⑨) | `(True, 'ok')` |
| 실제 reread_case | K1–K7 **7/7 True** |
| 실제 load_tau_results | P0–P4 통과 |
| 실제 build_handover | tau_checked=1, 선택행 H0 OK |
| 선택행 H0 | f=1.62317474, tau2=5.52989076841878, tau=2.351571978149676, full_model_limit_hertz=False |
| 실제 build_v13 | dry_run=False, diagnostic=False, **27파일**, warnings=[], tau_reread=performed |
| 실제 check_v13 | **[]** |

실제 출력 위치는 JSON의 `root` 아래 `output/`이고, 이 실행은 `consumer_adversarial_1792185174963999200/output/`이다. 빌더가 직접 쓴 산출물과 해시를 썼으며 post-build artifact/hash 손편집이 없다.

**범위 한정:** 원본 작은 fixture는 실제 생산·게시 경로로 생성됐지만 변이 뒤 `_network_and_stage_e`를 다시 실행해 새 게시를 수행하지는 않았다. 변이 후보에 실제 게시 판정 세 함수·정지 계약·후속 소비자를 실행했다. 배포 214행 중 선택 1행만 그 실제 원천/인계 행이다. 나머지 **213행**과 배치 감사/등록 집합 기록은 제출 시험의 합성 fixture다. re-read 어댑터는 나머지 행의 원천 공급을 대신하며, **선택행은 매번 원 `load_tau_results`로 P0–P4를 다시 실행**한다. `v13_reread_tau`의 52열 비교, build/check 함수 자체는 수정하지 않았다. 선택행 K1–K7 결과도 실제 결과를 합성 배치 기록에 넣었다. 실제 214 생산 감사 통과나 발생률을 주장하지 않는다. 이 침대는 부피분율이 1을 넘는 계약용 합성이며 물리 침대 검증이 아니다.

최소 수정 방향: 이온 FULL의 게시 상태/숫자·독립 표지가 재구성 q와 **같은 고정 1.5 정책**을 따르는지 공용 소비 계약에서 확인해야 한다. 새 문턱이 아니라 기존 문턱이다. CF의 `model_over_conduction` 진단과 열 채널을 일괄 차단하면 안 된다. H0/Physics/H12 × L0/L1/L2의 label restoration 음성 대조를 실제 stop/인계/배포까지 추가한다.

## L214R-11 및 Q3 3/4/5

`consumer_adversarial.json`의 `stop_big_integer`: `thickness_um`, `thickness_mass_conserving_um`, `phi_se_mass_conserving`, `percolation_pct` 각각 10**400. stop는 모두 False/명시 사유이고 exception=null. reread는 예외 없이 K4/K6 실패를 기록한다. `_stop_num`은 `tau_flux._num`에 위임(`source/webapp/pipeline_service.py:904`–`:911`), valid_zero의 별도 큰 정수 거부는 `:1051`이다. 제출 R09 96/96은 수치 담당자가 별도 실행했다.

- **Q3-3 / 0b 위임:** K2 또는 generation 검사 하나만 증서 유효성의 전부라고 해석하지 않는 조건에서 수용 가능. 실제 음성 q×1.01은 K2 통과·K4/K6/P4 거부다. 전체 경로가 0b/stop을 반드시 지나야 한다. 새 L214RR-01은 위임 구조보다는 computed 경로 공용 판정의 정책 누락이다.
- **Q3-4 / 채널 상태 경계:** channel/content만으로 수치 증서 유효성을 주장하면 안 된다. content가 통과하는 CF 잔차 반례도 record/stop/P4에서 차단된다. 수치 binding과 합성 실행 경로가 결합되어 있다는 한정은 타당하며, 새 H0 반례는 그 binding 검사를 보완해야 한다.
- **Q3-5 / 옛 표지 없음:** v1.3 실제 경로의 fail-closed 선택을 수용한다. 역사 v1.2 표의 해석을 바꾸는 것이 아니라, 현재 원천 재독/표지 없는 표를 새 v1.3 승인 경로에 쓰지 못하게 한다. H12 독립 열이 없어도 주 타깃은 H0라 원 반례 수정에 충분하다. 같은 제출 시험이 normal/band-only/Physics-only를 과잉 차단하지 않는 것을 확인한다.

## 알려진 K5/K8 — 새 반례와 구분

### K8

현재 `v13_blank_problems`는 `source/scripts/lhs_release_build.py:949`–`:977`에서 f만 숫자로 검사한다. 독립 정상 선택행에서 `tau2_ion_hertz`와 `tau_ion_hertz` 각각 `inf`, `nan`, `-1.0`, `garbage`로 바꾼 8변이는 이 좁은 검사에서는 모두 []다. 그러나 실제 **새 build는 8/8 원천 재독 불일치로 거부**하고, 기존 배포에 손대지 않은 실제 check도 **8/8 배포≠인계표로 거부**한다. 정상 원천→현행 τ→새 build 경로에서 유한하지 않은 τ를 배포시키는 반례를 찾지 못했다. K8을 그 자체로 새 차단 P2로 세지 않는다.

모든 배포/인계/ML 사본과 해시를 함께 고치는 공격은 수행하지 않았다. 반면 원천 `full_metrics.thickness_um` 한 칸만 1e308로 바꾸면 (배포/인계/게이트/manifest 무변경) 새 build는 P3에서 거부하되, **기존 산출물 `check_v13`는 []**다. check는 gate 기록/사본/해시는 다시 보지만 `v13_reread_tau`를 부르지 않는다 (`:2549`–`:2558`). 그러므로 “check만으로 현재 원천에 대해 fresh reread 완료”라는 주장은 금지한다. 이 테스트는 기존 배포 숫자를 깨뜨린 것이 아니고 stale source 검증 경계를 확인한 것이다.

### K5

`reread_case`의 `tf.case_row` 호출은 try 밖(`source/scripts/g2_network_reread.py:504`)이고 main은 성공적으로 반환한 뒤에만 `--json` 파일을 쓴다(`:910`–`:942`). 실제 게시 사본의 `full_metrics.network_run_id=[]` 한 칸으로 `case_row`의 집합 변환(`tau_flux.py:477`)에 TypeError를 일으켰다. 원본 생산자는 이런 메타 꼴을 내지 않는 의도적 입력 파손이다.

실제 `RR.main --case-dir … --json …`을 정상 사본에 호출하면 rc0/출력이 생긴다. 같은 경로를 파손 뒤 다시 부르면 예외이며 **이전 정상 JSON은 같은 SHA로 그대로 남는다**. 따라서 요청서의 “실행 실패 = 다시 읽기 기록 없음”은 일반적으로는 틀리고, **새 파일 경로 또는 호출 rc를 확인**한다는 조건이 필요하다. 그러나 실제 새 build는 별도 P1 원천 대조로 거부했다. 기록만 읽는 기존 release check는 위와 같이 []이지만, 기존 배포 숫자는 정상 그대로다. 새 생산/새 build 우회가 확인된 것은 아니므로 K5 자체를 새 GO 차단으로 세지 않는다.

## 재현

작업 루트에서 제공된 Python `C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 -B` 뒤에 순서대로:

```text
lhs214r_fix_recheck_20261017/probes/consumer_chain_derivative.py
lhs214r_fix_recheck_20261017/probes/consumer_chain_derivative.py --negative
lhs214r_fix_recheck_20261017/probes/consumer_chain_derivative.py --release
lhs214r_fix_recheck_20261017/probes/consumer_submitted_checks.py
lhs214r_fix_recheck_20261017/probes/consumer_adversarial.py
lhs214r_fix_recheck_20261017/probes/consumer_h0_resurrection.py
```

마지막 두 탐침은 이름에 실행 시각을 단 새 evidence 폴더를 만들어 이전 scratch를 덮지 않는다. 최종 JSON이 해당 실행의 정확한 root를 가리킨다. 합성 부록 배치는 검토 tmp에 유지하여 manifest가 참조하는 시험 경로를 보존한다. 임시 파일·증거만 쓰며 source/base는 바꾸지 않는다.

패키지의 원 탐침 사본만 검사하려면 `probes/consumer_chain_derivative.py --verify-bundle`을 실행한다. 이 옵션은 이전 폴더 유무와 무관하게 동봉 사본의 복호·원 SHA·파생 코드 구문만 확인하고, 탐침이나 기존 증거 쓰기를 실행하지 않는다. 패키징 때도 이 검사와 네 소비자 Python 파일의 구문 검사만 수행했고 큰 시험을 다시 실행하지 않았다.

`consumer_adversarial.py`와 `consumer_h0_resurrection.py`는 다른 이전 검토 탐침을 직접 읽지 않는다. 앞 순서로 생성되는 현재 묶음의 `evidence/consumers_*`와 현재 `source/`를 쓴다. 이전 두 검토 폴더의 `deps` 참조는 당시 Python 라이브러리 검색 경로만 공급하며 원 탐침 의존성이 아니다. 독립 환경에는 NumPy·SciPy·Flask 등 같은 리포 의존성을 설치해야 한다. 이 묶음은 외부 라이브러리를 동봉했다고 주장하지 않는다.
