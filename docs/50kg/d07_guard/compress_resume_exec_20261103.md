# D0.7-50 압축 체크포인트 재개 — 실행 절차 (Codex 11-03 조건부 GO §6 반영)

- 근거: Codex 판정 `docs/reviews/codex_kg50_d07_q3b_review_20261103/codex_review_kg50_d07_compress_resume_20261103.md` — **한 건 조건부 GO** · 요청서 §4-6 을 그대로 실행하는 것은 HOLD (`KG50Q-01` (Codex 표기 KG50Q3B-01) P2 = 영수증 첫 대조가 본 제출 뒤로 밀림).  이 문서가 §4-6 을 대신한다.
- 대상: `kg50_d07_b50.run335457` 의 `restart_compress_1000000.bin` · NP 56 · r56 · `-t 2000` · 도구 `66006239…` · 헬퍼 `d6e590a1…` · 승인값 = `docs/50kg/d07_guard/t_test_20261103/README.md`.
- 순서 (판정문 §6): **새 시험이 도는 동안 · 본 제출 전에** 영수증 전체 sha256 + 시험 신원 (영수증 3 · 5 행 · lmp) 을 대조한다 → 본 job 시작 뒤 본 신원 (영수증 1 · 5 행 · lmp).  불일치 · 확인 지연 · 결손 (빈 · 잘린 · 여러 신원 줄) = 중단 블록 → `sacct` 로 **최종 종료까지** 확인.  취소 명령 · "로그에 아직 없음" 은 종료 증거가 아니다.
- 지키지 않는 것: 그 뒤 런 전체 (물리 · 완주 · 시간) · 결과 해석 (11-01 §6-4 그대로).

## 창 A — 호출 전 확인 · 본 제출 호출

```bash
squeue -u $USER                                   # kg50_d07_b50 잡 없음 · 다른 호출 없음
sha256sum ~/dem_test/scripts/resume_ckpt.sh ~/dem_test/dem_restart.py | cut -c1-64   # 66006239… · d6e590a1…
ls -d ~/dem_test/kg50_d07_b50.run335457 ~/dem_test/kg50_d07_b50   # 원 폴더 · 직전 -T 폴더 (본 호출이 prev_<시각> 으로 옮겨 보존)
cd ~/dem_test/scripts && nohup bash resume_ckpt.sh -n 56 -s run335457 -r /home/yonghoon/dem_test -x r56 -t 2000 \
  -A 66006239ec58043f963fa885f9db545c63614d279bfb6cac1665a2eae9884c6d \
  -H d6e590a18849d10c70dc831d5e8bebabf3a5163d502d5968db9688a70a29d7c8 \
  kg50_d07_b50 > ~/d07_cmp_main.log 2>&1 &
```

## 창 B — 곧바로 (새 시험이 도는 동안 · 약 4 분 안 · 읽기만)

```bash
L=~/dem_test; W=$L/kg50_d07_b50; LOG=~/d07_cmp_main.log
OKR=cff47c44385a95529ed2c6e97438985a56e6e2ede194e05f7541c14788570176
until grep -q "▶ 시험 job\|⛔" $LOG; do sleep 5; done
grep -m1 "도구 신원" $LOG | grep -o "sha256 [0-9a-f]*\|attempt_r56_[0-9_]*"   # sha256 66006239… · sha256 d6e590a1… · 시도
grep "▶ 시험 job\|⛔" $LOG
A=$(grep -m1 "도구 신원" $LOG | grep -o "attempt_r56_[0-9_]*"); J=$(cat $W/$A/job_t.txt); echo "시도 $A · 시험 job $J"
R=$(sha256sum < $W/$A/main_inputs.sha256 | cut -c1-64); [ "$R" = "$OKR" ] && echo "✅ 영수증 = 승인값" || echo "⛔ 영수증 다름 $R → 중단 블록"
O=$L/logs/output_kg50_d07_b50_r56t_$J.out
until grep -q LMP_IDENTITY $O 2>/dev/null; do sleep 5; done
echo "시험 신원 줄 수 $(grep -c LMP_IDENTITY $O) (= 1)"; grep -h LMP_IDENTITY $O | tr ' ' '\n' | grep "sha256="
#   = ee2d7726… (lmp) · 4110ee76… (시험 덱 = 영수증 3 행) · 164824ea… (체크포인트 = 5 행)
```

- 위 셋 (영수증 · 신원 줄 수 1 · sha256 셋) 이 **시험이 끝나기 전에** 다 맞으면 기다린다 (도구가 G0–G3 뒤 본 제출).  하나라도 다르거나 · 시험이 끝날 때까지 확인을 못 했으면 → 중단 블록.

## 창 B — 도구가 끝난 뒤 (본 job 신원 · 읽기만)

```bash
while pgrep -f "resume_ckpt.sh -n 56 -s run335457" >/dev/null; do sleep 10; done
cat $W/$A/result.txt | tail -3; grep "G0\|G1\|G2\|G3\|본 제출 job\|⛔" $LOG | cut -c1-200 | tail -10
JM=$(cat $W/$A/main_job.txt); OM=$L/logs/output_kg50_d07_b50_r56_$JM.out; echo "본 job $JM"
until grep -q LMP_IDENTITY $OM 2>/dev/null; do sleep 10; done
echo "본 신원 줄 수 $(grep -c LMP_IDENTITY $OM) (= 1)"; grep -h LMP_IDENTITY $OM | tr ' ' '\n' | grep "sha256="
#   = ee2d7726… (lmp) · 12873efc… (본 덱 = 영수증 1 행) · 164824ea… (체크포인트 = 5 행)
squeue -j $JM; sacct -j $JM -X -o JobID,State,ExitCode,Elapsed
```

## 중단 블록 (불일치 · 확인 지연 · 결손 때만)

```bash
pkill -f "resume_ckpt.sh -n 56 -s run335457"      # 도구가 본 제출하지 않게 먼저
scancel $J
[ -s $W/$A/main_job.txt ] && scancel $(cat $W/$A/main_job.txt)
sleep 60; sacct -j $J -X -o JobID,State,ExitCode
[ -s $W/$A/main_job.txt ] && sacct -j $(cat $W/$A/main_job.txt) -X -o JobID,State,ExitCode
squeue -u $USER                                     # 그 시도의 시험 · 본 job 이 다 끝난 상태 (CANCELLED · COMPLETED · FAILED) 일 때까지 다시 본다
```

- 중단했으면 화면 전부를 Claude 에게 · 다시 호출은 원인 확인 뒤 (같은 승인값 · 새 시험).

## TIMEOUT 뒤 (판정문 §7 · 조건부 절차 범위)

- 매번 새 source job 종료 · 폴더 · 로그 · 덱 보존 · 새 체크포인트 (step · 경로 · sha256) 고정 → 같은 도구 · 헬퍼 · NP 56 · `-t 2000` 으로 **새 `-T`** → 원 로그의 S0 + 2 판정 자리 확인 → 그 새 영수증으로 위 창 B 대조.  `cff47c44…` · `164824ea…` 는 이번 체크포인트 값 — 다음 체크포인트에 그대로 쓰지 않는다.
- 짧은 재확인 대상 (판정문 §7): S0 · S0 + 1 에서 멈춰 S0 + 2 원 로그 없음 · 첫 판정에서 목표 도달로 `-t 2000` 시험 조기 quit (`-t` 를 줄여 통과시키지 않는다) · 같은 S0 재사용 (직전 재개의 첫 판정 = `Loop … for 2 steps` 일 수 있음) · 덱 · fix · 규약 · NP · 신원 · 도구가 바뀜 · 원자료를 잃음.
- 이완 중 TIMEOUT = 마지막 압축 체크포인트부터 압축 말기 + 이완을 다시 (이완 상태를 잇지 않음).
