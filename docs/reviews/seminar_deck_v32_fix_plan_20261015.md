# 연구세미나 덱 v3.2 — Codex 재확인 (10-15 · HOLD) 반영 수정 계획 (결과 0 건 · ⬜ 1저자 비준 대기)

> 근거 = `docs/reviews/codex_review_seminar_v32_recheck_20261015.md` (소스 핀 `90ca2c8cd` · **HOLD** · 새 P1 없음 · P2 셋 · P3 하나 · 수치 재계산 · 새 시뮬레이션 요구 없음) ·
> 증거 `docs/reviews/codex_seminar_v32_recheck_evidence_20261015/` (미니 묶음 · 반입 기록 `_README_import.md`).
> 대상 = 덱 v3.2 (18 장 · `docs/seminar_20261013/build_seminar_v32.py` · `docs/seminar_20261013/slide_text_v32.md`) · 세미나 10-16.
> 장 번호 = 실제 덱의 장 순서 (판정문과 같다 · 3 장 = PPTX 안 `slide18.xml`).

## 1. 결함 · 최소 해결 (판정문 §3 그대로)

- 원장 ID = `SEM32-NN` (Codex 표기 SEMV32-NN — 원장 ID 형식은 앞 글자 5 자까지 · `RINTG2` → `RINTG` 와 같은 처리).

| ID | 결함 | 자리 (`slide_text_v32.md`) | 최소 해결 (Codex 문안) |
|---|---|---|---|
| `SEM32-01` (Codex SEMV32-01) P2 | 3 장 ② 회전식이 작은 겹침 근사 (Rᵢnᵢⱼ × Fₜ,ᵢⱼ) 인데 판 전체를 "implemented equations" 라 부름 — 고정 LIGGGHTS 구형 입자 경로의 지렛대 크기 = Rᵢ − δᵢⱼ/2 (`surface_model_default.h` 173–188 · `tangential_model_history.h` 254–261) · 구별용 합성 검산 0.45 ↔ 0.50 µN·µm (11.1 %) | 44 (출처 줄) · 89 (notes) | 출처 줄 = *"Representative equations based on LIGGGHTS-PUBLIC 3.8.0 [2]; linear hysteretic law [1]. Equation ② uses the small-overlap approximation ℓᵢⱼ ≈ Rᵢnᵢⱼ."* · notes 에 구현 크기 Rᵢ − δᵢⱼ/2 (우리 배경 보고서 `docs/dem_governing_equations_background_20261011.md` 103–105 와 같은 구별) |
| `SEM32-02` (Codex SEMV32-02) P2 | 11 장 "model-internal until the open checks pass" — 내부 평형 · 보존 검사 통과가 실험 검증으로 이어지는 듯 읽힘 (B = 이력 초기화 · 감쇠 · 힘 유지 복합 개입은 이미 공개 = 새 P1 아님) | 196 | 본문 2 = *"At fixed platen, the original run relaxes to 165 MPa. A combined follow-up protocol—plate-contact history reset, lower damping and force hold—reduces thickness from 111.05 to 105.84 µm. This remains a model-internal diagnostic; static-equilibrium and conservation checks are pending."* · 기존 이력 초기화 · 13 SE 소실 표 · notes 유지 |
| `SEM32-03` (Codex SEMV32-03) P2 | 15 장 흐름도 · notes 의 마지막 두 단계가 비준 순서와 반대 (덱 = relaxation → platen removal → unloading · 비준 = 이완 → 언로딩 → 판 분리 · `docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` 437 · 454 · `docs/session_20260923_progress.md` 1067 — 줄 번호 = 핀 `90ca2c8cd`) | 265–269 · notes | 흐름도 = insertion → stabilization → compression → servo → relaxation → unloading → platen removal · notes 같게 · "Heckel analysis redone" → **"Heckel analysis to be redone"** |
| `SEM32-04` (Codex SEMV32-04) P3 | 13 장 notes 의 Kissel 2026 요약 "coverage followed the stress intensity rather than the number of stress events" — 응력 횟수 영향을 배제하는 것처럼 읽힘 (원문 Fig. 6c,d) | 231 | *"Coating coverage depended on stress intensity as well as stress number; increasing stress number alone did not collapse results across rotor speeds."* |
| `SELF-117` P3 | 요청서 §6 이 원 수식 PPTX (`8e76819a…`) 를 ZIP v8 에 넣었다고 적었는데 없었다 → A8 (원본 대비 8/8 XML · 그림 동일) 재현 불가 (판정문 §2 · 포장 누락만으로 수식 오류 판정은 아님) | ZIP v8 | 다음 ZIP (v9) 에 원 수식 PPTX + sha256 · 요청서 목록을 ZIP 실제 목록에서 만든다 |

## 2. 권고 (비차단 · 판정문 §4 · §5 · §6)

| 장 | 권고 (Codex 문안) | 비고 |
|---|---|---|
| 3 notes | ④ CDT — 상대 각속도 0 에서 토크 0 | Q3 답 |
| 5 notes | 대립 SE 1 개 추가 = 1저자 10-14 승인 (`docs/session_20260923_progress.md` · 판정문 Q5) — "답 대기" 갱신 | Q5 답 |
| 7 (첫 300 MPa 언급) | *"nominal stopping pressure; see Problem 4"* | 순서 질문 3 |
| 11 그림 `F_p4` | 띠 이름 = *"registered prediction band"* (값 · 빗금 그대로 · 그림만 재생성) | §5 |
| 15 notes · 작은 글 | *"Provisional geometric calibration target; experimental definition and load state still to be matched."* | 순서 질문 4 |
| 6 캡션 | *"Illustration of the 7:3 bed discussed next"* (순서 변경 필수 아님 · 개요 그림이면 허용) | 순서 질문 1 · **승계 장** |
| 4 notes | 감쇠 설명을 11 장 예고로만 짧게 | 순서 질문 2 · **승계 장** |

- **승계 장** = 1 · 2 · 4 · 6 · 8 · 18 (판정문 §7 — 인용 번호 정규화 · 다리 줄 분리 뒤 본문 · notes · 이미지 해시가 v3.1 대응 장과 같다 = v3.1 종결 GO 승계).  이 장을 고치면 승계가 끊겨 종결 확인 범위가 넓어진다.

## 3. 유지 (Codex 수용 · 바꾸지 않는다)

수치 전부 · 11 장 이력 초기화 · 입자 손실 공개 · `F_p4` 값 (압력 · 두께 · 입자 수 = 원로그 · STL) · 9 장 SBE 단일점 보정 한정 (0.545 · 3.41 · R 2.07 · Q 0.84) · 5 장 `planned` · 문헌 한정어 (Faka · Thompson · Hersey · Egermann · Kim) · 16 장 loading 한 줄 · 인용 1–13 · 승계 장 여섯.

## 4. 1저자가 정할 것

| Q | 결정 | 권고 |
|---|---|---|
| Q1 | `SEM32-01` 고치는 법 | **(가) 식은 그대로 · 출처 줄 = Codex 문안 · notes 에 구현 크기 Rᵢ − δᵢⱼ/2** — 원 수식 OMML 을 건드리지 않아 발표 전 표시 위험이 없다.  (나) ② 를 ℓᵢⱼ 로 다시 씀 = 수식 재작성 → PowerPoint 표시를 다시 확인해야 한다 |
| Q2 | §2 권고 반영 범위 | **이번에 바뀌는 장 (3 · 5 · 7 · 11 · 13 · 15) 의 권고는 전부 반영 · 승계 장 4 · 6 은 그대로** (Codex 가 지금 꼴을 허용 · 승계 유지 = 종결 확인이 작다) |

## 5. 순서 (비준 뒤)

1. 시험 먼저 — v3.2 덱에서 실패 확인: 금지 문구 (*implemented equations* · *until the open checks pass* · *Heckel analysis redone* · 옛 Kissel 문장 · 15 장 relaxation 다음 platen removal) · 필수 문구 (§1 · §2 Codex 문안) · 승계 장 1 · 2 · 4 · 6 · 8 · 18 = v3.2 와 본문 · notes · 이미지 같음 · 단어 수 · 렌더 겹침.
2. 생성기 v3.3 (`build_seminar_v33.py` = v3.2 + 위 변경) · `slide_text_v33.md` · `F_p4` 라벨만 재생성 (값 selftest 그대로) · 렌더 겹침 0.
3. 원장 `SEM32-01`~`04` · `SELF-117` → claimed_fixed → Codex 종결 확인 요청서 (ZIP v9 = 수정 PPTX + PDF + 렌더 + **원 수식 PPTX** · 목록 = ZIP 실제 목록) · 발송 = 1저자.
4. 발표 PC 의 PowerPoint 에서 3 장 수식 8 개 표시 확인 (1저자 · 판정문 §7).

- 수정 뒤에도 발표물 수용은 모델 검증 · 런 발사 · 데이터 배포 승인이 아니다 (판정문 §1).
