# 지시서 — Rint ② 코드 묶음 (Q11 + Q2) 내부 반박 리뷰 (독립 조수 · Codex 아님 · 11-12)

## 0. 할 일

작업 트리 `/home/user/rint-codepkg` 의 `af3cce37b..2f97617ef` (커밋 셋: ebb0e9f80 시험 먼저 · f17ea8c6b 구현 · 2f97617ef 시험 보강) 를 **반박하는 눈으로** 본다. 고친 사람의 설명 (`rint/codepkg/notes.md` · `amend_drafts.md` · `logs/`) 은 **맨 마지막에** 주장 대조에만 쓴다 — 먼저 diff 와 아래 "의도" 문서만으로 판단한다. 판정이 아니라 지적 목록이다 (1저자 11-10 운영 결정: Codex 토큰 소진 → 내부 반박 리뷰 · Codex verified 로 올리지 않음).

## 1. 의도 (무엇을 하려던 코드인가)

- 1저자 11-12 결정: 리포 `docs/reviews/rint2_time_reestimate_20261111/README.md` 의 결정 절 (Q11 = GPU 전처리 C 꼴 — Jacobi 를 LinearOperator matvec 로 · Q2 = 탄소 접합 준비 (원장) 저장본 재사용 · 둘을 한 코드 묶음으로 · 시험 먼저 · 봉인 전에만 넣을 수 있음) · 벤치 `docs/reviews/rint2_time_reestimate_20261111/bench/results_20261112/README.md` (3.40–3.79 배 · 합성 200 반복 해 비트 같음).
- 설계 (구현 전): `…/scratchpad/rint/codepkg/design.md` · 원 지시서 `…/scratchpad/rint/codepkg/BRIEF_codepkg.md` · 대피 이어받기 지시서 `BRIEF_evac.md`.
- 리포 규칙: CLAUDE.md 의 "Codex 요청 전 사전 공격 리뷰" ① – ⑤ (숫자 · 전칭 대조 · 지난 HOLD 부류 · 보장마다 작은 해석 반례 · 재개 규칙 처분 기준).

## 2. 볼 것

1. **바뀐 함수마다 지난 HOLD 부류**: NaN · inf · 넘침 · 빈 · 중복 · 검사 전 정규화 · 유니코드 숫자 · 공백 · 증서 ↔ 결과 결합 누락 · 다른 판본 증서.
2. **보장마다 작은 반례** (손으로 풀리는 크기): ⓐ 끔 경로 = 바탕 (af3cce37b) 과 비트 같음 ⓑ 저장본 열쇠가 원장에 영향을 주는 입력을 빠짐없이 덮나 (침대 · 복셀 · 접합 인자 · 스키마 · 코드 판 · 기하) — 하나만 바꾼 두 입력이 같은 열쇠를 받는 꼴이 있나 ⓒ 낡거나 어긋난 저장본을 돌려주는 길 (다른 침대 · 다른 코드 · 손으로 고친 파일 · 반쯤 쓴 파일 · 두 팔이 같은 저장본을 동시에 씀 · 쓰는 중 끊김) ⓓ 소유자 · 권한 검사 ⓔ GPU 전처리 꼴이 수렴 판정 · 반복 수 · 잔차 정의를 바꾸지 않나 · cupy LinearOperator 가 없을 때의 길 ⓕ 사슬 (rint_r_chain) · 계약 (run_contract) · 러너 (sdcp_gain_vox015_8arm.sh) 에 새 칸이 결속되나 (증서 ↔ 결과).
3. **새 시험이 옳은 이유로 실패하나**: 고친 곳을 되돌린 변이 몇 개를 스크래치 사본에서 넣어 본다 (구현 쪽 변이 목록과 따로 · 네가 고른 것).
4. **숫자 · 전칭**: 커밋 메시지 · 시험 이름 · 주석의 "비트 같음 · 전부 · 0" 같은 말을 시험 출력과 대조.

## 3. 규칙

- `/home/user/rint-codepkg` 는 **읽기만** (git 상태를 바꾸지 않는다). 변이 · 실험은 `git -C /home/user/rint-codepkg archive 2f97617ef | tar -x -C <새 빈 폴더>` 로 만든 사본에서 (`…/scratchpad/rint/codepkg/review/work/` 아래).
- 리포 본 트리 `/home/user/Yonghoon-DEM-DFT` 는 게이트가 도는 중 — 읽기만 · git 으로 상태를 바꾸는 명령 금지.
- 킷 풀이 · GPU 실행 · σ 열람 없음 · 봉인 상수 그대로. 신호 실험은 `unshare -pf --mount-proc --kill-child` 안에서만 (kill 번호 = 직접 만든 자식 · > 1).
- 시험은 한 번에 무거운 것 하나 (기계 4 CPU · 게이트 · 다른 조수와 나눔). 오래 걸리는 끝-끝 시험은 필요할 때만.
- 주소 · 포트 · 계정은 파일에 쓰지 않는다. Artifact 도구 · 웹 게시 도구는 쓰지 않는다.

## 4. 산출

`…/scratchpad/rint/codepkg/review/review_codepkg.md` — 머리 "내부 반박 리뷰 (Codex 아님) · 대상 af3cce37b..2f97617ef · 11-12". 지적 표 `번호 (RCP-NN) | 등급 (P1 = 틀린 결과를 받아들이거나 R 결과를 바꿈 / P2 = 봉인 · R 전에 고쳐야 함 / P3 = 표기 · 명료 · 시험 틈) | 어디 (파일:행) | 반례 · 재현 | 고칠 방향`. 그다음 보장 ⓐ–ⓕ 각각 "깨짐 / 조건부 / 섬" 표 · 변이 결과 · 확인 못 한 것.

## 5. 답장

10 줄 안팎: P1 · P2 · P3 수 · 가장 무거운 셋 · 보장 ⓐ–ⓕ 판정 · 산출 파일 전체 경로.
