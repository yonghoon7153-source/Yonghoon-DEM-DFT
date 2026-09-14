# COMSOL 6.3 — 후보 A 후기 시간상한 5초 단일 계산

Caps300R320LateCapA5s 한 번만 실행했다. 고정 기준 Caps300R320H0125 /18a00b03e38d4694b9ba30d88e7008f4는 재실행하지 않았다. 승인 cap은 `if(t<0.1[s],0.000125[s],if(t<1[s],0.005[s],0.025[s]))`다. 187개 요청 시각과 전극별241좌표, 물성·메시·초기화·허용오차·scale·보호는 유지했다.

- [결과 보고서](LATE_CAP_A_RESULTS_KO.md), [8개 비교창 분석](results/analysis.json), [독립 CSV 재계산](results/raw_arithmetic_recheck.json)
- [실제 step/설정](native_steps_summary.json), [구간별 분포 비교](accepted_interval_comparison.json), [최종 검사](final_checks.json)
- [독립 소스 감사](INDEPENDENT_SOURCE_REVIEW.md), [독립 native 감사](INDEPENDENT_NATIVE_AUDIT.md), [보존 수준](PROVENANCE_LEVELS.json)
- [수정 계획](../NEXT_RUN_PLAN.md), [변경 전 계획](NEXT_RUN_PLAN_before_late_cap_a.md)
- [비교 그림 PNG](figures/late_cap_a_comparison.png), [인쇄용 PDF](figures/late_cap_a_comparison.pdf)

사용자는 CPU 증가를 추가 승인했다. 도구는20코어 요청을 job생성 전에 거부했고, 기존30개 ID 불변 확인 뒤 최대16코어로 실제 새 job 한 개만 제출했다. 기준2코어 대비 병렬 반올림 가능성을 별도 제한으로 기록한다. 작업 중단 대기시간1200→1800초는 호스트 자원 설정이며 물리 시간은5초다.

## 자료와 재현

새 해의 원시 CSV·소스·SHA·staged/generated Java·request/status·전체 로그·MPH, 기준 해의 원시CSV·소스·로그·실제설정/step을 포함한다. 기준MPH와 이전632MB원본ZIP은 이미 전달됐으므로 중복 포함하지 않는다. 생성 당시 영수증 및 별도 수신확인은 원문 그대로 동봉한다.

별도 작업 사본에서 Python 표준 라이브러리로 다음 저장 자료 검사를 실행할 수 있다. COMSOL을 호출하지 않는다. 같은 경로의 분석 산출물에 기록하므로 보존 원본을 직접 작업 폴더로 사용하지 않는다.

```text
python work/late_cap_a/analyze_results.py
python work/late_cap_a/raw_recheck.py
python work/late_cap_a/extract_steps.py
python work/late_cap_a/independent_native_review.py
python work/time_caps/zip_identity_verify.py --root .
```

source preparation/preservation/final_checks/finalprovenance는 현지 전체 과거 목록을 요구한다. 이 ZIP이 현지1099개 목록 전체를 포함하거나 전체를 원격 재검증한다는 의미가 아니다. 그림 생성은Matplotlib/NumPy를 사용한다. 설치 캐시와합성fixture는 포함하지 않는다.

## 판정과 보존 한계

1mV·표면x1e-4의 판정은 이번 지정 및 정확 공통 저장 표본의 후기 시간상한 민감도에 한정한다. 1–5초에는 앞 구간의 상태 차이가 이어질 수 있어 후기 두 구간의 독립 효과를 분리했다고 쓰지 않는다. 병렬 실행 자원 변화도 포함되어 있다. 참값 오차·전체 수렴·장시간GO는 입증되지 않았다.

OCP 외삽 금지와 OCP입력/고체표면 StopCondition을 유지했다. **전해질 양수는 후처리 검사**다. 기존failed/INCOMPLETE_RANGE_STOP과 과거 원본을 보존하고 다른 실패를 범위중단으로 자동 분류하지 않는다. B, 추가시간반감·메시세분·전체프로토콜·12시간휴지·유한sigma·sweep은 별도 승인이다. 이번1회 후 정지한다.

이전 R320 timecap 수신 확인은632,054,218bytes·SHA e38968f13e3fae64948c2234fb020cad1d5f1119fc8535aa7fc8766e69274f67,160payload+manifest/CRC/history333이다. 옛967개현지목록에서는 직접56개(55불변+계획서의변경전사본1개) 확인이다. 전체967외부검증으로 확대하지 않는다. 이전TIME_CAPS두rawZIP차이원인은미확인이다.

과거333개 보관 바이트는 PREFLIGHT원본ZIP·manifest·SHA영수증·333ledger·검증코드로 새 전달ZIP 안에서 다시 검증했다. 이 보관 바이트 검증은 현지 현재파일 전체의 외부검증과 다르다.

package_manifest.json은 자기 자신을 제외한 새 payload 경로·크기·SHA를 적는다. 동봉한 과거manifest는 당시기록이다. 새ZIP의모든크기/SHA/CRC와역사333검사 후 옆 영수증에 **현지 생성본**의raw크기/SHA를 쓴다. 새수신본의확인은별도다.
