# sdcp_c12_v41 — 1단계 **부분 회신** (완료 잡 2개 · 실측 샘플)

수행 측(mirae) 2026-09-15. 번들 v41 (zip sha256 `76d76d50e4daeb5f…` · MANIFEST `fd5e4488cc097af9…`) 을
**그대로** 풀어 `run_staged.sh 1` 로 실행하다가, 1단계 12잡 중 **2잡이 완료된 시점에 운영상 판단으로 러너를 멈췄습니다.**
귀측이 "먼저 한 잡만 재 보시길" 권한 실측 샘플로 보시면 됩니다. 나머지 10잡은 실행하지 않았고(3번째 잡은
qdel 직후 0스텝에서 죽어 산출물 없음), 재개 불가 계약이라 **재실행은 새 extraction·잡1부터** 합니다.
따라서 `RESULTS.json`·`STAGE1_PASS.json` 은 없습니다 (러너가 판정 단계에 도달하지 않음).

## 결과

| 잡 | 원자 | 전자스텝 | 벽시계 | 종료 | TOTEN F (eV) | E0 (eV) | 총자화 (μB) |
|---|---|---:|---:|---|---|---|---:|
| `prospective/ptfe_c10__b00__afm2424_pm1` | 224 | 95 | 31.9 h | EDIFF 도달 · General timing | −1123.5935 | −1123.5933 | 0.0004 |
| `prospective/sdcp_neutral__b00__afm2424_pm1` | 227 | 106 | 34.1 h | EDIFF 도달 · General timing | −1151.2978 | — | 0.0801 |

- 둘 다 NELM=200 미달로 정상 수렴. 입력(INCAR·KPOINTS·POSCAR)은 손대지 않았습니다.
- `static/POSCAR` = 실행된 기하 (받은 그대로, NSW=0 이라 CONTCAR 와 동일).

## 실행 조건 (귀측 §0 질문에 대한 실측 답 포함)

- SGE 잡 123690, `64core.q@n33` **노드 1개** (물리코어 64 · Xeon Gold 6530 ×2 · RAM 503 GB · cgroup 메모리 제한 없음)
- `VASP_NPROC=64` · `VASP_NODES=1` · `NODE_MEM_GB=500` · `JOBS_PARALLEL=1` · `VASP_LAUNCHER_KIND=mpirun` (Intel MPI 2021.6, hydra `-f/-ppn 64`)
- 러너 사전검사 전부 통과: 메모리 게이트 177/425 GB (42 %), 배치 프로브 (`PLACEMENT_PROBE.json`), census 129파일, 거버넌스, POTCAR 19잡 봉인
- VASP 5.4.4.18Apr17-6-g9f103f2a35 (sha `f1eee9acd5f7…`), POTCAR potpaw_PBE.54 (`POTCAR_ROOT_SEAL.json`·잡별 `POTCAR_PROVENANCE.json`)
- 실측 s/전자스텝: 잡1 **1209**, 잡2 **1261** (64랭크·1노드). 참고로 192랭크·48코어 노드 4개에서는 682 s (2026-09-08 프로브)
- 실측 메모리: SGE 잡 maxvmem **268 GB** (노드 1개 · 잡 1개). 귀측 모형 177 GB 보다 1.5배 큽니다
- 큐: `h_rt=INFINITY` (walltime 상한 없음). "잡당 91 h" 는 저희가 드린 값이 아닙니다

## 동봉 파일

```
sdcp_c12_v41/
├── HANDOFF_c12_partial.md          (이 문서)
├── MANIFEST.json                   (받은 그대로)
├── POTCAR_ROOT_SEAL.json
├── ZIP_SHA256.txt
├── PLACEMENT_PROBE.json
├── RUN_LOG_stage1.log              (러너 stdout 전체 · qdel 시각 포함)
└── prospective/
    ├── ptfe_c10__b00__afm2424_pm1/
    │   ├── job.json  EXECUTABLE_RECEIPT.tsv  POTCAR_PROVENANCE.json  _placement.tsv
    │   ├── run_job.sh  POTCAR_ASSEMBLE.sh  POSCAR          (받은 그대로)
    │   └── static/  INCAR  KPOINTS  POSCAR  CONTCAR  OSZICAR  OUTCAR.gz  vasp.out
    └── sdcp_neutral__b00__afm2424_pm1/   (동일 구성)
```

제외: **POTCAR (라이선스)**, CHG·CHGCAR·WAVECAR·PROCAR·DOSCAR·EIGENVAL·vasprun.xml (용량 — 서버에 보존 중, 필요하시면 보냅니다).
나머지 17잡 폴더는 입력만 있는 상태라 넣지 않았습니다.

## 참고
- 잡2 총자화 0.08 μB (pm1 시드 기대값 ≈ 0) — 판단은 맡깁니다.
- 1노드 직렬로 1단계를 완주하면 ≈2주가 걸립니다. 그 사이 정전·장애가 오면 재개 불가라 전부 다시 돕니다 (2026-09-11 에 실제로 한 번 겪었습니다).
  완료된 잡 사이에서 이어갈 수 있는 모드가 있으면 알려 주십시오. 없으면 저희는 4노드/잡(192랭크) 배치로 단계를 짧게 끝내는 쪽을 검토합니다.
