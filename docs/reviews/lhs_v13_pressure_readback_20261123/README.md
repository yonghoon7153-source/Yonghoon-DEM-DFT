# LHS v1.3 압력 재고 · WSL30

| 구분 | 범위 | 결과 |
|---|---|---|
| 11-23 1저자 실행 GO | WSL의 lhs00_100–129, 케이스당 정해진 로그 두 개 | 새 현장 결과 대기 |
| 11-08 보존 재고 | 30케이스·60로그. 30쌍 모두 B7 해당 줄 수가 같고 파일 크기는 달랐다 | 이번 관측과 독립적으로 보존 |
| 11-16 O1 | 30개 현재 덱 SHA256이 당시 코호트 목록과 일치 | 실행 당시 입력 신원 미확정 |
| 11-18 출처 회신 | NONE_KNOWN | 정본과 구간 미선택, §5 및 τ 미판정 |

## 1. 1저자 WSL 명령

전달 TXT PASTE_LHS_V13_PRESSURE_INVENTORY_1123.txt를 Bash로 실행하고 인자로 GO_LHS_WSL30_PRESSURE_INVENTORY_ONCE 하나를 준다. 기존에 독립 검토한 스캐너(파일 SHA256 2305bd2194b29ac5439008906a17b1c673968a59fd52dcdde35b03ff4da20634)의 원바이트를 블록 안에 담았다. 실행 때 재검증하고 WSL 모드만 호출한다. 별도 스크립트 설치나 이전 홈 폴더 사본은 필요 없다.

WSL 로컬 1코어. 현장 소요시간 미측정. 원 명령의 시간 상한 없음과 자동 재시도 0을 유지한다. 스캐너가 두 로그를 행 단위로 검사해 B7 문법 일치·형식 불일치·두 재개 표시 줄 수와 파일 크기를 센다. 해당 .out은 이름과 일반 파일 개수만 확인한다. 압력·목표·N의 값이나 본문, 덱·include·restart 내용의 수집 범위는 0이다. 원 자료 디렉터리는 읽기 전용이다. 1저자 홈의 새 반환 폴더에만 ZIP을 쓴다.

끝 화면의 RETURN_ZIP과 SHA256을 함께 보낸다. 성공은 SCANNER_RC=0, INVENTORY_STATUS=INVENTORY_COMPLETE, COMMAND_RC=0과 30개 고정 case·60로그 전체 구조 확인이다. 숫자 항목은 줄 수와 파일 크기 등 재고 메타뿐이다. 누락·변경·심볼릭 링크·거부·잘린 출력·추가 키가 있으면 완료로 받지 않는다. 이때 반환 가능하면 INCOMPLETE 영수증과 해시만 담고 부분 행이나 원문은 담지 않는다. WSL 신원 확인 전 실패했거나 디스크에 쓸 수 없으면 정상 반환 ZIP이 없을 수 있다.

## 2. 반환 뒤 판독

실무 창이 화면 SHA와 ZIP 바이트, 내부 SHA256SUMS, 스캐너 지문·rc, 30개 케이스와 로그 60개의 이름·범위·정수 타입을 대조한다. 기존 11-08 메타와 다른 케이스는 별칭으로 기록한다. B7 해당 줄이 0이거나 두 로그의 수가 다르면 새 관측 그대로 보존한다. 기존과 같으면 두 시점에 관측된 메타가 같다는 뜻이다. 어느 경우에도 같은 실행·정본성·목표 압력 도달을 보증하지 않는다.

판독기 = docs/reviews/lhs_v13_pressure_readback_20261123/check_return.py. 인자 순서는 반환 ZIP, 화면의 SHA256, docs/data/lhs_wsl30_inventory_20261108/lhs_wsl30_inventory_received_20261108.json이다. 선택용 보존 재고 블록 PASTE_LHS_PRIOR_RECEIPTS_1123.txt는 이전 고정 JSON 다섯 개만 재판독하며 새 WSL30 재고는 위 첫 블록에서 받는다.

## 3. 다음 결정

실행 당시 덱·include·재개 사슬과 각 로그의 run/segment를 잇는 동시기 영수증이 생기면 그 출처부터 확인한다. 이후 정본(log.liggghts 후보, log.txt 대조), 명부·쌍·종점·필드·담당·노출 기록을 동결하고 값 GO를 따로 받는다. 그때까지 A/C, §5 압력 자격, τ는 미판정이다. ibb184 및 전체214 재고, production194와 supp20 배치의 봉인 감사·재판독, v1.3 생성·배포는 이 GO 범위 밖이다. 배포 후보에는 ‘탈압 전 값’과 ‘모델 내부 ML 기술자’를 명시하고 전달본을 한 번 독립 검토한다.

근거는 docs/data/lhs_wsl30_inventory_20261108/README.md, docs/data/lhs_o1_current_identity_20261116/README.md, docs/reviews/nonrint_development_returns_20261118/lhs_v13_author_source_lead.json, docs/reviews/lhs_v13_preparation_20261118/README.md, docs/reviews/lhs_release_v13_plan_20261007.md §2b와 docs/reviews/lhs_network_batch_registration_20261007_g2.md §5이다.

## 4. 로컬 재현

make_live_block.py와 make_operator.py는 각각 리포 폴더와 새 출력 파일명을 받아 B 기준 커밋 9352c4ece10a64a04ffd620062894bd616589582의 고정 바이트에서 TXT를 만든다. 두 TXT의 SHA256은 차례로 ed58e9bd6c0c8f0a0014de69a4071957c4bff61491d63d20d260452eff833eb8, c17bcd57759a1eb54bd8b1812942832d4c526758c03bbab0384a79d73ec80dda이다.

실무 준비 단계에서 실제 로그 열람·현장 실행 0회. 로컬 수치 및 오류 계약 합성 5/5, 모의 스캐너를 넣은 전체 블록·ZIP 재판독 2/2, 보존 입력·변경 방지 5/5. 두 WSL TXT는 bash -n 통과. 현재 WSL과 동일한 현장 성능·권한은 미측정이다.
