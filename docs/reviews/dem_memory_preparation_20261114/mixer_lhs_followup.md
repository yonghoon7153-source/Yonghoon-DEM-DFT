# 믹서·LHS — 준비본 연결 확인

## 1. 믹서 부모/자식 시계 결속

고정087ba5eb9a8d의 두 선택 함수만 AST로 읽었다. mixer_selected_process_sites.json에 각 원 소스SHA/blob·함수·호출행을 보존했다. mixer_smoke_blind.selftest에는 같은 wrapper 파일을 sys.executable로 다시 부르는 subprocess.run 한 곳, mixer_gate_reader_diff.build가 돌려주는 invoke에는 launcher에서 추출한 Python gate 문자열을 sys.executable -c로 부르는 한 곳이 있다. launcher 셸 실행0. 두 함수 밖 전체 동적 호출망 인증이 아니다.

기존 고정시계 사본은 wrapper 모듈의 datetime 이름을 대체한다. 자식 wrapper가 같은 사본의 __file__을 실행하는지 실제 네 칸 시험에서 sourceSHA와 함께 확인한다. 추출 gate/다른모듈/OS 시계까지 고정됐다고 확대하지 않는다. 기존 parent_child_clock_binding 칸에는 두 wrapper의 source/overlay 신원과 실제 대상시각 근거를 넣는다. 범위 밖 시계는 비적용/미확인으로 구분한다.

선택 함수 정적2곳·import0·subprocess 실행0. Linux 전체 selftest·POSIX0600·환경/자원·E0/first8·재봉인GO는 미완료 그대로. 네 칸 명부/목표 문턱은 변경0.

## 2. LHS 수령 준비 유지

O1은 현재 덱 신원만이며 원 명령 SHA2026d61bb920599ca95870b62b8aee9ed3345f288da21ed4ff090a0064e0b8a3를 다시 대조했다. 기존11키 양식/10사례가 있어 중복 parser/새 현장 명령을 만들지 않았다. 실제관측/원본rc/작성명령 신원은 미수령이다.

현재 신원·비결과 메타 뒤에도 원로그본문·값·실행당시 include/재개 사슬·정본/구간·A/C·동결·값GO는 자동 승인되지 않는다. A→B→A 한정 유지. 실제 출력이 오면 기존 빈칸/분기로 처리하며 가상 현장 결과를 채우지 않는다. 전체 HOLD.
