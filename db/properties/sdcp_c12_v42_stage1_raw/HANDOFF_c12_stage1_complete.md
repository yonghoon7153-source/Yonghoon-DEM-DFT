# sdcp_c12_v42 — **1단계 완료 회신** (12/12 잡 · 게이트 통과 · STAGE1_PASS.json)

수행 측(mirae) 2026-09-30. 번들 **v42** (zip sha256 `9a3976b8b13a7a6e…` · MANIFEST `a2e3e820a2767573…`) 을 새 extraction 에 풀고
§1′ 승계 경로(`SKIP_COMPLETE=1` + `CONTINUE_FROM=<v41 extraction>`)로 `run_staged.sh 1` 을 **완주**했습니다.
러너 판정: `✅ 1단계 통과 — STAGE1_PASS.json 기록 · 2단계 제출 가능` (2026-09-30 09:25 KST, rc=0).
이 tgz 는 extraction 을 **통째로** 압축한 것(POTCAR·CHGCAR·WAVECAR 등 제외)이라 앞서 보낸 부분 회신 4종을 대체합니다.

## 1단계 게이트 (러너 출력 그대로)
```
■ stage gate = vacconv · ok — Δ_vac -0.6 meV (문턱 5) · 반올림 일치
   ✓ vacuum          Δ_vac = -0.632 meV
   ✓ molecular_state 비영 시작이 부모보다 낮지 않다
   ✓ canary_geometry 부모/canary static 기하 동일 (2조각)
   ✓ potcar_identity sealed_root_v13 · 완주 전 잡이 봉인과 일치
   ✓ gas_box_delta   delta_gas_meV = -0.086 (tol 5.0)
   ✓ estimand_topology_pm1 두 complex 가 같은 자기 branch
   ✓ closure_blocks_clear · ✓ root_seal_covers_plan
=== 무결성 ===  검사 129개 · 변경 0 · 없음 0
```
잡 게이트 "통과 12/19 · 문제 7건" 의 7건은 전부 **2단계 잡 NOT_RUN** (아직 안 돌린 것) — 1단계 판정에는 영향 없음.

## 결과 — 12잡 전부 EDIFF 도달 · General timing · NELM 200 미달

| 잡 | 원자 | 스텝 | 벽시계 | TOTEN F (eV) | 총자화 (μB) | 실행 |
|---|---|---:|---:|---|---:|---|
| `prospective/ptfe_c10__b00__afm2424_pm1` | 224 | 95 | 31.9 h | −1123.59334 | 0.0004 | v41 → 승계 |
| `prospective/sdcp_neutral__b00__afm2424_pm1` | 227 | 106 | 34.1 h | −1151.29228 | 0.0801 | v41 → 승계 |
| `refs/clean_slab__afm2424_pm1` | 192 | 95 | 29.6 h | −944.94774 | 0.0001 | v41 → 승계 |
| `refs/mol__ptfe_c10__box20` | 32 | 38 | 11 min | −177.85487 | 0.0000 | v41 → 승계 |
| `refs/mol__ptfe_c10__box24` | 32 | 42 | 20 min | −177.85500 | 0.0000 | v41 → 승계 |
| `refs/mol__sdcp_neutral__box20` | 35 | 57 | 12 min | −205.38963 | 0.0000 | v41 → 승계 |
| `refs/mol__sdcp_neutral__box24` | 35 | 63 | 21 min | −205.38985 | 0.0000 | v41 → 승계 |
| `vacconv/clean_slab__afm2424_pm1__c2` | 192 | 100 | 33.8 h | −944.94787 | 0.0001 | v42, n40 |
| `vacconv/ptfe_c10__b00__afm2424_pm1__c2` | 224 | 76 | 44.0 h | −1123.59261 | 0.0000 | v42, n40 |
| `vacconv/sdcp_neutral__b00__afm2424_pm1__c2` | 227 | 131 | 54.4 h | −1151.29218 | 0.0097 | v42, n40 |
| `refs/mol__ptfe_c10__box24__nzmag` | 32 | 35 | 0.3 h | −177.85496 | 0.0000 | v42, n40 |
| `refs/mol__sdcp_neutral__box24__nzmag` | 35 | 62 | 0.4 h | −205.38985 | 0.0000 | v42, n40 |

(F 는 `STAGE1_PASS.json` 의 `stage1_energies_eV` 와 OSZICAR 마지막 줄 기준.)

관찰 (판단은 맡깁니다):
- 진공 36.66 → 40.66 Å: clean slab −0.13 meV · PTFE 복합체 +0.73 meV · SDCP 복합체 +0.10 meV → Δ_vac −0.6 meV.
- nzmag(비영 시드·NUPDOWN 해제)가 두 분자 모두 총자화 0 으로 붕괴, 에너지는 부모 대비 PTFE +0.04 meV · SDCP +0.00 meV → 닫힌껍질 일중항이 바닥.
- SDCP 복합체 c1 총자화 0.080 μB, c2 0.010 μB (pm1 시드 기대 ≈ 0) — 잔류 모멘트 작지만 0 은 아님.

## 실행 조건
- mirae SGE, `64core.q` **노드 1개** (64코어 Xeon Gold 6530×2 · RAM 503 GB · cgroup 상한 없음 · `h_rt=INFINITY`), `VASP_NPROC=64` · `VASP_NODES=1` · `NODE_MEM_GB=500` · `JOBS_PARALLEL=1`, Intel MPI 2021.6 (`-f/-ppn 64`)
- VASP 5.4.4.18Apr17-6-g9f103f2a35 (sha `f1eee9acd5f7…`), POTCAR potpaw_PBE.54 (`POTCAR_ROOT_SEAL.json` · 잡별 `POTCAR_PROVENANCE.json`), attestation 없음(post_hoc)
- v42 실행: SGE 잡 125185, 2026-09-24 20:30 → 09-30 09:25 KST (133 h 연속). 승계 7잡 전부 "입력 6 동일 확인" (`CONTINUATION.json`: 승계 7 · 미승계 5 · 이전 MANIFEST `fd5e4488cc09`). 잡 maxvmem 294 GB.
- 실측 s/전자스텝: 슬랩급 c1 1098~1261, c2(진공 +4 Å) 1216~2084. 기체 잡 30~60 s.
- v41 extraction(`~/projects/sdcp_c12_v41_2026_09_11/sdcp_c12_v41`)은 지시대로 **그대로 보존** 중.

## 동봉 — extraction 통째 (반송 계약 그대로)
```
sdcp_c12_v42/
├── HANDOFF_c12_stage1_complete.md  (이 문서)
├── MANIFEST.json · POTCAR_ROOT_SEAL.json · ZIP_SHA256.txt · PLACEMENT_PROBE.json · CONTINUATION.json
├── RESULTS.json · STAGE1_PASS.json
├── RUN_LOG_stage1.log  (러너 stdout 전체)
├── governance/ · analyze_results.py · census.py · run_staged.sh · SEAL_POTCAR_ROOT.sh · MAKE_POTCAR_ATTESTATION.sh · README·SUBMIT_CONTRACT·POTCAR_SPEC 등 (받은 그대로)
└── 19잡 폴더 전부 (job.json · run_job.sh · POTCAR_ASSEMBLE.sh · POSCAR · POTCAR_PROVENANCE.json · EXECUTABLE_RECEIPT.tsv · _placement.tsv)
    ├── 1단계 12잡: static/ INCAR KPOINTS POSCAR CONTCAR OSZICAR OUTCAR.gz vasp.out IBZKPT PCDAT XDATCAR REPORT
    └── 2단계 7잡: static/ INCAR KPOINTS (미실행)
```
제외: **POTCAR (라이선스)**, CHG · CHGCAR · WAVECAR · PROCAR · DOSCAR · EIGENVAL · vasprun.xml (용량 — 서버 보존, 요청 시 전송). OUTCAR 는 gzip.

## 다음
2단계 7잡(`bash run_staged.sh 2`)은 귀측 1단계 판정을 받은 뒤 시작하겠습니다. 같은 조건(1노드 64랭크 직렬)이면 약 9~10일, 4노드/잡이면 3~4일 — 지시해 주십시오.
