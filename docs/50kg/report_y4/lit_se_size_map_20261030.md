# SE 미립화 (복합양극) 문헌 지도 — 문헌이 무엇을 보이고, 우리 DEM · 망 파이프라인이 무엇을 재현하나 (10-30)

- 작성: 문헌 에이전트 (읽기 전용 · 10-30) → 메인 세션이 저장.  1저자 10-30 *"문헌들도 참고해서 이런 미립화에서 주로 어떤걸 보여주는지도 확인해봐 · 그걸 시뮬레이션으로 구현이 가능한거니까"* · *"중요한 누락된 논문들만 추려서 얘기해주면 먹여줄게"*.
- 함수 이름 = `scripts/dem_analysis_core.py` 안 (`calc_porosity` · `calc_porosity_union_exact` · `calc_interface_area` · `calc_coverage` · `calc_percolation` · `calc_ionic_active_am` · `calc_overlap_ratio` · `calc_tortuosity_all` · `calc_love_weber_stress`) · 망 수송 = `scripts/network_conductivity.py` · `scripts/tau_flux.py`.
- 대상 보고 = 50kg 4차년도 DEM (SE D50 0.7 · 1 · 2 · 3 µm 단분산 대리 · NCM D6 단일 · 85 wt% · 300 MPa · 가압 · 판 고정 이완 · 입도별 시드 1 · `docs/50kg/report_y4/storyline_draft1.md` p1–p7).
- 원천 = 정본 litdb **로컬 ref** `origin/claude/friendly-meitner-lldvar` (에이전트 = c13b28931 · 10-27 스냅샷 · 메인 10-30 재확인 = 8734b9e5b · 454 장 — §6 여덟 편 카드 여전히 없음 · 새 9 장은 입도 논문 아님) · `litdb/papers/` 445 장 → 후보 ≈ 60 → SE 입도가 변수인 16 장 열람 (복합양극 12 · 순수 SE 3 · 내재 σ 1) + 맥락 9 장.
- 표기: 수치 = 카드 값만 (카드 § 병기) · 판독 = 카드가 그림에서 읽은 값 · [우리 산술] = 카드 값으로 한 계산 · [미확인].
- "재현 가능" = 우리 모형 틀 (강체 구 DEM · SE 유효 E 1.35 GPa · 단분산 · 가압 상태 · 시드 1) 에서 같은 양을 계산할 수 있다는 뜻 — 실험값과 맞는다는 뜻 아님.  코드 이름은 리포 grep 으로 존재만 확인 (실행 안 함).

## 0. 요지
1. 공통 서사 = 분말 (PSD · SEM · 순수 SE σ) → 단면 (분포 · 기공) → CAM–SE 계면 · 피복 → 유효 이온 σ · tortuosity factor (± 전자 σ) → 용량 · 율특성.  12 편 중 10 편이 용량 · 율로 끝남 (우리가 못 하는 칸).
2. 방향: 작은 SE → 복합체 기공 ↓ (4 + 공정 · 응집 2) · 계면 · 피복 ↑ (4) · σ_ion,eff ↑ (5) · σ_el,eff 평탄 1 / ↓ 3.  밀링으로 만든 작은 SE 의 펠릿 σ ↓ (5, 평탄 1) → "구조 이득 vs 재료 손해 = 최적 · 균형" 서사 (Cronau 2 h · Frankenberg 밀링 에너지).
3. 재현 가능 = 구조 · 연결성 · 망 수송.  불가 = 전기화학 · 순수 SE σ(d) · PSD 폭 · 응집 · 언로딩.
4. 실험 다수는 SE ≳ CAM 영역 (Schlautmann CAM 3.4 vs SE 4–40 µm · Zhou NCM 1–5 vs SE 20 / 1 µm).  우리는 λ = D_AM/D_SE 2–8.57 · 85 wt% — Shi 모델에서 고-로딩 = λ 가 가장 결정적인 쪽 (shi2019 §A.2 · 잠정).
5. 빠진 것 = 실측 PSD · SEM (p1) · PSD 폭 · 응집 한정어 (p1 · p3 · p7) · 겹침 문턱 민감도 (p3 · 기존 도구) · 문헌 방향 열 (p7) · 순수 SE ↔ 복합체 반대 방향 해설 (p2).

## 1. 카드 표 (복합양극 12 · 순수 SE 3 · 내재 σ 1)

| 카드 | SE 입도 / 크기비 | CAM | 보인 것 (카드 수치) | 우리 재현 | 재현 불가 |
|---|---|---|---|---|---|
| `schlautmann2023_se_particle_size_composite_transport` | LPSCl D50vol 4 · 11 · 20 · 40 µm (SE ≥ CAM) | NCM811 D50 3.4 µm · 70:30 wt% · 탄소 · 바인더 없음 | 부피 · 개수 PSD · 순수 SE σ 2.2 mS/cm (L 2.8) · XRD/PDF/Raman 불변 · SEM-EDS · 기공 14.1 · 18.1 · 21.4 · 24.3 % · σ_ion,eff 0.254 · 0.199 · 0.153 · 0.165 · σ_el,eff 0.301 · 0.257 · 0.311 · 0.406 mS/cm (Table S4) · κ_ion,sim 4.70 · 6.65 · 8.56 · 7.50 · GeoDict 전류 지도 (XL = 점접촉 병목) · 계면 면적 S/XL ≈ 8.7 배 (판독) · C/20 방전 198 · 165 · 165 · 152 mAh/g · "균형 수송" (§3a–f · §5) | 기공 (`calc_porosity` · `calc_porosity_union_exact`) · 계면 면적 (`calc_interface_area`) · f · tau2 (`scripts/network_conductivity.py` · `scripts/tau_flux.py`) · 전류 지도 · 전자 f (AM–AM) | 용량 · 율 · 순수 SE 구조 · TLM 계면항 · 넓은 PSD · 미세분 |
| `minnmann2024_microstructure_porosity_visualization` | Li₃PS₄–0.5LiI (LPSCl 아님) d50 7.41 · 4.93 · 5.93 µm | NCM83 단결정 3–5 µm · 무탄소 | PFIB-SEM 3D 상분율 · 기공 (분할 ≈10 · 7.5 · 6 % · 기하 ≈20 · 16 · 11 %, 판독) · S_CAM-ISE 0.11 → 0.24 m²/g · 피복 ≈20 → ≈50 % · chord length · κ_ion exp ≈15 → ≈6 · 전류 지도 · σ_ion,eff ≈0.05 → 0.11 · σ_el,eff ≈15 → 10 mS/cm (판독) · 순수 SE 2.0 · 1.7 · 1.6 mS/cm · CAM 이용률 62 → 77 % · 0.1C 방전 92 · 156 · 152 mAh/g (§3 · §5) | 기공 두 규약 병기 형식 · 피복 (`calc_coverage`) · τ_geo · tau2 · 전류 지도 | chord length · OCV 이용률 · 용량 · 나노기공 |
| `shi2019_high_am_loading_particle_size_assb` | LPS 유리 1.5 · 3 · 5 · 8 µm · 모델 λ 0.33–8 | NMC532 5 · 12 µm · CNF 5 wt% (모델엔 없음) | LIGGGHTS DEM (Hertz · E_SE 18.5 GPa · 200 MPa) + 최단 경로 → θ_CAM 열지도 (λ × f_CAM) · λ_min (75 wt% θ 98 % → 2.1) · 70 wt% λ 1.67 → θ ≈ 1 · 85 wt% λ 1 → 8 에 θ ≈16 → ≈20 % · 모델 용량 155 × θ ↔ 실험 · 밀링 SE σ 0.32 · 0.24 · 0.22 · 0.14 mS/cm (SI Table S3) (§3 · §5 · §S.4) | 퍼콜레이션 (`calc_percolation`) · SE 관통망에 닿는 AM (`calc_ionic_active_am` → `ionic_active_pct` · `am_ionic_isolated_pct`) · λ 축 | 용량 환산 · 밀링 σ · ⚠ "활성 AM" 낱말 금지 (`KG50B-01`) |
| `bazzoun2025_dem_parameter_sensitivity_assb_cathode` | LPSCl SE45 4.5 · SE19 1.9 µm · λ 1.3 · ≈3 | NMC532 5.8 µm | DEM 민감도 (μ_CAM-SE 최강) · 기공 모의 ≈0.22–0.25 vs ≈0.16–0.18 (판독) · 실측 SE19 가 23.6 · 20.5 · 12.7 · 13.8 % 낮음 (f_CAM 60–85, 200 MPa) · θ_CAM · θ_SE · 85 wt% 방전 SE45 50.5 / 52.5 vs SE19 122.5 / 130 mAh/g (200 / 400 MPa) · 순수 SE 2.9 vs 1.0 mS/cm (§3) | 기공 · 연결 AM · SE 퍼콜레이션 · 마찰 민감도 (새 런) | 용량 · 순수 SE σ |
| `tailored_cathode_microstructure_low_pressure_assb` (Zhou 2025) | LPSCl coarse ~20 · fine ~1 µm | NCM811 ~1–5 µm | DEM 최소 겹침 0 · 2 · 5 · 10 % 별 CAM 접촉 비율 coarse 94 · 83 · 56 · 20 / fine 100 · 100 · 94 · 28 % (Table 1) · FIB-SEM 기공 11.3 vs 4.4 % · τ 1.84 vs 1.21 · BET 6.02 vs 9.24 m²/g · R_ct 17.3 → 9.9 Ω · 100 사이클 유지 (§3 · §5) | 겹침 분포 (`calc_overlap_ratio`) → 문턱별 접촉 AM · τ_geo · 기공 | R_ct · 사이클 · 스택압 · 균열 |
| `minnmann2021_jes_charge_transport_bottlenecks` | LPSCl D50 3.45 → 2.45 · D90 20.05 → 8.57 µm | NCM622 61 vol% | σ_ion,eff 3.06×10⁻⁶ → 1.17×10⁻⁵ S/cm · τ_ion² 130 → 33.8 · σ_el,eff 1.43×10⁻³ → 6.97×10⁻⁴ S/cm · 순수 SE 1.6 → 1.2 mS/cm (§9.2) | 이온 · 전자 f · tau2 | 순수 SE σ · 율 |
| `bazzoun2026_dem_fem_rnm_ionic` | LPSCl D50 1.49 µm (+ Fig 7 모의 1–8 µm) | NMC811 D50 5.50 µm | DEM → FEM · RNM (Holm + Kirchhoff) · σ_eff,ion 0.137 · 0.101 · 0.065 mS/cm (70 · 75 · 80 wt%, 400 MPa) · Fig 7 작은 SE → σ ↑ (§3 · §5) | f(d) 사슬 (`scripts/network_conductivity.py`) | 실측 EIS |
| `cronau2022_wet_milling_particle_size_ionic_conductivity` | 밀링 시간 축 (1–2 h ≈1.0 µm) | NCM-85 3.5 µm | σ 2.5 → 1.73 (2 h) → 0.36 mS/cm (50 h) · 0.6C 첫 방전 → "2 h 최적" · σ 하락 = 밀링 손상과 교란 (§0 · §3) | 같은 d 의 구조 쪽 f(d) | σ(밀링) · 용량 — p5 손익분기선의 문헌 원형 |
| `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` | LPSCl x50 17 µm → 밀링 | NCM83 단결정 · 70:30 wt% | 기공 0.376 → 0.265 · σ_ion 0.072 → 최대 0.155 → 0.124 · σ_e 0.73 → 0.23 mS/cm · 방전 110 → ≈164 → ≈90 mAh/g (§0 ④) | 주어진 구조의 기공 · f | 공정 · 결정자 · 용량 |
| `otani2025_dem_se_dispersion_aggregation_compression` | LPSCl 0.7 µm · 응집수 N 1 → 307 | NCM111 5 µm | EDEM (Hertz–Mindlin + JKR) · 상대밀도–압력 (300 MPa N=1 78.6 vs N=307 70.1 %, 판독) · 접촉 면적 감소 · 힘사슬 (§1 · §3) | 상대밀도–판 압력 · 접촉 면적 · 힘사슬 (`scripts/analyze_contacts.py`) | 응집 = 우리 침대에 없음 |
| `park2020_dimension_controlled_se_percolation_contact_area` | LLZO-Ta 0D 250 · 500 · 1000 nm | 흑연 음극 | 관통 경로 · SCA · σ_eff · "≤ ~500 nm 필요" | 관통 · 접촉 면적 · f | 산화물 · 음극 ("접촉 면적 ≠ 전도" 예로만) |
| `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` | 게스트 1 µm + 자유 SE 3 µm | NCM811 13.5 µm | 기계 혼합 코팅 · DEM CUE (A* 경로) · 접촉 면적 | 경로 연결 AM · 접촉 면적 | 코팅 · 용량 |
| `faka2026_particle_size_consolidation_strain_lpscl` (순수 SE) | LPSCl D50 4 · 11 · 20 · 40 µm | — | in-die 300 MPa 기공 26.3 · 22.5 · 16.0 · 12.9 % (판독) · Heckel · XRD 변형 · DEM 입자 응력 (실측 PSD vs 단분산) → "변형 = 크기 불균일 때문" (§0 · §3) | 입자 응력 분포 (`calc_love_weber_stress`) | 순수 SE · 격자 변형 — 작을수록 덜 치밀 = 복합체와 반대 |
| `lee2025_heckel_argyrodite_powder_densification_nanoindentation` (순수 SE) | 상용 ↔ 볼밀 | — | Heckel K · 300 MPa 기공 16.1 vs 14.8 % (판독) | Heckel 해석 (`scripts/heckel_analysis.py`) | 입경 미보고 |
| `schneider2023_particle_size_pressure_transport` (순수 SE) | t-Li₇SiPS₈ < 50 · > 50 µm | — | σ–성형압 · 작은 쪽 치밀하나 σ ↓ · "기공은 약한, PSD 는 강한 descriptor" | 정규화 f–압력 | 다른 재료 |
| `ou2026_microstructural_multiscale_fast_ion_transport` (내재 σ) | 결정립 nm–µm | — | 입계가 거시 D 를 깎는 몫 1 µm 0.7 % · 100 nm 5.8 % (카드 재계산) | — | p5 근거: 밀링 SE σ ↓ 를 "입계" 로 돌리지 말 것 |

맥락 카드 (SE 입도 변수 아님): froboese2019 · bielefeld2019 · bielefeld2020 · dem_mechanical_stresses_ssb_electrode_cycling · minnmann2022 · otani2023 · kim2026_operando_neutron · kang2026_intertwined · bouvard2000.

## 2. 문헌이 주로 보이는 것 (복합 12 편 · 근사 빈도)

| # | 그림 · 지표 | n/12 | 우리 |
|---|---|---|---|
| T1 | SE 분말 PSD · SEM | 10 | ✗ (단분산 입력) |
| T2 | 순수 SE σ vs 입도 | 7 | ✗ (σ₀ 입력) |
| T3 | 복합체 기공 · 밀도 | 7 | ✓ |
| T4 | 단면 · 3D 영상 | 5 | △ |
| T5 | 계면 면적 · 피복 · 접촉 | 6 | ✓ |
| T6 | 유효 이온 σ / f | 6 | ✓ |
| T7 | tortuosity factor · τ_geo | 5 | ✓ |
| T8 | 유효 전자 σ | 4 | △ (AM–AM, 탄소 없음) |
| T9 | 연결성 이용률 · 고립 AM | 6 | ✓ 연결성만 (`KG50B-01` 낱말) |
| T10 | 용량 · 율 (± R_ct · 사이클) | 10 | ✗ |
| T11 | λ = D_CAM/D_SE 축 | 4 | ✓ |
| T12 | 압력 × 입도 | 3 | △ 가압 가지 |
| T13 | 전류 밀도 지도 | 2 | ✓ |
| T14 | 공정 손상 (XRD · 결정자) | 5 | ✗ |
| T15 | 응력 · 힘사슬 · 균열 | 3 | ✓ (가압 상태) |

- 단서 · 반례: 응집하면 이득이 준다 (otani2025) · 순수 SE 는 작을수록 덜 치밀할 수 있다 (faka2026) · 순수 SE σ ↓ 는 밀링 공정과 교란 (cronau2022 · shi2019 · frankenberg2025) · 입계 몫은 µm 결정립에서 작다 (ou2026) · 전자 σ 는 작은 SE 에서 줄 수 있다 (minnmann2021 · minnmann2024 · frankenberg2025).

## 3. p1–p7 대응
- p1: 문헌 표준 = T1 + T11.  빠진 것 = 네 분말 실측 PSD (부피 · 개수) · SEM · "PSD 폭이 결과를 바꾼다" 한정어.  문헌 효과의 큰 몫은 λ < 1 → > 1 전이 (shi2019 Fig 3b).
- p2: 문헌 표준 = T3 + 밀도–압력 곡선.  빠진 것 = 두 규약 병기 · 순수 SE ↔ 복합체 반대 방향 해설 · (선택) 기공 크기 분포 (`scripts/extract_pore_mesh.py`).  껍질 점유 = 문헌에 같은 그림 없음 (`KG50B-05`).
- p3: 문헌 표준 = T5.  빠진 것 = Zhou 형 겹침 문턱 민감도 (기존 접촉 목록 + `calc_overlap_ratio` · 새 시뮬 없음) · 응집 한정어 (D0.7 실분말 응집 가능 → D0.7 값이 이득 쪽일 수 있음 [추정]) · "접촉 면적 ≠ 전도" (park2020).
- p4: 문헌 표준 = T6 · T7 · T13 · T9.  협착 몫은 입도 문헌에 없는 그림 = 우리 강점 (모형 내부 양).  T9 를 "SE 관통망과 경로 없는 AM 수 · 위치 (연결성 기준)" 로 낼지 = 1저자 결정.  전자 채널 = AM–AM 만 · 탄소 유무 [미확인].
- p5: 문헌 표준 = T2 + 최적 그림 (cronau2022) — 손익분기선 = 그 정량판.  [우리 산술] 밀링 SE σ 비 = MIN24 1.25 · MIN21 1.33 · CRO 1.45 · SHI 2.3 · BAZ25 2.9 → 덱의 5.1/2.3 = 2.217 은 범위 위쪽.  각주 = σ(d) 는 공정과 교란 · Schlautmann 4–40 µm 평탄 · 입계 증가로 σ 감소를 DEM 결론처럼 쓰지 않음 (ou2026).
- p6: 12 편 중 두께 방향 분포 낸 논문 없음 · 가장 가까운 것 = 입자 응력 vs 크기 · 위치 (Alabdali 2024 · faka2026 · otani2025) → `calc_love_weber_stress` 로 같은 종류 · z 구간 전위 · 소산 = 새 도구 · 모형 내부 추가분 표기.
- p7: 문헌 마무리 = T10 + "최적" (우리는 `KG50B-02` 로 막음).  권고 = "문헌 방향 (카드)" 열 추가 (기공 ↓ · 계면 ↑ · f ↑ / κ ↓ · 전자 f 평탄 / ↓ · 순수 SE 밀도 ↓ · 반례 = 응집).

## 4. 웹 후보 (전부 [미확인 — litdb 카드 없음] · 수치 안 옮김)
- Ohsaki 등 (오사카공립대) — LPSCl 입도 분포 · DEM · 입계 저항 최단 경로 tortuosity (보도: https://www.omu.ac.jp/en/info/research-news/entry-110534.html)
- Lin 등 — 서브 µm Li₆PS₅Cl 고-로딩 양극 (https://pubs.rsc.org/en/content/articlelanding/2025/cp/d4cp03893b)
- Lei 등 — Review of Particle Size Effects of Solid Electrolytes in ASSB (https://journal.hep.com.cn/eleer/EN/10.1007/s41918-026-00288-x)
- "Impact of Sulfide-based SE PSD on the Electrochemistry of ASSB via Impedance Study" (https://hal-u-picardie.archives-ouvertes.fr/hal-03696977v1)
- "Interface Engineering in Sulfide-Based ASSB: Insights from Resistance Analysis" (https://gdch.app/article/interface-engineering-in-sulfidebased-allsolidstate-batteries-insights-from-resistance-analysis-batt)
- Tron 등 — "Rational Optimization of Cathode Composites for Sulfide-Based ASSB" (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9866434/) — ⚠ litdb `tron2023_lpscl_ccd_ambient_pressure` 는 **다른 논문** (CCD)
- Rajagopal 등 — different sized solid electrolytes (Li₇P₂S₈I) (https://pubs.rsc.org/en/Content/ArticleLanding/2021/RA/D1RA05897E)
- Rosero-Navarro 등 — argyrodite precursor solution + dispersant (https://eprints.lib.hokudai.ac.jp/dspace/handle/2115/79133)
- 정본 카드 참고문헌에만 있는 것 (서지 = 카드 표기): Calpa 등 Electrochim. Acta 296 (2019) (park2020 참고문헌) · S. Choi 등 ACS AMI 2018 (shi2019 [29]) · Strauss 등 ACS Energy Lett. 2018 (cronau2022 [21]) · Ohsaki 등 Powder Technol. 387 (2021) (kawaguchi2023 ref 29) · Stavola 등 ACS Energy Lett. 8 (2023) (kim2026_operando ref 19)

## 5. 한계
- 445 장 중 이름 + 낱말 grep 으로 골랐다 (다른 낱말 카드 놓쳤을 수 있음) · 전문 정독 4 장 (Schlautmann · Minnmann 2024 · Bazzoun 2026 · Schneider 2023) · 나머지 12 장 요약 · 수치 · 그림 절 위주 · ≈ 40 장 grep 줄만.
- §2 빈도 = 근사 · 일부 카드의 정정 전 "우리 대비" 서술은 옮기지 않음 · otani2025 카드의 "Otani 2023 카드 없음" 은 낡음.
- 정본 확인 = 에이전트 10-27 스냅샷 → 메인 10-30 fetch (8734b9e5b) 로 §6 다시 확인 (카드 없음 그대로).

## 6. 넣어 주면 좋은 논문 (우선순위 · 정본 litdb 카드 없음 — 10-30 8734b9e5b 확인 · `tron2023_lpscl_ccd_ambient_pressure` 는 다른 논문)

| 순위 | 논문 | 우리 카드에 없는 것 | 쪽 |
|---|---|---|---|
| 1 | Ohsaki 등 — LPSCl PSD · DEM · 입계 저항 최단 경로 tortuosity [미확인] | 같은 SE · 같은 방법 계열로 PSD 폭 효과 — 단분산 대리의 직접 검증 · 반론 | p1 · p4 · p7 |
| 2 | Lin 등 — 서브 µm Li₆PS₅Cl 고-로딩 양극 [미확인] | 서브 µm LPSCl 복합양극 비교 — 우리 D0.7 자리 | p2 · p4 |
| 3 | Lei 등 — SE 입도 효과 리뷰 [미확인] | 표준 그림 점검 · 응집 · 부반응 절충 | p1 · p5 · p7 |
| 4 | "Impact of Sulfide-based SE PSD … via Impedance Study" [미확인] | LPSCl 에서 큰 PSD 가 이긴 반례 | p5 · p7 |
| 5 | "Interface Engineering … Resistance Analysis" [미확인] | 최적 입도의 SOC 의존 · 저항 분해 | p7 · p5 |
| 6 | Stavola 등, ACS Energy Lett. 2023 — thick NMC111–argyrodite 리튬화 기울기 · tortuosity factor | 아지로다이트 후막 두께 방향 실측 | p6 · p4 |
| 7 | Calpa 등, Electrochim. Acta 2019 — small-sized Li₇P₃S₁₁ (liquid phase) | 밀링 손상 없는 미립화 — p5 교란 분리 단서 | p5 · p2 |
| 8 | Tron 등 — Rational Optimization of Cathode Composites [미확인] | 입도만 다른 두 LPSCl 을 설계 변수와 함께 비교 | p5 · p7 |

## 7. 10-30 갱신 — 1저자가 PDF 를 준 8 편 (정본 litdb 카드 반입 · "SE 입도 효과" 절)

| 카드 | 바로잡은 것 · 더한 것 |
|---|---|
| `yano2026_se_psd_width_ionic_tortuosity_dem` | §6 의 "Ohsaki 등" = 1저자 Takeru Yano (교신 Ohsaki) · J. Energy Storage 153 (2026) 120973 · DEM 기하 tortuosity 평탄 (1.14–1.17) · 경로당 입자 수 +28 % · 밀링 펠릿 σ ÷2.78 (p5 목록) |
| `lin2025_submicron_lpscl_cathode_li_kinetics` | "sub-µm" = SEM 모양 · 레이저 D50 **2.34 µm** (우리 D2–D3 사이 — §6 의 "D0.7 자리" 는 틀림) · 밀링 펠릿 σ ÷3.28 (p5 목록 → 덱 2.217 = 범위 중간) |
| `calpa2019_small_li7p3s11_liquid_phase_composite_cathode` | Li₇P₃S₁₁ (LPSCl 아님) · 밀링 없는 미립화도 펠릿 σ 1.0 vs 1.9 mS/cm = 합성 경로 교란 (p5 교란이 없어지지 않음) |
| `tron2023_rational_cathode_composite_optimization_lpscl` | 크기 정성 · AM:SE 85:15 wt% 에서 용량 −36 % (300 MPa) |
| `yadav2021_lpscl_sieved_psd_impedance_tortuosity` | IWIS 2021 · 큰 SE 가 이긴 반례 (≥ 20 µm) · 펠릿 σ(d) × 우리 f(d) = 이중계상 위험 (p5 주의) |
| `lei2026_se_particle_size_effects_review` | 절충 점검표 · 수치는 2 차 인용 (원문으로 인용) |
| `kawaguchi2026_se_size_soc_dependent_cathode_resistance` | 최적 입도가 SOC 에 따라 바뀜 → p7 *"최적"* 금지 근거 · 큰 SE 이온 σ 2.33× |
| `stavola2023_thick_nmc111_lpscl_lithiation_gradient_tortuosity` | 두께 방향 기울기 (p6) · 논문 tortuosity factor 를 표 S8 로 다시 셈 = NMC 부피분율로 계산된 것으로 보임 → 9.19 / 8.43 평탄 (카드 §) |

- 다음 후보 = Jeong 2024 (Adv. Energy Mater. 14, 2304544 · SE <1 vs 3–5 µm · 두께 방향 SOC) — 카드 없음 [미확인].
