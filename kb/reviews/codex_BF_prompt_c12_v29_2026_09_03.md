---
title: "리뷰 요청 BF — C-12 v29 (회신 BE P0 4건 + P1 3건 이행 · clean tree 재생성)"
date: 2026-09-03
updated: 2026-09-03
tags: [review, codex, sdcp, c12, vasp, prompt]
status: 발송 대기
kind: review-request
system: sdcp
confidence: high
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 BF — C-12 v29

> 이전 회신: 회신 BE (실행 NO-GO · P0 4건 · P1 3건 · 재승인 최소조건 4개)
> **VASP 는 여전히 0잡입니다.** 이번 판은 계산이 아니라 *"v28 이 맞다는 사실을 게이트가
> 보증하지 못한다"* 는 BE 의 요지에 대한 답입니다 — 게이트가 **맞는 양·맞는 잡**을 실물에서
> 보증하도록 고쳤습니다.

```
sdcp_c12_v29.zip                                     21d1af4ad9280970e2a1b69024d29f82fb3e0549e28653fa621d94b8b2f9958d
MANIFEST.json                                        a68e478eda58876a9f1701cc86ec4e6db2f06119ea18966d5341d391321d770c
analyze_results.py (번들 안)                          78960d0afcc18cbb05732d7ca6d5ea4abd577349c16a1961c6d0300171b3eb0d
census.py (번들 안)                                   517c92fc09430b2e052cbd3325983243fc75112a3744a480c9e7d6b5f2b8fc81
run_staged.sh (번들 안)                               c53f67beba1390351198c7c8fec0054c48cc1677c4b90e10e78ab870750c83a5

tools/sdcp/vasp_handoff_bundle.py                    abedb61e153f100f1eaddc9b11e2f8cbad3f141f672db6164a2859cf25328929
db/properties/sdcp_c12_claim_prereg_2026_08_31.json  5bc7afbcc45eedc7e94ecd4070c4ace08c8b3aa86ccdd3d629e538be008a6aa3
db/properties/sdcp_c12_protocol_2026_08_30.json      941f64d38fee97d5408a9a07636b44b77928e7407738f51017c236a664bf663d
db/properties/c12_poses_2026_08_30.json              b5760d6c86ee2644da467157acfcdc217ce599371b7dba81120323a509da4f39
db/governance/decisions.json                         408e0f611c7006a1c0fbb29854ff82ff6931510b6a3d25f2ea3cbc441455acf7
커밋                                                  add4951e44a03bb83d34523951801ced632a42bf   (원격 있음 · 생성 트리 = 이 커밋, clean)
selftest                                             생성기 ✔ 632 (BE 시점 605) · 배포 분석기 390/390 · runner e2e 12/12
verify_zip                                           PASS · rc 0 · 잡 16
check_governance (번들)                               PASS — 원문 byte 재계산 포함
```

repo 해시는 `git show add4951e:<path>` 로 **커밋된 트리에서** 낸 것이고, 번들 `provenance`
의 생성기 SHA(`abedb61e…`)와 일치합니다. 위 네 db 해시는 번들 `governance/` 사본과 **같아야**
합니다 (§4) — 이것이 "사본과 manifest 를 함께 위조하는 경로" 를 리뷰어 쪽에서 닫는 대조입니다.

## 0. 무엇이 바뀌었고 무엇이 그대로인가

- 생성기의 **물리 입력 경로**(INCAR/POSCAR/KPOINTS 생성 · 16잡 · 셀 c 36.6551/40.6551 ·
  box20/24)는 이번 커밋에서 건드리지 않았습니다. 바뀐 것은 전부 **검증·봉인·판정 층**입니다.
  v28 과의 바이트 대조는 두 MANIFEST 의 `files_sha256` 중 잡 파일 항목으로 하실 수 있습니다
  (새 항목은 `governance/*.json` 4개만이어야 합니다).
- 생성 argv 는 v22~v28 과 같습니다 (`--out` 만 다름). `runs/sdcp_c12_2026_08_30/IDENTITY_v29.json`.

## 1. P0-1 — 추정량 네 키의 **의미**를 검사하고 fallback 을 없앴습니다

`_estimand_semantics_check(keys, jobs, man, label, want_role)` (analyze_results.py:6370).
네 키 각각에 대해 **기대 의미를 코드에 고정**하고 job.json 실물 + `manifest.planned` 선언
양쪽과 대조합니다:

| 키 | 요구 |
|---|---|
| `E_C_sdcp` / `E_C_control` | `kind=prospective_pose` · `fragment` 가 그 조각 · `role` = primary(pm1·net4) 또는 ALT 역할(pose_alt 봉인) · `seed` = 봉인의 `branch` · `vacconv` 아님 · `d3_twin_of` 아님 · `d3=on` · planned 에 있고 planned.meta 와 kind/fragment/role/seed/basin_id 일치 |
| `E_G_sdcp` / `E_G_control` | 키 이름이 정확히 `refs/mol__<frag>__box24` · `kind=mol_ref` · `box_margin_A=24` · `fixed_geometry_static=true` · planned 일치 |
| 봉인 자체 | `branch` 필수 · pm1 봉인은 `branch == afm2424_pm1` |

- 이 검사는 `estimand_topology` 자리에서 **다른 블록 유무와 무관하게 항상** 돌아 block 을
  기록하고(:6370 정의 · 호출은 `estimand_semantics` 검색), exact-key 대입 직전에 그 결과로
  **대입을 거부**합니다. 어긋나면 `ESTIMAND_SEMANTICS(...)` · `NO_VALUE` · D 는 만들어지지
  않습니다 (대체하지 않습니다).
- **fallback 폐지**: `estimand_job_keys` 가 없으면 조각별 최솟값으로 전환하지 않고
  `ESTIMAND_KEYS_ABSENT` → `NO_VALUE` (:7480). "map 을 없애면 다른 estimand 로 자동 전환" 경로가
  사라졌습니다.
- 민감도 봉인(net4·pose_alt)도 같은 검사를 받되 값이 아니라 **status** 가 막힙니다
  (`unavailable` + 사유 `SEMANTICS:…`); D_pm1 은 영향받지 않습니다.
- k 수렴 쌍 결박(§2)이 같은 공격에서 함께 발화합니다 — 키를 바꾸면 `kconv_pair` 가 primary
  두 키와 달라지기 때문입니다.

**회신 BE 의 네 공격을 selftest 로 그대로 재현했습니다** (`python3 analyze_results.py --selftest`
출력에서 `⛔음성 BE P0-1` 검색 — 기본 픽스처는 이제 실물 모양: 네 키 봉인 · POSCAR 실물 루트 ·
stress_sensitivity 대안 자세 잡이 planned/jobs 에 **상주**, 공격은 **manifest 키만** 바꿈):
`두 complex 키 교환` · `gas reference 교환` · `gas 자리에 nzmag canary` · `gas 자리에 box20` ·
`봉인에 branch 없음` · `pm1 봉인의 branch 가 net4` · `SDCP complex 를 stress_sensitivity 잡(b12)으로 교체`
→ 전부 `ESTIMAND_SEMANTICS` · `NO_VALUE` · `primary_ddE_lowE_eV` 없음. 양성(봉인대로)은 D=−0.5 로 나옵니다.

## 2. P0-2 — vac·gas·k 를 좌표·셀·exact key 에 결박했습니다

**Vacuum** (`closure_vacconv`, 블록 `VACCONV_C1_NOT_PRIMARY` :3134 · `VACCONV_GEOMETRY_MISMATCH` :5750):
① c1 은 `estimand_job_keys` 의 **그 잡**(exact key)이어야 하고 ② c1/c2 POSCAR **실물**의
원소·개수·고정 플래그·Cartesian 좌표가 같아야 하고(`poscar_set_c` 가 좌표를 보존하므로 그것이
근거) ③ a,b 벡터는 같고 c 만 `vacuum_convergence.c2_A − c1_A` 만큼 달라야 합니다. 실물을 못
읽으면 `VACCONV_GEOMETRY_UNVERIFIED` — 확인 못 한 것은 통과가 아닙니다.
selftest: `c2 가 다른 자세(원자 0.5 Å 이동)` · `c2 셀이 Δc 만큼 크지 않음(같은 셀)` ·
`c1 이 사전 고정 complex 가 아님` · `실물 없음` → 전부 `pass=False`.

**Gas** (`_gas_bytes_check` :6467 + 계약 필드): 선언에서 `gas_placement == com_at_cell_center` ·
`box_margin_A` 가 20/24 정확히, 그리고 POSCAR 실물에서 **셀 대각 축마다 정확히 +4.0 Å** ·
**모든 원자 좌표가 정확히 +2.0 Å 강체 평행이동**(= 같은 내부기하 · COM 이 두 셀 중앙) · 원소
순서·개수 동일. 하나라도 어긋나면 `GAS_PAIR_CONTRACT` 이고 `gas_box_delta.pass=False`.
selftest: `box20/24 가 실물에서 같은 셀` · `+2.0 Å 강체이동 아님` · `gas_placement=not_centered` ·
`box24 잡의 box_margin_A≠24` · `실물 없음` → 전부 위반.

**k** (:7040): `kconv_pair.jobs` 집합이 `{E_C_sdcp, E_C_control}` 와 **정확히 같아야**
합니다. 아니면 `KCONV_PAIR_NOT_PRIMARY`(scope=estimand) — 대안 자세의 δ_k=0 으로 primary 를
"안정" 이라 하지 않습니다. selftest: `kconv_pair 를 대안 자세로` → `kconv_delta` 없음 · NO_VALUE.

## 3. P0-3 — 루트 `.SELFTEST_FIXTURE` 우회를 없앴습니다

- `run_staged.sh:168` — 픽스처 판정은 **`MANIFEST.selftest_fixture is True` 그리고 마커** 둘 다
  (run_job.sh 와 같은 규칙). production MANIFEST 에 그 필드를 심으면 해시가 바뀌어 EXPECT·봉인
  대조가 깨집니다.
- `census.py:13` — 선언 없는 마커(루트 또는 잡 폴더)를 **거부**합니다.
- e2e 하네스는 이제 MANIFEST 에 선언을 심고, 음성 두 건을 지킵니다: `선언 없는 마커 → census 거부` ·
  `마커 없는 선언 → 거버넌스 preflight 가 돈다(dirty 트리라 거부)`.

**번들에서 직접 재현한 결과** (v29 사본에 `touch .SELFTEST_FIXTURE`):
```
census.py 1        → ⛔ 시험 마커가 있는데 MANIFEST 가 selftest_fixture 를 선언하지 않았다 ['.SELFTEST_FIXTURE'] … (BE P0-3)   rc 1
run_staged.sh 1    → 같은 문구로 실행 전 census 실패 — 중단                                                          rc 2
```

## 4. P0-4 — 단일 provenance registry + 거버넌스 **원문 byte 재계산**

- 생성기: protocol · prereg · decisions.json 읽기가 전부 `_prov_note`(registry)를 거칩니다.
  v29 `provenance`: `clean=true · n_files 17 · 입력 13` — 입력에
  `db/properties/sdcp_c12_protocol_2026_08_30.json` · `sdcp_c12_claim_prereg_2026_08_31.json` ·
  `c12_poses_2026_08_30.json` · `db/governance/decisions.json` 이 **들어 있습니다** (v28 은 10 · 셋 누락).
- 번들 `governance/` 에 원문 사본 4개를 싣고 `files_sha256` 에 결박, `governance_binding.bundled_sources`
  로 경로를 선언합니다.
- 분석기 `governance_bytes_check(man)` (:1234) 가 사본에서 **다시 계산**해 manifest 주장과
  항목마다 대조합니다: 참조 문서 sha ↔ `reference_files_sha256` · claim 문서의
  `ratified/digest_matches/superseded/has_ratification_record/status` ↔ `ref_doc_state(원문)` ·
  decision 의 `digest`·`recorded_digest`·`state`·`ratified` ↔ `dec_digest(원문)`·원문 ratification.
  하나라도 어긋나면 차단. `--check_governance`(preflight)와 `citation_status`(최종) **둘 다** 부릅니다.
  사본이 없거나 `bundled_sources` 가 없으면 확인 못 한 것 = 차단.
- **판독기는 사본이 아니라 같은 소스입니다**: 생성기의 `GOV_CORE_SRC` 문자열 하나를 생성기는
  `exec` 하고 분석기 템플릿에는 그대로 삽입합니다 (`ref_doc_state` :34 · `dec_digest` :27 —
  분석기 안에 정확히 한 벌). 확인:
  ```
  python3 - <<'PY'
  import importlib.util, sys; spec = importlib.util.spec_from_file_location("g", "tools/sdcp/vasp_handoff_bundle.py")
  m = importlib.util.module_from_spec(spec); sys.argv = ["x"]; spec.loader.exec_module(m)
  print("GOV_CORE 동일:", m.GOV_CORE_SRC in open("analyze_results.py", encoding="utf-8").read())
  PY
  ```
- selftest (`⛔음성 BE P0-4`): `manifest 는 ratified=True 인데 원문은 proposed` · `decision 원문 내용
  변경(기록 digest ≠ 재계산)` · `bundled_sources 없음` · `manifest superseded 주장이 원문과 어긋남` ·
  `원문 사본 sha ≠ manifest 기록` → 전부 `manuscript_citable=False`. 픽스처 자체를 **원문 byte 에서**
  만듭니다 (장난감 digest "a"*64 폐기).

## 5. P1

- **J_f**: 조각당 primary 자세가 1개면 `pose_basin_interaction[f] = {"판정": "not_measurable",
  "J_f_meV": None}` (:6857) — 구조적 0 을 "range 가 작았다" 로 내지 않습니다.
- **종료코드**: 분석기 rc **3** = 계산 완주·원고 인용 불가(탐색용, `manuscript_citable=false`)
  (:9216), rc 2 = 판정 실패. `run_staged.sh:417` 이 3 을 2 와 구분해 안내하고 exit 3.
  README/SUBMIT 문구 갱신. post_hoc 정책 묶음은 완주하면 **3** 으로 끝납니다 — 실패가 아닙니다.
- **phase-local POTCAR 결박**: run_job.sh 가 `cp POTCAR "$ph/"` 직후 그 사본의 sha256 을 재서
  receipt **9열** `potcar_sha256` 으로 남기고(run_job.sh:233), 분석기가
  `POTCAR_PROVENANCE.assembled_sha256` 과 대조합니다 (`RECEIPT_POTCAR_MISMATCH` :3366 ·
  `RECEIPT_POTCAR_SHA_MISSING` · 8열 행은 이제 `RECEIPT_MALFORMED` :4746). 헤더행의 9열은 `-`.

## 6. 이 판이 **못 하는 것** (숨기지 않습니다)

- 의미 검사는 job.json meta 가 **거짓으로 적혀 있으면** 못 잡습니다 — 그것은 `files_sha256` 과
  POSCAR/INCAR 실물 대조의 몫입니다 (배포 파일 115개 전수 해시).
- `governance/` 사본과 manifest 를 **함께** 위조하면 분석기는 못 잡습니다. 그 경로는 위 표의
  db 해시 ↔ 사본 해시 대조(리뷰어)가 닫습니다. 분석기가 우리 repo 를 직접 읽는 설계는 하지 않았습니다
  (외주 기계에 repo 가 없습니다).
- POTCAR 신원은 여전히 post_hoc — 이 묶음 결과는 원고 인용용이 아니고 rc 3 으로 끝납니다.
- 0.01 eV overall 인용 자격은 ENCUT 수렴 설계가 없어 이 번들에서는 영영 `None` 입니다.

## 7. 재현 명령

```
python3 tools/sdcp/vasp_handoff_bundle.py --verify_zip sdcp_c12_v29.zip --expect_jobs 16
cd sdcp_c12_v29
python3 analyze_results.py . --check_governance          # 원문 byte 재계산 포함 · rc 0
python3 analyze_results.py --selftest                    # 390/390 · '⛔음성 BE' 검색
cp -r . ../v29_marker && (cd ../v29_marker && touch .SELFTEST_FIXTURE && \
  EXPECT_MANIFEST_SHA256=$(sha256sum MANIFEST.json | cut -c1-64) EXPECT_ZIP_SHA256=$(printf '0%.0s' $(seq 64)) \
  BUNDLE_ZIP_SHA256=$(printf '0%.0s' $(seq 64)) python3 census.py 1)   # rc 1 · BE P0-3 문구
for f in governance/*.json; do sha256sum "$f"; done      # 위 표의 db 해시와 같아야 한다
```
회신 BE 의 합성 에너지 공격(키 교환·교체)은 MANIFEST 의 `estimand_job_keys` 를 그대로 고쳐
`analyze_results.py .` 를 돌리시면 됩니다 — `ESTIMAND_SEMANTICS` 블록과 `NO_VALUE` 가 나와야
하고, `RESULTS.json` 에 `primary_ddE_lowE_eV` 가 없어야 합니다.

## 8. 질문

- Q1. 원문 byte 재계산을 **번들 안 사본**에서 하고 repo 원본 대조는 리뷰어 몫으로 두는 설계가
  "governance 를 원문 byte 에서 재계산" 요구를 충족합니까? 아니면 분석기가 사본과 manifest 를 넘어
  **외부 anchor**(예: 메일 본문의 db 해시)를 EXPECT 처럼 요구해야 합니까?
- Q2. rc 3(완주·인용 불가)을 러너가 "실패 아님" 으로 안내하는 것이 문서 의미와 맞습니까?
- Q3. gas 강체이동·셀 차 허용오차 1e-4 Å, 진공 좌표 허용오차 1e-4 Å — 더 조여야 합니까?

**파일은 수정하지 않으셔도 됩니다 — GO/NO-GO 와 P0/P1 판정만 주십시오.**
