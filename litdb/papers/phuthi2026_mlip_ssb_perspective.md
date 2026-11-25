<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-10-07 신규 작성 (논문 에이전트). 사용자 요청: "우리 내용이랑 많이 겹치는거 같아서 확실하게".
       ① 이 편은 Perspective 다 — 자체 계산 0 · 자체 MLIP 학습 0 · 자체 실험 0. 숫자가 나오는 곳은
          본문 몇 줄과 **SI 의 비용 셈법(Table S1–S3)** 뿐이고, 그 비용표도 "새 벤치마크 0건 — 문헌 4개 환산" 이다.
          ⇒ comparison_vs_ours.md 물성 4축(A–D) 표에 **넣지 않는다**. 자리는 J 축 🔧 방법 원전 블록(J-59)이다.
       ② 크로핑 9장(본문 그림 6 + SI 표 3) 중 **본문 그림 6장 전부를 실제로 봤다**. SI 표 3장은 관례대로
          PDF 텍스트로 옮겼다(이미지로 안 봤다).
       ③ 핵심 산출물은 §7 "우리 작업과의 겹침 지도" · §7-B "같은 단위 비용 대조" · §8 우선순위 목록이다.
          우리 숫자는 **새로 옮기지 않고 원장 경로로 가리킨다** — 단, 비용 대조에 필요한 장부 숫자(GPU-h · 원자 수 · 시간)와
          방법 검증량(힘 RMSE · softening 기울기 — 1저자 2026-09-19 인용 가능 확정)은 원장 문구 그대로 인용했다. -->

# Machine Learning Interatomic Potentials for Modeling Solid-State Batteries — Phuthi, Wei, Li, Majumdar, Kolluru, Kumar, Blau, Canepa, Chan, Gómez-Bombarelli, Persson, Ceder, Ong\* (*Chem. Mater.* 2026, Perspective, ASAP)

> slug `phuthi2026_mlip_ssb_perspective` · DOI `10.1021/acs.chemmater.6c01051` · type `review/Perspective (자체 계산 0 · 비용 그림은 문헌 벤치마크 4개의 환산)` · PDF `litdb/inbox/Phuthi2026 ChemMater Machine Learning Interatomic Potentials for Modeling Solid-State Batteries.pdf` (18 pp = 본문 A–K 11 pp + refs 200개) + `litdb/inbox/Sup) Phuthi2026 ChemMater … .pdf` (SI 10 pp · Table S1–S3 · refs S1–S22) · digested `2026-10-07` · status ✅ · 태그 **[외부]**
> elements: Li, Na, P, S, Cl, B, H
> methods: DFT, AIMD, MD, MLIP, NEB, ESW, elastic, phonon

> 🙋 **사용자 요청 (2026-10-07)**: *"우리 내용이랑 많이 겹치는거 같아서 확실하게"* — 그래서 이 digest 의 중심은 논문 요약이 아니라 **§7 겹침 지도 · §7-B 비용 대조 · §8 빠뜨린 것 / 더 엄격한 것** 이다.
> 트랙: **SE·DFT 축 (방법론 · 우리 MLIP 사용 전반)**. 여러 트랙에 걸친다 — 각 행에 트랙과 1저자를 같이 적었다 (li2s = 외부 1저자 · CEI = 실험 쪽 1저자 · ESW/cascade/우리 DFT 기준선/W_ad = 사용자).
> 🎤 **관련 발표**: 해당 없음 — `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` 의 대기열 어디에도 이 논문이 없다.

> **저자·소속**: Mgcini Keith Phuthi\* (UCSD Nanoengineering) · Grace Wei · Bryant Li · Kristin Persson · Gerbrand Ceder (UC Berkeley / LBNL) · Sauradeep Majumdar · Rafael Gómez-Bombarelli (MIT) · V. S. C. Kolluru (Argonne CNM / Ohio State) · Nitesh Kumar · Samuel Blau (LBNL) · Pieremanuele Canepa (Houston; 약력에는 Purdue) · Maria K. Y. Chan (Argonne CNM) · **Shyue Ping Ong\*** (NUS). 전원 **ESRA (Energy Storage Research Alliance, DOE Energy Innovation Hub, Argonne)** 소속 겸직. 교신 kphuthi@ucsd.edu · shyue@nus.edu.sg.
> **서지**: 접수 2026-04-09 · 개정 2026-09-10 · 수락 2026-09-11 · 권·쪽 미부여(ASAP, `XXXX`) · 이해충돌 신고 없음 · 지원 ESRA DE-AC02-06CH11357.
> ⚠ **개발자 저자진**: Ong(M3GNet·MatPES·pymatgen) · Ceder/Persson(CHGNet·Materials Project·MatPES) · Blau(OMol25·OPoly26) — 본문이 이름을 대는 파운데이션 모델·데이터셋 상당수가 저자들 것이다. 상업 벤더 공저(makino2026 의 PFP)는 아니지만 **"FP 를 먼저 쓰라" 는 권고의 이해관계는 적어 둔다**(§10-A).

> **본 digest 에서 실제로 본 그림 (2026-10-07)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` — **본문 그림 6장 전부**.
> 안 본 것: `Table S1` `Table S2` `Table S3` (크롭은 있다 · 표는 PDF 텍스트가 정확해서 텍스트로 옮겼다).
> 그림에서만 읽은 값은 **`figure-read ≈`**, 논문 수로 내가 계산한 값(원논문 미보고)은 **`digest 계산`** 으로 표시했다.

---

## 0. 이 digest 를 읽는 법 — 답 먼저

| 물음 | 답 |
|---|---|
| 이 편이 새로 주는 숫자가 있나 | **거의 없다.** 본문에 MLIP 정확도 수치(meV/atom · eV/Å)가 **0회** 나온다. 숫자는 SI 의 **비용 셈법**(`Table S1`–`Table S3`)과 본문 몇 줄(담금질 속도 · 셀 크기 · 15 % 탄성)뿐이다. |
| 우리와 진짜 겹치는 곳 | **세 군데**: ① 이온전도 MD 규약(`§2.1.2`) ② "FP 먼저 → ab initio 로 검증" 권고(`§2.1.1` · `§3`) ③ 계면·SEI·유리에서 FP 를 믿지 말라는 경고(`§2.2.2`–`§2.2.3`). 셋 다 **우리 원장이 이미 더 구체적으로 정해 둔 것**이다 — §7 표. |
| 우리가 이 편보다 엄격한 것 | MSD 창 고정 · 확산 자격 게이트 · 시드 종류 분리 · 위원회 독립성 감사 · 원소별 softening · 관측창/홉 수 한 줄 · 절대 σ 금지. **논문은 이 중 하나도 정량 규칙으로 주지 않는다** (§7-D). |
| 우리가 빠뜨린 것 | ① 400/500 K 제외가 **통계 탓인지 체제 변화 탓인지** 안 갈랐다 ② Haven 교차상관을 **직접** 안 쟀다 ③ fine-tune 판정 기준 문서가 없다 ④ 우리 표준 셀·창이 `Table S1` 하한(2 nm · 0.3 ns) **경계 또는 미달**이다 ⑤ 입계(GB) 수송 0 — §8. |
| 조심할 것 | 🔴 본문의 Haven 문장 **부호가 자기 인용(ref 93)과 반대**다 · 🔴 담금질 속도 문장의 인용(ref 153)이 **엉뚱한 논문**이다 · ⚠ `Fig. 1b` 의 "Universal MLIP" 기준은 **fine-tune 된 MACE-medium** 이고 "Custom" 기준은 **42만 원자** 벤치마크라 둘의 격차(≈218×)에 크기 효과가 섞였다 — §10. |

---

## 1. 한 줄 요약

MLIP(특히 파운데이션 퍼텐셜 FP)는 DFT 대비 **수 자릿수 싼 비용으로 ~10⁴ 원자 · ns** 를 단일 GPU 에서 열어 주므로 전고체전지의 상안정·이온전도·OCV·표면·기계·열·계면·반응·스크리닝을 새로 볼 수 있다 — **단 "설득력 있는 과학적 주장은 아직 ab initio 또는 *검증된* custom/fine-tuned MLIP 에 기대야 한다"** 는 것이 저자들의 결론이고, 그 근거로 `Fig. 1b` 에서 속성별 최소 계산을 **GPU-h 로 환산한 비용표**(SI 셈법)를 낸다.

---

## 2. 메타 / 구성

| 항목 | 내용 |
|---|---|
| 유형 | Perspective (ESRA 허브 공동). 자체 계산 **0** — SI S2.3 원문: *"No new performance benchmarks were performed as part of this work."* |
| 구성 | §1 원자단위 모델링 (1.1 ab initio·경험 퍼텐셜 · 1.2 MLIP·FP · 1.2.1 데이터셋) → §2 SSB 물성 (2.1 고유물성: 상안정·이온전도·OCV·표면·기계·열 / 2.2 계면: ESW·계면수송·반응 MD·산화환원·상변화·외부전위 / 2.3 소재발견·고처리량) → §3 결론 |
| 그림·표 | 본문 Fig. 1–6 (표 0) · SI Table S1–S3 |
| 전고체 물질 언급 | Li₆PS₅Cl 두 번(Wang 2022 MTP 계면 · Ou&Grabowski GB) · Li₃PS₄ / Li₃OCl (GB 부호) · Li₇P₃S₁₁ · Na closo-hydridoborate(`Fig. 3`) · Mn-rich DRX(`Fig. 4`). **"argyrodite" 단어 0회.** |
| 이름이 나오는 모델 | 경험: ReaxFF · EAM(SI) / custom: ACE · GAP · MTP · Allegro(SI) / FP: **M3GNet · CHGNet · MACE (MACE-MP-0 · MACE-MATPES-r2SCAN-0) · UMA (UMA-OMAT)** / 전하인식: 4G-HDNNP · AIMNet2 · QET · Latent Ewald · MACE-POLAR-1 / δ-학습: MLTB(DFTB) |
| 이름이 **안** 나오는 모델·데이터 | SevenNet · Orb · MatterSim · eqV2 · PET-MAD · NequIP · DeePMD · **MPtrj** · Alexandria · GNoME (전문 검색 0회). **UMA 의 크기·버전(s/m · 1p1) 표기 없음.** |
| 이름이 나오는 데이터셋 | MP 이완 궤적 · **MatPES (r2SCAN)** · **OMat24** · OMol25 · OC22 · OpenPolymers(OPoly26) · OBELiX(실험 σ) · Li–P–S 벤치마크(Fragapane & Deringer 2026) |

---

## 3. 핵심 수치 — **이 편이 인쇄한 숫자 전부** ★

### 3a. 본문 숫자

| 항목 | 값 (원문) | 위치 | 비고 |
|---|---|---|---|
| SE 실용 이온전도 문턱 | **> 0.1 mS cm⁻¹** (typically) | §1 | ref 2 (Janek & Zeier 2016) |
| DFT 규모 상한 | **< 10³ 원자 · ~1 ns (O(10⁶) MD 스텝)** | §1.1 | ⚠ `Fig. 1a` 의 DFT/AIMD 회색 상자는 이보다 작다(§10-B2) |
| MLIP-MD 단일 GPU | **~10,000 원자 · ns** "readily accessible" | §1.2 | refs 25, 26 |
| MLIP vs 경험 퍼텐셜 | MLIP 가 **1–2 자릿수 느리다** | §1.2 | ref 26 |
| FP vs custom 매개변수 | FP 가 **≥ 1 자릿수 많다** → 추론 느리고 메모리 큼 | §1.2 | 정성 |
| MLIP 가 특히 맞는 계 | **"slower dynamics e.g., < 0.1 mS cm⁻¹"** · 비정질·다결정 | §2.1.2 | ref 87 |
| DFT 탄성 vs 실험 | **0 K · 대개 15 % 이내** | §2.1.5 | ref 116 (de Jong 2015) |
| GB 영향 폭 | **2–5 nm** · 결합 bulk–계면(공간전하 포함)은 **수십 nm** | §2.2.2 | ref 144 |
| Ou & Grabowski (Li₆PS₅Cl GB) | **> 16,000 원자 · > 5 ns** | §2.2.2 | ref 146 (PRMaterials 2024) |
| GB 밀도의 부호 | Li₃PS₄ 에선 σ **↑**, Li₃OCl 에선 σ **↓** | §2.2.2 | ref 143 |
| MD 담금질 속도 | **~10¹⁴ K/min (MD) vs ~1 K/min (실험)** = **14 자릿수** | §2.2.3 | ⚠ 인용 ref 153 이 Ni-rich 양극 열처리 실험 논문이다 (§10-B3) |
| 실제 입자 크기 | **> 10 μm** — 전 원자 시뮬레이션 밖 | §2.2.3 | refs 157, 158 |
| 스크리닝 처리량 | DFT **수십–수백** 후보 vs MLIP **수천–수백만** ("단일 DFT 이완 시간에") | §2.3.2 | ref 198 |
| `Fig. 6` 목표 범위 | **E_hull < 0.1 eV/atom · σ > 1 mS/cm** | `Fig. 6` | 예시 그림 안의 글자 |
| 결론의 규모 | MLIP 최적 구간 = **> 10³ 원자 · ns** | §3 | |

### 3b. SI `Table S1` — 속성별 **하한** 길이·시간 (그림 1a 의 각 영역 왼쪽 아래 꼭짓점)

> SI 원문 단서: *"order-of-magnitude lower bounds rather than universal convergence criteria"* · *"the lower bounds therefore indicate when a property can reasonably **begin** to be evaluated, rather than the trajectory length required for a highly converged result"* · ⭐ *"the statistical precision of a diffusion coefficient depends primarily on the **number of statistically independent diffusion events** sampled, rather than on trajectory duration alone."*

| 속성 | 하한 길이 | 하한 시간 | 근거 문헌 (SI) | 관측창 환산 (digest 계산 · 300 K · ν₀ 10¹³ s⁻¹ **가정** · 자리 1개) |
|---|---|---|---|---|
| Bulk ion diffusion | **2 nm** | **0.3 ns** | S1 Grasselli 2022 (유한크기) · S2 He 2018 (통계분산) | Ea_max ≈ 0.026·ln(3×10³) ≈ **0.21 eV** |
| Grain-boundary transport | 10 nm | 5 ns | S3 Ou 2024 (LPSCl GB) | ≈ 0.28 eV |
| Interfacial transport | 15 nm | 50 ns | S4, S5 | ≈ 0.34 eV |
| Structural evolution | 5 nm | 20 ns | S6, S7 | ≈ 0.31 eV |
| Local vibrations | 1 nm | 0.001 ns | S8, S9 | — |
| Phonons | 0.5 nm | Static | S10, S11 | — |
| Thermal conductivity | 5 nm | 5 ns | S12, S13 | — |
| Thermodynamic stability | 0.3 nm | Static | S14, S15 | — |
| Reaction dynamics | 15 nm | 10 ns | S16–S18 | ≈ **0.30 eV** |
| SEI formation, early stages | 15 nm | 100 ns | S4 | ≈ **0.36 eV** |

> 관측창 열은 우리 규칙(`D-2026-10-05-md-observation-window`: Ea_max ≈ kT·ln(ν₀·t), 자리 n 개면 + kT·ln n)을 논문의 하한 시간에 적용한 것이다 — **논문에 없는 계산**이다. 읽는 법: 저자들이 "반응 동역학은 10 ns 부터 볼 수 있다" 고 할 때, 300 K 에서 그 궤적이 단일 자리에서 원리적으로 볼 수 있는 장벽은 **≈ 0.3 eV 까지**다. 15 nm 슬래브처럼 반응 자리가 10⁴ 개면 + 0.026·ln 10⁴ ≈ +0.24 eV → **≈ 0.54 eV**. 논문 본문의 정성 서술(*"only processes with relatively small kinetic barriers are likely to be observed directly"*, §2.2.5)과 같은 방향이다.

### 3c. SI `Table S2` — 그림 1b 의 작업량 정의

밀도 **ρ = 50 atoms nm⁻³** 가정 · N = ρL³ (입방) / N = ρAh (슬래브, A = L²) · **Δt = 2 fs** · S = 1000·t[ps]/Δt[fs] · 이온스텝·변위구조·AIMD 스텝 = 에너지+힘 1회 (SCF 반복은 따로 안 셈).

| 계산 | N (원자) | S (스텝/평가) | 가정 |
|---|---|---|---|
| Thermodynamic stability | 50 | 50 | 이온 이완 50 스텝 |
| Phonons | 100 | 300 | 원자당 6 변위 × 대칭 축소 0.5 |
| Bulk conductivity | **400** | **1.5 × 10⁵** | 2 nm 입방 · 0.3 ns · 2 fs |
| Interface dynamics | **112,500** | **2.5 × 10⁷** | 15 × 15 × 10 nm³ 슬래브 · 50 ns · 2 fs |

### 3d. SI `Table S3` — 기준 비용 (전부 **NVIDIA A100 1장** 문헌값의 환산)

비용 모형: **G_m = C_ref,m · N · S · (N/N₀,m)^(p_m − 1)** — DFT/AIMD **p = 3**, custom·universal MLIP **p = 1**, 고전 FF 는 **G = C_ref · N · S · ln N / ln N₀**. SI 원문 단서: *"do not explicitly account for fixed computational overhead, memory limitations, **reduced GPU utilization for small systems**, communication overhead, or changes in numerical convergence with system size."*

| 방법 | 기준계·모델 | 보고 성능 | 환산 C_ref (GPU-h · atom⁻¹ · step⁻¹) | 출처 |
|---|---|---|---|---|
| DFT/AIMD | ~50 원자 **Be** · VASP PAW-PBE · **Γ 점 · 300 eV** · MP1 σ 0.2 eV | **8.33 s / 평가** | **4.63 × 10⁻⁵** | S19 Baghishov 2026 |
| Custom MLIP | **Allegro** (Li₃PO₄ 전용) · **421,824 원자** | **0.552 μs / atom·step** | **1.53 × 10⁻¹⁰** | S20 Musaelian 2023 |
| Universal MLIP | **MACE-medium, Cu–Al 로 fine-tune 된 FP** · 1,024 원자 | **0.12 ms / atom·step** | **3.33 × 10⁻⁸** | S21 Bernstein 2024 |
| Classical FF | LAMMPS **EAM** · 4.096 × 10⁶ 원자 | **190 × 10⁶ atom-step / s** | **1.46 × 10⁻¹²** | S22 Lawrence 2023 |

### 3e. 그림 1b 막대 재구성 — **digest 계산** (위 셈법 그대로 · 원논문은 막대만 그렸고 숫자를 안 적었다)

| GPU-h | DFT/AIMD | Custom MLIP | Universal MLIP | Classical FF |
|---|---|---|---|---|
| Thermo stability (50 × 50) | **0.116** (≈ 7 분) | 3.8 × 10⁻⁷ | 8.3 × 10⁻⁵ | 9.4 × 10⁻¹⁰ |
| Phonons (100 × 300) | **5.6** | 4.6 × 10⁻⁶ | 1.0 × 10⁻³ | 1.3 × 10⁻⁸ |
| **Bulk conductivity (400 × 1.5×10⁵)** | **1.78 × 10⁵** (≈ 20 GPU-년) | **9.2 × 10⁻³** (≈ 33 초) | **2.0** | 3.5 × 10⁻⁵ |
| Interface dynamics (112,500 × 2.5×10⁷) | **6.6 × 10¹⁴** (축 상단 10¹² 밖 — 막대 잘림) | **430** (≈ 18 일) | **9.4 × 10⁴** (≈ 11 년) | **3.1** |

> **검산 (그림과 대조)**: `Fig. 1b` 를 실제로 보고 막대 꼭대기를 읽었다 — Universal·Bulk `figure-read ≈` 10^0.3–10^0.5 GPU-h · Custom·Bulk `figure-read ≈` 10⁻² · Universal·Interface `figure-read ≈` 10⁵ (오른쪽 축 "10 yr"–"100 yrs" 사이) · FF·Interface `figure-read ≈` 10^0.5 · DFT·Interface 막대는 축 꼭대기 10¹² 에서 **잘려 있다**. 위 계산과 모두 같은 자릿수다 ⇒ SI 셈법이 그림을 실제로 만든 식이 맞다.
> **Universal / Custom 비 = 3.33×10⁻⁸ / 1.53×10⁻¹⁰ ≈ 218 배** — `Fig. 1b` 의 노랑–청록 격차 전부가 이 한 비율이다(§10-B1 에서 이 비율의 함정).

---

## 4. 계산 방법 ★ — 자체 계산이 없으므로 "저자들이 권하는 방법 지도"

- **code / version · functional · pseudo · k · ecut**: 이 편의 계산 **없음**. 유일한 계산 설정은 SI 비용 기준의 DFT 벤치마크(VASP PAW-PBE · Γ · 300 eV · MP1 0.2 eV · ~50 원자 Be)인데 **남의 벤치마크**다.
- **데이터 충실도 권고 (§1.2.1)**:
  - "MLIP 는 학습·검증 데이터만큼만 좋다." 품질 = ① **원자환경 표본화**(능동학습 / 저충실도 긴 궤적의 부표본화) ② **이론 수준(functional)** ③ **수치 수렴**(ecut · k).
  - functional 이 열역학 안정성(ref 33)과 **이온 확산도(ref 62 Banerjee & Tkatchenko 2025)** 를 바꾼다 → r2SCAN(MatPES) · ωB97M-V(OMol25) 데이터셋. *"MLIP 추론 비용은 functional 과 무관하다"* 가 상위 functional 로 가는 논리.
  - **나쁜 전자 수렴 → 틀린 힘** (ref 64 Kuryla 2025) · **DFT+U 불일치 → 오류** (ref 65 Warford 2026, *"Better without U"*).
  - 실험 데이터 학습(미분가능 궤적 재가중, ref 66)은 연구 중.
- **UQ (§1.2.1 · §3)**: committee(ref 58) · conformal prediction(refs 59, 60) · Bayesian(ref 57) — *"critical for the safe deployment of MLIPs"* · 결론에서 *"uncertainty quantification will be an essential component of their trustworthy use"*. ⚠ **위원회 구성원의 학습 데이터 중복**에 대한 말은 **없다**.
- **fine-tune (§1.2)**: 좁은 화학공간에 소량 데이터로 FP 를 fine-tune(예: Na 옥시할라이드 SE ref 45 · Mn-rich DRX ref 46)이 "인기 있는 절충". best practice 는 *"active areas of research"* (refs 47, 48 = 우리 `liu2026_finetuning_umlip_tutorial` 의 arXiv 판). **"언제 fine-tune 하나" 의 정량 기준은 주지 않는다.**
- **δ-학습 (§1.2)**: tight-binding + ML 보정(MLTB) — 전자구조까지 나온다는 장점, 단 TB 자체를 먼저 맞춰야 한다.
- **무질서**: *"Repetitions of simulations with different initial conditions and structural disorder also allow for more robust statistical error estimates"* (§2.1.2, refs 85, 87). SQS·열거 같은 구체 처리 언급 없음.
- **§2 전체의 전제 (중요)**: *"As a conceptual framing, we will assume that an MLIP can be trained to arbitrary accuracy in reproducing the PES. In practice, MLIPs should always be validated against ab initio results."* ⇒ §2 의 "MLIP 로 이것도 저것도 된다" 는 **정확도 문제가 풀렸다는 가정 위의 서술**이다. 이 가정을 빼고 §2 문장을 인용하면 과장이 된다(§10-A2).

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a | 속성 범주별 **최소 길이(nm) × 최소 시간(ns)** 지도 (log–log). 각 영역 왼쪽 아래 = `Table S1` 하한, 그라데이션 = 클수록 좋다. 짙은 회색 = DFT/AIMD 한계, 옅은 회색 = MLIP-MD 한계 | 우리 MD 셀(558 · 204 · 120 원자)과 창(200–800 ps)을 이 지도 위에 찍어 보는 **자기 점검용** — §7-C. ⚠ 회색 상자 크기가 본문 수치와 안 맞는다(§10-B2) |
| 1b | 대표 계산 4종 × 방법 4종의 **GPU-h 막대**(왼쪽 log 축 10⁻¹²–10¹²) + 단일 GPU 벽시계(오른쪽 축 1 s … 100 yrs) | **우리 실측 장부와 같은 단위 비교** — §7-B. 막대값은 §3e 에 재구성 |
| 2 | ab initio · custom MLIP · foundational MLIP 를 7개 기준(실행 용이 · 학습데이터 비용 · 검증 비용 · 실행 비용 · 일반화 · 정확도 · 전자구조)으로 짙기 비교한 **표 그림** | FP 칸의 *"generally have qualitative accuracy"* · *"may need finetuning for quantitative accuracy"* · *"Validation tests against ab initio necessary"* — 우리 UMA 인용정책(상대차만)의 **외부 문구 근거** |
| 3a | Na–B–H 3원 상도 **300 K vs 650 K** (MLIP 유한온도 자유에너지) — 650 K 에서 새 상 **o-NBH = Na₃(B₁₂H₁₂)(BH₄)** 이 ★로 등장 | 유한온도 상안정 예시. 우리 hull 은 0 K DFT — 적용 낮음 |
| 3b | log D(cm² s⁻¹) vs 1000/T: Na₂B₁₂H₁₂(단사) · NaBH₄ · o-NBH. 실선 = 적합, 점선 = 300 K 까지 외삽 | ⭐ **고온 아레니우스 외삽 경고**의 시각 근거 — 우리 600/800/1000 K 3점 규약과 직결 (§7 행 6) |
| 4 | custom CHGNet 으로 낸 Li_xMn₀.₈Ti₀.₁O₁.₉F₀.₁ 의 **전압 곡선**(spinel vs δ 상) — x 간격이 촘촘 | 우리 축 밖 (양극 OCV) |
| 5a | 전고체 셀 모식 (집전체 · 양극 · SE · 금속 음극 · 음극–SE 계면상) | 계면 범주 정리용 |
| 5b | 양이온 산화환원 vs 음이온 산화환원 + O₂ 방출 모식 | CEI(실험 쪽 1저자 트랙) 어휘 |
| 5c | 사면체 회전(10–20° tilting)과 Li 홉의 **약한/강한 상관** 모식 (Jun 2024, CC-BY) | 우리 T16(음이온 회전 자기상관 도구)의 어휘 |
| 5d | 금속 음극–SE 계면상 층 구조 모식: bulk SE(≳1 nm) · 표면 무질서(~1 nm) · 비정질(≳2 nm) · 결정화(~1 nm) · 표면 무질서(~1 nm) · bulk 음극(≳2 nm) | T3(Li\|LPSCl 반응 MD) 셀 두께 설계 시 층 두께 감각 |
| 6 | 역설계 루프: 구조 생성 → **MLIP 물성 예측(E_hull < 0.1 eV/atom · σ > 1 mS/cm)** → 갱신 | ⚠ MLIP σ 를 **절대 문턱**으로 쓰는 그림 — 우리 절대 σ 금지 규율과 정반대 (§7 행 18) |
| Table S1 | 속성별 하한 길이·시간 표 | §3b · §7-C |
| Table S2 | 비용 작업량 표 | §3c |
| Table S3 | 기준 벤치마크 표 (A100 4건) | §3d · §10-B1 |

### 5a. 그림별 실제 판독 (본 것만)

- **`Fig. 1a`** — 축: x Length Scale (nm) 10⁻¹–10³, y Time Scale (ns) "Static" · 10⁻³ … 10⁴. 범례 7범주(Ion transport · Structural/Mechanical · Vibrational · Thermal transport · Thermodynamic · Kinetics · Aging). "Bulk ionic conductivity" 영역은 `figure-read ≈` 2 nm · 0.3 ns 에서 시작해 **DFT/AIMD 상자 밖**에 있다. DFT/AIMD 짙은 상자는 `figure-read ≈` x ≤ 1.5 nm · y ≤ 0.3 ns, MLIP-MD 옅은 상자는 `figure-read ≈` x ≤ 100 nm · y ≤ 40–50 ns. SEI formation 영역은 MLIP 상자 **위로 삐져나간다** (100 ns 하한 > MLIP 상한) — 저자들도 SEI 초기 단계는 MLIP-MD 로도 하한 근처라는 것을 그림으로 인정한 셈이다.
- **`Fig. 1b`** — §3e 검산 참조. 오른쪽 축 눈금: 1 s · 1 min · 1 hr(= 10⁰ GPU-h) · 1 d · 1 mon · 1 yr · 10 yr · 100 yrs. DFT·Interface 막대는 잘려 있다.
- **`Fig. 2`** — 짙은 초록 = 그 기준에서 최선. Ab initio 는 학습데이터·검증·일반화·정확도·전자구조가 짙음, 실행비용은 흰색. Custom 은 실행비용만 짙음. Foundational 은 실행 용이성만 짙음, 나머지 옅음. **정확도 칸: Custom "only reliable in-distribution" · Foundational "may need finetuning for quantitative accuracy"**.
- **`Fig. 3b`** — y 축 라벨이 "Diffusivity (cm² s⁻¹)" 인데 눈금이 −5 … −20 이라 실제로는 **log₁₀ D** 다(라벨 누락). x 1000/T 1.25–3.5, 점선 세로선 `figure-read ≈` 3.33 (= 300 K). o-NBH 는 **300 K 까지 직접 시뮬레이션 점**이 있고 `figure-read ≈` log D −6.6. Na₂B₁₂H₁₂ 는 `figure-read ≈` 1000/T ≈ 2.0 (500 K) 부근에서 기울기가 꺾이고 가장 낮은 점은 `figure-read ≈` 2.67 (≈ 375 K) · log D ≈ −9, 300 K 외삽은 `figure-read ≈` −12.6. NaBH₄ 는 고온 4점만 있고 외삽 `figure-read ≈` −20. ⇒ 본문 *"non-Arrhenius behavior for Na₂B₁₂H₁₂ below 500 K"* 와 그림이 **맞는다** (꺾임이 보인다).
- **`Fig. 4`** — y 1.0–5.5 V vs Li/Li⁺, x 0–1.2. spinel(검정)은 `figure-read ≈` x 0.6 에서 ≈ 3.5 → 2.4 V 로 큰 계단, δ 상(빨강)은 완만. 초록 점선 `figure-read ≈` x 0.59. 본문 *"large voltage drop in the spinel phase and solid solution behavior in the δ phase"* 와 맞는다.
- **`Fig. 5`** — 모식뿐 (수치 없음). (d) 의 층 두께는 원문 그대로 위 표에 옮겼다.
- **`Fig. 6`** — 모식. 목표 범위 글자만 수치.

---

## 6. Post-processing ★ — 저자들이 언급하는 분석 기법

| 기법 | 이 편의 서술 | 우리 쪽 |
|---|---|---|
| MSD → tracer D | *"typically computed from the mean squared displacement"* · 창·적합 규칙 **없음** | MSD 창 2–50 ps 고정 · 자유절편 D · 골격 COM 제거 · 시간원점 평균 (CLAUDE.md · `kb/concepts/md.md`) |
| 교차상관 / Haven | *"requires an explicit calculation of cross-correlation terms, which has become feasible with MLIP"* | 미실행 (NE · Haven=1) — §8 ② |
| Green–Kubo | **열전도**에서만 언급(refs 132, 133) · 이온 σ 용 GK 는 **안 나온다** | 미실행 · 정본 `lynch2026_greenkubo_mlip_conductivity_thesis` |
| 통계 오차 | refs 85 (Usler 2023 일반식) · 87 (He 2018) 인용만 | `he2018_statistical_variances_diffusional_aimd` · `mccluskey2025_…` · `zaby2026_…` digest 보유 |
| 아레니우스 | 고온 외삽 경고 · 비아레니우스 · 고온 상전이 | 600/800/1000 K 3점 · Ea 상대차만 |
| NEB | 고처리량 NEB(ref 103 fine-tuned CHGNet) · **FP 는 전이상태를 잘 못 맞춘다(ref 104)** | Li₃N UMA NEB 조사 → 금지 (§7 행 11) |
| 증강 표본화 | metadynamics(ref 105) · FP 재가중 합의(ref 155) | 미실행 |
| 열역학 | grand potential 상도(ref 138) · 유한온도 진동엔트로피 | 0 K DFT grand potential (축 B) |
| 전하 할당 | Bader/오비탈 분해는 *"only used to compare changes"* · 전하인식 MLIP 의 전하는 PES 와 이론적으로 일관되지 않을 수 있다 | Bader/ICOHP 는 DFT 로만 |

---

## 7. 우리 작업과의 겹침 지도 ★★★ (이 digest 의 핵심)

> 판정 어휘: **같다** · **다르다** · **우리가 더 엄격** · **우리가 빠뜨림** · (필요 시 둘 이상).
> 우리 쪽 근거는 **원장 경로**로 가리킨다. 숫자를 옮긴 곳은 비용 장부·방법 검증량뿐이다 (σ·D·Ea·W 값은 옮기지 않는다).

### 7-A. 겹침 지도

| # | 우리 자리 (트랙 · 1저자) | 이 논문의 권고/서술 | 판정 | 근거 (우리 기록 · 논문 위치) |
|---|---|---|---|---|
| 1 | **MD 전도 — 창·적합** (우리 DFT 기준선 · 사용자) | MSD → D 라고만 한다. 창·절편·확산영역 판정 규칙 **없음**. SI: 하한 = *"reaching the linear diffusive regime"* · 정밀도는 **독립 확산 사건 수**가 좌우 | **우리가 더 엄격** | CLAUDE.md §MLIP-MD (창 2–50 ps 고정) · cascade v6 카드의 D_inc 평탄성·부창 기울기비·사건 수 게이트 (`db/properties/cascade_d_rel_closed_2026_10_01.json` §1) · 논문 §2.1.2 · SI S1 |
| 1′ | 〃 (반례) | SI *"precision … depends primarily on the number of statistically independent diffusion events"* | 🔴 **우리 자료가 이 문장의 한계를 보인다** | cascade v6 는 런당 **사건 3,992–4,724 회**(문턱 50)로 사건 수는 넉넉히 통과했는데 **확산 자격은 0/40** (MSD 가 2–100 ps 에서 아래로 휨). ⇒ 사건 수는 **필요조건**이지 충분조건이 아니다 — 같은 원장 §1 `③_사건수` · `①_D_inc` |
| 2 | **MD 전도 — 셀·시간 하한** (〃) | `Table S1` bulk ion diffusion **2 nm · 0.3 ns** (order-of-magnitude 하한 · 수렴 기준 아님) | **우리가 빠뜨림 (경계·미달)** — 단 상대비교 규약이라 무효화는 아님 | §7-C 표: 558 원자 ≈ 2.2 nm · 표준 200 ps (시간 미달) / cascade 204 원자 ≈ 1.6 nm · 200 ps (둘 다 미달) / li2s 유리 120 원자 L ≈ 14 Å (길이 미달 · 원장 단서가 이미 박음) |
| 3 | **MD 전도 — 시드·무질서 통계** (〃 · li2s 는 외부 1저자) | *"Repetitions … with different initial conditions and structural disorder"* → robust error | **같다 (방향) · 우리가 더 엄격** | 우리: 비율은 멀티시드만(단일시드 1.33× 철회) · cascade 독립 부모 배열 10 × 속도 시드 2 · li2s 유리 = **담금질 시드 5 의 IQR · 속도 시드 열잡음과 풀링 금지** (CLAUDE.md MLIP-MD 줄 · `lpscl_smallcell_glass_md_v2_closed_2026_10_05.json` `D_시드간_상대산포`). 논문은 시드 **종류**를 구분하지 않는다 |
| 4 | **Haven / Nernst–Einstein** (우리 DFT 기준선 · 사용자) | 상관 운동 → H ≠ 1 · 교차상관을 **직접** 계산하라 · ⚠ *"ion−ion correlations often **suppress** net ionic conductivity, leading to Haven ratios **below one**"* | **같다 (원칙) · 우리가 빠뜨림 (직접 계산)** · 🔴 논문 문장 부호 오류 | 우리: σ 는 NE(Haven=1) · **절대 σ 인용 금지** · H_R 정의·부호 `kb/concepts/md.md` §6 · J-31 [Marc17NE] (H<1 ⇒ NE 가 σ 를 **과소**). 논문 문장은 H = D*/D_σ 정의에서 **"억제"와 "<1" 이 서로 반대** — 자기 인용 ref 93 (Marcolongo & Marzari) 과도 반대. §10-B4 |
| 5 | **Green–Kubo σ** (〃) | 이온 σ 에 GK 를 **권하지 않는다**(GK 는 열전도에서만) | **같다 (둘 다 안 함)** | 정본 `lynch2026_greenkubo_mlip_conductivity_thesis` · J-29 [He18Var] |
| 6 | **아레니우스 600/800/1000 K 3점 · 400/500 K 제외** (〃) | 고온 외삽은 비아레니우스·고온 상전이로 **무효화될 수 있다** · RT 직접 시뮬레이션(custom/fine-tuned)이 *"more reliable than the Arrhenius extrapolation from AIMD"* · `Fig. 3b` 의 500 K 꺾임 | **다르다 — 우리는 논문이 경고하는 경로 위에 있다** · 방어선 = Ea **상대차만** · RT σ 를 내지 않음 | CLAUDE.md (400/500 K 제외 판정 · 1저자 인용정책 2026-09-18) · 논문 §2.1.2 · §3 · `Fig. 3b`. ⚠ **제외 사유가 통계(창 안 비확산)인지 체제 변화인지 우리가 가른 기록을 찾지 못했다** → §8 ① |
| 7 | **FP 를 fine-tune 없이 쓰는 것** (우리 MLIP 전반) | FP 먼저 써 보라(*"almost always be advantageous to first perform simulations with an appropriate FP"*) — 그러나 *"convincing scientific arguments should still rely on ab initio or **validated custom/fine-tuned** MLIP predictions"* | **다르다 (등급)** — 우리 UMA-s-1p1(omat)는 **fine-tune 0** · 검증은 **스냅샷 힘 대조**로만 | 검증 장부: `lpscl_smallcell_closed_2026_09_18.json` (a-Li₄PS₄Cl 120 원자 · F RMSE 0.039 eV/Å · 상대 3.79 % · 단일 시드 10 프레임 · **G-B2 탈락**) · `b2o3_uma_vs_dft_force_result_2026_09_11.json` (R = 0.951) · `mlip_bench_li3ps4_uma.json` (Li₃PS₄ 243 구조 · F RMSE 0.0446 eV/Å). ⇒ 저자 기준으로 우리 UMA 수송은 "탐색" 등급이고, **우리 인용정책(상대차만 · citable false)이 그 등급과 맞물린다** |
| 8 | **softening (PES 연화)** (〃) | 본문은 *"FPs are known to poorly predict out-of-equilibrium and transition states; therefore, thorough benchmarking is necessary"* 한 줄 + ref 104 (Deng 2025 *Systematic softening*) 인용. **"softening" 단어는 본문에 없다** | **우리가 더 세분 (더 엄격)** | `lpscl_smallcell_closed_2026_09_18.json` 허용 서술 ③: 전체 기울기 0.9836 이지만 **원소별 부호가 갈린다** — S 0.9785 · P 0.9766 (무름) / Cl 1.0104 · Li 1.0149 (단단). ⇒ "FP 가 전반적으로 무르니 Li 이동이 과대평가된다" 는 단순 서사를 **우리 계에 그대로 쓸 수 없다** (⚠ 이것은 보고이지 게이트가 아니고, 힘 기울기 ≠ 장벽이다) |
| 9 | **위원회 UQ** (〃) | committee · conformal · Bayesian 을 권한다. 구성원 독립성 말 없음 | **우리가 더 엄격 (독립성 감사) · 우리가 빠뜨림 (보정)** | `mlip_committee_baseline.json`: UMA · MACE-MP-0 · SevenNet-0 세 FP 가 **실질 2진영**(MPtrj 공유 쌍이 가장 잘 맞음) · 문턱은 표본 분포에서 유도(물리 기준 아님) · 계는 modelc 62 원자 600 K 하나. conformal 보정은 안 했다 |
| 10 | **학습 데이터 functional · 참조 DFT** (〃) | functional 이 확산도를 바꾼다(ref 62) · r2SCAN 데이터 · 전자 수렴(ref 64) · +U 불일치(ref 65) | **같다 (인식) · 한계 공유** | UMA omat = OMat24 (PBE/PBE+U 계열) · 우리 참조 DFT 도 PBE/USPP(QE) ⇒ "PBE 대비 일치" 이상을 말 못 한다 — `b2o3_…_result` 의 봉인 단서 · `mlip_committee_baseline.json` 머리말(kim2024 · lee2024 functional 효과). 우리는 회수물 단일 실행 점검(`JOB DONE`·힘 블록 1·1)까지 했다 — 논문 ref 64 의 우려에 대한 실무 대응 |
| 11 | **UMA Li₃N 금지** (우리 DFT 기준선) | FP 는 *"generally have qualitative accuracy"* · OOD 에서 나쁨 · 전이상태 나쁨 (`Fig. 2` · §2.1.2) | **우리가 더 구체 — 논문 경고의 실사례** | `db/interphases/li3n.json` (`⛔_UMA_금지_2026_09_09` · UMA 가 위상을 뒤집음 · 인용위험 `HZ-uma-li3n-banned`) · `tools/neb_diffusion/li3n_uma_investigate.py` · b2o3 O-자리 UMA 선호를 DFT 가 뒤집은 사례(`kb/reports/paper_first_author_requests_2026_08.md` 분포 밖 외삽 행). 논문은 **계별 금지 판정**이라는 운영 단위를 말하지 않는다 |
| 12 | **유리/비정질** (li2s · ⛔ 외부 1저자 · 잠정 해석만) | 담금질 속도 MD **~10¹⁴ K/min** vs 실험 ~1 K/min · 데이터셋이 결정상에 치우침 | **같다 (차수) · 우리가 더 엄격 (보고 범위)** | 우리 120 원자 유리 담금질 **10¹² K/s (≈ 6 × 10¹³ K/min)** — 논문이 말하는 차수 그대로이고 원장이 이미 영구 단서로 박았다 (`lpscl_smallcell_closed_2026_09_18.json` §2-②). v2 마감은 **수송 계수를 보고하지 않는다** (`lpscl_smallcell_glass_md_v2_closed_2026_10_05.json`) · 대조 계 카드 `lpscl_smallcell_glass_control_li3ps4_estimand_2026_10_05.json`. ⚠ 외부 1저자 트랙이라 이 행은 **잠정 해석**이다 |
| 13 | **입계(GB) · 계면 수송** (우리 DFT 기준선) | GB 2–5 nm · 결합 bulk–계면 수십 nm · `Table S1` GB 10 nm/5 ns · 계면 15 nm/50 ns · Ou&Grabowski 16,000 원자 | **우리가 빠뜨림** | 우리 GB MD 0 건. 정본 문헌 `ou2026_microstructural_multiscale_fast_ion_transport` (같은 그룹 후속) · `kim2024_mtp_argyrodite_disorder_gb` · J-19 |
| 14 | **계면 점착 W_ad (UMA+D3)** (사용자 1저자) | FP 는 계면용으로 학습되지 않았다(*"lack of large data sets with interfaces"*) · 전하 이동 못 다룸 | **같다 · 우리가 더 엄격 (라벨 결속)** | `D-2026-09-23-wad-a-prime-scope` (작은 주기 모델 DFT 와 전체 계면 UMA+D3 예측 분리 · MLIP 은 탐색·DEM 민감도 시나리오로만) · `D-2026-10-01-wad-se-pairs-uma-card` · 결과 `wad_se_pairs_uma_result_2026_10_01.json` · 외주 V5 대조. **W 값은 여기 옮기지 않는다** |
| 15 | **SEI/CEI 반응 MD · 짧은 MD '무반응'** (T3 · CEI = 실험 쪽 1저자) | *"only processes with relatively small kinetic barriers are likely to be observed directly"* · 증강 표본화 · 외부 전위 못 다룸 · 전하 이동 한계 | **우리가 더 엄격 (정량 한 줄 의무)** | `D-2026-10-05-md-observation-window` (Ea_max ≈ kT·ln(ν₀t) 한 줄) · `D-2026-09-27-barrier-hop-count` · `tools/sei/collect_neb.py`. 위원회 기준선의 T3 함의(**PS₄ 골격에서 모델 간 합의가 가장 낮다**, `mlip_committee_baseline.json`) |
| 16 | **T3 Li\|LPSCl 반응 MD 계획** (우리 DFT 기준선 · 계획 단계) | `Table S1` SEI early **15 nm · 100 ns** · reaction **15 nm · 10 ns** | **우리가 빠뜨림 (시간 하한)** | 계획: Li 6 nm ‖ LPSCl 10 nm · ~7,000 원자 · 350 K · ≥ 20 ns (`kb/open_items.md` T3 행) ⇒ 길이(16 nm)는 한 축에서 맞고 횡단면(원문 "~3 nm²")은 15 nm 에 한참 못 미치며, 20 ns 는 reaction 하한 ≥ · SEI early 하한(100 ns) < . 관측창 350 K · 20 ns ≈ 0.37 eV (CLAUDE.md 예시) |
| 17 | **탄성 modelc_2x** (우리 DFT · 진행 중) | DFT 0 K 탄성 = *"well established"* · 실험 대비 ~15 % · 온도 효과는 보통 무시 · *"perhaps soft solid electrolytes"* 는 온도 의존 가능 · MLIP 로 유한온도·다결정 | **같다 (DFT 경로)** · 빠뜨림(유한온도) — **낮은 우선** | `D-2026-09-11-elastic-conv-threshold` (relaxed-ion Cij · 수렴 문턱) · 논문 §2.1.5. ⚠ 논문은 FP 탄성의 정확도(연화 → 계수 과소?)를 **말하지 않는다** — 그건 ref 104 원문 몫이다 |
| 18 | **cascade 고처리량 스크리닝** (사용자 1저자) | FP = 1차 거르기 → DFT/실험 검증 · 능동학습 fine-tune · UQ 보정 · `Fig. 6` 은 MLIP σ > 1 mS/cm 를 **목표 문턱**으로 그린다 | **우리가 더 엄격 (사후에 배운 것) · 논문이 빠뜨린 것** | cascade v6: **자격 0/40 · 242.10 GPU-h · 방법상 무효** — 속도시험 런에 판정 게이트를 안 걸었다 (`cascade_d_rel_closed_2026_10_01.json` `4_기록_남길_것.속도시험_자격_미점검` · CLAUDE.md §계산 규율 ⭐) → v7 탐침 카드 (`cascade_estimand_card_v7_probe_2026_10_01.json`). 논문에는 "그 스크리닝 지표가 **그 셀·그 창에서 정의되는가**" 를 먼저 판정하라는 말이 **없다** — 우리 실패가 바로 그 빈칸이다 |
| 19 | **비용 장부** (li2s · cascade) | `Fig. 1b` · SI 셈법 · *"reduced GPU utilization for small systems"* 미반영을 스스로 밝힘 | **같은 차수 · 우리가 4–8× 비쌈** · 작은 셀 오버헤드를 우리가 실측으로 보였다 | §7-B |
| 20 | **장거리 정전기 · 전하 인식** (공통) | 전하인식·장거리 MLIP 가 다음 세대 핵심 · Wang 2022 MTP 가 Li\|LPSCl 전하 이동을 못 기술 | **우리가 빠뜨림 (공통 공백)** | `comparison_vs_ours.md` §H (1128 행대: *"우리 UMA 는 단거리 GNN 이고 이 가정을 점검한 적이 없다"*) · `wang2022_resistive_decomposing_interfaces_se_alkali_metal` (= 논문 ref 15·94) |
| 21 | **상안정 / hull · ESW** (우리 DFT · 사용자) | FP 먼저, **최종 상안정은 반드시 ab initio 로 검증** · grand potential 상도 · 유한온도 | **같다** (우리 hull·ESW 는 DFT) · 유한온도 미반영은 공통 | 축 B (`comparison_vs_ours.md` §B) · 논문 §2.1.1 · §2.2.1 |

### 7-B. 같은 단위 비용 대조 — `Fig. 1b` vs 우리 장부 ★

> 단위는 **GPU-h · atom⁻¹ · step⁻¹** 로 맞췄다. 우리 쪽 숫자는 장부 문구 그대로, 나눗셈은 **digest 계산**이다. 차수 비교만 한다.

| 계산 | 기계 · 모델 | 장부 (원장 문구) | 원자 × 스텝 | 우리 GPU-h/atom·step | 논문 기준 | 배수 |
|---|---|---|---|---|---|---|
| cascade v6 MD 한 런 | kgy RTX 3090 · UMA-s-1p1 | **242.10 GPU-h / 41 런 · 런당 약 5.89 h** (`cascade_d_rel_closed_2026_10_01.json` `비용`) | 204 원자 × 102,500 스텝 (평형 5 + 생산 200 ps · 2 fs) = 2.09 × 10⁷ | **≈ 2.8 × 10⁻⁷** (≈ 1.0 ms/atom·step) | Universal 3.33 × 10⁻⁸ (A100 · MACE-medium FT) | **≈ 8.5 ×** |
| 〃 논문 셈법으로 예측하면 | — | — | 같은 셈 | — | 3.33 × 10⁻⁸ × 2.09 × 10⁷ = **0.70 GPU-h/런** | 실측 5.89 h |
| cascade v5 MD 한 런 | V100 · UMA | **3.09 GPU-h/런** (같은 원장 · ⚠ 셀·시간이 v6 와 같다고 가정 — 확인 안 함) | (2.09 × 10⁷ 가정) | ≈ 1.5 × 10⁻⁷ | 〃 | ≈ 4.4 × |
| 작은 셀 오버헤드 실측 | (장비 미기록 · 도구 기본 `cuda`) | `mlip_engine_probe_comp1.json`: 52 원자 6,921 μs/atom·step → 416 원자 1,532 μs/atom·step · *"원자 8배 → 스텝당 1.8배 · 원자당 4.5배 싸짐 ⇒ 작은 셀은 오버헤드 지배"* | — | — | SI 가 *"reduced GPU utilization for small systems"* 를 **모형에 안 넣었다고** 밝힘 | 우리 실측이 그 빈칸의 크기를 보인다 |
| DFT SCF 1 점 | kgy QE 7.4.1-GPU · PBE · 52 Ry · Γ | **점당 8.1 분** (`lpscl_smallcell_gb3_result_2026_09_18.json`) · 120 원자 | 1 평가 | 0.135 GPU-h/평가 | 논문 DFT 모형: 4.63 × 10⁻⁵ × 120 × (120/50)² = **0.032 GPU-h (≈ 1.9 분)** | **≈ 4.2 ×** |
| li2s 유리 담금질 1 시드 | kgy · UMA · 120 원자 | 벽시계 **28.7–47.0 h** · 등분 점유 **14.3–16.5 GPU-h** (`lpscl_smallcell_glass_control_li3ps4_amendment_cs_2026_10_05.json` `①_80_이_틀린_이유`) | (담금질 스케줄 원자×스텝 미확인) | — | — | 장부 정의(벽시계 vs 등분 점유)가 **두 가지**라는 것 자체가 논문 셈법에 없는 축 |

**읽는 법**
- **같은 자릿수 안이다.** 우리 MD 는 논문 모형보다 **4–8 배**, DFT SCF 는 **≈ 4 배** 비싸다. 기계(A100 vs V100/3090), 모델(MACE-medium FT vs UMA-s), 셀 크기(1,024 vs 204 원자), 계(Be·Cu–Al vs 황화물 · 300 eV vs 52 Ry ≈ 707 eV)가 다 다르므로 **차이를 분해하지 않는다.**
- ⚠ **우리 GPU-h 장부의 정의를 확인하지 않았다** — cascade 의 "런당 5.89 h" 가 단독 점유 벽시계인지, 한 GPU 에 여러 런을 얹은 벽시계인지에 따라 배수가 달라진다(li2s 장부는 그래서 등분 점유를 따로 둔다). 원장에서 확인하기 전에는 **"같은 차수"** 까지만 말한다.
- **논문 셈법의 진짜 쓸모**: 카드의 비용 견적을 "같은 캠페인·기계의 실측 장부와 대조" 하라는 우리 템플릿 §4-c(회신 CS)의 **외부 1차 견적기**로 쓸 수 있다 — 단 우리 작은 셀은 오버헤드 지배라 **논문 모형이 과소 견적**한다는 보정(× 4–8)을 붙인다.

### 7-C. `Table S1` 하한 위에 우리 MD 를 찍으면 (digest 계산 · 논문의 ρ = 50 atoms nm⁻³ 가정으로 길이 환산)

| 우리 MD | 원자 | L (nm) | 시간 | `Table S1` bulk 하한 2 nm · 0.3 ns | 비고 |
|---|---|---|---|---|---|
| 결정계 modelc · lpsocl box331 | 558 | ≈ 2.2 | 표준 200 ps (lpsocl box331 은 400 ps 런 있음) | 길이 ✓ · 시간 **미달**(200 ps) / ✓(400 ps) | 규약은 상대비교라 무효화되지 않는다 (dutra2025 digest 와 같은 결론) |
| cascade v6 셀 | 204 | ≈ 1.6 (공통부피 4,066 Å³ → 실제 밀도 ≈ 50.2 nm⁻³ 로 가정과 일치) | 200 ps (v6) · **400 ps (v7 탐침 · 개정 · 메인 세션 확인 10-07)** | 길이 **미달** · 시간 v6 **미달** / v7 **충족** | 자격 0/40 과 같은 방향의 신호 — 인과는 미검증 |
| li2s 소셀 유리 | 120 | ≈ 1.4 (원장 L ≈ 14 Å) | 550 K 800 ps · 600 K 400 ps | 길이 **미달** · 시간 ✓ | 원장 영구 단서(자기이미지 감김)가 이미 이걸 말한다 · ⛔ 외부 1저자 트랙 |
| T3 계획 | ~7,000 | 길이축 16 · 횡단면 원문 "~3 nm²" | ≥ 20 ns | SEI early 15 nm · 100 ns 대비 시간 **미달** | 계획 단계 · 보고량 카드 전 |

### 7-D. 우리가 이 논문보다 엄격한 것 — 원고·답신 포지셔닝용

1. **MSD 창 고정(2–50 ps) + 확산 자격 게이트** (D_inc 평탄성 · 부창 기울기비 · 사건 수) — 논문은 창 규칙이 없다. 그리고 우리 자료는 SI 의 "사건 수가 정밀도를 좌우" 가 **필요조건일 뿐**임을 보인다(사건 ~4,000 · 자격 0/40).
2. **절대 σ·D·Ea 인용 금지, 상대차만** (1저자 2026-09-18) — 논문 `Fig. 6` 은 MLIP σ 를 절대 문턱(> 1 mS/cm)으로 쓴다. 논문 자신의 결론(*"convincing arguments … validated custom/fine-tuned"*)에 비추면 **우리 쪽이 그 결론에 더 충실하다.**
3. **시드 종류 분리** — 담금질(구조) 시드 IQR 과 속도 시드 열잡음을 풀링하지 않는다. 논문은 "반복" 만 말한다.
4. **위원회 독립성 감사** — FP 세 개가 학습 데이터로 2진영이라는 것을 쟀다. 논문은 committee 를 권하기만 한다.
5. **원소별 softening 분해** — 전체 0.98 아래에서 S·P 무름 / Li·Cl 단단으로 부호가 갈린다. 논문은 ref 104 한 줄.
6. **계별 사용 금지 판정**(Li₃N) 과 인용위험 원장 — 논문은 "정성 정확도" 라는 등급만 준다.
7. **관측창·홉 수 한 줄 의무** — 논문의 "작은 장벽만 보인다" 를 수치 한 줄로 강제한다.
8. **결과 전 게이트·닫힘 조건** (보고량 카드 · 마감 규율) — 논문에는 사전등록·닫힘 개념이 없다.

---

## 8. 우리가 빠뜨렸거나 다시 볼 것 — 우선순위 (계산 제안은 전부 **보고량 카드가 먼저**)

1. **[우리 DFT 기준선 · 사용자] 400/500 K 제외의 사유 분류** — 통계(창 안 비확산 · 사건 부족)인지 **체제 변화**(비아레니우스 · `Fig. 3b` 같은 꺾임)인지 기록으로 가른다. 계산이 아니라 **기존 판정 기록 재독**이 먼저다. 체제 변화 가능성이 남으면 "Ea 상대차" 도 **두 계가 같은 체제에 있다는 가정** 아래에 있다는 단서를 원장에 단다.
2. **[우리 DFT 기준선] Haven 교차상관의 직접 계산** — 기존 궤적에서 후처리로 가능할 수 있다 (box331 예비 ≈ 0.60 은 `citable:false`). 보고량 카드 먼저: 교차항이 들어간 집단좌표 통계량은 원자마다 표본을 얻는 자기항과 달리 계 전체에서 표본 하나라 독립 표본이 적다(J-31 '집단좌표 통계량' 행 — gen1 200 ps 는 문헌 등급의 절반) 때문에 **"이 궤적 길이에서 잘 정의되는가"** 가 §3 의 질문이다.
3. **[MLIP 전반] fine-tune 판정 기준 문서** — "언제 fine-tune 하나" 를 우리 쪽 결정으로 남긴 적이 없다. 재료: `liu2026_finetuning_umlip_tutorial` · `tompa2026_finetuning_mlip_foundation_strategies` · `zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill` · 우리 G-B2 탈락(유리 Li–Cl 첫 봉우리 0.150 Å). 계산 아님 — 결정 원장 항목 후보.
4. **[cascade · 사용자] `Table S1` 하한을 v7 탐침 카드의 셀·시간 선택 근거로 대조** — 204 원자 · 200 ps (v6) 는 두 하한 모두 미달이었다 (v7 탐침은 생산 400 ps 라 시간은 충족 · 셀 ≈ 1.6 nm 는 여전히 길이 하한 2 nm 미달 · 메인 세션 확인 10-07). v7 카드가 이미 다른 질문(탐침)으로 갔으면 한 줄 대조로 끝난다.
5. **[T3 · 계획] 시간 하한** — SEI early 100 ns 대비 20 ns. 카드 §1–3 에서 "20 ns 로 무엇을 볼 수 있나" 를 관측창(350 K · 20 ns ≈ 0.37 eV)과 같이 명시.
6. **[비용 장부] GPU-h 정의 통일** — cascade "런당 h" 와 li2s "등분 점유" 가 같은 단위인지 확인. 논문 `Fig. 1b` 와 비교하려면 단독 점유 기준 하나가 필요하다.
7. **[위원회] conformal 보정** — 기준선이 modelc 62 원자 600 K 하나뿐. 새 계(유리 · 계면)에 쓰려면 그 계에서 다시 뽑아야 한다고 원장이 이미 말한다 — 그 재추출이 아직 없다.
8. **[낮음] 입계 MD · 유한온도 탄성 · 유한온도 상안정** — 논문이 기회로 든 것들. 지금 트랙들에 걸린 질문이 없으면 열지 않는다.

---

## 9. 인용 가능 문장 (deck / paper 용 — 원문 그대로)

- *"At this point, convincing scientific arguments should still rely on ab initio or validated custom/fine-tuned MLIP predictions."* (§3) — 우리 UMA 결과를 상대차·탐색으로 한정하는 이유의 외부 근거.
- *"We emphasize that where ab initio methods are feasible, MLIP predictions should always be validated against them."* (§3)
- *"FPs are known to poorly predict out-of-equilibrium and transition states; therefore, thorough benchmarking is necessary."* (§2.1.2, ref 104)
- *"Most FPs are not specifically trained for these applications, especially due to the lack of large data sets with interfaces."* (§2.2.3) — W_ad UMA 를 민감도 시나리오로만 쓰는 근거.
- *"… the quenching rates are often up to 14 orders of magnitude faster than in experiments (∼10¹⁴ K/min in MD compared to ∼1 K/min experimentally)."* (§2.2.3) — ⚠ 인용할 때 원 출처를 따로 확인 (이 편의 ref 153 은 맞지 않는다, §10-B3).
- *"Directly simulating superionic conductors at room temperature with custom/fine-tuned MLIPs can be more reliable than the Arrhenius extrapolation from AIMD."* (§3) — ⚠ "custom/fine-tuned" 를 빼고 인용하지 않는다.
- SI: *"the statistical precision of a diffusion coefficient depends primarily on the number of statistically independent diffusion events sampled, rather than on trajectory duration alone."* — ⚠ 우리 cascade 반례(§7-A 1′)와 같이 쓴다.
- ⛔ **인용 금지**: §2.1.2 의 Haven 문장(*"… suppress net ionic conductivity, leading to Haven ratios below one"*) — 부호 오류.

---

## 10. 주의 / 한계 (over-claim 방지)

### 10-A. 성격·이해관계
1. **개발자 Perspective** — M3GNet·CHGNet·MatPES·MP·OMol25 개발진이 "FP 를 먼저 쓰라" 고 권한다. 권고 자체는 합리적이지만 **독립 검증 문헌이 아니다.** `Fig. 3`·`Fig. 4`·`Fig. 5c` 도 저자들 그룹 작업이다.
2. **§2 는 "MLIP 정확도 = 임의로 좋다" 는 가정 위에 서 있다** (§4 인용). §2 의 "MLIP 로 X 를 할 수 있다" 를 정확도 단서 없이 인용하면 과장이다.
3. **정확도 수치 0 건** — meV/atom · eV/Å 가 한 번도 안 나온다. 어떤 FP 가 어떤 계에서 얼마나 틀리는지는 이 편으로 말할 수 없다 (그건 `chang2026_…` · `makino2026_…` · 우리 장부 몫).

### 10-B. 내부 어긋남·검증 결과
1. **`Fig. 1b` 의 Custom vs Universal 격차(≈ 218 ×)에 크기 효과가 섞였다** — Custom 기준은 Allegro **421,824 원자**(GPU 포화) 벤치마크이고 Universal 기준은 MACE-medium **1,024 원자**다. SI 스스로 *"reduced GPU utilization for small systems"* 를 모형에 안 넣었다고 밝혔다. 400 원자 bulk 계산에서 Allegro 가 0.552 μs/atom·step 을 낼 리 없다 ⇒ 400 원자 칸의 Custom 막대는 **과소**다. 또 "Universal" 기준이 **fine-tune 된** MACE 라 out-of-box FP 의 비용을 대표하는지도 불분명하다.
2. **`Fig. 1a` DFT/AIMD 상자 vs 본문** — 본문은 DFT 한계를 *"< 10³ atoms … ∼1 ns"* 라 하는데, 그림의 짙은 상자는 `figure-read ≈` 1.5 nm (ρ = 50 이면 ≈ 170 원자) · 0.3 ns 까지다. 본문 수치로 그리면 bulk ionic conductivity(400 원자 · 0.3 ns)가 DFT 상자 **안**에 들어간다 — 그림은 AIMD 의 영역을 본문보다 좁게 그렸다.
3. **ref 153 오인용 의심** — 담금질 속도 10¹⁴ K/min 문장의 인용이 Sun *et al.* *Nat. Commun.* 2025 *"Thermal processing to modulate surface chemistry and bulk charge distribution in nickel-rich layered lithium positive electrodes"* 로 되어 있다. MD 담금질 속도를 다루는 논문으로 보이지 않는다(제목 기준 · 원문 미확인). 숫자 자체는 통상 MD 담금질(10¹²–10¹³ K/s)과 맞다.
4. **Haven 문장 부호 오류** — H = D*/D_σ 에서 "상관이 전도를 **억제**" 면 D_σ < D* 라 **H > 1** 이어야 한다. 본문은 "억제 → H < 1" 이라 적었고, 인용한 ref 93 (Marcolongo & Marzari 2017) 은 LGPS 에서 H < 1 · NE 가 σ 를 **과소** 평가함을 보인 논문이다(우리 J-31). 바로 앞 문장 *"suppress or accelerate … not equal to unity"* 는 맞다.
5. **중복 참고문헌** — ref 15 = ref 94 (Wang … Canepa 2022 JMCA) · ref 90 = ref 138 (Ong … Ceder 2013 EES).
6. **`Fig. 3b` y 축 라벨** — "Diffusivity (cm² s⁻¹)" 인데 값이 −5 … −20 이라 log₁₀ 이 빠졌다.
7. **UMA 버전 미표기** — "UMA" · "UMA-OMAT" 만 나온다. 우리 `uma-s-1p1` 과 같은 체크포인트인지 이 편으로 알 수 없다.

### 10-C. 우리 쪽 단서
- §7-B 의 배수는 장부 정의 미확인 상태의 **차수 비교**다.
- §7-A 행 12 (li2s) 는 외부 1저자 트랙 — **잠정 해석**이고 그 트랙의 판정이 아니다.
- 이 편의 어떤 문장도 우리 σ·D·Ea·W 값을 바꾸지 않는다. 바꾸는 것은 **서술의 근거와 우선순위**뿐이다.

---

## 11. 기술 용어 미니 사전

| 용어 | 뜻 (한 단계씩) |
|---|---|
| PES (퍼텐셜 에너지 면) | 원자 좌표 → 에너지 한 숫자. 미분하면 힘·응력. MLIP 는 이걸 흉내 내는 대리모형이다 |
| custom MLIP | 한 물질(좁은 화학공간)만 학습한 MLIP (ACE · GAP · MTP · Allegro). 그 안에서 정확, 밖에서 크게 틀린다 |
| FP (foundation potential) = universal MLIP | 주기율표 대부분을 학습한 MLIP (M3GNet · CHGNet · MACE-MP · UMA). 어디서나 "그럭저럭", 정량은 fine-tune 이 필요할 수 있다 |
| fine-tune | FP 를 내 계의 소량 DFT 데이터로 추가 학습. 일반성과 정확도의 절충 |
| δ-학습 | 싼 방법(예: tight-binding)의 오차만 ML 로 보정 |
| softening (PES 연화) | FP 가 DFT 보다 힘·곡률을 작게 내는 계통 편향 (ref 104). 우리는 원소별 힘 기울기로 잰다 (1 보다 작으면 무름) |
| OOD (분포 밖) | 학습 데이터에 없던 구조. FP 의 큰 오차가 주로 여기서 난다 |
| committee / conformal | 여러 모델의 의견 차이로 불확실성 추정 / 보정된 신뢰구간을 주는 통계 틀 |
| Haven 비 H = D*/D_σ | 추적자 확산과 전하 확산의 비. H < 1 이면 상관 홉이 전도를 **돕는다** → NE(H=1 가정)가 σ 를 과소평가 |
| Green–Kubo | 속도(또는 전류) 자기상관을 적분해 수송계수를 얻는 법. 교차항까지 넣으면 Haven 을 직접 얻는다 |
| 관측창 Ea_max | 길이 t 인 궤적이 원리적으로 볼 수 있는 최대 장벽 ≈ kT·ln(ν₀t) |
| GPU-h · atom⁻¹ · step⁻¹ | 원자 하나를 MD 한 스텝 미는 데 드는 GPU 시간. 이 편 `Table S3` 의 공통 단위 |

---

## 12. 🗨️ Q&A 로그

(아직 없음)

---

## 13. 📥 이 편에서 받아야 할 논문 (우선순위)

1. **ref 104** Deng, Choi, Zhong, …, Persson, Ceder, *"Systematic softening in universal machine learning interatomic potentials"* npj Comput. Mater. 2025, 11, 9 — 우리 원소별 기울기와 같은 정의인지 대조 (litdb 에 독립 digest 없음; zhang2026 · dutra2025 · wu2026 digest 가 2차 언급).
2. **ref 84** Du, Hui, Zhang, Wang, *"Universal MLIPs are Ready for Solid Ion Conductors"* arXiv 2025 — RT 직접 시뮬레이션 주장의 1차 근거.
3. **ref 69** Fragapane & Deringer, *"Li−P−S Electrolyte Materials as a Benchmark for MLIPs"* JCTC 2026 — 우리 계(Li–P–S)의 벤치마크.
4. **ref 12** Qi … Ong, *"Bridging the gap between simulated and experimental ionic conductivities in lithium superionic conductors"* Mater. Today Phys. 2021.
5. **ref 62** Banerjee & Tkatchenko, *Nat. Commun.* 2025 — 비국소 상호작용이 Li 확산을 정한다 (functional 축).
6. **ref 85** Usler … De Souza, J. Comput. Chem. 2023 — D 통계오차 일반식 (우리 MSD 창 오차막대의 외부 앵커 후보).
7. **ref 146 / SI S3** Ou … Grabowski, PRMaterials 2024 — LPSCl GB (우리 `ou2026_…` 의 선행편).
8. **ref 155** Majumdar … Gómez-Bombarelli, arXiv 2026 — FP 간 자유에너지 재가중 합의 (위원회 대안).
9. **ref 64 · ref 65** Kuryla 2025 (DFT 힘 불확도) · Warford 2026 (*Better without U*).

---

## 14. 한 줄 결론

이 편은 **우리가 이미 원장에 박아 둔 규율의 "필드 대표 그룹 버전"** 이다 — 방향은 거의 다 같고(FP 먼저 · ab initio 검증 · 계면/SEI/유리 경고 · 고온 외삽 경고), **정량 규칙은 우리가 더 많다**. 새로 가져올 것은 ① `Table S1` 하한으로 우리 셀·창을 점검하는 습관 ② `Fig. 1b` 셈법을 비용 견적의 1차 기준으로 쓰되 작은 셀은 4–8× 보정 ③ 400/500 K 제외 사유를 다시 분류하는 것이다. **Haven 문장과 ref 153 은 인용하지 않는다.**

---

**관련 digest**: `chang2026_performance_based_mlip_selection_sse` · `makino2026_mlip_battery_materials_review` · `liu2026_finetuning_umlip_tutorial` (= 이 편 ref 48) · `tompa2026_finetuning_mlip_foundation_strategies` · `petmad2026_lightweight_universal_interatomic_potential_mad` · `lynch2026_greenkubo_mlip_conductivity_thesis` · `zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill` · `wu2026_ml_driven_electrolyte_interface_design_review` · `jang2025_thioarsenate_argyrodite_mlip_mechanism` · `li2026_mci_vs_sei_na3ps4_na_mlip_md` · `choi2025_mlip_cu_taxn_interfacial_adhesion` · `he2018_statistical_variances_diffusional_aimd` (= SI S2 · ref 87) · `marcolongo_ionic_correlations_failure_nernst_einstein` (= ref 93) · `wang2022_resistive_decomposing_interfaces_se_alkali_metal` (= ref 15·94) · `ou2026_microstructural_multiscale_fast_ion_transport` · `grasselli2025_uncertainty_era_ml_atomistic` · `dutra2025_atomistic_modelling_ml_se_review`
