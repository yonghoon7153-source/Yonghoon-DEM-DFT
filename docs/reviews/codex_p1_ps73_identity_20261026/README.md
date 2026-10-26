# P1 7:3 원본 여섯 파일 신원 확인 접수

**사용자가 전달한 2026-10-26 20:14:00–20:14:02 KST 관찰에서 원본 여섯 파일의 경로·크기·SHA256이 기존 기록과 모두 일치했다.** ibb-master의 yonghoon 사용자가 읽은 결과이며, 파일별 stat/sha256sum 반환값 12개와 전체 identity_read_rc가 모두 0이다. Codex가 ibb에 접속하거나 명령을 실행한 결과는 아니다.

다음은 기존 성공 이력·문법 자료와 지정 실행 파일, 실제 작업 폴더가 수용된 키트에 맞게 준비되어 있는지 확인하는 단계다. 준비 조건이 갖춰지고 실행이 허용된 뒤 첫 실제 시험은 7:3 RJ 복원이며, 이번에 실행하거나 통과한 것은 아니다.

## 무엇을 근거로 확인했나

[사용자 전달 출력 전사본](user-relayed-output.txt)과 [기계 판독 접수 기록](identity-receipt.json)을 함께 보존한다. 전사본은 채팅의 결과 블록을 수동으로 옮겼고 명령·프롬프트는 제외했다. 원본 터미널 파일의 바이트 사본이라고 주장하지 않는다. 아래 해시는 전사본 자체의 신원이다.

전사본 SHA256: `a13f547cf1274c956b781965acde105ea750aa484873d2035fb0ae27a6387f23`.

사용자가 알려 준 원본 게시 경로는 docs/reviews/p1_ps73_input_identity_20261026/ibb_identity_screen.txt이다. 20:22 KST 원격 source `446b5bf543c39120e0003f3a7e2272264d1e97a8` 확인에서는 이 경로가 아직 없었다. 원본 게시 확인은 대기 중이지만 전달된 수치의 비교는 완료했다. 이후 원본이 게시되면 출처를 추가 대조하면 된다. 이 기록은 다른 prefix를 사용하여 예정된 원본 경로를 선점하지 않는다.

## 과거 기준과 이번 관찰

기준은 수용된 ULPRI `4c29705fa1c4ba94737a858b206fa4f4c5bb2bde`의 [params](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/unload_params.json), [10월 9일 ibb 원문](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/reviews/dem_unloading_ps45_precheck1_20261009/ibb_precheck1_screen.txt#L163-L170), [r8 로그·덱 압축본](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz)이다. 앞 네 파일은 params/과거 ibb 원문의 값이고 로그·덱은 보존된 압축본의 값이다. 덱 해시는 params head_source에도 있다.

| 입력 | 바이트 수 | 이번 관찰 SHA256 = 과거 기준 |
|---|---:|---|
| ckpt | 81154383 | `0aa6e41a2330ae7825a715b8d98da6b708c37cb4093d3ab0f8fe2c2653ca3730` |
| atom | 21430748 | `2da106f8470a60c7d3b85894025007d6a5decdffb249b22e0a2ce67d08bbdd9e` |
| contact | 149687008 | `53ae293b4586d091dfca58ab430c174f36b641dcd24678eb10d10fc3f416e65c` |
| mesh | 349 | `c25296a6d4d6b185be3c1c0ff98543dbfdb710c281403111c7fae2b9bde2b820` |
| orig_log | 127049 | `35e28690eb9b45c989d7526205a1b168b23041cd1cce6afb12a020deb5096c49` |
| last_deck | 5916 | `097658aa640f798b53da4c40a9d101632b8faaee6f80f4d1d2667591eef8d9cd` |

여섯 전체 경로와 각 반환값은 JSON 및 전사본에 있다. 과거 예상 해시만 있었던 상태에서 **이번 사용자 관찰 구간의 원본 신원 일치**가 추가되었다. 지속적인 파일 불변성이나 관찰 이후 상태를 보증하지 않는다. 이전 인계 문서의 당시 미확인 기록은 고치지 않고 이 후속 기록으로 연결한다.

## 남은 준비 조건 — 실행 지시 아님

1. 실제 작업 checkout과 전체 봉인 키트가 수용된 4c 구현에 해당하는지 구분한다. T12 종결 가지나 가변 Claude 가지 이름만으로 4c 구현 반입을 증명하지 않는다.
2. 이번 결과는 원본 경로의 파일이다. 실제 작업 폴더의 ps_7_3_r45/in/ 여섯 파일이 준비됐는지, 이전 시도 디렉터리가 있는지는 별개다. 이번에 복사하지 않았다. 기존 inputs_check는 네 해시와 로그·덱 존재 여부를 검사하며 여섯 해시 검사는 아니다.
3. 지정 LMP의 현재 신원과 MPI/NP6, 기존 성공 이력·문법 run 및 그에 맞는 봉인 키트가 남아 있는지 확인할 조건이 남는다. 과거 LMP SHA256은 `ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f`다. 이미 보유한 성공 이력 hist_20261014_094731과 문법 gram_20261015_030225 또는 gram_20261015_122956을 구분한다. 기존 실패 기록은 보존한다. 문법 prerequisite는 원래 실행 결과를 봉인 reader로 다시 읽고 19개 조건을 확인하므로 verdict JSON만으로 충분하지 않다. 원래 경로 및 matching kit가 중요하며 새 fixture 실행이 필요하다고 미리 가정하지 않는다.
4. 준비·실행 범위가 허용되면 기존 preflight를 사용한다. 이는 stat/hash 관찰과 다른 단계이며 이번에 수행하지 않았다. 실제 복원 판독에는 성공 이력 자료도 필요하다.
5. 실제 7:3 순서는 RJ의 G0 → Ut0 → R → UN → UK다. 기술 실패는 후속 단계를 멈춘다. 생산 복원 RESTORED와 정상 RJ 완료 영수증, grammar_prereq=PASS가 있어야 뒤의 UB/UT/UC 등으로 진행할 수 있다. 파일 신원 일치나 작은 fixture PASS가 이를 대신하지 않는다.

세부 근거: [수용된 README](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/README.md), [기존 runner preflight](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/run_unload.sh#L104-L137), [복원·문법 판독](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/data/ps45_unload_20261009/ul_reader.py#L1395-L1445), [등록된 순서와 비준](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/4c29705fa1c4ba94737a858b206fa4f4c5bb2bde/docs/reviews/dem_unloading_ps45_prereg_20261009.md).

기존 P1 체크포인트/S0 지정은 유지하지만 생산 복원 자격을 새로 부여하지 않는다. ULPRI-01/02와 T12R-01의 한정된 CLOSED 상태도 유지하며 재검토나 완료된 검사 반복을 요청하지 않는다. P2 R-a/S0·물리 T12·Q7–Q9는 별도 조건이고 물리 T12는 NOT_RUN이다. 이번에는 CI 변경, Claude 중심 가지 반입, 파일 복사, 새 계산·WSL·물리 실행을 하지 않았다.
