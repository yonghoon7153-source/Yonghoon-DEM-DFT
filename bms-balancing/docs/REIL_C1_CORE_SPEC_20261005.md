# REIL C1-core — 논문 · 보충 자료에서 확인한 핵심 실험 정의 (N1 · 2026-10-05 · 게이트 차수 밖 · 실행 0)

> **기록이다.** 자료 개봉 (P0) · 맞춤 · 설치 · E3b 등록 · 프로토콜 수정의 승인이 아니다. 논문 원문은 이 공개 저장소에 넣지 않는다 — sha256 과 원문 위치
> (쪽 · 표 · 식 · 그림 번호) 만 적는다. 범위는 `REIL_PREREQUISITES_STATUS_20261004.md` §3 N1 그대로: ① 시트의 의미 ② 명목 참값 (LII) 의 정의 ③ 셀 / step
> 선택 + 프로토콜 (v2 + 부속 A + 부속 B) 과 어긋나는 곳의 목록 (고치지 않는다).

## §0 원문 식별

| 파일 (사용자 업로드 2026-10-05 · 저장소 밖) | 크기 | SHA-256 | 쪽 |
|---|---:|---|---:|
| 본문 PDF | 6,696,708 B | `8ccf029c45a3be1b60f8994e36a5dd3b204cf65288b700175d4ad275cb3343c1` | 28 |
| 보충 자료 PDF (Supplementary Materials) | 5,511,025 B | `5d25a800f7e2c32fd849eed972f0ba0a23b36d0999bcb065186e6aab156460c9` | 10 |

서지: T. Li, Y. Zhang, B. Nowacki, S. Navidi, T. Schmitt, S. Hu, C. Hu, "Benchmarking half-cell model fitting approaches for lithium-ion battery
degradation diagnostics," *eTransportation* 29 (2026) 100593 · doi `10.1016/j.etran.2026.100593` (본문 p1 · PDF 메타데이터와 같다 · 공개 저장소 README
의 인용과 같다 — 상태 문서 §6). 아래 "p" 는 본문 쪽, "S" 는 보충 자료의 절 번호다.

## §1 ① 시트의 의미

출처: 본문 Table 1 (p9 — 11 셀의 PE · NE 지름 · SOC 와 모사 LAM_PE · LAM_NE · LLI) · 보충 S1.2 (셀 제작 — 초기 PE SOC 별 절차) · 본문 p12 (흑연
pre-formation · Fig. 8 캡션). 시트 이름은 2026-10-02 브리핑 raw 의 기록이다 — **xlsx 는 열지 않았다.**

**이름 규칙 (추정 — 11 분석 셀 전부와 일치):** `<PE 지름>-LFP <NE 지름>-Gr` = 전극 원판 지름 (mm) · `SOC-x` = LFP 를 x % 만큼 미리 탈리튬한 것
(Table 1 의 PE SOC = 100 − x — 보충 S1.2 의 제작 절차와 같은 뜻) · `SOC-100` = PE SOC 0 % + NE SOC 100 % (S1.2 의 LAM_PE-1 제작) · `after FM` =
흑연 음극을 16 mm LFP 와 C/20 두 cycle 미리 형성한 뒤 12 mm LFP 와 다시 조립한 셀 (p12 의 pre-formation) — 약어 "FM" 자체는 논문에 없다.

| # | 시트 | 논문 대응 | 근거 | 확정도 |
|---:|---|---|---|---|
| 1 | `15-LFP 16-Gr Full-cell @ C_20` | Fresh (15 · 100 · 16 · 0) | Table 1 | 이름 ↔ 설계 일치 |
| 2 | `15-LFP 16-Gr SOC-10` | LLI-1 (15 · 90 · 16 · 0) | Table 1 · S1.2 | 같음 |
| 3 | `15-LFP 16-Gr SOC-20` | LLI-2 (15 · 80 · 16 · 0) | Table 1 · S1.2 | 같음 |
| 4 | `12-LFP 16-Gr SOC-100` | LAM_PE-1 (12 · 0 · 16 · 100) | Table 1 · S1.2 | 같음 |
| 5 | `15-LFP 12-Gr Full-cell @ C_20` | LAM_NE-1 (15 · 100 · 12 · 0) | Table 1 | 같음 |
| 6 | `Full cell after FM SOC 0` | LAM_PE,LLI-1 (12 · 100 · 16 · 0) · pre-formed 흑연 | Table 1 · p12 · Fig. 8(c) | 같음 (FM 의 뜻은 추정) |
| 7 | `Full cell after FM SOC 10` | LAM_PE,LLI-2 (12 · 90 · 16 · 0) · pre-formed 흑연 | Table 1 · p12 · Fig. 8(d) | 같음 (같음) |
| 8 | `15-LFP 12-Gr SOC-10` | LAM_NE,LLI-1 (15 · 90 · 12 · 0) | Table 1 · S1.2 | 이름 ↔ 설계 일치 |
| 9 | `15-LFP 12-Gr SOC-20` | LAM_NE,LLI-2 (15 · 80 · 12 · 0) | Table 1 · S1.2 | 같음 |
| 10 | `12-LFP 12-Gr SOC-10` | All mode-1 (12 · 90 · 12 · 0) | Table 1 · S1.2 | 같음 |
| 11 | `12-LFP 12-Gr SOC-20` | All mode-2 (12 · 80 · 12 · 0) | Table 1 · S1.2 | 같음 |
| 12 | `12-LFP 16-Gr Full-cell @ C_20` | LAM_PE,LLI-1 설계의 pre-formation **없는** 판 — Fig. 8(a) | p12 · Fig. 8 캡션 | **추정** · 11 셀 분석 집합 밖 |
| 13 | `12-LFP 16-Gr SOC-10` | LAM_PE,LLI-2 설계의 pre-formation 없는 판 — Fig. 8(b) | 같음 | **추정** · 밖 |
| 14 | `12-LFP Half-cell @ C_20` | 12 mm LFP 반쪽전지 (Li 금속 상대 · C/20 · 2.5–4.0 V) | S1.2 · S1.3 | 종류는 일치 |
| 15 | `12-LFP C_20 Updated` | 같은 종류의 LFP 반쪽전지로 보인다 — "Updated" 의 뜻은 논문에 없다 · 노트북이 PE 기준으로 쓰는 시트 (v2 §6-2) | S1.2 · S1.3 | **미확인** |
| 16 | `12-Graphite Half-cell @ C_20` | 12 mm 흑연 반쪽전지 (C/20 · 0.01–1.5 V) · 노트북의 NE 기준 | S1.2 · S1.3 | 종류는 일치 |
| 17 | `12-Graphite Half-cell @ C_30` | 논문 · 보충에 C/30 흑연 반쪽전지 서술 없음 (S1.3 은 C/20 만) | — | **미확인** |
| 18 | `Half cell after FM` | 대응 서술 없음 | — | **미확인** |
| 19 | `12-14 12-15` | 대응 서술 없음 (p12–13 의 N/P 비교 셀 — 12 mm LFP 와 15 mm 흑연 — 과 관련 있을 가능성) | — | **미확인** (가능성은 추정) |

- 한 시트 안의 여러 셀 열 (노트북의 `cell_idx` 0 · 1) 이 무엇인지 (복제 셀 · 다른 시험) 는 논문 · 보충에 없다 → P0.
- 결과: **분석 집합 11 시트는 Table 1 의 11 행과 이름 · 설계로 일대일**이고, 노트북의 반쪽전지 기준 둘은 S1.2–S1.3 의 반쪽전지 서술과 종류가 같다.
  ~~나머지 6 시트 (#12 · #13 은 대응 추정 · #15 의 "Updated" · #17 · #18 · #19) 는 논문만으로 확정할 수 없다.~~ **(정정 · §8-3)** 밖 6 = 시트 #12 · #13 · #14 · #17 · #18 · #19 (#15 · #16 = 기준 둘).

## §2 ② 명목 참값과 LII 의 정의

| 항목 | 논문 (원문 위치) | util · 노트북 (v2 §1-1 · §1-3) |
|---|---|---|
| LAM | 식 (13) p7 — `LAM_PE = (m_PE^fresh − m_PE)/m_PE^fresh` · NE 도 같은 꼴 | 명목 m_P · m_N = 1 − LAM |
| LII (원리) | 식 (14) p7 — 두 전극의 화학량론 끝점 사이 최대 순환 리튬: `min(Q_PE^0, Q_NE^100) − max(Q_PE^100, Q_NE^0)` | — |
| LII (단순화) | 식 (15) p7 — N/P > 1 · 충전 끝 PE 잔류 리튬을 가정해 `LII = Q_PE^max − x_offset` · `Q_PE^max = m_PE q_PE^max` · `x_offset = δ_PE − δ_NE` ("fitting reference at the beginning of a full-depth charge") | `LII = (m_P · max_q − (d_P − d_N))/max_q` — 식 (15) 를 max_q 로 나눈 꼴 (같은 구조 · 단위 정규화) |
| LLI | 식 (16) p7 — `(LII_fresh − LII)/LII_fresh` | 명목 LII = 1 − LLI |
| 명목 ("expected" · "Theoretical") | Table 1 p9 의 Degradation Emulation (%) — 제작 설계에서 온 값 · Fig. 6 (p10) 의 "Theoretical" 표식 (축 "Degradation parameter value") | v2 §1-3 의 11 행 (m_P, m_N, LII) |

- **11 행 모두 일치:** 노트북 명목 (m_P, m_N, LII) = (1 − LAM_PE, 1 − LAM_NE, 1 − LLI) 이 Table 1 과 같다. 반올림: (12/16)² = 0.5625 → 0.56 (LAM_NE 44 %) ·
  0.64 × 0.9 = 0.576 → 0.58 (LLI 42 %) · 0.64 × 0.8 = 0.512 → 0.51 (LLI 49 %). LAM_PE 36 % = 1 − (12/15)² 그대로.
- **곱 구조 확인:** LLI 는 pristine 15 mm LFP 의 리튬 재고 (Fresh) 기준이다 — 12 mm (0.64) × PE SOC 90 % = 0.576 · × 80 % = 0.512.
- **제작 방법 (S1.2):** PE SOC 90 · 80 % = 신선 LFP 를 16 mm 흑연과 C/20 (1 C = 1.932 mA/cm² — 공급사 면적 용량) 로 2 · 4 시간 충전 → 분해 → 새 흑연과
  재조립. LAM_PE-1 = (i) 12 mm LFP | 16 mm 흑연을 4.0 V 까지 충전해 얻은 탈리튬 LFP (PE SOC 0 %) + (ii) 16 mm LFP | 16 mm 흑연을 4.0 V 까지 충전해 얻은
  리튬화 흑연 (NE SOC 100 %) 을 재조립. 명목 LLI 0 % 의 계산 근거 (16 mm LFP 에서 온 리튬 · 첫 충전의 SEI 손실) 는 논문에 없다.
- **v2 §6-2 의 가설 (나) 가 맞다:** #3 (LAM_PE-1) 은 리튬 재고를 흑연 쪽에 둔 설계 (S1.2) 로 명목 LII 1 > m_P 0.64 다. util 의 G (`d_P − d_N ≥ 1e-4` → LII <
  m_P) 는 "양극 용량을 넘는 리튬 재고는 없다" 는 모델 가정이고 #3 은 그 가정 밖에서 설계된 셀이다. v2 §1-3 의 `PRIOR_INCOMPATIBLE` 표시는 그대로다.

## §3 ③ 셀 · step 선택

- **맞춤 대상 = 다섯 번째 cycle:** 본문 p8 §4.1 ("The fifth cycle is used for fitting the half-cell model") · 보충 S1.3 ("All the electrochemical data
  collected for processing and analysis were obtained from the fifth cycle of each cell"). 첫 세 cycle 은 formation (p8) · 최대 8 cycle (p8).
- **시험 조건 (S1.3):** 완전지 C/20 (LFP 용량 기준 1 C = 1.932 mA/cm²) · 2.0–3.6 V · 각 step 뒤 20 분 휴지. 반쪽전지 LFP C/20 · 2.5–4.0 V · 흑연 C/20
  (1 C = 1.903 mA/cm²) · 0.01–1.5 V · 20 분 휴지. 반쪽전지 원판 12 mm · Li 금속 15.6 mm (S1.2).
- **기준점:** x_offset 은 "full-depth charge 의 시작" 기준 (p7) — 맞추는 곡선이 충전 곡선이라는 뜻으로 읽힌다 (추정 · 그림 대조 전).
- **노트북의 `step_idx` (6 · 7 · 0) · `cell_idx` (0 · 1) 가 "다섯 번째 cycle 의 (충전) step" 과 같은지는 논문 · 보충에 없다** → P0 에서 자료를 열어 대조할
  항목 (v2 §1-5 의 "반복 cycle 지정과 step 분절을 같은 것으로 가정하지 않는다" 그대로).

## §4 프로토콜 (v2 + A + B) 과 어긋나거나 새로 보이는 곳 — 고치지 않은 목록

1. **v2 §6-2 의 "의미 미확인" 중 풀린 것 · 남은 것:** SOC 표식 · LII 정의 · FM (셀 쪽 뜻) 은 §1 · §2 로 풀렸다. 질량 인자 20.16 · 11.4 와 노트북의 장전량
   13.5 · 5.77 mg/cm² 는 논문 · 보충에 없다 (보충 S1.1 은 공급사 면적 용량만 — LFP 1.932 · 흑연 1.903 mAh/cm²) → 여전히 미확인.
2. **#3 의 해석:** 가설 (나) 확인 (§2) — v2 §1-3 의 "허용 영역이 명목값을 배제하는 대수적 사실" 그대로 · 문구 정정 불필요.
3. **참값 불확실성 (v2 §6-1 이 미리 적어 둔 자리 — 크기는 논문에 셀별로 없다):**
   a. 명목은 설계값이고 formation (첫 세 cycle) 의 SEI 리튬 손실을 넣지 않는다. 논문은 N/P 가 클수록 첫 cycle CE 가 낮다고 적는다 (p12–13 · Fig. 9 —
      15 | 16 셀이 가장 높은 86.5 %) → 명목 LLI 의 오차가 셀마다 다를 수 있다.
   b. 높은 N/P (12 mm LFP | 16 mm 흑연) 셀의 LAM_NE 명목 0 은 저자 스스로 "undetermined emulation of LAM_NE" 라고 적는다 (p14) · LAM_PE-1 의 추정 m_NE 가
      명목보다 크게 낮은 이유를 비균일 리튬화로 설명 (p10–11 · §4.2.1) → #3 · #5 · #6 의 명목 m_N (1) 은 불확실.
   c. PE SOC 90 · 80 % 의 10 · 20 % 는 공급사 명목 용량 기준의 전하량이다 (S1.2) — 실제 LFP 용량과의 비는 미확인.
   d. FM 셀 (#5 · #6) 은 흑연을 미리 형성해 formation 손실이 다른 셀과 다를 수 있다 (p12 — 수치 없음 · 방향은 추론).
   → v2 §6-1 대로 명목 비교와 함께 "실제 참값 불확실성 — a–d (크기 미정)" 으로 적는다. 사후에 참값 영역을 넓히지 않는다.
4. **명목 LII 의 기준:** ~~식 (16) 은 LLI 를 맞춘 신선 셀 LII 대비로 정의하지만, Fig. 6 (· A.4) 의 "Theoretical" 표식과 노트북 명목표는 (1 − LLI) 를 util 의~~
   ~~정규화 LII (÷ max_q) 와 직접 비교한다 — 둘이 같으려면 신선 셀에서 x_offset = 0 · m_P = 1 이어야 한다 (v2 §1-3 의 #0 "경계" `d_P = d_N` 가 그 가정).~~
   ~~제안 (반영은 사용자 결정): H1 보고에 "명목 비교의 기준 = util 정규화 LII (논문 Fig. 6 과 같은 기준)" 을 함께 적는다.~~ **(정정 · §8-1)**
5. **max_q 어림 (v2 §1-4 · 추정 — 판정에 쓰지 않는다):** 공급사 면적 용량 (S1.1) 과 노트북 상수 (LFP 장전량 13.5 mg/cm² · 인자 20.16) 로, 반쪽전지가
   공급사 명목 용량을 낸다고 가정하면 max_q ≈ 1.932 / 13.5 × 20.16 ≈ 2.89 mAh — v2 §1-4 의 어림 (3.0–3.3 · 비용량 0.150–0.165 가정) 보다 조금 낮다. 어느
   쪽이어도 #2 · #8 조건 (max_q ≤ 2.5) 밖 · #10 (≤ 3.85) · #1 · #7 (≤ 5.0) · #6 · #9 (≤ 8.3) 안 → v2 §1-4 의 정성 결론은 바뀌지 않는다. 확정은 P0.
6. **셀 · step:** §3 — `step_idx` · `cell_idx` 대응은 P0. FM 셀의 `step_idx` 0 은 재조립 셀의 자료가 어디서 시작하는지에 달렸다 (P0).
7. **코드 ↔ 논문 서술 (E3a 는 코드 경로 그대로):** 논문 p8 "PCHIP 으로 250 점" ↔ util f2 의 실험 곡선 100 점 (v2 §1-1). E3a 는 코드를 바꾸지 않는다 —
   E3b 를 등록할 때 이 차이를 비교 기준에 적어야 한다.
8. **C1-E3b 와 닿는 곳 (위치만 · 등록 아님 · 수치 옮기지 않음):** 결과 Fig. 6 (p10) · Fig. A.2–A.4 (부록 — A.4 는 p23) · 대표 해 = Utopia 점까지 정규화
   거리가 가장 작은 해 (p9 — v2 §2 E3b 칸이 예로 든 `find_balanced_solution` 과 같은 방식으로 보인다). p9–10 에서 저자들은 LAM_PE-1 의 추정 m_PE 와 LII
   가 "nearly equal" 이라 적고 원인으로 LFP 평탄부를 든다 — v2 §1-2 의 대수 (G 아래 LII < m_P) 와 같은 방향의 관측이고 둘은 서로 배타적이지 않다. 판정은
   E3a / H 의 몫이다.

## §5 이 문서가 하지 않은 것

`LFP_Data.xlsx` · `results/*.pkl` · 노트북 열기 · 맞춤 · 설치 · 버전 실측 · E3b 등록 · 프로토콜 (v2 · A · B) 수정 · 논문 원문 커밋. §4 는 고치지 않은 목록이다.

## §6 다음 (각각 사용자 결정 · 자동 시작 없음)

- **C1-core 의 논문 쪽 몫은 채웠다** — 분석 11 시트의 의미 · 명목 정의 · "다섯 번째 cycle". 남은 대응 (`step_idx` · `cell_idx` · 분석 밖 6 시트) 은 자료를
  열어야 하므로 P0 에 넘긴다.
- §4 를 프로토콜에 반영할지 (새 부속 C + 재검토) — 제안: §4-3 (참값 불확실성) · §4-4 (명목 기준) · §4-6 (P0 출력에 step 대응 기록) 은 P0 승인 요청 (N3)
  전에 부속 C 로 묶는 편이 낫다 — P0 이 무엇을 출력해야 하는지가 달라지므로.
- C6 실행 (이 컨테이너 — 판 확인 · 프로필 봉인 · COBYQA 옵션 대조) — 별도 승인.

## §7 덧붙임 (2026-10-05 — 위키 digest 교차 대조 · 위 §0–§6 은 그대로 · 프로토콜 반영은 부속 C)

교차 대조: 논문 에이전트의 위키 digest `wiki/raw/papers/li2026_half-cell-fitting-multiobjective-benchmark.md` (커밋 `48f48e959` · 컴파일
`040c3ab8c` — 같은 원문을 다시 읽고 그림을 판독한 기록). §1–§3 의 원문 사실과 어긋난 곳은 없었고 (digest §16-1 "일치"), 아래를 더한다. 반영은
`REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_C.md` (같은 커밋).

- **번호 체계 — 이 문서의 혼동 주의:** §1 표의 `#` 는 시트 순서 (1–19) 이고, §2 · §4 의 `#3` · `#5` · `#6` 등은 v2 §1-3 의 0-기반 셀 번호
  (#0 Fresh … #3 LAM_PE-1 … #10 All mode-2) 다.
- **§3 의 "충전 곡선 (추정)":** 논문 Fig. 7 · A.3 의 맞춤 곡선은 ≈2.33 V → 3.6 V 의 충전 곡선이다 (digest G13 · 그림).
- **§2 의 "같은 구조":** 논문 Fig. 3(g) · Fig. 5 · 식 (15) 의 δ 규약에서 맞다. 인쇄된 식 (7) 은 `q = (Q − δ)/m` 이라 util 의 `Q = m q − d` 와
  부호가 반대다 (δ = −d · digest D7) — 식 (7) 을 그대로 구현하면 `x_offset` 부호가 뒤집힌다.
- **§4-3 에 더할 원인 (후보):** 낮은 N/P (15 mm LFP 와 12 mm 흑연 · 명목 N/P 0.63) 셀 셋 (v2 #4 · #7 · #8) 의 충전 끝 음의 dV/dQ · 평탄부 —
  리튬 석출과 들어맞는 신호 (digest §9-3 · 그림 판독 + 해석 · 논문은 다루지 않는다). ~~a 의 크기 단서: Fig. 9 의 CE 곱 ≈ 0.83 → Fresh 형 셀의~~
  ~~formation 손실 ≈ 17 % (digest §9-2 · 그림 · 가정 둘).~~ **(철회 · §8-2 — U-a 크기 미정)**
- **§4-5 에 더할 어림:** 출판 그림의 판독으로 열 셀의 `Q_end / LII` ≈ 3.10–3.16 mAh (`d_N ≈ 0` 가정 · digest §8-4) — 부속 A §5-3 의 #2 · #8
  τ = 0.02 문턱 25/8 = 3.125 와 판독 오차 안에서 겹친다. 판정에 쓰지 않는다 — P0 의 max_q 가 정한다.
- **§4-7 에 더할 차이:** 식 (9) ↔ f1 · 식 (11) ↔ f3 · 부등식 G · 상자 · NE 의 0.01 V 상수 외삽은 논문에 없거나 다르다 (digest §3 · §16-1).
- **§4-8 의 "nearly equal" 의 실제 모양:** LII 가 0.64 로 내려온 것이 아니라 m_PE 가 ≈ 1.0–1.1 로 올라간 설계의 '거울' 해다 (digest §8-5 ·
  그림) — 같은 붙음이 15 mm LFP 셀들의 QV 단독 맞춤에서도 보인다 (digest §8-3). 수치는 출판 그림의 판독이고 E3b 는 미등록 그대로다.

## §8 정정 (2026-10-05 — 부속 C 재검토 RV2C-N1–N3 · 위 §0–§7 의 해당 문장은 취소선으로 남긴다 · 프로토콜 반영은 부속 D)

회신: `bms-balancing/reviews/prereview_reil_v2_annexC_20261005/` (`ANNEX_C_CONDITIONALLY_ACCEPTABLE_THREE_LOCAL_DOCUMENT_CORRECTIONS` · C1-core 의
논문 쪽 근거 수용 · 실물 시트 · 셀 열 · step 대응은 P0 · v2 + A + B 의 C2 종결 유지). 반영: `REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_D.md` (같은
커밋). 아래 세 곳 말고는 고치지 않는다.

- **8-1 (RV2C-N1 · §4-4):** 명목 목표값은 Table 1 · Fig. 6 / A.4 의 "Theoretical" 표식과 대응하지만, 출판 추정치의 정확한 정규화 분모가 util 의
  `max_q` 와 같다고 확인한 것은 아니다. util 정규화 LII 를 `z`, 같은 기준의 Fresh 값을 `z_F` 라 하면 식 (16) 의 상대 잔존량은 `z / z_F` 이고,
  `z_F = m_P,F − (d_P,F − d_N,F) / max_q` 다 — 명목 Fresh 의 `m_P = 1` · `d_P = d_N` 은 `z_F = 1` 을 주는 충분조건이지 유일한 필요조건이 아니다.
  식 (16) 의 상대 LLI 는 미등록 그대로 (부속 D §1).
- **8-2 (RV2C-N2 · §7 의 "a 의 크기 단서"):** Fig. 9 의 CE 곱 (≈ 0.83 — 우리 판독) 은 CE 비 (`Q_dis / Q_ch`) 들의 곱이라 Li 재고 잔존율 ·
  formation 손실률로 환산하지 않는다 — cycle 사이 용량과 초기 재고를 잇는 결속 없이는 망원곱이 아니다. "≈ 17 %" 는 철회 · U-a (§4-3 a) 의 크기는
  미정 (부속 D §2).
- **8-3 (RV2C-N3 · §1 끝):** 기준 둘 = 시트 #15 `12-LFP C_20 Updated` · #16 `12-Graphite Half-cell @ C_20` 이므로 분석 · 기준 밖 6 = **시트 #12 · #13 ·
  #14 · #17 · #18 · #19** (이름은 부속 D §3-3). §6 과 부속 C 의 "분석 밖 6 시트" 도 이 여섯이다. #15 의 "Updated" 는 미확인 그대로 기록하되 밖 6 에
  넣지 않는다. 이 집합은 위 §1 표의 집합 차이고 실제 xlsx 를 본 것이 아니다 — P0 의 대조 · cycle 과 방향의 판정 규칙은 부속 D §3.
