# 50kg 보고 덱 DEM 장 최종 (11-03 · 1저자 덱 `50kg_report_DEM_slides_1.pptx` 위)

1저자 11-03: *"DEM 부분 다 수정해서 넣자"* · *"geometric tortuosity 안 넣을 거고 수송 tortuosity 넣을 거고 tortuosity 로만"* · *"사진들 내가 준 것 활용하거나 공백으로"* · *"origin 으로 바로 그림 그릴 수 있게 값들도"* · *"다 최종본으로"*.

`finalize_dem_deck.py` (인자 = 원 덱 · 출력 · 차트 폴더 · 그림 폴더 · 리포 · 6장 한 장 덱 · 6장 압밀 곡선 그림) 가 바꾼 것 — 나머지는 1저자 덱 그대로 (덱 파일 39 MB = 리포 밖):

| 장 | 바꾼 것 |
|---|---|
| 6 | 1저자 한 장 덱 `50kg_p06_compaction_1.pptx` 으로 바꿔 끼움 (글머리 2줄 · 압밀 곡선 칸 3.50 × 3.85 in · Particle packing) · 압밀 곡선 = 위 · 오른쪽 축선 없는 판 (아래 명령) + 노트 (1 µm 질문 대비 = 감쇠 항력 상당 65 % · 원장 KG50-20 · Origin 시트) |
| 7 · 11 | 'Transport tortuosity' 라벨 셋 → 'Tortuosity' · 글머리 '수송 tortuosity' → 'tortuosity' · 11장 22 GPa 구조 칸 = 2 µm 같은 침대 그림 · 값 아래 tortuosity 경로 그림 칸 셋 (1저자 11-03 *"여기에 tortuosity도"* · 22 GPa = 31 · 11 · 33 GPa = 점선) · 노트 |
| 8 | 'Geometric tortuosity' → 'Tortuosity' · 값 1.22 / 1.28 / 1.37 (기하) → 6.00 / 8.26 / 13.63 (수송) · Structure · Pore · Tortuosity 칸 = 1저자 그림 (웹앱 캡처 27–32 · pore3d) · Coverage = 공백 |
| 12 | 같은 라벨 · 값 1.28 / 1.28 / 1.30 → 7.80 / 8.26 / 9.05 · 22 GPa 칸 = 2 µm 같은 침대 그림 · 11 · 33 GPa = 공백 |
| 9 · 13 | 글머리 '수송' 뺌 · tortuosity 막대 그림 = 세로축 'Tortuosity' 로 다시 (값 같음 · `p09_tortuosity_DSE.png` · `p14_tortuosity_ESE.png`) |
| 7 · 9 · 10 · 11 · 13 · 15 | 막대 그림 12 개 전부 = 위 · 오른쪽 축선 없는 판 · 끊긴 축 표시 = 왼쪽만 (`docs/50kg/report_y4/tmpl_202611/build_tmpl_dem.py` · 값 · 크기 · 자리 그대로 · 1저자 11-03 *"우측, 위측 테두리는 없애줘 그게 우리 표준이야"*) |
| 14 | 응력 지도 여섯 칸 (`figs/stress_maps/modulus_*` · 이완 끝 · 웹앱 질감 · 판 · 바닥 접촉 입자 뺌) |
| 10 · 15 | 노트 (Origin 시트) |

`50kg_DEM_origin_data.xlsx` · `origin_data/*.csv` = 덱 차트마다 시트 하나 (1행 이름 · 2행 단위 · Origin 가져오기 꼴) — p06 D1 압밀 (시간 축 셋 · XY 쌍) · p07 · p12 두께 · 기공 · p09 · p14 기공 · tortuosity · coverage · p11 · p16 σ_Li+ · p14 응력 (중앙값 · p10 · p90 · 판 압력).
tortuosity = φ_SE·σ₀/σ_eff (수송 · 제곱근 아님) — 화면 이름은 'Tortuosity' 만 (1저자 11-03).

**다시 만들기 (11-03 열린 틀 판)** — 막대 그림 12 개 = `python3 -I docs/50kg/report_y4/tmpl_202611/build_tmpl_dem.py` 의 차트 출력 (PNG · CSV) ·
6장 압밀 곡선 = `python3 -I docs/50kg/report_y4/figs/d1_compaction/make_fig_d1_ms.py --atomtop --figsize 3.5 3.85 --b3-contact --hi-span 45 --hi-frac 0.35 --preview-dir <폴더>` 의 `d1_ms_compaction_3panel_atomtop_slide.png` (옛 네 변 틀 = `--closed-frame`) ·
덱 = `python3 -I finalize_dem_deck.py <원 덱> <출력> <차트 폴더> <그림 폴더> <리포> <6장 한 장 덱> <압밀 곡선 PNG>` (덱 파일은 리포 밖).

**6장 기공 그림 — 1저자 한 장 덱 그대로 (11-03 검수)**: 네 칸 = 웹앱 기공 보기로 우리 D1 덤프를 찍은 것 (단계 프레임 = `docs/50kg/report_y4/figs/d1_compaction/stage_frames_d1.csv` 의 recommended — 450000 · 1250000 · 2650000 · 2785002) · 덱 칸 높이 비 1 : 0.95 : 0.85 : 0.85 (2.26 · 2.14 · 1.92 · 1.92 in) ≈ 가압판 높이 비 1 : 0.945 : 0.848 : 0.846 (144.95 · 136.95 · 122.95 · 122.60 µm).
⚠ 셋째 칸 (300 MPa) 과 넷째 칸 (After relaxation) 은 **같은 그림 파일** (sha256 `3a74d19a950a…` — 받은 덱에서부터) · 두 프레임의 가압판 높이 차 0.35 µm · ε_sphere 17.06 ↔ 16.83 % 라 눈으로는 거의 같지만 한 칸은 이름과 다른 프레임이다 → 2650000 (294 MPa) 을 따로 찍어 넣을지 = 1저자.
기공 보기는 격자 추정 그림이다 — 덱의 기공도 숫자 (7 · 9 · 11 · 13장) 는 정확 union 값 (그림에서 읽은 값 아님).
