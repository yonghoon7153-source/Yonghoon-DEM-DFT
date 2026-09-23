---
title: "Bielefeld, Weber, Janek 2020 — Modeling Effective Ionic Conductivity and Binder Influence in Composite Cathodes for All-Solid-State Batteries (ACS Appl. Mater. Interfaces 12, 12821-12833)"
source_url: local-upload/19._Modeling_effective_ionic_conductivity_and_binder_influence_in_composite_cathodes_for_all-solid-state_batteries.pdf + 19._Sup_Modeling_effective_ionic_conductivity_and_binder_influence_in_composite_cathodes_for_all-solid-state_batteries.pdf (SI)
source_url_note: "본문 13 쪽(그림 6 · 표 1 · 식 19 · 참고문헌 70) + SI 6 쪽(LaTeX · Fig. S1-S5 · 표 S1-S2). 모델 편 — 새 측정 0. 크로퍼 자동 13 장(제외 1 — SI Fig. S1 벡터). Read 6 장 + Fig. 5b · 5d 확대 + 극한식 쪽 렌더, 안 본 것은 digest §13. 원자료는 커밋하지 않는다."
source_doi: 10.1021/acsami.9b22788
source_license: "© 2020 American Chemical Society — 오픈액세스 표기 없음"
pdf_sha256: 779dbc592e97d732ee0a26804237b478561e234d96a47ab7312ab59d209293eb
si_sha256: a28973145a0faea8ac32bd268ec9a5719016b54b9e199c91a481b776138567e4
ingested: 2026-09-23
sha256: dd82929e516a01b6a1c5b5e39d01fca0fc8fd6ca089ccad4bdc575b2e3934f44
---

# 수집 목적

`assb` 섹션 **57호**. 큐 **58번** — 2차 묶음(큐 40~59, 원장 §1 상단 순서)의 **열아홉째 편** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md`) 행 ★★★: "1호 직계 속편. 24호의 **14 % void 가정과 τ 정의의 출처** — 01호와 24호를 잇는 유일한 고리". 지목 **3 회**: 15호 Rahman 2024 ref [28](요약 한 문단) · 24호 Stavola 2023 ref 41 · SI ref 5("14 % void" · "point contacts … non-intuitive") · 53호 Ren 2023 ref [151b](한 문장 — 바인더 분포 → 활성 면적). 56호(Bielefeld 2022)는 이 편을 ref 25 로 인용하고, 56호 digest 가 **"pore(void) 문턱 → 저항 급증"(14호 ref [69] 가 Bielefeld 2022 에 붙인 문장)의 실제 출처 후보**로 이 편을 넘겼다.

이 digest 의 1순위 물음: **(1) 'pore 문턱' 귀속 — 이 편에 void 분율 스윕과 유효 전도도(또는 이용률)의 급변 문턱이 인쇄돼 있나 (2) 유효 이온 전도도 모델(굴곡도 · Bruggeman 지수 · 퍼콜레이션)과 실험 대조 — 곱 `σ⁰·ε/τ²` 를 구조가 푸는가, 55호 실측(void 13.2 % · `τ` 1.27/1.74 · LCO/SE 0.616)과의 관계 (3) 바인더는 이온 경로를 막는가(수송 곱) 아니면 CAM–SE 접촉을 가리는가(`φ`, 37호 `A_eff·k`) — 카드 `θ` 의 어느 자리인가 (4) 01호 `p_c` 의 계보 — 01 → 이 편 → 56호(반례)에서 `p_c` 가 어떻게 바뀌나.**

A. Bielefeld*, D. A. Weber, J. Janek* (3 인, * 교신 2) —
**"Modeling Effective Ionic Conductivity and Binder Influence in Composite Cathodes for All-Solid-State Batteries"**,
*ACS Appl. Mater. Interfaces* **2020**, **12**(11), 12821–12833, doi `10.1021/acsami.9b22788`.
`[인쇄]` Received 2019-12-17 · Accepted 2020-02-25 · Published 2020-02-25 · "© 2020 American Chemical Society" — 오픈액세스 표기 없음. Research Article.
소속: **JLU Giessen 물리화학연구소**(Bielefeld · Janek; Janek 은 + LaMa) · **Volkswagen AG, Group Innovation, Wolfsburg**(Bielefeld 겸직 · Weber). 자금: `[인쇄]` "The authors thank **Volkswagen AG** for the financial support" · BMBF FESTBATT(03XP0177A, J.J.). 감사: Philipp Minnmann(JLU) 논의 · **Math2Market**(GeoDict 개발사) "smart script to accurately meet the binder content".
**계보 겹침**: 01호(Bielefeld · Weber · Janek 2019 *J. Phys. Chem. C*)와 **저자 셋이 똑같다** — 이 편 ref 21("our recently published conduction cluster analysis and percolation study"). 56호(Bielefeld 2022)는 이 편의 후속(56호 ref 25). 55호 Hlushkou 2018 = 이 편 ref 26 · SI ref S3. 22호 Strauss 2018 = ref 23. 23호 Koerver 2017 = ref 29. 04호 Shi 2020 은 **다른 Shi** — ref 28 = Shi, Tu, Tian, Xiao, Miara, Kononova, Ceder 2020 *AEM* 10, 1902881(입도 최적화). ⚠ 이 편의 "Nam et al. 2018"(ref 25) = Nam · Oh · Jung · Jung *JPS* 375, 93(건식 ↔ 슬러리 비교) — **41호 Nam 2018 *JMCA*(3전극)와 다른 논문**이다. 큐 59(Asheri 2023)는 이 편보다 늦다(인용 0).

본문 PDF **13 쪽**(그림 6 · 표 1 · 식 19 · 참고문헌 70) · SI PDF **6 쪽**(LaTeX · Fig. S1–S5 · 표 S1–S2 · 참고문헌 7). PDF sha256 은 frontmatter(본문 `pdf_sha256` · SI `si_sha256`). ⚠ 두 PDF 모두 ACS 내려받기 바닥글(내려받은 기관 · 날짜 2026-09-23)이 쪽마다 찍힌 판 — 같은 논문의 다른 내려받기와 해시가 다를 수 있다. 원자료는 커밋하지 않는다.

> ⚠ **표기**: `[인쇄]` = 지면에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 읽은 값(figure-read ≈) ·
> `[재현]` = 지면의 수치로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. 표시가 없는 서술은 원문이 실제로 말한 것이다.
> ⚠ **이 편은 모델 편이다.** GeoDict 합성 미세구조 + 정상 상태 전도(EJ-heat 풀이기). 새 측정 0. 실험 대조는 **남의 값 둘**(Kato 2018 `σ_eff` 한 점 · Nam 2018 GITT 면적 비). "바인더가 면적을 X % 깎는다" 류는 전부 **모델 명제**다.
> ⚠ **기호**: 이 편의 `ϕ`(NFKC 로 `φ`)는 **void 부피분율**이다 — 카드 · 29 · 39 · 56호의 `φ`(표면 피복 분율)와 **다른 양**이다. 아래에서는 혼동을 피해 void 는 **`φ_void`**, 피복은 카드대로 `φ` 로 쓴다. `ε_SE` = 전체 부피 기준 SE 분율(void 포함 분모), `v_SE` = 고체 부피 기준, `ε_SE = (1 − φ_void)·v_SE`(`[인쇄]`). `τ²` = 굴곡도 **인자**(55호 `τ`, 24호 `τ²`, 이 위키 [[assb-tortuosity-factor-effective-conductivity-split]] 의 `τ²` 와 같은 양). `A_spec,a` = 01호의 활성 계면 면적(전자 클러스터 AM ↔ 이온 클러스터 SE 사이 면적 ÷ 전극 부피, 10⁵ m⁻¹).

---

# 판정 (먼저)

> ★★★★ **'pore 문턱' — 이 편에도 없다. 귀속은 '출처 불명'.** 이 편은 계보에서 **void 부피 스윕 → 유효 이온 전도도**를 계산한 **유일한 Bielefeld 편**이지만(Fig. 4), 그 스윕은 **세 점**(`φ_void` 5 · 10 · 20 %, d = 5 µm)이고 결과는 **단조 · 완만**하다 — `[인쇄]` "a higher void space significantly lowers the ionic conductivity, with **2-fold** higher effective conductivities for 5% void space, compared to 20%". 낱말: `threshold` **0**(SI 0) · `surpass` **0** · `critical` 4(전부 일반론) · `abrupt` 2 · `steep` 2 — **넷 다 AM 분율 축**("Above a volume ratio of 65:35 AM:SE, the ionic tortuosity rises abruptly" · "Toward higher AM loading … the tortuosity factor steeply increases" · 바인더 "more AM than … 70:30 AM:SE+B … the conductivity drops abruptly"). ⇒ 14호 `[인쇄]` "a prior study[69] indeed revealed an **abrupt resistance increase when the pore volume increases and surpasses a threshold**" 의 세 요소(pore 부피 축 · 문턱 · 저항 급증)가 **한 편에 같이 있는 곳은 01 · 56 · 58 셋 어디에도 없다**:
>
> | 편 | void/공극 축 스윕 | 문턱 | 저항 · 전도도 |
> |---|---|---|---|
> | **01호 Bielefeld 2019** | ✅ 공극률 43 → 3 %(70/30 고정, Fig. 9) | ✅ **퍼콜레이션 판정** — `[인쇄]` "high porosities **above 34 %** are accompanied by ionically and electronically isolated regions" · "Down to 21 % … electronic limitation is still present" | ❌ 계산 0("not explicitly treated") |
> | **58 = 이 편 (2020)** | ✅ `φ_void` **5 · 10 · 20 %** 세 점(Fig. 4) | ❌ `threshold` 0 — 급변은 **AM 분율 축**에서만 | ✅ `σ_eff` · `τ²` — `[도표]` 50:50 에서 0.78 / 0.65 / 0.43 mS cm⁻¹ |
> | **56호 Bielefeld 2022**(14호 [69] 가 가리킨 편) | ❌ 피복률 · void 크기만 | ❌ `threshold` 0 | ❌ 전도도 계산 0 |
>
> `[해석]` 14호 문장은 **01호의 공극률 퍼콜레이션 문턱(≈34 %, 이용률 기준)과 이 편의 void → `σ_eff`(단조 ×2)를 합친 서술**이거나, 이 편 AM 축 급변의 재서술로 읽힌다 — 어느 쪽이든 **인용된 56호가 근거가 아니고, 이 편도 문장 그대로의 근거는 아니다.** 원장의 "1호 `p_c` 의 실험판" 은 세 편 모두 모델이라 성립하지 않는다(실험 0).
>
> ★★★★ **유효 전도도 모델 — 곱 `σ⁰·ε/τ²` 은 구성상 풀려 있고, `τ²` 는 `σ_eff` 의 이름표다.** 정상 상태 포아송(식 (10))을 복셀 미세구조(0.2 µm voxel⁻¹ · 80 × 80 × 140 µm)에서 풀어 `σ_eff` 를 얻고, 식 (11) `τ² = σ⁰·ε_SE/σ_eff` 로 **나눈다**. 입력 `σ⁰` 2.7 mS cm⁻¹(Table S1) · `ε_SE` 는 구조가 안다 ⇒ `τ²` 는 새 정보가 아니라 `σ_eff` 의 환산이다(`[재현]` Fig. 4 50:50 · `φ_void` 5 %: 2.7 × 0.475 / 0.78 = **1.64** ↔ `[도표]` ≈1.65 ✓). **Bruggeman 판정**: 식 (18) `τ² = ε^−1/2` 는 `[인쇄]` "significantly underestimates … 4-fold larger" · 수정식 (19) `τ² = γ ε^−α` 적합 `[인쇄]` α ∈ [2.02, 1.21] · γ ∈ [0.32, 0.67](Fig. 2 범례: 3 µm `0.325·ε^−2.018` · 15 µm `0.668·ε^−1.213`) — `[재현]` `σ_eff/σ⁰ = ε^(1+α)/γ` 이므로 **전도도 지수 3.02 · 2.21**(고전 1.5). 저자 판정: `[인쇄]` "these parameters **do not offer any further scientific insight**".
>
> ★★★ **실험 대조 — 한 점, 그리고 모르는 void 를 손잡이로.** Kato 2018(LCO:LGPS:아세틸렌블랙, SEM 단면에서 재구성): `[인쇄]` 모의 `σ_eff` **0.68 mS cm⁻¹** · `τ²` 2.29 ↔ Kato 0.73 · 2.47. `[인쇄]` "no information on the void space … is provided … we **assumed 15 %**". `[재현]` `σ⁰` 3.2(LGPS, 본문 §3.3 값)면 3.2 × 0.85 × 0.571 / 0.68 = **2.28** ✓, Kato 2.47 은 void 를 뺀 `ε` 0.571 로 나눈 값(`[재현]` 2.50) — 저자가 짚은 대로 `τ²` 차는 `ε` 규약이다. **곱으로는 0.213 ↔ 0.228(7 %)**. 그런데 같은 지면 Fig. 4 가 `φ_void` 5 → 20 % 에서 `σ_eff` 를 **×1.8–2.2** 움직인다 — **검증의 일치 폭(7 %)이 가정한 손잡이의 영향(×2)보다 훨씬 작다** ⇒ 이 한 점은 void 가정과 모델을 **같이** 맞춘 것이지 모델만 검증한 것이 아니다(`[해석]`). 오차 척도 · 반복 배열 · 오차 막대 **0**(`error` 1 = Nam GITT 인용문).
>
> ★★★ **55호와의 관계(비교용 — 판정 근거 아님).** 이 편은 55호를 **void 기본값의 출처**로 쓴다(`[인쇄]` Table S1 "15 % similar to Hlushkou et al." · 본문 "pressed electrodes with 13.2% residual porosity") — **55호 D7 "void 13.2 % = 수지 + 잔류 void" 가 두 번째로 넘어왔다**(56호에 이어). 55호 표적과 **같은 조성 · 같은 양은 없다**: 55호 LCO/SE 0.616(= AM:SE ≈38:62) ↔ 이 편 NCM 구형 · 최저 AM 은 `φ_void` 5 % 에서 ≈42:58. `[도표]` 가장 가까운 점 — `φ_void` 10 % · 45:55 `τ²` ≈1.75 · 5 % · 42:58 ≈1.5 ↔ 55호 1.74(13.2 %) · 1.27(무공극): 크기 차수는 같다. **void 효과의 로그 분할**: `[재현]` 이 편 50:50 에서 `φ_void` 5 → 20 % 의 `σ_eff` 비 1.81 = `ε` ×1.19 · `τ²` ×1.52 → 로그 몫 **`τ²` 70 %** ↔ 55호 가상 치환 **59 %** — "void 는 `ε` 만이 아니라 기하를 바꾼다" 가 합성 구조에서도 같은 방향. 전도도 지수 `[재현]` 이 편 2.2–3.0(구형 AM · 다면체 SE · `φ_void` 15 %) ↔ 55호 함의 1.89(실측 구조).
>
> ★★★★ **바인더의 자리 — 경로와 접촉 둘 다, 그리고 `θ_AM` 은 구성상 불변(모델 명제).** 바인더는 AM 입자 사이 **메니스커스 다리**(SI: AM 팽창 → 수축 반복, "binder bridge", 젖음성 높음)로 넣고, 부피는 **SE 에서 뺀다**(`[도표]` Fig. 5a 위 축 50:47:2.5 · 70:23:7.0). 이온 · 전자 절연체(Table S1 에 바인더 전도도 칸 없음 — G6). 결과(`V(B):V(AM)` 0.05 · 0.10, d = 5 µm, `φ_void` 15 %):
>
> | 자리 | 바인더 효과 | 수 |
> |---|---|---|
> | **`θ_AM`**(AM 이용률 — 카드 `θ`) | **불변** — `[인쇄]` "Owing to the mechanism of binder generation that was used on an existing AM microstructure, the utilization level of the AM is **not affected**" | `[도표]` Fig. 5b 세 곡선 겹침 |
> | **`θ_SE`**(SE 이용률 — 이온 퍼콜레이션) | 70:30 위에서 감소 — `[인쇄]` "the binder impedes and blocks ionic pathways … not all SE particles contribute" | `[도표]` ε_AM 68 에서 무 ≈98 · 0.05 ≈91 · 0.10 **≈55 %** |
> | **`A_spec,a`**(활성 계면 — 37호 `A_eff`/카드 `φ` 자리) | 감소 — `[인쇄]` "reduced by at least **17 %** … and **29 %** … low AM … high AM … **43 and 82 %**" | `[도표]` Fig. 5d 0.05: ≈83 → ≈56 % · 0.10: ≈71 → ≈20 % |
> | **`σ_eff` · `τ²`**(수송 곱) | 감소 · 증가 — 70:30 에서 `[인쇄]` `τ²` **10**(1.8 wt% NBR) · **6.4**(0.9 wt%) ↔ 무바인더 **4.2** | `[도표]` ε_AM 68: `σ_eff` 0.045 / 0.0098 / **3.3 × 10⁻⁴** mS cm⁻¹ · `τ²` 10 / 38 / **≈800** |
>
> ⇒ 37호 틀로(`[해석]`): 바인더는 **`ε_p`(`LAM_PE`) 자리가 아니다** — 구성상 `θ_AM` 을 건드리지 않고, **`A_eff·k` 자리(면적)와 `κ_eff` 자리(수송)를 한 손잡이로 같이 깎는다.** 그리고 `A_spec,a` 감소 안에 **표면 피복**과 **SE 고립**(`θ_SE`)이 섞여 있다 — `A_spec,a` 는 "퍼콜레이션하는 두 클러스터 사이 면적" 이라 SE 가 고립되면 그 면적도 빠진다. 이 편은 둘을 가르지 않았다. `[재현]` 이 편의 `τ²` 는 **순수 SE 분율**로 나눈 값이다(ε_AM 68 · 0.10: 순수 SE 로 835 ↔ SE+바인더로 1391, `[도표]` ≈800) — 그러므로 `τ²` 증가는 SE 부피 손실이 아니라 **경로 차단**의 몫이다.
>
> ★★★★ **01호 `p_c` 의 계보 — 01 에서 태어나고, 이 편에서 말없이 실려 가고, 56호에서 손으로 덮인다.** 이 편은 `[인쇄]` "We use the AM microstructures generated in our previous work" — 01호 배열을 재사용한다. `[도표]` Fig. 5b AM 이용률은 ε_AM **49 → 50 vol%** 에서 ≈22 → ≈63 % 로 뛴다(40 vol% ≈3 %) — `[재현]` 01호 식 (8) `p_c(5 µm)` = 49.3 vol% 와 같은 자리. 그런데 이 편은 그것을 **한 번도 말하지 않는다**(`threshold` 0 · `p_c` 0) — 오히려 `[인쇄]` "we suppose that electronic conduction is **not the limiting factor** because conductive carbon will be introduced". 전자 퍼콜레이션을 탄소로 치운다고 해 놓고, **`A_spec,a`(Fig. 5c)는 탄소 없는 AM 클러스터로 계산**해 ε_AM < 49 에서 ≈0 이다(D8). 이 모순이 Nam 대조를 오염시킨다(아래). 56호에서 같은 연구실은 01호 `p_c` 가 실험 셀(42 vol%)과 어긋나자 고립 입자를 손으로 옮겨 `θ = 1` 로 만들었다. ⇒ 계보: **01 `p_c(d)` 출력 → 58 상속(무언) + 이온 쪽 새 무릎(바인더 `θ_SE`) → 56 반례 · 수작업 강제**.
>
> ★★★ **Nam 2018 대조 — 면적 비 대 GITT 곱.** Fig. 5d 에 Nam 2018(NCM622:LPSCl:C65:NBR, 슬러리 ↔ 건식)의 GITT 유래 "접촉 면적" 비를 겹쳤다. `[인쇄]` "for the small (70 wt % ≃ 48 vol %) and the large AM fraction (85 wt % ≃ 69 vol %), the data and model match quite well" · "intermediate … better contact than predicted" · "GITT … subject to **large errors**". `[도표]` 삼각형 **4 개**(본문은 조성 셋): ε_AM ≈41 → ≈69 % · ≈52 → ≈91 % · ≈59 → **≈73 % 와 ≈45 %** 둘 ↔ 0.10 곡선(Nam 바인더 ≈10 vol% 에 대응) ≈71 · ≈63 · ≈53. (i) "작은 AM 일치"(41 vol%)는 **`p_c` 아래**라 모델 `A_spec,a` 가 바인더 · 무바인더 모두 ≈0.1 × 10⁵ m⁻¹(봉우리의 2–4 %)인 자리의 **거의 0 ÷ 거의 0** 이다 — Nam 전극은 C65 가 들어가 전자적으로 연결돼 있다(D7) (ii) ε_AM 59 의 두 점 중 하나(≈73)는 0.05 곡선 위에 있고 본문은 언급하지 않는다(D6) (iii) `[해석]` GITT "면적" 은 `D_app ∝ D·(A/V)²` 에서 `D` 불변을 가정해 뽑은 이름표다(29 · 31호 구조) — 대조의 실험 쪽이 **곱 자체**다.
>
> **채움표: ≈20.0 → ≈20.0 (새 칸 0).** Q1 **층 하나(모델 명제)** — "바인더는 `θ_AM` 불변 · `A_spec,a`(피복 + SE 고립) · `σ_eff` 를 한 손잡이로 깎는다; void 는 `σ_eff` 를 ×2(5 → 20 %) — `θ(N)` 0/57" · Q2 없음 · **Q3 층 하나** — "유도된 `τ²`(σ⁰ε/σ_eff 이름표) + 가정 void 15 %(55호 수지 + void 13.2 % 출처) + 남의 GITT 면적 비(자기 경고 'large errors', `p_c` 아래 점)" · **Q4 0/57 — 마흔아홉 번째 성질 "적합 자유도의 무의미를 인쇄했다(α · γ 'do not offer any further scientific insight') — 그러면서 자기 검증은 모르는 void 를 15 % 로 놓은 한 점 일치(7 %)로 했고, 그 void 가 `σ_eff` 를 ×2 움직인다는 것을 같은 지면이 보인다"** · Q5 해당 없음(음극 0) · Q6 없음(`pressure` 0 · `MPa` 0) · Q7 해당 없음 · Q8 없음(NCM811 196 mAh g⁻¹ · 4.76 g cm⁻³ 는 C-율 환산용, OCP 0). 곱 축퇴 처방 **마흔 번째 적용**(§10) — 새 줄 "**한 공정 손잡이가 두 곱을 같이 깎을 때 — 면적 비와 수송 비를 같은 모델에서 따로 보고, 실험 쪽 GITT '면적' 은 곱으로 적는다**".

---

# 0. 원문에 없어서 확인이 필요한 것

| # | 없는 것 | 왜 필요한가 |
|---|---|---|
| G1 | **void 생성 절차** — void 가 SE 안에 흩어지는지, AM–SE 경계에 붙는지 | 경로 효과 ↔ 접촉 효과의 몫이 void 위치에 달렸다. 이 편은 01호 절차를 따른다고만 하고(`[인쇄]` "particle arrangements … generated in GeoDict"), `[도표]` Fig. S4 모델 단면에서 void(흰색)는 **SE 안의 잔 조각**으로 보인다 |
| G2 | **배열 반복 수 · 오차 막대** | Fig. 1–5 는 조성마다 점 하나. 01호는 8–10 배열에 `p − p_c` = 1 vol% 에서 ±32 % 폭을 인쇄했다 — 이 편 AM 이용률 무릎(49 → 50 vol%)은 바로 그 폭 안이다 |
| G3 | **검증 계산의 `σ⁰`**(LGPS) | Table S2 에 없다. `[재현]` 3.2 mS cm⁻¹(§3.3 에 Kato 2018 값으로 인쇄)면 `τ²` 2.29 가 재현된다 |
| G4 | **아세틸렌블랙 · 바인더의 전도도 배정** | Table S1 은 SE · AM 둘뿐. 검증 모델 AB 4.8 %(고체 기준)는 이온 절연으로 둔 듯하나 미인쇄 |
| G5 | **SE 밀도**(wt% ↔ vol% 환산) | `[재현]` Fig. 5a 70:26.5:3.5 · NBR 0.9 wt% 는 `ρ_SE` ≈1.97 g cm⁻³ 를 요구. 지면에 없다 |
| G6 | **바인더 전도도 · 계면 조건** | "ionic and electronic insulators" 는 서론의 일반론이다. 모델 바인더의 `σ` · AM/바인더 · SE/바인더 계면 규칙이 없다 |
| G7 | **접촉 저항 40 Ω cm² 의 적용 방식과 효과** | `[인쇄]` AM/SE 계면에 Braun 2018 추정값을 걸었다. `[재현]` AM 을 지나는 경로는 5 µm 에서 5 × 10⁻⁴ cm ÷ 10⁻⁷ S cm⁻¹ = **5000 Ω cm²** — 접촉 저항(40)보다 두 자릿수 크다 ⇒ 이 파라미터는 `σ_eff` 에 사실상 무력하다(`[해석]`). 이온은 SE 로만 간다 |
| G8 | **Nam 2018 삼각형 4 개의 정체** | 본문은 조성 셋(작 · 중 · 대)을 말한다. ε_AM ≈59 의 두 점(≈73 · ≈45)이 무엇인지 없다 |
| G9 | **SE 입자 크기 고정(3 µm)의 영향** | 01호 G3 그대로 — "AM 크기 효과" 는 크기비 `d_AM/d_SE` 1 → 5 와 교락. 저자도 `[인쇄]` "equivalent with a high AM/SE particle size ratio" |
| G10 | **모델 두께 140 µm 와 전류밀도 추정의 두께(100–300 µm)** | §3.3 은 `τ²` 를 두께와 무관한 재료 상수로 쓴다. 01호의 유한 크기 경고(얇은 체적에서 클러스터 부풂)가 `τ²` 에도 있는지 미검사 |

---

# 1. 서지 · 낱말 지문

규칙: NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문(참고문헌 전, 쪽 바닥 내려받기 줄 제외); SI 는 괄호(참고문헌 전).

| `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **0** (SI 0) | **0** (SI 0) | **0** | 0 | 0 | **0** | 0 | **0** | 0 | **1** (SI 0) | **0** (SI 0) |

- NFKC 변경 본문 **245 자**(`ﬀ` 111 · `ﬁ` 69 · `ﬂ` 40 · `ﬃ` 13 · `ϕ` 12 — void 기호 `ϕ` → `φ`) · SI **36 자**(`µ` 25 · `ﬀ` 4 · `¨` 3 · `ﬁ` 2 · `ﬂ` 1 · `Ω` 1) — **열 변화 0**. 소프트 하이픈 0 · 줄끝 하이픈 본문 31 곳 · SI 2 곳(이으면 `binder` 72 → 71 — 열 변화 0).
- ⚠ ACS 조판 추출이 식 (1)–(19)를 글자 조각으로 흩고, `ﬀ` 합자 뒤 공백을 잃는다("trade-oﬀbetween"). 식은 쪽 렌더로 확인(식 (11) · (15) · (17) · 극한식).
- `contact loss` 1 = 서론 "the volume change … may lead to **contact loss** upon cycling" — 일반론, 이 편 계산과 무관.
- 보조(본문 / SI): `void*` **49 / 5** · `porosit*` 6 / 0(정의 · 문헌 인용) · `pore` 1("pore size scales with particle size") · **`threshold` 0 / 0 · `surpass` 0** · `abrupt` **2**(둘 다 AM 분율 축) · `steep*` **2**(AM 축 · 바인더) · `critical*` 4(일반론) · `percolat*` 11 / 0 · `tortuos*` 70 / 1 · `Bruggeman` 20 / 0 · `binder` 72 / 14 · `contact` 7 / 2 · `active surface` 9 · `interface area` 7 · `utiliz*` 9 · `isolat*` 1(01호 정의 인용) · `fit*` 7(전부 Bruggeman · 멱법칙) · `error` 1(Nam GITT) · `validat*` 1 · `experiment*` 10 · `Hlushkou` 2 / 1 · `resistance` 4 / 1(접촉 저항 · IR 강하) · `pressure` **0** · `cycl*` 4 · `degrad*` 2 · `aging` 2 · `uniqu*` 0 · `sensitiv*` 0 · `Nam` 4.
- `[해석]` 식별성 낱말 자리를 **"these parameters do not offer any further scientific insight"**(수정 Bruggeman) · **"the calculation of the tortuosity factor is ambiguous"**(Kato 대조) · **"the Bruggeman equation(s) should be used cautiously"** 가 차지한다 — 적합 자유도와 `ε` 규약의 모호함을 **인쇄로 인정**한 계보(56호 "Achilles heel" 의 3 년 전).

---

# 2. 방법 (§2, SI Table S1 · Fig. S1–S3)

- **출발점** `[인쇄]`: 01호의 "conduction cluster analysis and percolation study" — GeoDict 로 AM(구형 · 겹침 없음 · 2차 입자 NCM) + SE(볼록 다면체 · **겹침 허용** — `[인쇄]` Young 률 ≈25 GPa · 연성 반영). 두 가정: (1) SE 는 단일 이온 전도체 · 전자 전도 무시 (2) AM 이온 전도는 SE 의 10⁻⁴ 배라 무시(퍼콜레이션 분석에서).
- **이 편의 확장**: `[인쇄]` "we target at modeling electrodes manufactured in a casting process: we suppose that electronic conduction is not the limiting factor because conductive carbon will be introduced … our focus therefore lies on ionic conduction" · 바인더 추가 · 유효 물성 계산. 단 `[인쇄]` "the study on the active material size, the void space, and the electrode composition are **not restricted** to electrodes manufactured in a casting process".
- **굴곡도 정의** 식 (1) `D_eff = ε/τ² · D_bulk` · 식 (3) `σ_eff = ε_SE/τ² · σ_bulk,SE` · 식 (4) 기하 `τ = Δl/Δx`(최단 경로 — "underestimates") · **식 (11) `τ² = σ_bulk,SE · ε_SE / σ_eff`**(흐름 기반 `σ_eff` 에서 역산). `[인쇄]` "the term porosity can be ambiguous for ASSB electrodes" — void `φ_void` · 전체 기준 `ε_SE` · 고체 기준 `v_SE` 를 구분.
- **흐름 기반 계산**(§2.2): 전도 텐서 중 `σ₃₃`(집전체 수직)과 `σ₁₃` · `σ₂₃` 만. GeoDict **EJ-heat** 풀이기(Wiegmann · Zemitis 2006 — 조화 평균 + 계면 명시 점프)로 식 (10) `∇·(−σ∇φ) = 0` 를 양끝 전위차 경계로 푼다. `[인쇄]` "Different from our percolation study, an ionic conductivity is assigned to **both** components" — AM(NCM532, Amin · Chiang) `σ` = 10⁻⁴ mS cm⁻¹ · SE(LPSCl) **2.7 mS cm⁻¹**(Kato 2016) · **AM/SE 접촉 저항 40 Ω cm²**(Braun 2018 이 Kato 2016 EIS · SEM 에서 추정) · ΔU 1 V · 0.2 µm voxel⁻¹ · 80 × 80 × 140 µm(Table S1).
- **바인더**(§2.3 · SI Fig. S1–S2): `[인쇄]` "the binder does not exhibit a specific morphology (such as … PTFE … fibrils) … but preferably smears up voids between AM particles. Accordingly, the binder **covers active interface area** and may **affect ionic transport**". 절차 = AM 을 바인더 막으로 팽창 → AM + 막을 한 덩어리로 보고 같은 폭만큼 수축 → AM 사이 좁은 곳에만 "binder bridge" 가 남음 → 목표 함량까지 반복. `[인쇄]` 팽창 · 수축 같은 속도 = "minimal contact angle … high wettability".
- **전류밀도 추정**(§2.4 · SI Fig. S3): 옴 강하만 — 식 (15) `j = σ_bulk,SE (1 − φ_void) v_SE ΔU / (τ² l)` · 식 (17) C-율 `= σ v_SE ΔU / (c_AM ρ_AM v_AM τ² l²)`(두께 제곱). `[인쇄]` "we neglect all non-ohmic behaviors such as charge-transfer effects or ionic diffusion in the AM" · "good case scenario".

---

# 3. 결과 — 유효 전도 (§3.1)

**기본 void `φ_void` = 15 %** `[인쇄]` "reasonable compromise for slurry-based electrodes, which are reported to possess 20−30% residual porosity in an uncalendered state, as well as pressed electrodes with 13.2% residual porosity[26 = 55호]" · 침투 + 냉간 압착은 6–8 %(Kim 2017).

## 3.1 문헌 대조 (Kato 2018, SI Fig. S4 · Table S2)

- LCO:LGPS:아세틸렌블랙(고체 기준 38.1 : 57.1 : 4.8 %) — LCO 는 5 각 평판 다면체(두께 μ 3 µm · 반경 μ 2.5 µm, 가우스), LGPS 는 7 각 볼록 다면체(μ 4 µm), 80 × 80 × 100 µm, **void 15 % 가정**(`[인쇄]` "the SEM image does not allow us to distinguish between acetylene black and void space").
- `[인쇄]` 모의 **0.68 mS cm⁻¹ · `τ²` 2.29** ↔ Kato **0.73 · 2.47** · "the calculation of the tortuosity factor is ambiguous because Kato et al. do not account for the residual void space … Still … in good accordance".
- `[도표]` Fig. S4(봤다): 왼쪽 SEM 에서 검은 영역 = "Acetylene black and void space"(구분 불가), 오른쪽 모델에서 void(흰색)는 **SE 영역 안에 잘게 흩어진 화소 조각**이고 AB(진회색)는 LCO 사이 삼각 틈. 모델 LCO 는 SEM 보다 더 각지고 고르다.
- `[재현]` 위 판정 표 — `σ⁰` 3.2 로 2.28 ✓ · Kato 2.47 은 무공극 `ε` 0.571(`[재현]` 2.50). 곱 비 **1.07**.

## 3.2 AM 입자 크기 (Fig. 1 — 봤다)

- `[도표]` Fig. 1a: `σ_eff` 는 ε_AM 40 → 66 vol% 에서 **거의 직선으로** 감소(3 µm 0.565 → 0.055 · 15 µm ≈0.62 → ≈0.10 mS cm⁻¹); 큰 입자가 위. `[인쇄]` "an increasing AM fraction … **linearly** reduces the effective ionic conductivity".
- Fig. 1b: `τ²` ≈2(50:50) → 60 vol%(= 70:30)에서 3.5–5.0 → **66 vol% 에서 5.3–9.7**. `[인쇄]` "starts at τ² ≃ 2 for … 50:50 and rises … close-to-linear … until 65:35 … Above … 65:35 … rises abruptly, especially for small particle sizes".
- ⚠ `[도표]` **60 → 66 vol% 사이에 점이 없다** — "abrupt" 구간은 선 하나로 이은 한 칸이다. `[해석]` `σ_eff` 가 선형으로 0 에 다가가면 `σ_eff` 의 **상대** 감소가 가속되고, `τ² = σ⁰ε/σ_eff` 는 그 비를 그대로 보인다 — 문턱이 아니라 매끈한 발산의 시작일 수 있다(이 편은 SE 퍼콜레이션 문턱을 따로 계산 · 인쇄하지 않았다).
- 해석 `[인쇄]`: 작은 AM → 장애물 수 ↑(Froboese 2019) · 큰 AM/SE 크기비 유리(Shi 2020 *AEM*) · "pore size scales with particle size" — 작은 입자는 경로가 많지만 좁다.

## 3.3 Bruggeman 대조 (Fig. 2 — 봤다)

- `[도표]` 가로 `ε_SE` 18.6–44 vol%(로그), 세로 `τ²`(로그). 데이터(점선)와 적합(실선): 3 µm `0.325·ε^−2.018` · 15 µm `0.668·ε^−1.213` · Bruggeman `ε^−1/2`(검정). 최저 `ε_SE` ≈18.6 %: 3 µm ≈9.7 · 15 µm ≈5.3 ↔ Bruggeman ≈2.3(`[인쇄]` "4-fold").
- `[도표]` 적합선은 데이터를 곧게 가로지른다 — 3 µm 양끝(≈18.6 · ≈44 %)에서 데이터가 적합 위, 가운데서 아래(곡률). `[인쇄]` "describes the behavior **acceptably**".
- `[인쇄]` "In contrast to conventional electrodes, further characteristics like the morphology, particle size and distribution of the SE particles … can affect ionic tortuosity … making it even less applicable for ASSB cathodes".

## 3.4 다봉 분포 (Fig. 3 — 안 봄 · SI Fig. S5 — 안 봄, 텍스트 추출)

- 3봉 L:M:S = 1:1:2(개수), dS 3 µm · dM 5.5 µm(= (√2 − 1)·rL 관계) · dL 5.5–13.5 µm. `[인쇄]` "Compared to monomodal particle arrangements, the tortuosity is generally lower, even though the average particle size is smaller".
- SI Fig. S5(텍스트): 70:30 AM:SE · `φ_void` 15 % — `τ²_mono(d) = 6.40 (d/µm)^−0.246`, R² 0.95 · `τ²_tri(dL) = 5.55 (dL/µm)^−0.190`, R² 0.99.
- ⚠ **D1**: 본문 `[인쇄]`(쪽 렌더로 확인) "The fits indicate that the **upper limit** of the tortuosity factor, which would be reached for **vanishing AM particle size**, is at … `lim_{d→0 µm} {τ²_mono(d)} = 6.40`" — `a·d^−b`(b > 0)는 d → 0 에서 **발산**한다. 6.40 · 5.55 는 **d = 1 µm 에서의 값**(계수 `a`)이다.
- `[인쇄]` "Targeting an ionic tortuosity factor of 3.5, both distributions … require an AM particle size of 12 µm" — `[재현]` 6.40·12^−0.246 = 3.47 · 5.55·12^−0.190 = 3.46 ✓.
- ⚠ **D2**: 같은 절 `[인쇄]` "a specific composition (**70:30 SE:AM** volume ratio)" ↔ 다음 쪽 · SI S5 "**70:30 AM:SE**".

## 3.5 void (Fig. 4 — 봤다)

- `[인쇄]` "Figure 4 displays the effective ionic conductivity and tortuosity factor versus the AM:SE volume ratio for void spaces between 5 and 20% with 5 µm-sized AM particles" · "Volume ratios with an AM content above 73:27 AM:SE are challenging to obtain in microstructures of 5% void space because the limit of dense packing … applies to the AM volume fraction in the entire volume".
- `[도표]` 범례 **세 값뿐**: `φ_void` 20 · 10 · 5 %(15 % 곡선 없음). 곡선 범위: 5 % ≈42:58 → ≈72:28 · 10 % ≈45:55 → ≈76:24 · **20 % 50:50 → ≈85:15**.
- `[도표]` `σ_eff`(mS cm⁻¹, 로그): 50:50 에서 **0.78 / 0.65 / 0.43**(5 / 10 / 20 %) · ≈70:30 에서 ≈0.28 / ≈0.24 / ≈0.13 · 20 % 끝(≈85:15) ≈0.006.
- `[도표]` `τ²`(로그): 50:50 에서 ≈1.65 / ≈1.9 / ≈2.5 · ≈70:30 에서 ≈2.6 / ≈3.2 / ≈5 · 20 % 는 ≈75:25 부터 가팔라져 ≈85:15 에서 **≈55**.
- `[인쇄]` "a higher void space significantly lowers the ionic conductivity, with 2-fold higher effective conductivities for 5% void space, compared to 20%. This originates in the **loss of ionic pathways**" · "Toward higher AM loading, the effective ionic conductivity drops, and the tortuosity factor steeply increases" · "void space is indeed an important and inherent electrode property that should not be neglected".
- `[재현]` 50:50 분해: `σ_eff` 비 1.81 = `ε_SE` 비(0.95/0.80) 1.19 × `τ²` 비 1.52 → 로그 몫 **`τ²` 70 %** · `ε` 30 %. `[재현]` `τ²` 검산(`σ⁰` 2.7): 5 % 1.64 · 20 % 2.51 ✓ — Fig. 4 는 Table S1 `σ⁰` 로 계산됐다.
- ⇒ **void 축에는 문턱이 없다** — 세 점으로는 해상할 수도 없다. 급변은 **20 % 곡선의 고AM 끝**(다른 두 곡선은 조밀 충전 한계로 거기까지 못 간다)에만 있다. `[해석]` "void 가 크면 더 높은 AM 분율까지 구조가 만들어지고, 거기서 `τ²` 가 발산한다" 를 "pore 부피가 문턱을 넘으면 저항이 급증" 으로 읽을 수는 없다 — 축이 다르다.
- **void 는 이 편에서 경로(수송 곱)로만 들어간다.** AM 이온 경로가 사실상 막혀 있고(G7), `σ_eff` 계산에는 반응 · 접촉 면적 항이 없다. 접촉 쪽 void 효과는 01호의 `A_spec,a`(Fig. 8 · 9)에만 있고 이 편 void 절은 `A_spec,a` 를 다시 계산하지 않았다 — 55호(경로)와 같은 쪽이다.

---

# 4. 결과 — 바인더 (§3.2, Fig. 5 — 봤다, b · d 는 원본 래스터 확대로 판독)

- **함량 정의** `[인쇄]`: `V(B):V(AM)` 로 AM 부피에 묶음 → wt% 는 AM 과 함께 조금 오른다. `[도표]` Fig. 5a: NBR(ρ 1 g cm⁻³) 0.05 → **0.73–0.97 wt%** · 0.10 → **1.45–1.95 wt%** · PVDF(ρ 1.78) 0.05 → 1.27–1.70 · 0.10 → **2.55–3.40 wt%**(ε_NCM811 40–68 vol%). `[인쇄]` "V(NBR):V(AM) = 0.1 equals weight fractions lower than 2 wt % … even small binder weight fractions consume a significant volume".
- **부피 배정** `[도표]` Fig. 5a · 5d 위 축: "Volume fraction NCM811:LPS:B" 50:47:2.5 / 50:44:5.0 … 80:16:4.0 / 80:12:8.0 — **바인더 부피는 SE 에서 나온다**(AM:SE+B 비 고정). ⚠ **D11** 이 축과 본문(`NMC811:LPS:NBR`)은 SE 를 "LPS" 로, Table S1 은 "LPSCl" 로 쓴다.
- **퍼콜레이션**(Fig. 5b) `[도표]`: AM 이용률(마름모) — 40 vol% ≈3 · 45 ≈5 · 48 ≈5 · **49 ≈22 · 50 ≈63** · 55 ≈94 · ≥58 ≈98–100 %, 세 바인더 곡선 **겹침**. SE 이용률(원) — ≤60 vol% ≈99–100 % 전부 · 68 vol% 에서 무 ≈98 · 0.05 ≈91 · **0.10 ≈55 %**. `[인쇄]` "there is a significant effect on the SE utilization for compositions with AM content larger than the 70:30 AM:SE volume ratio … the binder impedes and blocks ionic pathways".
- **활성 계면**(Fig. 5c) `[도표]`: `A_spec,a`(10⁵ m⁻¹) 봉우리 무 ≈4.15(ε_AM ≈58–59) · 0.05 ≈3.05(≈56–58) · 0.10 ≈2.4(≈56); **ε_AM ≤ 48 에서 셋 다 ≈0.1–0.2**, 49 → 50 에서 급등(= AM 퍼콜레이션). 68 vol%: 3.35 / 1.9 / 0.67.
- **상대 면적**(Fig. 5d) `[도표]`: 0.05 ≈83(40) → ≈72(59) → ≈56 %(68) · 0.10 ≈71 → ≈53 → ≈20 %. `[인쇄]` "reduced by at least 17% … and 29% … low AM … 43 and 82%" ✓(`[도표]` 대응).
- **Nam 2018 대조** — 판정 절 참조. ⚠ **D5** 캡션 `[인쇄]` "**blue points** represent data from GITT" ↔ `[도표]` 그림은 **진회색 역삼각형**.
- **수송**(Fig. 5e · f) `[도표]`: `σ_eff` ε_AM 40: 0.60 / 0.50 / 0.43 · 60: ≈0.18 / ≈0.10 / ≈0.05 · 68: 0.045 / 0.0098 / 3.3 × 10⁻⁴ mS cm⁻¹. `τ²` 40: ≈2.05 / 2.3 / 2.6 · 60: 4.2 / 6.4 / 10 · 68: 10 / 38 / ≈800. `[인쇄]` "it becomes especially crucial in high-energy cells with more AM than … 70:30 AM:SE+B … the conductivity **drops abruptly**, and the ionic tortuosity increases **steeply**".
- `[재현]` **`τ²` 의 `ε` 규약 = 순수 SE**: ε_AM 40 · 0.10 → 2.57(순수) ↔ 2.83(SE+B) · 68 → 835 ↔ 1391 · 60 → 10.3 ↔ 13.5 — `[도표]` 2.6 · ≈800 · 10 은 **순수 SE** 쪽. ⇒ 바인더가 올린 `τ²` 는 SE 부피 손실을 뺀 **경로 차단**의 몫이다.

---

# 5. 결과 — 적용 전류밀도 (§3.3, Fig. 6 — 봤다 · Table 1)

- `[인쇄]` ΔU **0.1 V** · `φ_void` 15 % · NCM811 196 mAh g⁻¹ · 4.76 g cm⁻³. `[도표]` Fig. 6a/c: `τ²` 4 · `v_SE` 30 vol% 고정, `l` 40–400 µm × `σ_SE` 1–25 mS cm⁻¹ · 6b/d: `l` 100 µm · `σ_SE` 3.2 고정, AM:SE 50:50–85:15 × `τ²` 1–7.
- `[재현]` 인쇄 문장 검산: "5 mA cm⁻² … thinner than 70 µm … 5 mS cm⁻¹" → **64 µm** ✓ · "100 µm … C-rates above 2 C … below 17 mS cm⁻¹" → 17 에서 **1.95 C** ✓ · "45 vol % SE … τ² above 3 … not … higher than 1 C" → **0.94 C** ✓.
- **바인더 사례** `[인쇄]` 70 vol% AM · 15 % void · LGPS 3.2 · 100 µm: `τ²` 10 / 6.4 / 4.2 → **0.82 mA cm⁻²(0.15 C) · 1.3(0.23 C) · < 2(0.35 C)**. ⚠ **D4** `[재현]` 이 셋은 `v_SE` **0.30**(SE + 바인더)으로 계산됐다(0.816 · 1.275 · 1.943 ✓). 그러나 `τ²` 10 · 6.4 는 **순수 SE `ε`** 로 나눈 값이다(§4) — 같은 규약이면 `v_SE` 0.23 · 0.265 → **0.63 mA cm⁻²(0.11 C) · 1.13(0.20 C)**, 곧 인쇄값은 바인더 사례를 ×1.30 · ×1.15 **낙관**한다(무바인더는 그대로).
- **Table 1**(텍스트) `[재현]` 여섯 전류 중 다섯 ✓: 고에너지 300 µm · 80:20 · `τ²` 10 → 0.181 / 1.417 mA cm⁻²(인쇄 0.18 / 1.42) · 중간 140 µm · 70:30 · 4 → 1.457 / 11.38(1.46 / 11.4) · C-율 0.010 · 0.074 · 0.19 · 1.46 ✓. ⚠ **D3** 고출력 100 µm · 60:40 · 인쇄 `τ²` **1.7**(`[인쇄]` "We referred to the Bruggeman equation to estimate its lower tortuosity limit" — `[재현]` 0.34^−0.5 = 1.715 ✓) → 식 (15) 로 **6.40 / 50.0 mA cm⁻²(1.35 / 10.5 C)** ↔ 인쇄 **7.25 / 56.7(1.5 / 11.9 C)** — 인쇄값은 `τ²` **1.50** 에서 정확히 나온다(7.253 · 56.67 · 1.52 · 11.91).
- `[인쇄]` 권고: "lithium-ion conductivities of **10 mS cm⁻¹** should be targeted" · 액체 1 M LiPF₆ 는 전달수 0.27 로 부분 Li⁺ 전도도 2.7 mS cm⁻¹ — "The essential difference is that the SE does not easily wet the AM surface but introduces its own microstructure … with the void space and binder strongly affecting (and impeding) ionic pathways".

---

# 6. 결론 (인쇄 요지)

- `[인쇄]` "The choice of the AM particle size can be seen as a trade-off between ionic and electronic conduction" · 3봉 분포 · 단결정 AM 권고.
- `[인쇄]` Bruggeman "is not valid for complex ASSB microstructures and significantly underestimates the tortuosity … should be used cautiously".
- `[인쇄]` "The residual void space and the binder content are two processing-rooted properties, which critically influence ionic transport and the active surface area available for Li insertion".
- `[인쇄]` "a model microstructure can only be understood as the **snapshot** of a real ASSB cathode because the latter are time-variant … future work … elastic modeling and the effects of volume changes, as well as on a full electrochemical simulation" — **시간축 0 을 저자가 인쇄**했다(→ 56호가 "full electrochemical simulation" 을 했고, 여전히 첫 충전 한 번).

---

# 7. 'pore 문턱' 귀속 — 판정 근거 정리

| 요소(14호 문장) | 이 편 | 01호 | 56호 |
|---|---|---|---|
| "pore volume increases" — void 부피 축 | ✅ 5 · 10 · 20 %(d 5 µm) | ✅ 43 → 3 %(70/30) | ❌ |
| "surpasses a threshold" — 문턱 | ❌ `threshold` 0; 급변은 AM 축 | ✅ 34 % · 21 %(이용률 판정, 기준 미인쇄 — 01호 G5) | ❌ |
| "abrupt resistance increase" — 저항 급증 | ⚠ `σ_eff` ×2(5 → 20 %) — 단조 · 완만 | ❌ 전도도 0 | ❌ |
| 인용 관계 | 56호 ref 25 · **14호 인용 0**(14호 PDF 전문에서 `Bielefeld` 는 [69] 한 번 = 2022 편) | 이 편 ref 21 · 14호 인용 0 | **14호 ref [69]** |

⇒ **판정: 출처 불명(계보 안 어느 편도 문장 그대로 뒷받침하지 않는다).** 가장 가까운 두 조각은 01호 Fig. 9(공극률 문턱 — 퍼콜레이션, 저항 아님)와 이 편 Fig. 4(void → `σ_eff` — 저항 쪽, 문턱 아님)다. `[해석]` 14호가 volumetry(압력 → OCV) 해석의 근거로 쓴 이 문장을 **ASSB 합성 truth 의 "void 문턱" 입력으로 옮기지 않는다** — 문턱 값도, 축도, 관측량도 원전에서 정해지지 않았다.

(14호 참고문헌 확인: 14호 PDF 전문(NFKC)에서 `Bielefeld` · `12821` 검색 — `Bielefeld` 1 회([69] = 2022 편) · `12821` 0 회. ⇒ 14호는 01호도 이 편도 인용하지 않는다.)

---

# 8. 이 편을 ASSB 합성 truth 에 쓸 때 (`[추론]`)

37호 §9 다섯 조건 (i) `θ` 가 용량에 곱해지되 `ε_p` 와 별개 (ii) 비연결 입자가 자기 SOC 리튬을 붙든다 (iii) 죽은 부피가 전해질이 되지 않는다 (iv) `θ` 에만 반응하는 조작 · 관측 (v) 이중층이 접촉 면적에 비례.

| 조건 | 이 편 | 판정 |
|---|---|---|
| (i) `θ` 별개 칸 | `θ_AM`(이용률)은 **계산된다** — 01호 배열 그대로, 바인더와 무관 | ✅ 기하량으로만(전압 · 용량 0) |
| (ii) 비연결 입자 | 고립 AM 은 "cannot be addressed" 로 정의만 | ⚠ 정의 |
| (iii) 죽은 부피 ≠ 전해질 | void 는 void(전도 0) ✅ · **바인더는 SE 부피를 먹는다**(전해질 → 죽은 부피) ✅ | ✅ |
| (iv) `θ`-전용 조작 | **바인더는 `θ_AM` 을 안 움직이고 `A_eff` · `σ_eff` 를 움직인다 — `θ` 의 반대, "`θ` 불변 조작"** · void 는 `σ_eff`(이 편) + `θ` · `A_spec,a`(01호) | ❌ — 그러나 **대조군으로는 쓸모**: 바인더 스윕은 "`LAM_PE` 도 `θ` 도 아닌 율 손실" 의 모델 표본 |
| (v) `C_dl ∝` 면적 | 용량성 요소 0 | ❌ 해당 없음 |

⇒ `[추론]` 이 편은 합성 truth 에 **"`θ_AM` · `ε_p` 불변 + `A_eff` · `κ_eff` 동시 감소"** 조작의 크기를 준다 — 바인더 0 → 0.10(부피비)에서 70:30 기준 `[도표]` `A_spec,a` ×≈0.50 · `τ²` ×2.4. 우리 degeneracy 질문에서 이것은 **율 의존 손실을 만드는 비-LAM 손잡이**이고(저율 OCV 에는 안 보여야 한다 — 이 편은 전압을 계산하지 않았다), 두 곱을 **같이** 움직이므로 곱 하나로 요약하면 몫이 섞인다.

---

# 9. 계보 대조

| 편 | 대조 |
|---|---|
| **01호 Bielefeld 2019**(ref 21) | 같은 저자 셋 · 같은 AM 배열. 01호가 `[인쇄]` "tortuosity, and resulting effective conductivities … not explicitly treated" 로 뺀 항을 **이 편이 채운다**. `p_c` 는 Fig. 5b 에 말없이 재현(49 → 50 vol%). 01호 초록이 계산 없이 말한 "effective conductivities"(01호 §10 불일치 1)의 실제 계산이 여기다. 01호 공극률 문턱(34 · 21 %)은 이 편 void 절(5–20 %)의 범위 **밖** |
| **55호 Hlushkou 2018**(ref 26 · S3) | void 기본값 15 % 의 출처 — "13.2 % residual porosity/void space" 로 인용(55호 D7: 수지 + void, **두 번째 전파**). `[인쇄]` 55호 `τ²` 1.6(EIS) · 1.74(모의) · 1.27(void → SE 가상 치환)을 정확히 옮겼다 ✓. 같은 양 대조 0 — 조성 · 형태 다름. void 로그 몫 `τ²` 70 %(이 편, 합성) ↔ 59 %(55호, 실측 구조) — 같은 방향(`[재현]`, 비교용) |
| **56호 Bielefeld 2022**(56호 ref 25) | 후속. 이 편 = 경로만(void · 바인더 → `σ_eff`), 56호 = 접촉만(void → `φ`). 56호 서론 "Highly tortuous ionic paths … crucial impact"(refs 25, 27)가 이 편을 가리킨다 ✓. 56호가 넘긴 "pore 문턱" 귀속은 **이 편에도 없다** |
| **14호 Oh 2025 *Maxwell***([69] = 56호) | "pore 문턱" — §7, 출처 불명 |
| **24호 Stavola 2023**(ref 41 · SI 5) | ⚠ **D13**: 24호 `[인쇄]` "assuming **14%** of the cathode is void (refs 7, **41**, 42, 48, 49)" · "Bielefeld and co-workers have demonstrated that tortuosity effects in ASLBs are determined by complex **point contacts** … non-intuitive" ↔ 이 편: void 기본값 **15 %**(스윕 5 · 10 · 20), "14" 가 void 로 나오는 곳 **0** · `point contact` **0** · `intuitive` 1("the impact of the AM particle size … is **not intuitive**" — 점 접촉 아님). ⇒ 원장 행 "24호의 14 % void 가정과 τ 정의의 출처" 는 **절반만 맞다** — `τ²` 정의(식 (3) · (11), void 포함 `ε_SE`)는 ✅, 14 % 는 ❌(`[해석]` 14 % 는 Rueß 2020 · 56호 쪽 값). 그리고 24호 D1(`ε` 로 CAM 분율을 쓴 오류)은 이 편 규약(식 (11) `ε_SE = (1 − φ)v_SE`)과 **어긋난다** — 24호가 이 편 정의를 가져왔다면 따르지 않은 것이다 |
| **15호 Rahman 2024**([28]) | 15호 요약 문단(`[인쇄]` "even small amounts of binder can significantly impact ion transport paths and active surface area")은 이 편 초록과 일치 ✓. 15호 "SBMS 에 중요" 의 다리는 이 편에도 없다(전압 0) |
| **53호 Ren 2023**([151b]) | 53호 한 문장("도전 바인더 분포 → 활성 면적")은 이 편 **§2.3 문헌 서술**(`[인쇄]` "Nanoporosity of the CBC network can amplify the effect of surface coverage by the binder" — Trembacki 2018 인용)과 맞는다. 이 편 **모델** 바인더는 절연 · 탄소 없음 — 부분 ✓ |
| **37호 Li 2024** | 바인더 = `A_eff·k` 자리 + `κ_eff` 자리, `ε_p` 아님(§8) |
| **22호 Strauss 2018**(ref 23) | "small AM diameters leading to enhanced electronic percolation" 의 근거로 인용 ✓ |
| **29 · 31호**(GITT 곱) | Nam GITT "접촉 면적" = `D·(A/V)²` 곱에서 `D` 불변 가정 — 대조의 실험 쪽이 곱이다(`[해석]`) |
| **41호 Nam 2018 *JMCA*** | ⚠ **다른 Nam 2018** — 이 편 ref 25 는 *JPS* 375, 93(건식 ↔ 슬러리) |

---

# 10. 곱 축퇴 처방 — 마흔 번째 적용

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | 모의 EIS 0 · `C` 0 · 정상 상태 전도만 | ❌ |
| **2단계** 면적 대조군 | **모델 안**: 바인더 0 · 0.05 · 0.10 — `A_spec,a` 비(Fig. 5d) · **실험 쪽**: Nam 2018 건식 ↔ 슬러리 GITT "면적" 비 | ⚠ 모델판 + 곱 대조 — 실험 쪽이 `D·(A/V)²` 이고 저자가 "large errors" 를 인쇄 · 작은 AM 점은 `p_c` 아래 |
| **3-a** `Ea` | 온도 0 | ❌ |
| **3-b** `C` 상한 | — | 해당 없음 |
| **4단계** 두 영역 | 없음 | ❌ |
| 수송 곱 줄(24 · 54 · 55호) | `σ⁰` 입력 · `ε` 구조 · `τ²` = `σ_eff` 이름표 — **구성상 풀림**. 실측 대조는 한 점(Kato) · void 가정 15 % · 곱 비 1.07 ↔ 같은 지면 void 손잡이 ×2 | ⚠ 55호 줄("같은 시편 · 같은 `ε`")의 **실패형** — 시편의 `ε` 를 모르고 가정했다 |
| 율 스윕 줄 | 전압 0 — 옴 강하 추정만(ΔU 0.1 V 고정) | ❌ |

**곱이 선 자리** — 이 편 모델 안에서 수송 곱 `σ⁰·ε/τ²` 은 **입력 `σ⁰` + 구조 `ε` + 계산 `σ_eff`** 로 풀려 있다(54호 "구조 계산으로 뗀다" 부류). 동역학 곱 `A_eff·k` 는 반쪽만 있다 — 면적(`A_spec,a`)은 계산하고 `k` 는 없다(전압 0). **바인더 · void 는 두 곱을 한 손잡이로 같이 깎는다**: 70:30 · 0.10 에서 `[도표]` `A_spec,a` ×≈0.50 · `τ²` ×2.4(`σ_eff` ×≈0.28 — `ε_SE` 손실 ×0.75 포함). 실측 셀에서 이 손잡이를 돌리면 곡선의 율 손실이 **면적 몫 · 수송 몫 · (SE 고립이면) 이온 퍼콜레이션 몫**으로 섞여 들어온다.

**⇒ 이 적용이 처방에 더하는 것**:
1. **새 줄 "한 공정 손잡이가 두 곱을 같이 깎을 때 — 면적 비와 수송 비를 같은 모델에서 따로 보고, 실험 쪽 GITT '면적' 은 곱으로 적는다"**: 바인더 · void · 압착처럼 `A_eff` 와 `σ_eff`(그리고 `θ_SE`)를 동시에 움직이는 조작을 대조군으로 쓸 때 (i) 모델에서 `A_spec,a` 비 · `τ²` 비 · `θ_SE` 를 **같은 구조에서 나란히** 보고하고 (ii) `A_spec,a` 감소 안의 **피복 몫 ↔ SE 고립 몫**을 가른다(이 편은 안 했다) (iii) 실험 쪽 "접촉 면적" 이 GITT 유래면 `D` 불변 가정을 명시하고 `D·(A/V)²` 곱으로 적는다 (iv) 모델이 퍼콜레이션 문턱 아래인 점(분모 ≈0)은 비 대조에서 뺀다.
2. **검증 일치 폭 ↔ 가정 손잡이 폭 비교** — 모르는 입력(여기선 void)을 가정한 한 점 대조는, 그 입력이 결과를 움직이는 폭(같은 지면 Fig. 4: ×2)이 일치 폭(7 %)보다 크면 **모델 검증이 아니다**. 55호 줄의 반대편 끝.

**⚠ 이것이 곱을 푼 것은 아니다** — 전부 모델 명제이고 전압 · 용량 · 시간축이 없다. `[도표]` 비는 로그 축 판독이다. 신품 · 정적 구조 · `LAM_PE` 없음.

---

# 11. Q1–Q8 / 채움표 행

| Q1 정량 | Q2 독립관측 | Q3 라벨층위 | Q4 유일성 | Q5 Li-In | Q6 압력 | Q7 dead Li | Q8 화학·OCP |
|---|---|---|---|---|---|---|---|
| **이동 없음 — 층 하나(모델 명제)** "바인더는 `θ_AM` 을 구성상 안 움직이고 `A_spec,a`(피복 + SE 고립, 17–82 %) · `σ_eff`(`τ²` 4.2 → 10) · `θ_SE`(→ ≈55 %)를 한 손잡이로 깎는다; void 5 → 20 % 는 `σ_eff` ×2(단조, 문턱 0)". 01호 `p_c` 는 Fig. 5b 에 말없이 재현. `θ(N)` **0/57** | 없음 — 대조는 남의 한 점(Kato `σ_eff`) · 남의 GITT 비(Nam) | ★ 층 하나 **"유도된 `τ²`(σ⁰ε/σ_eff 이름표) + 가정 void 15 %(55호 수지 + void 출처) + 남의 GITT 면적 비('large errors' 자기 경고 · `p_c` 아래 점)"** | **0/57 — 마흔아홉 번째 성질** "적합 자유도의 무의미를 인쇄했다(α · γ 'do not offer any further scientific insight') — 그러면서 자기 검증은 모르는 void 를 15 % 로 놓은 한 점 일치(7 %)로 했고, 그 void 가 `σ_eff` 를 ×2 움직인다는 것을 같은 지면이 보인다" | 해당 없음(음극 0) | 없음(`pressure` 0 · `MPa` 0) | 해당 없음 | 없음 — NCM811 196 mAh g⁻¹ · 4.76 g cm⁻³ 는 C-율 환산용, OCP 0 |

**채움표 57호 행 — 누적 ≈20.0 → ≈20.0 (새 칸 0).** 칸을 움직이지 않은 이유: Q1 의 새 내용은 **모델 명제**(정적 · 기하 · 전압 0)이고 실측 · 논문 측정 명제가 아니다. Q4 는 식별성 계산 0.

---

# 12. 어긋남 (실제로 어긋난 것만)

| # | 자리 | 어긋남 |
|---|---|---|
| **D1** | §3.1.4 극한식 ↔ SI Fig. S5 | "upper limit … for vanishing AM particle size … `lim_{d→0 µm}` = 6.40 / 5.55" ↔ 적합 `a·d^−b`(b 0.246 · 0.190 > 0)는 d → 0 에서 발산 — 6.40 · 5.55 는 **d = 1 µm 값** |
| **D2** | §3.1.4 | "70:30 **SE:AM** volume ratio" ↔ 다음 쪽 · SI S5 "70:30 **AM:SE**" |
| **D3** | Table 1 고출력 | 인쇄 `τ²` 1.7(Bruggeman, `[재현]` 1.715) → 식 (15) 6.40 mA cm⁻² · 1.35 C ↔ 인쇄 **7.25 · 1.5 C**(LSiPSCl 56.7 · 11.9) — 인쇄값은 `τ²` 1.50 에서 정확히 나온다 |
| **D4** | §3.3 바인더 전류 | 0.82 / 1.3 mA cm⁻² 는 `v_SE` 0.30(SE+B)로 계산 ↔ `τ²` 10 / 6.4 는 순수 SE `ε` 로 나눈 값(`[재현]` §4) — 일관 규약이면 **0.63 / 1.13**(×1.30 / ×1.15 과대) |
| **D5** | Fig. 5 캡션 | "blue points represent data from GITT" ↔ 그림은 진회색 역삼각형 |
| **D6** | §3.2.1 Nam 대조 | 본문 조성 셋(작 · 중 · 대) ↔ `[도표]` 삼각형 4 개(ε_AM ≈59 에 ≈73 · ≈45 둘); "large … match quite well" 은 ≈45 만(0.10 곡선 ≈53), ≈73 은 0.05 곡선 위 — 본문 언급 없음 |
| **D7** | §3.2.1 "small AM … match" | ε_AM ≈41 은 모델 `p_c`(≈49–50) 아래 — `A_spec,a` 가 무 · 0.10 모두 ≈0.1 × 10⁵ m⁻¹(봉우리의 2–4 %)인 자리의 비 · Nam 전극은 C65 로 전자 연결 |
| **D8** | §2 ↔ Fig. 5b · c | "electronic conduction is not the limiting factor because conductive carbon will be introduced" ↔ 퍼콜레이션 · `A_spec,a` 는 **탄소 없는 AM 클러스터**로 계산(AM 이용률 40 vol% ≈3 %) |
| D9 | §3.2 ↔ Fig. 1b | "Above … 65:35 … rises abruptly" ↔ `[도표]` 60 → 66 vol% 사이 점 없음(한 칸 보간) — 모순은 아니고 해상 부족 |
| **D10** | Table S1 · §3.1 ↔ 55호 | "13.2% residual porosity" · "void … similar to Hlushkou" ↔ 55호 `[인쇄]` 13.2 % = 수지 + 잔류 void(55호 D7 두 번째 전파) |
| D11 | Table S1 ↔ Fig. 5a · §3.3 | SE "LPSCl"(σ 2.7, Kato 2016) ↔ "NCM811:LPS:B" · "NMC811:LPS:NBR" |
| **D12** | 계보 — 14호 [69] · 56호 digest 귀속 후보 | "abrupt resistance increase when the pore volume … surpasses a threshold" ↔ 이 편 `threshold` 0 · void 3 점 단조(§7) |
| **D13** | 계보 — 24호 ref 41 · 원장 | 24호 "14% … void (… 41 …)" · "point contacts … non-intuitive" ↔ 이 편 void 15 % · `point contact` 0 · "not intuitive" 는 입자 크기 문장 |

---

# 13. 그림 — 무엇을 봤나

크로퍼 자동 **13 장**(본문 Fig. 1–6 · SI Fig. S2–S5 · 표 1 · S1 · S2) — 제외 1 건(SI Fig. S1 "그래픽 없음" — 벡터 도식).
- **Read 6 장 + 확대 2 + 쪽 렌더 1**: Fig. 1 · 2 · 4 · 5 · 6 · S4 + Fig. 5b · 5d 원본 래스터 2 배 확대(판독용, 저장소 밖 스크래치) + p. 12827 극한식 쪽 렌더(D1 확인).
- **안 봄**: Fig. 3(다봉 분포 · 전자 클러스터 그림) · S2(구성 도식) · S3(전류밀도 요소 도식) · S5(`τ²(d)` — 적합식 · R² 는 텍스트 추출로 읽음) · S1(벡터, 미추출). 표 1 · S1 · S2 는 텍스트로.
- 본문 서술과 어긋난 그림: **Fig. 5 캡션 색**(D5) · **Fig. 5d 삼각형 개수**(D6) · **Fig. 5b · c 의 `p_c` 무릎**(D8 — 본문 무언급) · **Fig. 1b 표본 간격**(D9) · **Fig. 4 범례 세 값**(15 % 곡선 없음 — 본문 "between 5 and 20%" 와 모순은 아님).

---

# 14. 참고문헌 중 후속 후보 (70 번호 · SI 7, 서지 기준 — 미열람)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| **Nam, Oh, Jung, Jung, *J. Power Sources* 375, 93 (2018)** | 25 | Fig. 5d 실험 점의 원전 — GITT "접촉 면적" 과 N₂ 흡착 상관, 건식 ↔ 슬러리. **`D` 불변 가정의 실제 형태**와 삼각형 4 개의 정체(G8) | 2단계 대조군 · 29 · 31호 곱 |
| **Kato, Shiotani, Morita, Suzuki, Hirayama, Kanno, *J. Phys. Chem. Lett.* 9, 607 (2018)** | 44 · S7 | 유일한 `σ_eff` 검증점(0.73 mS cm⁻¹ · `τ²` 2.47) — 시편 void · `ε` 규약 · 측정법 | 수송 곱 · 55호 줄 |
| **Froboese, van der Sichel, Loellhoeffel, Helmers, Kwade, *JES* 166, A318 (2019)** | 27 | 실험 모형계(불활성 유리 입자 + 고분자 SE)의 굴곡도 — 수정 Bruggeman α · γ 가 이 편과 "similar" | 수송 곱 실측 |
| Shi, Tu, Tian, Xiao, Miara, Kononova, Ceder, *AEM* 10, 1902881 (2020) | 28 | AM/SE 크기비 ↔ 이온 퍼콜레이션(모델 + 실험) — **04호 Shi 2020 과 다른 편** | Q1 · 01호 G3 |
| Braun, Uhlmann, Weiss, Weber, Ivers-Tiffée, *JPS* 393, 119 (2018) | 52 | 접촉 저항 40 Ω cm² 의 출처(Kato 2016 EIS · SEM 추정) | 면적 규약 · 50호 |
| Trembacki, Mistry, Noble, Ferraro, Mukherjee, Roberts, *JES* 165, E725 (2018) | 48 · S2 | 탄소-바인더 영역 형태 · 나노 공극이 피복을 증폭(53호 문장의 원천) | `φ` 자리 |
| Hippauf 외, *Energy Storage Mater.* 21, 390 (2019) | 32 | PTFE 0.1 wt% 건식 필름 — 섬유 바인더 형태(이 편 모델이 배제한 형태) | 바인더 형태 |
| Landesfeind, Hattendorff, Ehrl, Wall, Gasteiger, *JES* 163, A1373 (2016) | 47 | 대칭셀 EIS 굴곡도 원전(55호 후속과 겹침 — **지목 2 회째**) | 수송 곱 측정법 |
| Randau 외, *Nature Energy* (2020) | 42 | 계보의 탄소 사용 · 벤치마크 | 조건 |

**큐 59**: Asheri 2023 ❌(이 편보다 늦다). 이 편이 01호 이후 계보에서 **void → `σ_eff` 를 계산한 유일한 Bielefeld 편**이라는 것까지만 적는다.

---

# 15. 이 digest 가 주장하지 않는 것

- **"pore 문턱은 존재하지 않는다" 고 주장하지 않는다.** 01 · 56 · 58 세 편에서 14호 문장 그대로의 근거를 찾지 못했다는 것까지다 — 14호가 다른 문헌을 뜻했을 가능성은 남는다.
- **바인더가 실제 셀에서 면적을 X % 깎는다고 주장하지 않는다** — §4 의 수는 이 편 모델의 출력(`[도표]`)이고, 실험 대조는 남의 GITT 비(저자 스스로 "large errors")다.
- **D3 · D4 의 인쇄값이 틀렸다고 단정하지 않는다** — 지면의 식과 인쇄 입력으로 재계산하면 어긋난다는 것까지다(D3 은 `τ²` 1.50 이 쓰였다는 추정, D4 는 `τ²` 규약을 그림 판독으로 정한 것).
- **Kato 대조가 틀렸다고 하지 않는다** — 일치(7 %)가 가정 void 의 영향 폭(×2) 안이라 **모델 검증으로는 약하다**는 것까지다.
- **24호 · 14호 인용이 틀렸다고 단정하지 않는다** — 이 편에 그 내용이 없다는 것까지다(24호 14 % 는 다른 refs 7 · 42 · 48 · 49 에서 왔을 수 있다).
- 55호 · 이 편의 `τ²` 수를 같은 계의 값으로 비교하지 않는다 — 조성 · 형태 · SE 가 다르다(비교용).
- 우리 파이프라인(`degradation-degeneracy/`)을 이 모델로 돌려 보지 않았다. 우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본이다.
- 인용한 원전(Nam 2018 *JPS* · Kato 2018 · Froboese 2019 · Braun 2018)은 열람하지 않았다.
