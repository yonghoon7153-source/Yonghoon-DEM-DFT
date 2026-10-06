# PS01-16 수용 범위 정리 — 외부 fail-closed 결과만 수용 · TryParse 내부 분기 UNOBSERVED (2026-10-06 · 사용자 결정 (가))

> 지난 수신 검토 (`BMIN_R2_RETRY3_REVIEW_20261006` §3 PS01-16 · §7) 가 권고한 문서상 범위 정리다. **승인권자 (사용자) 가 2026-10-06 (가) 로 정했다**
> (COMSOL SPEC §61). 새 관측 · probe · 재시험 · 생산 변경은 없다.

## 원안과 실제

| 항목 | 원안 (`LIMITED_VALIDATION_PLAN.json` PS01-16 expected) | 실제 관측 (결과 묶음 `ed0138b9…`) |
|---|---|---|
| 외부 결과 | 정밀도 경계 문자열 → GDecision INCOMPLETE · GFields INVALID / INCONCLUSIVE | **관측됨** — `results/PS_RESULTS.json` 의 PS01-16 행 · `engine_returns/PS51_stdout.txt` 의 그 줄 (정정표 `BMIN_R2_RETRY3_ACCOUNTING_CORRECTION_20261006.json` 의 PS01-16 행이 줄 번호 · sha256 으로 결속) |
| 내부 경로 | "actual path must be confirmed on the target engine" | **관측 안 됨** — TryParse 반환값 · 변환 뒤 decimal · 어느 거부 분기였는지의 기록이 없다 |

## 정리

1. **수용 대상 = 외부 fail-closed 결과.** 정밀도 경계 입력이 들어와도 Windows PowerShell 5.1 의 실제 GDecision · GFields 가 INCOMPLETE · INVALID /
   INCONCLUSIVE 를 낸다는 것 — 이 사례로 확보한 보장은 이것이다.
2. **TryParse 내부 분기 = `UNOBSERVED`.** "반올림됨을 실제 확인" · "TryParse 실패를 실제 확인" 이라고 쓰지 않는다. 코드상 가능한 경로 설명 (`ps_cases.ps1` ·
   추출 `GDecision.ps1.txt`) 은 실행 관측과 분리해 둔다.
3. 원안 문장 "target engine 에서 내부 actual path 확인" 은 **미충족으로 기록**하고, 계획 종결은 위 1 의 범위로 한다.
4. 내부 분기 확인을 필수로 되돌리려면 사전 봉인한 한정 관측 1 건을 별도 승인한다 (77 입력 전체 반복 · 생산 변경 아님). 지금은 하지 않는다.
