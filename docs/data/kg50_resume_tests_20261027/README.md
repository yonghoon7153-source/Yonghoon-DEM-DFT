# 50kg D2-50 재개 시험 (`-T`) 기록 — ibb · 10-27 밤 (KST)

- 무엇: v3 50×50 `kg50_d2_b50` 삽입 런의 settling 체크포인트 (`restart_kg50_d2_b50/restart_settling_20001.bin` · step 20001) 를 `scripts/resume_ckpt.sh -T` (시험만 · 첫 긴 run 2,000 step · NP 4) 로 재개해 본 기록.  1저자가 ibb 에서 돌린 보고 원본 두 개 (`~/dem_test/resume_r4_<시각>.md` · 1저자 10-27 밤 업로드) 를 바이트 그대로 둔다.
- 덱 = `docs/data/kg50_decks_20261027_v3_b50/kg50_d2_b50/` · 절차 = `docs/resume_ckpt_procedure_20260927.md` 끝 절 (10-26 · 10-27 · 10-27 개정 2).

| 파일 | sha256 | 회차 · 도구 판 | 무엇이 적혔나 |
|---|---|---|---|
| `resume_r4_1027_2110.md` | `d77553af4ed56bd37e51e64ea608454322d8331979ae1dc7de08bbbd4b7dd2d7` | 둘째 시도 · 도구 = ibb 사본 sha256 `b98af8ac…` (1저자 ibb 화면 · 10-27 KG50-16 `-c` 판) | 머리 두 줄뿐 — 정적 대조가 재개 덱을 거부한 회차 (`남은 step 다름` · 재개 덱 `run 179999` ↔ 본 덱 그 run 끝 200001 − 체크포인트 20001 = 180000 · 원장 `KG50-17`).  거부 줄은 nohup 화면 기록에만 있고 보고에는 케이스 절이 생기지 않는다 · 시험 미제출 · 원본 그대로 |
| `resume_r4_1027_2230.md` | `342e4fe1f0dbc224352e8390ef19aa67cdba28fb5b50c593452b6373806c6bcf` | 셋째 시도 · 도구 = KG50-17 고침 판 (보고의 *"첫 긴 run (10-27 · 1저자 Q1 (가))"* 줄은 그 판에만 있다 · 1저자 연구실 PC 사본 sha256 `65f73b37…` 를 ibb 로 보냄 · ibb 사본 sha256 은 기록 없음) | 첫 긴 run 고침 `[run 179999] → [run 180000]` (원 줄 157 · 다시 대조 통과) · 정적 대조 통과 (문제 0) · 시험 job 327010 · **G0** COMPLETED · ExitCode 0:0 · 마지막 step 22001 = 기대 22001 · Loop time 있음 · **G1** step 20001 KinEng 2.3980032 = 같음 · **G2** 체크포인트 step 덤프 없음 → G1 KE 일치로 대신 · **G3** step 21000 KinEng 2.5527533 = 같음 · `-T` 라 본 제출 안 함 |

- 받지 못한 것: `plan_r4.txt` · `fixrun_r4.txt` · `deckcheck_r4.txt` · nohup 화면 기록 (`resume_d2_b50_T.log`) — 핵심 줄은 보고 안에 있다.
- 이 기록이 말하는 것: settling 체크포인트 재개 길 한 건이 실제 ibb SLURM 에서 G0–G3 를 통과했다 (시험만).  말하지 않는 것: 본 제출 · 압축 · 물리값 · after_settling · compress 재개 길 (이 기록과 무관 — 그 길의 두 결함 `KG50-18` · `KG50-19` 는 10-28 합성 시험으로 고침 · 실제 ibb 확인 전).
- 등록 순서 (1저자 10-27 밤 *"50kg 권고대로 해"* = Q5 등록 초안 `docs/50kg/kg50_q5_dt_damping_registration_draft_20261027.md` Q1–Q12 권고대로): D0.7-50 본 제출 = 재개 도구 Codex 재확인 GO + Q5 등록 뒤 (본 런이 정착 끝 체크포인트를 쓰면 멈추고 Q5 가지) · D1-50 = 정착 끝에서 Q5 결과를 기다림 (Q10) · D2-50 = 그대로 진행해도 됨 (Q10 · 싸다 · 버려도 하루 안팎).
- 이 기록 뒤 도구가 바뀌었다 (10-28 · KG50-18 · 19 · 새 sha256 `e59c43e6…`).  고친 판의 settling 경로 출력은 고치기 전 판과 바이트가 같다 (합성 45 장면 · `scripts/test_resume_ckpt.py --compare-old`) → 이 기록과 같은 길은 새 판에서도 같은 줄이 나올 것으로 본다 (추정 · 실제 ibb 재실행 아님).
