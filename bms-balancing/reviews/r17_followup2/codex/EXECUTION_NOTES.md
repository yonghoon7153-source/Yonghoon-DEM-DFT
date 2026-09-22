# 실행 범위와 중간 오류

- 기존 사용자 작업트리를 건드리지 않기 위해 별도 sparse clone의 detached HEAD를 사용했다.
- 네트워크 읽기 권한 승인 뒤 원격 HEAD를 확인했다. 전역 Git safe.directory/Windows ACL은 수정하지 않았다.
- 첫 focused 시험은 71개 실행 뒤 pytest의 기본 임시 폴더 `pytest-of-User/pytest-current` 정리에서 PermissionError가 발생했다. 원래 focused.log/xml/json을 보존하고, 고유 검토 전용 basetemp로 focused_scoped를 다시 실행했다.
- 같은 기본 임시 폴더를 쓰던 최초 full 실행은 완료 전에 중단했다. full.log는 보존하며 전수 결과로 세지 않는다. full_scoped가 별도 전수 시도다.
- repro_producer_reader 최초 시도는 결과 JSON/log 저장 뒤 마지막 콘솔 출력에서 cp949 UnicodeEncodeError였다. 표준 출력 UTF-8을 명시해 재실행했다. 그 오류를 대상 프로그램 실패로 세지 않는다.
- 합성 데이터 최적화는 재현 시험이다. 실제 셀 원자료 재적합이나 과학 정본 갱신이 아니다.
- GC 재현에서 삭제된 것은 새로 만든 합성 파일뿐이다. 전후 경로/해시는 REPRO_RESULTS.json에 있고 재현기로 다시 만들 수 있다. 사용자 원자료/기존 산출물은 삭제하지 않았다.
- 전체 시험은 일부 회귀가 소스/fixture를 잠시 변형했다가 복구하는 동작을 포함한다. 최종 checkout status 및 원본 blob/checkout 바이트는 REVIEW_IDENTITY.json으로 재확인한다. Windows 줄바꿈 정규화 여부도 구분한다.
- 지원 환경의 Linux 전수 성공·Windows 전체 호환·동시 게시의 안전을 이 결과로 대신 증명하지 않는다.
