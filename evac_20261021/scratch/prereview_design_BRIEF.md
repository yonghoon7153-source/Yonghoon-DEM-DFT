# 사전 리뷰 — 설계 · 등록 쪽 (이름 `design`)

먼저 `prereview_common.md` (같은 폴더) 를 읽는다.

## 볼 것 (문서 — 그리고 문서가 가리키는 코드 · 숫자)
- 설계 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` · 등록 R 초안 `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` · kgy 명령 `docs/reviews/rint2_kgy_commands_20261020.md` · 수정 계획 `docs/reviews/rint2_design_fix_plan_20261021.md` · Codex 요청서 `docs/reviews/codex_rint_carbon_additive_design_request_20261020.md` (지난 회차) · 판정문 `docs/reviews/codex_review_rint2_carbon_additive_design_20261021.md`.

## 꼭 볼 보장 · 주장 (최소 — 더 찾으면 더)
1. RCA-01 — 보정 폭: SBE 1.63 한 점 보정이 R_j,0 를 얼마나 좁히나 — ±2 % 양끝을 **실제 응답**으로 잡는 절차인가 (선형 보간 · 기울기 가정 없이) · 판정문의 31,622.7766 / 100,000 Ω 꼴 (마지막 이웃) 이 개정 절차에서 어떻게 처리되나.  작은 해석 응답 곡선 (단조 · 평탄 · 꺾임) 세 개로 절차가 맞는 답 / 거부를 내는지 손으로.
2. RCA-02 — origin 양끝: 네 모서리 × {lo · 0 · hi} × arm 1 · 2 가 판정 함수에 어떻게 들어가나 · W 0.293 → 0.836 꼴 (판정문) 이 개정판에서 등급을 어떻게 바꾸나.
3. RCA-08 · 09 · 10 · 12 · 13 — P 간극 envelope · 감도 = 주 판정과 같은 추정량 · DIA 표지 · 유한 Rc 1차 해석 한정 · τ_mono 단위 · 영값 상태.  판정표의 모든 칸 (상태 × 조건) 이 빠짐 · 겹침 없이 닫혀 있나 (표를 직접 열거해 빈 칸 · 두 번 걸리는 칸 찾기).
4. RCA-11 · Q8 — s_min = SBE 개발 단계에서 고르고 DBE 열람 전에 봉인 · 표본화 절차가 결과 전 등록인가 (결과를 보고 고를 수 있는 자유도가 남았나 — 하나씩 열거).
5. 다음 세대 규칙 — 두 침대 VGCF E 100 GPa 재압밀 · VGCF σ 하나 (직경 보존 7854 S/cm · Endo 2001 1 × 10⁴ · vox 0.15) · 보정 = R_j,0 하나 (SBE 1.63) · DBE 4.68 = 예측 (독립 holdout 아님 — 현 세대 보정에 쓰인 값) — 문서 어디에도 "독립 검증" · "holdout 적중" 식 문장이 없나 (§5-3 금지 문장 · 헤드라인 문안과 대조).
6. Q13 — 새 킷 payload 줄에서 `--joule-heat` · `--save-step4-grid` 를 빼는 명령이 kgy 문서에 정확히 있나 (sed 꼴 · 옛 킷 무변경 · 뺀 뒤 payload 줄 전체를 보이는 확인 명령) · 재압밀 명령 (VGCF E 만 · 이름 "E + dt + 재하율 세대 전환") 이 등록과 같은가.
7. 런 수 · 시간 상한 — 등록 §10 의 런 목록을 직접 세어 (사다리 · 양끝 · DBE 네 모서리 · origin · 감도) 수와 GPU 시간 어림 (현 세대 8 팔 실측 ≈ 50 분/팔 · LEAN=4) 이 10-31 안에 드는지 · 멈춤 규칙 (시간 넘으면 무엇을 버리나) 이 결과 전 등록인가.
8. 문서 ↔ 코드 이름 — 문서에 쓴 노브 · 필드 · 상태 · 멈춤 코드 이름이 통합 코드 (`<HEAD>`) 에 실제로 있는가 (grep 으로 하나씩 · 없는 것 목록).
9. 숫자 · 전칭 — 문서의 숫자 (1.63 · 4.68 · 0.347 · 2.618 · 7854 · 1.629 · 1.888 · 4.729 · rtol 1e-12 · ε_I 1e-4 …) · "N/N" · "비트 같음" · "닫힘" 을 리포 원자료 · 판정문 · 시험 출력과 한 줄씩 대조.

## 산출
`prereview_common.md` 의 형식대로 `<SCRATCH>/prereview_design/REVIEW.md`.
