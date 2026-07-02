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

### 형상 메모 — VGCF waviness = 압력-의존 buckling proxy (2026-06-30)
이전 VGCF는 완벽한 직선(curl=0)이라 뷰어에서 artifact처럼 보였음.  실제 VGCF(기상성장
탄소섬유)는 SEM상 곧은 막대가 아니라 **본질적으로 물결치는(wavy)** 필라멘트 + 슬렌더 컬럼이라
가압 시 **좌굴(buckling)**함(L/r~267, Euler σ_cr≈수십 MPa ≪ 가압 → 좌굴; SE에 박혀 단파장 wrinkle).
→ `mpm3d_compaction.py`에서 VGCF `curl`을 **press의 함수**로:
`_press_curl(P)=0.095·(1−exp(−P/0.30))` (`--vgcf-curl <0` = auto, ≥0 = 고정).  P 0.1→0.027 / 0.3→0.060 /
0.6→0.082 / 1.0→0.092 (단조·포화; 후좌굴 성장 후 densifying SE가 pin).  **압력 환경에 따라 형상 생성이 바뀜**(사용자 요청).
- **porosity 검증에 영향 없음**: curl은 경로 모양만 바꾸고 per-point 부피(`add_pvs·w`)는 보존 →
  volume-fill porosity·예측(13.79%) 불변.  STEP 1 이후 GPU 코드 pull 후 재-run하면 형상만 개선됨.
- **지름 균일 유지**: `vol_conserve`를 `vcv>0`에만 묶어(drawing=PTFE 전용) VGCF는 curl을 줘도
  제조상 일정 Ø(150nm) 유지.  `curl`은 grid step 단위라 waviness ∝ curl·√(L/step) — n_grid에
  따라 약간 민감, 너무 곧/과하게 꼬이면 `--vgcf-curl`로 튜닝.
- ★ **PRESCRIBED vs EMERGENT (정직)**: 위는 buckling의 *prescribed* proxy(seeding이 press에 반응).
  연속체 MPM은 sub-grid 섬유의 굽힘강성(∝두께³)을 격자로 못 풀어서(150nm fibre를 100µm box서 resolve =
  ~10⁹ cell, 불가) **emergent 좌굴은 안 나옴**.  진짜 emergent는 fibre 점에 **명시적 sub-grid Cosserat/
  bonded-rod**(축+굽힘 director DOF)를 얹어 기존 MPM 가압에 반응시키는 빌드 — MPM에서 가능(DEM은 가압
  불가→LAMMPS).  per-additive·coupling·CFL·sequencing은 backlog `digest_model_application_backlog.md`
  "F. Additive mechanics fidelity" 참조.
- σ_y 비대칭: SuperP(σ_y=0.1=100MPa<가압)·PTFE(0.05=50MPa<가압)는 이미 MPM서 소성 압밀=press 반응 *부분
  emergent*; VGCF(2.0=2000MPa≫가압)만 탄성유지라 prescribed curl이 필요한 유일 상.  → buckling 모델 가장
  필요한 건 VGCF.

## 실행 로그
| # | 조건 | mixing | por_pred | por_meas | thick_meas | 판정 | 비고 |
|---|---|---|---|---|---|---|---|
| 1 | VGCF 1 wt% | ball-mill | 13.79 | (run 중) | | | STEP 1 시작 |

(각 run 후 이 표 + CSV의 meas_* 채움)

## 순서 (합의)
1. **porosity/구조 검증** (이 캠페인, ball-mill) ← 지금
2. **A4** (SE-coating seeding — thinky-SuperP 구조)
3. **network** (carbon phase → σ 계산 → σ_e/σ_ion 실측 대조)

## ★ 실제 실험과 비교 — volume-fill 방향이 carbon에선 반대 (frame[4], 2026-07-02) ★
"사실 실제 현상도 엇비슷하게 나오나?"에 대한 정직한 답.  결론: **carbon 첨가제(VGCF/SuperP)에
대해 우리 volume-fill 예측과 실제 실험의 porosity 방향이 반대다.**

**직접 앵커 — Cho 2024** (`docs/data/cho2024_conflicting_roles_conductive_additive.csv`,
NCM811 + **우리와 동일한 LPSCl SE** + VGCF 2 wt%, 433 MPa 가압):
| 조건 (2 wt% VGCF) | 우리 volume-fill | Cho 2024 실측 |
|---|---|---|
| porosity Δ | **−3.3 %p** (15.45→12.11) | **+1 %p** (72wt%AM 0.14→0.15; 88wt%AM 0.18→0.19) |
| tortuosity | (변화 없음, 경로만) | **↑** (6.47→7.56, 17.41→18.34) |
| r_ele (전자저항) | (미계산) | **↓ 2.4–3.3×** (전자망 형성) |

⇒ 실제 VGCF는 porosity를 **거의 불변~살짝 증가**시킨다(우리 −3.3 %p 감소와 방향 반대).
이게 논문 제목 "conflicting roles" — **전자전도는 좋아지지만(r_ele↓) 밀도·tortuosity는
나빠진다(porosity↑)**.

**왜 반대인가 (물리):**
- 우리 volume-fill = 첨가제를 **수동적 void-filler(조밀 덩어리가 기존 공극으로 떨어짐)**로 가정
  → 부피만큼 porosity 감소.
- 실제 VGCF = **뻣뻣한 슬렌더 섬유(E≈200 GPa ≫ 300 MPa)** → 압밀을 *방해*하는 scaffold로
  구조를 벌려놓음(prop-open) + 자기 percolation 망을 형성 → 오히려 공극 유지/증가.
- SuperP도 고비표면(C65 BET 62 m²/g) fluffy 응집체 → 조밀 고체처럼 안 뭉침, 자체 내부 공극 추가.
- carbon은 저밀도(VGCF≈2.0/C65 1.60 vs AM 4.8) → 같은 wt%가 큰 vol% → 우리 모델선 큰 감소,
  실제론 그 큰 부피가 densify 안 되니 오히려 두께·공극으로 감.

**즉 이 캠페인이 검증한 것 vs 아닌 것:**
- ✓ 검증됨: **zip→MPM이 volume-fill을 정확히 구현**하는가 (내부 일관성; Δ≤0.045 %p PASS).
- ✗ 검증 아님: **volume-fill 가정 자체가 실제 carbon 거동과 맞는가** — 실제론 안 맞음
  (carbon은 void-filler가 아니라 compaction-resisting scaffold).

**frame[4] 관점:** 이 불일치는 실패가 아니라 **정량화된 모델 한계**(publishable).  volume-fill은
"조밀·연성 filler" 극한이고, 실제 carbon은 "압밀-저항 scaffold" 극한 → 실제는 후자.  실제 방향을
맞추려면 첨가제를 MPM에서 **하중을 견디며 압밀에 저항**하게 만들어야 함 = F1/F2 backlog
(emergent fibre mechanics, Cosserat/bonded-rod) — buckling이 "DEM-territory"인 것과 같은 이유
(수동 연속체가 못 잡는 discrete mechanics).

**보조 앵커 — Reisacher 2023** (`docs/data/reisacher2023_percolation.csv`, LPSCl+C65 매트릭스,
AM 없음): carbon 전자 percolation 임계 **~4 wt%**(matrix; cathode 환산 ~1.2 wt%).  그 아래선
isolated island(void에 들어갈 수도 있으나 여전히 밀도-주도 아님) → 우리 σ_e STEP 3 검증용.

⚠ 캐비엇: Cho는 433 MPa·AM 72/88 wt%(우리 300 MPa·다른 조성)라 1:1 오버레이는 아니다.  하지만
**SE가 동일(LPSCl)하고 VGCF 방향이 견고**하므로 "방향 반대"는 신뢰.  깨끗한 porosity-vs-wt% 실측
스윕은 아직 없음(Cho는 0/2 wt% 두 점, Reisacher는 전도도 스윕) → 직접 곡선 오버레이는 미보유.
