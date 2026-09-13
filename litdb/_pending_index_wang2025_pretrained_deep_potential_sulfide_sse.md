# ⏸ 병합 대기 — `wang2025_pretrained_deep_potential_sulfide_sse`
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 2026-09-09 · litdb-curator 다중 동시 실행으로 **`INDEX.md`·`comparison_vs_ours.md` 직접 수정 금지**를
> 받아, 넣어야 할 내용을 여기 적어 둔다. 충돌이 풀리면 **아래 블록을 옮기고 이 파일을 지운다.**
>
> ✅ 이 편은 **물성값이 있다** (LPSCl·Cl-rich·O-doped 의 σ₃₀₀K·Ea, 전부 `figure-read` 소환값)
> ⇒ **축 A(이온전도)에 넣는다.** 동시에 MLIP 방법론 편이므로 **§J 축에도 블록이 필요하다.**
> ⛔ 단 **σ·D 절대값은 우리 db 와 같은 표에 놓지 않는다** (MSD 창·시드·셀 미기재, digest §13-2/§14-1).

---

## ① `INDEX.md` 에 추가할 행

| `papers/wang2025_pretrained_deep_potential_sulfide_sse.md` | **[MLIP·★★황화물 SE 전용 사전학습 deep potential = UMA 의 대조군 후보]** **Ruoyu Wang**¹²³†, **Mingyu Guo**⁴⁵†, Yuxiang Gao¹², Xiaoxu Wang⁴⁶, Yuzhi Zhang⁴⁶, Bin Deng⁴, **Mengchao Shi**³⁴\*, **Linfeng Zhang**⁴⁶\*, **Zhicheng Zhong**¹²³\* (¹²USTC 인공지능·데이터과학부/쑤저우고등연구원 ³Suzhou Lab ⁴**DP Technology** ⁵중산대 ⁶AI for Science Institute; †공동1저자 2인), "**A pre-trained deep potential model for sulfide solid electrolytes with broad coverage and high accuracy**" (***npj Comput. Mater.* 2025, 11, 266**, DOI `10.1038/s41524-025-01764-6` · CC BY-NC-ND 4.0 · 접수 2025-07-24 / 수락 2025-08-04; 본문 10 pp · SI 10 pp · Fig **7 + S1–S12** · **Table 0개** · refs 50+4) — **모델 이름 `DPA-SSE`**. ⚠ **서지 대조**: 1저자 기억(`R. Wang, M. Guo, Y. Gao, X. Wang, Y. Zhang 외, npj Comput. Mater. 2025`) **전부 맞다**; 다만 교신은 **Shi / L. Zhang / Zhong** 3인이고 실질 소속 축은 **DeePMD 개발사 DP Technology** 다(자기 프레임워크 벤치마크 = 이해충돌 축, digest §13-8). **★★ 훈련셋에 우리 계가 들어 있다**: `Fig. 1` 1층 6종에 **Li₆PS₅Cl·Br·I 가 포함**(+LGPS 계열 3종), 2층 20종(Li₃PS₄·Li₇P₃S₁₁·Li₇PS₆·LiBS₂/Li₃BS₃/Li₅BS₄ 등), 3층 14종(LiCl·LiBr·LiI·**Li₂O**·Li₂S·**B₂S₃**·P₂S₅ 등), 4층 Li 금속 = **41계 · 15원소 · 54,771 스냅샷**(VASP·PAW·**PBEsol**·600 eV·KSPACING 0.3·힘 0.01 eV/Å; **DP-GEN 능동학습, NPT 0–1200 K / 0–2 GPa 로 일부러 비평형 샘플링**). ⚠ **B·O 는 원소로만 있고 B–O 결합은 41계 어디에도 없다**(B 는 B–S 만, O 는 Li₂O 만) · **란탄족 0 ⇒ Nd 는 범위 밖**. **정확도**: 전체 test **E 1.58 meV/atom · F 30.28 meV/Å**(Fig 2a,b 패널 표기는 1.57), 150→1150 K 가열궤적에서도 유지(⚠ **Fig. 2c 의 LSnPS 는 `figure-read ≈2.5` 로 본문 *"within 2 meV/atom"* 을 넘는다**), **훈련에 없는 고용체**(LXPS·**LPSX = Li₆PS₅Cl₁₋ₓ₋ᵧBrₓIᵧ**)에서도 **1.56 / 29.15** (`Fig. 3`; 인셋에서 **halide 혼합이 cation 혼합보다 오차 넓다** = 우리 축이 더 어려운 쪽). **★★ 범용 MLIP 유죄판정**(`Fig. 5`): base MPtrj 모델들의 LGPS c축 호핑장벽 `figure-read ≈0.12`(M3GNet)–`≈0.20`(DPA-2-MP) vs **DFT ≈0.345** = **1/3 수준**, 그 결과 **300 K D 를 `≈1.3×10⁻¹⁰`~`≈1×10⁻⁹` m²/s 로 DPA-SSE(≈4.5×10⁻¹²) 대비 30–220× 과대**(본문 Discussion 은 *"more than an order of magnitude"* 라고 **보수적으로** 씀 — 그림은 두 자릿수). ⛔⛔ **UMA 는 시험 대상이 아니다** — 피고는 **DPA-2-MP · MACE-MP-0a(small) · M3GNet-MP-2021.2.8 · CHGNet · ORB-v2** 전부 **MPtrj 세대**이므로 *"따라서 UMA 도 그럴 것"* 은 **가설이지 이 논문의 결론이 아니다**. **★★★ 우리 조성이 SI 에 직접 있다**: `Fig. S10a` **Li₆₋ₓPS₅₋ₓCl₁₊ₓ**(= 우리 **modelc = x 0.6**) σ₃₀₀K `figure-read` 7.8/11.0/11.8/15.7 (x=0/0.3/0.5/0.7, 실험 7.1/9.2/16.1/17.3) · `Fig. S10b` Br 치환 4.6/10.4/15.5/18.6 · **`Fig. S11` Li₅.₅PS₄.₅₋ₓOₓCl₁.₅ 의 O 도핑은 σ 를 단조 감소**(계산 11.8→7.0, 실험 9.5→6.0)시키며 캡션이 *"which help improve moisture stability"* 로 **수분안정성↔전도도 트레이드오프**를 명시 ⇒ **우리 +O/+B₂O₃ 서사에 축 명시 의무를 부과한다**. **`Fig. 6b` 무질서**: LPSCl 상온 **5 ns** MSD — 질서상은 `≈11.5 Å²` 에서 **포화**(장거리 수송 0), 무질서상(`50%@4c`)만 선형 증가해 `≈38 Å²`, 그리고 **무질서상이 `≈7.5 meV/atom` 더 안정**. ⚠ **inset 자리 라벨(`S 4c`/`Cl 4a`)이 본문 서술(halide@4c↔S@4a)과 뒤집혀 있다**. **`Fig. 6c,d`**: LPSCl σ `≈7` vs 실험 `≈3`(**2.3× 과대**), **Ea `≈0.24` vs 실험 `≈0.324`(0.084 eV 과소)** — 본문 *"excellent agreement"·"very close"* 는 **과장**(5계 중 4계에서 σ 1.6–2.8× 과대, Ea 0.02–0.08 eV 과소). **★★ fine-tune 비용 실측**(`Fig. 4`): 미학습 Li₂B₂S₅(mp-29410) zero-shot **162.65 meV/atom · 369.16 meV/Å**(에너지에 **+0.16 eV/atom 계통 편향**) → **20 프레임**이면 **3.44 / 89.07**, **60 프레임**이면 **from-scratch 760 프레임을 능가**(≈**10× 데이터 절약**) · **DPA-2-MP-ft 가 DPA-SSE 와 거의 같은 데이터효율**을 내서 저자 스스로 *"fine-tuning as a viable future direction"* 이라 씀 ⇒ **효과의 본체는 "황화물 전용 체크포인트"가 아니라 "비평형 데이터"** 일 수 있다. **★★ 증류·비용**(`Fig. 7`, LGPS 1350원자 V100+12코어): 사전학습 DPA-SSE `≈8.6×10⁻³` s/step·atom 은 **MACE-ft 보다도 46× 느리다**; 증류 학생(표준 DeePMD) `≈1.65×10⁻⁵` = **≈520× 가속**에 정확도만 **2.10 meV/atom / 48.44 meV/Å**(교사 1.59 / 30.0) ⇒ **우리 200 ps×3시드×3온도 규약에 사전학습 원본은 못 쓴다(558원자 환산 ≈50일), 증류하면 ≈2.3시간**(`digest 계산`, 교차 하드웨어 주의). **`Fig. S3` 보존성**: **orb-v2(비보존)는 500 K NVE 100 ps 에서 ΔE `≈6–7 eV/atom` 폭주**, DPA-SSE·MACE 는 평탄 ⇒ 본문이 벤치를 **보존형으로 한정**한 근거. **공개**: 모델·훈련데이터 **AIS Square**(model id **266** / dataset `Solid_State_Electrolyte` id **217**) + Bohrium 노트북 **71679486918** — ⚠ **접근·라이선스 미확인**. **🔴 우리 지적 10건**(digest §13): ① **PBEsol 을 쓴다면서 ref 47 로 PBE 논문 인용** · **학습률 스케줄이 같은 문단에 두 개**(0.001→12M vs 2e-4→2M) · **본문 상호참조 오류 2건**(`Fig. 6d`→실제 6b, `Fig. S10b,c`→실제 S12b,c) · **축 단위 오식 3건**(`Fig. 4b` y=`F_DFT`→`F_DP`, `Fig. 4d` `eV/atom`→`eV/Å`, `Fig. S12b` `meV/atom`→`eV/atom`) ② **재현성 정보 부재가 결정적** — 표 0개이고 **MD 셀·궤적길이·시드 수·thermostat·MSD 창·오차막대 정의가 전부 없다** ⇒ **σ·D 를 우리 규약과 정량 대조 불가** ③ **하필 LPSCl 에서만 이상 신호 둘** — `Fig. S1a` 에서 **LPSCl 만 DPA-SSE 막대가 없고**, `Fig. S1d` 에서 **CHGNet base(≈24) < DPA-SSE(≈31) meV/Å** 로 41계 벤치 전체의 **유일한 역전**이 우리 계에서 나며 본문이 **언급조차 안 한다**; `Fig. 1` heatmap 에서 **Cl 칸 색이 옅다**(프레임 수 적음) ⑤ **증거 배치가 자기 편** — 본문 `Fig. 2c,d` 에는 ft 모델만 넣고 base 의 참담한 수치는 SI 로 뺐다; **`Fig. S2` 는 본문이 부여한 "호핑 사건 에너지 과소평가" 역할을 감당 못 한다**(eV/**atom** 축 0.5 폭인데 52원자 셀의 0.35 eV 장벽은 6.7 meV/atom) ⑥ **`Fig. S4`(격자 parity)는 2.5–22.5 Å 축이라 1% 오차가 안 보인다** ⇒ 격자 정확도 근거로 인용 금지 ⑦ **`Fig. 3c` t-SNE 를 커버리지 증명으로 사용**(거리 비보존; 눈으로도 Component-1 60–90 에 연두 없이 주황만 있는 구역) ⑧ **이해충돌** — 비교군 중 `DPA-2-MP` 만 자기 아키텍처이고 그것만 동급, MACE 는 **small**, M3GNet 은 **matgl** 판, **모델 크기 맞춘 비교 없음** ⑨ **UQ 가 0건** — DP-GEN(모델 불일치 능동학습)으로 훈련하면서 **최종 모델의 불확실도를 한 번도 보고 안 함**, `Fig. 6` 오차막대 정의조차 없음 ⑩ **Nernst–Einstein Haven=1** 을 그냥 씀(ref 50 France-Lanord & Grossman 을 인용하면서 그 경고는 적용 안 함) — 자기가 `Fig. 5` 에서 *"concerted"* 라 부른 협동호핑이 정확히 Haven≠1 의 기제다. **⛔ committee 판정**: **부적격**(§J-11) — 아키텍처·코퍼스·**참조 범함수(PBEsol vs UMA 의 PBE 계열)** 가 모두 달라 Grasselli §2.2 *"equivalent models"* 전제가 깨진다. **✅ 대신 독립 검증 기준(대조군)으로는 최적**이고, **공개 데이터셋으로 시드만 바꿔 M≥4 를 직접 학습하면 합법적 committee 가 성립**한다. **그림 19장 중 13장 실제 열람**(`Fig. S4`·`S11` 은 자동 크로퍼가 "거의 백지"로 오판해 **SI 해당 쪽을 수동 전면 렌더**해 살렸고 `figures.json` 에 fallback 표시; **안 본 것 = `Fig. S6·S7·S8·S9`**). | **MLIP(황화물 SE 전용 사전학습 DP)·이온전도 소환값·UMA 대조군 판정** |

---

## ② `comparison_vs_ours.md` **§A (이온전도)** 에 추가할 블록

> 약칭 제안: **[Wang25DPA]**
> ⛔ **σ·D 절대값을 우리 db 와 같은 셀에 넣지 않는다** — MSD 창·시드·셀 크기 미기재(digest §13-2).
> 아래는 **추세·부호·순서**만 옮긴 것이다.

**[Wang25DPA] `wang2025_pretrained_deep_potential_sulfide_sse` — MLIP-MD 로 낸 소환값 (Fig. 6c,d / S10 / S11)**

| 항목 | [Wang25DPA] (MLIP-MD, DPA-SSE) | 우리 (UMA-s-1p1 MLIP-MD) | 판정 |
|---|---|---|---|
| **Ea, Li₆PS₅Cl** | `figure-read ≈ 0.24 eV` (실험 `≈0.324`) | comp1 **0.253 eV** ⚠단일궤적 | 🔵 **0.013 eV 차 — 놀랍게 가깝다.** 그런데 **둘 다 실험보다 0.07–0.08 eV 낮다** ⇒ **같은 방향·같은 크기의 빗나감.** 모델 공통 결함일 수도, **MLIP-MD 로 Ea 를 뽑는 방식(짧은 궤적·NE·Haven=1)의 공통 결함**일 수도 있다. 후자면 **모델을 바꿔도 안 낫는다** — 별도 조사 항목 |
| **Cl-rich σ 추세** | Li₆₋ₓPS₅₋ₓCl₁₊ₓ x=0→0.7 에서 7.8→15.7 mS/cm (**≈2.0×↑**) | comp1→modelc **D 2.6×↑**, Ea↓ | ✅ **방향 일치, 같은 자릿수.** ⚠ **D 비와 σ 비는 다른 양**(V·T 인자) — 직접 등치 금지 |
| **우리 modelc 조성(x=0.6)** | 논문이 안 찍음. 0.5(11.8)–0.7(15.7) 보간 **≈13.7 mS/cm** `digest 계산 (원논문 미보고)` | ⛔ 우리는 σ 절대값 인용 금지 | ⛔ **참고만.** db 미등록 |
| **Br 치환** | 같은 x 에서 Cl 보다 σ 높음(x=0.7: 18.6 vs 15.7). 논문 설명 = 배열 엔트로피(*"possibly"*) | 우리 Br 계 없음 | 🔵 미탐색 축 |
| **★ O 도핑** | `Fig. S11` Li₅.₅PS₄.₅₋ₓOₓCl₁.₅: σ **단조 감소** 11.8→7.0 (x 0→0.30, **−41%**); 실험 9.5→6.0 (x 0→0.25, **−37%**) | LPSOCl 은 **전자구조(gap 2.2309 eV)가 정본**, MD 전도도는 별도 | 🔴 **경고.** **문헌은 O 도핑이 전도도에 불리하다고 말한다**(계산·실험 합치). 우리 +O/+B₂O₃ 를 "개선"으로 쓰려면 **어느 축인지 반드시 명시** — 수분/산화 안정성이지 이온전도가 아니다. `Fig. S11` 캡션이 그 트레이드오프를 그대로 씀 |
| **무질서 = 수송 on/off** | `Fig. 6b`: LPSCl 질서상 MSD 가 `≈11.5 Å²` 에서 **포화**(D→0), 무질서상만 선형(5 ns 에 `≈38 Å²`). 무질서가 `≈7.5 meV/atom` **더 안정** | 우리도 무질서 배열 사용 | ✅ **정성 일치.** ⚠ 논문은 **무질서 배열 생성법을 안 밝힌다**(`50%@4c` 라벨뿐) ⇒ **우리 처리와 정량 대조 불가** |
| **MSD 창** | **미기재** (`D = lim MSD/6t` 정의만) | **2–50 ps 고정·자유절편** | ⛔ **이 한 줄이 위 표 전체를 "추세만" 으로 제한한다** |
| **σ 산출** | Nernst–Einstein, **Haven=1**, `σ₀T^m`, m=−1 | 동일(NE, Haven=1) | ✅ 같은 관례 — 그래서 **같은 방향으로 틀릴 수 있다**(digest §13-10) |

**⛔ [Wang25DPA] 에서 축 A 로 옮기면 안 되는 것**
1. **σ·D 절대값** — 셀·궤적·시드·MSD 창 미기재.
2. *"DPA-SSE 는 실험을 정확히 재현한다"* — `Fig. 6c` 는 5계 중 4계에서 **1.6–2.8× 과대**다.
3. **LGPS 계열 값 전부** — 우리 계가 아니다.
4. `Fig. S5a` 의 개별 분해에너지 — **범례 10색 순환으로 점 특정 불가**.

---

## ③ `comparison_vs_ours.md` **§J** 에 신설할 절 — **J-11**

### J-11. ★★★ **황화물 전용 사전학습 MLIP — UMA 의 대체·committee·대조군 판정** ([Wang25DPA], 2026-09-09 신설)

> 계기: UQ 3편(Grasselli / Carrete / Kurniawan)이 공통으로 *"단일 파운데이션 모델로는 committee 를
> 못 만든다"*(Grasselli 식 27 은 **M ≥ 4**)를 짚었고, 우리 이종 committee(UMA / MACE / SevenNet)는
> **훈련 코퍼스가 달라 §2.2 "equivalent models" 전제가 깨진다**(§J-1 · [Gra25UQ]).
> **[Wang25DPA] 는 그 빈칸을 메우는가?** — 세 갈래로 나눠 판정한다.

**갈래 ①: UMA 의 대체인가** → 🔵 **조건부 후보. 단 그 판정을 이 논문이 해 주지 않는다.**

| 근거 | 내용 |
|---|---|
| ⛔ **UMA 는 이 논문에서 시험되지 않았다** | 피고는 **DPA-2-MP · MACE-MP-0a(small) · M3GNet-MP-2021.2.8 · CHGNet · ORB-v2** = **전부 MPtrj 세대**. ⇒ *"범용 MLIP 가 장벽을 1/3 로 본다"* 는 **말할 수 있고**, *"따라서 UMA 도"* 는 **말할 수 없다** |
| ✅ 커버리지는 우리 계에 유리 | `Fig. 1` 1층에 **Li₆PS₅Cl 포함** · `Fig. S10a` 가 **우리 modelc 조성계열**(x=0.6 이 0.5–0.7 사이) · `Fig. S11` 이 **우리 O 도핑계** |
| ⚠ **b2o3 는 반대다** | **B–O 결합이 41계 어디에도 없다**(B 는 B–S 만, O 는 Li₂O 만). `Fig. 4a` 는 **Li–B–S 삼원(Li₂B₂S₅)조차 zero-shot 162.65 meV/atom 로 무너짐**을 보인다 ⇒ **b2o3 에 zero-shot 으로 들이대면 UMA 보다 나쁠 공산이 크다** |
| ❌ **Nd 는 범위 밖** | 란탄족이 15원소에 없다. type map 확장 가능 여부는 이 논문 밖 |
| ⚠ **비용이 판을 지배한다** | 사전학습 원본 `≈8.6×10⁻³` s/step·atom = **MACE-ft 보다도 46× 느림**. 우리 558원자 셀 환산 **200 ps 1런 ≈5.6일 · 9런 ≈50일** (`digest 계산`, 교차 하드웨어) ⇒ **규약에 그대로 못 꽂는다.** 증류하면 **≈18.8 ns/day = 9런 ≈2.3시간**, 즉 **UMA(252 ps/day) 대비 ~75× 처리량** |

**갈래 ②: committee 네 번째 멤버인가** → ⛔ **부적격.**

| Grasselli §2.2 전제 | UMA-s-1p1(omat) | DPA-SSE | 깨지나 |
|---|---|---|---|
| 같은 아키텍처 | equivariant 계열 | **DPA-2 (attention)** | ⛔ |
| 같은 훈련 분포 | OMat24 (범용) | **황화물 전용 54,771 프레임** | ⛔ |
| **같은 참조 PES** | **PBE 계열** | **PBEsol** | ⛔⛔ **결정적** |

> **한 줄 판정**: 두 모델이 **서로 다른 참조 PES 를 향해** 학습됐으므로 **둘의 불일치는 epistemic
> uncertainty 가 아니라 PBE−PBEsol 계통 오프셋을 포함한다.** committee spread 를 오차막대로 환산하는
> 순간 그 오프셋이 "불확실도"로 둔갑한다 ⇒ **우리 이종 committee 문제가 완화되는 게 아니라 축이 하나 는다.**
> ⚠ 저자 반론(*"PBE↔PBEsol 은 moderate shift 이고 fine-tune 이 흡수"*, 근거 `Fig. 5a,b` 의 두 범함수
> NEB 경로 일치)은 **fine-tune 하는 경우에만** 유효하다. 그리고 그 근거는 **LGPS 두 경로**에서만 확인됐다.

> ✅ **그러나 합법적 길이 하나 열린다**: 훈련 데이터가 **공개**돼 있으므로(AIS Square dataset id 217,
> 54,771 프레임) **같은 데이터·같은 아키텍처로 시드만 바꿔 M ≥ 4** 를 학습하면 Grasselli 전제를
> **정확히 만족하는 committee** 다. 값싼 변형: **증류 학생 모델을 시드만 바꿔 4–8개**(교사가 라벨을
> 공짜로 찍으므로 **DFT 추가 0**). ⚠ **그 committee 가 재는 것은 "학생이 교사를 못 따라간 분산"이지
> "교사가 DFT 에서 틀린 오차"가 아니다** — 두 층을 절대 섞어 부르지 않는다.

**갈래 ③: UMA 검증의 독립 기준인가** → ✅ **최적. 이것이 이 논문의 우리에 대한 실사용처다.**

| 우리 계 | DPA-SSE 를 심판으로 | 이유 |
|---|---|---|
| **comp1 / modelc** | ✅ **적격** | Li₆PS₅Cl 은 훈련 1층, Cl-rich 는 `Fig. S10a` 로 일반화 실증 |
| **LPSOCl (O 도핑)** | ✅ **적격** | `Fig. S11` 에 직접 대응 계가 있다 |
| **+B₂O₃** | ⛔ **부적격** | **B–O 결합 미커버.** ⚠ 특히 `db/properties/b2o3_uma_vs_dft_force_prereg_2026_09_08.json`(**봉인 2026-09-08, results_seen=false**)에 DPA-SSE 를 세 번째 심판으로 넣고 싶어질 텐데 — **넣으면 안 된다.** UMA(OMat24)는 B₂O₃ 를 봤을 공산이 크고 DPA-SSE 는 확실히 못 봤으므로, 둘의 불일치가 *"누가 맞나"*가 아니라 *"누가 그 결합을 봤나"*를 잰다. **⛔ 그 봉인 카드는 어떤 경우에도 수정하지 않는다** — DPA-SSE 는 **별도 카드**로 붙인다 |
| **Nd–O** | ❌ **범위 밖** | 란탄족 없음 |

**⇒ 실행 사다리 (digest §11-4 전문)**

| 단계 | 내용 | 비용 | 전제 |
|---|---|---|---|
| **0** | AIS Square model **id 266** / dataset `Solid_State_Electrolyte` **id 217** / Bohrium 노트북 **71679486918** 접근·라이선스·**type map 에 Cl·O·B 실재** 확인 | 반나절 · 계산 0 | ⛔ 못 받으면 아래 전부 무의미 |
| **0.5** ★★ | **§J-1 의 PET-MAD Li₃PS₄ test 243구조**(`db/properties/mlip_bench_li3ps4_uma.json`, 도구 `tools/mlip/bench_against_dft.py`)에 **DPA-SSE 를 그냥 태운다**. **라벨이 PBEsol = DPA-SSE 모국어** | 몇 시간 · **DFT 0회** | ⚠ **공정한 대결 아님** — `Fig. 1` 2층에 Li₃PS₄ 로 보이는 항목이 있어 **DPA-SSE 에겐 훈련 근처, UMA 에겐 외부**. *"훈련셋 안이면 얼마나 좋은가"* 를 잴 뿐. ⛔ **§J-1 의 30.0 과 논문의 30.28 을 나란히 놓지 마라 — test set 이 완전히 다르다** |
| **1** | 우리 궤적 스냅샷에 UMA·DPA-SSE 단일점. **표본 규칙은 b2o3 봉인 카드 §4 의 결정적 규칙 재사용**(700 K, s2·s3, 2–50 ps 창 등간격 5프레임). 보고량은 **절대 \|ΔF\| 가 아니라 비** | 하루 | ⛔ **b2o3 제외.** ⛔ **봉인 카드 수정 금지 — 새 카드로** |
| **2** | Step 1 에서 가장 갈린 **20–40 프레임에 PBE·PBEsol 단일점을 둘 다** | 1–2일 (kgy CPU) | 이게 없으면 **PBEsol 모델을 PBE 자로 재는 것** |
| **3** | ① `Fig. 5a,b` 형식 **NEB 3자 대결**(UMA · DPA-SSE · 우리 DFT) → *UMA 가 base 무리(1/3 장벽)인가* 한 장 판정 ② `Fig. S3` 형식 **500 K NVE 100 ps 드리프트** → **우리 UMA 가 보존형 힘을 쓰는가** | 2–3일 | ★ ②는 **지금 당장 할 수 있는 최저비용·최고가치**. Langevin NVT 는 비보존성을 **가려 준다** |
| **4** | 증류 → 우리 규약 재실행 | 1–2주 | ⚠ **두 개의 σ·Ea 가 생긴다.** `comparison_group` 과 정본 규율을 **결과 보기 전에** 정한다 |
| **5** | 시드만 바꾼 학생 M ≥ 4 = 합법 committee | 선택 | ⚠ 증류 분산 ≠ 모델 오차, 카드에 먼저 명시 |

**🔴 [Wang25DPA] 가 §J-1 에 주는 직접 소득**
> §J-1 의 명시적 한계 **#3 — *"Cl 이 없다 … 아르지로다이트·Cl 무질서로의 전이를 이 벤치가 보증하지
> 않는다"*** 를 이 논문이 **정면으로 메운다**: Li₆PS₅Cl/Br/I 가 훈련 1층이고, **Cl-rich 시리즈**(`Fig. S10a`)와
> **O 도핑 시리즈**(`Fig. S11`)까지 시험됐다. ⚠ 단 *"Cl 이 있다"* 와 *"Cl 이 충분하다"* 는 다르다 —
> `Fig. 1` heatmap 의 **Cl 칸이 옅고**, `Fig. S1` 에서 **LPSCl 만 두 개의 이상 신호**를 낸다(§13-3).

**⛔ 이 축에서 인용하면 안 되는 것**
1. *"이 논문이 UMA 를 시험해서 나쁘게 나왔다"* — **UMA 는 시험 대상이 아니다.**
2. `Fig. 7` 의 속도값을 **우리 하드웨어 약속으로** 쓰는 것 — V100+12코어 vs A6000, **자릿수 판정용**.
3. 논문 σ·D 를 **우리 db 절대값과 같은 표에** 놓는 것 — MSD 창·시드·셀 미기재.
4. *"DPA-SSE 가 UMA 보다 정확하다"* — **아무도 그 비교를 하지 않았다.** Step 0.5–3 이 그 시험이다.
5. `Fig. S2` 를 *"호핑 장벽 에너지 과소평가의 증거"* 로 — **eV/atom 축이라 장벽 스케일을 못 담는다.**
   그 증거는 **`Fig. 5a,b`** 다.

---

## ④ 병합자에게 남기는 메모

- **PDF 를 `litdb/inbox/` 로 옮기지 못했다**(쓰기 범위 제한). 원본 두 개:
  - 본문 `/root/.claude/uploads/82ea256b-12bc-5a75-994e-7718d79c71ba/dc978d7f-90._A_pretrained_deep_potential_model_for_sulfide_solid_electrolytes_with_broad_coverage_and_high_accuracy.pdf`
  - SI `/root/.claude/uploads/82ea256b-12bc-5a75-994e-7718d79c71ba/ad74839f-90._Sup_A_pretrained_deep_potential_model_for_sulfide_solid_electrolytes_with_broad_coverage_and_high_accuracy.pdf`
  → 나중에 그림 재추출을 하려면 `litdb/inbox/` 에 넣고 `pdf_map.tsv` 에 등록해야 한다.
  (`litdb/figures/_sources.json` 에는 업로드 경로 기준으로 이미 색인됐다.)
- **`litdb/figures/wang2025_pretrained_deep_potential_sulfide_sse/` 는 만들었다** (PNG 19장 + `figures.json`).
  `fig_S4.png`·`fig_S11.png` 은 자동 크로퍼가 *"거의 백지"* 로 **오탐 제외**한 것을 **SI 해당 쪽 전면 렌더**로
  되살린 것이라 `figures.json` 항목에 `note` 로 표시해 뒀다. ⚠ **`fig_S11.png` 은 SI 8쪽 전체**라
  **`Fig. S10` 도 같이 들어 있다**(webapp 이 S11 을 띄우면 S10 이 위에 보인다).
- **`litdb/talks/*.md` 는 건드리지 않았다.** `grep -l "논문 에이전트 인입 대기열"` → `lee2026_skku_mlip_materials_design.md`
  한 건이고, 그 §99-10 대기열(1·2·3a·3b·3b′·3c·3c′·4·5·6·7·8·9)에 **이 논문은 없다** ⇒ **양방향 링크 의무 없음.**
- **`db/` 는 건드리지 않았다.** 다만 위 §J-11 이 **봉인 카드
  `db/properties/b2o3_uma_vs_dft_force_prereg_2026_09_08.json`(results_seen=false)** 를 참조한다 —
  ⛔ **그 카드는 수정 대상이 아니고**, DPA-SSE 확장은 **별도 카드**로 만들어야 한다.
- **`properties/` 하위 문서 갱신 없음** — 이 논문의 σ·D 는 전부 소환값이고 MSD 창 미기재로
  우리 레지스트리에 넣을 수 없다.
