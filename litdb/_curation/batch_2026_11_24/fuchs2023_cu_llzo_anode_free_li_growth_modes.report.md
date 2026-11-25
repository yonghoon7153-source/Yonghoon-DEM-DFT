# 끝 보고 — fuchs2023_cu_llzo_anode_free_li_growth_modes (2026-11-24 · litdb-curator · 배치 #10)

쓴 파일은 셋이다.
- digest `litdb/papers/fuchs2023_cu_llzo_anode_free_li_growth_modes.md` (543 줄 · 표 13 개 · 칸 수가 어긋난 줄 0 · Python-Markdown 으로 렌더해서 확인)
- 그림 `litdb/figures/fuchs2023_cu_llzo_anode_free_li_growth_modes/` (크롭 16 장 + figures.json + 동영상 프레임 jpg 21 장)
- 이 보고 파일

`litdb/figures/_sources.json` 은 추출 도구가 다시 썼다 (손 안 댐). 공유 파일 · git 은 안 건드렸다.
⚠ 메인 체크포인트 커밋 (b60590e6 · 650af2c3 · 1b9f8a85) 에 크롭 · 프레임 · digest 의 앞선 판이 이미 들어가 있다. 최종본은 지금 작업 트리에 있는 digest 다. 커밋 뒤에 고친 것: 같은 배치 slug 교차 참조 · Wang 2020 대조 · LLZO:Ta 출처 표기 · 머리 주석.

확인한 것
- 웹앱 `/paper/<slug>` 200 · Sakamoto 배지가 뜨고 그림 16 장이 붙는다 · `paper_figure_notes` 가 16 개 키 전부 (f1–f7 · fS1–fS9) 에 붙는다. 동영상 두 행은 어느 그림에도 안 붙는다 (첫 칸에 숫자를 안 썼다).
- `_paper_pis` = `['sakamoto']` · 원소 태그 Li · Cu · La · Zr · O · Al · Ta · 기법 태그는 비움 (operando SEM · EIS 가 METHOD_MAP 에 없다 — `spencerjolly2023` 과 같은 꼴).
- `pytest webapp/tests/test_v3_literature.py` → 20 passed.
- `build_index.py --check` → 이 slug 는 "어느 인덱스에도 없음 [dft]" 와 "comparison_vs_ours.md 미편입" 두 곳에만 뜬다 (rc 1 은 배치 18 편이 대기 중이라서다). 아래 (a) · (b) 를 넣으면 풀린다.
- `extract_figures --audit` → 이 slug 경고 없음 (본문 7 · SI 9 · 표 0). `--inbox --only fuchs2023` → 본문 · SI 가 자동으로 짝지어진다 (제목 51 %).
- talk 인입 대기열 (`litdb/talks/*`) 에 이 논문은 없다. 역링크는 필요 없다.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: build_index 분류는 [dft] → `INDEX.md`. 이 배치 (무음극 Li 성장 · 공극 · 점착 18 편) 를 묶는 새 절을 만들면 거기 넣는다 (예: `## 🌱 Li 금속 음극 — 무음극 성장 · 핵생성 · 공극 · 압력 (2026-11-24 배치)`). 새 절이 없으면 `## 🧲 계면 점착 · 인터레이어 트랙` 끝에 넣는다. 다만 그 절은 머리말이 "LPSCl 이 한쪽 면" 이고 이 편은 LLZO 라서, 행에 `⚠ LLZO 계` 표지를 달았다.

```
| `papers/fuchs2023_cu_llzo_anode_free_li_growth_modes.md` **(본문 11 pp + SI 7 pp · 크롭 16장 전부 실독 · 동영상 2편 프레임 21장 (2 초 간격 19 + 끝 2) · 2026-11-24)** | 🏷 **Jeff Sakamoto 공저** · **[외부·exp·⭐⭐ 무음극 Cu\|LLZO 첫 충전 Li 성장 — operando SEM · ⚠ LLZO 계 (SEI 없음 · LPSCl 로 수치 이식 금지) · 원자단위 계산 0]** ✅ **Till Fuchs**/**Juri Becker** (공동1)/C. G. Haslam/C. Lerch/**Jeff Sakamoto**/**Felix H. Richter\***/**Jürgen Janek\*** (JLU Giessen 물리화학 · ZfM + Univ. Michigan MSE · ME), "**Current-Dependent Lithium Metal Growth Modes in "Anode-Free" Solid-State Batteries at the Cu\|LLZO Interface**" — ***Adv. Energy Mater.* 13, 2203174 (2023)**, DOI `10.1002/aenm.202203174` (OA CC BY-NC-ND). 100 nm Cu 패치 (≈150 µm² · W 탐침) 에 16 µAh cm⁻² 도금: 50 → 1000 µA cm⁻² 에 핵 밀도 **≈7 → ≈61×10⁶ cm⁻²** (개수 11 → 92 = 8.4 배 · 본문 '6 배') · 평균 투영 면적 figure-read ≈1.8 → ≈0.26 µm² (본문 '4 → 0.5') · **투영 덮임은 ≈12–17 % 로 거의 그대로** (카드 산술 — 저자의 'coverage 증가' 와 어긋남) · 단결정 LLZO 는 탐침 옆 한 곳만 (η_nuc 200 vs < 50 mV · 곡선 없음) · 100 µA cm⁻² + **2000 µA cm⁻² ≈10 s 펄스 둘** (본문 '1000') → 30 min N ≈172 vs ≈63×10⁶ cm⁻² (n = 1 · 펄스 전부터 두 패치 ≈10 배 차) · 100 · 400 nm Cu 는 Li 위스커가 뚫고 5 µm 막 · 10 µm 박은 안 뚫림 · 10 µm 박 단면 (0 MPa · LLZO:Ta): 50 · 100 µA cm⁻² = 위스커 + 막 (Li 는 Cu–LLZO 직접 접점에서 핵 · 틈 ≈2 µm) · 500 µA cm⁻² = SE 안 Li (45–100 s 전압 요동) · R_int 630 → 105 Ω cm² (2 MPa · figure-read · 본문 'several 100') · 벗기기 CE 13 % · ⚠ 탐침 근처 편중 · 빔 조건 미기재 (빔 유도 Li 석출을 저자가 인정) · LLZO:Al ↔ LLZO:Ta 교락 | **무음극 Li 핵생성 · 성장 모드 · 집전체 두께 (W_ad 보고서 §7 실험 대조 · DEM 핵 자리 = CC–SE 접점 · 계면 틈)** (exp, 외부 · LLZO) |
```

## (b) `comparison_vs_ours.md` 에 넣을 줄

물성 4축 (A–D) 에는 **넣을 것이 없다** (LLZO 의 σ · 탄성 · 띠틈이 이 논문에 없다). **§E (환원 / 음극 Li 금속 계면)** 에 전제 대조 한 줄과, Reference key 한 줄을 넣는다.

§E 행:
```
| **🆕 (2026-11-24) 무음극 첫 충전의 Li 핵생성 · 성장 모드 숫자는 'SE 가 Li 에 안정' 한 계의 값이다 — Cu\|LLZO 에서 핵 밀도 ≈7 → ≈61×10⁶ cm⁻² (50 → 1000 µA cm⁻² · 16 µAh cm⁻²) · η_nuc ≤ 50 mV (다결정) · Li 는 Cu–LLZO 직접 접점에서 핵 · ≤ 400 nm Cu 는 위스커가 뚫는다** | **[Fuchs23CuLLZO]** `Fig. 2e` · `Fig. 5` · `Fig. S7` · p.2 · p.4 · p.6 (LLZO · 0 MPa · 조건당 n = 1) | 환원 가장자리 **1.717 V** (Li 교환 0 · comp1 = modelc · grand-potential) — Cu\|LPSCl 무음극 셀은 핵 전 전위 하강이 이 가장자리를 지나므로 첫 핵이 환원 산물 (0 V 끝 Li₂S + Li₃P + LiCl) 옆에 선다 (열역학 · 속도는 계산 밖) · 핵생성 · 성장 모드 계산은 없다 (§H · W_ad 보고서 §7 '할 수 없는 것') | — 축 다름 (전제 대조) · ⛔ 핵 밀도 · η_nuc · 모드 경계 전류를 LPSCl 값으로 옮기지 않는다 |
```

Reference key 행:
```
| **[Fuchs23CuLLZO]** ⭐⭐ **무음극 Cu\|LLZO 첫 충전 Li 성장 (operando SEM) — 핵 밀도 vs 전류 · CC 두께 · 성장 모드** · ⛔ **LLZO (SEI 없음) · exp 전용 · A–D 물성 4축 진입 금지** (§E 1 행만) | Till Fuchs/Juri Becker/C. G. Haslam/C. Lerch/Jeff Sakamoto/F. H. Richter\*/J. Janek\* (JLU Giessen · Univ. Michigan) *Adv. Energy Mater.* 13, 2203174 (2023) | `papers/fuchs2023_cu_llzo_anode_free_li_growth_modes.md` ✅ | exp |
```

(선택) `comparison_vs_ours_DEM.md` §I 카드 — 번호는 메인이 매긴다 (`sharafi2017` 보고서도 I-11 을 제안했다):
```
### I-xx. `fuchs2023_cu_llzo_anode_free_li_growth_modes` — (인접 축 · 점착 정량 없음 · ⚠ LLZO 계) 무음극 Cu|LLZO 첫 충전 Li 성장 — 핵 자리 = CC–SE 직접 접점 · 무압에서 계면 ≈2 µm 벌어짐 · CC 관통 문턱 400 nm–5 µm

> **무엇을 주나.** operando SEM (W 탐침 · FIB 패치 ≈150 µm² · 0 MPa · 25 °C): 100 nm Cu 위 16 µAh cm⁻² 에 핵 밀도 ≈7 → ≈61×10⁶ cm⁻² (50 → 1000 µA cm⁻²) · 투영 덮임 ≈12–17 % (카드 산술) · 10 µm Cu 박 단면에서 Li 는 Cu–LLZO 직접 접점에서 핵 → 계면이 ≈2 µm 벌어짐 (100 µA cm⁻² · ≈97 µAh cm⁻²) · 500 µA cm⁻² 는 SE 안 Li · 100 / 400 nm Cu 관통 · 5 µm 막 / 10 µm 박은 관통 없음 · R_int 630 → 105 Ω cm² (2 MPa · figure-read).
> **★ DEM 쪽에 닿는 곳.** ① 핵 자리 = 접촉점 (DEM 접촉망 출력 → 무음극 핵 모델 입력) · ② 모드 (i) 위스커 = CC–SE 계면이 Li 성장으로 열림 → CC–SE 분리 기준 (G_c 류) 이 모드를 가르는 변수 · 값은 이 논문에 없다 (같은 계 Wang 2020 의 박리 점착은 그 digest 에) · ③ CC 막 강성 문턱 (400 nm–5 µm) — Ag–C · CC 를 막으로 넣을 때의 차수.
> **⛔ 인용 금지 / 한정어.** LLZO 수치를 LPSCl 로 옮기지 않는다 · 'coverage 증가' 로 인용하지 않는다 (덮임은 거의 그대로) · 펄스 '≈3 배' 는 n = 1 · 핵 밀도는 척도에 따라 다르다 (같은 50 µA cm⁻² 에서 Wang 2020 ≈10³ cm⁻²) · frame[4]: 대조 표적이지 보정 표적이 아니다.
```

## (c) `pdf_map.tsv`

**필요 없다.** digest 를 쓴 뒤 `--inbox --only fuchs2023` 가 본문 · SI 를 제목 51 % 로 자동 짝지었다. (mp4 두 편은 추출기가 다루지 않는다. 프레임은 ffmpeg 로 따로 뽑았다.)

## (d) 추가로 먹일 만한 논문 (≤ 8)

최근 것 (2024–2026) 중 이 주제의 핵심 편은 대부분 **이미 이 배치에 들어 있다**: Sandoval 2025 *Nat. Mater.* · Metzler 2025 / 2026 · Lu & Trinkle 2026 · Cicvarić 2026 · Kim 2026 · Shi 2026. 그래서 아래는 2024 한 편 다음은 2023 이전이다. 서지를 확인한 정도를 칸마다 적었다. "기억" 이라고 적은 것은 원문 확인 전에 인용하지 않는다.

| # | 논문 | 왜 | litdb | 서지 확인 |
|---|---|---|---|---|
| 1 | T. Fuchs et al., "Imaging the microstructure of lithium and sodium metal in anode-free solid-state batteries using electron backscatter diffraction", *Nat. Mater.* (2024) | 같은 1저자의 후속편. 무음극 Cu\|LLZO 에서 석출 Li 의 결정립 · 방위를 봤다. 이 논문이 *"grain orientation was not determined"* 로 남긴 빈칸이다. Sakamoto 공저로 기억한다 | 없음 | ⚠ 기억 — 권 · 쪽 · 저자 확인 필요 |
| 2 | S. E. Sandoval et al., "Structural and electrochemical evolution of alloy interfacial layers in anode-free solid-state batteries", *Joule* 7, 2054 (2023) | **LPSCl** 무음극 + 합금 인터레이어 (Ag 등). Li 핵 · 성장의 황화물 쪽 대조이고 Ag–C 와 바로 이어진다 | 없음 | 권 · 쪽은 `zhang2026_anode_free_asslsb_li2s_pi3_na_current_collector.md` 참고문헌으로 확인 · 제목은 기억 |
| 3 | Y. Wang et al. (… B. S. Vishnugopi, P. P. Mukherjee, G. Henkelman, D. Mitlin), *Adv. Mater.* 35, 2206762 (2023) | Li₂Te 친리튬 Cu 집전체 무음극 ASSB · DFT + 메조 모델. W_ad §7 의 '친Li 코팅 집전체' 를 계산 + 실험으로 다룬 선례 | 없음 | 저자 · 권 · 쪽은 zhang2026 digest 로 확인 · **제목 원문 확인 필요** |
| 4 | E. Kazyak et al., "Understanding the electro-chemo-mechanics of Li plating in anode-free solid-state batteries with operando 3D microscopy", *Matter* 5, 3912 (2022) | 이 논문 ref [25]. 같은 Cu\|LLZO 무음극에 **압력**을 더했다 (1–5 MPa 에서 Li 물집이 눌린다). '기공 벽 핵생성' 관찰이 이 논문과 충돌한다. **Jeff Sakamoto 공저** (이 논문 참고문헌 저자 목록에서 확인) | 없음 (`kazyak2020_…` 는 다른 편) | 저자 · 권 · 쪽 확인 · 제목은 기억 |
| 5 | S. Narayanan et al., "Effect of current density on the solid electrolyte interphase formation at the lithium\|Li₆PS₅Cl interface", *Nat. Commun.* 13, 7237 (2022) | LPSCl 쪽 **전류 밀도 의존 SEI**. 이 논문을 LPSCl 로 옮길 때 빠지는 축 (핵 전 SEI) 이다 | 자체 digest 없음 | 저자 · 권 · 쪽은 `beutl2024_round_robin_coin_cell_sulfide_assb.md` 참고문헌으로 확인 · 제목은 기억 |
| 6 | Y.-G. Lee et al., "High-energy long-cycling all-solid-state lithium metal batteries enabled by silver–carbon composite anodes", *Nat. Energy* 5, 299 (2020) | 이 논문 ref [3]. **Ag–C 원전**인데 litdb 에 자체 digest 가 없다 (여러 digest 에서 인용만 된다) | 자체 digest 없음 | 권 · 쪽은 이 논문 참고문헌으로 확인 · 제목은 기억 |
| 7 | T. Krauskopf et al., "Lithium-metal growth kinetics on LLZO garnet-type solid electrolytes", *Joule* 3, 2030 (2019) | 이 논문 ref [16]. LLZO 위 Li 핵생성 · 성장 동역학의 원전이다 (같은 Giessen 그룹 · η_nuc) | 없음 | 권 · 쪽은 참고문헌으로 확인 · 제목은 기억 |
| 8 | K. Yan et al., "Selective deposition and stable encapsulation of lithium through heterogeneous seeded growth", *Nat. Energy* 1, 16010 (2016) | 기판별 Li 핵 과전압 (Au · Ag · Zn · Mg ≈ 0, Cu 는 뚜렷한 과전압). 'Li 친화성' 의 표준 실험이라 W_ad §7 ①–③ 의 계산 순위를 맞춰 볼 표적이다 (액체 전해질) | 없음 | ⚠ 기억 |

그다음 후보: Pei et al. *Nano Lett.* 17, 1132 (2017) (ref [22] · 액체에서 핵 밀도의 전류 의존) · Motoyama et al. *ACS Appl. Mater. Interfaces* 12, 38045 (2020) (ref [23] · Cu\|LIPON · 이 논문의 직접 비교 대상 · 제목은 참고문헌에 없다).

## (e) DEM-DFT 보고서에 쓸 거리 — W_ad 보고서 7 절 (Li 친화성 · 핵생성 · 집전체 계면 점착) · 연속체 · DEM 입력

⛔ 전부 **LLZO 계**다 (SEI 없음 · 치밀 산화물 SE). 0 MPa (S9 만 2 MPa) · 25 °C · 조건당 한 번이다. 값은 차수 · 경향으로만 쓴다. "봤다" = 이번에 그 그림을 직접 보고 읽었다는 뜻이다. 상세 표는 digest §11.

**7 절 — 핵생성 (§7 이 '할 수 없는 것' 으로 적은 것의 실측)**
1. **핵 과전압 η_nuc**: ≤ 50 mV (다결정 · 상한 · 골이 안 보임) · 200 mV (단결정 · **곡선 없음**) — p.2 · p.4 · `Fig. 1c` (봤다) · `Fig. S2` (봤다 · 그림은 SEM 뿐이다).
2. **핵 밀도 n(j)**: ≈7 / 21 / 51 / 61 ×10⁶ cm⁻² @ 50 / 100 / 500 / 1000 µA cm⁻² (16 µAh cm⁻²) · n ∝ j^≈0.7 이고 높은 전류에서 포화한다 (우리 산수) — p.4 · `Fig. 2e` (봤다). 같은 쌍에서 전류만 바꿔 **8.4 배**, 표면 상태만 바꿔 η_nuc 가 **4 배 넘게** 달라진다. W (0 K · 재료 쌍 하나) 로는 이 축을 못 잡는다는 §7 한계 문장의 실험 근거로 쓴다.
3. **핵 밀도는 척도에 따라 다르다**: 같은 50 µA cm⁻² 에서 Wang 2020 (확산 접합 Cu 박 · 펠렛 전체) 은 ≈10 mm⁻² = 10³ cm⁻² 다 (`wang2020_lithium_free_insitu_plating_llzo.md` §1). **10⁴ 배 차이**라서, 입력으로 옮길 때 CC 형태 · 분해능 · 계산 문턱 (A ≥ 0.02 µm²) 을 같이 적는다.
4. **핵 자리 = CC–SE 직접 접점** (기공 벽이 아니다) — p.6 · `Fig. 5d–g` (봤다) · Video S2 (봤다). DEM 접촉망의 접촉점 목록을 핵 자리 후보로 쓸 수 있다. Kazyak 2022 의 반대 관찰과 충돌한다.

**7 절 — Li 친화성**
5. 이 논문에 정량은 없다. 저자는 Cu 를 '비합금 · 저고용' 이라서 골랐다 (p.2). 다른 자리에선 "up to 14 at%" 라고 쓴다 (p.6). ⇒ §7 ③ (합금 구동력) 에서 **Cu 는 비합금 끝 기준점**이다. **§7-1 대상 표에 Cu(111) 을 '맨 집전체 기준' 으로 넣자고 제안한다** (Ag(111) · 흑연과 같은 잣대) — 계산 앵커는 같은 배치의 `cicvaric2026_li_nucleation_ni111_cu111_anode_free.md` (Cu(111) · Ni(111) Li 흡착 DFT + EIS).

**7 절 — 집전체 계면 점착**
6. 모드 (i) 위스커 = **CC–SE 계면이 Li 성장으로 열린다**. 무압 100 µA cm⁻² · ≈97 µAh cm⁻² 에서 틈이 ≈2 µm 까지 벌어진다 — p.6 · `Fig. 5g` (봤다). 국부 Li 는 ≈1.3–2 µm 로 균일 환산 0.47 µm 의 3–4 배다 (단면 창 효과일 수 있다 · 우리 산수). 이 논문에 W 도 G_c 도 없다. 같은 Cu/LLZO 계의 박리 점착 (G_c 부류 · 상한) 은 Wang 2020 digest 에 있다 → DEM 에서는 CC–SE 분리 기준이 모드 (i) 와 (ii) 를 가르는 변수가 된다. 우리 W (LPSCl–Ag(111) · LPSCl–흑연 · Ag–C · C–C) 에는 Cu 쌍이 없다 (값은 보고서 §2 · `db/properties/adhesion.json` — 여기 안 옮김).

**연속체 · DEM 입력**
7. **CC 관통 문턱**: 100 · 400 nm 는 관통하고 5 µm 막 · 10 µm 박은 관통하지 않는다 — p.7–8 · `Fig. S7` · `Fig. S8` · `Fig. 5` (모두 봤다). 관통 기하는 막 아래 부풂 ≈5 µm → Cu 껍질 원뿔 돌기 (폭 3–4 µm) → 꼭짓점 파열 순서다 (`Fig. S7` 봤다 · 400 nm · 20 µA cm⁻²). Ag–C · CC 를 연속체에서 막으로 넣을 때의 차수로 쓴다.
8. **성장 모드 지도**: 100 µA cm⁻² 아래는 위스커 + 막, 500 µA cm⁻² 위는 막 + 덴드라이트 (10 µm Cu 박 · 0 MPa) — p.8 · `Fig. 7` (봤다 · 도식). 경계는 50 / 100 / 500 세 점에서 그었다.
9. **SE 침투 신호**: 500 µA cm⁻² 에서 45–100 s 동안 전압이 요동하고 (골 ≈ −0.19 · ≈ −0.24 V) 그 뒤 회복한다 — `Fig. 6a,c` (봤다). 치밀 LLZO:Ta (> 96 %) 의 값이다.
10. **계면 저항 시간 변화**: R_int ≈630 → ≈105 Ω cm² (30 min · 100 µA cm⁻² · 2 MPa · 아직 하강 중) · R_bulk ≈220 · R_GB ≈60 Ω cm² — `Fig. S9b` (봤다 · figure-read). 본문의 "several 100 Ω cm² 수렴" 은 그림과 다르다.
11. **미세전극 겉보기 ASR** ≈1000 Ω cm² (η ≈100 mV @ 100 µA cm⁻² · 패치 면적 기준) — LLZO 퍼짐 저항은 0.5 mV 이하라 거의 전부 계면 몫이다 (우리 산수 · σ 를 10⁻⁴–10⁻³ S cm⁻¹ 로 가정 · `Fig. 1c` 봤다).
12. **투영 덮임률** ≈12–17 % (16 µAh cm⁻²) · ≈10 대 ≈18 % (60 µAh cm⁻² · 연속 대 펄스) (우리 산수). 핵 밀도와 덮임은 **다른 변수**로 둔다 — 핵을 8 배 늘려도 덮임은 거의 그대로다.
13. **펄스**: 2000 µA cm⁻² × ≈10 s 펄스 한 번에 N 이 +≈130×10⁶ cm⁻² 늘고, η_IR 이득은 ≈10 min 안에 상당 부분 돌아간다 — `Fig. 4` · `Fig. S3` (봤다). 런 안 비교만 단단하다.
14. **벗기기 CE 13 %** (덮임이 낮은 얇은 막 · 무압) — `Fig. S1` (봤다).
15. **LPSCl 로 옮길 때의 차이 (우리 DFT)**: 환원 가장자리 1.717 V (grand-potential) 때문에 Cu\|LPSCl 의 핵 전 구간은 SEI 형성 구간이다. §7 의 Li\|SE 젖음은 맨 LPSCl 면만이 아니라 **환원 산물 (Li₂S · Li₃P · LiCl) 면**도 후보로 둬야 운전 조건에 가깝다 (문헌의 Li\|SEI 상 접합일 대조는 `comparison_vs_ours.md` §E 의 [Wang22Res] 행).

## (f) 그림 · 동영상 크롭 요약

- `extract_figures.py --slug … --pdf <본문> <SI> --clean` → **16 장** (본문 Fig. 1–7 · SI Fig. S1–S9 · 표 0). `missing_labels` 는 [] (번호 공백 · 놓친 캡션 없음). 오탐 없음. `--audit` 경고 없음.
- **16 장 전부 직접 봤다.** 본문과 어긋난 것은 여섯 곳이다:
  - `Fig. 2e` — 평균 A 와 배수
  - `Fig. 3` · `Fig. S3` — 펄스 2000 µA cm⁻² (본문은 1000)
  - `Fig. S3` — η_nuc −30 mV 대 골 ≈0.2 V
  - `Fig. S9b` — several 100 대 ≈105 Ω cm²
  - `Fig. 4` — 같은 전하가 아니라 같은 시각에서 비교 · 대조의 A 가 E_WE > 0 V 인 1 min 부터 0 이 아니다
  - 교차 참조 둘 — p.8 "Figure 5" 는 Fig. 3 · "Figure S8c,d" 는 Fig. S9c,d

  자세한 것은 digest §10-②.
- 겉모양만의 흠 하나: `fig_S1.png` 맨 위에 SI 쪽 머리말 "Δ denotes equal contributions" 한 줄이 같이 잘렸다 (내용에는 영향 없음).
- **동영상**: movie1 은 2 초 간격 16 장 (`movie1_001`–`016` · 0–30 s), movie2 는 3 장 (`movie2_001`–`003` · 0 · 2 · 4 s). 2 초 간격으로는 끝 2.5 s 가 빠져서 **끝 프레임을 따로** 뽑아 같은 폴더에 `movie1_end.jpg` (≈32.4 s) · `movie2_end.jpg` (≈6.5 s) 로 넣었다 → jpg 21 장.
  - movie1 에서 본 장: 16 장 접촉 시트 (저해상 · 전부) + `001` · `006` · `007` · `end` 는 원본 크기
  - movie2 에서 본 장: `001` · `002` · `003` · `end` 전부 원본 크기
  - Video S2 mp4 에는 오디오 트랙이 있다 (ffprobe) — 듣지 않았다.
- ⚠ 동영상 프레임은 figures.json 에 없다 → 나중에 이 slug 를 `--clean` 으로 다시 추출하면 폴더째 지워진다 (`shutil.rmtree`). mp4 에서 같은 ffmpeg 명령으로 다시 만들 수 있다.
- **scratch 대조 (지시 반영)**: 처음에 본문 · SI 글자를 scratchpad 의 공용 이름 `main.txt` · `si.txt` 로 뽑아 읽었다. 지시를 받은 뒤 슬러그 폴더에 PDF 를 다시 뽑았고, 제목 · 저자 · 쪽 표시 `2203174 (11 of 11)` 과 digest 에 쓴 본문 수치 · 문구 66 개를 문자열로 대조했다 → **전부 일치**. 공용 `main.txt` 는 그 사이 누가 지워 두었고, 공용 `si.txt` 는 새로 뽑은 것과 바이트까지 같다. 처음 읽은 세 덩어리도 쪽 번호가 끊김 없이 이어져 있었다. 그 뒤 내 임시 파일은 전부 scratchpad `fuchs2023_cu_llzo_anode_free_li_growth_modes/` 아래로 옮겼다.

## (g) Jeff Sakamoto 저자 여부

**예.** 저자 7 명 중 5 번째 공저자다 (교신 저자는 아니다 — 교신 = Felix H. Richter · Jürgen Janek). 소속은 University of Michigan 재료공학과 + 기계공학과.
- digest 저자 줄에 **Jeff Sakamoto** 로 적었고 웹앱 `_paper_pis` 가 `['sakamoto']` 로 잡는 것을 확인했다.
- (a) 행 둘째 칸 맨 앞에 `🏷 **Jeff Sakamoto 공저** · ` 를 달았다.
- 이 논문 참고문헌의 Sakamoto 공저 편: [10] Sharafi 2017 · [13] Taylor 2018 · [14] Kazyak 2020 · [15] Wang 2020 · [25] Kazyak 2022 · [30] Zhu 2019 · [31] Connell 2020 · [47] Kinzer 2021. 이 중 Sharafi 2017 · Kazyak 2020 · Wang 2020 은 이 배치에 있고, Kazyak 2022 는 (d) 4 번이다.
