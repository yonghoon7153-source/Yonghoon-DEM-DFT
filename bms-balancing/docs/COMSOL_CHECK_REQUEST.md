# COMSOL 확인 요청 — `ICA_degradation mode.mph` (2026-09-13)

**받는 분**: COMSOL 라이선스로 이 모델을 여실 수 있는 분
**보내는 쪽**: 안용훈 (마이크로 쇼츠 모델 디버깅)
**걸리는 시간**: 1번만 하면 **약 5분**. 2번까지 하면 30분 + 계산 시간.
**모델을 고쳐 달라는 요청이 아닙니다.** 값을 몇 개 읽어서 알려 주시면 됩니다.

---

## 왜 필요한가 (세 줄)

`.mph` 의 XML 을 뜯어서 정적 분석을 했는데, **파일에 저장된 값만으로는 COMSOL 이 실제로 무엇을
쓰는지 확정할 수 없는 자리가 세 군데** 있습니다. 특히 입자 노드의 최대농도는 사용자 입력칸에
`cs_Gr_max*dm_fNE` 라는 식이 들어 있는데 **출처 선택은 "From material"** 로 되어 있어서,
그 식이 쓰이는지 아닌지가 파일만으로는 안 갈립니다. 이 하나로 진단이 완전히 뒤집힙니다.

또 하나 — **저장된 해(solution)와 지금 편집 상태의 설정이 다릅니다.** 그래서 기존 해에서 값을
읽으면 안 되고, **지금 설정으로 새로 초기화한 값**을 봐야 합니다.

---

## 1번 요청 — 계산 없이 값만 읽기 (약 5분) ⭐ 이것만이라도

### 1-A. GUI 에서 눈으로 확인 (스크린샷이면 더 좋습니다)

모델 트리에서 아래 두 노드를 열고, **"Maximum concentration"(최대농도) 칸의 드롭다운**이
`From material` 인지 `User defined` 인지 봐 주세요.

```
Component 1 > Lithium-Ion Battery (liion)
  > Porous Electrode 1 - Graphite > Particle Intercalation 1     ← 여기
  > Porous Electrode 2 - NCM811   > Particle Intercalation 1     ← 여기
```

같은 화면에서 **"Initial species concentration"(초기 농도)** 칸의 식도 같이 적어 주세요.

> 참고: 비활성인 `Additional Porous Electrode Material 1 - Silicon` 아래의 같은 노드는
> `User defined` 로 되어 있습니다. 두 전극이 그것과 같은지 다른지가 핵심입니다.

### 1-B. 값 읽기 — 계산은 안 해도 됩니다

`Study 1` 우클릭 → **`Get Initial Value`** (초기값 가져오기). 몇 초면 끝나고 실제 계산은 안 합니다.

그 다음 `Results` 우클릭 → `Evaluation Group` 추가 → `Global Evaluation` 추가 →
**Expressions 칸에 아래를 그대로 붙여 넣고** 실행해서, 나온 표를 그대로 보내 주세요.

```
liion.pce1.pin1.cEeqref
liion.pce2.pin1.cEeqref
liion.soc_average_pce1
liion.soc_average_pce2
x_Gr_init
x_NCM_init
epss_el
epss_pos
epss_Gr
nLi_target
dLi_LLI
cs_Gr_max
cs_NCM_max
dm_fNE
dm_fPE
E_cell
```

> `liion.pce1.pin1.cEeqref` 라는 이름이 안 먹으면, Global Evaluation 의 Expression 칸 옆
> **화살표 버튼 → Model > Component 1 > Lithium-Ion Battery** 로 들어가서 "Maximum concentration"
> 비슷한 이름을 찾아 골라 주세요. 이름이 버전마다 조금 다릅니다.
> 그것도 안 되면 **1-A 의 스크린샷만으로도 충분**합니다.

### 1-C. 지금 선택된 것이 무엇인지

`Results > Datasets` 에서 **어느 dataset 이 굵게(기본) 되어 있는지**, 그리고
`Study 1 > Parametric Sweep` 노드가 **활성인지 비활성(회색)인지** 알려 주세요.

---

## 우리가 알고 싶은 것 (읽는 법)

| 만약 | 뜻 |
|---|---|
| `liion.pce*.pin1.cEeqref` 가 **31507 / 50707.7** 로 나온다 | 재료값이 쓰인다 = 사용자 식은 안 쓰인다 → **우리 진단이 틀렸고 모델은 이 축에서 정상**입니다 |
| **30696.6 / 49204.7** 로 나온다 | 사용자 식(`cs_max × dm`)이 쓰인다 → LAM 이 두 번 걸린 것이고 수정이 필요합니다 |
| `soc_average_pce2` 가 **0.9241** | 정상 |
| `soc_average_pce2` 가 **0.9523** | 초기농도와 최대농도의 짝이 안 맞습니다 |
| `soc_average_pce2` 가 **0.9190** | 옛 저장 설정이 살아 있습니다 (별도 문제) |

---

## 2번 요청 — 여유가 되시면 (30분 + 계산)

**원본은 건드리지 말고 복사본에서** 해 주세요.

1. `파일 > 다른 이름으로 저장` → `ICA_degradation mode_check.mph`
2. `Study 1` 의 **Parametric Sweep 을 끈 상태**로, 파라미터가 `C_rate = 0.1`,
   `sigma_short = 1e-20` 인지 확인
3. `Compute` (전에 8초쯤 걸렸습니다)
4. 아래를 CSV 로 export 해 주세요 — `Results > Export > Table` 또는 `Plot Group` 에서 우클릭 → Export

   | export 할 것 | 표현식 |
   |---|---|
   | 시간 vs 셀전압 | `t`, `E_cell` |
   | 시간 vs 양극/음극 SOC | `t`, `liion.soc_average_pce1`, `liion.soc_average_pce2` |
   | 시간 vs 전류 | `t`, `liion.cdc1.Icell` |

5. 계산이 끝난 뒤 **1-B 의 Global Evaluation 을 한 번 더** 돌려서 값이 바뀌었는지 봐 주세요.

---

## 3번 — 답이 가능하시면 (계산 불필요)

1. 입자 노드의 최대농도 칸에 `cs_Gr_max*dm_fNE` 를 **누가 언제 왜** 넣었는지 기억나시나요?
   지금은 선택이 `From material` 이라 안 쓰이는 상태로 보입니다. **의도적으로 되돌린 것**인지,
   아니면 **넣어 놓고 선택을 안 바꾼 것**인지가 중요합니다.
2. `LAM_PE` / `LAM_NE` 를 모델에 넣을 때 의도한 뜻이 어느 쪽인가요?
   - (a) 전극 전체 용량이 `1−LAM` 배로 준다 (부피분율만 줄인다)
   - (b) 부피분율도 줄고 남은 재료의 사이트 밀도도 준다
3. `dPE = 0.0101000283` 은 어디서 온 값인가요? 받은 적합 결과 4개 파일에서 못 찾았습니다.
4. `sigma_short` 를 쓸 때 그 값이 **재료 고유 전도도**인가요, 아니면 **실효 전도도**인가요?
   (분리막 상의 부피분율 보정 `0.45^1.5 ≈ 0.302` 가 곱해지는지 여부가 갈립니다.)

---

## 안 해 주셔도 되는 것

- 모델 수정 · 파라미터 변경 · 파일 정리 — **전부 하지 마세요.** 값만 읽으면 됩니다.
- 저장된 옛 해(solution) 삭제 — 그대로 두세요. 오히려 비교 자료입니다.
- 1번이 어려우면 **1-A 스크린샷 두 장**만으로도 큰 도움이 됩니다.

문의: 안용훈
