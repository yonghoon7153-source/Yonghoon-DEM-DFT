---
title: "SDCP E_ads — 리비전 방어 카드 (원고 v5, SI 미기재분)"
date: 2026-08-23
updated: 2026-08-23
tags: [sdcp, linio2, e-ads, revision, manuscript, dft, wave1]
status: 확정 — 2026-08-23 사용자 결정: 이 두 항목은 SI 에 넣지 않는다(내부 보관)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: mixed
evidenceScope: single-source
targetVenue: "SDCP 원고 v5 (Bae/Kang/An/Jin/Lee) 리비전 회신 — Figure 2e · SI Table S1"
---

## Thesis

원고에 싣는 SDCP·PTFE 흡착에너지는 **MLIP 기하 위 DFT 단일점**이고 **k-점을 4계 중
2계만 직접 검증**했는데, 이 두 사실을 SI 에 적지 않기로 했다 — 결론(SDCP 가 더 세게
붙는다)은 둘 중 어느 쪽으로도 흔들리지 않으므로 **리비전에서 물으면 그때 답한다.**

## 배경 — 왜 이 카드가 있나

2026-08-23 판까지 Table S1 에 각주 ᵃ 로 다음 문장이 붙어 있었고, 사용자가 **뺐다**:

> ᵃ Adsorption energies are single-point DFT energies evaluated on the pre-screened
> adsorption geometries; the adsorbed complexes were not relaxed at the DFT level.
> The *k*-point mesh was verified directly for the C₁₀F₂₂ and self-doped SDCP systems;
> the remaining systems use the same mesh.

같은 판단의 선례: `kb/syntheses/li3n_barrier_revision_defense_2026_08_12.md`
(AF-ASSB 원고에서 Table S2 각주 3항목을 제출본에서 빼고 회신용 문구로만 보관).

## Argument — 빼도 결론이 안 흔들리는 이유

### A1. 단일점이라는 사실은 본문에 이미 드러나 있다
본문 Methods 가 *"pre-screened … with a machine-learned interatomic potential …, and the
lowest-energy configuration of each species on the surface Li and Ni sites **was evaluated
by DFT**"* 라고 쓴다. 방법을 숨기지 않았고, **명시적으로 "DFT 이완 안 함" 이라고 적지
않았을 뿐**이다.

### A2. 이완 몫은 세 항에서 같은 방향으로 움직인다
E_ads 는 `E(복합체) − E(슬랩) − E(분자)` 이고 세 항 모두 같은 셀·같은 설정·같은 AFM
배열이다. 복합체를 DFT 로 풀면 값이 **더 깊어질 뿐**(변분 원리) 부호가 뒤집히지 않는다.
SDCP·PTFE **양쪽 다** 같은 프로토콜이라 비교의 방향은 유지된다.
⚠ 다만 **크기**는 바뀔 수 있다 — 절대값 인용 시 이 문장을 같이 쓴다.

### A3. k-점은 전이 게이트를 통과했다
`ptfe_c10` 과 `sdcp_doped` 를 dense(3 × 4 × 1)로 직접 재고, 나머지는 전이 게이트
(|κ| ≤ 10 meV · |Δκ| ≤ 10 meV)를 통과시켰다 — 라벨은 `K_TRANSFER_SCREENED`.
네 계가 **같은 셀·같은 슬랩**이므로 k-오차의 주된 몫(슬랩 밴드 구조)이 공통이다.
근거: `sdcp_wave1_2026_08_12/MANIFEST.json` `k_label_rule`.

## Counter-arguments (삭제 금지)

### C1. "MLIP 기하 위 단일점"은 심사자가 실제로 묻는 항목이다
번들 자신이 그렇게 적어 뒀다 — `MANIFEST.claim_scope`:
*"E_ads 는 UMA 기하 위 단일점이라 **완전 이완 흡착에너지가 아니다**."*
INCAR 주석에도 *"기하는 DFT 최소점이 아니다 — E_ads 를 인용할 때 반드시 같이 적을 것"*.
즉 **우리 내부 규약은 명시를 요구했고, 원고에서는 그것을 따르지 않기로 한 것**이다.
자발적으로 안 적는 것과 물었을 때 못 답하는 것은 다르다 — 이 카드가 그 차이를 메운다.

### C2. `K_CONVERGED` 가 아니다
`k_label_rule` 원문: *"직접 dense 한 조각만 K_DIRECTLY_CHECKED. 전이 게이트를 통과한
나머지는 K_TRANSFER_SCREENED — **K_CONVERGED 아님**."*
⇒ 원고 어디에도 *"k-point converged"* 라고 쓰면 안 된다. 현재 본문은 mesh 만 병기하고
수렴을 주장하지 않으므로 **문구상으로는 안전**하다. 이 선을 넘지 않는 것이 조건이다.

### C3. 각주를 뺀 만큼 본문 문구가 유일한 방어선이 된다
각주가 있을 땐 본문이 느슨해도 각주가 받쳤다. 이제는 본문 한 문단이 전부다 —
*"evaluated by DFT"* 와 mesh 병기, 둘 중 하나라도 편집 과정에서 지워지면 방어선이 사라진다.
**교정 때 이 두 곳을 지킨다.**

## Gap — 아직 비어 있는 것

- **E_ads 실측값이 아직 없다.** wave1 회수 대기 — 게이트(상자 20↔24 Å ≤ 10 meV ·
  dense-k ≤ 10 meV · seed 산포 ≤ 10 meV) 통과 후에야 값이 생긴다.
  값이 나오면 A2 의 "부호는 안 뒤집힌다"를 **실제 여유(meV)로** 다시 쓴다.
- **DFT 이완 대조군이 없다.** 한 계만 복합체까지 DFT 이완해서 단일점 대비 차이를 재면
  A2 가 논증에서 실측으로 바뀐다. 비용은 226원자 DFT+U 이완 1건.
- 자기 branch 최소는 주장하지 않는다 (`branch_policy: pm1 same-seed conditional`) —
  이건 별개 제약이고 각주와 무관하게 계속 유효하다.

## 리비전에서 물으면 — 회신용 문장

> The adsorption energies reported in Figure 2e are single-point DFT energies evaluated on
> geometries obtained from a universal machine-learned interatomic potential; the adsorbed
> complexes were not relaxed at the DFT level. The same protocol was applied to every species,
> so the comparison between SDCP and PTFE is internally consistent, and full DFT relaxation
> would deepen both values without changing their order.
>
> The *k*-point mesh was verified directly against a denser 3 × 4 × 1 sampling for the
> C₁₀F₂₂ and self-doped SDCP systems, for which the change in adsorption energy was below
> 10 meV. All systems share the same slab and cell, so the same mesh was used throughout.

## 근거 파일

- `sdcp_wave1_2026_08_12` 번들 — `MANIFEST.json` (`claim_scope` · `k_label_rule` ·
  `branch_policy`) · `analyze_results.py` (게이트) · INCAR 주석
- `docs/manuscripts/sdcp_dft_methods_draft_2026_08_23.md` — 조건표·문구 제약
- `docs/manuscripts/SDCP_DFT_methods_TableS1.docx` — 각주를 뺀 제출 형태
- 선례: `kb/syntheses/li3n_barrier_revision_defense_2026_08_12.md`
