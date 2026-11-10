# D-3/LIVE·R-a — 필수 채널·단계 경계 한정 검토

발송=1저자. 고정 핀은 11-10 하루 묶음 `PIN_MANIFEST.json`에 제공한다. 바탕은 T11 `ea5f22b6ae807dda3decf1928ec310d459996cb9`다. **독립 판정 PENDING·실제 관측/자격 NOT_RUN·전체 HOLD.**

| 이번에 닫으려는 것 | 닫지 않는 것 |
|---|---|
| 같은 source/frame·단위에 결속된 7채널의 완전성, 명시 raw 극성·반력/면적 산술, 고정 ID/type/radius/mass 재고, 원 T11 계획 재검증 | 실제 채널의 원천 진위·실제 단위/부호·물리 힘/토크 수지 재계산·hidden history 인증 |
| 기존 servo bridge 뒤 별도 완전 R-a 창·고정판·같은 이력을 요구하는 순수 진단, 끝 step에 결속된 boundary 후보 | 실제 reader/엔진 단계 전이·물리 R-a/S0·경계 파일/운영 봉인·P2 ULPR·T12·연구 GO |
| 누락 balance 구성요소를 NOT_COMPUTED로 보존하는 후보의 작은 보완 | 기존 첫 연결 708의 전체 독립 판정 또는 과거 닫힌 결함 재판정 |

**권고안 전제(Q-LIVE-1/2)**를 사용한다. q의 고정 합성 scalar 기준과 추가 채널의 명시 toy 한도를 실제 정량 등록값으로 바꾸지 않는다. 전달된 계획·모든 trace를 함께 바꾸지 못하게 하는 외부 인증 기능도 없다.

## 1. 독립 확인 질문

1. torque·회전 KE·힘 수지 구성요소·접촉 완전성의 결손이 scalar 성공만으로 채워지지 않는가? 비유한/형식 파손과 NOT_COMPUTED가 구분되는가?
2. 각 채널의 run/attempt/stage/step/sample/tick/window·source/unit이 정확하게 결속되는가? bool/int·float/int 동등 비교만으로 시점이 통과하지 않는가?
3. 입자 수가 같아도 ID/type/radius/mass가 바뀌면 거부되는가? raw 반력·부호·정규화 힘·면적/압력이 같은 sample에서 대조되는가?
4. 원 T11 plan/context가 직접 재검증되는가? 기존 bridge의 완전 예산·terminal 창·pending 제한과 기존 scalar profile을 약화시키지 않는가?
5. servo 성공과 R-a 완료가 분리되는가? R-a의 모든 행에 고정판·같은 이력이 요구되고, 결손 예산·잘못된 단계/시점·불충족 terminal 창에서 S0 후보가 나오지 않는가?
6. boundary 후보는 마지막 R-a step·재고·계획/trace/end-frame bytes에 결속되며 원 입력과 별도 사본인가? 이 digest를 실제 출처나 숨은 이력의 인증으로 주장하지 않는가?
7. 사전 구현 초안·stub red·초안 1실패·최소 보완·green·docstring 정정 후 final green이 구분되는가? 변이 7개는 이전 green 소스 대상이며 최종과 docstring 외 바이트/AST 동일하다는 대조를 실제 재실행으로 부풀리지 않았는가?

## 2. 증거·재현 범위

README·계약 초안·`verification_summary.json`, 원 source/test·초안·스텁·원 로그·변이·두 manifest와 최종 manifest를 함께 대조한다. 새 scratch의 작은 합성 입력으로만 재현한다. 기존 q/T0/T11 전체 suite나 실제 호스트/자료/engine·MPI/Slurm·Rint·전체 gate/CI는 이번 수행 범위가 아니다.

한정 수용돼도 실제 채널 수집, 정확한 경계 직렬화, 물리 S0/T12, 등록·빌드/재개·현장 자격·운영 봉인·최종 발사와 배포 GO는 별도로 남는다.
