# Codex 검토 — 50kg 4차년도 SE 입도 비교 DEM 덱 (2026-10-26)

**판정: 현재 묶음 그대로의 속도 시험·다일 본 런은 HOLD. 새 P1 2건, P2 4건, P3 2건.**
생성 수치의 재현성과 실행 경로의 안전성은 다르다. 기존 selftest 81/81, 독립 생성·산술 검사 86/86, 재생성 38파일 바이트 동일을 확인했지만, 속도 시험이 입자를 넣을 수 없는 경로와 실패한 재개 시험을 본 런으로 승격하는 경로가 남았다.

## 0. 대상·증거 경계

- 사용자 지정 커밋: `3056eef12b60ed754fa59ec5a84fad811b14c9c8`.
- 사용자 제공 트리 해시: `481337fc0ec74967a179ded879e7f3aa074cb592`.
- 입력 ZIP: `codex_kg50_decks_20261026.zip`, 221,441 bytes.
- 직접 계산 SHA-256: `dd19d19c15d6e6898ab9ed3ec1f8327b3eeb61355b1c6ce2e61b675a14224a82` — 사용자 값과 일치.
- 사용자가 미푸시 상태를 확인했고 첨부 고정 바이트 검토를 승인했다. 따라서 아래 판정의 직접 대상은 `snapshot/repo/`이다. 커밋·트리 신원은 사용자 진술이며 원격 Git 객체와 독립 대조한 것으로 쓰지 않는다. 미푸시 자체는 finding이 아니다.
- LIGGGHTS 소스 대조: 공식 PUBLIC `3d5c00f20519e6bb6eb6756f51f1ad36564e649d`. 실제 ibb/hit 바이너리와 외부 `dem_restart.py`·`hit_resume.sh`는 제공되지 않았다.
- **LIGGGHTS·MPI·WSL·SLURM·원격 런을 실행하지 않았다. 생산 코드·덱·공유 Git 상태를 수정하지 않았다.** CPU 산술, 소스 판독, 생성기 selftest/재생성, 합성 로그의 조건식 검증만 수행했다.
- 파일:행은 첨부 `snapshot/repo/` 기준. 아래 재현 명령의 시작 위치는 이 보고서가 있는 폴더다. 실행 환경의 `python`을 사용한다.

## 1. finding 요약

| ID | 등급 | 무너지는 결론 | 최소 처방 |
|---|---|---|---|
| KG50-01 | P1 | 현재 NP28/56 속도 덱이 312,506입자 침대의 시간을 잰다 | NP1 삽입·상 재고 확인 후 동일 checkpoint에서 NP/skin 비교 |
| KG50-02 | P1 | G1–G3 PASS이면 짧은 재개 시험이 정상 완료됐다 | 완료 상태·exit code·기대 마지막 step·run 완료 확인을 본 제출 조건에 추가 |
| KG50-03 | P2 | 저장된 최종 공통 프레임이 100,000-step 이완 끝이다 | 끝 step의 atom/contact/mesh를 명시적으로 함께 저장 |
| KG50-04 | P2 | Rayleigh 1.5%만으로 D0.7의 dt가 충분히 검증됐다 | 큰 viscous 감쇠를 포함한 짧은 동일 물리시간 dt 비교와 수치 자격화 |
| KG50-05 | P2 | D3 평균 차 통과가 모든 SE 크기의 영역 독립성을 보증한다 | 공학적 선택과 동등성 주장을 분리하고 미식별·경계 처리 고정 |
| KG50-06 | P2 | 첫 20k settling 시간이 압축 throughput/skin 이득 하한이다 | 대표 압축 구간·실제 I/O를 포함한 별도 시간 측정; 현 값은 추정 유지 |
| KG50-07 | P3 | MPI의 floor 때문에 AM이 반드시 체계적으로 부족하다 | 잔여 무작위 배분·고정 시드 상관을 반영해 설명 정정 |
| KG50-08 | P3 | 출력된 AM 구간이 정확히 ±0.5%, 총수 하한이 정확히 99%다 | 정수 경계의 방향 수정 또는 실제 허용 정수 구간을 정본으로 표기 |

P1은 다일 런 전 필수 수정이다. P2 중 KG50-03은 결과를 잃지 않도록 런 전에 고치는 것이 맞고, KG50-04는 가장 작은 SE의 본 런 전 자격화 항목이다. KG50-05는 결과의 해석 범위, KG50-06은 자원·운영 결정을 제한한다.

## 2. KG50-01 — 속도 덱의 고코어 fresh 삽입은 기하적으로 불가능

**위치:** `scripts/make_se_size_decks.py:553–572`; `docs/data/kg50_decks_20261026/README.md:28–35`; 실제 네 speed 덱의 `processors * * 1`와 `fix ins_mix ... overlapcheck yes`.

생성기는 속도 시험을 NP1 checkpoint의 재개로 만들지 않는다. 각 NP에서 다시 `insert/pack`을 수행한다. AM 검사만 제거해도 이 문제는 없어지지 않는다.

공식 소스의 연결은 다음과 같다.

1. `FixInsertPack`의 `check_dist_from_subdomain_border_` 기본값은 true.
2. `all_in no`는 region 경계의 shrink를 끄는 것이며, 이 MPI subdomain 검사까지 끄지 않는다.
3. 후보 중심은 모든 subdomain 면에서 해당 입자 반경 이상 떨어져야 한다. `domain->dist_subbox_borders`에는 주기경계 예외가 없다.
4. 이 덱의 AM 반경은 3 µm다. NP28의 4×7 분해는 10×5.714286 µm, NP56의 7×8 분해는 5.714286×5 µm다. 좁은 방향의 최대 중심 여유는 각각 2.857143·2.5 µm로 **필요한 3 µm보다 작다**.
5. 자동 분해의 선택을 달리해도 해결되지 않는다. Px·Py=28 또는 56, Pz=1인 모든 정수 조합 중 양쪽 폭이 6 µm 이상인 조합은 없다.
6. 분포는 큰 입자부터 삽입한다. AM을 가진 rank는 첫 AM에서 공통 시도 예산을 소진하고 다음 SE로 진행하지 못한다.

[기본값·삽입 루프](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_insert_pack.cpp#L175), [subdomain 거리](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/domain_I.h#L126), [큰 템플릿 우선](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_particledistribution_discrete.cpp#L463).

평균 rank 배분이면 NP28에는 rank당 AM 약 33개 이상, NP56에는 약 16개 이상이 있어 총 삽입 0이 예상된다. 이것은 실행 실측이 아니라 소스와 기하로부터의 결론이다. 배분이 비균일할 가능성까지 허용해도 통과할 수 없다: AM 개수분율 0.0030335467에서 AM floor가 0일 수 있는 rank 목표는 최대 329개다. AM 없는 rank들만 성공한다고 극단적으로 잡아도 총수 상한은 NP28에서 9,212, NP56에서 18,424로 **검사 하한 309,380보다 훨씬 작다**.

**최소 해결:** 생산 경로처럼 NP1에서 실제 삽입하고 총수·AM·SE·ID 재고를 저장한다. 그 동일 checkpoint를 읽는 네 비교 덱으로 NP/skin을 바꾼다. 삽입 실패를 피하려고 overlap 검사나 subdomain border 검사를 무조건 끄는 처방은 권하지 않는다. 동일 침대·동일 비교 구간·성공한 실행의 시간을 비교한다. 직행 `run_kg50_d07_b40.sh`도 fresh NP56 경로이므로 재개 절차를 우회해 실행하면 같은 문제다.

**닫힘 증거:** 새 speed 덱에 재삽입이 없고 checkpoint 신원이 같음; 각 비교의 실제 재고·시작/끝 step·정상 완료·Loop time. 단순 selftest 초록이나 AM 검사 삭제로는 닫히지 않는다.

재현: `python -B evidence/kg50_design/probe_design.py`.
결과: `probe_design_results.json`의 `speed_fixture_impossibility`. 소스+산술 탐침이며 실제 삽입 실행은 아니다.

## 3. KG50-02 — FAILED 재개 시험이 본 제출 분기에 들어감

**위치:** `scripts/resume_ckpt.sh:67–74, 76–95, 107–109`; 생산 의존 `README.md:58`.

대기 루프는 FAILED/CANCELLED/TIMEOUT도 종료 상태로 받아들인다. 이후 본 제출 전에 COMPLETED·ExitCode 0:0·마지막 step을 요구하지 않는다.

삽입 전용 로그의 정상 thermo가 1,1000,2000,2001이라고 두자. 시험이 step1 setup만 출력한 뒤 MPI signal로 실패해 대문자 `ERROR`가 없으면:

- G1: step1의 Atoms·KE가 같아 PASS.
- G2: settling이고 step1 dump가 없어 G1의 KE로 대체 → PASS.
- G3: 공통 정규 thermo 줄이 없음 → “원 로그에 비교할 줄 없음”이라고 해석하여 PASS.
- 마지막 `if G1 && G2 && G3`는 본 런 `sbatch` 분기를 선택.

원 로그에는 정규 줄이 실제로 있다. 시험 로그가 끝까지 가지 못한 결손을 원 로그 부재로 바꾼 것이다. step1000까지 정상인 뒤 죽는 합성 사례도 통과한다.

| 합성 입력 | G1/G2/G3 | 본 제출 조건 |
|---|---|---|
| 정상 완료, 끝 2001 | PASS/PASS/PASS | 참 |
| FAILED, setup1만, 완료 footer 없음 | PASS/PASS/PASS | **참 — 반례** |
| FAILED, step1000 뒤 중단 | PASS/PASS/PASS | **참 — 반례** |
| 정상 완료이나 1000에서 KE 변조 | PASS/PASS/FAIL | 거부 |
| 대문자 ERROR 포함 | FAIL/PASS/PASS | 거부 |

**최소 해결:** trial의 정상 종료 상태·exit code·예상 끝 step(이번에는 2001)·run 완료 기록을 본 제출에 결합한다. 기대 비교 구간이 원 로그에 있으면 공통 줄 결손은 FAIL이다. 조회 실패·대기 시간 초과·로그 미완료도 본 제출 금지로 둔다. 실패를 한 번 더 돌려 본 런으로 넘어가는 것으로 처리하면 안 된다.

**추가 한계:** G2의 KE 대체는 입자 위치·type·반경·각속도 동일성 검사가 아니다. 같은 checkpoint 복원을 확인하려면 step1 atom 재고/상태와 hash 대조를 추가한다. 외부 `dem_restart.py`의 재선언·재삽입 금지·남은 settling step은 실제 생성 덱으로 별도 확인해야 한다. 원 경로의 settling 끝은 **200001**이다.

재현: `python -B evidence/kg50_restart/probe_source_semantics.py`.
이는 원문 조건을 assert한 **Python 의미 재현**이다. 원문 Bash/AWK 추출 harness도 만들었으나 환경에서 Bash가 시작 전에 차단돼 실행 증거로 세지 않았다. 실제 scheduler 제출은 0회다.

## 4. KG50-03 — 이완 종료 상태를 저장하지 않음

**위치:** `scripts/make_se_size_decks.py:321–330`; 대표 덱 `kg50_d07_b40/input_kg50_d07_b40.liggghts:208,227,233–234`.

압축 루프가 k번이면 종료 step은 다음과 같다.

- settling + 판 생성 + 안정화 끝: 400002.
- 압축 끝: 400002 + 5000k.
- 이완 끝: **500002 + 5000k**.

원자는 50,000, contact는 10,000, mesh는 5,000의 배수 step에서 저장된다. run 종료는 dump를 강제하지 않는다. 공식 [output.cpp:331–346](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/output.cpp#L331)에도 이 동작이 명시돼 있다.

예를 들어 k=1019:

| 항목 | step | 이완 진행량 |
|---|---:|---:|
| 압축 끝 | 5,495,002 | 0 |
| 이완 끝 | 5,595,002 | 100,000 |
| 마지막 atom 및 공통 프레임 | 5,550,000 | **54,998** |
| 마지막 contact | 5,590,000 | 94,998 |

마지막 공통 프레임은 끝보다 **45,002 step** 전이다. 옛 atom 간격 5,000이면 마지막 atom은 끝−2, 마지막 공통 atom/contact는 이 예에서 끝−5,002였다. 덤프를 줄인 것이 시간 표본의 의미도 바꾸었다.

실제 이완 결과가 얼마나 달라지는지는 미측정이다. 여기서 입증한 것은 **동일한 100k 이완 종료 상태가 출력되지 않는다**는 것이다. 첨부에 후처리기가 없으므로 특정 소비자가 잘못된 프레임을 이미 읽었다고 주장하지 않는다.

**최소 해결:** 정규 dump 간격은 유지하되 실제 최종 step의 atom/contact/mesh를 동기 저장하고 step·재고를 검증한다. 최종 restart 보존도 권한다. 출력 격자에 맞추려고 이완 길이를 조용히 늘리는 것은 별도 개입이므로 피한다. 실제 바이너리에서 지원하는 출력 명령으로 마지막 상태가 만들어지는지 짧은 테스트를 붙인다.

재현: `python -B evidence/root/probe_numerics_and_endpoint.py` 및 `python -B evidence/kg50_decks/probe_terminal_cadence.py`.

## 5. KG50-04 — D0.7의 viscous 시간척도는 Rayleigh보다 훨씬 짧음

**위치:** 대표 덱 dt 선언과 `:199`의 `fix damp all viscous 0.5`; 요청서의 Rayleigh 기반 dt 설명.

Rayleigh 비율 계산 자체를 반박하는 것이 아니다. 안정화·압축에서 고정된 큰 viscous 계수를 함께 고려해야 한다.

공식 [fix_viscous.cpp:138–157](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_viscous.cpp#L138)은 `F -= gamma*v`, [nve/sphere](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_nve_sphere.cpp#L167)는 두 반-step 속도 갱신을 사용한다. 이 코드 순서의 순수 drag 모드에서 인접 half-step 속도 배율은 **q = 1 − gamma·dt/m**이다.

실제 덱 SI 길이 r=0.00035 m, density=1640 kg/m³에서 D0.7 SE 한 입자의 질량은 2.9453478325e−7 kg이다. gamma=0.5, dt=1e−6 s를 대입하면:

| SE D (실제 µm) | m/gamma (µs, 덱 시간) | gamma·dt/m | q |
|---|---:|---:|---:|
| 0.7 | 0.589070 | 1.697592 | **−0.697592** |
| 1 | 1.717404 | 0.582274 | 0.417726 |
| 2 | 13.739232 | 0.072784 | 0.927216 |
| 3 | 46.369908 | 0.021566 | 0.978434 |

D0.7은 순수 drag에서도 속도 부호가 번갈아 바뀌는 수치 모드다. 연속 drag의 같은 dt 배율은 +0.183124이며, dt/2의 이산 배율은 +0.151204다(0.5 µs 한 step당 값이며, dt/2의 충분성까지 보증하는 수는 아니다). 순수 drag 안정 경계 2m/gamma=1.178139 µs보다 dt가 작으므로 **발산한다고 단정하지 않는다**. 전체 접촉망의 안정성·최종 압밀 오차도 이 계산만으로 결정되지 않는다.

그러나 “Rayleigh의 1.5%니까 충분하다”는 자격화는 성립하지 않는다. 현재 속도 덱은 gamma=1e−5인 settling만 실행하므로 이 모드를 시험하지도 않는다.

**최소 해결:** 새 물성 적합이 아니라 **시간 이산화 확인**을 등록한다. 같은 상태·같은 물리시간의 안정화/압축 짧은 구간에서 dt와 dt/2, 필요하면 추가 refinement를 대조한다. 비교 관측량·허용 오차는 결과 전에 고정하고, dump/판 이동/가압 판독 시간을 물리시간으로 맞춘다. 결과 전에는 dt 적합성 및 비용 추정을 조건부로 둔다.

재현: `python -B evidence/root/probe_numerics_and_endpoint.py`. 실제 DEM 실행이 아닌 원문 갱신식의 산술 반례다.

## 6. KG50-05 — D3 영역 시험의 합격 범위를 좁혀야 함

**위치:** `README.md:69–71`와 `docs/50kg/dem_plan_20261026.md`의 D3→모든 크기 선택.

D3에서 40/50을 비교하는 것은 합리적인 **공학적 사전 점검**이다. 하지만 아래 두 결론은 나오지 않는다.

1. 평균 차만 문턱 안이라는 이유로 모집단 차도 그 문턱 안이라는 결론.
2. D3가 가장 큰 SE라는 이유로 D0.7/D1/D2 수송량의 유한크기 오차까지 상한을 준다는 결론.

실제 KG50 결과가 아닌 합성 반례: porosity 두 그룹을 [19.69,20.00,20.31]%와 [20.09,20.40,20.71]%로 두면 양쪽 SD=0.31%p, 평균 차 −0.40%p이므로 현행 ±0.5%p 규칙은 PASS다. 독립 정규 표본 가정 아래 차의 90% 구간은 **[−0.9396,+0.1396]%p**로 허용 범위를 벗어난다. n=3씩, 같은 SD에서는 90% 구간 반폭부터 0.5396%p다. 이 산포를 KG50의 실측 산포로 쓰지는 않았다.

AM 직경은 같지만 L/D_AM=6.67·8.33인 두 영역에서 AM/SE 크기비는 D3의 2에서 D0.7의 8.57까지 바뀐다. 접촉망의 상관 길이·관통 경로가 D3에서 가장 불리하다는 정리는 제시되지 않았다.

**최소 해결·권고:** 저자가 선택한 D3 3시드 설계를 강제로 폐기할 필요는 없다. 다만 통과 이름을 “D3의 등록 지표 평균 차 기준 통과, 타 입경은 해당 영역을 채택한 탐색 비교”로 제한한다. 동등성·영역 수렴을 주장하려면 구간 기준 및 경계/미식별 상태를 결과 전에 정하고, 다른 입경으로의 이식 근거도 추가해야 한다. 현재 0.5%p/상대 5% 등의 지표 정의·상대 차 분모·비관통/비유한 처리·측정 프레임도 고정해야 한다. **여기의 porosity 문턱은 0.5%p**이며, 문구나 단위를 다른 수로 바꾸는 제안이 아니다.

주 값이 한 시드인 D0.7/D1/D2에는 seed 불확실성을 측정하지 않았다는 한정을 붙인다. D3의 표준편차를 그 셋의 오차막대로 전용하지 않는다.

재현: `python -B evidence/kg50_design/probe_design.py`의 `area_pilot_uncertainty`.

## 7. KG50-06 — settling timing은 압축 시간의 보증이나 이득 하한이 아님

**위치:** `scripts/make_se_size_decks.py:557`; `README.md:63–67`.

20,000 step은 덱 시간 0.02 s, 전체 5–7M step의 0.29–0.40%다. 그 구간에는 top mesh, 압축, atom/contact I/O가 없고, 중력은 98.1 대 9.81, viscous는 1e−5 대 0.5로 다르다.

문서의 이웃 수 138·65·19·11은 휴리스틱 식에 phi_SE=0.30을 넣으면 재현된다. 명목 **삽입 영역(reg_mix)** 기준 phi_SE는 0.1100766으로 예측되므로 같은 식은 약 50.53·23.78·7.04·4.08이다. 초기 침대·압축 침대·재구축 빈도를 섞어 단일 throughput으로 환산할 수 없다.

skin 2→0.5 µm면 최대 입자쌍의 single-communication halo 어림은 8→6.5 µm다. 둘 다 NP56 칸 폭 5.714×5 µm보다 크다. skin 감소가 halo를 없애지는 않는다. 더 잦은 rebuild와 더 적은 neighbor work 사이의 손익이 실제 하드웨어·밀도에 달린다.

**최소 해결:** KG50-01을 고친 동일 checkpoint 비교의 settling 시간은 “settling 측정”으로만 쓴다. 압축 대표 구간에서 같은 입자 상태·같은 출력 cadence를 둔 NP/skin 측정과 실제 peak memory/I/O를 별도로 기록한다. 본 런 ETA는 그 단계별 시간과 실측 남은 step으로 갱신한다. 1.5–3일은 현재 입증도 반증도 되지 않은 추정이다. source만으로 삽입 완료 시간·벽시계 시간을 보증하지 않는다.

skin 변경 자체가 접촉법칙을 바꾼다는 새 결함은 찾지 않았다. 공식 코드는 pair cutoff에 skin을 더하고 tag 기반 이력을 보존하며 이동 mesh도 rebuild 판단에 참여한다. 이것은 “설계상 같은 법칙”의 근거이고, 실제 바이너리/압축 궤적의 자격 증거와는 다르다. [neighbor.cpp](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/neighbor.cpp), [contact history](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_contact_history.cpp), [mesh rebuild](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_mesh.cpp).

## 8. KG50-07·08 — 설명과 정수 문턱의 작은 불일치

### KG50-07 / P3 — “체계적 부족” 단정 철회

**위치:** `make_se_size_decks.py:299–300,425`; 생성 덱의 SELF-70 설명.

정확 개수 모드도 rank별 템플릿 수를 먼저 floor한 후 **잔여 가중치로 빈칸을 배분**한다. 두 템플릿이면 AM은 local 기대값의 floor 또는 ceil이다. 따라서 floor만 인용해 항상 부족하다고 결론 내릴 수 없다.

또한 rank RNG는 독립 표본이 아니다. 공식 RanPark의 seed shift로 첫 추출값들이 매우 가까울 수 있다. 소스 규칙으로 가상 5580/5581 균등 배분을 계산하면 현재 pdd seed 11300017에서 AM 952, 옛 seed 32452867에서 896이 나온다(계획 948). **실제 speed 삽입은 KG50-01 때문에 이 숫자로 성공하지 않는다.** 이것은 배분 설명의 반례다.

[분포 배분](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/fix_particledistribution_discrete.cpp#L398), [RNG](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/random.cpp#L69).

**처방:** “rank·시드에 따른 상별 수 변동; 고정 시드에서 부족 또는 초과 가능; NP1로 변동 축소”로 고친다. NP1 사용과 실현 재고 검사는 지지한다. NP1도 이 계산에서는 948 또는 949가 가능하므로 계획과 모든 상이 항상 정확히 일치한다는 표현은 피한다.

재현: `python -B evidence/kg50_restart/probe_seeded_rounding.py`.

### KG50-08 / P3 — 정수 경계가 1입자 넓음

**위치:** `make_se_size_decks.py:297`; `make_ps_sweep_decks.py`의 삽입 하한 생성.

- 계획948의 정확한 ±0.5% 정수 구간은 944–952; 현재 943–953은 ±0.5274%.
- 계획1481이면 정확한 구간은 1474–1488; 현재 1473–1489는 ±0.5402%.
- D3-40 총수4906의 99%는 4856.94; floor4856은 98.98084%.

**처방:** 정확한 비율 규약이면 lower=ceil, upper=floor를 쓰고 테스트한다. 아니면 현재 정수 구간을 명시적 허용치로 등록한다. 이 한 입자 차이 자체를 다일 런의 P1으로 승격하지 않는다.

## 9. Q1–Q8 답

| 질문 | 답 |
|---|---|
| Q1 MPI·NP1→재개 | **NP1 삽입 권고 지지, 부족의 원인 설명은 수정.** 다른 NP로 restart 읽기는 지원된다. 그러나 동일 미래 궤적 보장은 아니다. 이번 고NP fresh 삽입에는 KG50-01이 먼저 걸린다. |
| Q2 G1–G3 | **정상 thermo 스케줄은 정합; 안전 관문으로는 REFUTED.** 기대 행 1·1000·2000·2001. KG50-02 수정과 외부 재개 덱 대조 필요. |
| Q3 skin | **같은 접촉법칙을 유지한다는 설계 설명은 조건부 지지.** 궤적·성능 동일성 및 압축 검증은 별도. 실제 후보 speed 경로는 먼저 고쳐야 한다. |
| Q4 quit1 | **지원 문법은 아님, 하지만 이 고정 소스에서는 비정상 종료한다.** `Input::quit`은 인자를 거부하고 `Error::all`이 exit(1). FATAL 후 checkpoint 전에 멈춘다. bare quit로 바꾸면 정상 종료로 바뀔 수 있어 무작정 교체하지 말 것. 실제 실행 바이너리의 음성 대조 필요. |
| Q5 3000회 삽입 | **int32 상한은 통과, 성공률은 미확인.** NP1 D0.7-40 예산937,518,000; 최대 fallback50의 안전 여유 포함1,904,334,900 <2,147,483,647. 이것은 성공 보장이 아니다. NP1 삽입 전용 짧은 관측을 장기 런과 분리해 확인. |
| Q6 시간 | **5–7M의 운동학적 오더는 정합, 1.5–3일 벽시계는 미검증.** 50–60µm 이동은5–6M step, 전후0.5M 포함5.5–6.5M. KG50-01·06 때문에 현 speed 결과로 보증 불가. |
| Q7 D3 영역 이식 | **공학적 선택 기준으로 한정 수용; 모든 입경의 영역 수렴 주장에는 반대.** KG50-05의 해석·결측·경계 규약을 먼저 고정. |
| Q8 추가 결함 | KG50-03 최종 프레임, KG50-04 drag 시간척도. 외부 재개 생성기·바이너리·실 삽입 성공은 미수령/미실행으로 남김. |

공식 restart 근거: [read_restart 문서](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/doc/read_restart.txt), [재분배 소스](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/read_restart.cpp#L206). quit 근거: [input.cpp:1110](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/input.cpp#L1110), [error.cpp:158](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/error.cpp#L158).

## 10. 유지되는 것·다음 순서

**유지되는 것:** AM D6·85wt%, 밀도4.85/1.64, 고체 두께101.9816µm, 영역·판 꼭짓점·압력 면적 두 곳, 계획 개수, 소수 seed, 허용 변경 범위, 삽입 prefix 바이트 동일, int32 방어는 이번 독립 검사에서 재현됐다. gen1 물성을 재적합하거나 임의의 새 물리 모델로 교체하라는 판정은 아니다.

단 `k ∝ R → 같은 압력에서 δ/R 동일`은 모든 입자와 하중 기하를 함께 닮게 스케일할 때의 유도다. 여기서는 AM을 고정하고 SE만 바꾸므로 혼합쌍·접촉망 전체의 겹침 불변까지 보증하지 않는다. 그 문장은 “동일 물성·고정 gen1 규약을 비교에 사용” 정도로 한정한다.

| 단계 | 이번 판정 | 선행 조건 |
|---|---|---|
| 오프라인 생성·산술·문서 정정 | GO | 고정 바이트 유지 |
| NP1 삽입 전용 진단 | 설계상 진행 가능 | 실제 binary 신원·정상/실패 기록·총수/상 재고 확인; 이 보고서가 실행을 대신 승인한 것은 아님 |
| 현재 네 fresh NP28/56 speed 덱 | **HOLD** | KG50-01 |
| 수정된 동일 침대 speed 비교 | 조건부 | KG50-01·02 수정, 완료·상태 비교, 압축 시간은 별도 |
| D3 영역 비교 자료 생산 | 조건부 | 최종 동기 출력, 저자 판정선·해석 범위 고정, actual binary/삽입 확인 |
| D0.7/D1 재개 후 다일 본 런 | **HOLD** | KG50-01·02, 최종 출력, 실제 재개 덱, D0.7 dt 자격화 |
| 네 SE의 정량 그림·영역 수렴 주장 | HOLD/범위 제한 | 완료된 동일 상태 산출물과 미확인 범위 해소 |

순서는 **코드/출력 최소 수정 → 합성 실패 관문 → NP1 삽입 재고 → 실제 생성 재개 덱 대조·짧은 정상 완료 → 압축 구간 수치/성능 확인 → 저자 결정 후 본 런**을 권한다. 새 무거운 연구 캠페인을 자동으로 추가하라는 뜻은 아니다. 실패한 시험을 넘겨서 장기 실행으로 확인하는 순서는 거부한다.

## 11. 재현·증거

```bash
# 이 리뷰 폴더에서. 생성/산술만 수행; LIGGGHTS·scheduler 실행 없음.
python -B snapshot/repo/scripts/make_se_size_decks.py --selftest
python -B evidence/kg50_decks/audit.py
python -B evidence/kg50_decks/audit_fallback.py
python -B evidence/kg50_design/probe_design.py
python -B evidence/kg50_restart/probe_source_semantics.py
python -B evidence/kg50_restart/probe_seeded_rounding.py
python -B evidence/root/probe_numerics_and_endpoint.py
```

- `evidence/intake.json`: 첨부 해시와 파일별 바이트/신원.
- `evidence/kg50_decks/`: selftest,38파일 재생성,86항 대조,각 덱 diff, fallback·출력 cadence 탐침.
- `evidence/kg50_design/`: 24개 공식 소스 blob 대조, 삽입 불가능성·시간/영역 산술.
- `evidence/kg50_restart/`: 정상·실패 합성 로그 조건, seed 배분, 공식 restart/quit 근거. `probe_resume_gates.py`는 준비된 Bash harness이며 실행 통과 목록에서 제외.
- `evidence/root/`: 사용자 pin 진술, viscous/적분 원문, drag·최종 프레임 독립 계산.

정상 결과와 반례가 함께 보존돼 있다. 과거 전체 게이트 또는 이 selftest를 실제 ibb/hit 완주 증거로 전용하지 않는다.

**최종: HOLD — P1 2건을 닫고, 최종 상태 출력·D0.7 수치 자격화까지 확보한 뒤 본 런으로 진행.**

