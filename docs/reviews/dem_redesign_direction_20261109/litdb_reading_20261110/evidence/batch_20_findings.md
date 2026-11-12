# batch_20 정독 근거 (카드 4 장 · 전문 읽음 · 2026-11-10)

읽은 카드: `vijay2025_hybrid_cgmd_dl_slurry_microstructure` (687 줄) · `wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn` (437) · `yoo2026_porosity_gradient_dry_electrode` (480) · `zhang2026_dryprocess_electrode_architecture_cell_level` (1486). 끝까지 못 읽은 카드 없음 (vijay 4 번 · wang 6 번 · yoo 4 번 · zhang 10 번에 나눠 마지막 줄까지 읽음).

배치의 성격: 네 장 모두 **액체 LIB (또는 슬러리 단계까지만 간 ASSB) 의 제조 · 미세구조 · 대리모델** 카드다. vijay = CGMD 슬러리 + DEM 압연 + DL 시간 대리 (ASSB 는 슬러리에서 끝) · wang = 캘린더된 NCM811 LIB 양극의 복셀 FE 체적탄성률 + GNN · yoo = 건식 흑연 음극의 두께 방향 기공 구배 실험 + 토모 계산 · zhang = 건식 NMC811 후막 실험 + CGMD (AM 없음) + COMSOL. **MPM 카드 · 순수 SE 압력별 기공 · 되돌아옴 실측 · SE 항복 / 경도 · 하중 몫 · 큰 변형 접촉 법칙 대안을 준 카드는 없다.** 가압 · 탈압 계획에 쓸 것은 방법 · 보고 규율 (2D → 3D 경고 · 해상도 · 기공 z 프로파일 · 탄성 균질화) 이다.

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (`stated` · `source-data` · `derived(ours)` · `figure-read ≈` · `[인쇄]` · `[판독]` · `[우리 산술]` · `[추정]` · `[미확인]`) · 없으면 "표지 없음". "카드 풀이" = 논문 문장이 아니라 카드 작성자의 서술. "내 검산" = 카드에 적힌 숫자끼리만 대조한 것 (새 계산 아님 · 카드 문제 절에만 씀). 따옴표 안 문장은 카드가 옮겨 둔 원문 (한국어 따옴표는 카드의 옮김). **"인용 금지" · 철회 표지가 붙은 값** (숫자로 옮기지 않음 · 위치만): zhang2026 L472 · L1260 (D_Li) · L925 (CE 로 수명을 말하는 형태) · L1174 (원장 CL-33 — 카드에도 숫자 없음) · L1318 (원장 CL-24 철회 계열 두 값 · ⛔ 표지 있음). 랩 표준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³) 은 고정 — 이 배치에는 그와 같은 양의 문헌 값이 없다.

---

## a. 순수 SE (LPSCl · 황화물) 압력별 기공 곡선 · 진밀도

이 배치에 없음.
- [a] vijay2025_hybrid_cgmd_dl_slurry_microstructure | (참고 · 같은 양 아님) ASSB 슬러리 밀도 1.415 g/cm³ (외삽 1.400 · %diff 1.06) = CGMD 슬러리 상자 밀도 — 이 논문에서 ASSB 로 내려간 유일한 물성 | Table 6 · L116 · §10-A L539 | stated | NMC-622 + argyrodite + CBSA 슬러리 · 압축 없음 · SE 진밀도가 아니므로 랩 표준과 견줄 양이 아님

## b. 압력을 뺄 때 되돌아오는 양 · 잰 방법

이 배치 카드 자신의 측정 · 계산값은 없다. 다른 카드를 가리키는 서술과 방법만.
- [b] vijay2025_hybrid_cgmd_dl_slurry_microstructure | 압연 DL 자매편 (정본 `galvezaranda2024_time_dependent_dl_calendering_microstructure`) 의 springback 을 "우리가 그림에서 뽑았다": 압연도 25 / 35 / 45 % → 4.8 / 7.6 / 10.1 %p (그 논문은 숫자 0 건) | §12-1 L645 | 다른 카드의 그림 판독 (2차) | 이 카드의 값 아님 · 재료 · %p 의 정의가 이 카드에 없음 → 그쪽 카드에서 확인
- [b] zhang2026_dryprocess_electrode_architecture_cell_level | Weitze 2024 카드가 springback 을 다룬다는 포인터뿐 | §8-E L1135 · §13 L1329 | 표지 없음 | 값 없음
- [b] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 되돌아옴 측정 없음 · 대신 압축이 끝난 구조의 작은 변형 탄성 균질화 (주기 경계 · ε₁₁ = ε₂₂ = ε₃₃ = −0.0125 · K = −P/(ΔV/V₀)) 방법 — 되돌아옴 크기를 정하는 탄성 계수 쪽 | §3-3 L90–91 · §8-7 L371–374 | [인쇄] · 카드 제안 | 액체 LIB · 선형 탄성 · 완전 결합 복셀

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 환산

- [c] yoo2026_porosity_gradient_dry_electrode | primer layer (Super P : 바인더 90 : 10) 미세압입: PVDF-PL 압축계수 6.31 MPa · 탄성계수 15.99 MPa (최저) · PAA · CMC-PL 은 약 2 배 | §4.1 L140–142 · Fig 2c–e · S4 | 표지 없음 | 탄성 · 압축 계수뿐 (항복 · 경도 · 크리프 없음) · 일축 항복 환산 없음 · 비압연 PL (SAICAS-DN 원통팁 Ø600 µm · 0.1 µm/s · stop 0.45 N = 1.6 MPa) · SE 아님
- [c] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | NCM 경도 2차 인용: de Vasconcelos [26] = NMC532 이차입자 E 139 GPa · H 8.9 GPa · [25] = 113 GPa · H 7.8 (정본 sedlatschek2026 카드가 전한 값) | §7-3 L316 · L28 | [추정] (2차 대 2차 · 원전 미열람) | NMC532 (NCM811 아님) · AM · 압입 경도 · 일축 항복 환산 없음
- [c] vijay2025_hybrid_cgmd_dl_slurry_microstructure · zhang2026_dryprocess_electrode_architecture_cell_level | 항복 · 경도 값 없음 (vijay = E · ν · σ_y · COR 0 건 · L421 / zhang = 인장강도 · 탄성계수 수치 n/a · L508) | L421 · L508 | — | —

## d. 단단한 + 무른 입자 혼합 압축의 하중 몫 · 재밍

하중 몫 · 재밍을 직접 잰 카드 없음. 관련만.
- [d] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 선형 탄성 FE 에서 무른 상 (CBD 1.8 GPa · 봉우리 ≈9 vol%) 을 넣으면 K +10.6 % (13.531 → 14.965 GPa · 같은 20 개) — 무른 상의 강성 몫이 작다 | 표 1 p.6 · L93 · L210 | [인쇄] · [우리 산술] | 압축 과정 아님 · 작은 변형 −1.25 % · 액체 LIB CB/PVDF (SE 아님)
- [d] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | AM 망 (≈70 vol% · 결합 목) K ≈15–16 GPa 로 우리 DFT LPSCl B₀ 26.23 GPa 보다 낮다 → 카드 해석: "얼린 AM" 근사가 정당한 것은 위치 고정 때문이지 골격이 단단해서가 아니다 | §8-5 L363–364 | [추정] | 액체 LIB · 완전 결합 복셀 · 둘째 상 강성 0 (카드가 "값 이전 금지" 명시) · ⚠ 카드 문제 3 (프로젝트 기록과 어긋남)
- [d] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 국소 응력 집중: σ₁₁ 범례 최솟값 −1.804 × 10¹⁰ Pa ≈ 부피 평균 (≈−0.57 GPa) 의 ≈30 배 → "목이 하중을 진다" | §3-3 L92 · 그림 6b · L260 | [인쇄] + [우리 산술] | 범례 극값은 한 절점일 수 있다 (카드) · 선형 탄성
- [d] yoo2026_porosity_gradient_dry_electrode | 단단한 흑연 필름 아래 무른 primer layer 가 라미네이션 · 캘린더 때 소성변형 → 집전체 쪽이 더 치밀 → 두께 방향 기공 구배 (가장 무른 PVDF-PL 이 가장 가파름) | §3 L111–116 (p.9) | 표지 없음 (저자 해석) | 응력 · 하중 몫 측정 없음 · 입자 혼합이 아니라 층 구조 · 흑연 LIB

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위 · 대안

대안 (multi-contact · MDR · EEPA · Thornton–Ning · Storåkers) 을 쓴 카드 없음. 각 카드의 접촉 표현만.
- [e] vijay2025_hybrid_cgmd_dl_slurry_microstructure | CGMD 접촉 = LJ 12-6 + granular Hertz (순수 탄성 · 이력 접선 · Coulomb X_µ 0.012–0.015) · 항복 캡 · 잔류 겹침 · 형상 변화 없음 · 카드: "Thornton–Ning/EEPA 류의 접촉 소성조차 없다" · 압연 DEM 접촉법칙은 미보고 | §4-1 L218–222 · §4-3 L247–249 · L237 | stated / 카드 풀이 | 맞춘 값 = FF 계수를 슬러리 밀도 · 점도에 맞춤 (ref [39] PSO 상속 · L226) · Table 1 은 chemistry 마다 12–14 행 (몇 개를 맞췄는지 카드에 없음)
- [e] zhang2026_dryprocess_electrode_architecture_cell_level | CGMD = LJ 12-6 + harmonic 결합 · 각만 · 접촉역학 (Hertz · 마찰 · 소성 · 점착) 없음 · FF 수치 0 개 공개 (유일한 관계 ε(VGCF–PTFE) > ε(PTFE–PTFE)) | §4-1 L554–564 | stated | 실험 정량 보정 0 (L625)
- [e] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 접촉 법칙 없음 — 복셀 면 공유 = 완전 결합 · 카드: 같은 기하의 점접촉 망보다 단단한 쪽 | §4-2 L220–223 | [추정] (방향 논증 · 크기 미측정) | 선형 탄성 균질화

## f. MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙 · 수치 오차 추정

MPM 카드 없음. 해상도 · 수치 오차 관련 (전부 MPM 아님).
- [f] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 복셀 FE 격자 수렴 (10³ · 20³ · 40³ · 80³ · 100³ 재사상): 80³ ↔ 100³ 차 0.36–0.75 % (평균 0.61 %) · 10³ 의 100³ 대비 상대 편차 1.04–2.01 (= 2–3 배 단단 · 거칠면 목이 굵어짐) · 40³ (복셀 0.45 µm) 부터 평탄 | 부록 D.2 L94–95 · 그림 D1 · §8-4 L358–359 | [인쇄] / [판독] | 복셀 FE · 입경 분포 [미확인] (L47) 이라 지름당 셀 수로 못 바꿈 · RVE 크기 수렴 시험 없음 (L289)
- [f] zhang2026_dryprocess_electrode_architecture_cell_level | PFIB z 슬라이스 250 nm > VGCF 직경 100 nm → 개별 섬유 해상 불가 → "CBD" 균질상 lumping (σ_CBD 700 S m⁻¹ 한 상수) · 카드: "선택이 아니라 해상도의 강제" | §5-2 L811–813 · §14-2 L1380–1384 | stated / 카드 풀이 | 영상 해상도 · 면내 픽셀 미보고 · REV / voxel 수렴 시험 n/a (L506)
- [f] yoo2026_porosity_gradient_dry_electrode | 같은 두께 방향 기공 구배가 XCT (픽셀 250 nm) 와 FIB-SEM (46.52 nm) 두 해상도에서 모두 보임 → "측정해상도 artifact 아님" | §4.3 L204–205 · Fig 5e | 표지 없음 | 영상 (계산 격자 아님)
- [f] vijay2025_hybrid_cgmd_dl_slurry_microstructure | 정규화 위치 오차를 물리 단위로 바꾸면 test ≈1.7 µm = 최근접 접촉 거리 (RDF 첫 봉우리 ≈2.5 µm) 의 ≈68 % · 건조 bead 지름 1.3 µm 의 ≈1.3 배 — 오차를 특징 크기 대비로 판정 · SI 비정규화 CV MeanAE 0.991–0.998 µm 가 환산 1.0 µm 와 1 % 안 | §10-D L558–566 | derived(ours) + figure-read | DL 좌표 오차 · 스케일러 범위 가정 (L567–569)

## g. 2D → 3D 이전의 경고 · 증거

- [g] zhang2026_dryprocess_electrode_architecture_cell_level | 2D 대면적 단면 한 장의 헤드라인 (최대 연결 CBD 61.2 vs 17.1 % = 3.58 배) 이 3D PFIB 슬라이스 통계 (121 / 135 장 평균 0.5359 vs 0.3836) 로는 1.397 배 — "2.6배 과장" · 2D 의 17.1 % 는 3D 분포 최솟값 (16.3 %) 근처 · 61.2 % 는 p75 (58.7 %) 위 | §3-3 L284–298 · L363–371 | stated · source-data → derived(ours) | 액체 LIB CBD · 정규화 분모 미정의 · 2D · 3D 분할 파이프라인 다름 (Weka ↔ Avizo) · 방향은 유지 (d 1.26)
- [g] zhang2026_dryprocess_electrode_architecture_cell_level | COMSOL 메시 = *"by stacking two identical images together"* → 2D 단면의 z 압출 · 면외 연결이 인위적으로 완전 (카드 판단: 대비를 줄이는 보수 편향일 가능성 · 미검증) | §4-3 L655–660 · §11-⑤ L1252–1253 | stated (원문 인용) + 카드 풀이 | 연결성이 논지 핵심인데 편향 방향을 논문이 논하지 않음
- [g] zhang2026_dryprocess_electrode_architecture_cell_level | TauFactor τ 를 2D 에서 쟀는지 3D 에서 쟀는지 애매 ("segmented PFIB-SEM images") | §3-8 L512 · §4-4 L676 | n/a | —
- [g] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 2D SEM 질감 (Gram) 손실로 3D 재구성 → 2D 통계만 맞추고 3D 목 연결은 직접 제약하지 않음 · K 는 그 목이 정함 (국소 지수 ≈6) · 직교 세 방향 기준 영상 미기재 (같은 단면이면 등방 가정 — 캘린더 전극은 이방) · 재구성 검증 = 기공률 한 숫자 | §10-3 L388 · §3-2 L79 | [미확인] / 카드 풀이 | 액체 LIB · 재구성 부피 하나
- [g] vijay2025_hybrid_cgmd_dl_slurry_microstructure · yoo2026_porosity_gradient_dry_electrode | 해당 없음 (3D 만) | vijay §10-J L608 | — | —

## h. DEM 에서 FE · MPM 으로 넘긴 선례 · 시점

DEM → FE · MPM 넘김 선례 없음. 관련 음성 사례만.
- [h] vijay2025_hybrid_cgmd_dl_slurry_microstructure | 사슬 = 슬러리 CGMD → 건조 CGMD → 압연 DEM; DL 예측 좌표를 바로 NEMD 에 넣으면 입자 손실 → CGMD 평형화 1 스텝 필수 · 카드가 옮긴 저자 귀속 *"예측 위치가 서로 너무 가까워 겹침 → 입자간 힘 불균형 → 내부 충돌"* · 평형화는 겹침만 풀고 중거리 구조는 못 고침 (Fig 7a) | §3-3 L133 · §5-5 L380–382 · §5-4 L360–361 | stated (한국어 옮김) / figure-read ≈ | 입자 → 입자 (FE · MPM 아님)
- [h] zhang2026_dryprocess_electrode_architecture_cell_level | CGMD 출력이 COMSOL 입력이 되지 않는다 — CGMD 상자 (AM 없음 · 압밀 없음) 와 COMSOL 대상 (PFIB 실물) 이 달라 "공정 → 구조" 와 "구조 → 성능" 이 다른 대상 위에서 따로 성립 | §4-0 L531–535 | 카드 풀이 | 넘김 없음
- [h] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 영상 → 복셀 FE (DEM 을 거치지 않음 · 압축 물리 없음) | §4-1 L217 · §4-2 L222 | 카드 풀이 | —

## i. 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음 (AM + SE 카드 없음 · 압력 축 카드 없음). 참고 (AM + 탄소 · 바인더 · 액체 LIB · 압력 아님):
- [i] vijay2025_hybrid_cgmd_dl_slurry_microstructure | NMC-111 (LIB) 압연 DEM 기공: 압연도 0 / 15 / 20 / 25 / 30 % → 53.53 / 49.65 / 47.14 / 44.50 / 41.14 % (CGMD 8 시드 평균) | Table 9 · L139–143 | stated | 두께 감소율 축 (압력 0 건) · 누른 채 / 뺀 뒤 카드에 없음 · ASSB 기공 0 건 (L18)
- [i] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 캘린더된 NCM811 LIB 양극 기공 참밀도 21.9 · 수은 20.7 · 재구성 20.3 % (한 상태) | 표 5 · L104 | [인쇄] | 캘린더 조건 [미확인] · 압력 없음
- [i] yoo2026_porosity_gradient_dry_electrode | 흑연 음극 MIP 32.2–33.3 % @ 전극 밀도 1.5 g/cm³ · VED 계산 (Fig S26) 밀도 1.5 → 1.7 g/cm³ 에 기공 28.6 → 19.1 % | §4.1 L128 · §4.5 L258 · L320 | 표지 없음 | 흑연 음극 · 압력 없음 · 밀도 1.5 의 두 기공 값 (카드 문제 8)
- [i] zhang2026_dryprocess_electrode_architecture_cell_level | 건식 NMC811 후막 목표 기공 ~30 % (실측 n/a) · 카드 유도 전극 두께 91.4–105.0 µm · 밀도 3.07–3.34 g/cm³ (ε 30 % · ρ 가정) | §2-1 L166 · §2-4 L209–214 | stated / derived(ours) | 캘린더 압력 n/a · 기공 실측 없음

## j. 카드가 스스로 적은 한계 가운데 가압 · 탈압과 닿는 것

- [j] vijay2025_hybrid_cgmd_dl_slurry_microstructure | DEM 압연의 접촉법칙 · E · ν · μ · COR · 판 속도 · 압력 전부 미보고 · "압축 축이 '두께 감소율' 이라 우리 300 MPa / Heckel P_y 와 원리적으로 겹칠 수 없다" · ASSB 는 슬러리에서 끝 (압연 · 기공 = NMC-111 전용) | §4-2 L237–238 · §10-A L539 | stated (미보고) / 카드 풀이 | —
- [j] vijay2025_hybrid_cgmd_dl_slurry_microstructure | 저자 결론: 에너지 보존 같은 물리 제약을 넣으면 평형화 단계를 없앨 수 있을 것 (미래 과제) — 현행은 순수 지도학습 | §4-4 L273–275 | stated (결론) | —
- [j] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 저자: *"the CBD-pore was physically idealized as a zero-stiffness region … a computational simplification rather than based on the assumption that the mechanical contribution of the CBD is strictly negligible"* — 세-상 판으로 −9.58 % 과소 확인 | §3-1 L65 · §10-4 L389 | [인쇄] | 무른 상 강성 0 근사의 자인
- [j] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 역학 모형 = 선형 탄성 · 완전 결합 목 · 소성 · 손상 없음 · 압축 · 캘린더 과정의 물리 없음 · 라벨 = 모형 내부값 (실험 K 대조 없음 — 저자 인정) | §10-4 L389 · §4-2 L221–222 | [인쇄] / 카드 풀이 | —
- [j] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 저자: *"the present spatially grouped evaluation remains a within-parent-volume validation … do not establish cross-volume generalization"* | §3-11 L181 (p.14) | [인쇄] | —
- [j] yoo2026_porosity_gradient_dry_electrode | 카드: 토모그래피는 고정 미세구조 정량이지 압축 역학 예측은 못함 (post-mortem 구조) | §7(d) L426–427 | 카드 풀이 | —
- [j] yoo2026_porosity_gradient_dry_electrode | 저자 caveat: 중간 면적용량 ~3.5 mAh/cm² 에서만 평가 · 더 높은 로딩 / 두께에서 장거리 연결성 유지 여부는 향후 과제 | §4.3 L226–227 | 표지 없음 | —
- [j] zhang2026_dryprocess_electrode_architecture_cell_level | 캘린더 압력 · 갭 · 선하중 n/a (Alabdali · Weitze 에 이어 세 번째) · 최종 도전망은 캘린더링이 정하는데 그 조건이 논문에 없다 (100 °C 만) | §2-1 L170 · §3-8 L501 · §11-⑫ L1276–1277 | n/a | —
- [j] zhang2026_dryprocess_electrode_architecture_cell_level | 캘린더링 (압축) 은 CGMD 로 전혀 다루지 않음 (NVT 고정 부피 · 공정 3 단계 중 1 단계만) · Fig 3f 미수렴 ("~250 nm" 는 스냅샷) | §4-6(d) L742–743 · §11-⑩ L1270–1271 | 카드 풀이 / figure-read | —

## k. DEM 의 한계 (인용 서지 포함)

- [k] vijay2025_hybrid_cgmd_dl_slurry_microstructure (Vijay et al. 2025, Energy Storage Mater. 75, 103883, DOI 10.1016/j.ensm.2024.103883) | 말 없음 — 논문이 DEM 한계를 말한 문장을 카드가 옮기지 않았고 압연 DEM 파라미터 자체가 미보고 (L237). 카드 풀이: 입자 = 구 bead 만 · 강체 구 + 순수 탄성 접촉 · 항복 캡 · 잔류 겹침 · 형상 변화 없음 | §4-3 L245–248 | 카드 풀이 | 논문 문장 아님
- [k] vijay2025_hybrid_cgmd_dl_slurry_microstructure (같은 서지) | 보정값이 물성이 아닌 사례 (카드 풀이): CGMD 접촉 강성 k_n 3.31–7.5 kPa → E* ≈2.5–5.6 kPa = "'연화된 재료'가 아니라 *애초에 재료가 아닌* 유변학 피팅 계수" (카드 frame[2] 3 종 표의 (iii)) | §3-6 L206–209 · §7-2 L431–440 | derived(ours) | 슬러리 CGMD (압밀 DEM 아님)
- [k] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn (Wang et al. 2027, J. Energy Storage 183, 125194, DOI 10.1016/j.est.2026.125194) | 말 없음 (DEM 을 쓰지 않음) | — | — | —
- [k] yoo2026_porosity_gradient_dry_electrode (Yoo et al. 2026, Energy Storage Mater. ENSM 105331, DOI 10.1016/j.ensm.2026.105331) | 말 없음 (DEM 을 쓰지 않음) | — | — | —
- [k] zhang2026_dryprocess_electrode_architecture_cell_level (Zhang et al. 2026, Nature Energy, DOI 10.1038/s41560-026-01981-3) | 말 없음 (DEM 을 쓰지 않음). 카드 풀이 (우리 DEM 에 대한): 우리 LIGGGHTS 는 무작위 삽입 → 정착 → 일축 압밀로 시작해 전단 이력이 한 스텝도 없다 · 첨가제가 동역학 객체가 아니라 MPM 복셀에 사후 seeding · 비열적 granular dynamics | §8-B L1043–1051 | 카드 풀이 | 논문은 우리 DEM 을 다루지 않음 — 인용 근거는 "건식 공정 문헌은 전단이 도전망을 만든다" 까지
- [k] zhang2026_dryprocess_electrode_architecture_cell_level (같은 서지) | 카드가 만든 원고용 문장 (논문 원문 아님): *"Dry-processing 문헌은 전단이 도전망을 만든다고 본다 (Zhang 2026). 그 축은 우리 DEM 압밀 파이프라인에 원리적으로 없다 — 우리는 전단 이력 없이 일축 압밀만 하고, 탄소·바인더는 동역학 객체가 아니라 사후 seeding 된다. 다만 그 문헌의 전단 모델 자체도 활물질·압밀·전도도를 포함하지 않는 2성분 박스이므로, 현재 어느 모델도 '전단 → 도전망 → σ_e' 를 하나의 사슬로 잇지 못한다."* | §8-B L1064–1069 | 카드 풀이 | —
- [k] zhang2026_dryprocess_electrode_architecture_cell_level (같은 서지) | DEM 은 아니지만 입자 (CG bead) 모형의 한계 원문: *"This behaviour arises from mass and inertia differences, with lighter PTFE being more readily displaced by the relatively immobile VGCF."* → 카드: 구동력이 임의로 고른 bead 반경 (14 vs 50 nm · 질량비 41 배) 이 정한 관성 분리 · bead 1 개 ≈ C₂F₄ 1.52 × 10⁵ 단위 (Martini 대비 ≈10⁵ 배 거칠다) · 시뮬 ≈660 ns = 공정 10 min 의 ≈1.1 × 10⁻⁹ | §4-6(d) L735–739 · (a) L702–717 · (e) L746–757 | stated (원문 인용) + derived(ours) | CGMD (LJ bead-spring) · 압밀 DEM 아님

## l. 소성변형이 왜 어려운가 · 택한 우회와 값 (인용 서지 포함)

이 배치에 소성을 입자 계산에 넣기 어려운 이유를 설명한 카드 없음 (네 논문 모두 소성을 다루지 않음).
- [l] vijay2025_hybrid_cgmd_dl_slurry_microstructure (Vijay et al. 2025, Energy Storage Mater. 75, 103883) | 말 없음 — 소성 0 (항복 캡 · 잔류 겹침 · 형상 변화 없음) · 카드: "우리 DEM (hooke/hysteresis + Stage-E 소성면적) 보다도 아래" · 비용 = 슬러리 CGMD 9–10 h · 건조 24–36 h · 압연 DEM ≈6 h (14 코어 1 노드 · 입자 수 미보고) | §4-3 L247–248 · §3-5 L153–156 | 카드 풀이 / stated | 우회 없음
- [l] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn (Wang et al. 2027, J. Energy Storage 183, 125194) | 말 없음 — 등방 선형 탄성 · 소성 · 파괴 · 이력 없음 · 작은 변형률 −1.25 % 한 번 · 기하 비선형 끔 · 우회 = 압축 과정을 빼고 영상 구조 위에서 탄성만 균질화 · FE 라벨 1000 개 (51.2 만 요소씩) 계산 시간 미보고 | §4-2 L221 · §3-3 L90 · §3-10 L171 | [인쇄] / [미확인] | —
- [l] yoo2026_porosity_gradient_dry_electrode (Yoo et al. 2026, Energy Storage Mater. ENSM 105331) | 말 없음 — "무른 PL 의 소성변형" 은 저자의 기전 해석 (p.9) · 계산 모델 없음 · "MPM 압축 + scaffold 로 재현 가능한 물리" 는 카드 주장 | §3 L111–116 · §8 L459 | 표지 없음 / 카드 풀이 | —
- [l] zhang2026_dryprocess_electrode_architecture_cell_level (Zhang et al. 2026, Nature Energy) | 말 없음 — 카드: 그들 모델에서 형상 변화는 바인더 (PTFE 사슬 · 폴리머 자유도 · "소성 아님") 에만 있고 우리 모델에서는 SE (MPM J2) 에만 있다 · "탄소섬유의 형상변형은 양쪽 어디에도 없다" · CGMD 35,300 bead · 445 ns (프로토콜 합) | §4-2 L643–650 · §4-1b L620 · §4-1 L574 | 카드 풀이 / derived(ours) | —

## m. 받아들일 통찰

- [m] vijay2025_hybrid_cgmd_dl_slurry_microstructure | 무엇을: 합성 · 예측 구조의 합격 기준 = 상별 RDF (AM–AM 따로) + Fréchet 거리 + 아핀 축소 기준선을 같이 싣고 지는 칸을 그대로 보고 · 어디에: 흐름 밖: 예측기 · Phase 4 미세구조 합성 합격 기준 · 왜: 전역 위치 MAE 는 수 많은 상이 지배해 AM–AM 상관을 잃는다 (ASSB AM–AM DL 0.564 vs 기준선 0.314) · 그림에선 9/9 패널에서 DL 과 기준선이 겹침 | Table 8 L330–340 · §5-4 L348–353 · §8-① L475–489 | stated · figure-read ≈ | 액체 LIB · 슬러리
- [m] vijay2025_hybrid_cgmd_dl_slurry_microstructure | 무엇을: 예측 · 합성 좌표를 물리 솔버에 넣기 전 겹침 검사 · 평형화 단계 — 평형화는 겹침만 풀고 중거리 구조는 못 고친다 · 어디에: 흐름 밖: 합성 구조 → network_conductivity · STEP3 투입 전 겹침 게이트 · 왜: 예측 구조를 바로 NEMD 에 넣으면 입자 손실 · 겹침은 Holm 접촉반경과 ε_sphere 를 함께 오염 (카드) | §3-3 L133 · §5-5 L380–382 · §5-4 L360–361 · §7-3 L457–459 | stated · figure-read ≈ · 카드 풀이 | —
- [m] vijay2025_hybrid_cgmd_dl_slurry_microstructure | 무엇을: 같은 시드 짝 비교는 대응표본으로 — 독립 평균 CI 중첩으로 "차이 없음" 을 판정하지 않는다 · 어디에: 단계 3 (두 접촉 표현의 누르는 힘 비교를 짝으로 보고); 결과 전 대조 항목 · 왜: 8 짝 Δ 부호 5/5 + · 평균 +0.67 %p 인데 저자는 CI 중첩으로 "유의차 없음" | Table 9 L139–147 · §10-E L573–575 · §8-③ L500–504 | stated / derived(ours) | —
- [m] vijay2025_hybrid_cgmd_dl_slurry_microstructure | 무엇을: 오차는 물리 단위 · 특징 크기 대비로 보고 (정규화 MAE 0.017 = ≈1.7 µm = 최근접 접촉 거리의 ≈68 %) · parity plot 은 동적 범위를 상자 전체로 잡으면 늘 좋아 보인다 · 어디에: 흐름 밖: 예측기 대시보드 · 보고 방식 · 왜: ±50 µm 축 위의 ±2 µm 띠가 "거의 완벽" 해 보였다 | §5-3 L318–322 · §10-D L558–566 | derived(ours) + figure-read | 스케일러 범위 가정
- [m] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 무엇을: 눌린 구조 격자에 작은 변형 선형 탄성 균질화 (주기 경계 · 정수압 −1.25 % · K = −P/εᵥ) 를 걸어 탄성 계수를 내고, 다공 LPSCl 펠릿 벌크 E 4.7 ± 1.1 GPa (13 % 기공 · 정본 song2025 카드 값) 와 견준다 · 완전 결합 복셀 판은 그보다 단단해야 (차이 = 접촉 유연성) · Hashin–Shtrikman 상한 (그들 FE/HS⁺ 0.20–0.32) 으로 위 울타리 · 리포의 스칼라 FFT 균질화기를 탄성으로 확장하는 길이 가장 작다 (카드) · 어디에: 단계 6; 결과 전 대조 항목 · 왜: 압축 뒤 탄성 계수가 우리 DEM · MPM 어디에도 없는 판독 | §8-7 L371–374 · §8-4 L357–360 · §3-13 L203 | 카드 제안 · [우리 산술] | 펠릿 E 는 2차 인용 · 방향만 (크기 미정)
- [m] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 무엇을: 하중을 목이 지는 구조에서 거친 복셀은 목을 굵혀 강성을 과대 (10³ · 20³ 에서 2–3 배 · 40³ 부터 평탄 · 80³ ↔ 100³ 0.36–0.75 %) — 격자 수렴은 목 굵기가 풀리는 해상도까지 확인 · 어디에: U6; 단계 2 (해상도 수렴 시험) · 왜: 재사상 다섯 RVE 모두 같은 꼴 | 그림 D1 L95 · 부록 D.2 L94 · §8-4 L358–359 | [판독] · [인쇄] | 선형 탄성 · 재사상 (재구성 아님)
- [m] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 무엇을: 대리모델 보고 = "조성 기준선 R² → 대리 R² → 잔차 분산 중 몫" 세 칸 + 같은 설계점 (시드 형제) 묶음 CV 를 무작위 폴드와 나란히 · 어디에: 흐름 밖: ML 예측기 (ml_design_structure 중첩 CV) · 왜: φ 이차식 3 매개변수 0.905 > GNN 0.880 · 25 : 75 혼합 0.917 → GNN 몫 ≈13 % · 공간 묶음 분할 R² −0.007 | 표 12 L190 · §3-13 L206 · 표 10 L180 · §8-1 L342–345 · §8-2 L347–350 | [인쇄] · [우리 산술] | 혼합 비율은 시험 분할 위 사후 선택 (L191)
- [m] wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn | 무엇을: 이 논문을 부를 때 연도 · 저널 · 논문 번호를 함께 (Wang 2027, J. Energy Storage 183, 125194) · E_AM 140 의 출처로 쓰지 않음 (사용례 · NMC532 압입값 인용) · 어디에: 흐름 밖: 서지 위생 (NCM E 출처) · 왜: 원장 CL-90 이 철회한 "Wang 2020" 서지와 1저자 성만 같다 | §7-3 L316–318 | 카드 판정 (비준 대기) | —
- [m] yoo2026_porosity_gradient_dry_electrode | 무엇을: 기공은 전체값과 함께 두께 방향 z 프로파일 (top · middle · bottom + 1.25 µm 구간) 로 보고 · 어디에: 단계 0 (기공 연산자 · 판정 기준); 단계 4 · 5 (판 쪽 / 반대 판 쪽 구배) · 왜: 전체 MIP 32.2–33.3 % 가 같아도 top↔bottom 차가 24.5 vs 5.6 %p 로 다르다 | §4.1 L127–138 · Fig 2b · §7(d) L418–419 | 표지 없음 | 흑연 LIB · 원인은 무른 PL (저자 해석)
- [m] yoo2026_porosity_gradient_dry_electrode | 무엇을: 구조 구배가 해상도 인공물이 아님을 두 해상도에서 같은 구배로 확인 · 어디에: U6 (우리 격자 두 단계에서 같은 z 구배가 나오는지) · 왜: XCT 250 nm ↔ FIB-SEM 46.52 nm 에서 같은 구배 | §4.3 L204–205 · Fig 5e | 표지 없음 | 영상 해상도
- [m] yoo2026_porosity_gradient_dry_electrode | 무엇을: τ 를 두 독립 방법 (대칭셀 EIS 식 1 · 영상 확산 시뮬 식 2) 으로 내되 일치는 순서만 근거 · 두 식 모두 τ 가 제곱으로 들어가므로 우리 tau2 와 견줄 때 제곱 여부부터 맞춘다 · 어디에: 단계 7; 흐름 밖: τ 실측 앵커 경로 · 왜: EIS τ 절대값은 본문 미기재 · 순서 PVDF < PAA < WPE 만 같음 | §4.1 L145–153 · §4.3 L207–215 · §7(b) L385–394 | 표지 없음 | 기공 (액체) 도메인 τ
- [m] yoo2026_porosity_gradient_dry_electrode | 무엇을: 기공 쪽 망 지표 (PNM watershed 분할 → 기공 배위수 · connectivity matrix 정규화 밴드폭 표준편차) 를 입자 접촉 CN 의 보완축으로 · 어디에: 단계 7; 흐름 밖: voxel_conductivity 보조 지표 · 왜: 국소 CN (PAA 4.44 · PVDF 4.20 · WPE 2.94) 과 장거리 밴드폭 (PVDF 0.1581 > PAA 0.1309 > WPE 0.0976) 이 순서가 다르다 | §4.3 L217–225 · Fig S17–S19 · §7(d) L420–422 | 표지 없음 | 흑연 LIB
- [m] zhang2026_dryprocess_electrode_architecture_cell_level | 무엇을: 2D 단면 한 장의 배수를 3D 크기로 옮기지 않는다 · 이웃 슬라이스는 독립이 아니므로 유효 표본수로 · 어디에: 단계 3 (2D 결과 → 3D 는 방향만); 단계 0 (슬라이스 통계 판정에 n_eff) · 왜: 3.58 배 ↔ 3D 슬라이스 1.397 배 · lag-1 r 0.567 / 0.663 · τ_int 5.11 / 6.86 슬라이스 · n_eff 26.4 / 17.6 · Welch t 10.19 → 4.25 | §3-3 L284–298 · L325–343 · L363–366 | source-data → derived(ours) | 액체 LIB CBD · 정규화 분모 미정의
- [m] zhang2026_dryprocess_electrode_architecture_cell_level | 무엇을: 2D 영상을 z 로 복제한 준-2D 메시는 면외 연결을 인위적으로 완전하게 만든다 — 연결성 · 하중 경로를 다루는 2D 시험을 3D 로 옮길 때의 경고 · 어디에: 단계 3 · 왜: *"by stacking two identical images together"* 로 만든 메시에서 217 배 입자 전류 우회비를 냈다 | §4-3 L655–660 · §11-⑤ L1252–1253 · §14-9 L1452–1455 | stated (원문 인용) + 카드 풀이 | 편향 방향 미검증
- [m] zhang2026_dryprocess_electrode_architecture_cell_level | 무엇을: 균일도 ≠ 연결성 — 관측량 = 최대 연결 성분 분율 (탄소상 최대 연결 성분 / 전체 탄소 복셀) 을 균일도와 따로 · 어디에: 단계 7; 흐름 밖: graded-z 성패 지표 · STEP3 신규 지표 · 왜: 두께 방향 CBD 균일도는 건식이 더 나쁜데 (std 1.15 vs 1.00 %) 최대 연결 클러스터는 61.2 vs 17.1 % | §3-2 L261–271 · SI Fig 9 · §9-1 · 2 L1171–1178 | stated | 크기는 2D 단면 값 (위 항목)
- [m] zhang2026_dryprocess_electrode_architecture_cell_level | 무엇을: τ 를 쓸 때 D_eff 관계식 (ε/τ 인지 ε/τ² 인지) 을 같은 줄에 적는다 · 어디에: 단계 7 (수송 tortuosity = tau2 규약 확인) · 왜: TauFactor 규약 (D_eff = εD/τ) 이면 +15.3 % 인데 논문의 "~33 %" 는 ε/τ² (+32.9 %) 로만 재현 — 한 논문 안의 미끄러짐 | §3-4 L390–408 | derived(ours) | 공극 (액체) 상 τ · 기공 실측 없음

## 카드 문제

1. **vijay2025 — Minnmann 을 실험 앵커로**: L427 (§7-1 "실험 앵커" 칸) 이 우리 쪽 앵커로 "Minnmann 10 %@300" 을 적었다 — 순수 SE 300 MPa 기공 앵커로서의 Minnmann 은 철회됐다 (CLAUDE.md `CL-94`).
2. **vijay2025 — 세제곱근 산술**: L301 · L313–315 (와 L38 "정확히 닫힌다") 의 "(1.18/1.71)^(1/3) = 0.8872 ⇒ 11.28 % 작음" — 내 검산 (카드 숫자만): (1.18/1.71)^(1/3) = 0.8837 → 11.63 % 작음 (기울기로는 +0.132). 그림 기울기 +0.127 (= 11.3 %) 와의 닫힘은 "정확히" 가 아니라 근사 (11.3 vs 11.6 %).
3. **wang2027 — 얼린 AM 서술이 프로젝트 기록과 어긋남**: L364 (§8-5) 의 [추정] "우리 MPM 의 '얼린 AM' (무한 강성) 근사가 정당한 것은 … 위치에 고정되기 때문" — CLAUDE.md DO-NOT · `fam_platen_prereg` §11 기록은 얼린 AM 이 하중 0 을 져 SE 가 100 % 를 지고 정직한 가압에서 ε_sphere 1.125 % 로 과압축된다 (② AM 하중분담이 병목) 고 적는다.
4. **wang2027 — 참고문헌 [25] 연도 두 값**: L318 ④ · L400 · L417 — 이 논문 목록 2018 vs 정본 다른 카드 2019 (카드 자체 [미확인] 표지 · 고치지 않음 명시).
5. **wang2027 — "¼–⅙" 범위**: L312 · L430 "다공 LPSCl 펠릿 벌크 E 4.7 GPa = 압입 28 GPa 의 ¼–⅙" — 카드에 적힌 두 숫자로는 4.7/28 ≈ 1/6 만 나오고 ¼ 끝은 안 나온다 (+1.1 을 넣어도 ≈1/4.8 · 내 검산). 출처 카드 (song2025) 에서 확인 필요 (2차 인용).
6. **yoo2026 — 머리 표지가 내용과 다름**: L3 type `MPM` · L12 methods `dft, elastic` 인데 논문에 MPM · DFT 가 없다 (카드 본문 L407–409 "DEM 접촉망 σ도, MPM 소성 morphology도 없음").
7. **yoo2026 — 3C CC SOC 두 값**: L185–187 · L281 — DPE@PVDF-PL 3C CC SOC 가 본문값 27.89 % 와 Fig 4c 막대 라벨 29 % · 라벨 CC 29 + CV 72 = 101 %.
8. **yoo2026 — 밀도 1.5 g/cm³ 의 기공 두 값**: L80 · L128 (MIP 32.2–33.3 %) ↔ L258 · L320 (Fig S26 VED 계산 28.6 %) — 같은 전극 밀도에서 기공이 다르다 · 카드가 차이를 설명하지 않음.
9. **yoo2026 — "확정" 과장**: L152–153 — "정량 절대값은 본문 미기재" 라 적고 같은 괄호에 "후속 FIB-SEM 확산시뮬에서 WPE 3.09 / PAA 1.98 / PVDF 1.86으로 확정" — 미기재 EIS 값을 시뮬이 확정할 수 없다 (§7(b) L386 은 순서 일치만 말함).
10. **zhang2026 — 철회된 라벨**: L999 "우리 σ_SDCP 250 S cm⁻¹ | 재료 앵커" — 그 라벨은 철회됐다 (CLAUDE.md `CL-61` 2026-09-03 — ref [35] 는 σ_SDCP 를 뒷받침 못 함 · 값 지위 = 저자 지정). 카드 digested 2026-08-19 (철회 전).
11. **zhang2026 — σ_VGCF 100 의 출처 서술 모순**: L1020 "우리 100 은 직경보존 식에서 왔고" ↔ 같은 표 L997–998 (100 = 생산 입력값 · 직경보존 재척도값 = 11.04 @ vox 0.4) — 서로 다름 (CLAUDE.md CL-47 정정 10-03: 100 = 출처 없이 넣은 값).
12. **zhang2026 — 자기 경고와 어긋난 인용 문장**: L365 · L1203 ([Z26-2]) 이 Welch t = 10.2 를 쓰는데 카드가 L296 에서 그 값 (원시 n) 을 "⚠ 부풀려져 있다" 로, L350 에서 n_eff 판 4.25 조차 "유의성 검정으로 인용하지 말 것" 으로 적었다.
13. **zhang2026 — 한 문장에 세 배수**: L406–407 "τ 규약이 한 번 미끄러지면 D_eff 가 2.15배 틀린다" — 2.15 는 증가율 두 값의 비 (32.9 / 15.3 · 내 검산) 이고 같은 문장 괄호는 증가 배수 1.153 vs 1.329 · 절대 D_eff 차 2.5–2.9 배를 적는다 — "D_eff 가 2.15배" 는 적힌 숫자와 맞지 않음.
14. **zhang2026 — 작동압 원장 범위 두 값**: L175 "5–70 MPa 작동압 원장" ↔ L198 "Doux 5 · Lee 2 · Luan 30 · Wang2026 110–200 MPa".
15. **zhang2026 — 중원자 수**: L709 — PTFE bead = C₂F₄ 1.52 × 10⁵ 단위 · "원자 9.1 × 10⁵, 중원자 4.6 × 10⁵" — C₂F₄ 에는 수소가 없어 중원자 수가 원자 수의 절반일 근거가 카드에 없음 (결론 "약 10⁵ 배 거칠다" 에는 영향 없음).

(참고 · 문제 아님: zhang2026 의 "인용 금지" · 철회 표지 값 위치 = L472 · L1260 · L925 · L1174 · L1318 — 위 머리말 참조 · 숫자로 옮기지 않음.)
