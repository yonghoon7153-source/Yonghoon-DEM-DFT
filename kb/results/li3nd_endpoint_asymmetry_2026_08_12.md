---
title: li3nd NEB 끝점 2.07 eV — 수치 인공물이 아니라 실제 자리 차이
date: 2026-08-12
updated: 2026-08-12
tags: []
status: 진행
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
---

## 무엇이 문제였나

li3nd(Li₃Nd, Fm-3m) 공공 NEB 의 두 끝점 에너지가 **+2072 meV** 벌어졌다.
공공은 Wyckoff **c**(ep_initial), 뛰는 Li 는 **b**(ep_final) —
즉 Δ = E(공공@b) − E(공공@c) 다 (meta.json 의 `pair_orbits`).

금속에서 두 Li 자리가 2 eV 차이 나는 건 크다. 게다가 k 3×3×3 · degauss 0.02 는
금속에 성기다. **k/smearing 미수렴 의심**이 자연스러웠고 오늘 세 번 제기됐다.

## 판정 — 수치가 아니다

이완된 끝점 좌표를 고정하고 scf 만 사다리로 돌렸다
(`splice_relaxed.py --positions_only` 로 기하 승계 · 각 31원자 · 8건):

| 조건 | Δ (meV) |
|---|---:|
| k 3×3×3 · degauss 0.02 | 2072 |
| k 5×5×5 · degauss 0.02 | 2045 |
| k 7×7×7 · degauss 0.02 | 2048 |
| k 5×5×5 · degauss 0.01 | 2013 |

전체 산포 **59 meV = 2.8%**. k 5→7 에서 3 meV, degauss 절반에 32 meV.
→ **k 도 smearing 도 수렴했다. 2.07 eV 는 실제 자리 에너지 차다.**

## 따라서 NEB 를 어떻게 읽나

Ea(→) 2.114 eV 중 거의 전부가 이 자리 차이고, Ea(←) ≈ 42 meV 로 상온 kT 수준이다.
즉 **안장점이 아니라 언덕**이다 — 공공은 c 에 살고 `c→b` 는 전도 경로가 아니다.
단일 Ea 로 인용하면 안 되고, "매우 비대칭한 홉" 으로 서술해야 한다.

## 남은 한계 — 셀 크기

사다리는 k·smearing 만 테스트했다. **2×2×2(31원자) 의 공공-공공 이미지 상호작용은
검증되지 않았다.** 금속의 중성 공공이면 보통 0.1 eV 수준이라 2 eV 를 만들진 못하지만,
이 숫자를 논문에 쓸 거면 3×3×3 셀 한 번은 봐야 한다.

## 재현

```
ls /data/work/runs/sei_neb_v2/li3nd/ep_*/ladder_*/scf.out
```
사다리 입력은 `tools/sei/splice_relaxed.py --positions_only` 로 만들었다
(고정셀 relax 는 CELL_PARAMETERS 를 안 찍어서 그 플래그가 필요하다).
