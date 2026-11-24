# Codex 반박 리뷰 요청 — 믹서 문제 · 공백 · 새로움 v1 (2026-11-24)

> 1저자 11-24 *"한다음에 codex 반박 받아도 되고"* · *"다 권고대로"* (Q5 = 따로 있는 Codex 반박 리뷰 창) · 문서 검토만 · **새 계산 · 시뮬레이션 0 건**.
> 리뷰 핀 = 이 요청서를 담은 stoic 커밋 (`claude/stoic-knuth-NObVQ` · 핀 sha 는 1저자가 보내는 글에 적는다) · litdb 정본 = `origin/claude/friendly-meitner-lldvar` @ `c32e89830`.

## 0. 이번에 닫는 것 / 닫지 않는 것

| 닫는 것 (판정 요청) | 닫지 않는 것 |
|---|---|
| v1 의 새로움 문장 (§1-3) 이 이 서랍 근거로 서는가 · 더 좁힐 곳 | 믹서 계산 결과의 타당성 (B1 · B2 판독 = Codex 실무 몫 · 개발 자료) |
| 공백 넷 판정 (§2) 의 빠진 반례 · 한정 | 사다리 등록 자체 (초안 = 실무 창 · 1저자 GO 전) |
| 예측 P-0 · P-a · P-b · P-c (§4) 가 반증 가능한가 | 원고 문장 (원고 흐름 = 1저자) |
| §5 금지 문장 · §6 위험 의 빠진 것 | 서랍 밖 문헌의 판정 (검색 낱말만 요청) |

## 1. 읽을 것

- 대상: `docs/reviews/mixer_problem_gap_novelty_20261124.md` (v1)
- v0 내부 반박 리뷰 (Codex 아님 · P1 4 · P2 16 · P3 12): `docs/reviews/mixer_problem_gap_novelty_review1_20261124.md` — v1 이 다 반영했는지도 봐 주세요.
- 근거: `docs/data/mixer_lit_matrix_20261123/` (gap_check.md · matrix.json · gap_summary.json · README.md) · `docs/hetero_thesis.md` §2 · `docs/reviews/mixer_direction_feedback_20261123.md` · `docs/reviews/mixer_b1_pair_return_20261122/README.md` · `docs/reviews/mixer_b2_flow_20261124/` (README · mixer_next_design.md · b1_b2_u_contacts.json) · `docs/reviews/mixer_d3_se_flowability_anchor_design_20261015.md` · 정본 카드 (위 핀)

## 2. 질문

| ID | 질문 |
|---|---|
| MGN-Q1 | §1-3 네 고리 문장이 이 서랍 근거로 방어되는가 — 깨지는 고리 · 고칠 문장 |
| MGN-Q2 | §2 공백 넷 — 서랍 안에서 빠진 가장 강한 반례 · 한정 / 서랍 밖에서 맞설 주제의 검색 낱말 (인용 아님) |
| MGN-Q3 | §4 P-0 (B2-C 판독 전 등록 · 기하평균 쌍별 Bo 위계로 C − U 방향) 의 논리 · 반증 조건이 충분한가 · P-a · P-b (대립 H-b1 · H-b2) · P-c 가 결과 전에 판정 가능한 꼴인가 |
| MGN-Q4 | 고리 ① 주 축 = 같은 SE 탐침 떼는 힘 비 (절대 세기 · 흐름 세기 고정 조건) 가 맞는가 · 거친 입자 (CGF 151.4) 점착 규칙 후보와 그것을 결과 전에 고르는 법 |
| MGN-Q5 | 고리 ② AFM 계획의 실행 가능성 — 거친 기판에서 R\* 약분 가정 · 탐침 지름 ↔ 덱 SE 환산 · SE–벽 재질 쌍 |
| MGN-Q6 | 고리 ④ (parcel 혼합 → 실크기 압밀 넘김) 가 규칙으로 가능한가 · 아니면 주장에서 빼야 하나 |
| MGN-Q7 | §5 · §6 에 빠진 것 · 1저자 결정 Q1–Q5 (11-24 권고대로) 가 근거와 맞는가 |

## 3. 답 꼴

- 판정문 한 파일 · 지적 ID = `MGN-NN` · 등급 P1 (문장 · 판정이 틀림) · P2 (오해 · 빠진 한정) · P3 (표기) · 고칠 문장 제안 · 근거 줄.
- 새 계산 · 시뮬레이션 없음 · 숫자는 카드 · 리포 줄로만 · 카드에 없는 서지는 채우지 않음 (`[미확인]`).
