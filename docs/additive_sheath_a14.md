# A14 — surface_conformal SWCNT sheath (제3 도전재 morphology) — 2026-07-21

앵커: **#275 koo2026** (Joule 10, 102392; litdb `docs/lit_koo2026_swcnt_sheath_thick_electrode.md`).
구현: `additives.seed_sheath()` + `additives.sheath_ion_tradeoff()` + `mpm3d_compaction --add-recipe
…SWCNT… [--swcnt-wrap]` + **STEP3 sid 8 배선**(payload `--sigma-swcnt`/`--swcnt-ion-block`) + viewer.
selftest: sheath 10종 + `step3_sigma --selftest-swcnt` 3종 PASS.
**3각 적대 리뷰(코드·물리·전기화학) 22건 전부 반영** (CRITICAL 1 = sid 무배선, MAJOR 8 포함 — §7).

## 1. 무엇이 다른가 (3-morphology 구분)

| morphology | 코드 | 배치 | 역할 |
|---|---|---|---|
| SuperP (discrete) | `seed_carbon_black` | 입자간극 분산점/체인 | gap-filler — 두꺼운 전극에서 연속망 실패 (#275 서론과 우리 SuperP-vs-VGCF 발견 일치) |
| VGCF (bulk fibre) | `seed_fibres` | 벌크 관통 강성섬유 | interstitial backbone |
| **SWCNT sheath (A14)** | `seed_sheath` | **AM 표면 위 연속 정맥형 필라멘트** | conformal 전자 skin — koo2026 **액체계**에서 활물질 99.7wt% 두꺼운 전극의 승자 실증.  **우리 LPSCl계 전이는 조건부**: 탄소-morphology 물리(연속 1D가 discrete를 이김)만 전이; 이온습윤·전해질침투는 비전이, 이온접촉 상한(§3)·SE-분해면적(R_chem, §6) 축은 미해결 |

A4 `coat_block`(SuperP thinky 차단막 = 고립 film 점)과도 별개 — sheath는 **체인이 자기-연속**
(geodesic walk, step≈voxel).  ⚠ 프로덕션 점예산(~0.2wt%+max_pts)에서 **AM별 skin의 체인-간 연결성은
표현-밀도 한계** (µm급 체인간 갭; coverage와 같은 캐비엇 클래스) — 방향은 정직(복셀 스탬프가 실제
연속 skin의 σ_e를 **과소**표현, 가짜 이득 없음).

## 2. 시딩 물리 (koo2026 앵커 ↔ 구현 맵)

| koo2026 실측 | 구현 |
|---|---|
| ζ 자가조립: PDDA +14.2mV → f-SWCNT −35mV 부착 → 합성물 ζ≈**−1.9mV = near-complete coverage** | `wrap_frac=1.0` 기본 (process row; `--swcnt-wrap`으로 부분피복 what-if) |
| 부착 강건성: **고전단 슬러리(wet) 혼합 >2000rpm 후 Raman 신호 유지** (Fig 1F); koo 자체 dry 공정 = kneading/캘린더링 | thinky/handmix = 앵커 커버.  **⚠ dry 볼밀(미디어 충격)은 앵커 범위 밖** — 같은 미디어가 SDCP 3µm→0.3µm를 분쇄하는 매트릭스에서 nm 정전부착 skin 생존은 가정(§F1 라벨, ballmill row) — wrap 1.0은 방향치, `--swcnt-wrap<1`이 열화 knob |
| "vein-like" 정맥형 섬유망 (Fig 1D) | sphere 위 geodesic random walk, persist=0.85(표현 knob) 곡률노이즈 → 물결 vein |
| SWCNT 외경 ~2nm (OCSiAl, Fig S1) — **sheath 두께는 미발표** | few-layer skin **~2-10nm = 우리 추론**(튜브 Ø에서; "2-10nm (Koo)"로 인용 금지).  표현 skin `SWCNT_SHELL=0.08µm` = sub-voxel 정직(1-voxel 과대표현 클래스, add_pvs 부피-핀 → porosity 정직) |
| 0.2wt% 로딩 분말전도 ~0.20 S/cm vs (NCMA+CB 99:1) ~0.06 (>3×) | **0.20은 분말-복합체값 — 상(phase) σ로 이식 금지**.  `--sigma-swcnt` 기본 100 (VGCF급 lit-order ⚠hook) |

기타 §F1 미앵커 (hook 라벨): 번들 Ø 50nm(`SWCNT_BUND_D`, 카운팅/뷰어 스케일 — Fig 1D 수치 없음),
ADD 행 E=0.5/σ_y=0.1 GPa(skin **transverse film-effective** 미앵커 — 단일튜브 axial ~1TPa는 축이
다름; ≤0.5wt%+부피핀 → 압밀 영향 무시가능 — 물리리뷰 P2G 검증: 질량·응력 전부 pvs-스케일),
DENS 1.35(이론 (10,10)급 1.33, 번들 1.3-1.5 중간 proxy — count 스케일만).

## 3. 이온접촉 trade-off — 2층 보고 (★핵심 정직성)

sheath는 AM|SE 계면에 **개재**하므로 전자 skin의 대가로 이온 접촉을 잃을 수 있다 (ASSB 특유 축).
`sheath_ion_tradeoff()`가 **두 층으로 분리 보고**:

1. **physical_bound (해석적)** — `blocked_of_se_contact_pct_upper_bound` = `100·wrap_frac` %.
   랜덤 cap 방향 하의 **기대값(수학적으로 정확, SE-군집 무관** — P(점∈랜덤 cap)=cap 면적비; 물리
   리뷰 수치검증).  wrap=1에서만 진짜 상한; wrap<1에선 개별 AM이 국소적으로 100%까지 차단될 수
   있음(SE 접촉이 cap 안에 군집 시 — dead-AM 핫스팟, 케이스-평균이 숨기는 꼬리).  **"상한"은
   ion-blocking-skin 가정 축의 상한**: 문자 그대로면 wrap=1 → 100% 차단 = **전기화학적으로 죽은
   양극**인데 koo2026 셀은 11.4 mAh/cm²를 뽑음 — 즉 액체계에선 skin이 Li⁺를 통과시킴(우리 추론:
   전해액이 nm 튜브망을 적심; koo의 **발표된 수송 주장은 기공-채널 비우기**(D_eff 2.5×)지 trans-skin
   다공성이 아님 — 오귀속 금지).  **고체 LPSCl 최근접 앵커 = kim2025 SP@CAM**(개재 탄소: 활성표면적
   −49%, σ_ion −31% @2.9wt%) = 측정된 **부분** 차단 → 실제 손실은 상한보다 훨씬 아래 기대.
   bracket이지 예측 아님; blocked_eff는 R_int(N) 프레임의 **R_ct ∝ 1/(1−blocked_eff)** 로 연결.
2. **cloud_at_representation_density (per_band)** — 시드 점군 vs Fibonacci AM-표면샘플, Hertz
   0.13/Tabor 0.26µm.  ⚠ **양쪽 점군 모두 표현-밀도 한계**: sheath 점간격(프로덕션 ~0.5µm) > 밴드,
   SE쪽도 서브샘플(300k, 간격 ~0.19µm — Tabor 근해상·Hertz 미해상)이라 se_contact_pct가 실제 AM|SE
   접촉을 **크게 과소**표기.  체인-배치 진단용; 물리 피복으로 읽기 금지.  `n_se_used`/
   `se_nn_spacing_um`/`se_cloud`(pre-compaction 라벨)/`cloud_nn_spacing_um`을 meta에 병기해
   자기-기술.  조밀 케이스에서 상한으로 수렴(selftest: dense 합성 98.96% ≈ 100%).

## 4. 배선 (리뷰 CRITICAL 수정 후 — 실제로 살아있는 경로)

- `additives.py`: `PHASE['SWCNT']=6`, 상수/DENS, `ADDITIVE_PROCESS['SWCNT']`(mixing별 §F1 라벨),
  `seed_sheath`(매 스텝 u-재정규화+Gram-Schmidt — tiny-cap wf≤0.025 불안정성 수정; **이웃-매몰
  해석적 drop**(KDTree) — 복셀 in_am의 own-host 20% 오드랍 수정; max_pts 예산), `sheath_ion_tradeoff`
  (<2점 가드 — inf JSON 방지), selftest 10종(tiny-cap 3종 포함).
- `step3_sigma.py`: **`SID_NAME[8]='SWCNT'` + rasterize phase→sid `(6,8)`** (리뷰 전엔 미배선 =
  무음 no-op이었음) + `--selftest-swcnt`(스탬프·테이블 3종).
- `mpm_webapp_payload.py`: `--sigma-swcnt`(100 hook) → `_sig3[8]`; **이온 기본 = SE-투명**
  (`_sig3i[8]=σ_ion_se`: 1-voxel 차단은 2-10nm skin의 40-200× 과대표현 = trade-off 상한 이중계상)
  + **`--swcnt-ion-block`** = 상한 시나리오 opt-in(σ_i=0 → 이온 dof·BV면 소멸); field sel_sids
  전자(…,8)/이온(5,6,8); sigma_table에 SWCNT+ion_mode 기록; `electronic_connectivity` cond_phases
  +6; `additive_fibres` fib_mask +6(vein 폴리라인 렌더); additive_points (6,'SWCNT').
- `viewer3d.js`: PHCOL/PH/PHN/swatch/범례 + **`add_swcnt` 단독 서브모드**(개별+비교 패널).
- meta: `additives.SWCNT.sheath{wrap_frac, shell_um, n_chains(전역 fid 오프셋 전 unique — 리뷰
  수정), morph}` + `sheath_tradeoff`.

## 5. 성능 (컨테이너 실측)

real14급 합성(AM 457개, 0.2wt% → 179k objects): 시딩 165k pts/44k chains **6.6s**, trade-off 0.3s.

## 6. 남은 것 / 후속

- **GPU 검증 런** (V100): real14 + `AM:SE:SWCNT:PTFE` — porosity 불변(부피핀) + sheath_tradeoff
  meta + STEP3 σ_e 효과(이제 실제 배선됨 — 리뷰 전엔 0이었을 것) + vein 렌더 + `--swcnt-ion-block`
  상한 시나리오 쌍런.
- deformed-cloud trade-off (압밀 후 SE 재배치) = payload-side future.
- **미해결 전기화학 축 2개 (리뷰 지적, §F1 정직)**: ① conformal skin은 **탄소|LPSCl 접촉면적을
  최대화** → SE-분해(고전위 산화) 면적 축 = R_int(N) 프레임의 **R_chem(N) 악화 후보** (sheath =
  best-σ_e / worst-R_chem 가능성 — 앵커 문헌 대기); ② **300 MPa 공압밀 생존**은 혼합-강건성과
  별개 질문(LPSCl 소성유동 하 nm skin — 미앵커).
- LPSCl 위 CNT skin 이온투과성 앵커 문헌 대기 (확보 전까지 상한+kim2025 부분차단 bracket만).

## 7. 리뷰 기록 (2026-07-21, 사용자 지시 "할때마다 코드·전기화학·물리 리뷰")

3각 적대 리뷰 22건 → 전부 반영: **CRITICAL** phase6 sid 무배선(무음 no-op) = sid 8 신설로 수정 +
selftest-swcnt 신설.  **MAJOR**: 이온 이중계상 함정(→ SE-투명 기본 + ion-block opt-in 설계),
"koo2026 porous/ion-passing" 오귀속(→ 채널-비우기 발표 + trans-skin은 추론), kim2025 부분차단 앵커
누락(→ §3 반영), "2-10nm (koo)" 오귀속(→ 우리 추론 라벨), slurry 한정사 탈락+볼밀 외삽(→ §F1 라벨),
30k SE 서브샘플 미기술(→ 300k + meta 자기기술), tiny-cap walk 불안정(→ 재정규화+클램프+selftest),
n_chains 전역오프셋 인플레(→ unique 선계산), own-host 복셀 오드랍 20%(→ 해석적 KDTree drop),
fibres/econn/서브모드 미배선(→ 배선).  **MINOR**: inf JSON 가드, 기대값-vs-상한 라벨, dead-cathode
귀류 명시, "실제 승자" 조건부화, R_chem/공압밀 캐비엇, budget floor 문서화.
