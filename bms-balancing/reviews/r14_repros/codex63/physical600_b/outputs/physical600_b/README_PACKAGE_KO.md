# COMSOL 6.3 B — 물리300→600, 입자320/320 고정

승인된 Astra High·16코어·1800초 예산으로 새5초 계산1회만 실행했다. 기준 Caps300R320H0125C16은 재실행하지 않았다. 새 이름은 Caps600R320H0125C16이고 job56975e4d24054b23bcec87553875f729다. 물리 메시만240/120/240으로 변경했다. 입자320/320·원래 H0125 cap·물성·OCP·초기조성·Li·전류·sigma·초기화·허용오차·scale·보호·187요청시각·241좌표를 유지했다.

- [결과 보고서](PHYSICAL600_B_RESULTS_KO.md), [8창 분석](results/analysis.json), [별도 구현의 원시 재검산](results/raw_arithmetic_recheck.json)
- [소스 변경](Caps600R320H0125C16_source.diff), [계약](comparison_contract.json), [실제 설정과 step](native_steps_summary.json), [최종 검사](final_checks.json)
- [수정 계획](../NEXT_RUN_PLAN.md), [변경 전 계획](NEXT_RUN_PLAN_before_physical600_b.md), [보존 수준](PROVENANCE_LEVELS.json), [이전 수신 확인](RECEIPT_CONFIRMATION.json)

## 내용과 재현

새MPH와 두 해의 원시CSV14개씩·소스/SHA·staged/generated Java·request/status·전체 로그·Time/Variables 설정·accepted 간격·성분/표면 비교를 포함한다. 이전 기준MPH와 이전 원본CORE16_CONTROL ZIP은 이미 전달된 자료이므로 중복 포함하지 않는다. 이전 생성 영수증·manifest와 별도 사용자 수신 확인은 보존한다.

별도 작업 사본에서 Python 표준 라이브러리로 다음 후처리를 재계산할 수 있다. COMSOL을 호출하지 않는다. 산출물 경로에 기록하므로 보존 원본을 직접 작업 폴더로 사용하지 않는다.

```text
python work/physical600_b/analyze_results.py
python work/physical600_b/raw_recheck.py
python work/physical600_b/extract_steps.py
python work/time_caps/zip_identity_verify.py --root .
```

extract_steps는 포장에 없는 기존 기준MPH에 대해 audit_files.json의 이전 해시를 사용하고 재해시가 아님을 명시한다. 전체 명부를 필요로 하는 준비/보존/native_and_preservation_check는 이 부분 전달본만으로 현지 전체 검증을 재현할 수 없다. package_manifest.json은 자기 자신을 제외한 payload를 기록한다.

## 해석과 보존

187요청시각과 정확 공통 저장 교집합을 따로 비교한다. 시간 보간·최근접 시각 대체가 없다. 같은 cap은 같은 accepted 이력이나 새 메시의 시간 정확도를 보증하지 않는다. 기준1mV·표면x1e-4의 충족은 이번 지정 표본의 물리축 세분 민감도 범위다. 참값 오차·전체 수렴·장시간GO를 뜻하지 않는다.

OCP/entropy 외삽none, StopCondition 노드1개/활성 조건2개, 기존 failed/INCOMPLETE_RANGE_STOP을 유지한다. 전해질 양수는 **후처리 검사**다. 이번 범위는 새 보호 작동 시험이나 전체 프로토콜 검증이 아니다. 추가 계산·재시도·시간/메시 세분·12시간 휴지·유한sigma·sweep은 별도 승인이다. 한 번의 실행과 검증 후 정지한다.

이전CORE16_CONTROL ZIP 수신 확인은707,524,803bytes·SHA5f5b197e4467c15c3150de2650c0e2c6c1e937710f005c24e5ea9ccc306143af,234payload+manifest/CRC/history333이다. 이는 별도 사용자 보고다. 당시 현지1,247개 전체가 아닌 직접93개(92불변+계획서 변경 전 사본1개) 확인이다. 이번 현지 명부와 이 전달본의 직접 포함 수는 PROVENANCE_LEVELS.json/최종 영수증에 구분한다. 역사333개는 별도 범위이며 현재 파일 수에 합산하지 않는다. 이전TIME_CAPS raw ZIP 차이 원인은 미확인이다.

최종ZIP의 모든 payload 크기·SHA·CRC와 역사333 보관 바이트를 재검증한 후 외부 영수증에 현지 생성본 rawZIP 식별을 기록한다. 새 수신본 식별은 아직 관측하지 않았다.
