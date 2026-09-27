# 검토자 보조 검사 이력

- `data_audit.py` 첫 실행: rc 1. 검토자가 `artifacts/` 전체 불변을 잘못 가정하여 README 문구 정정을 결과 바이트 변경으로 셌다. 실제 묶음 디렉터리와 index로 범위를 정정했다. 생산 코드 결함이나 송신 시험 실패로 계산하지 않는다. 첫 실행의 SOURCE_BEFORE는 보존하고 재읽기 동일성을 확인한다.
- 대상 저장소의 모듈·suite·과학 계산·archive/restore 프로그램은 실행하지 않는다. 별도 검토자 스크립트와 허용한 순수 함수/문장 추출 검사는 각 출력에 실행 경계를 명시한다.
- 두 번째 data audit: rc 1. 기존 소급 `paired_fixed5_v4`에도 evidence.out이 있다고 가정한 검토자 KeyError. 기존 소급 상태는 그대로 읽고, 이번 진단 실행 grid_fit_v5의 필수 out 결속만 별도로 검사하도록 정정했다. 과거 기록을 채우거나 attach하지 않았다.
- data audit 최종 rc 0: 57 RUN_SCOPE·2,789 tracked 파일·두 영수증·묶음·등록부·투영 불변 대조 완료.
- decision_probes 첫 실행 rc 1: 검토자가 heredoc import 문장의 철자를 잘못 가정하여 추출 ValueError. 앞선 18개 순수 판정 사례의 내부 assertion은 통과했으나 집계 JSON은 저장 전이었다. 첫 fixture는 보존하고 정확 heredoc 구분자로 바꾼 뒤 새 fixtures02에서 다시 검사한다. 생산 코드/시험 실패가 아니다.
- decision_probes 두 번째 실행 rc 0, 23개 사례 기록. shell footer 사례의 `du/cut/cat`이 Git Bash PATH에서 누락된 stderr가 있었다. 원문을 보존하고 `shell_boundary_check.py`에서 해당 두 사례만 Git 유틸리티를 프로세스 PATH에 넣어 재확인한다. 생산 archive는 어느 경우에도 실행하지 않는다.
