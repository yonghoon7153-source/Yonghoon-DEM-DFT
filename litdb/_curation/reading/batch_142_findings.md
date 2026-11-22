# batch 142 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-22 · 후보 N-93)

대상: `kwon2024_low_resistance_dry_ptfe_lfp_thick_electrode` — K. Kwon · J. Kim · S. Han · J. Lee · H. Lee · J. Kwon · J. Lee · J. Seo · P.J. Kim\* · T. Song\* · J. Choi\*, "Low-Resistance LiFePO4 Thick Film Electrode Processed with Dry Electrode Technology for High-Energy-Density Lithium-Ion Batteries", *Small Science* **4** (5) (2024) 2300302 · DOI 10.1002/smsc.202300302 (10 쪽 · SI 17 쪽).
같은 LFP : Super P : 바인더 = 97 : 1 : 2 를 습식 (PVDF · NMP 슬러리 · 2.1 g/cc · 190 µm) 과 건식 (PTFE 섬유화 · 행성 혼합기 + 막자 · 60 °C 압착 라미네이트 · 2.3 g/cc · 175 µm) 으로 만들어 액체 LIB 반쪽 셀 (5.5 mAh/cm²) · 흑연 전셀 (7.8 mAh/cm² 후막 포함) 에서 견준 실험 (DEM · MPM · 모델 없음).
쪽 = 학술지 인쇄 쪽 = PDF 쪽 · SI = 받은 보충 PDF 쪽 · 판독 원자료 = `litdb/figures/kwon2024_low_resistance_dry_ptfe_lfp_thick_electrode/digitized.csv` (225 행 · 본문 = 원 래스터 화소 · SI = 300 dpi 렌더) · 고른 의도 대조 = **일부** (카드 §0-1 — '건식 공정' · '건식 LFP 후막' 채움 · 'ΔV 0.22 V' 는 원문 인쇄값이 아니고 같은 부하의 습식 ↔ 건식 CV 봉우리 간격 0.83 ↔ 0.61 V 의 차로만 나옴 · '슬러리 로딩 증가' 계열 없음).
인용 서지 (질문 k · l 용): Kwon et al., Small Sci. 4 (2024) 2300302.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 고체전해질 없음 (액체 LIB LFP 양극).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 압착 · 라미네이트 · 캘린더 하중도, 하중을 뺀 뒤 두께 회복도 측정 없음 (최종 두께 190 · 175 µm 만 · 카드 §4-4 (iv)).

## c — 항복 · 경도 · 크리프 값과 정의
- [c] kwon2024_low_resistance_… | SAICAS 깊이별 정규화 수평력 F_H (30 · 60 · 90 · 120 µm): 습식 30 µm ≈1.0 → 60–120 µm ≈0.88–0.90 = 원문 *"decreases (by approximately 12%) as the depth increases from the top to the middle and bottom points"* · 건식 네 깊이 ≈1.0 (*"nearly similar adhesion strengths"*) | 카드 §3-3 · 그림 3b · 3c · p.2–3 · `txt_p2p3_saicas_wet_12pct_binder_migration.png` | 인쇄 (12 %) · 판독 (눈대중 · 축 0.3 간격 · digitized.csv 에 없음) | 접착 · 바인더 분포 지표 (항복 아님) · 정규화 기준 · 칼날 속도 미기재 · 축 이름 'Normalized … (N)' · 가로축 = 시간 · 원문 가정 *"proportional to the binder ratio"*

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 하중 몫 측정 없음 (LFP + 고분자 바인더 · 압력 미기재).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · DEM 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 2D → 3D 진술 없음 (단면 SEM · TEM 은 정성 · 전기화학은 두께 한 축).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 복합 양극 (AM + SE) 아님 · 압력별 기공 없음 (액체 LIB 전극 캘린더 뒤 Hg 기공 39.5 · 38.2 % 두 값 · 압력 미기재 — 측정 규약 근거로만 m 에 적음).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
- [j] kwon2024_low_resistance_… | 원문에 '한계' 절 없음 · 카드가 적은 원문 공백: 혼합 rpm · 시간 · 막자 반죽 · 60 °C 압착 하중 · 캘린더 하중 · 간극 · 횟수 · LFP 입경 · 셀 수 · 오차 막대 · 측정 온도 · 대칭 셀 전해질 · 면적 · R_ion 추출 모형 · N_M · τ 식 · R_ct 숫자 · 300 사이클 유지율 · 에너지 밀도 계산식 [미확인] | 카드 §0 ⑧ · §11 · [미확인] 목록 | 카드 서술 | 가압 · 탈압 계산에 넣을 압력 값이 없다
- [j] kwon2024_low_resistance_… | 원문이 적은 습식의 제조 한계: *"A high-density wet-processed electrode could not be fabricated at high areal capacity (>2.2 g cc⁻¹, >5 mA h cm⁻²) because of delamination between electrode layer and current collector."* (p.4) · 7.8 mAh/cm² · 2.3 g/cc 습식은 균열 (그림 S11 · p.7) | 카드 §3-5 · §3-7 · `txt_p4p5_hg_porosity_382_395_delamination_22gcc.png` · `txt_p7_78mah_23gcc_wet_cracks_300cycles_previous_3mah.png` | 인쇄 · 사진 (정성) | 밀도 · 부하 문턱만 (압력 · 접착 숫자 없음) · 액체 LIB 습식 전극의 일

## k — DEM 의 한계 (서지: Kwon et al., Small Sci. 4 (2024) 2300302)
- [k] kwon2024_low_resistance_… (Kwon 2024 · Small Sci.) | **말 없음** — DEM · 연속체 · 접촉 모델이 없다 (본문 식 0 · SI 식 (1) = GITT 확산 계수 식 하나) | 카드 §4-4 (i) · §0 ⑨ | 카드 서술 | —

## l — 소성변형이 왜 어려운가 · 우회 (서지: Kwon et al., Small Sci. 4 (2024) 2300302)
- [l] kwon2024_low_resistance_… (Kwon 2024 · Small Sci.) | **계산 쪽 논의 없음 · 우회 없음 (맞춘 값 0)** — 기계 쪽 문장은 *"a dry process, which uses polytetrafluoroethylene (PTFE) as a deformable binder, has emerged as a potential method for fabricating thick electrodes without using any solvent"* (p.2) 와 섬유화 · 압착 서술뿐 · 사이클 뒤 습식 LFP 입자 균열의 원인은 인용으로만: *"It would be attributed to the high stress of inserting and extracting Li ions in the particles of the wet-processed LFP electrode."* (p.6 · 참고 [42] · 응력 측정 없음) | 카드 §4-4 (ii) · §3-6 · `txt_p2_wet_issues_nmp78_three_dry_steps_lfp_not_reported.png` · `txt_p6_ptfe_xrd_18deg_unreacted_wet_particle_cracks.png` | 인쇄 | 바인더 변형 · 사이클 균열 서술 — 입자 소성 계산과 무관

## m — 받아들일 통찰
- [m] kwon2024_low_resistance_… | **같은 이름 'ΔV' 가 두 양이다 → 문헌 ΔV 는 정의와 함께 등록** — 같은 5.5 mAh/cm² 에서 CV 봉우리 간격 0.83 ↔ 0.61 V (그림 4b 글자 · 원문 '26% lower') 와 첫 사이클 정전류 평탄 차 ≈0.26 ↔ ≈0.10 V [판독] 가 다르고, 2 차 인용 (kang2026 L170 *"ΔV 최대 0.22 V"*) 은 CV 간격의 차 (0.22) 를 정전류 ΔV (≈0.14) 옆에 놓았다 → 결과 전 대조 칸에 문헌 ΔV 를 넣을 때 정의 (CV 간격 · 주사 속도 / 정전류 · C-rate · 평탄 구간) 를 같은 칸에 적는다 | 자리: 단계 0 (문헌 값 등록 전 정의 칸); 흐름 밖: STEP4 전압 히스테리시스 대조 | 왜: 카드 §0-1 · §3-4 (a)(b) · digitized.csv (Fig 4a)
- [m] kwon2024_low_resistance_… | **정의식이 없는 문헌 'τ' 는 τ = ε·N_M 산술로 tau2 ↔ √ 를 가른다** — 그림 5c 막대 22.29 × 0.395 = 8.80 · 4.34 × 0.382 = 1.66 (두 전극 모두 판독 정밀도 안) → 원문 τ = 우리 tau2 · 같은 그림의 N_M 비 5.14 ↔ R_ion × 두께 비 5.16–5.21 로 N_M ∝ R_ion/d 계산도 확인 [카드 산술] | 자리: 결과 전 대조 항목; 흐름 밖: τ 명명 규약 (J 축) | 왜: 카드 §3-5 · 그림 5a · 5c · digitized.csv (Fig 5c)
- [m] kwon2024_low_resistance_… | **기공률이 거의 같아도 (39.5 ↔ 38.2 %) 바인더 형태 · 분포만으로 기공 쪽 tau2 ×5.3 · R_ion ×5.7** — 수송 tortuosity 를 ε 만의 함수 (Bruggeman 류) 로 읽지 않는다 · 우리 침대의 첨가제 표현 규약 (STEP3 PTFE `centerline` = 중심선 한 셀 절연 · 표면 막 없음 · CL-60) 이 수송 결과를 바꿀 수 있다는 크기 감각 (액체 기공 상 · 값 전이 금지) | 자리: 단계 7; 흐름 밖: STEP3 PTFE · 첨가제 규약 | 왜: 카드 §3-5 · §7-3 · §7-4 · BET 11.6 / 9.5 / 11.9 m²/g (그림 2e)
- [m] kwon2024_low_resistance_… | **문헌 기공 + 명목 밀도로 골격 밀도를 검산한 뒤 판정 기준으로 쓴다** — 같은 97 : 1 : 2 인데 2.1/(1−0.395) = 3.47 ↔ 2.3/(1−0.382) = 3.72 g/cm³ (표 S1 평균 밀도로도 3.47 ↔ 3.73) → 기공 측정법 (Hg) · 분모 · 시료가 명목 밀도와 같은 골격으로 맞는지 결과 전 대조 칸에서 확인 (안 맞으면 어느 쪽을 기준으로 쓸지 먼저 정한다) | 자리: 단계 0 | 왜: 카드 §3-5 · §7-2 · 표 S1 · 그림 5b · SI 그림 S5

## n — 논문 에이전트 후보 (카드가 인용 · 언급했지만 litdb 에 카드가 없는 것)
- [n] P. Zhu, P. R. Slater, E. Kendrick, Mater. Des. 2022, 223, 111208. (원문 참고 [35] 그대로 · 제목 · DOI 없음 = 서지 일부만) | m (흐름 밖: τ 명명 규약 J 축) — 이 논문이 N_M · τ 를 정의한다고 가리킨 원전 (그림 5c · 식 미인쇄) · τ = ε·N_M 꼴인지 원문으로 확정 — 카드 §3-5 · §12 | papers/ 목록 (zhu2022* 없음) · '111208' grep 0 건 → 카드 없음 (후보 표 · wishlist 에도 없음)
- [n] M. S. Hossain, L. I. Stephens, M. Hatami, M. Ghavidel, D. Chhin, J. I. G. Dawkins, L. Savignac, J. Mauzeroll, S. B. Schougaard, ACS Appl. Energy Mater. 2020, 3, 440. (원문 참고 [36] 그대로 · 제목 · DOI 없음 = 서지 일부만) | m (흐름 밖: τ 명명 규약 J 축 · 기공 쪽 수송 측정) — N_M · τ 정의의 두 번째 원전 — 카드 §3-5 · §12 | papers/ 목록 (hossain* 없음) · 'Hossain' · 'Schougaard' grep 0 건 → 카드 없음 (후보 표 · wishlist 에도 없음)
- [n] Y. Itou, N. Ogihara, S. Kawauchi, J. Phys. Chem. C 2020, 124, 5559. (원문 참고 [32] 그대로 · 제목 · DOI 없음 = 서지 일부만) | m · 흐름 밖 (B 축 · 대칭 셀 R_ion) — 이 논문 R_ion (대칭 파우치 셀) 의 방법 원전 · 추출 모형 (TLM 등) · 전해질 조건을 이 원전으로 채운다 — 카드 §3-5 · §12 | papers/ 목록 (itou* 없음) · '5559' grep 0 건 (wishlist 의 Ogihara 2012 JES 159 A1034 = 다른 논문) → 카드 없음
- [n] A. Nickol, T. Schied, C. Heubner, M. Schneider, A. Michaelis, M. Bobeth, G. Cuniberti, GITT analysis of lithium insertion cathodes for determining the lithium diffusion coefficient at low temperature: challenges and pitfalls, Journal of The Electrochemical Society, 167 (2020) 090546. (SI 참고 [1] 그대로 · 본문 참고 [25] 는 제목 없음) | m (흐름 밖: STEP4 D_s 문헌 대조) — SI 식 (1) 의 출처 · 2 상 평탄 GITT 의 함정 (이 논문은 펄스 조건 · 기호 정의가 그림과 어긋남) — 카드 §3-4 (c) · §12 | papers/ 목록 (nickol* 없음) · '090546' · 'GITT analysis of lithium insertion' grep 0 건 → 카드 없음
- [n] Y. Zhang, S. Lu, F. Lou, Z. Yu, Solvent-free lithium iron phosphate cathode fabrication with fibrillation of polytetrafluoroethylene, Electrochimica Acta, 456 (2023) 142469. (SI 참고 [5] 그대로) | 흐름 밖: 후막 · 건식 공정 · 믹서 V2 — 표 S2 의 앞선 PTFE 섬유화 건식 LFP (3.1 mAh/cm² · 2.0 g/cc · LFP 90 %) = 이 논문의 '처음 보고' 주장과 견줄 자료 · 혼합 · 섬유화 조건 숫자의 후보 — 카드 §3-7 · §12 | papers/ 목록 (zhang2023* = pfib 4D 영상 한 편뿐 · 다른 논문) · '142469' · 'Solvent-free lithium iron phosphate' grep 0 건 → 카드 없음

## 카드 문제
- `kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode` **L170** *"(p.8; 문헌 슬러리 로딩 증가 시 ΔV 최대 0.22 V, ref 40)"* — ref 40 = 이 논문인데 원문 (본문 10 쪽 + SI 17 쪽) 에 **로딩을 늘린 습식 계열이 없고 '0.22' 인쇄값도 없다** · 0.22 V 는 같은 5.5 mAh/cm² 의 습식 ↔ 건식 CV 봉우리 간격 (0.83 ↔ 0.61 V) 의 차로만 나온다 [카드 산술] · 같은 줄이 나란히 둔 Kang 의 ΔV ≈0.14 V 는 정전류 평탄 차라 다른 양 · 그 줄이 Kang 원문 p.8 의 문장을 옮긴 것인지 카드의 풀어 쓰기인지는 Kang PDF 대조 전 [미확인] (고치지 않음).
- `kang2026_*` **L386** ('왜 · 카드' 칸 *"건식 LFP 후막 (ΔV 0.22 V 비교의 출처 …)"*) — 서지 줄 자체는 원문과 같다 · '비교의 출처' 는 위 L170 과 같은 한정 (로딩 증가 비교는 원문에 없음).
- 서지 줄 = 원문과 같음: `kang2026_*` L386 (ref 40) · `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` L414 (ref 23 · 저자 11 명 · Small Sci. 4 (5) (2024) 2300302) · `han2024_fec_mitigates_ptfe_decomposition_dry_thick_graphite_anode` L343 (ref 15) · `lee2025_pvp_ptfe_binary_binder_dry_thick_graphite_anode` L348 (ref 35).
- 보탤 정보 (그 카드는 고치지 않음): `kim2026_pregranulation_…` **L405** 표 머리 *"'J. Choi' 가 Junghyun Choi 인지는 머리글자만이라 [미확인]"* — 이 논문 (ref 23) 에 대해서는 원문 p.1 *"Junghyun Choi\*"* (KICET + 가천대 배터리공학과 · 교신) · SI p.1 junghchoi@gachon.ac.kr (kim2026 L21 의 J. Choi 전자우편과 같은 글자) 로 풀린다 (한글 이름은 여전히 미인쇄).
- 보탤 정보: `han2024_fec_…` L343 의 *"전셀 양극 공정 (§11-15) 을 채울 후보"* — 이 논문은 LFP : Super P : 바인더 **97 : 1 : 2** (han2024 전셀 LFP 는 94 : 3 : 3 · 같은 LFP-NCO · 같은 과제 20024261) 라 그 공정을 그대로 채우지 않는다 · 그 카드 머리에는 팔로우 랩 태그 줄 *"[팔로우 랩: 가천대 최준현 교수 (건식 전극)]"* 이 없다 (교신 Junghyun Choi · 같은 태그를 단 lee2025_pvp · kim2026 · kang2026 · lee2026_li 와 다름 · 고치지 않음).
- 후보 표 N-93 행의 'litdb 확인' (*"2300302 grep = 위 두 카드 (인용만)"*) — 지금은 han2024 (L343) · lee2025_pvp (L348) 까지 넷 (인용만) · 카드 없음 판정은 맞음.
- 원문 자체 어긋남 (카드 문제 아님 · 카드 §3-8 · §11 에 적음): 본문 1 C 유지율 *"wet- and dry- … 89% and 80%, respectively"* ↔ 그림 4d 판독 습식 80.0 · 건식 89.4 % · CV 주사 속도 본문 · 캡션 1 ↔ 방법 0.1 mV/s · GITT 0.1 mA/cm² · 30 분 휴지 ↔ 그림 S3 휴지 ≈604 s · 그림 4c 충전 ≈35 000 s · 그림 S1 점 ≈33 개 (전 충전에 ≈1.0–1.1 mA/cm² 필요 [카드 산술]) · SI 식 (1) m_B · M_B 정의 뒤바뀜 · XPS PTFE 689.9 eV ↔ 그림 S7c ≈687.5 eV [판독] · 본문 패널 글자 (S7a,b / c,d) ↔ SI 캡션 배치 · XRD PTFE 18° ↔ 별표 ≈17.0° (LFP 분말에도 ≈17.1° 봉우리) · 전셀 1 C *"approximately 75%"* ↔ 판독 71.1 % · R_ion '83 %' ↔ 그림 글자 82.3 % · 표 S1 'Cathode Current Density' (mAh/cm²) = 부하 × 0.158 설계값 · Wet 1 유지율 85.9 ↔ 재계산 87.2 % · 부피 용량 376.8 ↔ 표 S3 기준 ≈345 mAh/cm³ · 470 Wh/L = '+ High Density LFP' 가정 칸 · '처음 보고' ↔ 표 S2 [5] 건식 PTFE LFP · 그림 S12 축 이름 'mAh/g' · 'V vs Li/Li⁺' · 그림 7 '140µm ≥' · EIS '250 kHZ to 10 MHz' · R_ion '1–1 MHz' · 그림 5c 범례 'Tortusity' · 본문 *"outperforms the that"*.
