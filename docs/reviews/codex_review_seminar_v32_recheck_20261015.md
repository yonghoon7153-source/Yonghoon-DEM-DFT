# 연구세미나 덱 v3.2 재확인 판정

작성 2026-10-15 KST. 대상은 10-14 제출된 18장 PPTX와 PDF의 변경분이다. 소스 핀은 `90ca2c8cd6766c5e5df173533a78893cec04f6c3`. v3.1 종결본과의 승계 여부도 실제 PPTX에서 대조했다.

## 1. 결론

**현재 파일 그대로의 종결은 HOLD. 새 P1은 없고, 발표 전에 고칠 P2 세 곳이 있다. 수치 재계산이나 시뮬레이션 재실행을 요구하지 않는다.**

1. **3장:** 반지름 근사식을 포함하면서 전체를 `implemented equations`라고 부른다. 대표식이라는 표지와 ②의 근사 조건을 붙이거나 실제 지렛대 벡터로 바꾼다.
2. **11장:** `model-internal until the open checks pass`를 고친다. 내부 평형·보존 검사를 통과해도 실험 검증이 되는 것은 아니다.
3. **15장:** 같은 핀의 저자 비준은 **이완 → 언로딩 → 판 분리**인데 화면과 notes는 마지막 두 단계를 거꾸로 적었다.

기존 수치, 11장의 이력 초기화·입자 손실 공개, 9장의 SBE 단일점 보정 한정, 새 문헌의 주요 한정어는 유지할 수 있다. 13장 Kissel 문헌 요약 한 문장은 P3 교정을 권한다. 수정 후에도 발표물 수용은 모델 검증·런 발사·데이터 배포 승인이 아니다.

**표시 검증 한계:** 제출 PDF 18쪽은 독립 렌더 후 전수 육안 검사했다. PowerPoint 앱이 없어 네이티브 OMML의 실제 표시까지 확인하지는 못했다. 특히 3장은 발표할 컴퓨터에서 한 번 열어야 한다.

## 2. 입력 고정과 확인 범위

| 대상 | SHA256 |
|---|---|
| `seminar_20261013_v32.pptx` | `1b6988f3e55dc6bcf7e81d0ba4ec35b11ed2a0790a1357ba6e6185d22b08f28d` |
| `seminar_20261013_v32.pdf` | `0e8f9a74cbb8ee004af293c4dbec2795f92efd4f540a8135de178ecf833a769e` |
| 제출 ZIP | `9d219c577269e44ce89dd0d2eb00d43a3995d32869d94b15e7997464741e9ca5` |
| v3.1 비교 PPTX | `73fa2dc3b5629eabb9ec744b47495512db477dd962753a003820ad02b525401b` |

- 별도 첨부 PPTX·PDF와 ZIP 내부 사본이 각각 일치한다. ZIP 매니페스트 84건 모두 일치한다.
- 실제 PPTX의 슬라이드 관계표를 따라 본문·notes·수식·이미지를 읽었다. 생성기와 제작자 검사 245/245를 판정 근거로 대신하지 않았다.
- ZIP에 든 `repo/` 파일 전부를 고정 커밋과 대조했고 차이가 없었다. 별도로 확보한 리포 자료는 Git blob SHA를 대조했다.
- 문헌 카드는 별도 정본 브랜치의 조회 시점 커밋 `ebfed0ff5cb3ef81d386ca0575037469a824e3e5`에서 재대조했다. 담당자가 읽은 여섯 사본과 본문이 같으며 차이는 파일 끝 개행 하나뿐이다. 덱 핀과 같은 커밋이라고 주장하지 않는다.
- 새 시뮬레이션, 생산자 코드 실행, 덱 수정, 소스 변경은 하지 않았다. 원로그 읽기·산술·문서 대조만 수행했다.

요청서 §6에 포함됐다고 적은 **원 수식 PPTX `8e76819a…`는 ZIP에 없다.** 따라서 A8의 원본 대비 8/8 XML·그림 동일성은 이번 입력으로 재현하지 못했다. 배포 수식 자체의 의미와 네이티브 수식 8개 존재는 별도로 확인했다. v3.1 비교 기준은 앞선 리뷰의 보존본으로 복구했다. 이 포장 누락만으로 수식을 틀렸다고 판정하지 않는다.

## 3. 수정할 finding

### SEMV32-01 · P2 · 회전식 근사를 구현식으로 표시

**위치:** 실제 3장 출처 줄·② Rotation·notes. 소스 대조 위치는 `docs/seminar_20261013/slide_text_v32.md:44,89`; PPTX 내부 논리적 3장은 `ppt/slides/slide18.xml`이다.

슬라이드는 (R_i\mathbf n_{ij}\times\mathbf F_{t,ij})를 쓰면서 전체 판을 `implemented equations`라고 소개한다. 고정 LIGGGHTS 구형 입자 경로는 `cri = radi - 0.5*deltan`을 만들고 접선력 토크에 곱한다. 따라서 지렛대 크기는 (R_i-\delta_{ij}/2)이다. [고정 surface 소스](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/surface_model_default.h#L173-L188), [토크 적용 소스](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/3d5c00f20519e6bb6eb6756f51f1ad36564e649d/src/tangential_model_history.h#L254-L261).

**검산:** (R_i=0.5\,\mu m), (\delta=0.1\,\mu m), 직교 접선력 (1\,\mu N)이면 구현 토크는 **0.45 µN·µm**, 표시식은 **0.50 µN·µm**로 11.111111% 차이다. 이는 구별용 합성 입력이지 실제 침대 오차의 추정이 아니다. δ/R=0.02로 작아져도 차이는 1.010101%이므로 정확식과 근사식의 구별은 남는다.

**무너지는 것:** 식 ②까지 한 글자 그대로 구현했다는 소개. Newton–Euler 운동방정식의 채택이나 작은 겹침에서 (R_i\mathbf n_{ij})를 쓰는 발표용 근사 자체는 무너지지 않는다. n의 방향이 정의되지 않았으므로 토크 부호까지 틀렸다고 단정하지 않는다.

**최소 수정:** 식을 유지하려면 출처 줄을 다음처럼 바꾼다.

> Representative equations based on LIGGGHTS-PUBLIC 3.8.0 [2]; linear hysteretic law [1]. Equation ② uses the small-overlap approximation ℓᵢⱼ ≈ Rᵢnᵢⱼ.

정확식을 원하면 ②를 `Σ(ℓᵢⱼ × Fₜ,ᵢⱼ + Mᵣ,ᵢⱼ)`로 쓰고, ℓ의 방향 및 구형 입자 경로의 크기 (R_i-\delta_{ij}/2)를 정의한다. `docs/dem_governing_equations_background_20261011.md:103–105`도 이미 구현식과 이 근사를 구분한다.

**해결 증거:** 수정된 실제 PPTX·notes에 이 구별이 함께 있고, 발표 컴퓨터에서 3장의 수식이 잘리지 않는 화면. 수식 의미만 정정한다면 새 DEM 런은 불필요하다.

### SEMV32-02 · P2 · 내부 검사를 외부 타당성으로 읽힐 수 있게 연결

**위치:** 11장 본문 두 번째 문장, `slide_text_v32.md:196`.

`model-internal until the open checks pass`는 검사 통과 뒤에는 model-internal이라는 한정이 해제되는 것처럼 읽힌다. MV-01·02·08의 평형·이력·보존 검사는 모델의 수치 상태와 비교 해석을 자격화한다. **실험과 맞는 모델이라는 증거를 주지는 않는다.** 이전 판정 Q11 역시 조건 충족 뒤에 허용한 것은 해당 침대 끝점을 명목 정적 300 MPa 상태로 해석하는 것까지다 (`codex_review_model_validation_20261008.md:209–215`).

또한 B는 서보 단독 개입이 아니다. 실제 `in.branch_B.liggghts:214–246`은 판·벽 fix를 지워 다시 만들고 감쇠를 1e−5로 바꾼다. 다만 **이 혼입은 현재 화면의 표와 notes에 이미 공개돼 있다.** 이를 숨겼다는 새 P1은 성립하지 않는다.

**최소 교체 문장:**

> At fixed platen, the original run relaxes to 165 MPa. A combined follow-up protocol—plate-contact history reset, lower damping and force hold—reduces thickness from 111.05 to 105.84 µm. This remains a model-internal diagnostic; static-equilibrium and conservation checks are pending.

**무너지는 것:** 열린 검사 몇 개가 닫히면 실험 타당성까지 확보된다는 함의. 관측된 두께 변화와 B의 진단적 가치는 유지된다. 3개 압력 막대를 하나의 연속 궤적으로 말하거나, 두께 감소 전부를 감쇠 제거 효과로 말하면 안 된다.

**해결 증거:** 위 구별이 실제 본문에 있고, 기존 이력 초기화·13 SE 소실 표와 notes가 유지된 수정본.

### SEMV32-03 · P2 · 최신 비준과 다른 언로딩 순서

**위치:** 15장 흐름도의 마지막 두 상자와 notes, `slide_text_v32.md:265–269`.

현재 덱은 **relaxation → platen removal → unloading**이다. 그러나 같은 핀의 계획서 `dem_protocol_gen2_plan_draft_20261014.md:437,454`와 진행 원장 `session_20260923_progress.md:1067`은 저자가 Q1 권고안을 비준한 순서를 **이완 → 언로딩 → 판 분리**로 고정한다. v3.2 반입은 그 뒤의 밤 9 기록이다. 리뷰 이후 최신 HEAD를 들이대는 지적이 아니다.

히스테리시스 접촉에서 판을 먼저 없애는 갑작스러운 해제와, 접촉을 유지하며 하중을 줄인 뒤 분리하는 절차는 같지 않다. 초안의 옛 D2 문장을 최신 결정으로 잘못 가져온 것이다.

**최소 수정:** 흐름도를 아래 순서로, notes도 동일하게 수정한다.

> insertion → stabilization → compression → servo → relaxation → unloading → platen removal

`Heckel analysis redone`도 **`Heckel analysis to be redone`**으로 바꾸면 계획임이 더 분명하다.

**무너지는 것:** 현재 슬라이드가 최신 저자 결정을 정확히 설명한다는 주장. 세대 1 결과, 언로딩 이력 시험 PASS, 키트 HOLD 표지는 영향을 받지 않는다.

**해결 증거:** 실제 15장 상자와 notes가 같은 순서인 수정본. 생성기·글 정본도 함께 맞추되 이번 리뷰는 파일을 직접 고치지 않았다.

### SEMV32-04 · P3 · Kissel 요약에서 응력 횟수의 영향을 배제하는 표현

**위치:** 13장 notes, `slide_text_v32.md:231`.

`coverage followed the stress intensity rather than the number of stress events`는 횟수의 영향이 없다고 읽힌다. 원문 Fig. 6c,d 설명은 같은 stress number에서도 intensity에 따라 피복이 달라지는 한편, 낮은 강도에서 횟수·시간 증가가 피복을 늘리는 효과도 남긴다. [Kissel 원문](https://www.nature.com/articles/s41467-026-71305-2).

교체안:

> Coating coverage depended on stress intensity as well as stress number; increasing stress number alone did not collapse results across rotor speeds.

이는 드럼 결과나 판정을 뒤집는 결함이 아니다. 다른 믹서·재료·응집 없는 coarse-grained DEM이라는 기존 한정은 유지한다.

## 4. Q1–Q8 답

| 질문 | 판정 | 답 |
|---|---|---|
| Q1 · 11장 해석 | **부분** | 복합 개입의 공개는 충분히 보인다. 본문에서도 직접 쓰면 더 명확하다. `until`에 의한 지위 승격은 SEMV32-02대로 수정한다. |
| Q2 · F_p4 | **수용** | 압력·두께·총 입자 수는 원로그·STL에서 맞는다. ε·drag는 저장 분석 출력 및 독립 산술까지 일치한다. 개별 atom 재합산은 자료 부재로 미실시. 등록 띠·빗금은 유지 가능하다. |
| Q3 · 수식 | **부분** | ③ 비포화 가지·④ spring 마찰 및 CDT·⑤ 강성의 주요 구현 대응과 감쇠 값은 맞다. ② 근사 표지 수정, 원 수식 PPTX 부재 및 PowerPoint 표시 미확인이 남는다. |
| Q4 · 9장 | **수용** | 3.41은 기록된 S2 끝점의 로그 보간과 맞는다. 유효값·SBE 한 점·DBE order only/pending 표지가 적절하다. R/Q를 실험 일치나 밴드 합격으로 승격하지 않았다. |
| Q5 · 5장 | **수용** | `planned`와 `no results yet`가 결과 없는 계획임을 구분한다. 같은 핀 진행 기록 :1069에서 대립 SE 1개 추가 승인도 확인된다. notes의 ‘답 대기’는 갱신 권고. 실험 설계 승인과는 별개다. |
| Q6 · 문헌 | **수용, P3 한 문장 권고** | 순수 SE·in-die·공간 분해능·청정 끝 조성·접착 W 아님이라는 핵심 한정이 보존된다. SEMV32-04만 교정 권고. |
| Q7 · 15·16장 | **부분** | 계획/런 없음·이력 PASS/키트 HOLD 구별은 맞다. 15장 단계 순서는 SEMV32-03 수정. 16장 loading 한 줄은 앞 내용을 정확히 요약하므로 유지한다. |
| Q8 · 인용·다리 줄 | **수용** | 실제 사용 인용은 1–13이고 참고문헌에 대응한다. `[0,1]`은 수학적 범위이지 인용 0번이 아니다. 연결 문장 15개에 새 수치 주장이나 필수 차단점은 없다. |

③의 이력식은 k₂ 갱신·포화 알고리즘 전체를 한 식으로 대체하지 않는다. 현 notes가 이를 제한하므로 다시 전체 모델 설명을 요구하지 않는다. ④의 CDT는 **상대 각속도 0에서 토크 0**임을 notes에 보완하면 좋다. 순수 구름 식을 일반 3D 회전에 그대로 확장하지 않은 점은 유지한다.

## 5. 수치 검산과 증거 수준

### 11장 원자료

| 항목 | 독립 대조값 | 확인 수준 |
|---|---:|---|
| B 출발 압력 | 300.90644 MPa | 원 thermo의 정상 적분 행 |
| 원 런 고정판 이완 압력 | 165.34203 MPa | 별도 r8 원로그 |
| B 종료 압력 | 299.27373 MPa | 원 thermo의 정상 적분 행 |
| B 출발 → 종료 두께 | 111.052 → 105.842 µm | 저장 판 STL 좌표 |
| B 총 입자 수 | 160420 → 160407 | 원 thermo |
| 두께 변화 | −5.210 µm, −4.691496% | 위 좌표의 산술 |
| 구 체적합 공극률 | 14.95305959 → 10.76925460% | 저장 `analysis_branch.json`의 부피·상자·판 위치를 재계산 |
| drag/목표 힘 | 434.180477964/750 = 57.8907304% | 저장 분석 합계의 산술 |

같은 step에 존재하는 `run 0`/setup 행의 326.70943·326.05006 MPa를 끝점으로 오독하지 않았다. 정상 적분 행에서 그림의 300.9·299.3이 나온다. 원 고정판 이완 경로의 입자 손실은 3개이고 B는 13개여서, 세 압력 막대는 하나의 끊김 없는 궤적이 아니다. 그림의 `original run`/`branch B` 표지는 중요하다.

57.9%는 **목표 힘에 대한 drag 비**다. 원로그 압력 감소율은 **45.0520135%**여서 같은 수가 아니다. 300 MPa에서 57.9%를 빼 정적 압력을 계산하지 않는다. 750 N의 `deck units` 한정도 삭제하지 않는다. 물리적 50×50 µm 면적에 300 MPa를 곱하면 0.75 N이다.

B 보고 아카이브에는 개별 atom dump가 없다. 그러므로 속도·반지름을 다시 합산한 ε/drag 검증이나 상별 census를 완료했다고 말하지 않는다. 저장 분석 부피 감소는 6.80678408 µm³로 반지름 0.5 µm인 SE 13개의 체적과 맞지만, 이것이 보존 검사를 통과시킨다는 뜻도 아니다.

등록 띠 8.3–11.7%는 결과 전 B2의 **모델 예측 띠**다. 실험 범위·통계 신뢰구간이 아니다. 그림을 더 명확히 하려면 `registered prediction band`로 부른다. 빗금과 열린 검사 표를 유지하는 한, 띠 안에 있다는 사실 자체를 삭제할 필요는 없다. 삽입된 F_p4 이미지의 SHA256도 제출 그림과 일치한다.

### 9장 보간과 비

기록된 S2의 두 점 `(2.618,3.8694)`와 `(3.927,4.8260)`에서 로그 기울기는 **0.5448520884**, SBE 표적 4.47 mS/cm를 지나는 탄소 입력은 **3.4117757749 S/cm**다. 화면의 0.545·3.41은 맞는다. 이는 기록값의 산술 재현이며 원 솔버 재실행은 아니다.

`70.53/34 = 2.07441176`, `59.28/70.53 = 0.84049341`도 2.07·0.84로 반올림된다. R은 등록 상한 2 이내가 아니며, Q는 모델 민감도 예측 충족이지 실험 hit가 아니라는 현재 표 문구를 유지한다. σ_VGCF*는 고유 섬유 물성이 아니라 해당 격자·접촉 미해상도를 흡수한 유효 보정값이다. S3/J1/J2가 미판정인 핀의 상태를 발표 전 새 결과 없이 바꾸지 않는다.

## 6. 문헌과 발표 흐름

| 문헌 | 이번에 허용되는 사용 | 보존할 경계 |
|---|---|---|
| Faka 2026, Fig. S2 | 0.3 GPa에서 상대밀도 약 87→74%, 즉 공극률 약 13–26%라는 그림 판독 | 순수 LPSCl, in-die. 복합 DEM 침대 검증 아님. 소수 첫 자리 디지타이즈값까지 이번 육안 판독으로 인증한 것은 아님 |
| Thompson 2026 | 479 MPa에서 대부분의 입계 공극 닫힘, 1155 MPa에서 분해 가능한 공극 소실; 감압 중 가역/잔류 변화 구분 | 1.277 µm 분해능 맥락, 공극률 0 아님. 감압 하한 ≈1.1–1.8 GPa, 무하중 springback 아님 |
| Hersey 1975 | 미분이 carrier에 붙는 ordered mixing 및 무작위 기준 지수의 한계 | 우리 드럼에서 실현·검증됐다는 증거 아님 |
| Egermann & Orr 1983 | interactive 유형과 σ<σ_R라는 ordered 균질 정도의 용어 구별 | 용어 제안이지 두 현상이 항상 동치라는 법칙 아님 |
| Kissel 2026 | 믹서 강도·응력 횟수의 중요성에 대한 다른 시스템 맥락 | 드럼·cohesion/코팅 기전을 직접 검증하지 않음. SEMV32-04 반영 |
| Kim 2012 | 계산한 끝 조성 청정 슬랩의 모든 비교 면에서 LiNiO₂ 표면 에너지가 더 낮음 | NCM 분말 실측이나 NCM/SE 접촉 W 아님 |

출판사: [Faka](https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/aenm.202505186), [Thompson](https://doi.org/10.1002/adfm.75195), [Hersey](https://doi.org/10.1016/0032-5910(75)80021-0), [Egermann와 Orr](https://doi.org/10.1016/0032-5910(83)80016-3), [Kissel](https://www.nature.com/articles/s41467-026-71305-2), [Kim](https://pubs.rsc.org/en/content/articlelanding/2012/jm/c2jm31145c). 각 문헌의 열람 범위·원문 그림 해시는 `agents/literature.md`에 있다. Hersey 전체 원문 등 이번에 별도 전수 열람하지 않은 부분까지 확인했다고 확장하지 않는다.

요청서의 네 가지 순서 질문에 대한 답은 다음과 같다.

1. **6장의 7:3 접촉망 그림이 설명보다 먼저 나오는 것:** 개요 그림이면 허용된다. 캡션에 `Illustration of the 7:3 bed discussed next`를 붙이면 충분하다. 순서 변경 필수는 아니다.
2. **3장 수식과 4장 Luding 그림의 중복:** 3장은 무엇을 계산하는가, 4장은 무엇을 못 표현하는가로 역할이 달라 유지 가능하다. 4장 notes의 감쇠 설명은 11장의 예고로만 짧게 한다.
3. **7·10장의 300 MPa 한정이 11장에 늦게 등장:** 7장의 원 상태 수치와 10장 notes의 fixed-platen 158–175 MPa가 구분돼 있어 새 수치 오류는 아니다. 첫 언급에 `nominal stopping pressure; see Problem 4`를 붙이면 청중의 잘못된 선이해를 줄인다.
4. **5장의 10%와 15장의 ε_union 10–13%:** 같은 검증 자료가 아니다. 5장은 기존 보정 목표, 15장은 새 프로토콜의 계획된 기하 목표다. 다음 문구를 15장 notes/작은 글에 권한다: `Provisional geometric calibration target; experimental definition and load state still to be matched.` union을 맞추는 것이 질량·밀도·두께 공극률을 맞춘다는 승인은 하지 않는다.

## 7. 승계와 표시 확인

본문·notes 인용 번호를 정규화하고 새 다리 줄만 분리하면 **1·2·4·6·8·18장의 본문, notes, 이미지 해시 모두 v3.1 대응 장과 일치**한다. 모든 대응 장의 기존 이미지 해시도 유지된다. 따라서 이 여섯 장의 기존 과학 내용은 승계할 수 있다. 새 문구가 기존 GO를 자동 승계하는 것은 아니다.

제출 PDF를 다시 렌더한 18쪽에서 필수 문구 잘림·덮임은 발견하지 않았다. 9장은 밀도가 높지만 주요 한정은 화면에 남아 있다. 원래 발표자가 넣도록 비워 둔 그림칸과 첫 장 날짜 placeholder는 이번 변경분의 과학 finding으로 세지 않았다. 발표 직전 실제 날짜와 사용할 그림은 별도로 마무리한다.

PowerPoint가 그리는 OMML과 LibreOffice PDF가 그린 fallback 이미지는 별도 경로다. 실제 수식 8개는 존재하고 literal `\u2003` 같은 잘못된 문자열도 없다. **PDF가 잘 보였다는 것만으로 PowerPoint 식 줄바꿈·잘림까지 합격시키지 않는다.**

## 8. 최소 종결 목록과 재현

- [ ] SEMV32-01: 3장 대표식/근사 표지 또는 정확 지렛대, notes 동기화.
- [ ] SEMV32-02: 11장 `until` 삭제, 내부 진단과 외부 검증 구분. 기존 복합 개입·손실 공개 유지.
- [ ] SEMV32-03: 15장 언로딩→판 분리 순서, notes 동기화.
- [ ] 발표 컴퓨터에서 3장의 PowerPoint 네이티브 수식 8개 표시 확인.
- [ ] 권고: 13장 Kissel 문구, 15장 미래형, 원 수식 PPTX 누락 보완, 5장 대립 SE notes 상태 갱신.

재현 스크립트는 생산자 모듈을 실행하지 않는다. 검산은 `inspect_deck.py`(실제 PPTX/PDF·해시·차이), `final_checks.py`(승계·F_p4 삽입·보간), `agents/equations_probe.py`(OMML·지렛대 반례), `agents/physics_probe.py`(원로그·STL·저장 분석 산술)다. 네트워크 원자료 고정은 `prepare_sources.py`와 `verify_external_sources.py`에 분리했다. 결과는 `evidence/`와 `agents/*probe*.json`에 보존했다.

**HOLD — 발표 전 문구·순서 3곳 수정. 새 P1 없음. 모델 재계산·새 런 요구 없음.**
