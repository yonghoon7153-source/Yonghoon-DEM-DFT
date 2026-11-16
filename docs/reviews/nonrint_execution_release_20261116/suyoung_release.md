# 수영 S/F 형상 출력 — 커밋 판 전달

## 1. 구현과 보존

핀 `c759c4c7ab7abec2148e23fa231d004c1d4d0fec`의 변경은 `scripts/dem_suyoung_sf2d_dev.py`와 `scripts/test_dem_suyoung_shape_output.py` 둘뿐이다. 검토했던 로컬 바이트와 같다.

누적 변형 지도 F_total은 관측기에만 쌓는다. 물리 상태·힘 계산에는 돌려주지 않는다. 물질점 위치, 입자/물질점 번호, 탄성 F, 누적 F_total, 시각과 step을 실제 관측 시점의 NPZ로 저장한다. SVG는 운반된 물질점 셀의 사각형을 그리며 보간·재시드·볼록껍질을 만들지 않는다. 겹친 사각형 면적의 합을 공극률로 해석하지 않는다.

기본 물리 커널 10함수 AST 보존, 출력 켬/끔의 trace 바이트 및 마지막 240 step 평균의 비트 동일, F_total을 7배로 오염시킨 관측기의 힘·상태 비되먹임, ID 및 step 보존은 `scripts/test_dem_suyoung_shape_output.py`가 확인한다. 전체 출력 계약은 `docs/reviews/suyoung_shape_preparation_20261116/output_schema.json`을 따른다.

## 2. 전달 블록

외부 파일명: PASTE_SUYOUNG_SHAPE_WSL_CPU1_20261116.txt. 실행 핀과 소스 tar SHA256을 원문에 고정하고 RELEASE_BOUND=YES로 표시했다. 고정 tar는 Git blob 3개와 manifest 하나이며 작업 트리 덮어씌움은 없다.

| 항목 | 고정 내용 |
|---|---|
| 기계·자원 | 1저자 로컬 WSL · CPU1 · 기존 프로젝트 venv의 NumPy · 설치/업데이트 없음 |
| 순서 | S 다음 F · 각 팔 별도 프로세스 · S 실패 때 F 시작 안 함 |
| 입력 | 작은 합성 침대 · grid32 · steps1200 · dt0.0005 · wall_speed0.15 · friction0.20 |
| 시간 | 팔당 600s TERM, 10s 뒤 KILL 정리 · 자동 재시도 0 |
| 출력 | 각 팔 trace · summary · NPZ/SVG 12프레임(0,1,120,…,1200) · frame hash manifest · 합친 요약 |
| 합친 요약 | 양팔 완결과 출처를 확인한 뒤 두 평균의 비 · 이전 2.47을 새 결과로 재사용하지 않음 |
| 회수 | 원 작업 폴더 밖의 새 반환 폴더에 tar · command_rc/archive_rc · SHA256 |

이전 양팔 개발 런의 보고 시간 약 8.3s는 참고일 뿐이며 형상 I/O가 더해진 이번 실측 시간은 미정이다. 산출물은 개발 자료다. 새 물리 판정이나 형상 기반 union 공극률 자격을 부여하지 않는다.

## 3. 검사

커밋 blob을 별도 폴더로 꺼내 새 14/14 및 기존 9/9를 다시 통과했다. Windows Python3.12.14/NumPy2.3.5, 합성 입력이며 WSL/현장 재실행이 아니다. 이전 red는 동일 14메서드에서 failure 관측16/오류0였으며 subtest를 고유 메서드 수로 합산하지 않는다. 이번에 red를 다시 실행하지 않았다.

전달 tar 4파일·manifest3/3, ASCII 블록·Bash 문법, 내장 Python 두 조각 AST를 확인했다. 결과 tar는 입력 디렉터리 밖에 작성하므로 앞선 자기 포함 tar 문제를 반복하지 않는다.
