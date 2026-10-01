# Origin 그래프 가이드 — 10-21 워크숍 덱 (한양대 DEM 파트) · BML 표준 + Aptos

- 그래프 8 개 (G1 · G2 · G3 · G4 · G5a · G5b · G6 · G7) = 워크북 하나씩.  데이터 = 이 폴더의 `Gx.csv` (만든 곳: `../make_figs.py` · 원자료는 리포 안).
- 서식 = BML 표준 (바깥 틱 major + minor · 위/오른쪽 축선만 · #404040 · 레이어 cm 단위) — **글꼴만 Aptos** (사용자 지정 · BML 기본 Arial/Calibri 대신).
- 덱에는 지금 미리보기 PNG (`../previews/Gx.png`) 가 들어 있다.  Origin 결과를 같은 자리에 **바꿔 끼운다** (복사 → 붙여넣기 · 그림 크기 = 패널 안쪽 약 11 × 8.7 cm).
- 색지도 · xyz · 3D 그림 (2-5 3D 구조 · 2-10 드럼 단면) 은 Origin 대상이 아니다 (웹앱 캡처).

## 0. 공통 — 가져오기

| 단계 | 클릭 경로 | 설정 |
|---|---|---|
| 1 | Origin 에 `Gx.csv` 를 끌어 놓기 (또는 Data > Import From File > CSV) | Import Wizard 가 열리면 다음 |
| 2 | Header Lines | **Long Name = 1 줄 · Units = 2 줄** · Data Start = 3 줄 |
| 3 | 워크북 이름 | `Gx` 로 바꿔 두면 찾기 쉽다 (Script 는 이름과 무관 — 활성 워크북을 쓴다) |
| 4 | 워크북이 활성인 상태에서 Window > Script Window → `Gx.ogs` 내용 붙여넣기 → 마지막 줄에서 Enter | 새 그래프가 생기고 서식이 들어간다 |

★ 스크립트는 **워크북이 앞에 있을 때** 실행한다 (`string bk$ = %H;` 가 활성 창 이름을 잡는다).  그래프가 앞에 있으면 엉뚱한 책을 찾는다.

## 1. 그래프별

| 그래프 | 덱 장 | 열 (A, B, …) | 모양 | 스크립트 뒤 GUI 마무리 |
|---|---|---|---|---|
| **G1** | 2-6 왼쪽 | A 대입자 몫 (X) · B P:S · C 공극률 union · D 구 부피 합 · E 두께 | DoubleY — 왼쪽 C (빨강 선+원) · 오른쪽 E (하늘 점선+네모) | X 눈금 글자를 P:S 로: 아래 축 더블클릭 → Tick Labels > Display = **Tick-indexed dataset** > Col(B) · 눈금 = 0, 0.3, 0.5, 0.7, 1.0 (Scale > Major Ticks = By Custom Positions) · 왼쪽 Y 15–22 · 오른쪽 Y 108–120 |
| **G2** | 2-6 오른쪽 | A 대입자 몫 · B P:S · C n · D 편차 · E 편차 (치밀 = 음수) · F 편차 (성김 = 양수) | 열 두 개 겹침 (E 하늘 · F 주황) | 막대 폭: 더블클릭 > Spacing = 30 % · Overlap 100 % · Y −22 ~ 17 · y = 0 기준선: Graph > Add Straight Line (Y = 0) · 값 표시: Plot Details > Label 탭 Enable |
| **G3** | 2-7 왼쪽 | A SE 부피분율 (점 X) · B 공극률 (점 Y) · C 구간 중심 · D 구간 중앙값 · E 구간 · F n | 점 (회색 빈 원) + 선 (빨강) | 회색 점: Symbol > Fill = None (빈 원) · X 5–75 · Y 0–32 · 범례 = "130 design points" · "Bin median" |
| **G4** | 2-7 오른쪽 | A 대입자 지름 · B 공극률 · C 구간 중심 · D 구간 중앙값 | 점 + 선 (하늘) | X 4–16 · Y 0–32 · 범례 G3 과 같게 |
| **G5a** | 2-8 왼쪽 | A·B = 130 관통 (SE %, 굴곡도) · C·D = 64 SE 과량 · E·F = 130 비관통 (SE %, 0.9 고정) | 점 셋 (하늘 원 · 주황 삼각 · 빨강 ×) | × 는 "경로 없음" 표시용 (굴곡도 값이 아님 — 범례 "No SE path (24)") · X 5–90 · Y 0.7–4.5 · SE ≤ 21 % 띠: Insert > Rectangle 연회색 (선택) |
| **G5b** | 2-8 오른쪽 | A·B = 130 (SE %, 고립 %) · C·D = 64 | 점 둘 | X 5–90 · Y −5–105 |
| **G6** | 2-9 오른쪽 | A VGCF wt% · B·C·D = 격자 0.15 · 0.20 · 0.25 µm 의 σ_e (원점 8 평균, mS/cm) | 선+기호 셋 · **Y 로그** (`layer.y.type = 2`) | X 눈금 1, 2, 3, 4 · minor 끔 · 범례 "voxel 0.15 µm" … |
| **G7** | 2-11 왼쪽 | A 런 (X, 글자) · B M · C 런내부 SD (Y 오차) | 열 + 오차 막대 | 색: L0 진회색 · LA 하늘 · LB 연청회 · LC 빨강 — Plot Details > Pattern > Fill = **By Points** 대신 막대 하나씩 클릭해 색 지정 · Y 0.85–1.05 · y = 1 점선 · 왼쪽 위 글: "Δ (LC − LA) = +0.001 ± 0.007" (Insert > Text, Aptos 20 pt) |

## 2. 축 제목 · 범례 글꼴 (LabTalk 로 안정적으로 안 됨 → GUI)

| 대상 | 클릭 경로 | 값 |
|---|---|---|
| 축 제목 | 제목 더블클릭 → Ctrl+A → Format 도구모음 | **Aptos 34 pt · #404040** (R 64 G 64 B 64) |
| 틱 라벨 | 스크립트가 넣는다 (Aptos 28 pt) — 안 바뀌었으면 축 더블클릭 > Tick Labels > Font | Aptos 28 pt |
| 범례 | 범례 더블클릭 → Ctrl+A | Aptos 24 pt · 테두리 없음 (우클릭 > Properties > Frame = None) |
| 그림 안 글 | Insert > Text | Aptos 20 pt · #404040 |
| 보기 배율 | View > Fixed Factor | 0.7 |

## 3. 덱에 넣기

1. 그래프 창에서 Edit > Copy Page → PowerPoint 의 미리보기 그림을 지우고 붙여넣기 (또는 File > Export Graphs > PNG 600 dpi).
2. 크기 = 탭 패널 안쪽 (가로 약 11 cm) · 그림 아래 회색 캡션의 "미리보기 — Origin (…) 으로 교체" 줄을 지운다.

## 4. 문제 해결

| 증상 | 원인 → 해결 |
|---|---|
| 스크립트가 `Range not valid` | 워크북이 아닌 그래프가 활성 → 워크북을 클릭하고 다시 실행 |
| 한글 열 이름이 깨짐 | Import Wizard 에서 File Encoding = **UTF-8** (파일은 BOM 있는 UTF-8) |
| G7 오차 막대가 안 보임 | Col(C) 우클릭 > Set As > **Y Error** → 그래프 지우고 다시 실행 |
| G1 오른쪽 축 서식이 안 들어감 | 오른쪽 레이어 (2) 를 클릭해 활성화한 뒤 스크립트 마지막 4 줄만 다시 실행 |
| Aptos 가 목록에 없음 | Office 2023 이후 설치본에 들어 있다 — 없으면 같은 자리에 Arial (BML 기본) |

## 5. 마무리 체크

| # | 항목 | 확인 |
|---|---|---|
| 1 | Fixed Factor 0.7 | ☐ |
| 2 | 축 제목 Aptos 34 pt · #404040 | ☐ |
| 3 | 틱 라벨 Aptos 28 pt · #404040 · 바깥 틱 (major 6 · minor 3) | ☐ |
| 4 | 위 · 오른쪽 축선 (틱 없음) — G1 은 오른쪽 축이 두께 축 | ☐ |
| 5 | 색 = BML 팔레트 (빨강 F14040 · 하늘 4FBDFF · 초록 52B788 · 주황 F4A261 · 회색 404040) | ☐ |
| 6 | 덱 캡션의 "미리보기 …" 줄 삭제 | ☐ |
