# 끝 보고 — choi2025_silver_exsolution_argyrodite_anode_free (배치 2026-11-24b · #5)

- digest: `litdb/papers/choi2025_silver_exsolution_argyrodite_anode_free.md` (새 파일 · 483 줄 · 한국어 standalone · §0–§16 + Post-processing 표).
- 그림: `litdb/figures/choi2025_silver_exsolution_argyrodite_anode_free/` — 크롭 31 장 = 도구 27 장 (본문 그림 4 + SI 그림 23 · `--pdf 본문 SI --clean`) + 손 크롭 4 장이에요. 손 크롭은 SI 표 3 장 (`Table S1`–`S3` · 캡션이 표 **아래**라 도구가 캡션 밑 빈칸을 자르고 '거의 백지' 로 뺐어요) 과 `Fig. S9` 앞쪽 (그림이 SI p.10–11 두 쪽에 걸치는데 도구는 캡션 쪽 p.11 만 잘랐어요 · `fig_S9_p10.png` · `panel_of: fS9`). 도구가 낸 번호 공백 3 건 (`tS1`–`tS3`) 은 `missing_labels[].resolved` 로 닫았어요. `figures.json` 31 항목 전부 `viewed` · `viewed_how` 를 달았어요. 캡션은 본문 4 장이 두 단 배치 때문에 첫 단에서 잘려 있어서 PDF 글자층 전문으로 바꿨고 (`caption_raw` 에 원래 것), SI 5 장은 글자층 잔재만 고쳤어요 (´ → × · 'oC' → °C).
- 원자료 · 구조: xlsx 24 시트 중 21 시트를 열어 숫자를 다시 냈어요 (S4 · S5 · S6 시트는 안 열었어요). POSCAR 두 개는 ASE 로 읽었어요. 계산은 전부 `scratchpad/choi2025_silver_exsolution_argyrodite_anode_free/` 안에 `choi2025_` 접두 이름으로만 썼어요. Python 은 `-I` 로 돌렸어요.
- 공유 파일 · git: 안 건드렸어요 (`litdb/figures/_sources.json` 은 추출 도구가 이 slug 항목을 더해 다시 썼어요 · 손 안 댐). 나는 git 을 안 썼는데, 그림 폴더 32 파일은 메인 세션 checkpoint `7a9f8c62` (크롭 · 손 크롭 포함) 와 `98271324` (갱신된 `figures.json` — 31 항목 · viewed 31) 에 이미 들어가 있고 지금 HEAD 와 같아요. digest 와 이 보고만 미추적이에요.
- 점검 (읽기만): `build_index.py --check` → 이 digest 는 "어느 인덱스에도 없음 [dft]" + "comparison_vs_ours 미편입" (아래 (a) · (b) 를 넣으면 풀려요) · `extract_figures.py --inbox --only choi2025_silver` → 본문 + SI 자동 매칭 `[제목 75%]` · `extract_figures.py --audit` → 이 slug 경고 없음 (본문 4 · SI 24 · 표 3) · 웹앱 `/paper/<slug>` 200 · 그림 참조 31 · `paper_figure_notes` 30/31 (S9 p.10 손 크롭만 키가 달라 주석이 안 붙어요 · 정상) · `_paper_pis` = `['ysjung']` (저자 줄 'Yoon Seok Jung' 로 잡힘 · 다른 PI 오탐 0) · 원소 Li · Ag · P · S · Cl · Br 연결 ✓ (`/api/element?syms=Ag,Br` 에 이 slug) · 기법 dft · md (AIMD) · pdos · esw 연결 ✓ (XPS 는 용어 사전에 항목이 없어 0 건) · 시험 `test_v3_literature` + `test_v3_markdown` **43/43 통과** · `test_webapp -k "sakamoto or litdb_figure or recent_digests or digest_date or element_papers or glossary_papers or figure_comment"` 7 통과 1 실패 = `test_recent_digests_are_on_every_litdb_surface` (이 배치 digest 들의 INDEX · comparison 미편입 — 합치면 풀려요).

⚠ **메인에 알릴 것**
1. **이 논문엔 점착 W · 흡착 · 계면 · 입계 에너지가 하나도 없어요.** DFT 는 E_hull (도핑 배치 100 개 · MP 기준) · 전위별 분해 E_D(φ) (pymatgen grand potential) · PDOS · 1000 K AIMD 뿐이에요. 우리 W 와 같은 줄에 못 놓아요. 같은 도구 계열인 우리 ESW 와만 방향 대조가 돼요 (창 절대값 일치로는 안 써요).
2. **원자료로 재현이 안 되는 숫자가 둘이에요** (digest §10-① · ② · §14 에 인용 금지를 걸었어요).
   ① 60 °C 파우치 50 사이클 유지율이 본문은 **95.0 %**인데 원자료 `Figure 3h` 로는 **91.5 %** (187.32 / 204.69 mAh g⁻¹) 예요. 95 % 대는 38 사이클이고, 같은 계산으로 낸 30 °C 값 (87.35 %) 은 본문 87.4 % 와 맞아요.
   ② Ag 석출 뒤 층의 전도도가 Methods 기하 (10 µm · ⌀13 mm) 로 낸 값의 ≈100 배예요. 전자전도는 원자료 `Figure S11` 의 R = 29.9 Ω (x = 0.6) 에서 2.5 × 10⁻⁵ S cm⁻¹ 가 나와 보고값 2.5 × 10⁻³ 의 정확히 1/100 이고, 이온전도 (`Figure S10` · Note 1) 는 65–120 배예요. 10 µm ↔ 1 mm 단위 착오와 맞는 배수예요 (기하를 안 적어서 확정은 못 해요). 정성 결론 (전자전도 급증) 은 남고, '석출 뒤에도 이온전도 유지 (1.3 → 1.0 mS cm⁻¹)' 는 이 자료로 뒷받침되지 않아요.
3. **POSCAR 정체를 확정했어요.** `Direct configuration= 1` · `=200000` 이라 1000 K AIMD (2 fs) 의 첫 틀과 400 ps 틀이고, 두 틀로 잰 MSD (Li 1227.74 · Ag 171.67 · P 9.98 · S 11.21 · Cl 11.69 Å²) 가 원자료 `Figure S22` 의 마지막 행과 소수점까지 같아요. 시작 구조의 부피 (998.73 Å³) 는 `Figure 1d` x = 0.75 의 #85 이고, 그게 100 개 중 **E_hull 최저 (19.36 meV/atom)** 예요. `Fig. S22` 의 MSD 는 단일 시간원점 · 실험실 좌표라 골격 표류 3.27 Å 가 들어 있어요 (빼면 골격 0.2–0.5 Å²). 구조에서 Ag 셋은 **S 하고만** 배위하고 (Cl 0), 자유 음이온은 4d · 4a 두 자리 모두 S : Cl = 2 : 2 로 섞여 있어요 (Methods 엔 없음).
4. **같은 배치 이웃 연결.** 병렬로 생긴 `xie2024_agc_buffer_layer_lithiation_delithiation_mechanism` (배치 #11 · 벌크 Li–Ag 합금 상) 과 `kasemchainan2019_…` (#10 · 이 논문 ref 18) 은 digest 의 계보 · §7d-6 · §16 에 slug 로 달았어요 (그쪽 값은 안 옮겼어요). `lee2020_…` (#9 · Ag–C 원전 · 이 논문 ref 35) · `ko2025_…` (#8) 는 내가 확인할 때 digest 가 없어서 '진행 중' 으로만 적었어요 — 그 digest 들이 끝나면 choi2025 와 역링크를 걸지 메인이 정해 주세요 (남의 digest 라 안 건드렸어요).
5. **baer 보고 (d) #1 의 Kotakadi ChemRxiv 판은 저널에 나왔어요** — *Joule* 9, 102175 (2025-11) · DOI 10.1016/j.joule.2025.102175 (Crossref 확인 · 저자 6 명 같음). baer 보고 · 추가 목록에 반영이 필요해요.
6. 공개 심사자로 **Ieuan Seymour** 가 실려 있어요 (`seymour2021_…` 의 1저자 · W_ad 보고서 8-1 의 W ≥ 2γ_Li 문턱 원전). 심사 파일은 inbox 에 없어요.
7. (d) #3 Park 2025 (*Inorg. Chem. Front.*) 의 저자 Cho W. · Kim K. 은 이 논문의 KETI 저자 (Woosuk Cho · KyungSu Kim) 와 이름이 같아요 — 같은 그룹으로 보이지만 소속은 확인 안 했어요.
8. 발견 검색 (최근 2 년 먼저): Crossref 주제어 검색 6 번 + 서지 확인 8 번 (DOI 4 · 제목 4 · 일반 UA · 개인 정보 없음). 받은 기준은 제목 · 첫 저자 · 저널 · 연도가 다 맞을 때만이에요.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 한 묶음)` — 행 순서상 **'Ag/C 인터레이어' 묶음 끝** (`metzler2026_sputtered_ag_carbon_interlayers_anode_free` 다음 · `shi2026_…` 앞). 같은 배치 이웃 `xie2024_…` (#11) · `lee2020_…` (#9) 도 같은 묶음일 거예요. 저자에 Jeff Sakamoto 가 없어서 🏷 는 안 달아요.

| `papers/choi2025_silver_exsolution_argyrodite_anode_free.md` **(본문 9 pp + SI 30 pp + 원자료 xlsx 24 시트 + POSCAR 2 · 크롭 31 장 (도구 27 + 손 4 = `Table S1`–`S3` · `Fig. S9` p.10) · 31 장 전부 봄 — 18 장 원해상도 · 13 장 대조표 · 원자료 21 시트 재계산 · POSCAR ASE 대조 · 2026-11-24)** | **[외부·exp+DFT(VASP-PBE · vdW 없음 · E_hull · grand potential · PDOS)+AIMD(1000 K · 400 ps · 52 원자)·⭐⭐ SE 격자 안 Ag⁺ 가 첫 충전에 석출되어 친Li 씨앗 · ⛔ W · 흡착 · 계면 에너지 0 — 우리 W 와 같은 줄 금지]** ✅ **Seung Ho Choi**†\*/Chang Hoon Baek†/Jihoon Oh/Geung-Jong Lee/Minsoo Kim/Hyesu Lee/Dong-Joo Yoo/**Yoon Seok Jung**/KyungSu Kim/Ji-Sang Yu/**Woosuk Cho**\*/**Haesun Park**\*/**Jang Wook Choi**\* (KETI · 연세대 · 서울대 · 중앙대 · 고려대), "**Silver exsolution from Li-argyrodite electrolytes for initially anode-free all-solid-state batteries**" — ***Nat. Commun.* 16, 5871 (2025)**, DOI `10.1038/s41467-025-61074-9` (CC BY-NC-ND 4.0). Li₆₋ₓAgₓPS₅Cl (x 0.2–0.6 · Ag⁺ 48h · Methods '48a' 오기) 10–15 µm 층 + LPSClBr 분리층 · 첫 방전 **1.8 V 평탄** (✎ 원자료 1.799 V · 1.0 mA cm⁻² · 60 °C) 에서 Ag⁺ → Ag (이론 48.9 mAh g⁻¹ 의 96 % 를 1.2 V 까지) → β LiAg (0.12 V) → γ₃ Li₉Ag₄ (0.04 V) → γ₂ Li₁₀Ag₃ (0.005 V) · 첫 석출 = SE \| SUS 접점 → 입계 · 기공 → 도금 Li 속 Ag (EDS) → 박리 뒤 SE 입계 합금. DFT: E_hull < 50 meV/atom (배치 100 · 원자료) · grand potential Li₆PS₅Cl 창 1.71–2.13 V · **Ag⁺/Ag 1.92 V (창 안)** · 같은 전위에서 숙주 평형은 Li₃PS₄ + LiCl + Li₂S (골격 유지는 속도론) · PDOS bulk 1.65 · GB 1.54 · 1.36 eV (읽는 법 미기재). 반쪽 x = 0.6 1179 사이클 CE 99.69 % · CCD 6.0 mA cm⁻² · 파우치 NCM811 7.0 mAh cm⁻² · 2.0 MPa (WIP 500 MPa · 80 °C 로 제조) · 1312 Wh L⁻¹. 🔴 60 °C 50 사이클 95.0 % ↔ 원자료 91.5 % · 석출 뒤 σ_ion · σ_e ≈100 배 (Methods 기하 가정) · E_D 창 값 ≠ E_hull · x = 0.75 의 0.93 V 반응식 불균형 · K 58 > 50 인데 'feasible' · AIMD = 사실상 Ag 1 개 · MSD 단일 원점 + 골격 표류 3.27 Å (✎ POSCAR) | 점착 트랙: W(LPSCl \| Ag) 는 '첫 충전 전' 계면 — LPSCl · Ag⁰ 공존 창 ✎ ≈1.71–1.92 V · 운전 중 = LPSCl \| SEI \| Li–Ag · 7 절 ③ 합금 상 순서의 실험 표적 · 8-3 (Ag 가 도금 Li 속에 퍼짐 · 첫 핵 = 집전체 접점) 과 같은 방향 · ⛔ 우리 W · ESW 절대값과 같은 줄 금지 · 이웃 `xie2024_…` · `metzler2026_…` · `lu2026_…` · `kasemchainan2019_…` (ref 18) |

---

## (b) `comparison_vs_ours.md` 에 넣을 줄

**A–D 물성 4축의 본 자리는 없어요** (음극 · 공정 논문). B① (같은 도구 계열 ESW) · D (띠틈) · E (음극 계면) · F (도핑) 에 방향 행만 냈어요.

### b-1. `📑 Reference key` 표에 한 행 (4 칸: 약칭 | 논문 | digest/status | 유형)

| **[Choi25AgEx]** **SE 격자 안 Ag⁺ 를 첫 충전에 석출시켜 친Li 씨앗으로 — Li₆₋ₓAgₓPS₅Cl \| LPSClBr 이중층 · 무음극** · ⛔ **W · 흡착 · 계면 에너지 0 — 우리 W 와 같은 줄 금지** · ⛔ **60 °C 95.0 % · 석출 뒤 σ 수치 인용 금지 (원자료 재현 안 됨)** | Seung Ho Choi\*/Chang Hoon Baek/…/Yoon Seok Jung/…/Woosuk Cho\*/Haesun Park\*/Jang Wook Choi\* (KETI · 연세대 · 서울대 · 중앙대 · 고려대) 2025 ***Nat. Commun.* 16, 5871** (DOI 10.1038/s41467-025-61074-9 · CC BY-NC-ND 4.0) — "Silver exsolution from Li-argyrodite electrolytes for initially anode-free all-solid-state batteries" | ✅ `papers/choi2025_silver_exsolution_argyrodite_anode_free.md` — 판정은 §E 1 행 + §B① · §D · §F 각 1 행 | exp + DFT (VASP-PBE · E_hull · grand potential · PDOS) + AIMD (1000 K) |

### b-2. §E 표에 한 행 (4 칸: 주장 | 출처 | 우리 | 일치)

| **🆕 (2026-11-24) SE 격자 안 Ag⁺ 가 첫 리튬화 1.8 V (✎ 원자료 1.799 V · 1.0 mA cm⁻² · 60 °C) 에서 금속 Ag 로 석출 — 숙주 grand-potential 창 (1.71–2.13 V) 안 (DFT Ag⁺/Ag 1.92 V) · 이어서 β LiAg (0.12 V) → γ₃ Li₉Ag₄ (0.04 V) → γ₂ Li₁₀Ag₃ (0.005 V) · 첫 석출은 SE \| SUS 접점 → 입계 · 기공 → 도금 Li 속 Ag (EDS) → 박리 뒤 SE 입계 합금** — ✎ LPSCl 과 Ag⁰ 가 준안정하게 공존하는 창 ≈1.71–1.92 V · 운전 (≈0 V) 계면 = LPSCl \| SEI \| Li–Ag | **[Choi25AgEx]** `Fig. 2b` · `Fig. 2c` · `Fig. 2d` · `Fig. S9` · `Fig. 3c–g` · `Fig. S16` · 원자료 `Figure 2b` · `Figure 2c` · `Figure 2d` | 우리 LPSCl \| Ag(111) W 두 종결 (위치만: `db/properties/adhesion.json` · W_ad 보고서 2-3 절) · 우리 ESW 환원 한계 1.717 V (`litdb/our_dft_baseline.md`) | 🟡 **W 의 '상태' 선언 근거** (W(LPSCl \| Ag) = 첫 충전 전 · 금속 Ag 의 계면) · ⛔ 우리 W 와 같은 줄 금지 (이 논문 계면 계산 0) · ⛔ 60 °C 95.0 % · 석출 뒤 σ_ion · σ_e 수치 인용 금지 · ✎ 0.005 V 까지 용량의 ≈10 % 는 γ₂ 합금으로 설명 안 됨 (SE 환원 몫일 수 있음 · SEI 분석 0) |

### b-3. §B 표에 한 행 (4 칸: 축 | 우위 | 출처 | 우리 값 / 재현)

| **B① 🆕 (2026-11-24) LPSCl grand-potential 창의 또 하나의 문헌 점 + Ag 도핑 — Li₆PS₅Cl 1.71 V (`+ 20 Li → 4 LiCl + 20 Li₂S + 4 P`) · 2.13 V (교환 0 `→ Li₃PS₄ + LiCl + Li₂S`) · 2.37 V LiS₄ · Li₆₋ₓAgₓPS₅Cl (x 0.25–0.75) 의 Ag⁺/Ag 1.92 V · 창 안 E_D −13.6 / −22.3 meV/atom (✎ 원자료 · `Fig. 1e` 의 E_hull 최저 17.1 / 19.4 와 안 맞음)** | (우위 아님 — **같은 도구 계열 대조**) | **[Choi25AgEx]** `Fig. 2d` · `Fig. S9` (pymatgen + MP · VASP-PBE 520 eV · 보정 미기재) | 우리 comp1 환원 한계 1.717 V · 산화 개시 2.14 V (LiS₄ 포함) / 2.256 V (LiS₄ 제외 · 정본) — 🟡 방향 같음 · 같은 데이터베이스 · 같은 도구라 독립 확인이 아니다 · **창 절대값이 맞는다고 쓰지 않는다** (`HZ-esw-reduction-limit-label` · `HZ-esw-reduction-limit-facet-convention`) · ✎ 반응식 균형 검산: x = 0.75 의 0.93 V 줄만 Li 불균형 (`4 LiP` 여야) |

### b-4. §D 표에 한 행 (4 칸: 주장 | 출처 | 우리 | 비고)

| **🆕 (2026-11-24) Ag 도핑 Li₅.₂₅Ag₀.₇₅PS₅Cl PBE 띠틈 bulk 1.65 · Σ3[110]/(111) 1.54 · Σ5[100]/(210) 1.36 eV — 읽는 법 미기재 · ✎ 원자료 DOS 문턱 (10⁻³) 재판독 1.73 · 1.60 · 1.41 · 축소는 CB 쪽 (VBM 셋 다 0) · VBM 아래 0.5 eV 투영 DOS 의 Ag 34–37 %** | **[Choi25AgEx]** `Fig. 4c` · 원자료 `Figure 4c` · `Fig. S23` | comp1 2.066 · modelc 2.099 eV (fixed-occ nscf 고유값 · 비교군 `gap-fixedocc-eigenvalue-v1`) | ⛔ **비교군이 다르다** (DOS 판독 · 금지 `dos_threshold_readout`) · 'wide-gap' 수준만 · 방향 (Ag 4d 가 VBM 에 섞인다) 만 · GB 모형의 크기 · 이완 · 에너지 미기재 · 'GB 띠틈이 좁아 GB 에서 먼저 석출' 은 추론 (자기 자료 `Fig. S16` 은 집전체 접점에서 먼저) |

### b-5. §F 표에 한 행 (3 칸: 주장 | 출처 | 우리 연결)

| **🆕 (2026-11-24) '희생 도펀트' — 숙주 환원 한계보다 높은 전위에서 환원되는 양이온 (Ag⁺/Ag 1.92 V > 숙주 1.71 V) 을 SE 에 넣으면 첫 충전에 셀 안에서 친Li 씨앗이 생긴다 · 다른 양이온 E_hull Cu 20 · K 58 · Na 41 · Mg 43 · Zn 48 meV/atom (K 는 자기 기준 50 초과인데 'feasible') · 실험 σ (293 K) 2.0 → 1.3 mS cm⁻¹ · Ea 0.36 → 0.42 eV (x 0 → 0.6)** | **[Choi25AgEx]** `Fig. 1d–f` · `Table S1` · `Fig. S9` | 우리 도핑 cascade 에 '도펀트 환원 전위 > 1.717 V (우리 환원 한계)' 를 거름 축으로 넣을 수 있다 (같은 grand potential 도구 · 제안 · 시험 안 됨) · σ · Ea 는 축이 달라 숫자 대조 안 함 · 홉 수 검산 (ν₀ 10¹³ s⁻¹ 가정 · 293 K): Ea 0.36 → 1/Γ ≈ 0.16 µs · 0.42 → ≈ 1.7 µs |

### b-6. (권장 · 점착 트랙의 실제 집) `comparison_vs_ours_DEM.md` §I 에 블록 (지금 I-22 · baer 보고가 I-23 을 제안했으니 **I-2x** — 번호는 메인이 정해 주세요)

### I-2x. `choi2025_silver_exsolution_argyrodite_anode_free` — ★★ (exp + DFT · ⛔ W 아님) **SE 안 Ag⁺ 가 첫 충전에 씨앗이 된다 — W(LPSCl \| Ag) 는 '첫 충전 전' 계면 · 운전 중은 LPSCl \| SEI \| Li–Ag**

- **무엇**: Li₆₋ₓAgₓPS₅Cl 층의 Ag⁺ 가 첫 리튬화 1.8 V 에서 SE \| SUS 접점부터 입계 · 기공으로 석출되고, 더 낮은 전위에서 LiAg → Li₉Ag₄ → Li₁₀Ag₃ 로 합금하며, 도금 Li 속으로 퍼졌다가 박리 뒤 SE 입계에 합금으로 남는다.
- **점착 트랙에 주는 것 셋**: ① 우리 LPSCl \| Ag(111) W 의 **상태 선언** — 같은 논문 grand potential 로 보면 LPSCl 과 금속 Ag 가 함께 서는 전위는 ✎ ≈1.71–1.92 V 뿐이라, 이 W 는 '첫 충전 전 · 반응 전 · 금속 Ag' 의 값이다 (8-3 의 'LPSCl \| Ag 는 첫 충전 전의 계면' 을 전위로 뒷받침) ② 7 절 ③ 합금 구동력의 **실험 표적** — 상 순서 β (0.12) · γ₃ (0.04) · γ₂ (0.005 V) 와 DFT (MP) 단계 0.59 · 0.37 · 0.14 · 0.07 V · 순서 대조만 (상 이름이 다르다) ③ 8-3 과 **같은 방향의 관찰** — Ag 가 도금 Li 속에 퍼지고, 첫 석출은 집전체 접점에서.
- **DEM 쪽 쓰임** (출처 그대로 · 시나리오 입력 후보): 제조 압력 (반쪽 50 MPa 냉간 + 500 MPa 1 분 · 파우치 WIP 500 MPa · 80 °C) · 운전 적층압 (반쪽 20 MPa · 파우치 2.0 MPa) · 층 두께 (Ag-SE 10 µm (figure-read ≈12) · 캐스트 15 µm · 이중층 35 µm · LPSClBr 막 ≈700 µm) · 입도 1–3 µm · 도금 Li 5.0 mAh cm⁻² ≈ 23 µm (figure-read · ✎ 조밀 Li 24 µm) · '석출 Ag–Li 가 공극을 채운다' (`Fig. S18` · SEM 대비만 · 정량 아님).
- **금지**: 이 논문 숫자를 우리 W · ESW · 띠틈과 같은 줄 · 60 °C 95.0 % · 석출 뒤 σ 수치 · AIMD 를 Ag 확산 계수 · 장벽으로.

---

## (c) `pdf_map.tsv`

**필요 없어요** — `extract_figures.py --inbox --only choi2025_silver` (매칭표만) 가 본문 + SI 를 자동으로 붙였어요 (`[제목 75%]`). 굳히고 싶으면 한 줄:

```
choi2025_silver_exsolution_argyrodite_anode_free	choi2025_ag_exsolution_argyrodite
```

---

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저)

> litdb 에 이미 있거나 이 배치에서 먹는 중이라 세지 않은 것: ref 18 `kasemchainan2019_…` (배치 #10) · ref 20 `wang2019_…` · ref 32 `spencerjolly2023_…` · ref 33 `zhu2015_…` · ref 34 `schwietert2020_…` · Xie 2024 `xie2024_…` (배치 #11) · ref 35 Lee 2020 *Nat. Energy* (배치 #9 `lee2020_…` · 진행 중) · Ko 2025 *Nat. Commun.* (배치 #8 · 진행 중).
> 대조: `litdb/papers` 파일 이름 + digest 본문 grep (DOI · 제목) · `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md` grep · 이 배치 `batch.json`. '왜' 는 제목 · Crossref 메타 기준이에요 (본문 안 엶).

| # | 문헌 | 왜 (우리 축) | litdb | 목록 |
|---|---|---|---|---|
| 1 | Kotakadi, Aspinall, Burton, Liang, Aihara, Pasta · *Joule* 9, 102175 (2025) — "Impact of metallic interlayers at the lithium-Li6PS5Cl solid electrolyte interface" · DOI 10.1016/j.joule.2025.102175 (Crossref 확인 · 발견 검색) | Li \| LPSCl 의 금속 인터레이어 — W_ad 7 절의 실험 짝 (baer 보고 (d) #1 ChemRxiv 판의 저널판) | 없음 | 없음 |
| 2 | Wang Y., Raj V., Naik K., Vishnugopi B. … · *Adv. Mater.* 37, 2410948 (2025) — "Control of Two Solid Electrolyte Interphases at the Negative Electrode of an Anode-Free All Solid-State Battery based on Argyrodite Electrolyte" · DOI 10.1002/adma.202410948 (Crossref 확인 · 발견 검색) | 무음극 아지로다이트 음극의 SEI 둘 — '운전 중 계면 = LPSCl \| SEI \| 금속' 의 실험 근거 | 없음 | 없음 |
| 3 | Park Y., Kang S., Kim T., Oh H., Kim K., Cho W., Kim S. · *Inorg. Chem. Front.* 12, 5449 (2025) — "Temperature-dependent interfacial reactions between a sulfide argyrodite solid electrolyte and a lithium metal anode" · DOI 10.1039/d5qi00760g (Crossref 확인 · 발견 검색) | 이 논문은 60 °C 운전 — Li \| LPSCl 반응의 온도 의존 (같은 그룹으로 보임 · 소속 미확인) | 없음 | 없음 |
| 4 | Oh J., Choi S., Kim H., Kim J., Lee G., Bae K. … · *Energy Environ. Sci.* 17, 7932 (2024) — "Lithio-amphiphilic nanobilayer for high energy density anode-less all-solid-state batteries operating under low stack pressure" · DOI 10.1039/d4ee03130j (Crossref 확인 · SI ref 6) | 친Li · 소Li 를 겹친 층 · 2.0 MPa (`Table S2` 의 Mg-W 행) — 7 절 친Li 판정의 설계 사례 | 없음 | 없음 |
| 5 | Yu T., Li H., Liu Y. … Zhou H. · *Sci. Adv.* 9, eadj8171 (2023) — "A prototype of dual-ion conductor for all-solid-state lithium batteries" · DOI 10.1126/sciadv.adj8171 (Crossref 확인 · ref 37) | Li₆PS₅Cl 안 Cu⁺ 이동 — SE 쪽 금속 양이온 이동의 선례 · '희생 도펀트' (b-5) | 없음 | 없음 |
| 6 | Ye Y., Xie H., Yang Y., Xie Y., Lu Y., Wang J. … · *J. Am. Chem. Soc.* 145, 24775 (2023) — "Solid-Solution or Intermetallic Compounds: Phase Dependence of the Li-Alloying Reactions for Li-Metal Batteries" · DOI 10.1021/jacs.3c08711 (Crossref 확인 · ref 31) | Li–Ag 고용체 대 금속간 화합물 — 7 절 ③ · 도금 Li 속 Ag 고용체 해석 | 없음 | 없음 |
| 7 | Liu X., Garcia-Mendez R., Lupini A. … · *Nat. Mater.* 20, 1485 (2021) — "Local electronic structure variation resulting in Li 'filament' formation within solid electrolytes" · DOI 10.1038/s41563-021-01019-x (Crossref 확인 · ref 38) | 입계 전자 상태 → Li 필라멘트 — 이 논문 GB 띠틈 논거의 원전 | 없음 | 없음 |
| 8 | Jung Y.-C., Hwang C., Kwak M., Jeon S., Lee Y., Kwak W. … · *J. Mater. Chem. A* 11, 25275 (2023) — "On-site formation of silver decorated carbon as an anodeless electrode for high-energy density all-solid-state batteries" · DOI 10.1039/d3ta05307e (Crossref 확인 · SI ref 5) | Ag 를 셀 안에서 '스스로' 만드는 다른 길 (탄소 쪽) — 이 논문 (SE 쪽) 과 짝 | 없음 | 없음 |

다음 순번: Sandoval 외 *Joule* 7, 2054 (2023) (ref 13 · **목록에 있음** 표 2 #6) · Park, Jung, Sohn *Electrochem. Solid-State Lett.* 12, A171 (2009) (나노 Ag 리튬화 · ref 30) · Quirk & Dawson *Adv. Energy Mater.* 13, 2301114 (2023) (입계 설계 · ref 39).

---

## (e) DEM-DFT 보고서 (W_ad 보고서) 에 쓸 거리

| 보고서 항목 | 이 논문에서 쓸 점 | 위치 (쪽 · 그림 · 표 · 원자료) | 직접 봤나 |
|---|---|---|---|
| **1. 2-3 절 LPSCl \| Ag(111) — W 의 '상태'** | grand potential 로 Ag⁺/Ag 1.92 V · 숙주 환원 1.71 V → LPSCl 과 금속 Ag 의 준안정 공존 창 ✎ ≈1.71–1.92 V · 음극 운전 (≈0 V) 에서는 전자가 통하는 Ag (합금) 에 닿은 LPSCl 이 환원 → 실제 계면 = LPSCl \| SEI \| Li–Ag · **우리 W 는 '첫 충전 전 · 금속 Ag' 계면의 값**으로 적는다 | p.3–4 · `Fig. 2d` · `Fig. S9` (SI p.10–11) · 원자료 `Figure 2d` · digest §3d · §7d-3 | ✅ `Fig. 2` · `S9` 두 쪽 원해상도 · 시트 열람 · 반응식 전부 균형 검산 |
| **2. 7 절 ③ 합금 · 반응 구동력** | 실험 상 순서 β LiAg (0.12 V) → γ₃ Li₉Ag₄ (0.04 V) → γ₂ Li₁₀Ag₃ (0.005 V) + 도금 뒤 Li-풍부 고용체 (EDS) · DFT (MP) 단계 LiAg₃ 0.59 · LiAg 0.37 · Li₈Ag₅ 0.14 · Li₃Ag 0.07 V — 우리 pymatgen grand potential 로 바로 낼 수 있고 실험 순서가 대조 표적 (순서 대조만 · 상 이름 다름) · 이웃 `xie2024_…` 의 벌크 합금 계산과 같이 | p.3 · `Fig. 2c` · `Fig. S9` · digest §3c · §3d · §7d-6 | ✅ 원해상도 · 원자료 `Figure 2c` |
| **3. 7-1 표 Ag 행 ('충전 중 Li–Ag 합금 면 후보')** | 후보 면을 상 순서로 — LiAg · Li₉Ag₄ · Li₁₀Ag₃ · Li-풍부 bcc 고용체 (도금 Li 와 닿는 것은 마지막) | `Fig. 2c` · `Fig. 3f` · `Fig. S21` | ✅ 원해상도 (`3f` 2 배 확대) |
| **4. 8-3 절 (Ag/C 층에서 Li 가 쌓이는 곳)** | 같은 방향 관찰 둘 — ① Ag 가 도금 Li 층 전체에 퍼진다 (5.0 mAh cm⁻² · 파우치 50 % 방전) ② 첫 석출은 전자가 들어오는 집전체 접점 (1 분 · 0.016 mAh cm⁻²) · 다른 점 — 박리 뒤 Ag 가 남는 곳이 탄소 위가 아니라 **SE 층 입계 (합금)** | p.4–5 · `Fig. 3f` · `Fig. 3g` · `Fig. S16` · `Fig. S21` | ✅ 원해상도 |
| **5. 2-3 · 2-4 절 종결 해석 (정성)** | DFT 구조 (POSCAR) 의 Ag⁺ 셋은 S 하고만 배위 (2.44–3.04 Å · Cl 0) — 'Ag 가 S 와 결합할 자리' 를 종결 설명에 같이 적을 근거 · ⚠ 계면 계산이 없고 격자 Ag⁺ ≠ 금속 Ag⁰ 라 **두 종결 순위 근거로 쓰지 않는다** | digest §4a (✎ POSCAR 대조) | ✅ ASE |
| **6. 8-4 절 압력 · DEM 입력** | 제조 (반쪽 50 MPa 냉간 + 500 MPa 1 분 · 파우치 WIP 500 MPa · 80 °C) · 운전 (반쪽 20 MPa · 파우치 2.0 MPa) · 층 두께 · 입도 1–3 µm · 도금 Li 23 µm @ 5 mAh cm⁻² (figure-read) — '2.0 MPa' 는 늘 제조 압력과 같이 쓴다 | Methods p.7 · `Fig. S19` · `Table S3` · `Fig. 3f` | ✅ `Table S3` · `3f` 원해상도 · `S19` 대조표 |
| **7. 6 절 한계 · 8-6 절 '가져오지 않는 것'** | 셀 수치 두 개가 원자료로 재현 안 됨 (60 °C 95.0 → 91.5 % · 석출 뒤 σ ≈100 배) · 파우치 CE > 100 % (Li 저장고) — 이 논문 셀 성능을 근거로 쓸 때 단서 | `Fig. 3h` · `Fig. S10` · `Fig. S11` · 원자료 `Figure 3h` · `Figure S10` · `Figure S11` | ✅ 원해상도 (`3h`) · 대조표 (`S10` · `S11`) · 시트 재계산 |
| **8. 3 절 작은 모델 DFT 확인 (내부 대조)** | POSCAR_initial (최저 E_hull 의 Li₅.₂₅Ag₀.₇₅PS₅Cl 52 원자) · POSCAR_final (1000 K 400 ps) — UMA 로 같은 셀을 돌려 끝 상태 · Ag 이동을 견줄 시작점 (CC BY-NC-ND · 출처 표기 · 셀까지 이완된 구조라 우리 고정셀 규율과 다름) | digest §4a · §7f | ✅ ASE |

보고서 문장 후보 (공유 보고서 문체 · 출처는 랩 표준 꼴):
- *고체전해질 격자 안에 넣은 Ag⁺ 는 첫 충전 때 약 1.8 V (Li 기준) 에서 금속 Ag 로 빠져나와 입계와 기공에 씨앗을 만들고, 더 낮은 전위에서 Li 와 합금한다 (Nat. Commun., 16, 5871 (2025)).*
- *같은 연구의 상평형 계산으로 보면 Li₆PS₅Cl 과 금속 Ag 가 함께 서는 전위는 약 1.7–1.9 V 뿐이라, 이 보고의 LPSCl | Ag(111) 점착 에너지는 첫 충전 전 계면의 값으로 쓴다.*
- *운전 중 (음극 약 0 V) 의 실제 계면은 고체전해질 | 분해 생성물 | Li–Ag 합금이다.*

---

## (f) 그림 · 동영상 크롭 요약

- **31 장** = 도구 27 (`Fig. 1`–`4` · `Fig. S1`–`S23`) + 손 4 (`Table S1`–`S3` · `Fig. S9` p.10). 동영상 없음. 도구가 낸 번호 공백 3 건 (`tS1`–`tS3` · '거의 백지 1.000') 은 캡션이 표 **아래**에 있는 SI 표였어요 — 표 벡터선 · 글자 범위로 손 크롭 · `manual_crop` 사유 · `missing_labels[].resolved`. 다시 자른 것 0. `--audit` 경고 없음.
- **본 것: 31/31** — 원해상도 18 장 (`Fig. 1`–`4` · `S3` · `S8` · `S9` + p.10 · `S15`–`S18` · `S21`–`S23` · `Table S1`–`S3`) · 2×2 대조표 13 장 (`S1` · `S2` · `S4`–`S7` · `S10`–`S14` · `S19` · `S20` · 타일 폭 980 px · 숫자는 원자료로). `Fig. 3f` 는 2 배 확대해 눈금으로 두께를 쟀어요.
- **그림 · 원자료가 본문과 어긋난 것**: `Fig. 3h` · `3i` (그림 · 원자료 모두 50 사이클 ≈187 mAh g⁻¹ = 91.5 % 쪽) 대 본문 95.0 % · `Fig. 2e` · `Fig. S11` · Note 1 의 석출 뒤 σ (≈100 배) · `Fig. 2d` 창 E_D 대 `Fig. 1e` E_hull · `Fig. 2b` 1.2 V 지점 46.9 (본문 ≈48.1) · `Fig. S8` x = 0 의 293 K ≈2.9 (figure-read) 대 `Fig. 1f` 2.0 · `Fig. S9` 반응식 1 줄 불균형 · '0.0.37' · 2.71 V 두 줄 · `Fig. 1b` 'Ag⁺ (48h)' 대 Methods '48a' · `Fig. S3` 정돈 구조 그림 대 DFT 모형 (S/Cl 섞임) · `Fig. S15d` Ag 도핑 곡선 = `Fig. 3a` 자료 재사용 · 복합 대조 58 사이클 CE 200 % (본문 언급 없음) · `Fig. S22` 골격 MSD ≈10 Å² = 표류 · `Fig. 4c` 띠틈 대 원자료 DOS 판독 (0.05–0.08 eV) · `Table S2` · `S14` 'mA cm⁻¹' · `Table S3` 'Ni' 대 SUS.
- **임시 파일 점검 (병렬 충돌 주의)**: 글자 · 스크립트 · 대조표 · 확대본 · Crossref 응답은 전부 `scratchpad/choi2025_silver_exsolution_argyrodite_anode_free/` 안에 `choi2025_` 접두 이름으로만 썼어요 (공용 이름 없음). 본문 글자 첫 줄 = 이 논문 (*Nat. Commun.* · "Silver exsolution …" · Choi) · SI 글자 첫 줄 = 이 SI · 네 inbox 파일 sha256 = `batch.json` 값과 일치 (`38da27a4…` · `d7601516…` · `6f9aeccf…` · `b72dfcc3…`). 대조표 그림 내용도 이 논문 것이었어요.

---

## (g) Jeff Sakamoto 저자 여부

**아니에요** — 저자는 Seung Ho Choi · Chang Hoon Baek · Jihoon Oh · Geung-Jong Lee · Minsoo Kim · Hyesu Lee · Dong-Joo Yoo · Yoon Seok Jung · KyungSu Kim · Ji-Sang Yu · Woosuk Cho · Haesun Park · Jang Wook Choi 13 명 (KETI · 연세대 · 서울대 · 중앙대 · 고려대) 이에요. 참고문헌에는 ref 20 Wang, Choudhury & Sakamoto, *Joule* 3, 2165 (2019) (= litdb `wang2019_li_se_interface_dynamics_stack_pressure_current_density`) 로만 나와요. INDEX 행에 `🏷 Jeff Sakamoto 공저` 를 달지 않아요. digest 머리 35 줄에는 그 이름도 부정문도 없고, 웹앱 `_paper_pis` = `['ysjung']` (정윤석 교수 · 저자 줄 'Yoon Seok Jung') 예요.
