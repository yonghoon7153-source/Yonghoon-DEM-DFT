# S0 단계1·저장본 — 최종 핀 결과 전 대조표

## 1. 지위·신원

소스 = 64e4d213e8267bafaf3ae5af00a42996cefd3f33. SBE 한 침대, stage1, PROBE=1, CPU raster/census와 저장본 진단. 솔브·σ 없음. 결과0·HOLD. 앞 결과는 6bf70fe4a의 docs/data/rint2_s0_sbe_20261113/ADOPTION_CHECK.md이며 역사 개발 자료다. 이번에 해당 README/ADOPTION_CHECK 문장만 참조했고 원 결과JSON·로그·배열을 열지 않았다.

기준 = docs/reviews/rint2_s0_store_probe_20261112/README.md 결과 전 기대·문턱. 기존 T1–T3 숫자를 바꾸지 않는다. 새 계획·새 출력으로 받고 옛 등록 경로를 덮지 않는다. 감싸개는 원바이트, monitor의 Python 호출만 -I -B. 배포 블록/하네스/소스 지문은 block_manifest.json과 source_identities.json에 고정한다.

## 2. 기대와 실패

| 항목 | 결과 전 기대 | 수령 시 확인 | 실패·미확인 |
|---|---|---|---|
| E1 | 자식 rc0, 여섯 출력, 계획 선언SHA=실제SHA; import 도구 ADOPT_CANDIDATE | rss.log의 해당 자식 rc 출처·단일성, PIN/clean·코드7지문, 외부 목록/CRC/6파일해시 | DONE·셸rc0·후보표지만으로 채택 안 함; 빠짐/깨짐/모호하면 미완료 |
| E2 | 감싸개 호출1, instances117583 | 같은 bed/설정/입력 신원 먼저 대조; junction 행수와 연결 | 원인 조사·HOLD; 다르게 나왔다고 기대를 사후 수정하지 않음 |
| E3 | encode.ok true; built_written→hit; strict/registry_fp/object_is_new true | preloaded=[]·start.error=null·code_drift=[]·error=null·machine-id 읽기 성공 | 쓰기skip/fail/disabled/다른읽기/불일치/오류/빠짐은 저장본 채택 보류; 자동 재시도·⑥ 진행 없음 |
| E4 | 배열2와 의미 설정/문턱·입력은 역사 기준과 일치 | 아래 차이 허용 목록은 필드별 출처를 확인 | 허용 목록 밖 차이는 의미를 조사, 임의 통과 안 함 |

여섯 출력 = s0_stage1_kit_SBE_vgcf100.json, s0_junctions_kit_SBE_vgcf100.npz, s0_instances_kit_SBE_vgcf100.npz, cjunc_plan.json, cjunc_plan.sha256, payload_capture_kit_SBE_vgcf100.log. 여섯 파일 존재와 완결성·귀속을 구분한다. 배열은 수령 비준 범위에서 해시/꼴/정의 대조만 하고 수송값을 만들지 않는다.

E4 허용 후보는 코드 지문·git_head·tool_sha256, elapsed_s, 계획 source/tool_sha256과 그에 따른 plan.sha256, 새 출력 경로가 포함된 inputs.payload_argv_sha256이다. 범주만 맞으면 무조건 면제하는 것이 아니라 각각 고정 blob·실행 경로·새 계획 정준 바이트에 귀속되는지 대조한다. inputs.settings_sha256, 입력 사슬·단위·문턱·배열 의미의 변경은 면제하지 않는다. 11-13 역사 E4에서 argv 지문을 시간/코드와 별도로 다룬 한정을 이어받는다.

## 3. T1–T3와 실패 분기

| 항목 | 결과 전 문턱 | 해석 |
|---|---|---|
| T1 | seconds_write≤600 s, seconds_read≤300 s, read≤build×0.10 | 모두 유효한 유한 비음수 시간, build>0이어야 계산 가능. 초과/결측은 보고·R 계획 판단 대기 |
| T2 | VmHWM(저장본②–④)−VmRSS(①앞)≤4 GiB | hwm_reset 성공·해당 RSS/HWM 존재·단위 확인. 실패하면 증가량 미확인; 5초 표본으로 대체 안 함 |
| T3 | 저장본 파일≤2 GiB | 파일 귀속·길이·쓰기/읽기 영수증과 대조. 초과/결측은 보고·대기 |

문턱을 만족해도 실행 GO가 자동 발생하지 않는다. 초과·결측·OOM·중단은 완료/수용으로 세지 않는다. PROBE=0으로 자동 우회하지 않고 원본 보존 뒤 1저자에게 사유와 선택지를 올린다. S0 재기 저장본은 R 팔에 사용하지 않는다(문턱/열쇠가 다름). 새 S0 계획 채택과 기존 watcher 경로 연결은 별도 판단이다.

## 4. 수령 목록

새 묶음+외부SHA, meta, monitor rc/RSS, store_probe, 여섯 출력과 출력SHA. 사본을 빈 폴더에서 읽고 원본 보존. 원 ZIP·원 로그·현장 경로는 공개 리포에 넣지 않는다. 새 결과 등록 위치는 실제 수령 뒤 새 폴더로 결정한다. 이 문서가 실제 결과의 읽기나 실행 승인을 대신하지 않는다.
