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
- ✅ **EMPIRICALLY CONFIRMED (2026-06-27, rounds 3+4 GPU 실행 완료): se-am-drag = 3번째 artifact 확정.**  더 이상
  예측 아님 — 실제 GPU 런 2회(round 3 fixed coef=1.0, round 4 flexible base=2.0)로 검증.  아래 리뷰(wq3sgfk9j +
  wlq429sda) 예측이 empirical로 적중 (round 3: 1mAh_6 void-fill 15.6→17.26 침식; round 4: robust 0.62≈0.64 thin-pair
  구분 실패 + 100_12 더 나빠짐 13.75).  → §13을 이제 "EARNED, empirical-backed"로 승격 (혼자 단정 아님, 4-round CYCLE 근거).
  - **code PASS**(default off byte-identical, 버그 없음) 하지만 **physics = tunable knob, NOT regime-auto.**
  - **결정 논거:** drag는 *local* am_near(3³ AM-fraction, geometry-static)만 본다.  그러나 §13의 진짜 discriminator
    는 **두께(global)** — **100_12(thin)·real_14(thick) 둘 다 am_near 높음** → 한 coef가 둘을 구분 불가 → 100_12
    고치는 coef가 real_14 void-fill도 망침.  isotropic이라 수직 압축(legit densification)도 막음.
  - "coef를 ~4로 올려 16 맞추자"는 **target-dial = artifact 사고**(사용자가 지적).  물리면 *고정* coef 하나가 전
    regime 자동.  drag는 그게 불가(local≠global).  ⇒ **세 번째 artifact.**
  - **GPU 부수발견:** no-drag 100_12가 11.62 ↔ 12.70 = **MPM ~1%p run-to-run variance** (fixed config).  ±1%p는 noise.
    (그 12.70은 drag 아님 — sed가 multi-line run_mpm.sh서 안 먹어 --se-am-drag 미적용이었음, grep로 확인.)
  - **확정 방향 (4× empirical):** 조건부(over-dense)·am-jam(over-loose)·se-am-drag-fixed(1mAh_6 침식)·se-am-drag-flexible
    (thin-pair 구분 실패) **모두 GPU로 artifact 확인**.  ⇒ 코너 porosity = *global* AM 재배열(frame[1] local MPM 한계)
    = DEM 영역, §13 regime-gate = **EARNED, empirical-backed** (round 3+4 완료).  `--se-am-drag`/`--am-jam` opt-in 유지
    (default OFF, production 무영향).  OPEN: round 5(local SE-content 계수) 또는 §13 채택 — 사용자 결정.

## §15 ★ 물리모델 탐색 CYCLE (idea → 반박 리뷰 → empirical → iterate) — 표준 프로세스 (2026-06-27)
사용자 채택.  매 라운드: **(1) 물리 가설 1개 → (2) adversarial 반박 리뷰(죽이려 시도: correctness+physics+regression)
→ (3) 살아남으면 GPU empirical test → (4) outcome 로그 → 다음 가설.**  ⚠ RULE: **empirical test 없이 "확정" 금지**(혼자 결론 X).

| # | 물리 가설 | 반박 리뷰 | empirical test | outcome |
|---|---|---|---|---|
| 1 | wallP 조건부 (f_AM 응력분담 정지) | — | 100_12 GPU: 11.6 (조건부 ON인데 과압축) | ❌ artifact (over-dense) |
| 2 | --am-jam (percolating AM rigid 정지) | — | standalone: 100_12 22.6 / real_14 18.4 | ❌ artifact (over-loose, AM overlap 무시) |
| 3 | --se-am-drag (SE-AM confinement, **fixed** coef=1.0) | wq3sgfk9j: tunable-patch *예측*(local≠global thickness) | GPU: 100_12 11.6→**14.8** / 1mAh_6 15.6→**17.26** | ❌ tunable patch (방향 ✓ but 1mAh_6 void-fill 침식) |
| 4 | --se-am-drag **flexible 물리계수** (AM load-path robustness서 유도, base=2.0) | wlq429sda: robust factor가 thin-pair 구분 못함 *예측* | GPU: 100_12 base2.0→**13.75** (robust 0.62) / 1mAh_6→**17.26** (robust 0.64) | ❌ **반박 confirmed** (robust 0.62≈0.64 thin 둘 동일; am_frac fix가 100_12를 더 망침 14.8→13.75; 1mAh_6 round3과 IDENTICAL) |

★ round 3 결과: (a) 방향 ✓ (11.6→14.8, 옳은 방향). (b) ✗ — fixed coef=1.0이 100_12는 부분개선했으나 1mAh_6 void-fill
(15.6→17.26)을 **침식**.  ⇒ tunable patch (한쪽만 맞음).  → round 4 flexible 물리계수 설계.
★ round 4 결과 (am_frac 버그 fix + coef=f(global AM-robustness), base=2.0): **반박 리뷰 wlq429sda가 정확히 적중.**
robustness factor가 thin 두 케이스에 거의 동일(100_12=0.62 ≈ 1mAh_6=0.64) → flexible coef가 100_12-vs-1mAh_6를
**구분 못함**.  am_frac 이진-fix가 am_near를 약화 → 100_12는 round3(14.8)보다 **더 나빠짐**(13.75); 1mAh_6는 round3과
**완전 동일**(17.26, void-fill 여전히 침식).  ⇒ flexible 계수도 손-튜닝 fixed-coef와 같은 한계: **local MPM이 global
AM-재배열 discriminator(두께)를 유도 불가**.  8mAh = 미실행(zip 없음)이나 real_14(thick, robust=0.00 = drag-off)가
standalone서 이미 thick drag-off 구조 확인 → 8mAh도 동일 예상.

| 5 | **mobile elastic real-E AM** (E=140, softening 無, freeze 아니라 하중-bearing; nu_se=0.49가 soft-bulk 잡았으니 안전하다는 가설) | 3-lens(physics/regression/feasibility) **전부 KILL** + ★ 기존 empirical 발굴 | **이미 실행됨**: dem3d_composite_overshielding.md 4-lever 스크린 (real E=140 AM, e_am 140→40→12→4) | ❌ **기존 데이터로 KILL** (아래) |
| 6 | **frozen AM + platen이 AM-protrusion top(am_top)에 stop, thin-protrude gate** (사용자: "AM이 SE 뚫고 나옴, 면용량 1일때") | 2-lens(physics/honesty + regression/gate) **전부 KILL** + ★ 기존 empirical 2건 발굴 | **이미 실행됨**: round 2(am_jam_z stop) + round 4(n_layers gate) — 양쪽 절반이 각각 로그됨 | ❌ **기존 데이터로 KILL** (아래) |

★ round 5 가설의 출발점은 **옳았다**(사용자 통찰): AM-AM은 영률 안 줄인 *real physics* (SE만 18× softened) → 내가 코너를
"AM softened-E proxy"라 한 건 *틀림*.  하지만 그 real AM에 하중을 주면(=mobile) 어떻게 되는지는 **이미 2026-06-15에
empirical로 실행됨** (`docs/dem3d_composite_overshielding.md`, scripts/dem3d_plastic.py) — 4 라운드 내내 내가 못 본 데이터:
  • resolved-grain 3D DEM, **real E=140 AM**, bulk axial virial → composite **34–41 %** (측정 9–19 %, over-shielded).
  • **AM 영률 sweep 140→40→12→4 = 36→37→38→32 %** (변화 거의 없음) — 즉 round 5가 쓰려던 바로 그 lever(real AM E)를
    이미 쓸어봤고 안 됨.  friction·cohesion·AM-yield 도 전부 실패.  ⇒ over-shielding은 **GEOMETRIC**(SE가 AM 틈에 안 들어가
    있음, rigid-sphere가 FLOW 못 함), contact-force/modulus 문제 아님.  rigid(cap off) ≈ plastic(cap on) ~36 %.
  • **★ 두 force-chain 구분 (내 premise 오류 정정):** (a) **52–56 %** = soft-bulk SE artifact → nu_se=0.49로 *dissolved*
    (CORRECTION 1).  (b) **34–41 %** = geometric rigid-sphere void-fill limit → real E=140, rigid≈plastic, nu_se가 *안 건드림*.
    round 5의 "nu_se가 mobile AM을 안전하게 만든다"는 (a)(b)를 혼동한 것 = 거짓.
  • reliability 문서(§46-47)가 **이미 mobile-AM을 pre-reject**: "force-chain 일부는 SE-bulk 부작용(nu_se 0.49 완화)이나
    AM-mobile 자체는 ③CFL/OOM(n_grid≥384 blow-up) ④drift(측정 skeleton 이탈) 때문에 기각."  feasibility lens 확인:
    scaffold는 SE-only material(line 307), AM은 am_mask(v=0)와 **상호배타** → mobile-AM 코드 path 자체가 없음 + 코너가
    요구하는 n_grid≥300서 OOM.  ⇒ 새 코드 + OOM 위험 무릅써 돌려도 결과는 36–41 % over-shielding 재현(기존 DEM 스크린이 보증).

★ round 6 가설의 출발점도 **부분적으로 옳았다**(사용자 통찰): default servo가 platen을 튀어나온 rigid AM **통과**시켜 SE
과압축(11.6) = 진짜 비물리 지점.  그리고 AM은 frozen 유지(round 5 kill 회피).  하지만 **양쪽 절반이 이미 GPU로 실행·기각됨**:
  • **stop-height (am_top):** code 주석(line 238) — 코너 regime에선 `am_top ≈ am_jam_z` → round 6 = **round 2(am-jam, 22.6,
    real_14 16.7→18.4 깨짐)와 기하학적으로 동일**.  게다가 am_top은 *단일 최고 구* = lone-sphere(무한 국부응력) → percolating
    `am_jam_z`보다 **덜 물리적**(셋 중 최악); am_top ≥ am_jam_z라 production over-loosen은 **≥18.4로 더 악화**.
  • **gate (n_layers thin-protrude):** round 4 `--se-am-drag`의 n_layers gate(line 579-581)와 **동일 스칼라** → 이미 GPU 실행:
    **robust(100_12)=0.62 ≈ robust(1mAh_6)=0.64** = thin-pair **straddle**, 어떤 threshold도 코너 ON / production OFF 분리 불가.
  • **★ 핵심 발견 (이 라운드의 payoff): 코너 discriminator는 2-DIMENSIONAL (두께 × SE-content).**  두 직교 straddle pair가 증명:
    (a) **8mAh_real_14(SE/sol 16%, thick) gap +0.1 ✓** vs **2mAh_real_20(SE/sol 16%, thin) gap +7.1 ✗** → 같은 SE-content, **두께**가 가름.
    (b) **100_12(SE/sol 26%, 코너) vs 1mAh_6(SE/sol 36%, reliable)** → 둘 다 thin 1mAh, **SE-content**가 가름.
    단일 스칼라(am_top·n_layers·drag = 전부 geometry-static)는 한 축을 붕괴 → 반드시 한 pair 오분류.  **이게 모든 patch가 실패한
    이유 = 운이 아니라 차원.**  → §13이 이미 내린 결론(2-변수 validity domain, gateable mechanism 아님)을 정량 재확인.
  • **틀린 target:** 코너 truth ~20 %(cross-capacity bracket), 32.8은 thin loose-packing **DEM outlier** → am_top은 그 outlier를 재현 = 틀린 끝.

★ **누적 결론 (6 라운드, empirical-backed):** mobile AM(하중-bearing) → over-shielding 36–41 %(production real_14 15.6 깨짐);
frozen AM → SE 하중-bearing densify 15.6 ✓(production) 但 코너 over-compress 11.6.  **코너=loose AM 필요, production=frozen AM
필요 → 어느 쪽이냐 선택 = 바로 regime-gate = §13.**  코너 porosity는 BRACKET[frozen-MPM 11.6 하한 … DEM 32.8 상한 (단 32.8도
thin loose-packing outlier 의심 — thick sibling+MPM cross-capacity ~20 %)]; truth는 그 사이 ~20 %, DEM(softened-E overlap)+packing이
owns.  ⇒ §13 = **5중 backed**: (1) 6 GPU 라운드(조건부/jam/drag×2/mobile/am_top), (2) DEM 4-lever geometric 스크린(modulus 포함
전부 실패), (3) 프로젝트 자체 pre-rejection 문서, (4) **코너 discriminator 2-dimensionality 증명**(두 직교 straddle pair),
(5) round 6의 두 절반이 각각 round 2·4서 GPU-기각.  ⚠ PROCESS 교훈: round 5·6 둘 다 **이미 repo에 있던 empirical 데이터**로
죽음 — 새 가설 전에 기존 GPU 로그(§15, dem3d_composite_overshielding, se-am-drag robust)를 먼저 확인할 것.  반박 CYCLE이 두 번 다 그 miss를 잡음.
★ **건설적 대안 (둘 다 lens가 지목):** ~20 %에 *복사 아니라 계산*으로 착지하는 건 이미 있는 **skeleton-spring wallP-conditional**
(§9-11): SE가 `(1−f_AM)·target`을 받아 작은 plastic 증분 *계산* → MPM = DEM_rigid − increment (height-clamp이 못 하는 것),
gate가 SE-content-aware(f_AM/margin) = round 6 geometric gate가 못 보는 그 축.  단 이건 자체 OPEN validation(코너 런) 남음 = "옳은 레인",
"완전 종결"은 아님.
★ OPEN (사용자 결정, 혼자 확정 X): §13 채택 + wallP-conditional(SE-content-aware) validation 마무리 vs round 6 GPU 재확인
(예측 exact: real_14 ≥18.4, 100_12↔1mAh_6 분리 불가 — 기존 결과 재현일 뿐).

## §16 ★ 코너 = SE-sub-functional + thin subset (사용자 통찰 → 강버전 반박 KILL → scoped 생존, 2026-06-27)
계기 (사용자): "round 7 patch 말고, 그 1mAh 코너가 *물리적으로 안 만들어지는 셀*인지 확인해보자."  → MPM을 고치는 게 아니라
**코너 입력 자체가 functional cell인지** 묻는 다른 lane.  ⚠ **첫 강버전(아래)은 사용자 요청 반박 2-lens로 KILL됨 — scoped 버전만 생존.**

### 강버전 (KILLED): "코너 = near-monolayer ∩ SE-starved = 물리적으로 못 만드는 셀"
첫 컷(full_ranking.csv σ, 24케이스 매칭)은 깨끗해 보였음: CORNER 8/8 vs reliable 0/16이 thin∩starved.  **그러나 반박이
정량으로 깸** (lens ac20b5471 circularity/overclaim + a3a4242643 generalization):
1. **CIRCULARITY:** ρ(SE/sol, σ_ionic) = **0.972** → σ_ionic은 SE/sol의 monotone 변환.  "코너는 SE-starved"는 코너의 정의
   (AM-rich/SE-poor)를 *재진술*한 것 = 독립 발견 아님.
2. **near-monolayer는 second axis 아님 (BROKEN):** ★ 첫 컷은 거의 다 1mAh.  반박이 빠진 2mAh 코너 케이스로 확장
   (case_3d_collection.csv — 내 "a-sweep는 σ 없음" caveat가 **사실과 다름**, 31/36이 σ 보유):
   2mAh_a9_p10 **n_layers 3.00**, 2mAh_real_20 **2.68**, 2mAh_a9_50_p10 **2.71** = **near-monolayer 아닌데 코너**.
   full 코너서 SE-starved 13/13 (universal) but near-mono 10/13 (깨짐).  + reliable의 10/16(첫컷)~23/78(전체)도 near-mono
   → 변별 안 됨.  ★ **clincher (같은 두께 control):** 2mAh_real_10 (n_layers 2.99, SE/sol 32, σ **0.126**) → MPM 17.95 ≈
   DEM 17.75 **reliable** vs 2mAh_a9_50_p10 (n_layers 2.71, SE/sol 19, σ **0.0066**) → MPM 9.31 ≪ DEM 18.45 **corner**.
   같은 두께, 반대 결과 → **SE-content가 가르고 두께는 안 가름.**
3. **OVERCLAIM "un-manufacturable":** Bazzoun 80wt% 셀(σ 0.065)은 *실제로 만들어 EIS 측정됨*.  코너 σ 0.025–0.036은 겨우
   ~2× 아래 + 1mAh는 real lab loading.  조립 못 한다는 증거 0 → 맞는 말은 "**sub-functional / 문헌 검증 envelope 밖**".

### scoped 생존 버전 (둘 다 lens가 인정) — 이게 §16의 최종
data: `docs/data/mpm_corner_realizability.csv` (hertz σ, 84케이스: 6 코너 / 78 reliable).
- **SE-sub-functionality(σ_ionic_hertz < ~0.065 = Bazzoun functional 하한)는 MPM-unreliable 코너의 NECESSARY 조건
  (6/6, lens B full 코너 13/13).**  그러나 **NOT sufficient** — reliable 78 중 **22개(σ<0.05)/33개(σ<0.065)도 sub-functional**.
- sub-functional이 reliable로 남는 경로 = **THICKNESS escape (§13 확인):** 8mAh_real_11–15 (SE/sol 16, σ~0.005, **n_layers
  10–12**) gap≈0 = reliable.  2mAh (n_layers ~2.4–2.9)는 borderline(gap 2–4); 1mAh (n_layers 1.3–1.9)는 코너.
  ⇒ **두께는 연속 modulator (8mAh escape → 2mAh borderline → 1mAh corner)**, binary near-monolayer 경계가 아님.
- **VERDICT (scoped):** MPM-unreliable 코너 = **SE-sub-functional ∩ thin (thickness-escape 못 받는)** subset.  코너 셀은
  **sub-functional**(ionic 전송 나쁨, 실제 셀 SE/sol≥38vol%·σ≥0.065보다 아래) — **"못 만든다"가 아니라 "잘 작동 안 하는,
  문헌 envelope 밖 설계".**  → §13 보강: **MPM은 functional 셀(σ 충분) 전체 + thick 셀(thickness-escape) 전체에서 신뢰;
  과압축은 thin × sub-functional corner에만.**  단 이는 코너의 SE-poor 정의를 크게 재진술한 것(ρ0.97) — non-circular 가치는
  *literature functional 하한*(Bazzoun)을 코너가 넘어선다는 **외부 anchor** + thickness-escape의 연속성뿐.
- **정직한 정정 기록:** (1) 강버전 "un-manufacturable" overclaim → "sub-functional/envelope 밖"로 격하.  (2) "near-monolayer
  = 2nd realizability axis" = **틀림** (2mAh 코너 n_layers 3.0; reliable도 near-mono 다수).  (3) 내 "a-sweep porosity-only"
  caveat = **사실 오류** (case_3d_collection에 σ 31/36 존재) → 전체 join으로 정정.  (4) σ=0.0009(100_15)는 솔버 marginal-
  percolation 최약 regime 값 → 단독 근거로 못 씀.
- ⇒ §13의 backing은 유지되나 "강한 physical-realizability law"는 **철회**.  사용자 원래 질문("1mAh 코너 물리적으로 못 만드나?")
  답 = **strict 不可는 아님; SE-sub-functional·문헌 envelope 밖** = 안 좋은 설계지 불가능한 설계 아님.

### §16-lit ★ 제조 envelope 문헌 확인 (b 완료, 2026-06-27) — scoped 결론 GROUNDED
litdb 60편 + 우리 랩 케이스(Kim/Cho/Kang 2024-25) recipe table 추출 (agent af383e5).  코너(87–92wt% AM, SE/sol
16–26vol%, ~15–20µm = 1–2 입자층, mono-large 12µm)를 **실제 제조된 envelope**과 3축 대조:
- **조성 (87–92wt%): EDGE/borderline.**  最-AM-rich *functional* = **Choi 2024(SAIT) 85wt%**(SE 14.25wt%, full pouch
  >800 Wh/kg, 300cyc) + Mun2025 ref[69] 85wt%(10mAh/cm², 96.5%@100cyc).  **88–90wt%는 만들어 cycle은 되나 SE-기아
  열화 regime**: **Kim2024(우리 랩) 90wt% σ_ionic 0.014 mS/cm(80wt%의 ~1/10)**; **Park2020 90wt% = ionic-percolation
  FAILURE(dead-SE 6–20%)**.  코너 SE/sol 16–26vol%는 Choi 85wt% 경계 *at/just below* = 문헌이 SE-기아로 기록한 그 자리.
- **두께 (~15–20µm, ~1mAh/cm²): OUTSIDE.**  실제 fabricated cathode = **40–157µm @ 5–10mAh/cm²** (Mun 156.8 / Lee 120 /
  Choi 105 / Kim2025 full-cell 40–47.5µm).  최薄 = Park2020 ~39µm(그조차 SIM, NCM~8µm).  **15–20µm·1mAh/cm² 황화물
  cathode를 만든 논문 0편** — energy density는 오히려 *더 두껍게*(dry up to 300µm) 민다.
- **modality (mono-large 12µm): OUTSIDE/anti-design.**  high-AM 실제 cathode는 의도적으로 **bimodal**(Choi 4+15µm,
  Kang 3+10µm = packing/loading).  mono-large는 Shi2019(λ=8 small-SE 필요, mono/large-SE FAIL) + Kang(大입자 cracking)이
  보인 under-fill 구성.
- **VERDICT: 코너는 두께+modality축 OUTSIDE, 조성축 EDGE(marginal/degrading).**  ⚠ 정직: 두께는 "**시도된 적 없음/타깃
  아님**"이지 "tried & failed"가 아님(아무도 15–20µm 황화물 cathode를 *시도*안 함); 조성 edge는 same-material(LPSCl+NMC811)
  Choi 85wt% robust ↔ Park/Kim 90wt% fail로 정량 bracket.  ⇒ scoped §16 = literature-grounded: 코너 = 제조 envelope 밖
  (thickness/modality) + 조성 degrading edge = **MPM이 못 푸는 게 아니라 *현실에서 안 만드는/작동 나쁜* 설계.**
- **★ DIGITAL-TWIN 선례 (사용자 "twin 아니면" 고민에 직접 답):** **Park2020이 바로 digital-twin 논문**인데, 거기서도
  90wt% AM에서 ionic-percolation FAILURE(dead-SE)를 모델로 매핑함 → 우리 코너 finding과 **일치**.  즉 "twin이 코너서
  못 푼다"가 아니라 "**twin이 코너 = SE-percolation 실패를 *진단*한다**"가 정상.  우리 랩 Kim2024 90wt% σ 0.014(실측)이
  그 SE-기아를 실험으로 확증.  → twin = functional envelope 전체 예측 + 실패 regime 진단, 둘 다.  코너를 못 푸는 게 흠이 아님.
- **production gate (사용자 "거부?" 질문 답, 이제 threshold가 lit-grounded):** hard-refuse 아님 → **flag+defer+reason**:
  입력 SE/sol < ~26vol%(Choi 경계) AND thickness < ~40µm(최薄 fabricated) → "⚠ out-of-envelope: SE-poor+thin, σ sub-functional,
  porosity는 DEM 사용, |gap|=certificate" output.  §13 regime-gate의 코드판(clamp 아님).

## §17 ★ FINAL LOGIC — production서 막 계수 제거 + outlier disposition + nu_se status (2026-06-27)
사용자 audit("막 계수 넣고 그렇지 않았나?") → production 코드 정리.  commit: mpm_input_from_case.py.

### A. 적용 코드 = pure scaffold + hold (wallP conditional 제거)
production 경로 = webapp [MPM input 변환] → `mpm_input_from_case.py` → `run_mpm.sh` → `mpm3d_compaction.py`.
변경 전 주입하던 **`--am-load-frac`(Love-Weber f_AM 스프링) + `--floor-porosity`(DEM−5 HARD porosity 클램프) 제거.**
이 둘은 descent 단계(mpm3d_compaction.py:716-748)서 *live*였음(hold는 descent 후 platen 고정뿐) → inert 아니었음.
- floor = porosity 클램프 = §13 "조작" — 진짜 |DEM−MPM| gap을 가림(그 gap이 validity 증명서인데).
- **제거 효과:** in-envelope ~80 = **BYTE-IDENTICAL**(floor 위서 멈춰 `engage=(floor−por)/floor_engage→0` → `am_skel=0` →
  이미 pure stress); real_14 15.93 그대로.  out-of-envelope 코너 ~11 = 이제 pure로 **정직하게 over-compress**(100_12 ~11.6,
  클램프 DEM−5 아님) → un-clamped gap이 flag.
- **최종 적용 한 줄:** `--am-scaffold --se-dump --periodic --protocol hold --e-se/--nu-se(K-fixed μ-scale) --target-gpa`.
  전부 원칙적(scaffold=DEM골격, hold=LIGGGHTS BC, K-fixed=CORRECTION1).  conditional·--se-am-drag·--am-jam = mpm3d opt-in
  (default 0/off), production 미주입.  mpm3d defaults 확인: am-load-frac/floor-porosity = 0.0.

### B. outlier disposition (porosity)
- **in-envelope: outlier 없음** — 80/cross-validated 전부 |gap|≤4 (real_14 16.7↔15.6).  conditional 제거로 불변.
- **out-of-envelope 코너 ~11(gap>4, positive)**: 1mAh_100_10/12/13/14/15, 2mAh_real_20, 2mAh_a9_p10, 2mAh_a9_50_p10,
  1mAh_8_AMP_S2/S5, 1mAh_9_S2/S3/S4.  전부 **SE-sub-functional(σ_ion<0.065) + thin = §16-lit out-of-envelope**(제조 안 되는
  설계) → **regime-gate: porosity는 DEM 사용, MPM 신뢰 X, |gap|=certificate.**  data: `docs/data/mpm_corner_realizability.csv`.
  ⚠ CSV `mpm_porosity` 칼럼은 conditional 시절 값(stale) — pure 재실행시 더 낮아질 수 있으나 flagged라 production 무관(코너는
  DEM 사용).  negative-gap(SE-rich, MPM>DEM) = 별개 regime(DEM ε_sphere overlap artifact, MPM 신뢰) — 이 변경 무관.

### C. nu_se=0.49 morphology — reasoned likely-intact + MORE physical, GPU 직접비교 pending
사용자 ①의 미검증 건.  **결론: 물리적으로 intact일 가능성 높고 nu0.49가 *더* 물리적 — 단 3D 직접 SEM 비교는 GPU(user box) 남음.**
- **물리 논거:** morphology(SEM core-preserved + boundary-flattening) = PLASTIC SHEAR 현상(σ_y + μ 지배).  nu가 바꾸는 건
  주로 K(bulk): E=1.53서 **nu0.30 → K=1.28/μ=0.588**, **nu0.49 → K=25.5/μ=0.513**.  **σ_y=0.30 불변**, μ는 −13%만 변함.
  → 소성 형상은 ~intact 예상.  K 20×↑(volume-preserving)은 deviatoric/shear 형상을 *안* 바꾸고 비물리적 부피 crush만 차단
  (LPSCl 비압축 ≈ 실제) → nu0.49가 **MORE physical**.  (2D champion E=1.53/σ_y=0.15가 SEM(vis_zoom④) 매치 — 거긴 nu 主레버 아님.)
- **잔여 미검증:** 3D nu0.49의 직접 SEM-morphology 대조(3D는 porosity/coverage/thickness만 검증됨).
- **GPU verify (user box):** `mpm2d_morphology.py --nu-se 0.30` vs `--nu-se 0.49` 형상 출력 → SEM 대조; 또는
  `viz_mpm_morphology.py`로 3D x-z slice.  μ −13%면 boundary-flattening이 *아주 약간* 더 강할 수 있음(확인 포인트).
- status: **reasoned likely-intact + more-physical; GPU 직접비교 1건 남음(blocker 아님, production nu0.49 유지 OK).**
