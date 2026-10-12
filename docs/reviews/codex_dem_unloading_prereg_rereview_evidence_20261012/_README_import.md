# DEM 언로딩 등록 개정 1 — Codex 재검토 증거 반입 (10-12) · 우리 트리 재확인

정본 판정 = `docs/reviews/codex_review_dem_unloading_prereg_rereview_20261012.md` (검토 핀 `3409814a3` · LIGGGHTS 고정 `3d5c00f` · **문서 부분 수용 · 키트 개발 가능 · 본 R · 10:0 이완 연장 · 개발 / 생산 U = HOLD** — 새 finding `ULR1-01` · `ULR1-02` (P1) · `ULR1-03` · `ULR1-04` · `ULR1-05` (P2)).
Codex 묶음 설명 = 이 폴더 `README_REVIEW.md` (묶음의 `README.md` 를 이름만 바꿨다).

## 1. 받은 것 · 넣은 것

| 묶음 | 크기 · 항목 | sha256 | 리포 |
|---|---|---|---|
| `codex_dem_unloading_prereg_rereview_20261012.zip` (1저자 첨부 10-12) | 1,393,081 B · 155 항목 (위험 경로 · 링크 없음) | `fa360301caafeb98557ac3c5b5a4ff6250fa934abbd70004d81dff858fb0520b` | 아래 표만 |

- 묶음 sha256 표 (`CONTENTS_SHA256.json` · 154 행 · 자기 제외) 대조 = **154 / 154 같음**.
- 첨부 두 문서 (`submitted/prereg.md` · `submitted/request.md`) = 리포 `docs/reviews/dem_unloading_ps45_prereg_20261009.md` (sha256 `73bc55a5…`) · `docs/reviews/codex_dem_unloading_prereg_rereview_request_20261011.md` (sha256 `92f9c5ee…`) 와 바이트 같음 → 사본은 넣지 않았다.
- ibb 주소 · 포트 없음 (검색).  `evidence/request_commits.json` = GitHub API 응답 그대로 (작성자 = 커밋 메타데이터의 noreply 주소뿐).

| 무엇 | 반입 | 빠진 것 |
|---|---|---|
| 판정문 | `docs/reviews/codex_review_dem_unloading_prereg_rereview_20261012.md` (바이트 그대로) | — |
| 묶음 README · `CONTENTS_SHA256.json` · `source_manifest.json` · `upstream_manifest.json` · `prepare_sources.py` · `package_review.py` | 전부 | — |
| `evidence/` JSON 5 (`state` · `observers` · `reproduction` · `pin_receipt` · `request_commits`) | 전부 | — |
| `notes/` 셋 (`history` · `observers` · `state` — 보조 · 정본은 판정문) · `probes/` 셋 | 전부 | — |
| `source/` 97 파일 | — | 핀 `3409814a3` 의 리포 파일 사본 — **blob 97 / 97 이 우리 리포 핀의 같은 경로와 같다** · `source_manifest.json` 으로 복원 |
| `upstream/` 37 파일 (LIGGGHTS-PUBLIC 원문) | — | 고정 `3d5c00f` 공개 저장소 원문 (`upstream_manifest.json` 에 sha256) · 10-11 반입과 겹치는 27 파일은 sha256 같음 · 새 10 (`dump*.cpp` · `write_dump.cpp` · `write_restart.cpp` · `run.cpp` · `normal_model_hooke.h` · `surface_model_default.h` · `rolling_model_cdt.h` · `dump_custom.h`) = 판정문 §5 줄 번호의 근거 (독립 대조 없음) |
| `submitted/` 2 | — | 위 등록 · 요청서와 같음 |
| `tree.json` (3.4 MB) | — | 핀의 GitHub tree 응답 — `git ls-tree -r 3409814a3` 로 다시 만든다 (오프라인 재검산에 불필요 · 묶음 README) |

## 2. 우리 트리 재확인 (10-12 · 핀 `3409814a3` = 우리 HEAD · 컨테이너 Linux · Python 3.11.15 · DEM · 키트 실행 없음)

### 2-1. Codex 탐침 무변경 재실행 (`_repro_ours_20261012/codex_probes_rerun.json`)

| 실행 (`python3 -I -X utf8 -B` · 묶음 사본 · 별도 작업 폴더) | rc | 대조 |
|---|---|---|
| `probes/ulr_state.py` | 0 | 출력 JSON = `evidence/state.json` **같음** |
| `probes/ulr_observers.py` | 0 | 출력 JSON = `evidence/observers.json` **같음** |
| `probes/reproduce.py` | 0 | PASS · source 97 · upstream 37 검증 · Codex 영수증과 다른 것 = `runtime` (플랫폼 · Python 판) 뿐 |

### 2-2. 우리 식 재확인 (`_repro_ours_20261012/ulr_checks_ours.py` → `ulr_checks_ours.json` · Codex 탐침을 import 하지 않는다)

| 항목 | 판정문 | 우리 |
|---|---|---|
| 등록 sha256 · 줄 수 | `73bc55a5…` · 685 행 | **같다** |
| 판정문이 인용한 등록 줄 34 곳 (275 · 288 · 307 · 319 · 320 · 332 · 334–337 · 389–394 · 413 · 435 · 473 · 619 · 625 · 627 · 629 · 633–636 · 650 · 651 · 655 · 660–662 · 667 · 678) | 그 내용 | **34 / 34 그 내용** (줄마다 낱말 대조) · 결정표 앞뒤 (625–645) 에 결손 · 무효 끝점 처리 문구 **없음** |
| ULR1-01 — 결정표 글자대로 | 유한 넷 + 등호 0.10 = 유일 · 결손 = 행 없음 | **같다** (NaN 도 행 없음) |
| ULR1-02 — 4 단 사다리 (0.20 · 0.25 · 0.30 · 0.35 µm / 1.2 · 0.8 · 0.6 · 0.4 MPa) · h0 111.052 µm | 보간 0.225 µm · ρ_M 0.2026077873 % < 옛 TIMEOUT 하한 0.3151676692 % | **같다** (거짓 부등식) |
| ULR1-03 — +1.6 / −0.6 MPa 상당 | 순 +1.0 · REG:650 CONTACT 조건 · REG:319 · 651 TENSION | **같다** |
| ULR1-04 — 창 | T_W 0.005 s · dt/2 에서 W 10,000 · 0.6 µm/덱 s → 0.003 µm/창 (S4 FAIL) ↔ 글자대로 5,000 = 0.0015 (PASS) | **같다** |
| ULR1-05 ① — 비단조 b | 첫 · 마지막 교차 1.025 · 1.125 µm · 차 0.0900479055 %p | **같다** |
| Q2 — S3 norm 순서 · σ_P ddof · 표면 관측자 | 0.002 ↔ 0 · σ 0.33 ↔ 0.3385728562 (3σ 0.99 ↔ 1.0157185686) · 빈 칸 100 ↔ 99 µm · p99.9 190.1 ↔ 200 µm | **같다** |
| Q3 — 세 팔 · 괄호 | A 폭 0.1800958110 %p · 괄호 차 최대 0.2200958110 · 미측정 모서리 0.60 %p | **같다** |
| Q6 — 10:0 일정 | 3,660,000 · 3,650,000 mod 10,000 = 0 · 3,660,000 mod 50,000 = 10,000 · 추가 끝 3,710,000 · R 이어 쓰기면 3,662,000 | **같다** |
| source 97 blob ↔ 우리 리포 핀 | — | **97 / 97 같다** |

- 재현 명령: `python3 -I -B docs/reviews/codex_dem_unloading_prereg_rereview_evidence_20261012/_repro_ours_20261012/ulr_checks_ours.py <리포> out.json` (rc 0 = 전부 같음).

## 3. 한정

- 규칙의 **합성 반례** 재확인이다 — 언로딩 결과 · 키트 출력이 아니다 (키트는 아직 없다).  실제 침대의 S3 · S4 실패율 · TIMEOUT 빈도 · 회복량은 미측정.
- 판정문의 "닫힘" = **문서 항목** (판정문 §1) — 원장 `UL-01` ~ `UL-10` 은 **open 유지** (키트 증거 전 미검증 · 판정문 §1 둘째 표).
- §5 의 LIGGGHTS 덤프 블록 = 고정 소스로 본 **키트 시험 후보** (실행 검증한 덱 아님 · 판정문 · 묶음 README).
