# 믹서 · 코팅 공정 — 1저자 읽기 후보 목록 (2026-10-13)

> **요청** (1저자 2026-10-13, 원문): *"그리고 이거 믹서, 코팅 공정 관련해서 내가 읽으면 좋은 논문들도 후보군으로 추가로 부탁할게 / litdb에도 있겠지만"* · 같은 날 추가: 1저자가 이미 가진 PDF 10 편 ("DEM mixer" 폴더) 중 무엇을 읽을지 → **Part A′**.
> **지위 — 후보 목록 — 인용 전 litdb 정본 카드로 만든다.**  이 문서의 서지 · 요약을 원고 · 보고 · 덱 · 웹앱에 그대로 옮기지 않는다 (CLAUDE.md 규율 ⑥ *"원문을 보지 않은 서지는 채우지 않는다"*).
> **기준 논지** — `docs/hetero_thesis.md` (비준 블록의 예측 P1–P3 · §2 원리 · §3 어긋남 · §4 열린 결정 D2–D4 · §6 검색 낱말).  이 목록은 논지 §6 *"배경 문헌 reference 화"* 의 **입력**이다 — 카드화는 §6 대로 10/21 이종기술 자료 뒤 · 원문 PDF 확인 뒤.
> **조사 범위** — 정본 litdb = `origin/claude/friendly-meitner-lldvar` 커밋 `6963e7f13` (2026-10-13 fetch) 의 `litdb/papers/` 목록 386 개 (양식 파일 포함) 를 직접 훑었다 (INDEX 파일에 기대지 않음).  새 후보는 웹 검색 (아래 §0 한계).  litdb 브랜치 · 카드는 **건드리지 않았다**.

---

## 0. 읽는 법 — 출처 표지 · 이번 조사의 한계

| 표지 | 뜻 |
|---|---|
| (카드) | 정본 litdb 카드에 적힌 값 · 서술 그대로 (그 카드가 원문 PDF 로 확인한 것) |
| (목록 제목) | 웹 검색 결과 목록에 뜬 **출판사 · 색인 페이지 제목** 을 그대로 옮김 |
| (요약) | 웹 검색 도구의 **요약문** 에 나온 값 — 출판사 페이지를 **직접 열지 못했다** |
| (URL 에 표시) | DOI 가 결과 URL 경로에 그대로 들어 있음 |
| [미확인] | 어느 쪽에서도 확인 못 함 — 채우지 않았다 |

⚠ **한계 (숨기지 않는다)**
- 이 세션에서 페이지 열기 도구는 모든 호스트에서 이름 풀이에 실패했고, 서지 색인 API (Crossref · OpenAlex · Semantic Scholar · doi.org · Europe PMC · PubMed) 는 조직 egress 정책으로 403 이었다 — **우회하지 않았다**.
- ⇒ Part B 의 서지는 **검색 결과 목록 (제목 · URL) + 검색 도구 요약문** 뿐이다.  초록도 원문으로 읽지 못했다.  '왜' 칸은 요약이 전한 초록 내용 기준의 **정성 서술**이고, 요약의 수치는 옮기지 않았다.
- ⇒ Part B 모든 행 = **"검색 결과 서지 · 원문 미확인"**.  DOI 는 요약 · URL 에 나온 것만 적었고 추측해 만들지 않았다.  카드로 만들 때 출판사 페이지 · PDF 로 한 칸씩 다시 맞춘다.
- 검색 요약끼리 어긋난 곳은 그대로 적었다 (예: B2-4 의 저자 · 소속).

**우선순위** — ★★★ = 논지 (P1–P3 · D2–D4) 에 바로 닿음 · 먼저 읽기 / ★★ = 방법 · 정의 · 비교 대상 / ★ = 맥락 · 나중.
**주제 번호** — 1 건식 혼합 · 건식 코팅 · 건식 막 / 2 활물질 (CAM) 에 SE 코팅 / 3 응집성 분말의 혼합 균질도 / 4 표면 에너지 · 접착 / 5 유동성 앵커 · DEM 점착 보정 / 6 혼합 상태 → 압축 뒤 미세구조 · σ_ion (대칭셀 TLM 포함).

**우리 쪽 기준 (판독용 두 줄)**
- 믹서 = CGF 151.4 의 3 상 저-Fr **회전 드럼** · 점착 = 상 쌍별 CED (SJKR · LIGGGHTS) — `docs/reviews/mixer_layered_prereg_20260921.md` · 논지 §2-6.
- 혼합 지표 = 칸 (주판정 16×16×4) 기반 Lacey M — ① 칸 한 변이 AM_P 지름 수준이라 해상도가 거칠고 ② 분모를 그 런 자신의 t₀ 분산으로 잡아 M 이 음수가 된 개발 런이 있다 (②에 대한 처방 = 논지 §5 *"이론 분모 Lacey"*).

---

## Part A′ — 1저자 보유 PDF 10 편 ("DEM mixer" 폴더)

> **대응 확인** — 10 편 모두 정본 카드가 있다.  카드를 하나씩 열어 **PDF 필드의 파일명 번호 (01–09) 와 제목**으로 맞췄다 (10 은 카드의 PDF 파일명이 달라 제목 · 내용으로 맞춤).
> ⚠ **01 은 `frankenberg2024_dem_high_intensity_mixer_assb` 가 아니다** — `otani2025_dem_se_dispersion_aggregation_compression` 카드의 PDF 필드가 01 파일명 (*Quantitative Study of Solid Electrolyte Particle Dispersion and Compression Processes …*) 과 같다.  Frankenberg 2024 는 별도 카드 (Part A).

| # | 정본 카드 | 우선 | 왜 / 우리 믹서 파이프라인과의 관계 (카드 기준) | 카드 서지 |
|---|---|---|---|---|
| 01 | `otani2025_dem_se_dispersion_aggregation_compression` | ★★★ | 응집수 (응집체 하나의 SE 입자 수) 를 정해 넣고 압축 — 응집이 클수록 같은 압력에서 밀도 ↓ · AM–AM 힘사슬 · AM\|SE 접촉 ↓ (카드).  **P3 (혼합 상태 → 압축 뒤 SE 경로) 에 가장 가까운 DEM 선례.**  한계: 응집을 *입력* 으로 만든다 (혼합 DEM 아님) · 모든 쌍에 γ 하나 (상 쌍 행렬 아님, 카드 §4.1) → P1 · P2 는 시험 대상이 아니다 · 전달 σ 없음 → 우리 망 단계가 이을 자리.  짝 = Otani 2023 (B6-1) | Otani 외 (Inoue 지도) · *Electrochemistry* 93(6), 063009 (2025) · `10.5796/electrochemistry.25-71025` |
| 02 | `hare2026_dem_pept_dry_mixing_nmc622_eirich` | ★★ | Eirich 집약 믹서 안 NMC622 유동을 PEPT 로 실측해 CG DEM (Hertz–Mindlin + JKR) 속도장과 대조 — 날개 끝 속도를 올려도 Lacey 혼합 속도는 수확체감 (카드).  **'혼합 DEM 을 실험으로 검증하는 틀'** 로 읽는다.  한계: SE 없음 · 날개 믹서 ≠ 우리 저-Fr 회전 드럼 → 값 · 조건 전이 불가 | Hare 외 · *Powder Technology* 469 (2026) 121804 · `10.1016/j.powtec.2025.121804` |
| 03 | `lischka2025_dem_eirich_intensive_mixer_dry_mixing` | ★★ | CG 하에서 JKR γ 를 cohesion number 불변으로 다시 정함 (카드의 유도: γ ∝ R\*^(8/5)) · 벽 γ 따로 · 툴 충돌이 분쇄 지배 · RSD 는 짧은 시간에 포화 (카드).  **D2 (CGF 151.4 에서 쌍별 CED 를 정하는 규칙)** 와 **칸 · 표본 크기 의존** (우리 Lacey M 칸 문제의 실물 사례) 두 곳에 닿는다.  한계: 입자종 하나 (상 쌍별 γ 없음) · SE 없음 · γ ↔ 점착 강성 환산식 없음 (카드) | Lischka, Nirschl · *Particuology* 104 (2025) 52–67 · `10.1016/j.partic.2025.06.002` |
| 04 | `asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing` | ★ | 카본블랙 분쇄를 PBE 로 풀고 DEM 은 응력 · 빈도만 준다 (CB 는 DEM 밖) (카드).  도전재 분산 축이라 이 논지 (SE–SE 응집) 와는 멀다 — 첨가제 (SBE · DBE) 쪽에서 나중에 | Asylbekov 외 · *Energy Technology* 11 (2023) 2200867 · `10.1002/ente.202200867` |
| 05 | `nadeem2023_gnn_mixing_index` | ★★★ | 칸 없이 **이웃 구성** 으로 혼합도를 재고 **무작위 기대값으로 나누는** 지수 (GNN) — 불균등 조성 · 3 종 이상으로 일반화 (카드).  우리 Lacey M 의 **칸 해상도 · 시작 상태 분모** 문제의 대안 사양서.  카드 실측: 스칼라 그대로는 우리 압밀 침대에서 크게 과소 → **입자별 커널 + 무작위 정규화만 살린다** (카드 §8) — P1 측정에 직접 | Nadeem 외 · *Advanced Powder Technology* 34 (2023) 103933 · `10.1016/j.apt.2022.103933` |
| 06 | `chibwe2020_nnsi_segregation_index` | ★★ | 근접이웃 **거리** 로 분리를 재는 NNSI (LIGGGHTS 로 검증) — 접촉 기반 지표가 못 보는 '닿진 않았는데 뭉친' 상태를 본다 (카드).  쓸 자리 = **혼합 직후 · 압축 전 프레임** (P1).  한계: 연화 DEM 의 큰 겹침 · 300 MPa 압밀 프레임에서는 음수 · 동적범위 붕괴 (카드) | Chibwe 외 · *Powder Technology* 360 (2020) 481–492 · `10.1016/j.powtec.2019.10.079` |
| 07 | `jadidi2023_dem_batch_solid_mixers_review` | ★★ | 배치 믹서 DEM 리뷰 — 혼합지수 8 종의 식 · 점착 모델 · 보정 · CG 정리, 점착을 다룬 연구가 소수라는 진단 (카드).  **지도용**: 지표의 장단 평가는 이 리뷰가 스스로 하지 않고 다른 문헌에 넘긴다 (카드) → 05 · 06 과 같이 읽는다 | Jadidi 외 · *Rev. Chem. Eng.* 39(5) 729–764 (2023) · `10.1515/revce-2021-0049` |
| 08 | `lippke2023_dem_drying_structure_formation_lib` | ★ | 습식 슬러리 **건조** 중 구조 형성 DEM (유체 대리 힘 · 1D 건조기 커플링) (카드).  건식 공정 논지와 거리 — 같은 iPAT 사슬의 맥락만 | Lippke 외 · *Energy Technology* 11 (2023) 2200724 · `10.1002/ente.202200724` |
| 09 | `sun2026_dem_extrusion_recirculation_dry_electrode` | ★ | 트윈스크류 **건식 압출 + 재순환** DEM (LIGGGHTS) — 섬유 (CNF) 를 구의 유효물성으로 뭉개자 σ_e 순위가 실험과 뒤집혔다는 **관측된 실패** (카드).  첨가제 표현의 주의로는 값지지만 코팅 · 혼합 논지와는 멀다 | Sun, Vigneaux, Franco · *Batteries & Supercaps* 9 (2026) e202500211 · `10.1002/batt.202500211` |
| 10 | `varkey2026_multicontact_elastoplastic_dem` | ★ | 이미 정리됨 (CLAUDE.md 'LIT: Varkey 2026' 절) — 다중접촉 탄소성 **압밀** 접촉법칙 · 할라이드 SE · 혼합 아님 → 이 논지로 다시 읽을 필요는 낮다 (압밀 접촉법칙을 비교할 때 다시) | Varkey 외 · *Adv. Powder Technol.* 37 (2026) 105338 · `10.1016/j.apt.2026.105338` |

**한 줄 결론** — 먼저 **01 · 05**, 다음 **02 · 03 · 06 · 07**, **04 · 08 · 09 · 10** 은 나중.

---

## Part A — 이미 정본 litdb 에 있는 카드 (A′ 10 편 밖)

| slug | 주제 | 우선 | 왜 읽을 만한가 (카드 기준) | 카드에서 확인한 서지 |
|---|---|---|---|---|
| `lee2026_mechanical_halogen_argyrodite_drycoating` | 2 · 4 | ★★★ | 황화물 SE 를 NCM 에 건식 코팅할 때 품질을 정하는 것은 이온전도도가 아니라 SE 기계 물성 · **NCM 표면과의 접착일 W_ad** (AFM-FS 측정 + MLIP/DFT 계산) (카드).  **D4 (계면 분리일 계산) · 논지 §2-8 (측정)** 의 같은 랩 선례.  카드 저자 목록에 *Yonghoon An* — 1저자 본인이면 원자료 접근이 쉽다 (확인 필요).  ⚠ 카드 한정어: 계산 W_ad 는 본문 식으로 재현되지 않는다 | Yeokyung Lee 외 (Jong-Won Lee 교신) · *ACS Nano* 2026 (ASAP) · `10.1021/acsnano.6c09375` |
| `lee2026_lpscl_coating_thickness_ncm811` | 2 · 6 | ★★★ | mechanofusion 건식 코팅으로 LPSCl 껍질 두께를 네 수준으로 — 두 차단형 대칭셀로 σ_ion · σ_e 를 따로 재니 σ_ion 은 안쪽 최대, σ_e 는 단조 감소 (카드).  **'많이 덮을수록 좋다' 가 아니다** → P2 문안의 한정 · 대칭셀 측정 설계의 본보기 | Lee 외 · *Small Structures* 7, e70530 (2026) · `10.1002/sstr.70530` |
| `kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb` | 2 | ★★ | [우리 그룹] 유성 원심 혼합기로 LPSCl 을 NCM811 에 무용매 건식 코팅 · **코팅분만큼 추가 SE 를 줄여 총 SE 를 맞춘** 비교 설계 (카드) — 논지의 '같은 SE 총량' 조건 그대로.  결과는 고전압 · 계면 화학 쪽 (논지가 '하지 않는 말' 영역) → **공정 · 비교 설계 부분만** 읽는다 | Junhee Kang 외 (Jong-Won Lee 교신) · *Chem. Commun.* 61, 16850–16853 (2025) · `10.1039/d5cc04349b` |
| `kim2025_conductive_agent_se_coating_cathode` | 2 | ★★ | 유성 혼합기로 LPSCl (작은 입자) 을 LiNbO₃ 코팅 NCM711 에 코팅 — 도전재를 같이 넣으면 (0D vs 1D) 코팅층 구조 · 전자 경로가 달라진다 (카드).  건식 host–guest 코팅의 실례 · SBE/DBE 첨가제와도 닿음 | Dongyoung Kim 외 (Yong Min Lee 교신) · *Battery Energy* 2025 · `10.1002/bte2.20250027` |
| `so2022_dem_compaction_coated_particles_assb` | 2 · 6 | ★★★ | SE 코팅 (core–shell) vs 입자 혼합을 DEM 냉간압밀로 비교 — 코팅이 낮은 압력에서 SE 퍼콜레이션을 먼저 만들고, 저압에서는 쉘이 AM–AM 전자 접촉을 가린다 (카드) · Otani (A′01) 와 같은 Inoue 연구실.  **P2 → P3 사슬의 압축 쪽 선행 DEM** · 우리 LC 팔 해석의 비교 대상 | So 외 (Inoue 교신) · *J. Power Sources* 530 (2022) 231279 · `10.1016/j.jpowsour.2022.231279` |
| `frankenberg2024_dem_high_intensity_mixer_assb` | 1 · 3 | ★★★ | 고강도 믹서의 ASSB 복합양극 혼합을 CG DEM (JKR · 접촉력 f² 스케일링) + 3 단계 보정 (안식각 · 압축) 으로 — 응력강도 · 비에너지 → 이종응집 · 풀셀 용량 (카드).  **D2 (CG 하에서 점착을 어떻게 키우나)** · 실험 보정 절차의 본보기.  한계: 할라이드 SE · LFP · 전달 σ 없음 (카드) | Frankenberg 외 (Kwade) · *Powder Technology* 435 (2024) 119403 · `10.1016/j.powtec.2024.119403` |
| `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` | 1 · 2 | ★★★ (⚠ 카드 = 뼈대) | mechanofusion 으로 단결정 NCM 에 할라이드 SE 코팅 + DEM 응력강도 (카드 한 줄 요약).  논지와 가장 가까운 '건식 코팅 + DEM' 실험 논문이지만 **카드가 PDF 없이 만든 뼈대 (⏳ 문서 대기) → 인용 금지** → Part D | Kissel, Frankenberg 외 · *Nature Communications* 2026 · `10.1038/s41467-026-71305-2` |
| `lee2025_halide_segregation_uhs_mixing_li_chalcogen_assb` | 1 | ★★ | 고속 원심 혼합 (장시간) 이 아지로다이트 표면 조성을 바꾸고 LPSCl 자체 σ 가 크게 떨어진다 (카드).  **센 건식 혼합 · 코팅은 SE 를 바꿀 수 있다** → 실험 쪽 코팅 공정 해석의 주의 (모델은 SE 물성을 고정한다) | Jieun Lee 외 (Amine, Xu 교신) · *Science* 388, 724–729 (2025) · `10.1126/science.adt1882` |
| `lee2025_corolling_dryprocess_lpscl_ptfe` | 1 | ★★ | LPSCl + NCM811/NCM82 + VGCF + PTFE 건식 co-rolling 박막 — 우리와 같은 재료의 **건식 막 · 자립막** 실험 (카드).  실험 축 (건식 전극 · 자립막) 의 같은 재료 앵커 | Dong Ju Lee 외 (Zheng Chen 교신) · *Nat. Commun.* 16, 4200 (2025) · `10.1038/s41467-025-59363-4` |
| `thorntonning1998_adhesive_elastoplastic_contact` | 4 | ★★★ | 점착 탄소성 구 충돌의 **붙는 임계 속도** · 반발계수 해석해 · JKR pull-off (카드).  논지 §2-4 *"충돌 에너지보다 접착 에너지가 큰 접촉만 살아남는다"* · §6 *"부착 · 이탈 임계 속도"* 의 정본 출처 후보 · 논지 §2-6 의 SE–SE 붙는 속도 상한 산술을 검증할 축 | Thornton, Ning · *Powder Technology* 99(2) 154–162 (1998) · `10.1016/S0032-5910(98)00099-0` |
| `pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament` | 4 | ★★ | LPSCl 벌크 · 표면 DFT — 종결별 표면 · 파괴 에너지 · SI 슬랩 구조 (카드).  **D4 (SE 표면 에너지 계산) 의 출발 구조** | Pustorino 외 · *Chem. Mater.* 37, 313–321 (2025) · `10.1021/acs.chemmater.4c02577` |
| `kim2026_moisture_surface_degradation_lpscl_dryroom` | 4 | ★★ | 드라이룸 미량 수분에도 LPSCl 표면이 단계적으로 O-농화층으로 바뀐다 (카드).  논지 §2-3 ⚠ *"실제 분말 표면은 … 청정 표면 계산값과 다를 수 있다"* 의 직접 근거 → **D4 · §2-8 에서 γ_SE 를 청정 표면값으로만 두지 않을 이유** | Yoon-Seong Kim 외 (Dong-Hwa Seo 교신) · *Nat. Commun.* 17, 9270 (2026) · `10.1038/s41467-026-75537-0` |
| `shenouda2020_dem_metal_powder_am_liggghts_tutorial` | 5 | ★★ | LIGGGHTS 튜토리얼 — **점착에너지밀도 (CED) 를 바꿔 안식각** 을 보는 데모 (카드).  **D3 (SE–SE 점착을 안식각으로 앵커)** 를 우리 엔진 · 우리 점착 모형 그대로 시험하는 가장 작은 예.  한계: 금속 분말 · 기술보고서 | Shenouda, Hoff · LLNL-TR-813736 (2020, 기술보고서 · DOI 없음) |
| `kim2025_impedance_decoupling_tlm_assb` | 6 | ★★★ | 우리 랩 — 황화물 복합양극 대칭셀 + 수정 TLM 으로 이온 · 전자 수송 · 계면 전하전달 · 확산을 분해 (카드).  실험 쪽 **대칭셀 이온전도도** (논지의 실험 축) 를 모델 σ_ion 과 맞댈 때의 방법 정본 | Siwon Kim 외 (Jong-Won Lee 교신) · *Electrochim. Acta* 2025 · `10.1016/j.electacta.2025.147413` |
| `schlautmann2023_se_particle_size_composite_transport` | 6 | ★★ | 무탄소 NCM811 + LPSCl 복합양극에서 SE 입도 분포만 바꿔 — 작은 SE 가 기공을 줄이고 SE 를 고르게 퍼뜨려 유효 σ_ion 을 올린다 · 접촉저항 없는 복셀 모델은 σ_el 추세가 실측과 어긋난다 (카드).  **'SE 분포 → σ_ion' 의 실험 사례 (P3)** | Schlautmann 외 (Zeier 교신) · *Adv. Energy Mater.* 13, 2302309 (2023) · `10.1002/aenm.202302309` |

**그 밖의 관련 카드** (주제만 닿음 — 위 표를 읽은 뒤에)
- 1 건식: `mun2025_dry_electrode_technology_assb_review` · `liu2025_dry_processing_high_energy_li_batteries_review` · `wang2026_dryprocess_thick_cathode_failure_ncm94` · `matthews2024_ptfe_nanofibril_network` · `kang2025_bollard_anchored_binder_dry_electrode` · `lee2025_dual_fibrous_ptfe_dry_electrode` · `koo2025_cnt_wrapped_sc_nca_dry_cathode` · `choi2026_bzox_dry_zro2x_nmc_shell_coating` (산화물 껍질 · 같은 mechanofusion 공정) · `lyu2025_3d_dem_drying_calendering_lib` (습식 건조 — 거리 멂)
- 4 접착 접촉 모형: `dmt1975_adhesion_contact_deformation` · `luding2008_cohesive_frictional_contact_models` · `thakur2014_eepa_adhesive_elastoplastic_dem` · `pasha2014_linear_elastoplastic_adhesive_contact`
- 5 보정 · 유동: `coetzee2017_dem_calibration_review` · `paulick2015_elastic_particle_properties_dem_review` · `molerus1975_theory_of_yield_cohesive_powders`
- 6 수송 · 측정: `minnmann2021_jes_charge_transport_bottlenecks` · `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` · `malifarge2017_tortuosity_symmetric_cell_impedance_tlm` · `siroma2015_transmission_line_model_porous_electrode_impedance` · `tailored_cathode_microstructure_low_pressure_assb` · `reisacher2023_percolation_sulfide_carbon_matrix` (LPSCl 2 차 응집의 정성 관찰 — 브리핑 초안 `docs/reviews/mixer_cohesion_briefing_draft_20261002.md` §2) · `oh2026_bimodal_composite_cathode` · `kim2024_carbon_volumetric_occupation_se_domain`

---

## Part B — 새 후보 (정본 litdb 에 카드 없음 · 2026-10-13 확인)

> 카드 유무 = 정본 `papers/` 목록 + 카드 본문 낱말 검색 (제목 · 저자 · DOI 조각) 으로 확인.  일부는 다른 카드의 **참고문헌으로만** 나온다 — 그 사실은 서지 교차 확인이라 '왜' 칸에 적었다.
> 표지 칸은 모든 행이 같다: **검색 결과 서지 · 원문 미확인**.

### B1. 건식 혼합 · 건식 코팅 · 건식 막 (주제 1)

| # | 우선 | 서지 (검색 결과) | URL | 왜 이 논문인가 (검색 요약 기준) | 표지 |
|---|---|---|---|---|---|
| B1-1 | ★★★ | Hippauf, Schumm, Doerfler, Althues, Fujiki, Shiratsuchi, Tsujimura, Aihara, Kaskel (요약) · *Overcoming binder limitations of sheet-type solid-state cathodes using a solvent-free dry-film approach* (목록 제목) · Energy Storage Materials 21 (2019) 390–398 (요약) · DOI 10.1016/j.ensm.2019.05.033 (요약) | https://www.sciencedirect.com/science/article/abs/pii/S2405829719302715 | 황화물 SE 복합양극을 섬유상 PTFE 건식막 (자립막) 으로 — 저바인더 · 고로딩 · 무용매 셀 (요약).  우리 실험 축 (건식 전극 · 자립막) 의 기준 문헌.  정본 카드 `mun2025_…` (ref [33]) · `matthews2024_…` 가 인용한다 | 검색 결과 서지 · 원문 미확인 |
| B1-2 | ★★★ | Frankenberg, Heck, Kissel, Lange, Faka, Diener, Haase, Michalowski, Zeier, Janek, Kwade (요약) · *Tailoring Composite Microstructure Through Milling for Dry‐Processed Sulfide‐Based Solid‐State Battery Cathodes* (목록 제목 "… - Frankenberg - 2025 - Small") · Small 21(41) e07279 (2025) (요약) · DOI 10.1002/smll.202507279 (URL 에 표시) | https://onlinelibrary.wiley.com/doi/full/10.1002/smll.202507279 | LPSCl + NCM 건식 복합양극을 밀링 강도별로 — SE 입경 감소 · SE–AM 응집체 형성 · 이종 접촉 밀도를 실험 + DEM 으로, 과한 에너지는 열화 (요약).  **'혼합 강도 → 응집 · 접촉 → 성능' = P3 사슬의 실험 + DEM 선례** · `frankenberg2024_…` · `kissel2026_…` 와 한 묶음 | 검색 결과 서지 · 원문 미확인 |
| B1-3 | ★★ | Pfeffer, Dave, Wei, Ramlakhan (요약) · *Synthesis of engineered particulates with tailored properties using dry particle coating* (목록 제목) · Powder Technology 117(1–2) (2001) 40–67 (요약) · DOI 10.1016/S0032-5910(01)00314-X (요약) | https://www.sciencedirect.com/science/article/abs/pii/S003259100100314X | 큰 host 에 미세 guest 를 용매 · 바인더 없이 기계적으로 입히는 건식 입자 코팅의 장치 · 기전 · 공정 모델 리뷰 (요약).  'SE 선코팅' 공정 어휘 (host–guest · 충격 블렌딩 · mechanofusion) 의 바탕 | 검색 결과 서지 · 원문 미확인 |

### B2. 활물질에 SE 코팅 — 건식 경로 중심 (주제 2 · 6)

| # | 우선 | 서지 (검색 결과) | URL | 왜 이 논문인가 (검색 요약 기준) | 표지 |
|---|---|---|---|---|---|
| B2-1 | ★★★ | Nakamura, Kawaguchi, Masuyama, Sakuda, Saito, Kuratani, Ohsaki, Watano (요약) · *Dry coating of active material particles with sulfide solid electrolytes for an all-solid-state lithium battery* (목록 제목) · Journal of Power Sources 448 (2020) 227579 (요약) · DOI 10.1016/j.jpowsour.2019.227579 (요약) | https://www.sciencedirect.com/science/article/abs/pii/S0378775319315721 | 건식 충격 블렌딩으로 NCM 단입자에 Li3PS4 연속층 (core–shell) — NCM 파손 없이, 반쪽셀 율 · 사이클 개선 (요약).  **'같은 SE 를 AM 위에 먼저 입힌다' 의 공정 원형** · `so2022_dem_compaction_coated_particles_assb` 카드의 실험 대조 [17] (Nakamura) 가 이 논문인지는 미확인 | 검색 결과 서지 · 원문 미확인 |
| B2-2 | ★★ | Kawaguchi, Nakamura, Watano (요약) · *Parametric study of dry coating process of electrode particle with model material of sulfide solid electrolytes for all-solid-state battery* (목록 제목) · Powder Technology 305 (2017) 241–249 (요약) · DOI 10.1016/j.powtec.2016.09.085 (요약) | https://www.sciencedirect.com/science/article/abs/pii/S0032591016306702 | 모델 SE (Na2SO4) 로 날개 끝 속도 · 처리 시간 · host/guest 비를 바꿔 피복 조건을 본다 — 충격력이 모자라면 덮이지 않는다 (요약).  코팅 **공정 창** = LC 팔을 '실제 코팅' 에 대응시킬 때의 실험 쪽 근거 | 검색 결과 서지 · 원문 미확인 |
| B2-3 | ★★★ | Kawaguchi, Nakamura, Hayakawa, Ohsaki, Watano (요약 · 연구 DB 목록) · *Statistical analysis of electrode fabrication process for all-solid-state batteries and effects of electrode fabrication conditions on battery performance* (목록 제목) · Advanced Powder Technology 34(12) 104264 (2023) (요약) · DOI 10.1016/j.apt.2023.104264 (요약) | https://www.sciencedirect.com/science/article/abs/pii/S0921883123003291 | 단순 혼합 vs 건식 코팅 (core–shell) 입자를 실험계획법으로 — 두 경우 성능을 가장 크게 움직이는 인자가 다르다 (혼합 = 압밀 압력, 코팅 = SE 비) (요약).  **코팅 vs 혼합 대조 실험의 설계 사례** (P2 · P3) | 검색 결과 서지 · 원문 미확인 |
| B2-4 | ★★★ | Lee, D. 외 (요약 — 2026 인용 표기 "Lee, D. et al." · 저자 목록 · 소속은 검색 요약끼리 엇갈림 → [미확인]) · *Shear force effect of the dry process on cathode contact coverage in all-solid-state batteries* (목록 제목) · Nature Communications 15, 4763 (2024) (요약) · DOI 10.1038/s41467-024-49183-3 (요약) | https://www.nature.com/articles/s41467-024-49183-3 | 무바인더 손혼합 펠릿 · 습식 · 건식 전극의 AM 피복률을 화상 분석으로 비교 — 건식 (전단) 쪽 피복률이 높고 율 · 사이클이 좋다 · 피복률 → 활물질 이용률 모델 (요약).  **공정 (전단) → 접촉 → 성능** 사슬 · 논지 §6 *"10-02 #59 · #62 KETI 논문 단서"* 의 **후보** (KETI 소속 여부 미확인 — 1저자 확인) | 검색 결과 서지 · 원문 미확인 |
| B2-5 | ★★★ | 저자 [미확인] (보도자료 요약: Yoon-Cheol Ha (KERI) · Byung Gon Kim (Kyung Hee Univ.) · Janghyuk Moon (Chung-Ang Univ.) 팀) · *Exploring optimal cathode composite design for high-performance all-solid-state batteries* (목록 제목) · Energy Storage Materials (2024 — 요약) · 권 · 쪽 [미확인] · DOI [미확인] | https://www.sciencedirect.com/science/article/abs/pii/S2405829724004331 | 손혼합 · 완전 core–shell 대신 **SE 피복률 100 % 미만** 을 설계 규칙으로 둔 기계 혼합 (불활성 분위기 블레이드 밀) (요약).  '다 덮을수록 좋다' 가 아니라는 반례 후보 → `lee2026_lpscl_coating_thickness_…` 와 같이 P2 문안의 한정 | 검색 결과 서지 · 원문 미확인 |
| B2-6 | ★★ | Jaeik Kim, Joonhyeok Park 외 (요약 — 고려대 연구 포털 기록 · 목록 잘림) · *High-Performance All-Solid-State Batteries Enabled by Intimate Interfacial Contact Between the Cathode and Sulfide-Based Solid Electrolytes* (요약) · 저널 · 연도 · DOI [미확인] | https://scholar.korea.ac.kr/item/2595e663-b70b-4484-bebc-3a69de9892c2 | mechano-fusion 으로 NCM811 core – LPSCl shell 입자 → 높은 NCM 분율 · 후막급 셀 (요약).  한양대 Taeseup Song 그룹 MRS 2024 발표와 저자가 겹친다 (요약) — `kang2025_highvoltage_…` 카드가 적은 선행 *"Song et al. (ref 19, dry mechanofusion SE 코팅)"* 과 같은 논문인지 **미확인** | 검색 결과 서지 · 원문 미확인 |

### B3. 응집성 분말의 혼합 균질도 (주제 3)

| # | 우선 | 서지 (검색 결과) | URL | 왜 이 논문인가 (검색 요약 기준) | 표지 |
|---|---|---|---|---|---|
| B3-1 | ★★★ | Lacey (목록 제목 "… - Lacey - 1954 - Journal of Applied Chemistry" · 이름 머리글자 [미확인]) · *Developments in the theory of particle mixing* (목록 제목) · Journal of Applied Chemistry 4(5) 257–268 (1954) (요약) · DOI 10.1002/jctb.5010040504 (URL 에 표시) | https://onlinelibrary.wiley.com/doi/10.1002/jctb.5010040504 | 혼합을 성분으로 나누고 혼합 속도를 확산식으로 다룬 원전 (요약) — **Lacey 지수의 출처** (정본 `jadidi2023_…` 카드도 출처로 적는다).  우리 M 의 **'이론 분모' (완전 분리 · 무작위 분산)** 를 원전에서 확인 → 논지 §5 · M 이 [0, 1] 밖으로 나가는 문제 | 검색 결과 서지 · 원문 미확인 |
| B3-2 | ★★★ | Hersey (요약 — 인용 목록들) · *Ordered mixing: A new concept in powder mixing practice* (목록 제목) · Powder Technology 11(1) 41–44 (1975) (요약) · DOI [미확인] | https://www.sciencedirect.com/science/article/abs/pii/0032591075800210 | 응집성 · 상호작용 입자의 혼합은 '무작위화' 가 아니라 '무질서 → 질서' 로 가는 **'정렬 혼합'** 이라는 개념 제안 (요약) · 미세 입자가 굵은 입자 표면에 붙어 단위를 이룬다는 설명은 인용 문헌 쪽 요약.  논지 §2-5 *"상호작용 · 정렬 혼합 — 정본 카드 없음 [미확인]"* 의 **원전 후보** | 검색 결과 서지 · 원문 미확인 |
| B3-3 | ★★★ | Jarray, Shi, Scheper, Habibi, Luding (요약) · *Cohesion-driven mixing and segregation of dry granular media* (목록 제목) · Scientific Reports 9, 13480 (2019) (요약) · DOI [미확인] | https://www.nature.com/articles/s41598-019-49451-z | 회전 드럼에서 실란 처리로 점착을 조절한 유리 입자 실험 — 단분산은 점착이 크면 분리, 이분산은 적당한 점착이 분리를 줄인다 · 혼합 예측 틀 (요약).  **우리 회전 드럼 · P1 (점착이 상별 응집을 남기나) 의 실험 대조** | 검색 결과 서지 · 원문 미확인 |
| B3-4 | ★★ | Chandratilleke, Yu, Bridgwater, Shinohara (요약) · *A particle‐scale index in the quantification of mixing of particles* (목록 제목 "… - Chandratilleke - 2012 - AIChE Journal") · AIChE Journal 58(4) 1099–1118 (2012) (요약) · DOI 10.1002/aic.12654 (URL 에 표시) | https://aiche.onlinelibrary.wiley.com/doi/10.1002/aic.12654 | **배위수로 정의한 입자 스케일 혼합지수** (PSMI) 를 DEM 블레이드 믹서에서 기존 지수와 비교 (요약).  칸 없는 접촉 기반 지수 = `docs/reviews/prereg_m7_aggregation_20260919.md` (접촉 enrichment · CN 기반 Lacey) 의 선행 | 검색 결과 서지 · 원문 미확인 |
| B3-5 | ★★ | Nase 외 (요약 — 저자 목록 [미확인]) · *Discrete characterization tools for cohesive granular material* (목록 제목) · Powder Technology 116(2–3) 214–223 (2001) (요약) · DOI [미확인] | https://www.sciencedirect.com/science/article/abs/pii/S0032591000003983 | **granular Bond number** (점착력 / 무게) 와 충돌을 넣은 **collisional number** 를 정의하고 더미 · 텀블러 · 호퍼에서 시험 (요약 · 점착 = 액가교).  논지 §2-1 '쌍 Bond 수' · §2-4 '충돌보다 점착이 큰 접촉만 남는다' 의 무차원 틀 | 검색 결과 서지 · 원문 미확인 |

### B4. 표면 에너지 · 접착 (주제 4)

| # | 우선 | 서지 (검색 결과) | URL | 왜 이 논문인가 (검색 요약 기준) | 표지 |
|---|---|---|---|---|---|
| B4-1 | ★★★ | Johnson, Kendall, Roberts (요약 — 왕립학회 기록) · *Surface energy and the contact of elastic solids* (목록 제목) · Proceedings of the Royal Society A 324(1558) 301–313 (1971) (요약) · DOI 10.1098/rspa.1971.0141 (요약) | https://royalsocietypublishing.org/rspa/article/324/1558/301/13377/Surface-energy-and-the-contact-of-elastic-solids | 표면 에너지가 접촉 크기와 떼는 힘을 바꾸는 탄성 구 이론 (JKR) + 고무 · 젤라틴 구 실험 (요약).  논지 §2-1 *"떼는 힘 F ≈ (3/2)π·W·R\*"* 의 원전 (정본 `otani2025_…` 카드가 그 논문의 참고문헌으로 같은 권 324 를 적는다) | 검색 결과 서지 · 원문 미확인 |
| B4-2 | ★★★ | Begat, Morton, Staniforth, Price (요약 — Bath 연구 포털 기록) · *The cohesive-adhesive balances in dry powder inhaler formulations I: Direct quantification by atomic force microscopy* (요약) · Pharmaceutical Research 21(9) 1591–1597 (2004) (요약) · DOI 10.1023/B:PHAM.0000041453.24419.8a (요약) | https://researchportal.bath.ac.uk/en/publications/the-cohesive-adhesive-balances-in-dry-powder-inhaler-formulations-2/ | AFM 콜로이드 탐침으로 **같은 물질끼리 (응집) 와 다른 물질 사이 (접착) 힘의 비 (CAB)** 를 직접 재는 방법 (요약).  논지 §2-8 *"NCM–NCM · NCM–SE · SE–SE 떼는 힘"* 측정의 형판 · 판가름 수 F_SE–AM / F_SE–SE 에 바로 대응.  ⚠ 포털 주소 끝 '-2' 가 Part II 와의 구분일 수 있음 — 확인 필요 | 검색 결과 서지 · 원문 미확인 |
| B4-3 | ★★ | Fowkes (요약) · *ATTRACTIVE FORCES AT INTERFACES* (목록 제목) · Industrial & Engineering Chemistry 56(12) 40–52 (1964) (요약) · DOI 10.1021/ie50660a008 (URL 에 표시) | https://pubs.acs.org/doi/10.1021/ie50660a008 | 표면 에너지를 분산 · 극성 성분으로 나누는 Fowkes 식 (요약).  논지 §2-1 **기하평균 규칙 W ≈ 2√(γ_i·γ_j) (분산 성분)** 의 출처 후보 · IGC 분산 성분 해석의 바탕 | 검색 결과 서지 · 원문 미확인 |
| B4-4 | ★★ | van Oss, Chaudhury, Good (요약) · *Interfacial Lifshitz-van der Waals and polar interactions in macroscopic systems* (요약) · Chemical Reviews 88(6) 927–941 (1988) (요약) · DOI 10.1021/cr00088a006 (요약 · 다른 요약에선 미확인) | https://pubs.acs.org/toc/chreay/88/6 | 표면 장력을 무극성 (LW) + 산 · 염기 (전자 받개 · 주개) 성분으로 나누는 모형 (요약).  논지 §2-7 *"극성 성분이면 기하평균 규칙이 깨질 수 있다"* 를 정량하는 틀 · 이 모형에 대한 비판도 있다 (요약) | 검색 결과 서지 · 원문 미확인 |
| B4-5 | ★★ | Matsusaka, Maruyama, Matsuyama, Ghadiri (요약) · *Triboelectric charging of powders: A review* (목록 제목) · Chemical Engineering Science 65(22) 5781–5807 (2010) (요약) · DOI 10.1016/j.ces.2010.07.005 (요약) | https://www.sciencedirect.com/science/article/abs/pii/S0009250910004239 | 분체 취급 중 마찰 대전 · 대전 입자의 부착 · 벽 부착 리뷰 (요약).  논지 §2-7 *"건식 혼합의 마찰 대전 (모델에 없음)"* 의 출발점 | 검색 결과 서지 · 원문 미확인 |
| B4-6 | ★★ | Garcia, Bareño, Yan, Chen, Hauser, Croy, Iddir (요약 — LBL 출판 목록) · *Surface Structure, Morphology, and Stability of Li(Ni1/3Mn1/3Co1/3)O2 Cathode Material* (목록 제목) · The Journal of Physical Chemistry C 121(15) 8290–8299 (2017) (요약) · DOI 10.1021/acs.jpcc.7b00896 (URL 에 표시) | https://pubs.acs.org/doi/10.1021/acs.jpcc.7b00896 | NMC111 저지수 면의 DFT 안정성 · 형상 (요약).  **D4 (코팅 전 NCM 표면 에너지 계산) 의 출발점** — 우리 NCM811 과 조성이 다르고, 종결 · 화학퍼텐셜 가정을 따로 명시해야 한다 | 검색 결과 서지 · 원문 미확인 |
| B4-7 | ★★ | Mohammadi-Jam, Waters (요약) · *Inverse gas chromatography applications: A review* (목록 제목) · Advances in Colloid and Interface Science 212 (2014) 21–44 (요약) · DOI 10.1016/j.cis.2014.07.002 (요약) | https://www.sciencedirect.com/science/article/abs/pii/S0001868614002164 | IGC 의 원리 · 장치 · 응용 (분산 · 특이 성분 표면 에너지 · 불균일도) 리뷰 (요약).  논지 §2-8 *"코팅 전후 NCM · SE 분말의 유효 표면 에너지 (IGC)"* 측정 계획의 입문 | 검색 결과 서지 · 원문 미확인 |

### B5. 유동성 앵커 · DEM 점착 보정 (주제 5)

| # | 우선 | 서지 (검색 결과) | URL | 왜 이 논문인가 (검색 요약 기준) | 표지 |
|---|---|---|---|---|---|
| B5-1 | ★★★ | Roessler, Katterfeld (요약) · *DEM parameter calibration of cohesive bulk materials using a simple angle of repose test* (목록 제목) · Particuology 45 (2019) 105–115 (요약) · DOI 10.1016/j.partic.2018.08.005 (요약) | https://www.sciencedirect.com/science/article/abs/pii/S1674200119300033 | 점착 분말용 '원통 들어올림' 안식각 시험 — 흐름 단계 · 원통 크기 · 속도 무관성 · 기둥의 휨 · 붕괴를 새 기준으로 (요약).  **D3 (SE–SE 점착을 안식각 실험으로 앵커) 의 보정 절차** | 검색 결과 서지 · 원문 미확인 |
| B5-2 | ★★ | Alizadeh 외 … Hassanpour (요약) · *A methodology for calibration of DEM input parameters in simulation of segregation of powder mixtures, a special focus on adhesion* (목록 제목) · Powder Technology 339 (2018) (요약 · 쪽 [미확인]) · DOI 10.1016/j.powtec.2018.08.028 (요약) | https://www.sciencedirect.com/science/article/abs/pii/S0032591018306442 | 혼합물의 분리 DEM 에서 점착을 계면 에너지로 두고 안식각 + cohesion number 로 보정 · 3 성분 혼합 더미의 분리로 시험 (요약).  **D2 (상 쌍별 점착 입력) · D3 의 '혼합물' 보정 사례** | 검색 결과 서지 · 원문 미확인 |
| B5-3 | ★★ | Geldart, Abdullah, Hassanpour, Nwoke, Wouters (요약) · *Characterization of powder flowability using measurement of angle of repose* (목록 제목 — White Rose 저장소) · China Particuology 4(3–4) 104–107 (2006) (요약) · DOI 10.1016/S1672-2515(07)60247-4 (요약) | https://eprints.whiterose.ac.uk/id/eprint/85192/ | 적은 양의 약한 점착 분말도 재는 안식각 시험기 · 결과가 Hausner 비와 일관 (요약).  **글러브박스 · 소량 SE 분말로 D3 앵커를 잴 때의 방법 후보** | 검색 결과 서지 · 원문 미확인 |
| B5-4 | ★★ | Deng, Garg, Bradley (요약) · *A study of particle adhesion for cohesive powders using a novel mechanical surface energy tester* (목록 제목) · Powder Technology 391 (2021) 46–56 (요약) · DOI 10.1016/j.powtec.2021.06.002 (요약) | https://www.sciencedirect.com/science/article/abs/pii/S0032591021005192 | 입자를 얹은 기판을 여러 높이에서 떨어뜨렸다 멈춰 떨어져 나간 입자의 크기를 분석 → 떼는 힘과 분말 Bond 수를 내는 기계식 시험기 (요약) · 습도 영향 후속 연구 있음 (요약).  **SE–SE 떼는 힘 · Bond 수를 분말 상태로 직접 재는 길** (D3 · §2-8) | 검색 결과 서지 · 원문 미확인 |

### B6. 혼합 상태 → 압축 뒤 미세구조 · σ_ion (주제 6)

| # | 우선 | 서지 (검색 결과) | URL | 왜 이 논문인가 (검색 요약 기준) | 표지 |
|---|---|---|---|---|---|
| B6-1 | ★★★ | Otani, Muta, Furuta, Miyuki, Kaburagi, Inoue (요약 — 정본 카드 `otani2025_…` 참고문헌 [5] · `miss2026_insitu_conductivity_porosity_pressure_compaction` 참고문헌 26 과 서지 일치) · *Ionic conductivity prediction model for composite electrodes and quantification of ionic conductivity reduction factors in sulfide-based all-solid-state batteries* (목록 제목) · Journal of Energy Storage 58 (2023) 106279 (요약 · 카드 참고문헌) · DOI 10.1016/j.est.2022.106279 (요약) | https://www.sciencedirect.com/science/article/abs/pii/S2352152X2202268X | 황화물 복합전극의 이온전도 예측 모형 · 전도도 감소 인자 정량 (요약).  **A′01 (Otani 2025) 의 실험 앵커** · `otani2025_…` 카드 §0 에 따르면 `lee2024_multiphysics_dem_fem_initial_pressure_assb` 카드가 이 논문의 SE 분율–굴곡 경험식을 **카드 없이** 쓰고 있다 → P3 의 σ 쪽 비교 대상이자 카드화가 급한 이유 | 검색 결과 서지 · 원문 미확인 |

> **(B2-2 · B2-3 · B2-4 · B2-5 · B1-2 도 주제 6 에 닿는다** — 공정 → 접촉 · 피복 → 성능.)

### 검색에서 믿을 만한 것을 못 찾은 주제 (빈칸을 숨기지 않는다)

| 주제 | 결과 | 대신 |
|---|---|---|
| NCM · 황화물 SE **분말의 실측 표면 에너지** (IGC · AFM) | 배터리 분말을 직접 잰 문헌을 못 찾음 | 방법론만 (B4-2 · B4-7) · 같은 랩의 AFM-FS W_ad (`lee2026_mechanical_halogen_…`) |
| **황화물 SE 분말 유동성** (안식각 · Hausner 비 · 전단셀) | 못 찾음 | D3 앵커는 우리 SE 분말로 직접 재야 할 가능성 (B5-1 · B5-3 · B5-4 방법) |
| 회전 드럼에서 **JKR 점착 · 크기가 다른 이원 미분 혼합** 을 Bond 수로 쓸어 본 DEM | 정확히 맞는 것을 못 찾음 | Jarray 2019 실험 (B3-3) · 정본 `jadidi2023_…` 카드가 모은 원저들 (점착 텀블러 DEM 포함) |
| 논지 §6 의 **KETI 논문 단서** (10-02 #59 · #62) | 후보 하나 (B2-4) · ✅ 10-13 카드 대조: B2-4 (`lee2024_shear_force_dry_process_cathode_coverage`) = KETI 교신 (Seung Ho Choi · KyungSu Kim) 맞음 · 단서 문구 없음 · #62 발화의 *"케티에서 나온 유지성 박사님"* = 새 26 편 저자에 없음 · 정본 카드 중 KETI J.-S. Yu (Ji-Sang Yu · 한글 이름 [미확인]) 공저 = `kim2024_carbon_volumetric_occupation_se_domain` · `jung2023_single_crystal_ncm_morphology` (둘 다 다른 주제 — 카드 기준) | 1저자 확인 (제목 · PDF) |
| **Hausner 비 원전** (1967) | 제목을 확인하지 못해 뺐다 | B5-3 이 Hausner 비와의 일치를 다룬다 |
| 작은 입자–큰 입자 부착의 곡률 (R\*) · 임계 부착 속도 | 새 문헌을 따로 찾지 않음 | 정본 `thorntonning1998_…` · `dmt1975_…` |
| 습식 SE 코팅 경로 (용액 침투 · 용액 코팅) | 검색에 나왔지만 건식 논지와 별개라 목록에서 뺐다 | — |

---

## Part C — 권장 읽기 순서 (처음 10 편)

| 순서 | 무엇 | 어디 | 볼 것 (예측 P1–P3 · 결정 D2–D4 와 연결) |
|---|---|---|---|
| 1 | Otani 2025 | A′01 (카드 ✅) | **P3** — 응집 상태가 압축 뒤 AM\|SE 접촉 · 힘사슬 · 밀도를 어떻게 바꾸는지, 무엇을 관측량으로 쓰는지.  모든 쌍 γ 하나라 P1 · P2 는 이 논문이 답하지 않는다는 점까지 |
| 2 | Lee 2026 (ACS Nano, 건식 코팅 · W_ad) | Part A (카드 ✅) | **D4 · §2-8** — 코팅 품질을 정한 W_ad 를 AFM 으로 잰 방법과 계산 방법 · 카드 한정어 (계산 재현 불가) · 같은 랩 원자료 |
| 3 | Nakamura 2020 + Kawaguchi 2017 | B2-1 · B2-2 | **'SE 선코팅' 이 물리적으로 무엇인가** — 충격 블렌딩의 공정 창 (속도 · 시간 · 비) · 연속층 조건 → LC 팔을 실제 코팅에 대응시킬 근거 |
| 4 | Lee D. 2024 (Nat. Commun.) | B2-4 | **공정 (전단) → 피복 → 이용률** — 피복률 정의 · 화상 분석 방법 · KETI 단서인지 |
| 5 | KERI ESM 2024 + Lee 2026 (Small Struct., 두께) | B2-5 · Part A | **P2 문안의 한정** — 피복률 100 % 미만 설계 규칙 · σ_ion 안쪽 최대 · σ_e 단조 감소 ('다 덮을수록 좋다' 가 아님) |
| 6 | Jarray 2019 + Nase 2001 | B3-3 · B3-5 | **P1 · D2** — 회전 드럼에서 점착 크기 · 크기비가 분리 · 혼합을 어떻게 바꾸나 · Bond 수와 충돌수의 틀 |
| 7 | JKR 1971 + Fowkes 1964 (+ van Oss 1988) | B4-1 · B4-3 · B4-4 | **논지 §2-1 – §2-3 식의 원전** — 떼는 힘 · 기하평균 규칙 · 극성 성분이 들어오면 무엇이 깨지나 (D2 결합 규칙) |
| 8 | Begat 2004 + Mohammadi-Jam 2014 | B4-2 · B4-7 | **§2-8 측정 계획** — AFM 응집 · 접착 힘의 비 (CAB) 와 IGC 로 판가름 수 (γ_A/γ_S · F_SE–AM/F_SE–SE) 에 어떻게 다가가나 |
| 9 | Roessler 2019 + `shenouda2020_…` + Geldart 2006 | B5-1 · Part A · B5-3 | **D3** — SE–SE 점착을 안식각으로 앵커하는 절차 · LIGGGHTS CED ↔ 안식각 · 소량 분말 시험 |
| 10 | Lacey 1954 + Nadeem 2023 + Chibwe 2020 | B3-1 · A′05 · A′06 | **논지 §5 관측량** — Lacey 이론 분모 (M 음수 해소) · 무작위 기대로 나누는 이웃 지수 · 압축 전 프레임의 거리 지수 |

---

## Part D — 정본 카드로 먼저 만들 것 (1저자가 PDF 를 주면)

> 카드 규칙 (CLAUDE.md litdb 절 · 규율 ⑥): 정본 브랜치 `papers/` 목록 전수로 중복 확인 → PDF (SI 포함) 로 서지 · 값 확인 → 정본 브랜치에만 추가.  **이 문서는 카드를 만들지 않았다.**

| 순위 | 대상 | 왜 먼저 |
|---|---|---|
| 1 | Otani 2023 (B6-1) | 정본 카드 둘이 인용하고, 한 카드는 이 논문의 경험식을 **카드 없이** 쓰고 있다 (규율 ⑥ 상 가장 급함) · A′01 의 실험 앵커 |
| 2 | Nakamura 2020 (B2-1) | 'SE 선코팅' 공정의 원형 · 논지 실험 공정과 가장 가깝다 · `so2022_dem_compaction_coated_particles_assb` 의 실험 대조와 같은 논문인지도 그때 확인 |
| 3 | Lee D. 2024 (B2-4) | 공정 → 피복 → 성능 사슬 · KETI 단서 확인 · 저자 · 소속 어긋남 해소 |
| 4 | KERI ESM 2024 (B2-5) | 저자 · 권 · DOI 가 전부 [미확인] — 서지부터 확정 · 피복률 설계 규칙 |
| 5 | JKR 1971 (B4-1) · Fowkes 1964 (B4-3) · van Oss 1988 (B4-4) | 논지 §2 의 식 (떼는 힘 · 기하평균 규칙 · 극성 성분) 은 논지 문서 머리가 *"litdb 정본 카드로 출처를 확인한 뒤"* 인용하라고 적는다 |
| 6 | Hersey 1975 (B3-2) | 논지 §2-5 의 용어 '상호작용 · 정렬 혼합' 이 지금 [미확인] 표지 |
| 7 | Begat 2004 (B4-2) | §2-8 측정의 형판 · Part I / II 구분부터 확인 |
| 8 | Jarray 2019 (B3-3) | 회전 드럼 · 점착 · 이분산 혼합의 실험 대조 · 공개 접근 (요약) |
| 9 | Roessler 2019 (B5-1) | D3 보정 절차 |
| 10 | `kissel2026_…` (뼈대 카드 완성) | 카드가 있는데 PDF 없이 만든 뼈대라 인용 금지 상태 — 원문으로 채워야 쓸 수 있다 |
| 11 | Frankenberg 2025 (B1-2) | 건식 황화물 양극 + DEM · 공개 접근 (요약) · `frankenberg2024_…` · `kissel2026_…` 와 묶음 |
| 12 | Lacey 1954 (B3-1) | 우리 M 의 원전 · 이론 분모 |
| 13 | B2-6 (고려대 포털 기록) | 저널 · 연도 · DOI 전부 [미확인] — 서지 확정이 먼저 · `kang2025_highvoltage_…` 카드의 선행 ref 19 와 같은지 |

### 1저자 확인이 필요한 것

1. 논지 §6 의 **KETI 논문 단서** 가 B2-4 (*Shear force effect of the dry process …*) 인가. → 10-13 대조: B2-4 = KETI 소속 · 문구 없음 · 10-02 #62 발화 = *"주 포인트로는 케티에서 나온 유지성 박사님 해서 문구는 있었는데 이제 그렇게 주로 한 내용은 아니었던 것"* → 다른 KETI 논문일 가능성 [추정] · 1저자 확인 대기.
2. `lee2026_mechanical_halogen_argyrodite_drycoating` 카드 저자 *Yonghoon An* = ✅ 1저자 본인 (10-13 확인).
3. Part D 의 PDF 중 이미 가진 것 · 받을 수 있는 것.

---

*변경 이력* — 2026-10-13 첫 판 (조사 · 작성).  litdb 정본 브랜치 무변경 · 새 카드 없음.
