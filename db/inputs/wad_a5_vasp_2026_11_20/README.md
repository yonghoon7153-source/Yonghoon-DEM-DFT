# W_ad a5 — 은 쪽 G4 ENCUT 650 분리 끝점 재시도 (개정 5 v2)

- 묶음 MANIFEST sha256: `026abb2d5a97c9db228ff34e96f8afcfa3bdbb730ac7f3e6a1eeba7dddc9ca44` (받은 뒤 `sha256sum MANIFEST.sha256` 로 같은지 확인)
- 잡: `V5_s_outer_A_G4_e70_far_a5` 하나 · 사다리 ⓪ 확인 → A5 (A5c 이어서 · A5f 새로) → c1 → c1 이 주 기준 OK 가 아니면 c2 · A5 자격 미달이면 c1 · c2 는 ⓪ 복사본에서 · ⓪ 도 없으면 값 없음
- 누적 상한 180 h (넘으면 다음 단을 띄우지 않고 멈춘다) · 0 스텝 인프라 중단은 잡 전체 2 회

## 돌리는 법
```
W0_WAVECAR=<외주 2차 묶음>/run/V5_s_outer_A_G4_e70_far_a4_a4/stageA/WAVECAR \
VASP_CMD="mpirun -np 64 vasp_std" POTCAR_DIR=<PAW_PBE 폴더> [PERF_TAGS_FILE=<성능 태그 파일>] bash run_a5.sh
```
- 보존된 a4 ⓐ WAVECAR 가 없으면 `W0_WAVECAR=none` 을 적는다 (A5 가 새로 시작한다). 원본은 읽기만 한다 (복사본만 쓴다).
- 다 끝나면 `a5_return.tgz` 와 `a5_return.tgz.sha256` 을 보낸다 (`sha256sum -c a5_return.tgz.sha256` 통과 뒤). WAVECAR · CHGCAR · POTCAR 본문은 담지 않는다.
- 종료 0 c1 또는 c2 수렴 · 1 주 기준 값 없음 (그대로 반송 — 실패도 기록) · 2 인자·패키지 오류 · 4 포장 실패 (`PACK_ONLY=1 bash run_a5.sh`) · 5 누적 상한 · 벽시계 미상 · 6 공통 환경 고장
- 0 스텝 인프라 중단: `bash run_a5.sh --infra-abort <A5|c1|c2> <스케줄러 잡 id> <취소 UTC> <사유>` · 끊긴 시도: `WALL_S=<초> bash run_a5.sh --killed <단> <id> <UTC> <사유>`
- INCAR · POSCAR · KPOINTS 를 고치지 마세요. 시도 폴더가 있으면 덮어쓰지 않습니다 (다시 돌리면 기록을 다시 판정해 다음 단을 정합니다).
