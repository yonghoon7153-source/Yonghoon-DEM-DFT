---
title: 캐스케이드 챔피언 슬롯의 조성족 섞임 — Cl-rich 변형이 이름표만 같은 채 앉아 있다
date: 2026-08-16
updated: 2026-08-16
tags: [cascade, esw, oxidation, composition, provenance, b2o3, correction]
status: 확정 — 270 슬롯 전수 분류, 도구 3건·db 4건 반영
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-16
verifiedBy: 우리 repo 전수 재현 (pinned ESW 270행 + cascade CSV 3615행 + b2o3_esw.json 교차)
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

## 요약

캐스케이드의 **챔피언 슬롯은 (도펀트, 농도라벨) 하나당 하나**이고, 그 슬롯은
`combined_score` 최대값이 가져간다. 그런데 후보 풀에는 **같은 도펀트의 두 설계 변형**이
같이 들어 있다:

| 변형 | `charge_compensation` | 음이온 | Li | 조성 예 (B2O3) |
|---|---|---|---|---|
| plain  | `compound_set`       | S17 Cl4 | Li18 | `Li28P2S17Cl4B2O3` |
| Cl-rich| `compound_set_chain` | S16 **Cl5** | Li17 | `Li17B2P4S16Cl5O3` |

Cl-rich 는 **S 하나를 Cl 로 바꾼 것**이다. 그래서 270 슬롯 중 **17개는 이름표만 같고
조성이 다르다**. 그 17행의 `delta_ox_vs_host_V` 는 host(`Li6PS5Cl`) 와의 차이므로
**도펀트 효과가 아니라 (도펀트 + 음이온 치환)의 합**이다.

## 전수 결과

```
host(2.140 V) 초과 비율
  plain  : 17/253 =  6.7%
  Cl-rich: 11/17  = 64.7%     → 9.7배
```

| 종 | plain ox_V | Cl-rich ox_V | 판정 |
|---|---|---|---|
| Al2O3 | 2.140 (=host) | 2.354 | ⛔ Cl-rich 에서만 개선 |
| MoO3  | 2.140 (=host) | 2.356 | ⛔ Cl-rich 에서만 개선 |
| WO3   | 2.140 (=host) | 2.356 | ⛔ Cl-rich 에서만 개선 |
| **B2O3** | **없음** | 2.317 | ⛔⛔ plain 챔피언 자체가 없다 (3점 전부 +Clrich) |
| Sc2O3 | 2.356 | 2.339 | plain 도 개선 — 무관 |
| Y2O3  | 2.282 | 2.282 | 축퇴 — 무관 |
| MgO·ZnO | 2.140 | 2.140 | 둘 다 개선 없음 |
| Nd2O3·Sm2O3 | 1.920 / 1.989 | 1.987 / 2.034 | 둘 다 host 미만 |

Cl-rich 11건이 개선 쪽인데 그 onset 이 **도펀트와 거의 무관하게** 뭉친다
(Al 2.354 · Mo 2.356 · W 2.356 — 화학적으로 완전히 다른 셋이 같은 값).
"이건 도펀트가 아니라 음이온 치환이 만든 값" 이라는 **정황**이지 증명은 아니다 — 아래 참조.

## 제일 비싼 파급: B2O3 의 부호가 뒤집힌다

B2O3 는 우리 **DFT-deep 2종 중 하나**(다른 하나 Nd2O3)다. 그런데:

| 대상 | 조성 | grand-potential onset | host(2.14) 대비 |
|---|---|---|---|
| **DFT-deep 셀** (`b2o3_esw.json`) | `Li58P8S41Cl16B2O3` | **2.03 V** | **−0.11 V (악화)** |
| 캐스케이드 챔피언 (pinned) | `Li17B2P4S16Cl5O3` | **2.317 V** | **+0.177 V (개선)** |

둘 다 grand-potential ESW · MP GGA_GGA+U · chemsys `B-Cl-Li-O-P-S` · **346 entries**,
host 값도 양쪽 2.14 로 일치한다 → **방법 차이가 아니라 순전히 조성 차이**이고 **부호가 반대**다.

세미나 표에서 B2O3 만 `dft_deep=1` 이면서 onset 이 Cl-rich 유래였다.
"우리가 DFT 로 깊이 본 종이 산화 창을 넓힌다" 는 문장은 **두 조성을 이어붙인 것**이라
성립하지 않는다.

- ⛔ 금지: "B2O3 가 산화 onset 을 +0.177 V 올린다"
- ✅ 허용: "Cl-rich chain 변형 `Li17B2P4S16Cl5O3` 의 onset 은 2.317 V 로 host(2.14 V)보다 높다.
  DFT-deep 셀 `Li58P8S41Cl16B2O3` 의 onset 은 2.03 V 로 host 보다 낮다."

## 안 무너지는 것

- **최종 생존자 WO3** 는 pool ox_V 가 **plain 챔피언 값(2.140)** 이다 — 오염 아님.
- Y2O3 는 두 족의 onset 이 **같아서**(2.282) 라벨이 아무 혼동을 만들지 않는다 (`degenerate`).
- 47종 pool 중 오염은 **B2O3 단 1건** (`ox_family_confounded=1`). 43 plain · 3 degenerate.
- G3 통과/탈락 집계와 캐스케이드 깔때기 숫자는 그대로다 — 바뀐 건 **B2O3 한 행의 해석**이다.

## 반영 (도구 3 · db 4)

| 대상 | 조치 |
|---|---|
| `tools/oxidation/esw_cascade_batch.py` | `classify_family()` + `annotate_families()`; 정상 실행에 상시 포함, MP 없이 기존 출력에 입히는 `--annotate`, `--selftest` 28건(음성 9건) |
| `tools/cascade/build_screening_funnel.py` | G3 에 `composition_family_caveat` (G1·G5 엔 이미 있었는데 **정작 산화 게이트엔 없었다**), pool 행에 `ox_composition_family` 옮겨싣기 |
| `tools/figures/plot_cascade_seminar_47.py` | `ox_composition_family()` 해석 + CSV 3열 추가 + 그림 각주 2개 + **오염 집합이 `['B2O3']` 에서 바뀌면 실패하는 assert** |
| `db/.../oxidation_stability_cascade_v3_pinned.json` | 행마다 `composition_family`·`delta_ox_vs_host_V_confounded`·`comparable_to_plain_champions`, 최상위 `composition_family_audit` + `dft_deep_composition_collision` |
| `db/properties/b2o3_esw.json` | `composition_collision_2026_08_16` |
| `db/.../cascade_seminar_oxidation_transport_47.csv` · `_scorecard_47.csv` | `ox_composition_family` 등 3열 |
| `db/properties/cascade_screening_funnel.json` | pool 행 3필드 + G3 caveat |

판별자는 **CSV 의 `charge_compensation`** 이다. `dopant` 라벨의 `+Clrich` 접미사는
거울일 뿐이라 둘이 어긋나면 `family_label_inconsistent` 로 남긴다 (현재 0건).
모르는 `charge_compensation` 값은 **plain 으로 흘려보내지 않고** `unknown` 으로 떨어뜨린다.

## 반증·한계

- **분해를 못 한다.** Cl-rich 행의 Δ 를 (Cl 치환분) + (도펀트분) 으로 나누려면
  **도펀트 없는 Cl-rich 기준**(`Li_x P4 S16 Cl5`)을 같은 phase set 안에서 재야 하는데,
  그건 **어느 phase set 에도 없다**. 현재 판정은 "섞였다" 까지이고 "Cl 때문이다" 는 아직 아니다.
  → 남은 일: host 처럼 Cl-rich 기준도 모든 chemsys 안에서 같이 재는 실행 1회(MP만 필요, DFT 불필요).
- Al/Mo/W 의 Cl-rich onset 이 2.354–2.356 로 뭉치는 건 **정황**이다. 다만 plain Sc2O3 도
  2.356 이라 그 값이 Cl-rich 전용 지문은 아니다. onset 반응식을 보면 2.35 군은 `P2S7`,
  2.140 군은 `Li3PS4` 가 생성물인데 — 그 해석은 **하지 않았다**(반응식 몇 개만 읽은 것).
- 이 카드는 **산화 onset 축만** 본다. de(G1)·E/GB(G5) 는 3점 평균이라 조성족이 **행 안에서**
  섞여 있고(그건 funnel 의 G1·G5 caveat 에 이미 적혀 있다), 그쪽 파급은 재지 않았다.
- x 라벨(x002/x005/x010)이 농도가 아니라는 기존 경고는 그대로다 — 실측은 셋 다 x=0.25.

## 출처

- `db/properties/cascade_v23_all.csv` (3615행, `charge_compensation` 3105 plain / 510 chain)
- `db/properties/oxidation_stability_cascade_v3_pinned.json` (270 챔피언 + 84 host)
- `db/properties/b2o3_esw.json` (2.03 V, ocv_decomp 의 `16 LiCl` 로 조성 역산)
- 관련: `kb/methodology/cascade_pipeline_anatomy_2026_08_13.md` (G3 phase_set 폐쇄)
