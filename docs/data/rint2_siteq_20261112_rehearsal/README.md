# Rint ② 현장 확인 블록 예행 — kgy · gabia (2026-11-12 · 핀 `11a794674` · 짧은 꼴 + nohup 꼴)

> 출처 = 1저자가 두 기계에서 블록 넷 (짧은 꼴 · nohup 꼴 × kgy · gabia — 블록 틀 `68d5d92a0` 에 본 세션이 칸 일곱을 채워 11-12 보냄) 을 돌리고 기계마다 tgz 로 묶어 대화에 올림 (11-12 04:4x UTC).  점검 도구 = `docs/reviews/rint2_siteq_prep_20261109/tools/siteq_probe.py` (핀 `11a794674` 에서 sha256 c455c792ba431f4840a4964f48f0c01142d4e05e7c5b5f5f6e3ae3b4b81e1a65 = 네 결과의 `probe_sha256` 칸과 같음).
> **지위 = 예행.**  계획 `docs/reviews/rint2_siteq_remaining_plan_20261110.md` §0-2 Q1 (1저자 11-10) = 본 현장 확인 블록의 핀은 단일 개정 커밋 그 자체 → 그 커밋 뒤에 한 번 더 돈다.  이 결과는 그 핀의 증거가 아니다 — 블록 틀이 두 기계에서 두 꼴 모두 끝까지 도는지 · 11-09 와 같은 상태가 나오는지를 본 것이다.  등록 R · 봉인 · R 런 · 실행 GO 아님 (전체 HOLD 그대로).
> 이 폴더 = 홈 경로를 가린 사본 (11-09 규칙 · §2).  받은 원본 바이트는 리포에 두지 않는다 (원본 sha256 = `_orig_hashes.tsv`).

## 1. 받은 것

| 묶음 | 크기 | sha256 |
|---|---|---|
| kgy tgz | 126,692 B | 58587db8016c98364c0b94917b3f4d104b2f8dcb6a3f1dfcf800a630d311500e |
| gabia tgz | 142,827 B | 09e813f40ba765a787c5f023524ea4a14ef68174c6a6f93aa0794b9dc471df7b |

- tgz 목록을 먼저 봤다 (절대 경로 · `..` 없음).  특수 파일 = FIFO 8 · 심볼릭 링크 2 (점검이 결과 폴더에 남긴 시험 파일로 보임 · 추정) → 풀지 않았다.  보통 파일 · 폴더만 빈 폴더에 풀어 읽었다 (python -I).
- 반입 = 보통 파일 24 (기계마다 12):

| 파일 | 뜻 |
|---|---|
| `<기계>/<꼴>/siteq_result.json` | 점검 결과 (33 칸) |
| `<기계>/<꼴>/siteq.log` | 점검 화면 기록 |
| `<기계>/<꼴>/siteq_block_env.txt` | 블록이 적은 umask (블록 시작 · 점검) · SIGHUP 무시 여부 |
| `<기계>/<꼴>/siteq_block_modes.txt` | 계획 폴더 · 원장 · 출력 자리 권한 (읽기만 · 소유자는 이름 · 번호 없이 부류로) |
| `<기계>/<꼴>/siteq_block_rc.txt` | 블록 rc · 끝 시각 |
| `<기계>/nohup_launch/nohup.log` · `nohup_rc.txt` | nohup 꼴 실행 화면 · rc |

## 2. 가림

- 11-09 규칙 그대로 — 홈 폴더 경로 → `<HOME>` (문자열 치환).  파일마다 바꾼 자리 = `_orig_hashes.tsv` 4 열 (`siteq_result.json` 25 · `siteq.log` 2 · `nohup.log` 3 · 나머지 0 · 네 실행 같음).
- 그대로 둔 것 = 나머지 바이트 (11-09 와 같은 칸 — machine-id · boot-id · uid · 기계 별명).  주소 · 호스트 이름 · 사용자 이름은 원본에 없다 (훑어봄).
- 원본 `siteq_result.json` sha256 (`_orig_hashes.tsv` 3 열) = 묶음 안 sha256 기록과 같음 · 짧은 꼴 둘 (kgy 74a06daa… · gabia aa86000c…) 은 1저자 화면 값과도 같음.
- 가린 사본 sha256 = `SHA256SUMS` (24 줄 · 자기 · 이 README 제외).

## 3. 결과

| | kgy 짧은 | kgy nohup | gabia 짧은 | gabia nohup |
|---|---|---|---|---|
| 블록 rc · 끝 (UTC) | 0 · 04:43:11 | 0 · 04:43:28 | 0 · 04:44:01 | 0 · 04:44:20 |
| PASS · INFO · WARN · FAIL · ERROR | 25 · 8 · 0 · 0 · 0 | 25 · 8 · 0 · 0 · 0 | 24 · 9 · 0 · 0 · 0 | 24 · 9 · 0 · 0 · 0 |
| 실행 사용자 | uid 1003 | uid 1003 | uid 0 (root) | uid 0 (root) |
| umask (블록 시작 = 점검) | 0002 | 0002 | 0022 | 0022 |
| SIGHUP 무시 | no | **yes** | no | **yes** |

- 걸린 시간 (1저자 화면 · 짧은 꼴) = kgy 14.0 s · gabia 17.9 s.

| 대조 | 결과 |
|---|---|
| 두 기계 (같은 꼴끼리) — 준비 문서 `docs/reviews/rint2_siteq_prep_20261109/README.md` §3-3 나란히 보기: pin · env unit (C02) · code_key_sha256 (C04) | SAME 셋 · 짧은 꼴 · nohup 꼴 둘 다 (pin `11a7946748fa4da2cd8e691ef5f7abc02aac2a56` · numpy 1.24.4 · Python 3.8 · scipy 1.10.1 · code_key 51a2ed2946c8f5956dbae5e5df93f237a8a5d7ab4111125f46fcab97b5aac159) |
| 같은 기계의 짧은 ↔ nohup — 33 칸 상태 | 같음 (두 기계) · 권한 목록도 출력 폴더 이름 말고 같음 |
| 11-09 (`docs/data/rint2_siteq_20261109/` · 핀 `db86ce9b9`) ↔ 11-12 짧은 — 33 칸 상태 | 같음 (두 기계 · 칸 id 집합 같음 · C13b = kgy PASS · gabia INFO 그대로) |
| 권한 목록 | 계획 폴더 = kgy 0775 (같은 그룹 쓰기 가능) · gabia 0755 · 원장 · 출력 뿌리 · 계획 파일 = 아직 없음 (두 기계) |

## 4. 말하는 것 · 말하지 않는 것

- 말하는 것: 블록 틀 (`68d5d92a0` · 계획 §10 의 2 번 · 1저자 11-10 Q1 · Q6 · Q8) 이 두 기계에서 짧은 꼴 · nohup 꼴 모두 끝까지 돌았다 (rc 0 넷).  같은 핀에서 두 기계의 환경 단위 · 코드 키가 같고, 33 칸 상태가 11-09 와 같다.  nohup 꼴은 SIGHUP 을 무시한 채 돌았다.
- 말하지 않는 것: 본 현장 확인 (단일 개정 커밋 핀 · 계획 §0-2 Q1 — 그 커밋 뒤 같은 블록을 다시 돈다) · 11-09 README §5 의 남는 몫 그대로 (쓰는 도중 kill · 전원 손실 · 실제 OOM · 디스크 가득 · 여러 시간 런 · 두 기계가 한 원장을 같이 쓰는 경우 · 실제 러너 · GPU 풀이 · 숫자 칸 · 실행 정책).
- kgy umask 002 (새 파일 664) · 계획 폴더 0775 = 같은 그룹 사용자가 기록을 고칠 수 있다 (그룹 구성원 미확인 · 11-09 §4 와 같은 기록) · gabia = root 라 권한 기반 보호 (C13b) 는 뜻이 없다 (기대대로).
