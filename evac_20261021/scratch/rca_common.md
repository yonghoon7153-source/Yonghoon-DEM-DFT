## 공통 (세 에이전트 A · B · C)
- 1저자 10-21: 수정 계획 `docs/reviews/rint2_design_fix_plan_20261021.md` Q1–Q12 **전부 권고대로** + Q13 (가) (생산 킷 payload 줄의 `--joule-heat` · `--save-step4-grid` = 새 킷 만들 때 뺀다) · *"최대한 기한 맞추고 타이트하게"* — 일요일 10-25 안에 Codex 재검토를 받고 런까지 가는 것이 목표.
- ★ **1저자 10-21 (뒤) — 기한 = 이번 달 말 (10-31) 로 늘어남 · *"더 꼼꼼하게 보자"*** ⇒ 빠르기보다 꼼꼼함이 먼저.  생략하던 무거운 시험도 돌린다 (`nice -n 19` · 하나씩) · 보장마다 손으로 풀리는 작은 해석 반례 + 변이 시험 (구현을 일부러 틀리게 하면 그 시험이 실패하는가) · 지금까지 줄이거나 건너뛴 것은 보고에 적는다.  범위 · 금지 규칙은 그대로.
- 정본 = Codex 판정문 `docs/reviews/codex_review_rint2_carbon_additive_design_20261021.md` (RCA-01–13 · RINT2-B-01 · §3 · §4-1 · §5) · 증거 `docs/reviews/codex_rint2_carbon_design_review_evidence_20261021/` (반례 코드 geometry/*.py · registration/*.py · 우리 Linux 재현 = RCA-07 주 반례는 우리 환경에서 B 실패 (경계 사례) · 연결 보조 사례 −0.904 % · 23 반복 사례 +5.56e-4 는 A/B/C 통과).
- 기반: 너의 작업 트리에서 `git reset --hard 47d23baba` (Z3 까지 합친 메인 · 게이트 중 · 같은 저장소라 객체 있음) · `git fetch` 안 함 · push 안 함 · `scripts/check_all.sh` 안 돌림 · 봉인 32 파일 (`scripts/run_network_194_parallel.py` CODE_FILES) 금지 · 원장 `findings.json` · CLAUDE.md · 진행 기록은 메인 몫.
- 시험 먼저: Codex 반례를 우리 시험으로 먼저 옮겨 고치기 전 코드에서 실패 확인 → 구현 → 커밋 메시지 "pre-fix N/M (fails = K checks from J counterexamples)" · 끈 경로 (새 동작이 켜지지 않으면) = 기반과 비트 같음.
- 무거운 시험은 하나씩 `nice -n 19` · 다른 둘이 같이 돈다 · 디스크 적게.
- 커밋 메시지 영어 · 모델 이름 없음 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 보고 = 한국어 · 표 · 짧게: 커밋 SHA · 고치기 전 → 뒤 · Codex 반례 재현 값 → 고친 뒤 값 · 끈 경로 · 실행 시간 · 설계와 다르게 한 곳 · 남은 것 · 다른 에이전트와 맞출 이름.
