---
title: "회신 BL 대응 — NO-GO 수용(추가 MD·C3 실행 0), 감사 GO 항목 전부 착수: 개정안(post-hoc)·C3 도구 2판·C6 원장 등록"
date: 2026-09-11
updated: 2026-09-11
tags: [review, codex, reply, lpsocl, closure, gate, arrhenius, framework, post-hoc]
status: 진행
kind: review-reply
system: lpsocl
confidence: medium
verificationStatus: verified
verifiedAt: 2026-09-11
verifiedBy: agent
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

# 회신 BL 대응 — 추가 MD 0 으로 규칙·도구 결함부터 닫는다

> 회신 원문: `kb/reviews/codex_BL_reply_lpsocl_gate_ambiguity_2026_09_11.md` (미수정 보관)
> 요청문: `kb/reviews/codex_BL_prompt_lpsocl_gate_ambiguity_2026_09_11.md`
> 한줄: **NO-GO(추가 MD · 지금 C3 실행) 수용. 감사 GO 항목은 이 커밋에서 전부 착수했다.** 곧바로 "전체 no_value" 도 아니다 — C6 은 `not_assessed` 다.

## 0. 회신의 사실 주장 감사 — 6건 전부 확인

| # | 회신 주장 | 우리 확인 | 결과 |
|---|---|---|---|
| 1 | 09-01 개정 R1 "온도별 3시드 중 2개 이상 → 3점" 이 선행 규칙 | `lpsocl_box331_amendment_2026_09_01.json` §3 R1, 1저자 승인 09-04 | ✅ 맞다 — s4/600 한 건으로 600 K 를 탈락시킨 우리 독법이 누락 |
| 2 | C3 도구가 세 온도 같은 시드 집합을 요구 | `arrhenius_compat.py` 1판 :211–215 (빈 칸이면 SystemExit) | ✅ 맞다 |
| 3 | 드라이버가 온도별로 다른 RNG seed | `disorder_ensemble_diffusion.py:427` `seed + 1000*ci + int(T)` | ✅ 맞다 — 시드 번호 pairing 근거 없음 |
| 4 | 드라이버가 STO Ea 를 자동 계산·저장·출력 | `:273 arrhenius()` · `:436 print(... Ea=...)` · `ensemble_results.json` | ✅ 맞다 — "Ea 계산 0회" 는 틀린 범위 |
| 5 | §3 이 C2b·C5·C6 누락 · §7 이 HOLD 를 비양립 문구로 고정 | 마감 카드 :94–97 · :133·:138 | ✅ 맞다 |
| 6 | b2o3 골격 MSD 2.8–9.9 Å² 기록 → "b2o3 도 전부 <2" 가정은 기록과 불일치 | `md_run_ledger.json:280` | ✅ 맞다 — b2o3 철회 유지 |

## 1. 항목별 대응

### Q1 — C2·C6 판정 단위
- **수용.** C2 온도 자격은 R1 승계로 명시한다 (개정안 A3): 600 K = s2·s3 자격, s4 의 D 는 어디에도 안 넣는다. 3점이 선다. **s5 도 연장도 없다.**
- 시드 제외 규칙과 통계 절차의 단절(도구가 같은 시드 집합을 요구) → **C3 도구 2판**이 온도별 시드 수 상이(2·3·3)를 받는다. `null` 칸은 제외 목록에 남긴다.
- C6 집계 미정 → **전건**을 제안한다 (A6). 다수결·평균은 소수 시드의 구조 전이를 평균으로 지우는 것 — 회신이 C2 D안에서 거부한 행동과 같다. C2 의 2/3 은 이식하지 않는다.
- D안(평균곡선) 반대 → 수용. 취하지 않는다.

### Q2 — s5 한 번만
- **수용.** A/B/C 어느 것도 하지 않는다. "27→256" 은 독립 정보량이 아니라 열거수라는 정정도 수용 — 도구 2판 docstring 에서 그 문장을 지웠다.
- `--scan` 에 정본 창 (50,100) 이 없다는 지적 → 맞다. `--scan` 은 진단으로만 남기고, 최종 판단은 4창 값·창 수·반올림 전 산포로 한다 (기존 `--mto` 출력이 그것이다).

### Q3 — COM 결과가 α 를 확정하나
- **수용 + 네 문장 철회** (800>1000 β 불가 · S 189 통계 · RMS<결합길이 · COM 잔여=진동). 요청문은 고치지 않고 이 문서에 철회를 적는다.
- framework_static ≠ C6 통과표 → C6 는 `not_assessed` 로 **판정 원장에 등록**했다 (`A-2026-09-11-lpsocl-box331-C6-framework`, β 경보 3칸 보존, binding = diagnostic_unbound — 등록된 claim 이 아직 없다).
- "MSD 하한은 새 판정 규칙" → 수용. 하한을 붙이지 않고, 대신 **원자별 자리 이탈 census** 를 C6 판정 근거로 정의했다 (개정안 §2 — O>2.5 Å / S>3.0 Å 최근접 P 거리 · 자유 음이온·P 변위 >2.0 Å · 10 ps 연속). 문턱은 결합길이·자리 간격에서 왔고 **원자별 자료를 보기 전에** 박았다. 도구 `framework_site_census.py` 는 신설 예정 (사다리 ②: 원자별 골격 census 가 기존 도구에 없다).
- 기록 위치 4곳 → 개정 카드(있음) · 결과 파일(경보 보존, census 결과는 병기 예정) · 판정 원장(있음) · canonical_registry(등록 claim 이 생길 때 참조 — 지금은 값이 없으므로 항목이 없다).
- b2o3 → 같은 census 감사 대상에 넣되 철회는 유지 (골격 MSD 2.8–9.9 Å² 는 census 와 무관하게 이동이다).

### 결함 1 — C2b 미입증
- **수용.** 요청문의 홉 수(15.5–68/이온)는 `hops_per_ion_msd` 상한이었다. 개정안 A5: 측정 = `aimd_jump_stats.py` inter-cage hops / n_Li, ≥3.0 충족 · 상한만 넘으면 **미입증 = HOLD**. 문턱은 그대로(더 엄격해진다). 정의를 커밋한 뒤에 센다.

### 결함 2 — 공유 800 K vs paired seed 혼동
- **수용.** `tools/ionic/arrhenius_compat.py` **2판**: 온도별 자격 시드 평균의 온도 간 독립 재표본(전수 열거, 온도별 nⁿ 의 곱), **800 K 평균 하나를 두 구간에 공유**, ΔEa 직접, 같은 재표본으로 3점 무가중 Ea → C5 폭 · C4 LOO. 대조 = 800 K 를 두 구간에 따로 뽑은 분포 — 공유 쪽 SD 가 커야 정상 ((c1+c2)² > c1²+c2²), 같으면 두 번 뽑은 것. selftest 24/24 (음성: 800 K 이중 뽑기 · 1시드 온도 · 2점 · inconclusive 문구 · 해상도 1 µeV).
- ⛔ 실데이터에는 안 돌렸다 (NO-GO). 순서: 비준 → C2b 계수 → C6 census → 자격표 → C3.

### 결함 3 — HOLD 를 곡률 증거로
- **수용.** 개정안 A2: C3 incompatible 일 때만 "양립하지 않는다"; inconclusive·C2b·C4·C5 HOLD 는 **"양립 여부를 판정하지 못했다"**. A1: §3 에 C2b·C5·C6 명시 + `not_assessed` 표지.

### 결함 4 — "Ea 0회" 범위
- **수용.** A8: "MTO/C3 미계산·미열람" 으로 축소. STO Ea 열람 여부는 1저자·에이전트가 각각 선언한다 (개정안 §6 ③). 에이전트 선언: BL 프롬프트 작성 때 `grep` 은 코드에만 돌렸고 `lps400.log`/`ensemble_results.json` 의 값은 열지 않았다 — 다만 watch 출력에 Ea 줄이 찍혔는지는 확인하지 못했다.
- 그리고 회신의 마지막 문장 — *"C2·C6 와 D_inc 를 이미 본 상태라 결과 독립 사전등록이 아니다"* — 그대로 수용해 개정안을 **post_hoc: true** 로 표시하고 §4 에 항목별 관측 의존을 적었다.

## 2. 산출물 (이 커밋)

- `db/properties/lpsocl_box331_closure_amendment_2026_09_11.json` — proposed · post-hoc · 추가 MD 0
- `db/governance/decisions.json` `D-2026-09-11-lpsocl-box331-closure-amendment` (proposed · retrospective · results_seen)
- `db/governance/assessments.json` `A-2026-09-11-lpsocl-box331-C6-framework` (not_assessed · 경보 보존)
- `tools/ionic/arrhenius_compat.py` 2판 (selftest 24/24) · `convention_check` 0 위반 · `validate_canonical` 그래프 ✅
- 마감 카드 원문 불변 (비준 digest 보존)

## 3. 1저자 결정 4건 (개정안 §6)

1. C6 온도 집계: **전건**(권고) / 다수결 — 이 자료에선 결과가 같다(경보가 확정되면 둘 다 no_value).
2. §2 census 문턱 비준 (결과 보기 전).
3. `lps400.log` / `ensemble_results.json` 의 STO Ea 열람 여부 선언.
4. A3 적용(600 K = s2·s3) 을 R1 승계로 확인.

## 4. 이 문서가 하지 않는 것

- C3·ΔEa 를 계산하지 않았다. MD 를 더 돌리지 않는다. C6 의 물리를 판정하지 않았다 — census 가 한다.
- 회신의 Nosek·Hesterberg 인용은 확인하지 않았다 (논지에 필요 없는 출처라 소환하지 않는다).
