# 지시서 — Rint ② 코드 묶음 2 회차 고침 (11-12 밤 · 시험 먼저 · 작업 트리 `/home/user/rint-codepkg`)

## 0. 할 일

재리뷰 `…/scratchpad/rint/codepkg/review/rereview_codepkg.md` (RCP 닫힘 7 · 일부 3 (03 · 04 · 06) · 한정 1 (07) · 새 P2 2 · P3 4) 를 `0ac6edf3c` 위에서 고친다. 순서 = 시험 먼저 커밋 (고치기 전 실패 수 기록) → 고침 커밋 → (필요하면) 게이트 배선 · 문서 커밋. 서명 없음 · push 없음 (반입 = 본 세션).

1. **RCP2-01 (P2)** — 저장본 열쇠의 코드 칸이 Store() 때 디스크 해시라, 런 도중 코드가 바뀌면 옛 코드로 지은 원장이 새 코드 열쇠로 저장되고 뒤의 정직한 런이 hit 로 받는다 (반례 CE-A). 고칠 방향: 런 시작 때 잰 코드 칸과 발행 직전에 다시 잰 코드 칸이 다르면 저장하지 않음 (구조화 사유) · 시험 = CE-A 꼴 (시작 뒤 열쇠 코드 파일 하나를 바꿈 → 저장 안 됨 · 정직 흐름 = 저장 · 그 뒤 hit).
2. **RCP2-06 (P2)** — 시험 · selftest 가 git 을 부를 때 `GIT_DIR` · `GIT_WORK_TREE` · `GIT_INDEX_FILE` · `GIT_OBJECT_DIRECTORY` · `GIT_ALTERNATE_OBJECT_DIRECTORIES` · `GIT_COMMON_DIR` 를 지우지 않아, 부르는 쪽 환경이 새면 남의 리포에 쓴다 (11-12 밤 실제 사고: `run_contract.py --selftest` RCPT-sha 의 임시 `git init · add -A · commit` 이 본 리포 가지에 커밋을 만듦 · 본 세션이 되돌림). 쓰기 쪽 (`run_contract.py` selftest RCPT-sha · 이 묶음이 고친 시험들) 은 git 부를 때 위 환경을 지운 env 를 넘긴다 · 읽기 쪽 (`mpm_webapp_payload.py` `_code_sha` 639 행 근처 · `test_step3_gpu_precond.py` 69 행 근처) 도 같은 꼴로 (새면 남의 리포 sha 를 읽음). 시험 = `GIT_DIR` 를 다른 임시 리포로 export 한 채 selftest 를 돌려도 그 임시 리포가 바뀌지 않고 결과가 같음 (고치기 전 = 그 임시 리포에 커밋이 생김을 실패로 기록). ⚠ 이 시험은 **반드시 일회용 임시 리포를 GIT_DIR 로** 쓴다 — 본 리포 · 작업 트리 리포를 가리키지 않는다. 봉인된 파일인지 먼저 확인 (`scripts/run_network_194_parallel.py` CODE_FILES · 언로딩 키트 SHA256SUMS · 그 밖 봉인 목록) — 봉인 파일이면 고치지 말고 보고.
3. **P3 넷** — RCP2-02 (`링크/.` 꼴이 Store · 사슬 · 러너 세 겹 심볼릭 거부를 비켜 감 → 경로 정규화 뒤 성분마다 검사) · RCP2-03 (모드 검사 0o002 변이 N9 를 못 잡음 → 그룹 쓰기만 있는 갈래 시험) · RCP2-04 (S0 블록의 문턱 · 기대를 블록 머리 주석과 리포 문서 자리에 · 1저자 11-12 밤 오버나잇 = Q-B (가) · 문턱 [제안] 그대로 채택) · RCP2-05 (T14 가 scripts/ 안 모듈만 봄 → 범위를 적거나 넓힘).
4. 일부였던 RCP-03 · 04 · 06 은 리뷰가 적은 남은 몫만 · 못 하면 한정 문장으로.
5. 다시 돌릴 것: 저장본 시험 · Q11 · 사슬 · e2e · e2e12 · conv_cert · kgy 3.8 묶음 (전과 같은 꼴) · 변이 (리뷰어 N9 포함) · 끔 경로 = 바탕 대조. GPU 확인 블록 · Q11PIN 은 바뀐 sha 로 5 판.

## 1. 규칙 (꼭)

- **`GIT_DIR` · `GIT_WORK_TREE` · `GIT_INDEX_FILE` 을 절대 export 하거나 명령 앞에 붙이지 않는다** (위 2 의 일회용 임시 리포 시험만 예외 · 그때도 그 임시 리포만). git 이 필요하면 작업 트리 `/home/user/rint-codepkg` 안에서 그대로 (그 작업 트리의 HEAD 만 움직인다) 또는 scratch 사본 안에서 따로 `git init`.
- 본 리포 작업 트리 `/home/user/Yonghoon-DEM-DFT` 에서는 아무 git 명령도 치지 않는다 (읽기 포함 — 필요하면 `git -C /home/user/rint-codepkg show <sha>:<경로>`).
- 킷 풀이 · GPU · σ 열람 없음. 신호 실험은 `unshare -pf --mount-proc --kill-child` 안에서만. 무거운 시험 하나씩 (다른 조수 · 게이트와 기계를 나눔).
- 주소 · 포트 · 계정 · 홈 경로 · 호스트 이름 값을 산출에 쓰지 않는다. Artifact 도구 · 웹 게시 · 시스템 패키지 설치 · 시스템 설정 변경 금지.

## 2. 답장

10 줄 안팎: 커밋 sha (시험 먼저 → 고침 → …) · 고치기 전 → 뒤 시험 수 · RCP2-01 · 06 처분 · P3 고침 · 봉인 파일 확인 결과 · 변이 · 끔 경로 · GPU 블록 5 판 · 남은 [미확인] · 산출 파일 전체 경로.
