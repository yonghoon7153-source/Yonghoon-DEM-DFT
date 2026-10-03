# 판단 메모 v2 부록 2 — 추가 문헌 10 편 (tortuosity_3) 흡수 (2026-10-03 저녁 · 서브 세션)

> 짝 문서: 판단 메모 v2 `docs/reviews/tau_conventions_judgment_v2_20261003.md` · 부록 1 `docs/reviews/tau_conventions_judgment_v2_addendum_lit10_20261003.md`.
> 카드 = 정본 litdb (`claude/friendly-meitner-lldvar`) 커밋 `8e3d7a5d7` — 새 카드 10 · 그림 (103 장 전수 열람 · 손 크롭 45 장 (교체 32 · 추가 13 · 스캔 두 편 Molerus · Kakar 는 전부 손 크롭)) · INDEX_DEM · comparison J 절.
> 1저자 지시: *"이거 먹여줄게"* (문헌 표 2 · 3 순위) → PDF 묶음 `tortuosity_3.zip` (10 편 · **James 1977 은 구하지 못함** · Minnmann 2021 은 정본 카드가 이미 본문 + SI 원문 대조 끝 — 요청 표에서 내가 잘못 넣었다).
> ⚠ 이 부록은 **결정 16 의 권고를 바꾸지 않는다** (10 편 모두 "no").  바뀌는 것은 사전등록 항목 · 한정어 · 메모 v2 의 쪽 번호 근거다.  쪽 번호는 인쇄 쪽 (규율 ⑥) · 수치 표지 = stated (원문) / 판독 (그림) / 카드 산술.

## §0. 결론 여덟 줄
| # | 결론 | 근거 (카드 · 쪽) |
|---|---|---|
| ① | **결정 16 권고 변경 없음** — 10 편 각자 관련 결정을 대조했고 전부 "권고 변경 no" | 각 카드 §8 |
| ② | **M-factor 원전 닫힘** — Wiedenmann 2013 Eq 11 σ_eff/σ₀ = εβ/τ_geo, 지수 전부 1 · 맞춘 매개변수 0 (유도 가정 Eq 5 의 값).  원문에 'M-factor' 낱말 없음 → 부록 1 §2 "부분 해소" → **해소** · "경험 지수는 원전에도 없다" | `wiedenmann2013_…` p.1448 |
| ③ | **Park σ₀ 조성식의 출처는 [18a–c] 어디에도 없다** — Jung 2019 (= [18b]) 본문 10 쪽 + SI 10 쪽 전수, S/cm 수치는 인용값 하나 → **출처 미상 모형 입력** · Park 역산 tau2 = 추세 전용 유지 | `jung2019_…` p.22967–22976 · SI |
| ④ | **COMSOL τ_F 칸 = tau2 근거가 둘 늘었다** — Thorat Eq 1 (κ_eff = κε/τ) + α 1.5 → τ_F = ε^−½ 꼴 · Kato Eq 2 κ_eff = (ε/τ)κ ("tortuosity factor") → 결정 5 지지.  배터리 인터페이스 GUI 캡처는 여전히 필요 | `thorat2009_…` p.592–598 · `kato2018_…` p.609 |
| ⑤ | **결정 9 의 c² 는 이 묶음으로 못 정한다** — Kakar 1967 실측 밀도 ≲ 0.71 (Arzt 띠 0.84–0.90 밖) · Molerus 의 f = πδh 는 c² = 1 (기하 절단 — E2 값으로 쓰지 않는다).  두 끝 1.27 · 1.40 유지 + 기구 · 밀도 한정어.  E3 꼴 (A = F/p_f) 의 원전 = Molerus · "다이 압밀 국소압" 단서는 Molerus 가 아니라 Arzt 문장 | `kakar1967_…` p.3223–3228 · `molerus1975_…` p.263–265 |
| ⑥ | **τ_e (결정 13) — 부호 불정 유지, 진단 항목이 구체화** — Malifarge 해석식은 레일 대칭 (이온/전자 레일을 스펙트럼 하나로 못 가름 → 독립 σ_el,eff 필요) · Morasch 구배만으로 −46…+66 % (모의) · 같은 전극 정/역 2.12× · Cooper 는 τ_e 지배식 원전이 아니다 (부피 축전 확산 FD 틀) | `malifarge2017_…` E3330–E3331 · `morasch2018_…` A3462–A3465 · `cooper2017_…` p.683 · 687 |
| ⑦ | **전자 tau2 (결정 14) — "f 만" 쪽을 지지** — Asano σ_e 가 SOC 0 → 50 % 에서 조성마다 ×26 / ×34 / ×45 → f_e 가 상태 의존 → σ₀ 메타에 AM SOC 필수 · 기본 인계는 f_el 만 | `asano2017_…` A3962 Table II |
| ⑧ | **기준 상태 장부가 사전등록 칸으로 내려와야 한다** — Kato: σ₀ 만 냉간 펠릿 3.2 ↔ 소결 8.3 mS/cm 로 바꿔도 τ 2.47 ↔ 6.48 · ε · q · 두께 = 기공 0 기준 ((1−p)² 장부) · Asano: 한 논문 안 σ₀ ×1.14 · Wiedenmann: 기준 행 τ ≡ 1 을 표에 둔다 | `kato2018_…` p.610 · SI p.4/6 · `asano2017_…` · `wiedenmann2013_…` Table 1 |

## §1. 결정별 보강 (권고 불변 · 사전등록 항목 · 한정어)
| 결정 | 보강 | 근거 |
|---|---|---|
| 3 | hertz 면적 (LIGGGHTS c_cpl[22] 교차 원판) ≈ Molerus 소성 면적 1 차 ≈ 탄성 Hertz 의 2 × → 열 머리 한정어 ("hertz = 교차 원판 · 탄성 Hertz 아님") | molerus · kakar |
| 4 | 사전등록 ⓓ σ₀ 메타 = 출처 (냉간 펠릿 · 소결 · 액체 벌크 · 문헌 입력) · 성형압 · 측정 온도 · ⓑ ε 기준 (고체 / 상자) · 두께 장부 ((1−p)¹ 두께 실측 vs (1−p)² 치밀 기준) · 실험 τ 방법 불확도 (Kato 율속 20–25 %) 를 판정선 띠에 · 정규화 표에 기준 행 (순수 SE 망 = 1) 명시 | kato · asano · wiedenmann · thorat |
| 5 | τ_F = tau2 근거 셋 (COMSOL 5.6 Eq 6-6 · Thorat Eq 1/4 · Kato Eq 2) · 한정어 "τ_F 값은 σ₀ · ε · 두께 장부와 짝으로 넘긴다" · γ 붙은 상관식 (Thorat 1.8 ε^−0.53 등) 은 사용자 정의 "Tortuosity" 칸으로만 | thorat · kato |
| 9 | c² 두 끝 1.27 · 1.40 유지 · 한정어: Arzt/Kakar 값 = 원거리 재분배 (밀도 · Z 의존 · 1 차 c² ≈ 1 + Z(a/R)²/8 — 카드 유도) · Storåkers = 국소 pile-up (밀도 무관) · 둘은 우리 밀도 띠에서만 겹친다 · c² = 1 금지 · E3 한정어 "접착 하중 제외 · 점접촉 가정" · C1 은 법선 성분만 합 (접선력은 트레이스 항등식에 0, Molerus A9) · E2 의 R_c 는 hertz 대비 0.845–0.887 배 (두 끝 차 ≈ 5 % = 2 차 효과 · 카드 산술) · C0/C4: 밀도 → 면적 평균장 사상 금지, 접촉별 + 분포 보고 | kakar · molerus |
| 11 | Wiedenmann 의 무협착 기준 = 균일 관 (β = 1 · σ ≤ εσ₀) → 우리 CF (T < 1 이 26/157) 는 그 기준 상태가 아니다 = "모델 내부 기준선" 지지 · Cooper 복셀도 계면 항 0 (CF 쪽 · CL-81 과 정합) · 복셀 ÷ 접촉망 대조 사전등록 후보: 최소 특징 ≥ 5 voxel · DC 관문 (임피던스를 붙이면 ω → 0 이 각 솔버의 1/f 를 재현해야 한다) | wiedenmann · cooper |
| 13 | 실험 앵커 장부에: 레일 둘 여부 · R_e 고정 여부 · β (전자 ÷ 이온 저항) · 경계형 (개방 = conventional / 차단 = R/3 형) · 분리막 면 · 방향 (정/역) · 두께 시리즈로 계면 분리 여부 (Thorat).  진단 후보: z 단면 저항 r_k 로 반사 가중 F_z = Σr_k·3⟨(1−u)²⟩/Σr_k 를 정/역 둘 다 (Morasch 카드 유도) · 구현 함정: SE 노드에 부피 비례 축전을 주면 τ_e 가 아니라 확산 임피던스가 나온다 (Cooper) | malifarge · morasch · cooper · thorat |
| 14 | σ₀ 메타에 AM SOC 필수 · 기본 인계 f_el 만 · Malifarge β 로 Minnmann 본문값을 보면 β ≈ 20 → 0.002 (CAM 25 → 61 vol%) — "AM 등전위" 가정은 질량비 80:20 이상에서만 6 % 안 (카드 산술) | asano · malifarge |
| 15 | τ_geo 키에 분모 · 쌍 규약 메타 (같은 8 시료 평균 Wiedenmann 1.77 ↔ Holzer 카드 1.62) · 기호 충돌 (Molerus τ = 전단응력 · σ₀ = 정수압 · κ = 응집력 비 · f = 접촉 면적 · H = 응집력) → LHS-25 사전등록은 명시 태그 (F_c · A_c) | wiedenmann · molerus |

## §2. 메모 v2 정정 후보 (쪽 번호 · 메모는 아직 안 고침 — 정오표 단계에서)
| # | 메모 자리 | 지금 문장 | 원문 | 근거 |
|---|---|---|---|---|
| 1 | §8-2 Wiedenmann 행 · 부록 1 §2 | "τ_geo 지수 [미확인]" · "부분 해소" | 해소 — Eq 11 지수 1 · 맞춤 0 | p.1448 |
| 2 | §3-5 | "협착으로 읽을 수 없다" | "접촉 (Holm) 협착 배수로 읽을 수 없다" | Wiedenmann p.1448 · 1456 |
| 3 | 부록 1 §0 ④ · J | Holzer 경유 √τ_elc/τ_geo 0.76–1.46 | 원표 0.77–1.30 (8 점 중 2 점 < 1) | Wiedenmann p.1449 |
| 4 | §8-2 Kato 행 | "EIS 와 독립인 사이클 기반 τ" · "절대 대조 교차" | 율속 (방전 용량–전류) · 옴 한계 · 정의 교차만 (값 교차 불가 — 기공 미측정 · 재료 다름) | p.607 · 609–611 |
| 5 | §8-2 Asano 행 | "같은 실험 축의 두 번째 점 · §3-3" | 측정 축만 같다 (기공 · vol% 기준 · SE 입경 미보고 · SE = Li₃PS₄ 유리) → 닫는 항목 결정 4 · 14 | A3960–A3963 |
| 6 | §8-2 Malifarge 행 | "ASSB 에서 r_el ≪ r_ion 이 안 설 때" | 전자 저항이 큰 영역은 시험 안 함 · ASSB 언급 없음 · 해석식은 Tröltzsch–Kanoun | E3330–E3331 |
| 7 | §8-2 Cooper 행 | "망 임피던스 (τ_e) 구현 참고" | FD 틀 · open/closed · 정규화 · DC 관문 — τ_e 지배식 원전 아님 (원전 = Nguyen eSCM) | p.682–683 · 687 |
| 8 | §8-2 Thorat 행 | "eRDM 원조" | RDM 자체가 아니라 박리 전극막에 적용한 첫 직접 측정 | p.593 |
| 9 | §8-2 Morasch 행 | "구배 전극의 방향 의존 τ" | "차단 EIS 겉보기 τ 의 방향 의존 — 투과형은 방향 무관" | A3463 |
| 10 | §8-2 Molerus 행 · §6-3 | "f = 4πp/(ZD) — Arzt (20) 평균장의 원전" · "die 압밀은 국소압으로 바꾸라는 단서" | 인쇄 꼴은 σ = (F/d²)k(1−ε)/π (Eq 4 · A7) — 4πp/(ZD) 는 그것을 F 로 푼 Arzt 판 (R = 1) · 국소압 단서는 Molerus 에 없다 | p.263 · 273 (p.259–275 전수) |
| 11 | §6-3 "보정 셋" 의 접선력 | 보정 항목 | 사용 규칙 "법선 성분만 합 · \|F\| 금지" (접선력은 구의 트레이스 항등식에 0) | Molerus A9 p.273 |
| 12 | §8-2 Kakar/James 행 · 결정 9 | "압분 (Pb · Cu · Zn · Al) 접촉면적 실측 — E2 c²" | Kakar = 납 + 사파이어 (Cu · Zn · Al 은 James) · D ≲ 0.71 → "c² 밀도 의존 한정어" 로 · Fischmeister 1978 대체 못 됨 | p.3223 · 3227 |
| 13 | 결정 9 · §6-1/6-2/6-4 | "Arzt 1.27–1.40 또는 Storåkers ≈ 1.4" | 기구 (원거리 재분배 vs 국소 pile-up) · 밀도 띠 한정어 | Kakar Eq 1 p.3224 |
| 14 | 부록 1 결정 13 ⓒ | β 식 | 원문 식이 아니라 카드 유도 · 그래프법 기준 · β = 2 에서 부호 반전 — 셋을 표지로 | Malifarge 카드 §10 |
| 15 | §3-4 · 부록 1 ⑥ | Park σ₀ 출처 후보 | "[18a–c] 어디에도 없음" · Jung 2019 추가 (Park 2019 · 2020 CEJ 는 Table S2 각주의 [12] — 구분) | Jung 본문 + SI |
| 16 | §1 명명표 | — | Thorat (Tjaden Eq 8 원출처 · "factor" 낱말 0 회) · Kato ("tortuosity factor" = tau2) · Malifarge τ₂ · Cooper (Z̃(0) = τ/ε) · Morasch (Landesfeind Eq 13) · Wiedenmann (τ_elc = tau2 · τ_geo 를 'tortuosity factor' 로 부름 — **이름 반대**) | 각 카드 |
| 17 | §3-5 Bruggeman 배수 | — | LFP 막 ≈1.8× · Celgard ≈1.9× (Thorat) · 판상 흑연 2.3–3.7× (Malifarge) · Kato 1.86/2.51 · Morasch 구배 방향만으로 2.00–4.25× (카드 산술) · Wiedenmann 표값 1.80–3.11 | 각 카드 |
| 18 | 부록 1 "펠릿 ≡ 1" 목록 | — | Kato 추가 (냉간 420 MPa ↔ 복합체 500 MPa → 운전 50 MPa) | Kato SI p.4 |
| 19 | §7 | — | sink 는 접촉 면적 가중 (부피 아님) · "R_ion = 3·R_eff" 는 1D 환산이 −19/−23 % 과소 (Cooper Fig 6) · 크기 · 부호 규칙 (Morasch A3462–63) | Cooper p.685 · 687 · Morasch |

## §3. 다른 카드 (정본) 정정 후보
- 이번 정본 커밋에서 **고친 것 셋**: `comparison_vs_ours_DEM.md` 의 "Morasch R_int/R_i" 두 자리 → Morasch **2021** (JES 168 080519 · 정본 카드 없음) 표지 · `pouraghajan2018_…` 머리 주석 "정밀 인용 금지" → "정밀값으로 쓰지 않는다" (정본 웹앱 `_BAN_RE` 가짜 ban 표지 해소) · `minnmann2022_…` 꼬리 판정문 CL-94 정정 표지 (메인 결정 7).
- **고치지 않은 것** (새 카드 §10 에 근거 · 정본 다음 정리 때): holzer2013 Archie m 배정 반대 (원문 ol 2.31 · wo 2.95) · τ_geo 평균 1.62 ↔ 원문 1.77 · landesfeind2016 Eq 4 [미확인] 닫힘 · "β = τ̄_geo/T" 는 원문 명명으로 δ_elc · tjaden2018 41행 "AC + PI" (막은 PI 만) · nguyen2020 κ₀ 0.046 S/m Thorat 귀속 (Landesfeind 2016 값) · nguyen2020 ref 42 "부록 eSCM 대응" · arzt1982 "국소압" 귀속 · minnmann2021 [27] "49 vol% 최적" · cronau2022 [22] "입경 감소 성공" · kim2025 · interfacial_impedance 의 "Morasch" = Morasch 2021 · park2020 §4 · froboese §8(f) "[18b] 미대조" → 대조 완료 · mcgeary1961 단순입방 53.36 ↔ π/6 52.36 %.

## §4. 실행 순서 — 변경 없음
원장 등재 (✅ 10-03 `62f9e4cb3`) → 라벨 · 정오표 (TAU-01 · 배포 v1/v1.1 정오표 · 메모 v2 정정 = 부록 1 §2 + 이 부록 §2) → 봉인 밖 도우미 `scripts/tau_flux.py` + 시험 먼저 (웹앱 같은 묶음 J20-l) → WSL 명령 → 사전등록 (순수 SE 게이트 · LHS-25 — 위 §1 칸 반영) · 단계마다 Codex 요청서.

## §5. 카드 목록 (정본 `8e3d7a5d7`)
| slug | 서지 | 줄 |
|---|---|---|
| `jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb` | J. Mater. Chem. A 7, 22967–22976 (2019) + SI · DOI 10.1039/c9ta08517c | 462 |
| `wiedenmann2013_pore_structure_ion_conductivity_ceramic_diaphragms` | AIChE J. 59(5), 1446–1457 (2013) · 10.1002/aic.14094 | 401 |
| `kato2018_thick_electrode_assb_cycle_tortuosity` | J. Phys. Chem. Lett. 9(3), 607–613 (2018) + SI · 10.1021/acs.jpclett.7b02880 | 488 |
| `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` | J. Electrochem. Soc. 164(14), A3960–A3963 (2017) · 10.1149/2.1501714jes | 375 |
| `malifarge2017_tortuosity_symmetric_cell_impedance_tlm` | J. Electrochem. Soc. 164(11), E3329–E3334 (2017) · 10.1149/2.0331711jes | 469 |
| `cooper2017_simulated_impedance_diffusion_porous_media` | Electrochim. Acta 251, 681–689 (2017) · 10.1016/j.electacta.2017.07.152 | 417 |
| `thorat2009_quantifying_tortuosity_porous_liion` | J. Power Sources 188, 592–600 (2009) · 10.1016/j.jpowsour.2008.12.032 | 449 |
| `morasch2018_binder_gradient_impedance_tortuosity` | J. Electrochem. Soc. 165(14), A3459–A3467 (2018) · 10.1149/2.1021814jes | 402 |
| `molerus1975_theory_of_yield_cohesive_powders` | Powder Technol. 12, 259–275 (1975) · DOI [미확인] (PDF 에 없음) | 430 |
| `kakar1967_deformation_theory_hot_pressing` | J. Appl. Phys. 38(8), 3223–3230 (1967) · 10.1063/1.1710093 | 349 |
