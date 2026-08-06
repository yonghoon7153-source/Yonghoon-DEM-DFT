# 세미나 용어·기호 규약 + 레퍼런스 (2026-08)

`docs/seminar_20260806_script.md` 의 부속.  **원칙 — 필드에서 실제로 쓰는 용어를 쓰고,
각 용어에 그것을 정의·확립한 문헌을 붙인다.**  우리가 만든 이름(내부 은어)은 발표에서
쓰지 않거나, 쓸 때 "우리 표현"임을 명시한다.

서지 표기: **[✓]** = 우리 자료(정본 litdb 카드 · SDCP Methods SI · 2026-04 덱)에서 **확인됨**
· **[⚠]** = 표준 문헌이지만 권·쪽 등 서지 세부를 **발표 전 확인 필요** (지어내지 않는다).

---

# 0. ★ 먼저 — 우리 자료 안의 기호 충돌 4건 (defense 지뢰)

발표 전에 **반드시** 하나로 정해야 한다.  청중이 못 알아채도, 질문자가 알아채면 무너진다.

## 0-1. ⚠⚠ τ (굴곡도) — 우리 안에 **두 규약이 공존한다**

| 위치 | 관례 |
|---|---|
| `docs/pipeline_step1_to_step5_guide.md:585` | σ_eff = σ_bulk·φ / **τ²** |
| `scripts/step3_sigma.py:1089` (`tau_from_solve`) | σ_eff = σ_bulk·φ / **τ** (선형) |
| `step3_sigma.py:1091` 주석 | *"⚠ 관례 지뢰: `build_tau_regime_db._tau_from_sigma` 는 √(φ·σ/σ_eff) = **τ² 관례**"* |

- **같은 해가 τ = 4 로도, τ = 2 로도 읽힌다.**  숫자를 보고하는 순간 2배 차이가 난다.
- 필드도 통일돼 있지 않다 — "tortuosity τ"(기하 경로비, σ∝1/τ²)와 "tortuosity factor
  τ_f"(σ∝1/τ_f)가 혼용된다.
- ★ **발표 권고 — 세 가지를 동시에 한다**:
  1. 슬라이드에 **식을 그대로 적는다**: `σ_eff = σ_bulk · φ / τ` (선형 관례 명시)
  2. 가능하면 **MacMullin 수** N_M ≡ σ_bulk/σ_eff 로 보고한다 — **규약이 하나뿐이라
     오해가 원리적으로 불가능**하다. [⚠ Landesfeind & Gasteiger 계열 문헌 확인]
  3. 우리 문서의 τ² 표기(가이드 §13)를 선형으로 **통일**하거나, 두 값을 병기한다.

## 0-2. φ 가 세 가지를 뜻한다

| 표기 | 의미 | 나오는 곳 |
|---|---|---|
| φ_e, φ_i | **전위(potential)** [V] | STEP3/4 (∇·σ∇φ = 0) |
| φ_AM, φ_SE | **부피 분율(volume fraction)** [–] | 조성·스케일링 법칙 |
| φ_SE_local | SE 가 제 몫 공간을 채운 비율 | SE 응답곡선 (p.14b) |

- 발표 권고: **부피 분율은 ε 또는 v_f 로 바꾸고 φ 는 전위 전용**으로 쓴다.
  (전기화학 청중에게 φ = 전위가 압도적 표준.  다공도는 이미 ε 를 쓰고 있으니 충돌 없음.)
- 못 바꾸면 **각 슬라이드에서 첫 등장 시 단위를 붙여** 구별시킨다 (φ_e [V] vs φ_SE [–]).

## 0-3. σ 가 전도도이자 응력이다

| 표기 | 의미 |
|---|---|
| σ_ion, σ_e, σ_thermal | **전도도** [S/cm] |
| σ_y, σ_zz, wallP | **응력** [GPa] |

- 두 분야의 표준이라 바꾸기 어렵다.  발표 권고: **응력은 항상 [GPa], 전도도는 항상 [S/cm]
  또는 [mS/cm]** 로 **단위를 반드시 병기**하고, 응력 슬라이드와 전도 슬라이드를 섞지 않는다.

## 0-4. P 가 압력이자 입자 종류다

- **P** = 성형 압력 [MPa] / **P** = AM_P = 큰 다결정 입자 (P:S 비의 P).
- 발표 권고: 입자 쪽은 **"large (polycrystalline)" / "small (single-crystal)"** 로 풀어 쓰고,
  비율은 **L:S** 또는 **PC:SC** 로 표기.  압력만 P 로 남긴다.
  (필드 표준도 poly/single 은 **PC / SC** 다 — Trevisanello 2021 [✓].)

---

# 1. 용어 도입 순서 지도 (모르는 사람이 따라올 수 있게)

> 규칙: **정의되기 전에 나오는 용어가 하나도 없어야 한다.**

| 슬라이드 | 여기서 **처음** 나오는 용어 | 말로 하는 한 줄 정의 |
|---|---|---|
| p.2 | solid electrolyte (SE) · active material (AM) · composite cathode | "액체 없이 분말을 눌러 붙인 양극" |
| p.2 | porosity | "빈 공간 비율" |
| p.3 | EIS | "셀에 교류를 흘려 저항을 재는 법 — 총합만 준다" |
| p.4 | **DEM** · **MPM** | (표로 대비 — 0에서 정의) |
| p.4 | plastic deformation | "눌리면 안 돌아오는 변형" |
| p.5 | calibration / cross-validation | "실험에 맞추는 것 / 서로 안 맞춘 둘이 만나는지 보는 것" |
| p.6 | single-ion conductor · transference number t⁺ | "음이온이 안 움직인다 (t⁺≈1)" |
| p.7 | grid convergence | "격자를 조여도 답이 안 변하는지" |
| p.8 | **Furnas dip** · packing | "작은 공이 큰 공 틈을 메워 더 조밀해지는 것" |
| p.9 | **voxel** · Kirchhoff · **constriction resistance** · **coverage** | 각각 한 줄 |
| p.10 | **LOOCV** · percolation · coordination number (CN) · tortuosity | 각각 한 줄 |
| p.11 | Ridge regression · effective medium theory (EMT) | "정규화 회귀 / 평균 물성으로 바꾸는 근사" |
| p.12 | **Butler–Volmer** · overpotential (η) · polarization | "반응 속도식 / 반응을 밀기 위해 더 준 전압" |
| p.13 | (새 용어 없음 — 의도) | |
| p.14 | **CZM** · CEI · von Mises yield | 각각 한 줄 |
| p.15 | surrogate model · MLIP | "빠른 대역 모델 / ML 원자간 퍼텐셜" |

**★ 원칙**: 한 슬라이드에 **새 용어 3개 이하**.  p.9·p.10 이 지금 4개라 하나씩 Appendix 로 뺄 것.

---

# 2. 본편 용어 슬라이드 (p.4 뒤 또는 배포 카드 1장)

> 실제 배포용: **A4 한 장으로 인쇄해 청중에게 돌린다** (덱 장수에 안 잡힘).

| Term | 뜻 (한 줄) | 우리 파이프라인에서 |
|---|---|---|
| **AM / SE** | 활물질(NCM) / 고체전해질(Li₆PS₅Cl) | 전극을 이루는 두 분말 |
| **DEM** | 입자를 단단한 공으로 보고 뉴턴 운동을 푸는 법 | 패킹·접촉망 (STEP1) |
| **MPM** | 재료를 연속체로 보고 변형을 푸는 법 | 소성 압밀 (STEP2) |
| **Porosity ε** | 빈 공간 비율 [–] | 두 모델의 교차검증 양 |
| **Coordination number CN** | 한 입자가 몇 개와 닿았나 | 전도의 1차 결정자 |
| **Percolation** | 한쪽 끝에서 반대 끝까지 **이어졌나** | 안 이어지면 전도 0 |
| **Tortuosity τ** | 이온이 얼마나 **돌아가나** (직선 대비) | σ_eff = σ_bulk·ε/τ |
| **Constriction resistance** | **좁은 목**을 지날 때 생기는 추가 저항 | 접촉 하나하나의 저항 |
| **Coverage** | AM 표면이 SE 로 덮인 비율 | 반응이 일어날 수 있는 면 |
| **Overpotential η** | 반응을 밀기 위해 **더 줘야 하는 전압** | 손실의 정체 |
| **Butler–Volmer** | 과전압 ↔ 반응 전류의 관계식 | 계면마다 푼다 |
| **CEI** | 사이클마다 계면에 자라는 저항성 피막 | 열화의 98 % |

---

# 3. 전체 용어집 — 필드 표준어 + 레퍼런스

## 3-1. 시뮬레이션 방법

| Term (필드 표준) | 한국어 | 쉽게 말하면 | Reference |
|---|---|---|---|
| **Discrete Element Method (DEM)** | 이산요소법 | 입자를 하나하나 단단한 공으로 보고 뉴턴 방정식을 푼다 | Cundall & Strack, *Géotechnique* **29** (1979) 47–65 [✓] |
| — 구현체 **LIGGGHTS** | | 오픈소스 DEM 코드 | Kloss et al., *Prog. Comput. Fluid Dyn.* **12** (2012) 140–152 [✓] |
| **Material Point Method (MPM)** | 물질점법 | 재료를 연속체로 보되 물질점으로 이력을 나른다 | Sulsky, Chen & Schreyer, *CMAME* **118** (1994) 179–196 [✓] |
| — **MLS-MPM** | | 우리가 쓰는 변종 | Hu et al., *ACM TOG* **37** (2018) 150 [✓] |
| — **Taichi** | | GPU 실행 언어 | Hu et al., *ACM TOG* **38** (2019) 201 [✓] |
| **Hertzian contact** | 헤르츠 접촉 | 두 탄성구가 눌릴 때의 접촉 면적·힘 | H. Hertz, *J. Reine Angew. Math.* **92** (1882) 156 [⚠] |
| **von Mises (J2) plasticity** | 폰미제스 소성 | "모양을 바꾸는 응력"이 한계를 넘으면 영구변형 | von Mises (1913) [⚠] · 교과서: Simo & Hughes, *Computational Inelasticity* (1998) [⚠] |
| **Cohesive zone model (CZM)** | 응집영역모델 | 계면이 떨어질 때 필요한 에너지로 파단을 다룸 | Bucci, Swamy, Chiang & Carter, *J. Mater. Chem. A* (2017) [✓] |

## 3-2. 패킹 · 압밀

| Term | 한국어 | 쉽게 말하면 | Reference |
|---|---|---|---|
| **Furnas packing / bimodal packing** | 이봉 패킹 | 작은 입자가 큰 입자 틈을 메워 더 조밀해짐 | C.C. Furnas, *Ind. Eng. Chem.* **23** (1931) [⚠] · de Larrard, *Concrete Mixture Proportioning* (1999) [⚠] |
| **Heckel equation** | 헤켈 식 | ln(1/(1−D)) = K·P + A — 압력↔밀도 관계 | R.W. Heckel, *Trans. Metall. Soc. AIME* **221** (1961) [⚠ 권·쪽 확인] |
| — **yield pressure P_y** | 항복압 | = 1/K.  재배열 → 소성으로 넘어가는 압력 | 위와 동일 |
| **Random close packing (RCP)** | 무작위 조밀 패킹 | 굴려서 도달 가능한 최대 밀도 (구 ≈ 0.64) | 표준 [⚠] |
| **Cold pressing** | 냉간 가압 | 가열 없이 눌러 굳힘 (황화물의 장점) | Sakuda, Hayashi & Tatsumisago, *Sci. Rep.* **3** (2013) 2261 [✓] |
| **Stack pressure** | 스택 압력 | 셀 운전 중 유지하는 외부 압력 | Cronau et al., *ACS Energy Lett.* **6** (2021) 3072–3077 [✓] |

## 3-3. 수송 (transport)

| Term | 한국어 | 쉽게 말하면 | Reference |
|---|---|---|---|
| **Effective conductivity σ_eff** | 유효 전도도 | 전극 전체로 본 전도도 (재료 자체보다 낮음) | — |
| **Tortuosity τ** | 굴곡도 | 이온이 직선 대비 얼마나 돌아가나 | ⚠ 규약 §0-1 |
| **MacMullin number N_M** | 맥멀린 수 | σ_bulk/σ_eff — **규약이 하나라 안전한 보고 단위** | [⚠ 확인] |
| **Percolation / backbone** | 침투·백본 | 끝에서 끝까지 이어진 뼈대 | Stauffer & Aharony, *Introduction to Percolation Theory*, 2nd ed. (1994) [⚠] |
| **Bruggeman relation** | 브루그만 관계 | σ_eff = σ·ε^1.5 — 균질화 근사 | D.A.G. Bruggeman, *Ann. Phys.* **416** (1935) [⚠] |
| **Effective medium theory (EMT)** | 유효매질이론 | 미세구조를 평균 물성으로 바꿔치기 | 리뷰: *J. Electromagn. Waves Appl.* **37**(2) (2023) 282–322 [✓ 4월 덱] |
| **Constriction / spreading resistance** | 수축·확산 저항 | 좁은 목을 지날 때의 추가 저항 R = 1/(2σa) | R. Holm, *Electric Contacts*, 4th ed., Springer (1967) [✓] · 원형: Maxwell, *A Treatise on Electricity and Magnetism* (1873) [✓ 4월 덱] |
| **Coordination number (CN)** | 배위수 | 한 입자가 닿은 이웃 수 | — (패킹 표준) |
| **Coverage** | 피복률 | AM 표면 중 SE 가 덮은 비율 | 우리 정의 — Hertz(직접 접촉) / Tabor(소성 퍼짐) 두 값 병기 |
| **Grain-boundary (GB) resistance** | 입계 저항 | 결정립 사이의 추가 저항 | Cronau et al. (2021) [✓] |

## 3-4. 접촉 역학

| Term | 한국어 | 쉽게 말하면 | Reference |
|---|---|---|---|
| **Indentation hardness H** | 압입 경도 | 눌렀을 때 견디는 압력 (≈ 3σ_y) | D. Tabor, *Proc. Roy. Soc. A* **192** (1948) 247 [✓ 4월 덱] |
| **Tabor plastic contact area** | 소성 접촉면적 | A = F/H — 탄성 헤르츠보다 큼 | Tabor (1948) [✓] |
| **Fracture toughness K_IC** | 파괴 인성 | 균열이 퍼지기 시작하는 문턱 | Fan et al., ECER-D-26-00097 §3.5 (미출판 draft) [✓ litdb] |
| **Critical energy release rate G_c** | 임계 에너지 방출률 | 계면을 벌리는 데 드는 에너지/면적 | Bucci et al. (2017) [✓] |

## 3-5. 전기화학

| Term | 한국어 | 쉽게 말하면 | Reference |
|---|---|---|---|
| **Butler–Volmer equation** | 버틀러-볼머 식 | 과전압이 크면 반응 전류가 지수적으로 커짐 | Bard & Faulkner, *Electrochemical Methods*, 2nd ed., Wiley (2001) [⚠] |
| **Exchange current density i₀** | 교환 전류밀도 | 평형에서 양방향으로 흐르는 전류 크기 | 위와 동일 |
| **Overpotential η** | 과전압 | 반응을 밀기 위해 평형보다 더 준 전압 | 위와 동일 |
| **Open-circuit potential (OCP/OCV)** | 개회로 전압 | 전류 0에서의 열역학 전압 (SOC 의 함수) | Chen et al., *J. Electrochem. Soc.* **167** (2020) 080534 [⚠ 쪽 확인] |
| **Porous electrode theory** | 다공성 전극 이론 | 전극 두께 방향으로 반응이 퍼지는 이론 | Newman & Tiedemann, *AIChE J.* **21** (1975) [⚠] |
| **DFN (Doyle–Fuller–Newman) model** | | 위 이론의 표준 구현 | Doyle, Fuller & Newman, *JES* **140** (1993) 1526 [⚠] |
| **Transference number t⁺** | 이온 수율 | 전류 중 Li⁺ 가 나르는 비율 (SE 는 ≈1) | 표준 |
| **Reaction front** | 반응 전선 | 반응이 몰려 있는 두께 방향 위치 | Newman 이론의 귀결 [⚠] |
| **EIS / TLM** | 임피던스 / 전송선 모델 | 교류 저항 측정 / 다공성 전극용 등가회로 | Minnmann et al., *JES* **168** (2021) 040537 [✓] |
| **CEI (cathode–electrolyte interphase)** | 양극-전해질 계면상 | 사이클마다 자라는 저항성 피막 | Yun et al., *Energy Storage Mater.* (2023) [✓ 우리 랩] |
| **Parabolic (Wagner) growth** | 포물선 성장 | 확산 제한이면 두께 ∝ √t | C. Wagner (1933) [⚠] |

## 3-6. 재료 · 첨가제

| Term | 한국어 | 쉽게 말하면 | Reference |
|---|---|---|---|
| **Argyrodite Li₆PS₅Cl (LPSCl)** | 아지로다이트 | 대표 황화물 SE, σ ~3 mS/cm | Cronau et al. (2021) [✓] |
| **NCM811 / NMC811** | | Li(Ni₀.₈Co₀.₁Mn₀.₁)O₂ 양극재 | Chen et al. (2020) [⚠] |
| **Polycrystalline (PC) vs single-crystal (SC)** | 다결정 vs 단결정 | PC 는 입계가 있어 균열·저항, SC 는 없음 | Trevisanello et al., *Adv. Energy Mater.* **11** (2021) 2003400 [✓] |
| **VGCF** | 기상성장 탄소섬유 | 전자 고속도로 | (제조사 스펙 + 문헌) |
| **PTFE binder (fibrillated)** | 섬유화 바인더 | 건식 공정의 결합재, **절연체** | DuPont PTFE handbook [⚠ 판·연도] |
| **Mixed ionic–electronic conductor (MIEC)** | 혼합 전도체 | 이온·전자를 **둘 다** 나름 (= SDCP) | 표준 용어 [⚠] |

## 3-7. 통계 · ML

| Term | 한국어 | 쉽게 말하면 | Reference |
|---|---|---|---|
| **LOOCV (leave-one-out CV)** | 하나빼기 교차검증 | 하나 가리고 나머지로 배워 그 하나를 맞힌다 | 표준 — Hastie, Tibshirani & Friedman, *ESL* (2009) [⚠] |
| **Ridge regression** | 능형 회귀 | 계수를 억눌러 과적합을 막는 회귀 | 위와 동일 |
| **Surrogate model** | 대리 모델 | 무거운 시뮬레이션을 흉내내는 빠른 모델 | 표준 |
| **MLIP (ML interatomic potential)** | ML 원자간 퍼텐셜 | DFT 정확도를 MD 속도로 | MACE / UMA (4월 덱) [⚠] |
| **Symbolic regression (SISSO)** | 기호 회귀 | 데이터에서 **식 자체**를 찾아냄 | [⚠] |

## 3-8. ⚠ 우리 내부 표현 — 발표에서 쓰지 말거나 반드시 풀어 쓸 것

| 내부 표현 | 발표에서는 | 이유 |
|---|---|---|
| **frame[4] / frame[5]** | "independent calibration & cross-validation" / "complementary model division" | 우리 문서 안의 번호일 뿐 |
| **Stage-E** | "plastic contact-area correction (Tabor)" | 내부 단계 이름 |
| **wallP** | "platen reaction stress" | 내부 변수명 |
| **STEP1–5** | "packing / compaction / transport / electrochemistry / degradation" | 숫자보다 이름이 전달됨 |
| **kit / payload / ledger** | "input package" / "post-processing tool" | 내부 도구명 |
| **near-null** | "near-singular system" | 수치해석 표준어는 singular |
| **ASSUMED-FORM** | "assumed functional form (magnitude anchored, shape assumed)" | 라벨 자체는 좋지만 풀어 써야 함 |
| **SBE / DBE** | 슬라이드에 정의 병기 (single/dual-binder electrode 등 실제 뜻) | 약어가 자명하지 않음 |

---

# 4. 발표 전 체크리스트 (용어 한정)

- [ ] **τ 규약을 하나로 확정**하고 슬라이드에 식을 적었는가 (§0-1) — **최우선**
- [ ] φ 가 전위/부피분율로 혼용되지 않는가, 혹은 단위가 병기됐는가 (§0-2)
- [ ] 응력과 전도도가 같은 슬라이드에 σ 로 함께 나오지 않는가 (§0-3)
- [ ] P:S 를 PC:SC 또는 large:small 로 바꿨는가 (§0-4)
- [ ] 정의 전에 나오는 용어가 하나도 없는가 (§1 지도)
- [ ] 슬라이드당 새 용어 ≤ 3 인가 (p.9 · p.10 확인)
- [ ] 내부 표현(frame[5] · Stage-E · wallP · kit)이 본편에 남아 있지 않은가 (§3-8)
- [ ] [⚠] 표시된 서지 세부를 **확인했거나**, 확인 못 한 것은 인용을 뺐는가
- [ ] SBE / DBE 가 처음 나올 때 풀네임이 있는가
- [ ] 용어 카드(§2)를 인쇄해 가져가는가
