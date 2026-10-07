# Origin 그래프 가이드 — ps_7_3_r45 압밀 곡선 (시간–두께 · 시간–압력) · BML 표준 + Aptos

- 그래프 2 개 = 워크북 하나씩: `ps73_time_thickness` · `ps73_time_pressure` (만든 곳: `../make_fig.py` — 원자료 `../raw/` 두 tgz).
- 서식 = 10-21 덱 그래프와 같은 BML 표준 (`docs/report_20261021/origin/GUIDE.md` §0 · §2 — 바깥 틱 · 위/오른쪽 축선 · #404040 · 레이어 10 × 8 cm · 틱 라벨 Aptos 28 pt).
- 미리보기 `../previews/*.png` (이 기계에 Aptos 가 없어 Liberation Sans) 를 Origin 결과로 바꿔 끼운다.  두 그래프는 **같은 크기**로 둔다.

## 가져오기 · 스크립트

| 단계 | 클릭 경로 | 설정 |
|---|---|---|
| 1 | `ps73_time_*.csv` 를 Origin 에 끌어 놓기 | Header Lines: **Long Name = 1 줄 · Units = 2 줄** · Data Start = 3 줄 |
| 2 | 워크북이 앞에 있는 상태에서 Window > Script Window → 같은 이름 `.ogs` 붙여넣기 → 마지막 줄에서 Enter | 새 그래프 + 서식 + 단계 경계 점선 둘 (압축 시작 0.400002 · 이완 시작 3.125) · 압력 그래프는 300 MPa 점선 |

## 그래프별

| 그래프 | 열 | 축 | GUI 마무리 |
|---|---|---|---|
| 시간–두께 | A Simulation time (s) · B Thickness (µm) — 판 메시 5,000 step (= 0.005 s) 간격 605 점 | X 0.2–3.25 · Y 108–142 | 단계 이름 (Insert > Text, Aptos 20 pt, 회색): 0.2–0.4 "Stabilization" (세로, **아래쪽** — 판 높이 선과 겹침 방지) · 0.4–3.125 "Compression" · 3.125–3.25 "Relaxation" (세로) |
| 시간–압력 | A Simulation time (s) · B Pressure (MPa) — thermo 1,000 step (= 0.001 s) 간격 3,274 점 | X 0.2–3.25 · Y 0–330 | 단계 이름은 위와 같되 "Stabilization" 은 **위쪽** · "Target 300 MPa" 글은 안정화 점선 오른쪽 · 이완 구간의 진동 (123.8–204.6 MPa) 은 그대로 둔다 (실제 자료) |

- 축 제목 글꼴: 제목 더블클릭 → Ctrl+A → Aptos 34 pt · #404040 (10-21 GUIDE §2 와 같음).
- X 축 제목 = **Simulation time (s)** — 시뮬레이션 시간 = step × 1e-6 s (1저자 10-07 · 축척 덱이라 실제 압착 시간 아님 · `../README.md` §5).  숫자는 옛 Step (×10⁶) 축과 같다 —
  옛 step 그래프가 이미 있으면 X 축 제목만 바꿔도 된다.
- 단계 경계 점선이 안 보이면: Graph > Add Straight Line → X = 0.400002 · 3.125 (점선 · 회색).
- **슬라이드판** `ps73_time_pressure_slide.csv` (3,274 점) — 같은 `ps73_time_pressure.ogs` 로 그린다 (이 CSV 를 가져온 워크북을 앞에 두고 붙여넣기).  압축 끝 (3.125) 까지 원값 · 그 뒤 이완 구간 = **모식 감쇠** (τ 15,000 step = 0.015 s · 끝 값 165.3 MPa 만 계산값 · 1저자 10-06 밤 실선) — `../README.md` §5.
