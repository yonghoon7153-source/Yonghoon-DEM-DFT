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
evidenceScope: multi-source
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

## 3. ★ basin 벌점을 **측정**했다 — 50 meV

A/B 가 섞인 잡의 어긋남이 전부 같은 크기다. 서로 독립인 네 경로에서:

| 경로 | 값 |
|---|---|
| ΔE ptfe_c10 (100.2 − 49.8) | **+50.4 meV** |
| ΔE sdcp_neutral (9.3 − (−40.7)) | **+50.0 meV** |
| E_ads ptfe_c10 Litop | **50 meV** |
| E_ads sdcp_neutral Nitop | **51 meV** |

⇒ **Ni #82 를 뒤집는 값은 분자와 무관하게 50.2 ± 0.2 meV**, 그리고
**basin A 가 50 meV 낮다** = net4 clean slab 은 **제 바닥이 아니다**.
게이트가 막은 건 옳았고, 이제 막힌 이유가 숫자로 설명된다.

## 4. 쓸 수 있는 값 (pm1 = A/A 완결)

ΔE = E(Ni_top) − E(Li_top) · 양수 = **Li_top 우세**

| 조각 | pm1 | net4 | 판정 |
|---|---:|---:|---|
| ptfe_dimer | +36.1 | **+36.2** | ★ **2-seed 0.1 meV 일치** — basin 이 달라도 같다 |
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
