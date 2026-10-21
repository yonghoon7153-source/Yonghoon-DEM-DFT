# Claude에게 전달할 회신 — REIL C4-E E1 v2
2026-10-21

판정: CHANGES_REQUIRED_NO_EXECUTION. 현재 고정본으로 E1-0 실행 승인 단계에 진입하는 것은 보류합니다.

제출 문서2개는 커밋 0e4fbbde88d6b1bcfd47be65718c4ff0efe2191c와 같습니다. 초안4개 식별, 기존 모듈5·시험2·SOURCES 보존본, S1 추가 파일/봉인 연결을 정적으로 대조했습니다.

N1 가림 차단·S1 결속, N6의 E1-0/실제 E1-1–3 및 새24/전체51 활동 구분은 수용 가능합니다. 다음을 비활성 정정안에서 보완해 주세요.

1. 외곽 reap():118과 timeout:208에서 버리는 관측 오류를 누적 보존하세요. 첫 오류 뒤 정상 empty가 나와도 unknown/실패가 유지돼야 합니다.
2. 외곽 자체 Git·pytest·fixture의 첫 Git 호출부터 환경을 정제하세요. _tree()의 init/commit은 launcher.child_env 이전이며 GIT_OBJECT_DIRECTORY 등으로 허용 밖 쓰기가 가능한 정적 경로가 남습니다.
3. 정리15초와 실행기의 10+5+5초 배정을 일치시키세요. settle 전 elapsed_s는 전체 정리시간이 아닙니다. 자동 예산 확대는 승인하지 않았습니다.
4. launcher 준비(688–699행)의 폴더 생성·자기 읽기·disk 조회 예외도 최초 오류·미시작 상태·외부 실패 기록에 연결하세요.
5. 필수 01_red/02_green.source_sha256.txt의 생성 주체·대상·시점·실패 기준을 고정하세요.

미래 E1-2 별도 항목: WORK 사전 Git 검사와 실제 data/git fetch의 includeIf 문맥이 다릅니다. 조건부 TLS 해제/출처 변경을 부작용 전 차단하는 방안이 남습니다. 이번 E1-0에서 실자료 fetch를 하라는 뜻은 아닙니다.

외곽 timeout 무시험이라는 공개 한계만으로 새 결함을 추가하지는 않았습니다. 다만 확인된 오류 유실·시간 배정은 정정해야 합니다. 대조를 추가하면 기존24/51에 조용히 포함하지 말고 새 수·SHA·argv/cwd·예산을 제안해 주세요.

시험·탐침·환경 변경·원자료 fetch/open·optimizer·COMSOL·commit/push는 수행하지 않았습니다. 이번 회신은 코드 정정 실행 또는 E1-0/E1-1–3 승인이 아닙니다. 정확 위치·종결 범위는 REVIEW_KO.md와 DECISION.json을 참고해 주세요.
