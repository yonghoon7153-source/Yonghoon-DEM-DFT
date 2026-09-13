# ⏸ 병합 대기 — `liu2026_finetuning_umlip_tutorial`
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 2026-09-09 · litdb-curator 동시 실행으로 **`INDEX.md`·`comparison_vs_ours.md`·`talks/` 직접 수정 금지**를
> 받아, 넣어야 할 내용을 여기 적어 둔다. 충돌이 풀리면 **아래 세 블록을 그대로 옮기고 이 파일을 지운다.**
>
> ⛔ 이 논문은 **우리 계의 물성값 0건**이다 (σ·Ea·ESW·gap·탄성 어느 것도 LPSCl 계에 대해 주지 않는다)
> → **A/B/C/D 물성 4축 표에 넣지 않는다.** `comparison_vs_ours.md` **§J-7 `🔧 방법 원전`** 에만 둔다
> (grasselli2025 · shapeev2016 · park2024 선례).

---

## ① `INDEX.md` 에 추가할 행

| `papers/liu2026_finetuning_umlip_tutorial.md` | **[외부·methods·★U-MLIP fine-tuning 실무 레시피 편]** **Xiaoqing Liu**(SJTU 수학 + SJTU–충칭 AI), Kehan Zeng, Zedong Luo, **Yangshuai Wang\***(NUS 수학), **Teng Zhao\***(SJTU 자연과학연), **Zhenli Xu\***(SJTU MOE-LSC), "**Fine-tuning universal machine-learned interatomic potentials: A Tutorial on methods and applications**" (***J. Appl. Phys.* 139, 041101 (2026)**, DOI `10.1063/5.0299305` · **CC BY** · 투고 2025-08-27 / 채택 2025-12-02 / 온라인 2026-01-26; **본문 16 pp + 부록/refs = PDF 22 pp** · **SI 없음** · Fig **11개** · Table **10개(I–X)** · refs 141 · 계산자원 **A800 80GB 단일 GPU**, CUDA 11.7 · 사사에 **KISTI** KSC-2024-CRE-0513) — **Tutorial**(원저 아님). ⛔⛔ **UMA 는 다루지 않는다** — `UMA` 3회 전부 Table I 한 행·ref 41·무관 인명이고 **`fairchem` 0회**; 실제 fine-tune 된 것은 **MACE-MP-0b3 · MACE-MPA-0 · MACE-OMAT-0** 셋뿐이다(⚠ **MACE-OMAT-0 ≠ UMA**: 전자는 MACE 아키텍처 + OMat24 데이터, 우리 UMA-s-1p1 은 eSEN + fairchem — 데이터 계보만 겹친다). **`argyrodite` 0회 · 할로겐 전해질 0건 · 무질서(site disorder) 0건.** **★★ 요청 전제 2개가 사실과 다르다**: ① *"A comprehensive benchmark to determine the optimal…"* 는 **초록이 아니라 §II A 2** 이고 문장 전체가 *"…is **still lacking**, but future work will aim to provide such guidance"* = **논문이 없다고 선언하는 공백** ② *"generalizability deterioration"* 은 초록에 없고 `deteriorat*` 는 논문 전체 **1회**, 그것도 *"**batch size larger than 20** … tends to deteriorate the generalizability"* = **배치크기 경고**. 논문 주장은 정반대(*"fine-tuning **maintains, rather than degrades**, generalization"*). **★★ 우리에게 값진 소득 5개**: ①**실물 하이퍼파라미터**(repo 실측 `examples/Mo/run_finetune_Amir_Mo.sh`) `energy_weight 1.0 / forces_weight 10.0 / stress_weight 0.0 / loss universal / lr 5e-4 / batch 4 / max_num_epochs 150 / ema_decay 0.99 / weight_decay 1e-6 / clip_grad 10 / float64 / num_samples_pt 500 / swa_lr 5e-4 / swa_energy_weight 100.0` — 논문 Listing 1 은 PDF 에서 **이미지**라 텍스트 추출 불가, **저장소가 정본** ②**ablation 효과크기 20:18:1**(Table V, LGPS, 3시드): `forces_weight 1→100` 힘 RMSE **18.71→14.80 (−20.9%, 단 1→10 에서 −15.6% 를 다 먹는다)` · `lr` U자 최적 1e-3 (18.52↔15.24, −17.7%) · `ema_decay` **−1.1% 뿐** ⇒ 🔴 논문은 셋을 동급으로 제시한다 ③**Mo 탄성 연화 정량**(Table VI): 파운데이션이 **C₁₁ −45.32%**(251 vs DFT 459 GPa)·**C₄₄ −51.55%**(47 vs 97)·B −19.85%(210 vs 262) → FT 가 452/82/267 로 회복 = **uMLIP PES softening 의 최초 정량 근거**(우리 `talks/lee2026_skku…` 슬 8 A1 의 정본) ④**데이터효율**(Fig. 4, figure-read): 힘 RMSE ≈18.3(10%)→≈14.85(100%) — **10× 데이터로 19% 개선**, 심한 수확체감 ⑤**LGPS σ_F = 840.3 meV/Å** — repo `.npy` 로 직접 잰 값이 Table IV/V 의 `RMSE_F/(Rel.F/100)` 역산 평균과 **소수점까지 일치**(digest 계산) ⇒ repo 데이터 = 논문 데이터 확정. **🔴 논문 내부 불일치 6+4건**: ①**에너지 RMSE 가 정확히 10× 다르다** — Fig. 2(c) 테스트 **3.2 meV/atom** ↔ Table IV **0.32**, Fig 2(e) **2.8** ↔ **0.28**, 그런데 **힘은 완벽 일치**(16.2↔16.15, 15.8↔15.84) ⇒ ⛔ **이 논문의 절대 에너지 RMSE 인용 금지**(상대 개선폭만) ②**Table VI 본문↔표**: 본문 45.91→2.58 / 56.88→**14.77** / 48.27→3.45(실험 기준) ↔ 표 45.32→1.52 / 51.55→15.46 / 43.33→6.67(DFT 기준), **표에 실험 열이 아예 없다**(digest 계산 역산: C₁₁≈464 GPa · C₄₄=109 · ν=0.29), C₄₄ 의 **14.77% 는 24.77% 오타로 보임** ③Table VI 캡션이 없는 열(tabGAP·NNIP) 열거 = 타 논문 캡션 복사 ④**Fig. 4 가 본문을 반증** — *"consistently lower errors than training-from-scratch"* 인데 **75%·100% 힘 RMSE 에서 scratch(≈15.0/≈14.55)가 세 FT 모델(15.6–16.45 / 14.85–15.85)을 전부 이긴다**(figure-read) ⑤**Table VIII 가 본문을 반증** — *"consistently lower elapsed times"* 인데 **128원자에서 cuEq 가 더 느리다**(710 > 658); §II A 3 의 *"factor of 3–10"* 가속 ↔ 실측 최대 **1.94×**(2900원자 5084→2619 s) ⑥**MD 시간이 세 값** — 본문 **200 ps** / repo `run.py` **10 ps** / Fig. 9(a) x축 **2 ps** ⑦라이브러리명 **cuEquivalence** → 정확히는 **cuEquivariance** ⑧Table III 권장 상한 `forces_weight ≤ 20` ↔ 자기 최적 **100** ⑨repo README 가 clone 주소를 **`YangshuaiWang/…`** 로 안내(본문 정본은 `John2021-hub/…`), BibTeX `author={}` 공란·year 2023 ⑩**LiGePS 예제에 fine-tune 스크립트가 없다**(readme 는 있다고 적어 놨으나 실제로는 `deepmd2mace.py` 뿐) = **우리 계에 제일 가까운 예제의 레시피가 빠져 있다**. **★ repo 실측 (clone 3/3 성공)**: `John2021-hub/mace-ft-tutorial`(401파일, 모델 3종 79.5MB씩, **LGPS 원데이터 6550 프레임** = data.init 50원자 3260 + 400원자 1704 + iter.000000–2 각 ≈528) · `ACEsuit/mace` **v0.3.17 @ 59ad3a4** · `BingqingCheng/cace-lr-fit`(178파일, **CC BY-NC 4.0**, UC Berkeley 가 Latent Ewald 가출원 — 논문의 **마지막 두 예제 데이터 출처**이자 비교기준선). **🔴 repo 실측으로만 잡히는 결함 2건**: ①**튜토리얼 스크립트는 사실상 single-head 로 돈다** — `run_train.py` 의 `if args.foundation_model not in ["small","medium","large"] and args.pt_train_file is None: args.multiheads_finetuning = False` 때문에, **경로**로 파운데이션을 주고 `--pt_train_file` 이 없는 튜토리얼 명령은 multi-head 가 **조용히 꺼지고** `--num_samples_pt=500` 이 **무효**가 된다 ⇒ 논문이 §II A 2·§III B 에서 강조한 **forgetting 완화 장치가 배포 스크립트에서 작동하지 않는다** ②**multi-head 를 켜면 lr 이 덮어써진다** — `if not args.force_mh_ft_lr: args.lr=0.0001; args.ema_decay=0.99999` ⇒ **Table V 의 최적(lr 1e-3, ema 0.999)과 multi-head 는 기본설정에서 양립 불가**. ⚠ 둘 다 **v0.3.17 기준**, 저자 사용 버전(2025)에서 달랐을 수 있음. **★★ 우리 질문 4개에 대한 판정**: ⓐ**UMA fine-tune 불가** — `run_train.py` 가 `model_foundation.r_max.item()`·`.interactions[0].avg_num_neighbors` 를 읽고 `load_foundations_elements_default()` 가 MACE 블록에 가중치를 복사한다 = **아키텍처 하드락**(`mace/tools/fairchem_dataset/` 는 fairchem **LMDB 데이터** 어댑터이지 UMA **모델** 로더가 아니다) ⇒ **레시피 문서로는 쓰고 실행경로로는 못 쓴다** ⓑ**M ≥ 4 snapshot committee 안 된다** — `--keep_checkpoints --save_all_checkpoints` 로 파일은 최대 150개(`<tag>_epoch-<N>.pt`, stage2 는 `_swa` 접미) 만들 수 있으나 **네 가지가 준독립성을 깬다**: EMA 평활(저장이 `with ema.average_parameters():` 안, `decay 0.999` 유효창 ≈1000 스텝) · `kurniawan2025` 의 **100-epoch 간격** 요건(150 epoch 런에서 **최대 2개**) · stage1/2 **목적함수 불일치**(swa_energy_weight 100) · **순환 LR 부재**(MACE 는 `ExponentialLR`·`ReduceLROnPlateau` 둘뿐 — Huang 2017 의 cyclic restart 가 없다) ⓒ**일반화 저하는 이 논문이 재지 않았다** — Si OOD(Fig. 5, 막대 인쇄값 MPA-0 **46.69** meV/atom·**126.07** meV/Å → FT **3.88**·**52.48**, 에너지 12.0×·힘 2.4× 개선; FT vs FT-SH 는 10%/9.8%)는 **구조 OOD 이지 화학 OOD 가 아니다**(훈련도 Si, 테스트도 Si) — **fine-tune 모델을 사전학습 분포로 되돌려 평가한 표가 0건**이고 `forget*` 4회는 전부 정성적, 저자 스스로 *"important direction for **future research**"* ⓓ**학습 wall-clock 이 논문에 0줄** — Table VIII 은 MD **추론** 시간. 유일한 근거는 digest 계산 **≈2.2×10⁵ optimizer step**(train ≈5895 × 150 epoch ÷ batch 4, ⚠ **LGPS batch size 는 논문에 없어 Mo 값 가정**). **기타 실무 소득**: **E0s 는 훈련파일 안 `config_type=IsolatedAtom` 프레임으로 주입**(Mo train.xyz 에 1개, `dft_energy=−1855.3529371 eV`) · Mo train 6301 프레임 중 **62%가 nat 1–2 셀**(반발영역을 싼 다이머로 채운다) · **세 예제가 라벨 키 규약이 다르다**(MACE 기본 `REF_energy/REF_forces` ↔ Mo `dft_energy/dft_force` ↔ LGPS 변환본은 ASE 가 `SinglePointCalculator` 로 넣는 `energy/forces`) · 그래핀–물 라벨링 = **VASP PAW+PBE+D3, cutoff 400 eV, SCF 1e-6 eV**, 고전MD(Tersoff+SPC/SHAKE+LJ+Ewald, NVT) 사전평형 → 비상관 스냅샷 → 단일점 · **Fig. 9(b) 가 논문에서 가장 설득력 있는 그림**(RMSE 아닌 **구조 관측량**: 산소 수밀도 첫 봉우리 FT ≈10.8 ≈ AIMD ≈11.6 vs 파운데이션 ≈6.4 로 **40% 낮고 퍼짐**; d_gw MACE/AIMD 0.35 nm vs Exp 0.36) · MACE v0.3.17 에 **`--freeze N`·`--lora/--lora_rank 4/--lora_alpha 1.0`·`--lr_params_factors` 가 이미 있으나 논문은 전부 full-parameter** 로만 실험(동결 실측 0건) · **`--patience` 기본 2048** 이라 150 epoch 런에서 **조기종료가 사실상 없다**(stage1 에서 걸리면 종료가 아니라 stage2 로 점프) · **replay 데이터는 자동 다운로드**(`mp`→`mp_traj_combined.xyz`, `omat`→`mp_traj_combined_omat.xyz`) ⇒ KISTI 계산노드에서 **사전 캐시 필요**. **🔴 figure-read 로만 잡은 것 3건**: Fig. 4 의 scratch 역전(위 ④) · **Fig. 7 GSFE 의 부호 뒤집힘** — 파운데이션은 DFT 대비 **−60% 과소**(≈0.59 vs ≈1.475 J/m²)인데 **FT 는 +11.9%/+13.9% 과대**(≈1.65/≈1.72 vs ≈1.475/≈1.51), Table VII 은 절댓값만 줘서 이 정보가 소실된다 ⇒ 우리 슬 8 인용을 *"되돌린다"* 가 아니라 **"지나쳐 되돌린다"** 로 고쳐야 한다 · Fig. 9(a) 시간축 2 ps. **그림 6/9 열람**(Fig 1·2·4·5·7·9; **안 봄** = Fig 3·6·11 전부 원자구조 렌더링; ⚠ **Fig. 10 은 크로핑 실패** — 추출도구가 p16 을 *"그래픽 없음(img0/draw0)"* 으로 제외, **막대값 미확인**). ⚠ **실행 검증 0** — 이 환경에 `torch`·`dpdata`·`e3nn` 부재로 fine-tune 미실행, 코드는 **읽어서** 판정(`ase`·`numpy` 로 데이터 포맷만 실제 열람). **⛔ 물성 4축 편입 금지** → `comparison_vs_ours.md` **§J-7 `🔧 방법 원전`** 에만. | **방법론(MLIP fine-tuning 실무)·MACE 전용** — 우리 계 물성값 0, **UMA 미수록** · 🎤 `talks/lee2026_skku_mlip_materials_design` 슬 8(A1 PES softening) 의 정량 정본 |

---

## ② `comparison_vs_ours.md` §J-7 `🔧 방법 원전` 에 추가할 블록

**[Liu26FT] `liu2026_finetuning_umlip_tutorial` — U-MLIP fine-tuning 절차의 실무 원전 (MACE 전용)**
(⛔ 우리 계 물성값 0건. A–D 4축 행 금지. 아래는 **절차·수치 규모·판정**뿐이다.)

| 항목 | [Liu26FT] 가 주는 것 | 우리 현재 | 판정 |
|---|---|---|---|
| **다루는 모델** | MACE-MP-0b3 · MACE-MPA-0 · MACE-OMAT-0 (**셋뿐**) | **UMA-s-1p1 (omat), fairchem, 고정 체크포인트** | 🔴 **아키텍처 불일치.** `UMA` 는 Table I 한 줄, 실험 0건. ⚠ **MACE-OMAT-0 ≠ UMA** |
| **fine-tune 실행 가능성** | `run_train.py` 가 `model_foundation.r_max`·`.interactions[0]` 를 읽고 MACE 블록에 가중치 복사 | UMA = eSEN 체크포인트 | 🔴 **아키텍처 하드락. 이 도구로 UMA fine-tune 불가** (repo 실측) |
| **옮길 수 있는 것** | 데이터 준비(extxyz·90/10·`IsolatedAtom` E0s·rattle 0.1–1.0 Å+MC 필터·2단계 부트스트랩·1–2원자 셀로 반발영역) · **힘 가중을 크게** · lr 1e-3 근처 U자 · batch ≤20 · **RMSE 로 끝내지 말고 물성으로 재검증** | — | ✅ **레시피는 전부 이식 가능** |
| **못 옮기는 것** | `--swa_*`·`--freeze`·`--lora*`·`--pt_train_file`·`--num_samples_pt`·`start_swa=max_epochs//4*3` 자동규칙 | — | 🔴 MACE 종속. fairchem 쪽을 **따로 확인해야 한다**(이 논문은 무언) |
| **힘 RMSE 규모** | LGPS **fine-tune 후 14.88–16.15 meV/Å** (Table IV, 소환값) | `mlip_bench_li3ps4_uma.json`: **44.58 meV/Å**(zero-shot, Li₃PS₄ 243구조) | ⚠ **직접 비교 금지**(계·DFT설정·테스트셋 전부 다름). 자릿수만: **44.58/15.3 ≈ 2.9×** (digest 계산) |
| **zero-shot 출발점** | Si OOD **126.07** · LiCl/GaF₃ **179.2** · C/cBN **171.3** meV/Å | 우리 **44.58** meV/Å | ✅ **우리 출발점이 그들보다 훨씬 좋다** ⇒ 🔴 **그들의 9–10× 개선을 우리에게 기대하면 안 된다.** 상한은 **≈3×** |
| **fine-tune 이득의 조건** | 에너지: 전 구간 ✅ / **힘: 데이터 ≲30% 일 때만** — 75·100% 에선 **scratch 가 이긴다**(Fig. 4b figure-read) | — | 🔴 **본문 주장(*consistently*)이 자기 그림에 반증됨.** 갈라 인용 |
| **필요 라벨 규모** | ≈590 프레임(풀의 10%)에서 힘 RMSE ≈18.3 meV/Å; 5895 프레임(100%)에서 ≈14.85 = **10× 데이터로 19%** | Cl 라벨 **0** | 🔵 **파일럿 규모 근거 확보.** ⛔ **우리는 Cl 라벨이 없어 시작선에도 못 서 있다** |
| **탄성 연화 (PES softening)** | 파운데이션 **C₁₁ −45%·C₄₄ −52%·B −20%**(Mo, Table VI) → FT 로 회복 | 우리 E_VRH·B₀ 는 **DFT** 산출 | ✅ **DFT 값은 fine-tune 과 무관 — 안 끊긴다.** 이 행은 *MLIP 의* 연화 경고로만 |
| **연화 교정의 방향** | GSFE: 파운데이션 −60% → **FT 는 +12~14% 과대**(figure-read, Fig. 7) | — | 🔴 **"되돌린다"가 아니라 "지나쳐 되돌린다".** 슬 8 A1 인용문 수정 필요 |
| **일반화 저하(=우리 3번 질문)** | ⛔ **재지 않았다.** Si "OOD" 는 **구조** OOD(훈련·테스트 모두 Si). 사전학습 분포 되돌림 평가 **0건** | +B₂O₃ · Nd–O 공도핑 결과 다수 | 🔴 **우리에게 제일 치명적인 결측.** B/O/Nd 는 진짜 **화학** OOD ⇒ **대가를 우리가 직접 재야 한다** |
| **대가 측정기** | 없음 | `mlip_bench_li3ps4_uma.json` 243구조(Cl 없음) | 🔵 **우리는 이미 갖고 있다** — fine-tune 후 이 셋으로 되돌려 재면 그게 곧 forgetting 계측 |
| **M ≥ 4 committee** | 파일 최대 150개 가능하나 **EMA 평활 · 100-epoch 간격(→최대 2개) · stage1/2 목적함수 불일치 · 순환 LR 부재** 로 준독립성 4중 위반 | `force_contrast` M=3 (이종) | 🔴 **`grasselli` 식 (27) 의 M≥4 출구가 이 문서로는 안 열린다.** 400+ epoch·EMA off·순환 LR 이라는 **별도 설계**가 필요 |
| **학습 비용** | ⛔ **wall-clock 0줄.** step 수만 digest 계산 ≈2.2×10⁵ | — | 🔵 파일럿 첫 측정항목 = **우리 GPU 의 1 step 시간** |
| **MD 추론 가속** | cuEquivariance: 2900원자 **1.94×**(5084→2619 s/10k step), scaling 0.76→0.41. **128원자에선 더 느림** | 우리 셀 400–1000원자 | ✅ **이득 구간 안**. ⚠ 논문 본문의 *"3–10×"* 는 자기 표와 안 맞음 |
| **비교군 보존** | Table IV 에 **zero-shot 행이 없어** LGPS 개선폭을 알 수 없다 | — | 🔵 **우리는 반복하지 않는다** — fine-tune 전 대조 잡을 먼저 돌린다 |

**⛔ [Liu26FT] 에서 인용하면 안 되는 것**
1. **절대 에너지 RMSE 전부** — Fig. 2(2.4–3.2 meV/atom)와 Table IV/V/X(0.25–0.35)가 **정확히 10× 어긋나고**
   PDF 로 어느 쪽이 옳은지 확정 불가. **상대 개선폭(10.7% 등)만** 쓴다.
   (특히 LiCl/GaF₃ 의 **0.09 meV/atom** 은 DFT 수렴오차보다 작아 물리적으로 의심스럽다.)
2. *"이 튜토리얼로 UMA 를 fine-tune 할 수 있다"* — **UMA 실험 0건 + 아키텍처 하드락**.
3. *"fine-tuning 은 항상 scratch 보다 낫다"* — **Fig. 4b 가 75·100% 힘 RMSE 에서 반증**.
4. *"fine-tuning 이 일반화를 향상시킨다"를 우리 B₂O₃/Nd 계열에 적용* — 그 근거는 **동일 원소 내 구조 OOD**뿐이다.
5. Table VI 의 **본문 퍼센트**(45.91/56.88/48.27→2.58/14.77/3.45) — 기준(실험)이 표(DFT)와 다르고
   **표에 실험 열이 없으며** C₄₄ 는 오타로 보인다. 인용하려면 **표의 DFT 기준 열**을 쓴다.
6. Table VII 의 GSFE 오차를 **"개선"으로만** 서술 — 부호가 뒤집혀 **과대평가로 넘어간 것**이다.
7. 논문의 *"cuEquivariance 가 3–10× 빠르다"* — 자기 Table VIII 실측은 **최대 1.94×**.

---

## ③ `talks/lee2026_skku_mlip_materials_design.md` 에 넣을 역링크 (초안)

> ⚠ **이번 세션은 `talks/` 를 수정하지 않았다.** 아래는 충돌 해제 후 반영할 초안이다.
> ⛔ **방향은 논문 → talk 뿐.** talk 은 citable=no 이고, 어긋나면 이 논문(digest)이 이긴다.

**(a) §슬 8 / §99-4 A1 에 붙일 것**

A1 = *"uMLIP 의 PES 는 평형 근처 훈련점에 치우쳐 고에너지 영역에서 물러진다; 이를 fine-tuning 으로 되돌린다"*

⇒ **이 명제의 정량 정본이 생겼다**: `papers/liu2026_finetuning_umlip_tutorial.md` §10c.
- **연화는 실재한다**: MACE-MP-0b3 가 BCC Mo 의 **C₁₁ 을 45.32%, C₄₄ 를 51.55% 과소**평가
  (251 vs DFT 459 GPa / 47 vs 97 GPa), 벌크계수도 −19.85% (Table VI, DFT 기준 열).
- **fine-tuning 이 되돌리는 것도 사실**: 452 / 82 / 267 GPa 로 회복.
- 🔴 **그러나 "되돌린다"는 부정확하다.** GSFE(Fig. 7, figure-read)에서 파운데이션은 DFT 대비 **−60%**
  (≈0.59 vs ≈1.475 J/m², ⟨110⟩)인데 **fine-tuned 는 +11.9% 과대**(≈1.65). ⟨121⟩ 은 +13.9%.
  FT-Default 는 더 심하다(+15.3% / +23.8%). ⇒ **정정 문구: "지나쳐 되돌린다(over-correct)".**
- ⚠ **단, 이건 BCC 금속 Mo 다.** 황화물 전해질의 연화는 이 논문이 재지 않았다
  (LGPS 예제에 **zero-shot 행이 없다**) ⇒ **우리 계로의 외삽 금지.** `talks` §99-3 의
  *"T1b 는 우리가 직접"* 판정은 **여전히 유효하다.**

**(b) §12(주의/한계) 에 추가할 정정**

- 슬 8 의 fine-tuning 화살표를 인용할 때 **"연화를 교정한다"까지만** 허용.
  **"DFT 를 재현한다"는 금지** — 잔차가 GSFE 에서 **12–14%** 남고 **부호가 반대로 넘어간다**.

**(c) 위시리스트/대기열**

- 이 논문은 talks 의 *"논문 에이전트 인입 대기열"* 표에 **행이 없었다**(2026-09-09 확인,
  `grep -n -i "finetun|liu|mace|tutorial"`). ⇒ 대기열 행을 긋는 작업은 **해당 없음**.
  대신 **§99-4 A1 각주**로 거는 것이 맞다.

---

## ④ `properties/` 갱신

**해당 없음.** 이 논문은 σ·Ea·ESW·gap·탄성 어느 것도 **우리 계(LPSCl 계열)에 대해** 주지 않는다.
Mo 탄성상수(Table VI)는 **BCC 금속**이라 우리 `properties/` 어느 파일에도 걸리지 않는다.


> ⛔ **2026-09-09 정정 — 지표가 섞였다.** 여기 쓴 우리 값 **44.58 meV/Å 는 RMSE** 다.
> `db/properties/mlip_bench_li3ps4_uma.json` 실측: **MAE 29.97** / **RMSE 44.58** eV/Å×10⁻³.
> (조율 세션이 큐레이터 프롬프트에 RMSE 를 MAE 라고 넘겼다 — 내 오기다.)
> ⚠ **그냥 29.97 로 바꾸면 안 된다.** 저쪽 zero-shot 값(126.07 · 179.2 · 171.3)이
> MAE 인지 RMSE 인지 **이 digest 로는 확정 안 됐다.** 같은 지표끼리 대야 하므로,
> 저쪽 지표를 원문에서 확인하기 전까지 **배수(≈3×)는 잠정**이다.
> · 저쪽이 MAE 라면 우리 상한은 29.97/15.3 ≈ **2.0×** 로 더 내려간다
> · 저쪽이 RMSE 라면 44.58/15.3 ≈ 2.9× 가 맞다
> 어느 쪽이든 **'우리 출발점이 더 좋다 → 기대치를 낮춰라'** 는 결론은 안 바뀐다.
