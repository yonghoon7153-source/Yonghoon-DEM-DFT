# U2 — 언로딩 키트 ULPR-01–04 수정 독립 재확인 (10-21) · 탐침 · 결과 · 재실행 명령

리포에 쓰지 않는다 (작업 트리 = U2 격리 작업 트리 · `bbc2adefe` · 바뀐 파일 0).  실행 = scratch 거울 사본 (`git archive`).

```bash
U=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_unload/u2
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/heavy.sh
cd $U
# 거울 (키트 + 키트가 리포에서 읽는 파일)
bash mk_mirror.sh bbc2adefe m_fix ; bash mk_mirror.sh 286a8d562 m_base ; bash mk_mirror.sh f1b911f76 m_tf
bash mk_mirror.sh 55fff3eb1 m_u01 ; bash mk_mirror.sh 2932b63bc m_u34 ; bash mk_mirror.sh c21b1a051 m_g1
# 자체시험 숫자 (절대 경로로)
bash run_selftests.sh $U/m_fix $U/st_fix ul_lib ul_s3 ul_observers ul_gates ul_reader seal_check decks_check hist_decks_check seal_selftest decks_selftest hist_decks_selftest hist_read_selftest
bash $H bash run_selftests.sh $U/m_fix $U/st_fix ul_runner_test
python3 -I count_checks.py st_fix/logs/ul_reader.selftest.log R37 R35 R16 R33 R36
# 고치기 전 판 + 지킴 시험 (시험 먼저 코드에 2932b63bc..28b66e116 의 시험 diff 를 얹음) = 191/212
cp -a m_tf m_pg && (cd m_pg && patch -p1 < ../out/guard_tests.diff)   # 그 파일 봉인 줄만 다시 계산 (위 셸 기록)
bash run_selftests.sh $U/m_pg $U/st_pg ul_reader
# 사전 리뷰 탐침 (증거 폴더 사본)
bash run_probe.sh probe_resume_unfinished.py m_fix/docs/data/ps45_unload_20261009 out/pre_ul01_fix.json
bash run_probe.sh probe_misc.py m_fix/docs/data/ps45_unload_20261009 out/probe_misc_fix.json
# U2 독립 탐침
bash run_probe.sh u2_probe_tails.py m_fix/docs/data/ps45_unload_20261009 out/u2_tails_fix.json         # ULPR-01 이웃 (N2 = PRE-UL2-01)
bash run_probe.sh u2_probe_two_boundaries.py m_fix/docs/data/ps45_unload_20261009 out/u2_two_fix.json
bash run_probe.sh u2_probe_g2.py m_fix/docs/data/ps45_unload_20261009 out/u2_g2_fix.json               # ULPR-03 · 04
# 최소 해결 후보 (scratch 만 · 리포 아님): m_patch2 = 판독기 두 줄 + R10 · R37 POS_LATER 픽스처 덱 순서
bash run_selftests.sh $U/m_patch2 $U/st_patch2 ul_reader ; bash $H bash run_selftests.sh $U/m_patch2 $U/st_patch2 ul_runner_test
bash run_probe.sh u2_probe_tails.py m_patch2/docs/data/ps45_unload_20261009 out/u2_tails_patch2.json
# 변이 (고친 사람 25 · U2 추가 20)
bash $H bash run_probe.sh mutate_fixer.py m_fix mut_work out/mutations_fixer25.json
bash $H bash run_probe.sh u2_mutate.py m_fix mut_work2 out/mutations_u2.json
# Codex 탐침 (10-15 증거 probes/ + 10-21 변형 둘) 을 리뷰 핀 28b66e116 사본에서
bash setup_codex_rerun.sh 28b66e116 $U/codex_pin
bash $H bash run_codex_probes.sh $U/codex_pin resume_recheck receipt_ids_recheck receipt_ids_recheck_q4tolerant grammar_provenance grammar_provenance_kitreader grammar_types history_actual kit_byte_checks grammar_windows_r32 source_audit
# 금지 인용 스윕 — 바뀐 파일 94 (files=) · 전체 CLI
python3 -I -B u2_bansweep_changed.py /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a948397637bfe9a76 out/changed_files.txt out/bansweep_changed.json
(cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a948397637bfe9a76 && bash $H python3 -I -B scripts/check_review_findings.py --ban-sweep)
```
