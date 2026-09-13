# ⏳ pending — `chang2026_performance_based_mlip_selection_sse` 의 INDEX / comparison 반영분
> ✅ **①②③ 병합 완료 2026-09-13** (조율 세션) — INDEX.md: ① 병합됨 · comparison_vs_ours.md: ② → J-0 · ③ → J-7. 남은 것 없음.

> 2026-09-09, litdb-curator. **동시작업 충돌 회피**로 `INDEX.md` · `comparison_vs_ours.md` 를 직접 안 고쳤다.
> 아래 블록을 **사람이(또는 조율 담당 세션이) 그대로 옮겨 붙이면 된다.**
> digest 본체: `litdb/papers/chang2026_performance_based_mlip_selection_sse.md`
> 그림: `litdb/figures/chang2026_performance_based_mlip_selection_sse/` (**16장** = 그림 8 + 표 8)
> 🎤 talk 역링크: **해당 없음** (`litdb/talks/lee2026_skku_mlip_materials_design.md` §99-10 대기열에 없음)

---

## ① `litdb/INDEX.md` — **`## 🤖 MLIP 방법론 — 우리 UMA 스택을 재는 축`** 절에 추가할 행

```markdown
| `papers/chang2026_performance_based_mlip_selection_sse.md` | **[외부·methods·★★argyrodite 에서 직접 잰 MLIP 선정 벤치마크]** **D. Chang, A. Taqieddin, F. Laskowski\*** (3인 전원 **Solid Power Operating Inc.**, Materials Informatics & Modeling Div., Louisville CO), "**Performance-Based Selection of Machine Learning Interatomic Potentials for Studying Solid-State Electrolytes**", ***Chem. Mater.* 2026, 38 (7), 3133–3144** · DOI `10.1021/acs.chemmater.5c02352` · 접수 2025-09-04 / 게재 2026-04-02 · 본문 12 pp + SI 16 pp · Fig 1–4 + S1–S4 · Table 1–3 + S1–S5 · refs 65+6 · ⛔ **코드·데이터 미공개**(Data Availability 절 없음) · 자원 ACCESS/SDSC Expanse. — **질문**: *"범용 MLIP 를 fine-tune 없이 as-is 로 argyrodite 에 써도 되나, 그리고 어느 걸 골라야 하나."* **답**: **정적 지표로는 못 고른다(5모델 전부 MAE < 10 meV/atom = DFT 자체 불확도), 고르는 것은 동역학이고 기준은 힘의 보존성이다.** **★1 피고 5종(전부 `Table 2`)**: **EqV2**(`eqV2 S DeNS`, EquiformerV2, MPtrj+DeNS, 31.2 M, cut 12 Å, **direct**) · **DeePMD**(`DPA3-v1-MPtrj`, 4.81 M, cut 6 Å, conservative) · **ORB v2**(`ORB v2 MPtrj`+Alexandria, GNN 비등변, 25.2 M, cut 10 Å, **direct**) · **SevenNet**(`SevenNet-l3i5`, NequIP/E(3)등변 l=3, **1.17 M**, cut **5 Å**, conservative) · **MACE**(`MACE-MP-0`, ACE-MPNN, 4.69 M, cut 6 Å, conservative). ⛔⛔ **UMA·eSEN·OMat24 학습 모델은 없다** — 가장 가까운 `eqV2 S DeNS` 조차 **MPtrj 학습 + direct force** 라 우리 UMA-s-1p1(OMat24 + conservative)과 **양쪽이 다르다**. **★4 DFT 기준 = VASP / **PBE** / 520 eV / MP k-밀도 · MP 수렴기준 · vdW 없음 · PAW셋·스핀 미기재 · ⛔AIMD 설정 전무** ⇒ **우리 MLIP 벤치(PET-MAD **PBEsol** 라벨)와 에너지 수치 비교 불가**, 우리 DFT 정본(PBE)과는 정성 비교만. **★2 "performance-based selection" 에는 스칼라 점수도 문턱도 없다** — 지표 8종(형성E MAE/RMSE·회귀통계·오차분포 대칭성·Ehull 편차·**구조유형별 분해**·E(T) 열전이성·**에너지 드리프트**·추론효율)을 **순서대로 서술**할 뿐, 가중합 없음 ⇒ 우리 `combine_rankings.py` 가 걱정하는 함정은 없지만 **이식할 점수식도 없다**. **🔑 헤드라인 수치**: `Table 1`(N=**158** = argyrodite 129 + MP 29) MAE meV/atom — ORB v2 **4.686** < SevenNet 4.916 < EqV2 6.487 < DeePMD 6.842 < MACE 9.610; **`Table S1` 구조유형별 분해가 결론을 뒤집는다** — 이미 이완된 MP 구조는 ORB v2 **2.198** 압승인데, **거친 Li₇PS₆ 프로토타입에서 이완시킨 argyrodite 는 SevenNet 3.717 / ORB v2 5.246 / MACE 9.392** ⇒ *"Matbench Discovery 순위는 우리 과제 순위가 아니다"*. **★★ 동역학이 진짜 판정**: 1100 K NVT 10 ps 총에너지 드리프트 (`Fig. S3`, `figure-read ≈` digest 계산) **EqV2 +590 · Orb +425 meV/atom** vs **SevenNet·DeePMD ≈0** ⇒ 비보존(direct-force) 아키텍처는 *"artificially enhanced diffusion"*. **★5 MD 규약**: 셀 52원자(모델비교) / conventional 1×2×2(전도도), 램프 100 K→목표(1 K/4 fs), 평형 20–50 ps(±5% 판정), 생산 **10 ps**(모델비교) / **300–450 ps**(전도도), 온도 **700/900/1100/1300 K**, **MSD 창 τ > 100 ps**, pymatgen, **Haven=1**(우리 역산 2% 이내 확인), **시드 1개**, 오차막대는 **MSD 의 x,y,z 3성분 SEM**(독립표본 아님), thermostat·dt·절편 미기재. **★3 argyrodite 에서 실제로 잰 것 = 4a/4c 자리선호(⚠DFT 로만) + cage 간 점프빈도**: `Table 3` DFT ΔE meV/atom — **Cl 4a 100% 가 바닥상태(0)**, **75% 4a 가 3.28 로 사실상 축퇴**, 4c 100% 만 39.72 로 확연히 불리, 나머지 25 이내(상온 접근가능; Minafra Rietveld 실측 4a ~50%). ⛔ **MLIP 이 이 순위를 맞추는지는 논문이 채점하지 않았다** — 게다가 평가집합을 **ORB v2·MACE 가 사전선별**했다(SI §2 자백). ⛔ **"dopant-induced charge" 는 측정 안 했다**(Bader·전하해석 0건, Introduction 동기문장일 뿐), ⛔ **"descriptor for screening of argyrodite" 는 참고문헌 (62) 의 제목** = **Jun & Lee JMCA 2022**, 우리가 이미 보유(`jun2022_argyrodite_ion_cage_size_descriptor`). **★6 거짓 음성 검증 = 안 했다** — 탈락시킨 ORB v2·EqV2 로 D·σ 를 재본 적 없고, **MACE 는 MD 자체를 안 돌렸다**(`Table S2` 에 행 없음) ⇒ 보존적인데 정적 최하위인 모델의 운명은 미결. **🔴🔴 우리가 산술로 잡은 오류 3건**: ① **`Table 3` 의 "Ea [meV]" 는 eV 다** — `Fig. 3b` 인쇄값 **Ea = 0.41 ± 0.02 eV** 가 표의 40.6 과 1000배 어긋나고, D₀·D(700 K) 역산이 eV 해석에서만 맞는다 ⇒ 실제 Ea 범위 **0.197–0.406 eV** ② **앙상블 σ = 14.67 mS/cm 의 Boltzmann 가중이 per-atom** — exp(−ΔE[meV/**atom**]/kT) 로 계산하면 **14.666 재현(정확 일치)**, 물리적으로 옳은 셀당(×52원자) 가중이면 **0.065 mS/cm** (**225배**) ⇒ *"실험 ~5 mS/cm 와 3배 이내"* **인용 금지**; 배열 다중도도 미포함 ③ **표본수 3중 불일치** — `Table 1` 캡션 129+29=**158**(우리가 `Table S1` 가중평균으로 5모델 전부 재현 확인) vs `Fig. 1a` **209** vs `Fig. S2` **206(126+80)**. **🔴 SI 사실오류**: SI §4 *"slight reduction in the overall MAE of SevenNet"* → **틀렸다, 늘었다** (전체 4.916→**5.763**, argyrodite 3.717→**5.249 (+41%)**); 확장셋(`Table S4`, N=282)에서 **SevenNet 5.763 vs ORB v2 5.907 = 사실상 동률이고 RMSE 는 ORB v2 승(6.836 vs 9.497)** ⇒ 본문의 "SevenNet 압승" 그림이 옅어진다. **🔴 본문 부호 서술이 `Fig. 1c` 를 3번 뒤집는다**(p.3137 *"SevenNet slightly overestimates"* · p.3138 *"ORB v2 … underestimate"* — 그림은 정반대). **🔴 `Fig. 2` "depth" 주장 미지지** — SevenNet 등고선은 DFT 보다 **더 깊다**(Ehull 은 반대로 SevenNet 이 확실히 낫다: 0.010–0.028 vs ORB v2 0.030–0.040 eV/atom). **🔴 `Fig. 4b` 상관이 조건부** — σ 최저인 100%-0% 배열이 **Cl 자리 점프빈도는 최고(7.8/ps)**, 상관은 **S²⁻ 자리에서만** 성립. **★★★ 우리 UMA 방어 판정 = 🟡 부분 방어**: ⭕ *"보존적 모델을 쓰라"* 가 이 논문의 1차 판정축이고 **UMA-S 는 보존적(NVE ✓, `uma2026…` Table 1/4/16 + 우리 유한차분 프로브 0.198%)** ⇒ **탈락 범주에 속하지 않는다**는 것이 argyrodite 에서 직접 측정된 근거로 방어된다; ⭕ *"리더보드 ≠ 응용 적합성"* 이 우리 J-1 실측(Li₃PS₄ 힘 MAE 30.0 meV/Å)을 정당화한다; ⛔ 그러나 **UMA 는 시험되지 않았고**, 승자는 **MPtrj 학습 SevenNet** 이며, **SevenNet-MPtrj vs UMA-OMat24 비교는 어느 논문도 안 했다**. ⇒ **재야 할 것 3건(전부 DFT 0회)**: **A1** UMA 로 `Table 3` 6배열 ΔE 재현(정답이 인쇄돼 있다 — 4a/4c 자리선호를 UMA 가 맞추나) · **A2** UMA NVT 10 ps @1100 K 드리프트(`Fig. S3` 와 직접 겹침) · **A3** 우리 궤적 **log-log MSD** 로 2–50 ps 가 확산영역인지 확인. **🔴 우리 MSD 창에 대한 유일한 실질 위협** = `Fig. S1b`: 700 K 완전정렬 배열에서 **τ ≈ 10–70 ps 가 케이지 평탄부** → 저자는 τ>100 ps 에서만 피팅. 우리 창은 2–50 ps 이고 **우리 최저 온도는 600 K 로 더 낮다** ⇒ **comp1 600 K 가 최고 위험 조합**. ⛔ **규약은 A3 결과 없이 바꾸지 않는다**(`tools/convention_check.py` 관리 대상). ⛔ **물성 4축(A/B/C/D) 편입 금지** — band gap 0 · elastic 0 · ESW 0 · σ 는 인용금지 ⇒ `comparison_vs_ours.md` **`🔧 방법 원전`(J-7)** 에만. **후속 확보 1순위**: **ref 53** Lee/Ju/Han, *"Disorder-Dependent Li Diffusion in Li₆PS₅Cl Investigated by MLP"*, **ACS AMI 2024, 16, 46442** (**r2SCAN 학습 SevenNet → ~5 mS/cm**, 우리 미보유) + **ref 52** Kim 외 JACS 2025, 147, 1042 (**같은 아키텍처 PBE 학습 → ~44 mS/cm @350 K**) ⇒ **σ 를 ~9배 가르는 것이 아키텍처가 아니라 학습 범함수**라는 명제의 원전 짝 | **방법론(MLIP 선정)·T1(우리 엔진을 재는 축)** — **argyrodite 에서 직접 잰 몇 안 되는 편**, 물성값은 인용불가 |
```

**⚠ INDEX 행에 같이 반영할 것**
- 같은 절의 **`wang2025_pretrained_deep_potential_sulfide_sse`** 행에 상호참조:
  *"⇒ 같은 진단(범용 MLIP 의 평형 편중)을 **argyrodite 에서 직접** 잰 편 = `chang2026_…`.
  ⚠ 두 편 모두 피고가 **MPtrj 세대**라 UMA(OMat24)로의 이식은 여전히 막혀 있다."*
- **`tompa2026_finetuning_mlip_foundation_strategies`** 행에 상호참조:
  *"⇒ `chang2026_…` 은 **fine-tuning 을 일부러 안 한** 반대편 실험이고, 그 이유로 Tompa 가 정량화한
  **'fine-tune 이 도메인 밖을 1.7배 악화시킨다'** 를 그대로 든다 (§2, 이유 (b))."*
- **`jun2022_argyrodite_ion_cage_size_descriptor`** 행에 상호참조:
  *"⇒ `chang2026_…` 의 ref 62 로 인용됨. **'argyrodite screening descriptor' 라는 표현의 정본은 이쪽이다**
  — chang2026 자체에는 이름 붙은 descriptor 가 없다."*
- **`uma2026_family_of_universal_models_for_atoms`** 행에 상호참조:
  *"⇒ `chang2026_…` 이 argyrodite 에서 **보존/비보존을 1차 판정축으로 세웠고**, UMA-S 는 그 축의 합격 쪽이다
  (`Table 1`/`4`/`16` NVE ✓). ⛔ 단 chang2026 은 UMA 를 시험하지 않았다."*

---

## ② `litdb/comparison_vs_ours.md` — **§J-0 출처표** 에 추가할 줄

```markdown
| **[Chang26Sel]** 🔧 | `chang2026_performance_based_mlip_selection_sse` — **argyrodite 에서 직접 잰 사전학습 MLIP 선정 벤치마크** (*Chem. Mater.* **38**, 3133 (2026) · Solid Power Inc.). 피고 5종 = EqV2·DPA3·ORB v2·**SevenNet**·MACE, **전부 MPtrj/PBE** · ⛔ **UMA 없음**. ⚠ **물성값 인용 불가**(σ·D 는 PBE 편향 + 400 K 외삽 + 단일시드, Ea 는 단위 오기) → 아래 **J-7** 에만, A–D 축 금지. ★ **우리 계(Li₆PS₅Cl)로 직접 잰 몇 안 되는 방법론 편** |
```

---

## ③ `litdb/comparison_vs_ours.md` — **§J-7 `🔧 방법 원전`** 에 추가할 블록

```markdown
**[Chang26Sel] `chang2026_performance_based_mlip_selection_sse` — *어떤 사전학습 MLIP 를 골라야 하나* 의 argyrodite 실측**
(*Chem. Mater.* **2026**, 38, 3133–3144 · DOI 10.1021/acs.chemmater.5c02352 · **Solid Power Operating Inc.** 3인 ·
⛔ 코드·데이터 미공개 · **물성값 인용 불가**)

> 🔑 **이 편에서 가져오는 것은 값이 아니라 "판정축"이다.**
> 그리고 그 판정축이 **우리 UMA 선택을 부분적으로 방어해 준다** — 다만 **UMA 자체는 이 논문에 없다.**

| 항목 | [Chang26Sel] | 우리 (UMA-s-1p1 omat) | 판정 |
|---|---|---|---|
| **피고 목록** | EqV2(direct) · DPA3(cons.) · ORB v2(direct) · **SevenNet-l3i5(cons.)** · MACE(cons.) | **UMA-s-1p1** | ⛔ **UMA 없음.** 가장 가까운 `eqV2 S DeNS` 도 **MPtrj + direct** ⇒ 우리와 양쪽이 다르다 |
| **사전학습 코퍼스** | **전부 MPtrj** (ORB v2 만 +Alexandria) | **OMat24** | ⚠ `wang2025` 때와 **같은 세대 문제**. OMat24 가 MPtrj softening 을 개선했다는 우리 기록(`db/external/omat24/README.md`)이 있으므로 **결론 직수입 금지** |
| **★ 참조 범함수** | **PBE** (VASP 520 eV, MP 설정) | DFT 정본 **PBE**(QE/USPP) / MLIP 벤치 라벨 **PBEsol**(PET-MAD) | 🟡 DFT 축은 같은 계열이라 **정성** 비교 가능 · 🔴 **MLIP 벤치는 라벨이 달라 수치 비교 불가** |
| **★★ 1차 판정축 = 힘의 보존성** | 비보존(ORB v2·EqV2) → 1100 K 10 ps **+425 / +590 meV/atom 드리프트** (`Fig. S3`, `figure-read ≈`) · 보존(SevenNet·DPA3) → **≈0** | **UMA-S = 보존적**, NVE ✓ (`uma2026…` Table 1/4/16) + 우리 **유한차분 프로브 0.198% @ δ=0.005** | ⭕⭕ **우리가 합격 쪽이다.** *"우리는 이 논문이 탈락시킨 범주가 아니다"* 는 **정당한 방어** |
| **정적 지표의 변별력** | ⛔ **없다.** 5모델 전부 MAE < 10 meV/atom | 우리 J-1 = 힘 MAE 30.0 meV/Å | ⚠ **"MAE 가 낮으니 안전" 논증은 이 논문이 직접 부정한다.** 우리 J-1 도 같은 한계를 이미 적어 놨다(장벽·응력 미측정) |
| **평가설계** | **거친 Li₇PS₆ 프로토타입 → 전이완 → 채점**. 이완된 MP 구조로 채점하면 리더보드 재현일 뿐 | 우리 벤치는 **주어진 구조에 단일점 힘/에너지** | ⭕ **이식할 가치 있음** — 우리 벤치에 없는 축 |
| **MD 온도창** | **700 / 900 / 1100 / 1300 K**, 300 K 는 **외삽** | **600 / 800 / 1000 K** | 🟡 우리가 더 낮다 = caging 위험이 더 크다 |
| **★★ MSD 피팅 창** | **τ > 100 ps**. 근거 = `Fig. S1b` 에서 **700 K 완전정렬 배열이 τ≈10–70 ps 에 평탄부** | **2–50 ps 고정** | 🔴 **정면 충돌.** 단 그쪽은 **가장 느린 배열**이고 우리 modelc 는 빠르다 ⇒ **"확인할 것"이지 "이미 틀린 것"이 아니다.** **comp1 600 K 가 최고 위험 조합** |
| σ 산출 | pymatgen NE, **Haven = 1** (우리 역산 2% 이내 확인) | NE, Haven=1 | ⭕ **동일** |
| 시드·오차막대 | **시드 1** · MSD 의 x,y,z **3성분 SEM**(독립표본 아님) | modelc 600 K **3-시드** (Ea 0.197±0.032) | ⭕ **우리가 낫다.** `mccluskey2025`·`pranami2015`·`maginn2019` 가 3성분 SEM 의 과소평가를 지적 |
| **자리무질서(4a/4c) DFT 정답** | `Table 3` ΔE meV/atom: **100%4a = 0** · 75% = **3.28** · 50% = 24.73/27.52 · 25% = 22.48 · **0%4a = 39.72** | ⛔ **우리는 안 쟀다** | 🔴 **A1 — DFT 0회로 UMA 를 채점할 수 있는 외부 정답** |
| **추론 비용** (52원자, 1100 K) | ORB v2 462 ATS / SevenNet 117 / DPA3 80 / EqV2 51 atom-steps/s ⇒ **ORB v2 가 SevenNet 의 4.0배** | — | ⚠ 이 논문은 **4배 느린 쪽을 물리적 일관성 때문에 골랐다.** 하드웨어 미기재라 절대값 인용 금지 |
| **학습 범함수 ↔ σ** | ref 53(r2SCAN 학습 SevenNet) **~5 mS/cm** vs ref 52(PBE 학습 같은 아키텍처) **~44 mS/cm @350 K** | 우리 규율: **σ 절대값 인용 금지** | ⭕⭕ **우리 `mlip_committee.py` 규율의 독립 재확인** |

**⛔ 이 편에서 인용하면 안 되는 것**
1. **`14.67 mS/cm` 앙상블 평균** 및 *"실험 ~5 mS/cm 와 3배 이내"* — **Boltzmann 가중이 per-atom** 이다.
   우리 재현: per-atom → **14.666**(정확 일치) · 셀당(×52) → **0.065 mS/cm**. **225배.**
2. **`Table 3` 의 Ea 를 meV 단위로** — **eV 다** (`Fig. 3b` 인쇄값 0.41 ± 0.02 eV 가 증거).
3. **σ·D 절대값 전부** (PBE 편향 + 700 K→300 K 외삽 + 단일시드).
4. *"모든 MLIP 이 10 meV/atom 안"* 을 **UMA 로 확장** — UMA 는 시험되지 않았다.
5. *"MACE 는 argyrodite 부적합"* — **MACE 는 MD 시험을 안 받았다**.
6. **`Fig. 1a`/`Fig. S2a` 의 표본수 209/206** — 실제 158(`Table 1`) / 282(`Table S4`).
7. **`Fig. 3a` 의 절대 세로 오프셋** — 참조보정이 없어 해석 불가(우리 `bench_against_dft.py` docstring 참조).

**⇒ 우리가 지금 할 수 있는 것 (전부 DFT 0회)**

| # | 할 것 | 근거 | 비용 |
|---|---|---|---|
| **A1** | UMA 로 `Table 3` 6배열 ΔE 재현 → **UMA 가 Cl 4a 선호를 맞추나** | 논문 DFT 값이 인쇄돼 있다 | UMA relax 6회 |
| **A2** | UMA NVT 10 ps @1100 K, Li₆PS₅Cl 52원자 **총에너지 드리프트** | `Fig. S3` 와 직접 겹치는 시험 | 낮음 |
| **A3** | 기존 궤적으로 **log-log MSD** → 2–50 ps 가 확산영역인지 | `Fig. S1b` 가 제기한 유일한 실질 위협 | **재분석만** |

⛔ **A1–A3 는 기존 도구 확장으로 한다**(`tools/mlip/bench_against_dft.py` · `tools/ionic/`) — 새 파일 금지(코드 규율).
⛔ **A5(6배열 UMA-MD σ 비율) 같은 새 물리량은 `kb/templates/estimand_card.md` 를 먼저 채운다.**
```

---

## ④ (선택) `litdb/properties/` — 해당 없음

이 논문은 우리 물성 4축(A 이온전도 / B 산화안정 / C 기계 / D 전자구조)에 **넣을 수 있는 값이 없다**:
`band gap` 0회 · `elastic` 0회 · 전기화학창 0회 · σ·D 는 인용금지 · Ea 는 단위 오기.
⇒ **`properties/*.md` 갱신 없음.** `comparison_vs_ours.md` 의 **J-7(방법 원전)** 에만 들어간다.
