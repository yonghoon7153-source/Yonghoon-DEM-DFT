# ⏳ pending — `tompa2026_finetuning_mlip_foundation_strategies` 의 INDEX / comparison 반영분
> ✅ **①②③ 병합 완료 2026-09-13** (조율 세션) — INDEX.md: ① 병합됨 · comparison_vs_ours.md: ② → J-0 · ③ → J-7. ⏳ **남은 것**: ④ 정정 후보 · ⑤.

> 2026-09-09, litdb-curator. **동시작업 충돌 회피**로 `INDEX.md` · `comparison_vs_ours.md` 를 직접 안 고쳤다.
> 아래 블록을 **사람이(또는 조율 담당 세션이) 그대로 옮겨 붙이면 된다.**
> digest 본체: `litdb/papers/tompa2026_finetuning_mlip_foundation_strategies.md`
> 그림: `litdb/figures/tompa2026_finetuning_mlip_foundation_strategies/` (**29장** = 자동 28 + **수동복구 `fig_7.png` 1장**)

---

## ① `litdb/INDEX.md` — **`## ✅ Digest 완료 (paper-level)`** 표에 추가할 행

```markdown
| `papers/tompa2026_finetuning_mlip_foundation_strategies.md` | **[외부·methods·★MLIP fine-tuning 전략 벤치마크 · 🔴arXiv preprint(동료심사 전)]** **T. L. Tompa**†, **E. Varga-Umbrich**†(Cambridge Eng.), **I. Batatia**(Cambridge · **MACE 제1저자**), **A. M. Elena**(STFC Daresbury), **N. Bernstein**(US NRL), **G. Csányi\***(Cambridge), "**Fine-tuning MLIP foundation models: strategies for accuracy and transferability**" (**arXiv:2606.12704v1** [physics.chem-ph], **2026-06-10** · DOI 미발급 · 본문 20 pp + refs 3 + Appendix A–H 14 = **37 pp** · **별도 SI 없음** · Fig 1–20 · Table 1–9 · 코드 `github.com/ACEsuit/mace` **MACE ≥3.15 에 이미 머지** · 데이터 `huggingface.co/datasets/ev-tlt/MACE_finetuning_supplementary` · 이해상충: Csányi = Symmetric Group LLP 파트너 + Ångström AI 지분, **본인 신고**) — **파운데이션 MLIP 를 fine-tune 하는 7전략의 체계적 벤치마크. 물성값 0건**(`conductivity`·`diffusion`·`activation energy`·`band gap`·`elastic` **전문 0회**; MD 는 돌리지만 **안정성·RDF 만** 보고 수송계수를 안 뽑는다). **질문**: *"파운데이션 MLIP 를 언제·어떻게 fine-tune 해야 하나."* **답**: **전략 선택보다 ①파운데이션 품질 ②E₀ 일관성 ③안정적 최적화가 먼저이고 그 영향이 더 크다**; 그 뒤엔 **좁은 표적=naive, 넓은 배치=multihead replay**. **7전략**: ①**naive**(전 파라미터, lr 1e-3/EMA 0.999) ②**Freeze**(readout만 / embed+1st MP, ~5%) ③**LoRA** r=4/16/64(**등변 linear 에 irrep 블록별 `W_l+B_lA_l`** → 등변성 보존, ~2.5/10/30%, lr **1e-2**) ④**multihead replay**(몸통 공유 + target/replay 두 head, **head 별 E₀**, lr **1e-4**/EMA **0.9999**) ⑤**pseudolabel replay**(replay 라벨=파운데이션 자신의 예측 → **원 사전학습 데이터 불필요**) ⑥**MH+LoRA**(⛔ 대체로 과규제, **예외: Sɴ2 5구성 극단희소**) ⑦from-scratch(기준). ⛔ **weight decay=0 필수**(0 쪽으로 당겨 파운데이션 해에서 멀어짐) · ⛔ **2단계 손실 스케줄 금지**(`Fig. 12` epoch 500 전환에서 급등). **★★ 우리 계가 벤치마크 #1 이다**: **Li₆PS₅Cl 500 PBE 구성 단일조성**으로 fine-tune → **130+ 다른 argyrodite 조성 + 비-argyrodite Li 전해질**(개수·조성 미기재)로 OOD 평가, replay = **MPTraj 무작위 10,000 + OMat24 pseudolabel** (`Table 6`). §2.1 이 *"LPSC 는 OMat24 에 흔한 종류라 이 계만으로는 방법 간 구분이 어려울 것"* 이라고 **명시** ⇒ **우리 계 = 이 논문의 "가장 쉬운 쪽 끝"**. **🔑 LPSC 정량 (`Table 9`, lr 스윕)**: target head **E 0.5 meV/atom · F 18.4 meV/Å**, replay head 6.1/23.9 — 그런데 **lr 1e-3 으로 올리면 target F 는 18.1 로 그대로인데 replay F 가 217.6 (9배 붕괴)** ⇒ *"breadth-maintenance 는 표적이 이상 징후를 보이기 훨씬 전에 이미 깨진다"* = **표적 지표만 보면 replay 죽은 걸 모른다**. **🔴🔴 우리 최대 소득 — "fine-tune 하면 기존 결과와 비교가 끊긴다"의 정량 (`Fig. 7b`·`Fig. 17`, `figure-read ≈`)**: OMat 파운데이션 **비-argyrodite F MAE ≈0.045 → naive ≈0.075 eV/Å (1.7배 악화, 꼬리 0.08→0.24)** / **pseudolabel ≈0.042 (유지)**; 약한 MP0 파운데이션이면 **≈0.08 → naive ≈0.28 · LoRA ≈0.30(꼬리 1.78)**. 반면 **얻는 것은 작다** — 다른 argyrodite F MAE ≈0.043→≈0.030(**30%**), E MAE ≈1.8→≈1.6 meV/atom(**거의 0**). **★ `Fig. 17` 헤드라인**: **fine-tune 안 한 OMat 파운데이션(≈0.043)이 MP0 를 최선으로 fine-tune 한 것(≈0.072)보다 낫다** ⇒ *"파운데이션 교체 3배 > 전략 선택 25%"*. **★★ catastrophic forgetting (`Fig. 10a`, SPICE 1구성/분자, 파운데이션 대비 배율 `figure-read ≈`)**: scratch **≈7×10³** · **naive ≈4×10³** · LoRA r=4 ≈2×10² · r=16 ≈3×10² · **r=64 ≈4×10¹** · **multihead ≈1.0** · **pseudolabel ≈1.3** · PS+LoRA ≈4. ⚠ **절대값 인용 금지** — `Fig. 10a` 는 meV/Å, `Fig. 10b` 는 eV/Å 로 **축 단위가 1000배 어긋난다**(§10-1, preprint 오기 의심) ⇒ **비율만**. 저자 명시: *"forgetting 과 in-domain 성능은 대체로 **분리**된다"*(SPICE 기준 — replay 가 표적정확도를 안 깎는다). 단 **ice trained-phase 에서는 대가가 있다**(`Fig. 7a` naive E ≈0.038 vs multihead ≈0.207 meV/atom = **5.4배**, 힘은 0.0020 vs 0.0031 = 1.55배). **★★ E₀ 초기화가 전략 차이를 넘어선다**: averaged E₀ 는 reestimated 대비 **force RMSE 2–3배** 악화(LPSC `Fig. 4a` ≈0.040→≈0.075 eV/Å); `Table 1` — **ice Ih 25구성, averaged E₀ 면 naive/LoRA/multihead 가 전부 100 K 50 ps 내 붕괴, reestimated 면 전부 250 ps 완주 + 50→800 K 램프 안정** ⇒ ***"검증 RMSE 는 멀쩡한데 MD 가 터진다"의 실측 사례*** (= 우리 b₂o₃ creep 과 같은 계열의 실패). `Table 2`: 전자 전량 SPICE E₀ 를 **학습 없이** 복원 — 평균법 MAE **3.13 eV** vs **model-aware reestimation 0.33 eV**(우리 원소: **S −2.409 vs +0.351** · **Cl −1.681 vs +0.163**). 🔴 **LPSCl 단일조성 fine-tune 이면 averaging 은 애초에 rank-deficient** 라 원소별 E₀ 가 유일하지 않다(최소노름 해만). **★★ RSS PES-hole (`Fig. 11`, 인쇄된 숫자 — 판독 아님)**: PyXtal 10조성×50구조=**500구조**, **relax–rattle 3회**, 4기준(원자겹침 <0.5×공유반경합 / 부피 <30% 중앙값 / 에너지 <중앙값−10 MAD 또는 −5 eV/atom / 복합). 파운데이션 baseline **0.1 GPa 8.6% · 50 GPa 10.0%**. **replay 없는 방법은 데이터를 늘릴수록 구멍이 는다** — naive 50 GPa **9.4→34.4%**, LoRA 50 GPa **7.8→57.4%**, scratch 최대 **87.0%**, ⚠**Freeze(5) 최악 85.2%**; **multihead/pseudolabel 은 전 조건 파운데이션 이하**(pseudolabel 최저 **2.6%**). 저자: *"in-domain 정확도가 좋아지는 **와중에도** 구멍이 는다"*. ★ **모든 모델에 ZBL pair repulsion 이 명시적으로 들어 있는데도** 구멍이 생긴다 ⇒ **학습된 many-body 반발 기여의 붕괴**. **replay 조성은 상관없다** (`Fig. 15`·Appendix E): 원소일치 OMat24 / 무작위 MPTraj 10k / 결합 **셋 다 동일**, 라벨도 pseudolabel 로 충분 ⇒ **🔑 OMat24 원본 데이터 없이도 replay 가 된다**. **비용**: multihead = naive 대비 **학습 compute 3–15배**(데이터 2배 + lr 10배 낮춰 수렴 느림). **필요 라벨수**: LPSC **500** · ice MD안정 **25** · NaCl RDF **96(10%)에서 포화** · Sɴ2 **60**(5구성은 MH+LoRA만) · SPICE 19,687~855,905. ⛔ **한계(저자 4+1)**: ①**전 실험이 MACE 아키텍처 — 타 아키텍처 일반화 미검증** ②하이퍼파라미터 탐색 제한(특히 LoRA 어댑터 위치·replay:target 비율) ③**RSS 는 단거리 반발벽만 — "경쟁 상 상대안정성이 틀리는" PES artefact 는 다른 진단 필요** ④파운데이션이 주기 무기물 편중 ⑤**최적 replay 조성은 미해결(향후 과제)**. ⛔ **한계(우리 지적)**: 🔴**동료심사 전 preprint** · **`Fig. 10` 축 단위 1000배 불일치** · **`Table 4`·`Fig. 11` 의 "Freeze (5)/(6)" 이 §2.3 의 두 정의와 매핑되지 않음**(그리고 한쪽은 최악 +40.8%p 인데 본문은 "readout-only 는 보존" — **어느 쪽인지 알 수 없다**) · **LPSC RSS 는 "했다"고 서술만 있고 그림 없음**(Fig 11·16 은 NaCl 뿐) · **시드 반복이 aq. NaCl 뿐**(Sɴ2 는 명시적 *"single run"*, **LPSC·ice·SPICE 오차막대 0**) · **LPSC 500구성의 샘플링·온도·Cl/S 부분점유 처리 전부 미기재** · **비-argyrodite 평가셋의 N·조성 미기재**(우리가 제일 무겁게 쓰는 숫자가 거기서 나온다) · **GPU시간·epoch수·batch 크기 어디에도 없음**(compute 보고 = "3–15배" 한 줄) · scratch 기준선만 Agnesi transform 을 끔(아키텍처가 달라진 것). **🔧 우리 좌표**: 우리는 **UMA-s-1p1(omat) 고정 체크포인트** = `Fig. 17` 의 **`OMat (found.)` 회색 violin 자리** ⇒ **이 논문 권고 #1("가장 강한 파운데이션에서 출발")을 이미 충족**. **판정 — UMA fine-tune 은 라벨(500점)·하드웨어(논문의 Li 계도 A100 1장) 관점에선 현실적이나 지금 우선순위 아님**: 이득이 제일 작은 자리(우리 계 = OMat24 핵심영역)인데 비용(비-argyrodite 1.7배 악화)은 **+B₂O₃·Nd–O 방향**으로 걸린다; 게다가 **LoRA·pseudolabel replay·E₀ reestimation 은 `ACEsuit/mace` 3.15+ 전용**이고 **fairchem 대응물 미확인**, 저자가 *"전 실험 MACE"* 라고 못박음 ⇒ **더 방어 가능한 경로 = "UMA 그대로 쓰고, fine-tune 이 필요하면 MACE-OMat 으로 갈아탄다"**. **★★★ snapshot ensemble (M≥4) 질문에 대한 답**: ⛔ **이 논문은 snapshot ensemble·UQ·앙상블을 다루지 않는다**(`snapshot` 0 · `uncertainty` 0 · `ensemble` = NEB 뿐 · `committee` = 참고문헌 [11] 제목만) — 체크포인트 저장 정책·권장 간격·멤버 수 **전부 없음**. 우리가 유도할 수 있는 것: 학습길이 **수백~1000 epoch**(`Fig. 12` 2단계 전환이 epoch 500) ⇒ 100-epoch 간격이면 **5–10 멤버**; **aq. NaCl 에서 seed 1–3 이 실제로 돌아갔다**(`Table 4` 42.44±5.28 / 43.79±5.03 / 41.54±4.76 = std ≈ 평균의 10–12%) ⇒ **시드 다중 fine-tune 이 M≥4 의 가장 방어 가능한 경로**. 🔴🔴 **그러나 새 긴장 발견(우리 논증, 논문 주장 아님)**: **`Table 7` 의 EMA decay 0.999(naive)/0.9999(multihead) 가 snapshot 다양성을 정면으로 지운다** — EMA 0.9999 는 최근 ~10⁴ 스텝 평균이라 스냅샷들이 서로 거의 같아진다(유효 M→1). 그런데 논문은 **EMA 를 올리는 것이 안정적 naive fine-tuning 에 필수**라고 한다 ⇒ **"정확도를 위한 설정"과 "UQ 를 위한 설정"이 충돌**한다. 회피: raw(비-EMA) 가중치 별도 저장 / EMA 낮춤 / **시드 독립학습**. **🔑 fine-tune 없이 지금 당장 가져올 것 4가지**: ①**RSS PES-hole 진단(DFT 0회)을 UMA·우리 조성에 그대로 실행** — b₂o₃ 마감의 사후진단 가능(⚠ 보고량 카드 먼저) ②**MD 안정성 표준(250 ps 완주 + 50→800 K 램프 50 ps)** — 우리 MSD 창 2–50 ps 보다 긴 완주시험 ③**`Fig. 3a` 로 우리 이종 committee σ 재해석** — OMat24계열 vs MPTraj계열이 우리 계에서 **힘 MAE ≈2–3배 차이**(≈0.045 vs ≈0.105) ⇒ **우리 σ 의 상당부분이 epistemic 이 아니라 사전학습셋 계통차** ④**`mlip_bench_li3ps4_uma.json` 의 선형 원소보정(Li 0.09312/P 0.03104/S 0.12416 eV/atom, fit R²=0.620)이 바로 이 논문이 "쓰지 말라"는 averaging 방식** ⇒ **식 (6) model-aware reestimation 으로 교체 가능**(아키텍처 무관 — **이 논문에서 UMA 에 즉시 이식 가능한 유일한 수식**). ⛔ **물성 4축(A/B/C/D) 편입 금지** — σ·ESW·탄성·gap **0건** → `comparison_vs_ours.md` **`🔧 방법 원전`** 에만. ⛔ **LPSC F RMSE 18.4 meV/Å(MACE·PBE·LPSCl)를 우리 UMA Li₃PS₄ 30.0 meV/Å MAE / 44.6 RMSE(UMA·PET-MAD 라벨·**Cl 없음**)와 같은 표에 놓지 말 것** — 모델·계·라벨·평가셋이 전부 다르다. **"자릿수가 같다"까지만** | **방법론(MLIP fine-tuning 전략)·T1(모델 불확실도 축의 출구)** — 물성값 0, **우리 계 LPSCl 이 벤치마크 #1** |
```

**⚠ INDEX 행에 같이 반영할 것**
- 같은 날 인입된 UQ 3편(`grasselli2025_…` · `imbalzano2021_…` · `kurniawan2025_…`)과 **상호 참조**를 건다:
  · `kurniawan` 행 → *"snapshot ensemble 의 재료(= fine-tune 체크포인트)를 어떻게 만드나 → **`tompa2026_…`**.
    단 그 논문은 snapshot 을 다루지 않고, **EMA 설정이 오히려 방해**한다(tompa digest §12-F)"*
  · `grasselli` 행 → *"M≥4 를 채우는 실무 경로 후보 = **시드 다중 fine-tune**(`tompa2026_…` `Table 4` 가 3-시드 비용감각을 준다).
    ⚠ 시드만 다른 fine-tune 이 식 (27) 의 독립추출 조건을 만족하는지는 **어느 논문도 판정하지 않았다**"*
- **`tompa2026_…` 행 자체에 preprint 표지를 남긴다**: `🔴 arXiv preprint — 동료심사 전, 게재본에서 수치 변경 가능`.

---

## ② `litdb/comparison_vs_ours.md` — **§J-0 출처표** 에 추가할 줄

```markdown
| **[Tompa26FT]** 🔧 | `tompa2026_finetuning_mlip_foundation_strategies` — **MLIP 파운데이션 fine-tuning 전략 벤치마크** (**arXiv:2606.12704v1**, 2026-06-10, **동료심사 전**). Tompa/Varga-Umbrich/**Batatia**/Elena/Bernstein/**Csányi** = **MACE 그룹 본인**, 구현이 `mace ≥3.15` 에 머지됨. ⚠ **물성값 0**(σ·Ea·ESW·탄성·gap 전무) → 아래 **J-7** 에만 등장, A–D 축 금지. ★ **벤치마크 5계 중 #1 이 Li₆PS₅Cl** — 우리 계로 직접 잰 수치가 있는 드문 방법론 편 |
```

---

## ③ `litdb/comparison_vs_ours.md` — **§J-7 `🔧 방법 원전`** 에 추가할 블록

```markdown
**[Tompa26FT] `tompa2026_finetuning_mlip_foundation_strategies` — *파운데이션 MLIP 를 어떻게 fine-tune 하는가* 의 원전**
(**arXiv 2606.12704v1** · 2026-06-10 · **preprint, 동료심사 전** · Cambridge MACE 그룹 + STFC + US NRL · **물성값 0**)

> 🔑 **우리가 이 편에서 가져오는 것은 값이 아니라 "레시피와 그 대가"다.**
> 그리고 **벤치마크 5계 중 첫 번째가 Li₆PS₅Cl** 이라서, 드물게 **우리 계로 직접 잰 방법론 수치**가 있다.
> ⚠ 다만 §2.1 이 *"LPSC 는 OMat24 에 흔한 종류라 이 계만으로는 방법 간 구분이 어려울 것"* 이라고 **미리 못박는다**
> — **우리 계는 이 논문에서 "차이가 제일 안 보이는 자리"** 다.

| 항목 | [Tompa26FT] | 우리 (UMA-s-1p1 omat, 고정 체크포인트) | 판정 |
|---|---|---|---|
| **엔진** | MACE (등변 MPNN), 4.7–9.1 M 파라미터 | **UMA-s-1p1**, fairchem | ⚠ **아키텍처가 다르다.** 저자 명시: *"모든 실험이 MACE … 타 아키텍처 일반화는 미검증"* ⇒ **결론 직수입 금지** |
| **사전학습 도메인** | **OMat24**(주) vs MPTraj(비교군) | **OMat24 계열**(omat task) | ⭕⭕ **우리가 좋은 쪽에 있다.** `Fig. 3a`: 우리 계에서 MPTraj계 F MAE ≈0.105 vs OMat계 ≈0.045 eV/Å (`figure-read ≈`, **2–3배**) |
| **fine-tune 여부** | 7전략 비교 | **0회** | 🔴 우리는 `Fig. 17` 의 **`OMat (found.)` 회색 violin** 자리. **이 논문 권고 #1 을 이미 충족** |
| **fine-tune 의 이득 (우리 계)** | argyrodite OOD **F MAE ≈0.043 → ≈0.030 (30%)** · **E MAE ≈1.8 → ≈1.6 meV/atom (거의 0)** | — | 🔴 **이득이 작다.** 500 PBE 점을 써서 30% |
| **fine-tune 의 대가 (우리 계)** | **비-argyrodite F MAE ≈0.045 → naive ≈0.075 (1.7배 악화), 꼬리 0.08→0.24** | 우리 **+B₂O₃ · Nd–O** 가 그 방향 | 🔴🔴 **"기존 결과와 비교가 끊긴다"의 정량.** ⇒ **plain LPSCl 로만 fine-tune 하면 도핑계가 나빠질 수 있다** |
| 그 대가를 없애는 법 | **pseudolabel replay** → 비-argyrodite ≈0.042 로 **파운데이션 수준 유지** | — | ⭕ **replay 면 끊김 ≈0.** 비용 = 학습 compute **3–15배** |
| **replay 데이터 조달** | `Fig. 15`·Appendix E: **원소일치 OMat24 / 무작위 MPTraj 10k / 결합 = 전부 동일**, 라벨은 파운데이션이 자체 생성 | OMat24 원본 미보유 | ⭕⭕ **원 사전학습 데이터 없이 된다.** 우리에게 결정적 |
| **필요 라벨 수** | **LPSC 500(PBE, 단일조성)** · ice MD안정 **25** · NaCl RDF **96 에서 포화** · Sɴ2 **60** | `mlip_bench_li3ps4_uma.json` = **243 구조** (⚠ `elements: [Li,P,S]` — **Cl 없음**) | 🟡 **자릿수가 같다.** 단 **Cl 포함 라벨을 새로 만들어야** 한다 (새 계산 ⇒ **보고량 카드 먼저**) |
| **E₀ (원자기준에너지)** | **model-aware reestimation** (식 6) 필수. **averaging 금지** — force RMSE 2–3배 악화, 게다가 **단일조성이면 rank-deficient** | `mlip_bench_li3ps4_uma.json` 이 **선형 원소보정**(Li 0.09312 / P 0.03104 / S 0.12416 eV/atom, **fit R² 0.620**) 사용 = **바로 그 averaging** | 🔴 **우리가 지금 쓰는 방식이 이 논문이 금지한 것.** ⭕ **식 (6)은 아키텍처 무관 ⇒ UMA 에 즉시 이식 가능** — **이 논문에서 우리가 바로 쓸 수 있는 유일한 수식** |
| **MD 안정성 판정** | ①정온 **250 ps** 완주 ②**50→800 K 램프 50 ps** (`Table 1`) | MSD 창 **2–50 ps**, 600/800/1000 K | ⭕⭕ **우리보다 훨씬 긴 완주시험.** `Table 1` 은 *"검증 RMSE 정상 + MD 붕괴"* 를 E₀ 하나로 만들어낸 사례 ⇒ **b₂o₃ creep 과 같은 계열** |
| **PES 병리 진단 (RSS)** | PyXtal 10조성×50 = **500구조**, relax–rattle **3회**, 4기준. 파운데이션 **0.1 GPa 8.6% · 50 GPa 10.0%** | ⛔ **없다** | ⭕⭕⭕ **DFT 0회로 지금 실행 가능한 최우선 이식 항목** |
| **"더 학습하면 더 낫다"** | ⛔ **틀린다.** replay 없는 방법은 **데이터↑ 이면 PES hole↑** (naive 50 GPa 9.4→34.4%, LoRA 7.8→**57.4%**) — **in-domain 정확도는 개선되는 와중에** | — | 🔴 **우리 직관과 반대. 규율로 박을 것** |
| **ZBL pair repulsion** | **전 모델에 명시적으로 들어 있는데도** 구멍 발생 ⇒ **many-body 반발 기여의 붕괴** | — | ⚠ *"단거리 항 넣었으니 안전"* 이 성립 안 함 |
| **UQ / 앙상블** | ⛔ **전혀 없다** (`snapshot` 0 · `uncertainty` 0 · `committee` = 참고문헌 제목만) | 이종 committee **M=3** | 🔴 **이 편은 UQ 논문이 아니다.** M≥4 경로는 우리가 **유도**한 것 (아래) |
| **수송계수(D·Ea·σ)** | ⛔ **없다.** MD 를 돌리지만 안정성·RDF 만 | 우리 보고량 본체 | 🔴 **층위가 다르다** → `imbalzano2021_…` 가 그 층위 정본 |

**🔗 UQ 3편과의 접속 — 우리가 유도한 것 (논문 주장 아님)**

| 물음 | [Tompa26FT] 가 주는 것 | 판정 |
|---|---|---|
| **M≥4 를 채울 재료가 생기나** | 🟡 **간접**. 학습이 **수백~1000 epoch**(`Fig. 12` 2단계 전환 = epoch 500) ⇒ 100-epoch 간격이면 5–10 스냅샷. **aq. NaCl 에서 seed 1–3 이 실제로 돌아갔다**(`Table 4`) | **시드 다중 fine-tune 이 가장 방어 가능** |
| 시드 산포는 얼마인가 | `Table 4` NaCl F RMSE: **42.44±5.28 / 43.79±5.03 / 41.54±4.76 meV/Å** ⇒ **std ≈ 평균의 10–12%** | ⚠ 이건 **재현성 산포**이지 UQ 용 σ 가 아니다 |
| 🔴 **방해 요소는 없나** | **있다 — EMA.** `Table 7` EMA decay **0.999(naive) / 0.9999(multihead)**. 0.9999 ≈ 최근 10⁴ 스텝 평균 ⇒ **스냅샷들이 서로 거의 같아진다(유효 M→1)**. 그런데 논문은 **EMA 를 올리는 것이 안정적 fine-tuning 에 필수**라고 한다 | 🔴🔴 **"정확도용 설정"과 "UQ용 설정"이 충돌한다.** 이 긴장은 **tompa 에도 UQ 3편에도 없다 — 우리가 새로 세운 것** |
| Grasselli 식 (27) 의 독립추출 조건을 만족하나 | ⛔ **어느 논문도 판정 안 함** | 🔴 **열린 질문으로 남긴다** |

**🔴 이 편이 닫지 못하는 것 — 반드시 같이 인용**
1. 🔴 **동료심사 안 됐다** (arXiv v1). 게재본에서 수치·그림이 바뀔 수 있다.
2. 🔴 **전 실험이 MACE 다.** 저자 스스로 한계로 적음 ⇒ **UMA 이전성 미검증**.
   그리고 **LoRA·pseudolabel replay·E₀ reestimation 의 구현은 `ACEsuit/mace` 3.15+ 전용**,
   **fairchem 대응물은 이 세션에서 확인 못 했다.**
3. 🔴 **`Fig. 10` 의 축 단위가 패널 간 1000배 어긋난다**(a: meV/Å · b: eV/Å, 두 값 모두 알려진 MACE-OMat
   힘오차와 안 맞음) ⇒ **forgetting 은 "파운데이션 대비 배율"로만 인용**.
4. 🔴 **`Freeze (5)`/`Freeze (6)` 라벨이 §2.3 의 두 정의와 매핑되지 않는다.** 한쪽은 `Fig. 11` 최악(+40.8%p)인데
   본문은 *"readout-only 는 반발벽을 보존한다"* 고 쓴다 ⇒ **Freeze 계열은 이 논문으로 선택할 수 없다.**
5. 🔴 **우리 계(LPSC)의 RSS hole% 가 없다.** *"LPSC 에도 적용했다"* 는 서술만 있고 `Fig. 11`·`Fig. 16` 은 **NaCl 뿐**.
6. 🔴 **오차막대가 aq. NaCl 에만 있다.** Sɴ2 는 명시적 *"single run"*, **LPSC·ice·SPICE 는 시드 반복 0**
   ⇒ `Fig. 7b` 의 "naive ≈0.075 vs pseudolabel ≈0.042" 가 시드 노이즈보다 큰지 **논문이 보증하지 않는다**
   (violin 은 *평가구조 간* 산포이지 *시드 간* 산포가 아니다).
7. 🔴 **LPSC 500 구성의 샘플링·온도·Cl/S 부분점유 처리가 전부 미기재.** 우리 계의 본질적 자유도(무질서)가 통째로 빠짐.
8. 🔴 **비-argyrodite 평가셋의 N·조성 미기재** — 우리가 제일 무겁게 쓰는 숫자가 거기서 나온다.
9. 🔴 **GPU 시간·epoch 수·batch 크기 어디에도 없다.** compute 보고 = *"multihead 는 naive 대비 3–15배"* 한 줄.
   ⇒ **"UMA fine-tune 에 몇 시간 드나"에 이 논문은 답하지 않는다.**
   유추 가능한 것 하나: *"Li 모델은 **NVIDIA A100** 에서 학습"*(나머지는 GH200/MI300A) = **A100 1장 규모**.
10. **RSS 는 단거리 반발벽만 본다.** 저자 명시 — *"경쟁 상들의 상대안정성이 틀리는 종류의 PES artefact 는
    다른 진단이 필요하다."* 🔴 **우리 b₂o₃ 골격 creep 은 오히려 그쪽에 가깝다** ⇒ `Fig. 11` 이 우리 creep 을
    예측한다고 쓰면 안 된다.

**⛔ 이 축에서 인용하면 안 되는 것 (→ §J-6 에도 추가)**
- ⛔ *"이 논문이 fine-tuning 이 이온전도도/확산장벽 예측을 개선한다고 보였다"* — **σ·D·Ea 를 한 번도 계산하지 않는다.**
- ⛔ *"이 논문이 snapshot ensemble / UQ 를 다뤘다"* — **한 번도 안 다룬다.** 우리 §12-F 는 **유도**다.
- ⛔ *"naive fine-tuning 은 catastrophic forgetting 을 일으키지 않는다"* — **정반대다.**
  논문의 주장은 *"초기 실패의 원인이 naive 의 본질적 결함이 아니라 약한 파운데이션·잘못된 E₀·불안정 학습이었다"* 이고,
  **SPICE forgetting 은 naive 가 여전히 ≈4×10³ 배로 최악**이다.
- ⛔ **`Fig. 10` 의 절대 force RMSE 값** (축 단위 불일치 — 위 3번).
- ⛔ **LPSC F RMSE 18.4 meV/Å**(MACE-OMat-0-medium · PBE · Li₆PS₅Cl · fine-tune 후)를
  **우리 UMA Li₃PS₄ F MAE 30.0 / RMSE 44.6 meV/Å**(UMA-s-1p1 · PET-MAD 라벨 · **Cl 없음** · zero-shot)와
  같은 표에 놓는 것 — **모델·계·라벨·평가셋이 전부 다르다.** *"자릿수가 같다"* 까지만.
- ⛔ **`figure-read ≈` 값을 본문 명시값처럼 쓰는 것.** `Fig. 3a`·`Fig. 4a`·`Fig. 7b`·`Fig. 17`·`Fig. 10` 의 숫자는
  **전부 violin 중앙부 판독**이고 본문에 숫자가 없다(순위·정성 서술만). **±10–20% 오차 가정.**
  **인쇄된 숫자는 `Fig. 11` 과 `Table 1–9` 뿐이다.**
```

---

## ④ 🎤 talk 역링크 — **해당 없음** (단, 주제 인접 + **정정 후보** 기록)

`grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `talks/lee2026_skku_mlip_materials_design.md` 하나.
그 §99-10 대기열(#1–9)을 확인했고 **이 논문은 대기열에 없다.** ⇒ **talk 파일을 건드리지 않았다.**

> 🔴 **다만 조율 담당이 판단할 정정 후보가 하나 생겼다** (그 talk 은 `citable=no` — 방향은 논문 → talk 뿐):
> 덱 **슬 8 "MLIP PES softening → fine-tuning"** 의 명제 —
> *"DFT PES → uMLIP PES 로 갈 때 softening 이 일어나고, **fine-tuning 으로 되돌린다**"* —
> 를 이 논문이 **부분적으로 뒤집는다**: `Fig. 11` 은 **replay 없이 fine-tune 하면 데이터를 늘릴수록
> 고에너지·단거리 영역이 오히려 더 망가진다**고 보여준다 (naive 50 GPa hole 9.4→34.4%, LoRA 7.8→57.4%,
> **in-domain 정확도가 개선되는 와중에**).
> ⇒ 덱의 *"fine-tuning 으로 되돌린다"* 는 **replay(multihead)를 붙였을 때만** 성립한다.
> 그 talk 의 §99-10 에 이미 *"덱에도 talk 에도 softening 을 잰 수치가 없다"* 는 미결이 있는데,
> **이 논문이 그 미결에 대한 첫 정량 자료**다 (단 **softening 자체가 아니라 PES hole 이라는 다른 지표**로).
> **나는 talk 을 안 건드렸다** — 대기열 밖이라 §99-11 양방향 링크 규율의 대상이 아니다.

---

## ⑤ 이 curator 가 **하지 않은 것** (조율 담당이 확인할 것)

- ⛔ `litdb/INDEX.md` 미수정 (위 ① 를 옮겨야 함)
- ⛔ `litdb/comparison_vs_ours.md` 미수정 (위 ②③ 를 옮겨야 함)
- ⛔ `db/` 미수정 · **git 명령 미실행** (요청에 따라)
- ⛔ `litdb/talks/` 미수정 (대기열 밖 — 단 ④ 의 정정 후보를 남김)
- ⚠ **`litdb/figures/_sources.json` 은 추출기가 자동 갱신했다** (196편 색인에 이 논문 추가). 의도된 동작.
- ⚠ **`fig_7.png` 는 수동 복구본**이다 — 자동추출기가 p.15 에서 "영역 없음"으로 버렸다
  (캡션 위에 이미지 2개가 나란한 배치). `figures.json` 의 해당 항목에 `"note": "manual recovery…"` 를 달아 뒀다.
  **`extract_figures.py --clean` 을 다시 돌리면 이 그림이 사라진다** — 재추출 시 복구 필요.
  (근본 수정은 추출기 쪽 일이라 이 세션에서 손대지 않았다.)
