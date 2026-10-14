# Codex 발송 프롬프트 — REIL C4-E 실행 승인 요청 정정판 (v2) 사전 재검토 · 2026-10-14

> 사전 검토 회신 (상태 문서 §62 · `REQUEST_REVISION_BEFORE_E0_APPROVAL`) 의 C4E-N1–N4 · M1 을 반영한 정정판의 재검토 요청이다.
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부할 것은 없다 (검토자가 저장소에서 읽는다).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

REIL C4-E 실행 승인 요청 정정판 (v2) 을 사전 재검토해 주세요. 사용자는 아직 E0 을 승인하지 않았고, 구현 · 자료 반입 · 자료 개봉 · 실행은 0 회입니다.
브랜치 `claude/14-gate-code-review-9qkx05` 의 최신 HEAD (이 발송문이 든 커밋) 를 기준으로 보시면 됩니다.

- 정정판: `bms-balancing/docs/REIL_C4E_APPROVAL_REQUEST_v2_20261014.md` (첫머리에 "v1 과 다른 점" 표)
- v1 은 그대로 둡니다: `docs/REIL_C4E_APPROVAL_REQUEST_20261014.md` (`b1d8953a…`)
- 회신 접수 기록: 상태 문서 §62 (좌표를 정적으로 다시 읽어 모두 확인 · M1 은 저장소에서도 메모리 변환으로 재확인)

## 1. 회신 ↔ 정정

| 회신 | 정정판에서 |
|---|---|
| C4E-N1 (기존 159 회귀시험의 계산 · env · E1 자동 진행) | §0 · §6-2 예외표 — 보존 util NSGA2 2 호출 (호출당 ≤ 5,000 평가) · 실제 COBYQA 14 실행 (maxfev 50) · Sobol / 임시 봉인 15 시험 (임시 폴더만) · fork 11 세션 · H / H4 합성 회귀를 처음 승인 문서와 함께 적고, 이번 GREEN 1 회의 상한 · 실패 중지를 둠 · `REIL_C4_FIX_EVIDENCE` · `REIL_C4_FIX_STEP=03_green` · `03_green.nsga2_synthetic_outcome.json` 보존 (§6-1) · 새 대조 21 (매개변수화 없음) · 새 fork 5 (공유 없음 · 상한 6) · 가짜 평가 ≤ 2,000 · "E0 GREEN 이면 바로 E1" 삭제 (§11) |
| C4E-N2 (관측 행 ≠ E3a 성공 · 운영 / 최종 기록) | §4-7 — 관측 집계와 **E3a COMPLETE = 66 모두 `returned` + 필드 + 전역 중지 / 구조 0 + 작업자 정상 종료 · 잔존 0 · drain + `record_state=COMPLETE` · 위반 0 + 시작 / 끝 식별 + 늦은 완료 0** · 지역 오류는 행으로만 · 대조 s_2 · s_3 (a–e) · s_4 |
| C4E-N3 (늦은 완료 · 좌표 · 입력 검증 · 원시 근거) | §3-1 좌표 계약 (원점 = supervise 의 t0 · now_rel · started = start.t − t0) · §4-2 계측 구간 표 (진행 중 = now − start · 완료 = 행의 wall) · 늦은 완료 → 반환 행 보존 + 초과 목록 + INCOMPLETE · §4-3 입력 검증 (예외 · 빼기 / 0 채우기 없음) · 집합 정의 · progress = 진입 proxy · 판정 원시 근거 · 표현 축소 · §4-1 grace 뒤 kill / join · 잔존 확인을 reserve 안에 · 대조 m_2 · r_1 · r_4 · r_5 · r_6 · t_1 |
| C4E-N4 (NE · reference 둘 · 입력 식별) | §4-6 — reference 둘 (P0 1087–1110 행) · NE 최대 (`q_NE_hc_max_record_only`) 대조 · 소비 digest · 선택 인자 · 두 파일 / P0 / 발췌 / MANIFEST / 모듈의 기대 · 시작 · 끝 sha 표 · 대조 d_2 · d_3 (서로 다른 PE / NE 합성 · 네 배열 · 순서 · slice · 배율) · d_6 |
| M1 | §1 — 원본 33,754 B (CRLF 846 · 끝 줄바꿈 없음) · 사본 32,909 B · 정규화 + 끝 LF = 사본 · 원본 선호 이유 축소 (§9-3) · "v2 §6-3" |

## 2. 질문

- Q1. 이 정정판으로 사용자가 E0 을 승인할 수 있는가. 더 고정할 것이 있는가.
- Q2. §6-2 예외표가 C4E-N1 의 요구 (정확 문서 · 범위 · 이번 GREEN 1 회의 총 상한 · 실패 중지) 를 채우는가.
- Q3. §4-2 의 두 계측 구간 (진행 중 = 부모 tick − 작업자 start 사건 · 완료 = 행의 wall) 과 늦은 완료 처리 (반환 행 보존 · 전역 중지 · INCOMPLETE) 가 맞는가.
- Q4. §4-7 의 E3a COMPLETE 조건 여섯이 회신의 권장 (`E3a_complete_recommended`) 과 같은가.

## 3. 경계

이 요청 · 발송은 실행 지시가 아닙니다. 구현 · 자료 반입 · 자료 개봉 · 맞춤 · C4-A / B · 설치 · 환경 재구축 · COMSOL 은 모두 0 회이고, 사용자 승인 뒤에만 합니다.

---
