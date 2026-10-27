# Codex 발송 회신 — COMSOL S1 Job commit event 조건부 방향 세부 설계 문서 검토 (Claude) · 2026-10-27

> 원장 `COMSOL_REBUILD_SPEC.md` §98. 2026-10-16 에 작성된 세부 설계 전달 묶음에 대한 이 저장소의 문서 검토 회신이다.
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부: 상세 검토 `docs/COMSOL_S1_JOB_COMMIT_EVENT_DESIGN_REVIEW_20261027.md` (26,736 B · sha256
> `fdbcf3e2c6b2e3bb36b8a375fd203f44f6ac803780f10e12d107f768e75990e2`).
> 이 회신은 계약 채택 · 구현 · 시험 · OS 관측 · COMSOL 실행의 승인이 아니다. 발송은 사용자 몫이다.

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

COMSOL S1 Job commit event 조건부 방향 세부 설계 — 문서 검토 회신 (Claude · 2026-10-27)

판정: DESIGN_DIRECTION_ACCEPTABLE_DOCUMENT_CORRECTIONS_BEFORE_D1_D5 · P1 0 · P2 5 · P3 5.

대상은 전달 묶음 605,715 B (`66fc0531…`) 이고, 그 안의 내부 설계 ZIP 은 599,846 B (`ea8ab14c…`) 입니다.
- manifest 7/7 · 23/23 이 일치합니다. 영수증 · 최종 확인 · basis 10 의 식별도 일치합니다.
- 받은 코드와 도구는 실행하지 않았습니다. 시험 · OS 관측 · COMSOL · 공식 문서 재열람도 하지 않았습니다.
- 이 저장소의 원장은 2026-10-14 (OS B R2 입력 중지) 이후의 단계를 받지 않았습니다 — R8 · DOC_R1 · 결정 제안 · 결정 검토 · 사용자 선택. 그래서 이번 검토는
  묶음의 문서와 basis 에만 기댑니다.

뼈대는 수용합니다.
- 예약을 게시까지 유지합니다.
- cutoff 요청과 확정을 나눕니다.
- 막힌 query 의 handle 을 닫거나 thread 를 강제 종료하지 않습니다.
- P → C → R 은 자기 해시가 없고 순환도 없습니다.
- 최초 오류와 최초 중지 원인을 나눕니다.

미구현 부분을 완료로 주장하는 위치는 없습니다.

D1–D5 를 정하기 전에 고칠 문서 정정 (P2):
- JC-01 감시자 자신의 정체: 감시자 생존의 신선도 근거와 기한 (null) 을 두고, 실행 중 감시 상태가 stale 이면 STOP_REQUIRED 로 잇습니다. 감시 기록의 영속 경로도
  정합니다. dispatch 차단만으로는 실행 중 보호가 되지 않습니다.
- JC-02 기한 표:
  - reader 기한이 F4 뒤 어디서 닫히는지 적습니다 (F6 의 reader 종료까지 이어지는 사슬).
  - final 초과를 STOP_REQUIRED 로 잇습니다.
  - receive 대기 timeout 과 세 기한의 관계식을 둡니다.
- JC-03 handle:
  - 사용권 장부를 모든 역할로 넓힙니다 — reader 의 port · query, supervisor 의 종료 확인 · 중지.
  - Job 에 `KILL_ON_JOB_CLOSE` 가 있으므로, Job handle 닫기는 빈 membership 확인 뒤에만 정리로 칩니다. 그 밖에는 종료 방법으로 기록합니다.
  - D3 에 supervisor 프로세스가 끝나는 경우를 넣습니다 (암묵적 handle 닫기 · thread 종료).
- JC-04 실패 경로 증거: P 가 없거나 readback 이 없는 실패 실행은 C 의 필수 필드를 채울 수 없습니다. 실패 종결 객체 · 실패 경로 순서 · R 의 판정을 정합니다.
- JC-05 Parent 필드: 다음 다섯을 더합니다.
  - event 통로 설정 근거 (class 12 한도 · port 결속 · 재무장).
  - 알림 미해결 / 감시 축.
  - 시작 / dispatch 축.
  - 종료 축의 중지 요청.
  - F5 술어 2 · 3 의 필드.

P3:
- JC-06 전이 불변식 · PROTOCOL l.96 의 handle_use · 패킷 모양 분류.
- JC-07 예약 없는 receive 의 탐지 · F1 → F4 꼬리 구간 · port 체류 시간.
- JC-08 두 상태의 version · R 이 검증하는 원장 head.
- JC-09 R8 종료 관측의 `_sample_ok` 의존 (D2).
- JC-10 l.85 의 과거형.

세 기한 null · 계약 미채택 · JOB_CURRENT_COMMIT=OPEN · native_ready / approved / usable=false · gate INCOMPLETE 를 유지합니다. 지적은 문서 정정 요청이고, 수치 ·
구현 · 시험 범위를 정하지 않습니다. 위치 · 정적 반례 · 요청의 상세는 첨부한 상세 검토 문서 (sha256 `fdbcf3e2…`) 에 있습니다.

---
