# Codex Rint ② 설계·구현 재검토 (10-22) — 반입 기록

- 판정문 = `docs/reviews/codex_review_rint2_rereview_20261022.md` (바이트 그대로 · 41,797 B · sha256 `c8637357c99d6cd668f08f3967eff33bc6a3e0de8823f5932d32418ac3236131`) — ZIP 안 사본과 Codex 작업 공간 폴더 사본이 같은 파일 (같은 sha256).
- 리뷰 핀 = `0b3012460fb8e8b7d53484b0efe399e2dc506aec` (가지 `claude/sdcp-dem-manuscript-si-pqwtv8` · 비교 기준 `5dc6f7f0b`) — 우리가 보낸 ZIP `codex_rint2_rereview_0b3012460.zip` 2,069,820 B · sha256 `dcbdb9805fc211ec5592453d36c502892d579b88edc3187efe8d47396c97aac1` · 리포 파일 205 / 205 = 핀 blob (판정문 §1 · `evidence/zip_integrity.json` · `evidence/zip_pin_comparison.json`).
- 원 ZIP (Codex 작업 공간) = `codex_rint2_rereview_20261022.zip` · 46,100,433 B · sha256 `958e3aa5fecc73c7f2dc7c68b66cc6f1d522a7aec011cc1a84f8139ed458ea53` (`MINI_MANIFEST.json` 머리).
- 받은 미니 ZIP (1저자 WSL 명령 · 10-22) = 986,383 B · sha256 `071f690287f5ec00c72979d51e2bd367da10672d0b3d35aa20d1a6e996d614c0` · 47 항목 · 경로 이상 0 · 링크 0 · 중복 0 · CRC 정상 · 매니페스트 sha256 대조 46 / 46 · 원 ZIP 에서 뺀 것 = 핀 소스 사본 `source/` 1,679 항목 (77,777,194 B · 이름 · 크기 · sha256 = `MINI_MANIFEST.json` `excluded`) — 그 밖에 뺀 것 0.
- 핀 소스 다시 만들기 = `source_manifest.json` 의 1,679 경로 전부 핀 git 객체와 같다 (blob id · sha256 · 크기 · 합 77,777,194 B · `_source_rebuild_check.json`) — 리포에 다시 넣지 않는다 (`git show 0b3012460:<경로>` 로 같은 바이트).
- 리포에 넣지 않은 것 둘: 미니 ZIP 의 `_outside_zip/` 폴더에 든 판정문 사본 (판정문과 같은 sha256) · `evidence/tree.json` (4,649,724 B · sha256 `642c080b42f3749a248754322aa05b8cd4061274db21e3cda310176d73b010c9` · 핀의 GitHub 트리 목록 · git 으로 다시 만들 수 있음).
- 나머지 = 미니 ZIP 그대로 (`_members_mini.tsv` = 경로 · 크기 · sha256 · 자리).  안의 스크립트 (`intake.py` · `package_review.py` · 탐침) 는 반입 때 실행하지 않았다.
- 환경 (Codex · 판정문 §1) = Windows · Python 3.12.14 · NumPy 2.5.3 · SciPy 1.16.3 · OpenBLAS / OMP / MKL 1 스레드 · 실침대 · 생산 캠페인 · 전체 셸 CLI · `check_all` 실행 없음 · S0 탐침 = 작은 합성 fixture 의 실제 raster / census 본체 (transport solve 0 회 · 셸 인자 = 고정 fixture · 단계 2 Git 계획 선행관문 제외).

## 판정 요약 (판정문 §0 · §9 · 최종 판정 그대로 줄임)

- **등록 R 정량 판정 캠페인 = HOLD** · **S0 단계 1 + SBE 숫자 탐침 = 조건부 GO** · S1 · S3 = 조건부 GO 유지 · S2 v0 = 기구 · 탐침 조건부 GO · 수렴 증서 ⓓ = 조건부 GO · 새 P1 없음.
- RCA 12 건 중 11 건 = 지난 판정 최소 해결 닫힘 (범위 한정) · RCA-06 = 부분 · RCA-11 · RIMPR-04 · RINT2-B01 = 범위 밖 (닫지 않음).  실침대에서 물리 모형이 검증됐다는 뜻이 아니다 (§0).
- 새 결함: P2 `RCA2-01` (SV 문턱 = nominal 비 · 증서 구간 미전파) · `RCA2-02` (F1 · F2 코드 귀속) · `RCA2-03` (F8 S0 → R 침대 귀속) · `RCA2-05` (시간 · 중단 · 재시도 봉인 밖 · 사전등록 절차) · P3 `RCA2-04` (F3 SV 기록 계약) · `RCA2-06` (F4 회귀 사각 · F6 실패 상태 설명) · `RCA2-07` (총 ×100 문구 · SV 위끝 풀이 비용) · `RCA2-08` (`fsum` 넘침) · 번호 없는 P3 = DBE R 단조 방어 검사 부재 (§8 → 원장 `RCA2-09` · Codex 번호 아님).
- §9 최소 해제 목록 (실행 전) = SV 구간 전파 + 기록 계약 · 코드 귀속 · 침대 귀속 · 사전등록 실행값 (계획 · 숫자 · scope · 시간 · 재시도 · 기계 귀속 · SV 범위 · 문서 / JSON 동기화) · 실측 보충 (새 SBE / DBE S0) · 작은 끝-끝 정상 · 음성 증거.
- C6 (저자 미결 30 자리) = 결함 #3 · #5 · #12 · #13 · #17 · 나머지 = 선택 · 정책 · 문서 (판정문 §7).

## 원장 변경 (반입 커밋)

- `RCA-01` · `02` · `03` · `04` · `05` · `07` · `08` · `09` · `10` · `12` · `13` → **verified** (verified_by codex · verified_sha `0b3012460` · verified_scope = 판정문 §2 표 그대로 줄임).
- `RCA-06` → claimed_fixed 유지 + `partial_note` (원 국소 소산 반례 · 못 가른 덩어리 제거 = 닫힘 · 최종 문턱 보장 = `RCA2-01` · 닫는 조건 = `RCA2-01` 검증).
- `RCA-11` → open 유지 (판정문 §2 끝 · §9 실측 보충 뒤 재판정) — 메모 한 줄.
- 새 `RCA2-01` – `RCA2-09` open.

## 우리 트리 재현

반입 뒤 따로 한다 (판정문 §10 명령 · 묶음 복사본에서 · `RINT_REVIEW_SOURCE` = 핀 작업 트리).  결과는 이 문서 끝에 덧붙인다.

→ ✅ 10-22 재현 = `_repro_ours_20261022/README.md` — 판정값 차이 0 (탐침 여섯 · rc 0 · 등록 467 / 467 · 증서 · 기하 · provenance · S0 판정값 같음 · 숫자 차 = CG · spsolve 반올림 · 버전 · Windows 줄 끝 · RCA-07 main 반례 B 하나만 환경 칼날 = 10-21 과 같음).
