# Rint ② 2 일 차 Y — payload · 러너 · 판정기 배선 (시험 먼저 · 작업 트리 · push 안 함)

## 기반
- 너의 작업 트리에서 `git reset --hard 5dc6f7f0b` (원격 본 가지 끝 · S0–S3 구현 · 길이 법칙 v0 · 수렴 증서 · face_alpha 배선 · `ca_ext` 블록) → `git log -1`.  `git fetch` 하지 않는다.
- 정본: 설계 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §3-2 · §4-2 · §5-2 (입력 · 출력 · 스위치 이름) · §6 (수렴) · §7 (세대 · 영수증 · LEAN 표 · `p3ca-` · `unknown:ca_ext`) · 등록 R §3 · §4 (런 꼴) · 지금 코드 = `scripts/mpm_webapp_payload.py` (face_alpha · `--step3-rtol` 배선 있음) · `scripts/run_contract.py` (`CA_EXT_SUBBLOCKS` = `ptfe_face` 만) · `scripts/sdcp_gain_vox015_8arm.sh` (`PTFE_STAMP=face_alpha` 를 아직 거부) · `scripts/sdcp_gain_verdict.py` (`ca_ext_record_ok` 를 아직 안 부름) · `scripts/carbon_junction.py` (읽기만 · 손대지 않음 — 다른 에이전트 X 가 고친다).
- ⛔ 봉인 32 파일 금지 (`scripts/run_network_194_parallel.py` 의 `CODE_FILES` — `webapp/mpm_lab_register.py` · `webapp/app.py` 포함) · 문서 · 원장 · CLAUDE.md · 진행 기록 금지 (메인).

## 할 일 (묶음마다 시험 먼저 → 구현 · 기본 끔 · 끄면 매니페스트 = `code_sha` · `exec_env` 빼고 바이트 같음)
1. **payload 의 탄소 접합 · SDCP 수정자 배선 (B6)** — 설계 §4-2 · §5-2 의 스위치 (접합 켜기 · R_j · 법칙 `len_scaled_v0` · s_min (필수 · 기본값 없음 · 정량이면 없을 때 거부) · PTFE–접합 끝 P0/P1 · SDCP c ∈ {0, 1}) 를 CLI 로 · `carbon_junction` API 그대로 호출 · `ca_ext` 에 `cjunc` · `sdcp_mod` 하위 블록을 `run_contract.CA_EXT_SUBBLOCKS` 에 `ptfe_face` 와 같은 꼴로 등록 (생산자 · 소비자 검사 같은 함수) · 세대 id `p3ca-` · 블록 결손 = `unknown:ca_ext` 그대로 · 규칙 M 회계 (`protocol_ext`).
2. **조합 정책** — face_alpha + cjunc 동시 = 지금처럼 거부 (payload 입구에서도 같은 거부 · 구조화 사유) · **face_alpha + `--step3-rtol` = 허용** (다음 세대 판정 꼴) → 픽스처 끝-끝 시험 하나 (둘 다 기록 · 수렴 증서 칸 · 매니페스트) · cjunc + `--step3-rtol` 도 같은 꼴 시험.
3. **러너** `scripts/sdcp_gain_vox015_8arm.sh` — `PTFE_STAMP=face_alpha` 허용 · 새 손잡이 env (접합 · R_j · s_min · P · c · rtol) → payload 인자 (`P2_EXTRA` 허용목록) · 팔 이름 태그에 새 축 (옛 팔과 이름 충돌 없게 — CLAUDE.md Lee 절의 SKIP 캐시 함정) · 발사 전 계약 검사 (선언한 축 = 매니페스트 축) · 러너 selftest 가 있으면 시험 먼저.
4. **판정기** `scripts/sdcp_gain_verdict.py` — 팔 JSON 마다 `run_contract.ca_ext_record_ok` (소비자 검사) · 세대 섞임 (현 세대 ↔ `p3ca-`) = 거부 · 수렴 증서 칸 없음 / 실패 = 미게시 팔로 셈 · 시험 먼저 (변조 팔 · 섞인 코호트 · 증서 없는 팔).
5. **웹앱 표지** — face_alpha 처럼 봉인 밖 템플릿 `webapp/templates/mpm_lab.html` 에 cjunc · sdcp_mod 표지 (매니페스트 값을 읽기만) · 시험 `webapp/test_ca_ext_labels.py` 에 추가 · 봉인 파일이 필요하면 하지 않고 "미룸" 으로 보고.
- 회귀: `scripts/test_ptfe_face_alpha.py` · `webapp/test_ca_ext_labels.py` · `python3 scripts/run_contract.py --selftest` · `python3 scripts/check_method_discipline.py --selftest` + 인자 없이 (오류 0 · 규칙 M) · 러너 · 판정기 selftest · `python3 scripts/step3_sigma.py --selftest` · 끈 경로 매니페스트 대조 (face_alpha 시험의 B2 꼴).  `scripts/test_step3_conv_cert.py` 는 돌리지 않는다 (2,000 초대).

## 규칙
- push · `scripts/check_all.sh` · `git fetch` 안 함 · 디스크 적게 · 다른 에이전트 X 가 같이 돈다: `scripts/carbon_junction.py` · `scripts/ca_s0_census.py` · 그 시험 파일은 건드리지 않는다.
- 커밋 메시지 영어 · 모델 이름 없음 · "pre-fix N/M (fails = …)" 꼴 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 보고 (한국어 · 표 · 짧게): 커밋 SHA · 고치기 전 → 뒤 · 새 CLI · env 이름 · 끈 경로 비트 대조 · 조합 정책 시험 · 설계와 다르게 한 곳 · 남은 것 (런 사슬 명령 꼴 등).
