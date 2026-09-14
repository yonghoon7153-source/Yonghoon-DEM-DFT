# COMSOL 6.3 제안 A — 초기 시간상한 4회 전달본

승인된 5초 계산 네 번만 수행했다. 전체 물리 요소 300개, 각 입자40/80요소, 초기상한 .001/.0005초의 네 조합이다. 0.1초부터 상한은 .1초다. 모든 계산은0.1C·sigma=1e-20 S/m, 동일187개 요청 시각·241개 FE 공간 표본/전극과 기존물성을 사용했다.

시간상한 반감 차이는 전압·표면 x 기준 이내다. 반경40→80 비교는 같은 .001/.0005초 상한에서 각각2.506696517/2.505981087 mV로1 mV 기준을 넘었다. 전체수렴과입자80요소수렴은미완이다. 추가300/160은계획서의제안만있고미실행이다.600/80·전체프로토콜·12시간휴지·기준값외sigma·sweep도미실행이다.

## 먼저 읽을 자료

- [결과와 동시 전압 분해](TIME_CAP_RESULTS_KO.md)
- [수정한 NEXT_RUN_PLAN](../NEXT_RUN_PLAN.md)
- [독립 수치 검토](results/independent_review.md)
- [실제 step](native_steps_summary.json), [소스 SHA](source_configs.json), [설정·현지 보존 확인](final_checks.json)
- [비교 그림](figures/time_caps_comparison.png), [그림 PDF](figures/time_caps_comparison.pdf)
- [이전 ZIP 정체성과 재검증 범위](zip_identity/README_ZIP_IDENTITY_KO.md)

전압 비교는 공통 native 저장 시각이며 시간 보간이 없다. 표면 값은 해당 시각의 공통 좌표에서 FE 공간 보간으로 평가했다. 최대값은 지정 표본에 한정된다. 전해질 양수 확인은 후처리 검사이며 실시간 음수 StopCondition은 구현되지 않았다. OCP입력·고체표면조성의 기존 실시간 보호와 extrap=none을 유지했다. 기존 failed·INCOMPLETE_RANGE_STOP도 그대로다.

## 파일 구성과 재현

- outputs/time_caps/: 계약·소스 차이·비교 CSV·분해·그림·실제 step와 전체 Time/Variables getter·독립 검토·ZIP 대응표
- outputs/NEXT_RUN_PLAN.md: 이번 결과를 반영한 계획
- outputs/comsol63/time_caps/: 네 실제 제출 소스
- outputs/comsol63/.comsol-jobs/<job>/: request/status·staged/generated Java·compile/batch/console/worker 로그·저장 MPH
- outputs/model_audit/<job>/: 각14개 원시 CSV, 모델 XML, audit_files.json
- work/time_caps/: 준비·분석·실제step·그림·ZIP 재검증·보고서·패키지 코드와 합성 회귀 테스트
- 이전 Axes300R40/R80 소스와 decoder: 새 소스의 원본 및 데이터 추출 재현 근거

Python 분석·검증 코드는 COMSOL을 실행하지 않는다. 기본 분석·검증은 Python 표준 라이브러리를 사용하며 그림만 Matplotlib/NumPy가 필요하다. COMSOL6.3의 새 실행 또는 MPH 재계산은 별도 사용자 선택이 필요하다. 런타임·설치·캐시·실험 fixture 복사본은 포함하지 않았다.

전달 ZIP을 해제한 루트에서 다음 명령으로 기존333개 보관 바이트를 재검증할 수 있다.

```text
python work/time_caps/zip_identity_verify.py --root .
```

필요 입력은 동봉한 현지 PREFLIGHT ZIP·외부manifest·SHA영수증·outputs/mesh_axes/preserved_before.json 네 개다. ZIP 내부330개와 별도3개를 검증한다. 해당PC의현재파일상태나사용자의다른097d4b65…c3b51포장본을검증하는명령은아니다. 두번째raw ZIP은확보하지못해재포장여부가미확인이다. 현지 현재468개 바이트보존 확인과 전달된과거333개 보관바이트검증을 구분한다.

현지PREFLIGHT ZIP은46,999,470 bytes/SHA3bc4e4e4d14ff815a710998ac3e538712343933cef6d460eb5845f21e7235018이다. 동봉한이ZIP과바탕화면에서발견한압축해제본의manifest·331개payload가같음을확인했으나,그압축해제본이사용자보고47,006,147 bytes/SHA097d4b65…c3b51에서나왔다는출처는미확인이다.

## 무결성

package_manifest.json은 자신을 제외한 모든 ZIP 항목의 크기·SHA를 기록한다. 패키저는 최종 ZIP의 CRC 및 모든 항목의 SHA·크기를 대조하고, 최종 ZIP에서 네 역사 입력만 읽어 별도 폴더에서333개를 다시 검증한다. 최종 ZIP 자신의 SHA와 검사 영수증은 자기참조를 피하도록 ZIP 밖에 둔다. 파일 무결성과 과학적 수렴·실험 정확도는 다른 판정이다.
