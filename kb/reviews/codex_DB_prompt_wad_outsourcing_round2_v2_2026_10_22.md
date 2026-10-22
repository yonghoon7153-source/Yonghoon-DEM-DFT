---
title: "DB 프롬프트 — W_ad 외주 2차 묶음 v2 재리뷰: CZ 해제조건 일곱 + 발송 전 자체 검토 고침 (S1–S9) 이 닫혔는지 (고친 곳 diff 만) · 발송 승인 여부"
tags: [review, wad, adhesion, vasp, outsourcing, runner, checker, codex, prompt, letter]
letter: DB
date: 2026-10-22
track: wad
channel: codex
kind: prompt
status: 초안 — 발송 전 (사용자가 보낸다 · 기준 커밋 3d684e502 · 묶음 v2 MANIFEST b9450f6f… · 자체 검토 S1–S9 반영)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

> 트랙 = W_ad (DEM 협업 · 1저자 = 사용자). CZ (NO-GO · 발송 해제조건 일곱) 다음 편지다. 사용자 결정 2026-10-22: 고친 묶음을 Codex 에 한 번 더 보인다 (diff 만).
> ⛔ 점착 W 값은 kb 문서에 싣지 않는다 — 이 편지에도 W 숫자를 쓰지 않는다 (문턱 · 비율 · 벽시계만).
> 기준 커밋 `3d684e502` (브랜치 `claude/evac-2026-10-22`). ⬇ 아래 **보내는 글**만 발송한다. 회신이 오면 `codex_DB_reply_…` 로 원문 보존.
> 개정 (같은 날 · 발송 전): 첫 초안 (`ed84da61d` · 묶음 MANIFEST `92e41141…`) 을 보내기 전에 우리 쪽 적대적 검토가 CZ 고침에서 구멍 여덟 (P0 둘) 을 더 찾았다 → 고쳤다 (§2b) · 묶음 v2 를 다시 빌드했다. 첫 초안의 묶음은 아무에게도 안 갔다.

---

**[W_ad · 외주 2차] 묶음 v2 재리뷰 — CZ 해제조건 일곱 + 발송 전 자체 검토 고침이 닫혔는지 (고친 곳만) · 발송 승인 여부**

## 0. 무엇을 묻나

CZ 에서 NO-GO 와 발송 해제조건 일곱을 받았다. 설계 · 구조 봉인 · 집계 산식은 그대로 두고 일곱을 고쳤다 (해제조건 하나 = 커밋 하나).
보내기 전에 우리 쪽에서 그 고침을 적대적으로 다시 봤고 **구멍 여덟 (P0 둘 · P1 하나 · P2 다섯) + 하나** 를 더 찾아 고쳤다 (§2b · 커밋 셋).
이번에는 **고친 곳만** 봐 달라 — **해제조건마다 닫혔는가 (GO / 조건부 / NO-GO) · 자체 검토 고침이 맞는가 · 고치면서 새로 생긴 구멍은 없는가 · 이 묶음 v2 를 업체에 보내도 되는가.**
CZ 에서 GO 였던 곳 (구조 봉인 · 마스크 · 집계 산식 · optB88 입력 조합) 은 다시 열지 않아도 된다.

## 1. 보는 범위 (diff)

- 기준 = CZ 를 받은 커밋 `8d41e4e0` (묶음 v1 · MANIFEST `31e47474…`). 고친 커밋:
  - CZ 해제조건 일곱: `01c1cc4bd` (1/7) · `90ba35b17` (2/7) · `744edd949` (3/7) · `c4725b51e` (4/7) · `0eaa4896a` (5/7) · `44b095ef9` (6/7) · `b3c13f0aa` (7/7)
  - 발송 전 자체 검토: `c11446827` (1/3 · S1 · S2) · `a9cf825b0` (2/3 · S3 · S4) · `a551036e3` (3/3 · S5–S9)
  - 묶음 v2 다시 빌드 · 빌드 기록: `3d684e502`
  커밋 메시지마다 고친 것 · 재현 · 시험 · 깨기 목록이 있다.
- `git diff 8d41e4e0 3d684e502 -- tools/wad/build_round2_vasp_package.py tools/wad/build_v5_vasp_package.py tools/wad/build_aprime_interfaces.py` (+1404 −184 · 대부분 selftest).
- 묶음 v2 = `db/inputs/wad_round2_vasp_v2_2026_10_22/` · MANIFEST.sha256 의 sha256 `b9450f6f7e188b9159030b6cc6a031a106682fbd2076c27dd66acfd6f4f7bc70`.
  첫 초안의 v2 (`92e41141…`) 와 다른 파일은 넷 (run_all.sh · README.md · jobs.json · MANIFEST.sha256) — 잡 입력 (INCAR · POSCAR · KPOINTS · POTCAR.spec) 은 같다.
  옛 v1 폴더 (`db/inputs/wad_round2_vasp_2026_10_22/`) 는 리뷰받은 그대로 둔다 (발송 안 함).
- 빌드 기록 `db/properties/wad_round2_build_log_2026_10_17.json` 의 `⑤-2_CZ_고침_2026_10_22` · `⑤-3_자체_검토_고침_2026_10_22`.

## 2. 해제조건별로 한 것 (CZ 재현 사례 → 지금 막는 시험)

**① 확정 실행 기록 모순은 자동 재시도 자격을 얻지 못한다 (Q-CZ-1 · `01c1cc4bd`)**
- 판정 순서: 실행 머리줄 ≥ 2 · 끝난 OUTCAR 의 머리줄 ≠ 1 또는 마지막 `Iteration n( k)` 의 k ≠ N · 안 끝난 OUTCAR 인데 k > N + 1 → SCF_UNVERIFIED (rc 보다 먼저).
  안 끝난 OUTCAR 의 결측 (k 없음 · k ≤ N + 1) 은 실행 실패 그대로 (비준 정책 '전자 스텝 ≥ 1 뒤 충돌 = 실행 실패').
- 러너 awk 와 검사기 python 둘 다 · 탐침 대조에 10 개 더함 (`rc1_two_runs` · `rc1_it_mismatch_term` · `crash_midstep` · `crash_outcar_short` · `crash_no_iter` ·
  `crash_no_header` · `crash_outcar_ahead` · `noterm_two_runs` · `term_no_header` · `rc0_noterm_midstep`) — 기존 탐침 기대값은 하나도 안 바뀜. (S6 에서 다섯 더 — §2b.)
- 끝에서 끝: FAKE_VASP `crash_tworuns` (행 7 · rc 1 · 머리줄 둘) → 러너 단 0 SCF_UNVERIFIED · r1 안 띄움 · 검사기도 단 0 에서 멈춤 · 정상 r1 을 붙여도 'RUN_FAILED → r1 OK' 사슬이 안 나온다.

**② A→B 결박 · A 머리 = 실제 OUTCAR · 봉인한 재시작 규칙 (Q-CZ-2 · `90ba35b17`)**
- ⓑ (r1B · r2B · a4B) 는 자기 ⓐ 의 검사 기록을 꼭 받고, ⓑ 의 src = copied = end = 그 ⓐ 의 기록 WAVECAR sha 여야 한다 (r2B ← r1A). 없거나 다르면 RESTART_NOT_HONOURED.
- ⓐ 머리 NKPTS · NBANDS · ENCUT 는 반송된 ⓐ OUTCAR 원문에서 다시 읽고 (러너 `out_num` 과 같은 패턴), WAVECAR.info 의 OUTCAR 사본도 원문과 같아야 한다.
- 등록부 `restart_read_regex` 는 원문 (stdout.log + OUTCAR · 줄바꿈 그대로 — grep 과 같은 줄) 에서 다시 찾는다. 러너 `stat_of` · `elig_A` 도 같은 규칙 (이어 돌리기 · 손댄 기록에서 같은 답).
- 재현 셋 다 음성 시험 + 양성 (FAKE 긍정 문구 · 그 문구로 봉인한 등록부 → OK).
- 봉인 조건: 파일럿에서 ⓐ WAVECAR 를 읽은 ⓑ 전부에 맞고 · 새로 시작한 시도 (단 0 · ⓐ · 되돌아간 ⓑ) 에 하나도 안 맞고 · grep -E 와 python 이 시도마다 같은 답일 때만.
  (S5: 러너는 패턴을 `-e` 로 넘기고 · '-' 로 시작하거나 수량자가 붙은 regex 는 형식에서 거부 — §2b.)

**③ 모든 시도의 환경 감사 · 질문별 실패 분리 · 파일럿 재결박 (Q-CZ-3 · `744edd949` · S1 · S2 로 넓힘)**
- `resolve_job` 이 시작한 모든 단을 감사한다 (사다리가 안 지나간 단 포함 · 시작 = INCAR 또는 attempt.json). 환경 등급 모순 (status · conflicts 목록 둘 다) ·
  등록부와 다른 환경 증거 · 시도 사이 VASP 버전 · PP 종별 sha · 커널 sha 갈림이 최종 상태를 덮는다 (원래 값 `adopted_status` · 단 `env_in`).
  어느 시도든 무결성 실패면 그 이름으로 덮는다 (S1). ⇒ OK = 모든 시도 통과 + 채택 시도 수렴.
- 환경 증거는 **무결성 검사 전에** 읽는다 (S1): OUTCAR 원문의 모든 실행 머리줄 · POTCAR.species.sha256 · 커널 sha (attempt.json · 없으면 시작 표지) — 멈추는 쪽으로만 쓴다.
- 전역 감사 = 모든 잡의 모든 시도 + `run_aborted/` 의 모든 시도 → 하나라도 걸리면 공통 환경 고장 → G5_C BLOCKED · 종료 6. **`--collect` · `--check` (종료 6) · `--a4_result` 가 같은 경로** (S2).
  질문별 실패 전파는 최종 상태 기준 그대로.
- 봉인 (등록부 schema v2): 모든 시도를 본다 — 무결성 · 환경 · 그 밖 모순·결측은 거부 · 물리 실패 (실행 실패 · 미수렴 · SCF 미확인 · 재시작 미이행 · 그래서 생긴 ⓐ 자격 미달) 는 안 막는다.
  단 SCF 미확인 중 판정 근거의 확정 모순 (`run_blocks` · `outcar_oszicar_mismatch` · `step_numbering` · `rows_after_ion_summary` · `n_gt_nelm` · `nelm_unknown` · `ediff_unknown`) 은 막는다 (S1).
  `from_pilot` = {잡: {단: run_id}} · `from_pilot_sha256` 도 모든 시도. 등록부가 있으면 파일럿 잡의 시도 집합 · run_id · attempt.json · OUTCAR sha 가 봉인과 같아야 한다
  (`PILOT_BINDING_MISMATCH` · 시도 자체가 무결성 실패면 그 이름이 먼저 · 환경 등급이 있으면 그것이 이긴다).
- P1 셋: `run_one` 이 VASP 를 띄울 때마다 `pp_ok` (끊긴 뒤 재개한 ⓑ 포함) · `release_text` 와 러너 둘 다 상한이 유한한 양수 (러너 정규식과 같은 표기 — 1e+06 꼴도 거부) 가 아니면 거부 ·
  V5 `check()` 가 `a4_result` 의 시도 전부를 일관성 집합에 넣는다 (한 줄). `--a4_result` 는 봉인 등록부가 있어야 내고 V5 `load_a4_result` 는 등록부 sha 가 없는 a4 결과를 받지 않는다 (S2).
- 재현: a4A 만 다른 빌드 → 봉인 거부 · 등록부로 보면 VERSION_MISMATCH (STAGE_A_INELIGIBLE 안에 안 묻힘) · 집계 종료 6 / a4A 가 정상 환경에서 전자행 뒤 충돌 → 탄소 등록부 봉인됨 /
  봉인 뒤 run_id 변경 · OUTCAR 변경 (기록 sha 맞춤) · 봉인에 없던 단 → PILOT_BINDING_MISMATCH · CLI `--check` 종료 3 / 'ⓐ 끝 · ⓑ 전' 에서 C POTCAR 를 바꿔 이어 돌림 → 종료 6 · `.b` 안 생김 /
  해제 파일 cap_h `nan` · `0` · total `-5` → 종료 2 (고치기 전에는 cap_h `nan` 인데 잡이 돌았다).

**④ optB88 실제 함수 선택 · 커널 읽기/재생성 구분 (Q-CZ-5 · `c4725b51e`)**
- OUTCAR 해석값 `GGA = … GGA type` (입력 되울림 제외) — optB88 은 BO · PBE+D3 · a4 는 PE. 다르면 SETTINGS_MISMATCH · 못 읽으면 SETTINGS_UNVERIFIED.
  (V5 실물 반송 OUTCAR 22 개 모두 이 줄이 하나 — `   GGA     =    PE    GGA type`.)
- 커널 상태: vdW 와 kernel 을 같이 말하는 줄에 재생성 표지 → regenerated · 부정 표지 → not_read → `KERNEL_NOT_READ` (환경 등급 · 전역 정지 · 봉인 거부).
  읽기는 등록부 `kernel_read_regex` (파일럿 원문으로 봉인 — optB88 시도 전부에 맞고 optB88 아닌 시도에는 안 맞아야) 가 원문에 있을 때만 확인된다.
  등록부 전에는 optB88 수렴 시도도 KERNEL_UNVERIFIED (기존 파일럿 기대값을 의도대로 바꿈 · 봉인은 이 상태를 받는다).
  커널 문구를 읽는 stdout.log 는 이제 실행 기록 sha 에 묶인다 (S7).
- 재현 넷 (BO→PE · GGA 줄 삭제 · `ERROR: vdw_kernel.bindat not read` · `kernel differs, recalculating vdW kernel`) 다 음성 시험.

**⑤ 0 스텝 인프라 중단 — 결측 ≠ 0 행 · 미상 비용 ≠ 0 초 (Q-CZ-4 · `0eaa4896a` · S3 · S4 로 넓힘)**
- OSZICAR 결측 (`missing`) · 0 행 (`zero_rows`) · 있는데 못 읽음 (거부) 을 가른다 · stdout.log 전자 반복행이나 OUTCAR `Iteration n(` 이 있으면 거부 (출력 유실이지 0 스텝이 아니다).
- `WALL_S` (0 이상의 정수) 를 안 주면: 그 시도에 attempt.json 이 있으면 `ATTEMPT_JSON` (시간은 이미 안다) · 없으면 `UNKNOWN` → 장부가 UNKNOWN → `cap_ok` 가 다음 잡을 안 띄운다 (종료 5) →
  `bash run_all.sh --infra-wall <run_aborted 폴더> <초>` 로 장부 (json · tsv) 를 채우면 이어진다 (이미 숫자면 거부). 알려진 시간은 한 번만 더한다.
- **전자 스텝 뒤 러너째 끊긴 시도** (S3 — 시간 제한 · 노드 고장 · attempt.json 없음): 시작 표지 `attempt.start` 만 있으면 장부가 미상 → 다음 잡 보류 →
  `WALL_S=<초> bash run_all.sh --killed <잡> <단> <스케줄러 잡 id> <취소 UTC> <사유>` 로 `killed.json` 을 쓰면 이어진다. 그 시도는 사전등록대로 다시 돌리지 않는다 (값 없음 · 1저자).
- 장부의 시간은 단조 시계 `elapsed_s` (`/proc/uptime`) — 시계가 뒤로 가도 멈추지 않는다 (S4). README 5 번 · 영어 요약도 같은 뜻.

**⑥ 재개 PP · 반송 열거 오류 · 유한 상한 · δ 의존성 (Q-CZ-3 P1 · Q-CZ-6 · Q-CZ-10 ①③ · Q-CZ-9 P2 · `744edd949` · `44b095ef9`)**
- `pack()`: 있는 폴더만 열거 · find 실패 = 포장 실패 · 종료 4 (시험은 PATH 앞에 실패하는 find 를 둔다 — 시험 환경이 root 라 권한으로는 find 를 못 깨뜨린다).
- δ 실패 전파 목록에 대응 PBE+D3 쌍 · far 진단마다 `source_rung` · `source_status` · `adopted` (채택 안 된 시도의 진단이 채택 자료처럼 안 읽히게) ·
  신호 입력 결측 (채택된 far 의 p_z 없음 · G3 (ii) ΔW/ΔD3 없음) 은 `not_evaluated` + G5 라벨 ('신호 없음' 과 가른다 · '신호 없음 ≠ 중성 입증' 그대로).
- `check_rigid_shift`: 좌표 · 셀 비유한이면 위반 (NaN 좌표 extxyz 왕복 포함) · 봉인본은 전부 유한이라 재봉인 안 함.
- 영어 요약: *"24 jobs; 25 VASP executions when nothing fails (the silver a4 job is a two-stage run), up to 94 under the registered retry ladder, excluding separately recorded infrastructure retries."* (§3-3).

**⑦ 재생성 · 재봉인 · 전체 시험 (`b3c13f0aa` · `3d684e502`)**
- 사용자 결정 (2026-10-22 · CZ 권고): 파일럿 `P2S_S_A_far` 에 LOCPOT xy 면평균 — 사다리 INCAR 넷 `LVHAR = .TRUE.` · 러너 추출기
  (VASP 5 머리 · 격자 줄 · 값 개수 (모자람 · 남음 둘 다) · 유한수 · 어긋나면 안 만들고 경고만 — 잡 판정과 무관) · LOCPOT 원본은 지우고 반송 금지 ·
  `LOCPOT.zavg.txt` (z Å · 면평균 eV · 머리에 LOCPOT sha · run_id) 는 반송 · attempt.json sha 에 묶임 · 집계는 채택 시도의 것만 (아니면 `not_used`) · 정보 — 판정 아님 · 조각별 순전하로 읽지 않는다.
  잡 수 24 그대로 · 카드 · 개정 4 · 결정은 안 바꿈.
- 묶음 v2: 두 번 빌드 바이트 동일 · `sha256sum -c MANIFEST.sha256` OK · `bash -n run_all.sh` OK · `run_all.sh` = 도구의 `run_all_text()` · 묶음 schema v2 ·
  README 상태 줄 '준비본 v2 — Codex CZ 고침 + 발송 전 자체 검토 (S1–S8) 반영 · 발송 전'.
- 시험 (Linux · bash 5.2.21 · GNU grep 3.11 · GNU tar 1.35 · Python 3.11): round2 **156/156** (CZ 전 53 · CZ 고침 뒤 121) — **mawk 1.3.4 와 gawk 5.2.1 둘 다** ·
  V5 237/237 · interfaces 79/79 · s3 41/41 · se_sym_slab 122/122.
- 일하는 방식: 재현 사례마다 음성 시험을 먼저 쓰고 고치기 전 판에서 빨간 것을 본 뒤 고쳤다. 고친 뒤에는 그 고침 하나만 되돌린 사본 (CZ 고침 80 · 자체 검토 42) 에서
  자기 시험이 빨개지는지 봤다 (커밋 메시지마다 목록 · 같은 고침에 기대는 뒤 시험이 같이 빨개진 경우도 적었다).

## 2b. 발송 전 자체 검토 (2026-10-22) — 더 찾은 구멍과 고침

CZ 고침 diff 를 같은 세션의 적대적 검토 (저장소 읽기만) 에 맡겼고, 지적마다 우리가 다시 재현한 뒤 고쳤다.

| | 지적 (재현) | 고침 | 커밋 |
|---|---|---|---|
| S1 P0 | 무결성 검사에서 멈춘 시도는 OUTCAR 를 안 읽어 버전이 감사에 안 들어갔다 — 끊긴 시도 (attempt.json 없음) 가 다른 빌드여도 G5_C PASS · 종료 0 / 단 0 OK 인데 다른 빌드 · INPUT_MODIFIED 인 r1A 폴더 → 잡 OK / 파일럿 OUTCAR 에 두 번째 머리줄 (다른 빌드) → SCF_UNVERIFIED run_blocks 라 봉인 통과 · 첫 머리줄만 봤다 | 환경 증거를 무결성 전에 (모든 머리줄 · PP 종별 sha · 커널 sha) · 등록부와 직접 대조 · 사다리 밖 무결성 실패 → 잡 OK 아님 · `run_aborted` 전부 · 봉인은 판정 근거의 확정 모순을 막는다 | `c11446827` |
| S2 P0 | 전역 감사가 `collect` 에만 — 다른 빌드의 중단 시도가 있는 반송에서 `--collect` 6 · `--check` 0 · `--a4_result` OK → V5 가 채택 | `resolve_all` 한 경로 · `--check` 종료 6 · `--a4_result` 등록부 필수 + `common_environment_failure` · V5 `load_a4_result` | `c11446827` |
| S3 P1 | 전자 스텝 뒤 러너째 끊긴 시도의 비용이 0 초 · README 는 '사다리가 다룬다' 고 했지만 값 없음으로 끝난다 | 시작 표지 · 장부 미상 → 보류 · `--killed` (WALL_S) · README 5 · 재시도는 그대로 안 함 | `a9cf825b0` |
| S4 P2 | 시도 중 시계가 뒤로 가면 장부가 음수 → UNKNOWN → `--infra-wall` 로도 못 풀어 영구 보류 · 검사기는 형식 위반 | `elapsed_s` = `/proc/uptime` 차 · 검사기는 t_end ≥ t_start 를 안 요구 | `a9cf825b0` |
| S5 P2 | 러너 `grep -aqE "$RESTART_RE"` (`-e` 없음) — 봉인된 `-*reading WAVECAR` 가 옵션 오류 → 진짜 재시작을 미이행으로 · `*+ ++ ?+ +?` 는 파이썬 3.11 소유·게으른 수량자 (`X*+X` 가 "X" 에 파이썬 안 맞음 · grep 맞음) | 러너 `-e` · '-' 시작 · 붙은 수량자 형식 거부 | `a551036e3` |
| S6 P2 | 판정이 줄바꿈을 바꿔 읽고 `splitlines()` · `split()` — 행 안의 `\r` 로 러너 SCF_UNVERIFIED · 검사기 OK | 원문 그대로 · 줄은 `\n` · 칸은 빈칸·탭 · 탐침 다섯 (탐침 비교도 바이트로) | `a551036e3` |
| S7 P2 | stdout.log · POTCAR.titel · POTCAR.species.sha256 가 실행 기록 sha 밖 — stdout.log 에 재생성 줄을 더하면 무결성 경보 없이 KERNEL_NOT_READ (전체 정지) | 넷 (+ 시작 표지) 을 sha 에 묶음 | `a551036e3` |
| S8 P2 | WAVECAR.info 가 객체가 아닌 JSON (`[1]`) 이면 `a_eligible` 예외 | 없는 것으로 → ⓐ 자격 미달 | `a551036e3` |
| S9 (우리) | `incar_val` 이 빈 마지막 대입 (`NELM =`) 을 건너뛰어 앞 값을 썼다 (awk 는 값 없음) | awk 와 같게 | `a551036e3` |

검토 권고와 다르게 한 곳: ① 검토는 단조 시계로 bash `$SECONDS` 를 권했지만 그것도 벽시계 기반이라 `/proc/uptime` 을 썼다 (시작 때 못 읽으면 종료 2) ·
② 봉인에서 모순으로 막는 판정 사유를 권고의 둘 (`run_blocks` · `outcar_oszicar_mismatch`) 에서 판정 근거가 실행 하나를 말하지 않는 일곱으로 넓혔다 (행 없음 · 비유한은 물리 쪽 그대로) ·
③ V5 는 a4 결과의 등록부 sha 가 **있는지 · 형식** 만 본다 — 등록부 대조는 외주 2차 쪽이 a4 결과를 낼 때 고정 sha 로 했고, V5 는 a4 결과 파일 sha 를 고정값으로 받는다 ·
④ 끊긴 시도는 재시도하지 않는다 (사전등록 '0 스텝 중단만 다시 돈다') — 기록 경로 (`--killed`) 만 더했다.

## 3. CZ 제안 · 인계 설계와 다르게 한 곳 (이유) — 이것을 특히 봐 달라

1. 재시작 · 커널 문구 regex 글자를 `[A-Za-z0-9 _:.,=()|*+?^$/-]` 로 좁혔다 (괄호 표현 · 역슬래시 뺌) — `[\]]` · `\d` · `[[:space:]]` 가 grep -E 와 python 에서 뜻이 갈린다.
   `(?` · 빈 문자열에 맞는 regex · '-' 로 시작 · 수량자가 붙은 꼴 (S5) 도 거부한다. 구절 하나를 찾는 데는 필요 없다고 봤다.
2. 커널 줄: `(?i)kernel` 이 든 아무 줄이 아니라 **vdW 와 kernel 을 같이 말하는 줄만** — MPI · OS 경고 (`kernel module … not loaded`) 가 KERNEL_NOT_READ (전체 정지) 로 잡히는 오탐을 막으려고.
   대가: vdW 를 말하지 않는 커널 부재 문구는 놓친다 (그 경우도 읽기 문구가 없어 KERNEL_UNVERIFIED 로는 남는다).
3. 영어 요약: 제안 문구 'at least 25' 대신 '25 … when nothing fails' — a4A 가 자격 미달이면 a4B 가 안 돌아 24 회 실행도 가능하다.
4. 환경 감사에 `run_aborted/` 의 시도도 넣었다 — 처음엔 attempt.json 있는 것만, S1 부터는 전부 (0 스텝이어도 OUTCAR 머리에 빌드가 찍힌다 · 어느 쪽이 맞는지 모르므로 전부 막는다).
5. 봉인: ⓐ 에서 `a_eligible` 이 봐주는 결측 (SETTINGS_UNVERIFIED · ENERGY_UNPARSEABLE · D3_UNVERIFIED · KERNEL_UNVERIFIED) 과 등록부 전의 KERNEL_UNVERIFIED 는 봉인을 막지 않는다.
   판정 근거의 확정 모순 (S1 · 일곱 사유) 은 막는다.
6. 0 스텝 기록에 attempt.json 이 있으면 WALL_S 없이도 `ATTEMPT_JSON` (미상 아님 · 다음 잡을 막지 않는다).
7. 결박 안 된 파일 (끊긴 시도 · 무결성 실패 시도) 의 환경 증거도 읽는다 (S1) — 위조될 수 있지만 멈추는 쪽으로만 쓴다 (거짓 경보는 1저자가 반송을 보고 푼다).
8. 업체가 쓰는 명령이 하나 늘었다 (`--killed` · S3) · 러너는 `/proc/uptime` 을 읽을 수 있어야 한다 (S4 · 지원 환경 Linux 는 그대로).

## 4. 질문

- **Q-DB-1 … Q-DB-7**: 해제조건 1–7 이 닫혔는가 — GO / 조건부 / NO-GO · 남은 것이 있으면 최소 수정.
- **Q-DB-8**: §3 의 여덟 이탈이 맞는가 — 특히 (2) 커널 줄 좁히기의 대가와, 부정 · 재생성 표지 낱말 (`not · no · error · cannot · unable · fail* · missing · differ*` / `recalc* · regenerat* · generat* · comput* · writ*`) 이
  5.4.4 의 실제 긍정 문구에 걸릴 위험 (걸리면 파일럿 원문을 보고 검사기만 고친다는 방침이 맞는가) · (7) 결박 안 된 증거로 멈추는 방침의 거짓 경보 비용.
- **Q-DB-9**: LOCPOT 추출기 계약 (머리 · 격자 · 개수 · 유한 · 채택 시도만) 이 '정보' 용으로 충분한가 · 업체 LOCPOT 에 데이터 뒤 다른 블록이 있으면 (값이 남음 → 안 만듦)
  정보 손실만 있고 판정에는 영향이 없다는 설계가 맞는가.
- **Q-DB-10**: §2b 자체 검토 고침 S1–S9 가 지적을 닫았는가 · 고치면서 새로 연 구멍은 없는가 — 특히 `--killed` 절차 (업체 쪽 부담 · 끊긴 시도를 다시 안 돌리는 것) · `elapsed_s` 를 `/proc/uptime` 으로 재는 것 ·
  봉인이 막는 판정 사유 일곱의 범위.
- **Q-DB-11**: 발송 승인 — 이 묶음 v2 (MANIFEST `b9450f6f…`) 를 업체에 보내도 되는가.

## 5. 바뀌지 않은 것

카드 문턱 · 잡 행렬 24 · 사다리 INCAR (LVHAR 만 `P2S_S_A_far` 넷에 더함) · 집계 산식 (Δ_C · G3 · G4 · G5 · 80 % 발동 · δ 규칙) · 구조 봉인 · 단계 상한 값 · 결정 둘 (`D-2026-10-15-wad-p2small-vasp-card` · `D-2026-10-15-wad-aprime-v5-e70-a4-rerun` · active) ·
재시도 규칙 (끊긴 시도는 다시 안 돈다 · 0 스텝 중단만 같은 단을 다시).

## 6. 재현 방법

- `python3 -I tools/wad/build_round2_vasp_package.py --selftest` — CZ 재현 사례는 시험 이름의 'R1' … 'R7' · 자체 검토는 'S1' … 'S8' · '⛔음성'.
  mawk 로는 `mkdir /tmp/m && ln -s "$(command -v mawk)" /tmp/m/awk && PATH=/tmp/m:$PATH python3 -I …` (gawk 도 같은 식).
- `python3 -I tools/wad/build_round2_vasp_package.py --build --seal db/inputs/wad_p2small_seal_2026_10_17 --out <새 폴더>` → `diff -r` · MANIFEST sha 대조.
- 깨기 사본 목록은 커밋 메시지 (`git log 8d41e4e0..3d684e502`).
