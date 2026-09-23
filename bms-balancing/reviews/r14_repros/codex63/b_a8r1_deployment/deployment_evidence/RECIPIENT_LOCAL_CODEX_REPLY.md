# 실행본 확정안 수신 검토 회신

2026-09-24. **제한 오프라인 배치 준비 방향은 조건부 수용합니다. 이 회신은 실행 승인이 아니며 B는 계속 미승인입니다.**

수신 ZIP 54,175 bytes / SHA-256 `696de7adf371d2d3a02bafee2a9d942765b3cead7198f3fd679ca357445e4783`의 11 payload+manifest 무결성을 확인했습니다. A8 166개 코드 식별과 불변 복사 대상 11개는 기존 수신 바이트와 일치하고, 새 네 phase argv/cwd도 도출 규칙에 맞습니다. 224개 보존 기록의 내부 일치와 원격 현재 파일 직접 검증을 구분했습니다.

A8 N6/N7을 다시 열거나 389개 suite/F/COMSOL 진단을 반복할 필요는 없습니다. 다음 배치 승인에는 아래를 명시해 주세요.

1. **D01–D16 정확 집합 검사:** completion_contract.py의 389개 집계는 synthetic 단계 전용입니다. 새 deployment_binding에서는 새 driver가 누락/중복/알 수 없는 ID/실패·skip/하위 양성 대조 및 이유·도달 단계를 검사하고, 그 결과를 완료 소비 결과와 AND로 결합해야 합니다. D12에 온전/빈 집합/누락/중복/실패 기록을 포함하세요. 기존 공통 모듈은 변경하지 마세요.
2. **최종 raw 계약 우선:** 최종 후보 contract.approved=false/B_path_ready=true 바이트를 시험 전 seal에 넣고 그 객체에서 한 필드만 false인 view를 만드세요. 다른 필드·타입·raw SHA 변화는 거부합니다. 시험 후 플래그를 바꾼 새 바이트를 기존 시험으로 통과 처리하지 마세요. D10/D11과 최종 manifest에 같은 바이트를 연결하세요. 실제 B 승인 파일은 생성하지 마세요.
3. **TTY 주장 정정:** 기존 launcher는 apply 실행 뒤에 timed_attest의 isatty를 검사합니다. 따라서 ‘TTY가 없으면 Desktop 전에 코드가 막는다’는 보장은 없습니다. 같은 실제 호출 경로에서의 현지 입력/TTY 사전 확인을 아직 미완인 B 착수 조건으로 명시하세요. 이번 오프라인 배치에서 launcher/transport 변경이나 실제 TTY/native 시험은 요구하지 않습니다. 선행 코드 gate가 필요하면 별도 승인을 요청하세요.

기본 prefs 두 참조는 제안한 현재 SHA로만 갱신하고 16개 security 값과 실제 현지 바이트를 다시 확인해야 합니다. 달라지면 중지하세요. 승인 fixture에는 정상 대조뿐 아니라 승인 없음/false/다른 run·manifest 경계를 포함하고, 진짜 approvals/runtime에 쓰지 마세요.

이 조건은 새 세 배치 도구와 기존 D10–D12의 명세를 구체화하는 것이며 native 제어 변경을 허용하지 않습니다. 각 ID 내부 사례 수는 따로 기록하세요. 최대2회·첫 완전 통과 후 종료 등 제안 예산을 유지하고, 사용자 별도 배치 승인 뒤에만 착수하세요.

배치 후 고정 실행본을 다시 독립 확인한 다음 B를 별도로 승인받습니다. 현재 B approved=false/usable=false와 기존 A7/A8 플래그, 원래 failed·b003 pending/원복·MPH·ZIP·영수증, 정상 gate/API 복구/전체 수렴 미완·장시간 보류를 유지하세요.
