---
title: b2o3 아레니우스가 800 K 위에서 굽는다 — 단일 Ea 를 철회한다
date: 2026-08-23
updated: 2026-08-23
tags: [b2o3, md, arrhenius, multiseed, retraction]
status: 판정완료
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-23
verifiedBy: "3시드 D 를 구간별로 재적합 + 인공물 가설 3개를 각각 실측으로 반증 (β 게이트 · MSD 창 스캔 · 궤적 골격 배위수)"
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

# b2o3 아레니우스 굽음 (2026-08-23)

## 한 줄

**600–1000 K 를 하나의 Ea 로 기술하지 않는다.** 600→800 구간 0.222 eV,
800→1000 구간 **0.077 eV** — 145 meV 차이다. 굽음은 실재하며 측정 인공물이 아니다.

## 실측

3온도 × 3시드 (고온 6런은 2026-08-21 재시드분, `A-highT-reseed-traj` 복원분):

| T | 시드별 D (cm²/s) | 평균 |
|---|---|---|
| 600 K | 7.981 / 13.043 / 10.211 e-06 | 1.041e-05 |
| 800 K | 2.741 / 2.750 / 3.641 e-05 | 3.044e-05 |
| 1000 K | 3.720 / 4.403 / 3.305 e-05 | **3.809e-05** |

```
600→800   2.92배 빨라짐   구간 Ea 0.2219 eV
800→1000  1.25배 빨라짐   구간 Ea 0.0773 eV   ← 거의 안 빨라진다
```

★ **세 시드 모두 같은 경향**이다 (1000/800 비 1.09 · 1.22 · 1.45). 한 시드의 사고가 아니다.

대조: modelc 800→1000 은 2.46배, LPSOCl 은 2.36배로 정상이다.
LPSOCl 만 두 구간 Ea 가 0.279 / 0.296 로 **17 meV 차** — 유일하게 직선이다.

## 인공물 가설 셋을 전부 반증했다

| 가설 | 검사 | 결과 |
|---|---|---|
| ① β 게이트 실패 | `msd_diffusive_check --scan --average --mto` | ⛔ 반증 — **6/6 확산 영역** |
| ② MSD 창 포화 | 창 스캔 2-50 / 10-50 / 25-100 | ⛔ 반증 — m **2.678 → 2.784 (+4 %)**, 포화면 떨어져야 한다. c 는 +3.41 → −0.72 로 **줄어든다**(sub-diffusion 이면 커져야 한다) |
| ③ 1000 K 구조 붕괴 | 궤적 첫/끝 프레임 P 배위수 | ⛔ 반증 — **8/8 CN=4**, 시작=끝 완전 동일 |

③ 의 실물 (s2, T1000, 100 ps):
```
PS₄ × 6 · PS₃O × 1 (P92) · PS₂O₂ × 1 (P29)     시작 = 끝
```
O 치환 형태도 b2o3 도핑이 만들어야 할 바로 그것이다. 해리된 P 가 하나도 없다.

⚠ 첫 검사는 **P–S 만 세도록 잘못 짜여** 5~6/8 로 나왔다 (P–O 결합을 놓쳤다).
   b2o3 는 B₂O₃ 를 넣은 계라 P 가 O 와도 결합한다 — ELF 작업의 `PS₃O` 가 그것이다.
   다만 그 잘못된 판에서도 **시작 = 끝**은 같았으므로 "변화 없음" 결론은 그때도 유효했다.

⇒ 남는 설명은 **물리적 포화**다. 800 K 위에서 Li 확산이 상한에 닿는다.

## 철회

⛔ **기존 `Ea_eV_PAPER_SUPERSEDED_600K_only = 0.206 (+0.038/−0.030)` 을 철회한다.**

그 값은 600 K 3시드 + **단일시드 고온 앵커**로 냈다. 그 단일시드 1000 K 는 5.067e-05 로
3시드 평균 3.809e-05 보다 **33 % 높다** — 운 좋게 높은 시드였고, 그것이 굽음을 가려
직선처럼 보이게 했다. 그 앵커로 재면 800→1000 구간 Ea 가 0.180 eV 로 나와
600→800 의 0.222 와 가까워 보인다. 3시드로 제대로 재니 0.077 로 드러났다.

⛔ 2026-08-23 에 새로 계산한 3×3 단일 적합 **0.1732 eV 도 쓰지 않는다** — 굽은 곡선에
   억지로 그은 직선이라 두 구간의 어중간한 평균일 뿐이다 (R² 0.9533).

## 쓸 수 있는 것

✅ **600→800 구간 Ea = 0.222 eV**

흥미롭게도 이 값은 원래 단일시드 값 0.2234 와 거의 같다. 즉 저온 구간은 처음부터
맞았고, 1000 K 를 끼워 넣으면서 값이 망가진 것이다.

## 원고 문장 (그대로 쓸 수 있게)

> The Arrhenius plot of b2o3 curves above 800 K. The apparent activation energy is
> 0.222 eV over 600–800 K and drops to 0.077 eV over 800–1000 K. All three seeds show
> the same trend (D(1000 K)/D(800 K) = 1.09–1.45). We found no evidence of a measurement
> artifact: all six high-T runs pass the diffusive gate, the MSD fit window scan shows a
> constant slope (m +4 % from the 2–50 ps to the 25–100 ps window), and the framework
> coordination is unchanged over the 100 ps run (8/8 P remain four-coordinate). We
> therefore do not report a single activation energy for the full 600–1000 K range.

## 이 카드가 못 하는 것

- **왜 포화하는지 말하지 않는다.** "800 K 위에서 상한에 닿는다" 는 관찰이고,
  기구(Li 부격자 완전 융해 / 골격이 정하는 상한 / 다른 것)는 규명하지 않았다.
- 1000 K 위를 안 봤다. 1200 K 를 보면 정말 평평한지, 아니면 다시 오르는지 갈린다.
- modelc 도 102 meV 굽었다 — 같은 검사를 안 했다. 600 K 가 단일시드라 먼저 채워야 한다.
- σ(300 K) 재계산을 아직 안 했다. Ea 가 바뀌었으므로 반드시 다시 내야 한다.

## 근거

`db/properties/b2o3_md_arrhenius.json` (600 K 3시드) ·
`gabia/kgy:/home/kgy/work/runs/highT_reseed_traj/b2o3/s{2,3,4}/**/T{800,1000}` (고온 3시드) ·
`tools/ionic/msd_diffusive_check.py --scan --average --mto`
