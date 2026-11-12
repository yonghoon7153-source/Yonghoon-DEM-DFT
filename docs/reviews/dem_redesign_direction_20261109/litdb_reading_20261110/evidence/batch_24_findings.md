# batch_24 정독 근거 (카드 6 장 · 전문 읽음 · 2026-11-11)

읽은 카드: `koo2025_cnt_wrapped_sc_nca_dry_cathode` (483 줄 · 3 번에 나눠) · `koo2026_swcnt_sheath_thick_electrode` (1012 · 6 번) · `lee2024_shear_force_dry_process_cathode_coverage` (419 · 3 번) · `lee2025_corolling_dryprocess_lpscl_ptfe` (161 · 1 번) · `lee2025_dual_fibrous_ptfe_dry_electrode` (527 · 3 번) · `lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode` (400 · 3 번). 끝까지 못 읽은 카드 없음 (모두 마지막 줄까지).

배치의 성격: 건식 전극 · 탄소/바인더 형태 실험 6 편. 액체 LIB 4 편 (koo2025 = 단결정 NCA + MWCNT · koo2026 = NCMA + SWCNT sheath · lee2025_dual = NCM811 + PTFE 이중 섬유 · lee2026 = Si/흑연 건식 음극 + Li/Cu 밑층) + 황화물 ASSB 2 편 (lee2024 = NMC532/LPSCl 피복률 · lee2025_corolling = NCM811·82/LPSCl/VGCF/PTFE co-rolling). 수치 해석 = 복셀 디지털 트윈 (koo2025 · koo2026) · COMSOL 2D (lee2024) · COMSOL 3D DFN + MD (lee2026). **DEM · MPM 을 쓴 카드는 없다. 순수 SE 의 압력별 기공 곡선 · 탈압 되돌아옴 실측 · SE 항복/경도 · 큰 변형 접촉 법칙을 준 카드도 없다.** 가압 · 탈압 계획에 쓸 것 = 순수 LPSCl 펠릿 한 점 (lee2024) · 가압 중 AM 파괴의 SC/PC 서열과 압력 의존 (lee2025_corolling · koo2025) · 실험 기공 규약 (koo2026 밀도 기반 · lee2025_dual Hg ↔ 밀도 기반) · 피복 측정 규약 (lee2024) · τ 의 방법 · 라벨 함정 (koo2025 · koo2026).

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (`[인쇄]` · `[판독]` · `[우리 산술]` (= 카드 작성자의 산술) · `[추정]` · `[미확인]` · `stated` · `digitized` · `TREND`) · 없으면 "표지 없음". "카드 풀이" = 논문 문장이 아니라 카드 작성자의 서술. 큰따옴표 안 영어 = 카드가 옮겨 둔 원문. 랩 표준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³) 은 고정 — 이 배치의 다른 값은 "랩 표준과 다른 문헌 값" 으로만 적었다.

**인용 금지 표지가 붙은 값 (숫자로 옮기지 않음 · 위치만)**: koo2026 L716–717 (코드 주석의 sheath 두께 추론값에 "do not cite … (Koo)" 표지 · 같은 값이 L637 에도). 그 밖에 값에 붙은 '인용 금지' 표지 없음 (lee2025_dual L518 의 '인용 금지' 는 SAICAS 동영상을 압밀 대응물로 쓰지 말라는 용도 제한 · 숫자 아님).

---

## a. 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선 · 진밀도 · 질량 기준 · 누른 채 / 뺀 뒤

곡선은 이 배치에 없음. 한 점과 관련만:
- [a] lee2024_shear_force_dry_process_cathode_coverage | 순수 LPSCl 펠릿 한 점: 32 mg · ⌀6 mm PEEK · 1 TON 3 min (= 347 MPa) · 두께 725.0 µm · R 304.9 Ω · σ 0.8 mS/cm (25 °C) → 밀도 1.56 g/cm³ (질량 ÷ 기하 부피 = 질량 기준) · 결정밀도 1.86 g/cm³ (이 논문 밖 값 = 다른 카드 `lee2026_unveiling_ptfe_dry_electrode_digital_twin` 의 SI p.17 값) 기준 상대밀도 ≈84 % (공극 ≈16 %) | §3-9 L204–206 · §3-10 L213 · SI S12 · 본문 p.8 식 1 | [인쇄] (질량 · 두께 · 저항 · σ) · [우리 산술] (압력 · 밀도 · 상대밀도) | 한 압력 한 점 · 두께는 "EIS 뒤 측정" (누른 채 / 뺀 뒤 명시 없음) · 1 TON = 1000 kgf 가정 · **랩 표준과 다른 문헌 값** (진밀도 1.86 ↔ 랩 1.64 g/cm³ · 공극 ≈16 % ↔ 랩 10–13 %)
- [a] lee2025_corolling_dryprocess_lpscl_ptfe | 순수 LPSCl 펠릿 σ_ion pristine 2.19 → 볼밀 1.64 mS/cm · σ_e 5.0×10⁻⁴ → 3.3×10⁻⁴ mS/cm — 펠릿 성형 압력 · 밀도 · 기공은 카드에 없음 | §3 L38–39 · Supp Fig 4e,f | stated | 기공값 없음 · 성형 조건 카드에 없음
- koo2025 · koo2026 · lee2025_dual · lee2026: SE 없음 (액체 LIB).

## b. 압력을 뺄 때 되돌아오는 양 · 잰 방법

이 배치에 없음 (성형 뒤 탈압 되돌아옴을 잰 카드 없음). 관련만:
- [b] lee2025_corolling_dryprocess_lpscl_ptfe | 500 MPa 제조 뒤 운전 스택압 75 → 2 MPa 에서 사이클 뒤 계면 void 비 freestanding 4.0 → 15.5 · co-rolled 1.9 → 3.5 (ImageJ 하위 5 % 문턱 · 세 영역 상대비) · 2 MPa 에서도 500 사이클 >80 % 유지 (75 MPa >95 %) | §3 L45 · §5 L83 · §6 L98 · Fig 5a,b,e,f · Supp Fig 27–29 | stated | 되돌아옴 측정 아님 (사이클 뒤 계면 void · 상대 지표)
- [b] lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode | 자립 막 ≈85 µm → 라미네이트 뒤 전극 63–65 µm — 줄어든 과정 (라미네이트 압밀) 서술 없음 · 압력 미기재 | §3-1 L73 · L77 | [인쇄] (두께) · [미확인] (과정) | 가압 뒤 두께만 · 되돌아옴 아님
- [b] koo2026_swcnt_sheath_thick_electrode | 파우치 장기 사이클 외부 가압 1 MPa (Table S8) — 탈압 거동 기록 없음 | §11.9 L906 | 표지 없음 | 운전 압력 기록일 뿐

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 세기와 견줄 환산

SE 의 항복 · 경도 · 크리프 값은 이 배치에 없음. 일축 항복 세기와 견줄 환산도 없음. 관련만:
- [c] koo2025_cnt_wrapped_sc_nca_dry_cathode | AM 입자강도 = nano-press 로 입자를 10 % 변형시키는 압력, H = 2.8P/(π·d_p²) — 단결정 SC-NCA 111.63 vs 다결정 PC-NCA 48.96 MPa (≈2.3×) | §5(a) L245–246 · §8 L357 · SI Fig S23 | 카드가 '본문/표 명시값 (정밀)' 으로 분류 (L457) | NCA (AM · SE 아님) · 식은 하중 → 입자강도 환산 (일축 항복 환산 아님) · 액체 LIB
- [c] koo2026_swcnt_sheath_thick_electrode | VMS 디지털 트윈 입력 NCMA 영률 105 GPa · ν 0.27 (NCM811 값 대용) · 3.4 vol% 팽창 (부분몰 팽창계수 2.912e-7 m³/mol) · 모든 상 선형탄성 | §5 L281–282 · §11.10 L935–937 · L948 · SI Note S5 · Fig S28 | 표지 없음 (Table S7 'NCM811 대용') | 탄성값만 (항복 없음) · 다른 재료 값을 빌림
- [c] lee2025_corolling_dryprocess_lpscl_ptfe | PTFE storage modulus 30 → 120 °C 에서 67 % 감소 (≈150 → 50 MPa · DMA 1 Hz) · 인장강도 SSE 막 0.049 · 전극 0.441 · co-rolled 0.510 N/cm (n=5) | §3 L42–43 · Supp Fig 10 · Fig 3b | stated | 바인더 · 막 값 (입자 항복 아님)
- [c] lee2025_dual_fibrous_ptfe_dry_electrode | 건식 자립막 인장강도 SDE 0.47 · DDE 1.39 N/mm² · "yield strain" (= 최대하중 변형률) 0.35 / 0.70 % · 시컨트 탄성률 ≈0.13 / 0.20 GPa (카드 계산) | §4 L157–159 · Fig 4c | stated (강도 · 변형률) · derived TREND (시컨트) | 면내 인장 — 카드: 우리 압축 접촉강성 · AFM 압입과 같은 양 아님 (L389 · L519–520) · '항복' 이름이 최대하중점을 가리킴
- [c] lee2024_shear_force_dry_process_cathode_coverage | LPSCl = "ductile sulfide solid electrolyte" (전단 · 가압에서 변형해 활물질을 덮는다) — 값 없음 | §3-2 L96 · §4-2 L232 · p.2 | [인쇄] (문장) | 정성
- [c] lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode | Li 금속 = "항복 강도가 아주 낮은 금속" (값 없음) | §4-3 L189 · §7-2 L267 | [추정] (카드 풀이) | 논문 문장 아님

## d. 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

하중 몫 · 재밍을 잰 카드 없음. 단단한 입자 (AM) 의 압축 중 파괴만:
- [d] lee2025_corolling_dryprocess_lpscl_ptfe | 가압 뒤 큰 다결정 PC-NCM (5–15 µm) 균열 · debris / 작은 단결정 SC-NCM (3–5 µm) 무손상 · 300 vs 500 MPa: PC 는 500 에서 균열 ↑ · SC 는 균열 없음 · 접촉 ↑ · 저자 서술: PC 는 거친 표면 + 큰 CAM / 작은 SE 사이 큰 void → 가압 시 심한 균열, SC 는 압밀 전부터 조밀 · 친밀 접촉 | §3 L46 · §4 L63–64 · §5 L73 · L87–89 · Fig 2b,c · SI Fig 6–8 | stated (SEM) | 정성 (균열 분율 수치 없음) · 하중 몫 값 없음
- [d] koo2025_cnt_wrapped_sc_nca_dry_cathode | 전극 압밀 뒤 단면 미세균열 면적 분율 PC-NCA 7.8 % @3.6 g/cc vs SC-NCA 0 % @4.0 g/cc · 카드: "단결정은 견고 → 고밀도 압축 (4.0 g/cc) 가능, 다결정은 입계균열로 못 감" | §5(a) L247–250 · SI Fig S23d,e | 카드가 '본문 명시값' 으로 분류 | NCA · 액체 LIB · 캘린더 압력값 없음 (밀도로만) · 하중 몫 없음
- [d] lee2024_shear_force_dry_process_cathode_coverage | 단면에서 NMC 균열 (펠릿 · 건식 큰 입자 일부) · 펠릿 단면 수평 균열 | §4-2 L232 · §3-2 L97 · S2 · S8 | [판독] (정성) | 수치 없음
- [d] lee2025_corolling_dryprocess_lpscl_ptfe | co-rolled 막 인장강도 ≈ 두 막의 합 (0.510 ≈ 0.049 + 0.441 N/cm) → 카드: "둘 다 하중분담" | §3 L43 · §5 L77 · Fig 3b | stated (값) · 카드 풀이 (해석) | 막 수준 인장 (입자 하중 몫 아님)

## e. 점접촉 법칙이 깨지는 범위와 대안 (multi-contact · MDR · EEPA · Thornton–Ning · Storåkers) · 맞춘 값 수

이 배치에 없음 (DEM · 접촉 법칙을 다룬 카드 0 편).

## f. MPM 의 접촉 · 다물체 · 강체 결합과 해상도 규칙 · 수치 오차 추정

이 배치에 없음 (MPM 카드 없음). 관련만 (다른 수치 해석의 해상도 · 오차 추정):
- [f] koo2026_swcnt_sheath_thick_electrode | FIB-SEM 820 장 · milling 32.5 nm · voxel 31.01 / 37.22 nm · 재구성 부피분율 ↔ 이론값 상대오차 6.56 % (CB-wet) / 5.45 % (SWCNT-dry) · 2C 방전 시뮬 ↔ 실측 상대오차 ~2.15 % | §5 L239–252 · §11.10 L943–945 · SI Note S2 · S4 · Fig S25 | 표지 없음 | 복셀 균질화 (MPM 아님) · 카드: 입력 σ_s 가 이미 전극 시트 측정값이라 Exp–Sim 일치는 "자기일관 검사" (L772–775)
- [f] koo2025_cnt_wrapped_sc_nca_dry_cathode | FIB-SEM 840 장 · voxel 32.5 · 37.22 nm · Unet 분할 · 재구성 ↔ 이론 부피분율 편차 (카드에 두 값 — 카드 문제) · σ_s,eff exp ↔ sim 편차 4.2 % | §4 L201–204 · L221–222 · §7 L337 | 표지 없음 | MPM 아님
- [f] lee2025_dual_fibrous_ptfe_dry_electrode | micro-CT 복셀 650 nm = rope Ø 248 nm 의 2.6 배 → "이 CT 는 피브릴을 원리적으로 못 본다" (CT 의 'pore–CB–PTFE' 상 = 세 상의 혼합 저밀도상) | §7 L262 · §13 L512–513 · Fig 3 | 표지 없음 (카드 판정) | 영상 해상도 사례 (MPM 아님)
- [f] lee2024_shear_force_dry_process_cathode_coverage | 논문의 "MPM" = multi-particle model (COMSOL 전기화학) — 물질점법과 다른 말 | 머리 L38 ⑤ · §3-6 L166 · §10 L383 | [인쇄] | 문헌 검색 · 인용 때 용어 충돌

## g. 2D 결과를 3D 로 옮길 때의 경고 · 증거

- [g] lee2024_shear_force_dry_process_cathode_coverage | 피복 = 2D 단면의 둘레 길이 몫 ↔ 우리 = 3D 면적 몫 · 카드: 등방 무작위 단면이면 둘레 몫의 기댓값 = 표면적 몫 (입체해석학 S_V ↔ L_A) 이라 평균끼리는 견줄 수 있으나, 입자별 값은 단면 위치 (적도 ↔ 극) 에 따라 흔들려 2D 분포 폭이 더 넓다 | §7-2 L302 | [추정] (논문은 언급 안 함) | 카드 풀이 · 검증 없음
- [g] lee2024_shear_force_dry_process_cathode_coverage | COMSOL 1D SPM 을 2D 로 확장 · 면외 깊이 D = 36.378 m 로 모델 활물질 부피 V = π·rp²·D = 11.429 mm³ 를 셀 실제값에 축척 · 그 V 의 겉보기 NMC 밀도 2.73 g/cm³ (근거 미확인) | §3-6 L129 · L139 · L151 · Table S1 | [인쇄] (D · V) · [우리 산술] · [추정] | 2D 모델의 3D 축척 근거 미기재
- 다른 카드: 이 배치에 없음.

## h. DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

이 배치에 없음 (DEM → FE · MPM 을 한 카드 없음). 관련만 (DEM 없이 FE · 복셀 기하를 만든 선례):
- [h] lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode | FEM 기하 = Blender 4.3 으로 Si · C 입자를 "sequentially stacking … within a 50 μm thick domain" → COMSOL 메시 · 압밀 없음 · 접촉은 메시로 붙어 접촉 저항 항 없음 | §3-7 L173 · §4-3 L190 · SI p.4–5 | [인쇄] (방법) · [추정] (CONTACT_FREE 범주) | 영역 50 µm ↔ 실제 63–65 µm · 물성 · 입자 수 미기재
- [h] koo2025_cnt_wrapped_sc_nca_dry_cathode · koo2026_swcnt_sheath_thick_electrode | 측정 구조 (FIB-SEM 토모) → 분할 → 복셀 균질화 · PNM · 1D 전기화학 — 카드: "토모는 이미 압축된 전극" · 압력 → 구조 예측 없음 | koo2025 §4 L199–212 · koo2026 §5 L238–252 · §9(e) L531 | 표지 없음 | 출력단 재구성 · 압축 경로 없음

## i. 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음 (AM + SE 복합의 압력별 기공을 잰 카드 없음). 관련만:
- [i] lee2024_shear_force_dry_process_cathode_coverage | NMC532 : LPSCl : SP = 80 : 18.5 : 1.5 (펠릿) · 80 : 17 : 1.5 : 1.5 (습식 · 건식) 전극을 LPSCl 분리막 위에서 7 TON (⌀13 mm → 517 MPa) 가압 — 전극 두께 · 공극률 · 밀도 미확인 | §3-1 L65 · L70–71 · L76 | [인쇄] · [우리 산술] (MPa) · [미확인] (공극률) | 기공값 없음
- [i] lee2025_corolling_dryprocess_lpscl_ptfe | 양극 CAM : SSE : VGCF : PTFE = 80 : 17 : 3 : 0.5 · 두께 120 µm · 31.4 mg/cm² · 제조 500 MPa — 정량 기공 n/a | §2 L23 · §3 L48 · §4 L61 | stated · n/a | 기공값 없음
- 참고 (AM + SE 아님 · 압력 축 없음 · 비교 대상 아님): 액체 LIB 전극 기공 koo2026 Table S3 22.3 / 22.6 / 18.8 / 16.1 % (밀도 기반 · L805–808) · koo2025 MIP 0.14 / 0.083 ↔ 토모 14.84 / 13.47 % (L187 · L204) · lee2025_dual Hg 27.4 / 27.1 % (L150).

## j. 카드가 스스로 적은 한계 가운데 가압 · 탈압 계산과 닿는 것

- [j] koo2026_swcnt_sheath_thick_electrode | 그 논문엔 입자스케일 압축역학 예측 없음 — "고정 미세구조 — 토모는 이미 압축된 전극" · 압력 → 미세구조 → σ 예측 없음 | §9(e) L531–534 · §10 L586–588 | 카드 풀이 | —
- [j] koo2026_swcnt_sheath_thick_electrode | VMS 는 모든 상 탄성 (소성 미포함, preliminary) · 역학 = 평형식 + 운동학식, 선형탄성 · 소성 없음 (Note S5 명시) | §5 L282 · §11.10 L948 | 표지 없음 | 압밀 소성 없음
- [j] koo2026_swcnt_sheath_thick_electrode | 분말 전도 최대 64 MPa → "300 MPa 외삽은 금지" · 전극 시트 σ 는 외부 가압 조건 자체가 기술되지 않음 · 온도 · 습도 · 집전체 부착 여부 미기록 | §11.4(a) L739–740 · §11.4(b) L752–755 | 카드 판정 | 압력 범위 한정
- [j] lee2024_shear_force_dry_process_cathode_coverage | 모델 ↔ 실험 정량 맞춤 없음 — "this model cannot precisely match the experimental results" (p.5) · 압력별 · 혼합 시간별 피복 안 함 · 셀 적층압 MPa · 전극 두께 · 공극률 미확인 · SEM 단면이 셀에서 꺼낸 시료인지 따로 누른 시료인지 미확인 | §6 L279 · 머리 L38 ④ · §4-1 L229 | [인쇄] (인용문) · [미확인] | 가압 조건 결손
- [j] lee2025_corolling_dryprocess_lpscl_ptfe | 시뮬레이션 0 → 압밀 기공 · Heckel · 배위수 · coverage · E_SE · σ_y · 접촉면적 전부 n/a · void 는 사이클 뒤 계면 상대비 · co-rolling 전단은 "우리 RVE 모델이 안 다루는 공정 영역" | §10 L146–147 · L154–155 | 카드 판정 | —
- [j] lee2025_dual_fibrous_ptfe_dry_electrode | 다압력 스윕 0 (롤프레스 압력조차 미기재 → Heckel · 압밀곡선 불가) · 피브릴 치수는 한 조건 한 세트 (압연 전 / 후 명시 없음) · 동영상 = 절삭 시험 (압밀 아님) | §10.6 L430–432 · §13 L497–498 · L518 | 카드 판정 | —
- [j] lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode | 라미네이트 압력 · 온도 미확인 · ≈85 µm → 63–65 µm 압밀 과정 서술 없음 · FEM = 압밀 안 한 Blender 적층 · 물성 · 시간 · 메시 전부 미확인 · Li 금속이 라미네이트 때 막 바닥으로 흘러 맞물렸을 가능성 논의 없음 | §3-1 L74 · L77 · §10 L344 · §4-3 L189 · §7-2 L267 | [미확인] · [추정] | 음극 · 액체 LIB
- [j] koo2025_cnt_wrapped_sc_nca_dry_cathode | 단일 스냅샷 (시간 · cycling chemo-mechanical 은 공통 GAP) · 압력값 없이 밀도로만 | §10 L455 | 카드 판정 | —

## k. DEM 의 한계 (인용 서지 병기)

이 배치 6 편 모두 DEM 을 쓰지 않는다 → 논문 문장으로는 "말 없음". 카드 풀이와 인용 가능한 실험 사실만:
- [k] koo2025_cnt_wrapped_sc_nca_dry_cathode (Koo J.K. et al., *Energy Storage Materials* 78 (2025) 104270) | 말 없음 (DEM 사용 없음) | — | — | —
- [k] koo2026_swcnt_sheath_thick_electrode (Koo J.K. et al., *Joule* 10 (2026) 102392) | 말 없음 · 카드 §9(e) 는 그 논문에 "explicit 접촉 σ triad 없음 (GeoDict effective σ만, 우리 Holm constriction 없음 → 점접촉 sub-voxel 못 잡음)" 이라 적음 — DEM 의 한계가 아니라 그 논문의 범위 | §9(e) L531–533 | 카드 풀이 | —
- [k] lee2024_shear_force_dry_process_cathode_coverage (Lee D. et al., *Nat. Commun.* 15, 4763 (2024)) | 말 없음 · 카드 풀이: "전단으로 SE 가 펴져 덮이는 기전은 우리 두 모델 어디에도 없다 — 코팅 · 피복 상태는 우리 쪽에서 입력이지 결과가 아니다" · "건식 67 % 는 강체 구 DEM 이 못 가는 영역 (MPM 소성 Tabor 띠 74 % 근처)" · 인용 가능한 실험 사실 = 같은 조성에서 건식 피복 67.2 % ↔ 무바인더 펠릿 30.6 % · 원문 "the shear force effect plays a critical role in particle-to-particle contact by deforming the ductile sulfide solid electrolyte particles" | §4-2 L234 · §7-1 L291 · §8-2 L335 · §3-2 L96 (p.2) | 카드 풀이 · [추정 · 정의 다름] · [인쇄] (원문) | 논문은 DEM 을 평가하지 않음
- [k] lee2025_corolling_dryprocess_lpscl_ptfe (Lee D.J. et al., *Nat. Commun.* 16, 4200 (2025)) | 말 없음 · 카드 풀이: "PC-NCM은 진짜로 깨진다(rigid sphere가 아님 — 우리 DEM AM_P 파괴/Auerbach가 맞는 방향)" · 인용 가능한 실험 사실 = 가압 뒤 PC-NCM 균열 · debris, SC-NCM 무손상, 500 MPa 에서 PC 균열 증가 (Fig 2b,c · SI Fig 6–8) | §4 L57–60 · §3 L46 · §5 L87–89 | 카드 풀이 · stated (SEM) | 균열 분율 수치 없음
- [k] lee2025_dual_fibrous_ptfe_dry_electrode (Lee K.-H. et al., *Energy Environ. Sci.* 18, 8446–8461 (2025)) | 말 없음 | — | — | —
- [k] lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode (Lee H.-W. et al., *Energy Environ. Sci.* 19, 1944–1953 (2026)) | 말 없음 · 카드 풀이: "2.1 g cm⁻³ (공극률 ≈3–7 % [우리 산술 · 가정]) 은 강체 구 DEM 의 바닥 (~20 %, frame[1]/[2]) 보다 훨씬 치밀하다 — 흑연 판상 입자의 재배열 · 변형 · 섬유 PTFE 가 만드는 치밀화이므로 우리 강체 구 DEM 의 검증 표적으로 쓸 수 없다 (입자 형상 · 크기 정보도 없음)" | §7-2 L268 | 카드 풀이 · [우리 산술 · 가정 밀도] (공극률) | ~20 % 는 이 논문 값이 아님 (카드가 우리 frame 에서 가져옴)

## l. 소성변형이 왜 어려운가 · 택한 우회 (인용 서지 병기)

이 배치에 입자 소성을 계산한 카드 없음 → 어려움에 대한 논문 설명은 "말 없음". 각 논문이 택한 단순화만:
- [l] koo2026_swcnt_sheath_thick_electrode (Koo J.K. et al., *Joule* 10 (2026) 102392) | 전기화학-역학 VMS 디지털 트윈 = 재구성 3D 위 Li 농도 의존 변형 → 응력 · 모든 상 탄성 (소성 미포함, preliminary) · 입력 = NCM811 값 대용 (E 105 GPa · ν 0.27 · 3.4 vol% 팽창) · 맞춘 값 0 개 (빌린 값) · 소성을 뺀 이유 서술 없음 · 비용 미기재 | §5 L280–285 · §11.10 L935–937 · L948 · SI Note S5 · Fig S28 | 표지 없음 ('Note S5 명시') | 압밀 아님 (충방전 팽창 응력)
- [l] lee2024_shear_force_dry_process_cathode_coverage (Lee D. et al., *Nat. Commun.* 15, 4763 (2024)) | 모델이 입자 형상 · 접촉 · SE 망을 그리지 않고 피복을 입력으로 줌 (2D 원 둘레 일부를 절연 공극으로 지정) · 양극 두께를 입자 하나로 줄여 "eliminating other effects such as ionic conduction in the bulk electrode domain" (p.5) · tuned 값 5 개 (T · L_pos · i0_neg · cs0_pos · C_dl) · D_s 미기재 · "this model cannot precisely match the experimental results" (p.5) | §4-2 L233 · §3-6 L129 · L135–150 · 머리 L36 · §6 L279 · §10 L375–376 | [인쇄] | 소성 계산 없음 · 어려움 설명 없음
- [l] lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode (Lee H.-W. et al., *Energy Environ. Sci.* 19, 1944–1953 (2026)) | FEM 기하 = 압밀 없는 Blender 순차 적층 (강체 기하 · 접촉 저항 없음) · 카드 풀이: "무른 금속이 다공 입자층 바닥으로 흘러 들어가는 부피 보존 흐름" 은 MPM (J2 소성) 의 몫이고 접촉 면적 → 박리 강도는 DEM 의 몫 — "지금 우리 MPM 에 Li 금속 상 · 집전체는 없다" | §4-3 L190 · §7-2 L267 | [인쇄] (방법) · 카드 풀이 · [추정] | 이유 · 비용 서술 없음
- [l] lee2025_corolling_dryprocess_lpscl_ptfe (Lee D.J. et al., *Nat. Commun.* 16, 4200 (2025)) | 말 없음 (실험) · PTFE 섬유화 5 단계 기전 모식 (계면 접촉 → 전단 이동 · 바인더 응력 → 계면을 가로지른 인발 · 섬유화 → 새 접촉 → 두께 감소마다 반복) · 바인더 연화 (120 °C 에서 모듈러스 67 %↓) 를 공정 레버로 씀 | §4 L53–55 · L65 · SI Fig 18a · Supp Fig 10 | stated | 모델 없음
- [l] koo2025_cnt_wrapped_sc_nca_dry_cathode (Koo J.K. et al., *Energy Storage Materials* 78 (2025) 104270) · lee2025_dual_fibrous_ptfe_dry_electrode (Lee K.-H. et al., *Energy Environ. Sci.* 18 (2025) 8446) | 말 없음 | — | — | —

## m. 받아들일 통찰 (무엇을 · 어디에 · 왜)

- [m] koo2025_cnt_wrapped_sc_nca_dry_cathode | τ 는 방법 이름을 붙여 보고 — 같은 전극이 EIS-TLM (τ = R_ion·A·ε/(L·ρ)) 1.75 / 1.03 ↔ 디지털 트윈 확산 2.05 / 1.26 · 자리: 단계 7 (흐름 밖: τ 명명 · 보고) · 왜: 카드 "같은 전극인데 방법 따라 값 다름" | §3 L186–190 · §4 L226–227 · §8 L365–367 · SI Note S2 · Fig 4f | 표지 없음 | 액체 LIB
- [m] koo2025_cnt_wrapped_sc_nca_dry_cathode | 재구성 상 부피분율을 조성 · 진밀도 이론값과 대조해 편차 (%p) 를 보고하는 점검 (CB-wet SC-NCA 76.58 / CBD 8.58 / pore 14.84 % · CNT-dry 83.97 / PTFE 0.74 / CNT 1.81 / pore 13.47 %) · 자리: 단계 0 (기공 연산자의 상별 부피 점검) · 왜: 분할 품질을 이론 부피로 판정 | §4 L203–204 · §7 L336–337 · SI Fig S15–S16 | 표지 없음 | 카드에 편차 값이 둘 (카드 문제)
- [m] koo2025_cnt_wrapped_sc_nca_dry_cathode | 고립 기공 몫 (CB-wet 17.72 % ↔ CNT-dry 2.4 %) · PNM 기공 배위수 중앙 (3 ↔ 4) 을 기공 쪽 관측량으로 · 자리: 단계 7 (흐름 밖: 고립 SE 채널의 기공판 지표) · 왜: 고립 기공은 수송 기여 0 | §4 L215–219 · §8 L363–364 | 표지 없음 | 액체 LIB 기공
- [m] koo2025_cnt_wrapped_sc_nca_dry_cathode | AM 강도 정의 (10 % shape strain · H = 2.8P/(πd²)) 와 서열 SC 111.63 > PC 48.96 MPa · 4.0 g/cc SC 균열 0 % ↔ 3.6 g/cc PC 7.8 % · 자리: 조건 R7 · 결과 전 대조 항목 (단계 5 의 AM 파괴 정성 서열) · 왜: 같은 조성 SC ↔ PC 직접 대비 | §5(a) L245–250 · SI Fig S23 | 카드 '본문 명시' | NCA · 액체 LIB · 압력값 없음
- [m] koo2026_swcnt_sheath_thick_electrode | 실험 기공 규약 = 밀도 기반 ε = 1 − ρ_전극/ρ_mix (역혼합 진밀도 AM 4.8 · 탄소 1.6–1.7 · 바인더 1.78–2.2) — ε_sphere 도 ε_union 도 아님 · 자리: 단계 0 (실험 대조 전에 규약을 맞춤) · 왜: 카드 "실험이 보고하는 ε 은 이 밀도 규약" | §11.6 L810–815 · Table S3 각주 | [인쇄] (규약) | 액체 LIB 전극
- [m] koo2026_swcnt_sheath_thick_electrode | 맞추는 데 쓴 입력과 견주는 값이 같은 측정이면 일치는 검증이 아님 — 디지털 트윈 'active material σ_s' 입력 5.13 / 17.78 S/m = 실은 전극 시트 측정값 (Fig S15 의 역수) · Sim/입력 ≈0.94 · 0.91 → "자기일관 검사" · 자리: 결과 전 대조 항목 · 조건 R5 · 왜: 순환 검증 함정 | §11.4(b) L761–775 | [우리 산술] · 디지타이즈 | —
- [m] koo2026_swcnt_sheath_thick_electrode | 식을 자기 숫자로 닫아 라벨 확인 — D_eff 비 = (ε₂/ε₁)(τ₁/τ₂)² = 2.48 은 2.31 / 1.28 을 τ 로 읽을 때만 재현 (τ² 로 읽으면 1.37) · 본문 "high porosity" 와 달리 SWCNT-dry 기공이 더 낮음 · 자리: 단계 7 (흐름 밖: τ ↔ tau2 · 수송 tortuosity 명명) · 왜: 'tortuosity factor' 라벨을 METHODS 는 "square of tortuosity" 로 정의 — 문헌 라벨이 느슨 | §11.6 L820–830 · §11.13-2 L988–989 | [우리 산술] | 기공은 디지타이즈 토모 값
- [m] koo2026_swcnt_sheath_thick_electrode | 접촉 지배 → 부피 지배 이행: 분말 σ 이득 비가 펠릿 압력 16 → 64 MPa 에서 7.9× → 3.1× 로 단조 감소 → 이득은 고압 끝에서 읽고 범위 밖 외삽 안 함 · 자리: 결과 전 대조 항목 (흐름 밖: 접촉망 σ_e 의 압력 의존) · 왜: 가압이 discrete 탄소의 접촉을 강제 | §11.4(a) L722–740 | 디지타이즈 TREND | NCMA 분말 · 300 MPa 외삽 금지
- [m] lee2024_shear_force_dry_process_cathode_coverage | 피복 측정 규약을 결과 전에 고정 (화소 규칙 · 문턱 · 단면 수 · 입자 선택 · 평균 방식 개수 ↔ 둘레 가중 · AM–AM 면 처리) — 보고 30.6 ↔ 33.3 % 가 S13 구간 개수 평균으로는 35.3 ↔ 41.7 % (펠릿 ≈ 습식 판정이 평균 방식에 갈림) · 자리: 단계 7 · 단계 0 · 왜: 정의 차가 결과 차로 둔갑 | §3-2 L94 · §7-4 L316 · §10 L371–372 | [우리 산술] · [판독] | —
- [m] lee2024_shear_force_dry_process_cathode_coverage | 첫 외부 피복 대조점: 무바인더 손혼합 펠릿 (NMC/(NMC+LPSCl) 81.2 wt%) 30.6 % · 피복 20 % 미만 입자 21 % · S13 20 % 구간 분포 → 우리 침대에 2D 단면 둘레 판 (AM–AM 포함 / 제외) 추가 · 자리: 결과 전 대조 항목 (단계 7) · 왜: 바인더 · 혼합 전단 없는 쪽 = 우리 DEM 과 같은 쪽 | §7-2 L305 · §8-2 L334–336 · S13 | [인쇄] · [판독] | 2D · 정의 다름 · 517 MPa
- [m] lee2024_shear_force_dry_process_cathode_coverage | 공정 (전단) 이 만든 피복 차를 접촉 법칙 매개변수 (E 연화 · Stage-E) 로 흡수하지 않는다 — 같은 17 wt% SE 에서 습식 33 → 건식 67 % · 자리: 조건 R5 · 단계 4–5 (맞추는 값 하나) · 왜: 공정 효과를 재료 매개변수로 흡수하는 순환 (frame[4]) | §8-3 L338–341 | [추정] (카드 판단) | —
- [m] lee2024_shear_force_dry_process_cathode_coverage | 순수 SE 기준 펠릿은 질량 · 두께 · 성형 압력 · 측정 압력을 모두 기록해 상대밀도를 거꾸로 낼 수 있게 (이 논문은 32 mg · ⌀6 mm · 725 µm 로 재계산 가능) · 자리: 단계 4 (실험 기공 대조의 기록 항목) · 흐름 밖: σ₀ 기준 시료 · 왜: σ₀ · 밀도가 성형 · 측정에 따라 갈림 | §8-6 L353–356 · §3-9 L204–206 | [인쇄] · [우리 산술] | 진밀도 1.86 은 랩 표준과 다른 문헌 값
- [m] lee2025_corolling_dryprocess_lpscl_ptfe | AM 파괴의 압력 의존 대조: 가압 뒤 PC-NCM debris · SC-NCM 무손상 · 300 → 500 MPa 에서 PC 균열 ↑ · 자리: 조건 R7 · 결과 전 대조 항목 (단계 5 의 300 MPa 결과에서 AM_P 만 파괴되는지) · 왜: 같은 소재 (LPSCl + NCM811 · 82) | §3 L46 · §5 L87–89 · SI Fig 6–8 | stated (SEM) | 정성 · 분율 없음
- [m] lee2025_corolling_dryprocess_lpscl_ptfe | 수송 대조값에는 제조 압력 (500 MPa) 과 측정 압력 (75 MPa · Supp Fig 5) 을 같이 적는다 · 자리: 단계 6 · 단계 7 · 결과 전 대조 항목 · 왜: 측정은 일부 탈압된 운전 스택압 상태 | §3 L32 · L45 · §4 L61 | stated | —
- [m] lee2025_corolling_dryprocess_lpscl_ptfe | PTFE 함량 페널티 곡선 (CAM : SSE : VGCF = 80 : 17 : 3 고정 · 75 MPa): PTFE 0.5 / 2 / 5 wt% → σ_e 34 / 4.5 / 0.011 · σ_ion 0.069 / 0.024 / 0.007 mS/cm · 자리: 흐름 밖: PTFE 절연 페널티의 결과 전 대조 항목 · 왜: 같은 소재 · 같은 도전제 쌍 | §3 L32–33 · Supp Fig 5 | stated | 레시피 다름 (VGCF 3 · PTFE 0.5)
- [m] lee2025_corolling_dryprocess_lpscl_ptfe | ImageJ 하위 5 % 문턱 void 면적 분율 (전극 / 계면 10 µm / SSE 세 영역) 은 사이클 뒤 계면 void 의 상대비 — 압밀 기공과 다른 연산자 · 자리: 단계 0 (함정) · 왜: 카드 "우리 15.6% 와 직접 비교 금지" | §6 L98 · §10 L147 | 카드 판정 | —
- [m] lee2025_dual_fibrous_ptfe_dry_electrode | 계층 창 함정: 가는 계층의 지름 (rope 0.248 µm) 과 굵은 계층의 종횡비 (AR 160) 를 섞으면 키메라 · AR 은 스케일 불변 아님 (Ø 0.017–0.382 µm 에서 AR ≈27 · Ø 1–3 µm 에서 33–500) → 계층 하나를 골라 라벨 · 자리: 흐름 밖: 첨가제 (PTFE 피브릴) 기하 입력 · 왜: 두 출처가 같은 망의 다른 층을 잼 | §0 L38–40 · §10.5 L410–426 | stated (치수) · 카드 계산 (AR) | 액체 LIB · 한 조건
- [m] lee2025_dual_fibrous_ptfe_dry_electrode | 평균과 함께 시료 간 산포를 보고 — 체적 전자저항 SDE 1.78 ± 0.39 (CV ≈22 %) ↔ DDE 1.29 ± 0.02 (CV ≈1.6 %) · LEIS 띠무늬 · 자리: 흐름 밖: σ_e 실측 대조 · 보고 방식 · 왜: 카드 — 진짜 헤드라인은 "평균 1.4배" 가 아니라 "공간 산포가 무너진다" | §4 L153 · §4.1 L165–168 · Fig 2b | stated (평균) · digitized (오차) | —
- [m] lee2025_dual_fibrous_ptfe_dry_electrode | 기공을 두 독립 방법으로 맞춰 보기: 면적질량 / 두께 (3.117 g/cm³) + 가정 진밀도 (NCM 4.75 · PTFE 2.2 · CB 2.0 — 논문에 없음) → 25.8 % ↔ Hg 압입 27.1 % (1.3 %p 이내 · 가정 감도 ±1.3 %p) · 자리: 단계 0 · 왜: 규약 (Hg ≠ ε_sphere ≠ ε_union) 과 가정 진밀도 감도를 같이 적는 꼴 | §10.4 L386–387 | 카드 계산 | 액체 LIB
- [m] lee2025_dual_fibrous_ptfe_dry_electrode | 영상 복셀이 형상보다 크면 그 상을 못 봄 — micro-CT 650 nm > rope 248 nm · 자리: 단계 7 (흐름 밖: 해상도 규칙 = 형상 크기 ÷ 셀) · 왜: CT 의 'pore–CB–PTFE' 상은 혼합 저밀도상 | §7 L262 · §13 L512–513 | 카드 판정 | —
- [m] lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode | 두 처치를 함께 바꾼 두 점 비교 (프라이머 제거 + Li 추가 · 2×2 없음) 는 몫을 못 가름 → 설계표에 '처치가 함께 바꾸는 변수' 칸 · 자리: 흐름 밖: 믹서 V1 (코팅 상태) 설계 · 단계 0 (판정 설계를 결과 전에) · 왜: 원문 "due solely to the prelithiation" (p.1950) 이 프라이머 차를 무시 | §7-6 L289 · §8-1 L301–304 · §10 L338 | [인쇄] (원문) · 카드 판단 | —
- [m] lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode | 이득을 출발점 오프셋과 감쇠 기울기로 나눠 보고 — NCM 10 → 500 사이클 절대 감소 PrL-ThA 1.40 ↔ ThA 1.44 mAh/cm² (거의 같음) → 이득 = Li 재고 오프셋 · 자리: 흐름 밖: A10 사이클 원장 · R_int 트랙 보고 방식 · 왜: 재고 항과 접촉 · 수송 열화 항을 분리 | §3-5 L148 · §8-2 L306–309 | [판독] · [우리 산술] | 그림 판독
- [m] lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode | 메시로 붙인 접촉 (접촉 저항 없음) 위의 FEM 결과 = CONTACT_FREE 성격의 상한 · 압밀 없는 적층 기하 · 자리: 단계 7 (흐름 밖: 연속체 결과를 인용할 때 접촉 가지 표지) · 왜: 접촉 저항을 넣으면 SOC 깊이가 줄어드는 쪽 | §4-3 L190 · §7-3 L274 | [추정] | 물성 미기재
- [m] lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode | AM–AM 접촉 면적을 Holm 꼴 확산 전도도 (≈2·D·a) 로 바꾸면 접촉망 고상 Li 확산 채널 — STEP4 의 입자별 독립 구형 확산에는 없는 경로 (코드 메타 "inter-particle redistribution NOT modeled") · 자리: 흐름 밖: STEP4 · 왜: ASSB 에서는 고체 접촉이 기본 경로 | §7-1 L263 · §7-4 L277–278 · §8-3 L311–314 | [추정] | 제안 단계

---

## 카드 문제

**koo2025_cnt_wrapped_sc_nca_dry_cathode**
1. 철회된 출처를 앵커로 적음: "앵커는 Bazzoun(LPSCl)/Varkey(halide)/**Minnmann(LPSCl cold-press)**/#266/#271" 를 σ/porosity 절대앵커로 (L42 · L377–378 · L445–446 · L465 · L483) — Minnmann 순수 SE cold-press 기공 앵커는 철회된 출처.
2. 머리 메타 "methods: dft" (L12) — 본문은 실험 + GeoDict 디지털 트윈 (type `FEM·digital-twin` L3) · DFT 서술 없음.
3. 재구성 ↔ 이론 부피분율 편차가 두 값: L203 "CB-wet <2.64 %p / CNT-dry 0.13 %p" ↔ L337 "Fig S16: CB-wet <1.29 %p / CNT-dry <0.36 %p" (CBD 도 L204 "8.58→9.79" ↔ L336 "8.58").
4. CNT-dry 기공 두 값이 조정 없이 공존: 토모 · 이론 pore 13.47 % (L204 · L336 · Fig S15) ↔ MIP ε 0.083 (L187 · Table S1) — 카드는 τ 의 방법 차만 표지하고 기공 차는 말하지 않음 (CB-wet 은 14.84 ↔ 0.14 로 가깝다).
5. 단결정 SC-NCA 비표면적 두 값: 서론 0.88 m²/g (L91 · L253) ↔ Fig 1d 'bare SC-NCA ~0.7' (L129 · 디지타이즈) — 조정 없음.
6. 우리 쪽 NCM σ_e 끝점 값이 카드 안에서 둘: "우리 σ_e 끝점가정 σ_S-single 10 > σ_P-poly 5" (L265 · L398) ↔ "우리 σ_e 끝점(σ_AM)의 reference … 우리는 NCM811 ~50 mS/cm = 5 S/m 기준" (L361 · L453).

**koo2026_swcnt_sheath_thick_electrode**
1. 철회된 출처를 앵커로: Minnmann(LPSCl cold-press) 를 σ/porosity 절대앵커로 (L41–42 · L446 · L607–608 · L1010).
2. 머리 메타 "methods: dft, elastic" (L15) — DFT 서술 없음 (elastic = VMS 는 맞음).
3. 중량 에너지밀도 두 값: 310 Wh/kg (L54 · L443) ↔ GED 315 / 315.2 Wh/kg (L332 · L341 · Table S10).
4. D_eff 식: §5 L263 "D_eff = D_int · ε/τ (Equation 1)" 가 표지 없이 남음 — §11.13-2 (L988) 정정은 §8 (L420) 만 가리킴 (본문 Eq 1 은 ε/τ²).
5. (방침상 · 읽기 함정) §11.13 정정 4 건의 원 줄 (L147 · L276–278 · L317 · L390 · L420) 이 그대로 남아 있음 — 원 줄만 읽으면 틀린 서술 (Fig S7 '단조 ↑' · BET 'pristine 과 유사' · S23/S24 배정 · ε/τ).
- 참고 (문제 아님): L716–717 의 sheath 두께 값에 "do not cite … (Koo)" 표지 — 출력에 숫자 옮기지 않음.

**lee2024_shear_force_dry_process_cathode_coverage**
1. 머리 한정어 번호 중복: L38 에 "③" 이 두 번 (③ 세 전극 교란 · ③ 용량 대조) 뒤 ④ ⑤.

**lee2025_corolling_dryprocess_lpscl_ptfe**
1. 철회된 출처를 근거로: §7 비교표 porosity 행 "DEM 15.6% / MPM 16.7% @300 (**Minnmann 10%**)" (L115) — 순수 SE 10 % @300 MPa 서술.
2. "Cronau 단결정 3.0" 라벨 (L85 · L132 · L152 'Cronau 3.0') — 프로젝트 원장 CL-91 (CLAUDE.md) 이 '단결정' 라벨을 철회 (3.0 = Cronau 2021 SI 의 펠릿값) · Minnmann 과 같은 부류의 철회 라벨.
3. 원제 (영문 제목) 가 카드에 없음 (L1 · L20) · 머리 메타 "elements: Li" (L7) 뿐.

**lee2025_dual_fibrous_ptfe_dry_electrode**
1. 철회된 출처를 근거로: §10.4 porosity 행 "**Minnmann pure-SE 10 %**" (L386).
2. 원제가 카드에 없음 (L1–3 · PDF 파일 이름만).
- 참고 (카드가 이미 표지한 원문 모순 · 카드 오류 아님): Fig S2(d) 꼬임 수 합 46 ≠ (c) rope 13 (L92–93) · Fig S3(b) CB 0.5 wt% 측정 ↔ (c) CB 1 wt% 'N/A' (L191–193) · Table S2 'This work / Graphite' 251 ↔ 291 · Table S1 250 ↔ 본문 251 (L213–214) · 활물질 로딩 50.48 ↔ Table S1 50.25 (L205).

**lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode**
1. PrL-ThA 계면 저항 표기 두 값: 0.021 (L37 · L92 · L214) ↔ 21.5 mΩ cm² (L259) — 비 2.14 (L92) 는 0.0215 기준 (사소).
- 참고 (카드가 이미 표지한 원문 모순): 표 S1 ThA 화성 뒤 합 170.0 ≠ 202.1 (L122 · L332) · LFP 그림 5a 곡선 끝 ↔ 본문 (L330) · NCM 'ICE 20 %' = 18.5 %p (L331) · F:O 논리 (L127 · L333) · S20 캡션 LFP ↔ 범례 NCM (L147) · Note S1 로딩 13.7 ↔ 표 S2 (L159) · FEM 식 (3) 발산 · 식 (5) 부호 누락 (L174) · CV 창 1.0 ↔ 1.5 V (L82).

합계: 카드 자체 문제 18 건 (koo2025 6 · koo2026 5 · lee2024 1 · lee2025_corolling 3 · lee2025_dual 2 · lee2026 1) · 그중 철회 출처 (Minnmann) 를 근거로 쓴 것 4 장 (koo2025 · koo2026 · lee2025_corolling · lee2025_dual).
