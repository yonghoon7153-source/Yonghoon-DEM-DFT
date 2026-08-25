---
title: "SDCP wave1 VASP 회신 — 자기 basin 이 갈랐다 (E_ads · 자리선호)"
date: 2026-08-25
updated: 2026-08-25
tags: [sdcp, vasp, adsorption, magnetic, gate, wave1, ptfe]
status: 확정-부분
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-25
verifiedBy: "43 OUTCAR 직접 재해석 · 두 seed 교차확인 · basin 벌점 3중 독립 재현"
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# SDCP wave1 VASP 회신 (2026-08-25)

2026-08-12 번들 30잡 / OUTCAR 43개. 외주 완주, 전부 정상 종료.

## ⚡ 한 줄

**pm1 seed 는 완결이고, net4 는 그것을 ≤1 meV 로 재현한다 — basin 이 맞는 잡에 한해서.**
게이트 13건은 뿌리가 둘뿐이다.

## 1. 게이트 0/30 은 우리 버그였다 (숫자 아님)

외주처 지적이 맞았다. 다만 **원인 진단은 달랐다** — 한 줄에 결함이 둘 겹쳐 있었다.

| | 결함 | 증상 |
|---|---|---|
| ① | `re.search(KEY + "=...")` 에 **앵커가 없다** | 분자 박스 OUTCAR 129행의 VASP 권고문 `\| So try LREAL= Auto` 가 첫 매치 → 실제 줄이 `LREAL = F` 인데 got="Auto" |
| ② | 되울림을 **문자열로 비교** | `520.0`≠`520`, `T`≠`.TRUE.` |

외주처는 ②만 지목했다(①은 "VASP 가 Auto 를 논리값으로 출력"으로 설명 — 실제로는
권고문 오탐이다). 둘 다 고친 뒤 **INCAR_MISMATCH 30 → 0**, 게이트 **0/30 → 17/30**.
LREAL 은 `Auto`/`On` 을 되울림만으로 못 가른다 — 실공간/역공간까지만 검증한다(도구에 명시).

덤으로 `_read_text` 가 `.gz` 경로를 받으면 gzip 바이너리를 `errors="ignore"` 로 읽어
**깨진 문자열을 조용히 반환**하고 있었다(모든 정규식이 빗나가 E0·NIONS 가 전부 None).
매직바이트 판별로 교체.

## 2. 남은 게이트 13건 = 뿌리 둘

### (A) net4 clean slab 이 시드 topology 를 못 지켰다 — 11잡 연쇄

**언제나 같은 Ni 하나**다: POSCAR idx **82**, μ = **+1.18 μB**. 무작위 아님.

- basin **B**(82 뒤집힘): clean_slab · ptfe_c10 Nitop · ptfe_dimer 양쪽 · sdcp_neutral Litop · cross 2개 — 7잡
- basin **A**(시드대로): ptfe_c10 Litop · sdcp_doped 양쪽 · sdcp_neutral Nitop — 4잡

### (B) sdcp_doped 라디칼 스핀 분기 — 4잡 (seed 무관)

## 3. ★ ~50 meV 는 **branch offset 진단값**이다 (측정 아님 — 2026-08-25 codex E-4 로 정정)

> ⛔ **이 절의 첫 판("독립 네 경로에서 측정, 50.2 ± 0.2")은 과대주장이었다.** 네 값은
> 서로 **상관된 contrast** 다: 같은 조각의 ΔE식·E_ads식이 pose 에너지를 공유하고,
> E_ads 두 식은 같은 clean 쌍(net4−pm1 = **128.292 meV**)도 공유한다.
> 항등식 `ΔE차 = E_ads(Ni)차 − E_ads(Li)차` 로 닫으면 조각당 잔차 +0.93 / −0.47 meV —
> **독립 표본 4개가 아니라 사실상 조각당 1개**다. ±0.2 는 SEM 이 아니며 의미 없다.

| contrast | 값 (meV) |
|---|---:|
| ptfe_c10 ΔE 의 branch 차 | +50.45 |
| sdcp_neutral ΔE 의 branch 차 | −49.96 |
| ptfe_c10 Litop E_ads 의 branch 차 | −49.53 |
| sdcp_neutral Nitop E_ads 의 branch 차 | −50.44 |

**허용 문구**: *두 분자 맥락에서 얻은 서로 상관된 contrast 들이 **49.5–50.5 meV 의
magnetic-branch offset** 과 일치했다. 인과적인 "Ni #82 반전 비용" 이 아니라 진단값이다.*

- clean net4−pm1 자체는 **128.3 meV** 다 — 50 은 clean spin-flip 비용의 직접 측정이 아니다.
- "언제나 #82" 는 우리 db(`sdcp_wave1_results.json` 의 `flipped_ni_poscar_idx`)에 기계기록돼
  있으나 외주 첨부 RESULTS 에는 없었다 → 분석기 v2 가 `flip_indices_poscar` 를 RESULTS 에
  싣도록 고쳤다 (2026-08-25).
- 반전 **비용**을 재려면 같은 구조·같은 Hamiltonian 에서 #82 상태만 다른
  constrained/paired 계산이 필요하다 (noncollinear — 현재 범위 밖, 미착수).
- **보정에 쓰지 않은 결정은 유지** — codex 도 옳다고 확인.

## 4. 쓸 수 있는 값 (pm1 = A/A 완결)

ΔE = E(Ni_top) − E(Li_top) · 양수 = **Li_top 우세**

| 조각 | pm1 | net4 | 판정 |
|---|---:|---:|---|
| ptfe_dimer | +36.07 | **+36.16** | ★ matched-pose ΔE 가 두 sampled branch 에서 **0.09 meV 차이** (branch×site 상호작용). ⚠ k-미검증이라 "0.1 meV 정확도" 아님 · basin 무관성의 **증명 아님** — 공통 shift 상쇄의 정의가 곧 이 작은 상호작용 |
| ptfe_c10 | +49.8 | (A/B 오염) | 1-seed |
| sdcp_neutral | +9.3 | (B/A 오염) | 1-seed · 값이 작다 |
| sdcp_doped | +86.4 | −18.9 | ⛔ 라디칼 분기 — 미해결 |

E_ads (box24 기준, basin 일치분만):

| 잡 | net4 | pm1 |
|---|---:|---:|
| ptfe_dimer Litop | −0.366 | −0.366 |
| ptfe_dimer Nitop | −0.330 | −0.330 |
| ptfe_c10 Nitop | −0.362 | −0.363 |
| sdcp_neutral Litop | −0.768 | −0.768 |
| cross_Li_at_Ni | −0.773 | −0.773 |
| cross_Ni_at_Li | −0.763 | −0.763 |

**basin 이 맞으면 두 seed 가 ≤1 meV.** 어긋난 4잡은 전부 ~50 meV — (3) 과 같은 수다.

수렴 게이트: 분자 상자 box20→box24 **0.06–0.32 meV** · k 점 ΔE **0.0 meV** / E_ads **0.2 meV**.

## 5. 다음 (판단 필요)

1. **clean_slab net4 를 basin A 로 다시** — 이거 하나면 4잡이 풀린다. 가장 싸다.
2. sdcp_doped 라디칼 분기 — 스핀 상태를 고정해 다시 세울지 결정 필요. NELM=200 미수렴 1건도 여기.
3. 게이트 정밀화 제안: `MAGNETIC_REFERENCE_INVALID` 는 **E_ads 만** 막아야 한다.
   ΔE 는 clean slab 이 소거되므로 두 pose 의 basin 만 같으면 유효하다.
   ⚠ 원하는 답을 얻으려 게이트를 푸는 것으로 보일 수 있어 **단독 적용하지 않는다** — 리뷰 후.

## 반론 / 한계

- basin 벌점 50 meV 는 **4점 추정**이고 전부 같은 슬랩·같은 idx 82 다. 다른 자리가
  뒤집히면 같은 값이라는 근거는 없다.
- 3항의 "50 meV 로 보정" 은 **하지 않았다**. 보정값으로 결론을 만들면 측정이 아니라 가정이다.
- sdcp_doped 는 두 seed 가 105 meV 벌어진다 — 어느 쪽도 인용 불가.

원자료: `db/properties/sdcp_wave1_results.json` · `.csv`
