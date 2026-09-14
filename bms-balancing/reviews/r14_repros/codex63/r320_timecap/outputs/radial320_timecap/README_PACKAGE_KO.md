# COMSOL 6.3 — 300/320H0125 단일 5초 전달본

새 Caps300R320H0125 한 번만 수행했고 기존 Caps300R320H0250은 재사용했다. 물리300·입자320/320을 유지하고 초기 cap만 .00025초에서 .000125초로 반감했다. .1초 이후 상한은 .1초로 같다. 187개 요청 시각·전극별241좌표·물성·OCP·Li·초기화·허용오차·scale·보호도 같다.

판정은 이번 표본의 초기 시간상한 민감도에 한정한다. .1초 이후 시간 정확도·참값 오차·전체 수렴을 입증하지 않으며 장시간 보류를 유지한다. 이전 반경 차이 .6170341087208 mV에 대한 비율은 크기 비교이고 수렴 차수가 아니다.

- [결과·구간별 최대·동시 성분·크기 비율](TIMECAP320_RESULTS_KO.md)
- [분석·CSV 목록](results/analysis.json), [독립 원시 검토](results/independent_review.md)
- [실제 설정·step·새 MPH SHA·보존 검사](final_checks.json), [native step](native_steps_summary.json)
- [독립 소스 감사](INDEPENDENT_SOURCE_REVIEW.md), [독립 native 감사](INDEPENDENT_NATIVE_AUDIT.md)
- [중복 검사](DUPLICATE_CHECK_BEFORE.json), [최종 job 보존 검사](FINAL_PROVENANCE_CHECK.json), [확인 수준](PROVENANCE_LEVELS.json)
- [수정 NEXT_RUN_PLAN](../NEXT_RUN_PLAN.md), [그림 PNG](figures/timecap320_comparison.png), [그림 PDF](figures/timecap320_comparison.pdf)

## 구성과 재현

새 H0125의 Java·staged/generated Java·request/status·전체 로그·CSV·저장 MPH를 포함한다. 기준 H0250도 소스·CSV·로그·실제 설정·step을 포함하며 기준 MPH는 이전에 전달되어 중복 전송하지 않는다. 현재 시간반감 pair의 원시 비교 자료가 포함되어 있다.

아래 명령은 Python 표준 라이브러리를 이용한 저장 자료 분석이며 COMSOL을 호출하지 않는다. 분석 결과를 같은 경로에 쓰므로 별도 작업 사본에서 실행한다.

```text
python work/radial320_timecap/analyze_results.py
python work/radial320_timecap/raw_recheck.py
python work/radial320_timecap/extract_steps.py
python work/radial320_timecap/independent_native_review.py
python work/time_caps/zip_identity_verify.py --root .
```

그림은 Matplotlib/NumPy를 사용한다. 캐시·설치 의존성·합성 시험 fixture는 동봉하지 않는다. source preparation/preservation/final_checks는 현지 과거 전체 목록을 요구하므로 이 ZIP만으로 현지 목록 전부를 재검증할 수 있다는 뜻은 아니다.

이전 반경 차이의 analysis·보고서·manifest와 R160H0250의 양쪽 경계 CSV 2개를 크기 참조 재계산용으로 포함한다. 기존 R320 경계 CSV와 함께 사용한다. 이전 단계 전체 원시 입력을 동봉한 것은 아니다. 이전 반경 비교의 full payload는 이미 수신·검증된 COMSOL63_RADIAL320_HANDOFF.zip에 있다.

이전 RADIAL320 생성본은429953577bytes·SHA89703ec4a1e47985ddefa9b0270cd317d0356cbe2ec7d4efe31f879703702aa0로 보존했다. 이번 사용자는147payload·manifest·CRC·역사적333개와 원시 비교 수치를 확인했다. 이번 메시지가 outer ZIP 크기/SHA를 새로 명시한 것은 아니므로 두 확인 수준을 구분한다. 이전 영수증은 당시 기록 그대로 보존했다. 현지 보존 목록 전체의 외부 검증으로 확대하지 않는다. 이전 TIME_CAPS raw ZIP 차이 원인은 미확인이다.

과거333개 보관 바이트의 독립 재검증을 위해 PREFLIGHT 원본 ZIP·외부 manifest·SHA 영수증·333 ledger·검증코드를 포함한다. 최종 새 ZIP에서 이 입력을 꺼내333개 검사를 수행한다. 기존 범위 실패 job의 request/status/log도 포함한다. 기존 failed/INCOMPLETE_RANGE_STOP을 보존하며 다른 solver 실패를 같은 분류로 자동 처리하지 않는다.

OCP 외삽 금지·OCP입력/고체표면 StopCondition은 그대로다. 전해질 양수는 후처리 검사이며 실시간 중단으로 표시하지 않는다. 이번 한 번 이후 추가 시간반감·메시 세분·전체 프로토콜·12시간 휴지·유한 sigma·sweep은 실행하지 않는다.

## ZIP 식별

이 폴더의 package_manifest.json은 자기 자신을 제외한 새 payload의 경로·크기·SHA를 기록한다. 동봉된 이전 단계 manifest는 그 당시 원본 ZIP의 기록이다. 최종 ZIP의 모든 크기/SHA·CRC를 검사하고, ZIP 옆 영수증에 현지 생성본의 raw 크기/SHA를 기록한다. 새 수신본의 확인은 별도다.
