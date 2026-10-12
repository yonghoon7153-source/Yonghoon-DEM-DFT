# 보충 20 지원 검토 증거 반입 (10-12) · 우리 트리 재현

정본 판정 = `docs/reviews/codex_review_supp20_support_20261012.md` (리뷰 핀 `b429c3c1d` · 기준 = 재검증 7 핀 `3cedd40a5` · **HOLD — 보충 지원 전체 · 214 배포 승인 · 새 P1 없음** ·
P2 `SUP20-01` · P3 `SUP20-02` · 194 의 R7 기술 차단 해제 유지 · 수치 재계산을 요구하는 새 결함 없음).
Codex 묶음 설명 = 이 폴더 `README_REVIEW.md` (묶음의 `README.md` 를 이름만 바꿨다).

## 1. 받은 것 · 넣은 것

| 묶음 | 크기 · 파일 | sha256 | 리포 |
|---|---|---|---|
| 원 ZIP (1저자 PC · Codex 작업 공간) | 46,171,879 B | `2f957f42bbbdb0af3e5469f8f4a27330a5ec516f11dc7997db02c3af96ca6239` (`ORIGINAL_ZIP_SHA256.txt`) | 넣지 않음 |
| slim ZIP `codex_supp20_support_review_20261012_slim.zip` (1저자 WSL 에서 줄임 · 10-12 첨부) | 1,835,619 B · 94 항목 (위험 경로 · 링크 없음) | `38bc4035415ef3ca52861bcb910797615784448a6a909d15ea8dd70de06a5e95` | 아래 표만 |

- 묶음 sha256 표 (`MANIFEST.sha256.json` · 1,107 행 · 자기 제외) 대조 = slim 에 남은 **90 / 90 같음** · 뺀 **1,017** 은 `SLIM_EXCLUDED.tsv` (경로 · 크기 · sha256) 에 있고 그 sha256 = 표와 같음 · 표에 있는데 남지도 빠지지도 않은 것 0.
- 판정문 = 묶음 맨 위 사본 = 묶음 폴더 안 사본 (바이트 같음 · sha256 `3d70e4e3…`).  윈도 경로 (`C:\Users\Administrator\…`) = Codex 작업 공간 경로 그대로 (비밀 아님 · 증거 13 파일) · 메일 주소 · 토큰 · IP 없음 (검색 — `@` 낱말 1 = 코드의 `@functools.lru_cache`).

| 무엇 | 반입 | 빠진 것 (복원 방법) |
|---|---|---|
| 판정문 | `docs/reviews/codex_review_supp20_support_20261012.md` | — |
| 묶음 README · `MANIFEST.sha256.json` · `run_checks.py` · `package_review.py` · `prepare_source.py` · `acquire_extra.py` · `source_manifest.json` · `ORIGINAL_ZIP_SHA256.txt` · `SLIM_EXCLUDED.tsv` | 전부 | — |
| `evidence/` 35 · `notes/` 3 · `probes/` 5 | 전부 | — |
| `baseline/` 37 (기준 쪽 스크립트 · 웹앱) | — | 기준 핀 `3cedd40a5` 의 git blob 과 **37 / 37 바이트 같음** (`git show 3cedd40a5:<경로>`) |
| `submitted/request.md` | — | 리포 `docs/reviews/codex_supp20_support_review_request_20261012.md` 의 `06d2cf328` 판 (= 지금 HEAD) 과 바이트 같음 (sha256 `b22c626f…`) · 리뷰 핀 `b429c3c1d` 판과는 발송 표지 · 핀 · U5 커밋 명시 세 곳이 다르다 (판정문 §6) |
| `commit.json` (263,822 B · `43a7c909…`) · `compare.json` (1,426,096 B · `d8c6905c…`) | — | GitHub API 응답 = 핀 커밋 · `3cedd40a5...b429c3c1d` 비교 (10 커밋 · 파일 목록 300 에서 잘림) → `git show b429c3c1d` · `git diff 3cedd40a5 b429c3c1d` |
| `source/` 1,016 (68,985,889 B · slim 에서 뺌) | — | 핀 `b429c3c1d` 의 리포 파일 — **우리 git 의 blob SHA-1 · SHA-256 · 크기 = `source_manifest.json` 1,016 / 1,016 같음** |
| `tree.json` (3,511,147 B · slim 에서 뺌) | — | 핀의 GitHub tree 응답 — `git ls-tree -r b429c3c1d` (8,484 항목) |

## 2. 우리 트리 재현 (10-12 · HEAD `b556dd5db` · 리뷰 핀 이후 바뀐 것 = 문서 · 자료뿐 (`scripts/` · `webapp/` 변경 0) · 컨테이너 Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1)

| 무엇 | 어떻게 | 결과 |
|---|---|---|
| Codex 탐침 `release_probe` · `design_probe` (무변경) | 새 빈 폴더에 Codex `run_checks.py` + `probes/` · `source` = HEAD 의 git worktree (스냅샷 1,016 파일이 아니라 전체 체크아웃) · `python3 run_checks.py design_probe release_probe` | **둘 다 rc 0** (7.5 s · 21.9 s · 로그 = `run_checks_ours.log`) |
| `compare_probe_outputs.py` → `compare_probe_outputs.json` | 우리 출력 (`release_probe.json` · `design_probe.json`) ↔ Codex 증거 — 평탄화 키별 | **판정값 차이 0** · `release_probe` 키 97 / 97 · 같음 91 · 다른 6 = 작업 경로 문자열 (빌드 출력 폴더 3 · τ 대역 호출 인수의 뿌리 경로 3) · `design_probe` 키 914 / 914 · 같음 900 · 다른 14 = 재적합 `free` 계수 · 지표의 실수 끝자리 (상대 ≤ 1e-12 · 최소제곱 수치) |

우리 트리에서 다시 확인된 것 (판정값 = Codex 와 같음):
- `SUP20-01` — 정상 214 build → check 문제 0 · 다른 code_fp 보충 뿌리 (합성 `3b0ef9f1…` ↔ `250a59b2…` = 시험용 축소 봉인 · 생산 지문 아님) → **build 거부** (ReleaseError) ·
  manifest `supp_batch` 만 교체 (`batches.supp20.root` 원래) → **check 문제 0** · 교차 뿌리도 교체 뿌리로 → 문제 2 · 교체 + 교차 뿌리 = 없는 경로 → **문제 0** · 정상 묶음 교차 뿌리 하나만 없는 경로 → **문제 0** ·
  `supp_batch.code_identity` 삭제 → **문제 0** (최상위 194 `code_identity` 삭제 → 문제 1 = 대조) · 승인 없는 봉인 변경 (`sealed_changed ['webapp/app.py']` · `allowed []`) → **문제 0** · 교체 뿌리 자신의 관문 → 문제 0 (대조).
- `SUP20-02` — mono_AM_S 네 행 (`lhss_001` · `002` · `003` · `020`) 원천 P 슬롯 0.3 · 0.3 · 0.3 · 0.375 · S 슬롯 0 · 변환 `ps_frac` = 0 (어댑터 정상) ↔ 열 사전 식 `w_AM_P / (w_AM_P + w_AM_S)` = 1.
- 설계 독립 재계산 = 불일치 0 (20 행 × 40 열 · 정수 개수 오차 최대 0.47 · 하중 반올림 최대 4.9e-5) · 어댑터 CSV sha256 `df505b79…` (20 행 · 40 열 · ID 20).
- 합성 경로 수 = 214 행 · 적합 189 (lhs 106 · lhsx 64 · lhss 19) · 194 참고 적합 170 · 원 194 주 표 · Physics 부록 · 열 사전 8 파일 바이트 같음 — **합성 관문 시험값이다 · 실제 g2 214 결과로 인용 금지** (판정문 §3 Q4).
- 판정문이 기존 경계로 남긴 것 (새 결함으로 세지 않음 · 증거 보존): 인계표의 고정 하중 칸에 99 · −1 · NaN · 글자를 넣어도 build · check 통과 (lhs · lhss 모두 · §3 Q3) · 인계표 해시가 manifest 기록과 달라도 (출처 열만 바꿈) check 문제 0 (§6).

- 재현 명령: 새 빈 폴더 `R` 에 이 폴더의 `run_checks.py` · `probes/` 를 복사 → `git worktree add --detach R/source <커밋>` → `R` 에서 `python3 -B run_checks.py design_probe release_probe` → `python3 -I -B _repro_ours_20261012/compare_probe_outputs.py <이 폴더>/evidence R/evidence out.json release_probe.json design_probe.json` (rc 0 = 판정값 차이 0) → `git worktree remove --force R/source`.
- 한정: 반례 · 계약 재현이다 — 배포 시험 전체 (Codex = 윈도 232 PASS / 2 FAIL — 경로 문자열 · git HEAD 가정) · 실행기 자체시험 · `check_all` · fast16 + real4 · 생산 194 · 보충 20 은 이 재현에 들어 있지 않다 (우리 게이트가 앞의 셋을 따로 돈다).

## 3. 판정문이 정한 한정

- `SUP20-01` 은 **배포 도구 층** 결함이다 — 정상 build 의 교차 검사 (다른 봉인 보충 = 거부) · 이미 계산된 σ · 194 R7 기술 판정 · 수치 봉인 32 (`code_fp e8b2496b…` 바이트 같음) 를 반증하지 않는다 · 이 결함만으로 214 재계산 이유 없음 (§4).
- `SUP20-02` = 열 사전 문구 — CSV · 계산 · 배치 ID 정상 (§2).
- Q1 (같은 발사 SHA) = 이번 등록 §4 대로 같은 깨끗한 발사 핀 권고 · 같은 `code_fp` 만으로 실행기 · 인계기까지 같다고 말하지 않는다 · "SHA 불일치 무조건 금지" 새 조건은 없음.
- Q6 = 등록 §2 를 채운 것만으로는 발사 불가 — 수정 diff + 입력 봉인 · 사전 점검 영수증 짧은 확인 (ID 지문 `991cf115…` · 등록 §2 raw 표 · TSV = 반입 파일 재계산 = 발사 dry-run · 도구 핀 · 관측 ON · 새 ROOT 둘 · 사전 점검 · 저자 발사 승인).
  `preflight rc 0` 하나로 보충 등록까지 인증하지 않는다 (등록 불성립 = 일반 계획 `--expect-case` 강등 — §4).
- 등록 §4 의 fetch 예시 브랜치 (`claude/sdcp-dem-manuscript-si-pqwtv8`) → 발사 전 `claude/stoic-knuth-NObVQ` 와 최종 핀으로 맞춘다 (§5 끝).

## 4. 다음

수정 계획 `docs/reviews/sup20_fix_plan_20261012.md` (Q1–Q4 · 1저자 비준 대기) → 반례 먼저 → 수정 → 원장 claimed_fixed → 고친 트리에서 Codex 탐침 다시 → 짧은 재확인 요청서 → 1저자 발송 → Codex.
