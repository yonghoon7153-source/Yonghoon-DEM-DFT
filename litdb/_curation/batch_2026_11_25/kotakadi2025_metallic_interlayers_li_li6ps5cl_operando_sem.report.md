# 끝 보고 — kotakadi2025_metallic_interlayers_li_li6ps5cl_operando_sem (2026-11-25 · litdb-curator · 배치 2026-11-25 #1)

쓴 파일은 셋이에요.
- digest `litdb/papers/kotakadi2025_metallic_interlayers_li_li6ps5cl_operando_sem.md` (561 줄 · 표 17 개 · 칸 수 어긋난 줄 0 · 목록 앞뒤 빈 줄 넣음 · Python-Markdown 으로 렌더해 표 17 · 문단 속 깨진 표 0 확인)
- 그림 `litdb/figures/kotakadi2025_metallic_interlayers_li_li6ps5cl_operando_sem/` (크롭 29 장 = 그림 23 + 표 6 · figures.json)
- 이 보고 파일

공유 파일 · git 은 안 건드렸어요. ⚠ 단 하나 — 지시대로 돌린 추출 도구가 `litdb/figures/_sources.json` 에 이 slug 항목 (8 줄) 을 **자동으로** 넣었어요 (점검 시점 `git diff` 에는 이 항목만 더해져 있었어요). 같은 배치의 다른 두 에이전트도 같은 도구를 돌리니까, 합칠 때 세 slug 항목이 다 남았는지 한 번 봐 주세요 (동시에 쓰면 한쪽이 덮일 수 있어요).

## 핵심 세 줄
1. **우리 계 그대로** — 상용 Li₆PS₅Cl 위 Bi · In · Ag · Mg 100 nm. Bi 는 LiBi → Li₃Bi (+61 %) 에서 들려 깨지고 Li 가 층 **밑**에서 기둥으로 자라 첫 사이클 뒤 단락 · In · Ag · Mg 는 멀쩡하고 Li 가 층 **위**에 고르게 방울로 (0 MPa operando SEM · 셀 하나씩).
2. **SE 위에 증착하면 CC 위보다 CPE Q 35 배** (= 접촉 면적 35 배로 읽음 · Brug 식으로는 ≈75 배 · 우리 산수) — 전류는 고르게 퍼지지만 전자 전도 층이 SEI 를 키운다 (CTTA 180 h ≈0.09 대 층 없음 ≈0.034 mAh cm⁻² · 접촉 35 배에 SEI 1.4 배).
3. **저자의 'Mg 가 부동태 SEI 로 손실을 줄인다' 는 약해요** — `Fig. S9` 원자료에서 Mg 가 모든 시각에 가장 많이 · 가장 빨리 Li 를 잃고, `Table S3` 를 빼서는 `Fig. 6B` 가 재현이 안 돼요 (Mg 늦은 기울기 3 배 차). XPS 의 'MgS 유지' 도 위치 차 0.2 eV 이고 Mg 시료엔 리튬화 뒤 Li 1s 가 안 늘었어요 (Data S1).

## 확인한 것
- inbox 5 파일 sha256 = batch.json (전부 일치).
- 추출: 29 장 (본문 그림 6 · 표 1 · SI 그림 17 · 표 5) · `missing_labels` [] · auto_fallback 없음 · 손 크롭 0. `--inbox --only kotakadi --dry` → 본문 · SI 가 **제목 100 %** 로 자동 짝 (pdf_map 줄 필요 없어요).
- `extract_figures --audit` 는 300 s 제한에 걸려 못 끝났어요 (전체 그림 폴더를 훑어서). 대신 이 slug 의 figures.json 을 직접 봤어요 — blank ≥ 0.965 인 다섯 (`S1` Nyquist · `S3`–`S6` 상평형도) 은 선 그림이라 백지가 아니에요 (축소 시트로 눈으로 확인).
- 그림: 23 장 **전부** 봤어요 — 원해상도 16 장 (본문 6 전부 + SI S2 · S7 · S8 · S9 · S10 · S11 · S12 · S15 · S16 · S17) + 축소 접촉 시트로 7 장 (S1 · S3–S6 · S13 · S14 — 내용 확인만 · 숫자는 안 읽음). 표 6 장은 PDF 글자층으로 읽었어요. 숫자는 `Fig. 5A` · `Fig. 6A,B` · `Fig. S9` 곡선을 색으로 픽셀 판독 · `Fig. S2` 눈금 · `Fig. 3` / `Fig. 4` 축척 막대를 픽셀로 쟀어요.
- **본문 서술과 어긋난 그림**: `Fig. 3C` (Ag 평탄 ≈0.055 · ≈0.015 V ↔ 본문 0.56 · 0.2 V) · `Fig. S16f` (첫 CE 층 없음 ≈95 % 최고 ↔ 본문 'Ag · Mg 가 CE 향상') · `Fig. 6E,F` ('30 min' ↔ Data S1 · `Fig. S10` · `S11` 40 · 50 min) · `Fig. 6F` (Ag 'S-Metal' ↔ `Fig. S11` · Data S1 'li2s' · 같은 160.0 eV) · `Fig. S7c` (In ≈0.6 V 평탄 ↔ `Fig. 3B` 평탄 없음 · '같은 전위 곡선' 주장) · `Fig. S2` 위 축 (네 금속 공통 0.100 mAh cm⁻² ↔ `Table S1` 100 nm) · `Fig. S9` ↔ `Fig. 6B` ↔ `Table S3`. 전부 digest §10 에 적었어요.
- Data S1 (VAMAS 3 개) 은 CasaXPS 맞춤 성분 줄을 읽어 BE 표를 냈어요 (§3g · §17) — 그림 6E–H · S10–S12 의 봉우리 위치 대조에 썼어요.
- 웹앱: Flask 로 `/paper/<slug>` 200 · 렌더 HTML 표 17 · `paper_figure_notes` 29 키 전부 (f1–f6 · fS1–fS17 · t1 · tS1–tS5) · `_paper_pis` = [] (배지 없음 — 맞아요) · 원소 태그 8 개 (Li · P · S · Cl · Bi · In · Ag · Mg) — Bi · Mg · In 원소 쪽에서 1 위예요. 기법 태그 `XPS` 는 웹앱 `METHOD_MAP` 에 xps 가 없어서 기법 쪽 링크는 0 이에요.
- ⚠ **화면 캡처는 못 봤어요** — headless Chrome 이 이 환경에서 40 s 안에 안 끝났어요 (zygote 오류 · 두 번 시도). 데스크톱 · 폰 폭 렌더는 확인 못 한 것으로 적어요. 띄운 임시 서버 · 브라우저는 다 내렸어요 (내 포트 5077 · 5078 만).
- `build_index.py --check` (rc 1 · 배치 대기분 때문) → 이 slug 는 두 곳에만 떠요: '어느 인덱스에도 없음 **[dft]**' · 'comparison_vs_ours.md 미편입'. 아래 (a) · (b) 를 넣으면 풀려요.
- talk 인입 대기열 (`litdb/talks/lee2026_skku_mlip_materials_design.md`) 에 이 논문은 없어요.
- 우리 점착 W 값은 digest 에 없어요 (J m⁻² 숫자 0 · `db/properties/adhesion.json` 은 위치로만 3 번).
- Crossref REST 만 썼어요 — DOI 확인 8 건 + 주제어 발견 검색 5 번 + 저자 · 주제 검색 1 번 (2025 이후 필터 · 일반 UA · 개인 정보 없음). 출판사 페이지 · 본문은 안 열었어요.
- 임시 파일은 전부 scratchpad `kotakadi2025_metallic_interlayers_li_li6ps5cl_operando_sem/` 아래 (`kotakadi_` 접두어 · 공용 이름 없음). inbox 를 읽은 python 은 `-I` 로 돌렸어요.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 + 11-24b 12 편)` — `becker2026_…` 행 바로 뒤 (같은 LPSCl · 금속 층 짝) 가 맞아요. SE 가 LPSCl 이라 이 절의 ⚠ LLZO 표지가 필요 없어요. 분류기는 **[dft]** 예요 (INDEX.md 쪽). 절 머리 '18 편 + 11-24b 12 편' 숫자는 메인이 이 배치 셋을 합친 뒤 고쳐 주세요.

```
| `papers/kotakadi2025_metallic_interlayers_li_li6ps5cl_operando_sem.md` **(본문 16 pp + SI 16 pp + Data S1 (XPS VAMAS 3) · 크롭 29장 (그림 23 + 표 6 · 손 크롭 0 · 번호 공백 0) — 그림 16장 원해상도 + 7장 축소 시트로 봄 · 표는 글자층 · Data S1 맞춤 성분 판독 · 영상 안 옴 · 2026-11-25)** | **[외부·exp·⭐⭐ LPSCl 위 Bi · In · Ag · Mg 100 nm 층의 리튬화 · 도금 · SEI (operando SEM · CTTA · in situ XPS) — ✅ SE = Li₆PS₅Cl (우리 comp1 조성) · operando 셀 적층압 0 · 조건당 셀 1 · 원자단위 계산 0]** ✅ **Souhardh Kotakadi**/J. Aspinall/M. Burton/Y. Liang/Y. Aihara/**Mauro Pasta\*** (Oxford 재료과 · Faraday Institution · Nissan), "**Impact of metallic interlayers at the lithium-Li6PS5Cl solid electrolyte interface**" — ***Joule* 9, 102175 (2025)**, DOI `10.1016/j.joule.2025.102175` (OA CC BY · ChemRxiv 판 `10.26434/chemrxiv-2025-bfts2`). 접촉: Bi 를 SE 위 대 CC 위 = CPE Q **35 배** (4.637 → 163.9 µF s^(α−1) · Brug ≈75 카드 산술) · 리튬화 (0 MPa · 0.2 mA cm⁻²): Bi 0.78 · 0.74 V 평탄 → LiBi → Li₃Bi **+61 %** 에서 박리 · 파괴 · Li 가 층 **밑** 기둥 · 첫 사이클 뒤 단락 / In (증착 ≈1 µm 방울 · InLi +52 % · 전체 +269 %) 멀쩡 / Ag · Mg 고용체 고르게 · Li 는 층 **위** 방울 · 1.5 mAh cm⁻² 입자 수 Ag 481 · In 444 · Mg 321 · 핵 과전압 none ≈17.8 · Bi ≈10.8 · In ≈4.6 · Ag ≈2.0 · Mg 0 mV (figure-read) · CTTA 180 h none ≈0.034 · Bi/In/Ag ≈0.09 · Mg ≈0.05 mAh cm⁻² (정규화 · figure-read) · XPS (Data S1) S–In +0.45–0.58 · S–Mg +0.19–0.21 eV vs Li₂S · 리튬화 뒤 In → Li₂S · Mg −0.05 eV 만 · Ag 는 S 2p 로 안 갈림 · ⚠ **`Fig. S9` 원자료에서 Mg 가 가장 많이 잃고 `Table S3` 로 `Fig. 6B` 재현 안 됨** · `Fig. S2` at% 축이 네 금속 공통 0.100 mAh cm⁻² (100 nm 의 3.8–8 배) · 첫 CE 는 층 없음 ≈95 % 최고 (본문 'CE 향상' 과 어긋남) · `Fig. 6E,F` '30 min' = 데이터 40 · 50 min · 특허 출원 준비 (이해 상충) | **W_ad 보고서 §7 ③ 합금 전위 순서 (Bi ≫ In > Ag ≈ Mg) · §8-2/8-5 계면 상태 (증착 직후 금속 황화물 · 도금 뒤 Li₂S) · §8-3 Li 가 쌓이는 자리 (0 MPa 위 · Bi 밑 — becker2026 15 MPa 와 반대) · §8-4 층 부피 변화 · DEM 접촉 분율 대조 (Q 35 배)** (exp, 외부 · LPSCl) |
```

## (b) 비교 문서에 넣을 줄

분류기가 **[dft]** 라 `--check` 가 요구하는 곳은 `comparison_vs_ours.md` 예요 → §E 한 줄 + Reference key 한 줄이 본 줄이에요. DEM 쪽 거리 (접촉 분율 · 층 부피 변화 · Li 자리) 가 있어서 `comparison_vs_ours_DEM.md` §I 카드도 같이 드려요 (becker2026 와 같은 꼴). 물성 4축 (A–D) 에는 **넣을 것이 없어요** (LPSCl 의 σ · 탄성 · 띠틈이 이 논문에 없어요).

**`comparison_vs_ours.md` §E 행** (`## E. 환원 / 음극(Li 금속) 계면` 표 · 4 칸):
```
| **🆕 (2026-11-25) LPSCl 위 100 nm 금속 층 (Bi · In · Ag · Mg) 은 리튬화 중 이미 SE 와 반응한 계면이다 — 스퍼터 중 S–In (+0.45–0.58 eV vs Li₂S) · S–Mg (+0.19–0.21) 생성 · Mg 는 P 2p 의 ≈50 % 가 환원 P · 도금 뒤 In → Li₂S (159.90 eV) · Mg 는 S–Mg 유지 (−0.05 eV · 약함) · Ag 는 S 2p 로 안 갈림 (Data S1 맞춤값) · 전자 전도 층은 SEI 를 키운다 (CTTA 180 h Bi on SE ≈0.089 > Bi on CC ≈0.062 > 없음 ≈0.034 mAh cm⁻² · figure-read) · 합금 평탄 Bi 0.78 · 0.74 V · In (3 전극) ≈0.6 · Ag ≈0.055 · ≈0.015 V (figure-read)** — ⚠ CTTA 정규화 재현 안 됨 (원자료 Mg 최대) · 0 MPa operando · 조건당 셀 1 | **[Kotakadi25OpSEM]** `Fig. 3` · `Fig. 6` · `Fig. S7` · `Fig. S9`–`S12` · `Table S3` · `Table S4` · Data S1 (Li₆PS₅Cl · 상온 · XPS 막 ≈10 nm 이온빔) | 환원 가장자리 **1.717 V** (Li 교환 0 · comp1 = modelc · grand-potential) → 1.242 V (5 Li₂S + LiCl + P) → 0 V 끝 Li₂S + Li₃P + LiCl — 네 층의 합금 전위가 전부 가장자리 아래라 층\|LPSCl 은 **도금 전 합금 단계부터** 환원 영역 (저자의 '도금 뒤 전자 화학 퍼텐셜이 같아진다' 보다 이르다) · 금속 황화물 · 인화물 계산은 없음 | 🟢 **같은 방향** (Li₂S · 환원 P · 전도 층 SEI 증가) · ⚪ Mg 부동태 · CTTA 순위는 대조 불가 (방법 · 재현 문제) |
```

**`comparison_vs_ours.md` Reference key 행** (Becker26Micro · Ko25MIL 옆):
```
| **[Kotakadi25OpSEM]** ⭐⭐ **LPSCl 위 금속 층 (Bi · In · Ag · Mg 100 nm) 의 리튬화 · 도금 · SEI — operando SEM · CTTA · in situ XPS (Data S1)** · ⛔ **exp 전용 · A–D 물성 4축 진입 금지** (§E 1 행만) · ⚠ CTTA 정규화 재현 안 됨 · 0 MPa operando · 조건당 셀 1 | Souhardh Kotakadi/J. Aspinall/M. Burton/Y. Liang/Y. Aihara/Mauro Pasta\* (Oxford · Faraday Institution · Nissan) *Joule* 9, 102175 (2025) | `papers/kotakadi2025_metallic_interlayers_li_li6ps5cl_operando_sem.md` ✅ | exp |
```

**`comparison_vs_ours_DEM.md` §I 카드** (번호는 메인이 매겨요 — 지금 I-33 까지 · 이 배치 다른 둘도 붙을 수 있어요):
```
### I-xx. `kotakadi2025_metallic_interlayers_li_li6ps5cl_operando_sem` — ★★ (exp · ⛔ 점착 정량 없음 · ✅ LPSCl 계) **증착 자리가 전기화학 접촉 면적을 바꾼다 (CPE Q 35 배) — DEM 접촉 분율의 대조 표적 · 층 부피 변화 (Bi +61 % 파괴 · In +52 % 멀쩡) · 0 MPa 에서 Li 가 쌓이는 자리**

> **무엇을 주나.** Li₆PS₅Cl 냉간 압착 (430 MPa) 위 Bi · In · Ag · Mg 100 nm: Bi 를 SE 위 대 SUS CC 위에 두면 CPE Q 163.9 대 4.637 µF s^(α−1) (35 배 · Brug ≈75 카드 산술 · 3 전극 · 셀 하나 · CC 압착 압력 미기재) · operando SEM (적층압 0 · 0.2 mA cm⁻²): Bi 는 LiBi → Li₃Bi (+61 %) 에서 박리 · 파괴 · Li 가 층 밑 기둥 · In (+52 % · 전체 +269 % · 증착 방울 막) · Ag · Mg (고용체) 멀쩡 · Li 는 층 위 방울 (1.5 mAh cm⁻² 입자 수 481 · 444 · 321) · 5 MPa 반쪽 셀: Bi 2 째 · 층 없음 3 째 사이클 단락 · CTTA: 전도 층이 SEI 를 키운다 (접촉 35 배 ↔ SEI 1.4 배 · figure-read).
>
> **★ DEM 쪽에 닿는 곳.**
> ① 접촉 분율 — '눌러 붙인 박 대 등각 막' 의 전기화학 접촉 비 1/35–1/75 (압력 미기재 → 같은 차수를 내나의 대조로만).
> ② 층의 부피 변화 · 연성이 접촉을 끊는다 (Bi) — 얼마나보다 어느 단계 · 무른 상이 받나 (In).
> ③ Li 가 쌓이는 자리는 압력 · 층 파괴에 따라 — 0 MPa (이 논문) 대 15 MPa (I-27 becker2026) 가 Bi · Ag 둘 다 반대.
> ④ SEI 는 접촉에 비례하지 않는다 (35 배 ↔ 1.4 배).
>
> **⛔ 인용 금지 / 한정어.** 0 MPa 형태를 가압 셀로 옮기지 않는다 · 'Q 35 배' 를 '면적 35 배' 로 단정하지 않는다 · CTTA 의 Mg 순위 (정규화 재현 안 됨) · 조건당 n = 1 · 점착 · 젖음 측정이 아니다 (점착 일은 저자 가설 · ref 24) · 대조 표적이지 보정 표적이 아니다.
> 상세: digest §3b · §3c · §3f · §7c · §10 · §11.
```

## (c) `litdb/pdf_map.tsv` 줄

**필요 없어요** — `--inbox --only kotakadi --dry` 가 본문 · SI 를 제목 100 % 로 자동 짝지어요. 굳이 고정하고 싶으면:
```
kotakadi2025_metallic_interlayers_li_li6ps5cl_operando_sem	kotakadi2025_metallic_interlayers_
```

## (d) 추가로 먹일 논문 (≤ 8 · 최근 먼저 · 전부 litdb 에 없음 · 전부 Crossref 로 서지 확인)

| # | 논문 | DOI | 왜 |
|---|---|---|---|
| 1 | Jun, Lee, Park, Son, Lee, Lee · *ACS Energy Lett.* 11, 2135–2142 (2026) — "Alloy Phase-Formation-Driven Lithium Deposition Pathways in Magnesium-Based Breathing Anodes for Long-Lasting Anode-Free All-Solid-State Batteries" (발견 검색) | `10.1021/acsenergylett.5c03980` | Mg 층의 리튬화 · 석출 경로 — 이 논문 Mg 결론 (β 불균일 · 부동태) 의 후속 대조 · SE 종류는 메타데이터로 미확인 |
| 2 | Burton, Jagger, Liang, Gibson, Aspinall, Long, Swallow, Weatherup, Pasta · *Nat. Commun.* 16, 9304 (2025) — "The role of phosphorus in the solid electrolyte interphase of argyrodite solid electrolytes" (ref 14) | `10.1038/s41467-025-64357-3` | 같은 그룹 · LPSCl SEI 의 환원 P · 부동태 — 우리 §E (0 V 끝 Li₃P) 와 이 논문 Mg '인화물이 Li 소모를 늦춘다' 논증의 근거 |
| 3 | Zhao, Feng, Wu, Guo, Chen, Risal, … · *Nat. Commun.* 16, 4283 (2025) — "Imaging the evolution of lithium-solid electrolyte interface using operando scanning electron microscopy" (발견 검색) | `10.1038/s41467-025-59567-8` | operando SEM 방법 짝 — 층 없는 Li\|SE 계면을 같은 방식으로 (SE 종류는 Crossref 초록이 없어 미확인) |
| 4 | Sivavec, Kravchyk, Kovalenko · *Commun. Chem.* 8, 96 (2025) — "Impact of stack pressure on coulometric titration time analysis" (ref 48) | `10.1038/s42004-025-01496-0` | CTTA 의 압력 · 접촉 의존 — 이 digest §10-① (CTTA 정규화 · 접촉) 판정의 방법 원전 |
| 5 | Alt, Müller, Riegger, Aktekin, Minnmann, Peppler, Janek · *Joule* 8, 2755–2776 (2024) — "Quantifying multiphase SEI growth in sulfide solid electrolytes" (ref 49) | `10.1016/j.joule.2024.07.006` | SEI 저항 환산 (134 nS cm⁻¹) · 10 Ω cm² 목표의 원전 · LPSCl SEI 성장 속도 |
| 6 | Aspinall, Sada, Guo, Kotakadi, Narayanan, Chart, Jagger, Milan, Brassart, Armstrong, Pasta · *Nat. Commun.* 15, 4511 (2024) — "The impact of magnesium content on lithium-magnesium alloy electrode performance with argyrodite solid electrolyte" (ref 37) | `10.1038/s41467-024-48071-0` | Li–Mg + LPSCl · β-Li D 되먹임 논증의 원전 |
| 7 | Jeong, Wang, Yoon, Liu, Chen, McDowell · *ACS Energy Lett.* 9, 2554–2563 (2024) — "Electrochemical behavior of elemental alloy anodes in solid-state batteries" (ref 31) | `10.1021/acsenergylett.4c00915` | 원소별 합금 음극 전기화학 — W_ad 7 절 ③ (합금 전위 순서) 의 넓은 대조 |
| 8 | Aktekin, Riegger, Otto, Fuchs, Henss, Janek · *Nat. Commun.* 14, 6946 (2023) — "SEI growth on Lithium metal anodes in solid-state batteries quantified with coulometric titration time analysis" (ref 12) | `10.1038/s41467-023-42512-y` | CTTA 원전 · 9 nm/µAh cm⁻² 환산 — 고용체 층에 CTTA 를 쓸 때의 가정 확인 |

이미 다른 목록에 있는 것 (새로 안 셌어요): Narayanan 2022 *Nat. Commun.* 13, 7237 (ref 13 · 11-24 추가 목록) · Thomas · Behara · Van der Ven 2024 *Chem. Mater.* 36, 8936 (ref 39 · 11-24b 추가 목록 #2) · Kim S. 2020 *Adv. Energy Mater.* 10, 1903993 (11-24b 목록 #18) · Park Y. 2025 *Inorg. Chem. Front.* 12, 5449 (11-24b 목록 #26) · Sandoval 2023 *Joule* 7, 2054 (ref 28 · 이 배치).

## (e) W_ad · DEM-DFT 보고서에 쓸 거리 (`docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` 7 절 · 7-1 표 · 8 절)

⛔ 우리 W 값은 안 옮겼어요. 아래 문장은 공유 보고서용 초안이라 내부 사정 (판독 방법 · 검산 단계) 은 뺐고, 값에 붙는 사용 조건 (그림 판독 · 셀 하나 · 무가압) 만 남겼어요.

| 보고서 자리 | 넣을 거리 (초안) | 근거 (쪽 · 그림 · 표) · 직접 봤나 | 11-24b digest 와 |
|---|---|---|---|
| **8-3** Li 가 쌓이는 자리 | "같은 Li₆PS₅Cl 이라도 Li 가 쌓이는 쪽은 압력 · 층 파괴에 따라 달랐다. 적층압 없이 위에서 본 셀에서 Ag · In · Mg 100 nm 층은 Li 가 층 위에 방울로 쌓였고, Bi 층은 LiBi → Li₃Bi (부피 +61 %) 에서 들려 깨진 뒤 Li 가 층 밑에서 기둥으로 자랐다 (Joule, 9, 102175 (2025)) — 15 MPa 사후 단면 (Energy Environ. Sci., 19, 2367 (2026)) 과 Bi · Ag 둘 다 반대다. 위에서 보는 관찰은 층 밑의 Li 를 못 본다." | p.4–8 · `Fig. 3E–H` · `Fig. 4` (봤다) | becker2026 와 **반대** (Bi: becker 는 Li 가 CC 쪽 · Ag: becker 는 SE 쪽) · ko2025 (가넷 · 0 MPa) 와 **같은 꼴** → 보고서 8-3 의 '계 · 압력에 따라 다르다' 를 **같은 SE 에서도** 압력 · 층 파괴 · 관찰법으로 좁힐 근거 |
| **8-2 · 8-5** 계면의 상태 | "금속 층 \| Li₆PS₅Cl 은 증착하는 순간부터 반응한다. in situ XPS 에서 In · Mg 는 스퍼터 중 금속 황화물 성분이 생겼고 (Li₂S 대비 +0.45–0.58 · +0.19–0.21 eV), Mg 는 P 도 환원됐다. Li 가 오면 In 쪽은 Li₂S 로 바뀌었다. Ag 는 S 2p 로 반응이 안 갈렸다 (Joule, 9, 102175 (2025) · 원자료 맞춤값)." | p.9 · `Fig. 6E–H` · `Fig. S10`–`S12` (봤다) · Data S1 | choi2025 의 '운전 중 계면 = LPSCl \| SEI \| Li–Ag' 와 같은 그림 · baer2026 · kim2026 (Li 가 닿으면 Li₂S 류) 와 같은 방향 |
| **7-1 표 Ag 행** · 2-3 | LPSCl\|Ag(111) (반응 없는 날카로운 계면) 은 "스퍼터 Ag 는 S 2p 로 반응이 안 보인다 (In · Mg 는 보인다)" 는 한정과 같이 쓸 수 있다 | `Fig. S11` · Data S1 (봤다) | choi2025 (Ag⁰ 와 LPSCl 공존 1.7–1.9 V 창) 과 모순 없음 |
| **8-4** 균열 · 접촉 · 부피 | "층의 부피 변화도 접촉을 끊는다. Bi 는 LiBi → Li₃Bi (+61 %) 에서 깨졌고, In 은 첫 단계 +52 % (전체 +269 %) 를 무른 In 과 방울 꼴 막이 받아 멀쩡했다 — 얼마나보다 어느 단계에서 · 무른 상이 받느냐가 갈랐다. 저자는 층과 이웃 재료의 점착 일이 받아 줄 부피 변화를 정할 수 있다고 보았다 (값 없음)." | p.4–6 · `Fig. 3G,H` · `Fig. 4A–C` · `Table S2` (봤다 · 표는 글자층) | becker2026 (Bi → Li₃Bi 층 유지 · 15 MPa) — 압력이 있으면 Bi 층이 안 깨질 수 있다는 대조 (우리 해석) |
| **8-4** · DEM 접촉 분율 | "층을 고체전해질 위에 증착하면, 집전체 위에 증착해 눌러 붙인 것보다 이중층 용량 계수가 35 배였다 (같은 Bi 100 nm · 한 셀 · 누른 압력 미기재) — 눌러 붙인 박의 전기화학 접촉이 등각 막의 수 % 라는 차수다. 접촉이 넓으면 SEI 도 커졌지만 (180 h Li 소모 ≈0.089 대 ≈0.062 mAh/cm²) 접촉에 비례하지 않았다." | p.3–4 · p.9 · `Table 1` · `Fig. 2C` · `Fig. 6A` (봤다) | 새 거리 — 11-24b 카드에 같은 양 없음 |
| **8-1 · 8-5** 층에 저장되는 Li | "고용체 층 (Ag · Mg) 은 평형 전위가 전량 적정 (CTTA) 의 50 mV 문턱보다 낮아, 합금 속에 저장되는 Li 와 SEI 로 잃는 Li 를 그 방법으로 가르기 어렵다 — 같은 논문의 Mg 결과는 정규화 방식에 따라 순위가 바뀐다." | `Fig. S9` · `Fig. 6B` · `Table S3` (봤다) | 8-1 의 Chu (Energy Environ. Sci., 19, 5836 (2026) · '합금 층에 저장된 Li 와 느린 확산') 과 같은 함정의 LPSCl 판 |
| **8-5** 실험과 견줄 것 | 핵생성 과전압 순서 (층 없음 ≈18 > Bi ≈11 > In ≈5 > Ag ≈2 > Mg ≈0 mV · Li₆PS₅Cl · 3 전극 · 그림 판독) · 합금 전위 순서 (Bi 0.78 · 0.74 V > In ≈0.6 V > Mg · Ag < 0.25 V · 그림 판독) | SI p.6 · `Fig. S8` · `Fig. 3A–D` · `Fig. S7` (봤다) | becker2026 의 Bi ≫ Au > Ag 와 이어 붙일 수 있다 (Bi 평탄 0.78 · 0.74 V ↔ 800 · 760 mV 같다) · haslam2025 의 Ag 0.054 V 와 같은 자리 |
| **7 절 ③** 합금 구동력 | '생기나 · 녹나 · 남나' 를 나눌 근거 한 편 더 — Ag · Mg (고용체 · 금속이 Li 로 퍼짐) 대 In · Bi (마지막 금속간 상이 남음) | p.6–8 (봤다) | haslam2025 (Au 남음 · Ag 녹음) · becker2026 (Au 입자 · Ag 녹음 · Bi 층) 과 같은 갈래 |
| **8-7** 읽은 논문 표 | `\| Joule, 9, 102175 (2025) \| Li₆PS₅Cl 위 금속 층 넷 (Bi · In · Ag · Mg) · operando SEM · 전량 적정 · in situ XPS \| 8-2 · 8-3 · 8-4 · 8-5 \|` | — | — |

**Kotakadi 를 기다린다고 적힌 곳** (그 파일들은 안 고쳤어요 — 메인이 slug 로 바꿔 주면 돼요):
- `litdb/papers/baer2026_li_metal_argyrodite_interface_stability_transport.md` — (d) 표 #1 (ChemRxiv 판 · litdb '없음') + '🔗 이어 읽기 · 바로잡기 (2026-11-24b 묶음)' 절의 "(d) 1 번 Kotakadi 외 ChemRxiv (2025) 는 저널판이 있다" 줄.
- `litdb/papers/choi2025_silver_exsolution_argyrodite_anode_free.md` — (d) 표 #1 ('없음').
- `litdb/papers/lepley2015_modeling_interfaces_between_solids_li_battery_materials.md` — (d) 표 #2 ('없음').
- 보고 · 목록: `_curation/batch_2026_11_24b/extra_papers_2026_11_24b.md` #1 · `becker2026 … .report.md` (d) #1 · `sandoval2025 … .report.md` (d) #3 · `_curation/wishlist.md` 784 줄.
- 11-24b digest 들의 '🔗 이어 읽기 · 바로잡기' 절에서 Kotakadi **내용** 을 기다린 곳은 없었어요 (위 baer2026 의 서지 줄 하나뿐). 내용상 고칠 곳으로 보이는 건 하나 — W_ad 보고서 8-3 의 Ko 2025 문단 끝 '계 · 압력에 따라 다르다' (위 8-3 행 참고).

## (f) 그림 · 자료 크롭 요약

- 크롭 **29 장** = 본문 그림 6 + 표 1 + SI 그림 17 + 표 5 · 도구 그대로 · **손 크롭 0** · 다시 자름 0 · 번호 공백 0 (`missing_labels` []) · auto_fallback 표시 0.
- 빈칸 의심 다섯 (blank ≥ 0.965: `S1` · `S3`–`S6`) 은 선 그림이라 정상 (축소 시트로 확인). 본문 크롭 다섯 (`fig_1` · `3` · `4` · `5` · `6`) 은 쪽 머리 (Joule · CellPress 로고) 가 같이 잘렸어요 — 보기에만 거슬리고 내용은 다 들어 있어요.
- **안 온 자료**:
  - 영상 — 본문은 도금 영상을 **Videos S1–S7** 로 부르고 (p.6 · 배치 메모의 'S1–S6' 보다 하나 많아요), 리튬화 영상은 번호 없이 'supplemental files' 로만 불러요. digest 는 `Fig. 3` · `Fig. 4` 스냅숏으로만 읽었고 '영상 안 봄' 을 적었어요. 영상이 오면 Bi 균열 시작 시점 · In Li 핵 시점 · Ag 'Li 는 층 위' 를 프레임으로 확인할 수 있어요 (필수는 아니에요).
  - **'Sup2' 엑셀 (40 MB)** — 본문 · SI 어디에도 이름이 없어요 (SI 는 보충 자료 목록을 안 실어요). 본문은 Data S1 (XPS 원자료) 과 영상만 이름을 부르고 *"All data used in this study are included as supplemental data"* (p.13) 라고만 해요 → 그림 원자료 (전기화학 · CTTA · 덮임 · 크기 분포) 로 짐작해요 (확인 안 됨). **digest 자체엔 필요 없지만, §10-① (CTTA 정규화 — `Fig. S9` ↔ `Fig. 6B` ↔ `Table S3`) 과 §10-② (`Fig. S2` at% 축) 를 가르려면 필요해요.** 통째가 무거우면 CTTA (`Fig. 6` · `Fig. S9`) 시트만이라도 받으면 돼요.
- Data S1 (`{Mg,Ag,In}_XPS.vms`) 은 다 썼어요 — 파일당 36 블록 · CasaXPS 맞춤 성분이 들어 있어서 봉우리 위치를 숫자로 대조했어요 (digest §3g 표 · §17 절차). 셋째 스퍼터 단계 이름 (In 40 · Ag 50 · Mg 30 min) 이 `Fig. 6E,F` 표기와 다르다는 것도 이 파일로 잡았어요.

## (g) Jeff Sakamoto 저자 여부

**아니에요.** 저자는 Kotakadi · Aspinall · Burton · Liang · Aihara · Pasta 여섯이고 (Oxford · Faraday Institution · Nissan), Sakamoto 는 refs 23 (Haslam 2025) · 29 (Haslam 2023) 로 인용만 돼요. INDEX 행에 🏷 배지를 달지 않았고 웹앱 `_paper_pis` 도 [] 예요.
