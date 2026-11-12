# 믹서 E0 자격 pilot — ibb 읽기 전용 보충 조회 q9b · q2b · q7b (2026-11-12 22:08 UTC)

[DEM 우선 Ⓒ] 믹서 E0 자격 pilot 한 팔 준비 — 등록 초안 13-1 절의 봉인 전 보충 조회 결과 (가린 사본).
⛔ **관측일 뿐이다 — 자격 판정 · 봉인 · 운영 승인 · 발사 GO 가 아니다.** 전체 HOLD 그대로.
앞선 메타 수집 = `docs/data/mixer_e0_meta_ibb_20261110/README.md` (11-10 · 같은 반입 규칙).

## 1. 블록

- `block/query_block_b.txt` — 551 줄 · 37817 B · 파일 sha256 d1a400ad776b38d3b3c6ec8736f4c5b4bf5435c75a1632a5218ed587411d104c. 본문 스크립트를 셸 변수에 담고 마지막 줄이 스크립트 md5 3c0a612028d16692625c264224a573fc 를 대조한 뒤에만 `bash -c` 로 돈다 (한 글자라도 깨지면 아무것도 안 한다). 본문 사본 = `out/query_script.sh` (같은 md5 · 36783 B).
- 읽기 전용: ibb 에서 쓰는 곳 = 새 폴더 하나 (raw/ = 가리지 않은 원문 · ibb 에만 / out/ = 가린 사본 / tgz = out/ 만). 안 하는 것 = 제출 · 취소 · 잡 제어 · 지우기 · 옮기기 · 복사 · conda 바꾸기 · 프로그램 실행. 숫자 값 · 본문 · 경로 문자열은 옮기지 않는다 (센 수 · 꼴 · 해시만).
- 가림: 홈 (로그인 · 실제) · 계정 · 호스트 · 노드 이름 (sinfo 자리표) · 도메인 · IPv4 · uid / gid · 빌드 사용자 → 자리표 (`<HOME>` · `<HOME_REAL>` 등).
- 시험 (본 세션 scratch · 리포 밖 · 가짜 HOME · 가짜 명령 · PID 이름공간): 고치기 전 PASS 48 · FAIL 38 → 뒤 PASS 1104 · FAIL 0. 진짜 SLURM · Lustre · conda 에서는 시험하지 않았다.
- 판독기 = read_query_bundle_b.py (본 세션 scratch · 이 폴더에는 안 넣음 · md5 5bc4218296a0873ac6e317eb36de4d7e · sha256 b0ae3ecff25d75b02376cc23c363ab04a7d197712d31ee483ff95216455c3cf7) — 받은 tgz 를 빈 새 폴더에 풀고 (정규 파일만 · 링크 · 하위 폴더 · `..` 거부) 대조 · 요약한다 (`python3 -I`).

## 2. 승인 · 범위

- 1저자 11-12 밤 오버나잇 "권고대로" = 등록 초안 18 절 2 회차 표 Q-F′ (q9b) · Q-G′ (q7b) · Q-K (q2b).
- q9b: DEV E0 다섯 (r1–r5) + dev-bo 둘 (LHx10 · LHx30) + dev-u 둘 (LU212 · LU637) 의 `log.liggghts` — thermo 표 안 숫자 줄이 아닌 줄마다 표 번호 · 표 안 차례 · 앞 숫자 행 수 · 앞 공백 · 가린 첫 낱말 (24 자).
- q2b: DEV E0 r1 의 post 프레임 셋 (이름의 step 으로 처음 · 가운데 · 끝) — 끝 바이트 개행 · 개행 수 · 머리 1 · 3 째 줄 꼴 · 2 째 줄 = 이름 step 인가 · 4 째 줄 원자 수 (TIMESTEP 값 · 본문은 안 옮김).
- q7b: 사용자 conda 환경의 꾸러미 일곱 (openmpi · ucx · ucc · libfabric · libfabric1 · libpmix · libhwloc) 의 conda-meta JSON 이 적은 파일마다 번호 · 종류 · 크기 · 수정 시각 · sha256 + JSON sha256 + 꾸러미 다이제스트 (읽기만 · 실행 없음 · 경로 · 이름은 안 옮김).

## 3. 실행 · 반입

- 1저자가 ibb 로그인 셸 (SLURM 할당 밖 · bash 4.4.20 · GNU Awk 4.2.1) 에서 실행: 2026-11-12T22:08:55Z → 22:09:07Z (12 초) · 조회 116 = 전부 OK (nodes 1 · q9b 9 · q2b 13 · q7b 93).
- 묶음 `mixer_e0_queryb_20261112T220855Z.tgz` = 48341 B · sha256 d426fe98988fad0b58690b116af23d785dd72ce9b239356573dcd22a9ea385f4 (판독기 `--expect-sha256` 대조 통과).
- 판독기 rc 0 (구조 정상): 묶음 sha256 · `out/SHA256SUMS` 전수 · 스크립트 md5 = 블록 md5 · 형식 `mixer_e0_queryb/1` · 상태 어휘 · 줄 꼴 검사 (정해진 꼴 밖 줄 0) · 가림 뒤 남은 토큰 0 · 가리지 못한 파일 0 · 노드 이름 토큰 8 (가림 목록에만). 빈 새 폴더에 다시 판독 = rc 0 · 요약 JSON 바이트 같음 · 금지 문자열 (계정 · 주소 · 포트 · 호스트 4 개) → 0 곳.
- 이 폴더 = 가린 사본 `out/` 31 파일 그대로 + 판독 요약 `reader_summary.json` (판독기 `--json` 그대로 · sha256 b19b919d672b2d77a176e0e880830d617d441643283da2b1b880fe96ab8c3190) + 블록 + 이 README. raw/ 는 ibb 에만 — `out/RAW_SHA256SUMS` 가 그 해시다.
- 반입 전 따로 찾기 (이 폴더 전체 · 판독기와 별개 · 센 수만 봄): 계정 · 주소 · 포트 · 호스트 (금지 목록 4) 0 · 노드 이름 (11-10 sinfo 의 8) 0 · IPv4 · IPv6 · MAC 꼴 0 · 홈 경로 값 0 (`/home/` 글자는 블록의 가림 규칙 안에만 있다).

## 4. 관측 (자격 판정 아님)

| 조회 | 본 것 | 파일 |
|---|---|---|
| q9b | 로그 아홉 다 읽힘 (없음 0 · 못 읽음 0 · 넘침 0 · CR 0) · 로그마다 thermo 표 4 · 닫힘 4/4 · 머리 5 칸 · 비유한 행 0 · 빈 줄 0 · 표 안 비-행 줄 = 삽입 보고 쌍뿐 — 쌍마다 `INFO:` 다음 `-` · 둘 다 그 표의 첫 숫자 행 바로 뒤 · 앞 빈칸 0 / 1 · 탭 0 · 쌍이 놓인 표 = 덱의 insert/pack 선언 다음 run (E0 = 표 1 · dev-bo · dev-u = 표 1 · 3 · 덱 기대 = 리포 덱 사본 `docs/data/mixer_highbo_dev_decks_20260930_v26/` · `docs/data/mixer_highbo_dev_decks_20261002_bo/` · `docs/data/mixer_highbo_dev_decks_20261005_u/`) 9/9 · 쌍 밖 줄 0 (표 안 `WARNING:` · `ERROR` 0) | `out/q9b_l1.txt` – `out/q9b_l9.txt` · 요약 `q9b` |
| q2b | r1 의 `mix_*.liggghts` 1037 (다 `mix_<숫자>.liggghts` 꼴) · 고른 step 1000 · 519000 · 1037000 · 세 장 다 끝 바이트 개행 · 개행 수 100009 = 9 + 원자 수 100000 · 1 째 줄 `ITEM: TIMESTEP` · 2 째 줄 = 이름 step · 3 째 줄 `ITEM: NUMBER OF ATOMS` | `out/q2b_pick.txt` · `out/q2b_frames.txt` · 요약 `q2b` |
| q7b | 꾸러미 7/7 OK · 파일 1011 해시 (링크 108 · 대상 다 정규 파일 · 사유 0 · 넘침 0) · 꾸러미별 223 · 160 · 43 · 0 · 3 · 31 · 551 (libfabric 꾸러미의 파일 목록은 비었다) · 파일 수정 시각 다 2026-03-26T05:28:48Z 이하 | `out/q7b_p1_sum.txt` – `out/q7b_p7_files.txt` · 요약 `q7b` |

- 11-10 대조: 아홉 로그의 크기 · 수정 시각 = 11-10 목록 (`docs/data/mixer_e0_meta_ibb_20261110/out/` 의 run 목록 파일) 과 같음 9/9 · JSON 이름 일곱 = `docs/data/mixer_e0_meta_ibb_20261110/out/conda1_meta.txt` 의 이름과 같음 7/7 (11-10 에는 파일 해시가 없다).
- 11-12 앞선 조회 (11:52Z · 가린 사본은 아직 리포 밖) 대조: r1 로그 표 센 수 같음 · q2b 세 장 크기 같음 3/3 · 링크 라이브러리 30 개 가운데 10 개 = 이 목록 안 파일과 같은 sha256 · 크기 10/10 (나머지 20 개는 목록에 없다).

## 5. 한정 · 쓰는 곳

- q9b · q2b 는 DEV (옛 덱 세대 · 기본 `%g` 덤프) 의 로그 · 프레임이다 — pilot (전 정밀도 덤프 · 새 덱) 의 로그 · 덤프가 아니다. q9b 는 첫 낱말 · 차례 · 자리 · 앞 공백 수준이다 (넣은 수 · mass · step · 본문은 안 옮겼다). q2b 는 r1 세 장뿐이다 (끝 줄 칸 수는 안 셌다).
- q7b 는 22:08Z 한 시점의 설치 파일 목록 해시다 — 실제로 불러 쓴 부품 · 그 뒤 변경은 말하지 않는다. `reader_summary.json` 은 발사 직전 · T9 직후 q7b 대조의 기준이다 (판독기 `--q7b-ref` · 등록 초안 12 절 W9).
- `UNKNOWN` · `ABSENT` · `FAIL` 은 0 · 정상이 아니다 (이번 묶음에는 없다).
