# B-min R1 준비 재검토 회신

고정 커밋 `741dde19b5d07be1872e8bdcedaa90611cbf5b71`, manifest `9dcb47f0ec3ec346b491d90c2836e3b30f54eb88fd5e4fbd216fc34782275cdb`를 정적으로 검토했습니다. 후보 import·구문 해석·컴파일·실행 및 COMSOL/JVM 호출은 0회입니다.

**판정: 국소 보완 필요 — P2 1건.**

- BMIN-N1: 종료 축 분리는 준비 수준 수용합니다. 보존/정책/정리 실패로 entry rc1이면 NOT_ESTABLISHED/NATIVE_CHILD_RC라는 보수적 한계도 수용하며 entry 변경을 요구하지 않습니다. 이는 원시 로그의 독립 재측정이 아니라 부모의 별도 증거 소비입니다.
- BMIN-N2: 누락·구간 밖 DOF 문제는 개선됐습니다. 다만 `mesh_evidence` 322–325행의 줄 수 검사+`re.search`는 같은 줄에 서로 다른 DOF 문구 두 개가 붙어도 첫 값만 읽습니다. 정상 문구 뒤 불완전 DOF 문구가 붙어도 같습니다. 전체 줄 일치 또는 동등한 잔여 문자열 거부로 이 경계만 보완해 주세요. 예상값과 다른 유효 DOF는 계속 기록만 합니다.
- 원 NORMAL480 ZIP을 재해시하고 batch.log를 직접 읽었습니다. Stationary는 86행 1202+12, Time-Dependent는 131행 79485+12이며 시간 의존 구간의 DOF 줄은 정확히 하나입니다. 원본을 재실행하지 않았습니다.
- C1: 문구 축소와 PS01-16의 INCOMPLETE 기대 원칙을 수용합니다. 해당 문자열은 소수 30자리·유효숫자 28자리이므로 “31 significant digits”만 정정하고, PS01-16을 정확 등호 사례 목록에서 분리해 주세요.

검증안은 9군 54 ID / 1530초로 계산이 맞습니다. 동일 행 중복/불완전 꼬리, consumer solved=0, GNativeAxis의 반환 오류·run/manifest 불일치·종료 구조 불일치에 대한 이유별 대조를 명시해 주세요. 기존 ID의 하위 사례와 새 ID를 구분하고 최종 총수·예산·harness/engine/source seal을 시험 전에 고정합니다.

요청하는 다음 산출물은 이 국소 범위의 수정·최소 diff·새 manifest·정정 검증안입니다. Java·entry·물리·시간·좌표·기준 CSV·허용치를 변경하거나 기존 전체 suite를 재실행하지 않습니다. **이 검토 회신 자체는 새 구현/시험 승인이 아닙니다.** 변경부 검증과 native150초 최대1회는 각각 별도 사용자 승인입니다. approved=false/usable=false와 전체·정상 gate INCOMPLETE를 유지합니다.

상세 근거와 실행하지 않은 문자열 반례는 동봉 REVIEW_KO.md, INDEPENDENT_STATIC_AUDIT.json에 있습니다. 후보 함수의 기능 시험 결과로 부르지 않습니다.
