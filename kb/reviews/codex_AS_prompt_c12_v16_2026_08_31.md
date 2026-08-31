---
title: "리뷰 요청 AS — C-12 v16 (회신 AR 해제조건 10건 이행)"
date: 2026-08-31
updated: 2026-08-31
tags: [review, codex, sdcp, c12, vasp, bundle, staged, potcar, attestation, estimand]
status: 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: max
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 AS — C-12 v16

회신 AR(v15 제출 NO-GO)의 **해제조건 10건 전부**를 이행했다. AR 은 ZIP 무결성·
114/114 해시·16잡 구성·δ_gas 식은 통과시켰고, 막은 것은 **exact estimand 가
계산 전에 막히는 경로**와 **치명적 실패가 지워지거나 stage 2 가 열리는 경로** 였다.

- 번들: `sdcp_c12_v16.zip`
- **ZIP SHA256: `796ac6566e79395c2ec89168bc3eecae8e26d3f02007d6f2fcf4ffda583f518f`**
- 생성 커밋: `779463c3` (`claude/friendly-meitner-lldvar`)
- 생성 인자: v15 와 **동일** —
  `--from_basins db/properties/c12_poses_2026_08_30.json
   --frags sdcp_neutral ptfe_c10 --refs --refs_minimal --both_seeds --single_point
   --allow_no_pin --cell_c 36.6551 --cell_c2 40.6551 --min_vacuum 15.0
   --roles primary sensitivity stress_sensitivity`
- **물리·후보집합·자세 동결은 하나도 안 바꿨다.** 바뀐 것은 ① 기체 기준을
  고정기하 static 으로 (relax 제거) ② 기체 분자를 셀 **질량중심**에 배치 —
  이 둘이 POSCAR 바이트를 바꾼다. 나머지는 게이트·러너·문서다.
- ⚠ **VASP 를 한 잡도 돌리지 않았다.** 결과를 보기 전 창이 아직 열려 있다.

### ⚠ 실물 생성이 결함 둘을 더 드러냈다 (v16 확정 전에 고침)

첫 v16 을 실제로 만들어 보고서야 잡힌 것 둘이다. **둘 다 selftest 는 통과하고
있었다** — 그 사실 자체가 보고 대상이라 적는다.

**(a) 비 UTF-8 표준출력.** 해제조건 10 에서 분석기의 **파일 IO** 를 전부
`encoding="utf-8"` 로 박고 `LC_ALL=C` 시험을 추가했는데, 그 시험 환경에
`PYTHONIOENCODING=utf-8` 을 **같이 넣어** stdout 만 살려 놓고 통과시켰다.
실제 실행(`LC_ALL=C`, 그 변수 없음)은
`UnicodeEncodeError: 'ascii' codec can't encode character '\u2713'` 로 죽었다.
⇒ 분석기 시작 시 stdout/stderr 를 `utf-8(errors="replace")` 로 재설정하고,
시험 환경에서 `PYTHONIOENCODING` 을 **제거**했다. 이제 실제로 재현·차단된다.
⚠ 이것은 "양성만 있는 selftest" 의 전형이고, 우리 코드 규율이 금지하는 모양이다.

**(b) 대안 자세 봉인이 통째로 비었다.** 해제조건 6 의 자세 봉인을 "같은 역할끼리
짝짓기" 로 짰는데, 실물 c12 는 두 조각의 대안 자세가 **다른 역할 이름**을 달고 있다:

| 조각 | primary | 대안 |
|---|---|---|
| `sdcp_neutral` | b00 | **b12 `stress_sensitivity`** |
| `ptfe_c10` | b00 | **b52 `sensitivity`** |

그래서 어느 쪽도 짝이 없어 봉인이 비고 `altpose_purpose`(탐색용)로 떨어졌다 —
**스테이지 2 의 네 잡(실행 4회)이 정의된 양을 하나도 못 내는 상태**였다.
⇒ 같은 역할이 양쪽에 있으면 그 역할로, 없으면 조각당 하나뿐인 대안 자세를
`role_pair` 로 봉인한다. 실물 v16 이 낸 봉인:

```
role_pair: E_C_sdcp    = prospective/sdcp_neutral__b12__afm2424_pm1
           E_C_control = prospective/ptfe_c10__b52__afm2424_pm1
           roles       = {sdcp_neutral: [stress_sensitivity], ptfe_c10: [sensitivity]}
```

봉인 안에 **역할이 비대칭이라는 사실**과 **해석이 아직 미정이라는 것**을 같이
적었다 — 식은 결과 보기 전에 박고, 뜻은 Q4 로 열어 둔다.

## 1. 조건별 이행

**① clean-free exact 경로에서 옛 clean-reference gate 제거 (AR P0-1 / Q7-1)**
`analyze_results.py` 가 manifest 에 clean-slab 이 **선언되지 않았으면** clean Q
reference 를 요구하지 않는다(`mg["clean_free"]`). 그 역할은 `_estimand_topology_check`
의 direct topology 비교가 대신한다. 종전엔 exact pm1/net4 complex 가 전부
`MAGNETIC_REFERENCE_INVALID` 가 되어 primary D 를 낼 수 없었다.
⚠ clean 이 **선언돼 있으면** 옛 게이트는 그대로 산다 (레거시 회귀 방지).

**② 정본 blocks 를 보존하고 primary scope view 만 강등 (AR Q1 / P0-2)**
`out["blocks"]` 는 **다시 쓰지 않는다.** 강등은 `out["primary_estimand_blocks"]`
라는 별도 view 에서만 일어난다. 재현하셨던
`MOLECULAR_STATE_UNRESOLVED + BASIN_HETEROGENEOUS` → 빈 배열이 이제 나오지 않는다.
pooled 결과(`secondary_G`)와 pooled minimum 은 heterogeneity 가 있으면 계속
차단한다(`out["pooled_effect"]` 의 `secondary_G_citable` / `pooled_min_citable`;
차단 시 `secondary_G_eV = None`). exact key 의 에너지·입력·기하·전자수렴·직접
topology 차단은 별도로 유지된다.

**③ box20/24 를 공통 내부기하의 static pair 로 + cross-job gate (AR Q2)**
생성기:
- 기체 분자를 **질량중심이 셀 중앙**에 오도록 놓는다(경계상자 중심이 아니다).
  두 상자의 내부좌표가 정의상 같아지고 분수 `DIPOL` 이 둘 다 (0.5, 0.5, 0.5) 다.
- COM 배치가 어느 축에서든 여백을 4 Å 밑으로 먹으면 **생성기가 멈춘다**.
- `--single_point`/`--closure` 면 기체도 **고정기하 static 단독**이다
  (v15 는 네 gas parent 가 전부 relax→static 이었다 — 지적하신 그대로다).
- `job.json` 에 `internal_geometry_sha` · `electronic_state_sha` ·
  `fixed_geometry_static` · `gas_placement` · `com_frac` 를 박는다.

분석기 — `GAS_PAIR_CONTRACT`:
box20/box24 의 내부기하·전자상태·원소순서·원자수가 같고 **둘 다 고정기하 static**
이어야 δ_gas 를 문턱에 건다. 하나라도 어긋나면 차단하고
`gas_box_delta.pass` 를 통과로 세지 않는다. 지문 필드가 없는 구판 번들도
"확인 못 함 = 통과 아님" 으로 막는다.

**④ 옛 조각별 gas gate 제거, 결측·불일치를 예외 없이 구조화 hard block (AR P0-3)**
조각별 10 meV 게이트는 `pass: None` · `role: "diagnostic_only"` 로 내려갔고,
`emol[f] = e24`(정본)를 그대로 쓴다. 결측은 `GAS_BOX_NOT_MEASURED` 구조화 차단이다.
재현하셨던 경우(SDCP/PTFE +20/+19 meV → δ_gas 1 meV)를 회귀시험으로 박았다 —
종전엔 두 `emol` 이 None 이 되어 `float − None` 으로 죽었다.

**⑤ stage-1 선결조건에 δ_gas·pm1 topology·잔여 block·seal 포괄 결박 (AR Q4)**
`_stage1_prereqs()` 로 분리했고 **여덟 축**이다:
`vacuum · molecular_state · canary_geometry · potcar_identity ·
gas_box_delta · estimand_topology_pm1 · closure_blocks_clear · root_seal_covers_plan`.
- `closure_blocks_clear` 는 `scope ∈ {estimand, global}` 잔여 record **와**
  구조화되지 않은 옛 문자열 block 둘 다 0 이어야 통과한다.
  `pooled_diagnostic` 강등분만 제외한다.
- `root_seal_covers_plan` 은 봉인이 **현재 manifest 와 예정 16잡 전체**(미실행
  2단계 포함)를 포괄하는지 본다.
여덟 축을 하나씩 깨뜨리는 ⛔음성 시험이 **배포본 안에** 있다.

**⑥ net4 topology 실패시 D_net4 실제 차단 + 대안자세 봉인 (AR P1-9 / P1-10)**
- `usable_as_sensitivity` 를 **읽는다.** topology 가 same 임을 확인 못 하면
  `branch_sensitivity.status = "suppressed_topology"` 이고 `D_net4_eV` ·
  `D_net4_minus_D_pm1_eV` 가 **둘 다 None** 이다. D_pm1 은 영향받지 않는다.
- 대안 자세를 net4 와 **같은 모양**으로 봉인했다:
  `estimand_job_keys_pose_alt[role] = {E_C_sdcp, E_C_control, E_G_*, formula, gate}`,
  보고량은 `D_pose[role] − D_pm1`. 게이트도 같다.
  봉인식이 안 만들어지는 구성에서는 manifest 의 `altpose_purpose` 로 **탐색용**임을
  명시하고 분석기가 `pose_sensitivity.status = "exploratory_only"` 로 찍는다.
- `sensitivity_complete` 를 한 곳에서 판정하고, 미완이면
  `SENSITIVITY_INCOMPLETE` / `POSE_SENSITIVITY_INCOMPLETE` 주석으로
  "분기에 강건" · "자세에 강건" 서술을 금지한다.

**⑦ root seal ↔ attestation ↔ exact variant ↔ manifest/ZIP ↔ 실행 VASP 상호결박 (AR P0-5·P0-6)**
root seal — 다음을 **전부 필수**로 한다:
`schema(=potcar_root_seal/v2) · allowlist_sha256 · manifest_sha256 ·
bundle_zip_sha256 · vasp_executable(+sha256) · vasp_version_banner ·
sealed_at_utc · assembled_sha256_by_job · sealed_before_production(+evidence)`.
64자리 hex 검사. 그리고
- 봉인 variant 집합 == **계획 잡 전체**가 요구하는 variant 집합
- `assembled_sha256_by_job` 이 계획 잡을 전부 덮는가
- 봉인 배너에 **관측 VASP 버전**이 있는가
- 봉인 ZIP 해시 == 받은 ZIP 해시
⇒ 재현하셨던 "`source_sha256` + 선언만 있는 반쪽 봉인" 이 이제 `sealed_root_v13`
라벨을 못 받는다.

attestation — 세 집합의 **완전일치**를 요구한다:
`attestation variants = root-seal source variants = 계획 잡 POTCAR_SPEC variants`.
추가로 variant 별 `source_sha256`·`titel`(관측 TITEL 과 대조)·`embedded_hash`,
그리고 `manifest_sha256` · **정확한 ZIP SHA** · `allowlist_sha256` ·
`vasp_executable`/`sha256`/`version` · `site` · `created_utc` ·
`made_before_production_evidence` 를 필수로 한다.
⇒ 재현하셨던 `FAKE_RELEASE` + `UNRELATED` variant 하나짜리 합성 attestation 이
이제 `usable:false` 이고 강한 Methods 문구도 안 나온다.

`made_before_production` 은 자기선언이 아니라 **산출물 부재 검사**로 입증한다 —
`MAKE_POTCAR_ATTESTATION.sh` 가 OUTCAR/vasprun/OSZICAR/CONTCAR/WAVECAR/CHGCAR 이
하나라도 있으면 **거부**하고, 그 사실을 `made_before_production_evidence` 에 적는다.

ZIP 결박 경로: 번들 안에는 자기 해시를 넣을 수 없으므로 현장이 받은 ZIP 에서
직접 구해 `BUNDLE_ZIP_SHA256` 로 넘긴다. `SEAL_POTCAR_ROOT.sh` 와
`MAKE_POTCAR_ATTESTATION.sh` 가 그것을 요구하고 `ZIP_SHA256.txt` 로 남긴다.
분석기는 `--zip_sha256` 또는 그 파일로 읽고, 없으면 `ATTESTATION_ZIP_UNBOUND` 다.

**Q5** — 필드명을 `methods_sentence` → `methods_candidate` + `allowed_claim`
(`paw_release_attested` / `bundle_conditional_only`) 로 바꿨고,
"**후보 문구**이고 원고 채택은 사람이 한다" 를 결과에 박았다.

**⑧ runner preflight census + lock 경쟁조건 (AR P0-7 / P0-8)**
census — `run_staged.sh` 가 **실행 전에** 셋을 확인한다:
1. `MANIFEST.json` 해시를 `EXPECT_MANIFEST_SHA256`(선택) 및 봉인의
   `manifest_sha256` 과 대조
2. 계획 잡 **집합** 완전일치 — `job.json` 집합과 잡 폴더 집합 **둘 다**
3. 단계 분류를 디스크 `job.json` 으로 다시 계산해 manifest 의 `run_census.stage_of`
   와 대조하고 **개수**까지 확인
생성기가 `run_census = {job_keys, stage_of, stage_counts}` 를 박는다.
분류 규칙은 `analyze_results.py` 의 `_stage_of` 와 1:1 이다.
⇒ 재현하셨던 "job.json 하나를 지워도 classified=15·디렉터리 16 으로 통과" 가 막힌다.
봉인 완전성(12필드)과 `ZIP_SHA256.txt` 결박도 **매 실행마다** 확인한다.

lock — 내용을 **먼저 쓴** 임시 파일을 `ln` 으로 원자적으로 링크한다
(내용이 없는 창이 존재하지 않는다). `host|pid|utc` 를 기록하고,
같은 호스트의 죽은 pid 여도 **자동으로 지우지 않는다** (다른 노드의 실행일 수 있다).
종료 시 **자기 lock 만** 치운다.

**⑨ README·SUBMIT·MANIFEST·반송물·실행 횟수·의존성 안내를 실물과 일치 (AR P1-11)**
- clean-slab 이 없으면 README 가 **없다고 명시**하고 반송을 요구하지 않는다.
- "전 잡이 단일점" 을 단정하지 않고 `planned` 의 phases 에서 세어 문장을 만든다.
  relax 가 있으면 SUBMIT 이 `relax/OUTCAR·CONTCAR` 를 요구한다(canary 기하 출처).
- MANIFEST 의 `phase_dependencies`·`runner_note` 가 staged 에서
  **의존성 있음 + 단일 경로**를 말한다 (종전엔 "의존성 없음 + 배열 제출").
- 반송물에 `POTCAR_ROOT_SEAL.json` · `ZIP_SHA256.txt` ·
  `POTCAR_ATTESTATION.json` · `STAGE1_PASS.json` 을 넣었다
  (SUBMIT 과 `MANIFEST.submission.required_returns` 양쪽).
- 이전 wave 계보 주장과 `PBE PAW 5.4` 단정을 지웠다. walltime 하드코딩(56 h)도
  `cost_frozen` 에서 유도한다.
- `BUNDLE_ZIP_SHA256`(봉인 필수)·`EXPECT_MANIFEST_SHA256` 안내를 넣었다.
- **VASP 실행 수**: v15 는 잡 16 · 실행 20(gas relax 4 때문)이었다. v16 은
  기체가 고정기하 static 이므로 **잡 16 · 실행 16** 이다. MANIFEST 의
  `n_vasp_executions_total` 은 상(phase) 수이고, 그 사실을 필드 옆에 적었다.

**⑩ 배포본 production-path e2e (AR P1-12)**
- 사전등록 estimand ⛔음성 묶음을 **분석기 템플릿 안으로** 옮겨
  `_selftest_closure(chk)` 로 만들었다. 생성기 selftest 는 그 함수를 호출한다
  (검사 출처가 하나다). `python3 analyze_results.py --selftest` 가
  179 → **244건**(estimand 판정 65건 포함)이고, `selftest N/N · PASS` 와
  `재현: python3 analyze_results.py --selftest` 를 스스로 찍는다.
- **러너를 실제로 돌리는** e2e 를 넣었다(`_runner_e2e`). 가짜 PP 트리·site
  allowlist·stub `vasp_std` 로 `SEAL_POTCAR_ROOT.sh → census` 경로를 관통하고,
  지적하신 결함을 그대로 심어 막히는지 본다: job.json 삭제 · 계획 밖 잡 삽입 ·
  단계 분류 변조 · MANIFEST 변조 · 남의 lock(다른 호스트/죽은 로컬 pid) ·
  반쪽 봉인 — **⛔음성 7건**.
- **비 UTF-8 기본 인코딩**: 분석기의 전 파일 IO 에 `encoding="utf-8"` 을 박았다.
  `LC_ALL=C PYTHONUTF8=0` 으로 배포본 selftest 를 다시 돌리는 ⛔음성 시험을
  추가했다 — 수정 전에는 `UnicodeEncodeError` 로 실제로 죽었다(재현 확인).

## 2. 숫자

| | v15 | v16 |
|---|---:|---:|
| 잡 | 16 | 16 |
| 1단계 / 2단계 | 10 / 6 | 10 / 6 |
| **VASP 실행** | **20** | **16** |
| 기체 부모 phases | relax+static | **static** |
| stage-1 선결조건 | 4 | **8** |
| 배포본 selftest | 179 | **245** |
| 생성기 selftest | 524(주장) | **404**(실측·재현 가능) |
| 대안 자세 | tier 만 | **`role_pair` 봉인**(역할 비대칭 명시) |

⚠ 생성기 selftest 의 "524" 는 철회한다 — 지금 실물이 찍는 수는 402 이고,
그중 배포본 안에서 재현되는 것이 244 다. 두 수 다 실행 출력에서 센 값이다.

## 3. 여쭙고 싶은 것

**Q1.** 기체 분자를 **질량중심**에 놓는 선택. 경계상자 중심 대신 COM 을 쓰면
두 상자의 관계가 정확한 강체 평행이동이고 분수 DIPOL 이 둘 다 (0.5,0.5,0.5) 가
된다. 다만 비대칭 분자에서는 축마다 여백이 달라진다(최소 여백 4 Å 미만이면
생성기가 멈춘다). 이 선택이 δ_gas 를 오히려 흐리는 경우가 있는가?

**Q2.** `--single_point` 판에서 기체 기준을 **이완하지 않는** 선택. 복합체가
UMA 고정기하 단일점이므로 state-selection policy 를 맞춘 것인데, 그러면
`A(f,p) = E_C − E_G` 의 `E_G` 가 평형 분자가 아니다. D 는 두 조각의 차라
"각 조각의 gas 변형에너지" 가 소거되지 않는다 — 이것을 estimand 정의에
어떻게 적어야 하나? (`D(고정 conformer)` 로 선언하면 충분한가?)

**Q3.** stage-1 선결조건 8축이 **과한가**. 특히 `root_seal_covers_plan` 은
1단계 산출이 아니라 **계획**에 대한 조건이라 성격이 다르다. 여기 두는 것이
맞는가, 아니면 0단계(봉인) 실패로 분리해야 하나?

**Q4.** 대안 자세 봉인식 `D_pose[role_pair] − D_pm1`. **두 조각의 대안 자세가
다른 이유로 골렸다** — SDCP 는 `stress_sensitivity`(b12), PTFE 는
`sensitivity`(b52). 그래서 이 값은 "같은 종류의 자세 변화" 가 아니라 "두 조각을
각자의 사전등록 대안 자세로 옮겼을 때의 대비" 다. 두 가지를 여쭙는다:

(i) 이 비대칭 짝짓기가 **정의된 양**이긴 한가? 아니면 `D_pose` 를 조각별
    `A(f, alt) − A(f, primary)` 두 개로 따로 보고하는 편이 나은가?
(ii) 값이 크게 나오면 무엇을 말할 수 있나 — "자세 민감도가 크다" 인가,
    **"사전등록 자세 선택이 틀렸다"** 는 신호인가? 후자라면 재개 조건에
    넣어야 한다. 지금은 봉인에 "해석 미정" 이라고만 적어 두었다.

**Q5.** ZIP 결박을 **현장이 계산한 해시**에 의존한다. 현장이 잘못된 파일에서
해시를 뜨면 봉인·attestation·`ZIP_SHA256.txt` 가 **일관되게 틀린다**. 우리가
보낸 값과 대조하는 것은 사람의 눈뿐인데, 이 결박에 의미가 있나?

**Q6.** `methods_candidate` 를 코드가 고르는 것은 유지했다. 다만 attestation 이
`usable` 이어도 **원고 채택은 사람**이라고만 적었다. 더 강한 장치(예: 사람이
서명한 필드 없이는 강한 문구를 아예 출력하지 않음)가 필요한가?

**Q7.** 이번 판에서 **결과를 보기 전에** 더 넣어야 할 잡이 있나. AR 이
"box20 을 지금 넣는 쪽이 맞다" 고 했던 것과 같은 종류의 판단이 남아 있는가?

## 4. 확인 방법

```bash
python3 tools/sdcp/vasp_handoff_bundle.py --selftest          # 404건
python3 tools/sdcp/vasp_handoff_bundle.py --verify_zip sdcp_c12_v16.zip --expect_jobs 16
cd <풀린 번들> && python3 analyze_results.py --selftest        # 245/245 · PASS
env -u PYTHONIOENCODING LC_ALL=C PYTHONUTF8=0 python3 analyze_results.py --selftest
```

파일은 수정하지 않으셔도 됩니다 — 판정만 주십시오.
