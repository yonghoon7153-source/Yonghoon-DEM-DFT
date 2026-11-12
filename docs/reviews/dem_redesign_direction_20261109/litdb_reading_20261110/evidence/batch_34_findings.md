# 배치 34 — 질문 a–n 근거

카드 7 장 (정본 사본 sha c8faad2d7) 전문 읽음: luan2025 · matsusaka2010 · minnmann2022 · nadeem2023 · nase2001 · neumann2021 · nirmalraj2009.
위치 표기: L = 카드 줄 번호 (사본 파일 기준) · § = 카드 절 · p = 논문 쪽 · Fig / Table = 원문 번호. 표지는 카드에 적힌 그대로 옮겼다.
형식: `- [글자] slug | 내용 (값 · 단위) | 위치 | 표지 | 한계`.

## a — 순수 SE 압력별 기공 곡선

- [a] minnmann2022_designing_cathodes_solidstate | 곡선 없음 (설계 Perspective · 기공 수치 0 개). 카드가 출처 정정 맥락에서 남의 값 둘을 적음: ① Sakuda 2013 의 75Li₂S-25P₂S₅ 유리 cold-press 밀도 87 % @ 300 MPa (= 기공 13 %) · σ 회복 91 % ② "순수 SE ~10 % @ 300 MPa" = 우리 MPM/DEM 보정 수렴값 → 10-03 정정에서 출처 [미확인] · 외부 앵커 없음 | §0 L49–55 · §6 L294–295 · L434 | 표지 없음 (출처 정정표) · L434 = 10-03 정정 표지 | 2 차 인용 · 곡선 · 진밀도 · 질량 기준 여부 · 누른 채인지 뺀 뒤인지 모두 카드에 없음 · ①은 유리 (LPSCl 아님 · 정본 카드 sakuda2013_sulfide_mechanical_property 있음) · ②는 실험값 아님 (카드 문제 2 · 3)

## b — 탈압 때 되돌아오는 양과 잰 방법

- [b] nase2001_granular_bond_collision_number_wet_cohesion | 측정 없음. 접촉 단위 제하 법칙만: 항복 전 제하 = 탄성 · 항복 뒤 제하 F_n = F_max − k_n√R̄ (α_max − α)^{3/2}, R̄ = R′/R* = (F_y/F_max)((2F_max + F_y)/(3F_y))^{3/2} (새 접촉 반경 R′ = 잔류 압흔) | §3-1 L59 · 식 6–7 · p.215 | [인쇄] | mm 유리 충돌 · 흐름 모사 (압밀 · 탈압 아님) · 이 법칙으로 되돌아옴을 잰 검증 없음
- [b] luan2025_graded_cathode_400whkg_pouch | 되돌아옴 측정 없음. 제조압 (양극 단축 300 MPa · 파우치 등방 500 MPa) 과 사이클 스택압 30 MPa 를 나눠 적음 | §3-1 L73–77 · §7-A L426 | stated | 탈압 뒤 두께 · 기공 없음
- [b] minnmann2022_designing_cathodes_solidstate | 되돌아옴 측정 없음. 제조 (cold-press) 압 ↔ 작동 스택압 "수~수십 MPa" 구분만 | §0 표 L92 · §2.2 L159–161 · §10-4 L372–373 | 표지 없음 · 직접 인용 | 범위 권고뿐

## c — 항복 · 경도 · 크리프 값과 정의

- [c] nase2001_granular_bond_collision_number_wet_cohesion | 접촉 단위 항복 힘 F_y (Thornton 탄–완전소성) — "본질적으로 맞춤 매개변수" · 항복 뒤 선형 F_n = F_y + k_y(α − α_y), k_y = (2/3)(F_y/α_y) · F_y 값 [미확인] · 경도 · 크리프 · 일축 항복 세기와의 환산은 카드에 없음 | §3-1 L58 · 식 5 · p.215 · §10-9 L192 | [인쇄] · [미확인] | 접촉 힘이지 재료 응력 아님 · k_y 계수 확인 필요 (카드 문제) · 환산은 배치 밖 thorntonning1998 카드 L250–251 에 p_y ≈ 1.6σ_y · H ≈ 3σ_y 서술이 있음
- 나머지 6 장: 이 배치에 없음.

## d — 단단한 · 무른 입자 혼합의 하중 몫 · 재밍

- 이 배치에 없음. (minnmann2022 는 "hard CAM + soft SE 또는 그 반대" 설계 원칙만 · 하중 몫 수치 없음 — §1 L116 · §6 L235.)

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안

- [e] nase2001_granular_bond_collision_number_wet_cohesion | 대안 = Thornton 탄–완전소성 법선 접촉 (항복 전 Hertz F_n = k_nα^{3/2} · 항복 뒤 선형 · 제하 = 새 반경 R′) + Walton–Braun 접선 (γ = 1/3 · k_t0 = k_n(1 − ν)/(1 − ν/2)) + 펜듈러 액체 다리. 맞춘 값 = F_y 1 개 (값 [미확인]) · 나머지는 재료값 (E 7.0 × 10¹⁰ Pa · ν 0.25 · ρ 2500 kg/m³). 점접촉이 깨지는 범위 · 다접촉 보정은 말 없음 | §3-1 L57–60 · §3-4 L79 · p.215–216 · p.218 | [인쇄] · [미확인] | mm 유리 흐름 (조밀 압밀 아님)
- 나머지 6 장: 이 배치에 없음.

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙

- [f] neumann2021_garnet_3d_structure_grain_boundaries_li_transport | MPM 아님 — 복셀 연속체 참고값: 분할 0.1 µm → 계산 voxel 0.5 µm · 입자 지름 3.1–4.6 µm = 6–9 voxel · 축소 뒤 입자 번호 규칙 · 격자 수렴 · 실현 수 미기재. 저자: "due to the spatial resolution … the lithium distribution algorithm most likely overestimates the residual lithium content needed for a percolating network" | §0-1 L15–17 · §4-1 L139–140 · §4-5 L163 · §3-6 L134 (p.4798) | stated · n/a | 소결 garnet · 역학 없음 · 수치 오차 추정 없음
- 나머지 6 장: 이 배치에 없음.

## g — 2D ↔ 3D 옮김 경고

- [g] nadeem2023_gnn_mixing_index | 3D CT 를 찍고 이웃은 2D 단면에서만: "since calculations were performed on 2D cross-sectional slices extracted from the 3D volumetric CT reconstructions, neighbor particles were only defined in the 2D plane". 카드: 3D 배위수 (6+, Pinson 이성분 구) 를 2D 이웃에 적용 = 차원 어긋남 · 단면 겉보기 반지름 보정을 GNN 에는 안 함 (MGMMI 에만 면적 가중) | §4.6 L261–267 · §10-② L603–604 | 원문 인용 · 카드 해석 | 방향이 반대 (3D 값을 2D 에) · 혼합지표 (압밀 아님)
- [g] nase2001_granular_bond_collision_number_wet_cohesion | 드럼 충돌 수 Co 의 δ/R_t ≈ 0.03 = Gilchrist 2D 드럼 실험값 차용 — "3D · 배플 · 다른 채움에서는 다를 수 있다 (… 4 제곱이라 민감)" | 한정어 ④ L36 · §3-6 L99 · §10-7 L190 | [우리 산술] · [추정] | 믹서 흐름 (압밀 아님)

## h — DEM 에서 FE · MPM 으로 넘긴 선례

- 이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공

- [i] luan2025_graded_cathode_400whkg_pouch | NCM88 + LPSC + Super P 양극 단축 300 MPa (코인) · 파우치 등방 500 MPa — 기공 · 밀도 · 두께 미보고 ("논문이 어디에도 안 준다") · 두께 그림 SI Fig S6b 는 미보유 | §3-1 L73 · L76 · L81 · §7-A L427–428 · SI 절 L654 | stated | 대조 값 없음
- [i] minnmann2022_designing_cathodes_solidstate | 카드가 남의 값 언급: Minnmann 2021 JES — NCM622 + LPSCl · 건식 단축 cold-press 380 MPa · 평균 14 % (범위는 본문 13–17 % ↔ 10-03 정정 7.6–17 % — 카드 문제 4) · EIS-TLM | §0 L44–48 · §6 L291–293 · L434 | 표지 없음 (출처 정정표) | 2 차 인용 (정본 카드 minnmann2021_jes_charge_transport_bottlenecks 있음) · 380 ≠ 300 MPa

## j — 카드가 적은 한계 중 가압 · 탈압 계산과 닿는 것

- [j] luan2025_graded_cathode_400whkg_pouch | COMSOL 은 "압밀/porosity 시뮬 없음 — 300 MPa 성형은 실험에서만 하고 모델은 압밀 후 구조를 가정" · 입자 · 접촉 · 공극 없는 2-region 연속체 · 등방압 ↔ 단축: "같은 MPa 라도 같은 압밀이 아니다" (porosity · 이방 tortuosity · 접촉면적 전이 금지) | §4-3 L347 · §7-A L425 · §10-1 L588–590 · §10-12 L610–612 · §11 L637–638 | stated (카드 판정) | —
- [j] minnmann2022_designing_cathodes_solidstate | 작동 스택압: "Clearly, such high pressures are not suitable for large-scale commercial applications" (수십 MPa) · §5.4 = 미세구조 mechanical 모델을 electrochemical · thermal 모델과 결합해 압력 · 온도 효과를 봐야 한다 (카드 한국어 옮김 · 원문 영어 없음) | §2.2 L159–161 · §5.4 L228–232 | 직접 인용 · 표지 없음 | 권고 문장 · 수치 없음
- [j] nadeem2023_gnn_mixing_index | 논문은 압밀 중 배위수 변화를 고려하지 않음 (믹싱) → 카드: 압밀이 부분 배위수 Z_ij 를 바꾸면 접촉 통계 E_XY 가 혼합과 무관하게 움직인다 (우리 쪽 새 결함 후보 · German 2014 제목 인용) | §7-D L494 · §8-③ L538–546 | 카드 해석 | 혼합지표 (압밀 계산 아님)

## k — DEM 의 한계 (인용 서지와 함께)

- [k] nase2001_granular_bond_collision_number_wet_cohesion (Nase · Vargas · Abatan · McCarthy, 2001, Powder Technology 116, 214–223) | 항복 힘 F_y 를 "본질적으로 맞춤 매개변수" 라 적음 (카드 한국어 옮김 · 원문 영어 문장은 카드에 없음) = 보정값이 물성이 아니라는 고백 · 그 값 · 계산 입자 크기 · 개수 · 시간 간격 [미확인]. 연화 E 부작용 수치: "soft" (acrylic 성질 · E 두 자릿수 작음) 계산 더미 Bo_g 10 → 62° vs acrylic Bo_g 18 → 38° — 점착 (모세관) 이 E 와 무관한데도 · 논문이 DEM 한계로 말한 것은 아님 (카드 해석 [추정]) | §3-1 L58 (p.215) · §4-1 L108–110 · §8-4 L171 · Fig 5 · §10-9 L192 | [인쇄] · [판독] · [추정] · [미확인] | mm 유리 · 흐름 (압밀 아님)
- [k] matsusaka2010_triboelectric_charging_powders_review (Matsusaka · Maruyama · Matsuyama · Ghadiri, 2010, Chemical Engineering Science 65, 5781–5807) | 역학 DEM 한계는 말 없음. 대전 모형 쪽: 축전기 모형 k_c · z₀ 는 맞춤 상수 (z₀ = "the critical gap including the geometrical factors" · 독립 측정 불가) · 균일 대전 구 가정은 절연 입자에서 깨짐 (전하가 접촉 자리에 국소화) → DEM 이 표면을 대전 자리 32 · 200 · 392 개로 나눔 (Yoshida 2003 인용) | §3-1 L74 (p.5788) · §4-1 L169–170 · §3-8 L162 (p.5802–5803) · §10-2 L329 | [인쇄] | 역학이 아닌 대전
- [k] luan2025_graded_cathode_400whkg_pouch (Luan et al., 2026, Adv. Funct. Mater. 36, e26239) | 말 없음 — DEM 없음 ("DEM/discrete element/particle" 단어 0 회) | §4-3 L343 | 카드 판정 | —
- [k] minnmann2022_designing_cathodes_solidstate (Minnmann et al., 2022, Adv. Energy Mater. 12, 2201425) | 말 없음 — 시뮬레이션 없음 · "구형 CAM 패킹 유리" + "비구형 형상을 다시 생각" 권고만 (카드 해석: 형상 = 미해결 설계축) | §4 L259–267 · §5.4 L228–230 | 표지 없음 | DEM 한계 문장 아님
- [k] nadeem2023_gnn_mixing_index (Nadeem · Subramaniam · Nere · Heindel, 2023, Advanced Powder Technology 34, 103933) | 말 없음 — DEM 없음 · "can also easily be adapted to 3D data, such as those generated by DEM" = 전망 문장 | §10-⑬ L631–632 | 원문 인용 | —
- [k] neumann2021_garnet_3d_structure_grain_boundaries_li_transport (Neumann et al., 2021, ACS Appl. Energy Mater. 4, 4786–4804) | 말 없음 — DEM 없음 (FIB-SEM 실구조 · watershed voxel 입자) | §4-6 L166 | 카드 판정 | —
- [k] nirmalraj2009_swcnt_network_junction_resistance (Nirmalraj · Lyons · De · Coleman · Boland, 2009, Nano Letters 9, 3890–3895) | 말 없음 — 계산 없음 | §2 L38 | — | —

## l — 소성변형이 왜 어려운가 · 택한 우회 (인용 서지와 함께)

- [l] nase2001_granular_bond_collision_number_wet_cohesion (Nase et al., 2001, Powder Technology 116, 214–223) | 어려운 이유 설명 없음. 우회 = 접촉 힘 법칙의 소성 (Thornton 탄–완전소성 · 항복 뒤 선형 · 제하 = 새 접촉 반경) — 카드: "접촉 힘 법칙 의 소성이지 입자 형상 소성이 아니다" · 맞춘 값 = F_y 1 개 (값 · 무엇에 맞췄는지 [미확인]) · 검증 = 정지 더미 · 드럼 그림에 계산점 (acrylic · soft) 을 실험점과 함께 Bo_g · Co 축에서 대조 (Fig 5 · 9) · 압밀 · 하중 이력 검증 없음 · 계산 비용 (입자 수 · 시간) [미확인] | §3-1 L57–59 · §4-1 L108–110 · §10-9 L192 | [인쇄] · [미확인] | 흐름 (압밀 아님)
- [l] luan2025_graded_cathode_400whkg_pouch (Luan et al., 2026, Adv. Funct. Mater. 36, e26239) | 말 없음. 우회 = 입자 · 접촉 · 공극 없는 2-region 균질 연속체 + 미공개 퍼콜레이션 상관식 (σ_e 입력 2 점) · 격자 · 수렴 · 초기 / 경계조건 미제시 (재현 불가) | §4-2 L326–334 · §4-3 L344–348 | stated (카드) | 압밀 · 형상 없음
- [l] minnmann2022_designing_cathodes_solidstate (Minnmann et al., 2022, Adv. Energy Mater. 12, 2201425) | 말 없음 (시뮬레이션 없음). 대신 결합 mechanical–electrochemical–thermal 미세구조 모델을 요구 (§5.4 · 카드 한국어 옮김) | §5.4 L228–232 | 표지 없음 | 권고뿐
- [l] matsusaka2010 · nadeem2023 · neumann2021 · nirmalraj2009 | 말 없음 (역학 · 소성 계산 없음 · neumann2021 은 소결체 실측 형상) | — | — | —

## m — 받아들일 통찰 (무엇 | 어디에 | 왜 · 근거 위치 | 표지 · 한계)

- [m] luan2025_graded_cathode_400whkg_pouch | 문헌 기공과 견줄 때 가압 방식 (단축 · 등방 · 롤) 을 칸으로 두고 섞지 않는다 — "같은 MPa 라도 같은 압밀이 아니다" (파우치 등방 500 MPa ↔ 코인 단축 300 MPa) | 결과 전 대조 항목 (단계 4 · 5) | §7-A L425 · §10-12 L610–612 · §11 L637–638 | stated · 이 논문 자체는 기공 없음
- [m] luan2025_graded_cathode_400whkg_pouch | 제조압 (300–500 MPa) 과 사이클 스택압 (30 MPa) 을 나눔 → 탈압 끝 상태를 0 MPa 하나로만 두지 않고 작동압 점도 보고 | 단계 6 | §3-1 L77 · §7-A L426 (작동압 밴드 Doux 5 · Minnmann 40 · Luan 30) | stated · 작동압 값 하나
- [m] luan2025_graded_cathode_400whkg_pouch | 탄소 0.5 wt% 고정 · SE 10→60 wt% 에서 σ_e 약 6 자릿수 붕괴와 용량 붕괴가 같은 자리 → 문턱항 없는 φ_AM⁴ 꼴 σ_e 폼을 φ_AM(고체) < 0.3 으로 외삽하지 않는다 | 흐름 밖: σ_e 폼 유효범위 (메인 CLAUDE.md σ_e 절에 이미 반영) | §3-5 L197–207 · §7-B L442 · §8 P-7 L555–559 | figure-read ≈ · 붕괴 φ = DERIVED(ours) (ρ 가정) · σ_e 절대값 인용 금지
- [m] luan2025_graded_cathode_400whkg_pouch | 층상 · graded 대조군은 CAM · SE · 탄소 총량을 고정하고 위치만 바꾼다 · 롤프레스 뒤 층 사이에 뚜렷한 계면이 없음 → 층상 합성은 계단이 아니라 완만한 구배 | 흐름 밖: 층상 양극 (Phase-5 · graded-z) | §3-2 L87–95 · §5 Fig 6d,e L385 · §8 P-6 L550–553 | stated · SEM 정성
- [m] matsusaka2010_triboelectric_charging_powders_review | 코팅은 점착 일 (ΔW) 만이 아니라 접촉 전위차 (CPD) 도 지운다 (알루미나 · 실리카 코팅이 티타니아 대전 부호를 옮김) → 코팅 대리 팔 (LC) 결과를 실물과 견줄 때 둘이 섞임 · 대전 · 제전 대조가 필요 | 흐름 밖: 믹서 확인 블록 · 논지 P1 | §3-2 L97 · Fig 13 · §7-1 L271–272 · §8-3 L318 | [판독] · [추정] · 배터리 소재 자료 없음
- [m] matsusaka2010_triboelectric_charging_powders_review | 정전기 (영상력) ÷ JKR 점착 비 ∝ 지름 → 조립자화 (CG 배율 f) 에서 f 배 부풀려짐 · 덱에 정전기를 넣으면 Bo 와 다른 CG 규칙이 필요 | 흐름 밖: 믹서 DEM 조립자화 | §7-2 L276–285 | [우리 산술] · 교과서 쿨롱식 · σ 는 리뷰 자료 띠
- [m] matsusaka2010_triboelectric_charging_powders_review | 대전 측정 형식 = blow-off (미분 SE + 운반체 NCM 꼴) · Kelvin–Zisman CPD (불활성 분위기로 옮길 수 있음 · 표면층이 값을 바꾸므로 시료 이력 기록) · 리뷰 자료의 최저 RH 0.1 아래는 없음 (드라이룸 · 글로브박스 = 범위 밖) | 흐름 밖: 믹서 D3 실측 설계 | §3-3 L115 · §3-7 L152–154 · §7-4 L294–296 | [인쇄] · [추정] · 황화물 측정 선례 없음
- [m] minnmann2022_designing_cathodes_solidstate | 기공 앵커는 연도 · 논문까지 적는다 — 이 2022 Perspective 는 기공 · σ 수치 0 개 · 복합 기공 = Minnmann 2021 JES (380 MPa · NCM622) · 87 % @ 300 MPa = Sakuda 2013 (유리) · 순수 SE 10 % @ 300 MPa = 외부 출처 없음 (10-03 정정) | 결과 전 대조 항목 · 단계 4 · 5 | §0 L37–68 · §6 L287–296 · L434 | 카드 판정 + 10-03 정정 · 카드 안 범위 불일치 (카드 문제 4)
- [m] minnmann2022_designing_cathodes_solidstate | 같은 해 Minnmann JES 가 둘 — 040537 (abf8d7 · Charge Transport Bottlenecks = 기공 · τ 앵커) ↔ 040502 (abf3a3 · charge rate and inactive components) · 카드 작성 때 우리 refs.bib 의 @Minnmann2021 이 040502 를 가리킴 | 흐름 밖: 원고 참고문헌 | §0 L70–80 · §10-2 L367–369 | 카드 판정 (파일 미수정) · refs.bib 현재 상태는 이 배치에서 미확인
- [m] minnmann2022_designing_cathodes_solidstate | 300 MPa 는 제조 (cold-press) 압 · 작동압은 수~수십 MPa — 탈압 계산의 끝 압력을 정할 때 혼동 금지 | 단계 6 | §2.2 L159–161 · §10-4 L372–373 | 직접 인용 · 범위뿐
- [m] nadeem2023_gnn_mixing_index | 지표 눈금은 "정답을 아는 배치" 로 실측 정의 — null-mixed (같은 insert/pack 시드 절차 앙상블) · null-segregated (상별 층 분리) · 논문의 0 / 1 을 우리 계로 옮기지 않음 | 흐름 밖: 믹서 응집 지표 (E_XY) | §8-④ L549–558 · §10-⑧ L619–622 | 카드 설계 · 12:4:1 다분산의 '무작위' 는 자명하지 않음 (L557–558)
- [m] nadeem2023_gnn_mixing_index | 가중 규약 (입자당 ↔ 접촉당) 을 결과 전에 선언 — real_14 에서 AM_P 는 입자의 0.108 % 인데 접촉의 11.6 % (107 배) | 흐름 밖: 믹서 사전등록 (단계 0 과 같은 꼴) | §8-② L530–536 · §12 L715 | [우리 실측] · 논문 값 아님
- [m] nadeem2023_gnn_mixing_index | 압축 뒤 상별 접촉 통계에는 기공률과 상별 평균 접촉수 Z_i 를 공변량으로 같이 적는다 (압밀이 Z 를 바꾸면 혼합과 무관하게 지표가 움직임) | 단계 7 · 흐름 밖: 믹서 | §8-③ L538–546 | 카드 제안 · 판정선은 안 건드림 (공변량)
- [m] nadeem2023_gnn_mixing_index | 쓰면 안 되는 지표 — 고정 k 중심거리 이웃 (12:1 크기비에서 큰 입자를 못 봄: real_14 M_GNN 0.0239, 무편향이면 1.0) · 중심 (centroid) 기반 MGMMI (육안 분리에 ≈ 0.87 · GNN ≈ 0.44) | 흐름 밖: 믹서 지표 선택 | §7-B L389–422 · §8-⑤ L560–566 · Fig 7 | [우리 실측] · Fig 7 = digitized TREND only
- [m] nase2001_granular_bond_collision_number_wet_cohesion | 후보 C′ 의 항복 힘 (항복압) 은 물성이 아니라 맞춤 값 하나로 센다 (원문 "본질적으로 맞춤 매개변수") | 후보 C′ · 조건 R5 | §3-1 L58 (식 5 · p.215) · §4-1 L108 | [인쇄] · k_y 계수 확인 필요 (카드 문제)
- [m] nase2001_granular_bond_collision_number_wet_cohesion | 드럼 혼합 결과엔 Bond 수와 함께 충돌 수 Co (점착 ÷ Bagnold 충돌력) 를 적는다 — 드럼 동적 각은 Bo_g 로 전이가 안 보이고 Co 로 보면 전이 · Co 는 덤프의 흐름층 속도 · 두께로 식 29 계산 (λ² 하나 남음) | 흐름 밖: 믹서 확인 블록 보고 | §3-5 L89–91 · Fig 9 · 11 · §8-1 L168 | [판독] · [인쇄] · λ² 미기재 → 전이 위치는 λ² 선택에 달림 (원문 "subject to choice of the constant, λ²" p.222)
- [m] nase2001_granular_bond_collision_number_wet_cohesion | 점착 계는 회전 ↑ → 동적 각 ↓ (마른 계와 반대: 2 mm 젖음 1.1 → 3.8 rpm 에 28.3 → 26.6°) → 회전 속도 (Fr) 감도를 점착 · 비점착 팔로 묶지 않는다 | 흐름 밖: 믹서 Fr 감도 | §3-5 L90 · Fig 10 · §8-3 L170 | [판독] · mm 유리 모세관
- [m] nase2001_granular_bond_collision_number_wet_cohesion | 함정 — 식 29 에 호퍼 · 드럼 속도식을 넣으면 인쇄 식 31 · 34 의 절반 · 식을 섞으면 Co 가 2 배 어긋남 | 흐름 밖: 믹서 Co 계산 | §3-6 L97 · §10-2 L185 | [우리 산술] · λ² 에 흡수되는 상수 차
- [m] neumann2021_garnet_3d_structure_grain_boundaries_li_transport | 보정 → 예측 분리: 치밀 시료로 입계 값을 맞추고 같은 값으로 다공 시료를 예측 · 실패는 손잡이별 민감도로 보고 · 두 번째 조정 뒤의 일치 ("excellent agreement") 는 예측이 아님 · bulk σ · 입계 i₀₀ · 2차상이 같은 곡선을 맞춰 EIS 로 분리 불가 (저자) | 단계 4 → 단계 5 · 조건 R5 · 결과 전 대조 항목 | §4-4 L154–158 · §7-4 L233–235 · §10-1 L295 | stated · 저자 문구 "our model simulations only reproduce qualitative trends" (p.4795) · garnet 소결
- [m] neumann2021_garnet_3d_structure_grain_boundaries_li_transport | 입계 넓이 = voxel 면 세기 (무작위 방향 평균 ≈ 1.5 배) → 같은 격자에서 맞춘 계면 상수는 해상도에 묶임 · 넓이 보정 뒤 참 넓이당 값이 격자 이동에 강함 | 단계 7 · 흐름 밖: Rint ② SE–SE 계면항 | §7-5 L237–240 · §8-③ L267 | 카드 해석 (lindblad2005 카드 인용) · 논문은 이 점을 다루지 않음 (L302)
- [m] neumann2021_garnet_3d_structure_grain_boundaries_li_transport | 부피 ≠ 넓이 — 2차상 0.77 vol % 가 SE 표면 ≈ 2.2 % 를 얇게 덮으면 뚜렷한 둘째 반원 (뭉친 그대로면 ≈ 1.2 % 접촉 · 작은 특징) → 얇게 펴진 절연상 효과는 부피분율로 가늠 불가 | 흐름 밖: PTFE · SDCP 피복 표현 | §3-4 L111 · Fig 7 · §8-④ L268 | stated · 정성 결론만
- [m] neumann2021_garnet_3d_structure_grain_boundaries_li_transport | 피복은 비율보다 연결성 — 기공 속 Li 가 SE 표면을 55 → 73 % 덮어 퍼콜이 되면 ASR 15–16 → 6 Ω cm² (덮임 0 % ≈ 1100) · 해상도 탓에 퍼콜에 필요한 Li 를 과대평가했을 것 (저자) | 단계 7 (피복 정의) | §3-6 L124–134 · Table S5 · §7-8 L254–256 | stated · Li 금속 셀 (양극 아님)
- [m] nirmalraj2009_swcnt_network_junction_resistance | 탄소 접합 단일 손잡이 R_j,0 의 성립 조건 셋 (접합 지배 · 망 형태 고정 · 접합 상태 같음) 을 문장으로 적고, 접합 지배 여부는 보정 뒤 소산 분담 (접합 몫) · 섬유 σ ÷10 감도 팔의 σ_e 변화로 숫자 확인 | 단계 7 · 흐름 밖: Rint ② 보정 | §8-① L143 · §9 (가)-2 · 3 L151–152 · Fig 5 | stated (논문 Fig 5) · 카드 제안 · SWCNT ≠ VGCF
- [m] nirmalraj2009_swcnt_network_junction_resistance | 같은 SWCNT 에서 다발 크기 (D/A 27 배) · 질산 처리 (표 ÷1.41–2.88) · 1000 °C 처리 (×2.55–6.82) 가 접합 평균을 바꿈 → R_j,0 는 재료값이 아니라 그 침대의 접합 상태값 · SBE → DBE 예측은 같은 상태 가정 위 | 흐름 밖: Rint ② 한정어 (등록 R §7-1 ②) | §3-3 L66–76 · §9 (가)-1 L150 | stated (그림 라벨) · 배수 = derived(ours) · 요약 범위 ÷2.4–2.9 와 다름 (카드 문제)
- [m] nirmalraj2009_swcnt_network_junction_resistance | VGCF 응집 대리 지표 (섬유마다 접촉 instance 수 · 같은 섬유 쌍의 다중 instance) 를 SBE · DBE 나란히 보고 (새 문턱 없음) | 흐름 밖: Rint ② S0 census | §7-3 L139–140 · §8-③ L145 · §9 (가)-5 L154 | 카드 제안 · 보고 전용

## n — 논문 에이전트 후보 (litdb 카드 없음)

- [n] Pinson, Zou, Yu, Zulli, McCarthy, "Coordination number of binary mixtures of spheres", J. Phys. D 31 (1998) 457 (카드 표기 그대로 · 이름 머리글자 · DOI 없음 — 서지 일부만) | m — 혼합지표 E_XY 정규화의 부분 배위수 Z_ij: nadeem 카드는 입자수 분율 정규화가 Z_i 가 같을 때만 옳고 real_14 의 Z 가 62 배 산포한다며 "고칠 도구를 인용해 놓고 쓰지 않았다" 고 적음 (nadeem L58–59 · L432–435) | papers/ ls 에 pinson* 없음 · grep "Pinson" = chandratilleke2012 · chibwe2020 · nadeem2023 의 언급뿐
- [n] German, "Coordination number changes during powder densification", Powder Technol. 253 (2014) 368 (서지 일부만 — 이름 머리글자 · 공저자 · DOI 카드에 없음) | j · m — 압밀이 배위수를 바꾸는 크기: nadeem 카드 §8-③ (L538–546) 의 근거이고 우리 단계 5 · 7 의 압축 중 접촉수 변화 해석에 직접 닿음 | papers/ ls 에 german* 없음 · grep "Coordination number changes" = nadeem2023 만 · (같은 축의 arzt1982_particle_coordination_densification_spheres 카드는 있음 — 다른 논문)
- [n] J.F. Gilchrist, D.V. Khakhar, J.J. McCarthy, J.M. Ottino, "Chaotic mixing of granular materials in two-dimensional tumbling mixers", Chaos 9 (1999) 195–205 (nase 카드 §11 L205 그대로) | g · m — 드럼 Co 의 δ/R_t ≈ 0.03 출처 (2D 드럼 값 · 4 제곱이라 민감 · nase L36 · L99 · L190) — 3D 드럼에 그대로 써도 되는지 | papers/ ls 에 gilchrist* 없음 · 제목 grep = nase2001 만
- [n] Oguchi, T., Tamatani, M., 1986. "Contact electrification in inorganic binary compounds", Journal of the Electrochemical Society 133, 841–847 (matsusaka 카드 §11 L341 그대로) | m — 카드의 유일한 황화물 문장 "The same tendency is observed for metal fluorides and metal sulfides" (p.5786) 에 자료가 없고 (L33 · L93) 카드가 "황화물 자료가 있는지" 를 원전 확인 과제로 남김 (L341) | papers/ ls 에 oguchi* 없음 · 제목 grep = matsusaka2010 만
- [n] Yoshida, M., Shimosaka, A., Shirakawa, Y., Hidaka, J., Matsuyama, T., Yamamoto, H., 2003. "Estimation of electrostatic charge distribution of flowing toner particles in contact with metals", Powder Technology 135/136, 23–34 (matsusaka 카드 §11 L348 그대로) | m — 믹서 DEM 에 대전을 넣는 구현 선례 (표면 대전 자리 32 · 200 · 392 개 · 충돌마다 CPD + 국소 전기장 · Fig 64–65 · matsusaka L162 · L288) | papers/ ls 에 yoshida* 없음 · 제목 grep = matsusaka2010 만
- (뺀 것: Sakuda 2013 · Thornton–Ning 1998 · Minnmann 2021 JES · Chandratilleke 2012 · Bielefeld 2019 · Doux 2020 = 카드 있음. Thornton 1997 (J. Appl. Mech. 64, 383–386) 은 카드가 없지만 같은 탄–완전소성 법칙 (항복 캡 · 큰 반경 제하) 을 thorntonning1998 카드가 담아 뺐다.)

## 카드 문제

### minnmann2022_designing_cathodes_solidstate (7)
1. 머리 메타 "type `DEM`" (L3) · "methods: dft" (L12) ↔ 본문 "시뮬레이션을 수행하지 않는다" (§4 L259) · 설계 Perspective (L21) — 메타가 본문과 다르다.
2. 순수 SE 10 % @ 300 MPa 의 귀속이 카드 안에서 서로 다르다: 끝 판정문 L429 "~10 % pure-SE … = Minnmann 2021 JES 040537" · §0 L39–41 ("Minnmann" 이라 적은 값들의 진짜 출처 = 두 1차 논문) ↔ §0 L51–55 · §6 L295 (우리 보정 표적) ↔ 10-03 정정 L434 (그 귀속은 틀림 · 출처 [미확인] · 외부 앵커 없음 · 원장 CL-94). 정정 표지는 붙었지만 옛 문장이 그대로 남아 있다.
3. §6 L296 이 `ours_minnmann … pure_SE,300,10,experiment_anchor` 행을 그대로 옮긴다 — 순수 SE 10 % @ 300 MPa 가 실험 근거 표지 (experiment_anchor) 로 적힌 행 (카드는 재명명을 권고 · 그 출처는 CL-94 로 철회).
4. Minnmann 2021 JES 복합 기공 범위가 둘: "13–17 %" (L40 · L44 · L62 · L291 · L293 · L407) ↔ "7.6–17 %" (10-03 정정 L434 · 메인 원장 CL-94 의 같은 문구).
5. L53 "2021 JES + Sakuda 가 정의한 LPSCl cold-press 치밀화 거동" ↔ L49 · L294 Sakuda 2013 = 75Li₂S-25P₂S₅ 유리 — 재료가 섞였다.
6. L313 "작동 압력(40 MPa)" — 이 카드 안의 근거 (§0 표 L92 · §2.2) 는 "수~수십 MPa" 뿐 · 40 MPa 의 출처가 카드 안에 없다 (luan2025 카드 L426 도 "Minnmann 40" — 어느 Minnmann 논문인지 두 카드 다 미기재).
7. L316 · L325 σ_grain 3.0 에 붙인 '단결정' 라벨 (Cronau) — 메인 원장 CL-91 · SELF-51 이 철회한 라벨 (3.0 = Cronau 2021 SI Fig S2c 펠릿값). L316 의 "일관된 스프레드" 서술도 그 라벨에 기댄다.

### luan2025_graded_cathode_400whkg_pouch (4)
1. L438 · L478 σ_grain 3.0 에 '단결정' 라벨 (Cronau) — CL-91 · SELF-51 철회 라벨. L478 의 "'펠릿 < 단결정' 서열 4번째 독립 확인" 은 근거를 잃는다.
2. L427 우리 MPM 기공 15.93 % 를 대조 값으로 적음 — 메인 CLAUDE.md 2026-08-12 정정: 이 값은 정지 프레임의 함수 (독립 정보 아님). 카드 작성 08-11 (정정 전날). 우리 쪽 값의 지위 변경 (카드 안 모순은 아님).
3. L441 우리 SDCP SBE · DBE σ_e 두 값을 "우리 σ_e" 범위 근거로 적음 — 메인 CLAUDE.md 가 HISTORICAL · 인용 금지로 돌린 vox 0.4 µm SDCP 캠페인 값 (숫자는 옮기지 않음 · 카드에는 금지 표지 없음 · 원장 quotation_ban 목록에는 없음).
4. L466 "LPSC 1–2 µm = 협동변형 (<3 µm 파쇄임계 아래)" — 메인 CLAUDE.md 의 Fan 2026 요약은 협동변형 < 1 µm · 파쇄 > 3 µm → 1–2 µm 는 그 사이 (확인 필요).
- (논문 쪽 · 카드가 이미 표지 — 세지 않음: Fig 5b 0.1 C 값 ↔ Fig 4d–f stated 값 L154–155 · L600–601 · σ_e 100 배 cm↔m L203–207 · 본문 Eq (1) ↔ SI Table S2 분모 L289–294 · COMSOL 컬러바 단위 L335–337.)

### nase2001_granular_bond_collision_number_wet_cohesion (1)
1. §3-1 L58 식 (5) k_y = (2/3)(F_y/α_y) — 같은 Thornton 법칙을 다룬 정본 카드 thorntonning1998 (Fig 2 행 L170) 은 선형 소성 가지가 항복점에서 Hertz 곡선에 접하고 P₀ = −P_y/2 에서 P 축과 만난다고 적음 → 그 기하면 기울기 = (3/2)P_y/α_y [우리 산술: Hertz 기울기 = (3/2)P/α]. 2/3 ↔ 3/2 — 원문 p.215 렌더 대조 필요 (카드 표지 [인쇄]).
- (논문 쪽 · 카드가 이미 표지 — 세지 않음: 식 29 ↔ 31 · 34 의 2 배 L97 · L185 · "Co 를 0 으로" p.219 ↔ "Co → ∞" p.218 L187 · 참고문헌 44 쪽 149–153 ↔ 41–44 L188.)

### nirmalraj2009_swcnt_network_junction_resistance (1)
1. 산처리 배수 요약 "÷2.4–2.9" (L1 · L18 · L130) ↔ §3-3 표 (L70–73) ÷2.88 · ÷2.05 · ÷1.41 · ÷2.41 → 표 범위 ÷1.41–2.88 (B · C 묶음이 요약 범위 밖). 열처리 "×2.5–6.8" 은 표와 맞는다.

### neumann2021_garnet_3d_structure_grain_boundaries_li_transport (1 · 낮음)
1. Fig 1 행 L174 · §7-4 L234 "SBE 1.63 보정 / DBE 4.68 홀드아웃" — 같은 배치 nirmalraj2009 카드 L157 은 "DBE 4.68 은 holdout (현 세대 보정에 이미 쓰임 · K2)" 한정어를 붙이는데 neumann 카드에는 없다 (카드 사이 서술 차이).
- (논문 쪽 · 카드가 이미 표지 12 항 — §10-4 L299: Table S4 의 F 오기 · R 자리 Rydberg · "β-LPS" · σ_eff,bulk 56 % 본문 ↔ SI · ASR 본문 ↔ Table S5 등.)

### nadeem2023_gnn_mixing_index (1 · 낮음)
1. 같은 전망 문장의 인용이 두 꼴: L45–46 "can be readily adapted to ... DEM" ↔ L631–632 "can also easily be adapted to 3D data, such as those generated by DEM" — 한 문장인지 두 문장인지 원문 대조 필요.

### matsusaka2010_triboelectric_charging_powders_review
없음 (n₀ · 표면 전하 밀도 · F_es/F_JKR 표 · L₀ 산술을 다시 해 보니 카드 값과 맞음). 논문 쪽 (카드가 이미 표지): Fig 26 캡션 300 ↔ 200 µm · Fig 13 축 0.01 · 식 (7) "l" 미정의 · Fig 3 단위 (카드가 숫자 인용 금지 L331) · 식 (29) 근사를 "=" 로 (L330).
