# 전류 집중계수 `focus_top` 결함 — 진단 · 수리 · 회신 (2026-09-22, `SELF-45`)

> 촉발: 외부 리뷰어 지적 **A-2** — *"Table S3 hot-spot 의 `99.8th percentile / mean` = 1447 · 1189 은
> 수학적으로 불가능하다.  비음수 분포면 `P(X ≥ q) = 0.002 ⇒ E[X] ≥ 0.002·q`, 즉 `q ≤ 500·mean`."*
>
> 판정: **부등식은 맞다.  "불가능" 은 아니다.  그러나 그 지적을 따라가서 진짜 결함을 하나 찾았다.**
> 인계 문서 `docs/handoff_review_20260922.md` §7 #6 이 요구한 계산을 실제로 수행한 결과다.

---

## 0. 한 문단 요약

`focus_top` 의 **분모**는 그 백분위의 모집단 평균이 아니라 **인가 전류밀도**
`J_app = I/A = σ_eff·ΔV/L` 이고, `A` 는 **공극·SE 를 포함한 전 단면**이다.  분자는 **도체 복셀만**의
`|J|` 백분위다 ⇒ 모집단도 면적 규약도 달라 Markov 상한이 두 수를 묶지 않는다.  **열 이름이 틀렸다.**
그런데 확인하다 보니 **분자도 틀렸다**: 백분위를 장(field)이 아니라 **그림용 부분추출 점군**에
걸고 있었고, 그 추출은 상위 35 % 를 전수 보존하는 hot-biased 추출이라 **보고값이
`--field-max-points`(그림 예산)의 함수**였다.

---

## 1. 소스 — 무엇이 분자이고 무엇이 분모였나

| | 자리 | 정체 |
|---|---|---|
| 분자 | `mpm_webapp_payload.py:1941` → `step3_sigma.field_point_cloud` | `np.percentile(점군, 99.8)`, 점군 = `sid ∈ {1,2,3,4,5,7,8} ∧ cond` 의 `|J|` **부분추출** |
| 분모 | `mpm_webapp_payload.py:2011` · `step3_sigma.solve_sigma_z:891` | `σ_eff/L`, `σ_eff = I·L/(A·ΔV)`, **`A = nx·ny·vox²` = 격자 전체 단면** |

즉 `focus_top = J₉₉.₈(도체 복셀) / J_app(전 단면)`.  리뷰어가 *"분모가 전극 전체 거시
평균전류밀도이거나 영역이 다를 가능성이 크다"* 고 한 추측이 **정확히 맞다.**

---

## 2. 실측 — 실물 솔버(`solve_sigma_z`)로 침대 두 개를 풀었다

vox 0.15 µm · 60×60×90 · 생산 σ 표(AM_S 0.01 · AM_P 0.005 · VGCF 78.5398 S/cm).

| | ① AM 협착만 (**SBE 문법**) | ② AM + VGCF 14 가닥 (**DBE 문법**) |
|---|---|---|
| 도체셀 `N` · `φ_c` | 157,889 · 0.487 | 160,402 · 0.495 |
| `σ_eff` (S/cm) | 2.66e-4 | 0.3062 |
| `J_app = I/A` (A/cm² @1 V) | 0.19706 | 226.82 |
| `⟨\|J\|⟩_도체셀 / J_app` | **3.083 ×** | **1.999 ×** |
| `J₉₉.₈ / ⟨\|J\|⟩` ← **Markov 대상** | **17.2** ✅ ≤ 500 | **128.4** ✅ ≤ 500 |
| `J₉₉.₈ / J_app` (장 전수) | **52.9** | **256.7** |
| **보고되던 값** (`--field-max-points 90000`) | **71.6** ⟵ **1.35 × 과대** | 256.8 (편향 ≈ 0) |

### 2-1. 결정타 — 보고값이 **그림 점 개수**에 따라 움직인다 (침대 ①)

| `--field-max-points` | 5,000 | 20,000 | 40,000 | 90,000 | 전수 |
|---|---|---|---|---|---|
| 보고 `focus_top` | **201.2** | 157.0 | 118.6 | **71.6** | **52.9** |

원인: `field_point_cloud` 가 그림에서 백본을 살리려고 상위 `hot_budget_frac`(0.35)×`max_points` 를
**전수 보존**한다 (렌더링으로는 옳다).  그런데 소비자가 **그 점군에** 백분위를 걸어서, 실제로
집히는 것은 장의 99.8 % 가 아니라 **위에서 `0.002·max_points` 번째 셀**이었다.
과대 배율 ≈ `√(N/max_points)` (꼬리가 rank⁻⁰·⁵ 일 때; 실측 1.35 ≈ √(157,889/90,000) = 1.32).

### 2-2. ⚠ 편향이 **꼬리 모양에 걸린다** — 그래서 비에서 상쇄되지 않는다

침대 ①은 1.35 ×, ②는 1.00 × 였다 (탄소 도선이 있으면 상위가 고원이라 편향이 사라진다).
⇒ **SBE↔DBE 비에서도, 전자↔이온 비에서도 상쇄되지 않는다.**

### 2-3. 규율 ⑤ 의 그 자리

같은 모듈의 `joule_hotspot` 은 처음부터 `conc_ratio`·`hot_frac_50` 을 **추출 전**에 쟀다
(`step3_sigma.py:1284-1287`).  한 파일 안에서 규약이 갈려 있었고 **갈린 쪽만 보고값이 됐다** —
*"후보를 고르는 코드가 곧 사각지대다."*

---

## 3. `×1447 / ×1189` 에 대해 말할 수 있는 것 · 없는 것

- ✅ **Markov 위반이 아니다.**  1447 이 성립하려면 `⟨|J|⟩/J_app ≥ 2.894` 면 되고 실측이 3.083 이다.
  ⚠ 단 **그 침대에서 재보기 전엔 증명이 아니다.**
- ⛔ **그러나 1447 자체가 과대일 것이 거의 확실하다.**  `n_dof ≈ 2 M` 이면 `√(N/90,000) ≈ 4.7 ×`
  → 참값은 300 대일 수 있다.
- ⛔ **`−17.8 %` 헤드라인을 회신에 넣지 말 것** — §2-2 대로 편향이 케이스마다 달라 감소폭이
  줄거나 **부호가 뒤집힐 수** 있다.  *"전자 ×1447 vs 이온 ×26.75 = 54배"* 도 같은 이유로 보류.
- ✅ **본문 오염은 없다.**  전수 스윕(평문 + pptx/docx zip 리더) 결과 두 수는
  `ms_si_v7_edit_sheet_20260901.md` §4-3b 와 `ms_readthrough_20260903.md` 의 **제안**에만 있고
  본문 스냅샷 · Methods 초안 · Methods docx · 세미나 덱 어디에도 **없다**.

---

## 4. ★ 재실행 불요 — 저장된 payload 로 복원된다

상위 `0.35·max_points` 가 **전수 보존**돼 있으므로 점군이 장의 상위 꼬리를 그대로 들고 있다.

> **복원 가능 조건**: `0.002·N ≤ 0.35·max_points`  (예산 90,000 이면 **N ≤ 15.75 M**)

픽스처 검증: 보고 71.60 → 복원 **52.89** vs 전수 참값 **52.87** (오차 **+0.037 %**, payload 의
4자리 반올림 포함).  `⟨|J|⟩` 도 +0.11 % 로 복원된다.

```bash
python3 scripts/repair_focus_top.py <mpm_payload.json>            # 보고만
python3 scripts/repair_focus_top.py <dir> --write --csv out.csv   # 제자리 수정(원값 보존)
```
조건을 못 넘거나 이온 `ion_n_dof` 가 없는 옛 payload 는 **거부**한다 (근사로 채우지 않는다).

---

## 5. 이번 커밋이 바꾼 것

| # | 자리 | 무엇 |
|---|---|---|
| P-1 | `step3_sigma.field_point_cloud` | 부분추출 **전** 전수로 `p99_8`·`mean`·`n_total` 을 계산해 `stats` 로 반환 (`joule_hotspot` 규약에 맞춤).  반환이 2-tuple → **3-tuple** |
| P-2 | `mpm_webapp_payload` 전자·이온·열류 | `np.percentile(점군)` 폐기 → `stats` 사용.  **컬러바 정규화도 같은 값**으로 (라벨과 색이 같은 것을 가리키게).  `field_scale_*` 에 `focus_over_local_mean`(≤ 500 보장) · `j_mean_local_A_cm2_per_V` · `local_mean_over_j_app` · `n_conducting_voxels` · `percentile_basis` · **`focus_basis`**(분모 정의 문자열) 추가.  `step3.ion_n_dof` 신설 |
| P-3 | `viewer3d.js` | `(p99.8/⟨J⟩)` → **`(p99.8 / J_app)`**, 같은 모집단 비 병기, 툴팁에 분모 정의와 Markov 관계 명시, 옛 payload 경고 |
| P-4 | `step3_sigma --selftest` | `field-stats-budget-invariant`(예산 불변) · `field-stats-nonvacuous`(옛 규약은 실제로 움직인다 — 시험이 공허하지 않음의 증거) · `field-stats-markov` |
| P-5 | `findings.json` | `SELF-45` 등재 (P1) |
| P-6 | `scripts/repair_focus_top.py` | 옛 payload 복원기 + selftest 6 (정확 복원 · 비공허 · 평균 복원 · 거부 2종 · no-op) |

두 레인 게이트 **RC 0 / RC 0**.  `colorbar_fit` 의 *"마지막 눈금이 기준량을 밝힌다"* 단언은
기준량 이름을 `⟨J⟩` → `J_app` 으로 함께 고정했다 (취지 동일, 이름만 구체화).

---

## 6. 회신 초안 (영문, 붙여넣기용)

> Thank you — the inequality is correct and it caught a real problem, though not the one flagged.
>
> **On the bound.** Our denominator is not the mean of the percentile's own population. It is the
> **applied through-plane current density** `J_app = I/A = σ_eff·ΔV/L`, averaged over the **entire
> electrode cross-section including pores and solid electrolyte**, whereas the numerator is a
> percentile of |**J**| over **electronically conducting voxels only**. The two populations — and
> the two area conventions — differ, so Markov's inequality does not couple them. On reference
> solves we measure `⟨|J|⟩_cond / J_app` = 2.0–3.1 and `J₉₉.₈ / ⟨|J|⟩_cond` = 17–128, i.e. well
> inside the 500 bound. The column heading "× mean" was wrong and has been corrected.
>
> **On the numbers themselves.** Checking this, we found that the percentile had been evaluated on
> the *rendering* point cloud rather than on the full field. That cloud deliberately retains the
> hottest 35 % of its budget so the conduction backbone survives in the figure, which makes it a
> biased sample for a percentile: the reported value moves with the plotting budget (×201 → ×53 as
> the budget goes from 5×10³ to the full field). We have fixed the estimator, added a regression
> that pins the statistic to be invariant to the plotting budget, and are recomputing the focusing
> factors on the complete field. The revised table reports both ratios with each denominator
> defined explicitly.

---

## 7. 표 수정 (한 행 + 각주 한 줄)

```
Current-focusing factor   F₉₉.₈ = J₉₉.₈ / J_app          <재계산>   <재계산>
   (same percentile vs local mean)  J₉₉.₈ / ⟨|J|⟩_cond    (<값>)    (<값>)
```

> **Footnote.** J₉₉.₈, 99.8th percentile of |**J**| over electronically conducting voxels (full
> field); J_app = I/A = σ_eff·ΔV/L, the applied through-plane current density averaged over the
> full electrode cross-section (pores and SE included); ⟨|J|⟩_cond, mean of |**J**| over the same
> voxels as the percentile. The two denominators differ by ⟨|J|⟩_cond/J_app = <값>.

⚠ 같은 기회에 Table S3 제목의 *"obtained from the DEM simulations"* 도 고칠 것 — 이 값들은
**복셀 FV 솔버** 산출이다 (Codex R10 이 이미 잡아 둔 건, `codex_r10_verdict_20260829.md`).

---

## 8. 남은 것 (⬜ 열림)

1. **원고용 두 케이스(SBE·DBE)의 실제 payload 를 복원기에 통과시켜 정정값을 낸다.**
   그 payload 는 이 리포에 없다 ⇒ **저자 기계에서** 해야 한다.
   그 전까지 `×1447` · `×1189` · `−17.8 %` · `54배` 는 **인용 보류**.
2. `SELF-45` 를 이 커밋 SHA 로 `claimed_fixed` 승격.
3. ⚠ 부수 카비엇 (별개 · 작음): `_voxel_jmag` 는 면전류를 반씩 배분하는 프록시라 도체 **표면**
   셀이 최대 2배까지 과소 읽힌다.  침대 ②에서 `⟨|J|⟩/J_app = 1.999` 가 엄밀 하한
   `1/φ_c = 2.020` 을 1 % 밑돈 것이 그 자국이다.  이번 결함과 무관하고 크기도 작지만 기록해 둔다.

---

# ★★ 실측 결과 (2026-09-22 저녁) — 저장된 payload 에서 **재실행 없이** 나온 답

> 원자료: `webapp/mpm_lab/260714_145738_778fa4_{f752da,f79b67}/payload.json` (저자 기계).
> 도구 `scripts/repair_focus_top.py` (`73aa7ead9`).  CSV `~/focus_fix.csv`.

## A. 케이스 동정 — **확정**

| payload | σ_e (S/cm) | σ_ion (S/cm) | N (도체 복셀) | = |
|---|---|---|---|---|
| `f752da` | 0.054530 | 5.5341e-4 | 26,378,531 | **SBE** |
| `f79b67` | 0.071400 | 5.5798e-4 | 26,765,472 | **DBE** |

편집 시트 §4-3b 의 `0.0545 / 0.0714` · `5.53e-4 / 5.58e-4` 와 일치.  vox **0.3 µm**.

## B. 발표값은 **최소 2.7 배 과대** (엄밀 상한, 외삽 아님)

점군이 보존한 상위 31,499 개는 장의 상위 31,499 개와 **정확히 같다**.  값이 rank 에
단조 비증가이므로 `참 p99.8 (rank 52,759) ≤ 값(rank 31,499)` 이 **부등식으로** 성립한다.

| | 발표값 | 엄밀 상한 | 최소 과대 배율 |
|---|---|---|---|
| SBE | ×1447 | **≤ 520.6** (백분위 99.8806 %) | **≥ 2.78 ×** |
| DBE | ×1189 | **≤ 445.9** (백분위 99.8823 %) | **≥ 2.67 ×** |

⛔ 이 상한을 값으로 인용하지 말 것 — rank 가 1.68 배 얕은 **상한**이다.

## C. ★ 순서 주장은 **살아남는다** (백분위 사다리, 전부 정확값)

p99.8 은 못 닿지만 더 얕은 백분위는 **정확**하다.  같은 백분위에서 두 전극을 나란히:

| 백분위 | `J_q/⟨\|J\|⟩_cond` SBE | DBE | Δ | `J_q/J_app` SBE | DBE | Δ |
|---|---|---|---|---|---|---|
| 99.90 % | 102.6 | 90.87 | **−11.4 %** | 552.0 | 468.9 | −15.1 % |
| 99.95 % | 124.3 | 109.0 | **−12.3 %** | 668.7 | 562.2 | −15.9 % |
| 99.99 % | 174.9 | 153.2 | **−12.4 %** | 941.3 | 790.5 | −16.0 % |

⇒ **세 깊이 모두 SBE > DBE.**  *"DBE 가 전류를 더 고르게 분산한다"* 는 본문 주장은
**깊이에 강건**하고 유지된다.  다만 **크기가 바뀐다**: −17.8 % → **−11.4 ~ −12.4 %**.

## D. ⟨|J|⟩_cond / J_app — 리뷰어가 표에 넣자고 한 값 (전극별)

| | SBE | DBE |
|---|---|---|
| `⟨\|J\|⟩_cond` (A/cm² @1 V) | 40.451 | 50.792 |
| **`⟨\|J\|⟩_cond / J_app`** | **5.3806** | **5.1597** |

이 값은 전도상 단면분율의 역수 규모다 (`≥ 1/φ_c`).  **DBE 가 더 작다** = SDCP 가 더해져
전도상이 **4.3 % 더 많다**.  항등식 검산: `102.6 × 5.3806 = 552.0` · `90.87 × 5.1597 = 468.9` ✓.

★ **리뷰어의 우려가 실측으로 확인됐다** — 발표된 `−17.8 %` 는 두 가지의 곱이었다:
**전도망 내부 균일화 −11.4~12.4 %** × **전도상 증가 −4.3 %**.  `/J_app` 분모는 그 둘을
한 숫자로 합치므로 *"고르게 분산한다"* 주장에 쓸 수 없다.  ⇒ 헤드라인 분모는
**`/⟨|J|⟩_cond`** 로 간다 (리뷰어 제안 채택).

## E. ⬜ 아직 못 답하는 것

- **이온 채널 전부** — 옛 payload 에 `ion_n_dof` 가 없어 N 을 모른다.  본문의
  *"the ionic current distributions are comparable in the two electrodes"* 는 **미검증**이고
  근거였던 `focus_ion 26.75 vs 25.86` 은 같은 편향 추정기 산출이다.  ⇒ **재실행 필요**.
- **p99.8 정확값** — rank 가 1.68 배 부족.  재실행하면 나온다 (고친 코드는 `--field-max-points`
  와 무관하게 장 전수에서 계산한다 — 특별한 플래그 불요).
- **Figure S14/S15** — 정규화 분모가 바뀌었고(점군 p99.8 → 장 p99.8) 점군 편향이 패널마다
  다르므로 다시 그려야 한다.

## F. 권고 — 표·본문 최종형

원고의 백분위를 **99.9 %** 로 옮기고 사다리를 SI 에 같이 싣는 것을 권한다.  이유:
(i) 99.9 % 는 보관된 필드에서 **정확히** 계산되므로 재실행 없이 확정된다,
(ii) 세 깊이를 나란히 실으면 *"백분위를 고른 것 아니냐"* 는 반론이 원천 차단된다.
⚠ 다만 이것은 **결과를 본 뒤의 규약 변경**이므로 그 사실을 캡션에 적는다.

```
Current-focusing factor   F = J_q / ⟨|J|⟩_cond        SBE      DBE
  q = 99.9 %                                          102.6    90.87   (−11.4 %)
  q = 99.95 %                                         124.3    109.0   (−12.3 %)
  q = 99.99 %                                         174.9    153.2   (−12.4 %)
  ⟨|J|⟩_cond / J_app                                  5.381    5.160
```

---

# G. 재실행 레시피 — `meta.json` 이 전부 들고 있다 (2026-09-22 밤)

⚠ **정정**: 앞 §A 에서 vox 를 `0.3 µm` 로 적었는데 그것은 `/econn_summary/vox_um`(다른
서브시스템)이다.  **STEP3 격자는 `vox_um = 0.15 µm`** 다 (manifest · `step3.vox_um` 둘 다).
⇒ 26.4 M dof × 415 B/dof ≈ **11 GB** — V100 32 GB 에 들어간다 (이미 한 번 돌았다).

## 봉인된 재실행 인자 (SBE `f752da` 의 `meta.json.mpm_metrics.step3.manifest`)

| 축 | 값 |
|---|---|
| `code_sha` | `657c2192` |
| `input_digest` | `04b5a565ff4069f4` |
| `physics_protocol_id` | `p2-9cd29a0c61085621` |
| `vox_um` · `plate_z_grid_um` | **0.15** · `[0.0, 72.534]` |
| 스탬프 | `ptfe_stamp centerline` · `fibre_stamp segment` · `sdcp_stamp sphere (d 0.3)` |
| 기하 | `bridge_um 0.48 (explicit)` · `dilate_z 1.0719` · `ptfe_block 0.0` · `periodic_xy false` |
| 판 규약 | `plate_rule p2-occupied-surface-first` |
| σ (S/cm) | VGCF **78.5398** · SDCP 250 · PTFE **0** · SuperP 10 · SWCNT 100 · AM_S 0.01 · AM_P 0.005 |
| σ_ion (S/cm) | SE **0.003** · SDCP 0.001 · `swcnt_ion_block false` |
| 성분 | `electronic ✓ · ionic ✓` · thermal/pore/pnm/collector **disabled** |
| 필드 | `field_max 90000` (전자·이온 각 90,000 점 저장됨) |
| `se_source` | `npy` |
| 입력 지문 | scaffold `6184147f573f021d` · se `6146d358d8e9fd6a` · phase `601a887701420ea3` · fibre `bf5ff65dd265d540` · fibre_dia `95d320717868a4d0` · metrics_json `7b81d62524b74fca` |
| 실행 환경 | `/home/kgy/dem-venv/bin/python3` (3.8.10) — **kgy 에서 돌았다** |
| 수렴 | `cg_resid 9.93e-09` · `n_floating_dropped 41,445` |

DBE(`f79b67`)도 같은 구조의 `meta.json` 을 갖고 있다 — 그쪽 지문으로 대조할 것.

## ⛔ 재실행 전 확인 두 가지

1. **코드가 고쳐진 판인가** — 인계 §7 #7: `~/runyourai/1/Yonghoon-DEM-DFT` 는 git 리포가
   아니라서 러너의 `git pull --ff-only` 가 **조용히 실패**한다.  옛 코드로 돌리면 같은
   편향값이 또 나오고 이번엔 그것을 정답으로 믿게 된다.
   ```
   grep -c percentile_basis scripts/mpm_webapp_payload.py     # 0 이면 옛 코드
   python3 scripts/step3_sigma.py --selftest | grep -E "field-stats|joule-stats"   # 네 줄 OK
   ```
2. **입력 `.npy` 가 아직 있는가** — `se_source npy` 이므로 scaffold·se·phase·fibre·fibre_dia
   다섯 개가 필요하다.  위 지문으로 동일성을 확인한다 (같은 침대가 아니면 비교가 무효다).

## 재실행이 닫는 것

- 이온 채널 전부 (`ion_n_dof` 신설 ⇒ *"ionic comparable"* 검정 가능)
- p99.8 정확값 (rank 1.68× 부족이 사라진다)
- Figure S14/S15 (정규화가 장 p99.8 로 — e·ion·열류·**joule** 넷 다)

⚠ **플래그는 하나도 바꾸지 않는다.**  고친 코드는 통계를 장 전수에서 내므로
`--field-max-points` 와 무관하다.  90,000 은 그림용으로 그대로 둔다.

---

# H. 최종 회신문 (2026-09-22 밤) — 재실행 없이 ①②③ 확정, ④ 한정어

> 실행 판정: 원고 SBE/DBE 의 입력(`se_source npy` · `phase/fibre/fibre_dia`)은 **uma 에 없다**
> (uma 의 `pa/kits/*` 는 CSV 스캐폴드를 쓰는 **Phase A** 킷이다).  그 런은 `/home/kgy/dem-venv`
> 에서 돌았으므로 재실행은 **kgy** 에서만 가능하다.  ⇒ 아카이브된 필드로 답할 수 있는 데까지
> 답하고, 못 하는 것은 **못 한다고 적는다**.

```
Thank you — the inequality is right, and following it up turned out to matter more than the
label. Three things changed.

1. The denominator was mislabelled. The quantity we printed as "× mean" is not normalised by
   the mean of the distribution the percentile is taken over. It was normalised by the applied
   through-plane current density J_app = I/A = sigma_eff·dV/L, averaged over the FULL electrode
   cross-section (pores and solid electrolyte included), while the numerator is a percentile of
   |J| over electronically conducting voxels only. Different populations and different area
   conventions, so Markov's inequality does not relate them — which is why the number could
   exceed 500 without being impossible.

2. You are right that the denominator should change, and for the reason you gave. J_app carries
   the conducting-phase area fraction, so it mixes "the current is spread more evenly" with
   "there is more conducting phase". We measure that mixing directly: <|J|>_cond / J_app =
   5.381 (SBE) and 5.160 (DBE), i.e. the DBE has ~4 % more conducting cross-section. We have
   moved the reported quantity to the within-network measure, J_q / <|J|>_cond, and renamed it
   the current-focusing factor.

3. The numerator was also wrong, and this is the substantive error. The percentile had been
   evaluated on the point cloud we store for the field figures, not on the field. That cloud
   deliberately keeps the hottest 35 % of its budget so the conduction backbone survives in the
   rendering, which makes it a biased sample for a percentile: on a reference bed the reported
   value moves from x201 to x53 as the plotting budget goes from 5x10^3 points to the full
   field. The estimator now computes the statistic on the complete field before any
   subsampling, and a regression pins it to be invariant to the plotting budget.

   The archived fields retain the top 31,499 values exactly, which is enough to bound the
   published numbers rigorously (monotonicity, not extrapolation): the true 99.8th-percentile
   focusing factor is <= 520.6 for the SBE and <= 445.9 for the DBE, so the published 1447 and
   1189 are overstated by at least 2.78x and 2.67x respectively. They should not be used.

On your specific question about the ordering — it survives. The archived fields let us evaluate
the focusing factor exactly at any percentile shallower than ~99.88 %, and the SBE exceeds the
DBE at every accessible depth:

    percentile      F = J_q / <|J|>_cond           J_q / J_app
                     SBE      DBE      change     SBE      DBE     change
    99.9  %        102.6    90.87     -11.4 %    552.0   468.9    -15.1 %
    99.95 %        124.3    109.0     -12.3 %    668.7   562.2    -15.9 %
    99.99 %        174.9    153.2     -12.4 %    941.3   790.5    -16.0 %

So the direction of the claim holds and is stable with depth, but the magnitude is smaller than
published: about -11 to -12 % on the within-network measure, rather than -17.8 %. The
difference between the two columns is the conducting-area effect you identified. We propose to
report the ladder itself in the SI so the choice of percentile is visible rather than assumed,
and to state explicitly that 99.9 % (not 99.8 %) is used because that is what the archived
fields determine exactly.

Two things we cannot yet answer, and we would rather say so than paper over them:

  - The ionic channel. The archived payloads do not record the number of ionic conducting
    voxels, so the ionic focusing factors cannot be recomputed from them at all. The published
    ionic values came from the same biased estimator, and the ionic network has a much larger
    voxel population than the electronic one, so the bias was larger there, not smaller. We are
    therefore withdrawing the sentence "the ionic current distributions are comparable in the
    two electrodes" pending a re-run; it is not supported by anything we can currently stand
    behind.
  - Figures S14/S15. They are rendered from the same biased cloud and normalised by the same
    biased scale, and the bias differs between panels, so cross-panel visual comparison is not
    like-for-like. They will be regenerated with the corrected normalisation.

We will send the recomputed p99.8 values, the ionic factors and the regenerated figures once
the two cases have been re-run on the machine that holds their inputs.
```

## 무엇을 주장하지 **않는지** (내부용 체크)

- ⛔ `×1447` · `×1189` · `−17.8 %` · *"전자/이온 54배"* — 전부 철회.  상한만 인용 가능.
- ⛔ p99.8 **값** — 아카이브로는 상한뿐.  본문은 **99.9 %** 로 간다.
- ⛔ 이온 문장 — **삭제**.  "comparable" 도 "다르다" 도 말하지 않는다.
- ✅ 순서(SBE > DBE) · 크기(−11.4~12.4 %) · `⟨|J|⟩_cond/J_app`(5.381 / 5.160) — 세 깊이 정확값.
- ⚠ 99.9 % 채택은 **결과를 본 뒤의 규약 변경**이다.  회신문·캡션 둘 다에 그 사실을 적었다.

---

# I. 재실행 경로 확정 (2026-09-22 밤) — **MPM 재압밀 불요, STEP 2 만**

## 입력 위치 (kgy, phase 지문으로 확정)

| | 경로 | `phase.npy` 지문 |
|---|---|---|
| **SBE** | `/home/kgy/sdcp/kit_SBE/run_VGCF3_PTFE1_20260827_134104_3672586/` | `601a887701420ea3` ✓ |
| **DBE** | `/home/kgy/sdcp/kit_DBE/run_VGCF3_PTFE0.5_SDCP0.5_20260827_150029_3687585/` | `ec903b552319a935` |

킷 루트(`/home/kgy/sdcp/kit_SBE/`)에 `am_scaffold.csv` · `se_scaffold.csv` · `mpm_input.json` ·
`run_mpm.sh` · `harvest.sh` · `latest_run`.  런 디렉터리에 `se_dump.npy` · `se_dump_eps.npy` ·
`phase.npy` · `fibre.npy` · `fibre_dia.npy` · `mpm_metrics.json`.

## ★ 원고 payload 는 arm `.sh` 가 아니다

런 디렉터리의 `p2_{SBE,DBE}_sph_a{0..7}.*.sh` 37+개는 **SR-01 origin 앙상블** 팔이고
**`--no-field`** 다 ⇒ 점군·joule 을 안 만든다.  원고 payload 는 필드·joule·이온·collector 를
전부 갖고 있으므로 킷의 **`run_mpm.sh` STEP 2** 산출이다.

⇒ **MPM 압밀(STEP 1)을 다시 돌릴 필요가 없다** — `se_dump.npy` 가 그대로 있다.
`mpm_run.log` 가 그 재실행법을 직접 적어 둔다:

```bash
cd /home/kgy/sdcp/kit_SBE/run_VGCF3_PTFE1_20260827_134104_3672586
sed -n '/mpm_webapp_payload/,/--out mpm_payload.json/p' /home/kgy/sdcp/kit_SBE/run_mpm.sh > payload_only.sh
bash payload_only.sh
```

⚠ 이 런의 STEP 2 는 당시 **실패**했다 (`mpm_payload.json.failed`, 흔한 원인 = pip 모듈 누락:
`scikit-image` · `scipy`).  원고 payload 는 다른 시도에서 성공했다 (09-02 업로드).
⇒ 재실행 전에 그 모듈을 먼저 확인한다.

## 코드 위치 — **`/home/kgy/dem-mt/scripts`**

arm `.sh` 의 `SCR="/home/kgy/dem-mt/scripts"`.  ⇒ 재실행 전에 **거기**가 고쳐진 판인지 본다
(uma 의 리포가 아니다):

```bash
cd /home/kgy/dem-mt && git status -sb | head -3 && git log --oneline -1
grep -c percentile_basis scripts/mpm_webapp_payload.py        # 1 이어야 함 (0 = 옛 코드)
python3 scripts/step3_sigma.py --selftest 2>&1 | grep -E "field-stats|joule-stats"   # 다섯 줄 OK
```

## 검수 조건 (변경 없음)

`σ_e_eff` 가 **0.054530439566226836 (SBE)** · **0.0714004401030127 (DBE)** 로 소수점까지
재현될 것.  SELF-45 패치는 통계·정규화만 건드렸으므로 물리는 비트 동일해야 한다.
⚠ 재현 안 되면 **멈춘다** — 다른 침대로 비교하면 무효다.

## 부수 관찰

- arm `.sh` 에 `--step3-vox 0.4` 가 먼저 나오고 뒤에 `--step3-vox 0.15` 가 다시 나온다
  (argparse 는 뒤가 이긴다 = 0.15).  manifest 와 일치하므로 무해하지만 **읽을 때 헷갈린다**.
- `--sigma-ion-sdcp 0` (arm) vs 원고 manifest `sigma_ion_sdcp 0.001` ⇒ **arm 과 원고 런은
  플래그가 다르다**.  한 번 더 확인: 재실행은 반드시 **`run_mpm.sh` 의 STEP 2** 에서 뽑는다.

## I-2. ⚠ 정정 — `run_mpm.sh` 의 STEP 2 **도** 원고 명령이 아니다 (실측)

§I 에서 *"원고 payload 는 킷 `run_mpm.sh` STEP 2 산출"* 이라고 적었는데 **틀렸다.**
그 명령을 실제로 뽑아 보니 `--step3-vox 0.4` 이고 **p2 플래그가 하나도 없다**:

```
--n-vox 192 --tri-step 4 --smooth 1.5 --target-porosity 0.0759 --eps se_dump_eps.npy
--dilate-z 1.0719 --void-max 180000 --step3-vox 0.4 --field-max-points 90000 --step3-gpu
--joule-heat --metrics-json mpm_metrics.json --case 260714_145738_778fa4 --phase phase.npy
--fibre fibre.npy --fibre-dia fibre_dia.npy --collector-rint 110 ... --out mpm_payload.json
```

원고 manifest 는 `vox 0.15` · `bridge_um 0.48` · `ptfe_stamp centerline` ·
`fibre_stamp segment` · `sdcp_stamp sphere(0.3)` · `sigma_vgcf 78.5398` ·
`sigma_ion_sdcp 0.001` 이다 ⇒ **둘 다 아니다.**

| 후보 | 물리 축 | 필드 | 판정 |
|---|---|---|---|
| arm `p2_*_a0.*.sh` | **p2 맞음** (`--expect-physics` 계약까지 있음) | ⛔ `--no-field` | 점군·joule 없음 |
| 킷 `run_mpm.sh` STEP 2 | ⛔ vox 0.4 · p2 플래그 없음 | ✅ 필드·joule | 격자가 다름 |
| **원고 payload** | p2 (vox 0.15) | ✅ 필드·joule·이온·collector | **제3의 명령** |

⇒ 원고 payload 는 **따로 손으로 만든 명령**(또는 `payload_only.sh` 류)의 산출이다.
**⬜ 다음 세션 첫 일**: kgy 에서 그 명령의 흔적을 찾는다 —
```bash
ls -la /home/kgy/sdcp/kit_SBE/*.sh /home/kgy/sdcp/kit_SBE/run_*/payload*.sh 2>/dev/null
grep -rl 'step3-vox 0.15' /home/kgy/sdcp/ 2>/dev/null | head
grep -n 'step3-vox 0.15' ~/.bash_history 2>/dev/null | tail -5
```

못 찾으면 **arm `.sh` 에서 조립한다** (그쪽이 물리 축이 맞으므로):
`--no-field` 제거 · `--sigma-ion-sdcp 0` → **`0.001`** · `--out` 변경.
⚠ 그 조립의 **유일한 안전장치 둘**: ① arm `.sh` 에 이미 있는
`--expect-physics vox_um=0.15,bridge_um=0.48,…` 계약검사 ② σ_e 재현
(0.054530439566226836 / 0.0714004401030127).  둘 다 통과해야 그 명령이 맞다.

## I-3. kgy 환경 — 실행 전에 고쳐야 할 것 셋 (실측)

| # | 실측 | 조치 |
|---|---|---|
| 1 | `/home/kgy/dem-mt` 가 **detached HEAD** `17f5f017` · `percentile_basis` **0** = 옛 코드 | 브랜치로 돌린 뒤 pull.  ⚠ detached 라 로컬 변경이 있는지 먼저 확인 |
| 2 | `step3_sigma --selftest` 가 `field-stats*` 를 **한 줄도 안 냄** (옛 코드 확인) | 위 1 뒤 다섯 줄 OK 확인 |
| 3 | `(base)` conda 에 **`skimage` 없음** — 2026-08-27 STEP 2 가 실패한 그 원인 | 그 런을 성공시킨 env 를 찾거나 설치 |

⚠ 3 이 중요하다: **원고 payload 를 만든 env 는 이것이 아니다** (여기선 STEP 2 가 죽었다).
`meta.json` 의 `exec_env.python = /home/kgy/dem-venv/bin/python3` (3.8.10) 가 그 env 다 —
`(base)` conda 가 아니라 **`/home/kgy/dem-venv`** 를 써야 한다.

## I-4. 실측 마무리 (2026-09-22 밤) — env 확정 + 남은 단서

- ✅ **env 확정**: `/home/kgy/dem-venv/bin/python3` 에 `skimage`·`scipy`·`numpy` **있다**
  (`(base)` conda 에는 없다).  `meta.json` 의 `exec_env.python` 과 일치 ⇒ **재실행은 반드시
  이 python 으로.**  2026-08-27 STEP 2 가 죽은 것은 `(base)` 로 돌렸기 때문이다.
- ⛔ `kit_SBE` 에 `payload*.sh` 가 **없다** (`harvest.sh`·`run_a1_anchors.sh`·`run_mpm.sh` 뿐).
  `~/.bash_history` 에도 `step3-vox 0.15` 매치가 없다 ⇒ 원고 명령은 **파일로 안 남았다**.
- ★ **단서**: DBE 의 **08-12** 런 폴더에 `LDBE_v015_pt.sh` 라는 **손으로 만든** 스크립트가 있다
  (`_pt` = 점 스탬프로 보이므로 원고(구 스탬프)와는 다를 수 있다).  그런 일회성 스크립트가
  런 폴더에 저장된다는 뜻이므로 ⬜ **SBE 08-12 폴더를 먼저 볼 것**:
  `ls /home/kgy/sdcp/kit_SBE/run_VGCF3_PTFE1_20260812_204806_75857/*.sh | head -20`

### ⇒ 다음 세션의 두 경로

**(A) 흔적이 있으면** 그 스크립트를 쓴다 (`--out` 만 변경).
**(B) 없으면 arm `.sh` 에서 조립한다** — 물리 축이 맞는 유일한 후보다:
```
arm p2_SBE_sph_a0.*.sh 에서
  · `--no-field` **제거**            (점군·joule 을 만들어야 한다)
  · `--sigma-ion-sdcp 0` → `0.001`   (원고 manifest 값)
  · `--out` 을 새 파일로
  · python 을 /home/kgy/dem-venv/bin/python3 로
  · 나머지 플래그는 **한 글자도 건드리지 않는다**
```
⚠ 조립의 안전장치는 **둘뿐이고 둘 다 통과해야 한다**:
① arm `.sh` 에 이미 박힌 `--expect-physics vox_um=0.15,bridge_um=0.48,sigma_vgcf_S_cm=78.5398,
fibre_stamp=segment,sdcp_stamp=sphere,sdcp_yield_to_vgcf=False,periodic_xy=False,ptfe_stamp=centerline`
② **σ_e 재현** = `0.054530439566226836` (SBE) · `0.0714004401030127` (DBE).
⛔ 둘 중 하나라도 어긋나면 **멈추고 보고** — 다른 침대·다른 규약으로 비교하면 무효다.

⚠ `--no-field` 를 떼면 `--no-thermal --no-pore --no-collector --no-step4 --no-trackb` 는
그대로 둔다 (원고 manifest 의 component 표와 일치: thermal/pore/pnm/collector_geom = disabled).

## I-5. 탐색 종료 — **경로 (B) 확정** + 조립된 명령 (2026-09-22 밤)

`LSBE_v015_sph.sh` 는 원고 명령이 **아니다**: `--step3-rasterize-only
/home/kgy/sdcp/phase_ledger/ledger_SBE_v015_sph.json` 에 `--out unused_SBE_v015_sph.json` 이다
= **상별 부피 원장(CL-25) 전용**이라 솔브 전에 종료한다.  (`SCR` 도 `/home/kgy/dem-sk/scripts`
로 **세 번째** 코드 경로다.)

⇒ 저장된 스크립트 중 원고 명령은 **없다**.  **arm `.sh` 에서 조립한다.**

### 조립 규칙 (arm → 원고) — 네 곳만 바꾼다

| 바꾸는 것 | 이유 |
|---|---|
| `--no-field` **삭제** | 점군·joule 을 만들어야 한다 (원고 payload 에 있다) |
| `--sigma-ion-sdcp 0` → **`0.001`** | 원고 manifest 값 (SBE 엔 SDCP 상이 없어 물리 무영향, 기록 일치용) |
| `--out p2_SBE_sph_a0.json` → **새 이름** | 옛 산출을 덮지 않는다 |
| `python3` → **`/home/kgy/dem-venv/bin/python3`** | `(base)` 엔 skimage 가 없다 (2026-08-27 STEP 2 사망 원인) |

**그 밖의 플래그는 한 글자도 건드리지 않는다.**  특히 `--no-thermal --no-pore --no-collector
--no-step4 --no-trackb` 는 **유지** (원고 manifest 의 component 표와 일치).  `--collector-rint
110 --collector-name … --collector-scenario sbe` 도 유지 — `--no-collector` 는 기하 계산만
끄고 시나리오 후처리는 남는다 (원고 manifest 가 정확히 그 모양이다).

### SBE 실행 명령 (런 디렉터리 = **08-27**, `se_dump.npy` 가 거기 있다)

```bash
cd /home/kgy/sdcp/kit_SBE/run_VGCF3_PTFE1_20260827_134104_3672586
KIT=/home/kgy/sdcp/kit_SBE
/home/kgy/dem-venv/bin/python3 /home/kgy/dem-mt/scripts/mpm_webapp_payload.py \
  --se se_dump.npy --scaffold "$KIT/am_scaffold.csv" --se-dump "$KIT/se_scaffold.csv" \
  --n-vox 192 --tri-step 4 --smooth 1.5 --target-porosity 0.0759 --eps se_dump_eps.npy \
  --dilate-z 1.0719 --void-max 180000 --step3-vox 0.4 --field-max-points 90000 --step3-gpu \
  --joule-heat --metrics-json mpm_metrics.json --case 260714_145738_778fa4 \
  --phase phase.npy --fibre fibre.npy --fibre-dia fibre_dia.npy \
  --collector-rint 110 --collector-name bare_Al+SBE_electrode --collector-scenario sbe \
  --save-step4-grid step4_grid_SELF45_SBE.npz \
  --step3-fibre-stamp segment --sigma-vgcf 78.5398 --step3-vox 0.15 --step3-bridge-um 0.48 \
  --step3-origin-shift 0 0 0 --step3-sdcp-sphere-d 0.30 --ptfe-stamp centerline \
  --step3-require-gpu \
  --expect-physics vox_um=0.15,bridge_um=0.48,sigma_vgcf_S_cm=78.5398,fibre_stamp=segment,sdcp_stamp=sphere,sdcp_yield_to_vgcf=False,periodic_xy=False,ptfe_stamp=centerline \
  --sigma-ion-sdcp 0.001 --sigma-ion-se 0.003 \
  --no-step4 --no-thermal --no-trackb --no-pore --no-collector \
  --out payload_SELF45_SBE.json
```

⚠ **DBE 는 그쪽 arm `.sh`(`p2_DBE_sph_a0.*.sh`)에서 같은 네 곳만 바꿔 조립한다** — 베껴 쓰지
말 것 (`--collector-rint 46` · `--collector-scenario dbe` 등이 다르고, SDCP 가 실재해
`--sigma-ion-sdcp` 가 **물리에 영향**을 준다).

### ⛔ 실행 전 · 후 검수 (둘 다 통과해야 한다)

1. **코드**: `/home/kgy/dem-mt` 가 detached HEAD `17f5f017` (옛 코드)다.  브랜치로 돌려 pull 하고
   `grep -c percentile_basis scripts/mpm_webapp_payload.py` → **1**,
   `step3_sigma --selftest` 의 `field-stats*`·`joule-stats*` **다섯 줄 OK**.
2. **σ_e 재현**: `0.054530439566226836` (SBE) · `0.0714004401030127` (DBE) — 소수점까지.
   어긋나면 **멈추고 보고**한다 (다른 침대·다른 규약으로 비교하면 무효).
   ⚠ `--expect-physics` 계약검사가 실행 **전에** 한 번 더 막아 준다.

### 성공 판정

새 payload 를 복원기에 넣어 `✅ 이미 전수 기준 (SELF-45 이후 payload)` 가 나오면 그 안의
`field_scale_e/ion` 이 **최종값**이다.  그것으로 §H 회신문의 이온 문단을 교체하고,
p99.8 정확값·Figure S14/S15 를 마무리한다.

## I-6. ⛔ kgy 코드 리포는 건드리지 말 것 · 실행은 **uma(V100)** 에서 (2026-09-22 밤)

`/home/kgy/dem-mt` 에서 `git checkout claude/stoic-knuth-NObVQ && git pull` 을 시도하니
**`ahead 2188, behind 3038`** 로 갈라져 있고 `CLAUDE.md`·`README.md`·`litdb/**`·`webapp/**` 등
거의 모든 파일이 **`add/add` 충돌**을 냈다 = 같은 브랜치 이름을 쓰는 **별개 이력**이다.
⇒ `git merge --abort` 로 중단했다.  ⛔ **그 리포를 정본에 맞추려 들지 말 것** — 해결하려면
2000 커밋 규모의 이력 수술이고 이번 일과 무관하다.  kgy 는 **데이터 공급원**으로만 쓴다.

⚠ 인계 §7 #7 이 *"`~/runyourai/1/Yonghoon-DEM-DFT` 는 git 리포가 아니다"* 라고 적었는데
실측은 **git 리포다** (오늘 pull 로 최신화됐고 selftest 다섯 줄 OK).  낡은 항목이다.
진짜 위험한 자리는 그쪽이 아니라 **`/home/kgy/dem-mt` 의 갈라진 이력**이었다.

### 실행 계획 (확정)

코드는 **uma 의 `~/runyourai/1/Yonghoon-DEM-DFT`** (최신·검증됨), 데이터는 kgy 에서 scp.

입력 크기 (케이스당 **≈ 1.63 GB**, 8 파일):
`se_dump.npy` 778M · `se_dump_eps.npy` 260M · `fibre.npy` 260M · `fibre_dia.npy` 260M ·
`phase.npy` 65M · `se_scaffold.csv` 5.5M · `am_scaffold.csv` 52K · `mpm_metrics.json` 4K.
(수백 개의 `p2_*.sh`·`step4_grid_*.npz` 는 **옮기지 않는다**.)

⇒ 명령 전문은 아래 §I-7.

---

## I-7. 전송 실측 + v100 실행 명령 (2026-09-22 밤)

⚠ §I-6 마지막 줄이 이 절을 가리켜 놓고 **비어 있었다**.  아래가 그 내용이다.

### I-7-a. 전송 — kgy → v100 **직송**이 답이었다 (실측)

옛 계획의 `kgy → WSL → v100` tar-pipe 중계는 **0.57 MiB/s**(단일) 였고 케이스당 ~50 분으로
추정됐다.  세 번 시도해 세 번 다 실패·중단했다.  실제로 통한 경로:

| 관문 | 실측 |
|---|---|
| kgy 가 `machine.runyour.ai` 를 푸는가 | **예** — `101.79.28.40`, 배너 `SSH-2.0-SSHPiper` |
| 키를 kgy 에 두지 않고 되는가 | **예** — WSL 에서 `ssh-add v100.pem` 후 `ssh -A kgy` (에이전트 포워딩) |
| 한 방 tar-pipe | ⛔ **안 된다** — 게이트웨이가 `Connection closed by remote host` 로 끊는다 (2/2) |
| rsync | v100 에 **없었다** → `apt-get install -y rsync` 로 설치 |
| rsync + 재시도 루프, **단일 스트림** | ✅ **SBE 8/8 · 1분 30초** |

실측 SBE: `total 1,703,831,562 B` · 회선 위 **702 MB** (`speedup 2.43`) · 평균 7.36 MB/s ·
`fibre_dia.npy` 는 **205 MB/s** (상수 배열이라 압축이 거의 다 먹는다) · `rc=0`.

★ **교훈 세 줄** — ⓐ 병목은 "WSL 을 거치는 것" 이 아니라 **집 업링크를 3.3 GB 가 두 번 타는 것**
이었다.  Windows Downloads 경유는 구간을 하나도 안 줄이므로 **더 느리다**(디스크 왕복 추가 ·
`/mnt/c` = drvfs).  ⓑ **이 게이트웨이에 한 방 파이프를 쓰지 말 것** — 끊기면 전부 날아간다.
`rsync --partial --append-verify` 는 `tar` 가 남긴 반쪽 파일도 **정확한 prefix 라 이어받는다**.
ⓒ **동시 2세션이 끊김의 방아쇠로 의심**된다 (둘 다 같은 메시지로 죽었고, 단일 스트림에서는
한 번도 안 끊겼다) ⇒ **순차로 돌린다.**

재현 명령 (SBE; DBE 는 `kit_DBE` · 런디렉터리 · `dbe` 로 바꿈):

```bash
# WSL 에서 한 번 — 키는 에이전트에만 (kgy 디스크에 .pem 을 두지 않는다)
eval "$(ssh-agent -s)"; ssh-add ~/.ssh/v100.pem

ssh -A kgy '
R=/home/kgy/sdcp/kit_SBE/run_VGCF3_PTFE1_20260827_134104_3672586
K=/home/kgy/sdcp/kit_SBE
n=0
until rsync -av --partial --append-verify -z --progress \
    --rsync-path="mkdir -p ~/runyourai/1/rerun/sbe && rsync" \
    -e "ssh -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30 -o ServerAliveCountMax=6" \
    "$R/se_dump.npy" "$R/se_dump_eps.npy" "$R/phase.npy" "$R/fibre.npy" "$R/fibre_dia.npy" \
    "$R/mpm_metrics.json" "$K/am_scaffold.csv" "$K/se_scaffold.csv" \
    ubuntu@machine.runyour.ai:~/runyourai/1/rerun/sbe/ ; do
  n=$((n+1)); [ $n -ge 30 ] && { echo "GAVE UP after $n"; break; }
  echo "--- 끊김, 재시도 $n (15초 후) ---"; sleep 15
done
echo "RSYNC EXIT rc=$?"
'
```

⚠ 에이전트 환경변수(`SSH_AUTH_SOCK`)는 **셸 단위**다 — 새 창을 열면 포워딩이 깨진다.

### I-7-b. 지문 검수 결과 (2026-09-22, v100 `~/runyourai/1/rerun/`)

```bash
ssh v100 'for d in sbe dbe; do echo "== $d =="; cd ~/runyourai/1/rerun/$d && \
  for f in phase.npy fibre.npy fibre_dia.npy mpm_metrics.json; do \
    echo "$(sha256sum $f | cut -c1-16)  $f"; done; done'
```

| | `phase` | `fibre` | `fibre_dia` | `metrics_json` |
|---|---|---|---|---|
| **SBE** (봉인 매니페스트 대조) | `601a887701420ea3` ✅ | `bf5ff65dd265d540` ✅ | `95d320717868a4d0` ✅ | `7b81d62524b74fca` ✅ |
| **DBE** | `ec903b552319a935` ✅ | `ec20195cc44297d4` ★ | `b164870ad1b3f960` ★ | `17fd3a6d612768a6` ★ |

★ = **이번에 처음 기록되는 값**.  DBE 는 §I 표에 `phase` 지문만 있었다 (나머지 셋은 DBE
`meta.json` 을 안 열어 봐서 대조 기준이 없다).  ⇒ 이 세 값은 **대조가 아니라 측정**이다 —
DBE 의 침대 동일성은 `phase` 일치 + `--expect-physics` 계약검사 + **σ_e 소수점 재현**이 닫는다.
DBE `meta.json` 의 `input_digest` 표를 나중에 열게 되면 여기에 대조를 추가할 것.

### I-7-c. ⛔ 실행 **전** 관문 (셋 다 통과해야 한다)

```bash
ssh v100 'cd ~/runyourai/1/Yonghoon-DEM-DFT && git log --oneline -1 && \
  echo "--- percentile_basis (1 이어야 함) ---" && \
  grep -c percentile_basis scripts/mpm_webapp_payload.py && \
  echo "--- step3 selftest (다섯 줄) ---" && \
  python3 scripts/step3_sigma.py --selftest 2>&1 | grep -E "field-stats|joule-stats"'
ssh v100 'nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv'
```

1. `grep -c percentile_basis` = **1** (0 이면 옛 코드 — 같은 편향값이 또 나오고 이번엔 그걸
   정답으로 믿게 된다).
2. selftest 가 `field-stats-fixture` · `field-stats-budget-invariant` · `field-stats-nonvacuous` ·
   `field-stats-markov` · `joule-stats-budget-invariant` **다섯 줄**을 OK 로 낸다.
3. GPU 가 비어 있다 (`--step3-require-gpu` · 26.4 M dof × 415 B ≈ **11 GB**).

### I-7-d. SBE 실행 명령 — **v100 판** (§I-5 를 경로만 바꾼 것)

§I-5 의 kgy 판에서 바뀐 곳은 **경로 셋뿐**이다: 파이썬(`/home/kgy/dem-venv/bin/python3` →
v100 `python3`) · 스크립트(`/home/kgy/dem-mt/scripts/` → uma 리포) · `$KIT` (scaffold CSV 두 개가
이제 런 디렉터리에 같이 있으므로 맨 이름).  **플래그는 한 글자도 안 바꾼다.**

```bash
ssh v100
cd ~/runyourai/1/rerun/sbe
REPO=~/runyourai/1/Yonghoon-DEM-DFT
python3 $REPO/scripts/mpm_webapp_payload.py \
  --se se_dump.npy --scaffold am_scaffold.csv --se-dump se_scaffold.csv \
  --n-vox 192 --tri-step 4 --smooth 1.5 --target-porosity 0.0759 --eps se_dump_eps.npy \
  --dilate-z 1.0719 --void-max 180000 --step3-vox 0.4 --field-max-points 90000 --step3-gpu \
  --joule-heat --metrics-json mpm_metrics.json --case 260714_145738_778fa4 \
  --phase phase.npy --fibre fibre.npy --fibre-dia fibre_dia.npy \
  --collector-rint 110 --collector-name bare_Al+SBE_electrode --collector-scenario sbe \
  --save-step4-grid step4_grid_SELF45_SBE.npz \
  --step3-fibre-stamp segment --sigma-vgcf 78.5398 --step3-vox 0.15 --step3-bridge-um 0.48 \
  --step3-origin-shift 0 0 0 --step3-sdcp-sphere-d 0.30 --ptfe-stamp centerline \
  --step3-require-gpu \
  --expect-physics vox_um=0.15,bridge_um=0.48,sigma_vgcf_S_cm=78.5398,fibre_stamp=segment,sdcp_stamp=sphere,sdcp_yield_to_vgcf=False,periodic_xy=False,ptfe_stamp=centerline \
  --sigma-ion-sdcp 0.001 --sigma-ion-se 0.003 \
  --no-step4 --no-thermal --no-trackb --no-pore --no-collector \
  --out payload_SELF45_SBE.json 2>&1 | tee run_SELF45_SBE.log
```

⚠ `--step3-vox` 가 두 번 나오는 것은 **원본 그대로**다 (0.4 뒤에 0.15 — argparse 는 뒤를 쓴다).
고치지 말 것 — 봉인 명령에서 한 글자라도 바꾸면 *"무엇이 달라졌나"* 를 따로 증명해야 한다.
실제 적용값은 `--expect-physics vox_um=0.15` 가 **실행 전에** 검증한다.
(⚠ `input_digest` 는 **파일 내용만** 덮으므로 명령 문자열의 보증이 아니다 — CLAUDE.md 규율 ⑤.)

### I-7-e. DBE 실행 명령 — ⬜ **아직 조립 안 됨**

§I-5 가 *"DBE 는 그쪽 arm `.sh`(`p2_DBE_sph_a0.*.sh`)에서 같은 네 곳만 바꿔 조립한다 — 베껴
쓰지 말 것"* 이라고 못 박는다.  다른 값: `--collector-rint 46` · `--collector-scenario dbe` ·
`--case` · `--target-porosity` · `--dilate-z` · `--sigma-ion-sdcp`(SDCP 가 실재해 **물리에
영향**) 등.  ⇒ SBE 를 베끼면 **다른 물리를 돌리게 된다.**

조립에 필요한 원본:
```bash
ssh kgy 'ls /home/kgy/sdcp/kit_DBE/run_VGCF3_PTFE0.5_SDCP0.5_20260827_150029_3687585/p2_DBE_sph_a0.*.sh'
ssh kgy 'cat <위에서 나온 파일>'
```

### I-7-f. 수용 판정

`σ_e` 가 **`0.054530439566226836`**(SBE) · **`0.0714004401030127`**(DBE) 로 **소수점까지**
재현되면 같은 침대·같은 물리가 증명되고, 그 payload 의 `field_scale_e/ion` 이 **최종값**이다.
⛔ 어긋나면 **멈추고 보고**한다 (다른 침대·다른 규약으로 비교하면 무효).
