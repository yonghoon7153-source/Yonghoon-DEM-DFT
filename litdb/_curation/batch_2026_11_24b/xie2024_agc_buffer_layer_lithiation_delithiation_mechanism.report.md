# 끝 보고 — xie2024_agc_buffer_layer_lithiation_delithiation_mechanism (배치 2026-11-24b · #11)

- digest: `litdb/papers/xie2024_agc_buffer_layer_lithiation_delithiation_mechanism.md` (새 파일 · 536 줄 · 한국어 standalone · §0–§15 · Figure set 26 행)
- 그림: `litdb/figures/xie2024_agc_buffer_layer_lithiation_delithiation_mechanism/` — 크롭 26 장 (본문 그림 12 · SI 그림 7 · 본문 표 3 · SI 표 4) = 도구 23 + **다시 자름 3** (`Table S1`–`S3`) · 번호 공백 0 (`missing_labels` = []). `figures.json` 에 26 항목 전부 `viewed` / `viewed_how` 를 달았고, 캡션은 잘림 · 추출 잔재만 고쳤어요 (원문은 `caption_raw` 14 개에 남김).
- 입력 PDF: `litdb/inbox/xie2024_agc_buffer_lithiation_mechanism_main.pdf` · `…_SI.pdf` — sha256 둘 다 `batch.json` 11 번 값과 일치 (`4253d2e2…` · `2a10ebad…`).
- 공유 파일은 안 건드렸어요. `litdb/figures/_sources.json` 은 추출 도구가 이 slug 를 더해 다시 썼어요 (도구 동작 · 손 안 댐). git 작업 없음 (batch 규칙) — 메인 세션 checkpoint 커밋 `31cae0a5` · `482f1aa9` 에 그림 폴더 (크롭 26 장 + 다시 자른 표 셋 + 캡션 고친 `figures.json`) 가 이미 들어가 있고 (작업 트리와 차이 없음), **digest 와 이 보고는 미추적**이에요.
- 점검 (읽기만): `build_index.py --check` → 이 digest 는 '어느 인덱스에도 없음 [dft]' + 'comparison_vs_ours 미편입' (아래 (a) · (b) 를 넣으면 풀려요) · `extract_figures.py --inbox --only xie2024` (매칭표만) → 본문 + SI 자동 매칭 `[제목 74%]` · 웹앱 `/paper/<slug>` 200 · 그림 26 장 렌더 · `paper_figure_notes` 26/26 · `paper_pis` = `['ceder']` · 원소 페이지 Ag · Li · C · Zn · Mg 연결 ✓ · 기법 페이지 dft · phonon 연결 ✓ · 시험: `test_v3_literature` + `test_v3_markdown` **43/43 통과** · `test_webapp -k "sakamoto or litdb_figure or recent_digests or digest_date or element_papers or glossary_papers or figure_comment"` 7 통과 1 실패 = `test_recent_digests_are_on_every_litdb_surface` (INDEX · comparison 미편입 — 합치면 풀려요).
- 🎤 talk 역링크: talk 인입 대기열 (1 파일) 에 이 논문 없음.

⚠ **메인에 알릴 것**
1. **이 논문엔 W_ad · W_sep · 계면 에너지 · 흡착 에너지가 하나도 없어요.** DFT 는 벌크 Ag–Li 합금만이고, '점착' 은 연속체에 넣은 **점착 세기 (MPa · 응력)** 두 줄 (CC/BL ≈2 MPa 본문 · SE/BL figure-read ≈9.5 MPa · refs 22 · 60) 이에요. 게다가 그 `Fig. 7c` 는 **SE 를 LLZO 로 둔 계산** (캡션) 이에요 → 우리 W 와 같은 줄 금지 · 쓸 수 있는 건 **순서** (W(C\|LPSCl) 대 W(C\|Cu)) 뿐이에요.
2. **'Li 가 CC 쪽에 쌓인다' 의 두 근거 (BL/CC 의 ASR 이 더 작다 · BL/SE 점착이 더 세다) 는 둘 다 입력이에요** — ASR 2 대 20 Ω cm² 는 시나리오 (✎ 20 = BL/SE i_ex 1.3 mA cm⁻² 의 선형 BV 저항 · 2 = 그 0.1 배). 계산이 직접 보인 건 Ag–Li 열역학 (bcc 고용체 · AgLi₂₅ 에서도 양의 리튬화 전위) 쪽이에요.
3. **SI 표 크롭 셋이 틀려 있었어요** — 캡션이 표 **아래** · 쪽 경계에 걸리는 revtex 꼴이라 도구가 캡션 쪽의 다음 표를 잡았어요 (`tab_S1` = BCC 캡션 + FCC 표 · `tab_S2` · `tab_S3` 는 표 뒷부분만). 손으로 두 쪽 영역을 이어 붙여 다시 잘랐고 `figures.json` 에 `recrop` · `recrop_regions` · `auto_bbox` · `auto_page` 를 남겼어요. 도구 쪽 한계로 기록해 둘 만해요 (도구는 안 고쳤어요 — 쓰기 범위 밖).
4. **연속체 그림의 절대 시간축이 본문 매개변수와 4–10 배 어긋나요** (✎ 전하 수지): 0.68 mA cm⁻² × 15 분 = Li 등가 0.82 µm 라 10 µm BL 의 ≤ 8 % 만 채울 수 있는데 `Fig. 7a` 는 15 분에 ≈36 %p 를 채워요 · `Fig. 6` 의 'y ≈ 25 를 8 분' 은 Ag ≈0.14 vol% 여야 맞아요 (본문 1.6 vol%). → digest 에 '시간 · 20 % 부피 인용 금지' 를 걸었어요.
5. **`Fig. 8` 패널 매개변수 표기가 서로 안 맞아요** (색별 곡선 판독): 8c 파랑 (캡션 σ 0.1 · ASR 2) = 8d 검정 (σ 0.1 · ASR 20) · 캡션상 같은 조건인 8d 빨강과 달라요 · 8b (σ 1 · ASR 2) 는 같은 조건인 8c 검정과 안 맞아요. 경향만 쓰게 했어요.
6. **방전은 시뮬레이션하지 않았어요** — 'Ag 가 CC 위에 균일한 나노입자로 석출' 은 `Fig. 11` 도식 추론이고, litdb 이웃 실험 둘과 어긋나요 (`metzler2026_…`: 방전 뒤 Ag 가 C 위 (SE 쪽) 로 · `spencerjolly2023_…`: Li₁₀Ag₃ 대부분 층 안 복귀). W_ad 보고서 8-3 의 'Ag 는 방전 뒤 탄소 위에 덩어리로' 문장에 이 논문을 같은 근거로 걸면 안 돼요.
7. **포논 보정이 실험 대비 일치를 오히려 나쁘게 해요** — x = 8/13 의 γ₃ → BCC 교차가 MC 만 figure-read ≈470 K · 포논 포함 ≈280 K · 실험 γ₃ 상한 ≈473 K (`Fig. S5a` · `Fig. 1a`). 저자는 '너무 낮다' 고만 써요. '실온 Ag–Li = bcc 고용체' 는 방법 의존이고, operando XRD 의 Li₉Ag₄ 와 긴장이 있어요.
8. **`kang2026_…` 가 이 논문의 다공도 0.4 를 Ref. 39 로 가져갔는데, 이 논문은 40 % 를 '보여 주기용 (demonstrative)' 이라고 명시해요** — kang2026 digest 에 주석을 달지는 메인이 정해 주세요 (남의 digest 라 안 건드렸어요). `metzler2026_…` (ref 28 · 그 digest (d) 3 번 후보로 올려 둠) · `lu2026_…` (ref [15]) 도 이 논문을 인용해요 — 역링크도 메인 판단이에요.
9. **논문 자체의 오기 · 불일치** (digest §10 에 인용 금지 규칙): `Table 2` Bi 행 'BiLi₃ · x 0.94' (BiLi₃ 면 0.75 · R 2.1 은 BiLi₃ 부피와 맞음) · 본문 '8 분 ↔ BL 부피 약 20 %' 대 `Fig. 7a` ≈26 % · '처음 10 분은 기공을 크게 안 채움' 대 `Fig. 7a` 10 분 ≈30 % · `Fig. 6b` 0 교차 ≈9.3 분 대 본문 ≈8 분 · Ag '1.6 %' 대 '대략 2 %' · `Table S4` 'Electronic ASR' 대 본문 '전하 전달 ASR' · `Fig. 10` 'Overshoot' 대 본문 'over-saturation' · 캡션 'DFT computations in 2a' (그림 2 엔 패널 없음) · DFT k 점 '800 k-points per Å' (단위 모호).
10. W_ad 보고서 8 절 머리가 '18 편' 이라 이 배치 (11-24b) 를 넣으면 머리 문구 · 8-7 표도 같이 고쳐야 할 거예요 (앞 보고 #1 과 같은 지적).
11. 발견 검색 (최근 2 년 먼저): OpenAlex 1 번 (프록시가 막음 · 허용 안 된 호스트) · Crossref 주제어 검색 5 번 + 서지 확인 2 번 (ref 22 · 24) — 일반 UA · 개인정보 없음. 건진 최근 편 넷은 (d) 에 넣었어요 (제목 · 서지만 확인 · 본문 안 읽음).

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 한 묶음)` — 행 순서상 **'Ag/C 인터레이어' 묶음 끝** (`metzler2026_…` 행 다음 · `shi2026_…` · `chatterjee2025_…` (연속체 모델) 바로 앞). 이 논문이 Ag/C 기전 + 연속체를 같이 해서 두 묶음 경계가 맞아요. 저자에 Jeff Sakamoto 가 없어서 🏷 는 안 달아요.

| `papers/xie2024_agc_buffer_layer_lithiation_delithiation_mechanism.md` **(본문 18 pp + SI 14 pp · 크롭 26 장 (도구 23 + 다시 자름 3 = `Table S1`–`S3`) · 그림 19 장 전부 실독 · `Fig. 7a` 픽셀 판독 · `Fig. 8b`–`d` 색별 판독 · 2026-11-24)** | **[외부·DFT(VASP-PBE · PAW · 벌크 Ag–Li 만)+CE-MC+포논+연속체(자체 FEM)·⭐⭐⭐ Ag/C 층 기전의 계산 원전 · W_ad §7 ③ '합금 구동력' 의 문헌 정량 · ⛔ W_ad · W_sep · 계면 에너지 0 — '점착' 은 문헌 점착 세기 (MPa) 입력 · `Fig. 7c` = LLZO 계 · 우리 W 와 같은 줄 금지]** ✅ **Fengyu Xie**/Mouhamad Said Diallo/Haegyeom Kim/**Qingsong Howard Tu\***/**Gerbrand Ceder\*** (UC Berkeley · LBNL · RIT), "**The Microscopic Mechanism of Lithiation and Delithiation in the Ag/C Buffer Layer for Anode-Free Solid-State Batteries**" — ***Adv. Energy Mater.* 14, 2302960 (2024)**, DOI `10.1002/aenm.202302960` (CC BY-NC-ND · 자료 요청 시). Ag–Li: 0 K 바닥 B2 (x 0.5 · FCC I4₁/amd 보다 5.2 meV/atom 아래) · D0₃-AgLi₃ (0.75) · 200 K (Ag) 0–0.512 · β 0.524–0.548 · γ₃ 8/13 · BCC 0.693–1 → **300 K (Ag) 0–0.417 + BCC 고용체 0.466–1** · 리튬화 전위 **AgLi₂₅ 1.6 (200 K) · 2.6 mV (300 K)** · 과포화 음전위 없음 · Zn −3.4 · −19.0 mV · Mg 양수 (CALPHAD) · R (Ag γ₁) 17.7. 연속체 (d 40 nm · H 10 µm · σ 1 mS cm⁻¹ · 0.68 mA cm⁻²): ASR 2 대 20 Ω cm² (시나리오) → BL/CC 석출 · 내부 압력 ≈8 MPa · CC/BL ≈2 MPa + 적층 1 MPa < SE/BL ≈9.5 MPa (figure-read) → CC 쪽 압출 · CC 위 Ag 1–2 mV 가 25 µm 밖 돌기 전류를 끌어옴. 🔴 연속체 시간축이 전하 수지와 4–10 배 어긋남 (✎) · `Fig. 8` 패널 표기 불일치 · 포논 보정이 γ₃→BCC 교차를 ≈470 → ≈280 K (실험 ≈473 K) · 방전 계산 없음 ('방전 뒤 CC 위 Ag' 는 추론 · metzler2026 · spencerjolly2023 와 충돌) · `Table 2` Bi 행 오기 · 실험 0 | 점착 트랙: W_ad 보고서 7 절 3 번 (합금 구동력 = `Fig. 5`) · 7-1 Ag 행 (충전 중 면 = bcc 고용체 · 후보 B2-LiAg · D0₃-AgLi₃ · 희박 Li(Ag)) · 8-3 (W(C\|LPSCl) 대 W(C\|Cu) 의 **순서**가 이 기전 전제의 원자 수준 시험) · ✎ 1 mV ↔ 7.4 MPa (식 9) · ⛔ 점착 세기 · 시간축 · 다공도 40 % 인용 금지 · 이웃 `spencerjolly2023_…` (ref 26) · `metzler2025_…` · `metzler2026_…` (ref 28 로 인용) · `kang2026_…` (다공도 0.4 를 가져감) · `lu2026_…` (ref [15] 로 인용) · `liao2025_…` (같은 구도의 박리 인성 실측) |

---

## (b) `comparison_vs_ours.md` 에 넣을 줄

**A–D 물성 4축: 본 자리 없어요** (아지로다이트 물성 0 · 음극 Ag/C 층 논문). 판정은 §E 1 행 + §J 방법 블록이에요.

### b-1. `📑 Reference key` 표에 한 행 (4 칸: 약칭 | 논문 | digest/status | 유형)

| **[Xie24AgC]** 🔧 **Ag/C 버퍼층 기전 — Ag–Li 자유에너지 (CE-MC + 포논) · 리튬화 전위 (평형 · 과포화) · 연속체 (ASR · 점착 세기 · 압력 · 전류 분포)** · ⛔ **W_ad · W_sep · 계면 에너지 0 — '점착' 은 문헌 MPa 입력 (`Fig. 7c` = LLZO 계) · 우리 W 와 같은 줄 금지** · ⛔ **A–D 4축 진입 금지** | Fengyu Xie/Mouhamad Said Diallo/Haegyeom Kim/Qingsong Howard Tu\*/Gerbrand Ceder\* (UC Berkeley · LBNL · RIT) 2024 ***Adv. Energy Mater.* 14, 2302960** (DOI 10.1002/aenm.202302960 · CC BY-NC-ND) — "The Microscopic Mechanism of Lithiation and Delithiation in the Ag/C Buffer Layer for Anode-Free Solid-State Batteries" | ✅ `papers/xie2024_agc_buffer_layer_lithiation_delithiation_mechanism.md` — 판정은 §E 1 행 + §J (방법) | DFT (VASP-PBE · 벌크 합금) + CE-MC + 포논 + 연속체 FEM · 실험 0 |

### b-2. §E 표에 한 행 (4 칸: 주장 | 출처 | 우리 | 일치)

| **🆕 (2026-11-24) Ag/C 버퍼층에서 Li 가 집전체 쪽에 쌓이고 Ag 가 집전체 쪽으로 옮겨 가는 이유 = ① Ag–Li 가 실온에서 넓은 bcc 고용체 (x ≳ 0.47 · 300 K) 로 AgLi₂₅ 까지 리튬화 전위 > 0 (1.6 · 2.6 mV · 200 · 300 K) ② BL/CC 의 전하 전달 ASR < BL/SE (2 대 20 Ω cm² · 시나리오) ③ 점착 세기 SE/BL (figure-read ≈9.5 MPa · LLZO 계) > CC/BL (≈2 MPa) + 적층압 (≈1 MPa) → BL/CC 가 먼저 벌어져 Ag–Li 가 CC 쪽으로 압출** — ⚠ ② · ③ 은 입력 · 방전 (Ag 가 CC 위 나노입자로) 은 계산 없음 | **[Xie24AgC]** `Fig. 3` · `Fig. 5` · `Fig. 6` · `Fig. 7` · `Fig. 9` · `Table S4` (VASP PBE · CE-MC · Phonopy QHA · 자체 FEM) | 우리 W_ad 는 고정 기하 W (`db/properties/adhesion.json` · `db/properties/wad_*` · 값은 여기 안 실음) · Li–Ag 합금 계산 0 · 음극 계면 연속체 0 | 🟡 **방향 근거 (문헌)** — 합금 구동력은 인용 가능 (방법 · 온도 · 포논 의존 명시) · ⛔ 점착 세기 (MPa) 를 W (J m⁻²) 와 같은 줄 금지 · ⛔ 연속체 시간 (8 · 15 · 45 분) 인용 금지 (✎ 전하 수지 4–10 배 어긋남) · 🔀 [SJ23AgC] (operando XRD 의 Li₉Ag₄ · Li₁₀Ag₃ ↔ 300 K 계산 'FCC + BCC 뿐' 긴장 · 방전 뒤 Li₁₀Ag₃ 층 안 복귀) · metzler2026 (방전 뒤 Ag 가 C 위) 와 방전 쪽 충돌 |

### b-3. §J 끝에 블록 (지금 J-91 · **J-9x** — 번호는 메인이 정해 주세요 · 앞 보고 #1 이 J-92 를 제안했어요)

### J-9x. 🔧 **방법 원전 — [Xie24AgC] Ag–Li CE-MC 자유에너지 → 리튬화 전위 (평형 · 과포화 경로) · BV 압력 항 · 점착 세기 문턱의 분리 판정 — 우리 W_ad §7 ③ · 8-3 과 대조** (2026-11-24 신설)

📎 **출처**: `papers/xie2024_agc_buffer_layer_lithiation_delithiation_mechanism.md` (그림 19/19 실독 · `Fig. 7a` 픽셀 판독 · `Fig. 8b`–`d` 색별 판독 · SI 표 셋 다시 자름)

⛔ **A–D 물성 4축 표에 행을 만들지 않는다** — 판정은 **§E 1 행**. 우리 W 값은 위치만 (`db/properties/adhesion.json` · `db/properties/wad_*`).

| 항목 | [Xie24AgC] 가 보이는 것 | 우리 현재 | 판정 |
|---|---|---|---|
| 합금 열역학 | CE 셋 (BCC · FCC · γ — 클러스터 25 · 32 · 38 · RMSE 3.3 · 1.5 · 0.5 meV/atom) + 정준 MC 열역학 적분 (T₀ 20 K) + 포논 (몇 구조 · x 선형 보간) + B-스플라인 | 없음 (W_ad 7 절 3 번 제안만) | 🔑 **문헌 정량으로 인용** (VASP-PBE · CE-MC · 포논 · 200/300 K 명시) |
| 판정 규칙 | 과포화 경로 = 두 F 곡선 교점에서 통째 전이 · **음 과포화 전위 = 리튬화 정지 → 다른 곳 석출** · 좁은 정비 화합물이 위험 (Zn) | — | ✅ 합금 층 금속 고르기 판정 틀로 가져올 만함 |
| 점착 | MPa 점착 세기 두 줄 (입력 · refs 22 · 60 · LLZO 계) → 응력 > 점착 + 적층압 이면 분리 | 고정 기하 W (J m⁻²) | ⛔ **같은 표 금지** · 순서만 (W(C\|LPSCl) 대 W(C\|Cu)) |
| 압력 | 식 (9) 기계 항 V̄_Li ΔP/F · 포화 P = F⟨η⟩/V̄_Li (≈8 MPa) | DEM 압력 단계 | ✅ ✎ **1 mV ↔ 7.44 MPa** (설명용 환산) |
| 연속체 시간 | ✎ 전하 수지와 4–10 배 어긋남 | — | ⛔ 시간 인용 금지 · 순서만 |
| 검증 | 실험 대조 없음 (문헌 SEM · XRD 를 정성 인용) · 코드 · 자료 비공개 · 방전 계산 없음 | — | ⚠ |

**인용 위생**: 점착 세기 · 다공도 40 % ('demonstrative') · Ag 1.6 vol% · 시간축 · `Fig. 8` 패널 매개변수 · `Table 2` Bi 행 인용 금지 · AgLi₂₅ 1.6 · 2.6 mV 는 부호만 견고 (✎ 희박 고용체 배치 엔트로피만 1.01 mV @ 300 K) · 장벽 · MD 없음 → 홉 수 · 관측창 규칙 해당 없음.

### b-4. (권장 · 점착 트랙의 실제 집) `comparison_vs_ours_DEM.md` §I 에 블록 (지금 I-22 · **I-2x** — 번호는 메인이)

### I-2x. `xie2024_agc_buffer_layer_lithiation_delithiation_mechanism` — ★★ (계산 · ⛔ W 아님 · ⛔ G_c 아님) **Ag/C 층 기전: 합금 구동력 (mV) · ASR 비대칭 · 점착 세기 (MPa) 비대칭 → CC 쪽 석출 · 압출** · ✎ 1 mV ↔ 7.4 MPa

- **무엇**: Ag–Li 는 실온에서 넓은 bcc 고용체 (x ≳ 0.47) 로 AgLi₂₅ 까지 Li 를 받는다 (계산). 연속체에서 BL/CC 의 ASR 이 작고 (입력) 점착이 약하면 (입력 · MPa) Li 가 CC 쪽에 쌓이고 BL/CC 가 먼저 벌어진다.
- **점착 트랙에 주는 것 셋**: ① W_ad 7 절 3 번 '합금 구동력' 을 `Fig. 5` 로 채운다 (새 계산 불필요) ② 7-1 Ag 행의 '충전 중 면' 을 정비 화합물 대신 B2-LiAg · D0₃-AgLi₃ · 희박 Li(Ag) 로 잡는 근거 ③ 8-3 의 C\|Cu 후보는 이 기전 전제 ('BL/SE 점착 > BL/CC + 적층압') 의 원자 수준 시험 — **순서만**.
- **DEM 쪽 쓰임**: ✎ 1 mV ↔ 7.44 MPa (V̄_Li 12.97 cm³ mol⁻¹) — 적층압 1 MPa ≈ 0.13 mV · 압력은 합금화 열역학보다 접촉 · 분리를 바꾼다 · 기공이 막히면 수 mV 구동력이 수십 MPa (2.6 mV → ≈19 MPa 상한) 를 만들 수 있다 (BL 내부 분리의 구동력).
- **금지**: 점착 세기 (MPa) 를 W · Γ 와 같은 줄 · 다공도 0.4 를 실측처럼 (kang2026 이 가져감) · 연속체 시간 · '방전 뒤 Ag 는 CC 위' 를 계산 결과로.

---

## (c) `pdf_map.tsv`

**필요 없어요** — `extract_figures.py --inbox --only xie2024` (매칭표만) 가 본문 + SI 둘을 자동으로 붙였어요 (`[제목 74%]`). 굳히고 싶으면 한 줄:

```
xie2024_agc_buffer_layer_lithiation_delithiation_mechanism	xie2024_agc_buffer_lithiation_mechanism
```

---

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저)

> 대조: `litdb/papers` 파일 이름 + digest 본문 grep · `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md` grep. 1–4 는 Crossref 주제어 검색으로 찾았고 **제목 · 서지만 봤어요** (본문 안 읽음 · 쪽 번호가 아직 없는 편은 DOI 로). 7 · 8 은 이 논문 참고문헌을 Crossref 로 서지 확인했어요.
> 이미 litdb 에 있거나 이번 묶음에서 병렬로 도는 것 (세지 않음): ref 26 `spencerjolly2023_…` · ref 18 Kasemchainan 2019 (#10) · ref 21 Lee 2020 (#9) · Ko 2025 (#8) · Haslam 2025 (#4) · Becker 2026 (#3) · Hiraoka 2025 (#6).

| # | 문헌 | 왜 (우리 축) | litdb | 목록 |
|---|---|---|---|---|
| 1 | Tong … Li · *ACS Energy Lett.* 10, 6207 (2025) — *"A Nondeposition Solid-Solution Li Alloy Anode for Solid-State Batteries"* · DOI 10.1021/acsenergylett.5c02665 | 이 논문의 '고용체 = 끝까지 양의 전위 → Li 석출 없이 받는다' 를 음극 설계로 밀어붙인 편으로 보여요 (제목 기준) — W_ad 7 절 3 번 합금 구동력 | 없음 | 없음 |
| 2 | Huang … Zhu · *Adv. Sci.* 13 (2026) — *"Design Principles for Alloy-Anode-Based Low-Stack-Pressure Solid-State Batteries"* · DOI 10.1002/advs.76946 | 합금 음극 설계 원리 × 낮은 적층압 — `Table 2` · `Fig. 10` 의 금속 고르기 판정과 DEM 압력 단계 | 없음 | 없음 |
| 3 | Pham … Kim · *Chem. Commun.* (2026) — *"Carbon interlayers in anode-free solid-state batteries: linking surface chemistry to lithium retention and recovery"* · DOI 10.1039/d6cc06562g | 이 논문은 탄소를 'LiC₆ 포화 MIEC' 로만 둔다 — 탄소 표면 화학 (작용기 · 결함) → W_ad 7-1 탄소 모형 | 없음 | 없음 |
| 4 | Liu … Clemens · *Electrochim. Acta* 574, 149375 (2026) — *"Effect of carbon interlayer preconditioning on in-situ plated lithium metal stability in anode-free solid-state batteries"* · DOI 10.1016/j.electacta.2026.149375 | 이 논문 Step 1 (탄소가 먼저 리튬화) 의 실험 쪽 — 탄소 전처리와 석출 Li 안정성 | 없음 | 없음 |
| 5 | Park, Naik, Vishnugopi, Mukherjee, Hatzell · *Adv. Energy Mater.* 15, 2405129 (2025) — *"Lithium Kinetics in Ag–C Porous Interlayer in Reservoir-Free Solid-State Batteries"* · DOI 10.1002/aenm.202405129 | 이 논문의 후속 연속체 (같은 질문 · 다공도 ≈29 % 기준값) → 시간축 · 다공도 대조 · DEM 입력 | 없음 | **목록에 있음** (표 1 #9) |
| 6 | Thomas … Van der Ven · *Chem. Mater.* 36, 8936 (2024) (Li–Ag 합금상 이동 장벽 · `lu2026_…` digest 의 ref [18]) | 이 논문의 '입자 안 Li 즉시 균질' 가정의 장벽 근거 · CE 같은 계열 | 없음 | **목록에 있음** ('그 밖') |
| 7 | Park S. H., Jun, Jung, Lee, Lee, Lee · *J. Mater. Chem. A* 10, 21995 (2022) — *"Clarification of Li deposition behavior on anodes with a porous interlayer in Li-free all-solid-state batteries"* · DOI 10.1039/d2ta06466a (ref 24) | 이 논문 점착 논리의 직접 선행 (BL/SE 점착 > BL/CC → BL/CC 석출 · Coble 크리프) — 8-3 | 없음 (`sandoval2025_…` digest 에 인용만) | 없음 |
| 8 | Suzuki, Yashiro, Fujiki, Omoda, Shiratsuchi, Watanabe, Aihara · *Adv. Energy Sustainability Res.* 2, 2100066 (2021) — *"Highly Cyclable All-Solid-State Battery with Deposition-Type Lithium Metal Anode Based on Thin Carbon Black Layer"* · DOI 10.1002/aesr.202100066 (ref 22) | `Fig. 7c` 점착 세기 출처 둘 중 하나 · 금속/C 층 비교 (Ag 최고) · 흑연이면 BL/SE 석출 — 8-3 | 없음 (`sandoval2025_…` 에 인용만) | 없음 |

다음 순번: Tu, Barroso-Luque, Shi, Ceder · *Cell Rep. Phys. Sci.* 1, 100106 (2020) (ref 7 · 연속체 원전) · Wang M. & Sakamoto · *J. Power Sources* 377, 7 (2018) (ref 60 · 점착 출처 · **목록에 있음** '그 밖') · Haslam & Sakamoto · *J. Electrochem. Soc.* 170, 040524 (2023) (ref 68 · Au 씨앗 · **목록 노트에 있음**) · Kim J.-S. … Im · *Nat. Commun.* 14, 782 (2023) (ref 23 · LLZO 판 Ag/C) · Kim S. … Kang K. · *ACS Energy Lett.* 8, 9 (2022 · ref 25) · Ganser *et al.* · *J. Electrochem. Soc.* 166, H167 (2019) (ref 96 · 압력 항 BV) · Wang … Zhang · *J. Energy Storage* 110, 115303 (2025) (Li–Mg 합금 DFT — 이 논문의 Mg 제안 대조 · Crossref 검색).

---

## (e) DEM-DFT 보고서 (W_ad 보고서) 에 쓸 거리

| 보고서 항목 | 이 논문에서 쓸 점 | 위치 (쪽 · 그림 · 표) | 직접 봤나 |
|---|---|---|---|
| **7 절 3 번 '합금 구동력'** | Ag 리튬화 전위 = 7 절 3 번이 말한 '리튬을 받기 시작하는 전위' 그 자체 · 300 K: y < 0.5 에서 > 400 mV → AgLi 근처 ≈140 → y 2 · 3 · 5 에서 ≈110 · 50 · 12 mV (figure-read) → **AgLi₂₅ 2.6 mV (인쇄)** · 과포화 경로에도 음전위 없음 · ⚠ 부호는 견고 · 크기는 CE 오차 규모 · 방법 (VASP-PBE · CE-MC · 포논 보간) · 온도 명시 | p.7 · `Fig. 5` · p.5 · `Fig. 3` · digest §3c · §5.6 · §7c | ✅ `Fig. 5` · `Fig. 3` 원해상도 |
| **7-1 표 Ag 행 (충전 중 Li–Ag 합금 면)** | 실온 Ag–Li = (Ag) FCC 0–0.417 + **bcc 고용체 0.466–1** (그림 안 글자) → 충전 중 Ag 면은 '다른 재료의 면' 이 아니라 Li 로 이어지는 bcc 고용체 · 질서 후보 B2-LiAg (x 0.5) · D0₃-AgLi₃ (0.75) · 희박 Li(Ag) · ⚠ 포논 보정 의존 · operando XRD 의 Li₉Ag₄ · Li₁₀Ag₃ 와 긴장 | p.4–6 · `Fig. 2` · `Fig. 3c` · SI `Fig. S2` · `S5` · `S6` · digest §3a · §3b · §7c · §10-⑤ | ✅ 전부 원해상도 |
| **8-3 (Ag/C 층에서 Li 는 어디에)** | 집전체 쪽 석출 = ① ASR 비대칭 (BL/CC 2 대 BL/SE 20 Ω cm² · 시나리오) ② 점착 비대칭 (SE/BL > CC/BL + 적층압) — **둘 다 입력** · C\|Cu 후보는 ② 의 원자 수준 짝 → 우리 W 로 답할 질문 = W(C\|LPSCl) 대 W(C\|Cu) 의 **순서** · 방전 뒤 Ag 위치는 이 논문 (CC 위 · 추론) 과 metzler2026 (C 위 · 실험) 이 반대 → 8-3 첫 줄 문장에 이 논문을 같이 걸지 않는다 | p.8–9 · `Fig. 6` · `Fig. 7` · p.13 · `Fig. 11` · digest §6 · §7d | ✅ `Fig. 6` · `7` · `11` 원해상도 · `Fig. 7a` 픽셀 판독 |
| **1 절 · 6 절 · 8-6 (W 의 정의 · 가져오지 않는 것)** | 이 논문의 '점착' = **점착 세기 (MPa · 응력)** · CC/BL ≈2 MPa (본문) · SE/BL figure-read ≈9.5 MPa (본문에 숫자 없음) · `Fig. 7c` = LLZO 계 → W (J m⁻² · 고정 기하 분리 에너지) 와 다른 양 · ✎ 이상 강도로 바꾸면 2–3 자릿수 차 · 결합 규모 흡착 에너지 없음 (배위수 규칙 해당 없음) | p.9 · `Fig. 7c` · digest §3e · §7b | ✅ `Fig. 7c` 원해상도 |
| **8-4 (DEM · 연속체로 넘길 때)** | ✎ 식 (9) 기계 항으로 **1 mV ↔ 7.44 MPa** (V̄_Li 12.97 cm³ mol⁻¹ · `Table S4`) — 적층압 1 MPa ≈ 0.13 mV · 모델 압력 상한 8 MPa ≈ 1.1 mV · Li K 11 GPa (= `masias2019_…` K 11.1 GPa) · ⛔ 가져오지 않을 것: 다공도 40 % ('demonstrative' · kang2026 이 가져감 · metzler2026 은 흔한 Ag/C 층 ≈29 % 인용) · 연속체 시간축 (✎ 전하 수지 4–10 배 어긋남) | p.7–9 · 식 (8)–(13) p.15–16 · SI p.13 `Table S4` · digest §4h · §4i · §7f · §10-② | ✅ `Table S4` 대조표 (값은 글자층) · 식은 글자층 |
| **7-1 확장 (다른 금속 층)** | 판정 틀: 좁은 정비 화합물 → 음 과포화 전위 → 리튬화 정지 (Zn −3.4 · −19.0 mV) · 고용체 금속 (Ag · Mg) 은 양의 전위 유지 · R (부피 팽창비) 는 금속 부피 분율과 같이 봐야 함 (✎) · `Table 2` Bi 행 오기 | p.12–13 · `Fig. 4` · `Fig. 10` · `Table 2` · digest §3g · §10-⑦ | ✅ `Fig. 4` · `10` 원해상도 · `Table 2` 대조표 |

**8-7 표에 더할 행 후보** (보고서 꼴): `| *Adv. Energy Mater.*, 14, 2302960 (2024) | Ag/C 버퍼층 · Ag–Li 열역학 + 연속체 (계산) | 7 절 3 번 합금 구동력 · 8-3 Li 석출 자리 (입력 비대칭) |`

보고서 문장 후보 (공유 보고서 문체 · 출처는 랩 표준 꼴 · 내부 사정 없음):
- *Ag 는 Li 와 넓은 조성에서 bcc 고용체를 이뤄 Li 를 계속 받아들이는 쪽 (리튬화 전위 > 0) 으로 남는다는 계산이 있다 (Adv. Energy Mater., 14, 2302960 (2024)) — 충전 중의 Ag 면은 Li 와 따로 떨어진 재료의 면이라기보다 Li 속으로 녹아드는 면이다.*
- *같은 연구의 연속체 모델은 Li 가 집전체 쪽에 쌓이는 이유를 계면 전하 전달 저항과 점착 세기의 비대칭으로 설명하는데, 두 값은 계산한 것이 아니라 문헌에서 가져온 입력이고 점착 세기는 MPa 단위의 실용 값이라 이 보고의 W 와 같은 양이 아니다.*
- *합금화 구동력 1 mV 는 정수압 약 7 MPa 와 맞먹는다 (이 보고의 환산) — MPa 급 적층압은 합금화의 열역학보다 접촉과 분리를 바꾼다.*

문장 후보 기준표 (사용자가 항목마다 10 점으로 매기면 돼요): ① 논지 정확성 (계산 · 입력 · 추론 구분) __/10 · ② 출처 (랩 꼴 *저널*, 권, 첫 쪽 (연도)) __/10 · ③ 값 규율 (우리 W 값 없음 · 단위 · 계 명시) __/10 · ④ 공유 보고서 문체 (내부 사정 없음 · 짧은 평서) __/10.

---

## (f) 그림 크롭 요약

- **26 장** = 본문 그림 12 (`Fig. 1`–`12`) + SI 그림 7 (`Fig. S1`–`S7`) + 본문 표 3 (`Table 1`–`3`) + SI 표 4 (`Table S1`–`S4`). 도구 한 번 (`--slug … --pdf 본문 SI --clean`) 으로 23 장 · **다시 자름 3 장 (`Table S1`–`S3`)**: 캡션이 표 아래 · 쪽 경계에 걸려 도구가 캡션 쪽의 다음 표를 잡았어요 (`tab_S1` = BCC 캡션 + FCC 0–22 행 · `tab_S2` = FCC 23–31 행만 · `tab_S3` = γ 14–37 행만) → SI 4+5 · 5+6 · 6+7 쪽 영역을 이어 붙여 BCC 0–24 · FCC 0–31 · γ 0–37 + 각 캡션으로 다시 잘랐어요 (300 dpi · 긴 변 ≤ 3000 px · `recrop` 사유 · `recrop_regions` · `auto_bbox` · `auto_page`). 번호 공백 · 놓친 캡션 0.
- **캡션 정리**: `Fig. 1` · `7` · `9` 캡션이 900 자에서 잘려 있어서 본문 글자층에서 전문을 되살렸어요 · `Table 3` 캡션 뒤에 붙은 표 본문 삭제 · 합자 (ﬁ · ﬂ · ﬀ) · 수학 이탤릭 그리스 문자 (𝛼 · 𝛽 · 𝛾) 를 보통 글자로 · I43m → I-43m · Pm3m → Pm-3m. 원문은 `caption_raw` 14 개.
- **본 것: 그림 19/19 원해상도** (`Fig. 1`–`12` · `Fig. S1`–`S7`) · `Fig. 7a` 는 파란 곡선 픽셀을 좌표로 바꿔 읽었고 (1–14 분 8 점) · `Fig. 8b`–`d` 는 색별 곡선을 눈금 보정으로 읽어 패널끼리 대조했어요. 표 7 장은 축소 대조표로 크롭만 확인 (값은 PDF 글자층).
- **그림이 본문 · 표와 어긋난 것**: `Fig. 7a` 8 분 ≈26 % (본문 '약 20 %') · 10 분 ≈30 % (본문 '처음 10 분은 기공을 크게 안 채움') · `Fig. 6b` 0 교차 ≈9.3 분 (본문 ≈8 분) · `Fig. 7c` CC/BL 선 ≈2.3 MPa (본문 ≈2) · SE/BL 선 ≈9.5 MPa (본문에 숫자 없음) · `Fig. 8` 패널 매개변수 표기 불일치 (8c 파랑 = 8d 검정 · 8b ≠ 8c 검정) · `Fig. 10` 범례 'Overshoot' (본문 'over-saturation') · `Fig. 7` 캡션 '2a' (그림 2 엔 패널 없음) · `Table 2` Bi 행 · 전하 수지로 본 `Fig. 6` · `Fig. 7a` 시간축.
- **임시 파일 점검 (병렬 충돌 주의)**: 글자층 · 스크립트 · 대조표 · 검색 결과는 전부 `scratchpad/xie2024_agc_buffer_layer_lithiation_delithiation_mechanism/` 안에 `xie2024_` 접두 이름으로만 썼어요 (공용 이름 없음). 본문 글자 파일 첫 줄 = 이 논문 표지 (RESEARCH ARTICLE · 제목 · Xie … Ceder) · SI 글자 파일 첫 줄 = 이 SI 표지 · PDF sha256 두 개 = `batch.json` 값과 일치. 대조표 내용 (Ag–Li CE 표 · 연속체 매개변수) 도 이 논문 것이었어요.

---

## (g) Jeff Sakamoto 저자 여부

**아니에요** — 저자는 Fengyu Xie (공동 1저자) · Mouhamad Said Diallo · Haegyeom Kim · Qingsong Howard Tu (공동 1저자 · 교신) · Gerbrand Ceder (교신) 다섯 (UC Berkeley · LBNL · RIT). J. Sakamoto 이름은 **참고문헌 저자 목록에만** 나와요 — 본문 refs 13 · 15 · 19 · 20 · 60 · 68 · SI [6] (글자층 확인). digest 머리 35 줄에는 그 이름을 쓰지 않았고 (부정문도 없음 · §15 서지 메모에만 '참고문헌 저자 목록에 있다' 로), 웹앱 `paper_pis` = `['ceder']` 예요 — INDEX 행에 `🏷 Jeff Sakamoto 공저` 를 달지 않아요. PI 배지는 Gerbrand Ceder (`ceder`) 가 머리 저자 줄에서 붙어요.
