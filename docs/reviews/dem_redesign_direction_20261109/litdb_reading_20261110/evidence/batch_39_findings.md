# batch_39 정독 근거 (보충 카드 1 장 · 전문 읽음 · 2026-11-11)

읽은 카드: `choi2026_bzox_dry_zro2x_nmc_shell_coating` (184 줄 · 한 번에 마지막 줄까지 읽음). 배치 21 의 안내문 카드 `bzox_dry_zro2x_nmc_shell_coating_sulfide_assb` 가 가리키던 정본이다 (카드 L4 "supersedes").

카드의 성격: 단결정 NMC811 위 ~8 nm ZrO₂₋ₓ 껍질 (건식 mechanofusion) 의 전기화학 실험 + VASP 계면 슬랩 DFT. **압력 · 기공 · 밀도 · 두께 · 되돌아옴 · 항복 · 경도 · DEM · MPM 이 카드에 하나도 없다** → 가압 · 탈압 계획 (a–l) 에 줄 근거는 없고, 쓸 만한 것은 흐름 밖 (코팅 활물질 · 계면 저항 분해 · AM 전자 전도 입력) 뿐이다.

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (없으면 "표지 없음") · "내 검산" = 카드에 적힌 숫자끼리만 대조한 것 (카드 문제 절에만 씀). 랩 표준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³) 은 고정 — 이 카드에는 기공 · 밀도 값이 없어 대조할 것이 없다.

---

## a. 순수 SE (LPSCl · 황화물) 압력별 기공 곡선 · 진밀도

이 배치에 없음 (기공 · 밀도 · 압력 값이 카드에 없음). 관련만:
- [a] choi2026_bzox_dry_zro2x_nmc_shell_coating | "사이클 전엔 3 종 모두 저저항 (냉압 접촉 양호)" — 냉간 가압으로 셀을 만들었다는 흔적 한 줄뿐 | §3.4 L61 | 표지 없음 (카드 풀이) | 압력 값 · 누른 채 / 뺀 뒤 · 진밀도 카드에 없음

## b. 압력을 뺄 때 되돌아오는 양 · 잰 방법

이 배치에 없음.

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 환산

이 배치에 없음 (기계 물성 값 없음). 관련만:
- [c] choi2026_bzox_dry_zro2x_nmc_shell_coating | 코팅 뒤 NMC 입자 SEM: ~5 µm 단결정 · 표면 매끈 · "기계 손상 · 균열 없음" (mechanofusion 2000 rpm 10 min → 4000 rpm 30 min 뒤) | §5 SI 표 L120 (Fig S2) · §3.1 L33 | 표지 없음 (SEM 정성) | 힘 · 응력 값 없음 · 단결정 NMC811 (SE 아님)

## d. 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

이 배치에 없음.

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안

이 배치에 없음.

## f. MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙

이 배치에 없음.

## g. 2D 결과를 3D 로 옮길 때의 경고나 증거

이 배치에 없음.

## h. DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

이 배치에 없음.

## i. 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음 (복합 양극 조성 · 압력 · 기공이 카드에 없음 — 셀은 NMC | LPSCl | Li 금속 40 µm 라는 것만 · §2 L26).

## j. 카드가 스스로 적은 한계 가운데 가압 · 탈압 계산과 닿는 것

가압 · 탈압과 닿는 한계는 없음 (카드 §10 의 11 항은 전부 전기화학 · DFT 주장의 한계). 닿을 수 있는 것 하나만:
- [j] choi2026_bzox_dry_zro2x_nmc_shell_coating | 계면 상태를 직접 재지 않음 — space-charge layer 완화는 Fig 1 모식도 주장뿐 (직접 측정 없음) · 산소결핍 x 정량 없음 · σ_e 는 코팅 NMC 펠릿 값 (SE bulk 와 혼용 금지) | §10-8 L172 · §10-9 L173 · §10-10 L174 · §3.5 L69 | 표지 없음 | 눌린 구조의 계면 수송 (단계 7) 에 넣을 계면 저항 값은 주지 않음

## k. DEM 의 한계

이 배치에 없음 (DEM 을 쓰지 않는 실험 + DFT 카드 — "말 없음" 의 대상이 아님).

## l. 소성변형이 왜 어려운가

이 배치에 없음 (입자 계산이 없음). 관련만:
- [l] choi2026_bzox_dry_zro2x_nmc_shell_coating (Choi 외 · Small 2026, 0:e73805 · DOI 10.1002/smll.73805) | mechanofusion = "고속 회전 챔버의 전단 · 압축력으로 게스트 나노입자를 호스트 입자 표면에 무용매 융착" · 3 단계 (전단대류 → packing-milling → fusion · Fig 1) → ~8 nm conformal 껍질 — 혼합 중 게스트가 껍질로 펴지는 과정이 실험에 있다는 사실 (계산은 없음) | §11 L178 · §5 L111 · §3.1 L33–34 | 표지 없음 (카드 풀이 · 모식도) | 논문이 소성 계산의 어려움을 말한 것은 아님 · 맞춘 값 · 비용 해당 없음

## m. 받아들일 통찰

- [m] choi2026_bzox_dry_zro2x_nmc_shell_coating | 코팅의 운동학 비용을 이온 / 전자로 가르는 측정 세트: EIS 등가회로 (R_SE + R_CA-CA + R_CA-SE + R_AN-SE + CPE_W · 첫 사이클 뒤 R_CA-SE 44.5 / 192.9 / 55.2 Ω) + DC 분극 σ_e (÷25.5 vs ÷3.8) + GITT 과전압 (49.3 / 97.7 / 46.2 mV) 과 정규화 D_Li⁺·S²·V⁻² (충전 때 WZO 최저 · 방전 때 3 종 유사) → "WZO 병목은 σ_ion 이 아니라 σ_e" 판정 | 흐름 밖: 계면 저항 분해 (계면 항을 이온 / 전자 몫으로 가르는 실험 대조 꼴) | §3.4 L56–61 · §3.5 L63–69 · §3.6 L71–73 · §5 L114 (D_Li 는 V_m · S 불확실성 때문에 절대값 없음)
- [m] choi2026_bzox_dry_zro2x_nmc_shell_coating | 코팅 / 비코팅 단결정 NMC811 펠릿의 σ_e (DC 분극 200 mV · 30 °C · A 1.326 cm² · L 0.364–0.444 mm): 1.49×10⁻⁴ (비코팅) · 5.85×10⁻⁶ (절연 ZrO₂ ~9.7 nm) · 3.88×10⁻⁵ S/cm (ZrO₂₋ₓ ~8.1 nm) — ~8–10 nm 껍질 하나가 펠릿 전자 전도를 ÷3.8–÷25.5 로 바꿈 | 흐름 밖: AM 전자 전도 입력 · 코팅 활물질 (코팅 AM 을 넣을 때 AM 쪽 전자 전도는 껍질이 정함); 단계 7 | §3.5 L64–69 · §3.1 L34 (펠릿 성형압 · 기공 미기재 · SE bulk σ_e 와 혼용 금지)
- [m] choi2026_bzox_dry_zro2x_nmc_shell_coating | "코팅의 선악은 코팅 대상이 정의": SE 입자 코팅은 전자 절연 + Li 전도가 선 · AM 입자 코팅은 전자 · 이온 모두 전도가 선 — 같은 ZrO₂ 가 대상에 따라 실패 / 성공 (`sundar2025_oxide_coating_screening_lpscl` 과 상보) · 저자의 창 논리 = 밴드갭 0.5–2.25 eV (E_g < 0.5 eV 는 SE 표면 분해 촉진 — ref 11) | 흐름 밖: 코팅 활물질 설계 (코팅 프리셋에 "코팅 대상 + 요구 σ_e 방향" 을 같이 적기) | §7 L147–150 · §8-2 L155 · §3.1 L37 (밴드갭은 선행논문 소환값)
- [m] choi2026_bzox_dry_zro2x_nmc_shell_coating | 읽기 함정 둘: ① 유지율 % 만 보면 절연 코팅 (WZO 85.8 %) 이 최고 — 절대용량이 낮아 생긴 통계라 절대용량 + CE + 전압 이력을 같이 봄 ② 본문 rate 문장 (1 C 에서 ~140 vs ~115 mAh g⁻¹) 이 SI 그래프 판독 (~103 vs ~80 · 비코팅 ~115) 과 ~35 mAh g⁻¹ 어긋나고 본문은 비코팅을 빼고 비교 — 인용은 "코팅끼리의 우열" 까지만 | 흐름 밖: 실험과의 대조 · 문헌 값 인용 점검 | §3.3 L53 · §3.7 L75–78 · §10-1 L165 · §10-2 L166

## n. 논문 에이전트 후보

- [n] Choi et al., J. Mater. Chem. A 2024, 12, 30667 (DOI 10.1039/D4TA05179C) — 같은 1 저자의 black zirconia LIB 논문 (제목 · 공저자는 카드에 없음 — 서지 일부만) | 왜: m (흐름 밖: 코팅 활물질) — 이 카드의 BZOx 밴드갭 0.5–2.25 eV 와 Li 이동장벽 BZOx 0.8 / WZO 1.4 eV 가 전부 이 선행논문의 소환값이고 이 카드에서는 재계산하지 않음 (§3.1 L37 · §4 L101 · §10-7 L171 · 판 이력 L15) · a–l 에는 쓸 곳 없음 (근거 약함) | litdb 확인: papers/ `ls` 에 `choi2024_digital_twin_review_echem` 뿐 (다른 논문) · DOI `D4TA05179C` · "30667" · "black zirconia" grep 은 이 카드 자신에만 걸림 → 카드 없음

(카드가 인용한 나머지 — ref 11 Xiao/Ceder Joule 2019 = `xiao2019_cathode_coating_screening` · Sundar = `sundar2025_oxide_coating_screening_lpscl` · Cha = `cha2024_dualcompatible_halide_ncm_lpscl_interface` — 는 카드가 있어 적지 않았다. ref 25 "Ma/Janek" (SO₂ 기체 분해 산물 · L104) 는 서지가 카드에 없고 a–m 에 쓸 곳이 없어 뺐다.)

## 카드 문제

- choi2026_bzox_dry_zro2x_nmc_shell_coating | 머리 태그 `methods:` (L9) 에 bader · cohp · elf · md · mlip · neb 가 있는데 본문은 "없음 (n/a): AIMD · NEB (본 논문) · Bader · COHP · grand-potential · MLIP" (§4 L101) · "NEB / Bader / COHP / grand-potential / ELF / AIMD = 없음" (§6 L132) — 태그와 본문이 어긋남 (태그로 검색하면 잘못 걸림)
- choi2026_bzox_dry_zro2x_nmc_shell_coating | 상 배정이 세 곳에서 다름: 본문 텍스트 "BZOx = monoclinic 단상 · WZO = monoclinic + tetragonal 혼상" ↔ SI Fig S1 판독 "BZOx tetragonal 단상 (ZrO₁.₈ 카드)" ↔ DFT WZO 모델 = tetragonal P4₂/nmc (§3.1 L36 · §4 L97 · §10-4 L168) — 카드가 스스로 적은 혼선
- choi2026_bzox_dry_zro2x_nmc_shell_coating | rate 값 둘: 본문 "1 C 에서 BZOx ~140 / WZO ~115 mAh g⁻¹" ↔ SI Fig S5 판독 ~103 / ~80 (비코팅 ~115 · ±5) · 1 C 정의도 본문 200 ↔ 구판 SI 기록 180 mA g⁻¹ (§3.7 L75–78 · §10-1 L165)
- choi2026_bzox_dry_zro2x_nmc_shell_coating | 힘 수렴 기준이 같은 절에 둘 ("< 10⁻² eV/Å" 와 "< 0.001 eV/Å") (§4 L94 · §10-6 L170)
- choi2026_bzox_dry_zro2x_nmc_shell_coating | DFT 의 BZOx 모델 ZrO₁.₃₃ (x = 0.67) 이 실험 지문 (XRD ZrO₁.₈ · x ≈ 0.2) 의 3 배 산소결핍 (§4 L97 · §7 L151 · §10-3 L167)
- choi2026_bzox_dry_zro2x_nmc_shell_coating | 한 줄 요약 (L19) 과 인용 문장은 "100 cyc 유지율 70.6 → 80.4 %" 를 내세우는데 표에서 유지율 최고는 WZO 85.8 % (§3.3 L51–53 · §10-2 L166) — 카드가 스스로 "오독 유발 문구" 로 적음
- choi2026_bzox_dry_zro2x_nmc_shell_coating | §3.3 표의 NMC-WZO 100 cyc 방전용량 칸이 "(초기 ~100)" 으로 적혀 뜻이 불분명 — 첫 사이클 방전은 121.2 mAh g⁻¹ (§3.2 L43) 이고 내 검산으로 121.2 × 0.858 ≈ 104 (100 사이클 값이면 맞고 "초기" 값이면 121.2 와 어긋남) · 같은 표의 다른 두 줄은 검산이 맞음 (109.2 / 154.58 = 70.6 % · 126.69 / 157.57 = 80.4 %)
- choi2026_bzox_dry_zro2x_nmc_shell_coating | §3.2 표의 NMC-WZO 충전 용량이 "n/a" 인데 방전 121.2 + 비가역 손실 73.31 = 194.51 mAh g⁻¹ 로 정해지고 초기 CE 62.3 % 와 맞음 (내 검산 121.2 / 194.51 = 62.3 %) — 빈칸이 아니어도 되는 칸 (사소)
- choi2026_bzox_dry_zro2x_nmc_shell_coating | 구판 (SI 전용) 의 "WZO 도 E_F 직하" 판독을 본문 기준으로 뒤집음 (§4 결과 요지 L105) — 구판을 인용한 다른 카드가 있으면 낡은 서술일 수 있음 (이 slug 를 언급하는 카드: kawaguchi2017 · liu2026_ccto · nakamura2020 · park2026_ml_framework · pfeffer2001 · qian2025 — 내용 대조는 하지 않음)
- (검산 통과 · 문제 아님) §3.5 σ_e = L/(R·A): 0.0364 / (184.67 × 1.326) = 1.49×10⁻⁴ · 0.0444 / (5714.2 × 1.326) = 5.86×10⁻⁶ · 0.0419 / (816.3 × 1.326) = 3.87×10⁻⁵ S/cm — 표의 1.49×10⁻⁴ · 5.85×10⁻⁶ · 3.88×10⁻⁵ 와 끝자리 반올림 안에서 같음 (내 검산)
