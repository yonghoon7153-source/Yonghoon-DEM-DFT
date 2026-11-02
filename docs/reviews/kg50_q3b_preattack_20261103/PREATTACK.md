# Q3 (나) 압축 루프 재개 · 준비 구간 순서 고침 — 사전 공격 리뷰 (2026-11-03)

대상: `scripts/resume_ckpt.sh` sha256 `66006239ec58043f963fa885f9db545c63614d279bfb6cac1665a2eae9884c6d`
(kg50-q3b = `f37d5ee03` + 여섯 커밋 `4882eb295` · `066c6a0fc` · `59a5bab72` · `f1bbd274e` · `de4c5d741` · `d058816fb` · stoic 쪽 같은 sha 판도 도구 바이트 같음).
리뷰어 = 고친 사람 설명 없이 diff · 실제 덱 · 시험 하네스만 봄.  도구 원본은 안 건드렸다.

재현: `python3 docs/reviews/kg50_q3b_preattack_20261103/probes.py` (출력 `probes_out.txt`) ·
`python3 docs/reviews/kg50_q3b_preattack_20261103/mut.py <임시 폴더>` (출력 `mut_out.txt`) · 기준 `python3 scripts/test_resume_ckpt.py --only QB` = **52 PASS · 0 FAIL**.
⚠ 한계: 실제 `dem_restart.py` 는 리포에 없다 — 재개 덱은 시험 하네스의 합성 r075 꼴 (`qb_raw`) 만 썼다.  실제 ibb 산출 순서가 다르면 결과가 다를 수 있다.

## 발견

| # | 등급 | 한 줄 | 실제 D0.7 재개 |
|---|---|---|---|
| A | **P2** | 루프 위상을 작업 폴더 본 덱의 run 합으로만 정한다 — 체크포인트를 쓴 런 (원 로그) 의 판정 step 과 묶지 않고, G0–G3 는 위상에 눈멀다 | 영향 없음 (추정 · 확인 한 줄 아래) |
| B | **P2** | 순서 고침의 "본 덱 자리" = 다시 정의한 **마지막 줄** 자리 ↔ LIGGGHTS 는 다시 정의한 fix 를 **첫 정의 칸**에 둔다 → 고친 뒤도 원 런 fix 순서가 아니고, 비가환 fix 가 있으면 물리가 다른 덱이 통과한다 | 합산 순서만 (roundoff) — 청구 ② 는 이 덱에서 성립 |
| C | P3 | 청구 ③ "같은 명령 n 번 → 본 덱 마지막 n 자리" 를 지키는 시험 없음 (n < m · n > m 변이 둘 다 52/52 통과) | 영향 없음 (정적 대조가 둘 다 받음 · 같은 끝 상태) |
| D | P3 | G3 는 "원 로그 정규 줄 ⊆ 시험" 한 방향만 — 시험의 run 끝 줄 (S0 + r) 이 원 로그에 있는지는 안 본다 (A 의 싼 고침 자리) | — |

### A (P2) — 위상 ↔ 체크포인트를 쓴 런 미결속

- 입력: 시험 하네스 본 흐름 (`qb_flow`) · 본 덱 = 실제 v3 D0.7 (루프 진입 E = 400,002) · 원 로그 = `qb_orig_log(E′)` 로 E′ ≠ E (원 런이 다른 step 에서 판정).
- 관측 (`probes_out.txt` P1):
  - E′ = 397,502 (원 판정 997,502 · 1,002,502): 도구 = `루프 진입 400002 · 위상 4998 → [run 2]` (판정 1,000,002) · **G0 · G1 · G2 · G3 전부 통과 · 시험 냄** (-T 없으면 본 제출까지 간다).  원 런과 판정이 2,500 step 어긋난다.
  - E′ = 400,001 (원 판정 1,000,001): G3 결손 (`원 로그에 있는 비교 줄이 시험에 없음: 1000001`) 으로 **우연히** 잡힘 — 원 판정 줄이 시험 창 (S0, S0 + TS] 안 · 1000 배수 아님일 때만 잡힌다.
- 왜 중요: 판정 (if) 은 물리를 안 바꿔 G1 · G2 · G3 (상태 · 5 % 압력) 가 위상 오류를 못 본다.  청구 ① ("원 덱이 그 step 부터 돌 순서 그대로") 의 유일한 근거가 "작업 폴더 `input_<C>.liggghts` 의 run 합 = 체크포인트를 쓴 런의 step 일정" 이라는 **확인 안 한 전제**다.  실제로 체크포인트를 쓴 것은 본 덱이 아니라 그 전 재개 덱 (job 335457 이 돈 덱 · 삽입 NP 1 → 정착 재개 → …) 이다.  시험은 원 로그를 늘 같은 E 로 만들어 (`qb_orig_log(400002, …)`) 이 어긋남을 한 번도 안 본다.
- 실제 D0.7: 335457 이 도구가 만든 재개 덱 (첫 긴 run 을 정착 끝 200,001 에 맞춘 꼴) 이면 E = 400,002 → 위상 4,998 = 같음 (추정).  **확인 한 줄** (ibb · 읽기만): 원 로그에 step **1,000,002** 의 CPU > 0 줄과 바로 뒤 `Loop time … for 5000 steps` 가 있으면 확정 (thermo 1000 에서 1000 배수 아닌 정규 줄 = run 끝 = 판정).
- 권고: 도구가 원 로그에서 S0 + r (있으면 S0 + r − N 도) 의 run 끝 줄 + `Loop time … for N steps` 를 요구 (없으면 위상 거부) — awk 몇 줄 · 합성 로그 시험에 E′ ≠ E 장면 둘 (위 P1) 을 거부 시험으로.

### B (P2) — "본 덱 자리" ≠ LIGGGHTS fix 칸 순서

LIGGGHTS (LAMMPS `Modify::add_fix`) — 같은 ID 다시 정의 = **같은 칸**에 바꿔 넣음 · `unfix` 뒤 `fix` = 끝에 붙임.  탐침 `slot_order()` 가 이 규칙으로 칸 순서를 셈 (`probes_out.txt` P2).

- P2a 실제 D0.7 꼴 (QB17 장면 · 시험 · G0–G3 통과):
  - 원 런 체크포인트 때 칸: `zwall_bot, integr, gravi, top_mesh, zwall_top, damp, move_press`
  - 도구 순서 고침 뒤: `zwall_bot, integr, top_mesh, zwall_top, gravi, damp, move_press`
  - dem_restart.py 그대로: `zwall_bot, integr, gravi, damp, top_mesh, zwall_top, move_press`
  → 고친 뒤도 원 칸 순서가 아니다 (gravi 가 판 메시 · 벽 **뒤**로 감 · 원 런은 앞).  이 덱의 gravity · viscous · wall/gran 은 다 post_force 에서 f 에 **더하기**만 (f 를 읽는 fix 없음) → 합산 순서만 다름 = roundoff.  ⇒ **청구 ② 는 실제 덱에서 성립** · 실제 D0.7 물리 계속은 roundoff 까지 같음.
- P2b 합성 반례 (본 덱 `fix gravi … 98.1` 다음 줄에 `fix fz g_se_ins setforce NULL NULL 0.0` 하나): 원 런 칸 = `… integr, gravi, fz, top_mesh …` (gravity 뒤 setforce → SE z 힘 0) · 도구 재개 덱 = `… integr, fz, top_mesh, zwall_top, gravi …` (setforce 뒤 gravity → SE 가 중력을 받음) → **물리 다름 · 정적 대조 통과 · G0–G3 통과 · 시험 냄**.
- P2c: 원 런 칸 순서 그대로 낸 재개 덱 (`integr, gravi 9.81, fz, 판 메시 …`) 도 도구가 P2b 의 틀린 순서로 바꾸고 통과 — 10-28 순서 규칙 (`setup_order` · 순서 보존 부분열) 이 LIGGGHTS 와 같은 순서를 **거부**하고 틀린 순서를 **요구**한다.  순서 고침은 그 규칙을 기계적으로 맞출 뿐.
- 왜 중요: 커밋 · 절차 문서의 "다시 정의한 fix gravi 9.81 = 본 덱 뒤 자리 (본 덱 자리)" 가 LIGGGHTS 실행 순서라는 뜻으로 읽힌다 — 사실이 아니다.  다시 정의된 비가환 fix (setforce · freeze · aveforce · f 를 읽는 fix …) 가 든 덱이면 roundoff 를 넘는 차이를 받아들인다.  (뿌리는 10-28 규칙 · Q3 (나) 가 그 규칙에 기대 새로 노출.)
- 권고: 문서 서술 한정 ("정적 대조 순서 규칙의 자리 · LIGGGHTS 칸 순서 아님 · 이 덱은 더하기형 fix 뿐이라 합산 순서만") + 다시 정의 · unfix 된 fix 가 있으면 그 style 이 더하기형 허용 목록 (gravity · viscous · wall/gran · nve/sphere …) 안일 때만 통과 · 아니면 닫힌 실패.  또는 순서를 LIGGGHTS 칸 규칙으로 계산.

### C (P3) — 청구 ③ 시험 공백

`mut_out.txt`: M3 (n < m 이면 처음 n 자리) · M7 (n > m 이면 남는 앞 칸도 음수 번호로 자리) = 둘 다 **52 PASS · 0 FAIL** (살아남음).  QB17 은 n = m = 2 (thermo 1000) 뿐.  실제 덱 영향 없음 (n < m 은 정적 대조가 두 자리 다 받고 끝 상태 같음 · n > m 은 정적 대조 단사 짝 맞추기가 거부).  권고: 재개 덱 thermo 1000 한 번 (본 덱 155 · 212) → 212 자리 시험 + 같은 fix 두 번 (본 덱 한 번) → 거부 시험.

### D (P3) — G3 한 방향

`comm -23 <원 로그> <시험>` = 원 로그 줄이 시험에 없을 때만 실패.  시험의 S0 + r run 끝 줄이 원 로그에 없는 경우 (P1 E′ = 397,502) 는 통과.  A 의 권고를 여기 넣으면 싸다.

## 닫힘 (확인함)

- 위상 산술: 체크포인트 2 step 앞 (4,998 · run 2) · 1 step 앞 · 1 step 뒤 (4,999) · 위상 0 거부 · 변수 run · run 꼬리 · 루프 몸 fix · else · 다른 jump · 루프 몸 변수 앞 정의 · restart 0 없음 (KG50-11) — QB1–QB6 이 막음 (재실행 52/52).
- 준비 run · 판정 · 건너뜀 변이 16 (run 3 · run 5000 · jump · label 빠짐 · 자리 · 조건 · 이름 …) 거부 — QB7.
- 체크포인트 전에 `unfix` 된 fix (ins_mix) 를 준비 구간에 넣음 → 순서 고침이 본 덱 자리로 옮겨도 정적 대조 거부 (재삽입 · 재개 덱에만) — P3 탐침.
- 변이 M1 (순서 고침 끔) · M2 (같은 명령 전부 마지막 자리) · M4 (순서 고침 짝 = 글자 같음만 · 판 메시 file 이름 규칙 끔) → QB17–19 · QB10 계열이 잡음.  M6 (같은 키 역순) = 같은 키가 생기지 않아 동등 변이.
- 옛 판 (`f37d5ee03`) QB 1/52 (QB8 = 예전 거부만) · 중간 판 (`066c6a0fc` · 순서 고침 전) 48/52 (QB17 · QB18 ×2 · QB19 = 순서 거부 · 순서 고침 줄 없음) → **옳은 이유로 실패** (청구 ④).
- 검사 ↔ 실행 덱: `--q3b-fix` 가 바꾼 같은 파일을 정적 대조 · 시험 자르기 · 본 제출이 씀 · CRLF 재개 덱 = 안 넣음.
- 재개 꼴의 LIGGGHTS 흐름 (jump SELF 되감기 · label 건너뜀 중 치환 안 함 · 판정 = run r 마지막 step 판 힘 · restart 다음 쓰기 = S0 다음 배수) — 원 루프와 같음 (판단 · LIGGGHTS 실행 확인 아님).

## 안 닫힘

- A (위상 ↔ 원 런 결속) · B (칸 순서 모형 · 비가환 fix) · C · D 시험 공백.
- 실제 `dem_restart.py` 산출 덱으로의 순서 고침 = 미확인 (리포에 없음 · 합성 r075 꼴만).
