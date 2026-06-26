# 🗺️ 접촉모델·소성 LAW 층위 지도 (DEM contact + MPM plasticity) — 종합

> 작성 2026-06-26.  이번 세션에 digest한 접촉역학/소성 14편을 **우리 모델 기준으로 한 그림**에 배치.
> 각 논문 상세 = `papers/<slug>.md`.  목적: 우리 `hooke/hysteresis`·Stage-E·18×연화·f_AM·ε_sphere·MPM-J2가
> 문헌의 *어디*에 anchor되는지, 그리고 **경로 A(항복캡)** 구현 스펙을 한 곳에.

## 0. TL;DR
- **우리 DEM 접촉 = no-cap 점착-탄소성 이력 LAW** (Luding 2008 = 정의서).  항복압(p_y/H) 캡이 *없어서* E를 18× 연화.
- **경로 A = no-cap LAW + 항복캡** (Thornton–Ning 1998 LAW + KE/Jackson–Green/Mesarovic–Fleck/So의 H≈3σ_y).
  real E_SE=24 + p_y캡 → 18× 연화 *없이* 300 MPa porosity 시험 가능 (So 2021이 LPS로 0.98 입증).
- **우리 MPM = von Mises J2 + ν=0.49** — snow(box)·sand(DP) 가지를 *실제로 테스트*(DPC dead-end)하고 재료클래스
  (점착·비압축 결정)에서 유도된 필연.  cap은 homogenized-REV에서만 옳고 resolved-grain엔 틀림.
- **소성 접촉면적 pile-up ≈1.4×** (Storåkers c²·Mesarovic–Fleck a²/2hR₀, 2 독립 ref) = 우리 Stage-E/ε_sphere 근거.
- **SE-SE 점착 = DMT 체제** (작고 단단 → vdW가 접촉 *밖*; pull-off 2πRγ) = `adhesionStiffness`/`--coh` 물리 앵커.

## 1. DEM 접촉 LAW 층위 (우리 hooke/hysteresis가 속한 곳)
| 층 | 논문 | 항복압 캡 | 점착 | 우리 대비 |
|---|---|:--:|---|---|
| **A. no-cap 이력 (= 우리 모델)** | **Luding 2008** | ✗ | k_c (분리 안 함) | ★ **우리 LIGGGHTS hooke/hysteresis 정의서.** k̂₂/k_c/φ_f = m6/m7/m8 |
| | **EEPA (Thakur 2014)** | ✗ | f₀ + **면적의존 k_adh** | Luding + 점착 분리·비선형 n.  면적의존 점착↔Stage-E 면적 |
| | **Pasha 2014** (open) | ✗ | **에너지일관 A_p·Γ** | Luding + JKR jump-in + 미세분말(=SE).  Luding "α=0 파단 무시" 비판 |
| **B. 항복캡 (= 경로 A LAW)** | **Thornton–Ning 1998** | ✅ p_y | JKR | ★ **경로 A LAW.** Hertz→p_y→선형소성(cap)→잔류겹침.  Varkey 2026 사용 |
| | **So 2021** (digest됨) | ✅ H | — | F_th=2/3·H·A_con.  **LPS로 0.98 입증 = 18×연화 대체 실증** |
| **C. FEM EP 기준 (캡의 엄밀값)** | **Kogut–Etsion 2002** | (H=2.8Y) | — | 구-평면 FEM, **유료 CEB 대체**.  항복 ω_c 닫힌형, 완전소성 ω/ω_c=110 |
| | **Jackson–Green 2005** | (H 가변!) | — | ★ **H≠상수 3σ_y**: H_G/σ_y=2.84[1−e^{−0.82(a/R)^{−0.7}}] → a/R>0.2서 Stage-E 면적 과소 |
| | **Mesarovic–Fleck 2000** | (H≈2.8–3σ_y) | — | **異種**(=AM-SE) 엄밀해; soft상 변형집중·stiff≈rigid → **AM-freeze scaffold 정당화** |
| **D. 자기상사 소성면적** | **Storåkers 1997** | — | — | A=2πc²(m)rh, **c²: 0.5→1.43 pile-up**.  Martin–Bouvard 사용 = Stage-E A/B 기준 |
| **E. 점착 이론 (k_c 원전)** | **DMT 1975** | — | **2πRγ** | ★ **SE = DMT 체제**(작고 단단, vdW 접촉밖).  k_c/`--coh` magnitude = 2πRγ |
| | (JKR 1971 유료) | — | 1.5πRγ | 큰·무른 극한; DMT와 Tabor μ로 보간.  **우리는 DMT라 JKR 못 봐도 OK** |

## 2. ★ 경로 A 구현 스펙 (18× 연화 제거 시험 — backlog)
**목표**: real E_SE=24 GPa + 항복캡 → LIGGGHTS에서 300 MPa porosity가 연화 없이 나오나?
- **LAW** = Thornton–Ning eq2(Hertz)→eq9(항복 p_y≈1.6σ_y)→eq19(선형 소성, P=P_y+π·p_y·R*(δ−δ_y))→eq29(잔류겹침 R_p*).
- **p_y** = LPSCl σ_y 0.05–0.30 GPa → p_y 0.08–0.48 GPa.  ⚠ 우리 press 300 MPa와 *같은 차수* → 일부 접촉만 항복
  (Kogut–Etsion ω_c/R=6.43(Y/E)²로 접촉별 항복여부 gate 가능).
- **H 가변 보정** (Jackson–Green): 완전소성서도 H_G/σ_y가 a/R로 2.84→1 감소 → **Stage-E의 상수 H=3 가정을 a/R>0.2
  접촉서 H_G(a/R)로 교체**하면 dense regime 면적 과소 보정.
- **선례** = So 2021(H-cap, LPS 0.98) + Varkey 2026(Thornton–Ning + multi-contact F_mc; TN 단독은 ρ>0.7서 under-stiff →
  F_mc 필요할 수 있음).
- ⚠ EEPA/Pasha는 **캡 없음** → 단독으론 경로 A 아님 (Luding과 같은 층).  "EEPA + p_y캡"이라야 점착포함 경로 A.

## 3. ★ MPM 소성 계보 (snow → sand → 우리 J2)
| 재료 | 논문 | 항복면 | 점착 | 부피 |
|---|---|---|---|---|
| 눈 | **Stomakhin 2013** | 특이값 **box** + 압축경화 | 점착-유사 | 압축성 ν=0.2 |
| 모래 | **Klár 2016** | Drucker–Prager **원뿔** | **0** | 압축성(재배열) ν=0.3, 옆면 등적 |
| **LPSCl SE (우리)** | (champion) | von Mises J2 **원기둥** | 점착 | **비압축 ν=0.49** |
- 동일 EP-MPM 프레임(**F=F_E·F_P + 특이값공간 return mapping**, Stomakhin이 원전), **항복면만 box→cone→cylinder**.
- ★ **우리 DPC dead-end** = sand(DP) 가지를 resolved-grain LPSCl에 시도한 것.  실패 이유(Klár로 설명): 모래는 비점착+
  압축성(grain 재배열) → DP/cap 맞음; LPSCl SE는 점착+거의 비압축(bulk 24≫0.3 GPa) → cap=입자 부피수축=비물리 →
  과압축(champion no-cap 11% vs +cap 0.8%).  → **J2+ν0.49는 재료클래스에서 유도된 필연** (frame[4] 정량화 한계).
- cap의 *옳은* 자리 = **homogenized-REV**(`cap_compaction_heckel.py`, point=powder-with-voids → clean Heckel),
  *틀린* 자리 = resolved-grain.  Klár "모래=연속체 DP"는 우리 REV 수준 대응, resolved 아님.
- **de Vaucorbeil 2020** 리뷰 = 우리 MPM 변종(MLS/B-spline ULMPM) 위치 + image-based 치밀화(scaffold 선례) + contact
  (AM-freeze = MPM 내재 no-penetration의 최소활용) anchor.

## 4. 배터리 DEM peer (frame[5] 독립 확인)
- **Sangrós 2020** (TU-BS) + **Ngandjong 2021** (ARTISTIC): LIB 전극 DEM의 mech+elec+ionic 삼중 — 둘 다 **rigid 구 +
  CONTACT 소성, 형상소성 없음** = 우리 MPM이 메우는 *형상-morphology 절반*이 LIB DEM에도 빠짐 (frame[5] 독립 확인).
- ★ **이온 위상 역전**: LIB는 pore=이온전도체(Bruggeman, 압밀↑→σ↓), 우리 ASSB는 SE망=전도체(Holm, 압밀↑→σ↑) →
  **우리 SE-network 솔버가 LIB pore-Bruggeman을 대체** = 우리 work 정체성.
- **Sangrós bond / Ngandjong SJKR** = CBD 명시화 청사진 (backlog A3; SJKR 끊김·재형성 = PTFE cold-weld `--coh` 직접 모델).
