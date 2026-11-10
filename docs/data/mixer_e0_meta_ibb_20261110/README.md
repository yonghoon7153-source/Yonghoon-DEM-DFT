# 믹서 E0 자격 pilot — ibb 읽기 전용 메타 수집 (2026-11-10)

[DEM 우선 Ⓒ] 믹서 E0 자격 pilot 한 팔 준비의 1 단계.  ibb 의 링크 · OS · 권한 · 바이너리/MPI · 자원 · SLURM · 운영 전환 · first8 E0 자료를 **읽기만** 해서 모은 관측 메타다.
⛔ 자격 판정 · 실행 승인 · 발사 GO 가 아니다 (그 셋은 아래 "다음" 의 등록 · 내부 반박 리뷰 · 1저자 GO 뒤).

## 1. 블록

- `block/meta_block.txt` (541 줄) — 본문 스크립트를 셸 변수에 담고 마지막 줄이 md5 (4e01c25f8f3a1cebc9daee51e2999cc4) 를 대조한 뒤에만 `bash -c` 로 돈다.  한 글자라도 깨지면 아무것도 하지 않는다.  본문 사본 = `out/meta_script.sh` (같은 md5).
- 쓰는 곳 = ibb 새 폴더 `~/mixer_e0_meta_<UTC>/` 하나 (raw/ = 가리지 않은 원문 · out/ = 가린 사본 · tgz = out/ 만).  하지 않는 것 = 제출 · 취소 · 잡 제어 · 예약 · git 쓰기 · 지우기 · 옮기기 · conda / module 바꾸기 · 계산.  외부 명령은 전부 timeout 안 · 전체 상한 900 초 · 조회당 2 MB.
- 시험 (본 세션 scratch · 리포 밖): 컨테이너 가짜 HOME · 가짜 명령 · PID 이름공간 170 PASS · 0 FAIL (조수) · 본 세션 다시 170 / 0.  진짜 SLURM · LIGGGHTS · MPI · Lustre 에서는 시험하지 않았다.
- `block/read_meta_bundle.py` — 받은 tgz 를 빈 새 폴더에 안전하게 풀고 (절대경로 · `..` · 링크 · 장치 · out/ 밖 · 크기 상한 = 거부 · extractall 안 씀) `out/SHA256SUMS` 전수 · 스크립트 md5 를 대조해 요약한다 (`python3 -I`).

## 2. 1저자 결정 (11-10)

- Q1–Q4 *"권고대로해"*: Q1 실행 범위 승인 (ibb 로그인 셸 · 위 읽기 범위 · 900 초 · 조회당 2 MB) · Q2 `lmp_mpi -h` 켬 · Q3 SLURM 읽기 조회 켬 (sinfo · sacctmgr show · 내 squeue · scontrol 안 씀) · Q4 기준 바이너리 = 09-28 영수증 바이너리와 같으면 그것 · 다르면 멈추고 재빌드 여부 1저자.
- Q5–Q8 *"권고대로해"*: Q5 E0 pilot 런 폴더 = 발사 때 새로 (기존 dev7 폴더 안 씀 · 지금 안 만듦) · Q6 walltime · 디스크 문턱 · STOP 수치 = DEV E0 다섯 런의 실측 크기 · 시간으로 본 세션이 초안 → 결과 전 등록 (기본값으로 채우지 않음) · Q7 내부 반박 리뷰 = 이 블록 + 기준 고정 표 + 봉인 묶음을 실행 전에 한 번에 · Q8 반입 = 가린 사본 (out/) 만 이 새 증거 폴더에 (raw/ 반입 안 함).

## 3. 실행 · 반입

- 1저자가 ibb 에서 실행: 2026-11-10T14:49:56Z → 14:53:02Z (186 초).
- 묶음 `mixer_e0_meta_20261110T144956Z.tgz` = 66,769 B · sha256 e20cfd9d3027e937927c4a565bc55497e920e6fba4dc962b25740d4472d45266 (1저자가 함께 올린 `.tgz.sha256` 과 같음).
- 본 세션: `block/read_meta_bundle.py` 로 빈 새 폴더에 풀어 대조 = 구조 정상 (rc 0) · 스크립트 md5 같음 · `out/SHA256SUMS` 전수 같음 · 가림 뒤 남은 계정 · 호스트 · 경로 문자열 0 (블록 자체 확인) · 본 세션이 계정 이름 · 주소 · 포트를 따로 찾아도 0.
- `out/` = 묶음 안 가린 사본 그대로 (132 파일).  raw/ (가리지 않은 원문) 은 ibb 에만 있다 — `out/RAW_SHA256SUMS` 가 그 해시다.

## 4. 관측 (자격 판정 아님)

| 항목 | 값 | 파일 |
|---|---|---|
| 조회 | 140 개 = OK 127 · FAIL 13 | `out/probes.txt` |
| LIGGGHTS | 실제 파일 1 (ibb 의 LIGGGHTS-PUBLIC 빌드 폴더 src 의 lmp_mpi · 후보 123) · LIGGGHTS-PUBLIC 3.8.0 · 빌드 2026-03-26 · git 3d5c00f · sha256 ee2d77261bac9e7fa4e9311c8709e74bf7583a13225a5bc35a791bef9be60a3f = 09-28 영수증 바이너리와 같음 → Q4 = 이 바이너리 | `out/lmp1_help.txt` · `out/hashes.txt` · `out/fields.txt` |
| MPI | mpirun 실제 1 (conda env 의 mpirun · 후보 26) | `out/fields.txt` (mpi.candidate*) · `out/mpi1_version.txt` |
| SLURM | 내 잡 0 · QOS cpu-60 = 사용자당 cpu 60 · GPU 0 · 내 association 의 MaxWall 7-00:00:00 · cpu 파티션 시간 상한 14-00:00:00 (노드 4) | `out/slurm_squeue_me.txt` · `out/slurm_qos.txt` · `out/slurm_assoc_me.txt` · `out/slurm_sinfo_partitions.txt` |
| 디스크 | HOME = Lustre · 678T 중 515T 사용 · 130T 남음 (80 %) · 계정 할당 = 기본 (제한 0) · 사용 2,228,675,672 KB · 파일 543,500 | `out/df_home_human.txt` · `out/lfs_quota_home.txt` |
| 믹서 폴더 | 09-21 층상 runs 524,888 KB · dev7 63,444,400 KB · dev7_v26 90,504,844 KB (KB = `du -k`) | `out/mix1_du.txt` · `out/mix2_du.txt` · `out/mix3_du.txt` |
| first8 E0 | 제안 런 폴더 없음 (만들지 않았으니 정상 · Q5) | 요약 출력 |

- FAIL 13 은 해롭지 않은 것으로 본다 (관찰): 체크아웃 10 곳의 가지 이름 (`git` 가지 이름 명령 rc 1 · HEAD 는 따로 받음) · 정적 배너 (실행 파일 앞 8 KB 에 판 문자열이 없음) · `quota` (Lustre 라 `lfs quota` 로 따로 받았고 OK) · `lmp_mpi -h` 의 종료 코드 1 (도움말 9,033 B 는 정상 출력 · `-h` 가 원래 1 로 끝나는 것으로 봄 = 추정).

## 5. 다음

기준 고정 표 (바이너리 · MPI · SLURM · 디스크) + E0 pilot 등록 초안 (Q6 · walltime · 디스크 문턱 · STOP = DEV E0 다섯 런 (dev7_v26) 의 실측) → 결과 전 등록 → 내부 반박 리뷰 (Q7 · 블록 + 표 + 봉인 묶음) → 1저자 발사 GO.  (1저자 11-10 운영 결정 = 이 pilot 한 팔은 내부 반박 리뷰가 Codex GO 자리를 대신한다 · 발사 GO 는 1저자.)
