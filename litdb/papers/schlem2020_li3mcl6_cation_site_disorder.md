# Mechanochemical Synthesis: A Tool to Tune Cation Site Disorder and Ionic Transport Properties of Li₃MCl₆ (M = Y, Er) Superionic Conductors — Schlem et al. (Adv. Energy Mater. 2020)

> slug `schlem2020_li3mcl6_cation_site_disorder` · DOI `10.1002/aenm.201903719` · type `exp + DFT 보조(정적 defect-model만)` · PDF `dbe52075-36._Mechanuctors.pdf` + SI `32a189c2-36._Sup_Meuctors.pdf` (inbox #36 본문 10 pp + SI 15 pp 전부 정독) · digested `2026-07-28` · status ✅
> elements: Cl, Y, Er
> methods: DFT
> **저자**: Roman Schlem, Sokseiha Muy, Nils Prinz, Ananya Banik, Yang Shao-Horn, Mirijam Zobel, **Wolfgang G. Zeier*** (JLU Giessen 물리화학·LaMa / MIT DMSE / Univ. Bayreuth) · *Adv. Energy Mater.* 2020, **10**, 1903719 · 접수 2019-11-12, online 2019-12-17 · **Open Access CC-BY**

---

## 0. 이 digest를 읽는 법 — ⚠⚠ 정체 확정 + repo 귀속 오류 판정 포함
- **정체 실물 확정**: 본문 1쪽에서 제목·저자·DOI 확인 — **AEM 10, 1903719 = 할라이드 Li₃MCl₆(M=Y,Er) 논문**이다. **argyrodite(Li₆PS₅X) 논문이 아니다.** LPSCl 데이터·수치가 이 논문에는 **한 줄도 없다**.
- **★특별 검증 결론 (요약)**: 우리 repo 전반(li_transport.json·세미나 원고·open_items #5)이 "Schlem 2020 AEM 10,1903719 = LPSCl ordered Ea 0.25 / Cl-rich 0.22 eV"로 인용해 왔으나, **그 수치는 이 DOI에 존재하지 않는다**(이 논문의 Ea는 Li₃ErCl₆ 0.41–0.49 / Li₃YCl₆ 0.45–0.49 eV). → **귀속 오류 확정. LPSCl 0.25/0.22의 원전은 별도 확보 필요.** 상세 §11b.
- 그 판정과 별개로, 이 논문 자체는 우리 **'무질서 = 공정변수(합성으로 조절되는 변수)'** 논지의 **가장 깨끗한 외부 정량 실증**이다: 같은 조성에서 합성 경로(볼밀 vs 어닐 1 min/1 h vs 앰풀 1주)만 바꿔 **양이온 자리무질서 2.5→88 %**를 연속 조절하고, 그에 따라 **σ 18×·Ea −0.08 eV**가 움직임을 XRD+PDF 이중 프로브로 보였다.

## 1. 한 줄 요약
Li₃ErCl₆/Li₃YCl₆(삼방 P3̄m1 할라이드 SE)에서 **합성 방법이 M2–M3 양이온 자리무질서를 결정**한다 — 볼밀(기계화학)은 거의 완전한 자리반전(~88–100 %), 후속 어닐은 시간에 따라 질서 회복(1 min 9.9 % → 1 h 7.6 %), 고전적 앰풀 합성은 최저(2.5 %) — 그리고 **무질서가 클수록 σ↑(1.7×10⁻⁵→3.1×10⁻⁴ S/cm)·Ea↓(0.49→0.41 eV)**. DFT(VASP, 정적)는 무질서 배열들이 질서 배열과 **에너지 등가(~1–2 meV/atom)**임을 보여 "무질서가 열역학이 아니라 **공정**으로 결정되는 변수"임을 뒷받침한다.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 물질 | **Li₃ErCl₆ (주)** + **Li₃YCl₆ (SI 보조)** — 이온반경 Er 89 / Y 90 pm(Shannon)으로 동구조 쌍. ⚠ 우리 [Cha]가 코팅으로 쓴 **LYC = Li₃YCl₆ 바로 그 물질** |
| 왜 halide | Li₃MX₆(M=Y,Er; X=Cl,Br) = 산화안정성 + σ ~1 mS/cm급으로 급부상(thiophosphate 산화 취약의 대안) — Asano 2018 이후 |
| 핵심 질문 | 합성 방법(기계화학 vs 고전 고상)이 **평균/국소 구조와 자리무질서**를 어떻게 바꾸고, 그것이 수송을 어떻게 바꾸나 |
| 선행의 긴장 | 실험(Asano Li₃YCl₆, ref31; Li₃ErCl₆ ref33)은 "합성→무질서→σ에 유리" 시사 ↔ 이론(Wang/Mo ref32, Angew 2019)은 "**antisite(M-on-Li) 무질서는 유해**(채널 차단)" — **서로 다른 종류의 무질서**를 구분해야 함 |
| 이 논문의 답 | M2–M3 무질서(양이온 부격자 내 자리 교환)는 **유익**하고 합성으로 조절 가능; M-on-Li antisite는 이 물질들에서 **배제됨**(전자밀도 없음) |

## 3. 핵심 물성 (수치 총정리)

### 3a. σ_RT / Ea 전체 표 (Table S4; AC 임피던스, **total** — bulk/GB 분리 불가 명시)
| 시료 (Li₃ErCl₆) | σ_RT / S cm⁻¹ | Ea / eV |
|---|---|---|
| Ball milled (as-prepared) | **3.1×10⁻⁴** (본문 3.1(5)) | **0.41** |
| BM + 1 min annealed | 1.0×10⁻⁴ | 0.47 |
| BM + 1 h annealed | 4.8×10⁻⁵ | 0.48 |
| Ampoule (550 °C 1주) | **1.7×10⁻⁵** (본문 1.7(1)) | **0.49** |

| 시료 (Li₃YCl₆) | σ_RT / S cm⁻¹ | Ea / eV |
|---|---|---|
| Ball milled | 9.5×10⁻⁵ | 0.45 |
| BM + 5 min annealed | 4.7×10⁻⁵ | 0.48 |
| BM + 1 h annealed | 5.5×10⁻⁵ | 0.45 |
| Ampoule | 3.4×10⁻⁵ | 0.49 |

→ Er 계열은 **σ 18× 스팬·Ea 단조**로 깨끗; **Y 계열은 비단조**(중간 시료들 σ·Ea 순서 섞임) — §10 비판 참조.

### 3b. M2–M3 자리무질서 전체 표 (Table S2; XRD Rietveld vs PDF 이중 정량) ★'무질서=공정변수' 데이터
| Li₃ErCl₆ | XRD / % | PDF / % |
|---|---|---|
| Ball milled | — (비정질, 정련 불가) | **88.1** (r≤8 Å fit) / **69.5** (r≤20 Å fit) |
| 1 min annealed | **9.9(2)** | 7.67 |
| 1 h annealed | **7.6(1)** | 6.25 |
| Ampoule | **2.5(1)** | 2.30 |

| Li₃YCl₆ | XRD / % | PDF / % |
|---|---|---|
| Ball milled | — | **100** (⚠ PDF 육안 추정 — 정량 불가, 저자 스스로 "high uncertainty" 명시) |
| 5 min annealed | 16.1(3) | — |
| 1 h annealed | 17.3(3) | — |
| Ampoule | 9.8(3) | — |

→ XRD와 PDF가 **독립적으로 같은 서열** 재현(어닐 시간↑ → 무질서↓; 앰풀 최저). Y는 전 구간 Er보다 무질서 높음.

### 3c. Rietveld 점유율·격자 (Tables S5–S10)
| 시료 | a=b / Å | c / Å | M2 occ | M3 occ | M2 z | M3 z | LiCl 불순물 | Rwp/GOF |
|---|---|---|---|---|---|---|---|---|
| Er BM+1min | 11.1660(2) | 6.0388(2) | 0.900(2) | 0.099(2) | 0.5164(5) | −0.018(3) | (Fig S7 fit에 포함, wt% 미기재) | 5.19 % / 4.11 |
| Er BM+1h | 11.1684(1) | 6.0352(1) | 0.924(1) | 0.076(1) | 0.5126(6) | −0.038(5) | 6 wt% | 3.96 % / 3.20 |
| Er ampoule | 11.16892(9) | 6.02670(9) | 0.975(1) | 0.025(1) | 0.5127(6) | −0.03(2) | 6 wt% | 4.14 % / 3.27 |
| Y BM+5min | 11.1980(2) | 6.0446(2) | 0.839(3) | 0.161(3) | 0.521(1) | −0.031(4) | (미기재) | 1.43 % / 2.15 |
| Y BM+1h | 11.2001(2) | 6.0441(2) | 0.827(3) | 0.173(3) | 0.488(1) | −0.065(3) | 4 wt% | 1.27 % / 1.88 |
| Y ampoule | 11.2008(2) | 6.0352(2) | 0.902(3) | 0.098(3) | 0.516(1) | −0.053(6) | 3 wt% | 1.75 % / 2.37 |

공통 고정: M1(1a, 0,0,0) occ 1 / Cl1–Cl3(6i) occ 1(팔면체 배위 구속) / **Li1(6g, 0.3397,0.3397,0) occ 1·Li2(6h, z=0.5) occ 0.5 — Li는 X선 산란 약해 정련 불가, 고정값·Biso=5** (→ §10: "Li 재배열" 기전은 실측 아님).

### 3d. 기타 수치
| 항목 | 값 | 출처 |
|---|---|---|
| DFT defect-model 에너지 (1×1×2 supercell) | ordered −247.74 / full-inversion −247.67 / alternating −247.80(최저) / random+face-sharing **−246.21**(최고) eV | Fig 5 |
| PDF 국소 지문 | Er1–Er2 ~7.1 Å 피크가 BM에서 **부재**, Er1–Er3 ~6.5 Å 강도↑ → 밀링 중 M2→M3 이동 | Fig 3a·3b inset |
| 다면체 병목(삼각 전이면적) | 전 범위 ~5.4–6.3 Å²; 무질서↑에 따라 Oh(6g)–Td–Oh(6g)·z-방향 Oh–Oh **확대**, Oh(6h)–Td–Oh(6h) 축소 | Fig 4b |
| Ea↔병목 상관 | z-방향 6h/6g **Oh–Oh 면적 5.88→6.18 Å²** ↔ Ea 0.49→0.41 eV (무질서 2.3→88 %) | Fig S13 |
| Williamson–Hall strain 기울기 | 1 min 1.75×10⁻³ → 1 h 1.52×10⁻³ → 앰풀 ~0.93×10⁻³ (figure-read) — 어닐수록 미세변형↓ | Fig S2 |
| BM 잔류 전구체 | ErCl₃:Li₃ErCl₆ 몰비 **1.92**(8 Å fit) / **1.43**(20 Å fit) — BM 시료는 국소 Li₃ErCl₆ + 다량 ErCl₃ 혼재 | Table S1 |
| PDF fit Rw | 앰풀 14.8 / 1 h 16.8 / 1 min 14.2 / BM(8 Å) 8.7 / BM(20 Å) 28.5 / Y 5min 27.0 % | Fig 2d·S1d·S4 |
| σ(300 °C) 참고(인용) | Li₃InCl₆ ~0.2 S/cm @300 °C (Steiner 1992) | intro |

## 4. 구조 해부 (Fig 1) — 자리 명명이 이 논문의 문법
- **삼방 P3̄m1**, MCl₆³⁻ 팔면체 격자. **M1 = Wyckoff 1a**(0,0,0; z=0 평면). **M2 = 2d, z≈0.51 — (002) 평면**. **M3 = 2d, z≈0(−0.02~−0.06) — (001) 평면 = "M2를 c/2 이동한 등가자리"**. 완전 질서 = M1+M2 100 %, M3 공석.
- **M2–M3 무질서** = M2 양이온 일부가 M3로 이동 (c축 수직 face-sharing MCl₆ 사슬로 시각화 가능; 단 **M2·M3 인접 동시점유는 강한 반발로 불가** → 무질서에 국소 제약 있음).
- **Li 부격자**: 할라이드 팔면체 공극 — **6g(z=0, 점유 1) + 6h(z=0.5, 점유 0.5)**. 각 MCl₆³⁻ 팔면체를 a–b 평면에서 **edge-sharing LiCl₆⁵⁻ 6개가 벌집형으로 포위**.
- **Li 점프 4종**(Fig 1e·4a): ① **Oh(6h)–Oh(6g) z-방향**(face-sharing 팔면체 직결) ② Oh(6h)–T_d–Oh(6h) — (002)면 내 ③ Oh(6g)–T_d–Oh(6g) — (001)면 내 ④ T_d–T_d(비현실적). 6g가 만점유라 ③ 단독으론 느림 → **면내 수송은 6h(반점유) 경유가 유리**하고, z-방향 ①이 결정적.
- 평면 대응: **6g Li·M1·M3 = z≈0 평면 / 6h Li·M2 = z≈0.5 평면** → M2→M3 이동은 **Li(6g) 평면으로 양이온이 들어오는 사건** = 정전 반발로 Li 재배열 유발(가설).

## 5. 재료 & 합성 (Experimental) — '공정변수' 그 자체
- **전구체**: LiCl(Alfa 99.9 %)·ErCl₃(Sigma 99 %)·YCl₃(Alfa 99.999 %), Ar 글러브박스, 1 g 배치, **희토류 할라이드 10 wt% 과량**(예비분쇄 시 마노 유발에 들러붙는 손실 보상).
- **고전 고상(앰풀)**: 펠릿 압축 → 석영 앰풀(10 mm 지름, ~10 cm; 800 °C 동적진공 ≥1.5 h 예열 건조) 진공 밀봉 → **550 °C 1주** → 공랭(air-quench).
- **기계화학(볼밀)**: 45 mL ZrO₂ 컵(60 °C 동적진공 12 h 건조), **3 mm ZrO₂ 미디어, ball:powder 30:1, 500 rpm**; **총 297 사이클(99×3), 1 사이클 = 5 min 밀링 + 15 min 휴지**(발열 방지, 사이클마다 균질화) → 순밀링 ≈24.8 h (유도값).
- **후속 결정화 어닐**: 밀링 분말을 진공 앰풀에 넣어 **예열된 550 °C 로에 투입 → 1 min(Er)/5 min(Y) 또는 1 h → 공랭**(어닐 시간 정밀 제어 목적). Er은 **1 min 만에 결정화 완료**(Li₆PS₅Br 급속결정화 ref40과 평행 — "밀링이 이미 1차 합성 단계·전핵생성 클러스터" 서사).
- **임피던스 셀**: 펠릿 ~2 mm·0.79 cm²·기하밀도 >85 %, 손압축 후 **등방압 360 MPa 45 min**, **증착 Au 전극 0.53 cm²**, Ar 파우치셀.

## 6. 결과 — 섹션별 상세

### 6.1 평균구조: XRD·Rietveld (Fig 2a,c; S7–S12)
볼밀 as-prepared = 브래그 피크 광폭화(비정질화). 어닐 1 min만에 날카로운 패턴(급속 결정화). Rietveld(TOPAS): 저각 비대칭 때문에 GOF+육안으로 판정. **다양한 무질서 모델 시험 — 다른 Wyckoff(1b,2c,3e,3f) 점유·Er-on-Li antisite 전부 기각**(전자밀도 유의 없음) → **살아남은 무질서는 Er2–Er3뿐**. 무질서 정량은 §3b·3c.

### 6.2 국소구조: PDF (Fig 2b,d·3; S1, S3–S5)
- PDFgetX3(Qmax 12 Å⁻¹ 통일), 결정질 = PDFgui(r 2–20 Å = 단위셀 대각선), BM = DiffPy-CMI **2상(Li₃ErCl₆+ErCl₃) fit, r-범위 2종(2–8 Å 국소 / 2–20 Å 평균)**.
- BM G(r): 감쇠 빠름(저 간섭성)이나 **r<8 Å에서 이미 Li₃ErCl₆ 국소 모티프 형성** — 밀링만으로 국소 생성물 존재; r>8 Å은 결정질 잔류 ErCl₃가 지배(몰비 1.4–1.9).
- **국소 무질서 지문**: Er1–Er2(7.1 Å) 피크 BM에서 미형성 + Er1–Er3(6.5 Å) 강도↑ → 정성적으로도 M2→M3 이동.
- PDFgui 처리에서 Er·Cl 자리 분열(Fig S3) = P3̄m1보다 낮은 **국소 대칭(팔면체 구속 유지하며 Cl 0.76→0.77 수준 미세이탈)** 허용 — Rietveld가 못 잡는 국소 왜곡을 표현. Biso는 원소별 공통 구속.
- **Li₃YCl₆은 PDF 정량 불가**: Y 함유 전 시료에서 형광성 상수 배경(Fig S5) → S/N 저하·termination ripple → Rietveld만 사용.

### 6.3 어닐 시간축: 무질서 이완 + 미세변형 (Fig 3b; S2)
무질서는 **밀링 직후 거의 완전(88–100 %) → 어닐 시간에 따라 감소 → 앰풀(1주)에서도 2.5 %(Er)/9.8 %(Y) 잔존** — 완전 질서엔 도달 못 함("changes over time and relaxes into a more, but not yet fully ordered structure"). Williamson–Hall: 어닐 길수록 strain↓(1.75→1.52→0.93×10⁻³) = 미세구조 이완 동반(→ §10 교란변수).

### 6.4 다면체 경로 기하 (Fig 4)
Er·Cl 위치만으로(Li 위치 미지 명시) 4종 점프의 **삼각 병목 전이면적** 계산. 어닐 시료들은 T_d–T_d·Oh–Oh 면적 변화 미미, BM(고무질서)에서 급변: **(001)면 Oh(6g)–T_d–Oh(6g)·z-방향 Oh–Oh 확대 ↔ (002)면 Oh(6h)–T_d–Oh(6h) 축소**. 해석: Er 무질서(→(001)면 유입) → 국소 왜곡 → **6g/6h 주변 다면체 재편** → Li 점유·경로 변화(정전 반발). Er에서만 가능(Y는 형광 문제).

### 6.5 DFT defect 모델 에너지 (Fig 5) — "무질서는 열역학적으로 접근 가능"
- 1×1×2 supercell(P3̄m1 셀 Z=3 f.u.×2 = 6 f.u. ≈ 60원자; 원자수는 논문 미명시·격자에서 유추), 격자 = 실험값 고정, 이온만 완화.
- 모델 4종: (a) **완전질서**(Er1+Er2 만점유) −247.74 eV (b) **완전 자리반전**(Er2→Er3 전부; 그 자체로 또 하나의 '질서') −247.67 eV (c) **교대 배열**(Er2/Er3 층 교대, (002) 거울면 유지 = 형식 점유 50/50) **−247.80 eV 최저** (d) **무작위 + 국소 face-sharing ErCl₆ 발생** **−246.21 eV 최고**(최저 대비 +1.59 eV/supercell ≈ +26 meV/atom).
- 판정: (a)(b)(c)가 **~0.13 eV/supercell(≈1–2 meV/atom) 안에서 등가** → M2–M3 혼합점유는 에너지 벌점이 사실상 없음 = **어느 배열이 실현되는가는 공정(밀링 vs 어닐 온도·시간)이 결정**. 단 (d)처럼 **Er–Er face-sharing을 강제하는 배열만 강한 반발로 배제** → 무질서는 '완전 무작위'가 아니라 **단거리 질서 제약(M–M 근접 회피)** 하의 무질서.

### 6.6 임피던스·수송 (Fig 6; S6; Table S4)
- 나이퀴스트 = 반원 1개(CPE∥R) + 저주파 블로킹 꼬리(CPE). **α>0.9, 기하 정전용량 ~48 pF/cm² = bulk형 응답이나 bulk/GB 분리 불가 명시** → σ·Ea는 total.
- 아레니우스 선형(-40..60 °C), σ_RT·Ea는 §3a. **어닐 시간↑ → σ↓·Ea↑** (Er 단조; Y 대체로 동일 방향·비단조).
- **Fig 7a,b (본문 핵심 그림)**: σ·Ea를 **무질서 %에 대해** 재플롯(XRD·PDF 두 척도 모두) → 단조 상관. Ea 0.49→0.41 eV, σ 1.7×10⁻⁵→3.1×10⁻⁴ S/cm.

### 6.7 구조–수송 상관 3줄 결론 (§2.5)
1. **밀링 = 고무질서 생성, 어닐 = 시간의존 질서 회복** (DFT: 배열 간 등에너지 → 실현은 공정 몫; 어닐은 항상 Er2 고점유로 수렴).
2. **무질서↑ → σ↑**: Er가 (001)면에 들어오며 정전 반발로 **Li 부격자 재배열·유효 캐리어(빈자리) 증가 가설** — 저자 스스로 "중성자 + 대규모 AIMD 필요" 명시(**미실행**).
3. **무질서↑ → Ea↓**: 병목(전이면적) 확대와 상관 — 특히 z-방향 Oh–Oh(Fig S13). "여러 물질군에서 병목 면적↑ = 음이온 변위 필요량↓ = Ea↓" 일반론(ref 9,15,44)에 접속.

## 7. 전체 논증 흐름
합성 4경로(밀링/1 min/1 h/앰풀) → XRD·PDF 이중 정량으로 **무질서 = 연속 조절 변수**임을 확립(3b) → PDF 국소 지문·병목 기하로 **구조적 결과** 규명(6.2·6.4) → DFT로 **왜 조절 가능한가**(등에너지 배열, 6.5) → 임피던스로 **수송 귀결**(σ↑Ea↓, 6.6) → "합성 방법 = 자리무질서·수송의 설계 도구" 결론.

## 8. DFT/계산 방법 ★
- **code**: VASP (PAW, ref 51–52) · **functional**: GGA-**PBE** · **ecut**: 520 eV · **k-mesh**: 3×3×3 Monkhorst–Pack(1×1×2 supercell 기준) · **수렴**: 힘 <10⁻⁴ eV Å⁻¹ (매우 타이트) · **격자 고정 = 실험값**, 이온만 완화.
- **무질서 처리**: Li/Er 배열 열거 → **pymatgen Ewald summation으로 정전에너지 사전선별** → **대칭 다른 최저 정전에너지 구조 10개를 DFT 재계산** (SQS 아님; enumerate→lowest-Ewald 노선 — [Liu] AFM 2022와 동일 철학, 우리 cfg-enumeration과 같은 계열).
- **범위**: 정적 total energy **만**. NEB 없음·AIMD 없음·DOS/gap 미보고·기계물성 없음 → "무질서가 σ를 올린다"는 **계산으로 증명된 바 없음**(열역학 접근성만 계산).
- 임피던스: VMP300(Biologic), 7 MHz–100 mHz, 10 mV, −40..60 °C.
- XRD: STOE STADI P, **Ag Kα₁ λ=0.5594075 Å**(Ge(111) 단색화), Mythen2 4K(Dectris 4×), Debye–Scherrer, 0.5 mm 유리 모세관 밀봉, Q 0.3–20.5 Å⁻¹, 결정질 6 h·비정질 22 h. Rietveld = **TOPAS**(Chebyshev 10항 배경, mod. Thomson–Cox–Hastings pseudo-Voigt).
- PDF: **PDFgetX3**(S(Q) 푸리에; qdamp 0.011/qbroad 0.010 — LaB₆ 표준), fit = **PDFgui**(결정질)·**DiffPy-CMI**(BM 2상: mc1·G(r)_ErCl₃ + mc2·G(r)_Li₃ErCl₆ = G(r)_total, Eq 1).

## 9. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 | 구조 해부: ErCl₆ 골격·Er1/2/3 자리·Li 6g/6h 벌집·점프 경로 4종 | 자리 명명 문법; LYC([Cha] 코팅) 구조 백그라운드 |
| 2 | 합성별 XRD + PDF 원시 데이터 + 대표 Rietveld/PDF fit | 볼밀 비정질화→1 min 결정화; "XRD+PDF 이중 정량" 프레임 |
| 3 | (a) PDF 국소 비교 — 7.1 Å 부재/6.5 Å 증가 (b) **무질서 vs 공정 마스터 플롯**(XRD·PDF 겹침) + Er 거리 inset | ★'무질서=공정변수' 한 장 요약 — deck 인용 1순위 |
| 4 | (a) 점프 4종 기하 (b) **병목 전이면적 vs 무질서** | BVSE 없이 음이온 기하만으로 병목 정량 — 우리 BVSE 채널%의 저가 기하 판 |
| 5 | DFT defect 모델 4종 + 에너지 | 무질서 등에너지·face-sharing 벌점 — 우리 enumeration 서사의 실물 예 |
| 6 | 나이퀴스트(대표+4종 비교)·아레니우스·σ/Ea vs 공정 | total-σ 판독 방식; "공정→수송" 그림 문법 |
| 7 | σ·Ea vs **무질서 %** + Li 재배열/병목 확대 모식도 | 본문 결론 그림; 기전 2갈래(캐리어·병목) 구분 |
| S1 | Li₃YCl₆ XRD/PDF/fit (5 min 결정화) | Y 계열 재현성; PDF Rw 27 % 한계 |
| S2 | Williamson–Hall + strain 기울기 | 어닐=strain 이완 — 무질서와 병행하는 교란변수 |
| S3 | PDFgui 자리분열·ADP 구속 도식 | 국소대칭 저하를 fit에 넣는 법(방법론) |
| S4 | Er PDF fit 5종(범위별) | 2상 fit·r-범위 전략 |
| S5 | Y 형광 배경·termination ripple | 원소별 측정 한계 문서화 사례 |
| S6 | Y 임피던스 풀세트 | Y 비단조 — 상관의 한계 |
| S7–S12 | 시료별 Rietveld fit + 표 | 점유율 전량 공개(§3c) |
| S13 | **Ea vs z-방향 Oh–Oh 병목 면적** | 기하 서술자↔Ea 상관 — 우리 migration_volume/BVSE와 접속 |

## 10. 주의/한계 (비판적으로)
1. **Li를 못 봤다**: X선이라 Li 점유·위치 정련 불가(6g=1/6h=0.5/Biso=5 고정). "Li 재배열 = 캐리어 증가" 기전(Fig 7c)은 **가설**이고, 저자도 중성자+AIMD 필요를 명시. → 이 논문에서 가져갈 확정 사실은 "Er/Y 무질서 정량 + σ/Ea 상관"까지.
2. **σ·Ea는 total(임피던스)**: bulk/GB 분리 불가 명시. 어닐은 무질서만이 아니라 **결정화도·strain(W–H)·입계·LiCl 3–6 wt%·잔류 ErCl₃**를 동시에 바꾼다 → σ 18×를 자리무질서 단독 효과로 읽으면 과대. 특히 **BM as-prepared 시료는 비정질+ErCl₃ 몰비 1.4–1.9 혼합물** — 상관 플롯의 최극단 점(88–100 %)이 가장 불확실(Y "100 %"는 육안 추정).
3. **Y 계열 비단조**(σ 5 min 4.7 < 1 h 5.5×10⁻⁵; Ea 0.48/0.45; 무질서 16.1/17.3 %) — Er만큼 깨끗하지 않음. 상관은 "극단 간 방향"이 견고하고 중간점은 노이즈.
4. **DFT는 수송을 계산하지 않았다**: 정적 4(+10)개 배열 에너지·소형 셀(6 f.u.)·PBE·실험격자 고정. 무질서→Ea↓는 **기하 상관(전이면적)**으로만 연결.
5. **무질서 종류 구분 필수**: 여기의 유익한 무질서 = **양이온 부격자 내 M2–M3**; Wang/Mo(ref32)의 유해한 무질서 = **M-on-Li antisite**(채널 차단; 이 물질에선 실험적으로 배제). "halide는 무질서가 좋다/나쁘다" 뭉뚱그리면 틀림.
6. **argyrodite 이식 금지**: 자리 기하(삼방 P3̄m1 6g/6h vs 입방 F4̄3m 48h cage)·무질서 유형(양이온 M2–M3 vs 음이온 4a/4d)·수치 전부 물질군 다름. **방향(무질서↑→σ↑·Ea↓)과 '공정변수' 프레임만** 전이 가능.

## 11. 우리 DFT 대비 (comp1/modelc) → `../our_dft_baseline.md`
| 항목 | 이 논문 (halide Li₃MCl₆) | 우리 (argyrodite comp1/modelc) | 판정 |
|---|---|---|---|
| 무질서의 지위 | **공정변수** — 합성·어닐로 2.5→88 % 연속 조절(XRD+PDF 실측) | **공정변수 가정** — disorder ensemble(d=0.0/0.5 decorate), modelc 4d-Cl 12.5 % | **✓ 프레임 동일** — 우리 '무질서=공정변수' 논지의 외부 실증(단 양이온 vs 음이온 무질서로 부격자 다름) |
| 무질서↑ → σ↑·Ea↓ | σ 18×·Ea 0.49→0.41 eV (**total EIS**) | comp1 d=0(frozen, Ea artifact 1.17) → d=0.5 Ea 0.177±0.027 (**MLIP-MD bulk**); comp1→modelc D 2.6×·Ea 0.253→0.224 | **✓ 방향 일치·수치 등치 금지** (물질군·방법(총저항 vs bulk tracer) 모두 다름) |
| 무질서 열역학 | DFT 배열 등에너지(~1–2 meV/atom), face-sharing만 +26 meV/atom 벌점 | 우리 cfg-enumeration도 저에너지 스프레드 좁음(무질서 접근 가능) 전제 | **✓ 같은 물리** — '무질서는 바닥상태 강제가 아니라 공정 산물' |
| 무질서 처리(계산) | enumerate → **pymatgen Ewald 사전선별** → DFT 10개 | 우리·[Liu]와 동일 노선(enumerate→lowest-Ewald), SQS 아님 | **✓ 방법 계보 동일** |
| 병목 기하 서술자 | 음이온 삼각 전이면적(Å²) ↔ Ea 상관 (Fig S13) | BVSE 채널 %(3.32/4.74/6.73)·migration_volume_fraction | ○ 상보 — 우리 것이 더 정교(퍼텐셜 기반), 이 논문 것이 더 값쌈(기하만) |
| Ea 절대값 | 0.41–0.49 eV (halide, total) | 0.22–0.25 eV (argyrodite, MLIP bulk) | **비교 불가** — 물질군+방법 다름. §11b 참조 |
| DFT 셋업 | VASP·PBE·PAW·520 eV·3×3×3 k·실험격자 고정·정적만 | QE·PBE·완화격자·+MLIP-MD/BVSE/COHP/ESW | 우리가 수송·전자구조까지 확장한 상위집합 |
| gap/ESW/기계 | **n/a** (미보고) | 각 json | 비교 대상 없음 |

## 11b. ★특별 검증 — li_transport.json "Schlem 2020 ordered 0.25 eV" 귀속 판정
**질문**: 우리 `db/properties/li_transport.json`이 comp1(4fu natural) MLIP-MD Ea 0.2532 eV를 "Schlem 2020 LPSCl ordered ~0.25 eV와 EXACT MATCH"로, modelc 0.224를 "Schlem Cl-rich ~0.22"로 앵커링. repo가 지목하는 원전 = **AEM 10, 1903719** (`kb/open_items.md` #5·`kb/papers/lpscl_vs_lpscl16_seminar_v1.md` ref [3] 명시).

**판정 (a) — 이 논문이 그 "Schlem 2020"인가?**: repo가 인용한 DOI(10.1002/aenm.201903719)의 실물 = **본 논문 = Li₃MCl₆(Y,Er) 할라이드 기계화학 논문**. 즉 "repo가 가리키는 문헌"은 맞게 찾아왔으나, **그 문헌은 LPSCl 논문이 아니다**.

**판정 (b) — 0.25 eV는 이 논문의 무엇인가?**: **아무것도 아니다.** 본문+SI 전체에 (i) Li₆PS₅Cl/argyrodite 데이터 없음 (ii) Ea 0.25·0.22 eV 값 없음(전 Ea = 0.41–0.49 eV, AC 임피던스 total) (iii) Cl-함량 시리즈 없음 (iv) DSC/TGA 없음. 따라서 li_transport.json의 "LPSCl ordered 0.25 / Cl-rich 0.22"의 **원전은 미확인 상태**가 됐다 — 별도 논문(후보: Zeier계 LPSCl 시리즈·Adeli 2019 Angew·Minafra SSI 2020 등, **어느 것도 실물 미확인**)을 확보해 재귀속해야 함. 파생 오귀속 의심 지점(같은 DOI로 걸린 다른 주장들): 세미나 원고의 "Cl-rich DSC/TGA mass-loss onset 315 °C"(실제로는 **Zuo 2022 Fig S3b의 TGA 수치**임 — zuo digest §3와 일치)·"Cl 1.5–1.7 sweet spot"·"paper-grade Cl-content series" — 전부 이 DOI에 없음.

**판정 (c) — 비교의 방법론적 적법성**:
1. **물질 불일치(치명)**: 삼방 할라이드 Li₃MCl₆ ↔ 입방 argyrodite Li₆PS₅Cl. 어떤 Ea 일치도 물질군 교차 우연 — "EXACT MATCH" 앵커로 부적법.
2. **방법 층위(원전이 바로잡혀도 남는 문제)**: 임피던스 Ea는 대개 total(bulk+GB; 이 논문도 분리 불가 명시) ↔ 우리 Ea는 MLIP-MD bulk tracer(600–1000 K 3점, Haven=1). 우리 kraft2017 digest가 이미 확립한 규율("Kraft total 0.46 ≫ 우리 bulk 0.253 = 방법차") 그대로 — **±0.003 eV "정확 일치" 화법은 방법 층위가 같음을 확인하기 전엔 금지**.
3. **살아남는 것**: "무질서↑→Ea↓·σ↑" **방향** 서사는 이 논문(할라이드 교차-화학 실증)+Minafra(argyrodite)로 여전히 지지됨. 죽는 것은 **0.25/0.22 수치 앵커의 출처 표기**와 "EXACT" 수사.

**후속 조치 필요 목록 (이번 세션 범위 밖, litdb 밖 파일이라 미수정)**: `db/properties/li_transport.json`(comp1_4fu experimental_match·robust_findings·5fu note), `kb/papers/lpscl_vs_lpscl16_seminar_v1.md`(ref [3]·slide 표·Q&A 다수), `kb/papers/lpscl_vs_lpscl16_seminar_script_outline.md`, `tools/build_seminar_pptx.py`(Schlem 행 3곳), `kb/open_items.md` #5, `docs/transport/disorder_ensemble_2026_06_09.md`, `db/properties/literature_tensions_audit.json`, `litdb/papers/he2019…md`·`bai2020…md`·`liang2025…md`·`kraft2017…md`의 "Schlem 0.25 일치" 문구 — 전부 "출처 재확인 필요(AEM 1903719 아님)" 태그 대상.

## 12. 적용 인사이트
1. **'무질서=공정변수' 논지의 1급 외부 실증**: 같은 조성·4 공정·무질서 2.5→88 %·σ 18×·Ea −0.08 eV, XRD+PDF 이중 정량. 우리 disorder-ensemble(예: comp1 d=0→0.5) 서사에 "실험은 이렇게 무질서를 돌린다"는 실물 좌표 제공. deck 인용 1순위 = Fig 3b·7a,b.
2. **DFT 등에너지 논리 차용**: "배열 간 ΔE ~meV/atom = 어느 배열이 실현되는가는 공정 몫" — 우리 enumeration 결과(저에너지 스프레드)를 같은 문장으로 프레이밍 가능. 동시에 **face-sharing 벌점(+26 meV/atom)** = 무질서 decorate 시 비물리 근접쌍을 Ewald 사전선별로 걸러야 한다는 근거(우리 이미 수행).
3. **Ea-앵커 위생**: §11b — li_transport.json의 "Schlem 0.25 EXACT" 앵커는 재귀속 전까지 발표·원고에서 사용 중지 권고. "실험 LPSCl bulk 범위 0.16–0.30 내" 수준의 보수적 표현으로 대체.
4. **기하 병목 서술자**: 음이온 좌표만으로 삼각 전이면적↔Ea 상관(Fig S13) — 우리 comp1/modelc/도핑 셀에 같은 기하 지표를 뽑아 BVSE 채널%와 교차하면 값싼 2차 서술자.
5. **[Cha] LYC 연결**: 이 논문의 Li₃YCl₆ σ(3.4–9.5×10⁻⁵ S/cm)·합성 의존성은 우리 그룹 할라이드 코팅(LYC 0.37 mS/cm) 배경 물성 — 코팅용 할라이드도 공정(밀링/어닐)에 따라 σ 수 배 움직인다는 주의점.

## 13. 인용 가능 문장 (deck/paper용)
- "Schlem et al. (AEM 2020, 1903719) showed for trigonal Li₃MCl₆ (M = Y, Er) that the synthesis route continuously tunes cation site disorder (2.5→88 % by Rietveld/PDF) and thereby the transport (σ ×18, Ea 0.49→0.41 eV) — an experimental demonstration that site disorder is a *process variable*, the same framing we use for anion-site disorder in argyrodites."
- "Their static DFT finds ordered and site-inverted configurations degenerate within ~1–2 meV/atom (only face-sharing M–M arrangements are penalized), supporting the view that the realized disorder is set by processing, not by the ground state."
- ⚠ 사용 금지(정정 전): "our Ea 0.253 matches Schlem 2020 LPSCl ordered 0.25 exactly" — **이 DOI에 그 수치 없음** (§11b).

## 14. 용어 미니사전
- **PDF (pair distribution function)**: 전체 산란(브래그+확산)을 푸리에 변환한 G(r) — 국소(수 Å) 구조 프로브. Rietveld(평균구조)와 상보.
- **PDFgetX3 / PDFgui / DiffPy-CMI**: G(r) 생성 / 결정질 실공간 정련 / 다상·구속 유연 정련 툴체인.
- **Rietveld / TOPAS**: 분말 XRD 전체 패턴 정련(점유율·격자·Biso); TOPAS = 상용 정련 SW.
- **Williamson–Hall**: 피크폭 B·cosθ vs 4 sinθ 직선의 기울기=미세변형(strain), 절편=결정립 크기.
- **M2–M3 site disorder**: 같은 양이온 부격자 내 두 2d 자리 간 점유 교환(여기선 유익) ↔ **antisite(M-on-Li)**: 양이온이 Li 자리 점유(채널 차단, 유해 — 이 물질에선 배제됨).
- **삼각 전이면적(triangular transition area)**: 점프 경로 병목을 이루는 음이온 3개 삼각형 면적 — 기하학적 병목 서술자.
- **CPE / α**: constant phase element; α→1일수록 이상 축전기. α>0.9 + ~pF/cm² = bulk형 응답.
- **Debye–Scherrer(모세관) 기하**: 공기민감 시료를 밀봉 모세관으로 투과 측정 — 할라이드/황화물 표준.
