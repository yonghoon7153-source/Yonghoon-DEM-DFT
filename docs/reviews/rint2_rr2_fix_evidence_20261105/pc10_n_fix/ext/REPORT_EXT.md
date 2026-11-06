# Rint ② PC10 확장 — 사전 공격 11 P2-A · P2-B · P3-5 · P3-6 + 문구 정정 (11-06 · 작업 트리 에이전트 · 1저자 11-06 규칙)

- 근거 = 사전 공격 11 회차 (대상 = N1 · N2 · N4 고침 첫 판 · P1 0 · 새 결함 0 · P2 둘 = 바탕 `766e1e80c` 에도 있던 꼴 · P3 여섯) · 그 회차 탐침 사본 = pa11_probes/ · 규칙 = 생산자가 쓰지 않는 칸 조합 = 모순 = 재실행 자격 없음 (읽음 False · fail-closed) · 시험 먼저.
- 커밋 = 작업 트리 가지의 `766e1e80c` 위 한 커밋 (첫 판을 고쳐 다시 · push 없음 · main 반입 = cherry-pick -x · 원 번호 = 반입 커밋 메시지) · 원장 · CLAUDE.md · check_all.sh 무변경 · 게이트 안 돌림.
- 코드 sha256 (logs/code_sha256.txt): 사슬 0d72d11b… · 시험 4982c064… · 끝-끝 41762029… (무변경) · 고치기 전 (첫 판) = 사슬 f3d6a40f… · 시험 f7f1c0f7… · 중간 판 (outdir 접두만) = 사슬 8ef1bf85….
- ⚠ 이 파일 = 본 세션이 넣음 (하위 에이전트 보고 파일 쓰기 막힘 · 에이전트 본문 그대로 · 커밋 번호 줄만 반입 뒤에도 남는 표기로) → 넣은 뒤 pc10_n_fix/ · 바깥 SHA256SUMS 다시.

## 0. 쉽게 말하면
- P2-A — 결과 본 시도 폴더에 rejected.json 하나 ({} 도) → recover 결과 줄 rejected · 결과 전 → 채택에서 빠짐 · 새 --add rc 0 (옛).  이제 시도 폴더 안 거부 기록은 생산자 꼴일 때만 읽는다 (폴더 = attempt.json + rejected.json 뿐 · 칸 = REJECTED_KEYS · n = 번호 · 시작 커밋 = attempt.json) · 그 밖 = Stop ATTEMPT_LEDGER_MISMATCH · 결과 줄 없음 · 새 --add rc 3 ATTEMPT_ORDER_MISMATCH.
- P2-B — 한 칸 손질 넷 (멈춤 이름만 GU · GU 기록 rc 1→0 · GU 멈춘 런 = 앞의 끝난 런 · TIME_LIMIT 기록에 팔 읽음 + outdir 다른 곳) 이 자격을 얻던 꼴 → 기록 안 대조 (runs 마지막 · outdir · arms_read [] · GU = 끝 기록 사슬 쪽 확인 False) → 자격 False · 같은 부류: outdir 옆 이름 <런>_arm9 → 요청 칸이 정하는 정확한 이름 (지시서 밖 보탬 · 이름 계산 = Runner._prepare 와 같은 run_outdir_suffix).
- P3-5 — 요약 칸 꼴 틀림 일곱 (+ runs 정수) = traceback · 뒤 폴더 못 셈 (옛) → 그 폴더 Stop · 사유 · 뒤 폴더 결과 줄.
- P3-6 — 머리말 end_rc_known → end_record_known.
- 문구 정정 — REPORT §8 "여러 칸 함께" = 과소 기술 (한 칸 손질 넷이 있었다) · §1-2 · §8 · 사슬 주석 둘의 "디스크 signal_after = 옛 기록" = 근거 없음 (C2b 4ed966b5d 부터 디스크 원인 None · 시험 고정물 꼴뿐).

## 1. 생산자 꼴 (원천)
- 거부 기록: attempt_open (3482–) 순서 = 폴더 → attempt.json (ledger_commit = head) → 시작 기록 커밋 → 풀기 전 대조 → attempt_reject (3462) · 칸 = {schema · n · code = Stop.code · cause = str · ledger_commit = 같은 head · utc} · 그때 폴더 = attempt.json + rejected.json 뿐 (C1b ae8ea5ebd 부터 같은 칸).
- 멈춘 런 기록 (Runner._prepare 4813 · _execute 4825–): outdir = 이름 + run_outdir_suffix · rec = dict(req (arms · arm_list), outdir, arms_read []) 를 붙인 뒤 그 런에서 Stop → runs 의 마지막 · 팔 읽기 전 · GU 는 끝 기록 확인 False 일 때만 · TIME_LIMIT · RUNNER_RC 는 확인 True 뒤.
- recover_group (7371): 확인 안 된 · 결합된 끝 기록만 갈아 씀 → chain_end.confirmed = 생산자 꼴에서 늘 False.
- 단계 요약: stop = null · 객체 · runs = 목록 · 원소 = 객체 · outdir = 글.

## 2. 고친 것 (scripts/rint_r_chain.py)
- P2-A: rejected_in_folder (4334) = rejected_record → rejected_form_problem (4290) → rejected_folder_problem (4312) · result_recount (시도 폴더) · recover_ledger 가 이 한 함수 · 옆 거부 기록 = 그대로.
- P2-B: stop_record_problem → stopped_record_problem (4008) — 런 기록 있는 TIME_LIMIT · RUNNER_RC · GU 만: ① runs[-1] 이 멈춘 기록 ② outdir = RUN_DIR_RE · 접두 + 요청 칸 있으면 정확히 record_outdir (4773 · run_outdir_suffix 4764 = _prepare 와 한 함수) ③ arms_read = [] ④ GU 는 chain_confirmed (4044) 가 False 이거나 못 읽음 (None) 일 때만 · 그 밖 = 사유.
- P3-5: summary_shape_problem (4196 · result_fields 요약 길 첫머리) = Stop.
- 머리말 정정 + 확장 문단 · 주석 둘 정정 · 웹앱 화면 없음.

## 3. 시험 (시험 먼저)
- 새 시험: CT05 (P2-A · 31 행 = 결과 본 폴더 위조 셋 + 정직 · 생산자 꼴 폴더 둘 · 칸 바꿈 16 · 흔적 7 · attempt.json 없음 · 꼴 틀림) · CT06 (P2-B · 61 행 = 단위 49 (대조 17 · 손질 28 · 한정 행 1 · X12 씨앗 3) + 실경로 12 (위조 7 · 대조 5) · X5 · X6 씨앗 따로) · CT07 (P3-5 · 9 행 = 칸 꼴 8 + 대조 · 같은 바탕 뒤 폴더) · CT08 (P3-6 · 머리말 이름 대조).
- 고치기 전 → 뒤 (첫 판 사슬 + 같은 시험 판): CT05 28/31 · CT06 35/61 · CT07 8/9 · CT08 실패 · CT03 1/21 → 모두 0 · 중간 판 (outdir 접두만) = CT06 7/61 · 기록 logs/count_bad_*.json · before_new.* (첫 시험 먼저 실행).
- 고정물만 고친 기존 시험 둘 (뜻 그대로): AL12c (거부 기록 → 생산자 꼴 칸 · 첫 판에서도 통과 · INPUT_MISSING 그대로) · CT03 (대조 행 = P2-A 꼴 → 생산자의 풀기 전 거부 자리로 · 옛 고정물 = 새 행 ctl_traced (Stop) · 읽기 함수 · 옆 기록 다시 셈 행 10 (변이 X10 이 확장 뒤 살아남아 더함)) · 나머지 기존 시험 기대 무변경 (중간 판 전체 = 474/476 · 실패 = 이 둘뿐 · logs/mid_chain_full_py311_before_fixture_fix.log).

## 4. 생산자 꼴 그대로
- CT01 151 · CT02 21 · CT03 9 · CT04 7 행 = 고치기 전 ↔ 뒤 변화 0 (logs/rows_diff_summary.json) · CT04 대조 ctl_timeout · ctl_signal = True · rc 0 · ctl_rc1 = False · rc 3 그대로 · AL04 · PC13 · PC16 · AL13 · LG02 · RN02 · 끝-끝 (실제 러너) 통과.

## 5. 회귀
- 사슬 3.11 476/476 (515.4 s) · 끝-끝 3.11 51 PASS · 0 FAIL (824.7 s · 끝-끝 파일 무변경).
- kgy 3.8.20 11 묶음 통과 (run_contract 124/124 · step3_rint · ptfe 242 · carbon_junction 500/500 · ca_ext_b6 502 · ca_ext_runner 151 · 사슬 476/476 · 끝-끝 51/0 · target_cert 264/264 · conv_cert 29/29 · s0_census 167) · 최종 시험 판으로 3.8 사슬만 따로 = 476/476 (624.4 s · logs/py38_chain_final.log).
- pyflakes 4.1.0 rc 0 · check_doc_refs 깨진 참조 없음 · check_review_findings rc 0 · --ban-sweep 42 × 9,515 누수 없음.
- ⚠ 이 수들은 main 반입 전 작업 트리 (바탕 `766e1e80c`) 에서 쟀다 — main 에는 S0 메모리 고침 (carbon_junction 547 · S0 186) 이 먼저 들어가 있어 반입 뒤 게이트가 합친 판을 다시 잰다.

## 6. 변이 (git 없는 사본 · 되돌림 True)
- mutate_pc10ext.py: 새 가드 36 중 36 잡힘 (약하게 33 · 생산자 꼴 거부 3 = B05 · B07 · B17 · 모두 잡아야 할 검사가 FAIL).
- 사전 공격 11 mutate_pa11: 14 중 14 (생존이던 X5 · X6 · X12 = CT06 · X10 = CT03 읽기 행).
- 지난 회차 mutate_pc10: 26 중 24 (K1 = 동등 그대로 · J3 = 글자가 rejected_in_folder 로 옮겨 건너뜀 · 짝 = A11).

## 7. 탐침 다시 (고치지 않고 · probe_rerun/summary.json · 지난 판 = 첫 판)
- 사전 공격 11: probe_rej 2/3 바뀜 (위조 둘 = recover rc 3 · 다시 셈 Stop · 새 --add rc 3) · probe_rr 5/18 (S1 · S1 noarms · S2 · S4 · S5 → 자격 False · rc 3 · 그대로 13 = 대조 8 + 한정 5 (S3 · S6 · S7 ×2 · S9)) · probe_rr2 8/9 (N4s 일곱 = traceback → rc 3 · TR 위조 → False).
- 사전 공격 10: units 1/57 (G3 = GU + 끝 기록 확인 True = 생산자 꼴 아님 → False) · units2 3/11 (AttributeError → Stop) · ledger 0/6 · rcscan = 줄 번호만 (자리 41 같음 · 날 읽기 0 · 우회 17/17) · probe_new 0/6.
- Codex 회차 ② 303/311 = 첫 판과 모든 칸 같음 (codex_probe_rerun/compare_prev.out).

## 8. 한정 (고치지 않음)
- 런 기록 ↔ 그룹 끝 기록 (원인 · rc · TIME_LIMIT/RUNNER_RC 의 확인 True) 교차 대조 — 크게 바꿔야 해 한정 (by chain ↔ recover chain_end 사본 · 기록 signal_after ↔ 디스크 원인 None · 경합 꼴 (원인 + 정수 rc) · 짝 안 맞춘 고정물 다수) · 남는 예 = probe_rr S9 (세 칸) · GU ↔ 확인은 했다 (④).
- 같은 이름 런 기록 둘 (S3) · 런 전 TIME_LIMIT 이름 차례 · 다른 칸 미검사 (copied_from · seconds · machine · S5 = arms 없으면 지남) · 디스크 signal_after 받음 (S7) · 경합 꼴 (S7 timeout rc 1) · 칸 없음 받음 (rc 칸 없음 = null (S6) · arms_read 칸 없음 = [] · 요청 칸 없는 기록 = outdir 접두만) · GU 확인 대조는 읽힐 때만 (시작 기록 없음 · 결합 안 됨 · chain_end 없는 옛 recover 끝 기록 = 안 함).
- 거부 기록: utc 시각 꼴 · cause 내용 · code 의 STOPS 소속 = 안 봄 · 옆 거부 기록 = 객체 · 엄격 JSON 만 · rejected.json 자리가 처음부터 일반 파일 아님 = 거부 기록 없음 길 (PB-03 그대로) · 흔적을 다 지운 폴더 + 위조 기록 = 구별 불가 (Q-D).
- 파일 시스템 부산물 (.nfs* 등) = 흔적으로 봄 (보수) · 두 칸 이상 함께 바꾼 손 = Q-D.

## 9. Codex 요청 범위
- 닫는 것 (claimed): P2-A · P2-B 넷 + 같은 부류 (옆 이름 · 8 팔 · _arml 뺌 · 꼴 틀린 요청 칸 · arms_read null · 객체 · 글 · outdir 빈 · null · 경로 · 다른 런 · GU 확인 꼴 틀림 · 모르는 by) · P3-5 (일곱 + runs 정수) · P3-6 · 문구 정정 · 변이 생존 X5 · X6 · X12 · X10 의 시험.
- 닫지 않는 것: §8 전부 · 실제 SIGKILL · NFS/FUSE · 비 root · kgy 3.8.10 아님 · 게이트 · 원장 등재 (본 세션).

## 10. 파일 (ext/)
REPORT_EXT.md · mutate_pc10ext.py · rerun_probes_ext.py · pa11_probes/ · probe_rerun/ · codex_probe_rerun/ · logs/ (before_new.* · count_bad_* · rows_* · mid_chain_* · final_chain_full_py311.log · final_e2e_py311.log · check_kgy_py38.* · py38/ · py38_chain_final.log · mutation_* · check_* · pyflakes.log · environment.txt · code_sha256.txt).
