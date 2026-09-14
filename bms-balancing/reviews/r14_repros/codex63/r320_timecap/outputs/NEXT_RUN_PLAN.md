# NEXT_RUN_PLAN — 300/320H0125 단일 초기 시간상한 시험 후 정지

현재 판정: **이번 표본의 초기 시간상한 반감 민감도 기준 충족**. 전체 수렴 미완·장시간 운전 보류를 유지한다.

새 Caps300R320H0125(job18a00b03e38d4694b9ba30d88e7008f4)의 5초 계산 한 번만 완료했다. 기존 Caps300R320H0250(jobf0db6d080ad04045a2b43dc5a51d89b2)은 재사용했다. 초기 cap만 .00025→.000125초로 변경했고 이후 .1초 및 물리300·입자320/320·반경·물성·OCP·Li·전류·sigma·초기화·허용오차·scale·보호를 유지했다.

전체 정확 공통 저장 시각 0–5초의 최대 전압 차는 0.0012699200233 mV @0.002초, 최대 표면 x 차는 2.1349484521e-08 @0.002초·N z=52 µm다. 이전 반경 최대 .6170341087208 mV의 0.205810344250%다. 이는 크기 비교이며 수렴 차수가 아니다. 지정 시각과 정확 공통 저장 시각의 0–1/0–5초를 별도로 집계했고, 최대 시각과 .002초의 성분을 같은 시각끼리 분해했다.

실제 mesh·자유도·expr 설정·accepted step·.1초 경계를 확인했다. 판정은 이번 초기 시간상한 민감도에 한정한다. .1초 이후 시간 정확도·참값 오차·전체 수렴은 미입증이다.

**전달 후 정지한다.** 추가 시간반감·메시 세분·전체 프로토콜·12시간 휴지·유한 sigma·sweep은 이번 승인 범위에 없으며 자동 실행하지 않는다.

OCP 외삽 금지·기존 OCP입력/고체표면 StopCondition·failed/INCOMPLETE_RANGE_STOP과 원본을 보존했다. 전해질 양수는 후처리 검사다. 이전 TIME_CAPS raw ZIP 차이 원인은 미확인이다. 수신 측 이전147payload/history333 확인과 현지 보존 목록의 검증은 범위가 다르다.

[이번 결과](radial320_timecap/TIMECAP320_RESULTS_KO.md), [실제 step](radial320_timecap/native_steps_summary.json), [분석](radial320_timecap/results/analysis.json), [계약](radial320_timecap/comparison_contract.json).
