# 지시서 — Rint ② 코드 묶음 2 회차 고침의 짧은 독립 재확인 (11-12 밤 · 내부 반박 리뷰 · Codex 아님)

## 0. 대상

작업 트리 `/home/user/rint-codepkg` 의 `0ac6edf3c..ea3b13b89` (커밋 7 = f8077a51d 시험 먼저 → 4e1e5b6c6 고침 → ac7e1c58d 게이트 배선 → 8cc3fe462 · 609d78ca4 변이 보강 → c0ff22431 시험 먼저 → ea3b13b89 고침). 고친 쪽 설명은 일부러 주지 않는다 — 판단 근거는 diff 와 지난 리뷰 `…/scratchpad/rint/codepkg/review/rereview_codepkg.md` (RCP2-01–06 · RCP-03 · 04 · 06 남은 몫) 뿐.

## 1. 할 일

1. 재리뷰 지적마다 닫힘 · 부분 · 안 됨 (근거 = 파일:행 · 시험 이름).
2. **보장마다 작은 해석 반례** (CLAUDE.md 사전 공격 ③): RCP2-01 "런 시작 뒤 코드가 바뀌면 저장 안 함" (짓기 전 · 발행 직전 다시 셈 · 시각 1 s 규칙 — 같은 초 안 두 번 쓰기 · 크기 같은 바꿔치기 · mtime 되돌림 · 심볼릭 · 먼저 불린 모듈) · RCP2-06 "GIT_* 전부 지움" (`GIT_` 접두 아닌 git 환경 = `GIT_CONFIG_*` 는 접두에 들어가나 · `HOME` · `XDG_CONFIG_HOME` 의 전역 설정 · `-c` · 부모 리포 탐색 (`GIT_CEILING_DIRECTORIES`) · 하위 프로세스에 env 를 안 넘기는 자리) · RCP2-02 경로 정규화 (`a/./b` · `a//b` · 끝 `/` · 대소문자 · 유니코드 정규화) — 깨지면 반례 + 등급, 안 깨지면 시도한 꼴 목록.
3. 고친 쪽 보고의 숫자 · 전칭 대조: 시험 수 (store 62 · git_env 10 · run_contract 125 · e2e 51 · e2e12 33 · conv_cert 30 · Q11 19 · 사슬 506) 중 **가벼운 것만** 다시 돌려 확인 (store · git_env · run_contract selftest · Q11). 사슬 · e2e · conv_cert 같은 무거운 것은 돌리지 않는다 (본 세션 게이트가 돌고 있다) — 로그 `…/scratchpad/rint/codepkg/logs/r3/` · `r4/` 의 rc · 줄 수만 대조.
4. 봉인 대조 주장 (손댄 파일이 194 CODE_FILES 32 · 언로딩 키트 SHA256SUMS · 믹서 봉인에 없음) 을 직접 다시 대조.
5. 등급 P1 · P2 · P3 · 새 지적은 고칠 방향 한 줄.

## 2. 규칙 (꼭)

- **`GIT_DIR` · `GIT_WORK_TREE` · `GIT_INDEX_FILE` 을 export 하거나 명령 앞에 붙이지 않는다.** env 반례 시험이 필요하면 `unshare -pf --mount-proc --kill-child` 안에서 · 스크래치에 `git init` 한 **일회용 리포만** 가리킨다 (본 리포 · 작업 트리 리포를 가리키지 않는다).
- 본 리포 `/home/user/Yonghoon-DEM-DFT` 에서는 아무 git 명령도 치지 않는다. 작업 트리 `/home/user/rint-codepkg` 은 읽기만 (`git -C /home/user/rint-codepkg diff/show/log` 는 됨 · checkout · commit · reset 금지). 시험을 돌릴 때는 스크래치 사본 (`git -C /home/user/rint-codepkg archive ea3b13b89 | tar -x -C <스크래치 새 폴더>`) 에서.
- 킷 풀이 · GPU · σ 열람 없음. 무거운 시험 금지 (위 3). 주소 · 포트 · 계정 · 홈 경로 값 쓰지 않음. Artifact 도구 · 웹 게시 · 시스템 패키지 설치 · 시스템 설정 변경 금지. 큰 사본은 끝나면 지운다 (디스크 빠듯).
- 산출 = `…/scratchpad/rint/codepkg/review/recheck2_codepkg.md` (+ 반례 스크립트 · 출력 같은 폴더 `recheck2/`).

## 3. 답장

8 줄 안팎: 지적별 닫힘 · 부분 · 안 됨 수 · 새 지적 (등급 수 · 한 줄씩) · 반례 시도 결과 · 숫자 대조 · 봉인 대조 · 산출 파일 전체 경로.
