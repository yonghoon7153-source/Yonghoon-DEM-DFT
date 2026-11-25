# 끝 보고 — hiraoka2025_operando_raman_carbon_structure_anode_free_sulfide (배치 2026-11-24b · #6)

- digest: `litdb/papers/hiraoka2025_operando_raman_carbon_structure_anode_free_sulfide.md` (새 파일 · 366 줄 · 한국어 standalone · §0 · §0-1 · §1–§12 · 깊이 기준 zuo2022 · 꼴은 같은 계열 metzler2026 을 따랐어요)
- 그림: `litdb/figures/hiraoka2025_operando_raman_carbon_structure_anode_free_sulfide/` — 크롭 **19 장** = 도구 18 (`--slug … --pdf 본문 SI --clean`) + **손 크롭 1 (`Fig. 1`)**. `Fig. 1` 은 캡션 줄이 두 단짜리 본문 글자 블록에 묶여서 도구가 캡션을 못 찾았어요 (`figures.json` `manual_crop` 에 좌표 · 사유). `missing_labels` 둘: `f1` = 손 크롭으로 해결 · `tS4` = **SI 에 Table S4 가 없어요** (본문 p.27966 이 "Tables S3 and S4" 라고 가리키지만 14 쪽 SI 는 Table S3 에서 끝 — 논문 쪽 참조 오류 · `resolved` 에 적음). `figures.json` 에 전 항목 `viewed` / `viewed_how` 를 달았고, 캡션은 추출 잔재만 고쳤어요 (본문 5 개 = 합자 ﬁ · 'AF- ASSB' 줄바꿈 · SI 8 개 = 두 줄 캡션이 첫 줄에서 잘린 것) — 원문은 `caption_raw` 에 남겼어요.
- 공유 파일은 안 건드렸어요. `litdb/figures/_sources.json` 은 추출 도구가 이 slug 항목을 더해 썼어요 (손 안 댐 · 그 항목의 `figures: 18` 은 손 크롭 1 장을 안 센 값). git 작업 없음 — 메인 checkpoint **`7a9f8c62`** 에 크롭 19 장 + 원래 `figures.json` · **`482f1aa9`** 에 digest 첫 판 (352 줄) 이 이미 들어가 있고, 지금 digest · `figures.json` 은 그 뒤 고친 '수정' 상태예요 (§3-9 추가 · §12 다시 짬 · 범위 숫자 몇 개 고침 · figures.json viewed · 캡션 · Fig. 1 항목).
- 점검 (읽기만): `build_index.py --check` → 이 digest 는 "어느 인덱스에도 없음 [dft]" + "comparison_vs_ours.md 미편입" (아래 (a) · (b) 를 넣으면 풀려요) · `extract_figures.py --inbox --only hiraoka2025` (매칭표만) → 본문 + SI 자동 매칭 **`[제목 87%]`** · `extract_figures.py --audit` 에서 이 slug 경고 없음 · 웹앱 `paper_figures` 19 · `paper_figure_notes` 19/19 · `_paper_pis` = [] · 원소 페이지 Li · C · Ag · P · S · Cl 연결 ✓ · 기법 페이지: `Raman` 은 용어 사전에 항목이 없어 안 붙어요 (`metzler2026_…` 도 똑같이 빈 집합) · 시험: `test_v3_literature` + `test_v3_markdown` **43 / 43 통과** · `test_webapp -k "sakamoto or litdb_figure or recent_digests or digest_date or element_papers or glossary_papers or figure_comment"` 7 통과 1 실패 = `test_recent_digests_are_on_every_litdb_surface` (INDEX · comparison 미편입 — 합치면 풀려요 · 같은 배치 baer · becker · chu · haslam · lepley · xie2024 도 같은 이유로 같이 걸려 있어요).

⚠ **메인에 알릴 것**
1. **이 논문은 탄소가 받은 Li 양을 재지 않았어요.** '몇 mAh cm⁻² 까지' 의 답은 대리 값 넷뿐이에요 — 설계 (Ag/C 용량 ≈ 양극의 10 % → ≈0.6 mAh cm⁻² · Ag + C 합) · `Fig. 2a` 첫 충전 평탄 전 figure-read ≈1.2 mAh (≈0.4 mAh cm⁻²) · operando G 이동이 보인 3.3 V 측정점까지 흐른 전하 ≈0.6 mAh (`Fig. S1a` 적분 · 단면 셀 면적 미상) · CB 의 LiC₆ 상한 ≈0.3 mAh cm⁻² (밀도는 `kang2026_…` 값을 빌린 가정). 전부 첫 충전 (≈6 mAh cm⁻²) 의 수 %–10 % 예요.
2. **8-3 의 'Li\|C (리튬화된 탄소 · LiC₆)' 근거로는 '리튬화' 까지만 돼요 — LiC₆ 는 아니에요.** 충전 중 CB 의 G 가 두 점에서 같은 방향으로 ≈24 cm⁻¹ 내려갔다가 방전 끝에 돌아온 건 '맨 탄소가 아니다' 를 받쳐요. 하지만 가장 큰 변화는 단면 단락 (셀 셋 다 ≈3.85 V) 뒤 스펙트럼이고, 2 대역 맞춤에서 셋째 띠가 빠졌고, 5 h 쉰 뒤 (ex situ) 는 변화가 작고 G 가 오히려 **위로** 갔어요. 보고서 문구 수정안은 (e) 에 있어요.
3. **그림–표 어긋남 (디지털 판독으로 확인)**: `Fig. 4a,b` 점 2 충전 0.6–2.4 V 가 한 칸 (0.3 V) 왼쪽에 찍힘 · `Fig. 4b` 방전 점이 x = 2.00–3.43 V 에 찍힘 · **`Fig. 4a,b,d` 점 2 방전 계열 ≠ `Table S2`** (R 그림 0.98–1.83 대 표 1.35–6.65 · 그림 D 는 오히려 점 1 표값과 ≤1.7 cm⁻¹) · `Fig. 7` ≠ `Table S3` 세 스펙트럼 평균 (D 최대 ≈5 cm⁻¹ · AR 29 % 1.43 대 1.02) · Table S4 없음. 축은 점 1 충전값으로 맞춰서 표와 0.2–0.9 px 안에서 일치하는 걸 먼저 확인했어요.
4. **'aspect ratio' (ΣH/ΣW) 는 모양이 아니라 세기 지표예요** — 높이가 정규화 안 돼 있어서 (저자도 인정) 같은 물질 초기값이 점 1 3.04 · 점 2 1.81 로 갈려요. 인용 금지로 적었어요.
5. **새 봉우리 1087 · 1854 · 3648 cm⁻¹ 의 배정**: 저자는 'Ag–Li 합금과 관련' 이라고만 해요 (금속 · 합금은 Raman 활성 모드가 없다고 저자도 씀). 위치가 Li₂CO₃ · Li₂C₂ (아세틸라이드) · LiOH 와 가까워서, 드러난 단면의 Li 가 상자 분위기와 반응한 산물일 수 있다는 **제 가설**을 digest §10-⑦ 에 [일반 지식 · 기억값 · 원전 미확인] 표지로 적었어요. 1848 은 D · G 가 없는 석출물에서 제일 세서 탄소 격자 신호는 아니에요.
6. **앞 묶음 목록 (`extra_papers_2026_11_24.md` 표 2 #1) 의 Lee 2020 'Ag : 카본블랙 3 : 1'** 이 이 논문 배합 (CB 12 g : Ag 4 g = **Ag : CB 1 : 3**) · `kang2026_…` (1 : 3) 과 반대예요. 같은 배치 #9 (`lee2020_…`) 가 원전으로 확인해 주면 좋겠어요 (목록 파일은 안 건드렸어요).
7. **집전체가 SUS 예요** — W_ad 보고서 7-1 의 집전체 행은 Cu(111) 뿐인데, 이 셀 · Lee 2020 계열 · [우리 그룹] `kang2026_…` 도 SUS 박 · 막대예요 [다른 카드].
8. 서론의 '무음극이면 SE 가 SEI 를 안 만든다' 는 우리 grand-potential 환원 쪽 경계 · `baer2026_…` · `chaney2024_…` 와 어긋나요 (§10-⑪ · §7 E 행). 수치는 안 옮겼고 위치만 적었어요.
9. 발견 검색 (최근 2 년 먼저): Crossref 주제어 검색 6 번 (제목 없이 · 2025 이후 · 한 번은 빈 응답이라 다시 쳐서 받음) + 1저자 검색 1 번 + DOI 확인 5 번 + 참고문헌 2 편 확인 2 번 — 일반 UA · 개인정보 없음 · 본문은 안 열었어요. 같은 배치에 #8 Ko 2025 · #9 Lee 2020 · #11 Xie 2024 가 이미 들어 있어서 (d) 에서 뺐어요.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 한 묶음)` — 행 순서상 Ag/C 인터레이어 묶음의 **`metzler2026_sputtered_ag_carbon_interlayers_anode_free` 행 다음** (같은 'Li 가 닿는 탄소' 축 · `metzler2025_…` · `spencerjolly2023_…` 이웃). (baer 보고서가 짚은 대로 절 머리 '18 편 한 묶음' 문구는 11-24b 를 넣으면 같이 고쳐야 할 거예요.)

| `papers/hiraoka2025_operando_raman_carbon_structure_anode_free_sulfide.md` **(본문 11 pp (1 쪽 = 호 표지) + SI 14 pp (그림 S1–S8 · 표 S1–S3) · 크롭 19 장 (도구 18 + 손 1 · Table S4 는 SI 에 없음) · 그림 16 장 전부 실독 · `Fig. 4` · `7` · `S1a` · `2a` 디지털 판독 · 2026-11-24)** | **[외부·exp·⭐⭐ Ag/카본블랙 층의 CB 도 충전 중 Raman 이 바뀐다 (저자: Li 삽입 · 흡착) · 점착 트랙 "Li 가 닿는 탄소는 맨 탄소인가" · ⛔ Li 양 · 상 동정 · 점착 0]** ✅ **Koji Hiraoka**/Junichi Sakabe/**Naoki Suzuki\***/**Shiro Seki\*** (Kogakuin Univ. · Samsung Device Solutions R&D Japan), "**Operando and ex situ Raman spectroscopies for evaluating carbon structural changes in anode-free-type sulfide-based all-solid-state Li-ion batteries**" — ***J. Mater. Chem. A* 13, 27960–27969 (2025)**, DOI `10.1039/D5TA02406D`. Ag/C = CB (D50 38 nm · 상품명 · BET · XRD 미기재) 12 g + Ag (D50 60 nm) 4 g + PVDF (✎ 70 : 23 : 6.5 wt%) · 10 µm on **SUS 10 µm** ‖ Li₆PS₅Cl 시트 100 µm ‖ LZO-NCM90 (≈3 cm² · 설계 18 mAh) · WIP 490 MPa 353 K · 사이클 5 mA (C/4) · 318 K · ≈2 MPa · 첫 방전 figure-read ≈15 mAh (본문 '≈16'). 초기 CB: D 1349 · G 1589 cm⁻¹ · 2 대역 높이비 R 1.13–1.25 (✎ 표) · G FWHM ≈66. operando (단면 · 실온 · 0.11 mV s⁻¹ · 532 nm 3.2 mW ∼1 µm · 점 2): **G 1583 → 1559 (3.3–3.9 V 충전) → 1540 (3.6 V 방전) → 1575 (2.1 V)** · D 1355 → 1369 → 1382 → 1362 · R 1.25 → 1.04 → 3.70 → 1.25 · 새 봉우리 1087 · 1854 · 3648 (배정 못 함) · ex situ (5 h 휴지) 변화 작음 · G 반대로 +5–9 · Li 는 **Ag/C \| SUS 사이** (100 % 주석 ≈50 µm). Li 양 무측정 — 대리 값 ✎ 0.3–0.6 mAh cm⁻² (첫 충전의 수 %–10 %). 🔴 셀 셋 다 ≈3.85 V 단면 단락 (최대 변화는 단락 뒤) · 2 대역 맞춤에 셋째 띠 (`Fig. S4`) · aspect ratio = 비정규화 세기 · `Fig. 4` 점 2 방전 ≠ `Table S2` · `Fig. 4a,b` 점 2 충전 한 칸 밀림 · `Fig. 7` ≠ `Table S3` 평균 · ref 27 오기 · 서론 'SEI 없음' | 점착 트랙 (W_ad 보고서 7-1 카본블랙 행 · 8-3 Li\|C = 리튬화 결함 탄소 (LiₓC · x 미정) · LiC₆ 는 이상화된 끝 · 집전체 SUS 행) · 탄소 Raman 받을 때 사양 (digest §8 ⑥) · 이웃 `metzler2026_…` · `metzler2025_…` · `kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode` ([우리 그룹] 같은 배합) · `spencerjolly2023_…` |

---

## (b) `comparison_vs_ours.md` 에 넣을 줄

**A–D 물성 4축: 본 자리 없어요** (SE 물성값 0 — '∼2 mS cm⁻¹' 는 자료 없는 서술 · PS₄³⁻ 426 cm⁻¹ 는 식별용).

### b-1. `📑 Reference key` 표에 한 행 (4 칸: 약칭 | 논문 | digest/status | 유형)

| **[Hir25Ram]** ⭐⭐ **Ag/카본블랙 층 단면 operando + ex situ Raman — CB 의 D · G 띠가 충전 중 바뀌고 방전 뒤 대부분 돌아온다 (저자: Li 삽입 · 흡착) · Li 는 Ag/C \| SUS 사이** · ⛔ **Li 양 · 상 동정 (XRD · XPS) · 점착 없음 → A–D 물성 4축 수치 진입 금지** · ⚠ 단면 셀 셋 다 ≈3.85 V 단락 · 2 대역 맞춤 · 세기 비정규화 · CB 상품명 · BET 미기재 | **Koji Hiraoka**/Junichi Sakabe/**Naoki Suzuki\***/**Shiro Seki\*** (Kogakuin + Samsung Japan) 2025 ***J. Mater. Chem. A* 13, 27960** (DOI 10.1039/D5TA02406D) — "Operando and ex situ Raman spectroscopies for evaluating carbon structural changes in anode-free-type sulfide-based all-solid-state Li-ion batteries" | ✅ `papers/hiraoka2025_operando_raman_carbon_structure_anode_free_sulfide.md` — 판정은 **§E 1 행** + `comparison_vs_ours_DEM.md` **§I 블록** (넣으면 I-23) | 실험 전용 (단면 현미 Raman 532 nm · operando + ex situ · 광학 단면 · 계산 0) |

### b-2. §E 표에 한 행 (4 칸: 주장 | 출처 | 우리 | 일치) — `⚙ 🆕 Ag–C 인터레이어의 운전 중 상` 행 ([SJ23AgC]) 바로 다음

| **⚙ 🆕 (2026-11-24) Ag/카본블랙 층의 CB (D50 38 nm · 결함 많은 터보스트래틱 · 초기 R 1.13–1.25) 도 충전 중 구조가 바뀐다 — operando G 1583 → 1559 (3.3–3.9 V 충전) → 1540 (3.6 V 방전) → 1575 cm⁻¹ (2.1 V) · D 1355 → 1369 → 1382 → 1362 · 저자 해석 = 소량 Li 삽입 + 흡착 · ex situ (5 h 휴지) 변화 작음 · G 반대로 +5–9 · Li 금속은 Ag/C \| SUS 사이** (점착 트랙) | **[Hir25Ram]** `Fig. 3` · `Fig. 4` · `Fig. S4` · `Table S1` · `S2` · `Fig. 7` · `Table S3` · `Fig. S8` | 우리 음극측 축은 SE 환원 산물 (Li₂S/Li₃P/LiCl) · W_ad 탄소 쌍은 맨 흑연 (보고서 §2 · 값은 그 보고서와 `db/properties/adhesion.json` 에서만) · **Li\|C (리튬화) 미계산** · 이 논문 서론 'SE 는 SEI 를 안 만든다' 는 우리 grand-potential 환원 쪽 경계와 어긋남 | 🟡 **계산 대상 목록만 이식** — 충전 중 Li 가 닿는 탄소 = 리튬화된 결함 탄소 (LiₓC · x 미정) · LiC₆ 기저면은 이상화된 끝 · 집전체 SUS 면 후보 · ⛔ G 이동 · R 을 Li 양 · stage 로 옮기지 않는다 (단면 단락 셀 · 2 대역 · 가열 미점검) · ⚠ `Fig. 4` 점 2 방전 ≠ `Table S2` · 대조 사양은 `comparison_vs_ours_DEM.md` §I-23 |

### b-3. `comparison_vs_ours_DEM.md` §I 끝 (I-22 다음) 에 블록

```
### I-23. `hiraoka2025_operando_raman_carbon_structure_anode_free_sulfide` — ★★ Ag/카본블랙 층의 CB 도 **운전 중 Raman 이 바뀐다 (리튬화 · 정성)** — Li 금속이 닿는 탄소는 맨 탄소가 아니다 · ⚠ LiC₆ 근거 아님

> **무엇을 주나.** CB (D50 38 nm) + Ag (60 nm) 1 : 3 + PVDF · 10 µm on SUS ‖ Li₆PS₅Cl ‖ LZO-NCM90 적층 셀 (WIP 490 MPa · 운전 ≈2 MPa · 318 K · *J. Mater. Chem. A* 13, 27960 (2025)).  단면 operando Raman (실온 · 0.11 mV s⁻¹): G 1583 → 1559 (충전 3.3–3.9 V) → 1575 cm⁻¹ (방전 끝) · ex situ 단면: Li 가 Ag/C | SUS 사이 (100 % 주석 ≈50 µm).
>
> **★ 우리 축에 닿는 곳.**
> ① **7-1 카본블랙 행** — 결함 · 작용기 면 + '충전 중 리튬화된 결함 탄소' 를 같이 볼 것 · Li\|C 의 W 는 맨 · 리튬화 두 끝 (범위).
> ② **8-3 문장** — 'Li\|C (리튬화된 탄소 · LiC₆)' → '흑연이면 LiC₆ · 카본블랙은 Li 양 미정'.
> ③ **집전체 SUS** — 7-1 Cu 행만으로는 이 계열을 못 덮는다 ([우리 그룹] kang2026 도 SUS).
> ④ **DEM** — 제조 490 MPa · 운전 ≈2 MPa · Ag/C 10 µm 대 Li 층 수십 µm · 구속 없는 단면으로 Li 가 새어 단락 (자유면 경계 주의).
>
> **⛔ 인용 금지 / 한정어**
> · Li 양 · 단계 (stage) · 상 동정 없음 — 'CB → LiC₆' 금지 · 탄소 몫은 ✎ 첫 충전의 수 %–10 % (대리 값).
> · 최대 변화는 단면 단락 (≈3.85 V) 뒤 스펙트럼 · 2 대역 맞춤 (셋째 띠 누락) · aspect ratio 는 비정규화 세기 지표.
> · `Fig. 4` 점 2 방전 ≠ `Table S2` · `Fig. 7` ≠ `Table S3` 평균 · operando 점 2 개 · ex situ 3/10 선택.
> 상세: digest §0 · §0-1 · §3-5 · §3-8 · §8 · §10.
```

---

## (c) `pdf_map.tsv`

**필요 없어요** — `extract_figures.py --inbox --only hiraoka2025` (매칭표만) 가 본문 + SI 둘을 자동으로 붙였어요 (`[제목 87%]`). 굳히고 싶으면 한 줄:

```
hiraoka2025_operando_raman_carbon_structure_anode_free_sulfide	hiraoka2025_operando_raman_carbon_anode_free
```

---

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저)

> 대조: `litdb/papers` 파일 이름 + digest 본문 grep · `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md` grep · 배치 `batch.json` (12 편).  1–5 는 Crossref 주제어 검색 (제목 없이) · 저자 검색으로 찾고 DOI 로 서지를 맞췄어요 (본문 안 엶 · 1–3 은 제목만 보고 고른 거라 내용은 원문 확인이 필요해요).
> 이미 litdb 에 있는 이웃 (세지 않음): ref 31 `spencerjolly2023_…` · `metzler2025_…` · `metzler2026_…` · `kang2026_stress_…`.  같은 배치에서 먹이는 중 (뺌): Lee 2020 *Nat. Energy* 5, 299 (ref 29 · #9) · Xie 2024 *Adv. Energy Mater.* 14, 2302960 (#11 · `xie2024_agc_buffer_layer_lithiation_delithiation_mechanism` 이 이미 써져 있음) · Ko 2025 *Nat. Commun.* 16, 1066 (#8).

| # | 문헌 | 왜 (우리 축) | litdb | 목록 |
|---|---|---|---|---|
| 1 | Liu, Lu, Clemens · *Electrochim. Acta* 574, 149375 (2026) — "Effect of carbon interlayer preconditioning on in-situ plated lithium metal stability in anode-free solid-state batteries" · DOI 10.1016/j.electacta.2026.149375 | 탄소 층을 미리 조건화했을 때 석출 Li 안정성 — Li \| 맨 탄소 대 Li \| 리튬화 탄소 (8-3) 의 실험 짝 | 없음 | 없음 |
| 2 | Lee J., Choi Y., Lee J. · *J. Power Sources* 670, 239539 (2026) — "Unveiling the high lithiophilicity of lithiated hard carbon for lithium metal battery anodes" · DOI 10.1016/j.jpowsour.2026.239539 | '리튬화된 무질서 탄소는 친Li' — 7-1 카본블랙 행의 리튬화 끝 모형에 바로 걸려요 (계 · 방법은 원문 확인) | 없음 | 없음 |
| 3 | Hiraoka, Sato, Seki, Yamamoto · *ACS Appl. Energy Mater.* 9, 818 (2026) — "Multimodal Analysis of Short- and Medium-Term Degradation in Multilayered All-Solid-State Batteries" · DOI 10.1021/acsaem.5c03001 | 같은 1저자 · 교신의 후속 — 단면 셀 단락 · Raman 방법 문제를 고쳤는지 볼 곳 | 없음 | 없음 |
| 4 | Yuan, Guo, Gurgan, Siddique, Li, Jang, Noh, Kim · *Carbon* 238, 120214 (2025) — "Raman spectroscopy analysis of disordered and amorphous carbon materials: A review of empirical correlations" · DOI 10.1016/j.carbon.2025.120214 | I_D/I_G · 폭 → L_a · 단계 판정 — Raman 으로 7-1 행을 고르는 방법 원전 (digest §8 ⑥ · §10-④) | 없음 | 없음 |
| 5 | Ko D., Kim H., Park H., Kim E., Kim H. · *ACS Nano* 19, 16957 (2025) — "Correlation between the Microstructure of the Carbon Protective Layer and Cycle Performance of Anode-Free All-Solid-State Lithium-Ion Batteries" · DOI 10.1021/acsnano.5c02926 | **탄소 미세구조 ↔ 무음극 전고체 성능** — 탄소 '종류' 축을 정면으로 | 없음 | 없음 |
| 6 | Suzuki, Yashiro, Fujiki, Omoda, Shiratsuchi, Watanabe, Aihara · *Adv. Energy Sustain. Res.* 2, 2100066 (2021) — "Highly Cyclable All-Solid-State Battery with Deposition-Type Lithium Metal Anode Based on Thin Carbon Black Layer" · DOI 10.1002/aesr.202100066 (ref 30) | 이 논문이 시험한 '과포화 CB → Li 석출' 가설의 원전 · 카본블랙 층 | 없음 (`sandoval2025_electro_chemo_mechanics_anode_free_ssb` 에 인용만) | 없음 |
| 7 | Zhou, Doerrer, Kasemchainan, Bruce, Pasta, Hardwick · *Batter. Supercaps* 3, 647 (2020) — "Observation of Interfacial Degradation of Li₆PS₅Cl against Lithium Metal and LiCoO₂ via In Situ Electrochemical Raman Microscopy" · DOI 10.1002/batt.201900218 (ref 52) | Li \| LPSCl 계면 Raman 분해 산물 (Li₂S 383 cm⁻¹) 원전 — 'SEI 없음' 주장 · 새 봉우리 배정 대조 | 없음 | 없음 |
| 8 | Chacón-Torres, Wirtz, Pichler · *ACS Nano* 7, 9249 (2013) — "Manifestation of Charged and Strained Graphene Layers in the Raman Response of Graphite Intercalation Compounds" · DOI 10.1021/nn403885k (ref 48) | 흑연 Li-GIC 의 G 가 단계마다 어디로 가나 — 저자의 '흑연과 비슷한 경향' (방향이 엇갈림 · digest §10-⑤) 확인처 | 없음 | 없음 |

다음 순번: Sadezky 외 *Carbon* 43, 1731 (2005) (SI S3 · 5 대역 맞춤) · Mukofukasawa 외 *RSC Adv.* 15, 24117 (2025) (operando Raman · Li 석출 미세전극 — 새 봉우리 배정 대조) · Yuan 외 *Energy Storage Mater.* 76, 104110 (2025) (황화물 ASSB operando Raman 리뷰) · Hiraoka 외 *APL Energy* 3, 021502 (2025) (같은 1저자 Raman 리뷰) · Oh 외 *Batteries & Supercaps* 9, e70514 (2026) (저적층압 황화물 음극 계면 · DEM 압력) · Park 외 *Inorg. Chem. Front.* 12, 5449 (2025) (LPSCl \| Li 온도별 계면 반응).

---

## (e) DEM-DFT 보고서 (W_ad 보고서) 에 쓸 거리

| 보고서 항목 | 이 논문에서 쓸 점 | 위치 (쪽 · 그림 · 표) | 직접 봤나 |
|---|---|---|---|
| **1. 탄소 정보 — 7-1 표 입력 (Q1)** | 카본블랙 · 상품명 · BET · XRD (d₀₀₂ · L_a) · TEM · XPS **[미확인]** · **D50 38 nm** · Ag D50 60 nm · CB 12 g : Ag 4 g (Ag : CB = 1 : 3) + PVDF 8 wt% 용액 14 g (✎ 70 : 23 : 6.5 wt%) · SUS 10 µm 위 · 10 µm · 353 K 20 min → 373 K 진공 12 h · Raman (532 nm): CB 분말 **D 1349 · G 1589** · 날카로운 2D 없음 · 2 대역 맞춤 높이비 **R 1.25 · 1.13 (operando 초기) · 1.14–1.20 (ex situ 초기)** · 원 높이비 figure-read ≈1.0 · G FWHM ≈66 cm⁻¹ → **'결함 · 작용기가 많은 탄소 (카본블랙)' 행** · [우리 그룹] `kang2026_…` Ag–C 층 (CB 35 nm · Ag 60 nm · 1 : 3 · PVDF 8 wt% · 10 µm SUS) 과 거의 같은 배합이라 **우리 그룹 탄소의 가장 가까운 문헌 짝** [다른 카드] | p.27961–27963 · `Fig. 2c` · `Table S1`–`S3` · digest §3-1 · §3-4 | ✅ `Fig. 2c` 원해상도 + 확대 · 표는 PDF 글자층 |
| **2. SE · 셀 조건 (Q1)** | **Li₆PS₅Cl** (RT ∼2 mS cm⁻¹ · 자료 없음) 슬러리 시트 100 µm (아크릴 1 wt% · 부직포) · LZO-NCM90 85 : 15 : 3 : 1.5 · ≈3 cm² · 설계 18 mAh · **WIP 490 MPa · 353 K · 30 min** / 사이클 **5 mA (C/4 · ✎ ≈1.7 mA cm⁻²) · 318 K · ≈2 MPa** / operando 단면 셀 **실온 · ≈2 MPa · 0.11 mV s⁻¹** / ex situ **0.5 mA × 4 h · 318 K + 5 h 휴지** | p.27961–27962 · `Fig. 1` · digest §3-1–§3-3 | ✅ `Fig. 1` (손 크롭) · `Fig. S1` · `Fig. S7` |
| **3. D · G 변화와 해석 (Q2)** | operando 점 1: **G 1583 → 1566 (3.3 V) → 1559 (3.6–3.9 V 충전) → 1540 (3.6 V 방전) → 1575 (2.1 V)** · **D 1355 → 1369 → 1382 (3.3 V 방전) → 1362** · R 1.25 → 1.04 → 3.70 → 1.25 · 폭 뚜렷한 변화 없음 (D 106–163 · G 45–74) · 3.0 V 충전 ~ 2.7 V 방전에서 띠가 바탕 위로 거의 사라짐 · D–G 사이 셋째 띠 (≈1380–1470) / 해석: 저자 = 소량 Li 삽입 + 흡착 (흑연 Li-GIC 와 '비슷') · 형광 = 금속 같은 상태 · 새 봉우리 = 'Ag–Li 합금 관련' / ex situ: 변화 작고 G **+5–9 (반대 방향)** → 저자 = operando 는 비평형 (과포화) / 도금 전후: G 이동이 시작된 3.3 V 측정점은 셀 전류가 오르는 곳 (≈0.7 mA) 이라 '도금 전 삽입' 과 '도금과 함께' 는 못 가름 | p.27963–27967 · `Fig. 3` · `Fig. 4` · `Fig. S2`–`S5` · `Fig. 6` · `Fig. 7` · `Table S1`–`S3` · digest §3-5 · §3-7 | ✅ 전부 원해상도 · `Fig. 3` · `4a/b/d` 확대 · `Fig. 4` · `7` 디지털 판독 |
| **4. 몇 mAh cm⁻² 까지 (Q2)** | **무측정** — 대리 값: 설계 ✎ ≈0.6 mAh cm⁻² (Ag + C) · `Fig. 2a` 첫 충전 평탄 전 figure-read ≈1.2 mAh ≈0.4 mAh cm⁻² · operando 3.3 V 측정점까지 figure-read ≈0.6 mAh (`Fig. S1a` 적분 · 면적 미상) · LiC₆ 상한 ✎ ≈0.3 mAh cm⁻² (밀도 가정) → 첫 충전의 수 %–10 % · ⇒ 리튬화 탄소는 **계면의 막 조건** (W 는 탄소 쪽 표면 상태 하나를 정하는 문제) | p.27961 · `Fig. 2a` · `Fig. S1` · digest §3-8 ④–⑦ | ✅ `Fig. 2a` · `S1a` 디지털 판독 |
| **5. 7-1 표 · 8-3 (Q3)** | **7-1 카본블랙 행** '같이 볼 것' 칸에 **'충전 중에는 리튬화된 결함 탄소 면도 후보'** 를 더하고, Li\|C 의 W 는 **맨 결함 탄소 ↔ 리튬화 결함 탄소 두 끝 (범위)** 으로 · 저자 모식 (`Fig. 8`) 의 CB = '국소 정렬 층 (삽입) + 작용기 (흡착)' → 정렬 부분 끝으로 LiC₆ 기저면을 **이상화된 끝**으로만 / **8-3 문장 수정안**: 'Li\|C (리튬화된 탄소 · LiC₆)' → *'Li\|C (리튬화된 탄소 — 흑연이면 LiC₆, 카본블랙은 Li 양이 정해지지 않았다)'* · 근거로는 '리튬화' 까지 (정성) 쓰고 LiC₆ 근거로는 쓰지 않음 / **집전체 SUS 행 추가 제안** (이 셀 · [우리 그룹] 도 SUS · Cu(111) 만으로는 부족 · SUS 맨 면은 Cr 이 많은 산화막 [일반 지식]) / Li 가 쌓이는 곳 = **Ag/C 와 집전체 사이** (`Fig. S8`) — metzler2026 · metzler2025 와 같은 방향 | `Fig. 8` · `Fig. S8` · p.27961 · p.27966–27967 · digest §0-1 · §7 · §8 | ✅ `Fig. 8` · `S8` (확대) |
| **6. 한계 (Q4)** | **침투 깊이**: 532 nm 는 흑연질 탄소에 수십 nm [일반 지식 · 논문 언급 없음] → CB 1 차 입자 (38 nm) 한두 겹 · 그것도 **잘라서 드러난 면** · **국소성**: ∼1 µm 점 · operando 점 2 개 (셀 1 개) · ex situ 10 점 중 형광 적은 3 점 선택 · **레이저**: 3.2 mW · ✎ ≈4 mW µm⁻² · 같은 자리 19 장 ≈76 min · 가열 · 세기 의존 · OCV 대조 **없음** · **기타**: 셀 셋 다 단면 단락 · 2 대역 맞춤 · 높이 비정규화 · 기준 전극 없음 · 실온 대 318 K | p.27962–27964 · `Fig. S1` · `Fig. 5` · `Fig. S5` · digest §10 | ✅ |
| **7. DEM** | 제조 WIP 490 MPa · 운전 ≈2 MPa (압력 단계 예) · Ag/C 10 µm 대 Li 층 (ex situ 100 % 주석 ≈50 µm · ✎ 치밀 환산 ≈22 µm 의 ≈2.3 배 — 단면 Li 가 성기거나 면적 가정 오류) · operando 단면 부피 변화 ±5 µm (✎ ≈3–3.5 mAh → ≈5–6 µm 와 자릿수 일치) · **구속 없는 면으로 Li 가 새어 SE 균열 · 금속광 석출물 · 단락** (`Fig. 5a`) → DEM 에서 옆면 · 모서리를 자유면으로 두면 같은 인공물 주의 | p.27962–27966 · `Fig. 5` · `Fig. S8` · digest §3-8 ⑨–⑩ · §8 ⑤ | ✅ |

보고서 문장 후보 (공유 보고서 문체 · 출처는 랩 표준 꼴 · 저자 · 소속 이름 없음):
- *카본블랙과 Ag 나노입자로 만든 층도 충전 중 Raman 의 D · G 띠가 바뀌었다가 방전 뒤 대부분 돌아왔다 — 운전 중 Li 금속이 닿는 탄소는 맨 탄소가 아니라 Li 를 받은 탄소로 본다. 그 탄소에 든 Li 의 양 (LiC₆ 인지) 은 정해지지 않았다 (J. Mater. Chem. A, 13, 27960 (2025)).*
- *이 층에서도 Li 금속은 집전체 (스테인리스) 와 Ag/C 층 사이에 쌓였다 (J. Mater. Chem. A, 13, 27960 (2025)).*
- *그래서 Li | C 의 W 는 맨 결함 탄소와 Li 를 받은 결함 탄소 두 끝으로 낸다. 흑연 기저면의 LiC₆ 는 그 끝 상태의 이상화된 모형이다.*
- (8-7 '읽은 논문' 표에 넣는다면) `J. Mater. Chem. A, 13, 27960 (2025) | Ag/카본블랙 층 (스테인리스 집전체) | LPSCl · 무음극 · operando Raman | 7-1 카본블랙 행 · 8-3 리튬화 탄소`

---

## (f) 그림 크롭 요약

- **19 장** = 본문 그림 8 (`Fig. 1`–`8` · `Fig. 1` 만 손 크롭) + SI 그림 8 (`Fig. S1`–`S8`) + SI 표 3 (`Table S1`–`S3`). 본문에는 표가 없어요. 도구 한 번 (`--clean`) + 손 크롭 1 · 다시 자름 0. `missing_labels` 2 = `f1` (해결 · 손 크롭 · p.4 의 이미지 XObject + 캡션 두 줄 · 300 dpi) · `tS4` (SI 에 없음 — 본문 참조 오류 · `resolved` 기록).
- **본 것: 그림 16/16 전부 원해상도** (`Fig. 1`–`8` · `Fig. S1`–`S8`). 확대해서 다시 본 것 (scratchpad · 저장소에 안 남김): `Fig. 2a` 첫 충전 앞부분 · `Fig. 2b` 처음 · 끝 · `Fig. 2c` · `Fig. 3` (1087 · 1854 띠 · 3648 띠) · `Fig. 4a` · `4b` · `4d` · `Fig. S7` (2 h 격자) · `Fig. S8` (초기 · 100 %). **디지털 판독**: `Fig. 4` 전 패널 (표지점 색 · 점 1 충전값으로 축 맞춤 → 표와 0.2–0.9 px 일치) · `Fig. 7` (틀 좌표로 축 맞춤) · `Fig. S1a` (충전 갈래 전류 적분) · `Fig. 2a` (첫 충전 곡선). **표 3 장은 이미지로 안 열고** PDF 글자층으로 옮겼어요 (R · AR 은 거기서 다시 계산).
- **그림이 본문 · 표와 어긋난 것**: `Fig. 4a,b` 점 2 충전 한 칸 밀림 (0.30 V 에 표에 없는 점) · `Fig. 4b` 방전 x 위치 2.00–3.43 V · `Fig. 4a,b,d` 점 2 방전 ≠ `Table S2` · `Fig. 7` ≠ `Table S3` 평균 · `Fig. 2a` 첫 방전 ≈15.0 mAh (본문 '≈16') · `Fig. S1a` 방전 꼭지 ≈3.3–3.4 V (본문 '≈3.6 V') · `Fig. S7` CC 구간으로 읽은 충전 ≈13.5 · 방전 ≈4.5 mAh (본문 '≈10 mAh' · 0.5 mA 가정) · `Fig. 6` 형광 기울기는 낮은 SOC 쪽이 더 큼 (본문 '높은 SOC') · aspect ratio 최대 2.7 V (본문 '2.1–2.4 V') · SI S-8 'Fig. S5 에서 정의' = `Fig. S6` · `Fig. S1` 캡션 (b) 표지 빠짐.
- **임시 파일 점검 (병렬 충돌 주의)**: 글자 · 확대 · 판독 · 검색 결과는 전부 `scratchpad/hiraoka2025_operando_raman_carbon_structure_anode_free_sulfide/` 안에 `hiraoka2025_` 접두 이름으로만 썼어요 (Crossref 응답은 그 안 `crossref/` · 공용 이름 없음). 본문 글자 파일 첫머리 = 이 논문이 실린 호 표지 (*Journal of Materials Chemistry A* · 제목 · Suzuki, Seki et al.) · SI 글자 파일 첫머리 = 이 SI 제목 · PDF sha256 두 개 = `batch.json` 값과 일치 (`71c40010…` · `cc844ba9…`). 확대 그림 내용 (Ag/C Raman · 단면 셀) 도 이 논문 것이었어요.

---

## (g) Jeff Sakamoto 저자 여부

**아니에요** — 저자는 Koji Hiraoka (1저자 · Kogakuin Univ.) · Junichi Sakabe · Naoki Suzuki (교신 · Samsung Device Solutions R&D Japan) · Shiro Seki (교신 · Kogakuin Univ.) 넷이에요. 본문 · SI 글자층 (참고문헌 52 편 + SI S1–S4 포함) 에서 'Sakamoto' 검색 0 건이에요 ('Sakabe' 는 다른 사람). digest 머리말에 그 이름을 쓰지 않았고 웹앱 `_paper_pis` = [] 예요 — INDEX 행에 `🏷 Jeff Sakamoto 공저` 를 달지 않아요.
