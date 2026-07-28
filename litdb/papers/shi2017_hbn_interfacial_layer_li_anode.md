# First-Principles Investigations of the Working Mechanism of 2D h-BN as an Interfacial Layer for the Anode of Lithium Metal Batteries — Shi et al. (ACS Appl. Mater. Interfaces 2017)

> slug `shi2017_hbn_interfacial_layer_li_anode` · DOI `10.1021/acsami.6b14560` · type `DFT (순수 first-principles)` · PDF `82ea256b/bd05d979-firstprinciples…2dhbn…anode…lithium.pdf` · digested `2026-07-20` · status ✅
> **저자**: Le Shi, Ao Xu, **Tianshou Zhao\*** (metzhao@ust.hk) · Dept. of Mechanical & Aerospace Engineering, **HKUST** (홍콩과기대), Clear Water Bay, Kowloon, Hong Kong · *ACS Appl. Mater. Interfaces* **2017, 9, 1987–1994** · Received 2016-11-14 / Published 2016-12-22 · 지원 RGC HK Project 16213414
> ⚠ **비-argyrodite·신규 프로젝트(h-BN@VGCF / Li-metal anode / ORCA)의 DFT 방법론 핵심 레퍼런스**. 우리 LPSCl 캠페인 물성(comp1/modelc)과 **직접 수치 비교 대상 아님** — §7 참조.

---

## 0. 이 digest를 읽는 법
이 논문은 **"왜 2D h-BN 한두 층을 Li 금속 음극 위에 덮으면 dendrite가 줄고 Coulombic efficiency가 오르나?"** 를 **순수 DFT(QE/PBE-D2)** 로 분해한다. 실험(Yang et al.)이 먼저 "h-BN 덮으면 좋다"를 보였고, 이 논문은 그 **작동기전을 계산으로 설명**하는 후속 이론 논문이다.

핵심 그림은 하나다 — **Li⁺는 h-BN *위*가 아니라 h-BN *아래*(Li금속과 h-BN 사이 4 Å 틈)에 깔린다**. 왜? ① 두 층 h-BN이 전자 터널링을 막아(barrier >1.33 eV) 전자가 전해질로 못 새고, ② 그 틈에서의 Li 흡착이 맨 Li금속·맨 h-BN보다 **훨씬 강해서**(−2.0~−2.3 eV) Li가 거기 갇히길 선호하고, ③ 틈 안에서 Li 확산 barrier가 낮아(<0.21 eV) + h-BN이 딱딱해서(stiff) Li가 옆으로 고르게 퍼져 **layer-by-layer 평탄 도금** → dendrite 억제.

> ⚠ **가장 중요한 정직 포인트 3개** (자세히는 §10):
> 1. **결함(vacancy) 통한 Li 투과는 이 논문에서 계산 안 함.** 서론에서 "합성 중 생긴 결함이 Li⁺ 통로"라고 *실험(Yang et al.) 인용*만 하고, 정작 DFT는 전부 **pristine h-BN**. 계산된 "h-BN 위 확산"(0.10 eV)은 **면내(in-plane) 표면 확산**이지 **h-BN 면을 뚫는 out-of-plane 투과가 아니다**. 사용자 질문 #5(결함 매개 Li 투과)의 **정량 답은 이 논문에 없음**.
> 2. **흡착E 기준 = 고립 Li 원자 1개(진공), bulk Li 금속 아님** (eq 2). 그래서 모든 값이 크게 음수. ORCA로 옮길 때 기준 통일 필수.
> 3. **vdW=DFT-D2(2006, 구식·거친 보정).** vdW-지배 계면이라 층간거리(4.0 Å)·계면E가 D2에 민감. Li a=3.26 Å(실험 RT 3.51보다 ~7%↓)는 D2 과응집 신호. h-BN gap 4.3 eV·터널barrier 1.33/1.65 eV는 PBE라 **과소평가(실험 h-BN gap ~6 eV)** → 전자차단은 **하한**.

## 1. 한 줄 요약
2D h-BN 계면층이 Li dendrite를 억제하는 기전은 **(전자차단) + (Li의 under-cover 우선흡착) + (빠른 면내확산 × 높은 강성)** 의 시너지다: 두 원자층 h-BN이 전자터널링을 막고(barrier >1.33 eV) 전해질 분해를 차단, Li는 h-BN *아래* 틈에서 맨표면보다 강하게 흡착(−2.0~−2.3 eV)돼 갇히며, 낮은 확산장벽(<0.21 eV)과 h-BN의 딱딱함이 Li를 옆으로 고르게 펴 **평탄 layer-by-layer 도금**을 만든다.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 시스템 | **2D h-BN (단·이중층) / Li 금속 (bcc) 계면** — SE 없음, 액체 전해질 가정 |
| 질문 | Yang et al.(실험)이 보인 "h-BN 계면층 → dendrite↓·CE↑"의 **원자수준 작동기전이 뭔가** |
| 선행(실험) | **Yang et al.**: h-BN 몇 층을 Cu 집전체에 증착 → Li금속과 액체전해질 분리; 합성 중 생긴 **원자결함이 Li⁺ 통로**로 기대. 실험적으로 dendrite↓·CE 유지 확인 |
| 선행(비교) | 기존 인공 SEI **Al₂O₃, Li₃PO₄**: 기계강도·화학안정 좋으나 **Li⁺ 전도 낮고 계면저항 커서 rate 나쁨** |
| h-BN 선택 이유 | Young's modulus **~1 TPa**, 우수한 화학안정성, **절연성(넓은 gap)** |
| Li 금속 매력 | 이론용량 **3860 mAh/g**, 최저 전위 **−3.04 V vs SHE**; Li-S·Li-air의 전제 |
| 이 논문 기여 | h-BN↔Li 상호작용 성격(=weak vdW) 규명 + **전자차단·흡착·확산** 세 축을 DFT로 정량 → "왜 under-cover 평탄도금인가" 설명 |

## 3. 핵심 물성 (수치 총정리)

### 3-A. Li 금속 표면 (§3.1)
| 물성 | 값 | 비고 |
|---|---|---|
| Li bcc 격자상수 a | **3.26 Å** | "실험과 잘 일치"(원문) — 단 RT 실험 3.51 Å 대비 ~7%↓ (§10 D2) |
| γ {001} | **37.01 meV/Å²** (=0.593 J/m², 단위환산) | **최저** (Wulff 최대노출) |
| γ {110} | **41.28 meV/Å²** (=0.661 J/m²) | 중간 (Wulff 노출) |
| γ {111} | **42.76 meV/Å²** (=0.685 J/m²) | **최고** (Wulff 거의 안 나옴) |
| Li self-흡착 (Li{001}, H site) | **−1.68 eV** | H(hollow)=최강; 3 site(H/B/T) 중 |
| Li self-흡착 (Li{110}, T site) | **−1.85 eV** | T(top)=최강 |
| Li self-확산 barrier {001} | **0.090 eV** | adatom→최근접 안정자리 (Fig 2c) |
| Li self-확산 barrier {110} | **0.046 eV** | (Fig 2c) |
> Wulff 결과 {001}·{110}이 노출면 대부분 → 이후 이 두 면만 사용.

### 3-B. h-BN 단층 (§3.2)
| 물성 | 값 | 비고 |
|---|---|---|
| B–N 결합길이 | **1.45 Å** | 실험 일치 |
| Li 흡착 (hollow) | **−0.56 eV** | 4 site(N-top/B-top/bridge/hollow) 중 **최안정** |
| Li 흡착 (N-top) | **−0.46 eV** | metastable (B-top·bridge는 안정최소 아님, hollow/N으로 이완) |
| Li 면내 확산 barrier | **0.10 eV** | 경로 hollow→**N(saddle)**→hollow (Fig 3b). **면내 표면확산**(≠면투과) |
> Li on h-BN(−0.46~−0.56) ≪ Li on Li금속(−1.68~−1.85) → **Li는 h-BN *위*에 안 쌓인다**.

### 3-C. Li/h-BN 계면 (§3.3)
| 항목 | Li{001}/h-BN | Li{110}/h-BN |
|---|---|---|
| supercell matching | 3×4 Li{001} + 4×3 h-BN | 3×2 Li{110} + 4×2 h-BN |
| 원자수 | **108** | **92** |
| misfit-x / -y | 2.57 % / 0.059 % | 2.62 % / **5.66 %** |
| 계면형성E **E_i** | **−4.17 meV/Å²** | **−1.49 meV/Å²** |
| 계면E(변형제외) **σ** | **−5.85 meV/Å²** | **−6.40 meV/Å²** |
| h-BN↔Li 층간거리 | **4.02 Å** | **4.13 Å** |
| (2층) h-BN 층간거리 | 3.16 Å | 3.11 Å |
| **전자 터널링 barrier** (E_CB,min − E_F) | **~1.33 eV** | **~1.65 eV** |
| 2층째 h-BN gap | **4.3 eV** (pristine 근접, PBE) | 4.3 eV |
> E_i·σ 모두 음수 → 계면형성 열역학적 유리, 세기는 **typical vdW 범위**. 층간 4.0 Å↑ = Li 한 층 낄 공간. Li{110}은 E_i≪σ 차이 = Li{110}면이 h-BN 격자에 맞춰 **큰 strain**(5.66%)을 먹은 결과(h-BN이 더 단단해 Li가 순응).

### 3-D. Li/h-BN 계면 *아래* Li 흡착 (§3.4) — Table 3
| Li{001}/h-BN | A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8 |
|---|---|---|---|---|---|---|---|---|
| **E_ads (eV)** | **−2.18** | −2.04 | −2.10 | −2.17 | −2.11 | −2.12 | −2.16 | −2.13 |
| Δh_BN (Å) | 0.027 | 0.056 | 0.033 | 0.039 | 0.034 | 0.038 | 0.036 | 0.072 |

| Li{110}/h-BN | B1 | B2 | B3 | B4 | B5 | B6 | B7 | B8 |
|---|---|---|---|---|---|---|---|---|
| **E_ads (eV)** | **−2.29** | −2.29 | −2.29 | −2.29 | −2.21 | −2.28 | −2.19 | −2.28 |
| Δh_BN (Å) | 0.018 | 0.017 | 0.018 | 0.017 | 0.014 | 0.018 | 0.016 | 0.018 |
> - **interface ≫ bare**: 계면 −2.0~−2.3 eV ≫ 맨 Li(−1.68/−1.85) ≫ 맨 h-BN(−0.46/−0.56) → Li는 **h-BN 아래로 파고들기 선호**.
> - **자리간 편차 작음**: {001}/h-BN <0.14 eV, {110}/h-BN <0.10 eV → 계면이 Li를 **거의 균일**하게 받아들임 (평탄도금의 열역학 근거).
> - **Δh_BN 매우 작음(0.014~0.072 Å)**: Li 깔려도 h-BN이 평평 유지 = **높은 강성** (dendrite 억제 근거).

### 3-E. 계면 아래 Li 확산 (§3.5, NEB, Fig 9)
| 계면 | 전체 barrier 상한 | 구간별 값 (Fig 9) |
|---|---|---|
| Li{001}/h-BN | **< 0.21 eV** | 0.16 / **0.21** / 0.14 / 0.03 / 0.016 eV |
| Li{110}/h-BN | **< 0.15 eV** | 0.14 / 0.13 / **0.15** / 0.13 eV |
> 이 값 ≈ (맨 h-BN 0.10 eV + 맨 Li 표면 확산) 합과 비슷. 낮은 확산장벽 + 높은 강성 → **옆으로 고르게 퍼짐** → layer-by-layer 평탄성장.

## 4. DFT/계산 방법 ★ (이 논문의 핵심 — ORCA 이식 대상)
- **code / version**: **Quantum ESPRESSO** (버전 명시 없음). 평면파(plane-wave) + 주기경계.
- **functional**: **PBE (GGA)**.
- **vdW**: **Grimme D2 (DFT-D2, 2006)** — *유일한* dispersion 보정. ⚠ 구식(§10).
- **pseudo**: **PAW (projector augmented wave)**.
- **plane-wave cutoff**: **78 Ry** (≈1061 eV, ecutwfc). *ecutrho(전하밀도 컷) 명시 n/a*.
- **k-points**: geo-opt **mesh spacing < 0.05 Å⁻¹**; **DOS는 < 0.01 Å⁻¹**(더 조밀). (금속 Li인데 smearing 방식 명시 n/a.)
- **force 수렴**: **0.01 eV/Å**.
- **vacuum**: **10–15 Å** (슬랩 간 상호작용 차단).
- **Li 슬랩 두께**: **5–7 Li 층** (표면E 수렴 확인).
- **h-BN 층수 규약**: 계면 상호작용·흡착·확산 계산엔 **h-BN 1층만**(층간 vdW 약해서 비용절감); **DOS/전자터널링엔 2층**.
- **NEB images**: Li on Li표면 **9**, Li on h-BN **9**, Li at Li/h-BN 계면 **32**.
- **무질서 처리**: 해당없음 — pristine 결정(bcc Li, hexagonal h-BN). **결함/vacancy 배열 없음**(핵심 한계, §10).
- **DFT+U / AIMD / MLIP**: 없음 (정적 0 K DFT + NEB만).

### 핵심 정의식 (ORCA 이식 시 그대로 맞춰야 함)
| 식 | 정의 | 주의 |
|---|---|---|
| (1) 표면E | **γ = (1/2A)(E_slab^N − N·μ_Li)** | μ_Li=bulk Li 화학포텐셜 |
| (2) 흡착E | **E_ads = E_tot(S/I+Li) − E_tot(S/I) − E_tot(Li)** | **E_tot(Li)=고립 Li 원자 1개** ← 기준 |
| (3) 계면형성E | **E_i = (E_Li/h-BN − E_Li-slab − E_h-BN)/A** | 완전이완 슬랩들 기준 |
| (4) 계면E(strain제외) | **σ = (E_Li/h-BN − E_Li-slab(z) − E_h-BN(z))/A** | 슬랩 xy는 계면격자로 고정·z만 이완 |
| (5) 계면흡착 근사 | **E_ads(interface) ≈ E_ads(Li_surf) + E_ads(h-BN_surf) + δ**, δ>0 | 계면 Li는 아래 Li·위 h-BN 양쪽에 결합 → 두 표면 흡착E의 합 (§5.4) |

## 5. 결과 — 섹션별 상세

### 5.1 Li 금속 Wulff + self-흡착/확산 (§3.1, Fig 1·2)
Li bcc a=3.26 Å. 세 저지수면 표면E: **{001} 37.01 < {110} 41.28 < {111} 42.76 meV/Å²** → Wulff 다면체에서 {001}·{110}이 노출 대부분 (Fig 1). 이후 이 두 면만 다룸.
Li self-흡착 3자리(H/B/T): {001}은 **H(hollow) −1.68 eV**가 최강, {110}은 **T(top) −1.85 eV**가 최강 (Fig 2a,b). Self-확산은 adatom이 최근접 안정자리로 직접 이동, barrier **{001} 0.090 / {110} 0.046 eV** (Fig 2c). → **맨 Li 표면 자체가 이미 확산 매우 빠름**(<0.1 eV)이 baseline.

### 5.2 h-BN 단층 위 Li 흡착·확산 (§3.2, Fig 3)
h-BN B–N 1.45 Å. 4 site 중 최적화하면 Li는 **hollow(−0.56 eV)** 또는 **N-top(−0.46 eV)** 로만 이완(B-top·bridge는 안정 최소 아님). → **h-BN 위 Li 흡착은 맨 Li보다 3~4배 약함** → 도금 시 Li가 h-BN *위*엔 안 얹힌다. 면내 확산: **hollow→N(saddle)→hollow, barrier 0.10 eV** (Fig 3b). *이건 h-BN 시트 표면 위 hopping이지 시트를 뚫는 게 아님.*

### 5.3 Li/h-BN 계면 구조·전자 (§3.3, Fig 4·5, Table 1·2)
두 계면(Li{001}/h-BN, Li{110}/h-BN) 구성 (Table 1·2). 최적화하면 **h-BN 격자는 거의 안 변하고 Li 표면이 h-BN에 맞춰 변형**(h-BN Young's modulus↑ 반영) → strain은 Li가 다 먹음. 층간거리 **4.02/4.13 Å**(Li 한 층 낄 공간). E_i·σ 모두 음수 = 계면형성 유리, 세기 typical vdW.
전자구조(2층 h-BN DOS, Fig 5): 1층째 h-BN은 E_F 오른쪽에 작은 상태밀도 요동(Li금속과 상호작용) 있지만, **2층째는 요동 사라지고 pristine 수준 gap 4.3 eV** 복원. Liu et al. 방식(터널barrier = CB 바닥 − E_F): **{001}/2h-BN ~1.33 eV, {110}/2h-BN ~1.65 eV**. → **두 층이면 전자가 전해질로 못 샌다 → 전해질 분해 차단, Li는 아래에서 도금**.
> 🔑 왜 2층인가: 1층은 Li금속과 hybridize돼 gap이 부분적으로 채워짐(전자 샘). **2층째가 절연성을 회복**해야 진짜 차단막. = "몇 층이 필요한가"에 대한 계산 답.

### 5.4 계면 아래 Li 흡착 = under-cover trapping (§3.4, Fig 6·7·8, Table 3)
8개 대칭자리 각각에서 Li는 h-BN 아래 **hollow 또는 N**으로 이완(pristine h-BN과 같은 선호). 흡착E **−2.0~−2.3 eV** = 맨 Li·맨 h-BN보다 훨씬 강함 → **Li가 계면 틈에 갇히길 선호**. 자리간 편차 작음(<0.14 / <0.10 eV)=균일. Δh_BN 극소=h-BN 평탄 유지.
**핵심 물리 (eq 5, Fig 7)**: 계면 흡착E ≈ (맨 Li 위 흡착E) + (맨 h-BN 위 흡착E) + δ(작은 양수). 즉 **계면 Li는 아래 Li금속과 위 h-BN 양쪽에 동시 결합해서** 흡착E가 두 표면 몫의 *합* → 그래서 그렇게 강하다. Fig 7이 계면값 vs (합)을 y=x 근처로 그려 검증. → 8자리만 계산해도 다른 자리 예측 가능("interface > bare"는 전 자리 일반).
**전하이동 (Fig 8, A1·B1)**: **N 원자가 전자를 잃어 under-cover Li와 Li금속 표면 쪽으로 이동**. 강한 charge transfer가 흡착E를 키워 Li를 계면에 **anchor** → 전해질 노출 차단 → 부식 방지 → CE↑. iso-surface 0.001 |e|/bohr³ (파랑=결핍, 노랑=충만).
자리 다 차면 새 Li가 새 Li표면이 되고 그 위 새 틈이 다음 흡착자리 → **layer-by-layer**.

### 5.5 계면 아래 Li 확산 (§3.5, Fig 9)
안정자리 사이 NEB: **{001}/h-BN <0.21 eV, {110}/h-BN <0.15 eV**. 맨 h-BN(0.10)+맨 Li표면 확산 합과 비슷. **낮은 barrier + 높은 강성 → Li가 옆으로 균일 확산 → under-cover Li의 layer-by-layer 성장 → 평탄 음극면**.

## 6. 작동기전 종합 (§4 결론 = 3-축 시너지)
1. **전자차단** (weak vdW라 h-BN 전자구조 보존 + 2층이면 절연): terminal barrier >1.33 eV → 전자 안 새고 → 전해질 분해 차단 → Li가 위가 아니라 **아래로** 도금.
2. **Under-cover 우선흡착** (계면 −2.0~−2.3 eV ≫ bare): Li가 h-BN 아래 갇힘 → Li-전해질 직접접촉↓ → **CE↑·부식↓**.
3. **균일확산 × 강성** (barrier<0.21 eV + Δh_BN 극소 + Young ~1 TPa): Li가 옆으로 고루 퍼지고 h-BN이 평탄 유지 → **layer-by-layer 평탄도금 → dendrite 억제**.
> 결론 원문: "insulating 2D materials as the interfacial layer of Li metal anode is a promising strategy."

## 7. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
> ⚠ **직접 수치비교 대상 아님** — 이 논문은 **h-BN/Li금속**(액체전해질 가정), 우리는 **argyrodite 황화물 SE(LPSCl)**. 조성·결합·기하 전부 다름. 아래는 **① 방법론 이식(신규 ORCA 프로젝트)** + **② 개념 다리(전자절연 SEI 서사)** 만.

| 항목 | Shi (h-BN/Li) | 우리 (LPSCl) | 관계 |
|---|---|---|---|
| 흡착E 기준 | **고립 Li 원자** (eq 2) | (해당 물성 없음 — 우리는 bulk SE) | **⚠ 신규 ORCA는 기준 통일 필요** |
| functional/vdW | PBE-**D2** | PBE (bulk); mechanical은 우리 PBE (torii는 PBE-D3) | 방법 계열 유사, **dispersion은 D2→D3(BJ) 업글 권장** |
| Li 확산 barrier(면내, h-BN) | **0.10 eV** | (AIMD Ea comp1 0.253 / modelc 0.224 eV, 다른 시스템) | 비교불가(시스템·방법 다름) — **값 이식 금지** |
| 전자차단/절연 서사 | 2층 h-BN 터널barrier **1.33/1.65 eV**(PBE, 하한) | SEI 산물 gap(sei_products.json: LiCl 6.22 / Li₂O 5.24 등) = **전자절연 passivation=dendrite 억제** | **✓ 동일 *철학*** (전자절연막이 dendrite 막는다) — 값은 무관 |
| dendrite 레버 | 전자차단 + 강성 + under-cover 균일흡착 | §E/§F: 전자절연 SEI(LiCl/LiF/Li₃N) | **개념 평행** (우리 kim2026 LiF-SEI, Li₃N 연구와 같은 결) |
| band gap | h-BN 4.3 eV (PBE, 실험 ~6) | comp1 2.066 / modelc 2.099 eV (PBE, 과소·무질서민감) | 둘 다 **"wide-gap insulator"** 수준만; 절대 gap 비교 금지 |
> **결론**: 이 논문은 우리 LPSCl 물성표를 검증/반박하는 논문이 **아니다**. **(a) 신규 h-BN@VGCF/Li-anode 프로젝트의 흡착·확산 DFT 절차 표준** + **(b) "전자절연 계면막이 dendrite를 막는다"는 우리 음극(§E/§F) 서사의 2D-재료 판** 으로만 쓴다.

## 8. 적용 인사이트 (ORCA 복제 + 신규 프로젝트) ★

### 8-A. ORCA로 **직접 복제 가능**한 부분 (h-BN 쪽)
> 우리 새 프로젝트가 ORCA(분자/클러스터, Gaussian basis)로 Li 흡착·확산을 볼 거라 — **h-BN 단층 물리(§3.2)가 1:1 이식 대상**.
- **흡착자리**: pristine h-BN 위 **4자리(N-top / B-top / bridge / hollow)** 중 안정최소는 **hollow(−0.56)·N-top(−0.46)** 둘뿐 (B-top·bridge는 이완돼 사라짐). → ORCA에선 **가장자리-H 종단한 BN 플레이크**(예: B₁₂N₁₂H, 또는 더 큰 BN coronene류) 위 hollow·N에 Li 얹고 이완·비교.
- **기준식**: **E_ads = E(BN+Li) − E(BN) − E(Li원자)**. **Li 원자는 doublet(spin ½), unrestricted(UHF/UKS)** 로 같은 레벨에서 계산. 논문 재현용으로 vs-원자값 + (도금 열역학 원하면) vs-bulk-Li 둘 다 리포트.
- **확산**: 경로 **hollow → N-top(saddle) → hollow, barrier 0.10 eV**. ORCA는 **NEB-TS**(또는 relaxed scan / growing-string). saddle이 N-top 근처인지 확인 후 0.10 eV 재현 목표.
- **함수/보정**: 논문 PBE-D2 → ORCA는 최소 **PBE-D3(BJ)**, 가능하면 **ωB97X-D / B3LYP-D3(BJ)**. 평면파 78 Ry ≠ Gaussian basis → **def2-TZVP↑ + BSSE(counterpoise)** 로 흡착E 보정 (BSSE는 클러스터/Gaussian 특유 이슈, 평면파엔 없음 → 논문값과 정합시키려면 우리가 별도로 챙겨야 함).

### 8-B. ORCA로 **직접은 어려운**(주기·슬랩) 부분 — 정직히 표시
- **Under-cover 계면흡착 −2.0~−2.3 eV / layer-by-layer**: 본질적으로 **Li 금속 슬랩 + h-BN 캡의 주기적 confinement** 물리. ORCA(분자)로는 Li 클러스터 아래 BN 플레이크의 *근사*만 가능 → **정성적 경향만**, 절대값은 주기 DFT(QE/VASP) 권장. eq 5("계면 ≈ Li표면 + h-BN표면 흡착 합")는 ORCA로 **부분 검증**은 됨(Li 클러스터 위 흡착 + BN 위 흡착 각각 구해 합쳐보기).
- **전자 터널링 barrier(1.33/1.65 eV) / 2층 절연 회복**: 적층 h-BN의 **밴드/DOS = 주기 물성**. ORCA는 BN 플레이크 HOMO-LUMO gap은 주지만 **Li금속 E_F 대비 터널barrier는 못 준다** → 이 부분은 우리 sei_products.json 류 gap 논리로 *개념 인용*만, 정량은 주기 DFT.

### 8-C. 신규 프로젝트 설계 인사이트 (우리 h-BN@VGCF/Li-anode)
1. **"Li는 h-BN 위가 아니라 아래"** 가 이 논문의 심장 — 우리 h-BN@VGCF에서도 **Li가 h-BN 코팅 아래(VGCF/Li 쪽)로 가는지**가 관건. 흡착E 위계(맨탄소 vs 맨 h-BN vs 계면)를 우리 계로 다시 그리면 됨.
2. **"몇 층이 필요한가" = 2층**(1층은 전자 샘). 우리 코팅 두께 설계의 계산 근거 → 우리도 h-BN 층수 vs 전자차단을 볼 수 있으면 강함.
3. **결함 매개 Li 투과는 이 논문에 없음** = **우리가 채울 여지**. h-BN에 B/N vacancy·divacancy·삼각공공 넣고 **면투과(out-of-plane) NEB** 계산하면 이 논문이 못 한 걸 정면으로 답함 (사용자 질문 #5의 진짜 답).
4. **강성×확산 시너지**: dendrite 억제엔 낮은 확산장벽만이 아니라 **딱딱한 캡**도 필요(Δh_BN 극소). 우리 h-BN도 코팅이 평탄 유지하는지(기계) + Li 확산(전기화학) 둘 다 봐야.

## 9. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| **1** | Li bcc Wulff 다면체 + 3면 표면E (37.01/41.28/42.76 meV/Å²) | 어느 Li면을 모델로 쓸지 근거({001}·{110}); 우리 Li-anode 슬랩 선택 |
| **2**(a,b) | Li{001}·{110} self-흡착 3자리(H/B/T) | 맨 Li 흡착 baseline(−1.68/−1.85) |
| **2**(c) | Li self-확산 곡선 (0.090 / 0.046 eV) | 맨 Li 표면 확산 baseline |
| **3**(a) | h-BN 위 Li 흡착 4자리 + 이완 궤적 | **ORCA 복제 대상**: hollow/N 최소 |
| **3**(b) | h-BN 위 Li 확산 (hollow→N→hollow, 0.10 eV) | **ORCA NEB 복제 대상** |
| **4** | Li{001}·{110}/h-BN 계면 기하 + 층간거리 4.02/4.13 Å | 계면 confinement 공간(Li 한 층 낄 틈) |
| **5** | Li/2h-BN DOS (1층 요동·2층 gap 4.3 eV·터널 1.33/1.65 eV) | **전자차단=2층 필요** 근거; 우리 층수 설계 |
| **6** | 계면 8흡착자리 (이완 전/후) | 계면흡착 샘플링 방식 |
| **7** | 계면흡착 vs (맨Li+맨hBN) 상관 (y=x) | **eq 5 검증법** — ORCA로 부분 재현 가능 |
| **8** | 계면 Li 흡착 전하이동(N→Li) top·side view | anchoring 기전; 우리 charge-transfer 분석 참고 |
| **9** | 계면 아래 Li 확산 NEB ({001}<0.21 / {110}<0.15 eV) | under-cover 균일확산 근거 |

## 10. Post-processing ★
- **NEB** (QE ph/NEB): Li 확산 barrier. images 9(Li표면)·9(h-BN)·32(계면). 기록=상대E vs 반응좌표, barrier(eV).
- **DOS/PDOS** (2층 h-BN, 층·원소 분해): E_F 기준 상태밀도로 절연성/터널barrier(=CB바닥−E_F) 판독. 기록=층별(1st/2nd) B·N + Li PDOS.
- **Wulff construction** (표면E γ 3면 → 다면체): 노출면 결정. 도구 명시 n/a (pymatgen WulffShape류 추정).
- **charge transfer / 전하밀도차** (Δρ, iso 0.001 |e|/bohr³): N→Li 전자이동 시각화. 파랑=결핍/노랑=충만.
- **계면형성E E_i / 계면E σ**: eq 3·4로 vdW 결합세기 + strain 분리.
- **수치화·기록**: 흡착E(Table 3)·barrier(Fig 2c/3b/9)·터널barrier·층간거리 — 전부 정적 0 K 값.
> 우리 적용: **h-BN 쪽 흡착/NEB는 ORCA로**, **계면 confinement·터널barrier·DOS는 주기 DFT(QE/VASP)로** 이원화.

## 11. 인용 가능 문장 (deck/paper용)
- "Shi et al. (DFT, QE/PBE-D2) show Li binds far more strongly in the Li/h-BN interlayer gap (−2.0 to −2.3 eV vs a free Li atom) than on bare Li (−1.68/−1.85 eV) or bare h-BN (−0.46/−0.56 eV), so Li plates *under* the h-BN cover rather than on top of it."
- "Two atomic layers of h-BN are needed to recover an insulating gap (4.3 eV) and give an electron-tunneling barrier of 1.33–1.65 eV; a single layer partially hybridizes with the Li metal and leaks electrons."
- "The computed Li migration barrier is only 0.10 eV on pristine h-BN and <0.21 eV in the Li/h-BN interlayer, which together with h-BN's ~1 TPa stiffness drives uniform, layer-by-layer Li plating."
- "The interfacial adsorption energy is well approximated by the *sum* of the adsorption energies on the bare Li and bare h-BN surfaces (E_ads,int ≈ E_ads,Li + E_ads,hBN + δ, δ>0), reflecting Li bonding to both surfaces at once."
- (정직) "Shi et al. model **pristine** h-BN only; defect/vacancy-mediated Li permeation *through* the h-BN plane — the experimentally invoked Li⁺ pathway — is **not** computed."

## 12. 주의/한계 (over-claim 방지 · 비판) ★
1. **결함 매개 Li 투과 미계산 (가장 큰 구멍)**: 서론은 "합성 결함이 Li⁺ 통로"(Yang et al. 실험)라 하지만 DFT는 전부 pristine. 계산된 "h-BN 위 확산 0.10 eV"는 **면내 표면 hopping**이지 **면을 뚫는 out-of-plane 투과가 아님**. **Li가 어떻게 h-BN 아래로 들어가는지 자체는 계산으로 안 다룸** — under-cover 흡착·확산은 "이미 아래 있다"는 전제. → 사용자 질문 #5의 정량답은 여기 없음(= 우리가 채울 부분).
2. **흡착E 기준 = 고립 원자**: −2.29 eV 같은 큰 값은 **vs 진공 Li 원자**. bulk Li 응집E(~1.6 eV/atom 급) 대비로 환산하면 "계면이 bulk Li보다도 Li를 잘 잡는다"가 진짜 메시지지만, 논문 절대값을 그대로 "결합세기"로 인용하면 과대. ORCA 이식 시 기준 반드시 통일.
3. **DFT-D2 = 구식·거친 vdW**: vdW 지배 계면이라 층간거리·E_i·σ가 보정법에 민감. **Li a=3.26 Å(RT 실험 3.51보다 ~7%↓)·h-BN 층간 3.11–3.16 Å(bulk 3.33보다 짧음)** = D2 과응집 신호. "weak vdW" 정성결론은 견고하나 **정량 거리·에너지는 D2 의존** → 우리는 D3(BJ)/vdW-DF로 재확인 권장.
4. **PBE gap 과소 → 전자차단 하한**: 2층 h-BN gap 4.3 eV·터널barrier 1.33/1.65 eV는 **PBE**. 실험 h-BN gap ~6 eV → **실제 차단은 더 셈**. "절연·전자차단" 정성은 안전, 절대 barrier는 **하한값**으로만.
5. **터널barrier = (CB바닥−E_F) 는 heuristic**: Liu et al. 인용한 근사. 실제 터널링 확률은 barrier 높이 + **폭**(2층 ~6.3 Å) + 전해질 LUMO 정렬에 의존 → 계산된 터널링 전류가 아님.
6. **계면 incoherent·strained**: Li{110}은 h-BN에 맞추느라 5.66% strain(E_i≪σ 차이가 증거). strained 계면의 흡착E는 그 artifact를 안고 있음.
7. **Li=금속인데 smearing/k 정보 부족**: k<0.05 Å⁻¹는 큰 supercell엔 OK지만 금속 표면E엔 다소 성김; smearing 방식 명시 없음.
8. **온도·동역학 없음**: 0 K 정적 + NEB. 실제 도금은 유한온도·과전압·용매·농도 구배 — 전부 밖. "layer-by-layer 평탄"은 **열역학·정적 barrier 논증**이지 kinetic 시뮬레이션 아님.

## 13. 기법 용어 미니사전
- **h-BN**: hexagonal boron nitride, 2D 절연체(그래핀의 절연 사촌), B–N 육각격자, gap 실험 ~6 eV, Young ~1 TPa.
- **Wulff construction**: 표면E로 결정 평형형상 예측 → 어느 면이 많이 노출되나.
- **표면E γ**: 벌크를 잘라 표면 만들 때 단위면적 에너지 비용(낮을수록 안정·많이 노출).
- **흡착E E_ads**: 원자를 표면에 붙일 때 에너지 변화(음수=결합유리). *기준*(원자/벌크)이 값을 좌우.
- **weak vdW (van der Waals)**: 전하이동 없는 약한 분산 인력 — 층상물질 층간·physisorption의 결합.
- **DFT-D2/D3**: PBE가 못 잡는 분산력을 원자쌍 보정으로 더함(D3가 D2보다 정교, 좌표의존·감쇠 개선).
- **PAW**: projector augmented wave, 코어전자를 효율적으로 다루는 평면파 표준.
- **NEB (nudged elastic band)**: 두 안정상태 사이 최소E 경로·활성화barrier 찾는 방법(images=중간구조 수).
- **터널링 barrier**: 전자가 절연막을 뚫는 유효장벽(여기선 CB바닥−E_F 근사) — 클수록 전자 안 샘.
- **DOS/PDOS**: (부분)상태밀도 — E별 전자상태 수(층·원소로 분해하면 어디가 절연/금속인지).
- **Coulombic efficiency (CE)**: 방전/충전 전하비 — dendrite·SEI 소모로 떨어짐.
- **dendrite**: Li 도금 시 뾰족하게 자라는 가지 — 단락·SEI 파열 원인.
- **BSSE (basis set superposition error)**: Gaussian-basis 클러스터 흡착E의 인위적 과결합 — counterpoise로 보정(평면파엔 없음).
