# 끝 보고 — yang2021_flat_li_stripping_lithiophilic_interface_design (2026-11-24 · litdb-curator)

slug 는 그대로다 (첫 저자 Chi-Ta Yang 확인 · 저자 2 명: Chi-Ta Yang · Yue Qi\*).

쓴 파일: `litdb/papers/yang2021_flat_li_stripping_lithiophilic_interface_design.md` (≈ 556 줄 · 표 18 개 칸수 검사 0 건) · `litdb/figures/yang2021_flat_li_stripping_lithiophilic_interface_design/` (크롭 20 장 + figures.json) · 이 보고 파일. `litdb/figures/_sources.json` 은 추출 도구가 다시 썼다 (손 안 댐).
공유 파일 · git 은 안 건드렸다. 메인 체크포인트 커밋 (4739c5a7 · 55c16687) 에 digest 가 이미 들어갔고, 그 뒤 digest 에 한 줄 (§4e Seymour 배치 #1 가리킴) 을 더했다 — 다음 체크포인트가 가져가면 된다.
`build_index.py --check`: 이 slug 는 "어느 인덱스에도 없음 [dft]" · "comparison_vs_ours.md 미편입" 두 곳에만 뜬다 (아래 (a) (b) 를 넣으면 풀린다). 나머지 ⚠ 건수는 원래 있던 것.
웹앱 확인 (읽기만): `_paper_pis` → `[]` (Sakamoto 배지 오탐 없음) · 원소 태그 C · F · Li · N · O · P · 기법 태그 adhesion · dft · functional · kpoint · neb · pseudo · 그림 주석 20 키 전부 파싱 · `webapp/tests/test_v3_literature.py` 20 passed · `test_v3_markdown.py` + `test_v3_surfaces.py` 31 passed. (literature 시험이 첫 실행에서 '완성 digest 수' 단언으로 1 번 실패했는데, 병렬 에이전트가 그 사이에 digest 를 더한 경쟁이었다 — 바로 다시 돌려 통과.)

## (a) INDEX.md 행

넣을 절 (권고): **`## 🧲 계면 점착 · 인터레이어 트랙`** 표 끝 — W_ad 보고서 §7 (Li 친화성) 의 서술 원전이라서. 이 절은 DEM 쪽 트랙이라 `INDEX_DEM.md` (자동 생성) 에도 뜬다. ⚠ 절 머리 조건 ('LPSCl 이 한쪽 면' · 'G_c 부류') 에 안 맞으므로 절 머리 예외 줄을 하나 더하는 것을 권한다 (giovannetti2008 · wang2015 예외와 같은 꼴):
```
> ⛔ 예외 (2026-11-24): `yang2021_flat_li_stripping_lithiophilic_interface_design` 도 G_c 가 아니라 **DFT(PBE · vdW 없음 · Γ 만) W_sep** 다 — G_c 값과도, 우리 DFT W (PBE+D3(BJ)) 와도 **같은 줄 금지**. 계면도 LPSCl 이 아니라 Li 금속 \| SEI (Li₂O · LiF · LiPON · Li₂CO₃). Young–Dupré 친/소 Li · 계면 공공 지형 · KMC 의 **방법 · 서술 원전**으로만 쓴다.
```
대안 절: `## ✅ Digest 완료 (paper-level)` 본문 표 (build_index 분류는 [dft]).

행 (3 칸 · slug | 논문 | 축):
```
| `papers/yang2021_flat_li_stripping_lithiophilic_interface_design.md` **(본문 10 pp + SI 10 pp · 크롭 20장 (도구 18 + 손 크롭 2 `Fig. S2` · `Table S3` · 다시 자름 2 `Fig. S6` · `Fig. S7`) 중 그림 13장 실독 (본문 5/5 · SI 8/9 — `Fig. S1` 만 쪽 렌더) · 표 6장 PDF 글자층 · 2026-11-24)** | **[외부·DFT+KMC·계산 전용 · ⭐⭐⭐ 스트리핑 공극의 원자 기전 원전 · W_ad 보고서 §7 (Young–Dupré 친/소 Li) 의 서술 원전 · ⛔ G_c 아님 (DFT W_sep · PBE · vdW 없음 · Γ 만) — 우리 DFT W 와도 같은 줄 금지 · ⛔ 'Yang 0.7 J m⁻² 문턱' 은 이 논문이 아님 (형제 `yang2021_atomistic_li_stripping_plating_interface_md` = M. Yang · Mo)]** ✅ **Chi-Ta Yang**/**Yue Qi\*** (Michigan State → Brown), "**Maintaining a Flat Li Surface during the Li Stripping Process via Interface Design**" — ***Chem. Mater.* 33, 2814–2823 (2021)**, DOI `10.1021/acs.chemmater.0c04814`. VASP PAW-PBE 700 eV · Γ · Li(001)/Li₂O(110) · Li(001)/LiF(001) 층별 공공 형성 (bulk 0.49 eV · Li₂O 결합 L1 0.80 > bulk = 반발 · LiF L1 0.16 / 0.07 < bulk = 포획) + NEB (계면층 진입 forward 장벽 Li₂O 0.156 / 0.132 vs LiF 0.331 / 0.561 eV) → BKL KMC (40 Å Li · ν₀ 10¹³ s⁻¹ 가정 · 10⁵ 스텝 · 궤적 1 개): Li₂O 공공은 84 ps 안에 bulk 로 (계면 16 %) vs LiF 는 1.6 µs 동안 계면에 갇혀 공극 · **J_C 10¹–10² vs 10⁻⁵–10⁻⁴ A cm⁻²** · Test 1 (forward 장벽 → 0.05 eV) 이 공극을 메움 = 손잡이는 W 가 아니라 진입 장벽. W_sep **Li₂O 1.11 · LiPON 0.64 · Li₂CO₃ 0.30 · LiF 0.28 J m⁻²** · θ ∼0° / 108.7° (γ_Li 미기재 · LiF 쌍 역산 ≈ 0.41 J m⁻²) · 순위 Li₂O > LiPON > Li₂CO₃ > LiF (LiPON · Li₂CO₃ 는 KMC 없이 W · 전하 그림만). ⚠ J_C 는 SEI 수송 없는 상한 · 같은 벗겨낸 양 비교 아님 (3–42 원자 = 한 층의 1–16 %) · 슬랩 두께 · k 수렴 미입증 (`Fig. S2` 15 층에서도 +10–20 %) · LiF 대칭 / 비대칭 셀 차 ≤ 0.17 eV · `Table S5` LiF 두 공공 기준 불일치 · `Fig. S5b` 피팅 vs `Table 1` 어긋남 · 실험 0 | 점착 트랙 (W_ad 보고서 §7 Li 친화성 · Young–Dupré · 공극 억제 기전) · Li 금속 \| SEI 계면 공공 지형 견본 · anode-free 스트리핑 |
```
- 🏷 Jeff Sakamoto 표지는 **달지 않는다** ((g)).
- 🎤 talk 역링크 없음 — `litdb/talks/*.md` 인입 대기열 어디에도 이 논문이 없다 (grep 확인).

## (b) comparison_vs_ours.md

넣는다 (build_index 미편입 해소용 — slug 경로가 Reference key 에 있어야 한다). 물성 4축 표 (A–D) 에는 넣지 않는다 (우리 Li 금속 쌍 값 0 건 · 축이 E).

① `## 📑 Reference key` 표 (4 칸):
```
| **[YangQi21]** ⭐⭐ **스트리핑 공극의 원자 기전 원전 — 계면 공공 지형 (DFT) + KMC · W_sep → Young–Dupré θ → 친/소 Li** · ⛔ **J_C (10¹–10² vs 10⁻⁵–10⁻⁴ A cm⁻²) 를 실험 CCD 와 같은 양으로 인용 금지** · ⛔ **'Yang 0.7 J m⁻² 문턱' 과 혼동 금지 (그건 M. Yang · Mo 2021 *Adv. Mater.* — `[Wang22Res]` ref 29)** | **Chi-Ta Yang**/**Yue Qi\*** (Michigan State → Brown) 2021 ***Chem. Mater.* 33, 2814–2823** (DOI 10.1021/acs.chemmater.0c04814) — "Maintaining a Flat Li Surface during the Li Stripping Process via Interface Design" | ✅ `papers/yang2021_flat_li_stripping_lithiophilic_interface_design.md` (2026-11-24 · 크롭 20 장 중 그림 13 장 실독 · 표 6 장 PDF 글자층) | DFT (VASP PAW-PBE · Γ · vdW 없음) + KMC · 계산 전용 |
```
② `## E. 환원 / 음극(Li 금속) 계면` 표 맨 위 (4 칸 — 주장 | 출처 | 우리 | 일치):
```
| **🆕 (2026-11-24) 스트리핑 공극은 계면이 공공을 '밀어내나 · 가두나' 로 갈린다 — 친Li Li/Li₂O (W_sep 1.11 J m⁻² · θ ∼0°) 는 계면 결합 Li 의 공공 형성 0.80 > bulk 0.49 eV · 계면층 진입 장벽 0.156 / 0.132 eV 로 공공이 84 ps 안에 bulk 로 흩어지고 (계면 16 %), 소Li Li/LiF (0.28 · 108.7°) 는 0.16 / 0.07 < 0.49 eV · 진입 장벽 0.331 / 0.561 eV 로 공공이 계면에 갇혀 공극 → KMC J_C 10¹–10² vs 10⁻⁵–10⁻⁴ A cm⁻² · 공극을 메우는 손잡이는 W 가 아니라 forward 장벽 ΔE₂→₁ (Test 1 → 0.05 eV)** · 저자 연장: Li/LPSCl ≈ Li/Li₂S/LPSCl ≈ LiF 쪽 (계산 없음 · ref 33) | **[YangQi21]** `Fig. 1c,d` · `Fig. 2` · `Fig. 3` · `Fig. S9` · `Table 1` · `Table S4` (VASP PAW-PBE · 700 eV · **Γ 만** · vdW 없음 · Li(001) 정합 변형 · KMC BKL · ν₀ 10¹³ s⁻¹ 가정 · 10⁵ 스텝 · 궤적 1 개) | **없다.** 우리 Li 금속 쌍 W · 계면 공공 지형 · KMC 0 건 (W_ad 보고서 §7 은 제안 단계 · 값 위치 `db/properties/wad_*` · `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` §2). SEI 트랙 NEB 는 결정 (계면 아님 · `db/properties/sei_neb.json`) | 🟡 **대조 불가 (우리 값 없음) + 🔑 프레임.** W → 공극 사슬은 KMC 2 개 계의 상관 · J_C 는 단분자층 이하 · 고정 스텝 창 (같은 벗겨낸 양 비교 아님) → 순서 지표로만. `[Wang22Res]` 자기 γ_Li 로 우리 환산하면 Li\|LiCl θ ≈ 118–154° · Li\|Li₂S ≈ 85–89° (경계) · Li\|Li₃P ≈ 62° → 'LiCl 많은 SEI 는 스트리핑 공극 쪽에서 불리할 수 있다' 는 가설 (검증 0 · §E 머리 'Cl-rich 유불리 충돌' 축). ⛔ θ 를 실험 용융 Li 접촉각과 같은 양으로 쓰지 않는다 |
```
③ (선택) `comparison_vs_ours_DEM.md` §I 다음 번호에:
```
### I-n. `yang2021_flat_li_stripping_lithiophilic_interface_design` — (인접 축 · DFT W_sep · G_c 아님) **Young–Dupré 친/소 Li 의 원자 기전 원전 — W 가 아니라 계면층 진입 장벽이 공극을 메운다**

> **무엇을 주나.** VASP PAW-PBE (vdW 없음 · Γ) Li(001)/Li₂O(110) · Li(001)/LiF(001) 층별 공공 형성 + NEB → KMC. W_sep Li₂O 1.11 · LiPON 0.64 · Li₂CO₃ 0.30 · LiF 0.28 J m⁻² · θ ∼0° / 108.7° (γ_Li 미기재 · 역산 ≈ 0.41).
> **★ 우리 축에 닿는 곳.** ① W 보고서 §7 Young–Dupré 규칙 (θ < 90° 친Li · W ≥ 2γ_Li 완전 젖음) 의 외부 사례 — 단 논문은 90° 문턱을 명시하지 않는다 · ② γ_Li 를 같은 셀 · 같은 변형으로 적어야 하는 이유 (안 적어서 역산 · `[Wang22Res]` 0.46 과 10 % 차 → θ ≈ 90° 판정이 뒤집힘) · ③ 공극 모델 입력은 θ 가 아니라 계면층별 장벽 (`Fig. S9` Test 1).
> **⛔ 인용 금지 / 한정어.** DFT W_sep 를 G_c (I-1 · I-3) 나 우리 PBE+D3 W 와 같은 줄에 두지 않는다 · J_C 는 SEI 수송 없는 KMC 상한 · Li₂O 친Li 는 (110) 면 한정 (`[Wang22Res]` (111) 0.32–0.36 J m⁻² 는 소Li 쪽).
```

## (c) pdf_map.tsv

**불필요** — 자동 매칭이 된다 (`extract_figures.py --inbox --only yang2021` → `[제목 100%]` 본문 `yang2021_flat_li_stripping_main.pdf` · SI `yang2021_flat_li_stripping_SI.pdf`). 형제 `yang2021mo_li_strip_plate_md_*` 와 섞이지 않았다.

## (d) 추가로 먹일 만한 논문 (8 편)

⚠ 이 논문 (2021) 의 참고문헌에서 골랐다 — 2024–2026 후속은 PDF 로 확인한 것이 없다 (litdb 안에서 이 논문을 인용한 편은 `[Wang22Res]` (2022) 와 같은 배치의 형제 digest 뿐). 최근 편은 **오늘 배치에 이미 있다**: #12 `lu2026_li_ag_interface_thermodynamics_kinetics` · #14–15 Metzler Ag–C (2025 · 2026) · #17 `cicvaric2026…` · #18 Chatterjee diffuse interface · #13 Sandoval 2025. 같은 배치의 #1 Seymour & Aguadero 2021 (W_adh > 2γ 판정식) · #4 Sharafi 2017 (ref 55) 도 이미 들어 있어 아래에서 뺐다. 아래 8 편 모두 litdb 카드 없음 · 오늘 inbox 에도 없음 (파일명 grep · 2026-11-24). 서지는 이 PDF 의 참고문헌 목록 그대로.

| # | 서지 (이 논문 ref 번호) | 왜 | litdb |
|---|---|---|---|
| 1 | J. Kasemchainan, S. Zekoll, D. Spencer Jolly, Z. Ning, G. O. Hartley, J. Marrow, P. G. Bruce, "Critical Stripping Current Leads to Dendrite Formation on Plating in Lithium Anode Solid Electrolyte Cells," *Nat. Mater.* 18 (2019) 1105–1111 (ref 14) | **Li/Li₆PS₅Cl** 임계 스트리핑 전류 (2×10⁻⁴ · 1×10⁻³ A cm⁻² at 3 · 7 MPa) · 방전 중 공극 → 다음 도금 덴드라이트 — 우리 계 그대로 | 카드 없음 (10 개 digest 가 인용만) |
| 2 | C.-T. Yang, Y.-X. Lin, B. Li, X. Xiao, Y. Qi, "The Bonding Nature and Adhesion of Polyacrylic Acid Coating on Li-Metal for Li Dendrite Prevention," *ACS Appl. Mater. Interfaces* 12 (2020) 51007–51015 (ref 35) | 이 논문의 계면 모델 · **W_sep 정의 · γ_Li 의 출처** (이 PDF 에 없는 것) — DFT 점착 계산법 | 카드 없음 |
| 3 | Z. Liu, Y. Qi, Y. X. Lin, L. Chen, P. Lu, L. Q. Chen, "Interfacial Study on Solid Electrolyte Interphase at Li Metal Anode: Implication for Li Dendrite Growth," *J. Electrochem. Soc.* 163 (2016) A592–A598 (ref 32) | Li/LiF · Li/Li₂O · Li/Li₂CO₃ 계면 점착 · 방위 선택 근거 · 정합 셀 (< 5 %) — DFT 점착 계산법 | 카드 없음 |
| 4 | N. D. Lepley, N. A. W. Holzwarth, "Modeling Interfaces between Solids: Application to Li Battery Materials," *Phys. Rev. B* 92 (2015) 214201 (ref 33) | **Li/Li₂S** (LPSCl 분해 산물) 계면 결합 — 저자가 'Li/LPSCl ≈ LiF 쪽' 이라 한 유일한 근거 · Li 금속 \| 기판 점착 | 카드 없음 (7 개 digest 가 인용만) |
| 5 | Y. Qi, L. G. Hector, "Adhesion and Adhesive Transfer at Aluminum/Diamond Interfaces: A First-Principles Study," *Phys. Rev. B* 69 (2004) 235401 (ref 58) | W_sep · 대칭 셀 · coherent interface 근사의 **방법 원전** (우리 고정 기하 W_sep 과 정의 대조용) | 카드 없음 |
| 6 | F. Guo, C. Wu, H. Chen, F. Zhong, X. Ai, H. Yang, J. Qian, "Dendrite-Free Lithium Deposition by Coating a Lithiophilic Heterogeneous Metal Layer on Lithium Metal Anode," *Energy Storage Mater.* 24 (2020) 635–643 (ref 56) | **Ag · Au 친Li 금속층** — 저자가 '스트리핑에도 통할 것이라 믿는다' 고만 한 근거 (Ag 의 Li 친화성) | 카드 없음 |
| 7 | T. Krauskopf, B. Mogwitz, C. Rosenbach, W. G. Zeier, J. Janek, "Diffusion Limitation of Lithium Metal and Li–Mg Alloy Anodes on LLZO Type Solid Electrolytes as a Function of Temperature and Pressure," *Adv. Energy Mater.* 9 (2019) 1902568 (ref 25) | 합금 음극 · 방전 중 공극의 확산 한계 — Ag–C 층의 Li–Ag 합금과 같은 축 | 카드 없음 |
| 8 | J. A. Lewis, F. J. Q. Cortes, Y. Liu, … M. T. McDowell, "Linking Void and Interphase Evolution to Electrochemistry in Solid-State Batteries Using Operando X-ray Tomography," *Nat. Mater.* 20 (2021) 503 (ref 23) | 방전 중 공극의 operando 실측 — KMC 공극 그림의 실험 짝 | 카드 없음 |

(덜 급함: Y. Li, Y. Qi, *Energy Environ. Sci.* 12 (2019) 1286–1295 (ref 52) — Li/Li₂CO₃ 공공 응집 −0.32 eV.)

## (e) DEM-DFT 보고서 (W_ad 보고서 §7) 에 쓸 거리

쪽 = 저널 쪽 (PDF 쪽). "실독" = 크롭 PNG 를 원 크기로 직접 봤다.

| # | §7 의 어디에 | 쓸 점 | 출처 · 봤나 |
|---|---|---|---|
| 1 | Li 친화성 정의 · Young–Dupré | cos θ = W_sep/γ_Li − 1 로 DFT W 를 θ 로 바꾸고 'lithiophilic (θ ∼0°, Li/Li₂O 1.11 J m⁻²) vs lithiophobic (θ = 108.7°, Li/LiF 0.28 J m⁻²)' 로 부른 계산 원전 — 우리 문장 *"θ < 90° 면 친Li"* 의 외부 사례. ⚠ 논문은 **90° 문턱을 명시하지 않는다** (식에서 나오는 경계) | p. 2819 (PDF p. 6) 본문 — 글자층 (그림 아님) |
| 2 | W 와 2γ_Li 비교 | 논문은 γ_Li 값을 **안 적는다** → LiF 쌍 역산 γ_Li ≈ 0.412 J m⁻² (2γ ≈ 0.82) · Li₂O 1.11 > 2γ → θ = 0 으로 잘림 · LiPON 0.64 (W/2γ 0.78 · θ ≈ 56°) · Li₂CO₃ 0.30 (≈ 106°) — 우리 환산. 같은 Li(100) 면 `[Wang22Res]` 는 γ_Li 0.46 → 10 % 차 = **θ ≈ 90° 경계 판정이 뒤집히는 크기** → 우리 규칙 *"γ_Li 도 같은 방법 · 같은 Li 면으로"* 의 외부 근거 | p. 2819 본문 + 우리 환산 (digest §3h · §7b) |
| 3 | 공극 억제 기전 (반발 / 포획) | 계면 공공 형성에너지 vs bulk (0.49 eV): Li₂O 결합 L1 0.80 (반발) · LiF L1 0.16 / 0.07 (포획) · ⚠ Li₂O 비결합 L1 (25 %) 0.38 도 포획 쪽 | `Fig. 1c,d` p. 2815 — **실독** · `Table S1` · `Table S2` SI p. 3–4 — 글자층 |
| 4 | 공극 억제 기전 (동역학) | KMC: Li₂O 공공 84 ps 안에 bulk 로 (계면 16 %) vs LiF 1.6 µs 동안 계면에 갇혀 공극 | `Fig. 2` p. 2816 — **실독** · `Fig. S6` SI p. 6 — **실독** |
| 5 | 공극 억제 기전 (손잡이) | **공극을 메우는 것은 W 가 아니라 forward 장벽 ΔE₂→₁** (Test 1: 0.331 / 0.561 → 0.05 eV 에 공극 해소 · Test 2: 역방향 0 → 0.6 eV 는 효과 작음) → §7 의 *"W 가 크면 공극을 막는다"* 는 '2 개 계 KMC 에서 순서가 같았다' 수준으로 | `Fig. S9` SI p. 9 — **실독** · `Table S4` — 글자층 · `Table 1` p. 2816 — 글자층 |
| 6 | 임계 전류 (쓰려면 단서와 같이) | J_C 10¹–10² (Li₂O) vs 10⁻⁵–10⁻⁴ A cm⁻² (LiF) — SEI 수송 · 전하 전달 · 압력 없는 상한 · 고정 10⁵ 스텝 · 벗겨낸 3–42 원자 (한 층 1–16 %) | `Fig. 3` p. 2817 · `Fig. S7` · `Fig. S8` SI p. 7–8 — **실독** |
| 7 | 전자 기원 | Li₂O(110) 의 Li 2 개 모자란 저배위 O → 계면 전자 축적 큼 → 친Li · 평면 Δρ 최대 축적 figure-read ≈ 6.8 / 5.4 / 3.1 / 2.3 ×10⁻³ e Å⁻³ (Li₂O · LiPON · Li₂CO₃ · LiF) — 정성 (적분 전하 없음) → 우리 Ag–C · LPSCl 쌍에 같은 평면 Δρ 를 낼 수 있다 | `Fig. 4` p. 2819 — **실독** |
| 8 | 그들의 DFT 설정 (부록 A 대조) | VASP PAW-PBE · **vdW 없음** · 700 eV · **Γ 만** · Gaussian 0.1 eV · 10⁻⁶ eV · 0.02 eV/Å · 대칭 셀 (Li 15 층 + SEI 5 / 4 층 · 진공 24 Å · P-1) / 비대칭 셀 (Li 9 층 · 바깥 3 층 고정 · 진공 20 Å · NEB 용) · 정합 4×4 vs 3×4 / 5×5 (< 5 %, Li 를 늘림) · 면내 13.86×13.07 · 14.32×14.32 Å · **W_sep 정의식 · γ_Li 는 이 PDF 에 없음** (ref 35 · 58) · 슬랩 두께 수렴은 그림으로 안 보임 (15 층에서 +10–20 %) | Methods p. 2820 — 글자층 · `Fig. S2` SI p. 2 — **실독** (손 크롭) · `Fig. S1` SI p. 1 — **쪽 렌더만 (크롭 안 봄)** |
| 9 | 공극 모델 입력 | KMC 는 θ 를 입력으로 안 쓰고 계면층별 장벽 지도를 쓴다 (지수 피팅 ΔE(x) = a·exp(−bx) + c) → §7 *"Li–벽 접촉각 같은 입력"* 문장에 'θ 는 순위 지표 · 동역학에는 장벽 지도' 단서 | `Fig. 5` p. 2820 — **실독** · `Fig. S5` SI p. 5 — **실독** (x = 0 부근 2 배 확대) |
| 10 | Ag · 합금 | Ag · Au 친Li 층이 스트리핑 공극도 줄일 것이라 '믿는다' (계산 없음 · ref 56) · 합금 음극 지지 (ref 25) → §7 '합금 · 반응 구동력' 항과 같은 결론 (spencerjolly2023: Ag 는 운전 중 Li–Ag 합금) | p. 2819 마지막 문단 — 글자층 |
| 11 | '할 수 없는 것' 단서의 근거 | 이 논문은 0 K DFT θ 를 실험의 'lithiophobic' (ref 55 · 용융 Li 젖음) 과 같은 말로 잇는다 → 우리 단서 *"녹은 Li 접촉각과 같은 양이 아니다"* 의 반례 · 'Li₂O 친Li' 는 (110) 면 한정 (`[Wang22Res]` (111) 은 소Li 쪽) | p. 2819 본문 — 글자층 |
| 12 | LPSCl 쪽 연결 | 저자: Li/LPSCl ≈ Li/Li₂S/LPSCl · Li/Li₂S 결합은 LiF 에 가깝다 (계산 없음 · ref 33) · Kasemchainan J_C 와 '비슷한 자릿수' (실제로 1–2 자릿수 차) | p. 2818 본문 — 글자층 |

⚠ 공유 보고서 (docs/collab HTML) 에 옮길 때는 CLAUDE.md 규칙대로 내부 사정 (점검 단계 · 회신 차수 등) 은 빼고, 새 판이면 웹앱 `COLLAB_REPORTS` 표도 같이 고친다 — 메인 세션 몫.

## (f) 그림 크롭 요약

- **20 장** = 그림 14 (본문 `Fig. 1`–`Fig. 5` · SI `Fig. S1`–`Fig. S9`) + 표 6 (`Table 1` · `Table S1`–`Table S5`). 도구 자동 18 장.
- 도구가 놓친 것 2 장 → **손 크롭 (manual_crop)**: `fig_S2.png` (SI p. 2 — 벡터 막대그래프인데 도구가 '그래픽 없음 (img0/draw0)' 으로 건너뜀) · `tab_S3.png` (SI p. 6 — 표 제목이 `Fig. S6` 캡션과 한 글자 블록이라 안 뽑힘). 도구의 `⚠ 번호 공백` 2 건 (fS2 · tS3) 은 둘 다 `figures.json` `missing_labels[].resolved` 로 닫았다.
- 도구 크롭을 고친 것 2 장 → **recrop** (`auto_bbox` 보존): `fig_S7.png` (자동 크롭이 캡션 위 53 pt 띠만 잡음 → 래스터 6 장 + 패널 라벨 전체) · `fig_S6.png` (x 축 제목 'KMC steps' 잘림).
- 오탐 0 · 빈 영역 0. 본 그림 13 장 (`Fig. S1` 만 쪽 렌더) · 표 6 장은 PDF 글자층에서 옮김 (`figures.json` `viewed` · `viewed_how` 에 기록).
- ⚠ 병렬 운영 메모: scratchpad 가 다른 에이전트와 공유돼서 내 `main.txt` · `si.txt` 가 다른 논문 (Fuchs 2023 · 배치 #10) 글자로 덮어써졌다 — 덮어쓰기 전에 읽은 본문이 Yang & Qi 원문인지 쪽 렌더와 대조했고, 이후 추출은 전용 하위 폴더에서 다시 했다. 다음 배치에서는 에이전트마다 scratchpad 하위 폴더를 slug 이름으로 쓰게 하는 것을 권한다.

## (g) Jeff Sakamoto 저자 여부

**아니다.** 저자는 Chi-Ta Yang · Yue Qi 두 사람뿐이다. Sakamoto 는 참고문헌 ref 55 (Sharafi et al., *Chem. Mater.* 29, 7961 (2017) — 같은 배치 #4) 의 공저자로만 나온다. digest 머리말에는 그 이름을 풀네임으로 쓰지 않아 웹앱 배지 오탐이 없다 (`_paper_pis` → `[]` 확인). INDEX 행에 🏷 를 달지 않는다.
