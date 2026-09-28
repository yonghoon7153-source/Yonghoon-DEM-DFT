---
title: "Masias A., Felten N., Garcia-Mendez R., Wolfenstine J., Sakamoto J. 2019 — Elastic, plastic, and creep mechanical properties of lithium metal (J. Mater. Sci. 54, 2585–2600)"
source_url: local-upload/23._Elastic_plastic_and_creep_mechanical_properties_of_lithium_metal.pdf + 23._Sup_Elastic_plastic_and_creep_mechanical_properties_of_lithium_metal.pdf
source_url_note: "본문 PDF 16 쪽(J. Mater. Sci. METALS · 그림 10 · 표 3 · 식 (1)–(7) · 참고문헌 34, 구독 논문) + ESM PDF 2 쪽(Table S1 인장 creep 7 행 · Table S2 압축 5 행 × 3 시각 — 표 둘뿐, 그림 0). 그림 자동 크롭 6 장(Fig. 4 + Table 1–3 + Table S1–S2) + 수동 크롭 9 장(Fig. 1 · 2 · 3 · 5 · 6 · 7 · 8 · 9 · 10 — 캡션 왼쪽 여백 · 래스터 오른쪽 배치를 자동 추출이 '그래픽 없음' 으로 제외). 3차 묶음 파일 23 (2차 묶음 큐 번호와 별개). 21호 ref 49 · 5호 ref 15 · 46호 ref 51 의 원전([10])을 인용하는 편."
source_doi: 10.1007/s10853-018-2971-3
source_license: "© Springer Science+Business Media, LLC, part of Springer Nature 2018 — 구독 논문(오픈액세스 아님). 이 digest 는 인용 · 요약 · 재현 계산만 담는다"
pdf_sha256: 125ec6ace593f9ec10eb4d538c49489ba8fa33efc7889d66565bb7286126e869
si_sha256: f0a0726ff71d15e6521e4e5ba5347980b160165a3d67195fb1c89505ae6809ff
ingested: 2026-09-28
sha256: 12579a0e8568bfa67f46a0825e03acce1616066fa9663c1b78db738e94a2aa95
---
# 수집 목적

`assb` 섹션 **61호** — **3차 묶음 파일 23**(3차 묶음 셋째 편). 3차 묶음의 파일 번호 21–33 은 2차 묶음 "큐 N" 번호
(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-d, 큐 1–59)와 **별개**다 — 이 편은 "큐 23" 이 아니다. 닻은 `questions/assb-contact-loss-vs-lampe.md`.

들어온 경로: **21호**(Sedlmeier 2023, InLi 음극 파우치 μ-RE)가 ref 49 로 — `[인쇄]` 문헌의 InLi-(In) 탈리튬 전류 보고와 자기 결과가 어긋나는 원인 후보로
"원통 펠릿에서 Li 가 In 가장자리와 벽 사이로 분리막 쪽에 기어드는 Li creep" 을 들며 이 편을 달았고, 21호 후속 표 :730 은 **★ 7 순위 "Li creep 기계 물성"**
으로 올렸다. **5호**(Doux 2020, 압력 스윕 첫 편)도 ref 15 로 인용한다 — 5호 digest :205 `[인쇄]` "상온 Young 률·전단탄성률·푸아송비 측정, **항복강도 ≈0.8 MPa**,
그 위에서 **크리프 시작**. Tariq 2003 (ref 16) 과 일치". 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1): "★ **Masias 외 2019** — *J. Mater. Sci.* **54**, 2585 |
지목 21호 | 1 | Q6·Q7 | Li creep 기계 물성 — 21호 Li 박 조립 방향의 기계 쪽 근거".

**59호(파일 21) · 60호(파일 22)의 결과를 이어받는다.** 59호는 카드 13호 항의 "운전 압력 요구치 ≈1–5 MPa 독립 수렴" 을 반박했고(인쇄 띠 0.1–5 MPa · 일곱 편 ·
확인된 원전 0), 60호는 13호 `<5 MPa` 의 마지막 인용 다리 [45] 가 "5" 를 주지 않음을 확인했다(요구치 인쇄 0 · 정변위 지그 첫 충전 +1.51 MPa · 운전 중 구속 미명시).
이 편은 그 압력 계보의 **재료 쪽 근거**다 — Li 금속의 탄성률 · 항복 응력 · creep(2차 creep 속도 ↔ 응력, 실온)을 **벌크 시편**으로 실측한 편.

이 digest 의 일 (지시):

1. **인용 귀속 검증** — 21호 ref 49 · 5호 ref 15 가 이 편에 매단 명제를 원문이 실제로 주는가.
2. **(a)** 계보의 압력값(0.1–5 MPa 띠 · 5호 Doux 의 5 MPa · 60호의 0.8 / 1.51 MPa)이 이 편의 Li 항복 · creep 응력과 어떤 관계인가.
3. **(b)** "Li 이 creep 으로 계면을 채운다" 는 명제의 정량 근거(응력 지수 `n` · 활성화 · 시간 척도)가 어디까지 인쇄돼 있는가.
4. **(c)** 이 편은 ASSB 셀이 아니라 벌크 Li 시편(인장/압축 · 형상비 · 표면 상태)이다 — 셀 접촉 손실 `θ(N)` 으로 옮길 때 무엇이 빠지는가.
5. Q1–Q8 · 채움표 61호 행 · 곱 축퇴 처방 마흔네 번째 적용 · 보류 (가)(나)(다)(아)(자)(차)(타) 표시(결정 안 함).

> ⚠ **형식 — *J. Mater. Sci.* METALS 논문 16 쪽(그림 10 · 표 3 · 식 7 · 참고문헌 34) + ESM 2 쪽(Table S1 · S2 — 표 둘뿐, 그림 0). 1차 측정 있음 — 그러나 전기화학 0 ·
> 셀 0 · 고체전해질 0 · 도금/박리 0.** 이 편의 "LMSSB implications" 는 전부 Fig. 10 모식과 "we believe" 문장이다. 우리 카드의 축(양극 `LAM_PE` ↔ 접촉 손실)에는
> 직접 닿지 않고, **압력 계보의 눈금**(Li 이 어느 응력에서 항복하고 어느 속도로 기는가)을 준다.
>
> 표기: `[인쇄]` 본문 · 캡션 · SI 명시 · `[도표]` 그림에서만 읽은 값(`figure-read ≈`) · `[재현]` 지면의 숫자로 우리가 계산 · 대조한 값 · `[해석]` 우리 해석.
> `[해석]` 표시 없는 문장은 원문이 실제로 말한 것.

# 판정 먼저

| 물음 | 판정 | 한 줄 근거 |
|---|---|---|
| **5호 ref 15 귀속** — "E · G · ν 측정 · 항복 ≈0.8 MPa · 그 위에서 creep 시작 · Tariq 2003 과 일치" | ✅ 셋 · ❌ 하나 | E 7.82 · G 2.83 GPa · ν 0.381 ✅ · 항복 0.73–0.81 MPa ✅ · Tariq [13] 0.76 MPa "good agreement" ✅ — **"그 위에서 creep 시작" ❌**: 이 편의 creep 은 **항복 아래**에서 쟀다. `[인쇄]` "Tension creep performance was studied at loads **below the 0.8 MPa yield point** between 0.2 and 0.6 MPa" · 그 범위에서 power-law creep `n` = 6.56. 항복은 creep 의 문턱이 아니라 그 안의 한 눈금이다(5호 digest 문장 기준 — Doux 원문 어구는 미열람) |
| **21호 ref 49 귀속** — "원통 펠릿에서 Li 가 In 가장자리와 벽 사이로 분리막 쪽에 기어드는 Li creep" | ✅ 재료 전제 · ⚠ 기하 명제는 이 편 밖 | 이 편에 펠릿 · In · 분리막 · 셀 기하 0. 가장 가까운 것은 **Fig. 10a–c 모식** — `[인쇄]` "If Li freely flows without hydrostatic stress caused by friction, the cathode/solid electrolyte could cause Li to flow and eventually short-circuit" (측정 0). 21호의 명제는 21호 자신의 것이고, 이 편은 "상온 MPa 급 응력에서 Li 은 시간 의존 변형한다" 는 전제만 준다 |
| **(a) 압력 계보 0.1–5 MPa ↔ 이 편의 눈금** | ★★★ **띠가 한 물리가 아니다** | 이 편의 눈금으로 0.1–5 MPa 는 **확산 creep 영역(σ/G < 10⁻⁴ ⇒ < 0.28 MPa, 이 편이 인쇄한 [32] 기준) → 멱법칙 creep 측정 범위(0.2–0.6 MPa, `n` 6.56) → 항복(0.73–0.81) → 압축 시험 범위(0.8–2.4, "germane to LMSSB") → power-law breakdown(σ/G > 10⁻³ ⇒ > 2.83 MPa)** 을 가로지른다. `[재현]` 멱법칙으로 0.1 → 5 MPa 는 creep 속도 **×1.4×10¹¹**(11 자릿수) — 압력 ×50 이 속도 11 자릿수다. 5호의 5 MPa 는 breakdown 영역 · 항복의 6×; 60호 예압 0.8 = 항복 자리; 60호 첫 충전 총 ≈2.3 MPa = 이 편 압축 상한 근처 |
| **(b) "creep 이 계면을 채운다" 의 정량 근거** | ⚠ **`n` 하나 — 나머지 0** | 인쇄된 것: 인장 `n` = 6.56(7 시험 · 0.2–0.6 MPa · 실온 · AR ≈4) · 정규화 `n` = 6.70(Na · K 와 한 선) · 기구 "dislocation climb"([32] 지도 대조). **없는 것**: 활성화 에너지(온도 1 점 · `[인쇄]` "Future studies will investigate … −20 to 52 °C") · 입도 `d` · `p`(`[인쇄]` "assumed … polycrystalline") · 계면 채움 실험 0 · 압축 시간 의존 값은 **마찰 · 배럴링이 지배**해 응력 순서가 **역전**(0.8 → 2.4 MPa 에서 12 분 속도 1.93×10⁻⁴ → 4.02×10⁻⁵, `[인쇄]` "the higher the initial applied stress, the faster the strain rate decreased") — 저자 스스로 재료 법칙이 아니라고 적는다. 명제 자체는 Fig. 10 + "we believe" |
| **(c) `θ(N)` 으로 옮길 때 빠지는 것** | ★★ **여덟 가지** | ① 셀 · SE · 계면 0 ② 형상비 1–4.6 ↔ 셀 Li 박 `[인쇄]` ≈10⁻⁴(30 µm / 500–15,000 cm²) — 저자 자신이 "outside the scope" ③ 마찰 · 접착 미지(`[인쇄]` "degree to which friction was reduced was not known") ④ 온도 1 점 ⑤ 반복 · 진동 하중 0(60호 S14 · 33호 압력 진동) ⑥ 도금 Li 미세구조 0(멜트 가공 벌크) ⑦ 박리 · void 생성 속도와의 경쟁 0(창의 아래 벽 쪽 물리 0) ⑧ 양극 쪽 0 — 우리 카드의 `LAM_PE` ↔ 접촉 손실 축에는 **음극 계면 저항의 시간 상수**로만 들어간다 |
| **Q6 — 요구치 계보** | **여덟 번째 인쇄값 · 계보에서 가장 이른 것(2018)** | `[인쇄]` "Recent studies … suggest that stack pressures in the **1.0 MPa range are necessary** to achieve low and stable cell resistance [9, 10]" — 원전 **[9] Sharafi 2016 *JPS* 302 · [10] Wang & Sakamoto 2018 *JPS* 377**(같은 실험실 · 미열람). 같은 지면 뒤쪽: `[인쇄]` "How much compressive stress is **not known**, but our previous … used a constant nominal compressive stress of 1 MPa … **We believe** 1 MPa was sufficient". ⇒ 띠 0.1–5 MPa 그대로(≈1 은 8호 · 39호에 이미 있다) · 확인된 원전 0 그대로 — 다만 "≈1 MPa" 가닥이 **Sakamoto 실험실 2016–2021**(Sharafi 2016 → Wang 2018 → 이 편 → Wang 2021 *Joule* = 39호 원전)로 이어지는 **한 뿌리일 가능성**(`[해석]`, 미열람) |
| **59 · 60호와의 관계** | ✅ 일관 | 띠에 값을 더하지 않는다. 더하는 것은 **띠의 재료 눈금**(위 (a)) — 59호가 폭(×50)을, 60호가 "외압 0 ≠ 응력 0" 을, 이 편이 "×50 = creep 11 자릿수" 를 준다 |
| **Q1** | **없다 — `θ(N)` 0/61** | 셀 0. `contact` 6 회 중 셀 관련 1("assure contact is maintained between Li and the solid electrolyte" — 신념 문장) |
| **Q4** | **0/61 — 쉰세 번째 성질** | creep 기구를 `n` 하나와 남의 지도[32]의 대조로 확정하고(`p` · `Qc` 미측정), 압축 시간 의존 변형은 마찰 · 형상비가 지배해 재료 법칙이 아니라고 스스로 적으면서도 `[인쇄]` "most closely mimics LMSSB operation" 이라 옮긴다 |
| **곱 축퇴 처방 마흔네 번째** | **적용 불가 — 대상 없음** · 대신 `P↑` 연산자의 **음극 쪽 시간 상수** | 전기화학 0. 기록 이유: 압력 재인가 뒤 회복의 빠른 몫(초–분, ≥1 MPa)은 Li\|SE creep, 느린/안 돌아오는 몫은 양극 복합체 — **회복의 시간 상수가 전극을 가를 수 있다**(`[해석]`, 미검증) |
| **보류 (가)(나)(다)(아)(자)(차)(타)** | **근거 0 — 결정 안 함** | 일곱 항 모두 이 편의 내용과 닿지 않는다 |

# 서지

| 항목 | 값 |
|---|---|
| 제목 | Elastic, plastic, and creep mechanical properties of lithium metal |
| 저자 (5) | **Alvaro Masias**¹·²\*, Nando Felten³, Regina Garcia-Mendez², Jeff Wolfenstine⁴, **Jeff Sakamoto**²·³ |
| 소속 | ¹ Ford Motor Company, Energy Storage and Research Dept.(Dearborn) · ² Univ. of Michigan MSE · ³ Univ. of Michigan ME · ⁴ U.S. Army Research Laboratory RDRL-SED-C(Adelphi) |
| 서지 | *Journal of Materials Science* **54**, 2585–2600 (2019) · doi `10.1007/s10853-018-2971-3` · 섹션 **METALS** · © Springer Science+Business Media, LLC, part of Springer Nature 2018(**구독 논문** — 이 digest 는 인용 · 요약 · 재현 계산만 담는다) |
| 일정 | 접수 2018-07-25 · 승인 2018-09-24 · 온라인 2018-10-03 — `[재현]` 접수 → 승인 **61 일**. PDF 메타: creator Springer · 생성 2018-10-03 · 수정 2018-11-08 · title · author("Alvaro Masias") · subject(DOI) 일치 |
| 자금 | `[인쇄]` Ford-University Michigan Alliance program(Grant # UM0163) · Wolfenstine: Army Research Laboratory |
| COI | `[인쇄]` "The authors declare that they have no competing interests." |
| 분량 | 본문 pp. 2585–2598(그림 10 · 표 3 · 식 (1)–(7)) + 참고문헌 **34 편** pp. 2599–2600 = PDF 16 쪽(2,294,778 B) |
| ESM | PDF 2 쪽 — **Table S1**(인장 creep 최소 2차 creep 속도 vs 응력, 7 행) · **Table S2**(압축 creep 속도 vs 응력 × 시각, 5 행 × 3). 파일 메타: 작성자 "Jeff Sakamoto", Microsoft Word LTSC, **생성 · 수정 2026-09-28 11:25 (+09:00)** — 오늘 다시 저장된 파일이다(내용은 ESM 표 둘) |
| sha256 | 본문 PDF `125ec6ace593f9ec10eb4d538c49489ba8fa33efc7889d66565bb7286126e869`(2,294,778 B) · ESM PDF `f0a0726ff71d15e6521e4e5ba5347980b160165a3d67195fb1c89505ae6809ff`(106,093 B) — 호출자 명시값과 **일치** |
| 서지 대조 | 호출자가 준 "Masias A., Felten N., Garcia-Mendez R., Wolfenstine J., Sakamoto J. — *J. Mater. Sci.* 54, 2585–2600 (2019)" 와 **일치**. DOI 는 PDF 첫 쪽 · 메타에서 읽었다 |
| `[해석]` 자기 인용 | [7] Masias 2018(Springer 장) · [8] Masias & Sakamoto 2017 ECS 초록 · **[9] Sharafi … Sakamoto 2016 *JPS* 302, 135** · **[10] Wang & Sakamoto 2018 *JPS* 377, 7** · [20] Schmidt & Sakamoto 2016 *JPS* 324(음향) · [23] Sharafi … Sakamoto 2017 *Chem. Mater.* 29, 7961 · [33] Yu … Sakamoto, Siegel 2016 *Chem. Mater.* 28, 197(LLZO 탄성) · [6] Kim … Sakamoto 2016 *JACerS* — 34 편 중 **8 편**이 Sakamoto 그룹 |
| ⚠ 동명 주의 | 60호 · 33호의 "Zhang" 들과 무관. 46호(Schlenker 2020)가 ref 51 로 인용한 **Wang & Sakamoto 2018** 이 이 편의 [10] 이다 — 46호 digest 는 그것을 "**Li 항복 2 MPa**" 로 전사했다(§"귀속 검사") |

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | ★★★ **셀 0 · 고체전해질 0 · 계면 0 · 도금/박리 0** — "LMSSB implications" 절은 Fig. 10 모식 둘과 "we believe" 문장이다. 압력이 계면 저항 · 접촉을 어떻게 바꾸는지의 측정은 [9][10] 에 위임 | 이 편이 압력 계보에 주는 것은 재료 눈금뿐 — 창의 두 벽(접촉 손실 · 단락) 어느 쪽도 이 편 안에서 재지지 않았다 |
| G2 | ★★★ **활성화 에너지 `Qc` 미측정** — 온도 1 점(글러브박스 ≈26 °C = 0.66 `T/Tm`). `[인쇄]` "Future studies will investigate the tensile creep of Li at relevant temperatures, e.g., −20 to 52 °C". Fig. 7 의 온도 정규화는 [32] 의 확산계수를 빌린 것 | 기구 배정("dislocation climb rate-limited by lattice diffusion")이 `n` 과 남의 지도 대조로만 선다. 45 °C(60호) · −20 °C 로 옮길 근거 0 |
| G3 | ★★★ **입도 `d` · 입도 지수 `p` 미측정** — `[인쇄]` "It was assumed that the Li was melt processed, thus was polycrystalline" · "Without knowledge of these variables [grain size · impurities], it is not possible to explain the differences between the various studies" | 항복 0.60–0.81 MPa(문헌 산포)의 원인을 저자가 입도 · 불순물로 돌리면서 자기 시편의 입도를 모른다. 도금 Li(셀)의 입도는 또 다르다 |
| G4 | ★★ **마찰 계수 미지** — `[인쇄]` "The degree to which friction was reduced was not known, but it was assumed friction was not completely eliminated since barreling … occurred" · "These parameters [friction · aspect ratio] go outside the scope of this work" | 압축 쪽 값(Table S2 · Fig. 9)은 전부 이 미지수 위에 있다 |
| G5 | ★★ **형상비 간극** — 시험 AR 1.10(항복) · 1.89–2.57(압축) · 3.96–4.64(인장 creep) ↔ 셀 Li 박 `[인쇄]` "likely small (~1E-4) values … in an actual battery"(4 mAh cm⁻² × 1.5 → 30 µm; 2 · 5 · 60 Ah → 500 · 1250 · 15,000 cm² → 1.2E-4 · 7.5E-5 · 2.2E-5) | 저자 자신이 [32] Li 자료의 ×2 차이를 AR 로 설명한다 — AR 이 4 자릿수 다른 셀로 옮길 때 무엇이 남는지 지면이 답하지 않는다 |
| G6 | ★★ **시험 수 `n`** — 인장 creep 응력당 1 시험(0.4 MPa 만 3: 1.34 · 1.36 · 1.72×10⁻⁵, ×1.28) · 압축 응력당 1 · 압축 항복 4 시편(0.81 ± 0.10 MPa) · 인장 항복 그림 1 곡선 · 음향 N = 4–10 파형. **`n` = 6.56 의 오차 0** | `[재현]` 0.6 MPa 점을 빼면 `n` = 6.04, 0.2 MPa 점을 빼면 6.56 — 양 끝 한 점씩이 지수를 정한다 |
| G7 | ★ **표면 상태** — Cu 지그로 성형 · 압축은 미네랄 오일 윤활 · 인장은 시아노아크릴레이트로 Cu 봉에 접착 · 음향은 미네랄 오일/SWC-2 커플런트. 산화막 · 질화막 특성화 0(글러브박스 < 1 ppm O₂ · H₂O 명시) | 저자가 문헌 산포의 원인으로 "oxide/nitride surface layers during testing" 을 든다 — 자기 시편은 안 봤다 |
| G8 | ★ **변형 측정** — extensometer 없음(`[인쇄]` "compounded by the lack of an extensometer"). 응력-변형 기울기 0.43 GPa(인장) · 30.5 ± 16.6 MPa(압축)는 장치 순응 포함. 하중 제어 "constant load (pressure)" 는 공칭 응력 | 인장 true stress 미계산(넥킹) · 압축 true stress 는 등부피 가정 |
| G9 | ★ **Fig. 5 의 시험 식별** — 캡션 · 본문에 응력 미기재(범례만 "0.4MPa"; 0.4 MPa 시험 셋 중 어느 것인지 0). "135 s" · "2592 s" 의 판정 규칙 0(100 점 이동 평균) | 이 편의 유일한 creep 곡선 원자료 |
| G10 | ★ **반복 · 진동 하중 0** — 단조 하중만. 운전 셀의 압력은 사이클마다 ≈1 MPa 급 진동(60호 S14 · 33호) | 피로 · 래칫 · 회복(하중 제거 뒤) 0 |
| G11 | ★ **[9][10] 의 내용** — "low and stable cell resistance at 1.0 MPa" 가 무엇을 어떻게 잰 것인지 요약 0. 두 편 미열람. 46호는 [10] 을 "Li 항복 2 MPa" 로 전사 | 계보 "≈1 MPa" 가닥의 원전 |
| G12 | ★ **0.6–0.8 MPa 간극** — 인장 creep 상한 0.6 · 압축 하한 0.8 사이에 항복(0.73–0.81)이 있고 시험 0. 인장에서 항복 이상 creep 0 | "항복 위 creep" 은 이 편에 데이터가 없다 — 5호 문장의 자리 |
| G13 | Table S1 "Strain (%)" 열의 뜻 — "Minimum Secondary Creep" 머리 아래에 있어 최소 속도 시점의 변형률로 읽히나 정의 0; 0.6 MPa 행만 5.67 %(나머지 0.20–0.51) | |

# 그림 — 자동 크롭 6 장 + 수동 크롭 9 장, 실제로 본 것: 12 항목 / 안 본 것: 3 항목(Table 1 · 2 · 3 이미지 — 텍스트로 읽었다)

폴더 `raw/figures/masias2019_elastic-plastic-creep-mechanical-properties-lithium-metal/`(`figures.json` 15 항목). 자동 추출은 **Fig. 4**(모식) + **Table 1 · 2 · 3** + **Table S1 · S2** 만
잘랐고 **Fig. 1 · 2 · 3 · 5 · 6 · 7 · 8 · 9 · 10 을 "그래픽 없음(img0/draw1)" 으로 제외**했다 — 실제 쪽은 캡션이 왼쪽 여백, 래스터 그림이 오른쪽에 있는 배치라 캡션 아래
영역 검사가 비었다. 캡션 블록 + 이미지 rect 합집합으로 수동 크롭 9 장을 만들어 `manual: true` 로 더했다(`fig_N_manual_pP.png`).

**봤다(12)**: Fig. 1 · 2 · 3 · 4 · 5 · 6 · 7 · 8 · 9 · 10 · Table S1 · Table S2(SI 표는 텍스트 추출이 열을 뒤섞어 이미지로 열 대응을 확정했다).
**안 봤다(3)**: Table 1 · 2 · 3 의 이미지 — 값은 PDF 텍스트로 옮겼다(추출기 안내대로).

## `[도표]` Fig. 1 — 시험 절차 모식 (봤다 · 수동)

- (a) Tension Creep · (b) Compression Deformation. 두 패널 모두 화살표 두 개: **`d(V) = 0`**(정속 크로스헤드) → **`d(F) = 0`**(정하중). 힘(실선)은 선형 상승 뒤 평탄;
  변형률 속도(점선)는 (a) 급락 → 낮은 평탄 → 끝에서 급상승(파단), (b) 급락 → 단조 감소. 수치 0. `[해석]` (b) 의 단조 감소가 이 편 압축 자료의 모양 전부다 — 정상 creep 구간이 없다.

## `[도표]` Fig. 2 — 인장 응력–변형 (봤다 · 수동) — ⚠ **본문 "0.4 % 이후 감소" 와 어긋난다**

- 시편 15.5 mm 높이 × 12.7 mm 지름(캡션). 공칭 응력이 ε ≈ 0.01 에서 ≈0.88, `figure-read ≈` **0.93 MPa 정점이 ε ≈ 0.03–0.05** 에 있고, 그 뒤 단조 감소해 ε = 0.50 에서 ≈0.49 MPa.
  범례 "Tension"(점선). 인셋 사진: 시편 → 뾰족하게 넥킹된 파단.
- 인셋 그래프(0–0.010): 곡선이 (0.001, ≈0.45) · (0.002, ≈0.62) · (0.004, ≈0.76) · (0.010, ≈0.88) MPa. 세로 점선 **"7.82 GPa"**(PE, ε = 0.002 에서 거의 수직) ·
  점선 **"0.43 GPa"**(SS, (0.002, 0) 에서 기울기 430 MPa/단위변형). `figure-read ≈` PE 선과 곡선의 교점 **≈0.62–0.65 MPa**, SS 선과의 교점 **≈0.75–0.78 MPa**.
- ⚠ 본문 `[인쇄]` "steep and linear increase in stress … up to approximately 0.8 MPa stress and 0.4% strain … At strains greater than 0.4%, the stress continuously decreased"
  ↔ 그림은 0.4 % 뒤에도 **≈4 % 까지 오른다**(D2). 본문 "0.81 and 0.73 MPa … when using E values of 7.82 and 0.43 GPa, respectively" ↔ Table 3 는 SS(0.43) → 0.81 ·
  PE(7.82) → 0.73 (D1) — 그림 판독은 Table 3 의 순서(PE 가 낮다)를 지지하고, 두 값 모두 인쇄보다 ≈0.06–0.10 MPa 낮게 읽힌다(판독 오차 가능).

## `[도표]` Fig. 3 — 압축 응력–변형, 공칭 · 진응력 (봤다 · 수동)

- 시편 12.3 × 12.7 mm. 공칭(실선): ε ≈ 0.03 에서 ≈0.8 · 0.06 에서 ≈1.0 · 0.15 에서 ≈1.2 · **0.18–0.22 에서 ≈1.23 → 1.20 살짝 하강** · 0.30 에서 ≈1.5 · 0.46 에서 ≈2.1 MPa.
  진응력(점선): 0.18 에서 ≈1.47 · 같은 하강 · 0.30 에서 ≈2.1 · **0.375 에서 ≈3.05 MPa**(측정 상한). 인셋: 원통 → 배럴링된 원판.
- 본문과 정합: `[인쇄]` "0.81 ± 0.10 MPa" 까지 비선형 상승(0–3.93 ± 1.98 %) · "slight drop in stress between 18 and 22%" · 진응력 "dramatically increased above ~20%" ✓.
  `[해석]` 공칭 곡선이 ε = 0.30 에서 ≈1.5 MPa 라는 것이 Fig. 8 의 전제다 — 1.48 MPa 목표 하중은 **≈25–30 % 변형 뒤에야** 닿는다(D14).

## `[도표]` Fig. 4 — 배럴링 모식 (봤다 · 자동)

- (a) 원형 · (b) 형상비 감소, 압반 인접의 빗금 영역(변형 제한, 마찰) · (c) 더 감소해 빗금 영역이 겹침. [28] Cook & Larke 1945 를 개작. 수치 0.

## `[도표]` Fig. 5 — 인장 creep 곡선 (봤다 · 수동) — 범례에만 "0.4 MPa"

- 왼쪽 축 공칭 변형률 0–100 %, 오른쪽 축 변형률 속도 10⁻⁶–10⁻¹ s⁻¹(로그), 시간 1–10⁵ s(로그). 범례 "Strain (0.4MPa)" · "Strain Rate (0.4MPa)".
- 속도(실선): 1–30 s 에서 ≈3.5×10⁻⁵ 평탄 → 하강 → **최소 ≈1.4×10⁻⁵ s⁻¹ at ≈100–135 s** → 완만 상승(≈3×10⁻⁵ at 10³ s · ≈4×10⁻⁵ at 3×10³ s) → 5×10³ s 뒤 급상승 → ≈7×10³ s 에서 10⁻¹(파단).
  변형률(점선): ≈10³ s 까지 ≈0 · 10 % at ≈4×10³ s · 30 % at ≈5.5×10³ s → 100 %. 인셋: 원통 → 원뿔로 넥킹.
- 본문 정합: `[인쇄]` "after about 135 s the strain rate reaches a minimum … after 2592 s the strain rate continually increases until failure" ✓. 최소값 `figure-read ≈` 1.4×10⁻⁵ 는
  Table S1 의 0.400 MPa 행(1.34 · 1.36 · 1.72×10⁻⁵)과 맞는다. ⚠ 1차 creep(감속 구간)이 없다 — 본문이 "lack of work hardening" 과 제어 전환 왜곡으로 설명.

## `[도표]` Fig. 6 — 최소 인장 변형률 속도 vs 응력 (봤다 · 수동) — `n` = 6.56 의 그림

- 로그–로그, 응력 0.01–10 MPa · 속도 10⁻⁸–10⁻² s⁻¹. 점 7: 0.2 MPa 에서 2×10⁻⁷ · 0.3 에서 5×10⁻⁶ · **0.4 에서 세 점 1.3–1.7×10⁻⁵** · 0.6 에서 3.9×10⁻⁴. 점선 기울기 표시 "n = 6.56".
  Table S1 과 일치. `[해석]` 그림 상 데이터 폭은 **0.2–0.6 MPa 의 반 자릿수**뿐이고, 계보의 1–5 MPa 는 이 그림 오른쪽 빈 곳이다.

## `[도표]` Fig. 7 — 확산계수 · 전단탄성률로 정규화한 알칼리 금속 creep (봤다 · 수동) — ⚠ **축 값이 본문 `D` 로 재현되지 않는다**

- 가로 σ/G 10⁻⁵–10⁻³, 세로 ε̇/D **(cm⁻²)** 10¹–10⁷. Li [This Work] 두 점(≈7.1×10⁻⁵, ≈2.2×10³) · (≈2.1×10⁻⁴, ≈4.5×10⁶); Na [32] (≈4.7×10⁻⁵, ≈4×10²) · (≈1.4×10⁻⁴, ≈8.5×10⁴);
  K [32] (≈6.3×10⁻⁵, ≈8×10¹) · (≈1.2×10⁻⁴, ≈1.6×10⁴); Li [32] (≈2.3×10⁻⁴, ≈1×10⁴) · (≈2.6×10⁻⁴, ≈3.3×10⁴) — 공통 점선 "n = 6.70"; Li [32] 만 오른쪽에 따로.
- `[재현]` 이 편 Li 점 = Table S1 의 0.2 · 0.6 MPa 시험이라면 ε̇/D = 2.0×10⁻⁷/D ≈ 2.2×10³ ⇒ **D ≈ 9×10⁻¹¹ cm² s⁻¹**(0.6 MPa 로도 8.6×10⁻¹¹ — 자기 일관). 본문 `[인쇄]`
  "room-temperature lattice diffusivity Li (D = 3.1 × 10⁻¹ cm²/s), Na (1.94 × 10⁻¹), K (3.1 × 10⁻¹)" 로는 점이 ≈6×10⁻⁷–10⁻³ 에 놓여 축 밖이다 — 인쇄값은 지수앞자리 `D₀`
  크기이지 상온 값이 아니다(D4). 결론("한 선 · `n` 6.70 · Li[32] 는 ≈2× 높은 응력")은 그림 기준으로 성립한다.

## `[도표]` Fig. 8 — 압축 1.48 MPa 의 변형률 · 속도 vs 시간 (봤다 · 수동)

- 속도(실선): **10⁻³ s⁻¹ 평탄(정속 접근) → ≈200–300 s 에서 이탈** → ≈3×10⁻⁴ at 700 s · ≈1.2×10⁻⁴ at 10³ s · ≈10⁻⁵ at 5×10³ s · ≈2.5×10⁻⁶ at 1.5×10⁴ s(끝, 작은 스파이크).
  변형률(점선): 10 % at ≈120 s · 20 % at ≈230 s · 40 % at ≈400 s · 50 % at ≈500 s · 60 % at ≈10³ s · 70 % at ≈5×10³ s · ≈74 % at 끝. 인셋: 원통 → 납작한 원판.
- 본문 정합: `[인쇄]` "strain rate at 1000 s was 10⁻⁴ s⁻¹ whereas at 10000 s … ~10⁻⁶" ✓. ⚠ `[해석]` 정하중 구간이 시작될 때 시편은 이미 **≈25–30 % 눌린 배럴**이다 —
  "creep" 이라 부를 재료 상태가 아니다(저자도 본문에서는 "time-dependent deformation" 이라 부르고 SI 표 제목만 "Compression Creep").

## `[도표]` Fig. 9 — 12 · 60 · 120 분에서의 압축 속도 vs 응력 (봤다 · 수동) — ★ **응력 순서가 역전된 그림**

- 응력 0.8 · 1.0 · 1.2 · 1.48 · 2.4 MPa × 시각 3(■ 12 min · ◆ 60 min · ▲ 120 min). 12 min: ≈1.9×10⁻⁴ → 4.0×10⁻⁵(응력 ↑ 에 속도 ↓) · 60 min: ≈2.9×10⁻⁵ → 6×10⁻⁶ ·
  120 min: ≈1.1×10⁻⁵ → 2.6×10⁻⁶. Table S2 와 일치. 캡션 `[인쇄]` "The three time points were taken to represent a LMSSB charged or discharged in 12, 60, and 120 min".
- `[재현]` 재료 멱법칙(`n` 6.56)이면 0.8 → 2.4 MPa 는 속도 **×1,350** 이어야 하는데 그림은 **×0.21**. 저자 설명: `[인쇄]` "the higher the load, the faster the Li barrels,
  the slower the strain rate at a fixed time". ⇒ 이 그림의 값은 **시편 기하 · 마찰의 함수**이지 Li 의 성질이 아니다 — (b) 판정의 근거.

## `[도표]` Fig. 10 — LMSSB 두 시나리오 모식 (봤다 · 수동)

- 위 줄 "no hydrostatic pressure in Li": (a) Cathode | Solid State Electrolyte | Li 적층 → (b) Li 가 옆으로 퍼지며 SE · 양극이 가라앉음 → (c) 양극이 Li 와 닿아 **short-circuit**.
  아래 줄 "hydrostatic pressure in Li": (d) 같은 적층 → (e) Li 안에 빗금(정수압 영역) → **no short-circuit**. 수치 0. `[해석]` 5호 위 벽(고압 → Li creep → 단락)의
  **접착 · 마찰 조건부 판** — 5호는 압력이 높을수록 단락이 빠르다고 재었고, 이 편은 마찰이 없으면 어떤 압력에서도 흐른다고 그린다.

## `[도표]` Table S1 — 인장 creep (봤다) — 열 대응 확정

열: Pressure σ (MPa) · σ/G · Aspect Ratio (H/D) · Minimum Secondary Creep **Rate (sec⁻¹)** · **Strain (%)**. 7 행. 전사는 §"SI 표 전사". ⚠ 인장 응력을 "Pressure" 로 부른다(D11).

## `[도표]` Table S2 — 압축 creep (봤다) — 열 대응 확정

열: Pressure σ (MPa) · σ/G (10⁻⁴) · Aspect Ratio (H/D) · Rate (sec⁻¹) at **5C (720 sec)** · **1C (3600 sec)** · **0.5C (7200 sec)**. 5 행. C-율 표기는 12 · 60 · 120 분 충방전을 뜻한다.

# SI 표 전사 (`[인쇄]` 전부)

**Table S1: Tension Creep Minimum Secondary Creep Rate as a function of Pressure (room temperature)**

| σ (MPa) | σ/G | AR (H/D) | 최소 2차 creep 속도 (s⁻¹) | Strain (%) |
|---:|---:|---:|---:|---:|
| 0.200 | 7.13E-5 | 4.24 | 2.00E-7 | 0.25 |
| 0.301 | 1.07E-4 | 4.24 | 4.95E-6 | 0.51 |
| 0.396 | 1.42E-4 | 3.96 | 1.58E-5 | 0.36 |
| 0.400 | 1.42E-4 | 4.05 | 1.34E-5 | 0.20 |
| 0.400 | 1.42E-4 | 4.11 | 1.36E-5 | 0.26 |
| 0.400 | 1.42E-4 | 4.14 | 1.72E-5 | 0.37 |
| 0.600 | 2.13E-4 | 4.64 | 3.89E-4 | 5.67 |

`[재현]` 로그–로그 최소제곱 7 점: **`n` = 6.562**(인쇄 6.56 ✓) · `A` = 7.7×10⁻³ s⁻¹ MPa⁻ⁿ · 잔차비 0.71–1.69(0.301 MPa 점 +69 %, 0.6 MPa +44 %). σ/G 열이 함의하는 G =
**2.79–2.82 GPa**(본문 평균 2.83, D8). 0.2 → 0.6 MPa(×3)에서 속도 ×1,945.

**Table S2. Compression Creep Strain Rate as a function of Pressure and Time (room temperature)**

| σ (MPa) | σ/G (10⁻⁴) | AR (H/D) | 5C (720 s) | 1C (3600 s) | 0.5C (7200 s) |
|---:|---:|---:|---:|---:|---:|
| 0.80 | 2.85 | 2.12 | 1.93×10⁻⁴ | 2.85×10⁻⁵ | 1.12×10⁻⁵ |
| 1.00 | 3.56 | 2.40 | 1.45×10⁻⁴ | 2.34×10⁻⁵ | 9.26×10⁻⁶ |
| 1.20 | 4.28 | 2.57 | 1.04×10⁻⁴ | 1.40×10⁻⁵ | 5.05×10⁻⁶ |
| 1.48 | 5.28 | 1.89 | 7.83×10⁻⁵ | 1.13×10⁻⁵ | 4.44×10⁻⁶ |
| 2.40 | 8.54 | 2.03 | 4.02×10⁻⁵ | 6.01×10⁻⁶ | 2.63×10⁻⁶ |

`[재현]` 같은 응력에서 720 → 7200 s 에 속도 ×1/15–1/21 · 같은 시각에서 0.8 → 2.4 MPa 에 속도 **×0.21**(역전) · σ/G 열이 함의하는 G = 2.80–2.81 GPa.

# 절별 해체

## 초록 · 서론 (pp. 2585–2587)

- `[인쇄]` 목적: "characterize the elastic and plastic mechanical properties and creep behavior of Li". 결과 요약: E **7.82** · G **2.83 GPa** · ν **0.381**(펄스-에코) · 항복 **0.73–0.81 MPa** ·
  인장 power-law creep **`n` = 6.56**("dislocation climb") · 압축 시간 의존 변형 **0.8–2.4 MPa**("a range of stress believed to be germane to LMSSB") 에서 배럴링 + 시간에 따른 속도 감소.
- `[인쇄]` Monroe–Newman: SE 전단탄성률 ≥ **2 G_Li** 면 Li 관통 억제 [4, 5] — `[재현]` 이 편의 G 로 **≥ 5.66 GPa**. LLZO 파괴인성 [6].
- `[인쇄]` 양극 부피 변화 −8.0 / −7.7 / −6.7 %(LCO · LMO · LFP 완전 탈리튬) · C₆ +10.7 % · Sn 258 % · Si 311 %. "existing lithium ion cells and battery packs are typically held under compression" [7, 8].
- `[인쇄]` "elemental lithium anodes do not expand or contract but rather are stripped or plated during cycling" · "The design of lithium electrodes with **excess capacity** is considered an engineering
  necessity to account for irreversible material loss during use and to provide the anode with some mechanical stability".
- ★ `[인쇄]` "Recent studies of all solid-state cells using Li metal electrodes suggest that **stack pressures in the 1.0 MPa range are necessary** to achieve low and stable cell resistance [9, 10]".
- `[인쇄]` 선행 연구: 탄성 상수 셋을 같은 시편으로 직접 잰 적 없음 · 벌크 Li 항복은 인장 · 압축 각 한 편[11–14] · 공기 반응 문제 → 아르곤 내 하중 프레임.
- `[인쇄]` USABC 목표 15 년 · **−30 ~ 52 °C** [15] ⇒ Li 상동 온도 **0.54–0.72** — "significant creep is likely to occur".

## 재료 · 방법 (pp. 2587–2589)

- `[인쇄]` Li 99.9 %(Ca 88 ppm · Na 19 ppm) 12.7 mm 봉(Alfa Aesar #10773) · 아르곤 글러브박스(< 1 ppm O₂ · H₂O) ≈26 °C · "assumed … melt processed, thus was polycrystalline" ·
  AR 1 · 2 · 4(ASTM [16–18]) · Cu 지그 성형 · 밀도 이론값 대비 < 2 % · 인장: 시아노아크릴레이트로 Cu 봉에 접착 → Instron 2710-205 그립(5 kN) · 압축: 미네랄 오일 윤활 압반.
- **음향**: 펄스-에코 [19–21] · Olympus 5073R P/R + Picoscope 2207A · 200 Hz · 50 Ω · 8–16 µJ · 39 dB · 종파 M110-RM 5 MHz(미네랄 오일) · 횡파 V-156RM 5 MHz(SWC-2) ·
  원통 12.7 mm × **0.75–12.3 mm**.
- **응력-변형**: Instron 5944(2 kN) + 0.5 kN 로드셀 · DAQ 10 Hz / 1 N(항복) · 0.1 Hz / 0.3 N / 0.05 mm(creep) · 항복 전이 = 선형 회귀 **R² < 0.99** 지점 · 응력-변형 기울기가
  문헌 E 와 안 맞아(장치 순응 · extensometer 없음) **음향 E 를 0.2 % 오프셋에 사용** · 크로스헤드 `[인쇄]` "1 mm/s" ↔ 평균 변형률 속도 **1.22×10⁻³ s⁻¹**(D5) · ASTM 권고
  1.15–11.5 MPa/s ÷ E → 문헌 E 1.9–10.6 GPa 로 0.11–6.05×10⁻³ s⁻¹ 의 중간값 선택 · 항복 시편 AR ≈1("practical compromises" — ASTM 2 · 4 와 셀의 ≈10⁻⁴ 사이).
- **시간 의존**: 1.0×10⁻³ s⁻¹ 로 목표 하중까지 → 정하중(Fig. 1) · 100 점 이동 평균 · 인장 creep **0.2–0.6 MPa(항복 아래) · AR ≈4** · 압축 **0.8–2.4 MPa · AR ≈2** —
  `[인쇄]` "This covers the range of anticipated stack pressures that are required to achieve low and stable cell resistance [9, 10]" · 진응력은 압축만(인장은 넥킹).
- **Table 1**(문헌 E, `[인쇄]`): 다결정 5.0(선 굽힘 [11] Bridgman 1922) · 8.0(음향 [26] Robertson 1960) · 1.9(압축 [12] Schultz 2002) · 7.8(인장 [13] Tariq 2003) · **7.8(음향, this work)** ·
  단결정 *21.2 ⟨111⟩ · *3.0 ⟨100⟩(음향 [34] 에서 방위별 계산). ⚠ 본문 "two groups … 7.8–8.0 and 10.5–10.6 GPa" · "span … 1.9 and 10.6 GPa (see Table 1)" — 표에 10.5–10.6 없음(D7).

## 탄성 상수 (pp. 2589–2590) — Table 2

- 식 (1)–(4): E = 2ρVs²(1+ν) · G = ρVs² · ν = (1 − 2(Vs/Vl)²)/(2 − 2(Vs/Vl)²) · K = E/(3(1 − 2ν)). 세 높이(0.75 · 8.83 · 12.35 mm)에서 "independent of sample size".

| 높이 (mm) | ρ (g/cc) | Vl (km/s) | Vs (km/s) | E (GPa) | G (GPa) | K (GPa) | ν |
|---:|---:|---|---|---:|---:|---:|---:|
| 12.35 | 0.53 | 5.27 ± 0.01 (N = 4) | 2.29 ± 0.01 (N = 4) | 7.80 | 2.82 | 11.18 | 0.38 |
| 8.83 | 0.54 | 5.48 ± 0.02 (N = 6) | 2.30 ± 0.02 (N = 6) | 7.79 | 2.80 | 12.12 | 0.39 |
| 0.75 | 0.53 | **5.08 ± 0.26** (N = 6) | 2.32 ± 0.02 (N = 10) | 7.88 | 2.88 | 9.92 | 0.37 |
| 평균 | | | | **7.82** | **2.83** | **11.07** | **0.38** |

- `[재현]` ν 를 Vs/Vl 로 다시 계산하면 0.384 · 0.393 · 0.368 ✓ · E = 2G(1+ν) = 7.82 ✓ · K = E/(3(1−2ν)) 는 반올림 ν 로 10.95(행별 비반올림이면 11.07 재현) · ρVs² 는 ρ = 0.53 으로
  2.78–2.85(인쇄 2.80–2.88 — ρ 반올림). ⚠ 가장 얇은 시편의 Vl 오차 ±0.26(5 %)가 다른 둘의 13–26 배 → K 9.92 vs 11.18/12.12(폭 20 %) — "size-independent" 는 E · G 기준(D13).
- `[인쇄]` "To our knowledge, this is the first report of E, G, K and v on the same Li sample batch." · bcc Li 이방성 Zener 비 **A = 8.43** [22, 27] → 다결정(낮은 E) ↔ 단결정(높은 E) 구분.

## 정속 응력-변형 — 인장 (pp. 2590–2591) · Fig. 2 · Table 3

- `[인쇄]` 초기 선형 구간 기울기 **0.43 GPa**(R² < 99 % 기준 0.40 ± 0.02) ≪ 음향 7.82 → 둘 다로 0.2 % 오프셋: **0.81 · 0.73 MPa**(§Fig. 2 의 D1 참조). "in good agreement with the literature values for polycrystalline Li tested in tension".
- **Table 3**(`[인쇄]`): 다결정 인장 0.60(ε̇ 0.11×10⁻³ · AR 10.6, [31] Hull & Rosenberg 1959) · 0.76(2.0 · N/A, [13] Tariq 2003) · **0.81(SS · 1.21 · 1.10, this work)** · **0.73(PE · 1.21 · 1.10, this work)** ·
  다결정 압축 0.64(1.67 · 2.07, [12] Schultz 2002) · **15–105 MPa**(5 · 3–5, [30] Xu … Greer 2017 — sub-micron) · 단결정 인장 0.3([29] Gorgas 1981) · 0.2([14] Pichl 1997).

## 정속 응력-변형 — 압축 (pp. 2590–2592) · Fig. 3 · Fig. 4

- `[인쇄]` 식 (5)(6) σ_t = σ_n(1+ε_n) · ε_t = ln(1+ε_n)(등부피 · 단면 균일 가정). 0–**3.93 ± 1.98 %** 에서 비선형 상승 → **0.81 ± 0.10 MPa**, 기울기 **30.5 ± 16.6 MPa**(초기 S 곡선 < 1 %, 전 시편) —
  "load frame backlash and/or inhomogeneous sample-platen interface contact" · 이 변곡점은 항복이 아니다(기울기가 7.8 GPa 와 안 맞음) · ≈19–21 % 까지 계속 상승 · 18–22 % 살짝 하강(원인 미상, **4 시편** 모두) ·
  그 위 기울기 증가 → 하중 상한.
- `[인쇄]` 해석: 가공 경화 없는 연성 금속(Cook & Larke 1945 Cu [28]) · 세 영역(0–4 % 균일 · 4–20 % 압반 마찰로 정수압 영역 + 배럴링 · > 20 % 단면 증가/정수압 영역 겹침) · **접촉 면적 ≈25 % 증가**(Fig. 3 인셋).

## 항복 비교 (p. 2593)

- `[인쇄]` 인장 ≈ 압축 · 다결정 > 단결정(입계) · 최저 0.2–0.3(단결정) · 최고 15–105 MPa(sub-micron [30]) · **µm 급 다결정은 0.60–0.81 MPa 의 좁은 범위**(방법 · AR 1.1–10.6 · 속도 0.11–2.0×10⁻³ 가 달라도) ·
  산포 원인 = 입도 · 불순물(미지) · 변형률 속도(Tariq [13]).

## Creep — 인장 (pp. 2593–2595) · Fig. 5 · 6 · 7

- `[인쇄]` Tm = 180.5 °C(453.5 K) · 실온 = **0.66 T/Tm** · 인장을 고른 이유 = 압반 마찰 없음(재료 고유 거동).
- Fig. 5: 최소 속도 ≈135 s · 2592 s 뒤 계속 상승 → 파단(넥킹). 1차 creep 없음(가공 경화 없음 · 제어 전환 왜곡).
- 식 (7) `ε̇ = A σⁿ d^p exp(−Qc/RT)` [32]. `[인쇄]` 판정 규칙: T/Tm > 0.5 에서 `n` ≈ 1(확산 유동; p = 2 격자 · 3 입계) · 3–7(전위; ≈3 활주 · **5–7 상승**; p ≈ 0).
  **`n` = 6.56 → dislocation climb**. σ/G 가 "2.2×10⁻⁴ at the low stress level and 7.1×10⁻⁵ at the high stress level"(⚠ 뒤바뀜, D3) — 전위 creep 범위 안; **σ/G < 10⁻⁴ 확산 creep · > 10⁻³ power-law breakdown** [32].
- `[인쇄]` Sargent & Ashby [32] Li 압축 `n` = **6.4**(격자 확산 율속 전위 상승) · K 6.4 · Na 5.0 → 세 알칼리 금속 같은 기구. Fig. 7 정규화(Li D = 3.1×10⁻¹ · Na 1.94×10⁻¹ · K 3.1×10⁻¹ cm²/s · G_Na 1.53 · G_K 0.661 GPa [32]) →
  한 선 · **`n` = 6.70** · Li[32] 만 ≈2× 높은 응력 — [32] 의 Li 시편 AR 이 작았다는 것으로 설명 · `[인쇄]` "Future studies will investigate the tensile creep of Li at relevant temperatures, e.g., −20 to 52 °C; 0.56–0.71 T/Tm".

## 시간 · 응력 의존 변형 — 압축 (pp. 2595–2597) · Fig. 8 · 9

- ★ `[인쇄]` "Based on our previous work [9, 10, 33] we believe LMSSB will require a constant compressive load to assure contact is maintained between Li and the solid electrolyte during cycling.
  **How much compressive stress is not known**, but our previous solid-state cycling studies of Li metal used a constant nominal compressive stress of **1 MPa** [9, 10, 33]. **We believe 1 MPa was sufficient**
  to minimize the effect of pressure on cell impedance during cycling." → 0.8–2.4 MPa(공칭). ⚠ [33] 은 LLZO 탄성 논문이다(D9).
- Fig. 8(1.48 MPa): 정속 → 정하중 뒤 속도 단조 감소(전 시편) · 인장과 반대(넥킹 → 응력 ↑ · 배럴링 → 응력 ↓) · 10³ s 에서 10⁻⁴ · 10⁴ s 에서 ~10⁻⁶ s⁻¹.
- Fig. 9: 12 · 60 · 120 분 = "LMSSB charging or discharging times" · **초기 응력이 높을수록 주어진 시각의 속도가 더 낮다** · 시간이 길수록 낮다 — 둘 다 배럴링으로 설명.

## LMSSB 함의 · 결론 (pp. 2597–2599) · Fig. 10

- `[인쇄]` "the first comprehensive study of the elastic, plastic, and time-dependent mechanical properties of Li" · 다결정 값이 셀에 더 적합("LMSSB will cycle polycrystalline Li") · 인장 creep 에서
  "power-law creep (dislocation climb) when a stress relevant to LMSSB was applied (~1 MPa)"(⚠ 인장 creep 은 0.2–0.6 MPa 에서 쟀다 — "~1 MPa" 는 외삽 어구) · **압축 시간 의존 분석이 운전과 가장 닮았다** ·
  Fig. 10 두 시나리오 · "The Li anode aspect ratio and frictional forces will have significant effects on the cycling of Li under compressive stresses."
- 결론: `[인쇄]` "the effects of sample aspect ratio and friction (or adhesive forces) should be considered, in the design of LMSSB, to determine how much Li deforms during operation."

## 참고문헌 34 편 — 우리 축에 닿는 것

[4] Monroe & Newman 2005 *JES* 152, A396 · [5] Ferrese & Newman 2014 *JES* 161, A1350 · [9] Sharafi, Meyer, Nanda, Wolfenstine, Sakamoto 2016 *JPS* 302, 135 · [10] Wang & Sakamoto 2018 *JPS* 377, 7 ·
[12] Schultz 2002 Fermilab TM-2191 · [13] Tariq, Ammigan, Hurh, Schultz 2003 PAC · [14] Pichl & Krystian 1997 · [23] Sharafi … Dasgupta, Sakamoto 2017 *Chem. Mater.* 29, 7961 · [26] Robertson & Montgomery 1960 *Phys. Rev.* 117, 440 ·
[28] Cook & Larke 1945 · [29] Gorgas 1981 · [30] Xu, Ahmad, Aryanfar, Viswanathan, Greer 2017 *PNAS* 114, 57 · [31] Hull & Rosenberg 1959 · **[32] Sargent & Ashby 1984 *Scr. Metall.* 18, 145** · [33] Yu … Siegel 2016 *Chem. Mater.* 28, 197 · [34] Slotwinski & Trivisonno 1969.

# 어휘 집계 — NFKC 정규화 후, 대소문자 무시, 낱말 경계 (본문 · 캡션 · 표 | 참고문헌 | SI)

| 지문 열 | 본문 | 참고문헌 | SI | 메모 |
|---|---:|---:|---:|---|
| `identifiab` · `uncertaint` · `error` · `standard deviation` | **0** | 0 | 0 | 산포 표현은 `±` 11(음향 파속 · 압축 변곡 0.81 ± 0.10 · 3.93 ± 1.98 % · 30.5 ± 16.6 MPa) · `N =` 7(파형 수) |
| `LLI` · `LAM` · `degradation` · `OCV` · `EIS` | **0** | 0 | 0 | 전기화학 어휘 0 |
| `contact loss` · `void` | **0** | 0 | 0 | `contact` 6 = 압반 접촉 · 트랜스듀서 ×2 · "contact area … 25%" · **"assure contact is maintained between Li and the solid electrolyte"** 1 |
| `pressure` | 5 | 0 | 4 | `stack pressure` **2**(서론 · 방법 — 둘 다 [9, 10] 재인용) · SI 는 "Pressure" 열 이름 |
| `MPa` | **25** | 0 | 2 | 값: 0.81 · 0.8–2.4(×3) · **1.0 / 1(×8)** · 11.5(ASTM) · 0.8(×2) · 0.6 · 2.4 · 0.73 · 0.10(±) · 16.6(±) · 0.3 · 15–105 · 0.60–0.81 · 1.48 — **요구치 문장은 "1.0 MPa range … necessary" 하나** |
| `creep` | **52** | 2 | 4 | 본문 압축 절은 "time-dependent deformation" 을 쓴다 |
| `yield` | 31 | 1 | 0 | |
| `barrel` · `friction` · `aspect ratio` | 12 · 16 · 13 | 0 | 0 | 압축 자료의 지배 어휘 |
| `dislocation` · `diffusion` | 16 · 12 | 0 | 0 | 기구 배정 어휘 |
| `dendrit` · `short` · `adhesi` | 1 · 3 · 4 | 0 | 0 | `dendrit` = Monroe–Newman 한 번 · `short` = Fig. 10 |
| `temperature` · `activation` | 27 · 3 | 5 | 2 | 활성화 에너지는 정의 · 미측정 |
| `polycrystal` · `single crystal` | 26 · 12 | 0 · 2 | 0 | |
| `LMSSB` · `solid electrolyte` | 27 · 12 | 0 · 2 | 0 | |
| `stripp` · `plat(ed/ing)` · `cycl` | 2 · 2 · 9 | 0 | 0 | 셀 운전 어휘는 서론 · 함의 절에만 |
| `fatigue` | **0** | 0 | 0 | 13호 · 59호의 "피로" 위 벽은 이 편에 없다 |

# Q1~Q8 판정 (닻 페이지 수집 지침)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1** 접촉 손실 정량 | **없다 — `θ(N)` 0/61** | 셀 0. 계면 접촉은 `[인쇄]` "assure contact is maintained" 한 문장(신념) + Fig. 10 모식 |
| **Q2** 독립 관측 | **없다 — 셀 관측 0** · 재료 채널 셋 | 펄스-에코 음향(E · G · ν · K) · 정속 응력-변형(인장 · 압축) · 정하중 시간 의존(인장 · 압축). 전부 벌크 시편 — 셀 안 관측 0 |
| **Q3** 라벨 층위 | **measured-mechanical(벌크 · 실온)** — 음향 N = 4–10 ± · 압축 항복 4 시편 ± · 나머지 시험당 1 · **`n` 오차 0** | `[재현]` `n` 은 양 끝 한 점씩에 걸려 있다(0.6 MPa 빼면 6.04) · 압축 시간 의존 값은 장치 지배(응력 순서 역전) |
| **Q4** 유일성·식별성 | **0/61 — 쉰세 번째 성질** "creep 기구를 `n` 하나와 남의 지도[32]의 대조로 확정하고(`p` · `Qc` 미측정), 압축 시간 의존 변형은 마찰 · 형상비가 지배해 재료 법칙이 아니라고 스스로 적으면서도 '운전과 가장 닮았다' 고 옮긴다" | `identifiab` · `uncertaint` 0 |
| **Q5** Li-In 기준 | **해당 없음** | `indium` 0 |
| **Q6** 압력 | **칸 이동 없음 — 층 넷** | ① **여덟 번째 인쇄값 · 계보 최초(2018)**: "1.0 MPa range … necessary [9, 10]" + 같은 지면 "not known … we believe … sufficient" ② 원전 지목 **[9] Sharafi 2016 · [10] Wang & Sakamoto 2018**(미열람 · 46호가 [10] 을 "Li 항복 2 MPa" 로 전사) ③ **재료 눈금**: 항복 0.73–0.81 · creep `n` 6.56(0.2–0.6) · 압축 0.8–2.4 · σ/G 경계 0.28 / 2.83 MPa ④ 위 벽 기구의 조건부 판(Fig. 10 — 마찰 · 접착) |
| **Q7** dead Li · Li 재고 | **층 하나** | `[인쇄]` "excess capacity … engineering necessity to account for irreversible material loss during use and to provide the anode with some mechanical stability" · 4 mAh cm⁻² + 50 % → 30 µm. `dead` · `inactive` · `isolated` 0 |
| **Q8** 화학·OCP | **해당 없음** | 양극 0(부피 변화 % 인용만) |

# ★ Q6 — (a) 압력 계보의 값들을 이 편의 눈금 위에 놓는다

계보(카드 13호 항 · 59호 · 60호): 인쇄 요구치 띠 **0.1–5 MPa**(8호 <≈1 · 12호 0.4–1 · 13호 <5 · 25호 ≤5 · 33호 <2 · 39호 1 · 59호 <0.1), 5호 Doux 운전 5 MPa(대칭셀 창 1–75), 60호 정변위 지그 예압 0.8 + 첫 충전 +1.51 MPa.
이 편의 눈금: σ/G(G = 2.83 GPa) · [32] 지도 경계(σ/G 10⁻⁴ 아래 확산 creep · 10⁻³ 위 power-law breakdown — 이 편이 인쇄한 기준) · 항복 0.73–0.81 · 인장 creep 측정 0.2–0.6 · 압축 시험 0.8–2.4.

| 계보 값 (MPa) | 출처 | σ/G | 이 편의 눈금 | `[재현]` 인장 멱법칙(`n` 6.56 · `A` 7.7×10⁻³)으로 1 % 변형 시간 |
|---:|---|---:|---|---|
| 0.1 | 59호 요구치 | 3.5×10⁻⁵ | 시험 범위 밖(< 0.2) · **확산 creep 영역** — 멱법칙 외삽은 **하한**(그 영역은 `n` ≈ 1 로 더 빠르다) | 2×10⁻⁹ s⁻¹ · ≈55 일(하한) |
| 0.2 | 이 편 최저 시험 | 7.1×10⁻⁵ | 측정 2.0×10⁻⁷ s⁻¹ | ≈14 h |
| 0.4 | 12호 0.4–1 하단 | 1.4×10⁻⁴ | 측정 1.3–1.7×10⁻⁵ | ≈10–12 분(측정값) |
| 0.6 | 이 편 최고 인장 시험 | 2.1×10⁻⁴ | 측정 3.9×10⁻⁴ | ≈26 s(측정값) |
| **0.73–0.81** | **항복**(이 편) | 2.6–2.9×10⁻⁴ | 0.2 % 오프셋 · 인장 · 압축 모두 ≈0.8 | ≈10 → 5 s(외삽) |
| **0.8** | 60호 지그 예압("minimum pressure load") · 이 편 압축 하한 | 2.85×10⁻⁴ | 항복 자리 · 압축 12 분 속도 1.93×10⁻⁴(장치 의존) | |
| **1.0** | 이 편 기준값 [9, 10] · 8호 ≈1 · 39호 1 · 12호 상단 | 3.5×10⁻⁴ | "We believe 1 MPa was sufficient" · 압축 1.45×10⁻⁴ → 9.26×10⁻⁶(12 → 120 분) | ≈1.3 s(외삽) |
| 1.48 | 이 편 Fig. 8 | 5.3×10⁻⁴ | 압축 7.83×10⁻⁵ → 4.44×10⁻⁶ | ≈0.09 s(외삽) |
| 2 | 33호 <2 · 4호 ~2 · 6호 2–4 | 7.1×10⁻⁴ | 압축 범위 안 | ≈0.014 s(외삽) |
| ≈2.3 | 60호 정변위 첫 충전 총(0.8 + 1.51) | 8.2×10⁻⁴ | 이 편 압축 상한 근처 — Li 음극이었다면 항복의 ≈3× | |
| 2.4 | 이 편 압축 상한 | 8.5×10⁻⁴ | 압축 4.02×10⁻⁵ → 2.63×10⁻⁶ | ≈4 ms(외삽) |
| **2.83** | σ/G = 10⁻³ | 10⁻³ | **power-law breakdown 경계**([32], 이 편 인쇄) — 그 위는 멱법칙 외삽 무효 | |
| **5** | 5호 운전 · 13호 <5 · 25호 ≤5 | 1.8×10⁻³ | breakdown 영역 · 항복의 6× | (외삽 무효) |
| 10–75 | 5호 위 벽(10 MPa 474 h → 75 MPa 0 h) | 3.5×10⁻³–2.7×10⁻² | 항복의 13–94× | |

`[재현]` 멱법칙 그대로면 0.1 → 5 MPa 는 creep 속도 **(50)^6.56 = 1.4×10¹¹**(11.1 자릿수). 외삽이 무효인 양 끝(확산 영역 · breakdown)을 빼고 **0.28–2.83 MPa 만 잡아도 ×3.8×10⁶**(6.6 자릿수).

`[해석]` **띠는 압력으로는 ×50 인데 Li 의 시간 척도로는 자릿수 6–11 이다.** 그 안에서 결정되는 것은 "Li 이 한 번의 충전(12–120 분) 안에 1 % 변형만큼 계면을 채우는가(≥0.4 MPa) ·
하루(0.2 MPa) · 두 달(0.1 MPa) 인가" 다 — 계보의 값들은 서로 다른 물리 영역의 값이고, "≈1–5 MPa 수렴"(13호 항, 59호가 반박)이 설령 성립했더라도 **한 눈금이 아니었다**.
그리고 5호가 5 MPa 를 "optimal" 이라 부른 자리는 이 편의 눈금으로 **항복의 6배 · breakdown 영역**이다 — 5호의 창(1 MPa 에서 > 500 Ω, 5 MPa 에서 ≈110 Ω)이 Li 이 항복 아래(1 MPa 는 항복
바로 위지만 압축 시험 범위 하단)에서 위로 넘어가며 접촉을 만드는 구간이라는 읽기가 가능하다 — 단 5호 셀은 Li₆PS₅Cl 이고 이 편은 SE 0 이다.

## (a′) 요구치 — 여덟 번째 인쇄값, 그리고 계보의 뿌리 후보

| 편 | 요구치 | 근거 층위 | 원전 |
|---|---|---|---|
| **61호 Masias 2019(2018 온라인)** | **"1.0 MPa range … necessary"**(서론) · "0.8–2.4 MPa … anticipated stack pressures that are required"(방법) · **"not known … We believe 1 MPa was sufficient"**(결과) | **재인용(자기 실험실) + 신념** | **[9] Sharafi 2016 *JPS* 302 · [10] Wang & Sakamoto 2018 *JPS* 377**(미열람) |
| 8호 Li 2026 | < ≈1 MPa | 재인용 | Xu 2024(미수령) |
| 12호 Kouhestani 2022 | 0.4–1 MPa | 재인용(모델 최적) | Tian & Qi 2017 / Shao 2022 |
| 13호 Zheng 2026 | < 5 MPa | 1 차 주장 | [35] 미수령 · [45] = 60호(❌ "5" 없음) |
| 25호 Zhou 2025 | ≤ 5 MPa | 인용 없음 | — |
| 33호 Zhang 2025 | < 2 / ≤ 2 MPa | 인용 없음 | — |
| 39호 Sakka 2022 | 1 MPa | 인용 | Wang · Kazyak · Dasgupta · **Sakamoto** 2021 *Joule*(미열람) |
| 59호 Li Q. 2025 | < 0.1 MPa | 인용 없음 | — |

⇒ **여덟 편 · 여섯 값(0.1 · 0.4–1 · ≈1 · 1 · 2 · 5) · 띠 0.1–5 MPa 그대로 · 확인된 원전 0 그대로.** 새것: (i) 계보에서 **가장 이른 인쇄**(2018-10)이고 (ii) 요구치와 "not known" 을
같은 지면에 적으며(D10) (iii) 원전을 **자기 실험실 두 편**으로 지목한다. `[해석]` "≈1 MPa" 가닥(이 편 · 39호 · 8호 재인용)이 **Sakamoto 실험실 2016–2021 한 뿌리**(Sharafi 2016 → Wang 2018 →
이 편 → Wang 2021 *Joule*)일 가능성 — 원전 넷 중 열어 본 것이 이 편뿐이라 가설이다. [9][10] 을 원장에 올린다(wiki 밖).

## (b) "Li 이 creep 으로 계면을 채운다" — 인쇄된 정량 근거의 목록

| 요소 | 이 편 | 판정 |
|---|---|---|
| 응력 지수 `n` | **6.56**(인장 · 실온 · 0.2–0.6 MPa · 7 시험 · AR ≈4) · 정규화 6.70 · [32] Li 압축 6.4 | ✅ 유일한 정량 근거 · 오차 0 · `[재현]` 양 끝 점에 걸림 |
| 지수앞자리 `A` | 인쇄 0 | `[재현]` 7.7×10⁻³ s⁻¹ MPa⁻ⁿ(Table S1 적합) |
| 활성화 에너지 `Qc` | **0**(온도 1 점) — Fig. 7 은 [32] 의 D 로 정규화(그 값도 지면과 그림이 안 맞음, D4) | ❌ |
| 입도 지수 `p` · 입도 `d` | **0**(입도 미측정 · "assumed polycrystalline") | ❌ |
| 기구 | "dislocation climb rate-limited by lattice diffusion" — `n` 범위 + σ/G 범위 + [32] 지도 대조 | ⚠ 지도 대조뿐 · 미세구조 증거 0 |
| 시간 척도 | 인장: 최소 속도 시점 ≈135 s(0.4 MPa) · 파단 ≈7×10³ s. 압축: 12 · 60 · 120 분에서 1.9×10⁻⁴ → 2.6×10⁻⁶ s⁻¹(0.8–2.4 MPa) | ⚠ 압축 값은 **응력 순서 역전** — 장치 · 기하의 함수(저자 인정) |
| 계면 채움 실험 | **0** — Fig. 10 모식 · "we believe LMSSB will require a constant compressive load to assure contact is maintained" | ❌ |
| 접착 · 마찰 | "if lithium adheres … frictional forces will create hydrostatic stresses that impede deformation" — 계수 0 | ❌ |

⇒ **명제의 정량 근거는 `n` 하나다.** "creep 이 계면을 채운다" 는 이 편에서도 **신념 문장**이고, 이 편이 실제로 준 것은 "채운다면 그 속도는 응력의 6.56 제곱" 이라는 **감도 구조**다.
`[해석]` 그 감도가 우리에게 주는 것: 압력 한 점의 오차 ×2 는 creep 시간 ×94 다 — 압력 되돌림 시험(설계 조건 D1 계측)의 압력 정밀도 요구가 여기서 나온다.

## (c) 벌크 시편 → 셀 접촉 손실 `θ(N)` — 빠지는 것

| # | 이 편 | 셀 | 빠지는 것 |
|---|---|---|---|
| 1 | 벌크 원통 12.7 mm · AR 1–4.6 | Li 박 20–100 µm · AR ≈10⁻⁴(`[인쇄]`) | 저자 스스로 [32] Li 의 ×2 를 AR 로 설명 — AR 4 자릿수 차이의 효과는 지면에 없다 |
| 2 | 압반 마찰(미네랄 오일 · 계수 미지) | SE · 집전체와의 접착 · 마찰(미지) | Fig. 10 의 두 시나리오가 갈리는 변수인데 값이 없다 |
| 3 | 단조 정하중 | 사이클당 ≈1 MPa 급 진동(60호 S14 · 33호) + 정변위/정하중 구속 | 피로 · 래칫 · 하중 제거 뒤 회복 0 |
| 4 | 실온 1 점 | 25–60 °C · `Qc` | 온도 외삽 근거 0 |
| 5 | 멜트 가공 다결정(입도 미지) | 도금 Li(입도 · 결함 · SEI) · 박리 뒤 void | 재료가 다르다 |
| 6 | 인장 creep 은 응력 균일 | 계면 void 채움은 접촉점 응력 집중 · 곡률 | 경계값 문제가 다르다 — 단축 `n` 을 그대로 쓸 수 없다 |
| 7 | 변형 → 응력 (기계만) | 박리 전류 → void 생성 속도 ↔ creep 채움 속도의 경쟁(46호 후속 Kasemchainan 2019 형) | 창의 **아래 벽**을 정하는 경쟁 자체가 이 편에 없다 |
| 8 | 음극 Li 만 | 우리 카드 = 양극 `LAM_PE` ↔ 접촉 손실 | 이 편은 **음극 계면 저항의 시간 상수**로만 우리 3 항 분해(`η(i, P)`)에 들어간다 — `θ_AM`(양극)에는 직접 닿지 않는다 |

# 귀속 검사 — 5호 · 21호 · 46호 · 개념 페이지가 이 편(또는 이 편의 원전)에 매단 것

| 인용처 | 매단 명제 | 이 편 | 판정 |
|---|---|---|---|
| 5호 Doux 2020 ref 15(5호 digest :205) | E · G · ν 상온 측정 | 7.82 · 2.83 GPa · 0.381 | ✅ |
| 〃 | 항복강도 ≈0.8 MPa | 0.73–0.81(인장) · 0.81 ± 0.10(압축 변곡) | ✅ |
| 〃 | **그 위에서 creep 시작** | `[인쇄]` "studied at loads **below** the 0.8 MPa yield point between 0.2 and 0.6 MPa" · 그 범위에서 `n` = 6.56 | ❌ **creep 은 항복 아래에서 쟀다** — 항복은 creep 문턱이 아니다(5호 digest 문장 기준; Doux 원문 어구 미열람) |
| 〃 | Tariq 2003 과 일치 | `[인쇄]` "in agreement with those obtained with pulse echo [26, This Work]"(E) · Table 3 Tariq 0.76 ↔ 0.73–0.81 | ✅ |
| 21호 Sedlmeier 2023 ref 49(21호 digest :366) | 원통 펠릿에서 Li 가 In 가장자리 · 벽 사이로 분리막 쪽에 기어드는 Li creep | 펠릿 · In · 분리막 0. Fig. 10a–c: 마찰 없으면 Li 가 옆으로 흘러 SE · 양극이 가라앉는 모식 | ✅ 재료 전제 · ⚠ 기하 명제는 21호 자신의 것 |
| 21호 :119 · :165 | Li\|Li 셀 3 MPa · 분리막 네 장 — Li creep 방지 | 3 MPa = 항복의 ≈4× · 압축 시험 범위 위 · σ/G 1.06×10⁻³(breakdown 경계 근처) | `[해석]` "방지" 가 아니라 **가장 빨리 흐르는 쪽**이다 — 21호가 분리막 두께로 막은 것이지 압력으로 막은 것이 아니다 |
| 46호 Schlenker 2020 ref 51(46호 digest :207 · :379) | **Wang & Sakamoto 2018 = "Li 항복 2 MPa"** → 비커스 ≈6 MPa 논증 | 같은 실험실 1 년 뒤 이 편: **0.73–0.81 MPa** · 문헌 µm 급 다결정 0.60–0.81 | ⚠ **같은 그룹의 두 인쇄값이 2.5× 다르다** — Wang 2018 미열람(46호 전사 기준). `[해석]` 46호 논증(44 MPa 에서도 계면 임피던스가 계속 준다 → Li 경도로는 설명 불가)은 항복이 낮을수록 **더 강해진다** |
| [[assb-stack-pressure-operating-window]] §정의 | "Li 가 항복강도(≈0.8 MPa)를 넘어 크리프하고" | 항복 아래 0.2–0.6 MPa 에서 멱법칙 creep · 항복 위(0.8–2.4)는 시간 의존 변형(장치 지배) | ❌ 정정 필요 — "넘어 크리프" 가 아니라 "creep 속도가 σ^6.56 로 커진다" |
| 14호 Oh 2025 ref 70 = LePage 2019 · 5호 ref 18 | "10 MPa 는 Li creep 을 일으키기에 충분" · "상온 항복은 creep 지배" | 10 MPa = σ/G 3.5×10⁻³ = breakdown 영역 · 항복의 13× | ✅ 방향 일치(a fortiori) — LePage 미열람 |

# 인용 대조 — 우리 위키에 원전 · 관련 digest 가 있는 것

| 이 편 인용 | 우리 호 | 이 편이 적은 것 | 대조 |
|---|---|---|---|
| [4] Monroe & Newman 2005 · [5] Ferrese & Newman 2014 | 5호 refs 4 · 5 | G_SE ≥ 2 G_Li | 5호: "그 기준을 만족하는 단결정 LLZO 에서도 관통" — 이 편은 그 반례를 적지 않는다(2018) |
| [10] Wang & Sakamoto 2018 *JPS* 377, 7 | 46호 ref 51(미열람) | "1.0 MPa range … necessary" 의 원전 · 접착 강도 [10, 23] | 46호 전사 "Li 항복 2 MPa" ↔ 이 편 0.73–0.81(위 표) |
| [30] Xu … Greer 2017 *PNAS* 114, 57 | 46호 ref 54(미열람) | sub-micron Li 항복 15–105 MPa(298 K) | 46호: "≈200 MPa" 로 전사 — 이 편 Table 3 는 15–105 |
| [32] Sargent & Ashby 1984 | — | `n` 6.4(Li 압축) · 지도 경계 · D · G(Na · K) | 이 편의 기구 배정 · Fig. 7 전부가 여기 의존 · 미열람 |
| [9] Sharafi … Sakamoto 2016 *JPS* 302, 135 | — | 1 MPa 의 원전 · "Li–LLZO interface … temperature and current density" | 미열람 · 원장 §1 에 없음 |
| [23] Sharafi … Dasgupta, Sakamoto 2017 *Chem. Mater.* 29, 7961 | — | 접착 강도 · 초저 계면 저항(LLZO 표면 화학) | 미열람 |

⚠ 이 편(2018)은 5호(2020) · 21호(2023) · 46호(2020) · 59 · 60호를 인용하지 않는다 — 시점상 불가. 우리 계보에서 이 편보다 이른 편은 없다(Koerver 2017 = 23호는 양극 편).

# ★ 카드의 틀로 — 이 편이 우리 3 항 분해에 들어가는 자리 (`[해석]`)

## (ㄱ) `η(i, P)` 의 음극 몫에 시간 상수가 붙는다

[[assb-apparent-capacity-decomposition]] 의 `Q_apparent = θ_AM · η(i) · Q_material` 에서 압력 개념 페이지는 `η = η(i, P)` 로 넓히자고 했다. 이 편은 그 `P` 의존이 **즉각적이 아니라 시간 의존**이고
그 시간이 **σ^6.56** 에 걸려 있다는 것을 준다(음극 Li\|SE 쪽). `[재현]` 0.2 MPa 에서 1 % 변형 ≈14 h · 1 MPa ≈1 s(외삽). ⇒ 같은 "운전 압력 X MPa" 라도 **압력을 건 뒤 얼마 뒤에 잰 값인지**가
음극 저항을 정한다 — 압력 되돌림 시험의 설계 조건 D1(사이클 해상 계측)에 **유지 시간**이 붙어야 한다.

## (ㄴ) 회복의 시간 상수가 전극을 가를 수 있다 — 미검증 제안

`P↑` 연산자(4호 Shi 2020 300 MPa 재가압 · 11호 Yu 2024)가 되돌린 용량 · 임피던스 중 **초–분 안에 돌아오는 몫**은 이 편의 눈금으로 Li\|SE creep(≥1 MPa 에서 초 단위)이고, 양극 복합체(취성 SE · CAM,
creep 0)의 접촉 복원은 탄성 접촉(즉각) 아니면 안 돌아온다. ⇒ 재가압 뒤 **임피던스의 시간 곡선**(초 → 시간)이 회복 몫을 음극/양극으로 가를 수 있다(`[해석]` · 실측 0 · 3전극이면 직접 확인 가능 — 16호 형).
이것은 카드의 물음(양극 `LAM_PE` ↔ 접촉 손실)에 대한 **음극 오염을 빼는 절차**다 — 압력 개념 페이지 §"전극 귀속"(4호 귀속 문제)에 붙는다.

## (ㄷ) 합성 truth 의 운전 압력을 "가정" 으로 표시할 때 붙일 단서

[[assb-synthetic-truth-contact-loss-requirements]] 의 운전 압력은 가정이다(59호 새 제약 2). 이 편은 그 가정에 **"어느 영역인가"** 를 붙이게 한다: < 0.28 MPa(확산) · 0.28–2.83(멱법칙 · 항복 0.8 포함) · > 2.83(breakdown).
합성 truth 가 `θ(N)` 을 압력 비의존 상수로 두는 한 이 단서는 쓸 곳이 없다 — 압력 의존 `θ(P, t)` 를 넣을 때의 입력이다(R4 · R5 의 확장).

# 곱 축퇴 처방 — 마흔네 번째 적용 (`[[assb-lampe-contact-product-degeneracy]]`)

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | 전기화학 0 | ❌ |
| **2단계** (18 · 25호) | + 면적을 아는 대조군 | 압반 접촉 면적 +25 %(기계) | ❌ |
| **3단계-a/b** (19호) | `Ea` · `C` 상한 | 온도 1 점(`Qc` 0) | ❌ |
| **4단계** (20호) | 시간 영역 동일 검사 | 시간 의존 **변형**(전기화학 아님) | ❌ |
| 52호 줄 | 누적 결손 ↔ Li 재고 | 셀 0 | — |

⇒ **적용 불가 — 대상 없음.** 32 · 33 · 59 · 60호처럼 한 번으로 센다. 기록 이유: 처방의 압력 연산자(2단계의 "면적을 아는 대조군" 을 압력으로 만드는 4 · 11 · 39호 형)에 **음극 쪽 시간 상수**가 있다는 것 —
위 (ㄴ). 처방 표에는 행을 더하지 않는다(양극 곱 자체에 닿지 않는다).

# 보류 결정 (가)(나)(다)(아)(자)(차)(타) — 이 편이 주는 근거 (결정 안 함)

원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §3-b 와 대조. **결정은 사용자 몫이고, 이 편은 어느 항목에도 근거를 주지 않는다.**

| # | 결정 | 이 편 | 근거 |
|---|---|---|---|
| 가 | 29호 Q4 +0.5 유지 | 무관 | 적합 · 정적/동적 축 0 |
| 나 | 38호 Q2 +0.5 유지 | 무관 | 활성 질량 · 채널 0 |
| 다 | 28호 Bizeray 를 ASSB Q4 분모에 | 무관 | 식별성 방법 0 |
| 아 | 35호 합성 쌍 → Roman 특징 재계산 | 무관 | ML 0 |
| 자 | 31호 ICI zenodo `R/k` 면적 소거 | 무관 | 전기화학 0 |
| 차 | 23호 PyBaMM 면적 노브 / `j₀` 노브 분리 | 무관 | 양극 모델 0 — `[해석]` 정성 메모: 압력 의존 `θ(P, t)` 를 넣는다면 음극 `R_int(P, t)` 는 별도 노브 |
| 타 | Navidi 2024 digest 재점검 | 무관 | — |

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 어디 | 판정 |
|---|---|---|---|
| **D1** | ★★ **SS/PE ↔ 0.81/0.73 의 대응이 본문과 Table 3 에서 반대** — 본문 "0.81 and 0.73 MPa (Table 3) when using E values of 7.82 and 0.43 GPa, respectively" ↔ Table 3 *SS(0.43 GPa 기울기) → 0.81 · **PE(7.82) → 0.73. `[도표]` 인셋 교점 PE ≈0.62–0.65 · SS ≈0.75–0.78 — Table 3 순서(PE 가 낮다)가 물리적으로 맞고, 두 값 모두 인쇄보다 ≈0.06–0.10 낮게 읽힌다 | p. 2590 ↔ Table 3 ↔ Fig. 2 | 본문 "respectively" 오류로 읽힌다; 판독 차는 판독 오차 범위일 수 있다 |
| **D2** | ★★ **"0.4 % 이후 응력 감소"** ↔ Fig. 2: `[도표]` ≈4 % 까지 상승(정점 ≈0.93 MPa), 인셋 1 % 에서 ≈0.88 로 상승 중 | p. 2590 ↔ Fig. 2 | "4 %" 오타 또는 항복점(0.4 %) 뒤 "감소" 의 오기 |
| **D3** | ★★ **σ/G 저/고 뒤바뀜** — "2.2×10⁻⁴ at the low stress level and 7.1×10⁻⁵ at the high stress level" ↔ Table S1 0.2 MPa 7.13E-5 · 0.6 MPa 2.13E-4 | p. 2595 ↔ Table S1 | 전사 오류 — 결론(전위 creep 범위)은 불변 |
| **D4** | ★★ **Fig. 7 의 `D`** — 본문 "room-temperature lattice diffusivity Li (D = 3.1×10⁻¹ cm²/s)" ↔ `[재현]` 그림 축값(ε̇/D ≈2.2×10³ · 4.5×10⁶)과 Table S1 속도로 **D ≈ 9×10⁻¹¹ cm² s⁻¹**; 인쇄값으로는 점이 축 밖(≈10⁻⁷–10⁻³). Li 와 K 의 D 가 같은 값(3.1×10⁻¹)으로 인쇄 | p. 2595 ↔ Fig. 7 | 인쇄값은 `D₀` 크기 — 정규화 결론(한 선 · 6.70)은 그림 기준 성립 |
| **D5** | ★ **크로스헤드 "1 mm/s" ↔ 1.22×10⁻³ s⁻¹** — `[재현]` 15.5 mm 시편이면 6.5×10⁻² s⁻¹; 1 mm/**min** 이면 1.08×10⁻³(13.7 mm 게이지에서 1.22×10⁻³). Table 3 는 1.21 | p. 2588 ↔ Fig. 2 캡션 · Table 3 | 단위 오기(mm/min)로 읽힌다 |
| **D6** | ★ Table 3 "this work" AR **1.10** ↔ Fig. 2 시편 15.5/12.7 = 1.22 · Fig. 3 12.3/12.7 = 0.97 | Table 3 ↔ 캡션 | 대표 시편이 다르거나 반올림 |
| **D7** | ★ 본문 "two groups … 7.8–8.0 and **10.5–10.6 GPa**" · "span … 1.9 and 10.6 GPa (see Table 1)" ↔ Table 1 에 10.5–10.6 없음(단결정 *21.2 · *3.0 만) | p. 2589 ↔ Table 1 | 표에서 빠진 문헌값 |
| **D8** | ★ SI σ/G 열 → G = **2.79–2.82 GPa**(`[재현]`) ↔ 본문 평균 2.83 | SI ↔ Table 2 | 2.81 로 계산한 듯 — 0.7 % |
| **D9** | ⚠ "our previous solid-state cycling studies of Li metal used … 1 MPa [9, 10, 33]" — [33] Yu 2016 *Chem. Mater.* 는 LLZO 탄성 논문 | p. 2595 ↔ 참고문헌 | 인용 번호 오기 가능 |
| **D10** | ⚠ 서론 "1.0 MPa range are **necessary**" [9, 10] ↔ 결과 "How much compressive stress is **not known** … We believe 1 MPa was sufficient" | p. 2586 ↔ p. 2595 | 같은 값이 요구치와 미지/신념으로 두 번 |
| **D11** | ⚠ SI 표 제목 · 열 "Pressure" 가 **인장** 응력(Table S1) · SI "Compression **Creep**" ↔ 본문은 압축을 "time-dependent deformation" 으로 부르고 creep 법칙 해석을 피한다 | SI ↔ 본문 | 어휘 불일치 |
| **D12** | ⚠ Fig. 5 응력이 캡션 · 본문에 없고 범례에만 "0.4MPa"; 0.4 MPa 시험 셋 중 어느 것인지 0 | Fig. 5 | G9 |
| **D13** | ⚠ Table 2: 0.75 mm 시편 Vl ±0.26(5 %) → K 9.92 vs 11.18 · 12.12 — "independent of sample size" 는 E · G 에만 | Table 2 ↔ p. 2589 | K 폭 20 % |
| **D14** | ⚠ Fig. 8 정하중 구간이 시작될 때 변형률 `[도표]` ≈25–30 % — 본문은 배럴링만 적고 사전 변형을 적지 않는다 | Fig. 8 ↔ p. 2596 | 압축 "creep" 의 초기 상태 |
| **D15** | ⚠ 셀 AR 1.2E-4 · 7.5E-5 · 2.2E-5 ↔ `[재현]` 30 µm 로 1.3E-4 · 8.5E-5 · 2.4E-5(≈10 %; ≈27 µm 면 일치) | p. 2588 | 반올림 · 두께 |
| **D16** | ⚠ 결론 "power-law creep … when a stress relevant to LMSSB was applied (~1 MPa)" ↔ 인장 creep 은 0.2–0.6 MPa | p. 2598 ↔ p. 2588 | "~1 MPa" 는 시험 범위 밖 |

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. ★★★ **압력 계보 0.1–5 MPa 는 Li 의 눈금으로 한 물리가 아니다** — 확산 creep(< 0.28) → 멱법칙(0.2–0.6 측정, `n` 6.56) → 항복(0.73–0.81) → 압축 시험(0.8–2.4) → breakdown(> 2.83). 압력 ×50 = creep 속도 6–11 자릿수(`[재현]`).
   5호의 5 MPa 는 breakdown 영역 · 항복의 6×; 60호 예압 0.8 은 항복 자리; 60호 첫 충전 총 ≈2.3 MPa 는 압축 상한 근처.
2. ★★★ **5호 ref 15 의 "항복 위에서 creep 시작" 은 이 편이 주지 않는다** — creep 은 항복 아래에서 쟀다. 개념 페이지 §정의의 "항복강도를 넘어 크리프" 도 같은 정정. 21호 ref 49 는 재료 전제만 선다.
3. ★★★ **"creep 이 계면을 채운다" 의 정량 근거는 `n` 하나** — `Qc` · `d` · `p` · 채움 실험 · 접착 계수 0; 압축 시간 의존 값은 응력 순서가 역전된 장치 값. 명제는 Fig. 10 + "we believe".
4. ★★ **요구치 계보 여덟 번째 · 가장 이른 인쇄(2018)** — "1.0 MPa range … necessary [9, 10]" 와 "not known … we believe sufficient" 가 같은 지면. 원전 [9] Sharafi 2016 · [10] Wang & Sakamoto 2018(원장 등록 필요, wiki 밖).
   `[해석]` "≈1 MPa" 가닥의 Sakamoto 실험실 한 뿌리 가설.
5. ★★ **46호 대조** — 같은 실험실의 Wang 2018 이 46호 전사로 "Li 항복 2 MPa", 이 편은 0.73–0.81. Wang 2018 을 열어야 닫힌다(지목 2 회째).
6. ★★ **회복 시간 상수로 전극 가르기**(`[해석]`) — 재가압 뒤 초–분 회복 = Li\|SE creep, 안 돌아오는 몫 = 양극 복합체. 압력 되돌림 시험 D1 에 유지 시간 · 시간 곡선을 붙인다(결정은 사용자 몫).
7. ★ **Li 과잉 설계의 인쇄된 이유** — `[인쇄]` "excess capacity … irreversible material loss … mechanical stability"(Q7 층).

# 후속 후보 (원전 우선)

참고문헌 34 편 중 우리 축(Q6 · Q7 · 재료 눈금)에 닿는 것만. **셀 · 열화 · 식별성 원전 0.**

| 서지 | ref | 왜 | 축 | 우선 |
|---|---|---|---|---|
| **Sharafi A., Meyer H.M., Nanda J., Wolfenstine J., Sakamoto J. 2016 *J. Power Sources* 302, 135** — "Characterizing the Li–Li₇La₃Zr₂O₁₂ interface stability and kinetics as a function of temperature and current density" | [9] | **"1.0 MPa range … necessary" 의 두 원전 중 하나 · 계보 "≈1 MPa" 가닥의 2016 뿌리 후보** — 원장 §1 에 없음 → 등록 요청 | Q6 | ★★★ |
| **Wang M., Sakamoto J. 2018 *J. Power Sources* 377, 7** — "Correlating the interface resistance and surface adhesion of the Li metal-solid electrolyte interface" | [10] | 다른 하나 · 46호 ref 51(원장 ★ 행, "Li 항복 2 MPa")과 **같은 편 → 지목 2 회(46 · 61)** · 이 편 0.73–0.81 과의 2.5× 대조 · 접착 ↔ 계면 저항 | Q6 · Q7 | ★★★ |
| **Wang·Kazyak·Dasgupta·Sakamoto 2021 *Joule* 5, 1371** | (이 편 이후) | 39호 "1 MPa practically" 원전(원장 ★★★ 행) — 이 편과 같은 실험실 → 한 뿌리 가설의 확인처 · 재지목 | Q6 | ★★★(기존) |
| **Sargent P.M., Ashby M.F. 1984 *Scr. Metall.* 18, 145** — "Deformation mechanism maps for alkali metals" | [32] | 이 편의 기구 배정 · σ/G 경계(10⁻⁴ · 10⁻³) · Li 압축 `n` 6.4 · D · G 값의 원전 — D4 의 D 값 확인처 | 재료 눈금 | ★★ |
| **LePage … Dasgupta 2019 *JES* 166, A89** | (이 편 이후; 14호 ref 70 · 5호 ref 18) | "상온 Li 항복은 creep 지배" · "10 MPa 는 creep 충분" — 이 편 다음 세대의 Li 역학 원전(카드 후속 5 순위 기존) · 이 편과의 `n` · 항복 대조 | Q6 | ★★(기존) |
| Tariq S., Ammigan K., Hurh P., Schultz R. 2003 PAC, 1452 | [13] | E 7.8(extensometer) · σ_y 0.76 · 변형률 속도 의존 — 5호가 "Tariq 2003 과 일치" 로 인용 | 재료 | ★ |
| Xu C., Ahmad Z., Aryanfar A., Viswanathan V., Greer J.R. 2017 *PNAS* 114, 57 | [30] | sub-micron Li 15–105 MPa — 46호 ref 54(원장 행) → 지목 2 회; 46호 전사 "≈200 MPa" ↔ 이 편 표 15–105 | Q7 | ★(기존) |
| Monroe C., Newman J. 2005 *JES* 152, A396 | [4] | G_SE ≥ 2 G_Li — 5호 refs 4 · 5 와 같은 원전; 이 편의 G 가 그 기준의 입력(≥ 5.66 GPa) | Q6 | ★ |
| Schultz R. 2002 Fermilab TM-2191 · Hull & Rosenberg 1959 *Phil. Mag.* 4, 303 | [12] · [31] | 압축 0.64 · 인장 0.60 MPa — 문헌 항복 산포의 양 끝 | 재료 | ☆ |

# 이 digest 가 주장하지 않는 것

- **Li 이 계면을 creep 으로 채우지 않는다고 하지 않는다** — 주장은 "이 편이 그 명제를 재지 않았고, 준 것은 `n` = 6.56 의 감도 구조" 까지다.
- **계보의 값들이 틀렸다고 하지 않는다** — 값들이 이 편의 눈금으로 서로 다른 물리 영역에 놓인다는 것까지. 영역 경계(0.28 · 2.83 MPa)는 이 편이 인쇄한 [32] 의 σ/G 기준을 이 편의 G 로 환산한 것이다.
- **멱법칙 외삽값(1 % 변형 시간)을 셀의 값으로 옮기지 않는다** — 벌크 · 인장 · AR 4 · 실온 · 단조 하중의 외삽이고, 0.1 MPa 쪽은 하한 · 2.83 MPa 위는 무효다.
- **압축 Table S2 의 값을 Li 의 creep 속도로 쓰지 않는다** — 응력 순서가 역전된 장치 값이다(저자 인정).
- **5호 Doux 2020 이 "항복 위에서 creep 시작" 이라고 썼다고 단정하지 않는다** — 5호 digest 의 문장 기준이고 Doux 원문 PDF 는 이 세션에 없다.
- **Wang & Sakamoto 2018 의 항복이 2 MPa 라고도, 46호 전사가 틀렸다고도 하지 않는다** — 원전 미열람.
- **"≈1 MPa 가닥 = Sakamoto 실험실 한 뿌리" 를 사실로 적지 않는다** — 원전 넷 중 열어 본 것이 이 편뿐이다.
- **회복 시간 상수로 전극을 가른다는 것은 제안이다** — 실측 0.
- **Table 1 · 2 · 3 의 이미지는 보지 않았다** — 값은 PDF 텍스트에서 옮겼다(SI 표 둘은 이미지로 열 대응을 확인했다).
