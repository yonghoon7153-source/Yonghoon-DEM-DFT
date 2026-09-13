# ⏸ 병합 대기 — `liu2026_ai_ready_finetuning_solid_solid_interfaces`
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 2026-09-09 · litdb-curator 다중 동시 실행으로 **`INDEX.md`·`comparison_vs_ours.md` 직접 수정 금지**를
> 받아, 넣어야 할 내용을 여기 적어 둔다. 충돌이 풀리면 **아래 두 블록을 그대로 옮기고 이 파일을 지운다.**
>
> ⚠ 이 편은 **arXiv preprint (2601.17847v1, 2026-01-25) · 동료심사 안 됨** — 옮길 때 그 표기를 지우지 말 것.
> ⚠ **SI (S.1–S.4) 미확보** — 계면 구조 생성·DFT 설정·MD 온도가 전부 SI 로 미뤄져 있다. SI 를 받으면 digest §6·§7-1 재작성 필요.
> ⚠ **형제편 `liu2026_finetuning_umlip_tutorial`(J. Appl. Phys., 48 pp) 동시 진행 중** — 병합 시 상호참조 링크를 양쪽에 건다.

---

## ① `INDEX.md` 에 추가할 행

| `papers/liu2026_ai_ready_finetuning_solid_solid_interfaces.md` | **[외부·methods·★계면 MLIP 파인튜닝 레시피 편 · ⚠ PREPRINT]** **Xiaoqing Liu**†‡, **Xinyu Yu**¶§, **Yangshuai Wang**∥ (공동1저자 3인), Z.-T. Sun, Z. Luo, K. Zeng, **Teng Zhao\***, **Shou-Hang Bo\***, **Zhenli Xu\*** (**SJTU** 수학/Future Battery Research Center/충칭 AI 연구원 + **NUS 수학** + **SOG AI-Technology Co. Ltd.**), "**An AI-Ready Fine-Tuning Framework for Accurate Machine-Learning Interatomic Potentials in Solid–Solid Battery Interfaces**" (**arXiv 2601.17847v1** [cond-mat.mtrl-sci], **2026-01-25** · **DOI 없음 · 동료심사 안 됨** · 본문 21 pp 중 **참고문헌 8 pp** · Fig **4개** · **본문 Table 0개** · refs 61 · **SI S.1–S.4 우리 미확보**) — **제안 = FIRE(Fine-tuning with Integrated Replay and Efficiency)**: ① **replay**(에폭마다 사전학습 데이터 sub-sample + task mini-batch 를 **같이** 먹여 catastrophic forgetting 억제) + ② **표본추출 자동화**(perturbed **20–50개**로 pre-fine-tuned 모델 → MD 로 **~20,000 구조** → **SOAP(DScribe)→PCA→K-means** → 최종 **500–4,000 프레임**). 백본 = **MACE-MP-0 단독**. **★★ UMA·fairchem·OMat·eSEN 전문 0회** (유일한 "uma" 는 참고문헌 저자명 *Ne**uma**nn*) ⇒ ⛔ *"이 논문이 UMA 를 검증했다"* 인용 금지. **★ 능동학습 안 씀** — `active learn`/`uncertain` 각 1회이고 **둘 다 결론의 미래과제 문장**이다. **계 6종**: Na/Na₃SbS₄ · LiCl/GaF₃ · Li₂CO₃/LiF · **Li₃PS₄/Li₃B₁₁O₁₈**(황화물‖붕산염 코팅) · **Li/Li₆PS₅Cl** · LLZTO(M=Ta,Nb). 🔴 **"6종 계면" 은 과장** — 저자 자신이 LiCl/GaF₃·LLZTO 를 *"disordered solid electrolyte"* 로 분류하고, `Fig. 2` A 에서 **LLZTO 는 두 번째 상이 아예 없다**(도핑 벌크) ⇒ **실질 계면 4종**. **★★ 정확도 (`Fig. 2` C, 막대에 인쇄된 값 = figure-read 아님) FIRE/Vanilla/Reference**: E RMSE meV/atom = Na/Na₃SbS₄ **0.34**/0.71/15.66 · LiCl/GaF₃ **0.10**/0.12/1.00 · Li₂CO₃/LiF **0.19**/0.65/0.74 · **Li₃PS₄/Li₃B₁₁O₁₈ 1.04**/1.71/21.23 · **Li/Li₆PS₅Cl 0.86**/1.29/5.45 · LLZTO **0.11**/0.18/2.04 ‖ F RMSE meV/Å = **18.56**/23.23/61.92 · **18.28**/22.41/70.00 · **13.47**/26.88/50.00 · **54.18**/74.82/216.35 · **43.02**/55.47/93.90 · **8.50**/15.65/107.00. 🔴 **초록이 자기 그림과 모순**: *"below 1 meV/atom"* → **1.04 존재**, *"force near 20 meV/Å"* → **43.02·54.18 존재**하고 "near 20" 은 6계 중 3계뿐 — **낙제한 두 계가 하필 황화물 = 우리 화학** ⇒ ⛔ **"FIRE 로 LPSCl 계면 20 meV/Å" 인용 금지, 실제 43**. ✅ **가장 방어 가능한 결론 = replay 가 vanilla 보다 6계 전부에서 낫다**(E 1.2–3.4× · F 1.2–2.0×, 같은 데이터·같은 백본의 통제 A/B). **★★ 데이터 효율 (`Fig. 3`)**: 표본추출 비용이 파인튜닝의 **0.3–0.4 %**(sampling 2–3 min vs fine-tuning **13–18 h @ n=4000**, ⚠ **하드웨어 미기재·DFT 라벨링 비용 부재**) ⇒ **PCA+K-means 는 공짜, 안 쓸 이유 없음**. 🔴 **본문의 *"lowest RMSEs across all data sizes"* 는 `Fig. 3` C 가 반증** — n≈100 에서 **FIRE 0.86 > Random 0.42**(2배 나쁨)이고 n≥2000 에서 FIRE≈Random(4000 에서 0.14 vs 0.145, 힘 8 vs 8 **동일**) ⇒ **다양성 표본추출 이득은 계 의존**: 단순 매니폴드(Na/Na₃SbS₄)는 무작위로 충분, **다클러스터(LLZTO)에서만 3배 이긴다**(E 0.20 vs 0.60 · F 16 vs 25 @4000). **★ `Fig. 3` B figure-read 소득**(캡션에 없는 것): **LLZTO PCA 의 왼쪽 클러스터가 n=500 에서 통째로 비어 있다** ⇒ K-means 다양성 선택이 상(相)을 통째로 놓칠 수 있다 — 우리가 쓰면 **클러스터별 최소 할당(stratified) 강제**. **★★★ 무엇을 검증하나 = 🔴 계면 물성 0건**: 전문 `work of adhesion` 0 · `adhesion` 0 · `interfacial resistance` 0 · 계면 Li 이동 0. **학습은 계면 6종, 검증(`Fig. 4`)은 벌크 3종**(T-Na₃SbS₄ · LLZTO · LPSCl). **계면층/벌크층 분리 RMSE 도 없다** ⇒ 초록의 *"accurate MLIPs in solid–solid interfaces"* 가 **현재 데이터로 뒷받침되지 않는다**. **벌크 수송 (`Fig. 4` A)**: LPSCl D=4.29×10⁻¹¹ m²/s · σ_MD **0.75** vs σ_EIS **0.89** mS/cm(−16 %) · LLZTO 5.24×10⁻¹²·0.24 vs 0.31(−23 %) · T-Na₃SbS₄ 1.74×10⁻¹¹·0.14 vs 0.13(+8 %). **MSD 창 = 50–200 ps(LPSCl·LLZTO) / 100–500 ps(Na₃SbS₄)** — 우리 규약 **2–50 ps** 와 다름. 🔴 **MD 온도가 본문 어디에도 없고 캡션(*"at relevant temperatures"*)과 본문(*"room-temperature MSD"*)이 모순**, 게다가 **우리 검산에서 인쇄된 D 와 인쇄된 σ 가 Nernst–Einstein(H_R=1, 300 K)으로 30–120배 어긋난다**(LPSCl 89× · LLZTO 32× · Na₃SbS₄ 124×; ⚠ 격자상수·이온수는 **우리가 문헌값으로 넣은 것**이라 "저자가 틀렸다"가 아니라 **"본문 정보로 재현 불가"**) ⇒ ⛔ **D 값 이식 금지**. ✅ **MSD→D 사슬 자체는 자기정합**(LLZTO 적합선 기울기 3.07×10⁻¹¹ m²/s ÷6 = 5.1×10⁻¹² ≈ 인쇄값 5.24×10⁻¹²). **`Fig. 4` 전체에 오차막대 0 = 계당 궤적 1개**(우리 3-seed ±16 % 규율과 대조). **역학 (`Fig. 4` B, figure-read ≈)**: E(GPa) FIRE/실험 = Na₃SbS₄ **31/28**(+11 %) · LLZTO **156/127**(+23 %) · **LPSCl 26/40(−35 %, 최악이자 우리 계)** ‖ ν FIRE/Reference = 0.27/0.31 · 0.26/0.26 · 0.34/0.37. ⚠ **축이 섞였다** — E 는 **AFM 나노역학 맵 공간평균**(기공·입계·접촉모델 포함)이고 ν 는 **문헌 계산값**인데 같은 그림에 "Experiment"/"Reference" 로만 라벨을 바꿔 나란히 둔다. ⚠ ν 의 Na₃SbS₄ 앵커(ref 55)는 **뉴로모픽 메모리 학회 포스터**다. **`Fig. 4` C 스케일링**: MACE-MD **1.3→1.4 s/step (16→3456 원자, 사실상 평평)** vs VASP-MD 1.0→**195 s/step (16→576)**, DFT 는 메모리로 ~600 원자 한계. **figure-read: 16 원자에선 VASP 가 더 빠르다**(교차 30–60 원자) — 평평함은 확장성이 아니라 **오버헤드 지배**의 신호이고 1.3 s/step 이면 200 ps 궤적에 **36 h**. **🔴 재현 불가**: functional(`PBE` 0회)·k-mesh·ecut·supercell·PAW·**replay 비율**·**동결 층수**·학습률·에폭·**MD 온도/앙상블/dt/시드** 전부 본문에 없다(VASP 는 `Fig. 4` C 문맥 1회). **무질서 처리(SQS/enumerate) 도 미기재**. **🔴 계면 구조 생성 규약 완전 부재**: `strain` 0 · `lattice` 0 · `termination` 0 · `slab` 0 · `vacuum` 0 · `supercell` 0 · `mismatch` **1회(서론 동기 문장뿐)** ⇒ **★ 우리 B2 보고량 정의에 그대로 쓸 수 있는 항목 0개**(§12-2 항목별 표). 이 편은 *"초기 계면을 어떻게 짓나"* 가 아니라 *"이미 지어진 계면에서 학습 프레임을 어떻게 고르나"* 를 푼 논문이다. 🔵 **B2 에 쓸 수 있는 것 딱 하나 = "상태를 하나 고르지 말고 분포째 학습·보고하라"** 는 태도(**우리 해석**이지 저자 주장 아님) ⇒ `X_B2` 를 스칼라가 아니라 `median{W_ad} ± MAD, n=k seeds` 로 재정의. **"AI-ready" = 규격이 아니라 수사** — ref 42(Feng 2023 로봇 AI-Chemist)를 인용할 뿐 스키마·API·메타데이터·라이선스 0 ⇒ 이식 가능한 것은 파이프라인 순서뿐. **저자 자기 한계 절 0개**. **⚠ 이해상충 참고**: "이해상충 없음" 선언이나 교신저자 1인이 **SOG AI-Technology Co. Ltd.** 소속. **그림 4/4 전부 실제 열람** + `Fig. 4` A/B·`Fig. 3` C-left 고해상도 재크로핑 판독. **SI 그림 S1–S3·Table S1–S2 는 파일 부재로 미열람.** | **방법론(계면 MLIP 파인튜닝)·⚠ preprint·계면 물성 검증 0건** 🔧 |

---

## ② `comparison_vs_ours.md` 에 추가할 블록

> ⚠ **배치 판단**: 이 편은 **LPSCl 물성값을 실제로 낸다**(σ·E·ν·D) — 그래서 순수 방법론 원전
> (shapeev2016 · park2024 · grasselli2025 선례)과 달리 **A·C 축에 행을 넣을 자격은 있다.**
> 다만 **① 온도 미기재(D) ② E 의 실험 축이 AFM 공간평균 ③ 오차막대 0** 이라 **전부 조건부**다.
> 아래 A·C 두 행 + `🔧 방법 원전` 블록을 같이 넣는다.

### ②-a 축 A (이온전도) 에 추가할 행

| 문헌 | 계 | 문헌값 | 우리값 | 판정 |
|---|---|---|---|---|
| **[Liu26FIRE]** `liu2026_ai_ready_finetuning_solid_solid_interfaces` ⚠preprint | **LPSCl 벌크** (계면 아님) | MLIP-MD **σ 0.75 mS/cm** / 자체 EIS **0.89 mS/cm** · **D 4.29×10⁻¹¹ m²/s** · MSD 창 **50–200 ps** · **온도 미기재** · 오차막대 0 | ⛔ 우리 절대 σ 인용 금지 규율 · D 3.09×10⁻⁶ cm²/s **@600 K** · MSD 창 **2–50 ps** · 600 K **3-seed** | 🔴 **직접 비교 불가**. ① 저쪽 MD 온도 미상 ② 창이 다름 ③ 인쇄 D↔인쇄 σ 가 NE 로 **89배** 어긋남(우리 검산) ⇒ **소환값으로도 이식 금지**. ✅ 얻을 것은 **σ_MD vs σ_EIS 를 같은 논문에서 −16 % 로 맞춘 워크플로**뿐 |

### ②-b 축 C (기계) 에 추가할 행

| 문헌 | 계 | 문헌값 | 우리값 | 판정 |
|---|---|---|---|---|
| **[Liu26FIRE]** ⚠preprint | **LPSCl 벌크** | **E_MLIP ≈ 26 GPa** (figure-read, `Fig. 4` B) vs **E_AFM ≈ 40 GPa** · **ν 0.34** vs ref 0.37 | **E_VRH(comp1) 22.06 GPa** (DFT relaxed-ion) · modelc 27.66 | 🟠 **우리 DFT(22.1) 와 저쪽 파인튜닝 MLIP(26) 이 서로 가깝고, 저쪽 "실험"(40) 만 둘 다에서 멀다** ⇒ 차이의 주범은 모델이 아니라 **측정량**: AFM 공간평균은 **다결정 펠릿의 기공·입계 + 접촉모델(Hertz/DMT)** 을 타므로 **단결정 DFT C_ij 와 같은 양이 아니다**. ⛔ *"우리 E 가 실험보다 낮다"* 를 이 논문으로 논증 금지. ✅ **실측 앵커는 계속 `lee2026`(AFM-FS, 우리 랩) 이 정본** |

### ②-c `🔧 방법 원전` 절에 추가할 블록 (**이 편 가치의 8할이 여기다**)

**[Liu26FIRE] `liu2026_ai_ready_finetuning_solid_solid_interfaces` — 계면 MLIP 파인튜닝 레시피**
(⚠ **arXiv preprint, 동료심사 안 됨** · **SI 미확보** · **계면 물성 검증 0건**)

| 항목 | [Liu26FIRE] 가 답하는가 | 우리 현재 | 판정 |
|---|---|---|---|
| **★★ 계면 구조를 어떻게 만드나** (격자정합·변형률·종단·배향·gap·표본수) | ❌ **본문에 0줄** (`strain`/`lattice`/`termination`/`slab`/`vacuum` 전부 0회) | `run_cathode_interface.py` — SE 를 NCM xy 에 **한쪽 몰빵 변형**, `GAP=2.5 Å` 고정, `VACUUM=30 Å`, xy-shift 5 seeds, strain 0.2/1.1/3.3 % | 🔴 **B2 에 이식할 항목 0개.** 이 편은 *"계면을 어떻게 짓나"* 가 아니라 *"지어진 계면에서 프레임을 어떻게 고르나"* 를 푼다 |
| **B2 미정의(회신 BJ) 를 닫아 주나** | ❌ | `X_B2(M) = W_ad(NCM‖LPSCl:M) − W_ad(NCM‖LPSCl)` = 🔴 **미정의** (admissible state 다수·선택규칙 없음·`rng` 미지정으로 `Wad_std` 재현 불가) | 🔴 **안 닫힌다.** 🔵 단 **"고르지 말고 분포로 정의"** 방향은 얻는다 → `median{W_ad} ± MAD, n=k` + strain 배분·gap·종단을 **결과 보기 전에 선언** |
| **★★ 계면에서 무엇을 검증하나** | 🔴 **힘·에너지 RMSE 에서 멈춘다.** W_ad·계면저항·계면 Li 이동 전부 0. **계면층/벌크층 분리 RMSE 도 없다** | `adhesion.json` γ_SE 1.211 J/m² · Wad v2 1.107±0.027 | 🔴 **대조군 없음.** ⇒ **우리가 계면 MLIP 을 하면 `RMSE(계면층)/RMSE(벌크층)` 분리 보고를 반드시 넣는다** (이 편의 최대 결함을 우리가 피하는 방법) |
| **★ 계면 fine-tune 이 필요한가 / UMA 를 그냥 믿어도 되나** | 🔴 **답 없음.** **UMA·fairchem·OMat 0회**. 게다가 **MACE-MP-0 zero-shot 의 계면 오차 자체를 안 쟀다** (`Reference` 막대는 **문헌의 다른 전용 MLIP** 값) | UMA-s-1p1(omat) — **벌크 규약으로만** 검증, 계면 미검증 | ⛔ *"파인튜닝 없이는 계면에서 못 쓴다"* 인용 불가. 🔵 **약한 방향 신호**: 6계 중 **황화물 2계가 파인튜닝 후에도 최악**(43·54 meV/Å) ⇒ 황화물 계면이 이 종류 모델에 어렵다. **우리 계는 직접 재는 수밖에**: `force_contrast`(UMA/MACE/SevenNet M=3)를 **계면 구조에서** 돌리는 것이 GPU 0 에 가장 가까운 진단 (⚠ grasselli2025 판정대로 **epistemic 이 아니라 오설정 대조**) |
| **★ 필요한 라벨 수** | ✅ **여기는 답이 있다**: 종잣값 **20–50** perturbed → 후보 풀 **~20,000**(라벨 불필요) → 최종 **500–4,000 프레임**. 수렴은 계 의존(단순 500 / 다상 1000–2000) | 계면 라벨 캠페인 없음 | ✅ **실무 수치 확보**: **DFT 라벨 500–2,000점 + 종잣값 20–50점** |
| **★ GPU 비용** | 🔴 **답 없음** — 하드웨어 미기재, **DFT 라벨링 비용 부재**. 있는 것은 파인튜닝 **13–18 h @ n=4000** 과 표본추출 **2–3 min**(=**0.3–0.4 %**) 뿐 | — | 🔴 **예산 산정 불가.** ✅ 얻는 것: **표본추출은 공짜** |
| **능동학습** | ❌ 안 씀. 결론의 미래과제 한 문장뿐 | `force_contrast` M=3 | ✅ **우리가 오히려 앞선다** (grasselli2025 §4.1 축) |
| **replay (이 편의 유일한 알고리즘 신규성)** | ✅ **6계 전부에서 vanilla 보다 낫다** (E 1.2–3.4× · F 1.2–2.0×), 통제된 A/B | 파인튜닝 안 함 | 🔵 **우리가 언젠가 파인튜닝하면 replay 는 기본값으로 넣는다** ⚠ **replay 비율이 논문에 없다**(SI) |
| **SOAP→PCA→K-means 표본추출** | ✅ 레시피 명확 · 비용 0.3–0.4 % · ⚠ 하이퍼(r_cut/n_max/l_max/PC수/k) **전부 미기재** | 없음 | 🔵 **바로 이식 가능**(의존성 `dscribe` 1개). **커버리지 그림(전체 풀 회색 + 선택 표본 색)** 은 우리도 즉시 그릴 수 있는 유일한 "학습셋 대표성" 시각화 |
| **규모 상한 (우리가 인용 가능한 유일한 정량)** | ✅ MLIP **3456 원자** / DFT-MD **~576–600 원자**(메모리) · MACE 1.3→1.4 s/step vs VASP 1.0→195 | 우리 계면 슬랩 300–624 원자 | ✅ **우리 셀 크기가 DFT 한계 바로 위**라는 것을 외부 수치로 방어 가능 ⚠ 16 원자에선 VASP 가 더 빠르다(교차 30–60) |
| **우리 계와의 겹침** | Li‖Li₆PS₅Cl(우리 comp1 + Li 금속) · Li₃PS₄‖Li₃B₁₁O₁₈(황화물‖**붕산염 코팅** = 우리 B₂O₃ 축) | Stage 11 = **황화물 SE ‖ 산화물 양극(LiNiO₂)** | 🔴 **우리 주축(SE‖NCM)은 이 논문에 없다** |

---

## ③ 병합 시 같이 할 것

1. **`liu2026_finetuning_umlip_tutorial`(형제편)이 완성되면 양쪽에 상호참조 링크**를 건다.
   분담: **일반론(파인튜닝이 무엇인가·동결 층·하이퍼파라미터·파운데이션 모델 개관) = 튜토리얼 편** /
   **계면 6종 실측 RMSE·데이터 스캔·물성 검증 = 이 편**. ⚠ **replay 비율·동결 층수**가
   튜토리얼 편에 있으면 이 digest §6 에 역참조를 추가한다.
2. **🎤 talk 역링크: 대상 없음.** `litdb/talks/lee2026_skku_mlip_materials_design.md` §99-10
   인입 대기열 6건을 확인했고 **이 논문은 그 표에 없다**.
3. **SI 를 구하면** digest §6(계산 방법) · §7-1(계면 구조 규약) · §15(못 한 것) 를 **재작성**한다.
   지금의 "❌ 없음" 은 전부 **"본문에 없음"** 이지 "논문 전체에 없음" 이 아니다.
4. `properties/` 에 해당 파일이 있으면: **넣지 않는다** — D 는 온도 미상, σ 는 우리 인용금지 규율,
   E 는 AFM 공간평균이라 우리 C_ij 와 다른 양이다. **전부 조건부라 원장에 올릴 값이 아니다.**
