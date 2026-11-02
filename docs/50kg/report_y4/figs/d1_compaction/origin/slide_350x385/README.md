# D1 압밀 곡선 — 슬라이드 칸 크기 Origin 판 (1저자 11-03 *"이 사이즈로 origin 도 만들꺼니까 준비해놔"*)

6장 왼쪽 칸 = **3.50 × 3.85 in (8.89 × 9.78 cm)** · 1:1 로 붙인다 (생성기 `--figsize 3.5 3.85` 미리보기와 같은 크기).

| 항목 | 값 |
|---|---|
| 패널 그림 영역 (셋 같음) | 폭 6.89 cm (2.713 in) × 높이 2.40 cm (0.945 in) |
| 패널 사이 | 0.43 cm (0.17 in) · 위 패널 위 = "Particle packing" 자리 0.53 cm |
| 글씨 | 눈금 9 pt · 축 이름 9.5 pt · 단계 이름 9 pt 회색 (154,160,168) |
| y 이름 | 두 줄 — `Plate velocity` / `(µm s⁻¹)` · `Measured pressure` / `(MPa)` (GUI) · `Thickness (µm)` 한 줄 |
| x | 0–2800 ms · 500 간격 · 맨 아래 패널만 숫자 · 이름 `Time (ms)` |
| 선 | 곡선 0.8 × 2 pt (`set -w 800`) · 축 1 · 경계 점선 셋 (200.002 · 400.002 · 2685.002 ms) |

- `.ogs` = 상위 폴더 `.ogs` 에서 그림 영역 · 글씨 · 선 굵기만 바꾼 것 (`../make_slide_ogs.py` · 값 · 범위 · 색 그대로).  ⚠ Origin 실행 확인 안 함 (이 기계에 Origin 없음).
- CSV = 상위 폴더 그대로 (`d1_ms_thickness_plate.csv` · `d1_ms_plate_velocity.csv` · `d1_ms_pressure_slide.csv`).
- 원자 기준 두께 (Particle packing 포함) = bml CSV 가 오면 `d1_ms_thickness_atomtop.csv` + 이 크기 `.ogs` 를 더한다.
