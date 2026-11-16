# 지시서 — Rint ② 코드 묶음 고침 짧은 재리뷰 (11-12 밤 · 고친 곳만 · 독립 조수 · Codex 아님)

## 0. 할 일

내부 반박 리뷰 `…/scratchpad/rint/codepkg/review/review_codepkg.md` (RCP-01 … 11) 를 고친 커밋 셋 — 작업 트리 `/home/user/rint-codepkg` 의 `2f97617ef..0ac6edf3c` (`4557a30c2` 시험 먼저 · `94765bed3` 고침 · `0ac6edf3c` 게이트 배선) — 이 지적을 실제로 닫았나 **고친 곳만** 본다. 규칙 · 등급 · 표 꼴은 1 회차 지시서 `BRIEF_review_codepkg.md` 2–4 절 그대로 (지난 HOLD 부류 · 보장마다 작은 해석 반례 · 변이 · 숫자 · 전칭).

1. RCP 마다 "닫힘 / 일부 / 안 닫힘" (근거 한 줄 · 시험 이름 · 행).
2. 특히:
   - **RCP-01 (P1 · 저장본 열쇠)**: 열쇠의 코드 칸 넷 (`fibre_segment_raster.py` 더함) · find_spec 경로 찾기 (모듈을 불러오지 않음) · T14 가 짓는 동안 실제로 돈 파일 · import 를 잰다는 주장 — 원장 값에 영향을 주는데 열쇠가 덮지 않는 입력이 남았나 (다른 모듈 · 라이브러리 판 numpy / scipy · 파이썬 판 · 기계) 를 손 반례로. 옛 저장본이 새 코드에서 적중하는 꼴이 남았나.
   - 05 실행 자리 지문 · 06 소유자 · 모드 검사 + 폴더 심볼릭 거부 (Store · 사슬 · 러너): 경로 중간 성분의 심볼릭 · 검사와 사용 사이 바꿔치기 · 정직한 심볼릭 뿌리 (홈이 다른 자리로 가는 기계) 에서 정직한 런이 거부되는 꼴.
   - 08 `no_linop` · 09 ±0 · 비정규 수 · 10 `STORE_RASTERIZE_ONLY` · 예외 → 구조화 거부 · 11 머리 JSON 호스트 이름.
   - RCP-02 게이트 배선 (`scripts/check_all.sh` 세 단계 + 끝-끝 줄 · kgy 16 묶음) — 단계가 실제로 새 시험을 부르나 · 실패가 게이트 실패로 이어지나.
   - RCP-04 S0 다시 재기 블록 `s0probe/s0_rerun_probe_block.txt` — 읽기 · 쓰기 자리 · 원 산출 안 건드림 · 문턱 [제안] (쓰기 ≤ 600 s · 읽기 ≤ 300 s ∧ 짓기의 10 % 이하 · 메모리 증가 ≤ 4 GiB · 파일 ≤ 2 GiB) 이 결과 전에 적혀 있나 · 멈춤 셋 rc 2.
   - GPU 확인 블록 4 판 `gpu_check_block.txt` — 핀 · 모듈 sha256 (`859310da…`) · 하네스 md5 대조가 실제 파일과 맞나.
3. 끔 경로 = 바탕 `af3cce37b` 와 비트 같음 (σ_e 같음 · 다른 칸 = 코드 신원뿐) 주장을 작은 실침대 없이 확인할 수 있는 만큼 (픽스처 킷).
4. 변이: 고친 곳을 되돌린 변이 몇 개를 네가 골라 넣어 본다 (구현 쪽 · 1 회차 리뷰어 목록과 따로).
5. 고친 쪽 설명 (`notes.md` · `amend_drafts.md` · `logs/r2/`) 은 **맨 마지막에** 대조에만.

## 1. 규칙

- `/home/user/rint-codepkg` 는 읽기만 (git 상태 변경 금지). 변이 · 실험 = `git -C /home/user/rint-codepkg archive 0ac6edf3c | tar -x -C <새 빈 폴더>` (`…/scratchpad/rint/codepkg/review/work2/` 아래).
- 리포 본 트리 `/home/user/Yonghoon-DEM-DFT` 도 읽기만.
- 킷 풀이 · GPU · σ 열람 없음 · 봉인 상수 그대로. 신호 실험은 `unshare -pf --mount-proc --kill-child` 안에서만 (kill 번호 = 직접 만든 자식 · > 1 · 자기 · 부모 아님).
- 무거운 시험은 한 번에 하나 (기계를 다른 조수와 나눔). 오래 걸리는 끝-끝은 필요할 때만.
- 주소 · 포트 · 계정 · 홈 경로 · 호스트 이름 값을 산출에 쓰지 않는다. Artifact 도구 · 웹 게시 · 시스템 패키지 설치 · 시스템 설정 (apt · update-alternatives) 변경 금지.
- 하네스가 보고 파일 쓰기를 막으면 답장에 같은 꼴로 싣는다. 한국어 · 표 중심 · 짧게.

## 2. 산출 · 답장

- `…/scratchpad/rint/codepkg/review/rereview_codepkg.md` — 머리 "내부 반박 리뷰 재확인 (Codex 아님) · 대상 2f97617ef..0ac6edf3c · 11-12". RCP 별 닫힘 표 · 새 지적 표 (`RCP2-NN | 등급 (P1 = 틀린 결과를 받아들이거나 R 결과를 바꿈 / P2 = 봉인 · R 전에 고칠 것 / P3 = 표기) | 어디 | 반례 · 근거 | 고칠 방향`) · 변이 표 · 확인 못 한 것.
- 답장 = 10 줄 안팎: RCP 닫힘 / 일부 / 안 닫힘 수 · 새 P1 · P2 · P3 수 · 가장 무거운 둘 · 끔 경로 판정 · 산출 파일 전체 경로.
