# Pre-conditioning Strategy for Highly Reversible Anode-Less ZIBs — 도경록(Kyungrok Do), 한양대 BML 주간 세미나 (2026-09-02)

> slug `do2026_bml_alzib_preconditioning` · type `talk` (**랩 내부 주간 연구세미나 덱**) ·
> **axis: `zn-aqueous`** (⛔ 우리 황화물 SE 물성 4축 아님 — 아래 §11 축 분리 규율) ·
> 발표 **2026-09-02**, BML Research Seminar / Weekly Report @BML (한양대 Battery Materials Laboratory) ·
> 발표자 **Kyungrok Do (도경록)**, Division of Materials Science & Engineering, Hanyang University ·
> krd0318@hanyang.ac.kr ·
> 원본 덱 `794a02af-2026.09.02 …….pdf` (PowerPoint→PDF, **30쪽 = 슬라이드 30장**, 720×540 pt,
> sha256 `3b9546ad…c022ff693`) · digested **2026-09-03** · status ✅ (텍스트 30/30 · 래스터 그림 5장/패널 13개 판독)
>
> **⛔ DOI 없음 · 저널 없음 · peer-review 없음.** 이건 **논문이 아니라 주간 발표자료**다.
> 원고·SI·외부 발표에 이 수치를 인용하면 안 된다 (미출판·진행 중 연구, `talks/README.md` 인용 규율).
> `> elements:` **(none)** · `> methods:` **(none)** — 계산이 **0건**이다(전량 실험 덱).
> 원소·기법 태그를 붙이면 webapp 의 주기율표/용어집이 우리 황화물 축과 섞인다.
> (webapp 자동링크는 `litdb/papers/` 만 훑으므로 `talks/` 에 두는 것만으로 오염이 차단된다.)
>
> 🧭 **우리 기여 스코핑은 여기 다시 쓰지 않는다** → `kb/projects/zn_alzib_dft_md_contribution_2026_09_03.md`
> (계산 후보 C1–C7 · 착수 게이트 · "DFT/MD 가 답할 수 없는 것"). 이 digest 는 **덱 자체의 기록**이고,
> 그 카드가 **우리가 뭘 할지의 정본**이다. 중복 서술 금지.

---

## 0. ⚠ 파일 혼선 기록 (2026-09-03, 먼저 읽을 것)

같은 날짜 이름의 PDF **두 개**가 업로드됐고 처음엔 "내용 동일"로 안내됐지만, **서로 다른 발표**였다.
(digest 작업 중 구조 파싱으로 독립 발견 → 이후 조정자가 같은 내용으로 정정 확인.)

| 업로드 | md5 | 쪽 | 실제 내용 |
|---|---|---|---|
| **`794a02af-2026.09.02…pdf`** | `12fa7c66…` | **30** | ✅ **이 digest** — Kyungrok Do, Zn–I₂ ALZIB pre-conditioning |
| `3e8c3616-2026.09.02…pdf` | `e2035697…` | 38 | ❌ **다른 발표** — Jae Hyun Park, "Argyrodite electrolyte for ASSLMB" (Nd/O 공치환 LPSCl₁.₆). Zn 과 무관, **이 작업 대상 아님**. digest 미작성 |

### 판독 경로 (재현용)
- **정본 텍스트 = `sem794.txt`** (pdfminer, 30장 20,771자, 폰트 인코딩 정상).
- 보조 = `sem_clean.txt` (stdlib 스캐너). **글자가 깨져 있다**(`ZnI₂→ŶI2`, `→→ї`, `µm→ȝP`) —
  단독 인용 금지. 다만 **커버리지가 달라** 한쪽에만 있는 문장이 있으므로 **합집합으로** 확인했다.
- 추가 검증 = PDF 페이지 객체를 직접 파싱해 **텍스트 x/y 좌표**로 "어느 값이 어느 시료/패널의 것인지"를
  대조했다(§5.9·§6.6·§7b 의 배정이 그 결과다). 좌표 대조한 항목은 본문에 **"좌표 대조"** 로 표시.
- 이 digest 의 모든 수치는 **`sem794.txt` 로 재대조 완료**(2026-09-03).

---

## 1. 한 줄 요약

**"무음극 Zn–I₂ 셀에서 Cu 집전체를 미리 길들인다"** — 10 mA cm⁻² · 0.1 mAh cm⁻² 라는
**고전류·초저용량** 조건으로 **~500 사이클** 예비 순환(pre-conditioning)을 돌리면, Cu 표면에
**in-situ 로 zincophilic + 부식억제 이중기능 층**이 생기고, 그 뒤의 Zn 도금/탈리 가역성이
**Aurbach 평균 CE 77.8 % → 98.1 %** (0.5 mAh, ZnSO₄) 수준으로 뛴다.

핵심 논리 한 줄: **"용량이 아니라 사이클 수가 가역성을 결정한다"**
(Reversibility depends primarily on **cycle number** rather than deposition capacity — 슬 7).

**우리와의 관계**: 물질계가 **수계 Zn²⁺ / Cu 집전체 / Zn 금속 전착**이라 우리 황화물 Li⁺ SE 축과
**수치로 겹치는 것이 0** 이다. 겹치는 것은 **질문의 구조**뿐 — "계면에 in-situ 로 생긴 층이 무엇이고,
왜 수송을 돕고 부작용을 막는가". 그 층의 **상 동정**과 **표면 결합 서술자**가 우리가 낼 수 있는 칸이다.

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 발표자 | **Kyungrok Do (도경록)** — 한양대 Division of Materials Science & Engineering, BML |
| 자료 성격 | **Weekly Report @BML** 주간 연구세미나 덱 (30 슬라이드) |
| 날짜 | 2026-09-02 |
| DOI / 저널 | **없음** (논문 아님 — 지어내지 말 것) |
| 계 | **무음극(anode-less) 수계 Zn–I₂ 전지 (ALZIB)** |
| 전해질 | **2 M ZnSO₄**, 그리고 **2 M ZnSO₄ + 0.2 M ZnI₂** |
| 셀 구성 | 하프셀 **Zn‖Cu**, 풀셀 **Cu‖AC**(활성탄 I₂ host 로 보이나 덱에 명시 없음 — n/a) |
| 연구유형 | **전량 실험**. 계산(DFT/MD) **0건** |
| 슬라이드 표기 | 덱의 슬라이드 번호 = PDF 쪽 번호 (1쪽 표지, 29 Thank you, 30 appendix) |

---

## 3. 계와 문제 정의 (슬 2–5)

### 3.1 왜 무음극인가 (슬 2)
- ALZIB 는 **금속 Zn 음극의 무게·부피를 최소화**해 에너지밀도를 올린다.
- **N/P ≈ 1** (일반 AZIB 는 **~50**) → Zn 공급이 유한하고, 그 유한량이 **셀 수명을 직접 결정**한다.
- 따라서 셀 성능 = **Cu 집전체 위 Zn plating/stripping 가역성**.
- 인용: Nano-Micro Lett. **2022, 14, 208** / Adv. Funct. Mater. **2026, 36, e23442**.

### 3.2 bare Cu 의 실패 기전 두 갈래
**(a) 불균일 핵생성 (슬 3)** — Cu 는 **결정립계 · step edge · rolling mark** 때문에 표면이 불균일하고,
Zn 핵생성이 **소수의 자리에 국한**된다 → 국소 전류밀도 집중 → **덴드라이트** → 비가역 용량 손실.
(광학/SEM 스케일바 20 µm)

**(b) 기생 부반응 (슬 4)** — HER · 부식 · 부동태화가 **커플링**되어 각각 CE 를 갉아먹는다.
전해질에 노출된 Cu 가 도금된 Zn 과 **갈바닉 커플**을 이뤄 도금 Zn 위 HER·전기화학적 부식을 가속한다.
슬라이드 도식(EES **2025, 18, 10180** 레이아웃 개변 + Nat. Commun. **2026, 17, 7363**)의 4갈래:
`HER(H₂O→H₂, 전자 경쟁 → Faradaic efficiency↓)` · `ZHS 표면 부동태(Zn²⁺ 수송 차단 → 활성계면↓)` ·
`부식(Zn → Zn²⁺ + 2e⁻, 활성 Zn 소모 → 용량↓)`.
⇒ **"이 갈바닉 부식을 죽이는 것이 Cu 집전체의 핵심 요구조건"** 이 이 발표의 전제.

### 3.3 제안 (슬 5)
반복 Zn plating/stripping 으로 Cu 위에 **전기화학적으로 유도된 zincophilic interphase** 를 만든다.
그 층이 ① **치밀·평면 Zn 전착을 유도**하고 ② **부식에 의한 Zn 손실을 억제**한다 (= **이중기능**).
여기에 **ZnI₂ 를 전해질 첨가제**로 넣으면 pre-conditioning 유래 가역성이 더 좋아진다.

### 3.4 선행연구와 그 한계 (슬 6)
'Pre-Coverage of Side Reaction Sites Enables Quasi-Anode-Free Rechargeable Aqueous Zinc Batteries'
(**Adv. Funct. Mater. 2026, 36, e23442**):
- 탄소 기판에서는 pre-Zn-plating/stripping 처리로 **HER 자리에 ZHS**(Zinc Hydroxide Sulfate)가 덮인다.
- **Cu 기판에서는 ZHS 보다 표면 합금층 형성의 영향이 더 컸다.**
- ⚠ 그런데 **그 Cu-specific 기전은 언급만 되고 체계적으로 조사되지 않았다** → Cu 최적 프로토콜이 공백.
  ⇒ **이 발표의 출발점이 바로 그 공백**이다.

---

## 4. Pre-conditioning 프로토콜 (슬 7–9) — 이 덱의 핵심 조작변수

### 4.1 프로토콜 스크리닝 (슬 7, `Fig. 7`)
Zn‖Cu 하프셀(2 M ZnSO₄)에서 두 축을 나눠 훑었다.

| 축 | 시험한 조건 | 결론 (발표자 문장) |
|---|---|---|
| **전류밀도** | 1 · 5 · **10** · 20 · 40 mA cm⁻² (1 mAh cm⁻² 고정) | "A current density of **10 mA cm⁻²** yields the most stable Zn plating/stripping" |
| **용량 vs 사이클수** | 5 mA cm⁻²·1 mAh cm⁻² / 10 mA cm⁻²·0.5 mAh cm⁻²·100 cyc / 10 mA cm⁻²·0.1 mAh cm⁻²·100 cyc / **10 mA cm⁻²·0.1 mAh cm⁻²·500 cyc** | "Reversibility depends primarily on **cycle number** rather than deposition capacity" |
| **수렴점** | 재조립 후 Zn‖P.C. Cu 셀로 확인 | "CE converges after **~500** pre-conditioning cycles" |

⇒ **확정 프로토콜 = 10 mA cm⁻² · 0.1 mAh cm⁻² · 500 cycle** (이후 모든 "pre-conditioned Cu" 가 이것).

> ⚠ **덱 오타 1건**: 슬 7 본문의 `(in 10 mAh cm⁻², 0.1 mAh cm⁻² protocol)` 는 앞이 **10 mA cm⁻²** 여야
> 맞다(같은 슬라이드의 다른 라벨과 §4.1 표가 전부 10 mA cm⁻²). 인용할 때 그대로 복사하지 말 것.

차트 축(텍스트 레이어 눈금, 패널 3개): ① CE **99.6–100.0 %** / 사이클 0–2000 ·
② CE **97–100 %** / 사이클 0–800 · ③ CE **97–100 %** / 사이클 0–300.

### 4.2 표면 진화 (슬 8, `Fig. 8`)
- **고전류 + 저용량**으로 돌리는 이유 = **핵생성을 반복시키기 위해서**
  ("Zn is cycled at a **low capacity with high current density** to induce **repeated nucleation**").
- 사이클이 진행되며 **Zn 전착 과전압이 감소**하고 **가역성이 증가**한다.
- **육안으로 Cu 표면 색이 구리색 → 은색으로 바뀐다** (20 / 50 / 200 / 500 cycle 사진).
- 차트 축: CE **92–100 %**, 과전압 **−0.10–0 V**, 사이클 **0–500**.

### 4.3 ZnI₂ 첨가 효과 (슬 9, `Fig. 9`)
- 풀셀이 0.2 M ZnI₂ 로 돌기 때문에 pre-conditioning 에 대한 ZnI₂ 효과도 봤다.
- ZnI₂ 를 넣으면 **Zn 전착 과전압이 더 낮아지고 수렴이 빨라진다** → "faster surface coverage".
- 축은 슬 8 과 동일.

### 4.4 요오드가 왜 도움이 되는가 — **인용 근거(본인 검증 아님)** (슬 10)
- I₃⁻ 첨가제가 상용 Cu foil 에 **표면 재구성**을 일으키고, in-situ 로 생긴 **zincophilic Cu 나노클러스터**가
  초저과전압·균일 전착·우수한 가역성을 준다 — **Nano-Micro Lett. 2022, 14, 208**.
- **I⁻-rich EDL 이 Zn 이온의 Marcus charge-transfer 에너지 장벽을 낮춰** 핵생성 과전압을 낮춘다 —
  **Energy Environ. Sci. 2024, 17(19), 7372–7381**.
- I⁻ 가 **Zn(002) 우세 배향** 도금을 촉진한다.
> ⚠ 이 슬라이드는 **전부 문헌 인용**이다. 발표자 본인의 측정/계산이 아니다 (§7 G5).

---

## 5. 결과 — 슬라이드별 (슬 11–22, 하프셀)

### 5.1 표면 형상 (슬 11, `Fig. 11`)
- bare Cu: rolling mark · step edge → **불균일 핵생성 자리**.
- 두 전해질 모두 pre-conditioning 후 **나노스케일 Zn 이 치밀하게 깔린 층**이 생긴다. (스케일바 30 µm / 2 µm)
- ⚠ 발표자 스스로: *"Further analysis is required to determine whether the deposited layer provides a
  high density of nucleation sites **and** limits direct Cu–electrolyte contact"* (§7 G3).

### 5.2 상 조성 — **여기가 제일 큰 구멍** (슬 12, `Fig. 12`)
- **Cu 반사가 지배**한다: 층 두께 **~2–4 µm** ≪ XRD 침투깊이 **~30–40 µm**.
- 잡힌 피크: Cu(111)/Zn(101) 중첩 · Cu(200) · Cu(220) · Cu(311). 참조 패턴으로 **Cu · CuI · Zn** 표시.
- ⚠ **"The reflection near 43° cannot be unambiguously assigned to Zn owing to overlap with Cu"**
- ⚠ **"Further surface-sensitive characterization (GI-XRD, XPS depth profiling) is required to identify
  the layer composition"** (§7 G1) — **층이 무엇인지 아직 모른다**는 뜻이다.
- 차트 축: 2θ **20–100°**.
- ★ **우리 계산이 여기에 답을 냈다 → §11.2b**: 43° 는 원리적으로 못 가른다(8상 1.469° 폭,
  Cu(111)↔Zn(101) **0.097°**). 진단창은 **31–39°** (Cu 반사 0개).

### 5.3 Zn 전착 형상 (슬 13, `Fig. 13`)
- bare Cu: **두 전해질 모두** 국소적·덴드라이트형 전착.
- pre-conditioned Cu: **평면·치밀** 전착.
- **ZnI₂ 첨가 시 기판과 평행하게 정렬된 육각 판상(hexagonal flakes)** → 치밀 Zn 층 형성 시사 (§7 G7).
- 조건: 0.1 mAh Zn 전착 후, 스케일바 2 / 4 µm.

### 5.4 전기화학 분석 (슬 14, `Fig. 14`)
- ZnI₂ + pre-conditioning 이 **상승작용**으로 핵생성 과전압과 계면저항을 함께 낮춘다.
- 같은 과전압에서 전류가 크다 = **전하이동 속도론이 빠르다**.
- 차트 축(텍스트 레이어 눈금, ⚠ 데이터 판독 아님): bare 쪽 Nyquist 축 **0–120 Ω cm²**,
  pre-conditioned 쪽 축 **0–8 Ω cm²** → 축 스케일만으로도 **한 자릿수 이상 차이**를 시사한다.
  (정확한 R 값은 덱 본문에 숫자로 안 나온다 — n/a)

### 5.5 OCV = 잔류 활성 Zn 의 operando 지시자 (슬 15–16)
**슬 15 (`Fig. 15`)** — 0.1 mAh Zn 전착 후 휴지:
- 전기화학적으로 **활성인 Zn 이 남아 있는 동안 OCV 는 0 V 근처**에 머문다.
- **~10 min 안에 OCV 가 급상승** = Zn 고갈, 자발 부식으로 추정.
- 단계 표기: **(1) 0 V → (2) 100 mV → (3) 400 mV → (4) 500 mV**; +ZnI₂ 계는 **(900 mV)** 까지 간다.
⇒ **OCV plateau 지속시간 = 잔류 활성 Zn 의 operando 지표**로 채택.

**슬 16 (`Fig. 16`)** — plateau 를 두 축으로 스윕:
- **Zn 로딩** 0.1 / 0.2 / 0.4 / 0.8 / **1.6 mAh cm⁻²** → 로딩이 클수록 plateau 가 길다(= 잔류 Zn 많음).
- **ZnI₂ 농도** 0.1 / 0.2 / 0.3 M (0.08 mAh cm⁻² 전착) →
  **"Addition of ZnI₂ shortens the plateau and advances the OCV rise, suggesting accelerated Zn corrosion"**
  ⇒ ★ **ZnI₂ 는 부식을 가속한다**. 그런데 §5.8·§5.9 에서는 ZnI₂ 가 가역성을 **더 좋게** 만든다 (§7 G6 모순).

### 5.6 부식 저항 (슬 17, `Fig. 17`) — **덱의 가장 강한 단일 수치**
- **pre-conditioned Cu: OCV plateau ~3–4 h** vs **bare Cu: ~10 min** (0.1 mAh cm⁻² 전착 후 휴지).
- 해석: 층이 **전착 형상 개선 + Cu–전해질 직접 접촉 제한**으로 부식/부반응을 억제한다("likely").
- 대조군으로 "Pre-conditioned Cu **without** Zn deposition" 도 같이 그렸다.
- ✅ **래스터 실판독으로 확인**: 두 패널 각각 한 곡선이 ~0 V 를 **≈4.1 h**(2 M ZnSO₄) / **≈3.0 h**(+0.2 M ZnI₂)
  유지한 뒤 상승, 나머지 두 곡선은 **≈0.1 h(≈6 min) 안에** 0.4 V 이상으로 뛴다 (`figure-read ≈`).
  본문의 "~3–4 h vs ~10 min" 과 **일치**한다. (ZnSO₄/ZnI₂ 배정은 슬 16 의 "ZnI₂ 가 plateau 를 줄인다"와
  정합하도록 한 것 — 패널 라벨은 벡터라 래스터에 없다.)

### 5.7 층의 상 — 전압 프로파일 근거 (슬 18, `Fig. 18`)
- 탈리 후 전압이 **0 V 위**에 머문다 → **활성 Zn 이 표면에 남아 있지 않다**.
- ⚠ **"Voltage profiles during stripping and rest *suggest* the existence of Zn–Cu alloy"** (§7 G4)
  — **suggest 뿐**이다. 직접 상 동정 아님. 근거 인용: Nat. Commun. **2026, 17, 7363**.
- 조건: 5 mA cm⁻² · 1 mAh cm⁻², "Voltage of 5 seconds after stripping".
- 차트 축: 전압 **0–0.4 V vs Zn/Zn²⁺** / 사이클 **0–3000**.

### 5.8 ★ modified Aurbach 평균 CE (슬 19, `Fig. 19`) — 헤드라인 수치
프로토콜 A: **0.5 mAh 전착 → 0.1 mAh 사이클 ×9** / 프로토콜 B: **5 mAh 전착 → 1 mAh 사이클 ×9**.

| 프로토콜 | 전해질 | **bare Cu** | **pre-conditioned Cu** | 개선폭 |
|---|---|---|---|---|
| **0.5 mAh** (0.1 mAh ×9) | 2 M ZnSO₄ | **77.75 %** (덱 요약 77.8) | **98.14 %** (98.1) | **+20.4 %p** |
| **0.5 mAh** | + 0.2 M ZnI₂ | **75.86 %** (75.9) | **98.82 %** (98.8) | **+23.0 %p** |
| **5 mAh** (1 mAh ×9) | 2 M ZnSO₄ | **96.55 %** (96.6) | **98.49 %** (98.5) | +1.9 %p |
| **5 mAh** | + 0.2 M ZnI₂ | **95.66 %** (95.7) | **98.63 %** (98.6) | +3.0 %p |

발표자 해석 두 줄:
- "Pre-conditioning improves the average CE, **more markedly in the ZnI₂-containing electrolyte**"
- "CE improvement is **pronounced at low areal capacity**, indicating suppressed side reactions on **exposed Cu**"
  ⇒ 저용량일수록 **노출된 Cu 면적 비율**이 크므로 개선이 크다 — 논리가 자기일관적이다.
- ✅ **래스터 실판독**: 4패널 모두 전압-시간 프로파일. 0.5 mAh 프로토콜은 **~40–43 min**(0.1 mAh ×~10회),
  5 mAh 프로토콜은 **~5.7 h**(1 mAh ×~10회)에서 최종 탈리 스파이크가 0.5 V 로 치솟는다 (`figure-read ≈`).
  ⚠ **CE 막대그래프(77.8/98.1 …)는 벡터라 래스터에 없다** — 위 표의 수치는 **텍스트 레이어**에서 나왔다.

### 5.9 하프셀 수명 (슬 20, `Fig. 20`) — 5 mA cm⁻² · 1 mAh cm⁻²
전압 프로파일 스냅샷의 마지막 사이클 번호(= 셀이 죽은 지점). **x-좌표 대조로 확정**:

| 패널 (좌→우) | 조건 | 스냅샷 | **최종** |
|---|---|---|---|
| 1 | **Pre-conditioned Cu + ZnI₂** | 1 / 500 / 1000 / 2000 | **2700th** |
| 2 | **Pre-conditioned Cu, ZnSO₄** | 1 / 500 / 1000 / 1500 | **1584th** |
| 3 | **Bare Cu + ZnI₂** | 1 / 200 / 400 / 800 | **868th** |
| 4 | **Bare Cu, ZnSO₄** | 1 / 100 / 200 / 400 | **597th** |

발표자 해석: "Before pre-conditioning, ZnI₂ 계가 ZnSO₄ 보다 **평균 CE 가 낮다**. After pre-conditioning,
ZnI₂ 가 ZnSO₄ 를 **추월**한다."
> ⚠ **우리가 본 긴장 1건**: 위 표대로면 **bare 상태에서도 ZnI₂(868) > ZnSO₄(597)** 로 수명은 더 길다.
> "before pre-conditioning 은 ZnI₂ 가 열위" 라는 서술은 §5.8 의 **Aurbach 평균 CE**(75.86 < 77.75)에는
> 맞지만 **이 수명 그림에는 맞지 않는다**. 두 지표가 다른 것뿐일 수 있으나, 덱에서는 구분되지 않는다.
> (좌표 대조 결과이므로 패널 배정 오류 가능성은 낮다고 본다 — 그래도 발표자 확인 권장.)

### 5.10 CCD / 고율 (슬 21, `Fig. 21`)
- **10 mAh cm⁻²** 에서 C-rate 를 계단식으로 올려 임계전류밀도 측정. 단계: **1C → 2C → 4C → 8C → 10C**.
- **bare Cu 단락**: **4C**(2 M ZnSO₄) · **2C**(+0.2 M ZnI₂).
- **pre-conditioned Cu**: 두 전해질 모두 **10C 까지 안정**.
- ⚠ **래스터 판독 한계**: 이 슬라이드의 래스터에는 **곡선만** 들어 있고 C-rate 라벨·"Short-circuit" 화살표는
  **벡터 오버레이**라 추출되지 않는다. 각 패널에서 밝은 곡선이 어두운 곡선보다 **먼저 끝나는 것**까지만
  그림으로 확인했다(0–20 h, ±0.4 V vs Zn/Zn²⁺). **4C/2C 라는 숫자 자체는 그림으로 검증 못 했다** —
  본문 텍스트 값이다.

### 5.11 벤치마킹 (슬 22, `Fig. 22`)
- 10 mA cm⁻² · 1 mAh cm⁻², 스냅샷 1 / 500 / 1000 / **2000th**.
- "Half-cell performance under various current densities is **under evaluation**"
  / "results are **comparable to previous reports while showing slightly better performance**"
- 비교군 라벨: **HDE (2025) · CMC-ZnF₂ (2024) · MI (2026) · FU (2025) · PyrB (2025) · Glu (2024) · This work**
  ⚠ 이 6개 약칭의 **완전한 서지정보가 덱에 없다** → 우리 litdb 대조 불가 (§8).
- 차트 축: CE **98–100 %** / 0–2000 cycle, 벤치마크 플롯 CE **99.7–100 %** / 0–5000 cycle.

---

## 6. 결과 — 풀셀 Cu‖AC (슬 23–28)

### 6.1 풀셀 pre-conditioning (슬 23, `Fig. 23`)
- 조건: **사이클당 0.1 mAh**, **방전 컷오프 0.6 V**, 전해질 2 M ZnSO₄ + 0.2 M ZnI₂.
- 하프셀과 마찬가지로 **사이클이 쌓이며 CE 상승**.
- 충전 중 셀 전압이 낮아짐 → **Zn 핵생성 과전압 감소**로 해석.
- 차트 축: CE **92–100 %** / 0–500 cycle · 전압 **−0.10–0 V** · 면적용량 **0–1.2 mAh cm⁻²** (0.05·0.1 눈금).

### 6.2 풀셀 pre-conditioned Cu 의 표면·상 (슬 24, `Fig. 24`)
- **나노스케일 Zn 핵이 Cu 위에 조밀 분포** → 우선 전착 자리 제공.
- ⚠ **하프셀과 달리 풀셀 전극은 뚜렷한 구리색**을 유지한다 (하프셀은 은색으로 변했다 — §4.2).
- ★ **CuI (111) 반사가 확인되어, 재구성된 계면층 안에 CuI 상이 있다**고 명시.
  → 하프셀 슬 12 에서는 상 동정을 못 했는데, **풀셀에서는 CuI 를 잡았다**. (Cu·CuI·Zn 참조 패턴 병기)

### 6.3 풀셀 Zn 전착 형상 (슬 25, `Fig. 25`)
- **bare Cu 셀에서는 CuI 가 전착 Zn 과 함께 생긴다.**
- pre-conditioned Cu 에서는 Zn 이 균일 도금되고 **CuI 존재가 줄어든다** —
  "attributed to Zn being deposited on the Cu surface".
- ⚠ **"Further compositional analysis of the bare and pre-conditioned Cu surfaces is needed"**
- 인용: Nano-Micro Letters **2022, 14.1: 208**.

### 6.4 풀셀 전기화학 (슬 26, `Fig. 26`)
- pre-conditioned Cu 셀에서 충·방전 **과전압 감소**.
- "Pre-conditioning **lowers interfacial resistance while retaining the same Zn–Cu plating/stripping reaction**"
  (반응 자체는 안 바뀌고 저항만 준다는 주장).
- 차트 축: Nyquist **0–15 Ω cm²** · 셀 전압 **0.8–1.6 V** · 면적용량 **0.5–2.0 mAh cm⁻²**.

### 6.5 풀셀 부식 저항 (슬 27, `Fig. 27`)
- **풀셀의 OCV 유지 시간이 하프셀보다 길다.**
- ⚠ "Further analysis is **planned** to verify whether the corrosion resistance is superior in the full cell"
  — **아직 검증 안 된 관찰**.

### 6.6 ★ 풀셀 성능 (슬 28, `Fig. 28`) — x-좌표 대조로 확정

| 전류 | 최대 면적용량 | 용량유지 |
|---|---|---|
| **10 mA cm⁻²** | **1.48 mAh cm⁻²** | **75.0 % @ 600 cycles** |
| **20 mA cm⁻²** | **1.13 mAh cm⁻²** | **89.9 % @ 400 cycles** |

셀: Cu ‖ AC, 2 M ZnSO₄ + 0.2 M ZnI₂. "Improved reversibility is confirmed in the full cell subjected to
in-situ pre-conditioning."
> 참고: 전류를 2배 올리면 **용량은 24 % 줄지만 유지율은 오히려 올라간다**. 유지율이 좋아진 게
> "더 안정해서"인지 "애초에 덜 쓰기 때문"인지 덱은 구분하지 않는다.

---

## 7. ★ 발표자가 **스스로 미해결로 표시한** 문장 (원문 그대로)

이 절이 이 digest 의 존재 이유다. 아래는 **슬라이드 원문 인용**이며, 우리가 붙인 해석이 아니다.
(kb 스코핑 카드의 G1–G7 과 같은 번호를 쓴다 — `kb/projects/zn_alzib_dft_md_contribution_2026_09_03.md` §1.)

| # | 슬 | **원문 (verbatim)** | 성격 |
|---|---|---|---|
| **G1** | 12 | *"The reflection near 43° **cannot be unambiguously assigned** to Zn owing to overlap with Cu"* · *"**Further surface-sensitive characterization (GI-XRD, XPS depth profiling) is required** to identify the layer composition"* | **상 동정 미해결** |
| **G2** | 6 | *"For Cu substate, formation of surface alloy layer exerted a greater influence than the formation of ZHS"* · *"**The Cu-specific mechanism was noted but not systematically investigated**, leaving the optimal pre-conditioning protocol on Cu unexplored"* | 기전 미규명 |
| **G3** | 11 | *"**Further analysis is required to determine whether** the deposited layer provides a high density of nucleation sites **and** limits direct Cu–electrolyte contact"* | **이중기능 미분리** |
| **G4** | 18 | *"Voltage profiles during stripping and rest **suggest** the existence of Zn-Cu alloy"* | 간접 추정만 |
| **G5** | 10 | *"I⁻-rich EDL reduces the **Marcus** charge transfer energy barrier of Zn ions, lowering the nucleation overpotential of Zn."* — **Nano-Micro Lett. 2022, 14, 208 / EES 2024, 17, 7372 인용**, 본인 검증 아님 | 전제 미검증 |
| **G6** | **16 ↔ 20** | 슬 16: *"Addition of ZnI₂ **shortens the plateau and advances the OCV rise, suggesting accelerated Zn corrosion**"* ↔ 슬 20(+19): pre-conditioning 후 **ZnI₂ 쪽 CE·수명이 더 좋다**(98.82 % / 2700 cyc) | **모순 미해소** |
| **G7** | 13 | *"the ZnI₂-added sample shows **hexagonal flakes aligned parallel to the substrate**, implying the formation of a dense Zn layer"* | 배향 원인 미규명 |

**추가로 우리가 집어낸 "발표자 자인" 3건** (위 7개 밖):
- 슬 22: *"Half-cell performance under various current densities is **under evaluation**"* — 데이터 미완.
- 슬 25: *"**Further compositional analysis** of the bare and pre-conditioned Cu surfaces **is needed**"*.
- 슬 27: *"**Further analysis is planned to verify** whether the corrosion resistance is superior in the full cell compared with the half cell"*.
- 슬 30(부록): *"The layer formed by pre-conditioning is **presumed to be damaged by corrosion**"* — **presumed**.

### 7b. 부록 슬 30 — G6 를 정량화하는 자료 (좌표 대조로 확정)
휴지 시간을 넣은 뒤 CE 를 재본 표. **500 cycle pre-conditioned** vs **1 cycle** 비교 맥락.

| 휴지 | **2 M ZnSO₄** | **2 M ZnSO₄ + 0.2 M ZnI₂** |
|---|---|---|
| 없음 | **99.5 %** | **99.4 %** |
| 10 min | **97.5 %** | **89.7 %** |
| 1 h | **88.5 %** | **81.8 %** |
| 5 h | **80.2 %** | **83.0 %** |

⇒ ★ **ZnI₂ 계는 휴지 10분만으로 CE 가 99.4 → 89.7 % 로 무너진다** (ZnSO₄ 는 −2.0 %p).
이게 G6("ZnI₂ 는 부식을 가속하는데 왜 가역성은 좋은가")의 **정량적 얼굴**이다:
**연속 사이클링에서는 ZnI₂ 가 유리하고, 정지(calendar) 조건에서는 ZnI₂ 가 크게 불리하다.**
(5 h 에서 순서가 뒤집히는 것(80.2 vs 83.0)은 덱에서 설명되지 않는다 — 노이즈일 수도, 다른 기전일 수도.)

---

## 8. 인용된 선행문헌 — 우리 litdb 대조

| # | 서지 | 덱에서의 역할 | **우리 litdb 보유?** |
|---|---|---|---|
| 1 | **Nano-Micro Lett. 2022, 14, 208** | 슬 2(무음극 동기) · 슬 10(I₃⁻ → Cu 나노클러스터 재구성) · 슬 25 | **❌ 없음** (grep: `papers/`·`INDEX.md`·`comparison_vs_ours.md` 전무) |
| 2 | **Energy Environ. Sci. 2024, 17(19), 7372–7381** | 슬 10 — **I⁻-rich EDL 이 Marcus 전하이동 장벽↓** | **❌ 없음** (litdb 의 "7372" 히트는 `shin2026_bh4…` 의 무관한 숫자) |
| 3 | **Nat. Commun. 2026, 17, 7363** | 슬 4(기생 부반응 도식) · 슬 18(**Zn–Cu alloy** 근거) | **❌ 없음** |
| 4 | **Adv. Funct. Mater. 2026, 36, e23442** — Zhu 외, *"Pre-Coverage of Side Reaction Sites Enables Quasi-Anode-Free Rechargeable Aqueous Zinc Batteries"* | 슬 2 · **슬 6 = 직접적 선행연구**(ZHS pre-coverage, Cu 기전 미조사) | ⏳ **인입 중** — 2026-09-03 다른 세션이 PDF(`24f63dd6-72._Adv_Funct_Materials__2025__Zhu…pdf`)를 litdb 에 넣는 중. **digest 가 뜨면 이 행을 ✅ 로 고치고 §3.4 를 그쪽 정본으로 링크할 것.** ⚠ 파일명은 **2025**, 덱 표기는 **2026** — 연도 확인 필요 |
| 5 | **Energy Environ. Sci. 2025, 18, 10180** | 슬 4 도식 원출처 (레이아웃 개변 명시) | **❌ 없음** |

**⇒ #4 를 빼면 나머지 4편이 우리 litdb 에 없다.** 수계 Zn 축을 실제로 열려면 **#2(Marcus 전제)**
는 반드시 PDF 를 확보해 `papers/` digest 를 떠야 한다 — **우리 C5(ORCA 재구성에너지 λ)가 검증할 대상의
원전**이라, 그 논문을 안 읽고 λ 를 계산하면 "무엇과 비교할지"가 없다.

**추가로 대조 불가**: 슬 22 벤치마크 6종(**HDE 2025 · CMC-ZnF₂ 2024 · MI 2026 · FU 2025 · PyrB 2025 ·
Glu 2024**)은 **약칭만 있고 서지가 없다** → litdb 대조 불가. 발표자에게 원표를 받아야 한다.

**참고 — 우리 litdb 의 유일한 수계 Zn digest**: `papers/cho2026_eipc_zn_anode_azib.md`
(Cho 2026, ESM 89, 105186 — GO+PAA 복합막으로 **Zn 금속 음극** 보호, 2 M ZnSO₄).
⚠ **전극이 다르다** — Cho 는 Zn foil 음극 위 코팅, 이 덱은 **Zn 이 없는 Cu 집전체**(N/P≈1)다.
공통점은 전해질(2 M ZnSO₄)과 "Zn(002) 배향 유도" 논지 정도.

---

## 9. ★ 그림 판독 기록 — 본 것 / 안 본 것 (정직 목록)

**판독 조건**: 이 환경에는 PDF 렌더러(pdftoppm/mutool/gs)도 PyMuPDF 도 없다 →
`tools/litdb/extract_figures.py` **실행 불가**. 대신 PDF 안에 **PowerPoint 가 심어 둔 래스터 이미지**를
stdlib(zlib)+PIL 로 직접 꺼내 SMask 를 흰 배경에 합성해서 봤다.
⚠ **한계가 크다**: 축 라벨·범례·주석·막대그래프는 **벡터**로 그려져 있어 래스터에 **안 들어 있다**.
즉 **곡선 모양은 보이지만 그게 무슨 조건인지는 그림만으로 알 수 없다.**

### ✅ 실제로 본 것 (그림 5장 / 패널 13개)
| 그림 | 무엇을 봤나 | 본문 서술과 대조 |
|---|---|---|
| `Fig. 11` (1패널) | 조밀한 결절상 전착이 표면을 덮음 | ✅ "densely packed nanoscale Zn deposits" 와 일치 |
| `Fig. 13` (4패널) | 1장 = **기판과 평행한 판상(육각형에 가까움)이 치밀하게 깔림**, 2장 = 수직으로 선 판/침상(덴드라이트형), 1장 = 비교적 평탄 | ✅ G7 의 "hexagonal flakes aligned parallel" 주장을 뒷받침하는 패널이 **실재**한다. ⚠ 어느 패널이 어느 조건인지는 라벨이 벡터라 **확정 못 함** |
| `Fig. 17` (2패널) | 한 곡선이 ~0 V 를 **≈4.1 h / ≈3.0 h** 유지 후 상승, 나머지는 **≈0.1 h** 내 급상승 | ✅ "~3–4 h vs ~10 min" **검증됨** |
| `Fig. 19` (4패널) | Aurbach 전압 프로파일. 0.5 mAh 계열 **~40–43 min**, 5 mAh 계열 **~5.7 h**, 중간 사이클 ~9–10회 | ✅ 프로토콜 서술(0.1 mAh ×9 / 1 mAh ×9) **검증됨**. ⚠ CE 막대(77.8 %…)는 벡터라 **못 봄** |
| `Fig. 21` (2패널) | 0–20 h, ±0.4 V 계단 프로파일. 밝은 곡선이 어두운 곡선보다 **먼저 종료** | △ "bare 가 먼저 단락" 정도만 정합. **4C/2C·10C 라벨은 벡터라 검증 불가** |

### ❌ 안 본 것 / 못 본 것
- **`Fig. 7`·`Fig. 8`·`Fig. 9` (CE·과전압 vs 사이클)** — 벡터. **"~500 사이클 수렴"이라는 이 덱의 핵심
  주장을 그림으로 검증하지 못했다.** 텍스트와 축 눈금만 봤다.
- **`Fig. 12` (XRD)** — 벡터. **43° 피크(G1)를 직접 보지 못했다.** 이 덱에서 제일 보고 싶었던 그림인데
  하필 못 본다.
- **`Fig. 14`·`Fig. 26` (EIS Nyquist)** — 벡터. 축 눈금(0–120 / 0–8 / 0–15 Ω cm²)만 텍스트로 확보.
- **`Fig. 16`·`Fig. 20`·`Fig. 23` 래스터** — 추출은 했으나 **열어보지 않았다**(맥락 예산).
  → `litdb/figures/do2026_bml_alzib_preconditioning/` 에 있으니 필요하면 그때 보면 된다.
- **`Fig. 22` 벤치마크 플롯 · `Fig. 24`/`Fig. 25`(풀셀 SEM/XRD) · `Fig. 27`·`Fig. 28`** — 미판독.
- **슬라이드 전체 렌더 0장** — 렌더러가 없어 "슬라이드 그대로"는 한 장도 못 봤다.

⇒ **결론: 이 digest 의 수치는 사실상 전부 PDF 텍스트 레이어에서 나왔다.**
그림에서만 읽은 값은 §5.6·§5.8 의 `figure-read ≈` 표기 4건뿐이고, 그것들은 본문 값을 **확인**했을 뿐
새 숫자를 만들지 않았다.

---

## 10. ⚠ 비판 / over-claim 방지 (§ 우리 시각)

1. **"층"이 무엇인지 아직 아무도 모른다.** G1(43° 미귀속) + G4(alloy 는 suggest) + G3(이중기능 미분리)
   ⇒ 덱 전체가 **"층이 있다"는 간접 증거**(색 변화·과전압·CE·OCV·SEM) 위에 서 있고, **직접 상 동정이 0** 이다.
   유일한 직접 상 정보는 **풀셀의 CuI(111)**(슬 24) 하나뿐이고, 그건 pre-conditioning 층이 아니라
   **I⁻ 화학의 산물**일 수 있다.
   ⇒ **다만 이건 발표자의 실수가 아니다.** §11.2b 대로 43° 에서의 미귀속은 **회절 기하가 강제하는 것**이라
   더 잘 찍어도 안 갈린다. 비판의 방향은 "왜 못 했나"가 아니라 **"왜 31–39° 로 안 갔나"** 여야 한다.
2. **하프셀 ↔ 풀셀이 서로 다른 층을 만든다.** 하프셀은 **은색**, 풀셀은 **구리색 + CuI**(슬 8 vs 슬 24).
   같은 "pre-conditioning" 이라는 이름으로 묶여 있지만 **생성물이 다를 가능성**이 크다.
   ⇒ 풀셀 결론을 하프셀 기전으로 설명하면 안 된다.
3. **G6 는 단순 모순이 아니라 축 분리 문제다.** §7b 표대로 **ZnI₂ 는 정지(calendar) 조건에서 확실히 나쁘고
   (10분 휴지에 −9.7 %p) 연속 사이클링에서는 좋다.** 덱은 이 두 축을 같은 "reversibility" 로 부른다.
   → **"ZnI₂ 가 가역성을 향상시킨다"는 문장은 축을 명명하지 않으면 틀린다.** (우리 ESW 4축 규율과 같은 병.)
4. **"10 mA cm⁻² 가 최적"의 근거가 얇다.** 슬 7 에서 1/5/10/20/40 mA cm⁻² 를 훑었다고 하지만,
   각 조건의 **정량 지표(수렴 CE·수렴 사이클)가 숫자로 제시되지 않는다**. "most stable" 이 무엇으로 잰
   말인지 덱에 없다.
5. **~500 사이클의 물리적 의미가 없다.** 왜 500 인가에 대한 답이 덱에 없고(시계가 없다), 우리 계산으로도
   못 낸다(kb 카드 §3). 이건 메조스케일/속도론 영역이다.
6. **§5.9 의 수명 서열 긴장** — bare 상태에서 ZnI₂(868) > ZnSO₄(597) 인데 본문은 "before pre-conditioning
   ZnI₂ 가 열위" 라고 쓴다. **Aurbach 평균 CE 축과 수명 축이 반대 방향**일 수 있다는 뜻이므로,
   어느 축의 이야기인지 명시가 필요하다.
7. **풀셀 유지율 비교의 함정** — 10 mA(1.48 mAh, 75.0 %/600cyc) vs 20 mA(1.13 mAh, 89.9 %/400cyc) 는
   **사이클 수도 용량도 다르다**. 유지율 숫자만 나란히 두면 "20 mA 가 더 안정" 으로 오독된다.
8. **첨자·오타** — 슬 7 의 `10 mAh cm⁻²`(→ mA cm⁻²). 인용 시 원문 복사 금지.

---

## 11. 우리 DFT/MD 와의 접점 — ⛔ 축 분리부터

### 11.1 수치로 겹치는 것: **0**
| 우리 축 | 이 덱 | 겹침 |
|---|---|---|
| 이온전도 σ / Ea (Li⁺, LPSCl) | **없음** (Zn²⁺ 수계, σ 측정 0건) | ❌ |
| 산화안정 ESW / grand-potential | **없음** (수계 전위창, CV 0건) | ❌ |
| 기계 E_VRH / B₀ | **없음** | ❌ |
| 전자구조 gap / VBM | **없음** | ❌ |

⇒ **`comparison_vs_ours.md` 물성 4축 표에 이 덱의 수치를 한 줄도 넣지 않는다.**
(우리 db `db/properties/*` 절대값과 **절대 섞지 않는다** — 이온도 전극도 전해질도 다르다.)

### 11.2 겹치는 것: **질문의 구조**
- "**in-situ 로 생긴 계면층이 무엇이고, 왜 수송을 돕고 부작용을 막는가**" — 우리가 LPSCl/Li 계면(SEI)에서
  묻는 것과 **문장 구조가 같다**. 다만 이온·용매·전위가 전부 다르다.
- 방법 이전 가능성: **상 지문표(격자상수 → 분말 XRD 시뮬 → hkl 대조)**, **슬랩 결합에너지 순위**,
  **NEB 이동장벽**, **band gap 으로 전자 절연성 판정** — 우리가 argyrodite 에서 쓰는 도구가 그대로 간다.

### 11.2b ★ **C1 은 이미 계산해서 답이 나왔다** — G1(43° 미귀속)에 대한 우리 답

> 📊 **`db/properties/zn_cu_phase_fingerprint_2026_09_03.json`** (2026-09-03 생성,
> `tools/xrd/phase_fingerprint.py`, Cu Kα₁ λ=1.540598 Å, **실험 문헌 격자상수**(DFT 이완값 아님))

**(a) 발표자가 옳다 — 43° 는 원리적으로 못 가른다.**
42–44° 안에 **8개 반사가 1.469° 폭으로 몰려 있다**:

| 2θ (°) | 상 (hkl) | I_rel |
|---|---|---|
| 42.138 | CuZn₅ (ε) (002) | 24.6 |
| 42.208 | **CuI** (γ) (220) | 70.4 |
| 42.302 | Cu₂O (200) | 38.2 |
| **43.199** | Cu₅Zn₈ (γ-brass) (411) | (위치 전용) |
| **43.221** | **Zn (hcp) (101)** | 100 |
| **43.282** | **CuZn (β′, CsCl) (110)** | 100 |
| **43.318** | **Cu (fcc) (111)** | 100 |
| 43.607 | CuZn₅ (ε) (101) | 100 |

⇒ **Cu(111) ↔ Zn(101) 간격이 0.097°** 다. 통상 실험실 XRD 분해능·기기 broadening 아래에서
**분리 불가**. 게다가 **CuZn-β′(110) 이 그 사이 43.282° 에 정확히 끼어든다** — 즉 슬 18 의
"Zn–Cu alloy 를 suggest" 하는 그 상이 **43° 에서 Cu 와도 Zn 과도 겹친다**.
발표자의 *"cannot be unambiguously assigned"* 는 **표현이 아니라 사실**이다.

**(b) 갈 곳은 43° 가 아니라 31–39° 다.**
이 창에는 **Cu 반사가 하나도 없다**(Cu 는 43.32° 와 50.45° 뿐). 그래서 층 신호가 그대로 드러난다:

| 2θ (°) | 상 (hkl) | 의미 |
|---|---|---|
| 31.77 | ZnO (100) | 산화물 부산물 |
| 31.85 | Cu₅Zn₈ (γ) (310) | **합금 지문** |
| 34.42 | ZnO (002) | |
| 34.98 | Cu₅Zn₈ (γ) (222) | **합금 지문** |
| 36.26 | ZnO (101) | |
| **36.29** | **Zn (002)** | ★ 전착 Zn 의 **texture 축** (슬 10 의 "Zn(002) 배향", 슬 13 의 판상) |
| 36.42 | Cu₂O (111) | Cu 표면 산화 |
| 37.89 | Cu₅Zn₈ (γ) (321) | **합금 지문** |
| 37.94 | CuZn₅ (ε) (100) | **합금 지문** |
| 38.99 | Zn (100) | |

⇒ **제안(실험 쪽 다음 액션)**: GI-XRD 를 **31–39° 창**에 집중해서 찍으면
① Zn(002) texture ② Cu–Zn 합금 상(γ/ε) ③ 산화물(ZnO/Cu₂O)이 **Cu 간섭 없이** 갈린다.
**43° 를 더 잘 찍는 데 시간을 쓰지 말 것.**

**(c) 부수 결과 2건.**
- **ZHS**(Zn₄SO₄(OH)₆·nH₂O)는 **43° 부근에 주선이 없다**. 기저면 d(00l) ≈ 8–11 Å →
  2θ ≈ **8–11°**(고차선 ~16–18°, ~25°). ⇒ 슬 12 의 43° 논쟁에 ZHS 는 애초에 후보가 아니다.
  ⚠ 단 **수화수 n 이 정해지지 않아 계산은 안 했다** — 문헌 범위값이다.
- **CuI(220) 은 42.208°** 로 Cu(111) 에서 **1.11° 떨어져 있다** → 풀셀에서 CuI 를 잡은 것(슬 24)은
  **지문상 신뢰할 만하다**. (덱은 CuI(111) 로 확인했다고 적었다 — CuI(111) 은 저각이라 더 깨끗하다.)

**⛔ 이 계산이 못 하는 것** (json `limits` 그대로):
Rietveld 정량 아님 · **무작위 배향 가정**(전착 Zn 은 002 texture 라 강도는 실제와 다르다) ·
**어느 상이 실제로 생기는지는 말하지 않는다**(열역학·속도론 없음) · Cu₅Zn₈ 는 **위치 전용**
(52원자 basis 미확보 → 강도 null) · ZHS 미계산 · B_iso=0, Kα₂/기기 broadening/zero-shift 없음.

### 11.3 나머지 계산은 → **카드로 넘긴다**
계산 후보 **C1–C7**(상 지문표 / zincophilicity 서술자 / HER ΔG_H* / 갈바닉 Φ / Zn²⁺ 용매화·Marcus λ /
Zn(002) Wulff / MD), 각각의 **"못 하는 것"**, 착수 게이트 4개, 권장 순서(**C1 → C2+C3 → C6 → C5 → C7**)는
전부 여기 있다 — **중복 서술하지 않는다**:

> 📄 **`kb/projects/zn_alzib_dft_md_contribution_2026_09_03.md`**

(C1 은 위 §11.2b 대로 **이미 완료**다 — 카드의 권장 순서 `C1 → C2+C3 → C6 → C5 → C7` 에서 **다음은 C2+C3**.)

이 digest 에서 그 카드에 **추가로 넘길 관측 3건**:
- **(a) 풀셀 CuI(111) 확정**(슬 24) → C1 지문표에서 **CuI(220) 42.208° 는 Cu(111) 과 1.11° 떨어져** 있어
  귀속이 신뢰할 만하다(§11.2b-c). 하프셀(은색)과 풀셀(구리색+CuI)은 **다른 상 집합**이므로,
  C2/C3 슬랩 집합도 **두 벌**로 나눠야 한다.
- **(b) §7b 휴지-CE 표** → C4(갈바닉 구동력)·C3(HER)의 **검증 대상이 "연속 사이클"이 아니라
  "정지 상태 부식률"** 이라는 것이 분명해졌다. 우리가 계산할 양은 **calendar 축**에 걸어야 한다.
- **(c) `Fig. 13` 실판독** → 기판과 평행한 판상이 **실제로 보인다** → C6(Zn(002) Wulff, I 흡착)의 관측
  대상이 실재함을 확인. 다만 어느 조건 패널인지는 미확정이라, C6 착수 전 발표자에게 패널 배정을 물어야 한다.

### 11.4 착수 전 경고 (카드 §4 요약 — 잊기 쉬운 것만)
- **estimand 카드 먼저.** "합금 위 Zn 결합에너지" 는 *조성 × 종단면 × 피복률* 을 선언하기 전엔
  **정의되지 않은 scalar** 다 (SDCP 8회 반려의 그 함정).
- **UMA 는 수계 Zn 전해질에서 검증 영역 밖**이다 (검증 영역 = LPSCl 계열; Li₃N 편향 선례 2026-06).
  MLIP 단독 판정 금지 — 스크리닝 → DFT 앵커.
- **금속 smearing(ISMEAR/SIGMA·degauss)을 state-selection policy 로 선언**하고 결과 보기 전에 게이트로 박는다.

---

## 12. 인용 규율 (이 파일에서 나가는 모든 문장에 적용)

- ⛔ **외부 인용 전면 금지** — 미출판·진행 중 연구, 본인 논문화 예정. 원고/SI/포스터/외부 발표 금지.
- ⛔ **우리 db 절대값과 같은 표에 넣지 않는다.** 이 덱 수치는 전부 **"발표자 값(발표 소환값)"** 으로 표기.
  예: "발표자 값 Aurbach CE 77.8 → 98.1 %(2 M ZnSO₄, 0.5 mAh)" — 우리 σ/Ea/gap 옆에 놓지 말 것.
- ⛔ **부재의 증거로 쓰지 않는다** — "이 랩은 ~을 안 한다" 류 서술 금지. 덱은 발표 시간에 맞춰 잘린 것이다.
- ✅ **발표자에게 직접 물을 수 있다**(내부 세미나). 불확실 항목은 추정하지 말고 **묻는다**.
  현재 물어야 할 것: ① 슬 22 벤치마크 6종 서지 ② 슬 13 SEM 패널↔조건 배정 ③ 슬 20 수명 서열(§5.9 긴장)
  ④ 슬 14/26 EIS 의 실제 R 값 ⑤ 슬 7 "most stable" 의 정량 기준.
- 그림에서만 읽은 값은 **`figure-read ≈`** 표기 (현재 4건, §5.6·§5.8).
- 원본 PDF 는 repo 밖(업로드 경로). 재현하려면 §0 의 sha256 으로 파일을 확인할 것.
