# Codex 판정 반입 — 50kg D0.7-50 정착 재개 한 건 범위 GO (10-30)

- 받은 ZIP (1저자 10-30): `codex_kg50_d07_scoped_review_09ae533d0_20261030.zip` · 376,150 B · sha256 `6d80512a7fc62f34e76e1350db81fa9b77b333d9476ed981837418a609fd2f60` · 멤버 118 (경로 이탈 · 링크 0) — ZIP 자체는 리포 밖.  요청서 = 이 폴더 `evidence/codex_kg50_d07_scoped_go_request_20261030.md` (보낸 그대로) · 리뷰 핀 `09ae533d05f6f165c9754ff4edd42cd97c7c3c06`.
- 판정 = **한 건 범위 GO** — `kg50_d07_b50` · NP 56 · step 20001 체크포인트 → 정착 산출물 200001 · 요청서 §3 수동 영수증 대조 + 등록 Q6 수동 중단을 포함한 운영에 대한 GO (무인 실행 · 정착 뒤 물리 결과 GO 아님) · 새 P1 없음 · 새 `D07S-01` (P2 = `PAI-02` 재현 · 일반 도구 열림) · `D07S-02` (P3 · 자동 정지 아님) · 요청서 집계 정정 (시도 폴더 18 → 17).  `KG50R-F01` · `F02` 일반 종결 · Q5 · W1 · W2 · 압축 · 이완 물리 = 판정 안 함.
- 원 로그 (Codex 의 질문 뒤 1저자 보충): `evidence/input/kg50_d07_b50_ins1_log.liggghts` 13,475 B · sha256 `b1b298bbd54f77a1adf47745e6b1eed14ab2a35bbb5aea9c473b6e9ff46657f5` — ibb 원본 (kg50_d07_b50.ins1/log.liggghts) · 도구 사본 (kg50_d07_b50/log.liggghts.ins1) 둘 다 같은 sha256 · cmp 같음 (지킴이 ① · 10-30 15:21 KST · 판정문 §6-1 의 서버 확인).

## 반입 범위

| 넣음 | 뺌 (이유) |
|---|---|
| 판정문 · Codex `README.md` · `PACKAGE_MANIFEST.sha256` · `REVIEW_SCOPE.json` · `evidence/` (요청서 · 원 로그 · `-T` 묶음 tgz · intake · remote meta · `reproduce.py` · 탐침 · `independent/`) | `evidence/repo/` (리뷰 핀 blob 사본 = git 이력) · `evidence/trial/` (= `evidence/input/kg50_d07_T_1030.tgz` 의 풀린 사본) |

- 텍스트 10 개의 CRLF → LF (`.gitattributes` eol=lf · json · txt) — `PACKAGE_MANIFEST.sha256` 의 값은 ZIP 원본 바이트 기준이라 그 10 개는 다르다 (내용 같음).

## 우리 트리 재현 (`_repro_ours_20261030/`)

| 무엇 | 결과 |
|---|---|
| `evidence/reproduce.py` 그대로 (복사본 · `python3 -I -B` · 읽고 나서 실행 — 쓰기 = `independent/` 만 · 외부 명령 = 우리 `compare_transform.py` 하나) | **55/55** (`reproduce_stdout.txt` · `reproduce_checks.json`) |
| 결과 파일 22 개 ↔ Codex `independent/` | 19 바이트 같음 · 3 (`evidence/independent/transform/` 의 diff_D07.txt · diff_D2.txt · transform_compare.json) = Codex 쪽 CRLF 만 다름 (CR 지우면 sha256 같음) |
| 독립 `g13_check.py` (원 로그 ↔ 시험 출력 · 덱 메아리) | G1 step 20001 KE 2.2522724 = 원 로그 두 줄 (run 20000 끝 · run 3000 설정) · 원자 488,291 같음 · G3 step 21000 KE 2.3879436 같음 · 본 덱 1–166 행 명령 111/111 이 로그에 순서대로 · 삽입 덱 1–170 행 115/115 · 본 덱 167 행 `run 200000` = 로그에 없음 (원 런 = 삽입 덱 `run 20000` · 음성 대조) |

## 원장

| 원장 | 등급 · 상태 | 무엇 |
|---|---|---|
| `D07S-01` (Codex 표기 그대로) | P2 · open | `PAI-02` 재현 — 새 호출 영수증이 승인 영수증 `29ff619a…` 와 자동 대조되지 않음 (원 덱 정착 run 200000 → 210000 + 재개 덱 180000 → 190000 을 같이 바꾸면 정적 대조 문제 0 · 시험 덱 바이트 같음) · 이 한 건 = §6 수동 대조 (지킴이) |
| `D07S-02` | P3 · open | *"200001 에서 멈춤"* = 자동 종료 아님 (`write_restart` 뒤 `run 1` · 안정화 `run 200000` · 압축 루프) · 이 한 건 = 지킴이 ⑤ · 닫힘 = 정지 기록 반입 뒤 |
| `SELF-142` | P3 · claimed_fixed | 요청서 §2-4 의 G1 · G3 *"원 로그"* 값 = 도구 보고 전사 · 원 로그를 ZIP 에 안 넣음 → Codex 가 경로를 물음 · 고침 = 원 로그 보충 · 반입 · 독립 대조 |
| `SELF-143` | P3 · claimed_fixed | 요청서 표기 둘 — *"시도 폴더 18 파일"* (실제 17 · tgz 41 멤버 = 고유 23 + 같은 바이트 중복 17 + 폴더 1) · *"원 줄 157"* (도구 문구를 옮김 = 재개 덱 줄 번호 · 원 덱 첫 긴 run = 167 행) · 판정 영향 없음 (판정문 §5) |

## §6 운영 (이 한 건) — 지킴이 `docs/50kg/d07_guard/`

| 조건 (판정문 §6) | 10-30 기록 |
|---|---|
| 1 원 로그 서버 확인 | 원본 · 사본 sha256 `b1b298bb…` · cmp 같음 |
| 2 새 영수증 = `29ff619a…` (시험 끝나기 전) | 지킴이 통과 (③ · ④ 도달) · 시도 `attempt_r56_1030_152123_2568313` · 시험 job 333908 · ② 줄 원문 = 정지 뒤 전체 로그 반입 때 |
| 3 불일치 · 미확인 대응 | 지킴이가 그 시도 폴더의 job 만 취소 (흉내 9 장면) |
| 4 G0–G3 · 본 job 신원 | 시험 `G0 1 G1 1 G2 1 G3 1` · 본 job 333911 `LMP_IDENTITY` 3/3 (lmp_mpi `ee2d7726…` · 덱 `8e129f42…` · 체크포인트 `aa833368…`) |
| 5 Q6 수동 중단 | 지킴이 ⑤ 대기 (15:24:18 KST 시작) → 정지 기록 · `restart_after_settling.bin` sha256 = 다음 반입 |
