# A5(분산 CoV) + A6(pore-τ) CLOSEOUT — 2026-07-14

계기: 사용자 "step4 넘어가기전에 A4 이후거 닫자" (GPU 대기 중 GPU-free 항목 소진).
같은 세션에서 audit 문서의 stale 행 2개(#5 → A3 종결 미반영, #11 → A1 종결 미반영)도 정합화.
관련: `docs/digest_model_application_backlog.md` A5/A6 행, `docs/stage2_model_audit_vs_literature.md`.

## A5 — additive dispersion uniformity (E2, #284 SSRM-analog)

**구현**: `scripts/additives.py :: dispersion_metrics()` (numpy+scipy만) →
`mpm_webapp_payload.py`가 풀해상도 point cloud에서 per-phase(VGCF/SuperP/PTFE/SDCP +
conductive_all) 계산 → `mpm_metrics.additive_dispersion`.

**2축 설계 (서로 다른 질문에 답함)**:
| 축 | 정의 | 보정점 | 용도 |
|---|---|---|---|
| `index_of_dispersion` | 2µm cell 격자 per-cell 점수의 var/mean | CSR(포아송 랜덤)=1.0 | **같은 phase의 run간** 응집도 비교 (밀도-보정; raw CoV는 희소상이 1/√mean 포아송 바닥 때문에 불공정) |
| `nn_med_um`/`nn_p90_um` + `nn_clustering` | SE-매트릭스 샘플→최근접 첨가제 거리; nn_clustering = nn_med / 동밀도-포아송 기대 r_med=(3ln2/4πn)^⅓ | random=1.0 | **cross-phase** "매트릭스가 전도망에서 얼마나 먼가" (SSRM 메커니즘판) |

**정직 캐비엇 (설계에 명문화)**:
- chain/blob phase(VGCF·PTFE 섬유 = 물체당 수십 collinear 점)는 within-object 상관으로 D가
  구조적으로 >1 → D의 cross-phase 절대비교 금지, nn_* 축이 그 역할.
- nn_* 는 형상을 **포함**하는 게 설계 의도 — 같은 점예산에서 섬유망이 분산점보다 매트릭스
  공백을 멀게 남기는 것은 수송-관련 사실.
- §F1: #284 SSRM은 다른 모달리티 → **절대앵커 불가**, 우리 run간 상대비교 전용.

**selftest** (`python3 scripts/additives.py --selftest-dispersion`, 4종 PASS):
CSR 20k pts → D=1.0·nn×=1.0 (양 스케일 보정) / Gaussian blob 응집 → D=41.1·nn×=3.3 (검출) /
랜덤배치 직선섬유 → D=6.9 (캐비엇 방향 확인) / **AM-배제 보정** (리뷰 M2/M3 — 아래): 매트릭스-한정
CSR @ AM 19vol% → full-box D=1.54(zero-inflated)·nn×=0.95 vs **masked D=1.02·matrix-ref nn×=1.02**.

**잔여(⛔ 유지)**: carbon↔SE/AM work-of-adhesion으로 nucleate/surface_frac 물리근거화 —
문헌 정량값 확보 시 (§F1 날조 금지).

## A6 — pore-phase 유효확산 τ (DiffuDict/TauFactor 규약, #281/#286 축)

**구현**: `scripts/step3_sigma.py :: pore_tau()` → payload `step3.pore`
{eps_total_pct, eps_connected_pct, D_rel, tau, n_dof, resid, trust}.

**물리**: 검증된 `solve_sigma_z`(harmonic face-g, per-column distance-aware plates,
floating-island filter)를 **void상 σ=1**로 재사용하는 순수 READOUT — σ_eff가 곧 무차원
D_eff/D0.  τ = ε_total / D_rel (D_eff = D0·ε/τ, tortuosity FACTOR).  ε_total은 닫힌
기공 포함(TauFactor 규약 — 닫힌 기공이 τ를 올림), ε_connected 병기.  D_rel<1e-12
(비퍼콜 기공) → τ=None + reason.

**신규 로직은 2개뿐 (솔버 물리 무변경)**:
1. **z ≤ thickness crop** — 래스터 박스의 상단 void 패딩캡(~1 voxel)이 남으면 모든 컬럼의
   최상단 pore voxel이 플레이트 평면 위에 떠서 top 접촉이 sub-voxel 운으로 절단/유지됨.
   crop이 이 운을 제거 (selftest 3).
2. **PTFE solid-stamp** — PTFE는 전자/이온 격자에 미스탬프(양쪽 절연이라 σ테이블상 불필요)
   → sid==0만으로 기공을 정의하면 PTFE 부피가 열린 기공으로 오계상(ε 과대→τ 과소).
   `extra_solid_pts`로 rasterize와 동일한 단일복셀 스탬프 (selftest 4).

**selftest** (`python3 scripts/step3_sigma.py --selftest-pore`, 6/6 PASS):
전공극 τ=1 / 직선 2×2 채널 τ=1.000·D_rel=면적비 4/36 EXACT (plate half-cell 규약의 해석해) /
패딩캡+crop τ=1 / PTFE plug → D_rel~1e-16·τ=None / 닫힌 포켓 → ε_tot>ε_conn·τ=1.05>1 /
**1-voxel 솔리드 지붕 밀봉** (리뷰 M1 — 아래): frac(z_top/vox)=0.7에서 지붕 아래 기공이 sealed.

**⚠ 사용 규칙 (audit #2 이중계산 함정)**: 이 τ는 **STRUCTURAL descriptor** (기체/액체 침투,
frame[4] 구조 교차검증 축).  ASSB Li⁺ 수송은 SE 접촉망(σ_ionic Kirchhoff)이 담당 — Phase-4
PyBaMM τ 입력은 σ_ionic-anchored 역산(기존 규약)이며 **pore-τ를 수송 폼에 대입 금지**.
trust 문자열에 명문화.

**잔여**: DEM측 `voxel_conductivity`에 같은 패턴 이식은 필요 시 (STEP3측이 현 캠페인
[SDCP SBE/DBE] 커버).  실측 pore-τ 앵커 없음 — #286은 액체계 흑연음극(전이 금지), 우리
값은 run간 상대 + 닫힌기공 진단용.

## 물리 리뷰 (2026-07-14, 2-리뷰: self + adversarial agent — BLOCKER 0, MAJOR 3 전부 수정)

리뷰는 diff 전체를 적대 검증(수치 repro 포함): 어셈블리·crop 인덱스 수식·스탬프 frame 정합·JSON
안전성·payload 스코프·메모리 전부 CLEAN 판정.  MAJOR 3건은 모두 "출력 앵커/경계 regime" 문제
(솔버 물리 오류 아님) — **셋 다 수정 반영**:
- **M1 (수정: `plate_band_um=vox`)** — pore 상단 플레이트가 e-solve 기본 band(vox+0.1)로는
  **1-voxel 솔리드 지붕을 뚫고 결합** (지붕 아래 기공 dist = vox+α < vox+0.1 창).  누출 창
  frac(z_top/vox)∈[0.5,0.75) — **real_14 두께 30.28µm가 정확히 그 안** (τ=0.987<1 재현됨).
  crop 후 표면기공 dist<vox / 지붕기공 dist≥vox가 증명되므로 band=vox가 정확 분리.  e/ion
  솔브의 +0.1µm는 압입 crown-접촉 물리라 유지 — pore엔 press가 없어 solid=밀봉이 옳음.
  selftest 6(지붕 밀봉) 추가.
- **M2 (수정: `am_c_um/am_r_um` AM-셀 마스킹)** — 첨가제는 매트릭스에만 seed되므로 full-box
  격자에서 AM 내부 셀 = 구조적 0 → zero-inflation으로 "CSR=1" 앵커 붕괴 (매트릭스-CSR가
  25k→400k pts에서 D 2.3→22로 점수 스케일링, 응집이 아닌데).  셀 중심이 AM 구 내부인 셀을
  통계에서 제외 → 매트릭스-CSR가 D≈1 복원 (selftest: 1.54→1.02).  잔여 partial-cell 인플레이션
  명문화 — masked-D도 same-recipe·same-scaffold 상대비교용.
- **M3 (수정: 매트릭스-부피 밀도 레퍼런스)** — nn_clustering의 Poisson 기준밀도가 박스 전체
  부피 기준이라 매트릭스-CSR가 <1로 읽힘 (하한 (V_m/V)^⅓≈0.73-0.95).  n = N/(V·mat_frac),
  mat_frac = 1−ΣV_AM/V (AM 구에서 해석적) → 매트릭스-CSR ≈1 복원 (0.95→1.02).
- 동반 수정: **m2** (early-return 시 ε_conn=None — n_dof가 필터 전 값이라 의미 변질 방지),
  **m3** (z_top_um 필수화 — 없으면 패딩캡을 측정하는 오용 홀), **m5** (n_cells<2 → NaN JSON 가드).
- 문서화만 (수정 불요 판정): **m1** τ 편향 +≤0.5·vox/z_top (30µm/vox0.4 최악 **+0.67%**,
  frac<0.5면 EXACT — 검증자 정량화); **m4** rasterize의 AM-AM 접촉 브리지 볼(1.2·vox Hertz-neck
  proxy)이 pore에 solid로 계상 (ε≈15%서 기공상 ~2% — 실제 neck이 그 공간을 차지하므로 방향 옳음);
  **m6** SE 인덱스 transient ~240MB @30M pts (복사는 20k로 서브샘플 후 — 허용).

## 다음 payload run에서 기대할 것 (kgy/gabia GPU 재개 시 자동 포함)

- 로그에 `additive dispersion (A5/E2): VGCF D=… nn_med=…µm(×…)  SDCP …` 줄과
  `STEP3 pore-τ: ε_tot …% (conn …%) · D_rel … · τ …` 줄이 추가됨.
- 300 MPa 압밀 전극이면 pore가 비퍼콜(τ=None + reason)일 수 있음 — **그 자체가 결과**
  (기공 폐색 = 기체 불투과 진단; 오류 아님).
- SBE vs DBE 비교축 추가: SDCP nn_med(SE가 SDCP망에서 얼마나 먼가) + conductive_all
  nn_med(전도망 전체 커버리지) — SDCP "이온/전자 배달" 서사의 기하 정량판.
