# Codex 종결 확인 요청 — 연구세미나 덱 v3.1 (2026-10-13)

대상 = v3 재확인 판정 `docs/reviews/codex_review_seminar_deck_v3_recheck_20261013.md` (**조건부 GO** · SEMV3-01~10) 을 고친 판이다.
판정문 §7 이 적은 다섯 확인 — (1) p6/[9] 실제 출처 (2) p11–13 비교군 · 배율 라벨 (3) p11 · 12 · 15 제목과 진단 지위 (4) p13 가정 · 단위 · 군집 해석 (5) 세 반올림과 새 조판 — 을 **수정한 실제 PPT 와 그 PDF** 에서 확인해 주십시오.
새 시뮬레이션 · 값 변경 · 캠페인 재설계는 없다.  바뀐 것은 출처 · 비교군 이름 · 배율 정의 · 결론의 강도 · 반올림 · 조판이다.

## 0. 파일 고정

| 파일 | SHA-256 |
|---|---|
| v3.1 PPTX (17 장) | `73fa2dc3b5629eabb9ec744b47495512db477dd962753a003820ad02b525401b` |
| v3.1 PDF (LibreOffice + Carlito 렌더 · 17 쪽) | `5335e3fe61715eff556258dbb50946174a3d7b043db02a341294bf6107eaf474` |
| 고친 기준 = v3 PPTX (Codex 가 받은 판) | `baf2bb9899c23bbe94d50ee35f9fc5ccedb8f1fe6121afab2baf248fe2148d9c` |

- 생성기 · 그림 스크립트 · 글 전문 = 이 요청서와 같은 커밋의 `docs/seminar_20261013/build_seminar_v3.py` · `docs/seminar_20261013/figs_v3/make_seminar_figs.py` · `docs/seminar_20261013/slide_text_v3.md` (v3.1 글 전문 · 표 · 출처 줄 · notes 포함).
- PowerPoint 앱 렌더는 우리도 하지 않았다.  PDF 는 LibreOffice 에 Calibri 와 폭이 같은 Carlito 를 넣어 만들었다.
- ⚠ **1저자가 p8–p10 (Problem 1·2 · Problem 3 · 194-bed dataset) 을 줄일지 검토 중이다.**  줄이면 같은 생성기로 그 장만 빼서 다시 만들고, 남는 장의 값 · 문장은 바꾸지 않는다.  그때 ZIP v7 의 `MANIFEST` 에 새 PPT · PDF 해시와 장 번호 대응 (v3.1 17 장 → 축소판) 을 적는다.  아래 장 번호는 v3.1 17 장 기준이다.
- ✅ **1저자 결정 10-13: 줄이지 않는다 — 17 장 그대로가 최종판** (*"ppt는 오케이 · 더 수정은 지금 하는거까지만"*).  ZIP v7 (sha256 `1abdd488fbbffadebe50b9a7343899601e81a2e9d7d3b55cd4a0c37d5601ad3a`) 안의 이 요청서 사본은 결정 전 판이다 (윗줄 "검토 중") — 발송 글에 이 결정을 한 줄로 적는다.

## 1. 항목별 수정

| ID | 장 | 화면 | 그림 · CSV · notes | 상주 검사 (v3 → v3.1) |
|---|---|---|---|---|
| SEMV3-01 | p6 · p16 [9] | 출처 줄 · 크레딧 · [9] = **So et al., J. Electrochem. Soc. 168, 030538 (2021), Fig. 4a** · 참고문헌 16 개 유지 (옛 JPS 논문은 다른 장에 인용 없음) | 크롭 오른쪽 경계 0.475 → 0.515 (500 MPa 눈금 · 끝 데이터 포함 · 데이터 무변경) · 덱에 DOI 를 쓰지 않음 | 본문 금지 `j. power sources 508, 230344` (p6 · p16) · 필수 `j. electrochem. soc. 168, 030538` (p6) · `[9] m. so et al., j. electrochem. soc. 168, 030538 (2021)` (p16) |
| SEMV3-02 | p11–13 | 비교군 = `Low NCM–NCM cohesion` · `low-cohesion comparator` · 따로 있는 음성 대조만 `No cohesion (control)` | 그림 범주 · CSV 행 이름 · ΔM 축 = `ΔM = M(low-cohesion comparator) − M(setting)` · notes 에 작은 비영 CED 108,795 · 142,562 J m⁻³ · model Bond number 0.00109 · 0.00553 · NCM–벽 동반 변화 | 본문 금지 `no ncm–ncm cohesion` · `non-cohesive` · `cohesion removed` · notes 금지 `without NCM–NCM cohesion` · `cohesion removed` · `non-cohesive` · 그림 SVG 금지 `removed` · `non-cohesive` · 필수 `low NCM` (F_mix1 · F_mix3) |
| SEMV3-03 | p11 · p15 | 제목 `Layered-bed mixing: unresolved mixing-index contrast` · 본문 2 = Codex 문안 (ΔM 0.0012 · seed SE 0.0073) + `Subsequent diagnostic classification; the original 1% overlap condition was not met.` · p15 Mixing = Codex 문안 | notes = 수치 규칙 → 등록 범주 문장 + `This does not establish compliance with the original registration, equivalence, or a physical absence of segregation` · E0 겹침 4.7–5.8 % · 벽 4.5–5.7 % | 본문 금지 `no segregation detected` (p11 · p15) · `fully mixed` · 필수 `unresolved` · `overlap condition was not met` (p11) · `unresolved diagnostic mixing-index contrast` (p15) · notes 필수 `does not establish compliance` |
| SEMV3-04 | p12 | 제목 `Exploratory cohesion settings produce different mixing indices` · 본문 1 = 두 계열 정의 (큰 NCM 자기쌍 model Bond number 38.4 · 384 · 1152 / all nonzero cohesion-energy densities ×10 · ×14.42, 비교군 기준) · 본문 2 = 계열 안 ΔM 상승 · 수준 사후 선택 · 벽 접착 · 시작 상태 · `no verdict` · 출처 줄 = `low versus higher NCM cohesion, two revolutions` | 그림 = 두 구획 (`NCM-pair model Bond number` 38.4 / 384 / 1152 · `all-pair CED scale` ×10 / ×14.42) · `reference` 라벨 없음 · notes = 큰 NCM CED 3.56348e6 → 7.67728e6 → 1.10725e7 J m⁻³ (×2.154 · ×3.107) · Bo 1152 의 M −0.968 / −1.407 / −2.283 · 같은 개발 seed · 공통 SE 영률 2e8 Pa (원 soft 캠페인과 세대 다름) | 본문 금지 `stronger cohesion lowers` · `non-cohesive` · 12 장 전용 금지 `reference cohesion` · 필수 `bond number` · `cohesion-energy densit` · `no verdict` · 그림 SVG 필수 `38.4` · `1152` · `14.42` · `Bo` · `CED` · 금지 `reference` |
| SEMV3-05 | p13 | 본문 1 · 2 = Codex 문안 (`With equal contact areas and an assumed geometric-mean adhesion rule …` · `Exploratory all-pair CED scaling retains …`) · 출처 줄 = Codex 문안 | 도식 = `Assumed W_AS = 2√(γAγS); equal contact areas` · 식 + `(J m⁻²)` · `Conditional adhesive-work comparison.` · `Contact survival is not determined by particle size alone.` · notes = ΔU = −A·ΔW · JKR pull-off 1.8 / 1.6 · 0.309 / 0.391 = 두 접촉 힘 비교 · `not a necessary or sufficient condition` · CED 런은 SE–SE 도 바꾼다 · `the CED-scaling runs do not validate a surface-energy-based coating mechanism` | 본문 금지 `like–like contacts best` · `like–like contacts are favoured` · `holds on most` · notes 금지 `not SE–SE` · `would have to be below about 0.31` · 필수 `assumed geometric-mean` · `per unit area` · notes 필수 `0.309` · `not a necessary or sufficient condition` · 그림 SVG 필수 `Assumed` · `Conditional` · `J m` · 금지 `favoured` · `holds on most` |
| SEMV3-06 | p12 · p13 | — | 그림 · CSV · notes 값 = 판독 JSON 에서 직접 (`dev_planned_m` · `dev_delta_m` · `dev_cluster`): Bo 384 12×12×3 **0.927** · CED ×14.42 16×16×4 **0.865** · 비교군 군집 **0.400** | 그림 selftest 값 고정 (세 값 + Bo 1152 8×8×2 3.163938904 · CED ×10 하한 0.875368565) · F_mix2.csv = JSON 값 (오차 1e−12) |
| SEMV3-07 | p7 | 해석 줄 `Original Phase A campaign (VGCF E = 10 GPa): means of 96 primary arms, three voxel sizes; no contact resistance` | notes 에 100 GPa 재현 (순서 72/72) 을 따로 연결 · 그림값 무변경 | 필수 `vgcf e = 10 gpa` · notes 필수 `100 gpa` |
| SEMV3-08 | p9 | `The NCM–NCM stress-share ranking matches the experimental porosity summaries for the selected five compositions (exploratory, n = 5).` | 선택된 3-of-n 평균 · 불확도 미확립 = notes 유지 | 필수 `experimental porosity` |
| SEMV3-09 | p6 · p8 · p11 · p12 | — | p6 크롭 경계 · p8 F_limits 패널 제목 (a)(b)(c) · 폭 비 1.0 / 0.95 / 1.25 · 범례 10.5 pt · 간격 · p11 F_mix1 = 12.0 × 6.2 cm · 비교군과 음성 대조 사이 간격 · p12 F_mix2 = 12.0 × 7.0 cm · 두 구획 · p10 (b) 값 라벨 제거 (F_trans) · 그림 크기 = 덱 그림 띠 1:1 | 그림 selftest = 그려진 모든 글 상자 (눈금 · 축 · 제목 · 그림 안 글 · 범례) 쌍 겹침 0 |
| SEMV3-10 | p5 · p6 notes · p11 · p13 notes | p5 `Our fixed-shape implementation has no shape change and no yield cap: …` · p11 해석 줄 `M = 1: random-reference variance` | p6 notes = `σy = 0.30 GPa was selected in the pure-SE calibration sweep (…)` 까지 (`inside the literature range` 삭제) · p13 notes = SEMV3-05 와 같이 교체 | 본문 금지 `fully mixed` · notes 금지 `inside the literature range` |

판정문 §6 의 선택 개선 (P2) 처리:

| 항목 | 처리 |
|---|---|
| p10 범례를 고 τ 점에서 떼기 | 적용 — 범례 대신 직접 라벨 (`130-bed set` · `64-bed set` · `× no spanning path`) |
| p10 Tier 1 → `order-of-magnitude agreement` | 적용 (상태표 · `R = 2.07 (order-of-magnitude agreement); Q = 0.84`) |
| p10 `× : no spanning path (display position only)` | 적용 (해석 줄) |
| p9 색막대 0 / 75 / 150 MPa 바깥 눈금 | 미적용 — 오른쪽 그림은 1저자가 비준한 ps73 최종 판 그대로 · 해석 줄에 `0–150 MPa` |
| p5 압축 구간 감쇠 58 % · p6 현재 실행 상태의 화면 복구 | 미적용 — 판정문대로 필수 아님 (notes 유지) |

그림의 배치 뒤 글씨 (스크립트 pt × 배치 배율 · 배율 = 덱에 놓인 폭 ÷ 그림 원래 폭 · v3.1 PPTX 에서 잼):

| 장 | 그림 | 배율 | 가장 작은 글씨 |
|---|---|---:|---|
| p4 | F_trans | 0.895 | 조성 눈금 8.5 pt · 값 라벨 9.4 pt |
| p8 | F_limits | 0.846 | (c) 조성 눈금 · 범례 8.9 pt · 축 눈금 10.6 pt |
| p10 | F_dataset | 0.974 | `× no spanning path` 9.3 pt · 직접 라벨 10.2 pt |
| p11 | F_mix1 | 1.011 | 범주 10.1 pt (v3 판정 환산 9.3) |
| p12 | F_mix2 | 1.011 | 범례 10.1 · 구획 이름 10.6 · 범주 11.1 pt (v3 8.6) |
| p13 | F_mix3 · 도식 | 1.011 · 0.963 | 범주 10.1 pt (v3 9.2) · 도식 문장 10.1 pt |

- v3 README 의 *"글씨 = 배치 1:1 ≈ 12 pt"* 는 p4 · p8 에서 맞지 않았다 (배율 0.895 · 0.846).  README v3.1 절에서 고쳤다.  p4 · p8 의 글씨 크기는 이번에 바꾸지 않았다.

## 2. 시험 먼저 기록

새 검사를 Codex 가 받은 v3 덱과 v3 커밋 (`0c6f5c84e`) 의 그림 스크립트에 돌려 고치기 전에 실패하는지 먼저 봤다.
하네스 `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_1_fix/testfirst_v31.py` (리포 · 덱은 읽기만) · 기록 같은 폴더 `testfirst_v31.json`.

| 대상 | 검사 | v3 | v3.1 |
|---|---|---:|---:|
| 덱 본문 | 금지 문구 | 10 | 0 |
| 덱 notes | 금지 문구 | 6 | 0 |
| 덱 본문 | 필수 문구 누락 | 11 | 0 |
| 덱 notes | 필수 문구 누락 | 4 | 0 |
| 그림 | 글자 겹침 (쌍) | 7 | 0 |
| 그림 | 믹서 라벨 · 도식 가정 | 13 | 0 |
| 그림 CSV | 판독 JSON 값 (Bo 384 12×12×3) | 0.928 | 0.927 |

- 12 장 전용 금지어 `reference cohesion` 은 v3 에서 본문이 아니라 **그림 라벨** (F_mix2) 에 있었다.  그림 검사가 그것을 잡았고, 본문 검사는 다시 들어오는 것을 막는 용도다 (v3 · v3.1 모두 0).
- v3.1 덱 · 그림의 생성기 selftest 출력:

```
selftest ok — 17 slides · banned 0 · internal 0 · arm codes 0 · flagged phrases 0 · angle captions 0 · overlap 0 · blanks 4 · max words 105 · bullets ≥ 15 pt · note lines ≥ 12 pt · pictures 18
selftest ok — values match canonical sources and the readout JSONs · no banned strings · no arm codes · no overlapping text · labels checked
```

- 제작자 selftest 는 판정 근거가 아니다 (판정문 §2).  위 기록은 "검사가 옛 판에서 실패한다" 는 것만 보인다.

## 3. 바뀌지 않은 것

- 그림 값: F_poro · F_trans · F_limits · F_load · F_vgcf · F_dataset 의 값은 판정문 §5 에서 일치로 확인된 그대로다.  F_trans 는 겹치던 막대 위 값 라벨만 지웠고 CSV 값은 같다.
- 믹서 값: F_mix1 의 열 런 M · SD · 짝차 · seed SE 는 그대로다.  F_mix2 · F_mix3 은 세 반올림 (SEMV3-06) 외에 값이 같다.
- 빈 자리 4 (p5 우 · p7 좌 · p11 우 · p12 우) · 참고문헌 16 개 · 장 수 17 · 표지 날짜.
- 원장: `SEMV3-01`~`10` = open → 이 커밋 뒤 claimed_fixed · 내 오기 `SELF-111` (정본 대조 없이 쓴 출처 · 등록 정정 위반 · 배율 혼동 · 논지와 반대인 문장 · README 문자열만 보던 selftest).

## 4. 확인 질문

| Q | 질문 |
|---|---|
| Q1 | p6 출처 줄 · 크레딧 · [9] (JES 168, 030538 (2021), Fig. 4a) 와 넓힌 크롭으로 SEMV3-01 이 닫히는가.  덱에는 DOI 를 쓰지 않았다 (정본 카드의 머리 DOI 정정은 litdb 에서 원문 확인 뒤 따로 한다). |
| Q2 | p11–13 의 비교군 이름이 본문 · 그림 PNG/SVG · CSV · notes 전부에서 바뀌었는가 (SEMV3-02). |
| Q3 | p11 · p12 · p15 의 제목 · 요약 · 화면 한정이 후속 진단 지위와 맞는가 (SEMV3-03 · 04). |
| Q4 | p13 의 가정 · 단위 · 조건부 해석과 notes 의 0.309 / 0.391 한정이 판정문 §4 와 맞는가 (SEMV3-05). |
| Q5 | 세 반올림과 p6 · p8 · p11 · p12 조판이 실제 PPT · PDF 에서 닫혔는가 (SEMV3-06 · 09).  §1 끝 표의 배치 뒤 글씨 (p4 8.5 pt · p8 8.9 pt 가 가장 작다) 가 발표 전 고칠 문제인지도 봐 주십시오. |
| Q6 | 1저자가 p8–p10 을 빼기만 하면 (남는 장의 문장 · 값 무변경), 해시 · 장 번호 대응표 확인만으로 이 종결 판정을 이어받아도 되는가. |

## 5. 묶음 (ZIP v7 · 발송 = 1저자 · p8–p10 결정 뒤) · ✅ 10-13 결정 = 축소 안 함 (17 장)

- 덱 PPTX + PDF + 렌더 PNG (17 장 또는 축소판) + `MANIFEST` (해시 · 장 번호 대응).
- `docs/seminar_20261013/` (생성기 · 그림 스크립트 · `figs_v3/` 그림 png / svg / csv · `slide_text_v3.md` · `slide_sources_v3.json` · README).
- 문헌 크롭 3 장 (빌드 때 litdb 정본 브랜치에서 받은 Bazzoun 2026 Fig. 2 · Luding 2008 Fig. 1 · So 2021 Fig. 4).
- 이 요청서 + `docs/reviews/codex_seminar_deck_review_evidence_20261013/v3_1_fix/` (시험 먼저 하네스 · 기록).
- 이 판정은 시뮬레이션 발사 · 194 / 보충 20 / v1.3 배포 승인과 무관하다.
