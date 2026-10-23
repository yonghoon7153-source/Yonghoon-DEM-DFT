# LHS214 패키지 격리 실행 수정 재확인 — 2026-10-23

판정: 이전 감사의 LHS-PKG-01을 해소했다. 최종 패키지 감사의 미해소 결함은 없다. 전체 게이트·WSL·외부 반박·발사 GO를 뜻하지 않는다.

README 재생 명령 네 개는 모두 python -I이다. mutations.py와 provenance_replay.py 자식 실행에도 -I가 추가됐다. 실제 두 도구에서 이 인자만 제거한 바이트의 SHA-256을 계산하면 tool_changes.json의 수정 전 해시와 일치한다. audit.py·pin_probe.py는 동일 해시다. 따라서 계산/검사 본문이 함께 변경되었다는 증거는 없다.

격리 재검증 원시 로그를 직접 집계했다: pin 자체시험 123 PASS/0 FAIL, 네 변이 각각 122 PASS/1 FAIL(S11g), 이전 도구 121 PASS/1 FAIL(S0b). 신규 진리표 512 cases·mismatch0 및 7문서 반례, 여섯 pin 입력 결과, 비준 날짜8/7·바이트일치는 이전 원시 결과와 동일하다. 이전 도구 JSON은 old_source_sha256 필드가 추가되었고 기존 rc/last/failures 값은 모두 동일하다. 이전 실행이 격리였다고 소급하지 않고 isolated_revalidation/의 별도 기록으로 보존한다.

현재 증거 MANIFEST 58개와 SOURCE_SHA256SUMS 40개를 실제 파일로 재계산해 불일치0. reviewer·root_reproduction의 원시 파일은 원 실행 폴더의 대응 파일과 다시 바이트 대조했다. 기존 결과의 수·실패 종류·한정은 변하지 않았다. 원문·원 결과를 재분류해 새 시험 수에 합산하지 않는다.

이번 재확인은 수정분과 별도 재검증 증거의 감사다. 감사자의 이전 별도 pin 재현도 -I -B에서 동일한 123/123·LF 경계를 확인했으며 새 전체 게이트를 실행하지 않았다. 최초 감사 lhs214.md는 당시 지적을 남긴 이력으로 보존한다.
