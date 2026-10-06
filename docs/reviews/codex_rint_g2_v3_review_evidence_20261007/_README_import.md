# Codex Rint G2 v3 재검토 (2026-10-07) — 반입 기록

- 판정문: `docs/reviews/codex_review_rint_g2_v3_20261007.md` (= zip 의 같은 이름 파일 · 바이트 그대로 · 220 행 · 24,355 B · sha256 `913a8339a7a58c38c9daee066e46c349b80463a10d7c11eb29ec9f5ea8719005`) — **반례 개발 GO · `RINTV3-01` · `02` 계약 정정 뒤 AM–AM ①′ 구현 GO · ①′ 정량 채택 · 생산 HOLD** · 새 생산 P1 없음 · 기존 `RINTG-01` 부분 · `02`~`10` 설계 수준 닫힘 (판정문 §0 · §1 · §11).
- 받은 묶음: `codex_rint_g2_v3_review_20261007.zip` (1저자 전달 · 업로드 이름 `93cbdb56-codex_rint_g2_v3_review_20261007.zip`) · **218,237 B · sha256 `24116911daefaebdb631b6157a49c9e82bc683e745a09472cf94fac594ef4ac7`** · 18 항목 — 정규 파일만 (모드 0644) · 절대 경로 · `..` · 링크 · 암호화 항목 없음 (목록 먼저 확인한 뒤 리포 밖 빈 폴더에 풀었다).
- 묶음 안 `package_manifest.json` (Codex `package_review.py` 산출 · 자기 자신은 해시하지 않음) 17 행의 sha256 · 크기 **17/17 일치** · 목록 밖 파일 0 · 빠진 파일 0.
- 핀: `c3ff4408c513f8fea78eb342619a185b13184d41` (v3 초안 + 재검토 요청서 반입 커밋) — `source_manifest.json` 9 파일의 Git blob = zip `source/` 사본 = 핀 = 재현 시점 우리 HEAD `2802c649e` (9/9 · 아래 표).
- 원장 ID: Codex 표기 `RINTV3-01`~`03` 은 원장 ID 형식 (`scripts/check_review_findings.py` 의 `ID_RE` — 하이픈 앞 최대 5 자) 을 넘는다 (`RINTV3` = 6 자) → 원장 **`RINTV-01`~`03`** (제목 머리 "(Codex 표기 RINTV3-NN)") — 10-06 의 `RINTG2-NN` → `RINTG-NN` 과 같은 처리.
- 우리 트리 재현: `_reproduction_ours/README.md` — **판정값 차이 0** (숫자 키 192/194 · 92/97 비트 동일 · 나머지 7 = lstsq · CG 끝자리).
- 계약 정정 (1저자 비준 10-07 · 권고대로): `docs/reviews/contact_resistance_pipeline_draft_v3_1_20261007.md`.

## 묶음 18 항목과 처리

| zip 항목 | B | 내용 해시 sha256 (앞 8 자) | 처리 |
|---|---:|---|---|
| `codex_review_rint_g2_v3_20261007.md` | 24,355 | 913a8339… | → `docs/reviews/codex_review_rint_g2_v3_20261007.md` (바이트 그대로) |
| `README.md` | 4,416 | bd0892c9… | → 이 폴더 (Codex 묶음 설명 · 바이트 그대로 — ⚠ 그 "재현" 절의 `python -B probe_v3.py` 를 **이 폴더에서 하지 말 것**: 아래) |
| `probe_v3.py` | 12,610 | 6a330168… | → 이 폴더 |
| `probe_prior.py` | 7,503 | 53397815… | → 이 폴더 — `docs/reviews/codex_rint_g2_design_review_evidence_20261006/probe_design.py` 와 **바이트 같음** (10-06 탐침을 새 핀에서 다시 돌린 것) |
| `evidence_v3.json` | 9,079 | 22f30296… | → 이 폴더 (Codex 원본 · Windows 실행) |
| `evidence.json` | 6,726 | ec5919e4… | → 이 폴더 (Codex 원본) |
| `source_manifest.json` | 1,265 | adcfc19f… | → 이 폴더 (핀 · 9 파일 Git blob) |
| `package_manifest.json` | 3,413 | 95693b51… (자기 해시 행 없음) | → 이 폴더 (위 17/17 대조에 씀 · 옮긴 · 뺀 파일 행도 그대로 남는다) |
| `package_review.py` | 4,825 | 76c55a49… | **안 넣음** — 포장 · 완결성 검사 도구 (도구 설명 = completeness/integrity 검사 · scientific validity 아님) · 실행하면 상위 폴더 (= `docs/reviews/`) 에 zip · 영수증을 쓴다 |
| `source/` 9 파일 (`AGENTS.md` · 문서 5 · 코드 3) | 486,647 | 각 = `evidence*.json` 의 `source_verification` | **안 넣음** — 리포 파일 사본 · blob = 핀 (9/9) · `git archive c3ff4408c <경로>` 또는 `git cat-file blob c3ff4408c:<경로>` 로 복원 |

## 핀 대조 — zip `source/` 사본 = 핀 blob = 재현 시점 HEAD (9/9)

zip 사본의 바이트에서 Git blob 을 다시 계산해 `source_manifest.json` · `git ls-tree c3ff4408c` · `git ls-tree 2802c649e` 셋에 대조했다.

| 파일 | Git blob (핀 = manifest = zip 사본) | 재현 시점 HEAD (2802c649e) |
|---|---|---|
| `docs/reviews/codex_review_rint_g2_design_20261006.md` | blob `d4a2b26595b98671bc0f9085ec6c0bfb7c99a99d` | 같음 |
| `AGENTS.md` | blob `2829b46196a08ffae439ddbdc20dc093cde511c4` | 같음 |
| `docs/reviews/contact_resistance_pipeline_draft_v3_20261006.md` | blob `21558d722d0139556b4dc6d19ed8966a466d22ea` | 같음 (⚠ 이 반입에서 L3 한 줄이 바뀐다 — v3.1 포인터) |
| `docs/reviews/contact_resistance_pipeline_draft_v2_20261006.md` | blob `b0f9e2789480e2a53cc4267b6390eb715493bca4` | 같음 |
| `docs/reviews/contact_resistance_pipeline_draft_20261002.md` | blob `30f14ecf5c2f32a65795fc5e56ae6c79fd2fdaba` | 같음 |
| `docs/reviews/codex_rint_g2_rereview_request_20261006.md` | blob `c9ae2ec904d11a5edf67f583d69a5efddbb9f9cd` | 같음 (내용 해시 sha256 649bc7a3… = 판정문 §0 의 첨부 요청서) |
| `scripts/step3_sigma.py` | blob `4b33c7a4526f2d55dfbdefa3257e36619a9e4136` | 같음 |
| `scripts/lens_geometry.py` | blob `53a20c31554740957c21a0fa52362df0b000cc97` | 같음 |
| `scripts/se_material.py` | blob `506caca0f8744ee89836a026685f0730ef478f94` | 같음 |

⇒ 계산에 쓰이는 코드 세 파일은 핀 · HEAD 가 같다 (10-06 반입 때와도 같은 blob).  v3 sha256 `2fa89aaf…` = 판정문 §0 의 값.

## 이 폴더에서 탐침을 돌리지 말 것

탐침은 `Path(__file__).parent` 옆의 `evidence*.json` 을 덮어쓰고 (Codex 원본이 사라진다), 같은 자리의 `source/scripts` 에서 `step3_sigma` 를 import 한다 (이 폴더에는 `source/` 가 없다).  다시 돌리는 법 = `_reproduction_ours/README.md` (탐침 사본을 리포 밖 빈 폴더에서 `python3 -I -B` 로 · 핀 9 파일).

## 한정 (Codex 그대로)

- 탐침 둘 = 합성 입력 · 해석식 + 고정 소스의 실제 함수 소규모 검사 — **v3 owner · CNC · RRM 의 새 구현 시험이 아니다** · 실침대 캠페인 · GPU 런 · 리포 수정 · 원장 변경은 Codex 가 하지 않았다 (판정문 §0).
- 두 탐침의 rc 0 과 포장 검사 PASS = 증거 재현 · 무결성 성공이지 G2 구현 · 물성 · 생산 GO 증서가 아니다 (묶음 README).
- 판정문 안 GitHub 링크는 핀 고정이다 (`v3:L…` = 핀의 줄).
