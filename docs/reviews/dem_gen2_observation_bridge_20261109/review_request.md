# DEM 첫 연결 — 합성 관측·단계 진단 후보 독립 반박 요청

발송자는 **1저자**다. 이 문서는 구현 창이 작성한 요청이며 독립 수용 판정이 아니다. 고정 검토 핀은 이 문서와 함께 제공하는 ZIP의 `SOURCE_PIN.txt` 전체 SHA다. 원 바탕 B=`e91bd1c948362712def3f16b5b995027cc10011f`, 구현 직전 부모=`b492a206205958a7f5ab2a53d2e14e5403690f2e`다. 문서만인 선행 사본 둘과 새 코드 변경을 혼동하지 않는다.

## 1. 한정 대상

`scripts/dem_gen2_qualification.py`의 새 `observation_bridge`와 명시 문맥 dispatch, `scripts/test_dem_gen2_observation_bridge.py`만 새 구현/시험 대상이다. 기존 scalar guard의 **plain dict 규칙 입력** 결과·기존 자격 함수·생성기/gate 소스 보존도 대조한다. rules의 비내장 dict/mapping 입력은 명시 거부하도록 지원형식을 좁혔다. 임의 실행 가능한 Python 객체 전반의 보안 sandbox를 주장하지 않는다.

계약은 `43eb8a28c:docs/reviews/nonrint_approved_preparation_20261109/dem_quantitative_choices_and_t12_contract.md` §5 첫 연결과 §3 T11-04–07이다. 이번 구현은 그 중 **합성 trace→servo 종료의 relaxation 진단 후보**뿐이다. 실제 observer·엔진 stage 전이·R-a/S0 완료·정확 경계 serializer·P2 ULPR·등록 정량값·실제 T0/T5/T11/T12 수행은 없다.

## 2. 확인 질문

| 번호 | 독립 확인 요청 | 원하지 않는 확대 해석 |
|---|---|---|
| Q1 | run/bed/arm/attempt/definition/unit·stage/boundary·sample/step/integer tick·window 소속이 전체 trace에 결속되는가? stale·결손·교체·비정수/비유한을 버리거나 정렬해 통과시키지 않는가? | 합성 token 일치가 실제 원천·T0 극성·물리 dt·wall-clock freshness 인증은 아님 |
| Q2 | 최초 rolling 두 창 hit가 진단에 머물고, 완전 예산·끝의 고정 두 창·동일 trace pending suffix가 모두 있어야 후보인가? 예산 내 늦은 불안정·끝 창과 다른 pending 불안정을 거부하는가? | 유한 예산 통과를 영구 안정성·실제 침대 자격으로 바꾸지 않음 |
| Q3 | 문맥을 명시한 rules가 legacy scalar 경로로 후퇴하지 않는가? public 진입은 문맥 누락을 거부하고 비내장 dict/mapping은 명시적으로 거부하는가? | 과거 무문맥 scalar guard에 없던 신원 계약을 과거 결함으로 소급하지 않음 |
| Q4 | 합성 정상 trace와 기존 plain dict scalar 계약·22메서드·다른 자격 함수·생성기 소스가 보존되는가? 입력을 변조하지 않는가? | 과거 생성기18/18을 이번 재실행 또는 엔진/gate 자격으로 세지 않음 |
| Q5 | 모든 새 반환의 physical_ready/execution_go/transition_authorized/gate_write=false와 연구 결과0이 유지되는가? 파일 reader·process/network·gate 쓰기·실제 stage 작동이 추가되지 않았는가? | 기존 renderer 입구 HOLD·7 gate의 정적 보존이며 실제 gate 활성/배포 아님 |
| Q6 | 최종 동일 시험 바이트의 old assertion red→green, legacy 회귀, 내부 routing red와 변이 탐지가 실제 소스·시각·로그에 맞는가? 관측 수·메서드 수·반복을 중복 계상하지 않았는가? | 작성 창 내부 검토·변이는 독립 반박 판정이 아님; 전체 gate/CI는 미실행 |

## 3. 증거와 재현

`verification_summary.json`은 리포용 비결과 영수증이며, 전체 소스 SHA·최종 시험 수·실패/오류 수·미수행 범위를 기록한다. ZIP에는 원 red/green·내부 발견 전후·최종 같은 시험으로 original baseline 재대조·guard 변이·원본 source snapshot과 각 보고 JSON을 보존한다. `SNAPSHOT_MANIFEST.json`은 파일별 길이/SHA256/Git blob과 핀, 최상위 `SHA256SUMS`는 전체 파일 집합(자기 자신 제외)을 결속한다.

반박 창은 `REPRODUCE.md`에 따라 새 scratch에서 제공 소스의 합성 시험만 재현할 수 있다. 원 ZIP/운영 파일을 덮어쓰지 않는다. LHS·믹서 명령 문서는 이 DEM 검토 ZIP에서 실행할 대상이 아니다. 실제 자료·호스트·연구 엔진·MPI/Slurm·네트워크·Rint·전체 gate는 이 요청 밖이다.

## 4. 남는 상태

신규 후보의 외부 판정은 **PENDING**이다. 이전 G2PREP/ULPRI/T12R 좁은 수용은 그대로이며, 이번 범위에서 판정 가능한 새 결함이 있으면 그 반례·최소 영향·실행 환경을 분리해 회신한다. 실패 시 자동 재시도·예산 연장·값 접근 권한을 부여하지 않는다.

Q2 정량값·Q4 실제 자격은 미승인, 실제 live reader/경계/P2 연결과 통합·운영 봉인·실행 GO는 별도다. 원장 직접 수정0. **전체 HOLD 유지**.
