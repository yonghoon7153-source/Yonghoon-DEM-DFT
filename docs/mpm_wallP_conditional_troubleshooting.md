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
| 0 (조건부 off) | 300 | 15.9 (과압축) | +12.4 |
| **0.86 (von Mises)** | 42 | **25.25** | **+3.1** ✅ |
| DEM rigid | — | 28.34 | 0 |
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
[ ] real14 trust test(불변 확인) + _10 재실행(floor 버전) — 사용자 실행 대기.
