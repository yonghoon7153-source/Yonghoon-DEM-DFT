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

풀이 47인 이유는 **물리 게이트가 아니라 repo 취합 단계 한 곳**이다.
계산은 270/273 완주했고 미취합종도 `STAGE_12.DONE` 까지 찍혀 있다.
`esw_cascade_batch.py` 도 자기 입력을 다 처리했다 — **그 입력
(`cascade_v23_all.csv`) 이 이미 47종이었다.** 회수 비용은 **GPU 0시간**이다.

### 확정된 사슬 (2026-08-13 gabia 실측)

```
273 슬롯 → 270 완주            (As₂S₃ 3만 stage-02 종료)
  ├─ 09f_esw 270/270           ← 캐스케이드 안. 단 이것은 진짜 ESW 가 아니다
  └─ unified_dataset_273.csv   3615행 · 90종 · 5축(UMA·BVSE·anneal·EOS·elastic) 전부
           ↓  ⛔ 여기서 43종이 사라진다 — 계산이 아니라 취합
     cascade_v23_all.csv       2025행 · 47종 · rank_combined==1 → 141행 · ZrCl4 없음
           ↓
     esw_cascade_batch.py      (MP hull, DFT 0건) → oxidation_stability_cascade.json
                                                     Jun 25 11:28 = 스냅샷 날짜 그 자체
           ↓
     cascade_v23_ranked.csv    47행 (ox_V 없으면 행 자체가 안 생김)
           ↓
     풀 = 47
```

**완주 증거**: `ZrCl4_x005` 는 `STAGE_00`–`STAGE_12b` **18개 마커 전부** + 4.5 MB +
`FINAL_RANKING.json`·`dataset.csv`·`dft_inputs`·`predictor` — 취합된 `Al2O3_x005`(5.1 MB)와
구성이 동일하다. **판정 못 한 게 아니라 판정하고도 표에 안 실렸다.**
`As2S3_x005` 만 `STAGE_00/01/02` 3개 · 308 KB — 문서화된 seed 실패가 실물로 재현.

**cascade 관련 zip 은 존재하지 않는다** (gabia 전수 확인 — 아카이브는 전부 MPM/DEM·SDCP).

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

## 병목 확정 — `cascade_v23_all.csv` (2026-08-13)

| 파일 | 내용 | ZrCl₄ · LiBr · Li₂S |
|---|---|---|
| `unified_dataset_273.csv` (run dir) | 3615행 · **90종** · 5축 전부 | 모두 있음 |
| `cascade_v23_all.csv` (`/data/work/repo/db/properties/`) | 2025행 · 고유 dopant 58(=47종 + `+Clrich` 변형) · `rank_combined==1` **141행** | **전부 없음** |
| `oxidation_stability_cascade.json` | **141 항목** · 2026-06-25 11:28 | 없음 |

**ESW 배치는 자기 입력을 100% 처리했다** (141 in → 141 out). 43종은 그 앞,
`cascade_v23_all.csv` 를 만드는 취합 단계에서 사라졌다. 파일 날짜(6/25 11:28)가
canonical 스냅샷 날짜와 같다 — 그날 있던 것까지만 모아 굳었고, 뒤에 끝난
cascade 들이 재취합을 트리거하지 않았다.

### 단일 실패점 — 통합은 자동, **등록은 수동**이었다

`master_batch_273.sh` 마지막 블록:

```python
csvs = sorted(glob.glob('$BATCH_DIR/*/dataset.csv'))   # 270개 cascade
unified = pd.concat(dfs, ignore_index=True)
unified.to_csv('$BATCH_DIR/unified_dataset_273.csv')   # ← 자동
```

반면 `cascade_v23_all.csv` 를 **쓰는 코드는 어디에도 없다** (읽는 것만 3개).
git 로그가 수동 등록의 흔적이다:

```
336cb2e8  register doping cascade results to DB (36 compounds incl. NiO)
c649492f  register cascade: +Al2O3 x002/x005/x010 (39 compounds total)
2c34123e  cascade v23: aggregate 141 done compounds        ← 마지막, 6/29
```

36 → 39 → 141 로 "그때까지 done 인 것" 을 손으로 커밋했고 141(=47종)에서 멈췄다.

| 시각 | 파일 | 내용 |
|---|---|---|
| 6/25 10:58 | `cascade_v23_champions.csv` | 141행 |
| 6/25 11:28 | `oxidation_stability_cascade.json` | 141 항목 |
| **6/29 11:52** | `cascade_v23_all.csv` | 2025행 · 47종 · **수동 등록 마지막** |
| **7/11 23:06** | `unified_dataset_273.csv` | 3615행 · 90종 · **자동 통합, 등록 안 됨** |

**계산이 끝난 것은 7/11 이고 등록이 멈춘 것은 6/29 다 — 12일 차이.**

스키마가 이를 확증한다: U 에만 있는 열이 `composition_Br`·`composition_I`·`composition_N` —
A 에는 그 원소 열 자체가 없다.

### ⚠ 부수 위험 — 47종 값도 옛 세대일 수 있다

A 의 2025행이 U 에 **전부 포함**되지만(A-only 0), 공통 95열 중 **8열의 값이 다르다**
(`bvs_li_proxy_score`·`elastic_poisson_nu`·`screen_dV_over_V0`·`tier2_lattice_angle_dev_deg`·
`bvs_li_std` 등). U 는 **재계산된 세대**다. 즉 지금 db 의 47종 수치도 7/11 판과 다를 수 있고,
`bvs_li_proxy_score` 는 **G4 의 입력**이다. 덧붙이기(merge)가 아니라 **세대 교체**로 가야 하며,
교체 후 G4 통과 명단이 바뀌는지 반드시 대조할 것.

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
