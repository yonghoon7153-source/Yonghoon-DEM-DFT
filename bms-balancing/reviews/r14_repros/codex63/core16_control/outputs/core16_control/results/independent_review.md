# 독립 원시 산술 재검산

상태: **PASS**. 분석 구현을 import하지 않는 [raw_recheck.py](../../../work/core16_control/raw_recheck.py)가 원시 boundary/profile CSV를 읽어 Decimal 산술로 별도 검산했다.

두 쌍의 16개 창에 대해 최대 V 차이·최대 시각·동시 성분, 최대 pointwise 표면 x 차이·시각·전극·좌표를 확인했다. 세 해의 정확 공통 986개 시각과 475,252개 위치의 부호 있는 항등식도 확인했다.

동시 성분 36행, boundary 원문 72행, 표면 원문 snapshot 5,784행을 원시 CSV 문자열과 대조했다. 시간 보간·근접 시각·다른 좌표 대체가 없다.

이 PASS는 산술 일관성과 파일 원문 대응의 확인이다. 물리적 수렴 PASS, 일반적 코어×cap 상호작용 부재, 상쇄 부재 또는 추가 계산 승인을 뜻하지 않는다. 두 쌍의 민감도 기준 판정은 analysis.json의 comparisons에서 각각 확인한다.

[상세 재검산 JSON](raw_arithmetic_recheck.json).
