---
title: "H-제거 n=6 라디칼 상태지도 — estimand 카드 v2 (회신 S 반영)"
date: 2026-08-31
updated: 2026-08-31
tags: [sdcp, polaron, orca, estimand, spin-localization, prereg]
status: open
confidence: low
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: single-source
feedsInto: db/properties/sdcp_polaron_pilot_prereg_2026_08_31.json
---

## 질문

**H 원자를 하나 뗀 중성 n=6 SDCP 올리고머 라디칼에서, 홀전자가 EDOT 백본에 있는가
술포네이트 산소에 있는가 — 그리고 그 답이 conformer·H 제거 위치·유전환경·범함수에
얼마나 의존하는가.**

> ⚠ **v1 에서 바뀐 것 (회신 S, 2026-08-31).** v1 은 이 계산을 *"실제 자가도핑 SDCP 에서
> 캐리어가 백본에 있는가"* 라고 불렀다. 그것은 이 계산이 시험하지 않는 물질 수준 주장이라
> **NO-GO** 를 받았다. 이 계산이 답하지 **않는** 것: 실제 시료에서 자가도핑이 자발적으로
> 일어나는가 · H⁺ 와 전자의 reservoir 가 무엇인가 · 실제 산형/염형/수화도/산화도가 무엇인가.

**정본 명칭**: `neutral H-atom-removed n=6 radical model`.

---

# estimand 카드 v2 (`kb/templates/estimand_card.md`)

## 1. 무엇을 원하는가

> H 원자 하나를 제거한 중성 n=6 올리고머 라디칼(`charge 0, mult 2`)의
> **전자상태 지도** — 실현 가능한 SCF 해들과 각 해에서 홀전자의 공간 분포 —
> 이며, **conformer · H 제거 위치 · 유전환경 · 범함수에 조건부**다.

해석 가능한 모델 조건 (회신 S §1):
```
P–SO₃H  →  P–SO₃⁻ + H⁺
P–SO₃⁻  →  [P•⁺–SO₃⁻] + e⁻
```
⇒ 이 계산의 계는 **그 두 단계의 최종 생성물을 조건으로 둔 모델**이다.
H 원자 제거(= H⁺ + e⁻)가 그 과정을 **재현한 것이 아니다**.

**σ_SDCP = 250 S cm⁻¹ 와 기전적으로 연결하지 않는다** — 시편·출처가 미결이다.
**단량체 65/35 를 "전도 전제와 반대" 라고 부르지 않는다** — 단량체는 다중링 폴라론을
구조적으로 담지 못하고, spin 위치는 전도도와 다른 관측량이다.

## 2. 재는 양

### 2-1. Primary — spin share (세 집합, 상호배타·완전)

$$F_G^{(P)} \;=\; \frac{\int W_G^{(P)}(\mathbf r)\,|\rho_\alpha-\rho_\beta|\,d\mathbf r}
{\int |\rho_\alpha-\rho_\beta|\,d\mathbf r}
\qquad F_{bb}+F_{SO_3}+F_{other}=1$$

- `(P)` = 명시된 공간분할 (Hirshfeld primary · Löwdin sensitivity)
- `G` ∈ {`backbone`(EDOT 링 C·S·O, **ring 별로도 분리**), `sulfonate`(S + 3 O), `other`}
- **실공간 적분이 어려우면** `Σ|atomic spin|` 을 근사 경로로 쓴다 — 단 **같은 정의를
  두 분할에 똑같이** 적용한다.
- signed net spin 은 버리지 않고 **`M_bb` 로 따로 보존**한다.

> ⛔ v1 식(`Σ_bb s_i / Σ_i |s_i|`)은 **폐기**. 분자가 signed 라 백본 내부의 양·음
> polarization 이 다시 상쇄됐다 — 절대값 분모를 넣은 목적과 정면으로 모순이었다 (회신 S Q1).

### 2-2. 홀 위치 — **같은 핵**을 가진 쌍으로만

$$\Delta\rho_{\text{hole}}(\mathbf r) \;=\; \rho_{D^-}(\mathbf r) - \rho_{D^\bullet}(\mathbf r)
\qquad \text{같은 기하에서}$$

- `D⁻` = H 제거 조성, `charge −1, mult 1`
- `D•` = 같은 H 제거 조성, `charge 0, mult 2`
- 적분값이 **정확히 한 전자** — vertical hole redistribution 으로 읽을 수 있다
- orbital relaxation 때문에 음의 lobe 가 생기므로 **positive detachment 성분과 signed
  relaxation 성분을 분리**하거나 natural difference orbital 을 병기한다
- Hirshfeld `Δq` 는 이 실공간 차이밀도의 **fragment 요약**으로만 쓴다

> ⛔ **중성 산(acid) ↔ H-제거 라디칼의 `Δq` 는 홀 밀도가 아니다.** 두 계는 H 하나가 달라
> **핵 조성이 다르다** — H 핵·전자 제거, O–H 결합 소실, 탈양성자 효과, backbone
> oxidation·spin polarization 이 전부 섞인다. 그 값의 정본 명칭은
> **`H-abstraction-induced charge redistribution`** 이고 홀 위치가 아니다 (회신 S Q9-a).

### 2-3. 비편재 — ring profile 기반

$$N_{\text{eff}} = \frac{1}{\sum_j p_j^2}\qquad (p_j = \text{링 } j \text{ 의 spin share})$$
+ **80% spin 을 포함하는 최소 연속 ring span** 을 병기.

> ⛔ v1 의 `L_deloc`("최대링의 10% 이상인 연속 링 수")은 **폐기 또는 secondary 강등**.
> 작은 수치 잡음도 최소 한 링을 반환한다 (회신 S Q1).

### 2-4. 구조 이완 — **Marcus λ 가 아니다**

$$E_{\text{relax}} = E_{D^\bullet}(R_{\text{start}}) - E_{D^\bullet}(R_\bullet)$$

이것은 **radical 표면 한쪽의 relaxation energy** 이지 Marcus 재조직에너지 전체가 아니다.
A→B 로 state 가 바뀌면 구조이완과 전자 basin 전환이 섞이므로 **branch identity 를
hard-gate** 한다.

same-nuclei inner-sphere reorganization 을 원하면 **네 점**이 필요하다:
$$\lambda_{\text{in}} = [E_\bullet(R_-)-E_\bullet(R_\bullet)] + [E_-(R_\bullet)-E_-(R_-)]$$

### 2-5. BLA — 직교 보강지표

같은 조성의 `D⁻` 와 `D•` **기하를 비교**한다. acid parent 와 H-제거 라디칼의 비교는
H 제거 자체의 구조효과가 섞인다고 **표시**한다.
⚠ population 분할에는 독립이지만 **범함수·torsion·환경에는 여전히 민감**하다 —
Q1 의 partition 위험은 줄이되 Q7 의 functional 위험은 우회하지 못한다.

## 3. 상태 열거 — seed 집합을 **사전 봉인**한다

한 conformer 의 최소 seed 집합 = **8개**:

| seed | 무엇 | 개수 |
|---|---|---|
| A | 제거된 SO₃ 에 radical | 1 |
| B | **각 EDOT ring** 에 backbone polaron | **6** |
| default | fresh-start 기본 추정 | 1 |

> ⚠ 비틀린 유한 n=6 사슬에는 **엄밀한 좌우 대칭이 없다.** 실제 automorphism 을 증명하지
> 못하면 B seed 는 3개가 아니라 **6개**다 (회신 S Q2).

**준비 방법**: `MORead + Rotate` · charged-fragment orbital transplant · constrained-DFT 로
localized density 를 만든 뒤 제약 해제.

**규율 6 (회신 S Q2 원문)**
1. 제약은 **seed 생성에만** 사용
2. 최종 에너지와 최적화는 **완전 비제약**
3. 각 seed 는 `NoAutoStart` 로 분리
4. 최적화 후 **별도 stability SP**
5. unstable 이면 생성된 orbital 로 재최적화 후 **다시 검사**
6. energy·geometry·ring-spin profile 로 basin dedup

**표현**: *"사전등록 seed 집합에서 찾은 최저해"* — "전역 최소" 가 아니다.

> ⛔ `StabPerform` 은 상태 열거 규칙이 **아니다.** 이미 수렴한 determinant 가
> orbital-rotation 공간에서 국소 최소인지 검사할 뿐, 다른 SCF minimum 을 전수 탐색하지
> 않는다. black-box 로 쓰지 말고 orbital 과 에너지 차를 직접 확인한다.
> stability 는 **single-point 형 계산**에서 수행한다.

> ⛔ **`W_state` 에 보편값은 없다** (v1 의 "리뷰에서 정한다" 는 잘못된 요청이었다).
> **전자에너지는 모두 보고한다.** 열적 공존을 말하려면 같은 온도의 ΔG 가 필요하다.
> (참고: 298 K · 동일 degeneracy · minor population 10% 기준이면 약 56 meV — 그러나
> 진동·용매 자유에너지 없이 이것을 "축퇴" 라고 부르지 않는다.)
> 범함수에 따라 순서가 바뀌면 `FUNCTIONAL_DEPENDENT` 이지 넓은 `W_state` 로 합치지 않는다.

### 3-1. 놓쳤던 상태 (회신 S Q5) — 열거에 포함한다

- 각 SO₃ 의 **서로 다른 O-localized** radical
- 제거된 위치가 **아닌** 다른 sulfonate 로의 radical/proton 이동
- 각 EDOT ring 의 polaron
- SO₃/backbone **혼합상태**
- linker C/O · EDOT S/O · **σ-radical**
- 남은 산성 H 의 **proton-transfer microstate**
- 서로 다른 torsion · hydrogen-bond minimum
- 선택한 doublet manifold 밖의 **quartet sentinel**

⚠ **전자 SCF basin 과 proton-transfer/conformer minimum 은 별도 축이다.**
최적화 중 proton 이 이동하면 같은 basin 의 단순 이완으로 처리하지 말고 **새 microstate 로
재분류**한다.

> ⛔ v1 의 "k=1 bipolaron 유사해" 는 **삭제**. 961전자 doublet 의 한 홀은 true bipolaron 이
> 아니다. 가능한 명칭: single polaron · two-center charge-resonance · multiradical doublet.

## 4. 환경 — ε 규약을 사전 봉인한다

**기체상 양은 정의된다. 다만 고체 SDCP 의 양이 아니다.**
허용 문구 상한: *"H-제거 n=6 단일사슬의 ε=1 모델에서 찾은 상태"*.

> ⛔ v1 의 *"ε=1 에서는 전하분리의 쿨롱 대가가 무조건 커진다"* 는 **단순화가 지나쳤다.**
> 진공은 `SO₃⁻–backbone⁺` 사이 **인력을 강화**하고, 연속체는 그 인력을 screening 하면서
> 개별 이온성 분포를 안정화한다. A/B 의 순효과와 단조성은 **미리 정할 수 없다** (회신 S Q3).

**ε 규약 (branch-following — 매번 최저해를 다시 고르지 않는다)**

| ε | 역할 |
|---|---|
| 1 | vacuum control |
| 실측/문헌 dry-polymer 범위 | **primary sensitivity** ⏳ 값 미정 — litdb 근거 필요 |
| 20 | stress test |

추적할 곡선: `ΔE_{B−A}(ε)` · `F_bb^A(ε)` · `F_bb^B(ε)`.
plausible 범위에서 **순서가 교차하면 `ENVIRONMENT_DEPENDENT`**.

⚠ CPCM 은 **material prediction 이 아니라 model-response curve** 다. cavity 표면의 연속체
반응장이라 특정 수소결합·proton 위치·interchain packing 을 담지 않는다.
⚠ tethered `SO₃⁻` 가 **이미 내부 counterion** 이다 — 임의의 외부 양이온을 더하면 다른
화학계가 된다. 필요한 것은 실제 시료의 proton/electron reservoir 와 국소 수화·이온 환경이다.
⚠ 고체의 우세상태나 전도기전을 주장하려면 단일사슬+CPCM 으로는 **부족하다**.

## 5. 반증가능성 — positive control 이 필수다 (회신 S Q4)

**최소 adequacy control**: 같은 n=6 의 **fully protonated cation**
- `charge +1, mult 2` · 같은 범함수·환경 · backbone ring 별 localized seed
- 이것은 **에너지 기준이 아니라** *"이 방법이 알려진 형태의 backbone radical cation 을
  표현할 수 있는가"* 를 보는 것이다.

**사전 고정 판정 (결과 보기 전)**

| 판정 | 조건 |
|---|---|
| `BACKBONE_SUPPORTED` | B 가 **비제약 안정해**로 남고 물리 환경 범위에서 최저 또는 에너지 근접 |
| `SO3_CENTERED_WITHIN_MODEL` | positive control 통과 **하지만** H-제거계에서 A 가 환경·범함수·conformer 에 걸쳐 일관되게 낮음 |
| `ENVIRONMENT_DEPENDENT` | plausible ε 범위에서 A/B 순서 교차 |
| `FUNCTIONAL_DEPENDENT` | 범함수가 순서 또는 class 를 달리함 |
| `MODEL_NONDIAGNOSTIC` | positive control 실패 · 의도한 basin 회수 실패 · 상태 정체성 붕괴 |
| `PARTITION_DEPENDENT` | 분할법 사이 class 가 다르거나 `|ΔF_bb| > 0.10` |
| `THRESHOLD_DEPENDENT` | 0.4/0.5/0.6 경계에서 class 가 바뀜 |
| `TUNING_DEPENDENT` | OT-RSH tuning minimum 이 평평하거나 n·conformer 에 민감 |

**A 가 나와도 허용되는 최강 문구**:
> *"검사한 n=6 H-제거 분자모형에서는 탐색된 최저상태가 SO₃ 중심이었다."*

**class 부여 규칙**: 유일한 집합이 `F ≥ 0.5` 이고 **다음 집합과 차이가 ≥ 0.10** 일 때만.
`F_other` 가 크면 `F_bb − F_SO3` 만으로 판정하지 않는다.

## 6. 범함수 (회신 S Q7)

`r²SCAN-3c` + `ωB97X-D3` 는 **첫 screening pair 로는 충분하지만 판정기는 아니다.**
두 범함수가 **독립적인 state search 뒤** 같은 basin·같은 정성 class 를 주면
*"두 함수에서 견고한 모델 결과"* 로 인용한다. 갈리면 **사후 선택 금지** →
`FUNCTIONAL_DEPENDENT` 로 닫는다.

**OT-RSH 는 불일치 시 대표 subset 에만 escalation**:
tuning objective 와 charge/multiplicity 사전등록 · 같은 environment 에서 **하나의 ω 를
A/B 모두에** · A 와 B 를 **따로 tune 한 뒤 에너지 비교 금지** · 실행 불가능하면
`FUNCTIONAL_DEPENDENT` 에서 멈춤.

⚠ 내부 `SO₃⁻` 성격 때문에 **hybrid basis 의 diffuse-function sensitivity** 를 대표
구조에서 확인한다.

## 7. 게이트 — 결과 보기 전에 (회신 S Q8)

- H 제거 **인덱스·원소** · 전자수 · charge · multiplicity **출력 echo**
- ORCA version · 범함수 · basis · grid · **CPCM cavity** · geometry hash
- `NoAutoStart` 와 의도한 `MORead` lineage **구분**
- **모든 사전등록 seed 의 실행 receipt** — 하나라도 빠지면 lowest-found 판정 금지
- 최종 geometry 에서 **별도 stability SP**
- 제약·level shift·frozen orbital **완전 해제 확인**
- A/B branch identity 가 vertical→relaxed 동안 **유지되는지**
- 최적화 중 proton 이동·결합절단 시 **새 state 로 재분류**
- spin-density **적분값**과 signed-spin 합 검증
- backbone/SO₃/other atom map 의 **완전성·상호배타성·hash**
- Hirshfeld/Löwdin class 불일치 · 범함수별 state-order 불일치
- GBW · spin-density cube · difference-density cube **보존**
- 동일 에너지식 비교는 **같은 조성·범함수·basis·환경 안에서만**
- **판정바닥의 단위를 분리 명시**: share 는 0.01 (무차원), 에너지는 eV

⚠ `⟨S²⟩ 0.75–0.80` 은 **k=1 doublet quality gate 로는** 쓸 수 있지만 보편적 물리 경계가
아니다. **raw 값을 보존**하고 multiplicity 별 창을 따로 둔다:
restricted singlet ≈ 0 · **BS singlet 은 일반적으로 0이 아니며 두 spin-½ 한계에서 ≈ 1** ·
triplet ≈ 2.

## 8. 도핑 레벨 (회신 S Q6)

k=1 부터 시작 — **찬성**. 단 `1/6 = 17%` 는 **유한 oligomer 조성이지 실측 도핑률이 아니다**.

> ⛔ v1 의 *"k=1 이 백본으로 갔을 때만 k=2"* 는 **결과 의존적이라 폐기**.
> k=2 는 **polaron–polaron 상호작용**이라는 별도 estimand 이며, k=1 파이프라인이
> diagnostic 하면 **결과 방향과 무관하게** 연다.

k=2 최소 상태: ① RKS closed-shell singlet(paired/bipolaron 후보) ② UKS BS singlet(반평행)
③ UKS triplet(평행). 각 multiplicity 에서 `SO₃–SO₃` · `SO₃–backbone` · `backbone–backbone`
seed. **k=1 의 ⟨S²⟩ 창을 재사용하지 않는다.**

위치: k=1 은 **여섯 위치 전부** 또는 실제 대칭 증명 / k=2 는 adjacent · 중간거리 ·
최대거리 site pair.

## 9. Pilot 규모 (회신 S Q9-e) — 생산이 아니라 **adequacy pilot**

한 conformer · 한 H-removal site · 환경 2개(ε=1 + 근거 있는 low-ε 한 점) · 범함수 하나당:

| | 내용 | SP |
|---|---|---|
| `D•` vertical | A 1 + B(ring별) 6 + default 1 = 8 × 2환경 | **16** |
| same-nuclei `D⁻` reference | 1 × 2환경 | **2** |
| fully protonated `P⁺` positive control | ring별 B 6 + default 1 = 7 × 2환경 | **14** |
| | **범함수당 고정기하 SP** | **32** |

1. `r²SCAN-3c` 32건 먼저
2. adequacy gate 통과 시 `ωB97X-D3` 가 **독립 seed 로** 같은 32건 반복
3. 총 fixed-geometry pilot **상한 64건**
4. 발견된 **서로 다른 stable basin 마다** Opt 1건
5. 각 Opt 뒤 **final stability SP** 1건

> ⛔ Opt 수는 결과에 따라 달라지므로 **미리 `1` 로 고정하지 않는다.**

이 pilot 은 **상태탐색과 관측량의 유효성만** 판정한다. conformer·위치 결론으로 확장하려면
중성 8개가 끝난 뒤 **사전 규칙으로** 최소 두 개의 저에너지·torsion-diverse conformer 를
고르고, 엄밀한 대칭이 없으면 **여섯 H 위치**를 검사한다.

## 10. ⛔ 금지 서술

v1 의 여섯 건 유지:
- "SDCP 는 전자를 전도한다/안 한다" · "σ_SDCP 250 을 뒷받침한다" · "전역 최소" ·
  단량체 65/35 와 n=6 을 한 수치열에 · Figure 4 `σ_ele,eff` 와 한 표에 ·
  펠릿 σ_e 와 한 표에
- `λ` 로 hopping 속도·이동도·σ 를 계산해 인용

회신 S 추가 여덟 건:
- ⛔ "H 원자 제거가 **자가도핑 과정 자체를 재현**했다"
- ⛔ "spin density 가 곧 hole charge density 다"
- ⛔ "기체/CPCM 최저해가 **고체의 우세상태**다"
- ⛔ "k=1 과 k=2 가 실제 시료의 17%·33% 도핑률이다"
- ⛔ "B basin 을 못 찾았으므로 **고체에는** backbone polaron 이 없다"
- ⛔ "BLA 가 일치하므로 **범함수 의존성이 해결**됐다"
- ⛔ 출처가 봉인되지 않은 250 S cm⁻¹ 를 **계산의 실험 검증**으로 사용
- ⛔ 단량체 65/35 를 n=6 또는 전도도와 **반대되는 증거**로 표현

**Figure 4 층위 구분**: `excluded from conduction` 은 SDCP 를 절연체로 본다는 뜻이 아니라
**병렬 배선으로 모델하지 않았다**는 뜻이다. 이 계산은 Figure 4 를 지지·반박하지 않는다.
(회신 S 가 이 구분에 동의)

## 11. 규약 대조

- `kb/methodology/electron_localization_framework_2026_07_08.md` — **대조함: 무관하다.**
  LPSCl/B₂O₃ 고체전해질의 밴드갭·σ\*·ELF 이지 고분자 폴라론이 아니다 ⇒ **선행 판정 없음**
- `kb/reviews/codex_R4_doped_reopen_impl2_reply_2026_08_29.md` — localization 0.5/0.3 은
  라우팅 기준으로만 조건부 수용. ring 별 집합 · BS 양음 lobe 분리 · 두 분해 병기 요구
- `kb/projects/sdcp_master_v2_2026_07_11.md` §1.3 — 단량체 65/35, ⟨S²⟩ 0.7552, O–H BDE 4.24 eV

## 왜 중요한가

SDCP 를 "자가도핑 전도성 고분자" 라고 부르는 근거는 지금 **분광(라만 1062 = νs(SO₃⁻))** 과
**물질 계열(S-PEDOT)** 이다. 캐리어가 백본에 있다는 직접 증거는 없다.
이 pilot 은 그 물음에 **직접 답하지 않고**, 답할 수 있는 방법이 있는지를 먼저 본다.

## Evidence For

- S-PEDOT 계는 문헌상 자가도핑 전도체 (⚠ **litdb 대조 안 함** — 근거 보강 필요)
- 라만 1062 = νs(SO₃⁻) 실측 일치 ⇒ 술포네이트가 **이온화**돼 있다
- Table S2 σ_SDCP = 250 S cm⁻¹ (⚠ 시편 출처 미결 — 인용 금지)

## Evidence Against

- 단량체 r2SCAN-3c 실측: SO₃ 3-O 65% / 백본 π 35%
  (⚠ 링이 하나라 다중링 폴라론을 **구조적으로 담지 못하는 계**였다)

## 결정 실험

§9 의 32건 `r²SCAN-3c` adequacy pilot. **§5 의 종료 규칙 다섯 개 중 하나로 닫는다.**

## Status Log

- 2026-08-31: v1 생성 → 회신 S 접수(전체 생산 NO-GO / 32건 pilot 조건부 GO) → v2 로 재작성.
  착수 전 P0 5건은 `db/properties/sdcp_polaron_pilot_prereg_2026_08_31.json` 에 봉인.
