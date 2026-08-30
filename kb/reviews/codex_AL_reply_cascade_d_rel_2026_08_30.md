---
title: "회신 AL 접수 — NO-GO. 내 '같은 구조' 전제가 틀렸다"
date: 2026-08-30
kind: review_reply
status: 접수
tags: [cascade, doping, d_rel, prereg, anneal, estimand, review/codex]
---

# 회신 AL 접수 — **NO-GO** (본계산 312 GPU-h · 5×2 파일럿 **둘 다** 금지)

결론은 우리가 낸 Q1 (a) 와 같지만 **이유가 더 심각하다**: 지금 문제는 predictor 저신뢰도가
아니라 **target–구조–predictor estimand 가 서로 연결돼 있지 않은 것**이다.

---

## 0. ⛔ 우리가 틀린 것 — **실측으로 확인했다**

리뷰 P0-3 의 지적: 우리가 동일성 물증으로 쓴 `screen_de_per_atom` 은 **anneal 전** 값인데,
정작 채점 축(BVS 프록시·탄성 G)은 **500 K anneal 뒤** `post_relax.xyz` 에서 계산된다.

정본 CSV 전수 확인:

| | 1e-4 안에서 일치하는 삼중쌍 |
|---|---:|
| `screen_de_per_atom` (anneal **전** — 우리가 본 것) | **110 / 227** |
| `anneal_E_post_per_atom` (anneal **후** — 축이 계산되는 구조) | **0 / 227** |

post-anneal 에너지 상대산포: 중앙 **6.0e-3** · 최대 **2.8e-2**.
예 `Ag2O_cLi24gaS16e_s00` 삼중쌍 —
E_post = **−4.1964 / −4.1888 / −4.1113** eV/atom, ΔV = **−7.97 / −3.69 / −2.85 %**.
(리뷰가 인용한 값과 정확히 같다.)

**원인**: `tools/doping/run_anneal.py` 가 Langevin RNG·초기속도 seed 를 **받지도 기록하지도
않는다.** 비결정적 anneal 이 복제본마다 다른 endpoint/basin 으로 간다.

⇒ **철회**: *"같은 구조를 세 번 쟀다"*.
⇒ **살아남음**: ρ(예측기 0.22 · BVS 0.08) 과 front Jaccard(0.23–0.27) 는
**`config → anneal → axes → score → rank/front` 파이프라인 재실행의 불안정성**으로는 유효하다.
*동일 구조의 metric 재현성* 은 이 CSV 로 **잴 수 없다**.

⇒ **또 철회**: ρ 0.22 를 D 와의 상관 **상한**으로 쓴 것. 고전 감쇠식이라면 감쇠계수는
√0.22 ≈ 0.47 이고, Spearman·중앙값·이분산 anneal 에는 그것조차 정확히 안 맞는다.
그리고 median-of-3 신뢰도 0.75 와 재검사 ρ 0.22 는 **같은 양이 아니다**
(분산성분 추정 vs 잡음 복제본 간 순위상관) — 어긋난다고 말한 것도 틀렸다.

**도구 수정** (`tools/doping/axis_corr_csv.py`):
`IDENTITY_PROBE` → `anneal_E_post_per_atom` · 시드 삼중쌍을 정렬해 결정론적으로 고르고
미사용 시드를 센다(초판 `full[0]` 은 **순서 의존**이었다 — 리뷰 지적) ·
엄격판이 0개면 사유를 설명하고 `--loose_identity` 값이 무엇인지 명시.
음성시험 신설: *"anneal 전이 일치해도 후가 갈리면 동일 구조가 아니다"*.

---

## 1. 접수한 P0 (우리가 묻지 않은 것)

**P0-1 — 39 target 은 실제 구조 39개가 아니다.**
이름은 전부 `x020_s00` 인데 `aggregate_designs` 는 **축마다 독립적으로** 중앙값을 낸다.
⇒ 4축 벡터가 어느 실제 행에도 없는 **합성 벡터**다 (35/39). 이름의 행이 네 중앙값을
모두 가진 경우는 **1/39**. `n_replicates=15` 도 축별 반복이 아니라 그룹 전체 행 수다.
지금 s00 구조를 만들어 MD 를 돌리면 **predictor(config A) 와 D(config B)** 를 상관시킨다.

**P0-2 — 얼린 predictor 정의가 집계와 불일치.**
`median(3m+b) ≠ 3·median(m) + median(b)`. **우리 실측: 227설계 중 169개가 다르다
(최대차 0.0696).** 리뷰는 front 39 중 24개 불일치·순위 최대 11계단 이동을 보고했다.
*"행별 score 후 집계"* 인지 *"축 집계 후 score"* 인지 먼저 확정해야 한다.

**P0-4 — 실패 가지가 통계적으로 성립하지 않는다.**
`|ρ|<0.2 ⇒ 이동도 축 근거 없음` 은 **삭제**. n=39 에서 ρ̂=0 이어도 Fisher 95% 구간이
약 ±0.31 이다 — 작은 점추정은 무효 입증이 아니라 **정밀도 부족으로 판정 불가**다.
±0.2 동등성에는 이상적 조건에서도 n≥69. 게다가 39개는 30 dopant·10여 구조환경에 묶여
**독립 표본이 아니다** (top 10 중 7개가 같은 환경군).

**P0-5 — tracer D 는 300 K 전도도 게이트가 아니다.**
`σ_i/σ_h = (n_Li,i/n_Li,h)(D*_i/D*_h)(H_R,h/H_R,i)`.
39조성의 Li 수는 host 24 대비 **18–28** 이라 D* 비가 같아도 σ비가 같지 않다.
Deng 의 7%/31% 는 **표면 코팅 LPSC 의 상온 pellet EIS** 라 25% bulk 치환 문턱으로
옮길 외적 타당성이 없다. **0.90 은 물리 게이트가 아니라 임의 운영 cutoff.**

---

## 2. 채택하는 처방

| 질문 | 판정 |
|---|---|
| Q1 | (a) — 단 **수정이 아니라 v2 신규 동결**. v1 은 무효 사유와 함께 **보존**하고 덮어쓰지 않는다. label 미열람·변경 이유·수리 성공조건·코드/데이터/구조 hash 기록. v1 결과를 나중에 confirmatory sensitivity 로 부활시키지 않는다 |
| Q2 | 원인 진단이 **target D 보다 선행**. 1순위 원인은 후처리 RNG 가 아니라 **seed 없는 stochastic anneal**. 병렬 허용은 런처 개발과 **39 밖 sentinel** 기술시험뿐 |
| Q3 | 3.7% 수렴 철회는 맞지만 **"2×2×2 미수렴 확정"은 과하다** (한 시드·중첩 prefix·크기와 형상 혼입·다른 LPSOCl 셀). 지금 잴 수 있는 건 `D̂_rel(C_i, C_h, 600 K, 2–50 ps, s_config, s_velocity)` 뿐. 같은 `2×2×2` 라벨도 같은 물리 셀이 아니다 (총원자 48–56, Li 18–28) |
| Q4 | 산술은 맞다. **선택은 ②** — estimand 를 `600 K 고정 프로토콜의 tracer D_rel` 로 한정하고 **σ(300 K)·Deng 문턱 삭제**. ①(2온도)는 **반대** — `ln R₃₀₀ = 5 ln R₆₀₀ − 4 ln R₈₀₀` 라 잡음이 1.55–2.13배로 증폭되고 곡률·상변화도 못 본다 |
| Q5 | 1시드 게이트 **반대**. 8.4% 자체가 n=3·다른 셀이라 실제 SD 95% 범위가 4.4–52.8%. **host 3시드는 주기준을 개선하지 않는다** (Spearman 에서 host 분모가 정확히 소거된다). 절대 게이트에선 host 가 **공통 오차**라 pass/fail 을 독립 시행으로 세면 안 된다. 최소 설계당 ≥2 velocity seed · host ≥3, 게이트 근처는 3시드 |
| Q6 | 제안한 rank-spaced 5×2 파일럿은 **격리 실패** — predictor–outcome 방향과 게이트 위치를 보게 되고, 제외해도 오염이 남으며 confirmatory n 이 39→34 로 바뀐다. 허용 경로는 ① 39 밖 sentinel 기술 파일럿 ② 대상·순위 blind + 적응규칙 사전동결 ③ 이번을 exploratory 로 선언하고 fresh set 으로 v2 |

⚠ 검정력 정정: n=39 에서 **진짜** ρ=0.35 여도 기준 통과확률은 약 **50%**,
80% power 에는 기대 ρ≈**0.47** 이 필요하다. 우리가 쓴 *"필요 산포 9%"* 는 power 가 아니라
강한 가정 아래의 눈금일 뿐이다.

---

## 3. 실행 승인 해제조건 (8개, 전부 충족 전 금지)

1. target 을 **실제 구조 ID 또는 명시적 config ensemble** 로 재정의 + source observation·
   method·seed·좌표 hash 연결
2. anneal RNG 와 구조 계보 봉인 · predictor 집계식 **하나로 확정**
3. **전 seed** end-to-end 재실행으로 score·rank·front 안정성 재측정
4. v1 보존한 채 **label-blind v2** 를 새 hash 로 동결
5. `|ρ|<0.2 ⇒ 축 근거 없음` **삭제** + cluster 의존성·검정력·불확실성 규칙 신설
6. estimand 를 **cell-conditioned 600 K tracer D_rel** 로 제한, Deng/300 K σ 게이트 제거
7. 구조 builder·런처·manifest + framework retention·phase/melting·β/hop·MLIP applicability·
   invalid-run 처리 규칙 봉인
8. 39 밖 기술 파일럿 **또는** 사전 고정된 blinded internal-pilot 통과

부수: 탄성 G 가 스크립트에선 `clamped-ion Cij` 로 불리는데 실제 finite-strain 단계에서는
원자 내부좌표를 **다시 이완**한다. strain 별 수렴·branch switching 기록도 없다 — **G 정의부터**
고쳐야 한다.

## 4. 최종

순서 1→2 는 맞다. **3번(5×2 파일럿)으로 바로 가면 안 된다.**
합성 target · 구조 계보 · predictor 정의 · stochastic anneal 을 먼저 고친다.
그 뒤 이 캠페인은 *"600 K 조건부 tracer-mobility descriptor 검증"* 으로는 살릴 수 있지만,
*"300 K 전도도 0.90 게이트"* 로는 **살릴 수 없다**.
