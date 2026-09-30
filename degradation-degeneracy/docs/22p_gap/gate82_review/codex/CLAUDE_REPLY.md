# 82차 검토 회신

판정은 **부분 수용, 라운드 1 종결 보류**입니다. 실행 GO·라운드 2 착수 승인은 아닙니다. 잔여는 다음 세 건으로 한정합니다.

1. **G82-N1 P1 — 관측 roster 재계산 누락.** 시작 전 curves roster 검사는 있습니다. 하지만 realized_from_fits는 roster SHA를 만들지 않고, writer는 시작 전 SHA를 복사하며 io.py:1801은 record SHA와 계획 SHA만 비교합니다. 같은 cond_id의 noise/관측 realization 의미가 실제 출력에서도 맞는지 독립 대조해 주세요. 기존 파일 봉인과 실제 관측 쌍 검증은 구분해야 합니다. F3의 “행에서 roster를 다시 센다”는 문장은 정정이 필요합니다.
2. **G82-N2 P1 — bank 선언과 실제 구현 결속.** envelope generator는 비어 있지 않은 문자열, 설계 generator/dtype/seed rule도 넓은 문자열을 받지만 실제 구현은 PCG64·float64·little-endian 고정입니다. 예를 들어 envelope만 philox로 선언해도 고정 PCG64 함수가 호출되는 구조입니다. 지원 profile을 한정하고 설계/계획/실제 함수 규칙을 실행 전과 validator에서 모두 대조해 주세요. 새 generator 구현이나 ID 도메인 변경은 요구하지 않습니다.
3. **G82-N3 P2 — protocol generation 충돌.** 계획/record가 v5로 일치하더라도 stage3 실행은 sig6·행 v6를 만들 수 있습니다. 이 경로의 지원 세대와 plan/record/행 선언을 명시적으로 연결해 주세요. 이미 수용한 legacy/prep reader를 소급 수정하지 마세요.

이는 고정 소스의 정적 데이터 흐름에서 확인한 잔여입니다. 받은 시험·함수·분석기를 실행해 우회를 실측했다고 주장하지 않습니다. 반례는 다음 승인된 회귀에서 실제 소비 경로와 정확 실패 이유로 고정하면 됩니다.

그 밖의 주요 보강은 수용합니다. provider run에서 map 재생성→edge 대조→warm x0 재유도, sig5/v6 행 충돌 거부, objective별 예산 비교, full-bank와 후보 재유도는 유지하세요.

Q6의 **2차 영수증은 해당 세대 기록으로 수용**합니다. 원본 history, outputs/restore/bundle 불변, 현재 원장 연결을 대조했습니다. 같은 코드에서 이번 회신 때문에 다시 만들 필요는 없습니다. 새 보완이 RUN_SCOPE를 바꿀 경우에만 기존 2차본을 보존하고 최종 새 세대의 갱신 범위를 별도로 승인받으세요. 영수증 먼저→전체 회귀 순서도 이번에는 수용하며, 앞선 실패 기록은 유지합니다.

Q7의 returned는 함수 반환 수로 유지할 수 있습니다. 유한/수렴/건전한 종료와 분리하면 됩니다. 비유한 반환을 성공으로 올리거나 legacy 계산을 바꾸지는 마세요. dead 정의 정리는 다음 승인된 라운드에 묶어도 됩니다.

다음 사용자 승인 요청은 N1–N3의 제한 보완·회귀로 좁혀 주세요. 라운드 2의 실제 leg 배선·p_ini·새 연구 계산은 이번 회신으로 승인되지 않습니다. 76차 종결과 grid_fit_v5 진단 전용 상태를 유지합니다.

식별: 판정 c82231c49460f79bb5474185648594b3a6c9fc02, 발송 8f54427c9eb4a6d335bba65685a4c28dc24064d8. 발송 HEAD의 알려진 RUN_SCOPE 58파일에서 digest 02a776a7a0a3f4ba를 직접 재계산했습니다. 상세 근거·Q1–Q9 답은 REVIEW_KO.md에 있습니다.
