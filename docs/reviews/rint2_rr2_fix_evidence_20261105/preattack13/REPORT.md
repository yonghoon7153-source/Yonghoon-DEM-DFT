# 사전 공격 13 — 742a3b83f (RR3-01 · arms_read 구조 계약) · 11-08 · 독립 · diff 만 (40d9658c0..742a3b83f · rint_r_chain.py · test_rint_r_chain.py) · 저자 보고 · 계획 안 읽음
탐침 = probes/ (재실행: PA13_SCRIPTS=<742a3b83f 체크아웃>/scripts) · 출력 = *.out · *.log

## P2-1 같은 부류 — RR3-01 과 같은 두 칸 편집으로 RESUME_MISMATCH 가 재실행 자격 (결정성 위반이 채택 사슬로)
- 자리: prior_runs_problem (rint_r_chain.py:4221) · ResumeRunner.run (:5113–5128)
- 재현: 정직한 RESUME_MISMATCH 시도 (실제 CLI + 가짜 러너 · 시험 RS02x 꼴: 시도 1 그룹 미확인 → 재실행 시도 2 의 L02 payload ≠ 시도 1 남은 payload) 요약에서 stop.code → TIME_LIMIT · stop.run → L03_point. 앞 런 [L01 복사 · L02 재실행] = 둘 다 생산자가 실제로 쓴 exit_ok + verified → resume_ok True · 결과 줄 다시 셈 None · 두 시도 원장 --resume 1 차례 검사 None · 재실행 원천 (시도 2) L02 = _src_done True → 다음 재실행이 시도 1 과 바이트 다른 L02 를 대조 없이 복사.
- RR3-01 과 달리 실제 재개가 막지 않음. 부모 40d9658c0 에서도 같음 = 회귀 아님 (이번 수정이 닫지 못한 같은 부류).
- 모순 근거: 요약 resume.compared 에 same false · resume.rerun = L02 인데 stop ≠ RESUME_MISMATCH = 생산자가 안 쓰는 조합 · 사슬에 요약 resume 칸 읽는 곳 없음 (쓰기만 :5103–5125).
- 탐침: probes/p2b_resume_mismatch_chain.py (출력 p2b_resume_mismatch_chain.out · 부모 판 p2b_resume_mismatch_chain_PARENT.out) · 단일 시도 원장 판 probes/p2_resume_mismatch.py
- 고침 안: stop_record_problem 끝 규칙 — s.resume 이 객체이고 compared 에 same 이 True 아닌 원소가 있으면 stop.code == RESUME_MISMATCH 이고 stop.run == resume.rerun 일 때만 받음. 더 굳게 = 결과 줄 셀 때 resume.from 시도의 resume_leftovers 와 rerun 폴더 바이트 재대조 (same 을 true 로 고친 세 칸 편집도 막음). 정직 꼴 무영향 (compared 전부 같고 뒤 런에서 자원 · 시간 멈춤 / rerun 런에서 멈춰 compared [] · determinism None).

## P2-2 verified 판정이 칸 이름 + file · index · sha256 만 봄 — 나머지 ARM_PUBLIC 11 칸 값 안 봄
- 자리: arms_read_kind (:2170–2205)
- 재현: 실제 Runner._execute + 모의 run_in_group · 이름 맞고 내용 {} 인 팔 → read_run ARM_UNREADABLE → arms_read = file_ids. 요약 두 칸 편집 + 팔마다 11 칸을 생산자가 안 쓰는 값으로 (전부 None · state 'short'/'legacy' · protocol_id 'unknown:x' · cert_pass False · sid_fp '' · cg_iters True · err_rel −5.0) → verified · resume_ok True · 실제 git 원장 --add --resume 1 rc 0 (대조: 덧붙이지 않은 file_ids = rc 3 RESUME_NOT_ALLOWED) · py3.8 같음.
- read_run (:2381–2398) 성공 값: state ∈ {positive, zero} · protocol_id = 'p3ca-…' · sid_fp 비지 않은 글 · cert_pass 4 칸 (positive 면 전부 True) · err_rel 유한 float ≥ 0 (zero 면 0.0) · cg_iters/resolve_iters = int 또는 None.
- 탐침: probes/p1_value_domain.py · 실경로판 probes/p1b_value_domain_cli.py
- 고침 안: 위 값 꼴을 verified 조건에 (read_run 과 한 함수로 = 사본 없음) · 정직 팔 기록 406 개 거부 0 (probes/p5_value_domain_honest.py) · ⚠ 그럴듯한 값으로 일관 위조 = 선언된 한정 그대로 · 완전히 닫으려면 _copy 처럼 read_run 재판독.

## P3
- ① 앞 런 기록 완결성 대조 없음: arm_list 칸 없음 · REQ_KEYS 결손 · outdir 아무 값 · 파일 이름 NUL · 줄바꿈도 verified (probes/p6_struct_edges.py) · 이것만으로 실패 런 자격 길 아님 · MergeFetch 기록 outdir (units/…/attempt_n/<od> · source 칸) = record_outdir 꼴 아님 → 생산자별로.
- ② read_run (:2263) 이 arm_file_prefix 를 안 부르고 같은 식 사본 (지금은 RR3C · RR3P 가 어긋남 잡음).

## 버틴 것
- 정직 출력 잘못 거부 0: 실제 CLI 런 기록 260 전부 verified (probes/p3_honest_shapes.py · (1,None) 128 · (2,[1,2]) 96 · (8,None) 36 · 사다리 · 예측 · 12 단위 · MergeFetch · 넘침 점 · 재실행 복사) · 합성 510 꼴 (arms 1–8 × 유효 팔 고르기 × 킷 둘 · 정준 JSON 왕복) 전부 verified · 실패 꼴 전부 file_ids (probes/p4_all_arm_forms.py).
- 재실행 자격 있는 정직 요약에 file_ids 앞 런이 생기는 길 없음 · 생산자 셋 모두 생성 함수 · 초기값 [] = empty · bool · float · str · 큰 index · 순서 · 겹침 · 수 불일치 · 경로 · 킷 앞자리 · 끝 이름 · sha 꼴 · 섞인 칸 · 튜플 · 범위 밖 요청 = bad · NaN · Infinity = 엄격 JSON 이 막음.
- 변이 30/30 (--only RR3,PC12,CT06 · arms_read_kind 21 · prior_runs_problem 2 · 생산자 실패 길 3 · 성공 길 1 · 앞자리 1 · idx 자기 참조 1 · kit 무시 1 · probes/mutate.py · mutate2.py · mutation_run.log · mutation_run2.log).
- CI: py3.8.20 py_compile OK · RR3 · PC12 · CT06 13/13 (3.8 · 3.11) · 사슬 487/487 (3.11 364 s · 3.8.20 548 s) · 끝-끝 51/0 (829 s) · pyflakes · check_undefined_names 깨끗 · check_review_findings rc 0 · ban 누수 0 · check_method_discipline 오류 0 · 안 돌린 것 = check_all.sh 전체.
