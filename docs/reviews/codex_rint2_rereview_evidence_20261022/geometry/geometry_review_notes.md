# Rint ② 재검토 — geometry / SV 독립 메모

검토 핀: `0b3012460fb8e8b7d53484b0efe399e2dc506aec`; 비교 기준 `5dc6f7f0b`. 코드 수정·생산 캠페인 없음. 이 폴더에만 탐침·출력·메모 생성. `source/scripts`는 pinned source이며 `repo/scripts`와 해당 blob 일치. Python 3.12.14 / NumPy 2.5.3 / 단일 스레드 Windows에서 실행했다. 작성자 Linux 시험 숫자를 재사용하지 않았다.

## 판정

| 항목 | 닫힘 상태 | 판정 근거 / 남는 범위 |
|---|---|---|
| RCA-03 | 최소 해결 닫힘; S0 규모는 열림 | 같은 셀 비연속 방문은 별도 위치·dof. 원래 폴리라인 손 사슬 `G=1.071428571…`, 옛 병합 `2.5`, 현재 사슬과 일치. 끊긴 같은 fid 조각, 고리, 자기 접촉 거리, 재방문 사이 덮임도 재실행 통과. |
| RCA-04 | 최소 해결 닫힘; 선언한 퇴화 표현 한계 유지 | base / reverse / 공선 세분 / fid 재명명의 포트 `(1,1,2)↔(2,1,3)`, `G=5.263157894736835`, `sigma=2.339181286549705`, 계 바이트 digest 모두 같다. 먼 끝 변경·비이진 원점 EPS·covered 포트 이동 금지도 통과. 두 끝이 모두 같은 경로·닫힌 고리의 점열 순서 한계는 일반적 모든 표현 불변으로 확대하지 않는다. |
| RCA-05 | 최소 해결 닫힘; 물리 검증 아님 | 기존 집중 반례는 분산판으로 교체. 5-node rail 독립 해 `1.366013071895…`, 왼쪽 집중 `5`, 중앙 집중 `.238095238095…` 재현; 실제 CX fixture의 `Lc=10`, `k=5`, 각 포트·G·부분 PTFE 절단·부분 c 축약 손 회로 일치. 전이 길이·균일 접점 저항 분포 가정 및 정수 k 경계 계단은 남는다. S0 분포 미실측을 닫지 않는다. |
| RCA-06 | 부분 | 옛 소산 dominance 반례는 닫힘. 실제 SVX에서 G_full `4.61491207863014`, G_cut `.4484304932735439`, ratio `10.291253935345182`, SV 전류 몫 약 .9151인데 옛 국소 소산 비교 false인 회로가 이제 반사실로 드러난다. PRE2 못 가른 덩어리도 차단된다. 다만 아래 새 RR-G01 때문에 '증서로 보장된 참 비의 문턱 판정'은 미완결. |
| PRE2-impl-01 | 원 반례 닫힘 | 단일 못 가른 덩어리 [1,∞]→SV_UNCHECKED; 실제 코드가 두 덩어리도 전부 제거함을 새 회로에서 확인. |
| PRE2-impl-02 | 원 수 불일치 최소 해결 닫힘; F3 부분 열림 | G 비 불일치·거짓 cert flags는 거부; cert 누락·수/증서 결합·규칙/수 범위는 F3대로 남음. |
| PRE2-impl-03 | 다른 검토자 담당 | 계획 overflow·중복키 검증은 registration 메모. |
| PRE2-impl-04 | 원 single-component 회귀 닫힘; F4 시험 틈 열림 | 현 QD2 13개는 첫 덩어리만 제거하는 변이도 모두 통과. 새 두 덩어리 probe는 그 변이를 잡는다. |

S1은 조건부 GO 유지: K=8·지름 규약·상 수준 면제·판 결합 예외·명목 체적이라는 명시 범위에서 기구 검토 가능. F16/F17/F18/F19 44 PASS. 실제 양의 α를 K8이 0으로 만드는 원 반례도 재현되며 K16 diagnostic은 정확한 union 면적·연결성 인증이 아니다. 이것은 명시된 이산화 한계다.

S2 v0는 geometry 구현 자체의 지난 HOLD 원인이 닫혀 **기구·S0/수치 탐침에 조건부 GO**. 등록 정량 판정 경로는 RR-G01을 먼저 고쳐야 한다. S3는 S2를 전제로 **시나리오 끝 기구에 조건부 GO** 유지: c=0 bit identity, SBE no-op, c 단조, c=1 정확 축약, P1 우선, 근접 경계·부적절 값 거부 통과. 젖음 상한·실물 SDCP 효과의 식별 또는 생산 GO가 아니다. 최종 캠페인 판정은 main의 provenance/registration 조건과 합쳐야 한다.

## RR-G01 [P2] 수렴 증서의 오차 구간을 SV 문턱 판정에 넘기지 않아 참 비가 문턱 위인데 표지가 없다

자리: `source/scripts/rint_r_chain.py:554` (특히 562, 583–586), `source/scripts/ca_ext_svcf.py:75` 및 `303`, 등록 R `:177`·`:179`·`:435`. 생산자는 `carbon_junction.py:2463`부터 실제 각 끝의 증서를 생성하지만 투영은 참/거짓 칸만 남기고 target_lo/hi를 버린다. 사슬은 nominal ratio를 비교한다. 등록에 "증서 여유 칸 없음"이 쓰였으므로 숨겨진 구현 불일치는 아니지만, "참 비의 괄호"를 판정 보장으로 쓰는 목적에는 결함이다.

새 탐침 `geometry_results.json.actual_certified_threshold_crossing`은 실제 SVX raster→registry→plan→solve→certify→sv_cf_record→sv_cf_problem→sv_assess를 호출한다. 작은 fixture의 첫 선형 해 벡터에만 `+1e-8`을 더하고 이후 풀이·재풀이를 정확 직접해로 실행했다. 원장/기록 숫자/증서 칸은 변조하지 않았다. 이것은 인증 허용오차 안의 해를 주입한 판정 반례이며, 자연 발생 CG 실패 빈도 주장이나 실침대 결과가 아니다.

| 수치 | 값 |
|---|---:|
| 독립 손 회로의 G_full | 4.61491207863014 |
| 독립 손 회로의 G_cut | 0.4484304932735439 |
| 참 비 | 10.291253935345182 |
| 게시 비 (= 아래 = 위; 못 가른 덩어리 0) | 10.291249475344962 |
| 선택 가능한 등록 문턱 | 10.291251705345072 |
| 실제 증서 구간의 비 `[main.target_lo/cut.target_hi, main.target_hi/cut.target_lo]` | [10.29125393534377, 10.291253935346631] |
| 주 해 target_err_bound_rel | 4.333779186480367e-7 (허용 1e-4 이내) |
| 주 해·반사실 ⓐⓑⓒⓓ / ok | 전부 true |
| `sv_cf_problem` | None (통과) |
| `sv_assess` | `[]` (SV 표지 없음) |

즉 **실제 증서 구간 전체가 문턱보다 크다**. 지금 코드는 같은 증서가 증명하는 결과와 반대 문장을 고른다. 좁은 경계의 문제라는 사실은 보장 위반을 없애지 않는다. 실험 전 문턱을 정한다 해도 어떤 출력이 경계 근처가 되는지 사전 보장되지 않는다.

최소 해결: 주 해와 각 반사실 끝의 양의 target_lo/hi 및 해당 G 결합을 보존·검증한다. 다리비 아래는 `Gfull_lo/Gcut_lower_hi`, 위는 `Gfull_hi/Gcut_upper_lo`; topological zero 분모는 +∞ 처리한다. 이 **확장된 보장 구간**으로 아래>t/위≤t/걸침 판정. 구간을 당장 운반하지 않으면, 각 computed 해가 실제 인증되었다는 조건을 먼저 강제하고 보수적 `nominal_lo*(1−τ)/(1+τ)`, `nominal_hi*(1+τ)/(1−τ)`로 확장해도 된다 (τ=1e-4). 정보가 없으면 SV_UNCHECKED. 위 실제 증서 interval을 쓰면 이 사례는 SV_DEPENDENT; τ 최악폭만 쓰면 SV_UNCHECKED로 안전하게 멈춘다. 경계 양쪽·정확 equality·무한대·한 끝 실패 회귀가 필요하다.

## 알려진 F3 / F4 / F6 / O1 독립 확인

### F3 [P3] 재검증은 내부 숫자 일관성까지만 확인하며 증서와 값의 결합은 보장하지 않는다

`ca_ext_svcf.py:196`는 n_unsplit에 비음수 정수만 요구하고 `:200`은 bracket_rule에 비어 있지 않은 문자열만 요구한다. `:259`는 cert가 None이면 검사 전체를 생략한다. `:75–77`은 target interval, I_bot, scale 등 결합 가능한 숫자를 투영에서 버린다. `run_contract.py:756`이 이 검증기를 실제 소비한다.

정상 finite-upper 두 덩어리 회로에서 각각 독립 변경한 결과:

| 입력 변경 | 검증 |
|---|---|
| 아래 ratio만 1→1.1 | 거부 |
| 위 ratio와 mirror만 →1.1, G_cut 그대로 | 거부 |
| cert ok=False | 거부 |
| upper.n_components_removed=0, n_unsplit=2 유지 | 통과 |
| computed 끝 cert=None | 통과 |
| bracket_rule='not-the-registered-rule' | 통과 |
| n_unsplit=10**400 | 통과 |
| 다른 실제 회로의 성공 증서 + 원래 정상 fixture G/ratio | 통과 (target 수가 투영에서 사라짐) |

또한 실제 인증된 SVX 결과의 끝 증서만 제거해도 `certificate_removed_from_certified_run`은 통과한다. `foreign_certificate_accepted`는 실제 SVX 반사실 증서(I_bot=.4484304932735439)를 다른 fixture의 두 끝(G_cut=58.7301587301587와11.111111111111072)에 붙여 확인했다. 정상 producer는 cert 켬 경로에서 올바르게 증서를 만든다. 그러므로 이 결과를 fresh-run의 이미 확인된 오계산으로 부르지 않는다. 재판정·이동·과거판 기록 경계의 계약 결함이다. 최소 해결: registered R 경로는 computed 끝마다 현재 인증 필수; 각 끝의 G↔I_bot/target와 main 분자 결합; 정확한 rule/version; 실제 component census·removed count/cell 수의 일관성을 검증. 10**400 자체는 여기서 overflow 예외를 내지 않았고, 의미상 범위 검사 부재다.

### F4 [P3] 다중 덩어리 제거 회귀 틈 — 현재 구현 오작동은 발견하지 않음

새 회로: h=1, shape=(11,3,9); 완전한 수직 섬유 x=1.5,3.5,7.5,9.5; y=1.5, z=.5..8.5. SDCP는 z=4.5에서 x=1.5,2.5,3.5와7.5,8.5,9.5의 두 분리 성분. 각 성분에 두 섬유가 지남. 같은 높이 전위가 같으므로 가로 SDCP 다리의 전류가0: 다리만 제거한 참 비는 정확히1. 각 rail 저항은 `.005+6*.01+2*.007+.005=.084`, 총 G=4/.084=47.61904761904761; 실제47.61904761904763.

현 코드 `carbon_junction.py:2491`·`:2556`는 두 성분6셀 모두를 제거하여 괄호[1,∞]와 SV_UNCHECKED를 낸다. `_sv_unsplit_cells`가 labels는 모두 반환하되 셀 목록을 첫 label로만 제한하는 변이를 메모리에서 적용하면, G_full 불변, 위 비=2, threshold2에서 표지 없음이다. **현 QD2 13/13은 이 변이에도 통과** (`first_component_mutation.log`). 즉 F4를 독립 확인했다. 이 새 두 덩어리 사례를 상주 회귀에 넣고 전부 제거 여부·판 결합도 확인하면 된다. 현재 코드 자체를 고칠 증거는 없다.

### F6 [P3] census mismatch는 안전하게 거부되지만 '사슬 SV_UNCHECKED'라는 끝-끝 서술과 다르다

위 두 성분 회로에서 census n_unsplit만0으로 바꿨다. 생산자는 `carbon_junction.py:2547`에서 원장 재계산과 차이를 발견하고 upper.status=`unsplit_census_mismatch`를 낸다. 그 후 `sv_cf_problem`은 **"못 가른 덩어리0인데 위 끝 기록 dict"**로 거부한다. 독립 `sv_assess` 호출만 하면 SV_UNCHECKED지만 실제 `run_contract.py:759`가 앞에서 게시 거부한다. 따라서 안전성 우회가 아니라 오류 처분/설명의 불일치다. `KNOWN_STATUSES`에 이름이 없다는 사실 자체는 허용·거부 원인이 아니다: 검증기는 비를 싣지 않는 알 수 없는 상태도 받도록 의도되어 있다.

최소 해결은 fail-closed를 유지하며 census_mismatch를 명시적 구조화 실패로 끝-끝 기록하거나, 재계산 count와 입력 census count를 별도 칸으로 보존해 유효한 unreadable record로 전파하는 것이다. test 설명도 실제 게시/재판정 경로를 검증하도록 바꿔야 한다.

### O1 / C3: 보수성은 유효하지만 정보량·물리 정의가 별도 문제

위 대칭 두 성분 회로는 **실제 다리 전류0, 참 비1인데 [1,∞]**다. 독립 bypass rail을 하나 더 두면 G_full58.730158730158706, 위 비5.285714285714302다. 즉 큰 위 끝이 참 SV 영향이 크다는 증거가 아니며, 현재 blocker가 false-clear를 방지하는 대신 답을 못 주는 경우가 있다. 합성 fixture 수를 실침대 빈도로 해석하지 않는다.

Rayleigh 보장은 동일 cell graph의 간선 삭제 family에서 성립한다. 새로운 섬유 dof·자기 길·접촉을 추가하여 역할을 분리한 그래프는 그 family 밖일 수 있다. 등록435의 '드물게 범위 밖'은 빈도 근거가 없어 '범위 밖일 수 있다'로 쓰는 것이 정확하다. 역할 분리 표현은 **현 그래프의 보수적 진단을 실행하기 위한 선결조건은 아니다**. 다만 실물에서 SDCP를 없앤 인과 효과의 한 값, 또는 SV가 중요하지 않다는 넓은 정량 주장을 하려면 필요하다. 지금 괄호가 자주 걸친다는 이유로 DBE 열람 뒤 threshold를 높이거나 모델/범위를 고르면 안 된다. 먼저 unreadable/straddle 처분을 봉인하고 S0 자료 뒤 범위를 보충 검토한다.

모서리 하나라도 dependent/unchecked이면 해당 표지를 붙이고 두 표지를 허용하는 규칙은 전 범위 청구에 적절히 보수적이다. R_j0만 검사할 선택은 그 한 값에서의 가드라는 제한을 동반한다. envelope를 만드는 R_j_lo/0/hi 전체의 SV 비의존을 주장하려면 all3가 필요하고, 그 역시 임의 내부R·새 origin까지 보증하지는 않는다.

## 재현 / 출력

`run_review.py`는 source를 import하고 메모리 변이를 복구하며 이 폴더에만 결과를 쓴다. `RINT_REVIEW_SOURCE`에 `scripts/`를 포함한 다른 pinned source 루트를 지정할 수 있다; 생략하면 `rint2_rereview_20261022/source`를 쓴다. 실제 선택 경로와 SHA256은 결과에 기록한다. 환경:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTHONIOENCODING='utf-8'
$env:OPENBLAS_NUM_THREADS='1'
$env:OMP_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:PYTHONPATH='C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_review_20260930/deps;C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/gen2_network_reverify3_20261007/deps'
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'rint2_rereview_20261022/geometry/run_review.py'
```

- `geometry_results.json`: fresh numeric results, source SHA256, runtime, certificate records, mutation outcomes.
- `targeted_tests.log`: selected geometry/SV/S3/combination author regression 122 PASS /0FAIL.
- `s1_tests.log`: F16/F17/F18/F19 44PASS /0FAIL.
- `first_component_mutation.log`: deliberately wrong first-component-only implementation still passes existing QD2 13/13; custom two-component fixture distinguishes it.

전체16파일·전체게이트를 실행했다는 주장은 하지 않는다. 실침대 S0·재압밀·threshold 선택·생산 정량 결과는 없다. 사전 알려진 finding은 각각 원 코드 호출·새 작은 fixture·검증기 입력으로 확인했고, 작성자 보고 숫자를 실행 증거로 세지 않았다.
