# v3.3 문구·notes 종결 대조

2026-10-15. 범위는 실제 PPTX의 3·5·7·11·13·15장 본문과 notes, v3.2 대비 의미 변화다. 생성기·slide_text·제작자 self-test는 합격 증거로 쓰지 않았다. `ppt/presentation.xml` 순서와 relationship을 따라 actual body/notes를 읽었다. 독립 `semantics_probe.ps1 -Check`는 21/21 통과했다. `-Compare`는 실제 이전/현재 문단 차이를 출력한다. 이 probe는 ZIP/XML을 읽기만 하며, 생산자 모듈을 import하거나 덱을 다시 만들지 않는다.

**판정: SEMV32-02·03·04는 의미·notes 범위에서 닫힘. 새 의미상 P1/P2 없음. 3장의 요청 문구도 실제 파일에 있다. 수식의 바이트 동일성·원본 대조, 그림 값·빗금, PDF·발표 PC 표시는 별도 담당 검증 범위다.** 기존에 수용한 수치나 변경하지 않은 과학 내용을 새로운 차단점으로 재분류하지 않았다.

## Q1–Q6

| 질문 | 의미 범위 판정 | 실제 증거와 남은 범위 |
|---|---|---|
| Q1 · 3장 대표식/근사 | 문구 닫힘 | 실제 출처 줄에 `representative equations based on` 및 `Equation ② uses the small-overlap approximation ℓᵢⱼ ≈ Rᵢnᵢⱼ.`. notes는 구현 지렛대 크기 `Rᵢ − δᵢⱼ/2`와 CDT 상대 각속도 0에서 토크 0을 구별한다. 수식 의미·원본 동일성의 별도 검증 및 PowerPoint 표시 확인을 대신하지 않는다. |
| Q2 · 11장 SEMV32-02 | 닫힘 | 요청된 본문 2가 그대로 있고 `until the open checks pass`가 사라졌다. 복합 개입을 본문에서 직접 명시하며 notes는 내부 검사 통과와 실험 검증을 명시적으로 구별한다. contact-history reset 및 13 SE 소실 표/notes와 세 행의 `open` 상태가 보존된다. |
| Q3 · 15장 SEMV32-03 | 닫힘 | 실제 상자는 왼쪽부터 insertion → stabilization → compression → servo → relaxation → unloading → platen removal. notes도 같고 `Heckel analysis to be redone`이 본문·notes에 있다. 기존 계획/무결과 및 unloading-kit HOLD를 바꾸지 않았다. |
| Q4 · 13장 SEMV32-04 | 닫힘 | 요청된 Kissel 문장이 정확히 들어갔다. 실제 v3.2 notes에서 그 문장과 연결 구두점만 치환하면 v3.3 notes와 일치한다. 시스템·믹서·응집 없음·고속에서만 순동력 일치·드럼 비교 아님 등 기존 한정 전부 유지. |
| Q5 · F_p4_v33 과장 여부 | 문구 범위 수용 | 본문의 `registered prediction band`, `hatched = checks still open`와 notes의 결과 전 모델 예측/실험 범위 아님/통계 신뢰구간 아님이 함께 있다. 띠 포함을 실험적 검증 또는 static-equilibrium PASS로 승격하지 않는다. 실제 그림의 값·빗금·축 상한·렌더는 주 검토자 확인 사항. |
| Q6 · 7·11·15장 단어 상한 초과 | 의미상 차단 없음 | 늘어난 내용은 7장의 nominal stopping pressure 한정, 11장의 복합 개입·내부 진단 구별, 15장의 미래형이다. 이 문구를 지우거나 줄여서 숫자 상한을 맞출 근거는 없다. 발표물의 시각적 수용 여부는 실제 PDF/PNG에서 잘림·가독성을 확인한 뒤 결론 낸다. 15장의 provisional 설명을 notes에 둔 것은 요청된 범위이며 새 HOLD 근거가 아니다. |

## 실제 구절

### 11장 — `ppt/slides/slide11.xml`, `ppt/notesSlides/notesSlide14.xml`

본문 2 (105.84 뒤 공백은 실제 U+00A0):

> At fixed platen, the original run relaxes to 165 MPa. A combined follow-up protocol—plate-contact history reset, lower damping and force hold—reduces thickness from 111.05 to 105.84 µm. This remains a model-internal diagnostic; static-equilibrium and conservation checks are pending.

Notes 추가:

> Passing these internal checks would qualify the numerical state of this bed; it would not validate the model against experiment.

보존된 표 행:

> Plate re-created at servo start: contact history reset
>
> Atom-count guard vs. conservation (13 SE particles lost)

세 행 모두 상태 `open`. 보존된 notes:

> (ii) The servo deck re-creates the plate and wall fixes, which also resets the normal plastic contact history, so B is a combined protocol (history reset + damping drop + force hold); the registered follow-up protocol includes a reset of the plate contact history (MV-02). (iii) The atom-count guard does not certify conservation; the 13 lost particles are SE (MV-08).

띠 notes:

> a model prediction registered before the run, not an experimental range or a statistical confidence interval.

**의미:** 원 런의 fixed-platen 이완과 복합 후속 프로토콜을 구별한다. 내부 검사를 통과하면 명목 정적 끝점 해석을 자격화할 수 있다는 기존 notes는 남지만, 바로 다음 문장이 실험 검증으로의 승격을 금한다. 이 둘은 모순이 아니다. 기존 한 침대·한 조성·한 checkpoint 한정, sphere-volume와 exact-union 구별, 원 generation-1 프로토콜 사용 설명도 유지된다.

### 15장 — `ppt/slides/slide15.xml`, `ppt/notesSlides/notesSlide22.xml`

동일 y=4,937,760 EMU에 놓인 실제 흐름 상자의 x 좌표는 다음과 같다.

| 문구 | x (EMU) |
|---|---:|
| insertion | 521207 |
| stabilization | 1700783 |
| compression | 2880359 |
| servo | 4059935 |
| relaxation | 5239512 |
| unloading | 6419088 |
| platen removal | 7598664 |

Notes:

> stages insertion → stabilization → compression → servo (holding the target force) → relaxation → unloading → platen removal (order ratified on 10-14: docs/reviews/dem_protocol_gen2_plan_draft_20261014.md Q1; docs/session_20260923_progress.md, 10-14 night 7 entry)

본문과 notes 모두 `Heckel analysis to be redone`. notes의 provisional 구별:

> ε_union 10–13 %: Provisional geometric calibration target; experimental definition and load state still to be matched. It is a planned geometric target for the new protocol, not the existing 10 % calibration target on the MPM-inputs slide.

**교차 근거:** 이전 핀 원본 `source/docs/reviews/dem_protocol_gen2_plan_draft_20261014.md:437,454`와 `source/docs/session_20260923_progress.md:1067`에서 저자 비준은 이완 → 언로딩 → 판 분리다. 현재 수정은 이 비준을 맞춘다. 기존의 `DEM protocol generation 2 — plan, no runs yet`, notes의 `plan only, no runs and no results`, `history test passed; kit re-review HOLD, fixes ratified`를 보존했다. 따라서 계획을 완료된 계산·검증으로 바꾸지 않았다.

### 13장 — `ppt/slides/slide13.xml`, `ppt/notesSlides/notesSlide20.xml`

Notes 교체:

> Coating coverage depended on stress intensity as well as stress number; increasing stress number alone did not collapse results across rotor speeds.

문장 앞의 `coarse-grained DEM of a high-intensity mixer (one particle species, no cohesion term; simulated net specific power agreed with the experiment at high rotor speed only)`와 뒤의 `This is context for mixer-side process variables, not a comparison with the drum runs.`를 그대로 유지한다. 이전 덱 본문은 완전히 동일하며, notes는 위 단일 문장 치환 이외 동일하다. 기존의 post hoc, one seed, start-state difference, NCM–wall adhesion 동시 변경, 범위 밖 Lacey M, no verdict, 개발/확증 seed 구별도 모두 남는다. 새 문장은 강도의 중요성을 유지하면서 응력 횟수의 영향이 없다는 함의를 제거한다. 이전 종결 권고와 정확히 같은 문구이므로 새 과학적 범위 확장이 없다.

### 5·7장 권고

5장 `notesSlide4.xml`의 바뀐 부분:

> one large-particle LPSCl pellet added to the EIS plan, approved by the author on 10-14; docs/session_20260923_progress.md, 10-14 night 9 entry

이전 핀 진행 원장 1069행의 저자 `대립도 하나 할거야`와 맞는다. 실제 화면 본문은 v3.2와 동일하고 `Lab anchor (planned)` 및 `no results yet`가 남아 있다. 계획 승인 문구를 실험 결과나 검증 완료로 바꾸지 않는다.

7장 `slide7.xml`의 본문 첫 설명:

> Soft-sphere DEM with a linear hysteretic contact law, pressed to 300 MPa (nominal stopping pressure; see Problem 4); one bed per composition, no seed replicates.

이 한 삽입 외 본문과 모든 notes가 v3.2와 같다. `lowest of five` 한정, fixed-platen 165 MPa와 unloaded 구별, 순수 LPSCl/in-die 문헌과 복합 DEM 침대 검증의 구별이 그대로 남는다.

## 범위 경계

- 이전 과학 판정에 대한 의미상 closure audit이다. 새로운 시뮬레이션, 수송·역학 계산, 논문 전체 재검증을 하지 않았다.
- 입력 PPTX/PDF·생산 소스는 수정하지 않았다. 이 notes와 독립 read-only probe만 새로 작성했다.
- 발표물 문구 종결은 모델 검증·프로토콜 실행·194/보충 20/v1.3 배포 승인이 아니다.
- 실제 PowerPoint 앱 표시를 확인했다고 주장하지 않는다. 특히 3장의 OMML 및 유니코드 아래첨자는 주 검토자의 최종 표시 한정에 남겨야 한다.
