# 비활성 native60 승인 초안 — 실행 명령으로 사용 금지

approved=false / usable=false. 이 문서는 사용자 승인이나 실제 approval/release/USER_DECISION이 아니다. 변경부 기능 검증과 고정 후보의 수용은 아직 없다.

고정 run_id `normal60_candidate_001`, root `outputs/normal60_offline_preparation_20260930/`, manifest SHA `82e556243b29b10ae65b95dcdff7f854734b6f1cfffc1881327cab1939ebe5c8`.

추후 사용자에게 요청할 한 건: **정책 무변경·동일 provisional 모델 fresh t=0→60초 정상 진단 최대1회**. threshold0, physical300/particle320·320/0.1C/sigma1e−20·기존 초기화/물성/OCP/guard/cap 유지, 요청737시각. compile≤1/batch≤1/solve≤1, 추가control0/retry0. 저장MPH restart가 아니다.

일반 사용자 Windows PowerShell5.1 NoProfile 전경·고정Python에서 새 두 challenge를 사용자가 직접 입력한다. AI 대리 입력·별도 C2 check-only 없음. 후보 argv/cwd는 COMMAND_MAP.json에 정확한 배열로 고정했으며 현재 사용 불가다. cwd는 기존 `outputs/b020_profile_unit_stages_20260927/src`를 유지한다. 전달 ZIP의 snapshot에서 실행하지 않는다.

요청16코어, 시작 디스크20GiB, RAM은 관측만. 새 원점에서 사전/입력180·공유native3600·소유정리합계120·분석900·로컬증거300·부모전체5100초를 제안한다. 실제60초 비용·peak RAM은 미확인이다. timeout·정책/식별 불일치·경로 충돌·첫 오류는 보존하고 중지한다. 다른 프로세스 종료·자동 retry·다른 shell/권한/정책 fallback·미사용 예산 전용은 없다.

필수 선행: 변경부 수용에 결속된 새 검증 release, 현재 source/prefs 식별·security 값/실행 경로 확인, 이 후보와 위험/횟수/예산에 대한 사용자 별도 명시 승인. 현재 prefs 값은 미래 승인값으로 추정 기입하지 않았다. NATIVE_APPROVAL_FIELD_SPEC.json의 출처/필드에 결속한 실제 파일은 그때만 허용된 RUN 밖 경로에 생성한다. 봉인 CODE_MANIFEST/CONTRACT의 false 플래그는 수정하지 않는다.

예정 경로는 root 아래 future_run_001, future_parent_001 및 future_authorizations/{normal60_001.json,VALIDATION_RELEASE.json,USER_DECISION.json}이다. 현재 모두 미생성이고 충돌 시 삭제/재사용/새 이름으로 우회하지 않는다.

정상60 완료: 정확60초 저장·native 정상 종료·전 저장시각/737요청·좌표/단위/유한값·Li/전압 항등식·표면/guard, 두 기준 직접 비교, 보존/소유정리/정책 보존, 부모 자식 rc/최종POST_WRITE·예산을 함께 충족. 보호중단은 원인·전후 증거를 남기는60초 미완, 오류는 최초/후속 오류를 구분한다. rc0/ZIP만으로 성공하지 않는다.

부모 성공 상태는 AWAITING_60S_LIMITED_EXTERNAL_ACCEPTANCE다. 원 overall/normal gate INCOMPLETE·실효정책 UNVERIFIED를 보존한다. NoExit OS rc=null, 사용자 프롬프트 복귀는 OS 종료코드가 아니다. 마지막 반환 누락/오류/예산 초과가 이전 PRE_WRITE의 성공을 덮는다.

이번 초안은30초 반복·1198 재시험·120초/12시간·CDC·휴지·finite sigma·sweep·후보C를 포함하지 않는다. 결과를 수용한 뒤 다음 구간을 별도로 정한다.
