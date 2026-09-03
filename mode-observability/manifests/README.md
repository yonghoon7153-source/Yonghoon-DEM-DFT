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

## 좌표계 (Su 2024 §2.1 이 인쇄한 것과 우리 실측의 대조)

| 축 | 값 | 대조 |
|---|---|---|
| 화학·용량 | LiCoO₂/graphite, **45 mAh** (1C = 45 mA) | capacity 파일의 45.00 mA 와 일치 |
| 셀 형태 | **Su 원문에 없다** — 코인셀 여부 미확인 | Zhang 2020 에서 확인할 것 |
| 셀 목록 | 25 °C **8개**(25C01–08) · 35 °C **2개**(35C01–02) · 45 °C **2개**(45C01–02) = **12개** | 온도별 01–08 이 **아니다** — 아래 미확인 1 |
| `state I~IX` | **한 충방전 사이클 안의 아홉 측정 시점** (열화 단계 아님) | `EIS_state_{I..IX}_*` 의 의미 확정 |
| `state V` | **100 % SOC, 15분 휴지 후** | 나머지 8개 state 의 SOC/시점은 원문에 없음 |
| 열화 축 | 파일 안의 **`cycle number` 열** | state 축과 직교 |
| EIS | 정현파 **전류 5 mA**(≈ C/9) · **60 주파수** · **0.02 Hz–20 kHz** | 4,920행 = 60 × 82 스펙트럼과 일치 |

`state` 를 열화 축으로 오해하면 Phase 2 설계가 통째로 틀린다. Su 2024 는
**25 °C · state V · 5셀**(25C01/02/03/05/06)만 썼다 — **온도 축과 state 축
전체가 미사용 자원**이다.

## 아직 닫히지 않은 것 (Zhang 2020 원문 / Zenodo 로 닫아야 함)

Su 원문으로는 닫히지 않는다. **닫히기 전에는 아래 항목에 의존하는 수치를
내지 않는다.**

1. **셀 목록 불일치** — Su 는 12셀만 열거한다. 우리 파일명 패턴이 온도별
   01–08 을 실제로 포함한다면 둘 중 하나가 틀렸다. `su2024_eis.tsv` 의
   실제 열거를 확인할 것.
2. **파일 수 176** — 12셀 × 9 state = 108 EIS + 용량 12 = **120** 과 맞지
   않는다. `__MACOSX` 그림자 파일·추가 파일 여부를 확인할 것.
3. **`EIS_state_VI_25C42.txt`** (셀번호 42) — Su 의 열거로 설명되지 않는다.
4. **셀 형태**(코인셀?) 와 **사이클링 프로토콜**(충방전 전류·전압창) — Su 는
   적지 않는다.
5. **헤더 유무가 섞인 이유** — Su 는 파일 포맷을 다루지 않는다.

## 이 데이터셋이 답할 수 있는 것과 없는 것

**없는 것**: 이 데이터셋에는 **LLI/LAM 라벨이 없다.** Su 는 열화 모드를
재지 않는다 (LLI·LAM 이 본문에 네 번 나오지만 전부 수치 없는 서술이며,
그중 하나는 다른 논문에서 상속된 인용이다 — digest §2.4 참조).
따라서 이 데이터로 "SEV 가 LLI 와 LAM_PE 를 가르는가" 를 **직접 물을 수 없다.**

**있는 것**: **"SEV 축 자체가 셀 간에 재현되는가"**. Su Fig. 7 에서 이미
불길한 신호가 나온다 — 동일 조건 5셀에서 전하전달 DRT peak 높이의 SOH 상관이
1/5 에서, 분극저항 R_pol 은 2/5 에서 **부호가 뒤집힌다**. Phase 2 의 첫 물음은
이쪽이어야 한다. 배경과 판단 근거는 위키의
`wiki/concepts/zhang2020-eis-aging-dataset.md` 와
`wiki/questions/pvs-sev-lli-lampe-separability.md`.
