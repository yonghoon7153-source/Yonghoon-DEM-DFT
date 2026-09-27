# 검토자 검사 이력과 범위

- 별도 checkout `g76_20260927`, 고정 HEAD b5e4eade. 기존 g75 checkout/산출물은 변경하지 않음.
- `data_audit.py` 1회: 실제 tool chunk `543335`가 session35063으로 지속, 완료 polling chunk `d0a382`, exit_code0. DATA_AUDIT_PASS. 소스 2,868개·RUN_SCOPE58개·등록부369개·75차 원본 ZIP70payload 대조.
- `decision_probes.py` 1회: tool chunk `5e1a60`, exit_code0, wall_time_seconds2.6891794. 44개 모두 예상 결과. 제공 suite/실제 archive/restore/분석 프로그램은 실행하지 않음.
- 읽기 보조 `git diff` 한 호출은 lazy partial-clone blob을 가져오면서 기본 Schannel credential handle 오류로 실패했다(chunk `93aa25`의 첫 명령). 다른 읽기 출력은 반환됐다. 같은 diff를 `http.sslBackend=openssl`, `credential.interactive=never`로 다시 읽어 성공했다(chunk `c68716`). 대상 코드·자료 변경, 대상 시험의 실패/재실행이 아님.
- 위 chunk 정보는 이번 도구 반환에서 작성한 검토 기록이지 별도 원시 OS 감사 로그가 아니다. 검사 전체 stdout/판정은 DATA_AUDIT.json·DECISION_PROBES.json에 구조화되어 있다.
- 수신 Windows/검토자 PyYAML에서의 AST·heredoc 격리 검사와 송신 Linux의 1,944개 전체 회귀/strict smoke를 구분한다. source_digest는 대상 모듈 호출이 아니라 고정 파일들의 독립 재계산이다.
- reviewer fixture만 생성/변경. production 파일·원장·receipt·class·results·기존 ZIP은 수정하지 않음. 전체 과거 원격 파일/프로세스 보존을 검증했다고 주장하지 않음.
