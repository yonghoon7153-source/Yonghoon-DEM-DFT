# E0 단일 잡 squeue 부재 처리 고침

| 트랙 | 계산 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| 믹서 E0 | 기존366423 수집 | 사용자 제공 우회 수집 TXT 확인·컨트롤러 수정 | 새12/12, 기존19통과·1건너뜀 | 반입·다음 패킷에 적용, 기존 결과는 별도 수령 |
| 탈압 A·수영 2D | RT 연결·F 접촉 준비 | 앞선 대기열 유지 | 이 고침 중 새 계산0 | DEM 우선 차례 유지 |
| LHS·50kg | 기존 준비 | 변경0 | 신규0 | 기존 계획대로, 후막 보드 밖 |

바탕 B = `63f12d8a594c7490695abee0eaadc17f2257dd05`. 새 가지 codex/mixer-squeue-purged-1116. 반입 순서 = 코드/시험/README `dd2c50741f43830ec83b232d0ec51b990d5beaab` → 이 쪽지 커밋. 앞선 dem-observations·dem-a1-contact 가지는 재작성하지 않았으며 계속 별도 반입 대기다. Rint 고정 가지 불변.

## 변경과 근거

- scripts/mixer_e0_pilot_ibb.py: squeue 단일잡 rc1·빈stdout·지정 Invalid job id 진단 하나만 ABSENT로 처리. 원 rc/진단을 evidence에 보존하고 **sacct 유일 종료행**으로만 종료를 확인한다. 통신/권한/혼합오류·다른rc·stdout존재는 실패 유지. sacct 부재300초·실패·다른잡·중복/비종료행은 완료가 아니다. 제출/취소/예약/봉인 함수는 변경0.
- scripts/test_mixer_e0_squeue_absent.py: 실제 wait_job을 모의 scheduler/시간으로 호출. 같은12메서드 수정전 실패12관측/오류0 →12/12. 기존20메서드 중19통과·1건너뜀(OS symlink 생성 권한 없음), 실패0. 전체gate/실제Slurm 재실행0.
- docs/reviews/mixer_e0_squeue_purge_20261116/: 좁은 진단 형식, 보존, 시험/AST 신원. 기존27함수 AST 같음, wait_job만 변경·새 helper1개.

## 고정 자료와 이번 범위

사용자 제공 purgedfix TXT 전체 해시 및 내장 두 파일 동일성은 verification.json에 기록했다. 원 TXT·원 로그·주소/계정/홈 경로는 리포에 넣지 않았다. 기존366423 실행 소스핀 `997aabe1b5a702e2f389007e3923018d778ce857`와 그 승인·해시·반환은 변경하지 않는다. 새 코드가 기존 author_go의 소스 해시와 다르므로 그 실행 폴더에 덮어쓰거나 새 해시를 소급하지 않는다. 이번 고침은 새 소스핀 및 다음 패킷용이다. 앞단 수집 TXT도 새 패킷에서는 같은 helper로 판단하고 sacct 확인을 유지하도록 연결한다. 현재 고정 수집 helper/worker 교체 없음.

현장 접속·새 제출·취소·MPI/엔진·값 재계산0. 사용자 전달의 수집 수행과 이 창의 합성 시험을 구분한다. 현재 E0 결과의 최종 성공/물리 자격은 이번 수정으로 판정하지 않았다. 새 리뷰/실행 관문을 개발 준비에 추가하지 않는다.

## Claude 반입 때 넣을 줄

게이트 추가 제안: `python -I -X utf8 -B scripts/test_mixer_e0_squeue_absent.py` →12메서드·실패0·오류0. scripts/check_all.sh는 직접 고치지 않았다.

공유 기록: "E0 감시의 purged job squeue rc1 처리 고침: 해당 진단만 ABSENT, sacct 종료 확인 유지. 새12/12·기존19통과/1Windows symlink건너뜀. 기존366423 고정자료와 원격 트리 불변·현장실행0·결과 판정 별도."

원장·CLAUDE.md·진행 기록 변경0. 반입은 1저자 지시 뒤 Claude가 cherry-pick -x로 진행한다.
