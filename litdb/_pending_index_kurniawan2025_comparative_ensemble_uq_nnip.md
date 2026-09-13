# ⏳ pending — `kurniawan2025_comparative_ensemble_uq_nnip` 의 INDEX / comparison 반영분
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 2026-09-09, litdb-curator. **동시작업 충돌 회피**로 `INDEX.md` · `comparison_vs_ours.md` 를 직접 안 고쳤다.
> 아래 두 블록을 **사람이(또는 조율 담당 세션이) 그대로 옮겨 붙이면 된다.**
> digest 본체: `litdb/papers/kurniawan2025_comparative_ensemble_uq_nnip.md`
> 그림: `litdb/figures/kurniawan2025_comparative_ensemble_uq_nnip/` (13장)

---

## ① `litdb/INDEX.md` — **`## ✅ Digest 완료 (paper-level)`** 표에 추가할 행

```markdown
| `papers/kurniawan2025_comparative_ensemble_uq_nnip.md` | **[외부·methods·★MLIP UQ 벤치마크 · ⚠slug 연도 오기(실제 2026)]** **Y. Kurniawan** (BYU 물리→U Toronto MSE), **M. Wen** (UESTC), **E. B. Tadmor\*** (UMinnesota), **M. K. Transtrum** (Cross Stream Consulting), "**Comparative study of ensemble-based uncertainty quantification methods for neural network interatomic potentials**" (***Mach. Learn.: Sci. Technol.* 2026, in press**, DOI `10.1088/2632-2153/ae9fb4` · 원고 `MLST-105722.R1` · Accepted Manuscript CC BY 4.0 · 본문 17 pp + refs · **SI 별도(우리 미보유)** · 코드 `github.com/yonatank93/compare_UQ` · NSF DMR-1834251/1834332) — **탄소 동소체 NNIP 의 UQ 방법론 논문. 물성값 0건**(전문 검색 `battery`·`lithium`·`sulfide` **각 0회**, `Li` 는 **참고문헌 저자 성으로만 4회**; 계는 graphene/bilayer/graphite/**diamond** 뿐). **질문**: *"σ(앙상블 산포)를 정확도의 대용으로 써도 되나."* **답**: **ID 는 되고 OOD 는 안 된다 — 그것도 직관 반대 방향으로.** **비교 대상 4종**(각 **S=100 멤버**, **사후보정 일부러 안 함**): ①**bootstrap**(구성 단위 복원추출, **이 논문이 KLIFF 에 구현 추가**) ②**MC dropout**(추론 시 마스크, 학습 1회) ③**random initialization**(=deep ensemble/committee, 학습 100회) ④**snapshot**(단일 학습 궤적, burn-in 후 **100 epoch 간격**, 학습 1회). ⛔ **GP·conformal·mean-variance·quantile·Bayesian NN 은 서론 언급뿐 — 비교 안 함**. **모델**: MLP 3층×128, **tanh**, **ACSF** 기술자, dropout p=0.1 정칙화, Adam batch 100, lr 1e-3(5k epoch)→1e-4(35k), **총 40k epoch**; 라벨 = **PBE**(bilayer/graphite 만 **MBD**), cutoff **500 eV**, 진공 ~30 Å, Γ-centered MP(격자 미기재), **코드 미기재**; 데이터 **4,788 구성**(train 4,344/test 444; diamond 759·graphite 661·monolayer 2,181·bilayer 743) = Wen&Tadmor 2020 figshare 재사용. **★★ 채점 지표 5종 = 우리가 이 논문에서 가져올 본체**: **M1** 잔차-σ 패리티 log-log + KDE + "underconfident" 회색삼각(`Fig. 6`) · **M2** `Pearson(residual, σ)`(`Fig. 7a`) · **M3** MAE vs ⟨σ⟩ 병렬(`Fig. 7b`) · **M4** DFT 참값이 ±1σ 안인가(`Fig. 8`) · **M5** ★ **오차곡선 vs σ띠를 외삽좌표에 겹치고 PCA 내삽영역을 음영**(`Fig. 11`·`Fig. 13`) . ⛔ **NLL·sharpness·ECE·reliability diagram·AUROC·conformal 전부 0건**. **🔑 정량 소득**: `Fig. 7a` Pearson **all-data bootstrap 0.76 vs dropout 0.40 / random-init 0.32 / snapshot 0.30**(구조별 bootstrap 0.69–0.81, 나머지 0.30–0.63 — **bootstrap 이 5행 전부 1위**) 인데 `Fig. 7b` 는 **정반대**: bootstrap 힘 **⟨σ⟩ ≈ MAE/3**(all-data figure-read ≈0.65 vs 2.05 meV/Å/atom) = **최악의 과소확신**, dropout 은 **⟨σ⟩ ≥ MAE**(보정 최선) ⇒ 🔴 **같은 데이터에서 두 지표가 우승자를 반대로 뽑는다 = "지표 하나로 UQ 를 채점하지 말라"의 정량 근거**. **Table 2 ID RMSE**: E(test) bootstrap **9.204** 최악 / random-init 6.164 최선, F(test) bootstrap **3.350** 최선 / dropout 5.559 최악 — **저자가 이 역전을 "not investigated further"로 포기**. **비용**: 벽시계·GPU 시간 **0건**(정성만) — 유일한 결론 = ***"snapshot ≈ random init 인데 학습은 1회 vs 100회"***(추론은 넷 다 ×100). **★★★ 핵심 음성결과**: `Fig. 13`(bootstrap·graphene) σ = 내삽영역 **0.004 eV** → 경계 바로 밖 `a≈2.29 Å` **0.030(최대)** → 더 먼 `a=2.0 Å` **0.0145** ⇒ **σ 가 외삽 거리를 따라가지 않고 감소한다**; `Fig. 11` diamond 은 오차 **0.2–0.3 eV/atom** 인데 σ **≈±0.02** (10배 이상 과소확신). **`Fig. 8`** diamond 인장에서 dropout/random-init/snapshot 의 `E(a)` 가 **평탄해짐(비물리)**, 예측 a_eq ≈3.60–3.65 vs MP 3.567; graphene/graphite 는 a_eq ≈2.46–2.47 로 정확. **`Fig. 9` PCA**(상위 2 PC = 분산 **98 %**)가 **σ 가 아니라 이것이** diamond 붕괴를 외삽으로 설명 — **σ 없이 작동한 유일한 OOD 탐지기**. **`Fig. 10`** dropout p 0.1→0.8 스캔: p↑ 로 σ 확대·인장 개선하나 **압축 오차는 불변**(0.30→0.20), **p=0.8 은 예측이 수평선(학습실패)인데 σ 가 0 으로 붕괴** = *"UQ 는 모델이 망가진 것을 못 알려준다"*. **`Fig. 12` SchNet(GNN)에서 같은 병리 재현** ⇒ 아키텍처 특이 아님(단 저자 *"do not imply a general rule"*). **⚠⚠ 의뢰 전제 정정**: *"복잡한 추정기가 단순 committee 를 일관되게 이기지 못했다"* 는 **이 논문 초록이 아니라 서론이 인용한 [37] Carrete 2023**(*J. Chem. Phys.* 158, 204801)의 결론이고, *"어려운 배열 식별(OOD 탐지·능동학습)"* 도 그 편의 것 — **이 논문은 능동학습을 안 하고 AUROC 류를 안 잰다.** 이 논문판 결론은 *"ID 에서 네 방법 차이가 최소이고 최고를 못 정한다"*. **⛔ 한계(저자)**: NNIP 한정·원인 설명 실패(tanh 포화 가설은 **평형점 반례**로 깨짐)·*"코히런트한 학습 이론의 부재"*·bootstrap 의 i.i.d. 위반(MD 연속 스냅샷)·dropout p 에 보편지침 없음·내삽/외삽 경계 모호·사후보정으로도 분포이동 미해결. **⛔ 한계(우리 지적)**: 탄소 단일원소·훈련셋 4,788 로 좁음(**파운데이션 모델 내삽영역과 자릿수 다름**)·**테스트셋으로 모델선택 후 그 테스트셋으로 채점**(낙관편향)·**S 스윕 없음**·오차막대 없음(0.31 vs 0.34 는 유의성 불명, **0.76 vs 0.30–0.40 은 충분히 큼**)·OOD 프로브가 **부피 스캔 한 축**뿐(화학·안장점·계면 미검증)·`Fig. 12` 는 앙상블 종류 **미명시**·**포논은 전부 SI 라 우리가 인용할 숫자 0**. **🔧 우리 좌표**: **단일 UMA 로 지금 되는 것 = `Fig. 9` 식 PCA 외삽 진단(DFT 0회)**, **fine-tune 하면 snapshot 앙상블이 공짜**(체크포인트만 저장); bootstrap·random-init 은 **OMat24 훈련셋이 없어 불가**, MC dropout 은 **UMA 가 dropout 학습이 아니라 조건 불일치**. **★★ `tools/ionic/mlip_committee.py` 매핑**: `analyze`(이종 3모델 힘 RMS 불일치) = **`Fig. 6`·`Fig. 7` 의 x축(σ)**, `force_contrast`(UMA vs DFT 라벨) = **y축(잔차)** ⇒ **같은 프레임에 겹치면 M1·M2·M3·M5 가 전부 나온다**(선결: **Cl 포함 DFT 라벨** — §J-1 4번 한계 그대로, 새 계산이므로 **보고량 카드 먼저**). ⚠ **우리 committee 는 이종 훈련셋(UMA=OMat24 vs MACE-MP-0/SevenNet-0=MPtrj)이라 σ 가 "epistemic + 훈련셋 계통차"의 혼합** — 이 논문 네 방법은 전부 동일 데이터·동일 구조라 그 항이 없다 ⇒ **σ 해석을 그대로 옮기면 안 된다**. **⚠⚠ 보고량 간극**: 이 논문은 **힘·에너지 + 0 K 유도량(cold curve·phonon)에서 멈춘다. MD 를 한 번도 안 돌린다** ⇒ **우리 보고량인 궤적 시간평균 `D`(MSD 2–50 ps)·`Ea`·NE `σ_ionic` 로의 전파는 이 논문에 없다** → **자매편 `imbalzano2021_committee_uq_md_thermodynamic_averages` 가 정본**. 부분 다리 하나: diamond **포논에서 "wide uncertainty bounds fail to capture the true values"** = *"힘 σ 가 괜찮아도 유도량에서 깨진다"* 의 **정성 경고로만** 인용 가능. ⛔ **물성 4축(A/B/C/D) 편입 금지** — σ·ESW·탄성·gap **0건** → `comparison_vs_ours.md` **§J-7 `🔧 방법 원전`** 에만. ⛔ **힘 RMSE 3.35–5.56 meV/Å(탄소·ACSF-MLP·PBE)를 우리 UMA Li₃PS₄ 30.0 meV/Å(황화물·등변 GNN·PBEsol)와 같은 표에 놓지 말 것** — 단위만 같다 | **방법론(MLIP UQ 채점 지표)·T1(외삽 대리지표 채점)** — 물성값 0, 탄소 전용 |
```

**⚠ INDEX 행에 같이 반영할 것**
- `## ✅ Digest 완료` 표의 **자매편 행**(`imbalzano2021_…`, 다른 curator 가 작성 중)이 들어오면
  두 행에 **상호 참조**를 넣는다: 이 편 = *"힘·에너지 층위"*, imbalzano = *"궤적 시간평균 층위"*.

---

## ② `litdb/comparison_vs_ours.md` — **§J-0 출처표** 에 추가할 줄

```markdown
| **[Kurn26UQ]** 🔧 | `kurniawan2025_comparative_ensemble_uq_nnip` — **MLIP 앙상블 UQ 벤치마크** (*MLST* 2026, in press, DOI 10.1088/2632-2153/ae9fb4). ⚠ **물성값 0 · 탄소 동소체 전용** → 아래 **J-7** 에만 등장, A–D 축 금지. ⚠ slug 의 `2025` 는 오기 — **인용은 2026** |
```

---

## ③ `litdb/comparison_vs_ours.md` — **§J-7 `🔧 방법 원전`** 에 추가할 블록

```markdown
**[Kurn26UQ] `kurniawan2025_comparative_ensemble_uq_nnip` — UQ 를 *채점하는 지표* 의 원전**
(*Mach. Learn.: Sci. Technol.* **2026**, in press · Kurniawan/Wen/**Tadmor**/Transtrum · **탄소 동소체 전용 · 물성값 0**)

> 🔑 **우리가 이 편에서 가져오는 것은 값이 아니라 "채점표"다.** 지금 우리에게는
> **committee 불일치를 채점할 지표가 하나도 없다** — 이 논문이 그 다섯 개를 준다.

| 항목 | [Kurn26UQ] | 우리 (`tools/ionic/mlip_committee.py`) | 판정 |
|---|---|---|---|
| **σ(불확실도)의 정의** | **동일 아키텍처·동일 데이터** 앙상블 100멤버의 표준편차 (bootstrap/dropout/random-init/snapshot 4종) | **이종 3모델**(UMA-OMat24 / MACE-MP-0-MPtrj / SevenNet-0-MPtrj) 프레임별 원자당 힘 RMS 불일치의 **쌍별 최댓값**, 평균 힘 크기로 정규화 | ⚠ **부류가 다르다** — 우리 것은 ③ random-init 의 **일반화판**(변동 출처 = 아키텍처+훈련셋). ⇒ 우리 σ 는 **epistemic + 훈련셋 계통차의 혼합**이고 이 논문에는 그 항이 없다. **σ 해석 직수입 금지** |
| **잔차(정확도)의 정의** | DFT 라벨 대비 에너지·힘 residual/MAE/RMSE | `force_contrast`: UMA vs DFT 라벨, 골격 `dF_frame`·상대 `dF/F_ref`·`cos θ` | ⭕ **같은 축이다** |
| **M1 패리티 도식** | `Fig. 6`: y=|오차|, x=σ, **log-log**, KDE 등고, **회색 삼각 = underconfident** | ⛔ **없다** | ⭕⭕ **T1 이식 1순위** — `analyze` 와 `force_contrast` 산출 JSON 을 **프레임 키로 조인**하면 새 도구 없이 그려진다 |
| **M2 순서 지표** | `Pearson(residual, σ)`. **all-data: bootstrap 0.76 / dropout 0.40 / random-init 0.32 / snapshot 0.30** | ⛔ **없다** | ⭕⭕ **우리 값의 눈금이 생긴다.** 우리 committee 가 0.3 대면 *"이 논문의 약한 방법들과 동급"*, 0.7 대면 *"bootstrap 급"* |
| **M3 크기(보정) 지표** | `MAE` vs `⟨σ⟩` 병렬. bootstrap 힘 **⟨σ⟩ ≈ MAE/3 = 과소확신**, dropout **⟨σ⟩ ≥ MAE = 보정 양호** | ⛔ **없다** | ⭕⭕ **M2 와 우승자가 반대로 나온다** ⇒ 우리도 **둘 다** 봐야 한다. 하나만 보고 *"우리 σ 는 쓸 만하다"* 라고 쓰면 이 논문이 이미 반증한 종류의 주장 |
| **M4 coverage** | DFT 참값이 ±1σ 안인가 (`Fig. 8`, 정성) | ⛔ 없다 | 🟡 우리는 참값이 드물어 적용 제한 |
| **M5 외삽 추적** | ★ **오차곡선 vs σ띠를 외삽좌표에 겹치고 PCA 내삽영역을 음영** (`Fig. 11`·`Fig. 13`) | ⛔ 없다 | ⭕⭕⭕ **우리 판 = x축을 온도(600/800/1000 K) 또는 PCA 거리로.** *"σ 가 고온 외삽을 따라가는가"* — **§J-2 [Zhang npj] 1050 K 골격융해 경고의 감시 지표** |
| **사후 보정** | **일부러 안 함** (raw ensemble spread) | 해당 없음 | ⚠ 우리도 raw 로 시작하되 **"보정 안 했다"를 명시** |
| **비용 보고** | ⛔ 벽시계·GPU 시간 **0건**. 정성 결론 하나: **snapshot ≈ random-init 인데 학습 1회 vs 100회** | 추론 3회(3모델) | ⭕ **fine-tune 하면 snapshot 이 공짜** — 체크포인트 저장 한 줄 |
| **단일 파운데이션 모델 적용성** | 논외(4종 다 자체 학습) | **UMA 단일** | 🔴 **bootstrap·random-init 불가**(OMat24 훈련셋 부재) · **MC dropout 조건 불일치**(UMA 는 dropout 학습 아님) · **snapshot = fine-tune 시 가능** · **PCA 외삽 진단 = DFT 0회로 지금 가능** |

**🔴 이 편이 닫지 못하는 것 — 반드시 같이 인용**
1. **계가 탄소 단일원소**다. 다원소·이온성·**부분점유 무질서**계로의 전이는 **시험된 적 없다**.
2. **훈련셋 4,788구성**으로 좁다 ⇒ 파운데이션 모델의 내삽영역과 **자릿수가 다르다**.
   기구(외삽하면 σ 가 먹통)는 전이 가능성이 있어도 **빈도·문턱은 전이되지 않는다**.
3. **MD 를 안 돌린다** ⇒ **궤적 시간평균 `D`·`Ea`·NE `σ_ionic` 의 UQ 를 다루지 않는다.**
   → **`imbalzano2021_committee_uq_md_thermodynamic_averages` 가 그 층위의 정본.**
   ⚠ 부분 다리: diamond **포논**에서 *"wide uncertainty bounds fail to capture the true values"*
   = *"힘 σ 가 괜찮아도 유도량에서 깨진다"* — **정성 경고로만**, 정량 이식 금지.
4. **OOD 프로브가 부피 스캔 한 축**뿐. **우리 위험(고온 무질서·Li 도약 안장점·계면)을 대표하지 않는다**
   ⇒ `E(a)` 스캔을 LPSCl 로 그대로 베끼면 안 된다(그리고 무질서계는 **배열 선택·집계 규칙을 카드에 먼저** 선언).
5. **오차막대가 없다.** `Fig. 7a` 의 0.31 vs 0.34 차이는 유의성 불명. **0.76 vs 0.30–0.40 만 인용한다.**
6. **테스트셋으로 모델을 선택하고 그 테스트셋으로 채점**했다(검증셋 없음) ⇒ ID 성능에 낙관편향.

**⛔ 이 축에서 인용하면 안 되는 것 (→ §J-6 에도 추가)**
- ⛔ *"이 논문이 committee(단순 앙상블)가 제일 낫다고 했다"* — **아니다. 승자를 못 정했다.**
  *"복잡한 추정기가 단순 committee 를 일관되게 못 이긴다"* 는 **[37] Carrete 2023** (*J. Chem. Phys.* 158, 204801)
  의 결론이고 이 논문은 그걸 **인용**했을 뿐이다.
- ⛔ *"이 논문이 GP·conformal 과 비교했다"* — **앙상블 4종만.**
- ⛔ *"이 논문이 D·이온전도도의 UQ 를 다뤘다"* — **MD 를 안 돌린다.**
- ⛔ **힘 RMSE 3.35–5.56 meV/Å**(탄소·ACSF-MLP·PBE)를 **우리 UMA Li₃PS₄ 30.0 meV/Å**(황화물·등변 GNN·PBEsol)
  와 같은 표에 놓는 것 — **단위만 같고 계·기술자·functional 이 전부 다르다.**
```

---

## ④ 🎤 talk 역링크 — **해당 없음**

`grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `talks/lee2026_skku_mlip_materials_design.md` 하나.
그 §99-10 대기열 9건(Kim hydrolysis / 자료집 / Shapeev / Gubaev / Podryabinkin / Novikov / MLIP-3 /
Merchant GNoME / Park SevenNet / Luo cryoTEM / Shin BH₄ / Kim GA / KimYS moisture) 을 확인했고
**이 논문은 대기열에 없다.** ⇒ **talk 파일을 건드리지 않았다.**

> 다만 주제 인접성은 기록해 둔다 (**옮길 때 talk 에 넣지는 말 것 — 대기열 밖이다**):
> 그 talk 의 **MTP `γ`(외삽등급, 선형기저 위 maxvol/D-optimality)** 와 이 논문의 **앙상블 산포**는
> **"외삽 감시"라는 같은 문제의 서로 다른 해법**이다. 우리 `mlip_committee.py` docstring 이
> 이미 그 논지를 세워 뒀고, 이 논문은 거기에 **"그런데 그 대리지표를 어떻게 채점하나"** 를 보탠다.

---

## ⑤ 이 curator 가 **하지 않은 것** (조율 담당이 확인할 것)

- ⛔ `litdb/INDEX.md` 미수정 (위 ① 를 옮겨야 함)
- ⛔ `litdb/comparison_vs_ours.md` 미수정 (위 ②③ 를 옮겨야 함)
- ⛔ `db/` 미수정 · git 명령 미실행
- ⛔ `litdb/talks/` 미수정 (대기열에 없어 해당 없음)
- ⚠ **slug 연도 오기**(`2025` ↔ 실제 2026)를 **고치지 않았다** — 동시작업 조율 키라서.
  나중에 정리한다면 `kurniawan2026_comparative_ensemble_uq_nnip` 로 rename + `figures/` 폴더명 +
  `figures/_sources.json` 항목까지 같이 옮겨야 한다.
