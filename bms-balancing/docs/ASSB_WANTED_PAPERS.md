# ASSB 추가로 필요해진 논문 — 누적 원장

흡수한 논문이 **"이것을 읽어야 한다"** 고 가리킨 논문을 한곳에 모은다. 큐(`ASSB_TRANSFER_NOTE.md` §6)가
*받은 것*의 목록이라면 이 파일은 *아직 없는데 필요해진 것*의 목록이다.

- **지목 수**가 곧 우선순위의 1차 근거다 — 여러 편이 독립적으로 가리킨 논문은 계보의 공백이다.
- 지목은 흡수 보고의 `후속 →` 절에서 옮긴다. 옮길 때 **어느 호가 무엇 때문에** 가리켰는지 같이 적는다.
- 큐에 이미 있으면 그 번호를 적고 **"큐 안"** 으로 표시한다 (중복 요청을 막는다).
- 서지가 불완전하면 불완전한 채로 적는다 — 추측으로 채우지 않는다.

갱신: 2026-09-23 (52호까지 반영 · 2차 묶음 큐 40~59 = 이 원장 §1 상단 20편 수령 — **큐 20~37 흡수 완료**, 이 원장은 이후 사용자 업로드 요청의 정본).

## 1. 큐 밖 — 요청 대상

| 우선 | 논문 | 지목 (assb 호) | 수 | 축 | 왜 필요한가 |
|---|---|---|---|---|---|
| ★★★★ | **Sakka·Yamashige·Watanabe·Takeuchi·Uesugi·Uesugi·Orikasa 2022** — *J. Mater. Chem. A* **10**, 16602−16609 | 25 · 33 | **2** | **Q1**·Q6·DEM | ★ **X선 CT 로 압력별 CAM–SE 접촉 면적 분율을 쟀다** (50 ↔ ≤12 MPa) — **`θ(P)` 측정 후보.** Q1 이 33편 동안 측정량을 한 번(22호 XRD 상한)밖에 못 받았다. **측정 종류의 희소성**으로 최상위. ⚠ 33호(저압 종설, ref [120])도 인용하지만 **다른 명제**(압력 방향·3D 접촉 전략)로 — 25호가 옮긴 접촉 분율 수치를 33호는 한 글자도 안 옮김. 두 인용이 갈리는 것은 원문으로만 풀린다. DEM `θ(P)` 보정 목표 · **✅ 39호 흡수 (`de1a784e`, 큐 40)** — 판정: 잰 것은 `θ(P)` 가 아니라 **표면 피복 φ(P)** (NCM 표면적 대비 LGPS 접촉 면적), **제조 압력**, 신품 CT(사이클 0). 37호 기준 `A_eff` 손잡이(= k_p 와 항등) — 통째 비연결 u(LAM_PE 쪽)는 0.5 µm 화소에서 측정 범위 밖. φ ×1.10 vs R_ct ×14 → 면적이 R_ct 로그 변화의 ≈4 % 만 설명 (곱 축퇴가 데이터로 드러남). 25호·33호 인용은 **갈린 게 아니라 나눠 인용** (본문 결과 ↔ 결론 제언). Q1 +0.5 · Q6 +0.5 |
| ★★★★ | **Ikezawa 외 2020** — *Electrochem. Commun.* **116**, 106743 | 16 · 17 · 18 · 19 · 21 | **5** | Q5 | **R-LTO 기준극의 원전.** 18호가 "Assuming 1.55 V" 로 쓴 전위, 19호의 기준극 쌍 불일치 ±30 mV 의 근거. 21호는 이것을 **InLi-(In) 조립의 예로도** 인용한다 — **두 Q5 가지(R-LTO · In)가 만나는 자리**. ~~3배 압착에서 110 Ω cm²~~ (40호 정정: 원전에 그 수 없음 — 21호의 "∼40 mV ≈110 Ω cm²" 는 C/2 충–방전 **폭** 42.8 mV 를 옮긴 것, 탈리튬 과전압만은 21–23 mV ≈ 58–63 Ω cm²) · **✅ 40호 흡수 (`804cf4cf` 에 섞여 커밋 · 추적 `4d65a7b0`, 큐 41)** — 판정: 누설 0 · 드리프트 명시 측정 0 (두 전극 **차**로 ≈3 mV 상한만) → 구조적 공백 3 그대로. **1.55 V 는 측정 아님** (Costard 2017 액체셀 인용 + Li-In 문헌값을 증인으로 쓴 순환 — Q5 16번째 형태 '상호 증언'; 증인 0.62 V 면 1.5745 V = 16호의 1.57 V). 19호 ±30 mV 근거도 없음. 두 가지는 인용·기각·한 셀 세 겹으로 만난다 |
| ★★★★ | **Nam 외 2018** — *J. Mater. Chem. A* **6**, 14867 | 17 · 20 · 21 · 40 | **4** | Q5·Q7 | **Li 고갈 In 층 원전 (TOF-SIMS 단면 지도, 정성)** — ⚠ "In-rich depletion layer" 는 17호의 표현이고 원문에 그 낱말 없음 (41호 확인). 17호의 국소 고갈(+680~780 mV)과 20호의 Li 도금 전위 도달을 잇는 자리. 21호는 "탈리튬 후 계면 Li 고갈을 실험으로 봤다" 로 인용 — 21호 조립 방향 판정의 원전 · **✅ 41호 흡수 (`42c72cf5`, 큐 42)** — 판정: 본문 0.62 V 는 **인용**(Jung 2008 *AFM*), 그러나 **SI Fig. S2 가 기준극을 Li₀.₅In ↔ Li 금속으로 바꿔 대조** — 판독 중점 ≈0.621 V, 두 기준 차 ≈2 mV (수는 미인쇄) → **Q5 +0.5**, 17번째 형태 '기준극 교체 대조'. 40호 '상호 증언' 순환의 다른 끝에 순환 밖 측정 고리가 하나 있었다. 고갈층 ≈50 µm 는 TOF-SIMS 1 시편·대조 지도 없음. 쿨롱 효율 저하는 LLI 가 아니라 **연성 단락 누설** — CE 를 LLI 대리로 쓰는 통로의 세 번째 오염 경로 |
| ★★★★ | **Santhosha 외 2019** — *Batteries & Supercaps* **2**, 524 | 17 · 20 · 21 | **3** | Q5 | **0.62 V 의 출생지.** 그리고 InLi-(In) 형이 탈리튬 전류를 냈다는 보고가 **21호와 어긋난다** — creep 인가 전기화학 리튬화분인가 · **✅ 42호 흡수 (`f250306b`, 큐 43)** — 판정: 0.62 V 는 Li 대비 **측정**이나 **액체셀**(Swagelok 3전극, LiTFSI DOL:DME, 쿨로메트릭 적정 1 h/0.5 h) — ASSB 안 Li 대비 측정 0 → **Q5 +0.5**, 18번째 형태 '다른 전해질의 원전'. 평탄 창 ≈1–47 at% Li (판독), 창 안 이완 OCV 처짐 ≈15 mV. '출생지' 는 "실온·조성 분해·Li 대비 측정의 출생지, 단 액체셀" 로 좁힘 — 0.6 V 자체는 Wen–Huggins 1980 · Takada 1996 · Webb 2014 가 앞선다. 계보의 두 영점(R-LTO 1.55 V · In 0.62 V)이 **둘 다 황화물 SE 밖에서 측정**. 21호 어긋남: 대칭셀 저항 12 Ω cm² 가 SE 벌크 옴(우리 계산 ≈400–570 Ω cm²)의 1/25–1/47 — 이온 전류 입증 안 됨, 21호 creep(전자 경로) 가설과 양립 (**후보 설명 중 하나로 기록 — 승격 여부는 사용자 결정 대기**) |
| ★★★ | **Fukunishi 외 2023** — *ACS Appl. Energy Mater.* **6**, 10908 | 19 | 1 | Q1·Q2 | 흑연 3전극 + **cyclability** → `θ(N)`·`Ea(N)` 가능성이 계보 최고. 곱 축퇴 처방 3단계(`Ea` 면적-불변 채널)를 시간축으로 검증할 입력 · **✅ 43호 흡수 (`eb3a05f5`, 큐 44)** — 판정: 3전극 EIS 로 흑연 R_SE·R_X·R_CT 와 CPE·Ea 를 노화 **전후 모두 ± 로 인쇄**(계보 첫 완비). 용량 손실 → LAM 배정은 dQ/dV 봉우리 높이 하나에 기댄 **해석**. 반쪽전지(Li-In 저장소 ≈18배)라 LLI 없음 → 저율 용량 비 ×0.75–0.78 = `(1−LAM_NE)(1−u)` **음극 판 곱 축퇴**. θ(N) 여전히 0/43. ★ R-LTO 기준극 **첫 표류 값**: 333 K 가속 열화 뒤 흑연·Li-In 모두 공통 모드 ≈−14 mV (저자 'could' 배정) → **Q5 +0.5**, 19번째 형태 '공통 모드 표류 판독'. 1.55 V 는 또 인용(Colbow·Ohzuku) |
| ★★★ | **Jin·Park·Park·Lim 2015** — *Electrochim. Acta* **185**, 242 | 20 | 1 | Q2·Q6 | 20호 셀의 원전 — 그 편이 비운 G1 복합체 조성 · G2 σ · G3 압력 · **✅ 44호 흡수 (`8049c845`, 큐 45)** — 판정: 20호 공백 **G1 채움**(TiS₂ 50 wt% + SE 50 wt%, 도전재 없음 → 20호 0.06 g 은 활물질 질량) · **G2 조건까지 채움**(30 MPa 펠릿, SS 차단, 1 kHz–7 MHz) · **G3 절반**(제조 30 MPa 인쇄, 운전 압력은 Fig. 1 그림에만). 같은 레시피의 **다른 셀**. 'effective contact area' 는 GITT `√D·S/θ` 곱을 대조 셀 가정으로 쪼갠 값 (측정 아님). Li 재고 수지 위반(TiS₂ x≈1.37 > 1 — 분모 가정 전제). Li-Si 는 평탄 상대극 아님 (이완 전압 셀 간 ≈95 mV 차) → α·β 이식 평탄 음극 후보에서 빠짐 |
| ★★★ | **Hertle·Walther·Mogwitz 외 2023** — "Miniaturization of Reference Electrodes for Solid-State Lithium-Ion Batteries", *J. Electrochem. Soc.* **170**, 040519 (16호 ref [24] 인쇄) (⚠ 46호에서 Schlenker 2020 을 이 행에서 분리 — 아래 별도 행) | 16 · 21 | 2 | **Q5** | **μ-RE 원본 — Q5 최대 공백** (16호 판단). 21호: **"0 V 로 놓은 리튬화 금선" 관례의 출처** — 16호 셀 간 0.11 V 어긋남 가설 검증 · **✅ 45호 흡수 (`f1aaad1e`, 큐 46)** — 판정: '0 V' 는 Li 대조 셀이 아니라 **금선 위에 Li 를 석출**해 상(phase) 정체성으로 정한 영점. Fig. 7 이 Li 대 In/InLi = **−618 mV 를 셀 안에서 측정 축으로 인쇄**(계보 첫 ASSB 내 값, 42호 액체 0.622 V 와 대조) — 단 본문은 가정 어조·± 없음 → **Q5 +0.5**, 21번째 형태 '소모품으로 인쇄된 기준극'. 드리프트 값 0 ('약 8일'), 누설 0/45 (8일 수명 = 평균 ≈39 nA 소모 — 21호 간접 상한의 ≈9배, 우리 계산). 기준극은 **계단형**(+0.133 → +0.215–0.25 V)으로 튈 수 있음 → 전지 분할에서 LLI/LAM_PE 흉내. 16호 ∅25 µm 이식은 조건 밖 (면적당 전하 1/9.6, 비평탄 NMC 상대로 리튬화) — 16호 0.11 V 어긋남 = 한 평탄 계단 가설(미확정). 21호 추정 계보 'Schlenker → Hertle' 는 **불지지** (Schlenker 미인용, Giessen) ⚠ 47호: 45호가 [20](Solchenbach)에 단 **"134 / 215 mV" 는 그 원전에 없음** — Solchenbach 는 같은 Bach 2015 를 "∼0.3 / ∼0.2 V" 로 옮김 (칸 값 표가 둘) |
| ★★ | **Schlenker·Stępień·Koch·Hupfer·Indris·Roling·Miß·Fuchs·Wilhelmi·Ehrenberg 2020** — "Understanding the Lifetime of Battery Cells Based on Solid-State Li₆PS₅Cl Electrolyte Paired with Lithium Metal Electrode", *ACS Appl. Mater. Interfaces* **12**, 20012 | 21 | 1 | Q5·Q7 | 21호가 '0 V 리튬화 금선 관례의 출처' 로 Hertle 행에 병합했던 편 — **46호에서 분리**. **✅ 46호 흡수 (`577b87a7`, 큐 47)** — 판정: 금 도금 W 선 기준극을 **썼지만 영점을 정하지 않음**(Li\|Li 대칭셀 AC 분할만 — DC 값이 결과에 안 들어감, Q5 22번째 형태 '영점이 들어가지 않는 자리'). 계보는 **두 줄이 16호에서 처음 만남**: 하드웨어·저자 선(Marburg: Schlenker → 16호, Roling·Miß 공저) · 영점 선(Giessen: Hertle → 16호 [24]). 0 V 관례의 출처가 **아니다**. Q7: 수명 = 계면 면적 손실(저자 해석) · 단락 판정은 '급격한 전압 강하' 하나 — **연성 단락 배제 안 됨**, 대칭셀은 OCV 0 V 라 자기방전 신호가 구조적으로 안 보임. 저자가 'A 또는 B' 를 직접 쓰고 두 가지가 같은 말로 끝남(Li 음극판 곱 축퇴) |
| ★★★ | **Solchenbach 외 2016** — *J. Electrochem. Soc.* **163**, A2265 | 21 · 45 | **2** | Q5 | **금선 기준극(GWRE) 원전 (액체셀)** — 0.31 V 와 "CE 거칠어짐" 가설의 출처. ~~21호가 액체셀에서 잰 값을 ASSB 셀로 옮겨 쓴~~ **교정 이식의 뿌리** — 47호 정정: 값(0.31 V)의 **조상은 액체**, 21호는 ASSB Li\|Li 셀(3 MPa)에서 **다시 쟀고** 이식은 ASSB 안(Li\|Li → 20 MPa InLi 셀)에서 일어났다 · **✅ 47호 흡수 (`14e12031`, 큐 48)** — 판정: 0.311 V 는 액체 Li\|Li T-셀에서 **Li 대비 직접 측정**한 LixAu(0<x<∼1.2) 첫 2상 칸 OCV (150 nA×1 h, 절단면만 노출). 드리프트 판독: 20 h 이후에도 ≈3 mV, 2 mV 안은 ≈50 h 부터; 40 °C 에서 +35 mV 이탈. 누설 직접 0/47, 간접 상한 ≈0.27 nA. **0.31 V 와 0 V 는 같은 금선 사다리의 맨 위·맨 아래 칸**. 21호 이식은 원전 조건 넷 중 둘 벗어남(노출 면적 ≈40배 · 2 h 판독) — 틀렸다는 증거는 없고 **검사되지 않았다**. 액체셀이라 칸 0 (도구 칸), Q5 23번째 형태. 'CE 거칠어짐' 은 추론("We believe", 셀 1) |
| ★★ | **Dugas 외 2021** — *J. Electrochem. Soc.* **168**, 090508 | 21 | 1 | Q5·Q2 | ~~원형 InLi 기준극~~ → **전면 Li₀.₅In:SE(60:40) 복합 기준층** (원형 링은 **집전체** — 21호·원장이 집전체를 기준극으로 읽었다, 48호 정정) + 복합 CE. ~~리튬화에 따른 저주파 변화~~ → Li-In 저주파 호는 방향 무관 **시간에 따라 단조 성장**, 방향 의존은 **Li 금속** 쪽 (48호 정정). 21호가 "expected" 의 근거로 인용 · **✅ 48호 흡수 (`8da9f47b`, 큐 49)** — 판정: 영점은 Santhosha 622 mV **인용**(3전극 결과엔 안 들어감). 같은 재료 기준극으로 상대극 전위 창을 잼(β-LPS ±160 mV · argyrodite ±20 mV) + "20 mV ↔ ≤2 mAh/g" 로 용량 오차 환산 + **2전극 허용 조건 인쇄**(계보 첫) → **Q5 +0.5**, 24번째 형태. 2전극 재구성으로 **비식별성을 같은 셀에서 시연**(중간 호 ×2.2, "cannot be decorrelated"). 누설 0/48 |
| ★★ | **Barai·Uddin·Widanage·McGordon·Jennings 2018** — "Study of the influence of measurement timescale on internal resistance characterisation methodologies for Lithium-ion cells", *Sci. Rep.* **8**, 21 (20호 ref 24 인쇄) | 20 | 1 | Q2 | `R₀`/`R_ct`/`R_p` ~~작도법 원전~~ → **작도 규약을 시간 척도로 해석한 편** (작도 규약 자체의 출처는 Waag 2013 — 49호 정정). 제목이 *measurement timescale* — 20호에서 "분해가 적합조차 아니다 — 작도다" 가 나온 자리 · **✅ 49호 흡수 (`867d9c7c`, 큐 50)** — 판정(액체셀, 도구 칸): **총저항은 같은 양의 다른 창**(5 C 펄스 ΔV/ΔI(t) ↔ EIS \|Z\|(1/t) −6…+11 %), `R₀`/`R_ct`/`R_p` 는 **창 경계의 규약**(같은 셀·상태에서 방법 간 ×2.0·×2.9·×13; EIS `R_p` 경계만 0.1→0.01 Hz 로 옮겨도 ×3.9). 비유일성을 본문 두 곳에 인쇄하고 결론이 지움(Q4 41번째 성질). 20호는 모양 규칙만 가져가고 시간 규약(2 s·10 s)을 두고 옴 — 20호 `R_ct` 창은 원전의 ≈10³ 배 |
| ★★ | **Miß·Ramanayagam·Roling 2022** — "Which Exchange Current Densities Can Be Achieved in Composite Cathodes of Bulk-Type All-Solid-State Batteries? A Comparative Case Study", *ACS Appl. Mater. Interfaces* **14**, 38246 (16호 ref [30] 인쇄) | 16 | 1 | Q2 | TLM(전송선 모델) 원본 — 16호의 곱 축퇴 실측 표본이 기대는 모형 · **✅ 50호 흡수 (`7f92694e`, 큐 51)** — 판정: 면적과 j₀ 를 **가르지 않음** — 완전구 기하 면적 `a_v = 3ε/r` 을 넣고 데이터는 `j₀·a_v` 곱만 정함 (두께 가변은 R_ion ↔ R_CT/(a_v d) 만 가름). **16호 '접촉 면적 ≡ 1' 가정의 출생지**. 면적 규약 한 줄(a_v·τd → a_v·d, '적합 개선') 이 j₀ 를 τ 배(≈6.1–6.8) 옮김. 같은 지면 LCO↔NMC ×235 비교는 R·C 검사 통과, **16호↔50호 편 간 비교는 면적 서명**(1/R ×12.1 · C ×15.4 · τ ×1.28 — 우리 계산). r_CAM 2.5 µm 은 공칭 확인값. 칸 0 · Q4 42번째 |
| ★★ | **Illig·Ender·Chrobak·Schmidt·Klotz·Ivers-Tiffée 2012** — "Separation of charge transfer and contact resistance in LiFePO₄-cathodes by impedance modeling", *J. Electrochem. Soc.* **159**, A952–A960, doi `10.1149/2.030207jes` (18호 ref [29] · 11호 ref [9] 인쇄; 18호는 저자명을 "Chroal" 로 오기) | 11 · 18 · 47 | **3** | Q1·Q2 | "전하이동과 **접촉저항**의 분리" — ~~곱 축퇴(`θ`↔`j₀`)를 가르는 방법의 액체셀 원형~~ → **직렬 두 호(P1C 전하이동 · P2C 양극층\|Al 집전체 전자 접촉)의 이름 가르기** (51호 정정: 한 호 안의 곱 `A·j₀` 는 안 건드림, 카드의 CAM\|SE 이온 접촉 θ 와 다른 물리) · **✅ 51호 흡수 (`1ea489a1`, 큐 52)** — 판정(액체 LFP, 도구 칸): 측정 = DRT 대역(≈1 kHz vs 1–8 Hz) · 대칭셀 전극 배정 · **Ea 0.45 vs 0.06 eV**(셀 1, ± 없음) · SOC 의존. 이름은 가정('전달 과정은 항상 온도 활성'). 조작(캘린더링)은 네 변수 동시 변화라 방향만. 우리 재계산: 두 호 C 가 ≈1 µF vs ≈3 mF cm⁻² (3 자릿수) — 저자는 이 채널 미사용. ⚠ **'Ea≈0 = 접촉' 은 ASSB 로 안 옮겨짐**(18호 ASSB 전자 호 Ea 41–70 kJ/mol). 11호는 대역만 가져가고 온도 근거는 두고 옴. Q4 43번째 |
| ★★★ | **Oh·Kwon·Choi S.H.·Lee N.·Sohn·Lee T.·Lee T.·Kim J.Y.·Bae·Choi J.W. 2025** — "All-Solid-State Batteries with Extremely Low N/P Ratio Operating at Low Stack Pressure", *Adv. Energy Mater.* **15**(16), 2404817, doi `10.1002/aenm.202404817` (13호 ref [34] 제목 인쇄 · 14호 ref [10]) | 13 · 14 | **2** | Q6·Q3·Q4 | 저압 실셀 — 14호(Maxwell Protocol)와 **같은 연구실**. 13호 후속 4순위 → 14호에서 1순위 승격 · **✅ 52호 흡수 (`d349215e`, 큐 53)** — 판정: 운전 압력 20 MPa · 3 MPa(스프링/파우치 토크 — 교정 근거 없음; 표준 체결식으로는 17–29 MPa). **압력 효과는 분리 불가** — 두 점에서 적재(20↔6 mg/cm²)·N/P(0.15↔0.66) 동시 변화; 제목의 두 조건(N/P 0.15 · 저압)은 한 셀에서 안 만남. 용량 제한 전극·손실 배정 0 (LLI·LAM 낱말 0). 우리 계산: 3 MPa 누적 충–방 결손 ≈575 mAh/g = 양극 Li 재고의 ≈2배인데 용량 65 % 잔존 → **CE 결손은 Li 손실 아님**(누설 전자·SE 분해) — 41호 연성 단락 오염의 실셀 크기 판. 칸 0 · Q4 44번째 |
| ★★ | **Ren·Danner·Moy·Finsterbusch·Hamann·Dippell·Fuchs·Müller·Hoft·Weber 외 (…Latz·Srinivasan·Janek·Sakamoto·Wachsman·Fattakhova-Rohlfing) 2023** — "Oxide-Based Solid-State Batteries: A Perspective on Composite Cathode Architecture", *Adv. Energy Mater.* **13**, 2201939, doi `10.1002/aenm.202201939` (02호 ref 17 은 제목 없이 "2022, page 2201939" — 온라인 2022 · 권호 2023. 제목은 웹 검색으로 확인) | 02 (ref 17) | 1 | **Q1 시간축** | **`θ(N)` 시간축의 입구** — 1·2호가 동역학을 안 줬다. ⚠ **Perspective(종설형)·LLZO 산화물계** — 1차 `θ(N)` 측정 기대는 낮고, 그 안의 1차 원전을 찾는 입구로 본다 |
| ★★★ | **Neumann·Hamann·Danner·Hein·Becker-Steinberger·Wachsman·Latz 2021** — "Effect of the 3D Structure and Grain Boundaries on Lithium Transport in Garnet Solid Electrolytes", *ACS Appl. Energy Mater.* **4**, 4786–4804 (02호 SI ref (3) 제목 인쇄 · 02호 ref 38 · 27호 ref 14) | 02 (ref 38) · 27 | **2** | Q2 | GB 저항 모형 원전 + **EIS 로 파라미터화된 measured 라벨** |
| ★ | **Hlushkou 외 2018** — *J. Power Sources* **396**, 363−370 | 01 (ref 16) | 1 | Q1 | FIB-SEM **실측** 미시구조 — 합성 기하와 대조 |
| ★★ | **Bielefeld·Weber·Rueß·Glavas·Janek 2022** — "Influence of Lithium Ion Kinetics, Particle Morphology and Voids on the Electrochemical Performance of Composite Cathodes for All-Solid-State Batteries", *J. Electrochem. Soc.* **169**, 020539, doi `10.1149/1945-7111/ac50df` (02호 ref 36 · 14호 ref [69] — 둘 다 제목 없음, 제목은 웹 검색으로 확인) | 02 · 14 · 50 | **3** | Q1 | pore(void) 문턱 → 1호 `p_c` 와 이어짐. ⚠ **정정: '실험판' 이 아니라 FEM 시뮬레이션** (1호 Bielefeld 2019 모델의 후속 — void 를 넣은 미세구조 모델) |
| ★★★ | **Bielefeld·Weber·Janek 2020** — *ACS Appl. Mater. Interfaces* **12**, 12821−12833 | 15 · 24 | **2** | Q1·Q4 | 1호 직계 속편. 24호의 **14 % void 가정과 τ 정의의 출처** — 01호와 24호를 잇는 유일한 고리 |
| ★ | **Asheri·Fathidoost·Glavas·Rezaei·Xu 2023** — "Data-driven multiscale simulation of solid-state batteries via machine learning", *Comput. Mater. Sci.* **226**, 112186 (15호 ref [22] 제목·권·쪽 인쇄; 저자 전원은 웹 검색) | 15 | 1 | Q3·Q4 | 15호가 아는 유일한 SSB-ML ("interface damage"). 실체: 미세 스케일 화학-기계 시뮬(계면 박리 포함) 데이터로 학습한 **신경망 대리모형**을 2단 셀 모델에 넣어 박리→용량 손실 예측 — 측정 아님, 시뮬 대리 |
| ★ | **Li Q. 외 2025** — *Nat. Energy* · **Zhang 외 2025** — *Nat. Commun.* | 13 | 1 | Q6 | 무외압 Si 음극 — 저압 축 |
| ★ | **Masias 외 2019** — *J. Mater. Sci.* **54**, 2585 | 21 | 1 | Q6·Q7 | Li creep 기계 물성 — 21호 Li 박 조립 방향의 기계 쪽 근거 |
| ★★★ | **Zhang·Schröder·Arlt·…·Janek 2017** — *J. Mater. Chem. A* **5**, 9929−9936 | 22 · 23 · 33 | **3** | Q1·Q6 | 22호 셀 장치의 원전(양극 면적 미기재) + **충전 중 부피 수축 → 접촉 감소**를 압력으로 감시한 근거 — Q1 의 기구 쪽 입력 |
| ★★★★ | **Zhang·Weber·Weigand·…·Janek 2017** — *ACS Appl. Mater. Interfaces* **9**, 17835−17845 | 22 · 23 · 24 · 39 · 41 · 42 | **6** | Q1·Q2·Q5 | 7:3 조성의 근거 · **토모그래피** — 공극률 실측 후보. 23호(Koerver)의 **방법 원전**(본문 8회): 셀 기하·등가회로 배정·"In kinetic hindrance" 배정의 근거가 전부 여기로 간다 |
| ★★ | **Koerver·Walther·Aygün·…·Janek 2017** — *J. Mater. Chem. A* **5**, 22750−22760 | 22 · 42 | **2** | Q2 | 산화 계면층 — 곱 축퇴의 **`j₀` 쪽** 원전 (큐 22 Koerver *Chem. Mater.* 와 **다른 논문**) |
| ★★ | **Nam·Oh·Jung·Jung 2018** — *J. Power Sources* **375**, 93−101 | 22 · 39 | **2** | Q1 | 건식↔슬러리 혼합 복합전극 미세구조·분리. ⚠ 위의 **Nam 2018 *JMCA*** 와 **다른 논문** |
| ★ | **de Biasi 외 2017** — *J. Phys. Chem. C* **121**, 26163 · **Kondrakov 외 2017** — *J. Phys. Chem. C* **121**, 24381 | 22 | 1 | Q8 | 격자상수 ↔ `x(Li)` 교정의 원전 — 22호가 `c(x)` 최대 근처에서 **두 가지로 갈리는** 자리의 기구 |
| ★ | **Chen·He·Zhang·Wang·Ni 2013** — *Energies* **6**, 1632−1656 | 22 | 1 | Q1 | 22호가 기댄 "percolation theory" (SOFC) — 01호 모델과의 관계 |
| ★★★ | **Kondrakov·Schmidt·Xu·…·Janek 2017** — *J. Phys. Chem. C* **121**, 3286−3294 | 23 | 1 | Q1 | **NCM811 부피 수축 %의 원전** — 23호 SEM 틈 폭으로 역산한 요구치(ΔV/V ≈3–20 %)를 닫을 값. 22호의 *JPCC* 121, 24381 과 **다른 논문** |
| ★★ | **Zaghib·Simoneau·Armand·Gauthier 1999** — *J. Power Sources* **81−82**, 300−305 | 23 | 1 | Q5 | **LTO 1.55 V 가정의 뿌리** — 18호 "Assuming 1.55 V" 보다 이른 근거 (액체셀). Ikezawa 2020 과 함께 R-LTO 가지의 원전 쌍 |
| ★★★ | **Jung·Oh·Nam·Park 2015** — *Isr. J. Chem.* **55**, 472−485 | 23 · 41 | **2** | Q5 | In **0.6 V 가정**의 인용 근거(리뷰) — Santhosha 2019 와 함께 In 가지의 원전 쌍 |
| ★ | **Ishidzu·Oka·Nakamura 2016** — *Solid State Ionics* **288**, 176−179 | 23 | 1 | Q1·Q8 | 조성별 격자 부피 변화 — "Ni 가 많을수록 수축이 크다" 의 근거 |
| ★ | **Auvergniot·Cassel·Foix·…·Dedryvère 2017** — *Solid State Ionics* **300**, 78−85 | 23 | 1 | Q2 | XPS 산화종 배정(P₂S₅ 배제, S−Oₓ)의 참조 |
| ★★★ | **Minnmann·Quillman·Burkhardt·Richter·Janek 2021** — *J. Electrochem. Soc.* **168**, 040537 | 24 · 50 | **2** | Q3·**Q4** | 차단 셀 + TLM 방법의 원전 — "덜 중요한 저항은 자유롭게 둔다" 관행의 출처인지. DEM 브랜치에 `minnmann2021_sigma_tau_porosity` 앵커가 있다 (NCM-622+Li6PS5Cl = 우리 계) — **앵커 ≠ digest** |
| ★★★ | **Park·Zhao·Kang·…·Chueh 2021** — *Nat. Mater.* **20**, 991−999 | 24 | 1 | Q1·Q2 | **동역학이 만드는 가짜 상분리** — 24호 Fig. S17 의 θ 형 봉우리의 대안 설명이자 `i₀(x)` 의 출처. θ 와 η 를 가르는 판정에 직접 걸린다 |
| ★★ | **Naik·Vishnugopi·Mukherjee 2022** — *ACS Appl. Mater. Interfaces* **14**, 29754−29765 | 24 | 1 | **Q4** | 24호 "not kinetically limited" 판정의 근거 — **민감도 분석이 있는지** 확인 대상 (Q4 입구 후보) |
| ★★ | **Davis·Goel·Liao·…·Dasgupta 2021** — *ACS Energy Lett.* **6**, 2993−3003 | 24 | 1 | Q2 | 황화물 복합전극의 **operando 광학 η(z)** — EDXRD 와 독립인 깊이 채널 |
| ★★★ | **Shi·Tu·Tian·…·Ceder 2020** — *Adv. Energy Mater.* **10**, 1902881 | 24 · 25 | **2** | Q1 | 입도비 → 이온 수송 — 24호 "굴곡도가 진화했다" 기구의 원전 · 25호 **DEM 이용률의 방법 원전**. ⚠ 4호 Shi 2020(기계 열화)과 **다른 논문** |
| ★ | **Buchberger·…·Gasteiger 2015** — *J. Electrochem. Soc.* **162**, A2737 | 24 | 1 | Q3·Q8 | c/a → x 교정식 (x < 0.5) — Li 함량이 1 을 넘는 교정 오프셋 점검용 |
| ★ | **Li Z.·Yin·…·Liu P. 2020** — *Chem. Mater.* **32**, 6358−6364 | 24 | 1 | Q2 | 액체셀 두꺼운 전극 깊이 프로파일 · 전류 역전 · 가중평균 관행의 선례 |
| ★ | **Okasinski·Shkrob·Chuang·…·Abraham 2020** — *Phys. Chem. Chem. Phys.* **22**, 21977 | 24 | 1 | Q3·Q6 | 가압 불균일과 측면 구배 — 조각 정렬 문제 점검용 |
| ★★★ | **Xu·Yang·Li 2024** — *Adv. Energy Mater.* **14**, 2303539 | 25 · 32 · 33 | **3** | Q6 | 압력 종설 — 8호가 인용한 "<≈1 MPa" 의 출처로 보인다. 32호 `MPa` 0회, **33호는 이 편을 인용([11])하나 "수백 MPa" 문장에만** — "<≈1 MPa" 는 여전히 8호 단독 인쇄. 확인처는 이 원문뿐 → ★★★ 승격. 산업 요구치 계보 5편·4값(≈1·0.4–1·2·5 MPa)·확인된 원전 0 |
| ★★ | **Schlautmann·Weiß·Maus·…·Bielefeld 2023** — *Adv. Energy Mater.* **13**, 2302309 | 25 | 1 | Q1·Q2 | 같은 변수(SE 입도 분포)의 **독립 표본** — 25호의 셀 1개·교락을 가를 입력 |
| ★★ | **Jiao·Wang·Chen·…·Liu 2023** — *Energy Storage Mater.* **61**, 102864 | 25 | 1 | Q1 | DEM 연결성·굴곡도 후처리의 방법 원전 — **DEM 브랜치에 직결** |
| ★★ | **Orue Mendizabal 외 2023** — *ACS Appl. Energy Mater.* **6**, 11030 | 25 | 1 | Q2·Q5 | 양극·음극 계면 EIS 배정(`R_SSE/anode` ↔ `R_SSE/NCM`)의 근거 — 17호 함정 판정 |
| ★ | **Wang·Li 2024** — *Adv. Mater.* **36**, 2309306 | 25 | 1 | Q1 | 계층형 SE → 낮은 굴곡도 주장의 선행 |
| ★ | **Kim J.T.·…·Sun Y.-K. 2023** — *J. Mater. Chem. A* **11**, 20549 | 25 | 1 | Q6 | argyrodite 코팅 NCM 의 **상압 운전** — 저압 대조군 |
| ★ | **Minnmann·…·Janek 2022** — *Adv. Energy Mater.* **12**, 2201425 | 25 | 1 | — | 종설. ⚠ 위 Minnmann 2021 *JES*(TLM 원전)와 **다른 논문** |
| ★★★ | **Raijmakers·Danilov·Eichel·Notten 2020** — *Electrochim. Acta* **330**, 135147 | 26 · 37 | **2** | Q4·Q3 | 26호의 **데이터·"문헌값"·평형 곡선·β 함수가 전부 이 한 편**에서 온다. 26호 적합 변수 10개 중 7개가 정확히 문헌값 ×1.0500 이고 `D_e⁻` 가 10 자릿수 벗어났다 — 문헌값이 **측정인지 적합인지** 여기서만 확인된다 · 37호: 복합양극 모델 **이중층 항의 조상** — `c_dl` 이 면적에 비례하는가 (37호 `c_dl` 은 면적 무관 전극 상수 → R·C 처방 전제가 truth 에서 거짓) |
| ★★★ | **Danilov·Niessen·Notten 2011** — *J. Electrochem. Soc.* **158**(3), A215 | 12 · 26 | **2** | **Q4** | 이 모델 계보의 원형 — 파라미터 추정을 한 기계론 모델 (12호 [61] 재인용 · 26호 [15]) |
| ★★★ | **Firouz·Goutam·Soult·…·Van den Bossche 2020** — *J. Energy Storage* **28**, 101184 | 26 | 1 | **Q4** | 26호 인용 24편 중 **유일하게 제목에 "system identification"** 이 있는 ASSB 논문 (경험 모델) — **구조적 공백 1번 후보** |
| ★★ | **Kim·Lin·Abbasalinejad·Kim·Chung 2019** — *Electrochim. Acta* **317**, 663 | 12 · 37 | **2** | **Q4** | 같은 Danilov 모델 위의 **상태추정** — 12호가 Q4 후보로 지목했는데 26호는 인용하지 않는다. **구조적 공백 1번 후보** · 37호: ASSB 상태 추정기가 접촉·용량 손잡이를 어떻게 두는가 |
| ★★ | **Deng·Hu·Lin·Xu·Li·Guo 2021** — *IEEE Trans. Transp. Electrif.* **7**(2), 464 | 26 · 37 | **2** | Q4 | 축약 ASSB 모델 — 식별 대상이 되는 형태. 식별성을 다루는지 미확인 (공백 1번 후보) · 37호: 축약 모델이 θ 를 ε_p 와 **따로** 두는가 |
| ★★★ | **Bielefeld 2023** — *Batteries & Supercaps* **6**(9), e202300180 | 26 · 27 | **2** | Q4 | 1호 저자의 모델 방법론 의견 ("plea for simplicity") |
| ★ | **Danilov·Notten 2008** — *Electrochim. Acta* **53**, 5569 | 26 | 1 | 모델 | 해리 전해질 수송(이온+공공) 원전 — "SE 에 농도 구배" 가정의 출처 |
| ★ | **Xie·Imanishi·…·Yamamoto 2008** — *Solid State Ionics* **179**, 362 | 26 | 1 | Q3 | LCO 박막 확산계수를 GITT·EIS 로 **측정** — 적합된 `D_M⊕` 의 독립 대조 |
| ★ | **Shao·Shao·Sang·Liu 2022** — *J. Electrochem. Soc.* **169**, 080529 | 26 | 1 | Q1 | 12호가 재인용한 "Shao — 접촉 면적 파라미터" 와 같은 편인지 **미확인** |
| ★ | **Ansah·Shin·Lee·Cho 2021** — *Electron. Mater. Lett.* **17**, 532 | 26 | 1 | Q4 | 같은 "sensitivity = sweep" 관행의 표본 |
| ★★★ | **Schmidt·Sinzig·Wall 2024** — *J. Electrochem. Soc.* **171**, 100502 | 27 | 1 | **Q1** | resolved 모델의 **박리 = 접촉 손실 기구**. 27호가 재 보인 **P2D 대비 상수 오프셋 0.07 이 바로 비연결 입자 몫 `1−u`** 였다 — 그 기구의 모델 원전 |
| ★★★ | **Khalik·Donkers·Sturm·Bergveld 2021** — *J. Power Sources* **499**, 229901 | 27 | 1 | **Q4** | "P2D 파라미터를 실험에 맞춘다" 의 두 인용 중 하나 — DFN **파라미터 그룹화** 도구 후보 (공백 1번 후보, 액체셀) |
| ★★★ | **Lu·Trimboli·Fan·Wang·Plett 2022** — *J. Electrochem. Soc.* **169**, 080504 | 27 | 1 | **Q4** | 같은 문장의 두 번째 인용 — **집약(lumped) 파라미터 추정** (공백 1번 후보) |
| ★★★ | **Koerver 외 2018** — *Energy Environ. Sci.* **11**, 2142 | 27 · 33 | **2** | Q1·Q6·Q8·DEM | NMC 부피 변화 **측정** — 23호가 정량 원전이 아니었던 자리의 후속. ⚠ 큐 22 Koerver 2017 *Chem. Mater.* 와 **다른 논문**. 33호: 부피 곡선 + 압력 추적 + 제조 445 / 운전 70 MPa — DEM 입자 부피 변화 입력 후보 |
| ★★ | **Ramadesigan 외 2012** — *J. Electrochem. Soc.* **159**, R31 | 27 | 1 | Q4 | 시스템 공학 리뷰 — 파라미터 추정·불확실성 |
| ★★ | **Krewer 외 2018** — *J. Electrochem. Soc.* **165**, A3656 | 27 | 1 | Q4 | 진단용 동역학 모델 리뷰 — 파라미터화 |
| ★★ | **Kirk·Please·Chapman 2021** — *J. Electrochem. Soc.* **168**, 060554 | 27 | 1 | Q4 | P2D 에 **입자 크기 분포** — 27호의 `D/d²` (개수평균 vs d₄₃ 로 ≈3.5배) 교정 수단 |
| ★ | **Goldin 외 2012** — *Electrochim. Acta* **64**, 118 | 27 | 1 | Q1·Q3 | 3D 로 Bruggeman 을 평가한 원전 |
| ★ | **Neumann 외 2020** — *ACS Appl. Mater. Interfaces* **12**, 9277 | 27 | 1 | Q3·Q8 | NMC622 `D(χ)`·`σ(χ)` 출처 · sandwich 리튬화 |
| ★ | **Kremer 외 2020** — *Energy Technol.* **8**, 1900167 | 27 | 1 | Q8 | NMC622 OCV 출처 |
| ★ | **An·Zhou·Li 2021** — *Electrochim. Acta* **370**, 137775 · **A. Schmidt 외 2021** — *Energy Technol.* **9** | 27 | 1 | Q3 | P2D 적합성 비판 계보 |
| ★ | **Wirthl 외 2023** — *IJNMBE* **39** · **Saltelli 외 2010** — *Comput. Phys. Commun.* **181**, 259 · **Sobol 2001** — *Math. Comput. Simul.* **55**, 271 | 27 | 1 | Q4 방법 | GP+Sobol 방법·추정기·지수의 원전 — 27호의 대리모형 검증·CI 출처 공백 |
| ★★★ | **Forman·Moura·Stein·Fathy 2012** — *J. Power Sources* **210**, 263 | 28 | 1 | **Q4** | DFN(P2D) 에 **Fisher 식별성을 수치로** 잰 원전 — 28호(Bizeray)에 없는 정량 도구(FIM·신뢰구간). ASSB P2D(9·26·27호)로 옮길 후보 (공백 1번 도구, 액체셀) |
| ★★ | **Alavi·Mahdi·Payne·Howey 2016** — arXiv 1505.00153 | 28 | 1 | Q4·Q2 | Randles 등가회로의 식별성 — 16~25호 등가회로 적합에 걸 도구. 28호 방법이 **버리는 고주파 반원을 버리지 않는** 판 (곱 축퇴 처방 1단계가 여기서 산다) |
| ★★ | **Santhanagopalan·Guo·White 2007** — *J. Electrochem. Soc.* **154**, A198 | 28 | 1 | Q4 | 모델 판별 — 27호의 '모델 적합성' 을 식별성 언어로 잇는 원전 |
| ★ | **McTurk 외 2015** — *ECS Electrochem. Lett.* **4**, A145 | 28 | 1 | Q5 | 액체셀 선형 기준극 — Q5 기준극 계보의 액체 쪽 뿌리 |
| ★★★★ | **Yanev 외 2024 의 SI** (Table S2 · Fig. S1 · S6) — *J. Electrochem. Soc.* **171**, 050530 부록 | 29 | 1 | **Q4**·Q8 | **Q4 ASSB 첫 반 칸의 근거 수치 자체**. 본문은 "high dependencies close to unity in Table S2" 라고만 인쇄 — 값을 봐야 반 칸을 **확정하거나 접는다**. S6 = 형성 곡선. 본문은 받았고 SI 만 없음 (IOP 직접 접근은 프록시에서 막힘 → **사용자 업로드 필요**) |
| ★★★ | **Tian 외 2020** — *J. Power Sources* **468**, 228220 | 29 | 1 | Q4·Q2 | 29호 식 (2) `Q(R)=Q_M/(1+2(Rα)ⁿ)` 와 **`n` 배정(0.5=확산 / 1=저항)의 원전** — TLM 전송선의 √t 거동(같은 `n`≈0.5)을 대안으로 다뤘는지 확인해야 `n`≈0.5=고체 확산 배정이 가정인지 판정된다 |
| ★★★ | **Yanev 외 2022** — *J. Electrochem. Soc.* **169**, 090519 | 29 | 1 | Q1·Q4 | 같은 율 외삽 방법의 **ASSB 첫 판** · "균열 입자 이탈" 서술의 출처 (접촉 손실 서술의 원전 후보) |
| ★★ | **Kaiser 외 2018** — *J. Power Sources* **396**, 175 | 29 · 48 · 50 | **3** | Q3 | 굴곡도 식 `τ=σ₀ε/σ_eff` 와 TLM — 16호 Roling 계보. (TLM 원전 Minnmann 2021 과 짝) |
| ★★★ | **Ruess 외 2020** — *J. Electrochem. Soc.* **167**, 100532 | 29 · 38 | **2** | Q1·Q5·Q8 | NCM 균열과 GITT, 액체 vs 고체 비교 — 큐 37(Conforto)과 같은 공저 계열 · 38호: `D` · ∂E/∂x = 0.38 V · OCP 표류 그림의 출처 — 38호 활성 질량 채널의 기준 곡선 |
| ★★★ | **Nomura 외 2019** — *Angew. Chem.* **131**, 5346 | 30 | 1 | Q5 | 30호가 전류 방향 비대칭을 LATP/NMC 공간전하층에 배정한 근거의 **유일한 실측 원전** — 30호는 인용만 했고, 상대극 Li 석출↔박리 비대칭은 한 번도 다루지 않았다 (Q5 12번째 형태 '방향 비대칭의 일방 배정') |
| ★★ | **Yu·…·Wagemaker 2017** — *Nat. Commun.* **8**, 1086 | 30 | 1 | Q2 | 계면 수송과 벌크 수송을 **따로 재는** 방법(교환 NMR) — 2전극 배정 문제를 우회하는 측정 |
| ★ | **Lee·Park 2024** — *J. Phys. Chem. Lett.* **15**, 7095 | 30 | 1 | 방법 | 30호 저자의 b 값·Dunn 분해 절차 원판 (30호는 인쇄된 b 배정이 자기 Fig. 3 과 반대) |
| ★★★ | **Geng·Chien·Lacey·Thiringer·Brandell 2022** — *Electrochim. Acta* **404**, 139727 | 31 | 1 | Q4·곱 | 31호 그룹의 '`D` 추정 타당성' 편 — 면적 `A` 를 **변수로** 다뤘는지가 곱 `D·A²` 를 가르는 첫 확인처 (31호 ICI 는 BET 고정 = 같은 곱의 세 번째 배정, 처음으로 '고지된' 배정) |
| ★★★ | **Chouchane·Primo·Franco 2020** — *J. Phys. Chem. Lett.* **11**, 2775 | 31 | 1 | 곱 `D·A²` | GITT `D` 가 두 자릿수 흩어진다는 주장의 출처 — 3D 모델로 **유효 면적 효과**를 봄. 29·30·31호가 모두 입력으로 둔 `A` 를 모델로 다룬 유일한 후보 |
| ★★ | **Xu 외 2021** — *Nat. Mater.* **20**, 84 | 31 | 1 | Q1·LAM | fatigued 상 = 고 SOC 에서 **참여하지 않는 분율** — LAM 형 `u` 기구 (31호 해석: GITT/ICI `D_app` 은 통째 비연결 `u` 에 불변, 표면 피복 `φ` 에는 제곱) |
| ★ | **Chien 외 2020** — *JACS* **142**, 1449 | 31 | 1 | Q2 | `k ∝ Warburg` 의 다공 전극 유도 원전 |
| ★★ | **Celen 외 2021** — IEEE SysCon (DC-IR 데이터로 ASSB 등가회로) | 32 | 1 | BMS | 32호 종설 인용 160편 중 **유일한 ASSB BMS 모델 1차 원전** (종설은 재료 수치 출처로만 인용) |
| ★★ | **Kan 외 2024** — *Energy Storage Mater.* **68** (SSB 온도별 열 효과) | 32 | 1 | 온도 | 온도 의존·활성화 에너지 최선 후보 (종설) — 곱 축퇴 처방 2단계 '온도' 채널, 계보에서 거의 0 |
| ★ | **Wu 외 2021** — *InfoMat* **3** · **Diallo 외 2024** — *Nat. Commun.* **15**, 858 · **Charbonnel 외 2022** — *ACS AEM* **5** | 32 | 1 | 안전·Q6·Q2 | 32호 §5 실제 출처(안전) · 펠릿 밀도→파괴 · 열 남용 하 in-situ X선 — 모두 우선순위 낮음 |
| ★★ | **Gao·…·Bruce 2022** — *Joule* **6**, 636 | 33 | 1 | Q1·Q6 | 2 MPa 고정 · 컷오프로 **부피 변화 ↔ 감쇠**를 본 1차 자료 — `θ` 를 쟀는지 확인 필요 (33호 Fig. 7B 원전: 감쇠를 바꾼 변수는 압력이 아니라 양극 부피 변화 6→2.5 %) |
| ★★ | **Cronau·…·Roling 2021** — *ACS Energy Lett.* **6**, 3072 | 33 | 1 | DEM | SE 압분 전도도 — DEM SE 층 보정 목표 후보 |
| ★ | **Xu·Zhu·…·Li·Yang 2023** — *Adv. Mater.* **35**, 2212111 | 33 | 1 | Q6 | Xu 2024 그룹의 0.1–0.2 MPa 1차 자료 — "<1 MPa" 요구치의 배경일 수 있다는 가설 |
| ★ | **Ji 외 2022 · Han 외 2021** (스택 응력 응답) | 33 | 1 | DEM | 33호가 짚은 스택 응력 응답 원전 후보 — 서지 미확정 (33호 digest 참조) |
| ★★ | **Jiang·Tao·Lee·Moura 2026** — *Joule* **10**, 102342 ("Defining an accuracy limit in battery state estimation") | 34 | 1 | Q4 | CRLB 로 추정 정확도 한계를 정의한 원전 후보 — 34호는 FIM·CRLB·D-optimality 를 처방으로 인쇄하나 계산 0. ⚠ 곱 `A·j₀` 로만 의존하면 FIM 이 특이 — 그 경우를 다루는지 확인 (액체셀일 가능성 → 도구 칸) |
| ★★ | **Li·West·Preindl 2023** — *J. Power Sources* **580**, 233328 ("Characterizing degradation … with pulsing") | 34 | 1 | Q2·Q4 | 펄스로 **열화 모드 분해**를 하는지 확인 필요 — 처방 1·4단계의 온보드판 1차 후보 |
| ★★ | **Tang 외 2023** — *iScience* **26**, 106821 (10 s 펄스 · 10 Hz 샘플링 → 임피던스 예측) | 34 | 1 | 처방 1단계 | 재구성 EIS 의 `C` 가 **측정인지 학습 사전인지** — 나이퀴스트 5 Hz 로 계면 대역 10⁰–10³ Hz 중 ≈2.3 자릿수는 사전이 채움 |
| ★ | **Yang 외 2024** — *Science* **386**, 322 (Si 음극, 과도 펄스로 용량 회복) | 34 | 1 | Q2 조작 | 접촉 복원 조작 → 용량 회복 — 4호 재가압과 같은 부류 (단 액체 Si) |
| ★ | **Tao 외 2025** — *Energy Environ. Sci.* **18**, 1544 ("degradation pattern decoupling") | 34 | 1 | Q2·Q3 | 모드 분해인지 확인 |
| ★★ | **Birkl 2017** — 옥스퍼드 박사논문 (Oxford 셀 열화 데이터) | 35 | 1 | Q3 연결 | 35호 Group III 원 데이터 — **모드 분해(LLI/LAM)를 한 셀과 같은 셀일 가능성**. 맞으면 같은 셀 위에 '용량 스칼라 ML' 과 '모드 분해' 가 나란히 있는 유일한 대조 |
| ★ | **Kuleshov 외 2018** — ICML (calibrated regression) | 35 | 1 | Q3 도구 | 35호 isotonic 재보정의 원전 |
| ★ | **Richardson 외 2018** — *IEEE TII* (GPR) | 35 | 1 | Q3 | 같은 Oxford 데이터의 직접 비교 대상 |
| ★ | **Saxena 외 2008** — prognostics metrics | 35 | 1 | 어휘 | α-accuracy·β 의 원 정의 — 우리 전극 α·β 와 **이름 충돌**의 근원 |
| ★★★ | **Gasper·Gering·Dufek·Smith 2021** — *J. Electrochem. Soc.* **168**, 020502 | 36 | 1 | **Q4 도구** | 36호 종설에서 **파라미터 폭**을 다룬 유일한 자리 — 부트스트랩 파라미터 분포가 조건 누락·파라미터 과다 시 넓어짐. 우리 근최적 폭과 **같은 종류의 대상** (수명 모델 계수, 액체셀) |
| ★★★ | **Thelen 외 2022** — *Energy Storage Mater.* **50**, 668 | 36 | 1 | Q3·**Q4** | 36호 저자들의 모드 진단 원전 — **확률적 모드 진단의 가장 가까운 후보** (확률 출력 여부 미확인) |
| ★★ | **Ruan·Chen·Ai·Wu 2022** — *Energy AI* **9**, 100158 | 36 | 1 | Q4·22p | "모드가 본래 상관돼 정확도가 오른다" — **학습 사전의 상관이 비식별을 가리는지** 확인할 곳 (사후 상관이 아님) |
| ★★ | **Schmitt·Rehm·Karger·Jossen 2023** — *J. Energy Storage* **59**, 106517 | 36 | 1 | Q4·하네스 | 부분 창(20–70 % SOC) 모드 추정 — 하네스의 '창 하나' 하한 물음과 같은 물음 |
| ★★ | **Gasper·Collath·Hesse·Jossen·Smith 2022** — *J. Electrochem. Soc.* **169**, 080518 | 36 | 1 | Q4 도구 | 파라미터 분포 → 궤적 퍼짐 |
| ★★ | **Dubarry 외 2017** — *J. Power Sources* **360**, 59 | 36 | 1 | Q4 | OCV 데이터베이스 매칭 — **다중 해**를 보고하는지 |
| ★ | **Costa·Sánchez·Anseán·Dubarry 2022** — *J. Energy Storage* **55**, 105558 · **Tian·Xiong·Shen·Sun 2021** — *Energy Storage Mater.* **37**, 283 · **Lui 외 2021** — *J. Power Sources* **485**, 229327 · **Li 외 2021** — *J. Power Sources* **506**, 230034 | 36 | 1 | Q3·Q4 | 모드 진단 원전 (점 추정으로 소개됨) — '2 % error' 의 대상 · 부분 충전 OCV 재구성 · 'rough estimates' 크기 · 전극 수준 PINN |
| ★ | **Pannala 외 2024** — *J. Electrochem. Soc.* **171**, 010532 · **Prosser·Offer·Patel 2021** — *J. Electrochem. Soc.* **168**, 030532 | 36 | 1 | Q2 도구 | 두께 · 발열 — 전기 밖 독립 관측 채널 |
| ★ | **Nemani 외 2023** — *MSSP* **205**, 110796 · **Der Kiureghian·Ditlevsen 2009** — *Struct. Saf.* **31**, 105 | 36 | 1 | 어휘 | UQ 튜토리얼 · aleatory/epistemic 분류 원전 |
| ★ | **Froboese 외 2019** — *J. Electrochem. Soc.* **166**, A318 | 37 | 1 | Q3 (24호 τ/τ²) | brug 3.67 출처 — 37호 `D^p_SE` 역산 brug ≈1.52 와 대조 |
| ★★★ | **Bartsch 외 2019** — *Chem. Commun.* **55**, 11223 | 38 | 1 | **Q1**·Q2 | operando XRD 활성 질량 — 38호의 OCV 2점 활성 질량과 **같은 양을 OCV 와 독립으로** 잰 것. 38호 1 h 이완이 부족(자기 τ=L²/D 로 13–17 h)해 동역학 손실이 질량 채널로 새는 편향의 크기를 잴 수 있다 |
| ★★ | **Fantin 외 2021** — *Chem. Mater.* **33**, 2624 | 38 | 1 | Q1 (θ 전용 조작) | 단결정 분리·750 °C O₂ 재소성 절차 — 38호 SC↔PC 대조가 **θ 만 바꾸는 조작인지** 판정 |
| ★★ | **Lin 외 2014** — *Nat. Commun.* **5**, 3529 | 38 | 1 | Q1 배정 | 38호가 상전이 LAM 을 "낮다" 고 기각한 **유일한 근거** (액체셀 TEM) — 이것이 무너지면 38호 활성 질량 손실 전부를 접촉 손실로 읽은 배정도 무너진다 |
| ★ | **Schönleber·Ivers-Tiffée 2015 · Schönleber 외 2017** | 38 | 1 | Q4 | 미분 용량 분포(EIS-PSD) 방법 원전 — 크기 분포 역산의 식별성 |
| ★★★ | **Conforto 외 2021 의 SI** (Fig. S3 · S8 · S9) — *J. Electrochem. Soc.* **168**, 070546 부록 | 38 | 1 | Q1·Q2 | 활성 질량 절차(S3) · 적합 오차(S8) · Fig. 9 폐합 구성(S9) — 38호 Q2 +0.5 의 두 채널 결합 정도와 어긋남 D2·D4 를 가름. 본문만 받음 → **사용자 업로드 필요** |
| ★★★ | **Wang·Kazyak·Dasgupta·Sakamoto 2021** — *Joule* **5**, 1371 | 39 | 1 | **Q6** | 39호가 "**1 MPa practically**" 의 근거로 단 ref 22 — 계보가 모은 산업 운전 압력 요구치(≈1·0.4–1·2·5 MPa + 39호) **여섯 인쇄값 중 원전이 처음 지목된 편** (33호: 요구치 계보 5편·원전 0) |
| ★★ | **Ohashi·Kodama·Sun·Hori·Suzuki·Kanno·Hirai 2020** — *J. Power Sources* **470**, 228437 | 39 | 1 | Q1·Q6·DEM | "압력 변형이 AM–SE 접촉을 줄인다" 기구 서술의 근거 |
| ★★ | **Fathiannasab·Zhu·Chen 2021** — *J. Power Sources* **483**, 229028 | 39 | 1 | Q1·Q6 | CT 로 본 압력 변형·접촉 — Sakka 와 같은 측정 종류의 두 번째 후보 |
| ★ | **Ohashi·Kodama·Horikawa·Hirai 2021** — *J. Power Sources* **483**, 229212 | 39 | 1 | DEM | Young 률 차이에 따른 압분 · CT — DEM 압분 보정 |
| ★ | **Doux 외 2020** — *J. Mater. Chem. A* **8**, 5049 | 39 | 1 | Q6 | 제조 압력 50 ↔ 150 MPa 용량 비교. ⚠ 5호 Doux 2020 *AEM* 과 **다른 논문** |
| ★★★ | **Costard·Ender·Weiss·Ivers-Tiffée 2017** — *J. Electrochem. Soc.* **164**, A80 | 40 · 48 | **2** | **Q5**·Q2 | 40호(Ikezawa) **1.55 V 의 유일한 근거**이자 메시형 기준극 위치 선택의 근거 — 거기서 1.55 V 가 측정인지 인용인지가 R-LTO 가지 전체를 정한다. 1.55 V 수입 경로가 세 갈래(23호 Zaghib 1999 · 40호 Costard 2017 · 18호 Colbow 1989/Ohzuku 1995)이고 ASSB 안에서 Li 대비로 잰 적은 0 |
| ★★ | **Ender·Illig·Ivers-Tiffée 2017** — *J. Electrochem. Soc.* **164**, A71 | 40 · 48 | **2** | Q2 | 메시형 기준극 위치 artifact 이론 — "합을 보존하며 임피던스를 재분배" 논리의 원전 후보 (40호: 2전극 적합이 LCO R2 ×2.7 · R3 ×1.67 과대). ⚠ 큐 52 Illig 2012 와 **다른 논문** |
| ★ | **Braun·Uhlmann·Weiss·Weber·Ivers-Tiffée 2018** — *J. Power Sources* **393**, 119 | 40 · 45 | **2** | Q2·곱 | 복합전극에서 이온 수송·전하이동 결합 — R3 '비최적 적합' 의 설명 |
| ★ | **Chechirlian 외 1990** — *Electrochim. Acta* **35**, 1125 | 40 | 1 | Q2 | 1 MHz 이상 편차 = 기준극 artifact 근거 |
| ★★★ | **Jung·Lee·Kim·Kwon·Oh 2008** — *Adv. Funct. Mater.* **18**, 3010 | 41 | 1 | **Q5** | 41호(Nam 2018) 본문 **0.62 V 의 유일한 근거** — 그동안 In 가지 '출생지' 로 적던 Santhosha 2019 보다 1 년 이르다. 23호의 0.6 V 근거(Jung 2015)와 같은 연구실 — In 가지 0.6/0.62 V 는 두 경로로 이 연구실에 닿는다 |
| ★★ | **Yu·Bates·Jellison·Hart 1997** — *J. Electrochem. Soc.* **144**, 524 | 20 · 41 | **2** | Q5 | 박막 ASSB 의 **Li 금속 기준극 3전극** — 20호도 인용 |
| ★ | **Uhlmann·Illig·…·Ivers-Tiffée 2015** — *J. Power Sources* **279**, 428 | 41 | 1 | Q7 인접 | Li 도금 인용. ⚠ 큐 52 Illig 2012 와 **다른 논문** |
| ★★★ | **Takada·Aotani·Iwamoto·Kondo 1996** — *Solid State Ionics* **86–88**, 877 | 20 · 42 | **2** | **Q5** | "about 0.6 V over a wide stoichiometry range" 의 근거 — **ASSB 쪽 0.6 V 뿌리 후보** (20호 [20] · 42호 [18]). 42호 원전(액체셀)보다 앞선 고체 쪽 측정인지 확인 |
| ★★ | **Webb·Baggetto·Bridges·Veith 2014** — *J. Power Sources* **248**, 1105 | 42 | 1 | Q5 | 실온 In 리튬화의 다른 측정(스퍼터 박막, 탄산염+FEC) — 42호 값의 유일한 실온 대조 |
| ★ | **Wen·Huggins 1980** — *Mater. Res. Bull.* **15**, 1225 · **Sangster·Pelton 1991** — *J. Phase Equilib.* **12**, 37 | 42 | 1 | Q5 | 415 °C 0.5 V (실온 이전 유일한 열역학 측정) · In–Li 상도 원전 후보 |
| ★ | **Wenzel·…·Janek 2016** — *Chem. Mater.* **28**, 2400 | 42 | 1 | Q5·Q7 | In–Li 를 쓰는 황화물 계면 연구 |
| ★★★ | **Kuratani·Sakuda·Takeuchi·Kobayashi 2020** — *ACS Appl. Energy Mater.* **3**, 5472 | 43 | 1 | **Q1 (음극)** | 황화물 ASSB 흑연의 **void 형성 기구** — 음극 쪽 `θ(N)` 후보. 43호가 연 음극 판 곱 축퇴 `(1−LAM_NE)(1−u)` 를 가를 1순위 |
| ★★ | **Park·Song·Choi·Jin·Lim 2014** — *Jpn. J. Appl. Phys.* **53**, 08NK02 | 44 | 1 | G1·20호 | 44호가 Li-Si XRD·SEM·밀링 후 입도를 전부 위임한 자기 선행 연구 — 20호 음극 2차 밀링 여부·**용량 분모(TiS₂?)** 확인처 |
| ★★★ | **Bach·…·Renner 2015** — *Electrochim. Acta* **164**, 81 | 45 · 47 | **2** | Q5 | Au–Li 평탄 간격 134/215 mV 의 측정 원전 — 45호 기준극 계단 크기의 근거 · 47호: 칸 값 두 표(0.3/0.2 ↔ 0.215/0.134 V)의 **공통 원전** |
| ★★★ | **Kasemchainan·…·Bruce 2019** — *Nat. Mater.* **18**, 1105 | 46 · 48 | **2** | Q7 | 임계 박리 전류 → void → 도금 시 덴드라이트 · 삼중 경계 도금 — 46호의 대화 상대 |
| ★★ | **Krauskopf·Hartmann·Zeier·Janek 2019** — *ACS Appl. Mater. Interfaces* **11**, 14463 | 46 | 1 | Q7·Q6 | 공공 과포화·void·압력 ↔ 비커스 경도 가정의 원전 (46호가 반박) |
| ★★ | **Bron·Roling·Dehnen 2017** — *J. Power Sources* **352**, 127 | 46 | 1 | 곱(음극) | 황화물\|Li 혼합 전도 계면층 임피던스 — 'chemical capacitance' 배정 근거 |
| ★ | **Wenzel·…·Janek 2018** — *Solid State Ionics* **318**, 102 · **Wang·Sakamoto 2018** — *J. Power Sources* **377**, 7 · **Xu·…·Greer 2017** — *PNAS* **114**, 57 | 46 | 1 | Q7·Q6 | 아지로다이트\|Li 계면층 성장 · Li 항복 2 MPa · 소규모 Li 항복 ≈200 MPa |
| ★ | **Klink·…·La Mantia 2012** — *Electrochem. Commun.* **22**, 120 | 45 | 1 | Q2·Q5 | 3전극 artifact — >10 kHz 편차·고주파 호 #1 원인 후보 |
| ★★ | **Ender·Weber·Ivers-Tiffée 2012** — *J. Electrochem. Soc.* **159**, A128 | 47 | 1 | Q2 | 기준극 **위치** 아티팩트 원전. ⚠ 40호 Ender 2017 (A71) 과 **다른 논문** |
| ★★ | **Marchini·…·Tarascon 2020** — *ACS Appl. Mater. Interfaces* **12**, 15145 | 48 | 1 | Q5·LLI | 순수 Li+In 금속 음극에서 첫 효율 <70 % — **상대극이 방전을 끊는** 표본 (2전극에서 Li 손실이 양극 용량 손실로 보이는 경로, 45호 LTO 사례와 같은 부류) |
| ★★★ | **Waag·Käbitz·Sauer 2013** — *Applied Energy* **102**, 885 | 20 · 49 | **2** | Q2·Q4 | **작도 규약("usual prescription")의 실제 원전** — 20호 [25] · 49호(Barai) ref 8. 20호 '분해는 적합이 아니라 작도' 판정의 뿌리 |
| ★★ | **Cronau·…·Roling 2020** — *Batteries & Supercaps* **3**, 611 | 50 | 1 | Q2·Q4 | **두께 가변 TLM 의 원형**과 극한식 — 50호 방법의 뿌리. ⚠ 33호 Cronau 2021 *ACS Energy Lett.* 과 **다른 논문** |
| ★★ | **Gaberscek·Moskon·Erjavec·Dominko·Jamnik 2008** — *Electrochem. Solid-State Lett.* **11**, A170 | 51 | 1 | Q2·처방 1단계 전제 | '집전체 접촉' 이름의 원전 — 그 호의 `C` 가 **비접촉 면적**에 앉는지(그렇다면 접촉이 늘 때 R·C 가 같이 줄어 1단계 'τ 보존 = 면적 변화' 규칙이 이 호에서 뒤집힘) 확인할 유일한 곳 |
| ★★ | **Oh·…·Choi 2024** — *Energy Storage Mater.* **71**, 103606 · **Oh·…·Choi 2023** — *Adv. Energy Mater.* **13**, 2301508 | 52 | 1 | Q6 | 같은 연구실(14·52호)의 앞선 **압력 편** 둘 — 52호에 없는 **압력 스윕**이 있을 수 있음 |
| ★★ | **Menkin·…·Grey 2024** — *Faraday Discuss.* **248**, 277 | 52 | 1 | Q7·CE 오염 | **연성 단락 병렬 저항 틀의 원전** — CE 결손을 누설로 읽는 근거 (41·52호) |
| ★ | **Chen·…·Li 2021** — *ACS Appl. Energy Mater.* **4**, 4879 · **Yan·…·Chen 2022** — *Adv. Energy Mater.* **12**, 2102283 | 52 | 1 | Q6 | '저압에서 void 자가 치유 불가' 근거 — 압력 창 아래 벽 |
| ★ | **Schmidt·…·Ivers-Tiffée 2011** — *J. Power Sources* **196**, 5342 · **Illig·…·Ivers-Tiffée 2010** — *ECS Trans.* **28**(30), 3 · **Levi·Aurbach 1997** — *J. Phys. Chem. B* **101**, 4630 | 51 | 1 | Q2·Q4 | 11호 대역 문장의 직접 출처 · 같은 방법 앞선 판(셀 간 재현성) · DRT 전 차감한 확산 모형(P1C 누설 경로) |
| ★ | **Hess·…·Cuniberti 2015** — *J. Power Sources* **299**, 156 · **Morasch·…·Suthar 2021** — *J. Electrochem. Soc.* **168**, 080519 | 50 | 1 | 곱·규약 | 50호 비교 기준(액체 LCO 0.4 A m⁻²)의 **면적 규약** · 액체 TLM 규약·CPE 근거 |
| ★ | **Widanage 외 2016** — *J. Power Sources* **324**, 61 · 70 · **Schweiger 외 2010** — *Sensors* **10**, 5604 · **Barai 외 2015** — *J. Power Sources* **280**, 74 · **Smith·Wang 2006** — *J. Power Sources* **161**, 628 | 49 | 1 | Q2·Q4 | 다중사인·LPM(대역 끝이 직렬 R 을 정하는 구조) · 교차 방법 비교 선행 · 이완이 EIS 에 미치는 영향(4 h 휴지 근거) · `R_p` 창의 확산 물리 |
| ★ | **Bach·…·Renner 2016** — *Chem. Mater.* **28**, 2941 · **Dees·Jansen·Abraham 2007** — *J. Power Sources* **174**, 1001 · **Victoria·Ramanathan 2011** — *Electrochim. Acta* **56**, 2606 | 47 | 1 | Q5·Q2 | Au–Li 준안정상 명명 · 미세 기준극 크기/간격 조건 · 표류 문턱 모사 |
| ★★ | **Liu·…·Wu 2005** — *J. Power Sources* **140**, 149 | 20 · 44 | **2** | Q2 | "탈합금화가 합금화보다 빠르다" 의 유일한 근거(20·44호 모두) — 액체셀인지 확인. 44호 Li 수지 위반의 저자 설명 |
| ★ | **Shen·Cao·Rahn·Yang 2013** — *J. Electrochem. Soc.* **160**, A1842 · **Hayashi·…·Minami 2001** — *J. Am. Ceram. Soc.* **84**, 477 · **Asl·Keith·Lim·Zhu·Kim 2012** — *Electrochim. Acta* **79**, 8 | 44 | 1 | 곱·G2·Q6 | GITT 식 원전(m_B·S 정의) · σ 1.8×10⁻⁴ 대조 원전 · '벌크 ASSB 성능이 축 압력에 좌우' 근거 |
| ★★ | **Lee·…·Ahn 2022** — *ACS Appl. Energy Mater.* **5**, 5227 | 43 | 1 | Q6·Q2 | 탄소계 복합음극의 **스택 압력 crack healing** — 압력 되돌림 처방의 음극 판 |
| ★ | **Otoyama·…·Tatsumisago 2018** — *Solid State Ionics* **323**, 123 · **Höltschi·…·Novák 2020** — *J. Electrochem. Soc.* **167**, 110558 · **Yu·…·Fukutsuka 2022** — *Electrochemistry* **90**, 037003 | 43 | 1 | Q1·Q2·3-a | 흑연 복합음극 광학 관찰 · 리튬화 흑연↔황화물 반응성(R_X 화학) · 흑연\|Li₂S–P₂S₅ 계면 동역학(R_CT Ea 대조) |

## 2. 구조적 공백 — "그 한 편" 이 아니라 **목록에 없는 종류**

| 공백 | 처음 지적 | 왜 |
|---|---|---|
| **역문제·식별성을 다루는 ASSB 논문** | 01·02 (6-3-b) | 흡수분이 전부 forward 전용이면 **Q4 는 원리적으로 안 채워진다**. 28호까지 Q4 **0/28**, **29호(Yanev 2024)에서 처음 +0.5** — 저자가 적합 공분산 진단을 돌려 `Q_M`·`α` 비식별을 명제로 인쇄(식별 집합에 용량 스케일 포함). 다만 가르는 축은 정적↔동적이지 LAM_PE↔접촉이 아니고, 진단 수치는 SI 에 있다. 이 공백이 그 숫자의 원인이다. ⚠ 26호(제목에 "sensitivity analysis")도 식별성이 아니라 **one-at-a-time 스윕**이었다 — 다만 그 스윕 그림에 비식별 방향 셋이 드러나 **원전 수치만으로 재현 가능한 첫 편**이 됐다. 후보: **Firouz 2020** (system identification) · **Kim 2019** (Danilov 모델 상태추정) · **Khalik 2021 · Lu 2022** (27호, 파라미터 그룹화·집약 추정) · Deng 2021 · Naik 2022 · **Forman 2012** (DFN Fisher 식별성, 28호). ⚠ 큐 27 Bizeray(28호)는 **식별성을 실제로 잰 계보 첫 편**이나 액체셀이고, 식별 집합 `(τ_d⁺, τ_d⁻, R_ct)` 에 **용량이 없다** — LAM·접촉 손실이 사는 `Q_th` 는 기준극 입력으로 가정. 도구는 있고 대상이 없다 (21번째 '0의 종류'). ⚠ 27호(전역 Sobol + CI)도 **설계 KPI 의 모델 적합성**이었지 식별성이 아니다 |
| **ASSB 의 pOCV / 저율 OCV 곡선** | 02 (6-3-b) | 02 의 전압축은 전부 1 mA/cm² 부하 곡선이고 **OCV 곡선은 0 편**이었다 |
| **기준극 누설·드리프트를 잰 ASSB 3전극 논문** | 20 | 계보 20/20 편이 누설을 안 쟀다. 3전극은 기준극 표류를 공통 모드로 상쇄해 **원리적으로 못 본다** (20호). ⚠ **절반 채워짐 (21호)**: 드리프트는 28일 < 3 mV 로 **쟀다** — 두 전극이 평탄 전위에 고정돼 표류가 보이는 구조였다. 그래서 20호 명제는 "**고정된 전극이 없으면** 못 본다" 로 좁혀졌다. **누설은 여전히 0/21** (21호도 간접 상한 < ~4.3 nA 만) |
| **확률적 열화 모드 진단 — LLI/LAM 사후 공분산을 인쇄한 논문** (액체셀이라도) | 36 | 36호 확률적 ML 종설이 모드 진단 원전 13편을 **전부 점 추정으로** 소개, 해당 절에 불확실성·사후·Bayes 낱말 0. 저자 문제 그림(Fig. 4)도 모드 진단만 불확실성 표시 없음. 사후 폭 = 우리 근최적 폭이 되려면 **공분산(곱 방향 능선)** 이 인쇄돼야 한다 — 평균장 VI·상관된 학습 사전은 그 능선을 지운다 (36호 인쇄 + 해석). 후보: **Thelen 2022 · Gasper 2021** · Ruan 2022 · Dubarry 2017 (다중 해) · 위키에 이미 있는 Navidi 2024 (co-kriging 사후 분산 — 재점검 후보) |

## 3. 큐 안 — 이미 받았다 (중복 요청 금지)

| 논문 | 지목 | 큐 |
|---|---|---|
| Sedlmeier 외 2023 — *JES* **170**, 030536 (μ-RE, In-Li) | 17 ("Li 박 방향 뒤집기 = 16↔17호 대질") | **20** (✅ 21호 `ac961cde`) |
| Koerver 외 2017 — *Chem. Mater.* 29, 5574 | 18 ("큐 22번 당기기") · 21 (ref 29) · 22 (ref 9, 본문 4회) | **22** (✅ 23호 `492c1ff1`) — ⚠ "접촉 손실의 **실험** 원전" 은 맞지만 **정량** 원전은 아니다 (틈 치수·분율·용량 몫 0) |
| Fukunishi 외 2023 — *JPS* 564 (NCM523 3전극) | 16 (ref 39) | 17 (✅ 18호) |
| Zhang·Fu·Lu·…·Wang·Sun 2025 — *Adv. Mater.* **37**, 2413499 (저압 종설) | 25 (짝으로 지목 — **인용은 아님**) · 32 (08 이 인용 — 32호 종설에 없는 압력 수치를 공급, `MPa` 50) | **32** (✅ 33호 `49261fd7`) — 제조/운전 압력은 **가른다**("고압 제조 · 저압 운전"), 압력↔θ↔감쇠 정량 1차 관계는 **0**. 양극 접촉 손실 유일 문단이 원전(23호 Koerver 2017)과 **반대로** 옮김. 25호와 상호 인용 불가(시점) |
| Bizeray·Kim·Duncan·Howey 2019 — *IEEE TCST* **27**(5), 1862 (SPM 식별성) | 26·27 (**둘 다 인용 0** — 식별성 방법론 원전인데 ASSB 모델 두 편이 안 가리킨다) | **27** (✅ 28호 `d238c9e9`) — 식별 집합에 용량 없음 → Q4 ASSB 0/28, 도구 칸만 |
| Park 2024 — *Materials* **17**, 5014 (저 담지량 NMC111 / LATP / Li 비대칭 동역학) | 29 (같은 '율 한계 분해' 축) | **29** (✅ 30호 `ff11fc66`) — 율 한계 분해 설계가 **아니었다** (동기 = 표면/부피비). 복합양극 없음 → θ 자리 없음 |
| ICI 확산계수 — *Nat. Commun.* 2023 (+SI) | 29 (GITT `D` 대체 방법 — 29호 `D_app ∝ 1/A²` 로 `D` 와 면적 못 가름) · 30 (Randles–Ševčík `D_app ∝ 1/(A·C)²` — 같은 곱을 29호와 **반대로** 배정) | **30** (✅ 31호 `30a4da89`) — **못 가른다**. 식 19 에 `A` 가 제곱 입력, BET 고정 → 같은 곱의 **세 번째 배정** (처음으로 저자가 면적 불확정을 고지하고 비교를 비로 한정 — 절대 주장에서 한정이 빠짐). 액체셀만 → 도구 칸 |
| Li 외 2024 — *eTransportation* **20**, 100315 (복합양극 ASSB 모델 원형) | 9 (원천 추적) · 27 (P2D 동어반복 경고) | **36** (✅ 37호 `73052033`) — 표면 접촉 `A_eff` 는 LAM 과 **다른** 손잡이이나 `k_p` 와 곱 `A_eff·k_p` 로만 → 접촉 손실 ≡ 계면 화학 열화 (식 수준 항등). 통째 비연결은 `ε_p` 뿐 = LAM_PE. 9호 `A_eff` 는 출처 없는 이식값, `R_s` 9.3 µm 는 자기 SEM(≈0.5–1.5 µm)과 불일치 |
| Conforto 외 2021 — *J. Electrochem. Soc.* **168**, 070546 (화학-기계 열화 정량) | 37호가 **Q1 정량 1순위**로 지목 (인용은 아님) | **37** (✅ 38호 `0db6cb77`) — 사이클별 **활성 질량**(OCV 2점) + 확산 경로 길이(EIS-PSD) 측정. 그러나 활성 질량 = θ·(1−LAM) **합성량** → θ(N) 여전히 0/38, '합성 계열 1/38'. **Q2 +0.5** (두 채널 분할, 설계상 결합) |

## 3-b. 보류 결정 — 추가 논문을 흡수한 뒤 사용자와 최종 확인 (2026-09-23 사용자 지시)

큐 20~37 흡수 뒤 추린 판단 11건. 사용자가 원장 목록을 받아 논문을 더 올려 주기로 했으므로, 판정은 **그 논문들을 흡수한 뒤** 한꺼번에 한다. 괄호 안은 판정에 직접 닿는 원장 항목이다.

| # | 결정 | 닿는 논문 |
|---|---|---|
| 가 | 29호 Q4 +0.5 유지 여부 (축이 LAM↔접촉이 아니라 정적↔동적) | Yanev 2024 SI (Table S2) · Tian 2020 · Yanev 2022 |
| 나 | 38호 Q2 +0.5 유지 여부 (두 채널이 설계상 결합) | Conforto SI (S3·S8·S9) · Bartsch 2019 |
| 다 | 28호 Bizeray(액체셀 도구)를 ASSB Q4 분모에 넣을지 | Forman 2012 · Khalik 2021 · Lu 2022 · Firouz 2020 |
| 라 | 32호 양극성 스택 → `ASSB_TRANSFER_NOTE` §2 제약으로 올릴지 | Celen 2021 |
| 마 | 37호 "ASSB truth 5조건" 개념 페이지 분리 여부 | Schmidt 2024 · Raijmakers 2020 · Deng 2021 |
| 바 | 33호 상대극 압력 진동 ≈ 운전 압력 → 압력 되돌림 분리 시험 설계 조건으로 | Sakka 2022 · Koerver 2018 *EES* · Gao 2022 |
| 사 | 21호 P12 조립 방향 메타데이터를 입력 요구로 격상 | Ikezawa 2020 · Nam 2018 |
| 아 | 35호 합성 쌍(PyBaMM) → Roman 특징 30개 재계산 여부 | Birkl 2017 |
| 자 | 31호 ICI zenodo R/k 면적 소거 검사 여부 | Geng 2022 · Chouchane 2020 |
| 차 | 23호 PyBaMM 면적 노브 / j₀ 노브 분리 forward 여부 | Orue Mendizabal 2023 |
| 카 | 요청 우선순위 (Ikezawa 2020 1순위? Sakka 2022 당김?) | — (업로드 순서가 곧 답) |
| 타 | Navidi 2024 digest 재점검 여부 | Thelen 2022 · Gasper 2021 |

## 4. 갱신 기록

| 날짜 | 기준 | 더한 것 |
|---|---|---|
| 2026-09-23 | 1~20호 | 씨앗 — `ASSB_TRANSFER_NOTE.md` §6 의 `후속 →` 절과 §6-3-b 에서 옮김 (큐 밖 17 · 구조적 공백 3 · 큐 안 3) |
| 2026-09-23 | 21호 (큐 20 Sedlmeier) | Ikezawa 4→5 · Nam 2→3 · Santhosha 2→3 · Hertle 에 Schlenker 2020 병합(2회) · 신규 Solchenbach 2016 · Dugas 2021 · Masias 2019 · 누설/드리프트 공백 **절반 채움** · Sedlmeier 흡수 완료 |
| 2026-09-23 | 22호 (큐 21 Strauss) | 신규 7 — Zhang 2017 *JMCA* (부피 수축→접촉) · Zhang 2017 *ACS AMI* (토모그래피·공극률) · Koerver 2017 *JMCA* (산화 계면층) · Nam 2018 *JPS* (≠ *JMCA*) · de Biasi/Kondrakov 2017 · Chen 2013. 큐 22 Koerver *Chem. Mater.* 지목 3회. 22호는 2018-03 게재라 Ikezawa·Nam *JMCA*·Santhosha·Sedlmeier 를 **인용할 수 없다** (지목 0 은 부재가 아니라 시점) |
| 2026-09-23 | 23호 (큐 22 Koerver) | Zhang 2017 *JMCA*·*ACS AMI* 각 2회 (후자는 23호 방법 원전으로 ★★★★ 승격) · 신규 5 — Kondrakov 2017 *JPCC* 121 3286 (NCM811 부피 수축 원전) · Zaghib 1999 (LTO 1.55 V 뿌리) · Jung 2015 (In 0.6 V 근거) · Ishidzu 2016 · Auvergniot 2017. 23호는 2017-06 게재라 Ikezawa·Nam·Santhosha·Koerver *JMCA* 인용 불가 (시점) |
| 2026-09-23 | 24호 (큐 23 Stavola) | Zhang 2017 *ACS AMI* 3회 · Bielefeld 2020 2회(★★★ 승격, 01↔24 유일 고리) · 신규 8 — Minnmann 2021 (TLM 원전, **Q4**) · Park 2021 *Nat. Mater.* (가짜 상분리) · **Naik 2022 (Q4 입구 후보)** · Davis 2021 · Shi 2020 *AEM* (≠ 4호) · Buchberger 2015 · Li Z 2020 · Okasinski 2020 |
| 2026-09-23 | 25호 (큐 24 Zhou) | ★ **Sakka 2022 *JMCA* 신규 최상위** (X선 CT 압력별 접촉 면적 — `θ(P)` 측정 후보) · Shi 2020 *AEM* 2회 · 신규 7 — Xu 2024 · Schlautmann 2023 · Jiao 2023 (DEM 직결) · Orue Mendizabal 2023 · Wang 2024 · Kim J.T. 2023 · Minnmann 2022 (≠ 2021) · 큐 32 저압 종설 짝 표시 |
| 2026-09-23 | 26호 (큐 25 Iwakiri) | Danilov 2011 2회 · 신규 9 — **Raijmakers 2020 (26호 데이터·문헌값의 단일 출처)** · **Firouz 2020 · Kim 2019 (Q4 공백 후보)** · Deng 2021 · Bielefeld 2023 · Danilov 2008 · Xie 2008 · Shao 2022 · Ansah 2021. 구조적 공백 1번에 후보 5 명시 |
| 2026-09-23 | 27호 (큐 26 Sinzig) | Bielefeld 2023 · Neumann 2021 각 2회 · 신규 14 — **Schmidt 2024 *JES* (박리 = 27호 상수 오프셋 0.07 의 기구)** · **Khalik 2021 · Lu 2022 (Q4 공백 후보)** · Koerver 2018 *EES* (≠ 2017) · Ramadesigan 2012 · Krewer 2018 · Kirk 2021 · Goldin 2012 · Neumann 2020 · Kremer 2020 · An 2021/Schmidt 2021 · Wirthl/Saltelli/Sobol (방법) |
| 2026-09-23 | 28호 (큐 27 Bizeray) | 신규 4 — **Forman 2012 (DFN Fisher 식별성, Q4 정량 도구)** · Alavi 2016 (Randles 식별성) · Santhanagopalan 2007 (모델 판별) · McTurk 2015 (액체 기준극). 구조적 공백 1번: Bizeray 흡수 뒤에도 **ASSB 대상 식별성 0/28** |
| 2026-09-23 | 29호 (큐 28 Yanev) | 신규 5 — ★ **Yanev 2024 SI (Q4 첫 반 칸의 근거 수치, 업로드 필요)** · Tian 2020 (식 (2)·`n` 배정 원전) · Yanev 2022 (방법 첫 판) · Kaiser 2018 · Ruess 2020. 큐 안 지목: 29 Park · 30 ICI. 구조적 공백 1번 **처음 반 칸 움직임** |
| 2026-09-23 | 30호 (큐 29 Park) | 신규 3 — **Nomura 2019 (공간전하층 실측 원전, Q5)** · Yu/Wagemaker 2017 (교환 NMR) · Lee·Park 2024 (방법 원판). 큐 30 ICI 지목 2회 (29·30호 모두 `D`·면적 곱을 못 가름) |
| 2026-09-23 | 31호 (큐 30 Chien ICI) | 신규 4 — **Geng 2022 (같은 그룹 D 추정 타당성 — A 를 변수로?)** · **Chouchane 2020 (유효 면적 3D 모델)** · Xu 2021 *Nat. Mater.* (fatigued 상 = u 기구) · Chien 2020 *JACS*. 곱 `D·A²` 는 29·30·31호 세 편 모두 못 가름 — **구조적 공백 후보**로 승격 검토(최종 정리) |
| 2026-09-23 | 32호 (큐 31 Biçer 종설) | Xu 2024 *AEM* 2회 · 신규 5 — Celen 2021 (유일한 ASSB BMS 모델 1차) · Kan 2024 (온도 채널) · Wu 2021 · Diallo 2024 · Charbonnel 2022 (저순위). 인용 160편 제목 전수 검토 → **Q1·Q4·곱 분리·기준극 누설 1차 후보 0**. ⚠ 08 이 이 종설에 귀속한 '접촉 손실 vs 일반 노화 분리 진단' 요구는 **원문에 없음** (`contact loss` 0회) — 그 요구의 첫 인쇄는 08 자신 |
| 2026-09-23 | 33호 (큐 32 Zhang 저압 종설) | **Sakka 2022 2회** (33호는 다른 명제로 인용) · **Xu 2024 *AEM* 3회 → ★★★** ("<≈1 MPa" 확인처가 원문뿐) · Koerver 2018 *EES* 2회 → ★★★ · Zhang 2017 *JMCA* 3회 · 신규 4 — Gao 2022 *Joule* · Cronau 2021 · Xu 2023 *Adv. Mater.* · Ji 2022/Han 2021. DEM 보정 목표 후보 표시(Sakka θ(P) · Cronau SE 압분 · Koerver 2018 부피). 큐 33–37 인용 0 |
| 2026-09-23 | 34호 (큐 33 Liang 펄스 BMS 논평) | 신규 5 — Jiang 2026 *Joule* (CRLB 정확도 한계) · **Li·West·Preindl 2023 (펄스 모드 분해 1차 후보)** · Tang 2023 (재구성 EIS) · Yang 2024 *Science* · Tao 2025 *EES*. 큐 34·35 인용 0. ⚠ 지문 정정: NFKC 뒤 34호 `identifiab` 0→3, 큐 35 `confidence interval` 0→6 |
| 2026-09-23 | 35호 (큐 34 Roman ML SOH) | 신규 4 — **Birkl 2017 (Group III 원 데이터 — 모드 분해한 셀과 같을 가능성)** · Kuleshov 2018 · Richardson 2018 · Saxena 2008 (α·β 이름 충돌). 큐 35·36·37 지목. ⚠ 8호 원장 정정: 보정된 불확실성 0/8 → **1/8** (35호), 0.45 % 는 RMSPE |
| 2026-09-23 | 36호 (큐 35 Thelen 확률적 ML 종설) | 신규 16 (9행) — **Gasper 2021 (파라미터 폭) · Thelen 2022 (확률적 모드 진단 최근접 후보)** · Ruan 2022 · Schmitt 2023 · Gasper 2022 · Dubarry 2017 · Costa 2022 · Tian 2021 · Lui 2021 · Li 2021 · Pannala 2024 · Prosser 2021 · Nemani 2023 · Der Kiureghian 2009. **구조적 공백 4번 신설: 확률적 모드 진단 (사후 공분산)**. 큐 36·37 인용 0. (36호 Fig. 3 의 원본 'Birkl 2017' 은 *JPS* 도식 논문일 가능성 — 35호 박사논문 행과 동일 여부 미확인이라 합산하지 않음) |
| 2026-09-23 | 37호 (큐 36 Li 복합양극 모델) | Raijmakers 2020 · Kim 2019 · Deng 2021 각 2회 · 신규 Froboese 2019. 큐 37 Conforto 를 Q1 정량 1순위로 지목. ★ ASSB truth 가 카드 물음을 시험하려면 필요한 5가지(ε_p 와 별개 θ · 비연결 입자가 Li 붙듦 · 죽은 부피 ≠ 전해질 · θ 전용 조작 · 면적 비례 이중층)가 37호 카드 새 제약에 기록됨 |
| 2026-09-23 | 38호 (큐 37 Conforto) — **큐 끝** | Ruess 2020 2회 → ★★★ · 신규 5행 — **Bartsch 2019 (operando XRD 활성 질량 — OCV 독립)** · Fantin 2021 (SC/PC 조작 순도) · Lin 2014 (상전이 LAM 기각의 유일 근거) · Schönleber 2015/2017 · **Conforto SI (업로드 필요)** |
| 2026-09-23 | 39호 (큐 40 Sakka — 2차 묶음 첫 편) | **Sakka ✅ 흡수** (θ(P) 후보 → 실제로는 φ(P) 제조 압력) · Zhang 2017 *ACS AMI* 4회 · Nam 2018 *JPS* 2회 · 신규 5 — **Wang 2021 *Joule* (요구치 원전 첫 지목)** · Ohashi 2020 · Fathiannasab 2021 · Ohashi 2021 · Doux 2020 *JMCA* (≠ 5호). ⚠ 25호 digest 의 "모델상 25 MPa 면 안정" 은 Sakka 에 없음 (Zhou 원문의 인용 번호 없는 문장이 붙은 것) — 컴파일 페이지에서 정정됨 |
| 2026-09-23 | 40호 (큐 41 Ikezawa) | **Ikezawa ✅ 흡수** + '110 Ω cm²' 정정 (원전 수치 아님, ≈2배 과대) · Nam 2018 *JMCA* 4회 · 신규 4 — **Costard 2017 (1.55 V 유일 근거)** · Ender 2017 (≠ Illig 2012) · Braun 2018 · Chechirlian 1990. 구조적 공백 3(누설·드리프트) 그대로 |
| 2026-09-23 | 41호 (큐 42 Nam 2018 *JMCA*) | **Nam ✅ 흡수** (Q5 +0.5 — SI 에서 기준극 교체 대조; 행 이름 'In-rich depletion' 정정) · Zhang 2017 *ACS AMI* 5회 · Jung 2015 2회 → ★★★ · 신규 3 — **Jung 2008 *AFM* (0.62 V 유일 근거)** · Yu 1997 (20호 인용 합산 2회) · Uhlmann 2015 (≠ Illig 2012) |
| 2026-09-23 | 42호 (큐 43 Santhosha) | **Santhosha ✅ 흡수** (Q5 +0.5 — 액체셀 Li 대비 측정, 평탄 창 ≈1–47 at%) · Zhang 2017 *ACS AMI* 6회 · Koerver 2017 *JMCA* 2회 · 신규 5 — **Takada 1996 (ASSB 쪽 0.6 V 뿌리 후보, 20호 인용 합산 2회)** · Webb 2014 · Wen–Huggins 1980 · Sangster–Pelton 1991 · Wenzel 2016 |
| 2026-09-23 | 43호 (큐 44 Fukunishi 2023 *ACS AEM*) | **Fukunishi ✅ 흡수** (Q5 +0.5 — R-LTO 첫 표류 값 ≈−14 mV 공통 모드; 음극 판 곱 축퇴 `(1−LAM_NE)(1−u)`) · 신규 5 — **Kuratani 2020 (음극 void → θ(N) 후보)** · Lee 2022 (음극 crack healing) · Otoyama 2018 · Höltschi 2020 · Yu 2022 |
| 2026-09-23 | 44호 (큐 45 Jin 2015) | **Jin ✅ 흡수** (새 칸 0 — 20호 공백 G1·G2 채움, G3 절반; 'effective contact area' 는 곱을 가정으로 쪼갠 값; Li-Si 평탄 아님) · 신규 5 — Park 2014 *JJAP* (용량 분모 확인처) · **Liu 2005 (20호 인용 합산 2회)** · Shen 2013 · Hayashi 2001 · Asl 2012 |
| 2026-09-23 | 45호 (큐 46 Hertle 2023) | **Hertle ✅ 흡수** (Q5 +0.5 — 셀 안 Li vs In/InLi −618 mV 측정 축 인쇄; 기준극 계단형 이탈·소모품; 21호 'Schlenker→Hertle' 계보 불지지) · Solchenbach 2016 2회 (큐 48) · Braun 2018 2회 · 신규 2 — Bach 2015 (Au–Li 평탄 간격 원전) · Klink 2012 |
| 2026-09-23 | 46호 (큐 47 Schlenker 2020) | **Schlenker ✅ 흡수 + Hertle 행에서 분리** (새 칸 0 — 기준극 썼으나 영점 없음; 계보 두 줄이 16호에서 만남; 연성 단락 배제 안 됨) · 신규 6 — **Kasemchainan 2019 *Nat. Mater.*** · Krauskopf 2019 · Bron 2017 · Wenzel 2018 · Wang–Sakamoto 2018 · Xu 2017 *PNAS* |
| 2026-09-23 | 47호 (큐 48 Solchenbach 2016) | **Solchenbach ✅ 흡수** (칸 0 — 액체셀 도구 칸; 0.31 V 는 Li 대비 직접 측정, 0.31 V↔0 V 는 같은 사다리 양 끝) + 행 문구 정정(이식은 ASSB 안에서) · Hertle 행에 '134/215 mV 원전에 없음' 병기 · Illig 2012 3회 · Bach 2015 2회 → ★★★ · 신규 4 — Ender 2012 (≠ 2017) · Bach 2016 · Dees 2007 · Victoria 2011 |
| 2026-09-23 | 48호 (큐 49 Dugas 2021) | **Dugas ✅ 흡수** + 행 문구 정정 2건 (기준극은 전면 복합층, 링은 집전체 · 저주파 호는 시간 단조 성장) · Q5 +0.5 (2전극 허용 조건 인쇄) · Costard 2017 · Ender 2017 · Kasemchainan 2019 · Kaiser 2018 각 2회 · 신규 Marchini 2020 |
| 2026-09-23 | 49호 (큐 50 Barai 2018) | **Barai ✅ 흡수** (칸 0 — 액체셀 도구 칸; 총저항 = 같은 양의 다른 창, 성분 = 창 경계 규약) + 행 문구 정정 ('작도법 원전' → 규약의 시간 척도 해석; 규약 출처는 Waag 2013) · 신규 — **Waag 2013 (20호 인용 합산 2회)** · Widanage 2016 · Schweiger 2010 · Barai 2015 · Smith–Wang 2006 |
| 2026-09-23 | 50호 (큐 51 Miß 2022) | **Miß ✅ 흡수** (칸 0 — j₀ 는 기하 면적 고정 뒤 남는 값, 16호 '접촉 면적 ≡ 1' 의 출생지, 면적 규약이 j₀ 를 τ 배 이동) · Kaiser 2018 3회 · Minnmann 2021 2회 · Bielefeld 2022 3회 (큐 57) · 신규 — Cronau 2020 *B&S* (≠ 2021) · Hess 2015 · Morasch 2021 |
| 2026-09-23 | 51호 (큐 52 Illig 2012) | **Illig ✅ 흡수** (칸 0 — 액체 LFP 도구 칸; 직렬 두 호 이름 가르기, 전자 접촉) + 행 문구 정정 ('θ↔j₀ 분리 원형' 아님) · 신규 — **Gaberscek 2008 (처방 1단계 전제 확인처)** · Schmidt 2011 · Illig 2010 · Levi–Aurbach 1997 |
| 2026-09-23 | 52호 (큐 53 Oh 2025 *AEM*) | **Oh ✅ 흡수** (칸 0 — 압력 두 점이 적재·N/P 와 교락; CE 결손이 Li 재고의 ≈2배 → Li 손실 아님) · 신규 — Oh 2024 *ESM* · Oh 2023 *AEM* (같은 연구실 압력 편) · **Menkin 2024 (연성 단락 틀 원전)** · Chen 2021 · Yan 2022 |
