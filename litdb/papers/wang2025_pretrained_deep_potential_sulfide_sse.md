# A pre-trained deep potential model for sulfide solid electrolytes with broad coverage and high accuracy (DPA-SSE) — Wang et al. (npj Comput. Mater. 2025)

> slug `wang2025_pretrained_deep_potential_sulfide_sse` · DOI `10.1038/s41524-025-01764-6` · type `MLIP (모델 논문) + DFT 라벨링 + MLIP-MD + NEB` · PDF `dc978d7f-90._A_pretrained_deep_potential_model…pdf` (+SI `ad74839f-90._Sup_…pdf`) · digested `2026-09-09` · status ✅
> elements: Li, B, O, Al, Si, P, S, Cl, Ga, Ge, As, Br, Sn, Sb, I
> methods: DFT, AIMD, MD, MLIP, NEB
> **서지 (표지 대조 완료)**: Ruoyu Wang¹²³†, Mingyu Guo⁴⁵†, Yuxiang Gao¹², Xiaoxu Wang⁴⁶, Yuzhi Zhang⁴⁶, Bin Deng⁴, **Mengchao Shi**³⁴\*, **Linfeng Zhang**⁴⁶\*, **Zhicheng Zhong**¹²³\* — ¹USTC 인공지능·데이터과학부(허페이) ²USTC 쑤저우고등연구원 ³Suzhou Lab ⁴**DP Technology**(베이징) ⁵중산대 화학 ⁶AI for Science Institute. †공동 1저자 2인.
> ***npj Computational Materials* (2025) 11:266**, 본문 10 pp · SI 10 pp · Fig 7 + S1–S12 · **Table 0개** · refs 50 + SI refs 4. 접수 2025-07-24 / 수락 2025-08-04. OA **CC BY-NC-ND 4.0**.
> ✏ **1저자 기억과의 대조**: 저자 순서 `R. Wang, M. Guo, Y. Gao, X. Wang, Y. Zhang 외` · 저널 `npj Comput. Mater. 2025` — **전부 맞다**. 다만 교신은 Wang 이 아니라 **Shi / L. Zhang / Zhong** 3인이고, 이 논문의 실질 소속 축은 **DP Technology(DeePMD 개발사)** 다. 즉 **자기 프레임워크(DPA-2)로 자기 프레임워크를 벤치마크한 논문**이라는 이해충돌 축이 있다(§13-1).
> 🎤 **관련 발표**: 없음. `litdb/talks/lee2026_skku_mlip_materials_design.md` §99-10 인입 대기열 6건(+3건 추가)을 전수 확인했으나 **이 논문은 그 표에 없다** — talk 역링크 대상이 아니다.

---

## 0. 이 digest를 읽는 법

- 이 편은 **물성 논문이 아니라 "포텐셜(도구) 논문"**이다. 여기 나오는 σ·D·Ea 는 *그 도구가 잘 도는지 보여주려고* 낸 시연값이고, 조성 최적화를 주장하는 값이 아니다. **우리 db 절대값과 섞지 않는다.**
- **★ 우리가 이 편을 읽는 이유는 딱 하나다**: 우리는 전 MD 를 **UMA-s-1p1(omat)** 로 돌리는데, 오늘 들어온 UQ 3편(Grasselli / Carrete / Kurniawan)이 *"단일 파운데이션 모델로는 committee 를 못 만든다"* 를 공통으로 짚었다. DPA-SSE 가 **(1) UMA 의 대체 / (2) committee 네 번째 멤버 / (3) UMA 검증의 독립 기준** 중 무엇이 될 수 있는지 — 그 판정이 §11 이다. **§11 이 본론이고 §1–10 은 그 근거다.**
- **표기 규약**: 본문에 명시된 수 = 그대로. 내가 그림 눈금에서 읽은 수 = **`figure-read ≈`**. 내가 이 논문 수로 계산한 것(원논문에 없음) = **`digest 계산 (원논문 미보고)`**.
- 이 논문에는 **표가 하나도 없다**. 모든 수치는 본문 산문 또는 그림 눈금에서만 나온다 — 그래서 `figure-read` 표기가 유난히 많다. 그 자체가 이 논문의 한계다(§13-2).

---

## 1. 한 줄 요약

범용 MLIP(MACE·M3GNet·CHGNet·DPA-2-MP)는 **평형 근처 데이터로만 학습돼 Li 호핑 안장점 같은 비평형 구조의 에너지를 과소평가**하고, 그 결과 **황화물 SE 의 상온 확산계수를 1–2 자릿수 과대평가**한다. 이 논문은 **황화물 SE 전용**으로 15원소·41계·54,771 스냅샷(NPT 0–1200 K / 0–2 GPa 로 **일부러 비평형까지 샘플링**)을 DP-GEN 능동학습으로 모아 **DPA-2 아키텍처**에 학습시킨 `DPA-SSE` 를 내놓았다 — 에너지 MAE **1.58 meV/atom**, 힘 MAE **30.28 meV/Å**, 1150 K 가열궤적까지 유지, 그리고 **훈련에 없는 고용체(Li₆PS₅Cl₁₋ₓ₋ᵧBrₓIᵧ 등)에서도 MAE 가 그대로**(1.56 meV/atom / 29.15 meV/Å).

덤으로 **① fine-tune**(미학습 Li₂B₂S₅ 에 20 프레임이면 zero-shot 162.65 → 3.44 meV/atom, 60 프레임이면 from-scratch 760 프레임을 이김), **② distillation**(무거운 attention 모델 → 가벼운 DeePMD 학생 모델, 정확도 2.10 meV/atom 로 소폭 손실 · 속도 **~520×**)을 보여준다.

---

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 저널/년 | npj Computational Materials **11**, 266 (2025) |
| DOI | 10.1038/s41524-025-01764-6 |
| 모델 이름 | **DPA-SSE** (Deep Potential with Attention — Solid State Electrolyte) |
| 아키텍처 | **DPA-2** (Zhang et al., npj Comput. Mater. **10**, 293 (2024)) |
| 다루는 계 | LGPS 계열 Li₁₀XY₂S₁₂ (X=Ge,Sn,Si; Y=P,Ga,Sb,As) · **argyrodite Li₆PS₅X (X=Cl,Br,I)** · Li₇P₃S₁₁ + 그 분해산물 + Li 금속 |
| 연구유형 | MLIP 개발 + 벤치마크 (실험 없음, 실험값은 문헌 인용으로만 비교) |
| 공개 | **모델·훈련데이터 AIS Square 공개** (§9-5) |

**동기 문장(그대로)**: *"current universal force fields usually struggle to accurately predict out-of-equilibrium states critical to ionic transport, such as Li-hopping transition states, and lack the quantitative accuracy required for electrolytes simulation."*

⇒ 즉 이 논문의 적은 "범용 MLIP 가 부정확하다"가 아니라 **"범용 MLIP 의 훈련 분포가 평형에 치우쳐 있다"** 는 훨씬 구체적인 진단이다. 이 진단이 UMA 에도 적용되는지가 우리 질문이고, 이 논문은 **UMA 를 시험하지 않았다**(§13-4).

---

## 3. 핵심 수치 총정리

### 3.1 모델·데이터 규모

| 항목 | 값 | 출처 |
|---|---|---|
| 훈련 스냅샷 | **54,771** frames (E + F + virial 라벨) | Methods |
| 계(system) 수 | **41** — 이 중 Li 함유 사슬/사원 황화물 **26** + 이원 부분계 14 + Li 금속 1 | Fig. 1, 본문 (26/14/1 분해는 `digest 계산 (원논문 미보고)` — 논문은 "41 systems, 26 chalcogenides" 만 씀) |
| 원소 | **15**: Li, B, O, Al, Si, P, S, Cl, Ga, Ge, As, Br, Sn, Sb, I | Fig. 1 주기표(색 없는 칸 C·N·F·Se·In·Te 는 카운트 0) |
| 샘플링 조건 | NPT **0–1200 K**, **0–2 GPa** (DP-GEN 능동학습 반복) | Methods |
| 데이터 빈도(Fig. 1 heatmap) | 상한 60,000 · **Li·S·P 가 최고농도**, B·O·Al·Si·Ge 중간, **Cl·Ga·As·Sn·Sb 는 옅다** `figure-read` | Fig. 1 |

### 3.2 정확도 (DFT = PBEsol/VASP 대비)

| 시험 | E MAE | F MAE |
|---|---|---|
| 표준 test set (전 41계) | **1.58 meV/atom** (Fig. 2a 패널 내 표기는 **1.57**) | **30.28 meV/Å** |
| 6 전해질 가열궤적 150→1150 K | 본문 *"within 2 meV/atom"* — ⚠ **Fig. 2c 의 LSnPS 는 `figure-read ≈ 2.5`** 로 이 문장을 넘는다 | 본문 *"within 30 meV/Å"* |
| 고용체(훈련에 없음) LXPS·LPSX | **1.56 meV/atom** | **29.15 meV/Å** |
| 증류(distilled) 모델, 900 K AIMD 궤적 | **2.10 meV/atom** (교사 1.59) | **48.44 meV/Å** (교사 30.0) |

### 3.3 범용 모델 대비 (★ 우리 관심)

**(a) 평형 근처** (50 K DeePMD 10 스텝) — `Fig. S1a,b`, 전부 **fine-tune 안 한 base 모델**:

| 계 | DPA-2-MP | MACE | M3GNet | CHGNet | **DPA-SSE** |
|---|---|---|---|---|---|
| **LPSCl** E MAE (meV/atom) | ≈14 | ≈10.2 | ≈14.5 | ≈7.5 | ⚠ **막대가 아예 없다** |
| **LPSCl** F MAE (meV/Å) | **≈79** | ≈23.2 | ≈19.7 | ≈29.8 | **≈4.2** |
| LPSBr F MAE | ≈63.5 | ≈25.3 | ≈18.7 | ≈32 | ≈4.9 |
| LPSI F MAE | ≈81 | ≈25.5 | ≈22.9 | ≈39.4 | ≈5.2 |
| LGePS F MAE | ≈51 | ≈28.8 | ≈18.6 | ≈27.9 | ≈6.0 |

전부 `figure-read ≈`. **LPSCl 의 DPA-SSE 에너지 막대 누락은 §13-3.**

**(b) 가열궤적** (150→1150 K) — `Fig. S1c,d`, 역시 base 모델:

| 계 | DPA-2 | MACE | M3GNet | CHGNet | **DPA-SSE** |
|---|---|---|---|---|---|
| **LPSCl** E MAE (meV/atom) | ≈11.3 | ≈11.3 | ≈33 | ≈31 | **≈1.65** |
| **LPSCl** F MAE (meV/Å) | ≈181 | ≈126 | ≈45 | **≈24** | ≈31 |
| LGePS E / F | ≈40 / 201 | ≈27 / 165 | ≈45 / 83 | ≈44 / 119 | ≈1.7 / 29 |
| LSnPS E / F | ≈42 / 205 | ≈26 / 161 | ≈51 / — | ≈47 / — | ≈2.6 / 33 |

전부 `figure-read ≈`. ⚠ **LPSCl 힘에서만 CHGNet base(≈24)가 DPA-SSE(≈31)를 이긴다** — 41계 전체에서 유일한 역전이고, 하필 **우리 계**다(§13-3).

**(c) fine-tune 후** (`Fig. 2c,d`, DPA-SSE 데이터셋으로 4 epoch) — 전부 `figure-read ≈`:

| 계 | DPA-SSE | DPA-2-MP-ft | M3GNet-ft | MACE-ft |
|---|---|---|---|---|
| **E MAE (meV/atom)** LGePS / LPSBr / **LPSCl** / LPSI / LSiPS / **LSnPS** | 1.55 / 0.90 / **1.55** / 0.72 / 1.40 / **2.55** | 1.55 / 0.88 / 2.4 / 1.0 / 2.6 / 3.8 | 3.4 / 5.1 / 8.5 / 3.8 / 4.3 / 6.9 | 2.4 / 4.5 / 3.15 / **5.8** / 3.1 / 2.6 |
| **F MAE (meV/Å)** 같은 순서 | 25 / 26 / **28** / 22 / 24 / 29 | 35 / 30 / 33 / 24 / 34 / 41 | **108 / 73 / 82 / 60 / 103 / 118** | 40 / 33 / 43 / 29 / 29 / 38 |

세 범용 모델 모두 DPA-SSE 수준으로 좁혀지고 **M3GNet-ft 만 힘에서 크게 남는다**(60–118 vs DPA-SSE 22–29). 논문 해석 = 모델 크기·사전학습 데이터가 작아서.
⚠ 두 가지 어긋남: ① **LSnPS 의 DPA-SSE 가 2.55 meV/atom** — 본문 *"within 2 meV/atom"* 을 넘는다. ② 본문은 *"fine-tuned M3GNet exhibits larger errors than fine-tuned MACE and DPA-2-MP"* 라고 쓰는데, **에너지에서는 LPSI 의 MACE-ft(5.8)가 M3GNet-ft(3.8)보다 나쁘다.** (본문이 *"particularly in force predictions"* 로 헤지하긴 한다 — 힘에서는 주장이 성립한다.)

### 3.4 이온 수송 (LGPS · NEB)

| 항목 | 값 |
|---|---|
| c축 협동 호핑 장벽 (DPA-SSE) | **0.28 eV** (본문) — ⚠ `Fig. 5a` 눈금 `figure-read ≈ 0.31` |
| ab면 kick-off 장벽 (DPA-SSE) | **0.36 eV** (본문) — `Fig. 5b` `figure-read ≈ 0.37` |
| c축 장벽 (DFT PBE 참조) | `figure-read ≈ 0.345` |
| ab면 장벽 (DFT PBE 참조) | `figure-read ≈ 0.35` |
| **base 범용모델 c축 장벽** | `figure-read ≈ 0.12` (M3GNet base) · `≈ 0.20` (DPA-2-MP base) — **DFT 의 1/3 수준** |
| **base 범용모델 ab면 장벽** | `figure-read ≈ 0.115–0.12` — **DFT 의 1/3** |
| LGPS D(300 K) DPA-SSE | `figure-read ≈ 4.5×10⁻¹² m²/s` (1000/T = 3.33) |
| LGPS D(≈286 K) 실험 | `figure-read ≈ 2×10⁻¹² m²/s` (1000/T = 3.5) |
| **LGPS D(300 K) base 범용모델** | `figure-read ≈ 1.3×10⁻¹⁰`(MACE) · `≈3.2×10⁻¹⁰`(DPA-2-MP) · `≈1×10⁻⁹`(M3GNet) — **DPA-SSE 대비 30–220×** |

### 3.5 이온 전도도 (MD · Nernst–Einstein)

**`Fig. 6c,d` — 5개 계 상온값, 전부 `figure-read ≈`:**

| 계 | σ₃₀₀K DPA-SSE (mS/cm) | σ₃₀₀K 실험 | Ea DPA-SSE (eV) | Ea 실험 |
|---|---|---|---|---|
| LSiPS | ≈6.5 | ≈2.3 | ≈0.22 | ≈0.22 |
| LGePS | ≈9 | ≈12.5 | ≈0.21 | ≈0.28 |
| LSnPS | ≈10 | ≈5.0 | ≈0.20 | ≈0.26 |
| **LPSCl** | **≈7** | **≈3.0** | **≈0.24** | **≈0.324** |
| LPSBr | ≈8.3 | ≈5.3 | ≈0.20 | ≈0.225 |

⇒ 논문은 *"excellent agreement"* 라고 쓰지만, **중앙값 기준으로는 5계 중 4계에서 σ 를 1.6–2.8× 과대**, **Ea 를 0.02–0.08 eV 과소**한다. 오차막대가 커서 겹칠 뿐이다(§13-5).

**`Fig. S10a` — Li₆₋ₓPS₅₋ₓCl₁₊ₓ (= 우리 modelc 계열!)** `figure-read ≈`:

| x | 0 | 0.3 | 0.5 | 0.7 |
|---|---|---|---|---|
| DPA-SSE σ₃₀₀K (mS/cm) | ≈7.8 | ≈11.0 | ≈11.8 | ≈15.7 |
| 실험 (Feng 2020) | ≈7.1 | ≈9.2 | ≈16.1 | ≈17.3 |

> **우리 modelc = Li₅.₄PS₄.₄Cl₁.₆ 는 정확히 x = 0.6 이다.** 논문은 x=0.6 점을 안 찍었지만 0.5(≈11.8)와 0.7(≈15.7) 사이 — 선형보간 **≈13.7 mS/cm** `digest 계산 (원논문 미보고)`. ⛔ 이 보간값은 소환값이고 우리 db 에 넣지 않는다.

**`Fig. S10b` — Li₆₋ₓPS₅₋ₓClBrₓ** `figure-read ≈`: DPA-SSE 4.6(x=0.1) / 10.4(0.3) / 15.5(0.5) / 18.6(0.7); 실험(속빈 마름모) 5.0(0) / 12.0(0.3) / 17.0(0.5) / **24.0(0.7)**, 실험(채운 마름모) 14.1(0.7). ⇒ **같은 조성에 실험값이 두 개**(24.0 vs 14.1, 출처 다름) — 실험 기준선 자체가 1.7× 흔들린다.

**`Fig. S11` — Li₅.₅PS₄.₅₋ₓOₓCl₁.₅ (= 우리 O 도핑계!)** `figure-read ≈`:

| x(O) | 0 | 0.10 | 0.20 | 0.30 |
|---|---|---|---|---|
| DPA-SSE σ₃₀₀K (mS/cm) | ≈11.8 | ≈10.4 | ≈8.8 | ≈7.0 |
| 실험 (Peng 2022) | ≈9.5 (x=0) | ≈7.2 (x≈0.075) | ≈6.4 (x≈0.175) | ≈6.0 (x=0.25) |

⇒ **O 도핑은 σ 를 단조 감소시킨다** — 계산·실험 둘 다. DPA-SSE 는 x=0→0.30 에서 **−41%**, 실험은 x=0→0.25 에서 **−37%** `digest 계산 (원논문 미보고)`. **기울기는 맞고 절댓값이 ~1.2–2.5 mS/cm 높다.**

**`Fig. 6a` — Li₁₀SiₓGe₁₋ₓP₂S₁₂** `figure-read ≈`: 실험 7.6/6.3/4.2/3.15/2.25 (x=0/0.3/0.5/0.7/1.0) vs DPA-SSE 7.3/5.4/5.25/4.7/3.25. 추세(Si↑ → σ↓)는 재현, 중간 조성에서 과대. **DPA-SSE 오차막대가 ±30–40%** 로 매우 크다.

### 3.6 무질서 (★ 우리 4a/4c 축)

`Fig. 6b` — Li₆PS₅Cl 상온 MD, **5,000 ps(5 ns)** 궤적:

| 배열 | Li MSD @5 ns | 퍼텐셜에너지 |
|---|---|---|
| **무질서** (`50%@4c`) | **≈38 Å² 이고 여전히 선형 증가** | **≈ −5.604 eV/atom** |
| **질서** (`order`) | **≈11.5 Å² 에서 ~1 ns 이후 포화** (장거리 수송 없음) | ≈ −5.5965 eV/atom |

⇒ 무질서상이 **≈7.5 meV/atom 더 안정** (두 `figure-read` 눈금값의 차 — `digest 계산 (원논문 미보고)`). 논문 해석: LPSCl 실험에서 무질서상이 합성되는 것과 일치. 반대로 **LPSI 는 질서상이 더 낮아**(`Fig. S9`, 나는 안 봄) 전도도가 낮은 이유를 설명한다고 주장.

### 3.7 열역학·구조

- `Fig. S4`: 41 화합물 완화 격자상수, DPA-SSE vs DFT, **2.5–22.5 Å 범위에서 대각선 위**. ⚠ 축 범위가 20 Å 이라 **~1% 오차(10 Å 에서 0.1 Å)는 이 그림에서 안 보인다**(§13-6).
- `Fig. S5a`: 22 화합물 분해에너지 −2.75 ~ **+0.65 eV/f.u.**, 전부 대각선. 범례에 **`Li12P2S10Cl2` = Li₆PS₅Cl ×2** 가 들어 있다 → **argyrodite 분해에너지가 벤치마크에 포함**. ⚠ 범례 색이 10색 순환이라 **개별 점의 정체를 그림에서 특정할 수 없다** — "LPSCl 의 분해에너지가 얼마" 라고 쓰면 안 된다.
- `Fig. S5b`: xLi₂S–(1−x)P₂S₅ 볼록껍질. `figure-read ≈` x=0.7 (Li₇P₃S₁₁) −0.254 / **x=0.75 (Li₃PS₄) −0.264 (최저)** / x=0.875 (Li₇PS₆) −0.143 eV/atom. DPA-SSE 와 DFT 가 **완전히 겹친다**.

### 3.8 효율 (★ 우리 비용 판정의 근거)

`Fig. 7` — LGPS **1350 원자**, **V100 1장 + CPU 12코어**, 단위 s/(step·atom) `figure-read ≈`:

| 모델 | s/(step·atom) | DPA-SSE 대비 |
|---|---|---|
| **DPA-SSE / DPA-2-ft (사전학습 원본)** | **≈8.6×10⁻³** | 1× |
| MACE-ft | ≈1.85×10⁻⁴ | **46× 빠름** |
| M3GNet-ft | ≈1.13×10⁻⁴ | **76× 빠름** |
| **Distilled DPA-SSE** | **≈1.65×10⁻⁵** | **≈520× 빠름** |
| NVNMD\* (전용 하드웨어) | ≈8.7×10⁻⁷ | ≈9900× 빠름 |

⇒ **사전학습 DPA-SSE 는 MACE 보다도 46× 느리다.** 이게 §11-4 비용 판정의 핵심이다.

### 3.9 보존성 (★ 우리 UMA 점검 항목)

`Fig. S3` — LGPS 를 500 K NVT 로 데운 뒤 **NVE 100 ps**:

- **orb-v2 (비보존 = 힘이 에너지의 도함수가 아님)**: ΔE 가 ~15 ps 부터 오르기 시작 → 50 ps 에 ≈2 eV/atom → 55 ps 에 **≈6–7 eV/atom 으로 점프하고 그대로** `figure-read ≈`. **계가 사실상 폭발했다.**
- **DPA-SSE · MACE (보존)**: 100 ps 내내 ΔE ≈ 0.

본문은 이 때문에 벤치마크 대상을 **보존형(conservative) 힘장으로만 한정**했다고 명시한다.

---

## 4. 재료 & 방법

### 4.1 DFT 라벨링 (훈련 데이터)

| 항목 | 값 |
|---|---|
| 코드 | **VASP** (ref 46 = Kresse & Furthmüller 1996) |
| 유사포텐셜 | **PAW** |
| 범함수 | **PBEsol** — ⚠ **인용은 ref 47 = Perdew, Burke, Ernzerhof PRL 77, 3865 (1996) 로 되어 있는데 그건 PBE 논문이다**(§13-1) |
| ecut (평면파) | **600 eV** |
| 힘 수렴 | **0.01 eV/Å** (원자좌표 완화) |
| k-점 | **KSPACING = 0.3** (전 계 동일 격자 보장 목적) |
| 라벨 | 에너지 · 힘 · **virial** |
| 데이터 생성 | **DP-GEN 능동학습** (ref 45 = Zhang et al. PRM 3, 023804 (2019)); 초기 = 무작위 섭동 구조의 짧은 AIMD, 이후 반복은 **NPT 0–1200 K / 0–2 GPa** |
| **무질서 처리** | ⚠ **명시 없음.** argyrodite 4a/4c S/X 혼합을 어떻게 배열했는지(SQS? enumerate? 무작위 decorate?) 논문 어디에도 안 나온다. `Fig. 6b` 의 `50%@4c` 라벨과 `Fig. 6b` inset(S 4c / Cl 4a / S 16e)이 유일한 단서다(§14-2) |

### 4.2 모델 (DPA-SSE)

- 프레임워크 **DPA-2** — 로컬 디스크립터 `D_i` 를 단원자 채널 `f_i` + 회전불변 원자쌍 채널 `g_ij` + 회전등변 채널 `h_ij` 로 만들고 transformer 층을 통과시킴. `E = Σ_i E_i(R)`, **힘은 E 의 좌표 미분** → **보존형(conservative)**.
- 디스크립터: **repinit 1층** (은닉 25/50/100) + **repformer 12층**. repinit **cutoff 9.0 Å**. 단원자 표현 차원 8. **attention head 4개**. 임베딩 연결 MLP 25/50/100.
- 피팅망: **3층 × 240 뉴런**.
- 학습률 — ⚠ **같은 문단에 서로 다른 두 스케줄이 적혀 있다**: ① *"initial 0.001 → 3.51×10⁻⁸ after 12,000,000 steps, interval 60,000"* ② *"starts with 2×10⁻⁴, exponential decay every 10,000 steps, → 3×10⁻⁸ at 2,000,000 step"*. 어느 것이 DPA-SSE 본체인지 불명(§13-1).
- 손실 계수: 에너지 0.02→1, virial 0.2→1, **힘 1000→1** (힘 우선 → 에너지 우선으로 전환).

### 4.3 범용 모델 fine-tune (비교군)

- 전부 **DPA-SSE 데이터셋으로 4 epoch**, 프레임의 **5% 를 검증**에 사용.
- `DPA-2-MP` = **DPA-2.3.1-v3.0.0rc0** (MPtrj + 수백만 프레임 멀티태스크 사전학습; **DPA-SSE 와 같은 아키텍처**)
- `MACE` = **MACE-MP-0a small** (MPtrj)
- `M3GNet` = **M3GNet-MP-2021.2.8-PES**, 원 구현이 아니라 **matgl** 모듈로 fine-tune
- ⚠ **범용 모델은 PBE 로 라벨된 데이터로 사전학습됐고 DPA-SSE 데이터는 PBEsol 이다.** 논문은 *"moderate energy shift 이고 fitting network + 원소 참조에너지 갱신으로 흡수된다"* 고 주장하고, 근거로 `Fig. 5a,b` 의 PBE-vs-PBEsol NEB 경로가 거의 같다는 것과 Huang 2021 (ref 22)을 든다. **이 주장은 §11-2 committee 판정의 핵심 쟁점이다.**

### 4.4 Fine-tune 시연 (downstream)

- 대상: **Li₂B₂S₅ (mp-29410, "LBS")** — **훈련셋에 없음**(`Fig. S6` 결정구조). 원논문 표기가 `Li2B2S5`/`L2B2S5` 로 오락가락한다.
- 데이터: **DP-GEN 으로 800 스냅샷** 수집. test = 그중 **무작위 40 프레임**. 학습 가능 풀 = **760 프레임**.
- 학습: DPA-SSE / DPA-2-MP-ft / 무작위초기화 DPA-2 **셋 다 133 epoch**, LR 0.001 → 3.51×10⁻⁸ (동일 조건).

### 4.5 Distillation (증류)

1. `dpdata` 로 LGPS 구조를 **무작위 섭동** → DPA-SSE(교사)가 라벨
2. 섭동 구조 **5개**를 초기점으로 **900 K NPT, dt 1 fs, 2000 스텝** DPA-SSE MD
3. 각 궤적에서 **100 프레임** 추출 → **다시 섭동**
4. **|F| > 10 eV/Å 프레임 제거**
5. 최종 **8,579 프레임** → **표준 DeePMD (attention 없는 로컬 디스크립터) 학생 모델**을 **100만 스텝** 학습
6. test = **900 K AIMD NVT** 궤적 (완화된 LGPS 출발)

### 4.6 이온전도도 산출

- `MSD(t) = (1/N) Σᵢ |rᵢ(t) − rᵢ(0)|²`, `D = lim_{t→∞} MSD(t)/6t`
- `σ(T) = (ze)²/(V k_B T) · D` — **Nernst–Einstein, 상관 무시 = Haven ratio 1 가정** (ref 50 France-Lanord & Grossman 2019 를 인용하면서 그 논문의 경고를 그대로 쓰지는 않는다)
- `σ(T) = σ₀ T^m exp(−Ea/k_BT)`, **m = −1**
- ⛔ **명시되지 않은 것**: 생산 MD 의 셀 크기·원자수(효율 벤치의 1350 원자 외) · 궤적 길이(`Fig. 6b` 의 5 ns 외) · 시드 개수 · thermostat 종류 · **MSD 피팅 창** · 오차막대 산출법. §13-2 · §14-1.

---

## 5. 결과 — 절별 상세

### 5.1 훈련셋이 무엇을 덮나 (`Fig. 1`) ★★

`Fig. 1` 은 네 층의 깔때기다:

1. **전해질 본체 6종**: Li₁₀SiP₂S₁₂, Li₁₀GeP₂S₁₂, Li₁₀SnP₂S₁₂, **Li₆PS₅Cl, Li₆PS₅Br, Li₆PS₅I**
2. **Li 함유 삼원/사원 황화물 20종**: LiBS₂, Li₃BS₃, Li₅BS₄, LiAlS₂, Li₅AlS₄, LiGaS₂, Li₅GaS₄, Li₃AsS₃, LiSbS₂, Li₂SiS₃(그림 표기 `Li₂SiS`), Li₄SiS₄, Li₂GeS₃, Li₄GeS₄, Li₂SnS₃, Li₄SnS₄, Li₃PS₄(그림 표기 `LiP₃S4` — 오식으로 보임), Li₂P₂S₆, Li₇PS₆, Li₇P₃S₁₁, Li₃SbS₄
3. **이원 부분계 14종**: LiCl, LiBr, LiI, **Li₂O**, Li₂S, **B₂S₃**, Al₂S₃, Ga₂S₃, As₂S₃, Sb₂S₃, SiS₂, GeS₂, SnS₂, P₂S₅
4. **Li 금속**

논문 논리: LGPS 계열은 Li₂S + Y₂S₅ + XS₂ 로, argyrodite 는 **Li₂S + P₂S₅ + LiX** 로 분해하므로 그 산물을 다 넣어야 고온 MD 에서 계가 무너질 때도 힘이 맞는다. 실제로 이것이 1150 K 까지 버티는 이유다.

**★ 우리에게 결정적인 두 사실:**
- **O 는 있지만 Li₂O 하나뿐이다.** **B 는 있지만 B–S 결합(LiBS₂/Li₃BS₃/Li₅BS₄/B₂S₃)뿐이다.** ⇒ **41계 어디에도 B–O 결합이 없다.** 원소 지원 ≠ 결합환경 지원.
- **란탄족은 전혀 없다.** Nd 는 원소 자체가 밖이다.

주기표 heatmap(0–60,000 색눈금)에서 **Cl 은 눈에 띄게 옅다** — Li·S·P 가 최고 농도이고 Cl 은 Ga·As·Sn·Sb 급의 옅은 칸이다 `figure-read`. Cl 계(LPSCl+LiCl) 프레임 수가 적다는 뜻이고, 이것이 `Fig. S1` 의 LPSCl 이상치들과 무관하지 않을 수 있다(§13-3).

### 5.2 정확도 벤치마크 (`Fig. 2`, `Fig. S1`, `Fig. S2`) ★★

`Fig. 2a,b` 는 전 41계 parity — E 는 −5.5~−2 eV/atom 에서 대각선에 딱 붙고(MAE 1.57), F 는 −6~+6 eV/Å 에서 붙는다(MAE 30.28). 41계를 색으로 구분했지만 겹쳐서 계별 분해는 못 읽는다.

`Fig. 2c,d` 는 **가열궤적(150→1150 K)** 에서의 계별 MAE 를 **fine-tune 한 세 범용 모델과만** 비교한다 — **base 모델은 여기 없다**. base 는 `Fig. S1`, `Fig. S2` 에 있다. 이 배치가 본문을 관대하게 보이게 만든다(§13-5).

`Fig. S2` 는 이 논문 논지의 **기계론적 증거**로 쓰인다: 다섯 패널(DPA-SSE / CHGNet / M3GNet / MACE / DPA-2-MP)의 E parity.
- **DPA-SSE(a)**: −4.5~−3.95 eV/atom 전 구간 대각선.
- **b–e (범용 base)**: 점들이 **대각선 아래**(모델이 더 낮은 에너지) 로 내려가고 **기울기가 1보다 작다**. CHGNet 은 E_DFT −4.3→−3.8 (0.5 eV/atom 폭)에서 −4.28→−3.87 (0.41 폭) `figure-read` ⇒ **기울기 ≈0.82, 에너지 스케일의 ~18% 를 잃는다.**
- 더 중요한 것: **계마다 별도의 평행 가지**로 갈린다(LSiPS 가지가 LGPS 가지 아래). ⇒ **단일 상수 오프셋으로 못 고친다.** 도핑·혼합계에서는 국소 모티프 사이 *상대* 에너지가 틀어진다는 뜻이다.

⚠ 그런데 본문은 이 그림으로 *"lithium-hopping event 의 에너지가 과소평가된다"* 고 쓴다. **`Fig. S2` 는 그 문장을 지지하지 못한다** — 세로축이 eV/**atom** 이고 표시 폭이 0.5 eV/atom 인데, 52원자 셀에서 0.35 eV 장벽은 **6.7 meV/atom** 으로 이 그림의 점 지름보다 작다 `digest 계산 (원논문 미보고)`. 호핑 장벽 주장을 실제로 지지하는 것은 **`Fig. 5a,b`(NEB)** 다(§13-5).

### 5.3 구조·열역학 (`Fig. S4`, `Fig. S5`)

격자상수 41계 parity(`Fig. S4`)와 분해에너지 22계 parity(`Fig. S5a`), Li₂S–P₂S₅ 볼록껍질(`Fig. S5b`). 껍질은 DFT 와 **선이 겹칠 정도로** 일치하고 Li₃PS₄·Li₇P₃S₁₁·Li₇PS₆ 세 조성이 모두 hull 위에 있다.

### 5.4 고용체 일반화 (`Fig. 3`) ★★

훈련에 **없는** Li₁₀Ge₁₋ₓ₋ᵧSnₓSiᵧP₂S₁₂ (LXPS) 와 **Li₆PS₅Cl₁₋ₓ₋ᵧBrₓIᵧ (LPSX)** 고용체를 임의 농도로 만들고, 각 배열마다 **상온 AIMD 궤적**을 뽑아 test set 으로 썼다.
- E MAE **1.56 meV/atom**, F MAE **29.15 meV/Å** — 표준 test set(1.58 / 30.28)과 사실상 동일.
- 인셋 오차분포: ΔE 대부분 <0.002 eV/atom, ΔF 대부분 <0.1 eV/Å. **LXPS(주황)가 LPSX(파랑)보다 훨씬 좁다** — 즉 **halide 혼합 쪽이 cation 혼합보다 어렵다** `figure-read`. 우리 계가 halide 쪽이라는 점에서 유의미하다.
- `Fig. 3c` t-SNE: 훈련셋(연두) 위에 LPSX(파랑)·LXPS(주황)이 얹힌다. 논문 주장은 *"고용체 점들이 훈련셋이 친 영역 안에 있다"*. ⚠ 고해상 재크롭으로 다시 보니 **Component-1 ≈ 55–100, Component-2 ≈ −10~+40 구역에 연두가 거의 없는데 주황(LXPS)만 몰려 있다** `figure-read` — "완전히 안쪽"은 아니다(§13-7). 그리고 t-SNE 는 거리를 보존하지 않으므로 이런 그림은 **정성적 삽화이지 커버리지 증명이 아니다**.

> ⚠ **크로핑 주의**: 자동 크로퍼가 이 쪽(본문 4쪽, 2단 조판)에서 `Fig. 2`·`Fig. 3` 영역을 어긋나게 잘랐다(`fig_2.png` 에 Fig. 3 패널이 들어가 있었다). **수동 재크롭으로 고쳤고** `figures.json` 에 `note` 로 남겼다.

### 5.5 Fine-tuning — downstream 비용 (`Fig. 4`, `Fig. S6`, `Fig. S7`) ★★

**zero-shot 실패가 크다.** 훈련에 없는 Li₂B₂S₅ 에 DPA-SSE 를 그냥 쓰면 E MAE **162.65 meV/atom**, F MAE **369.16 meV/Å**. `Fig. 4a` 를 보면 단순 산포가 아니라 **명확한 상향 편향**(E_DP 가 E_DFT 보다 ≈+0.16 eV/atom 위, 인셋 ΔE 분포가 0.12–0.22 에 뭉쳐 있다) `figure-read`.

**20 프레임이면 편향이 사라진다**: E MAE **3.44 meV/atom**, F MAE **89.07 meV/Å**.

`Fig. 4c,d` 학습곡선 (`figure-read ≈`, 세 곡선 모두 133 epoch 동일):

| 프레임 | DPA-SSE-ft E MAE | DPA-2-MP-ft | **from-scratch DPA-2** |
|---|---|---|---|
| zero | 0.163 eV/atom | 0.044 | 1.6 |
| 10 | 0.0055 | 0.0055 | 0.018 |
| 20 | 0.0038 | ≈0.0045 | 0.014 |
| **60** | **0.0027** | 0.0042 | 0.0093 |
| 100 | 0.0026 | 0.0037 | 0.0084 |
| 760 (전체) | 0.0016 | 0.0019 | **0.0043** |

⇒ **60 프레임의 fine-tune 이 760 프레임의 from-scratch 를 이긴다**(0.0027 < 0.0043). 힘 쪽도 같다: from-scratch@760 ≈0.055 eV/Å ≈ DPA-SSE-ft@**80–100** 프레임. **≈8–12× 데이터 절약** `digest 계산 (원논문 미보고)`.

**주목**: `DPA-2-MP-ft`(=범용 모델을 DPA-SSE 데이터로 미리 적신 것)가 **DPA-SSE 와 거의 같은 데이터 효율**을 낸다. 논문 스스로 *"fine-tuning as a viable future direction for building domain-specific models"* 라고 쓴다 — 즉 **DPA-SSE 라는 특정 체크포인트가 마법인 게 아니라, "황화물 비평형 데이터로 적시는 행위"가 핵심**이라는 자기 고백이다. 이건 우리에게 좋은 소식이다(§11-3).

`Fig. S7` 은 M3GNet 만 따로 뽑은 같은 시험 (나는 안 봄).

### 5.6 NEB 와 확산 (`Fig. 5`) ★★

**`Fig. 5a` c축 협동 호핑** (migration coordinate 0–7): DFT(PBE) 봉우리 `≈0.345`, DPA-SSE `≈0.31`, MACE-ft `≈0.30`, DPA-2-MP-ft `≈0.28`, M3GNet-ft `≈0.225`. **base 모델(가는 점선)은 `≈0.12`(M3GNet) / `≈0.20`(DPA-2-MP)** — DFT 의 **1/3**.

**`Fig. 5b` ab면 kick-off** (coordinate 0–11): DFT `≈0.35`, DPA-SSE `≈0.37`, MACE-ft `≈0.305`, DPA-2-MP-ft `≈0.29`, M3GNet-ft `≈0.26`, **base 는 `≈0.115–0.12`**.

논문은 **PBE 와 PBEsol NEB 경로를 같은 그림에 겹쳐** 두 범함수가 이 문제에서 거의 같음을 보였다 — fine-tune 시 PBE↔PBEsol 혼용을 정당화하는 유일한 증거다.

**`Fig. 5c` LGPS D vs 1000/T** (0.65–3.5 K⁻¹, 즉 ~1540 K → ~286 K):
- AIMD(빨강 마름모)는 고온만, 실험(자홍 마름모)은 저온만 — **두 기준이 겹치지 않는다.**
- DPA-SSE(파랑)는 **고온에서 AIMD 와 겹치고 저온에서 실험 근처로 내려온다** — 이 그림의 핵심 주장.
- **base 범용 모델(가는 점선)은 저온에서 곡선이 훨씬 평평**하다 = Ea 가 작다 = 300 K 에서 `≈1.3×10⁻¹⁰`(MACE) ~ `≈1×10⁻⁹`(M3GNet) m²/s. DPA-SSE `≈4.5×10⁻¹²` 대비 **30–220×**.

⚠ 본문 Discussion 은 *"universal force fields overestimate the room temperature ion conductivity ... by more than an order of magnitude"* 라고 **보수적으로** 쓰는데, 그림은 **두 자릿수**를 보여준다.

### 5.7 도핑·무질서 MD (`Fig. 6`, `Fig. S8`–`S11`) ★★

- **`Fig. 6a`**: Si↔Ge 고용체 σ 추세 재현(§3.5).
- **`Fig. 6b`**: 4a/4c 음이온 자리 무질서가 **장거리 수송의 on/off 스위치**임을 5 ns MSD 로 보인다. 질서상은 **포화**(≈11.5 Å²)해서 D 가 0 에 수렴하고, 무질서상만 선형. 그리고 무질서상이 **에너지적으로도 더 낮다**(≈7.5 meV/atom).
  ⚠ 본문은 이 퍼텐셜에너지 비교를 *"Figure 6d"* 라고 쓰는데 **실제로는 `Fig. 6b` 오른쪽 축**이다. `Fig. 6d` 는 활성화에너지 막대다(§13-1).
  ⚠ 그리고 본문은 *"halide atoms at the **4c** sites randomly exchange with S at the **4a** sites"* 라고 쓰는데, **`Fig. 6b` inset 범례는 `S (4c)` / `Cl (4a)` / `S (16e)`** 다 — 자리 배정이 본문과 그림에서 뒤집혀 있다(§13-1). 우리처럼 4a/4c 를 구분해 다루는 쪽에서는 그냥 넘기면 안 되는 불일치다.
- **`Fig. 6c,d`**: 5계 σ·Ea (§3.5). 논문 서술 *"hopping barrier ΔE estimated by DPA-SSE is very close to the experimental measurement"* — **LPSCl 에서는 0.24 vs 0.324 로 0.08 eV 차이**라 그림이 그 문장을 지지하지 않는다(§13-5).
- **`Fig. S10a`**: 과잉 Cl 도핑 Li₆₋ₓPS₅₋ₓCl₁₊ₓ (= 우리 modelc 계열). Li 공공 + 4c 자리 S/Cl 혼합 강화가 σ 를 올린다는 실험(Feng 2020, Liu 2024)을 DPA-SSE 가 재현.
- **`Fig. S10b`**: Br 치환이 같은 x 에서 Cl 보다 σ 가 높다 — 논문은 **배열 엔트로피 증가** 로 설명(가설이라고 명시: *"possibly due to"*).
- **`Fig. S11`**: **O 도핑 Li₅.₅PS₄.₅₋ₓOₓCl₁.₅ → σ 단조 감소.** 캡션은 *"which help improve moisture stability critical to industrial application"* — **즉 O 도핑은 수분 안정성과 전도도의 트레이드오프**로 명시적으로 프레이밍된다.
- `Fig. S8`(LSiPS·LSnPS D), `Fig. S9`(LPSI MSD·PE) — **나는 안 봤다**(본문 서술만 인용).

### 5.8 증류와 효율 (`Fig. 7`, `Fig. S12`) ★★

교사(DPA-SSE) → 학생(표준 DeePMD)로 8,579 프레임을 넘기면 900 K AIMD 궤적에서 **2.10 meV/atom / 48.44 meV/Å** (교사 1.59 / 30.0). 논문 표현: *"induced error can be controlled within ... less than 1 meV/atom and a few dozen meV/Å"*.

대가로 **≈520× 속도**(§3.8). 논문 자신이 *"DPA-SSE is still rather expensive for large-scale dynamic simulations"* 라고 인정한다.

⚠ `Fig. S12b` 축 라벨이 **`E_Model (meV/atom)` / `E_DFT (meV/atom)`** 인데 값은 −4.25 ~ −4.40 이다 → **eV/atom 이어야 한다**(단위 오식, §13-1). `Fig. 4b` 도 x·y 축이 **둘 다 `F_DFT`** 이고(y 는 `F_DP` 여야 함), `Fig. 4d` 세로축이 **`Force MAE (eV/atom)`** (eV/Å 여야 함).

⚠ 본문이 증류 성능을 *"Supplementary Fig. S10b, c"* 라고 가리키는데 **실제로는 `Fig. S12b,c`** 다(§13-1).

### 5.9 비보존 모델의 파국 (`Fig. S3`)

§3.9 참조. **ORB-v2 가 100 ps NVE 에서 ΔE ≈6–7 eV/atom 까지 폭주**했다. 이 논문이 벤치마크 대상을 보존형으로 한정한 근거이자, **"MLIP 를 바꿀 때 가장 먼저 물어야 할 것은 정확도가 아니라 보존성"** 이라는 실무 교훈이다(§11-5).

---

## 6. 전체 논증 흐름

1. 도핑 최적화에는 임의 조성의 σ 예측이 필요하다 → AIMD 는 너무 비싸고 계별 MLIP 는 매번 재학습해야 한다.
2. 범용 MLIP 는 일반화되지만 **평형 근처 데이터**로 학습됐다 → **비평형 구조(호핑 안장점)의 에너지를 과소평가**(`Fig. S2`, `Fig. 5a,b`).
3. 그 결과 **장벽이 1/3, D 가 30–220× 과대**(`Fig. 5c`) → 조성 스크리닝에 못 쓴다.
4. **처방 = 도메인 특화 + 비평형 샘플링.** 41계 · 분해산물 포함 · NPT 0–1200 K / 0–2 GPa · DP-GEN (`Fig. 1`).
5. 그러면 1150 K 까지 <2 meV/atom (`Fig. 2`), **훈련에 없는 고용체도 같은 정확도** (`Fig. 3`).
6. 그래서 NEB 장벽이 DFT 와 맞고(`Fig. 5a,b`), D 가 AIMD·실험과 맞고(`Fig. 5c`), 도핑 추세가 실험과 맞는다(`Fig. 6a`, `Fig. S10`, `Fig. S11`).
7. **모르는 계는 fine-tune** — 20–60 프레임이면 된다(`Fig. 4`).
8. **너무 느리면 distill** — 520× (`Fig. 7`).
9. ⇒ *"a platform for continuous learning"*.

**논증의 약한 고리**: 3→4 단계에서 "도메인 특화" 와 "비평형 샘플링" 이 **분리 실험되지 않았다**. `Fig. 2c,d` 가 보여주는 것은 *"범용 모델도 DPA-SSE 데이터로 4 epoch 적시면 DPA-SSE 급이 된다"* 이므로, **효과의 대부분은 데이터(비평형 샘플링)에서 오고 "황화물 전용 모델"이라는 정체성에서 오는 게 아닐 수 있다.** 논문도 §5.5 끝에서 사실상 이를 시인한다.

---

## 7. DFT/계산 방법 ★

§4.1 참조. 요약: **VASP · PAW · PBEsol · 600 eV · KSPACING 0.3 · 힘 0.01 eV/Å · E/F/virial 라벨 · DP-GEN 능동학습 · NPT 0–1200 K, 0–2 GPa · 54,771 프레임**. DFT+U 없음. vdW 보정 언급 없음. spin 언급 없음(비자성 절연체라 자연스럽지만 명시는 없다). **무질서 처리 방법 미기재.**

MLIP: **DPA-2** (repinit + repformer×12, rcut 9.0 Å, head 4, fitting 3×240). MD: **Nernst–Einstein**, `m = −1` Arrhenius. NEB (구현체 미명시). 증류 MD 는 **900 K NPT, dt 1 fs**.

---

## 8. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | DPA-SSE 훈련셋 전경 — 15원소 주기표 heatmap(0–60,000) + 41계 4층 깔때기(전해질 6 / Li-삼원황화물 20 / 이원 14 / Li) + LXYS·LPSX 삼각상도 + 워크플로 | ★★ **커버리지 판정의 원전.** LPSCl 이 핵심 훈련계다. **B–O 결합은 없고 Nd 는 원소째 없다.** Cl 칸 색이 옅다(프레임 수 적음) |
| 2a,b | 전 41계 E/F parity — MAE 1.57 meV/atom, 30.28 meV/Å | 소환값 상한선. 우리 UMA 는 이런 계별 parity 를 아직 안 냈다 — 같은 형식으로 내면 바로 비교 가능 |
| 2c,d | 가열궤적(150–1150 K) 계별 E/F MAE, DPA-SSE vs **fine-tune 한** DPA-2-MP·M3GNet·MACE | ⚠ **base 모델이 빠져 있다** — 관대한 배치. base 는 S1/S2 에 있다 |
| 3a,b | 훈련에 없는 LXPS·LPSX 고용체 parity — 1.56 meV/atom, 29.15 meV/Å. 인셋 오차분포에서 **halide 혼합(LPSX)이 cation 혼합(LXPS)보다 넓다** | ★ 우리 modelc(Cl-rich)가 halide 축이라 이쪽 오차가 더 관련 있다 |
| 3c | 훈련셋 vs 고용체 t-SNE | 정성 삽화. **커버리지 증명 아님** — Component-1 60–90 에 연두 없이 주황만 있는 구역이 있다 |
| 4a,b | Li₂B₂S₅ zero-shot(편향 +0.16 eV/atom) → 20프레임 fine-tune 후 대각선 | ★★ **우리 B₂O₃·Nd 계의 예상 시나리오 그 자체.** zero-shot 실패 규모와 회복 비용의 실측 |
| 4c,d | 학습곡선: DPA-SSE-ft vs DPA-2-MP-ft vs from-scratch, 프레임 수 대 MAE | ★★ **fine-tune 비용 견적의 원전 — 20–60 프레임, ≈10× 데이터 절약.** 축 단위 오식 있음(`eV/atom`→`eV/Å`) |
| 5a,b | LGPS c축·ab면 NEB. DFT(PBE) vs DPA-SSE vs ft 모델 vs **base(가는 점선)**. base 봉우리 ≈0.12–0.20 vs DFT ≈0.345 | ★★ **"범용 MLIP 가 왜 D 를 과대하는가"의 유일한 직접 증거.** 우리가 UMA 로 똑같이 재봐야 할 시험 |
| 5c | LGPS D vs 1000/T, AIMD·실험·DPA-SSE·ft·base | ★★ base 모델이 300 K 에서 30–220× 과대. **우리 UMA D 를 이 그림에 얹어 보는 것이 최소 검증** |
| 6a | Li₁₀SiₓGe₁₋ₓP₂S₁₂ σ₃₀₀K 계산 vs 실험 | 추세 재현의 예. DPA-SSE 오차막대 ±30–40% |
| 6b | **LPSCl 질서 vs 무질서(50%@4c) MSD 5 ns + 퍼텐셜에너지.** 질서상은 ≈11.5 Å² 에서 포화, 무질서상만 선형. 무질서가 ≈7.5 meV/atom 더 안정 | ★★ 우리 4a/4c 무질서 처리의 직접 참조. ⚠ **inset 자리 라벨(S 4c/Cl 4a)이 본문 서술과 뒤집혀 있다** |
| 6c,d | 5계 σ₃₀₀K·Ea, 계산 vs 실험 | ★★ **LPSCl: σ 7 vs 3 (2.3× 과대), Ea 0.24 vs 0.324 (0.08 eV 과소).** "excellent agreement" 는 과장 |
| 7 | MD 효율 s/(step·atom), LGPS 1350원자 V100. DPA-SSE 8.6e-3 / MACE-ft 1.9e-4 / M3GNet-ft 1.1e-4 / **distilled 1.65e-5** / NVNMD 8.7e-7 | ★★ **비용 판정의 원전.** 사전학습 원본은 우리 규약에 못 쓴다 — distill 이 전제 |
| S1 | base 범용모델 5종 vs DPA-SSE, 평형 근처(a,b)와 가열궤적(c,d) E/F MAE | ★★ **LPSCl 이 유일하게 이상하다**: (a) DPA-SSE 에너지 막대 누락, (d) CHGNet base 24 < DPA-SSE 31 meV/Å. ⚠ **SI 캡션이 c,d 를 설명하지 않는다** |
| S2 | 가열궤적 E parity 5패널 — 범용모델은 대각선 아래 + **기울기 ≈0.82**, **계마다 평행 가지** | ★ 상수 오프셋으로 못 고친다 = 혼합계 상대에너지가 틀어진다. ⚠ 다만 eV/atom 스케일이라 **호핑 장벽 주장을 지지하지 못한다** |
| S3 | LGPS 500 K NVE 100 ps 에너지 드리프트. **orb-v2 ≈6–7 eV/atom 폭주**, DPA-SSE·MACE 평탄 | ★★ **MLIP 교체 시 첫 점검 항목 = 보존성.** 우리 UMA 설정도 이 시험을 아직 안 했다 |
| S4 | 41계 완화 격자상수 parity (2.5–22.5 Å) | ⚠ 축 범위가 넓어 **1% 오차가 안 보인다** — 격자 정확도 근거로 인용하면 안 된다 |
| S5 | (a) 22계 분해에너지 parity −2.75~+0.65 eV/f.u. (`Li12P2S10Cl2` 포함) (b) Li₂S–P₂S₅ 볼록껍질, x=0.75 최저 ≈−0.264 eV/atom | 열역학 축 참고. ⚠ 범례 색 10색 순환이라 **개별 점 특정 불가** |
| S6 | Li₂B₂S₅ (mp-29410) 결정구조 | fine-tune 대상 확인용 (나는 안 봄) |
| S7 | M3GNet 학습곡선 (무작위초기화 vs DPA-SSE 데이터 fine-tune) | 안 봄 |
| S8 | Li₁₀SiP₂S₁₂·Li₁₀SnP₂S₁₂ D 계산 vs 실험 | 안 봄 |
| S9 | Li₆PS₅I MSD·퍼텐셜에너지 (질서상이 더 안정 → 낮은 σ) | 안 봄 (본문 서술만 인용) |
| S10 | **(a) Li₆₋ₓPS₅₋ₓCl₁₊ₓ (b) Li₆₋ₓPS₅₋ₓClBrₓ σ₃₀₀K vs x, 계산 vs 실험** | ★★★ **(a)가 우리 modelc(x=0.6) 계열 그 자체.** x=0.5→11.8, x=0.7→15.7 mS/cm |
| S11 | **Li₅.₅PS₄.₅₋ₓOₓCl₁.₅ σ₃₀₀K vs O 농도 — 단조 감소** (계산 11.8→7.0, 실험 9.5→6.0) | ★★★ **우리 O 도핑계의 직접 대응.** "O 도핑 = 수분 안정성 ↔ 전도도" 트레이드오프의 문헌 근거 |
| S12 | 증류 스킴 + 교사/학생 E·F parity (2.10 vs 1.59 meV/atom; 0.048 vs 0.030 eV/Å) + 시간 인셋 | ★★ 증류 손실의 실측 규모. ⚠ 축 단위 오식(`meV/atom`→`eV/atom`) |

> **크로핑 17장 + 내가 추가 렌더 2장(S4·S11) = 19장 중 실제로 본 것 15장**: `Fig. 1, 2, 3, 4, 5, 6, 7, S1, S2, S3, S4, S5, S10, S11, S12`. **안 본 것 4장**: `Fig. S6, S7, S8, S9` — 이 넷에 대한 서술은 **본문 문장을 옮긴 것**이다.
> **내가 고친 것 4장**: ① `Fig. S4`·`S11` 은 자동 크로퍼가 *"거의 백지"* 로 오판해 **제외**했던 것을 **SI 해당 쪽 전면 렌더**로 살렸다(⚠ `fig_S11.png` 은 SI 8쪽 전체라 **`Fig. S10` 이 같이 들어 있다**). ② `Fig. 2`·`Fig. 3` 은 2단 조판에서 캡션 앵커가 어긋나 **`fig_2.png` 에 Fig. 3 의 패널이 들어가 있었다** — 4쪽을 다시 렌더해 좌표를 잡고 **수동 재크롭**했다. 네 건 모두 `figures.json` 에 `note` 로 표시했다.

---

## 9. Post-processing ★

- **무엇**: ① parity/MAE 통계 (E·F, 계별·전체) ② **t-SNE** 로 데이터 분포 커버리지 시각화 ③ **NEB** 호핑 장벽 ④ **MSD → D → Nernst–Einstein σ → Arrhenius Ea** ⑤ **볼록껍질(형성/분해에너지)** ⑥ 격자상수 완화 parity ⑦ **NVE 에너지 드리프트**(보존성 검사) ⑧ **s/(step·atom) 처리량 벤치마크**
- **도구**: **DeePMD-kit / DPA-2** (학습·추론), **DP-GEN**(능동학습), **dpdata**(구조 섭동·포맷), **VASP**(라벨), **matgl**(M3GNet fine-tune), **MACE / CHGNet / ORB** 공개 체크포인트, **AIS Square**(모델·데이터 배포), **Bohrium**(노트북·클라우드 계산). ⛔ NEB 구현체, MSD 계산 코드, t-SNE 하이퍼파라미터는 **명시 없음**.
- **수치화·기록**: 표가 0개다. 모든 결과가 그림 + 본문 산문. **원시 수치 테이블이 SI 에 없다** — 재현하려면 AIS Square 데이터셋을 직접 받아야 한다(§13-2).
- **우리 차용 후보**:
  - **`Fig. 5c` 형식**(D vs 1000/T 에 AIMD·실험·여러 MLIP 를 한 판에) — 우리 UMA D 를 이 판에 얹으면 UMA 가 base 범용모델 무리에 속하는지 DPA-SSE 쪽인지 **한 장으로 판정**된다. 우리는 이미 600/800/1000 K 3점을 갖고 있다.
  - **`Fig. S3` 형식**(NVE 100 ps 드리프트) — 저렴하고 결정적인 보존성 시험. `tools/ionic/` 에 붙일 수 있다.
  - **`Fig. 6b` 형식**(질서 vs 무질서 MSD + PE 를 한 축에) — 우리 4a/4c 무질서 판정을 한 장으로 보이는 양식.

---

## 10. 기법 미니사전

| 용어 | 뜻 (이 논문 맥락) |
|---|---|
| **DPA-2** | Deep Potential with Attention v2. 원자 로컬 환경을 단원자/원자쌍/등변 채널로 인코딩하고 transformer(attention)로 섞어 디스크립터를 만드는 구조. **주기율표 전역 커버리지 + 멀티태스크 학습**이 설계 목표. |
| **DP-GEN** | Deep Potential GENerator. **능동학습 루프** — 모델 여러 개의 예측 불일치가 큰 구조만 골라 DFT 라벨을 찍고 다시 학습. (⚠ 이 "모델 불일치" 가 곧 committee 아이디어인데, 이 논문은 최종 모델의 UQ 에는 쓰지 않는다.) |
| **out-of-equilibrium configuration** | 완화된 바닥구조 근처가 **아닌** 구조 — 고온 MD 스냅샷, 압축/인장, 그리고 결정적으로 **Li 호핑 안장점**. 이 논문의 전체 논지가 여기 걸려 있다. |
| **conservative force field** | 힘이 퍼텐셜에너지의 **좌표 미분**으로 나오는 모델. 아니면(direct force prediction) NVE 에서 에너지가 보존되지 않아 `Fig. S3` 처럼 폭주할 수 있다. |
| **knowledge distillation (증류)** | 무겁고 정확한 "교사" 모델로 대량의 (구조, 에너지, 힘) 라벨을 **공짜로** 찍어, 가볍고 빠른 "학생" 모델을 학습시키는 것. DFT 를 더 돌리지 않는다는 게 요점. |
| **zero-shot** | fine-tune 없이 사전학습 모델을 새 계에 그냥 적용하는 것. |
| **Nernst–Einstein (Haven=1)** | `σ = (ze)²·D/(V k_B T)`. 이온 간 상관을 무시한다는 뜻 — 실제 argyrodite 는 협동 호핑이 강해 Haven ratio ≠ 1 일 수 있고, 그러면 σ 가 계통적으로 틀어진다. |
| **t-SNE** | 고차원 점들을 2D 로 눌러 **국소 이웃 관계만** 대략 보존하는 시각화. **거리·면적·"바깥/안"의 의미가 없다** — 커버리지 증명으로 쓰면 안 된다. |
| **KSPACING** | VASP 에서 k-격자를 셀 크기에 맞춰 자동 생성하는 간격 파라미터(Å⁻¹). 0.3 은 41계에 **동일 기준**을 강제하려는 선택. |
| **NVNMD** | non von-Neumann Molecular Dynamics — DeePMD 를 전용 하드웨어(FPGA 계열)에 태워 메모리 병목을 없앤 것 (ref 42, Mo et al. 2022). 우리와 무관. |

---

## 11. ★★ 우리 좌표 — UMA 의 대체인가, 대조군인가 → `../our_dft_baseline.md`

> 우리 계: **comp1 = Li₆PS₅Cl** · **modelc = Li₅.₄PS₄.₄Cl₁.₆** · **+B₂O₃** · **Nd–O 공도핑**.
> 우리 규약: **UMA-s-1p1(omat)** · Langevin NVT · dt 2 fs · equilib 5 ps / prod 200 ps · **MSD 창 2–50 ps 자유절편** · 시드 3 · **600/800/1000 K**.
> ⛔ 아래 문헌 수치는 전부 **소환값**이다. `db/properties/canonical_registry.json` 에 넣지 않는다.

### 11-1. 질문 ①: **훈련셋에 우리 계가 들어 있나** — 계별 판정

| 우리 계 | DPA-SSE 지위 | 근거 | 판정 |
|---|---|---|---|
| **comp1 = Li₆PS₅Cl** | **핵심 훈련계** (`Fig. 1` 1층 6종 중 하나) | Fig. 1 | ✅ **완전 커버** |
| **modelc = Li₅.₄PS₄.₄Cl₁.₆** | 훈련계는 아니지만 **정확히 그 조성계열이 시험됐다** — `Fig. S10a` 의 Li₆₋ₓPS₅₋ₓCl₁₊ₓ, x=0/0.3/0.5/0.7. **우리는 x=0.6** | Fig. S10a | ✅ **일반화가 실증된 구간의 내부 보간점** |
| **O 도핑 LPSCl (LPSOCl)** | **`Fig. S11` 에서 직접 시험됨** — Li₅.₅PS₄.₅₋ₓOₓCl₁.₅, x=0–0.30 | Fig. S11 | ✅ **직접 대응 계가 있다** (O 는 훈련셋에 **Li₂O 로만** 들어 있는데도 통했다) |
| **+B₂O₃ 도핑** | ⚠ **B 도 O 도 원소로는 있지만 B–O 결합이 41계 어디에도 없다.** B 는 B–S 만(LiBS₂·Li₃BS₃·Li₅BS₄·B₂S₃), O 는 Li₂O 만 | Fig. 1 | ⚠ **결합환경 미커버.** 그리고 `Fig. 4a` 가 보여준 것: **Li–B–S 삼원(Li₂B₂S₅)조차 zero-shot 이 162.65 meV/atom 로 실패**했다. B–O 는 그보다 더 멀다 ⇒ **zero-shot 실패를 예상해야 한다** |
| **Nd–O 공도핑** | ❌ **란탄족이 15원소 안에 없다** | Fig. 1 | ❌ **범위 밖.** 원소 임베딩 확장 가능 여부는 이 논문으로 답할 수 없다(§14-4) |

**⇒ ①의 답**: **argyrodite 와 Cl 은 확실히 들어 있다.** 그것도 "겨우 들어 있다"가 아니라 **Li₆PS₅Cl/Br/I 세 개가 훈련 1층**이고, **과잉 Cl 도핑(우리 modelc 계열)과 O 도핑(우리 LPSOCl 계열)이 SI 에서 직접 시험**됐다.

> **이것이 우리 J-1 한계를 정확히 겨눈다.** J-1 은 *"PET-MAD Li₃PS₄ 벤치에 **Cl 이 없다**"* 였다. DPA-SSE 는 그 구멍을 정면으로 메운다 — Cl 이 있고, **Cl-rich 조성 시리즈까지 있다.**
> ⚠ 단서: `Fig. 1` heatmap 에서 **Cl 칸은 색이 옅다**(프레임 수가 Li·S·P 보다 훨씬 적다). 그리고 `Fig. S1` 에서 **LPSCl 만 두 개의 이상 신호**를 보인다(에너지 막대 누락 · CHGNet base 에 힘에서 밀림). "Cl 이 있다"와 "Cl 이 충분히 있다"는 다르다.

### 11-2. 질문 ②: **committee 멤버로 쓸 수 있나** — ⛔ **부적격 판정**

Grasselli 식 (27)의 committee 는 **`M ≥ 4` 개의 *equivalent* 모델**을 전제한다. equivalent 란 *같은 사후분포에서 뽑은 표본* — 실무적으로 **같은 아키텍처 · 같은 훈련 분포 · 같은 참조 PES**, 차이는 **초기화/부트스트랩 리샘플링뿐**이라는 뜻이다. DPA-SSE 를 UMA·MACE·SevenNet 옆에 네 번째로 세우면:

| 전제 | UMA-s-1p1(omat) | DPA-SSE | 깨지나 |
|---|---|---|---|
| 아키텍처 | eSEN/equivariant 계열 | **DPA-2 (attention)** | ⛔ 깨짐 |
| 훈련 코퍼스 | OMat24 (범용, 수천만 프레임) | **황화물 전용 54,771 프레임** | ⛔ 깨짐 |
| **참조 범함수** | **PBE(+U) 계열** | **PBEsol** | ⛔⛔ **결정적으로 깨짐** |
| 라벨 코드/설정 | VASP 별도 프로토콜 | VASP 600 eV, KSPACING 0.3 | ⛔ 깨짐 |

**⇒ ②의 답: committee 멤버로 부적격이다.** 이유를 한 줄로: **두 모델이 서로 다른 참조 PES 를 향해 학습됐으므로, 둘의 불일치는 인식적 불확실성(epistemic uncertainty)이 아니라 PBE−PBEsol **계통 오프셋**을 포함한다.** committee spread 를 오차막대로 환산하는 순간 그 오프셋이 "불확실성"으로 둔갑한다 — **우리 이종 committee 문제가 완화되는 게 아니라 한 축(범함수) 더 늘어난다.**

**⚠ 논문 자신의 반론과 그 한계**: 저자들은 *"PBE 와 PBESol 차이는 moderate energy shift 이고 fine-tune 이 흡수한다"* 라고 쓰고, `Fig. 5a,b` 에서 두 범함수의 NEB 경로가 거의 같음을 보인다. **이 반론은 fine-tune 하는 경우에만 유효**하다 — fine-tune 하면 원소 참조에너지와 피팅망이 다시 맞춰진다. **fine-tune 하지 않고 그냥 committee 에 세우는 우리 시나리오에는 적용되지 않는다.** 그리고 `Fig. 5a,b` 는 **LGPS 의 두 경로**에서만 확인한 것이지 argyrodite 도, 기계적/전자적 물성도 아니다.

**✅ 그런데 진짜 길이 하나 열린다 — 합법적 committee 를 만들 수 있다.**
훈련 데이터가 **공개돼 있다**(AIS Square dataset `Solid_State_Electrolyte`, id 217, 54,771 프레임). 같은 데이터·같은 아키텍처로 **시드만 바꿔 M ≥ 4 개**를 학습하면 그것은 **Grasselli 의 전제를 정확히 만족하는 committee** 다. 이종 문제가 원리적으로 사라진다.
- 비용: DPA-2 급 모델 4개 학습 = 수백만 스텝 × 4. 우리 GPU 사정으로는 **크다**.
- 값싼 대안: **증류 학생 모델(표준 DeePMD)을 시드만 바꿔 4–8개** 만든다. 교사(DPA-SSE) 한 개가 라벨을 무한정 찍어 주므로 **DFT 추가 비용 0**, 학생 학습은 훨씬 싸다. ⚠ 다만 그 committee 가 재는 것은 **"학생이 교사를 얼마나 못 따라갔나"**(증류 분산)이지 **"교사가 DFT 에서 얼마나 틀렸나"**(모델 오차)가 아니다 — **두 층을 절대 섞어 부르면 안 된다.** 이 구분은 우리가 §13 에 못박아야 한다.

### 11-3. 질문 ③: **UMA 의 대체인가 / UMA 는 여기서 유죄인가**

**⛔ 먼저 명확히: 이 논문은 UMA 를 시험하지 않았다.** 벤치마크 대상은 **DPA-2-MP, MACE-MP-0a(small), M3GNet-MP-2021.2.8, CHGNet, ORB-v2** — **전부 MPtrj 세대**다. **우리 UMA-s-1p1(omat)은 이 논문의 피고석에 없다.**

그래서 다음 두 문장을 구분해야 한다:
- ✅ **말할 수 있는 것**: *"MPtrj 로 사전학습된 범용 MLIP 들은 황화물 SE 의 Li 호핑 장벽을 DFT 의 1/3 수준으로 과소평가하고 상온 D 를 30–220× 과대평가한다"* (`Fig. 5a,b,c`).
- ⛔ **말할 수 없는 것**: *"따라서 UMA 도 그럴 것이다."* OMat24 는 MPtrj 와 훈련 분포가 다르고, 이 논문이 지목한 결함의 원인(평형 근처 편중)이 OMat24 에 같은 정도로 있는지는 **여기서 답할 수 없다**. **이건 가설이고, 검사는 §11-4 다.**

**우리 UMA 실패 전례 둘과의 대조:**

| 우리 전례 | DPA-SSE 가 도움이 되나 | 이유 |
|---|---|---|
| **Li₃N 사용 금지** (2026-06 결정론적 편향) | ❌ **무관** | Li₃N 은 질화물. **N 이 DPA-SSE 15원소에 없다**(주기표에서 색 없는 칸) |
| **b2o3 골격 creep** (700 K↑ 비-Li 골격 β 가 rigid 기준 초과 → MD 전도도 축 전체 마감) | ⚠ **양날** | **긍정**: DPA-SSE 는 NPT 0–1200 K/0–2 GPa 로 **일부러 고온·고압 비평형을 샘플링**했고 1150 K 가열궤적에서 <2 meV/atom 을 유지한다 — **고온 골격 안정성이 정확히 그 설계 목표**다. **부정**: 그런데 **b2o3 의 B–O 결합은 훈련 분포 밖**이다(§11-1). `Fig. 4a` 의 Li₂B₂S₅ zero-shot 실패(162.65 meV/atom)가 경고다. ⇒ **DPA-SSE 를 b2o3 에 zero-shot 으로 들이대면 UMA 보다 나쁠 가능성이 높다** |

> ⚠ **그리고 이건 꼭 짚어야 한다**: `db/properties/b2o3_uma_vs_dft_force_prereg_2026_09_08.json`(봉인 2026-09-08, results_seen=false)은 b2o3 creep 이 UMA 결함인지 실물리인지를 **UMA vs 우리 DFT 힘 대조**로 가르려 한다. DPA-SSE 를 **세 번째 심판**으로 넣고 싶어질 텐데 — **b2o3 에 대해서는 넣으면 안 된다.** UMA(OMat24)는 B₂O₃ 를 봤을 가능성이 높고 DPA-SSE 는 확실히 못 봤으므로, 둘의 불일치가 "누가 맞나"가 아니라 "누가 그 결합을 봤나"를 잴 뿐이다. **DPA-SSE 는 comp1/modelc/LPSOCl 의 심판으로는 훌륭하고, b2o3 의 심판으로는 부적격이다.**

### 11-4. **우리가 지금 할 수 있는 최소 실험** — 단계·비용

먼저 **비용부터 못박는다** (이게 판을 결정한다):

우리 modelc MD 셀은 **62 / 248 / 558 원자**(1×1×1, 2×2×1, 3×3×1). gabia A6000 에서 UMA 실측 **558원자 → 252 ps/day** (`db/properties/md_throughput_scaling_2026_08_26.json`).
`Fig. 7` 의 s/(step·atom) 을 우리 셀·우리 dt(2 fs)로 환산하면 — **전부 `digest 계산 (원논문 미보고)`**:

| 모델 | 558원자 환산 | 200 ps 1런 | **modelc 3온도 × 3시드 = 9런** |
|---|---|---|---|
| **UMA-s-1p1 (우리 현행, A6000 실측)** | **252 ps/day** | ≈19 h | **≈7일** (실측 기반) |
| **사전학습 DPA-SSE** (8.6e-3 s/step·atom) | **≈36 ps/day** | **≈5.6일** | **≈50일** ⛔ |
| **증류 DPA-SSE** (1.65e-5) | **≈18,800 ps/day (≈18.8 ns/day)** | **≈15분** | **≈2.3시간** ✅ |

⚠ **교차 하드웨어 비교다** — 논문은 V100+12코어, 우리는 A6000. 자릿수 수준으로만 읽어야 한다. 그래도 결론은 자릿수가 뒤집힐 여지가 없다:

> **⇒ 사전학습 DPA-SSE 를 우리 200 ps × 3시드 × 3온도 규약에 그대로 꽂는 것은 불가능하다. 증류(distillation)는 선택이 아니라 전제다.**
> **그리고 증류하면 UMA 대비 ~75× 처리량**이 나온다 — 이게 진짜 상금이다. 우리가 지금 못 하고 있는 것들(멀티시드, 큰 셀, 긴 궤적, 3점 아닌 6점 아레니우스)이 **전부 비용 문제**였는데 그 벽이 사라진다. `md_throughput_scaling` 카드가 *"3×3×1(17.2 Å)도 24 Å 수용영역 기준을 못 넘는다"* 고 적어 둔 그 문제도 셀을 더 키워 볼 여지가 생긴다.

**단계 (각각 앞 단계가 통과할 때만 다음으로):**

- **Step 0 — 접근 확인 (반나절, 계산 0)**
  AIS Square 에서 모델(`models` id **266**)과 데이터셋(`datasets` name `Solid_State_Electrolyte`, id **217**) 을 받는다. Bohrium 노트북 **71679486918** 이 사용법 예제다. **확인할 것**: ① 라이선스/가입 요구(논문 본문 라이선스는 CC BY-**NC-ND** 이고 모델 라이선스는 별개다) ② 체크포인트가 받는 원소 타입 목록에 **Cl·O·B 가 실제로 있는지** ③ DeePMD-kit 버전 요구. ⛔ 못 받으면 여기서 끝 — 아래 전부 무의미하다.

- **Step 0.5 — 이미 있는 벤치에 그냥 얹기 (몇 시간, DFT 0회)** ★★ **가장 싸다 — 이걸 먼저 한다**
  `comparison_vs_ours.md` **§J-1** 은 이미 UMA 힘 정확도를 **PET-MAD Li₃PS₄ test 243구조**로 쟀다 (`db/properties/mlip_bench_li3ps4_uma.json`, 도구 `tools/mlip/bench_against_dft.py`, 결과 **30.0 meV/Å**). **그 라벨이 PBEsol 이다** — 즉 **DPA-SSE 의 모국어**다. 같은 파일에 DPA-SSE 를 태우면 **DFT 한 점도 안 찍고** 같은 test set · 같은 지표의 숫자가 나온다.
  - ⚠ **공정한 대결이 아니다**: `Fig. 1` 2층에 **Li₃PS₄ 로 보이는 항목**이 있다(그림 표기 `LiP₃S4`). 그러면 DPA-SSE 에겐 훈련 근처이고 UMA 에겐 완전 외부다. **이 숫자는 "누가 더 좋은 모델인가"가 아니라 "훈련셋 안이면 얼마나 좋은가"를 잰다.** 그 한계를 붙여서만 쓴다.
  - 그래도 값진 이유 둘: ① **DPA-SSE 가 자기 주장(≈30 meV/Å)을 독립 데이터에서 지키는지**의 하한 검사 ② **§J-1 의 명시적 한계 #3 — *"Cl 이 없다"*** 를 이 논문이 정면으로 메운다는 사실을 표에 기록할 자리가 생긴다.
  - ⛔ **§J-1 의 우리 30.0 meV/Å 과 이 논문 본문의 30.28 meV/Å 을 나란히 놓지 마라.** test set 이 완전히 다르다(Li₃PS₄ 243구조 vs 41계 전체). **수가 우연히 비슷한 것뿐이다.**

- **Step 1 — 같은 스냅샷 힘 대조 (하루, GPU 거의 안 씀)** ★ 우리 계에서의 첫 공정 대결
  **새 MD 를 돌리지 않는다.** 이미 있는 UMA 궤적에서 스냅샷을 뽑아 DPA-SSE 단일점만 찍는다.
  - 표본: `b2o3_uma_vs_dft_force_prereg` 가 이미 정한 **결정적 규칙**을 그대로 재사용한다 — 700 K, 시드 s2·s3, 생산 2–50 ps 창 안 등간격 5프레임. **사람이 고르지 않는다.**
  - ⛔ **그 봉인 카드를 수정하지 않는다.** DPA-SSE 는 **별도의 새 카드**로 붙인다(같은 표본, 다른 보고량).
  - **보고량**: 절대 |ΔF| 가 아니라 **비(ratio)** 다. 봉인 카드가 이미 논증한 그대로 — 절대 힘 차이는 의사포텐셜·범함수 계통오차를 싣는다. DPA-SSE(PBEsol/VASP-PAW) vs 우리 QE(PBE/USPP) 는 그 차이가 **UMA 때보다 더 크다**(범함수까지 다르다).
  - **1차 판정량**: `dF_DPA(modelc) / dF_UMA(modelc)` 와 원소별 분해(Li vs P/S/Cl). 우리 물음은 *"DPA-SSE 가 UMA 보다 정확한가"* 이므로 **동일 스냅샷·동일 DFT 참조**에 두 모델을 세운다.
  - ⛔ **b2o3 는 이 시험에서 뺀다**(§11-3 이유).

- **Step 2 — 범함수 분리 (1–2일, kgy CPU 빌드)**
  Step 1 에서 가장 크게 갈린 프레임 **20–40개**에 **PBE 와 PBEsol 단일점을 둘 다** 찍는다. 그래야 *"DPA-SSE 가 틀렸다"* 와 *"우리 참조가 PBE 라 DPA-SSE 가 불리했다"* 를 가른다. 이 단계 없이 Step 1 만으로 판정하면 **PBEsol 모델을 PBE 자로 재는 것**이라 DPA-SSE 에 부당하다.
  - 설정은 봉인 카드 §4 의 레시피 그대로(52/520 Ry · Γ-only · fixed occ · conv_thr 1e-8 · scf only · tprnfor). 유사포텐셜 해시도 그대로. **범함수만 바꾼 짝**을 만든다.

- **Step 3 — NEB + NVE 두 장 (2–3일)**
  - **`Fig. 5a,b` 재현**: comp1/modelc 의 Li 호핑 경로 하나를 골라 **UMA · DPA-SSE · 우리 DFT** 로 같은 NEB 를 돌린다. `Fig. 5` 가 보여준 것이 정확히 이 그림이고, **UMA 가 base 무리(≈1/3 장벽)에 속하는지 아닌지가 여기서 한 장으로 판정**된다. 우리 Ea 값(comp1 0.253 / modelc 0.224 eV, MLIP-MD)과의 정합도 같이 본다.
  - **`Fig. S3` 재현**: comp1 500 K NVE 100 ps 드리프트를 **UMA 설정 그대로** 잰다. ⚠ 이건 지금 당장 해야 하는 저비용 검사다 — 우리는 Langevin **NVT** 만 써 왔고, thermostat 이 드리프트를 **가려 준다**. 우리 UMA 실행이 보존형 힘을 쓰는지(직접 힘 예측 헤드인지 autograd 인지)를 **문서가 아니라 실측으로** 확인하는 유일한 길이다.

- **Step 4 — 증류 (1–2주, Step 1–3 이 DPA-SSE 편일 때만)**
  §4.5 레시피를 우리 조성(comp1 / modelc / LPSOCl)에 적용. DFT 추가 비용 **0**. 그다음 우리 200 ps × 3시드 × 3온도 규약을 증류 모델로 **재실행하고 UMA 결과와 나란히** 놓는다.
  - ⚠ 그 순간 **두 개의 서로 다른 σ·Ea** 가 생긴다. `comparison_group` 을 새로 파고 `canonical_registry` 규율(§CLAUDE.md 데이터 규율)을 먼저 정한 뒤에 돌린다. **결과를 보고 어느 쪽을 정본으로 할지 정하면 안 된다** — 마감 규율 위반이다.

- **Step 5 — 합법적 committee (선택)**
  증류 학생 모델을 **시드만 바꿔 M ≥ 4**. §11-2 의 경고(증류 분산 ≠ 모델 오차)를 카드에 먼저 못박고 시작한다.

### 11-5. 값 대조표 (⛔ 소환값 — 우리 db 와 섞지 않는다)

| 항목 | DPA-SSE (이 논문) | 우리 | 차이 / 해석 |
|---|---|---|---|
| **σ₃₀₀K, Li₆PS₅Cl** | `figure-read ≈ 7` mS/cm (실험 ≈3) | ⛔ **우리는 σ 절대값 인용 금지**(CLAUDE.md MLIP-MD 규율) | 비교 불가. 다만 **DPA-SSE 도 실험 대비 2.3× 과대**라는 사실은 *"MLIP σ 절대값을 못 믿는다"* 는 우리 규율을 **문헌이 뒷받침**해 준다 |
| **Ea, Li₆PS₅Cl** | `figure-read ≈ 0.24` eV (실험 ≈0.324) | comp1 **0.253 eV** (UMA-MD, ⚠ 단일 궤적) | **0.24 vs 0.253 — 0.013 eV 차이.** 놀랍게 가깝다. 다만 **둘 다 실험(≈0.32)보다 0.07–0.08 eV 낮다** ⇒ **UMA 와 DPA-SSE 가 같은 방향으로 같은 크기만큼 빗나간다.** 이건 두 모델의 공통 결함일 수도, MLIP-MD 로 Ea 를 뽑는 방식(짧은 궤적·Nernst–Einstein·Haven=1)의 공통 결함일 수도 있다. **후자라면 모델을 바꿔도 안 낫는다** — 이게 이번 digest 에서 가장 불편한 발견이다 |
| **Ea, Cl-rich** | 논문은 Cl-rich 의 Ea 를 안 냈다(σ 만) | modelc **0.224 eV** (단일궤적) / **0.197 ± 0.032** (3-seed) | 대조 불가 |
| **σ 추세, Cl-rich** | x=0→0.7 에서 7.8→15.7 mS/cm (**2.0×**) | comp1→modelc **D 2.6×↑**, Ea↓ | ✅ **방향 일치.** 우리 x=0.6 에 해당하는 논문 보간 ≈2× 와 우리 D 비 2.6× 는 같은 자릿수. ⚠ D 비와 σ 비는 다른 양(V·T 인자)이라 **직접 등치 금지** |
| **O 도핑 효과** | `Fig. S11`: σ **단조 감소**(11.8→7.0, −41%) | 우리 LPSOCl 축은 **gap 2.2309 eV** 등 전자구조가 정본이고 **MD 전도도는 별도 판정** | ⚠ **문헌은 O 도핑이 전도도에 불리하다고 말한다.** 우리가 O/B₂O₃ 를 "개선"으로 프레이밍한다면 **어느 축에서 개선인지 반드시 명시**해야 한다 — 수분/산화 안정성 축이지 전도도 축이 아니다. `Fig. S11` 캡션이 그 트레이드오프를 그대로 쓴다 |
| **범함수** | PBEsol (라벨) | PBE (우리 DFT), UMA 는 OMat24 | ⛔ 흡수되지 않는 계통 차이. 절대값 이식 금지 |
| **무질서 처리** | 미기재(`50%@4c` 라벨만) | 우리는 실험 점유 decorate 계열 | 대조 불가 — 논문의 공백(§14-2) |
| **MSD 창** | **미기재** | **2–50 ps 고정, 자유절편** | ⛔ **D 절대값 비교 불가.** 이 한 줄이 §11-5 전체를 "추세만" 으로 제한한다 |

---

## 12. 적용 인사이트

1. **`Fig. S11` 이 우리 O 도핑 서사의 방향을 교정한다.** 실험(Peng 2022)과 DPA-SSE 가 함께 *"O 도핑 → σ 감소"* 를 말한다. 우리 +B₂O₃ / +O 계를 "성능 개선"으로 쓰려면 **축을 명시**해야 한다 — 수분/산화 안정성이지 이온전도가 아니다. 우리 규율의 *"Cl-rich oxidation stability 는 항상 축을 대라"* 와 같은 종류의 규율이 **O 도핑에도 필요하다.**
2. **`Fig. 5c` 형식의 한 장이 UMA 검증의 최단 경로다.** D vs 1000/T 판에 AIMD·실험·여러 MLIP 를 얹는 그림. 우리는 이미 600/800/1000 K 3점을 갖고 있으므로 **DPA-SSE 를 받기만 하면** 그 판을 만들 수 있다. UMA 가 base 무리 쪽인지 DPA-SSE 쪽인지가 한 장으로 갈린다.
3. **증류가 우리 UQ 병목을 물리적으로 푼다.** 오늘 들어온 UQ 3편이 요구한 것(M≥4 committee, 멀티시드, 긴 궤적)은 전부 **비용 때문에 못 하던 것**이다. 증류 DPA-SSE 는 UMA 대비 ~75× 처리량이고, 교사가 공짜로 라벨을 찍으므로 **DFT 추가 비용 없이** committee 를 만들 수 있다. 단 §11-2 의 경고 — 그 committee 가 재는 것은 증류 분산이지 모델 오차가 아니다.
4. **`Fig. S3`(NVE 드리프트)를 우리 파이프라인에 지금 넣는다.** 저렴하고(100 ps 1런) 결정적이다. Langevin NVT 는 비보존성을 **가려 준다** — 우리는 이 시험을 한 번도 안 했다.
5. **`Fig. 4` 가 fine-tune 예산의 현실적 견적이다.** 우리가 Nd–O 나 B₂O₃ 로 MLIP 를 밀고 싶다면 **20–60 프레임의 DFT 라벨**이 출발선이다(from-scratch 대비 ~10× 절약). 우리 QE 스택에서 62–128원자 Γ-only scf 가 5–40분/점이므로 **40프레임 ≈ 4–27시간** `digest 계산 (원논문 미보고)` — **감당 가능한 규모다.** 다만 그건 DPA-SSE 를 fine-tune 한다는 뜻이고, 그러면 §11-2 의 "PBEsol 모델을 PBE 라벨로 적신다" 문제를 **먼저 정리**해야 한다.
6. **논문 자신의 자백을 활용한다** — `Fig. 2c,d` + `Fig. 4c,d` 는 *"범용 모델도 이 데이터로 적시면 DPA-SSE 급"* 을 보인다. 즉 **우리가 진짜로 사야 하는 것은 DPA-SSE 체크포인트가 아니라 그 54,771 프레임 데이터셋**일 수 있다. 그걸로 **UMA 를 fine-tune** 하면 아키텍처를 안 바꾸고 훈련 분포만 고칠 수 있다 — 우리 스택 변경이 최소다. (⚠ UMA fine-tune 가능성은 이 논문이 답하지 않는다, §14-4)

---

## 13. ★ 비판 — 이 논문의 약한 곳

**13-1. 편집 품질이 낮다** (여러 건이라 논문 전체의 꼼꼼함을 의심하게 한다)
- **PBEsol 을 쓴다면서 ref 47 로 PBE 논문**(Perdew–Burke–Ernzerhof PRL 77, 3865 (1996))을 인용. PBEsol 은 PRL 100, 136406 (2008) 이다.
- **학습률 스케줄이 같은 문단에 두 개**(0.001→12M steps vs 2e-4→2M steps). 어느 것이 본체인지 알 수 없다.
- **본문 상호참조 오류 2건**: 무질서 퍼텐셜에너지를 *"Figure 6d"* 라 했으나 실제는 `Fig. 6b`; 증류 성능을 *"Fig. S10b,c"* 라 했으나 실제는 `Fig. S12b,c`.
- **축 라벨/단위 오식 3건**: `Fig. 4b` y축이 `F_DFT`(→`F_DP`), `Fig. 4d` y축 `eV/atom`(→`eV/Å`), `Fig. S12b` 양축 `meV/atom`(→`eV/atom`).
- **`Fig. 6b` inset 의 자리 배정(S 4c / Cl 4a)이 본문 서술(halide@4c ↔ S@4a)과 뒤집혀 있다.** 4a/4c 를 구분하는 우리에겐 사소하지 않다.
- **화합물 표기 흔들림**: `Li₂B₂S₅` ↔ `L2B2S5`, `Fig. 1` 의 `Li₂SiS`(→Li₂SiS₃?), `LiP₃S4`(→Li₃PS₄?).
- **`Fig. S1` SI 캡션이 c,d 패널을 설명하지 않는다** — 캡션은 *"50 K 10 스텝"* 만 말하는데 c,d 는 명백히 가열궤적이다(본문에서 유추해야 한다).

**13-2. 재현성 정보가 결정적으로 빠져 있다 — 이 논문의 가장 큰 결함**
표가 **0개**이고, **MD 생산 조건이 어디에도 없다**: 셀 크기·원자수(효율 벤치의 1350 외), 궤적 길이(`Fig. 6b` 의 5 ns 외), **시드 개수**, thermostat, **MSD 피팅 창**, **`Fig. 6a/6c` 오차막대의 정의**. 오늘 함께 들어온 UQ/전송계수 문헌(Maginn 2019 · Pranami 2015 · Zaby 2026 · de Klerk 2018)이 공통으로 요구하는 것이 정확히 이 목록이다. **σ·D·Ea 를 소환값으로도 쓰기 어렵게 만드는 공백**이고, 우리 규약(2–50 ps 창)과의 대조 자체가 불가능하다.

**13-3. 하필 LPSCl 에서만 이상 신호가 둘이다** (우리 계다)
- `Fig. S1a`(평형근처 E MAE): **LPSCl 만 DPA-SSE 막대가 없다.** 다른 5계엔 다 있다. 로그축 하한(10⁻¹) 아래라 안 보이는 것(즉 <0.1 meV/atom, 지나치게 좋음)일 수도, 누락일 수도 있다 — **어느 쪽인지 논문이 말하지 않는다.**
- `Fig. S1d`(가열궤적 F MAE): **CHGNet base 24 < DPA-SSE 31 meV/Å.** 41계 벤치 전체에서 base 범용모델이 DPA-SSE 를 이긴 **유일한 칸**이고, 하필 LPSCl 이다. 같은 칸의 M3GNet base(45)도 다른 계(83–120)보다 유난히 낮다. 본문은 이 역전을 **언급조차 하지 않는다.**
- `Fig. 1` heatmap 에서 **Cl 칸 색이 옅다**(프레임 수 적음). 세 신호가 같은 방향을 가리킨다: **Cl 계 데이터가 상대적으로 얇다.**

**13-4. "excellent agreement" 는 과장이다**
`Fig. 6c`: 5계 중 4계에서 σ 를 **1.6–2.8× 과대**. `Fig. 6d`: LPSCl Ea **0.24 vs 실험 0.324** — 0.084 eV 차이인데 본문은 *"very close to the experimental measurement"* 라고 쓴다. 오차막대가 커서 겹칠 뿐이고, **오차막대가 크다는 것 자체가 자랑이 아니다**. 정직한 서술은 *"범용 모델의 1–2 자릿수 오차를 2배 수준으로 줄였다"* 이지 *"실험과 일치한다"* 가 아니다.

**13-5. 증거 배치가 자기 편이다**
- `Fig. 2c,d`(본문)에는 **fine-tune 한 비교군만** 넣고, **base 모델의 참담한 수치는 SI(`Fig. S1`, `Fig. S2`)로 뺐다.** 본문만 읽으면 "다들 비슷한데 DPA-SSE 가 조금 낫다"로 읽힌다.
- 반대로 `Fig. 5c`(본문)에는 base 를 넣었는데, 이건 base 가 나쁠수록 논지에 유리한 그림이다.
- **`Fig. S2` 는 본문이 부여한 역할("호핑 사건의 에너지 과소평가")을 감당하지 못한다** — eV/atom 축이라 0.35 eV 장벽은 52원자 셀에서 6.7 meV/atom 이고 점 하나보다 작다. 그 주장의 진짜 증거는 `Fig. 5a,b` 다.

**13-6. `Fig. S4` 는 격자 정확도의 근거가 못 된다**
2.5–22.5 Å 축에 41계를 다 얹었다. 10 Å 계의 **1% 오차(0.1 Å)** 는 이 축에서 마커 반지름 안이다. σ 는 격자상수에 민감하므로(부피 인자 + 병목 크기), **"격자가 잘 맞는다"는 정량 주장에 이 그림을 인용하면 안 된다.** 잔차 히스토그램이나 계별 %오차 표가 필요한데 **둘 다 없다.**

**13-7. `Fig. 3c` t-SNE 를 커버리지 증명으로 쓴다**
*"points representing the solid solutions sit within the regions spanned by the training sets"* — t-SNE 는 **거리를 보존하지 않는다.** "안/밖"은 t-SNE 평면에서 의미가 없다. 게다가 눈으로도 Component-1 ≈ 60–90 에 **연두 없이 주황만 있는 구역**이 보인다. 일반화의 진짜 증거는 `Fig. 3a,b` 의 MAE 이고, t-SNE 는 삽화다.

**13-8. 이해충돌·자기 비교 구조**
저자 다수가 **DP Technology / AI for Science Institute** 소속 = DeePMD·DPA-2 개발사다. 비교 상대 중 `DPA-2-MP` 는 **자기 아키텍처**이고, 그것만 DPA-SSE 와 동급 성능을 낸다(`Fig. 4c,d`). MACE 는 **small 버전**을 썼고 M3GNet 은 **원 구현이 아니라 matgl** 로 fine-tune 했으며, 논문은 M3GNet 의 열세를 *"significantly smaller model size"* 로 설명한다 — **모델 크기를 맞춘 비교가 없다.** 경쟁 모델의 최신/최대 체크포인트를 쓰지 않은 벤치마크다.

**13-9. UQ 가 전혀 없다**
훈련은 DP-GEN(모델 불일치 기반 능동학습)으로 하면서, **최종 모델의 예측 불확실성은 한 번도 보고하지 않는다.** committee spread 도, 앙상블도, 외삽 등급(extrapolation grade)도 없다. `Fig. 6a/6c` 의 오차막대는 정의조차 안 나온다. 그러면서 **훈련 분포 밖(`Fig. 4a` LBS)에서 zero-shot 이 162 meV/atom 로 무너진다**는 것을 자기가 보였다 — **"언제 못 믿을지"를 사용자가 알 방법이 없다.** 이것이 우리가 이 모델을 committee 멤버가 아니라 **대조군**으로만 쓸 수 있는 또 하나의 이유다.

**13-10. Nernst–Einstein Haven=1 을 그냥 쓴다**
`ref 50` France-Lanord & Grossman (PRL 2019, *"Correlations from Ion Pairing and the Nernst-Einstein Equation"*)을 인용하면서 **그 논문의 경고를 적용하지 않는다.** argyrodite 의 협동 호핑(이 논문 자신이 `Fig. 5` 에서 "concerted"라고 부른다)은 정확히 Haven ratio 를 1 에서 밀어내는 기제다. σ 가 계통적으로 과대인 것(§13-4)의 일부가 여기서 왔을 수 있는데 **논의가 없다.**

---

## 14. ⛔ 못 하는 것 / 확인 못 한 것

1. **MD 규약을 우리 것과 정량 대조할 수 없다.** MSD 창·궤적 길이·시드·셀 크기가 논문에 없다(§13-2). 우리 2–50 ps 창과 이 논문 D 를 **나란히 놓으면 안 된다.**
2. **무질서 배열 방법을 모른다.** `50%@4c` 라벨과 `Fig. 6b` inset 이 전부다. SQS 인지, 무작위 decorate 인지, 몇 개 배열을 평균했는지 알 수 없다 — **우리 무질서 처리와 대조 불가.**
3. **모델·데이터를 실제로 받아 보지 못했다.** AIS Square 링크(model id 266 / dataset id 217)와 Bohrium 노트북 71679486918 은 **PDF 하이퍼링크에서 추출한 것**이고, 접근 가능 여부·라이선스·가입 요구·파일 크기·DeePMD 버전 요구를 **확인하지 않았다.** §11-4 Step 0 이 이걸 확인하는 단계다.
4. **DPA-SSE 에 새 원소(Nd)를 추가할 수 있는지 모른다.** DPA-2 의 원소 임베딩이 15원소로 고정 학습됐는지, type map 을 확장해 fine-tune 할 수 있는지 — **이 논문은 답하지 않는다.** 마찬가지로 **UMA 를 이 데이터셋으로 fine-tune 할 수 있는지**(§12-6)도 이 논문 밖이다.
5. **UMA 와의 직접 비교는 이 논문에 없다.** 벤치마크 대상은 MPtrj 세대 5종뿐. *"UMA 도 D 를 과대할 것"* 은 **가설**이고, 검사는 §11-4 Step 1/3 이다.
6. **안 본 그림 4장**: `Fig. S6`(LBS 구조), `Fig. S7`(M3GNet 학습곡선), `Fig. S8`(LSiPS·LSnPS D), `Fig. S9`(LPSI MSD·PE). 이 넷에 대한 서술은 **본문 문장을 그대로 옮긴 것**이고 그림을 확인하지 않았다. 특히 `Fig. S9` 의 *"LPSI 는 질서상이 더 안정"* 주장은 눈으로 검증 안 했다. **선정 기준**: 논문의 주장을 떠받치는 그림 + 우리 축(이온전도·무질서·MLIP 정확도·비용)에 걸리는 그림을 우선했고, 이 넷은 둘 다 아니라고 판단해 뺐다.
7. **`Fig. S5a` 의 개별 점을 특정할 수 없다** — 22계에 10색을 순환시켜 색이 겹친다. *"LPSCl 의 분해에너지 = 0.65 eV/f.u."* 같은 문장을 쓰면 안 된다.
8. **`Fig. 5a` 의 본문값(0.28 eV)과 그림 눈금(≈0.31)이 0.03 eV 어긋난다.** 장벽 정의(끝점 기준? 최저점 기준?)를 논문이 밝히지 않아 어느 쪽이 맞는지 판정 못 했다. **인용은 본문값 0.28 eV 로 하고, 그림 판독임을 밝힌 `≈0.31` 은 참고로만.**
9. **효율 비교는 교차 하드웨어다** (V100+12코어 vs 우리 A6000). §11-4 표의 환산은 **자릿수 판정용**이지 약속이 아니다.
10. **σ·D·Ea 를 우리 db 에 넣지 않는다.** 전부 소환값이고, MSD 창 미기재(§14-1)로 방법 정합조차 확인 안 된다.

---

## 15. 인용 가능 문장 (deck / 원고용)

- "MPtrj 로 사전학습된 범용 MLIP 들은 황화물 고체전해질의 Li 호핑 장벽을 DFT 대비 약 1/3 로 과소평가하고, 그 결과 상온 확산계수를 30–220× 과대평가한다 (Wang et al., npj Comput. Mater. 11, 266 (2025), Fig. 5)."
- "황화물 전용 사전학습 deep potential(DPA-SSE)은 15원소·41계·54,771 스냅샷을 0–1200 K / 0–2 GPa 비평형까지 샘플링해 학습했고, 에너지 1.58 meV/atom · 힘 30.28 meV/Å 를 1150 K 가열궤적까지 유지한다."
- "훈련에 없던 화합물에 대해 20–60 프레임의 DFT 라벨만으로 fine-tune 하면 from-scratch 로 760 프레임을 학습한 모델을 능가한다 — 약 10× 의 데이터 절약 (Fig. 4c,d)."
- "Li₅.₅PS₄.₅₋ₓOₓCl₁.₅ 에서 O 도핑은 상온 이온전도도를 단조 감소시키며(계산·실험 모두), 이는 수분 안정성 향상과의 트레이드오프로 보고되었다 (Fig. S11)."
- ⚠ **쓰면 안 되는 문장**: *"DPA-SSE 는 실험 이온전도도를 정확히 재현한다"* — `Fig. 6c` 는 5계 중 4계에서 1.6–2.8× 과대다. *"UMA 도 이 논문에서 나쁘게 나왔다"* — **UMA 는 시험되지 않았다.**

---

## 16. 이 digest 가 남기는 열린 항목

| # | 항목 | 다음 행동 |
|---|---|---|
| 0 | **`comparison_vs_ours.md` §J-1 의 명시적 한계 #3 (*"Cl 이 없다"*)이 이 논문으로 메워진다** | J-1 에 그 사실을 기록 (병합자 몫) |
| 1 | AIS Square 모델/데이터 접근 가능한가 (id 266 / 217) | §11-4 Step 0 → Step 0.5(DFT 0회 벤치) |
| 2 | **UMA-s-1p1(omat)이 보존형 힘을 쓰는가** | §11-4 Step 3, `Fig. S3` 형식 NVE 100 ps — **저비용·고가치, 지금 할 수 있다** |
| 3 | UMA 가 `Fig. 5c` 의 base 무리에 속하는가 | §11-4 Step 3 NEB |
| 4 | DPA-SSE 를 b2o3 봉인 카드의 세 번째 심판으로? | **⛔ 안 된다** (§11-3) — comp1/modelc/LPSOCl 만 |
| 5 | UMA 를 DPA-SSE 데이터셋으로 fine-tune 할 수 있나 | 이 논문 밖 (§14-4) |
| 6 | 우리 Ea 와 DPA-SSE Ea 가 **둘 다 실험보다 0.07–0.08 eV 낮다** | **모델 문제가 아니라 방법 문제일 수 있다** (§11-5) — 별도 조사 필요 |
