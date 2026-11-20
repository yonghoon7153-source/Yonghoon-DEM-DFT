# Ⓐ 367546 원 위치 재판독과 7:3 사전 셈

| 단계 | 관측 | 다음 |
|---|---|---|
| A3 · NP6 RT 문법 | 원 잡 367546은 12초에 FAILED 2:0. P·RT1·RT2 실행은 각 rc 0. 당시 판독기 rc 2, 14/20. 같은 출력의 원 위치 재판독은 rc 0, 20/20, 결속 PASS | 개발 fixture 재판독 수령 완료. 추가 제출 0 |
| A4 · 7:3 ⓡ | 생산 침대의 전역 W와 원래 쓴 24개 칸의 W는 미측정 | 1저자 승인 뒤 기존 네 파일을 읽는 블록 1회 |
| A5 · 봉인 직전 | A3은 작은 침대의 문법과 재시작 결속에 대한 개발 근거. B의 최초 내용 판정은 기존 기록에 고정 | A4 결과 및 B 잔여 한계를 검토 자료에 포함. 봉인 직전 독립 검토와 새 RJ 발사는 별도로 결정 |

## 수령 대조

실행 핀 `04efe33d61dfadf96a1033c31772f996ae5a205f`, 판독 핀 `851bfd571d4da9f0848e3f7040a1f05c59e4ef0c`. 전달 ZIP의 CRC, RT tar의 SHA256과 목록, tar 안의 세 파일과 바깥 대응 사본의 원바이트가 일치했다. `docs/reviews/p1_rt_fixture_readback_return_20261120/readback.json`은 반환 JSON 원바이트이고 `docs/reviews/p1_rt_fixture_readback_return_20261120/receipt.json`은 수령 대조다. 판독기 SHA256은 `docs/reviews/p1_rt_fixture_readback_20261118/build_reader.py`로 재생성해 일치했다.

SSH와 판독 확인은 각 rc 0, 원격 stderr는 0 B. 새로 참이 된 여섯 항목은 atom_read, pair_read, step, pairs, g2cp, hist_value다. 45개 파일의 원 위치 전후 해시 대조는 1저자가 실행한 판독 영수증의 관측이다. 같은 원자료의 재판독이므로 새 개발 런 수는 0이다. 이 수령 JSON과 기존 키트에서 받아들이는 RT 문법 증서의 스키마가 다르다. 생산용 소비자에 결속할 때는 원 위치 증거를 검증할 수 있게 해야 한다.

## A4가 가르는 것

정본은 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` §15-5b·§15-9 ⑥′, 순서는 `docs/reviews/p1_g2cp_mpi_development_20261116/results_20261116/next_steps.md` §3이다. 기존 323957의 저장 파일 두 개에서 같은 step 3200000의 접촉 쌍과 하중을 비교한다. 원 덱과 로그로 쓰기 당시 격자 6×4×1, NP24를 확인한다. 두 덤프의 고정 신원은 `docs/reviews/dem_unloading_rj_g2c_cause_20261102/ibb_result_20261102.json`, 쓰기 로그·덱의 신원은 `docs/reviews/codex_p1_ps73_identity_20261026/identity-receipt.json`에 있다.

판정 조건은 쌍 집합 일치, 전역 W ≤ 0.05, 모든 칸의 안쪽 하중 쌍 ≥ 100과 칸별 W ≤ 0.5다. 판정 가능한 위반이 우선한다. 그 밖에 격자 근거나 표본이 부족하면 미확정이다. A4 PASS는 다음 검토의 근거다. FAIL 또는 미확정이면 결과와 원인을 남기고 새 RJ 발사를 보류한다. A3·A4 모두 물리 실험 앵커는 없다. 실제 탈압 거동을 보고할 때는 같은 시료에서 잰 질량·면적과 압력별 두께 또는 기공률로 대조해야 한다.

## 1저자용 블록

`PASTE_A4_PS73_WSL_READONLY_1120.txt`는 리포 밖에서 전달한다. ibb의 기존 네 파일 약 300 MB를 읽어 새 비공개 WSL 임시 폴더로 복사하고, 네 해시를 판독 전후에 확인한다. 계산은 WSL CPU 1개에서 진행한다. 파일당 전송 상한 10분, 판독 상한 30분, 자동 재시도 0이다. 반환 대상은 끝 화면의 RETURN 폴더다. COMMAND_RC 0과 continuity.json의 PASS를 함께 확인한다. rc 2는 FAIL 또는 NOT_COMPUTED이며, 전송·신원·시간 오류는 별도 종료다. 이 블록은 기존 RJ 자료의 사전 셈에 한정한다.

사용한 수치 모듈은 851bfd571d4d 판독기에 포함된 바이트다. SHA256 `1778c8437d2f79327c24cec793030dbb50c71043660b5225bb3100f1c7fe3e98`. 기존 수치 회귀 37/37, 같은 6×4 원 격자와 끝 공백 헤더를 쓴 합성 입력 세 가지에서 정상 PASS, 칸당 99쌍 NOT_COMPUTED, 한 칸 전체 초기화 FAIL을 확인했다. 마지막 경우 전역 W=1/24로 전역선을 통과해도 칸 위반이 검출됐다. Bash 문법과 결과 기록용 Python 문법을 검사했다. 실제 ibb 접근과 WSL 역사 자료 판독은 미실시다.

1저자 GO 요청: Ⓐ A4 7:3 ⓡ 읽기 전용 사전 셈 · PASTE_A4_PS73_WSL_READONLY_1120.txt
