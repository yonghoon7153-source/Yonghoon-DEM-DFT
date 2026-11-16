# A/B 전달 패키지 누락·WSL 회수 정정

실행 소스 핀 = `8231f395cda98fed8dbbf5422ccda003b11a8da9`. 원 시도 = `ad7c1f826525d86166d65ad3c50ef82bce7e46fc`.

## 1. 원인과 수정

Python 모듈 의존을 모은 전달 목록에 비 Python 자원 `dem_scripts/mixer_20260921/launch_highbo.sh`가 빠졌다. `mixer_gate_reader_diff.py::_gate_code()`는 그 셸의 내장 Python 관문을 읽으므로 smoke_blind가 FileNotFoundError로 중단됐다. 기존 계산·판독 정책 결함으로 혼동하지 않는다.

V2 패키지는 고정 Git blob의 그 파일을 추가한다. 패키지 검사에서 파일의 목록 소속을 필수로 요구하고, B의 `e0_runtime_tool_identity.json`에도 그 해시를 넣어 변조를 재검사한다. 역사 source_seal의 12개 목록은 그대로다. 새 파일 1, 기존 변경 3(패키지 manifest·복사 조립 도구·그 시험), 나머지 270파일은 바이트 보존이다. 총 274파일이다. launcher 원문과 smoke_blind는 고치지 않았다.

## 2. 검증

- 동일 시험 10개: 수정 전 새 2실패/오류0 → 수정 후 10/10. 누락 목록이 자기 일관적이어도 거부하며 B의 자원 포함·변조 검사를 확인한다.
- 원 `_gate_code` 함수 그대로: 원 패키지 경로에서 FileNotFoundError 재현 → V2에서 내장 관문을 읽고 Python 구문 확인. 관문 실행·실제 제출이 아니다.
- 최종 고정 패키지의 로컬 assemble: A 네 단계·B validate8·40자산·12의존 통과, 덱8·STL24 보존. Linux 전체 smoke_blind 및 후속 모의는 1저자 V2 실행에서 확인한다.
- 두 V2 블록의 bash 구문 및 내장 Python 구문 확인. 작은 로컬 합성 파일을 폴더 밖에 압축: tar rc0, 입력 바이트 보존, 압축 멤버 읽기·SHA 출력 확인. WSL 현장 실행으로 세지 않는다.

## 3. 블록과 다음

V2는 기존 프로젝트 venv Python을 직접 선택하고, 작업 폴더 밖 별도 새 디렉터리에 result.tar.gz를 만든다. command_rc와 archive_rc는 따로 표시한다. 경고 숨김 옵션은 사용하지 않는다. 기존 실패 폴더·원 패키지는 덮지 않는다.

믹서는 V2 A/B 결과를 받는다. 수영은 이미 개발 계산 완료이며 V2 블록은 향후 사용용이다. 기존 수영 소스·패키지·입력은 변경하지 않았다. G2c′ 진행 중인 블록·잡은 수정하지 않는다. Rint 고정 가지와 공유 파일도 변경하지 않는다.

전달 파일·해시는 `docs/reviews/nonrint_execution_queue_20261116.json`에 기록한다. 원 수령과 수영 값의 확인 범위는 `docs/data/nonrint_wsl_results_20261116/README.md`를 따른다.
