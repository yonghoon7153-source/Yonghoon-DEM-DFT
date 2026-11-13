# 현행 Q11 v8 — 결과 전 소비 대조표

## 1. 판본

현재 블록 원문 MD5=b9d45d762f708d6f75ef0ebd6499add9, 옛 as-run v8 MD5=9182316778b3d01719a8f0219eb3601b. 같은 v8 이름으로 동일 판본이라 하지 않는다. 현재 하네스 MD5=4eb8a6c3ed2da1039e6b0988f63db906는 이번 초안에서도 원바이트다. 블록 외피만 최종 핀·사전 Git/GO 관문·새 출력·-I -B·실제 rc 보존으로 구성했다.

new=64e4d213e8267bafaf3ae5af00a42996cefd3f33의 step3_sigma.py, material=같은 핀의 se_material.py, old=11a794674의 step3_sigma.py. 각각 기대SHA는 source_identities.json. 새 폴더에 git show로 복사하고 하네스가 SHA와 실제 import 경로를 검사한다. 라이브 체크아웃에서 se_material을 불러오지 않는다. 측정 중 코드·환경 불변은 운영자 계약으로 남는다.

## 2. 고정 측정과 consume.adopt

| 항목 | 결과 전 조건 | 실패·미확인 |
|---|---|---|
| 설정 | backend=cupy, n_side298, seed20261112, logc1.0, main rtol1e-12, resolve1e-14, maxiter60000, short200 | 다른 설정은 이 등록 결과가 아님 |
| 동일성 | 5쌍: old-old, new-new, short old-new, main old-new, resolve old-new; 해 바이트/info/iters/LAST_BACKEND 모두 같음 | 한 쌍이라도 다름·빠짐이면 identical false·HOLD |
| 수렴 | main·resolve의 old/new 4회 모두 info0·finite=true | 같은 미수렴 결과라도 채택 불가 |
| backend | 총10회 모두 used=gpu, precond=jacobi, fallback_reason=null | CPU/다른전처리/폴백/누락이면 채택 불가 |
| 고정반복 | short 6회 각각 iters=200, info=200 | 조기종료·다른수·누락이면 채택 불가 |
| 출처 | old/new/material 기대SHA, se_material_from_scripts=true, forbid-dir 적재목록 없음(처음·끝) | 라이브모듈/지문차이/오류면 중단·채택 불가 |
| adopt | cupy AND identical AND converged AND backend_ok AND short_iters_ok AND source_ok | 하나라도 false/빠짐이면 수용하지 않음 |
| 완결 | harness_rc0, error=null, result 구조·환경·설정·핀·하네스 귀속 대조 | rc0만으로 adopt 주장 안 함; timeout/부분/오류는 미완료 |
| 성능 | C꼴 per-iteration이 더 빠를 것이라는 기존 기대 | 비율은 보고, 채택 술어에 몰래 새 문턱을 넣거나 실제 침대 가속으로 확대하지 않음 |

source_ok 하나만으로 모듈 신원 전체를 대체하지 않는다. 하네스 앞단 SHA/import 검사가 성공했고 최종 결과가 완결되어야 한다. true 칸만 읽는 것이 아니라 파일·설정·코드·실행 영수증을 함께 대조한다. 이 표는 임의로 편집된 JSON을 인증하는 새 소비자가 아니다.

## 3. 수령·다음

반환은 새 meta.txt, result.json, check.log와 하네스/세 복사 소스 신원이다. kgy 한 설치의 합성 SPD 결과이며 실제 킷·σ 없음. 다른 기계·다른seed·실제침대 자격으로 확대하지 않는다. 5400 s timeout은 현행 호출 보존이며 추가 kill-after 보장이나 장애 후 GPU 회수 인증은 아니다. 중단 뒤 잔존 프로세스 확인은 운영자 규약을 먼저 정한다.

서로 일치·수렴·backend·반복·출처·완결을 각각 수령 대조 → 1저자 수용 → S0 계획/환경/시간/자원/운영자 고정 → ⑥ 시도3 별도 GO. 한 검사만 성공한 채로 자동 다음 단계에 가지 않는다.
