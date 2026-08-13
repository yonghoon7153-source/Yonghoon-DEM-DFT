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
