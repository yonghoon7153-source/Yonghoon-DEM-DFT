# PB1 조인 보강 (JOIN_VERSION v5) 사전 공격 리뷰 + 문장 대조 (읽기 전용 · 10-20 밤)

너는 Codex 를 대신하는 **적대 검토자**다.  목표 = 이 수정이 Codex 에 가면 HOLD 를 받을 반례를 **먼저** 찾는 것.
순서가 중요하다: **먼저 공격 (1–4) 을 코드 · 시험만 보고** 하고, 그 다음에야 (5) 요청서 · 커밋 메시지 문장을 읽고 대조한다 — 고친 사람의 설명에 끌려가지 않기 위해서다.

## 대상
- 사슬 (본 가지 · 원격 push 진행 중): `d1768cf0c` (기준 · v4 모듈 = `a2cfd0365` 판과 같은 코드) → `af8d1d501` (시험 먼저) → `263c9502b` (수정 · v5) → `c4bdf18c9` (기록) → `828ca9802` · `952ad1a25` (문서만).
- 코드 diff: `git -C /home/user/Yonghoon-DEM-DFT diff d1768cf0c 263c9502b -- scripts/rint_iface_join.py scripts/test_rint_g2_join.py`
- 작업 자리: 너만 쓰는 분리 작업 트리 — `git -C /home/user/Yonghoon-DEM-DFT worktree add --detach /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/wt_prerev_pb1 952ad1a25` · 끝나면 `git -C /home/user/Yonghoon-DEM-DFT worktree remove --force <그 경로>`.  탐침 · 변이 사본 · 임시 파일 = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prerev_pb1/` 만 (쓰고 끝에 큰 것은 지운다 · 디스크 여유가 작다 — real14 같은 큰 사본 금지, 작은 합성 입력만).
- 근거 (공격 단계에서 읽어도 되는 것): Codex 판정문 `docs/reviews/codex_review_rint_join_rimpr_q7_recheck_20261020.md` (§3 · §4 · §6 · §7) · 그 증거 탐침 `docs/reviews/codex_rint_join_rimpr_q7_recheck_evidence_20261020/probes/` · 원장 `RIMPR-*` 항목 (`docs/reviews/findings.json`).  ⛔ 공격 단계 (1–4) 에서는 `af8d1d501` · `263c9502b` 커밋 메시지 · `docs/reviews/codex_rint_carbon_additive_design_request_20261020.md` Part B · `docs/reviews/rimprr_fix_plan_20261020.md` §3 끝을 읽지 않는다.

## 할 일
1. 바뀐 함수를 **모듈 문맥 안에서 전부** 읽는다 (호출자 · 피호출자 · 조인 결과를 소비하는 자리 전부 — 계획 · 정량 관문 · CLI · grep).
2. v5 가 새로 넣은 검사 넷 (머리 줄 표지 경계 = ASCII 공백 · 탭 · 줄 끝만 · 덤프 글자 어휘 관문 TAB · LF · CR · 0x20–0x7E · scaffold 실수 열 ASCII 고정소수 문법 + 주석 아닌 줄 어휘 · scaffold step 선언 ASCII · int64) 마다 지난 HOLD 부류로 반례를 **직접 만들어** 돌린다 — 각 = 입력 · 결과 (PASS / 거부 · 사유) · 기대:
   - **같은 부류의 남은 구멍**: 어휘 관문이 줄로 쪼개기 **전** 원문 전체에 걸리는가 (gzip 풀기 뒤 · 디코딩 오류 처리 · `errors=` 가 무엇인지 · 잘못된 UTF-8 바이트 · 0x7F DEL · NUL · BOM U+FEFF · 서로게이트) · CR 만 줄 끝 · CRLF 섞임 · 마지막 줄 개행 없음 · 탭 열 구분 · 겹 공백 · scaffold 의 주석 판정 (`#` 앞 공백 · 줄 중간 `#` · 주석 줄 안 비-ASCII = 통과해야 함) · 빈 줄 · scaffold 머리 행 · 실수 문법이 받는 꼴 (`.5` · `5.` · `+5` · `-0` · `1e-05` · `1E5` · 지수 표기 — 실제 생산 scaffold 값 꼴과 맞는지 리포의 scaffold CSV 에서 확인) · 6 자리 넘는 정밀도 · 아주 긴 토큰 · 아주 긴 step 숫자 (int() 한도 · int64 경계 2^63−1 · 2^63) · step 선언 꼴 변형 (`# step 100` · `#step 100` · `# Step 100` · `# step=100` · 두 번 선언 · 선언 없음).
   - **정상화 뒤 검사 부류**: 어휘 관문 통과 뒤 다시 `str.split()` · `strip()` 이 쓰이는 자리가 남아 비-ASCII 를 조용히 정리하는 길이 있는가 (scaffold 경로 · contact 경로 · 머리 열 경로 각각).
   - **넘침 · 비유한 (RIMPR-04 open 한정 목록 밖인가 확인)**: 새 검사 자체가 `inf` · `nan` 문자열 · 언더플로 수를 어떻게 다루는가.
   - **결합 · 판본**: v4 로 만든 조인 기록 · 결과를 v5 계획 · 정량 관문이 받는 길이 있는가 (`JOIN_VERSION` 확인 유무 — grep) · 새 사유 칸 (`atom_lexical` · `contact_lexical` · `scaffold_grammar` · `scaffold_lexical` · `scaffold_step`) 이 `join_gate_failed` 로 **모든** 소비 경로에 닿는가.
   - **거짓 거부 위험 (똑같이 중요)**: 실제 LIGGGHTS 꼴 atom · contact 덤프 (`… omegaz radius ` 끝 공백 · `pp pp ff` · `mm` · `fs` · `sm` · contact `ITEM: NUMBER OF ENTRIES` · `ITEM: ENTRIES c_…`) · 리포 안 scaffold CSV 전부 (`git ls-files '*scaffold*.csv'` 등 — 고정소수 아닌 토큰 · 비-ASCII 수를 다시 센다) · 리포 안 real14 · case15 실자료가 시험에서 쓰이는 자리 (그 시험만 한 번 돌려 확인 — 사본 만들지 말 것).
3. **시험이 옳은 이유로 통과하는지** — 새 묶음 (J15 · J16 · J17 · J18 · J15P · J13 ⑤) 의 반례마다 거부 사유가 **의도한 검사**인지 (앞의 다른 검사에 먼저 걸려 우연히 통과하는 것 아닌지).  변이 시험: 새 검사 넷을 하나씩 되돌린 사본 모듈 (`prerev_pb1/` 안) 에 새 시험을 돌려 **실패해야** 한다 — 안 실패하는 시험 = 그 검사를 지키지 못함 (수 · 이름).
4. Codex 탐침 넷 (`structure_probe.py` · `structure_minimal_replay.py` · `numeric_review.py` · `numeric_overflow_replay.py`) — 먼저 **전부 읽고** 네트워크 · 묶음 밖 쓰기 · 삭제 · 임의 subprocess 가 없을 때만 `prerev_pb1/` 로 복사 · 경로 상수만 바꿔 `python3 -I -X utf8 -B` 로 v5 트리에서 한 번씩.  리뷰 핀 기록 (같은 증거 폴더의 결과) 과 다른 것만 표로 (판정 뒤집힘 · 사유 추가 구분).
5. (공격이 끝난 뒤에만) 문장 대조 — `docs/reviews/codex_rint_carbon_additive_design_request_20261020.md` Part B (B-0 · B-1 · B-2 · B-4) · 원장 `RIMPR-R01` · `RIMPR-03` · `RIMPR-04` · `SELF-125` note · `docs/reviews/rimprr_fix_plan_20261020.md` §3 끝 · 커밋 메시지 셋 의 숫자 · 전칭 (*"전부"* · *"N/N"* · *"바이트 같음"* · *"0"* · *"닫힘"*) 을 git · 네가 돌린 출력과 한 줄씩 대조 (범위 · 시험 판을 같이 — `SELF-124` 부류).  특히: `af8d1d501` 메시지 *"pre-fix 231/309, fails = the 39 new counterexamples"* (실패 검사 수 78 ↔ 반례 39) · *"리포 scaffold 41 파일 · 2,042,453 행 · 고정소수 아닌 토큰 0"* · real14 · case15 *"배열 11 종 바이트 같음"* · 탐침 *"같음 130 · 다름 14"* · *"같음 97 · 다름 16"*.

## 규칙
- **리포 · 다른 작업 트리를 고치지 않는다 · 커밋 · push 하지 않는다 · `scripts/check_all.sh` 안 돌린다** (본 트리에서 게이트가 돌고 있다).  분리 작업 트리 안 파일도 고치지 않는다.
- 다른 에이전트 셋이 같이 돈다 — 시험 전체는 한두 번만 · 수천 번 반복 · 몇 분 넘는 전수 탐색 금지 · 병렬 실행 금지.
- 보고 (한국어 · 표 중심 · 짧게): ① 반례 표 (부류 · 입력 요약 · 결과 · 기대 · Codex 예상 등급 · 같은 부류 ID · 최소 수정 + 시험 한 줄) ② 변이 시험 표 ③ 거짓 거부 확인 표 ④ Codex 탐침 표 (다른 것만) ⑤ 문장 대조 표 (자리 · 문장 · 실제 · 맞음 / 정정 문구) ⑥ "Codex 에 보내기 전 고쳐야 할 것" 과 "요청서에 한정으로 적으면 될 것" 두 목록.  재현 파일 경로 (`prerev_pb1/…`) 를 같이 적는다.
