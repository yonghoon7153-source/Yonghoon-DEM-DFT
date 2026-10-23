# [LHS214] 독립 사전 검토 전달 — 2026-10-23 12:54 UTC

## 가지·커밋 범위

- 인계 가지: `codex/lhs214-relaunch` (이 쪽지는 반입 준비 단계에 작성).
- 검토 소스: `7799a2ff64ba462b42ce05edd3e63b7c2854d557`의 LHS214 관련 파일.
- 예정 커밋 제목: `Review LHS214 relaunch preflight and pin syntax`.
- 받아 갈 커밋 범위·끝 SHA 자리: `<<sha:Review LHS214 relaunch>>` 한 커밋. 실제 생성·push 전 준비 기록이며 완료를 주장하지 않는다.
- 공유 원장·CLAUDE·진행 기록·봉인 32·생산 소스를 직접 고치지 않았다. 이 트랙의 변경은 새 검토문·증거·이 쪽지다.

## 한 일과 남은 일

[독립 사전 검토문](../../reviews/codex_review_lhs214_preflight_20261023.md)과 [증거·재생 명령](../../reviews/lhs214_preflight_review_evidence_20261023/README.md)을 준비했다.

- S0b: 현재 123/123, 수정 전 도구 + 현재 비준 문서는 121/122·S0b 실패. 독립 진리표 512가지 불일치 0. 네 가드 제거는 각 122/123·S11g 하나로 실패.
- 봉인 32, 인계 2 + 빌더·실행기·스모크가 대조 핀과 같고, 두 등록 비준 diff·활성 지문·194/20 입력 지문 재계산이 일치했다.
- 새 P3 제안: 사전 점검 JSON의 `git.sha = 정상 40자리 + LF`가 P7·P10을 통과. 주 작업자가 별도 출력 폴더에서 같은 결과를 재현했다. 다른 승인 커밋 우회가 아니며 실제 발사 manifest F7·G7은 같은 반례 대상이 아니다.
- 수정 제안은 원문 SHA의 전체 문자열 검사와 여섯 경계 시험이다. 생산 코드를 고치지 않았다. `_HEX40` 공용 변경이면 모든 사용처 회귀를 먼저 범위에 넣는다.
- **전체 `scripts/check_all.sh`는 작성 시점에 메인 작업에서 대기 중이다. 이 쪽지는 전체 게이트 통과 기록이 아니다.** 커밋·인계 전에 정해진 전체 게이트가 필요하다.
- `SUPR-03`의 상태는 `claimed_fixed` 그대로다. 이 사전 검토를 외부 반박 세션의 verified로 바꾸지 않는다. `L214R-S03`·`L214R-S05`, S3, v1.3 한정도 그대로다.
- 실제 WSL의 B7 핀·깨끗한 트리·보통/격리 의존성·fast16/real4 및 도구 시험·새 ROOT 두 영수증·194 전체 값 손 대조·묶음 SHA가 아직 필요하다. 그 뒤 외부 반박 판정과 1저자 발사 승인도 별개다.

## 공유 기록에 넣을 문안 제안

> 10-23 Codex LHS214 독립 사전 검토 (`<<sha:Review LHS214 relaunch>>`): S0b 현재 123/123, 수정 전 121/122·S0b; 독립 512조합 불일치 0, 네 가드 변이는 S11g로 모두 검출. 봉인·등록·입력 재결합 일치. 사전 점검 git.sha 끝 LF 형식 결함 P3 제안(다른 승인 핀 우회 아님), root 별도 재현 동일. 실제 WSL 증거·B7 핀 선택·외부 반박·발사 승인 미완료. SUPR-03 및 기존 open 상태 변경 없음. 전체 게이트 결과는 메인 작업자가 별도 기록.

## 원장 추가 JSON 제안 — 직접 적용하지 않음

ID `LHS214-PRE-01`은 이번 보고서의 임시 ID다. 기존 원장 ID와의 충돌·담당을 Claude가 확인한 뒤 반영한다. `SUPR-03` 상태 변경 JSON은 제안하지 않는다.

```json
{
  "id": "LHS214-PRE-01",
  "severity": "P3",
  "status": "open",
  "owner": "claude",
  "found_by": "Codex 작업 세션 독립 사전 검토 2026-10-23; 주 작업자 별도 재현 동일",
  "opened_in": "docs/reviews/codex_review_lhs214_preflight_20261023.md",
  "title": "사전 점검 영수증 git.sha의 정상 40자리 뒤 LF를 _HEX40.match가 허용하여 P7·P10 통과 — 정확히 40 hex라는 형식 보장 누락",
  "note": "검토문 §3. run_network_194_parallel.py:792,2049,2082. 정상 JSON의 git.sha만 40자리+LF로 바꾸고 approved_sha에는 원래 40자리 전체를 주면 P0–P10 통과. CRLF·space·NUL은 P7/P10 실패, 마지막 hex 변경은 P10 실패. 다른 승인 커밋 우회가 아니고 수치·봉인 변경 증거도 아님. 실제 발사 manifest F7/G7은 fullmatch이므로 같은 허점으로 일반화하지 않음. 권고는 검사 전 정규화 없이 원문 전체 문자열 검사와 여섯 경계 시험; 공용 상수 변경이면 모든 사용처 회귀 확인. 코드 수정·발사 GO·원장 종결 없음.",
  "evidence_tests": [
    "docs/reviews/lhs214_preflight_review_evidence_20261023/tools/pin_probe.py",
    "docs/reviews/lhs214_preflight_review_evidence_20261023/reviewer/pin-probe.json",
    "docs/reviews/lhs214_preflight_review_evidence_20261023/root_reproduction/pin-probe.json"
  ]
}
```

## 다음 연결

이 P3의 처리 범위를 정한 뒤 시험 먼저 수정·독립 재검토한다. 실제 발사 환경의 사전 점검·외부 반박·발사 승인을 줄이지 않는다. 요청서의 WSL·B7 빈칸은 실자료를 받을 때만 채운다. 이 쪽지는 발송·기계 실행 승인 요청을 대신하지 않는다.
