# 📥 PENDING — `carrete2023_deep_ensembles_vs_committees` 인덱스/비교 반영 대기
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션) — 변형: `|F|` → `\|F\|` 이스케이프; 4열 → 3열 (3·4열을 " · " 로 합침, 내용 손실 없음). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 작성 2026-09-09 · litdb-curator (동시 4개 실행 중이라 `INDEX.md`·`comparison_vs_ours.md` 직접 편집 금지)
> **이 파일을 사람이 확인한 뒤 아래 3덩이를 각각 옮겨 붙이고, 이 파일을 지운다.**
>
> ⚠ **같은 다발 4편**: 오늘 MLIP 불확실도 논문이 함께 들어왔다 —
> `#78 imbalzano2021_committee_uq_md_thermodynamic_averages` · **`#79 = 이 편`** ·
> `#80 kurniawan2025_comparative_ensemble_uq_nnip` · `#81 grasselli2025_uncertainty_era_ml_atomistic`.
> **2026-09-09 확인**: 형제 3편의 pending 파일은 전부 **`J-7`(방법 원전)** 에만 붙이고 있고
> **`J-11` 을 잡은 편은 없다** ⇒ 아래 §2-c 의 절 번호는 지금 비어 있다.
> 다만 **병합하는 사람이 네 편을 J-11 한 절로 모으는 편이 낫다** — 넷이 같은 질문
> ("MLIP 예측을 얼마나 믿나")에 답하는데 J-7 에 흩어 두면 축이 안 보인다.

---

## 1. `INDEX.md` — 붙일 위치: `## 🤖 MLIP 방법론 — **우리 UMA 스택을 재는 축** (2026-08-19 신설)` 표 (line ~383)

| `papers/carrete2023_deep_ensembles_vs_committees.md` **(본문 19 pp + Zenodo 배포 데이터 3종 전수 검산)** | **[외부·methods·⛔물성 4축 아님·★불확실도 추정기 원전]** **Jesús Carrete\***/H. Montes-Campos/R. Wanzenböck/**Esther Heid**/**Georg K. H. Madsen** (TU Wien + USC Santiago + U. Porto), "**Deep ensembles vs committees for uncertainty estimation in neural-network force fields: Comparison and application to active learning**" (***J. Chem. Phys.* 158, 204801 (2023)**, DOI 10.1063/5.0146905, **OA CC BY**, JCP Special Topic; 데이터·코드 Zenodo `10.5281/zenodo.7643625`). **질문**: NNFF 불확실도를 committee 말고 더 좋게 잴 수 있나. **답 = 없다(대체로).** 다중 헤드 + heteroscedastic loss 로 **deep ensemble 을 NNFF 에 일반화**(σ²_E 헤드 = 원자합 · σ²_f 헤드 = 원자별 등방)했지만, **같은 양을 잴 때 단순 committee 대비 체계적 이점 없음**. `Table I` EAN: committee **1.16 meV/atom · 63.3 meV/Å** > deep ensemble 1.75 · 65.0 (원래 NeuralIL 1.86 · 65.6). STO bulk: 불확실도–오차 **Spearman committee 0.90 ≈ bootstrap 0.91** → 싼 committee 채택 (MAE_f 115.91 meV/Å, test MAD 2.23 eV/Å 대비 **5.2 %**). **⭐ 이론적 핵심(Appendix)**: **힘의 분산은 에너지 분산에 미분 연산자를 적용해 얻을 수 없다** — `σ²_f = ∂²⟨δE(X)δE(Y)⟩/∂X∂Y|_{X=Y}` 로 **두 점 공분산**이 필요한데 Behler–Parrinello 류 set-pooling 은 한 점만 예측하므로 헤드를 못 단다 ⇒ **전용 헤드 또는 앙상블 분산 외에 우회로가 없다**. **실용 소득**: ResNet 코어(도입 동기 = 정확도가 아니라 **앙상블 멤버 outlier 억제**) + 학습된 최적화기 **VeLO**(학습률 불필요, 유일 파라미터 = epoch 수) 로 **10–20× 학습 가속** → 능동학습 고리 현실화. **EAN MD 시드 실험**(같은 초기구조·다른 초기속도 **12궤적**, NVT 298 K, 80 ps, 1 fs, Nosé–Hoover chain 5): 파국(C–N 인위해리 연쇄)을 **모든 지표가 잡는다**, 고불확실도 구간 **500 스냅샷** 보강 재학습 → 파국 소멸·σ 평탄화(committee σ_E figure-read ≈11 eV → ≈0.12 eV). **SrTiO₃**: bulk(135원자 rattle, GPAW LCAO/PBE/Γ) → **(110) 4×1 표면**으로 **적대적 AL** `L_adv = σ²_f·exp(−E/k_BT)`, T=500 K, Powell — 2회전에 최상층 오차 **figure-read ≈10¹ → 10⁻² (3자릿수)**. 🔴 **2회차는 같은 구조에서 재출발하면 수확체감** — 1회차 산물에서 무작위 출발해야 개선 (국소 AL vs 전역 CMA-ES 의 구조적 불일치). **🔑 우리 재계산 12건(전부 원논문 미보고, Zenodo 3 zip 직접 해제)**: ① 데이터 개수 본문과 완전 일치(STO 1000/200·T 500·500 / EAN 666+75=741) ② **`Fig. 9` 기준값 재현** — bulk test 힘 MAD **2.219**·std **4.545** eV/Å (본문 2.23/4.53) ③ ★ **rattle 처방 역설계 — 본문 수식이 틀렸다**: 인쇄된 `분산 = 3T/(k_Bθ_D)` 는 차원 불성립. 실측은 **√m·σ_u = const**(0.641/0.908 amu^½Å @500/1000 K) · **σ ∝ √T**(비 1.405 ≈ √2) 이고 절대값이 **고전 고온 Debye MSD `⟨u²⟩=3ħ²T/(m k_Bθ_D²)`** 와 **0.5 % 일치**(σ_O,500K 실측 0.1603 vs 이론 0.1611 Å) ④ 🔴 **표면 배포 배열은 272 원자**(Sr40Ti64O168, 13층 = 5×SrTiO + 6×O₂ + 2×**Ti12O16 재구성 overlayer**, 면내 = (110) 1×1 의 8배)인데 **본문은 136 원자** — 판정 근거는 `Fig. 12` 축: **E/136 = −6.946…−5.247 eV 가 축 범위와 정확히 일치**, E/272 는 안 맞는다 ⑤ 🔴 **bulk 배포와 표면 배포의 에너지 원점이 다르다**(bulk −32.28 eV/f.u. 척도면 272원자 슬랩은 −1700 eV 아래여야 하는데 배포값은 −916.6 평균) ⇒ 저자가 `Fig. 12` 에서 말한 *"에너지 원점 불일치"* 의 **일부는 모델 결함이 아니라 두 DFT 데이터셋의 참조 차이** ⑥ **CMA-ES 세 궤적을 데이터에서 분리** — 거울대칭 매칭 원자수로 5000개가 정확히 3등분(184/104/24 고정 ⇒ **88/168/248 원자를 풀어 준 것**) ⑦ EAN 셀 = **225원자 = EA⁺·NO₃⁻ 각 15**, 12.9 Å 큐브 ⇒ ρ **1.255 g/cm³**(실험 ≈1.21) ⑧ 본문에 없는 초매개변수 회수(`R_CUT 3.5 Å`·`N_MAX 4`·`EMBED_D 2`·폭 [64,32,16]+head[16]·`N_BATCH 8`·seed 31337). **⛔ 인용 금지 4건**: `RMSE 33.6 / 38.18 **eV** atom⁻¹`(같은 문장 MAE 는 meV, 데이터 전체 폭이 1.06 eV/atom ⇒ 단위 오식) · `EAN-FD force MAE 400 **eV** Å⁻¹`(데이터 평균 |F| 0.5396 eV/Å ⇒ 0 을 예측해도 740× 낫다) · `xtol = 100`(**배포 코드는 `1e-1`** — scipy Powell 에서 100 이면 즉시 종료) · 표면 **"136 atoms"** — `comparison_vs_ours.md` **§J-7(방법 원전) + §J-11 신설** | **🔧 방법 원전 — 불확실도 추정기 · 능동학습 고리 · 힘 분산의 이론적 한계.** ⛔ **재료계 겹침 0**(EAN 이온성 액체 + SrTiO₃ 페로브스카이트 — Li·P·S·Cl 전무, 공유 원소는 O 하나). **물성값 이전 0건.** 축 A–I 해당 없음 |

---

## 2. `comparison_vs_ours.md` — 절 초안

### 2-a. Reference key 에 추가할 행 (`## 📑 Reference key` 표)

| **[Carrete23UQ]** ★ | **Jesús Carrete\***/H. Montes-Campos/R. Wanzenböck/**E. Heid**/**G. K. H. Madsen** 2023 ***J. Chem. Phys.* 158, 204801** (TU Wien + Univ. Santiago de Compostela + Univ. Porto; DOI 10.1063/5.0146905; **OA CC BY**; 데이터·코드 **Zenodo 10.5281/zenodo.7643625**) — "**Deep ensembles vs committees for uncertainty estimation in neural-network force fields**". NNFF(NeuralIL, Behler–Parrinello + spherical Bessel, r_cut 3.5 Å) 위에 **committee / bootstrap / deep ensemble** 3종을 같은 코드로 구현·대결. **결론이 저자에게 불리하다 — 같은 양을 잴 땐 committee 로 충분**(Spearman 0.90 vs 0.91). deep ensemble 의 유일한 승리 = **학습셋 품질 혼합 판별**(그것도 힘 채널). **Appendix = 힘 분산의 미분 불가능성 증명.** ⛔ **재료계 = EAN 이온성 액체 + SrTiO₃** — 우리와 공유 원소 O 하나뿐, **물성값 이전 0건** | ✅ `papers/carrete2023_deep_ensembles_vs_committees.md` | **MLIP 방법론 (계산 100 %) · 참조 DFT = GPAW LCAO/PBE/Γ-only** — **방법 원전 전용, 축 A–I 제외** |

### 2-b. `### J-7. 🔧 방법 원전` 블록에 추가 (물성값 0건이라 4축 표에 안 들어간다)

**[Carrete23UQ] `carrete2023_deep_ensembles_vs_committees` — 불확실도 추정기의 정의 원본 + 우리에게 없는 양의 이름**

> ⛔ **σ·Ea·D·ESW·탄성·gap 이 0건**이다. 여기 있는 것은 **우리가 "불확실도"라고 부르는 것이 무엇인지**를 정의하는 원본이다.

| 항목 | [Carrete23UQ] | 우리 | 판정 |
|---|---|---|---|
| 불확실도의 층위 | **모델 앙상블 분산** (committee 10 / bootstrap 10 / deep ensemble 10) | **단일 모델(UMA-s-1p1) · 멀티시드 MD 3-seed** | 🔴 **다른 양이다.** 우리 `Ea 0.197 ± 0.032 eV`(modelc 600 K 3-seed) 의 ±0.032 는 **열적 샘플링 산포**이고 [Carrete23UQ] 의 σ 는 **epistemic(모델) 분산**이다. ⇒ **우리에겐 epistemic 불확실도 추정치가 아예 없다** — 이 문장을 축 J 에 명시적으로 박아 둔다 |
| 힘 불확실도를 얻는 법 | ① 앙상블 멤버들의 힘 분산 ② 전용 σ²_f 헤드 | 없음 | **Appendix 가 지름길이 없음을 증명**: `σ²_f = ∂²⟨δE(X)δE(Y)⟩/∂X∂Y|_{X=Y}` — **두 점 공분산**이 필요한데 set-pooling 구조는 한 점만 낸다. ⇒ 우리가 σ_f 를 원하면 **committee 를 만드는 길뿐** |
| 가장 싼 실행안 | — | **UMA 체크포인트 복수(1.1 / 1.2 / 크기 다른 것)를 committee 로 묶어 같은 구조의 힘 분산 측정** | ⭕ **이식 후보 (T1)** — **DFT 0회 · 추가 학습 0회**. `uma2026` digest §⑥ 의 *"1.2 를 committee 멤버로 추가"* 와 같은 방향이고 **이 논문이 그 형식의 원전** |
| 전역 힘 불확실도 집계 | `σ_f = √(n⁻¹ Σ_atoms σ²_f)` — **RMS 집계**. 최댓값·softmax·90 백분위수를 전부 시험했으나 **이긴 사례 없음** | 해당 없음 | ⭕ **정의 채택 후보** — 우리가 committee 를 만들면 이 집계식을 그대로 쓴다 (최댓값 쓰지 않기) |
| 공간분해 진단 | **층별 오차/불확실도 violin**(`Fig. 10`) — 표면↔중심 **6 자릿수** 스팬 | 셀 전체 평균만 | ⭕ **이식 후보 (T2)** — 계면 슬랩에서 "MLIP 가 어느 층에서 틀리나". ⚠ **원자 단위로는 못 짚는다**(`Fig. 11`: 오차 최악 원자 ≠ 불확실도 최악 원자) |
| 능동학습 획득함수 | `L_adv = σ²_f · exp(−E_pot/k_BT)`, T=500 K, **Powell 국소 최대화**, 초기 Gaussian 변위 σ=0.1 Å | Stage 00–12 **순차 게이트**(싼 것 먼저) | 🔶 **다른 형식** — 탐색×타당성을 **곱 하나**로. §J-10 이 비판한 가중합 스칼라의 대안. ⚠ **국소 최적화라 전역 탐색을 대체 못 한다**(2회차 수확체감 — 출발점 다양성 필수) |
| rattle 데이터 생성 | 질량가중 Gaussian, θ_D = 418.5 K, T = 500 / 1000 K | 해당 없음 | ⭕ **처방 채택 시 주의**: **논문 인쇄식 `분산 = 3T/(k_Bθ_D)` 는 차원 불성립**. 실제로 쓰인 것은 **`⟨u²⟩ = 3ħ²T/(m k_Bθ_D²)`** (digest 재계산으로 0.5 % 확인). **논문 식을 그대로 코딩하면 안 된다** |
| 참조 DFT 등급 | **GPAW LCAO, PBE, Γ-only** | QE, PBE, PAW, k-mesh 수렴 | ⚠ **우리 기준으로 성긴 참조.** 이 논문의 "DFT ground truth" 를 우리 정본과 같은 등급으로 놓지 않는다 |
| MD 열욕 | **Nosé–Hoover chain(5)**, τ=100 fs, Δt **1 fs**, 298 K, 80 ps | **Langevin**, friction 0.02, Δt **2 fs**, equilib 5 ps / prod 200 ps | ⚠ 결정론적 chain ↔ 확률적 Langevin. **80 ps 내내 σ 가 단조 증가**(=평형이 아니라 탐색 지속)라는 관찰이 **우리 5 ps 평형화를 다시 보게 만든다** — 단 이건 **가설이지 판정이 아니다**(계·열욕·온도 전부 다름). 확인은 무료: 우리 궤적에 골격 MSD/σ 시계열 |

### 2-c. `### J-11.` 신설 제안 — **불확실도 추정기 축** (⚠ 절 번호 충돌 확인 필요)

> 오늘 들어온 불확실도 4편(#78 · **#79 = 이 편** · #80 · #81)이 하나의 축을 이룬다.
> 이 편이 그중 **유일하게 end-to-end**(추정기 구현 → MD 감시 → 재학습 → 능동학습 → 표면 확장)라
> **축의 뼈대로 삼기 적합**하다. 형제 에이전트가 #78/#80/#81 을 넣을 자리를 여기로 모을 것.

**J-11 이 답해야 하는 질문 = "우리는 UMA 가 이 계에서 얼마나 확신하는지 재고 있나?" → 지금은 아니다.**

| 우리가 지금 가진 것 | 이 축이 말하는 이름 | 빈 칸 |
|---|---|---|
| 3-seed MD 산포 `Ea 0.197 ± 0.032 eV` | **열적 샘플링 산포** (aleatoric 도 epistemic 도 아님) | — |
| 없음 | **epistemic σ** (모델 앙상블 분산) | 🔴 **비어 있다** |
| 없음 | **σ_f 공간분해** (층·원자별) | 🔴 **비어 있다** |
| UMA 힘 MAE 30.0 meV/Å (§J-1) | **평균 정확도** | ⭕ 있음 — 단 [Carrete23UQ]·[Zhang26] 둘 다 *"평균이 좋아도 특정 양은 틀린다"* 를 보인다 |

**이 축에서 ⛔ 하면 안 되는 것**
- **σ 를 신뢰구간으로 읽기.** `Fig. 7` 에서 학습범위 밖 실제 오차 **≈40 eV Å⁻¹** 를 띠(**±4–6**)가 전혀 못 감싼다. *"몇 σ 안에 참값"* 문장을 이 논문으로 지지할 수 없다.
- **서로 다른 퍼텐셜을 σ 로 비교하기.** AL 이 돌면 **σ 가 실제 오차보다 빨리 준다**(저자 자인) ⇒ comp1 과 modelc 를 UMA σ 로 비교하면 안 된다. **우리 기존 규율(σ 절대값 인용 금지·비율도 멀티시드 판정만)의 외부 근거가 바로 이것.**
- **원자 단위로 "고σ 원자만 보강" 전략 쓰기** (`Fig. 11` 반례).
- **[Carrete23UQ] 의 어떤 물성값도 우리 표에 올리기** — 재료계가 다르다.

---

## 3. 그 밖의 갱신

- **`properties/`** — 해당 없음 (repo 에 `litdb/properties/` 없음; 물성 원장은 `db/properties/`, 그리고 **이 논문은 물성값 0건**이라 애초에 대상 아님).
- **🎤 talk 역링크** — **불필요**. `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `talks/lee2026_skku_mlip_materials_design.md` 하나뿐이고, 그 §99-10 대기열 6건(Kim2026 hydrolysis · 자료집 목차 · Shapeev/Gubaev/Podryabinkin/Novikov MTP 계열 · Merchant GNoME · Park SevenNet · Luo cryo-TEM · Shin BH₄ · KimYS moisture)에 **Carrete / deep ensemble / NeuralIL 없음**. 양방향 링크 대상 아님.
- **`litdb/pdf_map.tsv`** — 필요하면 `carrete2023_deep_ensembles_vs_committees` ↔ `66caeb45-79DEEP1.PDF` 행 추가. (`litdb/figures/_sources.json` 에는 추출 도구가 이미 기록했다.)
- **`litdb/inbox/`** — 이 PDF 는 업로드 경로에서 직접 처리했다. inbox 로 옮겨 둘지는 사람이 결정.
