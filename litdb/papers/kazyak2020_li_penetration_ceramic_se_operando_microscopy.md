<!-- digest 표준 양식 (paper-level STANDALONE) · 2026-11-24 첫 작성 (병렬 논문 에이전트 런 — INDEX · comparison 은 메인 세션이 합친다).
     그림: extract_figures.py 24 장 + 손 크롭 1 장 (Table S1 — 이미지로 박힌 표라 캡션 앵커가 못 잡음 · figures.json manual_crop 사유).
     실제로 본 것 22 장 (본문 12/12 · SI 9/12 · Table S1) · 안 본 것 Fig. S4 · S8 · S10 (figures.json 의 viewed 표시와 같다).
     ⚠ PDF 텍스트층에서 'µ' 가 'm' 으로 깨진다 — 추출문의 "250 mm wide", "7 mm of Li", "Lrelax z 3 mm" 는 전부 µm (쪽 렌더 · 그림 축척으로 확인). -->

# Li Penetration in Ceramic Solid Electrolytes: *Operando* Microscopy Analysis of Morphology, Propagation, and Reversibility — Kazyak et al. (*Matter* **2020**, 2, 1025–1048)

> slug `kazyak2020_li_penetration_ceramic_se_operando_microscopy` · DOI `10.1016/j.matt.2020.02.008` · type `exp (operando 광학 동영상 현미경 + 시간 동기 전압 · EIS · 사후 FIB-SEM/BSE · XRD · COMSOL 3D FEM 전류분포 보조) · 원자단위 계산 0` · PDF `litdb/inbox/kazyak2020_li_penetration_main.pdf` (25 쪽 = 표지 1 + 인쇄 1025–1048) + `litdb/inbox/kazyak2020_li_penetration_SI.pdf` (21 쪽 = 표지 1 + 인쇄 1–20 · Figure S1–S12 · Table S1 · 동영상 1–10 캡션) · digested `2026-11-24` · status ✅ · 태그 **[외부]**

> elements: Li, La, Zr, Al, O, P, S
> methods: EIS, galvanostatic cycling, operando optical microscopy, FIB-SEM, XRD, FEM

> **저자**: Eric Kazyak¹ · Regina Garcia-Mendez² · William S. LePage¹ · Asma Sharafi¹ · Andrew L. Davis¹ · Adrian J. Sanchez¹ · Kuan-Hung Chen² · Catherine Haslam² · **Jeff Sakamoto**¹˒² · **Neil P. Dasgupta**¹˒³\* (¹ Univ. of Michigan, Mechanical Engineering · ² Univ. of Michigan, Materials Science and Engineering · ³ lead contact · 교신 ndasgupt@umich.edu) · 투고 2019-10-21 · 수정 2020-01-09 · 수락 2020-02-07 · 온라인 2020-03-04 · 권호 2020-04-01 · **OA CC BY-NC-ND 4.0** · 자금 ARPA-E DE-AR-0000653 (+ NSF GRFP DGE 1256260 · U-M College of Engineering · MC² NSF DMR-0723032) · 이해관계 — E.K. · R.G.-M. · J.S. · N.D. 가 이 작업 관련 미국 가특허 출원 · J.S. 는 Zakuro Inc. CTO
>
> **논문 CRediT**: 착상 N.P.D. · J.S. · E.K. · A.S. / 자금 · 지도 J.S. · N.P.D. / 실험 E.K. · R.G.-M. · A.L.D. · A.J.S. · A.S. / 소프트웨어 · 초고 · 분석 E.K. · A.J.S. · A.L.D. · W.S.L. / 자료 · 방법 E.K. / 시각화 E.K. · W.S.L. · K.-H.C.
>
> **계보**: Wood 2016 *ACS Cent. Sci.* (ref 27 · 같은 Dasgupta 랩 · 액체 전해질 Li 금속의 operando 동영상 현미경 'dendrites and pits' — 이 논문의 '전압 봉우리' 해석 틀) + Porz 2017 *Adv. Energy Mater.* (ref 6 · Li 로 찬 균열의 과전압–응력 모델 · 단결정 LLZO · 유리 LPS) + Sharafi 2017 *Chem. Mater.* (ref 7 · 같은 Sakamoto–Dasgupta · LLZO 표면 Li₂CO₃ 제거 → 초저 계면저항) → **본 논문** (in-plane operando 플랫폼 · 형태 4 분류 · 침투 Li 가역성 · 성장 속도 ∝ 전류 · 방전 공극) → Lee · Kazyak · Wang · Dasgupta · Sakamoto 2022 *Joule* 6, 2547 ('Analyzing void formation and rewetting of thin in situ-formed Li anodes on LLZO' — 이 논문을 ref 17 로 인용 · PDF `litdb/inbox/lee2022_thin_li_void_rewetting_main.pdf`) → Liao … Dasgupta 2025 *Adv. Mater.* (`papers/liao2025_interfacial_adhesion_li_plating_carbon_interlayer.md` ✅ · 점착이 Li 석출 위치를 정함).
>
> **litdb 이웃**: `papers/pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament.md` (LPSCl 의 Li 필라멘트 저항을 DFT 로) · `papers/luo2022_cryotem_li_dendrite_sulfide_interphase.md` (황화물 속 Li 덴드라이트 계면상) · `papers/hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd.md` (LLZO 이중층 CCD 모사) · `papers/wang2022_two_parameter_space_dendrite_constriction.md` · `papers/kang2026_site_specific_customized_se_dendrite_tolerant_li_metal.md` [우리 그룹].

> **본 digest 에서 실제로 본 그림 (2026-11-24)**: `Fig. 1`–`Fig. 12` (12/12) · `Fig. S1` `Fig. S2` `Fig. S3` `Fig. S5` `Fig. S6` `Fig. S7` `Fig. S9` `Fig. S11` `Fig. S12` · `Table S1` (손 크롭 · 300 dpi 로 값 대조) — **22 장**.
> 안 본 것: `Fig. S4` (COMSOL 전위 분포 — 옴 강하 0.27 / 0.23 V 는 SI 본문 값) · `Fig. S8` (XRD 상분율 — 값은 본문 p. 1034) · `Fig. S10` (같은 branching 의 조명 비교).
> 그림에서만 읽은 값은 **`figure-read ≈`**, 내가 계산한 값은 **우리 산수** 로 표시했다.

---

## 0. 이 digest 를 읽는 법

- 이 논문은 **우리 계 (결정 Li₆PS₅Cl argyrodite) 가 아니다.** 주 재료는 Al 도핑 LLZO (산화물 가넷) 이고, 황화물은 유리 Li₃PS₄ 한 셀 (`Fig. 12`) 뿐이다. 원자단위 계산은 없다.
- 그래도 읽는 이유는 셋이다.
  ① **"Li 침투 = Li 로 찬 균열이 기계적으로 열리며 자란다"** 의 operando 근거 — DEM · 연속체 균열 모형의 정성 근거이자 정량 표적 몇 개 (성장 속도 ∝ 전류 · 문턱 · 되밀림).
  ② **방전 (Li 탈리) 쪽 공극 · 접촉 면적 감소**가 계면저항을 키우는 과정 — W_ad 보고서 §7 (Li 친화성 · 점착과 공극) 의 실험 쪽 그림.
  ③ **침투 Li 는 되돌아 빠진다 (가역)** · dead Li · 남은 균열 벽의 전자전도 문제 — 우리 §E (Li 금속 계면 분해 · Li₃P) 와 이어지는 질문.
- ⚠ 읽을 때 세 가지.
  ① 전류밀도는 전부 **공칭** (전극 겉넓이 기준) 이다. in-plane 전극 가장자리의 국소 전류는 COMSOL 로 공칭의 ≈2.5–3 배다 (`Fig. S3`, figure-read).
  ② in-plane 셀은 **스택 압력 0** · 증착 후 **녹인** ≈8 µm Li 박막 · 전극 ≈0.5 mm² 다. 보통 셀과 조건이 달라서 CCD 가 '5–10 배 높게' 나온 이유의 일부가 여기 있다 (저자도 면적 통계를 이유로 든다).
  ③ PDF 텍스트층에서 µ 가 'm' 으로 깨진다 (머리 주석).
- 쪽 표기 — 본문은 인쇄 쪽 (p. 1025–1048), SI 는 SI 인쇄 쪽 (SI p. 1–20). PDF 쪽 = 본문 인쇄 쪽 − 1023 · SI 인쇄 쪽 + 1.

---

## 1. 한 줄 요약

Al-LLZO 연마면에 Li 전극 두 개를 나란히 증착한 **in-plane operando 셀**로, 공칭 1–5 mA/cm² 를 무압력에서 버티는 깨끗한 Li|LLZO 계면 (계면 < 5 Ω cm²) 을 만들고 그 위에서 Li 침투를 동영상으로 찍었다. 침투 형태는 **네 가지** (straight · branching · spalling · diffuse) 라 단일 기전으로 설명되지 않는다. 흔한 세 형태는 **Li 로 찬 균열이 기계적으로 열리며** 자라고 (성장 속도 ∝ 전류 · 전류를 끊으면 Li 크리프로 ≈3 µm 되밀림), 단락 전에는 **침투 Li 를 거의 다 되돌려 뺄 수 있으며** (dead Li 도 생긴다), 빠른 탈리 (방전) 는 **공극 · 탈습윤**으로 계면저항을 키운다. 유리 Li₃PS₄ 에서도 straight · spalling 침투가 같은 꼴로 보였다.

⚠ 성장 속도–전류 비례 (604 µm s⁻¹ mA⁻¹) 는 **균열 하나** · 펄스 세트 셋의 맞춤이고, 같은 전류에서도 세트 · 이력에 따라 최대 4 배 다르다 (§10-②).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 재료 | through-plane — Al-LLZO 명목 Li₆.₂₅Al₀.₂₅La₃Zr₂O₁₂ (투명 · RIHP + 1300 °C 50 h 어닐) / in-plane — Al-LLZO (명목 조성 미기재 · RIHP 1225 °C · 1.09 ± 0.1 mm · XRD 98.8 % 입방 가넷 + 1.1 % 리튬 지르코늄 산화물 + 0.1 % 란타넘 지르코늄 산화물) / 황화물 — 유리 LPS ≈300 µm (요약 · 본문 'glassy Li₃PS₄' · SI 합성 절 '25Li₂S–75P₂S₅ (mol %)' ⚠ §10-⑦) · 펠릿 두께 SI p. 5 — LPS 300 µm · LLZO 1.0–1.2 mm |
| 셀 | through-plane Li\|LLZO\|Li (Ni 핀 · ≈350 kPa · 쪼갠 단면을 옆에서 관찰) · in-plane Li\|LLZO\|Li (같은 면에 Li 두 개 · **스택 압력 0** · 위에서 관찰 · 한 펠릿에 크기 셋 39 쌍) · in-plane Li\|LPS\|Li |
| 던지는 질문 | Li 침투가 **언제 · 왜 · 어디서** 생기고 무엇이 경로를 정하나 — 전기 · 화학 · 기계 결합이 사이클 중 어떻게 변하나 |
| 문헌 갭 (본문 정리, p. 1026–1027) | 입계 경로 (Cheng 2017 ref 11 · 입계 국소 기계 물성을 이유로 든 계산 ref 17) · 과전압–균열 응력 · 임계 결함 크기 모델 (Porz 2017 · 단결정 LLZO · 유리 LPS — 입계 없는 SE 에서도 침투) · 일부러 낸 표면 결함보다 전극 가장자리 전류 집중이 먼저 (Swamy 2018) · SE 전자전도 기원 (Han 2019) · 탈리 쪽 공극 · 스택 압력 의존 (Wang · Krauskopf) — **operando 로 형태와 전압을 같이 본 자료가 부족하다** |
| 이 논문의 답 | 형태 4 · 가역 · 균열 열림 (성장 ∝ 전류 · 크리프 되밀림) · 탈리 공극 · 유리 LPS 에도 비슷한 행동 |

---

## 3. 핵심 수치 총정리 ★

> `figure-read` = 그림에서 읽은 값 (본문 미명시) · '우리 산수' = 내가 계산한 값 (가정 같이 적음).

### 3a. 셀 · 계면 상태

| 양 | 값 | 조건 / 출처 |
|---|---|---|
| in-plane 계면저항 (녹인 Li) | **< 5 Ω cm²** (EIS 검출 한계 아래 · 벌크 반원 하나) | 증착 Li 를 **250 °C · 5 min · 무압력**으로 녹였다 식힘 · `Fig. 2F` · p. 1031 |
| 같은 셀 EIS 반원 | `figure-read ≈` 0 → **16 kΩ** (7 MHz → 0.5 Hz) · 단락 후 ≈0 | `Fig. 2F` |
| 증착 그대로 (안 녹임) | 둘째 (계면) 반원 — `figure-read ≈` 벌크 ≈28 kΩ + 계면 ≈15 kΩ | `Fig. S5` (등가회로 R_s–(R_bulk‖Q_bulk)–(R_inter‖Q_inter)) |
| through-plane 단락 후 저항 | **≈100 Ω** ('soft short' — 가는 필라멘트 · 긴 경로) | SI p. 5 · `Fig. S1C` (`figure-read ≈` 80–100 Ω) |
| through-plane 저전류 응답 | 0.11 mA/cm² 까지 계단마다 평탄 · `figure-read ≈` 53 mV @ 0.11 mA/cm² (우리 산수 ≈0.48 kΩ cm² — 1 mm LLZO 벌크 포함) · < 0.1 mA/cm² 에서 형태 변화 없음 | `Fig. S1A` · p. 1028 |
| Li 양 | 모든 셀 > 1.5 mAh/cm² (`Fig. 1` 은 > 500 µm Li 포일 뒷받침) · 방전 실험 셀 ≈8 µm (QCM) | SI p. 2 · p. 1043 |

### 3b. 임계 전류 (CCD) · 안전 전류

| 양 | 값 | 조건 / 출처 |
|---|---|---|
| through-plane 핵생성 | 0.5 mA/cm² 펄스에서 **즉시** 핵생성 → 단락 | `Fig. 1B` — `figure-read ≈` 0.215 V 로 뛴 뒤 ≈125 s 동안 0.155 V 까지 서서히 내려가고 (전파) → ≈0.015 V (단락) |
| in-plane CCD 시험 | 0.25 mAh/cm² 씩 양방향 → 전류 계단. **1 · 5 mA/cm² 평탄 · 침투 없음** · 10 mA/cm² 에서 spalling (왼쪽 전극 좌하 모서리 · 곧 멈춤) → 30 s 뒤 branching (우하 모서리) → 다시 15 s 뒤 단락 | `Fig. 2D,E` · Video S2 · `figure-read ≈` 분극 1 mA/cm² ≈0.08 V · 5 mA/cm² ≈0.33 V · 10 mA/cm² ≈0.65 V |
| 본문 비교 | 보통 through-plane LLZO 셀과 같은 모습이지만 **5–10 배 높은 전류**에서 · 문헌 최고 (중간층 없는 평면 LLZO · 상온 · 스택 압력 있음) 1 mA/cm² · Li/Mg 합금 · MoS₂ 중간층 2 mA/cm² | p. 1031 (refs 8 · 9 · 21 · 22) |
| 안전 전류 분포 (녹인 Li · in-plane) | `figure-read ≈` 13 셀 · **≈2–36 mA/cm²** (대부분 4–10) · 그때 분극 0.05–0.66 V | `Fig. S6` · Video S9 = 작은 계단으로 10 mA/cm² 생존 |
| 높은 CCD 의 저자 해석 | ① 전극 면적이 작아 임계 결함이 들어 있을 확률 ↓ (통계적 취성 파괴 · ref 37) ② Li 를 **녹였다** (보통은 녹는점 바로 아래까지만) | p. 1031 |
| ⚠ 방전 실험 전류 | 4 mA/cm² = '앞서 잰 CCD 바로 아래' | p. 1043 — 어느 셀의 CCD 인지 명시 없음 |

### 3c. 형태 통계 · 기하

| 양 | 값 | 출처 |
|---|---|---|
| 형태 | straight · branching · spalling (흔함) / diffuse (2 회 · 최적화 셀에선 0) | p. 1031 · 1034 |
| branching 과 핵생성 전류 | 검사한 in-plane 셀 18 개 — 핵생성 < 0.2 mA/cm² 면 branching 없음 · > 0.3 이면 항상 있음 | p. 1034 (본문은 'Figure S7' 로 가리킴 → 실제 `Fig. S9`) · `figure-read ≈` 없음 3 점 (0.05 · 0.15 · 0.2) · 있음 ≈10 점 (0.5–75 mA/cm²) |
| 불순물 | 98.8 % 입방 가넷 · 1.1 % 리튬 지르코늄 산화물 · 0.1 % 란타넘 지르코늄 산화물 · 사이클 전부터 있음 | p. 1034 · `Fig. S8` (안 봄) |
| diffuse 셀 | 0.7 · 0.8 · 0.9 mA/cm² 변화 없음 → 1 mA/cm² 에서 흐린 어두워짐 · 분극 변화 거의 없음 → 1.5 mA/cm² 극 반전 뒤 Li 점 더 생김 → 마지막 펄스에 straight 로 단락 | p. 1035–1036 · Video S4 (Li **안 녹인** 셀) |
| straight 균열 3D (성장 측정 균열) | `figure-read ≈` 표면 아래로 얕게 누운 면 · 가로 ≈450 µm · 가장 깊은 곳 ≈75 µm · 그림 주석 '53 µm' | `Fig. S7C` (Keyence z-profile) |
| 균열 벌어짐 | `figure-read ≈` straight 0.5–1 µm (`Fig. S7B`) · spalling 고립 영역 안 균열 수십 nm–0.5 µm (`Fig. 5A,B`) | FIB 단면 · 기울기 보정 없음 |
| 침투 깊이 | 단면에서 Li 침투는 전해질 **위 300 µm 안** | SI p. 5 |
| LLZO 입자 (in-plane) | `figure-read ≈` 35–40 µm (윤곽 그린 입자 하나) — 본문 수치 없음 | `Fig. 9D` |

### 3d. 가역성 · 사이클

| 양 | 값 | 조건 / 출처 |
|---|---|---|
| 셀 | 전극 250 µm × 500 µm · 간격을 넓힘 (`figure-read ≈` 1.2 mm) | p. 1036 · `Fig. 6A` |
| 핵생성 펄스 | 공칭 **75 mA/cm² · 2 s** → 왼쪽 전극에 branching 즉시 | `Fig. 6A,B` · `figure-read ≈` 분극 −2.95 → −2.1 V |
| 반전 (같은 전류 · 2 s) | 왼쪽 구조가 줄어듦 (필라멘트 표면에서 먼저 탈리) · 오른쪽에 새 branching · 거의 모든 Li 제거 = **'무기 SSE 안에서 단락 전 침투 가역성의 첫 직접 관찰'** (저자 주장) | `Fig. 6C–H` · `figure-read ≈` 분극 1.65 → 골 1.43 (≈7.5 s) → **봉우리 1.70 (≈8.15 s) = 왼쪽 Li 소진 순간** → 1.62 V |
| 이후 사이클 | 같은 전하로 5 mA/cm² × 5 사이클 · 10 mA/cm² × 5 사이클 (Movie 5: 75 → 5 (사이클 2–6) → 10 (7–11)) · `figure-read ≈` 분극 ±0.08–0.12 V (5) · ±0.15–0.20 V (10 · 봉우리꼴) | `Fig. 7A` |
| 재도금 자리 | 첫 5 mA/cm² 반주기에 **예전 균열 하나로만** 다시 들어감 (다른 자리는 안 감 — 밑동 공극 가설 · `Fig. 5E`) · 매번 조금씩 더 전진 → 결국 양쪽이 만나 단락 | p. 1038 · `Fig. 7B` |
| dead Li | 둘째 사이클 뒤 고립 Li · 절연 SEI 가 없어 다시 도금하면 **재연결** · 밑동이 탈리 핫스팟이라 매 탈리 반주기마다 다시 고립 | `Fig. 7D` · `Fig. 7E–G` |
| 탈리 · 도금 순서 | 탈리 = **끝 (tip) 먼저** · 도금 = **밑동 (base) 먼저** → 남은 균열 구조는 전자 통로가 아니다 | `Fig. 7H–L` · p. 1038 |
| PEO 대조 | PEO 고분자 전해질은 가역성 거의 없음 (같은 그룹 ref 45) | p. 1036 |

### 3e. 균열 성장 (straight 하나 · `Fig. 8`) ★

| 양 | 값 | 출처 |
|---|---|---|
| 시작 | 음극 쪽 전극 가장자리에 다이아몬드 펜으로 긁고, 공칭 1 mA/cm² 로 긁힘 끝을 넘어 L₀ ≈ 60 µm 자랄 때까지 도금 | SI p. 3 · `Fig. S12` |
| 펄스 세트 | 0.5 · 1 · 2 · 5 mA/cm² · 펄스 시간은 **같은 전하**가 되게 조정 · 세트 3 개 · 펄스 뒤 개회로에서 되밀림 L_relax 측정 | p. 1039–1040 |
| 세트 1 기울기 (그림에 인쇄된 값) | **0.09 ± 0.01 · 1.95 ± 0.05 · 6.77 ± 0.21 · 16.87 ± 0.73 µm/s** (0.5 · 1 · 2 · 5 mA/cm²) · 이어진 0.5 mA/cm² 펄스 **0.36 ± 0.01** | `Fig. 8E` |
| 펄스당 전진 (같은 전하) | `figure-read ≈` 1 · 14 · 24 · 27 µm (0.5 → 5 mA/cm²) | `Fig. 8E` — 같은 전하인데 전진량이 다르다 (§10-②) |
| 비례 상수 | **604 µm s⁻¹ mA⁻¹** · R² = 0.9533 · x 절편 ≠ 0 → **문턱 전류** 존재 (값 미보고) | `Fig. 8G` · p. 1040 |
| 우리 산수 | 0.5 mA/cm² ↔ I_avg ≈ 0.0028 mA (`figure-read`) → 전극 ≈0.0055 cm² (≈0.55 mm²) → 공칭 기준 **≈3.3 µm s⁻¹ per mA cm⁻²** · x 절편 `figure-read ≈` 0.002 mA ≈ **0.4 mA/cm²** (공칭) | `Fig. 8G` |
| 되밀림 | 1 mA/cm² 넘는 펄스 뒤 개회로에서 수축 · 5 mA/cm² 뒤 6 s 동안 **L_relax ≈ 3 µm** · 큰 전류일수록 큼 | p. 1040–1041 · `Fig. 8E,F` (`figure-read ≈` 67 → 64 µm · 2 mA/cm² 뒤 ≈1 µm) |
| 세트 간 차이 | `figure-read ≈` 2 mA/cm² — 6.8 · 6.2 · 4.6 µm/s · 5 mA/cm² — 16.9 · 14 · 12.5 µm/s (세트 1 · 2 · 3) · 최저 전류 0.1–0.4 µm/s | `Fig. 8G` |
| 입자 관통 | 표면에 보이는 입자 **한가운데를 지나는** straight (입계만이 경로가 아님) · 표면 교차선에서 Li 압출 | `Fig. 9C,D` · Video S10 |

### 3f. 깊은 방전 · 공극 (`Fig. 10`, `Fig. 11`) ★

| 양 | 값 | 출처 |
|---|---|---|
| 프로토콜 | 4 mA/cm² · **1 min × 6 + 2 min × 8 = 14 펄스** · 펄스마다 OCV 5 s + EIS · 합 ≈1.5 mAh/cm² ≈7 µm Li · 증착 ≈8 µm → **85–90 % 탈리** | p. 1043 · SI p. 4 (⚠ SI 는 '10 회 뒤 2 min' — §10-⑦) · 우리 산수 1 mAh/cm² = 4.85 µm Li → 1.47 mAh/cm² = 7.1 µm ✓ |
| 분극 | `figure-read ≈` 펄스 1–9 ≈0.24 V 평탄 → 10–14 — 0.30 · 0.32 · 0.37 · 0.46 · **0.71 V** | `Fig. 10D` |
| 면적 비저항 (초기 면적 기준) | `figure-read ≈` 계면 ≈11 (0) → **3–4** (0.07–0.8 mAh/cm²) → 6 (0.93) → 10 → 13 → 20 → **45 Ω cm²** (1.47) · 벌크 58 → 62–66 → **80** · 합 69 → 66–72 → **125** | `Fig. 10E` |
| 겉보기 전극 면적 | `figure-read ≈` 0.55 → 0.31 mm² · **거의 직선 감소** | `Fig. 10F,H` (ImageJ 문턱 → 이진화 → 흰 픽셀) |
| 계면 커패시턴스 | `figure-read ≈` 1.05e-4 → 봉우리 **2.75e-4 F** (0.13 mAh/cm²) → 1.85e-4 (0.53) → **1.0e-4 (0.67) → 0.52e-4 (0.8)** → 0.12e-4 F (1.47) · 0.5–0.8 mAh/cm² 에서 **급락** | `Fig. 10F` · 우리 산수 2.75e-4 F ÷ 0.0055 cm² ≈ **50 mF/cm²** (§10-⑤) |
| 사후 단면 | 탈리 쪽 계면 **공극 여럿** (`figure-read ≈` 얇은 렌즈꼴 · 길이 1–3 µm · 두께 ≲0.4 µm) · 도금 쪽 **밀착** · 여러 곳 확인 · Video S8 3D 재구성 | `Fig. 11` |

### 3g. 유리 LPS (`Fig. 12`)

| 양 | 값 | 출처 |
|---|---|---|
| 펠릿 | ≈300 µm · 200 °C · 4 h · 270 MPa 열간 가압 | SI p. 2 |
| 거동 | CCD 아래는 평탄 · CCD 에서 급상승 (저자 — 공극 때문) → **다음 반주기에** 침투 · straight + spalling · **branching 없음** | p. 1045 · `Fig. 12D,E` |
| 전류 · 전압 | `figure-read ≈` ±2 mA/cm² → ±0.1 V 평탄 · +≈10 mA/cm² 에서 0.6 → 1.0 V 상승 · 이어 −≈10 mA/cm² 에서 첫 침투 · −3 V 근처로 튐 — **CCD 숫자는 본문에 없다** | `Fig. 12C–E` |

### 3h. COMSOL (in-plane 이 대표성 있나)

| 양 | 값 | 출처 |
|---|---|---|
| 가장자리 효과 | through-plane 과 비슷 · `figure-read ≈` 국소 전류 가운데 ≈0.75 · 가장자리 ≈2.1–2.85 mA/cm² (두 기하 모두 1 mm 펠릿) | `Fig. S3D` (모델 인가 전류 미기재) |
| 펠릿 두께 | ≳250–500 µm 면 전극 위 분포가 두께에 둔감 · 100 µm in-plane 은 안쪽 가장자리 `figure-read ≈` 6 mA/cm² | `Fig. S3E,F` · SI p. 5 |
| 전기장 | 전극 사이 얕은 아래 (영역 B) 의 전기장 선이 표면과 거의 평행 → 적층 셀 가운데를 지나는 필라멘트와 같은 상황이라는 주장 | `Fig. S2` · SI p. 5–6 |
| 옴 강하 | 전극 중심 간격 1 mm 로 같게 했을 때 in-plane **0.27 V** · through-plane **0.23 V** | SI p. 6 · `Fig. S4` (안 봄) |
| 매개변수 | D_Li+ 2.8×10⁻¹³ m²/s · D_n 2×10⁻¹⁵ m²/s · C_Li+ 0.019675 mol/cm³ (Li 자리 절반이 이동 가정) · k_d 1.771×10⁻⁴ s⁻¹ · k_r 9×10⁻⁹ m³/(mol s) (둘 다 LiPON 모델에서 가정) · j₀ 0.2 mA/cm² · α 0.5 | `Table S1` · 우리 산수 Nernst–Einstein (298 K) σ ≈ **0.21 mS/cm** |

---
