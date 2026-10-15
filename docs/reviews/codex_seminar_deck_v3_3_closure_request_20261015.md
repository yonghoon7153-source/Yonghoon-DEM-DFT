# Codex 종결 확인 요청 — 연구세미나 덱 v3.3 (2026-10-15 · 세미나 10-16)

> 리뷰 핀 = 이 요청서가 든 본 가지 커밋 (메인 세션이 적는다) · 묶음 = ZIP v9 (§6 · 목록은 ZIP 실제 내용에서 생성) · 발송 = 1저자.
> ✅ **발송 10-15 (1저자)** · 리뷰 핀 `aac17e11f` (이 요청서가 든 첫 본 가지 커밋 · ZIP `repo/` 사본 19 = 그 커밋 blob) · ZIP v9 → ✅ **Codex 종결 (10-15) = 내용 GO** · 남은 조건 = 발표 PC 3 장 PowerPoint 표시 (1저자 직접) · 판정문 반입 10-15 = `docs/reviews/codex_review_seminar_v33_closure_20261015.md` (증거 `docs/reviews/codex_seminar_v33_closure_evidence_20261015/` · 판정문 §2 의 PIN.txt 빈칸 = 이 요청서의 리뷰 핀 `aac17e11f` 로 기록).

대상 = v3.2 재확인 판정 `docs/reviews/codex_review_seminar_v32_recheck_20261015.md` (**HOLD** · 소스 핀 `90ca2c8cd` · SEMV32-01–03 P2 · SEMV32-04 P3 · 원장 `SEM32-01`~`04` · 포장 누락 `SELF-117`) 을 고친 판이다.
1저자 10-15 비준 = 수정 계획 `docs/reviews/seminar_deck_v32_fix_plan_20261015.md` **Q1 (가)** (3 장 식 OMML 그대로 · 출처 줄 + notes 로 고침) · **Q2** (바뀌는 장 3 · 5 · 7 · 11 · 13 · 15 의 권고 전부 · 승계 장 4 · 6 은 그대로).
판정문 §8 의 최소 종결 목록을 **수정한 실제 PPTX 와 그 PDF** 에서 확인해 주십시오.  새 시뮬레이션 · 새 계산 · 값 변경 없음 — 바뀐 것은 문구 · 순서 · 그림의 띠 이름뿐이다.

## 0. 파일 고정

| 파일 | SHA-256 |
|---|---|
| v3.3 PPTX (18 장 · ZIP `deck/`) | `e787298ef657d516f43c8255e80cf1a61bbc52ffe94c6fbfbea57faca14dbb8c` |
| v3.3 PDF (LibreOffice + Carlito · 18 쪽 · ZIP `deck/`) | `706d6a1d062936c16aff15af4500cb7cff9ef8e5c19866d4c48ccaaeea64999e` |
| 비교 기준 = Codex 가 받은 v3.2 PPTX (ZIP `v32/`) | `1b6988f3e55dc6bcf7e81d0ba4ec35b11ed2a0790a1357ba6e6185d22b08f28d` |
| 원 수식 덱 = 1저자 10-09 `DEM_Equations_final_20261009_2.pptx` (ZIP `source_eq/eq.pptx` · **SELF-117 보완**) | `8e76819a9f89516d75c7bd40c529cd65ce055e31a2c8b777d1b8e8edfc669223` |
| 양식 = 1저자 10-13 덱 (ZIP 밖 · v3.2 와 같은 파일) | `7746e163ddb399a62c40b1de85e71b0cd8df1aa87917b3621b3c015704387be7` |

- 생성기 · 그림 · 글 전문 = 이 요청서와 같은 커밋의 `docs/seminar_20261013/build_seminar_v33.py` (`build_seminar_v32.build_v32` 를 **그대로** 불러 v3.2 를 만든 뒤 6 장만 고친다 · v3.2 · v3.1 생성기 무변경) · `docs/seminar_20261013/figs_v3/make_seminar_figs_v33.py` · `docs/seminar_20261013/slide_text_v33.md` · `docs/seminar_20261013/slide_sources_v33.json` · README v3.3 절.
- PPTX 는 python-pptx 저장이라 빌드마다 해시가 바뀐다 — 동일성은 내용 대조로 말한다 (§3).  PowerPoint 앱 렌더는 우리도 하지 않았다 (3 장 식 = OMML · PDF 에는 대체 그림).

## 1. 항목별 수정

| ID | 장 | 화면 | notes · 그림 | 상주 검사 (v3.2 덱 실패 → v3.3 덱 통과) |
|---|---|---|---|---|
| SEM32-01 (SEMV32-01) | 3 | 출처 줄 = Codex 문안 + `This work —` 머리 (출처 줄 관례) · 162 자라 **두 줄** (각 ≤ 110 자 · 오른쪽 맞춤 · 제목 위에서 끝남) | notes: "implemented equations" → 대표식 + ② 작은 겹침 근사 + 구형 입자 경로의 구현 지렛대 크기 Rᵢ − δᵢⱼ/2 (`cri = radi − 0.5·deltan` · LIGGGHTS-PUBLIC 3d5c00f `surface_model_default.h` 173–188 · `tangential_model_history.h` 254–261 · `docs/dem_governing_equations_background_20261011.md` §3.1) + ④ CDT = 상대 각속도 0 에서 토크 0 (`rolling_model_cdt.h` 94 · 138 · torsion torque off) · **식 OMML 여덟 · 대체 그림 · 그림 = 바이트 그대로** (Q1 (가) · 표시 위험 없음) | 금지 `implemented equations` (장 글 · notes) · 필수 출처 줄 = 문안 · notes 필수 8 낱말 묶음 · A8 (원 수식 덱 대비 식 C14N 8 · 대체 그림 8 · 그림 2) · B3 식 = v3.2 |
| SEM32-02 (SEMV32-02) | 11 | 본문 2 = Codex 문안 (빨강 = `combined follow-up protocol` · `model-internal diagnostic`) · 표 (이력 초기화 · 13 SE 소실 행) 그대로 · 해석 줄 (b) `shaded = registered prediction band` | notes: 띠 = 결과 전 모델 예측 (실험 범위 · 통계 신뢰구간 아님) · `Passing these internal checks would qualify the numerical state of this bed; it would not validate the model against experiment.` · (ii) 복합 개입 · (iii) 13 SE 소실 문장 그대로 · 그림 F_p4_v33 (§2) | 금지 `until the open checks pass` · 필수 본문 2 (그대로) · 표 두 행 · notes 필수 8 |
| SEM32-03 (SEMV32-03) | 15 | 흐름도 = insertion → stabilization → compression → servo → relaxation → **unloading → platen removal** (상자 6 · 7 의 글만 바꿈 · 둘 다 남색 굵게) · 작은 글 `Heckel analysis to be redone` | notes: 같은 순서 + 근거 (`docs/reviews/dem_protocol_gen2_plan_draft_20261014.md` Q1 · `docs/session_20260923_progress.md` 10-14 밤 7) · `Heckel analysis to be redone` | 금지 relaxation 바로 뒤 platen removal (상자 · notes) · `Heckel analysis redone` (to be 없이) · 필수 상자 순서 · 상자 서식 |
| SEM32-04 (SEMV32-04) | 13 | — | Kissel 2026 문장 = Codex 문안 (그대로) | 금지 옛 문장 · 필수 새 문장 |
| SELF-117 | — | — | ZIP v9 에 원 수식 덱 · §6 목록과 `MANIFEST.sha256` = ZIP 실제 목록에서 생성 (`docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/package_v9.py` · 묶은 뒤 다시 열어 대조) | §6 |

권고 (판정문 §4 · §5 · §6) 처리 — 수정 계획 Q2:

| 권고 | 처리 |
|---|---|
| 3 장 notes · ④ CDT 0 토크 (Q3 답) | 적용 (위 표) |
| 5 장 notes · 대립 SE "답 대기" 갱신 (Q5 답) | 적용 — `one large-particle LPSCl pellet added to the EIS plan, approved by the author on 10-14` (진행 기록 10-14 밤 9) · 화면 표 그대로 |
| 7 장 첫 300 MPa (순서 질문 3) | 적용 — `pressed to 300 MPa (nominal stopping pressure; see Problem 4)` (줄 수 · 그림 자리 그대로) |
| 11 장 F_p4 띠 이름 (§5) | 적용 — 그림 · 해석 줄 (b) · notes |
| 15 장 provisional 문구 (순서 질문 4) | **notes 에만** — `Provisional geometric calibration target; experimental definition and load state still to be matched.` (+ 5 장 10 % 보정 표적과 다른 목표라는 한 문장) · 작은 글에 넣으면 단어 121 → 134 (한도 120) |
| 6 장 캡션 · 4 장 notes 감쇠 (순서 질문 1 · 2) | 미적용 — 승계 장 (Q2) |

화면 글 old → new (영어 전문 · 나머지 화면 글은 한 글자도 그대로 = 검사 B4):

| 장 | v3.2 | v3.3 |
|---|---|---|
| 3 출처 줄 | This work — implemented equations of LIGGGHTS-PUBLIC 3.8.0 [2]; linear hysteretic law [1] | This work — representative equations based on LIGGGHTS-PUBLIC 3.8.0 [2]; linear hysteretic law [1]. ／ Equation ② uses the small-overlap approximation ℓᵢⱼ ≈ Rᵢnᵢⱼ. |
| 7 본문 1 | … linear hysteretic contact law, pressed to 300 MPa; one bed per composition, no seed replicates. | … linear hysteretic contact law, pressed to 300 MPa (nominal stopping pressure; see Problem 4); one bed per composition, no seed replicates. |
| 11 본문 2 | At fixed platen the same bed relaxes to 165 MPa; a servo branch holding the target force (damping 1e-5) instead compacts it further (111.05 → 105.84 µm) — model-internal until the open checks pass. | At fixed platen, the original run relaxes to 165 MPa. A combined follow-up protocol—plate-contact history reset, lower damping and force hold—reduces thickness from 111.05 to 105.84 µm. This remains a model-internal diagnostic; static-equilibrium and conservation checks are pending. (105.84 와 µm 사이 = 줄바꿈 금지 공백) |
| 11 해석 줄 (b) | … shaded = band registered before the run; … | … shaded = registered prediction band; … |
| 15 상자 6 · 7 | platen removal · unloading | unloading · platen removal |
| 15 작은 글 | … (ε_sphere kept internally) · Heckel analysis redone | … (ε_sphere kept internally) · Heckel analysis to be redone |

## 2. 그림 F_p4 → F_p4_v33 (11 장)

- 그리는 코드 = `make_seminar_figs_v32.fig_p4` 그대로 (같은 기록 문자열 · 막대 · 값 라벨 · 빗금).  저장 직전에만: (b) 에 회색 이름표 `registered prediction band` (세 줄) + 띠 오른쪽 위 모서리로 가는 지시선 · (b) y 상한 18 → 20 (이름표 자리 · 값 무관) · CSV state 이름 셋 (`registered band low / high`, `registered point` → `registered prediction …`).
- 그림 검사 (`make_seminar_figs_v33.py --selftest`): v3.2 와 같은 값 대조 (README §1 · §4 · §12-4 · DEMP-01) + F_p4_v33 ↔ F_p4 = CSV 값 · 단위 · 출처 열 같음 · 빗금 `<pattern>` 본문 · 쓰인 횟수 같음 · 값 라벨 8 · `static` 없음 · 글자 겹침 0.  그림 크기 (1622 × 805 px) 와 덱 안 크기 그대로.

## 3. 바뀌지 않은 장 · 동일성

- **12 장 (1 · 2 · 4 · 6 · 8 · 9 · 10 · 12 · 14 · 16 · 17 · 18) = v3.2 와 글 run · notes · 그림 바이트 · 식 같음** — 생성기 검사 B3 (48 건) + 독립 대조 `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/cmp_codex_v32.py` (Codex v3.2 증거 `docs/reviews/codex_seminar_v32_recheck_evidence_20261015/evidence/pptx.json` 의 `extract()` 읽기 규칙을 다시 구현 · Codex 스크립트는 실행하지 않음 · 기록 `cmp_codex_v32.json`):
  ① 제출 v3.2 덱 = Codex 읽기 18 / 18 (대조기가 Codex 읽기를 재현한다) ② v3.3 빌드 안에서 다시 만든 v3.2 = 18 / 18 ③ v3.3 의 12 장 = Codex v3.2 ④ 바뀐 6 장 = 예상한 칸만 다름 (3 글 · notes / 5 notes / 7 글 / 11 글 · notes · 그림 / 13 notes / 15 글 · notes) — 3 장 식 · 그림 같음.
- 렌더: v3.3 PNG 18 장 중 14 장 (12 장 + notes 만 바뀐 5 · 13) 이 ZIP v8 의 v3.2 PNG 와 **파일 바이트까지 같다** (§6 목록의 sha256 = ZIP v8 `MANIFEST` 의 값) · 3 · 7 · 11 · 15 는 고친 자리만 다르다 (3 = 출처 줄 띠 · 7 = 본문 1 · 11 = 본문 2 아래 전체 · 15 = 흐름도 · 작은 글).
- 승계 장 1 · 2 · 4 · 6 · 8 · 18 (판정문 §7 = v3.1 대응 장과 같음) 은 v3.2 와 같으므로 그 승계도 그대로다 (v3.2 검사 A5 = v3.1 대비 같음 · 통과).

## 4. 검사 기록 (시험 먼저)

| 대상 | 검사 수 | 실패 |
|---|---:|---:|
| v3.2 덱 — 구현 **전** 에 쓴 v3.3 검사 (`testfirst_v33.json`) | 349 | 33 (A9 1 · A10 1 · B1 7 · B2 13 · B3 1 · B4 9 · B6 1) |
| v3.2 F_p4 그림 — 구현 전 그림 검사 (같은 기록) | — | 6 |
| v3.2 PDF — 렌더 검사 (`testfirst_render_on_v32.json`) | 10 | 6 (순서 1 · 문구 5) |
| v3.2 덱 — 최종 검사기 (`finalchecks_on_v32.json`) | 350 | 32 |
| **v3.3 덱 — 최종 검사기 (`checks_v33.json`)** | **350** | **0** |
| **v3.3 PDF — 렌더 검사 (`render_check_v33.json`)** | **10** | **0** |

- 기록 폴더 = `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/`.  v3.2 검사 245 는 그대로 돌고, 옛 파일 · 옛 문구를 강제하던 셋만 바꿨다 (이유를 검사 이름에 적음): A9 그림 파일 F_p4 → F_p4_v33 · A10 출처 줄 = 줄마다 ≤ 110 자 · 3 장만 두 줄 · A10 단어 한도 = 7 · 11 · 15 장은 Codex 필수 문안이 늘린 만큼만 초과 허용 (**7 = 104 / 100 · 11 = 121 / 120 · 15 = 121 / 120** — 닫힌 문장을 줄여 맞추지 않았다).
- 새 검사 B0–B6 = 105 건: 금지 · 필수 문구 · 12 장 동일성 · 바뀐 장 = v3.2 + 등록한 고침만 (`SHAPE_EDITS` · `NOTE_EDITS`) · 3 장 출처 줄 자리 · 11 장 그림 · 표 자리 · F_p4_v33.
- 렌더 검사 (`render_check_v33.py` · pdftotext 낱말 상자): 18 쪽 · 글끼리 겹침 > 2 pt 0 · 쪽 밖 0 · 3 장 출처 줄 끝 < 제목 윗선 · 15 장 상자 순서 · 새 문구 렌더 · 옛 문구 없음.  2 pt 이하 접촉 (줄 상자끼리 0.0–0.7 pt) 은 따로 적었다 — v3.2 에도 있던 3 장 "m_i g" 아래첨자 ↔ 캡션 줄 0.7 pt 포함 (복사한 힘 그림 · 무변경).
- 시험 먼저 커밋 뒤 고친 검사 둘: 빗금 대조 = `<pattern>` id 가 아니라 본문 (matplotlib 는 그릴 때마다 id 에 무작위 salt) · 11 장 본문 2 = 줄바꿈 금지 공백 하나 허용 (공백으로 바꾸면 Codex 문안과 같음).
- 제작자 검사는 판정 근거가 아니다 (v3.1 · v3.2 판정 §2).  위 기록은 "검사가 옛 판에서 실패하고 새 판에서 통과한다" 는 것만 보인다.

## 5. 확인 질문 · 남은 것

| Q | 질문 |
|---|---|
| Q1 | 3 장 출처 줄 (두 줄) + notes 로 SEM32-01 이 닫히는가.  식은 그대로다 (Q1 (가)). |
| Q2 | 11 장 본문 2 · notes 로 SEM32-02 가 닫히는가 (복합 개입을 본문에 직접 · 내부 검사 ≠ 실험 검증 · 표 · 13 SE 소실 공개 유지). |
| Q3 | 15 장 상자 · notes 순서로 SEM32-03 이 닫히는가 · "to be redone". |
| Q4 | 13 장 Kissel 문장으로 SEM32-04 가 닫히는가. |
| Q5 | F_p4_v33 (값 · 빗금 그대로 · 띠 이름 · (b) y 상한 20) 이 결과를 과장하지 않는가. |
| Q6 | 단어 한도 초과 (7 · 11 · 15 장 · 위 수) 를 발표물로 받아들일 수 있는가. |
| Q7 | ZIP v9 의 원 수식 덱으로 A8 (원본 대비 식 XML 8 · 대체 그림 8 · 그림 2 같음) 이 재현되는가 · §6 목록 = ZIP 내용 (SELF-117). |

- **남은 것** = 발표 PC 의 PowerPoint 에서 3 장 표시 확인 (1저자 · 판정문 §7 · §8) — 식 OMML 여덟 + 출처 줄 둘째 줄의 ℓᵢⱼ · Rᵢnᵢⱼ (유니코드 아래첨자 · Carlito 에 `ⱼ` 가 없어 LibreOffice PDF 는 대체 글꼴로 그렸다 · Calibri 에서도 대체될 수 있다).
- 원장 `SEM32-01`~`04` · `SELF-117` → claimed_fixed = 메인 세션 (이 커밋에서 원장은 고치지 않았다).
- 이 판정은 시뮬레이션 발사 · 194 / 보충 20 / v1.3 배포 · 모델 검증 승인과 무관하다 (발표물 한정 · 판정문 §1).

## 6. 묶음 (ZIP v9 · 목록 = 실제 ZIP 내용)

- ZIP = `codex_seminar_deck_v3_3_closure_20261015.zip` (리포 밖) · 안의 폴더 하나 `codex_seminar_deck_v3_3_closure_20261015/` · `repo/` = 이 판에서 바뀐 리포 파일 사본 (바뀌지 않은 v3.2 · v3.1 생성기 · 그림 스크립트는 핀의 리포에 있다) · `MANIFEST.sha256` = 자기 자신을 뺀 전 항목.
- 아래 목록은 `package_v9.py` 가 묶을 파일에서 만들어 넣고, 묶은 뒤 ZIP 을 다시 열어 같은지 확인한다 (경로 · 바이트 · sha256).

<!-- ZIP-LIST:BEGIN -->
```
sha256                                                            bytes  path (ZIP 안 · codex_seminar_deck_v3_3_closure_20261015/ 아래)
5986899767e57a982b2841227e5aceeeffc9b27c8960217fbd74e0e6dbc30449         403  PIN.txt
706d6a1d062936c16aff15af4500cb7cff9ef8e5c19866d4c48ccaaeea64999e     2886567  deck/seminar_20261013_v33.pdf
e787298ef657d516f43c8255e80cf1a61bbc52ffe94c6fbfbea57faca14dbb8c     9094504  deck/seminar_20261013_v33.pptx
14787d043cc45da35d9048288058d4e9ba2240f711e8169bf35ed410aee74bca      824623  png/slide-01.png
4e3fe37b418189f5a0cea0be2a71ad52180d43322ef37062003fc31620fd625c      159039  png/slide-02.png
5b972aaf87ace5a07b18d79a970826d1e4569ccbad5b83e89fe1b2c990e8b2ef      359938  png/slide-03.png
ff6004048a9b4719ffbf7bf3eb608522955aaf974cd11c0621a3f688a6c14ee2      211405  png/slide-04.png
461cb8011c503f8009c358832c9ffe52a6a0718a40389f22b5838af34a3480e8      278481  png/slide-05.png
981b1e8efb80e581b7b0da7df86f8ff5be3506f392dcc70ff0892dac208ec9db      233623  png/slide-06.png
b74b00a4d8f55515a08e70eda2f9feb4c1ac420e3c54c26c2a3808ab2e9bc9e6      715208  png/slide-07.png
006ac93458d28041ce216aa001c891f8406bbbbad0457f8baa020eeed463eaa8      319293  png/slide-08.png
f23ab92529d56a1eb282b362e4ba89febc72ac1d0d9f68fcad8c2746e5c98fbe      321066  png/slide-09.png
3d3db11e7a1681b9e515032818d7732c090c3a71718e7b9da504ef0443516799      604266  png/slide-10.png
27bd7e2a26a7f5fcc96f5e649f5525de9a63c573d1854f3cfc3cbf64c6c7cae2      350050  png/slide-11.png
956b70e1bee797d2560a3a6bfa9b2b09bda2ff6c0ef478babe559b509e323797      182655  png/slide-12.png
48e8ac8ded0458f8373e316cf7d7881fde86d34f0c07e907a5df6935778ad803      185054  png/slide-13.png
90d7dd468f1ef8c6664369bc348be43af87c0d1b10f75c1e4dc6f09356a0f2e5      317338  png/slide-14.png
b50aaf7cb88780a6a6c9d34c08805f73346c4b2377fc2fc96ad88449ebc334ba      209021  png/slide-15.png
1b0571ad3cc39f90f1b7074c03a98904a2ca66ac99ee990e918f5df7dd135881      146812  png/slide-16.png
5dcf7ff87ca991a38e28796a0d3c9ab31d65451e735361b9c5fdea50d4880e29      185072  png/slide-17.png
ca03421b135a9fe7e4c729c1b281524fcc2299016609a590cd199cbdc9ac7556     1322417  png/slide-18.png
54718d5b229224c2ffa25542baf5cdc08fbd192a1f6ccb3f69e633dd7fa51e22          87  repo/docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/checks_v33.json
22efb6d52b3947507532bb52838c3c47afb1499a41aca7e2cebeeaf375e65891        6393  repo/docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/cmp_codex_v32.json
94275c74ef630f3819db3461c8b96a5941230051aa8c1c1a8458b63773d8646e        5605  repo/docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/cmp_codex_v32.py
423ff13ce4bfb3f73a0392534504a1e09fb02e2a45ef2f3b8a0ce4d4bda32a6e        6097  repo/docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/finalchecks_on_v32.json
d1b317d4e7027f0783878f89f507624e95836d1b26b285960c789ab5353e255d        7238  repo/docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/package_v9.py
e58d9f9e5fc264df77d73e849c4a86d340abcf657a5897ebc7e40d7228fca96a       11485  repo/docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/render_check_v33.json
234213b446f527286e08b692d25b59bfd05d6fe45a5f13b93629d1b590a74f92        5326  repo/docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/render_check_v33.py
369a91d5418db60171c716dd2df05dd4edaf3a4724db57f83a6e512b5a7a5a6a       10521  repo/docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/testfirst_render_on_v32.json
2486c81c2d4db7203d8cd06095d36dcec420c156c6f0ad366bd18112434bec69        7629  repo/docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/testfirst_v33.json
d75fa50f44dcbd9bd7e7e78f2b1aeeb4e27b394db2ec01976a6204be3f83b348        2651  repo/docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_3_fix/testfirst_v33.py
83556aeaa23f53d97d85d03c0643d7f2f91a4f7e3321172a0260401e01fe7722       30541  repo/docs/seminar_20261013/README.md
425bbc53dfe56d3a142f0268e3efd35e555eebfb070188f47eb8be72e5e7ebcc       38061  repo/docs/seminar_20261013/build_seminar_v33.py
b3e5b1a5ccdb632c3ec351c9504c5981481ff709d67198ad7647c84513c0bad3         721  repo/docs/seminar_20261013/figs_v3/F_p4_v33.csv
0c95a945734ad3893ecf04d91ed384134d1cbfde083931d623940c1752c36863      128070  repo/docs/seminar_20261013/figs_v3/F_p4_v33.png
e2cbaad07a9eccb5446f4c4147885c2dcc24c0b9baf409b68e3dc0cdf89a76eb       15649  repo/docs/seminar_20261013/figs_v3/F_p4_v33.svg
f380b6f438b94bba04fd57052140ebbaa2de75e82e9fa95840a868805580717c        6490  repo/docs/seminar_20261013/figs_v3/make_seminar_figs_v33.py
f96ba6bec1eb6bf976274e150f88e8c9f4d1a28f192ee258d2385ff788942f63        7802  repo/docs/seminar_20261013/slide_sources_v33.json
a7294c7d3d38c02f67aab560e4a0fe4661a9f892b078e1c4f387ad0b98d9131e       49239  repo/docs/seminar_20261013/slide_text_v33.md
8e76819a9f89516d75c7bd40c529cd65ce055e31a2c8b777d1b8e8edfc669223     4683702  source_eq/eq.pptx
1b6988f3e55dc6bcf7e81d0ba4ec35b11ed2a0790a1357ba6e6185d22b08f28d     9077509  v32/seminar_20261013_v32.pptx
(this file — hash in MANIFEST.sha256)                                         codex_seminar_deck_v3_3_closure_request_20261015.md
(hash list of every other member)                                             MANIFEST.sha256
```
<!-- ZIP-LIST:END -->
