---
title: "Li, Fan, Zhang, Han, Wang, Liu, Jia, Guo, Zhu, He 2024 — Modeling of an all-solid-state battery with a composite positive electrode (eTransportation 20, 100315)"
source_url: local-upload/36._Modeling_of_an_all-solid-state_battery_with_a_composite_positive_electrode.pdf
source_url_si: local-upload/36._Sup_Modeling_of_an_all-solid-state_battery_with_a_composite_positive_electrode.docx
source_url_note: "본문 15 쪽(본문 13 + 참고문헌 2, 40 편) + SI .docx(텍스트 약 1.1 천 자 + Fig. S1 SEM png 1 장 + OLE 수식 WMF 4 장 + Table S1). 크로퍼가 본문 Fig. 1-11 + Table 1-2 를 잡았고 SI SEM 은 zipfile 로 word/media/image1.png 를 꺼내 fig_s1.png 로 등록했다. 8 장 + 표 1 봤다(Fig. 2 · 4 · 5 · 6 · 8 · 9 · 11 · S1 + Table 1 상단). 원자료는 커밋하지 않는다. 9호(Huo 2025)가 모델 · PSO 를 위임한 [27] 이 이 편이다."
source_doi: 10.1016/j.etran.2024.100315
source_license: "(c) 2024 Elsevier B.V. All rights reserved (open access 아님)"
pdf_sha256: abab37041fc1f1982a6100150b8fabddd1b4273dab4ad9ce987db3d3e3e45b5a
si_sha256: 20f8d0c333ef7fe8ff35fd12ff4dc06ebdeb9840aaf49c7ea7f1352ea0635ab8
ingested: 2026-09-23
sha256: b3f7e2865a928c6019be147f002bf46642c799c812f70506bde9fb29351bd29f
---

# 수집 목적

`assb` 섹션 **37호**. 큐 **36번** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-e — "9호가 모델·PSO·해법·`A_eff` 정의를 전부 위임한 곳").
닻은 `questions/assb-contact-loss-vs-lampe.md`. 9호 digest(`raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md`)는 해법을 `[인쇄]` "our previous articles [27]" 로 넘기는데,
그 [27] 이 이 편이다: Li, Fan, Zhang et al., *eTransportation* **20** (2024) 100315.

Guoliang Li, Guodong Fan, **Xi Zhang**(교신), Jingbo Han, Yansong Wang, Yisheng Liu, Linan Jia, Bangjun Guo, Chong Zhu (Shanghai Jiao Tong University, 기계공학부 +
National Engineering Research Center of Automotive Power and Intelligent Control), **Minghui He** (Shanghai Firm-lithium New Energy Technology Co., Ltd. — 산업체) —
**"Modeling of an all-solid-state battery with a composite positive electrode"**, *eTransportation* **20** (2024) 100315, doi `10.1016/j.etran.2024.100315`.
`[인쇄]` Received 13 Sep 2023 · Revised 3 Jan 2024 · Accepted 17 Jan 2024 · online 19 Jan 2024. Elsevier, "All rights reserved"(OA 아님).
`[인쇄]` 교신 `braver1980@sjtu.edu.cn`. 자금: NSFC 52177218 · 52307246, Shanghai NSF 23ZR1429100, Hainan "One Network" 073000KK52220001. 이해상충 없음 선언. `[인쇄]` "Data will be made available on request."
9호와 저자 겹침: Li · Fan · Zhang · Han · Wang · Jia — **이 편 10 인 중 6 인이 9호(9 인)에 있다**(큐 표의 "8/10" 보다 둘 적다; Huo · Zhou · Chen 은 이 편에 없고 Liu · Guo · Zhu · He 는 9호에 없다).

본문 PDF **15 쪽**(본문 13 + 참고문헌 2, 참고문헌 40 편) + SI **.docx**. 두 파일의 sha256 을 frontmatter 에 봉인했다. 원자료는 커밋하지 않는다.

> ⚠ **표기**: `[인쇄]` = 지면(본문 · SI)에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 눈으로 읽은 값(figure-read ≈, 판독 오차를 같이 적는다) ·
> `[재현]` = 지면의 수치 · 식으로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. `[해석]` 표시가 없는 문장은 원문이 실제로 말한 것이다.

---

# 판정 (먼저)

> ★★★★ **(a) 접촉 손실은 이 모델에서 `LAM_PE` 와 다른 손잡이다 — 그러나 그 손잡이는 반응 속도 상수와 정확한 곱이고, 입자 통째 비연결에는 손잡이가 없다.**
> `[인쇄]` 식 (8) `j^p_ct = (I − I^p_dl)/(A^p_eff·a_{s,p}·A·L_p)` · 식 (9) `a_{s,p} = 3ε_p/R_s` · 식 (15) 입자 표면 플럭스 `−I/(a_{s,p}·A·L_p·F)` (**`A_eff` 없음**) · 가정
> `[인쇄]` "The effective contact area is considered. However, when the concentration of lithium-ion is calculated, assuming a uniform current density distribution on the surface of the active material".
> 식을 따라가면 (`[해석]`, 계산은 이 위키):
>
> | 들어가는 곳 | `A^p_eff` (표면 접촉 분율 `φ`) | `ε_p` (활물질 부피분율 = `LAM_PE` 손잡이) |
> |---|---|---|
> | **용량** `Q_th = ε_p·A·L_p·c^p_max·F` (식 18 의 적분 극) | **없다** | **있다** |
> | **고체 확산** (식 15 · 17 · 18 — 표면 플럭스, 확산 시간 `R_s²/D_p`) | **없다** | `ε_p/R_s` 로 |
> | **계면 과전압** `η^p_ct = (2RT/F)·asinh(j^p_ct/2j^p_0)`, `j^p_0 = k_p·F·√c_SE·√(c_max−c_sur)·√c_sur` | **`A^p_eff·k_p·ε_p/R_s` 한 조합** | 같은 조합 |
> | 전해질 (식 28 · 35 · 37 · 39) | 없다 | `a_{s,p}`, `ε_SE` 로 |
> | 이중층 `I_dl = c_dl·dη/dt` (식 10, `c_dl` 단위 **F — 전극 전체**) | **없다** (`c_dl` 이 면적에 비례하지 않는다) | 없다 |
>
> ⇒ **표면 피복형 접촉 손실(`A_eff`)은 용량에도 확산에도 없고, 과전압에서 `k_p` 와 정확한 곱으로만 산다** — 식 (8) 과 식 (5) 만 보면 `A_eff → cA_eff, k_p → k_p/c` 는 모든 출력에서 **정확히 같다**.
> 즉 이 모델에서 접촉 손실은 `LAM_PE` 의 동어반복이 아니라 **계면 동역학 열화(`k_p` — 피막 · 계면 화학)의 동어반복**이다 — 18호가 `[인쇄]` "the chemical composition at the interface **or** the contact area" 로 남긴 "or" 가 **식 수준의 항등**으로 선다.
> **입자 통째 비연결(`u`, 27호의 `1 − u`)은 들어갈 자리가 `ε_p` 뿐**이고 — 그러면 `LAM_PE` 와 같은 파라미터다(27 · 28호 경고와 같은 결론, 이번에는 원형 모델에서).
> **31호 해석("`φ` 는 `D_app` 에 제곱")은 이 모델의 식에는 없고, 이 편의 파라미터 추출 식에 있다** — `[인쇄]` GITT 식 (51) `D_p = (4/πτ)(m_B V_M/(M_B S))²(ΔE_s/ΔE_τ)²` 의 `S` = `[인쇄]` "total contact area between the electrolyte and the electrode"(값 미인쇄). 모델은 `A_eff` 를 확산에서 빼는데, 모델에 넣을 `D_p` 는 접촉 면적의 **제곱**을 품은 측정에서 왔다.
>
> **(b) 파라미터 출처 — Table 1 에 각주 5 종(a SEM 측정 · b 직접 측정 · c "Identified from the experiment. Will be introduced in Sec. 4." · d 사전 고정 · e "Range identified by experiment and optimized by PSO")이 있고, `A^p_eff` · `A^n_eff` · `ε_p` · `ε_SE` · `c^p_dl` · `c^n_dl` · `t⁺₀` 에는 각주가 없다** (`[도표]` 표 이미지로 확인 — 텍스트 추출이 위첨자를 잃은 것이 아니다). §3 의 측정 절차에 접촉 면적 측정은 0 이다.
> ★★★ **`A^p_eff = 0.4938` · `A^n_eff = 0.4095` 는 9호 Table 3 과 네 자리까지 같다** — 복합양극 조성이 다른데(이 편 NCM 38 wt% ↔ 9호 56 wt%) · `ε_p` 0.1707 ↔ 0.321 · `L_p` 85 ↔ 98 µm. ⇒ 9호의 `A_eff` 는 9호 셀에 맞춘 적합값이 아니라 **출처 표시 없이 옮겨 온 상수**다(9호 digest §3.2 의 "(a) 적합값이지 측정값이 아니다" 를 이 편이 고친다 — "출처 없는 상속값").
> PSO 는 `[인쇄]` "initialized using the parameter set obtained from the experiments" · 목적함수 `[인쇄]` `J = min[RMS(U_mea − U_bat)]`(식 55) · 학습 0.4/1.0/1.2/2.0 C 정전류, 검증 나머지. 개체수 · 반복 · 경계 수치 · 시드 0.
> ★★ **`k_p` 는 측정 범위 밖으로 옮겨졌다**: Table 1 `2.263×10⁻¹²` ↔ `[도표]` Fig. 5d LSV–Tafel 측정 11 점 ≈0.7–7.2×10⁻¹¹(중간 SOC ≈0.9×10⁻¹¹) — 인쇄값은 **측정 최솟값보다도 작고** 중간 SOC 의 ≈1/4 이다. 곱 `A_eff·k_p` 로는 ≈1/8.
>
> **(c) 식별성 명제 0.** `identifiab` 0 · `uniqu` 0 · `correlat` 0(본문) · `Fisher`·`Hessian` 0 · `uncertaint` 0. "sensitivity analysis" 는 **Fig. 11 의 OAT 설계 스윕**(0.4 C 한 율 · 6 판) — 26호 표의 첫 줄.
> 가장 가까운 문장은 `[인쇄]` `A_eff` 1 ↔ 0.3 이 "minimal deviation" 이고 그것이 "attributed to the model's assumption of uniform current distribution across the surface" — **설계 민감도의 약함을 모델 가정 탓으로 돌린 문장**이지 식별성 명제가 아니다.
> 그리고 `[재현]` 그 "minimal" 은 **용량 끝점**에서만 맞다: 인쇄된 파라미터로 0.4 C 중간 SOC 과전압을 다시 계산하면 `A_eff` 1.0 에서 **+61 mV**, 0.3 에서 **−37 mV**(양 · 음극 합) — `[도표]` Fig. 11b/e 의 곡선 간격 ≈60 · ≈35 mV 와 맞고, 0.4 C RMSE 11.5 mV 의 3–5 배다.
> **Q4 는 움직이지 않는다 — ASSB 누적 0.5(29호) 그대로.** 스물아홉 번째 성질: **"접촉 면적의 자리를 모델에 새로 만들고, 그 자리가 반응 속도 상수와 곱으로만 들어가는 식을 인쇄한 뒤, 곱의 한쪽은 PSO 로 풀고 다른 쪽은 출처 없이 못 박았다 — 그리고 그 손잡이의 약한 용량 효과를 '가정 탓' 으로 인쇄했다."**
>
> **(d) 이 모델로 ASSB 합성 truth 를 만들면 동어반복이 두 갈래로 들어간다** (`[추론]`, §9).
> ① 접촉 손실을 `A_eff(N)` 으로 넣으면 — 용량에 없으므로 **OCV/저율 적합에는 보이지 않고**, 유한 율에서는 `k_p(N)`(계면 화학)과 **정확히 같다**. 그리고 `c_dl` 이 면적과 무관하게 고정이라 16호 이래 처방의 전제(`C ∝ 면적`, `R·C` 면적 불변)가 **truth 에서부터 성립하지 않는다**.
> ② `ε_p(N)` 으로 넣으면(9호가 한 방식) — **정의상 `LAM_PE`** 이고, `a_{s,p}` 가 같이 줄어 율 손실까지 한 손잡이에 묶인다(9호 `[재현]` 증폭 1.32–1.60).
> 어느 쪽이든 카드의 물음("물질은 그대로인데 용량이 준다 — OCV 가 그것을 `LAM_PE` 와 가르나")을 **시험할 수 없다** — ①은 "OCV 는 접촉 손실을 아예 못 본다" 를, ②는 "둘은 같은 것이다" 를 **truth 가 미리 정한다.** 27호가 경고한 동어반복의 **원형이 이 편이다**.
>
> **곱 축퇴 처방 스무 번째 적용 — 처방의 원천 모델에 처방을 건다** (§10): 1단계(`R·C`)는 모델 구조가 막고, 율 스윕 줄은 **율마다 다시 맞춘 `D_p,ref(C-rate)`** 가 정보를 먹는다(율 스윕 줄의 **세 번째 실패 조건**).
>
> **채움표: ≈16.0 → ≈16.0 (새 칸 0).** Q1 `θ(N)` **0/37** · Q4 ASSB 0.5 그대로.

---

# 0. 원문에 없어서 확인이 필요한 것

| # | 공백 | 왜 걸리는가 |
|---|---|---|
| **G1** | **`A^p_eff` · `A^n_eff` 의 출처가 없다** — Table 1 각주 없음, §3 측정 절차에 없음, §4 PSO 목록에도 명시 없음 | 이 편의 제목급 신규 요소(`[인쇄]` "the imperfect contact … taken into consideration")인데 값의 층위(측정 / 적합 / 가정)를 모른다. 9호 값과 네 자리 일치(§4) |
| **G2** | **`ε_p` · `ε_SE` · `c^p_dl` · `c^n_dl` · `t⁺₀` 도 각주가 없다** | `ε_p` 는 용량 손잡이, `c_dl` 은 이 편 두 번째 신규 요소 |
| **G3** | **PSO 로 푼 파라미터의 목록이 없다** — 각주 e(`k_p` · `k_n` · `D_p` · `D_n`)가 "optimized by PSO" 인 것만 확실. 경계 수치 · 개체수 · 반복 · 시드 · 재시작 0 | 자유 파라미터 수를 셀 수 없다 |
| **G4** | **각주 c "Will be introduced in Sec. 4" 의 파라미터(`κ_SE` · `D_SE` · `R_dc` · `c^n_max` · `c^p_max` · `Q`) 중 §4 에 나오는 것이 없다** — `κ_SE` · `D_SE` 는 §3.4 에 절차가 있고, `c^p_max` · `c^n_max` · `R_dc` · `Q` 는 어디에도 절차가 없다 | `c^p_max` 는 `[재현]` NCM811 이론 농도의 ≈0.54(밀도 가정) — 용량과 함께 정해진 **유효값**일 가능성 |
| **G5** | **OCP 측정 조건이 없다** — 율 · 휴지 · GITT/저율 여부 없음. `[인쇄]` "the determination of the open-circuit potential in test is based on a specific range of conditions with a certain level of polarization voltage" | 9호 digest G1 의 답이 **절반**만 왔다 — 방법(반쪽전지 + 차감)은 왔고 조건은 안 왔다 |
| **G6** | **Li-In 상대극 반쪽전지 곡선을 "(vs Li)" 로 그렸는데 환산값이 없다** (Fig. 4a 범례) | Q5 — §8 |
| **G7** | **GITT 식 (51) 의 `S`(접촉 면적) · `m_B` 값이 없다** | `D_p` 측정값이 `S²` 에 반비례 — 접촉 면적 가정이 측정 `D` 에 제곱으로 든다 |
| **G8** | **대칭 셀의 SE 두께가 없다** — 식 (52) 로 `D_SE` 를 낼 때의 `L_SE` | `[재현]` 완전지 `L_SE` = 0.825 mm 를 쓰면 인쇄값의 6.1 배(D5) |
| **G9** | **검증 조건(0.6 · 0.8 · 1.6 C · 동적 사이클)의 `D_p,ref` 를 어떻게 정했는지 없다** | `[도표]` Fig. 8a 가 0.6 · 1.6 C 에서 꺾인다(D11) — 검증이 표본 밖인지 모른다 |
| **G10** | **질량 · 로딩이 없다** (면적 용량 0.903 mAh cm⁻² 만) | `ε_p` 를 기하로 검산할 수 없다(9호는 15 mg 을 인쇄했다) |
| **G11** | **셀 수 · 반복 없음** — "five cycles are carried out at each specified rate" 는 사이클 반복이지 셀 반복이 아니다. `standard deviation` · `replicat` · `error bar` 0 | 모든 파라미터가 셀 1 개에서 나왔는지 모른다 |
| **G12** | **이중층 효과 결론의 근거 그림이 없다** — `[인쇄]` "the space charge layer … exhibits a small influence on the discharge profile" 인데 `c_dl` 을 흔든 그림 0 (Fig. 11 은 `R_s` · `A_eff` · `L_SE` · `ε_p` 만) | 두 번째 신규 요소의 결론이 지면에서 검증되지 않는다 |

---

# 1. 서지 · SI 의 정체 · 낱말 지문

**SI(.docx)** — 텍스트 ≈1.1 천 자. `zipfile` 로 열면 `word/media/image1.png`(**Fig. S1 SEM, NCM811**) + `image2~5.wmf`(OLE 수식 그림 = 식 S.1–S.4, 전해질 전달함수 (37)–(40) 의 3 차 Padé 결과) + **표 1 개**:

`[인쇄]` **Table S1 Pressure data during the preparation of the battery.**

| Material | Pressure (MPa) | Time |
|---|---:|---|
| Li-Si negative electrode | 480 | >1 min |
| Li-In counter electrode | 36–50 | <10 s |
| Electrolyte | 120 | >1 min |
| Positive electrode | 360 | >1 min |
| Battery | 50 | Maintain |

⇒ 운전 압력 **50 MPa 유지**가 이 셀의 유일한 스택 압력 값이다(스윕 0). 본문은 `MPa` 0 회 — 전부 SI.

**낱말 지문** (규칙: 참고문헌 전 본문 · NFKC 뒤 · 대소문자 구분 · 낱말 경계):

| 열 | 값 | 비고 |
|---|---:|---|
| `identifiab` | **0** | 대소문자 무시도 0. `identif*` 6(“parameter identification” 류) · 줄끝 소프트 하이픈 이으면 7 · 대소문자 무시 8 |
| `uncertaint` · `confidence interval` · `Bayes` · `posterior` | **0 · 0 · 0 · 0** | |
| `calibrat` | 1 | `[인쇄]` Kazemi [13] "adopt a strategy of **calibrating** the diffusion coefficient" — 불확실성 보정 아님 |
| `LLI` | **0** | |
| `LAM` | **0** | ★ 접두로 세도 0(`\bLAM\w*` 0) — 36호가 지적한 `LAMPE` 가림 문제가 **생길 낱말 자체가 없다** |
| `degradation mode` | **0** | `degrad*` 0 · `aging` 2(“rapid aging” · 향후 과제) |
| `contact loss` | **0** | 대신 `contact area` **10** · `effective contact` 5(대소문자 무시 7 — Table 1 행 이름) · `contact*` 16 |
| `MPa` | **0** (본문) / 1 (SI 표 머리) | `pressure` 본문 6 — 전부 "pressure cell" 류 · 1 회 Table S1 참조 |

**NFKC 전후 차이**: 본문에서 NFKC 가 바꾸는 글자는 **8 개(`´` U+00B4, "Padé" 의 악센트 → 공백 + 결합 악센트)뿐**이고 지문 열을 하나도 바꾸지 않는다. 합자 0.
⚠ 지문 도구의 다른 맹점이 여기 있다: **소프트 하이픈 U+00AD 81 개**(Elsevier 조판의 줄끝 분철). NFKC 는 소프트 하이픈을 지우지 않는다 — 이어 붙여야 `identif*` 6 → 7. 이 편에서는 지문 열 변화 0.

★ `[해석]` 이 편의 지문은 **열화 어휘 0 · 식별성 어휘 0 · 접촉 어휘는 "contact area" 형**이다 — 접촉 손실을 **노화 기구**가 아니라 **신품 셀의 불완전 접촉 상태**로 다루는 편. 노화는 결론의 향후 과제로만 나온다(`[인쇄]` "its impact on the battery performance after aging is planned to be investigated in our future work").

---

# 2. 셀 · 실험 (§3, `[인쇄]`)

- 셀: **NCM811(LiBO₃ 코팅) / Li₆PS₅Cl / Li₄.₄Si** 압력 셀, 몰드 반경 5 mm(`A` = 7.854×10⁻⁵ m² ✓ `[재현]`), 면적 용량 **0.903 mAh cm⁻²**.
- 복합양극 **NCM811 : LPSCl : 탄소 = 38 : 57 : 5 wt%**. `[인쇄]` "to ensure that the cells have good stability, a mass fraction of 38% NCM811 cathode cells are utilized" — 활물질 비율을 올리면 "a decrease in cycle life and rapid aging" 이라는 이유.
- 음극 Li-Si 합금 + 소량 탄소 · 바인더. **반쪽전지 상대극 = Li–In** (`[인쇄]` "The Li–In counter electrode half-cells are established to determine the electrochemical parameters of the electrode material").
- 활성화 5 사이클 뒤 측정. 아르곤 분위기.
- 율 시험: **0.4 · 0.6 · 0.8 · 1.0 · 1.2 · 1.6 · 2.0 C**, 2.0–4.3 V, 율당 5 사이클, 충 · 방전 뒤 **3 h 휴지**. + 동적 사이클(Fig. 4c, `[도표]` −1.0 ~ +0.5 C 계단, ≈225 s, ΔSOC ≈−0.9 %).
- `[인쇄]` "higher C-rate data could not be obtained due to the instability of the produced pressure cells."
- 파라미터 측정: **GITT**(양극 반쪽전지 → `D_p`) · **대칭 셀 차단 후 이완**(0.05 C 1 min → `D_SE`, 식 52) · **차단 셀 EIS**(10–10⁵ Hz, 10 mV → `κ_SE`) · **LSV**(양극 반쪽전지, 0.1 mV s⁻¹, OCV ±0.2 V 왕복, 여러 SOC → Tafel 절편 → `k_p`; 음극은 한 점) · **SEM**(두께 · `R_s`).
- 반복 셀 수 미기재(G11).

---

# 3. 모델 (§2) — 접촉 손실이 들어가는 자리를 식으로

## 3.1 구조

1-D: 음극(−L_n ≤ x ≤ 0, 평판, 입자 없음 — `[인쇄]` 과량 음극이라 농도 변화 작다) · SE 분리막(0 ≤ x ≤ L_SE) · 복합양극(L_SE ≤ x ≤ L_SE + L_p, **단일 입자**: `[인쇄]` "The concentration distribution of positive electrode particles is consistent across different locations").
단자전압 `[인쇄]` 식 (3) `U_bat = U^p_ocp − U^n_ocn + η^p_ct + η_SE + η^n_ct + η_dc`.
해법: 각 확산 PDE 를 Laplace 로 풀어 전달함수(식 17 · 23–24 · 37–40) → **3 차 Padé**(식 18 · 25–26 · SI S.1–S.4). `Ts` = 1 s. 실행시간 `[인쇄]` 0.36–0.54 s / 조건(Table 2).

`[인쇄]` 가정 여섯: 균일 구형 입자(SEM 은 Fig. S1) · 양극 입자 농도 위치 무관 · **"The effective contact area is considered. However, when the concentration of lithium-ion is calculated, assuming a uniform current density distribution on the surface of the active material"** · 음극 과량, 부피 변화 무시 · **"Particle fragmentation and volume changes during charging and discharging are negligible"** · SE 전기중성 + 음이온 이동.

## 3.2 ★★★ 식 단위로 — `A_eff` 는 어디에 있고 어디에 없나

| 식 | `[인쇄]` | `A^p_eff` | `ε_p` |
|---|---|---|---|
| (4)(5) BV | `j^p_ct = j^p_0[exp(α_aFη/RT) − exp(−α_cFη/RT)]`, `j^p_0 = k_p F (c^p_SE)^α_a (c^p_max − c^p_sur)^α_a (c^p_sur)^α_c`, α = 0.5 | — | — |
| **(8)** | `j^p_ct = (I − I^p_dl)/(A^p_eff · a_{s,p} · A · L_p)` ; `j^n_ct = (I − I^n_dl)/(A^n_eff · A)` | **여기만** | `a_{s,p}` 로 |
| (9) | `a_{s,p} = 3ε_p/R_s` | — | 있음 |
| (10) | `I^p_dl = c^p_dl · dη^p_ct/dt` (`c^p_dl` 단위 **F**) | 없음 | 없음 |
| **(15)** | `D_p ∂c_p/∂r|_{R_s} = −I/(a_{s,p} A L_p F)` | **없음** (가정 3) | 있음 |
| (18) | 3 차 Padé, 앞 인자 `−1/(a_{s,p}AL_p) · 3/(FR_s)` = `−1/(ε_p A L_p F)` | 없음 | **용량 극** |
| (28)(35) | SE 원천항 `(1−t⁺)(I − I^p_dl)/(FAL_p)` · `j^p_SE = (I − I^p_dl)/(a_{s,p}AL_p)` | 없음 | 있음 |
| (29)(43) | `D^p_SE = D_SE ε_SE^brug` · `κ_eff = κ_SE ε_SE^brug` | 없음 | `ε_SE` 로 (관계 미기재) |
| (48) | `η^p_ct = (2RT/F) sinh⁻¹(j^p_ct / 2j^p_0)` | 곱으로 | 곱으로 |

`[해석]` (48) 에 (8) 과 (5) 를 넣으면 `j^p_ct/2j^p_0 = (I − I^p_dl) / (2 · A^p_eff · k_p · (3ε_p/R_s) · A L_p F · √c_SE · √(c_max − c_sur) · √c_sur)`.
⇒ **`A^p_eff` 는 이 비 안에서만, 그리고 `k_p` 와 곱으로만 산다.** `ε_p/R_s` 는 이 곱에도 있지만 (15)(18)(용량 · 확산)에서 따로 붙잡힌다.
⇒ 9호 개념 페이지의 곱 `A_eff·ε_p/R_s` 를 이 편의 식으로 다시 쓰면 **`A^p_eff · k_p · ε_p / R_s`** 이고, 그중 **`A^p_eff ↔ k_p` 는 모든 출력에서 정확한 항등**(스케일 대칭)이다. 음극도 같다: `A^n_eff ↔ k_n`.

`[인쇄]` 저자 자신이 이 구조를 결과로 읽는다: "the influence of the effective contact area on cell performance exhibits limited significance when A^p_eff and A^n_eff remain at 1 (Fig. 11(b)), showing minimal deviation from the case with a ratio of 0.3 (Fig. 11(e)). **This outcome is attributed to the model's assumption of uniform current distribution across the surface. In this model, the actual current density primarily impacts the calculation of interface overpotential**, making its impact more significant under high Crate conditions."

## 3.3 ★★ `R_s` 스윕의 문장이 `A_eff` 와 `a_{s,p}` 를 섞는다

`[인쇄]` "halving the R_s yields increased battery capacity extraction. This increase in battery useable capacity arises from the **enlarged effective contact area** and the concurrent reduction in current density."
`[해석]` 모델에서 `R_s` 를 반으로 하면 `a_{s,p}` 가 두 배가 되고 확산 시간 `R_s²/D_p` 가 1/4 이 된다 — **`A_eff` 는 그대로**다. 저자의 "effective contact area" 는 여기서 **비표면적**을 가리킨다.
그리고 `[해석]` Fig. 11a/d 에서 용량을 움직이는 것은 확산(`η^p_d`, §6 · `[도표]` Fig. 9)이다 — 같은 편 Fig. 11b/e 가 보이듯 **면적만 늘리면 용량은 거의 안 움직인다**. ⇒ 한 편 안에서 "contact area" 가 두 양(`A_eff` ↔ `a_{s,p}`)에 쓰인다(D12 의 이웃).

## 3.4 이중층

`[인쇄]` "the electrical double layers at the solid-solid interface are also taken into consideration" — 식 (10), `c^p_dl` = 5.1×10⁻⁶ F · `c^n_dl` = 1.3×10⁻⁷ F(각주 없음).
`[재현]` 인쇄된 곱 면적 `A^p_eff·a_{s,p}·A·L_p` = **1.81 cm²** 로 나누면 `c^p_dl` ≈ **2.8 µF cm⁻²**, 음극 `A^n_eff·A` = 0.32 cm² 로 **0.40 µF cm⁻²** — 이중층 자릿수로 **그럴듯하다**(20호의 ≈1 F cm⁻² 와 반대편).
⚠ 그러나 `c_dl` 이 **F(전체)** 로 고정이라 `A_eff` 가 변해도 `C` 는 안 변한다 — 물리적 이중층은 접촉 면적에 비례해야 한다(`[해석]`, §9 · §10).

---

# 4. 파라미터 출처 — Table 1 각주 분류 (★ 9호 공백 G2 의 답)

`[인쇄]` 각주: a "Measured with Scanning Electron Microscope." · b "Identified by direct measurements." · c "Identified from the experiment. Will be introduced in Sec. 4." · d "Predefined (non-optimized) parameters." · e "Range identified by experiment and optimized by PSO."

| 층 | 파라미터 (`[인쇄]` Table 1 값) |
|---|---|
| **a SEM** | `L_n` 0.192 mm · `L_SE` 0.825 mm · `L_p` 0.085 mm · **`R_s` 9.315 µm** |
| **b 직접** | `A` 7.854×10⁻⁵ m² · `T` 301.15 K |
| **c 실험(§4 에서 소개한다고 함 — 안 함)** | `κ_SE` 0.1395 S m⁻¹ · `D_SE` 1.820×10⁻¹² · `R_dc` 25.05 Ω · `c^n_max` 7.120×10³ · `c^p_max` 2.668×10⁴ mol m⁻³ · `Q` 7.093×10⁻⁴ Ah |
| **d 사전 고정** | `α_a` = `α_c` = 0.5 · `brug` 3.67 · `c_SE,0` 2.972×10⁴ mol m⁻³ |
| **e 실험 범위 + PSO** | **`k_p` 2.263×10⁻¹²** · `k_n` 4.387×10⁻¹¹ m^2.5 mol^−0.5 s⁻¹ · `D_p`(값 "–" — Fig. 8 함수) · `D_n` 2.322×10⁻¹¹ m² s⁻¹ |
| **★ 각주 없음** | **`A^p_eff` 0.4938 · `A^n_eff` 0.4095** · `ε_p` 0.1707 · `ε_SE` 0.8293 · `c^p_dl` 5.1×10⁻⁶ F · `c^n_dl` 1.3×10⁻⁷ F · `t⁺₀` 0.363 · (`D^p_SE` 1.370×10⁻¹² — 식 29 의 유도량이어야 하나 안 맞는다, D4) · (`a_{s,p}` 5.497×10⁴ — 유도량 ✓) |

## 4.1 ★★★ 9호 Table 3 과의 대조 (9호 값은 9호 digest 의 `[인쇄]` 사본)

| | 이 편 (37호) | 9호 | 같은가 |
|---|---:|---:|---|
| 복합양극 NCM wt% | 38 | 56 | 다르다 |
| `L_p` | 85 µm | 98 µm | 다르다 |
| `R_s` | 9.315 µm | 9.466 µm | 1.6 % 차 |
| `ε_p` | 0.1707 | 0.321 | 다르다 |
| `a_{s,p}` | 5.497×10⁴ | 1.017×10⁵ | 다르다 (둘 다 `3ε_p/R_s` ✓) |
| **`A^p_eff`** | **0.4938** | **0.4938** | **네 자리 같다** |
| **`A^n_eff`** | **0.4095** | **0.4095** | **네 자리 같다** |
| `κ_SE` | 0.1395 | 0.3985 | 다르다 |
| `c^p_max` | 2.668×10⁴ | 2.741×10⁴ | 2.7 % 차 |
| `c^n_max` | 7.120×10³ | 1.065×10⁴ | 다르다 |
| `brug` | 3.67 | 3.67 | 같다 (d 사전 고정) |
| `T` | 301.15 K | 301.15 K | 같다 |

`[해석]` 조성 · 두께 · `ε_p` · `κ_SE` · `c^n_max` 가 모두 다시 정해졌는데 **접촉 면적비 두 개만 네 자리까지 그대로**다. 셀에 맞춰 다시 적합했다면 우연의 일치가 두 번 겹쳐야 한다.
⇒ `A_eff` 는 **셀 성질로 측정 · 적합된 양이 아니라 모델 상수로 운반된 값**이다. §3.2 의 항등(`A_eff ↔ k_p`) 때문에 운반해도 적합이 안 깨진다 — `k_p` 가 흡수한다. 9호는 `k_p` 를 `[인쇄]` "not disclosed" 로 가렸다.
(부수: 9호 Battery B 의 `k_LAM` = 0.0001707 과 이 편 `ε_p` = 0.1707 은 숫자열이 같다 — 의미를 부여하지 않는다.)

## 4.2 ★★ `R_s` "Measured with SEM" ↔ SI Fig. S1

`[도표]` Fig. S1(×5000, 스케일바 2.0 µm = 23 px → 11.5 px µm⁻¹, 시야 ≈52 × 34 µm, 스탬프 **2023.11.21**, 20 kV, SEI):
단일 입자 **지름 ≈1–3 µm**(반경 ≈0.5–1.5 µm), 가장 큰 응집체 **지름 ≈7 µm**. `[재현]` 문턱 분할(응집체가 붙어 과대) 등가 지름 중앙값 2.5 µm.
Table 1 `R_s` = 9.315 µm → **지름 18.6 µm = 214 px = 시야 높이의 55 %** 인 입자가 있어야 하는데 **시야에 하나도 없다.**
⇒ `R_s` 는 이 SEM 의 단일 입자 반경의 **≈6–18 배**, 가장 큰 응집체 반경의 ≈2.6 배다. 9호 digest 가 9호 Fig. 5a 에서 잰 ≈1.05 µm(→ 9 배)와 같은 방향 · 같은 자릿수 — **9호의 "9 배" 는 9호의 결함이 아니라 이 편에서 상속된 것이다.**
⚠ 한계: 투영 SEM · 분말 시료(복합체 아님) · 판독 ±0.5 µm. 그리고 **스탬프 날짜가 투고(2023-09-13) 뒤, 수정본(2024-01-03) 전**이다 — Fig. S1 은 심사 중에 찍혔을 가능성이 있고, 9.315 µm 가 그 전에 다른 근거(제조사 D50 등)로 정해졌을 수 있다. 원문은 말하지 않는다.
`[해석]` §3.2 의 묶음으로 보면 `R_s` 는 **데이터로 정해지지 않는다**: 확산에서는 `R_s²/D_p`(Bizeray 묶음 `τ_d`)로, 과전압에서는 `A_eff·k_p·ε_p/R_s` 로만 나오고 `D_p` · `k_p` 가 PSO 로 풀린다 — 틀린 `R_s` 는 `D_p` 와 `k_p` 가 흡수한다.

## 4.3 ★★ `k_p` 가 측정 범위 밖으로

`[도표]` Fig. 5d(LSV–Tafel, 11 점, SOC 0–1): SOC 0 **≈7.2×10⁻¹¹**, 0.1 ≈2.2, 0.2 ≈1.8, 0.3 ≈1.5, 0.4 ≈1.1, 0.5–0.9 **≈0.7–0.9×10⁻¹¹**, 1.0 ≈1.8×10⁻¹¹ (판독 ±0.1×10⁻¹¹).
Table 1 `k_p` = **2.263×10⁻¹²** — 각주 e "Range identified by experiment and optimized by PSO" 인데 **측정 11 점의 최솟값(≈0.7×10⁻¹¹)보다 ≈3 배 작다**.
`[재현]` 중간 SOC 대비 0.25 배, 곱 `A^p_eff·k_p` = 1.12×10⁻¹² 로는 0.12 배. LSV 의 `j_0` → `k_p` 환산에 쓴 면적(기하 `A`? `a_{s,p}AL_p`? `A_eff` 포함?)이 인쇄되지 않아 어느 쪽이 "같은 양" 인지 모른다(G3).
그리고 측정은 SOC 에 따라 **≈10 배** 변하는데 모델은 상수 하나다. `[해석]` 이 차이(모양 · 크기)를 `D_p,ref(C-rate)` · `trD_p(x)`(§5)와 `A_eff` 가 나눠 먹는다.

---

# 5. 식별 절차 (§4)

`[인쇄]` "The parameters are identified in Matlab to obtain the optimal set of parameters. In order to determine the electrochemical parameters of the ASSBs through particle swarm optimization (PSO), the algorithm is initialized using the parameter set obtained from the experiments [36]. It is explicitly stated that constant current charging and discharging conditions (0.4C, 1.0C, 1.2C, 2.0C) are utilized as the dataset for parameter identification, with the remaining conditions used as the validation set."
목적함수 `[인쇄]` 식 (55) `J = min[RMS(U_mea − U_bat)]`. PSO 원전 [36] = Rahman, Anwar, Izadian, *JPS* 307 (2016) 86 (9호 [44] 와 같다).

## 5.1 ★★★ `D_p` 는 율마다 다른 함수다

`[인쇄]` Fig. 8 캡션: **`D_p = D_p,ref(Crate) ∗ trD_p(x)`**. `[인쇄]` "Fig. 8(a) illustrates the reference diffusion coefficients (D_p,ref) for different C-rates. Researchers have offered a couple of possible explanations for involving rate-dependent diffusivities" (응력 [37] · non-Fickian [38,39]).
`[도표]` Fig. 8a: `D_p,ref` ≈**1.1×10⁻¹⁴** (0.4 C) → ≈1.6 (0.6) → ≈2.45 (1.0) → ≈2.5 (1.2) → ≈3.8 (1.6) → ≈**4.7×10⁻¹⁴** (2.0 C) — **0.4 → 2 C 에서 ≈4.3 배**, 꺾임이 0.6 · 1.0 · 1.2 · 1.6 C 에 보인다(±0.1×10⁻¹⁴).
`[도표]` Fig. 8b: `trD_p(x)` ≈0.2–0.37(x 0.25–0.95), 양 끝에서 ≈1.2(x 0.18) · ≈1.4(x 1.0).
`[재현]` 유효 `D_p` 중간 x: 0.4 C ≈3×10⁻¹⁵ · 2 C ≈1.4×10⁻¹⁴ ↔ `[도표]` GITT Fig. 5b 중간 SOC ≈2×10⁻¹⁴ — 적합값은 GITT 의 0.15–0.7 배.

`[해석]` ★ **율마다 다시 정한 `D_p,ref` 는 율 스윕의 정보를 먹는 손잡이다.** 29호 처방("율 스윕으로 `η(i)` 를 지워 `θ·Q` 를 뗀다")의 전제는 모델이 율에 **같은 파라미터**로 답해야 한다는 것이다.
여기서는 율에 따른 잔여 손실 — 계면(`A_eff·k_p`)이든 접촉이든 SE 수송이든 — 이 **`D_p,ref(C-rate)` 로 들어갈 자리가 있다.** 7 율 데이터가 있는데도 곱을 가를 수 없는 이유다.
그리고 `[도표]` 꺾임이 **검증 율(0.6 · 1.6 C)** 에도 있어 검증 조건의 `D_p,ref` 가 학습 율의 보간이 아닐 수 있다(D11, G9). `[재현]` Table 2: 학습 8 조건 RMSE 평균 20.2 mV ↔ 검증 6 조건 18.7 mV · 동적 18.1 — **검증이 학습보다 낫다.**

## 5.2 오차 (Table 2, `[인쇄]` + `[재현]`)

0.4 C 방전 11.5 · 충전 7.7 mV … 1.6 C 방전 34.3 · 2.0 C 방전 34.2 mV · 동적 18.1 mV. 휴지 끝 오차 0.03–6.4 mV.
`[재현]` 15 조건 RMSE 평균 **19.49 mV** ✓(인쇄 19.5) · 휴지 끝 평균 **2.76 mV** ✓(인쇄 2.8). 본문 "generally … within the range of 30 mV" · 결론 "within 35 mV" — 1.6 · 2.0 C 방전이 30 을 넘는 것을 본문이 적는다.
⚠ 오차 막대 · 셀 반복 0. `[도표]` Fig. 6 곡선 적합은 전 율에서 눈으로 겹친다.

---

# 6. 민감도 (§4.3, Fig. 11) — 무엇이 흔들리고 무엇이 안 흔들리나

`[인쇄]` Fig. 11 캡션: "(a, d) The influence of R_s … (b, e) The influence of the contact area … (c) The influence of L_SE … (f) The influence of ε_p … The simulations are conducted at a C-rate of 0.4."

`[도표]` (Fig. 11, 0.4 C 방전, ±0.02 V · ±0.1×10⁻⁴ Ah):

| 판 | 흔든 것 | 전압 | **용량 끝점** |
|---|---|---|---|
| a | `0.5 R_s` | 곡선 전체가 ≈+0.15–0.2 V 위 | **6×10⁻⁴ 에서 아직 ≈2.8 V** — 축 밖으로 연장 |
| d | `1.5 R_s` | ≈−0.15 V | **≈5.3×10⁻⁴** (−12 %) |
| b | `A^n_eff = A^p_eff = 1.0` | **≈+0.06–0.07 V** 평행 이동 | **≈6.0×10⁻⁴ 그대로** |
| e | `A^n_eff = A^p_eff = 0.3` | **≈−0.03–0.04 V** | **≈6.0×10⁻⁴ 그대로** |
| c | `0.1 L_SE` | ≈+0.01–0.02 V | 그대로 |
| f | `ε_p = 0.32` (신품 0.1707) | ≈+0.15–0.3 V | 곡선이 6×10⁻⁴ 에서 **≈3.15 V 로 잘림** — 용량 증가를 그림이 보이지 않는다(D13) |

`[재현]` (b)(e) 크기 검산 — 인쇄된 파라미터로 0.4 C · `c_sur = c_max/2` · `c_SE = c_SE,0`:
`j^p_0` = 0.502 A m⁻² · 면적 `A^p_eff·a_{s,p}AL_p` = 1.812×10⁻⁴ m² → `η^p_ct` **63.7 mV** (`A_eff` 1.0: 36.8 · 0.3: 86.7);
`η^n_ct` (`c_n` 절반 가정) **67.5 mV** (1.0: 33.7 · 0.3: 81.9). 합의 이동 **+60.7 / −37.4 mV** ↔ `[도표]` ≈+60–70 / ≈−30–40 mV. ✓
그리고 같은 계산이 Fig. 9 와도 맞는다: `[도표]` Fig. 9b 0.4 C `η^p_ct` ≈−0.07 · `η^n_ct` ≈−0.07 V ↔ `[재현]` 64 · 68 mV; 2 C `[도표]` ≈−0.17–0.24 · ≈−0.16 ↔ `[재현]` 143 · 147 mV(중간 SOC). ⇒ **Table 1 의 `k_p` · `A_eff` 가 그림을 만든 값이다.**

`[해석]` "minimal deviation" 은 **용량**에서 맞고 **전압**에서는 RMSE(11.5 mV)의 3–5 배다. 즉 `A_eff` 는 전압 데이터에 **보이는** 손잡이다 — 다만 `k_p` 와 구별되지 않는 모양으로(§3.2).
이것이 이 편에서 `A_eff` 가 "측정 불필요한 상수" 처럼 운반될 수 있었던 이유와 **같은 이유**다.

---

# 7. `[재현]` 검산 — 맞는 것과 안 맞는 것

| 검사 | 식 | 결과 |
|---|---|---|
| ✅ 비표면적 | `3·0.1707/9.315e-6` | **5.4976×10⁴** ↔ 5.497×10⁴ |
| ✅ 면적 용량 | `0.903 × 0.7854` | **0.7092 mAh** ↔ `Q` 0.7093 mAh |
| ✅ 체적 폐합 | `ε_p + ε_SE` | **1.0000** 정확 — `[인쇄]` "(ignore the pore)" (9호와 같은 규약, 이 편은 각주로 명시) |
| ✅ wt% → vol% | 38:57:5, 밀도 4.8 · 1.64 · 2.0 g cm⁻³ **가정** | **0.175** ↔ `ε_p` 0.1707 (2.6 % 차) |
| ⚠ 이론 용량 | `ε_p A L_p c^p_max F` | **0.815 mAh** → `Q/Q_th` = **0.87** |
| ⚠ `c^p_max` | NCM811 이론(밀도 4.75–4.8 가정, M 97.28) ≈4.88–4.93×10⁴ | 인쇄값은 그 **≈0.54 배** — 유효값(G4) |
| ⚠ N/P | `c^n_max A L_n F / Q` | **4.06** (모델 N/P; 9호 `[재현]` 3.14). `c^n_max` 7.12×10³ 은 Li₃.₇₅Si 완전 리튬화 ≈8.2×10⁴ 의 ≈9 % — 9호 digest 와 같은 성격의 유효값 |
| ❌ `D^p_SE = D_SE ε_SE^brug` (식 29) | `1.820e-12 × 0.8293^3.67` | **9.16×10⁻¹³** ↔ 인쇄 **1.370×10⁻¹²** (×1.50). 역산 `brug` ≈**1.52** (고전 Bruggeman 1.5) — D4 |
| (참고) `κ_eff` | `0.1395 × 0.8293^3.67` | 0.0702 S m⁻¹ (표는 "–") |
| ❌ `D_SE` (식 52) | `[도표]` Fig. 5c 직선 기울기 ≈−1.61×10⁻⁴ s⁻¹ (−5.0 → −5.58 / 3600 s) × `L_SE²/π²` | `L_SE` = 0.825 mm 면 **1.11×10⁻¹¹** ↔ 인쇄 1.820×10⁻¹² (**×6.1**). 인쇄값을 내려면 `L` = **0.334 mm** — 대칭 셀 두께 미기재(G8) |
| ✅ Table 2 평균 | 15 조건 | 19.49 / 2.76 mV ✓ |
| ⚠ 이완 시상수 | `R_ct = RT/(F j^p_0 · 면적)` × `c^p_dl` | 중간 SOC **285 Ω × 5.1 µF = 1.5 ms**, x 0.99 에서 1.4 kΩ → **7 ms** ↔ `[도표]` Fig. 9c/f 삽도 `η^p_ct` 이완 ≈**10² s** — **4–5 자릿수** (D7) |

---

# 8. 9호 digest 공백 중 여기서 풀린 것 / 안 풀린 것

| 9호 공백 | 이 편 |
|---|---|
| **G1 OCP 출처** | **절반** — `[인쇄]` 완전지 OCV + 양극 반쪽전지 OCP(상대극 Li-In) → 음극 OCN = **차감**, 정렬은 `[인쇄]` "by corresponding to the peaks of the two dQ/dV curves"(Fig. 4a,b). 측정 조건 0(G5), `[인쇄]` 분극 포함 인정. ⚠ 이것은 **이 편 셀(38 wt%)** 의 곡선이다 — 9호 셀(56 wt%)에 같은 곡선을 썼는지는 9호가 말하지 않는다 |
| **G2 provenance** | **부분** — 각주 5 종. 단 `A_eff` · `ε_p` · `c_dl` 은 각주 없음(G1 · G2) |
| **G3 비공개 6 개** (`c_p0` · `c_n0` · `k_p` · `k_n` · `D_p` · `D^p_SE`) | 이 편 셀의 `k_p` · `k_n` · `D^p_SE` 는 **인쇄**, `D_p` 는 그림(함수), `c_p0` · `c_n0` 는 "–". ⇒ **9호의 비공개는 이 편의 관행을 따른 것이 아니다.** 산업체 공저자(He, CRediT "Resources")의 영향은 지면으로 판단할 수 없다 |
| **G4 PSO 설정** | **부분** — 목적함수 식(55) · 실험값 초기화 · 학습/검증 분할. 경계 수치 · 개체수 · 반복 · 시드 0 |
| 해법 · `A_eff` 정의 | ✅ Laplace + 3 차 Padé, `A_eff` 는 식 (8) BV 분모에만 |
| **9호 §9 Fig. 5 의 "9 배"** | ✅ **원인이 여기 있다** — `R_s` ≈9.3–9.5 µm 가 두 편에 공통이고 두 편의 SEM 이 모두 ≈1 µm 입자를 보인다(§4.2) |
| 9호 D2 (`ε_se` 처리) | 신품 규약은 같다(`ε_p + ε_SE = 1`, "ignore the pore"). 노화 규칙은 이 편에 없다(노화 0) |

**Q5 (`[해석]`)**: 양극 OCP 는 Li-In 상대극으로 쟀는데 Fig. 4a 는 "(vs Li)" 로 그렸다(`[도표]` OCP ≈3.5–4.35 V; GITT Fig. 5a 의 전위 축은 ≈3.0–3.6 V 대라 **vs Li-In 으로 보인다** — 두 그림 사이 ≈0.5–0.7 V, 환산 미기재).
그런데 **OCN 을 `OCP − OCV` 차감으로 만들었기 때문에 기준 오프셋이 얼마였든 전부 OCN 에 들어가고 완전지 모델(`U^p − U^n`)에서는 상쇄된다.** 계보의 Q5 형태로 **열세 번째 — "차감 흡수: 기준 오차가 유도된 상대극 곡선으로 들어가 완전지 식에서 사라진다"**.
대가는 OCN 이 **물리적 Li-Si OCP 가 아니라** OCP · OCV 측정 조건 차(분극 · 이력)까지 담은 잔차라는 것이다. `[도표]` Fig. 4a OCN ≈0.27 V(SOC 0) → ≈0.18 V(SOC 1), ≈0.1 V 기울기 — 9호 digest 의 "이 셀의 상대극은 평탄하지 않다" 를 곡선으로 확인.

---

# 9. ★★★ (d) 이 모델로 ASSB 합성 truth 를 만들면 — 27호 경고의 원형

`degradation-degeneracy/` 는 PyBaMM 합성 truth 로 LLI/LAM 분할의 축퇴를 채점한다(`degradation-degeneracy/README.md`). 그 파이프라인의 `LAM_PE` 정의는
`degradation-degeneracy/docs/07_LAM_LLI.md` §2: 양극 활물질 부피분율을 `(1 − lam_pe)` 로 줄이고 **죽은 부피를 공극(전해질)으로 돌린다**, 그리고 같은 절의 물리 목록에 **"전기적 단절 (도전재 네트워크 이탈, 바인더 열화)"** 이 `LAM` 의 원인으로 들어 있다.
(우리 쪽 수치는 거기가 정본이다 — 여기 옮기지 않는다.)

이 편의 모델 가족(9호 포함)을 ASSB truth 생성기로 쓸 때 접촉 손실을 넣을 수 있는 자리는 둘뿐이다 (`[추론]`):

| 갈래 | 넣는 곳 | truth 가 미리 정하는 답 | 처방 입력에 미치는 것 |
|---|---|---|---|
| **① `A_eff(N)`** (이 편의 신규 손잡이) | BV 분모 | 용량 불변(§6 Fig. 11b/e) ⇒ **OCV · 저율 적합에 안 보인다**. 유한 율에서는 **`k_p(N)` 와 정확히 같다** ⇒ "접촉 손실 ↔ 계면 화학" 이 truth 에서 구별 불가 | `c_dl` 고정 ⇒ `R_ct ∝ 1/A_eff`, `C` 불변 ⇒ `τ = R·C ∝ 1/A_eff` — **16호 처방(면적 변화면 `R·C` 불변 · `C ∝ 면적`)이 truth 에서 거짓**. 처방을 이 truth 로 채점하면 처방이 틀렸다고 나온다 |
| **② `ε_p(N)`** (9호의 노화 방식 = 우리 `LAM_PE` 코드와 같은 형) | 용량 + `a_{s,p}` + 확산 | **정의상 `LAM_PE`** — 분할 시험이 동어반복. 그리고 `a_{s,p}` 가 같이 줄어 율 손실이 섞인다(9호 `[재현]` 증폭 1.32–1.60) | 죽은 부피를 어디로 보내나가 남는다 — 우리 코드처럼 전해질로 보내면 `ε_SE ↑ → κ_eff ↑`(9호 D2 의 "늙을수록 이온전도가 좋아진다" 가지). ASSB 의 비연결 NCM 은 **고체로 남는다** |

⇒ **없는 것은 `θ`(입자 통째 비연결 분율)의 독립된 자리**다 — 27호가 P2D 에서 보인 `1 − u` 바닥(비연결 입자가 초기 SOC 에 머묾, 리튬을 안고 죽는 `_li` 형)을 넣을 칸이 이 편 모델에 없다.
`[추론]` ASSB truth 가 카드의 물음을 **시험할 수 있으려면** 최소한: (i) `θ` 가 용량에 곱해지되 `ε_p` 와 별개 · (ii) 비연결 입자가 자기 SOC 의 리튬을 붙든다(`_li`) · (iii) 죽은 부피가 전해질이 되지 않는다 · (iv) `θ` 에만 반응하는 조작(압력 되돌림 — [[assb-pressure-reapplication-separation-test]])이나 관측이 truth 에 있다 · (v) 이중층이 접촉 면적에 비례한다.
이 넷 중 하나라도 빠지면 "OCV 적합이 접촉 손실을 `LAM_PE` 와 못 가른다" 는 **결과가 아니라 가정**이 된다.

---

# 10. 곱 축퇴 처방 — 스무 번째 적용 (처방의 원천 모델에 건다)

입력 점검 (처방 표 `concepts/assb-lampe-contact-product-degeneracy.md`):
- **1단계 `R_CT·C_dl`** — ⚠ **모델 구조가 막는다.** `C` 는 F 단위 상수(면적 무관), `R_ct` 는 미인쇄(`[재현]` 285 Ω). 이 모델 안에서 `A_eff` 를 바꾸면 `R·C` 가 **바뀐다** — 처방의 전제와 반대. 실측 EIS 는 이 편에 0(κ_SE 차단 셀뿐).
- **2단계 면적 대조군** — 모델 안에서만: Fig. 11b/e(`A_eff` 1 ↔ 0.3)는 "면적만 바꾼 쌍" 의 **모델판**이고, 결과는 용량 불변 · 전압 평행 이동. 실측 대조군 0.
- **3단계 `Ea`** — ❌ 301.15 K 한 점.
- **4단계 `C` 상한** — ✅ `[재현]` 2.8 µF cm⁻² 로 통과. ⚠ 그러나 그림(Fig. 9c/f)의 `η_ct` 이완 ≈10² s 는 이 `C` 로 나올 수 없다(1.5–7 ms) — **4단계를 거꾸로 건 첫 표본**: 파라미터는 상한 안인데 그 파라미터가 만든다는 그림이 상한 밖의 시상수를 보인다(D7).
- **율 스윕 줄** — ⚠ 7 율이 있다. 그러나 **율마다 다시 맞춘 `D_p,ref(C-rate)`** 가 있다 ⇒ ★ **율 스윕 줄의 세 번째 실패 조건**: "율에 따라 다시 정하는 파라미터가 모델에 있으면, 율 스윕이 곱을 가를 정보는 그 파라미터에 먼저 들어간다." 29호(종료 율 평탄) · 30호(스윕 중 표류)와 **별개**.
- **외부 기준 줄** — GITT 식 (51) 의 `S` 가 곱의 면적 인자를 **측정 단계에서** 고정한다(값 미인쇄). 31호 "상수 입력" 과 같은 부류이고, 여기서는 그 상수가 **모델의 `A_eff` 와 다른 자리**(확산 `S²` ↔ BV `A_eff`)에 들어간다.

⇒ **이 적용이 처방 표에 더하는 것 둘** (`[해석]`):
1. **"`A_eff ↔ k` 항등"** — 표면 피복형 접촉 손실은 이 모델 가족에서 `LAM` 이 아니라 **계면 반응 상수의 쌍둥이**다. 처방 1단계가 가르려는 것이 바로 이 쌍(`θ` ↔ `j₀`)인데, 모델이 `C` 를 면적과 떼어 놓으면 처방이 쓸 신호가 truth 에 없다.
2. **"율별 재적합 파라미터는 율 스윕을 먹는다"** — 처방 표 율 스윕 줄의 ↳ 실패 조건 셋째.

---

# 11. 채움표 행 (Q1–Q8)

| Q | 이 편 |
|---|---|
| **Q1 정량** | **없다 — `θ(N)` 0/37.** 접촉 양은 `A^p_eff` 0.4938(무차원, BV 분모) 하나 — **출처 각주 없음 · 측정 절차 없음 · 9호와 네 자리 같음**(층: **inherited-constant**). 신품만(노화 0). 입자 통째 비연결(`θ`)의 자리 없음 |
| **Q2 독립 관측** | **없다** — GITT · LSV · 대칭 셀 · 차단 셀 EIS · SEM 은 전부 **신품 파라미터 추출용**이고 접촉 ↔ LAM 을 가르는 데 쓰이지 않는다 |
| **Q3 라벨 층위** | 칸 없음 · **층 하나: "footnote-typed parameter table — the contact knob is the unmarked row"**. 각주 5 종으로 층위를 표기한 계보 첫 모델 편인데, 신규 요소 둘(`A_eff` · `c_dl`)과 용량 손잡이(`ε_p`)가 무표기. 부수: PSO 값이 측정 범위 밖(`k_p` ≈0.25×) · 율별 재적합(`D_p,ref`) · 식 29 불일치(`D^p_SE` ×1.50) |
| **Q4 유일성** | **ASSB 0 — 스물아홉 번째 성질**(판정 (c)). 누적 0.5(29호) 그대로. `identifiab` 0 · "sensitivity" = 0.4 C OAT 6 판 |
| **Q5 Li-In** | **이동 없음** — 반쪽전지 상대극 Li-In, "(vs Li)" 표기 · 환산 미기재. **열세 번째 형태 "차감 흡수"**(§8) |
| **Q6 압력** | **이동 없음** — `[인쇄]` SI Table S1: 제작 480 · 36–50 · 120 · 360 MPa, 운전 **50 MPa 유지**. 보고 · 통제, 스윕 0 |
| **Q7 dead Li** | 해당 없음 (Li-Si) |
| **Q8 화학 · OCP** | **이동 없음** — NCM811(LiBO₃ 코팅)/LPSCl/Li₄.₄Si, 기존 화학. OCP · OCV · OCN 곡선은 그림뿐(수치표 0). OCN 기울기 `[도표]` ≈0.1 V / SOC 전역 |

**누적 ≈16.0 → ≈16.0 (새 칸 0).**

---

# 12. 어긋남 (실제로 어긋난 것만)

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** ★★★ | `R_s` 9.315 µm "Measured with SEM" ↔ SI Fig. S1 단일 입자 반경 ≈0.5–1.5 µm, 최대 응집체 ≈3.6 µm | §4.2 `[도표]` |
| **D2** ★★★ | `A^p_eff` · `A^n_eff` 가 조성이 다른 9호 셀과 네 자리 일치 · 각주 없음 | §4.1 |
| **D3** ★★ | `k_p` Table 1 2.263×10⁻¹² 가 "range identified by experiment" 인 Fig. 5d 측정 11 점(≈0.7–7.2×10⁻¹¹) 밖 | §4.3 `[도표]` |
| **D4** ★★ | `D^p_SE` 1.370×10⁻¹² ≠ 식 (29) `D_SE ε_SE^3.67` = 9.16×10⁻¹³ (역산 brug ≈1.52) | §7 `[재현]` |
| **D5** ★ | 식 (52) 부호 — `[인쇄]` `ln(ΔV) = (π²D_SE/L²_SE) t + const`(양의 기울기) ↔ `[도표]` Fig. 5c 음의 기울기. 그리고 그 기울기로 `L_SE` 0.825 mm 를 쓰면 `D_SE` 가 인쇄값의 6.1 배 | §7 |
| **D6** ★★ | `A_eff` 1 ↔ 0.3 "minimal deviation" ↔ `[재현]` 0.4 C 전압 +61 / −37 mV (RMSE 의 3–5 배), `[도표]` Fig. 11b/e 도 그만큼 떨어져 있다 — 용량에서만 "minimal" | §6 |
| **D7** ★★ | Fig. 9c/f `η^p_ct` 이완 ≈10² s ↔ 인쇄 파라미터 `R_ct·c_dl` 1.5–7 ms. 해석 셋(`Ts` = 1 s 이산화 인공물 · 그림과 다른 파라미터 · `η_ct` 의 다른 정의) 중 지면으로 못 가른다 | §7 `[재현]` |
| **D8** ★ | 식 (47) 마지막 항의 `κ^p` 가 정의되지 않았다(Table 1 은 `κ_eff` "–", 식 43 은 `κ_eff`) | `[인쇄]` 쪽 렌더 확인 |
| **D9** ★ | 각주 c "Will be introduced in Sec. 4" — §4 는 `c^p_max` · `c^n_max` · `R_dc` · `Q` 의 식별을 소개하지 않는다 | G4 |
| **D10** ★ | Fig. 4b dQ/dV 봉우리 이동(`[도표]` 낮은 봉우리 3.42 → 3.56 V ≈0.14 V · 높은 봉우리 3.88 → 4.10 V ≈0.22 V)이 Fig. 4a OCN(≈0.25 V 중간 SOC → ≈0.19 V 높은 SOC)과 **크기도 방향도** 안 맞는다. dQ/dV 측정 율 미기재 — 저율 분극이면 설명될 수 있다 | `[도표]` ±0.02 V |
| **D11** ★ | Fig. 8a `D_p,ref` 꺾임이 검증 율 0.6 · 1.6 C 에 있다 — 학습 율 보간이면 직선이어야 하는 구간 | `[도표]` |
| **D12** ★ | "effective contact area" 가 §4.3 에서 `a_{s,p}`(비표면적)를 가리킨다(`R_s` 절반 → "enlarged effective contact area") — 모델의 `A_eff` 는 그대로 | §3.3 |
| **D13** ★ | Fig. 11f `ε_p` 0.32 곡선이 6×10⁻⁴ Ah 에서 잘려 본문의 "volumetric capacity" 향상을 보이지 않는다 — 그림이 보이는 것은 전압 상승(분극 감소)뿐 | `[도표]` |
| **D14** ★ | 결론 "space charge layer … small influence on the discharge profile" — `c_dl` 을 흔든 그림 · 표가 없다 | G12 |

---

# 13. 그림 — 무엇을 봤나

크로퍼 13 항목(Fig. 1–11 + Table 1 · 2) + SI 에서 직접 꺼낸 Fig. S1 = **14 항목**. `wiki/raw/figures/li2024_assb-composite-cathode-model-contact-area-edl/`.

**본 것 (8 + 표 1)**: **Fig. 2**(모델 모식 — 모든 NCM 입자가 탄소 · SE 에 닿게 그려졌다, 비연결 입자 0) · **Fig. 4**(OCV/OCP/OCN · dQ/dV · 동적 입력 — 확대 재판독) · **Fig. 5**(GITT · `D_p`(SOC) · 대칭 셀 이완 · `k_p`(SOC)) · **Fig. 6**(7 율 적합) · **Fig. 8**(`D_p,ref`(C-rate) · `trD_p`(x)) · **Fig. 9**(과전압 분해 0.4 · 2 C + 이완) · **Fig. 11**(OAT 스윕 6 판) · **Fig. S1**(SEM — 확대 크롭 + 스케일바 픽셀 계측) · **Table 1 상단**(각주 위첨자 확인).
**본문과 어긋난 그림**: Fig. 5c(식 52 부호) · Fig. 5d(`k_p` 인쇄값이 범위 밖) · Fig. 9c/f(이완 시상수) · Fig. 11b/e("minimal") · Fig. 11f(잘림) · Fig. 8a(검증 율 꺾임) · Fig. 4b(봉우리 이동) · Fig. S1(`R_s`).
**안 본 것**: Fig. 1(흐름도) · Fig. 3(압력 셀 모식 · 사진) · Fig. 7(율별 충방전 + 이완 14 판 — Table 2 의 RMSE 로 대신) · Fig. 10(동적 사이클 적합) · Table 2 이미지(텍스트로 읽음) · SI 수식 그림 S.1–S.4(WMF — 전해질 전달함수의 Padé 계수, 이 digest 의 물음에 안 걸린다).

---

# 14. 참고문헌 중 후속 후보 (40 편 중)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| Raijmakers, Danilov, Eichel, Notten, *Electrochim. Acta* **330** (2020) 135147 | [14] | 이 편 이중층 항의 조상(`[인쇄]` "integrating the electrical double layer capacitance … geometrical capacitance"). 26호가 데이터를 빌린 원전과 같은 저자군 | `c_dl` 이 면적에 비례하는가 · 처방 1단계 |
| Deng, Hu, Lin, Xu, Li, Guo, *IEEE Trans. Transp. Electrif.* **7** (2021) 464 | [29] | ASSB 축약 모델(ROM) — `A_eff` 형 손잡이가 있는지 | (a) 형태 비교 · Q4 |
| Kim, Lin, Abbasalinejad, Kim, Chung, *Electrochim. Acta* **317** (2019) 663 | [21] | ASSB 상태 추정(EKF) — 추정기에서 접촉/용량 손잡이 처리 | Q3 · Q4 |
| Froboese, v. d. Sichel, Loellhoeffel, Helmers, Kwade, *JES* **166** (2019) A318 | [30] | `brug` 3.67 의 출처 — 복합양극 미세구조 → 이온전도. D4 의 1.52 와 대조 | 24호 `τ` ↔ `τ²` 이름 충돌 |
| Koerver et al., *Energy Environ. Sci.* **11** (2018) 2142 | [16] | 화학-기계 팽창 — 23호(Koerver 2017)의 후속 · Janek 계보 | Q1 |
| Rahman, Anwar, Izadian, *JPS* **307** (2016) 86 | [36] | PSO 원전(9호 [44] 와 같다) — 경계 · 개체수 관행 | G3 |

큐 37(Conforto 2021) · 38(Yu 2024) 은 이 편에 **인용되지 않는다.**

---

# 15. 이 digest 가 주장하지 않는 것

- **`A_eff = 0.4938` 이 틀렸다고 주장하지 않는다.** 주장은 **출처가 지면에 없고, 이 모델에서 데이터로 정해질 수 없다**(`k_p` 와의 항등)는 것까지다.
- **`R_s` 가 틀렸다고 단정하지 않는다** — Fig. S1 은 분말 투영 SEM 한 장이고 스탬프 날짜상 `R_s` 결정 뒤에 찍혔을 수 있다. 주장은 **"Measured with SEM" 이라는 각주를 이 편의 SEM 이 지지하지 않는다**는 것까지다.
- **D7(이완 시상수)을 모델 오류로 단정하지 않는다** — 코드가 없다. 인쇄 파라미터로 계산한 `R·C` 와 그림의 시상수가 4–5 자릿수 다르다는 것까지다.
- **"이 모델 가족이 접촉 손실을 원리적으로 못 다룬다" 고 일반화하지 않는다** — 이 편 · 9호 두 편의 식 구조에 관한 것이다. `θ` 를 따로 가진 ASSB 연속체 모델이 있을 수 있다(확인 안 됨).
- **§9 의 합성 truth 함의는 `[추론]`** 이고, 우리 파이프라인을 이 모델로 돌려 본 것이 아니다. 우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본이다.
- **`[재현]` 과전압 검산은 `c_SE = c_SE,0` · `c_sur = c_max/2` · 음극 농도 절반을 가정**한 점 계산이다. Fig. 9 · 11 과 자릿수가 맞는다는 것까지를 주장한다.
