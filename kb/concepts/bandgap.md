# Band gap — 밴드 갭 (전자 밴드 간극)

> 점유된 밴드 꼭대기(VBM)와 비어 있는 밴드 바닥(CBM) 사이의 에너지 간극. 고체전해질(SE)에서는 이 값이 클수록 전자를 통과 못 시키는 "전자 절연체"라는 뜻이라 핵심 스크리닝 지표가 된다.

## 목차
1. VBM / CBM 정의
2. Direct vs Indirect gap
3. Fixed-occupation nscf로 gap 읽는 법
4. 왜 DOS-threshold 판독은 틀리나
5. PBE의 gap 과소평가
6. SE에서 gap의 물리적 의미

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

gap이 클수록 전자 전도도가 지수적으로 떨어진다 → 좋은 SE. 우리 데이터에서 **+O 도핑이 gap을 올리는(2.066 → 2.2309 eV)** 게 전자 절연 강화 방향이라 반가운 신호다.

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
| ~~comp1 DOS-threshold~~ | — | ~~1.76 / 1.82~~ | **틀린 값, 인용 금지** |

- 순서: **+O(2.2309) > modelc(2.099) > comp1(2.066) > comp2(2.04)**. +O가 전자 절연을 강화, Br은 소폭 낮춘다.
- comp1·modelc·+O·+B₂O₃는 (db/properties/electronic.json) fixed-occ eigenvalue canonical과 일치. **comp2 2.04는 잠정**(legacy band_gaps 유래, fixed-occ nscf 재확인 중 — eigenvalue canonical 아님). 절대값은 PBE-level임을 명시하되, 같은 레시피 조성 비교는 신뢰.
- DOS-threshold(1.76/1.82)는 **~0.3 eV 과소 아티팩트**라 문서/그림 어디에도 쓰지 않는다.

*tags: band gap · VBM · CBM · fixed occupation · nscf · DOS threshold · PBE underestimate · electronic insulation · argyrodite*
