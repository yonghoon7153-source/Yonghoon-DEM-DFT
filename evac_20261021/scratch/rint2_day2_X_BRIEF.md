# Rint ② 2 일 차 X — 접합 지문 · S0 가 같은 접합 함수 · s 목록 (시험 먼저 · 작업 트리 · push 안 함)

## 기반
- 너의 작업 트리에서 `git reset --hard 5dc6f7f0b` (= 원격 본 가지 끝 · S0–S3 구현 · 길이 법칙 v0 · 수렴 증서가 합쳐진 판) → `git log -1`.  `git fetch` 하지 않는다.
- 정본: 설계 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` (§1-2 #11 · #13 · §2 S0 · §4 S2 · §1-5) · 등록 R `docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md` §2-1 · 원장 `RINT-23`.
- ⛔ 봉인 32 파일 (`scripts/run_network_194_parallel.py` 의 `CODE_FILES`) 금지 · 문서 · 원장 · CLAUDE.md · 진행 기록 금지 (메인).

## 할 일 (커밋 묶음마다 시험 먼저 → 구현)
1. **`RINT-23`** — `scripts/carbon_junction.py` 의 `_fp` 가 dtype=object 배열의 포인터 바이트를 해시한다.  시험 먼저: 같은 내용 · 다른 객체 (그리고 별도 `python3 -I` 하위 프로세스 둘) → 지문 같아야 · 내용 한 글자 다르면 달라야 · 고치기 전 실패 확인.  수정: 객체 배열 = 내용 직렬화 (길이 접두 · UTF-8 · 순서 보존) · 숫자 배열 = dtype · shape · C 순서 바이트.  같은 꼴의 지문 함수가 `scripts/ptfe_face_alpha.py` · `scripts/ca_s0_census.py` · `scripts/step3_conv_cert.py` 에도 있으면 같은 시험으로 확인 (있으면 같이 고침).
2. **S0 = 같은 접합 함수** — `scripts/ca_s0_census.py` 의 접합 census (지금 B0 미리보기 · touch / band 두 정의) 를 판정 · 보고용으로는 `carbon_junction.cjunc_registry` (B3 · 길이 법칙 v0) 와 **같은 함수**로 센다 (설계 §4-1 끝 "S0 census ↔ registry").  미리보기 판은 표지를 달고 남겨도 된다.  새 출력: 긴 접촉 수 · L_c 분포 (요약 + 후보별 목록) · 같은 가닥 근접 후보마다 경로 호 길이 s (**후보별 목록** — s_min 을 정하는 근거 · 지금 원장은 요약뿐) · 배율 합.  σ 칸은 여전히 없어야 (S0 = 솔브 없음 · 시험이 강제).
3. **S0 의 α 사유 문장** — 합친 트리에서 *"S1 face_alpha 함수가 이 트리에 없다"* 는 사실이 아니다 → `ptfe_face_alpha` 의 실제 함수로 α 분포를 내거나 (raster-only 범위 안에서) 문구를 정확히 바꾼다 · 시험 (E1j 가 status 만 보던 것을 사유까지).
4. **끊기 규칙 사본 대조** — 생산 `step3_sigma._fibre_segment_ijk` ↔ B (`carbon_junction`) 사본 ↔ C (`ca_s0_census`) 사본 ↔ A (`ptfe_face_alpha.build_capsules`) 의 조각 규칙: 끊김 (gap_tol) 이 있는 합성 침대 몇 개에서 셀 집합 · 조각 경계가 같은지 시험 하나 (사본 하나를 일부러 틀리게 한 변이가 그 시험을 떨어뜨려야).  하나로 합치는 리팩터는 하지 않는다 (생산 경로 비트 동일 부담).
- 회귀: `scripts/test_carbon_junction.py` (지금 139) · `scripts/test_ca_s0_census.py` (108) · `scripts/test_ptfe_face_alpha.py` (238 · 오래 걸리면 끝에 한 번) · `python3 scripts/step3_sigma.py --selftest` · `--selftest-rint` · `python3 scripts/check_method_discipline.py --selftest` + 인자 없이 (오류 0).  `scripts/test_step3_conv_cert.py` 는 2,000 초대라 돌리지 않는다 (지문 함수를 바꿨다면 그 파일의 지문 부분만 짧게 확인).

## 규칙
- push · `scripts/check_all.sh` · `git fetch` 안 함 · 디스크 적게 · 다른 에이전트 하나 (Y — payload · 러너 · 판정기) 가 같이 돈다: 그쪽 파일 (`scripts/mpm_webapp_payload.py` · `scripts/run_contract.py` · `scripts/sdcp_gain_vox015_8arm.sh` · `scripts/sdcp_gain_verdict.py` · `webapp/templates/mpm_lab.html`) 은 건드리지 않는다.
- 커밋 메시지 영어 · 모델 이름 없음 · "pre-fix N/M (fails = …)" 꼴 (반례 수 · 검사 수 따로) · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 보고 (한국어 · 표 · 짧게): 커밋 SHA · 고치기 전 → 뒤 · 지문 재현 (두 프로세스) · S0 새 출력 칸 · 사본 대조 결과 · 설계와 다르게 한 곳 · 남은 것.
