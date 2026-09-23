<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/chaney2024_two_step_sei_growth_argyrodite_li_metal.md (같은 축 · 직전 편).
     2026-09-23 초판. 1저자 지정 1번 임무 = "이 논문이 자기제한을 동역학으로 보였나 → kb/concepts/cv_vs_dqdv_and_two_windows.md §8-4 를 고쳐야 하나".
     근거 층위 셋을 전부 읽었다: 본문 13 pp · SI 15 pp · 저자 코드 저장소(아래 커밋). 그림은 본문 6 + SI 6 을 실독, Fig. 2 는 원본 래스터 픽셀 판독까지.
     ⚠ "✎" 표시는 **논문이 보고하지 않은 것을 우리가 유도·검산한 것**이다. "figure-read ≈" 는 그림에서만 읽은 값이다. -->

# Distinguishing the mixed conduction interphase: a machine learning molecular dynamics study on the Na₃PS₄/Na battery interface — Li, Jeon & Persson (*Mach. Learn.: Sci. Technol.* **7**, 055011 (2026))

> slug `li2026_mci_vs_sei_na3ps4_na_mlip_md` · DOI `10.1088/2632-2153/aea2f0` · type `calc 전용 (ACE-MLIP MD + VASP AIMD/r²SCAN 라벨 + Onsager GK 후처리 · 실험 0회)` · PDF inbox #132 `litdb/inbox/132. MLST_2026_Li_Jeon_Persson_Distinguishing_mixed_conduction_interphase_Na3PS4_Na_MAIN.pdf` (본문 13 pp · sha256 `a88edb5e35357a88…`) + `litdb/inbox/132. Sup) MLST_2026_Li_Jeon_Persson_Distinguishing_mixed_conduction_interphase_SI.pdf` (SI 15 pp · sha256 `59e995526d416850…`) · 코드 `github.com/BryantLi-BLI/naps-mic` @ **`85557efd5bf6ef62fb23fa584e11e2b79012c625`** (로컬 읽기전용 클론 `/home/user/bryantli-bli/naps-mic`, 우리 repo 로 코드 복사 안 함) · digested `2026-09-23` · status ✅ · 태그 **[외부·Na 계·SEI↔MCI 판별 방법 원전 · ⛔물성 4축 아님(우리 계 값 0)]**

> elements: Na, P, S, Li
> methods: DFT, AIMD, MD, MLIP, EOS

> **저자**: **Bryant Y Li**¹, **Hwidong Jeon**¹, **Kristin A Persson**¹²\* — ¹UC Berkeley MSE · ²LBNL Materials Science Division · 교신 `kapersson@lbl.gov`
> 접수 2026-06-11 / 수정 2026-08-18 / 수락 2026-09-04 / **게재 2026-09-14** · OPEN ACCESS CC BY 4.0 · refs **53** (SI refs 5) · 연구비 DOE **ESRA**(Energy Innovation Hub) + Battery Materials Research(CMEI, Contract DE-AC0205CH11231) · NERSC DOE-ERCAP0026371
> ⛔⛔ **저자 혼동 금지**: 이 논문의 **Hwidong Jeon (Berkeley)** 은 우리 `jeon2026_concerted_li_motion_argyrodite_assi` 의 **Taegon Jeon (부경대)** 과 **다른 사람**이다. 1저자 **Bryant Y. Li** 도 우리 litdb 의 `[Li25]`(CuBr₂ 도핑) · `[Li26NaRev]`(`li2026_na_sulfide_halide_interface_review`) · `[Li26FDI]`(`li2026_functionally_differentiated_interphase`) 의 Li 와 **무관**하다.
> 🎤 **talk 대기열: 해당 없음** — `talks/lee2026_skku_mlip_materials_design.md` §99-10 에 이 논문이 없다(2026-09-23 확인). 덱과 어긋나는 것도 없다.
>
> **계보**: Hartmann 2013 (ref 3, **MCI 개념의 원전** — NASICON‖Li) → Wenzel 2016 *ACS AMI* (ref 6, **Na₃PS₄‖Na EIS 35 h 선형 저항 증가**) → **Li, Karan, Kaplan, Wen & Persson 2025 *J. Phys. Chem. C* 129, 16043** (ref 19 = SI ref 5, **같은 그룹의 Li₇P₃S₁₁‖Li MLIP-MD — 이 논문의 비교 대조군 전부가 여기서 온다**) → Karan et al. 2026 *Nat. Mater.* (ref 37, Onsager 방법) → **본 논문**.
> ⚠ **ref 19 는 우리 litdb 에 없다.** 그리고 `[Li25]`(우리 약칭)와 **다른 논문**이다 — 이 digest 에서는 **"Li2025JPCC(ref 19)"** 로만 부른다.

---

## 0. 이 digest 를 읽는 법 — 1저자 지정 읽기축 (2026-09-23)

| 순서 | 절 | 묻는 것 |
|---|---|---|
| ① 🔴🔴 | **§9** | **이 논문이 자기제한을 동역학으로 보였나** → 우리 `kb/concepts/cv_vs_dqdv_and_two_windows.md` §8-4 를 고쳐야 하나. **한 줄 결론은 §9-5** |
| ② | **§10** | 세 판별 특징(P–P 상관 · 비정질 Na₂S · Na–P 연결)이 **원인인가 신호인가** |
| ③ ⭐ | **§11** | `chaney2024` 와 정면 대조 — **결정성이 SEI/MCI 판별자인가**, 명시인가 우리 유도인가 |
| ④ 🔴 | **§12** | "혼합전도" 의 **전자 쪽**을 무엇으로 판정했나 |
| ⑤ | **§13** | 우리 **Li₆PS₅Cl‖Li** 로 옮겨지나 — 옮겨지는 것 / 안 되는 것 |
| ⑥ | **§4 · §14** | MD·MLIP 규약 전수 + 우리 규약과 나란히 |
| ⑦ | **§18** | 우리에게 **불리한** 결론 |
| — | §19 | SI·코드로 채운 것 / **여전히 못 채운 것** |
| — | §20 | 본 그림 / 안 본 그림 |

⛔ **이 편의 수치는 전부 소환값이고 Na 계다.** 우리 `db/properties/*.json` 절대값과 같은 표에 놓지 않는다.
⛔ **포텐셜 원소가 `Na·P·S` 뿐이다**(`mlip/input.yaml` L15 · `mlip/potential.yaml` speciesblock 12개 전부 Na/P/S 조합) — **Li 도 Cl 도 없다.** 이 포텐셜로 Li₆PS₅Cl 은 물리적으로 못 돌린다. 옮길 수 있는 것은 **판별 지표와 분석 코드의 설계**뿐이다(§13).
⭐ **이 편에서만 얻는 것**: SEI↔MCI 를 MLIP-MD 로 가르려는 **첫 명시적 시도**와, 그 시도가 **코드 수준에서 무엇을 재고 무엇을 못 재는지**의 전모. 우리 litdb 에서 **"안 멈추는 쪽" 대조 사례**가 들어온 것도 처음이다.

---

## 1. 한 줄 요약

**자체 학습한 ACE MLIP(원소 Na·P·S, r²SCAN 라벨)로 Na₃PS₄‖Na 계면을 50만 원자·10.5 ns·300 K NpT 로 돌려**, 계면상이 **log 모양으로 느려지지만 멈추지 않고** Na 금속 쪽으로 자란다고 보고한 뒤, 같은 그룹의 선행 **Li₇P₃S₁₁‖Li(Li2025JPCC, ref 19 — 이 논문에서 다시 돌리지 않았다)** 와 비교해 **세 가지 표지** — (1) 비정질 대리조성의 Onsager 계수에서 **P–P 항이 지배적**(L_PP = 16.68×10²⁰ (eV·cm·s)⁻¹) (2) **Na₂S 가 장거리 질서 없이 비정질**(τ 0.28 vs 결정 1.35) (3) **Na–P 결합그래프가 0.23 ns 부터 관통해 99.8 % 유지** — 를 **"MCI 와 부합, 자기제한 SEI 와 불부합"** 이라고 정리한다. 저자 스스로 **"necessary but not sufficient"**, **"definitive classification requires direct electronic conductivity measurements"** 라고 못박는다. **전자 전도는 한 번도 계산하지 않았다.**

---

## 2. 메타 / 동기 / 이 논문이 묻는 것과 안 묻는 것

**동기 (본문 축자 정리).** 계면상 분류는 둘이다 — **SEI**: *"ionically conductive but electronically insulating … thereby rendering the interphase self-limiting"* / **MCI**: *"conducts both ions and electrons, enabling continuous electron supply … sustaining propagating decomposition"* (ref 3 Hartmann 2013). Na₃PS₄ 분해산물(NaP·Na₃P·Na₂S)이 전자를 흘려 MCI 로 자라는지, SEI 로 부동태화하는지 **논쟁 중**이다(ref 6). AIMD 는 10–100 ps·수백 원자라 성장을 못 본다 ⇒ **능동학습 MLIP**.

**묻는 것 셋** (본문 §1 끝): ① 분해산물의 구조·형태 변화 ② **Onsager 수송 분석**으로 종간 상관 ③ **연결경로(connectivity)** 로 전자전도상 퍼콜레이션 가능성.

**묻지 않는 것 (중요 — 기대하고 갔다가 못 받는 것)**
- **전자 전도·밴드갭·DOS 를 이 계에서 계산하지 않는다.** 표 1 의 갭은 **전부 문헌 인용**이다(§12).
- **전기장·전위·전류가 없다**: *"the interatomic potential is **not charge-aware**, and neither an external electric field nor an explicit electrochemical potential is imposed."*
- **Li₇P₃S₁₁‖Li 를 이 논문에서 돌리지 않았다.** `Fig. 2` 청록 점선 · `Fig. 3b` · `Fig. 4b,d` 는 전부 ref 19 에서 온다(캡션 *"Reprinted with permission from [19]"* · SI `Table S5` 열 머리 *"Li₇P₃S₁₁/Li [5]"*). 포텐셜에 Li 가 **없다**.
- **성장 법칙을 적합하지 않는다.** "logarithmic" 은 서술어이고 적합선·계수·잔차가 본문·SI·코드 어디에도 없다(코드의 성장률은 **유한차분** `interphase_analysis.py` `compute_growth_rate` L772–797).
- **절대 성장속도를 주장하지 않는다**: *"the reaction kinetics observed here are **undeniably faster than expected** from room-temperature experiments"* … *"we do not claim to predict quantitatively."*
- **조성축·도핑축이 없다.** Na₃PS₄ 단일.

**서지 · 자료 공개**
- 본문 `Fig. 1`–`6` + `Table 1` · SI `Fig. S1`–`S14` + `Table S1`–`S5`.
- *"datasets … including the training dataset and the interphase trajectories, are available on MPContribs"* (본문) vs 저장소 README *"(public upon publication)"* — ⚠ **지금 공개됐는지 우리는 확인 안 했다.**
- ⚠ **저장소 README 는 낡았다** — *"Machine Learning: Science and Technology (in review)"* · *"DOI to be added upon publication"* · 그림 번호도 투고본 기준(README 의 *"Percolation (Fig. 4…)"*·*"Onsager transport (Fig. 3…)"* 가 게재본에서는 `Fig. 5`·`Fig. 4`). **README 와 게재 논문이 충돌하면 게재 논문이 이긴다.**
- ⚠ **Onsager 핵심 계산은 비공개 패키지 `py_oats`**(Vir Karan 관리, PyPI 없음 — `analysis/README.md` L31–33)에 있다. 저장소의 `analysis/onsager/` 는 **드라이버**뿐이다.

---

## 3. 핵심 수치 총정리 ★

### 3a. 계 제원 — 본문·SI·코드 + ✎ 우리 정합성 검산

| 항목 | 값 | 출처 |
|---|---|---|
| 원자수 | **500,000** (≈) | 본문 §2.3 · SI `Table S5` |
| 계면 방위(생산 런) | 🔴 **어디에도 없다** | Li 쪽은 *"(100)/(100)"* 인데 Na 쪽 칸은 방위 없이 *"500,000 atoms"* 만 (`Table S5`) |
| 계면 제작 | pymatgen `CoherentInterfaceBuilder`, Zur–McGill 변형 최소화 | 본문 §2.1 · `md/README.md` |
| 옆면 크기 | **≈137 Å × ≈137 Å** (figure-read ≈) | `Fig. 5b` x 축 0–≈137 Å · `Fig. 5a` x·y 0–≈135 Å |
| z 셀 길이 | **≈842 Å** | 코드 주석 `interphase_analysis.py` L53 *"≈ 5 Å at 842 Å cell"* |
| 궤적 저장 | **1060 프레임 / 10.5 ns = 10 ps 간격** | SI `Fig. S14` 캡션 · 코드 `time_per_frame=0.01` ns |
| 전해질 쪽 | **높은 z** (z_frac > 0.60) | `percolation.py` L42–44 주석 |

✎ **정합성 검산 (논문 미보고)**: 137 × 137 × 842 Å³ ≈ **1.58×10⁷ Å³** → 50만 원자면 평균 **≈0.032 원자/Å³**. bcc Na(≈0.025)와 Na₃PS₄(≈0.047, 입방 a≈7.0 Å, Z=2 로 대략 계산)의 **사이 값**이라 세 숫자(원자수·figure-read 옆면·코드 주석 z)가 서로 모순되지 않는다. ⚠ 두 벌크 밀도는 문헌 격자상수 기억값으로 잡은 대략치다.

### 3b. MLIP 정확도 — 본문 + SI `Table S1`·`S2` (**PDF 텍스트 전사**) + 코드

**학습셋 (`Table S1`)**: 계면 **3,097** + 비정질/무질서(MPMorph) **9,031** + 결정상(열 샘플) **7,986** = **20,114** (필터 전 **>24,000**).

**전체 오차 (본문 §3.1)**: 에너지 RMSE **39.64 (train) / 36.46 (test) meV/atom** · 힘 RMSE **171.58 / 188.79 meV Å⁻¹**.

**조성·힘 분해 오차 (`Table S2`, 20,114 전체, 원소별 기준 정렬 후)** — 굵게 = 이 digest 의 판정에 쓰는 행

| 조성 | 힘 층 | N | E MAE | E RMSE | F MAE | F RMSE |
|---|---|---|---|---|---|---|
| Na 금속 풍부 | 전체 | 1979 | 20.6 | 24.9 | 20.8 | 41.8 |
| Na–P 이원 | 전체 | 9227 | 26.4 | 35.0 | 120.8 | 192.7 |
| **Na–S 이원** | **전체** | **3344** | **40.9** | **58.5** | 48.4 | 120.7 |
| **Na–S 이원** | **반응(\|F\|≥3)** | **480** | **54.8** | **99.3** | 150.2 | 269.5 |
| Na–P–S 삼원 | 전체 | 5564 | 26.1 | 36.9 | 126.1 | 210.4 |
| **전체** | 전체 | 20114 | 28.2 | **39.6** | 100.4 | **178.5** |

(단위 meV/atom · meV Å⁻¹. 반응 층 = 최대 힘 ≥ 3 eV Å⁻¹, 코드 `validation.py` L30 `FORCE_THRESHOLD = 3.0`.)

- 🔴 **에너지 오차가 가장 큰 조성이 Na–S 이원(RMSE 58.5, 반응 층 99.3)이다** — 하필 특징 (2) "Na₂S 가 결정화 안 한다" 가 서 있는 화학이다(§10-2).
- 🔴 **"힘 80 meV Å⁻¹ 초과 배열을 걸렀다" 는 문자 그대로 읽으면 자기 표와 모순이다.** 본문 §3.1 과 SI S1.1 이 둘 다 *"filtering configurations with maximum site-wise force magnitudes exceeding **80 meV/Å**"* 라고 쓰는데, `Table S2` 에 **최대 힘 ≥ 3 eV Å⁻¹(= 3000 meV Å⁻¹) 인 배열이 6+2164+480+1942 = 4,592 개** 있다. 게다가 80 meV Å⁻¹ 로 걸렀다면 힘 RMSE 172 meV Å⁻¹ 가 **데이터 최대 힘보다 크다** — 힘을 0 으로 예측해도 그보다 낫다. ⇒ **단위 오기(80 eV Å⁻¹?) 로 보인다. 학습셋 구축 코드가 저장소에 없어 확인 불가.**
- ⚠ 힘 RMSE "전체" 가 표는 **178.5**, 본문 train 은 **171.58** — ✎ 코드 `validation.py` L98 이 **구조별 RMSE² 를 구조 단위로 평균**(원자 수 가중 아님)하므로 전역 성분 평균과 약간 갈린다. 실질 문제 아님.
- **SI S1.7 의 방어**: ACE 는 50만 원자·10 ns 를 돌리기 위해 **의도적으로 가벼운 모델**을 골랐고, 반응·비정질 배열은 **r²SCAN 라벨 자체가 흔들린다**(label noise) — *"the conclusions of this work are qualitative."*

**참고 대조 (전부 소환값, 같은 축에 놓지 말 것)**: Li2025JPCC 의 Li 포텐셜 **119.5 meV/atom · 269.8 meV Å⁻¹**(PBEsol 라벨, `Table S5`) · `[Chaney24SEI]` MTP 18.4/20.9 meV/atom(에너지만) · `[Wang22Res]` MTP 학습 MAE 0.32–0.87 meV/atom.

**검증 그림 (SI)**
- `Fig. S3` EOS: 부피·체적탄성률은 겹치는데 **최저 에너지가 조성에 따라 어긋난다** — figure-read ≈ **Na₃PS₄·Na₂PS₃ 는 ACE 가 DFT 보다 ≈0.25–0.3 eV/atom 낮고 Na₂S ≈0.13 eV/atom 낮으며**, NaP·Na₃P·Na₃P₁₁·Na 는 거의 겹친다. ✎ 이 패턴(S 많을수록 더 낮음)은 **원소별 기준에너지 차**로 상당 부분 설명될 수 있고 그 부분은 반응에서 상쇄된다 — 그러나 그림 판독 정밀도(±0.03–0.05)로는 **남는 부분을 확정 못 한다**. 본문 §3.1 도 *"deviations in … ground-state energies for Na, Na2PS4, and Na3PS4"* 를 인정한다(⚠ `Na2PS4` 는 `Fig. S3` 에 없고 Na₂PS₃ 만 있다 → 오기로 보인다).
- `Fig. S4` 이량체: **Na–S 꼬리를 ACE 가 과소평가** — figure-read ≈ DFT **≈−1.1 eV @4 Å · ≈−0.6 @5 Å · ≈−0.2 @7 Å**, ACE 는 ≈4.5 Å 이후 **거의 0**. SI 방어: *"long-range interactions are dominated by electrostatics in the condensed phase."* ✎ 우리 판단: Na₂S 반형석의 **둘째 Na–S 껍질이 5.4 Å** 라 이 과소평가는 정확히 장거리 질서(결정화) 구동력이 걸린 거리대다(§10-2, 가설).
- `Fig. S6` RDF 검증(결정상 8종 300 K) — ⛔ **추출기가 못 잘랐고 우리가 안 봤다**(§20).

**능동학습 γ (D-optimality 외삽등급)**: 10 스텝마다 평가 · **γ > 1.5 표시·학습셋 추가 · γ > 5 중단**(본문 §2.3·§3.1, `Table S5`). Li 쪽은 *"1 < γ < 2.5; 3 iterations"*. 🔴 **생산 궤적의 γ 통계(최댓값·표시 비율·중단·재학습 여부)는 0 건** — LAMMPS 입력이 저장소에 없고(`md/README.md` *"HPC job scripts are not included"*), `validation.py` 는 활성집합을 **불러오기만** 하고 γ 를 계산·보고하지 않는다(L60–61). ⇒ **"감시했다" 는 본문 서술로만 확인된다.** ⚠ 그리고 *"flagged and added to the active learning dataset"* 이 생산 중 재학습을 뜻한다면 **10.5 ns 궤적이 한 퍼텐셜로 만들어졌는지**도 불명이다.

### 3c. 열역학 — MP r²SCAN (본문 §3.2 · SI `Table S3`·`Table S4`, PDF 텍스트 전사)

**`Table S3` 반응산물 (Na₃PS₄ + Na, 원자당)**: NaP **−0.465** ("Yes") · Na₃P₁₁ −0.456 · NaP₇ −0.451 · Na₃P **−0.443** · Na₂PS₃ −0.137 eV/atom. 본문: 바닥 반응 **`Na₃PS₄ + 6Na → NaP + 4Na₂S`**, 대응 Li 반응 **−0.78 eV/atom**(ref 19). Na–P 족은 **≈20 meV/atom 안**에 몰려 있다(표에서 NaP–Na₃P 폭 22 meV/atom).

✎ **정규화 규약 주의 (논문 미보고)**: "바닥 반응 = NaP" 는 **원자당 최저**라는 MP 계면반응 규약의 선택이다. **Na₃PS₄ 화학식단위당**으로 환산하면 NaP 경로 −0.465 × 14 원자 = **−6.51 eV**, Na₃P 경로 −0.443 × 16 원자 = **−7.09 eV** — **Na 가 넘치는 금속 접촉에서는 완전환원 Na₃P(8 e⁻)가 더 발열적**이다(NaP 는 P⁵⁺→P⁻ 6 e⁻ 부분환원). 이것은 `li2026_na_sulfide_halide_interface_review` digest 의 `Na₃PS₄ + 8 Na → Na₃P + 4 Na₂S` 와 같은 방향이고, 우리 `HZ-anode-b2o3-reaction-direction`(원자당 vs 금속 과잉 규약) 과 **같은 종류의 함정**이다. ⇒ 본문의 **"−0.465 vs −0.78 eV/atom" 구동력 비교도 정규화 의존**이다.

⚠ **MLIP 오차와 비교하면**: Na–P 족 폭(≈22 meV/atom) < 포텐셜 에너지 RMSE(Na–P 이원 35.0) ⇒ **MLIP 는 어느 Na–P 상이 생기는지 가를 수 없다.** 본문 스스로 Na₂S 결정화 대안 설명으로 *"limitations of the MLIP in resolving such small energy differences"* 를 든다.

**`Table S4` 화학퍼텐셜 차 Δμᵢ = μᵢ(Na 쪽) − μᵢ(Na₃PS₄ 쪽) (eV)**

| T (K) | Δμ_Na | Δμ_P | Δμ_S |
|---|---|---|---|
| 0 | +1.232 | **−0.920** | −2.465 |
| 500 | +1.158 | **−0.382** | −2.218 |
| 900 | +1.074 | **+0.121** | −2.148 |
| 1200 | +0.977 | **+0.479** | −1.954 |
| 1500 | +0.720 | **+0.989** | −1.439 |

🔑 **Δμ_P 의 부호가 500 → 900 K 사이에서 뒤집힌다.** 플럭스 그림(`Fig. 4a`·`Fig. S11`)은 **900·1200 K 만** 보여 준다 — 즉 Δμ_P > 0 인 온도다(§10-1 에서 결정적으로 쓰인다).

### 3d. 구조 진화 — `Fig. 2` 원본 래스터 **픽셀 판독** (✎ figure-read ≈)

> 방법: 본문 5쪽 임베디드 이미지(1351×889 px)를 그대로 추출 → 눈금(tick)으로 축 보정(x 41.8 px/ns, 0–10.5 ns · y 36.4 px/nm, ±5 nm) → 청록 점선 픽셀(≈RGB 110,224,205)의 z 위치를 ±5 px 창 중앙값으로, Na 쪽 히트맵 가장자리는 **±0.2 ns 창에서 점유율 ≥ 50 %** 인 최외곽 bin 으로 읽었다. 패널 (a) 회색조는 글상자 테두리가 섞여 가장자리 판독에서 뺐다.

**(i) Li₇P₃S₁₁‖Li 경계(청록 점선, ref 19 에서 가져와 겹친 것) — 네 패널이 서로 조금 다른 선을 쓴다**

| 패널 | 1 ns (위 / 아래, nm) | 10.4 ns | 두께 1 → 10.4 ns | 1→10 ns 금속 쪽 이동 |
|---|---|---|---|---|
| (a) P–P | +2.20 / −1.92 | +2.30 / −2.14 | 4.12 → **4.44** | 0.22 nm |
| (b) Na–S | +2.05 / −2.05 | +2.16 / −2.27 | 4.10 → **4.43** | 0.22 nm |
| (c) Na–P | +2.08 / −2.07 | +2.18 / −2.29 | 4.15 → **4.47** | 0.22 nm |
| (d) P–Na | +1.76 / −2.37 | +1.86 / −2.59 | 4.13 → **4.45** | 0.22 nm |

⇒ **Li 쪽 "평탄" 도 1 → 10.4 ns 에 ≈0.3 nm(≈8 %) 더 자란다.** 0.1 → 1 ns 에는 ≈2.4 nm 가 자라므로 **decade 당 증가가 ≈8배 줄어드는 강한 감속**이지 **정지는 아니다**.

**(ii) Na₃PS₄‖Na 계면상 가장자리 (점유율 ≥ 50 %)**

| 시각 (ns) | (c) Na–P 아래 / 위 (nm) | (d) P–Na 아래 / 위 (nm) |
|---|---|---|
| 0.25 | −2.05 / +1.12 | −2.25 / +0.54 |
| 1 | −2.41 / +1.17 | −2.44 / +0.79 |
| 3 | −2.77 / +1.50 | −2.80 / +0.90 |
| 5 | −2.88 / +1.53 | −2.99 / +1.14 |
| 10 | **−3.15** / +1.56 | **−3.18** / +1.14 |

⇒ ✎ **금속 쪽 가장자리가 1 → 10 ns 에 ≈0.74 nm 이동 = decade 당 ≈0.6–0.75 nm 로 거의 일정** (0.25 → 1 ns 도 ≈0.36 nm/0.6 decade ≈0.6 nm/decade) — **log 법칙과 부합**한다. (c) 기준 두께 3.58 → **4.71 nm (+32 %)**.
⇒ 🔑 **"Li 는 멈추고 Na 는 안 멈춘다" 는 이 그림에서 "금속 쪽 decade 당 성장이 ≈0.22 vs ≈0.74 nm — 약 3–4배 차이" 이고, 관측 창은 1–10 ns 한 decade 뿐이다.** 절대 두께는 10 ns 에 Na ≈4.7 vs Li ≈4.4–4.5 nm 로 **비슷하고**, **≈3 ns 까지는 Na 쪽이 오히려 얇다**(패널 c: 1 ns 3.58 vs 4.15 · 2 ns 3.80 vs 4.20 · 3 ns 4.27 vs 4.24 nm). ⚠ 두 계의 가장자리 정의가 다르고(Na 는 우리 50 % 문턱 · Li 점선은 정의 미상, 범례의 `*` 설명 없음) 셀·포텐셜·열욕도 다르다(§9-3).

### 3e. 결정성 — SI S4.1·`Fig. S12` + 코드 `analysis/crystallinity.py` + `Fig. 3`

| 지표 | 계면상 Na₂S | 결정 Na₂S | 비 |
|---|---|---|---|
| 첫 Na–S 껍질 | **2.80 Å** | 2.82 Å | — |
| 2·3차 봉우리 높이 / 첫 봉우리 | **0.27** | **0.82** | ≈3.0배 |
| τ = (1/7)∫₃¹⁰\|g−1\|dr | **0.28** | **1.35** | ≈4.8배 ("∼5-fold") |

**코드가 실제로 하는 일 (`crystallinity.py` @85557ef)**
- 슬랩 = **고정 z 창 [460, 490) Å 의 Na·S 원자만**(L60 `el in ("Na","S")`) — **P 는 조성 필터 없이 그냥 뺀다.** SI 의 *"x_P < 0.01"* 은 코드가 **검사하지 않는다**(Na:S 비만 출력, L109–111).
- 그 30 Å 슬랩을 **z 방향으로도 주기적인 격자**로 만든다(L64–66 `Lattice.from_parameters(lx, ly, c=zmax−zmin, …)`) — 슬랩 위아래 면이 **인공적으로 붙는다**. ✎ 3–10 Å 껍질 쌍 중 면을 넘는 비율은 r/60(10 Å 에서 ≈17 %) 이라 **τ 를 ≈10–17 % 낮추는 정도**의 인공물이다(주효과 아님).
- 결정 기준 = **정적 CIF**(`reference/Na2S.cif`, a = 6.498 Å, 반형석) 4×4×4 에 **σ = 0.1 Å 스미어링만**(L31, L115–117) — **열진동이 없는 0 K 격자**다. `Fig. S12` 의 빨강 곡선이 봉우리 사이 **g = 0** 인 것이 그 증거다.
- **최종 5 프레임 한 시점뿐** — 결정성의 **시간 변화는 계산하지 않았다**. 본문의 *"remain amorphous **throughout** the 10 ns"* 는 `Fig. 3` 시각 판독 + *"reproducible across repeated simulations"*(횟수 미기재)가 근거다.
- **Li₂S 쪽 τ 는 없다** — Li 계 결정성은 ref 19 의 그림(`Fig. 3b`) 시각 판독뿐이다.

✎ **기준을 정적 격자로 잡으면 "5배" 가 얼마나 부풀려지나 — 우리 구현으로 재현 (논문 미보고, scratch 계산)**
같은 정의(σ 0.1 Å · 3–10 Å · a = 6.498 Å)로 **정적 격자 τ = 1.347, 꼬리비 0.817 을 재현**했다(저자 1.35 / 0.82). 여기에 **원자마다 독립 가우스 변위**(Einstein 근사, 축당 RMS u)를 주면:

| u (Å/축) | 0 | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 |
|---|---|---|---|---|---|---|
| τ | 1.347 | 1.251 | 1.056 | **0.859** | **0.667** | 0.509 |
| 꼬리비 | 0.817 | 0.815 | 0.815 | 0.805 | 0.814 | 0.802 |

⇒ 300 K 결정의 실제 u 를 우리는 모른다(측정·계산 안 함). 다만 **u ≈ 0.15–0.20 Å 만 돼도 τ 비는 ≈4.8배 → ≈2.4–3.1배**로 준다. **꼬리비(0.27 vs ≈0.81, ≈3배)는 이 변위에 거의 안 흔들리므로 더 튼튼한 지표다.** ⚠ 독립 변위 모형은 상관운동을 무시한다.
⇒ **"계면상 Na₂S 가 결정보다 훨씬 무질서하다" 는 선다. "∼5배 억제" 라는 크기는 0 K 기준 탓에 부풀려졌다.**

**그림이 말하는 것 (실독)**
- `Fig. 3a`(Na): **빨간 타원 1 개** — 나노결정 도메인이 **하나 있다**. `Fig. 3b`(Li, ref 19): **타원 7 개**. 축척·시각·절단 방향 표기 없음.
- `Fig. 6` 도식: **"Crystal Na₂S" 조각**을 비정질 Na₂S 안에 직접 그려 넣었다.
- `Fig. S12`: 계면상 곡선(파랑)에 **결정 봉우리 위치(≈5.5·7.1·≈9.5 Å)와 겹치는 약한 봉우리**가 남는다.
⇒ 🔴 **초록 *"amorphous Na₂S domains lacking nanocrystalline order"* 와 본문 *"remain amorphous throughout"* 는 자기 그림보다 강하다.** 그림이 보이는 것은 **"나노결정이 드문 대부분 비정질"** 이다 — 차이는 **유무가 아니라 정도**다.

### 3f. Onsager 수송 — 본문 §2.4·§3.3 · `Fig. 4` · SI S3 · `Fig. S11` · 코드 `analysis/onsager/`

**정의 (본문 Eq. 1, SI `Table S5` 가 "Green–Kubo (differential form)" 라 부르는 Einstein 형)**
Lᵢⱼ = [1/(6k_BTV)] lim d/dt ⟨Σ_α Δr_α^i · Σ_β Δr_β^j⟩ · 플럭스 **Jᵢ = −Σⱼ Lᵢⱼ ∇μⱼ** (SI Eq. S7 · 코드 `onsager_plotting.py` `get_flux` L124–146 `-np.dot(L, mu)`, L 표준편차로 1000회 몬테카를로). 양(+) 플럭스 = **음극(Na 금속) 쪽**.

**행렬 (`Fig. 4c` Na, `Fig. 4d` Li — 그림에 인쇄된 수, 조성족 평균 |Lᵢⱼ|, SI S3.2 *"average of the coefficient magnitudes |Lij| over the amorphous structures … at the reference temperature"*)**

| 조성족 | L_{M,P} | L_{P,P} | L_{P,S} | 컬러바 단위 |
|---|---|---|---|---|
| Na: Na–P | 1.91 | **16.68** | 0.00 | **×10²⁰** (eV·cm·s)⁻¹ |
| Na: Na–P–S | 5.85 | 6.95 | 1.55 | ×10²⁰ |
| Na: P–S | 0.00 | 1.07 | 0.60 | ×10²⁰ |
| Li: Li–P | **2.362** | 0.523 | — | **×10¹⁸** (eV·cm·s)⁻¹ |
| Li: Li–P–S | 0.313 | 0.025 | 0.049 | ×10¹⁸ |
| Li: P–S | — | 1.135 | 1.097 | ×10¹⁸ |

(⚠ "reference temperature" 가 몇 K 인지 본문·SI·코드 어디에도 없다.)

**플럭스 figure-read ≈ (`Fig. 4a`·`Fig. S11`, 900 / 1200 K, mmol cm⁻² s⁻¹)**
- **P**: NaP₁₅ **≈0.034 / ≈0.026** (최대) · NaP₅ ≈0.009 / ≈0.011 · Na₃P₄S ≈0.004 · P–S 조성 전부 ≈0 ~ −0.004.
- **Na** (`Fig. S11` 가운데): 크기 ≤ ≈0.004, **조성·온도마다 부호가 바뀐다**(예: Na₄P₃S +0.0037 / −0.0038). **NaP₁₅ ≈0.000 (900 K) / ≈+0.0015 (1200 K)** · NaP₅ ≈+0.003 / ≈+0.0014.
- **S**: 대부분 양(+), 최대 P₂S₃ ≈0.0036 (1200 K).
- ⚠ **Na 쪽 그림에 오차막대가 안 보인다**(범례에는 오차막대 기호가 있다). Li 쪽(`Fig. 4b`, ref 19)에는 있다.

**본문 주장**: Na–P 조성의 **L_PP 가 행렬 지배항**이고 *"exceeding the Li system by approximately an order of magnitude"* → *"collective P motion … coordinated transport toward the Na metal"*. Li 쪽은 L_LiP·L_PS 가 비슷해 **경쟁**하고, *"P–S coupling stems from anticorrelated motion … this anti-correlation **traps P** within the interphase."* 원인 가설: Na⁺ 가 커서(0.95 vs Li⁺ 0.60 Å) 음이온 반발을 가린다.

✎ **우리 검산 4건 (논문 미보고 — 전제는 각 줄에 적었다) — 이 절이 feature (1) 판정의 핵심이다**
1. 🔴 **단위: "약 한 자릿수" 는 지수를 빼고 비교한 값이다.** 인쇄된 수만 보면 16.68 / 2.362 = **7.1배**("약 한 자릿수")인데, 컬러바대로 지수를 넣으면 16.68×10²⁰ / 2.362×10¹⁸ = **≈706배**(L_PP 끼리는 16.68×10²⁰ / 0.523×10¹⁸ ≈ **3,190배**). **본문과 그림 중 하나는 틀렸다.**
2. 🔴🔴 **운동량 보존 검사 — Li 행렬은 통과, Na 행렬은 실패.** 총운동량이 0 으로 보존되는 MD(Nosé–Hoover 는 보존)에서 **이원 조성**이면 Σᵢ mᵢ ΣΔrᵢ = 0 이 매 순간 성립하므로 교차항이 **질량비로 강제**된다: A–B 이원에서 |L_AB| / L_BB = m_B/m_A.
   - Li: **P–S 행** |L_PS|/L_PP = 1.097/1.135 = **0.9665** vs m_P/m_S = **0.9661** (차이 0.05 %) · **Li–P 행** L_PP/|L_LiP| = 0.2214 vs m_Li/m_P = 0.2241 (차이 1.2 %).
   - Na: **Na–P 행** L_PP/|L_NaP| = 16.68/1.91 = **8.73** vs m_Na/m_P = **0.742** → **11.8배 위반** · **P–S 행** |L_PS|/L_PP = 0.561 vs 0.966 → **1.7배 위반**.
   ⇒ **같은 "Green–Kubo 형식" 이라는 SI S5 의 주장이 숫자로 지지되지 않는다.** Li 행렬은 질량중심 기준틀에서 계산된 모양이고, Na 행렬은 그렇지 않다. 원인(다른 기준틀 · 질량중심 표류 미제거 · 조성족 집계 방식 · 값 오류)은 **핵심 적분이 비공개 `py_oats` 안이라 판정 불가**다. 가능한 원인 하나로 **질량중심 표류가 섞이면 P 가 94 % 인 NaP₁₅ 에서 L_PP 가 부풀려진다**(✎ 추정일 뿐).
3. 🔴 **플럭스도 같은 방향으로 어긋난다.** 질량중심 기준틀이면 Σᵢ Mᵢ Jᵢ = 0 이어야 한다(J = −L·Δμ 가 그 성질을 보존한다). 그런데 figure-read **NaP₁₅ (900 K): J_P ≈ +0.034 인데 J_Na ≈ 0.000** · **NaP₅ (900 K): J_P ≈ +0.009, J_Na ≈ +0.003 — 둘 다 양(+)**. ⇒ **셀 전체 질량이 음극 쪽으로 흐르는 값**이다. 운동량 보존 계에서 나올 수 없다.
4. 🔴 **부호: 900·1200 K 에서 L_PP 항은 P 를 *전해질 쪽*으로 민다.** Jᵢ = −Σⱼ Lᵢⱼ Δμⱼ 와 `Table S4` 의 Δμ_P > 0 (900 K +0.121 · 1200 K +0.479) 를 그대로 쓰면 −L_PP·Δμ_P < 0 이다. 같은 규약에서 Na 는 전해질 쪽(Δμ_Na > 0), S 는 음극 쪽(Δμ_S < 0) 으로 가서 **물리적으로 말이 맞으므로 규약 해석은 옳다.** ⇒ `Fig. 4a` 의 **음극향 P 플럭스는 L_PP 가 아니라 Na–P 교차항(−L_{P,Na}·Δμ_Na, L_{P,Na} < 0)에서 와야 한다.** 조성족 평균 행렬로 재구성하면 900 K 는 두 항이 **거의 상쇄**(2.05 vs 2.02)되고 **1200 K 는 L_PP 항이 이겨 음(−)** 이 나와야 하는데 그림은 **양(+)** 이다. ⇒ **"P–P 상관이 음극향 협동 이동을 가능케 한다" 는 결론은 자기 입력(Δμ 표·흐름식)과 맞지 않는다.** 조성별 L 값이 공개되지 않아(`get_flux` 가 읽는 CSV 가 저장소에 없다) 더 좁힐 수 없다.

**그 밖에 (코드에서 확인)**
- 드라이버는 **`L_tensor` 와 `L_tensor_self` 를 따로 뽑는다**(`onsager_processing.py` L45–46) — 즉 **self 항과 distinct 항을 가를 수 있었는데 논문은 L_PP 를 나누지 않았다.** 게다가 본문 §2.4 는 *"the diagonal terms Lii describe **self-diffusion**"* 이라고 쓰고 §3.3 에서는 같은 L_PP 를 *"collective P motion"* 의 증거로 쓴다 — **Eq. 1 의 대각항은 self + distinct 합이라 둘 다 반만 맞다.** L_PP > 0 은 정의상 항상 성립(분산)하므로 *"This **positive** correlation indicates collective P motion"* 은 증거가 되지 못한다.
- 궤적은 **XDATCAR**, `time_step=1`, `step_skip=1000`(1 ps 간격)으로 읽는다(L22–28).
- **Li 쪽 "P 를 가두는 P–S 반상관"** 은 검산 2 에서 보듯 **운동량 보존이 강제하는 역류와 수치상 똑같다**(0.05 %). `marcolongo_ionic_correlations_failure_nernst_einstein` digest §4-3 의 **② 유형("골격 역류 — 빼야 한다")** 을 물리 기전으로 읽은 것이다.
- ⚠ 제시된 반경 **Li⁺ 0.60 / Na⁺ 0.95 Å** 는 인용한 Shannon(1976) 6배위 유효반경(Li⁺ 0.76 / Na⁺ 1.02 Å 로 알려짐)과 다르고 Pauling 결정반경과 같다 — ✎ 우리 기억 기반, **원문 대조 권장**.

### 3g. 연결성(퍼콜레이션) — 본문 §2.5·§3.4 · `Fig. 5` · SI S4.2 · `Fig. S13`·`S14` · 코드 `analysis/percolation.py`

**본문 수치**: 컷오프 **Na–P 3.2 Å · P–P 2.5 Å**(결정 기준상 RDF 첫 극소) · 관통 클러스터 **첫 출현 0.23 ns · 이후 프레임의 99.8 %** 유지 · SI: **1035/1060 프레임(97.6 %)**, 최대 연결성분 **Na–P ≈5,000 원자 vs P–P ≈10**, P–P 만의 망은 **어떤 컷오프에서도 관통 0**.

**코드가 실제로 정의하는 "관통" (`percolation.py` @85557ef)**
- 분석창은 **고정**된 z_frac **0.54–0.60**(L35–36) = 코드 주석의 842 Å 로 ✎ **≈455–505 Å(≈50 Å)** — `Fig. 5a` z 축 460–500 과 맞다. **시간에 따라 움직이는 계면상 경계를 쓰지 않는다.**
- 노드 = 창 안의 Na·P 전부, 간선 = P–P ≤ 2.5 Å · Na–P ≤ 3.2 Å, **Na–Na 간선 없음**(L345).
- **관통 = 한 성분 안에 z_frac ≥ 0.59 원자가 1개 이상 AND z_frac ≤ 0.55 원자가 1개 이상**(L49–50, L396–418). 코드 주석: *"Source: … bulk Na3PS4 side / Sink: … Na metal side"*.
- ⇒ **`Fig. 5b`·`Fig. 5c` 의 ±1.7 점선("Interphase/Na₃PS₄ Boundary"·"Na/Interphase Boundary")은 검출된 경계가 아니라 이 고정 source/sink 문턱**(0.57 ± 0.02 → ±1.7 nm)이다. 그래서 클러스터 원자가 그 선 **밖**(−2.5 nm·+2.3 nm)에도 있다.
- `Fig. S14` 의 "Z-span … which grows to approach the **full interphase thickness**" 의 "full span" 점선(0.06)은 **분석창 폭**이다 — 지표가 창에서 **구조적으로 포화**한다.
- 컷오프 스윕 범위: P–P 2.0–3.5 Å, **Na–P 2.5–4.0 Å**(L53–54).

**`Fig. S13` 실독**: ① P–P 만: 전 구간 **0 %** ② 혼합망, P–P 스윕(Na–P 3.2 고정): 2.0–3.5 Å 전 구간 **≈91 % 평탄** — **P–P 결합은 관통에 전혀 기여하지 않는다.** 관통은 **Na 를 다리 삼은 Na–P 간선만으로** 성립한다 ③ Na–P 스윕(P–P 2.5 고정): ≤2.9 Å **0 %** → 3.0 Å **≈72 %** → ≥3.1 Å **≈91 % 평탄**.
- ✎ ≈91 % ≈ **10/11** — 스윕이 **≈11 프레임** 표본일 가능성(추정, 논문 미기재; 전 궤적 기준은 97.6 %).
- ✎ **스윕 상단은 "반응 산물의 연결" 을 재지 못하는 구간이다**: 입방 Na₃PS₄ 의 최근접 Na–P 거리는 ≈a/2 ≈3.5 Å(✎ 결정구조 기하, 격자상수 기억값)라 **Na–P ≳ 3.5 Å 이면 반응 안 한 전해질의 Na–P 도 간선이 된다.** 그 구간에서도 관통하려면 P 가 금속 쪽 sink 층까지 와 있어야 하므로 **완전히 자명하지는 않지만**, 거기서의 평탄은 **반응 산물 망의 견고성 증거가 못 된다.** 의미 있는 창은 **3.0–3.4 Å** 이다. SI 가 *"plateaus for Na–P cutoffs ≥3.1 Å"* 을 견고성 근거로 쓰면서 이 점을 적지 않는다.

**`Fig. 5` 실독**: (a) 3D — 파랑 Na·빨강 P 클러스터가 창 전체(z 455–505 Å)를 채움. (b) X–Z 투영 — 클러스터가 **두 띠**(위: ≈−1.2 ~ +2.3, 전폭 / 아래: ≈−2.5 ~ −1.2, x ≈50–125 Å 에만)로 갈리고 그 사이 **z ≈ −1 ~ −1.5 에 원자가 거의 없다.** (c) z 분포 — "Na in cluster" 가 **z ≈ −1.0 ~ −1.2 에서 bin 당 ≈10–20 개로 바닥**. ⇒ **"관통" 은 Na₂S 층을 가로지르는 가는 목 몇 가닥**으로 이어진다(`Fig. 6` 도식의 가는 붉은 실과 같은 그림). 🔴 `Fig. 5b`·`5c` y 축 라벨이 **"Relative Z (Å)"** 인데 범위 ±3 이 창 폭 50 Å 와 맞으려면 **단위는 nm** 여야 한다 — **축 단위 오기**.

**`Fig. S14` 실독**: Na–P 간선 수 **≈9,000 (0.5 ns) → ≈11,000 (2 ns) → ≈12,500 (5 ns) → ≈14,000 (10.5 ns)** — **10 ns 까지 계속 늘어나는 감속 곡선**이다(figure-read ≈). ✎ 이것이 이 논문에서 **반응 진행도에 가장 가까운 단조 지표**인데 논문은 그렇게 쓰지 않는다. 최대 성분 크기 Na–P ≈3×10³–6×10³ (로그축), P–P ≈5 → ≈14.

### 3h. 전자 쪽 — `Table 1` (**PDF 텍스트 전사** · a = 계산 예측 표시)

| 상 | 밴드갭 (eV) | 논문 분류 |
|---|---|---|
| Na₂S | 3.22 [43], 2.99 [44] | Wide-gap insulator [45] |
| NaP | ∼0.74 [46]ᵃ | Semiconducting |
| Na₃P | ∼0.4 [43], 0.8ᵃ [46] | Semiconducting |
| Na₃P₁₁ | 1.66 [46] | Wide-gap semiconductor |
| NaP₇ | 2.0 [47] | Semiconductor |
| Li₂S | 3.24–5.08 [48, 49]ᵃ | Wide-gap insulator |
| **Li₃P** | **3.6 (direct), 2.03 (indirect) [50]ᵃ** | **Wide-gap semiconductor** |

- 본문: *"The electronic conductivity of crystalline Na₃P (12 S cm/1) exceeds that of Na₂S (10⁻¹⁶–10⁻¹² S cm⁻¹) by 13–16 orders of magnitude [46]"* — ⚠ `12 S cm/1` 은 원문 표기 그대로(S cm⁻¹ 의 조판 오류로 보인다). ✎ 12 / 10⁻¹² = 1.2×10¹³, 12 / 10⁻¹⁶ = 1.2×10¹⁷ → **13–17 자릿수**가 맞다(상한 한 자릿수 오기).
- 🔴 **출처가 섞였다**: [44] 는 **Na₂S *단층(monolayer)*** 계산 논문, [47] 은 **TiO₂ 나노튜브 기상성장** 실험 논문, [50] Li₃P 는 **1991 년** ab initio(방법 원문 미확인). ᵃ 표시도 일관되지 않는다([43] Na₃P 0.4 · [44] Na₂S 2.99 는 계산인데 무표시).
- 🔴 **Li₃P 값이 우리와 크게 다르다** — 우리 `db/properties/sei_electronic.json`(QE PBE, fixed-occ nscf) **Li₃P 0.7092 eV**, `sei_products.json` MP **0.70 eV · conductor-LEAK**. **같은 방법(PBE 계열)으로 놓으면 Li₃P 는 논문의 "반도체" Na₃P(0.4–0.8) 와 같은 칸이다**(§12-3, §13). ⚠ 우리 원장 규율: PBE 갭은 **순위로만**, 실험·타 방법 값과 나란히 놓지 않는다.

---

## 4. 계산 방법 — 우리가 같은 축을 흉내 낼 때 필요한 조건 전부 ★ (임무 ⑥)

### 4a. DFT (라벨러 · 학습 데이터)
| 항목 | 값 |
|---|---|
| 코드 | **VASP** (refs 20–25) |
| AIMD 범함수 | **PBEsol**, **비스핀분극**, **NVT Nosé–Hoover**, **dt 2 fs**, **Γ 점만** |
| AIMD 대상 | 결정 초셀 **≈100–200 원자 · 20 ps · 300/900/1500 K** · 비정질/무질서는 **MPMorph(atomate2) 900/1200/1500 K** · 계면 **21 종**(\|h\|,\|k\|,\|l\| ≤ 2, 전 종단, NVT — 온도 미기재) |
| 라벨(정적) | **r²SCAN** 단일점, **ecut 680 eV**, SCF **10⁻⁵ eV**, **스핀분극**, **MatPES r²SCAN 설정과 호환**(ref 18) |
| PAW·k-점(정적) | 🔴 **미기재** |
| 워크플로 | pymatgen · atomate2 · Jobflow · FireWorks |
| 선행 방법 | *"The workflow follows the methodology described by Li et al [19]"* |

### 4b. MLIP — ACE (코드 `mlip/input.yaml`·`mlip/README.md`·`mlip/potential.yaml` 메타)
| 항목 | 값 |
|---|---|
| 모델 | **Atomic Cluster Expansion**, pacemaker **0.2.7**, 평가기 tensorpot · 학습 시작 2025-12-01 (`potential.yaml` 메타) |
| 원소 | **`['Na','P','S']`** — Li·Cl 없음 |
| 기저 | 원소당 **350 함수** · UNARY/BINARY/TERNARY `nradmax [15,3,2,1] · lmax [0,4,2,0]` |
| 컷오프 | **7.0 Å** (`rcut: 7`, cos 컷오프, `dcut 0.01`, 내측 `r_in 0.5 · delta_in 0.5`) |
| 임베딩 | Finnis–Sinclair shifted-scaled, **ndensity 8** |
| 반경 기저 | SBessel, `radparameters [5.25]` |
| 근거리 반발 | **ZBL** (`repulsion: auto` — 학습셋 최단거리에 맞춤) |
| 손실 | 1단계 힘:에너지 **99:1** → 2단계 **95:5** (`kappa: 0.95`) · L1/L2 1e-8 · BFGS · maxiter 2000 · 조기종료 인내 200 |
| 기준 에너지 | Na −2.4717 · P −5.5668 · S −4.6452 eV |
| 학습/시험 | 90:10 |
| 활성집합 | `potential.asi` (D-optimality) — γ 계산용 |
| 정확도 | §3b |
| 공개 | ✅ 포텐셜·입력·활성집합 공개 · 학습셋·궤적은 MPContribs(공개 여부 **확인 안 함**) |

### 4c. MD — 계면 생산 런
| 항목 | 값 |
|---|---|
| 엔진 | **LAMMPS + Kokkos + ML-PACE** |
| 초기화 | **CG 에너지 최소화 → 곧바로 NpT 생산 — 평형화 없음** (*"extended equilibration would initiate decomposition reactions before reaching a converged configuration"*) |
| 앙상블 | **NpT**, 등방 **1 bar** · **Nosé–Hoover 열욕 τ_T 1.0 ps + 압력욕 τ_P 1.0 ps** |
| 온도 · dt | **300 K · 1 fs** |
| 길이 | **10.5 ns** |
| 크기 | **≈500,000 원자** (재현성 주장은 5,000–500,000 원자 · 여러 방위 · 여러 시드 — **개수·결과 미제시**) |
| γ 감시 | 10 스텝마다, 1.5 표시 / 5 중단 (통계 미보고) |
| 반응전선 추적 | **(t, z) 격자별 평균 배위수 히트맵**(P–P · Na–S · Na–P · P–Na, `Fig. 2`) + 코드의 조성 프로파일 경계(§6) |
| 무질서 처리 | 해당 없음(Na₃PS₄ 결정 + Na 금속 → 반응으로 비정질화). 초기 배열 선택·배열 앙상블 **없음** |

### 4d. MD — Onsager 대리조성
| 항목 | 값 |
|---|---|
| 셀 | **200–1000 원자** 비정질 (조성별) |
| 제작 | **용융-급랭**: 300 → **5000 K** (100 ps, NpT 1 bar) → 목표온도로 100 ps 냉각 → 10 ps 밀도 평형 → **NVT 전환** |
| 생산 | **500 / 900 / 1200 / 1500 K × 1 ns**, dt 1 fs, NH τ_T 1.0 ps |
| 보고 | 그림은 **900·1200 K 만** · 행렬은 "reference temperature"(값 미기재) |
| 적합 | MSD 선형영역(창 **미기재**) · 핵심 계산 **비공개 `py_oats`** |
| ⚠ | 용융 **5000 K** 는 학습 온도 최고치(1500 K)의 3배 이상 — 용융 단계에 γ 감시를 걸었는지 **미기재** |

Li 대조군(Li2025JPCC, `Table S5`): ACE 350/원소 · **6.0 Å** · **PBEsol 라벨** · 11,596 배열 · 99:1→90:10 · E RMSE **119.5 meV/atom** · F **269.8 meV Å⁻¹** · γ 1<γ<2.5, 3 반복 · 계면 (100)/(100) 50만 원자 · **NpT + Langevin 열욕** · 300 K · 1 fs · **10 ns** · Onsager 대리조성 **MPMorph ≈100 원자 20 종** · **연결성 분석 안 함**.

### 4e. 🔴 이 논문이 **하지 않은** 것
**전자구조 계산 0 (DOS·갭·Bader·COHP·ELF·폴라론 0)** · **전기장·전위 0** · **NEB 0** · **탄성·phonon 0** · **성장법칙 적합 0** · **Li 계 재계산 0** · **Li 계 연결성 0** · **결정성 시간변화 0** · **300 K 결정 기준 0** · **Onsager self/distinct 분리 보고 0** · **300 K 플럭스 0** · **γ 통계 0** · **다중 시드 결과 제시 0**.

---

## 5. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | MLIP 학습 흐름도 — 계면/무질서/유리 비정질/결정 → r²SCAN DB → 학습 → 정확도·안정성·동역학 검증 → 능동학습 재선택 | 🔧 **능동학습 루프의 표준 그림.** 수치 없음 |
| 2a–d | **(t, z) 배위수 히트맵** — (a) P–P 0–1 회색 (b) Na–S 0–6 보라 (c) Na–P 0–1 분홍 (d) P–Na 0–1 적색 · x 0–10.5 ns · y ±5 nm(위 Na₃PS₄, 아래 Na 금속) · **청록 점선 = Li₇P₃S₁₁‖Li 경계(ref 19)** | ⭐⭐ **이 편의 정본 그림이자 임무 ① 의 원자료.** 픽셀 판독(§3d): **Li 점선도 1→10.4 ns 에 ≈0.3 nm(≈8 %) 자란다** · Na 금속 쪽 decade 당 ≈0.74 vs Li ≈0.22 nm. 🔧 **히트맵 문법(중심원자–이웃종 배위수 z–t 지도)은 우리 계면 MD 에 그대로 이식 가능** |
| 3a,b | 황화물 풍부층 원자 스냅샷 — (a) Na₃PS₄‖Na (b) Li₇P₃S₁₁‖Li (ref 19) · 빨간 원 = Na₂S/Li₂S 대칭 나노결정 | 🔴 figure-read: **(a) 원 1개 · (b) 원 7개** — Na 쪽에도 결정 도메인이 **있다**. 축척·시각·절단 방향 표기 없음 |
| 4a | Na–P–S 조성별 **P 플럭스** 900/1200 K | 🔴 §3f 검산 3·4 의 원자료. 최대 NaP₁₅ ≈0.034 (figure-read ≈) · 오차막대 안 보임 |
| 4b | Li–P–S 조성별 P 플럭스 (ref 19) | ⚠ y 축 음수 눈금에 **마이너스 기호 누락**(0.01·0.02 로 표기) |
| 4c,d | 조성족 평균 \|Lᵢⱼ\| 행렬 — (c) Na **×10²⁰** (d) Li **×10¹⁸** (eV·cm·s)⁻¹ | 🔴🔴 **§3f 검산 1·2 의 원자료** — 지수 차 100배 · **Li 행렬은 운동량보존 질량비를 0.05–1.2 % 로 만족, Na 행렬은 11.8·1.7배 위반** |
| 5a–c | 10 ns Na–P 관통망 — (a) 3D (x,y 0–≈135 Å · z 455–505 Å) (b) X–Z 투영 (c) z 분포 | 🔴 **±1.7 점선 = 고정 source/sink 문턱**(코드), 계면상 경계 아님 · **"Relative Z (Å)" → 단위 nm 오기** · 두 띠 사이 z≈−1.2 **가는 목** |
| 6 | 층상 계면상 도식 — Na 금속(위) / 비정질 Na₃P / **결정 Na₂S + 비정질 Na₂S** / 혼합 Na₃P+Na₂S / Na₃PS₄(아래) + Na–P 연결 클러스터 | ⚠ **"Crystal Na₂S" 를 그려 넣었다**(초록 "lacking nanocrystalline order" 와 긴장) · 위아래가 `Fig. 2` 와 **반대** · 캡션은 금속 옆을 "Na–S-rich layer" 로 적어 도식(금속 옆 얇은 Na₃P)과 어긋남 |
| Table 1 | 산물 밴드갭 문헌 표 | **PDF 텍스트 전사**(§3h). 🔴 **Li₃P 2.03/3.6 eV(1991)** vs 우리 PBE 0.7092 |
| S1 | 학습/시험 에너지·힘 분포 | ⛔ 안 봄 |
| S2 | 패리티 플롯 | ⛔ 안 봄 |
| S3 | EOS 8 상 (r²SCAN 점 vs ACE 선) | ✅ + 확대 1장 — 티오인산염 최저 E ≈0.25–0.3 eV/atom 어긋남(figure-read ≈) |
| S4 | 이량체 6 쌍 | ✅ — **Na–S 4–7 Å 꼬리 과소평가** |
| S5 | 이량체 힘 | ⛔ 안 봄 |
| S6 | 결정상 8 종 RDF (MLIP vs AIMD 300 K) | ⛔ **추출기가 못 잘랐고(그래픽 판정 실패) 안 봄** |
| S7 | 조성·힘 분해 오차 막대 | ⛔ 안 봄 — `Table S2` 텍스트로 대체 |
| S8 | Na–P–S 3원 상도 (r²SCAN, MP) | ⛔ 안 봄 |
| S9 | 화학퍼텐셜 상도 | ⛔ 안 봄 — `Table S4` 텍스트로 대체 |
| S10 | Na₃PS₄‖Na 계면반응 볼록껍질 | ⛔ 안 봄 — `Table S3` 로 대체 |
| S11 | P·Na·S 전 조성 플럭스 900/1200 K | ✅ — **NaP₁₅ J_Na ≈ 0 인데 J_P ≈ 0.034** (§3f 검산 3) |
| S12 | 계면상 Na–S 부분 RDF vs 결정 | ✅ — **결정 기준이 정적(g=0 사이)** · 약한 결정 위치 봉우리 잔존 |
| S13 | 컷오프 스윕 관통확률 3 패널 | ✅ — **P–P 무관(≈91 % 평탄)** · Na–P 3.0 Å 에서 급등 |
| S14 | 관통 상태 · z-span · 최대성분 · 간선 수 vs t | ✅ — **z-span 이 창 폭에서 포화** · 간선 수 10 ns 까지 증가 |
| Table S1 | 학습셋 구성 | 텍스트 전사 (§3b) |
| Table S2 | 조성·힘 분해 오차 | 텍스트 전사 (§3b) |
| Table S3 | 반응산물·반응에너지 | 텍스트 전사 (§3c) |
| Table S4 | Δμ (0–1500 K) | 텍스트 전사 (§3c) |
| Table S5 | Na vs Li 프로토콜 대조 | 텍스트 전사 (§4e) — **Li 계가 다른 논문의 다른 포텐셜·다른 열욕**임을 여기서 확정 |

---

## 6. Post-processing ★

| 기법 | 썼나 | 도구·정의 (코드 @85557ef) |
|---|---|---|
| **(t,z) 배위수 히트맵** | ✅ | 격자 bin 평균 배위수 (`Fig. 2`). 컷오프 **미기재**(본문) |
| **조성 프로파일 경계** | ✅ | `interphase_analysis.py`: bin 0.006 분율(≈5 Å) · **금속 쪽 경계 = P 나 S 가 *하나라도* 있는 첫 bin**(L152–191, 문턱 0) · **전해질 쪽 경계 = 벌크 Na₃PS₄ 조성(3/8·1/8·4/8)과 ±2 % 로 맞는 첫 bin**(L194–250) · 다중 bin 폭·위상 평균판 있음(L432–) |
| **성장률** | ⚠ | **유한차분** d(두께)/dt (L772–797). **log 적합 0**. 플롯 보조함수에 선형 적합(%/ns) 만 |
| **Onsager Lᵢⱼ · 플럭스** | ✅ | 드라이버 `analysis/onsager/` → **비공개 `py_oats`** · J = −L·Δμ, L 정규분포 MC 1000회 |
| **결합그래프 퍼콜레이션** | ✅ | `percolation.py` scipy `cKDTree`+`connected_components` · x,y 만 주기 · 고정창·source/sink (§3g) |
| **Na–S 부분 RDF · τ** | ✅ | `crystallinity.py` pymatgen-diffusion `RadialDistributionFunctionFast`, σ 0.1 Å, r_max 10 Å, 정적 CIF 기준 (§3e) |
| **조성·힘 분해 검증** | ✅ | `validation.py` pyace, 원소별 선형 기준정렬 |
| **MP 상도·계면반응·μ 상도** | ✅ | Materials Project r²SCAN (앱) |
| 시각화 | ✅ | 3D 산점도(`Fig. 5a`, matplotlib 풍) · 원자 스냅샷(`Fig. 3`, 도구 미기재) · README 가 OVITO 용 덤프를 언급 |
| DOS·갭·Bader·COHP·NEB·탄성 | ❌ | 0 |

---

## 7. 결과 — 절별 상세 (그림 실독 포함)

### 7.1 MLIP 성능 (§3.1)
에너지 36–40 meV/atom · 힘 172–189 meV Å⁻¹. 점오차만으로 물리적 동역학이 보장되지 않는다는 점(ref 40)을 인정하고 **시뮬레이션 수준 관측량**(RDF·수송·γ 감시·에너지 표류 없음·밀도 붕괴 없음)으로 보강했다고 한다 — ⚠ **표류·밀도 곡선은 제시되지 않았다.**

### 7.2 구조 진화 (§3.2, `Fig. 2`·`Fig. 3`)
- Na 가 전해질로, P·S 가 금속 쪽으로 이동하며 계면상이 자란다. (a) P–P 배위가 **계면상 중앙, 전해질 쪽으로 치우쳐** 증가. (b) **금속 가까이 Na–S 층**(S 풍부). (c) Na–S 층 자리에서 Na–P 가 비고, **Na–S 층과 금속 사이에 Na–P 풍부 영역**이 따로 생긴다. (d) Na–S 층 안의 P 는 주로 Na 와 배위.
- *"logarithmic growth into the Na metal … slows but does not cease"* vs Li *"plateaus after initial growth, consistent with self-passivating SEI behavior [19]"* — §3d 의 픽셀 판독이 이 대비의 **실제 크기**다.
- Li₂S 는 나노결정 + 날카로운 조성경계, Na₂S 는 10 ns 내내 비정질이라고 쓴다. RDF(SI)로 장거리 질서 ∼5배 억제.
- 비정질의 원인 가설: **구동력 차**(−0.465 vs −0.78 eV/atom). 대안(계면 핵생성에너지 차 · MLIP 한계 · 시간 부족)을 **스스로 배제 못 한다**고 적는다. SI S4.1 은 더 조심스럽다 — *"it should **not** be attributed to reaction energetics alone."* ⚠ 결론 절은 다시 *"consistent with the lower thermodynamic driving force"* 로 돌아간다.

### 7.3 Onsager (§3.3, `Fig. 4`) — §3f 참조. 🔴 우리 검산 4건이 이 절의 논리를 받치지 않는다.

### 7.4 Na–P 연결경로 (§3.4, `Fig. 5`)
- 전자전도는 **폴라론 호핑**일 것인데 비정질에서 ab initio 로 잡기가 너무 비싸서, **Na–P 망의 위상적 연결을 전자 퍼콜레이션의 대리지표**로 쓴다 — *"This analysis assesses **only the structural topology** … and does not explicitly model electronic transport."*
- 관통망 0.23 ns 첫 출현 · 99.8 % 유지 · 컷오프 스윕에도 유지(SI).
- 화학량론적 근거: 산물이 Na₂S + 경쟁적인 Na–P 상들 → 표 1 의 갭 대비 → *"a possible mechanism for MCI behavior in which electrons are transported from the Na metal anode through the Na–P network to the reaction front."* 직접 검증은 *"explicit electronic-structure calculations of the heterogeneous interphase, a highly challenging task"* 로 넘긴다.
- P 플럭스 최대가 P 풍부 조성(NaP₁₅·NaP₅)이라 *"high P mobility enables formation of Na-rich phases (NaP, Na₃P), precisely the phases that constitute the percolation pathways"* — ⚠ **P 풍부 대리조성 → Na 풍부 상 형성** 의 연결은 **논증 한 줄**이지 계산이 아니다. SI S3.2 는 그 P 풍부 조성들이 *"transient … dispersed through the reacting region rather than resolved as a single contiguous band"* 라고 인정한다.

### 7.5 분류 함의 (§3.5, `Fig. 6`)
- 세 표지 → *"consistent with MCI-like behavior, permitting both ionic and electronic transport."*
- 실험 연결: Wenzel 2016 *"linearly increasing interfacial resistance over 35 hours"* → *"interphase continues to grow via electronic transport along the connected Na–P network"* · EIS 는 이온 임피던스만 재므로 전자 병렬경로는 안 보인다. ⚠ **그런데 MD 는 log(감속), 실험 R(t) 는 선형(비감속)** — 함수형이 다른데 둘 다 "MCI 와 부합" 으로 읽는다(§17-⑦).
- 율속 후보 셋: ① 비정질 Na₂S/Na–P 기지 속 Na⁺ 확산 ② 계면상/전해질 경계 반응 ③ 입계·조성경계의 전자 수송 — **판별 못 함**.
- 한계 자인: 속도가 실험보다 빠르다(MLIP 의 확산 과대 경향 ref 51 · 원자적으로 완벽한 계면) · 전기장 무시 · *"topological connectivity and transport correlations as **necessary but not sufficient** conditions for MCI behavior"*.

---

## 8. 메커니즘 종합 — 논문의 논증 사슬과 우리가 보는 약한 고리

```
Na 금속 ‖ Na₃PS₄   (개방회로 · 전압/전류/전기장 없음 · MLIP 에 전자 없음)
   │
   ├─ 관측 A : 계면상이 log 모양으로 감속하며 계속 자란다 ............ [Fig. 2]
   │           ↳ 약한 고리: Li 대조군도 ≈8 % 더 자란다 / 창 1 decade / 적합 0
   │
   ├─ 표지 (1) : 비정질 대리조성 Onsager 에서 L_PP 지배 ............ [Fig. 4c]
   │           ↳ 약한 고리: 운동량보존 위반(Na만) · 지수 100배 · self/distinct 미분리
   │                        · 900/1200 K 에서 L_PP 항은 P 를 전해질 쪽으로 민다
   │
   ├─ 표지 (2) : Na₂S 비정질 (τ 0.28) .................................. [Fig. 3, S12]
   │           ↳ 약한 고리: 0 K 결정 기준 · 한 시점 · Li₂S τ 없음 · Na–S 가 MLIP 최약 화학
   │                        · 자기 그림(3a, 6)에 결정 Na₂S 있음
   │
   ├─ 표지 (3) : Na–P 결합그래프 관통 (0.23 ns~) ....................... [Fig. 5, S13, S14]
   │           ↳ 약한 고리: 고정 평면 두 장 사이 · Na 다리만으로 성립(P–P 무관)
   │                        · Li 계 대조 분석 없음 · 가는 목 몇 가닥
   │
   └─ 전자 쪽 : 표 1 문헌 결정상 갭 + Na₃P 전도도 + EIS 선형 R(t) 해석 ..... [Table 1]
               ↳ 약한 고리: 계산 0 · 갭 출처 혼재 · Li₃P 1991 값이 PBE 와 3배 차
   ⇒ "MCI 와 부합 / SEI 와 불부합" (필요조건, 충분조건 아님 — 저자 명시)
```

**이 그림에서 우리가 가져갈 한 줄**: *"MLIP-MD 가 보여줄 수 있는 것은 **원자 수송이 멈추느냐** 까지이고, 그 정지조차 열욕·셀·시간창과 분리해야 한다. **전자가 막혀서 멈추느냐** 는 MLIP-MD 의 질문이 아니다."*

---

## 9. ★★★ 임무 ① — 자기제한을 동역학으로 보였나 · 우리 노트 §8-4 판정

### 9-1. 우리 노트가 지금 말하는 것 (축자)
`kb/concepts/cv_vs_dqdv_and_two_windows.md` §8-4: *"⚠ **분야 전체의 공백이기도 하다** — 2026-09-22 기준, 자기제한을 **동역학으로 증명한** 문헌을 우리 litdb 안에서 못 찾았다 (`Chaney 2024` 는 `self-limiting` 이라는 말이 0회이고, 그 계산의 6런이 전부 100 % 환원으로 끝난다)."* 그리고 §8-2 의 자기제한 기전은 **전자 차단**이다(*"생긴 층이 **전자를 안 통하면** 반응이 그 자리에서 멈춘다"*).

### 9-2. 이 논문이 Li₇P₃S₁₁‖Li 자기제한을 **직접 보였나, 전제했나** — 갈라서
| 질문 | 답 | 근거 |
|---|---|---|
| 이 논문이 Li₇P₃S₁₁‖Li 를 **시뮬레이션했나** | ❌ **아니다** | 포텐셜 원소 Na·P·S 뿐 (`input.yaml` L15) · 저장소 전체 `Li7P3S11` 검색 **0건** · `md/README.md` 는 Na 생산 런만 · SI `Table S5` 가 Li 계를 **"Li et al. [5]"** 의 별도 프로토콜로 명시 (PBEsol 라벨·6.0 Å·Langevin·E RMSE 119.5 meV/atom) |
| Li 쪽 "멈춤" 은 어디서 왔나 | **인용 + 재수록** | 서론 *"has been shown to form a passivating SEI [9]"*(Wenzel 2016 *SSI* — ⚠ 원전 판정을 우리는 확인 안 했다. 제목은 *"…degradation of charge transfer kinetics…"*) · §3.2 *"plateaus after initial growth, consistent with self-passivating SEI behavior [19]"* · `Fig. 2` 청록 점선(범례 `*` 미설명, 가공 방식 코드에 없음) |
| Na 쪽에서 반응전선이 **멈추는** 걸 보였나 | ❌ — **안 멈춘다가 이 논문의 주장** | `Fig. 2`, §3.2 |
| 문장 강도 | 초록은 *"the **passivating** Li₇P₃S₁₁/Li interface"* 로 **단정**, 본문은 *"consistent with"* 로 **완화** | 초록 vs §3.2 |

⇒ **이 논문은 Li₇P₃S₁₁‖Li 의 자기제한을 보이지 않았다. 전제했다** — 실험 문헌 [9] 와 자기 그룹의 선행 MLIP-MD [19] 를 인용하고, 그 경계선을 겹쳐 그렸을 뿐이다.

### 9-3. SEI 와 MCI 를 가르는 **조작적 기준**은 무엇인가 — 코드까지 확인
| 층위 | 기준 | 정량? |
|---|---|---|
| 개념 (서론, ref 3) | SEI = 이온 O·전자 X → 자기제한 / MCI = 둘 다 O → 계속 성장 | 정의 |
| 성장 곡선 | Na "slows but does not cease" vs Li "plateaus" | ❌ **문턱·적합·지수 0.** 코드엔 유한차분 성장률뿐. §3d: 실제 차이는 **decade 당 ≈0.74 vs ≈0.22 nm(금속 쪽)** — 창은 1 decade |
| 세 표지 | L_PP 지배 · 비정질 황화물 · M–P 관통 | 각 지표의 수치는 있으나 **SEI/MCI 를 가르는 문턱값은 없다**. 저자 스스로 "필요조건" |
| 실험 | EIS 선형 R(t) (ref 6) | 문헌 해석 |
| **"멈췄다" 의 판정** | 🔴 **정의되지 않았다** | 어떤 양이 얼마 이하이면 멈춘 것인지 본문·SI·코드 어디에도 없다 |

⚠ **비교의 교란 요인 — SI `Table S5` 가 스스로 적은 것만**: 라벨 범함수(r²SCAN vs **PBEsol**) · 컷오프(7.0 vs 6.0 Å) · 학습셋(20,114 vs 11,596) · 오차(37–40 vs **120 meV/atom**) · **열욕(Nosé–Hoover vs Langevin)** · Onsager 대리조성(용융급랭 200–1000 원자 vs MPMorph ≈100 원자) · 연결성(있음 vs **없음**). SI 는 *"These consistencies ensure that the qualitative contrasts … reflect genuine chemical and physical differences rather than differences in simulation protocol"* 이라고 결론짓지만 **자기 표에 차이가 7 개**다. 특히 **Langevin 마찰은 확산을 늦추는 방향**으로 작용할 수 있어(우리 `marcolongo…` digest §7-4c 와 같은 종류의 우려) **"Li 는 멈춘다" 를 부풀리는 쪽의 교란일 수 있다** — Li 쪽 마찰계수가 공개되지 않아 크기는 모른다.

### 9-4. 우리 litdb 전체에서 "자기제한을 동역학으로" — 이 논문이 들어온 뒤의 지형
| digest | 계 · 방법 | 무엇을 주장하나 | 우리 판정 (각 digest) |
|---|---|---|---|
| `chaney2024_two_step…` | LPSC‖Li · MTP · 31,824 원자 · 10 ns | `self-limiting` **0회**, "음의 되먹임" | 대형 6런 **전부 100 % 환원** · 멈춘 유일 런(소형·1 kbar·시드 1)은 논문 미언급 · 슬랩 5 nm 라 "막힘 vs 고갈" 분리 불가 |
| `kim2026_li_argyrodite_sei_reactive_md` (⛔ 프리프린트) | LPSC‖Li · MTP · ~7,000 원자 · 20 ns | **"self-passivating"** — PS₄ 20 → **6 층 평탄 (~11 ns)** | **구조적 격리이지 전자 차단 아님** · 고갈(20 층 중 14 층 소모) 배제 못 함 · 시드 1 · 대형모델 본문 내부모순("continued decomposition") |
| `lomeli2024_predicting_reactivity_passivation…` | 여러 SSE‖Li · AIMD · 550 K · 40 ps | "passivating" 라벨 = **반응 공간 국소성**(눈 판정) | 전자적 판정 **시도·실패**(액체 Li 로 E_F 유한 DOS) |
| **이 편** `li2026_mci_vs_sei…` | **Na₃PS₄‖Na** · ACE · 50만 원자 · 10.5 ns | Na = **안 멈춤**(MCI 부합) · Li₇P₃S₁₁ = 멈춤을 **ref 19 에서 전제** | Li 점선도 **≈0.3 nm(≈8 %) 더 자람**(figure-read) · 교란 7개 · 전자 계산 0 |
| (litdb 밖) Li2025JPCC ref 19 | Li₇P₃S₁₁‖Li · ACE(PBEsol, 120 meV/atom) · 50만 원자 · 10 ns · Langevin | "plateaus" | **우리가 원문을 안 봤다** — 확보 후보 1순위(§22) |

⚠ **§8-4 를 쓸 때(2026-09-22) 이미 `kim2026` 과 `lomeli2024` 가 litdb 에 있었다** — 노트는 `chaney2024` 하나만 들었다. **이 누락은 이 논문과 무관한 노트 자체의 결함**이다.

### 9-5. 🔴🔴 한 줄 결론
> **부분적으로 고쳐야 한다.** *"자기제한을 동역학으로 **증명**한 문헌이 없다"* 는 **여전히 맞다** — 이 논문은 Li₇P₃S₁₁‖Li 를 **돌리지 않았고**(ref 19 의 평탄을 가져와 겹쳤을 뿐), 그 겹친 점선조차 1→10 ns 에 ≈8 % 더 자라며, "멈춤" 의 조작적 정의가 없다. 그러나 **"분야 전체의 공백" 과 "`chaney2024` 하나가 근거" 는 틀렸다** — 원자 수송이 멈춘다고 **주장한** MD 가 litdb 안(`kim2026`)과 밖(Li2025JPCC)에 이미 있고, 노트가 그걸 빠뜨렸다. 빠진 것을 정확히 말하면 **"전자 차단에 의한 정지(§8-2 의 기전)의 동역학 증거"** 이고, 이것은 **MLIP-MD 로는 원리상 못 보인다**(전자가 없다 — 이 논문이 스스로 *"not charge-aware"* 라 적는다). ⇒ **stepwise CV 가 필요하다는 §8-4 의 결론은 오히려 강화된다.**

(구체 정정 문구는 `litdb/_pending_index_li2026_mci_vs_sei_na3ps4_na_mlip_md.md` ⑥.)

---

## 10. ★★ 임무 ② — 세 판별 특징: 원인인가 신호인가

**먼저 논문 스스로의 말**: *"markers"* · *"consistent with"* · *"necessary but not sufficient"* · *"definitive classification will require direct measurement or calculation of electronic conductivity."* — **저자도 인과를 주장하지 않는다.** 아래는 **신호로서도 튼튼한가**까지 본다.

### 10-1. (1) P–P 수송 상관 — ⛔ 원인 아님 · 🔴 신호로서도 흔들린다
- **어디서 쟀나**: 계면이 아니라 **균질 비정질 대리조성**(200–1000 원자) · **900/1200 K**(계면 MD 는 300 K) · 대리조성↔계면 영역 대응은 조성 유사성(SI S3.2)이고 가장 큰 플럭스를 낸 NaP₁₅·NaP₅ 는 계면에서 **띠로 관측되지 않는** 과도 조성이다.
- **인과 검정**: 없음(P 이동을 막고 성장이 멈추는지 같은 대조 잡 0).
- **신호로서의 문제 (§3f 검산)**: ① Na 행렬이 **운동량보존 질량비를 11.8·1.7배 위반** — 같은 논문이 가져온 Li 행렬은 만족 ② **질량 플럭스 합 ≠ 0**(NaP₁₅·NaP₅) ③ **Δμ_P > 0(900/1200 K)이라 L_PP 항은 P 를 전해질 쪽으로 민다** — 음극향 P 플럭스는 교차항 몫 ④ **L_PP 를 self/distinct 로 안 나눴다**(코드는 나눌 수 있었다) ⑤ **"약 한 자릿수" 는 지수 무시 비교**(실제 ≈700배 또는 표기 오류).
- **판정**: **원인으로 입증 안 됨. 동반 신호로서도 기준틀·부호 문제가 풀리기 전엔 인용 불가.**

### 10-2. (2) 비정질 Na₂S — ⛔ 원인 아님 · ⚠ 신호는 서지만 크기는 과장, MLIP 인공물 가능성 열림
- **관측 자체**는 선다: 꼬리비 0.27 vs ≈0.81 은 열변위에 둔감한 지표로도 ≈3배(§3e).
- **"∼5배"** 는 0 K 결정 기준 탓에 부풀려졌다(✎ u 0.15–0.20 Å 면 ≈2.4–3.1배).
- **인과**: "결정 Li₂S 가 확산을 막아 P 를 가둔다" 는 **Li 쪽에서 가져온 주장**이고, Na 쪽에서 결정화를 강제·억제하는 대조 실험이 없다.
- **인공물 가능성 — 논문도 대안으로 적는다**: Na–S 이원이 **MLIP 에너지 오차 최대**(RMSE 58.5, 반응 층 99.3 meV/atom) · **Na–S 4–7 Å 인력 과소평가**(`Fig. S4`) · Na₂S 반형석 둘째 껍질 5.4 Å 가 바로 그 거리대 ⇒ ✎ **포텐셜이 Na₂S 장거리 질서 구동력을 과소평가했을 가능성**(가설 — 검정 안 됨).
- **판정**: **신호(정도 차이)** 이고, 원인도 아니며, **포텐셜 한계와 분리되지 않았다.**

### 10-3. (3) Na–P 연결경로 — ⛔ 원인 아님(시뮬레이션 안에서는 원리상 불가) · ⚠ 신호의 정의가 느슨
- **시뮬레이션 안에서 원인일 수 없다**: MLIP 에 전자가 없으므로 그 망이 전자를 날라 성장을 일으킬 수 **없다**. 이 표지는 **실제 전지에서라면** 전자 경로일 수 있다는 **해석**이다.
- **정의의 느슨함 (코드)**: 고정 평면 두 장(≈34 Å 간격) 사이를 **원자 하나씩만** 걸치면 관통 · **P–P 결합은 전혀 기여 안 함 — Na 다리만으로 성립**(`Fig. S13`) · 스윕 상단 ≳3.5 Å 는 반응 안 한 전해질의 Na–P 도 간선이 되는 구간이라 거기서의 평탄은 견고성 증거가 못 된다 · 실제 경로는 Na₂S 층을 건너는 **가는 목 몇 가닥**(`Fig. 5b,c`).
- **대조군 없음**: Li₇P₃S₁₁‖Li 에 같은 분석을 **안 했다**(`Table S5` *"Not performed"*). ⇒ **"Li 와 Na 를 가르는 특징" 이라는 초록의 주장에 대조 데이터가 없다.**
- **판정**: **동반 구조 신호**이고, 판별력(Li 에서는 안 나온다는 것)은 **검증되지 않았다.**

### 10-4. 종합
**셋 다 인과로 세워지지 않았다 — 저자도 인과를 주장하지 않는다.** 인과 추론의 틀은 **n = 2 계 비교**(Na vs Li)인데 두 계는 **화학(양이온·SE·구동력) + 프로토콜 7 항목**이 동시에 다르다. "재현성" 주장(여러 시드·5,000–500,000 원자·여러 방위)은 **개수·결과가 제시되지 않았고**, 재현성은 인과가 아니라 견고성이다.

---

## 11. ★★ 임무 ③ — `chaney2024` 와 정면 대조: 결정성이 판별자인가

### 11-1. 이 논문이 **명시적으로** 말하는 것
- ✅ **명시**: 결론 *"We propose that the continuous P transport, **amorphous sulfide matrix**, and persistent topological connectivity pathways are chemical and morphological **markers inconsistent with the self-limiting behavior** characteristic of a passivating SEI."* — **비정질 황화물 = SEI 와 불부합 표지 셋 중 하나.**
- ✅ **명시(기전)**: §3.3 *"Combined with **crystalline Li₂S domains that physically block diffusion pathways**, this anti-correlation traps P within the interphase."*
- ❌ **말하지 않는 것**: 결정성이 **유일한/결정적** 판별자라는 말 · **결정화의 시간(언제 결정화하나)** 이 판별을 좌우한다는 말 · `chaney2024`·Golov & Carrasco 인용(**참고문헌 53개에 0건**).

### 11-2. 두 논문을 합쳐야 나오는 것 — **✎ 우리 유도 (어느 논문도 말하지 않는다)**
> *"아르지로다이트‖Li SEI 는 **먼저 비정질로 생기고 뒤늦게 결정화**한다(`chaney2024`). 이 논문의 틀에서 비정질 황화물이 비-SEI 표지라면, **결정화 전의 초기 수백 ps–ns 동안 아르지로다이트 SEI 는 MCI-유사 창을 지난다** — 결정화 *시점*이 자기제한 여부를 가른다."*
- 이 문장은 **두 논문을 이어 붙인 우리 가설**이다. 인용할 때 반드시 ✎ 표기.

### 11-3. 그 가설을 litdb 안 데이터가 받쳐 주나 — 🔴 **엇갈린다**
| 계 | 결정화 | 반응 정지 | 가설과 |
|---|---|---|---|
| Li₇P₃S₁₁‖Li (ref 19, 이 편 재수록) | ✅ 나노결정 7개(`Fig. 3b`) | "평탄"(우리 판독 ≈8 % 더 자람) | 부합 |
| LPSC‖Li `kim2026` (프리프린트) | ✅ ~11 ns 결정 핵생성 | ✅ PS₄ 평탄 동시 | 부합(동시성, 인과 아님 · 고갈 배제 못 함) |
| LPSC‖Li `chaney2024` model II | ✅ **결정화도 ≈70–81 %** | ❌ **6런 전부 100 % 환원** | 🔴 **반례**(단, 5 nm 슬랩이라 고갈로도 설명) |
| Na₃PS₄‖Na (이 편) | ⚠ 대부분 비정질(결정 1개) | ❌ 계속 성장 | 부합 |

⇒ **"결정화 ⇒ 정지" 는 MLIP-MD 문헌 안에서도 일관되지 않는다.** 가장 큰 계(`chaney2024` model II)가 결정화하고도 끝까지 환원됐다.

### 11-4. "결정성" 이 **같은 양인가** — 아니다
| | `chaney2024` | 이 편 |
|---|---|---|
| 무엇을 재나 | **원자 단위 결정/비정질 분류 → 결정 %** | **슬랩 평균 Na–S 부분 RDF 의 τ** |
| 알고리즘 | ref 34 방법 — **그 편에 0줄** | `crystallinity.py` 공개 (§3e) |
| 시간 | **시간 곡선**(ps–10 ns) | **최종 5 프레임 한 점** |
| 기준 | (없음 — 분류 비율) | **0 K 정적 결정** |
| 대조계 | 없음 | Li₂S 는 **그림만**(τ 없음) |
| 공간 | 부피 전체 | 고정 z 창 30 Å, **P 제외** |

⇒ **두 수를 나란히 놓으면 안 된다.** "Chaney 의 결정화도 70 % 와 이 편의 τ 0.28 을 비교" 같은 문장 **금지**.

---

## 12. 🔴 임무 ④ — "혼합전도" 의 전자 쪽을 무엇으로 판정했나

### 12-1. 전수
| 전자 쪽 근거 | 이 논문이 한 것 | 계산? |
|---|---|---|
| 계면상의 밴드갭·DOS | **없음** | ❌ |
| 전자전도도·폴라론 호핑 | **없음** — *"computationally prohibitive"* | ❌ |
| 전하·전기장·전기화학퍼텐셜 | **없음** — *"not charge-aware"* | ❌ |
| **위상적 연결** | Na–P 결합그래프 관통 (§3g) — *"proxy"* 로 명시 | ✅ 구조만 |
| **산물 갭** | `Table 1` — **전부 문헌 인용, 결정상** | ❌ (인용) |
| **산물 전도도** | 결정 Na₃P "12 S cm/1" vs Na₂S 10⁻¹⁶–10⁻¹² (ref 46) | ❌ (인용) |
| **실험** | Wenzel 2016 EIS 선형 R(t) 해석 | ❌ (인용) |

⇒ **"M" 은 한 번도 계산되지 않았다.** 이온 쪽(사실은 **중성 원자** 수송 — 아래)만 MD 로 보고, 전자 쪽은 **위상 + 결정상 문헌값**으로 "그럴 수 있다" 를 세운다. 저자 스스로 *"amorphous bandgaps can differ significantly from their crystalline counterparts"* 라 쓴다.

### 12-2. 🔑 MLIP-MD 의 "계속 성장" 자체가 전자 전도의 증거가 **될 수 없는** 이유 (✎ 우리 논증 — 논문이 말하지 않는다)
MLIP 에는 이온과 전자의 구분이 없다. 금속에서 전해질로 들어가는 Na 는 **중성 원자로 움직이며 환원력을 같이 들고 간다** — 즉 MLIP-MD 의 반응 전선은 **"Na⁺ + e⁻ 가 묶여서 이동"** 하는 가정 위에서 전진한다. 실제 전지에서 **전자를 막는 SEI** 라면 Na⁺ 만 지나가고 전자는 남아 반응이 멈출 것이지만, **MLIP 는 그 상황을 표현할 수 없다.** 그러므로
- **MLIP-MD 에서 성장이 계속된다** ≠ 전자가 통한다 (원자가 움직일 수 있다는 뜻일 뿐)
- **MLIP-MD 에서 성장이 멈춘다** = 원자 수송이 막혔다 (실제 전지라면 **이온 저항층** 쪽에 가깝다 — 이상적 SEI 가 아니다)
⚠ **예외적 뉘앙스**: 넓은 갭 절연체 안의 과잉 Na(=전도대 전자)는 DFT 라벨에서 에너지가 높게 찍히므로, **국소 에너지론으로는** 전자구조가 일부 반영된다. 그러나 **수 nm 를 건너는 전자 수송·페르미 준위 정렬·전기장은 7 Å 컷오프 포텐셜에 없다.**

### 12-3. `Table 1` 의 Na↔Li 전자 대비가 **방법 일관적이지 않다**
- Na–P: NaP ∼0.74 · Na₃P ∼0.4/0.8 → "semiconducting"
- Li–P: Li₃P **3.6(직접)/2.03(간접)** — **1991** ab initio → "wide-gap semiconductor"
- 우리 PBE fixed-occ nscf: **Li₃P 0.7092 eV** (`sei_electronic.json`) · MP **0.70**(`sei_products.json`, `exp_anchor` 필드 "~0.7" — 출처는 우리도 미확인)
⇒ **PBE 계열로 맞춰 놓으면 Li₃P 는 Na₃P 와 같은 "반도체" 칸**이다. 논문의 *"Li 쪽 산물은 전부 넓은 갭 → SEI"* 는 **방법이 섞인 표 위에 서 있다.** 이 논문 자신의 논리(반도체 M–P 상 + 연결 → MCI 가능)를 방법 일관 갭으로 돌리면 **Li₇P₃S₁₁‖Li 도 같은 의심을 받는다** — 그리고 그 계의 연결성 분석은 **없다**.

### 12-4. 결론
**방법적 급소가 맞다.** 논문은 급소를 숨기지 않는다(명시적 단서가 많다). 문제는 **초록과 결론 문장이 그 단서보다 강하다**는 것이다: 초록 *"These characteristics are consistent with mixed ionic-electronic conducting behavior"* — "electronic" 에 해당하는 계산이 0 이다.

---

## 13. 임무 ⑤ — 우리 Li₆PS₅Cl‖Li 로 옮겨지나

⛔ **값 이식 금지.** 방법·판정만.

### 13-1. ⛔ 못 옮기는 것
| 무엇 | 이유 |
|---|---|
| **포텐셜 자체** | 원소 **Na·P·S 뿐** — Li·Cl 이 없어 Li₆PS₅Cl 을 **물리적으로 돌릴 수 없다** |
| 모든 수치 (L_ij·플럭스·τ·두께·관통 시각) | Na 계 · r²SCAN 라벨 · 1 계 1 조건 |
| "Na 가 크니 P–P 상관이 강하다" 기전 | Na 전용 가설이고 검정 안 됨(§10-1) |
| Na 산물의 전자 성격 | NaP·Na₃P ≠ Li₃P 계열 |
| "MCI 다" 라는 결론 | Na₃PS₄‖Na 에서도 필요조건까지뿐 |

### 13-2. ✅ 옮길 수 있는 것 (분석 설계) — **고쳐서**
| 도구 | 이 논문 구현 | 우리가 쓴다면 고칠 것 |
|---|---|---|
| **(t,z) 배위수 히트맵** (`Fig. 2`) | 중심원자–이웃종 4 쌍 | 그대로 쓸 만하다. **Li–Cl · Cl–Li** 쌍 추가, 컷오프 명시 |
| **조성 프로파일 경계** | 금속 쪽 = "P/S 하나라도 있는 첫 bin" | **문턱 0 은 떠돌이 원자 하나에 흔들린다** → 분율 문턱 + 다중 bin 평균(코드에 이미 있음) |
| **결합그래프 관통** | 고정 평면 · 원자 1개 기준 · Na 다리 | **시간에 따라 움직이는 검출 경계 사이**로 정의 · 전해질 자체가 연결되는 컷오프 상단 표시 · **"안 멈추는" 대조계와 "멈추는" 대조계 둘 다**에 같은 분석 |
| **τ 결정성 지표** | 0 K 결정 기준 · 한 시점 · z 주기 슬랩 | **같은 포텐셜·같은 온도의 결정 MD 를 기준**으로 · 시간 곡선 · 슬랩은 z 비주기 처리 |
| **Onsager Lᵢⱼ** | 기준틀 미기재 · self/distinct 미분리 | **기준틀 선언**(우리 `--haven` 은 비-Li 골격 개수평균 기준 — `marcolongo…` digest §7-4a) · **Σᵢ mᵢ Lᵢⱼ = 0 검사를 게이트로** · self/distinct 동시 보고 · **MD 온도에서의 플럭스** |
| 능동학습 γ 감시 | 문턱만 보고 | **생산 궤적 γ 분포를 결과로 보고** — 단 γ 는 ACE/MTP 전용 개념이고 **UMA 에는 정의가 없다**(`kim2026` digest §15.4 와 같은 판정) |

### 13-3. 이 논문의 틀이 우리 LPSCl‖Li 에 대해 **말해 주는 것** (판정 아님 — 질문으로)
- **표지 (2)** 결정화: Li 계 MLIP-MD 3편(ref 19 · `kim2026` · `chaney2024`) 모두 **Li₂S(계) 결정화**를 본다 → 이 틀로는 **SEI-유사 쪽**. 그러나 `chaney2024` model II 는 결정화하고도 끝까지 환원됐다(§11-3).
- **표지 (3)** M–P 연결: 우리 0 V 산물에 **Li₃P(PBE 0.7092 eV)** 가 있다 → 이 틀에서는 **"반도체 M–P 상" 후보**. 관통 여부는 **아무도 계산 안 했다.**
  - ✎ **우리 유도 (가정: `chaney2024` 의 반형석 고용체 그림 + P 무작위 배치 + 공유 Li 를 통한 최근접 음이온끼리만 간선)**: Li₆PS₅Cl + 8Li → Li₁₄PS₅Cl = 음이온 자리 7 개 중 **P 1 개(p = 1/7 ≈ 0.143)**. 반형석의 음이온 부격자는 fcc 이고 **fcc 자리 퍼콜레이션 문턱 ≈0.198** 이므로 **무작위 고용체라면 이 논문식 M–P 망은 무한계에서 관통하지 않는다.** ⚠ **P 가 뭉치면(상분리 Li₃P) 결론이 뒤집히고**, 수 nm 얇은 층에서는 유한크기 효과로 문턱 아래에서도 관통할 수 있다. LPSCl1.6(`Li₅.₄PS₄.₄Cl₁.₆`)도 P 1 / 음이온 7 로 같은 0.143, b2o3 조성은 P 8 / 음이온 68 ≈ 0.118 로 더 낮다.
- **표지 (1)** P–P 상관: Li 쪽 결과(ref 19)는 **운동량보존 역류와 수치상 같아서**(§3f) 우리 계에 줄 정보가 없다.

⇒ **이 논문은 우리 LPSCl‖Li 가 SEI 인지 MCI 인지 답해 주지 않는다.** 줄 수 있는 것은 **"MLIP-MD 로 무엇을 재면 필요조건이라도 세울 수 있나" 의 체크리스트**와, 그 체크리스트를 **어떻게 구현하면 틀리는지의 목록**(§17)이다.

---

## 14. 우리 DFT / MLIP-MD / `db/properties` 대비 ★★ (`../our_dft_baseline.md`)

### 14-1. MD·MLIP 규약 — **판정하지 않고 나란히만** (임무 ⑥)
| 항목 | **이 편 (Na₃PS₄‖Na)** | Li2025JPCC (ref 19, 이 편 SI) | `[Chaney24SEI]` | **우리 (modelc/lpsocl)** |
|---|---|---|---|---|
| MLIP | **ACE 자체학습**, 350/원소, **7.0 Å** | ACE 자체학습, 350/원소, 6.0 Å | MTP 자체학습, level 8, 5.0 Å | **UMA-s-1p1 (omat) 범용 사전학습**, 미세조정 없음 |
| **라벨 범함수** | **r²SCAN** (정적) · AIMD 는 PBEsol | **PBEsol** | 미기재 | **omat = PBE(+U) 계열** |
| 원소 | Na·P·S | Li·P·S | Li·P·S·Cl | 범용 |
| 에너지 RMSE | 36–40 meV/atom | 119.5 | 18–21 | 외부 벤치마크 |
| 외삽 감시 | γ (1.5 / 5) — 통계 0 | γ 1–2.5 | D-optimality (학습 시) | ❌ (UMA 에 γ 정의 없음) |
| 앙상블 | **NpT** 1 bar | NpT | NPT | **NVT** |
| 열욕 | **Nosé–Hoover** τ 1 ps | **Langevin** | Nosé–Hoover | **Langevin**, friction 0.02 |
| dt | 1 fs | 1 fs | 1 fs (일부 0.5) | **2 fs** |
| 온도 | **300 K** (Onsager 500–1500 K) | 300 K | 300/350/400 K | **600/800/1000 K** (400/500 K 제외 판정) |
| 길이 | **10.5 ns** | 10 ns | 10 ns | equil **5 ps** + prod **200 ps** |
| 크기 | **≈500,000** | 500,000 | 7,956 / 31,824 | box331 **558** |
| 계면 | ✅ 1 계면(방위 미기재) | ✅ (100)/(100) | ✅ 샌드위치 2면 | ❌ 벌크 주기셀 |
| 반응 | ✅ | ✅ | ✅ | ❌ 조성 고정 |
| 시드 | "여러" (개수·결과 미제시) | ? | 2 | **멀티시드 규율** |
| 보고량 | 배위수 지도 · Lᵢⱼ · 관통 · τ | 배위수 · Lᵢⱼ | α(t) · 결정성(t) | **MSD(창 2–50 ps) → D → σ (NE, Haven=1)** |
| 확산 추출 | Onsager: MSD 선형영역(창 미기재) | 같음 | — | **MSD 창 2–50 ps 고정** |

🔴 **겹치는 것이 거의 없다** — 온도(300 vs 600–1000 K) · 라벨 범함수(r²SCAN vs PBE 계열) · 계면 유무 · 반응 유무. **어떤 동역학 수치도 나란히 놓지 않는다.**

### 14-2. 값 대조 — 무엇을 옮겨도 되나
| 양 | 이 논문 | 우리 | 옮기나 |
|---|---|---|---|
| Li₃P 밴드갭 | **2.03 (간접)/3.6 (직접)** — 1991 인용 | **0.7092** (QE PBE fixed-occ nscf, `sei_electronic.json`) | ⛔ **나란히 금지**(방법 상이). 🔴 **그 1991 값을 근거로 우리 Li₃P 를 비누설로 재분류하지 않는다** |
| Li₂S 밴드갭 | 3.24–5.08 인용 | 3.4379 (PBE, 순위로만) | ⛔ |
| SEI/MCI 분류 문턱 | **없음** | `sei_products.json` 역할 문턱(≥4 / 2–4 / <2 eV) | 🟡 우리 문턱도 **갭 필요조건만** 다룬다 — 이 논문이 말하는 연결성·형태 축이 우리에게 **없다** |
| 반응식 방향 | Na₃PS₄ + **6Na**(원자당 최저) | 우리 0 V 식 **BLOCKED** | ✅ **규약 교훈만**: 원자당 최저 ≠ 금속 과잉 종착 (§3c) |
| Onsager 규약 | 기준틀 미기재 | `--haven`: 비-Li 골격 개수평균 기준 | ✅ **반면교사** — 우리가 교차항을 쓴다면 기준틀 선언 + 질량보존 검사 |

### 14-3. ⭐ 우리 규율을 **지지**하는 지점
1. **"보고량을 먼저 정의한다"** — 이 논문의 핵심 약점 셋(멈춤의 정의 없음 · 관통의 정의가 고정평면 · 결정성 기준이 0 K)은 전부 **보고량 카드 §1–3 에서 걸렸을** 문제다(`kb/templates/estimand_card.md`).
2. **"검증 게이트를 결과 전에"** — Onsager 행렬에 **Σ mᵢ Lᵢⱼ = 0** 같은 값싼 물리 게이트만 걸었어도 Na 행렬 문제는 결과 전에 잡혔다.
3. **"MLIP 학습창 밖을 조심한다"** — 5000 K 용융 단계(학습 최고 1500 K)에 γ 를 걸었는지 미기재. `[Wang22Res]` 의 300 K 외삽 1709× 발산 사례와 같은 종류의 위험이 **보고되지 않은 채** 남는다. 반대로 **생산 MD 에 γ 감시를 걸었다는 점**은 `[Wang22Res]` 보다 앞선다(통계가 없는 것이 아쉽다).

---

## 15. 적용 인사이트 — 우리 연구에 어떻게

1. 🔴 **당장(문서)**: `kb/concepts/cv_vs_dqdv_and_two_windows.md` §8-4 를 **두 층(원자 수송 정지 / 전자 차단 정지)** 으로 쪼개 고친다 — 제안 문구는 pending ⑥.
2. ⭐ **우리 음극 판정축이 빠뜨린 차원이 선명해졌다**: 우리는 **"어떤 상이 생기나 + 그 상의 갭"** 까지다. 이 논문이 쓰는 **연결성(topology)** 과 **형태(결정/비정질)** 는 우리 자산에 0 이다. ⇒ 음극 서사는 앞으로 **"갭은 필요조건, 연결성·형태는 미계산"** 을 같이 적는다.
3. 🔧 **나중에 계면 MD 를 연다면 이 논문의 코드는 "설계도 + 함정 목록"** 이다 — 특히 **Σ mᵢ Lᵢⱼ = 0 게이트**, **시간 의존 경계 사이 관통**, **동온도 결정 MD 기준 τ** 셋은 첫날부터 넣는다.
4. 🟡 ✎ **값싼 계산 하나가 열린다**: `chaney2024` 고용체 그림이 맞다면 우리 조성의 P 음이온 분율(≈0.14)은 fcc 자리 퍼콜레이션 문턱(≈0.20) **아래**다. **SQS 반형석 고용체에서 Li-다리 P 망의 관통확률**을 두께별로 세면 이 논문의 표지 (3) 를 우리 계에 대해 **정적으로** 답할 수 있다. ⚠ **보고량 카드 먼저**(배열 앙상블 집계 규칙 · 컷오프 · 두께 정의).
5. 🔵 **Onsager 교차항은 기준틀의 산물일 수 있다** — 우리 Haven 원장(`Haven=1` · `[Marc17NE]`)과 같은 뿌리다. **골격이 흐르는 계에서 "상관" 을 해석하지 않는다**는 우리 b2o3 1200 K 제외 판정의 **또 하나의 외부 사례**.

---

## 16. 인용 가능 문장 (deck / paper 용)

- *"대규모 MLIP-MD(≈50만 원자·10.5 ns)는 Na₃PS₄‖Na 계면상이 log 모양으로 감속하면서도 멈추지 않는다고 보고하고, 이를 혼합전도 계면상(MCI)과 **부합**하는 거동으로 해석한다 — 저자들은 전자전도의 직접 계산 없이는 확정할 수 없다고 명시한다 [Li26MCI]."*
- *"MLIP 는 전하를 다루지 않으므로 MLIP-MD 가 보일 수 있는 것은 **원자 수송의 정지 여부**까지이며, 전자 차단에 의한 자기제한은 별도의 전자구조·수송 계산이나 실험이 필요하다 [Li26MCI] (저자 명시: 'not charge-aware … necessary but not sufficient')."*
- *"MLIP-MD 에서 계면상 분류에 쓰인 표지 — 비정질 황화물, 금속–P 결합망의 관통, P 의 협동 수송 — 는 **필요조건**으로 제안됐다 [Li26MCI]."*

⛔ **쓰지 않는다**:
- *"Na₃PS₄‖Na 가 MCI 임이 밝혀졌다"* (저자도 안 쓴다)
- *"Li₇P₃S₁₁‖Li 가 자기제한 SEI 임을 이 논문이 보였다"* (**다른 논문의 결과**이고 우리 판독상 점선도 자란다)
- *"Na 계의 P–P Onsager 계수가 Li 계보다 한 자릿수 크다"* (지수 100배 불일치 · 운동량보존 위반)
- *"P–P 상관이 P 를 음극으로 보낸다"* (자기 Δμ 부호와 불일치)
- *"계면상 Na₂S 의 장거리 질서가 5배 억제"* (0 K 기준 과장 — 쓰려면 "꼬리비 ≈3배, 0 K 결정 대비" 로)
- *"Li₃P 는 넓은 갭 반도체(2.03 eV)"* 를 **우리 계 판정에** 쓰는 것

---

## 17. 주의 / 한계 — 비판 (over-claim 방지) ★★

**① 🔴🔴 Li 대조군이 이 논문의 결과가 아니다.** 초록의 "passivating Li₇P₃S₁₁/Li" 는 ref 9·19 인용이고, 비교는 **다른 포텐셜(PBEsol, 120 meV/atom) · 다른 열욕(Langevin) · 다른 Onsager 프로토콜**로 만든 결과와의 대조다. SI `Table S5` 가 차이 7개를 적어 놓고 *"protocol differences 가 아니다"* 라고 결론짓는다.

**② 🔴🔴 "멈춤" 의 조작적 정의가 없다.** 적합 0, 문턱 0. 우리 픽셀 판독상 Li 점선도 1→10.4 ns 에 **≈8 %** 자란다. 차이는 **감속률 3–4배**이고 창은 **1 decade** 다.

**③ 🔴🔴 Onsager 결과가 물리 제약과 맞지 않는다 (§3f).** Na 행렬 운동량보존 위반(11.8·1.7배) · 질량 플럭스 합 ≠ 0 · 지수 100배 · Δμ_P 부호와 결론 방향 불일치 · self/distinct 미분리. **핵심 계산이 비공개(`py_oats`)** 라 원인 판정 불가 — **재현 불가능한 수가 논문의 첫째 표지다.**

**④ 🔴 Li 쪽 "P 를 가두는 P–S 반상관" 은 운동량보존 역류와 수치상 같다** (0.05 %). `[Marc17NE]` 가 경고한 **"골격 역류를 물리 상관으로 읽는"** 사례다.

**⑤ 🔴 관통 판정이 느슨하다 (§3g).** 고정 평면 · 원자 1개 기준 · P–P 무관 · 상단 자명 · **Li 대조 분석 없음.** `Fig. 5` 경계선이 실은 고정 문턱이고 y 축 단위가 틀렸다(Å→nm).

**⑥ 🔴 결정성 지표의 크기가 부풀려졌다 (§3e).** 0 K 결정 기준 · 한 시점 · z 주기 슬랩 · P 제외(조성 필터 미검사) · Li₂S τ 없음. 게다가 자기 그림(`Fig. 3a`·`Fig. 6`)이 결정 Na₂S 를 보여 준다.

**⑦ 🟡 실험 연결이 함수형에서 어긋난다.** MD = log(감속), 실험 EIS R(t) = 35 h **선형**. 둘 다 "MCI 부합" 으로 읽는 것은 **감속하는 MD 가 비감속 실험을 설명한다**는 추가 가정이 필요한데 다루지 않는다.

**⑧ 🟡 MLIP 정확도가 결론이 기대는 화학에서 가장 나쁘다.** Na–S 이원 RMSE 58.5(반응 99.3) meV/atom · Na–S 장거리 인력 과소 · Na–P 상 경쟁폭(22 meV/atom) < 오차(35) · 반응물 EOS 에너지 어긋남. **"80 meV Å⁻¹ 필터" 는 자기 표와 모순**(단위 오기 추정).

**⑨ 🟡 재현성 주장에 데이터가 없다.** "여러 시드 · 5,000–500,000 원자 · 여러 방위" 의 **개수·결과 0**. 생산 계면 **방위 미기재**. 에너지 표류·밀도 곡선 미제시. γ 통계 0.

**⑩ 🟡 표 1 의 출처 혼재** — 단층 Na₂S(ref 44) · 나노튜브 기상성장(ref 47) · 1991 Li₃P(ref 50) · ᵃ 표시 불일치 · 전도도 자릿수 산술(13–17 이 맞다) · "12 S cm/1" 조판.

**⑪ 🟡 원자당 반응에너지 규약**(§3c) — "바닥 반응 = NaP" 와 "−0.465 vs −0.78" 구동력 비교가 정규화에 의존한다. 금속 과잉 종착은 Na₃P 쪽.

**⑫ 🟡 작은 오기들** — `Na2PS4`(→Na₂PS₃) · 이온반경 값의 출처 불일치(✎, 원문 대조 권장) · `Fig. 4b` 음수 눈금 부호 누락 · `Fig. 6` 캡션↔도식 층 순서 · README 의 투고본 그림번호.

**⑬ 🟢 잘한 것도 적는다.** (a) **포텐셜·입력·활성집합·분석 코드 공개** — 이 digest 의 비판 대부분이 **코드가 공개됐기 때문에 가능**했다(`[Chaney24SEI]` 는 비공개) (b) 한계를 본문에 **먼저·여러 번** 적는다 (c) 결정성·관통을 **정량 지표로 만들려고 한** 첫 시도 (d) 컷오프 민감도 스윕을 **했다** (e) γ 감시를 생산 MD 에 **걸었다고 명시** (f) 50만 원자 규모로 **고갈(유한 셀) 문제를 사실상 피했다** — `chaney2024`·`kim2026` 의 약점을 이 설계는 갖지 않는다.

---

## 18. 🔴 임무 ⑦ — 우리에게 **불리한** 결론 (따로 적는다)

**(가) 🔴🔴 우리 노트 §8-4 가 틀린 부분이 있었다 — 이 논문과 무관하게.** 작성 시점에 litdb 에 이미 `kim2026`(자기부동태 **주장**)·`lomeli2024`(부동태 **라벨**)가 있었는데 `chaney2024` 하나만 들고 "분야 전체의 공백" 이라 썼다. 결론(stepwise CV 필요)은 살아남지만 **근거 서술이 부정확했다.**

**(나) 🔴 우리 음극 판정축은 이 논문이 "불충분" 이라 부르는 바로 그 축이다.** `sei_products.json`·`anode_interface_b2o3.json` 은 **산물 갭**으로 판정한다. 이 논문은 갭을 넘어 **연결성·형태**를 보려 했고, 그조차 필요조건이라 한다. ⇒ **"O 도핑의 음극 이점 = Li₂O/Li₃PO₄ 넓은 갭 차단" 서사(`sei_products.json` `anode_vs_cathode_summary`)는 연결성을 한 번도 보지 않은 서사**다. 소량의 넓은 갭 상이 **Li₃P 망을 끊는지**는 부피분율·배치의 문제이고 우리는 계산하지 않았다(b2o3 템플릿에서 Li₂O 3 몰 vs Li₃P 8 몰).

**(다) 🔴 이 논문의 틀을 방법 일관 갭으로 돌리면 우리 Li₃P 가 불리해진다.** 논문은 Li₃P 를 1991 값(2.03 eV)으로 "넓은 갭" 이라 안심시키지만, **우리 자신의 PBE 값(0.7092 eV)** 을 넣으면 Li₃P 는 Na₃P 와 같은 "반도체" 칸 — **이 틀에서의 MCI 후보**다. 우리 `ndo_passivation_argument_2026_09_14.json` 이 이미 *"⛔ 음극(0 V) 쪽 안정성 주장 — 둘 다 Li₃P(0.709 eV, conductor-LEAK)를 만든다"* 를 금지 서술로 두고 있는 것과 **같은 방향의 외부 틀**이 하나 더 생겼다.

**(라) 🔴 B 도핑은 이 틀에서 음극 MCI 위험을 *더한다*.** 우리 원장 `anode_interface_b2o3.json` 0 V b2o3 행이 이미 **`leaky_products: Li3P(0.7), LiB(0.0)`** — **금속성 LiB** 를 적어 두었다. 반도체/금속 M–X 상 + 연결 → MCI 라는 이 논문의 틀로 읽으면 **B 도핑은 무도핑보다 불리한 쪽**이다. ⚠ 단 그 산물 집합은 `HZ-anode-b2o3-reaction-direction`(BLOCKED) 때문에 **재확인 대기**이고, `LiB` 의 연결성은 아무도 계산하지 않았다.

**(마) 🟡 "도핑이 SEI 를 좋게 만든다" 류 서사는 우리 도구로 검정할 수 없다.** 우리 MLIP-MD 는 **벌크·조성고정·200 ps·계면 없음**이고, 연결성·Onsager·결정성 분석도 0 이다. 이 논문이 **최소한의 동역학 증거**가 어떤 모양인지 보여 줬고, 그 최소한조차 우리에게 없다.

**(바) 🟡 Onsager 교차항 해석의 함정은 우리 Haven 원장과 같은 뿌리다.** 우리 `H_R` 은 골격 기준틀로 재지만 **Langevin 열욕이 교차상관을 희석할 수 있다**는 `[Marc17NE]` digest 의 경고가 이미 있다. 이 논문은 **기준틀을 선언하지 않으면 교차항이 무엇이든 될 수 있다**는 사례를 하나 더 준다 — 우리가 계면 대리조성으로 확장할 때 같은 실수를 할 수 있다.

---

## 19. SI·코드로 **채운 것** / 여전히 **못 채운 것**

**채운 것 (처음엔 SI 가 없었다)**: 학습셋 구성(`Table S1`) · 조성·힘 분해 오차(`Table S2`) · EOS·이량체(`Fig. S3`·`S4`) · 반응산물·에너지(`Table S3`) · **Δμ 전 온도(`Table S4`)** · 전 종 플럭스(`Fig. S11`) · **결정성 정량(τ, `Fig. S12`) + 코드** · **컷오프 민감도(`Fig. S13`)** · 관통 시간 변화(`Fig. S14`) · **Li 대조군의 정체(`Table S5` — 다른 논문·다른 포텐셜·Langevin)** · **경계·관통·결정성·Onsager 드라이버의 정의(코드)** · 포텐셜 하이퍼파라미터(코드).

**⛔ SI·코드로도 못 채운 것 (13)**
1. **생산 계면의 방위(Miller 지수)와 셀 치수** — 옆면은 figure-read ≈137 Å, z 는 코드 주석 ≈842 Å 뿐.
2. **"여러 시드·5,000–500,000 원자·여러 방위" 재현의 개수와 결과.**
3. **생산 궤적의 γ 통계** — 최댓값·표시 비율·중단·도중 재학습 여부. LAMMPS 입력 미포함.
4. **Onsager 핵심 계산**(기준틀·질량중심 처리·적합 창·오차) — 비공개 `py_oats`. **조성별 L 값**(CSV 미포함). 행렬의 **"reference temperature"**. **500·1500 K 결과**.
5. **`Fig. 2` 청록 점선의 출처·가공**(범례 `*`) — 코드에 없다.
6. **Na 계 성장 법칙 적합** — 어디에도 없다.
7. **에너지 표류·밀도 곡선** — "없었다" 는 서술만.
8. **결정성의 시간 곡선 · Li₂S τ · 300 K 결정 기준.**
9. **계면상 전자구조** — 0.
10. **MPContribs 데이터 공개 여부** — **확인 안 함.**
11. **"80 meV Å⁻¹ 필터" 의 진짜 값** — 학습셋 구축 코드 미포함.
12. **ref 9 (Wenzel 2016 *SSI*) 의 원문 판정** — Li₇P₃S₁₁‖Li 가 실험으로 부동태였는지 우리가 확인 안 했다.
13. **`Fig. S6`** — 추출기 누락, 미열람. 그리고 `crystallinity.py`(원시 z [460, 490) Å)와 `percolation.py`(box 기준 분율)의 **z 원점이 같은지** 코드로 판정 불가 → SI 의 "그 창은 x_P < 0.01" 과 `Fig. 5c` 의 P 분포가 맞는지 확인 못 함.

---

## 20. 본 그림 / 안 본 그림 (실독 보고)

**크로핑 결과**: `litdb/figures/li2026_mci_vs_sei_na3ps4_na_mlip_md/` 에 **25개** (본문 `fig_1`–`fig_6` · SI `fig_S1`–`S5`, `fig_S7`–`S14` · 표 `tab_1`, `tab_S1`–`tab_S5`). ⚠ **`Fig. S6` 는 추출기가 "그래픽 없음" 으로 제외**(부제 (a)–(h) 가 사이사이 낀 8 패널 배치에서 영역 판정 실패로 보임). ⚠ `tab_1.png` 는 bbox 가 **8쪽 전체**라 과대 크롭(표는 텍스트로 읽었으므로 영향 없음).

| 파일 | 봤나 | 비고 |
|---|---|---|
| `fig_1` | ✅ | 흐름도, 수치 없음 |
| `fig_2` | ✅ + **원본 래스터 픽셀 판독** | 🔴 Li 점선도 자란다 · decade 당 성장률 (§3d) |
| `fig_3` | ✅ | 🔴 Na 쪽에도 결정 도메인 1개 |
| `fig_4` | ✅ + **컬러바·패널 확대 3장** | 🔴 10²⁰ vs 10¹⁸ · 운동량보존 검산 원자료 · (b) 음수 부호 누락 |
| `fig_5` | ✅ | 🔴 고정 문턱선 · Å→nm 오기 · 가는 목 |
| `fig_6` | ✅ | ⚠ "Crystal Na₂S" · 방향 반대 · 캡션 불일치 |
| `fig_S3` | ✅ + 확대 1장 | EOS 에너지 어긋남 |
| `fig_S4` | ✅ | Na–S 꼬리 과소 |
| `fig_S11` | ✅ | 🔴 NaP₁₅ J_Na ≈ 0 |
| `fig_S12` | ✅ | 🔴 정적 결정 기준 |
| `fig_S13` | ✅ | 🔴 P–P 무관 |
| `fig_S14` | ✅ | 🔴 z-span 창 포화 |
| `fig_S1`·`S2`·`S5`·`S7`·`S8`·`S9`·`S10` | ❌ **안 봄 (7)** | 검증·상도 그림 — `Table S2`·`S3`·`S4` 텍스트로 대체 |
| `Fig. S6` | ❌ **추출 안 됨·안 봄** | RDF 검증 |
| `tab_*` 6장 | ❌ **의도적** | PDF 텍스트 전사 |

⇒ **본문 6/6 · SI 6/13(+누락 1)** 실독. **본문 서술과 어긋난 것 9건**을 그림에서 찾았다: Li 점선 성장(`Fig. 2`) · Na 결정 도메인(`Fig. 3a`) · 단위 지수(`Fig. 4c,d`) · 운동량보존 위반(`Fig. 4c`) · 질량 플럭스 합(`Fig. S11`) · 고정 문턱선·축 단위(`Fig. 5`) · 결정 Na₂S 도식(`Fig. 6`) · 정적 기준(`Fig. S12`) · z-span 포화(`Fig. S14`).

---

## 21. 기법 미니 용어사전

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **SEI / MCI** | SEI = 이온만 통하고 전자를 막아 **스스로 멈추는** 계면상. MCI(mixed conducting interphase) = 이온·전자 둘 다 통해 **계속 자라는** 계면상 (Hartmann 2013) | Na₃PS₄‖Na = MCI **부합** 주장 |
| **ACE** (Atomic Cluster Expansion) | 원자 주변을 다체 기저로 전개한 선형(+임베딩) MLIP. 빠르다 | pacemaker, 350 함수/원소, 7 Å |
| **γ (외삽 등급)** | 새 원자환경이 학습 활성집합 밖으로 얼마나 나갔나(D-optimality). 1 초과 = 외삽 | 1.5 표시 / 5 중단 |
| **r²SCAN** | 메타-GGA 범함수. PBE 보다 결합·에너지가 대체로 낫다 | 라벨. 우리 UMA(omat) 는 PBE(+U) 계열 |
| **Onsager Lᵢⱼ** | 종 i 의 플럭스가 종 j 의 화학퍼텐셜 기울기에 반응하는 선형계수. 대각 = self + distinct 합, 비대각 = 종간 상관 | Eq. 1, **Einstein(MSD 기울기) 형** |
| **self / distinct** | 한 입자 자기 자신의 변위 상관 / **다른 입자끼리**의 상관. "협동 이동" 은 distinct 항이다 | 논문은 **분리 안 함** |
| **기준틀(reference frame)** | 변위를 무엇에 대해 재나 — 질량중심 · 특정 종 고정 · 골격 평균. 교차항 값이 기준틀에 따라 **바뀐다** | **미기재** |
| **운동량보존 제약** | 총운동량 0 인 MD 에서는 Σᵢ mᵢ ΣΔrᵢ = 0 → 이원계 교차항이 질량비로 **강제** | Li 행렬 만족 · Na 행렬 위반 (✎) |
| **결합그래프 퍼콜레이션** | 원자를 점, 컷오프 안 쌍을 선으로 잇고, 연결성분이 양끝을 잇는지 본다 | 고정 평면, Na–P·P–P 간선 |
| **자리 퍼콜레이션 문턱** | 격자 자리를 무작위로 채울 때 무한 연결이 처음 생기는 점유율. fcc 최근접 ≈0.198 | ✎ 우리 §13-3 유도에만 씀 |
| **τ (병진질서 지표)** | (1/7)∫₃¹⁰\|g(r)−1\|dr — 결정은 크고 비정질은 작다 | 0.28 vs 1.35 |
| **용융-급랭(melt-quench)** | 고온으로 녹였다 식혀 비정질 구조를 만드는 절차 | 5000 K → 목표온도 |
| **MPMorph** | atomate2 의 비정질 구조 생성 AIMD 워크플로 | 학습셋 비정질 9,031 배열 |
| **폴라론 호핑** | 전하가 국소 격자왜곡과 함께 자리를 뛰는 전도 기구 | 전자 쪽 가정, **모사 안 함** |

---

## 22. 🔎 확보 후보 (이 편이 가리키는 원전)

| ref | 문헌 | 왜 필요한가 |
|---|---|---|
| **19** 🥇 | **Li, Karan, Kaplan, Wen & Persson**, *J. Phys. Chem. C* **129**(36), 16043–16054 (**2025**) — "An atomistic study of reactivity in solid-state electrolyte interphase formation for Li/Li₇P₃S₁₁" | **Li 쪽 "평탄" 의 원전.** 셀 크기(고갈 여부)·Langevin 마찰·경계 정의·시드 수를 봐야 §9 의 판정을 닫을 수 있다. ⚠ 우리 `[Li25]` 와 **다른 논문** |
| **3** 🥈 | **Hartmann et al.**, *J. Phys. Chem. C* **117**, 21064 (2013) — NASICON‖Li, **MCI 원전** | SEI/MCI 조작적 정의의 원출처 |
| **6** | **Wenzel et al.**, *ACS AMI* **8**, 28216 (2016) — Na₃PS₄·β-알루미나‖Na | 35 h 선형 R(t) 의 원자료 · 우리 `li2026_na_sulfide_halide_interface_review` digest 가 이미 이 논문을 ref 83 로 인용(환원 ≈1.2–1.5 V) |
| **9** | **Wenzel et al.**, *Solid State Ionics* **286**, 24 (2016) — Li₇P₃S₁₁‖Li | "Li₇P₃S₁₁‖Li 부동태" 의 실험 근거가 정말 부동태인지(제목은 *degradation*) |
| **37** | **Karan et al.**, *Nat. Mater.* (2026) — Onsager 방법 | 기준틀·대리조성 규약의 원전 — §3f 의 운동량보존 문제를 풀 열쇠 |
| **50** | **Seel & Pandey**, *Int. J. Quantum Chem.* **40**, 461 (1991) | Li₃P 2.03/3.6 eV 의 방법 확인 |
| 코드 | `py_oats` (비공개) · MPContribs `naps_mci` | 조성별 L · 궤적 |

---

## 23. 이 digest 의 변경 이력

| 날짜 | 무엇 |
|---|---|
| 2026-09-23 | 초판. 본문 13 pp → **SI 15 pp + 저자 코드(@85557ef) 도착 후 전면 반영**. 그림 25개 추출(`Fig. S6` 누락), 본문 6 + SI 6 실독, `Fig. 2` 원본 래스터 픽셀 판독, `Fig. 4`·`Fig. S3` 확대. 1저자 지정 7축 전부 답함. ✎ 재계산 9건(셀 정합 · Li 점선 성장 · Na 가장자리 decade 성장 · 원자당↔f.u.당 반응에너지 · τ 열변위 민감도 · Onsager 지수 · 운동량보존 L · 질량 플럭스 합 · Δμ 부호 분해) + fcc 퍼콜레이션 유도 1건. 본문–그림/코드 불일치 9건 적발. **§8-4 노트 정정 필요 판정(부분).** |
