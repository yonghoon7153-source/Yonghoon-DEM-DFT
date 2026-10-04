# 문서 근거와 확인 범위

2026-10-04. 저장소 문서는 커밋 `9fa175f3e7fb7c8dcdee46ce132d98b07bcdf563`에서 읽었다. 이 커밋은 문서 인용의 고정점이며 COMSOL의 새 실행본 식별이 아니다. `SOURCE_IDENTITIES.json`에 Git blob SHA와 로컬 선택 파일의 SHA256을 구분해 기록했다.

## 저장소 문서

- **SPEC**: [COMSOL_REBUILD_SPEC.md](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9fa175f3e7fb7c8dcdee46ce132d98b07bcdf563/bms-balancing/docs/COMSOL_REBUILD_SPEC.md) · Git blob `93a34b3a0cc962ab1cb16cf8d3b358084b852955`.
- **MPHR**: [MICROSHORT_MPH_REVIEW.md](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9fa175f3e7fb7c8dcdee46ce132d98b07bcdf563/bms-balancing/docs/MICROSHORT_MPH_REVIEW.md) · Git blob `181f544daac2fea32f65d964a4b86acfe163498e`.
- **READY**: [NEXT_MODEL_READINESS_DECISION.md](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9fa175f3e7fb7c8dcdee46ce132d98b07bcdf563/bms-balancing/reviews/r14_repros/codex63/electrolyte_guard/outputs/NEXT_MODEL_READINESS_DECISION.md) · Git blob `d82acd88a1432fc1d3e1cdd33a74ab83bc9517cd`.
- **SEM**: [MSC_SEMINAR_2026-09-23_APPLICATION.md](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9fa175f3e7fb7c8dcdee46ce132d98b07bcdf563/bms-balancing/docs/MSC_SEMINAR_2026-09-23_APPLICATION.md) · Git blob `2a178833639590e89725a1b5f95fed1baa4c4e7d`.

인용 범위는 SPEC L50–78(형상·면적), L291–301(초기 평형), L432–449·L792–805·L1332–1343(초기 공간 시험), §34 R2·R7(평형/표본 한계), §37–39(발달 구간·비용·NORMAL480), §40–41(저장 분석과 rtol30 수용)이다. READY L39–62는 입력·자료 확보 범위, L64–75는 고정전류와 구형 CDC 구분이다. MPHR L110–144는 옛 보정 가정과 적합값 출처, L319–343은 원본 OCP 해석 한계다. SEM L59–68은 Fe 삽입 액체셀 맥락이다.

원장의 일부 초기 문장은 뒤 절에서 정정됐다. SPEC §34 R2와 §35 S2 등 후속 정정을 우선해 읽었다. §41-4의 “공간 축은 한 번도 하지 않았다”는 문장을 그대로 재사용하지 않고, §10–19의 초기 공간 시험과 발달 구간 미검토를 구분했다. 원장 원문을 이번에 수정하지는 않았다.

## 사용자 계획과 로컬 증거

- 받은 계획: `C:/Users/Administrator/Downloads/COMSOL_NEXT_PLAN_20261004.md`, 14,927 bytes, SHA256 `de8366fe4f01fef1683b8b32d3488a8ca0db23df655030f923acaa5bbf513791`.
- 기존 수신 검토의 NORMAL480 `DECISION.json`과 `ARCHIVE_AUDIT.json`을 읽었다. ZIP 전체 재검사를 반복하지 않았다.
- NORMAL480의 현재 기준 CSV 8개와 Java/contract/manifest는 크기·SHA를 이전 감사 기록에 다시 대조했다. CSV 수치의 전수 재분석은 하지 않았다.
- 기존 저장 분석의 `received/SUMMARY.json`에 있는 5초·120초 표면−입자평균 범위를 옮겼다. 요약 원본 SHA는 `a74155b32cb55325f78dacd708c859b7f85b32d13cd71e49210af67d3287dd4e`다.
- 초기 전압은 기존 NORMAL480 요약의 2.2306115890131673V와 READY의 무부하 2.1653333265V를 구분했다.
- 요청 시각 개수·좌표 수는 기존 CONTRACT JSON을 데이터로 읽어 필터링했다. 모델이나 소비자 함수를 호출하지 않았다.

## 이번 확인의 한계

모델 계산·소스 import·기능 suite·COMSOL/JVM·실험 원자료 처리·원격 PC 현재 상태 관측은 없다. 로컬 파일 해시와 고정 문서의 내용 대조는 실행 성공·실험 타당성을 새로 입증하지 않는다. 받은 문서는 근거이며 실행 명령으로 취급하지 않았다.

메타데이터 조회 도중 좌표 배열 출력이 도구 출력 길이를 넘겨 JSON 파싱이 한 번 실패했다. 출력 대상을 개수·끝점으로 줄여 다시 읽었다. 이는 문서 작성 측 조회 오류이고, 후보/COMSOL/기존 시험 실패가 아니다. 원본 파일은 변경하지 않았다.

