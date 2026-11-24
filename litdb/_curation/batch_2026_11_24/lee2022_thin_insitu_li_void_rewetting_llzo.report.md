# 끝 보고 — lee2022_thin_insitu_li_void_rewetting_llzo (2026-11-24 · litdb-curator)

쓴 파일: `litdb/papers/lee2022_thin_insitu_li_void_rewetting_llzo.md` (508 줄 · 표 16 개 칸수 검사 0 건) · `litdb/figures/lee2022_thin_insitu_li_void_rewetting_llzo/` (크롭 31 장 + figures.json — 메인 체크포인트 커밋 b60590e6 에 이미 들어감) · 이 보고 파일.
공유 파일 · git 은 안 건드렸다. `build_index.py --check`: 이 slug 는 "어느 인덱스에도 없음 [dft]" · "comparison_vs_ours.md 미편입" 두 곳에만 뜬다 (아래 (a) (b) 를 넣으면 풀린다).
웹앱 확인 (읽기만): `_paper_pis` → `['sakamoto']` · 원소 태그 Cu · La · Li · O · Ta · Zr · 그림 주석 27 키 파싱됨 · `methods: XPS` 는 METHOD_MAP 에 없어 링크 0 (정상 — 이 논문은 목록의 계산 기법을 안 쓴다).

## (a) INDEX.md 행

넣을 절: **`## 🧲 계면 점착 · 인터레이어 트랙`** 표 끝 (권고 — W_ad 보고서 §7 · 연속체/DEM 공극 모델용) · 절 머리 조건 'LPSCl 이 한쪽 면' 에 안 맞으므로 행 안 ⛔ 표시를 유지한다. 대안: `## ✅ Digest 완료 (paper-level)` 본문 표 (build_index 분류는 [dft]).

```
| `papers/lee2022_thin_insitu_li_void_rewetting_llzo.md` **(본문 20 pp + SI 29 pp · 크롭 31장 (도구 30 = 본문 그림 7 + SI 그림 19 + SI 표 4 · 손 크롭 1 `Fig. S8` — 그래픽 SI p.12 · 캡션 p.13) 중 22장 실독 (본문 7/7 · SI 15/19) · 표 4장은 PDF 글자층 · 2026-11-24)** | 🏷 **Jeff Sakamoto 공저** · **[외부·exp·LLZO 계 · ⭐⭐⭐ 얇은 (5–20 µm) in situ Li 벗기기의 두 제한 기전 + 가열 다시 젖음 · W_ad 보고서 §7 · 연속체/DEM 공극 모델 보정 표적 · ⛔ 아지로다이트 아님 (SEI 없는 계면) · ⛔ 'rewetting' = EIS 접촉 회복 (접촉각 · 점착일 측정 0)]** ✅ **Kiwoong Lee**/Eric Kazyak/Michael J. Wang/**Neil P. Dasgupta\***/**Jeff Sakamoto\*** (Univ. of Michigan ME · MSE), "**Analyzing void formation and rewetting of thin in situ-formed Li anodes on LLZO**" — ***Joule* 6, 2547–2565 (2022)**, DOI `10.1016/j.joule.2022.09.009`. Ta-LLZO (Li₆.₅La₃Zr₁.₅Ta₀.₅O₁₂, 2 mm) 위 Cu 에 0.05 mA cm⁻² 로 Li 도금 (1–4 mAh cm⁻² = 5–20 µm) · 상온 · 5.6 MPa 벗기기: 10 µm 접근 용량 Q_A **1.688 → 0.710 mAh cm⁻²** (0.05 → 0.6 mA cm⁻², n = 3 · 0.6 은 단락 1) · 0.4 mA cm⁻² 에서 Q_A/Q_max **48.8 / 50 / 68 %** (5 / 10 / 20 µm) · 포일 13 %. **≤ 0.1 = Li 고갈 (Cu 노출 · EIS 차단 · 영구) / ≥ 0.4 = 공극 (operando GEIS R_int 48 → 9,115 Ω · bulk 637 → 811 Ω)**. 압력만으로는 몇 분 안에 부분 회복 (0.2 → 0.4 kΩ cm² 에서 멈춤) · 남은 Li 접근 불가 → **170 °C (T_H 0.97) · 1 MPa · 5 h 가열**로 R_int 46 → 162 → 92 → **48 Ω** · Q_A 1.04 → 1.07. COMSOL: 계면 ASR 은 공극 분율 0.9 이상에서 급등 · bulk 는 얇은 SE 에서만. ⚠ `Fig. 2C` = 셀 하나 (Test 1) · `Fig. S7B` 범례 반대로 읽힘 · `Fig. S20` AC 진폭 ≈ ±40 µA vs Methods 1 µA · `Table S3` σ 9 mS cm⁻¹ 는 모델 출력 (≈ 1 mS cm⁻¹) 과 10 배 · 마찰 · 점착 측정 0 | 점착 트랙 (W_ad 보고서 §7 다시 젖음 · 점착과 공극) · 얇은 Li 고갈 · 공극 성장 모델 보정 · anode-free 음극 |
```

## (b) comparison_vs_ours.md

넣는다 (build_index 미편입 해소용 — slug 경로가 Reference key 에 있어야 한다). 물성 4축 표 (A–D) 에는 넣지 않는다.

① `## 📑 Reference key` 표 (4 칸):
```
| **[Lee22ThinLi]** ⛔⛔ **가넷 (LLZO) · 실험 — A–D 물성 4축 진입 금지** · 🔧 얇은 in situ Li 벗기기의 두 제한 기전 (고갈 ≤ 0.1 · 공극 ≥ 0.4 mA cm⁻²) + 가열 다시 젖음 (170 °C · 1 MPa · 5 h) · ⛔ 'rewetting' = EIS 접촉 회복 (접촉각 · 점착일 측정 0) | **Kiwoong Lee**/E. Kazyak/M. J. Wang/**N. P. Dasgupta\***/**Jeff Sakamoto\*** (Univ. of Michigan) 2022 *Joule* 6, 2547–2565 (DOI 10.1016/j.joule.2022.09.009) | ✅ `papers/lee2022_thin_insitu_li_void_rewetting_llzo.md` | exp + COMSOL FEM (원자단위 계산 0) |
```
② `## E. 환원 / 음극(Li 금속) 계면` 표 맨 위 (4 칸 — 주장 | 출처 | 우리 | 일치):
```
| **🆕 (2026-11-24) 얇은 (5–20 µm) Li 를 벗길 때 저전류 (≤ 0.1 mA cm⁻²) 는 Li 고갈, 고전류 (≥ 0.4) 는 계면 공극이 벗기기를 끝낸다 — 공극 계면은 압력만으로 몇 분 안에 일부만 회복 (0.2 → 0.4 kΩ cm²) · 170 °C · 1 MPa · 5 h 가열이 완전 회복 · 저자: 황화물은 SEI 로 접근 용량이 더 낮고 마찰 · 점착이 다를 것 (측정 0)** | **[Lee22ThinLi]** `Table S1` · `Fig. 3` · `Fig. 6` · `Fig. 7` · `Table S4` (LLZO · 상온 · 5.6 MPa · LLZO 2 mm) | Li\|SE 공극 · 다시 젖음 계산 없음 · 아지로다이트\|Li 분해 산물은 §E 의 다른 행 · W_ad 쌍 (Ag–C · C–C · LPSCl\|Ag(111) · LPSCl\|흑연) 은 위치만 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` §2 · §7 | **비교 불가** (LLZO · 실험 · 양이 다름) — 방향 정보만 (황화물 SEI → 접근 용량 ↓ 는 우리 §E 산물 방향과 같은 쪽) |
```
③ (선택) `comparison_vs_ours_DEM.md` §I 에 `### I-11. lee2022_thin_insitu_li_void_rewetting_llzo — (인접 축 · 점착 측정 0) 얇은 Li 벗기기의 두 제한 기전 · 압력 회복의 부분성 · 가열 다시 젖음 — 공극 모델 보정 표적 (LLZO 한정)` — 본문은 digest §11 표를 옮기면 된다.

## (c) pdf_map.tsv

**불필요** — 자동 매칭이 된다 (`extract_figures.py --inbox --only lee2022_thin` → `[제목 84%]` 본문 `lee2022_thin_li_void_rewetting_main.pdf` · SI `lee2022_thin_li_void_rewetting_SI.pdf`).

## (d) 추가로 먹일 만한 논문 (8 편 · 최근 것 먼저)

⚠ 이 논문을 인용한 후속을 외부에서 찾으려 했는데 OpenAlex 가 프록시에서 막혔다 (403). 그래서 최근 편은 litdb 카드의 참고문헌 목록 (원문 전사) 에서 골랐고, 나머지는 이 논문 참고문헌이다. 8 편 모두 litdb 카드 없음 (2026-11-24 파일명 · 제목 grep).

| # | 서지 | 왜 | litdb |
|---|---|---|---|
| 1 | Z. Wang, J. Xia, X. Ji, et al., "Lithium Anode Interlayer Design For All-Solid-State Lithium-Metal Batteries," *Nature Energy* 9 (2024) 251–262 | Ag–C 류 인터레이어 설계 + Li 크리프 수송 모델 — Ag–C 층 · 공극 · 연속체 셋 다 | 카드 없음 (`kang2026_stress_regulated…` 참고문헌 [21] 에만) |
| 2 | C. Lin, H. Ruan, M. Wang, "Comprehensive Study of Li Deposition and Solid Electrolyte Cracking by Integrating Simulation and Experimental Data," *Advanced Science* 12 (2025) 2501434 | Li 를 크리프 점성 유체로 다루는 phase-field — 연속체 Li 흐름 꼴 | 카드 없음 (같은 카드 [47] 에만) |
| 3 | C. G. Haslam, J. B. Wolfenstine, J. Sakamoto, "The effect of aspect ratio on the mechanical behavior of Li metal in solid-state cells," *J. Power Sources* 520 (2022) 230831 | 이 논문 두께 효과 기전 (마찰 · hydrostatic pinning) 의 원전 — 얇은 Li 고갈 모델 경계조건 | 카드 없음 · Sakamoto 공저 (서지 표기 J. Sakamoto) |
| 4 | A. L. Davis, E. Kazyak, D. W. Liao, K. N. Wood, N. P. Dasgupta, "Operando analysis of interphase dynamics in anode-free solid-state batteries with sulfide electrolytes," *J. Electrochem. Soc.* 168 (2021) 070557 | 같은 질문의 **황화물판** (SEI · 도금 개시 지연) — LLZO 결과를 LPSCl 로 옮길 다리 | 카드 없음 |
| 5 | J. Kasemchainan et al., "Critical stripping current leads to dendrite formation on plating in lithium anode solid electrolyte cells," *Nat. Mater.* 18 (2019) 1105–1111 | 임계 벗기기 전류 · 공극 → 도금 덴드라이트 · 갇힌 공극 | 카드 없음 |
| 6 | U. Roy, N. A. Fleck, V. S. Deshpande, "An assessment of a mechanism for void growth in Li anodes," *Extreme Mech. Lett.* 46 (2021) 101307 | 공극 성장 연속체 기전 — DEM/연속체 모델 비교 기준 | 카드 없음 |
| 7 | Y.-G. Lee et al., "High-energy long-cycling all-solid-state lithium metal batteries enabled by silver–carbon composite anodes," *Nat. Energy* 5 (2020) 299–308 | Ag–C 음극 원전 (우리 점착 트랙의 출발점인데 카드가 없다) | 카드 없음 |
| 8 | M. Wang, J. B. Wolfenstine, J. Sakamoto, "Temperature dependent flux balance of the Li/Li₇La₃Zr₂O₁₂ interface," *Electrochim. Acta* 296 (2019) 842–847 | 온도로 흐름 균형을 바꾸는 선행 — 가열 다시 젖음의 앞 단계 | 카드 없음 · Sakamoto 공저 |

차순위: Masias 2021 *J. Mater. Res.* 36, 729 (ref 37 — Li 압축) · Krauskopf 2019 *Adv. Energy Mater.* 9, 1902568 (ref 30 — 확산 한계 × 온도 · 압력).
**이번 배치 inbox 에 이미 있어 뺀 것** (PDF 메타데이터로 확인): seymour2021 (*J. Mater. Chem. A* — 계면 점착 → 공극, 점착 → 공극의 인과는 이쪽이 정본) · afssb2024 (*Nat. Mater.* 2024 anode-free electro-chemo-mechanics) · difint2025 (*JES* 172, 070522 diffuse-interface 공극 모델) · fuchs2023 (*Adv. Energy Mater.* 13, 2203174 Cu\|LLZO 성장 모드) · viscoplastic2026 (*Matter* 9, 102767 아지로다이트 점소성 · 적층압) · agli2026 · agdist2025 · sputag2026 · kim2026_void_impedance · nicu2026 · wang2019 (= ref 26) · wang2020 (= ref 40) · masias2019 (*J. Mater. Sci.* 2019 — ref 37 과 **다른 논문**, Eq. S1 의 A · m · Q 를 찾을 곳) · kazyak2020 (= ref 17) · sharafi2017 · yang2021 × 2.

## (e) DEM-DFT 보고서에 쓸 거리 (전부 LLZO · 상온 · 5.6 MPa · LLZO 2 mm 한정)

**W_ad 보고서 §7 — Li 친화성**
- 이 논문에는 Li 친화성 지표가 **없다**. 쓸 수 있는 건 전제뿐: LLZO 는 Li₂CO₃ 를 400 °C · 3 h 로 없애고 Li 를 170 °C 로 붙여야 계면저항이 낮다 (p.17 Methods · 글자층 · refs 48–49 — sharafi2017 이 배치에 있음). Cu 위 in situ Li 핵생성 과전압 `figure-read ≈` −35 → −22 mV (`Fig. 1B` · 봄).

**§7 — 젖음과 다시 젖음**
- 다시 젖음 = **접촉 회복의 속도 문제** (Li 크리프 · 확산 · 압력 · 온도). 우리 §7 의 W 대 2γ_Li (열역학적으로 붙는 게 유리한가) 와 **다른 질문**이라고 같은 문단에 적는다.
- 가열: 170 °C (T_H 0.97) · 1 MPa · 5 h → R_int 46 → 162 → 92 → 48 Ω · Q_A 1.04 → 1.07 mAh cm⁻² (p.14–15 · `Fig. 7` 봄 · `Table S4` 글자층).
- 저온: 50 °C 5 h 첫 단계가 계면 꼬리 폭을 ≈ 90 → ≈ 50 Ω 로 대부분 줄이고 80–170 °C 는 더 안 줄인다 (`Fig. S17` 봄 · `figure-read` · 같은 셀 연속 가열이라 첫 단계만 깨끗) — 본문은 "80 °C 도 된다" 까지만 씀 (p.16).
- 압력만: 몇 분 안에 부분 회복 · 0.2 → 0.4 kΩ cm² 에서 멈춤 (`Fig. 6` 봄) · 12 h ≈ 2 일 (`Fig. S5B` 봄) · 남은 Li ≈ 0.9 mAh cm⁻² 은 다시 벗기면 `figure-read ≈` 0.017 mAh cm⁻² 에서 1 V (`Fig. S14` 봄).

**§7 — 점착과 공극**
- 점착 문장은 결론부 하나: *"As the replenishing Li flux is restricted by the adhesion, the accessible capacity is expected to vary based on the type of the SE"* (p.16 · 글자층) — **가설 · 측정 0**. 두께 효과도 마찰 · hydrostatic pinning 을 Haslam 2022 에서 빌린 해석 (p.7).
- 불균일 동역학 '핫스팟' 이 공극 핵생성 자리일 수 있다 (`Fig. S12` 봄) — 점착 불균일과 같은 꼴의 논증이지만 점착이 아니라 교환전류밀도로 모델링했다.

**연속체 · DEM — 얇은 Li 고갈 · 공극 성장**
- 보정 1 순위: Q_A(j) 10 µm = 1.688 / 1.479 / 1.335 / 1.031 / 0.710 mAh cm⁻² (0.05–0.6 mA cm⁻²) ± SD 0.014–0.052 · 불안정 구간 용량 0.044–0.168 (`Table S1` · SI p.7–8 · 글자층). ⚠ `Fig. 2C` 점은 평균이 아니라 Test 1 (봄).
- 두께: Q_A/Q_max 48.8 / 50 / 68 % (5 / 10 / 20 µm · 0.4 mA cm⁻² · p.7 · `Fig. 2B,D` 봄) — *우리 산수* Q_A 때 남은 두께 2.48 / 4.85 / 6.21 µm → **단일 임계 두께 문턱 모델이 안 맞는다** (공극 누적 이력 필요) — 모델의 첫 음성 시험으로 쓸 것.
- 압력: `figure-read ≈` 1 V 도달 0.69 / 0.94 / 1.11 mAh cm⁻² (0.56 / 1.4 / 5.6 MPa · `Fig. S7A` 봄 · 단일 셀).
- 두 기전 판별 표지: 고갈 = EIS 차단 꼬리 재등장 + bulk 1.5–2 배 · 공극 = 소폭 증가 + 공극 간격 수 µm (`Fig. 3` 봄 · p.8–10).
- 공극 성장 중 저항: R_int 48 → 901 → 3,872 → 6,829 → 9,115 Ω · bulk 637 → 811 Ω (2 / 5 / 10 / 15 V₀ · `Table S2` 글자층 · `Fig. 4` 봄).
- 접촉 분율 → 저항 지도: 계면 ASR 분율 0.9 이상 급등 · bulk 는 t/l 작을 때만 (`Fig. 5` · `Fig. S11` · `Fig. S12` 봄 · p.11–13). ⛔ 저항으로 공극 분율을 역산하지 않는다 — 같은 190× 가 균일 동역학이면 ≈ 0.99, 10× 불균일이면 ≈ 0.9 · `Table S3` σ 9 mS cm⁻¹ · 섭동 1 V 는 모델 출력 · SI 본문과 어긋남.
- 흐름 균형: Δl̇_creep = l·Aσ^m e^(−Q/RT) vs jM/(ρF) (SI p.9 · 글자층 · A · m · Q 수치 없음) · *우리 산수* 벗기기 4.85 µm h⁻¹ per mA cm⁻² · 공극 구간에 억지로 맞춘 ε̇ ≈ 1.1–1.3 × 10⁻⁴ s⁻¹ 은 **차수 확인용만**.
- 얇은 SE 경고: t/l = 0.4 면 bulk 도 공극에 반응 (`Fig. 5B` 봄) — 황화물 분리막 (수십 µm) 진단에 기하를 같이 본다.

## (f) 그림 크롭 요약

- 31 장 = 도구 30 (본문 그림 7 · SI 그림 19 · SI 표 4) + **손 크롭 1 `Fig. S8`** (도구 '번호 공백' — 그래픽이 SI p.12 단독 래스터, 캡션이 p.13 · figures.json `manual_crop` 사유 + `missing_labels` resolved 기록). 오탐 0 · 남은 놓친 번호 0.
- 실독 22 장: 본문 `Fig. 1`–`Fig. 7` 전부 · SI `S1` `S2` `S3` `S5` `S6` `S7` (+ S7B 확대) `S8` `S10` `S11` `S12` `S13` `S14` `S16` `S17` `S20`. 안 본 것: `S4` (도식) · `S9` · `S15` (주파수 라벨 재수록) · `S18` (SEM) · `S19` (XRD) · 표 4 장 (글자층으로 옮김). 단위 글리프 (µA · °C · Ω cm²) 는 쪽 렌더 확대로 따로 확인.
- 본문과 어긋난 그림: `Fig. 2C` (평균이 아니라 Test 1) · `Fig. S1` (캡션 0.4 vs 본문 0.05 mA cm⁻² — 곡선은 0.05 쪽) · `Fig. S7B` (범례대로면 '벗기기 전' 이 더 크다) · `Fig. S20` (AC 진폭 ≈ ±40 µA vs Methods 1 µA) · `Fig. S11B` / `Fig. 5C` / `Table S3` (모델 σ · 섭동 · 무공극 계면값 불일치) · `Fig. S8` (증착 Li 는 두께 분율 효과가 없다 — 본문 "같은 경향").

## (g) Jeff Sakamoto

**예 — 교신 저자이자 lead contact** (소속 ¹ ME · ² MSE · ³ lead contact). 공동 교신 Neil P. Dasgupta. 이해상충: Zakuro, Inc. 창업자 · 이 논문 얇은 Li 제조법 (in situ 도금) 특허 공동 발명자. digest 저자 줄에 **Jeff Sakamoto** 로 적었고 웹앱 배지 판정 (`_paper_pis`) 이 `sakamoto` 로 잡는 것을 확인했다.
