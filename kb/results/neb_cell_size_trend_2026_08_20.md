---
title: "NEB 셀 크기 추세 — 작은 셀이 장벽을 1.3~3.3배 부풀린다 (UMA 정찰 6홉/4화합물)"
date: 2026-08-20
updated: 2026-08-20
tags: [neb, uma, cell-size, finite-size, sei, li3p, li2o, licl, li3po4]
status: 측정완료
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-20
verifiedBy: gabia UMA 정찰 12런 (tools/sei/build_neb_inputs.py --uma_scout) → db/properties/sei_neb_uma_scout.json
explored: false
authoredBy: agent
effort: medium
claimType: empirical
evidenceScope: multi-source-primary
---

# NEB 셀 크기 추세 — 작은 셀이 장벽을 부풀린다

> **한 줄**: 같은 홉·같은 엔진에서 `1×1×1 → 2×2×2` 로 키우면 장벽이 **예외 없이 내려간다**
> (6홉 / 4화합물, **1.32–3.24배**). ⇒ **`sei_neb_v2_cc333`(107원자) 의 2.56 eV 가
> `ccpath`(31원자) 의 0.229 보다 큰 것은 "미수렴" 말고 설명이 남지 않는다.**
> ⚠ UMA 값이다 — **장벽 절대값은 인용 금지**, 읽는 것은 **같은 엔진 안의 셀 의존성**뿐이다.

## 1. 값 (전수)

`db/properties/sei_neb_uma_scout.json` · UMA-s-1p1(omat) · 중성 공공 · 끝점 **한 번 이완**

| 계 | 공간군 | 홉 | d (Å) | 1×1×1 | **2×2×2** | 비 | 끝점차 |
|---|---|---|---|---|---|---|---|
| **li2o** (n=3) | Fm-3m | c-c | 2.310 | 0.648 | **0.270** | **2.40×** | −0 → +0 meV ✅ |
| **li3p** (n=8) | P6₃/mmc | **f-f** | 2.510 | 0.287 | **0.088** | **3.24×** | +0 → −0 meV ✅ |
| li3p | P6₃/mmc | b-f | 2.745 | 0.237 | 0.118 | 2.01× | −67 → **−273 meV** ⚠ |
| **li3po4g** (n=32) | Pnma | d-d | 3.049 | 0.666 | **0.463** | 1.44× | +4 → −0 meV ✅ |
| li3po4g | Pnma | c-d | 2.692 | 0.545 | 0.414 | 1.32× | −192 → **−205 meV** ⚠ |
| **licl** (n=8) | Fm-3m | a-a | 3.641 | 0.686 | **0.491** | 1.40× | −0 → +0 meV ✅ |

**예외 0/6.** 대칭 홉(끝점차 ≈ 0)만 보면 4/4 이고 비는 1.40–3.24배.

## 2. 이게 무엇을 정하나

### 2-1. ⭐ `cc333` 논쟁의 **방향**을 정한다
| 런 | 원자 | 수직폭 | Ea | 상태 |
|---|---|---|---|---|
| `sei_neb_v2_ccpath` | 31 | 8.47 Å | **0.2290** | 58 iter 수렴 |
| `sei_neb_v2_cc333` | 107 | **12.70 Å** | 2.5616 | **iter 11 미수렴** (error 0.46 eV/Å) |

셀을 키우면 장벽이 **내려간다**가 6/6 인데 cc333 이 **위에** 있다.
⇒ **2.56 은 값이 아니라 미수렴 상태의 스냅숏**이라는 해석이 강하게 지지된다.
수렴하면 **0.229 이하**로 내려와야 정합적이다. 그렇지 않으면 이 추세의 반례이므로
**그때 다시 논증해야 한다**(반증 가능한 예측).

### 2-2. Li₃P 는 큰 셀에서 **매우 빠르다** — 계면 작업에 직접 걸린다
`f-f ×(2,2,2) = 0.088 eV`. Lai 2025(HAML) 이 Li|LPSCl 계면의 주 생성물로 지목한 상이고,
우리 grand-potential 예측(LPSCl1.6 @0 V → Li₃P + LiCl + S)과도 일치한다.
`kb/results/uma_force_accuracy_li3ps4_2026_08_19.md` §5-4 에서 **Li₃P 잔여력 1차 통과**
(MP 이완점에서 UMA fmax 0.0205 eV/Å)를 확인했으므로, 이 값은 **경로 선택 근거**로 쓸 수 있다.
⛔ **장벽 절대값은 못 쓴다** — Li₃Nd 에서 UMA 는 c–c 를 **1.76배 과대**했다(0.403 vs DFT 0.229).

### 2-3. 우리 문턱(`MIN_WIDTH_A = 10.0`)이 보수적이지 않다
`ccpath` 의 수직폭 **8.47 Å** 는 문턱 아래이고, 위 표의 1×1×1 들은 그보다도 작다.
1.3–3.3배라는 크기는 **문턱을 넘겼다고 안전한 게 아님**을 뜻한다 —
`argyrodite_cage_neb.py` 의 10 Å 는 **최소 요건이지 수렴 보증이 아니다.**

## 3. ⚠ 약한 곳 (지우지 말 것)

1. **정찰은 끝점을 한 번만 이완한다** — 코드 재독 확인
   (`build_neb_inputs.py:815` 이 `relax_positions` 를 쓴다. `relax_endpoint_deep` 은
   2026-08-19 밤에 만들어져 정찰에 안 들어갔다).
   ⇒ ⚠ 두 줄(li3p b-f, li3po4g c-d)의 **끝점 비대칭이 셀을 키울수록 커지는 것**
   (−67 → −273 meV)은 유한크기로 설명되지 않는다(보통 **줄어야** 한다).
   comp1 에서 잡은 **얕은 분지 착지**(55 meV 회수)와 같은 서명이므로,
   **그 두 줄은 심화 이완 + 홉 추적 가드로 재실행해야 한다.**
   ⭕ 다만 **대칭 홉 4개(li2o·li3p f-f·li3po4g d-d·licl)는 끝점차 ≈ 0 이라 이 의심이 안 붙는다**
   — 셀 추세의 골자는 그 4개만으로도 선다(1.40–3.24배).
2. **b 와 f 는 서로 다른 Wyckoff 자리**다(Li₃P 는 Li orbit 2개). 그러니 b-f 의 끝점차는
   **일부가 진짜 자리 에너지 차**다 — 전부가 인공물이라는 뜻이 아니다.
3. **전하 취급이 DFT 와 다를 수 있다.** 정찰은 **중성 공공**인데 우리 DFT 규약은
   `electronic_class` 로 갈린다(절연체 = V_Li⁻ + jellium / 금속 = 중성).
   ⇒ UMA↔DFT 비교(예: Li₃Nd 1.76배)에는 이 항이 섞여 있을 수 있다.
   **셀 추세 자체는 UMA 내부 비교라 이 문제에 면역이다.**
4. **2점(1×1×1, 2×2×2)뿐이라 수렴을 못 본다.** 2×2×2 가 수렴값인지, 더 키우면 더 내려가는지
   모른다. 추세의 **방향**은 6/6 으로 단단하지만 **크기**는 상한이 아니다.
5. **UMA 값이다.** DFT 로 같은 추세가 나오는지는 미확인 — 그게 `cc333` 이 답할 것이다.

## 4. 출처

- 값: `db/properties/sei_neb_uma_scout.json` (12건)
- 도구: `tools/sei/build_neb_inputs.py --uma_scout` (엔진 조각은 `argyrodite_cage_neb.py` 재사용)
- 관련: `kb/results/uma_force_accuracy_li3ps4_2026_08_19.md` §5-4 (Li₃P 잔여력)
- 리뷰: `kb/reviews/codex_B_neb_md_tools_2026_08_20.md` §1-1 · §5(B-R5, B-R6)
- 계면 맥락: `litdb/papers/lai2025_haml_li_metal_lpscl_interface_doping_seFO.md`
