# batch_09 정독 근거 (카드 4 장 · 전문 읽음 · 2026-11-10)

읽은 카드 (전부 끝까지): `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` (522 줄) · `zunker2024_bulk_elastic_partII` (286) · `zunker2024_mdr_contact_model_partI` (402) · `zunker2025_dem_large_deformation_compaction` (555).

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (`stated` · `digitized` · `DERIVED` · `DERIVED-BY-US` · "원문 인용" · 추정 등) · 없으면 "표지 없음". "카드 풀이" = 카드가 논문 내용을 우리말로 풀어 적은 것 (원문 영어 문장은 카드에 없음 — 따옴표 인용은 원문 확인 뒤). "카드의 우리 쪽 기록" = 논문 값이 아니라 카드가 적은 우리 계산 · 코드 · 방침. "내 검토" = 이 정독에서 카드 안의 식 · 값을 서로 맞춰 본 것 (원문 미확인).

이 배치의 성격:
- Zunker 세 카드는 한 연작이다 (Part I 접촉 법칙 → Part II 벌크탄성 → 2025 편 다체 DEM + 입자별 FE + 실험) — 후보 C 의 원전. 재료는 "재료 무관 이론" (Part I · II) 과 Avicel PH102 (2025 편) 이고 LPSCl · NCM 값은 논문에 하나도 없다. 카드에 있는 LPSCl 숫자는 전부 카드의 우리 계산 (DERIVED-BY-US) 이다.
- 세 Zunker 카드는 그림 이미지를 못 보고 텍스트만 읽은 카드라고 스스로 적는다 (그림 판독 값 0 개 — Part I L54–56 · L237–238 / Part II L44 · L129 / 2025 편 L48–49 · L258).
- `xu2017` 은 DEM · MPM 논문이 아니라 AM (NMC532) 재료 값의 원전이다.
- 이름 주의: 2025 편 카드 §9-3 의 "경로 A" (LIGGGHTS 에 항복 캡 넣기) · "경로 A′" (Zunker 브랜치 직접 쓰기) 는 카드 자체의 이름이고 지시서의 후보 A · A′ (MPM) 와 다르다. 지시서 이름으로는 카드의 경로 A ≈ 후보 C′ · 경로 A′ ≈ 후보 C.

형식: `- [글자] slug | 내용 (값 · 단위) | 위치 | 표지 | 한계`

## a. 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선 · 진밀도 · 질량 기준 · 누른 채 / 뺀 뒤

**이 배치에 없음.** 아래는 "없다" 의 근거와, 섞어 쓰면 안 되는 이웃 값이다.

- [a] zunker2025_dem_large_deformation_compaction | 기공 · 상대밀도는 연작 세 편 어디에도 보고되지 않음 (검증 대상이 σ_axial(ε) · σ_radial(ε)) · 확실한 것은 die 부피비 0.6103 (높이 5.85 → 3.57 mm) 뿐 | §3-1 (L58–59 · L67) · §3-4 (L108–116) | stated (높이) · DERIVED (부피비) | Avicel PH102 (미결정 셀룰로오스) — SE 아님 · 카드의 최종 상대밀도 0.90–0.98 (기공 2–10 %) 은 "가정 기반 추정 — 논문 수치 아님, 인용 금지" (L113–115)
- [a] zunker2025_dem_large_deformation_compaction | 재료밀도 1560 kg/m³ (Avicel PH102) | §3-1 (L57) · Table 1 (L75) | stated | 황화물 아님 · 질량 기준 기공 환산은 카드에 없음
- [a] zunker2025_dem_large_deformation_compaction | 카드의 우리 쪽 제안 (논문 내용 아님): 순수 LPSCl 을 이 코드로 100 / 200 / 300 / 600 MPa die 압밀 · 결과 전 판정선 h0 "300 MPa 에서 porosity ≤ 12 %" · h1 "≥ 18 %" · 기공은 ΣV_o/V_box 로 직접 계산 · 1,000 입자 소형으로 먼저 | §12 ① (L393–409) | 표지 없음 (제안) | 판정선의 근거 값 ("Minnmann 10 % @300 MPa" · "Doux LPSCl 실측 floor 근처") 에 출처 위치 · 표지 없음 (카드 문제 16)
- [a] xu2017_nmc532_nanoindentation_modulus_hardness_toughness | 순수 SE 없음. 이웃 값: 상용 NMC532 전극 (NMC 94.2 : CB 3.0 : PVDF 2.8 wt% · 두께 45 ± 6 µm · 로딩 121 g/m²) 밀도 ≈ 2.7 g/cm³ → 기공 ≈ 35–38 % | §3-6 (L153–154) | stated (조성 · 두께 · 로딩) · DERIVED (가정 포함 — 진밀도 NMC 4.75 · CB 2.0 · PVDF 1.78 가정) | 액체계 전극 · SE 없음 · 압력 곡선 아님 · 압연 조건 없음
- [a] zunker2024_mdr_contact_model_partI · zunker2024_bulk_elastic_partII | 기공 · 상대밀도 값 없음 (접촉 한 개의 F · A_C · p̄ 와 입자 부피 V/V_o 만) | Part I §7-3 (L317–319) | — | —

## b. 압력을 뺄 때 되돌아오는 양과 잰 방법

수치가 있는 것은 Avicel 실험 한 건뿐 (LPSCl 아님). 나머지는 접촉 수준의 제하 처리와 그림 설명이다.

- [b] zunker2025_dem_large_deformation_compaction | 실험 (Avicel PH102 · die Ø8 mm): 최대 축변형 0.4 (높이 5.85 → 3.57 mm 로는 0.390) 뒤 제하 종료 변형 0.32 ⇒ 탄성 회복 0.08 (축변형) · 압축체 높이 대비 13.1 % · 해제 뒤 잔류 반경응력 15 MPa · 배출 축응력 실험 1.2 / 계산 1.5 MPa | §3-1 (L58–66) · Fig 9 (L270) | stated (0.32 · 15 MPa · 1.2 / 1.5 MPa) · DERIVED (0.390 · 13.1 %) | 연성 유기물 · 최대 240 MPa · 압축 + 해제 1 초 · 0.08 은 최대 변형을 0.4 로 둔 값 (카드 문제 12)
- [b] zunker2025_dem_large_deformation_compaction | 잰 방법: 압축 시험기의 상 · 하 펀치 축력 센서 + die 내면 반경압력 센서 2 개 (상 / 하) · 상 펀치를 사인파 변위로 축변형 0.4 까지 → 같은 사인파로 복귀 → 하 펀치 상승으로 배출 · 축응력 = 펀치 총 힘 / 펀치 면적 | §3-1 (L55–56) · §8 (L279–280) · §10 (L352–357) | stated | 계산 쪽 반경응력은 벽 반력이 아니라 입자 응력 텐서 평균 × 부피분율 — 실험 센서와 같은 양이 아님 (L281–284)
- [b] zunker2025_dem_large_deformation_compaction | 접촉 수준: 제하 때 쌍 사이 가상 강체 평면의 위치를 소성 변위로 선형 보간해 양쪽이 동시에 힘 0 에 닿게 함 (eq 1–2) · 반경비 [1, 0.75, 0.5, 0.25] 네 경우 모두 제하 곡선은 FEM 과 잘 맞음 | §4 (L133–135 · L149–151) · App C · Fig C.10 | stated (식 · 서술) | 같은 재료 쌍만 · 수치 없음
- [b] zunker2024_mdr_contact_model_partI | 접촉 수준: 제하 · 재하에 추가 처리 없음 — δ 만 줄이면 eq (30) 이 비선형 제하 곡선을 냄 · 누적 소성이 클수록 제하 곡선이 뻣뻣해지는 것까지 FEM 과 일치 (§8.1.1) · die 예고 (E/Y = 20 · ν = 0.3) 에서 2차 접촉은 제하 뒤에도 F 가 0 이 아님 (소성 반경 팽창은 비가역 · Fig 12) | §4-3 (L167–168) · Fig 12 행 (L253) | stated (서술) | 단일 입자 ↔ 강체 평판 · 되돌아온 양의 수치는 카드에 없음 (그림 판독 0 개)
- [b] zunker2024_mdr_contact_model_partI | 분리 (점착): 임계 신장 길이 Δl(a) = √(2πaΔγ/E*_c) (eq 11) · 분리 판정 계수 ξ = 3 (하중 제어) / 1 (변위 제어) (eq 15) · 뛰어 붙기 (jump-in) 는 무시 · 검증 δ_o,max/R_o = 0.5 까지 · 하중을 뺀 프로파일은 δ_o,max/R_o > 0.15 에서 접촉 중심 근처가 오목으로 바뀜 (FEM) — 모델은 볼록만 | §4-6 (L224–231) · §3 (L70–71) · Fig 13b | stated | 재료 무관 이론
- [b] zunker2024_mdr_contact_model_partI | 카드의 우리 쪽 대조: 우리 DEM 의 제하 = Walton–Braun 이력 (k₂ > k₁ 선형) ↔ 이 모델 = 비선형 제하 + 소성 누적에 따른 강성 증가 — "spring-back 정량이 필요하면 흡수 대상" | §7-2 (L301) | 표지 없음 (카드 판정) | 논문 값 아님
- [b] zunker2024_bulk_elastic_partII | die 구속: 제하 뒤 부피가 안 돌아옴 (2차 접촉 힘이 남아서) — 모델이 이 잔류까지 맞춤 (Fig 6) · 아무 정보도 넣지 않은 2차 접촉을 검출 · 진화시키고 제하 뒤에도 힘이 남음 (Fig 3c) | §5 (L135 · L138) | 표지 없음 (그림 설명 · 판독 0 개) | E/Y = 20 · ν = 0.3 단일 입자 · 수치 없음
- [b] zunker2024_bulk_elastic_partII | 함정: 제하 때 접촉 면적이 유한값 → 0 으로 급락 (die 1차 접촉 · Fig 4b) = 모델 인공물 (저자 설명: MDR · 벌크가 동시에 제하되어 MDR 쪽이 먼저 0) · ψ_b 를 키우면 (0.08 → 0.28 → 0.48) 제하 뒤 잔류 (소성 변위) 예측이 나빠짐 (App A · Fig A.7) | §5 (L136 · L139) · §7-3 (L211–212) · §10 (L269–270) | stated (서술) | 수치 없음
- [b] xu2017_nmc532_nanoindentation_modulus_hardness_toughness | 층 · 입자의 되돌아옴 값 없음 — 압입 제하 초기 기울기 S 로 환산 탄성률을 뽑는 Oliver–Pharr (식 2) · 하중 / 유지 / 제하 10 / 5 / 10 s | §4-2 (L204–209) · §0 (L26) | stated | NMC532 · 압입

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 세기 환산

LPSCl 의 측정 항복 · 경도 · 크리프 값은 **이 배치에 없음**. 경도 (접촉 평균압) ↔ 일축 항복의 환산은 Part I 카드에 있다 (배수가 변위에 따라 2.75 → 1.0).

- [c] zunker2024_mdr_contact_model_partI | 항복 = 일축 항복 세기 Y (탄성-완전소성 · 국부 von Mises). 접촉 평균압의 상한 (카드가 "경화곡선" 이라 부름): p̄/Y = 1.75·exp(−4.4 δ_o/R_o) + 1 (eq 16) → δ→0 에서 2.75 (실험 · 이론 인정 범위 2.61–2.84: Tabor 2000 · Ishlinsky 1944 · Lee 1972) · δ/R→1 에서 1.0 (접촉이 원기둥 단축압축으로 · Quicksall 2004 · Jackson & Green 2005) | §3 (L61–63) · §4-1 (L121) · §4-3 (L148) | stated | 재료 무관 · 상수 2 개는 E/Y = 200 FEM 곡선 한 번에 맞춘 것 · 가공 경화 없음 (완전소성)
- [c] zunker2024_mdr_contact_model_partI | 탄성 → 완전소성 전이: Hertz 평균압 p̄_H = (4E*_c/3π)·√(δ/R) 가 p_Y 에 닿을 때 (eq 40) · 항복 변위는 (4E*_c/3π)·√(δ_Y/R) = Y(1.75e^{−4.4δ_Y/R} + 1) 의 해 (eq 41) | §4-3 (L149–150) | stated (식) | —
- [c] zunker2024_mdr_contact_model_partI | 카드의 우리 계산 (LPSCl 가정 E 22.1 GPa · ν 0.37 · E*_c 12.80 GPa): Y 0.05 / 0.15 / 0.30 GPa → 항복 변위 δ_Y/R (구–평면) 0.064 / 0.56 / 2.06 % · (구–구 ×2) 0.13 / 1.12 / 4.12 % · 우리 겹침에서의 p_Y/Y = 2.26 (복합) / 2.08 (순수 SE) | §3-1 (L79–92) | DERIVED-BY-US ("논문 수치 아님") | 논문에 LPSCl 없음 · E*_c 정의 확인 필요 (카드 문제 4) — p_Y/Y 값은 E*_c 와 무관
- [c] zunker2024_bulk_elastic_partII | FEM 재료 E/Y = 20 · ν = 0.3 고정 · 단축압축에서는 p̄ → Y 로 수렴 | §3 (L54 · L58) | stated | —
- [c] zunker2025_dem_large_deformation_compaction | Avicel PH102 의 Y = 19 MPa — 문헌값이 없어 맞춘 값: "No reports in the literature on Avicel PH102 yield stress could be located, necessitating a fitting of Y" · E 5 GPa · ν 0.4 (문헌 범위) → E/Y 263 | §3-2 Table 1 (L73–75) · L80 · L85–86 | stated · 원문 인용 · DERIVED (E/Y) | 미결정 셀룰로오스 · 카드: "축 · 반경 응력 일치는 Y 를 맞춘 뒤의 일치" (L535)
- [c] zunker2025_dem_large_deformation_compaction | 크리프 · 속도 의존 없음: "Specific compaction speeds and loading sequence timings are omitted because of the rate-independent nature of the defined contact models" · Δγ 450 J/m² 는 K_Ic = √(2ΔγE*_c) 로 역산한 값 (카드 환산 K_Ic 1.64 MPa·m^½) | §3-2 (L76 · L81–84 · L90–92) | 원문 인용 · stated · DERIVED (1.64) | 카드 판정: 이 Δγ 는 열역학 표면 에너지가 아니라 소성 소산까지 묶은 유효 파괴 에너지
- [c] xu2017_nmc532_nanoindentation_modulus_hardness_toughness | AM 경도 — 정의 H = P_max/A(h_c) (식 1 · Oliver–Pharr · Berkovich · 1 mN · 접촉 깊이 ≈ 69 nm · 배치당 이차입자 15 개): NMC532 이차입자 pristine 8.6 ± 1.3 GPa · 소결 펠릿 12.6 ± 1.4 · 4.3 V 충전 7.1 ± 0.8 · 100 사이클 6.5 ± 0.9 GPa | §0 (L24 · L29–31) · Table 1 p. A3337 (L81) · §3-9 (L186) | stated (± 가 SD 인지 SE 인지 미기재 L25) · DERIVED (접촉 깊이) | NMC532 · sub-µm 국소값 · LPSCl 아님
- [c] xu2017_nmc532_nanoindentation_modulus_hardness_toughness | 일축 항복 환산: 논문에 없음. 카드의 우리 쪽 기록 — analyze_tabor_regime.py σ_y = H/3 = 2.0 GPa (H_AM 6.0 기준) · 우리 H_AM 6.0 은 pristine 8.6 대비 −2.0 SD 라 이 논문이 뒷받침 못 함 · 이상 기하에서 Vickers H_V ≈ 0.927 × 나노압입 H | §0 (L39) · §7 표 (L320) · §7-2 (L340–346) · 용어집 (L469) | 표지 없음 (우리 코드 값 · 카드 산술) | 논문 값 아님
- [c] xu2017_nmc532_nanoindentation_modulus_hardness_toughness | 하중 의존: < 2 mN 은 하중 무관 · > 2 mN 은 균열로 압입 E 가 내려감 (준정적 판독 3 mN ≈ 121 · 6 mN ≈ 102 · 10 mN ≈ 86 GPa) · > 10 mN 은 계면 균열 + sink-in 으로 Oliver–Pharr 부적합 | §3-5 (L141–142) · Fig 4c | stated (구간) · digitized (값) | 크리프 값 없음 (유지 5 s 만)
- [c] xu2017_nmc532_nanoindentation_modulus_hardness_toughness | 전극 기지 압입: CB + PVDF E 1.78 ± 0.35 · H 0.043 ± 0.01 GPa / 페놀수지 E 10.1 ± 0.8 · H 1.1 ± 0.2 GPa | §3-5 (L140) · Fig 4b | stated | 액체계 전극 기지
- [c] xu2017_nmc532_nanoindentation_modulus_hardness_toughness | 계면 파괴 인성 (cube-corner 방사 균열 · K_c = α(E/H)^½·P/c^{3/2} · α 0.036 · 균열 길이는 pop-in 으로 추정): 이차입자 0.102 ± 0.03 · 펠릿 0.309 ± 0.04 · 100 사이클 0.036 ± 0.018 MPa·m^½ | §0 (L33–35) · §4-3 (L211–220) · Table 1 (L82) | stated | 방법 조건부 (pop-in 길이 ±10 nm → K_c −30 / +59 % · 카드 산술 L290) · 15 압입 중 8–10 개만 사용 (L132)
- [c] 크리프 값 | 이 배치에 없음 | — | — | —

## d. 단단한 입자 + 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

단단한 입자의 **하중 몫을 논문이 수치로 준 카드는 없음** (Zunker 세 편은 단일 재료).

- [d] zunker2025_dem_large_deformation_compaction | 서로 다른 재료는 다루지 않음: "we focus on developing and testing a many-interacting particle methodology that properly handles varying radii, leaving the additional task of considering varying material properties as future work." | 머리 (L12–14) · 논문 §2.2 · §15 (L531–532) | 원문 인용 | —
- [d] zunker2025_dem_large_deformation_compaction | 같은 재료 · 다른 크기 쌍: 가상 강체 평면을 기하 교차점에 두면 겹침 분배가 δ_i,geo/δ ≈ R_j/(R_i+R_j) — 작은 입자가 겹침을 거의 다 가짐 (카드 계산: 12 : 1 이면 작은 쪽 92 % · 큰 쪽 8 %) · 카드 해석 "큰 쪽은 사실상 강체처럼 · 작은 쪽만 소성" | §4 (L128–146) · eq 3–4 | stated (식) · DERIVED (92 % / 8 %) | 재료가 같은 쌍의 기하 분배 — 하중 몫이 아님
- [d] zunker2025_dem_large_deformation_compaction | 반경비 0.25 에서 전방 재하 일치가 가장 나쁨 — 이유 (i) 기하 교차가 접촉 면적을 잘 못 나타냄 (ii) 작은 입자는 완전 항복인데 큰 입자는 거의 미항복이라 소성 누적 격차가 큼 | §4 (L149–152) · App C · Fig C.10 | stated (서술) | 검증 범위 반경비 0.25 까지
- [d] zunker2025_dem_large_deformation_compaction | 카드 계산 — 가짜 접촉 페널티가 강한 다분산에서 큰 입자끼리의 정당한 접촉을 지울 수 있음: R 6 µm 두 개 (중심 거리 11.9) + 홈에 낀 r 0.5 µm (6.4 × 2) → 작은 입자가 "중심" 으로 지정 · α = 136.8° → 가중 w = 0 (큰 입자끼리 접촉력 0) | §5-3 b (L207–221) | DERIVED ("논문의 오류 주장이 아니다" · 미검증 영역) | 논문 검증은 단분산 + 삼분산 (±20 %) 뿐
- [d] zunker2024_bulk_elastic_partII | 구속 (재밍에 해당하는 표현): 벌크탄성 발동 δ_o/R_o = 0.21 (삼축) · 0.49 (die 1차 접촉) · 단축은 발동 없음 — 같은 ψ_b 0.08 에서 구속의 정도가 발동 시점을 정함 | §3 (L51–53) · Fig 1 행 (L133) | stated | 단일 입자 · E/Y 20
- [d] zunker2024_bulk_elastic_partII | 1차 접촉이 만드는 원거리 인장응력이 2차 접촉 근처를 조기 항복시킴 (die · 0.2 < δ_o/R_o < 0.5 · Fig 5c) → 카드의 우리 쪽 추정: 하중을 받는 단단한 AM 골격이 주변 SE 를 조기 항복시킬 것 ("정량화 전 인용 금지") | §5 (L137) · §8 ⑤ (L240–242) | stated (저자 설명) · 추정 (우리 쪽) | 수치 없음
- [d] xu2017_nmc532_nanoindentation_modulus_hardness_toughness | 카드의 우리 쪽 기록: H_NMC 8.6 ↔ (우리) H_SE 0.85 GPa → 비 ≈ 10 = "AM 은 강체에 가깝고 SE 가 변형" 비대칭의 크기 근거 · 하중 분담 모듈의 "NCM811 압입 경도 문헌대 3–6 GPa" 는 출처 없음 · 역산 H_AM 3.83 GPa (real_14) 는 pristine 8.6 의 0.45× · 나노 경도는 입자 스케일 접촉압의 상한 쪽 양 | §7 표 (L321 · L327) · §9-3 (L418–423) | 표지 없음 (우리 코드 값 · 카드 판정) | 논문 값은 8.6 뿐 · 0.85 의 출처는 이 카드에 없음

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 · 대안마다 맞춘 값 개수

- [e] zunker2024_mdr_contact_model_partI | 깨지는 범위: 순수 기하 교차 면적 A_C = π(2δR − δ²) 는 δ_o/R_o > 0.3 에서 과소예측 (→ 겉보기 반경 R 성장 도입) · δ_o/R_o > 0.15 부터는 전부 완전소성 식이 지배 · E/Y 가 클수록 Hertz 가 맞는 δ 구간이 0 으로 줄어듦 (Fig 5b inset) · 선행 점착 접촉 연구의 검증은 전부 δ_o,max/R_o < 0.1 (Mesarovic & Johnson 2000 · Olsson & Larsson 2013 · Gonzalez 2019) | §3 (L69–70) · Fig 5 · 8 행 (L246 · L249) · 논문 §5.6.3 · §8.3.2 | stated | 단일 입자 ↔ 강체 평판
- [e] zunker2024_mdr_contact_model_partI | 대안 MDR 의 맞춘 값: 정규화 접촉압 곡선의 상수 2 개 (1.75 · 4.4) — E/Y = 200 FEM 곡선에 한 번 · 전 재료 공통 · 재료별 보정 0 (입력 R_o · E · ν · Y · Δγ) · FEM 스윕 E/Y 6.25–200 · ν 0–0.45 · δ_o/R_o ≤ 0.5 · 권장 하한 E/Y ≈ 10 · ν 는 힘 · 면적 · 평균압에 무시할 만한 영향 (App B.1) | §3 (L60–68) · Fig B.15 행 (L255) | stated | 같은 반경 · 같은 재료 · 가공 경화 없음
- [e] zunker2024_bulk_elastic_partII | 고밀도 (공극 소멸) 구간의 대안과 맞춘 값 (저자 정리를 카드가 표로): Harthong 2009 = 경험적 + Voronoï 셀 판정 (비용 큼 · 강소성 한정) / Frenning 2013 · 2015 = 경험 값 1 개 (삼축압밀 한 가지 하중만) / Garner 2018 = 전면 경험적 · 맞춤 함수 여럿 (재료마다 재보정 · 배위수 고정) / Giannis 2021a = 경험 스프링 상수 + 힘 부등식 (재보정 필요) / Zunker Part II = 물성 κ 하나 + 문턱 ψ_b 1 개 | §4-1 (L69–75) | 표지 없음 (카드 정리 표 · "저자 지적") | 선행 모델의 값은 카드에 없음
- [e] zunker2024_bulk_elastic_partII | 다접촉 보정 (Varkey 2026 의 F_mc · Giannis 계열) ↔ Zunker 벌크: F_mc = β·ν·a_ij·P_ij · 경험 상수 β = 0.5 (1 개) · 늘 켜져 있음 ↔ dF_Bulk = (A_con/V)·κ·dδ̄_o·A_C · 문턱 ψ_b (1 개) · A_free/A_tot < ψ_b 일 때만 켜짐 · 벌크 발동 δ_o/R_o 0.21 (삼축) / 0.49 (die) | §7-2 (L185–196) · §3 (L51–52) | 표지 없음 (카드 대조표) · stated (발동 시점) | Varkey 쪽 값은 다른 카드 소관 — 이 카드에서 확인 불가
- [e] zunker2024_bulk_elastic_partII · zunker2025_dem_large_deformation_compaction | ψ_b 는 값이 정해지지 않은 자유 값: Part II 0.08 ("No precise value of ψ_b exists, however ψ_b around 0.08 gives reasonable results") → 2025 편 0.5 ("tuned to trigger the high confinement bulk response stiffening in alignment with the experimental results") = 6.25 배 | Part II §3 (L49) · §7-3 (L210–215) · 2025 편 Table 1 (L77) · §15 (L533–534) | stated · 원문 인용 | E/Y 20 (Part II) · Avicel (2025 편)
- [e] zunker2025_dem_large_deformation_compaction | 다체 DEM 전체의 자유 값 6–8 개: Y (피팅) · ψ_b · µ_t 0.7 · µ_t,wall 0.1 · µ_roll 0.6 · t_p 50 · 겹침 캡 0.75 · (CoR) | §11 (L387) · §13-1 ② (L439) · §13-2 c (L472–480) | 표지 없음 (카드 집계) | 카드 판정: "무보정은 과장 — 정확히는 법선 접촉 물성을 왜곡하지 않는다"
- [e] zunker2025_dem_large_deformation_compaction | 큰 변형 전용 장치의 범위: 극단 겹침은 δ^max_geo/R > 0.75 이면 0.75R 로 자름 (App B) · 가짜 접촉 페널티가 걸리기 시작하는 겹침 (같은 크기 대칭 삼중항) δ/R > 0.299 · 절반 가중 0.586 · 사실상 소거 0.764 · 반경이 다른 쌍의 검증은 반경비 0.25 까지 | §4 (L136 · L149–152) · §5-3 a (L193–200) | stated (캡 · 반경비) · DERIVED (문턱 셋) | 문턱은 카드 기하 계산
- [e] EEPA · Thornton–Ning · Storåkers | 이 배치 카드에 값 없음 (Thornton–Ning 은 Part I 층위 표에 이름만 · L281) | — | — | —

## f. MPM 의 접촉 · 다물체 · 강체 결합 방법 · 해상도 규칙 (지름당 셀 수) · 수치 오차 추정

MPM 을 쓴 카드는 **이 배치에 없음** (지름당 셀 수 규칙 없음). 가까운 것만 적는다.

- [f] zunker2025_dem_large_deformation_compaction | 입자별 FE (MPFEM) 설정: 단분산 14 / 삼분산 12 입자 · C3D10M · Abaqus dynamic explicit · 감쇠 없음 · 강체 벽 6 면 등속 접근 · 법선 hard · 접선 마찰 µ 0.5 | §3-3 (L98–102) | stated | 요소 수 · 메시 수렴 · 오차 추정은 카드에 없음
- [f] zunker2024_mdr_contact_model_partI · zunker2024_bulk_elastic_partII | 단일 입자 FEM 메시: 7,653 CAX4R (축대칭 · 접촉 곡면 국부 세밀화 · 평판 = analytical rigid) / 48,167 C3D10 (삼축 · 단축) · 264,500 C3D10 (die) | Part I §3 (L74) · Part II §3 (L55) | stated | 수치 오차 추정 없음 — Part I 일치도는 "semi-quantitative" · 오차 지표 (RMSE 등) 미제시 (L379–380)
- [f] zunker2025_dem_large_deformation_compaction | DEM 시간 간격 규칙: Δt = 0.35·√(m/k) · m = ρ(4/3)πR_min³ · k = κ·R_min → 3×10⁻⁸ s (카드 검산 2.98×10⁻⁸ s) · 입자 관성 ≪ 평균 접촉력으로 준정적 확인 | §3-2 (L87–92) | stated · DERIVED (검산 일치) | DEM 규칙 (MPM 아님)
- [f] zunker2024_mdr_contact_model_partI | 카드의 우리 쪽 기록: "우리 MPM 은 J2 + σ_y 0.15–0.30 GPa 인데 E = 24 GPa 면 33–38 % porosity · E = 1.53 이어야 10 %" | §7-3 (L313–316) | 표지 없음 (우리 쪽 서술) | 차원 (2D / 3D) · 해상도는 이 카드에 없음

## g. 2D 결과를 3D 로 옮길 때의 경고나 증거

직접 경고는 **이 배치에 없음**.

- [g] zunker2025_dem_large_deformation_compaction | 한 줄뿐: "So 2021 이 rel.density 0.98 을 보였으나 LPS+Si, 600 MPa, 다른 캡, 2D" | §13-2 b (L467–468) | 표지 없음 | 어느 카드 (slug) 인지 적혀 있지 않음 · Part I 카드의 같은 문장 (L319) 에는 "2D" 가 없음 (카드 문제 14)
- [g] zunker2024_mdr_contact_model_partI · zunker2024_bulk_elastic_partII | Part I 의 FEM 은 2D 축대칭 요소로 3D 축대칭 접촉을 푼 것 (평면 2D 아님) · Part II 는 삼축 · die 구속을 3D (1/8 구 C3D10) 로 품 | Part I §3 (L74) · Part II §2 (L36) · §3 (L55) | stated | 2D ↔ 3D 비교 자체는 없음

## h. DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

DEM → FE · MPM 으로 넘겨 이어 계산한 선례는 **이 배치에 없음**.

- [h] zunker2025_dem_large_deformation_compaction | 반대 방향 — FE 배치를 DEM 으로 복제: MPFEM 셋업의 입자 좌표 · 반경을 정확히 복제해 LAMMPS 에 넣고 (압축 전 초기 배치) 같은 벽 운동으로 세 방향 응력을 대조 · XCT 수입은 세 논문 어디에도 없음 | §3-3 (L103–104) · §10 (L358–360) | stated | 14 / 12 입자 · 넘겨서 이어 계산한 것이 아니라 같은 출발 상태의 대조
- [h] zunker2025_dem_large_deformation_compaction | 형상 대조: DEM 상태 변수 (R · δ_max) 로 변형 형상을 재구성해 FEM 형상과 비교 — 삼축 단일 입자 (δ_o/R_o 0.15 · 하중 제거 뒤) · MPFEM 침대 안 한 입자 (최대 압축 시점 · 접촉 패치 5 개 모두 나타남) | §6 (L227–233) · Fig 7 | stated (정성 · "good agreement") | 비교일 뿐
- [h] xu2017_nmc532_nanoindentation_modulus_hardness_toughness | 실험 값 → DEM 입력 선례: Sangrós 2020 이 이 논문을 [32] 로 인용해 E_NMC 142.5 → 111.6 을 DEM 입력으로 씀 | §7-1 (L335–337) · §13 (L502) | 표지 없음 (다른 카드 기록) | 이 카드에서 확인 불가

## i. 복합 양극 (AM + SE) 의 압력별 기공

**이 배치에 없음** (Zunker 2025 편은 단일 재료 · `xu2017` 은 SE 없는 액체계 전극의 밀도 추정뿐 — a 항).

## j. 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것

- [j] zunker2025_dem_large_deformation_compaction | 서로 다른 재료 미지원 ("varying material properties as future work") → AM + SE 복합 불가 · 순수 SE (단일 재료) 만 가능 | L12–16 · §15 (L531–532) | 원문 인용 · 카드 판정 | —
- [j] zunker2025_dem_large_deformation_compaction | 기공 · 상대밀도 보고 0 · 압력 스윕 없음 (프로토콜 하나 0 → 0.4 → 0) · 20,000 입자 계산 시간 미보고 ("1 초" 는 14 입자 대조의 값) · 반경비 검증 0.25 까지 · 가짜 접촉 페널티는 강한 다분산에서 미검증 · 파쇄 · 온도 · 소결 · 사이클 없음 | §15 (L538–550) | 표지 없음 (카드 한계 목록) | —
- [j] zunker2025_dem_large_deformation_compaction | 응력 정의가 절마다 다름 — MPFEM 대조는 벽 반력 / 면적 · 정제 계산의 반경응력은 입자 응력 텐서 평균 × 부피분율 (실험의 벽 센서와 같은 양 아님) | §8 (L279–284) · §15 (L542–543) | 표지 없음 (카드 지적) | —
- [j] zunker2025_dem_large_deformation_compaction | 페널티 세기 t_p = 50: "a fitted penalty transition intensity" · "no unique value of t_p exists" | §5-2 (L182–183) | 원문 인용 | —
- [j] zunker2024_mdr_contact_model_partI | 저자가 미해결 · 미포함으로 적은 것: 반경 차 ("subject of active research" · §1 item 9) · 가공 경화 (item 10) · 접촉 가장자리 환형의 압력 불균일 (힘에는 작지만 점착 예측에는 큼 · 향후 과제) · 하중 뺀 프로파일이 오목–볼록인데 모델은 볼록만 (§8.3.2) · 점착 유효 조건 (eq 49) 은 사전 판정이 어려움 · E/Y ≲ 10 사용 불가 · 일치도 "semi-quantitative" | §10 (L374–386) · §4-4 (L175–182) | stated (카드가 "저자 명시 · 인정" 이라 적음) | —
- [j] zunker2024_mdr_contact_model_partI | 고구속에서 구관들이 심하게 교차하면 반경 성장 식 (eq 37) 이 음수 / 비정상 ΔR (App C 말미) → Part II 가 R 성장을 정지 | §4-4 (L182) · §4-5 (L218–220) | stated | —
- [j] zunker2024_bulk_elastic_partII | ψ_b 값 없음 · 원거리 응력 결합 미고려 (Fig 5c 불일치의 원인으로 저자 명시 · 향후 과제) · 제하 때 면적 급락 = 모델 인공물 (저자 인정) · 벌크 전단 응답 (μ 기반) 은 향후 과제 · 다체 계산 0 건 · E/Y 20 · ν 0.3 한 조합 | §10 (L261–273) | 표지 없음 (카드 한계 목록 · "저자 인정" 표기) | —
- [j] xu2017_nmc532_nanoindentation_modulus_hardness_toughness | 가압과 닿는 것: 측정은 sub-µm 국소값이라 이차입자 전체의 압축 응답은 "이 논문 밖" · 단결정 값 없음 · 전극의 압연 이력 정보 없음 | §4-6 (L241–244) · §10-2 (L446–450) | 표지 없음 (카드가 추가한 한계) | 저자가 밝힌 한계 (§10-1) 는 입계 나노기공 · 결정립 크기 의존 등

## k. DEM 의 한계 — 논문이 직접 말한 문장 · 수치 (인용 서지 병기)

서지: [Z25] = Zunker · Dunatunga · Thakur · Tang · Kamrin · 2025 · Powder Technology (카드는 프리프린트 판 — 권호 · 쪽 · DOI 카드에 없음 · 인용 전 출판판 확인) / [ZK-I] = Zunker · Kamrin · 2024 · J. Mech. Phys. Solids 183, 105492 · DOI 10.1016/j.jmps.2023.105492 / [ZK-II] = Zunker · Kamrin · 2024 · J. Mech. Phys. Solids 183, 105493 · DOI 10.1016/j.jmps.2023.105493 / [Xu17] = Xu · Sun · de Vasconcelos · Zhao · 2017 · J. Electrochem. Soc. 164 (13) A3333–A3341 · DOI 10.1149/2.1751713jes.

- [k] zunker2025_dem_large_deformation_compaction ([Z25]) | 겹침으로 접촉을 판정하는 DEM 은 큰 변형에서 사이에 낀 입자를 "관통한" 가짜 접촉에 힘을 계산함. 원문: "Should particle i be able to contact j given the presence of k?" · 카드 풀이: 작은 변형에서는 겹침이 반경보다 훨씬 작아 접촉끼리 간섭하지 않지만 큰 변형에서는 i, j 가 k 를 관통해 겹침 | 논문 §3 · Fig 3 (카드 §5-1 L158–167) | 원문 인용 (질문 문장) · 나머지는 카드 풀이 | Avicel · 발동 겹침 문턱 δ/R > 0.299 는 카드 계산 (DERIVED · L196–200)
- [k] zunker2025_dem_large_deformation_compaction ([Z25]) | 입자 모양: 통상의 탄소성 DEM 은 입자 변형을 알 수 없음. 원문: "aids in resolving a common deficit of elastic-plastic DEM whereby the deformation of a particle is not accessible." | 논문 §5 (카드 §6 L234–235) | 원문 인용 | 이 논문의 재구성도 자유 형상은 아님 — 입자당 스칼라 R 하나 + 접촉 평면 · 이방 배럴링 · 오목 프로파일 · 내부 변형장 불가 (카드 판정 L246–247)
- [k] zunker2025_dem_large_deformation_compaction ([Z25]) | 서로 다른 재료 미지원: "we focus on developing and testing a many-interacting particle methodology that properly handles varying radii, leaving the additional task of considering varying material properties as future work." | 논문 §2.2 (카드 L12–14) | 원문 인용 | —
- [k] zunker2025_dem_large_deformation_compaction ([Z25]) | 맞춘 값이 물성이 아님을 저자가 적은 문장: Y — "No reports in the literature on Avicel PH102 yield stress could be located, necessitating a fitting of Y" / ψ_b — "tuned to trigger the high confinement bulk response stiffening in alignment with the experimental results" / t_p — "a fitted penalty transition intensity" · "no unique value of t_p exists" | Table 1 · 논문 §7.1 (카드 L85–86 · L533–534 · L182–183) | 원문 인용 | µ_t · µ_t,wall · µ_roll 도 튜닝 — 각각 고밀도 응력 · 배출력 · 초기 패킹에 (카드 L536–537)
- [k] zunker2025_dem_large_deformation_compaction ([Z25]) | 겹침 상한 · 크기 비 한계: 극단 겹침은 δ^max_geo/R > 0.75 에서 잘라 냄 (App B) · 반경비 0.25 에서 전방 재하 일치가 가장 나쁨 (App C) | 카드 §4 (L136 · L149–152) | stated | 검증 범위 반경비 1–0.25
- [k] zunker2025_dem_large_deformation_compaction ([Z25]) | 입자별 FE 가 주고 이 DEM 이 못 주는 것: 내부 응력 · 변형장 · 자유 형상 · 임의 형상 · 다재료 접촉 · 파쇄 — 대가는 14 입자에서 5.5 시간 (10 프로세서) ↔ ≈ 1 초 (직렬) | 카드 §13-1 ⑦ (L444) · §3-3 (L105) | 표지 없음 (카드 판정) · stated (비용) | 원문 문장은 카드에 없음
- [k] zunker2024_mdr_contact_model_partI ([ZK-I]) | 구 교차 기하의 한계: 순수 기하 교차 면적 π(2δR − δ²) 는 δ_o/R_o > 0.3 에서 접촉 면적을 과소예측 · 선행 점착 접촉 모델의 검증은 전부 δ_o,max/R_o < 0.1 | 논문 §5.6.3 · §8.3.2 (카드 L69–70) | stated | 단일 입자
- [k] zunker2024_mdr_contact_model_partI ([ZK-I]) | 모양: 모델 형상은 "겉보기 반경 R 의 구 − 접촉마다 잘린 구관" 족에 갇힘 — 늘 볼록인데 실제 (FEM) 는 δ_o,max/R_o > 0.15 에서 오목–볼록 혼합 · 이방 배럴링 · 비축대칭 유동 · 파쇄 불가 | 논문 §8.3.2 · Fig 13b · App C eq C.1 (카드 L178–181) | stated (오목–볼록) · 카드 판정 (불가 목록) | —
- [k] zunker2024_mdr_contact_model_partI ([ZK-I]) | 조밀 영역: 구관들이 서로 심하게 교차하면 반경 갱신 식 (eq 37) 이 음수 / 비정상 ΔR 을 냄 | 논문 App C 말미 (카드 L182 · L218–220) | stated | 카드 판정: "고밀도로 가면 잘린-구 부기 자체가 무효 — 이 계열 전체의 공통 한계"
- [k] zunker2024_mdr_contact_model_partI ([ZK-I]) | 정확도 · 범위의 고백: 일치도 "semi-quantitative" (§8.1.1) · 정량 오차 지표 없음 · 반경 차 "subject of active research" (§1 item 9) · 가공 경화 미포함 (item 10) · E/Y ≲ 10 은 탄성 변형률이 선형탄성 통상 범위 (3–5 %) 초과 | 카드 §10 (L376–385) · §3 (L67) | stated (따옴표 표현은 카드가 옮긴 것) | —
- [k] zunker2024_mdr_contact_model_partI ([ZK-I]) | 항복 캡 없는 탄성 접촉에 대한 문장 — 카드가 쓴 영어 요약 (논문 원문 아님): "Because the contact force in the fully-plastic regime is the product of a yield-capped mean pressure and a geometric contact area, it is independent of Young's modulus — a structural reason why an elastic, yield-uncapped contact law must soften E to reach experimental densities." | 카드 §9 (L363–365) · 근거 §7-2 (L298) | 표지 없음 (카드 작성 문장) | 앞 절 (완전소성에서 F ≈ p_Y·A_geo) 은 논문 식 · 뒤 절 ("must soften E") 은 카드 해석 — 같은 카드 §7-3 에 반례 셋 · 원문 확인 뒤에만 인용
- [k] zunker2024_mdr_contact_model_partI ([ZK-I]) | 카드의 우리 계산: 우리 DEM 의 SE–SE 겹침 δ/R 14.8 % (복합) · 22 % (순수 SE) 는 LPSCl 항복 겹침의 3.6–169 배 (Y 0.15 GPa 에서 13 배) | §3-1 (L89–90 · L98–102) | DERIVED-BY-US | 논문 값 아님 · E*_c 정의 확인 필요 (카드 문제 4)
- [k] zunker2024_bulk_elastic_partII ([ZK-II]) | 공극이 사라질 때의 급격한 강성 상승을 접촉 법칙이 못 냄 — 선행 처리의 한계 (저자 지적): Harthong 2009 의 Voronoï 셀 = 비용이 커 대규모 불가 + 강소성 한정 / Frenning = 삼축 한 가지 하중만 / Garner 2018 = 전면 경험적 · 재료마다 재보정 · 배위수 고정 / Giannis 2021a = 재보정 필요 | 논문 §1 (카드 §4-1 L67–75) | 표지 없음 (카드 정리 · "저자 지적") | 원문 문장은 카드에 없음
- [k] zunker2024_bulk_elastic_partII ([ZK-II]) | 문턱 값이 물성이 아님: "No precise value of ψ_b exists, however ψ_b around 0.08 gives reasonable results" | 논문 §4.1 (카드 L49 · L210) | 원문 인용 | E/Y 20 한 조합
- [k] zunker2024_bulk_elastic_partII ([ZK-II]) | 접촉 독립 가정이 깨지는 곳: 1차 접촉이 만드는 원거리 인장응력이 2차 접촉 근처의 Mises 응력을 올려 조기 항복 — die 2차 접촉 0.2 < δ_o/R_o < 0.5 에서 FEM 평균압은 떨어지는데 모델은 못 따라감 (저자가 원인 명시 · 향후 과제) · 구속이 강하면 δ_o/R_o 0.21 (삼축) 부터 벌크 구간 | 논문 Fig 5c · §5.1 (카드 L137 · L266–268 · L51) | stated (서술 · 발동 시점) | 평균압 차이의 수치는 카드에 없음
- [k] zunker2024_bulk_elastic_partII ([ZK-II]) | 제하 때 접촉 면적이 유한값 → 0 으로 급락하는 모델 인공물 (저자 인정) | 논문 Fig 4b (카드 L136 · L269–270) | stated (서술) | —
- [k] xu2017_nmc532_nanoindentation_modulus_hardness_toughness ([Xu17]) | DEM 을 쓰지 않은 실험 논문 — DEM 한계에 대한 말 없음. 닿는 원문: "The size of the nanoindentation impression is around hundreds of nanometers which is comparable with the size of NMC primary particles. The mechanical response of NMC is largely influenced by the "grain boundaries"." → 카드 판정: 입자 하나 = 이차입자 하나인 구는 그 안 (1차입자 + 약한 계면) 을 점 하나로 봄 | 논문 p. A3337 (카드 §4-6 L239–244 · §7 표 L325) | 원문 인용 · 카드 판정 | NMC532

## l. 소성변형이 왜 어려운가 — 논문의 설명 · 택한 우회 · 그 값 (인용 서지 병기)

- [l] zunker2024_mdr_contact_model_partI ([ZK-I]) | 왜 어려운가: 탄소성 접촉에서는 소성이 압자의 무하중 형상을 계속 바꾼다 — 초기 갭 함수 g_3D(r) 를 모르니 문제를 못 품. 우회 = 순서를 뒤집음: ① 완전소성 구간의 압력 분포는 (거의) 균일 → 스칼라 p̄ 하나 ② 접촉 면적 진화는 해석식 ③ (p, a) 로 매 순간의 무하중 압자 형상을 역산 ④ 제하 = 압자를 빼는 것 · 점착 = 스프링이 붙는 것 — "탄소성 = 탄성 접촉의 연속열" | 논문 §5.1 (카드 §4-2 L123–133) | 표지 없음 (카드 풀이) | 원문 문장은 카드에 없음
- [l] zunker2024_mdr_contact_model_partI ([ZK-I]) | 부피 보존 유동 · 이웃 영향 · 이력의 처리: "소성은 비압축 ⇒ 모든 부피 변화는 탄성" — ΔV = −ΔV_e (eq C.5) 를 잘린-구 부피 식에 넣어 겉보기 반경 증분 ΔR 을 품 (eq 37) → 기존 접촉의 힘 증가 + 상대 변위 0 인 2차 접촉 생성 · 하중 이력은 접촉당 δ_max 로 기억 | 논문 App C (카드 §4-5 L189–205 · §4-3 L158–161 · §4-4 L179) | stated (식) | 고구속에서 ΔR 비정상 (L182)
- [l] zunker2024_mdr_contact_model_partI ([ZK-I]) | 우회의 값: 맞춘 값 2 개 (1.75 · 4.4 — E/Y = 200 FEM 한 번 · 전 재료 공통) · 검증 = 단일 구 ↔ 강체 평판 FEM (7,653 CAX4R · E/Y 200 / 100 / 50 / 25 / 12.5 / 6.25 · ν 0–0.45 · δ_o/R_o ≤ 0.5) + die 예고 1 건 · 다체 계산 0 건 · 비용 = 닫힌 해석식 (수치적분 없음) · 빠진 것 = 가공 경화 · 마찰 · 파쇄 · 반경 차 | 카드 §3 (L60–75) · §4-3 (L165–168) · §10 (L374–386) | stated | 재료 무관
- [l] zunker2024_bulk_elastic_partII ([ZK-II]) | 왜 어려운가: 공극이 사라지면 힘–변위가 급격히 뻣뻣해짐 (입자가 "고전적 무한소 연속체 요소" 로 환원 · 최종 형상 삼축 = 큐브 · die = 직육면체) — 기존 처리는 경험적이거나 비쌈. 우회 = 변위 증분을 면적 가중 평균 표면 변위 (벌크 몫) 와 그 편차 (MDR 몫) 로 쪼개고 선형탄성 tr(ε̄) = tr(σ̄)/3κ 에서 벌크 힘을 유도 — 물성 κ 하나 + 문턱 ψ_b 1 개 (값 비유일). 겹쳐 더할 수 있는 이유: 벌크 응답은 정수압 응력만 건드리고 항복을 지배하는 편차 응력은 안 건드림 | 논문 §1 · §3.2.1 · §4 (카드 L19–24 · L56–57 · L80–99) | stated (식) · 카드 풀이 | —
- [l] zunker2024_bulk_elastic_partII ([ZK-II]) | 값 · 비용: 검증 = 단일 입자 FEM 네 접촉 (삼축 · die 1차 · die 2차 · 단축 · E/Y 20 · ν 0.3 · 48,167 / 264,500 C3D10) · 다체 0 건 · 구현은 한 시간 간격에 "입자 집계 → 접촉 루프 → 입자 집계" 3 패스 (일반 DEM 의 쌍별 한 패스와 다름) · 벌크 구간에서는 R 성장 정지 · 삼축에서는 소성 누적도 멈춤 | 카드 §3 (L54–61) · §6 (L149–162) | stated | —
- [l] zunker2025_dem_large_deformation_compaction ([Z25]) | 다체로 갈 때의 어려움과 우회: (i) 반경이 다른 쌍 → 쌍 사이에 가상 강체 평면을 두고 양쪽에서 따로 힘을 계산해 평균 (쌍마다 힘 2 번 · 평면 양쪽의 접촉량이 불일치할 수 있음 — 저자 명시) (ii) 가짜 접촉 → 삼중항 각도의 시그모이드 페널티 (t_p 50) (iii) 3 패스 구조 + 삼중항 루프 (이웃의 이웃 순회) | 논문 §2.2 · §3 (카드 §4 L120–152 · §5-2 L169–189 · §9-1 L306–308) | stated | 같은 재료만
- [l] zunker2025_dem_large_deformation_compaction ([Z25]) | 값: 맞춘 값 Y 19 MPa (문헌 부재) · ψ_b 0.5 · µ_t 0.7 · µ_t,wall 0.1 · µ_roll 0.6 · t_p 50 — 카드 지적 "관측량마다 대응 노브" (고밀도 응력 / 배출력 / 초기 패킹) · 검증 = MPFEM (14 / 12 입자 · 세 방향 응력 · 단분산 최대 변위에서 σ_zz 만 약간 과대) + Avicel 실험 (축 · 반경 응력–변형 · 잔류 반경응력 · 배출력) · 기공 검증 없음 · 비용 = N 20,000 · Δt 3×10⁻⁸ s · 총 스텝 수 · 벽시계 미보고 · 14 입자에서 MPFEM 5.5 시간 (10 프로세서) ↔ DEM ≈ 1 초 (직렬) | 카드 §3-2 (L69–92) · §3-3 (L94–106) · §15 (L533–550) | stated · 표지 없음 (카드 지적) | 미결정 셀룰로오스 · 압력 스윕 없음
- [l] zunker2025_dem_large_deformation_compaction ([Z25]) | 카드의 우리 쪽 판정 (논문 내용 아님): 무르게 맞춘 영률의 "설명은 반쯤 무너지고 결론은 아직 안 무너짐" — 반례 셋 = 우리 MPM 은 항복 캡이 있어도 연화가 필요했음 · Zunker 세 편에 기공 검증이 없음 · 재료가 다름 (미결정 셀룰로오스는 파쇄 없음) | 카드 §13-2 (L448–484) | 표지 없음 (카드 판정) | 인용할 논문 문장 아님
- [l] xu2017_nmc532_nanoindentation_modulus_hardness_toughness ([Xu17]) | 소성 계산 논의 없음 (실험). 닿는 관찰: 2 mN 위에서는 균열이 섞여 압입 E 가 내려가고 (10 mN ≈ 86 GPa) > 10 mN 은 계면 균열 + sink-in 으로 표준 해석이 부적합 — 이차입자에서는 입계 균열이 낮은 하중에서 먼저 나타남 (균열 개시 ≈ 2 mN ↔ 펠릿 > 10 mN) | 카드 §3-5 (L141–142) · §3-4 (L131) · Fig 4c | stated · digitized (86 GPa) | NMC532

## m. 받아들일 통찰 (바로 가져다 쓸 방법 · 규칙 · 검증 시험 · 관측량 · 함정 · 보고 방식)

형식: `- [m] slug (서지) | 무엇을 | 우리 쪽 어디에 | 왜 (근거 위치 · 표지) | 한계`

- [m] zunker2024_mdr_contact_model_partI ([ZK-I]) | 검증 시험 — 입자 하나 압축의 기준 해와 좌표: 탄성-완전소성 구 ↔ 강체 평판 · 무마찰 · δ_o/R_o ≤ 0.5 · E/Y 6.25–200 의 F/(E R_o²) · A_C/(πR_o²) · p̄/Y · V/V_o 대 δ_o/R_o 곡선 + 두 극한 검사 (p̄/Y → 2.75 at δ→0 · → 1.0 at δ/R→1) | U1 | FEM 과 모델을 이 네 축으로 대조 (Fig 8–11 · L249–252) · 카드 "이 정규화로 그리면 문헌과 바로 겹쳐 그릴 수 있다" (§6 L266–267) · 극한 값 (L62–63 · stated) | 곡선 값은 카드에 없음 (그림 판독 0 개) — 원문 그림에서 읽어야 함
- [m] zunker2024_mdr_contact_model_partI ([ZK-I]) | 규칙 — 구–구 ↔ 구–강체 평판 환산: 같은 구 쌍의 대칭면 = 강체 평면 → δ(구–평면) = δ(구–구)/2 · 반경이 다르면 δ_i,geo/δ ≈ R_j/(R_i+R_j) 로 쪼갬 | U1; U5; 단계 3 | 논문 §4.2 의 미러링 (Fig 4 행 L245 · 카드 L81–82) · 2025 편 eq 3–4 가 같은 반경에서 δ/2 를 줌 (L128–143 · L494–496) | 탄성률 쪽 환산 (E*_c 를 어느 정의로 넣는가) 은 카드에서 불확실 (카드 문제 4)
- [m] zunker2024_mdr_contact_model_partI ([ZK-I]) | 관측량 정의 — 고체 부피 부기: 소성은 등적이라 부피 변화는 탄성분뿐 (ΔV = −ΔV_e) · 입자 부피 V = V_o(1 + tr ε̄) (입자 응력 Σf⊗b 로) → "초기 구 부피 합" 이 보존량이고 차이는 탄성 부피 변형 (카드 계산: 300 MPa / κ ≈ 26 GPa → ≈ 1.2 %) · 같이 적을 유효 범위: 구관이 심하게 교차하는 고밀도에서는 이 부기가 무효 | 단계 0 | eq 38–39 · C.5 (카드 §4-5 L189–220 · stated 식 · DERIVED 1.2 %) | 탄성 몫 1.2 % 는 카드 계산 · LPSCl 값 아님
- [m] zunker2024_mdr_contact_model_partI ([ZK-I]) | 함정 — 접촉 평균압 ↔ 항복의 배수는 상수 (3 근처) 가 아니라 2.75 → 1.0 으로 변위에 따라 줄어듦: 경도 / 3 같은 고정 환산으로 항복 세기를 견주거나 소성 접촉 면적 (F/H) 을 계산하면 큰 겹침에서 어긋남 (카드 계산: 우리 겹침에서 2.08–2.26 Y → 면적 24–44 % 과소) | 단계 4; 단계 7 | eq 16 (L61–63 · stated) · §3-1 (L91–92 · DERIVED-BY-US) · §8 ① (L332–338) | 우리 코드가 쓰는 H 값은 카드도 "선행 확인" 으로 남김 (L335–336) · 완전소성 가정
- [m] zunker2024_bulk_elastic_partII ([ZK-II]) | 관측량 — 구속비 A_free/A_tot (입자 표면 가운데 어떤 접촉에도 안 쓰인 몫): A_C,i = π(2δ_iR − δ_i²) + c_A,i · A_tot = 4πR² − 2πΣ(δ_max,MDR,i + δ_o,Bulk,i)R + A_con · A_free = A_tot − A_con — 덤프만으로 계산 | 후보 D0; 단계 0 | eq 30–33 (L103–109 · stated) · 카드 "DEM 재실행 불필요" (§8 ① L225–230) · 공극이 사라지는 구간에 들어갔는지의 판정 값 (ψ_b 0.08 기준 발동 δ_o/R_o 0.21 / 0.49) | 문턱 값 자체가 자유 값 (0.08 ↔ 0.5) · §8 ① 간략식은 δ 정의가 eq 32 와 다르게 적힘 (카드 문제 10)
- [m] zunker2024_bulk_elastic_partII ([ZK-II]) | 검증 시험 — 입자 하나 시험을 구속 세 가지 (삼축 · die · 단축) 로: 단축만 하면 벌크 구간이 안 나타남 · 같은 재료 (E/Y 20 · ν 0.3) 에서 발동 δ_o/R_o 0.21 / 0.49 / 없음 · 최종 형상 큐브 / 직육면체 / 원기둥 유사 · 벌크 구간에서 면적 성장 정체 | U1; U6; 결과 전 대조 항목 | §3 (L51–58 · stated) · Fig 1–2 행 (L133–134) | E/Y 20 한 조합 · 곡선 값은 원문 그림
- [m] zunker2024_bulk_elastic_partII ([ZK-II]) | 판별 시험 — die 구속에서 (a) 프로그램하지 않은 2차 접촉이 반경 팽창만으로 생기고 제하 뒤에도 힘이 남으며 부피가 안 돌아오는지 (b) 0.2 < δ_o/R_o < 0.5 에서 2차 접촉 평균압이 내려가는지 (원거리 응력 결합 — 접촉 독립 모델은 못 냄) 를 연속체 계산이 내는지 봄 | U1; 단계 6; 조건 R4; 후보 A′-0 | Fig 3c · 5c · 6 행 (L135 · L137–138 · stated 서술) · 저자가 원인을 원거리 인장응력으로 규명 (L137) | 수치는 카드에 없음
- [m] zunker2024_bulk_elastic_partII ([ZK-II]) | 함정 — 이 계열 모델은 제하 구간에서 접촉 면적이 유한값 → 0 으로 뛰는 인공물이 있음: 탈압 뒤의 면적 기반 수송량을 구 기반 큰 변형 모델에서 뽑지 않음 | 단계 6; 단계 7; 후보 C | Fig 4b 행 (L136) · §10 (L269–270 · 저자 인정) | —
- [m] zunker2025_dem_large_deformation_compaction ([Z25]) | 검증 시험 — 작은 조밀 충전 대조의 꼴: 단분산 14 / 삼분산 12 입자 (±20 % 반경) · 강체 벽 6 면 등속 접근 · 같은 좌표 · 반경을 두 방법에 복제 · 관측량 = 세 방향 응력 σ_xx · σ_yy · σ_zz 대 Δ/W · 기준 해 (입자별 FE) 비용 5.5 시간 (10 프로세서) | U6; U5; 단계 3; 후보 B | §3-3 (L94–106 · stated) · Fig 5–6 행 (L266–267) · 카드 "같은 대조를 짜려면 이 규모면 된다" (L266) | 같은 재료 (E/Y 20) · Δ/W 범위는 그림에만
- [m] zunker2025_dem_large_deformation_compaction ([Z25]) | 관측량 · 함정 — 탈압 관측량 묶음: 누르는 중 축 · 측방 응력 + 제하 종료 변형 + 해제 뒤 잔류 측방 응력 + 배출 응력 · 응력을 절마다 다른 정의 (벽 반력 / 면적 ↔ 입자 응력 평균 × 부피분율) 로 내면 같은 표에 못 넣음 → 정의를 결과 전에 하나로 고정 | 단계 6; 조건 R4; 단계 0; 결과 전 대조 항목 | §3-1 (L61–66 · stated) · §8 (L279–284) · §12 ⑥ (L425–428) | 값 (15 MPa 등) 은 Avicel — 목록만 가져옴 · 측방이 주기 경계면 벽 반력이 없음 (L428)
- [m] zunker2025_dem_large_deformation_compaction ([Z25]) | 규칙 · 함정 — 구 기반 계산의 겹침 한계를 숫자로: 같은 크기 삼중항에서 관통 (가짜) 접촉은 δ/R > 0.30 부터 · 우리 겹침 0.148 / 0.22 는 그 아래 (카드 계산) · 반대로 크기 비가 큰 침대에서는 거리 기반 "중심" 판정이 홈에 낀 작은 입자 때문에 큰 입자끼리의 접촉을 지움 (카드 예: w = 0) | 후보 D0; 후보 C; 단계 5 | §5-3 (L191–221 · DERIVED) · 논문 검증은 단분산 + ±20 % 삼분산뿐 (L218–219) | 문턱은 대칭 삼중항 가정의 카드 계산 · 논문 수치 아님
- [m] zunker2025_dem_large_deformation_compaction ([Z25]) | 보고 방식 — 맞춘 값과 관측량의 회계: 이 논문은 Y · ψ_b · µ_t · µ_t,wall · µ_roll 을 각각 다른 관측량 (축 응력 곡선 · 고구속 강성 상승 · 고밀도 응력 · 배출력 · 초기 패킹) 에 맞춤 — 1 : 1 이면 예측 주장이 약해짐 → 우리 표는 "맞춘 관측량" 과 "견주기만 한 관측량" 을 나눠 적음 | 조건 R5; 단계 4 | §15 (L533–537) · §13-2 c (L472–480) · Table 1 (L73–78 · stated) | 카드 지적 (논문 스스로의 말은 Y · ψ_b · t_p 의 맞춤 사실뿐)
- [m] xu2017_nmc532_nanoindentation_modulus_hardness_toughness ([Xu17]) | 보고 방식 — 재료 입력에 "측정 부류" 를 같이 적음: 같은 분말 · 같은 장비에서 이차입자 국소 142.5 : 치밀 펠릿 177.5 : 제일원리 190 GPa = 1 : 1.25 : 1.33 | 단계 5; 후보 D0 | Table 1 (L78–84 · stated · 비는 DERIVED) · §7-1 (L329–334): 우리 140 GPa 는 응집체 부류와 정합 — "정합이지 출처가 아니다" (L318) | NMC532 (우리 NCM811 아님) · 압흔 ≈ 1차입자 크기의 국소값
- [m] xu2017_nmc532_nanoindentation_modulus_hardness_toughness ([Xu17]) | 규칙 — 나노 경도는 입자 스케일 접촉 지지압의 상한 쪽 값으로만 씀: 하중 분담 판정 구간을 "나노 경도 (8.6 ± 1.3 · NMC532) 상한 · 입자 압축 강도 하한" 처럼 스케일을 밝혀 다시 적거나 판정을 빼고 서술로만 | 조건 R1 | §7 표 (L321) · §9-3 (L418–423): 지금의 "3–6 GPa 문헌대" 는 출처 없음 · pristine 8.6 은 그 상단보다 2 SD 위 | 카드 판정 (우리 쪽) · 입자 압축 강도는 다른 카드의 다른 양
- [m] xu2017_nmc532_nanoindentation_modulus_hardness_toughness ([Xu17]) | 방법 — AM 파괴를 켤 때 인성은 두 팔: 이차입자 계면 0.102 ↔ 펠릿 급 0.309 MPa·m^½ (우리 0.3 은 펠릿 값) · 개시 하중 ∝ K² 라 0.3 → 0.102 면 ×0.116 (카드 산술) · 이 K_c 는 pop-in 길이 하나에 걸린 방법 조건부 값 | 조건 R7; 흐름 밖: 파괴 분류 → 수송 식 재적합 | §7-3 (L351–365) · §6-3 (L286–294) · §9-4 (L424–426) · Table 1 (stated) | 압입 방사 균열 ↔ 구–구 접촉의 원뿔 균열은 파괴 모드가 다름 (L363–365)
- [m] xu2017_nmc532_nanoindentation_modulus_hardness_toughness ([Xu17]) | 실험 대조법 · 함정 — 압입 값을 받을 때 확인 셋: 위치 (0.25 < y/D < 0.75 에서 수렴) · 기지 교체 (CB + PVDF ↔ 페놀수지에서 같은 값) · 하중 (균열 문턱 2 mN 아래) — 균열이 생기는 하중에서는 E 가 가짜로 낮게 나옴 (10 mN ≈ 86 GPa) | 흐름 밖: 실험과의 대조 (SE · AM 압입 값의 채택 조건) | §3-5 (L138–142 · stated + digitized) · Fig 4 행 (L255) | NMC532 · SI 미보유

## 카드 문제

### A. 카드가 스스로 적어 둔 논문 쪽 불일치 — 인용 전 확인용 (고치지 않음)

1. `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` §8 (L376–407) — (a) pristine 값이 두 벌: Table 1 · 본문 142.5 / 8.6 ↔ Fig 5 의 0 % · 0 사이클 점 ≈ 145.1 / 8.9 (digitized) · 본문 "about 145" — 저자 비율 (77 / 80 % · 74 / 73 %) 은 145 / 8.9 기준으로 읽힘 → 카드 권고: 인용은 stated 142.5 ± 11.3 / 8.6 ± 1.3 · 비율은 Table 1 기준 (78 / 83 % · 75 / 76 %) (L378–381) · (b) 쿨롱효율 세 값 84.3 % ↔ ≈ 94 % ↔ ≈ 98 % (L384–385) · (c) 기지 "< 15 GPa" ↔ 판독 ≈ 6–44 GPa (L382–383) · (d) pop-in 기준 곡선 맞춤이 두 표현 (2 차 다항식 ↔ "Hertzian fitting") — K_c 에 직접 영향 (L397–398) · (e) "SOC 100 % = Li0.5" 는 저자 표기 · 카드 산술로는 Li ≤ ~0.41 (L386–388) · (f) 초록의 "interfacial fracture strength" 는 강도가 아니라 인성 (L36) · (g) 응집 에너지 절대값이 정의와 자릿수 불일치 (L395–396).
2. `zunker2024_bulk_elastic_partII` — 논문 오타 (카드 지적): eq (13) 의 지수 −1.1 ↔ eq (5) · App C 의사코드의 −4.4 (L59 · L271).
3. `zunker2025_dem_large_deformation_compaction` — 논문 안에서 응력 정의가 절마다 다름: MPFEM 대조 = 벽 반력 / 면적 · 정제 계산의 반경응력 = 입자 응력 텐서 평균 × 부피분율 (L279–284 · L542–543).

### B. 카드 안의 서로 다른 값 · 산술 · 정의 (내 검토 — 원문 미확인 · 고치지 않음)

4. `zunker2024_mdr_contact_model_partI` §3-1 (우리 계산 표 · L79–96) — 탄성률 정의: 카드는 E*_c = E/(2(1−ν²)) = 12.80 GPa (같은 구 두 개의 합성값) 를 넣으면서 변위는 구–평면 값으로 풀고 다시 ×2 한다. 같은 카드의 eq (3) (L141) 을 구 ↔ 강체 평면에 적용하면 E*_c = E/(1−ν²) 이고, eq (40) 이 p̄_H ∝ E*_c·√(δ/R) 이라 정의가 2 배 다르면 항복 변위는 약 4 배 작아지는 쪽으로 달라진다. 원문의 E*_c 정의를 확인하기 전에는 "항복의 13 배 (3.6–169 배)" 를 그대로 인용하지 말 것. 같은 가정이 r_Ip · Δl (L93 · L96) 과 2025 편 카드의 K_Ic 1.64 MPa·m^½ (L82) 에도 들어 있다. (p_Y/Y 2.08–2.26 은 이 정의와 무관.)
5. `zunker2024_mdr_contact_model_partI` §3-1 — r_Ip (Y = 0.05 GPa) = 5.7 µm (L93) 는 카드 자신의 식 E*_cΔγ/(πY²) 와 입력 (12.80 GPa · 1.107 J/m²) 으로는 ≈ 1.8 µm (다른 두 열 200 nm · 50 nm 는 식과 맞음 · 5.7 은 π 를 뺀 값과 같음) → 그 열의 2a/r_Ip 0.066 (L95) 도 ≈ 0.21. 판정 (❌) 은 안 바뀐다.
6. `zunker2024_mdr_contact_model_partI` — "모델은 E/Y 6.25–200 전 구간 검증" (L300) ↔ "모델 하한 E/Y ≈ 10 · E/Y ≲ 10 은 쓰지 말 것 · (a)–(e) 가 semi-quantitative" (L67 · L249 · L385) — 스윕 범위와 권장 유효 범위를 구분해 인용해야 함.
7. `zunker2024_mdr_contact_model_partI` — 우리 후처리의 접촉 경도: "상수 H (= 2.8–3.0 Y)" (L92 · L333) ↔ "δ→0 극한값 (Tabor 2.75) 에 고정" (L299) · 카드 스스로 "우리 코드가 H 를 정확히 몇으로 쓰는지" 를 선행 확인으로 남김 (L335–336) → "면적 24–44 % · σ +12–20 %" 는 그 확인 전 값.
8. `zunker2024_bulk_elastic_partII` — ψ_b 배수 표기 두 가지: "6 배" (L12–13) ↔ "6.25 배" (L215 · 2025 편 L534) (0.5 / 0.08 = 6.25).
9. `zunker2024_bulk_elastic_partII` — 표현 모호: 머리의 "Varkey F_mc (ρ>0.7 과강성 보정)" (L8) ↔ 대조표의 "조밀 영역에서 접촉모델이 과연해 응력이 부족" (L187) — "뻣뻣하게 만드는 보정" 으로도 "과강성을 고친다" 로도 읽힘. Part I 카드도 "Varkey ρ>0.7 과강성" (L242 · L348).
10. `zunker2024_bulk_elastic_partII` — 벌크 힘의 꼴: eq (27) 은 증분식 dF_Bulk,i = (A_con/V)·κ·dδ̄_o·A_C,i (L86) 인데 App C 의사코드 옮김은 F_Bulk = (A_con/V_geo)·δ_o,Bulk,i·κ·A_C,i (누적 변위 · L157). A_tot 도 eq (32) 는 Σ(δ_max,MDR,i + δ_o,Bulk,i) (L106) · §8 ① 간략식은 Σδ_i (L226). 구현 전 원문 확인.
11. `zunker2024_mdr_contact_model_partI` ↔ `zunker2024_bulk_elastic_partII` — 식 번호가 편마다 다름: 반경 갱신 식이 Part II 카드에서는 eq (34) (L60 · L121) · Part I 카드에서는 eq (37) (L159–160 — Part I 의 eq 34 는 보정 변위 δ_R). 기하 부피 식도 Part II eq (29) = Part I eq (C.1). 인용 때 편을 밝혀야 함.
12. `zunker2025_dem_large_deformation_compaction` — 탄성 회복 0.08 (L64) 은 최대 변형을 0.4 로 둔 값 · 같은 표의 높이로 계산한 최대 변형은 0.390 (L59) → 0.07. springback 13.1 % (DERIVED) 도 0.08 기준.
13. `zunker2025_dem_large_deformation_compaction` — 비용 배수 표기 셋: "≈ 2×10⁴ 배 (벽시계) · ≈ 2×10⁵ 배 (코어-시간)" (L106) ↔ "2×10⁴–10⁵ 배" (L444) ↔ 인용 문장 "roughly four orders of magnitude" (L516).
14. `zunker2025_dem_large_deformation_compaction` ↔ `zunker2024_mdr_contact_model_partI` — "So 2021 … rel.density 0.98 · LPS+Si · 600 MPa · 다른 캡" 에 2025 편 카드만 "2D" 를 붙임 (L468 ↔ Part I L319) · slug 가 없어 어느 카드인지 모름 (폴더에 so2021 카드가 둘).

### C. 서지 · 낡은 참조 · 미확인 표기 · 이름 겹침

15. `zunker2025_dem_large_deformation_compaction` — 서지 미완: DOI n/a · 권호 · 쪽 없음 (프리프린트 판 · L3 · L37–38 · L551) → 인용 전 출판판 확인.
16. `zunker2025_dem_large_deformation_compaction` · `zunker2024_mdr_contact_model_partI` — 순수 SE 판정선의 근거 값 "Minnmann 10 % @300 MPa" (Part I L326 · 2025 편 L341 · L401) · "Doux LPSCl 실측 floor 근처 18 %" (L403) 에 출처 위치 · 표지가 없음. 참고 (카드 밖 — 리포 CLAUDE.md 의 원장 CL-94): "순수 SE 기공 ≈ 10 % @ 300 MPa (Minnmann)" 은 2026-10-03 에 출처 철회로 적혀 있음 · 두 카드 (2026-08-25 작성) 는 그 전 표기.
17. `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` — 낡은 참조: Sharma 2023 (NMC811 K 0.271) 을 "미보유 · 다음에 확보할 원문" 이라 적지만 (L357–359) 같은 폴더에 sharma2023_nmc_single_crystal_anisotropic_nanoindentation.md 카드가 있음 (파일 목록으로만 확인 · 내용 대조 안 함).
18. `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` — 카드가 미확인으로 남긴 것: SI (Fig S1–S7) 미보유 (L7–8) · "142 GPa" 계보 세 편의 뿌리는 추정 (L335–337) · `so2022_dem_compaction_coated_particles_assb` 의 Cheng [37] 이 이 논문 [27] 과 같은 원전인지 미확인 (L505) · 우리 코드의 인성 출처 표기 ("Quinn 2020" · "Liu 2020") 는 출처 미확인 (L322–323) · E · H 의 ± 정의 미기재 (L25).
19. Zunker 세 카드 — 그림 이미지 미확인 (텍스트 추출만) 이라 그림에서 읽은 값이 0 개 (Part I L54–56 · Part II L44 · 2025 편 L48–49) · 2025 편은 graphical abstract 쪽 잡음으로 본문 쪽만 읽음 (L49). 곡선 값이 필요한 대조 (m 항의 U1 · U6) 는 원문 그림을 다시 봐야 함.
20. 이름 겹침 — 2025 편 카드 §9-3 의 "경로 A / 경로 A′" (L325–346) 는 지시서의 "후보 A / 후보 A′" 와 다른 뜻 (머리말 참조).
