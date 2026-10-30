# Codex 판정 반입 — 50kg 4차년도 DEM 보고 초안 1 (10-30) = 조건부 수용

- 받은 ZIP (1저자 10-30): `codex_kg50_y4_draft1_review_52f9e87e1_20261030.zip` · 10,816,608 B · sha256 `ac8de7e35b42424c0d2926c022ea5bd80573ee1b32823574cc69941963d6bb1a` · 멤버 92 (경로 이탈 · 링크 0) · `SHA256SUMS.txt` 91 줄 = 받은 바이트 그대로 일치 — ZIP 자체는 리포 밖.  리뷰 핀 `52f9e87e1049530f66aa250156d16e0b1b4f1baa` · 검토한 우리 ZIP sha256 `ebb04443…` (`PROVENANCE.json`).
- 판정 = **조건부 수용** — 7쪽 구성 · 1쪽 비교 틀 · 2쪽 보조 그림의 계산 정의를 유지해 초안 2 를 써도 된다 · 현재 PPTX 를 최종 보고본으로 종결하는 GO 아님 · 새 P1 없음 · 새 P2 둘 (`K50Y4-01` · `02`) · P3 하나 (`K50Y4-03`) · 새 DEM 실행 · 재개 도구 · 새 수송 지표 · 입도 효과 인과 · `KG50B-*` 원장 종결 = 판정 안 함.
- 핀 뒤 1저자 결정 반영 (판정문 §2): 글꼴 · 머리 줄 · 배치 = 검토 안 함 · Q2(b) 첫 줄 = *"물성 22 GPa (랩실 표준)"* 로 평가.

## 반입 범위

| 넣음 | 뺌 (이유) |
|---|---|
| 판정문 · `README.txt` · `PROVENANCE.json` · `SHA256SUMS.txt` · `intake.json` · `remote_meta.json` · `review_probes.py` · `check_prior_deck.py` · `independent/` (32 파일 — 재계산 JSON · 덱 차이 · 쪽 글 · PDF 글 · LIGGGHTS 3d5c00f `output.cpp` · `dump.cpp` · `dump_modify.txt` 사본) | `source/` (= 우리가 보낸 ZIP 원 바이트 — 요청서 · `repo/` = 핀 blob · 끝 상태 멤버 = 리포 tgz) · `independent/reference_report_20261001_draft.pptx` (= 리포 `docs/report_20261001/report_20261001_draft.pptx` 와 같은 blob `5b63111b…` · 5.4 MB) |

- 텍스트 35 파일의 CRLF → LF (`.gitattributes` eol=lf) — `SHA256SUMS.txt` 값은 받은 바이트 기준이라 그 35 개는 다르다 (내용 같음).

## 우리 트리 재현 (`_repro_ours_20261030/`)

| 무엇 | 결과 |
|---|---|
| `review_probes.py` 그대로 (복사본 · 읽고 나서 실행 · 쓰기 = 자기 `independent/` 만 · PDF 글 = PyMuPDF) | **129/129** — Codex 와 **같은 대조 집합** (`checks_ours.json` · 순서만 다름 = 파일 나열 순서) · 요약 출력 (`run_stdout_ours.json`) = Codex `independent/run_stdout.json` 과 같음 (CR · 경고 줄 뺀 뒤) |
| `check_prior_deck.py` | 같음 (`prior_run_stdout_ours.json`) — 1.35 GPa = 발표 **9쪽** (부품 `ppt/slides/slide13.xml`) |
| `independent/` 32 파일 ↔ 우리 실행 | CR 뺀 뒤 바이트 같음 24 · 다름 8 = `checks.json` (순서) + `pdf1–7_text.txt` (PDF 글 추출기 다름) — 판정값 차이 0 |

## 원장

- 원장 ID = `K50Y4-NN` (Codex 표기 KG50Y4-NN · 원장 ID 형식 = 앞 부분 5 자 이내 · `scripts/check_review_findings.py` `ID_RE`).

| 원장 | 등급 · 상태 | 무엇 |
|---|---|---|
| `K50Y4-01` | P2 · open | 압력 도달 순간 (압축 정지 step D2 3,915,002 · D3 4,475,002) 의 atom · contact · mesh 가 출력 주기 (50,000 · 10,000 · 5,000) 의 배수가 아니라 생기지 않음 → 후속 순서 *"두 프레임 수령"* 불성립 · 재고 먼저 |
| `K50Y4-02` | P2 · open | 1.35 GPa = 선행 유효 입력 규약의 계승 — 개별 기전 · 이번 복합양극 실험 기공률 일치의 검증으로 설명하지 않음 (스토리라인 1쪽 예상 답변) |
| `K50Y4-03` | P3 · open | 선행 출처 *"13 장"* = XML 부품 번호 · 발표 9쪽 |
| `SELF-144` | P3 · open | 같은 사건의 내 검증 누락 (ZIP 발췌문에 1.35 GPa 문장이 없는 것을 못 봄) |

- 원장 908 → **912** (claimed_fixed 346 · verified 242 · open 314 · wontfix 10).
- 다음 = 수정 계획 `docs/50kg/report_y4/draft2_fix_plan_20261030.md` (1저자 Q).
