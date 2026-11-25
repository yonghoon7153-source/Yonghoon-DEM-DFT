# 끝 보고 — metzler2026_sputtered_ag_carbon_interlayers_anode_free (2026-11-24 · litdb-curator)

쓴 파일: `litdb/papers/metzler2026_sputtered_ag_carbon_interlayers_anode_free.md` (428 줄 · 표 15 개 · `md_html` 렌더 칸 수 검사 이상 0) · `litdb/figures/metzler2026_sputtered_ag_carbon_interlayers_anode_free/` (크롭 18 + `figures.json`) · 이 보고 파일.  공유 파일 · git 쓰기 명령은 안 썼다 (`litdb/figures/_sources.json` 은 추출 도구가 다시 씀).  메인 체크포인트가 이미 digest 를 HEAD 에 담았다 (`git diff HEAD` 0 — 마지막 수정까지 포함).
웹앱 확인 (읽기만): track **dft** · PI 배지 `[]` · 원소 태그 Li · Ag · C · Cu · P · S · Cl (Ag 원소 페이지에 뜸) · methods 태그 비어 있음 (`> methods: Raman` — `METHOD_MAP` 에 Raman 이 없어 용어 페이지 링크는 안 생긴다) · 그림 주석 18 키 (f1–f5 · fS1–fS12 · tS1) 전부 · 웹앱 시험 `test_v3_literature` · `test_v3_markdown` · `test_v3_surfaces` 51 통과.
서지 (PDF 첫 쪽 · 머리글 확인): *ACS Appl. Energy Mater.* **9**, 9817–9827 (2026) · DOI `10.1021/acsaem.6c01118` · 받음 2026-03-31 · 고침 06-27 · 승인 07-02 · 출판 07-21 · CC-BY 4.0 · 저자 Michael Metzler · Christopher Doerrer · Guillaume Matthews · Yige Sun · Enzo Liotti · Patrick S. Grant\* (Oxford Materials · Faraday Institution · Doerrer 는 Toronto 겸).

## 한눈에 (메인이 사용자에게 옮길 요지)
- **무엇**: MTI 상용 탄소 코팅 Cu (Cu 9 µm + "fine particulate C" ∼1 µm) 위에 Ag ≈100 nm (BSE 89.32 nm) 스퍼터 → **Li₆PS₅Cl (황화물)** 펠릿 무음극 셀 (SE 250 MPa → 전체 500 MPa 조립 · 운전 4 MPa · 60 °C · 단결정 NMC83).
- **숫자**: 핵생성 과전압 **16.1 → 3.9 mV** (2 mA cm⁻² · n 5 · std err) · 첫 방전 **163 → 203 mAh g⁻¹** · ICE **71 → 86 %** (1 mA cm⁻² · n 3) · 10 사이클 유지율 59.3 % (C-only 38.5 · Ag-only 47.3 · Ag 500 nm 37) — 이 '유지율' 은 **C10/C1 충전 용량** (`Fig. S9` 로 역산 · 본문 정의 없음).
- **Li · Ag 위치**: Li 는 **Cu | C 사이**에 쌓여 C 를 SE 쪽으로 밀어낸다 · Ag (처음엔 C 윗면 = SE 쪽) 는 충전 뒤 Li 속에 희박하게 흩어졌다가 방전 뒤 **C 위 덩어리** · Cu–C 사이 큰 공극 + Li 잔여 실.
- **우리에게 날카로운 점 셋**: ① 운전 중 처음 벌어지는 계면은 **C\|Cu** — 우리 W 쌍 목록 (C–C · Ag–C · LPSCl\|Ag(111) · LPSCl\|흑연) 에 없다 ② **LPSCl\|Ag 는 첫 충전 전까지만** 맞는 쌍 (그 뒤 SE 쪽 면 = LPSCl\|C) ③ 탄소는 '흑연질' 이라 불렀지만 Raman I_D/I_G figure-read ≈1.3–1.4 → W_ad 보고서 §7-1 의 **'결함 많은 탄소' 행** · 합금의 끝 상태는 **희박 Li(Ag) ≈0.5 at%** [카드 산술].
- **그림 판독이 본문과 어긋난 곳** (digest §10): C 층 단면 2–3 µm (본문 ∼1 µm · 압축 뒤 0.5–0.75 µm) · 2D 기공률 26.7 → 18.5 % 가 두께 2–3 배 감소와 질량 보존이 안 맞음 · Li 두께가 같은 셀 안에서 figure-read 4–28 µm · `Fig. 2d` 는 세 셀 중 가장 좋은 셀 · σ 1.6 mS cm⁻¹ = R1+R2 (계면형 R2 포함) 로 푼 값 · Cu 쪽 S 신호 (`Fig. S11d` · `Fig. 4e,h` · `Fig. S12e` — 본문 언급 없음) · `Fig. S8` SOC 표기 뒤바뀜.
- **전작 (2025) 과 합치면**: 전작은 Ag 위치만 바꿨을 때 핵생성 전위 차이가 *"no resolvable"* (원문 PDF 확인) 이고 ICE 72 → 83 % 가 갈렸다 · 이번 편은 Ag 유무로 핵생성 과전압이 갈렸다 ⇒ 'Ag 유무 → 핵생성 꼭지 · Ag 위치/층 구조 → ICE · 석출 위치' 가설 [카드 해석 · 탄소 · 셀이 달라 결론 아님].

## (a) `litdb/INDEX.md` 에 넣을 행
넣을 절 = **`## 🧲 계면 점착 · 인터레이어 트랙 — LPSCl 이 한쪽 면인 계면/벌크 역학의 실측 앵커 (2026-09-23 신설)`** — `spencerjolly2023_ag_graphite_interlayer_operando_xrd` 행 아래 (metzler2025 행을 먼저 넣으면 그 바로 아래).

```
| `papers/metzler2026_sputtered_ag_carbon_interlayers_anode_free.md` **(본문 11 pp + SI 18 pp(그림 S1–S12 · 표 S1) · 크롭 18장 · 그림 17장 전부 실독)** | **[외부·exp·⭐⭐⭐ Ag–C 인터레이어 · Ag 위치를 스퍼터로 고정 · 점착 트랙 "Li 가 어디 쌓이고 무엇이 밀려나나"]** ✅ **Michael Metzler**/C. Doerrer/G. Matthews/Y. Sun/E. Liotti/**Patrick S. Grant\*** (Oxford · Faraday Institution), "**Lithium Plating and Stripping Facilitated by Thin Sputtered Silver and Carbon Interlayers in Anode-Free All-Solid-State Batteries**" — ***ACS Appl. Energy Mater.* 9, 9817–9827 (2026)**, DOI `10.1021/acsaem.6c01118` (CC-BY 4.0). MTI 상용 탄소 코팅 Cu (Cu 9 µm + "fine particulate C" ∼1 µm · Raman D 1359 / G 1588 / 2D 2689 · I_D/I_G figure-read ≈1.3–1.4) 위 **스퍼터 Ag ≈100 nm (BSE 89 nm · C 윗면 = SE 쪽)** → 500 MPa 조립 뒤 층 <1 µm ‖ Li₆PS₅Cl (≈1 mm · 250 MPa 선성형) ‖ 단결정 NMC83 : LPS : CNF = 75 : 22 : 3, **4 MPa · 60 °C**. 3 전극 핵생성 과전압 **16.1 → 3.9 mV** (2 mA cm⁻², n 5, std err) · 첫 방전 **163 → 203 mAh g⁻¹** · ICE **71 → 86 %** (1 mA cm⁻², n 3) · 10 사이클 유지율 59.3 % (= C10/C1 충전 · S9 역산). 단면 (P-FIB SEM/EDS · ⁷Li⁺ SIMS): Li 는 **Cu\|C 사이**에 쌓여 C 를 SE 쪽으로 밀어내고 Ag 는 Li 속에 희박 (≈0.5 at% [카드 산술]) → 방전 뒤 **C 위 Ag 덩어리** + Cu–C 사이 큰 공극 · Li 잔여 실. ⚠ **점착 · Li–Ag 상 · SEI 미측정** · η 정의 · iR 미기재 · C 두께는 공급사 값 (단면 figure-read 2–3 µm → 압축 뒤 0.5–0.75 µm) · Cu 쪽 S 신호 (그림 판독 · 본문 언급 없음) | 점착 트랙 (C\|Cu 가 먼저 벌어진다 · LPSCl\|Ag 는 첫 충전 전만) · Li 친화성 표면 모형 (결함 탄소 · 희박 Li(Ag) · Cu) · 핵생성 과전압 순서 |
```

- Jeff Sakamoto 배지: **해당 없음** (저자 아님 · (g)).
- 🎤 talk 역링크: **없음** — 인입 대기열이 있는 talk 은 `lee2026_skku_mlip_materials_design` 하나이고 `metzler` · `sputter` · `스퍼터` · `acsaem.6c01118` 0 건.
- `build_index.py --check`: 이 slug 는 "어느 인덱스에도 없는 것 18편" 목록에 [dft] 로 뜬다 (예상대로 · 메인이 합치면 사라진다).

## (b) `comparison_vs_ours.md` 에 넣을 줄
- **물성 4축 (A–D) 표: 없음** — 계산 0 · σ ≈1.6 mS cm⁻¹ 는 60 °C 풀 셀 EIS 의 R1+R2 (계면형 R2 포함 가능 · 10 kHz 상한) 라 A 축 비교 금지.
- 출처 표 줄 (`[SJ23AgC]` 행 · metzler2025 의 `[Met25AgD]` 행 아래 · 같은 꼴):

```
| **[Met26AgS]** ⭐⭐ **스퍼터 Ag (≈100 nm) / 상용 탄소 (<1 µm) 2 층 — Li 가 Cu\|C 사이에 쌓이고 C 가 SE 쪽으로 밀린다 (P-FIB SEM/EDS + ⁷Li⁺ SIMS)** · ⛔ **점착 · Li–Ag 상 · SEI 미측정 → A–D 물성 4축 수치 진입 금지** · ⚠ σ ≈1.6 mS cm⁻¹ = 60 °C 풀 셀 EIS R1+R2 — A 축 비교 금지 · 탄소 = MTI 상용 "fine particulate C" (Raman I_D/I_G figure-read ≈1.3–1.4) | **Michael Metzler**/C. Doerrer/G. Matthews/Y. Sun/E. Liotti/**Patrick S. Grant\*** (Oxford + Faraday Institution) 2026 ***ACS Appl. Energy Mater.* 9, 9817** (DOI 10.1021/acsaem.6c01118, CC-BY) — "Lithium Plating and Stripping Facilitated by Thin Sputtered Silver and Carbon Interlayers in Anode-Free All-Solid-State Batteries" | ✅ `papers/metzler2026_sputtered_ag_carbon_interlayers_anode_free.md` — 판정은 digest **§0-1** · **§7** · **§10** (+ `comparison_vs_ours_DEM.md` §I 블록) | 실험 전용 (스퍼터 · 3 전극 · P-FIB SEM/EDS · SIMS · Raman · 광학 조도 · EIS · 계산 0) |
```

- (선택) `comparison_vs_ours_DEM.md` **§I** 블록 — metzler2025 가 I-11 을 쓰면 **I-12**:

```
### I-12. `metzler2026_sputtered_ag_carbon_interlayers_anode_free` — ★★ Ag 를 스퍼터로 C 윗면에 고정하자 **Li 가 Cu | C 사이에 쌓이고 C 층이 SE 쪽으로 밀렸다** — 운전 중 처음 벌어지는 계면은 C\|Cu

> **무엇을 주나.** MTI 상용 탄소 코팅 Cu (C ∼1 µm · 압축 뒤 <1 µm) + 스퍼터 Ag ≈100 nm (C 윗면) ‖ Li₆PS₅Cl ‖ NMC83 (500 MPa 조립 · 4 MPa · 60 °C · *ACS Appl. Energy Mater.* 9, 9817 (2026)).  3 전극 핵생성 과전압 16.1 → 3.9 mV (2 mA cm⁻² · n 5) · 첫 방전 163 → 203 mAh g⁻¹.  단면: 충전 = Cu / Li (∼20 µm · Ag 희박) / C / LPSCl · 방전 = Cu / 공극 + Li 잔여 / C + Ag 덩어리 / LPSCl.
>
> **★ 우리 축에 닿는 곳.**
> ① **W 쌍 목록** — C\|Cu · Li\|Cu · Li\|C (리튬화) 가 운전 중 계면이다 · LPSCl\|Ag(111) 는 첫 충전 전만 대표 (그 뒤 SE 쪽 면은 LPSCl\|C · 방전 뒤 C 위 Ag 덩어리).
> ② **I-1 (Liao) 구도와 같은 방향** (탄소\|SE 점착이 크면 CC 쪽 석출) — 이 논문은 점착을 재지 않았다 (순서 관찰 · I-4 와 같은 처지).
> ③ **얇은 탄소 '껍질'** — 호스트 몫 ≲3 % [카드 산술] · Li ≈20 µm 가 <1 µm 층을 밀어낸다 → DEM 에서는 다공 호스트가 아니라 SE 에 붙은 막 + Cu 와의 약한 계면.  탈리 뒤 공극은 하중 해제로 넓어졌을 수 있다 (저자) — 언로딩 단계와 같은 꼴.
>
> **⛔ 인용 금지 / 한정어**
> · 점착 · 응력 · Li–Ag 상 · SEI 수치 없음 — G_c · W 대조 표적이 아니다.
> · 2D 기공률 18.5 % 를 DEM 입력 · 보정 표적으로 쓰지 않는다 (두께 2–3 배 감소와 질량 보존이 안 맞는다 · 저자도 신뢰성 한계 인정).
> · σ ≈1.6 mS cm⁻¹ 는 R1+R2 로 푼 값 — 물성으로 인용 금지 · 셀 n 3 · 5 · 2 · 오차는 std err.
> 상세: digest §0-1 · §3-4 · §3-5 · §8 · §10.
```

## (c) `pdf_map.tsv`
**필수 아님** — `extract_figures.py --inbox --only metzler2026` (드라이) 가 본문 · SI 를 "1쪽 본문 46 %" 로 자동 매칭한다.  굳히고 싶으면 (두 파일에 다 든 조각):
```
metzler2026_sputtered_ag_carbon_interlayers_anode_free	sputag2026_ag_c_sputtered
```

## (d) 추가로 먹일 논문 (8 편 · 이 논문 참고문헌에서 · 최근 것 먼저 · litdb 대조 2026-11-24)
| # | 논문 | 왜 | litdb |
|---|---|---|---|
| 1 | Park, Naik, Vishnugopi, Mukherjee, Hatzell, "Lithium Kinetics in Ag–C Porous Interlayer in Reservoir-Free Solid-State Batteries", *Adv. Energy Mater.* 15, 2405129 (2025) (ref 54 · S5) | Ag–C 층 안 Li 수송 · 석출 위치 · 연속체 (기공률 ≈29 % 기준값 출처) | 카드 없음 (`kang2026_…` · `zhang2026_…` 가 인용만) |
| 2 | Ko et al., "Mechanism of stable lithium plating and stripping in a metal-interlayer-inserted anode-less solid-state lithium metal battery", *Nat. Commun.* 16, 1066 (2025) (ref 51) | 금속 층 위치 (집전체 쪽) ↔ Li 석출 위치 — 층 순서 · Ag–C 기전 | 없음 |
| 3 | Xie, Diallo, Kim, Tu, Ceder, "The Microscopic Mechanism of Lithiation and Delithiation in the Ag/C Buffer Layer for Anode-Free Solid-State Batteries", *Adv. Energy Mater.* 14, 2302960 (2024) (ref 28) | Ag/C 리튬화 미시 기전 · Li–Ag 합금 구동력 | 없음 |
| 4 | Wang, Xia, Ji, Liu, Zhang, He, Zhang, Wan, Wang, "Lithium Anode Interlayer Design for All-Solid-State Lithium-Metal Batteries", *Nat. Energy* 9, 251–262 (2024) (ref 19) | 인터레이어 설계 원리 — 친Li · 소Li · 계면 에너지 · 젖음 | 카드 없음 (`kang2026_…` 가 인용만) |
| 5 | Doerrer, Metzler, Matthews, Bu, Spencer-Jolly, Bruce, Pasta, Grant, "Spraying Li₆PS₅Cl and Silver-Carbon Multilayers to Facilitate Large-scale Fabrication of All-Solid-State Batteries", *Device* 2, 100468 (2024) (ref 29) | 같은 랩 · Ag 위치를 층으로 나눈 '구조화' Ag/C · 제조 (DEM) 축 | 없음 |
| 6 | Müller, Paravicini, Morzy, Krause, Casella, Osenciat, Futscher, Romanyuk, "Influence of Au, Pt, and C Seed Layers on Lithium Nucleation Dynamics for Anode-Free Solid-State Batteries", *ACS Appl. Mater. Interfaces* 16, 695–703 (2024) (ref 48 — 이 논문은 연도를 2007 로 오기) | 금속 · 탄소 씨앗층별 핵생성 과전압 — 핵생성 · 탄소 대 금속 | 없음 |
| 7 | Fuchs, Ortmann, Becker, Haslam, Ziegler, Singh, Rohnke, Mogwitz, Peppler, Nazar, Sakamoto, Janek, "Imaging the microstructure of lithium and sodium metal in anode-free solid-state batteries using electron backscatter diffraction", *Nat. Mater.* 23, 1678–1685 (2024) (ref 61) | 집전체 위 석출 Li 의 결정 조직 (EBSD) — Li\|기판 · Li 면 선택 | 없음 · 참고문헌 표기 'Sakamoto, J.' (Jeff Sakamoto 로 보임 — 원문 확인 필요) |
| 8 | Haslam, Sakamoto, "Stable Lithium Plating in 'Lithium Metal-Free' Solid-State Batteries Enabled by Seeded Lithium Nucleation", *J. Electrochem. Soc.* 170, 040524 (2023) (ref 39) | 매끈 · 연속 vs 덩어리 Au 씨앗 — 이 논문의 '거친 Ag 가 낫다' 근거 · Li\|기판 핵생성 | 없음 · 위와 같은 'Sakamoto, J.' |

차순위 (digest §12 에만): Kwon et al. *Adv. Funct. Mater.* 35, 2420474 (2025) (Cu 부식 — §10-⑥ S 신호) · Futscher et al. *J. Mater. Chem. A* 10, 15535 (2022) (비정질 탄소 층) · Sandoval et al. *Joule* 7, 2054 (2023) · Kim J.-S. et al. *Nat. Commun.* 14, 782 (2023).
같은 배치에서 이미 정리된 이웃 (참고): `lu2026_li_ag_interface_thermodynamics_kinetics` (Li\|Ag 계면 DFT + MLIP — 합금 구동력) · `cicvaric2026_li_nucleation_ni111_cu111_anode_free` (Cu(111) 위 Li 핵생성 실험 + DFT — Cu 면 모형) · `metzler2025_…` (전작).

## (e) DEM-DFT 보고서에 쓸 거리 (W_ad 보고서 §7 · 연속체 · DEM) — 위치 · 직접 봤는지
| 쓸 곳 | 이 논문이 주는 것 | 쪽 · 그림 · 표 | 직접 봤나 |
|---|---|---|---|
| §7 Li 친화성 — 핵생성 과전압 (실험 순서 앵커) | 1 mA cm⁻² (1 셀씩): 꼭지 − 평탄 figure-read ≈ steel 16.7 > Cu 7.5 > C-Cu 2 ≳ Ag C-Cu 0 mV · 2 mA cm⁻² (n 5): C-Cu 16.1 ± 1.1 vs Ag C-Cu 3.9 ± 1.1 mV · 정의 · iR 미기재 → '꼭지 − 평탄' 으로 읽어야 본문 값 재현 · 평탄 (성장) 전압은 안 갈린다 | p.5 · `Fig. 3a,b` · `Fig. 1c` (RE 위치) | 봤다 (셀별 판독 · digest §3-4) |
| §7-1 Ag 표면 모형 | Ag 89–100 nm 스퍼터 막 · C 윗면 (SE 쪽) 에만 · 압축 뒤 "coherent, smoother" · 방위 미측정 → Ag(111) 은 가정 · 500 nm 는 마디 · 틈 메움 · 압축 뒤 Sa 0.075 | p.2–3 · SI S-4–S-5 · `Fig. 1d–g` · `Fig. S1` · `Fig. S2` · `Table S1` | 봤다 (`Fig. 1d` · `Fig. S2a` 확대) · 표는 글자 |
| §7-1 탄소 종류 → 모형 행 | MTI 'fine particulate C' (결합제 · 입경 미기재) · ≈0.1 µm 입자 응집 (figure-read) · Raman D 1359 · G 1588 · 2D 2689 · I_D/I_G ≈1.3–1.4 (figure-read · 532 nm) → **'결함 많은 탄소' 행 (빈자리 결함 기저면) + 흑연 기저면 LiC₆** · 작용기 (XPS 없음) 미상 · `kang2026_…` CNF 0.99 / 0.19 보다 무질서 | SI S-7–S-9 · `Fig. S4` · `Fig. S1a` | 봤다 |
| §7-1 표에 없는 면 — Cu | Li 가 쌓인 곳 = Cu \| C 사이 → Cu(111) · Cu(100) 위 Li 를 후보에 더할 근거 · 방전 뒤 Cu 쪽 S 신호 → Cu 위 황화물 막 (Cu–S · Li₂S) 가능성 [가설] | p.5 · `Fig. 3c–j` · `Fig. S11` · `Fig. 4e,h` · `Fig. S12e` | 봤다 (S 신호는 그림 판독 · 본문 언급 없음) |
| §7 합금 구동력 | 끝 상태 = 희박 Li(Ag) ≈0.52–0.73 at% [카드 산술] (SI: 0.5 vol% · 8.9 wt%) → bcc Li 속 Ag 용해 에너지 · 편석 · 선 스캔에서 Ag 는 Li 의 C 쪽 절반 (3.2–4.9 µm) · 방전 뒤 C 위 재석출 — 'Ag\|C 친화성 증거' 로 쓰지 말 것 (탈리 전선 기하로도 설명) · Li–Ag 상 미측정 | SI S-13 · `Fig. 3d–g` · `Fig. 3i` · `Fig. 4g,h` · p.7 | 봤다 |
| W 쌍 목록 (§2) | 운전 중 계면 = **C\|Cu (먼저 벌어짐)** · Li\|Cu · Li\|C · **LPSCl\|C** · LPSCl\|Ag 는 첫 충전 전 · 일부 자리는 C 가 Cu 에 붙은 채 Li 가 그 아래로 (figure-read) | `Fig. 3c` · `Fig. 5` · `Fig. S11` · p.5 · p.8 | 봤다 |
| 연속체 · DEM 형상 입력 | C 층 공급사 ∼1 µm · 압축 전 단면 figure-read 2–3 µm · 압축 뒤 0.5–0.75 µm · Ag 89 nm · 2D 기공률 26.7 → 18.5 % (**쓰지 말 것** — 질량 보존이면 압축 전 ≈70–90 %) · 조도 Sa/Sq 10 구성 · 조립 250 → 500 MPa · 운전 4 MPa · 60 °C · Ø 5 mm | p.3 · SI S-5–S-8 · `Fig. 1d` · `Fig. S2` · `Fig. S3` · `Table S1` | 그림 봤다 · 표는 글자 |
| Li 두께 · 불균일 (석출 분포 입력) | 같은 셀 저배율 ≈25–28 µm vs 확대 ≈4–5.5 µm · 다른 셀 ≈14 µm · 본문 ∼20 µm · 이론 24.3 µm [카드 산술] (SI 27 µm 는 3482 mAh g⁻¹ 오용) | `Fig. 3c` · `Fig. 3h–j` · SI S-14 | 봤다 (`Fig. 3h` 확대) |
| 탈리 뒤 공극 · 하중 해제 | Cu–C 사이 공극 figure-read ≈15 µm (그 자리) · 모든 탈리 셀에 공극 · *"likely widened after releasing the stack pressure"* · Li 잔여 실 · 다른 셀은 Cu 곁 ≈1.5 µm 남은 층 | p.6–7 · `Fig. 4c–i` · `Fig. S12` | 봤다 |
| 호스트 몫 (층 역할) | Ag (Li₁₀Ag₃ 까지) 1.7 % + C (LiC₆) 0.5–1 % ⇒ ≲3 % [카드 산술] — 담는 층이 아니라 핵생성 · 수송을 거드는 얇은 막 | digest §3-7 | 산술 (그림 아님) |
| 전작 대조 (Ag 위치 vs 유무) | 전작: Ag 위치만 바꾸면 핵생성 전위 차 *"no resolvable"* · ICE 72 → 83 % · 이번: Ag 유무로 16.1 → 3.9 mV | ref 30 원문 (PDF 글자 확인) · 이번 `Fig. 3b` | 전작은 글자만 (그림 안 봄) |

## (f) 그림 크롭
- 도구 **18 개** (그림 17 = 본문 5 + SI 12 · 표 1) · `missing_labels` 없음 · `⚠ 번호 공백` 절 없음 · 손 크롭 0 · 다시 자른 것 0.
- 본 것: **17 장 전부** (Read 렌더) + 확대 확인 3 (`Fig. 1d` · `Fig. 3h` · `Fig. S2a` — scratch 사본 · 저장소에 안 남김).  안 본 것: `Table S1` 이미지 (PDF 글자로 옮김).
- 흠 1 건: `fig_S7.png` 위쪽에 SI 본문 한 줄 ("high current densities.S14") 이 섞였다 — 판독에 지장 없어 그대로 둠.
- **임시 글자 대조 (병렬 충돌 점검)**: 처음 쓴 공용 이름 폴더 `scratchpad/metz/` 의 `main.txt` · `si.txt` 가 PDF 에서 새로 뽑은 글자와 **바이트 단위로 같다** (sha1 1db128d47f3b · 4691043c5ec1) · 제목 · DOI acsaem.6c01118 · 쪽 9817–9827 · SI 머리 확인 + 핵심 숫자 34 개 grep 일치 → 다른 논문 (Metzler 2025 포함) 글자 섞임 없음.  이후 임시 파일은 `scratchpad/metzler2026_sputtered_ag_carbon_interlayers_anode_free/` 에만.

## (g) Jeff Sakamoto
**저자 아님** (6 명: Metzler · Doerrer · Matthews · Sun · Liotti · Grant).  참고문헌 [7] (Masias … 2019) · [39] (Haslam & Sakamoto 2023) · [61] (Fuchs … 2024) 에 'Sakamoto, J.' 로만 나온다.  웹앱 PI 배지 `[]` 확인 · digest 머리 35 줄에 PI 별칭 없음.

## 점수표 (사용자가 번호로 답할 수 있게 · 각 10 점)
| 항목 | 기준 |
|---|---|
| 정확성 | 숫자마다 쪽 · 그림 · 표지 ([인쇄] / figure-read / [카드 산술]) 가 붙었나 |
| 완결성 | 지시 8 항목 (Ag 두께 · 탄소 · 순서 · 전해질 · 전류 · 압력 · 과전압 판독 · Li 위치) + 표면 모형 표 (§0-1) |
| 비판 | 본문 ↔ 그림 어긋남 · 정의 누락을 §10 (15 항목) 에 다 적었나 |
| 쓸모 | W_ad 보고서 §7 · DEM 에 바로 옮길 점 ((e)) 이 위치와 함께 있나 |
