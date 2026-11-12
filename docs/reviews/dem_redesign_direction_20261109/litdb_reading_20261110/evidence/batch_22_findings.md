# batch_22 정독 근거 (카드 6 장 · 전문 읽음 · 2026-11-10)

읽은 카드: `galvezaranda2025_paml_vgg16_dem_slurry_drying` (779 줄) · `han2025_icep_conductive_elastic_binder` (181) · `hare2026_dem_pept_dry_mixing_nmc622_eirich` (618) · `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` (294) · `hong2026_sulfide_cathode_binder_digitaltwin` (633) · `jadidi2023_dem_batch_solid_mixers_review` (591). 끝까지 못 읽은 카드 없음 (galvezaranda 4 번 · han 1 번 · hare 3 번 · hippauf 2 번 · hong 3 번 · jadidi 4 번에 나눠 마지막 줄까지 읽음).

배치의 성격: 건조 DEM + DL surrogate (액체 LIB · galvezaranda) 1 · 바인더 실험 (액체 LIB · han) 1 · 건식 혼합 DEM + PEPT 검증 (NMC622 단상 · hare) 1 · 황화물 건식 막 실험 (NCM90 + LPSCl · hippauf) 1 · **황화물 복합 양극 실험 + GeoDict 재구성 (LPSCl + NCM · hong — 이 배치에서 우리와 같은 소재계)** 1 · 믹서 DEM 리뷰 (일반 분말 · jadidi) 1. **MPM 카드 · 순수 SE 압력별 기공 곡선 · 탈압 되돌아옴 실측 · SE 항복 / 경도 · 큰 변형 접촉 법칙 (MDR · EEPA · Thornton–Ning · Storåkers · 다접촉) 을 준 카드는 없다.** 가압 · 탈압 계획에 쓸 것 = 복합 양극 기공 두 점 (hippauf 300 MPa 계산 ≈12 % · hong 350 MPa 재구성 22.3–29.4 vol%) · 같은 소재 양극 σ_ion (hong) · DEM 한계 문장 (hare · jadidi · galvezaranda) · 믹서 쪽 판독 규약 (hare · jadidi).

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (`stated` · `digitized` · `figure-stated` · `derived(ours)` · `digest 산술` · `[인쇄]` · `[판독]` · `[우리 산술]` · `[추정]` · `[미확인]` · 🧮) · 없으면 "표지 없음". "카드 풀이" = 논문 문장이 아니라 카드 작성자의 서술. "카드 옮김" = 카드가 원문을 한국어로 옮겨 따옴표에 둔 것. 큰따옴표 안 영어 = 카드가 옮겨 둔 원문. "우리 쪽 기록" = 카드가 적은 우리 계산 · 방침 (논문 값 아님). "내 대조" = 카드에 적힌 숫자끼리 맞춰 본 것 (새 측정 아님 · 카드 문제 절에만 씀). 랩 표준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³) 은 고정 — 다른 값은 "랩 표준과 다른 문헌 값" 으로만 적는다.

**인용 금지 표지가 붙은 값 (숫자로 옮기지 않음 · 위치만)**: galvezaranda2025 L113–121 · L372 (Fig 8 = 94/6 heat map · "인용 금지 대상") · L564–566 (RDF R² 분모 추정 "TREND 전용 — 숫자로 인용 금지") · L382 (보충영상 "내용 인용 금지"); han2025 L42 · L169 (toughness "절대값 인용 금지"); hare2026 L606–607 (DEM G 의 실 NMC 대비 연화 배수 "논문 주장으로 인용 금지" — 그 배수가 적힌 자리 L99 · L437 · L456–458 · L535) · L608–609 (Péclet "절대값을 인용하지 말 것" — 값 자리 L168); jadidi2023 L408 (§7 비교표 "원고에 그대로 인용하지 말 것").

---

## a. 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선 · 진밀도 · 질량 기준 · 누른 채 / 뺀 뒤

이 배치에 없음 (순수 SE 의 압력별 기공 곡선을 가진 카드 없음). 관련만:
- [a] hippauf2019_dry_film_ptfe_sulfide_cathode_sheet | 순수 SE 펠릿 (100.0 mg) σ 3.1 mS/cm 의 펠릿 밀도 = 본문 1.8 · 그림 범례 1.7 g/cm³ · 펠릿 성형 압력은 카드에 없음 | §3-4 L100 · §10-1 L258 · Fig 5A | [인쇄] | 기공 곡선 아님 · 밀도 두 값 (카드가 이미 표시)
- [a] hippauf2019_dry_film_ptfe_sulfide_cathode_sheet | 이론 밀도 식 (SI 식 S1 · 질량 분율 기준) ρ_comp = 1 / Σ(m_i / (100·ρ_i)) · (1 − P/100) 의 SE 진밀도 ρ_SE 1.9 g/cm³ (ρ_AM 4.8 · ρ_CA 2.26 · ρ_B 2.2) | §3-2 L83 | [인쇄] SI p.1 | 랩 표준과 다른 문헌 값 (LPSCl 1.64)
- [a] hong2026_sulfide_cathode_binder_digitaltwin | 디지털트윈의 LPSCl 밀도 1.86 g/cm³ (NCM 5 · Super C 1.6 g/cm³) | §2.4 L116–119 | 표지 없음 | 랩 표준과 다른 문헌 값 · 재구성 입력값이지 측정 곡선 아님
- [a] hong2026_sulfide_cathode_binder_digitaltwin | pristine LPSCl σ 1.87 → butyl butyrate 노출 뒤 0.53 mS/cm (AC 임피던스 · XRD 결정 변화 없음) · 셀 조립용 SE 펠릿 80 MPa | §4.1 L192–194 · §2.2 L98 · Fig S6 · S7 | 표지 없음 | 기공 · 밀도 값 없음
- [a] jadidi2023_dem_batch_solid_mixers_review | ρ_SE 1.64 g/cm³ (ρ_CAM 4.77 · bazzoun2026 카드에서 가져온 값 · "우리 덱의 실제 입력 밀도는 별도 확인 필요") | §4.9.3 L346 | 카드 인용 | 랩 표준과 같은 값 · 기공 곡선 아님
- galvezaranda2025 · han2025 · hare2026: 순수 SE 없음.

## b. 압력을 뺄 때 되돌아오는 양 · 잰 방법

이 배치에 없음 (압밀 탈압 되돌아옴을 잰 카드 없음). 관련만:
- [b] han2025_icep_conductive_elastic_binder | 전극 나노압입 탄성 회복률 ICEP 48.0 % vs PVDF 35.8 % (2.0 mN · 깊이 936.1 vs 3345.2 nm) — 카드: "탄성 binder → 소성변형 최소" | §3c L61–63 · Fig 2j | stated | 압입 회복률 (계산식 카드에 없음) — 압밀 탈압 되돌아옴과 다른 양 · 액체 LIB 전극
- [b] hong2026_sulfide_cathode_binder_digitaltwin | operando pressiometry = 압력 센서로 단위용량당 압력 변화 Δ(ΔP)_Q [MPa·g·(A·h)⁻¹] (LTO zero-strain 음극으로 양극만 분리): Pwd 1.88 · S-Pwd 1.89 · NBR 1.99 · PTFE 1.74 | §2.3 L105–106 · §4.3 L244–248 · Fig 3a · S16 · S17 | 표지 없음 | 사이클 중 부피 변화 지표 (탈압 아님) · 고정 구속 아래 치수 변화를 압력으로 재는 방법의 예
- [b] hippauf2019_dry_film_ptfe_sulfide_cathode_sheet | 압연 막 ≈200 µm (기공 ≈50 %) → 300 MPa 뒤 ≈100 µm · 전셀은 300 MPa 1 회 가압 뒤 외부 가압 없이 100 사이클 93.6 % · SE 층 · 양극 거시 균열 없음 | §3-2 L81–82 · §3-7 L151–154 | [인쇄] | 탈압 뒤 두께 변화를 따로 재지 않음

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 세기와 견줄 환산

SE 의 항복 · 경도 · 크리프 값은 이 배치에 없음. 일축 항복 세기와 견줄 환산 (H/3 류) 은 이 배치 어느 카드에도 없음. 관련만:
- [c] han2025_icep_conductive_elastic_binder | 바인더 필름 나노압입 E 6.03 · H 0.42 GPa (ICEP) vs 3.73 · 0.34 GPa (PVDF) · 0.1 mN · 깊이 96.5 vs 120.0 nm (카드: 표면 / 유리질 hard-block 지배 + Oliver–Pharr 고분자 과대 경향) | §3a L39–40 · Fig 1c | stated | 바인더 (SE 아님) · 환산 없음
- [c] han2025_icep_conductive_elastic_binder | 전극 나노압입 E 1.57 · H 0.15 GPa (ICEP 전극) vs 0.11 · 0.014 GPa (PVDF 전극) · 2.0 mN | §3c L61–62 · Fig 2j | stated | 다공 고분자 복합 전극 — MPM E_eff 와 동일시 금지 (§7-⑦ L133)
- [c] han2025_icep_conductive_elastic_binder | 필름 인장 flow stress ≈2.7 MPa plateau (PVDF ≈9 MPa 피크 뒤 조기 파단) · 초기 기울기 E_tensile ~10–25 MPa | §3a L43 · Fig 1a | digitized (추세) | 카드: MPM binder σ_y 스케일 후보 (§8-②) · E 는 프로브에 따라 3 자릿수 차 (§10 L171–172)
- [c] hippauf2019_dry_film_ptfe_sulfide_cathode_sheet | SE 연성 서술 — "SE 는 냉간 압축으로 입계가 사라질 만큼 연성" (값 없음) | §4-2 L165 | [인쇄] 서술 (p.5) | 정성
- hare2026 · hong2026 · jadidi2023 · galvezaranda2025: 항복 · 경도 값 없음 (hare 는 Hertz–Mindlin 순수 탄성 · §4.2 L217–219).

## d. 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

이 배치에 없음 (단단한 + 무른 입자 혼합 압축의 하중 몫 · 재밍을 다룬 카드 없음).

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 · 대안마다 맞춘 값 수

큰 변형에서 깨지는 범위를 수치로 준 카드 없음. MDR · EEPA · Thornton–Ning · Storåkers · 다접촉은 이 배치 어느 카드도 다루지 않는다. 관련만:
- [e] hare2026_dem_pept_dry_mixing_nmc622_eirich | Hertz–Mindlin (법선 eq 5 · 접선 eq 6) + JKR (eq 7) · 소성 없음 — 저자: NMC 가 단단해 고속 충돌에서도 소성 없음 · 카드: 이 가정은 비구속 전단 유동에 한해 방어되고 300 MPa 구속 압밀은 Bazzoun · Varkey 가 탄소성 / 다접촉을 도입하는 영역 · 맞춘 값 = Table 3 값 전체가 [85] Lischka & Nirschl 2023 보정 세트 (그중 몇 개를 맞췄는지 카드에 없음) | §4.2 L210–221 · §4.3 L230–236 | stated · 카드 풀이 | eq 6 G* 분모 · eq 7 JKR 둘째 항 γ 누락 = 인쇄 오타 (L216 · L228–229)
- [e] jadidi2023_dem_batch_solid_mixers_review | 분야 표준 팔레트 (Table 4) — Elastic: Hertz · linear spring (자유유동) / JKR · DMT (점착); Inelastic: hysteretic spring (Walton–Braun) / elasto-plastic adhesive (Hare 2015 · Luding 2008 · Pasha 2014 · Thakur 2014) · 식은 생략 · 카드: 우리 hooke/hysteresis + adhesion stiffness = [Free flowing × Inelastic] 칸 + 점착항 | §4.2 L103–116 | stated · 카드 풀이 | 큰 변형 범위 · 맞춘 값 수 서술 없음
- [e] jadidi2023_dem_batch_solid_mixers_review | rolling resistance 세 모델 (A 일정토크 · B 점성 · C 탄소성 spring-dashpot) — [원저 Ai 2011] "Model C 가 가장 적합" | §4.1 L99 | stated | 비구형 대리 (큰 변형 문제 아님)
- [e] galvezaranda2025_paml_vgg16_dem_slurry_drying | 접촉법칙 미기재 (ref [33] 로 미룸) — 카드 §12-2 요약: ref [33] = Lennard-Jones (모든 쌍) + JKR (겹친 쌍) · LAMMPS · COR 없음 (점성 감쇠로 대체) | §4-1 L213 · §12-2 L744–749 | 카드 요약 | 건조 · 소성 없음

## f. MPM 의 접촉 · 다물체 · 강체 결합 · 해상도 규칙 (지름당 셀 수) · 수치 오차 추정

이 배치에 없음 (MPM 카드 없음 · 지름당 셀 수 규칙 없음). 관련만 (복셀 해상도):
- [f] han2025_icep_conductive_elastic_binder | 카드 규칙 — 7 nm 코팅은 sub-voxel (우리 복셀 ~0.14 µm 의 1/20) 이므로 resolved 상으로 깔지 말고 계면 성질 (AM–SE 접촉 conductance 수정 · coverage modifier) 로 · fibril (PTFE) 만 resolved 시딩 | §8-③ L146–148 | 카드 풀이 | MPM 아님 · 복셀 수송 쪽 규칙

## g. 2D 결과를 3D 로 옮길 때의 경고 · 증거

이 배치에 2D → 3D 전이 경고 · 증거 없음. 관련만:
- [g] hare2026_dem_pept_dry_mixing_nmc622_eirich | depth-average 가 3D 속도장을 2D 로 접어 대조 — z 방향 구조는 대조에서 사라진다 (충진 25 mm) | §5.3 (f) L357 | 카드 풀이 | 3D → 2D 투영 (2D 계산을 3D 로 옮기는 문제 아님)
- [g] jadidi2023_dem_batch_solid_mixers_review | 리뷰 대상 전부 3D — "2D/3D 문제 아님" | §10.2 L521 | 카드 풀이 | —

## h. DEM 에서 FE · MPM 으로 넘긴 선례 · 넘긴 시점

이 배치에 DEM → FE · MPM 선례 없음. 관련만:
- [h] galvezaranda2025_paml_vgg16_dem_slurry_drying | DEM (+DL) 구조 → 복셀 (76 × 76 × 124 · 0.4 µm · 라벨 0 pore / 1 CBD / 2 AM) → GeoDict DiffuDict FV 로 D_eff · τ (z 방향 0↔1 mM Dirichlet · x·y 주기 · 프레임마다 후처리) | §3-A L93–96 · §4-5 L308–319 | stated | FE · MPM 아님 · 공극상 Fick (액체) · τ 규약 = ε / D_eff (카드: 규약 확인 필수 · L728–729)
- [h] hong2026_sulfide_cathode_binder_digitaltwin | 측정 (조성 · BET · porosity) → GeoDict GrainGeo 확률 재구성 → ConductoDict FV (상 · 하면 전위차 1 V) 로 current density · coverage | §2.4 L114–124 | 표지 없음 | DEM 에서 넘긴 것 아님 (재구성 · 고정 형상)

## i. 복합 양극 (AM + SE) 의 압력별 기공

압력별 곡선은 없고 한 압력 점 둘:
- [i] hippauf2019_dry_film_ptfe_sulfide_cathode_sheet | NCM90 (LZO) : VG-CNF : Li₆PS₅Cl = 85:2:13 wt% + PTFE 0.3 wt% · 300 MPa 뒤 ≈100 µm · 3.45 g/cm³ = 계산 기공 ≈12 % (이론 밀도 SI 식 S1 · 치밀 ≈3.92 g/cm³ → 12.0 %) · 압축 전 압연 막 ≈50 % | §3-2 L81–84 · p.3 · p.5 | [인쇄] · [우리 산술] | 압력 한 점 · 입경 [미확인] · 기공 = 측정 밀도 ↔ 이론 밀도 계산 (직접 측정 아님) · 하중 중 / 뺀 뒤 명시 없음 · ρ_SE 1.9 (랩 표준과 다른 문헌 값) · SE 13 wt%
- [i] hong2026_sulfide_cathode_binder_digitaltwin | NCM : LPSCl : Super C = 75 : 23.5 : 1.5 (Pwd) · 75 : 22.5 : 1.5 + PTFE 1 (PTFE) wt% · 350 MPa 조립 → pore volume Pwd 28.7 · NBR 29.4 · PTFE 22.3 vol% · 디지털트윈 AM 36–41 vol% | §2.2 L92–98 · §4.2 L227–238 · §7(a) L446 · Fig 2f · S15 | 표지 없음 | 재구성값 (측정 porosity 매칭 · 측정법 · 하중 상태 카드에 없음) · 활물질 mass loading 30 mg/cm² · Pwd 상별 부피분율 합과 pore 가 안 맞음 (카드 문제 11)
- [i] galvezaranda2025_paml_vgg16_dem_slurry_drying | 절대 porosity 값 없음 (오직 % 오차) · 액체 LIB 건조 · 압력 축 없음 | §0 L35 · §10-③ L601 | 카드 풀이 | —
- [i] han2025_icep_conductive_elastic_binder | porosity · 캘린더링 · 조성비 = 본문 없음 (SI) · 전극 두께 ≈230 / 190 µm 의 로딩 짝 미기재 → 밀도 · porosity 도출 불가 | §3c L65–67 | stated | 액체 LIB

## j. 카드가 스스로 적은 한계 가운데 가압 · 탈압 계산과 닿는 것

- [j] galvezaranda2025_paml_vgg16_dem_slurry_drying | 압력 · 응력 축 0 (MPa 0 회) — 사슬 3 편 (슬러리 · 건조 · 압연) 어느 것도 MPa 없음 · Heckel · 압밀 축과 원리적으로 안 겹침 | §0 L21 · §7-2 ⑤ L418–421 | stated (전수 grep) | —
- [j] galvezaranda2025_paml_vgg16_dem_slurry_drying | DL 이 r 을 출력하지 않아 반경 · 형상 변화 (bead 수축 · 사이클 반경 진동 · MPM 형상) 를 원리적으로 표현 못 함 → 출력 차원에 반경 · 형상 포함 필요 | §4-2 L235–236 · §8-5 L503–506 | 카드 풀이 | —
- [j] galvezaranda2025_paml_vgg16_dem_slurry_drying (카드에 적힌 우리 쪽 기록) | 우리 MPM scaffold 정착 porosity 가 플래튼 정지 프레임의 함수 (`--sub` 40 / 80 / 160 → 14.38 / 12.76 / 11.08 % · 수렴 안 함 · CL-04 준정적 ε_sphere 1.13 % = 실험 15.6 % 대비 14.5 %p 과압축) → 프레임 색인 surrogate 는 정지 인공물을 배운다 · 카드 제안 축 = TF 가 아니라 wallP | §7-2 L431–444 · §8-1 L486–490 | 카드 인용 (우리 정본) | 논문 값 아님
- [j] han2025_icep_conductive_elastic_binder | 압밀 porosity · Heckel · 복합 σ_eff 데이터 전무 · 나노압입 E 6 GPa 를 MPM binder 상 E 로 쓰면 안 됨 (bulk 거동은 MPa 급) · Auerbach 파괴에 binder 항 없음 | §10 L165–166 · L171–172 · §7-⑪ L137 | 카드 풀이 | —
- [j] hare2026_dem_pept_dry_mixing_nmc622_eirich | 무소성 Hertz–Mindlin 가정은 300 MPa 구속 압밀로 전이 안 됨 · 검증 축 = 속도 하나 (힘 · 응력 · 접촉수 · 편석 대조 없음) · 단분산 입력이 편석 가능성을 입력 단계에서 제거 | §4.2 L220–221 · §5.3 (a) L342–344 · §11-9 L598–599 | 카드 풀이 | —
- [j] hippauf2019_dry_film_ptfe_sulfide_cathode_sheet | 입경 [미확인] = 기공 12 % 를 다른 침대와 비교할 때 가장 큰 결손 · 12 % 는 측정 밀도 ↔ 이론 밀도 계산 · "PTFE fibrils will break during compression" 은 예상 (측정 아님) · 계면 항 없는 복셀 모델은 PTFE 에 따른 양극 계면 저항 (R4) 증가를 원리적으로 못 냄 (`CL-81`) | §10-8 L265 · §0 L36 ④ · §10-7 L264 · §7-4 L230 | [인쇄] · [추정] · 카드 풀이 | —
- [j] hong2026_sulfide_cathode_binder_digitaltwin | 디지털트윈 σ 는 입력 (자기참조) · ConductoDict FV 는 점접촉 sub-voxel 협착을 못 잡는 접촉 없는 상한 · PTFE void 억제는 75 wt% · 350 MPa 단일 조건 (PTFE cohesion 을 넣으면 이 1 점에 맞출 수밖에) · 우리 쪽도 시간 열화 · spring-back 없음 (카드: "단일 압축 스냅샷 … #285 spring-back 미구현과 같은 정체") | §10 L617–627 · §7(d) L529–531 | 카드 풀이 | —
- [j] jadidi2023_dem_batch_solid_mixers_review | 보정 = 시행착오 · 점착이면 입력이 많아 더 어려움 · 벌크 보정 ≠ 공정 예측 (Pantaleev 2017) · ML 은 훈련 설계공간 안에서만 · CG 허용조건 · 실패 모드 미제시 | §10.3 L525–532 · §4.5 L159–164 | stated · 카드 풀이 | 믹서 (압밀 아님)

## k. DEM 의 한계 (인용할 서지와 함께)

이 배치에 믿을 수 있는 겹침 · 상대밀도 상한이나 접촉 독립 가정이 깨지는 밀도를 수치로 준 카드는 없다. DEM 을 쓰거나 다룬 세 편이 적은 한계:
- [k] hare2026_dem_pept_dry_mixing_nmc622_eirich (Hare et al., Powder Technology 469, 121804, 2026) | 실크기 DEM 은 계산 불가 — 10 µm 입자 Δt ≈ 5 × 10⁻⁹ s · 0.7 kg 이면 n_p ≈ 7 × 10¹¹ → "극단적 계산부하" → 직경 200 배 (2 mm) · 46,000 입자로 축소 | §4.4 L249–250 · §3.2 L83 · L94 | stated (카드 옮김) | —
- [k] hare2026_dem_pept_dry_mixing_nmc622_eirich (Hare et al., Powder Technology 469, 121804, 2026) | 보정값 ≠ 물성 · 다른 계로 전이 불가 — "coarse graining 으로 유동거동을 정확히 예측하고 접촉모델에 필요한 재료 파라미터를 추정하기 위해 여러 보정 실험을 썼다" · 저자 결론 "다른 스케일로 확장하려면 신중한 재보정 필요" · γ 는 측정값이 아니라 2 mm 입자가 bulk 유동을 재현하도록 맞춘 유효값 | §4.4 L252–260 · §4.3 L232–236 | stated (카드 옮김) | 강성 연화 배수 숫자는 인용 금지 (L606–607) — 안 옮김
- [k] hare2026_dem_pept_dry_mixing_nmc622_eirich (Hare et al., Powder Technology 469, 121804, 2026) | 무소성 가정 — 저자: "NMC 622 입자는 비교적 단단해서 고속 충돌에서도 유의한 소성변형을 겪을 것으로 예상되지 않으므로 Hertz–Mindlin 이 가장 적절한 모델" · 카드: 비구속 전단 유동에 한해 방어 · 300 MPa 구속 압밀에는 전이 안 됨 | §4.2 L217–221 | stated (카드 옮김) + 카드 풀이 | —
- [k] hare2026_dem_pept_dry_mixing_nmc622_eirich (Hare et al., Powder Technology 469, 121804, 2026) | 구 고정 · 형상 불변 (비구형성은 rolling friction μ_r 0.075 로만 대리) · 단분산 2 mm (실 PSD 5.5/10/17 µm 를 버림 → "편석 없음" 은 결과가 아니라 입력 가정) | §4.5 L268–273 | 카드 풀이 | —
- [k] hare2026_dem_pept_dry_mixing_nmc622_eirich (Hare et al., Powder Technology 469, 121804, 2026) | DEM 속도 분포 폭 (SD) 이 PEPT 보다 +28 ~ +56 % — 저자 설명 "DEM 은 순간속도, PEPT 는 시간평균" · 30 m/s 저속 영역 불일치는 저자도 "이유는 불분명(the reason is unclear)" | §3.4 L133–134 · §5.2 L336–337 | stated · 원문 따옴표 | 검증 축 = 속도장 하나 (§5.3)
- [k] jadidi2023_dem_batch_solid_mixers_review (Jadidi et al., Reviews in Chemical Engineering 39(5), 729–764, 2023) | 계산 한계 — 시간스텝 = Rayleigh time 20–30 % ("usually no more than a few microseconds") · 시뮬 가능 공정 시간 최대 수 분 · 전형 규모 수십만 입자 · mm 급 · 산업 규모 (수억–수십억 입자) 현 하드웨어로 불가 · "미세(submillimeter) 분말을 시뮬할 때 더 심해진다 (더 작은 스텝이 필요하므로)" | §3 L46–49 · §4.4 L147–148 · §10.3 L525 | stated · 원문 따옴표 · 카드 옮김 | mm 급 자유유동 분말 기준 (µm 점착 체제 아님 · 카드 L149)
- [k] jadidi2023_dem_batch_solid_mixers_review (Jadidi et al., Reviews in Chemical Engineering 39(5), 729–764, 2023) | 입력은 직접 측정이 거의 불가 → 보정은 시행착오 — "특정 입자·분말의 DEM 입력을 직접 현미경 측정으로 얻는 것은 매우 어렵고 비싸며, 불가능하지는 않더라도" (Benvenuti 2016) ⇒ "통상 보정은 시행착오(trial and error) 로 수행된다" · "점착 입자를 시뮬레이션할 때 보정은 훨씬 더 어려워진다 — 접촉모델과 입자물성에 사용자가 정해야 할 입력이 더 많기 때문" (Pantaleev 2017; Safranyik 2017) · "어떤 경우엔 보정이 공정 시뮬 자체보다 더 오래 걸린다." | §4.3 L127–130 · §10.3 L526 | stated (카드 옮김) | —
- [k] jadidi2023_dem_batch_solid_mixers_review (Pantaleev et al. 2017 — 리뷰 Table 12 재인용 · 원저 서지는 카드에 없음) | 벌크 보정이 공정 예측으로 전이되지 않음 — "보정 단계에서 DEM 과 FT4 측정이 근접 일치했음에도 불구하고, 믹싱 시스템 DEM 모델은 실험으로 측정한 혼합속도를 정성적으로만 예측할 수 있었다" (visco-elasto-plastic adhesive · Thakur 2014 모델 · 건조 · 습윤 분말) | §3 L63 · §9 L493 · §8-③ L454 | stated (카드 옮김) | 믹서 (압밀 아님)
- [k] jadidi2023_dem_batch_solid_mixers_review (Jadidi et al., Reviews in Chemical Engineering 39(5), 729–764, 2023) | 형상 — 문헌 80 % 가 구형 · 3D 다면체 접촉검출이 전체 계산시간의 80 % (Zhong 2016 인용) · 카드: 전 문헌 강체 구 (소성 형상변화 없음) | §3 L43 · L50 · §7 L427 | stated · 카드 풀이 | —
- [k] jadidi2023_dem_batch_solid_mixers_review (Alizadeh et al. 2014b — 리뷰 Table 9 재인용 · 원저 서지 카드에 없음) | "정지마찰 계수와 Young's modulus 가 입자 혼합 동역학에 유의한 영향" — 카드: 우리 18× 연화가 재배열 통계까지 바꿀 수 있다는 같은 방향의 독립 관측 | §9 L492 | stated (카드 옮김) · 카드 풀이 | 회전드럼 혼합
- [k] jadidi2023_dem_batch_solid_mixers_review (Jadidi et al., Reviews in Chemical Engineering 39(5), 729–764, 2023) | coarse-graining 의 허용 조건 · 실패 모드 · 상한 l · 검증 기준을 한 줄도 적지 않음 — 보존되는 것을 "평균 거동" 이라고만 (Sakai 2016) · 카드 판정 "판정이 없다 · 전면 허용 서술" | §4.5 L154–164 | 카드 풀이 | "리뷰가 CG 를 검증했다" 로 읽지 말 것 (L510)
- [k] galvezaranda2025_paml_vgg16_dem_slurry_drying (Galvez-Aranda, Fernandez & Franco, ACS Appl. Mater. Interfaces 17, 32150–32162, 2025) | 논문: DEM 한계를 말하지 않음 — DEM 을 블랙박스 적분기로만 씀 (접촉법칙 · E · ν · μ · COR · 응집 · 건조 표현 미기재) · 겹침을 오류로 취급 "particle overlaps … not physically possible" → 카드: 강체구 규약 · 접촉 소성도 형상 소성도 없다 = 우리 DEM 과 같은 칸 | §4-1 L206–222 · §4-2 L234 · §7-1 L391 | 원문 따옴표 (부분) + 카드 풀이 | 원문 문장은 DL 이 낸 겹침에 대한 것
- [k] galvezaranda2025_paml_vgg16_dem_slurry_drying (Galvez-Aranda, Fernandez & Franco, ACS Appl. Mater. Interfaces 17, 32150–32162, 2025) | 시간 규모 — 전체 건조 1.5 ms 모사 ↔ 실제 대류건조 수십 초–수 분 · DEM 시간 ↔ 실제 공정 시간 매핑 없음 ("drying rate" 는 모델 파라미터) | §10-⑤ L623–625 | 🧮 (카드 산술) · 카드 풀이 | 카드의 지적 · 논문 문장 아님
- [k] hippauf2019_dry_film_ptfe_sulfide_cathode_sheet (Hippauf et al., Energy Storage Materials 21, 390–398, 2019) | 논문: 말 없음 (실험 · DEM 없음) · 카드 [추정]: SE 가 더 적은 이 논문 (13 wt%) 이 우리 300 MPa DEM (18.4 wt% · ε_sphere 15.0–19.2 %) 보다 치밀한 것은 입경 [미확인] · CNF · 연성 SE (실제 소성) 때문일 수 있고 "우리 강체 DEM 은 소성 흐름이 없어 기공 바닥이 높다 (frame [2])" | §7-1 L212 | [추정] (카드) | Hippauf 2019 의 주장이 아님
- [k] hong2026_sulfide_cathode_binder_digitaltwin (Hong et al., Energy Storage Materials 86, 104930, 2026) | 논문: 말 없음 (DEM 안 씀 — GeoDict 확률 재구성) · 카드 풀이: 우리 DEM (강체구 + 겹침 대리) 도 그들 GeoDict (고정형상) 도 소성 입자 형상변화가 없다 | §10 L630–631 | 카드 풀이 | 논문 주장 아님
- [k] han2025_icep_conductive_elastic_binder (Han et al., Adv. Mater. 37, 2506266, 2025) | 말 없음 (DEM 을 쓰지 않음 — 실험 + DFT 흡착만) | §4 L93 | — | —

## l. 소성변형이 왜 어려운가 · 택한 우회와 그 값 (인용할 서지와 함께)

이 배치에서 입자 계산에 소성을 넣기 어려운 이유를 직접 설명한 논문은 없다. 우회 · 맞춘 값 · 검증 · 비용만:
- [l] hare2026_dem_pept_dry_mixing_nmc622_eirich (Hare et al., Powder Technology 469, 121804, 2026) | 소성을 넣지 않은 이유 = 가정 (NMC 단단 · 이 공정은 접촉응력 낮음) → 항복캡 · 잔류겹침 · Thornton–Ning 류 탄소성 분기 없음 · 우회 = 소성 대신 보정된 유효 강성 (G 0.1 GPa · ν 0.25 — 유동 보정 + 시간스텝 경제) · 맞춘 값 = Table 3 세트 전체 (G · ν · e · μ_s · μ_r · γ_pp · γ_pw — 몇 개를 맞추고 몇 개를 고정했는지 카드에 없음 · [85] Lischka & Nirschl, Energy Technol. 2023) · 보정 실험 = 정적 안식각 · Schulze 전단셀 동적 안식각 · 회전 실린더 · 경사판 · 검증 = PEPT 속도장 (중앙값 ≤ 0.9 % · 평균 ≤ 8.4 %) · 비용 = 46,000 입자 · 20–30 s 모사 · DEM Δt ≈ 3.4 µs | §4.2 L217–219 · §3.2 L81–95 · L100 · §4.7 L299–305 · §5.1 L320–321 | stated · digest 산술 (Δt) | 보정 곡선 · 잔차 · 민감도는 논문에 없음 ([85] 외주 · L304)
- [l] galvezaranda2025_paml_vgg16_dem_slurry_drying (Galvez-Aranda, Fernandez & Franco, ACS Appl. Mater. Interfaces 17, 32150–32162, 2025) | 소성 다루지 않음 (말 없음 · 우회 없음) — DL 출력이 (x, y, z) 3 개뿐이라 반경 · 형상 자유도를 원리적으로 표현 못 함 · DEM 투영자도 위치만 완화 | §4-2 L234–236 · §7-1 L393 | 카드 풀이 | —
- [l] galvezaranda2025_paml_vgg16_dem_slurry_drying 의 ref [33] (Xu et al., J. Power Sources 554, 232294, 2023 — 카드 §12-2 요약 · 원 카드 `xu2023_realistic_am_shape_cgmd_calendering`) | 부피 변화의 우회 — 건조를 CBD bead Ø6.2 → 1.3 µm 순간 수축 + force field 전면 교체 (LJ 우물 CBD ×10⁶ · AM–AM 인력 켬) 로 표현 · 최종 두께는 실험 밀도 · porosity 로 미리 계산해 지정 ("건조 두께는 예측이 아니라 입력") · LJ + JKR (LAMMPS) · E AM 135 GPa · ν 0.3 · timestep · 플래튼 속도 미기재 · 검증 = 슬러리 밀도 2 점 · porosity–CD 실험 8 점 · µ-XCT τ 는 dilation–erosion 인자를 τ 에 맞춰 골라 독립 검증 아님 | §12-2 L744–757 | 카드 요약 | 이 논문의 값이 아님 · 원 카드에서 확인 필요
- [l] hippauf2019_dry_film_ptfe_sulfide_cathode_sheet (Hippauf et al., Energy Storage Materials 21, 390–398, 2019) | 모델 없음 (말 없음) — 실험 관찰만: SE 는 냉간 압축으로 입계가 사라질 만큼 연성 (p.5 서술) · 압축 중 PTFE 섬유 파단은 예상: "The binder is not expected to have a positive effect on the cathode integrity after cell assembly as the PTFE fibrils will break during compression. The binder is just required for cell preparation. Afterwards, it only contributes to the cell impedance." | §4-2 L165 · §3-7 L155 | [인쇄] 서술 · 원문 따옴표 | 둘 다 측정 아님 (예상 · 서술 · §10-7 L264)
- [l] hong2026_sulfide_cathode_binder_digitaltwin (Hong et al., Energy Storage Materials 86, 104930, 2026) | 말 없음 — 디지털트윈은 고정 형상 입자 (NCM 볼록 구 · LPSCl 다면체 · CBD 구) · 압력 → 구조 예측 없음 · 우회 = 측정 조성 · BET · porosity 에 맞춘 확률 재구성 + 실측 σ_ion 으로 각 모델 내부 형태 (coverage) 보정 · 검증 = 상별 부피분율 목표 ↔ 재구성 대조 (Fig S15b) · LPSCl 피복 추세 ↔ GITT (Fig S13) · 비용 카드에 없음 | §2.4 L114–124 · §4.2 L218 · L236–238 · §7(b) L477 | 표지 없음 | —
- [l] jadidi2023_dem_batch_solid_mixers_review (Jadidi et al., Reviews in Chemical Engineering 39(5), 729–764, 2023) | 소성이 어려운 이유 서술 없음 · Table 4 의 [Cohesive × Inelastic] = "Elasto-plastic adhesive models" 범주만 (식은 "이 연구에서는 간결성을 위해 접촉모델과 그 식을 보고하지 않는다") · 보정 파라미터 목록에 plasticity ratio 가 나란히: "the DEM interaction parameters such as coefficient of static and rolling frictions, coefficient of restitution, surface energy, plasticity ratio, and adhesion stiffness as well as particle properties such as shear modulus are systematically varied and their influence on the bulk response (i.e. macroscopic response obtained from standard characterization tests such as angle of repose or shear cell tests) is monitored." | §4.2 L107–114 · §4.3 L121 | stated · 원문 따옴표 · 카드 옮김 | 노브 사이 환산 (k_c ↔ Γ 등) 은 주지 않음 (L126)
- [l] jadidi2023_dem_batch_solid_mixers_review (Pantaleev et al. 2017 — 리뷰 Table 12 재인용 · 원저 서지 카드에 없음) | Tables 7–13 에서 [Cohesive × Inelastic] 칸을 실제로 쓴 유일한 연구 = visco-elasto-plastic adhesive (Thakur 2014) · 건조 · 습윤 분말 · FT4 레오미터 보정 → 혼합속도는 정성 예측만 · Luding 2008 판은 아무도 안 씀 | §4.3 L140–141 · §8-③ L454 | stated · 카드 집계 | 맞춘 값 개수 · 비용 카드에 없음
- [l] han2025_icep_conductive_elastic_binder (Han et al., Adv. Mater. 37, 2506266, 2025) | 말 없음 (입자 계산 없음) | — | — | —

## m. 받아들일 통찰 (무엇 → 어디 · 왜)

- [m] galvezaranda2025_paml_vgg16_dem_slurry_drying | 기공 연산자의 분모 (N_total) 를 정의하지 않으면 전극 위 빈 공간이 기공으로 계상되거나, crop 규칙이 두께 정보를 기공 오차에 섞는다 → 분모 = 판 사이 전극 부피 · 규약 키 porosity_convention (sphere_sum / union / voxel_label) 을 결과 전에 적는다 → 단계 0 | §10-③ L589–602 · §12-6 L769–772 | 카드 풀이 · 카드 제안 | 판별 불가 사례 (논문이 절대 porosity 를 안 줌)
- [m] galvezaranda2025_paml_vgg16_dem_slurry_drying | 판정 지표에서 "정의상 맞는 칸" 을 뺀다 — 시드 4 프레임 R² 1.000 (21 점 중 4 점 = 19 %) · RDF 배제영역 (≈0.88 µm 아래) 400 bin 중 88 은 겹치지만 않으면 맞는 칸 → RDF R² 는 구조 충실도의 약한 판별자 → 단계 0 · 결과 전 대조 항목 (판별력 있는 관측량만 판정에) | §10-① L553–571 · §5-2 L336–337 | 🧮 · 그림 판독 근사 | R² 분모 추정값은 인용 금지 (L566) — 안 옮김
- [m] galvezaranda2025_paml_vgg16_dem_slurry_drying | 짧은 물리 보정 단계 (nDEM) 를 정확도 다이얼로 가정하지 않는다 — nDEM 5000 → 10000 에서 porosity 단조 개선 0/4 · 10000 이 5000 보다 나쁜 경우 3/4 (Fig 6a) · nDEM 0 음성 대조 + trivial baseline (persistence · 등속 외삽 · affine 붕괴) 을 같은 투영자로 통과시켜 대조 → 흐름 밖: 반복 보정 루프 · 대리모델 검증 (예: 정착 step 수 늘리기) | §10-⑥ L627–643 · §10-⑧ L649–674 · §7-4 L472–476 | 🧮 · 카드 제안 | Fig 8 쪽 집계는 복사 오류 그림이라 쓰지 않음
- [m] galvezaranda2025_paml_vgg16_dem_slurry_drying | 가속 배수를 세 가지로 적는다 — step 단위 · 시드 포함 end-to-end · 손익분기 런 수 (논문 14.25× ↔ 시드 포함 4.77× · 천장 6.67×) → 흐름 밖: 계산 비용 보고 (surrogate · 가속) | §3-D L160–175 · §7-4 L470–471 | derived(ours) | —
- [m] han2025_icep_conductive_elastic_binder | 7 nm 코팅은 sub-voxel 이므로 resolved 상이 아니라 계면 성질 (AM–SE 접촉 conductance · coverage modifier) 로 넣고, fibril (PTFE) 만 resolved 시딩 — "coat = interface property, fibril = resolved phase" → 흐름 밖: Rint ② (계면 막 표현 · 첨가제 시딩 규칙) | §8-③ L146–148 | 카드 풀이 | 형상은 흡착 화학 + 공정이 정함 (§7-③ L129)
- [m] han2025_icep_conductive_elastic_binder | 막 ASR = t / σ_b 스케일 논증 — 7 nm 이온전도 코팅 ~5 × 10⁻³ Ω·cm² (계면 예산에서 사실상 0) ↔ 같은 두께 절연 코팅 (σ ≤ 1e-10 S/cm) ≥ 10³–10⁴ Ω·cm² (지배) → 흐름 밖: Rint ② 계면 저항 예산 (막 화학이 coat 허용 여부를 정함) | §7-④ L130 · §9 L158–160 | 우리 계산† (카드) | 논문 stated 아님 · σ_b 0.135 는 swollen 추정 (건식 이식 금지)
- [m] han2025_icep_conductive_elastic_binder | 함정 셋 — SAICAS 박리 N/m 는 소성 소산을 포함한 apparent 값이라 고유 G_c (Bucci) 와 직접 비교 금지 · 나노압입 E (필름 6.03 GPa) 는 표면 · 소변형 값이라 MPM 바인더 상 bulk E 로 쓰지 않음 · 전극 나노압입 E 1.57 GPa 와 MPM E_eff 1.53 GPa 의 근접은 우연 (물리 기원 다름 · 동일시 금지) → 결과 전 대조 항목 (견줄 외부 값 고르기) · 흐름 밖: 파괴 · 접착 값 대조 | §3c L60 · §7-⑥ L132 · §7-⑦ L133 · §10 L171–172 | stated · 카드 풀이 | —
- [m] han2025_icep_conductive_elastic_binder | 두께 방향 반응 균일성의 z-분해 실측 꼴 — confocal Raman E_g/A₁g 강도비 top / bottom (PVDF bottom 0.84 = pristine 0.83 → 바닥 미반응 · ICEP 0.98 / 0.99) → 흐름 밖: graded-z (A7) 출력에 z 별 반응도 프록시를 두면 직접 비교 관측량이 생김 | §3e L89 · §6 L116–117 · §8-⑤ L151–152 · Fig 6d–f | stated | 액체 LIB
- [m] hare2026_dem_pept_dry_mixing_nmc622_eirich | 여러 평균창 (5 / 10 / 15 s) 의 분포를 겹쳐 시간수렴을 보이는 그림 형식 — 겹침은 수렴의 필요조건이지 충분조건이 아님 · 속도 사다리와 같이 낸다 → 단계 4–6 정착 · 정상상태 판정 (단계 0 에 결과 전 등록) | §C-1 L522–525 · §9-③ L561–563 · Fig 11d · 12d | stated · 카드 풀이 | —
- [m] hare2026_dem_pept_dry_mixing_nmc622_eirich | Lacey 판독 규약 — 칸 구성 (radial 6 × azimuthal 8 × vertical 30) 을 mesh-independence 로 정했다는 판정만 있고 곡선 · 수치는 안 실림 · 카드: Lacey 는 칸 수에 강하게 의존 (칸이 작으면 M 이 낮아짐) · M₀ 가 다르면 k 를 직접 비교 금지 → 흐름 밖: 믹서 확인 블록 M 판독 (칸 민감도 수치 · M₀ 를 같이 보고) | §3.6 L180 · §7 L410–414 · §3.5 L159–160 | stated · 카드 풀이 | 정의식 (정규화) 을 논문이 특정하지 않음 (L406–409)
- [m] hare2026_dem_pept_dry_mixing_nmc622_eirich | 점착 세기는 γ 절대값이 아니라 무차원 Bond 수 F_po / W (F_po = (3/2)πγR*) 로 문헌과 견준다 — γ 가 55 배 다른 두 논문이 Bond 수로는 같은 O(1–10) 대역 · JKR 식을 구현할 때 인쇄된 eq 7 (점착항 γ 누락) 을 그대로 쓰지 않는다 → 흐름 밖: 믹서 D2 · D3 (SE–SE 응집 세기를 문헌과 견줄 때 · 결합 규칙 구현) | §4.3 L228–229 · L239–246 · §11-10 L600–601 | digest 산술 · 카드 확인 | 자매 카드 lischka2025 의 독립 같은 결론 (L245–246)
- [m] hare2026_dem_pept_dry_mixing_nmc622_eirich | 분포 대조는 median 을 주지표, mean · SD 를 보조로 — DEM 순간값 ↔ 실험 시간평균은 분포 폭이 구조적으로 다르다 (SD +28 ~ +56 %) · 필터 (점유율 평균 − 1 SD 제거) 가 관심 영역 (30 m/s rotor 근처) 데이터를 가장 많이 지운다 → 결과 전 대조 항목 (분포를 견줄 때 시간 평균창 · 필터를 맞춰 적는다) | §3.4 L130–134 · §C-1 L528–529 · §5.3 (e) L354–356 | stated · 카드 풀이 | —
- [m] hippauf2019_dry_film_ptfe_sulfide_cathode_sheet | 기공 = 측정 밀도 / 이론 밀도 (SI 식 S1 · 상별 진밀도 ρ_AM 4.8 · ρ_SE 1.9 · ρ_CA 2.26 · ρ_B 2.2) — 문헌 기공을 우리 값과 견줄 때 문헌이 쓴 진밀도를 적고 (SE 1.9 ≠ 랩 1.64) 같은 진밀도로 센 값끼리만 견준다 → 단계 0 (기공 연산자) · 결과 전 대조 항목 | §3-2 L83–84 | [인쇄] · [우리 산술] | —
- [m] hippauf2019_dry_film_ptfe_sulfide_cathode_sheet | 같은 총 SE 코팅 비교 실험에서 PTFE 함량 (≤ 0.3 wt% 권장 [추정]) · 섬유화 세기 · 로딩을 팔 사이에서 고정 — 0.7–1 wt% 부터 양극 계면 저항 ↑ (41 → 61 Ω) · 0.1 wt% 는 더 세게 갈아 불균일 (202 vs 215 mAh/g) · 무바인더 2.5 ↔ DF 6.5 mAh/cm² 로딩 차가 비교를 흐림 → 흐름 밖: 믹서 · 코팅 실험 설계 (V1–V3) | §7-3 L222–226 | [인쇄] · [판독] · [추정] | —
- [m] hippauf2019_dry_film_ptfe_sulfide_cathode_sheet | 혼합 상태가 DF · 압연 · 300 MPa 를 통과한다는 진술 ("the DF process does not influence the particle assembly" · SEM ×1,000 정성 · Frankenberg 2025 도 같은 진술) → 혼합 DEM → 압축 DEM 사슬에서 섬유화 단계를 건너뛰는 근사의 정성 근거 · 정량은 DF 전 · 후 단면으로 직접 확인 → 흐름 밖: 믹서 → 압축 사슬 (Ⓒ → 단계 5 초기 상태) | §3-2 L86 · §7-2 L218 · §8-3 L245–247 · Fig 4 | [인쇄] · 정성 | 정량 근거 아님 (L247)
- [m] hippauf2019_dry_film_ptfe_sulfide_cathode_sheet | 함정 — 순수 SE 펠릿 (그림 1.7 g/cm³) 보다 PTFE 막 (1.8) 이 더 치밀한데도 σ 가 3.1 → 2.7 이라 같은 밀도에서의 PTFE 몫은 13 % 보다 클 수 있다 → σ 감소를 견줄 때 밀도를 맞춘다 → 흐름 밖: σ₀ 기준 상태 · 첨가제 σ 감소 대조 | §3-4 L104 · §10-1 L258 | [우리 산술] · [추정] | 본문은 펠릿 1.8 이라 적어 두 값
- [m] hong2026_sulfide_cathode_binder_digitaltwin | 교락 변수를 차이 짝으로 떼는 4 구성 설계 — Pwd (무용매 · 무바인더) · S-Pwd (용매만) · NBR (용매 + NBR) · PTFE (PTFE 만): S-Pwd − Pwd = 용매 효과 · NBR − S-Pwd = NBR 효과 · PTFE − Pwd = PTFE 효과 → 흐름 밖: 첨가제 · 믹서 실험 팔 설계 (한 팔이 한 요인만 다르게) | §2.1 L80–89 · Fig S2 | 표지 없음 | —
- [m] hong2026_sulfide_cathode_binder_digitaltwin | 함정 — 디지털트윈의 σ_ion 은 입력 (실측으로 내부 형태를 보정) 이라 그 coverage · current density · 기공을 "모델 예측" 으로 견주면 자기참조 → 외부 값을 고를 때 그 값이 원 모델의 입력이었는지 표지를 붙인다 → 결과 전 대조 항목 | §2.4 L123–124 · §10 L617–620 | 카드 풀이 | —
- [m] hong2026_sulfide_cathode_binder_digitaltwin | 같은 소재 복합 양극에서 PTFE 1 wt% 가 기공을 6.4 %p 낮춤 (22.3 vs 28.7 vol% · 단일 조건) — 우리 모델은 PTFE 를 σ = 0 장애물로만 넣어 역학 몫이 없으므로 PTFE 있는 팔의 기공 · σ 비교에 "역학 몫 없음" 한정어 → 단계 5 · 흐름 밖: Rint ② PTFE 표현 | §4.2 L227–234 · §7(c) L504–518 · §10 L625–627 | 표지 없음 · 카드 풀이 | 정량은 1 점 외삽 (L627)
- [m] hong2026_sulfide_cathode_binder_digitaltwin | σ_ion 측정 조건 = 350 MPa 조립 뒤 30 MPa 고정 · full-blocking Li/LPSCl/cathode/LPSCl/Li AC (10 mHz–1 MHz) — 조립 압력과 측정 압력을 따로 적는다 (우리 300 MPa 표적과 다름 · Bazzoun 400 / 25 MPa) → 결과 전 대조 항목 (단계 7) | §2.2 L98–99 · §2.3 L103 · §7(a) L440–443 | 표지 없음 | —
- [m] jadidi2023_dem_batch_solid_mixers_review | 분산 기반 혼합지수 (Lacey · RSD) 를 우리 침대에 그대로 쓰면 개수 통계가 SE 에 지배 (크기비 12 : 4 : 1 → 부피비 1728 : 64 : 1) · 칸을 크게 잡으면 어떤 침대든 "잘 섞였다" → 칸 구성 · 개수 / 부피 가중 · σ_r² 정의를 결과 전에 적는다 → 흐름 밖: 믹서 확인 블록 · CLMI 부지표 (Ⓒ) | §4.7.4 L222–235 · §4.7.5 L244 · §8-② L447–449 | 카드 [우리 분석] | 이 경고는 리뷰에 없다 — 리뷰 인용으로 달면 날조 (L509)
- [m] jadidi2023_dem_batch_solid_mixers_review | Pantaleev 2017 (리뷰 Table 12 재인용): FT4 보정은 근접 일치했지만 혼합속도는 정성적으로만 예측 → 유동성 (AOR · 전단셀 · FT4) 앵커의 값은 "절대 예측" 이 아니라 "점착 노브가 실물의 어느 밴드인가" 까지로 한정해 계획 → 흐름 밖: 믹서 D3 (SE–SE 점착 유동성 실측 앵커) · 후보 D0 (보정 ≠ 예측) | §8-③ L452–455 · §9 L493 | stated (카드 옮김) · 카드 판단 | —
- [m] jadidi2023_dem_batch_solid_mixers_review | 점착은 혼합에 단조롭게 나쁘지 않다 — 매우 약한 점착 (F_cohesion/W_p 0.1) 은 자유유동보다 더 잘 섞임 (Chaudhuri 2006) · CED > 80 kJ/m³ 강점착은 악화 · 서로 다른 점착 입자 사이 점착이 없으면 균일 혼합 안 됨 (Yazdani & Hashemabadi 2019) → 결과 전 예측 방향에서 단조성을 가정하지 않는다 → 흐름 밖: 믹서 D2 (결합 규칙 · 비대칭 점착 팔) | §3 L55–56 · §9 L483–484 | stated ([원저]) | 회전드럼 · SJKR · 다른 소재계 (L484)
- [m] jadidi2023_dem_batch_solid_mixers_review | 재배열 관측량 D_ij (식 3) · Pe (식 5) · granular temperature (식 6) 은 기존 덤프의 변위 · 속도 시계열로 계산 가능 → "연화 = 재배열 대리" 를 시험하려면 압밀 단계별 D_ij 와 연화 계수 사이 예측을 런 전에 등록 (지금은 "잴 수 있다" 까지) → 후보 D0 · 단계 0 | §4.8 L275–279 · L314 · §8-④ L457–459 | 카드 [우리 분석] | 식 (3) · (6) 인쇄본에 평균 연산자 없음 — 원저 확인 (L280)

---

## 카드 문제

1. **galvezaranda2025** — 철회된 앵커 서술: §7-3 표 L459 "실험 앵커" 칸이 우리 쪽 앵커로 "Minnmann 10 %@300 MPa · Cronau overlap 11–12 % · Bazzoun EIS σ" 를 적었다 — 순수 SE 300 MPa 기공 앵커로서의 Minnmann 출처는 철회됨 (원장 `CL-94`).
2. **galvezaranda2025** — 하드웨어 코어 수 두 값: §2 메타 L60 "Intel Xeon E5-2680 v4 @ 2.40 GHz × 2 (14 core)" ↔ §3-A L98 "Xeon E5-2680 v4 × 2 (28 core)".
3. **galvezaranda2025** — (소소) 건조 수축 시작 지름: §4-2 L236 은 "vijay2025 의 건조 규약 (CBSA Ø7 → CBD 1.3 µm 수축) 이 ref [33] 에도 있다면" 이라는 가정형인데, §12-2 L750 은 ref [33] = "CBD bead Ø6.2 → 1.3 µm" 로 답했다 — §4-2 서술은 갱신되지 않았다.
4. **hare2026** — 같은 부류 (철회된 앵커): §8 표 L443 "Minnmann porosity · Cronau overlap · Bazzoun EIS 외부 앵커" · §B L517 "우리 쪽 대응 검증은 Minnmann/Cronau" (`CL-94`).
5. **hare2026** — 보정 실험 종류 수 두 서술: §4.3 L233–234 "정적 안식각 · Schulze 전단셀과 회전드럼을 쓴 동적 안식각 · 스테인리스강 경사판 시험" (세 가지 꼴) ↔ §4.7 L300–302 "보정 실험 4종: ① 정적 안식각 ② Schulze 전단셀을 쓴 동적 안식각 ③ 회전 실린더 ④ 경사판".
6. **hare2026** — (소소 · 내 대조) 같은 연화 배수를 §3.2 L99 · §8 표 L437 은 E 비 (E_CAM 161.5 GPa ↔ E_DEM 0.25 GPa) 로, §A-2 L458 은 G 비 (실 G ≈62 ↔ 0.1 GPa) 로 적는다 — 두 비는 ν 가 달라 같지 않다 (배수 숫자는 인용 금지 표지 L606–607 라 옮기지 않음).
7. **hong2026** — 철회된 앵커 서술: §8 보너스 L589 "σ/porosity 절대앵커 = Bazzoun(LPSCl) + #271(LPSCl) + Varkey(halide, 비교용) + Minnmann(LPSCl cold-press)" (`CL-94`).
8. **hong2026** — 철회된 라벨: §7(a) L449–451 · 비교표 L542 · L591–592 "Cronau 단결정 3.0" · "우리 σ_grain=3.0(단결정) + Cronau(r_SE) GB인자" — 프로젝트 원장 기준으로 3.0 = Cronau 2021 SI 의 µC 펠릿값 (`CL-91`) · Cronau(r_SE) 는 문헌이 아니라 모델 가정 (`SELF-51`) (카드 digested 2026-07-28 — 정정 전).
9. **hong2026** — 판정의 세기가 두 가지: §7(a) L429 "✅ 판정 — 우리 절대 σ_ionic은 in-range(검증됨)" · L432 "절대값 cross-validation(frame[4])" · §9 L605 "검증" ↔ §10 L613–616 "in-range ≠ 정밀 검증 · envelope 합치지 점대점 검증이 아니다 · 같은 (φ_SE, P) 에서 비교해야 진짜 검증". 또 견준 "우리 DEM σ_ionic ~0.04–0.18 mS/cm" (L426) 가 어느 σ₀ (솔버 입력 3.0 / 보고 기준 1.5) 로 낸 값인지 카드에 없다.
10. **hong2026** — 머리 표지가 내용과 다름: L3 type `FEM·digital-twin` ↔ §2.4 L121 방법 = ConductoDict "Finite Volume Method" · L12 methods `dft, elastic` — 논문에 DFT 없음.
11. **hong2026** — (내 대조) Pwd 부피분율 합: Fig S15b (L237) Pwd 목표 / 재구성 AM 36.8 / 36.2 · LPSCl 30.8 / 30.8 · CBD 2.3 / 2.3 → 고체 합 69.9 / 69.3 vol% (나머지 30.1 / 30.7 %) ↔ 같은 카드 pore volume Pwd 28.7 vol% (L229 · Fig 2f). NBR (36.3 + 29.1 + 5.2 → 29.4 ✓) · PTFE (40.8 + 33 + 3.9 → 22.3 ✓) 는 맞는데 Pwd 만 ≈2 %p 어긋난다 — 원문 확인 필요.
12. (소소) 머리 `elements` · `methods` 줄: galvezaranda2025 L6–7 "Li" · "elastic" (NMC111 · C65 · PVdF 원소 빠짐 · 접촉법칙 미기재인데 elastic) · han2025 L13 "F Li Mn O P" (NCM811 의 Ni · Co 빠짐) · hong2026 L11 "Li" 뿐.

참고 (카드 잘못 아님 — 카드가 이미 표시해 둔 원문 문제): galvezaranda2025 = Fig 8 ↔ Fig 6 행 치환 복사 32 칸 중 23 칸 (§3-C L130–158) · 초록 615 → 36 min (17.1×) ↔ 본문 684 → 48 min (14.25×) (§10-⑨ L676–687) · 94/6 문단 "In all cases … decrease" ↔ Fig 8a (§10-⑥ L640–641) · Table 1 7 번 층 95,860 ↔ 98,560 (§10-⑦ L645–647) · MSE · MAE 단위 미기재 (§10-② L573–587); han2025 = toughness 단위 "J m⁻³" ↔ S-S 면적 (L42 · L169 — 숫자 안 옮김); hare2026 = 본문 x@10 m/s k 0.454 ↔ Fig 15d 범례 0.46426 (L162–163 · L602) · 인쇄식 오류 3 (eq 6 G* 분모 E₂ · eq 7 JKR γ 누락 · eq 11 1/N 누락 · L600–601) · z 축 k 본문 "영향 없음" ↔ 범례 약한 단조 감소 (L156–158); hippauf2019 = 펠릿 밀도 본문 1.8 ↔ 범례 1.7 (L258) · Fig 7 · S6 캡션 NCM83 (L259) · SI 표 번호 · 음극 계면 10–33 ↔ 10.23–30.33 Ω (L260) · DSC 부호 (L261) · 흑연 음극 60:35:5 순서 (L262) · 반복 셀 차 (L263) · 이웃 카드 `matthews2024_ptfe_nanofibril_network` 서술 정정 후보 (L267); jadidi2023 = PSMI ↔ PMSI · Halidan 2014 ribbon ↔ bladed (L514) · SMI 라벨 "Subdomain-based" ↔ 원제 "non-sampling" (L232) · 원저 결론 충돌 3 쌍 미조정 (L513) · 혼합지수 기호 미정의 (L196).
