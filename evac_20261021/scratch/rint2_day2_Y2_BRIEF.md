# Rint ② 2 일 차 Y2 — 이어서 (러너 · 판정기 · 웹앱 표지) · 시험 먼저 · 작업 트리 · push 안 함

## 상황
- 앞 에이전트 (Y) 가 컨테이너 재시작으로 멈췄다.  그가 남긴 커밋 둘 (원래 브리프 `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rint2_day2_Y_BRIEF.md` 의 할 일 1 · 2):
  - `e3cf468f2` 시험 먼저 (B6 payload 배선 + 조합 정책) · `aff73c4d5` 구현 — 새 모듈 `scripts/ca_ext_cjunc.py` · `scripts/run_contract.py` · `scripts/mpm_webapp_payload.py` · 새 시험 `scripts/test_ca_ext_b6.py`.
- 너의 작업 트리에서 `git reset --hard aff73c4d5` (같은 저장소라 객체가 있다) → `git log --oneline -4` 로 확인.  `git fetch` 하지 않는다.

## 먼저 (읽기 · 확인)
1. 원래 브리프 전문을 읽는다 (규칙 · 정본 문서 · 회귀 목록은 그대로 따른다).
2. 남은 두 커밋을 읽는다 (`git show --stat` · `scripts/ca_ext_cjunc.py` 전문 · `run_contract.py` · `mpm_webapp_payload.py` 의 diff).  커밋 메시지의 "pre-fix" 숫자를 확인 (시험 파일을 부모 커밋 코드에 돌려 같은 실패 수가 나오는지 — 다르면 보고).
3. `python3 -B scripts/test_ca_ext_b6.py` → 전부 통과인지.  실패가 있으면 그것부터 (시험 먼저 원칙).

## 할 일 (원래 브리프의 3 · 4 · 5 — 묶음마다 시험 먼저 → 구현 · 기본 끔)
3. 러너 `scripts/sdcp_gain_vox015_8arm.sh` — `PTFE_STAMP=face_alpha` 허용 · 새 손잡이 env (접합 켜기 · R_j · 법칙 · s_min · P0/P1 · SDCP c · rtol) → payload 인자 (`P2_EXTRA` 허용목록) · 팔 이름 태그에 새 축 (옛 팔과 이름 충돌 없게 — 같은 OUTDIR 의 SKIP 캐시가 옛 팔을 재사용하는 함정) · 발사 전 계약 검사 (선언한 축 = 매니페스트 축).  러너에 selftest / 건식 모드가 있으면 그것으로 시험 먼저 · 없으면 셸을 부르는 작은 파이썬 시험 (`bash -n` + 가짜 python 으로 만든 명령줄 대조).
4. 판정기 `scripts/sdcp_gain_verdict.py` — 팔 JSON 마다 `run_contract.ca_ext_record_ok` (소비자 검사) · 세대 섞임 (현 세대 ↔ `p3ca-`) = 거부 · 수렴 증서 칸 없음 / 실패 = 미게시 팔로 셈 · 시험 먼저 (변조 팔 · 섞인 코호트 · 증서 없는 팔 · 정상 코호트 양성).
5. 웹앱 표지 — 봉인 밖 템플릿 `webapp/templates/mpm_lab.html` 에 cjunc · sdcp_mod 표지 (매니페스트 값을 읽기만 · face_alpha 표지와 같은 꼴) · 시험 `webapp/test_ca_ext_labels.py` 에 추가 · 봉인 파일 (`webapp/app.py` · `webapp/mpm_lab_register.py` 등 32) 이 필요하면 하지 않고 "미룸" 으로 보고.
6. 새 시험 파일 (`scripts/test_ca_ext_b6.py` 와 이번에 만든 것) 을 `scripts/check_all.sh` 에 기존 줄 꼴 그대로 등록 · 각 실행 시간을 잰다 (60 s 넘으면 보고 — 게이트 밖으로 뺄지 메인이 정한다).

## 회귀 (끝에 한 번 · 결과 수를 그대로 보고)
- `scripts/test_ca_ext_b6.py` · 새 시험 · `webapp/test_ca_ext_labels.py` · `python3 scripts/run_contract.py --selftest` · `python3 scripts/check_method_discipline.py --selftest` + 인자 없이 (오류 0 · 규칙 M) · 러너 · 판정기 selftest · `python3 scripts/step3_sigma.py --selftest` · 끈 경로 매니페스트 대조 (face_alpha 시험의 B2 꼴 — 새 손잡이를 다 끄면 매니페스트 = `code_sha` · `exec_env` 빼고 5dc6f7f0b 와 바이트 같음).
- `scripts/test_ptfe_face_alpha.py` 는 메인이 다른 가지에서 돌리는 중이니 돌리지 않아도 된다 (payload 의 face_alpha 경로를 바꿨다면 돌린다).  `scripts/test_step3_conv_cert.py` 는 돌리지 않는다 (2,000 초대).

## 규칙
- push · `scripts/check_all.sh` 실행 · `git fetch` 안 함 · 디스크 적게 (임시 = 스크래치 · 쓰고 지움).
- 다른 가지 (X — 메인이 회귀 중) 가 `scripts/carbon_junction.py` · `scripts/ca_s0_census.py` · `scripts/ptfe_face_alpha.py` · 그 시험 파일을 고쳤다 — 너는 이 파일들을 건드리지 않는다 (나중에 메인이 둘을 합친다).  `ca_ext_cjunc.py` 가 `carbon_junction` 의 내부 함수에 기대고 있으면 보고 (X 가 `_fp` 와 census 를 바꿨다).
- ⛔ 봉인 32 파일 (`scripts/run_network_194_parallel.py` 의 `CODE_FILES`) · 문서 · 원장 · CLAUDE.md · 진행 기록 금지.
- 커밋 메시지 영어 · 모델 이름 없음 · "pre-fix N/M (fails = K checks from J counterexamples)" 꼴 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 보고 (한국어 · 표 · 짧게): 이어받은 두 커밋 확인 결과 (pre-fix 재현 · 시험 수) · 새 커밋 SHA · 고치기 전 → 뒤 · 새 CLI · env 이름 · 팔 태그 꼴 · 끈 경로 비트 대조 · 조합 정책 시험 · 시험 실행 시간 · 설계와 다르게 한 곳 · 남은 것 (런 사슬 명령 꼴 등).
