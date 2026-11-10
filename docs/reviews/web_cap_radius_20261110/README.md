# WEB07 — brittle cap 반경 정규화 후보

**cap 투명도 계산을 실제 geometry 반경으로 정규화했다. 작성측 작은 합성 시험 9/9이며, 독립 판정·실제 화면 검증·배포 GO는 없다. 전체 HOLD.**

바탕 `0c56deba6f2fb824996d770163a19c8e7dbd8abe` 위 `codex/web-cap-radius-1110` 후보다. 고정 구본 `c571a27119ace92ca34d3d6f2b61135219a3f1b4`의 viewer는 이 바탕의 viewer와 Git blob·SHA256이 같다. 기존 범위표 핀 `f4647f2b7c218a6df7def3292c092273f9d4e35f`에서도 같은 원본이다. B 반입·원장 처분은 아직 없다.

상태: **0 = 후보 구현·작성측 합성 확인 완료**, **1 = 기존 기능/경계 보존**, **2 = 독립 판정 미수령**, **3 = 실제 앱·현장·배포 미수행/미승인**.

| 범위 | 상태 | 근거 | 판정·다음 |
|---|---:|---|---|
| WEB07 cap alpha | 0 | `webapp/static/js/viewer3d.js`의 `applyViewMode` → `brittle_surface` → `buildCap` | 실제 반경 `capRadius=r*1.005`를 geometry와 무차원 y 계산에 함께 사용. 원 반례는 아래 합성 범위에서 차단. |
| AM-only cap | 1 | 같은 source의 `renderAmOnlyContactCaps` geometry 부분 | 기존 `/R0`와 `0.3+0.7*t` 계산·RGB·geometry는 유지. 비교 주석 한 곳만 “구본 Brittle”로 명확히 함. |
| WEB02 | 1 | 같은 source의 `group particles by type` 구간 | 이미 구현된 unknown 보존·색 선택을 그대로 둠. 새 WEB02 수정/종결 주장이 아님. |
| 독립 검토 | 2 | `verification_summary.json`의 `independent_review` | NOT_RECEIVED. 작성측 시험을 독립 GO로 바꾸지 않음. |
| 실제 화면·앱·물리 | 3 | 동일 summary의 실행 경계 | browser/실제 Three.js/실제 payload/engine 실행 없음. 픽셀·WebGL·물리 결과 인증 아님. |
| 봉인/다른 경계 | 3 | `scope_provenance.json`의 `deferred_boundary_index` | WEB04/05/08/10/PRED01은 제안만. CODE_FILES32·Rint·운영 봉인·원장 수정 없음. |

## 1. 문제와 최소 변경

구본은 geometry y 좌표가 `R=r*1.005`의 길이인데 무차원 `cos(halfAngle)`과 바로 뺐다. 따라서 같은 구면 각도라도 입자 반경에 따라 alpha가 달랐다. 후보는 y를 실제 geometry R로 나눈 뒤 기존 clamp·제곱 fade를 그대로 적용한다. 입자 r만으로 나누지 않는다.

half angle π/3의 손계산 오라클은 무차원 y=1/0.5/0.75에서 alpha=1/0/0.25다. 반경 0.5/1/2는 **합성 fixture 선택**이며 실제 입경·물성 선택이 아니다. Float32 위치/색 저장의 절대 대조 오차는 `5e-6`이다.

`capRadius` 정의·geometry 인자·y 정규화 외의 실행 문장은 바꾸지 않았다. AM-only의 기존 비교 주석이 수정 뒤 사실과 달라지는 문제는 “구본” 두 글자로 한정했다. 해당 블록의 runtime 계산은 바뀌지 않았다. 시험도 원문 전체 주석 제거 같은 넓은 완화 없이, baseline에 정확히 한 번 있는 그 문구의 한 치환만 추가로 허용한다.

## 2. 시험 먼저 순서와 수의 의미

| 단계 | source / test SHA 앞부분 | 방법·결과 | 의미 |
|---|---|---|---|
| 준비 중단 | 구본 `015677ba…` / 시험 `17964bb9…` | Python recorder의 Windows subprocess audit 인자 표현 비교에서 Node 시작 전 중단. 시험 0. | argv의 Windows 문자열 표현과 명시 executable을 고쳐 새 이름으로 재시도. 코드 반례 red로 세지 않음. |
| 최초 실제 red | 구본 `015677ba…` / 시험 `17964bb9…` | 9개 중 assertion 실패 5, 비-assertion 오류 0, rc1 | viewer 구현을 쓰기 전에 원 산술 반례 확인. |
| 최초 후보 green | 중간 후보 `df4dfb7e…` / 같은 시험 | 9/9, rc0 | geometry 반경을 공통화하고 y 정규화한 첫 후보. |
| 최초 제거 대조 | 복사본 `70b769e9…` / 같은 시험 | 정규화만 제거 → assertion 실패 5, 오류 0, rc1 | 원본·후보는 보존. |
| 최종 시험으로 구본 red | 구본 `015677ba…` / 최종 시험 `ffc592cb…` | 같은 9개 중 assertion 실패 5, 오류 0, rc1 | AM-only의 비교 주석 한 치환을 허용한 좁은 보존 기대값 수정 뒤, 원 계산 반례를 다시 확인. |
| 최종 green | 최종 후보 `97fe9cf8…` / 최종 시험 | 9/9, rc0 | 중간 후보와 최종 source 차이는 그 비교 주석 한 곳뿐. |
| 최종 제거 대조 | 복사본 `5166d4a4…` / 최종 시험 | 정규화만 제거 → assertion 실패 5, 오류 0, rc1 | 의미 있는 제거 대조 한 종류를 최종 바이트에서 반복 확인. |

고유 시험 메서드는 **9개**다. 앞뒤 반복·반경·각도·정점·시나리오 수를 합산해 새 시험 수로 만들지 않는다. 최종 주석/보존 기대값 조정은 최초 수정의 9/9를 지우지 않으며, 이를 처음부터 최종 시험으로 엄격하게 진행한 이력으로 바꾸지 않는다. 최초 기능 구현은 실제 구본 red 뒤에 작성했다.

9개는 AM/WEB02 보존, brittle pole/rim/interior, 기존 네 half angle의 기하 오라클, 명시한 합성 out-of-cap clamp, geometry/RGB/material/좌표 변환 호출, AM-only linear floor, WEB02 5개 그룹/색 시나리오다. out-of-cap 점은 실제 SphereGeometry가 만들었다는 주장이 아니다. `scripts/test_viewer_cap_radius.mjs`가 고정 구본에서 세 블록을 marker로 정확 추출한다. AM-only 한 비교 주석 예외 외에는 보존 대상 바이트가 같아야 한다.

## 3. 합성 실행 경계

실행 환경은 Windows Node `v24.22.1`이고 executable SHA256은 `a20f46c2084bb1775275d867370f8f785aec8c9677f8d8aeb5cae4caa2c08a81`다. 처음 준비 시에는 설치 메타만 확인했고, 위 실제 호출의 preload 보고서에서 runtime version을 받았다.

- 전체 viewer를 import하지 않았다. tiny THREE geometry stub·합성 fixture와 함께 `buildCap`, AM-only geometry 초기화, WEB02 그룹/색 선택 블록만 새 VM context에서 평가했다. 실제 Three.js 색공간·quaternion 렌더링·WebGL을 재현한 시험이 아니다.
- 원문 함수 호출까지 VM timeout 아래에 두고 require/process/fetch/DOM을 context에 주지 않았다. Node permission에는 고정 복사본 파일 네 개의 read만 허용하고 write/child/worker/addon/WASI 권한은 주지 않았다.
- Python audit는 선언한 Node child 한 번만 허용한다. 사전 Node preload는 열거한 builtin process/network 진입점을 막고 기록한다. 여섯 실제 Node 호출 모두 preload 설치 보고와 **해당 계측 진입점의 시도 0**을 관측했다. 첫 준비 중단에서는 Node가 시작되지 않았다.
- 이 제어는 완전한 OS sandbox 또는 모든 syscall 감사가 아니다. Python audit가 Node 자식 내부의 모든 호출을 보았다고 주장하지 않는다. 실제 앱·host·연구자료·engine 접근을 수행하지 않았다.
- 각 호출은 rc·전체 stdout/stderr·길이·SHA·시간·전후 원본 및 복사본 해시를 보존했다. 실제 호출 여섯 건의 입력 전후 해시는 모두 같다. source/test 해시와 scope는 `verification_summary.json`에 있고, local 경로가 포함된 raw 증거는 리포 밖에서만 보존한다.

기존 전체 앱 시험·전체 gate·실제 browser/engine 검증은 실행하지 않았다. 위 합성 변경의 승인/기능 경계를 벗어난 불필요한 회귀 반복을 하지 않는다.

## 4. 고정 신원과 증거

| 대상 | SHA256 |
|---|---|
| 구본 viewer | `015677ba072ab15d5b22c2f4b33767fe54dbd32ca00ab1ba590c2692e89e040e` |
| 최종 viewer | `97fe9cf8c36dcef68d421309f77a9b4372da7347c933313c06bc1acd4a91eee1` |
| 미실행 초기 시험 초안 | `8751a28a4e06441919e38ee72759896176fede16594d01230148d2452264d53d` |
| 최초 red/green 시험 | `17964bb9fb675b26005fdf8a3cfb7db011eb4092c27c20aa6c2b70940b3f2d45` |
| 최종 red/green 시험 | `ffc592cb6584a6f8fd526c5b7454ddf41357119dc0845dcbb1fa18754c68f488` |
| 최종 raw manifest v2 | `69ffebeddbefcdf6d2df4697ddecdd536d2951f803cd907575ce6e7a40659a3b` |

`final_raw_manifest_v2.json`은 자신을 뺀 **70파일**을 결속한다. 먼저 닫은 `final_raw_manifest.json`(당시 41파일, SHA256 `de6df07e0a687ea869d4d3472d61d57bc5464bc399e724512ebbee7a1f90e842`)도 한 항목으로 포함한다. 옛 manifest는 처음 검증 시점의 부분집합이며 현재 전체 집합이라고 주장하지 않는다. 최초 recorder 중단·중간 source/test·앞선 통과·변이·최종 주석 수정의 순서를 모두 보존했다.

이 문서는 작성측 후보 설명이다. 원장 변경·기존 한정 판정 재개방·물리 분석 변경·운영 봉인·배포·실행 GO를 수행하지 않았다. **전체 HOLD 유지.**
