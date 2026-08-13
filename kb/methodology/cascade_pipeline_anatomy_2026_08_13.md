---
title: cascade 273 캠페인 해부 — 왜 풀이 47인가 (코드 계보 실측)
date: 2026-08-13
updated: 2026-08-13
tags: [cascade, pipeline, provenance, seminar, esw]
status: 확정 — 원인 특정됨 (ESW 배치 커버리지). 회수 경로 있음
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-13
verifiedBy: agent
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

## 요약

풀이 47인 이유는 **물리 게이트도, "3축 완비"도, 취합 순번도 아니다.
`ox_V`/`red_V` 를 만드는 진짜 ESW 배치가 47종만 돌았기 때문**이다.
나머지 다섯 축은 90종 전부 있다. 회수 비용은 **GPU 0시간**이다.

## 코드 계보 (2026-08-13 실측)

스크립트는 이 브랜치에 없다. `origin/claude/unified-2026-05-15` 에 있다:

```
git fetch origin 'refs/heads/claude/unified-2026-05-15:refs/remotes/origin/claude/unified-2026-05-15'
git show origin/claude/unified-2026-05-15:tools/doping/master_batch_273.sh
```

### master_batch_273.sh (v4.5.20) — 바깥 루프

```bash
PHASE_1A=( … 산화물 37종 … )                    # +1(4) +2(8) +3(12) +4(6) +5(4) +6(3)
PHASE_1B=( 불화물10 · 염화물19 · 브롬5 · 요오드4 · 질화5 · 황화11 )   # 54종
ALL_COMPOUNDS=("${PHASE_1A[@]}" "${PHASE_1B[@]}")
for cmp in "${ALL_COMPOUNDS[@]}"; do for conc in x002 x005 x010; do …
```

- **37 + 10 = 47.** 목록이 **계열별 연속 블록**이고 루프가 순차라, 어디서 끊어도
  경계가 계열에 맞아떨어진다. 0/19·0/11 같은 모양은 **이상한 게 아니라 당연**하다.
  물리 게이트였다면 계열 안에서 섞였을 것이다.
- 헤더 실측: per-cascade ~17 h · **1 GPU sequential ~193 days (6.4 months)**.
- 안전장치: 스테이지별 `STAGE_NN.DONE` 마커 resume · `set -uo pipefail`(-e 는 **일부러 뺌**)
  · 24 h timeout · cascade별 로그 · 5-트리거 skip 감지(v4.5.22).

### tier_cascade.sh — 안쪽 20 스테이지

| 스테이지 | 무엇 | 비고 |
|---|---|---|
| 00 preflight | 환경·기준구조 점검 | |
| 01 substitute | 자리 열거 → 후보 구조 | ⚠ `COMPOUND_FILTER` 미설정 시 ~85종 전수 열거 = 5000+ 구조 (문서화된 over-generation bug) |
| 02 screen | UMA relax 1500 steps | |
| 03 winners | 그룹별 승자 | `--max_dv 0.25 --require_converged` |
| 04 anneal | **500 K · 50 ps FIRE** | v4.2 에서 300 K/20 ps 폐기 — kT/Ea 근거 주석 있음 |
| 05 bvse | **어닐 후 기하**로 BVSE | 외부 리뷰 CR-3 반영 (BVS 가 결합길이에 지수민감) |
| 06 rerank | 어닐 후 에너지로 재순위 | |
| 07 eos · 08 elastic | B0 · Cij | |
| 09a–d | combine · collect · train_predictor · dft_inputs | |
| 09e ehull | `--top 10` | |
| **09f esw** | ⚠ **진짜 ESW 가 아니다** | 아래 §핵심 |
| 10 md_sigma | σ_Li MD, `TOP_K_SIGMA` × 3T × 50 ps | ≈12 h |
| 11 ncm adhesion | W_ad | 5–15 h |
| 12 / 12b | collect_final · train_final | |

## 핵심 — stage 09f 는 ESW 가 아니다

`tier_cascade.sh` 주석 원문:

```
# Stage 9f — Competing-phase energy span (qualitative metastability hint).
# NOT a real ESW — real ESW needs Mo 2012 grand canonical method (TODO v5).
# Report this in paper-SI only, NOT main table, NOT as "ESW".
# Skips gracefully if MP_API_KEY not set.
```

**진짜 ESW 는 캐스케이드 밖에 있다.** `oxidation_stability_cascade.csv` 헤더:

> grand-potential ESW per cascade dopant (UMA champion composition, MP GGA_GGA+U hull).
> **Source: `esw_cascade_batch.py` @ gabia**

즉 273 GPU 캐스케이드가 끝난 뒤, 별도 배치가 champion 조성을 MP hull 에 얹어
`ox_V`/`red_V` 를 만들었다. **그 배치가 47종만 돌았다.**

## 축별 커버리지 실측 (gabia `unified_dataset_273.csv`, 3615행)

| 계열 | 종 | UMA screen | BVSE | anneal | EOS | elastic | combined | **ESW** |
|---|---|---|---|---|---|---|---|---|
| Oxides | 37 | 37 | 36 | 36 | 36 | 36 | 37 | **37** |
| Fluorides | 10 | 10 | 10 | 10 | 10 | 10 | 10 | **10** |
| Chlorides | 19 | 19 | 19 | 19 | 19 | 19 | 19 | **0** |
| Sulfides | 10 | 10 | 10 | 10 | 10 | 10 | 10 | **0** |
| Bromides | 5 | 5 | 5 | 5 | 5 | 5 | 5 | **0** |
| Nitrides | 5 | 5 | 5 | 5 | 5 | 5 | 5 | **0** |
| Iodides | 4 | 4 | 4 | 4 | 4 | 4 | 4 | **0** |

- 황화물이 **10종**이다 (명단은 11). 빠진 하나가 As₂S₃ — stage-01 `n_structures = 0`
  정직 종료. **문서화된 seed 실패가 데이터로 정확히 재현된다.**
- `sigma_md_*` 는 **전 계열 0** — 47종도 마찬가지다. σ 는 이 통합표의 축이 아니다.
- 행 대비 축 충족률이 ~20% 인 것은 하류 스테이지가 `--top 10` / `TOP_K_SIGMA` 로
  상위 몇 개만 처리하기 때문이다 (결손이 아니라 설계).

## 그러므로 풀의 정의

`build_screening_funnel.py` `load_pool()` 이 `cascade_v23_ranked.csv` 를 읽고,
그 파일의 열이 `rank, dopant, group, score, de, **ox_V, red_V**, E_GPa, pugh, pareto` 다.
**ESW 없이는 행이 만들어지지 않는다.** 그래서 ranked.csv = 47행 = 풀.

`cascade_screening_funnel.json` 의 `selection_history` 가 적은
*"ESW·탄성·BVSE 3축이 모두 채워진 47종"* 은 **결과적으로는 맞지만 원인을 흐린다** —
탄성·BVSE 는 90종 전부 있었고 실제로 갈린 축은 ESW 하나다.

## 회수 경로 (다음 loop 1순위)

- 필요한 것: champion 조성 + MP hull + `MP_API_KEY`. **GPU 0시간, DFT 0건.**
- 대상: 43종 (염화물 19 · 황화물 10 · 브롬 5 · 질화 5 · 요오드 4).
- 하면: 풀이 **47 → 90** 으로 두 배가 되고, 게이트 감사·Pareto·co-doping 후보군이
  전부 그 위에서 다시 계산된다. 1,081 pair 도 C(90,2) = 4,005 로 바뀐다.
- ⚠ 다만 **G3 문턱 2.14 V 는 host 상대 기준**이라 풀이 바뀌어도 그대로다.
  G5(roster median)와 `transport_norm` 정규화는 풀 의존이라 **다시 계산해야 한다.**

## 반증·한계

- ESW 배치 스크립트(`esw_cascade_batch.py`) 자체는 아직 안 읽었다. 47에서 멈춘 것이
  의도(예산·검토 대기)인지 중단인지는 그 로그를 봐야 한다.
- `unified_dataset_273.csv` 는 gabia 에만 있다. repo 에 없으므로 이 표의 수치는
  2026-08-13 회수 시점 기준이다.
- 축 충족 = **열이 비어 있지 않음**이다. 값의 품질(수렴·이상치)은 따로 봐야 한다.
