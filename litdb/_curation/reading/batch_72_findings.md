# batch 72 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer` — G. R. Chandratilleke, Y. C. Zhou, A. B. Yu, J. Bridgwater, "Effect of Blade Speed on Granular Flow and Mixing in a Cylindrical Mixer", *Ind. Eng. Chem. Res.* 49(11) (2010) 5467–5478, DOI 10.1021/ie901581t (후보 표 N-32 · 고른 의도 = e · k — chandratilleke2012 DEM 의 방법 원전: 힘 법칙 (Hertz · Mindlin 여부) · 감쇠 · 구름마찰 식 · 연화 영률이 어느 점접촉 법칙에 들어갔는지).
2 날개 수직 원통 믹서 (안지름 249 mm · 날 40 × 10 mm · 벽 · 바닥 틈 없음) 에 단분산 5 mm 유리 유사 구 16,000 개를 넣고 날 속도 2–100 rpm 에서 흐름 · 배위수 · 공극 · Lacey 지수 · 힘 망 · 접촉력 분포 · 토크를 본 3D DEM — 비점착 · 압축 · 탈압 없음 · 실험 값 없음 (검증은 선행 PEPT).
쪽 = 학술지 쪽 (PDF 1–12 = 5467–5478) · SI 없음.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE 없음 · 압축 없음).  참고 (a 아님): 정지 침대 (바닥 – 날 윗변 슬랩) 공극 ≈ 0.45 · 흐르는 침대 0.539 (2 rpm) → 0.632 (100 rpm) [판독 Fig 4] — 단분산 mm 유리 유사 구의 고정 슬랩 값 (날 뒤 빈 곳 포함) · 랩 기준 (순수 SE 10–13 %) 과 견줄 수 없다 (카드 §7-2).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 압축 · 하중 제거 계산이 없다 (날 회전 혼합만 · 카드 §4-6 (iv)).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 탄성 (Hertz 꼴) + 점성 감쇠 + 마찰 (μ_s 0.3) + 구름 (μ_r 5 × 10⁻⁵ m) 뿐 · 항복 · 경도 · 크리프 정의 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (한 재료 · 단분산 · 색만 다른 두 무리).  참고 (d 아님): 큰 법선력 (0.1–0.3 N) 은 앞 날 · 벽 · 바닥 모서리에 모이고 100 rpm 에서 벽 쪽으로 옮겨 간다 (p.5474–5475 · Fig 10 · 11).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer | 깨지는 범위 · 대안 = **없음** (흐름 영역만).  쓴 점접촉 법칙 = Table 1: 법선 F_cn = −E/(3(1−ν²))(2R_i)^{1/2}δ_n^{3/2}n̂ (같은 크기 두 구 Hertz 꼴 · (4/3)E*√R* 와 계수 55,947 N m^{−3/2} 로 같음) · 접선 = μ_s F_cn [1 − (1 − min(δ_t, δ_t,max)/δ_t,max)^{3/2}] (Mindlin–Deresiewicz 꼴 · δ_t,max = 0.364 δ_n) · 감쇠 ∝ δ_n^{1/4} · 구름 = −μ_r F_cn ω̂_i (방향 일정 · ai2011 A 부류 꼴) · 맞춘 값 0 (모두 지정값 · *"commonly used as discussed in the recent review ... 13"*) | 카드 §3-2 · §0-1 · Table 1 p.5468 · 크롭 `eq_t1a` … `eq_t1f` | [인쇄] · [카드 산술] · [카드 대조] | 'Hertz' · 'Mindlin' 낱말은 원문에 없다 (꼴 대조) · 벽 접촉 · 크기 다른 쌍의 R [미확인]
- [e] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer | 이 법칙이 쓰인 변형 크기: 연화 E 에서 평균 법선력 0.0137–0.0222 N → 겹침 0.78–1.08 % d · 99 % 분위 0.101–0.159 N → 3.0–4.0 % d · 최대 0.3 N → 6.1 % d (5 % 간격 판정 거리보다 큼) · E = 10⁹ 이면 같은 힘에서 ÷59.9 | 카드 §3-9 ② · Fig 12 | [카드 산술 · 판독 힘] | 큰 변형 · 고밀도 압밀과 무관한 흐름 값

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (MPM 아님).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 3D DEM 만 · 2D → 3D 전이 말 없음 ('three dimensional' = 입체각 최대 이웃 수 14 문장 · 결론 (b) 의 '3 차원 소용돌이' 뿐 · p.5472 · 5476).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer | 저자 한계 · 미래: *"Many of the effects due to particle size and cohesive force will also become equally accessible"* (결론 (f) p.5477 = 크기 · 점착은 앞으로) · 연화 E 가 접촉 비를 바꿨을 것이라는 고백 (p.5473) · Knight 토크 모델은 *"does not account for the particle size"* 라 적용 불가 (p.5476) | 카드 §4-6 · §10 · 크롭 `txt_p11_conclusion_f_size_cohesive_future.png` · `txt_p07_cn_ratio_100rpm_softer_particles_larger_e_fewer_contacts.png` | [인쇄] | 압축 · 탈압과 직접 닿는 한계 문장은 없다
- [j] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer | 카드가 남긴 미확인: 계산 비용 · 하드웨어 · 적분법 · 54 µs 허용 간격의 식 (refs 21 · 22) · 벽 · 날 접촉의 R · 법선 감쇠의 R 과 m_i 뜻 · 인쇄 부호 · S_R² 에 쓴 N · Fig 7a '10 rpm' = 9.55 rpm 런인지 · Fig 4 ↔ Fig 7 전체 배위수 ≈ 0.15 차이의 원인 | 카드 §12 | [미확인] | —

## k — DEM 의 한계
- [k] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer — Chandratilleke, Zhou, Yu, Bridgwater 2010 (Ind. Eng. Chem. Res. 49, 5467–5478) | ★ 연화 영률이 접촉 기반 결과를 바꾼다는 저자 고백: *"In other words, the mixer is only capable of fully randomizing the particles and cannot engage in increasing the quality of the mixture any further. Therefore, the observed slight increase in the steady-state value should have resulted from the use of the softer particles in this work. Use of a larger Young's modulus will have resulted in fewer particle deformations and thus fewer particle contacts, possibly reducing the B-W CN ratio at the steady state."* (p.5473 · 100 rpm 정상 B–W / 전체 0.518 ↔ 2 · 47.75 rpm 0.504 [판독 Fig 8b]) | 카드 §0-1 · §3-6 · 크롭 `txt_p07_cn_ratio_100rpm_softer_particles_larger_e_fewer_contacts.png` | [인쇄] · [판독] | 정량 E 사다리는 없다 (고백만)
- [k] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer — Chandratilleke et al. 2010 (Ind. Eng. Chem. Res. 49, 5467–5478) | 보정값이 물성이 아니라는 문장 (시간 간격용 연화): *"Young's modulus E, however, was reduced from 10^9 of real glass beads to 2.16 × 10^6 to reduce computational time; this approach has been found to be able to produce reliable results.9,12"* (p.5468 · ÷463 [카드 산술]) | 카드 §3-1 · §7-3 · 크롭 `txt_p02_glass_like_mu_r_5e-5m_mu_s_0p3_e_1e9_to_2p16e6_dt_5us.png` | [인쇄] | '신뢰할 결과' 의 근거는 선행 논문 (refs 9 · 12) — 이 논문 안 검증 없음
- [k] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer — Chandratilleke et al. 2010 (Ind. Eng. Chem. Res. 49, 5467–5478) | 접촉 판정 허용이 만드는 인공물: *"solid angle analysis shows that a single particle can have a maximum of 14 contacts with uniform-sized spheres in three dimensional space (N.B.: coordination number >12 is possible because of the (5%)d gap allowance used here)"* (p.5472) · 간격 1 ↔ 5 % d 에 배위수 ≈ 1 차이 (Fig 4: 2 rpm 5.43 ↔ 6.34 · 100 rpm 4.34 ↔ 5.45 [판독]) · 배위수 · 공극은 *"difficult to produce experimentally"* (p.5470) | 카드 §3-5 · 크롭 `txt_p06_initial_cn_6_and_2_eight_vs_six_max14_gap_5pct.png` · `txt_p04_cn_gap_1_5pct_walls_included_porosity_0_to_blade_top.png` | [인쇄] · [판독] | —
- [k] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer — Chandratilleke et al. 2010 | 단단한 구 · 점접촉 · 형상 불변 자체에 대한 한계 문장 = **말 없음** (구 · 'properties close to those of glass beads' 만 · p.5468) | 카드 §4-6 (i) | — | —

## l — 소성변형이 왜 어려운가
- [l] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer — Chandratilleke, Zhou, Yu, Bridgwater 2010 (Ind. Eng. Chem. Res. 49, 5467–5478) | 소성 · 큰 변형이 어려운 이유 = **말 없음** (소성을 넣으려 하지 않음 · 'plastic' 0 회).  쓴 우회 = 탄성 Hertz 꼴 + 점성 감쇠 + 구름 토크에 E 연화 (÷463) — 목적은 **시간 간격** (*"to reduce computational time"*) · 소성 대리 아님 · 맞춘 값 0 · 검증 = 선행 PEPT (*"validated against the PEPT measurements as detailed by Stewart et al.10"*, p.5469) · 비용: 16,000 구 · dt 5 µs · 2 rpm 런 ≈ 157 s [판독 Fig 6a] ≈ 3.1 × 10⁷ 걸음 [카드 산술] · 시간 · 하드웨어 [미확인] | 카드 §4-6 (ii) · §3-1 · 크롭 `txt_p03_validated_against_pept_stewart_extension.png` | [인쇄] · [판독] · [카드 산술] | 연화하지 않은 E 로 옮긴 허용 간격 ≈ 4.6 µs (t_c 축척) · 2.5 µs (Rayleigh 축척) [카드 산술] — 실제로 쓴 5 µs 와 비슷 (연화의 시간 절약이 dt 50 → 5 µs 로 다시 쓰였다 [카드 추론])

## m — 받아들일 통찰
- [m] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer | 무엇: 'Lacey' 라는 같은 이름 아래 **연산자 네 칸** (분리 기준 = 이론 pq ↔ 런 t₀ · 칸 가중 = 입자 수 ↔ 같은 무게 · 무작위 기준 = 이항 pq/N ↔ 균일 삽입 런 실측 · 칸당 입자 ≈ 70–100 ↔ n_eff ≈ 3.6–3.7) 을 결과 전에 적고, 문헌 M 을 우리 M 옆에 나란히 놓지 않는다 · 어디: 단계 0 · 흐름 밖: 믹서 확인 블록 ([DEM 우선] Ⓒ) · 왜: 카드 §3-3 · §7 · §8-2 ① (식 3–4 p.5471)
- [m] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer | 무엇: 접촉 기반 지표 (s1 SE–SE 군집 · s2 AM–SE 부착 · 배위수) 는 연화 E 와 판정 거리에 걸린다 — 저자 스스로 접촉 비 +2.8 % 를 연화 탓으로 돌리고 (p.5473), 간격 1 ↔ 5 % d 에 배위수가 ≈ 1 바뀐다 (Fig 4) → **E 사다리 또는 판정 거리 사다리** 를 결과 전 등록에 · 어디: 후보 D0 · 단계 7 · 흐름 밖: 믹서 s1 · s2 · 왜: 카드 §3-5 · §3-6 · §8-2 ④ ⑤
- [m] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer | 무엇: **E 와 dt 를 같이 바꾼 비교는 교락** — 선행 (dt 50 µs · 40 rpm 이하) 의 '회전수 한 곡선' 과 이 논문 (5 µs · 2–100 rpm) 의 '한 곡선 아님' 은 두 가지가 함께 바뀐 비교 · 함정 (우리 Phase A 의 'E + dt 세대 전환 효과' 와 같은 구조) → 한 번에 하나만 바꾸는 사다리를 등록 · 어디: 후보 D0 · 단계 0 · 왜: 카드 §3-9 ③ · §8-2 ⑥ (p.5471)
- [m] chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer | 무엇: 같은 결과가 **시간 · 회전수 · 에너지** 축마다 승자가 다르다 (시간 = 100 rpm · 회전수 = 2 rpm (4 ↔ 6 회전) · 에너지 = 2 rpm (27.6 ↔ 65.5 J · 시간 33 배)) → 믹서 팔 보고 축을 셋으로 고정 · 에너지 = 정상 토크 × 쓸고 간 각 (재현: 맞춤식 Γ(2)·8π = 27.55 J · Γ(100)·12π = 65.51 J) · 어디: 흐름 밖: 믹서 V2 (혼합 시간 · 에너지) · 왜: 카드 §3-6 · §3-8 (p.5471 · 5476)

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] Zhou, Y.; Yu, A. B.; Stewart, R. L.; Bridgwater, J. Microdynamic Analysis of the Particle Flow in a Cylindrical Bladed Mixer. Chem. Eng. Sci. 2004, 59, 1343–1364. (원문 참고문헌 9 · 인쇄 그대로) | e · k · l — 이 DEM 모델의 원전 (첫째 · *"developed previously,9,12"*) · 연화 E 의 *"reliable results"* 근거 · 같은 조건 10 rpm 토크 1.1 N m · 배위수 · 공극 · 힘 망 방법 · 카드 §0-1 · §11 | litdb 확인: `papers/` 에 zhou2004* 없음 · 'Microdynamic' · '1343–1364' grep 0 건 · `wishlist.md` 0 건
- [n] Zhu, H. P.; Zhou, Z. Y.; Yang, R. Y.; Yu, A. B. Discrete Particle Simulation of Particulate Systems: Theoretical Developments. Chem. Eng. Sci. 2007, 62, 3378–3396. (원문 참고문헌 13 · 인쇄 그대로) | e — Table 1 힘 · 토크 식이 *"commonly used"* 라는 근거 리뷰 (접촉 법칙 종류 · 감쇠 · 구름 꼴의 정리) · 카드 §0-1 · §11 | litdb 확인: `papers/` 에 zhu2007* 없음 · 'Theoretical Developments' · '3378–3396' grep 0 건 · `wishlist.md` 0 건
- [n] Kristensen, H. G. Statistical Properties of Random and Non-Random Mixture of Dry Solids. Powder Technol. 1973, 7 (5), 249–257. (원문 참고문헌 18 · 인쇄 그대로) | m · 흐름 밖 (믹서) — 크기 다른 혼합물의 무작위 분산 (고정 부피 표본) · 저자가 S_R² = pq/N 이 크기 다른 혼합물에 맞지 않는 근거로 듦 (p.5471) → 우리 SE : AM 1 : 9 크기비의 무작위 기준 · 카드 §3-3 · §11 | litdb 확인: `papers/` 에 kristensen* 없음 · 'Kristensen' · 'Statistical Properties of Random' grep 0 건 · `wishlist.md` 0 건
- [n] Asmar, B. N.; Langston, P. A.; Matchett, A. J.; Walters, J. K. Validation Tests on a Distinct Element Model of Vibrating Cohesive Particle Systems. Comput. Chem. Eng. 2002, 26 (6), 785–802. (원문 참고문헌 21 · 인쇄 그대로) | m · e — 54 µs 허용 시간 간격 기준의 근거 (둘 중 하나 · 식은 이 논문에 없음 [미확인]) · DEM 검증 시험 · nadeem2023 카드가 MGMMI 원전으로 이름만 언급 · 카드 §3-9 ③ · §11 | litdb 확인: `papers/` 에 asmar* 없음 · 'Validation Tests on a Distinct' grep 0 건 · 'Asmar' grep = nadeem2023 (이름만) · `wishlist.md` 0 건
- (참고 · 후보로 세지 않음) Zhou, Y. C.; Wright, B. D.; Yang, R. Y.; Xu, B. H.; Yu, A. B. Rolling Friction in the Dynamic Simulation of Sandpile Formation. Physica A 1999, 269, 536–553. (참고문헌 12 · 모델 원전 둘째 · 구름 A 부류) = `wishlist.md` 에 이미 있음 · Stewart, R. L.; Bridgwater, J.; Zhou, Y. C.; Yu, A. B. Chem. Eng. Sci. 2001, 56 (19), 5457–5471 (참고문헌 10 · 같은 믹서 DEM ↔ PEPT) = 후보 표 N-45 · Tsuji 1993 (참고문헌 22 · 54 µs 근거 둘째) = 우선순위 낮음.

## 카드 문제
- `chandratilleke2012_particle_scale_mixing_index` **L307** (가리킨 줄): *"18 \| Chandratilleke GR, Zhou YC, Yu AB, Bridgwater J. Ind Eng Chem Res. 2010;49:5467–5478 \| 이 논문 DEM 의 방법 원전 — 카드 없음"* — 서지 ✓ (호 11 · 제목 · DOI 는 그 줄에 없음).  **'방법 원전' 은 반만 맞다** — 이 논문 자신이 *"The DEM model used here was developed previously,9,12"* (p.5468) 라 적으므로 모델 원전 = Zhou 2004 (*Chem. Eng. Sci.* 59, 1343) · Zhou 1999 (*Physica A* 269, 536) · 이 논문 = 식 (Table 1) 의 지면 출처.  '카드 없음' 은 이 카드로 낡음.  고치지 않음 (경미).
- `chandratilleke2012_…` **L187** (가리킨 줄): 서술 (운동량 식 · 법선 · 접선 탄성 + 감쇠 · 토크 + 구름 · 벽 · 날 = 입자 물성) ✓ · *"⚠ 힘 법칙의 식 (Hertz · Mindlin 여부) 은 이 논문에 없다 [미확인 — ref 18 · 29 참조]"* 의 [미확인] 은 이 카드 §3-2 로 해소 (Hertz 꼴 법선 · Mindlin–Deresiewicz 꼴 접선 · 이름은 2010 원문에도 없음) · 구름마찰 풀이 '변형 에너지 소산' 은 2010 원문에 없다 (2012 원문의 말인지는 2012 PDF 대조 안 함 [미확인]).  고치지 않음.
- `chandratilleke2012_…` **L291** (가리킨 줄): *"힘 법칙 미기재 — 이 논문만으로 DEM 을 재현할 수 없다 (ref 18 필요)"* ✓ — ref 18 (이 논문) 에 식이 있다.  단 ref 18 로도 2012 의 크기 다른 쌍 (크기비 0.5–1) · 벽 · 날 접촉의 R · 틈 있는 믹서 (벽 2.5 mm · 바닥 7.5 / 0 mm · 날 106 mm ↔ 2010 은 틈 없음) 는 정해지지 않는다 — 문제 아님 (기록).
- (참고 · 문제 아님) `chandratilleke2012_…` L61 의 연화 근거 *"(ref 12 · 17)"* = 2012 논문 자기 번호 · 2010 의 같은 문장은 refs 9 · 12 (Zhou 2004 · Zhou 1999).
- (참고 · 문제 아님) `jadidi2023_dem_batch_solid_mixers_review` L186 (Lacey 지수 · 블레이드 믹서 'Chandratilleke … 2010') · L255 (힘 망 · 접촉력 'Chandratilleke 2009/2010') ✓ — 이 논문과 맞음 · L382 표 머리 '다분산 · 표면거칠기 · 점착 findings' 는 리뷰 표 10 전체의 주제 (이 논문은 단분산 · 비점착) — 목록일 뿐.
- (관찰 · 원문 자체의 어긋남 — 카드 §10 에 기록) 법선 감쇠 식의 부호가 접선 감쇠와 반대 규약 (인쇄 그대로면 다가올 때 에너지를 넣음) · 접선 식의 \|δ_i\| (정의 안 된 기호 · \|δ_t\| 의 오식) · 법선 감쇠의 R 미정의 · Fig 9a 의 곡선 번호 '4' (캡션은 1–3) · 속도 표기 47.75 / 47.7 / 47.5 · 23.87 / 23.8 · 철자 'instaneous' · 'verticle' · 'Poison's ratio'.
- (참고 · 카드 아님) 후보 표 `litdb/_curation/S8_candidates.md` N-32 서지 = 원문과 같음 (제목 *"Effect of Blade Speed on Granular Flow and Mixing in a Cylindrical Mixer"* · 호 11 · DOI 10.1021/ie901581t 는 원문에서 채움).
- (참고 · 카드 아님) `litdb/figures/_sources.json`: 이 배치의 `extract_figures.py` 가 다른 카드 줄 (choi2018 `figures` 8 → 32 · devasconcelos2019 `pdfs` 목록) 을 바꿨으나 HEAD 값으로 되돌리고 이 카드 줄만 더했다 (batch_69 · 71 과 같은 현상).
