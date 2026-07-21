# A14 — surface_conformal SWCNT sheath (제3 도전재 morphology) — 2026-07-21

앵커: **#275 koo2026** (Joule 10, 102392; litdb `docs/lit_koo2026_swcnt_sheath_thick_electrode.md`).
구현: `additives.seed_sheath()` + `additives.sheath_ion_tradeoff()` + `mpm3d_compaction --add-recipe
…SWCNT… [--swcnt-wrap]` + payload/viewer phase 6 배선.  selftest 7종 PASS
(`python3 scripts/additives.py --selftest-sheath`).

## 1. 무엇이 다른가 (3-morphology 구분)

| morphology | 코드 | 배치 | 역할 |
|---|---|---|---|
| SuperP (discrete) | `seed_carbon_black` | 입자간극 분산점/체인 | gap-filler — 두꺼운 전극에서 연속망 실패 (#275 서론과 우리 SuperP-vs-VGCF 발견 일치) |
| VGCF (bulk fibre) | `seed_fibres` | 벌크 관통 강성섬유 | interstitial backbone |
| **SWCNT sheath (A14)** | `seed_sheath` | **AM 표면 위 연속 정맥형 필라멘트** | conformal 전자 skin — 활물질 99.7wt% 급 저탄소 전극의 실제 승자 (#275) |

A4 `coat_block`(SuperP thinky 차단막 = 고립 film 점)과도 별개 — sheath는 **체인이 표면 위에서
연속**(geodesic walk)이라 복셀화 시 AM별 연결된 도전 skin이 됨.

## 2. 시딩 물리 (koo2026 앵커 ↔ 구현 맵)

| koo2026 실측 | 구현 |
|---|---|
| ζ 자가조립: PDDA +14.2mV → f-SWCNT −35mV 부착 → 합성물 ζ≈**−1.9mV = near-complete coverage** | `wrap_frac=1.0` 기본 (process row; `--swcnt-wrap`으로 부분피복 what-if) |
| **혼합-강건**: >2000rpm 고전단 후에도 Raman SWCNT 신호 유지 (Fig 1F) | SWCNT row는 **mixing-독립** (ballmill≡thinky≡handmix — 유일한 mixing-독립 additive; sheath는 혼합 전 분말에 pre-formed) |
| "vein-like" 정맥형 섬유망 (Fig 1D) | sphere 위 geodesic random walk, persist=0.85 곡률노이즈 → 물결 vein |
| SWCNT 외경 ~2nm (OCSiAl) | `SWCNT_D=0.002µm` 기록; **표현은 sub-voxel 정직**: skin `SWCNT_SHELL=0.08µm` (seed_coat와 같은 1-voxel 과대표현 클래스, add_pvs 부피-핀 → porosity 정직) |
| 0.2wt% 로딩에서 분말전도 ~0.20 S/cm (CB 1wt% 0.06의 3배) | σ_e 방향은 STEP3 소관 (A4 관례와 동일) — seed는 구조만 |

§F1 미앵커 (hook 라벨, 날조 없음): 번들 Ø 50nm(`SWCNT_BUND_D`, 카운팅/뷰어 스케일 — Fig 1D에 수치
없음), ADD 행 E=0.5/σ_y=0.1 GPa (skin의 **transverse film-effective** 물성 미앵커 — 단일튜브 axial
~1TPa는 축이 다름; ≤0.5wt%+부피핀이라 압밀 영향 무시가능), DENS 1.35 (이론 (10,10)급 1.33, 번들
1.3–1.5 중간 proxy — count 스케일만 결정).

## 3. 이온접촉 trade-off — 2층 보고 (★핵심 정직성)

sheath는 AM|SE 계면에 **개재**하므로 전자 skin의 대가로 이온 접촉을 잃을 수 있다 (ASSB 특유 —
koo2026 액체셀에는 없는 축).  `sheath_ion_tradeoff()`가 **두 층으로 분리 보고**:

1. **physical_bound (해석적)** = `100·wrap_frac` %.  실제 skin은 2-10nm 연속막이므로 wrap된 영역의
   모든 AM|SE 접촉에 개재 → 이온접촉 손실의 **기하 상한**.  cap 방향은 SE 접촉위치와 무상관 →
   기대 blocked = wrap_frac.  **이 수치로 추론할 것.**
2. **cloud_at_representation_density (per_band)** = 시드된 점군 vs Fibonacci AM-표면샘플, Hertz
   0.13/Tabor 0.26µm 밴드.  ⚠ **표현-밀도 한계**: 0.2wt%+max_pts 캡에서 점간격(실측 ~0.5µm) >
   밴드라 연속 skin을 **과소**샘플 — 물리 피복이 아니라 체인-배치 진단용.  점간격 ≪ 밴드인 조밀
   케이스에서만 physical_bound로 수렴 (selftest에서 수렴 확인: dense 합성 98.96% ≈ 100%).

   초기 구현은 cloud 수치를 "상한"으로 라벨했었는데, 프로덕션 밀도 실측(165k pts/37,600µm² →
   blocked 9.5–22%)이 상한이 아니라 **과소치**임을 드러내 즉시 2층 구조로 정정 — trust 라벨에
   nn-spacing을 병기해 어느 층이 유효한지 자체 판별 가능.

상한의 의미(§F1): **ion-blocking skin 가정 시**의 상한.  koo2026(액체)은 다공 vein이라 이온 통과
주장; **고체 LPSCl 접촉이 개재 skin을 견디는지는 우리 계에 미앵커** → 손실 예측이 아니라 상한만.

## 4. 배선

- `additives.py`: `PHASE['SWCNT']=6`, DENS/`SWCNT_*` 상수, `ADDITIVE_PROCESS['SWCNT']`
  (regime=`surface_conformal`, 전 mixing wrap_frac=1.0), `additive_wt`/`recipe_counts_real`
  (v_obj = 1µm vein-번들 세그먼트 — 표현예산; 실튜브 Ø2nm면 수십억 객체라 불가), `seed_sheath`
  (max_pts=400k 예산캡 — dispatch "objects → pts" 출력으로 가시화, 침묵캡 아님),
  `sheath_ion_tradeoff`, `_selftest_sheath` (7종: skin·contiguity·coverage·partial-wrap·
  tradeoff수렴·burial·budget).
- `mpm3d_compaction.py`: ADD 행 `SWCNT`(phase 6, kind='sheath'), `--swcnt-wrap`, dispatch 분기
  (pre-additive SE 스냅샷 `_se0_box` 대비 seed-time trade-off → `mpm_metrics['additives']['SWCNT']
  ['sheath'/'sheath_tradeoff']`).  ⚠ taichi 미설치 컨테이너 → py_compile 검증만; GPU 런은 V100.
- `mpm_webapp_payload.py`: `_cond_ph`에 6 (STEP3 도전 스탬프 — sheath는 도체), additive_points
  루프에 (6,'SWCNT').
- `viewer3d.js`: PHCOL/PH/swatch/범례에 SWCNT green(#22c55e).

## 5. 성능 (컨테이너 실측)

real14급 합성(AM 457개, 0.2wt% → 179k objects): 시딩 165k pts/44k chains **6.6s**
(실제 `_in_am_abs`는 그리드 룩업이라 더 빠름), trade-off 0.3s.

## 6. 남은 것 / 후속

- **GPU 검증 런** (V100): real14 + `AM:SE:SWCNT:PTFE=…:0.2:…` — porosity 불변(부피핀) + payload
  sheath_tradeoff 확인 + 뷰어 vein 렌더 확인.
- deformed-cloud trade-off (압밀 후 SE 재배치 반영) = payload-side future.
- STEP3 σ_e에 sheath 연속망 반영 (경로: 복셀 스탬프가 이미 도전상 6을 포함 → 자동; 정량 비교런은
  SDCP 캠페인 패턴 재사용).
- LPSCl 위 CNT skin의 이온투과성 앵커 문헌 대기 (§F1 — 확보 전까지 상한만).
