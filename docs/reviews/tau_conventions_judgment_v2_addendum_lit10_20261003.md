# τ 판단 메모 v2 — 문헌 10 편 반영 부록 (2026-10-03 · 결정 16 비준 뒤 · 권고 변경 없음)

> 대상: `docs/reviews/tau_conventions_judgment_v2_20261003.md` (1저자 비준 10-03 · §0-2 권고대로).  비준 기록이 *"실행은 추가 문헌 10 편 (§8-1)
> 흡수 · 인사이트 보고 뒤"* 라고 적었으므로, 그 10 편을 정본 litdb 카드로 만든 뒤 결정마다 무엇이 바뀌는지 적는다.
> 카드 = 정본 브랜치 `claude/friendly-meitner-lldvar` 의 `litdb/papers/<slug>.md` (원문 PDF · SI 렌더 판독 · 인쇄 쪽 번호).  이 부록은 v2 본문을 고치지
> 않는다 — 비준된 표는 그대로 두고, 정정 후보는 §2 에 쪽 번호와 함께 따로 둔다.

## §0 결론

| # | 결론 |
|---|---|
| ① | **10 편 모두 결정 16 의 권고를 바꾸지 않는다.**  바뀌는 것은 사전등록 항목 · 한정어 문장 · 메모 v2 의 근거 문장이다 (§1 · §2). |
| ② | **tau2 한 이름 아래 기준 상태가 셋**이다 — 치밀 고유 σ = 1 (Park 2019 · 2020: 문헌 입력 σ₀) · 순수 펠릿 ≡ 1 (Minnmann · Kaiser · Hlushkou · Froboese — 펠릿 압밀 조건이 서로 다름) · 우리 (펠릿 σ₀ 3.0 위 SE–SE Holm).  ⇒ 결정 4 의 순수 SE 게이트가 절대 대조의 유일한 짝이라는 판단이 더 강해졌다. |
| ③ | **연속체는 모두 tau2 ≥ 1** 이다 (Ender τ_FEM 세 상 · Hlushkou 1.27 / 1.74 · Park 전부 · Holzer Eq 2).  우리 CF 가지의 T < 1 (26/157) 이 원기둥 bulk 산물이라는 결정 11 의 판단을 지지한다. |
| ④ | **"flux ≥ 기하" 순서는 √ 척도에서 반례가 있다** (Ender √τ_FEM/τ_geom 0.71–0.87 · Holzer √τ_elc/τ_geo 0.76–1.46).  ⇒ CF 결함의 근거는 Tjaden 순서가 아니라 **T_CF < 1 (Wiener)** 에 둔다. |
| ⑤ | **τ_e ↔ 관통 τ 실측 셋** (Kaiser ASSB · Pouraghajan 액체 · Landesfeind 2018) 어느 것도 "부호 불정" 을 깨지 않는다.  ASSB 1 사례 (Kaiser) 는 문턱 근처 (ε 0.3) 에서 TLM 이 관통보다 ≈ 7 배 높다 (판독). |
| ⑥ | **Park σ₀ 조성식의 출처는 여전히 [미확인]** — Froboese 2019 · Park 2019 · Park 2020 CEJ 셋 다 아니다 (원문 전수).  Park 역산 tau2 = "추세 전용" 유지. |

## §1 결정별 보강 (권고 변경 없음)

| 결정 | 보강 | 근거 (카드 · 인쇄 쪽) |
|---|---|---|
| 3 hertz 먼저 | 변경 없음.  ① 계면 저항 트랙의 면적 원천도 같은 순서로 맞춘다 (초안 D3 "physics 병기" → "LHS-25 뒤") | Codex 요청서 `codex_rint_stage1_request_20261003.md` §4 |
| 4 순수 SE 게이트 | 사전등록에 넷을 더한다: ⓐ 판정선을 **f 와 tau2 둘 다**로 · ⓑ 앵커별 **ε 장부** (고체 기준 · 기공 포함 · 수지 포함 여부) · ⓒ 정규화 목표가 **1 인지 φ_pure 인지** (Froboese 순수 펠릿 τ = φ_pure 0.956 · 우리 순수 침대 φ ≈ 0.88 이면 T ≈ 12 % 차) · ⓓ σ₀ 메타에 **기준 시료의 압밀 · 측정 상태** 열 (Kaiser · Hlushkou 펠릿 276 MPa · 30 min ↔ 복합체 392 MPa · 5 min).  Hlushkou 는 판정선 밖 (LPSI 유리 · 1 점 · 우리 과압축 띠 φ_SE 0.54–0.62 · 입경 미보고) | `hlushkou2018_…` p.365–369 · `froboese2019_…` A321 · A323 · `kaiser2018_…` p.178–180 · SI p.1–4 |
| 5 COMSOL 표기 | 변경 없음.  한정어 둘: tau2 에 "EIS" 를 붙일 때 **연결형** 병기 (T형 open–open = 관통 tau2 부류 · Z/E형 = τ_e 부류) · σ_eff 를 넘길 때는 **σ₀ 짝 + COMSOL 보정 설정 (No correction)** 명기 (Park 그룹은 τ 칸을 우회하고 σ_eff 를 P2D 식에 직접 넣었다) | `siroma2015_…` 표 2–3 p.317–318 · `park2019_…` SI p.3–5 · `park2020_dimension_…` SI p.3–5 |
| 9 LHS-25 | 변경 없음.  면적 열에 **분모 메타** (AM 부피당 / 전극 부피당) — 한 논문 안에서도 흔들린다 | `park2020_dimension_…` p.3 · SI p.8–10 |
| 11 CF 지위 | 변경 없음 (이름 그대로).  사전등록에 셋을 더한다: ⓐ 복셀 **격자 수렴 조건** · ⓑ 공변량 **a/dx · δ/d** (복셀 CF 는 해상한 목 기하를 품어 망 CF 와 같은 "협착 0" 이 아니다) · ⓒ CL-81 의 "복셀 σ 는 CF 가지 위" 는 **비기하 계면 항이 0** 이라는 뜻으로만 쓴다 (Holzer 틀에서 복셀은 해상한 목의 협착 δ 를 품는다).  영문 이름에 constrictivity · constriction factor 를 쓰지 않는다 (FULL/CF 는 δ 도 β 도 아니다) | `holzer2013_…` p.2936–2937 · p.2949 · `park2019_…` (vox 0.1 µm · 격자 시험 없음) · `park2020_dimension_…` |
| 13 τ_e | 변경 없음 ("부호 불정" 유지).  한정어 · 진단 추가: ⓐ "문턱 근처에서 갈림 · TLM > DC · ASSB 실측 1 사례" (Kaiser) ⓑ "R_ion = 3·R_eff" 는 **균일 r · c · z_C = 0** 일 때만 정확 (비균질 2 층 3:1 예 ±37.5 %) ⓒ 실험 앵커엔 고상 저항 **β 보정** (무시하면 R_ion 을 [(1+β) − 3β/(1+β)] 배) · 집전체 접촉 반원 (가리면 +25 %) ⓓ 진단 넷째 = 전자 레일 R_el/3 | `kaiser2018_…` p.178–180 · `siroma2015_…` 표 3 · `pouraghajan2018_…` A2647–A2651 |
| 14 전자 · 열 | 변경 없음.  선례: 단일 입력 σ₀ 로 전자 N_m 이 정확히 재현된다 (Park 2019 — N_m × σ_eff = 2.50 = σ₀) | `park2019_…` p.127 · SI p.3 |
| 15 키 이름 | 변경 없음.  지지: 같은 그룹이 2018 "effective tortuosity" → 2021 "τ²" 로 이름을 바꿨다 (식으로 판정) · Bruggeman α 관례 표지 필요 (σ 지수 3.67 = T 지수 2.67 = √T 지수 1.335) | `kaiser2018_…` Eq 2 · `froboese2019_…` A325 |

## §2 메모 v2 정정 후보 (본문 미적용 · 쪽 번호 포함)

| v2 자리 | 지금 문장 (요지) | 정정 후보 | 근거 |
|---|---|---|---|
| §8-1 #3 · 결론 ④ · §3-8 ① | Froboese = "ASSB 전극 · 입경비 가설의 실험 쪽 검정" · "입경비 … 지배" | 고분자 (PEO:LiTFSI) + 비활성 유리구 **모델계** · SE 입경 미보고 · 입경 효과는 공정 기공률과 교란 → "입경비" 는 **방향이 맞는 후보 중 하나**, "공정 기공" 후보 추가 | `froboese2019_…` A318–A319 · A322–A324 |
| §8-1 #3 · §3-4 | Park σ₀ 식 출처 후보 = Froboese | 이 논문에 없음 (σ₀ 6.19·10⁻⁴ A321 · Eq 18 A325) → 후보 제외 | 같은 카드 |
| §8-1 #4 | Landesfeind 2018 = "정의 · 방법 차이의 실측 크기" · "같은 전극" | **방법 (해상도 · CBD) 차** — 정의 차 분리 안 됨 · "같은 코팅에서 자른 전극" · OA = CC BY-NC-ND 4.0 | `landesfeind2018_…` A469 · A474–A475 |
| §8-1 #5 | Park 2019 · [12b] 에서 "τ 산출법 · σ₀ 규약 (역산 대신 원값)" | 둘 다 미충족 (Park 2019 = 흑연/LSTP 음극 · N_m 만 · Park 2020 CEJ = LLZO-Ta · τ 값 0) → 항목을 [12a] 계산 문장으로 · park2020 Table S2 각주 b 의 [12a] σ₀ 인용은 [12a] 에 그 값이 없다 | `park2019_…` p.126–127 · SI p.3 · `park2020_dimension_…` SI p.3 |
| §8-1 #6 | Hlushkou = "두 번째 절대 앵커" · "13–17 % 기공 비교" | "조건부 참고점 / 방법 벤치마크" · 13.2 vol% 는 **수지 + 잔류 공극** (FIB 시료) | `hlushkou2018_…` p.366–367 Table 3 · Fig 4C |
| §8-1 #8 | Kaiser = "§3 절대 대조 (게이트 뒤)" | 불가 (입경 미보고 · 기공 미측정 · ε 기공 0 가정 · LTO + 유리 SE) → "결정 13 · 결정 4 정의 사례" | `kaiser2018_…` p.178 · SI p.2–4 |
| §8-1 #9 | Ender = "복셀 Laplace N_M (STEP3 계열)" | 보고값은 **τ_FEM (Eq 2 = tau2)** · ParCell3D FEM (Tjaden 2b) · STEP3 와 공유하는 건 "연속체 · 계면항 0" 범주뿐 | `ender2011_…` p.167–168 |
| §3-5 | "Constriction overhead … 협착으로 읽을 수 없다 — 연속 기공상도 1.24–1.59" · √T_CF/τ_Dij "반대 방향" | 결론 유지, 근거를 "**접촉 (Holm) 협착 배수**로 읽을 수 없다" 로 (Holzer 틀에선 그 격차가 협착 δ) · "반대 방향" 은 √ 척도에서만 → CF 결함 근거 = T_CF < 1 (Wiener) | `holzer2013_…` p.2936–2937 · p.2949 · `ender2011_…` Table 1 |
| §3-5 Bruggeman 행 | 액체 전극 ≈ 1.5–3× | 보강: Landesfeind 2018 1.96–3.56× · Holzer 격막 1.8–3.1× | `landesfeind2018_…` A472–A475 · `holzer2013_…` Fig 15 |
| §3-8 ③ springback | "실험 T 를 올린다" | 두께를 **하중 아래**에서 잴 때만 · 해제 뒤 두께 (Kaiser) 면 반대 성분 | `kaiser2018_…` p.178 |
| §1 τ_e 행 · §7 마지막 행 | Minnmann "관통형에 가깝다 [판독]" | [판독] 해제 — Minnmann 식 [1] = Siroma 표 3 T형 open–open 행 (관통) | `siroma2015_…` p.316 · p.318 |
| §8-1 #7 | Minnmann R_ion 이 입계 · 접촉을 포함하는지 확인 | TLM 원문은 구조적 답만 (레일 = 균질 저항 하나 · 접촉저항은 끝면 요소로만) · 내용물은 Minnmann SI S2 가 정한다 | `siroma2015_…` p.313–315 · p.319 |
| §7 최소안 | "R_ion = 3·R_eff" | 성립 조건 한정어 (균일 · z_C = 0 · β) | `siroma2015_…` · `pouraghajan2018_…` |
| §8-2 Wiedenmann | "τ_geo 지수 [미확인]" | 부분 해소: Holzer 분해식의 τ_geo 는 1 승 (Eq 11 · Fig 16) · M-factor (ε·β/τ²) 꼴 · 지수는 이 논문에 없다 | `holzer2013_…` p.2950 |

## §3 실행에 주는 영향

- 실행 순서 (원장 등재 → 라벨 · 정오표 → 봉인 밖 도우미 `tau_flux.py` + 시험 → WSL 명령 → 사전등록 (순수 SE 게이트 · LHS-25)) 는 **바뀌지 않는다**.
- 사전등록 문서에 §1 의 결정 4 ⓐ–ⓓ · 결정 11 ⓐ–ⓒ · 결정 13 ⓐ–ⓓ 를 항목으로 넣는다.
- 원문 오식 (각 카드 §10): Holzer Eq 8 역수 · Eq 9 부호 · Froboese 인쇄 τ 791 (재계산 ≈ 80 — 인용 금지) · Pouraghajan z_c/z_cc 뒤바뀜 · 유한 Z₀ 가지 (재유도 전 사용 금지) · Park 2019 σ_eff 본문 ↔ 그림 · Park 2020 CEJ Table S3 ↔ 그림 · Hlushkou 1.34 ↔ 1.365 · Siroma 그림 12 z_B 표지 · (A.4) 부호 · Landesfeind 2018 R_Ion 전극 수 규약.

## §4 카드 (정본 · 10-03 · 커밋 `e7f425b80`)

`holzer2013_constrictivity_effective_transport_porous_layers` · `froboese2019_microstructure_ionic_conductivity_assb_electrode` ·
`landesfeind2018_tortuosity_impedance_vs_tomography` · `park2019_electrode_design_methodology_assb_3d` ·
`park2020_dimension_controlled_se_percolation_contact_area` · `hlushkou2018_void_space_ion_transport_assb_cathode` ·
`siroma2015_transmission_line_model_porous_electrode_impedance` · `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` ·
`ender2011_3d_reconstruction_composite_cathode` · `pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte`
(그림 · 표 크롭 포함 · 손작업 크롭 19 장은 `figures.json` 의 `manual_crop` 사유).  J 절 = 정본 `litdb/comparison_vs_ours_DEM.md` §J.
