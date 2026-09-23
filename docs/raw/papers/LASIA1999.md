# LASIA1999 — Electrochemical Impedance Spectroscopy and its Applications

> **읽은 기록 (불변).** 에이전트가 2026-09-23 에 PDF 를 읽고 쓴 노트다. 기계용 기록은
> `packages/wrdkit/src/wrdkit/eis/knowledge/lasia1999.json` 이다. 아래에서 말하는 JSON 이 그것이고,
> 원문 인용은 코드가 인용하는 기록에만 남겼다. "우리 코드" 와의 대조는 그날 02:10–02:30 UTC
> 작업 트리 기준이다. 그 뒤 무엇을 고쳤는지는 `docs/syntheses/eis-paper-knowledge.md` 에 있다.
> PDF 는 저장소에 넣지 않는다 (저작권).

## 서지

- A. Lasia, "Electrochemical Impedance Spectroscopy and its Applications", B. E. Conway, J. O'M. Bockris, R. E. White (편), *Modern Aspects of Electrochemistry* No. 32, Kluwer Academic/Plenum Publishers, New York, 1999 — 2장, pp. 143–248.
- 연도 1999 는 장 첫 쪽 하단 각주의 인쇄 표기다 (p. 143). PDF 판권면(PDF 5쪽)에는 eBook 판 ©2002 와 Print ISBN 0-306-45964-7 만 있고 인쇄 연도는 적혀 있지 않다.
- DOI 없음. `papers/b113771.pdf` 의 PDF 160–265쪽 = 인쇄 143–248쪽, 인쇄 쪽 − PDF 쪽 = −17 (`pdf_page_offset`).
- 구조화 레코드 40개와 코드 대조 16건: `kb/LASIA1999.json`. 인용문은 모두 해당 쪽 텍스트와 대조했다.

## 한 줄 요지

회로 응답의 기초에서 시작해 확산(반무한·유한 투과/반사), 흡착, 고체 전극(CPE·프랙털·다공성)의 임피던스, 데이터가 "좋은" 임피던스인지 가리는 조건(선형·인과·안정·유한, KK), CNLS 피팅과 가중, 장비 한계까지 정리한 리뷰이며, 결론은 측정보다 **모델링이 가장 어렵고 오류가 가장 많이 생기는 곳**이라는 것이다 (p. 242).

## 핵심 내용

### 피팅·가중

- CNLS 는 실수부·허수부 잔차의 가중 제곱합 S(식 241)를 Marquardt–Levenberg 로 최소화하며, Randles 류 스펙트럼도 도식법보다 CNLS 가 최선이다 (p. 187, 236).
- 초기값이 멀면 발산한다. "단순 모델 → 고정 → 원소 추가 → 전체 해제" 방식은 국소 최소에 빠질 수 있으니 여러 초기값에서 다시 맞춰 χ² 를 비교하고, 평평한 최소는 큰 상대 표준편차로 드러난다 (p. 236).
- 파라미터 수는 최소로 두고, 추가는 F-검정(식 242)으로 유의할 때만 받아들인다. 인쇄된 기준 자유도가 F(k, N−p) 와 F(k, N−k) 로 엇갈리니 쓰기 전에 정해야 한다 (p. 236–237).
- 모델이 맞으면 잔차는 무작위여야 하고 체계적 경향은 원소가 모자라다는 신호이며, 위상 보드 그림이 시정수 검출에 특히 민감하다 (p. 237).
- 시뮬레이션 스펙트럼에 잡음을 더해 다시 맞추면 파라미터별 잡음 민감도를 알 수 있다 (p. 237).
- 단위 가중은 가장 큰 |Z| 만 반영해 작은 시정수를 놓치고, 최선은 반복 측정 분산의 역수지만 실무에선 드물다 (p. 237).
- 비례 가중(1/Z_i² 또는 1/Z_calc²)은 실수·허수부 정밀도가 서로 독립이라는 전제다. 장비는 두 성분을 같은 감도로 재므로 두 성분에 같은 가중 1/(Z'²+Z''²)을 주는 **모듈러스 가중**이 더 나을 수 있다 (p. 237–238).
- Solartron FRA 에서 실수·허수부 표준편차는 같고 σ = α|Z'| + β|Z''| + γ|Z|²/R_m(식 243) 꼴이며, 밀리옴–메가옴 오차 범위에서 확인됐다 (p. 238).
- 서로 다른 회로 구조(사다리·Voigt·혼합, Maxwell)가 알맞은 값에서 모든 주파수에 같은 스펙트럼을 낸다(식 238–240). 이 모호성이 가장 큰 난제이며 전위·온도·농도 등을 바꾼 계열 측정으로 모델을 뒷받침해야 한다 (p. 232–235).
- 먼저 측정 모델로 원소의 수와 종류를 정한 뒤 과정 모델로 가고, 반원이 하나뿐이면 시정수 하나짜리로 줄인다 (p. 231–232).
- 흡착 중간체 하나인 반응에서도 속도상수를 맞바꾼 두 파라미터 집합이 같은 곡선을 준다 — 식별성 문제다 (p. 196).
- Randles 회로에서 t_f/t_d = 2σ²Cdl/Rct ≤ 30 이면 CNLS 로 속도론 정보를 뽑을 수 있다(VanderNoot) (p. 173–174).

### 소자(CPE·Warburg·다공성)

- CPE 는 Z = 1/[T(jω)^φ](식 177–178)인 '새는' 커패시터이며, T 가 이중층 용량과 같은 것은 φ = 1 일 때뿐이다. T 의 단위는 F cm⁻² s^(φ−1), 용량성 직선은 90°(1−φ) 기운다 (p. 203–204).
- φ = 1 이면 커패시터, 0.5 면 반무한 Warburg, 0 이면 저항, −1 이면 인덕터다 (p. 205).
- CPE 의 원인은 거칠기만이 아니다. 다결정 금속 수준의 거칠기는 관측보다 훨씬 높은 주파수에서만 CPE 를 만들고, Au 단결정의 분산은 특이흡착이 있을 때만 나타났다 (p. 203, 205–206).
- Brug 환산(식 179–181): 차단 전극 T = C^φ·Rs^−(1−φ), 패러데이 반응 T = C^φ·(Rs⁻¹+Rct⁻¹)^(1−φ). Ni 수소발생에서 T·φ 는 전위에 따라 변했지만 환산한 C 는 약 38 µF cm⁻² 로 일정했다 (p. 205).
- Cole–Cole 식(식 175–176)은 (1−φ)90° 기운 반원이며 ln τ 에 대칭인 하나의 넓은 분포에 해당한다 (p. 202).
- 그 분포 G(τ) 를 데이터에서 뽑는 일(DRT)은 부적정 문제라 결과가 잡음에 매우 민감하다 (p. 205).
- 반무한 Warburg 는 Z = σω^−½(1−j)(식 62–63), 위상 −45° 이며 유한한 R·C 조합으로 표현할 수 없는 분포 소자다 (p. 171–173).
- 유한 확산·투과 경계(tanh, 식 92–94)는 저주파에서 실수 √2σl/√D 로 수렴해 전체 임피던스가 Rs + Rct + √2σl/√D 가 된다 (p. 179–181).
- 유한 확산·반사 경계(coth, 식 99–101)는 저주파에서 R_W = √2σl/(3√D) 와 C_W = l/(√(2D)σ) 의 직렬이 되어 허수부는 발산하고 실수부는 일정해진다 (p. 181–182).
- 지수를 일반화한 유한 Warburg(식 226, Macdonald; coth 판은 Inzelt–Láng)는 데이터를 잘 맞출 수 있지만 φ < 0.5 에서 파라미터의 물리적 의미는 분명하지 않다 (p. 223–224).
- de Levie 기공 모델(식 194–200)은 Z = √(RZ)·coth(√(R/Z)·l) 로 고주파 45° 직선 뒤 반원을 보이며, 침투깊이 λ ≫ l 이면 평면 전극, λ ≪ l 이면 Z ∝ Z_el^½ 가 되어 프랙털(φ = 0.5) 모델과 구분되지 않는다 (p. 212–215).
- 직류 분극 하에서는 de Levie 식이 근사에 불과하다. 엄밀한 계산의 직류 저항은 2배였고, 이중층을 CPE 로 바꾸면 φ = 0.91–0.93 으로 잘 맞지만 그것은 모델의 부적합을 가릴 뿐이다 (p. 217).
- 원통이 아닌 기공은 고주파에서 45° 직선 대신 호·평탄부·반원을 보인다 (p. 222).

### 좋은 임피던스의 조건(KK·선형·정상상태)

- 임피던스는 선형·인과·안정·유한 네 조건을 만족할 때만 유효하고, 선형성은 교류 진폭을 절반으로 줄여도 임피던스가 같은지로 확인한다 (p. 224–225).
- 안정성은 s 가 실수일 때 Z 도 실수이고 Re Z ≥ 0(음의 저항 없음)이라는 것이다 (p. 225).
- 정상상태는 스펙트럼을 반복 측정해 보드 그림이 같은지로 확인하고, 주파수를 올리며/내리며 잰 결과 비교도 시간 변화를 잡아낸다 (p. 226, 240).
- 유한성: ω → 0 과 ω → ∞ 에서 임피던스가 일정한 실수로 가야 한다 (p. 226).
- 선형화가 EIS 의 전제이므로 인가 진폭은 ΔE < 8/n mV(피크-투-피크, n = 교환 전자 수), 곧 0-피크로는 그 절반 이하여야 한다 (p. 168).
- KK 관계식(식 229–233)은 실수부↔허수부, 허수부만으로 분극저항, 모듈러스로부터 위상을 준다. 식 230 분자는 'zZ''(ω)' 로 잘못 인쇄됐고, 식 232 는 부호 관례상 양변이 −R_p 다 (p. 226–227).
- 주된 난점은 유한 대역이라 KK 불일치는 조건 위반뿐 아니라 적분·외삽 오차에서도 생긴다 (p. 227).
- Voigt 측정모델·Boukamp 선형 KK(식 234–235): τ_k = 1/ω_k 로 고정해 R_k 만 선형으로 풀고(decade 당 6–7개), 상대 잔차로 비적합 점을 골라낸다. R_k 부호는 자유, τ_k 는 양수이며 KK 는 매우 민감한 기준이다 (p. 227–229).
- 저주파에서 발산하는 계(차단 전극, CPE, 반무한 확산)는 어드미턴스로 KK 를 하거나 병렬 저항을 더한 뒤 변환한다 (p. 227, 229).
- 검증된 데이터를 얻은 다음에 모델링으로 넘어간다 (p. 235).

### 측정 함정

- 나이퀴스트는 주파수를 숨긴다. 용량이 달라도 반원은 똑같고 점의 주파수만 달라지므로 모든 정보가 담긴 보드 그림을 함께 봐야 한다 (p. 154–155).
- 위상 최대의 주파수는 −Z'' 최대(반원 꼭지)의 주파수와 다르다(식 27–28; 예 1658 vs 500 s⁻¹) (p. 156).
- 흡착 중간체는 저주파 유사 유도성 루프를 만들 수 있고, 이때의 R·C·L 은 실제 소자가 아니라 속도상수·전위의 함수다 (p. 194–195, 199).
- 1–10⁵ Ω, 5×10⁴ Hz 이하가 정밀 측정이 쉬운 영역이다. 고임피던스에서는 입력 임피던스(측정값의 100배 이상 필요), 저임피던스에서는 배선·전류측정 저항의 직렬 인덕턴스가 고주파를 왜곡한다 (p. 240–242).
- 보통 decade 당 10점으로 재고, 상한은 포텐쇼스탯 위상지연과 부유 용량·인덕턴스(당시 20–50 kHz), 하한은 보통 1 mHz(5주기에 1시간 23분)다. 스윕이 빠르면 과도오차가 생기지만 적분 10주기·decade 당 5점 이상이면 무시할 수 있다 (p. 239–240).
- 같은 진폭이면 저주파에서 응답은 약하고 잡음은 크다 (p. 165).
- FRA 의 상관 적분은 고조파를 제거하고 적분 시간이 길수록 잡음을 줄이며, 비선형 오차는 기본파와 3차 고조파 측정으로 추정한다(Diard) (p. 160–162).
- 기준전극·루긴 모세관의 위치가 고주파 인공물을 만들 수 있다 (p. 242).

## 우리 코드에 대한 함의

1. **KK 검증기를 `wrdkit.eis` 에 순수 함수로 추가한다.** Boukamp 식 선형 Voigt(τ_k = 1/ω_k, decade 당 6–7개)와 점별 상대 잔차를 돌려주고, 차단 셀(`blocking_verdict` 가 True 이거나 `circuit_end == "blocking"`)은 Y = 1/Z 로 검사한다. 절단된 적분형 KK 는 만들지 않는다. `audit_fit` 의 첫 검사로 둔다 — 검증 후 모델링. 식 232 는 허수부만으로 전체 분극저항을 주므로 맞춤이 보고한 저항 합의 독립 검산으로 쓸 수 있다. (`LASIA1999.kk-linear-voigt-test`, `LASIA1999.kk-blocking-systems`, `LASIA1999.kk-finite-frequency-range`, `LASIA1999.four-validity-conditions`, `LASIA1999.kk-relations`)
2. **`fit.py` 의 가중 명칭을 고친다.** 구현은 측정 |Z| 로 나누는 모듈러스 가중이므로 "proportional"·"Calc-Modulus" 를 "modulus (measured)" 로 바꾼다. 방식 자체는 챕터가 권하는 쪽이라 유지한다(잔차 벡터는 식 241 의 S 그대로다). (`LASIA1999.cnls-weighted-sum-of-squares`, `LASIA1999.proportional-vs-modulus-weighting`, `LASIA1999.error-structure-equal-real-imag`, `LASIA1999.statistical-weights-unit-vs-variance`)
3. **잔차 경향 검사와 F-검정.** `edge_misfit` 를 일반화해 잔차 부호의 연속(runs)을 보고, 회로를 비교할 때(아크 하나 vs 둘, 차단 꼬리 유무) 같은 가중 S 로 F-검정을 한다. 복소 데이터의 자유도 관례(N vs 2N)는 먼저 정한다. (`LASIA1999.residuals-should-be-random`, `LASIA1999.f-test-added-parameters`, `LASIA1999.measurement-model-first-minimal-parameters`)
4. **파라미터 결정성 보강.** 최적해에 측정 잔차 수준의 잡음을 더해 다시 맞추는 부트스트랩으로 야코비안 stderr·씨앗 흩어짐을 보완하고, Randles 류 회로는 2σ²C/Rct > 30 이면 Rct 를 `undetermined` 로 표시하는 사유를 하나 더 둔다. (`LASIA1999.noise-propagation-simulation`, `LASIA1999.vandernoot-time-constant-ratio`, `LASIA1999.local-and-flat-minima`)
5. **`capacitance.py` 환산에 가정을 드러낸다.** 전극 계면 아크에는 Brug(Rs∥Rct) 값을 함께 보이거나 어느 분포를 가정했는지 적는다. n = 0.8, R/Rs = 100 에서 3.17배 차이라 Irvine 표의 칸을 넘을 수 있다. (`LASIA1999.brug-cpe-capacitance`, `LASIA1999.cpe-definition`)
6. **`circuit_end`(이제 `circuit.py`, audit.py 가 사용)를 정밀하게.** 직렬 CPE 의 저주파 위상은 −n·90° 로 적고, 반무한 W 도 |Z| → ∞ 이므로 "안 막는 셀 + 직렬 W" 도 `blocking_element_on_open_cell` 과 같은 수준으로 검사하며, 안 막는 셀(저주파 위상 ≥ −30°)에 "diffusive" 회로를 대안으로 권하는 것도 다시 본다. `Ws` 는 저주파에서 실수로 돌아오므로 막는 소자가 아니고 `Wo` 는 막는 소자라는 현재 분류는 맞다. (`LASIA1999.cpe-definition`, `LASIA1999.semi-infinite-warburg`, `LASIA1999.kk-blocking-systems`, `LASIA1999.finite-transmissive-warburg`, `LASIA1999.finite-reflective-warburg`)
7. **전송선(TL/TLR) 해석 주의.** docstring 의 "저주파 R_ion/3" 은 차단 계면(또는 Rct ≫ R_ion)에서만 정확하고 일반식은 √(R_ion·Rct)·coth(√(R_ion/Rct)) 다. CPE 계면으로 잘 맞았다(n ≈ 0.9)는 것이 모델이 옳다는 증거는 아니며, 45° 스텁이 없어도 다공성일 수 있다 — 감사 문구에 반영한다. (`LASIA1999.de-levie-porous-electrode`, `LASIA1999.de-levie-cpe-hides-inadequacy`, `LASIA1999.pore-shape-hf-deviation`)
8. **드리프트 검사.** 한 파일에 같은 상태의 스윕이 여럿이면(ADR 0022) 공유 주파수에서 비교해 드리프트를 `check` 로 올린다. (`LASIA1999.stationarity-repeat-and-up-down-scans`)
9. **측정 범위 참고 표시.** |Z| 가 1–10⁵ Ω 밖이거나, decade 당 점이 5 미만이거나, 기록된 교류 진폭이 8 mV(p-p, n = 1)를 넘으면 `note` 로 적는다. (`LASIA1999.impedance-range-artefacts`, `LASIA1999.frequency-plan`, `LASIA1999.linearity-amplitude-limit`, `LASIA1999.low-frequency-noise-higher`)
10. **이름 붙이기.** bulk/GB 이름은 Voigt 구조를 가정한 결과일 뿐이므로 커패시턴스 검사(ADR 0040)와 온도·SOC 계열의 일관성을 σ 보고 앞에 둔다. (`LASIA1999.equivalent-circuits-indistinguishable`, `LASIA1999.model-ambiguity-needs-condition-series`, `LASIA1999.kinetic-parameter-permutation-identifiability`)
11. **그대로 둘 것.** `inductive_mask` 가 스윕 맨 위의 유도성 구간만 버리는 정책(저주파 유도성 루프는 셀의 거동일 수 있다), 멀티스타트와 동률 비교, DRT 정규화 스윕, 꼭지 주파수 (RQ)^(−1/n). 찌그러진 R∥CPE 아크 하나는 DRT 에서 넓은 봉우리 하나이므로 그 어깨를 별개 과정으로 읽지 않고, 회로 맞춤과 DRT 는 τ0 = (RQ)^(1/n) 로 서로 검산한다. 화면은 나이퀴스트와 보드를 항상 함께 보인다. (`LASIA1999.low-frequency-pseudo-inductive-loop`, `LASIA1999.drt-inversion-ill-posed`, `LASIA1999.cole-cole-rotated-semicircle`, `LASIA1999.phase-max-not-arc-apex`, `LASIA1999.nyquist-hides-frequency`)
12. **docstring 정정 (`circuit.py`).** CPE 상한 n ≤ 1 의 이유를 "인덕터" 가 아니라 "실수부가 음수 = 음의 저항, 안정성 조건 위반" 으로 적고, n < 1 을 다공성·거칠기의 증거처럼 쓰지 않으며, `_TL` 의 Wn 은 경험적 지수로 적고, `Wo` 에는 저주파 실수축 오프셋이 R/3 이라는 사실을 덧붙인다. (`LASIA1999.stability-no-negative-resistance`, `LASIA1999.cpe-exponent-limits`, `LASIA1999.cpe-origin-not-only-roughness`, `LASIA1999.generalized-warburg-exponent-unclear`, `LASIA1999.finite-reflective-warburg`)

## 우리 코드와 어긋나는 것

- **틀림** — `circuit.py` 모듈 docstring 의 "n > 1 인 CPE 는 인덕터" 는 식 178 과 맞지 않는다. 1 < n < 2 에서 허수부는 여전히 용량성이고 실수부가 음수(음의 저항)가 되어 안정성 조건 Re Z ≥ 0 을 어긴다. 인덕터는 φ = −1 이다 (p. 204–205, 225). 상한 n ≤ 1 자체는 옳고 이유만 틀렸다.
- **부정확** — `fit.py`: "proportional … Calc-Modulus" 라고 적었지만 구현은 측정 |Z| 기반의 모듈러스 가중이다 (p. 237–238).
- **부정확** — `circuit.py` `circuit_end`/`BLOCKING_KINDS`(audit.py 가 사용): 직렬 CPE 는 −90° 가 아니라 −n·90° 로 가고, 반무한 W 도 저주파에서 발산하는데 막는 소자 검사에서 빠져 있으며 안 막는 셀의 대안으로 "diffusive" 회로가 제시된다 (p. 171, 204, 227).
- **부정확** — `capacitance.py` `effective_capacitance`: 아크의 R 만 쓰는 Hsu–Mansfeld 식이다. 챕터의 Brug 식은 Rs(∥Rct)를 써서 더 작은 C 를 준다 (p. 205).
- **부정확** — `circuit.py` `transmission_line` docstring 의 "저주파 R_ion/3": 패러데이 계면에서는 식 198 꼴이 맞다 (p. 214).
- **부정확** — `circuit.py` `_TL` docstring 의 "Wn < 0.5 = 입자 크기 불균일" 은 챕터가 뒷받침하지 않는다 (p. 223–224).
- **부정확** — `circuit.py` `_CPE` docstring 이 찌그러진 아크를 다공성·거칠기 탓으로만 설명한다 (p. 203, 205–206).
- **일치(수치로 확인)** — `W`·`Ws`·`Wo` 식과 저주파 극한, CPE 정의, `transmission_line`(r_electron = 0 에서 de Levie 식과 상대 차 ~1e-16), `inductive_mask` 정책, 멀티스타트, DRT 의 부적정성, 꼭지 주파수.
