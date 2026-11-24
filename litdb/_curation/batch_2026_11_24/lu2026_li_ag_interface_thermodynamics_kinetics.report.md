# 끝 보고 — lu2026_li_ag_interface_thermodynamics_kinetics (배치 2026-11-24 · #12)

- digest: `litdb/papers/lu2026_li_ag_interface_thermodynamics_kinetics.md` (새 파일 · 한국어 standalone · §0–§12)
- 그림: `litdb/figures/lu2026_li_ag_interface_thermodynamics_kinetics/` (fig_1–4 · tab_1–3 · figures.json)
- 도구가 다시 쓴 공유 색인: `litdb/figures/_sources.json` (추출 도구 자동 · 손대지 않음)
- 그 밖의 파일은 안 건드렸다 · git 작업 없음 · `build_index.py --check` 만 (이 digest 는 "어느 인덱스에도 없음 [dft]" 으로 뜬다 — 아래 (a) 를 넣으면 풀린다)
- 웹앱 확인 (읽기만): `paper_figure_notes` 7 개 (f1–f4 · t1–t3) 정상 · elements Li·Ag·Mg · methods DFT·MLIP·NEB 링크 확인 · `paper_pis` = [] (Sakamoto 배지 없음 — 맞다)

⚠ **메인에 알릴 함정 하나** — 처음 저자 줄에 *"(Jeff Sakamoto 는 저자가 아니다 …)"* 라고 썼더니 웹앱 `paper_pis` 가 **sakamoto 배지를 붙였다** (머리말 창의 이름 문자열만 본다). 문구를 *"사카모토 교수는 참고문헌 [8] 인용에만"* 으로 바꿔 풀었다. 같은 배치의 다른 비-Sakamoto 편이 '아니다' 를 같은 꼴로 적었는지 `data.paper_pis(slug)` 로 한 번 훑어 보면 좋다.

---

## (a) `litdb/INDEX.md` 에 넣을 행

**절**: `## 🧲 계면 점착 · 인터레이어 트랙 — LPSCl 이 한쪽 면인 계면/벌크 역학의 실측 앵커 (2026-09-23 신설)` (표 끝에 한 행)

그 절 머리 인용문 ⛔ 예외 목록에 한 줄 (giovannetti2008 · wang2015 꼴):

```
> ⛔ 예외 (2026-11-24): `lu2026_li_ag_interface_thermodynamics_kinetics` 도 G_c 가 아니라 **DFT(PBE, vdW 없음) · 범용 MLIP(MACE-MP-0) W_ad** 다 — G_c 값과도, 우리 DFT W(PBE+D3 · 강체 분리 W_sep) 와도 **같은 줄 금지**. 방법 비교 · Li 친화성 (7 절) 앵커로만 쓴다.
```

행:

```
| `papers/lu2026_li_ag_interface_thermodynamics_kinetics.md` **(본문 12 pp · SI 없음 · 크롭 7장 (그림 4 + 표 3) · 그림 4장 전부 실독 · `Fig. 4` 3배 확대 판독)** | **[외부·DFT+MLIP·⭐⭐⭐ Li 금속\|Ag 계면 W_ad 의 DFT·MLIP 원전 · ⚠ PREPRINT 미심사 · ⛔ G_c 아님]** ✅ **Grace M. Lu**/**Dallas R. Trinkle\*** (UIUC MatSE · UC Irvine MAE), "**Thermodynamics and kinetics of lithium at the silver-lithium battery interface**" — ***arXiv* 2602.11430v1 (2026-02-11)** (자료 MDF `10.18126/gfpd-mm33`). VASP-PAW **PBE (vdW 없음)** · 500 eV · Γ 8×8×1 · MP 0.1 · 힘 0.005 eV/Å + **MACE-MP-0 medium (L = 1 · 미세조정 없음)**. Ag(111)·(100) 위 Li 6 방위 (BCC KS·NW·Pitsch·Bain 반정합 + FCC(111)·(100) 정합 · Li 3.77 % 2축 압축 · Ag 4.17 Å · Ag 24 Å 중 12 Å 고정 · registry = 5×5×5 재귀 격자 탐색 최저). **W_ad (eV/Å², MACE)**: FCC(111) 0.0919 · KS 0.0916 · NW 0.0898 · Pitsch = FCC(100) 0.0455 · Bain 0.0170 · **DFT: FCC(111) 0.093 · FCC(100) 0.106 → (100) 에서 MACE = DFT 의 43 % · 면 순서 뒤집힘** (`Table 3` · p.4). BCC 로 만든 계면도 조밀 충전으로 재구성 (KS → HCP 꼴 · Pitsch/Bain → FCC(100) 꼴). 계면 Li 공공 형성 +102 (111) / +227 meV (100) · 한 층 안쪽은 낮다 (`Fig. 3`). (111) 첫 홉 (Li 가 Ag 자리 공공으로) **0.029 (MACE) / 0.019 eV (DFT)** · ΔE figure-read ≈ −0.46 eV · Li 2·3 층 0.136·0.124 vs 벌크 FCC 0.11 eV (홉 수 검산: 홉당 1.7–2.8 배 · ps 규모 — '막힌다' 는 과장). ⚠ `Table 2` 단위 'eV/Å²' 는 J/m² 크기 (오기로 읽음) · 편집 메모 잔존 · Seymour & Aguadero 참고문헌 누락 | 점착 트랙 W_ad 보고서 7 절 (Li 친화성) — Li\|Ag W 첫 문헌 앵커 · Young–Dupré 입력 (논문 숫자로 DFT θ = 0° · MACE (100) θ ≈ 59–75°) · Ag 합금 구동력 (첫 홉 ΔE) · 범용 MLIP 계면 W 의 면 의존 오차 반례 (우리 같은-기하 작은 모델 확인의 근거) |
```

(선택) `## 🤖 MLIP 방법론 — 우리 UMA 스택을 재는 축` 에 짧은 교차 행:

```
| `papers/lu2026_li_ag_interface_thermodynamics_kinetics.md` | **[외부·DFT+MLIP·교차 — 본 행은 🧲 점착 절]** Lu & Trinkle *arXiv* 2602.11430 (2026) — MACE-MP-0 (medium) 가 표면 에너지 ≤ 9 % · 벌크 공공 ≤ 0.05 eV 벤치마크를 통과하고도 Li\|Ag(100) W_ad 를 DFT 의 43 % 로 줬다 ((111) 은 99 %). 벌크·표면 통과 ≠ 계면 W 정확 · 오차 부호 비보편 ([Agarwal26AD] 은 평균 과대) | MLIP 계면 검증 축 |
```

---

## (b) `comparison_vs_ours.md` 에 넣을 줄 (방법 비교 · 우리 W 값 없음)

물성 4축 (A–D) 에는 **넣지 않는다** (계가 순수 금속 Li\|Ag · argyrodite 0). 넣을 곳 둘:

### b-1. `📑 Reference key` 표에 한 행

```
| **[Lu26LiAg]** 🔧🔴 **Li 금속\|Ag 계면 W_ad — DFT (PBE) vs 범용 MLIP (MACE-MP-0) 의 면 의존 오차 반례** · ⛔ **미심사 프리프린트 (arXiv)** · ⛔ 순수 Li\|순수 Ag 금속 계면 · argyrodite 0 — A–D 물성 4축에 행을 만들지 않는다 (§J-88 에만) | **Grace M. Lu**/**Dallas R. Trinkle\*** (UIUC MatSE · UC Irvine MAE, **외부**) 2026 *arXiv* 2602.11430v1 (게시 2026-02-11 · 자료 MDF 10.18126/gfpd-mm33) — "Thermodynamics and kinetics of lithium at the silver-lithium battery interface" | ✅ `papers/lu2026_li_ag_interface_thermodynamics_kinetics.md` — 판정은 **§J-88** | DFT (VASP-PBE · vdW 없음) + uMLIP (MACE-MP-0 medium · 미세조정 없음) · 0 K 정적 · 실험 0 · SI 없음 |
```

### b-2. §J 끝에 블록 (지금 최대 J-87 → **J-88** 제안 · 병렬 편과 번호가 겹치면 메인이 정한다)

```
### J-88. 🔧🔴 **방법 원전 — [Lu26LiAg] Li 금속|Ag 계면 W_ad: 범용 MLIP 이 벌크·표면 벤치마크를 통과하고도 계면 W 를 면마다 다르게 틀린다 (*arXiv* 2026 · 미심사)** (2026-11-24 신설)

> ⛔ A–D 물성 4축에 넣지 않는다 (순수 금속 Li|Ag). ⛔ 우리 W 값과 같은 줄에 놓지 않는다 — 보고량 정의 (분리 끝점 · 이완 · vdW · registry 집계) 넷이 다르다. 우리 값의 위치: `db/properties/wad_*` · 보고서 2 절.

| 항목 | [Lu26LiAg] | 우리 W_ad 파이프라인 (방법만) | 판정 |
|---|---|---|---|
| 보고량 | W_ad = (E_Ag + E_Li − E_int)/A · 분리 = 따로 계산한 두 슬랩 (이완 여부 · Li 슬랩 격자 n/a) | W_sep = [E(far 10 Å) − E(bound)]/A · 강체 분리 (12 Å 점검) | 🔴 다른 양 — 같은 설정이면 W(이완 슬랩) ≤ W_sep |
| 범함수 · vdW | PBE · vdW 없음 | PBE + D3(BJ) 2 체 (ATM 민감도) | D3 는 W 를 키우는 쪽 · Ag 격자도 4.17 → (우리 PBE+D3) 4.07 Å |
| MLIP ↔ DFT 대조 | 정합 2 계면 DFT 재계산 (같은 기하인지 n/a · 허용 범위 사전 설정 없음): (111) 0.0919 vs 0.093 · **(100) 0.0455 vs 0.106 eV/Å² (43 %)** · 면 순서 뒤집힘 | 작은 모델 · 같은 원자 배치 · 같은 끝점 · 같은 D3 단일점 · 허용 차이 사전 설정 | ⭕ 우리 설계의 근거 — 표면 ≤ 9 % · 벌크 공공 ≤ 0.05 eV 통과가 계면 W 를 보증하지 않는다 · 오차 부호도 보편 아님 ([Agarwal26AD] 은 평균 과대) |
| registry | 5×5×5 재귀 격자 (면외 간격 포함) · 최저 하나 | 비등가 2–4 개 평균 + 범위 | ⚠ 다른 집계 — 문헌 대조 때 우리 최대 W registry 를 같이 본다 |
| 셀 · 변형 | 정합 FCC Li 3.77 % 2축 압축 · Ag 4.17 Å · 변형 전부 Li · Ag 24 Å (12 Å 고정) · Li 두께 수렴 0.01 eV/Å² (≈ 0.16 J/m²) | 무른 쪽을 Ag 격자 (PBE+D3) 에 맞춤 · Ag 4 층 (아래 2 층 고정) · 끝점 점검 0.01 J/m² | ⭕ 원칙 같음 · 변형률 · 두께 기준은 우리 것으로 다시 |
| 이식 후보 | 층별 공공 형성 z 프로파일 · BCC Li 로 만든 계면의 이완 뒤 상 판독 · 정합 FCC(111) Li\|Ag(111) 작은 셀 | — | ⭕ 7 절 Li\|Ag 를 계산할 때 |
```

### b-3. (권장 · 점착 트랙의 실제 집) `comparison_vs_ours_DEM.md` §I 에 **I-11**

```
### I-11. `lu2026_li_ag_interface_thermodynamics_kinetics` — ★★★ (DFT·MLIP · ⛔ G_c 아님) **Li 금속|Ag 계면 W_ad 의 첫 문헌 앵커** — 보고서 7 절 (Li 친화성) 의 입력과 함정

> **무엇을 주나.** VASP-PBE (vdW 없음) + MACE-MP-0 (medium · 미세조정 없음). Ag(111)·(100) 위 Li 6 방위. W_ad (eV/Å²): MACE FCC(111) 0.0919 · KS 0.0916 · NW 0.0898 · Pitsch = FCC(100) 0.0455 · Bain 0.0170 / DFT FCC(111) 0.093 · FCC(100) 0.106 (`Table 3` · p.4). 우리 환산 1 eV/Å² = 16.02 J/m².
>
> **★ 우리 축에 닿는 곳 셋.**
> ① **Young–Dupré** — 논문 γ_Li (`Table 2` · BCC 면 0.462–0.544 · J/m² 로 읽음) 로 우리 산수: DFT W ≥ 2γ_Li → θ = 0° (두 면 모두) · MACE (100) θ ≈ 59–75° · MLIP 이냐 DFT 냐가 (100) 의 젖음 판정을 바꾼다.
> ② **합금 구동력** — `Fig. 4` 첫 홉 ΔE figure-read ≈ −0.46 (111) · −0.17 (100) eV · W > γ_Ag + γ_Li → γ_int < 0 (부호 수준 · 우리 산수) = 섞이려는 계 → Ag 는 '젖음' 이 아니라 '섞임' 축 (7 절 ③).
> ③ **DFT vs MLIP** — 벤치마크 통과 뒤에도 (100) W −57 % — 우리 계면·종결별 같은-기하 확인 설계의 문헌 근거.
>
> **⛔ 인용 금지 / 한정어**
> · 이 W_ad 를 우리 W(PBE+D3 · 강체 W_sep · registry 평균) 와 같은 줄에 놓지 않는다 — 넷이 다르다. G_c (I-1 · I-3) 와는 더더욱.
> · "Li plates as FCC on Ag" · "(111) 이 (100) 보다 유리" (MACE 에서만) · "2 층부터 합금이 막힌다" (홉당 ≤ 6 배 · ps 규모) 는 옮기지 않는다.
> · `Table 2` 단위 표기 eV/Å² 는 J/m² 크기 — 원문 그대로 옮기지 않는다.
```

---

## (c) `pdf_map.tsv`

**필요 없음** — digest 를 쓴 뒤 `extract_figures.py --inbox --only lu2026 --dry` 가 자동으로 짝을 붙였다 (`[1쪽 본문 61%]` → `agli2026_li_ag_interface_thermo_kinetics_main.pdf`). 앵커가 61 % 로 낮다 싶으면 안전용 한 줄:

```
lu2026_li_ag_interface_thermodynamics_kinetics	agli2026_li_ag_interface_thermo_kinetics
```

---

## (d) 추가로 먹일 만한 논문 (≤ 8 · 최근 먼저 · 서지는 전부 이 논문 참고문헌 목록에서)

> 이미 **이번 배치에 있는 것** (세지 않음): Seymour & Aguadero *J. Mater. Chem. A* 9, 19901 (2021) = 배치 #1 (이 논문이 W_ad 비교 앵커로 쓰면서 참고문헌에서 빠뜨린 그 편) · Yang & Qi *Chem. Mater.* 33, 2814 (2021) = 배치 #2 (이 논문 ref [9] · 'W 가 작으면 공공을 가둔다') · Spencer-Jolly *Joule* 2023 = litdb 에 이미 있음 (`spencerjolly2023_ag_graphite_interlayer_operando_xrd`).

| # | 논문 | 저널 · 연도 | 왜 (축) | litdb |
|---|---|---|---|---|
| 1 | Thomas, Behara, Van der Ven — "Thermodynamic and Kinetic Properties of the Lithium–Silver System" | *Chem. Mater.* 36, 8936–8948 (2024) | **Li–Ag 합금** — 합금상 (D0₃-AgLi₃ · γ₁ · γ₃) 이동 장벽 ≈ 0.1 eV · 7 절 ③ 합금 구동력의 상평형 쪽 (이 논문엔 hull 없음) | 없음 |
| 2 | Behara, Thomas, Van der Ven — "Fundamental thermodynamic, kinetic, and mechanical properties of lithium and its alloys" | *Chem. Mater.* 36, 7370–7387 (2024) | **Li 금속 기준값** — BCC/FCC Li 공공 이동 (35 meV 출처) · γ_Li 후보 = Young–Dupré 분모 | 없음 |
| 3 | Xie, Diallo, Kim, Tu, Ceder — "The microscopic mechanism of lithiation and delithiation in the Ag/C buffer layer for anode-free solid-state batteries" | *Adv. Energy Mater.* 14, 2302960 (2024) | **Ag–C 층 + Li–Ag 합금** — BCC/FCC/γ 클러스터 전개 (300 K, Li > 46.6 at.% 에서 BCC 고용체) | 없음 |
| 4 | Ko *et al.* — "Mechanism of stable lithium plating and stripping in a metal-interlayer-inserted anode-less solid-state lithium metal battery" | *Nat. Commun.* 16, 1066 (2025) | **Ag–C 층 (금속 인터레이어) 기전** — 실험 쪽 합금 · 도금 위치 | 없음 |
| 5 | Deng *et al.* (Persson · Ceder) — "Systematic softening in universal machine learning interatomic potentials" | *npj Comput. Mater.* 11 (2025) | **MLIP 계면 검증** — 범용 MLIP 연화 (이 논문 MACE 장벽 과소의 원인 후보 · UMA 에도 해당하는지) | 독립 digest 없음 (`phuthi2026` · `zhang2026_minimum…` 에서 인용만) |
| 6 | Zhao *et al.* (Qi 공저) — "Imaging the evolution of lithium-solid electrolyte interface using operando scanning electron microscopy" | *Nat. Commun.* 16 (2025) | **Li 금속\|SE 공극** — Mg–Li 합금이 공극을 쪼갠다 (이 논문 Mg 제안의 실험 근거 · ref [41]) | 없음 |
| 7 | Yang, Liu, Mo — "Lithium crystallization at solid interfaces" | *Nat. Commun.* 14, 2986 (2023) | **Li 금속\|기판** — 기판 위 Li 결정화 MD (Li\|Li₂O 비정질 · HCP 꼴 5 층) · 계면 Li 상 선택 = 우리 Li 슬랩 면 · 상 결정 | 없음 (배치 #3 은 같은 그룹의 *Adv. Mater.* 2021 다른 편) |
| 8 | Lee *et al.* (Samsung) — "High-energy long-cycling all-solid-state lithium metal batteries enabled by silver–carbon composite anodes" | *Nat. Energy* 5, 299–308 (2020) | **Ag–C 층 원전** (Ag : 카본블랙 3 : 1 · 무과잉 Li) | 독립 digest 없음 (`spencerjolly2023` 계보에 인용만) |

---

## (e) DEM-DFT 보고서 (W_ad 보고서 7 절) 에 쓸 거리

> 우리 설정 = 보고서 부록 A + `wad_agc_graphite_prereg_2026_10_02.json` · `wad_agc_graphite_closed_2026_10_06.json` (Ag(111)|흑연 카드). 우리 W 값은 여기 안 싣는다.

| 7 절 항목 | 쓸 것 | 출처 | 직접 봤나 | 우리 설정과 같은 점 / 다른 점 |
|---|---|---|---|---|
| ② Li 친화성 — W 앵커 | Li\|Ag W_ad: MACE 6 계면 0.0170–0.0919 eV/Å² · DFT FCC(111) 0.093 · FCC(100) 0.106 (우리 환산 1.49 · 1.70 J/m²) | p.4 `Table 3` · p.4 본문 | 표 = PDF 텍스트 + 4쪽 렌더 (tab_3.png 이미지로는 안 봄) | **다름 넷**: 보고량 (따로 계산한 슬랩 vs 우리 강체 10 Å W_sep) · vdW 없음 vs 우리 D3(BJ) · registry 최저 vs 우리 평균 · Ag 격자 4.17 vs 우리 4.070 Å. **같음**: PBE · 평면파 · 무른 쪽이 변형 |
| ② Young–Dupré | 논문 γ_Li (BCC 0.462/0.501/0.544 · J/m² 로 읽음) 로 우리 산수: DFT W/γ_Li = 2.7–3.7 → θ = 0° · MACE (100) θ ≈ 59–75° · Bain 116–122° (무질서라 제외) | p.3 `Table 2` + p.4 | 표 = PDF 텍스트 | **같은 원칙**: 7 절은 '같은 Li 면으로 γ_Li' 를 적었다 — 논문은 그 짝을 안 맞췄다 (γ 는 BCC 무변형 · W 는 압축 FCC · γ 는 Tran 재인용 = 다른 DFT 설정). ⇒ 우리 계산에선 W 와 γ_Li 를 같은 셀 · 같은 설정으로 |
| ③ Ag 합금 구동력 | 첫 홉 (Li 가 Ag 자리 공공으로) ΔE figure-read ≈ **−0.46 (111) · −0.17 (100) eV** (MACE · (111) 은 DFT 도 ≈ −0.46) · 첫 Li 층 원자 에너지 −0.22…−0.27 eV · W > γ_Ag + γ_Li → γ_int < 0 (부호 수준 산수: DFT (111) −0.18…−0.26 · (100) −0.42 · MACE (100) +0.56 J/m²) | p.8 `Fig. 4` · p.7 `Fig. 2` · `Fig. 3` · p.3–4 표 | **봤다** (`Fig. 4` 3배 확대 · 마커 좌표 판독 · 라벨 6 개 ±0.002 eV 재현) | 우리 7 절 ③ 은 상평형 (hull) 으로 보자는 제안 — 이 논문엔 hull 이 없다 (Thomas 2024 · Xie 2024 필요). ΔE 는 공공이 먼저 있어야 하는 과정 (DFT 벌크 Ag 공공 형성 0.70 eV) |
| 부록 · DFT 와 MLIP 차이 | MACE-MP-0 가 표면 ≤ 9 % · 벌크 공공 ≤ 0.05 eV 통과 (`Table 1`, `Table 2`) → 그래도 W (100) −57 % · (111) −1 % · 면 순서 뒤집힘 · 저자 설명은 정의 없는 'Ag 슬랩 0.44 eV/atom' | p.3 `Table 1`, `Table 2` · p.4 본문 | 표 = PDF 텍스트 | **같음**: 둘 다 범용 MLIP · 미세조정 없음 · 작은 정합 셀을 DFT 로 확인. **다름**: 우리는 같은 원자 배치 · 같은 끝점 · 같은 D3 단일점 + 허용 범위 사전 설정 (논문은 같은 기하인지도 안 적어 오차를 구조/에너지로 못 가른다) · 우리 MLIP = UMA-s-1p1 + D3 (MACE 아님). 오차 부호 비보편 ([Agarwal26AD] 은 평균 과대) |
| 셀 설계 (7-1 의 Ag(111) 위 Li) | 정합 FCC(111) Li\|Ag(111) = 가장 작은 DFT 셀 (Li 3.77 % 압축 · 논문 격자 기준) · Ag 24 Å (자유 표면 쪽 12 Å 고정) · Li 두께 '계면 에너지 0.01 eV/Å² 수렴' · registry 재귀 격자 (5×5×5 · 면외 간격 포함) · 구조 MDF 공개 | p.3–4 본문 · p.5 `Fig. 1` | `Fig. 1` **봤다** | **다름**: 우리 Ag 4 층 (아래 2 층 고정) · k 헤드라인 9×9×1 (12×12×1 탐침) vs 논문 8×8×1 (셀 크기 n/a) · 쌍극자 보정 우리만 · 힘 수렴 논문 0.005 eV/Å 가 우리 ≈ 0.026 보다 빡빡 · 논문 두께 문턱 0.16 J/m² 는 우리 끝점 문턱 0.01 J/m² 의 16 배. 변형률은 **우리 격자로 다시** (Ag 4.07 Å 면 Li 압축이 3.77 % 와 다르다) |
| Li 면 · 상 선택 | BCC(110) 로 만든 KS 는 계면이 HCP 꼴로 전단 · Pitsch/Bain 은 FCC(100) 꼴 · 벌크 FCC–BCC 차 1 meV/atom (DFT) | p.2 · p.4–6 본문 | 텍스트 | 7 절이 Li(100) · Li(110) (BCC) 를 적었다 → **이완 뒤 Li 상 판독 (CNA · PTM)** 을 카드에 넣고 FCC(111) 정합 셀을 한 줄 더 |
| 장벽 인용 규칙 | 0.029 eV → 298 K 평균 대기 ≈ 0.31 ps · 2·3 층 0.124–0.136 eV ≈ 13–20 ps (벌크 FCC 0.11 ≈ 7 ps) · Ag 쪽 v_Ag 0.57 eV ≈ 0.44 ms (ν₀ 10¹³ s⁻¹ 가정) | p.8 `Fig. 4` · p.3 `Table 1` | 그림 봤다 | 우리 홉 수 검산 규칙 (`D-2026-09-27-barrier-hop-count`) 적용 — 논문의 '동역학적으로 막힌다' 는 옮기지 않는다 (홉당 1.7–5.8 배) |

---

## (f) 그림 크롭 요약

- 크롭 **7 장**: `fig_1`–`fig_4` (그림 4) · `tab_1`–`tab_3` (표 3). `missing_labels` = 0 · 손 크롭 · 재크롭 없음.
- 놓친 것: 없음. 12 쪽 'Graphical Table of Contents' 는 `Fig. 4` 와 같은 그림이라 안 잘렸다 (정상).
- **본 것**: 그림 4 장 전부 (`Fig. 4` 는 두 패널 3 배 확대 · `Fig. 2` · `Fig. 3` 은 픽셀 좌표 판독). 표 3 장은 이미지로 안 봤다 (PDF 텍스트 · 3–4 쪽 쪽 렌더).
- 그림이 본문과 어긋난 곳: ① `Fig. 3` 의 '벌크' 기준 (figure-read Li ≈ 0.53 · Ag ≈ 0.68 eV) 이 본문 MACE 벌크값 (0.57 · 0.74) 과 다르다 ② `Fig. 3` 캡션 "계면 Li 는 계산 안 함" ↔ 그림에 계면 Li 점 (0.63 eV, 본문 인용) ③ `Fig. 2` 캡션 "네 방위" ↔ 패널 6 ④ `Fig. 4` 캡션 "(100) 은 벌크보다 크다" ↔ 본문 "벌크와 같다 (0.11)" ⑤ `Fig. 2` · `Fig. 3` y 축 단위 없음 ⑥ 방향 표기 일부 비직교 (`Fig. 1`, `Fig. 4` inset). 숫자 라벨 자체는 그림 · 본문 · 표가 서로 맞는다.

## (g) Jeff Sakamoto 저자 여부

**아니다.** 저자는 Grace M. Lu · Dallas R. Trinkle 두 사람뿐 (UIUC · UC Irvine). Sakamoto 는 참고문헌 [8] (Sharafi *et al.* *Chem. Mater.* 29, 7961 (2017) = 이번 배치 #4) 에만 나온다. INDEX 행에 🏷 를 달지 않는다 · 웹앱 `paper_pis` = [] 확인.
