# Q1 독립 검토 — 재시작·벽 이력 (2026-10-11)

검토 범위: 제출 요청 Q1(a–f), 실행 등록 §3·§10 Q6/Q11, 지정된 분기 README/재개 절차, LIGGGHTS-PUBLIC `3d5c00f20519e6bb6eb6756f51f1ad36564e649d` 원문. 시뮬레이션·생산 코드·Git 변경 없음. 아래 줄은 **로컬 원문 파일의 1-based 줄**이다. `upstream/` 파일은 원저장소 `src/` 파일에 대응한다. 추가 두 파일은 `notes/source_extra/`에 있다.

## 결론

Q1 전체: **현재 문안은 HOLD, 수정 후 재개 진단 단계 GO**. 복원 기능 자체가 없는 문제가 아니다. 소스는 pair·primitive·mesh 이력 복원을 지원한다. 그러나 현 G4는 (1) primitive 바닥을 출력하지 못하고, (2) 활성 compute를 둔 채 벽을 unfix하면 오류, (3) uncompute 후에도 첫 run 뒤 같은 compute를 재정의할 수 없으며, (4) R 2,000 step 뒤의 이력 대비는 S0 이력 복원 증명이 아니다. 이 미확인을 표지만 달고 본 U로 넘기는 §10 Q6은 바꿔야 한다. G2c의 “setup에서 이력 갱신 전혀 없음”도 소스와 다르다.

| 세부 | 판정 | 핵심 |
|---|---|---|
| (a) restart 복원 | 조건부 GO | 동일 ID뿐 아니라 동일 style·모델·이력 배열 순서와 길이·벽 기하·재료값을 재선언할 때 복원 경로 존재 |
| (b) setup/G2c/NP | 수정 후 GO | shear 적분은 막지만 `deltaMax=max(deltaMax,delta)`는 setup에서도 수행. 힘 일치는 전체 숨은 이력의 일치를 증명하지 못함 |
| (c) wall/gran/local/G4 | HOLD | mesh만 지원, primitive 제외; 현 UN 경로 실행 불가; 2,000 step 뒤 R–UN은 복원 식별 검사 아님 |
| (d) move fix/unfix | GO | 같은 mesh/wall 유지 시 위치 이어지고 tracker 삭제 없음; 접촉이 물리적으로 끊기면 정상적으로 이력 소거됨 |
| (e) 10:0 r2→R | 조건부 GO | G0 기준은 r2의 S0 시점 PHASE 4 활성 정의. 파일 이름·이전 r 조각 수는 복원 알고리즘의 조건이 아님 |
| (f) 10:0 이완 연장 | 수정 후 조건부 GO | 유효한 새 고정판 이완 갈래. 재시작 관문을 먼저 통과하고, S0′ 재판정·기술자/기준 재계산·계보 분리 필수 |

## (a) 이력 복원의 실제 경로

공통 복원은 `modify.cpp:863–911`이다. global 및 per-atom restart 목록에서 **ID와 style이 맞는** fix에 `restart()`/`unpack_restart()`를 호출하고 `Resetting ... state of Fix ... from restart file info`를 로그에 남긴다. 따라서 눈에 보이는 wall fix ID만 같다는 서술보다 내부 fix 이름까지 검사하는 것이 정확하다.

- Pair: `normal_model_hooke_hysteresis.h:64–70`이 `deltaMax`를, `tangential_model_history.h:66–80`이 shear x/y/z를 이력에 등록한다. `pair_gran.cpp:286–316`은 첫 init 때 내부 `contacthistory` fix를 만든다. `fix_contact_history.cpp:93–102`는 global/per-atom restart를 활성화하고, `554–581`은 배열 길이 검사, `588–634`는 partner atom ID와 각 이력 값을 저장/복원한다. 따라서 `read_restart` 뒤 첫 run 전 동일 pair 모델을 재선언하는 머리는 이 복원 경로를 이용할 수 있다. `dnum` 길이만 같다고 다른 모델/순서를 허용할 수는 없다.
- Primitive 바닥: `fix_wall_gran.cpp:497–519`는 `history_<wall ID>`를 `property/atom` vector, restart=yes로 만든다. 여기서는 `history_zwall_bot`이다. `fix_property_atom.cpp:102–106,174–189,449–473`에서 per-atom restart와 배열 복원을 확인한다.
- Mesh 판: 기하는 `fix_mesh.cpp:216–220,405–443,690–702`의 restart 경로로 복원된다. 동일 ID/style의 global restart가 있으면 STL은 존재 여부만 검사하며 실제 기하는 binary restart에서 온다. 입자–삼각형 이력은 별도 경로다. `fix_wall_gran.cpp:482–488` → `fix_mesh_surface.cpp:687–709`가 `tracker_<mesh ID>` (`tracker_top_mesh`, style `contacthistory/mesh`)를 만들며, `fix_contact_history_mesh.cpp:613–645`가 triangle partner ID와 이력 배열을 복원한다. 기하가 맞아 보이거나 STL MD5가 같다는 것만으로 tracker 복원을 대신하지 못한다.

최소 추가 gate: 같은 실행에서 `contacthistory` global/per-atom, `history_zwall_bot` global/per-atom, `top_mesh` global, `tracker_top_mesh` global/per-atom의 reset 로그를 확인하고 빠진 항목은 TECH. 실제 존재하는 재시작 항목을 기준으로 목록을 고정한다. 이 로그는 로드 경로의 증거이며 모든 값이 원본과 같다는 독립 수치 증거와는 구별한다.

기존 실행의 직접 증거도 있다. 추출된 `evidence/ps73_logs/home/yonghoon/dem_test/ps45/logs/output_ps_7_3_r45_r8_220537.out:31–32,82–90`에 위 다섯 종류의 global/per-atom reset 로그가 모두 있다. r8 덱 `.../ps_7_3_r45/input_ps_7_3_r45_r8.liggghts:90,95,98,116–117`은 해당 pair/compute/벽/메시 정의를 확인한다. 이는 r8의 해당 재개에서 로드 경로가 실제 실행되었다는 기존 증거다. 새 S0 머리와 10:0의 성공을 대신하지는 않는다.

## (b) setup·G2c·rank 변경

`verlet.cpp:142,174–198`의 setupflag 안에서 pair/wall 힘을 다시 계산한다. `pair_gran.cpp:665–669`와 `fix_wall_gran.cpp:736–743`는 setup의 shearupdate를 0으로 만든다. local compute 재평가도 `pair_gran.cpp:699–704`, `fix_wall_gran.cpp:752–758`에서 두 flag를 0으로 둔다. 접선 모델의 시간 적분·회전·미끄럼 재설정은 `tangential_model_history.h:143–159,195–199`의 guard로 막힌다.

그러나 normal 모델 `156–158`은 `if (deltan > history[0]) history[0] = deltan;`를 **guard 없이** 수행한다. `165`의 `update_history`는 `176–177,191–192`의 점착 가지 재설정에만 쓰인다. 분리 경로에서도 `normal_model_hooke_hysteresis.h:257–261`, `tangential_model_history.h:358–368`이 이력을 0으로 만든다. 정상 복원 상태에서 이미 deltaMax≥현재 overlap이면 max 연산은 값에 영향이 없지만, 이를 “모든 이력이 갱신되지 않는다”라고 쓰면 틀리다.

G2c는 유용한 **초기 접촉 힘 지문**이다. 다만 힘→이력 역변환은 일대일이 아니다. 포화 deltaMax들은 같은 힘을 만들고, Coulomb clipping은 여러 shear 크기를 같은 접선 힘으로 보낼 수 있다. 접선 힘에 dashpot도 포함된다(`tangential_model_history.h:165–175,214–217`). 따라서 “접선 힘이 0 아닌 몫”은 저장 shear의 식별 가능한 몫과 같지 않다. 가능한 경우 pair의 `history` 열을 추가하여 기록하되 기존 contact_S0에 이력 열이 없으면 과거 원자료와 직접 비교한 것으로 쓰지 않는다.

NP 변경은 지원된다. `read_restart.cpp:218–244`는 원 rank chunk들을 읽어 현재 subdomain 소유 입자로 재분배하며 `569–574`는 rank 변경을 오류가 아닌 warning으로 처리한다. Pair 이력은 partner tag에 매여 있고 i/j 역방향 복사에서 shear의 부호를 바꾸며 deltaMax는 바꾸지 않는다(`fix_contact_history.cpp:393–409`; 각 history의 newton flag는 위 모델 등록에 있음). 따라서 정확 같은 초기 상태의 **비퇴화 접촉**은 순서와 방향을 정규화한 뒤 동일한 접촉/힘을 기대할 수 있다. bitwise/문자열 동일과 이후 궤적 동일까지 보장하는 것은 아니다.

`compute_pair_gran_local.cpp:379–394,428–472`는 ghost 중복 제거·tag 방향·periodic ghost flag·위치 remap의 근거다. 현 무순서 pair-key, 위치 swap, 힘 부호 swap, ghost flag 제외는 맞는 방향이다. 추가로 duplicate-key/자기쌍을 검사하고, history를 비교한다면 shear만 방향 반전하고 deltaMax 등 scalar는 그대로 둬야 한다. 좌표는 periodic remap 후 비교한다. near-zero 열에 중앙값도 0인 경우 현 상대 오차식은 허용폭 0이므로 출력 자릿수에 맞는 절대 floor를 별도로 등록하는 편이 안전하다. 진짜 접촉 집합 차이를 단순 “MPI 끝자리”로 통과시키지는 않는다.

G2 원자 열에는 `omega`도 추가하는 것이 맞다. 회전 상태가 접선 상대속도/힘에 들어가므로 위치·선속도만 같다고 접선 힘 재현의 입력을 다 검사한 것이 아니다. G2c 불일치 시 NP 일치 초기 재생을 진단에 쓰는 것은 가능하지만, 미래 궤적 일치를 요구하거나 불일치 하나로 과거 ps45 조각 전체의 이력 소실을 단정하면 안 된다.

최소 문안: “setup/local compute는 접선 이력의 시간 적분과 미끄럼 재설정을 억제한다. hooke/hysteresis의 deltaMax 상한 갱신 및 분리 소거는 예외다. G2c는 방향·주기 정규화 후의 초기 접촉 힘 재현 검사이며, 모든 숨은 이력의 동일성을 단독으로 입증하지 않는다.”

## (c) G4를 막는 구체적 문제와 최소 대체

1. 문법은 존재한다. `compute_pair_gran_local.h:44–45`가 pair 및 wall 스타일을 같은 클래스에 등록하고, `.cpp:93–107`이 `force_tangential`, `history`를 받는다. 단 `.cpp:247–269`는 **mesh wall만 선택**하고 primitive에 대해 “output will only happen for mesh wall - particle pairs” 경고를 낸다. primitive 바닥을 같은 compute로 따로 판정한다는 등록은 실현되지 않는다. 메시 ID/triangle ID/particle ID는 `648–685,777–780`에 있으며 이력 열 수는 `275–279`에서 dnum에 의해 정해진다.
2. 현 UN은 실행되지 않는다. `fix_wall_gran.cpp:541–542`는 활성 `wall/gran/local`이 남아 있으면 unfix를 거절한다. 따라서 해당 dump 해제 및 compute 해제가 선행되어야 한다. 그러나 `compute_pair_gran_local.cpp:126–127`은 timestep>0이고 restart 진행 중이 아니면 새 compute 정의를 금지한다. `modify.cpp:206–210`은 첫 run init에서 저장된 restart 자료를 해제한다. 곧 R 2,000 step 뒤 uncompute→wall 재정의→같은 compute 재정의라는 단순 수정도 실패한다. 이 경로는 키트에서 별도 진단 설계로 바꾸고 정적 문법 및 짧은 진단 단계에서 확인해야 한다. 여기서 검증되지 않은 reset_timestep 우회나 다른 기하 생성문을 확정 실행안으로 제시하지 않는다.
3. 이력 소거 자체는 사실이다. `fix_wall_gran.cpp:528–556`은 primitive history 및 mesh tracker를 삭제하고, `fix_mesh_surface.cpp:715–722`가 tracker를 실제 삭제한다. 첫 run 뒤에는 원 restart 자료도 없어 같은 ID로 다시 정의해도 원 이력이 다시 복원되지 않는다.
4. **G4의 2,000 step 시점은 restart 식별에 너무 늦다.** 처음 이력을 잃은 R도 2,000 step 동안 접선 spring을 새로 쌓고, 직후 강제로 지운 UN과는 10배 이상 다를 수 있다. 반대로 올바른 복원이라도 shear가 작거나 dashpot가 지배하면 10배를 못 넘는다. 중앙값은 contact-set 차이, 0/0, 국소 소실을 숨긴다. 특히 등록된 부등식 그대로는 R 중앙값=UN 중앙값=0일 때도 0≥10×0이므로 **판별력 0인데 PASS**한다. 비영 접촉이 절반 미만인 경우 국소 이력이 있어도 중앙값은 0이다. “R median ≥10×UN median”은 복원 통과 기준으로 부적합하다.
5. primitive 직접 관측 후보는 내부 `history_zwall_bot` per-atom 배열이다. `fix_property_atom.cpp:174–178`이 peratom_flag와 vector 열을 공개하므로 `dump custom ... f_history_zwall_bot[N]`가 생산 모델을 바꾸지 않는 관측 경로 후보다. 정확 열순서/길이와 dump 문법을 키트에서 확인해야 하며 이번 읽기만의 검토에서 실행 검증한 것으로 쓰지 않는다.

판 압력의 민감도 판독은 대체로 맞다. 무한 평면/평평한 판 내부 face의 normal이 z이면 접선 힘의 z 투영은 0이다(`compute_pair_gran_local.cpp:789–812`의 normal/tangent 분해). 포화 가지의 normal은 `normal_model_hooke_hysteresis.h:163–169`에서 deltaMax 수치와 무관하다. 다만 메시 edge/corner 접촉, 비포화 접촉, 이후 운동은 이력을 잃을 때 판 압력을 바꿀 수 있다. “거의 못 본다”는 포화/평면 조건 아래 설명이며 실제 접촉 분포 확인 없이 보편 명제로 만들지 않는다.

최소 문안: “벽 재시작은 적분 전 S0에서 내부 fix 복원 로그와 이력 배열로 판정한다. 메시 판은 wall/gran/local history를, primitive 바닥은 내부 per-atom history의 관측 경로를 사용한다. 가능한 원 restart 배열/원 참조 값과 매칭하며, 아직 확보되지 않은 직접 대조는 미검증으로 구분한다. R–UN은 이력 소거에 대한 관측자의 반응을 보는 보조 진단이고 복원 증명이 아니다. 본 U는 벽 복원 관문이 확인된 침대에서만 제출한다. 정보 부족·문법 오류·복원 불일치는 분리 기록하며, 미확인을 표지만 달고 본 U로 넘기지 않는다.”

## (d) 같은 top_mesh의 move→run→unfix

GO. `notes/source_extra/mesh_mover_linear.cpp:79–86`의 등록/해제, `94–111`의 dx=v·dt 이동 → `fix_mesh.cpp:733–735` → `multi_node_mesh_I.h:502–525`는 **현재 노드에 dx를 더하는** 경로다. linear는 매 run 원래 위치로 되돌리는 절대 이동이 아니다. `fix_move_mesh.cpp:122–164`의 unfix는 mesh 속도를 0으로 만들고 이동 등록/참조점만 지우며 mesh나 contact tracker를 지우지 않는다. `multi_node_mesh_I.h:392–407`의 해제도 node_orig 보조 저장소만 삭제한다. 다음 move 등록은 당시 현재 노드를 기준으로 만든다(`354–383`).

따라서 같은 mesh/wall fix를 유지하는 계단은 위치·저장 이력을 이어 간다. 이를 “모든 접촉의 이력이 영구 보존된다”로 쓰면 안 된다. 접촉이 실제로 끊기거나 다른 삼각형으로 넘어가면 접촉법칙/메시 알고리즘에 따른 이력 변화가 있다. 이동 뒤 setup 압력 합 문제는 별개이므로 기록은 정상 step/run 경계 규칙을 따라야 한다.

## (e) 10:0 원 덱형 r2에서의 첫 재개

G0의 기준을 **r2가 S0에서 켜 두었던 PHASE 4 정의**로 잡는 것이 맞다. 초기 r2 머리의 settling gravity 98.1이나 압축 damping 0.5를 그대로 복제하면 틀린 모델이다. precheck1 원 화면 `181–194`에는 r2 restart·mesh 생성 및 나중 gravity 9.81, damping 1e-5 전환이 있고, `200–206`에는 정확 pin과 S0 restart 해시가 있다. 원 생성 덱은 `in.ps_10_0_r45.liggghts:93,101,183–184,212–217`에서 pair/walls·move 해제·이완 damping을 보여 준다.

복원 알고리즘은 “r8인지 r2인지”를 보지 않는다. 내부 mesh ID/style, tracker, primitive history와 pair 이력이 있는 restart인지가 조건이다. 따라서 (a)의 근거가 동일하게 적용된다. 다만 제공된 사본에는 ibb r2 전체 덱·binary restart가 없고 화면 발췌만 있다. 현재 검토는 **메커니즘을 확인한 것**이며 r2 전체 활성 정의를 G0로 실제 대조 완료했다는 뜻은 아니다. 생성 키트 전에 마지막 r2 전체 덱·hash를 확보하고 변수/재료표/벽 모델까지 S0 활성 상태를 정적으로 재구성해야 한다. G0의 문자열 동일 요구는 관측용 compute 추가와 output 경로/주기 차이를 별도 허용목록으로 명시하는 편이 실행 가능하다.

## (f) 10:0 60,000 step 이완 연장

승인된 고정판 연장은 유효한 F2의 세부형태다. 압축 정지점·판 높이를 다시 만드는 것보다 좁은 변경이다. 기존 F2 정의가 “압축 끝부터 재생성”이므로 명칭을 `F2-relax: 같은 압축 상태에서 고정판 이완을 연장한 새 갈래`처럼 분명히 보완하면 된다. 3,600,000+60,000=3,660,000이고 S0′는 마지막 restart 3,650,000인 계산은 일관된다. 이는 3,650,000 주변 +5,000 창까지 관측할 여유도 있다.

다만 다음을 최소 보완한다.

- 연장 전 재개 검사는 G1–G3만이 아니라 수정된 G0/G2c/벽 복원 gate도 적용한다. 잘못 복원된 상태를 먼저 60,000 step 이완하면 오차를 완화/은폐한 뒤 새 S0로 승인하는 꼴이 된다.
- R 시험 2,000 step 후 production 연장은 **다시 원 3,600,000 checkpoint에서 시작**한다고 명시한다. R 상태를 이어 run 60,000하면 끝이 3,662,000으로 달라진다. 등록의 62,000 비용 표기는 두 독립 실행이라면 맞다.
- 3,650,000의 ±5,000 정규 압력과 연장 런 마지막 25줄의 1% gate를 다시 적용한다. 실패 시 사전 등록한 추가 50,000 한 번/S0″ 규칙을 고정하고 이후 기준 완화는 하지 않는다. 추가 연장은 3,700,000+5,000까지 정규 출력이 반드시 있어야 한다.
- h0, 원자 수/상별 질량, 압력, D(S0′), 대안 기술자, KE(회전 포함) 기준을 새 상태에 맞춰 기록한다. 고정판·무입자손실이면 h0와 sphere 고체량은 유지되지만 접촉 이력/배열은 바뀔 수 있으므로 자동 같다고 간주하지 않는다.
- 원 갈래 3,640,000와 새 갈래 같은 step에서 atom-ID별 위치/속도/omega, 원자·접촉 수, h, pressure, KE, D 및 가능한 이력 차이를 기록한다. 출력 자릿수와 NP(11→6)·분기 checkpoint 해시를 함께 남긴다. 이는 branch difference이며 오직 NP 효과로 분리했다고 주장하지 않는다.

다른 네 침대가 PHASE4+65–90k이고 10:0이 +109,999인 것은 이 다섯 등록 상태의 조건부 회복률 비교를 금지하지 않는다. 그러나 조성 효과와 잔류 이완 상태를 분리한 실험은 아니다. 따라서 해석은 “각 등록 S0의 회복”으로 한정하고 동일한 안정성/무이동 표류 기준을 다섯에 적용한다. 불균등 이완 길이를 모델의 경과시간 물성으로 해석하지 않는다. equal-age 또는 동일 잔류에너지 비교를 새로 요구하는 것은 현 질문보다 강한 별도 설계다.

## 남는 불확실성

- ibb binary restart, 실제 R/UN 결과, 실제 내부 history 배열 및 r2 전체 덱을 이 검토에서 읽지 않았다. 소스의 복원 지원과 특정 침대에서 복원 성공은 구별한다.
- 같은 NP에서도 bitwise 장기 궤적 일치를 보증하지 않는다. rank 변경에 따른 초기 출력 ordering/roundoff와 실제 값 불일치를 구별할 판독기 구현 검증이 필요하다.
- primitive history custom dump와 새 UN 경로는 읽기만의 검토에서 실행하지 않았다. 모델 소스 수정 없이 가능할 유력 관측 경로를 제시한 것이다.
- 추가 소스 SHA256: `mesh_mover_linear.cpp` = `a63597ff09175a5050958de45fbb458daa100ed5885e8c8d3c52e1249f41a957`; `multi_node_mesh_I.h` = `c6a468d8e92728199845fd60718c514622af44cdbbc5f8cf552a0ab9d82e526f`. raw 주소는 `https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/<filename>`.
