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
