# v3 시각·가독성 검토: p01–p09

검토 범위: v3 contact sheet 및 p01–p09를 각각 원래 1280×960 렌더로 열람했다. PPTX의 text box, run, paragraph, master와 그림 geometry를 읽었다. 원본 파일 변경, 새 이미지 제작, 재렌더, 계산 실행은 하지 않았다. 아래는 **제안 좌표**이며 수정판 렌더에서 재확인이 필요하다. 단위는 10×7.5 in 슬라이드 왼쪽 위 기준 `x, y, w, h`이다.

## 첫인상과 문법

3초 첫인상: **학교·연구실 템플릿을 유지한 실제 진행보고 초안으로 보이며, 가장 먼저 보이는 미완성 신호는 여섯 빈 패널과 p07의 많은 글이다.** 작성 주체나 AI 사용 여부를 시각만으로 판별할 수 있다는 뜻은 아니다.

같은 그림 본문 틀 12장, 꺾쇠 캡션, 두 칸 자체는 제공한 연구실 문법이다. 이를 일괄 삭제하거나 새 디자인으로 바꾸는 것은 개선 근거가 없다. 반복 틀보다 p02의 박스 가장자리까지 차는 작은 문구, p07의 수평선에 걸린 제목, p04·06·08·09의 화면 속 제작 명령이 자동 조립된 초안이라는 느낌을 강하게 만든다. 차트와 3D 그림의 시각언어가 서로 다른 점은 재사용 연구자료의 자연스러운 흔적이다.

원래 10-13 기준 덱은 동봉하지 않았으므로 **원본과 같은 밀도·줄간격·색 사용이라고 인증할 수 없다.** 현재 파일에서 section 24 pt, body 13 pt, caption 10 pt는 확인한다. 중요한 차이: 요청서는 ■ 제목을 15 pt라고 하지만, 실제 p02 등의 제목 run에는 `sz`가 없고 일반 도형으로서 master `otherStyle` 및 presentation `defaultTextStyle`의 **18 pt**를 상속한다. JSON의 `font_sizes_pt`는 명시된 run 값만 수집하므로 상속 글자 크기의 전수 목록이 아니다. 실제 제목을 13 pt로 잘못 읽거나, 15 pt로 일괄 줄이면 안 된다.

권장 공통값:

- section·로고·바닥글·폰트 계열은 유지한다. ■ 제목은 현재 실효 18 pt를 유지하되 한 줄짜리 주제명으로 줄인다. 제목 15 pt가 정확한 템플릿 계약이라면 원본 덱 확인 뒤 적용한다.
- 본문은 내용을 줄이고 **15 pt**로 복원한다. 현 그림 본문 틀의 paragraph line spacing은 150%, p07 상단은 130%, 두 칸 본문은 110% + before 7 pt다. 본문 15 pt에서 기존 150%를 무조건 유지하면 다시 길어진다. 그림 본문은 120–130%, paragraph after 4–6 pt 정도를 출발점으로 렌더 비교한다. p07 두 칸은 110–115%, before 4 pt로 충분하다.
- 그림을 읽는 데 필요한 qualifier·캡션은 **12 pt 이상**, 핵심 수치·정의는 본문 15 pt에 둔다. 10 pt 출처는 추적용으로만 사용하고 거기에 주장의 핵심 한정어를 숨기지 않는다. 12 pt가 모든 강의실 뒷줄에서 읽힌다는 보증은 아니다. 실제 투영 크기와 거리를 모르는 조건의 하한 권장이다.
- 새 그림 F1은 슬라이드에 놓인 뒤 기준으로 제목 14–15 pt, 설명 12–13 pt를 목표로 한다. 재사용 래스터 그림은 확대하면 내부 글자도 커지지만 폰트만 따로 편집할 수 없고 해상도 한계가 있다. 현재 글씨를 읽어야만 성립하는 핵심은 15 pt 본문에 반복한다. 모든 세부 눈금을 뒷줄에서 읽히게 하겠다는 목표보다 그림당 읽을 핵심을 정하는 편이 낫다.
- p01–p09에는 우상단 source tag 자체가 없다. 생성기의 `body_slide`가 복제한 source box를 삭제하고, 이 장들에서 `tag()`를 다시 부르지 않는다. 따라서 '출처 줄의 자리와 크기가 원형대로 유지됐다'는 판정은 불가하다. 필요한 직접 인용은 짧은 `[n]`를 해당 문장 또는 캡션 12 pt로 붙이고, 긴 경로는 notes로 둔다.
- 현재 강조색은 과하지 않다. 반복틀·꺾쇠 캡션·기관 로고를 AI 흔적으로 잡지 않는다. p07의 길고 보편적인 결론 문장은 시각 효과보다 과학적 범위와 문장 길이가 문제다.

## 장별 구체 제안

### p01 — 손질, 이메일 가림

확인: 저자 상자는 `(0.6805,2.9356,6.4457,1.4159)`, 캠퍼스 그림은 `(1.4563,3.8419,8.5437,3.6093)`이다. 렌더에서 이메일 오른쪽이 건물 그림에 겹친다. 날짜 `[date — to be set]`는 의도이므로 지적·입력 대상이 아니다.

**P0 화면 충돌 수정:** 캠퍼스/로고는 움직이지 않고 저자 블록의 빈 문단을 제거한다. 저자 블록 목표 `(0.68,2.98,8.40,0.75)`, 이름 16 pt, 소속·이메일 14 pt, 세 줄, paragraph 간격 0, line spacing 약 18 pt. 블록 아래가 그림 위 3.84 in보다 위에 오도록 한다.

화면 문구는 그대로 세 줄로 정돈한다:

> Yonghoon An  
> Division of Materials Science & Engineering, Hanyang University  
> (E-mail: yonghoon71@hanyang.ac.kr)

제목의 `cathodes:` 한 단어 줄바꿈은 거슬리지만 이메일 가림보다 후순위다. 기존 제목을 줄이거나 날짜를 채우는 것을 필수로 요구하지 않는다.

### p02 — 손질, F1 글씨와 상자 간섭

확인: F1 실제 삽입 좌표는 fit 결과 `(1.4439,3.35,7.1123,2.65)`다. 생성기에 넘긴 `(0.5,3.35,9.0,2.65)`와 실제 image width는 다르다. 첫 두 박스의 bold heading이 좌우 테두리에 거의 닿거나 걸리고, 회색 calibration 문구는 렌더 기준 약 7–8 pt 상당이다. 단순히 PNG 폭만 9 in로 지정하고 높이를 2.65 in로 유지하면 확대되지 않는다.

**P0:** 기존 SEM-01의 과학 문구 수정과 함께 F1 안 문장을 줄인다. 그림을 목표 `(0.77,3.00,8.46,3.15)`로 확대한다(동일 aspect ratio). 캡션은 `(1.0,6.28,8.0,0.36)`, 12 pt. 상단 제목·본문을 먼저 줄여 그림 윗변과 0.15 in 이상 간격을 둔다.

권장 짧은 ■ 제목: `DEM, MPM and voxel transport`.

F1 각 박스의 역할을 나타내는 단문 후보(원래 과정·화살표 순서 유지):

| 박스 | 제목 | 설명 |
|---|---|---|
| 1 | `Powder packing and compaction` | `DEM` / `Spherical particles` / `Contact forces` |
| 2 | `Plastic electrolyte compaction` | `MPM` / `Fixed AM skeleton` / `Plastic SE` |
| 3 | `Voxel transport` | `Finite volume` / `Ionic, electronic and thermal transport` |
| 4 | `Electrode response (planned)` | `Reaction distribution` / `Rate capability` |

박스 제목은 최대 2줄, 설명 최대 3줄, 박스 양끝 0.10–0.12 in 안쪽 여백을 둔다. 과학적으로 틀린 `each calibrated…never…`, `anchored to conductivity measurements`를 가독성 목적으로 notes에 옮겨 보존하지 않는다. 기존 과학 리뷰의 교정으로 대체한다. 이 회색 아래 라벨을 삭제하는 것은 작은 글자와 과장 두 문제를 함께 해결한다.

### p03 — 손질, 그림을 읽는 정보의 우선순위

확인: 4단계 3D 이미지 `(0.5404,3.45,5.5191,2.55)`, G1 `(6.20,3.3256,3.40,2.6488)`. 3D 자체와 색 대비는 좋다. 아래 porosity label은 약 8–9 pt, 오른쪽 graph의 tick·숫자도 작아 투영 뒷줄에서 세밀한 비교가 어렵다. 3D 형태는 compaction progression을, G1은 조성 경향을 지지하므로 둘 다 장식은 아니다.

**P1:** ■ 제목 `Composition dependence of DEM porosity`. 첫 bullet `One bed per composition, compacted to 300 MPa with linear hysteretic contacts.` 15 pt. 둘째 bullet은 `7:3 has the lowest porosity among these five simulated beds.` 15 pt. 4단계 숫자 나열은 그림과 중복이므로 **notes로 넘기거나**, 강연에서 꼭 읽을 값이면 12–13 pt 캡션에 직접 적는다. tiny image label만을 읽게 하지 않는다.

추천 caption 두 줄: `< 7:3 bed: porosity 31.8%, 25.1%, 16.7%, 16.5% >` / `< checkpoints: 0, 47, 296, 165 MPa >`. 마지막이 무하중 상태로 보이지 않도록 기존 과학 리뷰의 상태 명칭을 적용한다. 캡션 상자 `(0.55,6.02,5.55,0.62)`, 12 pt. 우측 캡션 `(6.1,6.05,3.6,0.55)`, 12 pt, `< one bed per composition >` 또는 조성 축 해석을 유지한다.

그림 확대를 택한다면 오른쪽 목표 `(5.75,3.00,3.90,3.04)`, 왼쪽 목표 `(0.55,3.37,5.05,2.33)`. 이는 우측 plot을 약 15% 키우지만 모든 내부 글자가 12 pt가 되는 것은 아니다. **재사용 그림 재작성, 두께 curve/axis 삭제, 가짜 error bar 추가는 제안하지 않는다.**

### p04 — 손질, 제작문이 밀도를 키움

확인: 좌측 graph 실제 `(0.638,3.45,2.5741,2.55)`, 가운데 `(3.5837,3.45,2.6825,2.55)`, placeholder `(6.55,3.45,3.0,2.55)`. 현 118단어 중 placeholder 47단어를 제외하면 약 71단어다. 이 장의 인상은 긴 제목+2줄 bullet 두 개+작은 세 패널 때문에 빽빽하다. 빈 상자를 실패한 그림으로 계산하지 않는다.

**P1:** ■ 제목 `Li⁺ transport in a contact network`. 본문 15 pt 후보:

> Hertz contact radii, σ₀ = 1.5 mS cm⁻¹.  
> T = φSE σ₀/σeff. Constriction accounts for 73–75% of model Joule dissipation.

이 표현의 과학 범위는 기존 SEM-11을 적용한다. 원래 `not in path length` 대조문과 반복적인 긴 과정 설명은 삭제 대상이다. 읽는 데 필수인 Hertz/σ₀/모형 내 몫을 10 pt 캡션에만 맡기지 않는다.

두 graph를 더 읽히게 하려면 fit container를 각각 `(0.45,3.00,3.25,3.05)`, `(3.80,3.00,3.25,3.05)`로 늘리고 placeholder를 `(7.20,3.30,2.35,2.55)`로 조정한다. 그래프 원본·축·데이터는 유지한다. 공통 12 pt caption 상자 `(0.50,6.17,6.45,0.58)`에 `Hertz-radius network model; PC:SC = large:small NCM` 같은 필요한 해석을 넣는다(문장부호는 현 템플릿에 맞춰 두 줄 가능).

두 y축은 0이 아닌 값에서 시작한다. reusable plot이므로 다시 그리라는 요구 대신, 막대 **높이 비율**로 효과 크기를 읽으면 안 된다고 notes에 남기고 본문에는 실제 범위·정의만 쓴다.

placeholder 화면은 14 pt, 최대 3–4줄로 줄인다:

> 7:3 ionic-current pathways  
> Hertz-radius network  
> Image pending

긴 `webapp…scripts…WSL…` 두 문단은 모두 notes로 옮긴다. 실제 source/run 및 top 50% 정의가 확정되기 전 `actual current pathways` 캡션은 `current-path visualization planned`로 바꾼다. 그림이 끝내 없으면 **좌측 두 graph만으로 이 장 주장은 성립**한다. 오른쪽은 14 pt definition note로 대체할 수 있다. 장 합치기는 필요 없다.

### p05 — 손질, 그래프 detail보다 한계가 먼저

확인: 그림 `(0.50,3.5126,5.50,2.4749)`, 문헌 요약 `(6.20,3.60,3.40,2.40)`, 요약은 12 pt. 그림은 hysteretic law의 작동을 보여주며 58% damping 실측 근거 그림 자체는 아니다. 따라서 그림 caption의 `code reproduction`은 유지한다. 일부 곡선 설명·legend는 약 7–9 pt 상당이므로 모두 읽히는 slide가 아니다.

**P1:** ■ 제목 `Limitations of the current DEM implementation`. 본문 15 pt에서 두 bullet을 짧게:

> Fixed particle shapes. SE modulus reduced from 24 to 1.35 GPa as a model parameter.  
> Global damping supplies 58% of plate reaction in one 7:3 bed during compression.

첫 문장의 24 GPa 재료·출처 한정은 과학 교정에 따르며, 이 수치를 근거 없이 다른 재료의 고유값으로 표현하지 않는다. 이력 법칙의 모든 기호 설명과 선정 문헌 조사 절차는 notes로 둔다.

그림 목표 `(0.40,3.15,6.00,2.70)`, caption `(0.60,6.05,5.60,0.45)`, 12 pt. 문헌 summary 목표 `(6.55,3.35,3.05,2.45)`, 14 pt. 문구:

> 22 selected DEM studies  
> SE softening: 0/22  
> Yield or hardness cap: 7/22  
> Linear hysteresis: 1/22  
> Global damping: not reported

문헌을 전수 조사한 듯 읽히지 않도록 `selected`와 author-classification notes를 유지한다. 왼쪽 그래프 확대 후에도 가장 작은 symbol은 뒷줄용 본문이 아니다.

### p06 — 손질, 방법 slide로는 그림 없이 성립

확인: 상단 method 설명은 53단어 수준이고 실제 밀도 대부분은 placeholder instructions다. 두 상자 `(0.60,3.45,4.30,2.55)` / `(5.10,3.45,4.30,2.55)`는 그대로 유지 가능하다.

**P1:** ■ 제목 `Plastic compaction with the material point method`. 본문 15 pt:

> J2 plasticity allows the electrolyte to deform into pores.  
> The active-material scaffold remains fixed.

왼쪽 화면 placeholder는 14 pt, `2D plastic electrolyte morphology` / `E = 1.53 GPa, σy = 0.15 GPa` / `Image pending`. 오른쪽은 `3D electrolyte around a fixed AM scaffold` / `x–z section` / `Image pending`. 기존 `2D champion`, machine/path, script command는 notes로 넘긴다. 두 caption 12 pt로 올린다.

채울 글은 '무엇'은 충분하나 현재 오른쪽 CLI가 유효하지 않다는 이전 SEM-12가 미해결이다. 두 이미지가 다른 설정이므로 동일 scale bar만 맞춰 비교 근거가 생기지 않는다. 각 run의 상태·단위·하중 시점은 notes에 붙여야 한다.

발표 전 그림 미확보 시에는 두 점선 영역을 **2D/3D method text로 대체**해도 19장 순서를 유지할 수 있다. 왼쪽 `2D formulation: deformable electrolyte`, 오른쪽 `3D formulation: fixed AM geometry and deformable SE material points`처럼 방법만 쓰며, 검증한 형태나 성과를 보였다고 말하지 않는다. 초안 검토판에서는 현재 점선을 남겨도 된다.

### p07 — 다시(내용 압축), 가장 큰 실제 글 밀도

확인: 151단어, placeholder 없는 전체 텍스트 장. 오른쪽 소제목 `(5.05,2.20,4.40,0.36)`가 2줄로 흘러 y=2.58의 rule을 통과한다. 왼쪽도 3개 bullet에 수치·문헌·해석을 한꺼번에 넣었다. 하단 conclusion `(0.40,5.55,9.20,0.38)`는 2줄로 나와 지정 높이를 넘긴다. 빈 공간이 남아도 장이 편안한 것은 아니다. 읽을 그룹이 많다.

**P0:** 오른쪽 소제목을 `Calibration target and limitations`로 교체하면 현재 좌표·14 pt로 한 줄에 들어갈 가능성이 높다. 왼쪽 `Model parameters`, 오른쪽 `Calibration target`도 가능하다. rule을 내리는 처방만으로 문구 장황함을 보존하지 않는다.

**P1, 압축 목표 80–95단어:** ■ 제목 `Electrolyte parameters and calibration`. 상단 긴 `Bulk modulus from DFT…` 문장은 핵심이 두 칸에서 다시 나오므로 삭제하고 검증된 이력만 notes로 옮긴다. 두 칸 `(0.55,2.66,4.25,2.75)` / `(5.05,2.66,4.40,2.75)`는 유지, 본문 15 pt, line spacing 110–115%, before 4 pt.

왼쪽 수치표 역할 문장 후보:

> DEM: E = 1.35 GPa  
> 3D MPM: E = 1.53 GPa, ν = 0.49, σy = 0.30 GPa  
> K = 25.5 GPa. DFT comparison: B₀ ≈ 26.2 GPa

오른쪽:

> Pure SE: 10% porosity at 300 MPa  
> Unpublished laboratory calibration target  
> Independent validation remains incomplete

아래 짧은 conclusion 후보: `Transfer to composite cathodes remains under test` (14 pt, `(0.55,5.60,8.90,0.60)`). 해당 표현은 이전 SEM-07의 보정 이력 수정과 함께 적용한다.

**notes로 넘길 실제 문장:** `It is not a literature anchor; the earlier citation was retracted`는 정확한 출처 철회 이력으로 notes에 두되, `Unpublished laboratory calibration target`은 반드시 화면에 남긴다. `softening the bulk over-crushed the bed`는 시험한 설정·결과·한계를 notes에 적는다. **`single-crystal LPSCl` 재료 오기나 `irreducible` 보편 명제는 notes로 옮기는 것으로 해결하지 않는다.** 기존 과학 리뷰대로 정정·삭제 대상이다.

### p08 — 손질(과학 비교 먼저), 큰 blank가 density를 과장

확인: 104단어 중 43단어가 제작지시다. 큰 placeholder `(0.70,3.50,8.60,2.50)`의 긴 source line은 읽을 내용이 아니라 provenance 작업이다. 제목의 `what agrees…what does not count…`가 2줄이고 body에는 결과·비판·원인추정이 함께 있다.

**P1:** ■ 제목을 `MPM comparisons under different initializations` 또는 더 짧게 `DEM-scaffold MPM: comparison limits`로 바꾼다. 15 pt 본문에서 역사적 scaffold와 별도 300 MPa run을 구분한다. 기존 SEM-02와 충돌하지 않는 시각적 문장 틀:

> Earlier cell-filled SE calculation with bidirectional servo: thickness 30.7 vs 30.28 µm.  
> A separate 300 MPa run gives sphere porosity 1.13% vs 15.6% measured.

30.7 결과를 DEM-seeded SE 계산으로 설명하면 안 된다. 다른 초기화/하중 경로의 일치를 독립 검증으로 확대하지 않는 한정을 유지한다. 통합 판정문의 최소안처럼 옛 숫자 비교를 빼도 된다. `Pressed honestly`와 `AM load sharing is the missing piece`는 과도하게 매끈한 원인 단정과 구어 표현이므로 원래 과학 교정에 따라 삭제한다.

placeholder 14 pt 화면 문구: `DEM and MPM morphology` / `Source and loading history to be verified before comparison`. 기계경로·grid·dump·명령은 notes로 이동. **같은 camera보다 같은 초기화·하중 이력·판독 시점이 우선**이다. 현재 텍스트만으로 바로 figure 생성하라고 하기에는 비교 정의가 불충분하다.

미확보 시 그림 대신 출처/상태를 분리한 짧은 비교 text를 현재 넓은 영역에 넣을 수 있다. 30.7을 현재 solver 검증값으로 만들어서 빈 그림을 채우지 않는다. 장 합치기·새 계산은 필요 없다.

### p09 — 손질, method/입출력을 읽히게

확인: 133단어 중 72단어가 placeholder instructions. 표면상 p07보다 비슷하게 빽빽해도 실제 방법 설명은 약 61단어다. 동일한 두 상자 위치는 p06과 같아 입력→출력을 설명하기 적합하다.

**P1:** ■ 제목 `Voxel transport on the phase grid`. 본문 15 pt 후보:

> Finite-volume ionic and electronic transport uses ∇·(σ∇φ) = 0.  
> The thermal analogue uses temperature. Harmonic face conductivities add no separate contact resistance.

정확한 방정식 변수·solver 범위는 기존 SEM-08 및 용어 교정을 따른다. `turns morphology into a transport mesh`나 `contact-free branch`의 추상적 설명은 위 간명한 설명으로 바꾼다. harmonic mean은 notes로 옮겨도 되지만 **별도의 interface-resistance term이 없다는 모델 가정은 화면에 남긴다.**

placeholder는 기존 위치 유지, 14 pt. 왼쪽 `Phase grid` / `AM, SE, pore and additives` / `Mid-plane section, image pending`. 오른쪽 `Electronic current density` / `Planned: same bed and section at 1 V` / `Colour scale in A cm⁻²`. 둘 다 실제 데이터처럼 보이지 않도록 pending/planned를 유지한다. caption 12 pt.

`STEP3…scripts…S16/S17…export…`는 notes로 보낸다. 채울 지시에 **같은 bed/run, origin, voxel pitch, phase mapping, boundary conditions, current-density unit, source file**가 빠져 있다. S16/S17 문서 이름만으로 두 패널이 한 해의 입출력임을 보증하지 못한다. 실제 `vox 0.15` 설정 자체를 hold 수치 누출로 간주할 근거는 없다. 전도도 hold 값과 구분한다.

미확보 시 왼쪽은 `Input: phase labels and phase conductivities`, 오른쪽은 `Output: effective conductivity and current-density field`로 방법 text를 보여주면 된다. 고정 19장/순서를 바꾸지 않아도 핵심 논리가 성립한다.

## 여섯 placeholder 요약

| 위치 | 무엇은 충분한가 | 남은 provenance/지시 문제 | 발표 전 없을 때 |
|---|---|---|---|
| p04 오른쪽 | 예, 7:3 이온 전류 경로 | exact run, Hertz/FULL, top50% 정의, j 또는 I, 시점 | 두 graph로 주장 가능, definition note로 대체 |
| p06 왼쪽 | 예, 2D SE morphology | 외부 파일의 실제 존재·시점·단위, 'champion' 이름의 의미 | 2D method text |
| p06 오른쪽 | 예, 3D x–z section | 알려진 CLI 불일치, actual payload/scaffold·시점 | 3D method text |
| p08 전체 | 형태는 알 수 있음 | 비교 초기화·하중 이력이 과학적으로 불일치/미확정 | 두 비교의 출처·상태를 분리한 text |
| p09 왼쪽 | 예, phase grid | full grid source, mapping, origin, pitch, same run | input definition text |
| p09 오른쪽 | 예, 1 V current density | 실제 result 파일, 왼쪽과 같은 해인지, 단위·BC | output definition text |

빈 상자 6개를 그대로 둔 초안은 검토 가능하다. 실제 발표판에는 **제작 명령이 아닌 짧은 예정 표시 또는 방법 설명**을 보여주는 것이 낫다. six blank를 강제 완성하거나 새 계산을 하라는 요구가 아니다.

## p01–p09 최종 표

| 장 | 그대로 / 손질 / 다시 | 걸리는 것 | 고칠 것 |
|---|---|---|---|
| 1 | 손질 | 이메일과 캠퍼스 그림 중첩 | 연락처 세 줄, 빈 문단 삭제, 날짜 그대로 |
| 2 | 손질 | 긴 제목, F1 box-edge 간섭·미세 회색 글 | 문장 압축, F1 비례 확대, 과학 교정 반영 |
| 3 | 손질 | 양쪽 그림의 작은 내부 수치 | 핵심을 15 pt 본문/12 pt caption에 배치 |
| 4 | 손질 | 긴 문구와 47단어 제작지시 | 짧은 모델 정의, graph 확대, 지시는 notes |
| 5 | 손질 | 작은 law annotation, 12 pt 문헌요약 | image 확대·14 pt 짧은 요약, model reproduction 표시 |
| 6 | 손질 | 본문보다 제작지시가 더 많음 | 두 method placeholder 14 pt, provenance notes |
| 7 | 다시 | 151단어, heading/rule 충돌, 결론 overflow | 80–95단어, 한 줄 subhead, 15 pt 두 칸 |
| 8 | 손질 | 길고 방어적인 제목, 비교 정의 미해결 | 출처/초기화 분리 뒤 간결한 비교 text |
| 9 | 손질 | 긴 method prose + 제작지시 72단어 | 짧은 input/output 문구, no-interface assumption 화면 유지 |

시각만 보면 p01/p02/p07의 충돌을 고치고 production instructions를 정리하면 조건부 GO다. **전체 발표 GO는 과학 검토의 미해결 조건이 우선**이므로 이 문서가 기존 과학 보류를 해제하지 않는다.
