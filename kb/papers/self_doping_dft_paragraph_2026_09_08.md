---
title: "원고 자가도핑 DFT 문단 — 스핀 하나로 좁힌 5문단 (2·3·6 계열)"
date: 2026-09-08
updated: 2026-09-15
tags: [manuscript, dft, sdcp, self-doping, spin, polaron]
status: 1저자 승인 — 삽입 위치 대기
kind: manuscript-draft
system: sdcp
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-08
verifiedBy: self
explored: false
authoredBy: agent
claimType: empirical
evidenceScope: multi-source-primary
---

# 원고 자가도핑 DFT 문단

## 무엇이 바뀌었나

**종전 초안의 Second·Third 를 뺐다** (1저자 결정 2026-09-08 — 문헌과 개념이 안 맞음).

- ⛔ 뺀 것 ②: 산화가 Li 자리 지형을 평탄화한다 (중성 1.27 eV → 산화 0.43 eV)
- ⛔ 뺀 것 ③: DPE 14.17 eV / LCA −6.76 eV → 사슬은 –SO₃Li 로 작동한다

남은 하나(**산화 상태에서 스핀이 어디 있나**)를 FT-IR 과 전도도 사이의 **다리**로 세운다:

> FT-IR (상태가 존재하는가) → **DFT (그 상태의 캐리어가 무엇·어디인가)** → 전도도 측정 (수송)

세 계열 **n = 2·3·6 을 모두 싣는다** (1저자 확정 2026-09-08). n=6 만으로도 핵심 주장은 서지만,
기체상 올리고머로 폴리머를 말하려면 **사슬 길이 의존성**이 유일한 논거이고, 교차(SO₃ 우세 →
백본 우세)가 있어야 "공액 길이가 만드는 폴라론" 이라는 메커니즘이 선다.
⚠ n=1(모노머)은 **싣지 않는다** — 에테르 산소가 없어 분모가 다르고, 35.0 → 32.6 으로 내려가
백본 단조 서술이 깨진다.

## 본문 (미국식 영어 · 2문단)

Density functional theory was used to identify what carries the charge in the oxidized,
deprotonated chain. A hydrogen atom was removed from the sulfonic acid group of gas-phase oligomers
of two, three, and six repeat units (Figure S3). The resulting doublets were optimized at the r²SCAN-3c level
(Supplementary Note 2). The oxidized state is imposed by this construction; that it is realized in
the material follows from the infrared spectra above. Löwdin spin populations show the unpaired spin
migrating from the sulfonate onto the conjugated backbone as the chain grows. The backbone share
rises from one-third in the dimer to 79.7% at six repeat units, while the sulfonate share falls to
7.7% (Figure S4); the spin therefore resides on the conjugated backbone rather than on the
oxidation site itself.

The carrier is therefore a backbone polaron delocalized over several repeat units, with the
deprotonated sulfonate as its fixed counter-anion. This is the molecular signature of self-doping:
the chain supplies both the carrier and the charge that compensates it. Because the backbone share
has not saturated at six units, the polymer is expected to be at least this delocalized. These
gas-phase models identify the carrier but not its mobility, which also requires the doping level and
inter-chain transfer. That transport was measured directly: the polymer shows a four-point-probe
electronic conductivity of 250 mS cm⁻¹ (Section X).

### 개정 이력 (2026-09-08)

- **5문단 → 2문단.** 1저자 지적: *"논문스럽게 써야지 하나하나 다 넣으려고 하지 마."*
  방어 문구를 문장마다 박으니 논문이 아니라 체크리스트가 됐다. 한계는 한 문장으로 접고
  나머지는 Methods/SI 로 내린다.
- **SI·Methods 로 내린 것 4:** 네 그룹 합 100.0% · "어느 고리도 1/4 미만" · 스핀 이성질체
  탐색 없음 · 스핀밀도 ≠ 홀 전하밀도. 앞의 둘은 표가 보여주고 뒤의 둘은 Methods 한 줄이면 된다.
- **본문에 남긴 방어 3:** `imposed by this construction`(자발성 주장 차단) ·
  `rather than localized at the oxidation site`(ring4 국재 오독 차단) ·
  마지막 두 문장(전도도 주장 차단).
- **"Density functional theory" 를 되살렸다.** 압축 판에서 빠져 `r²SCAN-3c` 만 남았는데,
  앞이 FT-IR 절이면 방법이 바뀌는 지점이라 명시해야 한다.
- **문장 길이 9–24 단어로 균질화.** 한 문장에 몰아넣지 않는다.

## 본문에 남긴 방어선

| 구절 | 막는 것 |
|---|---|
| `The oxidized state is imposed by this construction` | DFT 로 **자발성**을 주장한다는 오독. H 를 손으로 뗀 계산이다 |
| `follows from the infrared spectra above` | 자발성은 FT-IR 몫 — 역할 분담을 한 절로 |
| `Counted over ring atoms only` → **Figure S4 캡션으로** | 7월 n=1–3 과 같은 분할. strict/extended 를 섞지 않는다 |
| `rather than localized at the oxidation site` | 세 고리 중 하나에 "국재" 로 읽는 것. **자리는 고리 4번**(1-기준 · 2026-09-09 번호 정정)이고 그 고리가 셋 중 **가장 작다**(15.9 < 20.0 < 23.3) — 산화 자리가 최소 지분이라 이 구절이 데이터로 받쳐진다. ⚠ 어느 고리가 최대인지는 **쓰지 않는다**(아래 참조) |
| `expected to be at least this delocalized` | 외삽 한계 — "폴리머에서 100%" 는 못 쓴다 |
| `identify the carrier but not its mobility` | 전도도를 계산으로 주장하는 것 차단 |
| `That transport was measured directly` | 계산이 못 하는 것을 **측정이 답한다** — 회피가 아니라 역할 분담임을 보인다 |

⚠ `Counted over ring atoms only` 는 본문에서 뺐다 — **Figure S4 캡션에 반드시 넣는다.**
빠지면 7월 값과 다른 분할(strict 79.5 · extended 91.6)이 같은 그림에 섞여 읽힌다.

## 캡션·SI 확정 (2026-09-08 · 공저자 형식 지적 반영)

> **지적:** 다른 캡션은 다 compact 하다. S3·S4 캡션을 한두 줄로 줄이고 나머지는 Note 2 로 몰아라.
> Note 1 이 소제목 없는 산문 한 덩어리이므로 Note 2 도 그 형식에 맞춘다.

**Figure S3** — *Optimized structures of the oxidized (deprotonated) oligomers of two, three
(oxidized at a terminal and at the internal ring), and six repeat units. The sulfonate from which
the hydrogen was removed is indicated.*

**Figure S4** — *Löwdin spin populations of the oxidized oligomers: (a) partition into sulfonate,
aryl rings, ether oxygens, and hydrogens against chain length; (b) spin on each thiophene ring at
six repeat units.*

캡션 → Note 2 로 옮긴 것 4: **분할 정의(ring atoms only)** · 참고 분할 79.5/91.6 · ring3 도핑
자리 · 기체상·단일 SCF·스핀밀도 한계. 캡션에는 "무엇을 보여주는 그림인가" 만 남는다.

⚠ 그림이 지켜야 할 것 둘 (캡션이 설명하지 않으므로):
1. **상자를 끈다** (VESTA `Objects → Unit cell` 해제) — 캡션에 상자 설명이 없다.
2. **산화 자리를 실제로 표시한다** — S3 캡션 두 번째 문장이 그걸 약속한다.
   n=2 A-ring · n=3 말단/내부 · **n=6 ring3 = 고리 4번** (탈양성자 SO₃ 는 O–H 가 없는 유일한 sulfonate).

## Methods 편입 + Note 2 (2026-09-08 · 외부 독자 감사 반영)

> **지적 (1저자):** ① Note 2 내용을 Methods 에 제대로 편입해라. ② 우리끼리 쓰는 말로
> 쓰지 않았는지, 처음 보는 독자가 이해되는지 확인해라.

### 외부 독자 감사 — 고친 3건

| 원문 | 문제 | 고침 |
|---|---|---|
| `determined from the optimized structure rather than from the run label` | **`run label` 은 우리 폴더 이름**이다. 독자는 그게 뭔지도, 왜 의심했는지도 모른다. 우리가 우리(와 Codex)에게 하는 해명이라 논문에 있을 자리가 아니다. 정작 독자에게 필요한 **고리 번호 기준**은 빠져 있었다 | `Rings are numbered from one chain end as in Figure S4` 로 교체 |
| `spin isomers` | **용어 오류.** spin isomer 는 통상 ortho/para 수소류를 가리킨다. 우리가 뜻한 것은 스핀이 다른 자리에 국재된 다른 SCF 해다 | `alternative spin-localized solutions` |
| `with the main text quoting the ring-atoms-only value throughout` | 원고 내부 사무처럼 읽힌다 | 정의를 먼저 말하고 값을 붙이는 순서로 재배열 |

### Methods — **분자 문단을 슬랩 앞에** (1저자 지적 2026-09-08)

> 분자 계산이 결합제 **자체**를 다루고 슬랩은 그것이 **표면에 붙었을 때**를 다룬다. 논리 순서로도
> 결과 제시 순서로도 분자가 먼저다. 순서를 바꾸면 슬랩 문단의 **자가도핑 정의 중복이 사라진다.**

**문단 1 (분자 · 신규 · 8문장 10–22단어)**

> **DFT calculations:** Molecular models of the SDCP binder were treated first. Oligomers of two,
> three, and six repeat units were built from the sulfonate-functionalized EDOT unit (C₁₁H₁₆O₆S₂).
> Each was oxidized by removing one hydrogen atom from a sulfonate group. This leaves a
> charge-neutral open-shell species (multiplicity 2) in which the oxidized backbone is compensated by
> the tethered sulfonate. For three repeat units, oxidation at a terminal and at an internal ring was
> treated separately. The molecules were optimized in the gas phase with ORCA 6.1.1 at the r²SCAN-3c
> level. Default convergence thresholds were used, with no solvent model or symmetry constraint. The
> unpaired-electron distribution was analyzed by Löwdin spin populations (Supplementary Note 2).

**문단 2 (슬랩 · 기존) — 두 문장만 바뀐다. 나머지 다섯 문장과 모든 수치는 원문 그대로.**

| | 원문 | 바꾼 뒤 | 왜 |
|---|---|---|---|
| 첫 문장 | `Spin-polarized DFT calculations were performed with Quantum ESPRESSO…` | `Adsorption at the cathode surface was **then** treated with **periodic**, spin-polarized DFT in Quantum ESPRESSO…` | 앞에 분자 문단이 생겨 "DFT 계산을 수행했다" 가 두 번 나온다. `then` 이 순서를, `periodic` 이 기체상 분자와의 대비를 만든다 |
| 넷째 문장 | `SDCP was represented by its … repeat unit (C₁₁H₁₆O₆S₂; the self-doped form C₁₁H₁₅O₆S₂ was obtained by removing a hydrogen atom, leaving a charge-neutral unit with an oxidized backbone compensated by the tethered sulfonate group) and PTFE by …` | `Here SDCP was represented by **a single repeat unit** in its neutral (C₁₁H₁₆O₆S₂) and self-doped (C₁₁H₁₅O₆S₂) forms, and PTFE by …` | 괄호 안 자가도핑 설명이 문단 1 과 **중복**이다. `a single repeat unit` 은 올리고머(2·3·6)와 모델 크기가 다름을 밝힌다 |

✅ 보존 확인: 60/480 Ry · 0.05 eV · 1×10⁻⁶ Ry · 1×4 4층 192원자 18.27×11.51 Å · >15 Å ·
Γ-centered 2×3×1 · 7자리 48배향 · 1×10⁻³ Ry bohr⁻¹ · 20→24 Å · 식 (1)과 `where` 절 — 전부 무수정.

⚠ `E_binder`("the isolated binder")가 ORCA 기체상 분자로 오해될 여지가 생기지만, 바로 앞 문장이
*"Gas-phase references were relaxed at the Γ point in the same cell"* 로 QE 안에서 정의하므로 성립한다.

### ⛔ P0 — 흡착 문단·Table S1 에서 **자가도핑형을 뺀다** (1저자 발견 2026-09-08)

1저자 지적: *"우리 adsorption 할 때는 자가도핑 뺐잖아."* 맞다. db 가 명시적이다.

- `sdcp_doped_closed_2026_08_28.json` (**상태 active**) — 닫는 범위 = *"sdcp_doped(자가도핑 단량체,
  C₁₁H₁₅O₆S₂ doublet)의 **표면 흡착 수치 전부** — E_ads·자리선호·carrier 상태 판정"*.
  금지 서술에 *"doped E_ads 수치 일체"* · *"doped 가 중성보다 강하게/약하게 붙는다 — 비교 자체가
  미정의"* 가 있다.
- `sdcp_neutral_closed_2026_08_28.json` — 닫는 범위 = *"sdcp_neutral(C₁₁H₁₆O₆S₂) 의 LiNiO₂(104)
  흡착"*, ⛔ *"doped 는 이 문서의 범위가 아니다"*.

⇒ **흡착 계산은 중성 하나뿐이다.** 그런데 원고 두 곳이 둘 다 한 것처럼 읽혔다 —
그리고 이는 내 수정본만이 아니라 **원문부터** 그랬다 (원문의 괄호 설명이 Adsorbate 맥락에 있어
두 형태를 다 흡착시킨 것으로 읽힌다). 마감된 결과를 암묵적으로 주장하는 셈이라 P0 다.

| 위치 | 고침 |
|---|---|
| Methods 슬랩 문단 | `…in its neutral (C₁₁H₁₆O₆S₂) and self-doped (C₁₁H₁₅O₆S₂) forms…` → **`…a single neutral repeat unit (C₁₁H₁₆O₆S₂), and PTFE by…`** |
| Table S1 Adsorbate 행 | `SDCP repeat unit (neutral / self-doped)` · `C₁₁H₁₆O₆S₂ / C₁₁H₁₅O₆S₂` → **`SDCP repeat unit (neutral)`** · **`C₁₁H₁₆O₆S₂`** |

부수 효과: 표의 자가도핑 화학식이 `C₁₁H₁₇O₆S₂` 로 읽히던 문제(H 가 **늘어난** 표기)도 그 행이
사라지며 함께 해소된다. 구조도 깨끗해진다 — 자가도핑 화학종은 **분자 문단(ORCA)에만** 나오고
거기서는 정당하다(스핀 위치를 보는 계산). 흡착 문단은 중성만.

⏳ **본문 전체 점검 필요:** doped 흡착에너지 수치나 "자가도핑형이 더 강하게 붙는다" 류 비교가
다른 절에 남아 있으면 전부 뺀다 (마감 문서의 금지 서술 2건).

⏳ **고정 원자 144개가 본문에 없다.** Table S1 에는 `Constrained atoms 144 (z ≤ 17.40 Å)` 가 있는데
Methods 는 "four layers, 192 atoms" 까지만 말한다. 넣으려면 `with more than 15 Å of vacuum` 뒤에
`, the lower 144 atoms held fixed,`. 1저자 결정 대기.

### Supplementary Note 2 (Methods 편입 후 남는 것)

> **Supplementary Note 2. Spin partition of the oxidized SDCP oligomers**
>
> Löwdin spin populations were taken from the final self-consistent field of each optimized
> structure; for six repeat units the total spin population is 1.000, as expected for one unpaired
> electron. The backbone share quoted in the main text counts ring atoms only, and is 79.7% at six
> repeat units; counting the side-chain ether oxygens as well raises it to 91.6%, whereas counting
> the ring hydrogens instead gives 79.5%. For six repeat units the hydrogen was removed from the
> sulfonate on the fourth thiophene ring counted from one chain end. Each structure is a
> single self-consistent solution; no search for alternative spin-localized solutions or side-chain
> conformers was performed, and the spin densities are reported directly rather than interpreted as
> hole charge densities. The models are isolated gas-phase molecules, without solvent, external
> counterions, or interchain packing.

역할 분담: **Methods = 어떻게 계산했나** · **Note 2 = 그 숫자가 어떻게 정의됐고 무엇을 뜻하지
않는가.** 제목도 "Oligomer models" → "Spin partition" 으로 바꿨다 (모델 서술은 Methods 로 갔다).
`external counterions` 의 `external` 은 필수 — SO₃⁻ 자체가 짝음이온이라 그냥 "counterions 없음"
이라고 하면 모순으로 읽힌다.

### Table S1 · Methods 표기

- **Table S1 제목을 좁힌다**: *"Parameters used for the **adsorption-energy** DFT calculations."*
  표 내용이 전부 슬랩·흡착 쪽인데 코드가 둘이 된 이상 종전 제목은 실제보다 넓게 말한다.
- 표 각주 한 줄: *"Parameters for the molecular (oligomer) calculations are given in Supplementary
  Note 2."*

### 채운 값 · 남은 빈칸

- ✅ ORCA **6.1.1** · 수렴 기준은 **프로그램 기본값**(NormalOpt): TolE 5e-6 Eh · TolMAXG 3e-4 ·
  TolRMSG 1e-4 Eh/bohr · TolMAXD 4e-3 · TolRMSD 2e-3 bohr (`n6_doped.out` 실측 2026-09-08).
  ⚠ `Strict Convergence = False` 이므로 "tight" 라고 쓰지 않는다.
- ⏳ **반복단위의 화학 표기** — 지금은 "the repeat unit defined in Figure 1" 로 가리킨다.
  Figure 1 이 그 구조를 실제로 정의하지 않으면 여기서 한 번 풀어 써야 한다.
- ✅ **n=6 도핑 자리 = ring3(0-기준) = 고리 4번(1-기준·원고 표기)** (2026-09-08). 라벨이 아니라 구조에서 찾았다 — 탈양성자
  sulfonate(S=72)에서 곁사슬을 따라가 원자 43(C)이 ring3 에 속한다 (`nseries_n6.py doping_site`).
  스핀 최대는 ring4 = 고리 5번(23.3)이라 **자리에서 한 칸 밀려 있다** — 본문의 `rather than localized at the
  oxidation site` 가 데이터로 받쳐진다.

> ⚠ **고리 번호 규약 (2026-09-09 통일).** 원고·그림(Figure S4)은 **1-기준(고리 1–6)**,
> 기계 자료(`figure_S4b_ring_profile.csv` 의 `ring_index`, `sdcp_nseries_spin_2026_09_08.json`
> 의 `ring0..ring5`)는 **0-기준**이다. **ring3 = 고리 4번**이고 그 자리가 산화 자리다.
> ⛔ 종전 Note 2 는 `on ring 3` 이라고만 써서, 1-기준으로 읽으면 산화 자리가 스핀이 몰린
> 세 고리(4·5·6번)를 **비껴가는** 그림이 됐다. 실제로는 그 셋 중 하나다.

> ⛔ **고리별 프로파일(옛 Figure S4b · 패널 (c))을 원고에서 뺀다 (1저자 결정 2026-09-09).**
> 남기는 주장은 **S4a 하나** — *홀이 술폰산에서 백본 π 로 옮겨간다*(백본 79.7 % · SO₃ 7.7 %).
> 뺀 이유: 고리별 값으로 뭔가를 말하려면 *"왜 산화 자리가 최대가 아닌가"* 에 답해야 하는데
> **우리 데이터로 답이 안 된다** — ① n=6 계산이 한 번뿐이고 산화 자리도 하나라 대조가 없다
> ② `fresh SCF 한 번`(원장 금지_서술) ③ **오차막대가 없어 23.3 vs 20.0 이 유의한지 모른다**.
> 그리고 하려는 주장(폴라론이지 국재 라디칼이 아니다)에 **고리 분해가 필요하지 않다** —
> SO₃ 가 7.7 % 뿐이라는 것만으로 *"산화 자리에 국재하지 않는다"* 가 성립한다.
> ⚠ `db/properties/figure_S4b_ring_profile.csv` 는 **실측이라 지우지 않는다** — 원고 미사용으로 표시한다.
> ⚠ 그래서 본문의 `delocalized over several repeat units` 는 이제 **고리 분해가 아니라 n-추세**
>   (백본 35 → 79.7 % as n grows)가 근거다. 한 반복단위에 갇혀 있다면 n 을 늘려도 지분이
>   안 올라간다 — 약해진 근거지만 성립한다. 문구를 더 좁히려면 `delocalized over the
>   conjugated backbone` 으로 바꾼다.

## ⏳ 흡착 문단 — **보류 초안** (2026-09-09 · 1저자: "값은 나중에 고친다")

> 원고 초안이 이 문단을 들고 있다. **지금 상태로는 못 내보낸다.** 다만 **두 갈래를 갈라야
> 한다** — 하나는 곧 풀리고 하나는 안 풀린다.

### 갈래 A — 값·부등호: **보류다. 곧 복권된다** ⏳

`HZ-sdcp-wave1-absolute-eads` (**BLOCKED**) · 마감 카드 상태
`closed_for_scope_pending_spin_equivalence`.
막고 있는 것: **절대값 · 0.346 eV · 부등호 방향 서술 전부**.

원인은 하나다 — 기체 기준 분자가 `NUPDOWN=0` 제약이라
`δ_m = E_M^{M=0} − E_M^{free}` 가 절대 E_ads 에 남는다 (자세차에는 소거된다).

**해제 조건 (카드 §해제_조건_spin_equivalence_짝검사 — 3단계다):**

| 단계 | 무엇을 | 무엇이 풀리나 |
|---|---|---|
| 1 | 기준 분자 **3종**(box24·기하 고정)을 **free-spin `NUPDOWN=−1` + `LREAL=F`** 로 재실행 | **δ_m 확정**만. 값은 아직 안 풀린다 |
| 2 | 관련 SDCP/PTFE **complex 를 `LREAL=F`** 로 재실행 | **ΔΔE_ads(조각 간 대비)** — slab 이 대수적으로 소거된다 |
| 3 | **matching slab F** 추가 | **절대 E_ads** — 원고가 인용하는 `−0.77 / −0.41` 이 여기서 풀린다 |

⚠ 회신 P 3·4번: `LREAL` 은 **F 유지** — 분자 T 재실행은 all-T 값을 만들 뿐 all-F 정본을
못 잰다. 분자 T 계산은 생략.

⛔ **정정 (2026-09-09).** 조율 세션이 처음에 *"분자 3점이면 이 문단 전체가 살아난다"* 고
말했는데 **틀렸다.** 분자 3점은 **1단계뿐**이고 δ_m 만 준다. 원고가 쓰는 것은
**절대 E_ads** 라 **3단계까지** 가야 한다. 1단계만 하고 값을 되살리면 회신 O 가 반려한
그 자리로 돌아간다.

**도구:** `tools/sdcp/vasp_handoff_bundle.py --closure` 가 정본이다.
⛔ `tools/sdcp/make_allF_static_bundle.py` 는 **2026-08-29 폐기** — 부격자 씨앗을 스스로
만들려다 슬랩 인덱스와 복합체 원자 순서가 어긋나는 문제가 있었다(2026-08-12 에 "파일
순서로 반 갈랐더니 24/48 일치 = 동전 던지기" 이력). 정본 생성기가 `_assert_slab_lineage` +
순열 재매핑으로 처리한다.

⇒ 그때 이 문장이 복권된다 (그때 수치로):

> The SDCP fragment gives an adsorption energy of **[δ_m 복구값]**, more negative than the
> **[δ_m 복구값]** obtained for PTFE (Figure 2e).

⚠ 복권돼도 남는 제약 — 카드 ⛔_금지_서술 그대로:
`'PTFE 보다 이긴다'·'약 2배 강하다'` 금지(per-분자 전자에너지 차 이상 금지) ·
PTFE **고분자**로 확장 금지(조각 vs 조각) · 접착력·계면저항·피복률 확장 금지 ·
자리 불문 금지(자리대비는 30 meV 해상도에서 미해결).

### 갈래 B — 기전 문장: **보류가 아니라 반증됐다** ⛔ 안 돌아온다

초안의 두 문장:
1. *"the acidic O–H of the sulfonate is directed at a surface oxygen"*
2. *"The polar sulfonate moiety therefore engages the exposed surface sites of NCM far more
   effectively than the non-polar fluorocarbon chain."*

**우리 좌표가 정반대다** (`db/structures/sdcp_wave1/sdcp_neutral__*.vasp` 네 자세 직접 측정,
2026-08-29 회신 T P0-1 · 우리가 독립 재현):

| | 실측 |
|---|---|
| 산성 O–H 의 **H ↔ 슬랩** | **7.083 / 7.099 / 7.158 / 7.170 Å** |
| 술포네이트 O ↔ 슬랩 Li | 4.88–5.39 Å |
| **실제 최단 접촉** | **탄소결합 H ··· 슬랩 O/Ni 2.441–2.462 Å** |

⇒ **δ_m 을 고쳐도 이 둘은 복권되지 않는다.** 값의 보류와 기전의 반증은 다른 사건이다.
`HZ-sdcp-sulfonate-mechanism`(CONDITIONAL): *"기전 문장을 쓰지 않는다. C-12 가 회수되면
그 DFT 로 판정한다"* — 즉 기전은 **C-12 회수**를 기다리지 δ_m 을 기다리는 게 아니다.

**대체 문장 (지금도 쓸 수 있다 — 기하는 보류 대상이 아니다):**

> In the optimized geometries the closest contacts to the slab are carbon-bound hydrogens at
> 2.44–2.46 Å, with the sulfonate oxygens 4.9–5.4 Å from the nearest surface Li (Figure 2f);
> the calculations do not identify the sulfonate as the contacting group.

### 그때까지 Figure 2e 는?

에너지 막대라 갈래 A 에 묶인다. 셋 중 하나 — ① 2e 를 빼고 2f(기하)만 · ② δ_m 3점을 돌려
풀고 그대로 · ③ 보류 표시를 달고 둔다. **1저자 결정: 값을 고쳐서 살린다(②)** — 그래서
이 절을 지우지 않고 보류 초안으로 둔다.

## SI 연결

- **Figure S3** = 구조 (n=2 · n=3 end/mid · n=6) — `db/structures/si_figure_S3/` (xyz+vasp+vesta).
- **Figure S4** = 스핀 분포 3패널 — `docs/figures/sdcp_nseries_spin/sdcp_nseries_spin_partition.png`,
  영문 캡션 `docs/figures/sdcp_nseries_spin/caption.md`. **표는 쓰지 않는다** (1저자 결정 —
  그림에 숫자가 다 찍혀 있다).
- 수치 원본(Origin-ready) = `db/properties/sdcp_nseries_spin_2026_09_08.csv` ·
  `db/properties/sdcp_n6_ring_profile_fig.csv`.
- 정본 값·허용/금지 서술 = `db/properties/sdcp_nseries_spin_2026_09_08.json`.

## ⏳ 남은 것

1. ✅ **Section X 해결** — 4-probe 실측 **250 mS cm⁻¹** (1저자 2026-09-08). 문헌 소환값이
   아니라 우리 측정이라 `measured directly` 로 쓴다. 단위는 mS cm⁻¹ 로 뒀다 — 이 논문의
   황화물 전해질 이온전도도와 같은 축에서 읽히게 (0.25 S cm⁻¹ 로 바꾸려면 원고 전체 통일 필요).
   ⏳ 시료 형태만 미확인: **박막이면 four-point-probe**, 펠릿이면 `four-terminal`/`van der Pauw`
   로 한 단어 교체.
2. **삽입 위치** — FT-IR 절 **뒤**여야 한다. [1]의 `above` 가 그 전제다 (앞이면 `below` 로).
3. ✅ **n=6 도핑 자리 = ring3(0-기준) = 고리 4번(1-기준)** (해결). 선택: 본문에 `(ring 4)` 을 넣어 검증 가능하게 만들지,
   Figure S4 (c) 패널에 자리 표시를 넣을지 — 1저자 결정.

## 흡착 문단 — C-12 대기 상태로 동결 (2026-09-08)

**1저자 결정: 외주(C-12) 결과가 올 때까지 hold.** 지금 문단은 자리표시로 둔다.

### 확정된 것

- **SI 그림 폐지.** 흡착 쪽 SI 그림은 만들지 않는다 — Figure 2f 가 슬랩·흡착 구조를,
  Table S1 이 셀·진공·고정원자 144·상자 여백을 싣는다. 본문 참조는 `Table S1` 하나로 줄인다
  (`computational models and` · `Figure S[x] and` · `respectively` 삭제).
  ⚠ 자가도핑 쪽 SI 그림 둘(올리고머 구조 · 스핀 분포)은 **그대로 살아 있다.**
- **이름은 `adsorption energy`.** 사전등록이 막은 것은 `binding energy` · `free energy` 뿐이다.
  한정어 `fixed-geometry` 는 식 (1) `where` 절에 한 번:
  *"…all evaluated as single points at fixed geometries."*
- **인과 서술 삭제.** `primarily due to robust hydrogen bonding` 은 쓰지 않는다. 자세에 그 접촉이
  있다는 기술은 되지만, 에너지 하나로 특정 접촉의 기여를 분리할 수 없다.

### C-12 가 오면 할 일 4

1. 숫자 셋 채우기 — `E_ads(sdcp)` · `E_ads(ptfe)` · `ΔE_ads` (사전등록이 셋 다 보고하라고 정함).
2. **주어를 ΔE_ads 로.** 사전등록: *"순위·부호 주장은 ΔE_ads 로, 절대값은 '규모(order)' 로만."*
   ΔE 는 clean slab 항이 소거돼 안정하고 절대값은 그것을 직접 빼서 민감하다.
3. 식 (1) `where` 절에 `fixed geometries` 한정어 확인.
4. 축자 조건 문구 한 줄 넣기 — *"사전등록한 18.272 × 11.512 Å² lateral cell, 1 fragment/cell,
   fixed geometry, pm1, PBE+U+D3 프로토콜에서의 differential complex–gas reference energy 이다…"*
   ⛔ 사전등록이 **줄이거나 조건절 떼는 것을 금지**한다.

⚠ 숫자와 구조는 **같은 런(C-12)에서 함께** 온다. 섞으면 안 된다 — 이번에 내가 에너지는 wave1,
기하는 b00 로 섞어 쓴 사고가 있었다 (wave1 자세는 술포네이트가 표면에서 4.88–5.39 Å 떨어져 있다).

## Methods · DFT(슬랩) 문단 — **확정본 2026-09-15** (1저자 "이걸로 확정" · 9/16 제출본)

> 원장 정합 점검을 마친 판이다 — 값 0개 · 부등호 0개 · 기전 문장 0개 · "converged" 0회 ·
> 자가도핑형 0회. 인용위험 셋(`HZ-sdcp-wave1-absolute-eads` · `HZ-sdcp-sulfonate-mechanism` · doped 마감)
> 어디에도 안 걸린다. 기체상 기준 상자(box20/box24 패딩, `sdcp_wave1_results.json`
> `molecule_reference_box`)와도 맞다.

> **DFT calculations:** Adsorption at the cathode surface was treated with periodic, spin-polarized DFT in
> Quantum ESPRESSO using the Perdew–Burke–Ernzerhof functional, Grimme D3 dispersion, and a Hubbard
> correction of U = 6.2 eV on the Ni 3d states.[51,52] Wave functions and the charge density were expanded
> to 60 and 480 Ry, respectively, with Gaussian smearing of 0.05 eV and a self-consistency threshold of
> 1 × 10⁻⁶ Ry. The NCM811 surface was approximated by an antiferromagnetic LiNiO₂(104) slab (1 × 4, four
> layers, 192 atoms, 18.27 × 11.51 Å in plane) with more than 15 Å of vacuum, sampled with a Γ-centered
> 2 × 3 × 1 mesh and a dipole correction along the surface normal. SDCP was modeled as a single repeat unit
> in its neutral, protonated form (C₁₁H₁₆O₆S₂), and PTFE as a C₁₀F₂₂ segment. Adsorption configurations
> were pre-screened over seven surface sites and 48 molecular orientations with a machine-learned
> interatomic potential, and the lowest-energy configuration found at a surface Li site and at a surface
> Ni site was then evaluated by DFT. Gas-phase references were relaxed at the Γ point until residual forces
> fell below 1 × 10⁻³ Ry bohr⁻¹, with the box padding increased from 20 to 24 Å to confirm convergence.
> Adsorption energies were obtained as follows:
>
> E_ads = E_slab+binder − E_slab − E_binder (1)
>
> where E_slab+binder, E_slab, and E_binder are the total energies of the adsorbed complex, the clean slab,
> and the isolated binder, respectively, all evaluated as single points at fixed geometries.

**09-08 판에서 바뀐 것 (2026-09-15 같이 읽기)**

| # | 무엇 | 왜 |
|---|---|---|
| ① | *"relaxed at the Γ point **in the same cell**"* → "in the same cell" **삭제** | 분자 기준은 슬랩 셀이 아니라 패딩 상자(20/24 Å)에서 돌았다 — 사실 오류. 뒤 구절 "box padding" 이 상자를 이미 말한다 |
| ② | *"taken in its protonated form to represent the side chains that **remain undissociated** at the particle surface"* → *"in its neutral, protonated form"* | 재지 않은 물리를 이유로 댄 문장이었다. 범위 선언으로만 |
| ③ | *"The deprotonated, self-doped form … was not considered"* 문장 — **넣지 않기로** (1저자) | "neutral, protonated form" 이 이미 범위다. 8/23 단일점 각주와 같은 선례 — **안 적고, 물으면 답한다**. 회신용 문장은 `kb/syntheses/sdcp_eads_revision_defense_2026_08_23.md` §회신용 |
| ⚠ | 제출 전 확인: ③ 삭제 뒤 **"The deprotonated."** 두 단어 꼬리가 남아 있었다 | 확정 직전 붙여넣기에서 발견 — 지운다 |

**이 문단 밖에 남은 것**
- **Table S1 참고번호** — 표는 `Ref. 48, S1` / `Ref. S2, 49` (09-08 판), 본문은 `[51,52]`. 표를 51/52 로 맞춘다
  (`docs/manuscripts/table_s1_build.js` 46–47행). MLIP(UMA) 본문 인용은 없음 — SI `Ref. S3` 만. 선택 사항.
- **코드 표기** — 문단은 QE 문법(60/480 Ry · 1e-6 Ry · 1e-3 Ry/bohr), 원장 wave1 값은 VASP(520 eV · 1e-6 eV ·
  −0.02 eV/Å). **값을 넣는 날** 둘 중 하나로 맞춘다 (QE 재계산 또는 방법 문단 VASP 화). 값 없는 제출본엔 안 걸린다.

