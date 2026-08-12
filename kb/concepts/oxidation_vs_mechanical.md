---
title: 산화안정성과 기계적물성 — 정의·공통점·차이점과 DFT 계산법
date: 2026-08-12
updated: 2026-08-12
tags: [esw, elastic, dft, methodology, concepts]
status: 확정
confidence: high
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: definition
evidenceScope: multi-source-primary
---

전고체전지 고체전해질(SE)을 평가할 때 자주 같이 나오지만 **서로 다른 질문**에 답하는
두 축이다. 섞어 쓰면 "결합이 세니까 안정하겠지" 같은 틀린 추론이 나온다.

---

## 1. 산화안정성 (electrochemical stability window, ESW)

### 정의

전압을 올릴 때(= Li 를 뽑을 때) **이 화합물이 다른 상들로 갈라지지 않고 버티는 상한**.
정확히는 grand-potential 볼록껍질(convex hull) 위에 남아 있는 μ_Li 구간이다.

$$
\Phi(\mu_{\rm Li}) = E - \mu_{\rm Li} N_{\rm Li}, \qquad
V \;=\; -\frac{\mu_{\rm Li} - \mu_{\rm Li}^0}{e}
$$

μ_Li 를 낮추면(전압 ↑) 어느 시점에 경쟁 상 조합의 Φ 합이 더 낮아진다. 그 지점이
**산화 한계**다. 반대쪽 끝(μ_Li 를 올림)이 **환원 한계**이고, 둘 사이가 intrinsic window.

### 무엇이 일어나는가 — 두 가지가 동시에

**전자** — 전압을 올린다 = 전자를 빼앗는다. 어느 원자에서 빠지는지는 **가장 높이 있는
점유 밴드**가 정한다. S²⁻ 3p 는 높고 O²⁻ 2p 는 깊어서, 황화물이 산화물보다 창이 좁다.

**분해** — 전자가 빠진 뒤 원자들이 **어디로 가는가**. 원래 화합물만 봐서는 알 수 없고
가능한 모든 생성물 조합을 알아야 한다. 그래서 데이터베이스 hull 이 필요하다.

### 우리 실측 (경로 인용 — 숫자는 db 가 권위)

`db/properties/oxidation_stability.json` · `db/properties/nd_doped_lpscl_esw.json` ·
`db/properties/llzo_esw.json`

```
comp1  (Li₆PS₅Cl)        산화 한계 2.14 V   → Li₃PS₄ + 0.25 LiS₄ + LiCl + 1.75 Li
modelc (Li₅.₄PS₄.₄Cl₁.₆) 산화 한계 2.14 V   → Li₃PS₄ + 0.1 LiS₄ + 1.6 LiCl + 0.7 Li
nd (Nd₂O₃ 도핑)          산화 한계 1.92 V   ← 도핑이 창을 좁혔다
LLZO (산화물)            intrinsic 창 2.84 V (황화물 0.90 V 대비)
```

### DFT 로 어떻게 계산하나

**방법 A — grand-potential 프로파일 (우리가 쓰는 것)**

```
tools/oxidation/esw_grand_potential.py
  --target "Li6PS5Cl:comp1" --elements Li P S Cl --out esw.json
```

내부적으로 `pymatgen` 의 `PhaseDiagram.get_element_profile(Li, comp)` 를 쓴다
(Mo/Ong/Ceder 방식). 필요한 것:

1. **대상 조성** — 우리 DFT 이완 셀에서 뽑은 화학식 (정수비가 아니어도 된다)
2. **hull 엔트리** — Materials Project 의 그 화학계 전체 (`thermo_types=GGA_GGA+U` 고정)
3. Li 를 open element 로 열어 μ_Li 를 훑는다

⚠ **엔트리 에너지는 MP 값이지 우리 계산이 아니다.** 한 DB 안에서 일관되므로
**상 사이 비교**에만 쓰고, 우리 QE 절대값과 같은 표에 올리지 않는다.

⚠ 대조군은 **같은 원소계 hull 에서** 다시 돌린다. `nd_doped_lpscl_esw.json` 에서
modelc 를 6원소 hull(Cl-Li-Nd-O-P-S)로 재실행해 4원소 hull 결과를 정확히 재현한 것이
"차이가 hull 아티팩트가 아니다" 의 증거다.

**방법 B — 직접 계산 (엔트리가 없을 때)**

생성물 후보를 손으로 정하고 각각을 DFT 로 이완해 형성에너지를 계산한 뒤 반응
자유에너지를 비교한다. 후보를 빠뜨리면 창이 **과대평가**된다 — hull 방식이 안전한 이유.

**방법 C — 명시적 delithiation**

Li 를 하나씩 빼며 이완·SCF 를 돌려 전압 곡선을 만든다. 가장 비싸지만 **동역학적
장벽**과 중간상을 볼 수 있다. hull 은 열역학만 말한다.

---

## 2. 기계적물성 (elastic constants, moduli)

### 정의

작은 변형에 대한 **응력 응답**. 탄성 텐서 $C_{ij}$ 가 원본이고, 나머지는 전부 거기서 나온다.

$$
\sigma_i = C_{ij}\,\varepsilon_j \qquad (i,j = 1\ldots6,\ \text{Voigt})
$$

| 양 | 뜻 | 전지에서 왜 보나 |
|---|---|---|
| $B$ (체적탄성률) | 등방 압축 저항 | 적층 압력·부피 변화 대응 |
| $G$ (전단탄성률) | 형상 변형 저항 | **Li 덴드라이트 억제** (Monroe–Newman) |
| $E$ (영률) | 1축 인장 저항 | 계면 응력·크랙 |
| $G/B$ (Pugh) | 연성/취성 | <0.57 연성 · >0.57 취성 |
| $\nu$ (푸아송비) | 횡수축 비 | 위와 같은 축 |

다결정 평균은 **VRH**(Voigt–Reuss–Hill): Voigt(변형 균일)와 Reuss(응력 균일)의 산술평균.

### 우리 실측

`db/properties/elastic.json` — 예: `dft_0K_clamped_ion_stress_strain_full_Cij` 에
B_VRH 43.59 · G_VRH 20.12 · E_VRH 52.31 · ν 0.30 (GPa)

⚠ **조성별 pseudo/ecut/k 가 다르다.** 교차비교 전 `kb/methodology/elastic_constants.md`
를 확인할 것. 그리고 MLIP 300K/600K 절은 2026-07-23 삭제됐다.

### DFT 로 어떻게 계산하나

**방법 A — 유한변형 stress–strain (우리가 쓰는 것)**

```
tools/modelc_v3/fit_elastic_cij_stress.py
```

1. 셀을 **완전히 이완**한다 (`vc-relax`, 잔여응력 < 0.1 kbar). 이게 안 되면 전부 틀린다.
2. 6개 Voigt 변형 각각에 ±δ (보통 δ = 0.005) 를 준다 → **12회 SCF**
3. 각 변형에서 응력 텐서를 읽는다 (`tprnfor`·`tstress`)
4. $C_{ij} = \partial\sigma_i/\partial\varepsilon_j$ 를 중앙차분으로 적합
5. VRH 평균 → B, G, E, ν

**clamped-ion vs relaxed-ion**

- **clamped-ion**: 변형 후 원자를 안 움직인다. 싸고, 순수 격자 응답
- **relaxed-ion**: 변형 후 내부 좌표를 다시 이완한다. **항상 더 부드럽다**(값이 작다).
  실험과 비교할 값은 이쪽이다.

`elastic.json` 이 두 계열을 따로 담고 있는 이유다. **섞어 인용하면 안 된다.**

**방법 B — 에너지-변형 적합**

$E(\varepsilon)$ 을 2차로 적합한다. 응력을 안 써도 되지만 변형점이 더 많이 필요하고
수렴에 민감하다.

**방법 C — DFPT**

`ph.x` 로 해석적 2차 미분. 정확하지만 USPP/PAW 지원과 구현 제약이 있다.

### 수렴이 여기서 특히 까다롭다

응력은 에너지의 **미분**이라 에너지보다 훨씬 느리게 수렴한다.

- `ecutwfc`·`ecutrho` 를 에너지 수렴값보다 **높게** 잡는다 (Pulay stress)
- k 점도 늘린다
- 이완 잔여응력이 남아 있으면 $C_{ij}$ 에 그대로 실린다

---

## 3. 공통점

**① 둘 다 전자구조에서 나온다.** 결합의 세기와 방향성이 탄성 텐서를 정하고,
음이온 밴드 위치가 산화 한계를 정한다. 뿌리가 같다.

**② 둘 다 0 K 열역학이다.** 온도·속도·미세구조가 안 들어간다. 실제 셀에서는
과전압·계면 반응 속도·결정립계가 지배할 수 있다.

**③ 둘 다 "상 사이 비교" 로 쓰는 게 안전하다.** 절대값은 방법 의존이 크다
(PBE 갭 30–50% 과소, 탄성률 clamped/relaxed 차이).

**④ 둘 다 이완 품질이 지배한다.** 이완이 덜 된 구조면 응력도 형성에너지도 틀린다.

---

## 4. 차이점

| | 산화안정성 | 기계적물성 |
|---|---|---|
| **묻는 것** | 이 상이 **존재를 유지하나** | 이 상이 **얼마나 단단한가** |
| **범위** | 계 전체 (경쟁 상 조합 포함) | 이 구조 하나 |
| **필요한 것** | 화학계 전체의 hull | 이 셀의 응력 응답만 |
| **결과** | 전압 구간 + 분해 반응식 | 텐서 $C_{ij}$ (6×6) |
| **깨지는 방식** | 후보 상을 빠뜨리면 **과대평가** | 이완/수렴 부족이면 임의 방향 오차 |
| **온도** | 0 K hull (엔트로피 없음) | 0 K 조화근사 |
| **우리 도구** | `tools/oxidation/esw_grand_potential.py` | `tools/modelc_v3/fit_elastic_cij_stress.py` |
| **비용** | 거의 0 (DB 조회) | SCF 12회 × 조성 |

### 가장 중요한 차이 — 결합 세기는 산화안정성을 예측하지 못한다

| | P–S ICOHP | 산화 한계 |
|---|---:|---:|
| comp1 | −5.938 eV | 2.14 V |
| modelc | −5.9997 eV | 2.14 V |

modelc 의 P–S 결합이 1% 세지만 **산화 한계는 같다.** 두 계 모두 산화 개시가
S²⁻ → 폴리설파이드(LiS₄)이기 때문이다 — 끊기는 건 P–S 가 아니다.

산화 한계는 `E(생성물) − E(반응물)` 인데 결합 세기는 **반응물만** 말한다.
생성물에도 결합이 있고 폴리설파이드의 S–S 도 세다. 상쇄된다.

**결합 세기가 영향을 주는 경로는 있다** — VBM 을 깊게 만들고(전자 쪽), 형성에너지를
낮춘다(열역학 쪽). 다만 **같은 음이온 화학 안에서는 미세 조정**이고, 음이온 종류
(O vs S)를 바꾸는 효과가 훨씬 크다.

---

## 5. 세 번째 축을 헷갈리지 말 것 — 밴드갭

갭은 **전자가 통과하나**를 묻는다 (SEI 의 전자 차단). 분해되느냐와 다른 질문이다.
`db/properties/sei_electronic.json`.

Nd 판정이 좋은 예다. **독립된 두 축이 같은 방향을 가리켰다**:

- 축 1 (열역학): ESW 창 0.90 → 0.40 V 로 좁아짐
- 축 3 (전자): 그 창 밖 생성물 Nd₂S₃ 갭 0.77 eV — Li₃P(0.709) 옆자리

→ `kb/syntheses/nd_doping_two_axis_verdict.md`

---

## 6. 실무 체크리스트

**산화안정성을 계산할 때**
- [ ] 대상 조성이 **이완된 셀**에서 나왔나
- [ ] hull 엔트리가 한 thermo_type 으로 고정됐나 (혼합하면 E_hull 이 터진다)
- [ ] 대조군을 **같은 원소계 hull** 에서 재실행했나
- [ ] MP 스냅샷 버전·entry ID 를 기록했나 (없으면 재현 불가 — 실제 사례 있음)
- [ ] 절대 전압을 우리 DFT 값처럼 인용하지 않았나

**탄성을 계산할 때**
- [ ] `vc-relax` 잔여응력이 충분히 작나
- [ ] `ecutwfc`/`ecutrho` 를 에너지 수렴값보다 높게 잡았나 (Pulay)
- [ ] clamped-ion 과 relaxed-ion 을 섞지 않았나
- [ ] Born 안정성 조건을 확인했나 (음의 고유값이면 그 구조는 불안정)
- [ ] 조성 간 비교라면 pseudo/ecut/k 가 같나

## 이 문서가 다루지 않는 것

- 유한온도 탄성(준조화·MD), 소성·파괴
- 계면 반응 속도 (hull 은 구동력만 말한다)
- 공간전하층·결정립계 효과
- 실험 비교 (PBE 갭 과소, 0 K 탄성률과 상온 값의 차이)
