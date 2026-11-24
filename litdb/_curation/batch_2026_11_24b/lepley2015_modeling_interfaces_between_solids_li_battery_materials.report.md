# 끝 보고 — lepley2015_modeling_interfaces_between_solids_li_battery_materials (배치 2026-11-24b · #12)

- digest: `litdb/papers/lepley2015_modeling_interfaces_between_solids_li_battery_materials.md` (새 파일 · 503 줄 · 한국어 standalone · §0–§16 · Figure set · Post-processing 표 · 머리 태그 `elements: Li, O, P, S` · `methods: DFT, NEB, DOS, PDOS`)
- 그림: `litdb/figures/lepley2015_modeling_interfaces_between_solids_li_battery_materials/` — 크롭 22 장 (본문 그림 20 + 표 2). 도구 (`--slug … --pdf 본문 --clean`) 가 14 장을 잘랐고, 놓친 8 장 (그림 8 · 11 · 13 · 14 · 15 · 17 = 벡터 그림이라 '영역 없음' · 표 I · II = 로마 숫자 캡션이라 아예 못 찾음) 은 손으로 잘랐어요 (`figures.json` `manual_crop` 사유 · `missing_labels[].resolved`). 전 항목에 `viewed` / `viewed_how` 를 달았어요.
- PDF: `litdb/inbox/lepley2015_modeling_interfaces_between_solids_main.pdf` sha256 `b4fbf0a2…675f0e` = batch.json 값 · 본문 15 쪽 · **SI 없음** (본문이 보충 자료를 가리키지 않아요 — '안 받음' 으로 적을 것도 없어요).
- 공유 파일은 손대지 않았어요. `litdb/figures/_sources.json` 은 추출 도구가 이 slug 항목을 더해 다시 썼어요 (손 안 댐). git 작업 없음 — 메인 checkpoint 커밋 (`98271324` 까지) 에 크롭 22 장 + 지금의 `figures.json` 이 이미 들어가 있고, digest 는 미추적이에요.
- 임시 파일은 전부 `scratchpad/lepley2015_modeling_interfaces_between_solids_li_battery_materials/` 안 (`lepley2015_*.txt` · `tools/lepley_*.py` · `crossref/*.json` · `vec_fig*.txt`) — 공용 이름 없음.
- 점검 (읽기만): `build_index.py --check` → 이 digest 는 "어느 인덱스에도 없음 [dft]" + "comparison_vs_ours 미편입" (아래 (a) · (b) 를 넣으면 풀려요) · `extract_figures.py --inbox --only lepley2015` (매칭표만) → 본문 자동 매칭 `[제목 72%]` · 웹앱 `/paper/<slug>` 200 · `paper_figures` 22 · `paper_figure_notes` 22/22 · `_paper_pis` = [] · 원소 페이지 Li · O · P · S 연결 ✓ · 기법 페이지 dft · neb · dos · pdos 연결 ✓ · 시험 `test_v3_literature` + `test_v3_markdown` 43/43 통과.

⚠ **메인에 알릴 것**
1. **이 논문엔 W (점착 일 · 분리 일) 값이 없어요.** 식 (2) 로 정의만 하고, 표 II 는 변형을 뺀 '정합 극한' 계면 에너지 γ̃^lim (두 벌크 기준 · LDA) 와 전해질 쪽 진공 표면 에너지뿐이에요. Li 금속 표면 에너지가 없어서 Dupré 식이 이 논문 자료로는 안 닫혀요.
2. ⭐ **`yang2021_atomistic_…` 카드의 'Lepley 2015 W' 다섯 개 (Li–Li₂O 1.153 · 1.218 · Li–β-Li₃PO₄ 0.481 · Li–γ-Li₃PO₄ 0.593 · 1.153 J/m²) 는 표 II + γ_Li = 30.0 meV/Å² (0.481 J/m²) 의 Dupré 값이에요** — 다섯 개가 소수 셋째 자리까지 재현돼요 (✎ digest §11b). 그 γ_Li 는 이 논문 밖이에요. 그 카드 §10-④ 의 모순도 이걸로 풀려요 (큰 값 = Li₂O(110) 진공 표면 72 meV/Å² 가 그대로 들어간 것). 카드 라벨 수정 · §I 재귀속 행은 메인이 정해 주세요 ((b-3)).
3. **그림과 표가 어긋나요 (PDF 벡터 경로로 판독)**: `Fig. 8` 맞춤선 절편 −226 대 표 II · 본문 −216 (세 점은 본문 범위 −175 ~ −225 밖) · `Fig. 6` β-Li₃PO₄ 기울기 1.55 대 표 1.8. 작은 것 둘 (`Fig. 2` Ω̃₂ 기울기 0.13 대 0.2 · `Fig. 6` γ(010) 절편 29.6 대 31).
4. **`wang2022_resistive_…` 카드 4a 표의 "Li 12 Å · Na 14 Å (금속은 계면영향이 더 깊다 — ref 26)" 는 이 논문으로 뒷받침되지 않아요** — 이 논문은 반대로 계면 효과가 짧은 거리라고 써요 (첫 Li 층 밖은 벌크 · n_b 가 작아도 직선). Wang 원문 문장은 이번에 안 봤어요.
5. 1 번 보고서 (d) #1 **Kotakadi (ChemRxiv 2025) 는 저널판이 있어요** — *Joule* 9, 102175 (2025) · DOI 10.1016/j.joule.2025.102175 (Crossref 확인).
6. **wishlist 줄 번호가 바뀌었어요**: 이 논문 = 780 줄 (`[본 세션 · 11-24] Lepley, Holzwarth, PRB 2015 92 214201`) → ✅ 처리 가능 · 프롬프트의 '579 줄' (2013 PRB 88, 104103) 은 지금 761 줄이고 다른 편이에요 (digest (d) #7 로 넣었어요).
7. 추출 도구 한계 두 개 (고칠지는 메인 몫): ① 벡터만으로 된 PDOS 그림 6 장을 '영역 없음' 으로 버림 ② `TABLE I.` 같은 로마 숫자 표 캡션을 표로 못 찾음 (`table_caption_vote` 0/0). 웹앱도 로마 숫자 표 참조 (`Table II`) 를 그림 연결하지 못해서 digest 에는 `Table 1` · `Table 2` 로 적고 그 사실을 §0 에 밝혔어요.
8. 🎤 talk 역링크: 해당 없음 — 인입 대기열이 있는 talk (`lee2026_skku_mlip_materials_design`) 에 이 논문이 없어요.
9. 발견 검색 (최근 2 년 먼저): Crossref 주제어 검색 15 번 + DOI · 서지 확인 약 14 번 (일반 UA · 개인정보 없음). OpenAlex · Semantic Scholar 는 프록시가 막아서 '이 논문을 인용한 최근 편' 목록은 못 뽑았어요 — 주제어로만 찾았어요.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 한 묶음)` — 행 순서상 **'판정 기준 · 계면 원자 모형 (DFT · MD)' 묶음 맨 앞** (`seymour2021_…` 행 앞) 을 권해요. 그 묶음의 seymour2021 · yang2021_atomistic 와 `## ✅ Digest 완료` 절의 `wang2022_resistive_…` · 이번 묶음 `baer2026_…` 가 다 이 편을 인용하는 2015 방법 원전이라서요. 절 머리 '18 편 한 묶음' 문구는 11-24b 를 넣을 때 같이 고쳐야 할 거예요 (1 번 보고서 6 번과 같은 얘기).

| `papers/lepley2015_modeling_interfaces_between_solids_li_battery_materials.md` **(본문 15 pp · SI 없음 · 크롭 22 장 (그림 20 + 표 2 · 도구 14 + 손 크롭 8 = 그림 8 · 11 · 13 · 14 · 15 · 17 · 표 I · II) 중 18 장 봄 (그림 16 + 표 2 · 안 본 것 그림 1 · 5 · 12 · 19) · 그림 2 · 4 · 6 · 8 · 10 은 PDF 벡터 경로로 판독 · 2026-11-24)** | **[외부·DFT(QE · LDA · PAW 64 Ry · vdW 없음)·⭐⭐⭐ 고체 \| 고체 계면 에너지 형식론 (변형 외삽 · 정합 극한) 의 방법 원전 · ⛔ W (점착 · 분리 일) 값 0 — 식 (2) 정의만 · Li 표면 에너지 없음]** ✅ **N. D. Lepley**/**N. A. W. Holzwarth\*** (Wake Forest Univ. Physics), "**Modeling interfaces between solids: Application to Li battery materials**" — ***Phys. Rev. B* 92, 214201 (2015)** (DOI 10.1103/PhysRevB.92.214201 · NSF DMR-1105485) — 주기 셀의 계면 에너지 γ̃ 를 변형된 쪽의 양 n_b 로 직선 외삽해 **γ̃ = γ̃^lim + n_b·σ** (식 6) · γ̃^lim = 변형을 뺀 정합 극한 = 참값의 **하한** (식 7) · 셀 안 계면 둘이라 A = 두 면 합 (계면 하나당 값). **Li \| Li₂S 네 배치 47 · 11 · 19 · 19 meV/Å² (σ 4.0 · 4.0 · 0.2 · 0.0)** — 최저 11 은 '심하게 변형된' 배치 · (110) 과 극성 (100) 이 Li 와 닿으면 같은 19 · Li \| Li₂O 30 · 26 · Li \| β/γ-Li₃PO₄ 39 · 33 · 31 · **γ-Li₃PS₄ \| Li −216 (0 K 이완 중 분해 → Li₂S 비슷한 부동태층 · 반응 에너지 · 그림 ≈ −226)** · γ-Li₃PS₄ \| Li₂S 16 · 전해질 진공 표면 Li₂S (110) 41 · (100) 162 · Li₂O (110) 72 … (1 meV/Å² = 16.02 mJ/m²). PDOS 로 계면 P 환원 · Li⁺ 침입 2.1 eV (전자는 금속에 남음 · 전기장 0.54 / 0.27 eV/Å) · P–O 끊기 NEB ≈ 3 eV (인위적 Li 비용). 🔴 **그림–표 불일치**: `Fig. 8` 절편 −226 대 표 −216 · `Fig. 6` β 기울기 1.55 대 표 1.8. ⭐ **`yang2021_atomistic_…` SI `Table S1` 의 'Lepley W' 5 개 = 표 II + γ_Li 30.0 meV/Å² 의 Dupré 값 (✎ 재현)** · `wang2022_…` 의 '금속은 계면영향이 더 깊다 (ref 26)' 는 이 논문과 반대. ⛔ A–D 4축 금지 · 우리 W_sep 과 같은 줄 금지. | **방법 원전 — 계면 에너지 (변형 외삽) · Dupré 정의 · 반응 계면 판별 (W 값 없음)** |

---

## (b) `comparison_vs_ours.md` · `comparison_vs_ours_DEM.md` 에 넣을 줄

**A–D 물성 4축: 본 자리 없어요** (방법 원전 · 우리 계 값 0 · LDA). 판정은 §E 1 행 + §I 1 행 + §J 블록, 점착 트랙은 DEM 쪽 §I 블록.

### b-1. `📑 Reference key` 표에 한 행 (4 칸: 약칭 | 논문 | digest/status | 유형)

| **[Lep15Int]** 🔧 **고체 \| 고체 계면 에너지 형식론 — 변형 외삽 (γ̃ = γ̃^lim + n_b σ) · 정합 극한 = 하한 · Li \| Li₂O · Li₂S · β/γ-Li₃PO₄ · γ-Li₃PS₄ + γ-Li₃PS₄ \| Li₂S** · ⛔ **W 값 0 · Li 표면 에너지 0 — W 로 인용 금지** · ⛔ **A–D 4축 진입 금지** | N. D. Lepley/N. A. W. Holzwarth\* (Wake Forest) 2015 ***Phys. Rev. B* 92, 214201** (DOI 10.1103/PhysRevB.92.214201) — "Modeling interfaces between solids: Application to Li battery materials" | ✅ `papers/lepley2015_modeling_interfaces_between_solids_li_battery_materials.md` — 판정은 §E 1 행 + §I 1 행 + §J (방법) | DFT (QE · LDA · PAW) · 실험 0 |

### b-2. §E 표에 한 행 (4 칸: 주장 | 출처 | 우리 | 일치)

| **🆕 (2026-11-24) γ-Li₃PS₄ \| Li 는 0 K DFT 이완만으로 분해 (계면 PS₄ 파괴 → Li₂S 비슷한 층 · P 환원) · '계면 에너지' −216 meV/Å² (반응량 따라 −175 ~ −225 · 그림 ≈ −226) · Li₂S \| Li (σ ≈ 0 배치 19) · γ-Li₃PS₄ \| Li₂S (16) 는 반응 없음 → 부동태층 · Li₃PS₄ + 8Li → Li₃P + 4Li₂S 발열 12.30 eV** — ⚠ LDA · 0 K · 부동태층 크기 과소 (저자) · '안정' = 장벽 없는 분해가 안 보였다 (Li₃PO₄ \| Li 도 열역학적으론 불안정 · NEB ≈ 3 eV 로 보호) | **[Lep15Int]** `Table 2` · `Fig. 7` · `Fig. 8` · `Fig. 16` · `Fig. 17` · 식 (10) · (11) (QE · LDA · PAW 64 Ry) | 우리 grand-potential 환원 한계 1.717 V · 0 V 산물 Li₂S + Li₃P + LiCl (`litdb/our_dft_baseline.md`) | ✅ **방향 일치** (PS₄ 골격은 Li 와 닿으면 P 가 환원) · 수치 비교 없음 (계 · 방법 다름) · 🔀 [Baer26LiArg] (같은 꼴 Li \| LPSCl · 음의 γ_inter) · [Wang22Res] (분해 뒤 산물 계면) |

### b-3. §I 표 (출처 재귀속) 에 한 행 (5 칸: 우리가 쓰던 것 | 붙어 있던 출처 | 원문 실물 | 판정 | 조치)

| `yang2021_atomistic_li_stripping_plating_interface_md` §3g · §10-④ · 411 줄 — 'Li–Li₂O [110] 1.153 · 1.218 · Li–β-Li₃PO₄ [010] 0.481 · Li–γ-Li₃PO₄ [100] · [010] 0.593 · 1.153 J/m²' (문헌 DFT W 표 · '우리 Li/Ag · Li/흑연 계산의 문헌 대조') | **[Lep15Int]** (Yang SI ref 3) | ✅ **원문에는 W 값이 없다** (식 (2) 정의만) — `Table 2` 의 전해질 진공 표면 · γ̃^lim 에 **γ_Li = 30.0 meV/Å² (0.481 J/m² · 논문 밖)** 를 넣은 Dupré 값으로 다섯 개가 소수 셋째 자리까지 재현된다 (✎ ×16.02 · 다섯 개가 요구하는 γ_Li 29.97–30.03) | 🔴 **출처 라벨 틀림** — 'Lepley 계산 W' 가 아니라 'Lepley 표로 만든 W' (LDA · 계면 · 표면 모두 이완 · 가정 γ_Li) | 라벨: 'Lepley 2015 표 II 로 Dupré 를 닫은 값 · γ_Li ≈ 0.48 J/m² 가정 (Yang SI 에서 출처 확인 필요)' · 우리 W 대조 표로 쓰지 않는다 · 카드 수정은 메인이 |

### b-4. §J 끝에 블록 (지금 J-91 · 이번 묶음 다른 보고서가 J-92 를 제안했으니 **J-9x — 번호는 메인이** 정해 주세요)

### J-9x. 🔧 **방법 원전 — [Lep15Int] 고체 \| 고체 계면 에너지: 주기 셀 변형을 n_b 외삽으로 떼는 '정합 극한' γ̃^lim (참값의 하한) · W 는 정의만 · 반응 계면은 음의 γ** (2026-11-24 신설)

📎 **출처**: `papers/lepley2015_modeling_interfaces_between_solids_li_battery_materials.md` (그림 16 + 표 2 봄 · 그림 2 · 4 · 6 · 8 · 10 벡터 판독 · §11b 인용 카드 답)

⛔ **A–D 물성 4축 표에 행을 만들지 않는다** (LDA · 우리 계 값 0) — 판정은 §E 1 행 · §I 1 행. 우리 W 값은 위치만 (W_ad 보고서 · `db/properties/adhesion.json` · `db/properties/wad_*`).

| 항목 | [Lep15Int] 가 보이는 것 | 우리 현재 | 판정 |
|---|---|---|---|
| 싣는 양 | γ̃^lim = 두 벌크 기준 계면 에너지 − 변형 (식 4–6) · W 는 식 (2) 정의만 | 고정 기하 W_sep (붙은 상태 − 10 Å 뗀 상태) | ⛔ 같은 표 금지 |
| 변형 | 셀 면내 = 전해질 벌크 · Li (또는 Li₂S) 가 변형 · n_b 3–6 점 직선 외삽 (맞춤 오차 1–3 %) · 명시 변형 계산과 41 대 39 | 같은 변형 슬랩끼리 빼서 벌크 변형 상쇄 | 🔑 '변형 몫' 을 따로 싣는 법 (σ) 은 옮길 만 — ✎ Li₂X 를 본뜬 Li 는 σ ≈ 0.35 eV/Li |
| 하한 · 오차 | γ̃^lim ≤ γ ≤ γ̃ (식 7) — 전위 에너지 빠짐 · 최저 Li \| Li₂S 값 (11) 이 σ 4.0 배치 | registry 범위 · 끝점 점검 | 🔑 '최저값 = 대표값' 아님 — 집계 규칙을 결과 전에 |
| 배치 탐색 | 정렬 출발 + 무작위 잡음 출발 (≈ 1 Å) · 판정 규칙 'γ̃^lim 과 σ 둘 다 작은 배치' | registry 여럿 평균 | 다른 집계 규칙 |
| 두께 수렴 | n_b 직선이 작은 n_b 부터 성립 = 짧은 거리 · 전해질 3 층 넘으면 무시 | 끝점 10 → 12 Å · Ag–C 3 → 4 층 · LPSCl 쌍 두께 연속 점검은 보고서 부록 A 에 없음 | 🔑 우리 빈칸 |
| Dupré | 열려 있지만 Li 표면 에너지 없음 · 대표 배치의 Li 가 정의된 면이 아님 · ✎ Li₂S (110) 대 극성 (100) 기준면 차 121 meV/Å² ≈ 1.94 J/m² | 7 절 Young–Dupré · 'γ_Li 는 같은 방법 · 같은 Li 면' | ✅ 우리 원칙과 같은 경고 — 기준면이 W 를 지배할 수 있다 |
| 반응 계면 | γ-Li₃PS₄ \| Li 음의 γ (반응 에너지) · PDOS 로 P 환원 | Li \| LPSCl 쌍 없음 | 🔑 반응 계면은 상태 선언 없이는 W 가 정의 안 됨 ([Baer26LiArg] 와 같은 결론) |
| 범함수 | LDA · vdW 없음 · 범함수 영향은 '격자 −2 %' 한 줄 | PBE + D3(BJ) | ⛔ 크기 비교 성립 안 함 |

**인용 위생**: `Fig. 8` 절편 · `Fig. 6` β 기울기는 표와 어긋나 소수 자릿수 인용 금지 · −216 은 계면 에너지 크기 비교 금지 · NEB ≈ 3 eV 는 인위적 Li 비용 경로 (홉 수 검산 3 eV · 298 K · ν₀ 10¹³ s⁻¹ 가정 → 평균 대기 ≈ 5.4 × 10³⁷ s — '동역학 장벽' 서술과 차수 모순 없음) · 띠 정렬 3.4 대 OCV 3.45 는 방법이 다른 두 계산을 이은 것 — 검증으로 인용 금지.

### b-5. (권장 · 점착 트랙의 집) `comparison_vs_ours_DEM.md` §I 에 블록 (지금 I-22 · 다른 보고서가 I-23 을 제안했으니 **I-2x — 번호는 메인이**)

### I-2x. `lepley2015_modeling_interfaces_between_solids_li_battery_materials` — ★★★ (DFT · 방법 원전 · ⛔ W 값 없음) **계면 에너지의 변형 외삽 (정합 극한 = 하한) · 'Lepley 의 W' 는 남이 Dupré 로 만든 것**

- **무엇**: 주기 셀 계면 에너지 γ̃ 를 변형된 쪽 양 n_b 로 직선 외삽 → 절편 γ̃^lim (변형 뺀 계면 에너지 · 참값의 하한) · 기울기 σ (변형). Li \| Li₂S 네 배치 47 · 11 · 19 · 19 meV/Å² · Li \| Li₂O 30 · 26 · Li \| Li₃PO₄ 39 · 33 · 31 · Li₃PS₄ \| Li₂S 16 · Li₃PS₄ \| Li −216 (반응) (LDA · 1 meV/Å² = 16.02 mJ/m²).
- **점착 트랙에 주는 것 셋**: ① W_ad 보고서 8 절에 Li \| Li₂S 문헌값을 넣는다면 이 편은 '계면 에너지 (변형 외삽 · LDA)' 로만 — W 칸에는 W 를 직접 계산한 `wang2022_…` (이완 W · 식 4) · `seymour2021_…` (이완 W) 를 그 정의와 함께 ② Young–Dupré 를 쓸 때 기준 표면이 W 를 지배할 수 있다 — 같은 계면 에너지 (19) 인데 Li₂S (110) 대 극성 (100) 기준이면 ✎ W 차 ≈ 1.94 J/m² ③ 배치 · registry 집계 규칙과 '변형 지표' 를 결과 전에 정한다 — 최저 γ̃^lim 이 가장 억지스러운 배치였다.
- **DEM 쪽 쓰임**: 값을 넘기지 않는다 (LDA · W 아님). 방법만 — 우리 W_sep 에 '변형 몫' · 두께 연속 점검을 더할 근거.
- **금지**: 'Lepley W' 인용 · γ̃^lim 을 W 와 같은 줄 · −216 을 계면 에너지 크기로 · `yang2021_atomistic_…` `Table S1` 의 [3] 다섯 행을 '계산 W' 로.

---

## (c) `pdf_map.tsv`

**필요 없어요** — `extract_figures.py --inbox --only lepley2015` (매칭표만) 가 본문을 자동으로 붙였어요 (`[제목 72%]`). 굳히고 싶으면 한 줄:

```
lepley2015_modeling_interfaces_between_solids_li_battery_materials	lepley2015_modeling_interfaces_between_solids
```

---

## (d) 추가로 먹일 논문 (≤ 8 · 최근 먼저)

> 대조: `litdb/papers` 파일 이름 + digest 본문 grep · `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md` grep (아래 여덟 다 '목록에 없음'). 서지는 전부 Crossref (api.crossref.org/works) 로 맞췄어요 — 제목 · 첫 저자 · 저널 · 권 · 쪽(번호) · 연도. 출판사 페이지 · 본문은 안 열었어요.
> litdb 에 이미 있는 이웃 (세지 않음): `wang2022_resistive_…` · `seymour2021_…` · `yang2021_atomistic_…` · `baer2026_…` · `lai2025_haml_li_metal_lpscl_interface_doping_seFO` (검색에 걸렸지만 이미 digest).

| # | 문헌 | 왜 (우리 축) | litdb | 목록 |
|---|---|---|---|---|
| 1 | Liu X., Yi X., Dou R., Wen Z., Liu X. · *J. Phys. Chem. C* 130, 10812 (2026) — *"Unraveling the Dual Role of Li3P at the Li/Li6PS5Cl Interface: First-Principles Insights into Electronic Self-Confinement and Fast Ion Transport"* · DOI 10.1021/acs.jpcc.6c03055 | Li \| LPSCl 분해산물 (Li₂S · Li₃P · LiCl) 계면 DFT + AIMD — 이 편 Li₂S \| Li 의 최신 후속 · 음극 계면 전자 차단 축 | 없음 | 없음 |
| 2 | Kotakadi, Aspinall, Burton, Liang, Aihara, Pasta · *Joule* 9, 102175 (2025) — *"Impact of metallic interlayers at the lithium-Li6PS5Cl solid electrolyte interface"* · DOI 10.1016/j.joule.2025.102175 | W_ad 7 절 금속 인터레이어를 Li \| LPSCl 에서 직접 — 1 번 보고서 (d) #1 의 ChemRxiv 판이 저널에 실림 | 없음 | 1 번 보고서 (d) #1 (ChemRxiv 판으로) |
| 3 | Zhang J., Zhang H., Chen B., Ji Y., Qian C., Wang J., Wang Y., Bao T. … · *Batteries* 11, 456 (2025) — *"First-Principles Calculation Study on the Interfacial Stability Between Zr and F Co-Doped Li6PS5Cl and Lithium Metal Anode"* · DOI 10.3390/batteries11120456 | 도핑 LPSCl \| Li 계면 DFT — 우리 도핑 축과 음극 계면이 만나는 곳 | 없음 | 없음 |
| 4 | Orlandi, Li J., Kenny, Martinez · *ACS Appl. Mater. Interfaces* 17, 21958 (2025) — *"Atomic Structure of the Lithium–Lithium Oxide Interface from First Principles"* · DOI 10.1021/acsami.4c22106 | 이 편 Li₂O \| Li 배치 탐색의 최신 후속 — Li₂O 는 SEI 내층 · W_ad 8-5 '반응 뒤 표면 (Li₂O)' | 없음 | 없음 |
| 5 | Marana, Ascrizzi, Silveri, Sgroi, Maschio, Ferrari · *Materials* 18, 3515 (2025) — *"A Theoretical Raman Spectra Analysis of the Effect of the Li2S and Li3PS4 Content on the Interface Formation Between (110)Li2S and (100)β-Li3PS4"* · DOI 10.3390/ma18153515 | 이 편 Li₃PS₄ \| Li₂S 계면의 최신 후속 (β 상 · DFT) — SEI \| 황화물 계면 | 없음 | 없음 |
| 6 | Wang Z., Xiao R., Li H., Chen L. · *J. Materiomics* 12, 101309 (2026) — *"Comparative study of the interfacial behaviors of oxides and fluorides with lithium metal anodes from first principles"* · DOI 10.1016/j.jmat.2026.101309 | Li \| 산화물 · 불화물 계면 DFT — SEI 성분 계면의 비교 기준 | 없음 | 없음 |
| 7 | Lepley, Holzwarth, Du · *Phys. Rev. B* 88, 104103 (2013) — *"Structures, Li⁺ mobilities, and interfacial properties of solid electrolytes Li3PS4 and Li3PO4 from first principles"* · DOI 10.1103/PhysRevB.88.104103 | 이 편 ref 13 · Li₃PS₄ 표면 에너지 0.320 J/m² 원전 (`damore2022_…` 카드의 '면당 · 두 면 미확인' 칸) · Li₃PS₄ \| Li · Li₃PS₄ \| Li₂S 첫 계면 | 없음 (인용 카드 다수) | wishlist 761 줄 |
| 8 | Finnis · *J. Phys.: Condens. Matter* 8, 5811 (1996) — *"The theory of metal - ceramic interfaces"* · DOI 10.1088/0953-8984/8/32/003 | 이 편 ref 2 · '분리 일 (끝 상태 = 이상 표면) 대 점착 일 (확산 · 뒤틀림 포함)' 정의 원전 — 우리 'W_sep' 이름의 뿌리 | 없음 | 없음 |

다음 순번: Benedek, Seidman, Woodward · *J. Phys.: Condens. Matter* 14, 2877 (2002) — "The effect of misfit on heterophase interface energies" · DOI 10.1088/0953-8984/14/11/307 (ref 3) · Camacho-Forero & Balbuena · *J. Power Sources* 396, 782 (2018) — "Exploring interfacial stability of solid-state electrolytes at the lithium-metal anode surface" · DOI 10.1016/j.jpowsour.2018.06.092 (1 번 보고서 '다음 순번').

---

## (e) DEM-DFT 보고서 (W_ad 보고서) 에 쓸 거리

보고서 1 절 (W 정의) · 6 절 (한계) · 7 절 (Young–Dupré) · 8 절 (문헌) · 부록 A (방법) 를 먼저 읽고 맞췄어요. 보고서 HTML 에는 지금 Li₂S 가 한 번도 안 나와요 (글자 검색 0) — 8 절에 Li \| Li₂S 문헌값을 넣는다면 아래 2 번 표의 정의를 같이 달아야 해요.

| 보고서 항목 | 이 논문에서 쓸 점 | 위치 (쪽 · 그림 · 표) | 직접 봤나 |
|---|---|---|---|
| **1. W 정의 (1 절 · 부록 A — 고정 기하 W_sep · registry 평균)** | **식 전부**: (1) γ_ab = [E_ab − n_a E_a − n_b E_b]/A (두 **벌크** 기준) · (2) W_ab = γ_a,vac + γ_b,vac − γ_ab (정의만 · Finnis 각주: 분리 일 = 끝 상태 이상 표면 · 점착 일 = 확산 · 뒤틀림 포함) · (4) 주기 셀 γ̃ (A = 두 계면 합 → 계면 하나당) · (5) γ̃^lim = γ̃ − Ẽ_str/A · (6) γ̃ = γ̃^lim + n_b σ (외삽) · (7) γ̃^lim ≤ γ ≤ γ̃. **차이 표 (digest §7a)**: 기준 상태 (벌크 대 뗀 슬랩) · 변형 (외삽 대 상쇄) · 이완 (계면 · 표면 다 이완 대 뗀 상태 고정) · 면적 (같음) · 두께 (n_b 직선 대 끝점 10 → 12 Å) · 배치 (대표 선택 대 registry 평균) · LDA 대 PBE+D3 | 식 (1)–(7) p.2–3 · 각주 1 p.2 · 셀 만들기 p.3–4 · `Table 2` p.4 | ✅ PDF 2–4 쪽 렌더 + `Table 2` 크롭 + 글자층 |
| **Dupré 판정** | 🟡 **정의상 열림 · 자료로는 안 닫힘 · 닫으면 다른 부류**: Li 금속 진공 표면 에너지가 표에 없고, σ 가 작은 '대표' 배치 (Li₂S Ω̃₃ · Ω̃₄) 의 Li 는 무작위 출발 구조라 γ_Li 를 넣을 면이 없다 · 닫으면 'LDA · 이완 · 변형 제외' 의 이완 W_ad (정의상 W_sep(고정) ≥ W_ad(이완)) · ✎ 같은 γ̃^lim 19 인데 기준면 Li₂S (110) 41 대 극성 (100) 162 → Li 쪽이 같다면 W 차 121 meV/Å² ≈ 1.94 J/m² · 실제로 닫은 선례 = yang2021 `Table S1` (γ_Li 30.0 meV/Å² 가정 · 메인 알림 2) | `Table 2` · p.5–6 (Ω̃₃ 'not closely related to any readily identifiable Li structure') · p.9 (극성면) | ✅ |
| **2. 8 절 — 문헌 Li \| Li₂S 값의 정의** | 이 논문 = **계면 에너지** (W 아님): Li₂S (110) Ω̃₁ 47 · Ω̃₂ 11 · Ω̃₃ 19 · (100) Ω̃₄ 19 meV/Å² (✎ 0.75 · 0.18 · 0.30 · 0.30 J/m²) · σ 4.0 · 4.0 · 0.2 · 0.0 · 셀 면내 5.57 × 7.88 Å · Li = 사방정 (Li₂S 속 Li) · 무작위 출발 · LDA · vdW 없음 · 원자 + 법선 셀 이완. 비교 (digest §7b · **같은 줄 금지**): wang2022 = 이완 W_adh 식 4 (γ_A + γ_B − σ · 구속 벌크 기준 · PBE · Li₂S (110) · (111)) · seymour2021 = 이완 W_ad (분리 슬랩 각각 이완 · PBE · Li₂S (111) 비정합) · baer2026 = γ_inter (Li \| LPSCl · 반응 포함 · Li₂S 계면 없음). 계면 에너지끼리는 셋 다 0.2–0.5 J/m² 차수 (wang σ 0.32–0.46 · seymour ✎ γ_i ≈ 0.42) · ⚠ 이 논문은 Li₂S 최저면 (111) 이 없다 · Li₂S (110) 진공 표면 LDA 0.657 대 wang PBE 0.51 J/m² (✎ +29 %) | `Table 2` · `Fig. 3` · `Fig. 4` · p.5–6 | ✅ `Fig. 3` · `Fig. 4` 크롭 (+ 벡터 판독 · 표와 소수 첫째 자리 일치) |
| **3. 6 절 한계 · registry** | 식 (7) 의 '상한 − 하한' 을 면내 셀 오차로 쓰는 생각 · **최저값 ≠ 대표값** — Li \| Li₂S 최저 11 이 σ 4.0 '심하게 변형된 모형' · 판정 규칙 'γ̃^lim 과 σ 둘 다 작은 배치' (p.9) · 결론 문장 (p.14 '작은 γ̃^lim = 더 물리적') 은 이 규칙과 어긋남 · 어긋남 5 % 인데 자리 어긋남으로 계면이 무너진 예 (β-Li₃PO₄ \| bcc Li) | p.9 · p.11 · p.13 · p.14 | ✅ 글자층 · `Fig. 4` |
| **4. 부록 A — 두께 · 이완 · 변형** | 두께: γ̃ 대 n_b 가 작은 n_b 부터 직선 (맞춤 오차 1–3 %) = 계면 효과는 짧은 거리 · 전해질 3 층 넘으면 무시할 만 · 변형 교차 점검: 외삽 39 대 명시 변형 슬랩 41 (β-Li₃PO₄) · 극성면 쌍극자 보정 = 값 그대로 · ⇒ 우리 LPSCl 쌍엔 두께 연속 점검이 부록 A 에 없다 (Ag–C 만 3 → 4 층) — 이 논문의 n_b 2–3 점 직선이 그 점검 꼴 | p.3–4 · p.7 · p.8–9 · `Fig. 2` · `Fig. 6` | ✅ `Fig. 2` · `Fig. 6` 크롭 + 벡터 판독 |
| **5. 7 절 Young–Dupré · γ_Li 짝** | 이 논문엔 γ_Li 가 없고 Li 쪽이 정의된 면이 아니라 cos θ = W/γ_Li − 1 에 넣을 짝이 없다 — 보고서 7 절의 'γ_Li 는 같은 방법 · 같은 Li 면' 원칙이 왜 필요한지 보여 주는 반례 | p.4–6 | ✅ |
| **6. 반응 계면 (8-6 'LPSCl 은 Li 와 반응')** | γ-Li₃PS₄ \| Li 는 0 K 이완만으로 PS₄ 가 깨져 Li₂S 비슷한 층 · 음의 γ̃ (−216 · 그림 ≈ −226 · 반응량 따라 −175 ~ −225) · PDOS 로 P 환원 (P 전도띠 상태가 E_F 아래로) · Li₂S \| Li 와 Li₃PS₄ \| Li₂S 는 반응 없음 → 부동태층 · 저자: '음의 계면 에너지 = 점착력 > 응집력 = 화학적으로 활발한 계면의 지표' | p.7–9 · `Fig. 7` · `Fig. 8` · `Fig. 16` · `Fig. 17` | ✅ 크롭 넷 + `Fig. 8` 벡터 판독 |
| **7. (참고) 음극 쪽 전자 차단** | Li₂S \| Li 의 E_F 가 Li₂S 전도띠 바로 아래 (✎ E_F 2.46–2.92 eV 대 CB 바닥 figure-read ≈ 3.0 eV · LDA) · Ω̃₁–Ω̃₃ 은 표면층만 전도띠 점유 — LDA 띠틈 과소라 실제 여유는 더 크다 | `Fig. 11` · `Fig. 14` · p.11 | ✅ |

보고서 문장 후보 (공유 보고서 문체 · 내부 사정 없음 · 출처는 랩 표준 꼴):
- *격자가 맞지 않는 계면 셀에는 억지로 맞춘 변형 에너지가 같이 들어간다. 변형된 쪽의 두께를 바꿔 재고 두께 0 으로 외삽하면 변형을 뺀 계면 에너지를 얻는데, 이 값은 실제 계면 에너지의 하한이다 (Phys. Rev. B, 92, 214201 (2015)).*
- *Li | Li₂S 계면 에너지 계산값은 원자 배치에 따라 0.18–0.75 J/m² 로 갈리고, 변형이 작은 배치는 0.30 J/m² 근처다 (LDA · Phys. Rev. B, 92, 214201 (2015)). 점착 에너지가 아니라 계면 에너지라서 이 보고의 W 와 나란히 두지 않는다.*
- *계면 에너지로 점착 에너지를 만들 때 (Dupré 식) 는 기준 표면을 무엇으로 두느냐가 값을 크게 바꿀 수 있다 — 같은 Li | Li₂S 계면 에너지에서 Li₂S 의 극성면을 기준으로 쓰면 점착 에너지가 2 J/m² 가까이 커진다 (Phys. Rev. B, 92, 214201 (2015) 의 표면 에너지로 어림).*
- *Li₃PS₄ 는 Li 와 닿으면 0 K 이완만으로 분해해 Li₂S 와 비슷한 층을 만들고 계면 에너지가 음수가 된다 (Phys. Rev. B, 92, 214201 (2015)). 반응하는 계면의 점착 에너지는 반응 전 · 후 어느 상태인지 정해야 정의된다.*

**인용 카드에 돌려줄 답** (`grep -l "Lepley" litdb/papers/*.md` 열 편 중 이 편을 인용한 넷 · 남의 카드는 안 고쳤어요 · 상세는 digest §11b):
1. `yang2021_atomistic_li_stripping_plating_interface_md` §3g · §10-④ · 411 줄 — [3] 다섯 값은 이 논문의 W 가 아니라 표 II + γ_Li 30.0 meV/Å² 의 Dupré 값 → 라벨 고침 · §10-④ 모순은 Li₂O(110) 진공 표면 (1.153 J/m²) 이 그대로 들어간 탓 · '우리 계산의 문헌 대조' 로 쓰지 않기.
2. `seymour2021_void_suppression_interfacial_adhesion_vacancy_transport` (d) #3 — '산화물 · 인산염 W 의 선행 보고' 가 아니라 계면 에너지 (변형 외삽) · 진공 표면 에너지 보고 · 내용은 이 digest 로.
3. `wang2022_resistive_decomposing_interfaces_se_alkali_metal` 계보 · INDEX 행 — 계 목록 맞음 (정확히는 Li₂O · Li₂S · β/γ-Li₃PO₄ · γ-Li₃PS₄ + γ-Li₃PS₄ \| Li₂S) · '상위 앵커' 는 방법 (식 1–7) 원전이라는 뜻으로만 · 4a 표 '금속은 계면영향이 더 깊다 — ref 26' 은 이 논문과 반대 (짧은 거리).
4. `baer2026_li_metal_argyrodite_interface_stability_transport` 219 줄 — ✅ p.9 문장과 맞음 (−216 · 그림 ≈ −226) · 단 Li₃PS₄ 는 Li 쪽 분해산물이 아니라 LPSCl 의 산화 쪽 산물 · 같은 PS₄ 골격의 대리 계 · '다음 순번' 의 이 편은 이제 digest 있음.
5. (번외 · 2013 편 인용) `damore2022_lpscl_symmetry_breaking_surface_energy_wulff_pbe0` 199 줄 '면당 · 두 면 미확인' — 이 편의 규약은 A = 두 면 합 → 면 하나당 · 표 II γ-Li₃PS₄[010]/vac 20 meV/Å² = ✎ 0.320 J/m² 로 같은 숫자 (같은 계산인지는 2013 원문을 봐야).
나머지 다섯 (`deklerk2018_…` · `haruyama2014_…` · `haruyama2017_…` · `lai2020_…` · `okuno2020_…`) 은 2013 · 2012 Lepley 를 인용해서 돌려줄 답이 없어요.

---

## (f) 그림 크롭 요약

- **22 장** = 본문 그림 20 (`Fig. 1`–`20`) + 표 2 (`Table 1` = TABLE I · `Table 2` = TABLE II). 도구 14 장 (`--slug … --pdf 본문 --clean`) + **손 크롭 8 장**: 그림 8 (p.7 · 도구 '그래픽 없음(img0/draw5)') · 그림 11 · 13 · 14 · 15 · 17 (p.9–12 · '영역 없음' — 셋 다 벡터 PDOS · 경로 수 152–792) · 표 I · II (로마 숫자 캡션 · `table_caption_vote` 0/0). 클립 = 벡터 경로 묶음 + 축 글자 + 여백 (표는 캡션 위 ~ 아래 이중선 아래) · 손 크롭 8 장은 가장자리에 걸린 어두운 화소 0 으로 점검 (표 둘은 처음에 아래 이중선이 잘려 다시 잘랐어요). `figures.json` `manual_crop` · `missing_labels[].resolved` 에 사유를 적었어요.
- **본 것 18/22**: 그림 16 (`Fig. 2` · `3` · `4` · `6` · `7` · `8` · `9` · `10` · `11` · `13` · `14` · `15` · `16` · `17` · `18` · `20`) + 표 2 (크롭 + PDF 쪽 렌더 2–4 쪽 + 글자층). **안 본 것 4**: `Fig. 1` · `5` (구조도) · `Fig. 12` (벌크 Li PDOS) · `Fig. 19` (전기장 보정 PDOS) — 내용은 본문 글자로만 적었어요.
- **벡터 판독**: `Fig. 2` · `4` · `6` · `8` · `10` 의 마커 중심 · 맞춤선 끝점 (점 44 개 · 선 11 개) 과 `Fig. 13` · `14` · `15` 의 E_Fermi 세로선 위치를 PDF 경로에서 읽었어요 (digest §3c · §3d).
- **그림이 본문 · 표와 어긋난 것**: `Fig. 8` 절편 −226 대 표 −216 (점들은 본문 범위 밖) · `Fig. 6` β 기울기 1.55 대 표 1.8 · `Fig. 2` Ω̃₂ 0.13 대 0.2 · `Fig. 6` γ(010) 절편 29.6 대 31 · `Fig. 13` (a)−(b) E_F 차 0.60 eV 대 본문 '0.8 eV' (본문이 가리킨 `Fig. 11` (a) 는 벌크 Li₂O 라 대조 대상도 모호) · 본문 'bulk γ-Li₃PS₄ shown in Fig. 16' 은 `Fig. 11` (d).
- **동영상**: 없음.
- **임시 파일 점검 (병렬 충돌 주의)**: 글자 · 스크립트 · 검색 결과는 전부 `scratchpad/lepley2015_modeling_interfaces_between_solids_li_battery_materials/` 안에 `lepley2015_` · `lepley_` 접두 이름으로만 썼어요 · 글자 파일 첫 줄 = 이 논문 머리 (*PHYSICAL REVIEW B 92, 214201 (2015)* · 제목) · PDF sha256 = batch.json 값.

---

## (g) Jeff Sakamoto 저자 여부

**아니에요** — 저자는 N. D. Lepley · N. A. W. Holzwarth (교신) 둘 (Wake Forest University 물리학과 · Crossref 저자 메타도 같아요). 참고문헌 50 편에도 Sakamoto 이름은 없어요 (본문 글자층 검색 0 건). batch.json `jeff_sakamoto: false` 와 같고, digest 머리말에 그 이름을 쓰지 않았어요 (웹앱 `_paper_pis` = []) — INDEX 행에 `🏷 Jeff Sakamoto 공저` 를 달지 않아요.
