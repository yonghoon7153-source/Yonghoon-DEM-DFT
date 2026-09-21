# sdcp_c12_v41 — 1단계 부분 회신 **통합본** (완료 7잡 / 19잡)

수행 측(mirae) 2026-09-21. 앞서 세 번에 나눠 보낸 부분 회신(09-15 prospective pm1 2잡 · 09-18 기체 4잡 · 09-20 clean slab pm1 1잡)을
**하나로 합친 것**입니다. 이 tgz 하나면 됩니다. 전부 **같은 extraction** (v41 zip sha256 `76d76d50e4daeb5f…` · MANIFEST `fd5e4488cc097af9…`)
에서 나왔고, 입력(INCAR·KPOINTS·POSCAR)은 손대지 않았습니다.

## 결과 — 7잡 전부 EDIFF 도달 · General timing · NELM 200 미달

| # | 잡 | 원자 | 스텝 | 벽시계 | TOTEN F (eV) | 총자화 (μB) | 실행 |
|---|---|---|---:|---:|---|---:|---|
| 1 | `prospective/ptfe_c10__b00__afm2424_pm1` | 224 | 95 | 31.9 h | −1123.5935 | 0.0004 | 09-12~13, n33 |
| 2 | `prospective/sdcp_neutral__b00__afm2424_pm1` | 227 | 106 | 34.1 h | −1151.2978 | 0.0801 | 09-13~15, n33 |
| 3 | `refs/clean_slab__afm2424_pm1` | 192 | 95 | 29.6 h | −944.94774 | 0.0001 | 09-18~20, n35 |
| 4 | `refs/mol__ptfe_c10__box20` | 32 | 38 | 11 min | −177.85487 | 0.0000 | 09-18, n33 |
| 5 | `refs/mol__ptfe_c10__box24` | 32 | 42 | 20 min | −177.85500 | 0.0000 | 09-18, n33 |
| 7 | `refs/mol__sdcp_neutral__box20` | 35 | 57 | 12 min | −205.38963 | 0.0000 | 09-18, n33 |
| 8 | `refs/mol__sdcp_neutral__box24` | 35 | 63 | 21 min | −205.38985 | 0.0000 | 09-18, n33 |

(# 는 러너의 1단계 사전순 번호. 기체 box20↔box24 차 0.1~0.2 meV.)

## 실행 조건 (공통)
- mirae SGE, `64core.q` **노드 1개** (물리코어 64 · Xeon Gold 6530 ×2 · RAM 503 GB · cgroup 메모리 제한 없음 · `h_rt=INFINITY`)
- `VASP_NPROC=64` · `VASP_NODES=1` · `NODE_MEM_GB=500` · `JOBS_PARALLEL=1` · `VASP_LAUNCHER_KIND=mpirun` (Intel MPI 2021.6, `-f/-ppn 64`, `I_MPI_JOB_RESPECT_PROCESS_PLACEMENT=0`)
- VASP 5.4.4.18Apr17-6-g9f103f2a35 (sha `f1eee9acd5f7…`) · POTCAR potpaw_PBE.54 (`POTCAR_ROOT_SEAL.json` · 잡별 `POTCAR_PROVENANCE.json`) · attestation 없음(post_hoc)
- 러너 사전검사 매 패스 통과: 메모리 게이트 177/425 GB (42 %) · 배치 프로브 · census 129파일 · 거버넌스 · POTCAR 봉인
- 실측: 슬랩급 **1098~1261 s/전자스텝**, 잡 maxvmem **239~268 GB** (귀측 모형 177 GB 의 1.35~1.5배). 기체 잡 79 GB

## 세 패스로 나뉜 경위 (receipt 에 그대로 보입니다)
`run_staged.sh 1` 을 같은 extraction 에서 세 번 실행했습니다. 러너는 이미 산출물이 있는 잡을 "⛔ 이미 산출물이 있습니다" 로 거부하고(receipt 손대지 않음) 다음 잡으로 넘어갑니다.
각 패스는 운영상 판단으로 원하는 잡이 끝난 시점에 `qdel` 했습니다. 로그 `RUN_LOG_stage1.log`(1·2) · `RUN_LOG_stage1_pass2.log`(4·5·7·8) · `RUN_LOG_stage1_pass3.log`(3) 에 전부 남아 있습니다.
- 잡 3 은 첫 qdel 직후 0스텝 찌꺼기가 남아 2차 패스에서 건너뛰어졌고, 찌꺼기(+core dump)를 지운 뒤 3차 패스에서 돌렸습니다.
- 각 패스에서 qdel 직후 다음 잡이 몇 초 기동했다 죽었습니다: `vacconv/clean_slab__afm2424_pm1__c2` 폴더에 `vasp.out` 만 남아 있고 OUTCAR 는 없습니다 (러너 stale 검사 대상 아님).

## 미실행 (12잡)
- 1단계: `refs/mol__ptfe_c10__box24__nzmag` · `refs/mol__sdcp_neutral__box24__nzmag` (6·9) · `vacconv/*` 3 (10~12)
- 2단계 7 (net4 계열 4 · b52/b12 pm1 2 · clean_slab net4)
- ⚠ **nzmag 2잡은 이 extraction 에서 러너로 돌릴 수 없습니다.** 러너가 `PARENT_GEOM` 잡을 2물결로 두고 **1물결 전부 성공**을 요구하는데, 완료 잡의 거부가 실패로 집계돼 2물결이 열리지 않습니다.
  부모(`box24`) 결과는 위에 있습니다. 완료 잡을 건너뛰는 **계획된 이어가기 모드**를 열어 주시거나, 새 extraction 으로 1단계 전체를 다시 돌려야 합니다 (완료 7잡 ≈ 97 h 낭비). **지시 부탁드립니다.**
- vacconv 3잡은 지금 상태에서 러너를 다시 띄우면 바로 돕니다 (잡당 ~30 h).
- `RESULTS.json` · `STAGE1_PASS.json` 은 러너가 판정 단계에 도달하지 않아 없습니다.

## 동봉 파일
```
sdcp_c12_v41/
├── HANDOFF_c12_stage1_partial7.md   (이 문서)
├── MANIFEST.json · POTCAR_ROOT_SEAL.json · ZIP_SHA256.txt · PLACEMENT_PROBE.json   (받은 그대로 / 러너 생성)
├── RUN_LOG_stage1.log · RUN_LOG_stage1_pass2.log · RUN_LOG_stage1_pass3.log
├── prospective/{ptfe_c10__b00__afm2424_pm1, sdcp_neutral__b00__afm2424_pm1}/
├── refs/clean_slab__afm2424_pm1/
└── refs/mol__{ptfe_c10__box20, ptfe_c10__box24, sdcp_neutral__box20, sdcp_neutral__box24}/
    각 잡: job.json  EXECUTABLE_RECEIPT.tsv  POTCAR_PROVENANCE.json  _placement.tsv  run_job.sh  POTCAR_ASSEMBLE.sh  POSCAR
           static/  INCAR  KPOINTS  POSCAR  CONTCAR  OSZICAR  OUTCAR.gz  vasp.out
```
제외: **POTCAR (라이선스)**, CHG·CHGCAR·WAVECAR·PROCAR·DOSCAR·EIGENVAL·vasprun.xml (용량 — 서버 보존, 요청 시 전송). 미실행 12잡 폴더는 입력만 있어 넣지 않았습니다.

## 참고
- 잡 2 총자화 0.08 μB (pm1 시드 기대 ≈ 0) — 판단은 맡깁니다.
- 큐 walltime 상한 없음. "잡당 91 h" 는 저희가 드린 값이 아닙니다.
