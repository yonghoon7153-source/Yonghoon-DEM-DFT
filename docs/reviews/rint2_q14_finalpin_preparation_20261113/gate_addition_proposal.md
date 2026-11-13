# Claude 반입 게이트 추가 제안 — 목적지 audit 회귀

## 1. 넣을 명령·기대

```sh
run 'rint_destination_audit (RTR-01 final destination audit; synthetic only)' python3 -I -B scripts/test_rint_destination_audit.py
```

기대: rc0, Ran 10 tests, OK, 실패0·오류0·skip0. Bash 없으면 성공으로 건너뛰지 않고 실패해야 한다. 실행 위치는 리포 루트, 부모/고친 소스 선택 환경 RINT_AUDIT_SOURCE_ROOT를 설정하지 않는 정상 게이트 환경. RINT_AUDIT_BASH를 쓰면 해당 설치의 Bash를 고정한다.

## 2. 근거·범위

648bb4990157의 시험 10개와 러너 목적지 audit 고침; 64e4d213e는 주석만 바뀌어 시험 원문 유지. 독립 재확인 = 부모 8실패→후보10/10, 기존13/13; 이번에는 이 suite를 다시 실행하지 않았다. 현재 gate에 직접 등록되지 않은 점을 정적으로 확인했다. check_all.sh·CI·공유 inventory는 변경0. Claude가 반입 때 인접 Rint 저장본 시험과 규율/CI 대응을 확인해 한 단계 추가하고, 실제 Linux 전체 게이트 결과·총단계수를 대응표에 적는다. 현재 총단계수가 그대로라고 미리 확정하지 않는다.

이 시험은 합성 파일·추출한 publication 셸 조각·AST 소비자만 본다. 연구 solver·MPI·GPU·현장·운영 봉인 검증으로 세지 않는다. 전체 게이트를 줄이거나 다른 단계를 빼자는 제안이 아니다.
