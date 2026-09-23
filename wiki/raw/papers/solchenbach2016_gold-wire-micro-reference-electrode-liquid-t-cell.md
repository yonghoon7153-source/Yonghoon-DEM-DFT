---
title: "Solchenbach, Pritzl, Kong, Landesfeind, Gasteiger 2016 — A Gold Micro-Reference Electrode for Impedance and Potential Measurements in Lithium Ion Batteries (J. Electrochem. Soc. 163, A2265)"
source_url: local-upload/9._A_gold_micro-reference_electrode_for_impedance_and_potential_measurements_in_lithium_ion_batteries.pdf
source_url_note: "PDF 9 쪽(1 쪽 = IOP 다운로드 표지, 논문 8 쪽, 참고문헌 53). SI 없음. 액체셀(LP57, Swagelok T-셀) 논문 — ASSB 0. 크로퍼 8 장(Fig. 1-8) 전부 봤다, 화소 판독 Fig. 2b · 2c · 5 · 6a(원본 래스터). 원자료 · PDF 는 커밋하지 않는다. 21호(Sedlmeier 2023) ref 11 · 45호(Hertle 2023) ref [20] 이 지목한 금선 기준극(GWRE) 원전."
source_doi: 10.1149/2.0581610jes
source_license: "CC BY 4.0, (c) The Author(s) 2016, published by ECS — open access"
pdf_sha256: 8cff1ea8fa561dffc2cf8dbae1f50bc4a02f17685a582c6e341ae59171c07529
ingested: 2026-09-23
sha256: 5b0fd38b17fe8fd352b4b8f869667fab93451907e51fd4b858667de27f161684
---

# 수집 목적

`assb` 섹션 **47호**. 큐 **48번**(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g, 2차 묶음 아홉째 편).
닻은 `questions/assb-contact-loss-vs-lampe.md` 의 **Q5**. 원장 ★★★ · 지목 2 회:
21호(Sedlmeier 2023, 같은 TUM Gasteiger 연구실) 가 ref 11 로 — **GWRE 0.31 V 와 "리튬화한 쪽 Li 전극이 거칠어져 호가 작다"
가설의 출처**, 45호(Hertle 2023) 가 ref [20] 으로 — **유일하게 인용한 금선 선례 + Au–Li 평탄값(134 / 215 mV) 출처 중 하나**.
두 관례(21호 0.31 V · 45호 0 V)의 **공통 조상 후보**로 걸려 있었다.

> ⚠⚠ **이 편은 액체셀이다.** 1 M LiPF₆ EC:EMC(LP57) · 유리섬유 분리막 · Swagelok T-셀. 고체 전해질 · 압력 · ASSB 는 지면에 0 이다.
> 그래서 이 편이 ASSB 칸에 줄 수 있는 것은 **원전 조건(도구 · 계보 칸)** 이다 — 28호(Bizeray) · 31호(Chien) 와 같은 자리.

> 표기: `[인쇄]` 본문 명시 · `[도표]` 그림에서만 읽은 값(`figure-read ≈`, 판독 오차 붙음) ·
> `[재현]` 우리가 지면의 숫자로 계산한 값 · `[해석]` 우리 해석.
> **`[해석]` 표시 없는 문장은 원문이 실제로 말한 것이다.**

---

# 원문에 없어서 확인이 필요한 것 (공백 먼저)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **0.311 V 를 낸 LixAu 의 조성 · 리튬화 깊이 미인쇄.** 인쇄는 "0 < x < ∼1.2 의 OCV"(ref 25 Bach 2015 인용)뿐. 150 nAh 가 단면 끝에서 얼마나 깊이 들어갔는지 · 축 방향 확산을 잰 측정 0 | `[재현]` 평균 x ≤ 1.2 가 되려면 끝에서 **≥ ≈24 µm**(지름의 ≈½) 까지 퍼져야 한다(아래 §3). 저자의 "축 방향 확산이 충분히 느리다" 와 크기 긴장 |
| **G2** | **표류의 수 = "초기 20 h 뒤 < 2 mV" 한 문장.** 추적 그림은 Fig. 2b 하나(셀 1 개씩, 25 °C 2 곡선 · 40 °C 1 곡선) | `[도표]` 20 h → 300 h 사이 ≈3.0 mV 움직인다(D1). 판정 문턱이 ±1 mV 급이면 "20 h" 는 "≈50 h" 다 |
| **G3** | **누설(자기 탈리튬) 전류 측정 0**(`leak` 0 회). 40 °C 표류를 `[인쇄]` "SEI growth and the concomitant self-delithiation" → "rapid depletion of lithium at the wire's tip" 로 **해석**(기구 서술, 측정 아님) | (5′) 기준극 판의 분모. `[재현]` 25 °C 간접 상한 **< ≈0.27 nA**, 40 °C(25 °C 리튬화) 소진 해석이면 **≈2.5 nA** |
| **G4** | **"CE(여기서는 WE) 거칠어짐" 가설 = `[인쇄]` "We believe"** — Li 표면 관찰 · 대조군(반대 전극에서 리튬화 · 비리튬화 셀) · 반복 0, 셀 1 개 | 21호가 "액체셀 선례" 로 가져갔다. `[재현]` 뺀 Li 는 균일 두께 **≈0.77 nm** |
| **G5** | **대칭셀 대조의 셀 간 산포 기준 없음** — "essentially identical" 을 셀 간 산포와 대지 않았다. 같은 지면의 다른 그림이 같은 상태에서 흑연 호를 ×1.6 다르게 보인다(D5) | 검증의 분해능이 정해지지 않는다 |
| **G6** | **고전압(>4.7 V) 양극에서의 수명 제한 · 재리튬화는 ref 33(Pritzl, Solchenbach, Gasteiger "Manuscript in preparation")** — 수 · 그림 0 | 안정성 조건 목록에 "상대극 전위" 축이 있다는 문장만 있다 |
| **G7** | **셀 압력 값 0**(스프링 T-셀, `pressure` 0 회 · `MPa` 1 회 = 전극 압연 260 MPa) | ASSB 로 옮길 때 가장 큰 변수 하나가 원전에 없다 |
| **G8** | **Au–Li 평탄값 "134 / 215 mV" 가 이 지면에 없다.** 인쇄는 "첫 단 OCV ∼0.3 V · 둘째 단 ∼0.2 V"(Bach 2015 인용) | 45호가 [20] 을 134 / 215 mV 의 출처 중 하나로 달았다 — 이 편만으로는 지지 안 됨(D6) |

---

# 판정 (먼저)

## (1) Q5 — 0.31 V 는 무엇이고, 어떻게 쟀나

| 물음 | 이 편 | 판정 |
|---|---|---|
| **무엇 대비** | **Li 금속 대비 직접**: 대칭 Li\|Li T-셀(Li 원판 ∅11 mm × 450 µm 두 장, LP57) 가운데에 GWRE. `[인쇄]` "the potential of the GWRE vs. Li/Li⁺" — 측정 축 그대로(Fig. 2a·b 축 "V vs. Li/Li⁺") | ✅ **측정** — 환산 0. 계보의 0.31 V 는 여기서 처음 Li 대비로 **잰** 값이다 |
| **어느 상** | `[인쇄]` "the potential of the GWRE shoots up to 0.318 V and then quickly relaxes to ∼0.311 V vs. Li/Li⁺, which corresponds to the OCV potential of a LixAu alloy with 0 < x < ∼1.2 [25]" · 서론 `[인쇄]` "already low degrees of lithiation will result in an OCV of around 0.31 V" | **Au-풍부 첫 단(2상) 의 개방회로 전위.** 상 이름은 주지 않는다 — 서론 `[인쇄]` 중간상은 "could not be assigned to any of the known thermodynamic Li-Au phases", Bach 2016(ref 30) 준안정 Li₃Au₂ · Li₅Au₃ · Li₃Au₅ · LiAu₂ |
| **리튬화 량 · 전류** | `[인쇄]` 150 nA × 1 h(Li WE 또는 LFP 에서) = **150 nAh** · 전류 범위 10 µA, 정확도 0.1 % → `[인쇄]` "error of ∼10 nA" · 25 °C(또는 40 °C) | `[재현]` 단면(∅50 µm, 1.96 × 10⁻³ mm²)만 노출 → **7.6 mA cm⁻² · 7.6 mAh cm⁻²** · 전하 ±≈7 % |
| **리튬화 중 전위** | `[인쇄]` "drops briefly below 0 V … then stays constant at ∼0.2 V" · `[도표]` 25 °C 두 곡선 ≈0.17 → 0.20 · ≈0.08 → 0.18 V(하나는 시작에 ≈−0.1 V 순간) · 40 °C ≈0.25 → 0.22 V | 과전압 ≈0.1 V — 도금(0 V) 칸에 **닿지 않는다** |
| **안정성(수 · 기간)** | `[인쇄]` "remains stable for more than 500 h, varying by less than 2 mV after the initial 20 h" · `[도표]` 25 °C 곡선 2 h **317.7** → 21 h **314.3** → 100 h ≈312.0 → 200–300 h **311.3–311.4** → 545 h **311.8 mV**(±0.3 mV, 0.14 mV/px) | ✅ **계보 첫 Li 대비 장기 추적 그림** — 단 액체 · 셀 1 개. ⚠ "20 h 뒤 < 2 mV" ↔ `[도표]` ≈3.0 mV(D1), "quickly relaxes" ↔ 0.311 도달 ≈150–250 h(D2) |
| **초기 창** | `[인쇄]` "the lithiated GWRE might not be suitable for highly accurate potential measurements during initial cycles, but is sufficient for tracking electrode potentials during prolonged cycling" | ★ **원전 스스로 초기 ≈20 h 를 정밀 영점에서 뺐다** — 21호는 2 h 에 읽었다(아래 (3)) |
| **온도 이력** | 25 °C 리튬화 → 40 °C: `[인쇄]` "starts to drift to more positive values after less than 10 hours" · `[도표]` 5 h 315.5 → 21 h 317.1 → 33 h 319.7 → 50 h ≈329 → **≈60 h 에 0.35 V 축을 벗어남**. 40 °C 리튬화 → 40 °C: `[인쇄]` 같은 안정성 "shifted downwards by 1–2 mV" · `[도표]` 21 h 309.7 → 100–135 h 308.8 → 493 h 309.7(범위 ≈1 mV), 25 °C 장기값 대비 **−2 mV** | ★★ **영점이 리튬화 온도에 1–2 mV 걸린다 · 리튬화 온도 < 운전 온도면 수십 시간 안에 이탈.** 기구는 `[인쇄]` "we hypothesize"(고온 SEI 무기물 多) · "not clear at this point" |
| **재리튬화** | `[인쇄]` "a re-lithiation of the wire with the same procedure at 25 °C restored a stable GWRE potential of 0.311 V vs. Li/Li⁺, as long as the cell was kept at 25 °C" · 고전압(>4.7 V) 양극에서도 "could be relithiated"(ref 33) | ✅ 소모품 · 재충전 절차의 **원형**(45호 "refresh" 보다 7 년 앞) — 재리튬화 뒤 값 · 횟수 · 그림 0 |
| **누설** | `leak` 0 · 자기 탈리튬은 기구 서술만 | **누설 직접 측정 0/47.** `[재현]` 25 °C: 150 nAh 가 ≈550 h 동안 창을 안 벗어남 → **< ≈0.27 nA**(단면 면적당 < ≈14 µA cm⁻²) · (5′) ≥ 10 을 550 h 에 보증하려면 **< ≈0.03 nA** — 지면에 없다. 40 °C 이탈(≈60 h)을 전량 소진으로 읽으면 **≈2.5 nA**(≥ ×9) |
| **사이클 중 확인** | `[인쇄]` Fig. 6 "The LFP potential center vs. lithiated GWRE remains constant during cycling, meaning that the lithiated GWRE maintains its stable potential of 0.311 V" · 3.11 V vs GWRE → "calculated value of 3.42 V vs. Li/Li⁺, which matches well with the true LFP equilibrium potential [40]" | `[도표]` 60 mAh g⁻¹ 에서 충전 띠 3.13–3.18 · 방전 띠 3.04–3.08 V(네 사이클 한 띠) → 중점 ≈3.11 V, **분해능 ≈±20 mV**(6.5 mV/px, 선 두께). `[해석]` **LFP 2상 평탄을 내부 표준으로 쓴 P10 의 액체 원형** — 수 미인쇄 · 문헌값 대조는 P6 형(증인 한 개) |

⇒ **Q5 스물세 번째 형태 — "원전 측정: 영점을 Li 금속 대비 개방회로로 수백 시간 추적하고, 그 영점을 쓸 조건(초기 이완 창 · 리튬화 온도 = 운전 온도 · 단면만 노출 · 재리튬화)을 같이 인쇄했다 — 액체셀에서"**.
칸은 **움직이지 않는다**(반 칸 검토 후 접음): 측정 · 명제가 전부 **액체** 이고, ASSB 로 옮길 근거(같은 선을 고체에서 잰 대조)는 이 지면에 0 — 28 · 31호 "도구 칸" 선례.

## (2) 0.31 V ↔ 0 V — 같은 선의 다른 칸이다

| 칸 | 이 편 `[인쇄]`(Bach 2015 인용) | 45호 Hertle `[인쇄]`(refs 20 · 33–35 인용) | 45호 `[도표]`(45호 digest) |
|---|---|---|---|
| Au + 첫 Li–Au 상(x < ≈1.2) | OCV **∼0.3 V**, 측정 **0.311 V** | "E(Au/AuLi) = **215 mV** … in OCV" | 전류 중 +0.21–0.25 V |
| 둘째 단 | OCV **∼0.2 V** | "E(AuLi/AuLi₃) = **134 mV**" | 개방회로 **+0.133 V** |
| 최대 리튬 상 | "Li₃Au … 408 mAh g⁻¹_Au"(가장 Li-풍부한 전기화학 상) | "complete lithiation of gold to AuLi₃" | — |
| 도금 Li | **논의 0**(`plat*` 7 회 = 선행 연구 · 평탄) | **0 V** | −0.618 V vs In/InLi |

- **관계**: 0.31 V 는 **사다리 맨 위 칸**(약간 리튬화된 Au), 0 V 는 **맨 아래 칸**(AuLi₃ 를 넘겨 도금된 Li). 같은 금선의 다른 상이다 — 이 편은 150 nAh 를 넣고 **위 칸에 머물렀고**(리튬화 중에도 ≈0.2 V), 45호는 8 µAh 를 넣어 **아래 칸까지 내려갔다**.
- ★★★ **45호 digest 의 "21호 0.31 V 는 이 편 사다리(0 · 0.134 · 0.215 V)의 어느 칸도 아니다" 는 원전 사다리로 풀린다**: 원전의 첫 칸이 **0.311 V** 이고, 21호 노출부 `[재현]` x̄ ≈1.16(21호 digest)은 원전 창(0 < x < ∼1.2)의 **위 끝 안**이다. 45호가 AuLi(x = 1)을 칸 경계로 쓴 것과 원전(Bach) 이 준안정상 x ≈1.2 를 경계로 쓴 것이 다르다.
- ★★ **두 편이 같은 원전(Bach 2015 = 이 편 ref 25 = 45호 ref 33)에서 칸 값을 ≈0.08–0.1 V 다르게 옮긴다**(0.3 / 0.2 ↔ 0.215 / 0.134 V). 45호가 [20](이 편)을 134 / 215 mV 에 단 인용은 **이 지면에서 지지되지 않는다**(`134` · `215` 0 회, D6). `[해석]` 후보 둘 — (a) 215 mV 는 **전류 중** 값(이 편 리튬화 중 ≈0.2 V · 45호 전류 중 +0.21–0.25 V 와 같은 층), 개방회로 첫 칸은 ≈0.31 V (b) 칸이 셋 이상이고 두 편이 다른 두 칸을 골랐다. **Bach 2015 원전으로만 가른다.**
- ⚠ 16호 0.11 V 의 "한 칸(0.133) − 23 mV" 후보(45호)는 **칸 값 표가 두 개**라 이 편으로 강해지지도 약해지지도 않는다.

## (3) 21호 "교정 이식" — 원전 조건과 얼마나 다른가

| | **원전(이 편, 액체)** | **21호(ASSB 파우치)** | 차 |
|---|---|---|---|
| 전해질 · 압력 | LP57 · 스프링 T-셀(값 0) | 황화물 SE · Li\|Li 3 MPa / InLi 20 MPa | 계 전체 |
| 노출 | **단면만**(1.96 × 10⁻³ mm²) — `[인쇄]` 안정성의 일부를 이것에 돌림("minimizing side reactions") | 끝 0.5 mm 원통 벗김(0.0785 mm²) | **×40** — 원전이 안정성 근거로 든 조건을 벗어남 |
| 리튬화 | 150 nA × 1 h = 150 nAh · `[재현]` 7.6 mA cm⁻² | 500 nA × 6 h = 3 µAh · 0.64 mA cm⁻² | 전하 ×20 · 전류밀도 ×1/12 |
| 리튬화 중 전위 | ≈0.17–0.20 V(25 °C) | −0.8 → **≈−5 mV** | ASSB 는 과전압 ≥0.3 V — **도금 칸 문턱까지 내려갔다** `[해석]` |
| 전류 뒤 경로 | 0.318 → 0.311(**위에서**, 수백 h) | ≈0.25 V 30 분 → 0.31(**아래에서**) | 이완 방향이 반대 — 다른 과정 `[해석]` |
| 영점을 읽은 시각 | 0.311 = 장기값(≈150–550 h) | **리튬화 후 2 h** | 원전이 뺀 초기 창 **안** — 원전 곡선 2 h 값은 317.7 mV(장기값 +6–7 mV) |
| Li 대비 안정성 | > 500 h · `[도표]` 20 h 뒤 ≈3 mV | **2 h**(Li\|Li 셀) | 장기 Li 대비 명제는 **액체에만** |
| 이식 뒤 장기 표류 | — | InLi 두 전극 공통 모드 < 3 mV / 28 일 | 21호 **자기 측정**(원전 명제 안 씀) |

⇒ **판정**: 21호가 원전에서 가져간 것은 **값(0.31 V, 두 자리) 과 절차(Li 전극에서 리튬화 → 개방회로로 읽기)** 이지 **안정성 명제가 아니다** — 장기 안정성은 21호가 자기 셀의 공통 모드로 잰다. 그리고 21호는 원전이 영점 조건으로 인쇄한 넷 중 **둘(단면 노출 · 초기 창 제외)을 벗어났다.** 값은 두 자리에서 일치하므로(원전 2 h 값 0.318 도 "0.31" 에 반올림된다) **이식이 틀렸다는 증거는 없다** — 원전 조건이 ASSB 에서 **검사되지 않았다**는 것까지다.
⚠ 원장 표현 "21호가 **액체셀에서 잰 값**을 ASSB 로 옮겼다" 는 **정밀하지 않다**: 21호는 0.31 V 를 **ASSB Li\|Li 교정 셀에서 다시 쟀고**(2 h, "displayed as measured"), 교정 이식은 **ASSB 안(3 MPa Li\|Li → 20 MPa InLi)** 이다. 액체는 그 **값의 조상**이다.

## (4) "CE 거칠어짐" 가설 — 측정이 아니라 추론이다

- `[인쇄]` Li\|Li 셀, GWRE 를 **WE** 에서 리튬화. "both semicircles of the electrode used for the lithiation of the GWRE … are about 35 % smaller compared to the other electrode … **We believe** that this originates from the stripping of lithium from the WE electrode during lithiation of the GWRE, as this would cause a roughening of the lithium surface, leading to higher surface area and thus smaller impedance."
- **근거의 층위**: 관찰(호 −35 %) = 측정, 원인(거칠어짐) = **추론** — Li 표면 SEM · 대조군 · 반복 · 크기 점검 0, 셀 1 개. `hypothes*` 1(다른 곳) · `believ*` 2.
- `[재현]` 뺀 Li 150 nAh → 5.6 × 10⁻⁹ mol × 13.0 cm³ mol⁻¹ / 0.95 cm² = **≈0.77 nm 균일 두께**. 면적 ×1.6 을 균일 박리로 만들 수 없다 — 국소 핏팅이어야 한다(원문 무언급). 21호의 같은 계산은 3.6 nm.
- `[도표]` Fig. 2c: 고주파 호 폭 WE ≈81 ↔ CE ≈131 Ω(비 0.62) · 꼭짓점 −Im 31.5 ↔ 49.1(0.64) — "about 35 %" ↔ ≈37 %. **두 호 모두 1300 Hz · 1 Hz 마커가 두 전극의 꼭짓점에** 있다 ⇒ `[재현]` τ 보존 ⇒ `C` 비 ≈1.6 = **순수 면적 서명**(곱 축퇴 처방 1단계 τ 형) — 거칠어짐(면적)과 **양립**하되, **면적의 원인**(거칠어짐 ↔ 원판 간 표면 차)은 못 가른다.
- `[해석]` **두 편 두 셀에서 "리튬화한 쪽이 작다" 가 같은 방향**(이 편 ×0.62 · 21호 ×0.45) — 우연이면 1/4. 약한 반복이지 기구 증거는 아니다.

## (5) 3전극 EIS 아티팩트 — 이 편이 말하는 것과 45호 ">10 kHz 편차"

- **위치 아티팩트**(Ender 2012 · Dees 2007 인용): 가장자리 기준극은 기하 · 전기 비대칭에 민감 → **가운데 · 작은** 기준극으로 피한다. `[인쇄]` Dees: 100 µm 간격에 25 µm 기준극이면 충분. 이 편: ∅50 µm(+ 폴리이미드 7 µm) · 두 200 µm 유리섬유 사이. `[재현]` (64 µm)/(≈400 µm) ≈0.16 ↔ Dees 0.25.
- **위치의 검사**: Li\|Li 에서 `[인쇄]` "The high frequency resistance (see inset) is identical for both lithium electrodes, which indicates that the GWRE is located centrally" — **올바른 범주**(분배 대칭)의 검사. `[도표]` 인셋 두 곡선 Re ≈3.6 Ω 에서 겹침.
- ★★★ **표류 아티팩트 — 이 편의 본체**: 비리튬화 금선은 `[인쇄]` 30 s 에 **20 mV**(0.67 mV s⁻¹) 표류 → PEIS 에서 **≲1 Hz** 왜곡(흑연 유도 고리 · LFP 휨 · **완전지까지** 뾰족한 봉우리). 리튬화 금선은 0.3 mV / 30 s(0.01 mV s⁻¹)로 왜곡 없음. 기구 `[인쇄]`: WE–RE 전위 제어(PEIS)에서 RE 가 표류하면 WE 가 따라가 **WE–CE 에 편향 전류** → 비선형 · 시변. 처방: GEIS 또는 WE–CE 제어(Fig. 4b · c) — `[인쇄]` "artefacts of a non-stable RE will still be visible in the half cell impedance".
- **45호 ">10 kHz 편차" 판정**: 이 편이 주는 기준극 아티팩트 기구는 **저주파 끝(≲1 Hz, 표류)** 과 **기하(위치)** 둘이고, **고주파 쪽 기구는 0** 이다. ⇒ 45호 편차의 원인 후보를 **더하지 않는다**. `[해석]` 오히려 한 가지를 정련한다 — PEIS 에서 표류하는 RE 는 **완전지 스펙트럼까지** 오염시키므로 "합 일치" 검사는 표류 아티팩트가 있어도 반쪽과 전체가 **같이** 틀려 통과할 수 있다(45호 줄 "합 일치는 분배를 검증하지 않는다" 에 표류 판을 더함).
- ★★ **검증 셋의 범주**: ① 고주파 절편 대칭(위치) ② **재조립 대칭셀 대조**(분배 — 외부 기준) ③ **PEIS ↔ GEIS 일치**(표류 · 편향 전류). 각각 맞는 범주다 — `[인쇄]` "These results confirm that the presented cell setup … is **free of measurement artefacts**" 는 ③ 에 대해 과잉(③ 은 기하 아티팩트를 못 본다 — 기하 아티팩트는 두 제어 방식에 같이 든다). ② 가 기하를 보는 유일한 검사이고, 그 분해능은 셀 간 산포에 묶인다(D4 · D5).

---

# 서지

- **Solchenbach, S.; Pritzl, D.; Kong, E. J. Y.; Landesfeind, J.; Gasteiger, H. A.** "A Gold Micro-Reference Electrode for Impedance and Potential Measurements in Lithium Ion Batteries." *J. Electrochem. Soc.* **163** (10), A2265–A2272 (2016). DOI `10.1149/2.0581610jes`.
  접수 2016-06-07 · 수정 2016-07-26 · 게재 2016-08-19. Honolulu 학회 Paper 211 판. TUM 기술전기화학(Gasteiger) + Singapore Institute of Technology(Kong). BASF SE Battery Research Network 자금.
  CC BY 4.0 오픈액세스. 본문 8 쪽 + 표지 1 쪽(IOP 다운로드 표지, "You may also like" 에 같은 저자 후속 "A Novel Reference Electrode … Full-Cells" 와 **21호** 가 뜬다 — 인용 아님). 그림 8 · 참고문헌 53 · **SI 없음**.

# 셀 · 방법 (전부 `[인쇄]`)

| 항목 | 값 |
|---|---|
| 셀 | 3전극 Swagelok T-셀 — 기준 집전체 앞면에 ∅1 mm × 2.5 mm 구멍, 옆 나사로 선 고정 · 봉지 · 다른 부품은 원래 그대로 |
| GWRE | Au 선 ∅**50 µm** + 폴리이미드 **7 µm**(Goodfellow), ≈1.5 cm, 뒷끝 3 mm 긁어 접촉 · **절연을 벗기지 않음 — 전해액에 닿는 것은 절단면뿐** · 두 유리섬유 사이 가운데 |
| 분리막 · 전해액 | 유리섬유(Whatman) 2 장(각 200 µm) · 60 µL · LP57(1 M LiPF₆ EC:EMC 3:7 wt, H₂O < 10 ppm) · VC 0.17 / 0.52 wt% |
| 양극 | LFP : C65 : PVDF 93:3:4 · 11.7 mg cm⁻²(2.0 mAh cm⁻²) · ∅11 mm · **260 MPa 압연 → 공극 35 %** · 탄소 코팅 Al |
| 음극 | 흑연 T311 : PVDF 95:5 · 5.9 mg cm⁻²(2.2 mAh cm⁻²) · 공극 40 % · BET ≈5 m² g⁻¹(뒤 본문) · N/P ≈1.1 |
| Li\|Li | Li 원판 ∅11 mm × 450 µm(Rockwood) 두 장 |
| 리튬화 | 150 nA × 1 h, WE(LFP 또는 Li) ↔ GWRE, VMP300 · 10 µA 범위(정확도 0.1 % → ≈10 nA 오차) |
| 사이클 | 2–4 V CCCV(C/20 차단)/CC · 25 / 40 °C 항온조 |
| EIS | PEIS 5 mV(WE–RE 제어) 또는 GEIS 0.5 mA · 100 kHz–0.1 Hz · 50 % SOC · 25 / 10 °C · 측정 전 15 분 OCV |

# 결과 — 절별 해체

## §3-1 GWRE 전위 안정성 (Fig. 2a · b) — 위 판정 (1) 표

`[인쇄]` 형태 변화 없음(해체 후 육안) · 40 °C 표류의 해석(SEI 성장 → 자기 탈리튬 → 끝의 Li 고갈, Abraham 2004 Li-Sn 선과 일치) · 40 °C 리튬화의 안정화 기구 가설(고온 SEI 의 무기물 · 부피 변화 없는 기준극에는 유리) · `[인쇄]` "We further believe that the stable potential … is partly due to the fact that … the reference electrode area exposed to the electrolyte is limited to the cross-sectional area of the tip" · `[인쇄]` "The stable potential over 500 h indicates that the lithium diffusion along the wire (i.e., away from the tip) must be sufficiently slow to prevent a significant depletion of lithium at the tip."

`[재현]` **G1 긴장의 크기**: 150 nAh = 5.60 × 10⁻⁹ mol Li. 평균 x = 1.2 로 채우려면 Au 4.66 × 10⁻⁹ mol = 4.76 × 10⁻⁸ cm³(10.2 cm³ mol⁻¹) → 단면 1.96 × 10⁻⁵ cm² 에서 **깊이 ≈24 µm**. Li₃Au(x = 3)로 꽉 채워도 ≈9.7 µm(부피 팽창 무시). ⇒ 0.311 V 창(평균 x < 1.2)이 끝 전체에서 성립하려면 Li 는 **수십 µm 를 축 방향으로** 퍼져야 하고, 표면만 Li-풍부하면 개방회로는 더 낮은 칸이어야 한다. 원문은 "0.311 = x < 1.2" 와 "축 확산은 느리다" 를 **나란히 적고 대조하지 않는다.** (깊이 분포 측정 0 — 해석하지 않고 긴장만 적는다.)

`[도표]` Fig. 2a 범례는 두 25 °C 곡선을 같은 이름("Lithiation at 25 °C")으로, Fig. 2b 는 두 40 °C 곡선을 같은 이름("OCV at 40 °C")으로 적는다 — 리튬화 온도의 구분은 캡션에만(D9).

## §3-2 Li\|Li 임피던스 (Fig. 2c) — 위 판정 (4)

`[인쇄]` 고주파 반원 100 kHz–20 Hz(꼭짓점 ≈1.3 kHz) = SEI 저항, 저주파 20–0.1 Hz(꼭짓점 ≈1 Hz) = 전하이동(ref 36 Mogi 2002 인용).
`[재현]` C = 1/(2π f_apex R), 면적 0.95 cm²:

| 호 | R(`[도표]`) WE / CE | C WE / CE | 판정 |
|---|---|---|---|
| 1.3 kHz "SEI" | ≈81 / ≈131 Ω | **≈1.6 / ≈1.0 µF cm⁻²** | 막형으로 양립 |
| 1 Hz "charge transfer" | ≳16 / ≳25 Ω(0.1 Hz 에서 미폐) | **≈10 / ≈7 mF cm⁻²** | ❌ 이중층 ≈10 µF cm⁻² 의 **×700–1000** — 금속 박이라 거칠기로 못 채운다 |

⇒ **"전하이동" 이름표가 C 상한에서 다섯 번째로 실패**(19 · 20 · 21 · 43호에 이어; 계보 첫 **액체** 표본). `[해석]` 21호 Li\|Li 저주파 호(≳0.64 mF cm⁻²)와 같은 부류 — 확산 · 농도 결합 과정 후보. 판정은 R(미폐 호 하한) · 이상 RC 가정 위.

## §3-3 비리튬화 ↔ 리튬화 (Fig. 3 · 4) — 위 판정 (5)

`[도표]` Fig. 3a: LFP vs 비리튬화 금선 0.748 → 0.769 V(30 s) · vs 리튬화 금선 **≈3.108 V**(두 번째 축) → `[재현]` +0.311 = **3.419 V vs Li**(50 % SOC 개방회로) · `[재현]` 비리튬화 Au ≈**2.67 V vs Li**, 음의 방향으로 표류.
`[인쇄]` 리튬화에 쓴 150 nAh 는 LFP 1.95 mAh 대비 "negligible" — `[재현]` 1/13,000.
`[도표]` Fig. 3c 고주파 절편 흑연 ≈3.0 · LFP ≈4.0 · 완전지 ≈7.0 Ω(합 일치) · 흑연 호 ≈3.0 → 7.2 Ω.
`[인쇄]` HFR 차 ≈1 Ω = LFP 코팅–집전체 접촉 저항(자기 측정 "data not shown", ≈1 Ω cm²) · LFP 전하이동 호 "small and almost invisible" · 흑연 호 = SEI + 전하이동(사이클 전에는 없음).

## §3-4 검증 (Fig. 5)

`[인쇄]` "Apart from a slight shift in HFR, the impedance response of the symmetric cells and the full-cell with the lithiated GWRE are essentially identical" · HFR 차는 대칭셀 유리섬유 압축이 약해서(추정, "probably") · Dahn 대칭셀의 고주파 접촉 특징은 단면 코팅이라 없음 · PEIS ↔ GEIS `[인쇄]` "completely identical".
`[도표]` 화소 판독(69.75 px/Ω): **흑연** GWRE 완전지 HFR ≈3.05 · 호 끝 ≈7.15(폭 ≈4.1 Ω) · 꼭짓점 −Im **1.30** ↔ 대칭셀/2 HFR ≈4.45 · 호 끝 ≈8.2(폭 ≈3.75) · 꼭짓점 **1.03** ⇒ 폭 −9 % · 높이 −21 % · HFR 차 ≈1.4 Ω(D4). **LFP** 두 곡선은 ≈0.55 Ω 평행 이동에 가깝다.
`[도표]` **Fig. 5c 의 흑연(PEIS 선 · GEIS 점)은 HFR ≈3.06 · 호 끝 ≈5.66(폭 ≈2.6 Ω) · 꼭짓점 0.80** — 같은 캡션 상태(1 형성 사이클 · 50 % SOC · 25 °C)의 Fig. 3c · 5a 흑연(폭 ≈4.1)과 **×0.63**(D5). 셀 동일성 미인쇄 — 다른 셀이면 **셀 간 ×1.6 > 검증 차 −9 %**.

## §3-5 200 사이클 (Fig. 6)

`[인쇄]` 1C · 25 °C · 형성 C/10 두 번 · EIS 는 5 · 10 · 이후 10 사이클마다 · 전위를 GWRE 축(왼쪽) + **0.311 V 를 더한 Li 축(오른쪽)** 으로 병기 — P11 "측정 축 병기" 의 **이른 표본**.
`[인쇄]` 과전압 불변 · 흑연 방전 끝 최대 전위 ↑ · LFP 방전 끝 최소 전위 ↑ → "the SOC of both electrodes slip against each other" · 두 전극 HFR +0.1–0.2 Ω(접촉 박리 또는 전해질 저항, 가르지 않음) · 흑연 호 ∼1.9 → ∼2.2 Ω · "can be related to the loss of active lithium due to a slow but steady SEI growth" · 결론 `[인쇄]` "we could identify lithium inventory loss due to SEI growth as the dominant aging mechanism".
`[도표]` 방전 용량 ≈129(10) → ≈121(200) mAh g⁻¹_LFP(−≈6 %) · 흑연 방전 끝 ≈+0.15(10) → ≈+0.87 V vs GWRE(200) · LFP 방전 끝 ≈2.15 → ≈3.0 V vs GWRE ⇒ **방전 끝이 양극 쪽에서 음극 쪽으로 넘어간다**(`[해석]` 교과서 `LLI` 서명).
`[해석]` **라벨 층위**: 전극별 끝점 이동 = **측정**(3전극), "`LLI` 지배" = **해석**(정량 0 · `LAM` 과 가르는 분해 0 · 셀 1 개). 우리 α·β 가 완전지 곡선에서 풀려는 것이 **여기서는 측정으로 갈려 있다** — 액체셀 · 양 전극 · 정량 안 함.

## §3-6 VC 량 (Fig. 7 · 8) — 우리 축 밖, 짧게

`[인쇄]` 전해액/용량 비 38 ↔ Burns 3.3 g Ah⁻¹(×11.6) → VC 0.17 / 0.52 % = Burns 2 / 6 %(0.06 / 0.2 g_VC Ah⁻¹) · 형성 40 °C · EIS 10 °C · 등가회로 R–(R‖CPE)–W(Illig 2012 = **큐 52** 단순화) · 흑연 `R_CT` ∼5 → ∼16 → ∼47 Ω cm² · LFP 불변(El Ouatani: LFP 에는 poly(VC) 막 없음) · 결론 "the ratio of mass VC to active material, rather than the VC concentration, is the key parameter".
`[도표]` Fig. 7 조건당 셀 **2 개**: 0.17 % 두 흑연 호 ≈11 ↔ ≈22 Ω(×2) · 0.52 % ≈46 ↔ ≈55 Ω. Fig. 8 오차 막대(정의 미인쇄, n = 2) — 0.17 % ≈16.8 (10.5–23) · 0.52 % ≈49.5 ↔ 본문 ∼47(D8).
`[재현]` **면적 규격화의 크기 점검**: 이 편 흑연 5.9 mg cm⁻² × 5 m² g⁻¹ = **295 cm² cm⁻²** · Burns 추정 10 × 0.7 = **70** ⇒ 거칠기 비 **≈4.2**(`[인쇄]` "∼5-fold", D7). Burns/이 편 `R_CT` 비는 VC 세 점에서 **6.0 · 3.75 · 3.2**(×1.9 퍼짐) — 면적 하나로는 세 점이 안 닫힌다(저자가 인쇄한 단서 "A different BET … would also affect the amount of additive per unit surface" 와 같은 방향). 저자는 오른쪽 · 위 축에 **BET 규격화 `R_CT` · VC/m²** 를 병기했다 — 곱 `R·A` 를 축으로 올린 사례.

---

# 곱 축퇴 처방 — 서른 번째 적용 (액체 · 도구 칸)

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C`(τ 형) | Fig. 2c 두 호 모두 두 전극의 꼭짓점 주파수 동일(1.3 kHz · 1 Hz 마커) | ✅ **면적 서명**(`C` 비 ≈1.6) — 저자 "거칠어짐" 과 양립, 면적의 원인은 못 가름 |
| **2단계** 면적 대조군 | 흑연 BET 5 m² g⁻¹ + 로딩(자기) ↔ Burns 추정(**다른 연구실 논문에서 가져온 값**) | ⚠ **외부 기준 다섯 번째 배정 — 연구 간 R 차를 추정 면적에**: `[재현]` 비 4.2 ↔ `R_CT` 비 3.2–6.0 |
| **3단계-a** `Ea` | 25 · 10 °C 측정이 다른 셀 · 다른 절 | ❌ |
| **3단계-b** `C` 상한 | Li\|Li 두 호 | ✅ "SEI" ≈1–1.6 µF cm⁻² 양립 · **"charge transfer" ≈7–10 mF cm⁻² ×700–1000 실패** |
| **4단계** 시간 영역 | Fig. 6 "overpotentials … do not change" — 수 0 | ❌ |

`[해석]` 액체 · Li 금속 · 흑연이라 카드의 곱(`A_eff·ε_p/R_s`)은 대상이 없다. 기여는 둘 — ① **"전하이동" 이름표 C 상한 실패의 액체 표본**(ASSB 고유 현상이 아니라는 대조) ② **외부 기준 줄의 다섯 번째 배정**: 연구 간 비교에서 면적을 **남의 논문 추정치로** 고정하고 R 차를 면적에 돌리는 형태 — 저자가 "only an estimate" 로 고지했고, 세 점의 비가 ×1.9 퍼져 단일 면적 인자로 닫히지 않는다.

# 칸별 요약 (채움표 행)

| 칸 | 판정 |
|---|---|
| Q1 정량 | **없다 — `θ(N)` 0/47.** 액체 · 접촉 손실 대상 없음. `contact` 6 = 집전체 · 셀 하우징 접촉 저항 |
| Q2 독립관측 | **해당 없음(액체)** — 도구 칸: 전극별 끝점 이동(3전극)으로 `LLI` 서명을 **측정**, 정량 · `LAM` 대조 0. 기준극 검증 셋(위치 · 외부 분배 · 표류)을 범주별로 배치 |
| Q3 라벨층위 | 층 하나 — **external-partition-validated**(재조립 대칭셀 대조, 셀 간 산포 기준 없음) + **undefined n = 2 error bars**(Fig. 8) · 등가회로 적합 `R_CT` 불확실성 0 |
| Q4 유일성 | **0/47 — 서른아홉 번째 성질 "검사마다 맞는 범주를 골랐고(위치 = 고주파 절편 대칭 · 분배 = 대칭셀 · 표류 = PEIS↔GEIS), 판정의 분해능(같은 지면의 셀 간 산포)을 대지 않았다"**. `identifiab` · `uncertaint` · `Kramers` 0 |
| Q5 Li-In | **이동 없음(반 칸 검토 후 접음)** — 스물세 번째 형태(위). 누설 0/47 |
| Q6 압력 | 해당 없음 — 액체 T-셀 스프링(값 0) · `MPa` 1 = 전극 압연 |
| Q7 dead Li | 해당 없음 |
| Q8 화학 · OCP | 해당 없음(액체 LFP/흑연) — 칸 밖: LFP 평탄 3.11 V vs GWRE → 3.42 V vs Li |

---

# 어긋남 (D)

| # | 인쇄 | 그림 · 계산 | 성질 |
|---|---|---|---|
| **D1** | "varying by less than 2 mV after the initial 20 h" | `[도표]` 21 h 314.3 → 300 h 311.3 mV(≈3.0 mV) · < 2 mV 는 ≈50 h 뒤부터 | 초기 창 길이 과소 |
| **D2** | "shoots up to 0.318 V and then quickly relaxes to ∼0.311 V" | `[도표]` 100 h ≈312.0 · 0.311 도달 ≈150–250 h | "quickly" ↔ 수백 시간 |
| D3 | 초록 곡선(40 °C 리튬화) "same stability … shifted downwards by 1–2 mV" | `[도표]` 장기 308.8–309.7 ↔ 311.3–311.8 → −2.0 ± 0.5 mV | 일치(기록) |
| **D4** | 대칭셀 대조 "essentially identical" apart from "slight shift in HFR" | `[도표]` 흑연 호 폭 −9 % · 꼭짓점 −21 % · HFR 차 ≈1.4 Ω(HFR 의 ≈45 %) | "slight" · "identical" 과장 |
| **D5** | Fig. 5c "the same LFP/graphite full-cell" | `[도표]` 흑연 호 ≈2.6 Ω ↔ 같은 상태 Fig. 3c · 5a ≈4.1 Ω(×0.63) | 셀 동일성 미인쇄 · 산포 기준 부재 |
| **D6** | (45호) "E(AuLi/AuLi₃) = 134 mV and E(Au/AuLi) = 215 mV … [20,33–35]" | 이 편: `134` · `215` 0 회, "∼0.3 V · ∼0.2 V"(ref 25) · 상 이름은 열역학 상에 배정 불가 | **교차 편 인용 불일치** |
| **D7** | "∼5-fold higher roughness factor" | `[재현]` 295 / 70 = **4.2** | 저자 자기 수로 ×0.84 |
| D8 | 흑연 `R_CT` 0.52 % "∼47 Ω cm²" | `[도표]` Fig. 8 ≈49.5 | 소 |
| D9 | Fig. 2a · 2b 범례 | 같은 이름 두 곡선씩(리튬화 온도 구분은 캡션만) | 표기 |
| D10 | "35 % smaller" | `[도표]` 고주파 호 폭 0.62 · 높이 0.64(≈37 %) | 일치(기록) |
| **D11** | "0.311 V … LixAu 0 < x < ∼1.2" + "lithium diffusion along the wire … sufficiently slow" | `[재현]` x ≤ 1.2 에는 ≥ ≈24 µm 축 확산 필요 | 두 문장의 크기 긴장(G1) |
| D12 | "stable for several weeks" | 가장 긴 추적 ≈550 h(≈3.3 주) | 일치(기록) |

# 낱말 지문

규칙: NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문(참고문헌 전; 표지 쪽 제외). SI 없음.
NFKC 변경 본문 **81 자**(`ﬁ` 69 · `ﬂ` 7 · `´` 3 · `¨` 2) — 열 변화 0. 소프트 하이픈 0 · 줄끝 하이픈 **92 곳**(이으면 `stab*` 24 → 25 · `electrolyte` 39 → 42 · `symmetric` 21 → 22 · `surface area` 8 → 9 — 지문 열 변화 0).

| `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | **1**(전극 압연 260) |

Q5 보조: `leak` **0** · `drift` **11** · `assum*` 2(둘 다 VC 절 — 기준 전위 아님) · `0.311` **6** · `0.31` 1(서론 "around 0.31 V") · `re-?lithi*` 3 · `stab*` 24 · `stable` 16 · `week` 3 · `deplet*` 2 · `rough*` 4 · `believ*` 2 · `hypothes*` 1 · `0 V` 1("below 0 V", 리튬화 순간) · `plat*` 7(도금 Li 기준극 0 — 선행 연구 · 평탄) · `Li3Au` 4 · `LixAu` 1.
EIS 보조: `artefact` **7**(영국식; `artifact` 0) · `symmetric` 21 · `Kramers` 0 · `capacitan*` 0 · `fit*` 4 · `error` 1(전류 정확도) · `reproduc*` 2(Burns 재현) · `cell to cell` 1 · `n =` 0 · `pressure` **0** · `solid` 5(고체 확산 · 선 종류).
`[해석]` **기준 전위 어휘가 계보에서 가장 짙은데 `calibrat` · `assum*`(기준 전위) 은 0** 이다 — 영점이 가정이 아니라 **측정**이라 가정의 낱말이 필요 없다(42호 Santhosha 와 같은 부류 — 가정의 원전). 대신 **`drift` 11** — 계보 첫 두 자릿수.

---

# 그림 — 본 것 / 안 본 것

크로퍼 8 장(`wiki/raw/figures/solchenbach2016_gold-wire-micro-reference-electrode-liquid-t-cell/`) — **8 장 다 봤다**(Fig. 1–8).
화소 판독(원본 래스터에서): **Fig. 2b**(0.1415 mV/px — 세 곡선 시계열) · **Fig. 2c**(3.51 px/Ω — 호 폭 · 꼭짓점) · **Fig. 5**(69.75 px/Ω — 흑연 호 세 곡선) · **Fig. 6a**(6.5 mV/px — LFP 평탄 띠). 나머지(Fig. 1 모식도 + SEM · 3 · 4 도식 · 7 · 8)는 눈 판독.
본문과 어긋난 그림: Fig. 2b(D1 · D2) · Fig. 5a · c(D4 · D5) · Fig. 8(D8, 소).
Fig. 1c SEM `[도표]`: 절단면 폴리이미드 가장자리 오른쪽이 들뜨고 조각져 보인다 — `[인쇄]` "almost completely intact" 와 양립(“almost”).

# 계보에서의 자리

`[해석]` … → 셀 안 도금 Li · 소모품 기준극(45호) → 영점이 들어가지 않는 자리(46호) → **원전 측정: Li 대비 장기 추적 + 영점의 사용 조건, 액체(47호)**.
- 두 관례의 공통 조상 판정: **0.31 V 관례(21호)의 조상 ✅**(같은 연구실 · 같은 선 · 같은 절차, 21호 ref 11) · **0 V 관례(45호)의 조상 ⚠ 하드웨어 선례만** — 이 편에는 도금 칸 · 0 V 문장이 없고, 45호가 이 편에 단 134 / 215 mV 도 지면에 없다. 0 V 는 Hertle 자신의 것이다(45호).
- 21호 교정 이식: 뿌리 ✅, 이식된 것 = 값 + 절차, 원전 조건 넷 중 둘 이탈(단면 노출 · 초기 창), 장기 안정성은 21호 자기 측정.

# 후속 (서지 기준, 미열람)

| 서지 | ref | 왜 |
|---|---|---|
| **Bach, Stratmann, Valencia-Jaime, Romero, Renner 2015 *Electrochim. Acta* 164, 81** | 25 | ★★★ 0.31 / 0.2 V(이 편) ↔ 0.215 / 0.134 V(45호) 를 **같은 원전**에서 다르게 옮겼다 — 개방회로 칸 값 · x 경계 판정 |
| Bach, Valencia-Jaime, Rütt, Gutowski, Romero, Renner 2016 *Chem. Mater.* 28, 2941 | 30 | 준안정상(Li₃Au₂ · Li₅Au₃ · Li₃Au₅ · LiAu₂) — AuLi / AuLi₃ 명명과 대조 |
| Ender, Weber, Ivers-Tiffée 2012 *JES* 159, A128 | 14 | 기준극 위치 아티팩트(기하 · 전기 비대칭) 원전 — 45호 >10 kHz 판정 재료 |
| Dees, Jansen, Abraham 2007 *JPS* 174, 1001 | 15 | 미세 기준극 크기/간격 조건(25 µm / 100 µm) |
| Victoria, Ramanathan 2011 *Electrochim. Acta* 56, 2606 | 17 | 선형 표류 0.1 mV s⁻¹ → 1–0.1 Hz 아티팩트 모사 — 표류 문턱 |
| Illig … Ivers-Tiffée 2012 *JES* 159, A952 | 35 | **큐 52** — LFP 등가회로 · Li 금속 호 배정 |
| Abraham … Dees 2004 *Electrochim. Acta* 49, 4763 | 6 | 리튬화 Sn 선 — 고온 불안정 · 재리튬화 선례 |
| Pritzl, Solchenbach, Gasteiger (in prep.) | 33 | 고전압(>4.7 V) 수명 · 재리튬화 — 후속 출판본 확인 |

큐 49–59 인용: **52(Illig 2012) 하나**(2016 논문이라 49–51 · 53–59 는 시간상 불가 또는 무관).

# 이 digest 가 주장하지 않는 것

- **0.311 V 가 ASSB 에서 틀렸다고 하지 않는다** — 21호의 ASSB Li\|Li 값 "0.31"(2 h)과 두 자리에서 맞는다. 주장은 **원전 조건 넷 중 둘이 21호에서 검사되지 않았다**는 것까지다.
- **D1 의 ≈3 mV 를 원전 표류 크기로 확정하지 않는다** — 셀 1 개 · 래스터 판독(±0.3 mV) · 20 h 기준점 선택에 걸린다.
- **누설 < 0.27 nA 는 측정이 아니라 상한**이고, 40 °C ≈2.5 nA 는 **"전량 소진" 해석** 위의 크기다.
- **"거칠어짐이 아니다" 라고 하지 않는다** — 0.77 nm 균일 두께는 균일 박리를 기각할 뿐, 국소 핏팅은 남는다.
- **45호 134 / 215 mV 가 틀렸다고 하지 않는다** — [20] 인용이 이 지면에서 지지되지 않는다는 것까지이고, 값 자체는 refs 33–35(Bach 등)에 있을 수 있다.
- **Fig. 5c 가 다른 셀이라고 단정하지 않는다** — 지면이 말하지 않는다.
