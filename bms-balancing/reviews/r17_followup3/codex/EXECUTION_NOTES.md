# 실행 범위와 검토 도구 메모

- 검토 대상 e834b01e, BMS 수정 7f09804f. 독립 sparse checkout을 사용하고 제품 코드를 수정하지 않았다.
- 네이티브 Windows/Python 환경이다. fcntl이나 shell을 가짜로 대체해 Linux 게시 성공을 주장하지 않았다.
- 원래 47 case 재현기와 producer 재현기는 이전 검토 파일과 바이트가 같다. 현재 fixture import의 변화와는 구분한다.
- 원래 producer 재현기의 child 실행은 rc 0이고 stdout/stderr/command JSON이 저장됐다. 이를 콘솔로 다시 인쇄하던 reviewer wrapper만 cp949 UnicodeEncodeError로 rc 1이 됐다. wrapper stdout을 UTF-8로 고쳤으며 제품 실패나 producer 실패로 집계하지 않는다. 재계산 성공으로 바꿔치기하지 않고 원래 저장된 child rc를 사용한다.
- 추가 optimizer fault probe의 첫 호출은 리뷰어가 필수 seeds 인자를 빠뜨려 TypeError가 났다. `NEW_FAST_INITIAL_PROBE_RESULTS.json`에 보존했다. 인자를 고친 후 새 fixture에서 다시 실행했다. 이 첫 TypeError를 제품 결함으로 세지 않는다.
- solver 반환 주입은 의존 객체에 대한 명시적인 fault injection이다. 정상 SciPy 계산에서 상자 밖 반환이 관측됐다는 주장이 아니다.
- Windows process command-line 상태 조회는 접근 거부됐다. 이 조회 실패로 시험 성공/실패나 전체 프로세스 부재를 추정하지 않았다.
- GC 재현은 각 실행마다 새로 만든 하위 경로만 대상으로 하며, 대상들이 그 fixture 안에 있고 symlink가 아님을 실행 전에 확인한다. A/B payload 제거는 합성 시험의 의도된 결과다. 실제 원자료 삭제 0.
- TEST_RESULTS의 분류는 trace의 첫 관측 원인 기준이다. 환경 제약 뒤에 제품 결함이 더 없다는 증명은 아니다.
- 임시 파일/합성 계산과 리뷰 산출물을 만들었다. 원자료 적합, 생산 코드 수정, commit/push, 외부 발송, COMSOL 호출은 하지 않았다.
