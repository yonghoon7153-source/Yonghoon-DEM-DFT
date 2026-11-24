# 끝 보고 — becker2026_electrodeposited_li_microstructure_metal_interlayers_anode_free (2026-11-24 · litdb-curator · 배치 2026-11-24b #3)

쓴 파일은 셋이에요.
- digest `litdb/papers/becker2026_electrodeposited_li_microstructure_metal_interlayers_anode_free.md` (591 줄 · 표 16 개 · 칸 수가 어긋난 줄 0 · 목록 앞뒤 빈 줄까지 Python-Markdown 으로 렌더해서 확인)
- 그림 `litdb/figures/becker2026_electrodeposited_li_microstructure_metal_interlayers_anode_free/` (크롭 29 장 + figures.json · 22 MB)
- 이 보고 파일

공유 파일 · git 은 안 건드렸어요. `litdb/figures/_sources.json` 은 추출 도구가 이 slug 항목을 자동으로 넣었어요 (손 안 댐).
⚠ 메인 체크포인트 커밋 (7a9f8c62 그림 · c62c3c65 digest 앞선 판) 에 앞선 판이 들어가 있어요. 그림은 지금 작업 트리와 같고, digest 는 그 뒤 고쳤어요 (목록 앞뒤 빈 줄 · 인용 셋을 원문과 글자까지 맞춤 · 사이클 IR 판독값 · haslam2025 교차 참조) — 최종본은 지금 작업 트리에 있는 파일이에요.

확인한 것
- 웹앱 `/paper/<slug>` 200 · 표 16 · 그림 29 장이 다 붙고 `paper_figure_notes` 가 29 개 키 전부 (f1–f6 · fS1–fS23) 에 붙어요. `_paper_pis` = `[]` (배지 없음 — 맞아요).
- 원소 태그 Li · Au · Ag · Bi · Ti · P · S · Cl (선언 정본) — 원소 쪽 링크에서 Bi · Au · Ag · Ti 1 위 · Li 2 위예요. 기법 태그는 비웠어요 (`methods: —` · EBSD · EDS · XRD · EIS · Potts 가 METHOD_MAP 에 없어요).
- 화면: 데스크톱 1440 · 폰 390 폭 캡처 + 페이지를 PDF 로 인쇄해 0 · 2 · 7 · 8 · 9 절 렌더를 직접 봤어요 (표 · 중첩 목록 정상). 처음엔 목록이 문단에 붙어 한 줄로 렌더돼서 빈 줄을 넣어 고쳤어요. 머리 HTML 주석이 글자로 보이는 건 fuchs2023 도 같은 웹앱 동작이에요. 앵커 (#9-figure-set) 로 바로 가는 캡처는 빈 화면이라 못 봤어요.
- `pytest webapp/tests/test_v3_literature.py` → 20 passed.
- `build_index.py --check` (rc 1 · 배치 대기분 때문) → 이 slug 는 두 곳에만 떠요: "어느 인덱스에도 없음 **[dem]**" · "comparison_vs_ours_DEM.md 미편입". 분류기가 slug 의 'microstructure' 로 [dem] 이라 봐요 (haslam2025 와 같아요). 아래 (a) · (b) 를 넣으면 풀려요.
- `extract_figures --audit` → 이 slug 경고 없음 (본문 6 · SI 23 · 표 0 · 중복 크롭 없음). `--inbox --only becker2026` → 본문 · SI 가 제목 66 % 로 자동 짝지어져요.
- talk 인입 대기열 (`litdb/talks/lee2026_skku_mlip_materials_design.md`) 에 이 논문은 없어요. 역링크는 필요 없어요.
- 우리 점착 W 값은 digest 에 없어요 (위치만 — 보고서 §2 · `db/properties/adhesion.json`). digest 안의 J m⁻² 숫자는 lai2020 의 문헌 γ_Li (0.47 · 0.50) 둘뿐이에요.
- 임시 파일은 전부 scratchpad `becker2026_electrodeposited_li_microstructure_metal_interlayers_anode_free/` 아래 (`becker_main.txt` · `becker_si.txt` 처럼 slug 이름을 붙였어요). PDF sha256 은 batch.json 과 같아요.
- 서지 · 발견 검색은 Crossref REST 만 썼어요 (DOI 9 건 확인 + 주제어 발견 검색 9 번 · 2025 이후 필터 · 일반 UA · 개인 정보 없음). 출판사 페이지 · 본문은 안 열었어요.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🌱 Li 금속 음극 — 공극 · 점착 · 핵생성 · 적층압 · Ag/C 인터레이어 (2026-11-24 · 18 편 한 묶음)` — '무음극 핵생성 · 성장' 의 fuchs2023 행 바로 뒤 (Ag/C 인터레이어 행 앞) 가 맞아요. 이 편은 SE 가 **LPSCl** 이라 이 절의 ⚠ LLZO 표지가 필요 없어요. 분류기가 [dem] 이라 `build_index.py` 를 다시 돌리면 INDEX_DEM.md 에도 생성돼요 (어느 쪽이든 `--check` 는 통과해요).

```
| `papers/becker2026_electrodeposited_li_microstructure_metal_interlayers_anode_free.md` **(본문 17 pp + SI 15 pp · 크롭 29장 (도구 29 중 손 크롭 1 = `Fig. S20` (도구가 S21 영역을 두 번 자름) · 다시 자름 1 = `Fig. S1` (SI 표지 글)) 전부 봄 — 21장 원본 + 확대 3 · 전체 단면 8장은 축소 시트 · 2026-11-24)** | **[외부·exp·⭐⭐ LPSCl 무음극 셀의 석출 Li 결정립 · 방위 (cryo-BIB 단면 EBSD) — Au · Ag · Bi 160 nm 층 · 박리 · 사이클 · ✅ SE = Li₆PS₅Cl (우리 comp1 조성) · 원자단위 계산 0 (3D Potts 만)]** ✅ **Juri Becker**/**Luca Schuster** (공동1)/Sascha Kremer/**Till Fuchs\***/**Jürgen Janek\*** (JLU Giessen 물리화학 · 실험물리 I · ZfM), "**Microstructure of electrodeposited lithium and its evolution during cycling when using metal interlayers in "anode-free" solid-state batteries**" — ***Energy Environ. Sci.* 19, 2367–2383 (2026)**, DOI `10.1039/D5EE07230A` (OA CC BY 4.0). Ti\|(층)\|LPSCl\|Li · 380 MPa 압착 · 15 MPa · 25 °C · 7.5 mAh cm⁻² @ 150 µA cm⁻²: 결정립 평균 폭 **Ti 136 · Au 30 · Ag 30 · Bi 170 µm** (Bi 는 11 개 중 811 µm 하나 — 빼면 ≈106 · 중앙값 Ti ≈88 · Bi ≈79 figure-read) · 우선 방위 (IPF ∥ 계면 법선) **Au <101> = Li(110) ∥ 계면 · Ag <111>** · Ti · Bi 뚜렷하지 않음 (세기 패널마다 정규화 · MUD 없음) · 끝 상 Au → Li₁₅Au₄ 입자 (Zener 류) · Ag → Li 에 다 녹음 (≈1 at% · 7.5 mAh 층 평균 ≈0.55 at% 카드 산술 · melt XRD −0.21 %) · Bi → Li₃Bi 층이 LPSCl 쪽 · Li 는 Ti 쪽 · 합금 평탄 Au 260 · 120 · Bi 800 · 760 mV (150 µA) · 적정 OCV 첫 평탄 Bi ≈0.84 ≫ Au ≈0.33 > Ag ≈0.25 V (figure-read) · 박리 (10 − 5 mAh cm⁻² · 100 µA): **Ti 위 Li 거의 전부 <101> = (110) 정렬** · 순수 Li 결정립 ↓ (Ti → ≈88 · Bi → ≈53 µm) · 합금 Li ↑ (Au ≈47 · Ag ≈59) · Ag 10 사이클: 박리 90–95 % ↓ · 핵 과전압 ↑ · 작은 결정립 · ⚠ 조건당 셀 하나 · 박리 비교가 전류 · 도금량을 같이 바꿈 · 면적 기준 (층 8 mm vs 10 mm) 미기재 · `Fig. S15` 높이 경향이 Note S4 와 반대 · `Fig. 2b` 입자 위치가 본문 ('Ti\|Li 근처') 과 다름 | **W_ad 보고서 §7 Li 면 선택 ((110) 1 순위 · Ag 계 (111) 대조) · §7 ③ 합금 구동력 (실측 평탄) · §8-3 Li 가 쌓이는 자리 (Au · Ag 박막: SE 쪽 · Bi: CC 쪽)** (exp, 외부 · LPSCl) |
```

## (b) 비교 문서에 넣을 줄

분류기가 **[dem]** 이라 `--check` 가 요구하는 곳은 `comparison_vs_ours_DEM.md` 예요 → §I 카드 하나가 본 줄이에요. 내용이 우리 환원 가장자리와도 닿아서 `comparison_vs_ours.md` §E 한 줄 + Reference key 한 줄도 같이 드려요 (fuchs2023 와 같은 꼴). 물성 4축 (A–D) 에는 **넣을 것이 없어요** (LPSCl 의 σ · 탄성 · 띠틈이 이 논문에 없어요).

**`comparison_vs_ours_DEM.md` §I 카드** (번호는 메인이 매겨요 — 지금 I-22 까지):
```
### I-xx. `becker2026_electrodeposited_li_microstructure_metal_interlayers_anode_free` — ★★ (exp · ⛔ 점착 정량 없음 · ✅ LPSCl 계) **석출 Li 의 결정립 · 방위가 층 (Au · Ag · Bi) 과 박리 이력으로 바뀐다 — W_ad 7 절 Li 면 (110) 1 순위의 실험 근거 · Li 가 쌓이는 자리는 층 종류가 정한다**

> **무엇을 주나.** Ti | (Au · Ag · Bi 160 nm) | Li₆PS₅Cl | Li · 380 MPa 압착 · 15 MPa · 25 °C · 7.5 mAh cm⁻² @ 150 µA cm⁻² (cryo-BIB mm 단면 EBSD): 결정립 평균 폭 Ti 136 · Au 30 · Ag 30 · Bi 170 µm (Bi 는 811 µm 결정립 하나 — 빼면 ≈106) · IPF ∥ 계면 법선 Au <101> = Li(110) ∥ 계면 · Ag <111> · 박리 (10 − 5 mAh cm⁻² · 100 µA cm⁻²) 뒤 Ti 위 Li 는 거의 전부 <101> · 끝 상 Au → Li₁₅Au₄ 입자 · Ag → Li 에 녹음 (≈1 at%) · Bi → Li₃Bi 층이 LPSCl 쪽 · Li 는 Ti 쪽.
>
> **★ 우리 축에 닿는 곳.**
> ① **Li 면** — 실험에 실제로 나오는 면은 (110) (Au 도금 · Ti 박리 뒤) · (111) (Ag 도금) · (100) 은 우세하게 나온 적 없음 → W_ad 7 절: (110) 1 순위 · Ag 계 (111) 대조 · (100) 문헌 대조. 증착 Ag 는 (111) 조직 (`Fig. S14`) → 보고서 2-3 Ag(111) 선택의 실험 근거.
> ② **합금 구동력 ≠ 결과** — 적정 OCV 첫 평탄 Bi ≈0.84 ≫ Au ≈0.33 > Ag ≈0.25 V (figure-read) 인데 덮임 · 결정립 미세화는 Au ≈ Ag ≫ Bi → 7 절 ③ 에 'Li 속 M 용해 에너지' · 'Li 쪽 끝 화합물 (Li₁₅Au₄ · Li₃Bi)' 을 같이.
> ③ **Li 가 쌓이는 자리** — Au · Ag 박막: SE 쪽 (합금|LPSCl 사이) · Bi: CC 쪽 (Li₃Bi 를 지나) → I-21 (metzler2026 · Cu|C 사이) 과 다른 꼴 · W 계면 후보를 층 구조별로.
> ④ **Li 층 = 결정립 몇 개** (폭 30–170 µm ≥ 두께 44–64 µm) → I-16 (masias2019) 의 등방 다결정 Li 물성으로 넣을 때의 한계 문장.
>
> **⛔ 인용 금지 / 한정어**
> · 결정립 크기 · 방위 분율 · 평탄 전위를 계산 입력값으로 옮기지 않는다 (조건당 셀 하나 · IPF 세기 정규화 · MUD 없음).
> · 'Bi 가 결정립을 키운다' 로 인용하지 않는다 (결정립 하나에 기댄 평균 · 중앙값은 Ti 와 비슷).
> · 실험 방위를 'W 가 가장 큰 면' 의 근거로 쓰지 않는다 · registry (면내 방향) 는 실험에서 못 얻는다.
> · 박리 비교는 전류 (100 대 150 µA cm⁻²) · 도금량 (10 대 7.5) 이 같이 바뀌었다 · 공극 정량 없음 · 순수 금속 박막이라 Ag–C 복합층에 그대로 옮기지 않는다.
> 상세: digest §3d · §3e · §7c–§7g · §10 · §11.
```

**`comparison_vs_ours.md` §E 행** (선택):
```
| **🆕 (2026-11-24) LPSCl 무음극 셀의 금속 층 (Au · Ag · Bi 160 nm) 은 상도의 Li 쪽 끝대로 남는다 — Au → Li₁₅Au₄ 입자 · Ag → Li 에 녹음 (≈1 at%) · Bi → Li₃Bi 층이 LPSCl 쪽에 남아 Li 가 Ti 쪽에 쌓인다 · 합금 평탄 (적정 OCV) Bi ≈0.84 · Au ≈0.33 · Ag ≈0.25 V 부터 수 mV 까지 (figure-read)** | **[Becker26Micro]** `Fig. 2b–d` · `Fig. S3` · `Fig. S4` · p.2370–2374 (Li₆PS₅Cl · 15 MPa · 25 °C · 조건당 셀 하나) | 환원 가장자리 **1.717 V** (Li 교환 0 · comp1 = modelc · grand-potential) — 세 층의 합금 평탄이 전부 그 아래라 층\|LPSCl 계면은 리튬화 동안 이미 열역학적 환원 구간이다 · Li–Au · Li–Ag · Li–Bi hull 전압 · Li 속 Ag 용해 에너지 계산 없음 (W_ad 보고서 7 절 ③ 제안 단계) | ⚪ 축 다름 (합금 순서 · 남는 상의 실험 근거 · 수치 비교 아님) · ⛔ 결정립 · 방위 · 평탄 숫자를 계산 입력으로 옮기지 않는다 |
```

Reference key 행:
```
| **[Becker26Micro]** ⭐⭐ **LPSCl 무음극 석출 Li 의 결정립 · 방위 (EBSD) — Au · Ag · Bi 160 nm 층 · 박리 · 사이클** · ⛔ **exp 전용 · A–D 물성 4축 진입 금지** (§E 1 행만) | Juri Becker/Luca Schuster/Sascha Kremer/Till Fuchs\*/Jürgen Janek\* (JLU Giessen) *Energy Environ. Sci.* 19, 2367 (2026) | `papers/becker2026_electrodeposited_li_microstructure_metal_interlayers_anode_free.md` ✅ | exp |
```

## (c) `pdf_map.tsv`

**필요 없어요.** `--inbox --only becker2026` 가 본문 · SI 를 제목 66 % 로 자동 짝지었어요. (동영상 없음.)

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저)

'목록' = `litdb/_curation/batch_2026_11_24/extra_papers_2026_11_24.md`. litdb 칸은 `litdb/papers/` 의 자체 digest 유무예요 (남의 digest 에 인용만 된 건 '없음'). 서지는 전부 이 논문 참고문헌 + Crossref 로 맞췄어요.

| # | 논문 | 왜 우리에게 | litdb · 목록 | 서지 확인 |
|---|---|---|---|---|
| 1 | Kotakadi, Aspinall, Burton, Liang, Aihara, Pasta · *Joule* 9, 102175 (2025) — "Impact of metallic interlayers at the lithium-Li6PS5Cl solid electrolyte interface" · DOI 10.1016/j.joule.2025.102175 | **Li 금속 \| LPSCl 사이 금속 층** — 이 논문이 Li–Bi · Li–Ag 상도와 "Li 와 LPSCl 을 떼면 SEI 가 바뀐다" 의 근거로 인용 (ref 56). 우리 계 그대로라 §E · W_ad 8-3 에 바로 걸려요 | 없음 (baer2026 digest 에 인용만) · 목록에 없음 | Crossref 확인 (9(11) · 논문 번호) |
| 2 | Chen H., Zhao Y., Zhang X. … Luo J. · *Nat. Synth.* 4, 552 (2025) — "Synthesis of monocrystalline lithium for high-critical-current-density solid-state batteries" · DOI 10.1038/s44160-024-00712-4 | **단결정 Li 방위별 CCD** — 이 논문이 '박리 뒤 <101> = Chen 의 최고 CCD 방위 (확산 장벽 · 영률 최저)' 로 인용 (ref 37). Li 슬랩 면 선택의 둘째 실험 근거이고, 방위별 장벽 · 영률 주장을 원문으로 확인해야 해요 | 없음 · 목록에 없음 | Crossref 확인 (4(5), 552–561) |
| 3 | Becker J., Fuchs T., Ortmann T., Kremer S., Richter F. H., Janek J. · *Adv. Energy Mater.* 15, 2404975 (2025) — "Microstructure of Lithium Metal Electrodeposited at the Steel\|Li6PS5Cl Interface in 'Anode-Free' Solid-State Batteries" · DOI 10.1002/aenm.202404975 | 이 논문의 **직전 편 · LPSCl 계** — '두께 효과' · 2D Potts · Li\|LPSCl 계면이 잘린 결정립을 만든다는 원전 (ref 34) | 없음 · 목록에 없음 | Crossref 확인 (15(16) · 온라인 2024-12-15) |
| 4 | Becker J., Weintraut T., Benz S. L. … Richter F. H., Janek J. · *Nat. Commun.* 16, 5395 (2025) — "Purity of lithium metal electrode and its impact on lithium stripping in solid-state batteries" · DOI 10.1038/s41467-025-61006-7 | 이 논문의 핵심 구분인 **'순수 Li 대 섞인 Li' 의 박리** 를 정면으로 다뤘어요 (ref 12) — W_ad 8-4 박리 공극 | 없음 · 목록에 없음 | Crossref 확인 |
| 5 | Wang A., Huang S., Xie Z. … Chen L. · *Acta Mater.* 287, 120780 (2025) — "In3Li13(311)/Li(110) coherent heterogeneous induced uniform epitaxial electrodeposition enabling the stable ultrathin lithium metal anode" · DOI 10.1016/j.actamat.2025.120780 | **발견 검색** — Li 합금 \| Li(110) 정합 에피택시로 석출을 고르게 → Li\|합금 계면 W (digest §7e) 와 (110) 면을 잇는 사례 · ⚠ 전해질 (액체일 수 있음) 은 제목만 봐서 미확인 | 없음 · 목록에 없음 | Crossref 확인 (제목 · 저자 · 권 · 번호) · 본문 안 엶 |
| 6 | Fuchs T., Ortmann T., Becker J., Haslam C. G. … Nazar L. F., Sakamoto J., Janek J. · *Nat. Mater.* 23, 1678 (2024) — "Imaging the microstructure of lithium and sodium metal in anode-free solid-state batteries using electron backscatter diffraction" · DOI 10.1038/s41563-024-02006-8 · 🏷 | 이 그룹 EBSD 방법의 원전 (ref 33) · steel · Cu 위 Li · Na 결정립 | 없음 · **목록에 있음** (표 2 #8) | 목록에서 Crossref 확인 (저자 메타 'Sakamoto, Jeff') |
| 7 | Motoyama M., Shimizu K., Kimura T., Yamamoto T., Watanabe S., Iriyama Y. · *JACS Au* 4, 4700 (2024) — "Uncovering the Dynamics of Li–Au Alloying and Li Nucleation at the Au/LiPON Interface with In Situ Z Contrast and Surface Roughness Contrast Imaging via Scanning Electron Microscopy" · DOI 10.1021/jacsau.4c00530 | **Li–Au 합금 순서 · Li 핵 자리를 in situ 로** (ref 26) — 이 논문이 사후 단면으로 추론한 '합금\|SE 사이 핵' 의 실측 짝 · ⚠ LiPON 계 | 없음 · 목록에 없음 | Crossref 확인 (4(12), 4700–4714) |
| 8 | Yoon J. S., Sulaimon H., Siegel D. J. · *J. Mater. Chem. A* 11, 23288 (2023) — "Exploiting grain boundary diffusion to minimize dendrite formation in lithium metal-solid state batteries" · DOI 10.1039/D3TA03814A | **'결정립 < 1 µm 이면 > 1 mA cm⁻²'** 의 계산 원전 (ref 35) — 이 논문 결론의 정량 근거이고, 우리 MLIP 로 Li 입계 확산을 잴 때의 비교 기준 (2023 이지만 넣었어요) | 없음 (sandoval2025 · makino2026 · wu2026 digest 에 인용만) · 목록에 없음 | Crossref 확인 (11(43), 23288–23299) |

그다음 후보: Zhang S. … Chen L. *ACS Energy Lett.* 6, 4118 (2021) "Phase Diagram Determined Lithium Plating/Stripping Behaviors on Lithiophilic Substrates" · DOI 10.1021/acsenergylett.1c02127 (상도 꼴 (고용 대 금속간) 이 도금 · 박리를 가른다 — 7 절 ③) · Alt C. D. … Janek J. *Joule* 8, 2755 (2024) "Quantifying multiphase SEI growth in sulfide solid electrolytes" · DOI 10.1016/j.joule.2024.07.006 (황화물 SEI 성장 · §E). 둘 다 Crossref 확인 · litdb 없음 · 목록에 없음. Haslam 2025 *ACS Energy Lett.* 은 목록 표 1 #4 이고 이번 묶음 #4 로 이미 들어왔어요.
참고: inbox 에 짝 없는 PDF 로 Ko 2025 *Nat. Commun.* (목록 표 1 #8) · Xie 2024 (목록 표 2 #3) 등이 이미 있어요 — 다음 묶음 몫으로 보여요.

## (e) DEM-DFT 보고서에 쓸 거리 — W_ad 보고서 7 절 · 8 절

✅ SE 는 **Li₆PS₅Cl** (산화물 아님 · 우리 comp1 조성) · 15 MPa · 25 °C · 조건당 셀 하나예요. 값은 차수 · 경향으로만 쓰고 계산 입력으로 넣지 않아요. "봤다" = 이번에 그 그림을 직접 보고 읽었다 · "축소" = 전체 단면을 축소 시트로만 봤다. 상세 표는 digest §7d–§7g · §11.

**질문 1 — 층마다 석출 Li 의 방위 · 결정립 · 사이클 뒤 변화 → Li 슬랩 면 (7 절)**
1. 도금 (7.5 mAh cm⁻²) 우선 방위 (IPF ∥ 계면 법선 y): **Au <101> → Li(110) 이 계면과 나란** · **Ag <111> → Li(111)** · Bi 는 (110)–(111) 사이지만 큰 결정립 몇 개의 방위 · Ti 는 뚜렷하지 않음 — p.2371–2372 · `Fig. 1d` · `Fig. S6` (봤다). y 가 법선이라는 근거: `Fig. 1c` 축 + p.2380 *"parallel to the stripping direction"*.
2. 박리 (10 − 5 mAh cm⁻²) 뒤: **Ti 위 Li 거의 전부 <101> = (110)** (가장 셈) · Au 는 <101> 근처 · Ag · Bi 는 조직 없음 — p.2376–2377 · `Fig. 4d` (봤다) · `Fig. S17` (봤다) · `Fig. S16` · `Fig. S21` · `Fig. S23` (축소).
3. 결정립 폭 (평균 · 본문): Ti 136 · Au 30 · Ag 30 · Bi 170 µm (Bi 는 811 µm 하나 — 빼면 ≈106) · 박리 뒤 figure-read Ti ≈88 · Bi ≈53 (순수 Li ↓) · Au ≈47 · Ag ≈59 (합금 Li ↑) — p.2373 · p.2376–2377 · `Fig. 2a` · `Fig. S18` · `Fig. S19` · `Fig. S22` (봤다). 사이클 (Ag 10 번) 뒤엔 기둥 셋 + 작은 결정립 다수 — `Fig. 5c` (봤다).
4. **권고 (digest §7d)**: **Li(110) 1 순위** (실험에 가장 자주 나오고 chaney2024 · baer2026 · wang2022 의 황화물 계면 선례가 같은 면) · **Ag 계 (LPSCl\|Ag · Ag–C) 에 Li(111) 대조 면 하나** (bcc (111) — lu2026 의 Ag(111) 위 정합 fcc(111) 과 다른 것) · **Li(100) 은 문헌 대조용** (seymour2021 · yang2021 · Cheng 2017). γ_Li 는 각 면 그대로 같은 방법으로.
5. 단서 다섯 (보고서에 같이): ① IPF 는 층 전체 분포 (계면 결정립만이 아님) ② 세기 패널마다 정규화 · MUD 없음 · 결정립 11–70 개 ③ 방위는 성장 · 박리 · 압력의 결과라 'W 가 큰 면' 의 근거가 아님 ④ **registry (면내 방향) 는 실험에서 못 얻음** (Ti 결정립 ≈17 µm ≪ Li 결정립 · `Fig. S5` 봤다) ⑤ Au · Ag 층에선 Li 의 CC 쪽 상대가 Au(111) · Ag(111) 이 아니라 Li 합금.
6. 덤 — **증착 Ag 160 nm 는 <111> ∥ 법선 = (111) 조직** (Au 도 같고 Bi 는 <001>) — SI p.14–15 Note S3 · `Fig. S14` (봤다). 보고서 2-3 의 LPSCl\|Ag(111) 면 선택 (첫 충전 전) 을 받쳐 주는 첫 실험 근거예요.

**질문 2 — 합금 순서 · 남는 상 · 위치 → 7 절 3 번 · 8-3**
7. 합금 순서 (전위 평탄): Au 260 → 120 mV (150 µA cm⁻²) + 저속 · 적정에서 ≈20–30 mV (Li₃Au\|Li₁₅Au₄) · Ag 150 µA 에선 평탄 없음 → 100 µA ≈68 · ≈45 · ≈5 mV · 적정 ≈250→207 · ≈97→65 · ≈32→17 · ≈5→0 mV · Bi 800 → 760 mV (Bi\|LiBi → LiBi\|Li₃Bi) — p.2370–2371 · `Fig. 1b` · `Fig. 4b` · `Fig. S3` · `Fig. S4` (봤다 · 평탄 값 외엔 figure-read).
8. 남는 상 · 위치: Au → **Li₁₅Au₄ 입자** (EBSD Kikuchi · 본문 'Ti\|Li 계면 근처' — ⚠ 그림의 입자는 LPSCl 계면에서 ≈10 µm 위) · Ag → **Li 에 다 녹음** (≈1 at% · ≈4.2 mAh cm⁻² 넘으면 · EDS 고름 · 7.5 mAh 층 평균 ≈0.55 at% 우리 산수) · Bi → **Li₃Bi 층이 LPSCl 쪽**에 남고 Li 는 그 뒤 (Ti 쪽) — p.2373–2374 · `Fig. 2b–d` (봤다 · `Fig. 2b` 는 확대까지).
9. **7 절 ③ 에 붙일 점**: 실측 첫 평탄 (적정 OCV) Bi ≈0.84 ≫ Au ≈0.33 > Ag ≈0.25 V = Li 하나당 ≈ −0.84 · −0.33 · −0.25 eV → DFT hull 전압의 **대조** 표적 (MP 조회 몇 분). 그런데 결과 (덮임 · 결정립 미세화) 순서는 Au ≈ Ag ≫ Bi 로 **반대** → 합금 생성 에너지 하나로 줄 세우지 말고 **Li 속 M 희석 용해 에너지** (Ag) · **Li 쪽 끝 화합물의 Li 대비 안정성** (Li₁₅Au₄ · Li₃Bi) · **그 화합물\|Li 계면** 을 같이 내자는 근거예요.
10. **8-3 에 붙일 점**: Li 첫 핵 자리 (저자 · p.2378) — Au · Ag 박막은 **합금\|LPSCl 사이 (SE 쪽)** · Bi 는 **Li₃Bi 와 Ti 사이 (CC 쪽)** · Ti 는 Ti\|LPSCl. 8-3 의 Ag/C 층 (Li 가 Cu\|C 사이 · metzler2026) 과 비교하면 **탄소 유무가 Li 자리를 바꾼다** (순수 Ag 막 = SE 쪽). W 계면 후보: Li\|Li₁₅Au₄ · Li(Ag)\|LPSCl · Li\|Li₃Bi · Li₃Bi\|LPSCl · Li\|Ti (제안 · 이 논문은 계면 에너지를 안 쟀어요). ⚠ 자리는 사후 단면에서 거꾸로 추론한 것이에요 (핵 순간 관찰 아님).
11. 우리 환원 가장자리 1.717 V 와 비교: 세 층의 합금 평탄이 전부 그 아래 → 층\|LPSCl 계면은 리튬화 동안 이미 열역학적 환원 구간 (우리 비교 · 이 논문은 SEI 를 분석 안 함) — `Fig. S3` · `Fig. S4` (봤다).

**질문 3 — 박리 · 공극 · 접촉과 결정립**
12. **공극 정량은 없어요.** 있는 것: 덮임 (Ti · Bi 맨 영역 · Au · Ag ≈100 % · 사진만 · `Fig. S12` 봤다) · 박리 뒤 축소 단면에 큰 공극 안 보임 (15 MPa · 절반 박리 · `Fig. S16` 등 축소) · Ag 10 사이클 박리 90–95 % → 감소 · 9 번째는 ≈3.5 mAh cm⁻² 부터 분극 상승 · LPSCl 조각이 Li 안 · IR 증가를 저자는 SEI + 접촉 상실로 해석 (p.2377 · `Fig. 5` 봤다).
13. 결정립 ↔ 공극은 **가설뿐**: 작은 결정립 → 입계 확산 ↑ → 공극 ↓ (ref 35 인용) · 박리 뒤 (110) = Chen 의 최고 CCD 방위 (ref 37 인용) · 순수 Li 결정립 재형성은 적층압이 몰았을 수 있고 합금 Li 는 합금 경화로 못 바뀐다 (p.2377). ⇒ 8-4 의 공극 근거로는 안 쓰고, '박리 이력이 Li 결정립 · 방위를 바꾼다 → 박리 뒤 계면의 Li 면은 도금 직후와 다를 수 있다' 한 줄만 써요.
14. 연속체 · DEM: Li 결정립 폭 (30–170 µm) ≥ 층 두께 (44–64 µm) → Li 층은 '결정립 몇 개의 모자이크' → 등방 다결정 Li 물성 (masias2019) 을 쓸 때의 한계 문장 근거 — p.2373 · `Fig. 2a` (봤다).

**질문 4 — 실험 조건과 옮기는 범위**
15. SE = **Li₆PS₅Cl** (상용 POSCO · 입경 5 µm · 90 mg · 지름 10 mm) · 펠렛 **380 MPa · 3 min** · 운전 **15 MPa** · **25 °C** · 전류 150 µA cm⁻² (7.5 · 4.5 mAh cm⁻²) · 100 µA cm⁻² (10 mAh cm⁻² 도금 + 5 박리) · 3 µA cm⁻² (합금) · 층 **160 nm** PVD (0.2–0.3 nm s⁻¹ · 지름 8 mm) · CC Ti 15 µm · CE Li ≈100 µm — p.2368–2369 · `Fig. 1` 캡션 · `Fig. S12` 캡션.
16. 산화물이 아니라 LLZO 한정어는 필요 없어요. 그래도 옮기는 것은 기전 셋 (분산 · 용해 · 상분리) · 방위의 종류 · '이력이 미세구조를 바꾼다' · '층 종류가 Li 자리를 바꾼다' 까지예요. 결정립 크기 · 방위 분율 · 평탄 숫자는 계산 입력으로 안 옮기고, 순수 금속 박막 결과를 Ag–C 복합층 값으로도 안 옮겨요. 우리 modelc (Li₅.₄PS₄.₄Cl₁.₆) 와는 Cl 양이 달라요.

## (f) 그림 크롭 요약

- `extract_figures.py --slug … --pdf <본문> <SI> --clean` → **29 장** (본문 Fig. 1–6 · SI Fig. S1–S23 · 표 0). 출력의 '번호 공백 · 놓친 캡션 후보' 는 없었어요 (`missing_labels` []).
- **고친 것 둘**
  - `fig_S20` — 도구가 **S21 과 같은 bbox** 로 잘랐어요 (두 파일 md5 가 같았어요). 이 SI 는 캡션이 그림 **아래**라 S20 캡션 (SI p.12 맨 위) 의 그림은 SI p.11 아래쪽 래스터예요 → 손으로 잘라 `manual_crop` 사유를 달았어요. 고친 뒤 `--audit` 중복 경고 없음.
  - `fig_S1` — SI 표지 글 (소속 · *Equal contribution* · *Supporting Information*) 이 같이 잘려서 래스터 경계 + 6 pt 로 다시 잘랐어요 (`recrop`).
- **29 장 전부 봤어요.** 원본 크기 21 장 (`Fig. 1`–`Fig. 6` · `Fig. S1`–`Fig. S6` · `Fig. S9` · `Fig. S12`–`Fig. S15` · `Fig. S17`–`Fig. S19` · `Fig. S22`) + 확대 렌더 3 곳 (`Fig. 1b` · `Fig. 2b` 위 SEM · `Fig. 4b`). 전체 단면 8 장 (`Fig. S7` · `S8` · `S10` · `S11` · `S16` · `S20` · `S21` · `S23`) 은 **축소 접촉 시트로만** 봤어요 — 결정립 색 · 대략의 길이만 읽었고 결정립 하나하나는 못 읽었어요.
- **본문과 어긋난 곳** (digest §10-④ · ⑤ · ③):
  - `Fig. S15` — 결정립 **높이가 거칠수록 높다** (figure-read ≈23 → ≈25 → ≈30 MCU) · SI Note S4 는 *"3.7 에서 더 낮다"* — 반대예요.
  - `Fig. 2b` — 본문은 Li₁₅Au₄ 가 *"predominantly near the Ti\|Li interface"* 인데, 그림의 분석 입자는 LPSCl 계면에서 ≈10 µm 위이고 Ti 계면은 화면 밖이에요.
  - p.2379 — Ag 를 *"significantly lower aspect ratio, i.e., … taller than they are wide"* 라 썼는데, 이 논문 종횡비 (높이 ÷ 폭 · `Fig. S9`) 로는 Ag 가 Ti 보다 커요 (문장 안에서 정의가 뒤집혔어요).
  - `Fig. S9` — Ag 평균 figure-read ≈1.4 · 본문 ≈1.3 (작은 차).
  - `Fig. 1b` · `Fig. 4b` · `Fig. S3` — Bi 리튬화가 3 µA cm⁻² 에서도 공칭 Li₃Bi 의 ≈70 % 조성에서 끝나고, 셀마다 끝 전하가 다르다 (우리 산수 · 논의 없음).
  - 캡션 · 라벨 오기 — `Fig. S16` · `Fig. S18` 의 'Figure 3' (→ Fig. 4) · `Fig. S22` 캡션 번호 'Figure 22' · `Fig. S13` 마지막 반사 '(200)' (→ (220)) · `Fig. S2` 축 't^1/2 / h' · `Fig. 3b` 입자 분율 단위 'MCU' · 방법은 입방 Li 만 지표화했다는데 `Fig. 2b` 는 Li₁₅Au₄ 를 판정.
- 덧: 본문 PDF 글자층에서 µ 가 'm' 으로 깨져요 (AdvPi1 글꼴) · 음수 부호는 '\x02' 로 나와요. *"around 10 mV"* (p.2370) 는 원문에 부호가 없어서 digest 에도 부호 없이 인용하고 그림 값 (≈ −13 → −8 mV) 을 따로 적었어요.
- 동영상은 없어요.

## (g) Jeff Sakamoto 저자 여부

**아니에요.** 저자는 Juri Becker · Luca Schuster (공동 1저자) · Sascha Kremer · Till Fuchs\* · Jürgen Janek\* (교신) 다섯 명이고 전원 JLU Giessen 이에요.
- Sakamoto 는 참고문헌 [8, 9, 11, 15, 18, 20, 31, 33] 의 공저자로만 나와요 (표기 'J. Sakamoto').
- digest 저자 줄에 없고 웹앱 `_paper_pis` = `[]` 를 확인했어요 · (a) 행에 🏷 를 안 달았어요.
- 이 중 [31] Haslam 2025 (이번 묶음 #4) · [33] Fuchs 2024 (목록 표 2 #8) 는 목록에서 Crossref 저자 메타 'Sakamoto, Jeff' 로 확인된 편이에요.
