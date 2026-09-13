# 📥 PENDING — `ou2026_microstructural_multiscale_fast_ion_transport` 인덱스/비교 반영 대기
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션) — 변형: 4열 → 3열 (3·4열을 " · " 로 합침, 내용 손실 없음). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 작성 2026-09-09 · litdb-curator (동시 실행 다수라 `INDEX.md`·`comparison_vs_ours.md` 직접 편집 금지)
> **사람이 확인한 뒤 아래 4덩이를 각각 옮겨 붙이고, 이 파일을 지운다.**
>
> ⚠ **이 편은 세 축에 동시에 걸린다** — 붙일 곳이 **세 군데**다:
> ① 물성 4축 A(이온전도) ② **§J-9 능동학습 축** (네 번째 형식) ③ **새 축: 미세구조·입계** (우리에게 없던 축)
> 그리고 `INDEX.md` 는 **MLIP 방법론 표**가 아니라 **argyrodite/이온전도 본표**에 넣는 것이 맞다
> (물성값이 실제로 있다 — [Carrete23UQ] 류의 "방법 원전 전용"이 아니다).

---

## 1. `INDEX.md` — 붙일 위치: argyrodite 이온전도 본표

| `papers/ou2026_microstructural_multiscale_fast_ion_transport.md` **(본문 13 pp + SI 32 pp + Source Data xlsx 22시트 + 저자 배포 Codes/Figures/PolycrystalDiffusion 전수 독해)** | **[외부·⭐⭐⭐ 우리 3축 동시타격: NE 규약 · 능동학습 · 입계]** **Yongliang Ou**¹²\*/Lena Scholz³\*/S. Keshav³/Yuji Ikeda¹/Marvin Kraft⁴⁵/S. Divinski⁶/**Rafael Gómez-Bombarelli**²/**Wolfgang G. Zeier**⁴⁵/**Felix Fritzen**³\*/**Blazej Grabowski**¹\* (U. Stuttgart + MIT + U. Münster + FZ Jülich), "**Microstructural insights into fast ion transport in solid electrolytes via multiscale modeling**" (***Nat. Commun.* 17, 8726 (2026)**, DOI `10.1038/s41467-026-76216-w`, OA CC BY; 데이터 DaRUS `10.18419/DARUS-5959`; 접수 2026-01-09/수락 2026-07-22). **순수 계산(실험 0, 전부 문헌 소환).** **DFT(VASP/PBE/PAW/500 eV/⛔vdW 없음) → AIMD(52원자 1500 K, 벌크만) → 닫힌고리 local-AL MTP(level 18) → LAMMPS MD(5.2만 원자, 5 ns) → FEM 균질화(FANS 512³ / NEPER collapsed, 27립 RVE)** 4겹 스택. **Li₆PS₅X, X∈{Cl,Br,I} × 음이온 무질서 0/25/50/75/100 %.** **핵심 3**: ① **질서 벌크 확산장벽이 음이온 반경에 선형** — digest 회귀 **0.799 eV/Å, R²=0.998**(+0.1 Å → +79.9 meV); ⚠ **GB 장벽은 비선형**(조각기울기 0.152 vs 1.017 eV/Å) ② **GB 는 벌크에 따라 부호가 뒤집힌다** — 질서 Li₆PS₅I **D_GB/D_bulk 59.25↑** · 질서 Li₆PS₅Br **64.06↑** · **50 % 무질서 Li₆PS₅Cl 0.44↓** (LLZO 소환값 **9.29×10⁻⁴**=1000× 차단 ⇒ **황화물 GB 는 산화물보다 3자릿수 덜 막는다**) ③ **질서 Li₆PS₅I 의 비-Arrhenius(T_c≈250 K)가 GB 에서 온다** (실험 T_c 250 K·ΔEa −0.10 예측 vs −0.12 실측). **⭐⭐ 우리한테 제일 값나가는 수치 = 입계 손실의 정량화**(Source Data `FigureS20c` + 배포 FE CSV 재계산): 50 % 무질서 Li₆PS₅Cl 300 K 에서 **D_macro/D_bulk = 0.568(5.9 nm) → 0.942(100 nm) → 0.993(1 µm) → 0.999(5 µm)** ⇒ **µm 입도에서 입계가 깎는 양은 0.7 %.** 예측 σ(치밀,∞)=**29.47 mS/cm** vs **QENS[Korjus] 31.01 (1.07×)** vs **EIS 16점 최대 4.73 (6.2×)·중앙값 0.77 (38×)** ⇒ **벌크↔실험 격차는 GB 가 아니라 공극·접촉**(공극 25–57 %면 σ ×0.49–0.004, 3모델 편차 10×). **modified NE**: σ=Λ(ze)²D/k_BT, **Λ_Cl=2.181×10⁻² / Λ_I=1.590×10⁻¹ Li Å⁻³ (7.29× 차)**; digest 역산 **Λ_Cl/n_Li=0.92–0.99 ⇒ H_R≈1.0–1.15**(=우리 규약과 사실상 동일) vs **Λ_I ⇒ H_R≈0.14**(그건 Haven 비가 아니라 **실험 두 편(Brinek σ + Hogrefe D)에서 역산한 앵커**) ⇒ ⛔ **Λ_I 이식 금지 · `Fig. 4b` 세로위치는 자유예측 아님.** **🔬 저자 배포 코드·그림소스가 본문을 정정한 것 10건(digest §10)**: ① **격자상수 본문 10.28 Å ↔ 배포 MD 셀 10.044 Å (2.4 % 불일치)** — 후자가 실제 계산 셀이고 실험 대비 +1.9 %(=평범한 PBE) ② **D_GB 는 측정값이 아니라 `D_GB=(D_cell−(1−f)D_bulk)/f`, f=0.67630871385 인 병렬혼합 역산값** (코드 주석 `# temporary setting of gb width`) ③ **MSD 추정기가 log-log 기울기를 1 로 *강제*(`func(x,a)=x+a`) + 단일원점** ④ **피팅창이 벌크 3–5 ns vs 다결정 4–5 ns 로 다른데 그 둘을 빼서 D_GB 를 만든다** ⑤ **MTP 를 `--stress_weight=0` 으로 학습**(본문 미기재) ⑥ MD 온도격자 400–700 K(본문 미기재), 벌크 6점 vs 다결정 5점 ⑦ AL 파라미터 불일치(`--threshold_break=9e20` vs 본문 5)·미기재(라운드당 MD 샘플러 **4개 독립시드**, `cut_extrapolative_nbh --cutoff=20`, `reduce_size.sh … 50 MB 초과 폐기`, SI Fig 2 의 pre-select 상자는 **주석 처리돼 비활성**) ⑧ **Meyer–Neldel 기울기는 그림 안 주석에만 있다** — `ln D₀=8.4605 Ea+7.1184, R²=0.93 ⇒ E_MN=118.2 meV`(digest 계별 분해: Cl 103.0 / Br 108.4 / I 121.1 meV) ⑨ `Fig. 2b` "다결정 평균" 46.676 ↔ **FE 입력 44.425 (5 % 차)** — 46.676 은 38개 단일 GB 등방평균 46.631 과 0.1 % 일치 ⑩ 그림 소스 정확값(DFT 소형셀 Σ9 24.5478 / Σ3 9.1446 / 4.4294 meV Å⁻²; D∥ 평균 48.627·D⊥ 42.641 ⇒ **비 0.877** = 캡션 0.87 확인; **SI Fig S9a 6배열 산포 211.53–216.22 meV, 평균 213.87 = ±1.1 %만**). **🔴 본문 서술 ↔ Source Data 불일치 6건**(전부 주장을 키우는 방향): GB 장벽 감소 "~80 meV"→실제 **−62.2**; 무질서 GB 증가 "~10 meV"→**+18.9**; "nearly uniform ~0.02 eV"→**+75.0/+18.9/+34.8 meV(4× 스팬, 100 %에선 부호 반전 −25.7)**; "less than 0.1 eV in Cl and I"→**I 는 −104.9**; "an order of magnitude higher than highest EIS"→**6.2×**; "threefold higher GB D"→**2.58×**. **🔴 Source Data 자체 불일치 1건**: Hogrefe 실험 D 가 `Figure4` 시트 **4.56×10⁻¹¹** vs `FigureS20` 시트 **3.2×10⁻¹¹** — 전자만 본문의 "유효입도 31 nm"를 재현(내 로그-로그 보간 31.1 nm ✓; 후자면 51.3 nm) ⇒ **4.6×10⁻¹¹ 을 쓴다**. **🔴 최대 약점 = GB 폭 2.5 nm 가정**: 10 nm 셀에서 **GB 부피분율 67.6 %**(FE 분해 런은 최대 71.5 %)이고, digest 재계산으로 폭을 1.5 nm 로 바꾸면 D_GB/D_bulk 가 **0.44 → 0.18**, 1.0 nm 면 **음수(정의불가)** ⇒ **D_GB 절대값 이식 금지, 비(ratio)만·"폭 2.5 nm 가정 하에서" 단서 필수**. 기타 한계: 원자 "다결정"이 **결정립 2개** · MD **시드 반복 없음**(오차막대는 MTP 5개=모델 산포) · NVE 5 ns 드리프트 점검 미보고 · 공극은 FE 가 아니라 **후보정 배수** · MTP **할라이드 간 전이 실패**(Br 27.71 meV/atom, 자체 기준 <10 의 2.8배) · 실험 앵커가 서로 모순(Cl 장벽 0.112 QENS ~ 0.451 EIS). **⛔ 우리 modelc(Li₅.₄PS₄.₄Cl₁.₆)에 직접 대응 없음** — 그들 "무질서 %"는 **화학량론 고정 S↔Cl 자리교환**이고 우리 modelc 는 **Cl 과잉+Li 공공**이라 **다른 축**이다. 겹치는 것은 **comp1 (Li₆PS₅Cl) 하나**. **📦 배포 솔버 `PolycrystalDiffusion` (LGPL-3.0, MSUtils+FANS+marimo)**: 입력 = **복셀 Voronoi h5 + (D_bulk, D_GB∥, D_GB⊥) [10⁻⁷ cm²/s] 또는 (D₀, Ea[meV], T)**, 출력 = 농도·구배·유량장 + **유효 확산텐서**(σ 아님) ⇒ **우리 UMA D_bulk 로 라벨 0개 sweep 가능** | ✅ `papers/ou2026_microstructural_multiscale_fast_ion_transport.md` (§10 코드대조 · §14 한계 15항) | **MLIP(MTP-MD) + DFT/AIMD + FEM** (실험 0) — 축 **A**(이온전도) · **J-9**(능동학습) · **신설 미세구조·입계 축** |

---

## 2. `comparison_vs_ours.md` — 절 초안

### 2-a. Reference key 에 추가할 행

| **[Ou26MS]** ⭐⭐⭐ | **Y. Ou**\*/L. Scholz\*/S. Keshav/Y. Ikeda/M. Kraft/S. Divinski/**R. Gómez-Bombarelli**/**W. G. Zeier**/**F. Fritzen**\*/**B. Grabowski**\* 2026 ***Nat. Commun.* 17, 8726** (U. Stuttgart + MIT + U. Münster + FZ Jülich; DOI 10.1038/s41467-026-76216-w; **OA CC BY**; 데이터 DaRUS 10.18419/DARUS-5959; 솔버 **LGPL-3.0**) — "**Microstructural insights into fast ion transport in solid electrolytes via multiscale modeling**". **Li₆PS₅X(X=Cl,Br,I) 다결정 Li 수송을 DFT→AIMD→local-AL MTP→MD(5.2만 원자)→FEM 으로 잇는다.** 실험 0. **우리와 재료계가 정확히 같은 유일한 "MLIP 학습 AL + 입계" 편**이고, **σ=Λ(ze)²D/k_BT 의 Λ 를 조성마다 다르게 잡는다**(Cl 2.181×10⁻² ↔ I 1.590×10⁻¹ Li Å⁻³, 7.29×) — 우리 NE(H_R=1) 규약의 외부 앵커이자 반례. **저자 배포 코드·TikZ 소스를 열어 본문과 대조한 결과 정정 10건**(digest §10) | ✅ `papers/ou2026_microstructural_multiscale_fast_ion_transport.md` | **MLIP(MTP)+DFT/AIMD+FEM (계산 100 %)** — 축 **A** · **J-9** · **신설 입계 축** |

### 2-b. 물성 4축 표 — **A(이온전도)** 에 추가할 행 (⚠ 이 편은 물성값이 있으므로 4축 표에 들어간다)

| 항목 | **[Ou26MS]** | 우리 | 판정 |
|---|---|---|---|
| Ea (Li₆PS₅Cl 벌크) | **0.3843**(질서) / **0.1985**(25 %) / **0.2162**(50 %) / 0.2158(75 %) / 0.3407(100 %) eV — MTP-MD, α≡1 강제, 3–5 ns 창 | **comp1 0.253 eV** (UMA-MD, 단일 궤적, 2–50 ps 자유절편) | 🔶 **같은 자릿수, 정량비교 금지.** 우리 0.253 이 그들 25 %(0.198)~50 %(0.216) 위·질서(0.384) 아래 ⇒ 우리 comp1 배열이 **부분 무질서처럼 거동**한다는 정성 해석까지만. 힘장·창·추정기 전부 다르다 |
| Ea (Cl-rich) | ⛔ **대응 조성 없음** (그들 축은 화학량론 고정 S↔Cl 교환) | modelc 0.224 (3-seed 0.197±0.032) | 🔴 **비교 불가.** ⚠ 우리 3-seed 산포 ±0.032 가 그들 25 %↔50 % 차이(0.018)보다 크다 |
| D (600 K, 질서 Li₆PS₅Cl 벌크) | **1.724×10⁻⁶ cm²/s** | comp1 **3.09×10⁻⁶** / modelc 7.90×10⁻⁶ | 🔶 우리 comp1 이 그들 **질서** 벌크의 1.8× (그들 50 % 무질서 600 K 벌크값은 미공개) |
| **D_GB / D_bulk** | 질서 Cl **8.79↑** · 25/50/75 % **0.19/0.44/0.38↓** · 100 % 2.85↑ · 질서 Br **64.06↑** · 질서 I **59.25↑** · (LLZO 소환 **9.29×10⁻⁴**) | 🔴 **없다** | 🔴 **우리에게 없는 양.** ⚠ 이식하려면 **GB 폭 2.5 nm 가정**이 딸려온다 |
| **D_macro / D_bulk (입도 의존)** | 50 % 무질서 Cl 300 K: **0.568(5.9 nm) / 0.788(23 nm) / 0.942(100 nm) / 0.993(1 µm) / 0.999(5 µm)** | 🔴 없다 | ⭐⭐ **우리 "벌크 상한" 주석을 정밀화하는 값.** ⇒ *"우리 D 는 **치밀 µm-다결정 상한**(입계 손실 <1 %)"* |
| σ (RT, 50 % 무질서 Li₆PS₅Cl) | 예측 **29.47 mS/cm**(치밀,∞) · QENS 31.01(1.07×) · EIS 최대 4.73(6.2×)·중앙값 0.77(38×) | ⛔ **σ 절대값 인용 금지**(우리 규약) | 🔴 **한 표에 올리지 않는다.** 그들 값도 Λ 가정이 들어간 유도값 |
| Ea vs 음이온 반경 | **질서 벌크 0.799 eV/Å, R²=0.998** (⚠ GB 는 비선형) | 해당 없음 | ⭕ **설계 규칙으로 인용 가능** — 단 "질서 벌크에서만" |
| Meyer–Neldel | **ln D₀ = 8.4605 Ea + 7.1184, R²=0.93, E_MN=118.2 meV** (그림 주석) | 🔴 없다 | ⭕ **기존 궤적 후처리로 즉시 계산 가능** (T1 이식) |
| 격자상수 a (Li₆PS₅Cl) | 본문 **10.28 Å** ↔ 배포 MD 셀 **10.044 Å** (2.4 % 불일치) | comp1 ≈ 10.04–10.055 Å (PBE-D3) | 🟰 **배포 셀과 우리가 사실상 같다.** ⛔ 본문 10.28 을 인용하지 않는다 |

### 2-c. `### J-9. 능동학습 축` 에 추가할 소절 — **J-9c. [Ou26MS] — MLIP 학습 AL (물질탐색 AL 아님)**

> **왜 여기 놓나**: J-9a([Cho25AL])·J-9b([Ma25AL])는 **물질 발굴** AL 이고,
> [Ou26MS]·[Carrete23UQ]는 **퍼텐셜 학습** AL 이다. **둘은 다른 종(種)이다** —
> 앞의 둘은 *후보를 랭킹*하고, 뒤의 둘은 *라벨을 어디에 쓸지*를 고른다.
> ⛔ **우리 `discovery enrichment 1.22× (p=0.426)` 를 이 편과 같은 표에 놓지 마라** — 분모가 다르다.
> **[Ou26MS] 가 특별한 이유 하나: 재료계가 우리와 정확히 같다(Li₆PS₅X).** [Carrete23UQ]는 EAN·SrTiO₃다.

| 항목 | [Ou26MS] | [Carrete23UQ] | 우리 |
|---|---|---|---|
| 불확실도 | **D-optimality 외삽등급 γ (단일 모델)** | **앙상블 분산** (committee/bootstrap/DE) | 🔴 없음 |
| acquisition | MaxVol `select_add`, γ_select **1.4**, 채택 임계 γ>**1.7** | `σ²_f·exp(−E/k_BT)`, Powell | 순차 게이트 |
| 오라클 | **DFT (VASP/PBE)**, 저정밀 이완 + 고정밀 단일점 2단계 | DFT (GPAW) | UMA-MD (대리) |
| 배치 | **라운드당 MD 샘플러 4개(독립 시드)**, level 당 최대 100 반복 | — | — |
| **중단조건** | ⭐ **①** MD 에서 더 이상 샘플이 안 나오면 **②** **목표 물성(GB 에너지·D)이 충분히 정확하면 level 상승 중지** | 오차 수렴 | 예산 |
| 대조군 | ⭕ **global-AL, 각 5회 반복** | ⭕ 추정기 3종 | ⛔ 없음 |
| **라벨 절감 (digest 재계산)** | **총 DFT 라벨 441 vs 2372 = 5.4×** (사전학습 6.4× · AL 획득 1.8×) · AL 라운드 6.2 vs 51.2 = **8.3×** · **level 6 에서 94 % 획득** | — | — |
| 일반화 시험 | ⭕ **Table S1** — 🔴 **할라이드 간 전이 실패**(Br 27.71 meV/atom vs 자체 기준 <10) | 표면 확장 | LODO R² −0.1805 |
| 사전등록 | ⛔ 없음 | ⛔ 없음 | ⛔ 없음 |

**⇒ J-9 에 추가할 판정 2줄**
- **J9-h ⭐⭐ 중단조건을 "보고량 수렴"으로 잡는 형식의 외부 선례가 생겼다.**
  *"optimized … guided directly by the target material properties rather than fitting or validation error"*
  — 우리 **보고량 카드**(`kb/templates/estimand_card.md`) 규율과 같은 철학에 독립적으로 도달했다.
- **J9-i ⭐ 국소구조 추출 라벨링(30 000 원자 → >200 원자 주기셀)** = 우리가 계면/도핑 슬랩 DFT 라벨이
  필요해질 때 비용을 2자릿수 줄이는 처방. **정확한 알고리즘이 `cut2box.py` 에 있다**
  (box 16 Å 시작 +0.2 증가 · 보호영역 6.5 Å · 화학량론 맞을 때까지 **최근접거리가 짧은 경계원자부터 삭제** ·
  d≥1.6 Å · 저정밀 DFT 이완 후 고정밀 단일점 1회).
  ⚠ 재사용 시 확인: `box_final` 이 16 Å 고정인데 `box_length` 는 커질 수 있어 PBC 되접힘 가능(clamp 코드가 주석 처리돼 있다).

**⛔ 이 축에서 [Ou26MS] 로 하면 안 되는 것**
- ⛔ **"AL 이 랜덤 대비 N배" 근거로 인용** — 랜덤 arm 이 없다. 대조군은 **global-AL** 이지 랜덤이 아니다.
- ⛔ **γ 임계 1.4/1.7/5 를 UMA 에 이식** — D-optimality 활성집합은 **MTP 같은 선형-파라미터 모델 전용**이다.
- ⛔ **"5.4× 절감"을 우리 캠페인 예산에 그대로 적용** — 그건 **local-AL vs global-AL** 비교이지 AL vs 무작위가 아니다.

### 2-d. 🆕 **신설 제안 — 미세구조·입계 축** (⚠ 절 번호는 병합자가 배정. J-12 후보)

> **우리에게 통째로 없는 축이고, 이 편 하나로 열 수 있다.**
> 질문: *"우리 D_bulk 와 실험 σ 사이의 격차 중 입계 몫은 얼마인가?"* → **답: µm 입도에서 1 % 미만.**

| 우리가 지금 가진 것 | 이 축의 이름 | 빈 칸 |
|---|---|---|
| D_bulk (comp1 3.09e-6 / modelc 7.90e-6 @600 K) | **벌크 자기확산** | ⭕ 있음 |
| 없음 | **D_GB (입계 확산)** | 🔴 비어 있음 (이식하면 폭 2.5 nm 가정이 딸려온다) |
| 없음 | **D_macro (다결정 유효)** | 🔴 비어 있음 — **`PolycrystalDiffusion`(LGPL-3.0)으로 라벨 0개 sweep 가능** |
| 없음 | **공극·접촉 항** | 🔴 비어 있음 — 이 논문도 FE 로 안 풀고 후보정 배수(3모델이 10× 갈린다) |
| DEM 펠릿 축 (별도 repo 축) | **분말 압축·공극률** | 🔶 있으나 DFT 축과 연결 안 돼 있음 ← **여기가 다리다** |

**이 축의 판정 3줄 (지금 바로 원고에 쓸 수 있는 것)**
1. **입계는 µm 입도에서 무시해도 된다** (D_macro/D_bulk = 0.993 @1 µm, 0.942 @100 nm).
2. **벌크 예측이 QENS 와는 1.07× 로 맞고 EIS 와는 6–38× 어긋난다** ⇒ 격차의 주인은 **펠릿**이다.
3. ⛔ **"GB 가 없으니 우리 D 를 실험 σ 와 직접 비교해도 된다"로 읽으면 안 된다** — 공극·접촉 항이 남아 있고,
   그 항의 크기는 이 논문에서도 모델에 따라 **10× 갈린다**.

---

## 3. `properties/` · `db/` 갱신

- **`litdb/properties/`** — repo 에 없음. 물성 원장은 `db/properties/` 인데 **이번 세션은 `db/` 수정 금지** 지시라 손대지 않았다.
- 사람이 반영할 때 검토할 것: `db/properties/canonical_registry.json` 의 comp1 D/Ea 항목에
  **`comparison_group` 주석으로 "치밀 µm-다결정 상한"** 을 다는 것이 이 편의 직접적 소득이다
  (⚠ 값은 안 바뀐다 — **해석 라벨만** 붙는다).

## 4. 🎤 talk 역링크 — **불필요 (확인 완료)**

`grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → **`talks/lee2026_skku_mlip_materials_design.md` 하나뿐**.
그 **§99-10 대기열 9행**(Kim2026 hydrolysis · 자료집 목차 · Shapeev/Gubaev/Podryabinkin/Novikov MTP 계열 ·
Merchant GNoME · Park SevenNet · Luo cryo-TEM · Shin BH₄ · KimYS moisture · KimYH GA-MLIP)에
**Ou / Grabowski / Fritzen / multiscale / FEM 없음** ⇒ 양방향 링크 대상 아님.

> 🔗 단, **연결 고리는 하나 있다**: 그 대기열의 **3b·3b′·3c·3c′ = Shapeev 2016 / Gubaev 2019 /
> Podryabinkin 2017 / Novikov 2021 / Podryabinkin 2023(MLIP-3)** 가 **이 논문이 쓴 AL 의 방법 원전**이다
> (이 논문 ref 19·44–47). 그 편들의 digest 가 만들어지면 **[Ou26MS] 를 "그 방법의 argyrodite 응용 사례"로
> 상호링크**할 것. `papers/shapeev2016_moment_tensor_potentials.md` 는 **이미 있다** ⇒ 병합자가
> 그 digest 에 한 줄 추가하면 즉시 연결된다.

## 5. 그 밖

- **`litdb/pdf_map.tsv`** — 필요하면 행 추가:
  `ou2026_microstructural_multiscale_fast_ion_transport` ↔ `88._Microstructural_insights_…pdf`
  (`litdb/figures/_sources.json` 에는 추출 도구가 이미 기록했다.)
- **`litdb/inbox/`** — 본문·SI 를 `88._Microstructural…pdf` / `88._Sup_Microstructural…pdf` 로 복사해 뒀다.
- **`litdb/figures/ou2026_…/`** — **31점**(본문 fig 1–4 + tab 1 · SI fig S1–S22 + tab S1–S4).
  ⚠ SI 는 추출 도구가 `Suppl. Fig.` 캡션을 못 잡아 **내가 "SI 페이지 1장 = 그림 1장"으로 직접 렌더**해
  `figures.json` 에 병합했다(200 dpi, 페이지 번호·캡션 포함). **도구 개선 후보**:
  `extract_figures.py` 의 캡션 정규식에 `Suppl\.\s+(Fig|Table)\.` 형식을 추가하면 이 논문 계열(Nature 계 SI)이 자동으로 잡힌다.
- **저자 배포자료 압축본**은 **repo 밖** 세션 스크래치패드에 풀었다 (`work/ou2026/`) — repo 에 커밋하지 않았다.
