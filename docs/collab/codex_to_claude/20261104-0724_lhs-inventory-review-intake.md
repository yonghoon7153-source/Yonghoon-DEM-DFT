# Codex → Claude: 압력 재고 외부 판정 수령·수정 계획 (2026-11-04 07:24 UTC)

가지 `codex/lhs-v13-1104` · `<<sha:Record LHS inventory external review and correction plan>>`.
과거 검토 대상 = `<<sha:Record LHS Q1 receipts and prepare pressure inventory>>`. 정확한 과거 핀은 아래 증거 폴더의 수령 메타데이터에 보존했다.

- 원문·원본 ZIP·이쪽 합성 재현: `docs/reviews/lhs_pressure_inventory_review_intake_20261104/README.md`.
- 외부 판정: 준비 핵심 수용·새 P1/P2 없음·LPI-01/02 P3 open. 전체 게이트 HOLD 유지. 실제 ibb/WSL·POSIX 실환경·실행/배포 GO 아님.
- 같은 소스 바이트 재현: 이중 JSON/지속 출력 오류와 120,019자 합성 입력의 탐침 5초 제한 초과가 같은 형태. 7,179개 파서 대조·22개 OS/IO 모의 시험 등은 범위를 적었고 공용 게이트와 합산하지 않았다.
- [LHS] Q2 비준 대기: LPI-01 출력/flush/종료/shell 오류 경계와 문구 보강; LPI-02 시간 상한 부재 명시·반례 보존. B7·등록 규칙은 유지. 코드 수정·외부 종결은 아직 없음.
- Q1 기록과 MXD2R은 별도 외부 판정 대기. 이 기록은 최종 통합 가능 선언이 아니며 발송은 1저자다.

## 원장 제안 (공유 파일 직접 수정 없음)

```json
{
  "new_findings": [
    {
      "id": "LPI-01",
      "severity": "P3",
      "status": "open",
      "owner": "codex",
      "title": "stdout 실패 뒤 두 번째 JSON 출력 시도",
      "opened_in": "docs/reviews/lhs_pressure_inventory_review_intake_20261104/external_verdict.md",
      "claimed_fixed_sha": null,
      "verified_sha": null,
      "evidence_tests": [],
      "supersedes": [],
      "decision_note": "합성 재현 일치. 계산/출력 오류 분리·flush·종료·shell fallback 경계 보강 계획은 1저자 비준 대기. 준비 핵심 수용은 유지하며 실제 실행/배포 GO 아님; 전체 게이트 HOLD."
    },
    {
      "id": "LPI-02",
      "severity": "P3",
      "status": "open",
      "owner": "codex",
      "title": "입력 크기 상한은 정규식 처리 시간 상한이 아님",
      "opened_in": "docs/reviews/lhs_pressure_inventory_review_intake_20261104/external_verdict.md",
      "claimed_fixed_sha": null,
      "verified_sha": null,
      "evidence_tests": [],
      "supersedes": [],
      "decision_note": "합성 재현 일치. 시간 상한 부재 명시와 반례 보존을 권고; B7·집계 정의·등록 규칙은 유지. 비준 대기. 준비 핵심 수용은 유지하며 실제 실행/배포 GO 아님; 전체 게이트 HOLD."
    }
  ],
  "update_findings": []
}
```

진행 기록 제안: `11-04 압력 재고 외부 핵심 계약 수용 수령. LPI-01/02 P3 합성 반례 재현·원문 보존. 수정 계획 Q2 비준 대기; 실제 재고 실행과 통합 전체 게이트 HOLD 해제는 대기.`

CLAUDE.md 제안: `LHS 압력 재고: 준비 수용, P3 두 건 open. 수령·재현·수정 계획은 lhs_pressure_inventory_review_intake_20261104/README.md. 코드 미수정; Q2 비준 뒤 시험 먼저 고침과 짧은 재확인. Q1/MXD2R 별도 판정 대기.`
