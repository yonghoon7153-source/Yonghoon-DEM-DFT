# KG50 재개 도구 재검토 — f118c1fd1e3e (2026-10-28)

**판정: 자동 본 제출은 HOLD. 새 P1 4건, P2 1건, 문서 P3 1건.**

G0의 정상 완료 조건, write_restart 뒤 run 대조, 제한된 +1 step 보정, 작업 사본의 전체 주석 줄 제거는 실제 개선이다. 그러나 **본문 run과 다른 시험을 만드는 경로**, **압축 루프의 남은 시간을 틀리게 수용하는 경로**, **현재 호출이 거부한 케이스를 옛 시험으로 승격하는 경로**가 남았다. 정상 시험 개수를 늘리기보다 이 반례를 제출 경로에 연결해야 한다.

## 0. 검토 핀과 증거 수준

- 핀: `f118c1fd1e3eb1a558299663dcee6a0bf83b9942`, `claude/stoic-knuth-NObVQ`.
- 입력: `codex-kg50-resume-recheck-f118c1fd1e3e.zip`, 975,729 bytes.
- 직접 계산 ZIP SHA-256: `0c073ccfdf208671b8348b07f823833130f93d1f1a22cbf3d964b6698f2e98ab`.
- `PIN.txt`의 리포 파일 **42/42** SHA-256 일치. 중복·경로 이탈 ZIP 항목 없음.
- 원격 고정 핀과 별도로 대조한 5개 Git blob도 일치: 도구, 시험, 요청서, 실제 기록 README, 22:30 보고. `remote_identity.json` 참조. 42개 전부를 원격과 대조했다고 주장하지 않는다.
- 도구 SHA-256: `e59c43e688b2b9a6c23a337ceee2b28214ed3f6c76bd69b7f2402f926336dae8`.
- 실제로 실행한 것: 도구의 **내장 Python 본문을 바이트 그대로 추출한 CLI**, 정상·음성 대조 및 변이, 덱 일정 산술, 상태 식별 반례. `independent/deck/results.json`에 각 rc/stdout과 원문 SHA를 남겼다.
- **미실행:** 원문 Bash/AWK 전체, 저자 fake-SLURM 87개, 실제 `dem_restart.py`, DEM/MPI/WSL/SLURM/ibb. Git Bash가 명령 실행 전에 Windows `NtCreateDirectoryObject ... 0xC0000022`로 종료됐다. 이를 제품 시험 실패로 세지 않으며 **87/87 독립 재현**이라고 쓰지 않는다. Linux에서 실행할 가짜 scheduler 탐침은 동봉했다.
- trial 생성 결과 일부는 `:693`의 단순 ASCII 원문 줄 변환을 좁게 옮긴 것이다. 그 변환 결과를 받는 **생산 Python 검사는 실제 실행**했지만, 변환 자체를 원문 awk 실행으로 표기하지 않는다.
- 생산 코드·덱·Git 상태 변경 없음. 리뷰 파일과 합성 fixture만 별도 폴더에 작성했다.

이하 파일:행은 동봉 `repo/`의 고정 바이트 기준이다. 기존 KG50 항목과 이번 새 반례 ID `KG50R-*`를 구분한다.

## 1. 기존 항목별 닫힘

| 항목 | 판정 | 범위와 이유 |
|---|---|---|
| KG50-02 | **부분** | `COMPLETED / 0:0 / 기대 끝 / 이후 Loop / ERROR 0` 결합과 비교 행 결손 거부는 지지. 하지만 현재 호출에서 거부한 케이스도 옛 완료 시험으로 본 제출 가능(KG50R-04). G0의 존재를 전체 승격 계약의 닫힘으로 확대할 수 없음. |
| KG50-10 | **부분** | timestep·compute 결손·일부 활성 fix·뒤 run 변경은 거부. 물리 명령·변수·label의 전체 프로그램 대응은 불완전(KG50R-02/03). |
| KG50-14 — 도구 | **부분** | 케이스 이름의 정규식 경계와 첫 큐 조회 실패 처리 자체는 개선. 그러나 첫 루프의 skip이 본 제출 금지가 아님(KG50R-04). `_s1` 덱 이름 등 범위 밖은 이번에 닫지 않음. |
| KG50-16 — 도구 | **닫힘, 좁은 범위** | 작업 사본의 전체 주석 줄만 제거하고 비주석 바이트를 보존하는 변경은 수용. 실제 CLI에서 CRLF·인라인 주석·따옴표 안 `#` 보존, 연속 명령을 바꾸는 주석 제거 거부를 재현. 모든 LIGGGHTS 문법의 의미 동등성이나 외부 helper의 실물 호환성 인증은 아님. |
| KG50-17 — 도구 | **닫힘, +1 산술 보정 한정** | 179999→180000 보정, 2 step 부족 거부, timestep 불일치 동반 시 거부를 직접 재현. 단 ‘다른 결함이 전혀 없다’는 전제는 정적 검사 사각지대 때문에 성립하지 않음. suffix velocity를 넣은 +1 후보도 고쳐 주므로 KG50-10을 대신 닫지 못함. |
| KG50-18 | **부분** | 정상 after_settling의 `run 1 + run 2000 = 2001` 기대값은 올바름. 그러나 잘못 길어진 시험도 합산해 정상 기대값으로 인정(KG50R-05); 첫 원본 run 옵션 검사도 우회(KG50R-02). |
| KG50-19 | **열림** | write_restart 뒤 안정화 run 변경은 잡는다. 하지만 제공된 실제 압축 덱 쌍에서 ‘같은 run 5000’이 남은 2 step을 대신해 통과(KG50R-01). 지원 대상인 첫 루프 run의 위상 문제이며, 이미 알려진 ‘둘째 긴 run 도중 checkpoint’와 다름. |

‘닫힘’ 둘은 해당 로컬 변환의 범위다. 자동 본 제출 GO나 설치된 helper/바이너리 인증을 뜻하지 않는다.

## 2. KG50R-01 — P1: 압축 루프 문구 일치가 판정 시점 4,998 step 지연을 통과시킴

**위치:** `scripts/resume_ckpt.sh:366–385`, `:206–216`. 실제 입력은 `docs/data/pure_se_r075_20260927/input_pse_r075_a.liggghts:71,85,90,123,132–136`, 재개 덱 `input_pse_r075_a_r30.liggghts:28,89–94`.

이것은 새로 꾸민 물리 덱이 아니다. 요청서 §6이 정상 PASS 예로 제시한 원본/재개 덱 쌍을 그대로 사용했다. 메시 파일의 존재 조건을 충족할 빈 placeholder만 둔 정적 시험이며, 메시 기하 검증은 아니다.

| 양 | 원문에서 재계산 |
|---|---:|
| 압축 루프 진입 step | 1 + 200000 + 1 + 200000 = **400002** |
| 압력 판정 step | **400002 + 5000 n** |
| 제공 checkpoint | **1500000** |
| 현재 루프 run에서 이미 지난 길이 | (1500000 − 400002) mod 5000 = **4998 step** |
| 다음 원래 압력 판정까지 | **2 step**, 즉 **1500002** |
| 재개 덱의 첫 판정 | 1500000 + 5000 = **1505000** |
| 판정 시점 지연 | **4998 step = 4.998 ms**, dt=1 µs |

생산 내장 CLI 결과는 `rc=0`, `루프 몸 run 같음 ... [label loop_press] [run 5000]`, `문제 0`이다. 즉 이 검사는 전체 루프 몸 길이를 맞출 뿐 **checkpoint가 그 몸의 어디에서 저장됐는지** 보지 않는다.

원래 next check에서 목표 압력에 도달하는 궤적이면 판의 이동 정지 시점도 늦어진다. **이번 검토는 실제 압력·두께 오차를 계산하지 않았다.** 4.998 ms는 덱 일정의 확정 차이이며 실제 물리 오차의 크기는 미측정이다. 입자 수나 짧은 KE 일치로 이 차이를 복구할 수 없다.

**최소 해결:** checkpoint의 원래 run/반복 위치와 다음 관측 시점을 복원한다. 이 예에서는 **첫 잔여 2 step → 압력 판정 → 필요한 경우 이후 5000-step 반복**을 구분해야 한다. 반복 몸의 5000을 단순히 2로 바꾸면 모든 후속 반복이 2가 되므로 오답이다. 위상을 결정할 수 없으면 해당 압축 재개를 거부한다.

**해결 증거:** 원래 루프 경계 직전·경계·직후 checkpoint에서 다음 압력 판정 step과 이후 주기를 대조. 이번 실제 쌍의 5000 전체 재실행은 거부되고, 올바른 첫 부분 반복은 수용돼야 한다. 문자열 동등성 대신 관측 일정의 동등성을 시험할 것.

재현: `python3 -B independent/deck/reproduce_deck.py` → `results.json`의 `supplied_compress_loop_case`. `run 2`만 바꾼 후보가 현재 검사에서 거부되는 기록도 포함하되, 그것을 완성된 수정안으로 제시하지 않는다.

## 3. KG50R-02 — P1: 원본 첫 run의 every 동작을 시험에서 지운 뒤 ‘지원 문법’으로 검사

**위치:** `scripts/resume_ckpt.sh:148–160`, `:334–365`, `:396–397`, `:693`, `:703`.

settling의 정상 `run 180000`을 다음 한 줄로 바꿨다.

```text
run 180000 every 1000 "velocity all set 1.0 0.0 0.0"
```

내장 정적 CLI는 **rc 0**, `남은 step 같음: 끝 200001`을 반환했다. 첫 run은 E의 뒤 순서 대조에서 제외되고, known 분기는 숫자와 `upto` 여부만으로 끝을 계산한다. 원문 줄 trial cutter는 옵션을 버리고 **`run 2000`**만 만든다. 따라서 정상 덱과 변이 덱의 trial prefix SHA가 같고, 이후 `trial_steps()`도 **rc 0 / 2000**이다.

`run_n()`에 every 거부 코드가 있다는 반박은 성립하지 않는다. 호출될 때는 이미 every가 지워진 시험이다. 본 덱은 매 1000 step 속도를 재설정하고 시험은 하지 않는다는 차이이다. [고정 LIGGGHTS run 설명서](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/doc/run.txt)는 every의 구간별 명령 실행을 명시한다.

**한정:** settling known 분기의 반례이다. after_settling/압축에는 별도의 `plain()/sched_cmp()`가 있으므로 전 모드에 일반화하지 않는다. 현재 정상 v2/v3 덱에 이 옵션이 들어 있다는 주장도 아니다. 외부 생성기의 잘못된 산출을 못 막는 관문 반례다.

**최소 해결:** trial을 줄이기 **전에** 원 재개 덱의 첫 논리 run 전체를 공통 파서로 검증. 미지원 옵션은 제출 전 거부. 허용 옵션은 본 덱과 시험 사이에서 의미를 보존하도록 명시한다. 원본→trial 생성→관문 사슬을 시험해야 하며, `trial_steps()`에 every를 직접 주는 단위시험만으로는 부족하다.

재현: 같은 명령, `static_cases.first_run_every`. 별도 독립 최소 fixture와 실행 결과는 `independent/scope/peer_every_result.json`.

## 4. KG50R-03 — P1: 선택 목록 대조가 물리 명령·변수·label의 프로그램 차이를 놓침

**위치:** `scripts/resume_ckpt.sh:40–44`, `:230–244`, `:280–302`, `:351–365`, `:395–402`.

| 원 재개 덱에 가한 변화 | 실제 정적 CLI | 짧은 시험 |
|---|---|---|
| 첫 긴 run 바로 뒤 `velocity all set 1.0 0.0 0.0` | **rc 0** | 원 정상 시험과 바이트 같음 |
| 같은 자리에 `set group all density 1.0` | **rc 0** | 같음 |
| 같은 자리에 `delete_atoms group all` | **rc 0** | 같음 |
| 같은 자리에 `include extra.in` | **rc 0** | 같음 |
| 나중에 사용하는 `target_press` 변수 정의 삭제 | **rc 0** | prefix는 달라도 숫자 run 검사 통과 |
| 첫 긴 run 앞에 기존 목적지와 같은 `label loop_press` 추가 | **rc 0** | `trial_steps()`도 통과 |
| 대조: timestep 변경 / c_zmax compute 정의 삭제 | **rc 1 / rc 1** | 정상 음성 대조 |

`FWD`, `state`, `SEQ`가 각각 일부 명령만 읽으므로 ‘원 덱 어딘가에 같은 줄이 있음’을 C/E가 완전히 보완하지 못한다. c_/f_ 정의 검사에는 변수 사용·정의의 완전성이 없다.

**Q9의 label 허용도 조건이 필요하다.** 현재 trial에 jump가 없다는 사실만으로 충분하지 않다. 본 덱 뒤의 `jump SELF loop_press`는 파일을 처음부터 다시 읽고 먼저 만나는 같은 이름 label로 간다. 추가된 앞 label로 인해 settling부터 다시 실행할 수 있다. [고정 LIGGGHTS jump 설명서](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/doc/jump.txt).

**최소 해결:** 지원하는 재개 변환의 허용 차이만 열고 나머지 실행 명령의 보존을 검사한다. prefix의 재정의 가능한 상태·변수와 suffix의 모든 실행 명령, 변수 참조, label 유일성·jump 목적지를 포함한다. 일반 LIGGGHTS 전체를 해석할 수 없다면 **지원하지 않는 구문은 자동 제출 전에 거부**한다. 몇 개 금지 명령만 계속 추가하는 방식은 같은 부류를 닫지 못한다.

재현: `reproduce_deck.py`의 `suffix_*`, `missing_target_variable`, `duplicate_loop_label`. 전체 Bash 실행이나 실제 삭제/밀도 변경 시뮬레이션은 수행하지 않았다.

## 5. KG50R-04 — P1: 현재 큐 차단 뒤에도 옛 성공 trial로 본 제출 가능

**위치:** `scripts/resume_ckpt.sh:661–662`, `:709–719`, `:725`, `:777–780`. 시험 사각지대: `test_resume_ckpt.py:354–364`는 시나리오마다 새 폴더를 만든다.

**조건부 소스 경로 반례:** 동일 case/SFX의 이전 성공 `job_r56t.txt`, mode, 원 로그, trial 로그, runner가 작업 폴더 W에 남아 있고 `-T`가 없는 재호출이다.

1. 현재 `squeue -u`가 같은 case의 진행 중 main을 돌려주거나 조회에 실패한다.
2. 첫 루프는 ‘건너뜀’ 후 continue한다. 여기까지는 의도대로다.
3. 둘째 루프는 **현재 성공한 case 목록이 아니라 원래 CASES 전체**를 돈다. `job_r56t.txt`가 있으면 옛 trial 7001을 다시 읽는다.
4. 옛 trial의 sacct는 여전히 COMPLETED/0:0이다. 둘째 squeue는 **옛 trial ID**만 조회하므로 현재 main의 존재를 막지 않는다.
5. 일관된 옛 로그의 G0–G3가 통과하면 현재 호출이 시험을 제출하지 않았는데도 `:779`의 본 sbatch에 도달한다.

저자 정상 fixture로 게이트 입력을 고정하면 G0 끝=22001, G1 N=312506·KE=0.1000 일치, G2 settling 대체, G3 필요한 21000·22000 존재 및 첫 KE 차 **0.526315789% < 5%**다. 이 조건에서 옛 파일을 배제하는 가드는 없다.

**증거 한계:** 이 건은 정확한 소스 분기와 입력의 경로 증명이다. 실제 Bash fake-SLURM 실행은 환경에서 시작하지 못했다. 실제 중복 제출이 관측됐다고 쓰지 않는다. `stale_trial_results.json`의 NOT_EXECUTED를 PASS로 바꾸지 않았다.

**최소 해결:** 현재 호출에서 정상 제출한 trial만 고유 attempt ID·case/job 목록에 넣고 둘째 루프는 그 목록만 소비. 이전 파일을 지워 증거를 없애지 말고 attempt별로 분리. 본 제출 직전 현재 case 충돌 및 이미 승격한 attempt 여부 재검사, 조회 실패 시 거부. 원본 덱·checkpoint·helper·trial/main runner와 증거를 같은 attempt에 묶는다.

**해결 증거:** 기존 성공 파일이 있는 상태에서 busy/조회 실패/정적 거부/시험 제출 실패를 각각 재현하여 새 main 호출 0회. 정상 신규 attempt만 trial 1회/main 1회. 새 빈 폴더만 쓰는 시험으로는 닫히지 않는다.

Linux 재현 준비본: `python3 independent/scheduler/probe_stale_trial.py`. 모두 가짜 scheduler이며 실제 sbatch를 호출하지 않는다. 이번 환경에서 실행 성공을 확인한 명령은 아니다.

## 6. KG50R-05 — P2: 계속 줄 run이 2,000-step 시험을 182,001 step으로 늘려도 기대값으로 수용

**위치:** `scripts/resume_ckpt.sh:693`, `:406–445`, `:703–711`, `:732`.

| 첫 긴 run 표기 | 정적 CLI | trial 논리 run | 합계 / 기대 끝 |
|---|---:|---|---:|
| `run 180000` | rc 0 | run 2000 | **2000 / 22001** |
| `run &` 다음 줄 `180000` | rc 0 | run 180000; run 1; run 2000 | **182001 / 202002** |

행 단위 cutter가 첫 논리 run을 놓친 반면 `trial_steps()`는 뒤늦게 논리 명령으로 합산한다. 관측된 Python 결과는 모두 rc 0이다. **1시간 안에 이 긴 시험이 끝나면 G0는 그 긴 끝을 정상으로 인정**한다. 따라서 ‘G0 TIMEOUT이 막는 닫힌 실패’는 보장되지 않는다. 실제 KG50 침대가 1시간 안에 끝난다는 예측은 아니다.

최소 해결: 같은 논리 명령 파서로 자르거나 이 형태를 제출 전에 거부. 허용된 setup run + 첫 긴 run의 최대 TS라는 **시험 예산·위치 계약**을 별도 검증한다. 잘못 생성한 시험의 합을 그대로 기대값으로 삼지 않는다.

재현: `python3 -B independent/scheduler/probe_trial_steps.py`. 원문 Python 실행과 awk 의미의 제한된 전사를 구분한 결과를 저장했다.

## 7. KG50R-06 — P3: 본 제출 유무의 시간·증거 지위가 문서마다 다름

요청서 `:29,111`은 실제 본 제출이 아직 없다고 쓰지만, 같은 핀의 `docs/data/kg50_resume_tests_20261027/README.md:15`는 **10-28 09:42 시험 328597 → 본 job 328599, NP4 RUNNING**이라는 저자 보고를 추가했다. 그 보고 원본은 미수령이고 구판 `65f73b37…`이다.

정정 문안: **“10-27 -T 보고 원본 수령. 10-28 구판 본 제출은 저자 화면 보고이며 원본 미수령. 최신 e59c43e6 판의 실제 실행 증거는 없음.”** 실행했다는 독립 확인도, 한 번도 제출하지 않았다는 단정도 피한다. 이것은 물리 실패의 증거가 아니다.

## 8. Q1–Q9 답

| Q | 답 |
|---|---|
| Q1 | **부분 닫힘.** 실패/미완료 trial 자체를 거부하는 G0와 결손 거부는 올바른 방향이다. 현재 시도와 그 trial을 연결하지 않으면 KG50R-04가 남는다. G0 최종 행도 숫자 첫 토큰만 보는 lastrun(:648)보다 헤더 폭·유한한 필수 필드가 있는 실제 thermo 행으로 확인하는 편이 맞다. 후자는 이번에 AWK 동적 재현하지 않은 보강 사항이다. |
| Q2 | **불충분.** write_restart 뒤 길이 변경 음성 대조는 잡지만, 제공 압축 쌍의 루프 위상과 명령/변수 사각지대는 놓친다. KG50R-01/03. 이미 알려진 미지원 경로 목록을 늘리는 것과 지원 경로의 실제 일정 검증은 다르다. |
| Q3 | **합산 수정은 맞고, 짧은 시험 보장은 미완성.** 정상 run1+run2000을 2001로 센 것은 지지. 원본 run 검증·논리 단위 절단·TS 상한 검사가 앞서야 한다. 계속 줄 run은 제출 전 거부 또는 올바르게 절단(KG50R-02/05). |
| Q4 | **제한된 임시 adapter 보정 수용.** 원 덱 끝200001−S0 20001=180000은 외부 도구 내부 원인과 무관하게 검산된다. 원인 추정과 산출 수정 근거를 구분하고 before/after SHA·보정값·재검사 기록을 남긴다. 장기적으로 helper를 고치는 편이 낫다. ‘문제 하나’는 현재 검사 범위 안이라는 뜻만 가진다. 중복 가드 때문에 mutant가 살아남는 것 자체는 실패가 아니나, 안전 속성을 실제 깨뜨린 입력을 놓치면 미해결이다. |
| Q5 | **좁은 주석 제거 규약 수용.** 비주석 원 바이트를 보존하는 검사와 파싱 대조가 실제로 작동했다. 인라인 외부 case 이름을 남겨 helper가 거부하는 것은 알려진 가용성 한계로 받아들일 수 있다. 이를 없애려고 코드 줄을 광범위하게 치환하면 안 된다. Unicode·모든 quoting 문법까지 같은 인터프리터라는 주장은 하지 않는다. |
| Q6 | **KE 대체는 상태 동일성 증명 아님.** 아래 §9의 독립 reader/가시 상태 대조를 추가하되, 원 런 및 숨은 이력까지 인증했다고 쓰지 않는다. G3는 21000·22000의 존재를 보고 수치는 최초21000만 비교한다. 두 시점 수치가 모두 같다는 전제로 강화하면 안 된다. |
| Q7 | **필요.** wrapper와 외부 helper의 실제 SHA를 기대값과 대조하고 불일치 시 중단. 여기에 checkpoint·덱·runner·NP·실제 바이너리·job/attempt 연결을 남긴다. 본문 고유 문구로 버전을 추정한 것은 설치판 SHA 증거가 아니다. SHA 표지만 추가해 KG50R-04가 해결되지는 않는다. |
| Q8 | **현 핀의 자동 본 제출 HOLD.** 도구 결함을 고친 뒤 실제 사용 환경의 해당 checkpoint·경로·NP로 -T와 원본 덱/로그/완료 증거를 먼저 확보. 구판 NP4 기록을 신판 NP56이나 after_settling으로 전용하지 않는다. D0.7 Q5 dt·감쇠 자격은 별도이며 이번 판정이 닫지 않는다. 이미 진행 중이라고 저자가 보고한 job의 중단/재실행을 이번 리뷰가 지시하지 않는다. |
| Q9 | **조건부 허용·보고 수정.** label은 전 프로그램의 유일성·목적지 보존이 확인될 때 허용. 현재 조건만으로는 KG50R-03. print/quit-only if 허용은 강제 종료가 G0에서 거부되고 실행 의미를 바꾸는 명령을 숨기지 못한다는 범위에서 합리적. 시험 전 거부도 최종 보고에 case·stage·reason·attempt를 기록해야 한다. 머리 두 줄짜리 보고를 정상 검사 완료로 읽을 수 있게 두지 않는다. |

## 9. 상태·실물 증거의 경계

22:30 제공 보고에는 N=22353, S0=20001에서 KE=2.3980032, 첫 정규 step21000에서 KE=2.5527533이 양쪽에 같다고 적혀 있다. **원본 trial 로그·sacct 출력·생성 덱·plan/fixrun/deckcheck 파일은 이 묶음에 없으므로 보고의 값을 원자료에서 다시 계산했다고 쓰지 않는다.**

합성 산술로 N=2, KE=1 J가 같은데 위치·type·radius·속도 방향이 다른 상태를 만들 수 있다(`independent/scope/state_observability.json`). 기존 `sel()`(:646)은 omega와 mass도 포함하지 않는다. 이는 이미 공개된 증거 한계이며 새 P1로 중복 등재하지 않았다.

제안한 별도 `read_restart → dump → run 0` reader와 trial S0 비교는 유용하다. 최소한 같은 관측 시점, ID 유일성/집합, step, type, radius, mass 또는 density, 좌표, 속도, omega를 고정 정밀도·정렬·허용치로 대조한다. 원본 파일 SHA는 별도 보존한다. 하지만 같은 checkpoint를 두 번 읽는 시험은 **재개 덱이 가시 상태를 바꾸지 않았는지**를 검사한다. checkpoint 생성 전 원 런 상태 및 숨은 접촉 이력 보존의 독립 증명은 아니다. 판/mesh·활성 fix·이력은 별도 자격이다.

공식 [read_restart 설명서](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/doc/read_restart.txt)도 MPI 분할 변경·일부 granular force의 초기 평가 때문에 재개 궤적이 정확히 같지 않을 수 있음을 설명한다. 따라서 행 순서/부동소수 차이와 실제 상태 결손을 구분한 계약이 필요하다. 해당 공식 소스와 실제 ibb 바이너리의 동일성은 이번에 확인하지 않았다.

## 10. 최소 해제 목록과 재현

1. **압축 루프 phase:** 다음 원래 압력 판정까지의 잔여와 이후 반복 주기를 복원. 결정 불가능한 checkpoint는 거부.
2. **원본 프로그램 검사:** first-run 옵션, 상태 변경 명령, 변수, label/jump를 trial 절단 전에 검증. 지원 차이만 명시적으로 허용.
3. **현재 attempt만 승격:** 옛 job/mode/log로 큐 거부나 정적 거부를 우회하지 못하게 하고, 두 번 호출하는 회귀시험 추가.
4. **짧은 시험 계약:** 논리 run 기준 절단 및 허용 setup+TS 상한. 계속 줄 반례와 every 반례를 실제 생성 사슬에 연결.
5. **실행 영수증:** wrapper/helper/덱/checkpoint/runner/binary/NP/job 신원을 묶고 시험 전 거부도 저장. 문서의 본 제출 상태를 시각·증거 수준별로 정정.
6. 수정 후 **원문 Bash fake-SLURM 시험과 실제 도구 사슬 -T**는 별도 증거로 확보. 본문 Python 탐침 통과만으로 이 둘을 대체하지 않는다. 물리·Q5 등록의 해제는 별도.

동봉 파일을 풀어 ZIP 루트에서:

```bash
# 모두 리뷰 fixture/원문 Python 검사; 실제 DEM·scheduler 실행 없음
python3 -B independent/deck/reproduce_deck.py
python3 -B independent/scheduler/probe_trial_steps.py
python3 -B independent/scope/probe_state_observability.py

# Bash가 동작하는 Linux에서만: 가짜 scheduler만 사용
python3 -B independent/scheduler/probe_stale_trial.py
# 저자 기존 시험 — 이번 Windows에서는 실행하지 못함
python3 -B repo/scripts/test_resume_ckpt.py
```

현재 결함이 남은 코드에서 반례 탐침의 rc=0/통과 출력은 **제품 수용이 아니라 false-green 재현**이다. 판정은 `results.json`의 각 변이 의미와 함께 읽는다. 재실행은 리뷰 fixture만 덮어쓰며 `repo/`는 읽기만 한다.

**HOLD**
