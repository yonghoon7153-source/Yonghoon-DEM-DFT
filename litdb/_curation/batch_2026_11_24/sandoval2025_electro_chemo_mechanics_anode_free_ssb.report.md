# 끝 보고 — sandoval2025_electro_chemo_mechanics_anode_free_ssb (2026-11-24 병렬 묶음)

- digest: `litdb/papers/sandoval2025_electro_chemo_mechanics_anode_free_ssb.md` (747 줄 · 완료)
- 그림: `litdb/figures/sandoval2025_electro_chemo_mechanics_anode_free_ssb/` (9 장 + figures.json)
- 이 편이 쓴 파일은 위 둘과 이 보고서뿐이다. `litdb/figures/_sources.json` 은 추출 도구가 다시 썼다 (손 안 댐). git 작업 없음.
- 논문: Sandoval · Haslam (공동 1) · … · Jeff Sakamoto · McDowell\*, "Electro-chemo-mechanics of anode-free solid-state batteries", *Nat. Mater.* 24, 673–681 (2025) · Perspective · 온라인 2025-01-02 · DOI 10.1038/s41563-024-02055-z · 본문 9 pp + SI 6 pp · refs 98

---

## (a) `litdb/INDEX.md` 에 넣을 행

**넣을 절 (권고)**: `## 🧲 계면 점착 · 인터레이어 트랙 — LPSCl 이 한쪽 면인 계면/벌크 역학의 실측 앵커 (2026-09-23 신설)` 표 끝.
그 절 머리말이 '실측 앵커' 라서 행 안에 '관점 · 값 0 · 출처 지도' 를 박아 두었다. 그 절이 맞지 않다고 보면 대안은 `## ✅ Digest 완료 (paper-level)`.
`build_index.py --check` 는 이 편을 `[dem]` 으로 분류한다 → `INDEX_DEM.md` 는 재생성 때 자동으로 잡힌다.

```
| `papers/sandoval2025_electro_chemo_mechanics_anode_free_ssb.md` **(본문 9 pp + SI 6 pp · 크롭 9장 (그림 6 + 표 3) · 그림 6장 전부 실독 · 손 크롭 1 (Fig. 1) · 재크롭 3 (Fig. 2 · 3 · 4))** | 🏷 **Jeff Sakamoto 공저** · **[외부·리뷰(Perspective)·⭐⭐ 무음극 전기-화학-역학 field map · 자체 데이터 0 → 값 앵커 아님 · 출처 지도]** ✅ **Stephanie Elizabeth Sandoval**/**Catherine G. Haslam**(공동1)/B. S. Vishnugopi/D. W. Liao/J. S. Yoon/S. H. Park/Y. Wang/D. Mitlin/K. B. Hatzell/D. J. Siegel/P. P. Mukherjee/N. P. Dasgupta/**Jeff Sakamoto**/**Matthew T. McDowell\*** (MUSIC DOE EFRC · Georgia Tech · Michigan · Purdue · Princeton · UT Austin · UCSB), "**Electro-chemo-mechanics of anode-free solid-state batteries**" — ***Nat. Mater.* 24, 673–681 (2025)** (Perspective · 온라인 2025-01-02), DOI `10.1038/s41563-024-02055-z`. 첫 석출 = CC\|SE 접촉점에서만 핵생성 (전류 · 적층압 · 온도 · CC 두께 · Cu/Li₂O 화학 불균일 · SE 미세구조 — `Fig. 2a` 매개변수 11 개) → 사이클 = **CE > 99.95 % for 1,000 cycles** (ref 37) · 방전 끝 **국부 Li 고갈 → 낮은 전체 전류에서도 공극 → 필라멘트** (ref 23 · `Fig. 3d`) → 인터레이어 = 탄소 (ref 88) · Au/Ag 100–150 nm (refs 24 · 29) · Li₂Te (ref 95) · **Ag–C 1,000 사이클+** (refs 30 · 82) · `Table S3` 16 행. 압력 층위 셋: 제조 **10–500 MPa** · 실험실 **1–수백 MPa** · 실용 **< 1 MPa**. ★ **DFT 는 Cu · Cu₂O 둘 다 친Li 인데 sessile drop 은 깨끗한 Cu 만 — Cu₂O → Li₂O (소Li)** (ref 25) = W_ad §7 '반응 뒤 표면' 의 문헌 근거. 고유 수치 = SI 에너지밀도 **1,208 → 1,435 Wh/L (+19 %) · 464 → 479 Wh/kg (+3 %)** (✎ `Table S2` 로 재현 · 'Li 과잉' = 20 µm ≈ 양극 용량 1.02 배). ⚠ 점착 수치 0 · `Fig. 4b` Au '전체에 흩어짐' vs 그림은 두 경계 띠 · `Fig. 4c` 는 석출 1 회 뒤 사진 · LPSCl 1.64 g/cm³ 무인용 · 보이는 공저자 자기 인용 ≥ 27/98 | 무음극 · 공극/필라멘트 · 적층압 · 인터레이어 · 집전체 · 점착 트랙 출처 지도 · W_ad §7 · DEM 입력표 |
```

선택 (메인 판단) — `INDEX.md` '🧮 LPSCl 펠릿 밀도 · 진밀도 1.64 출처 묶음' 표에 한 줄:

```
| `sandoval2025_electro_chemo_mechanics_anode_free_ssb` | Nat. Mater. 관점 논문 SI `Table S2` — 에너지밀도 산정에 LPSCl 밀도 **1.64 g/cm³ 무인용** (상대밀도 90 % · 계산기 = Wang 2021 *Joule* 5, 1371) · 결정밀도 ≈1.86 이면 중량값 −2.4 % [카드 산술] |
```

## (b) `comparison_vs_ours.md`

**없음 (리뷰)** — 물성 4 축 (A 이온 · B 산화 · C 기계 · D 전자) 에 넣을 수치가 0 이다.
선택: `comparison_vs_ours_DEM.md` §I 끝 (I-10 뒤 '추가' 줄 꼴) 에 한 줄:

```
> 2026-11-24 추가 — `sandoval2025_electro_chemo_mechanics_anode_free_ssb` — (관점 · 값 0 · 출처 지도) 무음극 전기-화학-역학 리뷰.  점착 축에 주는 것은 셋: ① W_ad 를 **반응 뒤 표면**에서도 내야 한다는 문헌 실례 (Cu₂O 는 DFT 로 친Li · 실측은 Li₂O 로 바뀌어 소Li · ref 25 = Yoon 2024 *ACS AMI*) ② `Fig. 2a` 의 K_c,SSE/CC (석출 가장자리 = CC|SE 계면 균열 선단) = 우리 DEM 박리 G_c 와 같은 부류의 자리 ③ 압력 층위 (제조 10–500 · 실험실 1–수백 · 실용 < 1 MPa).  W · G_c · Γ 숫자 0 건 → 대조 표적도 보정 표적도 아니다.
```

## (c) `pdf_map.tsv`

필요하다. `--inbox` 자동 매칭 (dry) 이 본문만 붙이고 (1 쪽 본문 47 %) SI 를 '짝 못 찾음' 으로 남긴다:

```
sandoval2025_electro_chemo_mechanics_anode_free_ssb	afssb2024_electro_chemo_mechanics
```

## (d) 추가로 먹일 만한 논문 (8 편 · 이 관점 논문이 인용한 것 · 최근 것 먼저)

litdb 확인 = `litdb/papers` 파일 이름 + 제목 문구 전문 검색 (8 편 모두 digest 0 · 문구 일치 0). 이 논문 인용 중 **이미 이번 묶음에 들어온 것** (ref 10 wang2020 · 21 wang2019 · 32 fuchs2023 · 36 lee2022) 은 뺐다.

| # | 논문 (본문 ref) | 저널 · 연도 | 왜 | litdb |
|---|---|---|---|---|
| 1 | Yoon J. S. et al., "Thermodynamics, adhesion, and wetting at Li/Cu(-oxide) interfaces: relevance for anode-free lithium-metal batteries" (25) | *ACS Appl. Mater. Interfaces* 16, 18790 (2024) | **Li 금속\|기판 점착** (DFT 친Li 판정 + sessile drop) · Cu₂O → Li₂O 가 젖음을 뒤집는 실례 · W_ad §7 에 바로 걸림 | 없음 |
| 2 | Liao D. W. et al., "Interfacial dynamics of carbon interlayers in anode-free solid-state batteries" (88 · `Fig. 4a`) | *J. Mater. Chem. A* 12, 5990 (2024) | **인터레이어** · Li 석출 위치 (LPSCl) — `liao2025_…` (점착 Γ 문턱) 의 전작 | 없음 (liao2025 머리에 계보로만) |
| 3 | Xie F., Diallo, Kim, Tu, Ceder, "The microscopic mechanism of lithiation and delithiation in the Ag/C buffer layer for anode-free solid-state batteries" (92) | *Adv. Energy Mater.* 14, 2302960 (2024) | **Ag–C 인터레이어** 기전 · 석출 동역학 | 없음 |
| 4 | Müller A. et al., "Influence of Au, Pt, and C seed layers on lithium nucleation dynamics for anode-free solid-state batteries" (85 · SI 9) | *ACS Appl. Mater. Interfaces* 16, 695 (2024) | **시드층 · 핵생성 과전압** = 실험 쪽 Li 친화성 지표 (무음극) | 없음 |
| 5 | Lee K. & Sakamoto J., "Li stripping behavior of anode-free solid-state batteries under intermittent-current discharge conditions" (61) | *Adv. Energy Mater.* 14, 2303571 (2024) | 무음극 **박리 · 공극** · 거칠기 → 박리 용량 · CE (Jeff Sakamoto) | 없음 |
| 6 | Lewis J. A. et al., "Accelerated short circuiting in anode-free solid-state batteries driven by local lithium depletion" (23) | *Adv. Energy Mater.* 13, 2204186 (2023) | ★ **무음극 고유 공극 → 필라멘트** 기전 (`Fig. 3d` 의 1 차) — 이 관점 논문의 핵심 주장 하나가 이 편에 기댄다 | 없음 |
| 7 | Sandoval S. E. et al., "Structural and electrochemical evolution of alloy interfacial layers in anode-free solid-state batteries" (29 · `Fig. 4b` · SI 2) | *Joule* 7, 2054 (2023) | Au/Ag 100 nm **인터레이어** 진화 (LPSCl · Cu) · 황화물 CC 압착 10–500 MPa 근거 · Au 입자 분포 확인 (§10-④) | 없음 |
| 8 | Seymour I. D., Quérel, Brugge, Pesci, "Understanding and engineering interfacial adhesion in solid-state batteries with metallic anodes" (53) | *ChemSusChem* 16, e202202215 (2023) | **금속 음극 점착** 리뷰 — W_ad 보고서 '점착과 공극' 틀 | 없음 (같은 1저자 2021 *JMCA* 는 이번 묶음 `seymour2021_…`) |

(8 편 밖 참고 — 넣지 않음: Ag–C 원조 Lee Y.-G. 2020 *Nat. Energy* 5, 299 (ref 30) 는 2020 이라 뒤로 미뤘다.)

## (e) DEM-DFT 보고서에 쓸 거리 (W_ad 보고서 §7 · 연속체 · DEM)

보고서 = `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` (§2 쌍별 값 · §7 Li 친화성 · §7-1 대상 표면). 우리 W 값은 digest 에 안 실었다 (위치만).

| # | 쓸 곳 | 이 논문이 주는 것 | 쪽 · 그림 | 직접 봤나 |
|---|---|---|---|---|
| 1 | §7 Li 친화성 · '할 수 없는 것' · §7-1 | ★ **명목 표면의 DFT 친Li 판정이 실측과 어긋난 실례** — Cu · Cu₂O 둘 다 DFT 친Li · sessile drop 은 깨끗한 Cu 만 (Cu₂O + Li → Li₂O, 소Li). ⇒ W 를 반응 뒤 표면에서도 낸다 · §7-1 표에 **CC 면 (Cu · SUS + 산화막)** 후보 추가 근거 | p. 676 'Interface and interphase effects' 첫 문단 · `Fig. 2f` · ref 25 | `Fig. 2f` ✅ (도식) · 본문 ✅ |
| 2 | §7 방법 3 (합금 · 반응) | 합금 · 화합물 (Li₃Au · LiₓAg · Li₂Te) → **핵생성 과전압↓ → 순간 대신 연속 핵생성** → 균일층 · Au 막은 충전 중 입자로 쪼개짐 · Li₂Te 는 유지 | p. 678 둘째–셋째 문단 · `Fig. 4b,c` · refs 85 · 93–95 · 24 · 29 | `Fig. 4b,c` ✅ |
| 3 | 점착과 공극 (새 절 후보) | 점착 · 젖음 조절 = **저압 사이클의 핵심** (ref 53) · **점착 ↔ Li 내부 응력 얽힘** (ref 74) · Li 와 계면상 · 이질 CC 점착 → 접촉 상실 동역학 (p. 676) · 무음극 방전 끝 공극 기전 (ref 23) | p. 678 결론 · p. 676 · p. 676–677 · `Fig. 3d` | `Fig. 3` ✅ (재크롭 뒤 전폭) |
| 4 | 인터레이어 (새 절 후보) | **새 계면 둘 (CC\|IL · IL\|SSE)** · IL 점착이 강해야 (ref 86) · SE 와 Li 양쪽에 붙는 IL (결론) · 석출 위치 (CC\|탄소 vs 탄소\|SSE) 는 계면에너지 · 기공 · 탄소 종류로 바뀜 (refs 86 · 90) → W 쌍에 **Li\|IL · CC\|IL** 필요 | p. 677 'Interfacial modification' 첫 문단 · p. 678 · `Fig. 4a,d` | `Fig. 4a,d` ✅ — **탄소 · Ag–C 둘 다 Li 가 CC 쪽 (인터레이어 아래)** |
| 5 | 연속체 · DEM 입력표 | `Fig. 2a` 매개변수 11 개 (t_CC · σ_Li · σ_CC · σ_SSE · γ_SSE/Li · γ_Li/CC · K_c,SSE/CC · K_c,SSE · d_SSE · V_LiΔG_V · 계면상) · 석출 가장자리 K_c,SSE/CC = **CC\|SE 계면 균열 (블리스터)** · 우리가 채울 칸 = γ (DFT) · d_SSE (DEM) · K_c,SSE/CC 하한 (W ≤ G_c) | p. 675 `Fig. 2` 캡션 · `Fig. 2a` | `Fig. 2a` ✅ (재크롭 — 위 라벨 줄 살림) |
| 6 | DEM 압력 단계 등록 | 제조 10–500 MPa (refs 29 · 30) · 실험실 1–수백 MPa (refs 10 · 20 · 22 · 36) · 실용 < 1 MPa (refs 37 · 81) · > 1 MPa 크리프 (refs 10 · 20 · 36) · 고압 = 공극↓ 침입↑ (refs 78–80) | p. 674 · 675 · 677 · 678 · `Fig. 2c` | `Fig. 2c` ✅ · 본문 ✅ |
| 7 | CC 경계조건 | 얇은 CC 파단 · Li 분출 / 두꺼운 CC 균일 · CC 는 남은 Li 따라 휜다 → CC 를 강체 벽 말고 휘고 찢어지는 판으로 (`Table S2` Cu 5 µm) | p. 676 · `Fig. 2e` · `Fig. 3c,d` | ✅ |
| 8 | 방전 끝 접촉 분율 (제안) | 고립 Li 섬 → 기하 접촉 면적↓ → 낮은 전체 전류에서도 국부 고전류 — DEM SE 표면 지형 → 접촉 분포 → 전류 분포 모델 | p. 676–677 · `Fig. 3d` · ref 23 | ✅ |
| 9 | 석출 Li 형상 | 치밀 Li **4.89 µm per mAh cm⁻²** (✎ `Table S2` 상수) · `Fig. 4` 픽셀 판독 b 0.99 · d 0.99 · a 0.80 · c 0.85 배 (기울기 보정 미상) | digest §3.6 · §13-2 | `Fig. 4` ✅ (+ 픽셀 단면 판독) |
| 10 | 셀 형상 기본값 | SE 20 µm · 복합양극 ✎ 75.9 µm · CC 5 µm · Li 0/20 µm (`Table S1` 재현으로 확인) | SI p. 4 `Table S2` | ✗ 이미지 안 봄 (PDF 텍스트) |
| 11 | 우리 DFT 제안 (보고서 밖) | LPSCl 환원 '수축 → 공극' 주장 (refs 56–58) 을 같은 방법 반응 부피로 가를 수 있다 (값 없음) | p. 676 | 본문 ✅ |

## (f) 그림 크롭 요약 · 본 그림 · 어긋난 곳 · scratchpad 대조

- **크롭 9 장** = 그림 6 (본문 Fig. 1–4 + SI Fig. S1–S2) + 표 3 (Table S1–S3). **그림 6 장 전부 Read 로 봤다.** 표 3 장은 이미지로 안 봤다 (PDF 텍스트 · Table S3 은 pymupdf find_tables 로 칸 대조).
- 도구가 놓친 것 1 = **Fig. 1** ('p2 영역 없음' — 작은 래스터 ≈1,140 조각 + 벡터 상자 도식) → 손 크롭 · figures.json `manual_crop` + `missing_labels[f1].resolved`.
- 도구 크롭이 잘린 것 3 → 재크롭 · `recrop` 사유 기록: **Fig. 2** (패널 라벨 a · F_stack pressure 줄) · **Fig. 3** (왼쪽 단만 — b · c · d 패널과 확대 원 둘이 빠졌었다) · **Fig. 4** (패널 제목 줄). `--audit` 경고 없음.
- **그림 ↔ 본문 어긋남 (digest §10)**: ① `Fig. 4b` — 본문 'Au 입자가 Li 층 *전체에*' vs 그림은 CC\|Li · Li\|SSE **두 경계 띠** ② `Fig. 4c` — 본문 '사이클 중 구조 유지' vs 캡션은 **석출 1 회 뒤** ③ `Fig. 4a` — 본문 '탄소층 전체에서 Li 성장' (ref 81) vs 그림은 **CC 와 탄소 사이 치밀층** (ref 88) ④ `Fig. 2d` — 그림은 고온 = 성긴 큰 핵 + '?' · 본문은 방향을 안 정함 ⑤ `Fig. S2` — LPSCl 값만 그렸는데 라벨 없음 ⑥ `Fig. 1` 1,435 vs `Table S1` 1436 (버림 vs 반올림).
- **scratchpad 충돌 대조**: 공용 이름 `scratchpad/main.txt` 가 11:39 에 다른 논문 (nicu2026) 글자로 덮어써진 것을 작업 중에 발견 — 덮어쓰기 **전에** Read 한 글자는 이 논문 (제목 · 저자 · 쪽 머리 'Nature Materials | Volume 24 | May 2025 | 673–681') 이었다. 그 뒤 전용 폴더 `scratchpad/sandoval2025_electro_chemo_mechanics_anode_free_ssb/` 에 PDF 에서 다시 뽑아 digest 의 핵심 문구 · 수치 **51 개** (본문 33 · SI 18) 를 새 글자와 대조 → **전부 일치** (줄바꿈 · '∼' 문자 정규화 뒤 · 'Reservoir Free' 는 `Fig. S1` 그림 속 글자라 텍스트 층에 없음 — 그림으로 확인). 참고문헌 98 편 지도는 전용 폴더 사본에서만 만들었다.

## (g) Jeff Sakamoto 저자 여부

**예 — 공저** (교신은 Matthew T. McDowell). 소속 번호 3 · 4 · 6 · 12 · 13 (MUSIC EFRC · Michigan MSE · Michigan ME · UCSB Materials · UCSB ME).
digest 머리 저자 줄에 **'Jeff Sakamoto'** 로 적었고, `webapp/data.py` `_paper_pis()` 로 `['sakamoto']` 배지가 잡히는 것을 확인했다. (a) 행 둘째 칸 맨 앞에 `🏷 **Jeff Sakamoto 공저** · ` 를 넣었다.

---

### 기타 (메인 세션 참고)

- 🎤 talk 인입 대기열: 이 논문 없음 (`litdb/talks/*` 검색 0).
- webapp 확인: Figure set 표 주석이 9 키 (f1–f4 · fS1 · fS2 · tS1–tS3) 모두 '표 → 절' 순으로 잡힌다 (`paper_figure_notes`). Fig. 4 는 주석 칸이 3 개라 '4a,d (탄소 계열)' · '4b,c (시드 계열)' 두 줄로 묶었다.
- 메인 세션 checkpoint 커밋 (`litdb: checkpoint of the parallel curator run`) 이 이 digest 의 중간본을 담고 있다 — 최종본은 그 뒤 §14 (참고문헌 98 편 제목 추가 · 같은 묶음 slug 표시) 가 바뀌었다.
