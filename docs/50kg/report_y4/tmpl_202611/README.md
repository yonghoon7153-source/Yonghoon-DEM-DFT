# 50kg 4차년도 보고 덱 — 2026.11 양식 DEM 장 생성기 (2026-11-02)

1저자 양식 덱 (리포 밖 · 읽기 전용 · 18 장) 에 DEM 장을 채운다.  양식의 글꼴 · 스타일 · 이야기는 그대로, 값만 우리 것.
양식 · 렌더 이미지는 리포에 넣지 않는다 — 인자로 받는다.

## 만들기
```
python3 docs/50kg/report_y4/tmpl_202611/build_tmpl_dem.py \
  --template <양식.pptx> --d1-fig <D1 가압 3단 그림 (다시 만든 그림이면 그 경로)> \
  --stage-frames docs/50kg/report_y4/figs/d1_compaction/stage_frames_d1.csv \
  --render-init <가압 초기 렌더> --render-50 <50 MPa 렌더> --render-300 <300 MPa 렌더> \
  --skill-dir <pptx skill 폴더 (scripts/add_slide.py · clean.py)> --work-dir <W> --out-dir <O> \
  --values-csv docs/50kg/report_y4/meeting_20261104/values/values_D123.csv \
  --metrics-modulus <metrics_modulus.csv (D2 · D2E05 · D2E15)> \
  --tau-geo-json <metrics_D2E05.json> docs/50kg/report_y4/draft2/data/D2/metrics_D2.json <metrics_D2E15.json>
```
값 대조 (`--values-csv` · `--metrics-modulus`) 가 어긋나면 덱을 만들지 않고 멈춘다.

## 장 (27 장 · 입도 절 → 영률 절)
| 덱 | 내용 | 양식 |
|---|---|---|
| 1–5 | 양식 그대로 | 양식 1–5장 |
| 6 | DEM 가압 거동 (D_SE = 1 µm) — 두께 · 판 속도 · 측정 압력 3단 + 기공 렌더 넷 (After relaxation = 빈 칸) · 렌더 침대 높이 ∝ 가압판 높이 (바닥 맞춤) | 새 장 (5장 복제) |
| 7 | 입도 1 / 2 / 3 µm — 렌더 · 경로 그림 = 같은 자리 빈 칸 (옛 자료 그림 뺌) · 경로 칸 옆 기하 tortuosity · 두께 · 기공도 막대 | 양식 6장 |
| 8–11 | 입도 절: 미세구조 비교 (넷째 칸 = Geometric tortuosity) · 지표 변화 · 응력 분포 (이완 후) · 이온전도도 변화 | 새 장 |
| 12 | E_SE = 11 / 22 / 33 GPa — 렌더 칸 비움 · 수송 tortuosity · 두께 · 기공도 막대 | 양식 7장 |
| 13–16 | 영률 절: 같은 네 장 | 새 장 |
| 17–27 | 양식 그대로 | 양식 8–18장 |

- 양식 6 · 7장의 막대는 Origin 9.5 OLE 그림 (값을 못 고친다) → 같은 자리 · 크기의 PNG 로 바꿨다.  Origin 으로 다시 그릴 CSV 를 그림마다 함께 쓴다 (`<O>/figs/`, 파일 이름 앞 = 덱 장 번호).
- 6장 기공 렌더: 웹앱 렌더는 침대마다 화면에 맞춰 확대돼 있다 (침대 높이 785 / 768 / 766 px) → 렌더마다 침대 bbox 를 재고, 장에서의 침대 높이를 가압판 높이 (stage_frames_d1.csv recommended 줄: 144.9457 / 136.9457 / 122.9457 / 122.5957 µm) 에 비례하게 · 집전체 쪽 바닥을 맞춰 놓는다 (가로세로 비 그대로).  빈 칸 (After relaxation) = 122.5957 µm 높이.
- 왼쪽 그림 = `--d1-fig` 경로 그대로 (2.15 × 3.42 in 상자 안에 비율 유지) — 다시 만든 그림은 경로만 바꿔 다시 돌리면 된다.
- 점선 사각형 = 1저자가 웹앱 렌더를 붙일 이미지 칸.  이온전도도 장 색 막대의 최댓값 칸은 비워 둔다.
- 경로 그림 (최단 경로) 옆 · 미세구조 비교 장 넷째 칸 = 기하 tortuosity.  수송 tortuosity 는 지표 변화 장 막대와 7 · 12장 글머리에만.

## 값 · 출처
- 입도 절 = `docs/50kg/report_y4/meeting_20261104/values/values_D123.csv` (= `docs/50kg/report_y4/draft2/metrics_all.csv`).
- 영률 절 = D2 + 영률 침대 기록 (`metrics_D2E05.json` · `metrics_D2E15.json` 의 `metrics`).  E_SE = 22 GPa 의 ×0.5 / ×1 / ×1.5 (DEM 유효 입력 0.675 · 1.35 · 2.025 GPa).
- 기공도 = 정확 합집합 · 두께 = 질량 보존 · 수송 tortuosity = φ_SE·σ₀/σ_eff (제곱근 아님) · σ_Li+ = f × 1.5 mS/cm (Hertz).
- 기하 tortuosity (최단 경로 / 두께) = 입도 1.22 / 1.28 / 1.37 (values_D123.csv) · 영률 1.28 / 1.28 / 1.30 (`tau_geo_all` 1.2831 · 1.2764 · 1.2964).
- 반올림: 두께 E_SE = 11 GPa 는 기록 123.6147 → **123.61** · 3 µm 수송 tortuosity 는 13.6283 → **13.63**.
