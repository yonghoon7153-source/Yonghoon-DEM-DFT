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
| **A5** | Q5 의 HSEH | **2024년 신생 이론**을 기성 틀처럼 인용한다. 확인할 것 — ① HSEH 가 **황화물 SE 에 실제로 적용된 선례**가 있나, 아니면 유비로 끌어온 것인가 ② 뒤 본문에서 HSEH 로 **무엇을 설명·예측**하나, 아니면 이름만 얹고 끝나나 | 후자면 **name-drop 지적**. 남기려면 "무엇을 새로 설명하는지" 한 문장을 요구 |

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
4. **(신생 이론 위치)** HSEH [80] 가 이 리뷰에서 **무엇을 새로 설명하는지** 한 문장으로
   밝혀 줄 것. 황화물 SE 에 적용된 선례가 없다면 "유비로 도입"임을 명시하는 편이 안전하다. *(A5)*
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
| Q6 | §3.1 | 미래 모델 요건 **4가지** — 결합에너지 강화 · 다중스케일 계면 상전이 kinetics · 전자–홀 결합 · 고체–기체 반응 열역학 | 그대로 인용 가능 · ★ **우리 좌표를 찍는 자**로 쓰기 좋다 | "공기안정성 정량 예측 모델은 결합에너지 · 계면 상전이 동역학 · 전자–홀 결합 · 고체–기체 반응 열역학을 **함께** 담아야 한다" |

---

## 🗂 다음에 채울 자리 (1저자가 문장 주는 대로)

- [ ] §3.2 Solvent Compatibility
- [ ] §3.3 Thermal
- [ ] §3.4 Electrochemical (ESW)
- [ ] §3.5 Mechanical
- [ ] §4 양극 계면 · §5 음극 계면
- [ ] §6 Summary & Future

> **작성 규칙** — 문장을 받으면 ① 🔵 원문을 그대로 박고 ② 🟢 우리 해석을 붙이고
> ③ 🔴 얼버무린 곳이 있으면 표에 한 줄 추가하고 ④ 인용문 대장에 등록한다.
> 우리 db 수치를 이 문서에 **절대값으로 옮기지 않는다** — 접점은 "같은 축"까지만 쓰고
> 숫자는 `db/properties/` 와 `litdb/our_dft_baseline.md` 를 가리킨다.
