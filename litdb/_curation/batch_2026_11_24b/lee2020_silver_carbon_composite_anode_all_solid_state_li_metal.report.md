# 끝 보고 — lee2020_silver_carbon_composite_anode_all_solid_state_li_metal (배치 2026-11-24b · #9)

- digest: `litdb/papers/lee2020_silver_carbon_composite_anode_all_solid_state_li_metal.md` (새 파일 · 512 줄 · 한국어 standalone · §0–§16 + §5b 동영상 · §16 인용 카드 답)
- 그림: `litdb/figures/lee2020_silver_carbon_composite_anode_all_solid_state_li_metal/` — 크롭 28 장 (본문 그림 6 · SI 그림 19 · SI 표 3). 도구 26 장 (`--pdf 본문 SI --clean`) + 손 크롭 2 장 (`Fig. 6` · `Fig. S10` — 도구가 번호 공백으로 보고) + 도구 크롭을 다시 자른 것 7 장. 그림 25 장 전부 Read 로 봤어요. 표 3 장은 PDF 글자층으로 읽었어요.
- 동영상: `video_frames/` 34 장 (3.0 MB · 폭 ≤ 1280 · JPG). 뽑은 명령은 digest §5b 에 있어요.
- 해시: inbox 다섯 파일 sha256 이 batch.json 9 번과 다 맞았어요.
- 공유 파일 · git 은 안 건드렸어요. `litdb/figures/_sources.json` 은 추출 도구가 이 slug 항목을 더해 다시 썼어요 (손 안 댐). 메인 세션 체크포인트 커밋 (`98271324` 등) 이 그림 폴더를 이미 지금 상태로 담고 있고, digest 는 미추적 상태예요.
- 점검 (읽기만): `build_index.py --check` → 이 digest 는 '어느 인덱스에도 없음 [dft]' + 'comparison_vs_ours 미편입' 만 걸려요 ((a) · (b) 를 넣으면 풀려요). `extract_figures.py --inbox --only lee2020_silver` (매칭표만) → 본문 + SI 자동 매칭 `[제목 72%]`. 웹앱: `/paper/<slug>` 200 · 그림 25 + 표 연결 · `paper_figures` 28 · `paper_figure_notes` 28 · `_paper_pis` = [] · 원소 API (Ag · Zr · Cu · Cl) 에 연결 · 기법은 `methods: Raman` 인데 용어 사전에 Raman 항목이 없어 기법 페이지에는 안 붙어요. 시험: `test_v3_markdown` + `test_v3_literature` 43 개 통과 · `test_webapp -k "sakamoto or litdb_figure or recent_digests or digest_date or element_papers or glossary_papers or figure_comment"` 7 통과 1 실패 = `test_recent_digests_are_on_every_litdb_surface` (INDEX · comparison 미편입 — 합치면 풀려요).
- 🎤 talk 역링크: 해당 없음 (`litdb/talks/*` 의 인입 대기열에 이 편이 없어요).

**메인이 먼저 알아야 할 것**
1. **WIP 의 온도 · 유지 시간 · 층 밀도 · 기공률은 이 논문에 없어요** (본문 · SI 전수). 있는 것은 490 MPa · 진공 밀봉 파우치 · 대기 중 가압 · 셀 두께 644.5 → 609.0 µm (`Table S2` · −5.5 % · 7 일 이완 없음) · 정성 SEM (`Fig. S10`) 뿐이에요. 장비 제품명은 'CIP' 계열로 적혀 있어요. 그래서 `minnmann2021_…` 의 "low single-digit porosity values" (2 차 인용) 는 이 논문으로 확인이 안 돼요.
2. **이 논문의 `Table S1` 은 SE 막 표가 아니에요** — SUS · Ag–C · Ag 층 · C 층 면저항 표예요. wishlist 572 줄의 'SI 표 S1' 은 `zhang2021_…` SI 의 문헌 막 비교표 (거기 Lee 2020 행이 있음) 를 가리켜요. 그 행 (99 wt% · 아크릴 · 혼합 용매 · 30 µm · 1.31 mS cm⁻¹) 은 원문과 맞아요.
3. **두 카드가 이 논문을 원문과 다르게 옮겼어요** (고치지 않았어요): `metzler2026_…` L195 '첫 효율 89 %' → 원문의 89 % 는 1,000 사이클 유지율이고 첫 사이클 CE 명시값은 없어요 · `spencerjolly2023_…` L34 '3.2 mA cm⁻²' → 원문 0.5 C = 3.4 mA cm⁻² · L42 'PVdF 비 Lee 2020 과 동일 (10 wt%)' → 원문은 마른 층 PVDF 비율을 안 적었어요 · L43 'Ag 5.7 vol% (Lee 2020 과 비슷)' → 원문 ≈8 vol% (기준 미기재).
4. **'>900 Wh/L' 과 '1,000 사이클' 은 다른 전지예요.** 0.6 Ah 2 면 셀 = 703 Wh L⁻¹ · 942 = 10 적층 5.87 Ah (0.05 C · 무가압 · 한 사이클) · 998 = 35 적층 계산값. 1,000 사이클은 0.6 Ah · 60 °C · 2 MPa · 0.5 C/0.5 C · 0.2 C 용량의 70 % 창이에요. ✎ 저장소 없는 무음극 셀이 CE 99.8 % 로 1,000 번 돌면 13.5 % 만 남아요 — 89 % 는 평균 CE ≈ 99.988 % 이거나 Li 저장소가 있다는 뜻이고, 원문은 이 산수를 안 해요.
5. **동영상 짝이 batch.json 추정 ('MOESM2–4 = Video 1–3') 과 달라요.** 장면으로 보면 MOESM2 = 가열 시험의 LIB (≈185 s 연기 → 234 s 부터 화면이 연기로 참) · MOESM3 = 가열 시험의 ASSB (584 s 내내 변화 없음) · MOESM5 = 절단 (Video 3) 이에요. 그래서 MOESM4 (안 받음) 는 소거법으로 기름 시험 (Video 2) 으로 보여요. SI 는 동영상을 셋이라 적었으니 Video 1 이 두 파일로 나뉜 것 같아요. 출판사 보충 자료 목록 (nature.com) 은 프록시가 막아서 못 열었어요 (다시 안 쳤어요).
6. **크롭 도구가 이 저널 판에서 세 가지를 놓쳤어요**: ① 본문 그림 다섯 장의 위쪽을 다 잘랐어요 — `Fig. 1` 은 a–d 패널 (y 58–330) 이 통째로 빠지고 아래 띠만 남았어요 (머리글 띠 아래 y 48 로 다시 자름) ② `Fig. 6` (p.8 · 벡터 8,088 path) 을 '영역 없음' 으로 버렸어요 ③ 쪽을 넘긴 캡션 (`Fig. S10` 그림 p.10 · 캡션 p.11) 을 못 짝지었어요. 그 밖에 `Fig. S11` 크롭에 `Table S2` 가 통째로, `Fig. S5` 에 본문 한 줄이 끼었어요. 사유는 `figures.json` 의 `manual_crop` · `recrop` (원래 bbox 는 `bbox_auto`) 에 있어요. 도구를 고칠지는 메인이 정해 주세요.
7. W_ad 보고서 쪽: 8-3 의 C | Cu 후보는 Cu 셀 (Metzler 2026) 기준인데, 이 원전 셀은 Cu 가 황화물과 반응해서 SUS 를 썼어요 (`Fig. S4a`) → C | SUS · Li | SUS 를 같이 두는 게 맞아 보여요 ((e) 문장 후보). INDEX 절 머리가 '18 편 한 묶음' 이라 이 배치를 넣으면 머리 문구도 고쳐야 해요.
8. wishlist 의 이 편 줄은 지시문의 13 · 390 줄이 아니라 지금 **195 · 203 · 572 줄**이에요 (밀려남). 셋 다 '카드 없음' 으로 남아 있어요.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 한 묶음)` — 행 순서상 **Ag/C 묶음 맨 앞** (`sandoval2025_electro_chemo_mechanics_anode_free_ssb` 행 다음 · `metzler2025_ag_particle_distribution_carbon_interlayer_anode_free` 행 앞). 이 편이 그 묶음의 원전이에요.

| `papers/lee2020_silver_carbon_composite_anode_all_solid_state_li_metal.md` **(본문 10 pp + SI 18 pp + 동영상 3 (MOESM2 · 3 · 5 · MOESM4 안 받음) · 크롭 28 장 (도구 26 + 손 크롭 2 `Fig. 6` · `Fig. S10` · 다시 자름 7 = `Fig. 1`–`5` 위쪽 · `Fig. S5` · `Fig. S11`) · 그림 25 장 전부 실독 · 영상 장면 34 장 · 2026-11-24)** | **[외부·exp·★★★ Ag–C 인터레이어 원전 · 무과잉 Li 황화물 파우치 · 계산 0]** ✅ Yong-Gun Lee/S. Fujiki/C. Jung/N. Suzuki/N. Yashiro/R. Omoda/D.-S. Ko/T. Shiratsuchi/T. Sugimoto/S. Ryu/J. H. Ku/T. Watanabe/Y. Park/**Y. Aihara\***/**D. Im\***/I. T. Han (기업 연구소 · 한국 · 일본), "**High-energy long-cycling all-solid-state lithium metal batteries enabled by silver–carbon composite anodes**" — ***Nat. Energy* 5, 299–308 (2020)**, DOI `10.1038/s41560-020-0575-z`. Ag NP (60 nm) : 카본블랙 (35 nm · 비정질) = 1 : 3 + PVDF · 5–10 µm (그림마다 ≈6–12) on SUS 10 µm ‖ Li₆PS₅Cl 30 µm 막 (아크릴 1 wt% · 1.31 mS cm⁻¹) ‖ LZO 5 nm NMC90 6.8 mAh cm⁻². 충전 → **Li 25 µm 가 SUS \| Ag–C 사이** (탄소만 층도 같은 자리 · 다공) · Ag 는 Li–Ag (Li₉Ag₄ 같은 상) → 일부가 Li 에 녹아 집전체 쪽으로 · 방전 뒤 안 돌아옴 · 100 사이클 뒤 아래쪽에 작게. 0.6 Ah 2 면 셀 · WIP 490 MPa (온도 · 유지 · 기공 **미기재**) · 운전 2 MPa · 60 °C · 0.5 C/0.5 C (3.4 mA cm⁻²) → 1,000 사이클 89 % · CE > 99.8 % 평균 · 703 Wh L⁻¹ (942 는 10 적층 5.87 Ah 0.05 C 무가압 · 998 계산). 기전 (핵생성 에너지 · Li 속 Ag 안정 · 탄소 이온 전도) 은 전부 추정. ⛔ W · 점착 · 핵생성 과전압 0 — 물성 4축 수치 진입 금지 · `Table S1` 은 면저항 표 · 'Ag 8 vol%' · 기공 · 탄소 200 GPa 를 DEM 입력으로 쓰지 않는다 | W_ad §7-1 Ag 행 · §8-3 (Li 자리 원전 · C\|SUS 후보) · §8-4 (압력 세 단계) · [혁주] LZO 코팅 선례 (계면 측정 0) · DEM A · I 축 · 이웃 `spencerjolly2023_ag_graphite_interlayer_operando_xrd` · `metzler2025_ag_particle_distribution_carbon_interlayer_anode_free` · `metzler2026_sputtered_ag_carbon_interlayers_anode_free` · `kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode` |

---

## (b) `comparison_vs_ours.md` · `comparison_vs_ours_DEM.md` 에 넣을 줄

### b-1. `comparison_vs_ours.md` `📑 Reference key` 표에 한 행 (4 칸: 약칭 | 논문 | digest/status | 유형) — `[Met26AgS]` 행 위 (원전이라 Ag–C 묶음 맨 앞)

| **[Lee20AgC]** ★★★ **Ag–C 인터레이어 원전 (무과잉 Li 황화물 파우치 · SEM/EDS · TEM/EELS · XRD)** · ⛔ **점착 · 핵생성 · 응력 미측정 → A–D 물성 4축 수치 진입 금지** · ⚠ 탄소 = 카본블랙 (비정질 · D50 35 nm) · 집전체 = SUS (Cu 는 황화물과 반응) | **Yong-Gun Lee**/…/**Y. Aihara\***/**D. Im\***/I. T. Han 2020 ***Nat. Energy* 5, 299** (DOI 10.1038/s41560-020-0575-z) — "High-energy long-cycling all-solid-state lithium metal batteries enabled by silver–carbon composite anodes" | ✅ `papers/lee2020_silver_carbon_composite_anode_all_solid_state_li_metal.md` — 판정은 §E 2 행 + `comparison_vs_ours_DEM.md` §I 블록 · A 축 한 줄 | 실험 전용 (단면 SEM/EDS · TEM/HAADF/EELS · SADP · XRD · Raman · X-ray CT · EIS · 계산 0) |

### b-2. `comparison_vs_ours.md` §E 표에 두 행 (4 칸: 주장 | 출처 | 우리 | 일치)

| **🆕 (2026-11-24) Ag–C 층 (Ag NP : 카본블랙 1 : 3 · 5–10 µm · SUS 위) 에서 Li 는 집전체 \| 층 사이에 25 µm 로 쌓이고, Ag 는 Li–Ag 합금 → 일부가 Li 속에 녹아 집전체 쪽으로 옮겨 방전 뒤에도 안 돌아온다 · 탄소만 층도 같은 자리 (다공 · 불균일) · Ag 만 층은 사라져 Li \| SE 직접 접촉** — 자리 · Ag 행방은 단면 SEM/EDS · TEM · XRD 로 봤고, 이유 (Ag 의 핵생성 에너지 저하 · Li 속 Ag 의 에너지 · 전하 전달 우세) 는 저자 추정 | [Lee20AgC] p.301–302 · `Fig. 3` · `Fig. 4` · `Fig. 5` · `Fig. S5` · `Fig. S6` | 우리 W 쌍 (W_ad 보고서 §2 · `db/properties/adhesion.json` · 값은 위치만) 은 LPSCl \| Ag(111) · Ag–C · LPSCl \| 흑연 · C–C — **운전 중 계면 (C \| SUS · Li(Ag) \| SUS · Li \| 카본블랙) 은 목록에 없다** · LPSCl \| Ag(111) 는 첫 충전 전만 대표 | — (정성 · 계면 목록 보완 · 맞출 표적 아님) |
| **🆕 (2026-11-24) 황화물 SE 와 Cu 집전체는 반응한다 (CV · 부식) → Ag–C 층 셀은 SUS 집전체 · Ag₂S 는 Ag–C \| Li 반쪽 셀에 2.0 V 평탄이 없어 '유의하지 않음'** | [Lee20AgC] SI p.4–5 · `Fig. S4` | W_ad 7-1 표 Cu 행 (Cu(111) · Li₂O) · LPSCl \| Ag(111) 는 반응 없는 날카로운 계면 가정 | Cu 행은 Cu 셀용 — **SUS (부동태 산화막) 행이 빠져 있다** · Ag₂S 배제는 간접 (XPS 없음) · 가정과 모순 없음 |

### b-3. `comparison_vs_ours_DEM.md` §I 블록 (지금 I-22 · 번호는 메인이 정해 주세요 — 병렬 편들이 I-23 이후를 쓸 수 있어요)

### I-xx. `lee2020_silver_carbon_composite_anode_all_solid_state_li_metal` — ★★★ Ag–C 층 원전: **Li 가 집전체 (SUS) \| Ag–C 사이에 쌓이고 Ag 는 Li 에 녹아 집전체 쪽으로 간다** — 위치는 탄소, 고르기는 Ag · 압력 세 단계 (제조 490 · 운전 2–4 · 무가압 0.1 C)

> **무엇을 주나.** Ag NP 60 nm : 카본블랙 35 nm (비정질) = 1 : 3 + PVDF · 5–10 µm on SUS 10 µm ‖ Li₆PS₅Cl 30 µm (아크릴 1 wt%) ‖ LZO 5 nm NMC90 6.8 mAh cm⁻² · 0.6 Ah 2 면 파우치 · WIP 490 MPa · 2 MPa · 60 °C (*Nat. Energy*, 5, 299 (2020)). 단면: 충전 = SUS / Li 25 µm (Ag 가 녹아 있음) / Ag–C / LPSCl · 방전 = SUS / Ag–C (Ag 가 아래쪽에 몰림) / LPSCl · 100 사이클 = 같은 자리 · Ag 작아짐. 대조: SUS 만 ≈19 사이클에 50 % (figure-read) · 탄소만 1 C/0.33 C 75 % (Ag 있으면 95–96 %) · 0.5 C 운전 불가 · Ag 만 0.33 C ≈72 mAh g⁻¹ (figure-read).
>
> **★ 우리 축에 닿는 곳.**
> ① **W 쌍 목록** — 운전 중 계면은 C \| SUS · Li(Ag ✎ ≈0.2–0.4 at%) \| SUS · Li \| 카본블랙 · LPSCl \| 카본블랙 (가장 오래 산다). LPSCl \| Ag(111) 는 첫 충전 전만. 집전체는 Cu 가 아니라 SUS (Cu 는 황화물과 반응 · `Fig. S4`).
> ② **I-20 (Metzler 2025) · I-21 (Metzler 2026) 과 같은 방향** — 이 논문이 원조 관찰이다. 탄소만 층도 같은 자리 (다공) 라서 '자리 = 탄소 · 치밀 = Ag' [카드 해석].
> ③ **DEM 압력** — 제조 490 MPa (등방 · 셀 두께 −5.5 %) · 운전 2–4 MPa (같은 성능) · > 4 MPa 단락 ↑ (자료 없음) · 0.1 C 무가압 — Li 항복 ≈0.8 MPa (`masias2019_…`) 보다 운전압이 높다.
>
> **⛔ 인용 금지 / 한정어**
> · W · 점착 · 핵생성 과전압 · 응력 수치 없음 — 맞출 표적이 아니다.
> · Ag vol% · 층 기공률 (✎ 질량으로 풀면 64–91 % · 세 숫자 불일치) · 탄소 탄성률 200 GPa (ref 45 · 다른 탄소) 를 DEM 입력으로 쓰지 않는다.
> · WIP 온도 · 유지 · 기공 = 원문에 없다.
> 상세: digest §3c · §3e · §3g · §3i · §6 · §7 · §10.

### b-4. (권장) `comparison_vs_ours_DEM.md` §A (압밀 / porosity) 에 한 줄

> 2026-11-24 추가 — `lee2020_silver_carbon_composite_anode_all_solid_state_li_metal` [Lee20AgC] — 0.6 Ah 2 면 파우치 **WIP 490 MPa** (온도 · 유지 · 매체 **미기재** · 장비 제품명 CIP 계열 · 진공 밀봉 파우치 · 대기 중) → 셀 두께 644.5 → 609.0 µm (−5.5 % · 3 · 7 일 무가압 이완 없음 · `Table S2`) · SE 막 ≈40 → 30 µm · Ag–C ≈9.6 → 7.9 µm (`Fig. S10b` 화소 잼) · **층 밀도 · 기공 숫자 0** (`Fig. S10` 정성 · 패널 c 눈금 없음) → '한 자릿수 기공' 의 근거로 쓰지 않는다 · 운전 2 MPa (2–4 같음 · > 4 단락 ↑ 서술만).

---

## (c) `pdf_map.tsv`

**필요 없어요** — `extract_figures.py --inbox --only lee2020_silver` (매칭표만) 가 본문 + SI 둘을 자동으로 붙였어요 (`[제목 72%]`). 굳히고 싶으면 한 줄:

```
lee2020_silver_carbon_composite_anode_all_solid_state_li_metal	lee2020_ag_c_composite_anode
```

---

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저)

발견 검색: Crossref REST 주제어 검색 4 번 (제목 없이 · 2024-11 이후 · 'silver carbon composite anode all-solid-state' · 'Ag-C interlayer anode-free sulfide stack pressure' · 'warm isostatic pressing sulfide' · 'silver migration current collector anode-free') + 확인 2 번 (Ito 2014 DOI · Hayashi works 레코드). 일반 클라이언트 이름 · 개인정보 없음. 대조: `litdb/papers/` grep (DOI · 쪽) + `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md`.

| # | 논문 (저자 · 저널 권, 첫쪽 (연도)) | 왜 (이 논문의 빈칸) | litdb | 목록 |
|---|---|---|---|---|
| 1 | Hayashi K., Mori T., Beamer C., Ito H. · *ACS Omega* 11, 1945 (2026 · 온라인 2025-12-24) — "Effect of Process Duration on Electrochemical Performance in Composite Cathodes for All-Solid-State Li-Ion Batteries Processed via Warm Isostatic Pressing" · DOI 10.1021/acsomega.5c10291 | **WIP 유지 시간** — Lee 2020 에 없는 칸 · 같은 저자 `hayashi2025_…` (WIP 온도) 의 후속 | 없음 | 없음 · Crossref 확인 |
| 2 | Song Y., Hong J., Kim H., Ko K., Lee J., Lee S.-M., Jo C., Park S. · *Adv. Energy Mater.* 16, e71461 (2026) — "Chemomechanically Adaptive MXene–Si–Ag Dual-Seed Interlayer Enabling Low-Pressure Sulfide all-Solid-State Batteries" · DOI 10.1002/aenm.71461 | Ag 씨앗 층을 저압 황화물 셀로 — 운전압 2 MPa 이하로 내려가는 쪽 (W_ad 7 · 8-4) | 없음 | 없음 · Crossref 검색 메타 |
| 3 | Liu Y., Lu Y., Clemens O. · *Electrochim. Acta* 574, 149375 (2026) — "Effect of carbon interlayer preconditioning on in-situ plated lithium metal stability in anode-free solid-state batteries" · DOI 10.1016/j.electacta.2026.149375 | **탄소만 층** (Lee Note S1 의 '다공 · 불균일 계면') 을 전처리로 고칠 수 있나 — 위치 = 탄소 · 치밀 = Ag 의 검증 | 없음 | 없음 · Crossref 검색 메타 |
| 4 | Packard J. S., Dai W., Kang J. H. … Lin Y. · *ACS Appl. Energy Mater.* (2026) — "Dry Compressible Anode Interlayer Design Enabling All-Solid-State Batteries at Low Stack Pressure" · DOI 10.1021/acsaem.5c02931 | 압축성 건식 음극 층 · 저압 — Ag–C 층의 역학 쪽 대조 (권 · 쪽 미확인) | 없음 | **목록에 있음** ('그 밖' 검색 줄) |
| 5 | Thorpe M. A., Zhang M., Liao D. W., Sandoval S. E., Kim Y., McDowell M. T., Thouless M. D., Dasgupta N. P. · *Matter* 8, 101955 (2025) — "Controlling stack pressure inhomogeneity in anode-free solid-state batteries using elastomeric interlayers" · DOI 10.1016/j.matt.2024.101955 | 지그 2 MPa 가 실제로 고르게 걸리나 · '> 4 MPa 단락' 의 압력 분포 쪽 설명 — DEM 압력 경계조건 | 없음 | 없음 · Crossref 검색 메타 |
| 6 | Lee Young-Geun, Whitacre J. F. · *J. Electrochem. Soc.* 172, 110537 (2025) — "Intimate Interfacial Contact Between the Electrode and Sulfide-based Solid Electrolytes by Hot-Pressing for High-Performance All-Solid-State Batteries" · DOI 10.1149/1945-7111/ae16da | WIP '온간' 의 **온도** 축 대조 (열간 압착 접촉) · ⚠ 1 저자는 이 논문 1 저자와 다른 사람 | 없음 | 없음 · Crossref 검색 메타 |
| 7 | Park, Naik, Vishnugopi, Mukherjee, Hatzell · *Adv. Energy Mater.* 15, 2405129 (2025) — "Lithium Kinetics in Ag–C Porous Interlayer in Reservoir-Free Solid-State Batteries" · DOI 10.1002/aenm.202405129 | Ag–C 다공 층 안 Li 수송 · 기공률 기준값 — Lee 의 기공 미기재 칸 | 없음 (인용만: `kang2026_…` · `metzler2026_…` · `zhang2026_…`) | **목록에 있음 (표 1 #9)** |
| 8 | Ito S., Fujiki S., Yamada T., Aihara Y., Park Y., Kim T. Y., Baek S.-W., Lee J.-M., Doo S., Machida N. · *J. Power Sources* 248, 943 (2014) — "A rocking chair type all-solid-state lithium ion battery adopting Li₂O–ZrO₂ coated LiNi₀.₈Co₀.₁₅Al₀.₀₅O₂ and a sulfide based electrolyte" · DOI 10.1016/j.jpowsour.2013.10.005 | **Lee 2020 LZO 코팅의 원전** (ref 40) — [혁주] LZO 코팅 NCA \| 황화물 트랙의 직접 선례 (코팅 조성 · 결정성이 거기 있을 수 있음) | 없음 (인용만: `hippauf2019_…` · `nam2018_…` · `zhang2021_…` — zhang2021 SI 표는 'Fujiki 2014' 로 적음) | 없음 · Crossref 확인 |

- 같은 배치 8 번 Ko 2025 *Nat. Commun.* 16, 1066 · 11 번 Xie 2024 *Adv. Energy Mater.* 14, 2302960 은 병렬이라 서지로만 적었어요 (digest 머리 계보).
- 논문이 아닌 원전: Ag–C 층 특허 US20190157723A1 (ref 49) · 금속 기판 위 카본블랙 학회 초록 (ref 50 · ECS 235th 2019 abstr. 163) — 층 조성 · 두께의 원 출처라 필요하면 따로.

---

## (e) DEM-DFT 보고서 (W_ad 보고서) 에 쓸 거리

`docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` 7 절 (7-1 Ag 행) · 8-3 · 8-4 를 먼저 읽고 맞췄어요. '봄' = 그 그림을 Read 로 직접 봤어요 · '글' = PDF 글자층으로만.

### e-1. Ag–C 층 (7-1 Ag 행 · 8-3)

| 물음 | 답 | 쪽 · 그림 · 표 | 봤나 |
|---|---|---|---|
| Ag 입자 · 탄소 | Ag NP D50 60 nm (TEM ≈60 nm · 서로 떨어져 망 없음) · 카본블랙 D50 35 nm · SADP 확산 고리 · XRD 넓은 봉우리 ≈25° · ≈43.5° → 비정질 · 난층 · 등급 · BET · Raman I_D/I_G · O/N 미기재 | p.302 · p.307 · `Fig. 5a–c` · `Fig. S8` | 봄 |
| Ag : C · 바인더 | 1 : 3 (질량) · Ag ≈8 vol% (기준 미기재) · Ag 8–16 mg Ah⁻¹ · PVDF ('PVDF 7 wt% 를 담은 NMP' · 마른 층 비율 미기재) · ✎ 세 숫자와 두께가 한 조합으로 안 맞음 (§10-⑤) | p.301 · p.307 | 글 |
| 두께 · 만든 법 | Methods 5–10 µm (그림마다 ≈6–12 µm · `Fig. 3` 화소 ≈9–12 · `Fig. S10b` 화소 ≈9.6 → 7.9) · NMP 슬러리 → 10 µm SUS 에 스크린 인쇄 → 공기 80 °C 20 min → 진공 100 °C 12 h | p.307 · `Fig. 1b` · `Fig. 3` · `Fig. 4i` · `Fig. S10` | 봄 |
| 사이클 뒤 Li 는 어디 | **집전체 (SUS) 와 Ag–C 층 사이**에 조밀한 층 (첫 충전 25 µm · 3.6 / 4.0 / 4.25 V 에서 6 / 20 / 25 µm · 100 사이클 뒤 0.5 C 충전 ≈22 µm figure-read) · 방전하면 완전히 사라짐 · 근거 = 단면 SEM 대비 + C-EDS 띠 위치 (Li 자체는 EDS 로 안 보임) · 탄소만 층도 같은 자리 (다공 · 불균일) | p.301–302 · `Fig. 3c,d` · `Fig. 4h–j` · `Fig. S5` · `Fig. S6b` | 봄 |
| Ag 는 어디로 | 충전: Ag–Li 합금 (XRD Li₉Ag₄ 같은 봉우리 23 · 27 · 28.3° · SADP 비정질화) → 일부가 Li 층 안으로 (EDS) · 방전: 층으로 안 돌아오고 층 아래쪽 (SUS 쪽) 에 남음 · 100 사이클: 아래쪽에 띠 · 입자 작아짐 · ✎ Li 속에 다 녹으면 ≈0.2–0.4 at% | p.301–302 · `Fig. 3c–f` · `Fig. 5d–n` | 봄 |
| 기전의 지위 | '핵생성 에너지를 낮춘다' = speculated · '합금 → 이동 → 고용' 순서 = assume · 'Li 속 Ag 가 에너지상 유리' = believed · '탄소는 이온 전도체' = presumed · '자리는 전하 전달이 정한다' = suspect — **전부 측정 없음** | p.301–302 · SI p.6 | 글 |
| 집전체 | Cu 는 황화물과 반응 (CV · 사진 부식) → **SUS** · Ag₂S 는 반쪽 셀 2.0 V 평탄 없음으로 배제 | SI p.4–5 · `Fig. S4` | 봄 |

### e-2. 셀 조건 (8-4 · [혁주])

| 항목 | 값 | 쪽 · 그림 · 표 | 봤나 |
|---|---|---|---|
| SE | Li₆PS₅Cl (상용 · 3 µm 입자) 99 wt% + 아크릴계 바인더 1 wt% · 자일렌 + 이소부티르산 이소부틸 · 닥터블레이드 ≈40 µm → 셀 안 30 µm · 양극 위 50 MPa 전사 · σ 1.8 (결정 분말 펠릿) · 1.31 mS cm⁻¹ (바인더 섞은 SE · 시료 형태 미기재) · Ea 0.35 eV | p.300–301 · p.307 · `Fig. 1c,d` · `Fig. S2` · `Fig. S3` | 봄 |
| 양극 | NMC90 · 복합 85 : 15 : 3 : 1.5 (NMC : SE < 1 µm : CNF : PTFE) · 건식 필름 · ≈100 µm · 6.8 mAh cm⁻² (✎ ≈31.6 mg cm⁻²) | p.306–307 · `Table S3` | 글 |
| **LZO 코팅 ([혁주])** | **Li₂O–ZrO₂ · 5 nm** (TEM 한 입자) · 졸–겔: 무수 2-프로판올 : 리튬 메톡사이드 (메탄올 중 10 %) : Zr(IV) 테트라프로폭사이드 = **200 : 20 : 1 (몰)** · NMC 분산 1 h → 50 °C 진공 증발 (초음파) → 여과 → **공기 300 °C 1 h** · 코팅의 Li : Zr · 결정성 · 함량 **미기재** · LZO \| SE 계면 측정 **0** · CE > 99.8 % 를 LZO 덕으로 돌림 (대조 없음) · 우리 랩 `kang2025_toughened_bimodal_nca_lzo` 는 6–8 nm 비정질 | p.301 · p.304 · p.306 · `Fig. 1e` | 봄 (`Fig. 1e`) · 글 (조건) |
| 적층압 · 제조압 | 운전 2 MPa (지그 · 2–4 MPa 성능 같음 · > 4 MPa 단락 ↑ 서술만) · 제조 WIP 490 MPa (온도 · 유지 미기재) · 0.1 C 무가압 가능 (한 사이클) | p.303 · p.306 · SI p.10 · `Fig. 6c` · `Fig. S11` · `Fig. S12` · `Table S2` | 봄 |
| 온도 · 전류 | 60 °C (대부분) · 화성 0.1 C CC–CV (0.05 C 까지) / 0.2 C · 수명 CC 0.5 C/0.5 C = 3.4 mA cm⁻² · 2.5–4.25 V (1 C = 6.8 mA cm⁻²) | p.307 · `Fig. 6` 캡션 | 봄 |
| N/P | 원문에 없음 · ✎ 층의 Li 수용 (석출 전) 0.5–0.64 mAh cm⁻² ÷ 6.8 ≈ 0.07–0.09 · 과잉 Li 0 | `Fig. 4a` (그림 안 표지) | 봄 |
| 에너지 밀도 근거 | `Table S3`: 215 mAh g⁻¹ · 86 % · 양극 95–105 µm × 2 · SE 30 · **'석출 Li 30 µm'** · Al 12 · SUS 10 · 57 cm² · 포장 120 × 2 · 절연 40 × (적층 − 1) → 703 / 942 / 998 Wh L⁻¹ (1 / 10 / 35 적층) · 충전 두께 · 지그 · 탭 제외 · ✎ 1,000 사이클 시험의 실제 ≈480 Wh L⁻¹ | SI p.16 · `Fig. S17` · `Fig. S18` | 봄 (그림) · 글 (표) |

### e-3. 기전 · Ag 없는 대조 (숫자)

| 대조 | 숫자 | 근거 | 봤나 |
|---|---|---|---|
| 층 없음 (SUS 만) | 0.1 C/0.33 C · 60 °C · 20 mAh: ≈14 사이클 80 % · ≈19 사이클 50 % · 50 사이클 ≈7 % (figure-read) · 0.05 C 석출 Li 섬 · 30 µm 다공 | `Fig. 2` | 봄 |
| 탄소만 (Ag 0) | 1 C/0.33 C **75 %** 대 Ag 있는 조성 95–96 % (1 : 3 ≈95 % figure-read) · **0.5 C/0.5 C 운전 불가 · 쉽게 단락** (곡선 없음) · 첫 사이클 0.1 / 0.33 / 1.0 C ≈ 201 / 196 / 181 mAh g⁻¹ (figure-read — 이 그림만 보면 ≈0.92 · 75 % 와 엇갈림) · Li 는 집전체 쪽 (다공) | SI p.6 · p.12 · `Fig. S6a,b` · `Fig. S13a` | 봄 |
| Ag 만 (3 µm) | 방전 0.1 / 0.33 / 1.0 C ≈ 193 / 72 / 5 mAh g⁻¹ (figure-read) · 층이 사라져 Li \| SE 직접 접촉 | SI p.6 · `Fig. S6c,d` | 봄 |
| 조성 | 1 : 1 → CE < 95 % · 단락 · ≈37 사이클에서 끝 · 1 : 2 → ≈243 사이클 ≈89 % · 1 : 3 → 300 사이클 ≈92.5 % (figure-read · 20 mAh · 0.5 C/0.5 C) | SI p.12 · `Fig. S13` | 봄 |
| 압력 의존 | 2 / 3 / 4 MPa: 1 C/0.33 C ≈94.2 / 95.2 / 95.5 % · 300 사이클 ≈94 % 겹침 (figure-read) · > 4 MPa 자료 없음 · 무가압 0.1 C 한 사이클 (충전 ≈236 · 방전 ≈217 mAh g⁻¹) | SI p.10 · `Fig. S11` · `Fig. S12` | 봄 |
| 읽어 낸 것 | **자리 = 탄소 · 고르기 = Ag** [카드 해석] — W 로 친Li 성 순위만 매겨 Li 자리를 예측하지 않는다 (8-3 의 Metzler 2025 결론과 같은 방향) | digest §6 | — |

### e-4. 안전 시험 영상 (짧게)

| 영상 (짝) | 셀 · 조건 | 보인 것 | 봤나 |
|---|---|---|---|
| MOESM2 = 가열 시험 LIB 쪽 | 시판 폴리머 LIB ≈1.4 Ah · 4.25 V · 상온 → 210 °C (5 °C min⁻¹) | ≈185 s 흰 연기 → 229–233 s 분출 → 234 s 부터 화면이 연기로 참 (불꽃 색 안 보임) | 봄 (5 s 간격 48 장 + 끝 11 초 1 s 간격) |
| MOESM3 = 가열 시험 ASSB 쪽 | ASSB 시제품 ≈1.2 Ah · 4.25 V · 210 °C 1 h 유지 | 584 s 내내 변화 없음 · `Fig. S19` 로 보면 **210 °C 는 히터 온도 · 셀 온도는 ≈160–172 °C (Li 녹는점 180.5 °C 아래)** | 봄 (5 s 간격 117 장) |
| MOESM4 (안 받음) | 0.6 Ah · SOC 50 % · 150 °C 기름 > 5 min (SI) | 부풂 없음 (SI 서술) | 안 봄 |
| MOESM5 = 절단 (Video 3) | 0.6 Ah · SOC 50 % (3.82 V) · LED · 금속 가위 · 건조실 | 가위가 닫힐 때마다 LED 가 0.1–0.3 s **꺼졌다가** (≈0.8 · 2.1 · 3.4 s · 손으로 찢을 때 ≈8.4 s) 다시 켜짐 — SI 는 'weak LED lighting' | 봄 (0.5 s 간격 21 장 + 전 프레임 LED 밝기) |

### e-5. 보고서 문장 후보 (랩 인용 꼴 · 회사 이름 없음)

- **8-3 첫 문단 앞 (원전)**: "Ag 나노입자와 카본블랙을 1 : 3 (질량) 으로 섞은 5–10 µm 층을 스테인리스 집전체 위에 둔 황화물 전지에서, 충전하면 Li 가 집전체와 Ag–C 층 사이에 약 25 µm 의 조밀한 층으로 쌓였고 Ag 는 그 Li 속에 녹아 집전체 쪽으로 옮겨 갔다. 방전 뒤 Ag 는 층으로 돌아오지 않았고 100 사이클 뒤에는 집전체 가까이에 작은 입자로 모였다 (Nat. Energy, 5, 299 (2020))."
- **8-3 '자리' 문단**: "탄소만 쓴 층에서도 Li 는 집전체 쪽에 쌓였지만 계면이 고르지 않고 다공질이었다. Ag 만 쓴 층은 Li 를 고르게 쌓았지만 층이 사라져 Li 가 고체전해질에 직접 닿았다 (Nat. Energy, 5, 299 (2020)). 이 논문은 Li 가 그 자리에 쌓이는 이유를 재지 않았다."
- **7-1 Cu 행 · 8-3 후보 목록**: "황화물 고체전해질은 Cu 와 반응해서 이 전지는 스테인리스 집전체를 썼다 (Nat. Energy, 5, 299 (2020)). 그런 전지라면 C\|SUS · Li\|SUS 도 W 를 낼 계면 후보다 — 스테인리스는 부동태 산화막 표면으로 모형화해야 한다."
- **7-1 Ag 행 '같이 볼 것'**: "운전 중 Ag 는 Li 속 묽은 고용체가 되어 집전체 쪽에 모인다 — Ag(111)\|Li 는 첫 충전 전의 계면이다 (Nat. Energy, 5, 299 (2020))."
- **8-4 '압력 세 단계' 문단 뒤**: "한 전지가 세 단계를 다 보였다. 조립 때 등방압 490 MPa, 운전 중 2 MPa (2–4 MPa 에서 성능 차이 없음 · 4 MPa 를 넘으면 단락이 잦아졌다고 적었다), 0.1 C 에서는 무가압 운전 (Nat. Energy, 5, 299 (2020)). 등방압의 온도 · 유지 시간 · 층 기공률은 적혀 있지 않다."
- **8-7 표 한 행**: `Nat. Energy, 5, 299 (2020) | Ag–C 층 (Ag : 카본블랙 1 : 3) \| LPSCl · 무과잉 Li 파우치 · 단면 SEM/EDS · TEM/EELS · XRD | 8-3 Li 자리 · Ag 이동 · 집전체 · 8-4 압력 세 단계`

### e-6. 인용 카드에 돌려줄 답 (남의 카드는 고치지 않았어요)

| 카드 · 줄 | 물음 | 답 | 쪽 |
|---|---|---|---|
| `dixit2022_isostatic_pressing_ssb_large_scale_manufacturing_review` §12 [69] · §3-4 문헌표 행 50 · wishlist 195 | WIP 490 MPa 의 온도 · 유지 · WIP 뒤 기공 | 490 MPa 만 · 온도 · 유지 · 매체 · 기공 없음 · 셀 두께 644.5 → 609.0 µm (−5.5 %) · 7 일 이완 없음 · SEM 정성 · 진공 밀봉 파우치 · 대기 중 가압 → 표 행 50 의 빈칸은 원문도 빈칸 | p.303 · p.307 · SI p.10–11 |
| `hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode` [13] · wishlist 203 | "over 900 Whl⁻¹ by using WIP" · WIP 조건 · 기공 | 900 Wh L⁻¹ 은 10 적층 5.87 Ah 셀 (942 · 0.05 C · 무가압) · 0.6 Ah 셀은 703 · WIP 효과는 정성 · 조건 · 기공 숫자 없음 | p.304 · SI p.10 · `Table S3` |
| `minnmann2021_jes_charge_transport_bottlenecks` [59] (p.9) | "low single-digit porosity values" 근거 | 이 논문에 기공률 숫자가 없다 — 확인 안 됨 | 본문 · SI 전수 |
| `zhang2021_dry_ptfe_calendered_30um_sulfide_se_membrane` [12] / SI [15] · §3-6 · wishlist 572 | 30 µm 습식 막의 바인더 · 함량 · 전도도 | zhang2021 표 행 (99 wt% · 아크릴계 · 혼합 용매 · 30 µm · 1.31 mS cm⁻¹) 은 원문과 맞다 · 30 µm 는 셀 안 가압 뒤 (막 ≈40 µm) · 1.31 은 '바인더 섞은 SE' · 시료 형태 미기재 · 결정 분말 1.8 · Ea 0.35 eV · 막은 양극 위 50 MPa 전사 · 이 논문 자기 `Table S1` 은 면저항 표 · ASR 2.29 Ω cm² 는 zhang2021 쪽 산수 (✎ 맞음) | p.300–301 · p.307 · SI p.7 |
| `spencerjolly2023_ag_graphite_interlayer_operando_xrd` L34 · L42–43 | 3.2 mA cm⁻² · PVdF 비 동일 · Ag 5.7 vol% | 원문 0.5 C = 3.4 mA cm⁻² · 1,000 사이클 89 % · 마른 층 PVDF 비율 원문에 없음 · 원문 Ag ≈8 vol% (기준 미기재 · ✎ 고체 기준 ≈5–6) | p.304 · p.307 |
| `metzler2026_sputtered_ag_carbon_interlayers_anode_free` L195 | "Lee 2020 의 첫 효율 89 %" | 원문에 첫 사이클 효율 89 % 는 없다 — 89 % 는 1,000 사이클 유지율 · 첫 사이클 CE 명시값 없음 (figure-read ≈91–92 % — `Fig. S4d` · `S7` · `S12` · `Fig. 6d`) · 0.2 C 215 mAh g⁻¹ 는 원문 값 | p.303–304 |
| `sandoval2025_electro_chemo_mechanics_anode_free_ssb` [30] | 압착 · 1,000 사이클 · CE · 탄소 유지 | 제조 490 MPa (등방) · 운전 2 MPa · 1,000 사이클 89 % · CE > 99.8 % 평균 · 탄소층은 충 · 방전 내내 SE 쪽에 남음 (100 사이클 두께 변화 무시할 만) | p.301 · p.303–304 |
| `cronau2022_wet_milling_particle_size_ionic_conductivity` [4] | "> 20 µm 분리막 부적합" · "평균 < 1 µm 필요" | 30 µm SE 막 (3 µm 입자) 을 썼고 '20 µm 초과 부적합' 문장은 없다 · '< 1 µm' 는 복합 양극 속 SE | p.300 · p.306 · p.307 |
| `kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode` [19] · `lee2022_thin_insitu_li_void_rewetting_llzo` [41] | '카드 없음' | 이제 카드 있음 | — |
| 물음 ③ ≈1,000 사이클 셀 조건 | — | 0.6 Ah 2 면 파우치 · LZO 5 nm NMC90 6.8 mAh cm⁻² · SE 30 µm (아크릴 1 wt%) · Ag–C 5–10 µm on SUS 10 µm · WIP 490 MPa · 지그 2 MPa · **60 °C** · CC 0.5 C/0.5 C (3.4 mA cm⁻²) · 2.5–4.25 V · 첫 0.5 C 방전 146 mAh g⁻¹ (0.2 C 의 70 %) · 600 사이클 95 % · 1,000 사이클 89 % · CE > 99.8 % 평균 · 셀 1 개 (n 미기재) | p.303–304 · p.306–307 · `Fig. 6g` · `Fig. S16` |

---

## (f) 그림 · 동영상 크롭 요약

- **크롭 28 장** = 본문 그림 6 (`Fig. 1`–`Fig. 6`) · SI 그림 19 (`Fig. S1`–`S19`) · SI 표 3 (`Table S1`–`S3`). 본문에는 표가 없어요.
- **도구** (`extract_figures.py --slug … --pdf 본문 SI --clean`) 26 장 · 번호 공백 2 (`f6` · `fS10`) → **손 크롭 2**: `Fig. 6` (p.8 · y 47–463 · 머리글 띠 아래 ~ 'Cycle number' 아래) · `Fig. S10` (SI p.10 아래 박힌 래스터 + 6 pt · 캡션은 p.11 맨 위). 둘 다 `missing_labels[].resolved` 를 달았어요.
- **다시 자름 7**: `Fig. 1` (a–d 패널이 통째로 빠져 있었음) · `Fig. 2`–`Fig. 5` (위쪽 패널 라벨 · 래스터 윗단 · `Fig. 4` 의 4.3 V 눈금이 잘림) — 넷 다 위쪽을 y 48 로 · `Fig. S5` (본문 한 줄 끼임) · `Fig. S11` (위에 `Table S2` 통째로 끼임 → 래스터 bbox + 6 pt).
- **캡션 고침 3**: `Fig. 1` (900 자에서 잘림 → PDF 글자로 끝까지) · `Fig. S15` ('25 oC' → '25 °C') · `Fig. S18` (줄바꿈 하이픈). 원문은 `caption_raw` 에 남겼어요.
- **figures.json 에 단 것**: 전 항목 `viewed` / `viewed_how` (그림 25 = 봄 · 표 3 = 글자층) · `manual_crop` · `recrop` · `bbox_auto` · `caption_raw` · `caption_fix` · `video_frames` (폴더 · 장수 · digest §5b 안내).
- **본 그림**: 25 장 전부. 화소로 잰 것 둘 (`Fig. 3` C-EDS 띠 · `Fig. S10` Ag–C 띠). 그림이 본문과 어긋난 곳: `Fig. 3` Ag–C 두께 (본문 5 µm 대 ≈9–12) · `Fig. 4f,g` ('변화 없음' 대 매끈해진 면) · `Fig. 5i,l` (남는 Li 미언급) · `Fig. 5n` 안쪽 'Ag–C alloy' · `Fig. 6e` 안쪽 축 단위 · `Fig. 6g` CE 흩어짐 미언급 · `Fig. S6a` 대 Note S3 75 % · `Fig. S17` 이 `Table S3` 보다 ≈2 % 낮음 · `Fig. S19` 셀 온도 ≈165 °C.
- **동영상 장면 34 장** (`video_frames/` · 3.0 MB · 폭 ≤ 1280 · JPG): MOESM2 타일 3 + 핵심 3 · MOESM3 타일 3 + 핵심 2 · MOESM5 0.5 s 간격 21 장 + 타일 1 + LED 확인 1. figures.json 밖이라 뽑은 명령을 digest §5b 에 남겼어요.

---

## (g) Jeff Sakamoto 저자 여부

**저자가 아니에요.** PDF 머리말의 저자 16 명을 대조했어요. 이름은 참고문헌 20 (Masias, Felten, Garcia-Mendez, Wolfenstine, Sakamoto · *J. Mater. Sci.* 54, 2585 (2019) = litdb `masias2019_li_metal_elastic_plastic_creep_properties`) 에만 나와요. digest 머리 35 줄에는 PI 이름 · 부정 저자문을 안 넣었고, 웹앱 `_paper_pis(slug)` = [] 를 확인했어요. INDEX 행에 🏷 는 안 달아요.
