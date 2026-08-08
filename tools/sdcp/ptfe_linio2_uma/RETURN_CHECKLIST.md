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
