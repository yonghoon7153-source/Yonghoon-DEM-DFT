# Return checklist

Pilot 뒤 먼저 회수:

- `logs/pilot.log`
- `uma-s-1p1_oc20/PILOT.json`
- `nvidia-smi` 출력

전체 screen 뒤 회수:

- `logs/screen.log`
- `uma-s-1p1_oc20/PLAN.json`
- `uma-s-1p1_oc20/references.json`
- `uma-s-1p1_oc20/rigid_poses.csv`
- `uma-s-1p1_oc20/RELAX_SHORTLIST.csv`
- `uma-s-1p1_oc20/relaxed_poses.csv`
- `uma-s-1p1_oc20/RESULTS.md`
- `uma-s-1p1_oc20/MODEL_CACHE_MANIFEST.sha256`
- `uma-s-1p1_oc20/MODEL_CACHE_SYMLINKS.tsv`
- `uma-s-1p1_oc20/DFT_HANDOFF.csv` + `DFT_HANDOFF.json`
- `uma-s-1p1_oc20/DFT_HANDOFF/`의 재정렬된 XYZ/POSCAR 쌍
- `uma-s-1p1_oc20/relaxed_structures/`의 `.xyz` + `.vasp` 쌍과 `.traj`
- `uma-s-1p1_oc20/rigid_records/` 및 `relaxed_records/` JSON 전부
- 결과 tarball의 SHA-256

결과를 받은 뒤 확인할 항목:

1. 147/147 rigid와 20/20 relax 완료 여부
2. 미수렴·이미지 경고·bond-change 격리 수
3. initial site와 post-relax multi-F registry가 같은지
4. dimer H-cap artifact 제외 여부
5. C10과 dimer 각각 eligible relaxed 후보가 최소 3개 이상이고, proxy 라벨과 무관하게 후보 20개 전부를 사람이 구조 감사했는지
6. 0.05 eV를 calibrated uncertainty처럼 오해하거나 그 밖을 확정 순위로 읽지 않았는지
7. VASP+D3에 넘길 구조 다양성
8. matched Li-top/Ni-top pair가 fragment별로 있고 azimuth·roll이 같은지
9. handoff POSCAR 종 순서, bottom-half-fixed mask, VASP 1-based contact index를 눈으로 확인했는지
10. handoff XYZ/POSCAR SHA-256과 `PACKAGE_COMMIT.txt`가 반환물 계보와 일치하는지

VASP 입력 생성 뒤 확인:

- `vasp_pilot/VASP_PLAN.json`: 18 templates / 36 relax+static executions
- `vasp_all/VASP_PLAN.json`: 20/20 eligible이면 54 templates / 108 executions;
  일부 격리 시 `14 + 2 x eligible_relaxed_count`와 handoff 행 수가 일치하는지
- `VASP_INPUT_MANIFEST.sha256` 검증 통과
- `UPSTREAM_DFT_HANDOFF.json`, full source SHA-256, `PACKAGE_COMMIT.txt` 포함
- 모든 complex가 34.6 Å 공통 c축, 종 순서 `Li Ni O C F H`, fixed atoms 96인지
- molecule은 Gamma + `IDIPOL=4`, surface는 `2x3x1` + `IDIPOL=3`인지
- `INCAR.dense`가 `ISTART=0, ICHARG=1`이고 `KPOINTS.dense=3x4x1`인지

VASP 계산 뒤에는 생성 폴더의 `VASP_README_KO.md` 반환 목록을 따르고,
`bash vasp_run.sh archive-final`이 만든 tarball을 그대로 회수해.
각 phase의 `RUNTIME_METADATA.txt`에서 POTCAR SHA-256/TITEL, host, 실행 명령과
상속 WAVECAR/CHGCAR 해시를 확인하고, `VASP_ANALYSIS.json`의
`numeric_claim_gates_all_passed`를 archive 생성 여부와 별도로 읽어.
