# 첨가제 테스트 캠페인 — input_6mAh_real_4 (ball-mill, step-by-step)

첨가제(VGCF / Super P / PTFE)를 넣었을 때의 물리가 **실제 MPM 구조와 맞는지** 조건별로
검증하고 전부 기록한다. 차근차근: 한 조건 GPU run → 예측 대조 → CSV에 측정값 기록 → 다음.

데이터: `docs/data/additive_test_campaign_6mAh_real_4.csv` (예측 14조건 + 측정칸).

## 베이스라인 (첨가제 0)
porosity **MPM 15.45 % / DEM 14.28 %** · thickness 113.4 µm · SE/solid 33.2 % ·
σ_ionic 0.108 (Physics) / 0.182 (Hertz) mS/cm · σ_e 4.37 mS/cm · 126 AM_P + 1372 AM_S + 158,688 SE.

## 예측 (volume-fill, ball-mill) — CSV 전체
첨가제 = 고체부피 → void 채움 → porosity ↓. `Δpor = −(첨가제 부피)/(box 부피)`.
같은 wt%면 세 첨가제 모두 비슷 (volume-fill은 밀도 주도, 첨가제 종류 무관).

| 조건 | wt% | n_objects | vol%_solid | Δpor (%p) | porosity_pred |
|---|---|---|---|---|---|
| VGCF | 1 | 26,696 | 1.94 | −1.66 | **13.79** |
| VGCF | 2 | 53,936 | 3.92 | −3.36 | 12.09 |
| VGCF | 4 | 110,120 | 8.01 | −6.86 | 8.59 |
| Super P | 1 | 1,185,506 | 2.04 | −1.75 | 13.70 |
| Super P | 2 | 2,395,205 | 4.13 | −3.54 | 11.91 |
| PTFE | 1 | 2,184 | 1.76 | −1.51 | 13.94 |
| PTFE | 2 | 4,413 | 3.56 | −3.06 | 12.39 |
| VGCF+PTFE | 1+1 | 29,174 | 3.74 | −3.21 | 12.24 |
| Super P+PTFE | 1+1 | 1,199,809 | 3.85 | −3.30 | 12.15 |
(0.5 wt% 행은 CSV 참조)

⚠ 예측 = volume-fill 1차 추정. MPM 재압축으로 ±~0.5 %p 가능. 통과 기준 = |예측−측정| ≤ 0.5 %p.

## 각 조건이 검증하는 것
- **porosity** (이번 단계): 첨가제 부피만큼 실제로 줄었나 → zip→MPM volume-fill 물리 확인.
- **morphology**: VGCF 섬유 / SuperP 응집 / PTFE 섬유망이 자연스럽게 깔렸나 (도전재 3D).
- **σ_e / σ_ion** (STEP 3, network 확장 후): carbon 전자경로↑ / SE점유 σ_ion↓ → 실측 대조.

### 형상 메모 — VGCF waviness (2026-06-30)
이전 VGCF는 완벽한 직선(curl=0)이라 뷰어에서 artifact처럼 보였음.  실제 VGCF(기상성장
탄소섬유)는 SEM상 곧은 막대가 아니라 **본질적으로 물결치는(wavy)** 필라멘트 → `mpm3d_compaction.py`
ADD dict의 VGCF `curl 0.0 → 0.06`(gentle as-grown waviness; PTFE 0.4=tangled과 구분).
- **porosity 검증에 영향 없음**: curl은 경로 모양만 바꾸고 per-point 부피(`add_pvs·w`)는 보존 →
  volume-fill porosity·예측(13.79%) 불변.  STEP 1 이후 GPU 코드 pull 후 재-run하면 형상만 개선됨.
- **지름 균일 유지**: `vol_conserve`를 `vcv>0`에만 묶어(drawing=PTFE 전용) VGCF는 curl을 줘도
  제조상 일정 Ø(150nm) 유지.  `curl`은 grid step 단위라 waviness ∝ curl·√(L/step) — n_grid에
  따라 약간 민감, 너무 곧/과하게 꼬이면 curl만 튜닝.
- 가압 중 휨: VGCF는 최강성 상(E=10≫SE 1.53, σ_y=2.0≫0.3 가압)이라 거의 탄성·평행이동;
  MPM에 굽힘(beam) 항이 없어 능동적 좌굴은 미표현 → 압축 후 추가 휨은 SE 흐름에 의한 수동
  왜곡뿐.  좌굴까지 보려면 fibre beam/bond 모델이 필요(차후 검토).

## 실행 로그
| # | 조건 | mixing | por_pred | por_meas | thick_meas | 판정 | 비고 |
|---|---|---|---|---|---|---|---|
| 1 | VGCF 1 wt% | ball-mill | 13.79 | (run 중) | | | STEP 1 시작 |

(각 run 후 이 표 + CSV의 meas_* 채움)

## 순서 (합의)
1. **porosity/구조 검증** (이 캠페인, ball-mill) ← 지금
2. **A4** (SE-coating seeding — thinky-SuperP 구조)
3. **network** (carbon phase → σ 계산 → σ_e/σ_ion 실측 대조)
