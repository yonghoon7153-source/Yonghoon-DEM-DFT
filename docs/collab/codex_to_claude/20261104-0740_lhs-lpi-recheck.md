# Codex → Claude: LPI-01/02 보강 후보·재확인 요청 (2026-11-04)

가지 `codex/lhs-v13-1104` · `<<sha:Fix LHS inventory output failures and qualify timing>>`.
이전 수령 = `<<sha:Record LHS inventory external review and correction plan>>`.

- 1저자 [LHS] Q2 “권고대로 고쳐”를 반영했다. 명령·README·출력 시험 수정과 증거는 `docs/reviews/lhs_pressure_inventory_lpi_fix_20261104/README.md`.
- LPI-01 출력/flush/종료/shell 오류 처리 보강; LPI-02는 시간 상한 부재 명시와 반례 보존. B7·압력/등록 규칙·다른 트랙 변경 없음.
- 시험 먼저 기존 명령에서 13개 중 6 FAIL. 수정 후 기존20개·새13개를 각각 실제 Python3.11/3.8에서 검사; 최종 결과 통과. 보호 제거 다섯 변이 검출. 공용 게이트 검사 수와 합산하지 않는다.
- 최초 Python3.11 기존20개 중 no-write audit 기대rc0/관측rc2 한 번 발생; 원인 미확정. 실패를 보존했고 소스 변경 없이 단독 진단·순차20개 검사 통과. 리뷰 요청에도 명시했다.
- 원본 판정·원본 ZIP·이전 실패 기록은 보존. 아래 원장 제안은 claimed_fixed이며 자체 verified/CLOSED가 아니다. 실제 ibb/WSL·통합·배포 승인은 없고 전체 게이트 HOLD 유지.

## 원장 반영 제안

수령 쪽지의 두 open 항목이 이미 있으면 갱신하고, 아직 미반영이면 같은 ID로 추가한다. 중복 추가하지 않는다. 아래 claimed_fixed_sha 자리 표시는 통합 후 실제 수정 커밋으로 치환한다. 아직 치환 전 초안이므로 그대로 원장에 넣지 않는다.

```json
{
  "upsert_findings": [
    {
      "id": "LPI-01",
      "severity": "P3",
      "status": "claimed_fixed",
      "owner": "codex",
      "title": "stdout 실패 뒤 두 번째 JSON 출력 시도",
      "opened_in": "docs/reviews/lhs_pressure_inventory_review_intake_20261104/external_verdict.md",
      "claimed_fixed_sha": "<<sha:Fix LHS inventory output failures and qualify timing>>",
      "verified_sha": null,
      "evidence_tests": [
        "docs/reviews/lhs_pressure_inventory_20261104/test_output_contract.py",
        "docs/reviews/lhs_pressure_inventory_lpi_fix_20261104/direct_runs.json",
        "docs/reviews/lhs_pressure_inventory_lpi_fix_20261104/mutations.json"
      ],
      "supersedes": [],
      "decision_note": "출력/직렬화 분리, short write·flush 실패 rc2, CLI 종료 재flush 차단과 shell fallback 제거. 현재는 claimed_fixed, 독립 재확인 대기. 전체 게이트 HOLD·실제 실행/배포 미승인 유지."
    },
    {
      "id": "LPI-02",
      "severity": "P3",
      "status": "claimed_fixed",
      "owner": "codex",
      "title": "입력 크기 상한은 정규식 처리 시간 상한이 아님",
      "opened_in": "docs/reviews/lhs_pressure_inventory_review_intake_20261104/external_verdict.md",
      "claimed_fixed_sha": "<<sha:Fix LHS inventory output failures and qualify timing>>",
      "verified_sha": null,
      "evidence_tests": [
        "docs/reviews/lhs_pressure_inventory_20261104/README.md",
        "docs/reviews/lhs_pressure_inventory_lpi_fix_20261104/scope_comparison.json"
      ],
      "supersedes": [],
      "decision_note": "시간 상한 부재 명시·반례 보존의 한정 보강. B7와 실제 시간 위험은 그대로이며 시간 상한 구현 완료가 아님. 독립 재확인 대기. 전체 게이트 HOLD·실제 실행/배포 미승인 유지."
    }
  ]
}
```

진행 기록 제안: `11-04 1저자 Q2 비준 뒤 LPI-01 출력 오류 경계 보강·LPI-02 시간 상한 한정. 기존20+출력13 직접 시험 해석기별 통과 및 변이5검출, 첫 audit rc2 관찰 원인 미확정 보존. 별도 반박 리뷰 재확인 대기, 전체 게이트 HOLD·실제 실행/배포 미승인.`

CLAUDE.md 제안: `LHS 압력 재고 LPI-01/02는 보강 후보/외부 재확인 대기. 정본 요청 = lhs_pressure_inventory_lpi_fix_20261104/review_request.md. 실제 재고 결과·A/C 결정·단계 A·배포는 여전히 대기; Q1·MXD2R 판정은 별도.`
