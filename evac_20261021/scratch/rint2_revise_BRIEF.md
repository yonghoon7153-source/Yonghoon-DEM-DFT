# Rint ② 설계 문서 셋 고치기 — 사전 리뷰 두 결과 반영 (문서만 · 10-20)

## 기반
- 너의 작업 트리에서 `git reset --hard worktree-agent-afe00cbd76c918fb8` (= `b694369b5` · 부모 `f507bdc74` = 원격) → `git log -3 --oneline` 확인.  `git fetch` 하지 않는다.
- 고칠 문서 셋: `docs/reviews/rint_carbon_additive_design_v1_20261020.md` (D) · `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` (R) · `docs/reviews/codex_rint_carbon_additive_design_request_20261020.md` (Q).
- 사전 리뷰 결과 (전부 읽는다):
  - 문장 · 숫자 · 출처 대조 41 건: `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prerev_rint2_findings_claims.md`
  - 공격 (Codex 대역) 21 건 + 수렴 탐침 표 + 새 결정 6: `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prerev_rint2_findings_attack.md`
  - 조인 수정 (Part B) 사전 리뷰 요지는 아래 "Part B" 절.

## 할 일 (커밋 하나 · 문서만)
1. 두 결과의 **모든 항목**을 반영한다 — "보내기 전 반드시 고칠 것" 은 설계 · 등록 · 요청서 본문을 실제로 고치고, "한정으로 적을 것" 은 해당 자리에 한정어를 넣는다.  고치지 않기로 한 항목이 있으면 이유를 요청서 끝 "사전 리뷰 반영표" 에 적는다 (항목 번호 ↔ 처리 ↔ 자리).
2. **수렴 (공격 #1)**: 다음 세대 판정 해의 수렴 인증을 다시 설계한다 — 정지 규칙 (rtol ≤ 1e-12 쪽 또는 판 전류 불균형 기준 정지) · 판 전류 불균형 문턱 ⓑ 는 합성 직접해 대조로 **결과 전에 봉인** (숫자는 B1 숫자 탐침에서 정하는 절차로 · 탐침 표는 근거로 인용 — "합성 격자 · 실침대 아님" 표지) · ⓒ 재풀이 대조는 판정에 쓰는 해 전부 (사다리 점 + DBE 네 모서리) · 시간 비용 (1e-8 → 1e-12 반복 ≈ 1.7–2 배 · 탐침 어림) 보고 · 현 세대 꼴은 같은 탐침에서 σ 오차 ≤ 5.5e-5 (현 세대 수치 무영향 — 합성 탐침 한정) 를 적는다.
3. **결정 자리**: D 의 1저자 질문 절을 하나로 정리한다 — 기존 N1–N10 + 새 것 (대조 #4 = Q9 '융합' 을 '근접 접합 축약 끝' 으로 · #5 = 원고 펠릿 9:1 의 지위 (법칙 고정 → 사전 점검) · #6 = Q6 "부피 보존 길이" 의 뜻 · 공격의 새 결정 1–6).  겹치는 것은 합친다 (예: 공격 1 = 대조 #4 · 공격 4 와 N6).  질문마다 권고 한 줄 · 본문은 **권고안으로 쓰되** 그 자리에 `⬜ 1저자 (권고)` 표지를 단다 (1저자가 정하면 메인이 ✅ 로 바꾼다).  N10 의 긴 접촉 부분은 J8 과 충돌하므로 공격 2 로 대체 ("주 fused" 철회).
4. **Part B (조인 수정 재확인)**: 아래 요지로 채운다 — 리뷰 핀 · 같은 부류 보강 커밋 자리는 `⬜ (메인이 채운다)` 로 남긴다.
5. 요청서 맨 위 "이번에 닫는 것 / 닫지 않는 것" 을 고친 내용에 맞춘다 · 숫자 ↔ 출처 표 (대조 #10 · #11) 를 실제로 쓴 숫자만으로 다시 만든다.
6. `python3 scripts/check_doc_refs.py` (`✓ 깨진 참조 없음`) → 커밋 하나 (영어 메시지 · 모델 이름 없음 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`).

## Part B 요지 (조인 수정 · 사전 리뷰 결과)
- 대상 커밋 (원격에 있음): `12d894c09` (시험 먼저 · 고치기 전 152/206 · 실패 54 = J12 26 · J13 6 · J14 22 (전각 · 아라비아-인도)) · `a2cfd0365` (수정 · JOIN_VERSION v4) · `654385e4c` (기록).  옛 138 판을 고친 모듈에 = 138/138.
- 사전 리뷰 결과: 숫자 전부 재현 · 새 P1/P2 없음 · Codex 탐침 넷 재실행 = 기대대로 (구조 144 건: 헤더 10 → 거부 · 나머지 134 같음 / 최소 반례 둘 거부 / 수치 113 건: 바뀐 7 = 전각 정수 + 1e160 계열 6 · 나머지 106 같음 / 넘침 3 건: 1e160 거부 · 1e150 대조 · 정상 그대로).
- 같은 부류 보강 (⬜ 1저자 Q1 — 권고 = 지금 고침 · 커밋 자리 `⬜`): ① 머리 줄 표지 경계를 공백 · 탭 · 줄 끝만 (지금 `isspace()` 라 NBSP · U+3000 등도 받음) ② 덤프 글자 어휘 관문 (TAB · LF · CR · 0x20–0x7E 밖 = `frame_layout`) ③ scaffold 실수 열 ASCII 고정소수 문법 (주석 줄 제외) ④ `_STEP_RE` ASCII ⑤ J13 에 f6 `wd` 만 넘치는 꼴 (변이 시험 틈).
- 한정 (RIMPR-04 open 에 남음 · 고치지 않음): 아주 작은 `sim_to_um` 언더플로 (반지름 · 면적 0 이 통과) · 반지름 ≈ 1e97 sim 이상에서 면적 도우미 OverflowError (`lens_geometry.py:34`) · f5 비교 자체의 inf/NaN · 계획이 조인 판 (v3 / v4) 을 확인하지 않음 (조인은 같은 프로세스에서 다시 계산 · 저장 기록을 되읽는 길 없음 — grep) · 절 순서 · 비-AM 중복 · 자기 접촉 · id 0/음수 미검사 · `ITEM: UNITS` · `ITEM: TIME` 지원 밖 거부 · 접촉 id ≥ 10⁶ (`%g` 손실) 거부 · 694 행 RuntimeWarning.
- 우리 기록 정정 (다음 커밋에서): 원장 SELF-124 note 의 범위 없는 "NUMERIC_MODULES 6 무변경" 등 11 곳.  **판정문 정정 알림**: Codex 판정문 (`docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md`) 의 "여섯 개는 두 핀 사이 모두 동일" 은 대조 핀 `dcb97f1ed` → 리뷰 핀 `2b9efa253` 구간에서는 맞지 않는다 — `scripts/network_conductivity.py` (NUMERIC_MODULES 6 중 하나 · 봉인 32 중 다른 트랙 변경 네 파일 중 하나) 가 L214R 트랙에서 바뀌었다 (두 Rint 커밋 ∩ 봉인 = 0 은 참).  확인: `git diff --stat dcb97f1ed 2b9efa253 -- scripts/network_conductivity.py`.

## 규칙
- **코드는 고치지 않는다** · push · `scripts/check_all.sh` · `git fetch` 안 함 · 무거운 계산 안 함 (작은 탐침은 스크래치 · 몇 초 · 끝나면 지움 — 디스크 여유가 작다).
- 값 · 서지는 litdb 정본 카드에서만 (`git show origin/claude/friendly-meitner-lldvar:litdb/papers/<card>.md`) · 없으면 `[미확인]`.
- 원격에 없는 커밋 번호를 쓰지 않는다 (`SELF-116`) — 네 커밋 번호는 쓰지 않는다.
- 끝나면 옛 초안 작업 트리를 지운다: `git -C /home/user/Yonghoon-DEM-DFT worktree remove /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe00cbd76c918fb8` (가지는 남는다 · 실패하면 그대로 두고 보고).
- 보고 (한국어 · 짧게 · 표): 커밋 SHA · 반영표 요약 (반영 / 한정 / 안 함 수) · 정리된 1저자 질문 표 (번호 · 질문 · 권고) · 남은 `[미확인]`.
