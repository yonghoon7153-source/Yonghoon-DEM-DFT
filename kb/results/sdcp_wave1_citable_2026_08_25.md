---
title: "SDCP wave1 인용 확정본 — 논문에 쓰는 값 한 장 (basin 일치분)"
date: 2026-08-25
updated: 2026-08-25
tags: [sdcp, vasp, citable, canonical, adsorption, paper]
status: 인용확정
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-25
verifiedBy: "원자료 총에너지에서 재유도(손 전사 0) · canonical validate 0 위반 · 교차리뷰 E 6라운드"
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source
---

# SDCP wave1 — 인용 확정본

**이 카드가 논문·발표에서 인용하는 유일한 기준이다.** 값은 전부
`db/properties/sdcp_wave1_citable.json` 에서 오고(원자료 총에너지 재유도),
canonical registry 에 11건 등록돼 수치 대조가 자동으로 돈다
(comparison_group `sdcp-wave1-*` — argyrodite 4축과 절대 안 섞임).

그림: `db/properties/sdcp_wave1_citable_fig.png` (+Origin CSV `…citable.csv`)

## 인용 가능 — ΔE 자리 선호 (meV · 양수 = Li-top 우세)

| 조각 | pm1 | net4 | 서술 |
|---|---:|---:|---|
| **ptfe_dimer** | **+36.07** | **+36.16** | ★ matched-pose ΔE 가 두 sampled branch 에서 **0.09 meV 차이** (서로 다른 basin 인데도). ⚠ "0.1 meV 정확도" 라 쓰지 않는다(k-미검증) · basin 무관성의 증명 아님 |
| ptfe_c10 | +49.77 | — | 단일 branch. wave1.5 후 net4 재확인 |
| sdcp_neutral | +9.27 | — | 단일 branch · **사실상 무선호**(<10 meV)로 서술 |

## 인용 가능 — E_ads (eV · box24 기준 · pm1 branch)

| | Li-top | Ni-top | cross |
|---|---:|---:|---|
| ptfe_dimer | −0.366 | −0.330 | — |
| ptfe_c10 | (basin 혼합) | −0.363 | — |
| sdcp_neutral | **−0.767** | −0.758 | −0.773 / −0.763 |

교차확인: basin 이 맞는 net4 쌍(dimer-Litop −0.366 · c10-Nitop −0.362)이
pm1 과 ≤1 meV — 재현성 근거. **단 net4 열은 wave1.5 전까지 정본 아님.**

## 헤드라인 문장 (그대로 써도 되는 판)

1. PTFE 조각과 SDCP 는 모두 LiNiO₂(104) 표면에서 Ni 자리보다 **Li 자리를
   선호**한다 (ptfe_dimer ΔE = +36.1 meV, 두 자기 branch 에서 0.09 meV 차이).
2. **SDCP(−0.77 eV)는 PTFE 조각(−0.33~−0.37 eV)보다 약 2배 강하게** 흡착한다.
3. 흡착 기하는 MLIP 이완 위 단일점이며, 값은 내부 비교(차이)로만 사용한다.

## ⚠ 값과 반드시 같이 적는 단서 (떼면 인용 아님)

- 기하 = **MLIP(UMA, freeze 0.85) 이완 위 단일점** — DFT 최소점 아님
- 진공 · 0 K · 단분자 — 실제 전극 예측 아님
- k 직접검증은 c10 만(0.0/0.2 meV) — dimer·neutral 은 transfer-screened
- VASP PAW 절대값 — 타 코드/문헌과 직접 비교 금지

## ⛔ 인용 불가 (등록 자체를 안 했다)

sdcp_doped 전 항목(라디칼 분기) · net4 E_ads(wave1.5 대기) ·
branch offset ≈50 meV(진단값 — 수치 인용 금지, codex E-4)

## 관련

판정: `kb/results/sdcp_wave1_vasp_return_2026_08_25.md` ·
리뷰: `kb/reviews/codex_E_sdcp_wave1_gate_2026_08_25.md` ·
webapp `/sdcp`
