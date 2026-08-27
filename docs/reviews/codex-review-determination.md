# Codex 리뷰 과제 — "쟀다" 를 무엇으로 판정하는가

[codex-session-bootstrap.md](codex-session-bootstrap.md) 로 세션을 연 뒤 아래
"붙여넣는 프롬프트" 를 그대로 붙여넣는다.

주제는 **하나**다: 피팅이 낸 숫자 옆에 `결정됨` 을 적을지 말지를 정하는 규칙.
지난 리뷰([codex-review-soc-scan.md](codex-review-soc-scan.md))의 확정 지적
**#1 · #2 · #8** 이 여기 걸려 있고, 그중 **#2 를 고쳤다.** #1 은 아직
안 고쳤고 이 리뷰에서 방향을 받고 싶다.

## 범위

```bash
git log --oneline 0de4875e..a81aadd4
git diff 0de4875e..a81aadd4 -- packages/wrdkit/src/wrdkit/eis
```

| 파일 | 무엇 |
|---|---|
| `packages/wrdkit/src/wrdkit/eis/circuit.py` | `Element.exchangeable` · `Circuit.exchangeable_pairs` |
| `packages/wrdkit/src/wrdkit/eis/fit.py` | `Parameter.alias_of` · `.status` · `.reason` · `.determined` |
| `packages/wrdkit/tests/test_eis_fit.py` | 새 테스트 4개 |

범위 밖: 그림 저장·화면 (그쪽은
[codex-review-figure-export.md](codex-review-figure-export.md) 로 따로 낸다).

---

## 고친 것 — 지난 #2, 회로가 아는 축퇴

### 지적

> 정확히 축퇴인 `TL1_Ri ↔ TL1_Re` 가 각각 측정된 값으로 나온다.

### 재현 (그대로 돌아간다)

```python
import numpy as np
from wrdkit.eis.circuit import parse_circuit
from wrdkit.eis.fit import fit_circuit
from wrdkit.eis.spectrum import Spectrum

freq = np.logspace(4, -1.5, 45)
circuit = parse_circuit("R0-TL1")
rng = np.random.default_rng(7)
noise = 1 + rng.normal(0, 0.005, size=freq.size)

for label, ri, re in (("참값 Ri=40, Re=12", 40.0, 12.0),
                      ("참값 Ri=12, Re=40", 12.0, 40.0)):
    truth = np.array([5.0, ri, re, 60.0, 1e-4, 0.8, 3.0, 0.5, 10.0])
    z = circuit.impedance(truth, freq) * noise
    sp = Spectrum(frequency_hz=freq, z_re=z.real, z_im=z.imag)
    res = fit_circuit(sp, "R0-TL1", restarts=8)
    v = {p.name: p.value for p in res.parameters}
    print(label, "→", round(v['TL1_Ri'], 4), round(v['TL1_Re'], 4),
          f"chi2={res.chi_squared:.4e}")
```

```
참값 Ri=40, Re=12  →  38.8781 11.2062  chi2=7.9466e-06
참값 Ri=12, Re=40  →  38.8781 11.2062  chi2=7.9466e-06
```

**참값이 정반대인 두 스펙트럼이 똑같은 답을 낸다.** χ² 도 유효숫자 다섯 자리
까지 같다. 둘 중 하나에서는 보고된 "이온 레일 저항" 이 **3.4 배 틀렸고**,
데이터에도 피팅에도 어느 쪽인지 말해 줄 것이 없다.

씨앗 흩기(#1 의 `spread`)로도 안 잡힌다 — 두 순서가 **비트까지 같은 곡선**이라
(`np.array_equal(Z(Ri,Re), Z(Re,Ri)) == True`) 흩어짐이 0 이다. 잡음 없는
합성에서는 오차 막대가 `1.6e-12` 로 나와, 화면에서 **가장 정밀해 보이는 두
숫자**가 가장 못 정한 두 숫자였다.

### 고친 방법

축퇴를 **회로가 선언한다**. 데이터가 아니라 식의 성질이기 때문이다:

```python
# circuit.py — 원소가 제 축퇴를 안다
"TL": _TL(..., exchangeable=(("_Ri", "_Re"),))
```

`parse_circuit` 이 이름을 완성해 `Circuit.exchangeable_pairs` 로 올리고,
`fit_circuit` 이 양쪽 `Parameter.alias_of` 에 상대 이름을 넣어 미결정으로
둔다. 전에는 `fit.py` 가 이름 끝(`_Ri`/`_Re`)을 보고 **다시 추측**했다.

### 안 바뀐 것 (일부러)

- **총저항·전도도는 그대로다.** `total_resistance` / `label_arcs` 는 plain
  `R` 만 본다 (`"_" not in name`). 레일을 미결정으로 돌려도 TL 회로의 총저항이
  안 사라지는 것이 그 덕분이다.
- **짝의 합은 여전히 잰 값이다.** 위 재현에서 `Ri+Re = 50.08` 은 두 경우 모두
  같고 참값 52 에 가깝다. 지금은 그 합을 **아무 데도 안 내보내고 있다** —
  질문 3.

---

## 고친 것 — 지난 #8, `미결정` 이 네 가지를 뭉갰다

`determined` 불리언 하나로 (a) 오차 막대가 값을 삼킴 (b) 씨앗 사이에서 값이
움직임 (c) 야코비안이 특이함/경계에 눌림 (d) 회로가 못 가름 을 전부 같은
줄표로 냈다. 화면을 보는 사람은 "이 셀이 이상하다" 와 "이 회로가 이 셀에
안 맞는다" 를 가를 수가 없었다.

```
status  : determined | not_checked | undetermined
reason  : "" | single_solution | relative_stderr | seed_spread
                | no_error_bar | structural_alias
```

`determined` 의 뜻은 안 바꿨다 (`status != "undetermined"`) — 기존 소비자
(총저항·전도도·API·화면)가 그대로 돈다.

**`not_checked` 를 새로 만든 것이 이 변경에서 가장 논쟁적인 부분이다.**
다듬은 해가 하나뿐이면 흩어짐 검사는 **돌지 않은** 것이다. "안 움직이더라"
가 아니라 "안 움직이는지 안 봤다" 다. 그런데 값은 그대로 낸다 — 답이 하나인
피팅의 모든 수를 감추면 화면이 통째로 빈다. 질문 1.

---

## 안 고친 것 — 지난 #1 (여기서 방향을 받고 싶다)

> `spread < 3` 은 2 배 가까이 움직이는 값을 통과시킨다. 스케일 파라미터와
> 유계 지수를 갈라야 하고, 프로파일 우도 구간으로 가야 한다.

동의한다. 아직 안 고친 이유는 셋이다.

1. `_SPREAD_LIMIT = 3` 은 `relative_error < 0.5` 와 **같은 뜻으로** 골랐다
   (비가 r 이면 값은 기하평균의 `[1/√r, √r]` 안, r=3 이 대략 −42 %/+73 %).
   문턱 하나만 조이면 두 규칙이 서로 다른 엄격함을 갖는다.
2. 유계 지수(`_n`, `_Wn` — 0.3~1.0, 0.1~0.8)에 **비**를 쓰는 것 자체가 틀렸다.
   `n` 이 0.4 에서 0.79 로 움직이면 비는 1.98 로 통과하는데, 그 둘은 물리적
   으로 다른 계면이다. 절대차라야 한다.
3. 프로파일 우도는 파라미터마다 재피팅이 필요하다. 지금 한 스펙트럼 맞춤이
   시작점 8~24 개 × 4000 nfev 인데, 스캔은 스윕이 스물이 넘는다.

## 새 질문 (답이 필요한 순서)

1. **`not_checked` 를 값과 함께 내는 것이 맞나.** 대안 둘: (a) 흩어짐 검사가
   안 돌았으면 아예 `undetermined` (정직하지만 답이 하나인 피팅의 화면이 빈다),
   (b) 검사가 늘 돌게 시작점을 강제로 둘 이상 다듬는다 (느려진다). 어느 쪽인가.
2. **`_SPREAD_LIMIT` 을 파라미터 종류별로 가른다면 경계를 어디에 긋나.**
   스케일(저항·CPE 크기·시간상수)은 비, 유계 지수는 절대차 — 절대차의 값은?
   `n` 의 물리적 분해능이 얼마쯤인가.
3. **`Ri + Re` 를 따로 내보내야 하나.** 짝의 합은 잰 값인데 지금은 두 미결정
   숫자로만 나가서, 사용자 입장에서는 **잰 것이 아무것도 없어 보인다.**
   `TL1_Ri+Re` 같은 파생 항목을 만드는 것이 맞나, 아니면 `reason` 만으로
   충분한가.
4. **`exchangeable` 을 다른 원소에도 붙여야 하나.** 지금은 `TL`·`TLR` 뿐이다.
   `p(R1,CPE1)-p(R2,CPE2)` 의 두 아크는 **정확한** 축퇴는 아니지만 (주파수로
   갈린다) 아크가 겹치면 사실상 못 가른다 — 지금은 `_order_arcs_by_frequency`
   로 순서만 정한다. 그것으로 충분한가.
5. **`no_error_bar` 가 두 가지를 아직 뭉갠다.** 경계에 눌려 `stderr` 를 지운
   것(`at_bound`)과 야코비안이 특이한 것이 같은 사유로 나간다. 화면에 다르게
   보여야 하는가 — 앞은 "회로가 이 스펙트럼에 안 맞는다", 뒤는 "이 값이 맞춤을
   안 바꾼다" 로 뜻이 다르다.
6. **아직 배관이 없다.** `status`/`reason`/`spread` 는 지금 `wrdkit` 안에서만
   산다 — DB·API·화면·내보내기까지 실어 나르는 것이 #8 의 나머지다. 그 경로
   에서 미리 경고할 것이 있나 (예: 옛 `parameters_json` 행에는 이 열쇠들이
   없다).

## 검사

```bash
make check                       # 651 통과
.venv/bin/python -m pytest packages/wrdkit/tests/test_eis_fit.py -q   # 57 통과
```

실측 파일로는 아직 안 돌렸다 — `WRDKIT_SAMPLE` 경로가 이 세션에 없다.

## 붙여넣는 프롬프트

```
이 저장소의 EIS "쟀다" 판정 규칙을 리뷰해 주세요.

읽을 것:
  docs/reviews/codex-review-determination.md   (이 문서 — 질문 6개가 여기 있습니다)
  docs/reviews/codex-review-soc-scan.md        (지난 리뷰 — #1·#2·#8 의 원문)
  git log --oneline 0de4875e..a81aadd4
  git diff 0de4875e..a81aadd4 -- packages/wrdkit/src/wrdkit/eis

우선순위:
  1) 질문 1 — `not_checked` 를 값과 함께 내는 것이 정직한가, 아니면 자기기만인가.
  2) 질문 2 — `_SPREAD_LIMIT` 을 파라미터 종류별로 가르는 기준.  지난 리뷰의
     #1 이 이것이고, 프로파일 우도로 가는 현실적인 경로(스윕 20개 × 파라미터
     13개를 견디는)를 제시해 주시면 그대로 따르겠습니다.
  3) 질문 3 — 축퇴한 짝의 합을 따로 내보내야 하는가.
  4) `Element.exchangeable` 이 회로 계층에 있는 것이 맞는 자리인가.

형식: 확정(재현 절차 포함) / 의심(근거) / 제안 으로 나눠 주세요.  숫자를 바꾸는
제안에는 그 숫자를 고른 이유를 함께 적어 주세요 — 우리 것도 그렇게 적었습니다.

범위 밖: 그림 저장·화면 레이아웃 (별도 문서), knee, dQ/dV, GITT, VPS·터널.
```
