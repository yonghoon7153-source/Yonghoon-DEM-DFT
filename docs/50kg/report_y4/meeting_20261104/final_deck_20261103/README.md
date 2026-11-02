# 50kg 보고 덱 DEM 장 최종 (11-03 · 1저자 덱 `50kg_report_DEM_slides_1.pptx` 위)

1저자 11-03: *"DEM 부분 다 수정해서 넣자"* · *"geometric tortuosity 안 넣을 거고 수송 tortuosity 넣을 거고 tortuosity 로만"* · *"사진들 내가 준 것 활용하거나 공백으로"* · *"origin 으로 바로 그림 그릴 수 있게 값들도"* · *"다 최종본으로"*.

`finalize_dem_deck.py` (인자 = 원 덱 · 출력 · 차트 폴더 · 그림 폴더 · 리포 · 6장 한 장 덱) 가 바꾼 것 — 나머지는 1저자 덱 그대로 (덱 파일 39 MB = 리포 밖):

| 장 | 바꾼 것 |
|---|---|
| 6 | 1저자 한 장 덱 `50kg_p06_compaction_1.pptx` 으로 바꿔 끼움 (글머리 2줄 · 압밀 곡선 칸 3.50 × 3.85 in · Particle packing) + 노트 (1 µm 질문 대비 = 감쇠 항력 상당 65 % · 원장 KG50-20 · Origin 시트) |
| 7 · 11 | 'Transport tortuosity' 라벨 셋 → 'Tortuosity' · 글머리 '수송 tortuosity' → 'tortuosity' · 11장 22 GPa 구조 칸 = 2 µm 같은 침대 그림 · 값 아래 tortuosity 경로 그림 칸 셋 (1저자 11-03 *"여기에 tortuosity도"* · 22 GPa = 31 · 11 · 33 GPa = 점선) · 노트 |
| 8 | 'Geometric tortuosity' → 'Tortuosity' · 값 1.22 / 1.28 / 1.37 (기하) → 6.00 / 8.26 / 13.63 (수송) · Structure · Pore · Tortuosity 칸 = 1저자 그림 (웹앱 캡처 27–32 · pore3d) · Coverage = 공백 |
| 12 | 같은 라벨 · 값 1.28 / 1.28 / 1.30 → 7.80 / 8.26 / 9.05 · 22 GPa 칸 = 2 µm 같은 침대 그림 · 11 · 33 GPa = 공백 |
| 9 · 13 | 글머리 '수송' 뺌 · tortuosity 막대 그림 = 세로축 'Tortuosity' 로 다시 (값 같음 · `p09_tortuosity_DSE.png` · `p14_tortuosity_ESE.png`) |
| 14 | 응력 지도 여섯 칸 (`figs/stress_maps/modulus_*` · 이완 끝 · 웹앱 질감 · 판 · 바닥 접촉 입자 뺌) |
| 10 · 15 | 노트 (Origin 시트) |

`50kg_DEM_origin_data.xlsx` · `origin_data/*.csv` = 덱 차트마다 시트 하나 (1행 이름 · 2행 단위 · Origin 가져오기 꼴) — p06 D1 압밀 (시간 축 셋 · XY 쌍) · p07 · p12 두께 · 기공 · p09 · p14 기공 · tortuosity · coverage · p11 · p16 σ_Li+ · p14 응력 (중앙값 · p10 · p90 · 판 압력).
tortuosity = φ_SE·σ₀/σ_eff (수송 · 제곱근 아님) — 화면 이름은 'Tortuosity' 만 (1저자 11-03).
