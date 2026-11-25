# Band gap — 밴드 갭 (전자 밴드 간극)

> 점유된 밴드 꼭대기(VBM)와 비어 있는 밴드 바닥(CBM) 사이의 에너지 간극. 고체전해질(SE)에서는 이 값이 클수록 전자를 통과 못 시키는 "전자 절연체"라는 뜻이라 핵심 스크리닝 지표가 된다.

## 목차
1. VBM / CBM 정의
2. Direct vs Indirect gap
3. Fixed-occupation nscf로 gap 읽는 법
4. 왜 DOS-threshold 판독은 틀리나
5. PBE의 gap 과소평가
6. SE에서 gap의 물리적 의미
7. 같은 O 를 넣었는데 왜 b2o3 만 gap 이 내려가나 (우리 실측)

---
## 1. VBM / CBM 정의
Kohn–Sham 계산은 각 k-point $\mathbf{k}$와 밴드 $n$마다 고유값 $\varepsilon_{n\mathbf{k}}$와 점유수 $f_{n\mathbf{k}}$를 준다. 절연체·반도체는 0 K에서 점유가 딱 나뉜다.

- **VBM (Valence Band Maximum)**: 점유된($f=1$) 상태 중 **가장 높은** 고유값
- **CBM (Conduction Band Minimum)**: 비점유($f=0$) 상태 중 **가장 낮은** 고유값

$$\varepsilon_{\text{VBM}} = \max_{n,\mathbf{k}}\{\varepsilon_{n\mathbf{k}} : f_{n\mathbf{k}} = 1\}, \qquad \varepsilon_{\text{CBM}} = \min_{n,\mathbf{k}}\{\varepsilon_{n\mathbf{k}} : f_{n\mathbf{k}} = 0\}$$

밴드 갭은 이 둘의 차이다:

$$\boxed{E_g = \varepsilon_{\text{CBM}} - \varepsilon_{\text{VBM}}}$$

> [!note] 왜 "고유값 차이"가 정답인가
> Gap은 정의상 "전자 하나를 VBM에서 CBM으로 올리는 데 드는 최소 에너지"다. 이건 **밴드 가장자리 두 고유값의 차이**로 직접 읽어야 하며, 상태밀도(DOS)가 "0에서 벗어나는 지점"으로 근사하면 안 된다 (4절 참조).

---
## 2. Direct vs Indirect gap
VBM과 CBM이 **같은 k**에 있으면 direct, **다른 k**에 있으면 indirect gap이다.

$$E_g^{\text{direct}} = \min_{\mathbf{k}}\left[\varepsilon_{\text{CBM}}(\mathbf{k}) - \varepsilon_{\text{VBM}}(\mathbf{k})\right], \qquad E_g^{\text{indirect}} = \varepsilon_{\text{CBM}}(\mathbf{k}_2) - \varepsilon_{\text{VBM}}(\mathbf{k}_1)$$

우리가 스크리닝에서 쓰는 값은 **fundamental (indirect 허용) gap** — 전자 절연성을 판정하는 데는 이게 맞다. optical gap(direct)은 흡수 스펙트럼용이라 별개.

| 종류 | VBM·CBM 위치 | 물리적 의미 |
|------|-------------|------------|
| Direct | 같은 $\mathbf{k}$ | 광 흡수/방출 (optical) |
| Indirect | 다른 $\mathbf{k}$ | 최소 전자 여기 에너지 (fundamental) |

---
## 3. Fixed-occupation nscf로 gap 읽는 법
절연체 gap은 **fixed occupations**(`occupations='fixed'`) nscf에서만 신뢰한다. 절차는 이렇게 한 단계씩 간다.

```
① scf: 수렴된 전자밀도 n(r) 확보 (smearing 써도 됨)
② nscf: 조밀한 k-grid + occupations='fixed'로 고정밀 고유값
③ VBM = 점유 밴드 최댓값, CBM = 비점유 밴드 최솟값
④ E_g = CBM − VBM
```

왜 nscf를 따로 도나? scf 단계는 metal도 커버하려 smearing을 쓰는데, smearing은 Fermi 근처 점유를 뭉개서 gap 가장자리를 흐린다. 그래서 밀도를 고정한 뒤 **fixed occupation**으로 고유값만 다시 뽑아 가장자리를 또렷하게 읽는다.

> [!tip] 실무 체크
> nscf k-grid를 scf보다 촘촘히 (예: 밴드 구조/조밀 MP mesh) 잡아야 진짜 VBM·CBM $\mathbf{k}$를 놓치지 않는다. 점유 밴드 개수 = 전자수/2 (spin-unpolarized)로 확인.

### QE 출력에서 실제로 읽기
Fixed-occupation nscf가 끝나면 QE는 출력에 이 한 줄을 찍는다.
```
highest occupied, lowest unoccupied level (ev):    X.XXXX   Y.YYYY
```
- 왼쪽 = VBM, 오른쪽 = CBM → $E_g = Y - X$. 이 값이 우리가 인용하는 gap.
- 이 줄이 안 나오면 (metal로 인식됨) `occupations`·`nbnd` 설정을 재확인.
- `nbnd`는 $N_{\text{elec}}/2$(spin-unpolarized 점유 밴드 수)보다 넉넉히 줘 CBM 위 비점유 밴드가 실제로 계산되게 한다.

---
## 4. 왜 DOS-threshold 판독은 틀리나
DOS-threshold란 상태밀도 $g(E)$가 "0에서 처음 올라오는 에너지"를 gap 가장자리로 삼는 방식이다. 이건 **금지**한다.

$$g(E) = \sum_{n,\mathbf{k}} \delta(E - \varepsilon_{n\mathbf{k}}) \;\xrightarrow{\text{smearing}}\; \tilde{g}(E) = \sum_{n,\mathbf{k}} \frac{1}{\sqrt{2\pi}\sigma}\exp\!\left[-\frac{(E-\varepsilon_{n\mathbf{k}})^2}{2\sigma^2}\right]$$

문제는 두 가지다.
- **Gaussian smearing $\sigma$의 꼬리**: 밴드 가장자리 상태가 gap 안쪽으로 번져 임계값을 안쪽으로 밀어넣는다.
- **유한 k-sampling**: 진짜 band edge $\mathbf{k}$가 mesh에 안 걸리면 DOS가 실제보다 늦게 올라온다.

두 효과가 합쳐져 gap을 **약 0.3 eV 과소평가**한다. 우리 폐기 사례가 바로 이거다.

> [!warning] DOS-threshold 폐기값 (틀린 예시)
> comp1을 DOS-threshold로 읽으면 **1.76 / 1.82 eV**가 나온다. 이건 **틀린 값**이라 어디에도 인용 금지. 같은 구조의 fixed-occupation nscf VBM/CBM 고유값은 **2.066 eV** — 0.3 eV가량 차이가 정확히 이 아티팩트다.

---
## 5. PBE의 gap 과소평가
여기엔 두 종류의 과소평가가 겹쳐 있으니 헷갈리지 말자.

1. **방법론적 과소평가 (물리)**: PBE 같은 (semi-)local 범함수는 **derivative discontinuity**가 빠져 있어 진짜 gap을 구조적으로 낮게 준다. 실험/HSE 대비 전형적으로 30~50% 낮음. 이건 이론의 한계지 버그가 아니다.
2. **판독 과소평가 (아티팩트)**: 4절의 DOS-threshold ~0.3 eV. 이건 **없앨 수 있는** 실수다.

$$E_g^{\text{true}} = E_g^{\text{KS}} + \Delta_{xc}$$

여기서 $\Delta_{xc}$가 derivative discontinuity 기여. 우리 캠페인은 조성 간 **상대 비교**가 목적이라 PBE-level gap을 일관되게 쓰되, (2)번 판독 아티팩트만은 fixed-occupation으로 반드시 제거한다.

> [!important] 절대값 vs 상대 비교
> PBE gap의 절대값을 "실험 gap"으로 주장하면 안 된다. 하지만 **같은 레시피**로 뽑은 조성 간 차이(예: +O가 gap을 올린다)는 방법 오차가 상쇄돼 신뢰할 수 있다.

---
## 6. SE에서 gap의 물리적 의미
고체전해질은 **이온은 통과, 전자는 차단**해야 한다. 전자가 새면 self-discharge와 Li dendrite 성장을 촉발한다. 그래서 gap은 곧 **전자 절연 여유**다.

$$\sigma_{\text{electronic}} \propto \exp\!\left(-\frac{E_g}{2k_BT}\right)$$

gap이 클수록 **bulk intrinsic** 전자 전도도가 지수적으로 떨어진다 → 좋은 SE. 우리 데이터에서 **+O 도핑이 gap을 올린다(modelc 2.099 → LPSOCl 2.2309 eV, +0.132)** — 전자 절연 강화 방향이라 반가운 신호다.

> ⚠️ **두 가지 한정 (2026-07-27 추가)**
>
> **① baseline은 같은 호스트끼리.** LPSOCl은 modelc(Li₅.₄PS₄.₄Cl₁.₆)의 S→O 치환체다(Li₂₇P₅S₂₁OCl₈).
> comp1 2.066을 before로 쓰면 **Cl 증량(1.0→1.6) 효과와 O 치환 효과가 한 델타에 섞인다.**
> canonical 델타는 electronic.json `doping_family_2026_07_16` 기준 **modelc 대비 +0.132**
> (같은 표에서 +B₂O₃는 modelc 대비 −0.132로 반대 방향).
>
> **② 이 공식은 bulk intrinsic 캐리어에만 맞다.** 실측 σ_e 는 계면/미세구조가 지배한다 —
> 우리 캠페인의 대표 반례가 Nd 도핑이다: **bulk gap이 0.55 eV 좁아지는데(2.184→1.632, Nd 5d)
> 실측 σ_e 는 오히려 떨어졌다.** electronic.json 이 이를 두고 *"a naive 'wider gap lowers
> e-conduction' reading is WRONG here"* 라고 못박는다(그 필드가 논문의 중심 메커니즘 결과).
> 즉 gap 은 **bulk 절연성의 필요조건 지표**일 뿐 실측 전자전도도의 예측자가 아니다.
> 전기화학 안정성(분해 onset)은 더더욱 아니다 — VBM ≠ onset(반응 자유에너지가 결정),
> band-edge는 분해창을 2–3× 과대평가한다(Schwietert 2020; 우리 직접 증거 = comp1/modelc VBM이
> 0.32 eV 다른데 onset은 동일). → `kb/concepts/esw` 계열 문서 참조.

```mermaid
graph TD
    A[SCF: converged density n r] -->|fix density| B[NSCF occupations fixed]
    B --> C[Dense k-grid eigenvalues]
    C --> D[VBM = highest occupied]
    C --> E[CBM = lowest unoccupied]
    D --> F[Eg = CBM - VBM]
    E --> F
    F --> G[Electronic insulation check]
    X[DOS threshold readout] -.forbidden ~0.3 eV low.-> F
    style A fill:#e0ebff,stroke:#2563eb
    style F fill:#fef9c3,stroke:#2563eb
    style G fill:#e2f6ec,stroke:#059669
    style X fill:#fde2e2,stroke:#dc2626
```
**한 문장 요약**: scf로 밀도를 얻고 fixed-occupation nscf로 VBM·CBM 고유값을 또렷하게 읽어 그 차이를 gap으로 삼는다 — DOS-threshold 판독은 ~0.3 eV 과소라 금지.

---
## 우리 캠페인 적용
모든 gap은 **fixed-occupation nscf VBM/CBM 고유값**이다. DOS-threshold 판독값은 폐기.

| 조성 | 약칭 | Canonical gap (eV) | 비고 |
|------|------|--------------------|------|
| Li₆PS₅Cl | comp1 | **2.066** | 기준 argyrodite |
| LPSClBr | comp2 | **2.04**† | Br 치환 (†잠정 — legacy band_gaps; fixed-occ nscf 재확인 중) |
| Li₅.₄PS₄.₄Cl₁.₆ | modelc | **2.099** | Cl-rich (LPSCl1.6) |
| LPSOCl (+O) | lpsocl | **2.2309** | O 도핑, gap 최대 |
| B₂O₃-doped LPSCl1.6 | b2o3 | **1.9671** | **O 를 넣었는데 gap 최소** — §7 참조 |
| ~~comp1 DOS-threshold~~ | — | ~~1.76 / 1.82~~ | **틀린 값, 인용 금지** |

- 순서: **+O(2.2309) > modelc(2.099) > comp1(2.066) > comp2(2.04)**. +O가 전자 절연을 강화, Br은 소폭 낮춘다.
- comp1·modelc·+O·+B₂O₃는 (db/properties/electronic.json) fixed-occ eigenvalue canonical과 일치. **comp2 2.04는 잠정**(legacy band_gaps 유래, fixed-occ nscf 재확인 중 — eigenvalue canonical 아님). 절대값은 PBE-level임을 명시하되, 같은 레시피 조성 비교는 신뢰.
- DOS-threshold(1.76/1.82)는 **~0.3 eV 과소 아티팩트**라 문서/그림 어디에도 쓰지 않는다.

---
## 7. 같은 O 를 넣었는데 왜 b2o3 만 gap 이 **내려가나** (2026-09-07)

1저자 질문: *"O 가 치환됐는데 상식적으로 b2o3 가 lpscl1.6·lpsocl 에 비해 떨어지는 이유"*.
**O 때문이 아니라 B 때문이다.**

### 7.1 두 도핑이 반대로 간다

| | gap (eV) | modelc 대비 |
|---|---|---|
| modelc (LPSCl1.6, 기준) | 2.099 | — |
| **lpsocl** (O 도핑) | **2.2309** | **+0.132** ✅ 상식대로 |
| **b2o3** (B₂O₃ 도핑) | **1.9671** | **−0.132** ❓ |

둘 다 O 를 넣었다. 다른 것은 **B** 하나뿐이다.

> [!note] ±0.132 가 정확히 같은 것은 **우연**이다
> 네 자리까지 대칭이라 눈에 띄지만 물리 법칙이 아니다.
> *"대칭적으로 상쇄된다"* 같은 표현을 쓰지 않는다.

### 7.2 무엇이 움직였나 — CBM 이다

`electronic.json` 의 VBM/CBM (modelc 대비):

```
lpsocl   ΔVBM −0.058 · ΔCBM +0.074   → 양쪽이 벌어진다
b2o3     ΔVBM +0.027 · ΔCBM −0.105   → CBM 이 끌려 내려온다
```

> [!warning] 이 분해는 **엄밀하지 않다**
> 주기계 계산에서 고유값의 절대 위치는 **임의 오프셋**(G=0 항)을 갖는다. 셀이 다르면
> 깊은 코어 준위나 정전위 정렬 없이 VBM·CBM 을 직접 비교할 수 없다.
> **정황이지 증명이 아니다.** 아래 §7.3(PDOS 성분)은 **한 계산 안**의 양이라 안전하다.
> 원고에는 §7.3 으로 쓴다.

### 7.3 b2o3 의 CBM 은 **B 다** (한 계산 안 — 안전)

CBM ~ CBM+1 eV 구간, **원자당** states/eV (원소별 총량은 원자수에 끌려가므로 정규화 필수):

| b2o3 (128원자) | 원자당 | 비중 | 원자수 |
|---|---|---|---|
| **B** | **16.07** | **46.3 %** | **2** |
| P | 12.80 | 36.8 % | 8 |
| S | 4.29 | 12.3 % | 41 |
| Li | 0.99 | 2.8 % | 58 |
| O | 0.32 | 0.9 % | 3 |
| Cl | 0.29 | 0.8 % | 16 |

같은 구간의 **modelc** 는 P 45.00 (69.2 %)이 1위이고 B 는 없다.
⇒ **원자 2개짜리 B 가 CBM 성분 1위**다.

### 7.4 왜 B 인가 — BS₃ 의 **빈 p_z**

ICOHP 원장: `B–S : N = 6`, B 가 2개 ⇒ **B 하나당 S 3개 = 삼각평면 BS₃**.

```
   PS₄  사면체 sp³            BS₃  삼각평면 sp²
       S                          S
       |                           \
   S — P — S                    S — B          ← 평면에 수직인
      /                            /              p_z 가 비어 있다
     S                            S
  4결합 = 궤도를 다 쓴다       3결합 = p_z 하나가 남는다
```

sp² 붕소는 평면에 수직인 **p_z 가 비어 있다.** BF₃·BH₃ 가 Lewis 산인 것과 같은 구조다 —
전자를 받을 자리가 준비돼 있고 에너지가 낮다. 그 빈 p_z 가 호스트 전도띠 **아래**에
들어앉아 새 CBM 이 된다.

> [!note] "결합이 센데 왜 CBM 을 내주나" 는 모순이 아니다
> B–S 는 **ELF 중점 0.959 로 챔피언에서 가장 공유결합적**이다(P–S 0.945 · P–O 0.930).
> 그런데 빈 p_z 는 **σ 결합 3개와 직교하는 비결합 궤도**다 — σ 가 아무리 세도 p_z 의
> 에너지는 거기 영향을 받지 않는다. 기하가 만든 궤도이지 결합 세기의 결과가 아니다.
> ⚠ **ELF 와 ICOHP 는 다른 양이다.** ELF 중점 = 얼마나 공유결합적인가,
> ICOHP = 얼마나 센 결합인가. ICOHP 순위는 P–O −8.551 > B–S −7.792 > P–S −6.023 으로
> **다르다.** `B–S(최강)` 이라는 기존 표기는 **ELF 순위**를 말한 것이다.

### 7.5 그럼 O 는 왜 gap 을 못 넓혔나

b2o3 의 O 는 3개뿐이고 **P 자리로 가서 P–O 인산염을 만들었다**(ICOHP −8.551, 전체 최강).
즉 O 가 자유롭게 S 를 대체해 VBM 을 눌러 내리는 것이 아니라 **P 에 묶여 있다.**
그래서 O 의 gap 확장 효과가 거의 나오지 않고(ΔVBM +0.027, 오히려 살짝 위) B 효과가 그대로 드러난다.

**lpsocl 은 반대다** — 거기서는 O 가 **S 자리**로 들어간다. O 2p 가 S 3p 보다 깊으므로
VBM 이 내려가고(−0.058) gap 이 넓어진다. §5 의 일반론대로다.

> **한 줄**: 같은 O 라도 **어디 앉느냐**가 다르고, b2o3 에는 **B 라는 더 센 반대 효과**가 하나 더 있다.

### 7.6 ⏳ 아직 추론인 것

실측한 것은 **원소별** PDOS 다 — *"b2o3 의 CBM 은 B 가 지배한다"*(원자당 46 %).
그것이 **p_z 냐**는 BS₃ 삼각평면 기하에서 나온 **화학적 추론**이다.

**2026-09-07 확인 결과 — 지금 repo 에는 없다.**
`tools/electronic/standard_dos/projwfc.in` 주석이 *"sum per-orbital PDOS afterwards"* 라고
적혀 있다. 즉 **궤도별 파일이 만들어졌는데 원소별로 합치면서 detail 을 버렸다.**
`db/properties/` 의 b2o3 PDOS 는 전부 원소별·자리별뿐이다.

원자료는 오프라인 백업(외장 SSD) `kisti_backup_2026-07-14/kgy_b2o3_eos_2026-07-14/b2o3_eos/`
에 있을 수 있는데, `kb/methodology/offline_archive_index_2026_08_20.md` 의 그 폴더 목록에는
cube 6종·Bader 55개만 적혀 있고 **`*.pdos_atm*` 은 목록에 없다** — 보존 여부 미확인.

회수 사다리 (비용 순):
1. SSD 에서 `ls *pdos_atm*` — 있으면 **재계산 0**, B 원자의 `wfc#N(l)` 만 l 별로 합치면 끝
2. 없으면 `tmp/`(저장된 파동함수) 확인 — 있으면 `projwfc.x` 만 재실행 (nscf 불필요, 분 단위)
3. 둘 다 없으면 nscf + projwfc 재계산 (그때 비용 발생)

> [!warning] 그때까지 쓰는 법
> 허용: *"b2o3 의 CBM 은 원자당 성분에서 B 가 지배한다(46 %)"*
> 조건부: *"삼각평면 BS₃ 기하에서 **예상되는** 빈 p_z"*
> ⛔ 금지: *"b2o3 의 CBM 은 B 의 p_z 다"* — l-분해 전까지 단정하지 않는다.

기계 판독용 기록: `db/properties/b2o3_cbm_character_2026_09_07.json`

*출처: `db/properties/electronic.json` (eigenvalue_gaps_v100_2026_06_16) ·
`b2o3_pdos_element_smooth.csv` · `modelc_pdos_element_smooth.csv` · `b2o3_icohp.json` ·
`kb/results/b2o3_elf_covalency_2026_07_02.md`*

*tags: band gap · VBM · CBM · fixed occupation · nscf · DOS threshold · PBE underestimate · electronic insulation · argyrodite · boron · BS3 · empty p_z · Lewis acid · ELF vs ICOHP*
