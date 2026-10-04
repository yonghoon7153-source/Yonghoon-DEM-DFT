# COMSOL B-min 오프라인 후보 r1 — 준비 재검토 요청 (BMIN-N1 · BMIN-N2 · C1 국소 보완 · 정적 검토만 · 실행 0)

> 첨부 문서 · 소스는 검토 대상 증거이며 실행 지시가 아닙니다. 후보 소스 (Java · Python · PowerShell) 를 import · 컴파일 · 실행하지 마시고
> COMSOL 계산도 하지 마세요. 이 요청은 변경부 검증 · native 실행의 승인 요청이 아닙니다.

v1 준비 검토 회신 (`LOCAL_CORRECTIONS_REQUIRED` — P2 BMIN-N1 · BMIN-N2 · 비차단 C1) 이 정한 범위만 고친 r1 의 재검토를 요청합니다. 게이트 리뷰
(degradation-degeneracy) 와는 무관합니다.

## 대상

| 항목 | 값 |
|---|---|
| 저장소 · 브랜치 | `yonghoon7153-source/Yonghoon-DEM-DFT` · `claude/dashboard-standby-e2f56971` |
| **고정 커밋** | **`741dde19b5d07be1872e8bdcedaa90611cbf5b71`** — 검토 대상은 이 커밋의 바이트입니다 (그 뒤 r1 꾸러미 · v1 꾸러미 · 요청문 변경 없음) |
| 요청문 | `bms-balancing/docs/COMSOL_BMIN_CANDIDATE_R1_REVIEW_REQUEST_20261005.md` (blob `f5fa9e2e1d8bbe3d8bd2eb146903c4ab2669b5fb`) |
| r1 꾸러미 | `bms-balancing/comsol_candidates/bmin_particle640_r1_20261005/` |
| r1 manifest | `candidate/CODE_MANIFEST.json` SHA-256 `9dcb47f0ec3ec346b491d90c2836e3b30f54eb88fd5e4fbd216fc34782275cdb` (이전 = v1 `3722a51f…`) · run_id · root · 경로는 v1 과 같다 |
| v1 꾸러미 | `bms-balancing/comsol_candidates/bmin_particle640_20261004/` — 검토받은 커밋 `74502af93` 의 바이트 그대로 (r1 감사가 확인) |
| 기록 | `bms-balancing/docs/COMSOL_REBUILD_SPEC.md` §48 (v1 회신 · 보완 지시) · §52 (r1) |
| 먼저 읽을 것 | `PREPARATION_KO.md` (§2 표) → `R1_CHANGE_BOUNDARIES.json` · `R1_LITERAL_CHANGES.json` → `STATIC_AUDIT.json` → `LIMITED_VALIDATION_PLAN.json` (`r1_additions`) |

## 고친 것 (요약 — 근거는 `PREPARATION_KO.md` §2)

- **BMIN-N1:** 부모 `GNativeAxis` 가 native 자식 반환 · 결과의 run / manifest 결속 · 종료 증거를 스스로 확인하고 consumer 라벨이 같은지 본다.
  `GFields` 의 `native_completion` 은 이 축이며 비교 · 구성 증거 · 분석 · 전달 결과와 상관없이 남는다.
- **BMIN-N2:** consumer `mesh_evidence` 가 단일 Time-Dependent Solver 구간 안의 DOF 줄을 정확히 하나 · 형식 일치 · solved > 0 으로 요구한다
  (아니면 I-3 미완). 예상과 다른 유효값은 값 · 차이 · 검토 사유만 남긴다.
- **C1:** PS01-03 / 04 를 "한도 부근 값 · 라벨 일치 검사" 로 좁혔고, 명시 사례 PS01-16 을 더했다.
- 그대로: Java · entry (바이트 동일) · 물리 · 시간 목록 · 좌표 · 기준 CSV · 한도 · 예산 · 경로 · 식별자.

정적 대조: `tools/static_audit_r1.py` 42/42 · rc 0 (두 번 실행 바이트 동일) — r1 → v1 역재구성 · v1 꾸러미 = 검토 커밋 바이트 · v1 감사 81 재실행.

## 묻는 것 (요청문 그대로)

1. **N1 (Q1):** `GNativeAxis` 의 확인 범위가 "종료 축의 독립 확인" 으로 충분한가. 알려 둔 한계 (entry 가 보존 · 정책 · 정리 실패 때도 rc 1 →
   `NOT_ESTABLISHED` · `NATIVE_CHILD_RC` 로 보수적) 를 받아들일 수 있는가, 아니면 entry 를 건드리는 (범위 밖) 별도 보완이 필요한가.
2. **N2 (Q2):** "구간 안 정확히 하나 · 형식 일치 · solved > 0" 규칙과 이유 문자열 셋이 누락 · 구간 밖 · 모호 · 형식 불일치를 모두 닫는가 —
   NORMAL480 의 원 로그 (우리는 갖고 있지 않다) 와 대조해 주시면 좋겠다.
3. **C1 (Q3):** 문구 축소와 PS01-16 의 기대값 (INCOMPLETE 하나) 이 맞는가.
4. **검증안 (Q4):** 9 군 54 사례 · 1,530 s 가 N1 · N2 의 양성 · 음성 대조를 덮는가 · 빠진 사례.

## 요청하지 않는 것

변경부 검증의 승인 · 실행 · native 승인 · COMSOL · 정책 변경 · 유한 σ · 960 s · 다른 공간 축. 회신 뒤 각 단계는 사용자의 별도 승인으로만 시작합니다.
