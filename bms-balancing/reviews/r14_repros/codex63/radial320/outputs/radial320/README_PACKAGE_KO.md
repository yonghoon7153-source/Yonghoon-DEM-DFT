# COMSOL 6.3 — 300/320H0250 단일 5초 전달본

새 Caps300R320H0250 한 번만 수행했고 기존 Caps300R160H0250은 재사용했다. 물리300은 유지하고 입자 Nel160/160→320/320만 바꿨다. 초기 cap .00025초(t<.1초)·이후.1초,187요청시각·전극별241좌표·물성·초기 재고·OCP·solver·보호 설정은 같다. 기준과 같은 cap이 R320의 시간정확도를 증명하지는 않는다. 판정은 이번 비교 표본의 세분 민감도 범위에 한정하며 전체 수렴 미완·장시간 보류를 유지한다.

- [결과·구간별 최대·동시 성분 분해](RADIAL320_RESULTS_KO.md)
- [정확한 비교와 CSV 목록](results/analysis.json), [독립 원시 CSV 검토](results/independent_review.md)
- [실제 설정·step·MPH SHA·보존 검사](final_checks.json), [native step 요약](native_steps_summary.json)
- [독립 소스 감사](INDEPENDENT_SOURCE_REVIEW.md), [독립 native 감사](INDEPENDENT_NATIVE_AUDIT.md)
- [사전 중복 확인](DUPLICATE_CHECK_BEFORE.json), [출처·확인 수준](PROVENANCE_LEVELS.json)
- [수정 계획](../NEXT_RUN_PLAN.md), [그림 PNG](figures/radial320_comparison.png), [그림 PDF](figures/radial320_comparison.pdf)

## 구성·재현 범위

새 R320의 Java·staged/generated Java·request/status·전체 로그·CSV14개·저장 MPH를 포함한다. 기준 R160H0250도 소스·CSV·로그·설정·step을 포함하며 기준 MPH는 중복 전송하지 않는다. 과거 단계 전체 파일이나 모든 과거 MPH를 동봉한 것은 아니다.

아래 명령은 저장값 분석·확인만 수행하며 COMSOL을 호출하지 않는다. 분석 출력을 같은 경로에 쓰므로 원본을 보관하려면 작업 사본에서 실행한다.

```text
python work/radial320/analyze_results.py
python work/radial320/raw_recheck.py
python work/radial320/extract_steps.py
python work/radial320/independent_native_review.py
python work/time_caps/zip_identity_verify.py --root .
```

분석은 Python 표준 라이브러리, 그림은 Matplotlib/NumPy를 사용한다. 캐시·설치 의존성·합성 테스트 fixture는 제외했다. source preparation 및 현지 preservation/final_checks는 현지 전체867개를 요구하므로 이 ZIP만으로 그 전체 현지 검사를 재현할 수 있다는 뜻은 아니다. 현재 pair의 원시 비교 자료는 동봉했다.

이전 R160_TIMECAP 원본 ZIP은307305998bytes·SHA481ce9ebb1455de18ffcc35554d34b8a5fceb5c8cea3018938a200fadd920bdc로 보존했다. 그 rawZIP은 이전에 전달됐으므로 중복 전송하지 않고 원본manifest·영수증 및 이번 사용자 수신확인을 구분해 기록했다. 기존 영수증의 당시 수신미확인 기록을 뒤집어 쓰지 않았다. 사용자의267payload/manifest/CRC 수신검증은 현지 현재867파일의 외부검증과 다르다. 이전 TIME_CAPS 두 rawZIP차이 원인은 여전히 미확인이다.

과거333개 보관 바이트를 재검증할 수 있도록 PREFLIGHT 원본 ZIP·외부manifest·SHA영수증·333ledger와 검증코드를 포함한다. 새 최종ZIP의 이 입력들에서333개 바이트 검증을 수행한다. 기존 OCP범위 실패 job의 request/status/log와 기존 분류 근거도 포함한다. 다른 solver 실패를 INCOMPLETE_RANGE_STOP으로 자동 분류하지 않는다.

OCP 외삽 금지·기존 OCP입력/고체표면 StopCondition을 유지한다. 전해질 양수는 후처리 검사다. 이번 한 번 외 추가 시간반감·더 세밀한 메시·전체 프로토콜·12시간 휴지·유한 sigma·sweep은 실행하지 않았다.

## 포장 식별

이 폴더의 package_manifest.json은 자기 자신을 제외한 새 전달 payload의 경로·크기·SHA를 기록한다. 포함된 이전 단계 manifest는 그 당시 원본 ZIP의 기록이므로 현재 전달 전체의 manifest로 취급하지 않는다. 생성 후 모든 payload 크기/SHA·CRC를 검증한다. ZIP 옆 영수증은 이번 현지 생성본의 raw 크기/SHA를 식별하며 아직 관측하지 않은 새 수신본으로 표현하지 않는다.
