# 제출 JSON 산술 대조 방법

검토용 산술만 수행했다. 받은 reil_p0.py를 import하거나 함수로 실행하지 않았고, 원자료를 열거나 P0를 재실행하지 않았다.

1. 부속 A §2-5 및 v2의 명목 11행과 세 영역 상자를 기준 상수로 읽었다.
2. max_q의 JavaScript DataView IEEE 754 비트를 정수 가수·2의 지수로 분해하고 BigInt 유리수로 약분했다. 제출 분수와 일치했다.
3. 십진 명목·τ·상자·D를 정수/10의 거듭제곱으로 읽었다. 모든 연산은 BigInt 분자·분모와 최대공약수 약분으로 했다.
4. P=[mP−τ,mP+τ]∩mP상자, N=[mN−τ,mN+τ]∩mN상자, I=[LII−τ,LII+τ].
5. lhs=[P_lo−I_hi,P_hi−I_lo], rhs=D/max_q. P와 N이 비지 않고 max(lhs_lo,rhs_lo)≤min(lhs_hi,rhs_hi)이면 양립이다.
6. 99개 정확한 키의 집합, 다섯 구간의 분수 끝점, 상태 및 집계를 대조했다. 십진 표시의 자릿수 품질이나 원 측정자료의 정확성을 대신 검증한 것은 아니다.
7. JSON의 배열 크기·OK/판정 불가·raw 메타데이터 부재와 두 환경 manifest·lock의 텍스트를 교차 대조했다.

ARITHMETIC_CHECKS.json의 99행은 새로운 연구 사례나 승인된 suite 횟수가 아니라 제출된 표의 산술 검산 기록이다.
