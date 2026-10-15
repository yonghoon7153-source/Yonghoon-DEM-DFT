# 연구세미나 덱 (2026-10 · 1저자 비준 개요 v1) — 생성기 · 그림 · 출처

## v3.3 (2026-10-15 · Codex v3.2 재확인 HOLD 반영 · 1저자 10-15 비준 Q1 (가) · Q2 · 18 장 · 세미나 10-16) — `build_seminar_v33.py` · `figs_v3/make_seminar_figs_v33.py` (F_p4_v33) · `slide_text_v33.md` · `slide_sources_v33.json`

- **방식** = v3.2 위의 차분이다.  `build_seminar_v33.py` 가 `build_seminar_v32.build_v32` 를 **그대로** 불러 v3.2 를 만든 뒤 3 · 5 · 7 · 11 · 13 · 15 장만 고친다 (`build_seminar_v32.py` · `build_seminar_v3.py` · `make_seminar_figs_v32.py` 무변경).  덱 · PDF · PNG = 리포 밖.
- 판정 = `docs/reviews/codex_review_seminar_v32_recheck_20261015.md` (HOLD · P2 셋 · P3 하나 · 새 계산 요구 없음) · 원장 `SEM32-01`~`04` (Codex 표기 SEMV32-NN) · `SELF-117` · 수정 계획 `docs/reviews/seminar_deck_v32_fix_plan_20261015.md` — **Q1 (가)** 식 OMML 그대로 · 출처 줄 + notes 로 고침 · **Q2** 바뀌는 장의 권고 전부 · 승계 장 4 · 6 은 손대지 않음.  문안 = 판정문 그대로 (영어).

| 장 | 고친 것 | 근거 |
|---:|---|---|
| 3 | 출처 줄 = `This work — representative equations based on LIGGGHTS-PUBLIC 3.8.0 [2]; linear hysteretic law [1]. Equation ② uses the small-overlap approximation ℓᵢⱼ ≈ Rᵢnᵢⱼ.` — 162 자라 한 줄에 안 들어가 **두 줄** (오른쪽 맞춤 · 위아래 여백 0 · 각 줄 ≤ 110 자 · 제목 위에서 끝남) · notes = "implemented equations" → 대표식 + ② 작은 겹침 근사 + 구현 지렛대 크기 Rᵢ − δᵢⱼ/2 (구형 입자 경로 `cri = radi − 0.5·deltan` · LIGGGHTS-PUBLIC 3d5c00f `surface_model_default.h` 173–188 · `tangential_model_history.h` 254–261 · `docs/dem_governing_equations_background_20261011.md` §3.1) + ④ CDT = 상대 각속도 0 에서 토크 0 (`rolling_model_cdt.h` 94 · 138) · **식 OMML 여덟 · 대체 그림 · 그림 = 바이트 그대로 (A8 16 + 2 · v3.2 와 식 C14N 같음)** | SEM32-01 · Q3 |
| 5 | notes 만: "awaiting an answer" → 큰 입자 LPSCl 펠릿 1 개 = 1저자 10-14 승인 (`docs/session_20260923_progress.md` 10-14 밤 9) · 표 그대로 | Q5 |
| 7 | 본문 1 첫 "300 MPa" → `pressed to 300 MPa (nominal stopping pressure; see Problem 4)` (줄 수 같음 · 그림 자리 같음) | 순서 질문 3 |
| 11 | 본문 2 = Codex 문안 (숫자–단위 사이 줄바꿈 금지 공백 U+00A0 하나 — 렌더에서 "105.84 / µm" 이 갈렸다 · 글자는 그대로) · 빨강 = `combined follow-up protocol` · `model-internal diagnostic` · 본문이 4 줄이라 그림 · 표 · 해석 줄을 0.30 in 아래로 (그림 크기 그대로 · 해석 줄 바닥 6.74 in) · 그림 **F_p4 → F_p4_v33** (그리는 코드 = v3.2 그대로 · (b) 에 이름표 `registered prediction band` + 지시선 · (b) y 상한 18 → 20 · 값 · 빗금 · 막대 · CSV 값 열 그대로) · 해석 줄 (b) `shaded = registered prediction band` · notes = 띠 = 결과 전 모델 예측 (실험 범위 · 신뢰구간 아님) · 내부 검사 통과 ≠ 실험 검증 · 그림 스크립트 이름 · **표 · 이력 초기화 · 13 SE 소실 공개 그대로** | SEM32-02 · §5 |
| 13 | notes 의 Kissel 2026 문장 = `Coating coverage depended on stress intensity as well as stress number; increasing stress number alone did not collapse results across rotor speeds.` | SEM32-04 |
| 15 | 흐름도 = insertion → stabilization → compression → servo → relaxation → **unloading → platen removal** (1저자 10-14 Q1 = `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` · 진행 기록 10-14 밤 7 · 상자 둘의 글만 바꿈 · 둘 다 남색 굵게) · 작은 글 `Heckel analysis to be redone` · notes 같은 순서 + `Provisional geometric calibration target; experimental definition and load state still to be matched.` (ε_union 10–13 % = 새 프로토콜의 계획된 기하 목표 · 5 장 10 % 보정 표적과 다름) — **작은 글에는 안 넣음** (단어 121 → 134 > 120) | SEM32-03 · 순서 질문 4 |
| — | ZIP v9 에 원 수식 덱 (sha256 `8e76819a…`) · 요청서의 동봉 목록과 `MANIFEST.sha256` = ZIP 실제 목록에서 생성 | SELF-117 |

- **바뀌지 않은 12 장** (1 · 2 · 4 · 6 · 8 · 9 · 10 · 12 · 14 · 16 · 17 · 18) = v3.2 와 글 run · notes · 그림 바이트 · 식이 같다 — 생성기 검사 B3 (48 건) · 독립 대조 `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/cmp_codex_v32.py` (Codex v3.2 증거 `docs/reviews/codex_seminar_v32_recheck_evidence_20261015/evidence/pptx.json` 의 읽기 규칙을 다시 구현 · Codex 스크립트는 실행하지 않음): ① 제출 v3.2 덱 (sha256 `1b6988f3…`) = Codex 읽기 18 / 18 ② v3.3 빌드 안에서 다시 만든 v3.2 = 18 / 18 ③ v3.3 의 12 장 = Codex v3.2 ④ 바뀐 6 장 = 예상한 칸만 다름 (3 글 · notes / 5 notes / 7 글 / 11 글 · notes · 그림 / 13 notes / 15 글 · notes · 3 장 식 · 그림 같음).  렌더도 14 장 (12 장 + notes 만 바뀐 5 · 13) 의 PNG (150 dpi) 가 ZIP v8 의 v3.2 PNG 와 **파일 바이트까지 같다** (3 · 7 · 11 · 15 는 고친 자리만 다르다).
- **검사 (시험 먼저)** — v3.3 검사를 구현 **전에** Codex 가 받은 v3.2 덱에 돌림: 349 건 중 33 실패 · 그림 검사 6 실패 (`docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/testfirst_v33.json`) · 렌더 검사 10 건 중 6 실패 (`testfirst_render_on_v32.json`) → 최종 검사기 = v3.2 덱 350 건 중 32 실패 (`finalchecks_on_v32.json`) · **v3.3 덱 350 건 0 실패** (`checks_v33.json`) · 렌더 10 / 10 (`render_check_v33.json`) · 동일성 (`cmp_codex_v32.json`).
  - v3.2 검사 245 는 그대로 돌고, 옛 파일 · 옛 문구를 강제하던 셋만 v3.3 판으로 바꿨다 (이유): **A9** 11 장 그림 = F_p4.png → F_p4_v33.png (띠 이름 바꾼 새 파일) · **A10 출처 줄** 한 줄 ≤ 110 자 → 줄마다 ≤ 110 자 · 3 장만 두 줄 (Codex 문장 162 자) · **A10 단어** ≤ 100 / 120 → 7 · 11 · 15 장은 Codex 필수 문안이 늘린 만큼만 넘을 수 있다 (7 = 98 → 104 / 100 · 11 = 119 → 121 / 120 · 15 = 119 → 121 / 120 — 닫힌 문장을 줄여 맞추지 않았다).
  - 새 검사 B0–B6 (105 건): 금지 문구 (`implemented equations` · `until the open checks pass` · `Heckel analysis redone` · 옛 Kissel 문장 · 15 장 relaxation 바로 뒤 platen removal · 5 장 "awaiting an answer") · 필수 Codex 문안 · 바뀌지 않은 12 장 동일 · 바뀐 장 = v3.2 + 등록한 고침만 (`SHAPE_EDITS` · `NOTE_EDITS` — 다른 글자는 한 글자도 그대로) · 3 장 출처 줄 자리 · 11 장 그림 · 표 자리 · F_p4_v33 = F_p4 값 · 빗금 + 띠 이름.
  - 시험 먼저 커밋 뒤에 고친 검사 둘: 그림 빗금 대조 = SVG `<pattern>` id 가 아니라 본문 (matplotlib 가 그릴 때마다 id 에 무작위 salt) · 11 장 본문 2 대조 = 줄바꿈 금지 공백 하나 허용 (U+00A0 → 공백으로 바꾸면 Codex 문안과 글자 같음).
- **렌더** = LibreOffice + Carlito → PDF 18 쪽 · 150 dpi PNG · `render_check_v33.py` (pdftotext 낱말 상자: 겹침 > 2 pt 0 · 쪽 밖 0 · 3 장 출처 줄이 제목 위에서 끝남 · 15 장 상자 순서 · 새 문구 렌더 · 옛 문구 없음) · 육안 3 · 5 · 7 · 11 · 13 · 15 장.  ⚠ Carlito 에 `ⱼ` (U+2C7C) 가 없어 LibreOffice 는 3 장 출처 줄 둘째 줄의 그 글자를 대체 글꼴로 그린다 (빈 네모 없음 · 10 pt 아래첨자라 작다) — PowerPoint 표시는 발표 PC 에서 3 장 식 여덟과 함께 확인.
- **양식** = 1저자 10-13 덱 (sha256 `7746e163…` · v3.2 와 같은 파일) · 원 수식 덱 = 1저자 10-09 (sha256 `8e76819a…`).
- 실행: `python3 build_seminar_v33.py --template <10-13 덱.pptx> --eq-deck <10-09 지배방정식.pptx> --repo <리포> --figs figs_v3 --lit <크롭 폴더> --out <out.pptx> --v32 <비교 v3.2 덱> --json <검사 기록> --sources-out slide_sources_v33.json` · `--selftest-only <덱> --repo <리포> --figs figs_v3 --v32 <v3.2 덱> --v31 <v3.1 덱> --eq-deck <…> [--json …]` · `--dump <덱> --out slide_text_v33.md` · 그림 = `python3 figs_v3/make_seminar_figs_v33.py figs_v3` · `--selftest <리포>`.  종결 확인 요청서 = `docs/reviews/codex_seminar_deck_v3_3_closure_request_20261015.md` (ZIP v9 · 발송 = 1저자).
- ✅ **Codex 종결 10-15 = 내용 GO** (`docs/reviews/codex_review_seminar_v33_closure_20261015.md` · 증거 `docs/reviews/codex_seminar_v33_closure_evidence_20261015/`) — SEMV32-01–04 (원장 SEM32-01–04) · SELF-117 닫힘 · verified (리뷰 핀 `aac17e11f`) · 새 P1/P2 없음 · 발표 최종 GO = 발표 PC 의 3 장 PowerPoint 표시 확인 (1저자 직접).

## v3.2 (2026-10-14 · 1저자 10-14 결정 1–9 · 18 장 · 세미나 10-16) — `build_seminar_v32.py` · `figs_v3/make_seminar_figs_v32.py` (F_p4) · `slide_text_v32.md` · `slide_sources_v32.json`

- **방식** = v3.1 덱 위의 차분이다.  `build_seminar_v32.py` 가 `build_seminar_v3.py` 를 **그대로** 불러 v3.1 (Codex 종결본) 을 만든 뒤 바뀐 장만 고치고 순서를 바꾼다 — 손대지 않은 장은 같은 코드 경로라 글이 같다.  덱 · PDF · PNG = 리포 밖 (사용자 덱 미반입 규약).
- **순서 (1저자 결정 1)** = question → model → what works → what does not → in progress → plan.  v3.1 p10 (진행 · 194-bed / 데이터셋) 은 **삭제** — 그 안의 Lee 2025 R / Q 는 9 장으로, 8 원점 연구 "보류" 는 9 장 notes 로 옮겼다 (결정 2).

| v3.2 | v3.1 | 바뀜 |
|---:|---:|---|
| 1 표지 · 2 Introduction | p01 · p02 | 없음 (다리 줄만) |
| 3 Model — DEM 지배방정식 | — | **새 장** (결정 8) |
| 4 DEM → MPM | p05 | 인용 번호만 (본문 [1, 7] → [1, 2] · notes [15] → [3]) · 다리 줄 |
| 5 MPM 입력 | p06 | 표 마지막 행 `Validation … pending` → `Lab anchor (planned)` (결정 5) · notes 덧붙임 |
| 6 Transport | p07 | 없음 (다리 줄만) |
| 7 DEM porosity | p03 | 문헌 꼬리표 (Faka 2026 [13]) · notes (Faka · Thompson) (결정 7) |
| 8 DEM 접촉망 | p04 | 없음 (다리 줄만) |
| 9 Problems 1–2 | p08 | 본문 2 = σ_VGCF* 3.41 문장 (결정 4) · Lee R / Q 두 줄 표 (결정 2) · 옛 본문 마지막 문장 → notes · notes 덧붙임 |
| 10 Problem 3 | p09 | notes 문헌 (Thompson · Faka) |
| 11 Problem 4 | — | **새 장** (결정 3) · 그림 F_p4 |
| 12–14 Mixing | p11–p13 | notes 문헌 (Hersey · Egermann & Orr · Kissel · Kim) · 14 장 꼬리표 (결정 7) |
| 15 Plan | p14 | 194-bed 결론 줄 삭제 · 언로딩 항목 · DEM 프로토콜 세대 2 (계획) (결정 6) |
| 16 Summary | p15 | "DEM loading" 한 줄 덧붙임 (**지시 목록 밖** · `SUMMARY_P4_LINE` · 끄려면 False) |
| 17 References | p16 | 인용된 것만 13 · 번호 다시 · 새 문헌 6 |
| 18 Thank you | p17 | 없음 |
| — | p10 | 삭제 |

- **인용 번호 (v3.1 → v3.2)** = [7] → [2] (LIGGGHTS) · [15] → [3] (Sakuda) · [12] → [10] (Lee) · [16] → [11] (Wang) · [1] · [8] · [9] 그대로 · v3.1 [2]–[6] · [10] · [11] · [13] · [14] = v3.1 어디에도 인용 없음 → 뺌.  새 [4] Hersey 1975 · [5] Egermann & Orr 1983 · [6] Kissel 2026 · [7] Kim 2012 · [12] Thompson 2026 · [13] Faka 2026 = litdb 정본 카드 (서지 낱말을 카드에서 대조 · [2] = 소프트웨어 고정 커밋 `docs/data/liggghts_add_pair_pin.json`).
- **3 장 지배방정식 (결정 8)** = 1저자 10-09 슬라이드 (리포 밖 업로드 · 생성기 인자 `--eq-deck`) 의 식 OMML 여덟 (`mc:AlternateContent` · Choice `Requires="a14"` · Fallback 그림) 과 그림 (힘 그림 · 판 틀) 을 관계 (`r:embed` → 새 image part) 와 함께 그대로 복사 — **다시 타이핑하지 않았다**.  검사 A8 = 식 XML C14N 바이트 같음 · 대체 그림 바이트 같음 · 그림 둘 바이트 같음 · `a14` 이름공간 유지.  바꾼 것 = 한글 라벨 → 영어 (`TRANS` 표) · 프로젝트 머리 (한글) 삭제 · 배치 (`xfrm`) · 대체 그림의 `fillRect`.  원 슬라이드는 식 무리를 가로 0.717 배로 눌러 넣었고 대체 그림도 눌린 크기에서 그려졌다 → 식 상자 폭은 원래 3.461 in 그대로 · 높이만 필요한 만큼 늘리고 `fillRect` 를 다시 계산 (전부 ≤ 0 — LibreOffice 는 양수 inset 이 섞이면 `fillRect` 를 무시한다).  출처 · 한정어 = notes (`docs/dem_governing_equations_report_20261009.md` §1 · §3 · `docs/dem_governing_equations_background_20261011.md` §2.3 · §3.1 · §5.2 · §5.3 · §6 · §7 · §8.2 · §9 · §11 · DEMP-01 open · [2] · [1]).
  ⚠ LibreOffice 는 OMML 이 아니라 **대체 그림**을 그린다 → PDF · PNG 의 식 = 대체 그림이다.  PowerPoint 는 OMML 을 그린다 — **우리 PowerPoint 렌더 없음** (발표 PC 에서 3 장 확인 필요).  LO 렌더에서 ④ 첫 식 끝 "|" 가 그림 가장자리에 붙어 보인다 (LO 만).
- **11 장 Problem 4 (결정 3)** = `docs/reviews/findings.json` DEMP-01 · MV-01 · MV-02 · MV-08 (open) · `docs/data/ps73_damping_branch_20261007/README.md` §1 · §4 · §12-4 · `docs/reviews/codex_review_model_validation_20261008.md` Q11 문안.  그림 F_p4 = README 기록 문자열만 (`figs_v3/make_seminar_figs_v32.py --selftest` = README · DEMP-01 대조 · 금지어 · 글 상자 겹침 0 · "static" 없음).  "static 300 MPa" 는 notes 의 조건문 (Codex Q11 문안) 안에만.
- **다리 줄** = 내용 장 2–16 · 바닥글 띠 같은 자리 (3.70, 7.02 in · 5.60 × 0.28) · 12 pt 기울임 · 한 줄 · 숫자 없음 · 장 밖 주장 없음 (`BRIDGES`).
- **검사 (시험 먼저)** — 구현 전 v3.1 덱에 v3.2 검사를 돌려 실패를 먼저 봤다: 202 건 중 125 실패 (`docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_2_fix/testfirst_v32.json`).  최종 검사기 = v3.1 덱 204 건 중 124 실패 (`finalchecks_on_v31.json`) · **v3.2 덱 245 건 0 실패** (`checks_v32.json`).  항목 = 장 수 · 절 / 제목 · 194 / LHS / ML / 데이터셋 / Latin 없음 (14 장 notes 의 접착 산술 "about 194×" 하나만 예외) · 다리 줄 · 손대지 않은 장 동일 · 참고문헌 ↔ 정본 카드 · 필수 / 금지 문구 · 식 복사 · F_p4 값 · 철회값 · 단어 ≤ 100 / 120 · 글꼴 · 겹침 · 바닥 · 도형 id 유일 · notes 의 리포 경로 실재.
- **v3.1 과의 동일성** (Codex 종결 §6 승계 조건 1) — 같은 폴더 `cmp_codex_v31.py` · `cmp_codex_v31.json`: 다시 만든 v3.1 덱 = Codex 종결 v3.1 PPTX (sha256 `73fa2dc3…`) 와 17 / 17 장 글 run · notes · 그림 바이트가 같다 (Codex 증거 `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_1_closure/evidence/pptx.json` 대조) · v3.2 의 손대지 않은 6 장 (1 · 2 · 4 · 6 · 8 · 18) 도 같다 (인용 번호 바꿈 적용 · 다리 줄 제외).  ⚠ PPTX 는 python-pptx 저장이라 해시가 빌드마다 다르다 — 동일성은 내용 대조로만 말한다.
- **렌더** = LibreOffice + Carlito → PDF 18 쪽 · 150 dpi PNG 18 장 · 육안 확인 (3 · 5 · 9 · 11 · 14 · 15 · 17 장 포함) · 덱 · PDF · 원 슬라이드 해시 = 재확인 요청서 §0.
- **장 순서에서 생기는 논리 문제 (순서는 1저자 결정대로 두었다)**: ① 6 장 (Transport) 의 발표자 그림 (i) = 7:3 침대의 접촉망 전류 경로인데, 접촉망 (8 장) 과 7:3 침대 (7 장) 는 그 뒤에 나온다 · ② 4 장의 Luding 크롭 (이력 법칙) 은 3 장 식 ③ 과 겹치고, 4 장 notes 의 "감쇠 58 %" 는 11 장과 겹친다 (손대지 않은 장이라 그대로) · ③ porosity (7 장) · 하중 분담 (10 장) 은 "300 MPa" 를 쓰고 그 명목 압력의 속은 11 장에서 나온다 (11 장 notes 에 "세대 1" 표지) · ④ 5 장 표의 보정 표적 "10 % at 300 MPa" (CL-94 · 우리 보정 표적) 과 15 장 세대 2 계획의 "ε_union 10–13 %" 는 다른 목표다 (계획 = 1저자 10-14 지시).
- **리포 기록에 아직 없는 것 (1저자 지시에서 옴)**: 15 장 "ε_sphere kept internally" · "Heckel analysis redone" · 5 장 큰 입자 LPSCl 펠릿 (진행 기록 10-14 저녁 = 권고 · "답 대기") — 커밋 때 진행 기록에 한 줄.  언로딩 수정 계획 파일 머리는 아직 "1저자 비준 전" (진행 기록 10-14 오후 2 = 비준).
- 실행: `python3 build_seminar_v32.py --template <10-13 덱.pptx> --eq-deck <10-09 지배방정식.pptx> --repo <리포> --figs figs_v3 --lit <크롭 폴더> --out <out.pptx> --v31 <v3.1 덱 사본 경로> --json <검사 기록> --sources-out slide_sources_v32.json` · `--selftest-only <덱> --repo . --figs figs_v3 --v31 <v3.1 덱> --eq-deck <…>` · `--dump <덱> --out slide_text_v32.md`.  재확인 요청서 = `docs/reviews/codex_seminar_deck_v3_2_recheck_request_20261014.md`.

## v3.1 (2026-10-13 · Codex v3 재확인 = 조건부 GO 반영) — 같은 파일 (`build_seminar_v3.py` · `figs_v3/` · `slide_text_v3.md` = v3.1 글 전문 · `slide_sources_v3.json`)

- 판정 = `docs/reviews/codex_review_seminar_deck_v3_recheck_20261013.md` (증거 `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_recheck/`) · 원장 `SEMV3-01`~`10` · `SELF-111`.  새 시뮬레이션 · 값 변경 없음 — 출처 · 비교군 이름 · 배율 정의 · 결론 강도 · 반올림 · 조판만.
- 6 장 · [9] = So et al., **J. Electrochem. Soc. 168, 030538 (2021), Fig. 4a** (크롭의 정본 출처 · 옛 JPS 인용 = 다른 논문) · 크롭 오른쪽 경계 0.475 → 0.515 (500 MPa 눈금까지).  덱에는 DOI 를 쓰지 않는다 (정본 카드 머리 DOI ↔ 출판사 DOI 어긋남 = litdb 원문 확인 전).
- 믹서 11–13 장: 작지만 0 아닌 비교군 = **low NCM–NCM cohesion · low-cohesion comparator** (`no cohesion (control)` = 따로 있는 음성 대조만) · 11 장 제목 = *unresolved mixing-index contrast* + 화면 한정 (후속 진단 분류 · 원 등록 1 % 겹침 조건 미충족) · 12 장 = 두 계열을 따로 정의 (큰 NCM 자기쌍 model Bond number 38.4 / 384 / 1152 ↔ all-pair CED ×10 / ×14.42) · 인과 제목 철회 · 13 장 = 접착일 식의 가정 (기하평균 결합 · 같은 접촉 면적 · J m⁻²) 과 조건부 해석 · 15 장 요약 교체.
- 반올림 = 판독 JSON 에서 직접 (`dev_planned_m` · `dev_delta_m` · `dev_cluster` — README 요약값을 베끼지 않는다): Bo 384 12×12×3 **0.927** · CED ×14.42 16×16×4 **0.865** · 비교군 군집 **0.400**.
- 7 장 해석 줄 = 원판 Phase A (VGCF E = 10 GPa) · 96 팔 평균 · 100 GPa 재현은 notes.  9 장 = 일치 대상 = *experimental porosity summaries* (선택된 다섯 조성 · 탐색).  10 장 = *order-of-magnitude agreement* · 비관통 표지 = *display position only* · 범례 대신 직접 라벨.
- selftest 추가 (생성기): 장별 금지 문구 (본문 · notes) · 장별 필수 문구 (본문 · notes) · 12 장 전용 금지어.  그림 selftest 추가: 그려진 모든 글 상자의 겹침 0 · 믹서 그림 라벨 (0 점착 표현 금지 · Bo / CED 구분 · 도식 가정) · 판독 JSON 값 고정 검사.  **고치기 전 실패 확인** = 새 검사를 Codex 가 받은 v3 덱 (sha256 `baf2bb98…`) 과 v3 커밋 (`0c6f5c84e`) 의 그림 스크립트에 돌린 기록 `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_1_fix/testfirst_v31.json` (하네스 = 같은 폴더 `testfirst_v31.py` · 덱 31 건 = 금지 문구 16 · 필수 문구 누락 15 · 그림 21 건 = 글자 겹침 7 쌍 · 라벨 13 · CSV 값 1 → v3.1 덱 0 건 · v3.1 그림 = 그림 selftest 통과).
- 그림 배치 배율 (덱에 놓인 폭 ÷ 그림 원래 폭) = F_poro 1.024 · F_trans 0.895 · F_vgcf 0.984 · F_limits 0.846 · F_load 0.960 · F_dataset 0.974 · F_mix1 · F_mix2 · F_mix3 1.011 · 도식 0.963 ⇒ 배치 뒤 가장 작은 글씨 = 4 장 조성 눈금 8.5 pt · 8 장 (c) 조성 눈금 · 범례 8.9 pt · 믹서 그림 ≥ 10.1 pt.  ⚠ 아래 v3 절의 *"글씨 = 배치 1:1 ≈ 12 pt"* 는 4 · 8 장에서 틀린 서술이다 (이번에 글씨 크기는 바꾸지 않음 · 요청서 Q5).
- 선택 개선 (P2) 중 미적용 = 9 장 색막대 (1저자 비준 ps73 최종 판 그림 · 해석 줄에 0–150 MPa) · 5 장 감쇠 58 % · 6 장 실행 상태의 화면 복구 (Codex: 필수 아님).
- ✅ 1저자 10-13 = 8–10 장 축소 안 함 (17 장 최종) → 종결 확인 묶음 ZIP v7 (요청서 `docs/reviews/codex_seminar_deck_v3_1_closure_request_20261013.md`).
- ✅ **Codex 종결 10-13 = GO** (`docs/reviews/codex_review_seminar_deck_v3_1_closure_20261013.md` · 증거 `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_1_closure/`) — SEMV3-01~10 닫힘 · 원장 SEM-01~14 · SEMV2-01~07 · SEMV3-01~10 · SELF-110 · 111 = verified (발표물 범위) · 발표 전 = p4 · p8 그림 글씨 (8.5 · 8.9 pt) 를 발표장 화면에서 확인 · PowerPoint 로 열 때 글꼴 대체로 줄바꿈이 바뀌는지 확인 · 비차단 잔여 `SEMV3-11` (생성기 머리말 주석 `:13` 옛 용어 — 출력 무관 · 다음 유지보수).

## v3 "보는 판" (2026-10-13 밤 · 1저자 지시) — `build_seminar_v3.py` · `figs_v3/` · `slide_text_v3.md` · `slide_sources_v3.json`

- 장 문법 = 10-13 덱 4 장: ■ 제목 **한 줄** + 소불릿 ≤ 2 (15 pt · 핵심어 빨강) + 그림 한 띠 (본문 높이 추정값 아래 · 바닥 6.45 in) + 우상단 출처 줄 (10 pt 기울임 · ≤ 110 자) + 그림 아래 해석 조건 한 줄 (12 pt 회색 · 꺾쇠 캡션 없음) · 문헌 크롭 = 위 꼬리표 + 아래 출처.  **빈 자리 = 도형 없음** — 출처 줄의 `figure: presenter — …` 가 무엇을 붙일지 적는다 (5 장 우 = MPM 3D · 7 장 좌 = 3D 전류 흐름 (접촉망 · 복셀) · 11 장 우 = 층상 침대 전 · 후 · 12 장 우 = 침대 스냅샷).
- 17 장 = 표지 · Introduction (흐름도 = PPT 도형) · DEM 2 · DEM → MPM · MPM (표 + 문헌) · Transport · Limits 2 · Progress (표 + 산점) · **Mixing 3** · Plan · Summary · References 16 (불변) · Thank you.  v2.1 → v3 대응표 = `docs/reviews/codex_seminar_deck_v3_recheck_request_20261013.md` §1 (Codex 가 닫은 값 · 문장은 그대로 · 옮긴 문장은 notes 전문).
- 그림 10 = `figs_v3/make_seminar_figs.py` (`--selftest` = 정본값 대조: `docs/report_20261021/summary.json` G1 · G6 · G7 · ps45 README · `plane_load.json` · 인자 끔 README · CL-24 공개값 · DC 분극 등록 · 믹서 prelim README 셋 · 철회값 0 · 팔 코드 0 · 조성 라벨 5) — F_poro · F_trans · F_limits (a b c) · F_load · F_vgcf · F_dataset (배포 v1.2 CSV 직접) · F_mix1 · F_mix2 · F_mix3 · F_mix3_scheme · 글씨 = 배치 1:1 ≈ 12 pt · png + svg + csv.
- 문헌 크롭 3 = litdb 정본 브랜치 `litdb/figures/` 의 Bazzoun 2026 Fig. 2 · Luding 2008 Fig. 1 · So 2021 Fig. 4 (a 패널만 잘라) — 생성기가 빌드 때 `git show` 로 `--lit` 폴더에 받는다 (리포에 사본 없음).  Lee 2025 = 미배치 (1저자 10-13 결정 · [12] 는 10 장 상태표 · 참고문헌으로만).
- 믹서 용어 = 분야 표준 (팔 코드 없음 — selftest 가 notes 까지 검사): cohesive / non-cohesive NCM · Bond number · Lacey mixing index M · bin grid · registered "no segregation" category (not "no effect") · 개발 런 = 그림 + 한정어 (숫자는 notes).
- selftest (v2.1 항목 + 추가 · 고치기 전 = v2.1 덱에서 실패 확인): 17 장 · 꺾쇠 캡션 0 · 빈 자리 장의 출처 줄 · 출처 줄 ≤ 110 자 · 제목 한 줄 (≤ 62 자 · 글꼴 폭) · **겹침 검사** (본문 바닥 추정 ≤ 그림 띠 윗선 — 줄바꿈 = Carlito (Calibri 폭) 로 잰다 · 없으면 DejaVu = 보수적) · 단어 ≤ 100/120 (출처 줄 · 꼬리표 · 표 제외) · bullet ≥ 15 pt · 해석 줄 ≥ 12 pt · 10 장 해석 줄 ↔ 집단 · 11 장 등록 범주 문구.
- 렌더 QA = LibreOffice + Carlito (fonts-crosextra-carlito · Calibri 와 폭 같음) → 17 장 겹침 0.  덱 · PDF 는 리포 밖 (ZIP v6 = Codex · 1저자).
- 실행: `python3 build_seminar_v3.py --template <10-13 덱.pptx> --repo <리포> --figs figs_v3 --out <폴더>/seminar_20261013_v3.pptx` (크롭은 `<폴더>/lit` 에 자동 수령) · `--selftest-only <덱> --repo <리포> --figs figs_v3` · `--dump <덱> --out slide_text_v3.md`.

## v2.1 까지 (아래 = 10-13 낮 판 · 역사)

- **덱 pptx 는 리포에 없다** (사용자 덱 미반입 규약) — 1저자에게 전달 · Codex 검토 ZIP 으로.  글의 정본 사본 = `slide_text_draft3.md` (장별 전문 + 발표자 메모).
- 흐름 (1저자 지정) = ① 파이프라인 → ② DEM 한계 → ③ MPM · SE 물성 · DEM↔MPM → ④ voxelization → ⑤ 첨가제 → ⑥ 문제 셋 → ⑦ 진행 → ⑧ 계획 · 본문 15 장 (2–16) + 표지 · 요약 · 참고문헌 · 끝 = 19 장.
- 양식 = 1저자 10-13 연구세미나 덱 (Codex 리뷰를 거친 밀도 · 리포 밖) 의 장을 프로토타입으로 복제 — 표지 · 그림 본문 · 두 칸 · 점선 틀 · 요약 · 참고문헌 · Thank you.

| 파일 | 내용 |
|---|---|
| `build_seminar.py` | 생성기 — `python3 build_seminar.py --template <10-13 덱.pptx> --repo <리포> --figs figs --out <out.pptx>` · 끝에 selftest (철회값 42 패턴 0 · 본문 내부 용어 0 · 19 장) |
| `figs/make_seminar_figs.py` | 새 그림 4 (파이프라인 · 격자 비 · 모델 vs 실험 σ_e · ps45 σ_e) — `--selftest` = 정본값 대조 + 철회값 스윕 · png + svg + csv |
| `slide_sources.json` | 장별 수치 출처 (생성기가 쓴다) |
| `slide_text_draft3.md` | 장별 글 전문 (자리 표시 글 · notes 포함) |
| `outline_v1.md` | 비준 개요 (10-13) |

## 재사용한 리포 그림 (덱 안 그대로 · 값 세대)

| 장 | 그림 | 출처 |
|---|---|---|
| 3 | ps73 네 단계 3D (porosity exact union) · G1 | `docs/data/ps73_compaction_curve_20261006/stages_20261012/aligned_ckpt/t1_geometry/` · `docs/report_20261021/previews/G1.png` |
| 4 | p14 수송 tortuosity (Hertz) · p15 σLi⁺ (σ₀ 1.5) | `docs/data/ps45_r45_network_g2_20261007/deck_p14p15_20261012/` |
| 5 | 이력 법선력 (코드 재현) | `docs/data/dem_governing_equations_report_20261011/fig2_hysteresis_cycle.png` |
| 10 | 첨가제 모식도 둘 · G6 | `docs/figures/additive_seed_vgcf_ptfe.png` · `additives_preview.png` · `docs/report_20261021/previews/G6.png` |
| 13 | 단면 하중 몫 · SE σ_VM 4 단계 (0–150 MPa 선형) | `docs/data/ps45_plane_load_20261007/slide/contribution_sigma_zz.png` · `docs/data/ps73_compaction_curve_20261006/stages_20261012/aligned_ckpt/t3_vm_se/…_4panel_nowall_linear_0_150_preview.png` |
| 15 | G5a · G5b · G3 | `docs/report_20261021/previews/` |

## 자리 표시 (리포에 없는 그림 — 1저자 10-13 *"공백에 글 포함해서 나중에 검토할 때 추가되게"*)

| 장 | 무엇 | 출처 · 명령 |
|---|---|---|
| 4 | 7:3 침대 실제 전류 경로 3D (이온 · Hertz · 전류 몫 50 %) | `scripts/network_current.py dump <ps45 7:3 결과 폴더>` → 웹앱 DEM 3D "⚡ 전류 흐름" 캡처 (WSL) |
| 6 | MPM 2D champion morphology (E 1.53 · σy 0.15) · 3D scaffold x–z 단면 | uma `~/work/mpm/vis_/viszoom_E1.53_sy0.15.png` · `scripts/viz_mpm_morphology.py <mpm run dir> --slice xz` |
| 8 | DEM-scaffold MPM 응력 정지 단면 ↔ DEM 침대 나란히 | 같은 스크립트 (real_14 · n_grid 384) + `docs/data/real14_reference_20260928` 덤프 |
| 9 | 복셀 상 격자 단면 · 전류 밀도 (원고 S16/S17) | STEP3 phase grid (`scripts/step3_sigma.py`) · 원고 SI 그림 (리포 밖) |

## 지킨 것

- 철회값 (`docs/reviews/claims.json` `quotation_ban`) 0 · 8팔 계열 비 · 이득 (CL-33 · CL-41 hold) 안 씀 — 절차 · 판정만 · 순수 SE 10 % = 보정 표적 (외부 앵커 아님 · CL-94) · 격자 비는 CL-24 공개값만.
- 수치는 전부 정본 문서에서 — `slide_sources.json` · 각 장 notes.  참고문헌 14 = litdb 정본 카드 서지 그대로.
- Codex 검토 요청서 = `docs/reviews/codex_seminar_deck_review_request_20261013.md` (발송 = 1저자).

## v2 (2026-10-13 · Codex NO-GO 판정 반영 · 1저자 Q1–Q6)

- 판정 = `docs/reviews/codex_review_seminar_deck_20261013.md` (첫 판 · SEM-01~14) + `codex_review_seminar_deck_v3_20261013.md` (통합 판정) · 계획 `docs/reviews/seminar_deck_fix_plan_20261013.md` · 재확인 요청서 `docs/reviews/codex_seminar_deck_v2_recheck_request_20261013.md` (대응표 SEM ↔ v2 · 발송 = 1저자).
- 1저자 결정: Q1 7 장 E ≈ **22 GPa** (우리 DFT E_VRH · DEM 문헌 입력 22.1 GPa [8]; Sakuda 24 GPa 유리값 = notes) · Q2 8 장 30.7 비교 삭제 (상태표 · 새 숫자 없음) · Q3 자리 표시 = 한 줄 라벨 + 명령 notes · Q4 14 장 상태표 다섯 행 · Q5 `transport tortuosity` + 정의식 · Q6 v2 → Codex 재확인.
- 생성기 v2: ■ 제목 18 pt (상속) · 본문 15 pt (125 % · 뒤 5 pt) · 캡션 12 pt · 그림 위로 · Codex §9 좌표.  **selftest (고치기 전 덱에서 실패 확인 뒤 고침)** = 지적 문구 16 본문 금지 · F4 조성 라벨 5 (svg) · 장당 단어 ≤ 100 (두 칸 · 점선 장 ≤ 120 · 자리 표시 제외) · bullet ≥ 15 pt · 캡션 ≥ 12 pt · 금지값 42 · 내부 용어 (`uma` · `WSL` 포함) 0 · 19 장.
- 새 그림 v2: F2–F4 글씨 = 최종 배치 기준 ≈ 12 pt · F4 라벨 5/5 (`_fmt` 의 x locator 를 범주 축에 안 씀 — 옛 판 결함 SEM-09) · F1 상자 문구 축약 + 띠 = 보정 **표적**.  값 불변 (selftest 정본 대조).
- 글 전문 v2 = `slide_text_v2.md` (덱에서 추출 · notes 포함) · `slide_text_draft3.md` = 초안 4 (역사).  참고문헌 16 (+ [15] Sakuda 2013 · [16] Wang 2018 — 정본 카드).
- 덱 pptx · PDF · 렌더 = 리포 밖 (ZIP v4) — Codex 재확인은 **수정 PPT + 그 PDF** 로.
- **v2.1 (10-13 · Codex 재확인 = 조건부 GO · `docs/reviews/codex_review_seminar_deck_v2_recheck_20261013.md`)**: P0 = p8 현재 등록 런 = **stress-controlled servo** (fixed-platen hold 오기 · SEMV2-01) · p15 캡션 집단 정정 (왼쪽 G5a = 130 + 64 · 오른쪽 G3 = 130 · SEMV2-02) · P1 = p12 축 제목 두 줄 + 조건 캡션 3 줄 · p2 F1 상자 안 줄바꿈 · p5 notes E_VRH = Young's modulus (K/B0 별도) · p7 미확인 σy 범위 삭제 · 철회 이력 · 중복 → notes · p4 `[8]` = 방법 · σ₀ 1.5 = chosen reference · p14 소개 문장 축약.  selftest 에 `fixed-platen hold` · `σy 0.05–0.30` 금지 + p15 캡션 ↔ 집단 검사 추가 (v2 덱에서 실패 확인).  글 전문 = `slide_text_v2.md` (v2.1 로 갱신).
