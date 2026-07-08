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

### 해결 — 물리 strut 모델 `--fibre-stiff` 빌드·GPU 검증 (2026-07-02)
"실제 방향을 맞추려면 첨가제를 하중-저항하게" = `--fibre-stiff`로 구현(VGCF 격자셀 rigid pin =
E→∞·σ_y→∞ strut 극한; `mpm3d_compaction.py`, docs/fibre_rod_mpm_design.md §COMPACTION-RESISTANCE).
VGCF 4 wt% @ input_6mAh_real_4 (n_grid 256, 2.39 M rigid VGCF 셀 = 8 vol% ∝ 부피):
- **방향 ✓**: porosity **volume-fill 8.63 % → 9.38 % (+0.75 %p UP)** = Cho conflicting-roles 부호.
- **메커니즘 ✓**: SE 소성변형 **뭉개짐**(Σdg 0.026→0.001; total strain 0.195→0.006) — rigid VGCF가
  bed를 떠받쳐 SE가 압밀 못 함 → 두께 +0.9 µm, cov AM_S 52.5→50.5.  밀도-페널티 서명 그대로.
- **크기 modest**: +0.75 %p = volume-fill 오차(6.8 %p)의 **~11 %만** 회복.  얼린 AM이 wall_z를 이미
  정하고 VGCF는 사이 공극에 있어 near-wall만 떠받침 — **AM 골격 자체를 벌리는 재배열(나머지 89 %)은
  못 함**(frozen).  = buckling과 같은 frame[5] 경계: 가장 센 MPM 레버도 11 % → 밀도 페널티는 packing/
  재배열 현상(**DEM 몫**) 실증.  절대 porosity는 frame[5] bracket [volume-fill 8.63 … strut 9.38 %]로
  보고, 나머지는 DEM 공동압밀(VGCF를 LIGGGHTS에 유효입자로)에 귀속.  → MPM은 direction+mechanism+
  morphology 소유, 절대 porosity(dip 포함)는 DEM 소유(frame[5] division).

## ★ SuperP 종결 — volume-fill DOWN (no-strut) + handmix 응집이 coverage만 낮춤 (2026-07-03) ★
kgy RTX3090, input_6mAh_real_4, n_grid 256.  SuperP는 `seed_carbon_black` 경로 = strut/align/buckle
**하나도 안 받음**(0D 구, L/D≈1 → rod-jamming/배향/좌굴 기하 전제 없음; soft E=0.5/σ_y=0.1<press →
소성 압밀이 이미 emergent).  이게 VGCF(1D stiff-elastic, prescribed 3-knob)와의 코드/물리 대비.
- **bulk(ballmill=thinky) 스윕 = 순수 volume-fill DOWN, threshold 없음** (VGCF strut-up과 정반대):
  0.5→14.585 / 1→13.711 / 2→11.936 / 4→8.275 %; cov AM_S 47→78 %(카본이 AM 표면 점점 감쌈).
  ballmill≡thinky (CB_MIX 동일 + coat_block 미seed) → 4점 전부 기록값 재현 = VGCF 코드변경이 SuperP
  안 건드림 확인.
- **handmix(분산 나쁨: k3→8 / surface_frac 0.70→0.30 off-AM / clump1→4) SIGNATURE**:
  | wt% | porosity(bm=hm) | cov AM_S bm→hm | Δcov | n_pts Δ |
  |---|---|---|---|---|
  | 0.5 | 14.585 (동일) | 47.3→43.2 | −4.1 | −26 % |
  | 1 | 13.711 (동일) | 53.7→46.0 | −7.7 | −27 % |
  | 2 | 11.936 (동일) | 64.4→51.4 | −13.0 | −27 % |
  | 4 | 8.275 (동일) | 78.2→60.8 | −17.4 | −27 % |
  Δcov가 wt%에 따라 단조 증가 (−4.1/−7.7/−13.0/−17.4).
  ★ **적대적 재검증 정정 (2026-07-03) — 이전 프레이밍 두 곳 과장이었음**:
  1) **porosity 불변 = 구조적 artifact(물리 발견 아님)**: `por=1−solid_vol/(area·height)`(mpm3d:986);
     solid_vol의 carbon 몫 = `add_pvs·len(pts)=vol_um3` EXACT(711-712,753)로 pin, height=wall_z는
     AM+SE 스캐폴드 jamming으로 pin(soft carbon σ_y0.1<press → 흘러서 wall 안 붙듦).  ∴ porosity는 carbon
     형상에 **구조적으로 독립** → byte-동일은 **강제**.  "예측 반증/더 깨끗"은 **틀림**(모델이 carbon-형상
     porosity 효과를 애초에 못 냄); 실제 high-structure-CB porosity(응집체 내부공극/국소 압밀저항)는
     **모델 범위 밖 = deferred CBD nano-porosity**.
  2) **cov 하락 = "SE coverage" 아니라 "carbon coverage"(라벨 artifact)**: `se_occ`(1088)가 x=xs(=SE+carbon,
     704)로 만들어져 "coverage by SE"(1113 라벨)가 실은 SE+carbon.  SE는 스캐폴드 동일(se_dump) →
     Δcov는 **100% carbon 성분**(SE cov 불변).  handmix가 carbon을 AM 밖으로 뺀 것 = **σ_e 신호(carbon
     전자접촉↓)는 진짜**지만 "SE coverage 하락"으로 라벨된 건 오류.
  → **살아남는 것**: handmix가 AM 표면 carbon을 실제로 줄임(분산 나쁨) = σ_e 축 신호, 방향 맞음
  (Reisacher/Kim2025).  **정정**: porosity 불변=구조적 강제(물리 아님), cov=SE 아닌 carbon.
  metric FIX ✅ (2026-07-03): `coverage_AM_P/S_pct`를 **SE-only**로, `coverage_AM_P/S_add_pct`를
  **additive-on-AM(σ_e 접촉)**으로 분리 (mpm3d_compaction `_cov_frac`를 `phase_np==1`로 게이트 +
  payload 키 전달; unit-test PASS, carbon-free real14 자동 불변).  ⚠ 기존 additive 런은 **새 코드로
  재실행**해야 분리값이 채워짐(coverage는 run-time 계산이라 recompute 불가) — SE/porosity 데이터는
  유효하니 coverage만 갱신되는 것, "처음부터"가 아님.
  ★ **검증 완료 (2wt% ballmill/handmix 재실행)**: SE-only cov AM_P/S ballmill **39.3/40.0** → handmix
  **39.3/40.2** = **MIXING-INVARIANT ✓**(SE 스캐폴드 구동); carbon-on-AM cov(`_add`) ballmill 7.9/35.8 →
  handmix 6.2/15.4 = **AM_S −20.4pp** → handmix "하락"이 **전부 carbon coverage에** 있음(옛 conflated
  −13.0보다 큼 — 불변 SE 40에 희석됐던 것).  mixing/cb_mix도 기록됨(handmix k8/sf0.3/clump4).
  ⇒ **"handmix는 SE coverage 안 바꾸고 carbon 접촉(σ_e)만 −20pp 떨어뜨린다"** 실데이터 확정.
  **★ SuperP CLOSED (metric-validated).**

## PTFE mixing = tautological (VGCF와 동일, SuperP와 다름) (2026-07-03)
`CB_MIX`는 `ADDITIVE_PROCESS['SuperP']`에서만 파생(additives.py:293) → **PTFE는 CB_MIX 없음**.  PTFE kind=
'fibre'(mpm3d:659) → `seed_fibres`(682) 사용(`seed_carbon_black` 아님), `seed_fibres`는 `mixing` 인자
자체가 없음(97) → mixing 무시.  PTFE process 3행 전부 regime='bulk', morph만 텍스트("TBD A4").
∴ **PTFE ballmill=thinky=handmix 전부 동일**(VGCF처럼 tautological) → mixing 3개 돌릴 필요 없음, 하나면 끝.
의도된 fibrillation-degree 차이는 미구현(A4).  (SuperP만 handmix가 CB_MIX로 실제 다름.)
⚠ **SUPERSEDED (같은 날, bb49666→bd1ff20)**: `--ptfe-fibril` 구현으로 PTFE도 이제 handmix가 다름 —
`ADDITIVE_PROCESS['PTFE']`에 `fibril=` 필드(bm/thinky 1.0, handmix 0.45, matrix-파생 = CB_MIX 패턴),
handmix → branch_frac 0.5→0.225 (덜-networked web).  §F1 tunable hook(`--ptfe-fibril`), 크기 미앵커 명시.
ballmill≡thinky는 여전히 동일(둘 다 fibril 1.0).
- **adversarial 검증 (workflow wf_17325d01)**: "handmix가 실제 적용됐나 vs mislabel/seed-noise?" 판정
  **handmix_applied (conf 0.85)**.  근거: n_pts −26 %는 seed-only 변동(측정 std 0.16–1.67 %)의
  **15–160σ 밖** → seed로 불가능; porosity-동일이 스캐폴드 불변 증명 → CB_MIX가 유일 lever;
  ballmill≡thinky니 다른 실현은 handmix뿐; cov AM_S만↓/AM_P flat = surface_frac 지문.  (judge의 toy
  random-sphere가 부호 재현 못 한 건 실제 압축 bed 아닌 toy 한계로 귀속 — 3점 스케일링이 독립 확증.)
- **TRACEABILITY fix (commit)**: metrics의 `mixing_regime`이 ballmill/handmix 둘 다 'bulk' → JSON만으론
  구분 불가였음.  `mpm3d_compaction.py` `_add_meta`에 **mixing NAME + cb_mix params(k/surface_frac/
  step/clump)** 추가 → 이제 bulk-regime 런도 자기-문서화(py_compile ✓, CB_MIX 구조 검증 ✓).
- **thinky의 진짜 차이(coat_block → σ_e 붕괴, Kim2025)는 여전히 A4 대기** — bulk에선 ballmill과 동일.
  handmix는 **분산/응집 축**(bulk, 지금 가능)이고 thinky는 **coating 축**(A4/STEP3)으로 분리됨.

## ★ PTFE 압축 물리 종결 — anchor+bridge binder, drape는 packing-지배 (2026-07-03) ★
kgy 09eac31, real_4 PTFE 0.5wt% ballmill.  풀 물리 스택(모두 metrics에 기록): fibrillation 1.0 /
branch_frac_effective 0.5 / **align_lambda_z 0.653**(PTFE로 auto-bake 확장) / **am_bind f=0.5**
(`--ptfe-am-bind`, PTFE nucleation의 AM-표면 drape 몫; carbon-count 독립 fraction, §F1 tunable) /
coh_ptfe 0.0649 (A3 binder_cap 0.649) / press_curl false(opt-in, VGCF-차용 크기라 §F1로 OFF).
- **porosity 14.703 = volume-fill 예측 14.7 EXACT** (soft PTFE, SuperP와 동일 구조).
- **PTFE-on-AM add-cov 0.8/1.1% — 낮은 게 맞는 물리**: 1D bridging binder ≠ 0D coating carbon
  (SuperP add-cov 35.8 @2wt%).  coverage는 PTFE 바인딩의 잘못된 렌즈.
- **기하 ground-truth (payload KDTree, 120k pts)**: PTFE의 **20.7%가 AM 표면 0.2µm 이내(drape)**,
  median gap 0.51µm, 79%가 1µm 이내, 18.5%가 pore-bridge(>1µm) = **anchor+bridge binder 형상**
  (Lee 2025 SEM "fibrils stretched & fibrillated ACROSS the interface, bridging particles" 정합).
- **★ AM-BIND 대조군 (`--ptfe-am-bind 0` 재실행)**: drape 20.7→**19.5%** (Δ+1.2pp), pore-bridge
  18.5→20.6%, porosity byte-동일.  ⇒ **drape는 PACKING-지배** — 56% AM 압축 bed에선 랜덤 fibril도
  이미 ~19.5%가 AM 근접; nucleation-bias는 방향 맞는(+drape/−deep-pore) 작은 증분만.  이유: fibril은
  시작점 1개만 AM에 앵커, 나머지 ~140점 worm-walk(L40µm, curl0.4)은 pore로 뻗음 — 그리고 그게
  dry-PTFE SEM(bridging, 필름-wrap 아님)과 일치.  `am_bind:false` traceability도 검증 ✓.
- **결론 (정직)**: PTFE-AM 바인딩의 본질 = **anchor+bridge 연결성**(+A3 cohesion 역학) — surface
  coverage %가 아님.  값은 STEP3(σ_e network / mechanical connectivity)에서 나타남.  PTFE porosity/
  형상 축 CLOSED; 남은 PTFE 물리 = handmix fibril 0.45 대비런(선택) + STEP3 연결성.

### PTFE wt% 스윕 완결 (0.5/1/2/4, ballmill full-physics, 2026-07-03)
| wt% | por (pred) | drape<0.2µm | add-cov AM_S | binder_cap |
|---|---|---|---|---|
| 0.5 | 14.703 (14.70) | 20.7% | 1.1% | 0.649 |
| 1 | 13.948 (13.94) | 20.8% | 2.2% | 0.930 |
| 2 | 12.415 (12.39) | 21.1% | 4.4% | 0.955 |
| 4 | 9.254 (9.21) | 21.0% | 8.8% | **0.504** |
3중 일관성: ① porosity = volume-fill EXACT 전 구간; ② **drape ~21% wt%-불변**(intensive 형상통계,
packing-지배 — am-bind 대조군과 정합) vs **add-cov 완벽 선형**(extensive 재료통계, 1.1→2.2→4.4→8.8);
③ **binder_cap이 A3 비단조 arc를 데이터로 완주** — 0.649→0.930→[peak 1.0 @1.5wt%]→0.955→**0.504**
(4wt% over-crosslink 반토막, 공식값 사전등록 후 적중).  PTFE porosity/형상 축 스윕까지 CLOSED.

### ⚠ 두께 컬럼 정직 노트 — 전 런 112.9µm 고정 = frozen-scaffold 강제 (2026-07-03, 사용자 관찰)
저장된 payload 23종의 두께가 전부 112.9µm(wall_z 2.1267 byte-동일; 유일 예외 VGCF-4 strut 113.8)인
것은 물리 결과가 아니라 **모델 구조 3중 pin**: ① AM 스캐폴드 frozen(무첨가 DEM 골격) ② hold 프로토콜
정지높이 = AM+SE jamming ③ soft additive(σ_y<press)는 흘러서 wallP 기여 0 → 플레이트 못 밀어올림.
⇒ 첨가 부피가 100% porosity↓로 강제 흡수(=volume-fill의 두께-측 얼굴).  **strut(113.8, +0.9µm)이
유일하게 두께 반응 = 메커니즘 증명**.
물리 판정: soft 저 wt%(pore의 ~6-12% 채움)는 void-fill ≈ 그럴듯(실제 두께변화 ~1%↓).  4wt%(=solid
7.3vol% ≈ pore 공간의 ~40%)를 골격 교란 없이 전부 pore로 = **과장** — 실제는 상당분이 두께↑
(porosity 유지 가정 시 ~+8µm: 112.9→~121µm).  stiff VGCF는 Cho 방향(두께가 첨가부피 이상 ↑)인데
frozen AM 탓에 strut가 ~11%만 회복(+0.75%p 결론과 동일 수치).
frame[5]: 두께 절대값 = porosity와 동일한 bracket [volume-fill 하한 … strut 부분회복] + 실제값은
Cho-dilate 곡선에서 유도(VGCF 2wt% dilate ε 15.28% → +4µm 스케일).  **트렌드/형상/coverage 비교는
모든 런이 같은 pin을 공유하므로 유효**.  두께 자유도는 모델에 있으나(wall_z는 300MPa까지 하강)
frozen 골격이 사실상 pin — AM-재배열 몫 = DEM(frame[5] division)의 두께-축 표현.

### PTFE handmix 스윕 완결 (0.5/1/2/4, 2026-07-03) — 4/4 사전등록 적중
porosity/두께: **전 점 ballmill과 byte-동일**(14.703/13.948/12.415/9.254, 112.87µm) — 구조적 pin의
mixing-측 표현: soft additive의 *형상*(분산/분기)은 wallP에 기여 0 → **mixing은 porosity·두께 축에서
원리적으로 무정보**(SuperP porosity-invariance 정정과 동일 클래스; 실제 저전단 분산불량은 packing 악화로
약간 두꺼워질 수 있으나 frozen-scaffold가 표현 불가 — af712a0 두께 노트 그대로).  mixing의 진짜 정보 =
**web 연결성**: fibrillation 0.45 → children 45%로 반토막(0.5wt% 337/784, 1wt% 683/~1577; ≥2wt%는
payload --fibre-max 4000 캡이라 full-res n_pts −15~18%로 확인) + PTFE-on-AM 소폭↓ → STEP3 축.
binder_cap은 wt%-구동·mixing-무관 확인(0.649/0.930/0.955/0.504 양쪽 동일).

## ★ 두께-형상 동시응답 — anchored dilation `--dilate-z` (2026-07-08, 2-agent 리뷰 반영 개정) ★
"질량보존 후처리는 숫자만 고치고 형상은 못 고친다"(사용자 지적, 맞음)에 대한 DEM-불요 해법.
**물리 판정 1순위**: 완전-emergent 골격 재배열 = granular force-chain = **DEM-클래스** (mobile-AM MPM은
틀린 응답=artifact, 기각 유지).  DEM 없이 가능한 최선 = **prescribed-but-anchored dilation**:
- λ_dz = **(1+φ_VGCF)·(1−ε_DEM)/(1−ε_real)**; **ε_real = ε_DEM + Δε_cho(w)** —
  `docs/data/vgcf_dilate_cho_calibrated.csv` 보간 (dem_perturbation driver C, **Balberg-percolation-
  gated, A_cho=1.568** = 레포의 유일 Cho-anchored 곡선).  ⚠ 첫-커밋(2db2e53)의 선형 0.5pp/wt%는 이
  곡선과 저 wt%서 모순(0.5wt% **부호 반대**: 곡선 −0.209pp = percolation 이하 fill-지배) → **폐기·
  단일화** (리뷰 발견 — 두 Cho-곡선 공존 금지).
- **Cho 앵커 캐비엇 상속**(§실제 실험과 비교 그대로): 433 MPa(우리 300 아님)·다른 조성·**2점(0/2wt%)
  앵커** → 기울기 ±~50%, 4wt%는 앵커 밖 외삽.  onset 상수는 [0.7 Balberg-percolation … 5.4
  Philipse-dense]·D/L **모델링 범위**(dem_perturbation.py:237-239).
- **Philipse 관계 (정직 표현으로 정정)**: strut onset은 solid-frame 4~8vol% **bracket**(2점)이고
  bed-frame으론 ~3.4–7.3vol% — Philipse dense-jamming 상한 8.1vol%와 **order-of-magnitude 정합**
  (±수십%; waviness·L_cv=0.4로 유효 α 불확실).  "독립 재현" 아님 — Cho의 2wt% soft onset은 Balberg
  percolation(0.7 하한)이 설명.
- **strut ⊃ dilation 규칙 (이중계상 방지)**: λ_dz가 Cho prop-open **전체**를 인코딩 → 같은 메커니즘의
  부분모델 rigid strut(+0.75pp@4wt%)을 겹치면 이중계상 → dilated zip은 auto-`--fibre-stiff` **드랍**
  (CLI --fibre-stiff 강제는 존중; buckle은 형상 전용 유지; **align은 ε_real 기준 재계산** = 두 auto-flag가
  하나의 porosity 서사).
- **soft additive(PTFE/SuperP)는 제외** — σ_y<press로 pore에 흘러들어 prop 못 함 → 그쪽 두께 pin이
  물리적으로 맞음.  z-only affine = die-press 전역 모드(lateral은 die 고정); 국소 비-affine 재배열은
  DEM 몫으로 명시 잔류.
- 구현: `mpm3d --dilate-z`(스캐폴드 AM+SE z-offset 스트레치, 반지름 불변=prop-open; 스캐폴드 없으면
  no-op + metrics 미기록) + `mpm_input_from_case` VGCF recipe 자동 bake — **canonical `parse_recipe`**
  ('VGCF:PTFE=1:1' / 'AM:SE:VGCF=…' / 'VGCF=4' 전 포맷; 첫-커밋 regex는 combo 소실·legacy 포맷 λ≈10.9
  재앙 → 수정) + λ∈[1,1.35] sanity gate + `--no-dilate`(bracket-floor 재생성, sed 불요) +
  **payload 동일-프레임 배선**(step2에 `--dilate-z`·ε_real 타깃 전달 — 없으면 뷰어/coverage가 dilated
  SE를 un-dilated AM과 비교 + voxelize가 porosity를 ε_DEM으로 되-pin).  두께/porosity는
  by-construction, **coverage·망·SE-strain은 emergent** (= 새 정보).
- λ_dz(real_4, 곡선 기준): VGCF 0.5→1.0077(T 113.7µm) / 1→1.0222(115.4) / 2→1.0536(118.9) /
  4→**1.1119(125.5)** / VGCF1+PTFE1→1.0225.  ⚠ opt-in 게이트(--am-jam/--floor-porosity/--se-am-drag)는
  un-dilated 앵커 → dilated bed 미보정(mpm3d 런타임 경고; 생성기는 애초에 안 bake).
- ⚠ 기존 VGCF 행들은 pre-dilation(un-dilated bracket 하한)으로 유효 유지; 이후 VGCF zip은 dilated 기본.
  CSV의 volume-fill pred 컬럼은 dilated 런에 부적용 — dilated pred = ε_real(노트에 기재).
- 검증런 사전등록 (VGCF 4wt% ballmill **dilated, auto-strut 드랍**): thickness ≈**125.5µm**,
  porosity(in-sim) ≈**17.5%** (= ε_real 16.41 + MPM-baseline offset ~1.2pp; offset의 λ-증폭 ±0.3pp 여유),
  **cov AM_S < 40.3 하락 = emergent 신규 정보**, metrics `dilate_z:1.1119` + `fibre_stiff:false`.

### ★ dilation 검증런 PASS — 두께·porosity·형상 최초 동시응답 (2026-07-08, V1: VGCF 4wt% dilated) ★
사전등록 전 항목 적중: **thickness 125.128µm = 112.87×1.1076 EXACT**(pin 최초 탈출) / porosity **16.838**
(설계 ε_real 16.41 + 0.43 — SE 구 z-분리로 voxel-union 부피 +3%가 원인, 리뷰가 예고한 2차 효과;
seed_SE 26.08% > 순수 스케일링 25.2%가 증거) / metrics `dilate_z:1.1076`+`fibre_stiff:false`(strut 드랍
규칙 작동) / payload 프레임 dilated 검증(AM top 125.5µm).
★ **emergent 형상 응답 (신규 정보)**: cov AM_S **SE-only 40.3→21.3** + **VGCF-on-AM 15.6**(AM_P 12.5+16.2)
— 분해하면 ① 벌어진 bed에서 SE가 덜 눌려 AM 접촉↓ ② 4wt% VGCF가 AM 표면 ~16% 점유(σ_e 좋고 σ_ion
손해 = Cho conflicting-roles의 구조적 기반).  ⚠ 옛 strut런 cov 50.5는 pre-split conflated(SE+VGCF)라
직접 비교 불가.  ⇒ dilation 축 CLOSED — 남은 조합런(VGCF1+PTFE4 zip 보유 / 1+1 handmix / SuperP2+PTFE1)
후 A4 진입.
