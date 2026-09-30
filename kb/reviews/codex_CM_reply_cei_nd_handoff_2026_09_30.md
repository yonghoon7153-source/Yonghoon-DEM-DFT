---
title: "회신 CM — CEI (Nd 계면) 외부 인계본 리뷰: NO-GO (P0 7 · P1 6) — 수치·무결성은 대체로 맞음 · 요약·교육 문구가 계산 범위를 넘음 · Fig. 2 재현 명령이 이력 파일을 덮음"
date: 2026-09-30
updated: 2026-09-30
tags: [review, codex, cei, nd, handoff, onboarding, reply, no-go]
letter: CM
track: cei
kind: review-reply
status: 수령 (2026-09-30 · 사용자 붙여넣기) — 회신 원문 · 고치지 않는다 · 이행은 별도 커밋 · ⛔ 트랙 = CEI (1저자 = 실험 쪽 다른 사람 · 계산 담당 = 사용자)
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-30
verifiedBy: self
explored: false
authoredBy: external
effort: high
claimType: mixed
evidenceScope: single-source
prompt: kb/reviews/codex_CM_prompt_cei_nd_handoff_2026_09_30.md
verdict: NO-GO
---

# 회신 CM — 원문

> ⛔ **이 아래는 Codex 회신 원문이다. 고치지 않는다.** 정정·해석·이행은 별도 파일·커밋으로 남긴다.
> 대상: 커밋 `fbfb63946757ddcaa6e09bf2c2ea770b487197bc` · `cei_handoff_2026_09_30.zip` (SHA256 `1e07d6ea…0126`).
> 링크의 `C:/Users/Administrator/…` 경로는 리뷰어 기계의 파일이다 — 이 저장소에는 없다 (원문 보존).
> 이행 기록: `kb/open_items.md` 의 CEI CM 절 · 이행 커밋 메시지.

## A. 채팅 요약 (붙여넣기 앞부분)

NO-GO — 수치 대조는 대체로 맞지만, 외부 인계 전에 고쳐야 할 P0가 7묶음 있습니다.
[전체 회신 CM — 정확한 인용·파일:줄·근거·교체 문장](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/REVIEW_CM.md)
P0 — 필수 수정

1. ‘산물 재분배’를 ‘양극 계면 열화 억제’로 확대합니다.
계산은 TM-인산염 분율 변화를 보여줍니다. 실제 열화·누설·저항 개선까지 입증하지는 않았습니다. 제목과 AI 예시 답도 그 수준으로 낮춰야 합니다.
2. NdP₅O₁₄의 ‘참조 불일치 확인’과 ‘원인 확정·동일 구조 재현’을 혼동합니다.
ID 해독은 맞습니다. 하지만 기본 StructureMatcher는 부피를 맞춘 구조 유사성 검사이므로, +0.003 eV 일치만으로 동일 조건 재현이나 원인 분해가 끝나지는 않습니다. P₂O₅ 사례로 NdP₅O₁₄의 부피 영향을 반증했다는 문장도 과합니다. [공식 설명](https://pymatgen.org/pymatgen.core.html#pymatgen.core.structure_matcher.StructureMatcher)
3. Nd₂S₃를 산화 산물로 잘못 읽습니다.
원자료에서 Nd₂S₃는 중성 분해 조합, 산화 개시 산물은 Nd₁₀S₁₉입니다. 또한 갭 0.76 eV만으로 “전자가 샌다·부동태가 아니다”를 확정할 수 없습니다.
4. 충전 시 Li 이동 방향과 계산 제어변수를 잘못 가르칩니다.
“Li가 양극으로 빠져나간다”는 설명을 고쳐야 합니다. 이 계산은 제거할 Li 개수가 아니라 Li 화학퍼텐셜을 고정합니다.
5. ‘구분폭 안이므로 크기는 말하지 않고 부호만 확정’은 안전장치가 아닙니다.
계산값의 부호는 보고할 수 있지만, 그것을 물리적으로 해소된 “더/덜 반응한다”는 결론으로 바꾸면 안 됩니다.
6. 한 조건의 ‘P 10:90 배분’을 전 조건에 일반화합니다.
LiCoO₂ 4.3 V 사례는 맞지만, 2.5 V에서는 남은 P가 Li 인산염으로 갑니다. AI 프롬프트의 “나머지 9할은 TM 인산염”은 조건 없이 쓰면 틀립니다.
7. Fig. 2 재현 명령이 이력 파일을 덮어씁니다 — 실행 재현했습니다.
x=0.02 자료를 넣어도 일반 이름의 `cei_p_host_ladder.png`와 CSV를 덮습니다. 현재 화면의 `_x002` 그림은 갱신하지 않습니다. 별도 출력 폴더를 지정해야 합니다.

검증 결과

* 해시 127건 일치, 저장소 유래 126파일이 지정 커밋과 동일
* 결속 시험 95개 PASS, 보호율 생성기 selftest PASS
* 120행·탈락 19·통과 101·전 농도 통과 17열, 판별종 82/14/1 재현
* 그림 9장 확인, 이미지 경로 누락 없음
* 결정 표 14항목의 상태 일치

P1 6건—94%의 합산 범위, 공통 상의 판별력, 보정 상쇄, 갭 ‘하한’, 문서 간 우선순위, 목표 셀 원자 수—도 전체 회신에 교체 문장까지 적었습니다. 송부판에서 빠진 **‘생성기 HTML 조각은 정본을 대체하지 않는다’**는 안내와 이메일 4건의 처리 방법도 별도 정리했습니다.
추가 DFT 없이 문구·조건 표시·출력 경로를 고쳐 닫을 수 있습니다. 원본 파일은 수정하지 않았습니다.

## B. 전체 회신 (REVIEW_CM.md)

# 회신 CM — CEI 외부 인계본 리뷰

NO-GO — 숫자의 전사·파일 무결성은 대체로 맞지만, 요약과 교육 문구가 계산이 뒷받침하는 범위를 넘고, 제공한 재현 명령 하나가 이력 파일을 덮어쓴다.

대상: 커밋 `fbfb63946757ddcaa6e09bf2c2ea770b487197bc` 및 `cei_handoff_2026_09_30.zip`.
이 판정은 **현재 묶음을 그대로 외부 1저자·초심자에게 넘기는 것**에 대한 것이다. 계산 결과 전체의 폐기나 추가 DFT 실행을 요구하지 않는다. 아래 수정은 대부분 문구·인계 규칙·출력 경로 정정으로 끝낼 수 있다.

## 1. 먼저 확인된 것

- ZIP SHA256: `1e07d6ea1c20d5d73405e116b47b0f263040233270fc1b59caf1ccd72e580126`.
- 첨부 해시 목록 127건 모두 일치. 그중 저장소 유래 126파일을 지정 커밋과 대조해 바이트 불일치 0건.
- 정본과 송부판을 텍스트·로컬 참조로 대조했고, 송부판 PNG 9장을 직접 확인했다. 이미지 경로 누락 0건. 브라우저 인쇄/PDF 렌더까지 검증한 것은 아니다.
- 해당 커밋의 `webapp/tests/test_interpretation_cards.py`: **95 passed**. 마지막 재실행 5.43초.
- 보호율 생성기 `--selftest`: **PASS**. 두 그림 재현 명령도 실행했으나, 두 번째는 정상 종료하면서 잘못된 출력 파일명을 사용한다(P0-7).
- 결정 표 14항목의 상태는 원장과 일치한다. 구형 항목의 `decision_state`와 신형 `status`를 구별해 대조했다. NdP₅O₁₄ 개정은 실제로 proposed다.
- DFT·UMA·MD, 비밀키를 이용한 MP 재조회, 외부 발송은 하지 않았다. 재현 명령은 별도 복사본에서 실행했고 첨부·저장소 원본은 수정하지 않았다.

### 독립 재계산

- 판별종: 양쪽 공통 **82**, Nd 계만 **14**, 무Nd 계만 **1**. Nd 계만 나오는 TM 함유 종 **5**.
- 보호율 CSV: **120행 / 탈락 19 / 통과 101**, **24열 중 전 농도 통과 17열**.
- 식 비교 가능한 11열: 최대오차가 **≤3.1 %p 3열 / 약 8.8 %p 2열 / 14.6 %p 1열 / 25–82 %p 5열**. NMC811 4.0 V의 식 기준 오차는 **14.6278 %p**다. 현재 화면은 이를 CSV의 `P_taken_by_Nd` 기준과 구별해 제대로 적었다.
- 비단조 3열: LiMnO₂ 3.0 V, NMC811 4.0·4.3 V.
- x=0.02의 유효 보호율 16칸: **−2.9656~12.279%**. 10.3%를 LiCoO₂ 4.3 V 사례로 쓰는 것은 맞다.
- 황화물 항목: 72칸의 정규화된 TM 분율 차를 합산해 **93.8693% ≈ 94%**를 재현했다. 다만 그 합산 범위를 요약에서도 유지해야 한다(P1-1).
- 갭: **2.264~5.993 eV**, NdP₅O₁₄ 제외 9종 offset 평균 **+0.053222 eV**, 중앙값 **+0.037 eV**, 최대 절대차 **0.120 eV**.
- ESW 원자료: 무Nd 계 산화 개시 **2.14 V**, Nd 계 **1.92 V**, Li 교환이 없는 중성 구간의 하단 **1.717 V**. 잘못된 구형 `reduction_limit_V`를 재인용하지 않았다.
- PDOS 원자료·구조 SUMMARY의 `n5fu / Cl8Li31Nd2O3P3S19 / 66 atoms` 이름표는 수정된 화면과 일치한다.

이 통과는 **원장과 화면의 결속**이다. 시험 파일 자체도 과학적 해석의 타당성을 판정하지 않는다고 명시한다. 새 인계 문서와 송부판 전체의 의미론까지 95개 시험으로 승인되는 것은 아니다.

## 2. P0 — 보내기 전 반드시

### P0-1. 산물 재분배를 실제 ‘양극 계면 열화 억제’로 승격한다

**위치·정확한 인용**

- [03_송부판_페이지.html:179](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:179>): `고전압 양극 계면 열화 억제`
- [02_AI_프롬프트.md:71](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/02_AI_프롬프트.md:71>): `"양극 계면 열화 억제" 로 써요.`
- [kb/syntheses/cei_nd_manuscript_framing_2026_09_18.md:91](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/kb/syntheses/cei_nd_manuscript_framing_2026_09_18.md:91>): `"안정성" 이 전압창을 뜻하면 반증됐고, 양극 열화 억제를 뜻하면 우리 데이터가 받친다.`

**근거·실패 상황**

직접 확인된 것은 0 K hull에서의 산물 조합과 TM-인산염 분율 변화다. 인산염을 면한 금속도 대부분 황화물로 옮겨가며, CEI 전체의 누설·저항·두께·기계적 손상·실제 양극 소모 감소는 이 계산에서 판정하지 않았다. 따라서 ‘분해가 일어난 뒤 생기는 것이 달라진다’와 ‘그 결과 열화가 억제된다’ 사이에 빠진 논증이 있다.

초심자가 제목과 예시 답만 복사하면, 본문의 ‘부동태 증명 아님’이라는 단서를 붙여도 이미 긍정적인 성능 결론을 전달한다. ‘속도는 모른다’만 덧붙여도 이 문제는 해소되지 않는다.

**바꿀 문장**

> Nd 치환에 따른 고전압 계면 분해 산물의 재분배 — 일부 조건에서 양극 금속의 인산염 분율이 줄지만, 실제 양극 열화나 CEI 전도 특성의 개선은 이 계산으로 확정하지 않는다.

원고 동기로 남기고 싶다면 ‘열화 억제의 가능성을 검토하기 위해 산물 재분배를 계산했다’까지다. 새 실험·계산 없이도 주장 수준을 이렇게 낮춰 송부할 수 있다.

### P0-2. NdP₅O₁₄의 참조 불일치 확인을 ‘동일 구조 재현·원인 확정’으로 확대한다

**위치·정확한 인용**

- [00_START_HERE.md:64](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/00_START_HERE.md:64>): `NdP₅O₁₄ 갭 ‘미재현’ — 원인 확인됨, 인용 조건 개정만 비준 대기`
- [03_송부판_페이지.html:1679](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:1679>): `모두 같은 구조`
- [03_송부판_페이지.html:1680](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:1680>): `우리 계산이 틀린 것이 아니라` / `참조의 계산 종류가 달랐다`
- [03_송부판_페이지.html:1673](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:1673>): `부피 가설은 반증됐다.`
- [03_송부판_페이지.html:1626](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:1626>): `MP 값도 PBE 계산이므로`
- [db/properties/cei_gap_ndp5o14_reference_check_2026_09_30.json](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/db/properties/cei_gap_ndp5o14_reference_check_2026_09_30.json>): `P2_1/c 와 Pmna 는 사실상 같은 골격의 대칭 표기 차이다.`

**맞는 부분**

새 MP ID의 base-26 해독은 맞다. aaabfxkr→560681, aaacqxxk→1211324 및 task ID 3개를 직접 검산했고, a=0·8자리 패딩·구/신 ID 변환은 [MP 공식 규약](https://github.com/materialsproject/public-docs/blob/main/data-production/identifiers.md)과 일치한다. 숫자 해독은 ID 대응을 보장하며, **그 task가 특정 summary 값의 출처라는 연결은 별도의 origins 자료**가 담당한다.

첨부 조회 기록은 6.3358의 출처를 r2SCAN Structure Optimization, 5.3904를 다른 엔트리의 GGA NSCF Line으로 연결한다. 따라서 기존 비교가 동일 계산 조건이 아니었다는 지적은 타당하다. 다만 API 원응답·구조 파일을 다시 받아 matcher를 재실행한 것은 아니므로, 조회 결과의 진위는 첨부 기록의 증거 수준이다.

**왜 결론은 과한가**

1. 기본 StructureMatcher는 `scale=True`로 부피를 맞추고 허용오차 안에서 구조 유사성을 판정한다. 일치=True는 동일한 셀·좌표·전자구조·갭 계산을 보증하지 않는다. [공식 API](https://pymatgen.org/pymatgen.core.html#pymatgen.core.structure_matcher.StructureMatcher)
2. 다른 구조·다른 task 종류·다른 계산 설정이 섞인 두 결과의 차가 +0.0026 eV라는 사실만으로, 기존 −0.943 eV 차의 원인이 **전부** XC 선택이라고 분해할 수 없다.
3. P₂O₅의 팽창에서 갭 차가 작았다는 관찰은 NdP₅O₁₄의 부피 민감도를 반증하지 않는다. 서로 다른 물질의 갭-변형 민감도가 같다는 전제가 없다.
4. 같은 조회 기록 §4는 ‘다른 9종의 MP 참조가 전부 GGA인지는 확인하지 않았다’고 적는다. 그런데 화면은 전체 MP 값이 PBE라고 가르친다.
5. proposed 비준은 인용 정책을 바꿀 수 있지만, 위의 구조·인과 증거를 추가하지는 않는다.

**바꿀 문장**

> 기존 MP 참조 6.336 eV가 r2SCAN 구조최적화에서 유래해 동일 근사 비교가 아니었음을 조회 기록에서 확인했다. 기본 StructureMatcher에서 유사하다고 판정된 다른 NdP₅O₁₄ 엔트리의 GGA NSCF 갭 5.3904 eV는 우리 값과 약 +0.003 eV 차이다. 이는 보조 비교이며, 동일 구조·동일 조건의 재현이나 차이의 원인 분해를 확정한 것은 아니다. 부피 기여는 이 자료만으로 배제하지 않는다. 등록 예측 실패와 9종 집계, 현재 인용 제한은 유지한다.

‘MP 값도 전부 PBE’는 ‘참조마다 origins/task의 계산 종류를 확인하며, 다른 9종의 동일 근사 여부는 이번 조회로 검증하지 않았다’로 바꾼다. 새 계산을 요구하는 것이 아니라 **현재 증거로 말할 수 있는 선을 고치는 것**이다.

### P0-3. Nd₂S₃를 산화 산물로 바꿔 읽고, 작은 갭만으로 전자 누설을 확정한다

**위치·정확한 인용**

- [01_읽기_지침서.md:154](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/01_읽기_지침서.md:154>): `산화 쪽 Nd₂S₃ 는 갭 0.76 eV 로 오히려 샌다(MP 소환값)`
- [03_송부판_페이지.html:332](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:332>): `산화 쪽 Nd 산물은 부동태가 아니다`
- [03_송부판_페이지.html:333](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:333>): `0.76 eV` / `로 전자가 샌다(MP 소환값).`

**근거·실패 상황**

[db/properties/cei_esw_Li_x002_2026_09_28.json](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/db/properties/cei_esw_Li_x002_2026_09_28.json>)에서 Nd₂S₃는 `neutral_rxn`에 나온다. Nd 계의 `oxidation_onset_rxn`에는 **Nd₁₀S₁₉**가 나온다. 두 상의 갭을 옮길 수 없다.

또한 갭은 전도도 자체가 아니다. 캐리어 농도·이동도·결함·접촉 및 상 연결성을 모른 채 0.76 eV만으로 ‘샌다’, ‘부동태가 아니다’를 확정하면, 큰 갭만으로 부동태를 증명하면 안 된다는 자기 규칙을 반대 방향으로 위반한다.

**바꿀 문장**

> 중성 분해 조합에는 Nd₂S₃가 있으며 그 MP 참조 갭은 0.76 eV다. 산화 개시 조합의 Nd 상은 Nd₁₀S₁₉이므로 이 값을 대신 쓸 수 없다. 해당 조합의 전자 누설과 실제 부동태 성립 여부는 현재 자료로 판정하지 않는다.

### P0-4. 충전 때 Li 이동 방향과 고정 전압 계산의 제어변수를 잘못 가르친다

**위치·정확한 인용**

- [03_송부판_페이지.html:1933](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:1933>): `전지를 충전하면 전해질에서 Li 가 양극 쪽으로 빠져나간다`
- [03_송부판_페이지.html:1044](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:1044>): `고전압이란 Li 가 양극으로 빠져나간 상태`
- [01_읽기_지침서.md:69](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/01_읽기_지침서.md:69>): `“Li 를 이만큼 뺐을 때” 를 여섯 번 따로 물어본 거예요.`

**근거·실패 상황**

통상적인 Li-ion 전지 충전에서는 양극에서 Li가 빠져 음극 쪽으로 간다. 문서 뒤의 2112행도 ‘전해질을 건너 음극으로’라고 적어 앞 설명과 충돌한다. [DOE의 충전 설명](https://www.energy.gov/cmei/vehicles/articles/reducing-reliance-cobalt-lithium-ion-batteries)

더 중요한 점은 이 hull 계산이 공간적 Li 이동을 추적하는 모델이 아니라는 것이다. 원자료의 `axis_convention`은 Li 저장고의 **화학퍼텐셜**을 지정한다. 전압별로 제거할 Li 개수를 먼저 정하는 것이 아니다. 방출/흡수량은 해당 μ에서 선택된 반응식의 결과다.

**바꿀 문장**

> 충전 시 양극에서 Li가 빠져나간다. 이 계산에서는 그 이동 경로를 추적하지 않고, μLi=μLi,metal−V인 Li 저장고와 평형을 이루는 산물 조합을 전압별로 구한다. 주고받는 Li의 양은 미리 정한 입력이 아니라 계산 결과다.

1044·1198·1933·2048·2061행과 지침서의 대응 비유를 함께 맞춘다.

### P0-5. ‘해상도 안이므로 크기는 금지, 물리적 방향만 확정’이라는 안전장치가 성립하지 않는다

**위치·정확한 인용**

- [01_읽기_지침서.md:98](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/01_읽기_지침서.md:98>): `크기는 인용하지 않고 부호만`
- [00_START_HERE.md:55](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/00_START_HERE.md:55>): `Li 자리 +(덜 반응) · P 자리 −(더 반응).`
- [02_AI_프롬프트.md:54](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/02_AI_프롬프트.md:54>): `x = 0.02 의 Δ 크기는 유의폭 ±0.010 eV/atom 안이라 부호만 말한다.`

**근거·실패 상황**

원장의 평균 +0.0066 / −0.0050 eV/atom은 문서 스스로 정한 ±0.010의 구분폭 안이다. 계산값의 대수적 부호는 그대로 보고할 수 있다. 그러나 그 부호를 ‘실제 더/덜 반응한다’는 해소된 방향으로 승격시키지는 못한다. 이 ±0.010을 통계적 신뢰구간으로 새로 해석하는 것도 아니다.

사전등록 개정문 자체가 ‘부호·가산성만’을 허용하고 있으므로 화면 전사 오류는 아니다. **그 운영 규칙을 물리적 확증처럼 설명한 것이 문제**다. 사전등록은 규칙 변경의 투명성을 지키는 장치이지 잘못된 추론을 유효하게 만들지는 않는다.

**바꿀 문장**

> 계산된 Δ의 부호는 Li 자리에서 +, P 자리에서 −다. 다만 평균 크기는 이 캠페인의 사전등록 구분폭 안이므로, 이를 물리적으로 해소된 개선·악화 또는 반응성 순위로 해석하지 않는다.

문턱과 구형 판정은 보존하고, 현재 인용 해석을 명시적으로 보완한다. 개별 칸이 평균과 같은 판정인지도 구별한다.

### P0-6. 한 조건의 ‘P 10% 대 90%’를 전 조건의 배분 법칙으로 복사한다

**위치·정확한 인용**

- [02_AI_프롬프트.md:57](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/02_AI_프롬프트.md:57>): `나머지 9 할은 여전히 양극 전이금속 인산염이다.`
- [03_송부판_페이지.html:211](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:211>): `나머지 9 할은 무도핑처럼 양극 TM 인산염`

**근거·실패 상황**

LiCoO₂ 4.3 V 사례의 10:90은 맞다. 하지만 원자료 [db/properties/cei_interface_V_x002_2026_09_28.json](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/db/properties/cei_interface_V_x002_2026_09_28.json>)에서:

- LiCoO₂ **2.5 V** · 목표 P자리 조성의 최소 반응은 P를 `0.306 Li3PO4 + 0.006376 NdPO4`로 보내며, Co는 `CoS2`로 간다. 남은 P가 TM 인산염이라는 설명은 여기서 직접 틀린다.
- LiMnO₂ **4.3 V** · 목표 조성은 `0.4469 P2S7 + 0.06393 PCl5 + 0.007444 Mn(PO3)2`를 포함한다. 해당 칸은 보호율 게이트에서 제외되므로 ‘보호’ 증거로 쓰면 안 되지만, 전 조건 P 배분을 일반화해서는 안 된다는 반례다.

P 원자의 분율과 반응한 TM의 분율도 다른 분모다. 이미 §2b가 정확히 설명한 예외를 첫 화면과 AI 규칙이 지운다.

**바꿀 문장**

> LiCoO₂ 4.3 V의 x=0.02 사례에서는 P의 약 10%가 Nd 인산염, 약 90%가 Co 인산염에 배정된다. 다른 양극·전압에서는 Li 인산염·티오인산염 등으로도 가므로 이 배분을 일반화하지 않는다. P 포획률과 TM-인산염 감소율은 별도로 보고한다.

### P0-7. 인계 카드의 Fig. 2 재현 명령은 옛 계열 파일을 조용히 덮어쓴다

**위치·정확한 인용**

- [00_START_HERE.md:118](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/00_START_HERE.md:118>): `python3 tools/figures/plot_cei_p_host_ladder.py --rec db/properties/cei_p_host_ladder_x002_2026_09_28.json --nd_bearing ndo_li_002,nd_p_002_asused`
- [tools/figures/plot_cei_p_host_ladder.py:238](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/tools/figures/plot_cei_p_host_ladder.py:238>): `ap.add_argument("--out", default=str(OUT))`
- [tools/figures/plot_cei_p_host_ladder.py:331](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/tools/figures/plot_cei_p_host_ladder.py:331>): `png = out_dir / "cei_p_host_ladder.png"`

**실행 재현**

첨부 복사본의 루트에서 문서대로 실행하면 rc=0이지만, 다음 **배포된 기존 파일 2개가 변경**된다.

- `db/properties/cei_figs/cei_p_host_ladder.png`
- `db/properties/cei_figs/cei_p_host_ladder_fig.csv`

송부 화면이 읽는 `cei_p_host_ladder_x002.png`를 갱신하는 것이 아니다. x=0.02 데이터가 일반 이름의 이력 파일을 덮고 현재 화면은 이전 x002 그림을 계속 읽는다. ‘옛 파일을 덮지 않는다’는 인계 규칙과 정면으로 충돌한다.

**바꿀 안내 문장**

> Fig. 2는 반드시 별도 재현 폴더에 생성한다. 출력의 일반 파일명은 현행 x002 게시 파일명이 아니므로 원본 폴더에 직접 실행하지 않는다. 비교 후 x002 게시 파일로 반영할 때만 명시적으로 이름을 대응시키고 해시를 갱신한다.

안전한 명령 예:

```text
python3 tools/figures/plot_cei_p_host_ladder.py --rec db/properties/cei_p_host_ladder_x002_2026_09_28.json --nd_bearing ndo_li_002,nd_p_002_asused --out review_output/fig2_x002
```

계열별 파일명을 생성기가 보장하도록 바꿀 수도 있다. 어느 방식을 택하든 ‘재현 후 이력 파일의 해시는 불변’이라는 음성/회귀시험으로 닫는 것이 맞다. 이 리뷰에서는 고치지 않았다.

## 3. P1 — 보내기 전 고치면 좋음

### P1-1. 94%의 합산 범위가 인계 요약에서 사라진다

- 위치: [00_START_HERE.md:53](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/00_START_HERE.md:53>), [01_읽기_지침서.md:111](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/01_읽기_지침서.md:111>), [02_AI_프롬프트.md:58](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/02_AI_프롬프트.md:58>).
- 인용: `인산염을 면한 양극 금속의 94 % 는 황화물이 된다.`
- 근거: 직접 재계산한 값은 72개 유효 칸에서 TM 인산염 감소분 합 4.86134, TM 황화물 증가분 합 4.56330의 비 **93.8693%**다. 서로 다른 조건에서 정규화한 분율 차의 합이며, 단일 셀의 생성물 수율이나 원자를 추적해 얻은 이동 확률이 아니다. 원 화면의 ‘72칸 합계’는 맞는데 요약이 이를 삭제했다.
- 바꿀 문장: **“보호율이 정의되고 게이트를 통과한 72조건에서, 정규화된 TM 인산염 감소분의 합에 대한 TM 황화물 증가분의 합의 비가 약 94%다. 개별 조건의 전환율은 아니다.”**

### P1-2. 공통 상을 ‘판별력이 전혀 없다’고 가르치는 것은 지나치다

- 위치: [03_송부판_페이지.html:1547](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:1547>), [03_송부판_페이지.html:1578](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:1578>).
- 인용: `공통 피크는 차이를 말해 주지 않는다` / `공짜로 줘도 이 질문엔 못 쓴다.`
- 근거: 두 조건에 같은 상이 있어도 양·연결성은 달라질 수 있다. 문서 자신의 황화물 재배분이 그 예다. XRD에서도 공통 피크의 강도·폭·위치 차는 정보를 가진다. 10종만 측정한 **존재 여부 기반 범위 제한**은 유지할 수 있지만, 공통 상이 물리적으로 무의미하다는 논증은 성립하지 않는다.
- 바꿀 문장: **“이번 갭 계산은 한쪽에만 출현하는 비-TM 상으로 대상을 제한했다. 공통 상의 양과 연결성 변화는 판별에 기여할 수 있으나 이번 갭 비교의 범위 밖이다.”**

### P1-3. 같은 MP 보정 체계라는 이유만으로 보정이 전부 상쇄되지는 않는다

- 위치: [03_송부판_페이지.html:2305](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:2305>).
- 인용: `같은 눈금끼리 빼면 보정이 상쇄된다.`
- 근거: MP 보정은 화학 환경·음이온 종류·GGA/+U 적용 등에 달린다. 동일 체계 사용은 비교의 필요조건이지만, 산물 조합과 보정 적용 원자 수가 다르면 잔여 보정이 남을 수 있다. 특히 이 분석은 산화물/인산염/황화물 사이 배분 변화를 본다. [MP 보정 설명](https://docs.materialsproject.org/methodology/materials-methodology/thermodynamic-stability/thermodynamic-stability/anion-and-gga-gga%2Bu-mixing)
- 바꿀 문장: **“일관된 MP 보정 체계에서 Δ를 비교한다. 공통 보정항은 상쇄될 수 있지만, 반응물·산물의 조합이 달라 보정 및 모델 오차가 전부 없어지는 것은 아니다.”**
- 이번 자료로 실제 잔여 보정의 크기를 계산한 것은 아니다. ‘상쇄 보장’이라는 일반 명제가 근거 없다는 지적이다.

### P1-4. frozen-4f 계산의 갭을 엄밀한 ‘하한’으로 부를 근거가 없다

- 위치: [03_송부판_페이지.html:1634](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:1634>).
- 인용: `Nd 함유 상은 4f 배치 때문에 <strong>하한</strong>이다.`
- 근거: PBE가 갭을 과소평가하는 경향과, 4f를 코어에 고정한 모형이 실제 갭의 하한을 보장한다는 명제는 다르다. 4f 상태가 갭 안에 들어와 최소 갭을 바꾸는 사례도 있어 일반적인 단조 오차 방향을 가정할 수 없다. [희토류 산화물의 밴드 가장자리 연구](https://arxiv.org/abs/1208.0503)
- 바꿀 문장: **“Nd 함유 상의 갭은 frozen-4f PBE 모형에 조건부인 값이다. 실제 갭에 대한 엄밀한 하한이나 전도도 예측으로 취급하지 않는다.”**
- 이 문장 정정 때문에 기존 10종 계산을 다시 하라는 뜻은 아니다.

### P1-5. ‘충돌하면 카드 우선’은 이미 철회한 문구를 되살린다

- 위치: [00_START_HERE.md:135](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/00_START_HERE.md:135>), [03_송부판_페이지.html:2363](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:2363>), [02_AI_프롬프트.md:35](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/02_AI_프롬프트.md:35>).
- 인용: `충돌하면 카드가 이긴다` / `페이지와 자료가 다르면 원자료가 맞다.`
- 근거: 원고 틀 카드 41행은 `Nd 는 창을 0.22 V 좁힌다.`, 50행은 `그 코팅의 기능을 in-situ 로 한다고 보인다`를 유지한다. 현재 페이지·인계 규칙은 전자를 정량 인용하지 않고 후자의 부동태 기능도 미확정으로 둔다. 숫자의 원본성, 현재 인용 허가, 원고 제안의 권위를 한 순서로 정하면 충돌을 잘못 푼다.
- 바꿀 문장: **“숫자는 해당 원자료에서 확인하되, 인용 허용 범위는 현재 유효한 결정과 인용위험 조건을 함께 따른다. 원고 틀은 제안이며 이를 확대하지 못한다. proposed 또는 과거 자료에 숫자가 존재한다는 이유로 인용을 승인하지 않는다.”**
- CEI 관련 유효 결정·hazard의 인계용 발췌를 붙이면 좋다. 전체 원장을 ZIP에서 뺀 사실은 이미 안내되어 있으므로, 이를 숨긴 누락이라고 판정하지는 않았다.

### P1-6. ‘목표 조성 약 618원자’에는 실제 원자 수·조성 근거가 없다

- 위치: [00_START_HERE.md:78](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/00_START_HERE.md:78>), [03_송부판_페이지.html:283](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/03_송부판_페이지.html:283>), [02_AI_프롬프트.md:81](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/02_AI_프롬프트.md:81>).
- 인용: `목표 조성의 원자 구조 계산(약 618 원자)은 못 돌린다.`
- 근거: 선언된 목표 조성 Li₅.₄₄Nd₀.₀₂P₀.₉₈S₄.₃₇O₀.₀₃Cl₁.₆를 **완전 점유 정수 원자로 정확히** 표현하면 최소 100식단위, Li544 Nd2 P98 S437 O3 Cl160 = **1244원자**다. 50식단위는 총 622원자에 S218.5/O1.5가 남는다. 618은 Li자리 조성의 50식단위 총수와는 맞지만 역시 O/S 정수화가 필요하다. 근사 조성 셀을 뜻한다면 그 근사와 실제 파일을 밝혀야 한다.
- 바꿀 문장: **“현재 목표 조성에 대응하는 구조 계산은 없다. 정확한 정수 점유 조성에는 최소 1244원자가 필요하며, 더 작은 근사 조성 셀은 아직 별도로 정의하지 않았다.”**
- 하드웨어에서 실행 가능한지 자체는 시험하지 않았다. 특정 셀의 불가능 판정에는 실제 셀과 방법·자원 근거를 붙여야 한다.

## 4. 송부판에서 빠지면 안 되는데 빠진 것

### 확인된 1건 — 생성기와 손편집 정본의 관계

정본 [db/properties/cei_figs/index.html:2612](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/db/properties/cei_figs/index.html:2612>)의 다음 안내가 송부판에서 빠졌다.

> 이 index.html 이 손편집 정본

같은 문장은 생성기가 그림·CSV·참고 조각 `sections_new.html`만 만들며 정본 HTML을 덮어쓰지 않는다고 설명한다. 생성기 재현을 받는 사람에게 시키는 인계에서는 이것이 단순 작업 이력이 아니라 **어느 산출물을 어디에 반영해도 되는가**를 결정하는 규칙이다. 참고 조각을 현행 페이지로 오인해 덮으면 갭 예측 실패·현행 한정 문구를 되돌릴 수 있다.

송부 페이지에 꼭 둘 필요는 없지만, 최소한 인계 카드의 재현 절에 다음을 복원한다.

> 페이지 HTML은 손편집 정본이다. 생성기의 sections_new.html은 참고용 조각이므로 정본이나 송부판을 대체하지 않는다. 그림·CSV만 별도 폴더에서 재현해 대조한다.

그 밖에 확인한 삭제는 정정 이력·과거 오답·내부 대화가 중심이었다. 환원 한계 정정, Li 장부, P₂S₇ 예외, x=0.20 이름표, NdP₅O₁₄ 등록 실패·인용 조건 등 **핵심 제한의 일반적인 삭제는 발견하지 못했다**. 이번 P0 대부분은 편집하면서 새로 생긴 결함이 아니라 정본에도 있던 주장이 송부판·지침서로 복제된 것이다.

## 5. 민감정보·권한

첨부에서 이메일 주소가 있는 비준자 필드 4개를 확인했다. 여기에는 주소를 재인용하지 않는다.

- [db/properties/cathode_cei_decomposition_estimand_2026_09_16.json:234](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/db/properties/cathode_cei_decomposition_estimand_2026_09_16.json:234>)
- [db/properties/cathode_cei_dopant_decomposition_amendment_2026_09_16.json:99](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/db/properties/cathode_cei_dopant_decomposition_amendment_2026_09_16.json:99>)
- [db/properties/cathode_cei_gap_target_amendment_2026_09_16.json:118](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/db/properties/cathode_cei_gap_target_amendment_2026_09_16.json:118>)
- [db/properties/trivalent_dopant_screen_amendment_C_gate_2026_09_16.json:125](<C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/cei_handoff_2026_09_30/db/properties/trivalent_dopant_screen_amendment_C_gate_2026_09_16.json:125>)

이름/이메일이 있다는 것만으로 금지된 유출이라고 판정하지 않는다. 반대로 **이번 리뷰 요청을 외부 공개 동의로 간주하지도 않는다.** 수신자·비공개 링크의 공개 범위에 대한 본인의 동의를 확인하면 원본 송부가 가능하다.

빼려면 봉인 원본은 보존하고 **별도 송부용 파생본**을 만든다. 역할 식별자로 치환한 항목, 원본 파일 해시, 파생본 해시, redaction 목록을 남긴다. 파생본의 내용 해시가 바뀌었으므로 원본과 동일한 봉인 검증을 통과한다고 표시하면 안 된다.

gabia의 내부 절대경로는 비밀번호가 아니라 실행 위치/출처다. 출처 표기는 가능하나 수신자가 실행 가능한 경로처럼 안내하지 않는다. 관련 계정·서비스의 접근권한까지 점검한 것은 아니다.

## 6. P2 — 교육·AI 프롬프트 제안 (위 사실 오류와 별도)

1. **용어를 세 층으로 나눈다.** ‘계산값’, ‘원장에 따른 판정’, ‘실험 기전 해석’을 답변에서 분리한다. 예: ‘TM-인산염 분율 감소’와 ‘열화 억제’는 같은 층이 아니다.
2. **도둑·경비·미끼 비유는 순서를 만들지 않게 한다.** “Nd가 먼저 가로챈다” 대신 “최종 평형 배분에서 Nd에 들어가는 P가 늘어난다”를 붙인다. 실제 선후·속도는 계산하지 않았다.
3. **금리 비유는 고정 가격으로 보완한다.** μ는 저장고와 Li를 교환하는 가격에 가깝다. 가격이 정해졌다고 교환량까지 정해지는 것은 아니다. 레고 비유에는 ‘제공된 블록 목록 안에서의 최적 조합이며 공간적 층의 연속성을 재지 않는다’를 붙인다.
4. **AI 답변은 조건·필드·상태를 같이 요구한다.** 숫자에는 파일/필드, 양극·전압·농도·자리, 분모, active/proposed/철회 여부를 붙인다. 파일을 못 읽었다면 “문서에 그렇게 적혀 있으나 원자료 검증은 못 했다”라고 답하게 한다. 프롬프트만으로 환각 방지가 보장된다고 하지는 않는다.
5. **회귀시험의 다음 범위는 인계 문서다.** 현재 95개는 유용하지만 새 00/01/02와 송부판의 주요 결론을 전부 검사하지 않는다. 최소한 P0-3의 산물 이름, P0-6의 조건 한정, P0-7의 역사 파일 불변을 실제 깨뜨렸을 때 시험이 실패하는지 확인한다. 스타일 문구의 전면 하드코딩은 필요 없다.

## 7. 해제조건

1. P0-1~6의 잘못된 인과·일반화·교육 문장을 **정본, 송부판, 00/01/02, 원고 틀**에서 같은 뜻으로 정정한다. 봉인된 과거 기록은 덮지 말고 정정/현행 해석을 연결한다.
2. P0-7의 재현 명령을 격리 출력으로 바꾸고, 재실행 후 역사 PNG/CSV의 해시가 그대로이며 어떤 파일이 Fig. 2에 대응하는지 확인한다.
3. 생성기 참고 HTML을 정본으로 대체하지 말라는 안내를 인계 카드에 복원한다.
4. NdP₅O₁₄는 proposed 상태 그대로 인계해도 된다. **‘원인 확정’이 아니라 확인된 참조 차이와 남은 한계를 병기하면 비준 완료를 송부의 필수조건으로 만들 필요는 없다.**
5. 이메일 원본 전달 동의 또는 정당하게 표시된 파생본 방식을 정한 뒤 수정된 ZIP의 해시 목록을 다시 만든다.

핵심은 계산을 더 돌리는 것이 아니라, **자료에 이미 있는 조건과 미확정을 요약에서도 잃지 않는 것**이다.

## 검증 기록

독립 재계산·상태 대조는 [numeric_evidence.json](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/numeric_evidence.json), 해시 대조는 [hash_audit.json](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/hash_audit.json), 송부판 대조는 [canonical_to_shipping.diff](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/canonical_to_shipping.diff), Fig. 2 재현 로그는 [repro_command_2.txt](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cm_fbfb63946/repro_command_2.txt)에 남겼다.
