---
title: cascade 273 캠페인 해부 — 왜 풀이 47인가 (코드 계보 실측)
date: 2026-08-13
updated: 2026-08-19
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
git show origin/claude/unified-2026-05-15:tools/doping/master_batch_273.sh   # lint-skip-path (이 브랜치엔 없음)
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

## 회수 1차 실행 결과 (2026-08-13)

`esw_cascade_batch.py --csv unified_dataset_273.csv` → **270 champion 처리 완료**
(`oxidation_stability_cascade_v2.json`). GPU 0시간, DFT 0건, MP hull 만.

| 검증 | 결과 |
|---|---|
| **세대 드리프트** | 옛 141개 (종,농도) 쌍 전부 매칭 · **ox_V 변경 0건** → 회수는 **순수 확장** |
| 회수 43종의 G3 | **21종이 ox_V ≥ 2.14** (LiBr·LiCl·LiI·Li₂S·CaS·MgS·MgCl₂·MgBr₂·MgI₂·CaCl₂·CaBr₂·AlCl₃·AlI₃·Al₂S₃·Ga₂S₃·ScCl₃·YCl₃·SiS₂·SnS₂·GeS₂·CrCl₃) |
| 탈락 22종 | AlBr₃·AlN·BaCl₂·Ca₃N₂·FeCl₃·GaCl₃·GaN·HfCl₄·LaCl₃·Li₃N·Mg₃N₂·Na₂S·NaI·NbCl₅·NdCl₃·Sb₂S₃·SmCl₃·SrCl₂·TaCl₅·TiCl₄·ZrBr₄·ZrCl₄ |

**LiBr = LiF = Li₂O = CaF₂ = CaO = 2.14 / 1.242 / win 0.898** — 한 자리도 안 다르다.
"LiBr 은 왜 없나" 의 답은 **"있었으면 LiF 와 같은 등급"** 이다.

### 신규 관측 — onset 은 음이온이 아니라 **양이온**이 정한다

| | ox_V | |
|---|---|---|
| Ga₂O₃ | 2.356 | 기존 |
| **Ga₂S₃** | **2.356** | 회수 신규 |
| Al₂O₃ | 2.354 | 기존 |
| **Al₂S₃** | **2.356** | 회수 신규 |

같은 M³⁺ 이면 O든 S든 onset 이 같다. 기존 그림 캡션의 *"6 exceptions = all trivalent
**oxides**"* 는 산화물만 본 표본 효과였다. 회수분이 그 대조군을 제공했다.

⚠ **"6종 → 11종" 으로 쓰면 안 된다.** 값이 하나도 안 바뀌었으므로 Al₂O₃·MoO₃·WO₃ 는
옛 데이터에서도 이미 2.14 위였다. 그림의 "6" 은 `cascade_v23_ranked.csv` 의 **도펀트별
집계값** 기준이고 위 21/11 은 **(종,농도) 최대값** 기준 — 다른 통계다. 같은 집계로
비교하려면 ranked.csv 를 재생성한 뒤에 다시 세야 한다.

### 회수 체인의 남은 블로커

```
cascade_v23_champions.csv (141행 → 270행 재생성 필요)
oxidation_stability_cascade.csv (_v2.json → CSV 변환 필요)
        ↓ tools/figures/plot_cascade_insights.py:145   ← ranked.csv 는 여기서 나온다
cascade_v23_ranked.csv
        ↓ tools/cascade/build_screening_funnel.py
cascade_screening_funnel.json
```

`plot_cascade_insights.py` 의 `parse()` 가 **산화물/불화물만 가정**하고 있었다
(ZrCl₄ → "F"·원자가 1). 2026-08-13 수정 + selftest 15케이스.

## stage 10(σ MD) · 11(W_ad) 는 **미실행**이다 — 미수확이 아니다 (2026-08-13 확인)

`unified_dataset_273.csv` 에서 `sigma_md_*`·`wad_*` 가 전 계열 결측이라
"수천 GPU-시간이 수확 안 됐나" 를 의심했으나, 실측은 그 반대다:

| | |
|---|---|
| `10_md_sigma` 디렉터리 | **5 / 270** (옛 시험런 잔재) |
| `11_*` 디렉터리 | **0 / 270** |
| `STAGE_10.DONE` · `STAGE_11.DONE` | **각 0** |
| 개별 `dataset.csv` 의 sigma·wad 열 | **0/20 행** |

`TOP_K_SIGMA=0` 으로 꺼서 돌렸다 (비용). **비용 산정도 이걸로 맞는다** — 헤더의
"~17 h/cascade · 193 days" 는 σ·W_ad 를 **켰을 때** 추정이고, 실제는 5/26 시작 →
7/11 통합 = 46일에 273개 = **cascade 당 ~4 h**. 17 h − σ 12 h ≈ 4 h 로 정합.

⚠ **총 투입은 ~1,100 GPU-시간이지 4,600 시간이 아니다** (2026-08-13 정정).

**함의**: cascade 어디에도 MD σ 가 없다. G4 의 `transport_norm` 은 영구적으로
**정적 BVSE 프록시**이며, "BVSE 를 전도도라 부르지 않는다" 는 단서는 회수로 없앨 수 있는
것이 아니라 **새 계산이 필요한 항목**이다. 세미나의 그 방어선은 유지된다.

## ★ co-modification 선례가 이미 데이터에 있다 (2026-08-13)

`oxidation_stability_cascade_v2.json` 을 plain champion vs `chain_Cl` champion 으로 갈라
비교했다. `chain_Cl` = cascade Type-C 사슬로 **Cl seed 를 추가로 넣은 구조**.

| dopant | plain | +Clrich | Δ (V) | 부류 |
|---|---|---|---|---|
| **WO₃** | 2.140 | **2.356** | **+0.216** | 천장까지 도약 |
| **MoO₃** | 2.140 | **2.356** | **+0.216** | 천장까지 도약 |
| **Al₂O₃** | 2.140 | **2.354** | **+0.214** | 천장까지 도약 |
| Nd₂O₃ | 1.920 | 1.987 | +0.067 | 오르지만 host 미만 |
| Sm₂O₃ | 1.989 | 2.034 | +0.045 | 오르지만 host 미만 |
| ZnO · MgO | 2.140 | 2.140 | 0.000 | 안 움직임 |
| Y₂O₃ | 2.282 | 2.282 | 0.000 | 이미 천장 위 |
| Sc₂O₃ | 2.356 | 2.339 | **−0.017** | 이미 천장, 오히려 손해 |

(B₂O₃ 는 chain_Cl 챔피언만 있어 비교 불가. chain_Cl 챔피언 17개 · 10종.)

**규칙**: Cl 단독으로는 S²⁻ 핀(2.14)을 못 깬다(ZnO·MgO 무변화). 양이온 단독으로도 못 깬다
(W·Mo·Al plain = 2.140). **둘이 같이 있어야** 2.35 천장에 닿는다. 그리고 이미 천장에 있는
Sc₂O₃ 는 Cl 을 더하면 **잃는다**(−0.017) — "많이 넣을수록 좋다" 가 아니다.

**천장 2.35–2.36 은 M³⁺ 단독군(Sc·Cr·In·Ga·Y·B, +회수 Ga₂S₃·Al₂S₃)이 도달하는 값과 같다.**
즉 서로 다른 경로로 같은 한계에 수렴한다 — 새 산화-제한 반응이 S²⁻ 를 대체한 지점.

### 한계

- n=9 (비교 가능한 종). 큰 도약은 **3종뿐**이고, 회수 43종은 chain_Cl 변형이 없어 이 표를
  넓히지 못한다 (내가 "3 → N 으로 늘 것" 이라 예상한 것은 **틀렸다**).
- `chain_Cl` 은 같은 cascade 안의 **Cl seed 추가**지 별도 화합물과의 명시적 공동치환이 아니다.
  "co-doping 계산" 이 아니라 "**co-modification 선례**" 로 인용할 것.
- 옛 `oxidation_stability_cascade.csv` 의 `clrich_ox_V` 열이 정확히 이 3종만 담고 있었다 —
  즉 이 관측 자체는 6/25 판에도 있었고, 아무도 전면에 안 꺼냈을 뿐이다.

## ⛔ 등록이 멈춘 진짜 이유 — 미푸시 브랜치 (2026-08-13 census)

gabia 체크아웃 전수 조사에서 나왔다. cascade 작업 디렉터리 `/data/work/repo` 는
**우리 브랜치가 아니다**:

| 체크아웃 | 브랜치 | 최종 커밋 | db/properties |
|---|---|---|---|
| `/root/Yonghoon-DEM-DFT` | claude/friendly-meitner-lldvar | 2026-08-13 | **206개 · 11 M** (정본) |
| `/root/work/Yonghoon-DEM-DFT` | b2o3run | 2026-07-18 | 98개 · 3.8 M |
| `/data/work/b2o3md` | claude/friendly-meitner-lldvar | 2026-06-30 | 52개 · 3.1 M |
| **`/data/work/repo`** | **claude/configure-spawn-halogen-lithium-TjDCB** | **2026-06-29** | **17개** (cascade 전용 sparse) |
| `/data/work/repo_dos` | claude/friendly-meitner-lldvar | 2026-06-15 | 13개 |
| `/data/work/v30u_ensemble/Yonghoon-DEM-DFT` | claude/dft-script-generator-webapp-GPSAG | 2026-03-26 | — |

그리고 그 브랜치의 **원격 tip 은 2026-06-16** (`a90fd1cf`) 인데 gabia 로컬은 6/29 다.
등록 커밋 3개(`336cb2e8` 36종 → `c649492f` 39종 → `2c34123e` 141종)는
**이 repo 의 어느 브랜치·어느 커밋에도 존재하지 않는다** (`git cat-file -e` 전부 실패).

**`cascade_v23_all.csv` 는 우리 repo 이력에 단 한 번도 없었다.** 풀 47종을 정의하는 그 파일이
gabia 디스크 한 곳의 **미푸시 커밋 안**에만 있다. 우리 `db/properties/` 의 cascade_v23_*
파일들(champions·ranked·litransport·themes·synergy·eos_refit)은 그 브랜치에서 **손으로 복사해
온 산물**이고, 원본 all.csv 는 따라오지 않았다.

→ 6/29 에 등록이 멈춘 것은 "사람이 잊어서" 가 아니라 **그 브랜치 자체가 그날 버려졌기 때문**이다.
7/11 에 계산이 끝났을 때 등록할 브랜치가 이미 없었다.

**보존 조치 필요**: `git bundle create` 로 미푸시 커밋을 파일화할 것 (인증 불필요).

## 아직 안 본 것 — census 가 드러낸 규모

`/data/work/runs` 총 **479 GB**. 이번 조사에서 본 것은 `multi_category`(1.3 G)·`sei_*`·`sdcp_v2` 뿐.

| 미조사 | 크기 |
|---|---|
| `sdcp_linio2_binding` | 165 G |
| `/data/work/bml` | 155 G |
| `li_neb_diffusion` | 86 G |
| `comp2_elastic_{uspp,dft,k444,0p01,lobster,relax}` | 합 ~63 G |
| `nd_doped_modelc` | 53 G |
| `lpsocl_{dft,elf,bader}` | 45 G |

**cascade 에서 확인된 병(계산 완료 ↔ 정본 미등록)이 이 종목들에도 있는지는 미검**이다.
1 MB 이상 필터로는 안 잡힌다 — cascade 의 `oxidation_stability_cascade.json` 도 71 KB 였다.

## ★ 농도축은 존재한다 — `dualx_v23` (2026-08-13 발견)

`/data/work/runs/dualx_v23` (68 MB · 20 dirs). **x002/x005/x010 이 전부 x=0.25 로 뭉개진
그 버그를 고친 판**이 이미 돌아 있었고, 등록되지 않았다.

```bash
# run_dualx.sh / run_dualx_highx.sh — 우리 repo tools/doping/ 에 있다
env COMPOUND_FILTER=$cmp X_COMPOUND=0.0625 bash tier_cascade.sh <cif> $OUT 5 2,2,1 0
env COMPOUND_FILTER=$cmp X_COMPOUND=0.25   bash tier_cascade.sh <cif> $OUT 5 2,2,1 0
```

- **`2,2,1` 슈퍼셀** (16 f.u.) — 하드코딩 `1,1,1` 이 아니다. `hard_dopant_handling_protocol.md`
  의 처방(2,2,1 → actual x 0.0625)과 정확히 일치.
- `actual_x` 실측 **0.0625 · 0.25** 두 값만 존재 — 진짜 두 농도다.
- 대상 10종: Sc₂O₃·Gd₂O₃·Cr₂O₃·Y₂O₃·La₂O₃·HfO₂·Ta₂O₅·Nb₂O₅·V₂O₅·TiF₄
- **stage 04(anneal)에서 의도적으로 kill** — 스크립트가 `STAGE_04.DONE` 보고 `kill -TERM`.
  중단이 아니라 설계(싸게 보려고). 20/20 이 04 까지 완주, 05 는 13, 06 은 10.
- 헤더 명시: *"Purpose: apples-to-apples **blocking_fraction** comparison ... in an identical cell"*
  → **원래 목적이 G4 축의 농도 응답**이었다. 형성에너지는 부산물.
- 헤더가 한계도 자백: *"the typeA_cluster structure-gen bug is left AS-IS on purpose,
  so both concentrations sample structures identically"*.

### 형성에너지의 농도 응답 — sub-linear

| species | x=0.0625 | x=0.25 | 비 (high/low) |
|---|---|---|---|
| Gd₂O₃ | −0.6391 | −1.2951 | 2.03 |
| Nb₂O₅ | −0.5789 | −1.0186 | 1.76 |
| V₂O₅ | −0.5767 | −0.9671 | 1.68 |
| La₂O₃ | −0.5474 | −0.9219 | 1.68 |

같은 셀에 unit 이 1 → 4 로 **4배**인데 ΔE/atom 은 **1.7–2.0배**. 순수 가산이면 4배여야 한다.
→ **도펀트–도펀트 상호작용이 반발적이고, 안정화 이득은 농도에 대해 포화한다.** 4종 4/4 일치.

⚠ n=4 (두 농도가 다 있는 종). UMA 상대값이고 어닐까지만 — ESW·탄성·BVSE 는 없다.
"농도 의존 **산화안정성**" 은 여전히 말할 수 없다. 말할 수 있는 것은 형성에너지의 농도 응답까지.

## ★★ G4 의 농도 의존 — 발표 P11 을 직접 건드린다 (2026-08-13)

`dualx_v23` 의 원래 목적이 이것이었다 (`run_dualx_highx.sh` 헤더: *"apples-to-apples
blocking_fraction comparison at x=0.25 vs x=0.0625 in an identical cell"*).
값은 `02_screen/uma_results.json` → `uma_relaxed.tier2.dopant_blocking_fraction`.

| species | min 0.0625 | min 0.25 | mean 0.0625 | mean 0.25 |
|---|---|---|---|---|
| HfO₂ | 0.093 | 0.362 | 0.137 | 0.481 |
| La₂O₃ | 0.144 | 0.514 | 0.231 | 0.650 |
| Gd₂O₃ | 0.167 | 0.542 | 0.243 | 0.657 |
| **Y₂O₃** | 0.175 | 0.583 | 0.245 | 0.680 |
| **Sc₂O₃** | 0.189 | 0.597 | 0.253 | 0.674 |
| **Cr₂O₃** | 0.211 | **0.667** | 0.261 | 0.750 |
| Nb₂O₅ | 0.229 | **0.729** | 0.325 | 0.816 |
| Ta₂O₅ | 0.229 | **0.698** | 0.317 | 0.812 |
| TiF₄ | 0.237 | **0.860** | 0.249 | 0.874 |
| V₂O₅ | 0.260 | **0.750** | 0.340 | 0.849 |

**10/10 일치 (min·mean 둘 다).** G4 문턱은 `blocking < 0.60`:

- **x = 0.25** → min 기준 5종 탈락 · mean 기준 8종 탈락
- **x = 0.0625** → **10종 전부 min ≤ 0.260**, 문턱 근처에도 안 간다

그리고 **47종 캠페인은 전부 x = 0.25 에서 돌았다** (의도는 2·5·10%, 슈퍼셀 버그로 0.25 고정).
6.25% 는 의도 범위 안이다.

→ **G4 는 아무도 선택하지 않은 농도에서 발화한 게이트일 가능성이 있다.**
표에 든 Cr₂O₃·Sc₂O₃·Y₂O₃ 는 "산화 onset 이 오른 6종" 중 셋이며, Cr₂O₃ 는
0.25 에서 0.667(탈락) → 0.0625 에서 **0.211**(여유 통과)이다.

### P11 문장 수정 필요

| 현행 | 정직한 판 |
|---|---|
| "산화 개선 6종이 **전부** G4 에서 멈춘다" | "**x = 0.25 에서는** 전부 멈춘다. 그 농도는 의도된 값이 아니었고, 6.25% 에서 잰 10종은 전부 문턱에서 멀다" |

### 한계 (반드시 병기)

- "많이 넣으면 더 막는다" 자체는 자명하다. 발견은 그게 아니라 **게이트가 실질적으로 작동한
  농도가 사고로 정해졌다**는 것이다.
- `blocking_fraction` 은 UMA 기하의 **정적 프록시** — 전도도가 아니다 (기존 단서 유지).
- G4 = `transport_norm > 0.30` **AND** `blocking < 0.60`. 여기서는 **blocking 만** 봤다.
  `transport_norm` 은 BVSE(stage 05) 산출이고 dualx 는 14/20 만 있어 불완전하다.
- 6종 중 **셋(Cr·Sc·Y)만** 이 10종에 포함. In·Ga·B 는 미측정.
- 두 농도뿐 (2점). 중간 농도 없음.

### 닫는 실험 (저렴)

같은 `2,2,1` 셀에서 In₂O₃·Ga₂O₃·B₂O₃ 를 x=0.0625 로 stage 04 까지 — `run_dualx.sh` 의
`for c in ...` 목록만 바꾸면 된다. 그러면 6종 전수로 P11 을 농도 조건부로 다시 쓸 수 있다.

## 미조사분 전수 확인 (2026-08-13 심야)

### `09e_ehull` 270개 — G1 을 못 살린다 (그리고 **우리는 이미 알고 있었다**)

행 키가 `hull_E_at_winner_composition_eV_atom` 이다 — **hull 까지의 거리가 아니라
그 조성에서의 hull 에너지 절대값**(−5.5 ~ −7.9 eV/atom). `E_above_hull` 은 없다.

거리를 얻으려면 `E(우리 구조) − E(hull)` 이 필요한데 우리 구조는 **UMA**, hull 은
**MP DFT** 라 기준계가 달라 뺄 수 없다. **못 쓰는 것이지 잊은 것이 아니다.**
→ **G1 은 vacuous 인 채로 유지.** 발표 P10 은 현행 그대로 맞다.

다만 `hull_decomposition` (270개) 은 유효하다 — ESW 반응식과 짝이 되는 분해산물 정보로
passivation 논의에 쓸 수 있다.

⛔ **더 중요한 정정**: `E_above_hull` 은 **이미 repo 에 있다** —
`cascade_stability_axes.csv` 의 `e_above_hull_meV`, 47종 전부.
**46종이 0.0 meV, 최대가 CrO₃ 46 meV.** 그리고 `cascade_stability_axes_verdict.json` T10 이
내가 오늘 세운 것과 **똑같은 가설을 이미 세우고 기각했다**:

> **예측이 빗나갔다.** "G1 이 vacuous 한 원인은 hull 대신 host 상대 Δe 를 쓰기 때문" 이라
> 가정하고 T10 을 세웠는데 **hull 로 바꿔도 탈락 0종**이다. 원인은 기준이 아니라 **풀**이다 —
> 47종이 애초에 안정한 흔한 이성분 산화물·불화물로 큐레이션돼 있어 어떤 열역학 안정성
> 기준을 걸어도 통과한다. → T10 은 접는다.

즉 "못 구한다" 가 아니라 **"구했고 아무것도 안 바뀐다"** 가 정답이다. 그리고 그 편이 낫다 —
G1 이 vacuous 한 것이 **풀 큐레이션의 성질**이라는 정량 근거가 되기 때문이다.

### σ MD · W_ad — **존재한다** (앞선 "없음" 판정 정정)

`multi_category_2026_05_19_v22_OLD_radiusonly_20260525`:

| | 개수 | 대상 |
|---|---|---|
| `STAGE_10.DONE` (σ MD) | **7** | Cu₂O_x002 · Li₂O_x002/005/010 · Na₂O_x002/005/010 |
| `STAGE_11.DONE` (W_ad) | **6** | Li₂O ×3 · Na₂O ×3 |
| 그 캠페인 `dataset.csv` 의 sigma/wad | **0 / 45행** | 스테이지는 돌았는데 **수집이 안 됐다** |

v23 에서는 `TOP_K_SIGMA=0` 이라 정말 없지만, 옛 radiusonly 캠페인에는 있다.
**"σ 는 어디에도 없다" 는 2026-08-13 판정은 틀렸다.** 다만 7종이고 radiusonly(폐기 계보)라
인용 가치는 낮다. 병은 같다 — `collect_dataset.py` 가 stage 10/11 을 읽지 않는다.

### `bvse_proxy.py` — **BV 파라미터가 정본과 갈라져 있다**

| | S | Cl | b |
|---|---|---|---|
| CLAUDE.md 규약 (`tools/comp1_v3/`) | R0 **2.105** | **2.249** | 0.37 |
| cascade (`tools/doping/bvse_proxy.py`) | R0 **1.94** | **1.91** | S 만 **0.40** | <!-- lint-skip-path: gabia 전용, 이 브랜치 미수록 -->

Adams 2003 계열 값이다. → **G4 의 transport 축 값은 우리 BVSE 결과와 같은 표에 올리면 안 된다.**
`tools/convention_check.py` 가 MSD 창은 잡지만 BVSE R0 은 안 잡는다 (규약 확장 후보).

부수 정정: cascade 판은 **Br 2.07 · I 2.29 · N 1.61 · Se · Te** 까지 갖고 있다. 내가
"BVSE 가 S·Cl·O 만 지원해서 회수 14종은 축을 못 채운다" 고 추측한 것은 **틀렸다**
(실측으로 이미 뒤집혔지만 이유도 틀렸다).

### 나머지

- `09f_esw` 270개 · `FINAL_RANKING.json` 270개 (`provenance/weights/n_structures/rows/grouped_stats`)
  — 구조 확인만, 미수집
- `predictor/` 270개 = `training_summary.json` + `predictor_screen_de_per_atom.pkl`
  (캐스케이드마다 학습된 ML 모델 270개, 미수집)
- `dft_inputs/` 270개 = `dft_input_summary.json` 뿐 (실제 입력 없음)
- `_OLD_radiusonly_20260525` 276 dirs 중 완주는 6개뿐 (STAGE_12)
- `tier_..._overgenerated` 는 종별 디렉터리가 아니라 **단일 cascade** 의 스테이지 디렉터리들이다
  (COMPOUND_FILTER 미설정 → 5250 구조 과생성 사례)

## ⛔⛔ G4 의 blocking 은 도펀트 **원자 수 프록시**다 (2026-08-14 새벽, 앞 절 정정)

`run_uma_screening.py` 실측 정의:

```python
blocked = sum(1 for li in li_idx if min(D2[li, d] for d in dopant_idx) < 4.0)
metrics['dopant_blocking_fraction'] = float(blocked) / len(li_idx)
```

**도펀트 원자에서 4 Å 안에 있는 Li 의 비율.** 순수 기하 — 에너지도 경로도 없다.

champion 262개 실측:

| | |
|---|---|
| blocking vs 셀 안 도펀트 원자 수 | **r = 0.876 · R² = 0.768** |
| blocking ≥ 0.60 (G4 탈락) | 92개 · 평균 도펀트 원자 **4.7** |
| blocking < 0.60 (G4 통과) | 170개 · 평균 도펀트 원자 **1.9** |

### 앞 절(농도 의존) 정정

"G4 는 아무도 선택하지 않은 농도에서 발화했다" 는 **발견이 아니라 정의의 결과**다.
도펀트가 4배면 4 Å 구 안의 Li 도 대략 4배가 된다 (실측 2.9–3.9배, 겹침으로 포화).
농도 표 자체는 유효하지만 **해석을 바꿔야 한다.**

### 대신 더 강한 비판이 나온다

`cascade_screening_funnel.json` 이 이미 적어놓았다: **G4 단독 탈락 27종 중 24종**이
`blocking < 0.60` 으로 떨어지고 BVSE cut 단독 기여는 3종(B₂O₃·GeO₂·MoO₃)뿐이다.
→ **G4 탈락의 대부분이 "4 Å 안에 Li 가 몇 개냐" 로 결정됐다.**

그리고 화학량론 교락이 눈에 보인다:

| G4 통과 11종 | 화학식당 원자 |
|---|---|
| CaO·MgO·ZnO·LiF | 2 |
| Ag₂O·Li₂O·CaF₂·MgF₂·SiO₂·SnO₂ | 3 |
| WO₃ | 4 |

| 산화 개선 6종 | 화학식당 원자 |
|---|---|
| Sc₂O₃·Cr₂O₃·In₂O₃·Ga₂O₃·Y₂O₃·B₂O₃ | **전부 5 (M₂O₃)** |

**통과군은 전부 2–4 원자, 산화 개선군은 예외 없이 5 원자.**
P11 의 "산화 개선 ↔ Li 경로 충돌" 은 (a) M³⁺ 가 onset 을 올린다는 실제 효과와
(b) M₂O₃ 가 원자 수가 많아 blocking 이 기계적으로 높다는 사실이 **겹친 것**일 수 있다.
R² 0.768 이면 blocking 에서 원자 수를 뺀 잔여 정보는 23% 다.

### ⚠ 위 우려는 **실측으로 기각됐다** (2026-08-14, `cascade_seminar_oxidation_transport_47.csv`)

6종의 실제 G4 탈락 사유를 열어보니 blocking 이 아니라 **transport_norm** 이 지배한다:

| | blocking | **transport_norm** | fail_mode |
|---|---|---|---|
| Cr₂O₃ | 0.889 | **0.05** | blocking_cut |
| In₂O₃ | 0.833 | **0.05** | blocking_cut |
| Y₂O₃ | 0.833 | **0.05** | blocking_cut |
| Sc₂O₃ | 0.778 | **0.05** | blocking_cut |
| Ga₂O₃ | 0.611 | **0.05** | blocking_cut |
| **B₂O₃** | **0.588 (통과)** | **0.10** | bvs_branch_cut |

G4 = `transport_norm > 0.30` **AND** `blocking < 0.60`. 6종 전부 transport_norm 이
**0.05–0.10 으로 문턱의 1/6–1/3** 이다. **blocking 항을 통째로 제거해도 6종 전부 탈락한다.**
B₂O₃ 는 blocking 을 통과(0.588)하고도 BVSE 축에서 떨어진다.

→ **"trade-off 가 원자 수 교락" 이라는 우려는 성립하지 않는다. P11 은 그대로 유효하고,
근거는 기하 개수가 아니라 BVSE 유래 이온 경로 프록시다.**
(blocking 이 원자 수 프록시라는 사실 자체는 여전히 참이고, G4 탈락 27종 중 24종을
설명한다는 것도 참이다. 다만 **이 6종에 대해서는 결정적 요인이 아니다.**)

### 발표 대응 (2026-08-14)

대본은 **바꾸지 않는다.** 6/6 관측은 사실이고, 현행 P11 이 이미
*"M–O 결합이 원인이라는 증명도 아닙니다"* 로 인과를 유보하고 있다.
"blocking 이 뭐냐" 질문에만 답을 준비한다:

> 도펀트 원자에서 4 Å 안에 있는 Li 의 비율입니다. 정적 기하 지표이고, 저희 데이터에서
> 셀 안 도펀트 원자 수와 R² 0.77 로 상관합니다. 그래서 이 게이트는 경로 물리보다
> 조성 화학량론을 상당 부분 반영하며, 그 점 때문에 G4 를 heuristic 으로만 씁니다.

### 후속

- blocking 을 **도펀트 원자 수로 정규화**한 잔차로 G4 를 다시 걸면 무엇이 남나
- `transport_norm`(BVSE 유래)만으로 G4 를 걸면 명단이 어떻게 바뀌나 — 단독 기여 3종뿐이라
  게이트가 거의 무력해질 가능성
- `convention_check.py` 에 BVSE R0 규약 추가 (cascade Adams-2003 vs 정본 softBV)

## ★ webapp 전면 개정 — 화면이 스스로 모순되던 것을 끊었다 (2026-08-14)

Codex 감사 지적: *"붙여준 화면은 사실상 47종 시대 UI 에 '90종 회수분' 탭만 덧댄 상태"*.
맞았다. leaderboard·Pareto·"Li transport"·합성 score·26개 site rule 이 **최신 승인 결과처럼**
남아 있었다. 구조를 바꿨다.

### 기본 화면이 결과가 아니라 **감사**다

| 전 (최상단 타일) | 후 |
|---|---|
| 47 랭킹 · 4 Pareto · 141 champion · 14 verified | **273 계획 · 270 완주 · 90 회수 · 승인 ranking 0** |

승인 0 은 실패가 아니라 **현재 상태의 정확한 이름**이다 — 47종판은 취합 경계라 superseded 고,
89종 재랭킹은 결측 19종을 안은 미검증 진단물이다. 단일 출처는 `webapp/data.py: CASCADE_TRUTH`.

탭 순서도 신뢰도 순으로 뒤집었다: `📋 현황·감사`(기본) → `🧪 ESW(90종·complete)` →
`🔁 90종 회수분(diagnostic)` → … → `🗄 47종 리더보드/깔때기(superseded)`.

### "Li transport" 라는 이름을 폐기했다

전도도를 잰 것처럼 읽혔는데 G4 입력은 정적 프록시 **두 개**뿐이다:

| 입력 | 실제 정의 | 함정 |
|---|---|---|
| `bvs_li_proxy_score` | 어닐 기하의 legacy BVS | **Adams-2003 파라미터**(R₀ S 1.94·Cl 1.91·b_S 0.40) — 정본 softBV(2.105/2.249/0.37)와 다름. comp1 BVSE 와 같은 표 금지 |
| `tier2_dopant_blocking_fraction` | 도펀트 4 Å 내 Li 비율 | 도펀트 **원자 수에 거의 비례**. host 원소만 든 Li₂S·LiCl 은 0.0 자동 통과 |

MD 확산계수·NEB 장벽·σ 는 **하나도** 안 들어갔다. 라벨을
`정적 Li-환경 프록시 (BVS + 4 Å foreign-center)` 로 바꾸고 funnel G4 · themes 카드 양쪽에 반영.

### 빌더가 풀 크기를 하드코딩하고 있었다 — 그게 사실 하나를 숨겼다

`build_screening_funnel.py`·`build_cascade_themes.py` 의 description·honesty_header·caveat 이
"47종" 을 문자열로 박고 있어서, `_v2`(89종)로 돌려도 설명문만 47종으로 남았다. `NP = len(rows)` 로
연동하고 두 판을 다시 만들었다. 그 과정에서 **정정된 사실**:

> **연성 경험칙.** 47종에서는 "B/G>1.75 를 넘는 종이 하나도 없다" 가 참이었다.
> 90종 회수분에서는 **Na₂S 가 B/G 2.50** 으로 넘는다 (로스터 B/G 범위 0.98 → **2.50**).
> ⚠ Na₂S 는 부분 결측 18종 중 하나라 **연성 판정으로 인용 금지** — 서술만 정정한다.

옛 문자열의 "로스터 범위 0.98–1.59" 는 pugh(G/B)가 아니라 **B/G = 1/pugh** 범위였다
(1/1.02=0.98, 1/0.63=1.59). 지금은 계산해서 쓴다.

### 되돌아가지 못하게 잠갔다

`webapp/tests/test_webapp.py` 에 6건 추가 (40 passed):
기본 탭이 audit 인가 · 타일이 273/270/90/0 인가 · superseded/diagnostic 라벨이 있는가 ·
G4 옛 이름이 **정정 문맥 밖에서** 살아있지 않은가 · v2 JSON 에 "47종" 이 없는가 ·
AlI₃·MgI₂·Li₂S·LiCl 이 기본 화면에 떠 있는가.

마지막 것이 실제로 **두 번째 인스턴스를 잡았다** — 🎯 테마 탭의 `ionic_transport` 카드가
같은 옛 라벨을 쓰고 있었다. 탭만 고치고 끝냈으면 놓쳤다.

## ★★ Codex 정식 리뷰 P0 8건 — 전부 확인되고 반영됨 (2026-08-14)

첫 개정(`090d0df2`)은 "옛 화면을 최신처럼 보이지 않게" 했을 뿐이고, **중간 탭들이 어떤 상태로
노출되는지**를 안 봤다. Codex 가 8건을 짚었고 **전부 코드로 재현됐다.**

| # | 지적 | 검증 | 처리 |
|---|---|---|---|
| P0-1 | 273 = **91**종 × 3 (90은 완주 수) | `master_batch_273.sh` 37+54=91 | 타일 툴팁 정정 |
| P0-2 | 🧪 ESW 탭 배지는 90종인데 표는 47종 파일 | v1 50행 vs v2 92행 | v2 로 전환 + 파일명 명시 |
| P0-2b | 90종 ESW 는 phase-set ID 미보존 | **v1·v2 공통** — 둘 다 반응식 문자열만, mp-ID·MP 스냅샷 없음 | v2 회귀 아님을 명시하고 한계로 게시 |
| P0-3 | 71/18/1 은 gate completeness 가 아니다 | `GATE_INPUT_COLS` 가 **미사용 `eos_B0_GPa` 를 세고 사용 중인 `pugh` 를 뺐다** | 정정 → **완전 88 · 부분 1 · 결측 1** |
| P0-4 | champions·themes·stability·co-doping 이 무표시 | 전부 v1 파일을 읽음 | 4탭에 상태 배너 |
| P0-5 | G4 순환 — blocking 탈락 시 norm 강제 | `build_screening_funnel.py:139-142` `else: n = GATE_FLOOR` | 코드째 화면에 게시 |
| P0-6 | x=0.05 가 아니라 x=0.25 | champions csv `concentration` 전부 0.25 | 라벨/실측 분리 표기 |
| P0-7 | base 가 Model C 가 아니다 | ESW 좌변 `Li22P4(S5Cl)4` → **Cl:P = 1.0** | scope 를 Li₆PS₅Cl 계열로 |
| P0-8 | "깔때기 논증은 유효" 가 너무 세다 | G3 phase set · G4 순환 · G5 로스터 의존 | 배너에서 철회 |

### 가장 큰 것 — 결측 18종은 **허수**였다

`GATE_INPUT_COLS["champions"]` 가 `[rerank_de, elastic_E_young, **eos_B0_GPa**]` 였는데,
`eos_B0_GPa` 는 **어느 게이트도 안 쓴다**(화면 표시용). 반대로 G5 연성축이 쓰는
`elastic_pugh_GoverB` 는 빠져 있었다. 바로잡으니:

| | 옛 감사 | 정정 |
|---|---|---|
| complete | 71 | **88** |
| partial | 18 | **1** (MgI₂) |
| dropped | 1 (AlI₃) | 1 (AlI₃) |

즉 **90종 풀의 완결성은 사실상 해결돼 있었다.** 내가 "18종 부분평가" 라고 여기저기 써 둔 것은
전부 틀렸고, 그 문구로 랭킹을 diagnostic 으로 낮춘 근거의 절반이 사라진다.

### 그럼 왜 90종 랭킹을 확정하지 않나 — 막는 건 결측이 아니다

| blocker | 내용 |
|---|---|
| **G4 순환** | blocking 컷 탈락자는 `transport_norm` 이 **0.05 로 강제**되어 BVS 값이 버려진다. 컷이 0.30 이라 blocking 탈락 = G4 탈락이 결정론적. "두 독립 신호가 일치" 로 읽으면 안 된다 (6/6 trade-off 서술 철회 대상) |
| **G5 로스터 의존** | median 컷이라 **풀이 바뀌면 문턱이 같이 움직인다** — 47종판과 89종판의 G5 통과자는 같은 기준이 아니다 |
| **가중치 수작업** | 0.30/0.25/0.20/0.15/0.10 은 물리 유도값이 아니다. soft+ductile 0.35 는 bucci2017 이 반증하는 단조 가정 |
| **ox_V 축퇴** | 호스트 S²⁻ pin 으로 여러 종이 같은 onset |
| **절대값 부풀림** | UMA 탄성이 실험(12–22 GPa) 대비 높음 — 내부 상대비교만 |

**89종 랭킹 자체는 지금 내려받을 수 있다** (`cascade_v23_ranked_v2.csv`). 못 하는 건
"이게 답이다" 라고 말하는 것이다.

### AlI₃ — 90번째를 넣는 유일한 경로

`rank_combined==1`(champion) 행에 탄성·EOS·BVS 가 없지만 **`rank_combined==2` 행에는 전부 있다**
(E 45.05 · 43.60 · 42.21 GPa, B0 20.98 · 17.04 · 18.03). 대체하면 90/90 이 되지만 **다른 종은
champion 인데 AlI₃ 만 2위 배치**가 되어 동일 기준 비교가 깨진다. 전수 확인 결과 이 상황인 종은
AlI₃ 하나뿐이다(La₂O₃+Clrich 는 변형 체인). **쓸지 말지는 사람이 정한다.**

### 회귀 테스트 5건 추가 (45 passed)

ESW 탭이 배지대로의 파일을 읽는가 · scope 가 Li₆PS₅Cl/x=0.25 인가 · G4 순환이 게시돼 있는가 ·
4개 탭에 상태 배너가 있는가 · gate 입력 정의가 pugh 를 포함하고 eos_B0 을 제외하는가.

## ★★★ 릴리스 감사 라운드 2 — Codex 재감사 반영 + **내 오류 하나 철회** (2026-08-14 저녁)

Codex 가 `Cascade_Audit_Seminar_2026_08_14_release.zip` 로 정본 계약·핸드오프·PPT·대본을 냈고,
`23ba5244` 를 다시 동결 감사해 **1건 닫힘 / 3건 부분 / 4건 잔존** 판정을 줬다.
문서는 `docs/reviews/` 에, 대본은 `kb/seminars/`, 덱은 `docs/seminars/` 에 등록했다.

### ⛔ 내가 틀린 것 — Na₂S "연성 경험칙 반증" 철회

오전에 *"90종에서는 Na₂S 가 B/G 2.50 으로 넘는다"* 고 올렸다. **틀렸다.** 두 겹이었다:

1. `Na2S_x100_cLi24gaCl4d_s00` 의 **B_hill = −36.27 GPa** — 음의 체적탄성률은 연질이 아니라
   **탄성 계산 실패**다. 옛 가드는 `nu < 0` 만 봐서 이 행이 3점 평균에 들어갔다.
2. 그 평균을 역수 취했다. `1/mean(G/B) ≠ mean(B/G)` (Jensen).

`mean(G/B) = 0.4012 → 1/0.4012 = 2.492`. 실패 행을 빼면 **Na₂S 는 B/G 1.22**,
`89종 어느 것도 1.75 를 못 넘는다` 가 다시 참이다.

**전수 확인: 270행 중 비물리 탄성 행은 이 한 행뿐이다.** `plot_cascade_insights.py` 의
`agg()` 에 `_elastic_ok()` (B_hill·G_hill ≤ 0 차단)를 넣고 `ranked_v2` 를 재생성했다.
waterfall 은 불변(89–89–84–45–28–1).

> 교훈: **"새 발견" 이 단 한 종에서만 나오면 그 종의 원자료를 먼저 본다.** 풀 전체가
> 조용한데 하나만 튀면 물리보다 실패 행일 확률이 높다.

### Codex 수치 독립 검증 — 전부 재현됨

| 주장 | 재현 |
|---|---|
| blocking 제거 시 6종 중 5종 통과 | ✅ Cr₂O₃ 0.8086 · Ga₂O₃ 0.3989 · In₂O₃ 0.6652 · Sc₂O₃ 0.4868 · Y₂O₃ 0.8825 · B₂O₃ 0.1000 — **소수점까지 일치** |
| G4 단독 탈락 27종 중 24 blocking / 3 BVS | ✅ 우리 funnel JSON `threshold_basis` 에 이미 있던 값 (B₂O₃·GeO₂·MoO₃) |
| LiS4 제외 시 host onset 2.256 V | ✅ `esw_lis4excluded.json` — comp1·modelc **둘 다** 2.256 |
| 71/18/1 이 gate completeness 아님 | ✅ 이미 정정 (88/1/1) |

### 내가 덧붙인 것 — **B₂O₃ 의 탈락도 풀 상대값이다**

Codex 표에서 B₂O₃ 만 0.1000 인데, 이건 `0.10 + 0.90n` 의 **바닥**이다. 즉 B₂O₃ 는 47종 풀의
**BVS 최솟값**(n = 0.0000)이라 그 값이 나온 것이지 독립 측정이 아니다. 89종 풀에서 다시 재면:

| | 47종 풀 | 89종 풀 |
|---|---|---|
| 최솟값 종 | **B₂O₃** | **ZrCl₄** |
| B₂O₃ blocking-free | 0.1000 (탈락) | **0.1998** (탈락) |
| Ga₂O₃ | 0.3989 | 0.4620 |
| Sc₂O₃ | 0.4868 | 0.5391 |

**같은 종의 G4 점수가 로스터만 바꿔도 최대 +0.09 움직인다.** 결론(5/6 통과 · B₂O₃ 탈락)은
두 풀에서 같지만, min–max 정규화를 쓰는 한 **어떤 G4 숫자도 풀 밖에서는 의미가 없다.**
47종판과 89종판의 통과선을 나란히 비교하면 안 된다는 근거가 하나 더 늘었다.

### 화면·계약 변경

- **manifest 도입** — `db/properties/cascade_audit_manifest.json`
  (`rebuild_pool_inputs.py --manifest` 가 생성). artifact 10건의 sha256·바이트·주석제외 행수와
  status 5종(`historical`/`recovered_unvalidated`/`approved`/`superseded`/`invalid`)을 굳힌다.
  **headline 6수치가 여기서 파생**되고, 파일이 바뀌었는데 manifest 가 안 따라오면
  숫자를 추측하지 않고 **fail-closed** 한다. (실제로 개발 중 한 번 작동했다.)
- 타일 4개 → **6개**: 273 계획 · 270 완주 · 90 완주종 · 47 역사스냅샷 · **0 승인** · **0 explicit pair**
- `/composition` 의 `🤖 Cascade hit` → `🗄 Cascade — historical 47종` + superseded 경고,
  `/elements` 카드도 동일. **legacy rank 우회 경로를 라벨링했다.**
- G4 endpoint 명단과 89행 랭킹을 `<details>` **opt-in** 뒤로. 수는 보이되 명단은 접어둔다.
- `concentration_convention` 의 `x=0.02/0.05/0.10` 전부 제거 — 라벨이지 농도가 아니다.

### 인계 산출물 병합 완료 (같은 날 저녁, `cascade_codex_audit_artifacts_9abe5105.zip`)

repo 에 없던 4종을 받아 등록했다. 받자마자 **독립 검증부터** 했고 전부 재현됐다:

| 검증 | 결과 |
|---|---|
| `g4_rescore.csv` 의 raw bvs·blocking 6종 | 우리 litransport 와 **소수점 6자리까지 일치** |
| "회수 270건 중 124건 onset 에 LiS4" | 우리 ESW json 으로 세어 **124/270 정확히 일치** |

**`cascade_audit_gate_completeness.csv` 가 내 감사보다 정확하다.** 나는 단일 88/1/1 을 썼는데
이건 **축마다 분모가 다르다**:

| gate | 전 라벨 완전 | 부분 | 결측 | method status |
|---|---|---|---|---|
| G1 | 88 | MgI₂ | AlI₃ | recovered_diagnostic |
| G2 | 90 | — | — | recovered_unvalidated |
| **G3** | **0** | — | **90종 전부 method identity 없음** | **blocked_method_contract** |
| G4 | 88 | — | AlI₃·**MgI₂** | historical_only |
| G5 | 88 | MgI₂ | AlI₃ | recovered_diagnostic |

**G3 가 핵심이다** — onset *기록*은 90종 전부 있는데 **method-complete 비교는 0종**이다.
파생표가 `phase_set_id` 를 떨어뜨렸고 plain/Cl-rich 지지가 섞여 있다. *기록이 있다 ≠ 비교 가능하다.*
내 감사는 "행이 있나" 만 봤기 때문에 이 구분을 못 만들었다. 화면을 이 표로 교체했다.
(G4 에서 MgI₂ 가 partial 이 아니라 **dropped** 인 것도 내가 놓친 것 — x005 입력이 없다.)

### manifest 를 한 파일로 합쳤다

Codex 플로터도 `db/properties/cascade_audit_manifest.json` 을 본다 — 내가 만든 것과 **같은 경로**다.
스키마를 갈라두면 둘 중 하나가 조용히 틀리므로 합쳤다: Codex 의 `schema_version 2`
(source_commit · headline 키 6개 · figures 5쌍 · supporting_tables) + 내 `artifacts` 블록.
이제 양쪽이 같은 파일을 검증한다 — `plot_cascade_audit_2026_08.py --validate-only` **exit 0**.

⚠ 그 과정에서 플로터가 **정확히 fail-closed 했다**: Na₂S 정정으로 `ranked_v2` 해시가 pin
(`2c930ebb…`)과 달라져 실행을 거부했다. pin 을 옮기되 **왜 옮겼는지를 `PIN_OVERRIDES` 에 기록**했다
— 이유 없이 옮기면 이 장치가 무의미해진다. 5개 패널은 ranked_v2 의 탄성 평균을 안 쓰므로 그림은 유효하다.

**그림은 재생성하지 않았다.** 이 컨테이너에 플로터가 쓰는 TrueType 폰트가 없고, 재생성하면
바이트가 달라져 무결성 대조가 깨진다. `9abe5105` 에서 만든 PNG 를 그대로 쓴다.

### 5개 감사 패널을 기본 화면에 올렸다

계약(§4.4)이 기본 공개를 허용한 유일한 그림이다 — campaign status · G3 phase-set 민감도 ·
G4 분해 · 계면 축 · ML 검증. 각 패널에 Origin-ready CSV 다운로드를 붙였다.
리더보드·Pareto·수송 순위·pair 예측 그림은 이번 릴리스에 넣지 않는다.

### Round-3 재감사 반영 — P0 4건 · P1 6건 (2026-08-14 밤)

판정: **감사 패널 조건부 GO · 전체 웹 NO-GO · 90종 leaderboard NO-GO.** 승인 ranking 계속 0종.
검증 가능한 주장은 전부 재현했다 — **G5 validity-aware 86 / AlBr₃·MgI₂·Na₂S / AlI₃ / usable 89**
가 우리 champions_v2 로 정확히 나왔다.

| # | 지적 | 처리 |
|---|---|---|
| P0-1 | manifest owner 가 둘 (두 도구가 서로의 계약 블록을 지움) | **`build_cascade_audit_manifest.py` 신설 — 단독 writer.** 두 생산자는 sidecar 만 쓴다 |
| P0-2 | mixed-source pin (top-level 9abe / ranked_v2 만 922) | artifact 별 `source_commit`·`derived_from`·`override_reason`. ranked_v2 는 **패널 의존에서 제거** (어느 패널도 안 읽는다) |
| P0-3 | fail-closed 가 headline 에만 걸림 | **`webapp/artifact_policy.py` 중앙 resolver** — `/api/file`·`/api/csv`·`/api/property` 전부 경유 |
| P0-4 | 홈 `UMA #1` 무표시 · `결측 19종` 잔존 · ESW `complete` | 전부 정정. ESW 는 **record-complete 90 / method-comparable 0** 로 |
| P1 | `<details>` 는 후보명을 초기 DOM 에 다 싣는다 | **`/cascade/diagnostic` 서버 라우트** — `?view=diagnostic` 없으면 렌더 자체를 안 한다 (403) |
| P1 | status 어휘 3중 혼선 | **두 축으로 분리**: `approval_status`(6종) ⊥ `use_scope`(4종) |
| P1 | G3 CSV 의 synthetic phase_set_id | 비우고 `phase_set_assumption` 으로 분리 |
| P1 | G4 CSV 메타 부족 | `pool_id`·`normalization_n`·BVS min/max·`actual_x` 추가 |
| P1 | G5 는 presence 만 센다 | `completeness_basis` + validity-aware 열 병기 |
| P1 | 깨끗한 checkout 에서 CRLF 로 무결성 실패 | `.gitattributes` 에 `db/properties/*.{csv,json} eol=lf` + 원장에 `sha256_lf` 병기 |

#### 두 축 분리가 핵심이었다

전에는 `historical` 같은 한 값이 "얼마나 믿을 수 있나" 와 "어디까지 보여줄 수 있나" 를 겸했다.
이제 직교한다:

```
approval_status : historical | recovered_unvalidated | approved | superseded | invalid | audit_current
use_scope       : default_visible | archive_only | diagnostic_only | blocked
                                     ?archive=1     ?view=diagnostic
```

원장에 없는 cascade artifact 는 **거부**한다 (미등록 = 미승인).

#### 실측으로 확인한 것

| 경로 | 조건 없음 | opt-in |
|---|---|---|
| `cascade_v23_ranked_v2.csv` | **403** | `view=diagnostic` → 200 |
| `cascade_v23_ranked.csv` (47종) | **403** | `archive=1` → 200 |
| `/api/property/cascade_screening_funnel_v2` | **403** | `view=diagnostic` → 200 |
| 감사 CSV·PNG | 200 | (default_visible) |
| cascade 밖 파일 | 200 | (정책 대상 아님) |

`/cascade/diagnostic` 은 gate 없으면 **후보명이 DOM 에 안 실린다** (403 화면에서 실측).

#### 남은 두 건도 닫았다 (같은 날)

**① 그림 재생성 — 폰트가 근본 문제였다.** `_font()` 가 `C:/Windows/Fonts/arial.ttf`
하나에 묶여 있어 **Linux 에서 이 도구가 아예 안 돌았다.** 폴백 체인을 넣었다:

```
Arial (Windows) → Liberation Sans (Arial 메트릭 호환) → DejaVu Sans → PIL default
```

이 환경은 **Liberation Sans** 로 해결됐고, 재렌더 결과가 Arial 원본과 시각적으로 동일하다
(메트릭 호환이라 같은 좌표계에서 레이아웃이 안 흔들린다). 어느 폰트를 썼는지는
원장 `render_provenance` 에 싣는다 — **폰트가 바뀌면 PNG 바이트가 바뀌므로 무결성의 전제다.**

그리고 더 중요한 것: 내가 손으로 고쳤던 감사 CSV 3건(G3 가정 분리 · G4 pool 메타 ·
G5 validity)을 **생성기에 이식**했다. 손으로 고친 CSV 는 재현 불가라 원장이 해시로 묶어봐야
의미가 없다. 이제 `plot_cascade_audit_2026_08.py` 가 그 내용을 스스로 만든다 —
G5 의 86/AlBr₃·MgI₂·Na₂S/AlI₃/89 도 champions_v2 에서 직접 계산한다.
**두 번 돌려도 바이트가 같은 것을 md5 로 확인했다.**

부수: `csv.writer` 기본 lineterminator 가 `\r\n` 이라 생성기가 CRLF 를 쓰고 있었다.
`lineterminator="\n"` 으로 고정했다.

**② 원장 자기완결.** `recovered_artifacts` · `source_hashes` · `render_provenance` 를
플로터 sidecar 에서 원장으로 옮겼다. 이제 **원장만 보면 된다**:

| 블록 | 내용 |
|---|---|
| `source_hashes` | 고정 커밋 blob 해시 (패널 입력이 조용히 안 바뀌었다는 근거) |
| `recovered_artifacts` | 회수 sidecar 행수·해시 + **게이트별 완결성** + ingestion 감사 |
| `render_provenance` | 사용 폰트 + 폰트가 바뀌면 해시가 바뀐다는 경고 |
| `datasets` · `metric_contract` | 앞 라운드에 옮김 |

테스트 **63 passed** (신규 3건: 폰트 없이도 도구가 도나 · 원장 자기완결 · CSV 가 생성기에서 재현되나).

테스트 **60 passed** (신규 7건 포함: 정책 전 경로 · 서버측 gate · 원장 단독소유 ·
artifact 별 provenance · G3 합성 ID 금지 · G4 메타 · G5 validity · LF 고정).

### Round-3 공개 패키지 반영 — **익명화 정책이 내 화면을 뒤집었다** (2026-08-14 심야)

`Cascade_Audit_Seminar_2026_08_14_round3_package.zip` (25장 공개 덱 + 대본 + Origin CSV 3종 +
PNG/SVG). 받자마자 분모를 우리 데이터로 다시 셌고 **전부 재현**됐다:

| 축 | Codex | 우리 재현 |
|---|---|---|
| record_present | 90 | 90 ✅ |
| G1 all-label | 88 | 88 ✅ |
| G4 x005 입력 | 88 / 결측 AlI₃·MgI₂ | 88 / AlI₃·MgI₂ ✅ |
| G5 method 유효 | 86 / AlBr₃·MgI₂·Na₂S / AlI₃ / 89 | 동일 ✅ |

#### ⛔ 정책 충돌 — 내 기본 화면이 후보 이름을 띄우고 있었다

Round-3 의 공개 경계는 *"candidate identity is **acquisition-only**"* 다. 그런데 내가 올린
G4 감사 패널은 **B₂O₃·Cr₂O₃·Ga₂O₃·In₂O₃·Sc₂O₃·Y₂O₃ 를 그대로 표시**하고 있었다.
89행 랭킹과 endpoint 명단은 서버측으로 막아놓고 정작 감사 그림에서 여섯 종을 노출한 것이다.

교체했다 — 공개 패널은 **익명본**(Case A–F · Scenario A/B), 종명이 든 판은 `diagnostic_only`:

| 공개 (default_visible) | 진단 (diagnostic_only) |
|---|---|
| `cascade_seminar_g4_anonymized_round3.{png,csv}` | `cascade_audit_g4_rescore.{png,csv}` |
| `cascade_seminar_g3_sensitivity_round3.{png,csv}` | `cascade_audit_g3_phase_set.{png,csv}` |

그리고 화면의 패널 목록을 **원장의 `figures` 에서 파생**하게 바꿨다. 목록을 화면 코드에
따로 두면 이번 같은 정책 변경이 화면에만 반영 안 되는 일이 또 생긴다.

#### 게이트 표를 분모 계약으로 교체

`gate_denominators_round3.csv` 가 **record_present 와 method_valid 를 열로 분리**한다.
내 앞 표는 `all_label_complete_species` 하나에 두 개념이 섞여 있었다:

| gate | 기록 | **method 유효** | status |
|---|---|---|---|
| G1 | 90 | 88 | recovered_diagnostic |
| **G3** | **90** | **0** | **blocked_method_contract** |
| G4 | 90 | 88 | historical_only |
| G5 | 90 | **86** | recovered_diagnostic |

**모든 게이트의 `approved_current_species` 가 0 이다.**

#### 그 밖

- headline 문구: `270 완주` → **`270 완주 (enabled-workflow)`**
- 91종 타일: **`PLANNED INPUT ROSTER × 3 라벨 — shortlist 아님`**
- 진단 PNG 도 원장에 등록해 **미등록 거부가 아니라 `diagnostic_only` 로 명시**한다
  (미등록이면 차단 사유가 '원장에 없다' 로만 나와 정책 의도가 안 보인다)

테스트 **65 passed** (신규 2건: 공개 G4 패널 익명 확인 · 분모 계약 record≠method).

### 남은 이견 (Codex 에게 재확인 요청할 것)

1. **후보명 완전 비노출 vs opt-in.** 나는 `<details>` opt-in 으로 했다. 완전히 숨기면
   "다음에 뭘 계산할지" 를 화면에서 못 고른다. 이게 계약 위반인지 판단 요청.
2. **`historical` vs `superseded`** 를 47종 artifact 에 어떻게 나눠 붙일지. 지금은
   원자료 CSV = `historical`, 파생 랭킹 = `superseded` 로 갈랐다.
3. Codex 가 참조한 `cascade_audit_gate_completeness.csv`·`plot_cascade_audit_2026_08.py`·
   5개 audit figure 는 **repo 에 없다**(로컬 미푸시). 넘겨주면 내 manifest 와 병합한다.

## ★★★ G3 가 닫혔다 — method-comparable 0 → 270/270 (2026-08-16)

`blocked_method_contract` 는 **마지막 blocked 게이트**였다. 원인은 "임의로 골랐는데 안 적었다" 가
아니라 **"규칙은 균일한데 그 규칙이 해석된 결과를 안 저장했다"** 였다.

### 무엇이 없었나

`esw_cascade_batch.py` 는 처음부터 균일한 규칙을 썼다 — `get_entries_in_chemsys(els,
thermo_types=["GGA_GGA+U"])`, **제외 필터 없음**. 저장한 것은 값과 반응식 문자열뿐이라,
**어떤 entry 집합**을 썼는지와 **MP 스냅샷 버전**이 사라졌다. 그래서 90종에 onset 기록이
다 있는데도 candidate–host 비교가 0종이었다.

### 무엇을 했나

| 조치 | 결과 |
|---|---|
| chemsys 마다 정렬된 MP entry ID 전체 + `phase_set_id = sha256(...)[:16]` + entry 수 + **db 버전** 저장 | phase_set **84개** · MP db **2026.04.13** |
| host 를 **각 후보의 chemsys 안에서** 같은 실행에 계산 | in-chemsys host 84개 |
| chemsys 를 **후보 ∪ host** 로 잡음 | 비교불가 9 → **0** |
| 각 후보에 `host_ox_V_same_phase_set` · `delta_ox_vs_host_V` · `method_comparable` 부착 | **270/270** |

### ★ 나온 답 두 개

**① host onset 이 84개 phase set 전부에서 정확히 2.140 V.** 예외 0건.
도펀트 원소를 뭘 넣어도 host 분해 경로가 안 바뀐다 — 지금까지 써온 "후보 − 2.140" 비교가
**사후적으로 정당화됐다.** 반대였으면 상위 28종 수치를 통째로 다시 매겨야 했다.

**② 같은 phase set 안의 Δox_V 분포** (이제 처음으로 인용 가능한 형태):

| Δ | 건수 |
|---|---|
| **> 0** (host 보다 좋아짐) | **28** |
| = 0 (변화 없음) | **102** |
| **< 0** (나빠짐) | **140** |

절반 이상이 host 보다 **나빠지고**, 38%는 아무 변화가 없다. 좋아지는 28건도 5개 값에 뭉쳐 있다.

### 부수 발견 — x=0.25 에서 Cl 이 통째로 사라지는 9건

`TiF₄ · ZrBr₄ · ZrF₄` 챔피언의 실측 조성이 `Li25 P3 S20 F4 Ti1` 처럼 **Cl 0개**다.
셀의 Cl 이 4개뿐이라, Cl 자리를 치환하는 도펀트는 x=0.25 에서 **Cl 을 전부 없앤다.**
그러면 host(`Li24P4S20Cl4`)가 그 chemsys 의 부분집합이 아니다 — 버그가 아니라 화학이다.
합집합 chemsys 로 묶어 해결했고, **그 9건의 후보 onset 은 안 변했다**(TiF₄ 2.024 · ZrBr₄/ZrF₄ 1.878).
비교를 성립시키면서 값은 안 흔들렸다.

### 게이트 분모 표가 이렇게 바뀐다

| gate | 기록 | method 유효 | status |
|---|---|---|---|
| G1 | 90 | 88 | recovered_diagnostic |
| **G3** | 90 | **0 → 90** | ~~blocked_method_contract~~ → **recovered_diagnostic** |
| G4 | 90 | 88 | historical_only |
| G5 | 90 | 86 | recovered_diagnostic |

⚠ **승인 랭킹은 여전히 0종이다.** G3 가 풀렸을 뿐, **G4 순환**(blocking 이 BVS 를 덮어씀)과
**G5 로스터 의존**(median 컷)은 그대로다. "재랭킹을 막는 건 결측이 아니라 게이트 정의" 라는
진단에서 **G3 항목만 빠진다.**

⚠ 그리고 남은 것 하나: `clrich` 변형이 섞여 있다. `Al2O3_x020_chain_Cl_x200` 이 2.354 로
나오는데 그건 Cl-rich 변형이지 plain champion 이 아니다. **같은 phase set 이어도 조성이 다른
것을 나란히 놓는** 문제는 별개이며 아직 안 닫혔다.

## TODO (2026-08-14 발표 이후, 우선순위 순)

1. ~~`09e_ehull` 로 G1 재건~~ → **불가 확인 (2026-08-13 심야)**. 위 절 참조 — 거리가 아니라
   hull 절대에너지이고 UMA/MP 기준계가 달라 뺄 수 없다. G1 은 vacuous 유지.
2. **회수 체인 실행** — `tools/cascade/rebuild_pool_inputs.py` (2026-08-13 신설, selftest 10건).
   `--inplace` 없이 먼저 돌려 `_v2` 로 뽑고 옛 판과 대조 → `plot_cascade_insights.py`
   → `build_screening_funnel.py` → 새 waterfall. **풀 47 → 90.**
3. **In₂O₃·Ga₂O₃·B₂O₃ x=0.0625** — tmux `dualx3` 로 예약됨(2026-08-14 00:02, QE 대기).
   끝나면 6종 전수가 되어 P11 을 농도 조건부로 확정 가능.
4. `09f_esw` 270개 · `FINAL_RANKING.json` 270개 · `predictor/` · `dft_inputs/` 수집
5. `multi_category_2026_05_19_v22_OLD_radiusonly_20260525` (276 dirs · 238 MB) ·
   `tier_..._overgenerated` (COMPOUND_FILTER 버그 사례) 확인
6. `tools/doping` 미독 ~20파일 (특히 `bvse_proxy.py` 296줄 — G4 축의 정의)
7. 덱 반영 — 20-스테이지 슬라이드 · P3(273 축) · P5(회수 가능한 43종) · P11(농도 조건)

**2026-08-14 발표는 현행 대본 그대로 간다.** 오늘 발견은 전부 "좋아지는" 방향이지만
3번이 끝나야 P11 에 농도 조건을 붙일 수 있고, 2번이 끝나야 90종 숫자를 말할 수 있다.

## 반증·한계

- ESW 배치 스크립트(`esw_cascade_batch.py`) 자체는 아직 안 읽었다. 47에서 멈춘 것이
  의도(예산·검토 대기)인지 중단인지는 그 로그를 봐야 한다.
- `unified_dataset_273.csv` 는 gabia 에만 있다. repo 에 없으므로 이 표의 수치는
  2026-08-13 회수 시점 기준이다.
- 축 충족 = **열이 비어 있지 않음**이다. 값의 품질(수렴·이상치)은 따로 봐야 한다.

## ★★★ Stage ↔ 발표 Step 대조표 — 코드에서 직접 뽑았다 (2026-08-19)

1저자 지적("step 을 잘 모르는 것 같다, 코드를 보라")에 따라 기억이 아니라
`tier_cascade.sh` 본문에서 실행 순서를 그대로 뽑았다. **파일 머리의 `Stage map:`
주석은 낡았다** — 04/05 가 뒤바뀌어 있고 anneal 조건도 다르다. 주석 말고 본문을 볼 것.

| 주석(11–21행) | 실제 코드 |
|---|---|
| `04 BVSE proxy` · `05 light anneal (300K, 20 ps)` | **04 = anneal(500 K, 50 ps)** · **05 = BVSE** |

### 실제 실행 순서 (본문 133–351행)

| Stage | 스크립트 | 핵심 인자 | 발표 Step |
|---|---|---|---|
| 00 | preflight | | — |
| 01 | `run_compound_batch.sh` → `substitute_compound.py` | `SUPERCELL=1,1,1` · `N_SEEDS=5` · `EXOTIC=0` | **Step 1–2** |
| 02 | `run_uma_screening.py` | `--steps 1500`, `cell_relax=True` | **Step 3** |
| 03 | `select_winners.py` | `--group_by dopant site anion_site_label` `--max_dv 0.25` `--require_converged` | **Step 3 게이트 + Step 4 선별이 한 줄** |
| 04 | `run_anneal.py` | **500 K · 50 ps · FIRE**(기본 `real`; `ANNEAL_MODE=light` 면 300 K/20 ps) | **Step 5** |
| 05 | `bvse_proxy.py` | post_relax.xyz · `--grid_resolution 25` | **Step 6** |
| 06 | `rank_anneal.py` | post-anneal 에너지 재랭크 `--top 30` | — |
| 07 | `run_mlip_postproc.py` | `--no_anneal --no_elastic --n_eos_seeds 5` → B₀·V₀·BM3 | **Step 7** |
| 08 | `run_mlip_postproc.py` | `--no_anneal --no_eos` → C_ij·VRH | **Step 7** |
| 09a–f | combine / collect / train_predictor / dft_inputs / ehull / **esw** | | **Step 8**(=09f) |
| 10 | σ_Li MD (top-5 × 3T × 50 ps) | | **Step 9** (미실행) |
| 11 | NCM adhesion v6 | | **Step 9** (미실행) |
| 12·12b | 최종 collect + ML 재학습 | | — |

### ⛔ 이 대조로 드러난 발표 오류 둘

**① Step 3 의 부피 게이트는 스크린(02)이 아니라 선별(03)에 있다.** 그리고 03 은
게이트와 "그룹당 Top-1" 을 **동시에** 한다. 실측 (`cascade_v23_all.csv`):

```
3,615행 (02 전수)
  −  100행   |ΔV| > 25 %          ← 2.8 %
  −     0행   수렴 실패            ← 전부 수렴
  − 2,834행   그룹당 Top-1 탈락    ← **78 %. 여기가 진짜 깔때기다**
  =   681행   → 04 anneal · 05 BVSE · 08 elastic (전부) / 07 EOS 622행
```

⇒ **발표는 25 % 게이트를 Step 3 의 주역처럼 말하지만 실제로는 2.8 % 손질이다.**
5배 축소는 Top-1 선별이 한다. (게이트가 무의미하다는 뜻은 아니다 — 에너지 컷과
교집합 0 이라는 11장 논지는 그대로다. 규모를 잘못 말하고 있을 뿐이다.)

**② "One structure per compound is kept for the full calculations" 는 순서가 거꾸로다.**
`--group_by dopant site anion_site_label` 이라 winners 는 **(도펀트 × 양이온자리 ×
음이온자리)당 하나**다. (도펀트, 농도라벨) 조합당 실측 분포:

```
1개 45 · 2개 186 · 3개 24 · 4개 39 · 6개 6   (조합 300개, 합 681)
```

**본 계산(anneal·BVSE·EOS·elastic)은 681개 전부에 돌았고**, compound 당 하나로 좁히는
것은 **그 뒤 09a 취합**이다. 즉 "하나만 남기고 계산" 이 아니라 "다 계산하고 하나를 고름" —
이게 `kb/results/champion_pool_size_bias_2026_08_18.md` 의 best-of-N 편향이 성립하는
바로 그 구조다. 발표 12장이 "세 점은 자리·시드가 다른 세 구조" 라고 이미 반쯤 알고 있다.

### 부수 사실

- `eos_B0_GPa` 는 681 중 **622행**만 찼다 — EOS 적합 59건 실패. 발표에서 EOS 수를
  681 로 말하면 안 된다.
- `sigma_300K_S_cm_NE` · `wad_J_m2_mean` 은 **0행** — Stage 10·11 미실행. 17장 문구와 일치.

## ★★★★ 전수 정독 (2026-08-19) — doping 파이프라인 31개 파일

1저자 지적("코드 확실하게 정독한 거 맞지")에 따라 unified 브랜치 `tools/doping/` 를
전부 읽었다. 앞 절(Stage↔Step 대조)은 **실행 경로만** 본 것이라 아래를 놓쳤다.

### A. 주석이 코드와 다른 곳 — 넷 (전부 읽는 사람을 속인다)

| 어디 | 주석이 말하는 것 | 코드가 하는 것 |
|---|---|---|
| `tier_cascade.sh` 머리 Stage map | 04 = BVSE · 05 = light anneal(300 K, 20 ps) | **04 = anneal(500 K, 50 ps)** · 05 = BVSE |
| `tier_cascade.sh` Stage 08 | "clamped-ion Cij" | 변형마다 **이온을 이완**한다(FIRE, fmax 0.05) = relaxed-ion |
| `run_compound_batch.sh` 머리 | 억셉터는 "Li-interstitial 경로 미구현, 전하 불균형" | `add_li_interstitials()` 로 **구현돼 있다** (B₂O₃ 는 Li 4개 삽입) |
| `bvse_proxy.py` 모듈 docstring | `proxy = std × (1−\|mean−1\|)` → **std 클수록 좋다** | `(1−\|mean−1\|) × (1−std)` → **std 클수록 나쁘다.** 부호가 반대다 |

(`substitute_compound.li_vacancies_needed()` 도 "interstitial 미구현" 이라 적혀 있고
**아무도 안 부른다** — 죽은 함수다. 실제 계산은 `substitute_compound_at_sites` 안에 있다.)

### B. ⛔ 진짜 결함 넷 — 전부 데이터에 지문이 남는다

**B-1. `Li_24g` 와 `Li_48h` 는 같은 구조다.**
`substitute_struct.find_host_indices_for_site()` 는 *"Li 24g 와 48h 를 가르려면 입력 파일의
Wyckoff 메타데이터가 필요한데 항상 있지는 않다"* 며 **두 라벨 모두 Li 전체를 돌려준다.**
`HOST_SITES` 의 전하(+1)·반지름(0.76)·`RADIUS_TOL`(0.60)도 둘이 동일하고, 씨드도 같으므로
`Li_24g_s00` 과 `Li_48h_s00` 은 **원자 좌표까지 같은 구조**다.

실측 (330쌍 전수):

```
|Δde| 중앙 1.5e-06 eV/atom      ← 이완 수치잡음. 물리 차이가 아니다
|Δde| > 1e-3 : 45/330           ← 같은 출발점에서 다른 분지로 간 것(MLIP 이완 카오스)
|Δde| > 0.1  :  8/330
```

라벨이 생긴 도펀트 12종은 전부 **1가**(Li·Na·Cu·Ag) — `LITERATURE_SITES` 가 그 넷에만
`['Li_24g','Li_48h']` 를 적어 놨기 때문이다.

**영향**: winner 681개 중 **66 슬롯이 두 라벨을 다 승자로 뽑았다(132행)** → 같은 구조에
anneal·BVSE·EOS·elastic 을 두 번 돌렸고, 챔피언은 *중복 둘 중 좋은 쪽*으로 뽑혔다.
그리고 10장 그림 `step2_site_grid.png` 의 *"9칸이 전부 채워져 있다 = 자리 조합을 훑었다"*
는 **6칸이 진짜고 3칸(Li 48h 행, 330개)은 복사본**이다.

**B-2. `li_mobility_score` 가 파일에 안 들어간다 — 그래서 랭킹의 30 %가 죽었다.**
`bvse_proxy.py` 는 JSON 을 **먼저 쓰고**(267–273행) 그 다음에 `li_mobility_score` 를
계산한다(278–282행). 다시 쓰지 않는다. ⇒ `cascade_v23_all.csv` 에서 **0/3,615**.

`combine_rankings.py` 는 그 열을 읽어 `normalize()` 에 넘기는데, 전부 None 이면
**상수 0.5** 를 돌려준다. 가중치는 `0.4·안정성 + 0.3·탄성 + 0.3·이동도` 다.

지문 — `combined_score` 3,615행 **전부** `[0.1500, 0.8500]` 안에 있다.
0.4·0 + 0.3·0 + 0.3·0.5 = 0.15, 0.4·1 + 0.3·1 + 0.15 = 0.85. 정확히 일치한다.

⇒ **모든 종의 챔피언(`rank_combined == 1`)이 안정성 + 영률 둘로만 뽑혔다.**
`esw_cascade_batch.py` 도 *"슬롯은 combined_score 최대값이 가져간다"* 고 적고 그대로 쓴다 —
우리 47/90종 리더보드·계면·ESW 가 전부 이 선택을 물려받았다.
(우리가 발표하는 `cascade_v23_ranked.csv` 의 점수식 `0.30 ox + 0.25 stable + 0.20 soft +
0.15 ductile + 0.10 window` 는 **다른 식**이라 그 자체는 무사하다. 문제는 그 식에
들어가는 **행이 이미 이동도-맹목으로 골라진 챔피언**이라는 것이다.)

**B-3. Type C(공동도핑) 스윕이 조용히 무너졌다.**
`halide_rich_swap()` 의 ValueError 는 **try 밖**이다(Type A 만 감싸져 있다). 그리고
`compound_summary.json` 은 루프가 **다 끝난 뒤에** 쓴다 ⇒ 뒤쪽 조합 하나가 죽으면
**앞에서 이미 만든 구조까지 통째로 버려진다.** 게다가 `2>&1 | tail -3 || true` 가 에러를 삼킨다.

M₂O₃ 는 1 unit 이 O 3개라 `anion_site=S_4a`(자리 4개)에 3개가 들어가 S 가 1개만 남고,
Cl 과잉 0.4 는 `n_swap=2` 를 요구해 죽는다. MgO·ZnO 는 O 가 1개라 3개가 남아 산다.

```
MgO · ZnO         excess 0.2 / 0.4 / 0.6 / 0.8   (각 120행)
나머지 9종        excess 0.2 만                  (각 30행)
```

⇒ **공동도핑 축은 설계의 1/4 만 존재한다.** 11종 × 4단계 = 44 조합 중 **17개만** 돌았다.

**B-4. `--method cluster` 블록은 죽은 코드다.**
`run_compound_batch.sh:174` 가 `--method cluster` 를 넘기는데
`substitute_compound.py:578` 의 argparse 는 `choices=['spread','random','first']` 다 →
즉시 종료, `|| true` 가 삼킨다. (`select_substitution_sites` 자체는 cluster 를 지원한다 —
argparse 만 막는다.) CSV 에 **중복 name 0건**인 것이 증거다.
⇒ "Type A cluster method (전구체 국소배위 모사)" 10종 × 3농도가 **한 번도 안 돌았다.**

### C. ⚠ 부피 게이트 — 앞 절 6b 의 결론을 **보류**한다

`preflight.py:84–89` 가 이렇게 적어 놨다:

> `|ΔV/V0| < 35 %` … **UMA 가 LPSCl 을 canonical 셀 대비 25–35 % 부풀린다**(Wang 2025
> sulfide PES softening). 구조 결함이 아니라 UMA 편향이다.
> *v4.5.5 fix: was 5 % → false-failed on every UMA cascade.*

이게 사실이면 기준 셀이 **26–28 Å³/atom** 에 있고, `screen_dV_over_V0` 는 부피가 아니라
**"이 구조가 아직 argyrodite 같아서 UMA 가 똑같이 부풀렸는가"** 를 재는 값이 된다.
−13 % 중앙, −33 % 꼬리가 전부 그것으로 설명된다.

⛔ 그러면 6b 의 null 대조 논증이 약해진다 — Li₂S·LiCl 은 host 와 사실상 같은 물질이라
**기준과 같이 부풀어서** 0 이 나온다. 영점이 물리적으로 맞다는 증거가 되지 못한다.

**반대 증거**: `uma_relax_check.py` 실측에서 UMA 는 DFT 이완 `modelC` 를 **+0.92 %**,
`b2o3_relaxV0` 를 **−0.00 %** 로 놔뒀다. 25–35 % 팽창이 사실이면 modelC 도 부풀어야 한다.

**가르는 판 — GPU 0 시간.** Stage 00 이 270 캐스케이드마다
`$OUT/00_preflight/preflight_report.json` 에 `baseline_relax.detail.dV_rel` 을 **이미 적어 놨다.**
gabia 에서 그 파일 하나만 읽으면 끝난다. (읽기 전까지 6b 의 "기준 셀은 정상이다" 는
**미확정**으로 둔다.)

### D. 나머지 확인 사항

- `select_winners.py` 에 필터가 **넷**이다 — 내가 앞 절에서 셋만 셌다. 넷째는
  `outlier_flag`(`dV>30 %` **또는** `|Δe|>5 eV/atom`). 그래서 "Top-1 이 2,834행을 뺐다" 는
  **상한**이다(errored·outlier 몫이 섞여 있다).
- winner 선정 지표는 `min(de_per_atom_vs_baseline)`. 스크립트가 `group_metric_spread` 를
  **이미 기록한다** — best-of-N 편향을 재는 계기가 산출물에 들어 있는데 우리가 안 썼다.
- `eos_ensemble` 은 rattle 5개 중 **r² 최대 하나를 고른다**(또 다른 best-of-N). 시드별 B0
  산포는 `ensemble` 에 있는데 우리 CSV 는 선택값만 들고 있다.
- `preflight.check_positive_controls` 가 적어 놓기를, UMA 는 Nd₂O₃/Al₂O₃/MgO 에 대해
  ΔE/atom **−0.5 ~ −0.9 eV** 를 주는데 문헌 범위는 ±0.03 eV 다 — **20~30배**. 허용범위를
  넓혀서 통과시켰다.
- ⛔ **cascade BVSE 는 우리 BVSE 와 파라미터가 다르다.** `bvse_proxy.py` 는
  Li–S R0 **1.94**(b **0.40**) · Li–Cl **1.91** 을 쓴다. 우리 정본은 S **2.105** · Cl **2.249**,
  b 0.37 (CLAUDE.md). 그리고 `migration_volume_fraction` 은 20³–25³ 격자에서
  **BVS ∈ [0.8, 1.2] 인 점의 비율**이지, 우리의 "iso 준위 아래 채널 %" 도 퍼콜레이션도 아니다.
  ⇒ **cascade Li-수송 수치를 우리 comp1_v3 BVSE 옆에 나란히 쓰면 안 된다.**
- `run_md_sigma.py`(미실행)는 자유절편 회귀는 맞지만 창이 `fit_start:끝`(50 ps)이고
  prod 50 ps 다 — 우리 규약(2–50 ps, prod 200 ps)과 다르다. 언젠가 켜면 먼저 맞출 것.
- `fetch_mp_structure.py` 가 mp-985592 를 **준안정 다형**이라고 스스로 적어 놨다.
- `site_preference.py` VALIDATION_SET 에 *"was fabricated Lee2025 ref"* 로 **날조 인용을
  찾아 지운 기록**이 있다.
