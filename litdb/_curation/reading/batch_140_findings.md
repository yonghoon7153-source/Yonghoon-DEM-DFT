# batch 140 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-22 · 후보 N-91)

대상: `lee2025_pvp_ptfe_binary_binder_dry_thick_graphite_anode` — J. Lee · C.Y. Son · S. Han · S. Yang · P.J. Kim · D. Lee · J.W. Lee\* · W.-H. Ryu\* · J. Choi\*, "Anode interface-stabilizing dry process employing a binary binder system for ultra-thick and durable battery electrode fabrication", *Chemical Engineering Journal* **503** (2025) 158271 · DOI 10.1016/j.cej.2024.158271 (10 쪽 · SI 16 쪽).
PTFE 섬유화 건식 흑연 음극 (96 : 1 : 3 · 93 µm · 1.5 g/cc) 의 흑연 몫 0.5 wt% 를 PVP 로 바꾼 '이원 바인더' 를 액체 LIB 반쪽 · 전셀 (NCM811) 에서 견준 실험 (LUMO 계산 하나 · 방법 미기재 · DEM · MPM 없음).
쪽 = 학술지 인쇄 쪽 = PDF 쪽 · SI = 받은 보충 PDF 쪽 · 판독 원자료 = `litdb/figures/lee2025_pvp_ptfe_binary_binder_dry_thick_graphite_anode/digitized.csv` (96 행 · 원 래스터 화소) · 고른 의도 대조 = **채움** (카드 §0-1 — 건식 공정 · 이원 바인더 · 건식 후막 셋 다 · 한정 = 액체 LIB 음극 · 공정 · 압력 숫자 없음 · PVP 효과는 FEC 전해질과 묶임).
인용 서지 (질문 k · l 용): Lee et al., Chem. Eng. J. 503 (2025) 158271.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 고체전해질 없음 (액체 LIB 흑연 음극).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] lee2025_pvp_… | 압연 뒤 되돌아옴 측정 없음 · 가까운 것 = 나노압입 하중 제거 곡선의 **국소** 탄성 회복 21.30 % (DG) · 54.04 % (DG-P) (1 사이클 뒤 · HM2000 · 회복 정의 미기재) · 그림 3a 깊이로 센 (h_max − h_last)/h_max = DG-P 54.1 % (표와 맞음) · DG 15.3 % (하중 제거 곡선이 1.33 mN 에서 끊김) | 카드 §3-4 · §4-4 (iv) · 표 S1 · 그림 3a | 인쇄 (표) · 판독 · 카드 산술 | 다공 전극 국소 압입 (전극 두께 회복 아님) · 압입자 · 최대 하중 · 유지 미기재 · 같은 꼴 조건의 han2024 'FEC 있음' 50.42 % 와 2 배 넘게 다름
- [b] lee2025_pvp_… | 1 사이클 뒤 단면 두께 93 → 112 µm (DG) · 98 µm (DG-P) = +20.4 · +5.4 % — 리튬화 · SEI · 결착 붕괴의 결과 (탈압 되돌아옴 아님) | 카드 §3-4 · 그림 S4 · 3e · 3f (글자) | 인쇄 · 카드 산술 | 단면 SEM 한 장씩 · 질량 · 밀도 · 세척 · 건조 조건 [미확인]

## c — 항복 · 경도 · 크리프 값과 정의
- [c] lee2025_pvp_… | 1 사이클 뒤 전극 나노압입 경도 4.21 (DG) · 2.02 MPa (DG-P) · 탄성률 75.00 · 28.20 MPa · 사이클 전 탄성률 4.2 · 8.5 MPa (본문 · 그림 판독 4.1 · 8.9) · 적신 뒤 3.9 · 4.9 MPa [판독] | 카드 §3-4 · 표 S1 · 그림 3b · p.4–5 | 인쇄 · 판독 (1 px = 0.2 MPa) | 다공 복합 전극의 국소 응답 (흑연 · PTFE 고유값 아님) · 일축 항복 환산 없음 · 본문 'DG 78 MPa' ↔ 표 75.00 · 그림 3a 깊이 축 'nm' 은 µm 로 읽어야 표와 맞음 (F/(26.43 h²) = 3.83–4.54 · 1.77–2.14 MPa [카드 산술 · 면적식은 카드 가정])
- [c] lee2025_pvp_… | SAICAS 정규화 수평력 (깊이 50 µm 까지 50 s 뒤 수평 · 끝 5 s 평균) 사이클 전 1.00 · 0.96 · 적신 뒤 0.70 · 0.91 · 1 사이클 뒤 0.46 · 0.99 (DG · DG-P) — 원문 *"almost twice higher adhesion strength"* | 카드 §3-4 · 그림 3d · S3 · p.6 | 판독 | 접착 · 응집 지표 (항복 아님) · 정규화 기준 · 칼날 폭 · 속도 미기재

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 하중 몫 측정 없음 (흑연 + 고분자 바인더 · 압연 압력 미기재).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · DEM 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 2D → 3D 진술 없음 (단면 · 윗면 SEM 은 정성 · 두께 한 축).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 복합 양극 아님 (액체 LIB 흑연 음극) · 압력별 기공 없음 (전극 밀도 1.5 g/cc 하나 · 진밀도 미기재 · 30.16 mg/cm² 후막의 두께 · 밀도 미인쇄).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
- [j] lee2025_pvp_… | 원문에 '한계' 절 없음 · 카드가 적은 원문 공백: 혼합 · 반죽 · 압연 · 라미네이트 조건 · 기공 · 진밀도 · 셀 수 · 오차 막대 · 나노압입 조건 · R_ion 추출식 · LUMO 계산법 [미확인] | 카드 §0 ⑨ · §11 · [미확인] 목록 | 카드 서술 | 가압 · 탈압 계산에 넣을 압력 · 기공 값이 없다
- [j] lee2025_pvp_… | 원문 스스로 PVP 만으로는 PTFE 환원을 다 못 막는다: *"These results indicate that the reductive decomposition of PTFE cannot be addressed entirely without an electrolyte additive that forms LiF-based SEI species."* (p.7 · LiClO₄ · FEC 없음 대조에서 부산물 비 56.7 vs 52.2 %) | 카드 §3-5 · 그림 S6 · `txt_p7_liclo4_control_fec_needed.png` | 인쇄 | 액체 LIB 음극 전위의 일 (흐름 밖 — PTFE 규약)

## k — DEM 의 한계 (서지: Lee et al., Chem. Eng. J. 503 (2025) 158271)
- [k] lee2025_pvp_… (Lee 2025 · Chem. Eng. J.) | **말 없음** — DEM · 연속체 · 접촉 모델이 없다 (계산은 LUMO 분자 계산 하나 · 함수 · 기저 · 프로그램 미기재) | 카드 §4-4 (i) · §0 ⑩ | 카드 서술 | —

## l — 소성변형이 왜 어려운가 · 우회 (서지: Lee et al., Chem. Eng. J. 503 (2025) 158271)
- [l] lee2025_pvp_… (Lee 2025 · Chem. Eng. J.) | **계산 쪽 논의 없음 · 우회 없음 (맞춘 값 0)** — 실측 해석만: 탄성률 정의 *"the stress–strain ratio when a tensile or compressive load is applied. A Lower elastic modulus can provide better elastic properties and flexibility against external forces"* (p.4) · DG-P 는 PTFE 섬유의 *"original flexibility"* 를 유지해 *"the DG-P electrode can withstand the mechanical stress caused by volumetric changes in graphite during repetitive charging and discharging"* (p.5) | 카드 §3-4 · §4-4 (ii) · `txt_p4p5_nanoindentation_modulus_recovery.png` | 인쇄 | 바인더 (고분자) 의 유연성 서술 — 입자 소성 · 형상 변화 논의 아님

## m — 받아들일 통찰
- [m] lee2025_pvp_… | **문헌 수명 '% 유지' 의 기준 사이클을 등록 칸으로** — 이 논문 인쇄 93 · 87 · 86.3 % 는 형성 (0.05 · 0.1 C) 둘 뒤 3 번째 사이클 기준이어야 재현되고 1 번째 기준이면 89.5 · 84.3 · 80.5 % [판독 산술] | 자리: 단계 0; 흐름 밖: 사이클 열화 (A10) 문헌 대조 표 | 왜: 카드 §3-7 · 그림 5c · 5d · digitized.csv
- [m] lee2025_pvp_… | **전극 국소 나노압입 값은 논문 사이에서 재현되지 않는다 → 같은 논문 안 상대비로만** — 같은 랩 · 같은 96 : 1 : 3 · 같은 VC + FEC 전해질 · 같은 HM2000 인데 1 사이클 뒤 탄성률 75.00 ↔ 17.80 MPa (4.2 배) · 경도 4.21 ↔ 1.33 · 회복 21.30 ↔ 50.42 % (han2024) · ICE · 두께는 거의 재현 → 문헌 전극 압입값을 우리 연화 배수 · 접촉 강성 · 바인더 상의 근거로 옮기지 않는다 | 자리: 결과 전 대조 항목 (쓰지 않음 표지); 흐름 밖: 바인더 기계 상 | 왜: 카드 §3-8 · §7-3
- [m] lee2025_pvp_… | **PTFE Li 소모는 바인더 조성만이 아니라 '먼저 덮는 계면 상' 의 함수** — F 없는 LiClO₄ 대조에서 PVP 유무 부산물 비 차 4.5 %p (FEC 전해질 17.7 %p) · 비가역 차 24 mAh/g = han2024 상한 (PTFE 3 wt% 전량 탈불소 · 흑연 기준 ≤ 33.5 mAh/g) 의 72 % [카드 산술 · g 기준 미기재] → STEP3 PTFE 불활성 (CL-60) 을 전위별로 적고, ASSB 음극 복합체 · 분리막 PTFE 를 다룰 때 Li 재고 항을 '바인더 조성 + 계면 상' 으로 결과 전 등록 | 자리: 흐름 밖: PTFE 규약 · Li 재고 · R_int 원장 | 왜: 카드 §3-5 · §7-4
- [m] lee2025_pvp_… | **문헌 그림의 축 단위 · 본문 값은 표 · 다른 그림으로 검산한 뒤 쓴다** — 한 논문에서 압입 깊이 'nm' (→ µm · F/(26.43 h²) 로 표 경도와 맞춤) · 전셀 용량 'mAh/cm²' (값 범위 0–230 = mAh/g · 그림 5a 로 나누면 양극 활물질 25.9–26.0 mg/cm²) · 본문 78 ↔ 표 75.00 MPa · 그림 2c 인쇄 ICE 85.1 % ↔ 같은 그림 용량비 ≈87.7 % 가 나왔다 | 자리: 단계 0 (문헌 값 등록 전 검산 칸) | 왜: 카드 §3-3 · §3-4 · §3-7 · §11

## n — 논문 에이전트 후보 (카드가 인용 · 언급했지만 litdb 에 카드가 없는 것)
- [n] T. Lee, J. An, W.J. Chung, H. Kim, Y. Cho, H. Song, H. Lee, J.H. Kang, J.W. Choi, Non-electroconductive polymer coating on graphite mitigating electrochemical degradation of PTFE for a dry-processed lithium-ion battery anode, ACS Appl. Mater. Interfaces 16 (7) (2024) 8930–8938, https://doi.org/10.1021/acsami.3c18862. (ref [14]) | m · j — 흑연을 고분자로 덮어 PTFE 분해를 줄이는 같은 발상의 선례 · 'PTFE Li 소모 = 계면 상의 함수' 의 두 번째 근거 (PVP 효과를 가를 대조) — 카드 §12 | papers/ 목록 (lee2024* 셋 = 다른 논문) · 'acsami.3c18862' · 'Non-electroconductive' grep 0 건 (후보 표 · wishlist 에도 없음) → 카드 없음
- [n] R. Tao, S. Tan, H.M. Meyer Iii, X.-G. Sun, B. Steinhoff, K. Sardo, A. Bishtawi, T. Gibbs, J. Li, Insights into the Chemistry of the Cathodic Electrolyte Interphase for PTFE-Based Dry-Processed Cathodes, ACS Applied Materials & Interfaces 15(34) (2023) 40488-40495, https://doi.org/10.1021/acsami.3c07225. (ref [30]) | m — **양극 쪽** PTFE 계면 화학 = 우리 STEP3 'PTFE = 양극 전위에서 불활성' (CL-60) 을 직접 볼 자료 (액체 LIB) — 카드 §12 · §7-4 | papers/ 목록 (tao* 없음) · 'acsami.3c07225' · 'Cathodic Electrolyte Interphase' grep 0 건 → 카드 없음
- [n] J.Y. Kim, J. Park, M.J. Lee, S.H. Kang, D.O. Shin, J. Oh, J. Kim, K.M. Kim, Y.-G. Lee, Y.M. Lee, Diffusion-Dependent Graphite Electrode for All-Solid-State Batteries with Extremely High Energy Density, ACS Energy Letters 5(9) (2020) 2995-3004. https://doi.org/10.1021/acsenergylett.0c01628. (SI ref [4]) | i · m — 표 S3 의 유일한 **전고체** 흑연 전극 (6.21 mg/cm² · 2 mAh/cm²) · ASSB 음극 복합체 (흑연 + 황화물 SE) 의 압밀 · 수송 자료 후보 — 카드 §12 · §3-7 | papers/ 목록 (kim2020* 없음) · 'Diffusion-Dependent' · 'acsenergylett.0c01628' grep 0 건 → 카드 없음
- [n] M. Ryu, Y.-K. Hong, S.-Y. Lee, J.H. Park, Ultrahigh loading dry-process for solvent-free lithium-ion battery electrode fabrication, Nat. Commun. 14 (1) (2023) 1316, https://doi.org/10.1038/s41467-023-37009-7. (ref [15]) | m (흐름 밖: 후막 · 건식 공정) — 초고부하 건식 공정 · 이 랩 카드들 (han2024 · lee2026_li · kim2026 · 이 카드) 이 못 준 공정 조건 숫자 (rpm · 시간 · 롤 하중) 의 후보 — 카드 §12 | papers/ 목록 (ryu* 없음) · 'Ultrahigh loading dry' · 's41467-023-37009' grep 0 건 → 카드 없음
- [n] Y. Suh, J.K. Koo, H.-J. Im, Y.-J. Kim, Astonishing performance improvements of dry-film graphite anode for reliable lithium-ion batteries, Chem. Eng. J. 476 (2023) 146299, https://doi.org/10.1016/j.cej.2023.146299. (ref [13]) | m (흐름 밖: 건식 음극) — 건식 흑연 음극의 선례 · PTFE 음극 열화 대조 — 카드 §12 | papers/ 목록 (suh* 없음) · 'Astonishing' · '146299' grep 0 건 → 카드 없음

## 카드 문제
- 없음 — 가리킨 두 카드의 2 차 인용 서지는 원문과 같다: `kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode` **L382** (ref 7 · *"Lee, J. et al. … Chem. Eng. J. 503, 158271 (2025)"* · *"그 목록에는 J. Choi 가 저자로 인쇄"* = 맞음) · `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` **L412** (ref 20 · 저자 9 명 · 제목 · 503 (2025) 158271 = 원문 p.1 과 같음).
- 보탤 정보 (그 카드는 고치지 않음): `kim2026_pregranulation_…` §12 '같은 그룹 후보' 표 머리의 *"'J. Choi' 가 Junghyun Choi 인지는 머리글자만이라 [미확인]"* — 이 논문 (ref 20) 에 대해서는 원문 p.1 *"Junghyun Choi e,\*"* (가천대 · 교신 · junghchoi@gachon.ac.kr) 로 풀린다 (한글 이름은 여전히 미인쇄).
- 다른 후보 행 참고 (카드 문제 아님): 이 논문 참고 [20] 은 N-92 를 *"J. Kim, K. Park, M. Kim, H. Lee, J. Choi, H.B. Park, H. Kim, J. Jang, Y.-H. Kim, T. Song, **U. Paik**, … Adv. Energy Mater. 14 (10) (2024) 2303455"* (11 명) 로 적는데, 후보 표 N-92 행 (`kim2026_*` L410 표기) 은 U. Paik 없이 10 명이다 — 두 인용 목록이 다르다 · N-92 원문 첫 쪽으로 가린다.
- 원문 자체 어긋남 (카드 문제 아님 · 카드 §3-9 · §11 에 적음): 본문 DG 사이클 뒤 탄성률 78 ↔ 표 S1 · 그림 75.00 MPa · 본문 DG-P 사이클 전 8.5 ↔ 그림 ≈8.9 [판독] · *"after the initial cycle, the DG electrode exhibited a slight volume expansion of 5 %"* = 그림 3f 의 DG-P (98 µm) 로 읽힘 · 그림 2c 인쇄 ICE 85.1 · 92.4 % ↔ 같은 그림 용량비 ≈87.7 · ≈93.1 % · 그림 3a 축 'nm' · 그림 S10 축 'mAh/cm²' · 부산물 식 분모 'CH₄' (대조 식은 'CF₄') · LUMO 서술 'first' ↔ 'simultaneously' ↔ 'FEC 먼저' · p.3 '(Fig. 3c)' = XPS 그림 · 오타 'socked' · 'samlpes' · 'spertra' · 'obtaning' · 'Horbia' · 'After cyclng'.
