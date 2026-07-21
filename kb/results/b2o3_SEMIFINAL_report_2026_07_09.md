# B₂O₃-doped LPSCl1.6 챔피언 — Semi-Final 통합 보고서

**날짜** 2026-07-09 (통합판 v1) · **갱신** 2026-07-21 (§9 잔여작업 정리, §11 3-시스템 진행표 신설) · **성격** 논문 초안의 뼈대가 되는 반최종 보고서
**통합 원본 5종** ① 전자 국소화 프레임워크 ② Li|전해질 계면 MD takeaways ③ σ\* 궤도 제어
④ convex hull(37.5 meV/atom) ⑤ anode 계면 campaign(6× 철회 + 종단 스캔) — 전부 2026-07-09
저녁 roll-0.71 clean-build 최종 판정까지 반영. 상태 표기: ✅확정 / 🔶잠정 / ⏳진행.

---

## 0. Executive Summary

**챔피언 서사 (한 문단).** B₂O₃ 도핑 LPSCl1.6은 **이온전도를 보존**하고(O-penalty를 면내 채널
개방이 상쇄, Ea 0.199≈0.197 eV), **압축 강성을 +13% 올리며**(B₀ 24.5 vs 21.7 GPa), **전기화학
안정성을 훼손하지 않고**(산화 onset 2.03≈2.14 V; Li-금속 계면 분해 kinetics 무도핑과 동등),
도핑 유래 결합(BS₃·P–O)은 **계 최강의 국소화 결합**으로서 매몰 기하에서 완전 생존한다.
직접 Li-접촉 종단 스캔은 여기에 기하-의존 보정을 단다: **매몰 = 불활성 생존자, B-노출 =
희생 방패(host 2.6× 보호), O-코너-노출 = 비보호·가속(소수 패치)** — 시험한 어떤 기하에서도
체적-평균 계면 성능은 악화되지 않는다.

**핵심 수치 카드**

| 축 | 무도핑 LPSCl1.6 | B₂O₃-doped | 판정 |
|---|---|---|---|
| Ea (MD, 3-seed×3-T) | 0.197±0.032 eV | 0.199±0.034 eV | **동등** ✅ |
| σ 비율 (T별) | 1 | 1.08 / 0.82 / 1.15 | 동등 (대칭 산포) ✅ |
| B₀ (DFT-EOS) | 21.7 GPa | **24.5 GPa (+13%)** | 강화 ✅ (Cij bulk 27 교차검증) |
| Band gap (band-edge) | 2.10 eV | 1.97 eV | clean insulator 유지 ✅ |
| 산화 onset (ESW) | 2.14 V | 2.03 V | 동등 ✅ |
| E_above_hull (UMA-일관) | 16.7 meV/atom | 37.5 (+20.8) | 둘 다 합성가능 준안정 ✅ |
| 계면 분해 (매몰, 3-seed) | 26±0 % | 22±9 % | **동등** ✅ |
| 계면 최전선 위계 (100 ps) | PS₄-노출 ~22% | B-노출 **8.4%** / PS₂O₂-노출 33.9% | 기하-의존 (§6) ✅ |

---

## 1. 시스템 — 구조·배위·열역학

- **챔피언 구조**: 124-atom modelc_2x 프레임에 B₂O₃ 도핑 → 128-atom. 국소 배위 = **삼각평면
  BS₃ thioborate**(B–S 1.83 Å) + **O는 phosphate 코너로**(P–O 1.56 Å; free-S 아님). B–O 결합 없음.
- **열역학 독립 입증 (convex hull, UMA-일관)**: E_above_hull **37.5 meV/atom** (무도핑 16.7,
  Δ+20.8) — 둘 다 합성가능 준안정(≲50 meV/atom, Sun 2016). 결정적으로 hull 분해산물에
  **Li₃BS₃(삼각 BS₃)와 Li₄B₇ClO₁₂(borate)**가 등장 → 열역학이 "B→thioborate, O→borate"를
  독립적으로 예측 = 구조 분석의 BS₃/O-on-P 결론과 이중 확인. ✅
- 사이트 선호 재확인 (2026-07-09 LPSOCl 스크리닝): O-on-corner가 free-S 대비 **1.29 eV** 우세
  — O의 phosphate-코너 선호는 조성이 달라도 재현되는 강한 화학. ✅

## 2. 이온 수송 — "O를 넣고도 전도 보존"의 수지 균형

- **최종 수치 (정직한 멀티시드)**: Ea 0.199±0.034 (doped) vs 0.197±0.032 eV (무도핑),
  σ 비율 1.08/0.82/1.15 (3-seed × 3-T) — **완전 동등**. 예비 단일시드의 "1.33× 개선"은
  시드 노이즈(600 K ±24%)로 판명, 철회. ✅
- **미시 회계**: O 3개가 Li–O 트랩(ELF 0.780, 1.91 Å)을 만들어 σ를 깎을 뻔했으나 **면내 BVSE
  채널 부피 +45% 개방이 상쇄** → 순효과 0. "황화물에 O를 넣으면 전도가 죽는다"는 통례가
  **배치(코너-O) + 채널 재편**으로 회피됨. ✅

## 3. 기계적 강화

- 사슬: 짧은 결합(B–S 1.83 / P–O 1.56 ≪ P–S 2.07 Å) → 강한 ICOHP(−7.8/−8.6 vs −6.0)
  → **B₀ +13%** (EOS 24.5 vs 21.7 GPa; Cij Bulk 27 교차검증). host 전하 불변(Bader) = 이온적
  연화 없음. ✅
- 스코프: 전단(G/E)은 relaxed-ion basin 문제로 미보고 — **"압축 강성 B₀"로 한정 인용**.

## 4. 전자구조 — 국소화 프레임워크 (왜 이 재료가 작동하는가)

**요지**: 고체전해질의 존재 조건 = "이온은 흐르고 전자는 갇힌다". 전자 국소화가 절연①·
산화저항②·환원저항③·강성④의 공통 뿌리이되, Li⁺ 경로의 음이온 표면은 무르게 남아야
한다(균형⑤). LPSCl은 그 균형을 타고났고, B₂O₃는 균형을 깨지 않으면서 국소화 이점만 추가.

**4.1 국소화의 3층위 측정** (하나만 보면 속는다 — §5의 P–S 반례)

| 층위 | 지표 | 핵심 값 (b2o3 / LPSCl1.6) |
|---|---|---|
| 실공간 | ELF | **B–S 0.959(계 최강)** > P–S 0.945≈0.944 > P–O 0.930 ≈ Li–S 0.93–0.94 > Li–Cl 0.884 > **Li–O 0.780(트랩)** |
| 전하 | Bader | Li +0.88(청정 캐리어), S −1.7~−1.9, Cl −0.91, **O −1.92**, B +3.0 |
| 에너지 | PDOS mean-3p | free-S −0.90~−1.14(최취약) ≪ B–S −2.15 ≈ PS₄-S −2.23 < Cl −3.0 < **O −3.64(최심)** |

**4.2 절연 (①)**: gap **2.10 → 1.97 eV (band-edge eigenvalue 관례** — smoothed-threshold
1.96/2.07과 혼용 금지**)**, N(E_F)=0, in-gap ≤1e-4. −0.13 eV는 가장자리 이동이지 gap 상태가
아님(CBM의 O 기여 0%, B 10%). 절연 실패의 두 모드(자가방전·내부 Li 석출)가 잠김. ✅

**4.3 산화 저항 (②)**: "가장 덜 갇힌 전자가 먼저 산화된다" — 취약 서열 = free-S(−0.9)이며
도핑이 추가한 전자(B–S/P–O/O)는 전부 그보다 깊음 → **산화 취약점 무추가**, onset 2.03≈2.14 V의
미시 근거. 개선의 정공법은 얕은 free-S 관리(Cl-rich화)임도 명시. ✅

**4.4 균형론 (⑤)**: 전자는 PS₄ 공유결합 내부에 감금하되 S 표면 전자구름은 무르게(Li 활강로)
— 절연과 전도가 같은 음이온 위에서 양립. B₂O₃는 이 균형을 안 깨고(§2 회계) 국소화만 추가. ✅

**4.5 회계표**: host 지표(P–S ELF/ICOHP, Li–Cl, CBM 조성, Li 전하) 전부 불변 + 신규 국소화
(B–S 0.959, P–O 0.930, O −3.64 eV/−1.92e)만 추가. 대가는 Li–O 트랩 하나 → 채널 개방으로 상쇄. ✅

## 5. σ\* 궤도 제어 — 환원분해의 미시 메커니즘과 유효 범위

- **원리**: 환원 = CBM 채우기 = CBM을 구성하는 결합의 σ\* 채우기 = 그 결합의 절단.
- **측정 (COHP 비점유측)**: σ\* onset **P–S +0.10 / B–S +0.75 / P–O +1.61 eV** above CBM;
  결합당 접근가능 σ\* 무게 P–S가 B–S의 3.7×, P–O의 5.8×; CBM 조성 S46+P27 (B10, **O 0%**). ✅
- **매몰 기하 MD와 정합**: 주입 전자는 P–S σ\*로만 → host P–S만 절단(P–Li 0.8→4.2 연속 상승),
  BS₃(9/9)·P–O(3/3 + 이후 누적) 온전. "강한 결합은 두 번 보호한다"(σ 깊음=산화저항,
  σ\* 높음=환원저항). ✅
- **열역학 역설 해소**: ESW는 B 환원(1.72 V)을 host(1.24 V)보다 먼저 지목하지만 열역학은
  산물의 순위, 궤도는 경로의 문 — B쪽 acceptor 문이 없어 전자는 P 채널로 (kinetic/orbital control).
- **유효 범위 (2026-07-09 종단 스캔으로 실측 확정)**: σ\* 게이트는 **매몰/제한-플럭스 regime의
  법칙**. 직접 금속 접촉(무제한 플럭스)에서는 **두 낮은 게이트(P–S +0.10 · B–S +0.75)가 clean
  build에서 견고하게 무너짐**(멀티시드·두 cleave). **가장 높은 게이트 P–O(+1.61)는 접촉면에서
  시드-분할** — roll-0.71 재시험 per-atom: **s2는 온전 P–O 2개 절단(2→0, 노출 O→Li₂O-like), s3는
  P–O 2개 유지(2→2)하고 P–S만 절단(O–P 1→1, O–Li 3→4)**. 즉 P–O 게이트는 2 시드 중 1에서만 무너짐
  (가장 높은 게이트답게 절반은 버팀 = σ\* 순서와 정합). 단 두 시드 모두 PS₂O₂는 PS₄보다 빨리 붕괴
  (집계 P–S 손실 35.7/32.0). 접촉면에서는 열역학 순위가 실현되며, 보호 여부는 게이트 높이가 아니라
  **산물의 계면 잔류(앵커링)**가 결정. ✅
- **PS₃O 스탬프(07-11)로 통일 독법 완성**: P–O는 '확률'이 아니라 **'마지막에 끊기는 결합'**이다 —
  S가 전부 벗겨진 P에서만 절단(PS₃O 2/2: 전선 cage가 relax+평형 중 **초고속 붕괴**해 production 시작 전
  이미 P–S 0, 이후 P–O 1→0, 매몰 2.5 Å O → Li₂O-like; PS₂O₂ s2 동일), 붕괴가 100 ps 내 미완결이면 생존
  (PS₂O₂ s3). 즉 'PS₂O₂ 시드-분할'의 실체 = **붕괴 완결 여부**. **접촉면에서 σ\* 사다리는 '절단 순서'로
  실현**(P–S 항상 먼저 → P–O 항상 마지막). 얕은 매몰(2.5 Å)은 보호가 아니며, production-창 집계는 전선
  피해를 과소평가. ✅
- **설계 규칙 (cascade Layer-2 descriptor)**: ① σ\* onset ≫ CBM ② CBM projection 미미
  ③ mean-3p ≪ free-S ④ Li–X ELF ≥0.8 또는 상쇄 경로 ⑤ (노출 대비) 환원 산물의 전자차단성
  + 계면 잔류성 — ①–④ 파이프라인 자동화 가능, ⑤는 산물상 계산 필요.

## 6. Li-금속 계면 — 매몰 캠페인 + 종단 스캔 (최종)

**6.1 매몰-기하 통제 캠페인 (3 seed × 100 ps × 3 슬랩, 600 K)** ✅
- **핵심**: 같은 프레임·같은 표면에서 PS₄ 분해 **22±9%(doped) vs 26±0%(무도핑) = 동등.**
  모든 채널(Li₃P·Li₂S·침투 +7원자 표면 국한) 오차 내 일치. 예비 "6× 억제"는 **thin-slab
  artifact**(1× 슬랩 48±8% = 2×의 1.9배) + 50 ps 조기 스냅샷으로 판명, 철회.
- **도핑 유래 결합 전 시드 생존**: B–S 3.00→3.00 (9/9), O–P 1.00→1.00 — 열역학 worst-case
  (금속성 LiB·Li₂O)가 매몰 기하 동역학에서 미실현. 분해는 오직 host P–S 채널.

**6.2 종단(termination) roll-scan — 최전선 위계 (clean-build, cleave 감사 통과, 각 2 seed)** ✅

| 최전선 (같은 프로토콜) | PS₄-결합 손실 | ΔLi 침투 | 도판트/코너 운명 |
|---|---|---|---|
| **B-노출** (BS₃, roll 0.51) | **8.4±1.8%** | **−0.5±1.5 (정지)** | B 리튬화(B–S 1.50, B–Li 5.0–5.5) — **앵커 유지** |
| **PS₄-노출** (통제, r051+r071 두 cleave) | **~22%** (22.2/22.2 · 25.0/19.4) | +4~+9 | 표면 P → Li₃P 전환·전파 |
| **PS₂O₂-노출** (O 코너 2개, roll 0.71) | **33.9±1.9%** | +10±0 | P–S 붕괴(양 시드); P–O는 **시드-분할** — s2 절단(2→0)·s3 유지(2→2) |
| **PS₃O-노출** (P-up, O는 2.5 Å 아래, roll 0.13) | **30.8±7.7%** (통제와 겹침) | +7±2 | 전선 cage **평형 중 초고속 붕괴**(production 시작 전 P–S 0), P–O 마지막 절단(2/2) |
| 매몰 (전 기하 누적) | 무도핑과 동등 | 표면 국한 | B 3.00→3.00 · O 1→1 무결 |

- **B-노출 = 희생 방패** (문헌 메커니즘 ①, LiF/Li₃BO₃형): B가 1번 타자로 환원되지만(ESW 예고
  그대로) 산물 Li–B–S 층이 **S-우리 절반을 문 채 계면에 앵커** → host 2.6× 보호 + 침투 정지.
- **PS₂O₂-노출 = 비보호·가속 방향** (시드 비겹침: 도핑 최소 32.0 > 통제 최대 25.0): O 코너는
  최전선 사면체를 지키지 못함. 붕괴 경로는 **시드-분할**(per-atom): s2는 P–O 자체 절단, s3는 P–O
  유지·P–S만 절단 — 어느 쪽이든 2-O 사면체가 plain PS₄보다 빨리 붕괴(가설: O 코너가 P–S 우리를
  약화 / P–O 절단 후 2-S 잔여의 붕괴 문턱이 낮음). **단, 이는 소수 패치 문제** — O 3/128이라 다결정 표면에서 확률 수 % 미만이고
  체적-평균은 6.1의 "동등"이 실측. **자연 방어 실측 확정 (2026-07-09 밤): O 표면-편석 에너지 ΔE_seg = +0.67 eV (+336 meV/O, UMA)** — O는 표면 코너를 강하게 기피(≫ 합성 kT ~60–70 meV) → 가속-종단은 평형에서 자기-회피. (캐비앗: UMA·스왑쌍 n=1·볼밀 비평형 동결 가능성 명기.) ✅
- **O-코너 용량-반응 (단조)**: 전선 PS₄-결합 손실이 O 코너 수에 단조 증가 — **0 O 22–24% < 1 O(PS₃O)
  ~31%(시드 넓음, 통제와 겹침) < 2 O(PS₂O₂) ~34%(깨끗한 분리)**. 단 production-창 수치라 전선 자체
  피해는 과소평가(PS₃O 전선은 평형 중 이미 붕괴).
- **통합 결론**: **보호는 ①매몰(깊은 매몰만 — 2.5 Å 얕은 매몰은 무효) ②앵커형 희생 산물(B 전용)에서만
  나온다.** 시험한 어떤 기하에서도 체적-평균 계면 성능은 무도핑 대비 악화되지 않음.

**6.3 전기화학 안정성 종합** (오해 방지)
- 산화측(고전압): **동등** (onset 2.03≈2.14 V, 취약 free-S 불변) — "향상" 주장 금지
  (ESW 환원창 축소 0.90→0.31 V로 반격당함).
- 환원측(Li metal): 무도핑과 **동등**(체적-평균) + 열역학 예측 대비 **좋음**(매몰 worst-case
  미실현) + B-노출 국소 **보호**.
- 정확한 문장: *"전기화학 안정성을 개선하지도 훼손하지도 않으며, 도판트-유래 추가 패널티는
  실측상 없다."*

## 7. 방법론 기여 (이 study가 잡아낸 artifact들)

| # | Artifact | 교정 | 제도화 |
|---|---|---|---|
| 1 | 단일시드 "1.33× σ 개선" | 3-seed×3-T 멀티시드로 동등 판정 | 멀티시드 필수 관례 |
| 2 | "6× 계면 억제" | thin-slab(1×, P 5개) 통계 지배 판명 | 같은-두께·같은-프레임 통제 |
| 3 | roll-0.16 "P–O 즉시 붕괴" | cleave가 build에서 P의 S 3개 사전 절단 | **`audit_cleave_bonds.py` 발사 전 필수 게이트** |
| 4 | band gap 1.96(smoothed) 인용 사고 | band-edge eigenvalue 표준(2.10/1.97) | 수치=band-edge, 곡선=smoothed 이원화 |
| 5 | Li₃N NEB 4연속 폭주 (참고: 자매 프로젝트) | 구속 PES-직접 프로파일 채택 | 방법-재료 궁합 문서화 |

## 8. 논문 문장 제안 (EN)

1. "Interface MD (3 seeds × 100 ps) shows the B₂O₃-doped electrolyte decomposes at the same rate as the undoped frame at a Li-metal contact (PS₄ retention 78±9 vs 74±0%), i.e., doping does not compromise interfacial stability."
2. "Both doping-derived bonds survive Li-metal contact intact in the buried geometry (B–S 3.00→3.00, O–P 1.00→1.00 in all seeds); neither metallic LiB nor Li₂O forms — the thermodynamic worst-case reduction is kinetically suppressed, and decomposition proceeds only through the host P–S channel."
3. "B₂O₃ doping neither improves nor degrades electrochemical stability: oxidation onset and the vulnerable free-S site are unchanged, and interfacial decomposition kinetics match the undoped electrolyte."
4. "A thin-slab control revealed a ~2× cell-size artifact in interfacial decomposition metrics, underscoring the need for same-frame controlled comparisons."
5. "A termination scan shows the protection mode is geometry-dependent: buried dopants remain inert spectators, whereas a B-exposed termination undergoes sacrificial lithiation (B–S 3.00→1.50, B–Li→5.0–5.5) that protects the host — PS₄ loss drops to 8±2% versus 22±0% for the P-exposed undoped control at the same cleave, and Li penetration is arrested. In no tested geometry does doping degrade the interface."
6. "A clean-build front-line test (cleave-integrity audited) shows that an exposed PS₂O₂ tetrahedron degrades faster than the intact-PS₄ control at the same depth (34±2% vs 22±3% P–S loss, both seeds). The front-line hierarchy — B-fronted 8% ≪ PS₄ ~22% ≲ PS₂O₂ ~34% — establishes that protection at a Li-metal contact arises only from burial or from a sacrificial product that stays anchored at the interface (realized only by B). The oxygen corners themselves are seed-dependent: in one of two 100 ps trajectories both P–O bonds cleave (the exposed O ending in a Li₂O-like environment), while in the other they survive and only the P–S bonds are lost — consistent with P–O being the most reduction-resistant of the three bonds even at a metallic contact."
7. "Energy-resolved COHP shows the P–S antibonding manifold begins essentially at the CBM (+0.1 eV), while B–S and P–O σ\* states are pushed 0.75 and 1.6 eV higher by their stronger bonding — electrons injected from Li in the buried regime therefore populate (and cleave) only host P–S bonds. At a direct metallic contact the two lower gates (P–S, B–S) are robustly overwhelmed, whereas the highest gate (P–O) is only marginally so (cleaving in one of two seeds), and protection is instead governed by whether the sacrificial product remains anchored at the interface."

## 9. 정직한 한계 · 남은 작업

- **100 ps 미수렴**: 분해 진행 중 — 비교(동등/보호/가속)만 인용, 절대량 금지. 방패층 장기
  자기제한도 100 ps 밖.
- **MLIP 수준**: 계면 반응상(Li₃P/Li₂S/Li–B–S) DFT 단발 검증 미실시 — "동등" 결론은 저위험,
  Li–B–S 방패·Li₂O-like는 "MLIP 수준" 명시 인용.
- **n=2/종단, cleave 1종/종단**; 측면 registry(`--shift_ab`)·a-면 슬랩 미탐색 (선택 확장).
- **hull은 UMA-일관 에너지** — 절대값보다 상대 Δ와 산물 정체가 견고.
- **잔여작업 정리 (2026-07-21 기준)**:
  - ~~O 표면-편석 ΔE_seg~~ ✅ (+0.67 eV, §6.2)
  - ~~PS₃O P-위 종단 시험 (roll 0.13)~~ ✅ (07-11 스탬프 — §5 통일 독법 + §6.2 표 반영 완료)
  - ~~roll-0.71 s2/s3 per-atom 도장~~ ✅ (§5: s2 P–O 2→0 / s3 P–O 2→2, CSV 주석 반영)
  - ⏳ **Li–B–S 산물상 gap/DOS** (설계규칙⑤ 마지막 조각: 희생 방패가 전자차단인지) — 유일한 실질 미완
  - 선택: DFT 도장(계면 스냅샷·hull winner) · 전단 G/E 재시도(strain 0.01) · 측면 registry/a-면

## 10. 데이터/파일 인덱스

| 축 | 파일 |
|---|---|
| 전도 | `db/properties/b2o3_vs_lpscl16_conductivity.csv` (FINAL), `bvse_channel_volume.csv` |
| 기계 | `b2o3_eos_*.{json,csv}`, elastic 관련 |
| Hull | `db/properties/b2o3_ehull_result.json`, `docs/figures/cascade/b2o3_ehull_comparison.png` |
| 전자구조 | `{b2o3,lpscl16}_pdos_element_PERATOM.csv`, `site_pdos_mean3p_summary.csv`, `bader_b2o3_vs_lpscl16.csv`, `{b2o3,modelc}_elf_bonds.csv`, `docs/figures/pdos/*` (gap 2.10/1.97 확정판) |
| σ\* | `docs/figures/icohp/b2o3_COHP_ext.csv` |
| 계면 | `interface_campaign_summary.csv`(매몰), **`interface_termination_scan.csv`(종단, per-seed+판정)**, `iface_timeseries.png`, CIF 스냅샷 6종 |
| 도구 | `tools/oxidation/{build_li_interface,run_li_interface_md,analyze_interface_decomp,audit_cleave_bonds}.py` |
| LPSOCl(자매) | `lpsocl_{dos_gap,eos_dft_result,icohp,interface,md_arrhenius}.json`, `lpsocl_pdos_element_PERATOM.csv`, `lpsocl_arrhenius_origin.csv`, BVSE `bvse_cubic_approx/`(orig 4.74%@0.5) |
| 원본 kb | framework · takeaways · redox_orbital · campaign · convexhull (각 문서 최신판 = 본 보고서와 동기화) |

---

## 11. 3-시스템 진행표 (여경 논문 패키지, 2026-07-21)

O = db 등록 완료 · ⏳ = 진행중 · ✕ = 미실시(선택). 수치는 canonical만 (gap = fixed-occ band-edge).

| 물성 | LPSCl1.6 (modelc) | LPSOCl (+O) | LPSCl1.6@B₂O₃ |
|---|---|---|---|
| BVSE 채널 (원본셀) | O | O (4.74% @0.5) | O (면내 +45%) |
| MLIP-MD Ea (멀티시드) | O 0.197±0.032 | **⏳ 0.284±0.047 → hiT 3-시드 반영 갱신 대기** | O 0.199±0.034 |
| Band gap (fixed-occ) | O 2.099 | O 2.2309 | O 1.9671 |
| EOS B₀ | O 21.7 GPa | O 24.71 GPa | O 24.5 GPa |
| ELF (결합 midpoint) | O | **⏳ SCF+pp 러너 가동 (gabia CPU, 2026-07-21)** | O |
| PDOS (mean-3p, -8..0) | O | O | O |
| ICOHP/COHP | O (비교값) | O | O (+σ\* ext) |
| Bader | O | ✕ (선택) | O |
| Li-금속 계면 MD | O (modelc62 control) | O (07-19, 1× ratio-clean) | O (매몰+종단 §6) |
| Convex hull (UMA-일관) | O 16.7 | ✕ (선택) | O 37.5 |
| ESW 산화 onset | O 2.14 V | ✕ (선택) | O 2.03 V |

**남은 필수 2건**: ① LPSOCl ELF (러너: `tools/electronic/run_lpsocl_elf_gabia.sh` — NC/80/320/fixed/k444, b2o3·modelc와 동일 midpoint 분석으로 `lpsocl_elf_bonds.csv` 등록; **Li–O 트랩 ELF를 b2o3의 0.780과 직접 비교**하는 게 목적) ② LPSOCl Ea 오차막대 완성 (gabia `~/work/runs/lpsocl_md/reseed_hiT/` 수확 → `lpsocl_md_arrhenius.json` 3-시드×3-T 갱신 → Arrhenius 그림·CSV 재생성). B₂O₃ 쪽 유일 미완은 §9의 Li–B–S 산물상 gap/DOS.
