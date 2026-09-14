# COMSOL 6.3 R160 초기 시간상한 반감 전달본

새 Caps300R160H0250의 5초 계산 한 번만 수행했다. 기존 Caps300R160H0500과 초기 cap만 .0005→.00025초로 비교했다. 관측 최대 전압 차 .002175461073 mV @.005초, 표면 x차4.3003216e-8 @.002초·양극121 µm다. 요청107/187시각과 전체 정확 공통282/363시각(0–1/0–5초)의 기준을 모두 충족한다. 이 시간 민감도는 과거 반경 최대1.248218 mV의 약.174%이며 기존 전체 수렴 미완·장시간 보류를 유지한다.

- [한국어 결과](TIMECAP160_RESULTS_KO.md), [정확한 분석 및 CSV 목록](results/analysis.json)
- [독립 원시 CSV 검토](results/independent_review.md), [독립 native 감사](INDEPENDENT_NATIVE_AUDIT.md)
- [실제 step](native_steps_summary.json), [소스 SHA](source_configs.json), [최종 설정·보존 검사](final_checks.json)
- [메타데이터 정정](corrections/CORRECTION_LOG_KO.md), [전후 SHA](corrections/before_after_sha256.json)
- [포장본 식별·확인 수준](archive_identity.json), [수정 계획](../NEXT_RUN_PLAN.md)
- [그림 PNG](figures/timecap160_comparison.png), [그림 PDF](figures/timecap160_comparison.pdf)

## 동봉 범위

새 H0250 소스·staged/generated Java·request/status·전체 로그·원시CSV14개·저장 MPH를 포함한다. 기존 R160H0500·R80H0500·R40H0500은 이전 결과의 재사용 증거로서 소스·로그·CSV를 동봉하며 이번에 재실행하지 않았다. 기존 MPH는 중복 동봉하지 않는다. R40은 정정된 과거 radial160 분석의 재현용이며 이번 시간반감 주 비교군에 넣지 않았다.

원본 RADIAL160 ZIP과 원본 영수증·manifest의 역할을 구분한다. 원래 ZIP은 SHA39ded591a29568d58b57791bf68147292a9cef06660de40b1c5e45ed16b434bc,226198096bytes로 현지 생성/사용자 수신 확인이 일치한다. 그 rawZIP은 이미 전달된 파일이므로 이번에 중복 동봉하지 않는다. 원본 archive manifest·영수증은 불변 그대로 포함하고, 현재 교정된 contract/analysis와 before백업·전후 ledger·current_metadata_manifest를 따로 포함한다. 원본 package_manifest는 당시 원래 ZIP 바이트를 설명하므로 현재 교정된 파일에 그대로 적용하면 안 된다. 이번 전달물 전체의 명세는 이 폴더의 새 package_manifest.json이다.

역사적333 보관 바이트 검증을 위해 이전 PREFLIGHT ZIP·외부manifest·SHA영수증·이전333ledger도 동봉했다. 이는 현지 현재663개 또는 이번 현지758개 전체의 외부 검증이 아니다. 원본 RADIAL160의160payload/manifest/역사333 외부 검증은 사용자 확인으로 기록했다. 이전 TIME_CAPS 두 rawZIP 차이 원인은 여전히 미확인이다.

## 읽기·재계산

다음 명령은 원시 저장값을 읽어 분석과 step 기록을 다시 만들며 COMSOL을 호출하지 않는다. 새 출력은 동일 경로에 쓰므로 보관 원본을 유지하려면 작업 사본에서 실행한다.

```text
python work/radial160_timecap/analyze_results.py
python work/radial160_timecap/raw_recheck.py
python work/radial160_timecap/extract_steps.py
python work/radial160_timecap/independent_native_review.py
python work/time_caps/zip_identity_verify.py --root .
```

새 분석은 Python 표준 라이브러리로 실행한다. 그림 재생성은 Matplotlib/NumPy가 필요하다. source preparation/현지 preservation/final_checks는 현지 전체파일을 요구하므로 이 전달본만으로 현지758파일 검사를 재현할 수 있다고 주장하지 않는다. 옛 TIME_CAPS rawZIP 전체 식별 재검증에는 그 rawZIP이 별도로 필요하다. 테스트 fixture·캐시·설치 의존성은 제외했다.

OCP 외삽 금지·고체표면/OCP입력 StopCondition·기존 failed/INCOMPLETE_RANGE_STOP을 보존했다. 전해질 양수는 후처리 검사다. 새 한 번 외에320·600/80·추가 시간반감·전체 프로토콜·12시간 휴지·유한 sigma·sweep은 실행하지 않았다.

새 ZIP은 생성 뒤 CRC·모든 payload 크기/SHA를 직접 검증하고 최종ZIP의 역사 입력에서333개 보관 바이트를 다시 검증한다. ZIP 옆 영수증은 이 PC에서 생성한 rawZIP의 크기/SHA를 식별하며 아직 확인하지 않은 새 수신본의 식별로 표현하지 않는다.
