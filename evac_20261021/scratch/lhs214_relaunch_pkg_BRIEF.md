# LHS214 다시 발사 — 다섯 단계 묶음 (문서 · 계산 대조만 · 10-20 밤)

## 왜
Codex 10-20 재확인 (`docs/reviews/codex_review_lhs214cx_fix_recheck_20261020.md` §5) = 수정은 닫혔고, 새 214 발사는 다섯 단계 전 HOLD:
① 194 · 보충 20 정책 개정 + 활성 §3 지문 1저자 비준 (대기 선언을 승인 지문으로 자동 취급하지 않음 · 결과 열람 뒤 변경 이력 보존) ② 발사 핀의 봉인 32 · 기대 세대 · 입력 ID / 원 dump hash / 코호트 표 · 인계 도구 · 배포 빌더 지문 재결합 ③ B7 승인 핀 = 사전 점검 · 두 manifest 와 일치 (실제 승인 SHA · 두 manifest 끼리 같다는 것만으로 부족) ④ 새 ROOT 둘에서 같은 승인 핀 · 지문 · 실제 fast16 + real4 · 관측된 의존성 · 전체 사전 점검 로그 + 완료 영수증 ⑤ 1저자 별도 발사 승인 (구 ROOT · 실패 기록을 사후 성공으로 덮지 않음).
1저자가 Q 에 답하기 전에 **비준할 문안과 그 뒤 명령을 한 문서에** 준비한다.  (1저자 결정 대기: 등록 비준 · σ₀ 1.5 상수를 이번 재봉인에 넣을지 — 권고 = 넣지 않음 · 다섯 단계 묶음을 Codex 에 한 번 보일지 — 권고 = 예.  ⇒ 문서는 **권고안 기준**으로 쓰고 각 자리에 `⬜ 1저자` 표지.)

## 기반
- 너의 작업 트리 HEAD (= 본 가지 `952ad1a25` 계열).  `git fetch` 하지 않는다.  push · `scripts/check_all.sh` 안 돌림 (본 트리 게이트가 돈다).
- 정본 (전부 읽는다): 194 등록 `docs/reviews/lhs_network_batch_registration_20261007_g2.md` (§2 · §3 · §4 · §9-7 · §9-8 — 개정 초안 · 대기 지문 `code_fp_pending 2149f873…`) · 보충 20 등록 `docs/reviews/lhs_network_batch_registration_20261012_supp20.md` (§2 · §3 · §4 · §9-1 · §9-3) · Codex 판정문 `docs/reviews/codex_review_lhs214cx_fix_recheck_20261020.md` (§2 핀 · §5) · 그 앞 판정문 `docs/reviews/codex_review_lhs214rr_fix_recheck_20261019.md` · `docs/reviews/codex_review_lhs214s_fix_recheck_20261019.md` (다섯 단계 원문) · 10-14 사전 점검 = 194 §9-7 · 보충 §9-1 · `docs/reviews/codex_review_supr_fix_reverify_20261014.md` (영수증 · `preflight-verify` · `--approved-sha` · 한정 = TSV 끝 개행 반례) · 실행기 `scripts/run_network_194_parallel.py` · 영수증 도구 `scripts/supp20_input_receipt.py` · 다시 읽기 `scripts/g2_network_reread.py` · 배포 `scripts/lhs_release_build.py`.
- ⛔ 봉인 32 파일 (실행기 `CODE_FILES`) 은 한 글자도 바꾸지 않는다 — 봉인 32 = 리뷰 핀 `34713ac96` → 지금 HEAD 사이 변화 0 (메인 확인).

## 할 일 (커밋 하나 · 문서만)
새 문서 `docs/reviews/lhs214_relaunch_package_20261020.md`:
0. 맨 위 **"이번에 닫는 것 / 닫지 않는 것"** (닫는 것 = 다섯 단계 준비 문안 · 지문 대조 · 명령 / 닫지 않는 것 = 비준 · 실제 발사 · S3 (별도 HOLD — 봉인 수치 모듈 둘이 바뀜 → S3 재봉인 의무) · v1.3 주 학습 인계 (H0 model_limit HOLD) · L214R-S03 · S05 (open · 한정 유지)).
1. **① 비준할 문안** — 194 §9-8 · 보충 §9-3 개정 초안을 "비준되면 바뀌는 줄" 표로 (자리 · 지금 원문 · 비준판 · 이력 표지 = *"결과 열람 뒤 정책 개정 (10-14 실행 결과를 본 뒤)"* 보존).  §3 활성 지문 = `2149f873…` 로 바뀌고 대기 선언은 지운다 (§9-8 문구 그대로).  ⚠ **지금 HEAD 에서 봉인 32 지문을 저장소 자신의 함수로 다시 계산**해 `2149f873…` 와 같은지 확인 (실행기 · 영수증 도구가 code_fp 를 계산하는 함수를 찾아 그대로 부른다 — 새 식을 짜지 않는다) · 다르면 멈추고 보고.  비준 커밋에 들어갈 문안 (194 · 보충 등록 §3 · §9-8 · §9-3 바뀌는 줄) 은 **이 문서 안에 diff 꼴로만** 적고 등록 문서 자체는 고치지 않는다 (비준 뒤 메인이 넣는다).
2. **② 재결합 표** — 발사 핀에 묶을 지문 전부: 봉인 32 code_fp · 기대 세대 (g2) · 입력 ID 집합 (`ids_sha256` production194 `a04282d7…` · supp20 `991cf115…`) · 원 dump hash 표 · 코호트 TSV (194 §2 · 보충 §2 `a7aaa3c8…` · `69d3f913…`) · 인계 도구 (`g2_network_reread.py` 등) · 배포 빌더 — 칸 = {등록 값 · 지금 HEAD 계산 값 (저장소 함수 · 명령) · 같음 / 다름 · 다르면 이유 (어느 커밋 · 등록 개정에 들어가야 하는지)}.  계산은 짧은 것만 (해시 · 지문) · 무거운 시험 금지.
3. **③ B7 승인 핀** — 정의 (= 1저자 비준 문안이 들어간 커밋 · push 된 SHA) · 사전 점검 · 두 manifest · `--approved-sha` 가 그 SHA 를 어떻게 싣는지 (코드 자리 file:line) · `runner.sha256` = 기록 전용 (SUPR 판정문 한정).
4. **④ WSL 명령 블록** — 10-14 사전 점검 (194 §9-7 · 보충 §9-1) 명령을 새 핀 · 새 ROOT 둘 (194 · 보충 20 · 날짜 붙은 새 이름 · 10-14 ROOT 는 지우지 않음) 로 다시 쓴다: 체크아웃 (승인 핀) · 깨끗한 트리 · fast16 · real4 · `--observe-imports` · `run --dry-run --preflight-receipt P.json` (전체 로그 + 완료 영수증) · `preflight-verify` · 보충 영수증 도구 · 194 §2 여섯 칸 손 대조 (자동 대조 = v1.3 뒤 · 1저자 10-14) · 1저자가 올릴 묶음 (tgz 이름 · 내용).  1저자가 WSL `~/dem-audit` 에서 그대로 붙일 수 있게 (CLAUDE.md: 가지 = `claude/stoic-knuth-NObVQ`) · 주소 · 포트는 적지 않는다 · 실제 발사 명령은 **"⑤ 승인 뒤"** 표지와 함께 꼴만.
5. **⑤ 1저자 확인표** — 발사 승인 전에 1저자가 볼 증거 목록 (영수증 rc · 지문 일치 · fast16/real4 결과 · 관측 의존성 · 손 대조) · 구 ROOT · 실패 기록 처리 (보존 · 덮지 않음).
6. **Codex 짧은 발사 확인 요청 초안** (권고 = 보냄 · ⬜ 1저자 Q5) — 같은 문서 끝 절 또는 `docs/reviews/codex_lhs214_relaunch_check_request_20261020.md` · 맨 위 닫는 것 / 닫지 않는 것 · 질문 (비준판 문안 · 지문 재결합 · 사전 점검 기록이 §5 다섯 단계를 채우는가) · 리뷰 핀 = ⬜ (메인).
7. 사전 공격 리뷰 (CLAUDE.md ①): 이 문서의 숫자 · 지문 · 전칭 (*"같음"* · *"변화 0"* · *"전부"*) 을 네가 돌린 명령 출력과 한 줄씩 대조 — 출력 원문을 문서 부록에 짧게 (명령 · 결과).
8. `python3 scripts/check_doc_refs.py` (`✓ 깨진 참조 없음`) → 커밋 하나 (영어 메시지 · 모델 이름 없음 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`).  원격에 없는 커밋 번호를 문서에 쓰지 않는다 (`SELF-116` — 네 커밋 번호 포함).

## 규칙
- 코드 고치지 않음 (필요해 보이면 멈추고 보고) · 원장 · CLAUDE.md · 진행 기록은 안 고침 (메인이 한다) · 다른 에이전트 셋 + 게이트가 같이 돈다 — CPU · 디스크 적게 (큰 사본 금지).
- 보고 (한국어 · 표 · 짧게): 커밋 SHA · 지문 대조 표 (같음 / 다름) · 다른 것 + 이유 · WSL 명령 블록 위치 · 남은 ⬜.
