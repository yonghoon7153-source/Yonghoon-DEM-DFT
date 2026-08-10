# Cascade 세미나 내용 편집 지시서 — 기준본 24장 (Codex 편집용)

> 역할: 과학 내용 편집자. PPT 편집 없음 — 지시만.
> 기준본: `Research_Seminar_2026_08_cascade_revised.pptx` (SHA `00D9CF8F…`, 24장) — **전 슬라이드 정독 완료**.
> 참조 자료: 요청문 §자료 목록 전부 열람. 문헌 그림은 실제 crop 을 본 것만 추천 (각 항목에 명시).
> 검산: 47종 5족 분류 = scorecard CSV 와 완전 일치 · 141행 실측 · air 문헌 커버리지 35/47 ·
> bvs_slope/cost_tier/mass_per_cation 47/47 · PASS 11종 = {Ag₂O, CaF₂, CaO, Li₂O, LiF, MgF₂, MgO, SiO₂, SnO₂, WO₃, ZnO}.

---

## 1. 한 문단 총평

기준본 24장은 provenance 규율(273 슬롯 vs 47 스냅샷 분리, G4/G5 heuristic 명시, 120 순열, unique-kill)이 이미 정확하고 시각 스타일도 깔끔해서 **골격은 그대로 두는 것이 옳다**. 가장 큰 내용 공백은 셋이다 — ① 청중이 **47종이 실제로 무엇인지 한 번도 보지 못한다**(이름이 화면에 등장하는 후보가 B₂O₃·Cr₂O₃ 등 6~8종뿐), ② webapp/DB 에 이미 있는 **air·low-cost·lightweight·dose-robustness 축이 발표에 전혀 안 나온다**(14 테마 중 화면 등장 축은 사실상 6개), ③ 후보의 **다축 프로필을 한눈에 보는 그림(레이더)이 없다**. 반대로 S15 철회 원장의 SDCP 2행은 cascade 서사와 무관해 사용자 지시대로 빼야 한다. 권장 최종 구성: **본문 21장(18 + 신규 3) / 부록 6장 = 27장**.

---

## 2. S1–S24 전수 편집표

| Source slide | Action | Why | Exact replacement / merge / move instruction | Evidence |
|---|---|---|---|---|
| S1 표지 | **KEEP** | cascade 한정 제목이 이 덱 범위에 맞음 | — | — |
| S2 Context (Sundar coating) | **KEEP** | 문제 제기 + coating≠substitution 단서 이미 있음. 그림은 덱에 내장된 것 유지 | — | litdb `sundar2025_…` (덱 내장 그림) |
| S3 Campaign design record | **KEEP** | 91×3=273 슬롯 정의가 정확 | — | `cascade_v23_champions.csv` |
| S4 Decision architecture | **KEEP** | cascade 의 존재 이유(비용 배치) — 본선 핵심 | — | `docs/cascade_pipeline_guide.md` |
| S5 Pool provenance | **KEEP** | 141=47×3, 44종 미분류, As₂S₃ 유일 문서화 — 검산 통과 | — | champions.csv (141행 실측) |
| S6 Same protocol tiers | **KEEP** | L0–L3 + "DFT 2건" 범위 명시 이미 있음 | — | guide §tiers |
| S7 LPSCl descriptors | **EDIT(소)** | 내용 정확. 단 화면의 `Delta = 0.033 eV` 를 `Δ = 0.033 eV` 로, `No citable comp1 Ea` 는 유지(정본과 일치) | 표기만 교체 | `electronic.json`, `canonical_registry.json` |
| S8 Five gates | **KEEP** | 실제 임계 + blocking heuristic 단서 + G5 ranking-only 전부 정확 | — | `cascade_screening_funnel.json` gates |
| S9 Post-hoc gate view | **KEEP** | 47→43→25→11 + "G5→1\*" 처리 정확 | — | funnel JSON waterfall |
| S10 Standalone/unique kill | **KEEP** | vacuous/redundant 감사 — 이 덱의 백미 | — | scorecard first-stop (G2 4종 검산) |
| S11 47-species snapshot audit (trade-off 그림) | **EDIT(소)** | 그림·주장 정확(6/6 검산). 화면 하단에 한 줄 추가: `A dataset-level trade-off — not causal proof of M–O blocking` | 하단 캡션 1줄 추가 | `cascade_seminar_oxidation_transport_47.csv` (6/6 G4_pass=0 검산) |
| S12 Conditional Pareto | **KEEP** | 조건부·비지배 언어 정확 | — | `cascade_seminar_pareto_47.csv` |
| S13 120 gate orders | **KEEP** | 순서 불변/서사 구분 — 유지 | — | guide 366행 |
| S14 Method-matched claims | **KEEP** | supported/not supported 경계 정확 | — | guide §trust |
| S15 Retraction ledger | **EDIT(대)** | **SDCP 2행 제거**(사용자 지시 — cascade 무관). 남길 실패 사례는 cascade 축 소속 4행으로 재구성. §3-N0 참조 | 행 교체: ① `Single-seed 1.33× conductivity → multi-seed rule` ② `MSD fit outside diffusion → β ∈ [0.8,1.2] gate` ③ `DOS-threshold band gap → fixed-occ eigenvalues` ④ **신규** `air_hsab qualitative tier → [Zhu20] cross-check: 9/35 disagreements, all one direction → axis demoted to CURATED` / 하단 문장 교체: `Failed claims became executable gates — the audit is part of the pipeline` | ④: `cascade_air_axis_lit_vs_tier.csv` (26/9/12 실카운트) |
| S16 Deep-DFT 2/47 | **KEEP** | 3-카운트 병렬(47/11/2) + B₂O₃ 비부분집합 명시 정확 | — | scorecard `dft_deep` |
| S17 UMA + co-doping ML | **EDIT(중)** | 텍스트 정확(LODO/L2DO<0). **우측에 상보성 레이더 1장 추가** — end-member 프로필 겹침이 "왜 pair 인가"를 한눈에 보여줌. 단서 문구 포함 | 그림 삽입: `docs/figures/cascade/cascade_radar_pair_CrHf.png` (✅ 직접 확인) + 캡션 `End-member profiles only — the pair itself is uncomputed (site competition unresolved)` | `cascade_radar_axes_origin.csv` · `dopant_site_preference_literature.md:43,71` |
| S18 Acquisition loop | **KEEP** | exploit/explore/validate — ML 을 label acquisition 으로 이미 옳게 프레이밍 | — | `cascade_ml_integration_guide.md` |
| S19 A1 terminology | **KEEP** | — | — | — |
| S20 A2 protocol matrix | **KEEP** | evidence-level 사전 — G 절 태그 체계의 기반 | — | — |
| S21 A3 scorecard heatmap | **KEEP** | 47종 상세는 부록이 맞음(본문엔 신규 로스터 1장) | — | `cascade_seminar_scorecard_47.csv` |
| S22 A4 defense Q&A | **EDIT(소)** | 5문항 유지 + 1문항 추가: `Q: Why is the air axis not a gate? A: Its literature proxy covers 35/47 (12 unknown ≠ unstable) and our qualitative tier failed a one-directional bias check — it stays descriptive.` | 행 추가 | air CSV + themes.json (35/47 검산) |
| S23 A5 defense Q&A (ML) | **KEEP** | — | — | — |
| S24 A6 source ledger | **EDIT(소)** | 신규 소스 3행 추가 (§7 표의 신규 항목) | 행 추가 | §7 |

---

## 3. 새로 넣을 슬라이드 사양 (본문 +3 — 최소한)

### N1. 후보 지도 (삽입: S5 뒤, 새 S6)
- **English title**: `The 47-species snapshot, by chemical family`
- **한 문장 claim**: 무엇을 탐색했는지 청중이 이름으로 확인한다 — 게이트 결과와 혼동하지 않는 "출연진" 명단.
- **화면용 English copy**:
  - 5개 가족 박스 (요청문 목록 그대로 — scorecard 와 일치 검증 완료):
    `Transition metal (23)` / `Main group (9)` / `Alkaline earth (6)` / `Lanthanide (6)` / `Alkali (3)`
  - 각 박스 안에 화합물 나열, **bold = retained through G4 (11)**, **† = targeted deep-DFT (B₂O₃, Nd₂O₃)**
  - 하단 범례: `bold = through the post-hoc G4 audit (11) · † = targeted deep-DFT case study (2) · 37 oxides + 10 fluorides, versioned 2026-06-25`
  - 금지: "273 에서 살아남은 47" 류 문구 사용 불가 — `versioned snapshot` 만.
- **데이터**: 47종 전부, PASS 11종 bold 지정 목록 = Ag₂O·CaF₂·CaO·Li₂O·LiF·MgF₂·MgO·SiO₂·SnO₂·WO₃·ZnO.
- **figure source**: 없음(텍스트 박스 — 기준본 스타일 유지). 대안으로 부록 A3 heatmap 을 참조 화살표로 언급.
- **Korean speaker notes**: "탐색 대상을 이름으로 보여드립니다. 전이금속 23, 주족 9, 알칼리토 6, 란타나이드 6, 알칼리 3 — 산화물 37과 불화물 10의 versioned snapshot 입니다. 진하게 표시한 11종이 사후 G4 감사까지 남은 후보고, 단검 표시 두 종만 targeted DFT 로 더 들어갔습니다. 이 장은 명단이지 순위가 아닙니다. 자세한 축별 값은 부록 heatmap 에 있습니다."
- **Evidence badge**: `CURATED` (명단) + `STATIC-PROXY` (bold 판정 출처 G4)

### N2. 질문-축 지도 (삽입: S12 뒤, 새 S14)
- **English title**: `One snapshot, different deployment questions — each answer carries its own evidence level`
- **한 문장 claim**: cascade 는 universal winner 기계가 아니라, 사용 목적별 질문에 축과 신뢰도를 붙여 답하는 조회 구조다.
- **화면용 English copy** (4행 표):

  | Deployment question | Axes consulted | Evidence level | Missing handling |
  |---|---|---|---|
  | High-voltage cathode side? | oxidation onset · ESW window | OURS-CALC (MP grand-potential) | — |
  | Survives ambient handling? | ΔG_hyd (lit., binary-sulfide proxy) · HSAB tier | LITERATURE (35/47) · CURATED | 12 unknown — **excluded, never zero** |
  | Cheap and light at scale? | cost tier · formula mass per cation | CURATED (2026 tier) · STATIC-PROXY | qualitative — never $/kg or Wh/kg |
  | Robust to doping level? | BVS proxy drift across 3 campaign labels | STATIC-PROXY (nominal labels) | labels ≠ resolved x |

  - 하단: `No axis alone rejects a candidate; descriptive axes never gate.`
- **데이터**: themes.json (`dG_hyd_MS_lit` 35/47 · `cost_tier`/`mass_per_cation` 47/47 · `bvs_slope` 47/47).
- **figure source**: 없음(표).
- **Korean speaker notes**: "같은 47종 스냅샷에 질문을 바꿔 던질 수 있습니다. 고전압 양극 쪽이 궁금하면 산화 onset 과 창을 보고 — 이건 저희 계산입니다. 공기 취급이 궁금하면 문헌 가수분해 proxy 와 정성 등급을 보는데, 문헌 커버리지가 35 에 47 이고 나머지 12종은 모름이지 불안정이 아닙니다. 비용·무게는 정성 tier 와 화학식 질량 proxy 고, 농도 내성은 세 campaign label 사이 BVS 변화입니다. 핵심은 축마다 증거 수준이 다르다는 것 — 그래서 화면마다 tag 를 붙였고, 서술 축 단독으로는 어떤 후보도 탈락시키지 않습니다."
- **Evidence badge**: 행별 표기 (표 안에 내장)

### N3. 다축 프로필 레이더 (삽입: N2 바로 뒤)
- **English title**: `Candidate profiles across eight axes — strengths trade, they do not add`
- **한 문장 claim**: 후보 4~6종의 팔각형 프로필로 "축마다 승자가 다르다"를 도형으로 보여준다.
- **화면용 English copy**: 그림 전면 + 하단 2줄:
  - `Within-pool favorable percentiles (descriptive ranking, not absolute properties)`
  - `Air axes excluded (provisional after a one-directional bias check); BVSE/blocking are static proxies`
- **데이터/후보**: WO₃(G5 top rank) · CaO · LiF(G4 생존) · B₂O₃(축충돌) · Cr₂O₃ · HfO₂(pair 반쪽). 축 8: Oxidation·ESW window·Li pathway·Low blocking·Disorder·Lightweight·Low cost·Soft.
- **figure source**: `docs/figures/cascade/cascade_radar_6panel.png` (**✅ 직접 확인**, 3300×2280). 재생성: `python3 tools/figures/fig_cascade_radar.py` (도펀트 교체 가능). Origin: `db/properties/cascade_radar_axes_origin.csv`.
- **Korean speaker notes**: "방금 그 질문-축 지도를 후보 단위로 접으면 이 팔각형이 됩니다. WO₃ 는 연질 쪽이 크지만 비용 축이 약하고, CaO 는 고르게 넓고, B₂O₃ 는 산화 쪽이 큰데 Li 경로만 움푹 들어가 있습니다 — 아까 본 트레이드오프가 도형으로 반복되는 겁니다. Cr₂O₃ 와 HfO₂ 는 서로 반대쪽이 큰데, 이 둘을 겹친 그림이 co-doping 절에 나옵니다. 축은 전부 47종 안 상대 percentile 이라 절대 물성이 아니고, 공기 축은 편향 검증이 끝날 때까지 뺐습니다."
- **Evidence badge**: `STATIC-PROXY`+`UMA-PROXY`+`CURATED` 혼합 — 그림 캡션에 명시 (위 2줄이 그 역할)

### (S15 EDIT 에 딸린 신규 행 N0 — 별도 슬라이드 아님)
- `air_hsab` 행: 위 §2 S15 참조. **몇 초**: 15초 (한 문장 — "공기 정성 축은 문헌 대조에서 한 방향 편향이 잡혀 서술 등급으로 강등했습니다"). 이 사례가 "왜 축에 증거 수준을 붙이는가"(N2)의 복선이 된다.

---

## 4. 삭제·부록 이동 목록

| 항목 | 처리 | 비고 |
|---|---|---|
| S15 의 `Deep adsorption = strong bond` 행 (SDCP) | **완전 삭제** | cascade 무관 — 사용자 지시 |
| S15 의 `9 meV pose difference = preference` 행 (SDCP) | **완전 삭제** | 동상 |
| 그 외 삭제 대상 | 없음 | 기준본에 DFT 강의·MLIP 일반론·SEI/DEM 상세·roadmap 반복 **이미 없음** — 추가 정리 불필요 |

36장 final 덱의 자산 중 이식하는 것은 §3 의 3장 + S15 ④행 + S22 1문항뿐. 나머지(지도 모식도, DFT 기초 3장, 철회의 철회, provenance 감사 장 등)는 **이식하지 않는다** — 이 덱의 범위 밖.

---

## 5. 권장 최종 순서 (27장)

| # | Title | 구분 |
|---|---|---|
| 1 | A gated MLIP-to-DFT screening cascade for LPSCl modification | BODY |
| 2 | One repair must survive several sulfide interfaces | BODY |
| 3 | Substitution turns one material into hundreds of decisions | BODY |
| 4 | A cascade spends precision only where it matters | BODY |
| 5 | Pool provenance · versioned lineage | BODY |
| 6 | **[N1] The 47-species snapshot, by chemical family** | BODY |
| 7 | Same protocol within each tier | BODY |
| 8 | LPSCl taught us which descriptors to watch | BODY |
| 9 | Five gates ask five different questions | BODY |
| 10 | The auditable hard-gate view stops at 11 | BODY |
| 11 | Standalone kill · unique kill | BODY |
| 12 | Oxidation–transport trade-off (47-species audit) | BODY |
| 13 | Conditional Pareto view within post-hoc G1–G4 | BODY |
| 14 | **[N2] One snapshot, different deployment questions** | BODY |
| 15 | **[N3] Candidate profiles across eight axes** | BODY |
| 16 | All 5! = 120 gate orders enumerated | BODY |
| 17 | Claim strength must match the method | BODY |
| 18 | Failures made the cascade more credible (ledger, 4행 재구성) | BODY |
| 19 | Current deep-DFT coverage: 2 / 47 | BODY |
| 20 | ML is already here — but it is not yet a discovery model (+pair radar) | BODY |
| 21 | The next cascade learns where to calculate next | BODY |
| 22 | A1 Terminology | APPENDIX |
| 23 | A2 Protocol matrix | APPENDIX |
| 24 | A3 47-species scorecard heatmap | APPENDIX |
| 25 | A4 Defense Q&A — cascade & evidence (+air 문항) | APPENDIX |
| 26 | A5 Defense Q&A — validation & ML | APPENDIX |
| 27 | A6 Canonical source ledger (+3행) | APPENDIX |

본문 21 / 부록 6. (요청 범위: 본문 18–22 ✓, 전체 24–28 ✓)

---

## 6. Codex 가 실제 편집 전에 확인할 미해결 사항

1. **레이더 그림 스타일 정합** — `cascade_radar_*.png` 은 house_style 색이라 기준본과 톤이 거의 같지만, 폰트가 DejaVu 다. 위화감이 있으면 `tools/figures/fig_cascade_radar.py` 상단 rcParams 에 폰트만 바꿔 재생성 (1분). 판단은 Codex 재량.
2. **N3 를 6패널로 할지 4패널로 할지** — 한 장에 6개가 빽빽하면 CaO·LiF 를 빼고 4패널(WO₃/B₂O₃/Cr₂O₃/HfO₂)로. 재생성 시 `PANEL` 리스트만 수정. 사용자 취향 확인 권장.
3. **S15 ledger 의 β-gate 행 표기** — `0/6 pass` 는 comp1 사례 숫자인데 host 계 얘기라 cascade 덱에서는 숫자 없이 `β ∈ [0.8,1.2] gate` 만 남기는 쪽을 권장 (숫자를 남기려면 출처가 host MD 감사 문서임을 note 에 명시).
4. **발표 길이 미확정** — 27장은 30–35분 감. 25분 슬롯이면 N3 을 부록으로 내리는 것이 1순위 컷.
5. 데이터 충돌 없음 — 이번 감사에서 기준본 수치 오류는 발견되지 않았다 (S7 표기 1건만 소소).

## 7. Source ledger (신규·수정 슬라이드분)

| Slide / claim | Short visible citation | Canonical local source | Field / row / figure | Evidence level |
|---|---|---|---|---|
| N1 47종 명단·가족 분류 | `Source: cascade_seminar_scorecard_47.csv (47 rows)` | `db/properties/cascade_seminar_scorecard_47.csv` | `dopant`, `group`, `pass_G1_G4`, `dft_deep` | CURATED + STATIC-PROXY |
| N2 ΔG_hyd 커버리지 35/47 | `[Zhu20, literature proxy — 35/47]` | `db/properties/cascade_v23_themes.json` | `dopants[].dG_hyd_MS_lit` (35 non-null 검산) | LITERATURE |
| N2 cost/mass/dose 축 | `Source: cascade_v23_themes.json` | 동일 | `cost_tier` · `mass_per_cation` · `bvs_slope` (각 47/47) | CURATED / STATIC-PROXY |
| N3 레이더 8축 percentile | `Source: cascade_radar_axes_origin.csv` | `db/properties/cascade_radar_axes_origin.csv` (+생성기 `tools/figures/fig_cascade_radar.py`) | 47행 × 8축, favorable 방향 접힘 | STATIC-PROXY/UMA-PROXY/CURATED 혼합 |
| S15 ④ air 축 강등 | `[Zhu20] SI cross-check — 9/35, one-directional` | `db/properties/cascade_air_axis_lit_vs_tier.csv` | agree 26 / disagree 9 / absent 12 (실카운트) | LITERATURE vs CURATED 대조 |
| S17 pair 레이더 | `end-member profiles; pair uncomputed` | `docs/figures/cascade/cascade_radar_pair_CrHf.png` | Cr₂O₃·HfO₂ 두 프로필 | STATIC-PROXY + `dopant_site_preference_literature.md:43,71` (site 는 heuristic·Hf 양쪽성) |
| S22 신규 문항 | — | air CSV + themes.json | 위와 동일 | — |

문헌 그림 신규 추천: **없음** (기준본 내장 Sundar 외 필요 없다고 판정. richards/xiao/zhu crop 은 직접 확인했으나 이 덱 서사에 불요 — 넣지 마라. duquesnoy2023 radar 는 **미확인**(캡션만 봄) — 추천 제외).
