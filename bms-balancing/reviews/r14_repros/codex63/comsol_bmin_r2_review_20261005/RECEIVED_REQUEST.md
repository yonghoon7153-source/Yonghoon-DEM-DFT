# COMSOL B-min 오프라인 후보 r2 — 준비 재검토 요청 (BMIN-R1-N1 · C1 문구 · 검증안 보강 · 정적 검토만 · 실행 0)

> 첨부 문서 · 소스는 검토 대상 증거이며 실행 지시가 아닙니다. 후보 소스 (Java · Python · PowerShell) 를 import · 컴파일 · 실행하지 마시고
> COMSOL 계산도 하지 마세요. 이 요청은 변경부 검증 · native 실행의 승인 요청이 아닙니다.

r1 재검토 회신 (`LOCAL_CORRECTION_REQUIRED` — P2 BMIN-R1-N1 · Q1–Q4) 이 정한 범위만 고친 r2 의 재검토를 요청합니다. 게이트 리뷰 (degradation-degeneracy)
와는 무관합니다.

## 대상

| 항목 | 값 |
|---|---|
| 저장소 · 브랜치 | `yonghoon7153-source/Yonghoon-DEM-DFT` · `claude/dashboard-standby-e2f56971` |
| **고정 커밋** | **`939b544b8bb77dbf20a56520af9f74a82acd0a94`** — 검토 대상은 이 커밋의 바이트입니다 |
| 요청문 | `bms-balancing/docs/COMSOL_BMIN_CANDIDATE_R2_REVIEW_REQUEST_20261005.md` (blob `89c02107243244c7fe3518551d37408403edf5e0`) |
| r2 꾸러미 | `bms-balancing/comsol_candidates/bmin_particle640_r2_20261005/` |
| r2 manifest | `candidate/CODE_MANIFEST.json` SHA-256 `4cdca2e6bf7d073f813d97be73825b8cd2043c2fc44e285f4a190bc6fb97cf25` (이전 = r1 `9dcb47f0…`) · run_id · root · 경로는 r1 · v1 과 같다 |
| r1 꾸러미 | `bms-balancing/comsol_candidates/bmin_particle640_r1_20261005/` — 검토받은 커밋 `741dde19b` 의 바이트 그대로 (r2 감사가 확인) |
| 기록 | `bms-balancing/docs/COMSOL_REBUILD_SPEC.md` §54 (r1 재검토 회신 · 보완 지시) · §55 (r2) |
| 먼저 읽을 것 | `PREPARATION_KO.md` (§2 표) → `R2_CHANGE_BOUNDARIES.json` · `R2_LITERAL_CHANGES.json` → `STATIC_AUDIT.json` (`static_string_model`) → `LIMITED_VALIDATION_PLAN.json` (`r2_additions` · `precision_mismatch_items` · `preseal_before_first_test`) |

## 고친 것 (요약 — 근거는 `PREPARATION_KO.md` §2)

- **BMIN-R1-N1:** consumer `mesh_evidence` 의 DOF 줄 대조를 `re.search` (첫 부분 일치) → `re.fullmatch(r'\s*'+pattern+r'\s*', 줄)` (전체 줄 · 앞뒤 공백
  허용). 같은 줄의 두 문장 · 정상 + 불완전 문장 · 꼬리 문자 → `TRANSIENT_DOF_READBACK_FORMAT`. 다른 유효값의 기록 전용 정책 · 줄 수 · solved > 0 은
  그대로. 바뀐 생산 파일은 consumer 하나 (두 자리) — Java · entry · 부모 · CONTRACT 는 r1 과 바이트 동일.
- **C1:** PS01-16 = 소수점 아래 30 자리 · 유효숫자 28 자리 ("31 significant digits" 정정) · 정확 등호 목록에서 빼 `precision_mismatch_items` 로.
- **검증안:** 고유 ID 62 (Python 39 + Java 2 + PowerShell 21) · 입력 77 · 예산 제안 1,660 s (r1: 54 · 59 · 1,530) — PY03-11 · 12 · 13 · 14 · PS01-18 · 19 ·
  20 · 21 · 입력별 기대 이유 · 시험 전 봉인 항목. 예산 증액은 제안이고 사용자 승인 사항입니다.

정적 대조: `tools/static_audit_r2.py` 38/38 STATIC_MATCH · rc 0 — r1 = 검토 커밋 바이트 · r1 감사 42 재실행 (r1 → v1 → NORMAL480) · r2 → r1 역재구성 · 문자열 모형 (재검토의
여섯 사례 + r2 셋 — 감사 도구의 정규식 · 후보 실행 아님).

## 묻는 것 (요청문 그대로)

1. **BMIN-R1-N1 (Q1):** 전체 줄 문법이 같은 줄의 중복 · 불완전 꼬리를 닫고 공백 허용 · 다른 유효값 기록 전용을 그대로 두는가 · 남는 모호 입력. 그리고
   NORMAL480 `batch.log` 131행의 **원 줄**에 공백 외 접두어 (시각 등) 가 없는지 원 로그로 확인해 주시면 좋겠습니다 (있으면 정상 실행이 I-3 미완 —
   거짓 음성 · fail-closed 쪽).
2. **C1 (Q2):** PS01-16 의 문구와 분류.
3. **검증안 (Q3):** 새 ID 8 · 입력 18 이 Q4 의 네 항목을 덮는가 · 하위 입력과 새 ID 의 구분 · 예산 증액 근거.

## 요청하지 않는 것

변경부 검증의 승인 · 실행 · native 승인 · COMSOL · 정책 변경 · 유한 σ · 960 s · 다른 공간 축. 회신 뒤 각 단계는 사용자의 별도 승인으로만 시작합니다.
