---
title: "회신 O — SDCP doped estimand 카드 전면 반려 (P0, 슬랩 NO-GO)"
date: 2026-08-28
updated: 2026-08-28
tags: [review, codex, sdcp, estimand, verdict]
status: 접수 — 구현 중
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-28
verifiedBy: codex
explored: false
authoredBy: human
effort: max
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 회신 O (2026-08-28) — 원문 보존

> 요청 프롬프트: `kb/reviews/codex_O_prompt_sdcp_doped_estimand_2026_08_28.md`
> 심사 대상: `kb/questions/sdcp_doped_estimand_2026_08_28.md` §1–3 (계산 전 심사 — 결과 없음)
>
> **총판정: P0 — 카드 통째 반려. 슬랩 NO-GO. 재승인 조건 7.**
> 한 줄 요지: *"아홉 번째 실패는 계산 오류가 아니라, 평균적인 실제 재료를 임의의
> 단일 oligomer microstate 로 바꿔 측정한 데서 생긴다."*
>
> 구현 기록은 이 파일이 아니라 카드(`kb/questions/sdcp_doped_estimand_2026_08_28.md`)의
> 「회신 O 반영」 절과 각 db 파일에 있다. 아래는 회신 원문 그대로 (전사 수정 없음).

---

총판정: P0 — 현재 카드는 통째로 반려한다. 슬랩 계산은 승인하지 않는다.
계산 전체를 반대하는 것은 아니다. 화학종·estimand·상태 판정축을 고친 뒤 제한적인 기체상 Stage 0은 가능하다. 현재 설계로 실행하면 아홉 번째 실패는 계산 오류가 아니라, 평균적인 실제 재료를 임의의 단일 oligomer microstate로 바꿔 측정한 데서 생긴다.

## 1. "모노머는 목표 화학종을 담을 수 없다" — P0

좁은 명제에는 동의한다. `n=1, +1 hole`은 명목상 고리당 홀 1개, 즉 100% 산화이므로 25–35% 평균 도핑의 bulk carrier를 대표하지 못한다. 다만 국소 SO₃–표면 결합이나 음성대조 모델로는 쓸 수 있다.
하지만 세 근거는 독립 반복증거가 아니다.

* Löwdin 사슬길이 계열은 동일한 유한 기체상 모델과 동일 분할법의 관측이다.
* 협력자 회신은 백본 캐리어에 대한 정성적 prior다.
* 25–35%는 ensemble 평균 산화도 prior다.

즉 서로 다른 세 축의 triangulation이지, 셋이 함께 "n=3 중앙 홀 하나가 실제 화학종의 바닥상태"를 증명하지 않는다. 특히 50.1%는 임의 문턱보다 0.1%p 높은 값에 불과해 `PASS`가 아니라 `unresolved`다.
숨은 가정도 크다.

* PEDOT/PEDOT의 평균 도핑률이 해당 SDCP batch에도 그대로 적용된다.
* 평균 `1 hole / 3 rings`가 모든 trimer의 중앙 국소 홀을 뜻한다.
* 기체상 oligomer의 상태가 고체 및 LiNiO₂ 계면에서도 유지된다.
* 말단기·conformer·counterion·용매 효과가 작다.
* 탈양성자화와 backbone hole이 1:1로 대응한다.

마지막 가정은 "탈양성자화와 도핑량은 1:1이 아니다"라는 협력자 회신과도 충돌한다.

## 2. n=3이면 충분한가 — P0

충분하지 않다. n=3은 목표 도핑률을 표현하는 최소 정수 모델이지, 사슬길이 수렴 모델이 아니다.
질문을 둘로 분리해야 한다.

* 조성 bracket: `DP3/+1 = 33.3%`, `DP4/+1 = 25%`이므로 n=4가 필수다. `DP5/+1 = 20%`라서 n=5가 자동 필수는 아니다.
* 고정 도핑률 길이수렴: `DP3/+1 → DP6/+2 → DP9/+3`이지만 carrier 수도 함께 변하므로 단순 총에너지 비교는 불가능하다.
* 단일 polaron 크기수렴: `DP3…DP6/+1`을 볼 수 있지만 이 경우 도핑률이 변한다.

최소 pre-slab 세트는 화학량론을 확정한 뒤 `DP3/+1`, `DP4/+1`, 동일 조성의 `DP6/+2` spin-state manifold다. n=4에서 급변할 때 n=5를 추가한다.
수렴은 단일 Löwdin 값이 아니라 다음으로 판정해야 한다.

* Löwdin과 Hirshfeld/IAO 또는 실공간 적분에서 backbone/SO₃ 우세 방향이 동일
* 말단 spin leakage가 사전 문턱 아래
* 인접 크기에서 group-spin 변화가 사전 허용폭 아래
* competing localization의 에너지 순서가 seed·conformer·functional 변화보다 큼
* 핵심 상태는 self-interaction에 덜 민감한 range-separated hybrid로 교차검사

## 3. `ΔE_carrier`의 정의 — P0

현재 식은 carrier-resolved adsorption estimand가 아니다.
같은 slab·분자 reference를 두 상태에 쓰면

ΔE_carrier = E_C(mol-hole) − E_C(slab-hole)

로 reference가 모두 상쇄된다. 이것은 흡착에너지 차가 아니라 복합체의 localization-state 에너지차다. 반대로 상태별로 다른 fragment reference를 쓰면 localization 에너지와 해리채널 차이가 섞인다.
둘을 분리해야 한다.
주 estimand:

E_ads^ad = E_C(s*) − E_S(B₀) − E_M(m₀)

여기서 s* 는 사전 선언한 탐색에서 발견된 최저 복합체 상태다. 함께 보고할 주 관측량은 연속적인 `carrier_retention`이다.
두 국소화 상태가 실제로 재현될 때만 보조 estimand를 연다.

ΔE_loc^vert(R,B,M) = E_C(s_mol; R) − E_C(s_slab; R)

같은 원자조성·전하·NELECT·기하·Hamiltonian·slab topology에서 비교해야 한다. 각 상태를 별도로 이완한 adiabatic 차이는 별도 estimand로 둔다.
현재 `s=(M_tot,m_mol,q_mol,B_slab,R)`은 제어변수와 계산 후 관측값을 섞는다. 다음처럼 나눠야 한다.

```
conditioning:
  formula, DP, protonation, counterions, Q, NELECT, hole_count
  geometry_hash, pose, cell, fixed_or_relaxed
  Hamiltonian/protocol ID
  spin-sector 또는 constraint ID
  slab-topology target

realized diagnostics:
  M_tot
  q_mol[method], m_mol[method], carrier_fraction[method]
  per-Ni signed moment vector와 flip indices
  occupation/redox fingerprint
```

SCF seed의 도착 빈도는 물리적 확률분포가 아니다. 둘 중 한 상태가 서지 않으면 `ΔE_loc=NA_STATE_NOT_IDENTIFIED`로 끝내야 한다. 두 unconstrained 국소최소가 bias 제거 뒤 반복 재현되지 않는다면 fragment-charge cDFT가 필요하다. `NUPDOWN`은 전체 (N↑−N↓)만 고정하므로 분자에 홀을 묶지 못한다. [VASP NUPDOWN](https://vasp.at/wiki/NUPDOWN), [Wu–Van Voorhis cDFT](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.72.024502)

## 4. G1–G6 — P0

* G1: 폐기. 서로 전자수와 spin sector가 다른 분자·슬랩·복합체에 같은 NUPDOWN 값을 요구하는 것은 틀렸다. 필요한 것은 같은 태그가 아니라 같은 state-selection policy다. 한 estimand 안에서 모두 자유 바닥상태를 쓰거나, 선언된 해리채널과 양립하는 대응 constraint를 써야 한다.
* G2: 계별로 분리. `M≈1`은 radical doublet의 필요조건일 뿐 바닥상태의 충분조건이 아니다. neutral/anion/closed-shell bipolaron은 M=0, triplet pair는 M=2, broken-symmetry singlet은 총 M=0이면서 국소 반대부호 spin을 가져야 한다. 경쟁 multiplicity와 SCF stability도 봐야 한다.
* G3: 50% 문턱 폐기. `50.1≥50`은 분할법 오차보다 작은 차이일 가능성이 높다. 연속값과 방법 간 spread를 보고, 방법들이 같은 우세 방향을 낼 때만 분류한다.
* G4: 총자화 판정 폐기. 같은 총자화에도 다른 Ni flip topology가 존재한다. per-Ni signed moment vector, flip indices와 필요시 DFT+U occupation fingerprint로 background basin을 식별해야 한다. carrier transfer 때문에 생긴 국소 Ni 변화는 질문의 답일 수 있으므로 basin 오류와 분리한다.
* G5: 분리. 30 meV는 site-preference 판정바닥이지 carrier-state gap이나 chain-length 수렴 문턱이 아니다. `DP`와 독립 matched-pair 수 `N_pair`도 구분한다.
* G6: 강등. 3.5 Å는 이미지 중첩 검사일 뿐 finite-size 수렴 증거가 아니다. vacuum·lateral cell 증가, dipole correction, carrier fraction과 에너지 수렴을 별도로 검사한다.

빠진 P0 게이트는 원자·전자 보존 반응식, proton/counterion reservoir, 동일 Hamiltonian, SCF·force·entropy 수렴, conformer sampling, vertical/adiabatic 구분, 분할법 강건성, state-existence 재현성이다.

## 5. A1–A7 — P0 재설계

* A1: 유지 가능하나 n=1 reference의 회귀 진단일 뿐 polymer 검증이 아니다.
* A2: `MAGMOM`은 constraint가 아니라 초기조건이다. SO₃ seed와 backbone seed의 fresh-start multistart로 바꾼다. 둘 다 SO₃로 가면 테스트한 초기조건에서 같은 attractor를 지지할 뿐 전역최소를 증명하지 않는다. 서로 다른 해로 남으면 metastable SCF 해의 존재만 증명한다.
* A3: n=3 한 점으로 G3 통과 금지. n=4와 방법·conformer 교차검사가 선행돼야 한다.
* A4: "neutral보다 강한가"를 유지한다면 n-matched neutral은 필요하다. 다만 proton/electron reservoir 없이 두 종의 실제 우세도를 뜻하지는 않는다.
* A5: 현재 주 estimand를 판별하지 않으므로 최소 세트에서는 제외한다. 별도 electron-affinity/화학 검산 목적일 때만 탐색값으로 둔다.
* A6/A7: A7을 두 상태로 분리한다.

```
A6   closed-shell singlet bipolaron 후보
A7a  triplet two-polaron
A7b  broken-symmetry open-shell singlet two-polaron
```

세 상태 모두 같은 n=6·원자조성·protonation·counterion·Q·NELECT에서 비교하고, 먼저 같은 기하의 vertical 비교를 한 뒤 각각 이완한 adiabatic 비교를 분리한다. polaron separation과 conformer도 둘 이상 필요하다. BS determinant는 순수 singlet가 아니므로 정밀한 singlet–triplet gap으로 부르면 안 된다.
같은 조성 안의 sampled state ordering은 비교할 수 있다. 그러나 `2E(n3,+1)`과 `E(n6,+2)`의 직접 비교는 말단·oligomerization 에너지가 섞여 무효다. 필요하면 동일 N에서

U_eff = E_N(+2) + E_N(0) − 2·E_N(+1)

같은 balanced metric을 보조로 쓰되, 원자수·protonation·reservoir가 정확히 같아야 한다.

## 6. wave1 스핀 제약 비대칭 — P0

"확정값은 총에너지 뺄셈이므로 영향 없음"이라는 근거는 틀렸다. 총에너지 뺄셈도 서로 다른 상태의 에너지를 섞으면 편향된다.
다만 0.13 μB 때문에 neutral 결과가 자동으로 틀렸다는 뜻도 아니다. adiabatic estimand라면 흡착 유도 spin polarization은 물리적 완화일 수 있다. 중성 분자의 NUPDOWN=0 해가 자유 바닥상태와 에너지상 같다면 기존 E_ads는 유지된다.
현재 값이

E_ads^old = E_C^free − E_S^free − E_M^{M=0}

이면 분자 reference의 보정은

δ_m = E_M^{M=0} − E_M^{free}

이고 E_ads^ad = E_ads^old + δ_m 다. 이 항은 동일 분자를 쓰는 자세차에는 소거되지만 절대 E_ads와 C10 대비 0.346 eV에는 남는다. 총자화 0.13 μB만으로 δ_m을 제한할 수 없다.
따라서:

* 유지: 원시 총에너지, 명시된 혼합-tag protocol의 조건부 값, 접촉기하, 이미 `NO_VERDICT`인 자리선호
* 조건부 보류: neutral 네 E_ads의 무조건적 "확정값" 지위와 정확한 0.346 eV headline
* 추가 철회 없음: doped E_ads는 이미 비워져 있음

최소 확인은 neutral 및 C10 gas reference를 같은 기하·설정에서 `NUPDOWN=0`과 자유 조건으로 짝계산하고, 자유 복합체를 여러 초기 자화에서 재현하는 것이다. fixed-M=0 estimand를 택한다면 clean slab과 네 복합체까지 모두 M=0으로 다시 계산해야 한다. 상태는 `closed_for_scope_pending_spin_equivalence`가 적절하다.
또한 `slab±1`이 아니므로 홀이 사라졌다는 해석도 성립하지 않는다. 총자화는 fragment-local carrier 위치의 증거가 아니다.

## 7. n=6 바이폴라론 "제3의 길" — P0

문헌 전제를 고쳐야 한다.
Kumar 2018은 `(EDOT6)^+2`와 `(SS6)^−2`를 별도 흡착종으로 사용했고 −0.42 eV/monomer를 보고했다. 이는 공유결합형 자가도핑 중성 `(EDOT-S)6` 모델이 아니다. 논문은 `bipolaron`이라고 부르지만 singlet/triplet 또는 restricted/unrestricted 비교를 보고하지 않으므로 "닫힌 껍질 singlet을 검증해 열린 껍질을 회피했다"는 근거가 아니다. 오히려 표면에서 PEDOT으로의 전자이동과 de-doping을 보고하므로 흡착 중 carrier 상태가 바뀔 수 있다는 경고다. [Kumar et al.](https://www.nature.com/articles/s41467-018-07435-z)
Yano 2019의 0.22–0.35 및 3–4 monomer/charge는 S-PEDOT에서 직접 측정한 carrier fraction이 아니라 "S-PEDOT의 doping level이 PEDOT와 같다고 가정하면"이라는 환산이다. 외부 실측 근거가 아니라 문헌 기반 prior로 강등해야 한다. [Yano et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC6461456/)
고도핑이라고 singlet bipolaron을 선험적으로 고를 수도 없다. PEDOT에서 triplet polaron pair가 실험적으로 관측됐고, 계산에서도 +2 상태의 singlet/triplet 순서는 chain length와 counterion에 민감하다. [Rubio-Govea et al.](https://pubs.acs.org/doi/10.1021/acs.jpcc.4c05602), [PEDOT–counterion 전자구조 연구](https://pmc.ncbi.nlm.nih.gov/articles/PMC11125351/)
따라서 n=3 doublet과 n=6 singlet 중 하나를 미리 고르는 것이 아니라 서로 다른 후보 microstate로 둬야 한다. 실제 분율을 결정하려면 최소한 EPR spin count와 독립 carrier/oxidation 측정, UV–vis–NIR/Raman의 결합이 필요하다. 도핑률 하나만으로 polaron/bipolaron을 선택할 수 없다.
열린 껍질을 "회피"하는 것은 정당화되지 않는다. 실물이 polaron 지배라면 질문을 해결한 것이 아니라 다른 화학종으로 바꾼 것이다.

## 8. 아홉 번째 실패가 생길 자리 — P0

가장 위험한 곳은 평균 재료의 ensemble을 임의의 단일 microstate로 치환한 뒤, 그 조건부 계산을 재료 전체의 답으로 부르는 부분이다.
현재 미정인 것은 다음과 같다.

* 실제 SO₃H/SO₃⁻ 분포
* counterion과 proton/electron reservoir
* polaron/bipolaron 분율
* conformer와 hole 위치의 분포
* 표면에서의 charge transfer 후 admissible state 집합

그런데 카드는 평균 도핑률만으로 "모든 trimer에 중앙 홀 하나"를 선택한다. 이것이 가장 큰 estimand 오류다.
두 번째 위험은 질문의 답을 gate가 삭제하는 것이다. 홀이 slab으로 이동해 Ni moment가 변하면 G4가 이를 basin mismatch로 버릴 수 있다.
세 번째 위험은 두 discrete localized state가 존재한다고 먼저 가정한 것이다. 실제 해가 하나의 mixed state뿐이면 `ΔE_carrier`의 정의역이 빈다.
마지막으로 현재 규율은 prose에 머물러 있다. 실행 전에 machine-readable `estimand_id`, 정확한 화학식·Q·NELECT, reference reaction, state-selection policy, 허용/중단 코드가 job manifest와 분석기에 연결돼야 한다. 그렇지 않으면 계산자는 다시 수렴 여부만 확인하고 다른 양을 보고할 수 있다.

## 재승인 조건

1. 분자식·protonation·counterion·Q·NELECT·reservoir를 먼저 확정
2. 주 estimand를 adiabatic E_ads와 연속 carrier-retention으로 변경
3. 두 재현 가능한 상태가 있을 때만 보조 `ΔE_loc` 개방
4. G1·G2·G3·G4 전면 교체
5. DP3/+1·DP4/+1 및 동일 n=6 spin-state manifold의 기체상 선행검사
6. neutral wave1 spin-equivalence 짝검사
7. 위 규칙을 machine manifest와 analyzer에 연결

이 일곱 조건 전에는 슬랩 NO-GO다.
