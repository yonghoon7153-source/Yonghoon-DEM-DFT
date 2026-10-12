# Q5 복원 관문 및 Q6 10:0 이완 연장 — 독립 소스 재검토

검토 범위: `submitted/request.md:44–45`, `submitted/prereg.md:599–609,676–685`. 시뮬레이션, WSL, 생산 코드 수정, git 명령은 실행하지 않았다. 고정 소스 `3d5c00f20519e6bb6eb6756f51f1ad36564e649d`의 기존 로컬 사본 및 추가 확보한 이번 묶음 `upstream/`을 직접 읽었다. 아래의 시험 설계는 실행 결과가 아니다. 추가소스의 정적 확인으로 PRE_SETUP `write_dump` 및 소거 restart 경로까지 아래에 보강했다.

## 판정 요지

- **Q5 문서 몫은 닫힘 가능.** §12-1은 G4를 폐기하고 내부 복원 로그와 값 관측을 구별하며, primitive/mesh 관측을 분리하고, setup의 예외 및 미확인 U 차단을 명시한다. 앞 판정 §8의 문서 항목 1 (`codex_review_dem_unloading_prereg_20261011.md:294`)에 대응한다. `③`의 round-trip/소거는 검사의 판별력 시험으로 타당하다. 다만 성공 증거가 제출되지 않았으므로 앞 판정의 별도 키트 항목(`:301–305`)이 닫혔다고 쓰면 안 된다.
- **Q6 주 일정은 닫힘 가능.** §12-11:678은 앞 판정 Q1(f):93–95의 원 3,600,000 재읽기, 60,000, 연장 전 복원 관문, 같은 3,640,000 대조, NP 11→6, checkpoint SHA 및 NP 인과분해 금지를 그대로 반영한다. 이것만으로 새 문서 HOLD를 만들 근거가 없다.
- 키트에 필요한 구체화는 아래의 관측 시점, 비퇴화 fixture, contact-key/열별 비교, 소거 경로, 추가 연장의 시작점이다. 과거 history/omega가 없으면 없는 값까지 직접 대조했다고 쓰지 않는 제한도 유지한다.

## 1. 소스로 확인한 사실

이 절의 경로는 `dem_unloading_review_20261011/upstream/` 기준이다.

| 사실 | 직접 확인 위치 | 의미 |
|---|---|---|
| primitive wall의 내부 ID는 `history_` + wall ID, `property/atom vector`, restart yes, 초기값 0 | `fix_wall_gran.cpp:497–519` | `zwall_bot`이면 `history_zwall_bot`; 벽 선언 이후에만 참조할 수 있다. 별도 동일 ID fix를 사용자가 덧붙이지 않는다. |
| per-atom 배열의 열 수와 매 step 접근이 공개됨 | `fix_property_atom.cpp:174–178` | `f_history_zwall_bot[N]`의 일반 custom-dump 경로와 연결되는 구조이다. 실제 parser와 바이너리 문법 시험은 별도로 필요하다. |
| property 배열은 fix 정의 때 할당되고 초기화되며, restart 복원이 그 뒤 일어남 | `fix_property_atom.cpp:184–218`; `modify.cpp:861–911` | 초기화 0만 보고 복원되었다고 할 수 없다. ID/style 일치 후 per-atom unpack이 호출되고 나서 관측해야 한다. |
| global/per-atom reset은 서로 다른 로그이며, 값 복원은 각 입자 unpack | `modify.cpp:866–908`; `fix_property_atom.cpp:449–473,571–580` | primitive에는 global 길이 일치 및 per-atom reset을 확인한다. 로그는 실행 경로 증거이고 배열 값 증거는 별도이다. |
| mesh tracker ID는 `tracker_top_mesh`, style은 `contacthistory/mesh` | `fix_mesh_surface.cpp:687–709`; `fix_contact_history_mesh.cpp:613–645` | geometry fix 복원 로그만으로 contact tracker 복원을 대신하지 않는다. |
| pair 내부 fix ID/style은 `contacthistory` | `pair_gran.cpp:299–316`; `fix_contact_history.cpp:572–581` | dnum 불일치는 소스가 거부한다. 같은 길이의 열 의미가 뒤바뀐 경우까지 길이 검사만으로 검증하지는 못하므로 모델/열순서가 별도 계약이다. |
| wall local compute는 mesh만 선택, primitive는 경고 후 제외 | `compute_pair_gran_local.cpp:247–269` | 바닥 값을 wall local 파일에서 찾지 않는다. |
| local dump는 contact force를 다시 평가한다 | `compute_pair_gran_local.cpp:300–335`; `fix_wall_gran.cpp:752–758` | 단순 메모리 덤프가 아니다. |
| run setup은 위치 소유권/주기 remap/neighbor 생성과 force 평가를 수행한다 | `verlet.cpp:142–198` | 적분 step이 0이어도 setup 전후 상태를 구분해야 한다. |
| setup/local 평가에서는 shear 시간 적분을 억제하지만 deltaMax 상한 갱신 및 분리 소거는 남는다 | `fix_wall_gran.cpp:736–758`; `normal_model_hooke_hysteresis.h:156–158,257–261`; `tangential_model_history.h:143–159,358–368` | reset 후 post-setup의 deltaMax가 0일 것이라는 음성 기대는 잘못이다. |
| 첫 run 초기화에서 restart cache 제거 | `modify.cpp:204–210,1283–1314` | 첫 run 전 wall 재정의는 같은 cache에서 원 이력을 다시 가져올 수 있다. 이를 소거 시험이라고 부르면 안 된다. |
| 활성 wall local compute를 둔 wall unfix는 거부 | `fix_wall_gran.cpp:541–542` | dump 해제 및 compute 해제를 wall unfix보다 먼저 한다. |
| 양의 timestep에서 새 local compute 정의는 restart 진행 중일 때만 허용 | `compute_pair_gran_local.cpp:126–127` | R 2,000 뒤 uncompute→unfix→refix→동일 compute 새 선언은 그대로 실행되지 않는다. |
| 벽 unfix는 primitive history와 mesh tracker를 삭제, top mesh 자체는 별도 fix | `fix_wall_gran.cpp:528–550`; `fix_mesh_surface.cpp:715–722` | 음성 대조는 top_mesh geometry를 보존하고 벽 history만 버릴 수 있다. |
| 다른 NP restart는 지원하며 경고로 처리 | `read_restart.cpp:218–244,569–574` | 이후 긴 궤적이 같다는 보장은 아니다. |

## 2. 키트에 고정할 관측 스키마와 시점

primitive 스키마는 최소 `id type x y z radius vx vy vz omegax omegay omegaz f_history_zwall_bot[1] ... [dnum]`이다. 모든 입자를 기록한 뒤 ID로 join한다. 현재 접촉 입자만 골라 기록하면 history 누락과 실제 접촉 해제를 혼동한다. 0을 버리지 말고 NaN/Inf, 중복 ID, 행 수, 예상 열 수를 검증한다. 가능한 최대 정밀도(예: 17자리)를 쓰고 출력 단위에 맞는 절대 허용폭과 상대 허용폭을 결과 전에 고정한다.

추가 로컬 원문 확인: [고정 dump_custom.cpp](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/dump_custom.cpp#L1367)의 **로컬 1367–1396**은 `f_` 다음 ID와 양의 정수 첨자를 파싱하고 배열 길이를 검사한다. **1835–1853**은 `array_atom[particle][N-1]`를 직접 pack한다. 따라서 **`f_history_zwall_bot[1]` 등 명시 정수 열 문법은 소스상 확인된다.** 첨자 없는 이름 또는 `[*]`를 임의로 사용하지 않는다. 이 parser는 `atoi`이므로 wildcard는 이 경로에서 유효한 양의 열 번호가 아니다. 소스상 지원과 실제 ibb binary 성공은 구분한다. 먼저 확인한 web 추출본은 빈 줄 처리 등으로 행 번호가 달랐으므로 이 문서에서는 확보한 로컬 파일 행을 정본으로 쓴다.

등록된 모델의 생성 순서는 surface→normal→cohesion→tangential→rolling (`contact_models.h:141–157`)이며 normal은 `deltaMax` 하나(`normal_model_hooke_hysteresis.h:70`), tangential은 `shearx,sheary,shearz` 세 개(`tangential_model_history.h:78–80`)를 추가한다. [고정 surface default](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/surface_model_default.h#L59)는 생성자에 이력 추가가 없고 추가 에너지 옵션이 기본 off이며, [rolling cdt](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/rolling_model_cdt.h#L59)는 이력을 추가하지 않는다. [hooke base](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/normal_model_hooke.h)는 생성자에 이력 추가가 없으며 hysteresis의 `postSettings`는 빈 override이다. 현 덱의 기본 옵션에서는 **4열 = deltaMax, shearx, sheary, shearz**가 맞다. 실제 G0에서 별도 에너지/추가 모델 옵션이 들어가지 않았음을 확인하고 dnum=4를 수락한다. 배열 길이만으로 열 의미까지 검증되었다고 쓰지 않는다.

따라서 작은 fixture에서 시험할 최소 PRE/POST 관측 블록은 다음과 같다(덱 머리/재료/벽은 G0와 같은 정의가 선행). 실제 성공 로그와 파일은 아직 없다. 별도 atom-state 스냅숏에는 위의 x/v/omega 열을 함께 넣는다.

```text
write_dump all custom bot_presetup.dump id f_history_zwall_bot[1] f_history_zwall_bot[2] f_history_zwall_bot[3] f_history_zwall_bot[4] modify format "%d %.17g %.17g %.17g %.17g"
compute wh all wall/gran/local id history
run 0
write_dump all custom bot_postsetup.dump id f_history_zwall_bot[1] f_history_zwall_bot[2] f_history_zwall_bot[3] f_history_zwall_bot[4] modify format "%d %.17g %.17g %.17g %.17g"
write_dump all local mesh_postsetup.dump c_wh[1] c_wh[2] c_wh[3] c_wh[4] c_wh[5] c_wh[6] c_wh[7] modify format "%.17g %.17g %.17g %.17g %.17g %.17g %.17g"
uncompute wh
```

키트는 세 파일에 S0 frame이 실제 생성되었는지 검사하고 header를 봉인한다. `write_dump.cpp:63–114`는 temporary dump를 만들고 **dump 자체 init→write**만 호출하며 `lmp->init()`/Verlet setup을 부르지 않는다. `dump.cpp:205–224,243–278`도 dump 설정/집계만 수행하고, 이 primitive 명령에는 compute/variable 열이 없어서 `dump_custom.cpp:434–447`의 추가 계산 경로를 쓰지 않는다. 따라서 위 첫 명령은 **복원된 primitive array를 setup 전에 직접 관측하는 정적 경로로 확인된다**. `format`은 `dump.cpp:571–580`의 단일 문자열 구문이다. 현대 LAMMPS의 `format float` 문법을 혼입하지 않는다. mesh는 `run 0` 후 local 재평가 경로이므로 raw restart의 무변경 판독이 아니다. `run.cpp:209–222`는 첫 run에서 setup을 수행하며 `run 0 pre no`로도 첫 setup을 건너뛸 수 없다.

mesh에는 예를 들어 `compute wh all wall/gran/local id history`를 첫 run 전에 선언한다. 출력 순서는 키워드 입력 순서가 아니라 구현 순서이며, 이 조합은 `(mesh index, triangle ID, particle ID, history[1..dnum])`이다 (`compute_pair_gran_local.cpp:679–685,777–780,845–848`). 최소 key는 이 세 ID의 tuple이며 mesh index와 실제 `top_mesh` 이름의 대응을 기록한다. fixture는 triangle seam/edge와 주기 경계에서 떨어진 face 내부에 두어 중복 및 contact transfer가 시험을 흐리지 않게 한다.

시점은 적어도 세 개를 명명한다.

1. `PRE_SETUP`: read_restart 후 활성 pair/material/wall 정의와 내부 unpack 완료 후, 첫 run/setup 이전 primitive 배열. 위의 `write_dump ... custom ...` 경로가 정적으로 확인되었으며 실제 파일/header 검사를 통과해야 관측 성공으로 쓴다. 이 시점의 primitive 값은 per-atom unpack을 본 것이지 mesh local 관측값이 아니다.
2. `POST_SETUP_S0`: `run 0`의 setup 및 local 재평가를 거친 값. atom step과 time가 S0 그대로여도 normal 상한 갱신/분리 소거의 가능성이 있다. mesh 관측 및 G2c는 이 이름으로 기록한다.
3. `R_END`: S0+2,000의 R/UN 보조 진단. 이것을 S0 원 이력 복원 증거로 승격시키지 않는다.

primitive의 PRE/POST를 함께 기록하면 setup에 의한 값 변화와 unpack 불일치를 직접 구분할 수 있다. mesh에는 일반 wall local만으로 raw restart 배열을 그대로 읽었다고 주장할 수 없다. 과거 생산 dump에 history가 없으면 '과거 history 직접 비교 미확보'라고 기록한다. 검증된 serialization 경로, reset 로그, 배열/형상 관측을 합친 실행 관문은 여전히 유효하며, 원본에 없는 참조값을 끝없이 요구하는 새 관문을 만들 이유는 없다.

로그 검사 시점도 분리한다. primitive/mesh tracker는 wall 생성 경로에서 복원되지만 pair의 `contacthistory` 생성은 `PairGran::init_style()` 안에 있다(`pair_gran.cpp:230,286–316`). 따라서 첫 run 이전 primitive PRE_SETUP 파일을 내는 순간에 pair reset 로그가 아직 없다는 이유만으로 TECH로 분류하면 안 된다. 첫 run 초기화에서 pair reset까지 확인한 후 복원 로그 묶음을 판정한다.

## 3. 작은 침대 round-trip/음성 대조의 최소 시험 행렬

작은 fixture는 bottom primitive와 top mesh 각각 적어도 하나의 지속 접촉을 가져야 한다. 동일 접촉법칙/내부 ID, 알려진 비영 접선 이력, 그리고 현재 overlap보다 큰 저장 deltaMax를 준비한다. 정상 재개에서 자동 max 갱신/분리로 값이 달라지지 않도록 `0 < current delta < saved deltaMax`이고 cohesive reset 경계·Coulomb clipping 경계·mesh seam에서 떨어진 접촉을 쓴다. 적재→부분 제하→작은 접선 변위로 이를 만들 수 있고, 원 producer에서 저장 직전의 이력과 상태를 관측해 기대값으로 봉인한다. 비영 이력이 확인되지 않은 fixture는 결과 0/0이므로 INCONCLUSIVE이며 PASS가 아니다.

| 행 | 입력/경로 | 기대와 수락 조건 |
|---|---|---|
| H0 문법 | 실제 ibb 고정 바이너리, 실제 모델/벽 옵션, 해당 열 포함 dump | exit 성공, 예상 ID/열 수/행 수, 내부 reset 로그. 성공했다고 값 보존까지 통과시키지 않는다. |
| H1 양성 round-trip | 알려진 fixture 저장→같은 NP에서 별도 프로세스 재개 | ID/key/형상/위치/v/omega 동일; primitive PRE_SETUP 전열 일치; mesh POST_SETUP 전열 일치. 절대+상대 허용폭 및 출력 정밀도를 로그와 함께 보관. |
| H2 rank-change | 같은 fixture checkpoint→다른 NP에서 재개 | 같은 key와 초기 배열 비교. row order 무시, pair의 방향 바뀐 shear만 부호 정규화. 장기 궤적 동일은 요구하지 않는다. |
| H3 primitive 소거 | 동일 fixture 복사에서 첫 run 후 bottom history만 소거 | 입자 상태/geometry 동일, bottom shear의 알려진 비영값→0. PRE_SETUP이면 deltaMax도 0, POST_SETUP이면 현재 overlap으로 재생될 수 있다. untouched mesh 이력은 유지. |
| H4 mesh 소거 | 동일 fixture 복사에서 첫 run 후 top wall tracker만 소거 | geometry/입자 상태 동일; 지정 mesh 접촉의 비영 shear 소실, 저장 deltaMax>현재delta인 sentinel은 감소. untouched primitive 이력은 유지. |
| H5 결손/모호 | 잘못된 내부 ID 또는 zero-only fixture | 로그 누락/키 누락을 TECH로 분류; zero-only를 PASS로 분류하지 않는다. 이 경우를 정상 production 로그 기대와 혼동하지 않는다. |

수락은 전체 배열의 key별 비교 및 지정 sentinel 접촉의 변화로 판정한다. 접선력 중앙값 10배, 전체 중앙값 0, 유의한 변화가 하나도 없는 음성대조로 수락하지 않는다. 판 압력 차는 보조 결과이다.

### 소거 뒤 local compute를 다시 정의하는 경로

같은 양의 timestep에서 compute 재선언을 강행할 필요가 없다. 작은 fixture의 별도 진단 사본에서 다음 순서를 키트로 시험할 수 있다.

1. 원 fixture를 읽어 필요한 observer를 첫 run 전에 선언하고 `run 0` 또는 기존 R을 끝낸다. 이로써 restart cache가 제거되었다는 조건을 확보한다.
2. 관련 dump를 `undump`하고 wall local compute를 `uncompute`한다. primitive property를 참조하는 dump도 bottom unfix 전에 해제한다.
3. 선택한 wall만 unfix한다. `top_mesh` geometry fix는 유지한다. 이때 primitive 내부 property 또는 mesh tracker가 삭제된다.
4. 해당 wall이 없는 진단 restart를 별도 파일로 저장한다. pair/입자/mesh geometry 상태의 checkpoint다. 원본을 덮어쓰지 않는다.
5. 새 프로세스에서 이 진단 파일을 read_restart하고 원 wall ID/style/options를 선언한다. 소거된 history의 reset 로그는 없어야 하고 신규 history는 초기 0이다. 이력 파일의 목적에 맞게 음성 대조의 로그 기대를 따로 둔다.
6. 이 새 restart의 첫 run 전에 compute와 dump를 정의하고 PRE_SETUP primitive 및 POST_SETUP primitive/mesh를 관측한다. 이를 양성 경로의 같은 시점에 대조한다.

이 방식은 양의 timestep compute 재정의 제한을 피하는 **정적으로 확인된 키트 설계**이다. 추가 확보한 `write_restart.cpp:166–190`에는 `lmp->init()`, `modify->setup_pre_exchange()`, PBC/remap 및 atom/mesh exchange가 있다. 따라서 이를 '어떠한 전처리도 없는 메모리 그대로 저장'이라고 쓰지 않는다. 그러나 해당 command는 force 재평가나 적분을 호출하지 않으며 삭제한 벽/history를 다시 생성하지 않는다. 현재 활성 fix만 `modify->write_restart`로 쓰고 atom restart를 pack한다(`:263,285`). top_mesh는 유지되어 geometry가 이어지고, 삭제된 tracker/property는 파일에 실리지 않는다. 새 프로세스에서 원 벽을 선언할 때 그 두 history는 새로 0 초기화된다. 저장 전후 atom ID/위치/v/omega와 mesh geometry를 정규화하여 대조하고, 저장 중 재분배/접촉 정렬을 row-order 차이와 분리한다. ibb fixture 성공 전에는 실행 검증한 경로라고 쓰지 않는다. post-setup 음성 값은 deltaMax까지 전부 0일 필요가 없다는 점이 핵심이다.

최소 순서 예시는 다음과 같다. 아래는 `run 0`이 끝나고 위의 일회 write_dump들이 닫힌 **별도 진단 프로세스**의 후속이다. 상시 dump가 있다면 해당 `undump`를 먼저 추가한다.

```text
# wh is still active here only if not yet uncomputed above
# uncompute wh
unfix zwall_top
unfix zwall_bot
write_restart negative_no_wall_history.bin
```

그 후 새 프로세스에서 `read_restart negative_no_wall_history.bin` → G0와 같은 재료/pair 및 `top_mesh`/wall 정의 → 위 PRE/POST 블록을 적용한다. 양성 control도 같은 serialize/reload 횟수를 거치되 wall unfix를 생략하면 저장 자체 효과와 소거 효과를 분리할 수 있다. H3/H4는 각각 bottom/top 중 하나만 unfix해 나머지 history가 보존되는지도 검사한다.

## 4. 생산 S0에 적용하는 관문

키트 fixture 통과는 특정 생산 파일의 과거 원상태를 대신하지 않는다. 각 침대 S0에서는 checkpoint SHA, 바이너리/덱/mesh SHA, G0 활성 상태, 내부 ID/style/dnum 및 reset 로그, S0의 atom/geometry/history 스냅숏을 묶는다. ①–⑤를 시행한 결과를 `RESTORED`, `UNCONFIRMED`, `SYNTAX_FAIL`, `VALUE_MISMATCH`처럼 구분할 수 있다. 미확인/실패에서 U를 막는 규칙은 이미 §12-1:606에 명시되어 있다.

실제 ID/style 불일치, 길이 mismatch, 값 불일치가 있으면 TECH이다. 반면 원 생산 덤프에 없는 과거 history 열의 직접 비교는 '미확보'라고 제한을 밝힌다. 알려진 이력을 보존/소거하는 경로의 시험과 실제 S0의 reset/값 관측이 있으면 그 증거 수준으로 판정해야 하며, 기록되지 않은 과거 배열을 새로 요구해서 문서상 닫힌 UL-01을 자동으로 재개방하지 않는다.

## 5. Q6 일정과 남는 구현 체크

§12-11:678의 주 산술은 정확하다.

| 실행 | 시작 | 길이 | 끝 | 판정/용도 |
|---|---:|---:|---:|---|
| 독립 R | 3,600,000 | 2,000 | 3,602,000 | 복원/재개 관문; 생산 연장의 상태로 이어 쓰지 않음 |
| 주 이완 연장 | 원 3,600,000 재읽기 | 60,000 | 3,660,000 | S0′=3,650,000; ±5,000=[3,645,000,3,655,000] 확보 |
| 필요시 추가 연장 1회 | 3,660,000의 연장 상태 | 50,000 | 3,710,000 | S0″=3,700,000; ±5,000=[3,695,000,3,705,000] 확보 |

- 추가 50,000을 별도 job으로 만들면 주 연장 끝 3,660,000의 checkpoint가 실제 존재하는지 확인하고, 없다면 명시 `write_restart`로 저장한다. `3,660,000 % 50,000 = 10,000`이므로 주기 배수는 아니나, run 종료 시 자동 write 여부는 `output.cpp`의 별도 규칙에 달려 있다. 그 소스를 확인하기 전 modulo만으로 '파일이 생기지 않는다'고 단정하지 않는다. 기존 '같은 머리로 50,000'을 원 3,600,000 재읽기로 오해하거나 S0′=3,650,000에서 50,000만 더하고 끝내면 S0″의 미래 +5,000 창이 없다는 일정 계산은 맞다.
- **접촉 출력 누락 지적 철회:** `3,650,000 % 10,000 = 0`이며 S0′는 contact 주기 10,000과 일치한다. 앞 메모의 '배수가 아니다'는 검토자의 산술 오류였다. 이를 근거로 별도 스냅숏을 요구하거나 등록 결함으로 싣지 않는다. 실제 생성 파일의 존재/완전성 확인은 통상 키트 검사이다.
- 원 갈래와 새 갈래의 3,640,000은 실제 제공 가능한 열끼리 비교한다. 기존 reference 생성 덱 `source/docs/reviews/codex_ps45_porosity_evidence_20261001/reference/dem_scripts/ps_sweep_6mah_20260914/in.ps_10_0_r45.liggghts:200`에는 omega 열이 없다. ibb의 실제 r2 전체/3,640,000 원덤프는 이번 자료에 없으므로 실제 부재까지 단정하지 않는다. 원 헤더를 확인하여 없는 omega/회전 KE/history는 미확보라고 쓰고, 새 갈래는 필수 출력한다. 과거에 없는 값을 사후 직접 대조했다고 쓰지 않는다.
- 위치는 ID별·주기 remap 정규화, 접촉은 canonical key 및 유효 contact 정의로 비교한다. 원자 수/h/상별 질량 및 가능한 KE/이력도 같은 행에 기록하면 앞 판정의 뜻을 충족한다.
- NP 변경 지원은 초기 unpack의 실행가능성 근거이다. 40,000 step 후 차이는 branch difference이며 NP 단독 효과 또는 복원 실패 단독 증거가 아니다. 7:3의 다른 NP 보조 진단을 10:0 장기 궤적 동일성 의무로 확대하지 않는다.

위 구현 체크는 추가 대규모 시뮬레이션이나 새 압축 캠페인 요구가 아니다. 문서 개정은 허용하고, 원래 예정된 키트 및 작은 ibb 증거 제출 단계에서 확인하면 된다.

## 6. 최종 보고서 §5–6 교차검사 및 정정 기록

최종 보고서 `codex_review_dem_unloading_prereg_rereview_20261012.md:259–350`을 읽고 직접 소스와 다시 대조했다. §5의 PRE_SETUP/POST_SETUP 명령, 정수 첨자 4열, custom의 `%d` ID + 4개 `%.17g`, local의 7개 `%.17g`, 첫 run 전에 compute 선언, 마지막 uncompute 순서가 일치한다. `write_dump`는 dump 자체 초기화/출력 경로이며 force/setup을 호출하지 않는다. `write_restart`는 system init·pre_exchange·재분배가 있으므로 무전처리 raw 복사로 표현하지 않는 보고서의 제한도 맞다. 실제 실행 성공으로 승격하지 않았다.

PowerShell 정수 연산 재검산: `3,600,000+2,000=3,602,000`; `3,600,000+60,000=3,660,000`; `3,602,000+60,000=3,662,000`; `3,660,000+50,000=3,710,000`; S0′±5,000은 `[3,645,000,3,655,000]`; S0″±5,000은 `[3,695,000,3,705,000]`. `3,650,000 % 10,000=0`과 `3,660,000 % 50,000=10,000`을 별도로 계산했다. contact cadence 지적은 철회했으며 원본 source/evidence는 변경하지 않았다. 보고서의 종단 restart **자동 생성 없음** 단정은 output scheduling 소스를 추가 확인하거나 위의 실제 파일 확인 문장으로 좁히면 된다.
