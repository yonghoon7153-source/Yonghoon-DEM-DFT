# 문법 fixture 실행 1 — ibb job 285220 (2026-10-14 19:26 · 작업 트리 `a30fe150e`) = FAIL (rc 2) · fixture 결함

| 파일 | sha256 | 무엇 |
|---|---|---|
| `gram_20261014_192604.report.tgz` | `015bd82ba266a3438db003a0e6cf025d4ad38ac51133ab75307be402c60ca7ee` (= 러너가 찍은 값) | 보고 묶음 (40 항목 · P · GA · 판정 · 키트 SHA256SUMS) |
| `ulHist_285220.out` | `6e391d74c6324805b44e9ee125762ab124e923d42ddd627968f5c650c2dbe292` | SLURM 출력 |

- 1저자가 WSL 로 받아 올림 · 반입 처리 = 새 빈 폴더 · sha256 대조 · 멤버 안전 (절대 경로 · `..` · 링크 0) · 읽기만.
- 원인 (GA `log.liggghts` 끝): `variable gr_P equal f_gr_av[1]` → `variable gr_P equal ${gr_P}` 에서 `ERROR: Mismatched fix in variable formula (../variable.cpp:1315)` — fixture 의 `gr_av` ave/time 입력 하나 (= 전역 스칼라) 를 벡터로 읽음.  원장 `SELF-115` = Codex `ULKRR-01` (같은 결함 · 소스 증명) · 고침 `039abb141`.
- 이 실행으로 **실제 바이너리에서 통과한 문법**: 빈 상태 파일 `include` · `if … jump SELF` 처음 경로 · `label` · `GRAM_START` (2000 · k 0 · 0.03) · 변수 주기 덤프 (창 끝 2100 에만 · setup 덤프 없음) · 판 mesh/stl 덤프 (2000 · 2100) · 첫 창 run 100 step.
- 아직 안 거친 문법: 상태 파일 쓰기 · `write_restart` · `move/mesh` 여러 번 · GB 이어 돌림 → 실행 2 (`77b5885e0` 이후).
- job 285228 (같은 날 · 옛 작업 트리 `a30fe150e` 로 제출됨) 은 1저자가 옛 덱 확인 (`c_gr_ke c_gr_erot` 0 줄) 뒤 취소 — 결과 없음.
