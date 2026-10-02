---
title: "Schmidt C.P., Sinzig S., Wall W.A. 2024 — An Electro-Chemo-Mechanic Model Resolving Delamination between Components in Complex Microstructures of Solid-State Batteries (J. Electrochem. Soc. 171, 100502)"
source_url: local-upload/54._An_electro-chemo-mechanic_model_resolving_delamination_between_components_in_complex_microstructures_of_solid-state_batteries.pdf
source_url_note: "본문 PDF 16 쪽(IOP 판 — p. 1 IOP 내려받기 표지 · 논문 지면 p. 2–16 · 꼬리말만 · 쪽 번호 인쇄 0 · PageLabels = PDF 쪽) 2,786,517 B · 업로드 접두사 fde9d5bd · 4차 묶음 파일 54 · 모형 편(3D 전기-화학-역학 · Nitsche 접촉) · SI 없음(원문에 보충 언급 0) · 시뮬레이션 결과 자료 Zenodo 10.5281/zenodo.13802728 (받지 않음) — 자동 크롭 17(그림 1–17 · f11 오탐) + 수동 9(그림 1 전폭 · 그림 11 · 표 I · 표 B·I–B·VI) 전부 봤다 · 그림 7 · 8 · 9 · 12 · 14 · 15 · 17 은 벡터 경로 판독 · 식 · 표는 쪽 렌더 조각으로 확인(판독용 · 커밋 안 함)"
source_doi: 10.1149/1945-7111/ad76dc
source_license: "© 2024 The Author(s). Published on behalf of The Electrochemical Society by IOP Publishing Limited — Creative Commons Attribution 4.0 License(CC BY · 오픈 액세스) — 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures 에 — 변형 없는 잘라내기)"
pdf_sha256: a58e96d8a6e69ee079f6e723072a0828afe5866440a0b70b9da8dc172ebe3957
ingested: 2026-10-02
sha256: c184fa1092ed4280042190c36c7f695c752fb61c405b6bacfc0cc3cfbb6510aa
---
# 수집 목적

`assb` 섹션 **94호** — **4차 묶음 파일 54**(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 요청 14 편 중 넷째 · 2026-10-02 사용자 공급 · 파일 51–64 = 91–104호를 받은 순서대로). 닻은 `questions/assb-contact-loss-vs-lampe.md` — 이 편이 걸리는 축은 **Q1(접촉 손실의 기구 · `θ(N)`)** 과 **Q6(압력)** 이 중심이고, 모형 안에서 "접촉 손실이 만든 용량 결손" 이 `LAM_PE` 와 어떤 관계에 있는지(곱 축퇴 · 3 항 분해)가 둘째, 27호가 걸어 둔 기대(`1−u` 0.07)의 대조가 셋째다.

TU München 계산역학연구소(Wall 그룹) + TUMint.Energy Research 의 **Christoph P. Schmidt · Stephan Sinzig · Wolfgang A. Wall** *J. Electrochem. Soc.* 2024 **모형 편** — 27호(Sinzig · Schmidt · Wall 2024 *JES* 171, 120519 — P2D 유효성 · 전역 민감도)와 같은 연구실 · 같은 코드(4C)의 **앞선 편**이다. 3차원 해상 미세구조(Li 금속 \| β-Li₃PS₄ \| NMC622)에 전하 · 질량 · 운동량 보존을 단일체로 풀고, 활물질-전해질 계면 일부를 "**mesh tying**"(늘 붙어 있음 · Lagrange 승수) 대신 "**contact**"(Nitsche 법으로 비침투 · 무접착 · 무마찰 접촉 제약 — 틈이 열리면 그 면의 Butler–Volmer 플럭스를 0 으로)로 바꿔, **같은 입력에서 두 계면 법칙의 차를 "박리 효과"** 로 읽는다. 검증은 패치 시험 · 질량 보존 둘이고, 결과는 단순 기하(입자 하나 · 예압 50 / 60 / 70 MPa · 0.1 C 첫 충전)와 복잡 미세구조(입자 79 · 70 MPa · 방전 상태 조립 → 0.5 C 첫 충전 / 충전 상태 조립 → 0.5 C 첫 방전)다. **1차 실험 0 · 열화(사이클) 0**.

들어온 경로: 원장 행(도착 표시 전 원문 그대로) "| ★★★ | **Schmidt·Sinzig·Wall 2024** — *J. Electrochem. Soc.* **171**, 100502 | 27 | 1 | **Q1** | resolved 모델의 **박리 = 접촉 손실 기구**. 27호가 재 보인 **P2D 대비 상수 오프셋 0.07 이 바로 비연결 입자 몫 `1−u`** 였다 — 그 기구의 모델 원전 |". 위키 grep(`100502` · `Schmidt 2024` · `Schmidt, Sinzig` · `Schmidt·Sinzig` · `delamination`): **27호**(Sinzig 2024 — [18] · 후속 표 :381 ★★★ "같은 그룹의 구성요소 사이 박리(delamination) 확장 — resolved 모델에서 접촉 손실을 기구로 넣은 편 | Q1") · 카드 :5052(27호 Status Log "3순위") · `log.md` :2103(27호 항 "★★★ 3") · 93호 digest(4차 묶음 13 편과의 관계 문장 — 지목 아님). **지목은 27호 후속 절 하나 — 원장 "27 \| 1" 과 일치.** 이 편은 우리 digest 셋을 인용한다(4 · 23 · 75호 — §인용 대조) · 4차 묶음 다른 13 편 중에서는 **파일 57 Koerver 2018 *EES*** 하나([26]).

이 digest 의 일 (지시):

1. **(a) 박리 · 재접촉 기준** — 무엇이 박리를 일으키고(인장 · 접착 0 · 문턱) 무엇이 재접촉시키는가(Nitsche 접촉 · 벌칙 매개변수 — 부록 A) · 비가역인가 가역인가 — [[assb-pressure-reapplication-separation-test]] 의 판정 틀에 넣는다.
2. **(b) 스택 압력** — 값 · 경계조건(정하중 · 정변위) · 시간 이력 · "increased mechanical stack pressure during cycling mitigates delamination" 의 범위와 근거(모의 몇 개) — 원장 §3-b (캐)(해)(태) 표본인가.
3. **(c) 전기화학 결과의 귀속** — 박리 → 내부 저항 ↑ · 전달 전하 ↓ 의 경로를 카드 Q1 `θ(N)` ↔ `LAM_PE` 곱 축퇴에 대응 · 모형 안에서 접촉 손실과 활물질 손실이 구분되는가.
4. **(d) 27호 `1−u` 대조** — 27호가 걸어 둔 기대(상수 오프셋 0.07)를 이 편이 확인하는가.
5. **(e) 매개변수 표 B·I–B·IV 의 출처 층위** · 검증(패치 시험) ↔ 실험 대조(validation) 유무 · Q4 어휘 전수.
6. **(f) 후속 후보** — 접촉 역학 · 박리 실측 · 압력 되돌림(지목 수는 각 digest 후속 절 grep 값만 · 4차 묶음 13 편은 "4차 묶음 파일 NN").

⚠ **표기 규약**: `[인쇄]` = 원문이 실제로 쓴 것 · `[도표]` = 그림을 눈으로 읽은 값(판독 폭 표시) · **`[도표·벡터]`** = 그림의 벡터 경로 좌표를 축 상자로 보정해 읽은 값(곡선 외곽선의 중앙 · 판독 폭 ≈±0.2 %p SoC · ±2 mV · ±0.3 %p 면적 몫) · `[재현]` = 원문 수치 · 식으로 우리가 다시 계산 · `[재현·가정]` = 가정이 붙은 재현(가정을 같이 적는다) · `[해석]` = 우리 해석 · **"(N호 digest 전사)"** = 이 편이 인용한 원 논문을 이 세션에서 다시 열지 않고 우리 위키 digest 에 전사된 값으로 대조한 것. **`[데이터]` 0** — 시뮬레이션 결과 자료(Zenodo `10.5281/zenodo.13802728`)는 받지 않았다(지시 · 이 환경에서 시도하지 않음). ⚠ 이 편의 **측정 · 인용 · 모형 값 구분**: 이 편 안의 수치는 **모형 출력(계산)** 이거나 **입력으로 쓴 인용 값**이다 — 이 편의 측정은 0 이다. 모형 출력은 "측정 값" 과 섞지 않고, 입력의 층위(측정 원자료 · 제일원리 · 남의 모형 입력 · 가정)는 §(e) 표로 가른다.

⚠ **쪽 표기**: IOP 판 16 쪽 — **p. 1 = IOP 내려받기 표지**(인쇄 지면 아님), 논문 지면은 p. 2–16(꼬리말 "Journal of The Electrochemical Society, 2024 171 100502" · 쪽 번호 인쇄 0 · PageLabels = PDF 쪽 1–16). 이 digest 는 PDF 쪽 "p. 8" 로 적는다.

---

# 판정 먼저

1. ★★★★ **(a) 박리는 '문턱' 이 아니라 Hertz–Signorini–Moreau 조건이 열고 닫는다 — 접착 0 · 마찰 0 · 손상 변수 0 · 탄성 SE 라서 구성상 완전 가역이다.** `[인쇄]` 식 (17) "g_n ⩾ 0, p_n ⩽ 0, g_n p_n = 0" · "As we do not account for adhesion in this work, the normal contact traction can only originate from compressive forces, i.e. p_n ⩽ 0. Without friction effects, the tangential contact traction has to vanish" · 전기화학 결합은 식 (27) 하나: "charge and mass are only transferred if the bodies are in contact, i.e. the normal contact traction is negative p_n < 0 … the interface kinetics is set to zero if the bodies have separated" → `j F = i = { i if p_n < 0 ; 0 else }`. 곧 **인장 강도 0 — 계면 수직 응력이 압축이 아니게 되는 순간 틈이 열리고, 틈이 닫혀 압축이 서는 순간 BV 플럭스가 그대로 돌아온다**(이력 · 손상 · 접착 기억 0). Nitsche 벌칙(`γ_n,e = C_u,e γ_n,0` — 요소별 국소 고유값 · 조화 가중 `ω_s` · `θ = 0` 비대칭판 · 부록 A)은 제약을 거는 **수치 장치**이지 물리 문턱이 아니고, 기준값 `γ_n,0` 은 **인쇄 0**(G2). 결과에서 재접촉은 **본문 0** — 초록 · 서론 · 모형 정의 · 결과 머리 · 요약의 `recontact*` 6 회가 전부 틀 문장이고, 계산된 장면은 그림 9 벡터의 한 곳뿐이다(70 MPa 곡선이 SoC 93.5 → 94.5 % 에서 89.6 → 87.7 % 로 ≈1.9 %p 내려감 `[도표·벡터]` · 본문 무언급). 분리 시험 틀(`Q_apparent = θ_AM · η(i) · Q_material`)에 넣으면 이 모형의 박리는 **`θ_AM`(통째 고립)이 아니라 표면 피복 `φ` 의 손실**이고, 그 손실은 **`η(i)` 항으로** 나타난다(③) — 압력을 높이면 `φ` 가 되돌아오는 **기억 없는 이상화된 끝**이다(39호 구조 기억 · 5호 이력 · 14호 +0.4 mV 와 반대 쪽 · 23호 50 사이클 방전 상태 SEM "similar morphology" 의 틈 지속도 이 법칙으로는 못 낸다 — 23호 digest 전사).
2. ★★★★ **(b) '스택 압력 50 / 60 / 70 MPa' 는 t = 0 예압이다 — 경계는 정하중도 정변위도 아닌 Robin 스프링이고, 사이클 중 압력 이력은 인쇄되지 않는다.** `[인쇄]` 식 (36) `(F·S)·N = k(u·N − u_k)N` on Γ_k · "a displacement offset in the normal direction u_k enabling the application of a defined mechanical stack pressure during cycling" · 표 B·I `k = 1.0·10¹³ kg m⁻² s⁻²`(= 10 MPa µm⁻¹) 출처 "**assumed**" · 표 B·VI `u_k,target` 5.041 / 6.049 / 7.057 µm(단순) · 7.102 · 7.133 µm(복잡 방전 · 충전 조립) · 식 (B·6) 코사인 램프 250 s/Ĉ. `[재현]` `k·u_k` = 50.41 / 60.49 / 70.57 / 71.02 / 71.33 MPa → 남는 0.041–0.133 µm 가 예압에서의 셀 압축 → 유효 구속 탄성률 30.5–38.4 GPa — 표 B·I 탄성률을 직렬로 묶은 Reuss–Voigt 범위(28.8–32.5 · 34.7–46.0 · 29.6–36.5 GPa) 안 ✅. 그런데 **같은 k 로 셀 두께 변화를 받으면**(`[재현·가정]` 양극 쪽 경계 정변위 · 측면 대칭 · Li 석출이 두께 방향 · 미보고) 반 사이클 동안 **+13 MPa(단순 0.1 C 충전) · +53 MPa(복잡 방전 조립 0.5 C 충전) · −58 MPa(복잡 충전 조립 0.5 C 방전)** 움직인다 — 예압과 같은 자릿수. 초록 "**increased mechanical stack pressure during cycling mitigates delamination tendencies**" 의 근거 = **단순 기하(입자 하나 · 요소 7,105) × 0.1 C × 첫 충전 × 예압 세 점** — 박리 시작 SoC 13.2 → 14.9 → 16.4 % · 끝 박리 몫 97.1 → 90.5 → 87.8 % · 4.2 V 도달 87.18 → 91.26 → 94.81 % `[도표·벡터]`(세 점 단조) · 복잡 미세구조는 70 MPa 한 점 · "during cycling" = 반 사이클 하나. 그리고 경계의 70 MPa 압축 아래에서도 **CAM\|SE 계면의 80 %(복잡 · mesh tying 인장 몫 — 그림 14) · 93 %(단순 — 그림 9 점선)가 인장**이다 ⇒ **(캐)(태) 강한 표본(모형 판)** — 모형에서도 "압력" 은 명목(예압 목표) ↔ 출력(반력 이력)을 갈라야 하고, 경계 압력 ≠ 계면 접촉 압력이다.
3. ★★★★ **(c) 박리가 만든 '전달 전하 감소' 는 활물질 손실도 통째 고립도 아니라, 남은 접촉 자리로 전류가 몰려 입자 안에 Li 가 남는 율 · 컷오프 의존 결손(η 형)이다 — 같은 곡선을 용량 축척으로 적합하면 `LAM_PE` 자리로 간다.** `[인쇄]` 사슬 "the delaminated parts of the interface do not take part in the charge transfer anymore. Consequently, the current at the remaining, not delaminated interface area increases. This effect leads to a rising internal resistance of the cell, and the cutoff voltage is reached earlier." `[재현·가정]` 크기를 나누면: 남은 면적의 BV 과전압은 끝에서 ≈6 mV(70 MPa · 87.8 % 박리 · 국소 i ≈1.1 A m⁻² · i₀ 4.98) 인데 같은 SoC 의 전압 차(contact 70 − mesh tying)는 90 % 에서 ≈24 mV · 94 % 에서 ≈46 mV `[도표·벡터]` — 나머지는 **입자 안 농도 분극**이다: 그림 10f 색 막대 21,380–22,930 mol m⁻³ = χ 0.406–0.436 → OCV 4.201 ↔ 4.135 V(67 mV) — 컷오프는 **접촉 자리 표면이 OCV 4.2 V 점(χ 0.4065 `[재현]`)에 닿을 때** 오고, 그때 입자 평균 χ 0.434 와의 차 `(0.434 − 0.406)/0.596 = 4.8 % SoC` 가 **mesh tying 대비 결손 4.5 %p(99.4 → 94.9 %)와 같다**. ⇒ 모형 안에는 **LAM 기구가 0**(재료 손실 · 균열 · 상전이 0)이고 접촉 손실은 부분 표면 `φ` 하나뿐이다 — 원인은 구성상 안다(두 계면 법칙의 차). 그러나 **지면의 관측(0.1 C · 0.5 C 전압 곡선 · 고정 컷오프)만으로는** 결손이 η 형인지 용량형인지 갈리지 않는다: 율 스윕 · 휴지 · CV 유지 계산 **0**(G6). 카드 물음의 forward 표본(조건: 유한 율 · 고정 컷오프 · 첫 충전).
4. ★★★★ **(d) 27호 `1−u` 0.07 — 확인하지 않는다. 이 편은 그 기구의 원전이 아니라 다른 기구(이온 계면 박리 `φ`)의 원전이다.** 27호(Sinzig 2024)의 `u = 0.93` 은 생성 미세구조에서 **집전체에 전자적으로 연결된 입자 몫**(정적 · 기하 분석)이고 Sinzig 2024 에는 **접촉 정식화 자체가 없다**(`contact` 0 회 — 27호 digest 전사). 이 편의 박리는 CAM\|SE **이온 계면**의 동적 · 부분 · 가역 박리이고, 전자 연결 · 이용률 · 고립 입자 분석은 **0**(`connect*` · `utiliz*` · `percolat*` · `inactive` 0 · `isolat*` 1 = 남의 단일 입자 모형 [23]). 꼴도 다르다 — 27호 = SOC 바닥 **상수 7 %** · 이 편 = **율 · 압력 · 조립 상태 의존 결손**(0.1 C · 70 MPa 4.5 %p · 0.5 C 복잡 3.1 %p · 충전 상태 조립 방전 0.2 %p). 두 편은 같은 코드 · 같은 그룹인데 역학 경계도 다르다(27호 틀 강성 500 MPa mm⁻¹ = 5×10¹¹ Pa m⁻¹ · 예압 0 ↔ 이 편 10¹³ Pa m⁻¹ · 50–70 MPa — 27호 digest 전사). ⇒ 원장 행 "그 기구의 모델 원전" 은 **전자 비연결 `u` ↔ 이온 계면 박리 `φ`** 두 기구를 한 이름("접촉 손실")으로 묶은 기대였다 — 27호 후속 표의 문구("resolved 모델에서 접촉 손실을 기구로 넣은 편")는 맞다.
5. ★★★ **(e) 매개변수 표의 출처 열은 층위 넷을 섞고, 결론을 좌우하는 입력이 제일원리 · 가정 쪽에 있다 · 검증은 verification 둘(패치 시험 · 질량 보존)이고 실험 대조(validation)는 0 이다.** 표 B·I–B·VI 출처 열 = 문헌 번호 · "averaged from 25" · "adapted from 25" · "assumed" — ① **제일원리 계산값**(β-LPS E 28.9 GPa · ν 0.27 ← [58] Yang 2016 · NMC622 E 175 GPa ← [54] Sun & Zhao 2017 — 둘 다 제목 기준) ② **남의 모형 편 입력의 평균 · 조정**(σ · D · i₀ · κ · c_max · 초기 농도 ← [25] Neumann 2020 — 그 편도 모형 편) ③ **가정**(k · χ0% 1.0 · χ100% 0.404 · t_el 1) ④ 측정 원자료는 Koerver 2018 부피 곡선[26](자료 χ 0.22–0.91 · 운용 창 0.404–1.0 — 위쪽 0.91–1.0 외삽 ≈+0.05 % `[재현]`) · Kremer OCV 함수[61] · CRC 밀도[60]뿐. 같은 목록의 **측정 탄성률 원전 [59] Sakuda 2013(황화물 18–25 GPa — 62호 digest 전사)은 밀도에만** 쓰였다. `[재현]` 재풀이 폐합: 패치 시험(표 I) ✅(η −24.7 mV · Φ 0.7737 / 0.8717 / 1.0490 V · σ_xx −0.552 Pa — 그림 4 · 5 와 일치) · 표 B·VI ✅(Reuss–Voigt) · **질량 수지(그림 7) ❌ 표 B·V 로는 안 닫힘** — 양극 초기 농도 2.10×10⁴(= χ 0.405 · 충전 상태)이면 AM 88 % · c_max·χ0%(5.19×10⁴)여야 36 % ✅(D1). 어휘(NFKC 전후): `identifiab*` · `uniqu*` · `uncertain*` · `sensitiv*` · `calibrat*` · `degenera*` · `validat*` **0** · `fit*` 0 → **2**(NFKC — 부피 다항식) · `verif*` 6 → 12 ⇒ **Q4 0/94 — 여든여섯 번째 성질**(§(e) 3).
6. **(f) 채움표** — Q1 층 하나(모형 출력 박리 몫 `φ_del(SoC; P)` — 단순 기하만 · 복잡 기하 contact 박리 몫 인쇄 0 · `θ(N)` 0/94 — 반 사이클 하나 · 이력 없는 법칙) · Q2 없다(1차 측정 0 — 계면 법칙 쌍은 모형 안 대조) · Q3 층 하나(출처 층위 넷 · 표 B·V ↔ 그림 7 불일치) · **Q4 0/94 — 여든여섯 번째 성질** · Q5 해당 없음(Li 금속 · Φ₀ = 0 · 기준극 0) · Q6 보고(예압 셋 · 스프링 'assumed' · 이력 0) · Q7 해당 없음(Li 석출 · 탈리 미해상 — 균질 성장) · Q8 층 하나(NMC622 OCV = 문헌 함수 · 부피 법칙 = 문헌 자료의 7차 적합 · 외삽 구간). **누적 ≈20.0 → ≈20.0 (새 칸 0).**
7. **(f) 후속** — ★★★ [13] Tian & Qi 2017 *JES* 164, E3512(**재지목 12 · 81 · 94 = 3** — 1D Newman 의 현상론 접촉 면적 손실 = `A_eff` 곱 자리의 원전) · ★★★ [16] **Shao, Liu, Shao, Sang, Chen 2022 *Energy* 239, 121929**(**지목 누락 보충 · 12 · 94 = 2** — 12호 후속 ★★★ 2 인데 원장 행 0 · 원장의 Shao 행(파일 63 · *JES* 169, 080529)과 다른 편) · ★★★★ [20] Barai 2021(**재지목 → 4**) · ★★★ [25] Neumann 2020(**재지목 → 5** — 입력 원전 + "박리 면을 역학과 무관한 입력으로") · ★★★ [12] **Liu B. … Bruce 2023 *SusMat* 3, 721**(새 — 부피 변화 · 스택 압력 → 양극 실험) · ★★★ [10] Jung S.H. 2019/2020(**재지목 → 3**) · ★★★ [26] Koerver 2018 *EES* = **4차 묶음 파일 57**(재지목 → 13) · ★★ [35] Schmidt 2023 *CMAME*(새 — 본체 모형 원전) · ★★ [23] Zhang T. · Kamlah · McMeeking 2024 *JMPS*(새 — 비가역 박리 + SE 균열) · ★★ [34] Naik 2023 *ESM*(새) · ★★ [21] Bistri 2021(재지목 → 2) · ★★ [59] Sakuda 2013(재지목 → 3) · ★★ [30] Wang & Sakamoto 2018(재지목 → 3) · ★★ [8] Hänsel & Kundu 2021(새) · ★★ [5] Kasemchainan 2019(재지목 → 4) · ★ [61] Kremer(재지목 → 3) · ★ [27] Ganser 2019 · [28] Singer 2023 · [58] Yang 2016 · [24] Huang 2023 · [22] Farzanian 2023(새). 지목 누락 둘: **Shao 2022 *Energy***(12호 ★★★ 2 — 이 편이 재지목) · **Lewis 2021 *Nat. Mater.* 20, 503**(14호 ★ · 19호 ★★ — 원장 행 0 · 이 편은 서론 목록 인용이라 재지목 안 함).

---

# 서지

| 항목 | 값 (`[인쇄]` — p. 2 · p. 13 · XMP) |
|---|---|
| 제목 | **"An Electro-Chemo-Mechanic Model Resolving Delamination between Components in Complex Microstructures of Solid-State Batteries"** |
| 저자 · 소속 | **Christoph P. Schmidt**¹,\*,ᶻ · **Stephan Sinzig**¹,²,\* · **Wolfgang A. Wall**¹,² — ¹ TUM School of Engineering and Design, Department of Engineering Physics and Computation, Institute for Computational Mechanics, Technical University of Munich (Garching) · ² TUMint.Energy Research GmbH (Garching) · \* Electrochemical Society Student Member · ᶻ 교신 Schmidt(메일 인쇄) · ORCID 셋 인쇄 |
| 저널 | *Journal of The Electrochemical Society* **171**(10), **100502** (2024) · doi `10.1149/1945-7111/ad76dc` · XMP `prism:number` 10 · 연구 논문(모형) |
| 일정 | Manuscript submitted **May 8, 2024** · revised manuscript received **July 31, 2024** · Published **October 4, 2024**(XMP `crossmark:MajorVersionDate` 2024-10-04 ✅) · `[재현]` 투고 → 수정 84 일 · 수정 → 게재 65 일 |
| 라이선스 | `[인쇄]` "© 2024 The Author(s). Published on behalf of The Electrochemical Society by IOP Publishing Limited. This is an open access article distributed under the terms of the **Creative Commons Attribution 4.0 License (CC BY)**" — 이 digest 는 인용 · 요약 · 재현 계산만 담고, 그림 크롭은 위키 관례대로 `raw/figures/` 에(변형 없는 잘라내기) |
| 자금 | 바이에른 경제부(프로젝트 "Industrialisierbarkeit von Festkörperelektrolytzellen") · BMBF **FestBatt 1(03XP0174D) · FestBatt 2(03XP0435B)** — 27호와 같은 묶음(27호 digest 전사: 바이에른 + FestBatt 2) |
| 코드 · 자료 | `[인쇄]` "All presented simulations are performed using our inhouse multi-physics research code **4C**.[45]" · 격자 **Coreform Cubit 2021.3**[47] · Data Availability "**The result data of the simulations is made available via the Zenodo record 10.5281/zenodo.13802728.**"(결과 자료 — 입력 · 코드 여부 미기재 · 받지 않음) |
| 키워드(정보 사전) | solid-state battery; theory and modelling; delamination; resolved microstructures; recontacting; electro-chemo-mechanics |
| 분량 | 16 쪽(p. 1 IOP 표지 · 본문 p. 2–13 · 부록 A · B p. 13–15 · 참고문헌 p. 15–16) · 그림 **17**(래스터 7 — 3 · 5 · 6 · 10 · 11 · 13 · 16 · 벡터 10) · 표 **7**(I · B·I–B·VI) · 번호 식 **47 + A·1–A·5 + B·1–B·7** · 참고문헌 번호 **1–61 · 인쇄 59 — 18 · 51 번이 목록에 없다**(17 → 19 · 50 → 52 — 렌더로 확인 · 본문은 "Refs. 14–19" · "Ref. 51" 로 부른다 — D8) |
| 절 | 초록 · 서론(무제) · Problem Definition(Geometric definitions · Bulk equations · Interface equations — 운동량 · 전하 · 질량 · Boundary conditions · Initial conditions) · Aspects of The Numerical Model · Results(Verification — 패치 시험 · 질량 보존 / Influence of different mechanical stack pressures / Investigations on complex microstructures — 방전 상태 조립 충전 · 충전 상태 조립 방전) · Summary · Acknowledgments · Data Availability · Appendix A(Nitsche 매개변수) · Appendix B(모형 매개변수 · 표 B·I–B·VI) |

**PDF 메타데이터 (직접 읽음 · pymupdf)**: 2,786,517 B · sha256 `a58e96d8a6e69ee079f6e723072a0828afe5866440a0b70b9da8dc172ebe3957`(호출자 명시값 ✅ — 직접 재계산) · `PDF 1.7` · 16 쪽(p. 1 595 × 842 pt · p. 2–16 585 × 783 pt) · 정보 사전: title **"An Electro-Chemo-Mechanic Model Resolving Delamination between Components in Complex Microstructures of Solid-State Batteries"**(전문 — 호출자 메모의 "…Batt" 는 줄임 표시) · author **"Christoph P. Schmidt"** · subject **"Journal of The Electrochemical Society, 171(2024) 100502. doi:10.1149/1945-7111/ad76dc"** · keywords 위 여섯 · creator **"IOPP"** · producer **"iText® 5.5.13.5 ©2000-2026 iText Group NV (IOP Publishing Ltd; licensed version)"** · 생성 **D:20241003194206+05'30'**(2024-10-03 — 게재 하루 전 조판) · 수정 **D:20261002134342+01'00'**(내려받은 날 — 표지 "downloaded … on 02/10/2026 at 13:43" 과 같음 · IP 는 옮기지 않음) · 암호 0 · XMP **5,942 B**(`dc:creator` 셋 · `prism:volume` 171 · `prism:number` 10 · `prism:pageRange` 100502 · `jav:journal_article_version` **VoR** · `pdfx:robots` noindex · crossmark 2024-10-04 · 도메인 iop.org · `xmp:CreateDate` 2024-10-03T19:42:06+05:30 · `ModifyDate` 2026-10-02T13:43:42+01:00) · **PageLabels**: 1 부터 십진(PDF 쪽 = 표지 1) · 래스터 **12**(p. 1 IOP 로고 700 × 166 · 광고 1640 × 1061 / p. 7 그림 3 482 × 631 / p. 8 그림 5 1821 × 654 · 그림 6 1001 × 367 / p. 9 그림 10 1821 × 1547 / p. 10 그림 11 1336 × 582 / p. 11 그림 13 네 패널 ≈1121–1125 × 958–965 / p. 12 그림 16 1810 × 748) · 그림 1 · 2 · 4 · 7 · 8 · 9 · 12 · 14 · 15 · 17 은 **벡터**(글자까지 외곽선 — 텍스트 층에 눈금 숫자 0).

⚠ **텍스트 층**: 식(1–47 · A · B)은 수식 글꼴 조각이 흩어져 **텍스트로 못 읽는다** — 식 · 표 B·I–B·III 은 **쪽 렌더 조각으로 읽었다**(150–190 dpi · 판독용 · 커밋 안 함). 합자 `ﬁ` 83 · `ﬂ` 25(본문) — NFKC 가 `fit*` 0 → 2 · `verif*` 6 → 12 · `finite element` 0 → 5 를 바꾼다(어휘 집계에 두 열). 꼬리말 15 줄(p. 2–16) 제외 · p. 1 표지 제외. 그림 안 글자는 외곽선이라 셈에 없다 — **그림 10 · 13 · 16 의 "4.2 V ≈ 99.4 % / 94.9 % / 92.5 % / 89.4 % SoC" · "2.8 V ≈ 1.7 / 1.9 % SoC" 표지는 래스터 그림 안에만** 있다(92.5 · 89.4 · 1.7 · 1.9 는 본문에도 있음 · 99.4 · 94.9 는 그림에만).

---

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **단순 기하의 측면 치수 · 대칭 자름 방식 · 입자 자리** — 표 B·IV "lateral dimensions" 칸이 **"—"**(복잡 기하만 50.0 µm) · 그림 6 은 원근 그림 하나 | 단순 기하 결과(그림 7–10 · 압력 세 점 — 초록 압력 명제의 근거 전부)가 지면만으로 재구성되지 않는다. `[재현·가정]` 그림 7 벡터로 측면 단면적 ≈18.0 µm² · AM ≈64.0 µm³(지름 10 µm 구의 ≈0.122)까지 |
| **G2** | **Nitsche 기준 벌칙 `γ_n,0` 값 · 시간 간격("the choice of the time step is based on the C-rate") · 비선형 허용 오차** — 인쇄 0 | 접촉 판정(p_n < 0)과 박리 면적 몫이 벌칙 · 시간 간격에 걸린다(벌칙은 침투 허용 폭을 정한다) |
| **G3** | **격자 수렴** — 단순 기하 사면체 요소 7,105 · 절점 1,832 · 그림 9 곡선이 계단 모양(요소 면 단위로 접촉 상태가 바뀜) · 복잡 기하 524,737 요소 — 접촉 면적 몫의 격자 의존 연구 0(시간 수렴은 [35] 인용 "the error decreases as the time discretization is refined") | 박리 시작 SoC 13.2–16.4 % · 끝 몫 87.8–97.1 % 의 차(압력 효과)가 격자 해상도보다 큰가 |
| **G4** | **사이클 중 스택 압력(스프링 반력) 이력** — 인쇄 0 | `[재현·가정]` 같은 k 로 +13 / +53 / −58 MPa(§(b) 2) — "70 MPa" 가 결과를 대표하는 값인지 |
| **G5** | **복잡 기하 contact 모의의 박리 면적 몫** — 인쇄 0(그림 14 는 **mesh tying** 모의의 인장 면적 몫 사후 처리) | 복잡 기하에서 실제로 몇 % 가 박리됐는지 · 통째로 접촉을 잃은 입자가 있는지(그림 13 b · d 의 둘레 흰 테 입자 하나) |
| **G6** | **율 스윕 · 휴지 · CV 유지** — 0 | 결손(4.5 %p · 3.1 %p)이 η 형(입자 안 남은 Li — 회수 가능)인지 확인하는 계산. `[재현·가정]` 은 η 형을 가리킨다(§(c)) |
| **G7** | **C-rate 의 기준 용량 · SoC 정의식** — 인쇄 0(표 B·II χ0% · χ100% "assumed" 만) | `[재현]` 그림 7 양극 선 기울기가 χ 1.0 → 0.404 창 정의와 1.3 % 안에서 맞는다 — `[재현·가정]` 면용량 0.295(단순) · 1.260 mAh cm⁻²(복잡) |
| **G8** | **전자 연결** — 79 입자 중 집전체 · 서로에 전자적으로 닿지 않은 입자가 있는지 · 입자 겹침 규칙 · 생성 방법(log-normal 매개변수 외) — 인쇄 0 | (d) — 27호 `u` 쪽 기구가 이 모형에 있는지 없는지 |
| **G9** | **Ref. 26 의 "1 mV/100 MPa" 측정 조건 · 부피 자료의 층위(격자 ↔ 입자)** | 4차 묶음 파일 57(Koerver 2018 *EES*) 흡수 때 확인 — 원장 §3-b (노) |
| **G10** | **참고문헌 18 · 51 번** — 목록에 없다 | 본문 "Refs. 14–19"(Li 음극 void 2D 모형 목록) · "Dolbow and Harari show in Ref. 51"(국소 벌칙의 안정성 근거) |
| G11 | **[22] 의 저널명** — 인쇄 "*Materials*, 6, 9615 (2023)" | 권 6 · 쪽 9615 가 *Materials* 와 맞지 않아 보임 — 원전에서 확인 필요(추측으로 고치지 않는다) |
| G12 | **Zenodo 결과 자료의 내용** — 전압 · 박리 몫 · 반력 시계열이 들어 있는지 | 받으면 G4 · G5 를 닫을 수 있다(받지 않음) |
| G13 | **표 B·II i₀ 의 "exchange current density factor"** — 식 (25) 는 상수 i₀(농도 비의존) | "factor" 가 농도 의존 i₀ 의 앞 인자를 뜻하는지 · 상수인지(27호 digest 전사: 같은 코드 계열에서 "i₀ 상수 · 농도 비의존") |
| G14 | **방전 상태 조립 셀의 다음 방전** — 첫 충전만 계산 | 재팽창 → 재접촉(구성상 가역)이 실제로 전부 되돌아오는지 — 제목 · 키워드의 "recontacting" 을 보일 유일한 계산 |

---

# 보충 자료 — 받은 것 · 대조

**SI 없음 (원문에 보충 언급 0).** 호출자 대조와 같은 결과를 직접 다시 셌다 — 본문 · 캡션 · 표 · 참고문헌 전문(NFKC 전후)에서 `supplement*` · `supporting information` · `video` · `movie` · `github` **0 회**, `appendix` 4 회 = 본문 안 부록 A · B 지시, `data availab*` 1 회 = 결과 자료 진술("The result data of the simulations is made available via the Zenodo record 10.5281/zenodo.13802728"), `zenodo` 2 회(같은 문장). 원자료 예치 = **Zenodo 결과 자료**(받지 않음 — 지시) · 코드 = 사내 4C(공개 URL 인쇄 "https://www.4c-multiphysics.org" — 27호와 같음). 그래서 이 digest 의 재현은 **인쇄 수치 · 식 + 쪽 렌더 + 그림 벡터 경로 + 우리 digest 전사** 네 층뿐이다.

---

# 그림 · 표 — 자동 17 항목 + 수동 9, 실제로 연 것 **26/26**

크로퍼(`wiki/tools/extract_figures.py`)가 그림 1–17 을 `fig_1 … fig_17` 로 잡았다(SI 오판 0 — 파일명 `54._An_electro-chemo-mechanic_model_…` 의 `SI_TAG` False 를 첫 실행 전에 확인 · 실행 뒤 이름을 눈으로 확인). **표 7 개(I · B·I–B·VI)는 하나도 못 잡았다**(표 캡션 미인식 — "Table B·I" 의 가운뎃점 형식 포함). 자동 크롭 점검(`figures.json` `note` 에 적음 — 자동 파일은 지우지 않았다):

- **fig_1 오른쪽 잘림** — 벡터 그림은 x 547.5 pt 까지인데 bbox 오른쪽이 537.8 pt → 오른쪽 경계 이름표 Γc(빨강) · Γel(파랑)이 "Γ" 일부만 남음 → **수동 `fig_1_manual_p3.png`**(전폭 재크롭).
- **fig_4 과대 + 캡션 필드 오염** — 위쪽에 **표 I 본문**이 같이 들어왔고(표 캡션은 빠짐), 캡션 필드는 900 자에서 잘렸다(그림 4 캡션 뒤에 패치 시험 절 본문이 붙음).
- **fig_9 캡션 필드 오염** — 캡션 뒤에 p. 9 왼쪽 단 첫 문장("pressure, as this leads to a higher level of compressive stress …")이 붙음.
- **fig_11 오탐** — 그림 11(복잡 기하 래스터 · p. 10 왼쪽 위 (48.1, 63.0)–(368.7, 202.5))이 아니라 **그림 12 그래프의 왼쪽 조각**(전압 눈금 숫자 잘림)을 잘랐다. 캡션 필드는 그림 11 로 맞다 → **수동 `fig_11_manual_p10.png`**.
- **fig_12 과대** — 위에 그림 11 표지 "(b) assembled in charged state" · 왼쪽에 본문 단 일부(그래프 온전).
- 나머지(fig_2 · 3 · 5–8 · 10 · 13–17) 라벨 · 내용 온전 · 과대 0 · 캡션 필드 깨끗.

수동 9 = 그림 1 전폭 · 그림 11 · **표 I · 표 B·I · B·II · B·III · B·IV · B·V · B·VI**(전부 300 dpi 쪽 렌더 · bbox 는 `figures.json`). **26 장 전부 직접 봤다 — 안 본 그림 · 표 0.** (그림이 아닌 래스터 — p. 1 IOP 로고 · 광고 — 는 열지 않았다.) 판독: 그림 7 · 8 · 9 · 12 · 14 · 15 · 17 은 **벡터 경로**(곡선 외곽선 · 축 상자 · 별표 무게중심)를 축 상자로 보정해 읽었다(판독 코드 · 중간 렌더는 `scratchpad` 에만 · 커밋 안 함).

## Fig. 1 — 계산 영역 모식 (p. 3 · 봤다 · 자동은 오른쪽 잘림 → 수동 전폭) ★ 모형 정의

- `[인쇄]` 캡션: "Figure 1. Schematic sketch of the computational domain."
- `[도표]` 2D 모식: 왼쪽 Ωa(음극) — 경계 Γa(음극-집전체, 갈색) · Γa-el(주황) · 가운데 Ωel(SE) · 오른쪽 위 Ωc(양극 활물질) — 원호 Γc-el(보라) · 오른쪽 경계 위 Γc(활물질-집전체, 빨강) · 아래 Γel(SE-집전체, 파랑) · 위 · 아래 Γcut(측면 대칭면). 원의 중심이 위쪽 Γcut 위에 있고 오른쪽 경계에서 잘린다 — **활물질이 집전체에 면으로 닿는다**(Φ = 0 이 걸리는 Γc). 축척 아님.

## Fig. 2 — 접촉 운동학 표기 (p. 4 · 봤다) ★ (a)

- `[인쇄]` 캡션: "Notation and kinematics to depict the contact interaction between two deformable bodies. The left part shows a configuration at time t0 where the two bodies are not in contact. The right part illustrates the deformed bodies at time t in contact but with a virtual separation for illustration purposes."
- `[도표]` Ω0(1) · Ω0(2) → Ωt(1) · Ωt(2) · 점 X(1) · X(2) → x(1) · x(2) · 사상 u(k)(X(k), t) · γct(1) · γct(2) · 단위 법선 n — 식 (12)–(13) 의 그림판. 수치 0.

## Fig. 3 — 패치 시험 기하 · 경계조건 (p. 7 · 봤다) ★★ (e)

- `[인쇄]` 캡션: "Geometry and boundary conditions of the patch test."
- `[도표]` 위 블록(전해질) t_el = 1 m · 2×2 · 아래 블록(전극) t_ed = 1 m · 3×3 **비정합 육면체 격자** · 단면 t = 1 m × 1 m · Γtop: **î = 0.1 A/m² · u_x = 0.0 m** · Γbottom: **Φ = 1 V · u_x = −0.04 m** · 좌표축 X 가 **아래** 방향. 측면 변위 0(본문).

## Fig. 4 — 패치 시험 해석해 ↔ 수치해 (p. 7 · 봤다 · 크롭 과대 · 표 I 본문 포함) ★★ (e) · R1

- `[인쇄]` 캡션: "Comparison of the analytic solution (dashed line) and the simulation result (solid line) of the patch test for the displacement and the electric potential." · 본문 "results in an error in the displacement solution of ε_u ≈10⁻¹² and an error in the solution of the electric potential of ε_Φ ≈10⁻⁹".
- `[도표]` x 축 "axial position x (m)" **0.00 – 1.96**(변형 뒤 길이 — 2 m 의 2 % 압축) · 변위 0 → −4×10⁻² m 선형 · 전위 ≈0.87 V(x 0) → ≈0.775 V(x 0.98 — 전해질 쪽 계면) · 점프 → ≈1.05 V → 1.00 V(x 1.96 — Φ = 1 V 경계). 점선 · 실선이 눈으로 겹친다.
- `[재현]` 표 I 로 다시 풀면(T 298 K · 변형 뒤 블록 길이 0.98 m): 전극 강하 0.1 × 0.98 / 2.0 = 0.049 V → Φ_ed(계면) **1.0490 V** · BV 대칭(α 0.5) η = −2RT/F·asinh(i/2i₀) = **−24.71 mV** → Φ_el(계면) = 1.0490 − 0.3 + 0.0247 = **0.7737 V** · 전해질 강하 0.098 V → Φ(top) **0.8717 V** · 점프 0.2753 V — **그림과 일치**.

## Fig. 5 — 패치 시험 전류 · 응력장 (p. 8 · 봤다) ★★ (e) · R2 · D2

- `[인쇄]` 캡션: "(a) shows the current in the x-direction and (b) the current in the x-direction at the contact interface. The xx-component of the Cauchy stress is displayed in (c), and the xx-component of the Cauchy stress at the contact interface in (d)." · 본문 "The fluxes across the contact interface are constant in the lateral direction because we used a segment-based coupling scheme."
- `[도표]` (a) 블록 전체 균일 초록 ≈ **−0.10 A/m²**(색 막대 −0.11 … −0.09) · (b) 계면 화살 균일 · **−x(위) 방향** · (c) 균일 노랑 ≈ **−0.552 Pa**(색 막대 −0.560 … −0.550) · (d) 계면 σ_xx 화살 균일.
- `[재현]` 식 (4) Ψ_el = α[tr(C_el) − 3] + (α/β)[det(C_el)^−β − 1] · α = E/[4(1+ν)] = 3.846 Pa · β = ν/(1−2ν) = 0.75 · 측면 구속 단축 변형 신장비 0.98 → S_xx = 2α[1 − λ^(−2β−2)] = −0.5636 Pa → **σ_xx = λ·S_xx = −0.5523 Pa** — 색과 일치.
- ⚠ **전류 부호**: 그림 4 의 전위가 +x 로 내려가고 식 (21)–(22) 가 i = −σ∇Φ · −κ∇Φ 이므로 전류는 **+x(아래)** 여야 하는데, 그림은 −0.10 · 화살 −x 다 — 출력 "current" 의 부호 규약 미기재(크기 0.10 은 일치)(D2).

## Fig. 6 — 단순 기하 (p. 8 · 봤다) ★★ (b) · G1

- `[인쇄]` 캡션: "Simplified SSB geometry consisting of a lithium metal anode (gray), a solid electrolyte (green), and a cathode active material particle (anthracite)."
- `[도표]` 원근 그림 하나 — 회색 Li 금속 판 · 반투명 초록 SE · 진회색 입자 조각(위 대칭면에 반원 단면) · 사면체 격자. **치수 · 눈금 0.** 표 B·IV: 양극 10.0 · 분리막 10.0 · 음극 5.0 µm · 입자 지름 10.0 µm · AM : SE 36 : 64 · 측면 "—".
- `[재현·가정]` 그림 7 벡터 값으로 측면 단면적 ≈18.0 µm² · AM ≈64.0 µm³ — 지름 10 µm 구 부피 523.6 µm³ 의 0.122(≈1/8 · 65.4) 와 같은 자릿수 · 정확한 자름 방식은 미인쇄(G1).

## Fig. 7 — 질량 보존 (p. 8 · 봤다 · 벡터 판독) ★★★ (e) · R7 · D1

- `[인쇄]` 캡션: "Amount of substance of lithium and lithium-ions over the state of charge during charging at 0.1 C until the cutoff voltage of 4.2 V is reached." · 본문 "prestressed to a stack pressure of 70 MPa" · "the total amount … remains constant … with only a minor relative deviation of approximately 10⁻⁵%".
- `[도표·벡터]` **음극 6.93 → 8.77 · 전해질 3.04(일정) · 양극 3.32 → 1.48 · 합 13.28 pmol(일정)** · 네 선이 SoC **95.1 %** 에서 끝남(= contact 70 MPa 의 4.2 V 도달 — 그림 8 과 같은 모의로 읽힌다) · 양극 선 기울기 −0.01954 pmol/%.
- `[재현]` 음극(두께 5.0 µm · 7.69×10⁴ mol m⁻³)으로 측면 **18.01 µm²** · 전해질(분리막 10 + 양극층 10 × 0.64 = 16.4 µm 등가 · 1.03×10⁴)로 **17.98 µm²** — 두 독립 경로가 0.2 % 안에서 맞는다. 그 면적으로 양극 3.32 pmol 을 읽으면 **초기 양극 농도가 c_max·χ0% = 5.19×10⁴ 일 때만** AM 부피 64.0 µm³ = 35.6 %(표 B·IV 36 : 64 ✅) — 표 B·V 의 **2.10×10⁴ 이면 158 µm³ = 88 %** ❌ (D1). 양극 선 기울기 × 100 / 초기량 = 0.588 ↔ 창 1.0 − 0.404 = 0.596(1.3 % 차).

## Fig. 8 — 압력 · 계면 법칙별 충전 전압 (p. 8 · 봤다 · 벡터 판독) ★★★★ (b) · (c)

- `[인쇄]` 캡션: "Comparison of the cell voltage curves over the state of charge of the different mechanical interface models for different mechanical stack pressures." · 본문 "neglecting the physical effect of delaminations … leads to overestimating the transferred charge" · "a higher mechanical stack pressure increases the transferred charge of the charging process" · "The results of the contact interface model would converge to the result of the mesh tying interface model for increasing mechanical stack pressure."
- `[도표·벡터]` **4.2 V 도달 SoC: mesh tying 70 MPa 99.30 · contact 70 / 60 / 50 MPa 94.81 / 91.26 / 87.18 %**(곡선 중앙선이 4.2 V 를 지나는 점 — 판독 폭 ≈±0.2 %p · 그림 10 래스터 표지 99.4 · 94.9 와 일치) · 전압 차(contact 70 − mesh tying) 47.5 % SoC 에서 5 mV · 61 % 에서 10 mV · 90 % 에서 24 mV · 94 % 에서 46 mV · contact 50 MPa 는 41 % 에서 5 mV · 51 % 에서 10 mV · 초기 혹 **3.682 V @ SoC ≈6.3 %**(네 곡선 같음).
- `[재현]` 식 B·1 OCV 의 국소 최대 3.6817 V @ χ 0.949(SoC 8.6 %) — 초기 혹은 OCV 함수 모양이지 역학 효과가 아니다. OCV = 4.2 V 는 χ 0.4065(SoC 99.58 %) — mesh tying 99.30 % 는 0.1 C 에서 열역학 한계의 0.3 %p 안.
- "would converge … for increasing mechanical stack pressure" 는 **세 점의 외삽 명제**(70 MPa 위 계산 0).

## Fig. 9 — 박리 계면 면적 몫 (p. 9 · 봤다 · 벡터 판독 · 캡션 필드 본문 섞임) ★★★★ (a) · (b) · Q1

- `[인쇄]` 캡션: "Comparison of the delaminated cathode-solid electrolyte interface area share over the state of charge of the different mechanical interface models for different mechanical stack pressures." · 본문 "for a larger stack pressure, the delamination occurs at a later SoC and that the share of the delaminated interface area is always lower" · mesh tying(점선) = "the share of the cathode interface under tensile stress that would lead to delaminations if not suppressed" · "starting from an SoC of approximately 25%, it exhibits almost the same course as the contact scenario for … 60 MPa".
- `[도표·벡터]` 시작(몫 > 0.6 %) SoC: **contact 50 / 60 / 70 MPa 13.2 / 14.9 / 16.4 %** · mesh tying 인장 몫 15.7 % · SoC 20 % 몫 30.0 / 23.8 / 16.5 · 16.1 % · 40 % 67.0 / 60.9 / 56.6 · 62.4 % · **끝 몫 97.1 / 90.5 / 87.8 · 92.9 %**(곡선 끝 SoC 87.1 · 91.4 · 95.2 · 99.4 %). 세 압력의 순서는 표본점 전부에서 유지 ✅ · mesh tying 점선은 25 % 뒤 60 MPa 곡선 ±1.5 %p ✅.
- ⚠ **재접촉 한 번 — 본문 0**: 70 MPa 곡선이 SoC **93.5 → 94.5 % 에서 89.6 → 87.7 %** 로 내려간다(≈1.9 %p) · 60 MPa 곡선도 89.6–90.1 % 에서 89.8 → 89.3 % 작은 굴곡. 계면 일부가 충전 끝에서 다시 닿았다는 뜻인데(`[해석]` 원인 미상 — 입자 안 농도 불균일 · 스프링 반력 증가 후보), 지면은 이 장면을 말하지 않는다(D3).
- 곡선이 계단 모양 — 요소 면 단위로 접촉 상태가 바뀐다(G3).

## Fig. 10 — 단순 기하 입자 단면 농도 · 계면 플럭스 (p. 9 · 봤다) ★★★★ (c) · R12

- `[인쇄]` 캡션: "Comparison of the development of the concentration distribution in the cathode active material at different states of charge for the mesh tying and the contact interface model for a mechanical stack pressure of 70 MPa. Note that each figure has its separate color bar. The black arrows indicate the magnitude of the local charge flux density across the cathode-solid electrolyte interface." · 본문 "The delamination of active material and solid electrolyte first occurs in lateral directions near the middle of the particle … compensated by a larger interface charge flux in the remaining interface area, as depicted by the increasing size of the black arrows near the current collector and the separator."
- `[도표]` 패널별 색 막대(mol m⁻³): (a) mesh tying 20 % **44,920–45,120** · (b) contact 20 % **44,900–45,120** · (c) mesh tying 50 % **36,105–36,265** · (d) contact 50 % **35,840–36,310** · (e) mesh tying "4.2 V ≈ 99.4 % SoC" **21,340–21,500** · (f) contact "4.2 V ≈ 94.9 % SoC" **21,380–22,930**. mesh tying 는 방사형 기울기 · 화살 균일 · contact 는 (d) 부터 측면 화살 소멸 · 양 끝 화살 커짐 · (f) 입자 중심 빨강(고농도 — Li 가 남음).
- `[재현·가정]`(χ = c·det F/c_max · det F ≈ (1+f(χ))/(1+f(1)) 반복): (f) 최솟값 → χ **0.4059** → OCV **4.2013 V** · 최댓값 → χ **0.4361** → **4.1346 V**(차 67 mV) · 평균 χ(SoC 94.9 %) 0.4344 · (e) 21,340–21,500 → OCV 4.2031–4.1959 V(차 7 mV). ⇒ contact 의 컷오프는 **접촉 자리 표면이 OCV 4.2 V 점에 닿을 때** 왔고, 그때의 평균 − 표면 χ 차 `/0.596` = **4.78 % SoC ≈ 결손 4.5 %p**. "SoC ≈99.4 · 94.9 %" 표지는 **그림 안 글자뿐**(본문 0).

## Fig. 11 — 복잡 미세구조 두 판 (p. 10 · 봤다 · **수동** — 자동은 오탐) ★★ (b) · (c) · G8

- `[인쇄]` 캡션: "Complex SSB geometries consisting of a lithium metal anode (gray), a separator and catholyte made of solid electrolyte (green), and an artificial cathode active material particle microstructure (anthracite)." · 본문 "the surfaces of the cathode active material inside the solid electrolyte are depicted in dark green" · (a) "assembled in the discharged state, i.e. with lithiated cathode active material" · (b) "assembled in the charged state, i.e. with delithiated cathode active material and a thicker lithium metal anode to keep the total lithium inventory constant".
- `[도표]` (a) · (b) 같은 입자 배치 — 회색 Li 판이 (b) 에서 눈에 띄게 두껍다(표 B·IV 8.0 ↔ 14.0 µm) · 입자 79 가 서로 겹치고 영역 경계에서 잘린 단면이 진회색 원. 축척 막대 0.
- `[재현]` AM 부피 0.38 × 50 × 50 × 40 = 38,000 µm³ ↔ 지름 e^2.3 = 9.97 µm 구 79 개 41,045 µm³(+8 % — 겹침 · 경계 잘림) · 두 판의 Li 재고 차 = 음극 6 µm × 2,500 µm² × 7.69×10⁴ = 1.154×10⁻⁹ mol ↔ 양극 창(χ 1.0 → 0.404) 1.175×10⁻⁹ mol(98.1 % — 정확히 맞추려면 6.11 µm).

## Fig. 12 — 방전 상태 조립 셀 0.5 C 첫 충전 (p. 10 · 봤다 · 벡터 판독 · 크롭 과대) ★★★ (b) · (c)

- `[인쇄]` 캡션: "Comparison of the cell voltage curves over the state of charge for two different mechanical interface models during a charging process applied to a complex microstructure of a cell assembled in the discharged state." · 본문 "The contact simulation shows a higher course of the cell voltage over SoC starting from about 30% SoC … leading to an SoC of 92.5% in the mesh tying case. In contrast, an SoC of only 89.4% is reached for the model incorporating the delamination effect."
- `[도표·벡터]` mesh tying 4.2 V @ **≈92.3–92.6 %**(외곽선 끝 92.65) · contact **≈89.5 %**(외곽선 끝 89.56) — 본문 92.5 · 89.4 ✅ · 전압 차 30 % 3 mV · 40 % 9 mV · 50 % 15 mV · 60 % 21 mV · 70 % 27 mV · 80–85 % 30 mV · 89 % 34 mV.

## Fig. 13 — 복잡 기하 단면 농도 (p. 11 · 봤다) ★★★ (c) · G5

- `[인쇄]` 캡션: "Comparison of the concentration distribution in the cathode active material at different states of charge for the mesh tying and the contact interface model on a slice through the complex microstructure of a cell assembled in the discharged state. Note that each figure has its color bar." · 본문 "In the mesh tying case, the concentration gradient is mainly oriented in the axial direction, with the smallest concentration value near the anode on the left … For the contact scenario … local delaminations dominate it … the concentration gradient in the radial direction of the cathode active material has vanished."
- `[도표]` (a) mesh tying 75 % **27,150–29,000** · (b) contact 75 % **26,400–30,600** · (c) mesh tying "4.2 V ≈ 92.5 % SoC" **21,900–23,500** · (d) contact "4.2 V ≈ 89.4 % SoC" **22,050–26,100** mol m⁻³. contact 패널에 입자 둘레 흰 틈(박리) · **작은 입자 하나는 단면에서 둘레 전체가 흰 테** — 3D 에서 통째로 떨어졌는지는 단면 하나로 모른다(G5). 단면 위치 미인쇄.

## Fig. 14 — 접착 범위 · 인장 면적 몫 (p. 11 · 봤다 · 벡터 판독) ★★★ (a) · (b)

- `[인쇄]` 캡션: "Development of the interfacial area share under tensile stresses and the interfacial area share that experiences tensile stresses in a range relevant for adhesion effects, i.e. up to 8 MPa, at the cathode active material-solid electrolyte interface for the mesh tying interface model." · 본문 "this share is always below 0.7% … the share of the interfacial area that experiences tensile stresses … goes up to 80% … supporting that the effect of adhesion can be neglected."
- `[도표·벡터]` 파랑(왼축 0–0.8 %) — 0–8 MPa 인장 몫 **최대 0.62 % @ SoC 26.7 %** · SoC ≈6 % 에서 시작 · ≈42 % 뒤 ≈0 · 빨강(오른축 0–80 %) — 인장 몫 SoC 20 % 13 · 30 % 34 · 50 % 64 · 70 % 73 · 90 % 79 · **끝(≈92.5 %) 79.8 %**. 본문 두 숫자 ✅. **mesh tying 모의의 사후 처리**다 — contact 모의의 박리 몫(복잡 기하)은 인쇄 0(G5).

## Fig. 15 — 충전 상태 조립 셀 0.5 C 첫 방전 (p. 12 · 봤다 · 벡터 판독 · x 축 100 → 0) ★★ (b) · (c)

- `[인쇄]` 캡션: "Comparison of the cell voltage curves over the state of charge for the different mechanical interface models during a discharging process applied to a complex microstructure of a cell assembled in the charged state." · 본문 "Only a minor difference toward the end of the discharge process at about 6% SoC … approximately 1.7% in the mesh tying case and 1.9% in the contact case, thus only deviating by 0.2%."
- `[도표·벡터]` 2.8 V 도달 SoC **≈1.60(mesh tying) · ≈1.86 %(contact)** — 본문 ✅ · 두 곡선은 6 % 아래에서만 갈린다(5 % 22 mV · 4 % 30 mV · 3 % 50 mV).

## Fig. 16 — 충전 상태 조립 셀 방전 끝 단면 (p. 12 · 봤다) ★★ (c)

- `[인쇄]` 캡션: "Comparison of the concentration distribution at the end of the discharge process for the mesh tying and the contact interface model on a slice through the complex microstructure of a cell assembled in the charged state."
- `[도표]` 공통 색 막대 **49,750–51,700** mol m⁻³ · (a) "2.8 V ≈ 1.7 % SoC" · (b) "2.8 V ≈ 1.9 % SoC" · 두 패널 거의 같음 · 오른쪽 아래 입자 무리 저농도(파랑)는 둘 다 — 박리 흔적 없음(본문과 같은 판독).

## Fig. 17 — NMC622 부피 변화 자료와 7차 적합 (p. 14 · 봤다 · 벡터 판독) ★★★ (e) · R5 · Q8

- `[인쇄]` 캡션: "Approximation of measured data of the volume change of NMC622 as published in Ref. 26 (symbols) by a polynomial fit of order seven (solid lines)." · 본문 식 (10) 등방 성장 "applied for secondary NMC particles whose primary particles can be assumed to be randomly distributed".
- `[도표·벡터]` 별표 **24 점 · χ 0.222–0.912 · f −0.0415 → −0.0002** · 실선은 **χ 0.218–0.920 만** 그림.
- `[재현]` 표 B·III 계수의 자료 잔차 RMS **0.00046** · 최대 0.00091 · f(1.0) = −0.00009 · f(0.404) = −0.01486 → 운용 창(χ 1.0 → 0.404)의 **ΔV/V −1.478 %**(선 변형 −0.495 %) · 0.912–1.0 은 **외삽**(단조 · +0.05 %). 자료가 격자(XRD) 부피인지 입자 부피인지 캡션 · 본문 미기재(G9 · 원장 §3-b (노)).

## Table I — 패치 시험 매개변수 (p. 7 · 봤다 · **수동** · 본문은 fig_4 위쪽에도) ★ (e)

`[인쇄]` 전해질 κ 1.0 S m⁻¹ · E 20 Pa · ν 0.3 / 전극-전해질 계면 i₀ 0.1 A m⁻² · α 0.5 · Φ₀ 0.3 V / 전극 σ 2.0 S m⁻¹ · E 20 Pa · ν 0.3 — 본문 "the material parameters listed in Table I are artificial and do not represent realistic materials".

## Table B·I — 역학 매개변수 (p. 14 · 봤다 · **수동**) ★★★ (e)

| 상 | E | ν | ρ | 출처 |
|---|---|---|---|---|
| NMC622 | 1.75·10¹¹ Pa | 0.3 | 5.03·10³ kg m⁻³ | [54] · [55–57] · [35] |
| β-LPS | 2.89·10¹⁰ Pa | 0.27 | 1.88·10³ | [58] · [58] · [59] |
| Li | 4.90·10⁹ Pa | 0.42 | 5.34·10² | [26] · [26] · [60] |
| 스프링 k (식 36) | **1.0·10¹³ kg m⁻² s⁻²** "equivalent spring stiffness" | | | **assumed** |

## Table B·II — 전기화학 매개변수 (p. 14 · 봤다 · **수동**) ★★★ (e)

`[인쇄]` NMC622: σ 4.55·10⁻¹ S m⁻¹ · D 2.40·10⁻¹⁴ m² s⁻¹(둘 다 "**averaged from 25**") · Φ₀ 식 B·1 [61] · i₀ **4.98 A m⁻²** "exchange current density factor"(**adapted from 25**) · α_a 0.5 [25] · c_max 5.19·10⁴ mol m⁻³ [25] · χ_max 1.0 [25] · **χ0% 1.0 · χ100% 4.04·10⁻¹ ("assumed")** / β-LPS: κ 1.20·10⁻² S m⁻¹ · t_el 1.0 [25] / Li: σ 1.00·10⁵ S m⁻¹ · Φ₀ 0.0 V · i₀ 8.87 A m⁻² · α_a 0.5 [25].

## Table B·III — 부피 변화 법칙 (p. 14 · 봤다 · **수동**) ★★ (e) · R3

`[인쇄]` NMC622 a₀ 0.000444577043098 · a₁ −1.24116361022373 · a₂ 9.30461909734883 · a₃ −29.44977325195 · a₄ 49.1126838772603 · a₅ −45.1097641074935 · a₆ 21.5994362668471 · a₇ −4.21656846170118 / Li g **1.2998·10⁻⁵ m³ mol⁻¹** — `[재현]` M_Li/ρ_Li = 6.941×10⁻³/534 = 1.29981×10⁻⁵ ✅.

## Table B·IV — 기하 · 이산화 (p. 15 · 봤다 · **수동** · 쪽 전폭) ★★★ G1

| 양 | 단순 기하 | 복잡 기하 |
|---|---|---|
| 측면 치수 | **—** | 50.0 µm |
| 양극 · 분리막 두께 | 10.0 · 10.0 µm | 40.0 · 8.0 µm |
| 음극 두께(방전 / 충전) | 5.0 µm | 8.0 / 14.0 µm |
| AM : SE (양극 안) | 36 : 64 | 38 : 62 |
| log-normal μ · σ | — | 2.3 · 0.05 |
| 입자 지름 · 개수 | 10.0 µm · 1 | — · 79 |
| 절점 / 요소 | 1,832 / 7,105 | 106,716 / 111,657 · 524,737 / 553,356 |

## Table B·V — 초기 농도 (p. 15 · 봤다 · **수동**) ★★★ D1

`[인쇄]` 양극 **2.10·10⁴** [25] · 전해질 1.03·10⁴ [25] · 음극 7.69·10⁴ mol m⁻³(식 B·5 c = ρ/M — `[재현]` 534/6.941×10⁻³ = 7.693×10⁴ ✅). ⚠ 양극 값은 χ = 2.10/5.19 = **0.405 = χ100%(충전 상태)** — 충전 상태 조립 셀(그림 11b)에만 맞고, 방전 상태 조립(단순 기하 · 그림 11a)의 초기값 c_max·χ0% = 5.19·10⁴ 는 표에 없다(그림 7 `[재현]` — D1).

## Table B·VI — 스프링 목표 변위 (p. 15 · 봤다 · **수동**) ★★★ (b) · R6

`[인쇄]` 단순 50 · 60 · 70 MPa ↔ u_k,target 5.041 · 6.049 · 7.057 µm · 복잡(방전 조립) 70 ↔ 7.102 · 복잡(충전 조립) 70 ↔ 7.133 µm. `[재현]` §(b) 1.

## 본문 서술과 어긋난 그림 (요약)

- 그림 5 — 전류 부호(−x) ↔ 그림 4 기울기 · 식 21–22(+x)(D2).
- 그림 7 — 양극 초기량이 표 B·V 의 양극 초기 농도와 안 맞음(D1).
- 그림 9 — 70 MPa 끝의 재접촉(≈1.9 %p)이 본문 · 초록의 "recontacting" 결과로 서술되지 않음(D3) · 캡션의 "delaminated … share" 가 mesh tying 점선(인장 몫)까지 덮음(D10).
- 그림 10 · 13 · 16 — SoC 표지가 그림 안에만(99.4 · 94.9 는 본문 0).
- 그림 13 — 둘레 전체가 흰 테인 입자(통째 박리 후보)가 본문에 없음.
- 그림 14 — "adhesion range" 축은 Li–LLZO 의 최댓값 8 MPa([30])로 그은 선 — 이 편이 "가장 관련" 이라 한 412 kPa([28])로 그었으면 몫이 더 작다(방향은 결론과 같음 — `[해석]`).

---

# 절별 해체 (본문)

## 초록 (p. 2)

`[인쇄]` "A novel approach is presented to model delamination and recontacting at internal interfaces of three-dimensional resolved microstructures of solid-state batteries. To resolve the effect of delaminations, we incorporate the consistent enforcement of contact constraints at those interfaces using Nitsche's method. … The simulations show that **increased mechanical stack pressure during cycling mitigates delamination tendencies** at the electrode-solid electrolyte interface. **Consistent with existing literature**, the simulations demonstrate that delaminations increase the internal resistance and reduce the amount of transferred charge. **In contrast to experimental analyses, the presented model allows quantitative and in-depth investigations of delamination effects.** Furthermore, our analysis of two cell concepts—one assembled in the discharged state and another assembled in the charged state—indicates that **half-cells assembled in an initial state from which the active material shrinks in volume upon first charge or discharge show a higher delamination risk** at the electrode-solid electrolyte interface."
`[해석]` 넷째 명제의 "first charge **or discharge**" 는 계산되지 않은 경우(방전 때 수축하는 재료)를 포함한 일반화다 — 비교는 NMC622 셀 둘 · 70 MPa · 0.5 C · 첫 반 사이클씩(D12). "Consistent with existing literature" 와 "quantitative" 는 §(e) 2 에서 대조.

## 서론 (p. 2–3)

- **박리 문헌**: 음극 쪽 void(산화물 [3,4] · 황화물 [5–8]) → `[인쇄]` "It is commonly observed that delaminations result in increased cell resistance due to a reduced active interface area, which leads to current constrictions. This effect can be moderated by increasing the stack pressure as shown in, e.g. Refs. 5, 8." · 양극 쪽 "volume changes of the cathode active materials during cycling, resulting in accumulating voids at the interface of active material and solid electrolyte, as demonstrated in Refs. 9–12"([9] = 23호 Koerver 2017 · [11] = 4호 Shi 2020 *JMCA* · [10] Jung · [12] Liu B. 2023 *SusMat*).
- **모형 문헌**: [13] Tian & Qi 2017 "a one-dimensional Newman model … to include the effect of contact area loss in a phenomenological manner" · 2D: 음극 void [14–19] · 양극 박리 [20–22](Barai 2021 · Bistri 2021 · Farzanian 2023) · 3D 단일 입자 [23](Zhang T. · Kamlah · McMeeking 2024) · 해상 미세구조의 "debonding index" 만 [24](Huang 2023 — "neglecting the interaction on the electrochemistry that no flux of charges or mass can be transferred over delaminated interfaces") · [25](Neumann 2020) — `[인쇄]` "interface effects are analyzed in detail, but the consideration of solid mechanics … is not assessed. Instead, the interfaces of the resolved microstructures that are delaminated are **specified as input regardless of the actual mechanical state**."
- **무시하는 효과 셋**(정량 근거 인쇄): ① 응력 → OCV — `[인쇄]` "Ref. 26 measured a dependence of 1 mV/100 MPa experimentally … [27] … 3.6 mV/100 MPa. Since … we vary the external pressure from 50 to 70 MPa, i.e. by 20 MPa, we expect that the influence … on the OCV is clearly below 1 mV … less than one per mil compared to the cycling voltage range" — `[재현]` 0.2 · 0.72 mV · 1.4 V 창의 0.05 % ✅ ② 응력 → i₀ — "[27] … a deviation of the exchange current density of approximately 1.4% between … the lowest and highest stack pressure"(재현 불가 — 부분 몰 부피 미인쇄) ③ 접착 — 문헌 값: 복합양극(NMC622 · 아지로다이트 · HNBR · C65) 최대 인장 **412 kPa**[28] · LTO/LLZO 30 · 540 kPa[29] · Li/LLZO **1.1 kPa(저항 최대) ↔ 8 MPa(저항 최소)**[30] · 액체 LIB 최대 2.3 MPa[31] · 200 kPa–1.2 MPa[32] — "We expect the highest relevance for … 412 kPa" · 결과 절에서 "justified to omit adhesion effects".

## Problem Definition (p. 3–6 · 식 1–40)

- **영역**(그림 1): Ωa(Li 금속) · Ωel(**균질** SE — "remaining voids or additional phases like binder or carbon black are omitted") · Ωc(활물질만) · 집전체 비해상.
- **체적 식**(식 1–10 · `[인쇄]` 앞 편 [35] 요약): 운동량(유한 변형 · F = F_el·F_gr · 식 3 · Neo-Hooke 식 4) · 전하(전극 σ · SE κ — 전기 중성 · 단일 이온 t = 1 · "the conductivity and the diffusion constants are unaffected by strain … the effect of stress gradients is neglected") · 질량(변형 영역 위 Fick — 식 7 · SE 식 8) · **Li 음극 = 두께 방향 이방 성장**(식 9 · g = M_Li/ρ_Li — "we do not resolve the surface deposition and dissolution at the lithium metal anode") · **NMC = 등방 성장**(식 10 · f(χ) 7차 다항 · 기준 χ₀ = 초기 상태).
- **계면 식**(식 11–27): Γ_ed−el = **mesh tying 부분 Γmt**(식 11 u(1) = u(2) — "no delamination occurs") ∪ **contact 부분 Γct**("A delamination of the bodies and subsequent recontacting can occur") · 법선 틈 g_n(식 13) · 견인력 분해(식 14–16) · **HSM 조건(식 17)** · 전하 · 질량 연속(식 18–24) · BV(식 25 — i₀ · α_a) · 과전압 η = Φ_ed − Φ_el − Φ₀(식 26) · **식 27 — p_n < 0 일 때만 플럭스**.
- **경계조건**(식 28–36): 집전체 불투과 · 측면 Γcut 대칭(질량 · 전하 플럭스 0) · Φ = 0 on Γc · 정전류 −i·n = î on Γa(양 = 충전) · Dirichlet · Neumann · **Robin 스프링(식 36)** — `[인쇄]` "to consider the mechanical stiffness k of the environment of the battery, e.g. a cell housing or a measuring setup".
- **초기 조건**(식 37–40): c = c⁰ · u = 0 · u̇ = 0 — "the battery is assumed to be in static equilibrium" · 역학 기준 = 조립 상태.

## Aspects of The Numerical Model (p. 6 · 식 41–46)

약형(식 41) · mesh tying = Lagrange 승수(식 42) · 접촉 항 재정식화(식 43–44 · 도약 연산자) · 가중 평균 {·}_ωs · **비매끈 등식 제약**(식 45 · [*]_− = min[0, *]) · **Nitsche 기여**(식 46 · θ ∈ {−1, 0, 1} — "The non-symmetric version with θ = 0 is applied throughout this work since it is explicitly appealing in the context of coupled problems") · 벌칙 γ_n · 가중 ω_s → 부록 A. 단일체 풀이 · 블록 전처리 · MPI(서론).

## Results — 검증 (p. 6–8 · 그림 3–7 · 표 I · 식 47)

- **패치 시험**: 비정합 두 블록 · 정상 상태 · 선형 해석해 · ε_u ≈10⁻¹² · ε_Φ ≈10⁻⁹ · "segment-based coupling" 이라 계면 플럭스가 측면 상수(노드-대-세그먼트는 아닐 수 있음 [46]).
- **질량 보존**: 단순 기하 · 70 MPa · 0.1 C 충전 → 4.2 V · "minor relative deviation of approximately 10⁻⁵%" · "The discrete solution does not perfectly fulfill the mass conservation due to the highly nonlinear nature of Eqs. 7 and 8. However, we already showed in our previous work[35] that the model formulation is consistent, and the error decreases as the time discretization is refined."
- `[해석]` 둘 다 **verification**(구현 · 보존) — 실험과 맞대는 validation 은 이 편에 없다(§(e) 2).

## Results — 스택 압력 (p. 8–10 · 그림 8–10)

단순 기하 · 방전 상태 조립 · 예압 50 / 60 / 70 MPa · 0.1 C 충전 → 4.2 V · mesh tying 은 70 MPa 하나. 인쇄 명제 다섯: ① contact 70 < mesh tying 70(전달 전하 과대 추정) ② 압력 ↑ → 전달 전하 ↑ ③ 박리 시작 늦고 몫 작음 ④ mesh tying 인장 몫 ≈ contact 70(처음) → ≈ contact 60(25 % 뒤) — "the mechanical interface law also impacts the solution of the solid mechanics field" ⑤ 측면 가운데부터 박리 · 남은 면(집전체 · 분리막 쪽)으로 플럭스 집중 → 농도 분포가 축 방향으로. 수치(`[도표·벡터]`)는 그림 8 · 9 절.

## Results — 복잡 미세구조 (p. 10–12 · 그림 11–16)

- **방전 상태 조립 → 0.5 C 첫 충전**(70 MPa): contact 전압이 30 % SoC 부터 높고 기울기 큼 · **92.5 ↔ 89.4 %** · contact 는 국소 박리(주로 측면 — "Due to the applied axial load, the delaminations occur mainly in lateral directions") · 방사 기울기 소멸 · `[인쇄]` "The most likely cause of the local delaminations … is the cell assembly in the discharged state … Even with a mechanical stack pressure of 70 MPa, the used electrolyte cannot compensate for this volume change through mechanical deformation."
- **접착 검사**(mesh tying 사후 처리): 0–8 MPa 인장 몫 < 0.7 % · 인장 몫 ≤80 % — "a large part of the interface experiences tensile stresses exceeding the adhesion strengths, supporting that the effect of adhesion can be neglected".
- **충전 상태 조립 → 0.5 C 첫 방전**(70 MPa · 2.8 V): 차 ≈6 % SoC 아래에서만 · **1.7 ↔ 1.9 %** · 단면 농도 거의 같음 · `[인쇄]` "This confirms the hypothesis from the previous Section that a cell assembly in the discharged state can increase mechanical problems".

## Summary · Data · 부록 (p. 12–15)

- 요약 — 위 명제 반복 + "adhesion effects do not play a significant role in preventing delaminations … for the investigated scenarios" · "assembling the cell in a discharged state, which is considered optimal from energy and power density considerations as an excess lithium metal anode can be prevented in theory, leads to an increased tendency for delaminations" · **향후 과제**: 불균일 Li 도금 성장 + 점소성 Li 구성식(음극 박리) · **접착 확장**(특히 소결 산화물 복합 전극) · 외부 압력 요구치에 대한 셀 개념 최적화.
- **부록 A**: 벌칙 γ_n 은 강성 · 격자 크기 역수에 비례해야(강제성 [48]) · 큰 벌칙은 Newton 수렴을 해침 · θ = 0 은 하한 γ_n > C_u 필요 → 고유값 문제(식 A·1–A·3 · [49]) · 요소별 C_u,e(Dolbow & Harari [51] — 목록에 없음) · **γ_n,e = C_u,e γ_n,0**(식 A·4 — γ_n,0 값 인쇄 0) · **조화 가중 ω_s = C_u(2)/(C_u(1) + C_u(2))**(식 A·5 · [53]).
- **부록 B**: 표 B·I–B·VI · OCV 식 B·1([61]) · 다항 f(χ) · log-normal 식 B·4(d̄ = d/1 µm) · c = ρ/M(식 B·5) · 예압 램프(식 B·6 — 250 s/Ĉ 코사인) · C-rate 램프(식 B·7 — 그다음 250 s/Ĉ) · "Both fields are ramped up depending on the C-rate because the choice of the time step is based on the C-rate".

---

# ★ (a) 박리 · 재접촉 기준 — 무엇이 열고 무엇이 닫나

## 1. 인쇄된 기준

| 자리 | 이 편 (`[인쇄]`) | 성질 |
|---|---|---|
| **여는 조건** | 식 (13) g_n = −n·[x(1) − x(2)] · 식 (17) **g_n ⩾ 0 · p_n ⩽ 0 · g_n p_n = 0** — "As we do not account for adhesion in this work, the normal contact traction can only originate from compressive forces" | **인장 강도 0** — 문턱 · 접착 에너지 · 손상 0. 수직 응력이 압축이 아니게 되면 틈이 열린다 |
| **전기화학 결합** | 식 (27) j F = i = { i if p_n < 0 ; 0 else } on γct — "charge and mass are only transferred if the bodies are in contact, i.e. the normal contact traction is negative" | 이진 스위치 — 닿은 면은 **같은 i₀** 의 BV, 떨어진 면은 0 · 접촉 압력이 클수록 반응이 빨라지는 항 0(응력 → i₀ 무시 — 서론) |
| **닫는(재접촉) 조건** | 같은 식 (17) — 틈이 닫히고(g_n = 0) 압축(p_n < 0)이 서면 식 (27) 이 BV 를 돌려준다 | **대칭 · 기억 0** — 박리 이력 · 접착 상실 · 표면 변화가 남지 않는다 |
| **접선** | "Without friction effects, the tangential contact traction has to vanish t_t = 0" | 미끄럼 자유 |
| **수치 강제** | Nitsche(식 45–46 · θ = 0) · γ_n,e = C_u,e γ_n,0(요소별 국소 고유값 · 식 A·1–A·4) · 조화 가중 ω_s(식 A·5) | 침투 허용 폭은 벌칙이 정한다 — **γ_n,0 값 인쇄 0**(G2) · 물리 매개변수 아님 |
| **mesh tying(대조)** | 식 (11) u(1) = u(2) · Lagrange 승수(식 42) — "no delamination occurs" | 같은 계면을 붙여 둔 반사실(counterfactual) — 인장 몫은 사후 처리로만(그림 9 점선 · 14) |
| **제외** | 접착 · 마찰("could be extended … based on our previous work, including friction[36] and adhesion[37]") · SE 소성 · 크리프 · 균열 · 공극 · 바인더 · 탄소 · 음극 쪽 박리(균질 성장) | 비가역 기구 전부 0 |

## 2. 가역인가 비가역인가 — **구성상 완전 가역**

`[해석]` 위 표의 어느 자리에도 **이력 변수가 없다** — 박리 여부는 매 순간의 기하(g_n)와 응력(p_n)만으로 정해진다. NMC 가 다시 리튬화되어 부피를 되찾거나(f(χ) 가 올라감) 외부 압력이 올라가 틈이 닫히면, 같은 면이 같은 i₀ 로 돌아온다. 따라서 이 모형에서 접촉 손실은 **"가역 · 순간 · 기하"** 이고, 비가역(접착 손상 · 표면 오염 · SE 크리프로 생긴 영구 틈)은 정의상 0 이다. 비가역은 저자가 확장 방향으로만 적었다(접착 [37] · 점소성 Li — 음극).

## 3. 결과에서 재접촉은 보였나 — **본문 0 · 그림 9 벡터에 한 번**

- `recontact*` **6 회**(초록 · 서론 둘 · 계면 정의 · 결과 머리 · 요약) — **전부 틀 문장**. 결과 절의 어느 문장도 재접촉 장면을 서술하지 않는다(D3).
- 계산된 반 사이클은 넷 — 단순 기하 첫 충전(박리만 자람) · 복잡 기하 첫 충전(박리) · 복잡 기하 첫 방전(충전 상태 조립 — 팽창 · 박리 없음). **방전 상태 조립 셀의 다음 방전**(재팽창 → 재접촉)은 계산 0(G14).
- `[도표·벡터]` 유일한 재접촉 흔적: 그림 9 의 **70 MPa 곡선 SoC 93.5 → 94.5 % 에서 박리 몫 89.6 → 87.7 %**(≈1.9 %p — 충전이 계속되는데 몫이 줄어든다) · 60 MPa 89.6–90.1 % 에서 −0.5 %p 굴곡. `[해석]` 후보 둘 — ① 입자 안 농도 불균일(접촉 자리 탈리튬 · 중심 리튬 유지)이 국소 부피 불균일을 만들어 응력이 재배분 ② 스프링 반력 증가(Li 석출로 셀이 두꺼워짐 — §(b) 2). 지면으로는 못 가른다.

## 4. 분리 시험 틀([[assb-pressure-reapplication-separation-test]])에 넣으면

`Q_apparent(i, P) = θ_AM(P, N) · η(i) · Q_material(N)` 의 세 항에 이 모형의 기구를 놓으면:

| 항 | 이 모형에서 | 근거 |
|---|---|---|
| `Q_material` | **고정** — 재료 손실 · 균열 · 상 변화 · 계면층 0 | 모형 정의 |
| `θ_AM`(통째 고립) | **계산되지 않음** — 전자 연결 · 이용률 분석 0 · 이온 통째 고립(입자 둘레 전부 박리)은 정의상 가능하나 보고 0(그림 13 흰 테 입자 하나) | G5 · G8 |
| 표면 피복 `φ`(박리 몫) | **계산된다** — `φ_del(SoC; P)` 그림 9 | 식 17 · 27 |
| `η(i)` | `φ` 손실이 **여기로** 들어간다 — 남은 면 전류 집중 → BV + 입자 안 농도 분극 → 컷오프 조기 도달(§(c)) | `[재현·가정]` |

`[해석]` ① 이 모형의 "압력 연산자"(예압 50 → 70 MPa)는 `θ_AM` 이 아니라 **`φ` 를 되돌리고, 그 효과는 `η(i)` 를 통해 용량에 보인다** — 0.1 C 에서 87.18 → 94.81 % 의 +7.6 %p 는 `ΔQ_mech` 꼴이지만, 개념 페이지의 해석("기하 접촉 손실의 용량 등가 상한")과 달리 **율 의존 몫**이다 → 개념 페이지 처방 "① 저율 쌍으로 `η` 를 먼저 죽이고 ② 마지막에 재가압" 의 **순서가 왜 필요한지의 forward 표본**(율을 먼저 죽이지 않으면 `φ → η` 경로의 회복이 `θ` 회복으로 읽힌다). ② 이 모형에서는 OCV · i₀ 의 응력 의존을 무시했으므로(0.2–0.72 mV · 1.4 %) **압력은 구성상 접촉만 움직이는 손잡이** — 합성 truth 요구 R4(θ-전용 조작)의 모형판이되, 움직이는 것은 `θ` 가 아니라 `φ` 다(R7). ③ 법칙에 기억이 없으니 **압력 되돌림은 완전 가역** — 실측(39호: 50 → 0 MPa 로 풀어도 공극 불변 · 5호 이력 · 14호 +0.4 mV 오프셋)과 반대 끝이다. 설계 조건 D1–D5 중 이 모형이 주는 것은 **D5 의 모형판**(압력이 φ 하나만 움직였는지 — 구성상 그렇다)과 **D1 의 모형판**(압력 이력 — 계산은 됐을 텐데 인쇄 0).

## 5. 실험 쪽 대조 — 이 법칙이 못 내는 관측 (우리 digest 전사)

- **23호(Koerver 2017 — 이 편 [9])**: 첫 충전 뒤(충전 상태) SEM "spherical gap" · **50 사이클 뒤(방전 상태) "a similar morphology"** · 첫 방전 뒤 시편 없음(23호 G7 — "틈이 재리튬화에서 닫히는가 … 안 닫히는가를 가르는 바로 그 시편이 빠졌다"). `[해석]` 방전 상태에서 틈이 남는다는 관측이 맞다면, **구성상 가역인 이 법칙으로는 그 상태를 못 만든다**(재리튬화 → 틈 닫힘). 이 편은 [9] 를 "voids … as demonstrated" 로만 인용한다.
- **4호(Shi 2020 *JMCA* — 이 편 [11])**: FIB-SEM void 2.87 → 9.50 vol%(0 → 50 사이클) · 접촉 손실 면적 10.4 % · **300 MPa 재가압으로 2 → 80 mAh g⁻¹ 회복**(개념 페이지 `ΔQ_mech` ≈60.5 %p — 4호 digest 전사). 이 편은 [11] 을 void 문헌으로만 인용하고 **재가압 회복**(이 모형의 "압력이 박리를 줄인다" 와 가장 가까운 실측)은 쓰지 않는다.
- **58호(Asheri 2023 — 인용 0)**: 같은 박리 축의 다중 척도 대리모형 — 미세 FE 문제는 계면 손상(KKT 이력) 변수를 갖고 대리모형은 그 이력을 기억 없는 사상으로 대신하며, 셀 쪽 박리는 `a·(1 − ⟨d⟩)` 면적 감소로만 들어간다(58호 digest · 개념 전사) — **손상(비가역) 쪽 판**이다. 이 편은 이력 없는 접촉판.

---

# ★ (b) 스택 압력 — 값 · 경계조건 · 시간 이력 · 주장의 범위

## 1. 값과 경계조건 — Robin 스프링 예압 (`[재현]`)

| 기하 · 조립 | 예압 | u_k,target | k·u_k | 셀 압축 | 셀 두께 | 유효 구속 탄성률 | 표 B·I 직렬 Reuss–Voigt |
|---|---|---|---|---|---|---|---|
| 단순 | 50 MPa | 5.041 µm | 50.41 MPa | 0.041 µm | 25 µm | 30.5 GPa | 28.8–32.5 ✅ |
| 단순 | 60 | 6.049 | 60.49 | 0.049 | 25 | 30.6 | 〃 ✅ |
| 단순 | 70 | 7.057 | 70.57 | 0.057 | 25 | 30.7 | 〃 ✅ |
| 복잡 · 방전 조립 | 70 | 7.102 | 71.02 | 0.102 | 56 | 38.4 | 34.7–46.0 ✅ |
| 복잡 · 충전 조립 | 70 | 7.133 | 71.33 | 0.133 | 62 | 32.6 | 29.6–36.5 ✅ |

가정(`[재현]` 의 경계): 측면 대칭면이 측면 변형을 막는 단축 변형 · 각 층 구속 탄성률 M = E(1−ν)/[(1+ν)(1−2ν)](Li 12.5 · LPS 36.1 · NMC 235.6 GPa) · 양극층은 AM : SE 분율로 Reuss(직렬) ↔ Voigt(병렬). ⇒ **표 B·VI 은 k = 10¹³ Pa m⁻¹ 과 표 B·I 탄성률로 자기 정합**이다. 경계 형식은 **정하중도 정변위도 아니다** — 유한 강성 스프링(셀 강성 ≈1.2×10¹⁵ Pa m⁻¹ 의 1/120)이라 사실상 "정하중에 가까운 스프링" 이고, 강성 값은 "assumed".

## 2. 시간 이력 — **인쇄 0** · 같은 k 로 다시 내면 (`[재현·가정]`)

| 모의 | 음극 두께 변화(Li 석출 / 탈리 · 식 9 · g = M/ρ) | 양극 AM 부피 변화(두께 등가 · 상한) | 순 두께 | Δp = k·Δ |
|---|---|---|---|---|
| 단순 · 0.1 C 충전 → 94.8 %(contact 70) | **+1.36 µm**(Δn 1.88 pmol = 0.948 × 0.596 × c_max × 64.0 µm³ · × g / 18.0 µm² — 그림 7 벡터 Δ 1.84 pmol 이면 +1.33) | −0.05 µm | +1.31 µm | **+13 MPa**(70 → ≈83) |
| 복잡 방전 조립 · 0.5 C 충전 → 89.4 % | **+5.46 µm** | −0.18 µm | +5.29 µm | **+53 MPa**(70 → ≈123) |
| 복잡 충전 조립 · 0.5 C 방전 → 1.9 % | **−6.00 µm** | +0.23 µm | −5.77 µm | **−58 MPa**(70 → ≈12) |

가정: ① 양극 쪽 경계(Γc ∪ Γel)가 법선 방향 고정(인쇄 0 — Robin 은 Γa 에만) ② 측면 대칭으로 측면 팽창 0 ③ Li 성장 전부 두께 방향(식 9 g ⊗ g) ④ 셀이 스프링보다 120 배 단단하다(✅ 위 표) ⑤ AM 부피 변화를 두께로 그대로(SE 가 흡수하면 더 작다 — 상한). ⇒ **"70 MPa" 는 t = 0 예압의 이름**이고, 같은 모형 매개변수로는 반 사이클 동안 예압과 같은 자릿수로 움직인다 — **방전 상태 조립 셀은 첫 충전 동안 압력이 오르고**(박리를 억제하는 방향), **충전 상태 조립 셀은 첫 방전 동안 압력이 떨어진다**(그런데도 박리 0 — 활물질이 팽창하므로). 두 조립 판의 비교(초록 넷째 명제)는 **반대 방향의 압력 궤적**과 같이 움직인다(`[해석]` — 지면은 압력 궤적을 보이지 않아 갈리지 않는다).

## 3. 초록 명제의 범위 — 모의 표

| # | 기하 | 조립 | 예압 | 계면 | 율 · 방향 | 끝 | 쓰인 그림 |
|---|---|---|---|---|---|---|---|
| V1 | 두 블록 | — | — | contact(비정합) | 정상 상태 | ε_u 10⁻¹² · ε_Φ 10⁻⁹ | 3–5 |
| V2 = S2 | 단순 | 방전 | 70 MPa | contact | 0.1 C 충전 | 94.8 % · 질량 10⁻⁵ % | 7 · 8 · 9 · 10 |
| S1 | 단순 | 방전 | 70 | mesh tying | 0.1 C 충전 | 99.3 % | 8 · 9 · 10 |
| S3 · S4 | 단순 | 방전 | 60 · 50 | contact | 0.1 C 충전 | 91.3 · 87.2 % | 8 · 9 |
| C1 · C2 | 복잡(79) | 방전 | 70 | mesh tying · contact | 0.5 C 충전 | 92.5 · 89.4 % | 12 · 13 · 14 |
| C3 · C4 | 복잡(79) | 충전 | 70 | mesh tying · contact | 0.5 C 방전 | 1.7 · 1.9 % | 15 · 16 |

⇒ **"increased mechanical stack pressure during cycling mitigates delamination tendencies"** = S2–S4 세 점(단순 기하 · 입자 하나 · 요소 7,105 · 0.1 C · 첫 충전) — 방향은 세 점 단조(`[도표·벡터]` 시작 SoC 13.2 → 14.9 → 16.4 % · 끝 몫 97.1 → 90.5 → 87.8 % · 4.2 V 87.18 → 91.26 → 94.81 %) · **복잡 미세구조의 압력 축 0** · "during cycling" = 반 사이클 하나 · 70 MPa 위 · 50 MPa 아래(실용 요구치 ≤10 MPa 쪽 — 59 · 81호) 0 · 압력 축 격자 수렴 0(G3). **"would converge to … mesh tying … for increasing mechanical stack pressure"** 는 세 점 외삽 명제다.

## 4. 경계 압력 ↔ 계면 응력 — 사상이 계산된 표본

`[도표·벡터]` 경계 예압 70 MPa(압축) 아래에서 CAM\|SE 계면의 **인장 몫이 단순 기하 92.9 %(mesh tying · 끝) · 복잡 기하 79.8 %**(mesh tying · 끝)까지 오른다 — 박리는 "측면 · 입자 가운데" 부터("Due to the applied axial load, the delaminations occur mainly in lateral directions"). `[해석]` 셀 경계의 축 압축은 활물질 수축(ΔV/V −1.48 % — 선 변형 −0.5 %)을 축 방향에서만 따라가게 하고, 측면은 대칭 구속 + SE 강성(28.9 GPa)이 붙잡아 인장으로 간다. ⇒ **"스택 압력 70 MPa" 와 "계면 접촉 압력" 은 다른 양**이고 그 사상은 해상 모형이 계산해 보였다 — 원장 (태)(모형 경계 압력 ↔ 셀 압력 사상 표기)의 **사상이 실제로 계산된 첫 표본**(88호 단일 구 · 83호 상자 구속은 사상 미인쇄).

## 5. 무시한 압력 효과 — 표류를 넣어도 작다 (`[재현·가정]`)

서론의 무시 근거는 **예압 범위 20 MPa** 로 셈했다(0.2 · 0.72 mV · i₀ 1.4 %). §2 표류(±50 MPa 급)를 넣어도 OCV 쪽은 0.5–1.8 mV(1.4 V 창의 0.13 %) — **결론(무시 가능)은 그대로**이나 근거 문장의 전제("we vary the external pressure from 50 to 70 MPa")는 모의 안 압력 범위와 다르다(D16 — 조건부).

## 6. 원장 §3-b 표본 판정

- **(캐)** "stack pressure 값의 명목 ↔ 계측 표기" — **강한 표본(모형 판)**: "70 MPa" = 스프링 오프셋 목표(표 B·VI)로 정한 t = 0 예압 · 반력 이력(모형 출력) 인쇄 0 · 구속 형식 = 유한 강성 스프링(가정).
- **(해)** "운전 압력 값의 출처 층위 표기" — 약: 출처 층위는 "모형 입력(예압)" 하나로 분명하다 — 층위 혼동은 없다(우리 쪽에서 실측 운전 압력과 같은 열에 놓을 때만 문제).
- **(태)** "모형 경계 압력 ↔ 셀 스택 압력 사상 표기" — **강한 표본**: 경계 = RVE(측면 대칭) 의 Γa Robin 예압 · 계면 인장 몫 80–93 % 가 그 사상의 계산 결과(§4).
- **(하) ①** D4 "운전 중 구속 형식(정하중 / 정변위)" — **강한 표본**: 셋째 형식(유한 강성 스프링 · 강성 값 가정)이 인쇄된 모형 — 정하중 / 정변위 이분법으로는 못 적는다.

---

# ★ (c) 전기화학 결과의 귀속 — 박리 → 저항 ↑ · 전달 전하 ↓ 의 경로

## 1. 인쇄된 사슬

`[인쇄]` "the delaminated parts of the interface do not take part in the charge transfer anymore. Consequently, the current at the remaining, not delaminated interface area increases. This effect leads to a rising internal resistance of the cell, and the cutoff voltage is reached earlier." · (복잡) "This difference in the cell voltage indicates a higher internal resistance which we attribute to delaminations … leading to a more inhomogeneous concentration distribution for the contact interface model, resulting in a lower SoC at the end of the charge process." — **"내부 저항" 은 전압 차의 이름**이고, 그 저항을 BV(계면) · 이온 경로 · 고체 확산으로 나누는 계산은 지면에 없다.

## 2. 크기 분해 (`[재현·가정]` — 단순 기하 · 70 MPa · 0.1 C)

| 항 | 값 | 근거 |
|---|---|---|
| 셀 전류 밀도 | 0.295 A m⁻²(면용량 0.295 mAh cm⁻² — 측면 18.0 µm² · χ 1.0 → 0.404 창 · C-rate 기준 가정) | R9 |
| 계면 전류 밀도(박리 0) | 0.135 A m⁻²(1/8 구 표면 39.3 µm² 가정) → BV η **0.7 mV** | 식 25 · i₀ 4.98 |
| 같은 · 끝(박리 87.8 %) | 1.11 A m⁻² → BV η **5.7 mV** · (60 MPa 90.5 % → 7.3 mV · 50 MPa 97.1 % → 23 mV) | 〃 |
| 전압 차 contact 70 − mesh tying | **24 mV @ 90 % · 46 mV @ 94 % SoC** | `[도표·벡터]` 그림 8 |
| 입자 안 농도 차(끝) | 그림 10f 21,380–22,930 mol m⁻³ = χ 0.406–0.436 → **OCV 4.201 ↔ 4.135 V(67 mV)** · mesh tying(10e) 7 mV | `[재현·가정]` |
| 고체 확산 시간 r²/D | 1,042 s(17 분) ≪ 0.1 C 충전 36,000 s | 표 B·II |

⇒ `[해석]` 남은 면적의 **BV 몫은 전압 차의 1/4 이하**이고, 큰 몫은 **전류 집중이 만든 입자 안 농도 분극**이다 — 접촉 자리 근처 표면은 빨리 탈리튬되고(χ 0.406) 먼 쪽 · 중심은 리튬이 남는다(χ 0.436). 확산 시간(17 분)이 충전 시간(10 h)보다 훨씬 짧은데도 기울기가 서는 것은 플럭스가 면적 12 % 에 몰려 확산 길이가 입자 크기급으로 늘었기 때문이다.

## 3. 결손 = 입자 안에 남은 Li (`[재현·가정]`)

컷오프 4.2 V 는 **접촉 자리 표면이 OCV = 4.2 V 점(χ 0.4065)에 닿을 때** 온다(그림 10f 최솟값 χ 0.4059 → 4.2013 V). 그때 입자 평균 χ(SoC 94.9 %) = 1 − 0.949 × 0.596 = **0.4344**. 평균 − 표면 = 0.0285 → `/0.596` = **4.78 % SoC** ↔ mesh tying 대비 결손 **4.5 %p**(99.4 → 94.9 — 그림 10 표지 · 벡터 99.30 → 94.81 = 4.49 %p). ⇒ **결손은 "입자 안에 남은 Li" 와 같은 크기**다 — 용량이 사라진 것이 아니라 컷오프 순간에 꺼내지 못한 것이다. 저율 · 휴지(접촉이 남은 상태에서)면 꺼낼 수 있는 몫으로 읽힌다(`[해석]` — 모형은 그 계산을 하지 않았다 · G6).

## 4. 모형 안에서 접촉 손실과 활물질 손실이 구분되는가

- **구성상으로는 안다** — LAM 기구가 0 이고 원인은 두 계면 법칙의 차 하나다. 이 편은 "참값을 아는" forward 다.
- **관측으로는 안 갈린다(지면의 관측 범위에서)** — 지면이 보인 관측은 고정 컷오프의 정전류 곡선(0.1 C · 0.5 C)뿐이다. 그 곡선의 결손(4.5 %p · 3.1 %p)은 **용량 축척을 줄인 곡선과 같은 방향**이다: 0.1 C 곡선을 OCV 기반 용량 축척(`Q_PE`)으로 적합하면 결손이 `LAM_PE` 로 읽힐 자리다(`[해석]` — 우리가 적합하지 않았다). 다만 **모양은 같지 않다** — contact 곡선은 끝으로 갈수록 벌어지는 기울기 변화(그림 8 · 12)를 보이는데, 순수 용량 축척은 곡선을 SoC 축으로 늘인다. 그 모양 차가 적합에서 얼마나 보이는지는 율 · 잡음에 걸린다(계산 0).
- **같은 결손을 다른 원인이 만들 수 있는가** — 지면 안에서 둘: ① 압력(50 → 70 MPa 에 +7.6 %p) ② 조립 상태(방전 조립 3.1 %p ↔ 충전 조립 0.2 %p). `[해석]` 이 모형 밖으로는 `LAM_PE`(재료 손실) · 계면층 저항(i₀ ↓) · 이온 경로(κ ↓) 도 같은 방향의 컷오프 결손을 만든다 — 율 의존(η 형)이라는 서명만이 이 편 기구를 `LAM_PE` 와 가른다.

## 5. 카드 · 개념에 대응

| 카드 · 개념 자리 | 이 편 |
|---|---|
| Q1 `θ(N)` | **0** — 반 사이클 하나 · 이력 없는 법칙이라 N 축 누적이 구성상 없다(충전마다 열리고 방전마다 닫히는 "SoC 주기형"만 가능) |
| 곱 축퇴 `A·j₀` ([[assb-lampe-contact-product-degeneracy]]) | 모형은 **A 를 역학으로 계산하고 j₀ 고정** — 곱을 구성으로 푼다. 관측 쪽에서는 면적 손실이 BV 곱보다 **확산 길이(r²/D)** 로 더 크게 나타난다 → 균질 모형 적합이면 `A·j₀` 뿐 아니라 `D_eff` · `r_eff` 로도 흡수될 자리(`[해석]`) |
| 3 항 분해 ([[assb-apparent-capacity-decomposition]]) | 결손은 **`η(i)` 항**(율 · 컷오프 의존) — `θ_AM` · `Q_material` 0 |
| 합성 truth R1 · R2 · R7 ([[assb-synthetic-truth-contact-loss-requirements]]) | `θ` · `u` 0 · `φ` 만 · 고립 입자가 Li 를 붙드는 구조(R2)는 정의상 가능하나 보고 0 · R7(`φ` ↔ `u` 를 한 구조에서 같이)은 여전히 0 — 이 편은 `φ` 쪽만 |

---

# ★ (d) 27호 `1−u` 대조 — 확인하지 않는다

## 1. 27호가 건 기대

- **27호 후속 표 :381**(Sinzig 2024 [18]): "★★★ 같은 그룹의 **구성요소 사이 박리(delamination)** 확장 — resolved 모델에서 **접촉 손실을 기구로** 넣은 편 | Q1".
- **원장 행**(§1 :264): "resolved 모델의 **박리 = 접촉 손실 기구**. 27호가 재 보인 **P2D 대비 상수 오프셋 0.07 이 바로 비연결 입자 몫 `1−u`** 였다 — **그 기구의 모델 원전**".

## 2. 두 기구 대조 (27호 쪽은 27호 digest 전사)

| | 27호 Sinzig 2024 *JES* 171, 120519 | 94호 이 편 *JES* 171, 100502 |
|---|---|---|
| 무엇이 끊기나 | 입자의 **전자 연결**(집전체까지) — "the share of the particles that are electronically conductively connected" | CAM\|SE **이온 계면**(활물질-SE 면) |
| 언제 · 어떻게 | 생성 미세구조의 **정적 기하 분석**(`u = 0.93`) — 시간 변화 0 | 충전 중 역학이 **동적으로** 연다(SoC 13–16 % 부터) · 닫힐 수 있음(가역) |
| 부분 ↔ 통째 | **입자 통째** — "the concentration in the non-connected particles remains at its initial value" | **표면 일부** — 끝까지 12 %(70 MPa) · 3 %(50 MPa) 면적이 남음 · 통째 박리 보고 0 |
| 용량에 미치는 꼴 | **상수 바닥** `SOC_end ≥ 1 − u = 0.07`(율 무관) | **율 · 압력 · 조립 의존 결손**(0.1 C 4.5 %p · 0.5 C 3.1 %p · 0.2 %p) |
| 접촉 정식화 | **없음**(`contact` 0 회) | Nitsche 접촉(이 편의 주제) |
| 역학 경계 | 틀 강성 500 MPa mm⁻¹(= 5×10¹¹ Pa m⁻¹) · 예압 0(축 응력 0 → ≈3 MPa) | 스프링 10¹³ Pa m⁻¹(20 배) · 예압 50–70 MPa |
| 이 편 어휘 | — | `connect*` · `utiliz*` · `percolat*` · `inactive` 0 · `isolat*` 1(남의 단일 입자 모형) |

## 3. 판정

`[해석]` **이 편은 27호 `1−u` 의 기구 원전이 아니다** — 같은 연구실의 다른 기구(이온 계면 박리 `φ`)의 원전이다. 27호 후속 표 문구("resolved 모델에서 접촉 손실을 기구로 넣은 편")는 맞고, 원장 행이 덧붙인 "**0.07 의 기구 원전**" 은 두 기구를 한 이름("접촉 손실")으로 묶은 기대였다. 두 기구는 카드 어휘로 **`u`(통째 고립 — `θ` 쪽 · 용량 바닥) ↔ `φ`(표면 피복 — `A_eff` 쪽 · η 경로)** 이고, 합성 truth 요구 **R7 이 바로 이 둘을 별개 변수로 두라는 요구**다 — 27 · 94호를 합쳐도 R7 은 아직 0 이다(같은 구조에서 둘을 같이 계산한 편 0). 원장 행 정정 문안은 보고서 6절.

---

# ★ (e) 매개변수 표의 출처 층위 · 검증 ↔ 실험 대조 · Q4

## 1. 출처 층위 (`[인쇄]` 출처 열 → `[해석]` 층위 · 제목 기준 판정은 원전 미열람)

| 층위 | 매개변수 | 출처 | 결론 의존 |
|---|---|---|---|
| **측정 원자료(문헌)** | NMC622 부피 곡선(자료 χ 0.22–0.91) · Li E 4.9 GPa · ν 0.42 · OCV-압력 1 mV/100 MPa | [26] Koerver 2018(4차 묶음 파일 57) | **높음** — 박리 구동력. 운용 창 위쪽(χ 0.91–1.0)은 외삽 |
| 측정 기반 함수(문헌 적합) | NMC622 OCV 식 B·1 | [61] Kremer | 중 — 컷오프 위치 · 0 % SoC = 2.50 V |
| 측정(편람) | Li 밀도 · g = M/ρ | [60] CRC | 낮음 |
| **제일원리(제목 기준)** | **β-LPS E 28.9 GPa · ν 0.27** | [58] Yang 2016 "insights from first-principles calculations" | **높음** — SE 가 수축 입자를 따라가는 정도. 같은 목록의 측정 원전 [59] Sakuda 2013(황화물 18–25 GPa — 62호 digest 전사)은 **밀도에만** |
| 제일원리(제목 기준) | NMC622 E 175 GPa | [54] Sun & Zhao 2017 "Electronic structure and comparative properties" | 중 |
| 문헌 묶음 | NMC ν 0.3 | [55–57] | 낮음 |
| **남의 모형 편 입력의 평균 · 조정** | σ · D("averaged from 25") · i₀ 4.98("adapted from 25") · α_a · c_max · χ_max · κ · t_el · Li σ · Φ₀ · i₀ 8.87 · 초기 농도 | [25] Neumann 2020(모형 편) | 중–높음 — 결손 크기(η) |
| 앞 편 | NMC 밀도 5.03×10³ | [35] Schmidt 2023(본체 모형) | 낮음 |
| **가정** | **k 10¹³** · **χ0% 1.0 · χ100% 0.404** · t_el 1 · 미세구조(log-normal μ 2.3 · σ 0.05 · 79 입자 · 38 : 62) · 단순 기하 측면 | "assumed" · 본문 | **높음** — k 는 압력 이력 · χ 창은 SoC 축 · 미세구조 실현 하나 |
| 인공(검증용) | 표 I 전부 | "artificial" | — |

⇒ 표의 출처 열은 **층위 넷(측정 원자료 · 제일원리 · 남의 모형 입력 · 가정)을 같은 "Source" 칸에** 둔다. 박리 결과를 가장 크게 좌우하는 세 입력 — **SE 탄성률(제일원리) · 부피 곡선(문헌 측정 + 외삽) · 스프링 강성(가정)** — 에 민감도 · 대안 값 계산 0.

## 2. 검증(verification)은 있다 — 실험 대조(validation)는 0

- `[인쇄]` "we verify the proposed model by comparing the numerical results to an analytic solution. The model is further verified by showing that the conservation of mass is fulfilled" — 저자 낱말도 **verify** 다(`verif*` 12 · `validat*` **0**) · 정의상 맞게 쓴다(93호 D11 과 다름).
- `[재현]` 패치 시험은 우리가 다시 풀어도 맞는다(R1 · R2). 질량 보존은 그림 7 로 4 자리까지 확인(10⁻⁵ % 는 판독 불가).
- **실험 대조 0**: 셀 측정 · 영상 · 압력 · 임피던스 어느 것과도 맞대지 않는다. 초록 "**Consistent with existing literature**, the simulations demonstrate that delaminations increase the internal resistance and reduce the amount of transferred charge" 의 문헌 근거는 서론 두 문장 — "increased cell resistance due to a reduced active interface area … moderated by increasing the stack pressure as shown in, e.g. Refs. 5, 8"(**Li 음극 void** 문헌 [3–8]) · "accumulating voids at the interface of active material and solid electrolyte, as demonstrated in Refs. 9–12"(양극 void — 저항 · 용량 수치 인용 0). **양극 박리 → 내부 저항 · 전달 전하** 를 수치로 맞댄 실험 인용 0(D5). "**In contrast to experimental analyses, the presented model allows quantitative and in-depth investigations**" 의 "quantitative" 는 모형 내부 정량이다(D6).

## 3. Q4 어휘 · 판정

`[인쇄]` 어휘(본문 | 참고문헌 · NFKC 전후): `identifiab*` · `uniqu*` · `uncertain*` · `sensitiv*` · `calibrat*` · `degenera*` · `confiden*` · `reliab*` · `Fisher` · `Bayes*` · `likelihood` **0 | 0** · `validat*` **0** · `verif*` 6 → **12**(합자) · `fit*` 0 → **2**(합자 — "a fit of published data of the volume change" · 그림 17 캡션 "polynomial fit of order seven") · `estimat*` 7(벌칙 추정 · "worst-case estimate") · `error*` 3(패치 시험 · 시간 이산화) · `inverse` 1("the inverse of the mesh size") · `assum*` 14 · `parameter*` 36.

⇒ **Q4 0/94 — 여든여섯 번째 성질**: "**같은 미세구조 · 같은 입력에 계면 법칙 두 개(mesh tying ↔ Nitsche 접촉)를 돌린 차를 '박리 효과' 로 정의한 결정론적 forward — 수치 검증(패치 시험 · 질량 보존)은 정확히 하고 실험 대조 · 민감도 · 불확실도 · 접촉 격자 수렴 · 벌칙 기준값 인쇄는 0 이며, 압력 셋 · 조립 둘 · 미세구조 실현 하나 위의 결과를 일반 명제로 쓰고, 결손이 율 의존(η)인지 고립(θ)인지 가를 계산(율 스윕 · 휴지)을 돌리지 않았다 — 원인을 구성으로 아는 모형이 관측 쪽 식별성을 묻지 않은 표본**".

---

# ★ (f) Q1–Q8 — 채움표 칸 (닻 카드 수집 지침)

| Q | 이 편 | 칸 |
|---|---|---|
| **Q1 정량** | **층 하나 — 모형 출력 박리 몫 `φ_del(SoC; P)`**(단순 기하 · 그림 9 — 시작 SoC 13.2 / 14.9 / 16.4 % · 끝 97.1 / 90.5 / 87.8 % `[도표·벡터]`) · 복잡 기하 contact 박리 몫 인쇄 0(mesh tying 인장 몫 79.8 % 만) · **`θ(N)` 0/94**(반 사이클 하나 · 이력 없는 가역 법칙 → N 축 누적 구성상 0) · 측정 0 | `θ(N)` 0/94 |
| **Q2 독립관측** | **없다** — 1차 측정 0 · "면적을 아는 대조" 는 모형 안 계면 법칙 쌍(mesh tying ↔ contact)뿐 | 없다 |
| **Q3 라벨층위** | 칸 없음 · **층 하나: 출처 열 한 칸에 측정 원자료 · 제일원리(SE E) · 남의 모형 입력 평균 · 가정(k · χ 창) 이 섞임 · 표 B·V 양극 초기 농도 ↔ 그림 7 질량 수지 불일치(c_max 로만 폐합)** | 층 |
| **Q4 유일성** | **0/94 — 여든여섯 번째 성질**(§(e) 3) | 0 |
| **Q5 Li-In** | **해당 없음** — Li 금속 음극 · Φ₀ = 0 V 상수 · 기준극 · `indium` 0 | 해당 없음 |
| **Q6 압력** | **보고(모형)** — 예압 50 / 60 / 70 MPa(단순) · 70(복잡) · 구속 = 유한 강성 스프링 k 10¹³ Pa m⁻¹ "assumed" · 반 사이클 이력 인쇄 0(`[재현·가정]` +13 / +53 / −58 MPa) · 경계 70 MPa 아래 계면 인장 80–93 % | 칸 이동 없음 |
| **Q7 dead Li** | **해당 없음** — "we do not resolve the surface deposition and dissolution at the lithium metal anode"(균질 이방 성장) · 음극 박리 = 향후 과제 | 해당 없음 |
| **Q8 화학 · OCP** | **층 하나** — NMC622 OCV = 문헌 함수(식 B·1 · [61]) — `[재현]` 4.2 V @ χ 0.4065 · 0 % SoC(χ 1.0) = 2.50 V · 초기 혹 3.68 V 는 함수 모양 · 부피 법칙 = [26] 자료의 7차 적합(자료 χ ≤0.912 · 운용 창 위쪽 외삽) | 층 |

**누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 의 모형 계산 `φ` 는 1 · 2 · 27 · 37 · 56 · 58호에 같은 종류(모형이 계산한 접촉 양 — `θ` · Connectivity · `u` · `A_eff` · `φ` · `⟨d⟩`)가 있어 칸을 움직이지 않는다 · Q6 의 압력 스윕(모형)도 새 형태 아님.

---

# 어휘 집계 — 텍스트 층 · 줄 끝 하이픈 복원 · p. 1 표지 · 꼬리말 15 줄 제외 · 본문(초록 → 부록 · 캡션 · 표 포함) | 참고문헌, NFKC 앞 → 뒤

| 낱말 | 본문 | 참고문헌 |
|---|---|---|
| `identifiab*` · `uniqu*` · `uncertain*` · `Fisher` · `Bayes*` · `likelihood` · `calibrat*` · `degenera*` · `sensitiv*` · `confiden*` · `reliab*` · `identif*` · `validat*` | **0** | 0 |
| `verif*` · `fit*` · `estimat*` · `error*` · `inverse` · `optimi*` | 6 → **12** · 0 → **2** · 7 · 3 · 1(격자 크기 역수) · 2 | 0 · 0 · 0 · 0 · 0 · 1 |
| `parameter*` · `assum*` · "averaged from" · "adapted from" | 36 · 14 · 2 · 1 | 0 |
| `delamin*` · `recontact*` · `contact*` · `debond*` · `gap` | 69 · **6**(전부 틀 문장) · 86 · 1 · 4 | 2 · 0 · 14 · 0 · 0 |
| `adhesi*` · `friction*` · `void*` | 24 · 4 · 5 | 8 · 4 · 2 |
| `crack*` · `fractur*` · `damag*` · `reversib*` · `irreversib*` · `hysteres*` | **0** | 1 · 0 · 0 · 0 · 0 · 0 |
| `pressure*` · `MPa`(대소문자 · 낱말 경계) · `kPa` · "stack pressure" · `prestress*` · `spring*` · `Robin` · `stiffness` | 31 · 21 · 7 · 28 · 10 · 5 · 2 · 6 | 6 · 0 · 0 · 3 · 2 · 3 · 0 · 0 |
| `tensile` · `compressive` · `traction` | 9 · 3 · 10 | 0 · 1 · 0 |
| `capacit*` · "transferred charge" · "internal resistance" · `resistance` · `overvoltage` | 1(서론 "high-capacity anode") · 6 · 5 · 9 · 1 | 1 · 0 · 0 · 1 · 0 |
| `degrad*` · `ag(e)ing` · `cycl*` · `fade` · `loss` · `LAM` · `LLI` | **0** · 0 · 8 · 0 · 1([13] 설명) · **0** · **0** | 3 · 0 · 0 · 1 · 3 · 0 · 0 |
| `open circuit`/`OCV` · `impedanc*` · `EIS` · `DRT` · `GITT` · `state of charge`/`SoC` | 9(OCV 4 · open circuit 5) · 0 · 0 · 0 · 0 · 26(SoC 14 · state of charge 12) | 0 · 0 · 0 · 0 · 0 · 0(대소문자 구분 — 구분 없이 세면 5 = "Soc." 약어) |
| `indium`/`Li-In` · `reference electrode` · `dendrit*` · `plating` · `stripping` | 0 · 0 · 0 · 1 · 1 | 0 · 0 · 1 · 2 · 2 |
| `P2D` · `Newman` · `PyBaMM`/`DFN` · "finite element" · `homogen*` · `Butler` | 0 · 2 · 0 · 0 → **5** · 8 · 2 | 0 · 0 · 0 · 0 → 3 · 0 · 1 |
| `experiment*` · `measur*` | 3 · 5 | 2 · 1 |
| `utili[sz]*` · `connect*` · `percolat*` · `inactive` · `isolat*` | **0** · **0** · **0** · **0** · 1([23] 설명) | 0 |
| `supplement*` · "supporting information" · `appendix` · "data availab*" · `zenodo` · `video`/`movie` · `github` | 0 · 0 · 4 · 1 · 2 · 0 · 0 | 0 |
| "mesh tying" · `Nitsche` · `penalty` · `C-rate` | 24 · 5 · 12 · 9 | 0 · 6 · 0 · 0 |

⚠ 텍스트 층 한계: ① 식 · 표 B·I–B·III 의 기호는 조각으로 흩어져 셈에 영향이 없도록 낱말 패턴만 셌다 ② 그림(벡터 외곽선 · 래스터) 안 글자는 셈에 없다 — 그림 8 · 9 · 12 · 14 · 15 범례("mesh tying" · "contact" · "MPa") · 그림 10 · 13 · 16 SoC 표지 ③ 합자 `ﬁ` 83 · `ﬂ` 25 — NFKC 뒤 셈을 기준으로 쓴다.

---

# 재현 (`[재현]` — 인쇄 수치 · 식 · 그림 벡터로 우리가 계산 · 가정 · 외부 값 표시)

| # | 무엇 | 결과 | 판정 |
|---|---|---|---|
| R1 | 패치 시험 전위(표 I · T 298 K · 변형 뒤 블록 0.98 m) | η −24.71 mV · Φ_ed(계면) 1.0490 · Φ_el(계면) 0.7737 · Φ(top) 0.8717 V · 점프 0.2753 V | ✅ 그림 4 |
| R2 | 패치 시험 응력(식 4 · E 20 Pa · ν 0.3 · 단축 변형 λ 0.98) | S_xx −0.5636 Pa · **σ_xx −0.5523 Pa** | ✅ 그림 5c 색 · ⚠ 전류 부호(D2) |
| R3 | Li 성장 · 농도 | M/ρ = 1.29981×10⁻⁵ m³ mol⁻¹ · ρ/M = 7.693×10⁴ mol m⁻³ | ✅ 표 B·III · B·V |
| R4 | OCV 식 B·1 | Φ₀(0.404) 4.2057 V · **4.2 V @ χ 0.4065(SoC 99.58 %)** · Φ₀(1.0) 2.502 V · 국소 최대 3.6817 V @ χ 0.949(SoC 8.6 %) | χ100% = 4.2 V 점 ✅ · 그림 8 초기 혹 3.682 V @ 6.3 % = 함수 모양 ✅ |
| R5 | 부피 다항식(표 B·III) ↔ 그림 17 별표 24 | 잔차 RMS 0.00046 · 최대 0.00091 · f(1.0) −0.00009 · f(0.404) −0.01486 → **ΔV/V −1.478 %**(선 −0.495 %) · 0.912–1.0 외삽 단조 +0.05 % | ✅ 적합 · ⚠ 운용 창 위쪽 외삽 |
| R6 | 표 B·VI ↔ k · 표 B·I | k·u_k 50.41 … 71.33 MPa · 셀 압축 0.041–0.133 µm · M_eff 30.5 · 30.6 · 30.7 · 38.4 · 32.6 GPa ↔ Reuss–Voigt 28.8–32.5 · 34.7–46.0 · 29.6–36.5 | ✅ 자기 정합 |
| R7 | 그림 7 → 단순 기하 | 측면 18.01(음극) · 17.98(SE) µm² · AM 64.0 µm³(c₀ = c_max) = 35.6 % ✅ ↔ 표 B·V c₀ 2.10×10⁴ 이면 158 µm³ = 88 % ❌ · 양극 기울기/초기량 0.588 ↔ 창 0.596 | **D1** · G1 · G7 |
| R8 | 복잡 기하 | AM 38,000 µm³ ↔ 79 × 9.97 µm 구 41,045 µm³(+8 %) · Li 재고: 음극 Δ6 µm = 1.154×10⁻⁹ mol ↔ 양극 창 1.175×10⁻⁹ mol(98.1 % — 정확히는 6.11 µm) | ✅ "inventory constant" 근사 |
| R9 | 면용량 · 전류(`[재현·가정]` C-rate 기준 = χ 1.0 → 0.404 창) | 단순 0.295 mAh cm⁻² · 0.1 C = 0.295 A m⁻² · 복잡 1.260 mAh cm⁻² · 0.5 C = 6.30 A m⁻² | G7(정의 미인쇄) |
| R10 | 압력 표류(`[재현·가정]` §(b) 2 의 가정 다섯) | **+13 · +53 · −58 MPa** | G4 · D4 · D16 |
| R11 | 남은 면 BV 과전압(`[재현·가정]` 1/8 구 표면 39.3 µm²) | 0.7 → 5.7 mV(70 MPa 끝) · 7.3(60) · 23(50) | 전압 차 24–46 mV 의 일부 |
| R12 | 농도 분극(`[재현·가정]` det F 근사 · 색 막대 끝 = 표면 · 중심) | 그림 10f χ 0.4059–0.4361 → OCV 4.2013–4.1346 V(67 mV) · 10e 7 mV · (평균 − 표면)/0.596 = **4.78 % ↔ 결손 4.5 %p** | 결손 = 입자 안 남은 Li |
| R13 | 확산 시간 | r²/D = 1,042 s(17 분) ↔ 0.1 C 36,000 s | 전류 집중 없이는 기울기가 작다(10e) |
| R14 | OCV 응력 의존 | 20 MPa → 0.2 / 0.72 mV · 1.4 V 창의 0.05 % · 표류 ±50 MPa 면 ≤1.8 mV | ✅ 무시 결론 유지 · 전제는 예압 범위(D16) |
| R15 | log-normal 식 B·4 | e^2.3 = **9.97 µm**(중앙) · σ 0.05 → ±5 %(거의 단분산) · log₁₀ 이면 200 µm(배제) | "log" = 자연로그(D14) |
| R16 | 그림 8 · 10 · 12 · 15 끝 SoC | 99.30 / 94.81 / 91.26 / 87.18 · ≈92.3–92.6 / ≈89.5 · 1.60 / 1.86 % `[도표·벡터]` ↔ 인쇄 99.4 / 94.9 · 92.5 / 89.4 · 1.7 / 1.9 | ✅ ±0.2 %p |
| R17 | 압력 효과(50 → 70 MPa · 단순 · 0.1 C) | 4.2 V 도달 +7.6 %p · 시작 SoC +3.2 %p · 끝 박리 몫 −9.3 %p | 세 점 단조 |
| R18 | 일정 | 투고 → 수정 84 일 · 수정 → 게재 65 일 · PDF 생성 게재 하루 전 | 계산값 |

---

# 참고문헌 61 번호(인쇄 59) — 우리 축에 닿는 것 (번호는 PDF p. 15–16 목록에서 직접 확인 · 18 · 51 없음)

| [#] | 서지 `[인쇄]` | 이 편의 쓰임 | 우리 축 |
|---|---|---|---|
| [13] | H.-K. Tian, Y. Qi, *J. Electrochem. Soc.* **164**, E3512 (2017) | "a one-dimensional Newman model … contact area loss in a phenomenological manner" | **Q1 · 곱 원전** |
| [16] | Y.-q. Shao, H.-l. Liu, X.-d. Shao, L. Sang, Z.-t. Chen, *Energy* **239**, 121929 (2022) | 2D 음극 void 모형 목록 [14–19] 안 | **Q1 · Q6**(12호 ★★★ 2) |
| [20]–[22] | P. Barai … V. Srinivasan, *Chem. Mater.* **33**, 5527 (2021) · D. Bistri, C. V. D. Leo, *JES* **168**, 030515 (2021) · S. Farzanian … Q. H. Tu, "*Materials*, 6, 9615 (2023)" | "delamination of cathode active material and solid electrolyte upon cycling" (2D) | **Q1** · R8 |
| [23] | T. Zhang, M. Kamlah, R. M. McMeeking, *J. Mech. Phys. Solids* **185**, 105551 (2024) | 3D 단일 입자 박리(+ SE 균열) | 비가역 박리 |
| [24] | P. Huang, L. T. Gao, Z.-S. Guo, *Electrochim. Acta* **463**, 142873 (2023) | 해상 미세구조 · "debonding index" 만(전기화학 결합 0) | 실제 미세구조 |
| [25] | A. Neumann, S. Randau, K. Becker-Steinberger, T. Danner, S. Hein, Z. Ning, J. Marrow, F. H. Richter, J. Janek, A. Latz, *ACS AMI* **12**, 9277 (2020) | **전기화학 입력 대부분의 출처** + "delaminated interfaces … specified as input regardless of the actual mechanical state" | **Q3 · Q1 · 곱** |
| [26] | R. Koerver, W. Zhang, L. de Biasi, S. Schweidler, A. O. Kondrakov, S. Kolling, T. Brezesinski, P. Hartmann, W. G. Zeier, J. Janek, *Energy Environ. Sci.* **11**, 2142 (2018) = **4차 묶음 파일 57** | 부피 곡선(그림 17) · Li E · ν · OCV 1 mV/100 MPa | **Q1 · Q6 · Q8** |
| [9] · [10] · [11] · [12] | Koerver 2017 *Chem. Mater.* 29, 5574 = **23호** · Jung … Sun *AEM* **10**, 1903360 (2019) · Shi … Ceder *J. Mater. Chem. A* 8, 17399 (2020) = **4호** · B. Liu, S. D. Pu, C. Doerrer, D. Spencer Jolly, R. A. House, D. L. R. Melvin, P. Adamson, P. S. Grant, X. Gao, P. G. Bruce, *SusMat* **3**, 721 (2023) | 양극 void "as demonstrated" | **Q1 · Q6** |
| [3]–[8] | Wang M.J. 2019 *Joule* · Krauskopf 2019 *ACS AMI* · Kasemchainan 2019 *Nat. Mater.* · Wang S. 2021 *AEM* · Lewis 2021 *Nat. Mater.* · Hänsel & Kundu 2021 *Adv. Mater. Interfaces* 8, 2100206 | 음극 void · "moderated by increasing the stack pressure as shown in, e.g. Refs. 5, 8" | Q6 · Q7 |
| [14] · [15] · [17] · [19] | Zhang X. 2020 *CRPS* · Ahmed 2022 *JPS* · Vishnugopi 2022 *AEM* · Barai 2024 *Chem. Mater.* | 2D 음극 void 모형 목록 | — |
| [27] | M. Ganser … R. M. McMeeking, *JES* **166**, H167 (2019) | 응력 결합 BV — OCV 3.6 mV/100 MPa · i₀ 1.4 % | R4 근거 |
| [28]–[32] | Singer 2023 *Energy Technol.* 11, 2300098 · Shen 2019 *JES* 166, A3182 · **Wang M. & Sakamoto J. 2018 *JPS* 377, 7** · Billot 2021 · Haselrieder 2015 | 접착 강도 412 kPa · 30 / 540 kPa · 1.1 kPa ↔ 8 MPa · 2.3 MPa · 0.2–1.2 MPa | 접착 무시 근거 |
| [33] · [34] | Naik · Vishnugopi · Mukherjee *ACS AMI* 14, 29754 (2022) = **75호** · *Energy Storage Mater.* **55**, 312 (2023) | 유효 계면 성질 → Newman 형 | Q1 · 곱 |
| [35] | C. P. Schmidt, S. Sinzig, V. Gravemeier, W. A. Wall, *Comput. Methods Appl. Mech. Eng.* **417**, 116468 (2023) | 본체 모형 · mesh tying · 시간 수렴 · NMC 밀도 | 모형 원전 |
| [36]–[53] | 접촉 · Nitsche · 벌칙 · 가중 방법(Gitterle 2010 · Grill 2019 · Hüeber & Wohlmuth 2005 · Mlika 2017 · Popp 2009 · 2010 · Nitsche 1971 · Wriggers & Zavarise 2007 · Seitz 2018 · 4C · Fang 2018 · Cubit · Chouly 2014 · Seitz 학위논문 · Griebel 2003 · [51] 없음 · Annavarapu 2012 · Burman & Zunino 2011) | 수치 방법 | — |
| [54]–[60] | Sun & Zhao *JPCC* 121, 6002 (2017) · de Vasconcelos 2016 *EML* 9, 495 · Wu & Lu 2017 *JPCC* 121, 19022 · Xu 2017 *JES* 164, A3333 · **Yang 2016 *ACS AMI* 8, 25229**(β-Li₃PS₄ 제일원리) · **Sakuda 2013 *Sci. Rep.* 3, 2261** · CRC | 역학 입력(E · ν · ρ) | Q3 |
| [61] | L. S. Kremer … M. Wohlfahrt-Mehrens, *Energy Technol.* **8**, 1900167 (2019) | OCV 식 B·1 | Q8 |
| [1] · [2] | Janek & Zeier 2016 *Nat. Energy* 1, 16141 · 2023 *Nat. Energy* 8, 230 | 서론 배경 | — |

---

# 인용 대조

## 1. 이 편을 인용한 우리 digest — 그 쓰임

| 호 | 자리 | 그 digest 가 매단 것 | 원문 대조 |
|---|---|---|---|
| **27호** Sinzig 2024 *JES* 171, 120519 | [18] · 후속 표 :381 ★★★ | "같은 그룹의 **구성요소 사이 박리(delamination)** 확장 — resolved 모델에서 **접촉 손실을 기구로** 넣은 편 \| Q1" | ✅ **"접촉 손실을 기구로"** 는 맞다(CAM\|SE 이온 계면 · Nitsche · 식 27) · ⚠ "구성요소 사이" 는 이 편 결과에서 **CAM\|SE 하나**(음극 쪽 박리는 해상 0 — 향후 과제) · ⚠ 원장 행의 "0.07 의 기구 원전" 은 맞지 않는다(§(d)) |

**지목 수 확인**: 지목은 각 digest 의 후속 절만 센다 — 27호 후속 표(:381) 하나 **= 1 — 원장 "27 \| 1" 과 일치(정정 없음)**. 카드 :5052 · `log.md` :2103 은 27호 흡수 기록(같은 지목의 전사).

## 2. 이 편이 인용한 우리 digest — 쓰임 대조 (digest 전사 · 원 논문은 이 세션에서 다시 열지 않음)

| 이 편 [#] | 우리 digest | 이 편의 쓰임 | 대조 |
|---|---|---|---|
| [9] | **23호** Koerver 2017 *Chem. Mater.* | 양극 void "as demonstrated" | 23호: 첫 충전 뒤 "spherical gap" · **50 사이클 방전 상태 "similar morphology"** · 첫 방전 뒤 시편 0(G7) · 부피 변화 % 인쇄 0(G1) — 방전 상태에서 남는 틈은 이 편의 **가역 법칙이 못 낸다**(§(a) 5) |
| [11] | **4호** Shi 2020 *J. Mater. Chem. A* | 양극 void "as demonstrated" | 4호: void 2.87 → 9.50 vol% · 접촉 손실 면적 10.4 % · **300 MPa 재가압 2 → 80 mAh g⁻¹** — 이 편은 재가압 회복(압력 명제의 가장 가까운 실측)을 쓰지 않는다 |
| [33] | **75호** Naik 2022 *ACS AMI* | 인공 미세구조 → 유효 성질 → Newman 형 | 75호: kinetics ↔ transport 영역 지도 · `i₀` 스윕 0 — 이 편 쓰임(방법 범주)과 충돌 없음 |

**교차 참조(이 편이 인용하지 않음 · 같은 축)**: **27호** Sinzig 2024(같은 연구실 · 이 편 뒤 — `u` 기구 · 역학 경계 다름) · **58호** Asheri 2023(박리 대리모형 — 미세 FE 의 계면 손상 이력 · 셀 쪽 `a·(1−⟨d⟩)` — 손상(비가역) 쪽 판 · 이 편보다 앞서는데 인용 0) · **56호** Bielefeld 2022(해상 FEM · void 반구 — `φ` 자리) · **83호** Jiao 2023(전기-화학-역학 · SE 탄성률 · 입계 CZM — CAM\|SE 불파괴 가정 · 인용 0) · **37호** Li 2024(접촉 면적 `A_eff` ↔ `k` 항등) · **1 · 2호**(해상 구조 · `θ` · Connectivity) · **59 · 81 · 88호**(스택 압력 · 요구치 — 이 편 압력 50–70 MPa 는 실용 요구치 밖) · 4차 묶음: **파일 57 Koerver 2018 *EES* = [26]** 하나(나머지 12 편 인용 0 — 원장의 Shao 행 파일 63 *JES* 169, 080529 은 이 편 [16] *Energy* 239, 121929 과 **다른 편**).

---

# 곱 축퇴 처방 — 일흔일곱 번째 적용 ([[assb-lampe-contact-product-degeneracy]])

**부분 적용 — 모형 안 대조쌍(mesh tying ↔ contact)이 "면적을 아는 대조군" 의 계산판이다. 관측 쪽 입력(R · C · Ea · 율 스윕)은 0.**

| 처방 단계 | 필요한 입력 | 94호 | 판정 |
|---|---|---|---|
| 1단계(16 · 23호) | `R` · `C` 같이 | EIS · 이중층 0(BV 계면에 정전용량 항 없음) | ❌ |
| 2단계(18 · 25호) | 면적을 아는 대조군 | **계면 법칙 쌍** — 같은 미세구조 · 같은 입력 · 면적만 다름(mesh tying = 전 면적 · contact = 역학이 정한 면적 · 그림 9 로 `φ_del` 앎) — **모형 안에서만** | ⚠ 계산판 |
| 3단계-a · b(19호) | `Ea` · `C` 상한 | 298 K 한 점 · C 0 | ❌ |
| 4단계(20 · 24호) | 시간 영역 · 같은 시편 | 같은 "시편"(미세구조)에 두 법칙 — 정전류 곡선만 · 휴지 · 율 0 | ⚠ |
| 율 스윕 · `J^T J` | — | 0.1 C(단순) · 0.5 C(복잡) — 같은 기하 두 율 0 | ❌ |

**곱 문장**(`[인쇄]` → `[해석]`):
- ① 식 (27) — 박리 면 플럭스 0 = 곱 `A·j₀` 의 **A 를 역학이 정하고 j₀ 는 고정**(i₀ 4.98 A m⁻² · 응력 의존 무시 1.4 %) — 모형 안에서 곱은 **구성으로 풀린다**.
- ② "the current at the remaining, not delaminated interface area increases" — 면적 손실 → 같은 전류 · 작은 면적 → 국소 전류 밀도 ↑ 의 곱 문장. `[재현·가정]` 그 몫(BV)은 끝에서 ≈6 mV 이고 전압 차(24–46 mV)의 큰 몫은 **고체 확산 분극**(67 mV 퍼짐) — 면적 손실이 `A·j₀` 하나로 접히지 않고 **확산 길이(r²/D)** 쪽으로도 번진다. 37호 원형 모델의 항등(`A_eff` ↔ `k` 정확한 곱)은 이 3D 해상 모형에서 **부분적으로만** 성립한다(56호 모델 명제와 같은 방향).
- ③ 4.5 %p(0.1 C) · 3.1 %p(0.5 C) 결손 = 고정 컷오프에서 **용량 축척처럼 보이는 결손** — `LAM_PE` 와 곱으로 읽힐 자리(카드 물음의 forward 표본 · 조건: 유한 율).

**⚠ 이것이 곱을 푼 것은 아니다** — 모형은 A 를 **알고** 시작한다. 지면의 관측(전압 곡선)에서 A 와 j₀(또는 A 와 D)를 가르는 계산은 0 이고, mesh tying 짝은 실험에 없는 반사실이다. 후보 메모(처방 표로 올리지 않음 · 결정 대기): **"계면 법칙 쌍(mesh tying ↔ contact)은 2단계 '면적을 아는 대조군' 의 모형판이다 — 합성 truth 에서 R4 · R7 검사에 쓸 수 있으나 움직이는 것은 `φ`(표면)뿐이고(`θ` · `u` 0), 면적 손실의 관측 서명은 BV 보다 고체 확산 쪽(율 · 휴지 의존)에 있다."** 처방 표 새 줄 0.

---

# 보류 결정 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(냐) — 이 편이 주는 근거 (결정 안 함)

| # | 결정 (요약) | 94호 근거 | 세기 |
|---|---|---|---|
| **(하)** | 압력 되돌림 설계 조건 보강 — ① D4 운전 중 구속 형식(정하중 / 정변위) | **셋째 구속 형식이 인쇄된 모형** — Robin 스프링 k 10¹³ Pa m⁻¹("assumed" · 셀 강성의 1/120 — 정하중에 가까운 스프링) · 예압은 오프셋 목표(표 B·VI) · `[재현·가정]` 같은 k 로 반 사이클 압력 표류 +13 / +53 / −58 MPa(이력 인쇄 0) — 정하중 / 정변위 이분법으로는 못 적는다 · ② 회복 시간 곡선 0 · ③ 원시 압력 = 예압 목표뿐 | **강** |
| **(캐)** | "stack pressure" 값의 명목 ↔ 계측 표기 | 모형 판 — "70 MPa" = t = 0 예압(스프링 오프셋으로 정함) · 반력 이력(모형 출력) 인쇄 0 · 초록 "**during cycling**" 은 반 사이클 하나 | **강** |
| **(태)** | 모형 경계 압력 ↔ 셀 스택 압력 사상 표기 | **사상이 계산된 첫 표본** — RVE(측면 대칭) Γa 예압 70 MPa(압축) 아래 CAM\|SE 계면 인장 몫 92.9 %(단순) · 79.8 %(복잡) `[도표·벡터]` · 박리는 축 하중 때문에 측면부터("Due to the applied axial load, the delaminations occur mainly in lateral directions") — 경계 압력 ≠ 계면 접촉 압력 | **강** |
| **(치)** | 모형 결론 옆 "배제 가정" 표기 | 초록 · 요약의 셋 명제("stack pressure … mitigates" · "adhesion … not … significant" · "assembled … shrinks … higher delamination risk")가 조건 없이 — 배제 가정: 접착 0 · 마찰 0 · 탄성 SE · 균질 SE(void · 바인더 · 탄소 0) · OCV · i₀ 응력 무관 · t₊ 1 · Li 균질 성장 · 반 사이클 하나 · 미세구조 실현 하나(σ 0.05 · 거의 단분산) · 단순 기하 입자 하나 · 예압 셋 · 격자 수렴 0 | **강** |
| **(세)** | 인쇄 매개변수 표의 재풀이 폐합 검사 | 패치 시험(표 I) ✅ 폐합(η −24.7 mV · σ_xx −0.552 Pa) · 표 B·VI ✅(Reuss–Voigt) · **질량 수지(그림 7) ❌ — 표 B·V 양극 초기 농도로는 AM 88 % · c_max·χ0% 로만 36 %**(D1) | **강** |
| (이) | 모형 값 인용 규칙 — 모형 입력이 측정과 같은가 | SE 탄성률 = 제일원리 28.9 GPa([58] — 제목 기준) · 같은 목록의 측정 원전 [59](황화물 18–25 GPa — 62호 전사)는 밀도에만 · 인공 미세구조(log-normal σ 0.05 · 79 입자 겹침) · 전기화학 입력 = 남의 모형 편([25]) 평균 · 조정 | 중 |
| (노) | 양극 부피 변화의 층위 선택 | [26] 의 "measured data of the volume change" 를 2차 입자 등방 성장으로 그대로(1차 입자 무작위 배향 가정) — 층위(격자 ↔ 입자) 미기재 · 운용 창 ΔV/V −1.48 % `[재현]` · 자료 χ ≤0.912 · 위쪽 외삽 | 중 |
| (차) | PyBaMM 면적 / j₀ 노브 분리 forward | 면적을 역학으로 계산 · j₀ 고정인 해상 forward 에서 면적 손실의 전압 몫은 BV(≈6 mV)보다 고체 확산 분극(≈67 mV 퍼짐)이 크다 `[재현·가정]` — 면적 노브를 BV 에만 거는 균질 forward 는 이 경로를 못 낸다(`[해석]`) | 중 |
| (키) | 합성 truth R8(`θ(N)` 형태) 후보 메모 | 이력 없는 가역 접촉 법칙은 N 축 누적을 구성상 못 만든다 — 충전마다 열리고 방전마다 닫히는 "SoC 주기형" 이 셋째 형태 후보(모형) · N 축은 비가역 항(접착 손상 · SE 소성 · 크리프 · 균열 — [23] · 58호 계면 손상 변수)에서만 | 중 |
| (저) | 65호 "첫 충전 상한" 검사 격상 | 첫 충전(방전 조립 3.1 %p) ↔ 첫 방전(충전 조립 0.2 %p) 비대칭이 **조립 상태(역학 기준 부피)** 에서 생기는 모형 표본 — 통째 고립 없이(η 형) · 비대칭을 `θ` 상한으로 읽기 전 조립 상태 · 압력 궤적 표기가 필요 | 중 |
| (냐) | 모형 결론의 회고 인용 — 조건 복원 | 이 편 초록 · 요약이 조건(단순 기하 · 0.1 C · 세 점 · 반 사이클) 없이 일반화(D12) · 우리 원장 행이 27호 `u` 기구와 묶은 회고 기대(§(d)) | 중 |
| (투) | (차) forward 에 "Wa 영역 선결" | 면적 손실의 관측 서명이 옴 ↔ 동역학 비(Wa)가 아니라 고체 확산 쪽에 선다 — 영역 판정에 확산 길이 축이 빠지면 놓치는 경로 | 약 |
| (러) | 합성 truth `θ → LAM_PE` 결합 항 | 반대 방향 표본 — 이 모형은 LAM 기구 0 · 접촉 손실은 η 형 결손으로만 | 약 |
| (두) | `θ` 판정의 시간 궤적 조건 | 휴지 · 저율에서 회수될 η 형 결손의 모형 표본(`[재현·가정]` 4.78 ↔ 4.5 %p) — 모형은 그 궤적을 계산 안 함 | 약 |
| (제) | 모형 "일치" 의 잔차 표기 | "Consistent with existing literature" — 수치 대조 0 · 근거 문헌은 Li 음극 void | 약 |
| (거) | Wang · Sakamoto 2018 · Sharafi 2016 요청 | [30] Wang & Sakamoto 2018 이 이 편에서는 접착 강도 최악값(8 MPa — Li\|LLZO)의 출처 — 같은 편이 압력 가닥 밖 자리(접착 상한)로도 쓰인다 | 약 |
| (애) | CAM 부피 분율의 기준 표기 | 두 상(AM : SE) 기준 · 공극 0 가정이라 전체 기준과 같다 — 기준이 명시된 표본(36 : 64 · 38 : 62) | 약 |
| (비) | SE(CAM) 입도 값 표기 | 모형 입력 분포 log-normal μ 2.3 · σ 0.05(d̄ = d/1 µm · 중앙 9.97 µm `[재현]`) · 측정 연결 0 | 약 |
| (체) | 평형(OCV) 곡선의 출처 층위 | 문헌 적합 함수(식 B·1 · [61]) · χ 창 경계는 "assumed" · 0 % SoC = 2.50 V(창 밖) `[재현]` | 약 |
| (무) | `j₀(x)` 모양 선택지 | i₀ 상수(농도 비의존 — "exchange current density factor" 이름만 · D13) 모형 표본 | 약 |
| (마) | (결정 · 반영됨) 합성 truth 요구 개념 | '닿는 논문' 첫 이름 "Schmidt 2024" 가 이 편으로 흡수 — 개념 페이지 `A_eff` 자리 · R4 · R7 · R8 출처 열에 94호를 더했다(구조 불변) | 반영 |
| (바) | (결정 · 반영됨) 압력 되돌림 설계 조건 D1–D5 | D5(압력이 무엇을 움직였나 — 모형에서는 φ 하나) · D1(압력 이력 — 모형에서도 인쇄 0)의 모형판 — 개념 페이지에 94호 절(구조 불변) | 반영 |

나머지 — (라)(사) 결정 · 반영됨, 그 밖의 글자는 **근거 0**(Li-In · 기준극 · 노화 사이클 · DRT · EIS · LLI · 실측 압력 시계열 · 프로토콜 비교 · 비선형 진단 · 식별 도구 축이 이 편에 없다). **결정 안 함.**

## 새 판단 거리 (셋 — 글자는 호출자가 붙인다)

1. **모형 '스택 압력' 의 구속 강성 · 사이클 중 압력 이력 표기** ((하)① · (캐) · (태) 의 모형판으로 묶어도 됨) — 모형 편의 "stack pressure X MPa" 를 카드 · 개념 · 합성 truth 로 옮길 때 경계 형식(정하중 · 정변위 · 스프링 — 강성 값과 그 출처)과 X 가 t = 0 예압인지 · 반 사이클 평균 · 끝값인지, 그리고 압력 이력(모형 출력이 없으면 인쇄 매개변수로 낸 `[재현·가정]` 표류)을 값 옆에 적게 할지 — 94호: Robin k 10¹³ Pa m⁻¹ "assumed" · 예압 50–70 MPa(표 B·VI) · 이력 인쇄 0 · `[재현·가정]` +13 / +53 / −58 MPa · 같은 코드의 27호는 k 5×10¹¹ · 예압 0.
2. **'접촉 손실 → 용량 손실' 모형 결과의 결손 꼴 표기 (η 형 ↔ θ 형)** — 모형이 "박리 · 접촉 손실이 전달 전하를 줄인다" 고 할 때 카드 Q1 · 3 항 분해 · 합성 truth 로 옮기기 전에 율 · 컷오프와 결손의 꼴(접촉 자리 표면 고갈로 입자 안에 남은 Li — 휴지 · 저율 회수 가능 / 통째 고립 — 회수 불가 / 재료 손실)을 확인해 적고, 율 스윕 · 휴지 계산이 없으면 `θ_AM` · `LAM` 근거로 세지 않게 할지 — 94호: 0.1 C 결손 4.5 %p ≈ (χ 평균 − 표면)/0.596 4.78 % · BV ≈6 mV ↔ 전압 차 24–46 mV `[재현·가정]` · 율 스윕 0.
3. **한 편을 다른 편 현상의 '모형 원전' 으로 지목할 때의 기구 층위 확인** ((냐) 의 지목판으로 묶어도 됨) — 원장 · 카드에서 지목 이유가 "X 의 기구 원전" 일 때, X 의 기구 층위(전자 비연결 `u` · 이온 계면 박리 `φ` · 공극 · 계면층 · 재료 손실)와 지목된 편의 기구 층위를 맞춰 보고, 다르면 도착 뒤 지목 이유를 고쳐 적게 할지 — 94호: 원장 행 "27호 `1−u` 0.07 의 기구 원전" ↔ 이 편 `φ`(부분 · 가역 · 이온) · 27호 `u`(통째 · 정적 · 전자 · 접촉 정식화 0).

---

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** | 표 B·V 양극 초기 농도 **2.10×10⁴ mol m⁻³**(= χ 0.405 · 충전 상태) ↔ 단순 기하 · 그림 11a 는 **완전 방전 상태에서 시작**(χ0% 1.0 → 5.19×10⁴) — 그림 7 의 3.32 pmol 은 c_max 로만 AM 36 % 와 맞는다(2.10×10⁴ 이면 88 %) `[재현]` | 표 B·V ↔ 표 B·II · B·IV · 그림 7 |
| **D2** | 그림 5a · b 전류 **−0.10 A m⁻² · 화살 −x** ↔ 그림 4 의 전위가 +x 로 감소 · 식 21–22(i = −σ∇Φ · −κ∇Φ)면 +x — 출력 부호 규약 미기재(크기 일치) | 그림 4 ↔ 5 |
| **D3** | "**recontacting**" 6 회(초록 1 · 서론 2 · 계면 정의 1 · 결과 머리 1 · 요약 1 — 정보 사전 키워드에도) ↔ 재접촉을 보인 결과 서술 0 · 유일한 흔적(그림 9 · 70 MPa · 93.5 → 94.5 % SoC 에서 −1.9 %p `[도표·벡터]`)은 무언급 | p. 2 · 4 · 6 · 12 ↔ 그림 9 |
| **D4** | 초록 "increased mechanical stack pressure **during cycling**" ↔ 압력 = t = 0 예압(스프링) · 모의는 반 사이클 하나 · 반력 이력 인쇄 0 | p. 2 ↔ 식 36 · B·6 · 표 B·VI |
| **D5** | 초록 "**Consistent with existing literature**, … delaminations increase the internal resistance and reduce the amount of transferred charge" ↔ 서론의 근거 문장은 Li 음극 void 문헌([3–8] · 압력 완화 [5,8])과 양극 void 관찰([9–12] — 저항 · 용량 수치 인용 0) | p. 2 |
| **D6** | 초록 "In contrast to experimental analyses, the presented model allows **quantitative** and in-depth investigations" ↔ 실험 대조 0(`validat*` 0) — 정량은 모형 내부 | p. 2 |
| **D7** | 표 B·IV 단순 기하 "lateral dimensions **—**" ↔ 표 B·VI 이 단순 기하의 목표 변위 셋을 인쇄 · 결과 넷이 단순 기하 — 기하 재구성 불가(G1) | 표 B·IV ↔ B·VI |
| **D8** | 참고문헌 **18 · 51 번이 목록에 없다**(17 → 19 · 50 → 52 — 렌더 확인 · 앞 항목 끝 " ." 조판 흔적) ↔ 본문 "Refs. 14–19" · "Dolbow and Harari show in Ref. 51" | p. 15–16 ↔ p. 2 · 13 |
| D9 | [22] "*Materials*, 6, 9615 (2023)" — 권 · 쪽이 저널명과 안 맞아 보임(원전 확인 필요) | p. 15 |
| D10 | 그림 9 캡션 "**delaminated** cathode-solid electrolyte interface area share … of the different mechanical interface models" ↔ mesh tying 점선은 인장 몫(박리 0 — 본문이 따로 설명) | 그림 9 ↔ p. 9 |
| D11 | 서지 연도: [10] Jung "(2019)" ↔ *AEM* **10**(원장 2020) · [61] Kremer "(2019)" ↔ *Energy Technol.* **8**(원장 · 27호 2020) · [17] Vishnugopi "(2022)" ↔ *AEM* **13**(90호 2023) — 온라인 연도로 읽힌다 | p. 15–16 |
| D12 | 초록 "half-cells assembled in an initial state from which the active material shrinks in volume upon first charge **or discharge**" ↔ 계산 = NMC622(충전 때 수축) 셀 둘 · 70 MPa · 0.5 C · 첫 반 사이클씩 — 방전 때 수축하는 재료 0 | p. 2 ↔ p. 10–12 |
| D13 | 표 B·II i₀ "exchange current density **factor**" ↔ 식 (25) 상수 i₀(농도 의존 항 0) | 표 B·II ↔ 식 25 |
| D14 | 식 B·4 "log" — 밑 미표기 · `[재현]` 자연로그(μ 2.3 → 9.97 µm)로만 입자 지름 10 µm 와 맞음(log₁₀ 이면 200 µm) | p. 13 |
| D15 | 질량 보존 모의(70 MPa · 0.1 C · contact)와 압력 절의 contact 70 MPa 가 같은 모의인지 명시 0 — 그림 7 끝 95.1 % ↔ 그림 8 94.81 % `[도표·벡터]` 로 같은 모의로 읽힘 | p. 7 ↔ p. 8 |
| D16 | 서론 무시 근거 "we vary the external pressure from 50 to 70 MPa, i.e. by 20 MPa" ↔ 같은 모형 매개변수(k)로 반 사이클 압력 표류 +13 … −58 MPa `[재현·가정]` — 근거 문장의 전제가 모의 안 압력 범위와 다르다(결론 "무시 가능" 은 유지 — ≤1.8 mV) | p. 3 ↔ 식 36 · 표 B·I |

---

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. **카드 물음의 forward 표본 — 원인을 아는 모형에서 표면 접촉 손실(`φ`)이 고정 컷오프 곡선에 '용량 결손' 처럼 보인다(유한 율).** 결손의 정체(입자 안 남은 Li — `[재현·가정]` 4.78 ↔ 4.5 %p)는 율 · 휴지 서명으로만 `LAM_PE` 와 갈린다. `degradation-degeneracy/` 가 합성 truth 로 채점하는 "맞는 곡선 ≠ 맞는 성분 분할" 의 ASSB 접촉판에서, **접촉 손실을 BV 면적 노브로만 넣은 truth 는 이 확산 경로를 못 낸다**(우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본 — 여기 옮기지 않는다).
2. **R7 의 두 변수가 같은 연구실 두 편에 따로 있다** — `u`(27호 — 전자 비연결 · 정적 바닥)와 `φ`(94호 — 이온 계면 박리 · 동적 · 가역). 같은 코드(4C)라 원리상 한 구조에서 둘을 같이 낼 수 있는 계보지만, 두 편 모두 그 계산은 0 이다.
3. **압력 축의 표기 규칙이 모형에도 필요하다** — "X MPa" = 예압인지 이력인지 · 구속 형식(정하중 · 정변위 · 유한 강성) · 경계 압력 ≠ 계면 접촉 압력(70 MPa 아래 인장 80–93 %).
4. **truth 입력의 층위** — 박리를 좌우하는 SE 탄성률(제일원리) · 부피 곡선(문헌 측정 + 외삽) · 스프링 강성(가정)을 그대로 가져가면 그 층위가 truth 의 숨은 가정이 된다.

---

# 후속 후보 (원전 우선 — 지목 수는 위키 digest 의 후속 절 grep 으로 센 값)

| 등급 | 서지 (PDF 목록 번호) | 지목 (후속 절) | 왜 | 축 |
|---|---|---|---|---|
| ★★★★ | **Barai P., Rojas T., Narayanan B., Ngo A.T., Curtiss L.A., Srinivasan V. 2021** — *Chem. Mater.* 33, 5527 ([20]) | 53 · 75 · 83 · **94** = **4** (재지목) | 사이클 축 박리 모형(원장 ★★★★) — 이 편이 "delamination of cathode active material and solid electrolyte upon cycling" 2D 모형 셋의 첫째로 인용 · 이 편의 가역 · 반 사이클 법칙과 대비되는 N 축 판 | Q1 · R8 |
| ★★★ | **Tian H.-K., Qi Y. 2017** — *J. Electrochem. Soc.* 164, E3512 ([13]) | 12 · 81 · **94** = **3** (재지목) | "a one-dimensional Newman model … contact area loss in a phenomenological manner" — `A_eff` 곱 자리의 원전 · 이 편이 해상판의 대조로 지목 | Q1 · 곱 · Q6 |
| ★★★ | **Shao Y.-q., Liu H.-l., Shao X.-d., Sang L., Chen Z.-t. 2022** — *Energy* 239, 121929 ([16]) | 12 · **94** = **2** (재지목 · **지목 누락 보충**) | 12호 후속 ★★★ 2("접촉 면적 손실이 압력의 함수로 모델에 들어간 첫 후보")인데 원장 행 0 · 원장의 Shao 행(파일 63 · *JES* 169, 080529)과 **다른 편** · 쓰임이 갈린다(12호: 1D Newman 접촉 면적 매개변수 · 압력 / 94호: Li 음극 void 2D 모형 목록) | Q1 · Q6 |
| ★★★ | **Neumann A., Randau S., Becker-Steinberger K., Danner T., Hein S., Ning Z., Marrow J., Richter F.H., Janek J., Latz A. 2020** — *ACS AMI* 12, 9277 ([25]) | 27 · 53 · 56 · 73 · **94** = **5** (재지목) | 이 편 전기화학 입력 대부분의 원전("averaged / adapted from 25") · "delaminated interfaces … specified as input regardless of the actual mechanical state" — 박리를 입력으로 둔 해상 모형 | Q3 · Q1 · 곱 |
| ★★★ | **Liu B., Pu S.D., Doerrer C., Spencer Jolly D., House R.A., Melvin D.L.R., Adamson P., Grant P.S., Gao X., Bruce P.G. 2023** — *SusMat* 3, 721 ([12] — 제목 "The effect of volume change and stack pressure on solid-state battery cathodes") | **94** = 1 (새) | 양극 부피 변화 × 스택 압력의 **실험** — 이 편 압력 명제와 가장 가까운 실측 후보(제목 기준 · 미열람) | Q1 · Q6 |
| ★★★ | **Jung S.H., Kim U.-H., Kim J.-H., Jun S., Yoon C.S., Jung Y.S., Sun Y.-K. 2019/2020** — *Adv. Energy Mater.* 10, 1903360 ([10] — 인쇄 연도 2019) | 38 · 87 · **94** = **3** (재지목) | 양극 void "as demonstrated" — 원장 행의 원전 라벨 "Ionically loosened / isolated"(`A_eff` ↔ `θ` 두 노브) — 이 편의 `φ` 와 `u` 구분을 실측 쪽에서 | Q1 |
| ★★★ | **Koerver R. 외 2018** — *Energy Environ. Sci.* 11, 2142 ([26]) = **4차 묶음 파일 57** | 4 · 27 · 33 · 37 · 41 · 53 · 59 · 73 · 75 · 81 · 82 · 87 · **94** = **13** (재지목 · 도착 · 처리 대기) | 이 편 부피 법칙 자료(그림 17) · Li E · ν · OCV 1 mV/100 MPa 의 원전 — 자료 층위(격자 ↔ 입자) · 운용 창 위쪽 자료 유무 확인(G9) | Q1 · Q6 · Q8 |
| ★★ | **Schmidt C.P., Sinzig S., Gravemeier V., Wall W.A. 2023** — *Comput. Methods Appl. Mech. Eng.* 417, 116468 ([35]) | **94** = 1 (새) | 본체 모형 원전(체적 식 · mesh tying · "the error decreases as the time discretization is refined") — 이 편 · 27호의 공통 바탕 | 모형 |
| ★★ | **Zhang T., Kamlah M., McMeeking R.M. 2024** — *J. Mech. Phys. Solids* 185, 105551 ([23]) | **94** = 1 (새) | 단일 입자 박리 + SE 균열 3D — 비가역(손상) 판 — R8 N 축 · 이 편 가역 법칙의 대조 | Q1 · R8 |
| ★★ | **Naik K.G., Vishnugopi B.S., Mukherjee P.P. 2023** — *Energy Storage Mater.* 55, 312 ([34]) | **94** = 1 (새) | "Heterogeneities affect solid-state battery cathode dynamics" — 해상 → 유효 계면 성질 → Newman — 접촉 손실이 균질 모형 어느 노브로 가는지 | Q1 · 곱 |
| ★★ | **Bistri D., Di Leo C.V. 2021** — *J. Electrochem. Soc.* 168, 030515 ([21]) | 83 · **94** = **2** (재지목) | 2D 양극 박리 · 다입자 화학-역학 | Q1 |
| ★★ | **Sakuda A., Hayashi A., Tatsumisago M. 2013** — *Sci. Rep.* 3, 2261 ([59]) | 71 · 86 · **94** = **3** (재지목) | 황화물 SE 측정 탄성률(18–25 GPa — 62호 전사) — 이 편은 밀도에만 쓰고 E 는 제일원리 28.9 GPa — 박리 결과를 좌우하는 입력의 층위 | Q6 · Q3 |
| ★★ | **Wang M., Sakamoto J. 2018** — *J. Power Sources* 377, 7 ([30]) | 46 · 61 · **94** = **3** (재지목) | 접착 강도 1.1 kPa ↔ 8 MPa(Li\|LLZO) — 이 편 접착 무시 검사의 "최악값" 출처 · 원장 (거) | Q6 |
| ★★ | **Hänsel C., Kundu D. 2021** — *Adv. Mater. Interfaces* 8, 2100206 ([8]) | **94** = 1 (새) | "stack pressure dilemma" — 이 편 "moderated by increasing the stack pressure as shown in, e.g. Refs. 5, 8"(초록 '문헌과 일치' 의 실측 다리 · 음극) | Q6 · Q7 |
| ★★ | **Kasemchainan J. … Bruce P.G. 2019** — *Nat. Mater.* 18, 1105 ([5]) | 46 · 48 · 75 · **94** = **4** (재지목) | 같은 "moderated by … stack pressure" 문장의 다른 다리 | Q7 · Q6 |
| ★ | **Kremer L.S. 외 2019/2020** — *Energy Technol.* 8, 1900167 ([61] — 인쇄 연도 2019) | 27 · 75 · **94** = **3** (재지목) | 이 편 OCV 식 B·1 원전(`[재현]` 4.2 V @ χ 0.4065) — 27호 OCV 와 같은 출처 | Q8 |
| ★ | **Ganser M., Hildebrand F.E., Klinsmann M., Hanauer M., Kamlah M., McMeeking R.M. 2019** — *J. Electrochem. Soc.* 166, H167 ([27]) | **94** = 1 (새) | 응력 결합 BV — 이 편이 OCV · i₀ 응력 의존을 무시한 근거(3.6 mV/100 MPa · 1.4 %) — 합성 truth R4(압력이 접촉만 움직이나)의 근거 | Q6 · R4 |
| ★ | **Singer C., Kopp L., Aruqaj M., Daub R. 2023** — *Energy Technol.* 11, 2300098 ([28]) | **94** = 1 (새) | 복합양극 접착 412 kPa — 이 편이 "가장 관련" 이라 한 값 · 층 접착인지 입자 계면인지 | Q6 |
| ★ | **Yang Y., Wu Q., Cui Y., Chen Y., Shi S., Wang R.-Z., Yan H. 2016** — *ACS AMI* 8, 25229 ([58]) | **94** = 1 (새) | β-Li₃PS₄ 탄성률 제일원리(28.9 GPa · 0.27) — 박리 결과를 좌우하는 입력의 원전 | Q3 |
| ★ | **Huang P., Gao L.T., Guo Z.-S. 2023** — *Electrochim. Acta* 463, 142873 ([24]) | **94** = 1 (새) | X선 현미 단층 재구성 미세구조 위 "debonding index" — 실제 미세구조판(전기화학 결합 0) | Q1 |
| ★ | **Farzanian S. … Tu Q.H. 2023** — "*Materials*, 6, 9615" ([22] — 저널명 확인 필요 · D9) | **94** = 1 (새) | 복합양극 기계 열화 · 박리 2D | Q1 |
| ☆ | Ahmed 2022 *JPS* 521, 230939([15]) · Vishnugopi 2022 *AEM* 13, 2203671([17] — 90호 ☆) · Barai 2024 *Chem. Mater.* 36, 2245([19]) · Wang S. 2021 *AEM* 11, 2100654([6]) | 행 없음 | 음극 void 모형 · 관찰 목록 | — |
| ☆ | Shen 2019 *JES* 166, A3182([29]) · Billot 2021([31]) · Haselrieder 2015([32]) | 행 없음 | 접착 값(다른 계 · 액체) | — |
| ☆ | Sun & Zhao 2017 *JPCC* 121, 6002([54]) · Wu & Lu 2017([56]) · Xu 2017 *JES* 164, A3333([57]) · CRC([60]) | 행 없음 | NMC · Li 물성 | — |
| ☆ | [36]–[53] 접촉 · Nitsche · 벌칙 · 가중 방법 · 4C · Cubit | 행 없음 | 수치 방법 | — |
| ☆ | Janek & Zeier 2016 *Nat. Energy* 1, 16141([1]) · 2023 *Nat. Energy* 8, 230([2]) | 행 없음 | 서론 배경 | — |

**원장 행이 있으나 재지목 안 함**(이 편 쓰임이 목록 인용이거나 축 밖): [3] Wang M.J. 2019 *Joule*(81 \| 1) · [4] Krauskopf 2019 *ACS AMI*(10 · 46 · 75 · 81 \| 4) · [14] Zhang X. 2020 *CRPS*(81 묶음 행) · [55] de Vasconcelos 2016 *EML*(77 \| 1 — 이 편은 ν 0.3 묶음 인용).

**흡수된 편(교차 — 지목 아님)**: [9] 23호 Koerver 2017 · [11] 4호 Shi 2020 *JMCA* · [33] 75호 Naik 2022.

**4차 묶음 13 편과의 관계**: 이 편은 **파일 57 Koerver 2018 *EES* 하나**를 인용한다([26] — 재지목 → 13). 나머지 12 편(Danilov 2011 · Firouz 2020 · Bielefeld 2023 · Khalik 2021 · Lu 2022 · Raijmakers 2020 · Kim 2019 · Deng 2021 · Danilov & Notten 2008 · Xie 2008 · Shao 2022 *JES*(파일 63) · Ansah 2021) 인용 0 — [16] Shao 2022 *Energy* 는 파일 63 과 다른 편.

**지목 누락 둘** — [16] **Shao 2022 *Energy* 239, 121929**(12호 후속 ★★★ 2 · 원장 행 0 — 이 편이 재지목) · [7] **Lewis J.A. … McDowell M.T. 2021 *Nat. Mater.* 20, 503**(14호 후속 ★ · 19호 후속 ★★ "operando X-ray tomography 로 void ↔ interphase ↔ 전기화학" · 원장 행 0 — 이 편은 서론 음극 void 목록이라 재지목 안 함). 등급 칸 없는 옛 후속 표에 있던 편(Neumann 2020 — 4 · 39 · 54호 · Janek & Zeier 2023 — 36호)은 "누락" 으로 단정하지 않는다(93호 처리와 같음).

---

# 이 digest 가 주장하지 않는 것

1. **이 모형이 틀렸다고 하지 않는다** — 검증 둘(패치 시험 · 질량 보존)은 우리 재현과 맞고, 박리 → 전달 전하 감소의 방향은 저자 사슬대로 계산에 선다. 걸린 것은 실험 대조 0 · 압력 이력 미보고 · 결론의 범위(세 점 · 반 사이클 · 실현 하나)다.
2. **압력 표류(+13 / +53 / −58 MPa)가 이 모의에서 실제로 일어났다고 단정하지 않는다** — 인쇄 매개변수(k · 두께 · 농도 · g)와 가정 다섯(양극 쪽 경계 고정 등 — 인쇄 0)으로 낸 `[재현·가정]` 이다. 모형 출력(반력 이력)은 지면에 없다.
3. **결손이 저율 · 휴지에서 회수된다고 단정하지 않는다** — 크기 일치(4.78 ↔ 4.5 %p)와 BV ↔ 농도 분극 분해까지가 `[재현·가정]`(색 막대 끝값 = 표면 · 중심 가정 · det F 근사)이고, 모형은 그 계산을 하지 않았다.
4. **27호 `1−u` 가 틀렸다고 하지 않는다** — 그 바닥은 27호 모형의 전자 비연결 몫으로 27호 digest 판정 그대로다. 이 편이 그 기구의 원전이 아니라는 것까지다.
5. **접착이 중요하다고 하지 않는다** — 저자 검사(0–8 MPa 인장 몫 < 0.7 %)는 그들 가정 안에서 맞다. 걸린 것은 인용 접착 값의 계면 종류(복합양극 층 접착 · Li\|LLZO)가 CAM\|SE 입자 계면과 다르다는 것(`[해석]`)까지다.
6. **단순 기하가 1/8 구라고 단정하지 않는다** — 측면 ≈18 µm² · AM ≈64 µm³ 의 자릿수 일치까지다(자름 방식 미인쇄 · 1/8 구를 18 µm² 정사각에 자르면 61 µm³ — 같은 자릿수일 뿐).
7. **Shao 2022 *Energy* 가 파일 63(*JES* 169, 080529)과 다른 편이라는 판단은 서지(저널 · 권 · 쪽)로만** 한다 — 두 원문 다 미열람이고, 12호의 "Shao — 접촉 면적 매개변수" 문장이 어느 편 내용인지는 원문으로만 닫힌다.
