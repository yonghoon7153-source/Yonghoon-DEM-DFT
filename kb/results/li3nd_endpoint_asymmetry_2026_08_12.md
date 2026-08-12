---
title: li3nd NEB 끝점 2.07 eV — 수치 인공물이 아니라 실제 자리 차이
date: 2026-08-12
updated: 2026-08-12
tags: []
status: 진행
confidence: high
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

## 확인 (2026-08-12) — c→c 끝점은 **0 mV**

예측을 그대로 시험했다. 진짜 전도 경로인 `c→c`(3.667 Å, 8c 부격자가 a/√2 = 3.666 Å
로 침투)의 두 끝점을 같은 프로토콜로 독립 이완했다.

```
/data/work/runs/sei_neb_v2_ccpath/li3nd   ep_initial ✓ · ep_final ✓ · Δ끝점 +0 mV
```

**두 끝점이 대칭 등가(둘 다 Wyckoff c)라 에너지가 같아야 하고, 실제로 0 이 나왔다.**
그러므로 앞의 2.07 eV 는 수치 문제가 아니라 **일어나지 않는 홉을 잰 것**이 맞다.

부수 확인: 독립적으로 이완한 두 끝점이 0 mV 안에 들어왔다는 것은 같은 계·같은 k·
같은 수렴 조건에서 계산이 **자기일관적**이라는 뜻이다 — 드리프트나 자기/전자 상태
의존이 있었으면 여기서 수십 mV 가 샌다.

NEB 본체는 진행 중(neb.x 3 프로세스). 대칭 홉이라 Ea 가 모호하지 않다
(비대칭 홉은 정/역 장벽이 달라 어느 쪽을 인용할지가 문제였다).

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
