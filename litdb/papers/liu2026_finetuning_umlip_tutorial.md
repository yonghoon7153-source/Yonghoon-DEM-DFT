# Fine-tuning universal machine-learned interatomic potentials: A Tutorial on methods and applications — Liu et al. (J. Appl. Phys. 2026)

> slug `liu2026_finetuning_umlip_tutorial` · DOI `10.1063/5.0299305` · type `MLIP (tutorial/benchmark)` · PDF `d32d0af1-93._Finetuning_universal_machinelearned_interatomic_potentials….pdf` · digested `2026-09-09` · status ✅
> **저자**: Xiaoqing Liu¹𝄒², Kehan Zeng², Zedong Luo², **Yangshuai Wang**³(교신), **Teng Zhao**²𝄒⁴(교신), **Zhenli Xu**⁵(교신)
> ¹상하이교통대 수학과 · ²SJTU–충칭 AI 연구원 · ³**NUS 수학과** · ⁴SJTU 자연과학연구원 · ⁵SJTU 수학과/MOE-LSC/CMA-Shanghai
> *J. Appl. Phys.* **139**, 041101 (2026) · 투고 2025-08-27 / 게재확정 2025-12-02 / 온라인 2026-01-26 · **CC BY**

> elements: Li, Ge, P, S, Mo, Si, C, H, O, Au, Mg, Al, Ti, Na, Cl, Ga, F, B, N
> methods: DFT, AIMD, MD, MLIP, elastic

---

## 0. 이 digest 를 읽는 법 — 먼저 세 가지를 바로잡는다

이 논문을 요청할 때 붙은 전제 셋 중 **둘이 사실과 다르다.** 그것부터 정리하고 시작한다.
digest 전체가 이 세 줄 위에 서 있다.

| 전제 | 실제 | 근거 |
|---|---|---|
| "48 pp" | **22 pp** (본문 16 pp + 부록/참고문헌). SI 없음 | PDF 실측 |
| "초록에 *A comprehensive benchmark to determine the optimal…*" | 초록에 **없다.** §II A 2 본문에 있고, 문장 전체는 *"A comprehensive benchmark to determine the optimal strategy under different scenarios **is still lacking**, but future work will aim to provide such guidance."* — **논문이 제공하는 것이 아니라 없다고 선언하는 공백**이다 | `optimal` 4회 전수 검색 |
| "초록에 generalizability deterioration" | 초록에 **없다.** `deteriorat*` 는 논문 전체에 **딱 1회**, 그것도 *"batch size larger than 20 … tends to **deteriorate the generalizability**"* — **배치 크기 경고**지 fine-tune 부작용이 아니다. 논문의 주장은 오히려 정반대다: *"fine-tuning **maintains, rather than degrades**, generalization"* | `deteriorat*`·`forget*`·`generaliz*` 전수 검색 |

⇒ **우리가 제일 알고 싶었던 3번(일반화 저하 정량)은 이 논문에 없다.** 있는 것은 그 반대 주장이고,
그 주장의 근거가 우리 질문에 답하지 못한다는 것이 §8 의 결론이다. 이건 논문의 결함이라기보다
**우리 질문이 이 논문의 범위 밖**이라는 뜻이다 — 그래도 답이 "없다"라는 걸 아는 게 중요하다.

그리고 하나 더, 이게 제일 중요하다:

> ⛔ **이 튜토리얼은 MACE 전용이다. UMA 는 다루지 않는다.**
> `UMA` 는 논문 전체에 3회 등장하고 전부 실질이 없다 — Table I 의 한 행, 참고문헌 41번,
> 그리고 무관한 저자 이름. `fairchem` 0회, `eSEN` 은 Table I 아키텍처 칸에만.
> **UMA 를 fine-tune 한 실험도, UMA 를 벤치마크한 표도, UMA 를 언급한 문장도 없다.**
> 실제로 fine-tune 된 것은 **MACE-MP-0b3 · MACE-MPA-0 · MACE-OMAT-0** 셋뿐이다. → §11

---

## 1. 한 줄 요약

MACE 파운데이션 모델을 **실제로 fine-tune 하는 절차**(데이터 준비 → 하이퍼파라미터 → 학습 → 검증 → LAMMPS/ASE 배포)를
코드와 함께 처음부터 끝까지 보여주고, 여섯 계(LGPS 고체전해질 · Mo 적층결함 · Si OOD · 그래핀–물 · 분자/산화물 계면 ·
고체/고체 계면)에서 fine-tune 이 **정확도·데이터효율·수렴속도**를 개선함을 보인다.
핵심 실무 결론은 **"어떤 MACE 파운데이션에서 출발하든 같은 하이퍼파라미터로 비슷한 정확도에 도달한다"**(Table IV)와
**"최적 하이퍼파라미터는 계마다 다르다"**(Table X) 두 개이고, 둘은 서로 긴장 관계다.

---

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 글의 종류 | **Tutorial** (원저 아님). J. Appl. Phys. 의 TUTORIAL 카테고리 |
| 중심 모델 | **MACE-MP-0** 계열 (MP-0b3 · MPA-0 · OMAT-0) |
| 동기 질문 | *"고정된 데이터셋이 주어졌을 때, 파운데이션을 fine-tune 할 것인가 scratch 로 새로 학습할 것인가?"* |
| 저자들의 답 | fine-tune 이 **학습시간·데이터 사용량**에서 유리하고, 정확도도 대등하거나 낫다 (⚠ §8·§10 에서 조건부로 무너진다) |
| 선행 공백 | 저자 주장: *"only one publicly available tutorial exists to date"* — 그것도 **scratch 학습** 중심이라 fine-tune 절차·하이퍼파라미터·사례 연구를 다루지 않았다 |
| 저장소 | `github.com/John2021-hub/mace-ft-tutorial` (본문·DATA AVAILABILITY 에 명시된 정본) |
| 계산 자원 | **NVIDIA A800 80 GB 단일 GPU**, CUDA 11.7, nvhpc 20.9 |
| 사사 | **KISTI** (National Supercomputing Center, KSC-2024-CRE-0513) ← 우리가 쓰는 그 센터다 |
| 이해상충 | 없음 선언 |

---

## 3. 저장소 실측 — clone 4/4 성공

**요청받은 링크 넷 중 셋을 clone 했고 전부 성공했다.** (넷째는 링크가 아니라 readthedocs 문서라 clone 대상이 아님.)
이하 `repo 실측` 은 전부 아래 커밋에서 직접 읽은 것이다.

| 저장소 | 결과 | 무엇을 얻었나 |
|---|---|---|
| `John2021-hub/mace-ft-tutorial` | ✅ clone (401 파일) | **실물 fine-tune 스크립트**·LGPS 원데이터·Mo 데이터셋·MD 스크립트 |
| `ACEsuit/mace` | ✅ clone, **v0.3.17** @ `59ad3a4` (2026-08-31) | CLI 옵션 실물·**체크포인트 저장 로직**·multi-head 분기·freeze/LoRA |
| `BingqingCheng/cace-lr-fit` | ✅ clone (178 파일) | 논문의 **마지막 두 예제 데이터 출처** — `fit-Au2-MgO-Al`, `fit-solid-LiCl-GaF3`, `fit-TiO2-NaCl-aq` |
| `mace-docs.readthedocs.io` | (문서, clone 대상 아님) | 코드가 더 정확해서 코드로 대체 |

**실행은 못 했다.** 이 환경에 `torch`·`dpdata`·`e3nn` 이 없다 (`ase` 3.29·`numpy` 만 있음).
그래서 fine-tune 을 돌리거나 `deepmd2mace.py` 를 실행하지는 못했고, **ASE 로 데이터 포맷만 실제로 열어 봤다**(§3b).

### 3a. `cace-lr-fit` 의 역할 — 경쟁자가 아니라 데이터 공급자

논문 사사에 명시돼 있다: *"we thank the author of the GitHub repository (…cace-lr-fit) for generously sharing
**the data set** that enabled our **last two numerical examples**."*
즉 CACE-LR 은 이 논문이 fine-tune 한 모델이 **아니고**, ① Au₂/MgO(Al-doped) ② LiCl(001)/GaF₃(001) ③ TiO₂–NaCl 수용액
데이터셋의 출처이자 **비교 기준선(baseline)** 이다. CACE-LR 은 *latent Ewald summation* 으로 장거리를 명시적으로 넣은 모델이고,
논문의 셀링 포인트는 **"장거리 항이 전혀 없는 MACE-FT 가 CACE-LR 을 이긴다"**(Table IX)이다.
⚠ repo 실측: `cace-lr-fit` 은 **CC BY-NC 4.0** 이고, UC Berkeley 가 *Latent Ewald Summation* 에 가출원 특허를 냈다(학술 사용 제한 없음).

### 3b. 데이터 포맷 — ASE 로 직접 열어 본 것

LGPS 원데이터(`iter.000000/02.fp/data.000/output.extxyz`, 첫 프레임):

```
nat 400 · Ge16Li160P32S192 · Lattice 17.330 × 17.330 × 25.115 Å · pbc TTT
E = −1659.8008 eV  (E/atom = −4.1495 eV)
forces (400,3) · virial 있음 · stress 없음
```

⚠ **여기서 진짜 함정 하나를 실측했다.** `deepmd2mace.py` 가 뱉는 extxyz 는 키가 `energy`/`forces` 라서
ASE 가 이걸 `atoms.info`/`atoms.arrays` 가 아니라 **`SinglePointCalculator` 로** 집어넣는다
(`atoms.info` 에는 `virial` 만 남는다). 반면 **MACE 의 기본 키는 `REF_energy`/`REF_forces`**(repo 실측,
`mace/tools/default_keys.py`)이고, 튜토리얼의 Mo 스크립트는 또 다른 `dft_energy`/`dft_force` 를 쓴다.
⇒ **세 예제가 서로 다른 키 규약을 쓴다.** Mo 스크립트를 LGPS 데이터에 그대로 복사하면 라벨을 못 읽는다.
우리가 파일럿을 짤 때 첫 번째로 막힐 지점이 정확히 여기다.

---

## 4. ★★ fine-tune 레시피 — 단계별 + 하이퍼파라미터 실물값

### 4a. 6단계 절차 (Fig. 1 + §II)

| # | 단계 | 실물 내용 | 출처 |
|---|---|---|---|
| ① | **파운데이션 선택** | MACE-MP-0 계열. **L=1(medium) 권장** — L=0 은 표현력 부족, L=2 는 효율 급락. 저자 문구: *"a medium-sized model (L = 1) provides the most balanced trade-off"* | §II C |
| ② | **데이터 준비** | 셋 중 하나: (a) **공개 데이터셋 재활용**(초심자 권장) (b) **random perturbation** — ASE `rattle`, **Gaussian 변위 0.1–1.0 Å**, 응력이 필요하면 셀 변형도 추가, 원자 과근접은 **MC 필터**로 배제 (c) **MD/MC 샘플링** — 비정질·액체용. 2단계 부트스트랩(고전 MD 로 탐색 → 일부 프레임만 DFT 재라벨) | §II B 1 |
| ③ | **E0s (고립원자 에너지)** | ⭐ *"It is **very important** to compute your own E0s"* — 최소제곱 회귀(`E0s="average"`)로 추정하지 말고 **직접 DFT 로, spin-polarized 로** 계산해 dict 로 넘긴다. MP 와 **완전히 동일한** DFT 설정일 때만 `E0s="foundation"` 허용 | §II C |
| ④ | **손실 가중** | energy : forces : stress. **힘 가중을 크게** 올리는 것이 이 논문의 핵심 처방 (→ 4b) | Table III/V |
| ⑤ | **2단계 학습** | **Stage one** (힘 중심) → **Stage two** (= SWA/stochastic weight averaging, **에너지 가중 급상승**). 두 단계 중 **검증손실이 가장 낮은 모델**을 저장 | §II C, Fig. 2 |
| ⑥ | **검증** | log 파일의 RMSE 요약표 + 자동 생성되는 **loss 곡선·parity plot**. 그 다음 downstream 물성(탄성·GSFE·밀도프로파일)으로 재검증 | §II D |

**동결(freeze) 범위 — 논문은 논하지만 쓰지 않는다.**
§II A 2 가 최적화 관점에서 세 전략을 분류한다: (i) **full-parameter** — 전부 갱신, 적응력 최대·과적합 위험 최대
(ii) **partial freezing** — 앞쪽 층/불변 특징추출기 고정, 수렴 빠르고 지식보존 좋지만 분포이동이 크면 적응 실패
(iii) **lightweight adapters** (LoRA·bias tuning) — 동결된 백본 위에 소수 파라미터만.
**그러나 논문의 모든 실험은 (i) full-parameter 다.** multi-head 에서도 *"the backbone remains trainable … Partial freezing is optional."*
⇒ **동결에 대한 실측 데이터가 이 논문에 0건**이다.

> **repo 실측 (MACE v0.3.17) — 코드에는 있다:**
> `--freeze N` (1..N 층 동결, 음수면 뒤에서부터, 기본 `None`) ·
> `--lora` / `--lora_rank 4` / `--lora_alpha 1.0` ·
> `--lr_params_factors '{"embedding_lr_factor":1.0,"interactions_lr_factor":1.0,"products_lr_factor":1.0,"readouts_lr_factor":1.0}'`
> (블록별 학습률 배율 — 부분동결의 연속판).
> ⇒ **기능은 이미 있고, 튜토리얼이 안 썼을 뿐이다.** 우리가 쓰려면 참고할 선례가 이 논문엔 없다.

**조기종료 — 사실상 꺼져 있다.**
> **repo 실측**: `--patience` 기본값 **2048**. 튜토리얼의 학습은 **150 epoch** 이므로 patience 가 발동할 수 없다.
> 게다가 코드상 stage 1 에서 patience 가 걸리면 종료가 아니라 **stage two 로 점프**한다(`epoch = swa.start`).
> ⇒ 이 레시피에 실질적 조기종료는 **없다**. "150 epoch 고정 + 최저 검증손실 모델 채택"이 전부다.

### 4b. 하이퍼파라미터 실물값

**(A) 논문 Table III — 권장 범위 (소환값)**

| 파라미터 | 뜻 | 권장 범위 |
|---|---|---|
| `energy_weight` | 에너지 손실 가중 | 1.0–20.0 |
| `forces_weight` | 힘 손실 가중 | 1.0–20.0 |
| `stress_weight` | 응력 손실 가중 | 0.0–20.0 |
| `lr` | 학습률 | 10⁻⁴–10⁻³ |
| `batch_size` | 배치 크기 | **2–20** (20 초과 비권장 — 일반화 저하) |
| `ema_decay` | EMA 감쇠 | 0.98–0.99999 |
| `swa` | SWA(stage two) 사용 | True/False |
| `swa_lr` | SWA 단계 학습률 | 10⁻⁵–10⁻⁴ |

🔴 **Table III 과 논문 자신의 결론이 모순된다.** Table V 가 고른 최적 `forces_weight = 100.0` 은
Table III 의 권장 상한 **20.0 의 5배**다. Table VII 의 GSFE 도, Table X 의 최적 설정도 전부 100.0 을 쓴다.
⇒ **Table III 을 그대로 따르면 논문의 최적값에 도달할 수 없다.** 우리가 인용할 때 반드시 갈라 써야 한다.

**(B) repo 실측 — 실제로 돌린 명령 (`examples/Mo/run_finetune_Amir_Mo.sh`)**

논문 Listing 1 은 PDF 에서 이미지라 텍스트가 안 잡힌다. **저장소의 실물 스크립트가 정본이다.**

| 플래그 | 값 | 비고 |
|---|---|---|
| `--foundation_model` | `mace-mp-0b3-medium.model` (**로컬 경로**) | ⚠ 아래 🔴 참조 |
| `--energy_weight` | **1.0** | |
| `--forces_weight` | **10.0** | Table V 최적(100)과 다르다 — 이 스크립트는 최적 이전 버전 |
| `--stress_weight` | **0.0** | **응력 안 씀** (Table VI 각주가 스스로 지적: *"can be further improved by incorporating stress observables"*) |
| `--loss` | `universal` | |
| `--energy_key` / `--forces_key` | `dft_energy` / `dft_force` | MACE 기본값 `REF_energy`/`REF_forces` 아님 |
| `--lr` | **0.0005** | Table V 최적은 0.001 |
| `--scaling` | `rms_forces_scaling` | |
| `--batch_size` | **4** | |
| `--max_num_epochs` | **150** | |
| `--ema` / `--ema_decay` | on / **0.99** | Table V 최적은 0.999 |
| `--weight_decay` | **1e-6** | |
| `--amsgrad` | on | |
| `--default_dtype` | **float64** | |
| `--clip_grad` | **10** | |
| `--seed` | **3** (변수 `SEED`) | 시드가 변수로 빠져 있다 → 다중시드 의도 |
| `--num_samples_pt` | **500** | ⚠ MACE 기본값은 **10000** — 20배 적다. 그리고 🔴 아래 |
| `--swa` | on | |
| `--swa_lr` | **5e-4** | |
| `--swa_energy_weight` | **100.0** | stage two 에서 에너지 가중 100× 상승 |
| `--swa_forces_weight` | **10.0** | |
| `--swa_stress_weight` | **0.0** | |

**(C) digest 계산 — 스케줄이 자동으로 정해지는 부분 (repo 실측 + 산수)**

`--start_swa` 를 안 주면 MACE 가 계산한다: `start_swa = max(1, max_num_epochs // 4 * 3)`.
`150 // 4 * 3 = 37 × 3 = 111` ⇒ **stage one = epoch 0–110, stage two = 111–149.**

✅ 이게 논문 Table IV 의 괄호 숫자(**110** / 146·148·149)와 **정확히 맞는다.**
⇒ **LGPS 도 `max_num_epochs=150` + 기본 `start_swa` 로 돌렸다**는 것이 산수로 확인된다 (논문은 안 밝힘).
Fig. 2 의 점선 위치(≈110)와 그래프 끝(150)도 같은 값이다 (figure-read).

**(D) 🔴 repo 실측 — 튜토리얼 스크립트의 실제 결함 두 개**

MACE v0.3.17 `mace/cli/run_train.py` 의 분기:

```python
if (args.foundation_model not in ["small", "medium", "large"]
        and args.pt_train_file is None):
    if args.multiheads_finetuning:
        logging.warning("Using multiheads finetuning with a foundation model that is not "
                        "a Materials Project model, need to provied a path to a "
                        "pretraining file with --pt_train_file.")
    args.multiheads_finetuning = False          # ← 강제 OFF
```

① **튜토리얼 스크립트는 사실상 single-head 로 돈다.** `--foundation_model` 이 `"medium"` 같은 이름이 아니라
**경로**이고 `--pt_train_file` 이 없으므로, `multiheads_finetuning`(기본 True)이 **조용히 False 로 꺼진다**.
⇒ 그러면 `--num_samples_pt=500` 은 **아무 일도 안 한다**(multi-head 재생(replay) 데이터 개수 인자이므로).
논문이 §II A 2 와 §III B 에서 강조한 **catastrophic forgetting 완화 장치가, 배포된 스크립트에서는 작동하지 않는다.**
(논문의 Si 예제는 FT(multi-head) vs FT-SH(single-head)를 비교하므로 저자들이 multi-head 를 돌린 건 맞다 —
**그 스크립트가 저장소에 없을 뿐이다.**)

② **multi-head 를 켜면 lr 이 덮어써진다.** 같은 파일 바로 아래:
```python
if not args.force_mh_ft_lr:
    args.lr = 0.0001;  args.ema = True;  args.ema_decay = 0.99999
```
⇒ `--pt_train_file=mp` 를 추가해 multi-head 를 살리는 순간 **Table V 의 최적값(lr 0.001, ema_decay 0.999)이
강제로 lr 1e-4 · ema_decay 0.99999 로 바뀐다.** 되살리려면 `--force_mh_ft_lr=True` 를 따로 줘야 한다.
**Table V 의 "최적" 과 multi-head 는 기본 설정에서 양립하지 않는다.**

⚠ 단서: 위 두 가지는 **v0.3.17(2026-08) 코드** 기준이다. 논문 투고는 2025-08 이라 저자들이 쓴 버전에서
동작이 달랐을 수 있다. 다만 경고 문구가 코드에 박혀 있다는 것은 이 가드가 오래된 것임을 시사한다.
**우리가 돌릴 때는 우리 버전에서 다시 확인해야 한다.**

**(E) 재생(replay) 데이터가 어디서 오나 — repo 실측**

`--pt_train_file` 에 `mp`/`omat`/`matpes_pbe`/`matpes_r2scan` 중 하나를 주면 MACE 가 자동으로 내려받는다:
`mp` → `mace-foundations/releases/.../mp_traj_combined.xyz`, `omat` → `.../mp_traj_combined_omat.xyz`.
사전학습 head 의 E0s 는 `"foundation"` 고정. ⇒ **인터넷 접근이 필요**하고, KISTI 계산노드에서는 미리 캐시해야 한다.

---

## 5. ★★ "optimal" 을 어떻게 정하나 — 지표와 범위

### 5a. 무엇을 최적화하나

**단 하나의 지표다: 테스트셋 힘 RMSE (meV/Å).**
Table V 의 굵은 글씨(최적)는 전부 **RMSE F** 열에서 골랐고, 논문이 명시한다:
*"the combination of forces weight = 100, lr = 0.001 and ema decay = 0.999 consistently yielded the **lowest RMSE
for force predictions**, while the energy RMSE remained essentially unchanged."*
⇒ **에너지 RMSE 는 사실상 결정에 관여하지 않았다.** downstream 물성(전도도·Ea·탄성)으로 고른 것이 **아니다.**

### 5b. 탐색 범위와 결과 (Table V, LGPS, 시드 3개 평균, 괄호=표준편차) — 소환값

| 축 | 값 | RMSE E (meV/atom) | **RMSE F (meV/Å)** | Rel. F (%) |
|---|---|---|---|---|
| **force weight** | 1.0 | 0.33 (0.01) | 18.71 (0.13) | 2.22 (0.02) |
| | 10.0 | 0.28 (0.01) | 15.80 (0.02) | 1.88 (0.01) |
| | 20.0 | 0.27 (0.01) | 15.55 (0.01) | 1.85 (0.01) |
| | 50.0 | 0.26 (0.01) | 15.11 (0.03) | 1.83 (0.06) |
| | **100.0** ★ | 0.27 (0.01) | **14.80 (0.03)** | **1.76 (0.01)** |
| **learning rate** | 0.0001 | 0.33 (0.01) | 18.52 (0.08) | 2.20 (0.01) |
| | 0.0005 | 0.27 (0.01) | 15.76 (0.03) | 1.87 (0.01) |
| | **0.001** ★ | 0.26 (0.01) | **15.24 (0.02)** | 1.81 (0.01) |
| | 0.005 | 0.28 (0.01) | 16.14 (0.04) | 1.92 (0.01) |
| | 0.01 | 0.29 (0.01) | 17.23 (0.13) | 2.05 (0.02) |
| **ema_decay** | 0.95 | 0.28 (0.01) | 15.88 (0.03) | 1.89 (0.01) |
| | 0.98 | 0.28 (0.01) | 15.81 (0.01) | 1.88 (0.01) |
| | 0.99 | 0.28 (0.01) | 15.77 (0.02) | 1.87 (0.01) |
| | **0.999** ★ | 0.27 (0.01) | **15.70 (0.01)** | 1.87 (0.01) |
| | 0.9999 | 0.31 (0.02) | 15.78 (0.02) | 1.91 (0.05) |

**읽는 법 — 축마다 실효 크기가 완전히 다르다.**
- `forces_weight` 1→100: **18.71 → 14.80 = −20.9%**. 진짜 효과. 단 **1→10 구간에서 −15.6% 를 다 먹고**
  10→100 은 −6.3% 뿐 — **수확체감**이다.
- `lr`: 최선 15.24 ↔ 최악 18.52 = **−17.7%**. U자형 (1e-4 도 1e-2 도 나쁘다).
- `ema_decay`: 최선 15.70 ↔ 최악 15.88 = **−1.1%**. 표준편차(0.01–0.03)의 6배 수준이라 통계적으론 살아 있지만
  **실무적으로는 무시해도 되는 크기**다. 🔴 그런데 논문은 이 셋을 나란히 "최적 조합"으로 제시한다 —
  **효과 크기가 20:18:1 인데 동급으로 서술한다.**
- 세 축을 **각각 독립으로** 훑었다(one-factor-at-a-time). **교호작용은 안 봤다.**

### 5c. 그 "최적" 이 옮겨가나 — Table X (소환값)

| 계 | 지표 | FT-Default | FT(최적) | Δ (%) |
|---|---|---|---|---|
| **LiGePS** | E (meV/atom) | 0.28 | 0.25 | **10.7** |
| | F (meV/Å) | 15.76 | 14.09 | **10.6** |
| | Rel. F (%) | 1.87 | 1.67 | **10.7** |
| **LiCl/GaF₃** | E (meV/atom) | 0.09 | 0.09 | **0.0** |
| | F (meV/Å) | 18.28 | 17.55 | 4.0 |
| | Rel. F (%) | 3.81 | 3.66 | 3.9 |

⇒ **최적화를 튜닝한 그 계(LiGePS)에서만 10% 이득이고, 다른 계로 옮기면 0–4% 로 죽는다.**
논문 자신의 결론: *"the optimal configuration is **case specific**."*

### 5d. 🔴 이 벤치가 우리 계와 얼마나 가까운가 — 가깝다, 그런데 딱 한 칸이 비어 있다

| | 이 논문 LGPS | 우리 |
|---|---|---|
| 조성 | **Li₁₀GeP₂S₁₂** | Li₆PS₅Cl / Li₅.₄PS₄.₄Cl₁.₆ |
| 원소 | Li, Ge, P, **S** | Li, P, **S**, **Cl** (+B,O,Nd) |
| 골격 | **티오포스페이트 PS₄³⁻** | **티오포스페이트 PS₄³⁻** ✅ 같다 |
| 관심 물성 | Li⁺ 수송 | Li⁺ 수송 ✅ 같다 |
| 셀 크기 | **400원자** (+50원자 세트) | 우리 MD 도 같은 자릿수 ✅ |
| **할로겐** | **없음** ⛔ | **Cl 이 핵심** ⛔ |
| 무질서 | (논문 언급 없음) | **S/Cl site-disorder 가 물리의 중심** ⛔ |

⇒ **이 논문 전체에서 우리 계에 가장 가까운 단일 사례가 LGPS 이고, 골격·물성·크기가 다 맞는데
정작 Cl 과 무질서가 없다.** 우리 `mlip_bench_li3ps4_uma.json` 이 **Cl 이 없다**는 문제와
**정확히 같은 구멍**이다. `argyrodite` 는 논문에 0회 등장한다.
(부수적으로 **LiCl/GaF₃** 예제에 Cl 이 나오지만 그건 이온결정 계면이지 전해질 수송이 아니다.)

---

## 6. ★★ 일반화 — 논문이 재는 것 / 우리가 묻는 것

### 6a. 논문이 실제로 잰 것 (Fig. 5, Si OOD)

Si 를 "out-of-distribution" 시험대로 삼았다. **훈련셋** = 표준 bulk + 결함 구성.
**테스트셋** = 입계(grain boundary) · di-interstitial · 적층결함 경로 · **비정질** — 무작위 분할이 아니라
**훈련에 전혀 없는 구성**으로만 채운 셋.

**Fig. 5 막대 위 인쇄값 (figure-read, 그림에 숫자가 찍혀 있어 정확)**

| 모델 | RMSE E (meV/atom) | RMSE F (meV/Å) |
|---|---|---|
| **MACE-MPA-0** (fine-tune 전) | **46.69** | **126.07** |
| Rand (무작위 5% 로 scratch) | 10.57 | 80.24 |
| AL (불확실도 필터 5% 로 scratch) | 8.34 | 71.62 |
| FT-SH (single-head fine-tune) | 4.35 | 58.16 |
| **FT (multi-head fine-tune)** | **3.88** | **52.48** |

**digest 계산**: 파운데이션 → FT 개선폭 = 에너지 **12.0×**(46.69/3.88), 힘 **2.4×**(126.07/52.48).
multi-head 가 single-head보다 에너지 **10.8%**, 힘 **9.8%** 낫다.
불확실도 기반 선별(AL)이 무작위(Rand)보다 에너지 21%·힘 11% 낫다.

### 6b. 🔴 그런데 이건 우리가 묻는 일반화가 아니다

**Si 의 "OOD" 는 *구조* OOD 이지 *화학* OOD 가 아니다.** 훈련도 Si, 테스트도 Si — 원소가 같다.
바뀐 것은 결함 종류·비정질성뿐이다.

우리가 두려워하는 것은 정반대 방향이다:
> **"LPSCl 에 fine-tune 하고 나면, 그 모델이 B₂O₃·Nd–O·다른 조성에서 예전만큼 하는가?"**
> = **사전학습 분포(OMat24 전체)에 대한 성능 유지**, 즉 진짜 catastrophic forgetting.

**논문은 이것을 한 번도 재지 않는다.** fine-tune 한 모델을 **원래 파운데이션의 테스트셋으로 되돌려 평가한 표가 없다.**
`forget` 4회 등장은 전부 **정성적 서술**이다:
- multi-head 가 *"mitigates catastrophic forgetting by preserving the performance of previously trained heads"* (근거표 없음)
- `num_samples_pt` 가 *"acts as a form of 'knowledge retention'"* (근거표 없음)
- active learning 반복은 *"can lead to catastrophic forgetting … Understanding and mitigating this effect is
  an **important direction for future research**"* ← **미해결로 명시**

⇒ **답: 얼마나 깎이는지 이 논문은 모른다. 재지 않았다.**
막는 법으로 제시된 것은 ① multi-head replay ② `num_samples_pt` 크게 ③ batch_size ≤ 20 셋인데,
①②의 **효과가 정량화된 표는 Fig. 5 의 FT vs FT-SH 한 쌍(≈10%)뿐이고 그것도 OOD-Si 안에서의 비교**다.

### 6c. 그나마 우리에게 유용한 간접 증거 (Table IX, 소환값)

| 계 | 지표 | MACE-MPA-0 (zero-shot) | FT | Baseline (CACE-LR / NEP) |
|---|---|---|---|---|
| **LiCl/GaF₃** | E (meV/atom) | 97.04 | **0.09** | — |
| | F (meV/Å) | 179.2 | **18.23** | 67.8 |
| **C/cBN** | E (meV/atom) | 48.09 | **3.72** | 7.00 |
| | F (meV/Å) | 171.3 | **18.78** | 135.3 |

**digest 계산**: 힘 개선 **9.8×**(LiCl/GaF₃) · **9.1×**(C/cBN).
논문의 자랑거리: **장거리 항이 명시적으로 없는데도** latent-Ewald 를 쓴 CACE-LR(67.8)과 NEP(135.3)를 이겼다.
저자 해석: *"large pre-trained models may **implicitly encode aspects of long-range physics** during pre-training."*
⚠ 저자 스스로 단다: *"such behavior is **case by case**"*, 그리고 Fig. 10 관련해 **zero-shot 파운데이션 오차를
일부러 보고하지 않는다** — *"differing DFT settings … can introduce misleading absolute offsets."*

🔴 **LiCl/GaF₃ 의 FT 에너지 RMSE = 0.09 meV/atom 은 믿기 어렵다.** 0.09 meV/atom = 0.00009 eV/atom 은
DFT 자체의 수렴 오차보다 작다. §14 의 10× 문제와 함께 봐야 한다.

---

## 7. ★ 체크포인트 저장 규약 — snapshot ensemble 재료가 되는가

**논문이 말하는 것 (§II D)** — 학습이 끝나면 나오는 파일:
- `MACE-FT.model` — 추론용 완성 모델
- `MACE-FT_compiled.model` — 배포 최적화판
- `MACE-FT_stageone.model` / `MACE-FT_stagetwo.model` — **단계별 중간 모델 2개**

⇒ **논문 표면만 보면 "모델 파일 2개"** 다. 간격·개수 규약은 논문에 **없다**.
그래서 코드를 읽었다.

### 7a. repo 실측 — MACE v0.3.17 의 실제 저장 로직

`mace/tools/checkpoint.py` + `mace/tools/train.py`:

- 파일명 규약: **`<tag>_epoch-<N>.pt`**, stage two 진입 후에는 **`<tag>_epoch-<N>_swa.pt`**
- 평가 주기: `--eval_interval` (**기본 1 epoch**)
- **검증손실이 개선된 epoch** → 저장. 그리고 `CheckpointIO.save()` 안에서
  ```python
  if not self.keep and self.old_path and not keep_last:
      os.remove(self.old_path)      # ← 직전 것을 지운다
  ```
  ⇒ **기본값에서는 "현재 최고" 하나만 남는다.**
- `keep_last=True` 가 되는 순간은 **stage one → stage two 전환 딱 한 번** ⇒ 그래서 최종적으로 **2개**가 남는다
  (= 논문이 말한 `_stageone` / `_stagetwo`). ✅ 논문 서술과 코드가 일치한다.
- **`--keep_checkpoints`** → `CheckpointIO.keep=True` → **아무것도 안 지운다** = 개선된 모든 epoch 이 남는다
- **`--save_all_checkpoints`** → **개선되지 않은 epoch 에도** 저장 ⇒ 둘 다 켜면 **최대 150개**(epoch 당 1개)

⇒ **"M ≥ 4 개의 체크포인트를 뽑을 수 있나?" 의 표면적 답은 예 — 플래그 두 개면 150개도 나온다.**

### 7b. 🔴 그런데 그 150개는 committee 가 되지 않는다 — 세 가지 이유

**① EMA 가 스냅샷을 서로 붙여 놓는다.** repo 실측: 저장은 `with ema.average_parameters():` 안에서 일어난다.
즉 저장되는 것은 순간 가중치가 아니라 **지수이동평균된 가중치**다. `ema_decay=0.999` 의 유효 평균창은
**≈ 1/(1−0.999) = 1000 스텝**(digest 계산). 튜토리얼 설정(batch 4)에서 1 epoch 이 대략 1.5k 스텝이므로,
**인접 epoch 의 스냅샷은 설계상 거의 같은 점**이다. 다양성을 만들라고 앙상블하는데 평활화 장치가 그걸 지운다.

**② 우리 기준(kurniawan)이 요구하는 간격을 못 채운다.** `litdb/papers/kurniawan2025_comparative_ensemble_uq_nnip.md` §④:
snapshot 앙상블은 *burn-in 스냅샷은 버리고 **100 epoch 간격**으로 저장해 근사 독립 확보*.
이 튜토리얼의 런은 **총 150 epoch** — 그중 stage one 이 0–110, stage two 가 111–149.
**digest 계산: 100-epoch 간격이면 한 런에서 뽑히는 준독립 스냅샷은 최대 2개.** M ≥ 4 가 아니다.

**③ stage one 과 stage two 는 애초에 다른 목적함수다.** stage two 는 `swa_energy_weight=100` 으로
**손실을 바꾼다**(Fig. 2 에서 전환점에 검증손실 스파이크가 보인다 — figure-read). 두 단계의 스냅샷은
**같은 사후분포의 표본이 아니다.** 섞어서 표준편차를 내면 그건 모델 불확실도가 아니라 손실함수 변경의 흔적이다.

**④ 그리고 결정적으로 — MACE 에 순환 학습률이 없다.** repo 실측: `mace/tools/scripts_utils.py` 가 지원하는
스케줄러는 **`ExponentialLR` 과 `ReduceLROnPlateau` 둘뿐**이다. snapshot ensemble 의 원전(Huang 2017,
kurniawan digest 의 [61])은 **cyclic LR restart** 로 서로 다른 극소에 착지시키는 것이 방법의 본체인데,
**그 스케줄러가 없다.** 단조 감쇠 궤적에서 뜬 스냅샷들은 한 극소 안의 잔떨림이다.

### 7c. ⇒ 판정

> **이 문서 기준으로 M ≥ 4 짜리 snapshot committee 는 만들어지지 않는다.**
> 플래그로 파일 개수는 채울 수 있지만(150개), **준독립성 요건(EMA 창·100-epoch 간격·동일 목적함수·순환 LR)을
> 네 개 다 어긴다.** 파일 4개를 모아 σ 를 계산하면 숫자는 나오지만 그 σ 는 `grasselli` 식 (27) 이 전제하는
> "독립 멤버의 산포"가 아니다 — **M=3 이종 committee 의 문제를 M=4 형태로 재포장하는 것**에 가깝다.
>
> **되게 하려면 이 논문 밖으로 나가야 한다**: ① epoch 수를 4×100 = **400+ 로 늘리고**
> ② **EMA 를 끄거나**(`--ema` 제거) 저장 시점만 EMA 없이 뽑고 ③ **stage two 전 구간에서만** 뽑아 목적함수를 고정하고
> ④ 순환 LR 이 필요하면 MACE 를 고쳐야 한다. **③④는 이 튜토리얼이 답을 주지 않는 영역이다.**
>
> **몇 시간인가**: ⛔ **논문에 학습 wall-clock 이 단 한 줄도 없다.** Table VIII 은 **MD 추론** 시간이지
> 학습 시간이 아니다. §9 에 우리가 세운 유일한 추정 근거를 적었다.

---

## 8. 필요한 라벨 수 — 데이터 효율 (Fig. 4)

### 8a. 데이터셋 실측 (repo, `.npy` 직접 카운트)

| 그룹 | 원자수 | 프레임 |
|---|---|---|
| `data.init` | 50 | 3260 |
| `data.init` | 400 | 1704 |
| `iter.000000` | 400 | 528 |
| `iter.000001` | 400 | 529 |
| `iter.000002` | 400 | 529 |
| **합계** | | **6550 프레임** |

에너지 범위 −4.3144 … −3.9970 eV/atom (표준편차 0.0655) · **힘 성분 표준편차 0.8403 eV/Å** · |F|max 11.62 eV/Å ·
힘 성분 총 4,437,000 개. readme 기준 **90/10 분할** ⇒ **≈5895 train / 655 valid**.

> ✅ **교차검증 (digest 계산) — 이 repo 데이터가 논문의 그 데이터가 맞다.**
> 논문의 "Relative F (%)" 는 *"force RMSE normalized by the standard deviation of DFT forces"* 로 정의된다.
> Table IV·V 의 11개 행에서 `RMSE_F / (Rel.F/100)` 을 역산하면 분모 σ_F 의 **평균 840.3 meV/Å**
> (행별 825.7–847.1). repo 데이터에서 직접 잰 힘 성분 표준편차 = **840.3 meV/Å**. **소수점까지 일치한다.**
> ⇒ 이 digest 의 repo 실측 수치는 논문 표와 같은 모집단에서 나온 것이다.

### 8b. 데이터 분율 vs 오차 (Fig. 4, figure-read ≈)

**⚠ 이 값들은 그림 눈금에서 읽었다. 논문에 표로 없다.**

**(a) RMSE Energy (meV/atom)**

| 분율 | from scratch | mp-0b3 | mpa-0 | omat-0 |
|---|---|---|---|---|
| 10% | ≈0.70 | ≈0.33 | ≈0.23 | ≈0.30 |
| 30% | ≈0.37 | ≈0.30 | ≈0.23 | ≈0.24 |
| 50% | ≈0.37 | ≈0.30 | ≈0.20 | ≈0.20 |
| 75% | ≈0.40 | ≈0.20 | ≈0.20 | ≈0.20 |
| 100% | ≈0.27 | ≈0.20 | ≈0.20 | ≈0.20 |

**(b) RMSE Force (meV/Å)**

| 분율 | from scratch | mp-0b3 | mpa-0 | omat-0 |
|---|---|---|---|---|
| 10% | ≈21.2 | ≈20.4 | ≈18.4 | ≈18.3 |
| 30% | ≈17.9 | ≈18.4 | ≈16.8 | ≈17.4 |
| 50% | ≈16.4 | ≈17.2 | ≈15.8 | ≈16.4 |
| 75% | **≈15.0** | ≈16.45 | ≈15.6 | ≈15.85 |
| 100% | **≈14.55** | ≈15.85 | ≈14.85 | ≈15.2 |

### 8c. 🔴 그림이 본문 주장을 부인한다

본문: *"Across **all** data set sizes, fine-tuned models (MP-0b3, MPA-0, and OMAT-0) **consistently** achieve
lower errors than training-from-scratch."*

**Fig. 4(b) 를 실제로 보면 틀렸다.**
- **75% 와 100% 에서 from-scratch 가 세 fine-tuned 모델을 전부 이긴다** (힘 RMSE ≈15.0 / ≈14.55 vs 15.6–16.45 / 14.85–15.85).
- 30%·50% 에서도 **mp-0b3 는 from-scratch 보다 나쁘다**.
- 에너지(a)에서는 본문 주장이 맞다 — 전 구간에서 fine-tune 이 이긴다.

⇒ **정확한 서술은 이렇다: fine-tune 의 이점은 (i) 에너지에서 전 구간, (ii) 힘에서는 데이터가 적을 때(≲30%)만.
데이터가 충분해지면 힘 정확도에서는 scratch 가 따라잡고 앞선다.**
이건 사실 놀랍지 않다 — fine-tune 은 사전학습 편향에 묶여 있고 데이터가 많아지면 그 구속이 손해가 된다.
**하지만 논문이 이걸 말하지 않는다.** 우리가 인용할 땐 반드시 갈라 써야 한다.

부수 관찰(figure-read): **오차막대가 from-scratch 만 크다** (에너지 10% 에서 ≈±0.10, 75% 에서 ≈±0.10;
fine-tuned 은 ≈±0.02–0.04). 3회 독립 실행의 1σ. ⇒ **fine-tune 의 진짜 이점은 평균 오차보다 "재현성"** 이다.
그리고 from-scratch 의 에너지 곡선은 **비단조**(30% 0.37 → 75% 0.40 → 100% 0.27)라 잡음이 크다.

### 8d. 목표 정확도별 라벨 수 (digest 계산)

repo 실측 6550 프레임 × readme 90% = **≈5895 train** 을 100% 로 놓고 Fig. 4 분율을 환산:

| 분율 | 대략 train 프레임 | 힘 RMSE (fine-tuned 최선, figure-read ≈) |
|---|---|---|
| 10% | ≈590 | ≈18.3 meV/Å |
| 30% | ≈1770 | ≈16.8 |
| 50% | ≈2950 | ≈15.8 |
| 75% | ≈4420 | ≈15.6 |
| 100% | ≈5895 | ≈14.85 |

⇒ **≈590 프레임(400원자급 LGPS)이면 힘 RMSE ≈18 meV/Å 에 도달한다.**
5895 프레임을 다 써도 14.85 까지밖에 안 내려간다 — **10× 데이터로 19% 개선**. 심한 수확체감.
**작은 파일럿의 근거가 여기 있다.**

⚠ 단, 분율은 **6550 프레임 전체 풀 기준의 무작위 부분집합**이지 "우리가 새로 만들 라벨 수"가 아니다.
그리고 이 풀은 이미 DeePMD active-learning 3 iteration 을 거친 **정제된** 셋이다(`iter.000000–2`).

### 8e. 계 크기별 비용 — 논문에 없다, 대신 Mo 데이터셋의 교훈

**⛔ 계 크기별 DFT 라벨링 비용표는 논문에 없다.** 대신 repo 실측으로 훨씬 유용한 걸 봤다:

`examples/Mo/train.xyz` = **6301 프레임**, 원자수 1–252. **구성비(ASE 로 실측)**:
- **nat=2: 2301 프레임** · **nat=1: 1634 프레임** ⇒ **전체의 62% 가 1–2 원자 셀**
- 실제 응집상 셀은 nat=36 (900) · 72 (540) · 54 (310) · 12 (285) …
- `config_type` 라벨이 대단히 세분화돼 있다: `C44_2`(1800) · `SliceSampleDFT`(1633) · `BCCDisDFT`(420) ·
  `pileup/*`(수십 개) · `Surfaces/{100,110,112}` · `VacancyDFT`·`diVacancyDFT`·`triVacancyDFT` ·
  `phononDFT` · `hcpDFT` · `compressed/*` · `IsolatedAtom`(**1개**, `dft_energy = −1855.3529371 eV`)
- test.xyz = **713 프레임**

⇒ **두 가지 실무 교훈**:
① **E0s 는 별도 옵션이 아니라 훈련파일 안의 `config_type=IsolatedAtom` 프레임으로 넣는다.** (논문 §II C 의
"직접 계산하라"가 실제로 구현된 모습.) 우리도 Li·P·S·Cl(+B·O·Nd) 각각 **고립원자 spin-polarized DFT 1점씩**이 필요하다.
② **훈련셋의 대부분은 비싼 큰 셀이 아니라 싼 1–2원자 셀**이다 — 반발벽·단거리 영역을 채우는 용도.
**우리 예산에서 DFT 라벨은 큰 셀에만 쓰고, 짧은 거리 영역은 다이머 스캔으로 싸게 채우는 게 이 논문의 실제 관행이다.**

---

## 9. 계산 비용 — 있는 것과 없는 것

### 9a. ⛔ 없는 것: 학습(fine-tune) wall-clock

논문 어디에도 **fine-tune 이 몇 시간 걸렸는지가 없다.** epoch 수(150)와 GPU(A800 80GB)만 있다.

**digest 계산 — 우리가 세울 수 있는 유일한 근거 (가정을 명시한다)**:
LGPS train ≈5895 프레임, `batch_size=4`(Mo 스크립트값을 LGPS 에도 가정 — **논문에 LGPS batch size 없음**)
⇒ epoch 당 ≈1474 optimizer step ⇒ **150 epoch ≈ 2.2×10⁵ step**.
`float64` + L=1 medium + 400원자 셀. ⚠ **이건 step 수일 뿐 시간이 아니다.** 시간으로 바꾸려면
우리 GPU 에서 1 step 을 실측해야 한다. 그게 파일럿의 첫 측정항목이다(§13).

### 9b. 있는 것: MD 추론 시간 (Table VIII, cuEquivariance 커널, 10,000 step)

| 원자수 | 128 | 372 | 1038 | 2900 | **Scaling** |
|---|---|---|---|---|---|
| **With** cuEq (s) | 710 | **800** | **1126** | **2619** | **0.41** |
| **Without** (s) | **658** | 1008 | 2031 | 5084 | 0.76 |

- 2900원자에서 **5084 → 2619 s = 1.94× 가속**. scaling 지수 0.76 → 0.41 (원자수에 대한 멱). 큰 계일수록 이득.
- 본문 주장 *"consistently lower elapsed times"* 는 🔴 **128원자에서 틀렸다** (710 > 658, cuEq 가 **더 느리다**).
  작은 계에서는 커널 오버헤드가 이득을 잡아먹는다. **우리 400–1000원자 셀은 이득 구간에 있다.**
- 논문 §II A 3 은 cuEq 가 *"typically by a factor of 3–10"* 빠르다고 하는데 **자기 Table VIII 은 최대 1.94×** 다.
  🔴 또 하나의 본문–표 불일치.
- 라이브러리 이름을 논문 전체가 **"cuEquivalence"** 로 잘못 쓴다 (정확한 이름은 **cuEquivariance**, NVIDIA).

⚠ repo 실측: `examples/graphene-water/run.py` 는 `steps=10000`, `time_step=1 fs` ⇒ **10 ps**.
그런데 본문 §III D 는 *"simulated for **200 ps** with a 1 fs time step"* 이라 하고,
**Fig. 9(a) 의 x축은 0–2000 fs = 2 ps** 다. 🔴 **세 값이 다 다르다** (200 ps / 10 ps / 2 ps).
그리고 run.py 는 `"mace-ft"` 와 `"mace-mp-0b3"` 두 항목에 **같은 모델 파일**을 넣는다
(`model_paths="mace-ft-tutorial-main-3.model"` 둘 다) — cuEq on/off 비교로는 맞지만 **이름이 오도한다.**

---

## 10. 결과 — 사례별 상세

### 10a. LGPS (Li₁₀GeP₂S₁₂) — 우리에게 가장 가까운 사례

데이터 출처 = **DPAISquare**(ref 80)의 공개 DeePMD 데이터셋 → `deepmd2mace.py`(dpdata 사용)로 extxyz 변환.
type_map = `["Li","Ge","P","S"]`.

**Table IV — 파운데이션별 최종 정확도 (소환값)**

| Model (epoch) | RMSE E (meV/atom) | RMSE F (meV/Å) | Relative F (%) |
|---|---|---|---|
| MACE-MP-0b3 (110) | 0.32 | 16.15 | 1.92 |
| MACE-MP-0b3 (148) | 0.28 | 15.84 | 1.87 |
| MACE-MPA-0 (110) | 0.30 | 15.07 | 1.79 |
| **MACE-MPA-0 (146)** | **0.27** | **14.88** | **1.77** |
| MACE-OMAT-0 (110) | 0.35 | 15.46 | 1.84 |
| MACE-OMAT-0 (149) | 0.27 | 15.32 | 1.82 |

**핵심 메시지**: *"for all U-MLIPs, with the same hyperparameters, we can all get comparable accuracy"* —
세 파운데이션의 최종 힘 RMSE 가 **14.88–15.84 (스프레드 6%)** 안에 들어온다.
**출발점 선택이 결과를 크게 안 바꾼다**는 것이 이 표의 요지이고, 이건 우리에게 좋은 소식이다(§12).

**단계별 이득 (digest 계산)**: stage two(SWA)로 넘어가며 에너지 0.32→0.28 / 0.30→0.27 / 0.35→0.27
(**−12.5 / −10.0 / −22.9%**), 힘은 16.15→15.84 / 15.07→14.88 / 15.46→15.32 (**−1.9 / −1.3 / −0.9%**).
⇒ **stage two 는 에너지 전용 장치다.** 힘에는 거의 영향이 없다. `swa_energy_weight=100` 이라는 설정 그대로의 결과.

⛔ **이 표에 zero-shot(fine-tune 전) 행이 없다.** 그래서 **"LGPS 에서 fine-tune 이 몇 배 개선했나"를
이 논문으로는 말할 수 없다.** (Si 와 계면 예제에만 before/after 가 있다.) 우리에게 제일 아쉬운 결측이다.

### 10b. Si — OOD 일반화 → §6a

### 10c. Mo — 탄성상수와 GSFE

**Table VI — 탄성 (소환값)**

| | EAM¹¹⁵ | GAP¹¹⁶ | **MACE-MP-0b3** | **Fine-tuning** | DFT¹¹⁴ |
|---|---|---|---|---|---|
| C₁₁ (GPa) | 465 (1.31%) | 478 (4.74%) | **251 (45.32%)** | **452 (1.52%)** | 459 |
| C₁₂ (GPa) | 161 (0.62%) | 166 (2.47%) | 189 (16.67%) | 174 (7.41%) | 162 |
| C₄₄ (GPa) | 109 (12.37%) | 108 (11.34%) | **47 (51.55%)** | **82 (15.46%)** | 97 |
| B (GPa) | 263 (0.38%) | 270 (3.05%) | 210 (19.85%) | 267 (1.91%) | 262 |
| ν | 0.26 (13.33%) | 0.26 (13.33%) | 0.43 (43.33%) | 0.28 (6.67%) | 0.30 |

**이게 이 논문에서 제일 강한 물리적 결과다.** 파운데이션 MACE-MP-0b3 는 **C₁₁ 을 45%, C₄₄ 를 52% 과소평가**한다 —
즉 **PES 가 물러 있다(softening)**. fine-tune 이 C₁₁ 을 251→452 (DFT 459)로, B 를 210→267 (DFT 262)로 되돌린다.
⇒ **범용 MLIP 의 탄성 연화가 실측으로 확인되고, fine-tune 이 그 특효약이라는 것.**

🔴 **표와 본문이 안 맞는다 (3중 문제)**:
1. 본문은 *"reducing the error from **45.91%** to **2.58%** for C₁₁, from **56.88%** to **14.77%** for C₄₄,
   from **48.27%** to **3.45%** for ν"* 라 하는데 **표는 45.32→1.52 / 51.55→15.46 / 43.33→6.67** 이다.
2. 이유: 본문은 *"percentage error relative to **experiment**"*, 표 캡션은 *"percentage deviation from the
   **DFT** reference"*. **기준이 다르다.** 그런데 **표에 실험 열이 아예 없다.**
   **digest 계산**으로 역산한 숨은 실험값: C₁₁ ≈ **464 GPa**, C₄₄ = **109 GPa**, ν = **0.29**.
3. 그 역산으로 검산하면 C₄₄ fine-tuned 의 실험 대비 오차는 (109−82)/109 = **24.77%** 인데
   본문은 **14.77%** 라 쓴다 ⇒ **자릿수 오타(2→1)로 보인다.**
4. 캡션이 열 이름과 다르다 — *"(EAM/FS, GAP, **tabGAP**, and **NNIP**)"* 인데 실제 열은
   EAM·GAP·MACE-MP-0b3·Fine-tuning·DFT. **다른 논문 캡션을 복사한 흔적.**

**Fig. 7 / Table VII — GSFE**

Table VII (barrier error, 단위 미표기 — **digest 계산으로 J/m² 확인**):

| 슬립 방향 | MACE-MP-0b3 | FT-Default | **FT** (force weight 100) |
|---|---|---|---|
| ⟨110⟩ | 0.88 | 0.23 | **0.17** |
| ⟨121⟩ | 0.78 | 0.36 | **0.21** |

**Fig. 7 에서 실제로 읽은 봉우리 (figure-read ≈, J/m²)**:

| | ⟨110⟩ | ⟨121⟩ |
|---|---|---|
| MACE-MP-0b3 | ≈0.59 | ≈0.73 |
| **DFT** | **≈1.475** | **≈1.51** |
| FT | ≈1.65 | ≈1.72 |
| FT-Default | ≈1.70 | ≈1.87 |

**digest 계산 검산**: 1.475−0.59 = 0.885 ≈ 0.88 ✅ / 1.65−1.475 = 0.175 ≈ 0.17 ✅ /
1.70−1.475 = 0.225 ≈ 0.23 ✅ / 1.51−0.73 = 0.78 ✅ / 1.72−1.51 = 0.21 ✅ / 1.87−1.51 = 0.36 ✅.
⇒ Table VII 은 **J/m² 단위의 절댓값 오차**가 맞다.

🔴 **그런데 부호가 뒤집힌다 — 논문은 이걸 한 번도 말하지 않는다.**
파운데이션은 DFT 를 **60% 과소**평가하고, **두 fine-tuned 모델은 DFT 를 넘어 과대**평가한다
(FT: ⟨110⟩ +11.9%, ⟨121⟩ +13.9%; FT-Default: +15.3%, +23.8% — digest 계산).
Table VII 은 절댓값만 주므로 **"오차가 줄었다"로만 읽히지만, 실제로는 물렀던 것이 딱딱해지다 못해 지나쳤다.**
잔차도 **여전히 12–14%** 다. ⇒ 우리 talk 슬 8 의 "softening → fine-tuning 이 되돌린다" 명제는
**"되돌린다"가 아니라 "지나쳐 되돌린다"** 로 고쳐 인용해야 한다.

FT 가 FT-Default 보다 나은 이유(저자 설명): 힘 가중 ↑ ⇒ PES 국소 기울기를 더 정확히 학습 ⇒
슬립 경로 각 지점의 원자 완화가 힘에 민감한 GSFE 에 유리.

### 10d. 그래핀–물 계면

**데이터 생성 파이프라인(§III D)** — 이게 우리가 베낄 만한 유일한 완결 레시피다:
1. **고전 MD 사전평형화** (LAMMPS): 그래핀 = **Tersoff** bond-order, 물 = **강체 3-site + SHAKE**,
   단거리 = **Lennard-Jones**, 장거리 정전기 = **Ewald**, PBC, **NVT**
2. 시간상 **비상관 스냅샷을 무작위 추출**
3. **VASP 단일점 라벨링**: **PAW + PBE + D3** 분산보정, **plane-wave cutoff 400 eV**,
   전자 SCF 수렴 **1×10⁻⁶ eV**
4. MACE fine-tune → LAMMPS `pair_style mace` 로 MD (metal units, **NVT 298 K**)

⇒ **무작위 생성으로 비물리 구조를 만들지 않는 것**이 요지. 계 372 원자.

**Fig. 9 (figure-read)**:
- (a) 온도: 세 궤적(MACE-FT-MD · MACE-MPA-0-MD · AIMD)이 ≈300 K 근처. 단 **MACE-MPA-0(주황)은
  초기 250 fs 에 ≈415 K 까지 튄다** — 본문의 *"comparable temperature fluctuations"* 보다 거칠다. x축 **0–2000 fs 뿐**.
- (b) 산소 수밀도 프로파일 (z = 10–17 Å): **MACE-FT(파랑)와 AIMD(보라 점선)가 거의 포갠다** —
  첫 봉우리 z ≈ 14 Å, 높이 ≈10.8(FT) vs ≈11.6(AIMD). **MACE-MPA-0(주황)은 봉우리 ≈6.4 로 40% 낮고
  더 넓게 퍼지며 onset 도 z≈11.8 로 당겨져 있다** (FT/AIMD 는 ≈12.4).
- 인쇄값: **d_gw(MACE) = 0.35 nm · d_gw(AIMD) = 0.35 nm · d_gw(Exp.) = 0.36 nm**

⇒ **이게 논문에서 가장 설득력 있는 그림이다.** RMSE 가 아니라 **구조 관측량(밀도 프로파일)** 에서
fine-tune 전후가 눈에 띄게 갈리고, fine-tune 후가 AIMD·실험과 맞는다.
**"RMSE 만 보지 말고 물성으로 검증하라"의 실물 증거.**

### 10e. 분자/산화물 계면 · 고체/고체 계면 → §6c (Table IX), Fig. 10

Fig. 10 은 (a) Au₂/Al-doped MgO(001) 구조 (b) 그 dual-axis RMSE (c) TiO₂(101)–NaCl 수용액 구조 (d) 그 RMSE.
CACE-LR 값은 ref 127(a,b)·ref 129(c,d)에서 가져왔고 MACE-FT 는 이 논문 값.
⚠ 저자가 **zero-shot 파운데이션 오차를 일부러 뺐다**(DFT 설정 차이로 절대 offset 이 오도할 수 있어서).
⚠ 그리고 *"Evaluations on task-specific quantities of interest, such as **adsorption energies**, would require
additional DFT calculations and are **left for future work**."* — **RMSE 만 보고 흡착에너지는 안 봤다.**
(우리 SDCP 흡착에너지 8회 반려 경험을 생각하면 이 유보는 정직한 쪽이다.)

---

## 11. 어느 파운데이션 모델을 다루나 — **UMA 는 없다**

**Table I (논문이 나열한 U-MLIP 목록, 소환값)** — 나열일 뿐 대부분 실험 대상이 아니다.

| Model | Year | Architecture | Data |
|---|---|---|---|
| M3GNET | 2022 | SchNet | MP, 89 원소, 62,783 화합물 |
| CHGNet | 2023 | GNN + Charge | MP + Trajectory, 89 원소, 146,000 화합물 |
| ALIGNN-FF | 2023 | Line GNN | JARVIS-DFT, 72,708 화합물 |
| PFP (Matlantis) | 2023 | Tensorial GNN | Custom, ≈10×10⁶ 구성 |
| GNoME | 2023 | NequIP | MP + Custom, ≈89×10⁶ 구성 |
| DPA-1,2,3 | 2023–2025 | DeepMD | Alloy, OC2M 등 |
| **MACE-MP-0** | 2024 | **MACE** | CHGNet 과 동일 데이터 |
| SevenNet-0 | 2024 | NequIP | CHGNet 과 동일 데이터 |
| MatterSim | 2024 | Graph transformer | MP + Alexandria + Custom, ≈17×10⁶ |
| EquiformerV2-OMAT24 | 2024 | EquiformerV2 | MP + Alexandria + Custom, ≈118×10⁶ |
| NEP89 | 2025 | NEP | OMat24, SPICE 등 |
| **UMA** | **2025** | **eSEN** | **459M 구성; 평균 원자수 19 (OMat24)–178 (ODAC25)** |

**실제로 fine-tune 된 모델 (전수)**

| 모델 | 어디에 | repo 에 가중치 있나 |
|---|---|---|
| **MACE-MP-0b3** (medium) | LGPS, Mo, 그래핀–물 | ✅ `models/mace-mp-0b3-medium.model` (79.5 MB) |
| **MACE-MPA-0** (medium) | LGPS, Si, 계면 | ✅ `models/mace-mpa-0-medium.model` (79.5 MB) |
| **MACE-OMAT-0** (medium) | LGPS | ✅ `models/mace-omat-0-medium.model` (79.5 MB) · **ASL 라이선스, 학술 전용** |

- **MatterSim**: Table I 한 행. **실험 0건.**
- **SevenNet**: Table I 한 행. **실험 0건.**
- **UMA / fairchem**: Table I 한 행 + 참고문헌. **실험 0건. `fairchem` 단어 0회.**

> ⚠ **혼동 주의 — MACE-OMAT-0 ≠ UMA.**
> 이름에 둘 다 "OMat/omat" 이 들어가서 헷갈리기 쉽다. **MACE-OMAT-0** 은 *MACE 아키텍처*를
> *OMat24 데이터*로 학습한 모델이고, 우리 **UMA-s-1p1(omat task)** 는 *eSEN 아키텍처*의
> *Meta fairchem* 모델이다. **데이터 계보만 겹치고 아키텍처·코드베이스·체크포인트 포맷이 전부 다르다.**
> 이 논문이 "OMAT-0 을 fine-tune 했다"고 해서 **우리 UMA 를 fine-tune 한 선례가 되지 않는다.**

---

## 12. ★ Figure set

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | fine-tune 전체 워크플로 도해: 사전학습(주기율표 원소별 데이터량 히트맵) → 계별 fine-tuning 데이터셋(나노입자·금속·촉매·수용액계면·합금·페로브스카이트) → Final potential → 구조/열역학/동역학 물성 | **§4a 6단계의 그림판.** 원소 히트맵에서 우리 원소 데이터량이 보인다 (figure-read: Li 222K · S 152K · P 173K · Cl 84K · O 865K · **Nd 31K**) — Cl 이 Li/S/P 보다 확연히 적다 |
| 2a | stage 1/2 훈련·검증 손실 곡선. **전환점 epoch ≈110, 총 150** | **체크포인트 스케줄의 실물**. §7 의 M≥4 판정 근거 |
| 2b | epoch 별 검증 RMSE(E, F). **F 는 매끈·단조, E 는 stage 1 내내 심하게 진동** | 에너지 수렴이 나쁘다 ⇒ 에너지 기준 조기종료는 위험. **stage two 가 에너지 전용 처방인 이유** |
| 2c–2f | stage1/2 각각의 에너지·힘 parity plot (train/test) | 🔴 **Table IV 와 정확히 10× 어긋난다** (§14-1). 인용 전 반드시 확인 |
| 3 | LGPS 원자구조 | (안 봤다 — 구조 렌더링) |
| 4a,b | **데이터 분율(10/30/50/75/100%) vs RMSE(E, F)**, scratch vs 3개 파운데이션, 3회 실행 1σ | ★★ **최소 파일럿 규모의 근거**. 그리고 🔴 **75–100% 에서 scratch 가 힘 정확도를 이긴다**(§8c) — 본문 주장 반증 |
| 5a | Si OOD 구조 | (안 봤다 — 구조 렌더링) |
| 5b,c | **Si OOD 테스트: MPA-0 / Rand / AL / FT-SH / FT 의 E·F RMSE (막대 위 숫자 인쇄)** | ★★ **일반화 논거의 전부**. 파운데이션 대비 E 12×·F 2.4× 개선. 단 **구조 OOD 이지 화학 OOD 가 아니다**(§6b) |
| 6 | BCC Mo 전위 구조 | (안 봤다 — 구조 렌더링) |
| 7a,b | **Mo GSFE 프로파일 ⟨110⟩·⟨121⟩**: 파운데이션·FT-Default·FT·DFT 4곡선 | ★ **PES softening 의 실물**. 🔴 파운데이션은 −60% 과소, **FT 는 +12~14% 과대 — 부호가 뒤집힌다**(§10c) |
| 8 | 그래핀–물 계면 구조 | (안 봤다 — 구조 렌더링) |
| 9a,b | 그래핀–물 MD: 온도 궤적 + **산소 수밀도 프로파일** (MACE-FT / MACE-MPA-0 / AIMD) | ★ **RMSE 아닌 구조 관측량으로 fine-tune 효과를 보인 유일한 그림.** 파운데이션은 첫 봉우리 40% 낮음. 🔴 x축 2 ps 인데 본문은 200 ps |
| 10a–d | Au₂/MgO(Al-doped)·TiO₂–NaCl 수용액 구조 + dual-axis RMSE (MACE-FT vs CACE-LR) | 장거리 상호작용 없이도 대등. ⚠ zero-shot 값 없음, 흡착에너지 미평가 |
| 11a,b | LiCl(001)/GaF₃(001) · 다이아몬드/cBN 계면 구조 | (안 봤다 — 구조 렌더링) |
| Table I | U-MLIP 목록 (아키텍처·데이터) | **UMA 가 여기 한 줄로만 존재한다** |
| Table III | 권장 하이퍼파라미터 범위 | 🔴 **Table V 의 최적(fw=100)이 이 범위(≤20) 밖** |
| Table IV | LGPS: 3개 파운데이션 × 2단계 정확도 | **출발점이 결과를 별로 안 바꾼다**. ⛔ zero-shot 행 없음 |
| Table V | 하이퍼파라미터 ablation (fw / lr / ema, 3시드) | ★★ **실물 최적값의 출처**. 효과 크기 20:18:1 |
| Table VI | Mo 탄성상수 (EAM/GAP/파운데이션/FT/DFT) | ★ **연화 −45%/−52% → 회복**. 🔴 본문·캡션·표 3중 불일치 |
| Table VII | GSFE barrier 오차 | 단위 미표기(J/m² 로 확인). 부호 정보 소실 |
| Table VIII | cuEq on/off MD 시간 (128–2900 원자) | 2900원자 1.94× 가속. 🔴 128원자에선 오히려 느림 |
| Table IX | 두 계면의 zero-shot vs FT vs baseline | **9× 개선** — 논문에서 before/after 가 있는 몇 안 되는 표 |
| Table X | 최적 하이퍼파라미터의 계간 이식성 | ★★ **"최적은 계마다 다르다"의 근거**. 10.7% → 0–4% |

---

## 13. Post-processing

- **무엇**: 힘·에너지 RMSE / parity plot / loss 곡선 (MACE 학습 스크립트가 자동 생성) ·
  **탄성상수 C₁₁·C₁₂·C₄₄ → B, ν** · **GSFE 프로파일**(슬립 경로 스캔 + 원자 완화) ·
  **산소 수밀도 프로파일 n(z)** · 온도 궤적 · MD wall-clock 벤치
- **도구**: **ASE**(구조완화 — preconditioned **L-BFGS**, 셀+좌표 동시 최소화 / Langevin NVT MD) ·
  **LAMMPS** (`pair_style mace no_domain_decomposition`, `pair_coeff * * <model>-lammps.pt <원소들>`, metal units) ·
  **VASP**(라벨링) · **dpdata**(DeePMD → extxyz) · **cuEquivariance**(추론 가속) ·
  **torch-dftd** (D3 + skin 이웃리스트, `CheukHinHoJerry/torch-dftd`) · **RBMD** (저자들 자체 대규모 MD 플랫폼)
- **수치화·기록**: MACE 는 log 파일 끝에 **RMSE 요약표**를 찍고, 모델 4종
  (`.model` / `_compiled.model` / `_stageone.model` / `_stagetwo.model`)을 남긴다.
  LAMMPS 배포는 별도 변환 스크립트로 `*-lammps.pt` 생성.
- **이웃리스트 재사용** (D3 오버헤드 완화): `every`(갱신 간격) · `delay`(다음 갱신 전 버퍼) ·
  `check`(재사용 조건 검증) · `skin`(버퍼 폭, Å) 네 파라미터. ⚠ **논문에 권장 수치가 없다** — 이름만 설명한다.

---

## 14. 🔴 논문 내부 불일치 — 인용 전에 반드시 알아야 할 것

이 논문에는 **본문과 표/그림이 어긋나는 자리가 최소 6곳** 있다. 튜토리얼이라 널리 복사될 텐데 위험하다.

1. **에너지 RMSE 가 정확히 10× 다르다.** Fig. 2(c) 테스트 **3.2 meV/atom** ↔ Table IV MP-0b3(110) **0.32**.
   Fig. 2(e) **2.8** ↔ Table IV(148) **0.28**. **힘은 완벽히 일치한다**(Fig 2d **16.2** ↔ Table IV **16.15**;
   Fig 2f **15.8** ↔ **15.84**). ⇒ **에너지 축에서만** 10배 어긋난다.
   물리적으로는 **Fig. 2 쪽(2.4–3.2 meV/atom)이 그럴듯하다** — 400원자 티오포스페이트에서 0.28 meV/atom
   = 0.00028 eV/atom 은 DFT 자체 수렴오차보다 작다. **어느 쪽이 옳은지 이 PDF 로는 확정 불가.**
   ⇒ **이 논문의 절대 에너지 RMSE 를 인용하지 말 것.** 상대 개선폭(10.7% 등)만 쓴다.
2. **Table VI 본문 vs 표**: 45.91→2.58 / 56.88→14.77 / 48.27→3.45 (본문, 실험 기준)
   ↔ 45.32→1.52 / 51.55→15.46 / 43.33→6.67 (표, DFT 기준). **표에 실험 열이 없다.**
   그리고 C₄₄ 의 14.77% 는 **24.77% 의 오타로 보인다**(digest 계산).
3. **Table VI 캡션**이 존재하지 않는 열(tabGAP, NNIP)을 열거한다 — 다른 논문 캡션 복사 흔적.
4. **Fig. 4 vs 본문**: *"consistently … lower errors than training-from-scratch"* 가
   **75%·100% 힘 RMSE 에서 반증된다**(§8c).
5. **Table VIII vs 본문**: *"consistently lower elapsed times"* 가 **128원자에서 반증**(710 > 658).
   그리고 §II A 3 의 *"factor of 3–10"* 가속 ↔ 실측 최대 **1.94×**.
6. **MD 시간이 세 값**: 본문 **200 ps** / 저장소 스크립트 **10 ps** / Fig. 9(a) x축 **2 ps**.
7. (부수) 라이브러리명 **cuEquivalence** → 정확히는 **cuEquivariance**.
8. (부수) Table III 권장 상한 `forces_weight ≤ 20` ↔ 논문 자신의 최적 **100**.
9. (부수) `John2021-hub` repo README 는 clone 주소를 **`YangshuaiWang/mace-ft-tutorial`** 로 안내한다 —
   논문 본문이 지정한 정본 저장소와 이름이 다르다. (README 의 BibTeX 도 `author={}` 가 비어 있고 year 가 2023.)
10. (부수) **LiGePS 예제에 fine-tune 스크립트가 없다.** `examples/LiGePS-SSE-PBE/readme.md` 는
    *"A script for fine-tuning foundation models"* 와 *"A script for computing the GSFE"* 를 포함한다고
    적어 놨지만 실제 파일은 **`deepmd2mace.py` 하나뿐**이다 (GSFE 스크립트는 Mo 폴더에만 있다 —
    LGPS 에 GSFE 를 넣은 것 자체가 readme 복사 실수). **우리 계에 제일 가까운 예제의 레시피가 없다.**

---

## 15. 🎯 우리 좌표 — 본론

> ⚠ 이 절의 논문 수치는 전부 **소환값**이다. `db/properties/` 의 우리 절대값과 같은 표에 섞지 않는다.

### 15a. 이 튜토리얼로 UMA 를 fine-tune 할 수 있나 — **아니다. 직접적으로는 불가능하다.**

**판정 근거 (repo 실측, MACE v0.3.17)**

`mace/cli/run_train.py` 가 `--foundation_model` 을 받아서 하는 일:
```python
model_foundation = torch.load(args.foundation_model, map_location=args.device)
args.r_max = model_foundation.r_max.item()                                  # ← MACE 속성
foundation_model_avg_num_neighbors = model_foundation.interactions[0].avg_num_neighbors   # ← MACE 속성
```
그리고 가중치 이식은 `mace/tools/finetuning_utils.py::load_foundations_elements_default()` 가
**MACE 블록(interactions / products / readouts)에 하나씩 복사**한다.
⇒ **UMA(eSEN) 체크포인트에는 `r_max`·`interactions[0].avg_num_neighbors` 가 존재하지 않는다.**
`torch.load` 단계에서 죽거나 그 다음 줄에서 `AttributeError` 다. **아키텍처 하드락이다.**

(참고: `mace/tools/fairchem_dataset/` 가 있긴 하지만 이건 **fairchem 의 LMDB *데이터* 포맷을 읽는 어댑터**이지
UMA *모델* 로더가 아니다. repo 실측: `fairchem_readme.md` = *"standalone implementation of the AseDBDataset
class extracted from the FairChem codebase"*.)

**옮길 수 있는 것 / 없는 것**

| | 옮길 수 있다 (아키텍처 무관) | 못 옮긴다 (MACE 종속) |
|---|---|---|
| **데이터** | extxyz 포맷 · 90/10 분할 · `IsolatedAtom` 프레임으로 E0s 주입 · rattle 0.1–1.0 Å + MC 필터 · 고전MD→선별→DFT 재라벨 2단계 · 1–2원자 셀로 반발영역 채우기 | (없음 — 데이터는 전부 이식 가능) |
| **손실** | **힘 가중을 크게**(1→100 에서 힘 RMSE −20.9%, 다만 1→10 이 −15.6%) · 응력은 옵션 · 2단계(힘 우선 → 에너지 우선) 개념 | `--swa_*` 플래그 이름, `--loss universal` 구현 |
| **스케줄** | lr 10⁻³ 근처가 U자 최적 · EMA 는 효과 미미(−1.1%) · batch ≤ 20 · epoch 150 정도면 수렴 | `start_swa = max_epochs//4*3` 자동규칙 · ReduceLROnPlateau(factor 0.8, patience 50) |
| **검증** | parity plot + loss 곡선 → **그다음 downstream 물성으로 재검증**(Fig. 9 교훈) | MACE log 포맷 |
| **동결** | 개념(full / partial / LoRA) | `--freeze` · `--lora*` · `--lr_params_factors` 구현 |
| **재생(replay)** | multi-head replay 라는 **발상** | `--pt_train_file` · `--num_samples_pt` · MACE 의 mp/omat 자동 다운로드 |

⇒ **결론**: 이 논문은 **레시피 문서로는 쓸 수 있고, 실행 경로로는 못 쓴다.**
UMA 를 fine-tune 하려면 **fairchem 쪽 도구를 따로 확인해야 하고, 이 논문은 그에 대해 아무 말도 하지 않는다.**
⚠ **fairchem 이 UMA fine-tune 을 지원하는지 여부는 이 작업에서 확인하지 않았다** (§17).

### 15b. M ≥ 4 체크포인트 절차 — **이 문서 기준으로는 안 된다** → §7c

요약: 파일 개수는 `--keep_checkpoints --save_all_checkpoints` 로 최대 150개까지 만들 수 있지만,
**EMA 평활(유효창 ≈1000 스텝) · 100-epoch 간격 요건(150 epoch 런에서 최대 2개) · stage1/2 목적함수 불일치 ·
순환 LR 부재** 네 가지가 준독립성을 깬다.
**몇 시간인지는 논문에 없다** — 유일한 근거는 §9a 의 step 수 추정(≈2.2×10⁵ step, 가정 명시)뿐이다.

### 15c. fine-tune 의 대가 — 우리 기존 결과와의 비교가 얼마나 깨지나

**이 논문은 답을 주지 않는다**(§6b). 그래서 **우리가 직접 판단해야 하는 부분**을 정리한다.

| 우리 결과 | fine-tune 후 비교 가능한가 | 이유 |
|---|---|---|
| **comp1 / modelc 의 Ea·D** (UMA-s-1p1, MSD 2–50 ps) | ⛔ **끊긴다** | 힘장이 바뀌면 궤적이 바뀐다. 고정 체크포인트라는 전제가 우리 D/Ea 비교군의 근거다 |
| **modelc 3-seed Ea 0.197±0.032** | ⛔ **끊긴다** | 같은 이유. 재계산 필요 |
| **+B₂O₃ · Nd–O 계열** | ⛔⛔ **가장 위험** | LPSCl 로만 fine-tune 하면 B·O·Nd 환경은 **훈련셋 밖**이고, 논문이 그 열화를 **재지 않았다**. 여기가 진짜 화학 OOD 다 |
| **DFT 값들** (gap · E_VRH · B₀ · ICOHP · ESW) | ✅ **안 끊긴다** | MLIP 과 무관한 DFT 산출물 |

⇒ **현실적 규율**: fine-tune 모델은 **새 이름의 별도 계열**로 관리하고, 기존 UMA-s-1p1 고정 체크포인트 결과와
**같은 표에 절대 넣지 않는다.** 우리 `comparison_group` 규약이 이미 이걸 강제하는 구조다.
그리고 **fine-tune 을 하더라도 baseline UMA 궤적을 지우지 않는다** — 비교군이 사라지면 되돌릴 수 없다.

### 15d. 우리 라벨 자산과 이 논문의 거리 (digest 계산 — 소환값 대 우리값 대조, 표는 따로 둔다)

| | 이 논문 LGPS | 우리 `mlip_bench_li3ps4_uma.json` |
|---|---|---|
| 모델 | MACE-MP-0b3/MPA-0/OMAT-0 **fine-tuned** | **UMA-s-1p1(omat), zero-shot** |
| 계 | Li₁₀GeP₂S₁₂ (Cl 없음) | Li₃PS₄ (**Cl 없음**) |
| 테스트 구조 수 | (풀 6550 의 10% ≈655) | **243** |
| **힘 RMSE** | **14.88–16.15 meV/Å** (fine-tune 후) | **44.58 meV/Å** (0.04458 eV/Å, zero-shot) |
| 힘 MAE | (미보고) | 29.97 meV/Å |
| 에너지 RMSE | 0.27–0.35 meV/atom *또는* 2.4–3.2 (§14-1 미해결) | **18.47 meV/atom** (원소별 선형보정 후) |

**⚠ 직접 비교 금지.** 계가 다르고(LGPS vs Li₃PS₄), DFT 설정이 다르고, 테스트셋 구성 방식이 다르다.
그래도 **자릿수 감각**은 얻을 수 있다: 우리 zero-shot 힘 RMSE **44.6** 은
이 논문의 fine-tune 후 값 **≈15** 의 **약 3배**(digest 계산 44.58/15.3 ≈ 2.9×).
그리고 이 논문의 zero-shot 파운데이션 값들(Si OOD 126 · LiCl/GaF₃ 179 · C/cBN 171 meV/Å)보다
**우리 UMA 가 훨씬 낫다** — 우리 출발점이 그들의 출발점보다 좋다는 뜻이다.
⇒ **fine-tune 으로 기대할 수 있는 상한은 "힘 RMSE 3배 개선" 정도이지 10배가 아니다.**
(그들의 9–10배 개선은 zero-shot 이 179 meV/Å 로 나빴던 계에서 나온 값이다.)

부수 관찰: 우리 파일의 `reference_correction.fit_R2 = 0.620` 은 낮다 — 원소 개수 선형조합으로 에너지 offset 의
62% 밖에 설명 못 한다. 이 논문 §II C 의 **"E0s 를 직접 spin-polarized DFT 로 계산하라"** 가 정확히 이 문제를 겨눈다.

### 15e. 🔬 최소 실험 설계 — 지금 우리 라벨로 할 수 있는 가장 작은 파일럿

> ⚠ **이건 제안이지 결정이 아니다.** 던지기 전에 `kb/templates/estimand_card.md` (보고량 카드) §1–3 을
> 먼저 채워야 한다 — **"무엇을 원하고, 어떤 식으로 재고, 이 계에서 그게 잘 정의되는가."**
> 특히 **"fine-tune 된 모델의 D 와 고정 UMA 의 D 를 같은 보고량으로 볼 것인가"** 가 카드에서 먼저 판정돼야 한다.

**단계 0 — 아키텍처 판정 (반나절, DFT 0점)**
`fairchem` 이 UMA-s-1p1 의 fine-tune 을 지원하는지 **먼저 확인한다.** 지원하지 않으면
파일럿 전체가 "MACE 를 새로 도입할 것인가"라는 다른 질문으로 바뀐다. **이 단계 전에 GPU 를 잡지 않는다.**

**단계 1 — 라벨 구멍부터 메운다 (Cl)**
현재 자산: `mlip_bench_li3ps4_uma.json`(243구조, **Cl 없음**) · 힘 대조용 700 K 20점(미실행) · Nd DFT 단일점 6개(진행중).
⇒ **Cl 라벨이 0 이다. 이 상태로 LPSCl fine-tune 은 성립하지 않는다.**
이 논문의 데이터 관행을 그대로 쓰면:
- **고립원자 E0s**: Li·P·S·Cl **4점** (spin-polarized 단일점, 큰 빈 셀). **필수** (§II C 의 최우선 권고)
- **본체**: comp1/modelc 궤적에서 **비상관 스냅샷 ≈300–600 프레임** → DFT 단일점
  (Fig. 4 의 10% ≈590 프레임이 힘 RMSE ≈18 meV/Å 를 낸 지점 — **가장 싼 유효 구간**)
- **단거리 보강**: Li–S·Li–Cl·P–S **다이머 스캔** 수십~수백점 (Mo 셋의 62% 가 1–2원자 셀이었다는 관행)
- 분할 **90/10**

**단계 2 — 대조 잡(control) 먼저**
fine-tune 하기 전에 **기존 고정 UMA 로 같은 테스트셋의 힘 RMSE 를 먼저 잰다.**
⇒ 이게 없으면 "fine-tune 이 얼마나 개선했나"를 말할 수 없다. **이 논문의 Table IV 가 정확히 그 실수를 했다**
(zero-shot 행 없음). 우리는 반복하지 않는다.

**단계 3 — 한 축만 훑는다**
이 논문의 ablation 세 축 중 **효과 크기가 20:18:1** 이므로 (§5b):
- `forces_weight` **1 → 10 → 100** (3점). 1→10 에서 이득의 80% 가 나온다
- `lr` **5e-4 / 1e-3** (2점)
- `ema_decay` 는 **훑지 않는다** (−1.1%, 표준편차의 몇 배지만 실무적으로 무의미)
⇒ **최대 6 런.** 각 런 150 epoch. **시드는 반드시 ≥3** (Table V 가 3시드였고, 우리 규율도 단일시드 판정을 금지한다).

**단계 4 — 검증은 RMSE 로 끝내지 않는다**
Fig. 9 의 교훈: **구조·수송 관측량으로 재검증한다.**
- 힘 RMSE (1차) → **밀도/RDF** → **MSD 2–50 ps 창의 D** (우리 고정 규약)
- ⚠ **D 절대값 인용 금지** 규율이 여기서도 산다. 비교는 **비율**로, **멀티시드**로.

**단계 5 — 대가를 측정한다 (이 논문이 안 한 것)**
- fine-tune 모델을 **`mlip_bench_li3ps4_uma.json` 의 243구조(Cl 없음)에 되돌려 평가**한다.
  ⇒ **이게 우리의 catastrophic-forgetting 계측기다.** 44.58 meV/Å 에서 얼마나 나빠지는지가 곧 "대가"다.
  **이 한 측정이 이 논문 전체에 없는 것**이고, 우리는 자산이 이미 있어서 공짜로 할 수 있다.
- 가능하면 **B₂O₃·Nd 계열 단일점 몇 개**에도 되돌려 본다 (Nd 6점이 진행 중이므로 완료되면 바로).

**비용 (digest 계산, 가정 명시)**
- DFT: 고립원자 4점 + 본체 ≈300–600점(400원자급 아님 — comp1 셀 크기 기준) + 다이머 수십점
- 학습: 6런 × 150 epoch. **1 step 시간을 우리 GPU 에서 먼저 실측해야 한다** (§9a — 논문에 학습시간 없음)
- GPU: **pw.x 와 UMA/torch 동시 실행 금지** 규율이 그대로 적용된다 (gabia VRAM 47/48 GB 사례). 
  kgy 도 공유이므로 던지기 전 `nvidia-smi`.

**⛔ 이 파일럿이 답하지 않는 것**: M ≥ 4 committee. §7c 대로 이 스케줄에서는 준독립 스냅샷이 안 나온다.
**모델 불확실도 축은 이 파일럿으로 안 닫힌다** — fine-tune 은 그 문제의 *전제조건*(단일 아키텍처 committee 가능성)일 뿐,
실제로 M≥4 를 만들려면 400+ epoch·EMA off·순환 LR 이라는 **별도 설계**가 필요하다.

---

## 16. 인용 가능 문장 (deck/원고용)

- *"Liu et al. 의 U-MLIP fine-tuning 튜토리얼(J. Appl. Phys. 2026)은 티오포스페이트 고체전해질 Li₁₀GeP₂S₁₂ 에서
  세 MACE 파운데이션(MP-0b3·MPA-0·OMAT-0)이 **동일 하이퍼파라미터로 힘 RMSE 14.9–15.8 meV/Å 로 수렴**함을
  보였다 — 출발 체크포인트 선택이 최종 정확도를 크게 좌우하지 않는다."* (소환값)
- *"같은 연구에서 힘 손실 가중을 1→100 으로 올리면 힘 RMSE 가 **18.71 → 14.80 meV/Å (−20.9%)** 개선되나,
  그 이득의 대부분(−15.6%)이 이미 가중 10 에서 실현된다."* (Table V, 3시드 평균; 개선율은 digest 계산)
- *"BCC Mo 에서 fine-tune 전 MACE-MP-0b3 는 C₁₁ 을 **45%**, C₄₄ 를 **52%** 과소평가했고
  (251 vs DFT 459 GPa; 47 vs 97 GPa), fine-tuning 이 이를 452 / 82 GPa 로 회복시켰다 —
  범용 MLIP 의 탄성 연화가 정량적으로 확인된 사례."* (Table VI, DFT 기준 열)
- ⚠ *"단, 같은 논문의 GSFE(Fig. 7)에서 fine-tuned 모델은 DFT 를 **12–14% 초과**한다 —
  연화의 교정이 과교정으로 넘어간다."* (figure-read + digest 계산)
- ⚠ *"fine-tuning 의 데이터효율 이점은 **에너지에서는 전 구간, 힘에서는 데이터가 적을 때만** 성립한다.
  훈련 데이터 75–100% 구간에서는 scratch 학습이 힘 RMSE 에서 fine-tuned 모델들을 앞선다."*
  (Fig. 4b, **figure-read** — 논문 본문은 반대로 서술한다)
- ⛔ **인용 금지**: 이 논문의 **절대 에너지 RMSE**. Fig. 2 와 Table IV 가 정확히 10× 어긋나고
  어느 쪽이 옳은지 PDF 로 확정 불가 (§14-1). 상대 개선폭만 쓴다.
- ⛔ **인용 금지**: *"이 튜토리얼로 UMA 를 fine-tune 할 수 있다"* — **UMA 는 Table I 의 한 줄일 뿐
  실험이 0건**이고, MACE 의 `run_train.py` 는 아키텍처 하드락이다 (repo 실측).

---

## 17. ⛔ 못 하는 것 / 확인 못 한 것

**이 digest 가 확인하지 못한 것**
1. **실행 검증 0.** 이 환경에 `torch`·`dpdata`·`e3nn` 이 없어 **fine-tune 을 한 번도 돌리지 못했다.**
   코드 로직은 **읽어서** 판정한 것이지 실행해서 확인한 게 아니다. (`ase`·`numpy` 로 **데이터 포맷만 실제로 열어 봤다**.)
2. **MACE 버전 불일치 위험.** §4b(D)의 multi-head 강제 OFF·lr 덮어쓰기는 **v0.3.17(2026-08-31 커밋)** 기준이다.
   저자들이 쓴 버전(2025년)에서 다르게 동작했을 수 있다. **우리 환경 버전에서 재확인 필요.**
3. **fairchem 이 UMA fine-tune 을 지원하는지 확인하지 않았다.** 이건 이 논문의 범위 밖이라
   조사하지 않았다. §15e 단계 0 이 그 조사다.
4. **논문의 Listing 1–5 원문을 못 읽었다.** PDF 에서 코드 리스팅이 **이미지**라 텍스트 추출이 안 된다.
   §4b 의 하이퍼파라미터는 **저장소의 실물 스크립트**에서 가져왔다 — Listing 1 과 값이 다를 수 있다.
5. **참고문헌 대조 안 함.** ref 80(DPAISquare LGPS 데이터) · ref 84(ACE 불확실도 필터) ·
   ref 113(Si 데이터) · ref 114(Mo 데이터) · ref 127/129/131(계면 데이터) 원문을 확인하지 않았다.
6. **§14-1 의 10× 에너지 불일치를 해소하지 못했다.** 어느 쪽이 옳은지 이 PDF 만으로 판정 불가.
7. **그림 9장 중 5장만 실제로 봤다** (아래).

**이 논문이 답하지 않는 것 (논문의 한계 — §IV 의 저자 자인 + 우리 관측)**
- 저자 자인: ① **최적 fine-tune 전략의 종합 벤치마크가 없다** (§II A 2) ② **하이퍼파라미터 자동 최적화가 없다**,
  최적값 탐색이 *"nontrivial and computationally demanding"* (§III A) ③ **최적 설정은 계마다 다르다** (§III F)
  ④ **active learning 반복이 catastrophic forgetting 을 일으킬 수 있고 그 완화는 미해결** (§II B 2, §IV A)
  ⑤ MLIP 은 물리법칙을 내장하지 않고 **데이터 커버리지가 정확도를 결정한다** (§IV)
  ⑥ **RMSE 를 넘는 벤치마킹 플랫폼이 필요하다** (§IV C, MLIP Arena 언급) ⑦ **모델 증류는 향후 과제** (§IV D)
  ⑧ 장거리 물리를 암묵적으로 포착하는 현상은 **case-by-case** (§III E/F) ⑨ 흡착에너지 같은
  task-specific 물성 평가는 **future work** (§III E)
- 우리 관측 추가: ⑩ **fine-tune 후 사전학습 분포 성능 유지를 한 번도 재지 않았다** (§6b — 우리에게 제일 치명적)
  ⑪ **LGPS 에 zero-shot 행이 없어 개선폭을 알 수 없다** (§10a)
  ⑫ **학습 wall-clock 이 전혀 없다** (§9a) ⑬ **동결·LoRA 실측 0건** (§4a)
  ⑭ **무질서(site disorder) 를 다루지 않는다** — 우리 argyrodite 물리의 중심축이 통째로 빠져 있다
  ⑮ **할로겐 함유 전해질이 없다** (LGPS 에 Cl 없음; LiCl/GaF₃ 는 계면이지 전해질 아님)

**본 그림 / 안 본 그림**
- ✅ **실제로 본 것 (5장)**: **Fig. 1**(워크플로) · **Fig. 2**(손실곡선+parity) · **Fig. 4**(데이터효율) ·
  **Fig. 5**(Si OOD) · **Fig. 7**(GSFE) · **Fig. 9**(그래핀–물) — 6장이다.
- ⛔ **안 본 것 (3장)**: **Fig. 3**(LGPS 구조) · **Fig. 6**(Mo 전위 구조) · **Fig. 11**(계면 구조) —
  전부 **원자구조 렌더링**이라 수치 정보가 없어 건너뛰었다.
- ⚠ **크로핑 실패 (1장)**: **Fig. 10** (Au–MgO / TiO₂–NaCl RMSE) 은 추출 도구가
  *"그래픽 없음(img0/draw0)"* 으로 제외했다 — p16 에 벡터/래스터 객체가 안 잡혔다.
  **그래서 Fig. 10 의 막대값을 읽지 못했고, §10e 는 캡션과 본문 서술로만 썼다.**
- **본문 서술과 어긋난 그림 3건**: Fig. 4(§8c) · Fig. 7 부호(§10c) · Fig. 9 시간축(§9b).
  전부 §14 에 기록했다.

---

## 18. 기법 용어 미니사전

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **U-MLIP** | universal / foundation MLIP. 주기율표 전반의 대규모 데이터로 사전학습된 범용 원자간 퍼텐셜 | 주제 그 자체. Table I 에 12종 |
| **MACE** | ACE(원자군집전개)를 **등변(equivariant) 메시지패싱 그래프망**으로 구현. 층이 **단 2개**인데도 각 층이 텐서곱으로 다체 상관을 직접 인코딩해 표현력을 확보 | 중심 모델. 부록 A 에 식 (A1)–(A7) |
| **L = 0 / 1 / 2** | 메시지패싱의 **등변 차수**(구면조화 차수). 클수록 표현력↑·비용↑ | **L=1 (medium) 권장** |
| **stage one / stage two** | 2단계 학습. stage two 는 곧 **SWA** 구간이며 **에너지 손실 가중을 크게 올린다** | 전환점 = `max_epochs//4*3` (150→**111**) |
| **SWA** | Stochastic Weight Averaging. 학습 후반 가중치를 평균해 더 평평한 극소로 | `--swa`, `--swa_lr 5e-4`, `--swa_energy_weight 100` |
| **EMA** | Exponential Moving Average. 가중치의 지수이동평균으로 최적화 잡음 평활 | `ema_decay` 0.98–0.99999. **체크포인트가 EMA 값으로 저장된다**(§7b) |
| **multi-head fine-tuning** | 공유 백본에 **task 별 출력 head** 를 여러 개. 사전학습 head 를 유지해 catastrophic forgetting 완화 | Si 예제 FT vs FT-SH. 기본 백본은 **학습 가능** 상태 |
| **replay / `num_samples_pt`** | 사전학습 데이터를 일부 **다시 먹여** 지식을 붙잡는 것. 크면 보존↑ 적응력↓ | MACE 기본 10000, 튜토리얼 스크립트 500 (⚠ 실제로는 비활성 — §4b D) |
| **catastrophic forgetting** | 새 과제를 배우며 이전 지식을 잃는 현상 | **정성적으로만** 4회 언급. 정량 0 |
| **OOD** | out-of-distribution. 훈련분포 밖 | Si 예제. ⚠ **구조 OOD 이지 화학 OOD 아님** |
| **snapshot ensemble** | 한 학습 궤적의 여러 epoch 모델을 앙상블로. 훈련 1회로 committee | 이 논문엔 없다. 우리가 §7 에서 가능성을 따진 것 |
| **GSFE** | generalized stacking fault energy. 슬립 경로를 따라 결정면을 미끄러뜨릴 때의 에너지 곡면 | Fig. 7, Table VII. **PES 경도의 민감한 시험대** |
| **relative F (%)** | 힘 RMSE ÷ DFT 힘 성분의 표준편차 | **σ_F = 840.3 meV/Å** (repo 실측으로 확인, §8a) |
| **cuEquivariance** | NVIDIA 의 등변 신경망 CUDA 커널 (segmented tensor product). 추론 가속 | 2900원자 **1.94×**. 128원자에선 **오히려 느림** |
| **CACE-LR** | latent Ewald summation 으로 **장거리를 명시적으로** 넣은 MLIP | Table IX·Fig. 10 의 **비교 기준선**이자 데이터 제공자 |
| **RBMD** | 저자들의 random-batch 분자동역학 플랫폼. 단일 GPU 로 10⁷ 입자급 | §IV 의 향후 통합 대상. 이 논문 결과에는 미사용 |
| **DPAISquare** | DeePMD 커뮤니티 공개 데이터 플랫폼 | LGPS 데이터 출처 (ref 80) |

---

## 19. 관련 문서

- `litdb/papers/kurniawan2025_comparative_ensemble_uq_nnip.md` — snapshot 앙상블의 **100-epoch 간격** 요건과
  *"snapshot ≈ random-init 성능인데 훈련 1회"* 논거. **§7 판정의 근거**
- `litdb/papers/grasselli2025_uncertainty_era_ml_atomistic.md` — 식 (27) 편향보정 **M ≥ 4** 하한.
  **§15b 가 답해야 했던 질문의 출처**
- `litdb/talks/lee2026_skku_mlip_materials_design.md` §슬 8 (A1: *uMLIP PES 는 평형 근처에 치우쳐 고에너지에서
  물러지고, fine-tuning 으로 되돌린다*) — 🎤 **이 논문이 그 명제의 정량 근거를 처음 제공한다**
  (Mo C₁₁ −45% / C₄₄ −52% → 회복, Table VI). ⚠ 단 **"되돌린다"가 아니라 "지나쳐 되돌린다"**(GSFE +12~14%, §10c).
  ⛔ talk 은 citable=no 이며, **이 digest 를 talk 에 반영하는 것은 이번 작업 범위 밖**이다(§20).

---

## 20. ⚠ 이 digest 의 작업 범위 제한 (동시 실행 충돌 회피)

다른 litdb-curator 와 동시에 도는 세션이라 **`litdb/papers/liu2026_finetuning_umlip_tutorial.md` 와
`litdb/figures/liu2026_finetuning_umlip_tutorial/` 만** 썼다.

**아직 안 된 것 (다른 세션이 하거나, 나중에 손으로):**
- `litdb/INDEX.md` 행 추가 → **`litdb/_pending_index_liu2026_finetuning_umlip_tutorial.md` 에 초안**
- `litdb/comparison_vs_ours.md` — **⛔ 물성 4축 표에 넣지 말 것.** 이 논문은 이온전도·산화안정·기계·전자구조
  **어느 축에도 우리 계의 값을 주지 않는다.** `🔧 방법 원전` 블록으로 따로 둔다 (초안은 pending 파일에)
- `litdb/talks/lee2026_skku_mlip_materials_design.md` §슬 8 역링크 — **초안만 pending 파일에**
- git commit/push — 이번 세션 범위 밖


> ⛔ **2026-09-09 정정 — 지표가 섞였다.** 여기 쓴 우리 값 **44.58 meV/Å 는 RMSE** 다.
> `db/properties/mlip_bench_li3ps4_uma.json` 실측: **MAE 29.97** / **RMSE 44.58** eV/Å×10⁻³.
> (조율 세션이 큐레이터 프롬프트에 RMSE 를 MAE 라고 넘겼다 — 내 오기다.)
> ⚠ **그냥 29.97 로 바꾸면 안 된다.** 저쪽 zero-shot 값(126.07 · 179.2 · 171.3)이
> MAE 인지 RMSE 인지 **이 digest 로는 확정 안 됐다.** 같은 지표끼리 대야 하므로,
> 저쪽 지표를 원문에서 확인하기 전까지 **배수(≈3×)는 잠정**이다.
> · 저쪽이 MAE 라면 우리 상한은 29.97/15.3 ≈ **2.0×** 로 더 내려간다
> · 저쪽이 RMSE 라면 44.58/15.3 ≈ 2.9× 가 맞다
> 어느 쪽이든 **'우리 출발점이 더 좋다 → 기대치를 낮춰라'** 는 결론은 안 바뀐다.
