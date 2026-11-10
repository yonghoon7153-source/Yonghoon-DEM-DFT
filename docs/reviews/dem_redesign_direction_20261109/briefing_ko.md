<!-- BRIEFING:UPDATED 2026-11-10 -->
# [DEM 우선 (수영)] 재설계 계획 브리핑 (쉬운 말 · 논문 기준)

**지위**: 1저자용 브리핑 · 방향 메모 3.1 판 (`docs/reviews/dem_redesign_direction_20261109/memo_v3_1.md`) 을 쉬운 말로 옮긴 것 · 결과 0 건 · 새 계산 0 건 · 실행 GO 요청 아님.  정본은 메모이고, 이 문서와 메모가 다르면 메모가 이긴다.  Codex 반박 리뷰 요청 = `docs/reviews/codex_dem_redesign_direction_request_20261109.md` (리뷰 핀 `13eb293cd` · 1저자 11-10 발송 · 판정 11-10 = 방향 지지 · 규칙 수정 필요 (HOLD) · 아래 §9).

**한 줄로**: 3D 를 새로 짜기 전에 값싼 2D 시험으로 하나를 먼저 가른다.  우리 MPM 에서 알갱이가 닿으면 붙어 버리는 것, 곧 속도장이 하나뿐인 것이 문제의 뿌리인가.  그 답으로 3D 를 어떻게 짤지 정한다.

## 1. 왜 이 질문부터인가

- 1저자가 정한 조건 셋 (느슨한 상태 출발 · 질량 보존 심기 · MPM 기공률이 주 출력) 은 순수 SE 만이면 지금 코드도 대체로 지킨다.
- 막히는 곳은 AM 이 섞인 복합과 탈압이다.  코드를 읽으면 이유가 하나로 모인다 (`scripts/mpm3d_compaction.py` · 메모 §2).
  - 얼린 AM 칸은 속도가 0 이라 SE 가 AM 에 모든 방향으로 붙는다.
  - 판은 위아래로 붙어 있어서 하중을 빼도 침대가 판에서 떨어지지 못한다.
  - SE 알갱이끼리는 속도장이 하나라 닿는 순간 한 덩어리가 된다.  미끄럼도 떨어짐도 없다.
- 가설: 이 붙음 때문에 강성을 15–18 배 낮추는 연화가 필요했고, 느슨한 출발에서 재배열도 막혔다.  아직 시험 전이라 먼저 가른다.

## 2. 논문 일곱 편이 계획의 어디에 들어갔나

| 논문 | 보여 준 것 | 계획에 들어간 자리 | 한계 |
|---|---|---|---|
| [1] Bardenhagen 2000 | 알갱이마다 속도장을 따로 두면 겹치지 않고 미끄러지고 떨어진다.  속도장 하나 (우리 코드) 는 그 논문의 미끄럼 없음 대조군과 같다 | 후보 A′ (입자별 장) 의 알고리즘.  장을 통째로 두면 우리 규모에서 약 30 TB 라 색칠 · 희소 슬롯이 필요하다 (단계 1 의 셈).  지름당 8 셀 이상 필요하고 4 셀이면 못 구른다 | 2D · 탄성 |
| [2] Bardenhagen 2001 | 떨어짐 판정을 수직 견인력으로 고쳤다 · 작은 질량 안정화 γ 0.5 · 3D 구 검증 | 탈압용 부품 A′-0 (AM · 판 · 벽에만 마찰과 분리 규칙).  탈압 단위 시험 U3 · U4.  인쇄된 식 (22) 의 max 는 min 으로 구현 | 저자 스스로 다른 재료 · 소성 계면에서는 안 맞는다고 적었다.  그래서 시험 통과 전에는 탈압 값을 내지 않는다 |
| [3] Nezamabadi 2022 | 입자마다 격자를 둔 MPM 과 접촉 풀이로 소성 원판을 연화 없이 충전율 0.99 까지 눌렀다 | "접촉을 풀면 연화가 필요 없을 수 있다" 는 가설의 근거.  2D 시험 3a 의 대조 띠 (응력이 논문 곡선의 0.7–1.4 배 안) | 2D · 재료가 항복에 비해 무르다 (E/σ_y 25 · LPSCl 약 60–74) |
| [4] Nguyen 2017 | 기공률 곡선은 방법이 달라도 비슷하게 나온다 · 마찰 0 과 0.5 비교 | 판정을 기공률이 아니라 같은 충전율의 판 응력 비로 한다.  마찰 팔 둘과 마찰 경보 | 학회 4 쪽 · MPM 쪽은 탄성뿐 |
| [5] Cárdenas-Barrantes 2020 | 단단한 입자와 무른 입자 혼합에서 기공 바닥은 단단한 입자가 움직이고 서로 닿아 하중을 받을 때 생긴다 · 입자 하나 상자 법칙 | 조건 R1 (AM 이 움직이고 하중 몫 f 를 계산).  2D 시험 3b (느슨한 출발 혼합).  단위 시험 U1.  후보 B (입자별 FE) 의 실례와 비용 | 2D · 초탄성 · 하중 쪽만 |
| [6] Cárdenas-Barrantes 2021 | 출발 상태 표 (φ0 · Z0) | 출발 충전을 결과 전에 고정하고 기록하는 규칙 | 학회 단편 |
| [7] Cárdenas-Barrantes 2022 | 2D 실험 (DIC) 으로 느슨하게 시작해 재밍을 관측하며 압밀 법칙을 검증했다 | 1저자 결정 (느슨한 출발) 과 같은 절차.  3b 대조 띠.  배위수 · 접촉 길이 같은 공통 관측량 | kPa · 2D · 초탄성 |

다섯 편이 같은 곳 (붙음) 을 가리키지만 모두 2D 라 가설의 근거이지 증거가 아니다.  그래서 2D 숫자는 3D 로 옮기지 않고, "접촉 표현이 원인인가" 판정에만 쓴다.

## 3. 단계

- **단계 0 등록** (런 0): 기공 세는 식 · 관측량 · 충전 수 · 문턱 · 갈림 표를 결과 전에 적어 둔다.
- **단계 1 셈** (CPU 며칠): 입자별 장을 3D 에 넣을 때 장이 몇 개, 메모리가 얼마인지 real_14 의 수 · 반경으로 센다.
- **단계 2 준비** (CPU 3–4 주): 2D 코드 하나에 S (지금처럼 속도장 하나) 와 F (입자별 장) 를 같이 넣는다.  단위 시험 U0 (색 하나면 S 와 비트까지 같음) · U1 (입자 하나 상자) · U2 (Bardenhagen 재현) · U5 (원판 충돌 · 세 원판 모서리) · U6 (이른 접촉 격자 사다리) 통과가 다음 단계의 문이다.
- **단계 3 2D 벤치마크** (CPU 1–2 주 · 핵심): 같은 코드 · 같은 출발 충전 셋 · 같은 재료 · 같은 판 속도에서 접촉 표현만 바꾼다.  같은 충전율에서 S 의 판 응력이 F (마찰 0.5) 의 몇 배인가로 가른다.  점은 셋 (재밍 근처 하나 · 치밀 둘) 이고, "다름" 은 평균 1.3 배 이상인 점이 둘 이상일 때만이다.
- **단계 4 3D 순수 SE** (Rint ② R 런 뒤 · 48 GB 카드): 느슨하게 붓고 질량을 다 심는다.  연화 팔 (E 1.53 · ν 0.49) 과 실제 팔 (E 22.06 · ν 0.36) 을 같이 돌리고 손잡이는 σ_y 하나다.  0.03–0.60 GPa 를 훑어 기공 11.5 % 가 되는 σ_y* 를 찾는다.  최종값은 50 × 50 × 30 µm 상자 · 충전 셋 평균이다.  결과는 넷 중 하나다 (실제 강성으로도 닿음 · 연화가 필요 · 둘 다 못 닿음 · 보류).
- **단계 5 3D 복합**: 줄인 입경비 상자 다음 real_14 의 수 · 반경 (위치는 새로 붓기).
- **단계 6 탈압**: U3 · U4 통과 뒤 · 보고만.
- **단계 7 구조 · 수송**.
- **일정** [추정]: 2D 4–6 주를 CPU 로 (Rint 일정 그대로) · 단계 3 결과 12 월 중순–말 · 3D 는 R 런 뒤.

**갈림 (결과 전에 정함)**

| 2D 결과 | 3D 길 |
|---|---|
| (가) 같음 | 붙음은 주원인 아님.  3D = A (AM 을 움직이는 강체로 + 부품 A′-0) |
| (나) 다름 | 붙음이 주원인.  3D = A′ (입자별 장) |
| (마) 못 가름 | A 로 가되 A′ 는 보류.  단계 4 에서 다시 열 수 있다 |
| (라) 이상 신호 | 마찰 없는 F 가 논문 띠 밖 · S 가 더 무름 · 마찰을 넣었는데 더 무름 · 기술 실패.  구현부터 의심하고 한 번 다시, 그래도면 멈추고 보고 |
| (다) MPM 길 멈춤 | 입자별 FE (B) 또는 두 재료 항복캡 DEM (C′).  단계 3 에서는 나오지 않는다 |

## 4. 진밀도 1.64 에서 기공률 10–13 %

1저자 11-10: *"이것도 진밀도 1.64에 porosity가 저 범위에 있어야돼"*.  메모에 이미 들어 있다.

- MPM 기공률 = 1 − (처음 심은 고체 부피 합) ÷ (바닥 넓이 × 판 높이).  코드 안 밀도가 1 이라 그 고체 부피가 곧 "질량 ÷ 진밀도" 다.  랩의 질량 기준 · 진밀도 1.64 기공률과 같은 정의다 (메모 단계 0).
- 단계 4 가 바로 그 맞춤이다.  σ_y 하나로 10–13 % (가운데 11.5 %) 에 넣고 그 값을 뒤 단계에 그대로 쓴다.
- 1.64 는 고정이고 손잡이가 아니다.  계산에 직접 들어가는 곳은 복합의 wt% 를 부피로 바꿀 때 (SE 1.64 · AM 4.85) 다.
- 비교 상태는 [DEM 우선] 의 D9′ 와 같은 "300 MPa 가압 뒤 판 고정 이완 끝" 이다.
- 결과 문장은 "진밀도 1.64 로 정의한 랩 기준과 맞는다" 까지다.
- 복합은 지금 설계에서 10–13 % 를 맞추지 않고 예측으로 낸다.  기준이 순수 SE 이고 손잡이가 σ_y 하나라, 복합까지 맞추면 맞춘 값이 둘이 된다 (아래 Q5).

## 5. 브리핑하다 찾은 빈 곳

메모가 litdb 정본에 이미 있는 LPSCl 카드를 쓰지 않았고, 사전 공격 세 번도 놓쳤다 (원장 `SELF-161`).

- [8] Lee 2025: 상용 Li6PS5Cl 을 다이 안에서 연속으로 누르며 압력별 기공 곡선 전체를 냈다.  진밀도를 1.64 로 둔 논문이다.  300 MPa 누른 채 약 15 % [카드 판독] · Heckel 항복압 약 0.29–0.34 GPa [카드 산술] · 나노압입 E 27.6 GPa · 경도 1.41 GPa · 약 900 MPa 에서 뺐을 때 높이 약 4.7 % 회복.
- [9] Miß 2026: 300 MPa 에서 뺐을 때 SE 두께 회복 1.6 % [카드 재계산].
- [10] Thompson 2026: 3.8 GPa 까지 가압 · 격자로 본 체적 탄성률 약 22.9 GPa [카드 산술] (우리 DFT 26.23 과 비슷).
- 왜 중요한가: 메모는 "σ_y* 를 견줄 LPSCl 항복 · 경도 카드가 없다", "외부 기준은 점 하나" 라고 적었다.  둘 다 틀렸다.  보정은 그대로 랩 기준 하나로 하고, 이 카드들은 결과 전에 등록하는 대조 항목 (σ_y* 비교 · 압력별 곡선 모양 · 탈압 크기) 으로 넣으면 된다.
- 처분: 1저자 11-10 메모 3.1 을 그대로 Codex 반박 창에 보냈다.  3.2 는 판정을 받은 뒤 이 대조 항목 · 참고문헌 목록과 판정 지적을 함께 반영한다.  기준 · 손잡이 · 갈림 표는 그대로다 (Q4).

## 6. 하지 않는 말

- 기공률이 창에 들었다는 것만으로 모델이 맞다고 하지 않는다.  손잡이 하나로 점 하나는 늘 맞는다.
- 2D 숫자를 3D 로 옮기지 않는다.
- "연화는 피할 수 없다" 는 한 속도장 MPM 의 구성식 탐색 결론으로만 쓴다.
- 탈압 값은 U3 · U4 통과 전에 내지 않는다.  15.6 % 는 DEM 값이다.
- 2D 에서 같음이 나와도 3D 에서 붙음이 원인이 아니라고 하지 않는다 (Codex `DRD-02`).
- 우리 σ_y 를 문헌 항복과 그대로 견주지 않는다.  σ_y 0.30 이면 연화 재료의 일축 항복은 압축 0.318 · 인장 0.454 GPa 다 (`SELF-160`).

## 7. 더 먹여 주면 좋은 문헌 (계획에 바로 쓰이는 순)

1. **NCM + LPSCl 복합 펠릿의 압력별 기공 (질량 기준)** 이 있는 논문이나 랩 자료.  단계 5 에 외부 기준이 생겨 판정을 하나 더할 수 있다.  가장 값지다.
2. **카드가 직접 확보 후보로 적은 것** (서지 = 카드에 인쇄된 참고문헌): Cantor et al., PRL 124, 208003 (2020) · 같은 그룹 3D 판 Soft Matter 18, 312 (2022) (후보 B 의 3D 비용을 알려 줄 1 순위) · PRE 103, 062902 (2021) · Barés et al., EPJ Web Conf. 249, 05004 (2021) · Vu and Barés, PRE 100, 042907 (2019) · Cárdenas-Barrantes 2022 보충 자료.
3. **우리 코드 계보 (MLS-MPM) 의 강체 양방향 결합 · 접촉**: 검색 낱말 "moving least squares material point method two-way rigid body coupling" · "material point method frictional contact multi-material".  후보 A 의 강체 결합과 노드당 셋 이상 처리에 바로 쓰인다.
4. **LPSCl 소성 · 크리프 · 나노압입**: 검색 낱말 "Li6PS5Cl nanoindentation hardness creep" · "argyrodite micropillar compression".
5. **냉간 가압 복합 양극 단면 형상 정량** (SE 형상 비교): 검색 낱말 "FIB-SEM cold-pressed composite cathode Li6PS5Cl morphology".

3–5 번의 저자 · 서지는 원문을 받기 전까지 확정하지 않는다.

## 8. 1저자 결정 (11-10)

- **Q1.** 단계 0–3 을 GPU 없이 시작하고 3D 는 Rint ② R 런 뒤로 둘까요?  권고: 예.  답: 권고대로 (예).
- **Q2.** SE 입자 형태 변형은 필수인가요?  권고: 필수.  답: 권고대로 (필수).
- **Q3.** `SELF-160` (σ_y 환산 오기) 은 문구만 고칠까요 (재실행 없음)?  권고: 예.  답: 권고대로 (문구만 · 재실행 없음).
- **Q4.** Codex 에 보내기 전에 메모를 3.2 로 고칠까요 (§5 의 카드를 대조 항목으로 등록 · 참고문헌 목록)?  권고: 고친 뒤 보낸다.  답: 3.1 그대로 보냄 (11-10) · 3.2 는 판정 뒤.
- **Q5.** 복합 기공도 10–13 % 에 맞춰야 하나요?  권고: 아니오.  복합은 예측으로 내고 D0 와 같은 식으로 비교한다.  답: 아니오.  기준은 순수 SE 만이고 복합 등 다른 것은 다른 값이 나와도 된다 (1저자 *"순수 SE만 기준이고 다른것들은 다른값 나와도 되지 당연히"*).

## 9. Codex 반박 판정 (11-10) 과 고칠 것

판정문 = `docs/reviews/codex_review_dem_redesign_direction_20261110.md` · 처분 = `docs/reviews/dem_redesign_direction_20261109/verdict_disposition_20261110.md`.

- **판정**: 방향은 지지한다.  다만 지금 적힌 판정 규칙 (단계 3 · 4) 은 고쳐야 해서 등록 · 봉인은 HOLD 다.  실행 GO 는 요청하지도 받지도 않았다.
- **큰 지적 둘 (P1)**
  - `DRD-01` 격자를 두 번 (지름당 12 · 16 셀) 돌려 등급이 같으면 확정한다는 규칙으로는 부족하다.  격자를 더 조이면 등급이 바뀌는 경우를 못 막는다 (합성 예: 12 셀 1.38 · 16 셀 1.31 로 둘 다 "다름" 인데 극한은 1.10 "같음").  고침: 응력 비의 수치 오차를 추정해 등급 경계와 견주고, 경계를 넘나들면 중간 · 보류로 둔다.
  - `DRD-02` 2D 에서 "같음" 이 나와도 3D 에서 붙음이 원인이 아니라고 할 수 없다.  재료식과 접촉은 서로 영향을 주기 때문이다.  고침: 결론을 "등록한 2D 조건에서 접촉 표현을 바꾸면 응답이 이만큼 달라진다" 로 좁히고, 3D 에서 실제 강성이 창에 못 닿으면 입자별 장 대조를 열지 정한다.
- **그 밖 (P2 열 · P3 하나)**
  - 논문 곡선과 견줄 때 충전율 정의를 하나로 고정한다 (`DRD-03`).
  - 단계 4 의 빈틈 셋을 메운다: 탐색이 전부 실패한 경우 · 자격에 쓸 충전 번호 · 다시 연 팔의 보류 조건 (`DRD-04` – `DRD-06`).
  - 누르는 중에도 접촉은 국소적으로 풀린다.  분리 · 마찰 검산 일부를 2D 벤치마크 앞으로 당긴다 (`DRD-07` · `DRD-08`).
  - 입자별 장의 색칠 안전 조건 · 후보별 맞춘 값 세기 · "얼린 AM 은 하중 0" 문장 · 작은 상자 자격의 범위를 고친다 (`DRD-09` – `DRD-12`).  Zunker 논문은 정식 출판본이 있다고 적는다 (`DRD-13`).
- **확인된 것**: 일축 항복 환산 네 값 · 2D 런 수 96 (넓히면 114) · 갈림 표 (상위 표 수준) · 새로 붓기와 질량 기준 연산자.
- **다음**: 메모 3.2 에서 위를 고치고 §5 의 대조 항목을 더한다.  고친 문서와 작은 결정 함수 · 합성 반례로 짧게 재확인받는다.  이 지적을 닫으려고 DEM · MPM 을 먼저 돌릴 필요는 없다 (판정문 §7).

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
| 8 | S.-Y. Lee, J.-H. Han, H.-W. Gong, J.-P. Ahn, K.-W. Yi, Y.W. Cho, Characterization of densification behavior and mechanical properties of solid electrolyte powders for all solid-state batteries, J. Mater. Chem. A 13 (2025) 6342–6346.  doi:10.1039/d4ta08604j | `lee2025_heckel_argyrodite_powder_densification_nanoindentation` |
| 9 | V. Miß, F. Lange, S. Staubitz, B. Roling, Experimental setup for in situ determination of conductivity-porosity-pressure relationships, ACS Appl. Mater. Interfaces 18 (2026) 32830–32836.  doi:10.1021/acsami.6c03789 | `miss2026_insitu_conductivity_porosity_pressure_compaction` |
| 10 | O. Thompson, O. Korjus 외, High pressure densification investigation of Li3PS4 and Li6PS5Cl solid electrolytes using combined X-ray diffraction, X-ray absorption tomography and ionic measurement, Adv. Funct. Mater. 36 (2026) e75195 | `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` |
