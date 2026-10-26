# Codex Rint ② 재검토 회차 ① (10-26) — 반입 기록

- 판정문 = `docs/reviews/codex_review_rint2_rr_round1_20261026.md` — ZIP 원본 = 26,625 B · sha256 `762f2ac47fe439728bb747d43b5c6f67eca63a33ff040226bcf7f7946b98dfab`.  리포 사본은 리포 `.gitattributes` (md = LF) 때문에 원본의 CRLF **한 곳** 이 LF 로 바뀌어 26,624 B · sha256 `75a58332cfcc34e07981ac914e762840a0aeaf627fd7006e1e962493f51fe792` (원본에 CRLF→LF 변환만 한 것과 정확히 같다 · 그 밖 바이트 같음).
- 리뷰 핀 = `9bec6b7646374daed0d3edbb9647f9f46d302750` (가지 `claude/sdcp-dem-manuscript-si-pqwtv8` · 비교 기준 `0b3012460`) — 우리가 보낸 미니 ZIP `codex_rint2_rr_round1_20261024.zip` 2,813,104 B · sha256 `a4866ec5…b9513b6` · 리포 파일 286 / 286 = 핀 blob (판정문 §1 · `evidence/zip_pin_checks.json`).
- 받은 ZIP (1저자 업로드 10-26) = `codex_rint2_rr_round1_review_20261026.zip` · 6,863,581 B · sha256 `e126cc312c4aec0f39cb6ac97598d8b78f4c48705260f96c69128c64fdaf61ad` · 481 항목.
- 리포에 넣은 것 = 판정문 · `PIN.txt` · `REPRODUCE.md` · `MANIFEST.sha256` · `fetch_sources.py` · `package_review.py` · `evidence/` (58 파일 — 아래 둘 제외).  판정문을 뺀 63 파일은 ZIP 원본과 바이트가 같다 (63 / 63).
- 뺀 것 (`_excluded_copies.tsv` = 경로 · 크기 · sha256 · 417 파일 · 27,218,208 B):
  - `repo/` 346 파일 = 핀 `9bec6b764` 의 git blob 과 **346 / 346 같음** · `baseline/` 66 파일 = `0b3012460` blob 과 **66 / 66 같음** · `historical/` 3 파일 = `49a1af626:scripts/step3_conv_cert.py` · `73c640dc2:scripts/carbon_junction.py` · `d1768cf0c:scripts/step3_sigma.py` 와 **3 / 3 같음** — git 으로 같은 바이트를 다시 만들 수 있다 (`_source_rebuild_check.json`).
  - evidence 폴더의 `repo_tree.json` · `baseline_tree.json` = 두 핀의 트리 목록 (git 으로 다시 만들 수 있음).
- 반입 때 ZIP 안 스크립트는 실행하지 않았다 — 탐침 셋은 아래 우리 트리 재현에서 따로 돌렸다.
- 환경 (Codex · 판정문 §1) = Windows · Python 3.12.14 · NumPy 2.5.3 · SciPy 1.16.3 · 스레드 1 · DEM / GPU / S0 실침대 / R 캠페인 · 156 전체 게이트 실행 없음.

## 판정 요약 (판정문 머리 · §2 · §10 그대로 줄임)

- **등록 R 판정 캠페인 = HOLD** · **S0 단계 1 개발 자료 = 조건부 GO** · ⑥ SBE 값 봉인 숫자 탐침 = 수치 검토상 조건부 GO (실행 정책 문구 정리 선행) · 묶음 B = 진행 가능 (끝 가중 그래프 귀속 추가) · 묶음 C = 조건부 진행 가능 (§7 세 조건) · Codex 회차 ② / 최종 계획 봉인 = 아직 미충족 · 새 P1 없음.
- 닫힘 = `RCA2-01` · `RCA2-06` · `RCA2-08` · `RCA2-09` · `RCA-06` (기존 최소 해결) · `SELF-132` · `SELF-133` (해당 수정).  부분 = `RCA2-04` (§3).
- 새 결함: P2 `RR1-01` (알려진 k=0 경계 = 같은 런 주 증서를 끝 증서로 복사해도 계약 통과 · 실제 전도도 1.707 % 차 · census 외부 결합만으로 안 닫힘) · P3 `RR1-02` (비차단 · `step3_conv_cert.py:509` 진단 합 넘침 경고 · "모든 유한 입력 무경고" 전칭 금지).
- Q9 개정 4 = 설계 방향 조건부 수용 (Q-A – Q-M 표) · 인수 조건 ① "같은 프로세스" 문구 → 같은 사슬 부모의 동결 환경 · 재개 = 새 프로세스 + 환경 지문 대조 ② 부모 사망에도 그룹 종료 확인 (별도 supervisor / recovery) ③ 구조가 같아도 최종 등급이 다르면 `REVERIFY_DIFF` 유지.
- 범위 밖 (닫지 않음) = `RCA2-02` · `03` · `05` · `07` · `RCA-11` · `RIMPR-04` · `RINT2-B01`.

## 원장 변경 (반입 커밋)

- `RCA2-01` · `RCA2-06` · `RCA2-08` · `RCA2-09` · `RCA-06` · `SELF-132` · `SELF-133` → **verified** (verified_by codex · verified_sha `9bec6b764` · verified_scope = 판정문 §2 표 줄임).
- `RCA2-04` → claimed_fixed → **open** (재개방 · 판정문 §2 · §3 · 닫는 조건 = `RR1-01` 해결).
- 새 `RR1-01` (P2) · `RR1-02` (P3) open.

## 우리 트리 재현

→ `_repro_ours_20261026/README.md` — 탐침 셋 rc 0 · **판정값 차이 0** (판정 잎 20 / 20 · 정확 유리수 비 · 조립 행렬 1,251 / 1,251 같음 · 숫자 차 = 해 반올림 끝자리).
