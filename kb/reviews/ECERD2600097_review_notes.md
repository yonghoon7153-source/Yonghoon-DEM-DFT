# 📝 리뷰 노트 — ECER-D-26-00097 (Fan 외, *Stability Issues in Sulfide-Based ASSB*)

> **무엇**: 1저자가 리비전 중인 113 pp 리뷰 원고를 읽으며 **건진 문장 + 그 문장에 대한 우리 해석**을 쌓는 곳.
> **원고 digest**(내용 요약·수치 총정리)는 따로 있다 → `litdb/papers/fan2026_sulfide_assb_stability_review_ECERD2600097.md`.
> 여기는 요약이 아니라 **읽으면서 든 판단**이다 — 세미나 답변·인용문 후보·원고에 물어볼 것.
>
> ⚠ **미출판 심사 중 원고**다. 인용문은 이 repo 안에서만 쓰고, 외부 발표·투고에 **원문 그대로 옮기지 않는다**
> (아래 "우리 표현" 칸의 순화 문장을 쓴다).
>
> ⚠ **세 층을 절대 섞지 않는다** — 문서 전체가 이 구분을 지킨다.
> ① 🔵 **원문 인용** (그들이 쓴 문장 그대로)
> ② 🟢 **우리 해석** (우리가 붙인 물리 — 원고엔 없다)
> ③ 🔴 **원고가 얼버무린 곳** (리뷰어로서 지적할 것 / 인용할 때 손봐야 할 것)

---

## §3.1 Air Stability — *왜 황화물은 드라이룸을 벗어나면 죽는가*

**한 줄**: 이 절의 논리는 딱 두 개다 — **결합에너지가 낮다** + **S²⁻가 soft base 다**.

### 🔵 건진 문장 (원문)

> "The P–S bond or M–S bond (where M represents electroactive or structurally stable cations
> such as Ge, Sn, or Si) within the material exhibits **lower bond energy and stronger
> polarizability** compared to the M–O bond in oxide, making it susceptible to attack by
> water molecules or oxygen [78]."

> "The sulfur anion (S²⁻) in the lattice exhibits typical **soft-base behavior**, which has a
> strong affinity for protons or polar molecules in the environment."

### 🟢 우리 해석 — HSAB 한 방으로 꿰기

원고는 "S²⁻가 soft base라 양성자·극성분자에 친화성이 강하다"까지만 쓴다.
그런데 그 문장은 결국 **P–O가 P–S보다 안정하다**는 말의 다른 표현이다. 물이 왔을 때 반응 방향은

> **P⁵⁺(hard acid)가 S²⁻(soft base)를 버리고 O²⁻(hard base)를 잡는 쪽이 유리**

이고, 짝이 hard–hard(P–O) · soft–soft(H⁺–S²⁻ → H₂S)로 **재배열**되는 것이다. 대표 반응식 하나면 세미나에서 충분:

```
Li₃PS₄ + 3 H₂O  →  Li₃PO₄ + 3 H₂S↑
```

아지로다이트(LPSCl)면 **PS₄³⁻ 사면체가 깨지면서 H₂S가 나오고 격자가 무너지는** 그림.

### 🔴 원고가 얼버무린 곳 — 리뷰 지적 후보

| # | 지점 | 무엇이 문제 | 우리 입장 |
|---|---|---|---|
| **A1** | *"moisture and oxygen"* 을 계속 **병렬**로 놓는다 | 실제로는 **H₂O 가수분해가 압도적으로 빠르고 지배적**이다. 건조한 O₂만 있는 조건의 순수 산화는 훨씬 느리다 — 대기 열화 실험이 대부분 **RH를 변수로** 잡는 게 그 증거 | 세미나 질문 *"산소랑 물 중 뭐가 주범이냐"* → **물, O₂는 조연.** 원고는 이 구분을 안 해준다 → **리비전에서 분리 요구** |
| **A2** | soft base 라서 **"kinetic barrier 가 낮다"** 고 씀 | **HSAB 는 열역학적(thermodynamic) 선호를 설명하는 틀**이다. 원고는 이걸 속도론으로 바로 연결했는데 **둘은 다른 축**이다. 열역학적으로 P–O 가 유리한 것과 반응이 실제로 빠른 것은 별개 — 실제 가수분해 속도는 **표면적 · 결정성(비정질 유리 > 결정질) · 조성**에 크게 좌우된다 | ⚠ **인용할 때 원문 그대로 옮기지 말 것.** 아래 "우리 표현"으로 순화 |

**우리 표현 (인용용 순화 문장)**

> "S²⁻의 soft-base 특성이 가수분해를 **열역학적으로 유리하게** 만든다."

— *"kinetic barrier를 낮춘다"* 로 쓰지 않는다.

### 🟢 곁가지 — *low-temperature compressible processing* 의 진짜 의미

원고가 장점으로 흘리는 이 표현이 실은 **황화물의 킬러 장점**이다.

- 산화물(LLZO 등)은 **1000 °C 넘는 소결**이 필요하다.
- 황화물은 **영률이 낮고 무르기 때문에 상온에서 압력만으로 치밀화**된다 → 냉간압착 셀 제작이 가능.

★ **장점과 약점이 같은 물성(낮은 강성)에서 나온다** — 무르니까 상온 성형이 되고, 무르니까 대기 노출에
약한 "무른 소재"다. 발표에서 이 양면성을 한 문장으로 짚으면 흐름이 깔끔해진다.

### 🔗 §3.1 이 다음 섹션에 던지는 떡밥

§3.1 은 **"왜 약한가"만** 설명하고 **"그래서 어떻게 막나"는 아직 안 나온다**.
그런데 **HSAB 논리를 뒤집으면 대응책이 그대로 도출**된다 — 문제 제기(§3.1) ↔ 답(뒤 regulation strategy).
발표 흐름 잡을 때 이 대응 관계를 **표로 미리** 준비할 것:

| §3.1 이 말한 취약점 | HSAB 를 뒤집은 대응 | 구체 수단 |
|---|---|---|
| S²⁻(soft base)를 뺏긴다 | **soft acid 를 넣어 S 를 붙잡아 둔다** | Sn⁴⁺ · Sb 치환 |
| P–S 가 P–O 보다 불안정 | **O 를 미리 조금 넣어 P–O 를 만들어 둔다** | oxygen doping |
| 물이 들어온다 | **hard base scavenger 로 물을 먼저 잡는다** | 금속산화물 첨가제 |

> 🔎 **우리 캠페인과의 접점** — 위 3행이 전부 우리가 이미 손대고 있는 축이다.
> ① soft-acid 치환 = `air_hsab` 스크리닝 축 · ② oxygen doping = **LPSOCl**(gap 2.2309 eV, ICOHP P–O 강결합)
> · ③ 강결합으로 취약 단위를 묶기 = **+B₂O₃**(B–S 가 free-S 를 −1.1 → −2.15 eV 로 안정화).
> ⚠ 단 **우리 계산은 0 K hull 축이고 가수분해(H₂O/H₂S 기체)는 그 밖**이다 —
> "우리가 H₂S 억제를 계산했다"는 주장 금지 (digest §11 과 같은 규율).

### 🔵 건진 문장 (2차분)

> "This process triggers **local structural rearrangements or interfacial phase transitions**,
> leading to a **continuous deterioration of interfacial transport properties** during
> electrochemical cycling."

> "From a structural perspective, the **low lattice energy, insufficient charge density, and
> highly polar covalent bond characteristics** collectively constitute the root causes of the
> **thermodynamic and kinetic** susceptibility of sulfide SEs to hydrolysis and oxidation reactions."

> "The **Hard-Soft-Electron-Hole (HSEH) theory** proposed by Mulks et al. extends the HSAB
> concept to **multi-electron systems** [80]."

### 🟢 우리 해석 (2차분)

**Q3 — 이 문장이 절의 무게중심을 옮긴다.**
앞까지는 "보관·취급 중 대기 노출"(storage) 얘기였는데, 이 문장은 그 피해가 **셀을 밀봉한 뒤에도
사이클 내내 계속된다**(operation)로 넘긴다. 대기 노출로 계면에 심어진 산물이 **씨앗**이 되어
사이클마다 상전이·재배열을 이어간다는 것 — *"잠깐 노출됐는데 괜찮겠지"* 가 안 통하는 이유가 여기다.
발표에서 **"대기 안정성은 보관 문제가 아니라 수명 문제"** 한 줄로 쓰면 잘 먹힌다.

**Q4 — 이 절 전체의 '근본 원인' 요약문.** 구조 기술자 세 개를 세운다:
① 낮은 격자에너지 ② 불충분한 전하밀도 ③ 강한 극성 공유결합.
★ 이 세 개가 **정확히 우리가 계산으로 갖고 있는 축**이라 접점이 제일 좋은 문장이다:

| 원고의 정성 기술자 | 우리 정량 대응물 | 어디에 |
|---|---|---|
| low lattice energy | EOS **B₀** · E_hull | `db/properties/eos.json` · explorer |
| (in)sufficient charge density | **Bader 净전하** (Li·P·S 자리별) | `db/properties/bader_ae_*.csv` |
| polar / covalent 성격 | **ICOHP P–S** · **ELF 결합 중앙 최솟값** | `db/properties/*icohp*` · `elf_bonds_3sys_origin.csv` |

> 값은 여기 옮기지 않는다 → `litdb/our_dft_baseline.md` · `/explorer`.
> ⚠ 그래도 **"우리가 가수분해를 계산했다"는 주장은 금지** — 우리 축은 0 K hull 이고
> H₂O/H₂S 기체는 그 밖이다. 쓸 수 있는 말은 *"원고가 정성으로 지목한 근본 원인에 대해
> 우리는 조성별 정량 기술자를 갖고 있다"* 까지.

**Q5 — HSEH.** HSAB 는 원래 **2중심·2전자** 짝짓기 휴리스틱인데, HSEH(Mulks, Chem 2024)는 이를
**다전자계 + 전자/홀 거동**으로 확장한 틀이다. 우리에게 반가운 이유는 **화학 휴리스틱을
전자구조 관측량으로 갈아타는 다리**이기 때문 — HSEH 를 들먹이는 순간 자연스러운 정량 언어가
**밴드엣지 성격 · 결합분해 COHP · 전하 재분배**가 되고, 그건 우리가 이미 내는 것들이다
(LPSOCl 의 O 2p 매몰·깨끗한 엣지, B₂O₃ 의 free-S 안정화가 그 결의 관측량).

### 🔴 원고가 얼버무린 곳 (2차분)

| # | 지점 | 무엇이 문제 | 우리 입장 |
|---|---|---|---|
| **A3** ⭐ | Q4 의 *"highly **polar** covalent bond"* | **분극률(polarizability) ↔ 극성(polarity) 을 뒤섞었다.** 앞(Q1)에서는 P–S 가 M–O 대비 *stronger polarizability* 라고 옳게 썼는데, 여기선 *highly polar* 라 한다. 전기음성도 차는 Δχ(P–S) ≈ 0.4 vs Δχ(P–O) ≈ 1.25 — 즉 **P–S 는 산화물보다 덜 극성이고 더 공유결합적이며, 대신 더 분극되기 쉽다**(무른 전자구름). 논지에 필요한 건 **높은 분극률**이지 높은 극성이 아니다 | **리비전 지적 1순위.** 두 용어를 갈라 쓰도록 요구. 우리 쪽 대응물도 **ICOHP(공유성)** 와 **ELF(전자 국재)** 로 갈려 있어 구분이 실익이 있다 |
| **A4** | Q4 의 *"thermodynamic **and** kinetic susceptibility"* | **A2 와 같은 뭉갬이 재발**한다 — 이번엔 요약문에서. 1회성 표현 실수가 아니라 **원고 전반의 패턴** | 리뷰 코멘트를 "이 문장 하나"가 아니라 **"절 전체에서 두 축을 분리하라"** 로 올려 쓴다 |
| **A5** ✅ **판정 완료 (2026-08-05, 원문 정독)** | Q5 의 HSEH | **① 황화물·무기고체 적용 선례 0건** — 전부 이산 분자(ORCA 가우시안 기저·기체상), 주기계·슬랩·표면 계산 0. S 포함 종은 DMSO·SCN⁻ 뿐, 고체에 가장 가까운 분자 27 조차 *"결정 구조를 잘라 분자로 축소"*. **② 그러나 HSAB 대비 새로운 건 실재한다** — EHR/EHI 로 **한 분자 안 자리별** hard/soft 를 부호 하나로 가르고, HSAB·Fukui 가 틀리는 SCN⁻·CN⁻·isoquinoline 을 실제로 뒤집는다 | ⛔ **단순 name-drop 지적은 부적절** (이론 자체는 알맹이가 있다). 대신 **"고체 적용은 미검증 유비임을 명시하라"** 로 간다. → `litdb/papers/mulks2024_hard_soft_electrons_holes.md` §1.5 |

### 🔵 건진 문장 (3차분) — §3.1 맺음 · **미래 모델 요구사항**

> "These models should comprehensively describe **bond-energy strengthening mechanisms**,
> **multiscale interfacial phase-transition kinetics**, **electron-hole coupling behavior**,
> and **solid-gas interface reaction thermodynamics**."

### 🟢 우리 해석 (3차분) — ★ 이 한 문장이 우리 좌표를 다 찍어준다

원고가 "공기안정성을 **정량 예측**하는 이론모델이 아직 없다"며 그 모델이 갖춰야 할 것을 **넷**으로 센다.
그런데 이 넷은 곧 **우리가 지금 어디 서 있는지 재는 자**다 — 그대로 대응표를 만들면:

| # | 원고가 요구하는 것 | 우리 상태 | 무엇으로 |
|---|---|---|---|
| ① | **bond-energy strengthening** | ✅ **보유** | ICOHP P–S(5계 canonical) · ELF 결합 중앙 최솟값 · **+B₂O₃ 의 free-S 안정화**(B–S 가 −1.1 → −2.15 eV) · LPSOCl 의 P–O |
| ② | **multiscale interfacial phase-transition kinetics** | ⛔ **완전 공백** | `open_items` **T3**(Li‖LPSCl 반응 MD) 미착수. 프로토콜만 확정 |
| ③ | **electron-hole coupling** | 🔶 **부분** | 우리는 PDOS·밴드엣지 성격·Bader 재분배까지. **HSEH**(ref [80] Mulks)가 이 칸의 이론틀 — digest 작업 중 |
| ④ | **solid-gas interface reaction thermodynamics** | 🔶 **이제 개시 가능** | `open_items` §H 의 ΔG_hyd 축 **0건**. **[Zhu20] ref [84] 의 레시피 + SI 정답지 확보(2026-08-05)** 로 착수 조건이 갖춰졌다 |

★ **구조적으로 재미있는 점** — 원고가 "필요하다"고 나열한 넷 중 **③과 ④는 원고 자신이 인용한
ref [80](HSEH)·[84](Zhu 가수분해 열역학)가 이미 부분적으로 하고 있는 것**이다.
즉 이 문장은 *"아직 아무도 안 했다"* 가 아니라 *"흩어져 있는 걸 아직 아무도 안 합쳤다"* 가 정확하다.

### 🔴 원고가 얼버무린 곳 (3차분)

| # | 지점 | 무엇이 문제 | 우리 입장 |
|---|---|---|---|
| **A6** | 미래 모델 4요건을 **일반적 소망 목록**으로 나열 | 넷 중 ③·④ 는 **원고가 같은 절에서 인용한 ref [80]·[84] 가 이미 다루는 축**이다. 그런데 원고는 "무엇이 이미 되어 있고, 무엇이 아직 빈칸인지"를 가르지 않는다 → 독자에겐 넷 다 미개척으로 읽힌다 | **리비전 요구**: 각 요건에 **현재 도달점(어느 ref 까지)** 과 **남은 간극**을 한 줄씩 붙일 것. 그래야 outlook 이 실행 가능한 로드맵이 된다 |


---

## §3.2 Solvent Compatibility — *습식공정 용매가 PS₄ 를 깨는 이유*

### 🔵 건진 문장

> "Furthermore, **N-methyl pyrrolidone**, as a widely used industrial solvent, has a **high
> dielectric constant and strong solvation ability**. It **irreversibly reacts** with **PS₄³⁻ or
> P₂S₇⁴⁻** structural units in sulfides, causing **P–S bond breakage and structural unit
> rearrangement**."

> "Based on the **HSAB theory**, the central atom **P⁵⁺** in sulfide SEs belongs to
> **relatively soft Lewis acids**, while polar solvent molecules containing lone pairs of
> electrons can act as **strong Lewis bases** and attack nucleophilically, inducing P–S bond
> cleavage and generating low-conductivity structural units (Figure 4b)."

> "For instance, incorporating stabilizing components like **InF₃** enhances **lattice bond
> energy** and **reduces polarizability**, which enables modified sulfide SEs to maintain high
> ionic conductivity even after organic solvent immersion (Figure 4c)."

### 🟢 우리 해석 — §3.1 과 **같은 논리, 다른 공격자**

물(H₂O) 자리에 **고립전자쌍을 가진 극성 용매**가 들어온 것뿐이다. NMP 는 아미드 N·카보닐 O 로
**친핵 공격** → PS₄³⁻ 의 P 를 치고 → P–S 절단 → 구조단위 재배열 → 저전도 분해상.
즉 §3.1(가수분해)과 §3.2(용매분해)는 **하나의 반응 유형**이고, 바뀐 건 공격자의 정체뿐이다.

★ **원고는 이 기전을 HSAB 로 설명하려다 스스로 발이 걸린다** (→ A7·A9).
가수분해(§3.1)와 용매분해(§3.2)를 **하나의 HSAB 서사**로 묶으려면 P⁵⁺ 의 분류가 두 절에서
같아야 하는데, 실제로는 반대다. 우리 쪽 정리로는 **둘 다 hard–hard 전하 제어**로 읽는 편이
일관된다 — P⁵⁺(hard) 가 O²⁻·N/O 주개(hard) 를 선호해서 S 를 내주는 그림.

★★ **대응책 문장(InF₃)이 세 가지를 한꺼번에 드러낸다** —
① 원고의 실제 논리축은 **polarizability** 다(*"reduces polarizability"*). §3.1 의 문제 진단도
*"stronger polarizability"* 였다. 즉 Q4 의 *"highly **polar** covalent"* 는 **원고 자신의 축에서
벗어난 표현**이고 → **A3 가 원고 문장으로 확증**된다.
② InF₃ 가 듣는 이유는 **§3.1 논리(soft-ish acid 가 S 를 붙잡는다)로만 설명되고 §3.2 논리
(P⁵⁺=soft 라 hard 주개에 공격당한다)로는 설명되지 않는다** → **A7 의 실증 반례**.
③ 그리고 그 설명이 맞다는 걸 **[Zhu20] SI 정량값이 뒷받침**한다 (아래).

> 🔎 **문헌 교차검증** — [Zhu20] SI 가수분해 ΔG (문헌 소환값, `db/properties/zhu2020_si_hydrolysis_energies.csv`):
> **In₂S₃ = +0.599 eV** · Ga₂S₃ +0.362 · **Li₂S = +0.225(기준선)** · P₂S₅ −0.156 · **B₂S₃ −0.901**.
> In 은 기준선보다 **훨씬 위** = S 를 잘 붙든다 → InF₃ 전략이 **정량적으로도 말이 된다**.
> ⚠ 이건 **이성분 황화물 프록시**이지 도핑된 SE 의 값이 아니다(`open_items` #11-1).

정량 손잡이는 원고 자신이 다른 데서 쓰는 **donor number(DN)** 다 —
DN 이 크면(강한 σ-주개) 공격이 세고, 방향족·무배위 용매(톨루엔·헵탄)는 불활성.
**공정 선택 규칙이 여기서 바로 나온다**: 습식공정 용매는 **DN 이 낮은 것**으로.

> 🔎 **우리 접점** — 공격 표적이 **PS₄³⁻ 사면체**와 (아지로다이트라면) **free S²⁻** 다.
> 우리 `+B₂O₃` 결과가 *"B–S 가 free-S 를 −1.1 → −2.15 eV 로 안정화"* 였으니,
> **"취약 단위를 강결합으로 묶는다"는 같은 처방이 용매 축에도 적용되는가**가 열린 질문이다.
> ⚠ 단 우리는 **용매 분자와의 반응을 계산한 적이 없다** — ICOHP 는 격자 안 결합 세기이지
> 친핵 공격 저항이 아니다. 이 접점은 **가설**로만 적는다.

### 🔴 원고가 얼버무린 곳

| # | 지점 | 무엇이 문제 | 우리 입장 |
|---|---|---|---|
| **A7** ⭐⭐ **원문 확인됨 (2026-08-05)** | **P⁵⁺ 의 hard/soft 가 두 절에서 뒤집힌다** | §3.2 원문: *"the central atom **P⁵⁺** … belongs to **relatively soft Lewis acids**"*. 그런데 §3.1 의 가수분해 논증은 **P⁵⁺ = hard acid** 여야 성립한다 — P⁵⁺ 가 hard 라야 hard base 인 O²⁻ 를 S²⁻ 보다 선호하고, 그래야 `Li₃PS₄ + 3H₂O → Li₃PO₄ + 3H₂S` 가 유리해진다. **P⁵⁺ 가 정말 soft 라면 soft base 인 S²⁻ 를 붙들고 있어야 하고, §3.1 의 가수분해 구동력 자체가 사라진다.** 즉 용어 흔들림이 아니라 **두 절의 기전이 HSAB 안에서 양립 불가**다. (Pearson 표준 분류에서 P⁵⁺ 는 Si⁴⁺·Al³⁺ 와 함께 **hard acid** 쪽이다) | **리비전 지적 최우선.** 어느 쪽을 택하든 다른 절을 고쳐야 한다. "무엇에 대해 상대적으로"를 반드시 명시하고, 두 기전이 공존한다면 **조건(수계/비수계·전하 vs 궤도 제어)** 을 갈라 서술할 것 |
| **A12** ⭐⭐⭐ ✅ **원전 확인 — 인과가 뒤집혔다 (2026-08-05)** | InF₃ 문장의 *"enhances **lattice bond energy** and **reduces polarizability**"* | **두 표현 모두 인용 논문에 없다.** 게다가 원 논문의 *"lower **polarization rate**"* 는 **F⁻ 치환이 이온전도도를 *낮추는* 이유**로 등장한다 — 리뷰는 그걸 **장점으로 뒤집어** 옮겼다. 즉 정의 부재를 넘어 **인과 방향 오인용**이다 | **확정 지적으로 승급.** 표현을 원 논문 근거(H₂O·유기용매 **흡착에너지 저하**, HSAB soft–soft 결합)로 바꾸거나, *"lattice bond energy"* 를 어느 계산량으로 정의하는지 밝히도록 요구 → `litdb/papers/li2024_inf3_argyrodite_ultrathin_film.md` §13 |
| **A13** ⭐⭐ ⚠ **방향 수정 (2026-08-05, 원전 정독)** | InF₃ 의 In/F 기여 | ⛔ **"분리하라"고 쓰면 반박당한다** — 원 논문은 **단일 도펀트 대조군을 실제로 갖고 있다**: σ 축 `Fig. S8`(pristine 4.8 → **In-only 7.0** / **F-only 4.3** mS cm⁻¹), 수분 축 `Fig. S22`(흡착 감소 **In 0.12 / F 0.15 / co-doped 0.32 eV**). 게다가 **그 논문은 리뷰 교신저자 본인의 것**이다. ★ 진짜 문제는 따로 있다 — **두 축에서 In 과 F 의 부호가 반대다**(σ: In↑·F↓ / 수분: F>In). 그리고 **리뷰가 실제로 인용한 축(유기용매 침지 후 σ 유지)에는 단일 도펀트 대조군이 없다**(`Fig. 4a`·`Fig. S24b` 는 pristine vs co-doped 2 점뿐) | **쓸 형태**: *"인용 논문은 σ·수분 두 축에서 단일 도펀트 대조군을 갖고 있고 **두 축에서 두 원소의 부호가 반대**다. 그런데 §3.2 가 인용한 용매 축에는 그 대조군이 없다. 통합된 'stabilizing component' 서술이 이 반전과 미분리를 모두 지운다 — **어느 축에서 어느 원소가 무엇을 담당하는지** 한 문장이라도 갈라 주면 §5.2.2 의 in-situ 불화물층 논의와도 정합해진다."* |
| **A10** ✅ **사실오류 (확정)** | *"proposed by **Mulks et al.**"* | ref [80] 은 **Florian F. Mulks 단독 저자**다 (RWTH Aachen, *Chem* **10**, 2724–2744, 2024, DOI 10.1016/j.chempr.2024.06.013). *et al.* 이 틀렸다 | 고치기 쉬운 **사실 오류** — 리뷰어 코멘트로 넣으면 확실히 반영된다 |
| **A11** ⭐ | 원고가 HSEH 로 *"환경 자극 하 **황화물 격자의 전자구조 진화**를 설명"* 한다고 쓴 대목 | ref [80] 은 **격자를 다룬 적이 없다**. 전부 이산 분자·기체상이고, 고체에 가장 가까운 사례(분자 27)조차 본문이 *"A simplification of the structure in the solid state was utilized"* — 결정을 잘라 분자로 축소했다. 즉 **고체를 계산한 게 아니라 피해서 계산**했다 | A5 가 "고체 적용은 유비"라면, 이 문장은 **유비를 넘어 없는 결과를 귀속**한다 → 더 강한 지적. 문장을 *"분자계에서 제안된 틀"* 로 한정하도록 요구 |
| **A9** ⭐ | 같은 문장의 *"strong **Lewis bases**"* | HSAB 짝짓기 규칙은 **soft acid ↔ soft base** 다. 그런데 NMP 의 공여 원자는 **아미드 N·카보닐 O** = **전형적 hard base**(Pearson: H₂O·NH₃·RO⁻·R₂O 계열). 즉 원고 서술대로 *P⁵⁺=soft* 를 받아들이면 **soft acid + hard base = 부조화 짝** 이라 HSAB 는 오히려 **공격이 약할 것**이라 예측한다 — 문장이 인용하는 바로 그 이론이 문장의 결론을 지지하지 않는다. ⚠ 게다가 원고가 이 절의 **정량 손잡이로 쓰는 donor number 는 SbCl₅ 기준의 σ-주개 세기 척도**라 hard 계열 basicity 다 → **DN 상관이 잘 맞는다는 사실 자체가 P⁵⁺ 를 hard 로 읽어야 한다는 방증** | HSAB 를 근거로 들 거면 **짝짓기 방향이 맞는지** 확인하도록 요구. 아니면 이 기전을 HSAB 가 아니라 **전하 제어(hard-hard) 친핵 치환**으로 다시 쓰는 편이 정직하다 |
| **A8** | *"irreversibly reacts"* 의 근거 | 비가역성은 **열역학(ΔG<0)** 인가 **동역학(역반응 장벽)** 인가 — 또 A2·A4 와 같은 축 뭉갬이다. 원고는 근거를 안 단다 | 실험 근거(회수 후 σ 미복원 등)가 있으면 그것을, 계산이면 반응에너지를 인용하도록 요구 |


---

## §3.3 Thermal Stability — *"400–500 °C 안정"이 안전성으로 읽히는 문제*

### 🔵 건진 문장

> "From the intrinsic material perspective, most crystalline sulfide SEs exhibit a high thermal
> stability maximum. **Under inert atmospheres**, representative materials such as **LGPS, LPSCl,
> and Li₇P₃S₁₁** maintain stable crystal structures within the **400–500 °C** range without
> significant thermal decomposition or phase transitions, which demonstrates **thermal resistance
> significantly superior to conventional carbonate-based liquid electrolytes** (Figure 5a)
> [99,101,102]. This elevated thermal decomposition temperature primarily results from the
> **continuous covalent-ionic hybrid bond network** within the sulfide lattice and the **low
> content of volatile components**, providing enhanced structural retention under thermal excitation."

### 🔴 원고가 얼버무린 곳

| # | 지점 | 무엇이 문제 | 우리 입장 |
|---|---|---|---|
| **A14** ⭐⭐ **구조화학 오류** | *"**continuous** covalent-ionic hybrid bond network"* | **LPSCl(아지로다이트)의 음이온 골격은 연결망이 아니라 고립 PS₄³⁻ + free S²⁻ + Cl⁻ 다.** 원고 자신이 §3.1·§3.2 에서 *"PS₄³⁻ **structural units**"* 라 부른 그것이다. 세 물질을 한 문장으로 묶었지만 실제로는 **연결도가 다 다르다** — LGPS 는 (Ge/P)S₄ 사슬, Li₇P₃S₁₁ 은 P₂S₇⁴⁻ 이합체 + PS₄³⁻, **LPSCl 은 완전 고립**. "continuous network" 로 뭉뚱그리면 **원고 자신의 §3.1 서술과 충돌**한다 | **리비전 지적 강도 상위.** 세 물질의 **음이온 연결도(isolated / dimer / chain)를 갈라 쓰고**, 열안정 기여를 연결도와 연결지어 서술하도록 요구. 그래야 §3.1(고립 PS₄ 가 공격받는다)과 §3.3(연결망이 열에 강하다)이 안 부딪힌다 |
| **A15** ⭐⭐ | *"under **inert atmospheres**"* → *"thermal resistance significantly superior to carbonate liquid electrolytes"* | **조건과 결론이 어긋난다.** 불활성 분위기의 상전이 온도는 **셀 안전성과 거의 무관**하다 — 실제 열 위험은 SE 단독이 아니라 **충전된 양극의 O₂ 방출·Li 금속과의 발열 반응**이고, 그건 400–500 °C 훨씬 아래에서 시작한다. 게다가 카보네이트 액체의 위험은 **분해 온도가 아니라 인화점·증기압·발열 폭주**다(DMC 인화점 ~18 °C). **분해온도끼리 비교하는 것 자체가 축이 안 맞는다** | *"불활성 분위기 기준"* 을 결론 문장에도 달고, 안전성 비교는 **DSC 발열 개시온도·발열량(J/g)**, 그리고 **양극/Li 공존 조건**에서 하도록 요구 |
| **A16** | *"**low content of volatile components**"* | 관찰 자체는 타당하나(고체 vs 통째로 휘발성인 액체) **황화물의 열분해 산물에 H₂S·S 가 있다**. "휘발 성분이 적다"가 곧 "방출 위험이 낮다"는 아니다 — §3.1 이 같은 H₂S 를 위험으로 다룬다 | 분해 **온도**와 분해 **산물의 독성/가연성**을 갈라 쓸 것 |
| **A17** | **400–500 °C** 의 성립 조건 | 승온속도·분위기·시편(분말/펠릿)·측정법(TGA vs DSC vs in-situ XRD)에 따라 달라진다. ref [99,101,102] 세 편이 같은 조건인지도 불명 | **B4 계열** — 임계 수치에 (a)방법 (b)조건 (c)출처 한 줄 |

### 🔵 건진 문장 (§3.3 대응책)

> "**Introducing oxygen** into sulfide lattices to form **oxysulfide SEs** increases **P–O bond
> ratios** and **enhances overall bond energy**, thereby reducing decomposition tendencies at
> elevated temperatures [89,110]. Concurrently, introducing **thermally stable oxide coatings**
> (e.g., **LiNbO₃ or Al₂O₃**) onto cathode particle surfaces effectively **buffers oxygen
> evolution** and inhibits direct contact with sulfide SEs, **significantly delaying the onset of
> interfacial exothermic reactions**."

### 🟢 우리 해석 — ★ O 도핑이 **두 축을 동시에** 올리는 드문 처방

§3.1(공기)의 대응책도 **O 도입**이었고, §3.3(열)의 대응책도 **O 도입**이다.
B1 표에서 대부분의 처방이 한 축을 올리면 다른 축을 깎는데, **O 도핑만 두 칸이 ↑ 다.**
그리고 우리 **LPSOCl** 이 정확히 그 조성이다 — gap 2.2309 eV · ICOHP P–O 강결합 · O 2p 매몰.

**그런데 원고가 안 말하는 대가가 있고, 우리는 그걸 숫자로 갖고 있다** ↓

| O 도핑 | 축 | 근거 |
|---|---|---|
| ↑ | 공기 §3.1 | 원고(전략①) + [Zhu20] 문헌 방향 |
| ↑ | 열 §3.3 | 이 문장 |
| **↓** | **이온전도** | **우리 MD**: modelc **Ea 0.197±0.032** vs **LPSOCl 0.287±0.024** (둘 다 3-seed×3-T, 같은 프로토콜) → **O 도입이 Ea 를 ~0.09 eV 올린다 = 느려진다.** 오차막대 밖 |
| ? | 기계 §3.5 | 강결합·고강성은 원고가 장점으로 든 *"저 E·소성변형"* 과 반대 방향 (미검증) |

> ⚠ 인용 규율 — MD Ea 는 **같은 시드 프로토콜끼리만** 비교한다. 위 두 값은 둘 다 3-seed×3-T 다
> (canonical 표의 modelc 0.224 는 단일 궤적이라 여기 쓰면 안 된다). σ 절대값은 인용하지 않는다.

★ 이게 **리뷰에 없고 우리에게 있는 칸**이다 — 원고는 O 도입을 두 절에서 대응책으로만 들고,
**그 대가(수송 저하)를 정량으로 붙이지 않는다.** B1 의 "축 상충 매트릭스"가 필요한 이유가 여기 있다.

### 🔵 건진 문장 (§3.3 맺음 — outlook)

> "Future research should advance **synergistically across multiple dimensions**, which include
> **electrolyte composition design, interface structure regulation, and overall battery thermal
> management strategies**. This approach aims to systematically improve the **thermal safety
> margins** of sulfide-based ASSBs **while maintaining high ionic conductivity and interface
> stability**."

### 🟢 우리 해석 — ★★ **원고가 trade-off 를 알고 있다는 증거**

*"**while maintaining** high ionic conductivity and interface stability"* —
이 단서가 붙었다는 건 **열 안정성 개선이 σ·계면을 해칠 수 있다는 걸 저자가 알고 있다**는 뜻이다.
그런데 **바로 앞 문단(Q11)은 O 도입을 대가 없이 제시**한다. 즉 **알면서 본문에 안 쓴 것**이다.

★ 그리고 이건 **B1(축 상충 표)의 결정적 근거**가 된다 —
§3.1 맺음(Q6)도 4요건을 *"함께"* 담으라 하고, §3.3 맺음도 3차원을 *"synergistically"* 하라 한다.
**절마다 outlook 에 `while maintaining …` 형태로 단서를 다는데, 그 단서들이 곧 상충 축이다.**
→ 리비전 요구가 자연스러워진다: *"각 절 outlook 이 이미 지목하고 있는 그 상충들을,
소망이 아니라 **표 하나**로 정리해 달라."*

### 🔴 원고가 얼버무린 곳 (§3.3 대응책)

| # | 지점 | 무엇이 문제 | 우리 입장 |
|---|---|---|---|
| **A18** ⭐⭐ **패턴** | *"enhances **overall bond energy**"* | **A12 와 정확히 같은 문제의 재발**이다(InF₃ 의 *"lattice bond energy"*). 원고는 **결합에너지를 논증의 핵심 설명 변수로 반복해서 쓰면서 정의도 측정법도 한 번도 주지 않는다** — 응집에너지인가, 결합해리에너지인가, COHP 적분인가, 아니면 인용 논문의 정성 주장인가 | **개별 문장 지적이 아니라 상위 요구로 올린다**: *"이 리뷰에서 'bond energy' 가 무엇을 뜻하는지 한 번 정의하고, 인용하는 값마다 그 정의로 잰 것인지 밝혀 달라."* 우리는 같은 양을 **ICOHP** 로 잰다 |
| **A19** ⭐ | O 도입의 **대가를 안 쓴다** | O 를 넣으면 **이온전도가 떨어진다**는 것이 이 분야의 상식이고 우리 MD 도 그렇게 나온다(위 표). §3.1·§3.3 이 O 도입을 두 번 대응책으로 들면서 **개선만** 말하면 독자는 무비용 처방으로 읽는다 | O 도입 단락에 **σ 대가**를 한 줄 붙이도록 요구. B1(축 상충 표)의 대표 사례로 쓰기 좋다 |
| **A20** | 코팅 문장의 **두 기전이 뭉개져 있다** | *"buffers oxygen evolution"*(양극 격자산소를 **화학적으로 붙든다**)과 *"inhibits direct contact"*(**물리적 장벽**)는 서로 다른 작용이다. LiNbO₃·Al₂O₃ 의 통상 역할은 **물리 차단 + 자기 화학안정**이지, 방출된 O₂ 를 흡수한다는 주장은 별도 근거가 필요하다 | 두 기전을 갈라 쓰고, "완충" 주장에는 근거(O 흡수 실측·계산)를 붙이도록 |
| **A22** ⭐⭐ | 맺음의 *"while maintaining high ionic conductivity and interface stability"* | **저자가 trade-off 를 알고 있음이 이 단서로 드러난다.** 그런데 본문(Q11)은 O 도입을 대가 없이 제시한다 — **아는데 안 쓴 것**이다. §3.1 맺음(Q6)도 같은 형태다 | **A19 를 강화**하고 **B1(축 상충 표) 요구의 근거**로 쓴다: *"각 절 outlook 이 이미 지목한 상충을 표로 정리해 달라"* |
| **A23** | *"**thermal safety margins**"* 가 정의 없이 등장 | §3.3 본문이 말한 건 **불활성 분위기 분해 온도(400–500 °C)** 인데, safety margin 은 다른 개념이다(작동 온도 ↔ 위험 개시 온도의 여유). **정의하면 정량 지표가 될 좋은 개념**인데 그냥 흘린다 | ★ **A15 의 해법이 여기 있다** — safety margin 을 *(위험 개시 온도 − 최대 작동 온도)* 로 정의하고 그 값으로 비교하면, "불활성 400–500 °C" 를 안전성으로 오독하는 문제가 자동으로 사라진다 |
| **A24** | outlook 이 §3.1 과 **같은 형태의 소망 목록** | §3.1 = 4요건을 *"comprehensively"*, §3.3 = 3차원을 *"synergistically"*. 둘 다 **무엇이 이미 되어 있고 무엇이 빈칸인지** 안 가른다 = **A6 의 반복** | 지적을 절 단위가 아니라 **원고 전반의 outlook 서술 방식**으로 올린다 |
| **A25** | *"overall battery **thermal management** strategies"* | 셀·팩 수준 **공학** 항목이라 이 리뷰의 재료·계면 축과 **스케일이 다르다**. 한 줄로 얹혀 있고 본문에 대응 절이 없다 | 범위 밖 항목을 outlook 에 넣으려면 **재료 관점에서 왜 중요한지** 한 줄 연결을 요구하거나 빼는 편이 깔끔 |
| **A21** | *"**significantly** delaying the onset"* | 얼마나? **개시 온도가 몇 도** 올라가는지·발열량이 얼마나 주는지 숫자가 없다 | DSC 개시온도(°C)·발열량(J/g) 로 쓰도록 — **A15·A17 과 같은 요구**(열 축은 숫자로) |

### 🟢 우리 해석 (A14 관련)

★ **A14 는 B1(축 간 상충)의 또 다른 실례**다. 같은 "공유-이온 혼성 결합"이
§3.1 에서는 **약점의 근원**(낮은 결합에너지·높은 분극률 → 물 공격 취약),
§3.5 에서는 **장점**(저 E·소성변형 → 접촉 유리),
§3.3 에서는 다시 **장점**(열분해 온도 높음)으로 인용된다.
→ 리비전 코멘트로 묶어 쓸 때 *"결합 특성 하나가 절마다 다른 부호로 인용된다"* 로 올리면 무게가 실린다.

> 🔎 **우리 축과의 거리** — 우리는 **열분해 축이 없다**. 갖고 있는 건 `b2o3_phonon_stability.json`·
> `comp2_v3_phonon_uma.json` 의 **0 K 동역학 안정성(포논)** 이고, 이건 *"허수 진동수가 없다"* 이지
> *"몇 도에서 분해되나"* 가 아니다. ⚠ 두 축을 같은 말로 쓰지 않는다.
> §3.3 은 우리가 **비어 있는 축**임을 확인해 주는 절이다(→ B1 표의 열 하나가 통째로 빈칸).


---

## §3.4 Electrochemical Stability — *"진짜 창"이라는 말*

### 🔵 건진 문장

> "First-principles calculations reveal that the **true thermodynamic stability range** of typical
> sulfide SEs is **significantly narrower** than the **apparent electrochemical window** obtained
> experimentally via methods such as cyclic voltammetry (Figure 6c) [114]."

### 🟢 우리 해석 — 이 칸은 **우리가 정면으로 갖고 있다**

grand-potential ESW 는 우리 상시 축이고, 그 **방법 원전이 [Zhu15]**(Zhu/He/Mo 2015 ACS AMI)다.
거기서 나온 값이 **Li₆PS₅Cl 1.71–2.01 V** · Li₃PS₄ 1.71–2.31 · LGPS 1.71–2.14 —
원고 §3.4 가 인용하는 *"LGPS ≈ 1.7–2.1 V"* 와 같은 계보다.

★ 그런데 **[Zhu15] 는 "왜 CV 창이 넓은가"를 이미 설명해 놨다** —
① **kinetic 과전압**(절연 산물·비-Li 확산·기체 핵생성) ② **전자절연 분해산물의 passivation**
(μ_Li = μ̃_Li⁺ + μ̃_e⁻ 에서 절연층이 μ̃_e⁻ 를 떨어뜨려 창 안으로 넣는다).
**즉 이 "불일치"는 미해결 문제가 아니라 원전이 이미 푼 문제다.**

### 🔵 건진 문장 (§3.4 — 계면 3분류)

> "The interfacial film formed after initial decomposition of the electrolyte **significantly
> alters subsequent reaction pathways and rates**, thereby governing the electrochemical behavior.
> Based on the **ion and electron transport characteristics** of the interfacial phase,
> sulfide/electrode interfaces can generally be categorized into **three types** [116]:
> **thermodynamically stable** interfaces, **mixed ion-electron conductive** interfaces, and
> **passivated** interfaces resembling SEI. Among these, **passivated** interfaces exhibiting both
> **high ionic conductivity and low electronic conductivity** are most desirable…"

### 🟢 우리 해석 — 이 3분류의 **2번↔3번을 가르는 장치가 우리에게 있다**

우리 grand-potential ESW 가 내놓는 건 **분해 산물의 조성**이고,
그 산물이 전자절연인지(→ **passivated**) 전자전도인지(→ **MCI**)를 가르는 것이
우리 `db/properties/sei_products.json` 의 절연 판정이다
(insulator ≥4 eV / marginal 2–4 / **conductor <2 eV**).
즉 **원고가 정성으로 세운 분류에 우리는 판정 규칙을 갖고 있다.**

> ⚠ **우리 쪽 약점도 같이 적는다** — 그 판정은 **결정상 gap** 만 쓴다.
> [KimSEI] 는 SEI 안의 Li₃P·LiCl 이 **비정질/고립 클러스터**로 남는다고 보고한다
> (`comparison_vs_ours.md` §H). 비정질 Li₃P 의 gap 을 안 재 봤으므로,
> 우리 절연 판정도 아직 가정 위에 있다.

### 🔵 건진 문장 (§3.4 — 양극 쪽)

> "On the cathode side, the **operational voltage of high-potential layered oxide CAMs far
> exceeds the thermodynamic stability threshold of sulfide SEs**, making interfacial instability
> particularly pronounced."

### 🟢 우리 해석 — ★ 우리가 **이 문장의 전제를 47종 전수로 검증했다**

우리 cascade 의 **계면 반응성 게이트**가 정확히 이 축이고, 47 코팅을 **5상대**
{양극 만충 · 양극 반충 · **SE(LPSCl)** · **Li 금속 음극** · LiNbO₃ 대조} 로 전수 계산했다
(판정 이력 **V1**, `litdb/comparison_vs_ours.md` §G·§H).

★ **결과가 이 문장의 강조점을 뒤집는다** — 축별 탈락 수:

| 상대 | 탈락 |
|---|---|
| 양극 만충 (LiCoO₂) | **2** / 47 |
| 양극 반충 (Li₀.₅CoO₂) | **3** / 47 |
| **SE (Li₆PS₅Cl)** | **29** / 47 |
| **Li 금속 음극** | **35** / 47 |

즉 **코팅이 실제로 마주하는 가장 가혹한 상대는 양극이 아니라 SE 와 Li 음극**이다.
원고는 §3.4·§4 에서 **양극 쪽 불안정만** 앞세우고 §5 에서 음극을 따로 다루는데,
**코팅 재료 선택**의 관점에서는 두 축을 **동시에** 봐야 한다는 것이 우리 데이터의 결론이다
(우리도 이걸 몰라서 M6 게이트를 *"vacuous"* 라 잘못 판정했다가 철회했다 — 판정 이력 V1).

### 🔵 건진 문장 (§3.4 — 산화물 buffer 코팅)

> "To suppress electrolyte oxidation decomposition and prevent the formation of **electronically
> conductive byproducts**, stable **oxide buffer layers** are typically introduced onto the cathode
> particle surface. Such coating layers **establish a chemical potential gradient** between the
> electrolyte and the high-potential cathode, **reducing the driving force for interfacial
> reactions** while providing stable ion transport pathways, thereby significantly enhancing
> cycling stability."

### 🟢 우리 해석 — ★★ 원고의 **"이상적 코팅 조건"에 다섯 번째가 빠졌다**

§4.2.2 가 세우는 이상적 코팅 조건은 넷이다 —
**① 고전압 열역학/화학 안정 ② 충분한 σ_ion ③ 최소 σ_e ④ 기계 유연성** (+두께 제어).
**⛔ 여기에 "SE 와도 반응하지 않을 것"이 없다.**

그런데 코팅은 **양극과 SE 사이에 낀다.** 두 계면이 생기는데 조건은 한쪽(양극)만 본다.
우리 47종 전수(판정 이력 **V1**)가 정확히 그 빈칸을 친다 —
**SE(LPSCl)와의 반응으로 29/47 이 탈락**한다(양극 만충은 2, 반충은 3).
코어 생존자가 11종 → **3종(CaF₂·LiF·MgO)** 으로 줄어든 것도 SE·Li 축이 8종을 새로 죽였기 때문이다.

★ 즉 *"코팅을 넣으면 구동력이 준다"* 가 아니라 **"코팅이 SE 와 또 반응할 수 있다"** 가 실측이고,
그래서 코팅 선택이 어려운 것이다. ⚠ 우리도 이걸 몰라서 M6 게이트를 *"vacuous"* 로
오판했다가 철회했다 — **같은 함정을 리뷰가 조건 목록에서 반복하고 있다.**

### 🔴 원고가 얼버무린 곳

| # | 지점 | 무엇이 문제 | 우리 입장 |
|---|---|---|---|
| **A34** ⭐⭐⭐ | *"establish a **chemical potential gradient** … **reducing the driving force** for interfacial reactions"* | **열역학 구동력은 두 끝 상의 화학퍼텐셜이 정하는 것이라 사이에 층을 넣는다고 줄지 않는다.** 코팅이 실제로 하는 일은 ① **직접 접촉을 끊고** ② **자기가 양쪽 각각에 대해 안정**하고 ③ **전자 경로를 차단**하는 것이다. "구배를 만들어 구동력을 낮춘다"는 표현은 **계단으로 나눈다**는 뜻이라면 이해되지만, 그러면 **각 계단이 여전히 반응할 수 있다**는 점이 따라와야 한다 — 그게 우리 47종 결과다(SE 축 29/47 탈락) | 표현을 **"직접 접촉 차단 + 양쪽에 대한 자기 안정성"** 으로 바꾸고, §4.2.2 의 **이상적 코팅 조건에 "SE 와의 반응성"을 다섯 번째로 추가**하도록 요구. ★ 이게 이번 리뷰에서 **가장 실질적인 개선 제안**이 될 수 있다 |
| **A35** | *"prevent the formation of electronically conductive byproducts"* | 코팅이 막는 것은 **반응 자체**이지 부산물 종류가 아니다. 그리고 **코팅 자신의 분해 산물**이 전도성일 수 있다(§3.4 3분류의 MCI 가 정확히 그 경우) | 코팅의 **자기 분해 산물**도 3분류로 평가해야 한다는 한 줄 |
| **A36** | *"**significantly** enhancing cycling stability"* | 얼마나? 사이클 수·용량유지율 없이 *"significantly"* | **B4 계열**(이번이 A15·A21·A33 에 이어 4번째) — 이제 개별 지적이 아니라 **원고 전반의 정량 부재**로 묶어 쓴다 |
| **A32** ⭐⭐ | **§3.4 안에서 두 문장이 서로를 약화시킨다** | 앞에서는 CV 창이 넓은 이유를 *"분해산물 계면막의 **kinetic 안정화**"* 로 설명한다(Q13 문맥). 그런데 이 문장은 *"**열역학** 문턱을 넘으니 계면 불안정이 두드러진다"* 고 단정한다. **kinetic passivation 이 작동한다면 열역학 문턱 초과가 곧 심각한 불안정은 아니다** — 실제로 LiNbO₃ 코팅 셀은 4.3 V 에서 돈다. 어느 쪽이 언제 지배적인지 조건이 없다 | **A2·A4 의 재발**이자 이번엔 **한 절 안의 자기모순**이다. *"열역학적으로는 초과하지만 실제 열화 정도는 passivation 성패가 가른다"* 처럼 두 축을 한 문장에서 이어 주도록 요구 |
| **A33** | *"far exceeds"* 에 **숫자가 없다** | 층상 산화물 작동전압(~3.0–4.3 V)과 황화물 anodic limit(~2.0–2.3 V)의 차이가 논지의 전부인데 값이 없다. ⚠ 게다가 anodic limit 은 **μ_Li 기준의 계산량**이라 셀 전압과 나란히 놓으려면 기준을 맞춰야 한다 | **B4 계열** + 기준계 명시. 두 숫자만 넣어도 *"far"* 가 검증 가능해진다 |
| **A29** ⭐ | 3분류가 **전기화학 축만** 본다 | 분류 기준이 *"ion and electron transport characteristics"* 뿐이다. 그런데 원고 자신이 §3.5·§5.1.3 에서 **부피변화·균열로 계면이 깨진다**고 쓴다 — **전자절연 산물이라도 균열로 새 표면이 노출되면 passivation 이 무너진다.** 즉 분류에 **기계 축이 빠져 있다** | **B1(축 상충)의 또 다른 실례.** 3분류에 *"기계적으로 유지되는가"* 를 조건으로 덧붙이거나, 최소한 §3.5 와 연결되는 한 줄을 요구 |
| **A30** ⭐ | ①(열역학 안정)과 ③(passivated)를 **무엇으로 구별하나** | 열역학 안정이면 계면상이 안 생기고, passivated 는 생기되 멈춘 것이다. 그런데 **실측에서 둘을 가르는 관측량이 제시되지 않는다** — 임피던스가 안 자라면 둘 다로 보인다. 분류를 세웠으면 **판별 기준**이 있어야 실용적이다 | 각 유형의 **판별 관측량**(계면상 두께 vs 시간·임피던스 성장률·XPS 종 변화 등)을 한 줄씩 붙이도록 요구 |
| **A31** ⭐ | 분류가 **정적**이다 | 원고 §5.1.2 자신이 *"SEI 내부 밴드갭 협소화 → 전자가 계면층 침투"* 를 쓴다. 그렇다면 **passivated → MCI 로 시간에 따라 전이**한다는 뜻이다. 3분류는 **상태**가 아니라 **궤적**으로 서술해야 맞는다 | *"초기 분류"* 임을 명시하거나, **전이 가능성**을 한 줄 추가하도록. §5.1.2 와 §3.4 를 잇는 다리가 된다 |
| **A26** ⭐⭐ | *"**true** thermodynamic stability range"* | **계산 창도 모델링 선택에 의존한다 — "true" 가 아니다.** 최소 세 가지가 값을 바꾼다: ① **준안정 SE 를 E_hull→0 으로 놓는 규약**([Zhu15] 자신의 규약. LPSCl 은 ordered 배열이 83 meV/atom 인데 0 으로 취급) ② **어느 배열을 쓰나**(무질서 50–60 배열 중 최저를 쓸지) ③ **상 집합(phase set)에 무엇을 넣나**. ⚠ ③은 **우리가 직접 겪었다** — 상 집합에서 한 상을 넣고 빼는 것으로 onset 이 달라져 별도 항목으로 처리해야 했다(`litdb/comparison_vs_ours.md` §H "LiS₄ 제외 ESW", `our_dft_baseline.md` §ESW) | *"true"* → *"**계산된(computed under a given phase set / hull convention)**"* 으로 바꾸도록 요구. 계산값을 절대 기준으로 놓으면 독자가 **실험이 틀렸다**고 읽는다 |
| **A27** ⭐ | *"apparent"* 의 이유를 **이 자리에서 안 준다** | 두 값은 **다른 양을 잰다** — 계산은 *열역학 구동력의 개시*, CV 는 *측정 가능한 전류가 흐르는 지점*이다. 원고는 뒤에서 kinetic 안정화를 말하지만, **이 문장 자리에서 "true" 와 "apparent" 를 나란히 놓으면** 독자는 "계산이 옳고 실험이 틀렸다" 로 읽는다 | ⭐ **원전([Zhu15])이 이미 준 설명을 이 자리에 한 줄로** 붙이면 해결된다 — kinetic 과전압 + 분해산물 passivation. 같은 계보 문헌이라 인용 부담도 없다 |
| **A28** | 인용 창 값의 **조건 미기재** | 1.7–2.1 V 가 어느 상 집합·어느 hull 규약·어느 배열에서 나온 값인지 없다. **B4 계열**(임계 수치의 성립 조건) | 창 값에 (a) 방법 (b) hull/배열 규약 (c) 출처 한 줄 |

> 🔎 **우리 기여 가능 칸** — "계산 창이 선택에 의존한다"를 **우리가 실측 사례로 보일 수 있다**
> (상 집합 변경 전후 onset 차이 · 구속 ESW 축). 값은 `db/` 와 `our_dft_baseline.md` 를 가리킨다.


---

## 🧭 내가 따로 잡은 revision 포인트 (B 계열 — 문장이 아니라 **구조**)

> A 계열은 1저자가 준 문장에 붙은 지적이고, 여기는 **digest 전체(113 pp 요약)를 훑어서
> 내가 독립적으로 잡은 것**이다.
> ⚠ 근거는 우리 digest(`litdb/papers/fan2026_…md`)이지 원고 재정독이 아니다 —
> **원고 확인 필요** 표시가 붙은 건 1저자가 실물로 대조해 주면 확정된다.

### B1 ⭐⭐ **축 간 상충(trade-off)을 다루는 절이 없다** — 이 리뷰의 최대 공백

원고는 안정성을 **5축**(공기 §3.1 · 용매 §3.2 · 열 §3.3 · 전기화학 §3.4 · 기계 §3.5)으로 쪼개고,
§6 에서 *"안정성 문제 = 화학×전기화학×열×기계 **결합 효과**"* 라고 맺는다.
**그런데 각 절은 독립적으로 "이렇게 하면 좋아진다"만 말한다.** 한 축을 좋게 하면 다른 축이
나빠지는 관계가 **표로도 문단으로도 정리되어 있지 않다.** 원고 안에서만도 충돌이 보인다:

| 처방 | 좋아지는 축 | 나빠질 수 있는 축 | 원고 근거 |
|---|---|---|---|
| **O 도핑(P–O 강결합)** | 공기 §3.1 | **기계 §3.5** — 강결합·고강성은 원고가 장점으로 든 *"저 E·소성변형 능력"* 과 반대 방향 | §3.1 전략① ↔ §3.5 "저 E(10–30 GPa)·소성변형이 접촉에 유리" |
| **할로겐(Cl/Br) 도핑** | σ ↑ · 음극 §5.2.2(in-situ Li-halide 층) | **공기 §3.1** — 할라이드 농축은 흡습·가수분해 축에 불리 | §5.2.2 ↔ §3.1 |
| **입자 서브미크론화** | 기계 §3.5(응력 균일분산) | **공기 §3.1 · 용매 §3.2** — 비표면적 증가 = 공격 면적 증가 | §3.5 완화책 ↔ §3.1/3.2 반응 표면 |
| **탄소 도전재** | 전자수송 §4.2.1 | **전기화학 §3.4** — 고전위에서 황화물 산화 촉진(원고 자신이 씀) | §4.2.1 ③ |

★ **우리 쪽에도 같은 충돌이 실측으로 있다** — `+B₂O₃` 는 PMF·MD 에서 4계 최선인데
[Zhu20] 기준 가수분해에서는 최악군이다(`open_items` **#11**). 즉 이건 우리만의 사정이 아니라
**이 분야가 공통으로 안고 있는 구조**이고, 리뷰가 그걸 정리해 주면 **가장 인용될 절**이 된다.

**요구**: §6 앞에 **"전략 ↔ 축 상충 매트릭스"** 한 표. 행=완화 전략, 열=5축, 칸=↑/↓/–.
리뷰의 부가가치가 가장 크게 오르는 곳이다.

---

### B2 ⭐⭐ **분자 언어와 고체 언어가 섞여 있다** — A3·A7·A9·A11 을 묶는 상위 진단

개별 지적으로 흩어 놓았지만 **한 뿌리**다. 원고는 주기계(고체 전해질)를 다루면서
**분자화학의 어휘·이론틀을 그대로** 가져온다:

| 어디 | 무엇 | 왜 문제 |
|---|---|---|
| §4.1.3 | *"양극 전기화학퍼텐셜이 황화물 **HOMO** 아래로"* | 고체는 **VBM/CBM** 이다. HOMO/LUMO 는 분자 용어 — 밴드폭·상태밀도가 있는 계에 쓰면 "단일 준위" 오해를 부른다 ⚠ **원고 확인 필요** |
| §3.1 | **HSEH**(ref [80]) 도입 | 원논문은 **전부 이산 분자·기체상**(A5·A11) |
| §3.1 ↔ §3.2 | P⁵⁺ 의 hard/soft 뒤집힘 | HSAB 자체가 분자 배위화학의 정성 틀 (A7) |
| §3.2 | HSAB 짝짓기 방향 오류 | 위와 같은 뿌리 (A9) |
| §3.1 | polarizability ↔ polarity 혼동 | 분자 기술어를 격자 결합에 옮기며 생긴 흔들림 (A3) |

**요구**: 고체를 서술할 때는 **밴드 언어**(VBM/CBM·밴드폭·상태밀도)를 쓰고,
분자 유래 틀(HSAB·HSEH·FMO)을 쓸 때는 **"분자계에서 온 정성 틀"** 임을 한 번 못 박을 것.
그러면 A3·A7·A9·A11 이 한꺼번에 정리된다.

---

### B3 ⭐ **§3.4 는 열역학/속도론을 제대로 가르는데 §3.1 은 안 가른다** — 처방이 원고 안에 있다

§3.4 서술: *"황화물의 전기화학 안정성은 고유 열역학이 아니라 **계면반응이 지배하는 kinetic
안정성**"*, *"실제 셀이 창 밖에서 도는 이유 = 분해산물 계면막의 kinetic 안정화"*.
**이건 두 축을 정확히 가른 좋은 서술이다.** 그런데 §3.1 은 같은 저자가 *"soft base 라 kinetic
barrier 가 낮다"*(A2) · *"thermodynamic **and** kinetic susceptibility"*(A4) 로 뭉갠다.

**요구**: 지적을 "틀렸다"로 하지 말고 — **"§3.4 에서 쓴 서술 방식을 §3.1 에도 적용하라"**.
저자가 이미 할 줄 아는 걸 한 절에서만 안 한 것이므로, 리비전 부담이 작고 수용 가능성이 높다.

---

### B4 **임계 수치들의 성립 조건이 없다** ⚠ 원고 확인 필요

digest 에 잡힌 것만도 — *파괴인성 **0.2–0.4 MPa·m¹ᐟ²*** · *입자 **>~3 µm** 면 탄성에너지 축적
→ 파쇄* · *LGPS 전기화학창 **1.7–2.1 V*** · *면적용량 **>3 mAh/cm²*** .
이런 값은 **측정·계산 조건에 강하게 의존**한다(응력 상태·구속압·시편 조밀도 / 어떤 열역학 틀에서
잡은 창인지 / 어떤 전류밀도 기준인지). 원고가 조건 없이 숫자만 옮기면 독자가 그대로 인용한다.

**요구**: 임계 수치마다 **(a) 측정·계산 방법 (b) 조건 (c) 원 출처** 한 줄. 최소한 표로.
— 이건 우리 자신의 규율(`CLAUDE.md`: 수치는 방법 명시 없이 이식 금지)과 같은 요구다.

---

### B5 **자체 종합 표가 없다** ⚠ 원고 확인 필요

이 원고는 `type: review (문헌 컴파일, **자체 계산/실험 0**)` 이다. 113 pp 를 쓰면서 자체 데이터가
없다면, 리뷰의 부가가치는 **흩어진 문헌 값을 한 좌표에 모아 비교**하는 데서 나와야 한다.
그런데 digest 로 보면 수치가 **절마다 서술 안에 흩어져** 있고, 같은 물성을 여러 논문이 보고한 것을
**나란히 놓은 표**가 잘 안 보인다.

**요구**: 최소 두 표 — (i) **σ_ion 비교표**(조성 · 합성법 · 측정조건 · 값 · 출처),
(ii) **공기/용매 안정성 비교표**(재료 · 노출조건(RH·시간) · 관측량(H₂S 발생량·σ 보존율) · 출처).
지금 본문에 있는 정보로 **재배치만** 해도 되므로 비용 대비 효과가 크다.


---

## 🧾 리뷰 코멘트 초안 (누적 — 리비전 회신용)

> 원고에 실제로 쓸 문장 후보. 위 🔴 표를 한 단계 올려 정리한 것.

1. **(용어) 분극률 ≠ 극성** — §3.1 은 P–S 결합을 한 곳에서는 *stronger polarizability*,
   다른 곳에서는 *highly polar covalent* 로 기술한다. 전기음성도 차를 보면 P–S 는 P–O 보다
   **덜 극성·더 공유결합적이며 더 분극되기 쉽다**. 논지가 기대는 성질은 후자이므로 두 용어를
   구분해 쓸 것을 권한다. *(A3)*
2. **(축 분리) 열역학과 속도론** — §3.1 은 HSAB 의 **열역학적** 선호를 *kinetic barrier* ·
   *kinetic susceptibility* 로 반복해서 이어 붙인다. 실제 가수분해 속도는 표면적·결정성
   (비정질 > 결정질)·조성에 크게 좌우되므로, 두 축을 분리해 서술하고 속도론 주장에는
   그에 맞는 근거를 붙일 것을 권한다. *(A2 · A4)*
3. **(주범 특정) 물 vs 산소** — 원고는 *moisture and oxygen* 을 병렬로 놓지만, 보고된 열화
   실험 대부분이 **RH 를 지배 변수**로 삼는다. H₂O 가수분해와 건조 O₂ 산화의 상대적 기여를
   구분해 주면 뒤의 완화 전략(흡습 차단 vs 산화 차단) 선택 근거가 분명해진다. *(A1)*
4. **(신생 이론의 적용 범위 + 사실오류)** ref [80] 은 **Mulks 단독 저자**이므로 *"Mulks et al."*
   를 *"Mulks"* 로 고쳐 주기 바란다. 내용 면에서, 원논문은 **전부 이산 분자 계산**(가우시안 기저·
   기체상)이며 무기 고체·황화물에 적용된 사례가 **한 건도 없다**. 특히 원고가 HSEH 로
   *"황화물 격자의 전자구조 진화"* 를 설명한다고 쓴 부분은 **원논문이 격자를 다룬 적이 없어
   지지되지 않는다** — 고체에 가장 가까운 사례조차 결정 구조를 분자 단량체로 축소해 계산했다. 이론 자체는 HSAB·Fukui 가
   틀리는 자리 선택성을 실제로 뒤집는 알맹이가 있으므로 인용은 정당하나, §3.1 의 **고체 가수분해
   문맥에 끌어오는 것은 아직 검증되지 않은 유비**다. 그 사실을 한 문장으로 밝히고, 가능하면
   *주기계로 확장하려면 무엇이 필요한지*(원논문이 인용만 한 고체 Fukui 선례 등)를 덧붙일 것을 권한다. *(A5)*
6. **(내부 일관성 — 최우선) P⁵⁺ 는 hard 인가 soft 인가** — §3.2 는 *"P⁵⁺ … belongs to relatively
   soft Lewis acids"* 라 쓰지만, §3.1 의 가수분해 구동력은 **P⁵⁺ 가 hard acid 여야** 성립한다
   (hard–hard 인 P–O 를 선호해야 S 를 내준다). P⁵⁺ 가 soft 라면 soft base 인 S²⁻ 를 유지하는 쪽이
   유리해져 §3.1 의 논증이 무너진다. 두 절 중 하나를 조정하거나, 두 기전이 공존한다면
   **어떤 조건에서 어느 쪽이 지배적인지**를 명시해 주기 바란다. *(A7)*
8. **(HSAB 짝짓기 방향) 용매 공격을 HSAB 로 설명하기 어렵다** — NMP 의 공여 원자(아미드 N·
   카보닐 O)는 **hard base** 에 해당한다. §3.2 서술대로 P⁵⁺ 를 soft 로 두면 soft acid–hard base
   **부조화 짝**이 되어 HSAB 는 오히려 약한 상호작용을 예측한다. 또한 같은 절이 상관 변수로 쓰는
   **donor number 는 SbCl₅ 기준 σ-주개 척도**라 hard 계열 염기도에 가깝다 — DN 상관이 잘 맞는다는
   사실 자체가 hard–hard 전하 제어 기전을 시사한다. HSAB 를 유지하려면 짝짓기 방향을 정리하고,
   아니면 **전하 제어 친핵 치환**으로 기술할 것을 권한다. *(A9)*
7. **(근거) "irreversible"** — §3.2 의 비가역성이 열역학적(ΔG)인지 동역학적(역반응 장벽)인지
   구분하고, 해당 근거(회수 시료의 σ 미복원 등 실험, 또는 반응에너지)를 붙여 줄 것. *(A8)*

9. **(축별 역할) InF₃ 의 In/F 기여** — 인용 논문은 **단일 도펀트 대조군을 갖고 있다**:
   이온전도에서 In 단독(4.8 → 7.0 mS cm⁻¹)과 F 단독(4.8 → 4.3), 수분 흡착에서 In(−0.12 eV)과
   F(−0.15 eV). **그런데 두 축에서 두 원소의 부호가 반대다.** 반면 §3.2 가 인용한 축
   (유기용매 침지 후 σ 유지)에는 단일 도펀트 대조군이 없다(pristine vs co-doped 2 점).
   통합된 *"stabilizing component"* 서술은 이 **반전과 미분리를 모두 지운다** — 어느 축에서 어느
   원소가 무엇을 담당하는지 한 문장이라도 갈라 주면 §5.2.2 의 in-situ 불화물층 논의와도
   정합해진다. *(A13)*
9b. **(인용 정확성 — 인과 방향)** *"enhances lattice bond energy and reduces polarizability"* 는
   인용 논문에 나오지 않는 표현이며, 그 논문에서 *"lower polarization rate"* 는 **F⁻ 치환이
   이온전도도를 낮추는 이유**로 쓰인다. 즉 현재 문장은 원 논문의 인과를 **반대 방향으로** 옮긴 것이다.
   원 논문 근거(H₂O·유기용매 흡착에너지 저하, HSAB soft–soft 결합)로 바꾸거나, *"lattice bond
   energy"* 를 어느 계산량으로 정의하는지 밝혀 주기 바란다. *(A12)*
10. **(용어 축의 일관성 — A3 보강)** §3.2 의 대응책 문장이 *"**reduces polarizability**"* 라 쓴 것은
   §3.1 의 진단 *"stronger polarizability"* 와 정확히 같은 축이다. 그렇다면 §3.1 의
   *"highly **polar** covalent"* 는 그 축에서 벗어난 표현이므로, **polarizability 로 통일**하면
   진단–대응이 하나의 물성으로 이어진다. *(A3·A12)*

11. **(구조화학 — 상위 지적) "continuous network" 서술** — §3.3 은 LGPS·LPSCl·Li₇P₃S₁₁ 의
   열안정을 *"continuous covalent-ionic hybrid bond network"* 로 설명하지만, 세 물질의 음이온
   연결도는 서로 다르다 — LGPS 사슬, Li₇P₃S₁₁ 은 P₂S₇⁴⁻ 이합체 + PS₄³⁻, **LPSCl 은 고립 PS₄³⁻ +
   free S²⁻ + Cl⁻ 로 연결망이 아니다**. 원고 자신이 §3.1·§3.2 에서 *"PS₄³⁻ structural units"* 라
   부른 그것이다. 연결도를 갈라 서술하고 열안정 기여를 그와 연결지어 주기 바란다. *(A14)*
12. **(조건과 결론의 정합) 열 안정성 비교 축** — *"under inert atmospheres"* 에서 얻은 400–500 °C 를
   근거로 *"카보네이트 액체 전해질보다 우수"* 라 맺는 것은 축이 어긋난다. 액체의 위험은 분해온도가
   아니라 **인화점·증기압·발열 폭주**이며, 고체계의 실제 열 위험도 SE 단독이 아니라 **충전 양극의
   O₂ 방출·Li 금속과의 발열 반응**이다. 비교하려면 **DSC 발열 개시온도·발열량**, 그리고 **양극/Li
   공존 조건**의 값을 쓰고, 아니면 *"불활성 분위기 기준"* 을 결론 문장에도 달아 주기 바란다. *(A15·A16)*

13. **(핵심 변수의 정의 — 상위 요구) "bond energy" 를 한 번 정의해 주기 바란다** — 이 리뷰는
   결합에너지를 반복해서 핵심 설명 변수로 쓴다(§3.1 *"lower bond energy"* · §3.2 InF₃
   *"enhances lattice bond energy"* · §3.3 oxysulfide *"enhances overall bond energy"*).
   그런데 그것이 응집에너지인지, 결합해리에너지인지, 결합차수/COHP 적분 같은 계산량인지,
   또는 인용 논문의 정성 주장인지가 한 번도 명시되지 않는다. **한 곳에서 정의하고 인용값마다
   그 정의로 잰 것인지 밝히면** 독자가 자기 계산축과 맞출 수 있다. *(A12·A18)*
14. **(처방의 대가) O 도입의 수송 손실** — §3.1 과 §3.3 이 모두 **산소 도입(oxysulfide)** 을
   대응책으로 들지만, 이온전도 저하라는 대가가 어느 쪽에도 적히지 않는다. 개선과 대가를 같이
   써야 독자가 설계 선택을 할 수 있다. B1 의 축 상충 표에 넣기 좋은 대표 사례다. *(A19)*

15. **(축 상충 — B1 의 근거) 각 절 outlook 의 단서를 표로** — §3.3 맺음은 *"…while maintaining
   high ionic conductivity and interface stability"* 라 쓰고, §3.1 맺음도 4요건을 *"comprehensively"*
   담으라 한다. **즉 원고는 축 사이의 상충을 이미 인지하고 있다.** 그런데 본문 각 절은 처방의
   개선만 서술한다(예: O 도입이 §3.1·§3.3 두 곳에서 대가 없이 제시된다). **각 절이 지목하는
   상충을 한 표(행=완화 전략, 열=5축, 칸=↑/↓/–)로 정리**해 주시면 이 리뷰의 활용도가 크게 오른다.
   *(A19·A22 · B1)*
16. **(용어 정의) "thermal safety margin"** — §3.3 맺음이 이 표현을 쓰지만 정의가 없다.
   *(위험 개시 온도 − 최대 작동 온도)* 처럼 정의하면 **정량 비교 지표**가 되고, 동시에 §3.3 본문의
   "불활성 분위기 400–500 °C" 가 안전성으로 오독되는 문제(코멘트 12)도 함께 해소된다. *(A23·A15)*

17. **("true" 라는 표현 · 그리고 불일치의 설명)** — §3.4 는 계산 창을 *"true thermodynamic
   stability range"*, 실험 창을 *"apparent"* 로 대비한다. 그러나 계산 창도 **준안정 상을
   E_hull→0 으로 놓는 규약 · 무질서 배열의 선택 · 상 집합 구성**에 따라 달라지므로 *"true"* 보다
   *"계산된(주어진 상 집합·hull 규약 하의)"* 이 정확하다. 또한 두 창이 다른 이유는 이미
   같은 계보의 선행 연구가 **kinetic 과전압 + 분해산물 passivation** 으로 설명했으므로, 그 한 줄을
   이 자리에 붙이면 "실험이 틀렸다" 는 오독을 막을 수 있다. *(A26·A27)*

18. **(3분류의 보완) 기계 축 · 판별 기준 · 시간 전이** — §3.4 의 계면 3분류(열역학 안정 /
   혼성전도 / passivated)는 **이온·전자 수송 특성만**을 기준으로 삼는다. 세 가지를 덧붙이면
   훨씬 실용적이 된다 — (i) 원고 §3.5·§5.1.3 이 다루는 **균열·부피변화**로 passivation 이 무너지는
   경로(**기계 축**), (ii) ①과 ③을 **실측에서 가르는 관측량**(계면상 두께 vs 시간·임피던스 성장률 등),
   (iii) §5.1.2 가 서술하는 **SEI 밴드갭 협소화 → passivated에서 혼성전도로의 전이**. 특히 (iii)은
   분류를 **상태가 아니라 궤적**으로 만들어 §3.4 와 §5.1.2 를 잇는다. *(A29·A30·A31)*

19. **(절 내부 정합) 열역학 초과 vs kinetic passivation** — §3.4 는 한편으로 CV 창이 넓은 이유를
   **분해산물의 kinetic 안정화**로 설명하고, 다른 한편으로 양극 쪽에서 *"열역학 안정 문턱을 크게
   초과하므로 계면 불안정이 두드러진다"* 고 단정한다. 두 서술은 서로를 약화시킨다 — passivation 이
   작동하면 문턱 초과가 곧 심한 열화는 아니기 때문이다(코팅 셀이 4.3 V 에서 작동하는 것이 그 예).
   **어느 조건에서 어느 쪽이 지배적인지**를 한 문장으로 이어 주기 바란다. 그리고 *"far exceeds"* 에
   **두 전압 값**(CAM 작동전압 · 황화물 anodic limit)을 넣으면 독자가 크기를 가늠할 수 있다.
   *(A32·A33)*

20. **(가장 실질적인 제안) 이상적 코팅 조건에 "SE 와의 반응성"을 추가** — §4.2.2 의 네 조건
   (고전압 안정 · σ_ion · 최소 σ_e · 기계 유연성)은 **코팅이 마주하는 두 상대 중 양극만** 본다.
   코팅은 양극과 SE **사이에** 끼므로 계면이 둘 생긴다. 또한 §3.4 의 *"chemical potential gradient
   를 만들어 구동력을 줄인다"* 는 표현은, 열역학 구동력이 두 끝 상으로 정해진다는 점에서
   **"직접 접촉 차단 + 양쪽에 대한 자기 안정성"** 으로 쓰는 편이 정확하다. 실제 스크리닝에서는
   **SE 와의 반응이 양극과의 반응보다 훨씬 가혹한 축**으로 나타난다. 다섯 번째 조건을 추가하면
   §4.2.2 의 재료 선택 논의가 크게 단단해진다. *(A34·A35)*
21. **(정량 부재 — 묶음)** *"significantly"* · *"far exceeds"* · *"400–500 °C"* 등 핵심 주장에
   **조건·수치가 붙지 않는 사례가 반복**된다(A15·A21·A33·A36). 최소한 **비교를 담은 주장**에는
   숫자와 조건을 붙여 주기 바란다. *(B4)*

5. **(outlook 의 구체화)** §3.1 맺음의 "미래 모델 4요건"(결합에너지 강화 · 다중스케일 계면
   상전이 kinetics · 전자–홀 결합 · 고체–기체 반응 열역학) 중 **전자–홀 결합은 ref [80],
   고체–기체 열역학은 ref [84] 가 이미 부분적으로 다룬다**. 각 요건에 *현재 도달점*과
   *남은 간극*을 한 줄씩 붙이면 outlook 이 소망 목록에서 로드맵으로 바뀐다. *(A6)*


---

## 📌 인용문 대장 (누적)

| # | 절 | 원문(축약) | 쓸 때 주의 | 우리 표현 |
|---|---|---|---|---|
| Q1 | §3.1 | P–S/M–S 는 M–O 대비 **결합에너지 낮고 분극률 큼** → H₂O/O₂ 공격에 취약 [78] | 그대로 인용 가능 | — |
| Q2 | §3.1 | S²⁻ 는 전형적 **soft base**, 양성자·극성분자에 강한 친화성 | ⚠ 원고는 이어서 *kinetic barrier* 로 연결 — **그 연결은 빼고** 인용 | "S²⁻ 의 soft-base 특성이 가수분해를 **열역학적으로** 유리하게 만든다" |
| Q3 | §3.1 | 국소 구조 재배열·계면 상전이 → **사이클 중 계면 수송 물성의 지속적 열화** | 그대로 인용 가능 · 다만 "연속"의 기전(상 성장 vs 응력 파괴)은 원고가 안 가름 | "대기 안정성은 보관 문제가 아니라 **수명 문제**다" |
| Q4 | §3.1 | 낮은 격자에너지 · 불충분한 전하밀도 · 강한 극성 공유결합 = 가수분해·산화 취약성의 근본 원인 | ⚠ **A3**(polar↔polarizable 혼동) · **A4**(열역학/속도론 뭉갬) 둘 다 걸림 — **그대로 인용 금지** | "격자에너지 · 전하밀도 · 결합의 공유성/분극률이 황화물의 취약성을 **열역학적으로** 규정한다" |
| Q5 | §3.1 | **HSEH**(Mulks 2024)가 HSAB 를 **다전자계**로 확장 [80] | ⚠ 신생 이론 — "확장한 틀이 제안돼 있다" 수준으로만 | "HSAB 를 다전자·전자/홀 거동으로 확장한 HSEH 가 제안돼 있다(Mulks 2024)" |
| Q16 | §3.4 | 산화물 buffer 코팅이 **화학퍼텐셜 구배**를 만들어 계면 반응 **구동력을 줄이고** 이온 경로를 제공 → 사이클 안정성 향상 | ⛔ **인용 주의** — 구동력은 두 끝 상이 정하므로 층을 넣어 줄지 않는다(A34) | "산화물 buffer 코팅이 **직접 접촉을 차단**하고 이온 경로를 유지해 계면 반응을 억제한다" |
| Q15 | §3.4 | 층상 산화물 CAM 작동전압이 황화물 **열역학 안정 문턱을 크게 초과** → 양극 계면 불안정이 두드러짐 | ⚠ 숫자 없음(A33) · 같은 절의 kinetic 안정화 서술과 **충돌**(A32) | "층상 산화물의 작동전압은 황화물의 계산 anodic limit 을 크게 웃돈다 — **다만 실제 열화 정도는 passivation 성패가 가른다**" |
| Q14 | §3.4 | 초기 분해로 생긴 계면막이 이후 경로·속도를 지배 · 계면 **3분류**(열역학 안정 / 혼성전도 MCI / **passivated**) — 고 σ_ion·저 σ_e 인 passivated 가 목표 [116] | 그대로 인용 가능 · ⚠ 기계 축 부재(A29) · 판별 기준 부재(A30) · 정적 분류(A31) | "계면상은 이온·전자 수송 특성에 따라 세 유형으로 나뉘며, **고 이온전도·저 전자전도의 passivation 층**이 목표다" |
| Q13 | §3.4 | 제일원리 계산의 **열역학 창**이 CV **겉보기 창**보다 크게 좁다 (Fig 6c) [114] | ⚠ *"true"* 는 과한 표현(A26) · 불일치 이유를 이 자리에서 안 준다(A27) | "제일원리 **열역학** 창은 CV 겉보기 창보다 좁다 — 두 값은 서로 다른 양을 재며, 차이는 kinetic 과전압과 분해산물 passivation 으로 설명된다" |
| Q12 | §3.3 | 향후 연구는 **전해질 조성 설계 · 계면 구조 조절 · 셀 열관리**를 동시에 진전시켜 **thermal safety margin** 을 높이되 **σ·계면 안정성은 유지**해야 | ★ 인용 가치 높음 — **원고가 trade-off 를 인지한다는 증거**로 쓸 수 있다 | "열 안전 여유를 넓히되 **이온전도와 계면 안정성을 유지**해야 한다 — 저자들도 이 상충을 지목한다" |
| Q11 | §3.3 | **O 도입(oxysulfide)** → P–O 비율↑·결합에너지↑ → 고온 분해 경향↓ · **산화물 코팅**(LiNbO₃·Al₂O₃)이 O 방출 완충 + 직접 접촉 차단 → 계면 발열 개시 지연 | ⚠ 'bond energy' 정의 없음(A18) · **σ 대가 미기재**(A19) · 코팅의 두 기전 뭉갬(A20) | "산소 도입으로 P–O 비율을 높이면 고온 분해가 늦춰지는 것으로 보고된다 — **단 이온전도 저하를 동반한다**" |
| Q10 | §3.3 | 불활성 분위기에서 LGPS·LPSCl·Li₇P₃S₁₁ 이 **400–500 °C** 까지 구조 유지; 원인 = 연속 공유–이온 혼성 결합망 + 낮은 휘발 성분 | ⛔ **그대로 인용 금지** — *continuous network* 가 LPSCl 에 안 맞고(A14), 액체와의 비교 축이 어긋난다(A15) | "**불활성 분위기 기준으로** 결정성 황화물 SE 는 400–500 °C 까지 상 구조를 유지한다고 보고된다" — 액체 비교·연결망 설명 **없이** |
| Q9 | §3.2 | **InF₃** 첨가 → 격자 결합에너지↑ · **분극률↓** → 유기용매 침지 후에도 σ 유지 (Fig 4c) | ⚠ 측정법 없음(A12) · In/F 기여 미분리(A13). 다만 **"분극률"** 축은 §3.1 과 일관 | "강결합 성분(InF₃ 등) 도입이 **분극률을 낮춰** 용매 침지 후 σ 유지에 기여한다고 보고된다" |
| Q8 | §3.2 | HSAB 근거로 **P⁵⁺ = 비교적 soft Lewis acid**, 고립전자쌍 극성용매 = **strong Lewis base** → 친핵 공격 → P–S 절단·저전도 구조단위 (Fig 4b) | ⛔ **인용 금지** — §3.1 과 P⁵⁺ 분류가 모순(A7)이고 HSAB 짝짓기 방향도 어긋난다(A9) | "고립전자쌍 주개(고-DN 용매)가 P 를 친핵 공격해 P–S 를 끊는다" — **HSAB 라벨 없이** |
| Q7 | §3.2 | **NMP**(고유전율·강용매화)가 PS₄³⁻·P₂S₇⁴⁻ 와 **비가역 반응** → P–S 절단·구조단위 재배열 | ⚠ *irreversibly* 의 근거(열역학/동역학)를 원고가 안 단다 — 인용 시 "비가역적으로 보고된다" 정도로 | "고립전자쌍을 가진 고-DN 용매(NMP 등)가 PS₄ 를 친핵 공격해 P–S 를 끊는다" |
| Q6 | §3.1 | 미래 모델 요건 **4가지** — 결합에너지 강화 · 다중스케일 계면 상전이 kinetics · 전자–홀 결합 · 고체–기체 반응 열역학 | 그대로 인용 가능 · ★ **우리 좌표를 찍는 자**로 쓰기 좋다 | "공기안정성 정량 예측 모델은 결합에너지 · 계면 상전이 동역학 · 전자–홀 결합 · 고체–기체 반응 열역학을 **함께** 담아야 한다" |

---

## 🗂 다음에 채울 자리 (1저자가 문장 주는 대로)

- [x] §3.2 Solvent Compatibility — Q7 (A7·A8)
- [x] §3.3 Thermal — Q10 (A14·A15·A16·A17)
- [x] §3.4 Electrochemical (ESW) — Q13 (A26·A27·A28)
- [ ] §3.5 Mechanical
- [ ] §4 양극 계면 · §5 음극 계면
- [ ] §6 Summary & Future

> **작성 규칙** — 문장을 받으면 ① 🔵 원문을 그대로 박고 ② 🟢 우리 해석을 붙이고
> ③ 🔴 얼버무린 곳이 있으면 표에 한 줄 추가하고 ④ 인용문 대장에 등록한다.
> 우리 db 수치를 이 문서에 **절대값으로 옮기지 않는다** — 접점은 "같은 축"까지만 쓰고
> 숫자는 `db/properties/` 와 `litdb/our_dft_baseline.md` 를 가리킨다.
