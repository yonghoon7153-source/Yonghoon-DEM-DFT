# Fine-tuning MLIP foundation models: strategies for accuracy and transferability — Tompa & Varga-Umbrich (arXiv preprint, 2026)

> slug `tompa2026_finetuning_mlip_foundation_strategies` · arXiv `2606.12704v1` [physics.chem-ph], **10 Jun 2026** · DOI `n/a (preprint)` · type `MLIP` · PDF `7eca4ae9-91._Finetuning_MLIP_foundation_models_strategies_for_accuracy_and_transferability.pdf` · digested `2026-09-09` · status ✅
> elements: Li, P, S, Cl, Na, O, H, C, N, F, Br, I
> methods: MLIP, MD, NEB, DFT

> 🔴🔴 **동료심사 안 됐다 — arXiv preprint v1 이다.** 저널 투고·심사 흔적이 표지에 없다
> (creator = `arXiv GenPDF`, producer = `pikepdf`). **인용할 때 반드시 "preprint" 로 표기**하고,
> 수치는 **게재본에서 바뀔 수 있다는 전제**로 쓴다. 특히 아래 §10 에 적은 **그림 축 단위 불일치**와
> **Freeze (5)/(6) 라벨 미정의**는 심사 과정에서 정정될 가능성이 높은 종류다.
> ⚠ 저자진 자체는 신뢰도가 높다 — **MACE 를 만든 그룹 본인들**(Batatia = MACE 제1저자, Csányi = 교신)이고
> 이 논문에서 구현한 세 기능이 **MACE 3.15+ 본체에 이미 들어가 있다**. 즉 "제안"이 아니라 "출시된 코드의 설명서"에 가깝다.

> 🔗 **왜 이 편인가 (2026-09-09 인입 맥락).** 같은 날 들어온 UQ 3편
> (`grasselli2025_uncertainty_era_ml_atomistic` · `imbalzano2021_committee_uq_md_thermodynamic_averages` ·
> `kurniawan2025_comparative_ensemble_uq_nnip`)이 공통으로 남긴 막다른 골목 —
> **Grasselli 식 (27) 이 M ≥ 4 를 요구하는데 우리 이종 committee 는 M = 3 이고, UMA 는 단일
> 체크포인트라 동종 committee 재료가 없다** — 의 유일한 출구가 `kurniawan` 이 짚은
> **snapshot ensemble(= fine-tune 하면 체크포인트가 공짜)** 이었다.
> **그 "그럼 fine-tune 을 어떻게 하나" 에 답하는 편이 이 논문이다.**
> ⚠ **다만 이 논문 자체는 UQ·앙상블·불확실도를 한 번도 다루지 않는다** (전문 검색:
> `ensemble` = NEB 의 *nudged elastic band* 뿐 · `uncertainty` 0 · `committee` 0(참고문헌 [11] 제목에만) ·
> `snapshot` 0). §12-C 에 그 간극을 정면으로 적었다.

---

## 1. 한 줄 요약

MACE 파운데이션 모델을 **7가지 방식으로 fine-tune** 해 5개 화학계(그중 하나가 **Li₆PS₅Cl**)에서 비교한 결과,
**전략 선택보다 ① 파운데이션 모델의 품질 ② 원자기준에너지 E₀ 초기화 ③ 안정적 하이퍼파라미터가 먼저이고 그 영향이 더 크다**;
그 세 전제가 충족된 뒤에는 **좁은 표적 하나면 naive(전 파라미터) fine-tune 이 최선이고, 넓게 쓸 모델이면
replay(multihead) 만이 파운데이션의 OOD 견고성과 단거리 반발벽을 지킨다** — 그리고 **catastrophic forgetting 은
"약한 파운데이션 + 잘못된 E₀ + 불안정 학습"의 결과였지 naive fine-tuning 의 본질적 결함이 아니었다**는 것이 저자들의 주장이다.

## 2. 메타

| 항목 | 값 |
|---|---|
| 저자 | **Tamás Lajos Tompa**†, **Eszter Varga-Umbrich**¹†, **Ilyes Batatia**¹, **Alin M. Elena**², **Noam Bernstein**³, **Gábor Csányi**¹\* (†공동 1저자) |
| 소속 | ¹Univ. of Cambridge Dept. of Engineering · ²STFC Daresbury Lab · ³U.S. Naval Research Laboratory |
| 발표 | **arXiv 2606.12704v1**, physics.chem-ph, 2026-06-10. **동료심사 전** |
| 분량 | 본문 20 pp + 참고문헌 3 pp + Appendix A–H 14 pp = **37 pp**. **별도 SI 없음**(부록이 SI 역할) |
| 그림·표 | **Fig. 1–20**(본문 11 · 부록 9) · **Table 1–9**(본문 4 · 부록 5) |
| 조성/계 | **Li₆PS₅Cl(LPSC)** · aqueous NaCl · ice Ih/II/VI/VIII · Sɴ2 반응 · SPICE 생체분자 (+ UiO-66 MOF) |
| 연구유형 | **MLIP 방법론 벤치마크** (DFT/MP2 라벨은 전부 **기존 공개 데이터셋 재사용**, 새 DFT 캠페인 아님) |
| 코드 | `github.com/ACEsuit/mace` **MACE ≥ 3.15** — LoRA · pseudolabel replay · E₀ reestimation 이 **이미 머지됨** |
| 데이터 | `huggingface.co/datasets/ev-tlt/MACE_finetuning_supplementary` (훈련셋 · **모델 체크포인트** · 평가 스크립트) |
| 이해상충 | Csányi 는 Symmetric Group LLP 파트너(force field 상용 라이선스) + Ångström AI 지분 보유 — **본인 신고** |
| 계산자원 | Isambard-AI(NVIDIA GH200) · CSD3 · MPCDF Viper-GPU(AMD MI300A) · STFC SCARF. **Li 계열만 NVIDIA A100** |

> ✅ **서지 확인**: 사용자 기억(“T. L. Tompa, E. Varga-Umbrich, **I. Batatia** 외, arXiv 2026, Batatia 는 MACE 저자”)은
> **표지와 일치**한다. 보탤 것 둘 — ⓐ 교신·감독은 **Csányi + Bernstein**이고 Batatia 는 3저자, ⓑ **Tompa 와
> Varga-Umbrich 가 공동 1저자**(†)다. 인용은 `Tompa, Varga-Umbrich, et al., arXiv:2606.12704 (2026)`.

## 3. 핵심 물성 (수치)

> ⛔ **우리 물성 4축(A 이온전도 / B 산화안정 / C 기계 / D 전자구조)에 넣을 값이 하나도 없다.**
> 이 논문은 σ · Ea · ESW · 탄성상수 · band gap 을 **한 번도 계산하지 않는다**.
> 전문 검색: `conductivity` 0 · `diffusion` 0 · `activation energy` 0 · `band gap` 0 · `elastic` 0 · `phonon` 1회(참고문헌 [24] 제목).
> **MD 는 돌리지만 "안정한가"와 "RDF 가 맞는가"만 본다 — 수송계수를 뽑지 않는다.**
> ⇒ `comparison_vs_ours.md` 는 **`🔧 방법 원전` 블록에만** 넣는다.

| 물성 | 값 | 비고 |
|---|---|---|
| 이온전도도 σ | **n/a** | 계산 안 함 |
| 활성화E Ea | **n/a** | 계산 안 함 |
| 산화 onset / ESW | **n/a** | 계산 안 함 |
| 기계적 (E/B/G, C_ij) | **n/a** | stress 라벨은 학습에 쓰지만(λ_S = 1.0) 탄성상수를 뽑지 않음 |
| 전자구조 (gap) | **n/a** | 계산 안 함 |

**대신 이 논문의 "물성"은 MLIP 정확도 지표다.** 우리에게 의미 있는 것만 추린다:

| 지표 | 값 | 계 · 조건 | 출처 |
|---|---|---|---|
| **LPSC 검증 힘 RMSE** | **18.4 meV/Å** (target head) | MACE-OMat-0-medium, multihead-pseudolabel, lr 1e-4, 500 LPSC 구성 | `Table 9` |
| **LPSC 검증 에너지 RMSE** | **0.5 meV/atom** (target head) | 동 | `Table 9` |
| replay head (MPTraj 10k) | E 6.1 meV/atom · F 23.9 meV/Å | 동 | `Table 9` |
| **다른 argyrodite(OOD) 힘 MAE** | 파운데이션 ≈0.043 → pseudolabel ≈0.030 eV/Å (`figure-read ≈`) | 130+ 조성, fine-tune 에 안 본 것 | `Fig. 7b`·`Fig. 17` |
| **비-argyrodite(OOD) 힘 MAE** | 파운데이션 ≈0.045 → **naive ≈0.075 (악화)** / pseudolabel ≈0.042 (`figure-read ≈`) | 동 | `Fig. 7b`·`Fig. 17` |
| Sɴ2 검증 (전체 데이터) | Naive E 0.05 meV/atom · F 3.8 meV/Å (scratch 0.19 / 12.1) | MP2 라벨 60구성 | `Table 4` |
| aq. NaCl (10% 데이터) | LoRA E 0.30±0.04 meV/atom · F 41.54±4.76 meV/Å | MP2 라벨, seed 1–3 | `Table 4` |
| SPICE E₀ 복원 오차 | 평균법 **3.13 eV** → reestimation **0.33 eV** (MAE, 10원소) | 전량 SPICE, 학습 없이 | `Table 2` |
| **multihead 추가 학습비용** | **naive 대비 3–15배** | 데이터 크기 의존 | Discussion |

## 4. DFT/계산 방법 ★

> ⚠ **이 논문은 DFT 를 직접 돌리지 않는다** (예외: E₀ 용 고립원자 계산). 라벨은 전부 남의 데이터셋이다.
> 따라서 "우리 DFT 설정과 비교"는 성립하지 않고, 비교 대상은 **MLIP 학습 설정**이다.

### 4.1 참조 이론수준 (계별) — `Table 6`

| 계 | 참조수준 | fine-tune 데이터 | 평가 | replay 데이터 |
|---|---|---|---|---|
| **Lithium electrolytes** | **PBE** | **500 LPSC 구성 (Li₆PS₅Cl 단일 조성)** — 학습+검증 | **130+ 다른 argyrodite 조성** + 여러 비-argyrodite Li 전해질 구조 (전부 미학습) | **MPTraj 무작위 10,000 구성 + OMat24 pseudolabel** |
| Aqueous NaCl | MP2 [21] | 963 구성 (분수 스케일링) | MD RDF vs BPNN 기준 | OMat24 원소일치 **2,912** |
| Ice polymorphs | **PBE+D3** | 400 (Ih/II/VI/VIII 각 100) | 상간 힘오차 + MD 안정성 | OMat24 원소일치 **196** |
| Sɴ2 반응 | MP2 [22] | 60 (**반응물/생성물만, 전이상태 제외**) | NEB 장벽 프로파일 | OMat24 원소일치 **3,706** |
| SPICE 생체분자 | ωB97M-D3(BJ)/def2-TZVPPD | 855,905 train / 95,100 val (MACE-OFF 정제본) | 별도 50,000 test + TorsionNet500 | OMat24 원소일치 **39,459** |

### 4.2 파운데이션 모델 아키텍처 — `Table 5`

| 모델 | Hidden irreps | L_max | Interaction block | Pair rep.(ZBL) | 파라미터 |
|---|---|---|---|---|---|
| MACE-OMat-small | 128×0e | 0 | DensityResidual | Yes | 8.2 M |
| **MACE-OMat-0-medium** ← 주 모델 | 128×0e + 128×1o | 1 | DensityResidual | Yes | 9.1 M |
| MACE-MH1 | 512×0e + 512×1o | 1 | ResidualNonLinear | Yes | 6.4 M |
| MACE-MP0a-medium | 128×0e + 128×1o | 1 | AgnosticResidual | **No** | 4.7 M |

- OMat 계열은 **Agnesi distance transform** 사용, MP0a 는 미사용.
- **MACE-MH1 은 readout head 6개**(OMat24 / OMol25 / MatPES / OC20 / MP-PBE / SPICE) — 나머지는 단일 head.
- MH1 은 **learnable bias 가 고립원자 에너지에 기여**한다 → E₀ 만 맞춰도 고립원자 정확도가 보장되지 **않는다**(§4.5).
- 비교에 등장하는 다른 체크포인트: MP-0a / MP-0b / MP-0b3 / MPA-0 / MH-0 (`Fig. 3a`).

### 4.3 손실함수 — Appendix A.1

- `L = λ_E L_E + λ_F L_F + λ_S L_S`, 각 항은 **Huber** (δ = **0.01**, MACE 기본 = OMat24 사전학습과 동일).
- **target head: λ_E = 10, λ_F = 10** — 에너지에 무게를 둔다(장벽·상대상안정 용도).
- **replay head: λ_E = 1, λ_F = 10** — 사전학습 목적함수와 동일하게.
- stress 라벨이 있는 계(ice)만 **λ_S = 1.0**.
- ⛔ **2단계 손실 스케줄(force → energy) 금지.** from-scratch 의 관례이지만 fine-tune 에서는 전환 지점(epoch 500)에서
  에너지·힘 오차가 **급등**하고 완전히 회복되지 않는다 (`Fig. 12`). 2단계 lr 을 낮추면 스파이크는 줄지만 상수가중 대비 개선 없음.

### 4.4 하이퍼파라미터 (전략별 개별 최적화) — `Table 7`

| 전략 | 학습률 | EMA decay | Grad clip | 학습가능 비율 |
|---|---|---|---|---|
| From-scratch | 10⁻² | 0.99 | 10.0 | 100% |
| **Naive** | **10⁻³** | 0.999 | 1.0 | 100% |
| Freeze | 10⁻³ | 0.999 | 1.0 | ~5% |
| LoRA (r=4) | **10⁻²** | 0.99 | 10.0 | ~2.5% |
| LoRA (r=16) | 10⁻² | 0.99 | 10.0 | ~10% |
| LoRA (r=64) | 10⁻² | 0.99 | 10.0 | ~30% |
| **Multihead** | **10⁻⁴** | **0.9999** | 1.0 | 100% |
| Pseudolabel MH | **10⁻⁴** | **0.9999** | 1.0 | 100% |
| MH + LoRA | 10⁻³ | 0.999 | 10.0 | ~2.5% |

- 옵티마이저 **AdamW** (β₁=0.9, β₂=0.999).
- ⛔ **weight decay = 0 (fine-tune 공통).** weight decay 는 파라미터를 **0 쪽**으로 당기지 **사전학습 해 쪽**으로 당기지 않는다
  → 파운데이션에서 출발한 이점을 스스로 깎는다. **이 한 줄이 이 논문에서 제일 자주 틀리는 것으로 지목된 설정이다.**
- LoRA 는 naive 보다 **한 자릿수 높은 lr** 을 견딘다(제약된 적응이 공격적 최적화를 허용).
- **multihead 는 반대로 한 자릿수 낮은 lr 이 필요**하다 — 두 head 가 매 스텝 상충하는 gradient 를 준다는 해석.

### 4.5 원자기준에너지 E₀ — §2.6 (이 논문의 실질적 기여 중 하나)

MACE 는 총에너지가 아니라 **고립원자 기준 원자화에너지**를 예측한다. 사전학습과 fine-tune 의 이론수준이 다르면
그 기준선이 어긋나고, 그 어긋남이 **fine-tuning 실패의 주된 원인**이라는 것이 §3.2 의 주장이다. 세 가지 방법:

1. **Explicit isolated-atom** — fine-tune 데이터와 **같은 코드·같은 이론수준**으로 단일원자 DFT
   (스핀편극 · 대칭 미부과 · 주기이미지 비상호작용 크기). **가장 정확하지만 원 DFT 워크플로 접근이 필요**.
2. **Averaging** — fine-tune 에너지를 원소 개수의 선형결합으로 최소제곱 (식 5). ⛔ **쓰지 마라.**
   ⚠ **조성이 전부 같으면 composition matrix 가 rank-deficient** 라 원소별 값이 유일하지 않고
   총 오프셋만 식별된다 (SVD 최소노름 해를 씀). **← LPSCl 단일조성 fine-tune 이 정확히 이 함정에 빠진다.**
3. **★ Model-aware reestimation** (식 6, 이 논문 구현) — 사전학습 모델의 **예측**과 fine-tune 참조에너지의
   잔차를 원소별 보정 Δ E₀ 로 최소제곱. 완벽한 사전학습 모델이면 잔차가 순수 기준선 차이라 **정확히 복원**된다.
   전제: 사전학습 모델이 이미 상호작용에너지를 대략 맞혀야 한다(무작위 초기화 모델엔 무의미).
   ⚠ 같은 rank-deficiency 를 공유 — 역시 최소노름 해.

> **검증 (`Table 2`)**: MACE-OMat-0-medium(가전자 기준, ≈0 shift)으로 **전자 전량 SPICE**(절대 수만 eV)
> 의 E₀ 를 맞혔더니 — **학습 없이** — 평균절대오차 **평균법 3.13 eV vs reestimation 0.33 eV**.
> Br(−70,045 eV) 같은 극단 규모에서도 reestimation 오차 0.238 eV. **기준선 규모가 달라도 작동한다**는 증거.

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | **7전략 도식** — from-scratch / naive / layer-freeze / LoRA / multihead. 색으로 "무작위 초기화 · 사전학습(또는 replay 갱신) · 새 데이터로만 학습 · 새 데이터로 갱신 · 동결" 5종 가중치를 구분. Epoch 0 → N 로 가중치가 파랑(사전학습)→주황(새 데이터)으로 물드는 것을 보여줌 | **우리 발표·SI 에 그대로 쓸 수 있는 개념도.** multihead 패널이 "공유 몸통 + Pretrain Readout / Default Readout 두 갈래"를 명확히 보여준다 — snapshot ensemble 설명할 때 이 구조가 전제 |
| 2 | 5개 벤치마크 계 개요. **OMat24 핵심영역에서 멀어지는 순서**로 배열: **LPSC(가장 가까움)** → aq. NaCl → ice → Sɴ2 → SPICE | **우리 계가 이 논문의 "가장 쉬운 쪽 끝"**이라는 것을 명시하는 그림. 방법 간 차이가 제일 안 보이는 자리 = 우리 자리 |
| 3a,b | **파운데이션 품질이 결과를 지배한다.** (a) LPSC: 8개 체크포인트를 **같은 pseudolabel-replay 레시피**로 fine-tune 후 argyrodite/비-argyrodite OOD 에서 violin. (b) Sɴ2 NEB: OMat24 기반은 MP2 장벽 재현, MPTraj 기반은 **곡선이 붕괴** | ★★ **우리 축의 핵심.** (a) 힘 MAE 가 MP-0a ≈0.105 → MH-1 ≈0.036 eV/Å (`figure-read ≈`, 약 3배) — **전략 간 차이(≈25%)보다 훨씬 크다** |
| 4a,b | **E₀ 초기화가 방법 차이를 넘어선다.** (a) LPSC: reestimated vs averaged E₀ × {Naive, LoRA}. (b) Sɴ2 NEB + H–H/F–F dimer 곡선 | ★★ averaged E₀ 는 argyrodite 힘 MAE 를 ≈0.040 → ≈0.075 eV/Å 로 **2배 악화**시킨다 (`figure-read ≈`). **단일조성 fine-tune 이면 averaging 은 애초에 rank-deficient** |
| 5 | ice 4상 교차학습 힘 RMSE, reestimated vs averaged E₀ × {Naive, LoRA} | E₀ 효과가 전략 차이보다 크다는 두 번째 계 |
| 6 | 좁은 표적 결과. **a,b** Cl–O RDF (10% / 100% 데이터) · **c** Sɴ2 NEB 프로파일 · **d** EMD vs 데이터량 | **10% 데이터(≈96 구성)에서 이미 포화**. 데이터를 더 넣어도 안 좋아진다는 정량 근거 |
| 7a,b | **근접 전이(near-transfer).** (a) ice 상간 (b) **LPSC → 다른 Li 전해질** | ★★★ **우리한테 제일 중요한 한 장.** 아래 §12-B 전체가 이 그림 |
| 8 | SPICE test 오차(1 구성/분자, 19,687 구성)를 subset 별로 분해 | naive 가 표적정확도 1위. 우리 축과는 무관 |
| 9 | SPICE torsion 정확도 vs 데이터 분수 + 대표 torsion 프로파일 | LoRA rank ↑ 이면 torsion 개선 — capacity-matching 근거 |
| 10a,b | **★ catastrophic forgetting.** (a) SPICE fine-tune 후 **OMat test set 힘 RMSE** (b) ice Ih fine-tune 후, 파운데이션 크기 3종 | ★★★ **§12-C 전체.** naive 는 파운데이션 대비 **≈4×10³ 배** 악화, replay 는 **≈1 배** |
| 11 | **RSS PES-hole 히트맵** (NaCl fine-tune 모델). 0.1 GPa / 50 GPa × 8전략 × 4데이터량. **숫자가 셀에 인쇄돼 있음** | ★★★ **b₂o₃ 골격 creep 과 같은 종류의 실패를 직접 잰 유일한 표.** 아래 §12-D |
| 12 | 손실가중 스케줄 비교 (ice Ih), naive/scratch × 상수 vs 2단계 | 2단계 스케줄 쓰지 말 것의 근거 |
| 13 | **multihead replay 의 lr 민감도 (LPSC)** — {1e-2, 1e-3, 1e-4} × {target head, replay head} 손실곡선 | **우리 계로 직접 잰 것.** lr 1e-3 만 돼도 replay head 가 즉시 튀고 회복 안 됨 |
| 14 | 같은 lr 스윕을 Sɴ2 에서 (replay set 2종) | 계 무관하게 1e-4 |
| 15 | **replay 조성 비교 (LPSC)** — 원소일치 OMat24 / 무작위 MPTraj 10k / 둘 결합 | **replay 구조의 출처는 중요하지 않다** — 구조적 다양성만 있으면 됨. 우리가 OMat24 원본을 못 구해도 된다는 뜻 |
| 16 | NaCl PES-hole 에 대한 replay-set 비교 (0.1 / 50 GPa) | 세 replay 선택 모두 hole 을 크게 줄이고 서로 차이는 ~3%p 이내 |
| 17 | **LPSC: 파운데이션 baseline(fine-tune 전) + Naive/LoRA/Multihead 를 MP0·OMat 두 계열로** | ★★★ **"OMat 파운데이션을 fine-tune 안 하고 그냥 쓴 것"이 "MP0 를 최선으로 fine-tune 한 것"보다 낫다**는 그림. §12-B |
| 18 | ice 교차학습에서 파운데이션 용량 효과 (OMat-small / medium / MH-1) | 용량↑ 이면 in-phase 유리, cross-phase 에서는 이점 축소 |
| 19 | ice 단일상 vs 4상 통합 fine-tune | **관련 상들을 섞는 것이 자동으로 이득이 아니다** — pseudolabel 이 특히 손해 |
| 20 | NaCl 전체 RDF·EMD 패널 (10% / 10%-10× / 100%) | Fig. 6 의 확장 |
| `Table 1` | **E₀ 가 MD 안정성을 결정한다** — ice Ih 25구성 학습, averaged E₀ 면 naive/LoRA/multihead **전부 불안정**, reestimated 면 **전부 안정** | ★★ **검증 RMSE 는 멀쩡한데 MD 가 터지는** 실측 사례. 우리 b₂o₃ 교훈과 같은 계열 |
| `Table 2` | SPICE E₀: explicit / averaging / reestimation 10원소 비교 | **S 오차 평균법 −2.409 eV vs reest. +0.351 eV**, **Cl −1.681 vs +0.163** — 우리 원소가 표에 있다 |
| `Table 3` | MACE-MH1 고립원자 RMSE vs 고립원자 구성 반복수 | learnable-bias 모델은 고립원자 구성을 **학습셋에 명시적으로 넣어야** 함 |
| `Table 4` | Sɴ2 · aq. NaCl 검증 RMSE (8전략) | 좁은 표적에서 LoRA/naive 우위. **Freeze (6) 이 유일하게 scratch 보다 나쁨** |
| `Table 5` | 파운데이션 아키텍처 요약 | §4.2 |
| `Table 6` | 벤치마크 데이터셋 요약 (참조수준·크기·평가·replay) | §4.1 — **LPSC 500 구성**의 출처 |
| `Table 7` | 전략별 하이퍼파라미터 | §4.4 — **그대로 복사해 쓸 표** |
| `Table 8` | MACE stress-loss 판 MH1 고립원자 RMSE | Table 3 의 보조 |
| `Table 9` | **LPSC · Sɴ2 lr 스윕 최종에폭 검증 RMSE** | ★★ **LPSC 목표head F RMSE 18.4 meV/Å** 의 출처 |

### 5.1 실제로 본 그림 / 안 본 그림 (2026-09-09)

- **크로핑 28장 + 수동복구 1장 = 29장** (`litdb/figures/tompa2026_finetuning_mlip_foundation_strategies/`).
  ⚠ **`Fig. 7` 은 자동추출기가 놓쳤다**(캡션 위에 이미지 2개가 나란히 있는 배치 → "영역 없음") —
  p.15 의 좌표 `(70,208)-(541,368)` 로 **수동 렌더해 `fig_7.png` 로 넣고 `figures.json` 에 등록**했다.
- **눈으로 본 것 (6장)**: `Fig. 1`(전략 도식) · `Fig. 3`(파운데이션 품질) · `Fig. 4`(E₀) ·
  **`Fig. 7`(LPSC 전이)** · **`Fig. 10`(forgetting)** · **`Fig. 11`(RSS holes)** · `Fig. 17`(LPSC 파운데이션×전략) — 실제 7장.
- **안 본 것**: `Fig. 2, 5, 6, 8, 9, 12, 13, 14, 15, 16, 18, 19, 20` (13장). 이유 — 우리 4축(이온전도·산화안정·기계·전자구조)에
  안 걸리거나(SPICE·ice·NaCl 전용), 본문 서술로 충분히 특정되거나(`Fig. 13`→`Table 9` 에 수치가 있음),
  캡션이 결론을 다 담고 있다. **표 9장(`tab_*.png`)은 이미지로 안 읽었다** — PDF 텍스트가 정확하다(관례).
- **본문 서술과 어긋난 것**: **2건 발견**. §10-1(축 단위 불일치), §10-2(Freeze 라벨). 둘 다 아래에.

## 6. Post-processing ★

이 논문의 방법론적 강점은 **"pointwise 오차만 보면 놓치는 실패"를 잡는 4가지 프로토콜**을 붙였다는 것이다.
우리가 그대로 베낄 수 있는 부분이다.

| 프로토콜 | 무엇을 잡나 | 도구·설정 | 계 |
|---|---|---|---|
| **NEB 반응경로** | **에너지 장벽**. 고정궤적 재평가가 아니라 **모델이 스스로 MEP 를 완화**해야 함 | Kolsbjerg–Groves–Hammer **automated NEB** [26]. 동일 NEB 설정으로 모델만 교체 | Sɴ2 (MP2 장벽 대조) |
| **MD RDF + EMD** | **구조(용매화 껍질)**. RDF 를 BPNN 기준과 **earth mover's distance** 로 스칼라화 | MD 궤적 → RDF → EMD | aq. NaCl |
| **MD 안정성 시험** | **터지느냐**. ①100 K NPT **250 ps** 완주 ②50→800 K **50 ps** 램프 | 비물리 왜곡·결합절단 육안/판정 | ice (`Table 1`) |
| **★ RSS (random structure search)** | **PES 구멍** = 단거리 반발벽이 인력으로 뒤집힌 영역 | **PyXtal** [37] 로 10 조성 × 50 초기구조 = **모델당 500 구조**. **relax–rattle 3회 반복** | NaCl · (LPSC 도 했다고 서술, **그림 없음**) |

**RSS 판정 4기준** (Appendix A.5) — 하나라도 걸리면 flagged:
1. **원자겹침**: 최소 원자간거리 / (공유반경 합) < **0.5**
2. **이상 부피**: 원자당 부피 < 조성별 중앙값의 **30%**
3. **이상 에너지**: 원자당 에너지가 중앙값보다 **10 MAD** 아래 (최소 문턱 **5 eV/atom**)
4. **완화기준 복합**: 부피 < 중앙값의 50% **그리고** 에너지 < 중앙값

> ★ **중요**: 모든 모델에 **ZBL 차폐쿨롱 pair repulsion** 이 명시적으로 들어 있다
> (총에너지에 직접 더하고 공유반경 합에서 다항식 cutoff 로 부드럽게 0). **그래도 구멍이 생긴다.**
> ⇒ 이 구멍은 **pair 항의 부재가 아니라 학습된 many-body 반발 기여의 붕괴**다.
> 우리가 "ZBL 넣었으니 괜찮다"고 넘어갈 수 없다는 뜻.

## 7. 우리 DFT/MLIP 대비 → `our_dft_baseline.md`

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **엔진** | MACE (등변 message-passing, e3nn 계열), 4.7–9.1 M 파라미터 | **UMA-s-1p1 (omat task)**, fairchem | ⚠ **아키텍처가 다르다.** 저자 스스로 §Discussion 에서 *"모든 실험이 MACE 다 … 다른 아키텍처로의 일반화는 미검증"* 이라고 못박음 |
| **파운데이션 사전학습셋** | OMat24 (주) / MPTraj (비교군) | **OMat24 계열** (UMA 의 omat task) | ⭕ **사전학습 도메인이 같다** — 이 논문의 "OMat24 기반이 MPTraj 기반보다 낫다" 결론의 **좋은 쪽**에 우리가 있다 |
| **fine-tune 여부** | 7전략 비교 | **고정 체크포인트, fine-tune 0회** | 🔴 **우리는 `Fig. 17` 의 `OMat (found.)` 회색 violin 자리에 있다** — 즉 *"fine-tune 안 한 강한 파운데이션"* |
| **표적계** | Li₆PS₅Cl (단일 조성, 500 PBE 구성) | Li₆PS₅Cl · **Li₅.₄PS₄.₄Cl₁.₆** · +B₂O₃ · Nd–O 공도핑 | ⚠ **우리 계가 더 넓다.** 이 논문은 조성 하나만 학습하고 나머지를 OOD 로 뒀다. 우리는 그 "나머지"를 **본론**으로 쓴다 |
| **라벨 이론수준** | **PBE** (Li 계) | 우리 DFT 는 QE·PBEsol 계열(계별 상이) · MLIP 벤치 라벨은 PET-MAD Li₃PS₄ 셋 | ⚠ **E₀ 재추정이 필수인 조건** — 코드·functional·pseudo 가 전부 다르면 기준선이 어긋난다(§4.5) |
| **힘 정확도(참고)** | LPSC 검증 F RMSE **18.4 meV/Å** (fine-tune 후, MACE-OMat-0-medium) | **UMA-s-1p1 zero-shot, Li₃PS₄: F MAE 30.0 · RMSE 44.6 meV/Å** (`db/properties/mlip_bench_li3ps4_uma.json`, 243 구조) | ⚠⚠ **직접 비교 금지.** 모델(MACE vs UMA)·계(LPSCl vs Li₃PS₄, **Cl 유무**)·라벨(PBE vs PET-MAD)·평가셋이 전부 다르다. **"자릿수가 같다"까지만** |
| **무질서 처리** | ⛔ **한 번도 안 다룬다.** LPSC 500 구성이 어떤 배열/점유인지 미기재 | Cl/S 부분점유가 우리 계의 본질 | 🔴 **공백**. §13 참조 |
| **UQ / 앙상블** | ⛔ 전혀 없음 | 이종 committee M=3 (`tools/ionic/mlip_committee.py`) | 🔴 이 논문은 UQ 를 **안 한다** — 우리가 §12-C 에서 **유도**해 쓰는 것이지 논문이 말한 것이 아니다 |
| **MD 산출물** | 안정성 · RDF 만 | **D · Ea · NE σ** (MSD 2–50 ps, 600/800/1000 K) | 🔴 **수송계수 층위가 이 논문에 없다** |

## 8. 적용 인사이트 (우리 연구에 어떻게)

1. **① 우리는 이미 "좋은 자리"에 있다 — 그게 이 논문의 1번 권고다.**
   `Fig. 17`: OMat 파운데이션을 **fine-tune 하지 않고 그냥 쓴 것**이 MP0(MPTraj) 를 **최선으로 fine-tune 한 것**보다
   argyrodite 힘 MAE 에서 낫다 (≈0.043 vs ≈0.072 eV/Å, `figure-read ≈`). UMA 는 OMat24 계열이다.
   ⇒ **"UMA 를 그냥 쓴다"는 것이 이 논문 기준으로 방어 가능한 기본선**이다. 지금까지 이 말을 문헌으로 못 했다.

2. **② fine-tune 을 한다면 "몇 점이 드나"의 답이 나왔다 — 우리 계로.**
   **500 PBE 구성 / 단일 조성**. NaCl 은 **96 구성(10%)** 에서 이미 포화했고 ice MD 안정성은 **25 구성**으로 됐다.
   ⇒ **DFT 100–500 점 규모**. 우리가 못 할 규모가 아니다.

3. **③ 그런데 "fine-tune 하면 기존 결과와 비교가 끊긴다"가 정량화됐다 — 그리고 값이 나쁘다.**
   `Fig. 7b`·`Fig. 17`: LPSC 500구성으로 naive fine-tune 하면 **비-argyrodite Li 전해질 힘 MAE 가
   ≈0.045 → ≈0.075 eV/Å 로 1.7배 악화**(OMat 기반), MP0 기반이면 ≈0.08 → ≈0.28(3.5배, 꼬리 0.96 eV/Å).
   ⇒ **plain LPSCl 로만 fine-tune 하면 +B₂O₃ · Nd–O 계는 오히려 나빠질 수 있다.** 이것이 우리 최대 리스크다.

4. **④ 그 대가를 없애는 유일한 방법이 replay 이고, 값이 싸다.**
   `Fig. 15`·Appendix E: **replay 구조의 출처는 상관없다** — OMat24 원소일치본 / 무작위 MPTraj 10k / 결합,
   셋 다 같은 결과. 그리고 라벨은 **파운데이션 모델이 스스로 붙인다(pseudolabel)**.
   ⇒ **OMat24 원본 데이터가 없어도 replay 가 된다.** 우리에게 결정적이다(fairchem 은 OMat24 를 배포하지만
   우리 디스크·대역폭 기준으로는 부담). 비용은 **학습 compute 3–15배**.

5. **⑤ `Table 1` 이 우리 b₂o₃ 교훈의 문헌판이다.**
   *검증 RMSE 는 멀쩡한데 100 K MD 가 50 ps 안에 터진다* — 원인이 **E₀ 초기화 하나**였다.
   우리 b₂o₃ 골격 creep 도 "지표는 그럴듯한데 궤적이 물리를 잃은" 같은 계열이다.
   ⇒ **MLIP 결과를 받을 때 pointwise 지표만 보지 않는다**는 규율에 문헌 근거가 생겼다.

## 9. 인용 가능 문장 (deck/paper 용)

> ⚠ 전부 **preprint 인용**으로 표기할 것. `Tompa & Varga-Umbrich et al., arXiv:2606.12704 (2026)`.

- "Fine-tuning 결과를 지배하는 것은 전략 선택이 아니라 **파운데이션 모델의 품질·E₀ 일관성·안정적 최적화**이며,
  이 전제들이 어긋나면 그 영향이 전략 간 차이를 일상적으로 넘어선다."
- "리튬 argyrodite 벤치마크에서, **fine-tuning 을 적용하지 않은 OMat24 기반 파운데이션 모델**이
  MPTraj 기반 파운데이션을 fine-tune 한 최선의 모델과 **동등하거나 더 낮은** 힘·에너지 오차를 보였다."
- "좁은 표적 하나에 쓸 모델이면 naive fine-tuning 이 이기기 어렵고, 넓게 배치할 모델이면
  **multihead replay 가 사전학습 분포 정확도와 단거리 반발벽을 함께 지키는 유일한 방법**이었다."
- "replay 라벨을 파운데이션 모델 자신의 예측으로 대체(pseudolabel)해도 원 DFT 라벨과 결과가 거의 같아,
  **replay 구조의 출처를 사전학습 코퍼스로부터 분리할 수 있다.**"
- "학습셋을 키우면 in-domain 정확도는 좋아지는데 **PES 구멍은 오히려 늘어난다** — replay 없는 방법에 한해서."
- ⛔ **쓰면 안 되는 문장**: *"이 논문이 fine-tuning 이 이온전도도/장벽 예측을 개선한다고 보였다"* —
  **σ·D·Ea 를 한 번도 계산하지 않는다.**

## 10. 주의/한계 (over-claim 방지)

### 10-1. 🔴 **`Fig. 10` 의 두 패널이 단위가 어긋난다 (내가 그림을 보고 발견)**
`Fig. 10a` y축 = **"Force RMSE (meV/Å) on OMat"**, 파운데이션 기준선 ≈0.35.
`Fig. 10b` y축 = **"Force RMSE on OMat (eV/Å)"**, 참조선 ≈0.4.
**1000배 차이**다. 둘 중 하나는 라벨 오기다 — 그리고 두 값 모두 MACE-OMat 의 알려진 힘오차
(수십 meV/Å 대)와 맞지 않는다.
⇒ **절대값을 인용하지 않는다.** 같은 패널 안의 **파운데이션 대비 비율**만 쓴다(비율은 단위와 무관).
그것이 아래 §12-C 표의 형식이다.

### 10-2. 🔴 **"Freeze (5)" · "Freeze (6)" 이 어디에도 정의돼 있지 않다 (그림 ↔ 본문 불일치)**
§2.3 은 두 동결 변형을 **말로만** 정의한다(“readout 만 학습” / “embedding + 첫 MP block 동결”).
그런데 `Table 4` 와 `Fig. 11` 은 **`Freeze (5)` · `Freeze (6)`** 이라는 이름을 쓰고 **매핑을 안 준다.**
게다가 `Fig. 11` 은 **Freeze (5) 가 8전략 중 최악**(0.1 GPa 100% 데이터에서 hole **49.4%**, 파운데이션 8.6% 대비 **+40.8%p**)
인데, 본문은 *"readout 만 남기고 전부 동결하면 반발벽이 보존된다"* 고 쓴다.
⇒ **Freeze 계열의 어떤 변형이 안전한지 이 논문만 보고 결정할 수 없다.** 우리는 Freeze 를 쓰지 않는 편이 낫다.
(추정으로는 Freeze (6) = readout-only 가 중립(+0.4~+1.8%p)이라 그쪽이 본문의 "안전한 것"으로 보이지만,
**추정이다 — 이 매핑을 인용하지 말 것.**)

### 10-3. **LPSC 에 대한 RSS 결과가 서술만 있고 그림이 없다**
Appendix A.5: *"We apply this protocol to both NaCl-fine-tuned **and lithium-electrolyte-fine-tuned** models."*
그런데 `Fig. 11` 도 `Fig. 16` 도 **NaCl 뿐**이다. **우리 계의 PES-hole 수치는 이 논문에 없다.**
⇒ §12-D 의 이식은 **NaCl 에서 Li 계로의 유추**이지 직접 근거가 아니다.

### 10-4. **저자가 스스로 적은 한계 4가지** (Discussion 말미)
1. **모든 실험이 MACE 아키텍처.** 등변·message-passing 이라는 귀납편향은 공유되지만
   **LoRA·layer freezing·multihead 의 구체적 거동은 다른 아키텍처에서 다를 수 있다** — 미검증.
   🔴 **우리 UMA 에 그대로 옮길 수 없다는 뜻이다.**
2. **하이퍼파라미터 탐색이 제한적.** 주요 설정(lr, λ_E/λ_F, batch, EMA, grad clip, weight decay)만 튜닝했고
   **철저한 method-specific search 는 안 했다.** 특히 **LoRA(어댑터를 어느 층에 다느냐)** 와
   **multihead(replay:target 데이터 비율·손실가중)** 는 순위가 바뀔 수 있다.
3. **RSS 가 모든 실패모드를 덮지 않는다.** relax–rattle 은 **단거리 반발벽 붕괴**만 본다.
   *"경쟁 상들의 상대안정성이 틀리는"* 종류의 PES 결함은 **다른 진단이 필요**하다.
   🔴 **우리 b₂o₃ 골격 creep 은 오히려 이쪽(상대안정성/골격 강성)에 가깝다** — §12-D 참조.
4. **파운데이션이 전부 주기적 무기물 위주 학습.** SPICE 결과가 분자계 fine-tune 가능성을 보이지만
   분자응용 전반을 망라하지 않는다.
5. (열린 질문) **최적 replay 조성**(어떤 구조를 · 어떤 비율로 · 총 몇 개) — **미해결, 향후 과제로 남김.**

### 10-5. **우리가 추가로 지적할 한계**
- **오차막대가 대부분 없다.** seed 반복은 **aq. NaCl 만**(seed 1–3), Sɴ2 는 명시적으로 *"single run"*.
  **LPSC·ice·SPICE 결과에 시드 산포가 없다** ⇒ `Fig. 7b` 의 "naive ≈0.075 vs pseudolabel ≈0.042" 같은
  차이가 시드 노이즈보다 큰지 **논문이 보증하지 않는다**. (violin 은 *평가구조 간* 산포이지 *시드 간* 산포가 아니다.)
- **LPSC 500 구성의 출처·샘플링이 안 적혀 있다.** MD 스냅샷인지 rattle 인지, 어느 온도인지,
  **Cl/S 부분점유를 어떻게 다뤘는지** 전부 미기재. 우리 계의 본질적 자유도가 통째로 빠져 있다.
- **비-argyrodite 평가셋의 정체가 모호하다.** *"several non-argyrodite structures"* — **개수도 조성도 없다.**
  §12-B 에서 우리가 제일 무겁게 쓰는 숫자가 나오는 셋인데, **N 을 모른다.**
- **compute 보고가 "3–15배" 한 줄뿐.** GPU-시간·벽시계·epoch 수가 **어디에도 없다.**
  ⇒ **"UMA fine-tune 에 GPU 몇 시간 드나"에 이 논문은 답하지 않는다** (§12-E).
- **`Table 4` 의 Sɴ2 열은 단일 run 인데 소수 둘째 자리까지 적혀 있다** (0.05 vs 0.03 vs 0.04 meV/atom).
  이 자릿수의 순위는 **의미 없다고 봐야 한다**.
- **from-scratch 기준선이 불리하게 설정된 구석이 있다.** Agnesi transform 을 scratch 에서만 껐다
  (*"severe optimisation instabilities"*). 저자는 공정성을 위해서라고 하지만 **아키텍처가 달라진 것**이다.

## 11. 기술 용어 미니사전 (우리 팀용)

- **파운데이션 MLIP (foundation model)** — 수백만 구조의 광범위 DFT 데이터로 미리 학습해 두고,
  임의의 조성에 그대로 힘·에너지를 주는 범용 원자간포텐셜. MACE-OMat / **UMA** / CHGNet / SevenNet / Orb 등.
- **naive fine-tuning** — 사전학습 체크포인트에서 시작해 **전 파라미터**를 표적 데이터로 계속 학습.
  구조 변경 없음. 다만 lr 을 낮추고 EMA decay 를 올린다(한 스텝에 얼마나 멀리 가는지를 제한).
- **EMA (exponential moving average) decay** — 가중치의 지수이동평균을 별도로 유지하고 **그것을 모델로 쓴다**.
  decay 0.999 → 대략 최근 1000 스텝의 평균. **0.9999 면 최근 10⁴ 스텝.**
  ★ 이것이 §12-C 의 snapshot ensemble 논의에서 핵심이 된다 — **EMA 가 높을수록 체크포인트끼리 서로 비슷해진다.**
- **layer freezing** — 일부 층의 가중치를 **고정**하고 나머지만 학습. **깊이 방향(depth-wise) 제약**.
- **LoRA (Low-Rank Adaptation)** — 원 가중치 `W` 를 얼리고 `W + BA` 로 바꾼다
  (`B ∈ R^{d_out×r}`, `A ∈ R^{r×d_in}`, `r ≪ min(d_in,d_out)`). `A ~ N(0,σ²)`, **`B = 0` 으로 초기화**해서
  시작 시점에 `W+BA = W`(= 파운데이션과 정확히 동일). **너비 방향(width-wise) 제약**.
  · MACE 판 특이점: **등변 linear layer** 에도 적용하되 **irrep 블록별로 독립**인 스칼라 가중치
  `W_l → W_l + B_l A_l` 로 분해 → **irrep 을 섞지 않으므로 등변성이 보존된다**.
  · ELoRA [20] 와의 차이: 이 논문은 **embedding·readout 을 포함한 모든 linear** 에 적용(ELoRA 는 등변층 + tensor product).
  · **참고**: r=4 가 medium 모델 전체 파라미터의 **약 3%**.
- **multihead replay** — 몸통(embedding+message passing)을 공유하고 **readout head 를 둘** 둔다:
  표적용 · replay 용. 손실은 두 head 의 합 (식 3). **head 마다 자기 E₀ 세트를 가진다**
  → 표적과 replay 의 **이론수준이 달라도 된다**. 지속학습(continual learning)의 experience replay [29,30] 의 원자계 판.
- **pseudolabel replay** — replay 데이터의 라벨을 **원 DFT 값이 아니라 fine-tune 대상 파운데이션 모델 자신의 예측**으로.
  [31] Learning without Forgetting 의 synthetic replay. **효과**: replay 구조 출처를 사전학습 코퍼스에서 **분리**하고,
  replay head 가 (좁은) replay 부분집합에 과적합하는 것을 줄인다.
- **E₀ (atomic reference energy)** — 원소별 고립원자 에너지. MACE 는 이걸 빼고 **원자화에너지**를 학습한다. §4.5.
- **catastrophic forgetting** [18] — 새 과제를 학습하면서 이전 과제 성능이 붕괴하는 현상.
  여기서는 **"fine-tune 후 OMat24 test set 에서의 힘오차"** 로 측정한다.
- **PES hole** — 퍼텐셜 에너지면에 생긴 비물리적 구멍. 원자를 가까이 밀면 **반발**해야 하는데
  모델이 **인력**을 예측해서 구조가 붕괴(implode)하는 영역.
- **ZBL** — Ziegler–Biersack–Littmark 차폐 쿨롱 pair 포텐셜. MACE OMat 모델에 **명시적으로 들어 있다**.
- **RSS (random structure search)** [27] — PyXtal 로 무작위 결정을 만들어 모델로 완화. 원래는 구조탐색용이지만
  여기서는 **PES 병리 탐지기**로 쓴다.
- **EMD (earth mover's distance)** — 두 분포(여기서는 RDF)를 옮기는 최소 "일". RDF 일치도를 **스칼라 하나**로.
- **Agnesi transform** — MACE 의 거리 변환 함수. OMat 계열 기본, MP0a 는 미사용.
- **Huber loss** — 잔차가 작으면 L2, 크면 L1. 이상치에 둔감. δ = 0.01.

---

## 12. 우리 좌표 — 본론 ★★★

> 우리 모델: **UMA-s-1p1 (omat task)**, fairchem, **고정 체크포인트**.
> 우리 계: Li₆PS₅Cl · Li₅.₄PS₄.₄Cl₁.₆ · +B₂O₃ · Nd–O 공도핑.
> 우리 라벨 자산: `db/properties/mlip_bench_li3ps4_uma.json` (**Cl 없음** — `elements: [Li,P,S]`) · 힘 대조용 700 K 20점(미실행).
> 우리 실패 전례: **Li₃N 사용 금지**(2026-06 결정론적 편향) · **b₂o₃ 골격 creep 으로 MD 전도도 축 전체 마감**.
> ⚠ **아래 모든 수치는 소환값이다. `db/` 절대값과 같은 표에 놓지 않는다.**

### 12-A. Fine-tune 전략 7종 — 정의 · 효과 · 트레이드오프 (질문 ①②)

| 전략 | 정의 (무엇을 학습하나) | 학습가능 | lr / EMA / clip | **표적 정확도** | **전이(OOD)** | **forgetting** | **반발벽(RSS)** | 추가 비용 |
|---|---|---|---|---|---|---|---|---|
| **From-scratch** | 무작위 초기화, 전 파라미터 | 100% | 1e-2 / 0.99 / 10 | 저데이터에서 **완패** (NaCl EMD 0.685 vs fine-tune 0.052–0.100) | — | — | **최악** (50 GPa 87.0%) | 데이터·시간 |
| **Naive** | 파운데이션에서 전 파라미터 이어학습 | 100% | **1e-3** / 0.999 / 1.0 | **최고** (Sɴ2 F 3.8 meV/Å · SPICE 1위 · ice trained-phase E ≈0.038 meV/atom) | **나쁨** (비-argyrodite 힘 ≈0.045→≈0.075) | **최악** (SPICE **≈4×10³ 배**) | 나쁨, 데이터 늘수록 악화 (8.0→20.2%) | 없음 |
| **Freeze (readout-only)** | embedding·MP·tensor product 전부 동결, readout 만 | ~5% | 1e-3 / 0.999 / 1.0 | 중간 | 제한적(solvation feature 적응 못 함) | — | 본문상 **보존**, ⚠ `Fig. 11` 라벨 불명(§10-2) | 없음 |
| **Freeze (embed + 1st MP)** | 앞 블록만 동결, 뒤 interaction 은 학습 | ~5% | 1e-3 / 0.999 / 1.0 | 중간~나쁨 (NaCl F 52.57 — scratch 42.44 보다 나쁨) | — | — | ⚠ 한쪽이 **최악**(+40.8%p) | 없음 |
| **LoRA r=4** | 모든 linear(scalar+등변)에 저랭크 `BA` 주입, 원 가중치 동결 | ~2.5% | **1e-2** / 0.99 / 10 | 좁은 계에선 **최고 수준** (NaCl E 0.30 · Sɴ2 E 0.02) / 넓은 계엔 부족 (SPICE 최하위권) | 중간 | **중간** (≈2×10² 배) | 나쁨 (50 GPa 100%데이터 **57.4%**) | 없음 |
| **LoRA r=16 / r=64** | 동, rank ↑ | ~10% / ~30% | 동 | rank↑ 이면 SPICE·torsion 개선 | 중간 | r=64 가 **≈4×10¹ 배**로 개선 | — | 없음 |
| **Multihead replay (원 라벨)** | 몸통 공유 + target/replay 두 head, 손실 합 | 100% | **1e-4** / **0.9999** / 1.0 | 표적에서 약간 손해 (ice trained-phase E ≈0.207 vs naive ≈0.038) | **최고** | **≈1 배 (거의 무손실)** | **최고** (전 조건 파운데이션 이하) | **학습 3–15배** + 사전학습 데이터 |
| **Pseudolabel replay** | 동, replay 라벨 = 파운데이션 예측 | 100% | 1e-4 / 0.9999 / 1.0 | 원 라벨과 **거의 동일** | **최고** | **≈1.3 배** | **최고** (0.1 GPa 최저 2.6%) | 학습 3–15배, **원 데이터 불필요** |
| **MH + LoRA (PS+LoRA)** | replay + LoRA 동시 | ~2.5% | 1e-3 / 0.999 / 10 | ⛔ **대체로 최악** (과규제) — **예외: 극단 희소(Sɴ2 5구성)에서 multihead 가 실패할 때만 성공** | 나쁨 | ≈4 배 | 중간 | 둘 다 |

**⚖ 트레이드오프가 걸리는 정확한 지점 3곳:**

1. **표적정확도 ↔ 견고성** — `Fig. 7a` ice 학습상(trained phase):
   naive E RMSE ≈0.038 vs multihead ≈0.207 meV/atom (`figure-read ≈`, **5.4배**);
   힘은 naive ≈0.0020 vs multihead ≈0.0031 eV/Å (**1.55배**).
   ⇒ **replay 의 값은 "표적에서 에너지 5배·힘 1.5배 손해"** 다. 힘 쪽 손해는 작다 — MD 용이면 감수할 만하다.
2. **정확도 ↔ 학습비용** — multihead 는 **naive 대비 3–15배 compute**. 두 이유가 겹친다:
   (ⓐ) epoch 당 데이터가 target+replay 로 늘고 (ⓑ) lr 을 10배 낮춰야 해서 epoch 당 수렴이 느리다.
3. **★ 표적정확도와 forgetting 은 서로 독립이다** (저자가 명시):
   *"forgetting and in-domain performance are largely decoupled"* — multihead/pseudolabel 은
   **표적정확도를 희생하지 않고** 사전학습 분포를 지킨다(SPICE 기준). ⇒ **"견고성을 사려면 정확도를 팔아야 한다"는
   직관이 SPICE 에서는 틀렸다.** ice trained-phase 에서는 (1)처럼 대가가 있다. **계 의존적이다.**

### 12-B. Lithium electrolyte 벤치마크 — 그 절 통째로 (질문 ④) ★★★

**이 논문의 5개 벤치마크 중 첫 번째가 우리 계다.** 절 구성은 §2.1(데이터) · §3.1(파운데이션) · §3.2(E₀) ·
§3.4-2(전이) · Appendix D(lr) · Appendix E(replay 조성) · Appendix F(`Fig. 17`) 로 흩어져 있다. 모아 옮긴다.

**계·데이터 (`Table 6`, §2.1)**
- **fine-tune: Li₆PS₅Cl 단일 조성, PBE 참조, 500 구성.** 학습 + 검증 겸용.
- **평가(전부 미학습)**: ⓐ **LPSC 이외의 argyrodite 구조 130+ 조성** ⓑ **비-argyrodite Li 전해질 구조**
  (*"elemental compositions can differ from the LPSC training composition apart from the shared presence of Li"*
  = **Li 만 공유하고 나머지 원소가 달라도 되는** 구조들. 개수·조성 미기재 — §10-5).
- **replay: MPTraj 무작위 10,000 구성 + OMat24 파운데이션 pseudolabel.**
- 위치 규정 (§2.1): *"LPSC 는 OMat24 에 흔한 종류의 무기 주기 고체라서 **이 계만으로 fine-tune 하면
  방법 간 구분이 어려울 것으로 예상**한다."* ⇒ **우리 계는 이 논문에서 "가장 쉬운 쪽 끝"이다.**

**결과 ① 파운데이션 품질 (`Fig. 3a`, 같은 pseudolabel-replay 레시피 · 같은 MPTraj 10k replay 로 고정)**

| 파운데이션 | argyrodite F MAE (eV/Å) | argyrodite E MAE (meV/atom) | 비-argyrodite F MAE |
|---|---|---|---|
| MP-0a | ≈**0.105** | ≈6.5 | ≈0.070 |
| MP-0b | ≈0.062 | ≈4.0 | ≈0.050 |
| MP-0b3 | ≈0.058 | ≈3.8 | ≈0.050 |
| MPA-0 | ≈0.057 | ≈2.8 | ≈0.050 |
| OMat-small | ≈0.048 | ≈2.1 | ≈0.048 |
| **OMat-med** | ≈**0.045** | ≈2.0 | ≈**0.045** |
| MH-0 (omat_pbe) | ≈0.045 | ≈1.9 | ≈0.048 |
| **MH-1 (omat_pbe)** | ≈**0.036** | ≈1.6 | ≈0.045 |

`figure-read ≈` — violin 중앙부 판독. **전부 그림에서만 읽었다.** 본문은 순위(“MP0a 최악, OMat·MH 최상위”)만 서술.
⇒ **파운데이션 교체로 힘 MAE 3배(0.105→0.036).** 아래 결과 ③ 의 전략 간 차이(≈25%)와 **한 자릿수 다르다.**

**결과 ② E₀ (`Fig. 4a`, MACE-OMat-0-medium)**

| 조건 | argyrodite F MAE | argyrodite E MAE | 비-arg. F MAE | 비-arg. E MAE |
|---|---|---|---|---|
| 파운데이션(fine-tune 전) | ≈0.043 | ≈1 meV/atom | ≈0.040 | ≈1.0 |
| **Reestimated E₀** + Naive | ≈0.040 | ≈2 | ≈0.080 | ≈2.3 |
| **Reestimated E₀** + LoRA | ≈0.034 | ≈2 | ≈0.060 | ≈1.7 |
| **Averaged E₀** + Naive | ≈**0.075** | ≈15 (꼬리 55) | ≈**0.15** | ≈4 |
| **Averaged E₀** + LoRA | ≈0.060 | ≈8 (꼬리 100+) | ≈0.12 | ≈5 |

`figure-read ≈`. 본문 명시값: *"averaged E₀ 는 reestimated 대비 **force RMSE 2–3배**"* — 판독과 일치.
🔴 **그리고 우리 조건에서는 averaging 이 애초에 정의되지 않는다**: LPSCl 단일 조성으로만 fine-tune 하면
composition matrix 가 **rank-deficient** 라 원소별 E₀ 가 유일하지 않다(§4.5). **최소노름 해가 나올 뿐이다.**

**결과 ③ 전략별 전이 (`Fig. 7b` · `Fig. 17`, MACE-OMat-0-medium, reestimated E₀)** ★ 우리 축 본체

| 모델 | argyrodite F MAE (eV/Å) | argyrodite E MAE (meV/atom) | **비-argyrodite F MAE** | 비-arg. E MAE |
|---|---|---|---|---|
| **OMat 파운데이션 (fine-tune 안 함)** | ≈0.043 (좁음: 0.035–0.050) | ≈1.8 | ≈**0.045** (0.02–0.08) | ≈1.0 |
| Naive | ≈0.040 (꼬리 0.115) | ≈2.0 (꼬리 16.5) | ≈**0.075** (꼬리 **0.24**) | ≈1.6 (꼬리 5.6) |
| LoRA | ≈0.034 (꼬리 0.10) | ≈2.0 (꼬리 18) | ≈**0.065** (꼬리 0.17) | ≈1.8 (꼬리 3.5) |
| **Pseudolabel replay** | ≈**0.030** (꼬리 0.10) | ≈**1.6** (꼬리 11) | ≈**0.042** (0.02–0.07) | ≈**1.0** (0.5–1.6) |
| PS+LoRA | ≈0.032 | ≈2.0 (꼬리 15) | ≈0.070 (꼬리 0.125) | ≈2.0 (꼬리 7) |

`figure-read ≈` — `Fig. 7b` 와 `Fig. 17` 우하단을 대조해 읽었다(두 그림이 같은 데이터를 다르게 그린 것).
본문 서술: *"모든 방법이 other-argyrodite 에서 파운데이션 대비 개선되고, **replay 계열이 더 먼 non-argyrodite
셋에서 최선의 전이**를 준다."* ⇒ **판독과 일치한다.**

🔴🔴 **여기서 나오는 세 문장이 우리 판정의 핵심이다:**
1. **500 구성 fine-tune 의 이득은 작다** — 다른 argyrodite 힘 MAE ≈0.043 → ≈0.030 (**약 30%**),
   에너지는 ≈1.8 → ≈1.6 meV/atom (**거의 없음**).
2. **naive/LoRA 는 더 먼 계를 "망가뜨린다"** — 비-argyrodite 힘 MAE 가 파운데이션보다 **나빠진다**
   (≈0.045 → ≈0.075, **1.7배**; 최악 꼬리는 0.08 → 0.24, **3배**).
3. **약한 파운데이션이면 그 파괴가 훨씬 크다** (`Fig. 17` 좌측 MP0 계열):
   비-argyrodite 힘 MAE 중앙값 MP0-found ≈0.08 → MP0-Naive ≈**0.28** / MP0-LoRA ≈**0.30**,
   **LoRA 꼬리는 ≈1.78 eV/Å** (`figure-read ≈`). ⇒ **약한 파운데이션 + naive fine-tune = 재앙.**
   그리고 **OMat 파운데이션을 그냥 쓴 것(≈0.045)이 MP0 를 최선(Multihead ≈0.09)으로 fine-tune 한 것보다 낫다.**

**결과 ④ lr (Appendix D, `Fig. 13` + `Table 9`) — LPSC 로 직접 잰 것**

| lr | target head E (meV/atom) | target head F (meV/Å) | replay head E | replay head F |
|---|---|---|---|---|
| **1e-4 (권장)** | **0.5** | **18.4** | 6.1 | **23.9** |
| 1e-3 | 0.7 | 18.1 | 41.2 | **217.6** |
| 1e-2 | 1.7 | 30.4 | 772.9 | 963.8 |

🔴 **읽는 법**: lr 1e-3 에서 **표적 힘은 사실상 동일(18.1 vs 18.4)한데 replay head 는 9배 붕괴(217.6 vs 23.9)**.
⇒ *"breadth-maintenance 이점은 표적 과제가 이상 징후를 보이기 훨씬 전에 이미 깨진다."*
**표적 지표만 보고 있으면 replay 가 죽은 것을 모른다.** 우리가 fine-tune 한다면 **replay head 지표를 반드시 같이 찍어야 한다.**

**결과 ⑤ replay 조성 (Appendix E, `Fig. 15`) — LPSC**
- 세 선택: ⓐ OMat24 원소일치 부분표본 ⓑ **무작위 MPTraj 10,000** ⓒ 둘 결합. **셋 다 pseudolabel.**
- **표적 정확도·replay 분포 보존 모두 사실상 동일.**
- Discussion: *"LPSC 벤치마크에서 **MPTraj 10,000 무작위 replay 가, 그 구조들이 OMat24 사전학습 코퍼스 밖에서
  왔음에도**, replay 없는 fine-tune 보다 OOD 성능을 더 개선했다."*
  ⇒ **replay 구조는 "사전학습 데이터"일 필요가 없다. 구조적으로 다양하기만 하면 된다.**
  ⇒ 🔑 **우리가 OMat24 원본을 안 받아도 replay 를 할 수 있다.**

### 12-C. Catastrophic forgetting — 얼마나 깎이고 막을 수 있나 (질문 ③) ★★★

**측정 정의**: fine-tune 후 **OMat test set 에서의 힘 RMSE** (사전학습 분포 정확도의 유지율).

**`Fig. 10a` — SPICE(가장 먼 계), 1 구성/분자 = 19,687 구성**
⚠ **절대값은 §10-1 때문에 인용하지 않는다. 같은 패널의 파운데이션 기준선 대비 배율만.**

| 전략 | 파운데이션 대비 힘오차 배율 (`figure-read ≈`) |
|---|---|
| From-scratch | ≈ **7×10³** |
| **Naive** | ≈ **4×10³** |
| LoRA (r=4) | ≈ 2×10² |
| LoRA (r=16) | ≈ 3×10² |
| **LoRA (r=64)** | ≈ **4×10¹** |
| **Multihead** | ≈ **1.0** (기준선과 사실상 동일) |
| **Pseudolabel** | ≈ **1.3** |
| PS+LoRA | ≈ 4 |

본문: *"Forgetting is most severe in the SPICE setting: with 1 configuration per molecule,
**naive fine-tuning degrades OMat performance by orders of magnitude**, while LoRA provides intermediate
protection and **replay-based methods maintain near-foundation accuracy**."* ⇒ 판독과 일치.

**`Fig. 10b` — ice Ih 학습, 파운데이션 3종(OMat-0-medium / OMat-0-small / MH-1)**
- Naive 는 참조선 대비 **한 자릿수 이상** 위 (OMat-medium 기준 `figure-read ≈` 30–40배).
- LoRA 는 OMat-medium 에서 ≈10배인데 **OMat-small 에서는 오히려 더 크게 무너진다**(≈70배 이상).
  ⇒ **작은 파운데이션일수록 LoRA 보호가 약하다** (같은 rank 가 상대적으로 더 큰 자유도).
- Multihead / MH+LoRA / Pseudolabel 은 **참조선 근처 또는 그 아래**.
  ⚠ 아래로 내려간 것은 *"replay head 가 좁은 원소일치 부분집합(H,O 196구성)에 특화돼 그 부분집합에서
  범용 파운데이션을 이긴 것"* 으로 읽는 것이 자연스럽지만, **논문이 그렇게 설명하지 않는다 — 내 해석이다.**

**막는 법 — 논문의 답 (Conclusion 권고 4·5)**
> *"좁은 응용에는 naive 를 첫 강한 기준선으로 써라. **naive 가 MD 에서 불안정이나 비물리적 거동을 만들면
> multihead replay 를 기본 대안(default fallback)으로 하라.**"*
> *"모델이 fine-tune 분포 밖 배열을 만날 수 있으면 multihead replay(원 라벨이든 pseudolabel 이든)를 써라."*

**⇒ 우리 문제로 번역하면**: UMA 를 argyrodite 에 맞추면 **기존 b₂o₃·comp1·modelc 결과와 다른 모델이 된다** —
이 논문이 그 대가를 **우리 계에서 직접 정량화한 유일한 자리**가 §12-B 결과 ③ 이다:
**비-argyrodite 힘 MAE ≈0.045 → ≈0.075 eV/Å (naive)**, **replay 면 ≈0.042 로 유지**.
🔑 **replay 를 쓰면 "끊김"을 거의 0 으로 만들 수 있다는 것이 이 논문의 답이다** — 학습비용 3–15배를 내고.

### 12-D. b₂o₃ 골격 creep 같은 실패를 forgetting 이 만들 수 있나 (질문 ④의 나머지) ★★

**`Fig. 11` (RSS PES-hole, NaCl fine-tune 모델). 파운데이션 baseline: 0.1 GPa = 8.6% · 50 GPa = 10.0%.**
셀 안에 숫자가 인쇄돼 있어 **판독이 아니라 전사다** (괄호 = 파운데이션 대비 절대 변화 %p):

| 전략 | 0.1 GPa: 5 / 96 / 96(10×) / 1963 구성 | 50 GPa: 5 / 96 / 96(10×) / 1963 |
|---|---|---|
| Scratch | 15.6 / 31.4 / 27.6 / **41.6** | 52.2 / **87.0** / 78.6 / 59.4 |
| **Naive** | 8.0 / 11.0 / 12.2 / **20.2 (+11.6)** | 9.4 / 23.0 / 24.6 / **34.4 (+24.4)** |
| **LoRA** | 7.6 / 14.0 / 18.0 / 14.6 (+6.0) | 7.8 / 21.8 / 38.6 / **57.4 (+47.4)** |
| **Multihead** | 7.4 / 6.0 / 5.2 / **7.6 (−1.0)** | 7.4 / 6.6 / 7.2 / 11.4 (+1.4) |
| **Pseudolabel** | 6.2 / 6.2 / **2.6 (−6.0)** / 7.0 (−1.6) | 7.0 / 7.6 / 7.0 / **8.6 (−1.4)** |
| PS+LoRA | 9.4 / 9.2 / 5.2 / 10.0 | 11.6 / 10.6 / 11.8 / 13.2 |
| Freeze (5) | 16.2 / 42.8 / 49.2 / **49.4 (+40.8)** | 32.2 / 75.4 / **85.2 (+75.2)** / 73.6 |
| Freeze (6) | 9.0 / 8.0 / 10.4 / 9.2 | 10.2 / 8.6 / 23.6 / 13.2 |

🔴 **읽는 법 세 가지:**
1. **replay 없는 방법은 데이터를 늘릴수록 구멍이 는다.** Naive 50 GPa: 9.4 → 34.4%. LoRA 50 GPa: 7.8 → **57.4%**.
   본문: *"models trained on more data develop more holes in the repulsive wall, **even as their in-domain
   accuracy improves**."* ⇒ **"더 많이 학습했으니 더 낫겠지"가 틀린다.**
2. **replay 는 그 추세 자체가 없다.** Multihead/Pseudolabel 은 전 조건에서 파운데이션 수준 또는 그 이하.
3. **고압(50 GPa)에서 훨씬 심하다** — 즉 **압축된/밀집된 배열이 위험 구간**이다.

**우리 실패와의 관계 — 정직하게 셋으로 나눈다:**
- ⭕ **기구가 같은 부분**: b₂o₃ 골격 creep 은 *"pointwise 지표는 멀쩡한데 궤적에서 골격이 물리를 잃는"* 실패였다.
  이 논문의 **`Table 1`**(검증 RMSE 정상 + 100 K MD 50 ps 내 붕괴)과 **`Fig. 11`**(in-domain 정확도 개선 + 구멍 증가)은
  **정확히 그 형태의 실패를 문헌에서 잰 사례**다. ⇒ **"pointwise 지표만 보고 MLIP 를 신뢰하지 않는다"는 우리 규율에
  문헌 근거가 생겼다.**
- ⚠ **기구가 다를 수 있는 부분**: RSS 가 잡는 것은 **단거리 반발벽(원자가 서로 뚫고 들어감)** 이다.
  b₂o₃ creep 은 **골격 강성·상대상안정성** 쪽에 가깝다. **저자 스스로 §Discussion 한계 3 에서
  *"경쟁 상들의 상대안정성이 틀리는 종류의 PES artefact 는 다른 진단이 필요하다"* 고 적었다.**
  ⇒ **`Fig. 11` 이 "우리 creep 을 예측한다"고 쓰면 안 된다.**
- ⛔ **우리 계 수치가 없는 부분**: `Fig. 11`·`Fig. 16` 은 **NaCl 뿐**이다. LPSC 도 했다고 서술만 있고 **그림이 없다**(§10-3).
  ⇒ **황화물의 hole% 는 이 논문에 없다.**

**⇒ 답**: **그렇다, 만들 수 있다 — 그리고 replay 없이 fine-tune 하면 데이터를 늘릴수록 더 잘 만든다.**
단, 우리가 겪은 creep 과 **정확히 같은 축인지는 이 논문으로 확정할 수 없다**.

### 12-E. "UMA fine-tune 이 현실적인가" — 판정 (질문 ⑤ + 우리 좌표)

**필요한 라벨 수 (질문 ⑤)** — 이 논문이 준 실측:

| 계 | fine-tune 구성 수 | 도달 지점 |
|---|---|---|
| **Li₆PS₅Cl (우리 계)** | **500 (PBE, 단일 조성)** | 검증 F RMSE 18.4 meV/Å · E 0.5 meV/atom (`Table 9`) |
| ice Ih (MD 안정성만) | **25** | 100 K 250 ps + 50→800 K 램프 안정 (`Table 1`, **단 reestimated E₀ 일 때만**) |
| aq. NaCl (RDF) | **96 (=10%)** | RDF 가 이미 포화; 963(100%) 로 늘려도 개선 미미 |
| Sɴ2 (NEB 장벽) | **60** (반응물/생성물만) | MP2 장벽 재현. **5 구성**에서는 MH+LoRA 만 성공 |
| SPICE | 19,687 (1/분자) ~ 855,905 | 목표정확도별 |

⇒ **우리 규모 = DFT 100–500 점.** `db/properties/mlip_bench_li3ps4_uma.json` 의 규모(243 구조)와 **같은 자릿수**다.
   ⚠ 다만 그 셋은 **Cl 이 없다**(`elements: [Li,P,S]`) — LPSCl fine-tune 라벨로 그대로 못 쓴다.

**GPU 시간 — ⛔ 이 논문은 답하지 않는다.**
- compute 언급은 **"multihead 가 naive 대비 3–15배"** 한 줄이 전부. **절대 시간·epoch 수·batch 크기 어디에도 없다.**
- 유추 가능한 것 둘: (ⓐ) *"Li 모델은 **NVIDIA A100** 에서 학습"* (나머지는 GH200/MI300A)
  ⇒ **A100 1장으로 되는 규모**라는 것. (ⓑ) `Fig. 12` 의 2단계 전환이 **epoch 500** 이고 그 뒤로도 곡선이 이어짐
  ⇒ **수백~1000 epoch** 규모. 500 구성 × 수백 epoch × 9 M 파라미터 = **A100/A6000 급 1장에서 수 시간~하루** 정도로
  **추정**되지만 **논문 근거가 아니다.**
- 🔴 **우리 gabia(A6000 단일) 는 pw.x 와 UMA 동시 실행 금지**라 학습 중 DFT 를 못 돌린다. kgy(RTX3090) 도 공유다.
  ⇒ **자원 충돌이 실제 병목**이지 "몇 시간이냐"가 아니다.

**★ 판정 — UMA fine-tune 은 이 논문 기준으로 "현실적이지만 지금 우선순위는 아니다"**

| 근거 | 판정 |
|---|---|
| 라벨 규모 500점 | ⭕ **가능**. 우리 캠페인 규모 안 |
| 하드웨어 | 🟡 **가능하나 자원 경합**. A100 급 1장이면 됨 (논문의 Li 계가 A100) |
| 파운데이션 품질 | ⭕⭕ **우리는 이미 최상위 자리**(OMat24 계열). 이 논문의 1번 권고를 이미 충족 |
| **이득 크기** | 🔴 **작다.** 우리 계(=OMat24 핵심영역)에서 500구성 fine-tune 의 이득은 **다른 argyrodite 힘 MAE 30%**, **에너지는 거의 0** |
| **비용(끊김)** | 🔴 **크다.** 비-argyrodite 계 힘 MAE **1.7배 악화** — 우리 +B₂O₃ · Nd–O 계가 그 방향 |
| **아키텍처 이전성** | 🔴 **미검증.** 저자가 *"모든 실험이 MACE"* 라고 명시. **UMA 는 MACE 가 아니다** |
| **E₀ 절차의 이전성** | 🔴 **불명.** MACE 의 E₀ 규약(고립원자 기준 원자화에너지 + 명시적 E₀ 파라미터)이 **UMA 에 그대로 있는지 확인 안 됨** |
| **도구** | 🔴 **MACE 전용.** LoRA·pseudolabel replay·E₀ reestimation 은 **`ACEsuit/mace` 3.15+ 에만** 구현됨. fairchem 에 대응물이 있는지 **미확인** |

**⇒ 결론**: *"UMA 를 fine-tune 하는 것"* 은 **라벨·하드웨어 관점에선 현실적**이지만,
**이 논문의 레시피(LoRA·pseudolabel replay·E₀ reestimation)는 MACE 코드베이스에 묶여 있다.**
그리고 **우리 계는 fine-tune 의 이득이 제일 작은 자리**다.
🔑 **더 방어 가능한 경로는 "UMA 를 그대로 쓰고, fine-tune 이 필요하면 MACE-OMat 으로 갈아타는 것"**이다 —
그러면 이 논문의 레시피가 **그대로** 적용된다. (⚠ 그 대신 우리 기존 UMA 결과와의 연속성이 끊긴다. §12-F)

### 12-F. Snapshot ensemble 재료 — M ≥ 4 를 채울 수 있나 (질문 ⑥) ★★★

> 🔴🔴 **먼저 정직하게**: **이 논문은 snapshot ensemble 을 다루지 않는다.**
> 전문 검색 — `snapshot` **0회** · `ensemble` 은 **NEB(nudged elastic band) 뿐** · `uncertainty` **0회** ·
> `committee` 는 **참고문헌 [11] 제목에만**. 아래는 **논문이 준 설정값에서 우리가 유도한 것**이지
> 논문의 주장이 아니다. **인용할 때 반드시 구분한다.**

**이 논문이 제공하는 것 / 안 하는 것**

| snapshot ensemble 에 필요한 것 | 이 논문이 주나 | 비고 |
|---|---|---|
| 체크포인트를 남기는가 | ⛔ **학습 중 저장 정책을 안 적는다.** 최종 모델만 HuggingFace 배포 | `Data Availability`: *"model checkpoints"* — **중간본인지 최종본인지 불명** |
| 권장 저장 간격 | ⛔ **없다** | — |
| 필요한 멤버 수 M | ⛔ **없다** | — |
| 학습 길이(= 몇 개를 뽑을 수 있나) | 🟡 **간접**: `Fig. 12` 의 2단계 전환이 **epoch 500**, 곡선은 그 뒤로 이어짐 | ⇒ **수백~1000 epoch** ⇒ 100 epoch 간격이면 **5–10 멤버**, `kurniawan` 의 간격(100 epoch)과 호환 |
| 시드 반복을 하는가 | 🟡 **일부**: aq. NaCl 만 **seed 1–3** (`Table 4`, *"mean ± std over seeds 1–3"*) | ⇒ **3-시드 fine-tune 이 실제로 돌아간 규모**라는 증거 |
| 체크포인트 다양성을 방해하는 요소 | 🔴🔴 **있다 — EMA** | 아래 |

**🔴 핵심 발견 (내 유도, 논문 주장 아님): EMA decay 가 snapshot ensemble 과 정면으로 충돌한다.**
- `Table 7`: naive **EMA 0.999**, **multihead/pseudolabel EMA 0.9999**.
- EMA 0.9999 는 대략 **최근 10⁴ 스텝의 평균**을 모델로 쓴다는 뜻이다.
- snapshot ensemble 의 전제는 *"학습 궤적이 서로 다른 극소점 근처를 지나가고, 그 스냅샷들이 **서로 다르다**"* 인데,
  **EMA 는 정확히 그 차이를 평균으로 지워버린다.**
- ⇒ **이 논문의 권장 설정을 그대로 쓰면 snapshot 멤버들이 서로 거의 같아진다** — M 은 채워도 **유효 M 은 1 에 가깝다.**
- ⇒ **snapshot ensemble 을 하려면 (ⓐ) raw(비-EMA) 가중치를 따로 저장하거나 (ⓑ) EMA 를 낮추거나
  (ⓒ) 시드를 바꿔 독립 학습해야 한다.** 그리고 (ⓑ) 는 **이 논문이 명시적으로 반대**하는 방향이다
  (EMA 를 올리는 것이 *"안정적이고 잘 수렴하는 naive fine-tuning 에 필수"*).
  🔴 **즉 "정확도를 위한 설정"과 "UQ 를 위한 설정"이 여기서 충돌한다. 이건 우리가 새로 발견한 긴장이고,
  세 UQ 논문에도 이 논문에도 없다.**

**M ≥ 4 를 채우는 세 경로 (전부 우리 유도)**

| 경로 | M | 이 논문이 뒷받침하는가 | 위험 |
|---|---|---|---|
| **① 시드 다중 fine-tune** (같은 데이터, 다른 초기화/셔플) | **원하는 만큼 (≥4 쉽다)** | 🟡 **간접 — NaCl 에서 seed 1–3 을 실제로 돌렸다** (`Table 4`) | 학습 M배. **다만 파운데이션이 같으니 다양성이 deep ensemble 보다 작다** — `carrete2023_deep_ensembles_vs_committees` 와 대조 필요 |
| **② snapshot (단일 학습 궤적)** | 학습길이/간격 (100 epoch 간격이면 5–10) | ⛔ **없다.** + **EMA 가 방해** | 유효 다양성이 과소. **raw 가중치 별도 저장 필요** |
| **③ LoRA rank/시드 다중** (파운데이션 공유, 어댑터만 다름) | 원하는 만큼 | ⛔ 없다 | **몸통이 완전히 동일**하므로 다양성이 제일 작다. 대신 **저장이 파라미터의 2.5%** 라 제일 싸다 |

**⇒ 답 (질문 ⑥)**: **M ≥ 4 는 채울 수 있다 — 단 이 논문이 그 방법을 말해 주지는 않는다.**
가장 방어 가능한 경로는 **① 시드 다중 fine-tune** 이고, 이 논문이 주는 뒷받침은
*"NaCl 에서 3-시드가 실제로 돌아갔고, 시드 간 std 가 평균의 10–12% 수준"*(`Table 4`: 42.44±5.28 · 43.79±5.03 · 41.54±4.76)
이라는 **비용·산포 감각뿐**이다.
🔴 **그리고 그 std 는 "UQ 용 σ"가 아니라 "재현성 산포"다 — Grasselli 식 (27) 의 α² 캘리브레이션에 넣으려면
멤버가 **동일 분포에서 독립 추출**이어야 하는데, 시드만 다른 fine-tune 이 그 조건을 만족하는지
**이 논문도 그 세 UQ 논문도 판정하지 않았다.**

### 12-G. 우리가 **지금 당장** 할 수 있는 것 (fine-tune 없이)

이 논문에서 fine-tune 을 하지 않고도 가져올 수 있는 것 4가지:

1. **★ RSS PES-hole 진단을 UMA 에 그대로 돌린다** (Appendix A.5, DFT **0회**).
   PyXtal 로 Li–P–S–Cl(+B,O,Nd) 조성 10종 × 50 구조 = **500 구조**, relax–rattle 3회, 4기준 판정.
   ⇒ **"우리 UMA 가 우리 계에서 구멍이 몇 %인가"** 라는, 지금 답이 없는 질문에 답이 나온다.
   그리고 그것이 **b₂o₃ 마감 사유의 사후 진단**이 될 수 있다.
   ⚠ **보고량 카드 먼저** (`kb/templates/estimand_card.md`) — 새 물리량이다. 판정기준(4기준 문턱)을 **결과 보기 전에** 고정.
2. **MD 안정성 프로토콜을 표준화한다** (`Table 1` 판정 방식): ①정온 **250 ps** 완주 ②**50→800 K 램프 50 ps**.
   우리 MSD 창(2–50 ps)보다 훨씬 긴 완주 시험이다 — **b₂o₃ creep 을 잡았을 시험**.
3. **`Fig. 3a` 식 파운데이션 비교를 우리 committee 로 재해석한다.**
   우리 이종 committee(UMA-OMat24 / MACE-MP-0-MPtrj / SevenNet-0-MPtrj)의 산포는
   이 논문 기준으로 **"OMat24 계열 1개 + MPTraj 계열 2개"** 의 차이를 포함한다.
   `Fig. 3a` 는 **그 두 계열이 우리 계에서 힘 MAE 로 ≈2–3배 차이난다**고 말한다(`figure-read ≈` 0.105 vs 0.045).
   🔴 ⇒ **우리 committee σ 의 상당 부분이 "epistemic 불확실도"가 아니라 "사전학습셋 계통차"다.**
   `kurniawan` digest 가 이미 경고한 것에 **이 논문이 수치를 준다.**
4. **E₀ 정합성을 점검한다** — 우리가 UMA 로 계산한 에너지를 우리 DFT 와 섞어 쓰는 자리가 있는지.
   `mlip_bench_li3ps4_uma.json` 은 이미 **선형 원소보정**(Li 0.09312 / P 0.03104 / S 0.12416 eV/atom, fit R² 0.620)을 쓰는데,
   이것이 이 논문이 **"쓰지 말라"고 한 averaging 방식**이다(식 5).
   🔴 **그리고 그 R² = 0.620 이 낮다는 것 자체가 averaging 의 한계를 보여준다.**
   ⇒ **model-aware reestimation(식 6)으로 바꾸면 개선될 수 있다** — 그 식은 아키텍처 무관하므로 UMA 에도 적용 가능하다.
   **이것이 이 논문에서 우리가 즉시 이식 가능한 유일한 수식이다.**

---

## 13. ⛔ 이 digest 가 **못 하는 것 / 확인 못 한 것**

1. **동료심사 안 된 preprint 다.** 게재본에서 수치·그림이 바뀔 수 있다. 특히 §10-1(축 단위)·§10-2(Freeze 라벨).
2. **그림 29장 중 7장만 봤다** (`Fig. 1, 3, 4, 7, 10, 11, 17`). 안 본 13장은 §5.1 에 목록.
   표 9장은 **PDF 텍스트로 읽었고 이미지로는 안 봤다**(관례).
3. **`Fig. 10` 의 절대값을 인용할 수 없다** — 패널 a/b 의 단위가 1000배 어긋난다(§10-1). **비율만** 썼다.
4. **`Fig. 3a`·`Fig. 4a`·`Fig. 7b`·`Fig. 17` 의 수치는 전부 `figure-read ≈` 다.**
   본문에 숫자가 없다(순위·정성 서술만). violin 중앙부 판독이라 **±10–20% 오차를 가정**해야 한다.
   `Fig. 11`·`Table 9` 만 **인쇄된 숫자**다.
5. **LPSC 500 구성의 정체를 모른다** — 샘플링 방법·온도·**Cl/S 부분점유 처리**가 전부 미기재.
   우리 계의 핵심 자유도(무질서)를 이 논문이 어떻게 다뤘는지 **알 수 없다**.
6. **비-argyrodite 평가셋의 N 과 조성을 모른다.** §12-B 결과 ③ 의 제일 무거운 숫자가 거기서 나온다.
7. **우리 계의 PES-hole 수치가 없다** — `Fig. 11`·`Fig. 16` 은 NaCl 뿐(§10-3).
8. **GPU 시간·epoch 수·batch 크기가 논문에 없다.** §12-E 의 시간 추정은 **추정이지 인용이 아니다**.
9. **snapshot ensemble·UQ 는 이 논문에 없다.** §12-F 는 전부 **우리 유도**다.
   특히 **"EMA 가 snapshot 다양성을 지운다"** 는 **내 논증이지 논문의 주장이 아니다** — 검증이 필요하다.
10. **UMA 로의 이전성을 확인 못 했다.** 저자가 *"모든 실험이 MACE"* 라고 명시했고,
    (ⓐ) UMA 가 명시적 E₀ 파라미터를 갖는지 (ⓑ) fairchem 에 LoRA/multihead replay 대응물이 있는지
    (ⓒ) UMA 의 task-head 구조(omat/omol/…)가 이 논문의 multihead 와 같은 것인지 —
    **셋 다 이 세션에서 확인하지 않았다.** ⚠ (ⓒ)는 특히 흥미로운데, **UMA 는 이미 multihead 구조일 수 있다**
    (task 별 head). 그렇다면 replay 를 붙이기가 오히려 쉬울 수 있다 — **미확인 가설**.
11. **`Fig. 10b` 에서 multihead 가 참조선 아래로 간 이유를 논문이 설명하지 않는다.** §12-C 의 해석은 내 것이다.
12. **`db/` 를 수정하지 않았다.** 이 논문 수치는 **전부 소환값**이며 우리 레지스트리에 넣지 않았다.
13. **동시작업 충돌 회피로 `INDEX.md`·`comparison_vs_ours.md` 를 직접 안 고쳤다** →
    `litdb/_pending_index_tompa2026_finetuning_mlip_foundation_strategies.md` 에 반영분을 넣어 뒀다.
14. **git 명령을 실행하지 않았다** (요청에 따라).

## 14. 🎤 talk 역링크 — **해당 없음** (단, 주제 인접 기록)

`grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `talks/lee2026_skku_mlip_materials_design.md` 하나.
그 §99-10 대기열(#1–9)을 확인했고 **이 논문은 대기열에 없다.** ⇒ **talk 파일을 건드리지 않았다.**

> 다만 주제 인접성은 기록해 둔다 (**옮길 때 talk 에 넣지 말 것 — 대기열 밖이고, 그 talk 은 `citable=no`**):
> 그 덱의 **슬 8 "MLIP PES softening → fine-tuning"** 개념도 —
> *"DFT PES → uMLIP PES 로 갈 때 softening 이 일어나고 fine-tuning 으로 되돌린다,
> 훈련점이 near-equilibrium 에 몰려 있어 high-energy state 를 augment 해야 한다"* —
> 가 **이 논문의 정확한 주제다.**
> 🔴 **그리고 이 논문은 그 명제를 부분적으로 뒤집는다**: `Fig. 11` 은 **fine-tuning 이 (replay 없이 하면)
> 고에너지 영역을 오히려 **더** 망가뜨린다**고 보여준다 (데이터 늘릴수록 PES hole 증가).
> 덱의 "fine-tuning 으로 되돌린다"는 **replay 를 붙였을 때만** 성립한다.
> ⚠ talk 의 §12/§99 에 정정으로 넣을지는 **대기열 담당 세션이 판단할 일**이다 — 나는 안 건드렸다.
