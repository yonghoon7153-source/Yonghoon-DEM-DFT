# batch 131 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 N-82)

대상: `kissel2025_cathode_mixing_quality_cam_utilization_reproducibility_press_cells` — M. Kissel · M. Schosland · J. Töws · D. Kalita · Y. Schneider · J. Kessler-Kühn · S. Schröder · J. Schubert · F. Frankenberg · A. Kwade · A. Bielefeld · F. H. Richter · J. Janek\*, "Quantifying the Impact of Cathode Composite Mixing Quality on Active Mass Utilization and Reproducibility of Solid-State Battery Cells", *Adv. Energy Mater.* **15** (2025) 2405405 · DOI 10.1002/aenm.202405405 (13 쪽 · SI 7 쪽 · 셀 workbook 17 배치 · 56 셀).
같은 재료 (단결정 NCM82 : Li₆PS₅Cl : CNF = 70 : 30 : 1) · 같은 조립의 펠릿 셀을 손 막자 ↔ 미니 진동밀 혼합으로 만들고 OCP 이완법으로 셀 안에서 '정적 CAM 이용률' 을 재어 용량 흩어짐 · gross ↔ active 비용량 · 정적 ↔ 동역학 손실을 가른 실험 (375 MPa 3 min → ≈80 MPa · 25 °C).
쪽 = PDF 쪽 = 학술지 'n of 13' · SI 는 'SI p.n' · 원자료 발췌 = `litdb/figures/kissel2025_…/data_file_s1_extract.csv` (56 셀) · 고른 의도 대조 = **채움** (카드 §0-1 — 정적 이용률 측정법 (원전 Conforto 2021 · 이 논문 = 초기 이용률 각색) · 2 차 혼합도 정의 (정의만 · 값 없음) · 혼합 품질 ↔ 이용률 (r 0.95 · 손 ↔ 기계 흩어짐)).
인용 서지 (질문 k · l 용): Kissel et al., Adv. Energy Mater. 15 (2025) 2405405.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 압력별 기공 · 밀도 곡선이 없다.
- [a] kissel2025_cathode_mixing_… | (참고 · 곡선 아님) 분리막 Li₆PS₅Cl 'CMP5' 80 mg ≈ 700 µm (Ø 10 mm) → 겉보기 1.46 g/cm³ → 랩 진밀도 1.64 로 나누면 ≈11 % (±50 µm 면 ≈4.5–17 %) | 카드 §3-1 · §7-2 · p.5 (`txt_p4_p5_anode_40_80_375_mpa_separator_700um.png`) · 그림 5 | [카드 산술] (인쇄 '≈700 µm' · 80 mg · 지름) | 375 MPa 3 min 압착 뒤 · 측정 시점 · 방법 미서술 · 원문에 진밀도 · 기공률 없음 · 랩 표준 옆 크기 감각만 (판정 아님)

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 되돌아옴 · 두께 측정 없음.
- [b] kissel2025_cathode_mixing_… | (조건만) 셀 성능은 전부 **375 MPa 3 min 압착 → ≈80 MPa 구동** (10 Nm · 그림 5 '>70 MPa') 상태의 값 | 카드 §0 ② · §3-1 · p.5 (`txt_p5_cell_assembly_protocol_375mpa_3min_80mpa.png`) | 인쇄 | 탈압 양 · 시간 의존 없음 · 우리 300 MPa 누른 채 값과 상태 다름

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 입자 기계 물성 값 없음 (정성 문장만: SE 의 *"mechanical characteristics influence the quality of mixing"* p.9 · *"compatible mechanical properties of the particles"* p.10 — 질문 l 에 옮김).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음.

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · DEM 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 계산 · 3D 영상 없음 (CNF 분말 SEM 만 · SI 그림 S9).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.  (인용만: 실험실 혼합 장치를 *"model systems to simulate the mixing action … stressing conditions such as stress intensity distribution and stress number [63]"* 로 쓰라는 제안 · p.10 · [35] = `frankenberg2024_dem_high_intensity_mixer_assb`.)

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 압력 한 값 (375 MPa) · 기공 미인쇄.
- [i] kissel2025_cathode_mixing_… | (참고 · 기공 아님) 복합체 15 mg · 그림 5 모식 두께 ~50 µm → 겉보기 3.8 g/cm³ · 70 : 30 : 1 wt | 카드 §3-1 · 그림 5 (`fig_5.png`) | [카드 산술] (모식의 '~' 두께) | 진밀도 · 기공률 없음 · 압력 의존 없음

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
- [j] kissel2025_cathode_mixing_… | 부분 전도도 (2 차 혼합도의 정량) *"requires symmetric cell setups, three-electrode cells, or transmission line models (TLMs), which was not possible in this study. The used measurement device sets an upper-frequency limit"* | 카드 §0-1 · §11-2 · p.7 (`txt_p7_eis_simplified_circuit_no_tlm.png`) | 인쇄 | 2 차 혼합도는 정의만
- [j] kissel2025_cathode_mixing_… | *"the CAM utilization is a static property and only differentiates between connected and unconnected CAM particles. This parameter does not contain any information on the quality of the connection"* | 카드 §3-5 · p.8 (`txt_p8_cnf_type2_75p6_vs_89p8_static_property.png`) | 인쇄 | 연결의 '질' (접촉 면적 · 저항) 은 담지 않는다
- [j] kissel2025_cathode_mixing_… | *"too high porosities must be avoided by sufficient densification and compatible mechanical properties of the particles"* (기공 · 압밀은 다루지 않음) · *"a more accurate normalization method to compensate for microstructural effects at higher C-rates still needs to be developed"* | 카드 §4-4 · p.9–10 (`txt_p9_p10_static_vs_kinetic_loss_recommend_initial_util.png` · `txt_p9_primary_secondary_degree_of_mixing.png`) | 인쇄 | 압력 · 기공 변수 없음

## k — DEM 의 한계 (서지: Kissel et al., Adv. Energy Mater. 15 (2025) 2405405)
- [k] kissel2025_cathode_mixing_… (Kissel 2025 · Adv. Energy Mater.) | **말 없음** — DEM 을 쓰지 않는다.  모사는 인용으로만: *"Simulations have shown that the microstructural arrangement of CAM particles and SE particles is crucial for the transport kinetics since it affects the effective conductivities within the composite cathode.[27–29]"* (p.2) | 카드 §4-4 (i) | 인쇄 | DEM 한계 진술 0

## l — 소성변형이 왜 어려운가 · 우회 (서지: Kissel et al., Adv. Energy Mater. 15 (2025) 2405405)
- [l] kissel2025_cathode_mixing_… (Kissel 2025 · Adv. Energy Mater.) | **논의 없음** — 입자 기계 성질은 혼합 · 치밀화의 조건으로만: *"The mechanical properties of the particles as well as often wide particle size distributions of the SE pose a challenge for a successful mixing process"* (p.2 · [35, 36]) · SE 의 *"mean and width of particle size distribution, particle adhesion forces, and mechanical characteristics influence the quality of mixing and the resulting microstructure"* (p.9) | 카드 §4-4 (ii) · `txt_p9_se_comparison_psd_adhesion_mechanics.png` | 인쇄 | 소성 · 변형 측정 · 계산 없음 · 우회 없음

## m — 받아들일 통찰
- [m] kissel2025_cathode_mixing_… | **정적 이용률의 모형 짝을 결과 전에 정의** — 원문 범주 (p.10): 전자 접촉 전부 손실만 '비활성' · SE 이온 접촉을 다 잃어도 연결된 CAM 으로 Li 가 들어가면 '정적 활성' → 우리 짝 = 전자 활성 몫 ∧ (SE 경로 또는 CAM 이웃) · `am_ionic_isolated_pct` 단독 아님 · 대조값 74–95 % (진동밀 87–93 %) | 자리: 단계 7 · 결과 전 대조 항목 | 왜: 카드 §7-1 · §8 · p.6 · p.10 (`txt_p10_contact_loss_categories_i_iv.png`)
- [m] kissel2025_cathode_mixing_… | **active 비용량에서는 무게가 약분된다** — q_act = q_gross / u = Q · q_ref / Q_창 (m_CC · x_AM 소거 · 식 1–3) → 실험 대조는 active 값으로 · 원문의 '흩어짐은 식 2 오차 전파 탓' 설명은 이 대수와 맞지 않는다 | 자리: 단계 0 (대조값의 정규화 칸) | 왜: 카드 §4-3 · §11-4 · 식 1–3 (`eq_01…` · `eq_03…`) [카드 산술]
- [m] kissel2025_cathode_mixing_… | **혼합 질 = 셀 간 흩어짐** — 손 ↔ 진동밀 9 셀: 0.1 C 평균 178.0 ↔ 179.5 · CV 5.1 ↔ 1.4 % · 이용률 89.0 ± 4.0 ↔ 89.0 ± 1.2 % → 믹서 → 압밀 → 접촉망 사슬의 판정 지표를 '시드 간 연결 몫 분포 (평균 + SD)' 로 | 자리: 흐름 밖: 믹서 Ⓒ (혼합 질 지표) | 왜: 카드 §3-3 · §3-8 · p.3 (`txt_p2_p3_hand_ground_162_188_cv.png` · `txt_p3_p4_machine_made_30hz_nine_balls_cv.png`) [인쇄 · 카드 산술]
- [m] kissel2025_cathode_mixing_… | **문헌 원자료를 대조값으로 쓰기 전 인쇄 그림과 대조** (함정) — workbook 38 셀로 r 0.971/0.917/0.736 (인쇄 0.95/0.89/0.73) · 배치 11 셀 2 · 3 은 그림 6a 에서 ≈1.045–1.05 배 (질량 12.6 ↔ ≈12.0 mg 의 비) · 배치 8 셀 3 없음 · 그림에만 있는 점 셋 · SD 는 모집단 SD | 자리: 흐름 밖: 실험 대조 규약 | 왜: 카드 §3-8 · `data_file_s1_extract.csv` (fig6a_check 열) [판독 · 카드 산술]

## n — 논문 에이전트 후보 (카드가 인용 · 언급했지만 litdb 에 카드가 없는 것)
- [n] G. Conforto, R. Ruess, D. Schröder, E. Trevisanello, R. Fantin, F. H. Richter, J. Janek, J. Electrochem. Soc. 2021, 168, 070546. | m · 단계 7 — OCP 이완법 (식 3 · 정적 이용률) 의 원전 · 이 논문은 '각색' (p.2 · p.6 · p.11) — 카드 §0-1 · §12 | papers/ 목록 · 'conforto' · '070546' grep = 카드 없음 (li2026 · taghikhani2025 가 인용만) · wishlist.md 에 이미 있음
- [n] S. Puls, E. Nazmutdinova, F. Kalyk, H. M. Woolley, J. F. Thomsen, Z. Cheng, A. Fauchier-Magnan, A. Gautam, M. Gockeln, S. Y. Ham, M. T. Hasan, M. G. Jeong, D. Hiraoka, J. S. Kim, T. Kutsch, B. Lelotte, P. Minnmann, V. Miß, K. Motohashi, D. L. Nelson, F. Ooms, F. Piccolo, C. Plank, M. Rosner, S. E. Sandoval, E. Schlautmann, R. Schuster, D. Spencer-Jolly, Y. Sun, B. S. Vishnugopi, et al., Nat. Energy 2024, 9, 1310. | m — 실험실 간 round robin (같은 재료 · 그룹마다 흩어짐) · 이 논문의 출발점 (p.2) — 카드 §1 · §12 | 'puls' · '9, 1310' grep = 카드 없음 (alharbi2026 이 인용만)
- [n] S. Yanev, H. Auer, C. Heubner, S. Höhn, K. Nikolowski, M. Partsch, A. Michaelis, J. Electrochem. Soc. 2022, 169, 090519. | m — 유효 C-rate (공칭 ÷ 이용률) 의 출처 (p.7 · p.9 · p.10) — 카드 §4-3 | 'yanev' · '090519' grep = 카드 없음 (wolf2026 이 인용만)
- [n] B. X. Shi, Y. Yusim, S. Sen, T. Demuth, R. Ruess, K. Volz, A. Henss, F. H. Richter, Adv. Energy Mater. 2023, 13, 2300310. | j · R7 — 사이클 중 활성 질량 손실 정량 (식 3 의 둘째 인용 · p.10) — 카드 §12 | '2300310' grep = 카드 없음
- [n] A. Kwade, Chem Eng. Technol. 2003, 26, 199. | h · 흐름 밖 믹서 — 응력 강도 · 응력수 모형 (p.10 · Frankenberg 2024 · Kissel 2026 DEM 의 바탕) — 카드 §12 | 'kwade2003' 파일 없음 · '26, 199' grep = kissel2026 이 인용만 → 카드 없음 (원문 목록 꼴 = 모든 항목에 제목 없음)

## 카드 문제
- `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` **L232**: *"2 차 혼합도 (secondary degree of mixing, ref 31): 응집체 수준의 혼합 상태."* — 원문 (Kissel 2025 p.9) 정의 = *"a measure of how tortuous the transport pathways are which can be quantified by effective conductivities"* (1 차 = CAM 이용률) · '응집체 수준' 은 원문에 없다.  (그 카드 L209 의 쓰임 *"a comparable tortuosity … i.e., a similar secondary degree of mixing"* 은 원문과 맞다.)  고치지 않음.
- `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` **L247** (경미): *"CAM 이용률 측정 (ref 34 방식) [인쇄 p.15]: … 3 h 유지 · 3 h 휴지 → V₁ · 0.05 C 로 3.4 V · 5 h 휴지 → V₂"* — ref 34 (= 이 논문) 의 절차는 3 h 유지 + **4 h** 휴지 → V₁ · **4 h** 휴지 → V₂ (p.11).  kissel2026 원문 p.15 가 실제로 다른 절차인지 그 카드의 옮김이 다른지는 [미확인] (그 PDF 를 이 작업에서 볼 수 없음) — 그 줄의 휴지 시간을 'ref 34 방식' 으로 인용하지 않도록 적는다.  고치지 않음.
