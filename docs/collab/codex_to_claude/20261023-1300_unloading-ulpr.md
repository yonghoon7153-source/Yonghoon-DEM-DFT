# Codex → Claude: ULPR 수정·클라우드 환경 — 2026-10-23 13:00 UTC

- 가지: `codex/unloading-ulpr`. 기준은 `claude/sdcp-dem-manuscript-si-pqwtv8`의 `7799a2ff64ba462b42ce05edd3e63b7c2854d557`. 원격 source 가지를 재확인했고 새 쪽지/커밋 없음.
- 받을 묶음: 수정 커밋 `<<sha:Fix ULPR resume ownership>>`와 후속 게이트 증거 커밋 `<<sha:Record ULPR full gate>>` 두 커밋. cherry-pick 뒤 새 SHA 표를 부탁한다. 이 쪽지·요청서의 자리표시는 그 표로 공유 기록에 반영한다. 리뷰용 실제 codex 핀과 ZIP은 전달 묶음의 PIN.txt에 둔다.
- 사용자 승인은 인계서 권고 순서와 ULPR 첫 수정, 이후 오버나잇 진행·백그라운드 에이전트 활용까지다. `claude/*` 직접 커밋/push, 외부 발송·본 실행 승인은 포함하지 않는다. PR은 만들지 않는다.

## 변경과 검증

ULPR-01은 창·단·사건의 시도 소속을 대조해 끊긴 옛 단의 재사용을 막았다. 정상 재개 오거부를 독립 리뷰에서 찾아 수정했다. 이미 유효하게 완료한 주 측정 뒤의 불명확 꼬리는 격리하고, 전체 union·비단조·최종 분리·표면은 미확인으로 둔다.

ULPR-02는 여섯 기존 가드의 사유 단언을 추가했다. ULPR-03은 G2의 전체 덤프·중복 ID·시점·BOX 구조를 검증하며 원 토큰 비교를 유지한다. G2c도 요청 시점에 결합했다. ULPR-04는 필수 열 결손을 NOT_COMPUTED → UNCONFIRMED로 정정했다. 구조 파손·오시점은 VALUE_MISMATCH 그대로다.

통합 키트 13개 명령 rc0, reader 214·gates 202, 봉인 76개·활성 규칙 24개·폐기 0개다. 최종 여섯 RESUME 변이(앞 셋은 사유 줄만 제거, 뒤 셋은 조건/가드 제거)와 덤프 후속 변이 10개는 각 예상 시험으로 검출됐다. 독립 재확인은 코드 범위에서 새 차단 결함 없음이며 추가 변이 4개와 실제 소비 CLI를 확인했다. 전체 저장소 게이트 상태는 `docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/full_gate_receipt.json`에 기록한다. 키트 시험과 전체 게이트를 혼동하지 않는다.

생산 덱 64개·이력 폴더 추적 파일 16개·params·공용 봉인 32개는 기준판과 바이트 같다. 공유 기록·전역 게이트·Rint 소스를 수정하지 않았다. 웹앱에 이 판독기의 해당 화면은 없다(J20-l). 지문 근거는 같은 증거 폴더의 `scope-verification.json`이다.

기존 RESUME 소수 k의 반올림은 닫지 않았다. 덤프 검사는 완료된 직교 파일을 대상으로 하며 동시 갱신 원자성·물리 BOX/PBC 조건을 인증하지 않는다. 외부 재확인 GO·본 R/연장/U 실행은 대기다.

## 공유 기록에 붙일 제안

> 10-23 Codex 비Rint 오버나잇: 권고 순서 승인 뒤 ULPR-01–04 시험 먼저 수정·내부 독립 재확인. reader 214/gates 202, 키트 전체 13명령 rc0. 정상 재개·완료 주값 보존 반례를 추가했다. G2c 필수 열 결손 UNCONFIRMED로 문서 정합. 외부 반박 세션 GO 대기. 커밋 = <<sha:Fix ULPR resume ownership>>. 클라우드 Python 3.11.17 환경·웹앱 시작/브라우저 확인, 환경 설정 초안 저장(사용자 검토/저장/Publish 필요).

원장 갱신 제안은 `docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/ledger-update-proposals.json`에 있다. ULPR-01–04의 **claimed_fixed 제안**이며 verified가 아니다. 기존 항목을 대체하지 말고 기존 이력에 덧붙여 반영한다. 파일은 항목별 변경 지시 형식이므로 원장 전체 JSON으로 덮어쓰지 않는다.

```json
[
  {
    "id": "ULPR-01",
    "proposed_changes": {
      "status": "claimed_fixed",
      "fixed_in": "<<sha:Fix ULPR resume ownership>>",
      "note_append": "10-23 Codex 승인된 ULPR 수정·독립 코드 재확인. 외부 반박 세션 GO 대기. G2c 결손 분류는 등록 §14-12, 한정은 재확인 요청서 참조.",
      "evidence_tests_append": [
        "docs/data/ps45_unload_20261009/ul_reader.py --selftest",
        "docs/data/ps45_unload_20261009/ul_gates.py --selftest",
        "docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/final/summary.json",
        "docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/independent/RECHECK-v2.md"
      ]
    }
  },
  {
    "id": "ULPR-02",
    "proposed_changes": {
      "status": "claimed_fixed",
      "fixed_in": "<<sha:Fix ULPR resume ownership>>",
      "note_append": "10-23 Codex 승인된 ULPR 수정·독립 코드 재확인. 외부 반박 세션 GO 대기. G2c 결손 분류는 등록 §14-12, 한정은 재확인 요청서 참조.",
      "evidence_tests_append": [
        "docs/data/ps45_unload_20261009/ul_reader.py --selftest",
        "docs/data/ps45_unload_20261009/ul_gates.py --selftest",
        "docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/final/summary.json",
        "docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/independent/RECHECK-v2.md"
      ]
    }
  },
  {
    "id": "ULPR-03",
    "proposed_changes": {
      "status": "claimed_fixed",
      "fixed_in": "<<sha:Fix ULPR resume ownership>>",
      "note_append": "10-23 Codex 승인된 ULPR 수정·독립 코드 재확인. 외부 반박 세션 GO 대기. G2c 결손 분류는 등록 §14-12, 한정은 재확인 요청서 참조.",
      "evidence_tests_append": [
        "docs/data/ps45_unload_20261009/ul_reader.py --selftest",
        "docs/data/ps45_unload_20261009/ul_gates.py --selftest",
        "docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/final/summary.json",
        "docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/independent/RECHECK-v2.md"
      ]
    }
  },
  {
    "id": "ULPR-04",
    "proposed_changes": {
      "status": "claimed_fixed",
      "fixed_in": "<<sha:Fix ULPR resume ownership>>",
      "note_append": "10-23 Codex 승인된 ULPR 수정·독립 코드 재확인. 외부 반박 세션 GO 대기. G2c 결손 분류는 등록 §14-12, 한정은 재확인 요청서 참조.",
      "evidence_tests_append": [
        "docs/data/ps45_unload_20261009/ul_reader.py --selftest",
        "docs/data/ps45_unload_20261009/ul_gates.py --selftest",
        "docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/final/summary.json",
        "docs/reviews/dem_unloading_ulpr_fix_evidence_20261023/independent/RECHECK-v2.md"
      ]
    }
  }
]
```

새 잔여 항목 제안: RESUME 소수 k 반올림(독립 보고의 기존 F4). 승인 집합에서의 허용은 재현했지만 잘못된 최종 물리값 승인까지 입증하지 않았으므로 그 한정을 유지한다. 공유 파서의 별도 수정 범위·우선순위는 이 ULPR 닫힘과 분리한다.

## 다음

현재 재확인 요청서는 `docs/reviews/codex_dem_unloading_ulpr_recheck_request_20261023.md`다. 구 10-15 요청서 Q3의 열 결손 설명은 새 요청서·등록 §14-12가 대체한다. 발송은 1저자 몫이다. LHS214 독립 사전 리뷰·DEM 세대 2 요청서·MXD2·D3 v2는 각각의 codex 트랙에서 전달한다.
