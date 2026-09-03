# manifests — 원본을 나르지 않고 "무엇을 봤는가" 를 고정한다

`mode-observability/data/` 는 `.gitignore` 대상이다. 3자 데이터셋의 재배포
권리가 불명확하고, 원본이 크다 (Su 2024 SI 의 EIS 176파일 = 90 MB).

대신 여기에 **manifest** 를 커밋한다: 파일별 sha256·크기·행수·스펙트럼 수와
파일명에서 푼 좌표. 다른 사람이 같은 zip 을 받아

    python3 tools/eis_ingest.py --verify

로 **바이트까지 같은 것을 봤는지** 확인할 수 있다. 수치 결과의 근거가
"내 컴퓨터에 있던 어떤 파일" 이 아니라 **이름 붙은 바이트**가 된다.

| 파일 | 무엇 |
|---|---|
| `su2024_eis.tsv` | Su 2024 SI 로 입수한 EIS 데이터. **원 출처는 Zhang et al. 2020** (아래). 생성: `tools/eis_ingest.py --scan` |

## 원본을 어디서 받나

논문 SI 의 zip (`EIS data.zip`) 을 `data/su2024/` 에 푼다. 폴더 구조는
`data/su2024/EIS data/*.txt`. 원 저장소는 아래 Zenodo DOI.

## ★ 출처 확정 (2026-09-03 — 이전의 유보를 해제한다)

이전 판에는 "Su 2024 가 선행 공개 데이터셋을 재사용했을 **가능성**이 있다 —
확정 전에는 출처를 'Su 2024 SI' 로만 적는다" 는 유보가 걸려 있었다.
**Su 2024 원문을 직접 확인해 유보를 해제한다.**

**판정: 재사용이다. Su 등은 이 데이터를 재지 않았다.** 근거 두 개는 원문에
인쇄돼 있다 (digest: `wiki/raw/papers/su2024_drt-soh-health-features.md` §2.1):

- §2.1 `[인쇄]`: "12 LiCoO2/graphite aging data with a 45mAh capacity are
  include in **the dataset supplied in [32]**"
- Data availability `[인쇄]`: "We used an **open dataset** at
  doi:https://doi.org/10.5281/zenodo.3633835, reference number [32]."

**원 출처 (이제부터 1차 인용은 이것이다)**:

> Y. Zhang, Q. Tang, Y. Zhang, J. Wang, U. Stimming, A. A. Lee,
> *Identifying degradation patterns of lithium ion batteries from impedance
> spectroscopy using machine learning*, **Nature Communications 11 (2020)**,
> DOI **10.1038/s41467-020-15235-7**.
> 데이터: **Zenodo DOI 10.5281/zenodo.3633835**.

**인용 규칙**: 이 데이터로 낸 수치의 1차 출처는 **Zhang et al. 2020 /
Zenodo 3633835** 로 적는다. Su 2024 는 "이 데이터로 무엇을 했는가" 의
**선행연구**로 인용한다 (같은 데이터에 DRT + GPR 를 적용한 사례).

## ★ 좌표계 (2026-09-03: Zhang 2020 **원전 인쇄**로 교체)

원전을 본문 + SI 로 직접 흡수했다 (digest:
`wiki/raw/papers/zhang2020_eis-gpr-capacity-rul.md`, 크롭 그림 8장:
`wiki/raw/figures/zhang2020_eis-gpr-capacity-rul/`). 아래는 Su 의 전언이 아니라
**Zhang Methods + SI Fig. 1** 이 인쇄한 것이다.

| 축 | 값 |
|---|---|
| 화학 | LiCoO₂ / graphite |
| **셀 형태** | **코인셀 — Eunicell LR2032** (20 mm × 3.2 mm) |
| 용량 | 공칭 **45 mAh** (1C = 45 mA). **실측 초기용량은 34–42 mAh** |
| 셀 목록 | **12개**: 25 °C 8(25C01–08) · 35 °C 2(35C01–02) · 45 °C 2(45C01–02) |
| **사이클** | **1C(45 mA) CC–CV 충전 4.2 V** / **2C(90 mA) CC 방전 3.0 V** |
| 선행 이력 | 전 셀 **25 °C 30사이클** 후 온도 분기. EoL = 그 후 초기값 **80 %** |
| 측정 주기 | EIS = **짝수** 사이클 · 용량 = **홀수** 사이클 |
| `state I~IX` | 한 사이클 안의 아홉 시점 — 아홉 개 전부 아래 표 |
| 열화 축 | 파일 안의 `cycle number` 열 (state 축과 직교) |
| EIS | 정현파 **전류 5 mA**(≈ C/9) · **60 주파수** · 0.02 Hz–20 kHz |

### state I~IX 아홉 개 전부 + **DC 전류 유무** (SI Fig. 1)

| state | 시점 | DC 전류 | SOC (어림) |
|---|---|---|---|
| I | 충전 전 (3.0 V) | 없음 | 0 % |
| II | 충전 시작 | **있음** | ≈ 0 % |
| III | 충전 20분 후 | **있음** | ≈ 40 % |
| IV | 충전 종료·휴지 전 (4.2 V) | 없음 | 100 % |
| V | 15분 휴지 후 (4.2 V) | 없음 | 100 % |
| VI | 방전 시작 | **있음** | ≈ 100 % |
| VII | 방전 10분 후 | **있음** | ≈ 57 % |
| VIII | 방전 종료·휴지 전 (3.0 V) | 없음 | 0 % |
| IX | 15분 휴지 후 (3.0 V) | 없음 | 0 % |

**★ Phase 2 에 직접 걸리는 결론 두 개**

1. **평형 임피던스로 쓸 수 있는 SOC 는 0 % 와 100 % 두 점뿐이다.** 중간
   SOC(III·VII)는 DC 바이어스 중 측정이라 정상성·선형성 가정을 위반한다.
   → "state 스윕 = SOC 곡선" 이 아니라 **양 끝점 2점 대비**로 설계한다.
2. **`IV vs V` 와 `VIII vs IX` 는 같은 SOC 의 휴지 전/후 쌍**이다 —
   SOC 가 아니라 **완화 시간**만 다른 대비이며 아무도 쓰지 않았다.

`state` 를 열화 축으로 오해하면 Phase 2 설계가 통째로 틀린다. Su 2024 는
**25 °C · state V · 5셀**(25C01/02/03/05/06)만 썼다. **원전(Zhang)도 온도군마다
state V 중심으로만 예측 모델을 세웠고**, state 축은 **복제 축**으로만 썼다
(SI Fig. 2 = state 마다 독립 GPR 아홉 개의 R²: V 0.88 · VII 0.86 · IX 0.81 ·
VIII 0.68 · II 0.66 · I 0.61 · IV 0.60 · III 0.53 · **VI 0.28**).
→ **state VI 는 쓰지 않는다.** state 간 **대비를 feature 로 쓰는 것**은 여전히
아무도 안 했다.

## 아직 닫히지 않은 것 — 2026-09-03 판정

원전으로 **6개 중 4개가 닫혔다.** 남은 것은 **파일 인벤토리** 계열이며,
그것은 Zenodo 원본으로만 닫힌다 (이번 세션에서는 egress proxy 가 `zenodo.org`·
`doi.org` 를 403 으로 차단해 확인하지 못했다). **닫히기 전에는 아래 항목에
의존하는 수치를 내지 않는다.**

| # | 항목 | 판정 (2026-09-03) |
|---|---|---|
| 1 | 셀 목록 불일치 | **닫힘** — Su 의 12셀 열거가 맞다. Methods `[인쇄]` + SI Fig. 4 범례로 교차확인. "온도별 01–08" 가설 폐기 |
| 2 | 파일 수 176 | **원문 미제시 (열림)** — 원전은 Zenodo 파일 구성을 기술하지 않는다. 설계상 정본 개수는 **9×12 = 108 EIS + 12 capacity = 120** 이고 "한 파일 = 한 (셀,state), 여러 사이클" 구조는 확정 → **56파일이 설계 밖**. `__MACOSX` 그림자 가설은 산술(120+120=240)이 안 맞아 단독 설명이 못 된다 |
| 3 | `EIS_state_VI_25C42.txt` | **부분 닫힘 → 조치 확정.** 셀 명부가 두 곳에서 exhaustive 하므로 **셀 42 는 존재하지 않는다**. 정체는 불명이나 **13번째 셀로 취급하지 않는다 — 격리하고 결과에 넣지 않는다** |
| 4 | 셀 형태 · 사이클링 프로토콜 | **닫힘** — 위 좌표계 표 |
| 5 | 헤더 유무가 섞인 이유 | **원문 미제시 (열림)** — 원전도 파일 포맷을 다루지 않는다. 2번과 같은 계열 |

**추가로 등록할 것 (원전이 준 데이터 품질 경고)**

- `[해석]` **셀 간 편차가 극단적이다.** 원전 공개 코드의 `RUL.txt` 를 셀
  구간으로 자르면 훈련 셀 EoL 이 **12 / 162 / 218 / 234 / 414** 사이클이고,
  시험 셀은 논문 Fig. 2 캡션이 **150 / 120 / 30 / 38** 로 인쇄한다 — 동일
  사양·동일 프로토콜의 25 °C 코인셀 8개에서 EoL 이 **20배**로 흩어진다.
- `[해석]` **온도가 배치와 교락돼 있을 수 있다.** SI Fig. 4 에서 초기용량이
  25 °C ≈ 34–36 · 35 °C ≈ 39–39.5 · 45 °C ≈ 40.5–42 mAh 이고, **고온 셀이 더
  오래 산다**. 논문은 이것을 언급하지 않는다. **온도 축을 쓰는 분석은 이
  교락을 먼저 진술하고 시작한다.**

## 이 데이터셋이 답할 수 있는 것과 없는 것

**없는 것**: 이 데이터셋에는 **LLI/LAM 라벨이 없다.** Su 는 열화 모드를
재지 않는다 (LLI·LAM 이 본문에 네 번 나오지만 전부 수치 없는 서술이며,
그중 하나는 다른 논문에서 상속된 인용이다 — digest §2.4 참조).
**2026-09-03: 원전에서 확정됐다** — Zhang 2020 본문 + SI 전체에서 `LLI`·`LAM`·
`lithium inventory`·`half-cell` 이 **각 0회**이고, 모드를 재는 절차(half-cell
OCP fitting · ICA/DVA · 해체분석 · 모드 시뮬레이션)가 하나도 없으며,
Introduction 이 미시 기구 모델링을 `[인쇄]` "unscalable" 하다며 명시적으로
포기한다. 제목의 "degradation **patterns**" 는 **셀마다 다른 감쇠 궤적**을
뜻한다 (본문 용례 2회 = 제목 + Discussion). 원전의 라벨은 **용량(측정)** 과
**RUL(= EoL − cycle)** 둘뿐이다.
따라서 이 데이터로 "SEV 가 LLI 와 LAM_PE 를 가르는가" 를 **직접 물을 수 없다.**

**있는 것**: **"SEV 축 자체가 셀 간에 재현되는가"**. Su Fig. 7 에서 이미
불길한 신호가 나온다 — 동일 조건 5셀에서 전하전달 DRT peak 높이의 SOH 상관이
1/5 에서, 분극저항 R_pol 은 2/5 에서 **부호가 뒤집힌다**. Phase 2 의 첫 물음은
이쪽이어야 한다. 배경과 판단 근거는 위키의
`wiki/concepts/zhang2020-eis-aging-dataset.md` 와
`wiki/questions/pvs-sev-lli-lampe-separability.md`.
