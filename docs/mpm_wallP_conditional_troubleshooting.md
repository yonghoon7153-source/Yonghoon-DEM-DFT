# TROUBLESHOOTING — scaffold MPM SE-poor over-compression → wallP 조건부 fix (working doc)

진단 doc(증상·regime map)은 `docs/mpm_scaffold_reliability_and_am_freeze.md`.  이 문서는 **fix 추적/구현
working doc** — 문제 → fix 설계 → f_AM 설계 진화 → DEM쪽 할 일 → 테스트 계획 → 상태 체크리스트.

---

## §1 문제 (증상)
scaffold MPM(AM frozen, SE만 소성)이 **SE-poor + mono-large-AM + thin(1–2mAh)** corner에서 과압축:
- input_1mAh_100_15 (10:0, SE/sol 25%, thin): porosity → **0.00%** (DEM 32.8%) = COLLAPSE.  SE가 바닥으로
  흘러내리고 frozen AM만 위에 노출.
- input_1mAh_100_10 (10:0, SE/sol 35%, thin): servo가 target 도달했는데도 **MPM 15.9% vs DEM 28.3%** = BRACKET.
- 8mAh mono-large(real_10/_15)는 **정상**(gap~0) — 두꺼운 AM 다층이 평판을 막음.  → thin-mono-large 한정.

**근본 원인:** frozen AM mask는 v=0(material point 없음) → **wallP 반력에 기여 0**.  실제론 강체 AM 골격이
300 MPa를 받지만(DEM: AM-AM force chain, F/P_c↑), frozen scaffold는 그 load-bearing을 전달 못 함 → SE 혼자
300을 받으려다 (a) 못 만들고 0%까지 내려가거나(COLLAPSE) (b) 자기 몫 이상으로 눌림(BRACKET).

---

## §2 Fix = Tabor식 wallP 조건부 (NOT DEM-rock clamp)
servo 정지 조건을 바꿈 (구현 완료, `--am-load-frac`, commit 70fd236):
```
기존:   wallP_SE ≥ target
조건부: wallP_SE ≥ target × (1 − f_AM)     # AM 분담 f_AM·target은 DEM에서 주입
```
- **Tabor 비유:** Tabor가 contact AREA를 F/H로 cap하듯, 이건 SE 압밀을 AM 하중분담으로 cap = **물리 조건**.
- **DEM-rock(clamp)과 결정적 차이:** clamp는 porosity 출력을 DEM값으로 *복사*(조작, 신뢰성 0).  조건부는
  **BC만 물리로 보정하고 MPM이 porosity를 *계산***(보정된 하중 하) → Tabor처럼 신뢰성 있음.
- 적용 범위: **failure corner에만**.  production bimodal(76% cross-validated)엔 f_AM=0(off) — 안 그러면
  교차검증을 파괴.

---

## §3 f_AM 설계 진화 (★ 천천히 다시 생각한 결과)
| 버전 | 정의 | 판정 |
|---|---|---|
| **v0 von Mises proxy** | f_AM = φ_AM·σVM_AM / (φ_AM·σVM_AM + φ_SE·σVM_SE) | ⚠ **SE-rich서 결함** |
| **v1 production = Love-Weber** | f_AM = σzz^(AM-AM) / σzz^(total), σzz=(1/V)Σ f_z·l_z | ✅ 채택 방향 |

- **v0 결함 (SE-rich):** 분산된 강체 AM은 강성 때문에 stress가 *집중*(Eshelby) → σVM_AM↑ → proxy가 f_AM>0을
  줌.  그러나 분산 AM은 **축방향 하중을 골격으로 전달 안 함** → 진짜 f_AM≈0이어야 함.  von Mises는 "AM이
  stressed"만 보고 "AM이 load-bearing"을 안 봄(percolation gating 없음) → SE-rich porosity를 잘못 올림.
  - v0이 OK인 곳: **mono-large**(AM percolate, coord↓지만 force chain이 하중 독점) → von Mises ≈ 하중전달
    → _10 f_AM=0.86이 합리적 *첫 probe*.
- **v1 Love-Weber (production):** AM-AM 접촉망이 전달하는 **축방향(z) 하중 분율**.  분산 SE-rich → AM-AM 접촉
  거의 없음 → 자연히 ~0.  mono-large 골격 → 큼.  **percolation이 공식에 내장** → 전 regime 자동 정확.
  - σ_ij = (1/V) Σ_contacts f_i^c · l_j^c  (Love-Weber/Christoffersen granular stress)
  - f_AM = [Σ_{AM-AM contacts} f_z·l_z] / [Σ_{all contacts} f_z·l_z]   (l = branch vector, z = 압축축)

---

## §4 DEM쪽 할 일 — **거의 없음 (재실행 불필요)** ★ (사용자 질문 직답)
- 우리 분석 파이프라인이 **이미 contact를 재구성**: `scripts/network_conductivity.py`의 `contact_map`은
  원자 dump(위치+반지름)에서 overlap(δ)+area를 pair별로 만듦(line ~189-207).  그리고 **per-particle von Mises
  stress를 이미 계산**(dashboard에 σVM 비 표시) → 이는 **per-contact 힘벡터 + branch 벡터가 이미 있다**는 뜻
  (von Mises = Σ f⊗l 필요).  ⇒ Love-Weber σzz^(AM-AM) 분율은 **같은 데이터로 계산 가능**.
- **사용자가 DEM에서 추가로 할 일: 없음.**  지금 scaffold용으로 주는 **원자 dump면 충분**(overlap→Hertz force
  재구성은 코드가 함).  LIGGGHTS에 새 contact dump(`pair/gran/local`) 안 떠도 됨.
- **내가 할 일(코드, 다음 단계):** von Mises 계산하는 곳에 **Love-Weber σzz pair-type 분해**를 추가해
  `f_AM = σzz^AM-AM / σzz^total`를 case별로 출력 (post-process 또는 network_conductivity 확장).  그 f_AM을
  `--am-load-frac`에 넣음.  → von Mises proxy를 대체.
- ⚠ 확인 필요(코드 읽을 때): 힘이 **실제 LIGGGHTS dump 값**인지 **overlap→Hertz 재구성**인지.  von Mises가
  나오는 걸로 보아 재구성이 있음 → 어느 쪽이든 branch z-성분만 있으면 σzz 분해 가능.

---

## §5 테스트 계획
1. **_10 corner (von Mises probe):** `--am-load-frac 0.86` + sweep 0.60/0.75/0.86.  기대: porosity 15.9% →
   DEM 28% 쪽으로.  28%에 닿는 f_AM이 effective 값 → Love-Weber 물리값과 비교(검증, fit 아님).
2. **SE-rich 확인:** 18개 SE-rich(SE/sol≥48%)는 이미 MPM>DEM(MPM 맞음).  v1 Love-Weber f_AM≈0이어야 → 조건부
   off → porosity 불변.  ⚠ **v0 von Mises f_AM으로 SE-rich 돌리지 말 것**(잘못 올림).  v1로 f_AM≈0 확인이 곧
   percolation-gating 검증.
3. **비교표:** `docs/data/mpm_dem_porosity_reliability.csv`에 am_load_frac 버전 열 추가 → old MPM vs new vs DEM.

---

## §6 SE-rich 데이터 근거 (기존 corpus, 재실행 없이)
SE-rich 18개 전부 **MPM > DEM** (MPM 11–18% 맞음, DEM 1–11% = ε_sphere overlap artifact):
a5(SE/sol 68%) gap −9.3~−10.8, a6(59%) −7.1~−9.6, a7(48%) −5.2~−6.7.  → SE가 load-bearing상 →
**조건부 OFF(f_AM≈0)이 정답**.  (이게 v0 von Mises의 SE-rich 결함을 드러낸 데이터.)

---

## §7 상태 체크리스트
- [x] 진단·regime map (reliability doc) + 105 case 분류 CSV.
- [x] wallP 조건부 `--am-load-frac` 구현 (Tabor식, opt-in, default off) — commit 70fd236.
- [x] f_AM v0(von Mises) 결함 규명 (SE-rich Eshelby) → v1(Love-Weber) 설계 확정.
- [x] DEM쪽 재실행 불필요 확인 (force vectors 이미 재구성).
- [x] **_10 corner 런 (f_AM 0.86)** — ✅ **DONE 2026-06-26, 검증 성공** (n_grid 384, hold, kserver):
  porosity **15.9% (조건부 없음) → 25.25% (f_AM 0.86)**, DEM 28.34 → gap **12.4 → 3.1 (75% 닫힘)**.
  thickness 19.3µm, coverage AM_P 42/68% (rigid 38/65, 유지).  SE_target 0.042 GPa.  ⇒ frozen-AM 과압축 fix 검증.
- [x] f_AM 출처 검증: 0.86 = DEM von Mises 독립유도(fit 아님) → MPM이 DEM 근처 재현 = cross-consistency.
  잔차 +3.1%p = SE가 42MPa 몫만 받고 큰 void로 소성 flow한 증분(frame[5]; MPM = DEM_rigid − 소성증분, clamp가
  못 하는 *계산*).
- [ ] sweep 0.75(SE_target 75MPa)/0.60(120MPa) — f_AM↔porosity 단조곡선 매핑 (확인용).
- [ ] f_AM v1 Love-Weber extractor 구현 (von Mises 코드에 σzz pair 분해 추가) → SE-rich 자동 f_AM≈0.
- [ ] SE-rich f_AM≈0 확인 (v1로) = production gate 마지막 조각.
- [ ] reliability CSV에 am_load_frac 버전 열 추가.

## §8 RESULT (_10 corner, 2026-06-26)
| f_AM | SE_target (MPa) | MPM porosity (%) | gap to DEM 28.34 |
|---|---|---|---|
| 0 (조건부 off) | 300 | 15.90 (과압축) | +12.4 |
| 0.60 | 120 | 21.78 | +6.6 |
| 0.75 | 75 | 23.56 | +4.8 |
| **0.86 (von Mises)** | 42 | **25.25** | **+3.1** |
| (Love-Weber 0.924) | 23 | ~27–28 (외삽) | ~0 |
| DEM rigid | — | 28.34 | 0 |
★ flat sweep MONOTONE (f_AM↑→porosity↑), 과압축 15.9 → DEM 28.34 매끄럽게 tune; 외삽 f_AM≈0.95에서 DEM 도달.
Love-Weber f_AM=0.924(`dem_am_load_fraction.py`) → ~27–28% ≈ DEM(소성증분 작음) = robust 버전(floor+0.924) production 값.
판정: Tabor식 wallP 조건부가 SE-poor/mono-large frozen-AM 과압축(0%→15.9 over-compress)을 물리적으로 교정.
f_AM은 DEM 응력에서 독립 유도 → cross-consistency(fit 아님).  잔차 3.1%p = 진짜 소성 void-fill(frame[5]).
DEM-rock clamp와 달리 MPM이 porosity를 *계산*(신뢰성 有).  → SE-poor corner fix로 채택 후보.

## §9 ROBUST 조건부 (skeleton-spring, ALL-regime safe) — flat f_AM의 결함 수정 (2026-06-26)
★ **flat `--am-load-frac`는 신뢰 불가 (검증으로 발견):** `scripts/dem_am_load_fraction.py`(Love-Weber
σzz^AM-AM/σzz^total)로 측정하니 f_AM이 **정상 케이스에서도 높음** — _10(mono-large) 0.924, **real14(bimodal,
이미 16.7≈DEM 15.6으로 맞음) 0.847**.  AM이 stiff(140 GPa)라 percolate하면 거의 항상 axial 하중 대부분을 짊어짐.
⇒ f_AM을 전 케이스에 flat 적용하면 real14가 SE_target 46MPa서 일찍 멈춰 **16.7→~28로 망가짐**.  f_AM 크기로는
gate 불가 (von Mises든 Love-Weber든).  _10도 사실 wallP 300에 *도달*함(15.9서) — "wallP 못 빌드"가 아니라
**frozen-AM이 DEM의 loose skeleton(28%)을 못 버텨 SE가 그 밑으로 과압축**.

★ **진짜 판별자 = DEM rigid-packing floor** (skeleton이 jam하는 porosity):
| regime | DEM floor | 거동 | 결과 |
|---|---|---|---|
| real14 (dense) | 15.6 | wallP가 floor *위* 16.7서 target 도달 → AM골격 미engage | **16.7 불변** ✅ |
| SE-rich a5 (DEM 1.7 ε-artifact) | 1.7 | wallP가 floor 위 11서 도달 | **11 불변** ✅ |
| _10 (loose mono-large) | 28.34 | floor 통과 → AM골격 engage → SE+골격=target서 멈춤 | 25–28 (복원) ✅ |

★ **채택 모델 — "AM skeleton-spring"** (`mpm3d_compaction.py --floor-porosity P --am-load-frac f`):
```
am_skel = f_AM·target · clamp((floor − por)/engage, 0, 1)   # floor 위=0, 아래=ramp-in
descend while (wallP_SE + am_skel) < target
```
물리: 강체 AM 골격은 **DEM packing floor에 도달해야** 하중을 받음(rigid jam).  floor 위에선 SE가 전부 받음 →
**dense/SE-rich 불변**(over-correction 없음).  floor 아래선 AM share가 ramp-in → **SE-poor 과압축을 floor 근처서
정지**(+소성증분).  → **모든 regime에서 안전**(사용자 "SE-rich서도 신뢰" 요구 충족).
자동화: `mpm_input_from_case.py`가 scaffold에서 **f_AM 자동계산 + `--floor-porosity {DEM porosity}` 자동주입**
→ run_mpm.sh가 케이스별로 robust 조건부를 자동 탑재 (dense면 자동 off).  scipy 없으면 f_AM=0(legacy).

★ **TRUST TEST (사용자 실행):** real14(또는 임의 dense/SE-rich 케이스)를 **새 조건부로 재실행 → porosity 불변**
이어야 함(16.7 그대로).  바뀌면 floor gating 실패 신호.  _10은 25–28(복원).  둘 다 통과하면 production 채택.

상태: [x] skeleton-spring 구현(mpm3d_compaction --floor-porosity + mpm_input_from_case 자동주입) + compile OK.
[x] ★ **real14 TRUST TEST 통과 (2026-06-26, kserver, n_grid 384)**: A(조건부 OFF) porosity **15.91%** =
    B(--am-load-frac 0.847 --floor-porosity 15.6) **15.91%** — **byte-identical**(coverage 336,831↔336,833 =
    2-voxel 노이즈).  로그: B가 frame15서 wallP 0.3225(>0.3) @ por 15.91% > floor 15.6 → am_skel=clamp(−0.21)=0
    → conditional 미engage → baseline 동일.  ⇒ floor-gate가 dense 케이스를 **완벽 보존**(over-correction 0).
    (15.91 = se-dump 값 ≈ CLAUDE.md 기록 15.93 ≈ DEM 15.6; 이전 인용 16.7은 se_frac cell-fill 모드 = 별개.)

## §10 VERDICT — robust 조건부 ALL-REGIME 검증 완료 → PRODUCTION 채택 (2026-06-26)
| regime | 조건부 결과 | 판정 |
|---|---|---|
| _10 (loose mono-large, 과압축 corner) | 15.9 → 25.25(f_AM 0.86) ~ 28(0.924); sweep 단조(0.6→21.78/0.75→23.56) | ✅ 복원 |
| real14 (dense, 정상 cross-validated) | 15.91 → 15.91 (조건부 OFF, am_skel=0) | ✅ 불변 |
| SE-rich (DEM floor 낮음, ε-artifact) | wallP가 floor 위서 target 도달 → 미engage | ✅ 불변(예측) |
⇒ "SE-rich/dense서도 안전" 요구 충족.  floor-gate = DEM-MPM 일치점에서 자동 ON/OFF.  f_AM(Hertz)은 floor 아래
소성증분만 정하는 2차 knob(--atoms-sigzz로 실제-virial 교차검증 가능).  **wallP 조건부 production 채택**
(mpm_input_from_case 자동주입 → 모든 케이스 robust, dense 자동 OFF).  backlog A2 = DONE.

## §11 ★ 놓쳤던 결함 + 수정 — floor=DEM 전역적용이 정당 소성을 억제 (재실행 전 발견, 2026-06-26)
대량 재실행 전 점검에서 발견: **floor=DEM을 *전 케이스* 자동주입하면 MPM이 DEM 아래로 가는 정당한 소성
densification을 억제**.  MPM은 plastic void-fill로 porosity<DEM이 되어야 정상(MPM 고유값) — 그게 frame[5].
데이터(reliability CSV, gap=DEM−MPM):
- mono-large gap>4 (catastrophic corner) **7** → floor 올바르게 복원 ✅
- mono-large gap 1-4 **6** → 복원(corner, defensible)
- **★ NON-mono gap 1-4 (정당 소성, MPM 1-4%p<DEM) 23** → floor=DEM이면 **DEM으로 잘못 끌어올림 = 억제** ❌
- gap≤0 (MPM≥DEM) **64** → floor OFF, 불변.  (real14가 통과한 건 MPM 15.91>DEM 15.6, 우연히 floor 위)
⇒ 과압축은 **catastrophic 정도**(MPM이 DEM보다 한참 아래)에서만 문제; legit plastic은 DEM 살짝 아래.
**FIX-v1(폐기): mono-large-AM geometry 게이트(r_AM/r_SE≥6)** — ⚠ **버그**: r_SE=1.5면 비율이 4로 떨어져
**a9_p10(r_SE 1.5, gap+15.5 진짜 과압축)을 놓침**.  geometry/비율 게이트는 r_SE 의존이라 신뢰 불가.
**FIX-v2(채택): porosity MARGIN 게이트 (geometry-AGNOSTIC)** — `floor = DEM − WALLP_MARGIN(5%p)`.  AM 골격은
**DEM보다 5%p 넘게 압축될 때만** engage(=catastrophic).  legit plastic(MPM ≤4%p<DEM)은 floor 못 닿아 보존;
catastrophic(gap>5)만 잡힘, **r_SE 무관**(a9_p10도 catch).  margin=5는 데이터 검증: legit max gap **3.9** <
catastrophic min gap **6.3** = 깨끗한 갭 한가운데.  (mpm_input_from_case.py: floor=DEM−5 자동주입, f_AM 전부 계산.)
**★ CROSS-CHECK 전체 107 케이스 (2026-06-26):** CAUGHT 7(전부 mono-large, gap>5: 1mAh_100_15/_10, real_20,
a9_p10, a9_50_p10, 1mAh_8_AMP_S5/S2 → new≈floor) · PRESERVED legit 37 · PRESERVED SE-rich/dense 63 ·
BOUNDARY(4<gap≤5) **0** · caught-but-non-mono **0**.  무결성 완벽.
⇒ **재실행 = 정확히 7개**(catastrophic); 나머지 100개 조건부 OFF → 현 MPM 그대로 → 재실행 불요.  backlog A2 = DONE.

## §12 ★ f_AM 출처 검증 — Hertz 재구성 vs 실제 hooke/hysteresis (real_14 dump, 2026-06-26)
사용자 우려: "우리는 Hertz가 아니라 hooke/hysteresis인데 scaffold extractor의 Hertz f_AM을 믿어도 되나?"
→ real_14 **실제 LIGGGHTS dump**(atom_2060000 + contact_2060000)로 직접 검증.
- **dump 파싱 (검증됨):** contact dump는 `id`와 `force` 사이에 **빈 0열**(c_cpl[9]=0)이 하나 끼어 있어
  실제 total force = 0-idx 열 `[9,10,11]` → **fz=C[:,11]**.  Σfz·lz = **−16.1115 = atom virial(c_strs[3]) −16.1098
  정확 일치**(비율 1.0001) → 파싱·물리 검증 완료.  force_normal=`[12,13,14]`(branch와 cos 0.986).
- **실제 정답 (hooke 접촉력 Love-Weber σzz 분해):** AM-AM **0.670** · AM-SE 0.276 · SE-SE 0.053.
  per-atom virial **AM-phase 0.809**(= AM-AM 0.670 + AM-SE 중 AM 몫 ~0.14).
- **Hertz 재구성 (같은 압축 geometry, 모듈러스 민감도):** E_SE=1.35 → AM-AM **0.843**(과대 +0.17);
  E_SE=24(real) → AM-AM **0.258**(과소, 반대로 튐).
- **판정 (2가지):** (1) 모듈러스는 Hertz에서 거대 지렛대 — E만 1.35↔24로 f_AM 0.843↔0.258.  "연화 유효
  모듈러스가 Hertz의 AM-AM 분담을 부풀린다"는 사용자 직관 **맞음**.  (2) 그러나 **어떤 단일 Hertz
  모듈러스도 실제 0.670을 못 맞춤** — 연화는 위로·real은 아래로, 실제는 그 사이.  간극 = **접촉 LAW 형태**:
  Hertz(δ^1.5·순수탄성) ≠ hooke/hysteresis(선형) + plasticityDepth(AM-AM 0.05 늦게·SE쌍 0.005 일찍 항복)
  + maxElasticStiffness(SE-SE cap 5.0 > AM-AM 1.5) + SE-SE adhesion(1e6).  이 SE-우대 항들이 AM-AM에서
  하중을 떼어 SE로 보냄 → Hertz엔 없음.  ⇒ **믿을 f_AM = hooke 접촉력 직접측정(0.670/0.809), Hertz 아님.**
- **production 영향 (= 없음, 안전):** skeleton-spring이 필요로 하는 건 **AM-phase 총하중**(per-atom **0.809**,
  frozen AM이 AM-SE 하중을 흡수→SE wallP에 안 잡힘).  Hertz scaffold 0.847 ≈ 0.809(차 0.04)로 *오히려*
  필요량에 근접(AM-AM 0.670보다 훨씬 가까움) — 우연한 정렬.  게다가 f_AM이 틀려도 **floor(DEM−5%p)가 상한**
  이라 bounded-safe(과대 f_AM → engage 일찍 → 덜 압축 → 보수적).  → 현 조건부 그대로 OK.
- **원칙적 해결(구현됨):** dump가 있으면 실제 hooke f_AM 사용 — `scripts/dem_am_load_fraction.py:
  am_load_fraction_liggghts(atom_dump, contact_dump)`.  webapp(dump 없음)는 Hertz scaffold + floor 안전망 유지.
⇒ 위시리스트 Tier 0~1(Walton–Braun/Luding/Tabor/Johnson/CEB)이 이 LAW의 물리 근거 — `litdb/WISHLIST.md`.

## §13 ★★ VALIDITY THRESHOLD — MPM porosity는 어디서 믿을 수 있고 어디서 DEM이 owns인가 (2026-06-27)

★ **결정적 재정리** (조건부·am-jam을 *끝까지 구현·검증*한 뒤 earned).  조건부(f_AM 응력분담)도 am-jam(기하 rigid
정지)도 **둘 다 artifact**다 — 100_12에서 조건부=11.6(과압축), am-jam=22.6(과소압축, real_14도 16.7→18.4 깨짐).
*진짜 물리*: 이 코너의 porosity는 **AM 재배열(rearrangement)**이 주도 = DEM의 softened-E/Furnas 영역이지
**SE void-fill(MPM 영역)이 아니다.**  근본 이유 = MPM scaffold가 AM을 frozen-rigid로 둬서 (i) AM-AM overlap
(DEM의 소성 proxy, 300 MPa서 AM 상호침투)을 못 만들고 (ii) AM 재배열을 못 함 → SE만 over-flow.  **frame[1] 본질
한계** (연속체엔 rigid 점접촉·재배열 없음).

### 데이터로 찍은 threshold (reliability corpus 117 케이스)
**90.6% (106/117) reliable** (|gap|≤4).  unreliable = catastrophic(gap>5) **11개뿐**, 전부 한 코너:
```
SE/sol bin   mean gap   catastrophic(gap>5)        reliable(|gap|≤4)
 0-20%          2.3         3/22                       19/22
 25-30%         3.1         7/27   ← 코너 집중          18/27
 30-35%        -0.4         1/24                       23/24
 35-45%        -0.7         0/26   ← 완벽              26/26
 45%+          -8.3         0/18   (SE-rich: DEM ε_sphere 과압축, MPM이 맞음)
```
catastrophic 11개 = **thin(1mAh) + SE-poor(SE/sol ≤32%) + AM-rich(85-92wt%)**: 100_1X(26%)·1mAh_8/9(28-29%)·
1mAh_100_15(25%) + 2mAh **mono-large만**(a9_p10·real_20·a9_50_p10, p=10:0/0:10).

### ★ threshold는 단일 SE/sol 선이 아니라 *두께 × SE/sol* (2D) — "thickness escape"
**결정 증거:** 같은 SE/sol 16%라도 두께가 가른다 —
```
8mAh_real_14 (SE/sol 16%!) DEM 19.1 / MPM 19.0  gap +0.1  ✅
8mAh_real_11/12/13/15 (16%) gap ~0              전부 ✅  ← 초-SE-poor인데 reliable
2mAh_real_20 (16%, mono-large) DEM 29.3/MPM 22.2 gap +7.1 ✗
```
**물리(geometric):** thick(8mAh) → AM 다층이 평판을 *기하적으로 차단* → SE 못 샘 → reliable (AM 주도라도!).
thin(1mAh) SE-poor → AM 층이 1-2개라 평판 차단 못 함 → SE 옆으로 over-flow → 과압축.  ⇒ "AM 주도=불가"가
아니라 **"AM 주도 + thin이라 AM 다층 차단이 없는" 코너**만 불가.  두께가 구제.

### ⇒ Operational regime-gate (validity domain — porosity 보고 규칙)
| 조건 | porosity 진짜 모델 | 근거 |
|---|---|---|
| **SE/sol ≥ 30%** (어느 두께든) | **MPM** ✅ | SE-governed, void-fill = MPM 물리영역 |
| **8mAh** (SE/sol 16%까지) | **MPM** ✅ | AM 다층 차단 → SE 못 over-flow |
| **2mAh bimodal** | **MPM** ✅ (대체로) | mono-large만 ✗ |
| **1mAh + SE/sol <~30% + AM-rich** | **DEM** ✗(MPM 과압축) | AM-재배열 주도, thin이라 차단 없음 |
| **2mAh/1mAh mono-large (10:0/0:10)** | **DEM** ✗ | 같은 코너 (AM 단일층) |

★ **clamp/조작 아님** — regime-gate(옳은 *물리 모델* 선택) + DEM↔MPM 일치(|gap|≤4)를 validity 증명서로 노출.
publishable: "어느 (조성×두께)에서 MPM(SE-소성)이 owns porosity이고 어디서 DEM(AM-재배열)이 owns인가"의 정량 경계.
frame[5] EARNED (단정 아니라 두 patch를 시험으로 소진해서).

## §14 ★ 다음 물리경로 — SE-AM confinement (장거리 migration 억제, 국소 conform 허용) — IN PROGRESS (2026-06-27)

조건부·am-jam(둘 다 artifact)을 버리고 *빠진 물리를 채우는* 방향.  **관찰:** pure-SE σ_y=0.30은 confinement 0서
10%로 calibrated인데, composite SE-poor선 dense-AM이 SE를 가둬야(거의 못 흐름) 함에도 MPM 연속체 SE가 AM 틈으로
**무한정 squeeze** → 과-flow(11.6).  빠진 항 = **AM confinement on SE flow.**
- **물리 가설:** SE는 접촉부서 *국소 소성변형(Sakuda fusion)*은 하되 **AM 골격을 가로질러 장거리 migration은 안 함.**
  AM 밀도가 flow를 modulate → SE-poor(dense AM): 거의 막힘→~DEM / SE-rich(sparse AM): void-fill.  **regime 자동.**
- **구현 후보:** AM-인접 grid node서 SE 속도 drag (local AM-proximity로 스케일) — `--se-am-drag` opt-in.  dense-AM
  근방 SE quasi-static(conform), AM 먼 곳 자유(void-fill).
- **검증 (GPU, 둘 다):** SE-poor 100_12 → ~16-18 (코너 고쳐지나) / SE-rich real_14·1mAh_6 → void-fill 유지(안 깨지나).
  한 coefficient가 둘 다 맞추면 genuine(regime auto); 한쪽만 맞으면 또 tunable patch → 폐기.
- ⚠ **DEM import도 억지 jam도 아님** — AM confinement는 *실재 물리*(SE가 AM에 갇힘).  맞으면 MPM이 porosity를
  물리적으로 내는 길 → §13 코너도 DEM 없이 MPM이 owns 가능.  status: 구현·adversarial 검증 진행.
- ★★ **VERDICT (2026-06-27): se-am-drag = 3번째 artifact.  §13 확정.**  adversarial 리뷰(wq3sgfk9j) + 사용자 통찰:
  - **code PASS**(default off byte-identical, 버그 없음) 하지만 **physics = tunable knob, NOT regime-auto.**
  - **결정 논거:** drag는 *local* am_near(3³ AM-fraction, geometry-static)만 본다.  그러나 §13의 진짜 discriminator
    는 **두께(global)** — **100_12(thin)·real_14(thick) 둘 다 am_near 높음** → 한 coef가 둘을 구분 불가 → 100_12
    고치는 coef가 real_14 void-fill도 망침.  isotropic이라 수직 압축(legit densification)도 막음.
  - "coef를 ~4로 올려 16 맞추자"는 **target-dial = artifact 사고**(사용자가 지적).  물리면 *고정* coef 하나가 전
    regime 자동.  drag는 그게 불가(local≠global).  ⇒ **세 번째 artifact.**
  - **GPU 부수발견:** no-drag 100_12가 11.62 ↔ 12.70 = **MPM ~1%p run-to-run variance** (fixed config).  ±1%p는 noise.
    (그 12.70은 drag 아님 — sed가 multi-line run_mpm.sh서 안 먹어 --se-am-drag 미적용이었음, grep로 확인.)
  - **닫음:** 세 genuine 시도(조건부 over-dense / am-jam over-loose / se-am-drag local-blind) 모두 **동일 근본 이유**
    로 실패 — 코너 porosity는 *global* AM 재배열·두께가 정하고 *어떤 local MPM 기제도* 못 잡음(frame[1]).  ⇒ 코너 =
    **DEM 영역**, §13 regime-gate가 production 정답.  `--se-am-drag`/`--am-jam` 코드는 opt-in으로 남겨 이 탐색을 기록
    (production default OFF, 무영향).  더 이상 patch 추구 안 함(= artifact 쫓기).  **MPM = 90% owns + morphology;
    DEM = thin·SE-poor·AM-rich 코너 porosity.**  EARNED (3× 시험).
