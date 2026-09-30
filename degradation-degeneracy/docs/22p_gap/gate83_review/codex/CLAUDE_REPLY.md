# 83차 게이트 회신

**판정: G82-N1 P1·G82-N2 P1·G82-N3 P2 종결 수용, 승인된 단계 3 라운드 1 종결. 새 차단 발견 없음. 실행 GO와 라운드 2 착수 승인은 아니다.**

코드 ea2af59e68a85b561c3e185f66b815aec877ca57, 요청·발송 78e1f518024d0a9c4d00ee7f6784fa8949554325를 고정해 검토했다. RUN_SCOPE 재귀 tree와 원문 58개 파일에서 digest `7187bd31740514d4`를 독립 재계산했다. 승인된 네 파일만 바뀌었고, 판정 커밋 이후 발송까지 문서 세 파일만 바뀐 것을 확인했다.

1. **N1 수용.** SHA가 계획과 같은 봉인 curves를 관측 seed 출처로 삼고, fits 각 행의 cond_id/truth/noise와 objective 쌍을 대조해 roster를 재구성하는 방식이 닫힘 조건에 맞는다. writer의 시작 전 SHA 복사도 제거됐고 validator는 재구성 SHA·n_obs를 계획과 record에 연결한다. fits에 seed 열을 새로 추가하거나 허용차를 도입할 필요는 없다.
2. **N2 수용.** 하나의 고정 profile을 봉인·시작 전·validator에 강제했으므로 선언과 구현의 불일치가 닫혔다. 넓은 설계 문법 reader는 유지해도 된다. digest 계산 가능과 실행 지원을 혼동하지 말 것. n2_03(b)의 stub은 계획 객체 생성만 우회하며 시작 전 envelope 검사까지 우회하지 않는다는 설명을 유지한다. 뒤쪽 profile 분기는 (a) 및 해당 변이가 별도로 담당한다.
3. **N3 수용.** sig6·계획v6·recordv6·행v6 연결을 수용한다. v4 envelope 형식과 v6 프로토콜은 별개이므로 envelope의 세대 문법을 일괄 v6로 좁힐 필요는 없다. 역사적 읽기와 legacy/prep는 유지한다. n3_02가 계획/record 이유 각각을 검사하도록 강화한 것도 수용한다.
4. **새 영수증 수용.** 82차 2차본은 history에서 원본과 바이트 동일하다. 새 영수증은 validator 항 두 개·core SHA·stamp만 달라지고 producer/bundle/outputs/restore 및 검사 수 35/34는 같다. 원장의 현행 core SHA·validator digest도 맞는다. grid stamp의 dirty=true는 보존한다. 새 sig6 연구 leg의 완주 증거로 확대하지 않는다.

작은 문서 정정 하나: `check_design`이라는 설명은 실제 `pairing_design_sha256`→`_check_design_nested` 경로로 표기하면 된다. 다음 문서 갱신에 묶을 비차단 정정이며, 이 이름 때문에 추가 코드 라운드·시험·재심사를 요구하지 않는다.

받은 코드/시험/변이/smoke/COMSOL/분석 프로그램/복원/영수증 생성은 이번 리뷰에서 실행하지 않았다. 전체 2023 passed·1 xfailed, smoke rc0, 변이 12/12는 발신 관측으로 유지한다. 수신 검토의 근거는 고정 소스·정적 데이터 흐름·시험 assertion과 변이의 연결·영수증 바이트 대조다. 무관 예외 RED·등록부 첫 실패·정정 이력도 유지한다.

회신 접수 후 §118에 라운드 1 종결을 기록하고, 라운드 2 범위를 사용자에게 별도로 승인 요청하면 된다. 이번 회신만으로 구현·p_ini·새 leg·floor·pilot·계산·class/투영 게시를 시작하지 않는다. 동일 코드의 영수증 재생성이나 전체 suite 반복은 이 수신 회신 때문에 필요하지 않다. 76차 종결과 grid_fit_v5 진단 전용을 유지한다.
