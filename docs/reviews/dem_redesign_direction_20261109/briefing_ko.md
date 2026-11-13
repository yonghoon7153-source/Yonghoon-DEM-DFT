<!-- BRIEFING:UPDATED 2026-11-13 -->
# [DEM 우선 (수영)] 재설계 계획 브리핑 (쉬운 말 · 논문 기준)

**지위**: 1저자용 브리핑 · 메모 3.2 판 (`docs/reviews/dem_redesign_direction_20261109/memo_v3_2.md` · 고정 핀 `5afa16488`) 의 계획과 한정을 쉬운 말로 옮긴 것 · 결과 0 건 · 새 연구 계산 0 건 · 실행 GO 요청 아님.  정본의 규칙은 메모가 기준이고, 최신 수령 지위는 `docs/reviews/memo32_closure_20261113/README.md` 를 따른다.  Codex 독립 판정 11-13 = 문서 잔여 종결 가능 (HOLD) · 아래 §9.  M32R-01–06 · M32RF-01의 문서 범위 수용이며 verified/closed 자동 승격이나 실제 실행 승인은 아니다.

**한 줄로**: 3D 를 새로 짜기 전에 값싼 2D 대조로 접촉 표현을 바꿀 때 응답이 얼마나 달라지는지 가른다.  같은 코드 · 재료 · 출발 충전에서 속도장 하나와 입자별 장을 견주고, 그 조건부 결과로 3D 의 다음 길을 정한다.  2D 차이를 3D 연화의 원인 증명으로 쓰지 않는다.

## 1. 왜 이 질문부터인가

- 이 트랙은 DEM 으로 느슨한 초기 충전을 만들고, 가압부터 탈압까지 AM 과 SE 를 한 모델로 계산하려는 재설계다.  이미 눌린 DEM 끝 상태를 MPM 에 넘기는 기존 계산과 구분한다.
- 현재 MPM 에서는 AM 이 얼려져 있고 판 접촉은 양방향이며, SE 는 속도장 하나를 쓴다.  움직임 · 미끄럼 · 분리 표현이 제한되어 있다.  얼린 AM 에도 반력이 생길 수 있으므로 하중이 0 이라고 쓰지 않는다.
- SE 를 15–18 배 무르게 둔 기존 보정이 접촉 표현의 제한과 관련되는지는 가설이다.  구성식과 접촉은 서로 영향을 주므로 하나의 원인으로 단정하지 않는다.
- 먼저 등록한 2D 조건에서 응답 차이를 보고, 수치 오차 추정의 가정과 보류 이유까지 같이 적는다.  숨은 느린 수렴이나 복합 오차를 모두 막는 보편 수렴 보증은 없다 (DRD-01).

## 2. 논문 일곱 편이 계획의 어디에 들어갔나

| 논문 | 보여 준 것 | 계획에 들어간 자리 | 한계 |
|---|---|---|---|
| [1] Bardenhagen 2000 | 입자마다 속도장을 분리하는 접촉 표현 | 후보 A′ 의 바탕과 격자 해상도 시험 | 해당 2D 탄성 문제의 결과를 조밀 소성 전체의 자격으로 쓰지 않음 |
| [2] Bardenhagen 2001 | 수직 견인력을 이용한 분리 판정과 3D 구 검증 | AM · 판 · 벽 접촉 부품 A′-0와 단위 시험 | 다른 재료 · 소성 계면의 자격은 별도 |
| [3] Nezamabadi 2022 | 입자별 격자 MPM 과 접촉 풀이로 소성 원판 압밀 | 단계 3a의 문헌 대조 | 2D · 재료와 하중 경로가 우리 3D 전극과 다름 |
| [4] Nguyen 2017 | 기공률 곡선만으로 방법 차이를 가르기 어려움 | 같은 충전율에서 판 응력을 비교하고 마찰 팔을 분리 | 학회 단편 · MPM 쪽은 탄성 |
| [5] Cárdenas-Barrantes 2020 | 움직이는 단단한 입자와 무른 입자의 혼합 압밀 | AM 운동 · 하중 몫, 3b 및 상자 단위 시험 | 2D · 초탄성 · 하중 쪽 |
| [6] Cárdenas-Barrantes 2021 | 출발 충전과 배위수 기록 | 출발 상태를 결과 전에 고정 | 학회 단편 |
| [7] Cárdenas-Barrantes 2022 | 느슨한 출발의 2D 실험과 압밀 법칙 대조 | 3b 정합과 공통 관측량 | kPa · 2D · 초탄성 |

메모 3.2는 이 일곱 편 외에 정본 카드와 측정 상태를 더 검토했다.  아래 참고문헌 열 편은 이 브리핑에 직접 쓰는 발췌 목록이며 전체 인용은 메모 부록 B·C를 따른다.  문헌 숫자를 3D 로 옮기거나 문헌 정합을 실제 전극 자격으로 바꾸지 않는다.

## 3. 단계

- **단계 0 등록** (런 0): 관측량 · 충전 ID · 수치 선택 · 문턱 · 판정선 · 실패와 결측 처리 · 검정력 표를 결과 전에 고정한다.  메모의 수치 초안만으로 등록이나 실행 승인이 생기지 않는다.
- **단계 1 셈** (CPU · 추정): 입자별 장의 메모리와 색칠 안전 조건을 센다.  실제 값과 현장 자격은 별도 승인 뒤 확인한다.
- **단계 2 준비** (CPU · 추정): 같은 2D 코드의 S는 속도장 하나, F는 입자별 장이다.  단계 3의 S와 F 모두 일방향 판을 쓴다.  U0 · U1 · U2 · U5 · U6 · U7 · U8 통과가 다음 단계의 문이다.  조밀 접촉 U6(c)는 U5(c)의 여덟 의무를 포함한다.  위반이면 단계 3과 3D F 판정을 중단하며, 필수 등록·관측 누락도 보류다.
- **단계 3 2D 벤치마크** (CPU · 핵심): 같은 출발 충전 · 재료 · 속도에서 S/F(마찰 0.5) 판 응력 비를 본다.  F(마찰 0)는 문헌 정합에 쓴다.  격자 사다리에서 팔별 수치 오차 구간을 추정하고 충전·점·시험 순서로 집계한다.  단순히 평균이 1.3 배를 넘는지만으로 판정하지 않는다.  상한 중단으로 목표점에 못 닿으면 목표점 응력은 미확정이고 cap은 한쪽 경계를 만들지 않는다.  그 점은 중간, 해당 F 띠 점은 미정이다.  다른 점의 독립 경보와 기술 실패는 유지한다.
- **단계 4 3D 순수 SE** (Rint ② R 런 뒤): 느슨한 충전 · 질량 보존 심기에서 실제 강성과 연화 팔을 견주고 σ_y 하나를 랩 기준에 맞춘다.  0.03–0.60 GPa 탐색, 최종 50 × 50 × 30 µm 상자와 충전 셋은 메모의 등록 전 안이다.  F 대조를 열 조건과 자격을 따로 지킨다.  줄인 상자의 필수 비교 명부에서 결측·실패를 제외하지 않는다.  F-비교미확정이면 F 채택과 수치 상자 효과 판정을 막고 메모의 기존 맥락별 처분을 따른다.
- **단계 5 3D 복합** (별도 자격 뒤): 움직이는 AM 과 SE 를 함께 계산한다.  복합 기공률은 추가로 맞추지 않고 예측으로 보고한다.
- **단계 6 탈압** (별도 자격 뒤): U3 · U4 등 등록된 분리·탈압 자격 뒤 보고한다.  현재 MPM의 O7 표지는 명시적 분리 법칙 없음이다.  이것을 모든 되돌아옴이 0 이라는 뜻으로 쓰지 않는다.
- **단계 7 구조 · 수송** (앞 단계 뒤): 구조·접촉·수송의 공통 정의와 등록 자격을 확인한 뒤 연결한다.
- **일정** [추정]: 2D 4–6 주 · 단계 3 결과 12 월 중순–말 · 3D 는 R 런 뒤라는 기존 어림을 보존한다.  착수일과 완료일 확정이나 실행 GO 가 아니다.

**갈림 (결과 전에 정함)**

| 2D 결과 | 3D 길 |
|---|---|
| (가) 같음 | 등록한 2D 조건에서의 조건부 같음.  A (움직이는 강체 AM) + A′-0로 시작하고 필요 조건에서 F 대조를 연다.  3D 원인 부정 아님 |
| (나) 다름 | 등록한 2D 조건에서의 응답 차이.  A′ (입자별 장) 방향을 택하되 비용·접촉 자격을 별도로 확인.  3D 원인 증명 아님 |
| (마) 못 가름 | 수치 구간·정합이 미정인 경우를 포함.  차이가 없다는 결론 없이 A + A′-0로 가되 F 대조 조건과 보류를 유지 |
| (라) 이상 신호 | 구현 조사 경보.  결함을 고친 뒤 문을 다시 통과해 허용된 한 번 재시도.  결함 미확인 또는 반복 경보면 판정 없이 중단·보고 |
| (다) MPM 길 멈춤 | 2D 단계에서 자동 선택하지 않음.  3D 결과와 1저자 판단 뒤 후보 B 또는 C′ 등을 검토 |

## 4. 진밀도 1.64 에서 기공률 10–13 %

- 랩 표준은 순수 SE · 진밀도 1.64 g/cm³ · 질량 기준 기공률 10–13 %다.  1.64 는 고정이고 손잡이가 아니다.
- MPM 은 느슨한 충전에서 고체량을 보존해 심고, 등록한 기공 연산자와 상태로 비교한다.  압력 상태를 섞어 수치를 맞추지 않는다.
- 단계 4의 적합 손잡이는 σ_y 하나다.  가운데 11.5 %를 목표로 하는 탐색과 자격을 통과해야 하며, 창에 닿음 자체는 물리 검증이 아니다.
- 비교 상태는 300 MPa 가압 뒤 판 고정 이완 끝이다.  랩 측정 상태의 남은 한정도 메모 §8대로 보존한다.
- 복합은 이 기준에 다시 맞추지 않는다.  DEM 세대 2와 MPM도 각각 같은 외부 기준에 따로 맞추고 서로를 맞춤 대상으로 쓰지 않는다.
- 바닥 모델 M0도 적합 1 + 사전 고정 2다.  맞출 변수와 나머지 값·출처는 등록 전 미정이며, 출처 없는 고정 선택은 별도 계상한다.  목록이 비면 비교 실행을 열지 않는다.

## 5. 브리핑하다 찾은 빈 곳

메모 3.1은 LPSCl 대조 자료를 놓쳤다 (`SELF-161`).  당시의 "항복·경도 카드가 없다"와 "외부 기준은 점 하나"는 둘 다 틀렸다.  메모 3.2에서는 보정 기준 하나와 보정에 쓰지 않는 문헌 대조를 나누었다.

- [8] Lee 2025는 연속 가압 자료다.  절대 기공률을 랩 값에 섞지 않고, 현재 D2는 같은 곡선의 h150/h300 두께 비를 대조한다.  종전 Heckel 기울기 비교는 철회했다.  다이·벽·속도 한정은 남는다.
- [9] Miß 2026은 조성과 압력 이력이 다르다.  D3 회복 대조의 상태와 탄성 기준을 함께 적으며, 입자 기구 검증으로 확대하지 않는다.
- [10] Thompson 2026의 격자 탄성 자료는 분말 덩어리의 체적 강성이나 무하중 회복 자료가 아니다.
- LA25의 두께는 약 6 시간의 운전압 시험/사다리 뒤 Cu 포일 제거 후 읽은 상태다.  최대 8 MPa EIS 사다리는 카드 해석이다.  그 상태를 압밀 직후 값으로 옮기지 않는다 (메모 §4-1 · M32R-06).
- 문헌 대조는 랩 표준과 다른 문헌 값으로 보고한다.  자료가 늘었다고 독립 검증 점이나 보정 자유도를 자동으로 늘리지 않는다.

## 6. 하지 않는 말

- 기공률이 창에 들었다는 것만으로 모델이 맞다고 하지 않는다.
- 2D 숫자를 3D 로 옮기지 않는다.
- 조건부 응답 차이를 "붙음이 3D 연화의 주원인"이라고 하지 않는다.  못 가름을 같음으로 바꾸지 않는다.
- 탈압 값은 U3 · U4 등 실제 자격 전에 내지 않는다.  DEM의 되돌아옴을 MPM 값으로 쓰지 않는다.
- 상한에 닿았다는 사실을 목표점 응력의 하한으로 쓰지 않는다.  결측을 빼서 F 비교를 완성하지 않는다.
- 우리 σ_y를 문헌 항복과 그대로 견주지 않는다.  일축 환산과 부호·구성식의 차이를 밝힌다 (`SELF-160`).

## 7. 더 먹여 주면 좋은 문헌 (계획에 바로 쓰이는 순)

1. 복합 펠릿의 압력별 질량 기준 기공과 측정 상태.  단계 5 외부 대조에 필요한 조건을 먼저 등록한다.
2. 3D 입자별 장·다물체 접촉·입자별 FE의 자격과 비용.  기존 정본 카드 목록은 메모 부록 B·C를 따른다.
3. LPSCl 소성·크리프·경도와 가압·탈압 이력.  다른 조성·진밀도·측정 상태를 한 기준처럼 묶지 않는다.
4. 냉간 가압 복합 양극의 단면 형상 정량.  SE 형태와 입자 수준 주장을 가를 관측량을 결과 전에 정한다.

이번 반영은 새 검색·원자료 열람 없이 고정 메모와 독립 판정만 옮겼다.

## 8. 1저자 결정 (11-10 기록 유지)

- **Q1.** 단계 0–3 을 GPU 없이 시작하고 3D 는 Rint ② R 런 뒤로 둘까요?  권고: 예.  답: 권고대로 (순서 결정 · 실제 실행 승인과 별개).
- **Q2.** SE 입자 형태 변형은 필수인가요?  권고: 필수.  답: 권고대로 (필수).
- **Q3.** `SELF-160` 은 문구만 고칠까요?  권고: 예.  답: 권고대로 (재실행 없음).
- **Q4.** 메모 3.2 반영 시점은 언제인가요?  권고: 판정 지적과 문헌 대조를 함께 반영.  답: 3.1 발송 뒤 3.2 반영 · 11-13 M32R-01–06 및 M32RF-01 문서 범위 종결 가능 수용.  실제 수치·등록 승인으로 확대하지 않음.
- **Q5.** 복합 기공도 10–13 % 에 맞추나요?  권고: 아니오.  답: 순수 SE만 기준 · 복합은 예측 (11-10 결정 유지).

## 9. Codex 반박 판정과 남은 것 (11-13)

최신 수령은 `docs/reviews/memo32_closure_20261113/README.md`, 원 판정 이력은 `docs/reviews/memo32_fixes_20261113/README.md` 와 `docs/reviews/memo32_rule38_20261113/README.md` 다.  메모 머리의 재확인 대기 문장은 고정 핀의 이력이고 최신 판정은 이 수령 기록을 따른다.

- **판정**: M32R-01–06 및 M32RF-01은 문서 범위 종결 가능이다.  새 P1/P2/P3는 없다.  전체 HOLD 다.  verified/closed 자동 승격이나 실행 승인은 아니다.
- **원 큰 지적의 한정 (P1)**
  - `DRD-01` 보편 수렴과 물리 자격은 남는다.  고침: 수치 오차 구간은 가정 아래의 추정이며 숨은 느린 항과 복합 오차를 모두 막지 못한다.
  - `DRD-02` 2D 응답 차이는 3D 인과 결론이 아니다.  고침: 등록한 2D 조건으로 결론을 좁히고 3D 재대조 조건을 남겼다.  원 지적 문서 범위 수용을 물리 검증으로 확대하지 않는다.
- **다른 DRD의 구분**
  - `DRD-03` · `DRD-04` · `DRD-05` · `DRD-06` · `DRD-07` · `DRD-09` · `DRD-13`은 DRD-02와 함께 원 재리뷰의 문서 범위 종결 가능 8건이다.
  - `DRD-08` · `DRD-10` · `DRD-11` · `DRD-12` 및 DRD-01 · `SELF-161`의 남은 한정은 그대로다.  새 여섯 수정의 수용이 원 항목 전체를 닫지 않는다.
- **독립 확인**: 메모 1231행 중 §6 38번 한 행 정정, 같은 문서 회귀 15개는 수정 전 1실패에서 15/15로, 원 탐침은 rc1에서 rc0로 확인됐다.  소형 문서·산술 검사이며 연구 실행 결과가 아니다.
- **남은 순서**: 등록·수치 선택·물리 자격·운영 봉인·실행 GO를 각 절차로 받는다.  이번 페이지와 DOCX 갱신은 전달 문서 반영이다.

## 참고문헌

서지는 litdb 정본 가지 (`claude/friendly-meitner-lldvar`) 의 카드에서 옮겼다.  [1]–[7] = 1저자가 11-09 에 준 PDF · [8]–[10] = 이미 정본에 있던 카드.

| # | 서지 | litdb 카드 (slug) |
|---|---|---|
| 1 | S.G. Bardenhagen, J.U. Brackbill, D. Sulsky, The material-point method for granular materials, Comput. Methods Appl. Mech. Engrg. 187 (2000) 529–541.  DOI 미인쇄 | `bardenhagen2000_mpm_granular_multibody_frictional_contact` |
| 2 | S.G. Bardenhagen, J.E. Guilkey, K.M. Roessig, J.U. Brackbill, W.M. Witzel, J.C. Foster, An improved contact algorithm for the material point method and application to stress propagation in granular material, CMES 2(4) (2001) 509–522.  DOI 미인쇄 | `bardenhagen2001_mpm_improved_contact_granular_stress_waves` |
| 3 | S. Nezamabadi, M. Ghadiri, J.-Y. Delenne, F. Radjai, Modelling the compaction of plastic particle packings, Comput. Part. Mech. 9(1) (2022) 45–52.  doi:10.1007/s40571-021-00391-4 | `nezamabadi2022_mpm_cd_plastic_particle_compaction` |
| 4 | T.H. Nguyen, S. Nezamabadi, J.-Y. Delenne, F. Radjai, Compaction of granular materials composed of deformable particles, EPJ Web Conf. 140 (2017) 05013.  doi:10.1051/epjconf/201714005013 | `nguyen2017_mpm_bpm_deformable_particle_compaction` |
| 5 | M. Cárdenas-Barrantes, D. Cantor, J. Barés, M. Renouf, E. Azéma, Compaction of mixtures of rigid and highly deformable particles: A micromechanical model, Phys. Rev. E 102 (2020) 032904.  doi:10.1103/PhysRevE.102.032904 | `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` |
| 6 | M. Cárdenas-Barrantes, D. Cantor, J. Barés, M. Renouf, E. Azéma, A micro-mechanical compaction model for granular mix of soft and rigid particles, EPJ Web Conf. 249 (2021) 02008.  doi:10.1051/epjconf/202124902008 | `cardenasbarrantes2021_soft_rigid_mix_compaction_proceedings` |
| 7 | M. Cárdenas-Barrantes, J. Barés, M. Renouf, É. Azéma, Experimental validation of a micromechanically based compaction law for mixtures of soft and hard grains, Phys. Rev. E 106 (2022) L022901.  doi:10.1103/PhysRevE.106.L022901 | `cardenasbarrantes2022_soft_hard_grains_compaction_experiment_dic` |
| 8 | S.-Y. Lee, J.-H. Han, H.-W. Gong, J.-p. Ahn, K.-W. Yi, Y.W. Cho, Characterization of densification behavior and mechanical properties of solid electrolyte powders for all solid-state batteries, J. Mater. Chem. A 13 (2025) 6342–6346.  doi:10.1039/d4ta08604j | `lee2025_heckel_argyrodite_powder_densification_nanoindentation` |
| 9 | V. Miß, F. Lange, S. Staubitz, B. Roling, Experimental setup for in situ determination of conductivity-porosity-pressure relationships, ACS Appl. Mater. Interfaces 18 (2026) 32830–32836.  doi:10.1021/acsami.6c03789 | `miss2026_insitu_conductivity_porosity_pressure_compaction` |
| 10 | O. Thompson, O. Korjus 외, High Pressure Densification Investigation of Li3PS4 and Li6PS5Cl Solid Electrolytes using Combine X-Ray Diffraction, X-Ray Absorption Tomography and Ionic Measurement (카드 PDF 파일 이름의 제목 · 원문 제목 대조 미확인), Adv. Funct. Mater. 36 (2026) e75195.  doi:10.1002/adfm.75195 | `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` |
