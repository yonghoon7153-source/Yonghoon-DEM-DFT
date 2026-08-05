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

---

## 📌 인용문 대장 (누적)

| # | 절 | 원문(축약) | 쓸 때 주의 | 우리 표현 |
|---|---|---|---|---|
| Q1 | §3.1 | P–S/M–S 는 M–O 대비 **결합에너지 낮고 분극률 큼** → H₂O/O₂ 공격에 취약 [78] | 그대로 인용 가능 | — |
| Q2 | §3.1 | S²⁻ 는 전형적 **soft base**, 양성자·극성분자에 강한 친화성 | ⚠ 원고는 이어서 *kinetic barrier* 로 연결 — **그 연결은 빼고** 인용 | "S²⁻ 의 soft-base 특성이 가수분해를 **열역학적으로** 유리하게 만든다" |

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
