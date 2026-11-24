# 끝 보고 — masias2019_li_metal_elastic_plastic_creep_properties (2026-11-24 · litdb-curator)

쓴 파일: `litdb/papers/masias2019_li_metal_elastic_plastic_creep_properties.md` (521 줄 · 표 16 개 칸수 검사 0 건) · `litdb/figures/masias2019_li_metal_elastic_plastic_creep_properties/` (크롭 15 장 + figures.json — 손 크롭 8 장 `manual_crop` 사유 · `missing_labels` 8 건 모두 `resolved` · `Fig. 4` 캡션 `caption_fix` · 본 그림 `viewed`) · 이 보고 파일.  추출 도구가 `litdb/figures/_sources.json` 을 다시 썼다 (도구 몫 · 손 안 댐).
공유 파일 · git 은 안 건드렸다.  그림 폴더와 digest 앞판은 메인 체크포인트 커밋 (b60590e6 · 4739c5a7) 에 이미 들어가 있고 그 뒤 digest 를 더 고쳐서 지금 ` M` 이다.
`build_index.py --check`: 이 slug 는 "어느 인덱스에도 없음 [dem]" · "DEM 비교문서 미편입" 두 곳에만 뜬다 — (a) · (b) 로 풀린다.
웹앱 확인 (읽기만): `list_papers()` → track **dem** · digested 2026-11-24 · `pis` = `['sakamoto']` (배지 붙음) · 원소 태그 Li · Na · K · methods `elastic`.
⚠ 저자: 요청서의 "Asma Masias" 가 아니다 — PDF 1 쪽 = **Alvaro Masias** (Ford · 교신).  digest 는 PDF 대로 적었다.

## (a) 인덱스

**축 판정 = DEM** (`webapp/data.py::literature_track` — slug · type · 제목 낱말 점수 dem 1 : dft 0).  걸린 낱말은 type 문자열의 `contact` 하나다 (*"5 MHz contact transducers"* — 원문 장비 이름 그대로).  그 낱말이 빠지면 0 : 0 → 기본값 **dft** 로 뒤집힌다 ⇒ 취약하다.
권고 (메인 몫 · litdb 밖): `LIT_TRACK_OVERRIDE` 에 `"masias2019_li_metal_elastic_plastic_creep_properties": "dem",` 한 줄.

- `INDEX_DEM.md`: `python3 tools/litdb/build_index.py` 재생성에 맡긴다 (그것으로 '어느 인덱스에도 없음' 이 풀린다).
- `INDEX.md` 행 (Jeff Sakamoto 공저라 권고): 넣을 절 = **`## 🧲 계면 점착 · 인터레이어 트랙`** 표 끝 (W_ad 보고서 §7 공극 쪽 · 같은 묶음 lee2022 과 같은 자리) — 절 머리 'LPSCl 이 한쪽 면' 조건에 안 맞으므로 행 안에 `[외부·Li 금속 벌크]` 표시를 둔다.  대안: `## ✅ Digest 완료 (paper-level)` 표 맨 위.

```
| `papers/masias2019_li_metal_elastic_plastic_creep_properties.md` **(본문 16 pp + SI 2 pp (`Table S1` · `S2`) · 크롭 15장 (도구 7 + 손 크롭 8 = `Fig. 1` · `2` · `3` · `5` · `6` · `7` · `8` · `Table 3` — Springer 옆 캡션) · 그림 10/10 실독 (+ `Fig. 2` 삽입도 확대 · `Fig. 5` · `Fig. 8` 픽셀 판독) · 표 5장 PDF 텍스트 · 2026-11-24)** | 🏷 **Jeff Sakamoto 공저** · **[외부·exp·Li 금속 벌크 역학 앵커 — 탄성 · 항복 · 크리프 (연속체 · DEM 입력) · 계산 없음]** Alvaro Masias\* (Ford) / N. Felten / R. Garcia-Mendez / J. Wolfenstine (ARL) / **Jeff Sakamoto** (Univ. Michigan), "**Elastic, plastic, and creep mechanical properties of lithium metal**" (***J. Mater. Sci.* 54, 2585–2600 (2019)**, DOI `10.1007/s10853-018-2971-3`). 실온 (≈26 °C · T/T_m 0.66) 다결정 Li: 펄스-에코 **E 7.82 · G 2.83 · K 11.07 GPa · ν 0.381** · 인장 0.2 % offset **σ_y 0.73–0.81 MPa** (1.2 × 10⁻³ s⁻¹ · AR 1.1) · 인장 정하중 0.2–0.6 MPa 최소 속도 → **n = 6.56 (전위 상승)** · Li+Na+K 정규화 n 6.70 · 압축 정하중 0.8–2.4 MPa = barreling 으로 속도가 시간에 따라 감소 (구성 법칙 아님). **Q_c 없음 (한 온도) · 점착 정량 없음 (`Fig. 10` 개념뿐)**. ⚠ 항복 SS/PE 짝이 본문 · 표 · 그림에서 다름 · `Fig. 3` '진' 응력은 압축 부호 오류 · `Fig. 7` D 인쇄값 (0.31 cm²/s) 자릿수 의심 · crosshead '1 mm/s' ↔ 1.22 × 10⁻³ s⁻¹ 불일치. 카드 재회귀 A′ = 7.73 × 10⁻³ s⁻¹ MPa⁻ⁿ (`Table S1` 7 점 · 논문 값 아님) | Li 금속 역학 (DEM · 연속체 입력) · W_ad §7 공극 쪽 |
```

## (b) comparison

`comparison_vs_ours_DEM.md` **§I 끝** (`### I-10` 뒤 · 지금 5821 행의 `## J.` 앞) 에 새 블록 — 번호는 합칠 때 정한다 (같은 묶음 lee2022 보고도 I-11 을 제안했다):

```
### I-1x. `masias2019_li_metal_elastic_plastic_creep_properties` — (인접 축 · 점착 정량 0) **Li 금속 자체의 탄성 · 항복 · 크리프** — 공극 · 적층압 모델의 Li 쪽 입력 원전 + 'Li 항복 ≈0.8 MPa' 2 차 인용의 원전

> **무엇을 주나.** 실온 다결정 Li (≈26 °C · T/T_m 0.66): 펄스-에코 **E 7.82 · G 2.83 · K 11.07 GPa · ν 0.381** · 인장 0.2 % offset **σ_y 0.73–0.81 MPa** (1.2 × 10⁻³ s⁻¹) · 인장 정하중 0.2–0.6 MPa → **n = 6.56** · 압축 정하중 0.8–2.4 MPa (AR ≈2 · 광유 윤활) 은 barreling 으로 속도가 시간에 따라 감소.
>
> **★ 우리 축에 닿는 곳.** ① 우리 DEM (강체 구) · MPM (SE J2) 에는 Li 크리프 · 공극 물리가 없다 (`tron2023` L191) — Li 를 넣게 되면 digest §7b 가 입력표 (E · ν · n · 카드 재회귀 A′ = 7.73 × 10⁻³ s⁻¹ MPa⁻ⁿ) ② 실온 Li '항복' 은 그 속도의 크리프 유동 응력이다 (카드 산수: 법칙이 1.22 × 10⁻³ s⁻¹ 에서 0.755 MPa · 문헌 다결정 항복 셋도 ±25 % 안) → 속도 무관 항복 상수 대신 점소성 법칙 ③ 압축 `Table S2` 는 구성 법칙이 아니라 **구조 응답의 검증 표적** (시각 고정 겉보기 지수 −1.4) ④ W_ad 보고서 §7: `Fig. 10` = 점착/마찰 → Li 안 정수압 → 단락 방지 (개념 · 정량 0) · γ_Li 없음.
>
> **⛔ 인용 금지 / 한정어.** · 실온 한 점 (Q_c 없음) · 항복 SS/PE 짝 불일치 (범위로만) · `Fig. 3` '진' 응력 (압축 부호 오류) · `Fig. 7` D 인쇄값 · '마찰 · 점착이 Li 변형률 속도를 10³–10⁴ 배 낮춘다' (Wang 2019 *Joule* 의 외삽 · 기하 포함 — 이 논문 데이터 안은 부과 속도 대비 10²–10²·⁷) · 우리 W 와 같은 줄 금지 (이 논문의 '점착' = 계면 전단 · 마찰 뜻).
```

선택 (이미 있는 2 차 인용을 원전에 잇기 — 값을 바꾸는 게 아니라 조건을 붙이기):
- `comparison_vs_ours_DEM.md` L310 · L324 · L330 — 'Li 항복 ~0.8 MPa (ref 144)' · 조달표 'Li 소성 σ_y 0.8 MPa' · '조달 추천 ③ ref 144 Masias 2019 (litdb 미보유)' → "✅ 보유 (2026-11-24) `masias2019_li_metal_elastic_plastic_creep_properties` · 0.73–0.81 MPa (인장 · 0.2 % offset · 1.2 × 10⁻³ s⁻¹ · RT) + 크리프 n 6.56".
- `comparison_vs_ours.md` L883 (§C · Famprikis 행) — 같은 원전 링크 한 줄.
- `comparison_vs_ours.md` 물성 4축 표에는 넣지 않는다 (Li 금속 · 우리 SE 계 아님).

## (c) pdf_map.tsv

**필요** — 자동 매칭이 본문만 잡고 SI 는 못 잡는다 (`extract_figures.py --inbox --only masias2019` → 본문 `[1쪽 본문 52%]` · `masias2019_li_creep_SI.pdf` 는 '짝 못 찾음' 목록):

```
masias2019_li_metal_elastic_plastic_creep_properties	masias2019_li_creep
```

(두 파일명에 다 들어 있는 조각.  이번 크롭은 `--pdf` 로 두 파일을 직접 줘서 SI 표 둘이 들어갔다 — 이 줄이 없으면 나중 `--refresh` · `--inbox --run` 이 SI 를 놓친다.)

## (d) 추가로 먹일 논문 (8 편 · 최근 먼저)

⚠ OpenAlex · Crossref 가 프록시에서 막혀 (403) 인용 검색을 못 했다.  그래서 **이 묶음 inbox PDF 의 인쇄 참고문헌 (글자층)** 에서 이 논문과 같은 축의 최근 편을 골랐다 — 서지는 그 목록 그대로.  8 편 모두 litdb 카드 없음 (제목 문자열 · slug grep · 2026-11-24).

| # | 서지 | 왜 | 서지 확인처 | litdb |
|---|---|---|---|---|
| 1 | H.-T. Jeong, W. J. Kim, "Deformation Mechanism Maps of Pure Lithium: Their Application in Determining Stack Pressure for All-Solid-State Lithium-Ion Batteries," *ACS Energy Lett.* 9 (2024) 3237–3251, doi 10.1021/acsenergylett.4c01229 | ★ 이 논문이 못 한 **온도 · 기전 지도 · Q** — 연속체 입력의 온도 축 · digest §10-⑤ (Fig. 7 D 의심) 확인 | viscoplastic2026 ref 36 | 없음 |
| 2 | A. M. Roach, W. Zhu, S. Vema, R. M. McMeeking, C. P. Grey, V. S. Deshpande, N. A. Fleck, "Void growth in the lithium anode of a solid state battery," *Eur. J. Mech. A/Solids* 113 (2025) 105710, doi 10.1016/j.euromechsol.2025.105710 | Li 크리프로 공극 성장을 푼 연속체 모델 — 공극 모델 · W_ad §7 | viscoplastic2026 ref 43 | 없음 |
| 3 | K. Li, J. Huang, X. Qu, G. Fu, X. Chen, W. Shen, Y. Lin, "Void Evolution at the Li/LLZO Interface: Stack Pressure and Operating Temperature-Driven Creep Effect," *ACS Appl. Mater. Interfaces* 17 (2025) 3146–3162, doi 10.1021/acsami.4c13564 | 적층압 · 온도 → 크리프 → 공극 (온도 축이 있는 크리프 공극 모델) | viscoplastic2026 ref 16 | 없음 |
| 4 | M. Lu, N. Kanazi, E. Lin, S. Xia, "Size- and temperature-dependent mechanical properties of metallic lithium," *Extreme Mech. Lett.* 61 (2023) 102022 | 크기 · 온도 의존 — 얇은 Li 층 (수십 µm) 에 벌크 값을 쓸 때의 보정 | afssb2024 ref 47 | 없음 |
| 5 | W. Zaman, L. Zhao, T. Martin, X. Zhang, Z. Wang, Q. J. Wang, S. Harris, K. B. Hatzell, "Temperature and Pressure Effects on Unrecoverable Voids in Li Metal Solid-State Batteries," *ACS Appl. Mater. Interfaces* 15 (2023) 37401–37409, doi 10.1021/acsami.3c05886 | 회복 안 되는 공극의 온도 · 압력 의존 — 공극 모델 검증 표적 | viscoplastic2026 ref 18 | 없음 |
| 6 | C. G. Haslam, J. B. Wolfenstine, J. Sakamoto, "The effect of aspect ratio on the mechanical behavior of Li metal in solid-state cells," *J. Power Sources* 520 (2022) 230831 | ★ 이 논문 `Fig. 4` · `Fig. 10` (AR · 마찰) 의 직접 후속 · Sakamoto 공저 | afssb2024 ref 74 · kalnaus2023 카드 [76] | 없음 (lee2022 보고 #3 과 겹침) |
| 7 | A. Masias, N. Felten, J. Sakamoto, "Characterizing the mechanical behavior of lithium in compression," *J. Mater. Res.* 36 (2021) 729–739 | ★ 같은 1 저자의 압축 후속 — 이 논문 압축 절 (barreling · 마찰) 의 다음 판 · Sakamoto 공저 | lee2022 PDF ref 37 | 없음 (lee2022 보고 '차순위') |
| 8 | W. S. LePage, Y. Chen, E. Kazyak, K.-H. Chen, A. J. Sanchez, A. Poli, E. M. Arruda, M. D. Thouless, N. P. Dasgupta, "Lithium mechanics: roles of strain rate and temperature and implications for lithium metal batteries," *J. Electrochem. Soc.* 166 (2019) A89–A97 | 변형률 속도 · 온도 의존 (이 논문에 없는 축) · 같은 해의 짝 원전 | kazyak2020 · wang2019 PDF 참고문헌 | 없음 |

차순위 (이 논문 참고문헌 — 서지 = 이 PDF): [10] Wang M, Sakamoto J (2018) *J Power Sources* 377:7–11 (Li\|SE 점착 ↔ 계면 저항 — W_ad §7 의 실험 짝 후보) · [32] Sargent PM, Ashby MF (1984) *Scr Metall* 18:145–150 (n · D 원전).
**이번 묶음 inbox 에 이미 있어 뺀 것** (PDF 첫 쪽 · 참고문헌에서 이 논문 인용 확인): **viscoplastic2026** (*Matter* 9, 102767 (2026) "Stack pressure effects and viscoplastic deformation in argyrodite solid-state electrolyte" — Li₆PS₅Cl 과 Li 둘 다의 점소성 크리프 · 이 논문 = ref 44 · **가장 가까운 후속** → 그 digest 가 생기면 서로 링크 권고) · wang2019 (*Joule* — 이 논문 압축 데이터로 '10⁴ 감속' 가정 · digest §7c-6) · kazyak2020 · wang2020 · yang2021mo · afssb2024 (*Nat. Mater.* 24, 673 (2025)) · kim2026_void_impedance · difint2025 · sharafi2017 (= 이 논문 ref [23] · digest 에 링크함) · seymour2021 (링크함).

## (e) DEM-DFT 보고서에 쓸 거리 (쪽 = 학술지 쪽 · '봤나' = 무엇으로 확인했나)

**연속체 · DEM 에 넣을 Li 금속 물성** (전부 실온 ≈26 °C · 다결정 지름 12.7 mm 막대 · 결정립 미측정):

| 쓸 것 | 값 · 조건 | 쪽 · 그림 · 표 | 봤나 |
|---|---|---|---|
| E · G · K · ν | **7.82 · 2.83 · 11.07 GPa · 0.381** (표 평균 ν 0.38) · 5 MHz 펄스-에코 · 높이 0.75 / 8.83 / 12.35 mm 평균 · 크기 무관 | p.2589–2590 · `Table 2` · 식 (1)–(4) | PDF 텍스트 전사 + 식으로 재계산 (반올림 안 정합) · 크롭 이미지는 안 봄 |
| ρ | 0.53–0.54 g/cc | `Table 2` | PDF 텍스트 |
| K 의 불확도 | 9.92–12.12 GPa (ν 0.37–0.39) — ν 0.01 → K ≈8 % | `Table 2` | 우리 산수 |
| 단결정 이방성 | Zener A = 8.43 · E⟨111⟩ 21.2 / ⟨100⟩ 3.0 GPa (2 차 · [22, 27, 34]) | p.2590 · `Table 1` | PDF 텍스트 |
| σ_y (인장) | **0.73–0.81 MPa** · 0.2 % offset · ε̇ 1.21–1.22 × 10⁻³ s⁻¹ · AR 1.10 — ⚠ 어느 E 에 어느 값인지 본문 · 표 · 그림이 다름 (그림 교점 `figure-read ≈` PE 0.63 · SS 0.73) | p.2590 · `Table 3` · `Fig. 2` 삽입도 | 표 = PDF 텍스트 + 손 크롭 이미지 · 그림 = Read + 2 배 확대 |
| 인장 최대 공칭 응력 | `figure-read ≈` 0.93 MPa @ ε 0.04–0.06 (그 뒤 ε 0.50 에서 0.49) | `Fig. 2` | Read |
| 크리프 법칙 (인장) | ε̇_min ∝ σⁿ · **n = 6.56** · 0.2–0.6 MPa · AR 3.96–4.64 · 최소 속도 시점 변형 0.2–5.7 % · ε̇ 2 × 10⁻⁷ – 3.9 × 10⁻⁴ s⁻¹ | p.2594–2595 · `Fig. 6` · `Table S1` | 그림 Read · 표 PDF 텍스트 · OLS 재현 n 6.562 ± 0.44 |
| 크리프 상수 A′ | **7.73 × 10⁻³ s⁻¹ MPa⁻ⁿ** (= 3.3 × 10⁻⁴² s⁻¹ Pa⁻ⁿ) — **카드 재회귀 · 논문 값 아님** · 유동 응력: 10⁻⁶ s⁻¹ → 0.26 · 10⁻⁵ → 0.36 · 10⁻⁴ → 0.52 · 1.2 × 10⁻³ → 0.75 MPa | `Table S1` | 우리 산수 |
| 속도 의존 검산 | 속도 500 배 → 유동 응력 2.6 배 (kalnaus2023 카드의 LePage 판독 2.2–2.9 배와 같음) | — | 우리 산수 · 이웃 카드 |
| Q_c · 온도 의존 | **없음** (한 온도) — 식 (7) 꼴만 | p.2593 식 (7) | PDF 텍스트 |
| 정규화 지수 | Li+Na+K **n 6.70** · 각 금속 2 점 · ⚠ D 인쇄값 (3.1 × 10⁻¹ cm²/s) 이 그림 (≈9 × 10⁻¹¹) 과 10⁹ 차 | p.2595 · `Fig. 7` | Read + 역산 |
| 압축 정하중 | 0.8–2.4 MPa · AR 1.89–2.57 · 광유 윤활 · 12/60/120 min 속도 (`Table S2`) — **구성 법칙 아님** (겉보기 지수 −1.4) · 구조 응답 검증 표적으로만 | p.2595–2597 · `Fig. 8` · `Fig. 9` · `Table S2` | 그림 Read + `Fig. 8` 픽셀 판독 · 표 PDF 텍스트 |
| 압축 응력–변형률 | 초기 0–3.93 ± 1.98 % 에 0.81 ± 0.10 MPa · 기울기 30.5 ± 16.6 MPa (항복 아님) · 공칭 끝 `figure-read ≈` 2.1 MPa @ 0.465 · ⚠ '진' 곡선 부호 오류 | p.2591–2592 · `Fig. 3` · `Fig. 4` | Read + 끝점 계산 |
| 시험 조건 | 크리프 접근 1.0 × 10⁻³ s⁻¹ → 정하중 · 100 점 이동평균 · 기록 10 Hz/1 N (항복) · 0.1 Hz/0.3 N/0.05 mm (크리프) · crosshead '1 mm/s' (1 mm/min 오기로 보임) | p.2587–2588 · `Fig. 1` | PDF 텍스트 · `Fig. 1` Read |
| 전지 쪽 변형률 속도 (차수) | 1 mA cm⁻² = Li 4.85 µm/h → 30 µm 층 균일 변형이면 ε̇ ≈4.5 × 10⁻⁵ s⁻¹ → 유동 응력 ≈0.46 MPa | (p.2588 의 30 µm 예) | 우리 산수 |

**W_ad 보고서 §7 (Li 친화성 정량화 · 점착 → 젖음각 · 공극 모델 입력) 에 쓸 점**:

| 쓸 것 | 내용 | 쪽 · 그림 | 봤나 |
|---|---|---|---|
| 점착이 역학적으로 왜 중요한가 | Li 가 SE · 집전체에 붙으면 마찰이 정수압 영역을 만들어 Li 압출 · 단락을 막는다 — **개념뿐 · 정량 0** | p.2598 · `Fig. 10` | Read + PDF 텍스트 |
| 그 '점착' 의 뜻 | 계면 전단 · 마찰 (*"if lithium adheres ... frictional forces"* · *"friction (or adhesive forces)"*) — 우리 W (법선 분리 에너지) 와 다른 양 | `Fig. 10` 캡션 · p.2599 | PDF 텍스트 |
| 점착이 크면 Li 탄성이 계면 응력에 중요 | *"recent analysis of the relatively high adhesion strength between Li and solid electrolyte [10, 23]"* | p.2589 | PDF 텍스트 |
| 마찰 '죽은 영역' 기전 | 끝면 마찰 → 정수압 쐐기 → barreling | p.2592 · `Fig. 4` | Read |
| 공극 모델의 Li 쪽 입력 | E · ν + n 6.56 · A′ (위 표) | 위 | — |
| γ_Li (Young–Dupré) | **없음** — W_ad 보고서 §7 이 적은 대로 같은 방법 · 같은 Li 면으로 계산해야 | — | — |
| 실전지 AR | 30 µm Li · 면적 500 · 1250 · 15000 cm² → AR 1.2 × 10⁻⁴ · 7.5 × 10⁻⁵ · 2.2 × 10⁻⁵ | p.2588 | PDF 텍스트 + 재현 |
| ⛔ '10⁴ 감속' | 후속 (Wang 2019 *Joule* PDF p.10) 이 이 논문 압축 데이터로 '마찰 · 점착 → 속도 10³–10⁴ 배 감속' 을 가정 — 이 논문 데이터 안은 부과 속도 대비 10²–10²·⁷ · 기하 포함 → 점착 근거로 쓰지 않는다 | `Fig. 8` · `Table S2` | wang2019 PDF 글자층 · `Fig. 8` 판독 |
| 우리 값 | W 값은 digest 에 안 실었다 — 위치만 (`docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` §2 쌍별 값 · §7 제안) · digest §7 이 인용한 우리 값은 canonical 둘뿐 (comp1 E_VRH 22.06 · B₀ 26.23 GPa · 방법 표지) · 우리 G 는 레지스트리 밖이라 안 옮김 | — | 레지스트리 확인 |

## (f) 그림 크롭 요약

- **15 장** = 도구 7 (`fig_4` · `fig_9` · `fig_10` · `tab_1` · `tab_2` · `tab_S1` · `tab_S2`) + **손 크롭 8** (`fig_1` · `fig_2` · `fig_3` · `fig_5` · `fig_6` · `fig_7` · `fig_8` · `tab_3`).
- 도구가 놓친 8 장 원인 (전부 같은 것): Springer **짧은 옆 캡션** (왼쪽 단 x 51–162 · 높이 33–69 pt < 0.6 × 폭) 이라 `_beside_rect` 의 '좁고 긴 캡션' 검사 (`min_tall=0.6`) 가 버렸다 → 그림 7 장 '그래픽 없음 (img0/draw1)' · `Table 3` 은 캡션 아래 빈 띠를 잘라 '거의 백지 (1.000)'.  그림은 전부 오른쪽에 박힌 래스터 (Im27–Im34) 라 그 사각형 + 4 pt 로 잘랐다 (figures.json `manual_crop` 에 좌표 · 원인).  ⇒ 도구 개선 후보 (메인 판단): 캡션 오른쪽에 큰 래스터가 캡션과 세로로 겹치면 키 조건을 풀기.
- 놓친 그림 0 · 오탐 0 · 번호 공백 0 (8 건 모두 `resolved`).  `Fig. 4` 캡션이 왼쪽 단에서 끊겨 오른쪽 단 이어지는 부분을 붙였다 (`caption_fix`).  `fig_9` · `fig_10` 크롭에는 옆 캡션 글자도 같이 들어 있다 (해 없음).  동영상 없음.
- **임시 파일 대조 (조정자 경고 뒤 · 2026-11-24)**: 공용 위치에 쓴 임시 파일 = scratchpad 루트 `masias_text.txt` (본문 글자 덤프) · `bi_before.txt` · `bi_after.txt` (+ 고유 하위 폴더 `masias_crop/`) — `masias_text.txt` 는 새로 뽑은 PyMuPDF 덤프와 **SHA-256 동일** (edb86db6…) · 1 쪽 제목 · 저자 5 명 · DOI 를 pdftotext 로 따로 확인 · digest 가 쓴 원문 문장 · 수치 40 개를 pdftotext (읽기 순서) 로 학술지 p.2586–2599 의 제자리에서 전부 다시 찾음 · `Table S1` 7 행 · `Table S2` 5 행 SI pdftotext 와 일치 · build_index 점검도 슬러그 폴더에서 다시 돌려 같은 결과 ⇒ **다른 논문 글자 섞임 없음** · 이후 임시 파일은 `scratchpad/masias2019_li_metal_elastic_plastic_creep_properties/` 에만.
- **본 것**: 그림 10/10 전부 + `tab_3` (크롭 확인).  **안 본 것**: `tab_1` · `tab_2` · `tab_S1` · `tab_S2` 이미지 (값은 PDF 텍스트).  그림이 본문과 어긋난 곳 6 (digest §10): `Fig. 2` 삽입도 (항복 짝) · `Fig. 2` 본 그래프 ('0.4 % 부터 감소' 아님) · `Fig. 3` ('진' 곡선 부호) · `Fig. 5` (최소점 · 1 차 구간) · `Fig. 7` (D 자릿수 · Li 2 점) · `Fig. 8` (`Table S2` 와 시각 원점).

## (g) Jeff Sakamoto 저자 여부

**예** — 마지막 저자 (Univ. Michigan 재료공학 · 기계공학) · 교신은 아님 (교신 = Alvaro Masias, Ford).  digest 저자 줄에 **Jeff Sakamoto** 로 적었고 웹앱 `_paper_pis` 가 `['sakamoto']` 를 돌려준다.  INDEX.md 행 둘째 칸 맨 앞 `🏷 **Jeff Sakamoto 공저** · ` 를 (a) 행에 넣어 두었다.
