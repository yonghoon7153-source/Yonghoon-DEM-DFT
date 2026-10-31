# LIGGGHTS 체크포인트 재개 기록 — r56 (56 MPI) · 2026-10-31 21:58
명령: bash resume_ckpt.sh -n 56 -s main1031 -r /home/yonghoon/dem_test -x r56 -t 2000 -T kg50_d07_b50
- 도구 신원 (10-28 Q4 · Codex Q7 · KG50R): resume_ckpt.sh sha256 2dc7f693263708d7788ab721386182c6109a8f9278797ecc43f5165d6715f1e8 (/home/yonghoon/dem_test/scripts/resume_ckpt.sh) · dem_restart.py sha256 d6e590a18849d10c70dc831d5e8bebabf3a5163d502d5968db9688a70a29d7c8 (/home/yonghoon/dem_test/dem_restart.py) · 승인 -A 없음 · -H 없음 (없음 · 다름)
- 시도 (10-28 KG50R-04): attempt_r56_1031_215830_2483798 — 이번 호출이 낸 시험만 본 제출 대상 (작업 폴더의 옛 job · mode 파일은 읽지 않는다)

## kg50_d07_b50
- 시도 (10-28 KG50R-04): attempt_r56_1031_215830_2483798 · 이번 호출이 낸 시험 job 335411 만 승격 대상 (기록 /home/yonghoon/dem_test/kg50_d07_b50/attempt_r56_1031_215830_2483798)
- 멈춘 폴더: kg50_d07_b50.main1031 (손대지 않음) · 멈춘 곳 ====== PHASE 2: STABILIZE ======
- 작업 폴더: /home/yonghoon/dem_test/kg50_d07_b50 (= 멈춘 폴더 cp -a) · 원 로그 → log.liggghts.main1031 · 체크포인트 뒤 덤프 → old_post_after200001_main1031/
- 재개: after_settling 체크포인트 `read_restart restart_kg50_d07_b50/restart_after_settling.bin` (step 200001) · 덱 input_kg50_d07_b50_r56.liggghts · 러너 run_kg50_d07_b50_r56.sh (#SBATCH -n 56 · mpirun --oversubscribe --bind-to none -np 56)
- 러너 (10-30 KG50R-F02 · 1저자 Q2): 헬퍼 러너 엄격 대조 통과 (10-30 KG50R-F02) — #SBATCH 6 · 환경 줄 6 · cd 실제 경로 = 작업 폴더 /lustre/home/yonghoon/dem_test/kg50_d07_b50 → 본 · 시험 러너를 도구 틀로 씀 (cd "작업 폴더 실제 경로" || exit 1 · -in "검사한 덱 절대 경로" · 잡 시작 때 덱 · 체크포인트 sha256 대조 · command mpirun 한 줄 · LMP_IDENTITY 줄 = 시험 로그에서 G0 관문) · 헬퍼 러너 원본 = attempt_r56_1031_215830_2483798/helper_run_kg50_d07_b50_r56.sh.orig · 실행 입력 영수증 attempt_r56_1031_215830_2483798/main_inputs.sha256 (다섯)
- 템플릿 재선언: pts1 pts2 pts3 pdd_mix (원 덱 그대로 · 삽입 fix 는 없음)
- 첫 긴 run (10-27 · 1저자 Q1 (가)): 첫 긴 run 고칠 것 없음 (정적 대조 통과) (fixrun_r56.txt)
- 재개 덱 정적 대조: 통과 (문제 0) (deckcheck_r56.txt)
- 시험: job 335411 · input_kg50_d07_b50_r56t.liggghts · output_kg50_d07_b50_r56t_335411.out · ERROR 0
- 시험 기대 끝 step (10-28 · KG50-18): S0 200001 + 시험 덱 read_restart 뒤 run 합 2001 ([run 1] [run 2000]) = 202002
- G0 시험 정상 종료: 통과 — 상태 COMPLETED · ExitCode 0:0 · 마지막 step 202002 (기대 202002) · Loop time 끝 step 뒤에 있음 · 조회 실패 0 번 · 끝 상태 얻음
- G0 마지막 줄 · Loop (10-28 KG50R-07): 마지막 thermo 줄 = 최신 머리 아래 · 칸 수 같음 · 모든 칸 유한 수 (step 202002 · 줄 235) · 'Loop time … for 2000 steps' ↔ 시험 마지막 run 2000 — 같음
- G0 잡 안 덱 신원 (10-30 KG50R-F02 · 관문): 통과 — 같음 (덱 /lustre/home/yonghoon/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56t.liggghts sha256 985ff18bd76e075019f895f7a79ecf1a76df077ea637912f8a945dc7bd93898c · 체크포인트 /lustre/home/yonghoon/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_after_settling.bin sha256 45a838c18d19e3c1399a97f5948d52ad0995490f6a55040e6a6ffec8fecd2d70 = 기록만 · lmp_mpi = 기록만)
    신원 줄 (10-30 KG50R-F02): LMP_IDENTITY (10-30 KG50R-F02): lmp_mpi=/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi sha256=ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f deck=/lustre/home/yonghoon/dem_test/kg50_d07_b50/input_kg50_d07_b50_r56t.liggghts sha256=985ff18bd76e075019f895f7a79ecf1a76df077ea637912f8a945dc7bd93898c checkpoint=/lustre/home/yonghoon/dem_test/kg50_d07_b50/restart_kg50_d07_b50/restart_after_settling.bin sha256=45a838c18d19e3c1399a97f5948d52ad0995490f6a55040e6a6ffec8fecd2d70
- G1 재개 첫 thermo (step 200001, setup 줄, CPU·압력 열 제외, 1e-6): 통과
    원 로그 : Step=200001 Atoms=488285 zmax=0.13697248
    재개    : Step=200001 Atoms=488285 zmax=0.13697248
- G2 체크포인트 상태 덤프 대조: 통과 —판 높이 같음 (====== PLATE HEIGHT: 0.142972437242453 ======)
- G3 원 로그 비교 구간 (step - 부터, 느슨한 확인): 원 로그에 비교 구간 (200001, 202002] 정규 줄 없음 → 생략
    원 로그 :
    재개    :
- 🧪 시험만 (-T) — G0–G3 통과 · 본 제출 안 함
- 본 제출 명령 (10-28 Q4 · KG50R · -T 를 뺀 같은 명령 + 승인값 · G0–G3 통과 케이스만 · 새 시험부터 다시): `bash /home/yonghoon/dem_test/scripts/resume_ckpt.sh -n 56 -s main1031 -r /home/yonghoon/dem_test -x r56 -t 2000 -A 2dc7f693263708d7788ab721386182c6109a8f9278797ecc43f5165d6715f1e8 -H d6e590a18849d10c70dc831d5e8bebabf3a5163d502d5968db9688a70a29d7c8 kg50_d07_b50`
