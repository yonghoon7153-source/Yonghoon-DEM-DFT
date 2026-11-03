# Codex 짧은 확인 요청 — D0.7-50 압축 체크포인트 재개 한 건 (Q3 (나) · KG50R-01 최소 해결) (2026-11-03)

리뷰 핀 = `PIN.txt` (이 요청서를 넣은 커밋).  ZIP `repo/` = 그 커밋의 파일 사본.  1저자 11-03 — *"넘어가기전에 여기서 d0.7 이거 다시 시작하고 넘어가자"*.

## 0. 이번에 닫는 것 / 닫지 않는 것

- **닫는 것 (요청)**: D0.7-50 (`kg50_d07_b50`) **한 건** — 멈춘 본 런 (job 335457) 의 압축 체크포인트 `restart_compress_1000000.bin` (step 1,000,000) 에서 Q3 (나) 재개 덱으로 **본 제출해도 되는가** (조건 = §4).  11-01 초안 2 판정 §6 이 *"압축 체크포인트 재개를 승인하지 않는다"* 고 적은 바로 그 자리다.
- **닫지 않는 것**: 재개 도구 일반 종결 (KG50R-03 · KG50P-01 · 03 · PAI-01–09 · 아래 사전 공격 A–D 의 도구 일반 고침) · 무인 지킴이 보장 · dt · 감쇠 물리 자격화 · 입도 효과 · 접촉 · 수송 · 응력 판정 · D0.7 결과 해석 · 11-01 §6 조건 4 (결과 반입 전 러너 원자 재고 · 다중 프레임 · 기록 대조 결손 · 소비 경계) — 결과 반입 때 따로.

## 1. 왜

- 11-01 §6 한 건 = 정착 끝 (step 200,001) → 압축 · 이완 (본 job 335457).  11-02 저녁 1저자가 코어를 D2 영률 두 판으로 돌리려고 취소 (*"D0.7은 잠깐 스탑하고"*) — 원 로그 끝 step 1,055,002 · 마지막 압축 체크포인트 1,000,000 (restart 간격 200,000).
- 정착 끝 (200,001) 부터 다시 돌리면 체크포인트까지의 압축 약 80 만 step (시간당 약 2 만 step → 약 40 h · 추정) 을 다시 돌고, 남은 압축 · 이완이 한 job 시간 한도 안에 끝난다는 보장이 없다 (추정).  취소 때 (11-02) 기록은 *"압축 체크포인트 재개 거부 = 10-28 Q3 (가) → 다시 돌릴 때 정착 끝부터"* 였다.
- ⇒ 1저자 11-02 Q3 (나) = 압축 루프 체크포인트 재개.  구현 = 10-28 판정문 KG50R-01 **최소 해결 그대로** (첫 잔여 step → 압력 판정 → 필요하면 이후 5000-step 반복 · 루프 몸 run 을 2 로 바꾸는 것은 오답 · 위상을 못 정하면 거부).

## 2. 도구

- `scripts/resume_ckpt.sh` sha256 `66006239ec58043f963fa885f9db545c63614d279bfb6cac1665a2eae9884c6d` (개정 5 = Q3 (나) · 개정 5b = 준비 구간 순서 고침 — 11-02 ibb 실제 `-T` 가 dem_restart.py 산출 순서 때문에 시험 전 거부 → 1저자 = 순서 규칙은 풀지 않고 도구 쪽 고침) · 헬퍼 `dem_restart.py` sha256 `d6e590a18849d10c70dc831d5e8bebabf3a5163d502d5968db9688a70a29d7c8` (ibb · 리포에 없음).
- 정본 서술 = `docs/resume_ckpt_procedure_20260927.md` *개정 5* · *개정 5b* 절 (루프 위상 규칙 · 재개 덱 · 시험 덱 · G0–G3 · 거부 조건 · 한계).
- 시험 = `scripts/test_resume_ckpt.py` 485 개 — 고친 판 485/485 (Python 3.11.17 + mawk 1.3.4 · Python 3.8.20 + mawk 1.3.4) · 시험 먼저 커밋의 시험으로 고치기 전 판 (`319e5e7b…`) `--only QB` = 48 PASS · 4 FAIL (QB17 · QB18 ×2 · QB19 = 순서 규칙 거부 · QB17 = ibb 실제 거부 문구와 같은 줄) · 옛 판 대조 (`--compare-old`) = 둘 다 정상인 장면 58 다름 0 (settling · after_settling · write_restart · `-C` 길 그대로).
- 오늘 판 확인: 11-03 전체 게이트 (`50b5fb4b7` · 도구 바이트 같음) 의 `resume_ckpt (재개 도구 · 가짜 SLURM)` 단계 통과 · `--only QB` 52/52 (11-03 다시 돌림).
- 재현: `cd repo && python3 scripts/test_resume_ckpt.py` (전체) · `--only QB` (압축 루프 묶음).

## 3. 증거

### 3-1. 위상 — 실제 원 로그 (1저자 ibb · 읽기만 · 11-03 새벽 · 사전 공격 A 의 확인 한 줄)

```
/home/yonghoon/dem_test/kg50_d07_b50.run335457/log.liggghts:4884: 1000002   488285  3.3622402e-08      868.48924  0.00011997834
/home/yonghoon/dem_test/kg50_d07_b50.run335457/log.liggghts-4885-Loop time of 868.491 on 56 procs for 5000 steps with 488285 atoms, finish time Mon Nov  2 14:29:16 2026
--
/home/yonghoon/dem_test/kg50_d07_b50.run335457/log.liggghts:4915: 1000002   488285  3.3622402e-08              0  0.00011997834
```

- step 1,000,002 = CPU > 0 정규 줄 바로 뒤 `Loop time … for 5000 steps` = 원 런의 5000-step 루프 run 끝 = 압력 판정 자리.  4915 줄 = 다음 run 의 setup 줄 (CPU 0).
- 도구 위상 = 루프 진입 E = 400,002 (본 덱 루프 앞 run 합) · (1,000,000 − 400,002) mod 5,000 = 4,998 → 남은 r = 2 → 다음 판정 1,000,002 = **원 로그와 같다** (이 한 건).

### 3-2. 실제 `-T` 시험 (ibb · job 337078 · 11-03 새벽)

- 명령: `cd ~/dem_test/scripts && nohup bash resume_ckpt.sh -n 56 -s run335457 -r /home/yonghoon/dem_test -x r56 -t 2000 -T kg50_d07_b50 > ~/d07_cmp_T.log 2>&1`
- 결과 = **G0 · G1 · G2 · G3 통과** · 본 제출 안 함 · 시도 `attempt_r56_1103_014321_1895853` · job 337078 = COMPLETED · ExitCode 0:0 · 00:03:53 · 끝 step 1,002,000 (= 1,000,000 + 준비 run 2 + 루프 run 1,998) — 원문 `docs/50kg/d07_guard/t_test_20261103/t_output_grep.txt` · 정리 `docs/50kg/d07_guard/t_test_20261103/README.md`.
  - G0: 마지막 thermo 줄 유한 · `Loop time … for 1998 steps` = 시험 마지막 run · 잡 안 덱 신원 같음 · 판정 (1,000,002) 에서 목표에 닿았다면 시험 덱 `quit` 으로 종료 코드 ≠ 0 → 0:0 = 목표 아래 · 루프 계속.
  - G1: step 1,000,000 setup 줄 KE `3.3619779e-08` = 원 로그 · G2: `atom_1000000.liggghts` · `mesh_1000000.stl` 같음.
  - G3: step 1,000,002 압력 `0.00011997834` → `0.00011998104` (상대차 2.25 × 10⁻⁵) · KE `3.3622402e-08` → `3.364381e-08` (6.37 × 10⁻⁴).
- 승인값 (영수증 `main_inputs.sha256` 파일 sha256 `cff47c44385a95529ed2c6e97438985a56e6e2ede194e05f7541c14788570176` — 붙여 넣은 다섯 줄로 다시 만든 값과 같음): 본 덱 `12873efc…` · 본 러너 `f20d6854…` · 시험 덱 `4110ee76…` · 시험 러너 `97e4df27…` · 체크포인트 `164824ea603741e436361589b48ee9d9f0fb16bf6bb12b92a630552bc3799de0` · lmp_mpi `ee2d7726…` (10-30 · 10-31 과 같음).  도구 신원 줄은 이번 grep 에 없다 — 본 제출의 `-A` · `-H` 가 같은 값을 강제 (`scripts/resume_ckpt.sh` 1924–1928 줄).

### 3-3. 사전 공격 리뷰 (`docs/reviews/kg50_q3b_preattack_20261103/PREATTACK.md` · 독립 리뷰어 · diff · 실제 덱 · 시험 하네스만)

| # | 등급 | 내용 | 이 한 건 | 처분 |
|---|---|---|---|---|
| A | P2 | 루프 위상을 본 덱 run 합으로만 정함 (원 로그 판정 step 과 미결속 · G0–G3 는 위상에 눈멂) | §3-1 원 로그 줄로 확인 = 같음 | 도구 일반 고침 = 닫지 않음 (권고 = 원 로그에서 S0 + r run 끝 줄 + `Loop time … for N steps` 요구) |
| B | P2 | 순서 고침의 "본 덱 자리" = 마지막 줄 자리 ↔ LIGGGHTS 는 다시 정의한 fix 를 첫 정의 칸에 둠 | 본 덱 fix 전수 (체크포인트 앞) = property/global 9 · wall/gran 2 (바닥 · 판) · particletemplate 3 · particledistribution · insert/pack (체크포인트 전 unfix) · nve/sphere · gravity · viscous · mesh/surface/stress · move/mesh — 입자 힘을 바꾸는 것은 gravity · viscous · wall/gran 뿐 = 모두 post_force 더하기 (setforce · freeze · aveforce 같은 비가환 fix 없음) → 자리 차이 = 합산 순서 (반올림) | 도구 문서 서술 한정 · 일반 고침 (더하기형 허용 목록 · LIGGGHTS 칸 규칙) = 닫지 않음 |
| C | P3 | "같은 명령 n 번 → 마지막 n 자리" 시험 없음 | 영향 없음 (n = m = 2 · thermo) | 닫지 않음 |
| D | P3 | G3 한 방향 (시험 끝 줄이 원 로그에 있는지 안 봄) | 영향 없음 (§3-1 이 같은 것을 본다) | 닫지 않음 |

### 3-4. 남은 압축 어림 (추정 · TIMEOUT 계획의 근거)

- 1,000,002 판정 압력 `0.00012` (덱 단위 · 목표 `target_press` 0.30 = 300 MPa) = 목표의 0.04 % — 판이 침대에 막 닿은 자리.  덱 산술과 맞다: 정착 끝 판 높이 − 침대 꼭대기 = 0.142972 − 0.136972 = 0.006 m · 판 속도 0.01 m/s × dt 1.0e-6 s = 1e-8 m/step → 600,000 step = 루프 진입 400,002 + 600,000.
- 같은 덱 꼴 (정착 200,000 · 안정화 200,000 · 판 속도 0.01 · 목표 0.30 · 이완 100,000) 의 D2 영률 판 (E05) 이완 끝 = step 4,485,002 → D0.7 도 비슷하면 남은 약 3.4 M step ≈ 170 h (시간당 약 2 만 step) > 러너 시간 한도 (리포 v3 러너 `--time=5-00:00:00` = 120 h · ibb 헬퍼 러너 값은 이 화면에 없음 · 도구가 그 값을 그대로 쓴다) → **TIMEOUT 한 번 뒤 다시 재개가 필요할 가능성이 크다** (추정 · 침대 높이 · 입도가 달라 끝 step 은 모른다).  ⇒ §4-5 · Q4.

## 4. 본 제출 조건 (11-01 §6 의 꼴 · 이 한 건)

1. NP 56 · 접미사 r56 · 멈춘 폴더 `kg50_d07_b50.run335457` (손대지 않음) · 체크포인트 `restart_compress_1000000.bin` · 도구 `66006239…` (`-A`) · 헬퍼 `d6e590a1…` (`-H`) · 같은 작업 폴더 동시 호출 없음 · 시간 한도 = 헬퍼 러너 값 그대로 (도구가 바꾸지 않음).
2. 본 제출 = `-T` 를 뺀 같은 명령 + 승인값 (도구가 새 시험 → G0–G3 → 통과일 때만 본 제출) · **수동 확인** (지킴이 v3 는 만들지 않는다 — 11-01 판정의 GO 근거 = 수동 확인 조건 · 지킴이 v2 단독 보장은 HOLD): 본 호출의 새 시도 `main_inputs.sha256` 파일 sha256 = `-T` 영수증 `cff47c44…` (다섯 줄 전부 — 본 덱 · 본 러너 · 시험 덱 · 시험 러너 · 체크포인트 · 10-31 지킴이 v2 의 OKR 대조와 같은 꼴) · 본 job `LMP_IDENTITY` 세 칸 (lmp `ee2d7726…` · 본 덱 `12873efc…` · 체크포인트 `164824ea…`) · 다르면 본 job `scancel` 뒤 `sacct` 로 종료까지 사람이 확인 (취소 호출만으로 차단 완료라 하지 않음).
3. 이후 = 읽기 전용 watch (`squeue` · `sacct` · 출력 끝 줄) · 5 분 RUNNING 을 완주 · 물리 적합성으로 읽지 않는다.
4. 끝 압력 · 낙폭 · 정의가 분리된 R5 / drag 를 함께 기록 · 입도 · 접촉 · 수송 · 응력 판정 보류 그대로 (11-01 §6-4).
5. TIMEOUT · 미완주: 자동 재제출 없음 · 본 런 폴더는 이름을 바꿔 보존 (`kg50_d07_b50.run<job>`) · 멈춘 폴더 `kg50_d07_b50.run335457` 그대로 · 다시 재개 = 같은 도구 · 같은 Q3 (나) 길로 그 런의 최신 압축 체크포인트 (restart 간격 200,000 → 위상 늘 4,998) 에서 새 `-T` (G0–G3) + §3-1 꼴 원 로그 확인 한 줄 → 본 제출 (아래 Q4).  이완 구간은 체크포인트가 없다 (루프 뒤 `restart 0` · KG50-11) → 이완 중 TIMEOUT 이면 마지막 압축 체크포인트부터.

### 4-6. GO 뒤 명령 (그대로 · §4-2 수동 확인 포함)

```bash
# ① 본 제출 — 도구가 새 시험 → G0–G3 → 통과일 때만 본 job (-T 를 뺀 같은 명령 + 승인값)
cd ~/dem_test/scripts && nohup bash resume_ckpt.sh -n 56 -s run335457 -r /home/yonghoon/dem_test -x r56 -t 2000 \
  -A 66006239ec58043f963fa885f9db545c63614d279bfb6cac1665a2eae9884c6d \
  -H d6e590a18849d10c70dc831d5e8bebabf3a5163d502d5968db9688a70a29d7c8 \
  kg50_d07_b50 > ~/d07_cmp_main.log 2>&1 &

# ② ~/d07_cmp_main.log 에 '✅ 본 제출 job' 줄이 나온 뒤 (읽기만) — 새 시도 영수증 = -T 영수증 · 본 job 신원 세 칸
grep "본 제출 job\|⛔" ~/d07_cmp_main.log
L=~/dem_test; W=$L/kg50_d07_b50
A=$(grep -o "attempt_r56_[0-9_]*" ~/d07_cmp_main.log | head -1); echo $A
sha256sum $W/$A/main_inputs.sha256 | cut -c1-64     # = cff47c44385a95529ed2c6e97438985a56e6e2ede194e05f7541c14788570176
JM=$(cat $W/$A/main_job.txt); echo "본 job $JM"
grep -h "LMP_IDENTITY" $L/logs/output_kg50_d07_b50_r56_$JM.out | tr ' ' '\n' | grep "sha256="   # = ee2d7726… · 12873efc… · 164824ea…
sacct -j $JM -X -o JobID,State,ExitCode,Elapsed
```

- 영수증 · 신원이 하나라도 다르면 본 job `scancel <job>` → `sacct -j <job> -X -o JobID,State,ExitCode` 로 종료 확인까지 사람이 본다.  같으면 그 뒤는 읽기 전용 watch.
- 본 호출은 작업 폴더 (이 `-T` 시험 폴더) 를 `kg50_d07_b50.prev_<시각>` 로 옮겨 보존한다 (`scripts/resume_ckpt.sh` 2216–2220 줄) → `-T` 영수증 원본 = 그 안 `attempt_r56_1103_014321_1895853/main_inputs.sha256`.

## 5. 질문

- **Q1.** §4 조건으로 이 한 건 본 제출 GO 인가?
- **Q2.** 지킴이 v3 없이 §4-2 수동 확인으로 충분한가?
- **Q3.** 사전 공격 A–D 처분 (이 한 건 = §3-1 · 덱 확인 · 도구 일반 = 닫지 않음) 을 수용하는가?
- **Q4.** §4-5 (TIMEOUT 뒤 같은 런의 더 늦은 압축 체크포인트 재개 · 새 `-T` G0–G3 + 원 로그 확인 한 줄) 를 이 GO 범위에 넣어도 되는가, 아니면 그때 다시 짧은 확인인가?

## 6. ZIP

`repo/` = `scripts/resume_ckpt.sh` · `scripts/test_resume_ckpt.py` · `docs/resume_ckpt_procedure_20260927.md` · 시험이 쓰는 덱 · 로그 (`docs/data/kg50_decks_20261026_v2/kg50_d07_b40/` · `docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50/` · `docs/data/pure_se_r075_20260927/` · `docs/data/kg50_resume_tests_20261027/d2_main_1028_0942/` · `docs/reviews/codex_kg50_resume_recheck_20261028/`) · `docs/reviews/kg50_q3b_preattack_20261103/` · `docs/50kg/d07_guard/` (README · `t_test_20261031/` · `t_test_20261103/`) · 11-01 판정문 (`docs/reviews/codex_kg50_y4_draft2_review_20261101/codex_review_kg50_y4_draft2_20261101.md`) · `PIN.txt` · `MANIFEST.sha256`.
