# 끝 보고 — 묶음 2026-11-24b · 8 번 · `ko2025_metal_interlayer_anode_less_li_plating_stripping_mechanism`

> Ko 외 · *Nat. Commun.*, 16, 1066 (2025) · DOI 10.1038/s41467-025-55821-1 · digest `litdb/papers/ko2025_metal_interlayer_anode_less_li_plating_stripping_mechanism.md` (575 행) · 그림 `litdb/figures/ko2025_metal_interlayer_anode_less_li_plating_stripping_mechanism/` (크롭 36 + `video_frames/` 141)
> 입력 해시 10 개 (본문 · SI · zip · 영상 7) 전부 batch.json 과 같음 · 쓴 파일 = digest · 그림 폴더 · 이 보고 셋 · git · 공유 파일 손 안 댐 (예외 하나 — (f) 끝 줄).

## 먼저 — 메인 세션이 알아야 할 것 다섯

1. **SE 는 가넷 LLZTO (산화물)** 이고 operando 셀은 적층압 없이 윗면이 열려 있어요. CE · 분극 · 두께는 LPSCl 로 안 옮기고, 기전 · 순서 · 계산 후보만 가져와요.
2. **원자료 xlsx 22 개로 다시 내 보니 본문 · 캡션과 어긋난 곳이 열 곳이 넘어요** (digest §11 · 17 항목). 제일 큰 것: 본문은 *"Li diffusivity in Au is higher than that in Ag"* (`Fig. S11` 근거) 인데 그 그림 · 원자료는 **Li–Ag 가 ≈ 2.4 자릿수 커요** (중앙값 8.0 × 10⁻¹⁵ 대 3.0 × 10⁻¹⁷ cm² s⁻¹). '확산으로는 설명 못 한다' 논증이 근거를 잃어요.
3. 풀셀 고장은 캡션의 '0.9 mA cm⁻² 방전 초기' 가 아니라 원자료상 **1.0 mA cm⁻² 충전 중** 이고 (0.9 에서 5 사이클 완주), `Fig. 4b` · `Fig. S9b` 의 가로축 'Time (h)' 는 실제로 **면적 용량** 이에요 (끝값 = `Fig. 4c` 용량 · 넷째 자리까지).
4. 대표성 근거 그림 `Fig. S6` 의 'Operando XPS' 열은 XPS 셀이 아니라 **XRD 30 분 런의 전압 200/200 점 + 시간 정확히 ½** 이고, `Fig. 3a` (사후 코인셀이라는 그림) 원자료는 **operando SEM 셀과 6680/6680 점이 같아요.**
5. CE 순위 Ag > Zn > Au > Cu 는 SEM 셀 하나씩의 값이에요. 같은 구성의 XPS 셀은 첫 사이클이 **Zn 97.8 > Ag 89.5 %** 라 Ag · Zn 순서는 견고하지 않아요 (Cu · Au 가 나쁜 건 두 기법에서 같아요).

---

## (a) INDEX 행 + 절

- **절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 한 묶음)` (INDEX.md 777 행 절) — 11-24b 묶음을 따로 절로 묶으면 그 절. `build_index.py --check` 의 트랙 판정은 **[dft] → INDEX.md** 예요.
- **🏷 Jeff Sakamoto 표지 없음** ((g)).
- **🎤 talk 역링크**: 해당 없음 — `talks/*.md` 인입 대기열 (`lee2026_skku_mlip_materials_design.md` 하나) 에 이 논문이 없어요.

```
| `papers/ko2025_metal_interlayer_anode_less_li_plating_stripping_mechanism.md` **(본문 13 pp + SI 34 pp (Fig. S1–S29 · Table S1) · 원자료 xlsx 22 · 동영상 7 · 크롭 36장 (도구 35 + 손 1 · 다시 자름 3) 중 16장 실독 · 영상 프레임 134장 + 모아보기 7장 · 2026-11-24)** | **[외부·exp + DFT 벌크 hull·⭐⭐ 금속 인터레이어 (Cu · Au · Ag · Zn 200 nm) on 가넷 LLZTO — Li 석출 자리가 금속마다 갈린다 · ⚠ LLZO 계 (Li 와 안정 · LPSCl 로 수치 이식 금지) · operando 셀 적층압 없음 · 금속당 셀 1 개]** ✅ **Dong-Su Ko**/**Sewon Kim** (공동1)/S. Lee/G. Yoon/D. Kim/C. Shin/D. Kim/J. Lee/S. Sul/**Dong-Jin Yun\***/**Changhoon Jung\***, "**Mechanism of stable lithium plating and stripping in a metal-interlayer-inserted anode-less solid-state lithium metal battery**" — ***Nat. Commun.* 16, 1066 (2025)**, DOI `10.1038/s41467-025-55821-1` (OA CC BY-NC-ND). 0.1 mA cm⁻² · 0.25 mAh cm⁻²: **Cu** 는 Cu 막 아래 Li 기둥 → Cu 들림 · 공극 (CE ≈ 20 %) · **Au** 는 Li–Au 합금 아래 Li → 볼업 · 층 박리 (≈ 55 %) · **Ag** 는 층 전체가 β → γ3 → γ2 → Li₃Ag → γ1 로 바뀌며 200 → ≈ 1000 nm · Li 는 합금을 지나 윗면에 덩어리 → 막 · 합금 \| LLZO 접촉 유지 (≈ 86 %) · **Zn** 은 LiZn 만 · 수염 남음 (≈ 76 %) · PBEsol hull γ2 15 · γ1 11 meV/atom 위 · cryo-TEM 석출 Li 속 나노 Li₃Ag · 표면 Ag ≈ 20 %. ⚠ 원자료 대조: **GITT 는 Li–Ag 가 ≈ 2.4 자릿수 큼 (본문 'Au 가 빠르다' 와 반대)** · 풀셀 고장 = 1.0 충전 (캡션 '0.9 방전' 아님) · Fig. 4b · S9b 가로축 = 용량 · Fig. S6 'XPS' 열 = XRD 런 (시간 ½) · Fig. 3a 원자료 = operando SEM 셀 · XPS 셀 첫 CE Zn 97.8 > Ag 89.5 % · 코인셀 '점착 낮은 쪽 (합금 \| Cu) 석출' 은 측정 없는 추론 | 점착 트랙 · W_ad §7-1 Ag · Cu 행 · §8-3 석출 자리 · Li–Ag 상 순서 |
```

## (b) comparison 줄 (`comparison_vs_ours.md`)

**참조 키 (📑 Reference key 표 · 열 = 약칭 \| 논문 \| digest/status \| 유형)**

```
| **[Ko25MIL]** ⭐⭐ **금속 인터레이어 (Cu · Au · Ag · Zn 200 nm) on 가넷 — Li 석출 자리 · Li–Ag 상 순서 (operando SEM · XPS · XRD · cryo-TEM) + PBEsol Li–Ag hull** · ⛔ **LLZO (Li 와 안정) · A–D 물성 4축 진입 금지** (§E 1 행만) · ⚠ 원자료와 본문 어긋남 다수 (GITT 방향 · 고장 조건 · 대표성 그림) | D.-S. Ko/S. Kim/S. Lee/G. Yoon/D. Kim/C. Shin/D. Kim/J. Lee/S. Sul/D.-J. Yun\*/C. Jung\* *Nat. Commun.* 16, 1066 (2025) | `papers/ko2025_metal_interlayer_anode_less_li_plating_stripping_mechanism.md` ✅ | exp + DFT |
```

**§E 환원 / 음극 (Li 금속) 계면 (열 = 주장 \| 출처 \| 우리 \| 일치)**

```
| **🆕 (2026-11-24) 금속 인터레이어 종류가 Li 석출 자리를 가른다 — Ag 는 Li–Ag 합금 (β → γ3 → γ2 → Li₃Ag → γ1) 을 지나 SE 반대쪽에 Li 를 쌓고 합금 \| SE 접촉을 지킨다 · Au · Cu 는 SE 쪽에 쌓여 층을 들어 올린다 · 첫 CE Ag > Zn > Au > Cu (SEM 셀 1 개씩 · XPS 셀은 Zn ≥ Ag)** | **[Ko25MIL]** `Fig. 1` · `Fig. 3c` · `Fig. 5c` · `Fig. S4` · `Fig. S20` · p.3–p.9 (LLZTO · 0.1 mA cm⁻² · 0.25 mAh cm⁻² · operando 셀 적층압 없음) | 우리 음극 축은 SE 환원 산물 화학 (1.717 V 가장자리 · grand-potential) 뿐 — Li–Ag 합금 계면 · Li \| Cu W 는 W_ad 보고서 §7-1 제안 단계 (미계산) · 이 논문 DFT 는 PBEsol 벌크 hull 뿐이라 같은 양 없음 | — 축 다름 · ⛔ LLZO 의 CE · 분극 · 두께를 LPSCl 로 옮기지 않는다 · 🟡 계산 후보 (Li₁₀Ag₃ · Li₃Ag · Li₁₂Ag 면 · 합금 \| Cu · 합금 \| SE) 만 이식 · ⛔ 'Li–Au 확산이 더 빠르다' 인용 금지 (자기 원자료와 반대) |
```

## (c) pdf_map 줄

**필요 없어요.** digest 를 쓴 뒤 `extract_figures.py --inbox --only ko2025 --dry` 가 **[제목 100 %]** 로 본문 (`ko2025_metal_interlayer_anode_less_main.pdf`) · SI (`…_SI.pdf`) 를 둘 다 붙였어요. (굳이 넣는다면 `ko2025_metal_interlayer_anode_less_li_plating_stripping_mechanism<TAB>ko2025_metal_interlayer_anode_less`.)

## (d) 추가로 먹일 논문 ≤ 8 (최근 먼저 · litdb 유무 · 기존 목록 유무)

발견 검색은 Crossref 로 주제어 + 연도 (2025 이후 · 제목 없이) 4 번 → DOI 확인 4 번 (+ 재시도 1). OpenAlex (정방향 인용 찾기) 는 이 세션 프록시가 막아서 (403) 안 썼어요. 대조 = `litdb/papers/*.md` grep + `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md`.

| # | 논문 (랩 인용 꼴) | DOI | 왜 (W_ad 보고서 자리) | litdb | 기존 목록 |
|---|---|---|---|---|---|
| 1 | Liu 외 · 탄소 인터레이어 전처리와 무음극 셀의 석출 Li 안정성 · *Electrochim. Acta*, 574, 149375 (2026) | 10.1016/j.electacta.2026.149375 | 탄소 층을 먼저 리튬화하면 Li 가 어디 서나 — 7-1 흑연 · LiC₆ 행 · 8-3 | 없음 | 없음 (발견 검색) |
| 2 | Liu 외 · 계면 Ag 층을 둔 Li–Ag 합금 음극 (Li₃InCl₆ 할라이드 SE) · *J. Power Sources*, 647, 237357 (2025) | 10.1016/j.jpowsour.2025.237357 | SE 쪽 Ag 층 + Li–Ag 합금 — 산화물 · 황화물 아닌 계에서 합금 면 · 7-1 Ag 행 | 없음 | 없음 (발견 검색) |
| 3 | Orlandi 외 · Li \| Li₂O 계면 원자 구조 (제일원리) · *ACS Appl. Mater. Interfaces*, 17, 21958 (2025) | 10.1021/acsami.4c22106 | 8-2 '반응 뒤 표면' (산화된 Cu 가 Li 와 반응한 Li₂O) 의 DFT 계면 구조 — 7-1 Cu 행 | 없음 | 없음 (발견 검색) |
| 4 | Park 외 · Ag–C 다공 인터레이어 안 Li 동역학 · *Adv. Energy Mater.*, 15, 2405129 (2025) | 10.1002/aenm.202405129 | Ag–C 층 안 Li 경로 — 8-3 | 없음 (이웃 digest 에 인용만) | **목록에 있음** (표 1 #9) |
| 5 | Sandoval 외 · 무음극 전고체전지의 합금 계면층 구조 · 전기화학 변화 · *Joule*, 7, 2054 (2023) | 목록에 있음 | **이 논문의 질문을 LPSCl \| Cu 에서** (Au · Ag 등) — 우선순위 1 | 없음 (이웃 digest 에 인용만) | **목록에 있음** (표 2 #6) |
| 6 | Inaoka 외 · Li/Li₃PS₄ 계면 Sn 인터레이어 · *J. Phys. Chem. C*, 127, 10453 (2023) | 10.1021/acs.jpcc.3c01740 | 이 논문 ref 31 · 황화물에서 '고용 없는 금속 층' 대조 | 없음 | 없음 |
| 7 | Li B. 외 · Li₆PS₅Cl 과 쓰는 Li–Ag 합금 음극 (이중 보호) · *ACS Appl. Mater. Interfaces*, 14, 37738 (2022) | 10.1021/acsami.2c09013 | 이 논문 ref 39 · 황화물 계에서도 탈리튬화 중 Li₃Ag 가 나오나 — 7-1 Ag 행 합금 면 후보 | 없음 | 없음 |
| 8 | Kim S. 외 · 가넷을 지나는 Li 성장에서 인터레이어 화학 (Ag · Au · Si) · *Adv. Energy Mater.*, 10, 1903993 (2020) | 10.1002/aenm.201903993 | 이 논문 ref 27 · 직접 선행 (Au 가 나쁜 이유의 첫 보고) | 없음 | 없음 |

- 번외: Braga 외 · Ag–Li 계 실험 + 제일원리 · *J. Alloys Compd.*, 817, 152811 (2020) · DOI 10.1016/j.jallcom.2019.152811 (ref 40) — 7 절 3 번 hull 위상 대조의 둘째 출처.
- 이번 묶음이라 다시 넣지 않음 (서지만): *Energy Environ. Sci.*, 19, 5836 (2026) (2 번) · *Energy Environ. Sci.*, 19, 2367 (2026) (3 번) · *ACS Energy Lett.*, 10, 2285 (2025) (4 번) · *Nat. Commun.*, 16, 5871 (2025) (5 번) · *Nat. Energy*, 5, 299 (2020) (9 번) · *Adv. Energy Mater.*, 14, 2302960 (2024) (11 번).
- ⚠ #1 · #2 · #3 은 Crossref 메타 (제목 · 저널 · 권 · 쪽) 만 봤고 초록 · 본문은 안 봤어요. #2 제목은 검색 결과에서 잘린 꼴로만 봤어요.

## (e) DEM-DFT (W_ad) 보고서에 쓸 거리 — 쪽 · 그림 · 원자료 · 직접 봤는지

보고서 7 절 (7-1 표 Ag · Cu 행) · 8-3 절을 먼저 읽고 맞췄어요. 값 규율: 아래 숫자는 이 논문의 계 (LLZTO · 0.1 mA cm⁻² · 0.25 mAh cm⁻² · 적층압 없음) 값이고 보고서 2 절의 우리 W 와 같은 표에 두지 않아요. 우리 W 값은 digest · 이 보고에 안 실었어요 (위치만).

### e-1. 셀 조건 — 금속마다 (질문 1 · digest §3)

| 항목 | Cu | Au | Ag | Zn | 근거 · 봤나 |
|---|---|---|---|---|---|
| SE | Li₆.₅La₃Zr₁.₅Ta₀.₅O₁₂ 펠릿 500 µm · ⌀14 mm · P3000 연마 + 1 M HCl 3 min · σ 0.74 mS cm⁻¹ (25 °C) | 같음 | 같음 | 같음 | p.10 · `Fig. S28` (안 봄) |
| 금속 층 | 200 nm | 200 nm (풀셀 100) | 200 nm (풀셀 100 · TEM 30) | 200 nm | p.10 · p.5 · p.8 |
| 만든 법 | RF 마그네트론 스퍼터 · 150 W · Ar 5 × 10⁻³ Torr · 22 °C · ⌀12 mm 마스크 · 글러브박스 연결 | 같음 | 같음 (10 nm min⁻¹) | 같음 | p.10 |
| 전류 · 용량 | 0.1 mA cm⁻² · 0.25 mAh cm⁻² (석출 2.50 h) | 같음 · 반셀 0.1 · 풀셀 0.1–0.3 | 같음 · XRD 셀 0.05 × 5 h (원자료 추정) · CCD 석출 0.1–1.0 / 박리 0.05 · 풀셀 0.1–1.0 | 같음 | [원자료 Fig.1(a) · SFig.19(a)] · p.10–11 |
| 압력 | operando: 적층압 없음 (Cu 탐침 한 점) · 코인셀 미기재 · 상대극 Li 는 CIP 250 MPa 3 min 로 붙임 | 같음 | 같음 | 같음 | p.10–11 · p.5 |
| 온도 | 코인 · 풀셀 25 °C · operando 미기재 | 같음 | 같음 | 같음 | p.10 |
| 집전체 (작업극 쪽) | operando 없음 (윗면 열림) · 반셀 · 사후 · 풀셀 10 µm Cu 박 | 같음 | 같음 | 같음 | p.10 · p.11 |
| 박리 끝 | 4 V | 4 V | 4 V | 4 V (XRD 런만 5.0 V) | p.11 · [원자료 SFig.15(a)] |

### e-2. 금속마다 Li 자리 · 꼴 · 남는 것 · 합금상 · 부피 · CE · 분극 (질문 2 · digest §5)

| 금속 | Li 자리 (EoLP) | 꼴 | 박리 뒤 | 합금상 | 부피 | CE 순위 | 분극 순위 (석출 / 박리) | 근거 · 봤나 |
|---|---|---|---|---|---|---|---|---|
| Cu | **Cu 막 아래** — Cu 가 들림 (측정) | 기둥 (옆 ≈ 15 µm 뒤 수직) + 수백 nm 수염 · 자리 무작위 | 기둥 · 수염 대부분 · LLZO \| 기둥 공극 | 없음 | — | 4 위 | 2 위 / 4 위 (가장 큼) | `Fig. 1b` · `Fig. S4a` · Movie 2 — 봄 |
| Au | **Li–Au 합금 층 아래** — 층 들림 · 볼업 (측정) | 수십 µm 볼업 · 수염 · 기둥 없음 · 껍질 밑 ≈ 10 µm Li (figure-read) | 볼업 일부 · 층 박리 | XRD 지정 Li₃Au · Li₁₅Au₄ 등 · 비가역 · 표면 Li:Au ≈ 1:1 | 정량 없음 | 3 위 · 반셀 5 사이클 뒤 · 풀셀 0.3 에서 단락 | 4 위 (가장 큼 · 불안정) / 3 위 | `Fig. 1c` · `Fig. S4b` · `Fig. S16` · Movie 3 — 봄 · `Fig. S9` 원자료만 |
| Ag | **합금 층 위** (열린 윗면 · 측정) · 코인셀은 합금 \| Cu 쪽 (**추론**) · 합금 \| LLZO 접촉 유지 (측정) | 불규칙 덩어리 → 얇은 막 · 수염은 옆으로 눕는다 · 결함 자리만 수십 µm 기둥 | 가장 적음 · 합금 층 ≈ 300 nm | β → γ3 → γ2 → Li₃Ag → γ1 (탈리튬화 γ1 → Li₃Ag → γ2 → γ3 → β) · 석출 Li 속 Li₃Ag 나노입자 · 표면 Ag ≈ 20 % | 200 → ≈ 1000 nm (× 5) · 박리 중 부푼 채 (V ≈ 900 nm 대 질량 수지 ≈ 390) | 1 위 · 반셀 962 사이클 (원자료 600 까지) · CCD 0.8 · 풀셀 0.9 | 3 위 / 2 위 | `Fig. 1d` · `Fig. 3` · `Fig. 5` · `Fig. 6` · `Fig. 2c` · Movie 4 — 봄 · [원자료 Fig.5(c) · Fig.2(c) · Fig.3(a)] |
| Zn | 얇고 끊긴 Li–Zn 층 **위로** 수염 · 덩어리 (측정 · 요약 문단은 '계면' 쪽으로 묶음) | 수염 위주 + 덩어리 약간 | 수염 그대로 · 덩어리는 빠짐 | LiZn 만 (약한 봉우리 하나) | 정량 없음 | 2 위 (XPS 셀 첫 사이클은 1 위) | 1 위 (가장 작음) / 1 위 | `Fig. 1e` · `Fig. S4d` · `Fig. S15` · `Fig. 2d` · Movie 5 — 봄 |

- CE 상대 (SEM 셀 · 본문 20 · 55 · 76 · 86 %): Ag ≈ Cu 의 4.3 배 · Au 의 1.6 배 · Zn 의 1.1 배. 원자료 시간 비 19.9 · 53.7 · 78.0 · 85.1 % 도 같은 순위.
- 분극 상대 [원자료 SFig.3 중앙값]: 석출 평탄 Au ≈ Ag 의 3–4 배 · Ag ≈ Zn 의 2 배 · Cu ≈ Zn · 박리 첫 평탄 Cu ≈ Ag 의 13 배 · Ag ≈ Zn 의 2 배. 두 전극 셀 분극이라 금속 층 과전압이 아니고, `Fig. S3a` Cu 확대 판은 원자료와 ≈ 60 mV 어긋나요 (그림을 믿으면 Cu 가 Ag 보다 커져 순위가 바뀜).
- 부피 [우리 산수 · Table S1 측정 격자상수]: Ag 원자당 β × 1.88 · γ3 × 3.24 · Li₃Ag × 4.09 · γ2 × 4.44 · γ1 × 14.0–14.2.

### e-3. 기전 주장 — 측정 대 추론 (질문 3 · digest §6 · §7)

- **측정**: 금속별 석출 자리 (SEM 영상 · FIB) · Ag 두께 200 → 1000 nm · Ag 상 순서 (XRD 두 속도 · 속도 바꾼 XRD) · 석출 Li 속 Li₃Ag (cryo-TEM SADP) · Ag 나노입자 자발 리튬화 (SEM 15 h · TEM) · in-situ TEM 의 Ag 입계 벌어짐 · Ag 덩어리 이동 · GITT (단 본문과 반대 방향).
- **추론**: γ2 → Li₃Ag + Li 상분리가 '핵생성 장벽 없는' 석출 자리 (스피노달 — 조직이 닮았다는 것뿐 · 저자도 조성 조건 미충족 인정) · 코인셀은 '점착이 낮은 쪽 = 합금 \| Cu' 에 쌓임 (점착 측정 0 · 단면에 Cu 박 없음) · Au 는 Li-rich 합금을 못 만들어 계면에 쌓임 (자기 XRD 가 Li₃Au · Li₁₅Au₄ 를 지정해 긴장) · Ag 가 녹은 δ-Li 가 수지상을 막음 (표면 Ag ≈ 20 % 는 저자가 적은 고용 한계 '수 at%' 의 몇 배 → Li₃Ag 섞임으로 읽힘) · 바이어스가 Ag 를 Li 로 녹임 (Ag 가 양극 · 무바이어스 대조 없음).
- **계산 (DFT)**: VASP · PBEsol · PAW · 520 eV · 0.5 meV/atom · γ 상마다 배열 30 개 중 최저 · 0 K · 엔트로피 없음 · k 점 · 셀 n/a · 계면 계산 0. [원자료 SFig.20] 으로 hull 재구성: γ2 15.1 · γ1 11.3 meV/atom 위 (본문 15 · 11 ✓) · Li₉Ag₄ 는 1.3 meV/atom 차로 겨우 hull 위 — 배열 펼침 7–9 meV/atom 와 같은 크기라 범함수 · 배열 · 엔트로피로 뒤집힐 수 있어요.
- **우리 기준선 대조**: 같은 양 없음 (축 A–D 해당 없음 · §E 는 SE 환원 산물 화학뿐 · W_ad 는 PBE + D3(BJ) 고정 기하 W_sep 이고 Li \| 금속 · 합금은 7 절 제안 단계). 우리가 Li–Ag 합금 구동력 (7 절 3 번) 을 내면 **hull 위 상 목록 (위상) 만** 이 논문과 견줘요.

### e-4. litdb 이웃 (질문 4 · digest §8)

| 이웃 | 맞는 점 | 다른 점 |
|---|---|---|
| Metzler 2026 (스퍼터 Ag on 탄소 · LPSCl) | Li 가 Ag 함유 층을 지나 집전체 쪽에 쌓이고 Ag 가 Li 속으로 간다 | 이 논문은 Ag 가 SE 쪽 · 탄소 없음 · 박리 뒤 Ag 가 LLZO 위 합금 층 (≈ 300 nm) 으로 남음 · SE 다름 |
| Metzler 2025 (Ag/CB 분포) | 'Ag 가 Li 통로' 그림과 맞음 | 3 전극 핵생성 과전압을 안 잼 |
| Kang 2026 (Ag–C + CNF · 하중 셀) | 충전 층에 Li-rich Li–Ag 상 | 이 논문은 압력 · 응력을 안 잼 (축이 다름) |
| Spencer-Jolly 2023 (Ag–흑연 · LPSCl · operando XRD) | β → γ3 → γ2 까지 같은 순서 · 탈리튬화가 단순 역경로 아님 | 이 논문은 그 뒤 **Li₃Ag · γ1 (Li₁₂Ag)** 까지 — 직접 전기화학 리튬화 · Ag 당 Li 많음 (x 4.8) · 흑연이 Li 를 먼저 안 가져감 [추론] |
| Fuchs 2023 (Cu \| LLZO) | 얇은 Cu 막은 Li 를 못 가둔다 (200 nm Cu 가 들림) · 같은 LLZO · 0.1 mA cm⁻² 는 Fuchs 범위 안 | 핵 밀도 · 성장 모드를 안 셈 |
| (덧붙임) Liao 2025 (탄소 층 박리 인성 · LPSCl) | '점착 낮은 쪽에 석출' 과 같은 방향 | Liao 는 잰 실용 G_c · 이 논문은 측정 없는 추론 · 둘 다 DFT W_sep 와 다른 양 |

병렬 묶음 2 · 9 · 11 번은 파일을 안 읽었고 서지로만 적었어요.

### e-5. 보고서 자리별로 쓸 것

| 보고서 자리 | 쓸 것 | 쪽 · 그림 · 원자료 | 봤나 |
|---|---|---|---|
| **7-1 표 Ag 행** ('충전 중 Li–Ag 합금 면 후보') | 200 nm Ag 가 Li ≈ 0.05 mAh cm⁻² (x ≈ 1) 만에 β 로 다 바뀌고 석출 내내 Li 가 만나는 면은 γ-brass (Li₉Ag₄ · Li₁₀Ag₃ · Li₁₂Ag) · Li₃Ag · 석출 Li 속에도 Li₃Ag ⇒ 합금 면 후보를 **Li₁₀Ag₃ · Li₃Ag · Li₁₂Ag** 로 좁힘 · Li 쪽도 순수 Li 가 아닐 수 있음 | p.6–9 · `Fig. 5c` · `Fig. 6a–d` · `Fig. 2c` · [원자료 Fig.5(c) · Fig.2(c)] | 봄 |
| **7 절 3 번** (합금 구동력) | PBEsol hull 위상 (β · γ3 · Li₃Ag 위 · γ2 · γ1 준안정) 을 대조 표적으로 · 절대값은 안 견줌 · 정합 셀 변형 기준은 `Table S1` 측정 격자상수 | p.7 · p.11 · `Fig. S20` · `Table S1` · [원자료 SFig.20] | 봄 (표는 글자) |
| **7-1 표 Cu 행** (맨 집전체 Li \| Cu) | 얇은 Cu 막 아래 Li 기둥 → Cu 들림 · 박리 공극 · CE ≈ 20 % — Cu 를 '합금 안 하는 소Li 대조' 로 씀 | p.3 · `Fig. 1b` · `Fig. S4a` · Movie 2 | 봄 |
| **8-3** (Li 가 어디 쌓이나 · W 를 낼 계면) | Ag 가 SE 쪽에 있어도 Li 는 합금을 지나 반대쪽 (측정) · Au · Cu 는 SE 쪽 (측정) · 코인셀 '합금 \| Cu' (추론) ⇒ 계면 후보에 **Li–Ag 합금 \| Cu · Li–Ag 합금 \| SE** 추가 · 8-3 의 'W(집전체 \| SE) − W(Li \| 집전체) − W(Li \| SE)' 꼴을 합금 층으로 늘려 **W(합금 \| CC) 대 W(합금 \| SE) 의 순서** 질문 | p.3–4 · p.6 · p.9 · `Fig. 1` · `Fig. 3c` · `Fig. S4` | 봄 (추론 부분은 원문 문장) |
| **8-1 · 8-4** (박리 공극) | 박리 중 합금 층이 부푼 채 빈 곳을 품음 (V ≈ 900 nm 대 질량 수지 ≈ 390 nm) — '접촉 유지' ≠ '꽉 찬 접촉' | `Fig. 3c` · `Fig. 3d` · digest §4.3 [우리 산수] | 봄 |
| **8-6** (가져오지 않는 것) | LLZTO 숫자 · 셀 하나씩 CE 순위 · GITT 방향 · 풀셀 고장 조건 (캡션) | digest §11 | — |

**보고서 문장 후보 (한국어 · 랩 인용 꼴 · 회사 이름 없음)**
- 가넷 고체전해질 위 200 nm Ag 층은 Li 가 쌓이는 동안 β-LiAg → Li₉Ag₄ → Li₁₀Ag₃ → Li₃Ag → Li₁₂Ag 로 차례로 바뀌고, Li 는 리튬화된 층을 지나 전해질 반대쪽에 쌓이며 합금 | 전해질 접촉은 유지됐다 (*Nat. Commun.*, 16, 1066 (2025)).
- 같은 셀에서 Au · Cu 층은 전해질 쪽에 Li 가 쌓여 층이 들렸고, 첫 사이클 쿨롱 효율은 Ag > Zn > Au > Cu 순이었다 (*Nat. Commun.*, 16, 1066 (2025)) — 적층압 없는 operando 셀 하나씩의 값이다.
- 그래서 충전 중 Li 가 만나는 은 쪽 면은 Ag(111) 이 아니라 Li-rich Li–Ag 합금 (Li₁₀Ag₃ · Li₃Ag · Li₁₂Ag) 이고, 석출된 Li 안에도 Li₃Ag 나노입자가 섞여 있었다 (*Nat. Commun.*, 16, 1066 (2025)).
- (조건부) 저자들은 적층압 아래에서는 점착이 낮은 쪽 (합금 | 집전체) 에 Li 가 쌓인다고 제안했지만 점착은 재지 않았다 (*Nat. Commun.*, 16, 1066 (2025)) — 같은 방향의 실측은 탄소 층의 박리 인성에서 나왔다 (*Adv. Mater.*, 37, 2502114 (2025)).
- ⛔ 쓰지 않을 문장: 'Li–Au 에서 Li 확산이 더 빠르다' (자기 원자료와 반대) · 'Ag 풀셀은 0.9 mA cm⁻² 방전에서 고장' (원자료는 1.0 충전) · 'Ag 가 녹은 δ-Li 고용체가 수지상을 막는다' (추론).

## (f) 그림 · 동영상 크롭 요약

- **그림 36 장** (`figures.json` 36 행): 도구 35 (본문 5 · SI 29 · 표 1) + **손 크롭 1** (`fig_2.png` — 도구가 'p5 영역 없음' 으로 뺀 Fig. 2 · `manual_crop` 사유 · `missing_labels` f2 에 `resolved`) · **다시 자름 3** (`recrop` 사유): `fig_3.png` (도구가 e 판 모식도 띠만 잡음 → a–e 전체) · `fig_4.png` (오른 축 'Coulombic efficiency (%)' 잘림 → 오른쪽 끝 513 pt) · `fig_6.png` (위쪽 판 글자 a–d · 상태 이름 잘림 → 위 끝 45 pt). `⚠ 번호 공백` 절은 f2 하나였고 해결했어요.
- **실제로 본 것 16 장** (`viewed: true`): 본문 Fig. 1–6 전부 · SI `S3` (+ Cu 칸 확대) `S4` `S5` `S11` `S15` `S16` `S20` `S25` `S26` `S29`. **안 본 것**: SI 19 장 (`S1` `S2` `S6`–`S10` `S12`–`S14` `S17`–`S19` `S21`–`S24` `S27` `S28` — 캡션 · 원자료로만) · `Table S1` (PDF 글자 + 원자료).
- **본 그림 중 본문과 어긋난 것**: `Fig. S11` (확산 방향 반대) · `Fig. 3a` (III 의 x ≈ 3.85 대 본문 'x < 3' · 진폭이 원자료의 ≈ 2 배) · `Fig. 3d` (범례 색 ≠ 캡션 색) · `Fig. 4` (캡션 고장 조건 · b 가로축 = 용량) · `Fig. 5a` (위 적층 시간축이 아래 영상의 ½) · `Fig. 6` (캡션 '(h and j)' 대 l 칸 14 · 17 min) · `Fig. S3a` (Cu 칸 ≈ 60 mV) · `Fig. S4` (캡션 'after operando SEM' 대 칸 EoLP) · `Fig. S5i` (8 사이클 그림 대 본문 '8 사이클 뒤 99 %' — 원자료 99.5 % 는 10 번째) · `Fig. S16` (Li₃Au · Li₁₅Au₄ 지정 대 'Li-rich 못 감') · `Fig. S29` ('ROI 3' 두 번).
- **동영상 7 개 · 프레임 134 장 + 모아보기 7 장** = `video_frames/` 141 파일 (≈ 13 MB 프레임 + 시트): 0.5 s 간격 + 끝 장면 · 폭 ≤ 1280 px · JPG (`<태그>_t<초>.jpg` · `<태그>_tEND.jpg` · `<태그>_sheet.jpg`). 모아보기 7 장으로 134 장을 전부 봤고, 원본 크기로 3 장 (MOESM4 4.5 s · sup2 끝 · MOESM9 끝) 을 봤어요. 명령은 digest §17 (`figures.json` 밖).
- **짝 확인 (전부 맞음)**: MOESM4 = Movie 1 (네 셀 나란히 · 제목 'Operando SEM analysis for Li plating / stripping on metal / LLZT / Li') · sup2 = MOESM5 = Movie 2 (Cu · WD 15.3 mm) · MOESM6 = Movie 3 (Au · WD 15.2 mm) · MOESM7 = Movie 4 (Ag · 오른쪽 위 결함) · MOESM8 = Movie 5 (Zn · WD 11.1 mm) · MOESM9 = Movie 6 ('Spontaneous lithiation of Ag NPs in SEM' · 축척 · 시각 없음 · 끝 장면 = `Fig. S25b`) · MOESM10 = Movie 7 (in-situ TEM · 장면 시계 세 구간 합 ≈ 20 min = `Fig. 6e–j`). Movie 4 박리 중반의 어두운 네모는 `Fig. S29` 빔 노출 자리와 같은 꼴 (형태 변화 아님 [추론]).
- **웹앱 점검** (`webapp.data.paper_figure_notes` · 읽기만): 36 키 전부 주석 붙음 · 엉뚱한 본문 키 (Fig. 7 이상) 0 · `paper_figures` 36. 원자료 시트 이름은 `SFig.N` 으로 적어 'Supplementary Fig. N' 이 본문 Fig. N 에 붙는 일을 막았어요.
- **`build_index.py --check`** (쓰기 없음): exit 1 — 저장소 전체의 기존 표 셀수 경고 + 이 묶음 12 편 미편입. 이 slug 는 'INDEX · comparison 미편입' 만 (예상 · 메인 세션 몫).
- ⚠ **공유 파일 한 곳 — 도구가 자동으로 썼어요**: `extract_figures.py` 가 `litdb/figures/_sources.json` 에 이 slug 항목 하나 (`figures: 35` · PDF 두 이름) 를 붙였어요 (손으로는 안 건드림). 손 크롭으로 36 장이 됐으니 합칠 때 숫자를 맞출지 보세요. 같은 파일에 병렬 편 (예: kasemchainan2019) 도 붙어요.
- 참고: 메인 세션 체크포인트 커밋 (`13464ff5` · 10/12) 이 이 digest 앞선 판과 그림 · 프레임을 이미 담았어요. 그 뒤 제가 digest 두 줄 (Fig. 4c CE 범위 · `Fig. S3a` 문장) 을 고쳤고 `figures.json` 에 `viewed` 를 달았어요.

## (g) Jeff Sakamoto 저자 여부

**저자 아님.** 본문 p.1 저자 11 명 (Dong-Su Ko · Sewon Kim · Sangjun Lee · Gabin Yoon · Daeho Kim · ChaeHo Shin · Dongmin Kim · Jaewoo Lee · Soohwan Sul · Dong-Jin Yun · Changhoon Jung) 과 SI p.1 명단을 확인했어요. 그 이름은 참고문헌 ref 11 (*Nat. Commun.*, 11, 5201 (2020)) 의 공저자로만 나와요. ⇒ INDEX 🏷 표지 안 달고, digest 에는 그 이름을 아예 안 적었어요 (batch.json `jeff_sakamoto: false` 와 같음).
