# Codex 재검증 2 요청 — LHS 피복률 · LHSC-03 R2 · LHSC-04 R2 수정 (2026-09-30)

> **판정 (09-30 밤) = HOLD · 새 P1 없음 · P2 R3 셋** — `docs/reviews/codex_lhs_coverage_reverify2_verdict_20260930.md` (증거 `codex_lhs_coverage_reverify2_evidence_20260930/` · 우리 트리 재현 전부 일치).  옛 변이 10 종 · 공동 반올림 오탐은 해제 · 남은 것 = LHSC-03 R3 (분율 누락 / None · 빈 개수 원장 · 집계 모순) · LHSC-04 R3a (생산자 부동소수 오차 전역 보증 반례) · R3b (`n_power_1pct` 표지 반례).  이 요청서의 §5 Q2 답 ("고정 여유가 생산자 오차를 덮는다") 은 **철회** — 생산 식은 덧셈형이 아니라 거리 인수 곱 / rsq 형이고 동심 근접에서 초과가 난다.

> 대상 판정: `docs/reviews/codex_lhs_coverage_reverify_verdict_20260930.md` (HOLD · P1 두 건 닫힘 · 새 P1 없음 · 잔여 P2 둘).
> 1저자 비준 09-30 낮 (*"비준이야 ㅇㅇ"*) → 반례를 셀프테스트로 먼저 옮겨 옛 코드에서 실패를 확인한 뒤 고쳤다.  발송 = 1저자.
> 묶음 = `docs/reviews/codex_lhs_coverage_reverify2_request_20260930/` (패치 2 · manifest · 재현 JSON · 셀프테스트 로그 · SHA256SUMS).

## 0. 적용 기준 · 핀 (SELF-67 교훈 — 적은 해시는 전부 실제로 계산했다)

- **패치 적용 기준 = 앞 재검증의 후보 트리** (2e57dff90 + 패치 0001–0011 = 검토 브랜치 `002cc2881`; Codex 후보 9 파일과 CRLF 제외 동일 — 앞 판정문 §5).
- 새 패치 **둘만** 보낸다: `0012` (LHSC-04 R2 · 검토 브랜치 `f2c15ceac`) → `0013` (LHSC-03 R2 · `ca0471d19`).  순서대로 `git am` (또는 `git apply`).
- 파일 sha256 · `diff --git` 이후 본문 sha256 = `source_manifest.json` (계산값).  0001–0011 은 **다시 보내지 않는다** — 바뀐 것이 없다는 말도 하지 않는다 (필요하면 앞 묶음의 파일을 쓴다).
- 정정 (앞 요청서): *"구간 상한 자체가 서지 않는다"* 는 틀렸다 — 0 ≤ A ≤ π·min(r1, r2)² 가 늘 선다 (Codex §2).  앞 요청서 §0 에 정정 줄을 달았다.

## 1. LHSC-04 R2 — 반올림 상자 포괄 구간 (패치 0012 · `scripts/lhs_descriptor_harvest.py` · `scripts/lens_geometry.py`)

- **계약**: 행마다 덤프 토큰 구간 `[A_dump ± h(A)]` 이 반올림 상자 `{r1 ± h(r1)} × {r2 ± h(r2)} × {δ ± h(δ)}` 위 교차 원판 A 의 **포괄 구간** `[lo, hi]` 와 만나지 않을 때만 초과 (셈만 · 거부 없음 · 피복률 값 불변).
- **계산** (`_area_enclosure`): 같은 식의 인수형 `a² = δ(2r1−δ)(2r2−δ)(2r1+2r2−δ)/(4d²)` (d = r1 + r2 − δ · 덧셈형과 대수적으로 같고 상쇄가 없다) 의 인수마다 선형 구간 (끝점 + 부동소수 바깥 여유) →
  ① 상자 전체가 δ ≤ 0 · d ≤ 0 · 포함 (2r_i − δ ≤ 0) 이면 A ≡ 0 ·
  ② 네 인수가 상자 전체에서 양수이고 ln A 의 편도함수 세 구간 (인수 역수의 합) 이 0 을 포함하지 않으면 두 꼭짓점 값이 **정확한** 최소 · 최대 (각 인수 형성 오차만큼 상대 여유) ·
  ③ 아니면 인수 구간의 곱 ∩ 덧셈형 항별 구간 `π/4·[2(r1²+r2²) − d² − (r1²−r2²)²/d²]` ∩ 기하 상한 `π·min(r1, r2)²` ·
  ④ 인수가 상자 안에서 부호를 바꾸면 (포함 경계 · d = 0 · δ = 0 이 상자 안) 하한 0 · 상한 = 덧셈형 항별 상한 ∩ 기하 상한.
  마지막에 생산자 (LIGGGHTS 덧셈형) 부동소수 바닥 `32·eps·π·max(r)²` 를 바깥으로.
  ⚠ 1저자 비준안의 표현은 "세 항 각각의 구간" 이었다 — 덧셈형 세 항만 쓰면 얕은 접촉에서 항끼리 상쇄되어 구간이 넓어지므로 인수형을 주 경로로 쓰고 덧셈형 항별 구간은 ③ ④ 의 교집합으로 쓴다 (1저자에게 보고함).
- **범위 분류는 없앴다**: `_in_domain_rows` · `n_boundary_excluded` · `AREA_CHECK_MARGIN` 삭제 — 모든 비교 행을 시험한다.  보고 = `n_tested` · `n_beyond_tol` · `n_lower_bound_zero` (하한 0 = 너무 작은 면적은 못 잡는다) · `n_wide_enclosure` ((hi − lo) > 1 %·A_dump = 1 % 치환을 못 잡는다) · `n_power_1pct` (둘 다 아닌 행).
- **서술 정정** (`lens_geometry` 독스트링 · 규칙 문자열 · 시험 이름): δ 에 **단조 아님** — d² = |r1² − r2²| 에서 극대 π·min(r)² · 포함 경계 d = |r1 − r2| 에서 **연속** (a² → 0) · 어긋나는 곳은 동일 반경 d → 0 퇴화 (식 극한 π r² ↔ 코드 d ≤ 0 → 0) 뿐 · 유한 상한 늘 있음.
  옛 시험 ④ "δ 에 단조 증가" 는 "동일 반경에서" 로 좁혔고 ⑥ (Codex 비단조 반례) · ⑦ (연속 · 퇴화) 을 더했다.
- **시험** (셀프테스트 ㉑ ㉑′ ㉑″ · 옛 코드 3 실패 → 149 줄 통과): Codex 반례 초과 0 · 포괄성 = 여섯 영역 (보통 · 깊은 겹침 · 포함 경계 근처 · 거의 같은 반경 d → 0 · 극값 근처 · δ ≈ 0) 600 상자 × 32 점 (꼭짓점 8 + 내부 24) 벗어남 0 ·
  반올림만 3000 행 초과 0 · 실효 상대 반폭 (포괄 반폭 + h(A)) 중앙 5.43e-6 · 최대 1.16e-5 · 3e-5 · Hertz 치환 3000/3000 검출 · 합성 3000 행은 전부 ② (꼭짓점) 방법.
  리포 밖 스트레스 (scratch): 12,000 상자 × 64 점 벗어남 0 (① 3217 · ② 5783 · ③ 1152 · ④ 1848).

## 2. LHSC-03 R2 — 엄격 검증기 (패치 0013 · `webapp/app.py` · `webapp/test_pipeline_provenance.py`)

- `_v2_ok_record` (status 'ok'): n_am = 명시적 비음수 정수 (bool · 실수 · NaN · 누락 거부 — 누락을 0 으로 채우지 않는다) · 무효 분모 둘 = 0 · 클립 수 ≤ n_am · 면적 셋 유한 ≥ 0 · 개수 정수 (cap 충돌 ≤ cap 가지 ≤ 접촉) · **접촉 실패 = 0** · 개수 dict 값 정수 · 분율 [0, 1] · 규약 문자열 · 막 두께 > 0 · `coverage_*_physics_v2` 전부 유한 [0, 100] · n_am > 0 이면 전체 피복률 필수 · n_am = 0 이면 피복률 키 없음.
- `_v2_blank_record` (status 'blank: 사유'): 사유 · 진단 키 넷 + 개수는 None 또는 정수 ≥ 0 · 분모 진단은 None (생산자 내부 오류 경로) 또는 정수 ≤ n_am · 규약 문자열은 None 허용 (진단 일부 None 이라는 기존 의도 보존) · 그 밖의 `*_physics_v2` 는 전부 None (물리 값 잔재 금지).
- 옛 시험 픽스처 `_healthy_cov_v2` 가 개수를 1.0 (실수) · 접촉 실패 1 로 적어 생산자 스키마와 달랐다 → 정수 · 실패 0 · 막 두께로 정정 (엄격해진 검증기가 옛 레코드를 거부했다).
- **시험** (T11k · T11l · T11m · 옛 코드 T11l · T11m 실패 → 209/209): 실제 생산자 (`compute_case`) 출력 8 종 전부 받음 · Codex 변이 10 종 전부 거부 · 필수 단계 재현 (실제 `_coverage_stage` · `summarize` · 계산만 대역) n_am 누락 · 면적 NaN = failed.

## 3. Codex 반례를 새 트리에서 (`_reproduction_r2_wtcov_ca0471d19.json` · 입력은 `audit_delta.py` 그대로)

| 항목 | 재검증 판정 (002cc2881) | 새 트리 (ca0471d19) |
|---|---|---|
| 실제 생산자 양성 대조 8 | 8 받음 | **8 받음** |
| 스키마 변이 10 | 10 받음 | **0 받음** |
| 필수 단계 (n_am 누락 · 면적 NaN) | ok · done | **failed · failed** |
| 범위 안 반올림 반례 | 초과 1 (diff/B 1.332) | **초과 0** · 포괄 [2.6601e-6, 4.7883e-6] (방법 ③) |
| 옛 예 rounding · hertz_deep · 3e-5_deep | 경계 제외 (시험 안 함) | 초과 0 · 0 · **1** — 셋 다 하한 0 행.  3e-5_deep 은 덤프가 기하 상한 π·(r+h)² 를 넘어 잡힌다 · Hertz 값은 그 상한 안이라 못 잡는다 (폭 넓은 행으로 적힌다) |
| 비접촉 대조 (δ 0 · A 0 / δ < 0 · A 0 / δ 0 · A 1e-6) | 0 · 0 · 1 | 0 · 0 · 1 |
| 비단조 (r1 .002 · r2 .001 · δ .00160 → .00161) | 감소 | 감소 (함수 그대로 · 서술만 정정) |
| 수확기 단독 import 에 plastic_coverage | 없음 | 없음 |

셀프테스트 여섯 (`selftests_ca0471d19.log`): 수확기 · lens_geometry · plastic_coverage · coverage_physics_vs_hertzian · lhs_webapp_batch · test_pipeline_provenance 전부 rc 0 · 실패 줄 0.

## 4. 재현 명령

```bash
# 앞 재검증 후보 트리 (002cc2881 상당) 에서
git am 0012-LHS-item-2-Codex-LHSC-04-R2-P2.patch 0013-run_pipeline-coverage-v2-Codex-LHSC-03-R2-P2.patch
python3 scripts/lhs_descriptor_harvest.py --selftest     # ㉑ ㉑′ ㉑″
python3 scripts/lens_geometry.py --selftest               # ④ ⑥ ⑦
python3 webapp/test_pipeline_provenance.py                # T11i–T11m
# Codex audit_delta.py 의 LHSC-03 · 04 절은 옛 API (_in_domain_rows · (ac, diff, bnd)) 를 부르므로 새 트리에서는 그 줄에서 멈춘다 —
# 같은 입력을 새 API 로 돌린 판 = 우리 scratch 스크립트 (결과 JSON 이 묶음에 있다 · 필요하면 스크립트 본문을 보낸다)
```

## 5. 질문

- **Q1 (LHSC-04)**: ① – ④ 의 포괄 구간이 반올림 상자의 **모든 점**을 담는다는 주장에 반례가 있는가 — 특히 ② 의 "편도함수 세 구간이 0 을 포함하지 않으면 두 꼭짓점이 정확한 최소 · 최대" 와 ④ 의 전환 조건.
- **Q2 (LHSC-04)**: 생산자 부동소수 바닥 `32·eps·π·max(r)²` + 인수 형성 오차 여유가 LIGGGHTS 쪽 계산 오차를 덮는가 (덤프 면적은 LIGGGHTS 가 덧셈형으로 계산한 값의 6 유효숫자).
- **Q3 (LHSC-04)**: 범위 분류를 없애고 하한 0 · 폭 넓은 행을 **시험하되 따로 세는** 계약 (검출력 부족을 수로 적는다) 이 앞 판정의 "범위 안의 상한 보증과 밖의 미판정 표지를 분리" 요구를 채우는가.
- **Q4 (LHSC-03)**: 생산자 양성 대조 8 · 변이 10 밖에서 받아들여지는 불완전 레코드가 있는가 — blank 에서 규약 문자열 None 허용이 구멍인가.
- **Q5 (병합)**: GO 면 의존 순서대로 한 항목씩 병합 (0001 … 0013) → 게이트 → 원장 LHSC-01 · 02 · 05 · 06 · 03 · 04 claimed_fixed → 5 번 (재수확 · coverage 배치) 은 최종 트리 해시를 고정한 뒤.  이 순서에 이의가 있는가.

## 6. 묶음 파일 (sha256 = `SHA256SUMS`)

`0012-…LHSC-04-R2….patch` · `0013-…LHSC-03-R2….patch` · `source_manifest.json` · `_reproduction_r2_wtcov_ca0471d19.json` · `selftests_ca0471d19.log` · `README.md` · 이 요청서.
