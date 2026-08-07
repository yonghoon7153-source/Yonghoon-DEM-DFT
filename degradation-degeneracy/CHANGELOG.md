# CHANGELOG

물리 파라미터·수식 변경은 반드시 여기에 근거와 함께 기록한다.
(`physics(...)` 타입 커밋과 1:1 대응)

## [Unreleased]

### Phase 0
- 프로젝트 스캐폴딩
- 환경 검증 완료 (2026-08-05): pybamm 26.7.1.0, IDAKLU OK, composite DFN OK.
  완방상태 자동 산출 검증: Gr=36.6, Si=3446.1, PE=58439.9 mol/m3
  → 원본 하드코딩(36.7/3446.3/58439.9)과 0.3% 이내 일치 확인.
  (하드코딩 값 자체는 현행 baseline과 정합했으나, 규칙대로 자동 산출을 사용)

### Phase 2 — physics 변경 기록
- `mode_protocol.lam_pe_de: charge_first → discharge_first` 정정.
  근거: 원본 코드 L174 `run_sweep(experiment, LAM_pe_de, ...)` 는
  experiment(discharge_first)를 사용하며, update_fn도 완충 기준
  `17038.0/(1-i)` 로 discharge_first 시작상태와 정합한다.
  문서 초안(02_CODE_AUDIT/03_ARCHITECTURE)의 표가 원본과 달랐던 것.

### Phase 3 — physics 변경 기록 (조합 격자 규약)
- 조합 격자는 charge_first(완방 프레임)로 통일하고 모든 초기 농도를
  완방상태 기준으로 명시 설정한다.
  - 03_ARCHITECTURE 4절 스케치는 lam=0인 전극 농도를 완충 baseline으로 남겨
    전극 간 상태 불일치(재고 이중계상)가 발생 → 수정.
  - LLI는 NE·PE 농도 모두에 (1−lli) 적용.
    스케치(NE만)는 완방 프레임에서 전체 재고의 ~0.1%만 제거해 사실상 no-op.
    모든 저장소 스케일링은 전체 재고를 정확히 lli 비율만큼 제거 (Birkl LLI 정의 정합).
  - guards: 완방 재고를 수용 불가한 조합(PE 농도 > c_max 등)은
    infeasible로 failed.csv에 기록하고 skip (PE-limited 영역).

### 변경 예정 — 근거 기록 필요
- [ ] 완방상태 하드코딩(36.7 / 3446.3 / 58439.9) 제거 → 자동 산출
      근거: 원본 코드 내 경고 주석, 주석값(428/82591/62877)과 코드값 불일치
- [ ] fitting bound 하한 재검토
      근거: 33p `lb=[1.00, ...]`은 α<1(열화)을 표현 불가. 정규화 기준 확인 필요

### Phase 4 — physics 변경 기록

- **LLI 환산식을 전하 보존으로 재유도** (`src/inventory.py`)

      LLI = 1 − r·[ w_PE·α_PE + w_NE·α_NE + κ·(β_NE − β_PE) ]
      w_PE, w_NE : reference 재고 중 각 전극 보유 비율 (합 1)
      κ          : Q_ref / n_Li_ref

  근거: 21p 식과 원본 코드 식 둘 다 합성 데이터의 **알려진 정답 LLI를 재현하지
  못했다** (평균 |오차| 0.128 / 0.200, 참값 LLI=0인 조건에서 추정값이 LAM_NE와
  거의 같게 나옴). 전하 보존으로 유도하니 두 군데가 달랐다.
    (a) 가중치 — 21p는 재고가 전부 양극에 있다고 가정하나, 이 셀은 기준 상태에서
        재고의 71%가 음극에 있고 총재고(8.1 Ah)가 가용용량(5.72 Ah)의 1.4배다.
    (b) β 항 부호 — 유도는 +(β_NE − β_PE), 21p는 +(β_PE − β_NE).
        원본 코드 주석의 "기존 부호가 반대였음"이 같은 지점을 가리킨다.
  검증: 유도식 |오차| 0.012 (21p 0.128, 원본 0.200). 자유 최소제곱 하한 0.0097에
  근접하며, 회귀로 얻은 상수(0.313/0.607/0.715)가 유도값(0.291/0.709/0.706)과 일치.
  21p·원본 규약도 `lli_hat_21p` / `lli_hat_code` 열로 함께 저장해 비교 가능.

- **fitting bound**: 33p 원본(`lb=[1.00,…]`)을 기본값에서 제외하고 expanded를
  기본으로 사용. 근거: α = (1−LAM)/r 이므로 α=1.00은 곧 "LAM = 용량손실"이고,
  33p bound 안에 참값이 들어오는 조건은 합성 격자의 17%뿐이다.
  두 preset을 모두 남겨(`--bounds original_33p|expanded`) 비교 자체를 결과물로 삼는다.

### Phase 4 — 기준 곡선 2-case 비교 결론 ★

full-range half-cell OCV(OCP 함수 직접 평가)를 기준으로 쓰면 α·β가 논문 규약의
의미를 정확히 갖는다. 기준 조건 자체 fitting이 baseline 값을 되돌려 이를 검증한다
(β_PE,ini = -0.395 → y0 = 0.270 = 17038/63104).

coarse 95조건, 정답 대비 평균 |오차|:

    Case 1 (full-range half-cell 기준)   LAM_PE 0.021  LAM_NE 0.027
        LLI, NE 기준식  1-(α_NE+β_NE-β_PE)r/(...)_ini    0.011   ★
        LLI, 21p 표기   1-(α_PE+β_PE-β_NE)r/(...)_ini    0.139
    Case 2 (기준 셀 창 + 유도식)          LAM_PE 0.028  LAM_NE 0.011  LLI 0.012

결론 두 가지:
 1) 논문 **구조**는 맞다 — 올바른 기준(full-range half-cell)에서는 셀별 상수
    없이 ini 정규화만으로 정답이 복원된다 (LLI 오차 0.011).
 2) 다만 **어느 전극 기준으로 재고를 세느냐**가 다르다. 21p 슬라이드 표기
    (PE 기준)는 0.139로 복원 실패하고, 전하 보존이 지시하는 NE 기준이 맞다.
    완충 상태에서 PE 보유 Li = -β_PE·C_full, NE 보유 Li = (α_NE+β_NE)·C_full
    이므로 총재고 = (α_NE + β_NE - β_PE)·C_full.
    원본 코드 주석의 "기존 부호가 반대였음"이 같은 지점을 가리킨다.

→ 즉 논문 식을 임의로 바꾼 것이 아니라, **기준을 논문과 맞춘 뒤 전극 기준만
  전하 보존에 맞게 고른 것**이다. Case 2의 유도식은 기준 셀 창을 쓸 때의
  등가 형태이며, 두 경로가 독립적으로 같은 결론(LLI 오차 0.011~0.012)에 도달한다.

### Phase 4 — 적대적 리뷰 반영 (2026-08-05)

Fable 최고강도 리뷰 20건 중 수용 15건 즉시 수정, 해석 규칙 5건 문서화.
**1순위 판정: V100에서 돌던 fine fitting(8dfd3b6)은 유효 — 죽일 필요 없음**
(리뷰어가 수식 재유도 + coarse 실데이터 스팟 재실행으로 교차 확인).

즉시 수정 (코드):
- F3  run.sh halfcell 경로의 FIT_ARGS 인덱스 버그 (--nproc 값을 덮어씀) → preset을 배열 구성 전에 결정
- F2  p_ini 기준 조건을 max(r)로 고르던 것 → truth(전부 0 + noise=0) 명시 선택, 없으면 예외
- F13 .fit.lock 판정이 src.grid만 인정 → src.fitting도 인정
- F12 recompute_lli.py가 halfcell 행을 grid 규약으로 덮어쓸 수 있던 것 → 가드 + p_ini를 행에 저장
- F11 halfcell LLI 식은 전 범위 테이블 전제 → coverage 검사, sim 테이블이면 예외
- F9  dqdv scale이 타깃 격자 의존 → reference 자기 격자로 계산 (조건 불변)
- F6  expanded β 하한 -0.40이 고LLI 코너 참값(-0.36)과 겹침 → -0.60
- F16 _minimize_until_stable의 (p, J) 불일치 가능성 → best_x 갱신 조건 수정
- F17 n_eval이 best restart만 집계 → 전체 합
- F18 fit resume이 목적함수 구성 변경을 감지 못 함 → 실행 서명 포함 완료 파일
- F19 전부 resume-완료 시 crash → 가드
- F1  α=1 소프트 벽(창 부족 벌점의 파일업)은 bound_active에 안 잡힘 → alpha_wall_* 열 추가
- F4  restart 원본 미저장 → restarts_json 열 (사후 재집계용)
- F20 테스트 공백 → halfcell 항등/스케일 불변, F16 회귀, dqdv 해석 검증 추가 (총 85개)

수정 후 Case 1 정확도 (coarse 95, clean): LAM_PE 0.018 / LAM_NE 0.018 / LLI 0.0088
— F9(스케일)·F2(기준 선택) 수정만으로 이전(0.054/0.126/0.039) 대비 대폭 개선.
이제 Case 1(논문 기준)과 Case 2(유도식) 모두 LLI ~0.01 수준으로 수렴.

해석 규칙 (Phase 5·6에서 반드시 적용):
- F1  grid 기준의 α_true<1 조건은 "원리적 복원불가군"으로 분리 집계 (alpha_wall_* 사용)
- F4  degeneracy 집계는 n_restarts로 조건화 (adaptive 조기 종료 때문), restarts_json으로 노이즈 환산 임계 재집계
- F5  degenerate 판정은 clean-fit 방법 바이어스(LAM_PE ~2.9%p)를 베이스라인으로 차감
- F10 noisy dQ/dV의 피크 가중은 스퓨리어스 피크로 희석될 수 있음 — "피크 가중 실패"로 오독 금지
- F14 격자에 "저LLI + 고LAM_PE" 코너가 없음(완방 프레임 guard 산물) — 22p 결론 서술 시 명시
- F15 (PLAUSIBLE) reference만 완충 시작이라 lli→0 극한 공통 오프셋 가능 — sanity 조건 1개로 정량화 예정

### Phase 4 — physics 수정: 영 조건 프레임 정렬 (F15 확정, 2026-08-06)

`build_overrides`가 영 조건에서만 빈 dict를 반환해, 그 조건만 완충 baseline에서
시작하고 나머지는 완방→CC충전 프레임이었다. CC-only 충전은 baseline 완충점에
정확히 닿지 못하므로 **reference만 1.74% 더 충전된 상태**가 됐다.

실측 (lli=1e-4, 사실상 무열화 조건):
    수정 전  r=0.98264  lam_pe_hat=0.01575  lli_hat=0.01565
    수정 후  r=0.99995  lam_pe_hat=0.00005  lli_hat=0.00002

→ 참값 0인 조건의 ~1.6%p 계통 편향이 0.005%p로. degenerate 판정 기준(2%p)과
  같은 크기였으므로 Phase 5 전에 반드시 고쳐야 했다.
  F5가 지적한 "방법 바이어스 2.85%p"의 상당 부분이 이것이었다.

Phase 4의 LLI 규약 결론에는 영향 없음 (세 규약이 같은 α·β·r을 공유).

### Phase 4 — 동시 실행 방지 수정 (F19, 2026-08-06 실측 사고)

`run_fit`이 실행 잠금(`.fit.lock`)을 **본체 마지막에** 잡고 있었다.
lock 이전 구간(curves.parquet 로드 → 3,069조건 태스크 구성 →
halfcell이면 p_ini self-fitting)이 수 분~수십 분인데 그동안 무방비였다.

실측 사고 (results/grid_fine_v1):
    PID 330053  04:17:13 시작   ← curves 재생성(04:37:56) **이전**
    PID 333299  04:38:48 시작   ← 재생성 이후 (정상)
    .fit.lock   04:39:15        ← 333299이 잡음. 330053은 검사조차 안 거침

두 프로세스가 같은 `--out`에 붙어 32워커씩 총 64개가 16물리코어를 나눠 써
속도가 반토막 났고, 더 심각하게는 330053이 **옛 프레임(Q=5720) 곡선**으로
fit_chunks에 결과를 쌓고 있었다. 청크 병합은 mtime 최신 우선(`io.py:56`)이라
그대로 두면 정상 결과를 덮어쓴다.

수정:
  - `run_fit`을 얇은 래퍼로 바꿔 **맨 앞에서** lock을 잡고
    `try/finally`로 본체(`_run_fit_locked`)를 감쌌다. 무방비 구간 ≈ 0.
  - resume 시 "완료 표시는 있으나 청크에 행이 없는" 조건을 완료에서 제외한다
    (F19b). 오염 청크를 삭제하면 표시만 남아 그 조건이 영원히 건너뛰어지는데,
    이는 결과가 조용히 비는 가장 위험한 실패 모드다.

물리·수식 변경 없음. 실행 무결성 수정.

### Phase 6 — 전극 격차 복원력 지표 추가 (2026-08-06)

Phase 6 스모크 중 발견: **22p 근방 격자점은 참값 자체가 LAM_PE = LAM_NE** 다.
따라서 "그 근방에서 복원이 잘 됐다"는 22p 결과를 옹호하는 증거가 되지 못한다.
물어야 할 것은 반대 방향이다 — 참값이 뚜렷이 다를 때도 fitting이 둘을 같다고
말하는가.

`tools/compare_objectives.py: gap_analysis()` 추가:
  gap_collapse_frac  참 격차 ≥6%p인데 복원 격차 <2%p로 답한 비율
  shrinkage          복원 격차 / 참 격차의 평균
  false_split_frac   참값은 같은데 다르다고 답한 비율 (반대 방향 오류)

coarse 격자(F15 수정 전) 실측:
    gap_collapse_frac = 2.2%    shrinkage = 0.95
    false_split_frac  = 63%

→ 예상과 반대 방향이다. 이 방법은 서로 다른 전극을 뭉개지 않는다.
  실패는 **없는 격차를 만들어내는** 쪽으로 나타난다.
  단, false_split 판정 기준(2%p)이 F15 편향(~1.6%p)과 같은 크기이므로
  63%의 상당 부분이 그 편향일 수 있다. fine 격자 재fit 결과로 확정할 것.

`tools/make_results.py`: 결론 문장이 **숫자를 따라가도록** 분기 처리.
이전 초안은 붕괴율과 무관하게 "증거가 되지 못한다"를 고정 출력해, 데이터가
반대일 때 거짓 결론을 쓰게 돼 있었다 (테스트로 고정).

### Phase 6 — dQ/dV 목적함수의 계단식 초기값 (F20, 2026-08-06)

fine 격자 결과에서 dQ/dV 항을 넣은 목적함수가 오히려 나빠졌다
(degeneracy 62% → 87%). 결론을 내기 전에 원인을 갈랐다.

**무열화 조건 자체 검사** (정답 전부 0, 노이즈 0, grid 기준이므로
정답 p=(1,0,1,0)·J=0 이 자명한 조건):

    objective          LAM_PE 복원    J(찾은 해)    J(정답)
    pocv               -7.8e-13       5.7e-12       0.0
    pocv_dvdq          -9.4e-14       7.1e-13       0.0
    pocv_dvdq_dqdv     -0.0647        0.402         0.0      ← ★
    dqdv_only          -0.0067        0.0345        0.0

**J(정답)=0 인데 최적화는 J=0.402에서 멈췄다.** 목적함수의 최소는 정답에
정확히 있다 — 못 찾은 것이다. 따라서 "34p 개선안이 나쁘다"가 아니라
**"dQ/dV 항이 들어가면 전역최소의 유인역이 사실상 0폭"** 이 실제 현상이다.

원인은 해상도다. 곡선이 조건당 300점 → dQ/dV 격자점당 5.4 mV인데
피크 FWHM 중앙값이 15.7점(85 mV)이고 savgol 창이 21점이다.
**스무딩 창이 피크보다 넓다.** dQ/dV가 뾰족한 이산 신호가 되어
α가 조금만 움직여도 피크가 격자 칸을 넘으며 J가 불연속으로 튄다.

교차 평가(n=120)도 같은 그림이다. dQ/dV 목적함수는 자기 해(J=0.409)를
pocv_dvdq 해(J=0.417)보다 2%만 낮게 평가하는데, 오차는 0.059 vs 0.024로
2.4배 나쁘다 — 거의 평평한 골짜기에서 최소점이 밀려 있다.

수정: `_fit_one`이 **매끄러운 항으로 먼저 풀고 그 해를 dQ/dV 목적함수의
초기값으로 물려준다** (objectives.yaml 정의 순서를 따름). 임의 튜닝이 아니라
표준적인 다단계 적합이고, dQ/dV의 본래 역할("이미 가까운 해를 피크로 다듬기")과도
맞는다. `--no-warm-start`로 끄고 비교할 수 있으며, 행마다 `warm_started`를
남겨 사후 감사가 가능하다. run_sig에도 포함해 다른 설정의 resume 혼입을 막았다.

물리·수식 변경 없음. 최적화 절차 변경.

### 실행 스크립트 수정 — --out이 조용히 무시되던 버그 (2026-08-06)

`run.sh --mode fit`이 `--in`을 받으면 사용자의 `--out`을 무시하고 `--in`으로
덮어썼다. 스모크 테스트를 별도 디렉터리로 빼려 해도 **본 실행 디렉터리에
쓰이게** 되며, 실제로 30조건 스모크가 5.7시간짜리 결과 디렉터리를 향했다
(다행히 쓰기 전에 중단돼 오염은 없었다).

수정: `--out`을 명시했는지 추적해서, 명시했으면 그대로 쓴다.
추가로 `run_fit`이 시작 시 **입력/출력 디렉터리 절대경로를 로그에 찍는다** —
같은 사고가 나면 첫 줄에서 보이게.

### Phase 5 — multi-start 지표 재정의 (F21, 2026-08-06)

fine 격자 요약에서 나온 두 숫자는 **그대로 인용하면 오독한다**.

    n_restarts=5 → agree_frac 0.0,  median_p_spread 0.0

- `agree_frac`: adaptive 조기 종료 때문에 restart를 5까지 간 조건은 "앞 두 번이
  안 맞아서 계속 간" 조건이다. 따라서 `agree >= n_restarts`는 **정의상 거짓**이며
  0.0은 측정이 아니라 동어반복이다.
- `p_spread = 0`: "해가 일치"가 아니라 **"최적 J에 도달한 restart가 하나뿐"** 이라는
  뜻이다. 오히려 서로 다른 국소최소가 있다는 신호에 가깝다.

`restarts_json`에 restart별 (p, J) 원본을 남겨 뒀으므로(F4 대비) **재계산 없이**
제대로 된 지표를 만들 수 있다. `multistart_diagnostics()`가 두 축을 분리한다.

    unique_min   최적 J에 모든 restart가 모이고 해도 일치      → 문제 없음
    flat_valley  같은 J인데 해가 서로 멀다                     → ★ degeneracy의 직접 증거
    multimodal   J가 다른 국소최소 여럿                        → 최적화 난이도. 초기값으로 해결 (F20)

두 실패 모드를 뭉치면 처방이 정반대가 된다. flat_valley는 데이터를 더 넣어야
하고(측정 방식 변경), multimodal은 초기값만 주면 사라진다.

`summarize()`의 `restart_conditioned` 블록은 하위호환으로 남기되, 인용하지 말라는
경고를 `_F4_주의`에 명시했다.

### Phase 6 — savgol 캐시를 띠 구조로 (F22 후속, 2026-08-06)

조밀 n×n 행렬 캐시가 V100에서 기대만큼 안 나왔다.

    단일 스레드   51.4s → 20.0s   (2.6배)
    V100 32워커   6.6 s/cond → 4.0 s/cond   (1.65배)

원인은 메모리 대역폭이다. 300×300 행렬은 698 KB로 L2에 안 들어가고,
32워커가 동시에 읽으면 대역폭이 병목이 된다. CPU 연산을 메모리 트래픽으로
바꾼 대가다.

그런데 이 연산자는 0이 아닌 원소가 7%뿐인 **띠 행렬**이다 — 내부 행은 창 크기
21개만, 나머지 279개는 0이고 가장자리 2h행만 조밀하다. 게다가 세 조각
(내부 계수 · 상단 블록 · 하단 블록) 모두 **n에 의존하지 않는다**. 가장자리는
언제나 앞뒤 w개 점에 다항식을 맞추기 때문이다.

    저장량   조밀 698 KB → 띠 3.4 KB              (203배)
    캐시 항목  (길이,창,차수) 204종 → (창,차수)별 1개
    단일 스레드  20.0s → 19.1s  (여기선 이미 savgol이 병목이 아님)

단일 스레드 이득은 작지만, 대역폭 경합이 있는 32워커 환경에서 의미가 있다.
정확성은 그대로다 (최대오차 1.3e-13, 신호 스케일 21.8).
`DD_SMOOTH_CACHE=0` 으로 끄고 scipy 경로와 대조할 수 있다.

물리·수식 변경 없음. 성능 최적화.

### Phase 6 — v2 결과 및 해석 (2026-08-06)

warm start(F20) + savgol 캐시(F22) 적용 refit. 3,069조건, 3.9 s/cond, 3시간 17분
(v1은 9.6 s/cond, 8시간+).

**목적함수 비교** (복원가능군 1,476행, v1 → v2):

    objective              degeneracy   보정      평균|err|   PE-NE 상쇄
    pOCV only              78% → 78%   67% → 67%  4.7 → 4.7   29% → 29%
    pOCV+dV/dQ (33p)       62% → 62%   15% → 15%  2.5 → 2.5   68% → 68%
    +dQ/dV (34p)           87% → 63%   95% → 24%  6.6 → 2.4   35% → 48%
    dQ/dV only             90% → 77%   92% → 64%  8.0 → 4.9   22% → 22%

warm start를 안 받는 두 목적함수가 소수점까지 동일 — 대조군이 작동했고
변화는 전부 F20 효과다.

**세 층위가 서로 다른 답을 준다. 이게 이번 결과의 핵심이다.**

  ① 정보 (Hessian, optimizer 무관)
       조건수 중앙값  pOCV+dV/dQ 42,061  →  +dQ/dV 432   (97배 개선)
       flat score          2.4e-5   →  2.3e-3
     → dQ/dV는 역문제의 조건화를 크게 개선한다. 데이터가 조합을 더 잘 구분한다.

  ② 최적화 (multi-start, 무작위 restart만 — F21b)
       flat_valley   4.13% → 0.95%      multimodal  79% → 98%
       unique_min   16.7%  → 1.2%
     → 지형이 극도로 다봉이 되어 optimizer가 그 정보를 회수하지 못한다.

  ③ 최종 오차
       degeneracy 62% vs 63%, 평균|err| 2.5 vs 2.4%p
     → 이득이 결과까지 오지 못했다.

즉 **"34p의 dQ/dV 추가는 옳다. 막힌 곳은 목적함수가 아니라 최적화다."**
F20(계단식 초기값)이 그 첫 수정이었고 87% → 63%를 만들었다. 남은 방향은
곡선 해상도 상향(300 → 1500점)이나 전역 최적화다.

⚠ 유보: `min_eigval_positive_frac`이 +dQ/dV에서 0.835다 — 16.5%는 최적점이
아닌 안장점에서 Hessian을 잰 것이다. 또 eps=1e-4 중심차분이 지형 거칠기를
곡률로 오독할 수 있어 eps 민감도 확인이 필요하다.

### Phase 6 — Hessian 조건수의 eps 의존성 (F23, 2026-08-06)

"dQ/dV가 조건수를 42,061 → 432로 97배 개선한다"는 잠정 결론을 검증하려
eps 민감도를 봤더니 **Hessian이 수렴하지 않았다.**

    pocv_dvdq_dqdv, n=100
      eps=1e-3   조건수     12.8   flat score 7.8e-2
      eps=1e-4   조건수    229     flat score 4.4e-3
      eps=1e-5   조건수 17,381     flat score 5.9e-5

3자리수 넘게 변한다. 목적함수가 여러 스케일에서 울퉁불퉁하면(=dQ/dV의 300점
이산화) 수치 Hessian은 "eps가 훑는 스케일의 유효 곡률"을 잴 뿐이고,
비매끄러운 함수에 조건수는 잘 정의되지도 않는다.

→ **조건수 절대값은 인용하지 않는다.** 같은 eps에서 목적함수끼리의 순서만
  쓴다. 그 순서가 여러 eps에서 유지되는지는 별도 확인이 필요하다.

수정:
  - hessian 결과와 요약에 `eps`를 기록 (어느 스케일인지 사후에 알 수 있게)
  - 요약에 인용 금지 경고를 넣고, RESULTS.md가 그대로 싣는다
  - RESULTS.md는 표에 eps가 섞여 있으면 경고를 띄운다

물리·수식 변경 없음. 해석 규칙 추가.

### 운영 — 계산 결과 백업 경로 (2026-08-07)

`.gitignore`가 `results/`와 `*.parquet`을 통째로 제외해서, fitting 결과가
**서버에만 존재**하는 상태였다. V100 컨테이너가 회수되면 14시간어치 계산이
사라진다.

`artifacts/`를 추적 대상으로 열고 `scripts/archive_results.sh`가 **재생성
비용이 큰 것만** 골라 넣도록 했다.

    남긴다   fits.parquet (조건당 4~10초 × 3,069 = 시간 단위)
             manifest.yaml (어떤 커밋·설정에서 나왔는지)
             *_summary.yaml, objective_comparison.*, figures/*.png
    버린다   curves.parquet (19 MB, 재생성 5~8분)
             degeneracy_map (fits에서 몇 초)
             chunks/, fit_chunks/, completed.jsonl (중간 상태)

fits.parquet만 있으면 score·hessian·report는 전부 몇 초 안에 복원된다.
실측: coarse 실행 하나가 392 KB.

### 운영 — lock 진입점 목록 누락 (F24, 2026-08-07)

`_pid_alive()`가 `src.grid`와 `src.fitting`만 살아 있는 실행으로 인정했다.
가중치 sweep은 `python -m src.weight_sweep`으로 뜨므로 이 검사를 통과하지
못했고, 그 결과 **살아 있는 실행의 lock이 stale로 판정돼 삭제**됐다.
F19에서 lock을 맨 앞으로 옮겨 막았던 동시 실행이 다른 경로로 다시 뚫린 것이다.

실측: 09:29 시작한 sweep(nproc=32) 위에 09:33 진단용 sweep(nproc=4)이
같은 `--out`으로 겹쳐 떴다. 두 실행의 청크가 섞였고, 표본 n=4짜리 결과가
`configs/objectives_optimized.yaml`을 덮어썼다.

수정:
  - `_RUN_ENTRYPOINTS`로 목록을 상수화하고 `src.weight_sweep` 추가
  - `scripts/watch_fit.sh`도 같은 패턴을 보게 수정 (sweep이 돌고 있어도
    "프로세스 없음"으로 오표시하던 문제)
  - 테스트가 `run.sh`의 `python -m src.*` 호출을 파싱해 목록과 대조한다
    — 새 진입점을 만들면 테스트가 먼저 깨진다

교훈: 같은 사실("이 실행이 살아 있는가")을 서로 다른 세 곳(lock 검사,
감시 스크립트, bg.sh 가드)이 각자 판단하고 있었다. 상수 하나로 모았다.

### Phase 6 — Case 1 vs Case 2 ★ 기준 곡선이 목적함수보다 중요하다 (2026-08-07)

같은 fine 격자(3,069조건)에 기준 곡선만 바꿔 fitting했다.

    Case 1  전 범위 half-cell OCV (21p 논문 방식)   --reference halfcell
    Case 2  격자의 무열화 조건 곡선 (유도식 방식)     --reference grid

**복원 가능 조건 수부터 갈린다.**

    Case 1   3,069 / 3,069   복원불가 0%
    Case 2   1,476 / 3,069   복원불가 52%

Case 2는 참값 α=(1−LAM)/r < 1 인 조건에서 재구성 창이 reference 범위를
벗어나 원리적으로 정답이 안 나온다(F1). 전 범위 테이블을 쓰는 Case 1에는
그 벽이 아예 없다. **격자의 절반이 되살아난다.**

목적함수별 (왼쪽 Case 1 / 오른쪽 Case 2):

    objective          degeneracy    바이어스보정    평균|err|     unique min
    pOCV only          100% /  78%    57% / 67%     8.5 / 4.7%p    88% / 11%
    pOCV+dV/dQ (33p)    37% /  62%    32% / 15%     2.4 / 2.5%p    64% / 39%
    +dQ/dV (34p)        98% /  63%    16% / 24%     4.3 / 2.4%p    22% /  3%
    dQ/dV only         100% /  77%    37% / 64%     6.9 / 4.9%p     8% /  5%

**33p 목적함수(pOCV+dV/dQ) 기준으로 degeneracy가 62% → 37%.**
그리고 방법 바이어스가 사실상 사라진다:

    Case 1 pocv_dvdq 바이어스   LLI −0.0004  LAM_PE +0.0003  LAM_NE +0.0029

0.03%p 수준이다. Case 2에서 F15 수정 후에도 남아 있던 편향이 기준을 바꾸니
없어졌다. `unique_min`도 39% → 64%로, 최적화 문제 자체가 훨씬 순해진다.

→ **목적함수를 바꾸는 것보다 기준 곡선을 바꾸는 편이 효과가 크다.**
  21p 논문의 전 범위 half-cell 기준이 옳았다는 뜻이기도 하다.

⚠ 단, Case 1에서 dQ/dV 계열은 오히려 나쁘다(98%, 100%). Case 2와 반대
방향이므로 기준×목적함수 상호작용이 있다. 원인은 아직 규명하지 않았다.

### Phase 6 — 발표 전 리뷰 반영 (2026-08-07)

독립 리뷰에서 나온 지적 5건. **두 건은 이미 보고한 내용을 뒤집었다.**

**① `gap_collapse`가 임계값으로 사실상 결정된다** (핵심 결론이었음)
붕괴로 세려면 격차를 6%p에서 2%p 아래로 끌어내려야 하므로 **최소 4%p의 격차
오차**가 필요하다. 실측 격차 오차는 중앙값 2.6%p, 99분위 5.7%p다. 즉 붕괴율
0.8%는 측정이 아니라 "오차 스케일 < 임계 간격"의 재진술에 가깝다.
→ `collapse_requires_gap_err` / `gap_err_median` / `gap_err_p99` /
  `collapse_measurable`을 함께 산출하고, 관측 불가 설정이면 결론에 경고를 붙인다.

**② halfcell의 "복원불가 0%"는 측정이 아니다**
`scoring.py:85-90`이 `reference != "grid"`면 `recoverable=True`로 **고정**한다.
전 범위 테이블이라 창 부족이 없다는 물리적 근거는 있으나 실측이 아니다.
→ `tools/compare_cases.py` 신설: 두 실행의 **공통 조건 중 grid 기준에서
  복원가능한 것**으로 행 수를 맞춰 비교한다. 그렇게 재도 결론은 강해진다.

    공통 1,476조건        Case 1 (halfcell) / Case 2 (grid)
    pOCV+dV/dQ            degeneracy   7% /  62%     평균|err| 1.4 / 2.5%p
    +dQ/dV                            99% /  63%              3.9 / 2.4%p
      └ 바이어스 보정 후   6% /  24%   ← 오차가 거의 일정한 **오프셋**이다

  즉 halfcell에서 dQ/dV의 실패는 degeneracy가 아니라 **캘리브레이션 편향**이다
  (`to_modes_halfcell`이 기준 조건 self-fit의 `p_ini`로 정규화한다).

**③ 조건수 순서가 실제 복원 성능과 역상관이다**
`dqdv_only`가 조건수 99(최고)인데 평균|err| 4.9%p(최악), `pocv_dvdq`는
조건수 42,061(최악)인데 오차는 절반이다. 지형이 거칠면 곡률이 크게 잡히므로
낮은 조건수가 "잘 정의된 최적점"이 아닐 수 있다.
→ **"dQ/dV가 정보를 더한다"의 단독 근거로 조건수를 쓰지 않는다.** 보고서가
  상관계수를 직접 계산해 역상관이면 경고를 띄운다. `min_eigval_positive`
  열도 추가(+dQ/dV는 16.5%가 안장점에서 잰 값이다).
  RESULTS.md에 하드코딩돼 있던 eps 스폿체크 수치도 제거(본문 표와 모순이었다).

**④ 22p·격차 표가 `noise=0` 전용인데 표기가 없었다** — 같은 문서가 "노이즈 0만
인용하면 과대평가"라고 경고하는 것과 충돌. 표 제목에 명기.

**⑤ 22p 답을 우도비로 정리** — 22p의 참 격차는 1%p라 `false_split` 군이다.

    P(같다고 답 | 참값 같음)          = 1 − false_split
    P(같다고 답 | 참값 6%p 이상 차이) = gap_collapse
    → 우도비

  `pe_ne_coupled ≈ 0%`(평평한 방향이 PE-NE 결합이 **아님**)도 표에서 결론으로
  올렸다. 22p 가설에 대한 직접적인 음성 결과인데 묻혀 있었다.

### Phase 6 — 가중치 sweep의 warm start 불공정 (F20b, 2026-08-07)

첫 sweep 결과에서 `w_dqdv=0`만 유독 나빴다.

    w_dqdv    0.00   0.25   0.50   0.75   1.00   1.25   1.50   2.00
    보정후    0.86   0.26   0.26   0.26   0.27   0.38   0.41   0.41

그런데 이건 dQ/dV 효과가 아니다. warm start 규칙이 "w_dqdv≠0이면 초기값을
받는다"라서, **w=0 하나만 seed 제공자가 되어 자기는 초기값을 못 받았다.**
F21b에서 multi-start 지표에 대해 잡았던 것과 같은 confound가 sweep 설계에
그대로 남아 있었다.

수정:
  - 목적함수 정의에 `_warm` 플래그를 두어 warm start 여부를 명시할 수 있게 함
  - `build_weight_objectives`가 맨 앞에 숨은 `_seed`(w_dqdv=0, _warm=False)를 두고,
    **보고 대상 w는 전부 `_warm=True`** 로 같은 seed를 받게 함
  - `_seed` 행은 집계에서 제외

w=0.25~2.00 끼리는 원래도 공정했고, 그 구간의 결론은 유효하다:
**w>1.25가 뚜렷이 나쁘다(0.26 → 0.41). 34p 기본값 w=1.0이 상한 근처다.**
그리고 `noise_levels_agree: false` — 노이즈별 최적이 1.0/0.25/0.75로 갈리므로
단일 값 채택 근거는 약하다 (F10).

### Phase 6 — 가중치 sweep의 비교 공정성 (F20c, 2026-08-07)

sweep을 두 번 다시 돌리고 나서야 원인이 잡혔다. 기록해 둔다.

**증상**: `w_dqdv=0`만 degeneracy 86%, 나머지 22~33%.

**1차 진단(틀림)**: "w=0이 warm start의 seed 제공자라 자기는 초기값을 못 받는다"
→ 숨은 `_seed` 목적함수를 앞에 두고 모두에게 물려주도록 수정.
**결과가 한 자리도 안 바뀌었다.** seed의 목적함수가 w=0의 것과 **동일**하므로
w=0은 자기 최적해를 자기 초기값으로 받은 셈이었다. 이득이 0이다.

**2차 진단(맞음)**: 두 가지가 겹쳐 있었다.

  ① warm start는 **지형이 거친 목적함수에만** 이득이다. w>0은 다른 목적함수의
     해를 받아 실질적 도움을 받지만 w=0은 받을 게 없다. seed를 어떻게 주더라도
     이 비대칭은 안 없어진다.
  ② **restart 2는 부족하다.** 같은 목적함수(w_dqdv=0)를 같은 237조건에서 비교:

         본 실행(restart 5)   degenerate 58% / 보정 17%   평균|err| 0.025
         sweep (restart 2)    degenerate 77% / 보정 92%   평균|err| 0.051

     `pocv_dvdq`는 unique_min이 39%뿐이라 restart가 여러 번 필요한 목적함수다.

**수정**: sweep은 `warm_start=False`로 돌리고 `n_restarts` 기본값을 5로 되돌린다.
모든 w를 같은 출발선에 세우는 것이 유일하게 공정한 설계다. 비용은 층화 표본으로만
아낀다 (468조건 × 9가중치 × 5restart ≈ 75분).

구버전 산출물은 `weight_sweep.yaml`의 `warm_start` 필드로 판별되며,
`make_results`가 "w=0 행을 인용하지 말 것" 경고를 자동으로 붙인다.

### F20d — 가중치 sweep의 warm start를 본 실행과 맞춤 (2026-08-07)

**증상**: restart 5로 재실행한 sweep에서 최적 w가 `0.5 → 0.0`으로 뒤집히고,
`w=1.0`의 보정 degeneracy가 90.3%로 나왔다. 그런데 같은 문서의 목적함수
비교표에서는 정의가 동일한 `pocv_dvdq_dqdv`가 24%다.

**진단** (`tools/check_sweep_consistency.py`, 계산 없이 parquet만 비교):

```
공통 468조건            sweep    본 실행
w=0 J중앙값             0.1440   0.1440    ← 소수점까지 일치 (대조군)
w=0 degeneracy          58.23%   58.23%
w=1 J중앙값             0.4060   0.3261    ← sweep이 더 나쁨
w=1 평균|err|           6.17%p   2.48%p
w=1에서 sweep의 J가 더 큰 조건 비율: 51.7% (반대는 2.1%)
```

`w=0 ≡ pocv_dvdq`, `w=1 ≡ pocv_dvdq_dqdv`로 가중치 정의가 글자 그대로 같으므로
결과도 같아야 한다. w=0만 일치하고 w=1이 계통적으로 나쁜 것은 **sweep이 warm
start를 끈 채 돌아 dQ/dV 항을 못 푼 것**이다 (F20에서 확인한 현상).

**원인**: F20c에서 "모두 같은 출발선에 세우는 것이 공정하다"고 보고
`warm_start=False`로 고정했다. 공정의 기준을 잘못 잡았다 — 모두에게 똑같이 주는
것이 아니라 **본 실행이 쓰는 설정 그대로** 재야 같은 문서 안에서 말이 맞는다.
w=0은 본 실행에서도 seed 제공자라 warm start를 안 받으므로, 켜면 두 실행의 구조가
정확히 일치한다 (위 표에서 w=0이 소수점까지 같은 것이 그 증거).

F20c 주석의 *"숨은 seed로 물려줬는데 결과가 한 자리도 안 바뀌었다"* 는 틀린
관찰이었다. 당시 `n_restarts=2`라 warm start를 줘도 어차피 못 풀던 상태였다.

**조치**
- `run_weight_sweep(warm_start=True)` 기본값. `--no-warm-start`는 진단용으로만 남김
- `build_weight_objectives`: w_grid에 0.0이 있으면 그것이 seed 제공자(맨 앞).
  없을 때만 숨은 `_seed`를 끼운다
- `weight_sweep.yaml`이 설정 이탈 시 `_경고`를 스스로 기록하고,
  `make_results.py`가 그 경고를 RESULTS.md에 그대로 싣는다
- `tools/check_sweep_consistency.py` 신설 — 계산 없이 본 실행과 대조
- 테스트 3건: 기본값 고정 / seed 제공자 위치 / 경고 분기

**부수 확인**: 본 실행에서 dQ/dV 계열만 warm start를 받는데도 `pocv_dvdq`(62%)를
못 이겼다(63%). **유리한 조건을 주고도 비긴 것**이므로 "dQ/dV가 오차를 못 줄인다"는
결론은 보수적이다. `make_results.py`가 `warm_started` 열을 실측해 이 문장을
결론에 자동으로 붙인다.

## 적대적 교차리뷰 대응 (2026-08-07, 기준 커밋 1790a9cc)

외부 리뷰가 제기한 15건 중 코드·데이터로 검증 가능한 9건을 전부 재계산했고,
**하나도 반박되지 않았다.** 아래는 그 조치다. 상세는 `docs/08_REVIEW_RESPONSE.md`.

### F25 — restart 출처 소실로 multi-start 진단이 무효였다

`fit()`이 `restarts`를 **J 오름차순으로 정렬해** 저장하는데, `multistart_diagnostics`의
`skip_first=True`는 "첫 항목 = warm start"로 보고 그걸 버렸다. 실제로는
**best restart를 버리고 있었다.** `degeneracy_summary.yaml`의
`multistart_random_only` 블록 전체가 무효다.

- restart마다 `{"p", "J", "i", "warm"}`을 저장 (`fit(warm_init=...)`)
- `skip_first`는 이제 **flag로** 거른다. 출처가 없는 옛 형식은 보정을 **생략하고
  경고**한다 — 위치로 추정하면 조용히 틀린 값이 나오므로
- 요약에 `warm_start_보정_적용` 필드를 넣어, 무효인 블록을 모르고 인용하지 못하게 함
- **기존 artifact로는 복구 불가.** 재fit이 필요하다

### F26 — half-cell `p_ini`를 목적함수 하나로 전부 덮어썼다

pristine 조건을 `pocv_dvdq`로 **한 번만** fit해 모든 목적함수에 주입했다.
목적함수마다 pristine optimum이 다르므로 나머지는 남의 원점에서 좌표를 읽은 셈이다.

목적함수별 pristine fit (artifacts/halfcell_v1 실측):

| objective | α_PE | β_PE | α_NE | β_NE |
|---|---|---|---|---|
| pocv | 1.51409 | −0.41920 | 1.12157 | −0.11930 |
| pocv_dvdq | 1.47598 | −0.40844 | 1.06166 | −0.05826 |
| pocv_dvdq_dqdv | 1.51873 | −0.42200 | 1.06265 | −0.05949 |
| dqdv_only | 1.48489 | −0.41018 | 1.05073 | −0.05073 |

목적함수별 원점으로 다시 변환하면 (공통 1,476조건):

| objective | 공통 p_ini | 목적함수별 p_ini |
|---|---|---|
| pOCV only | 99.5% | **59.5%** |
| 33p | 6.6% | 6.6% (원점 제공자라 불변) |
| 34p | 99.1% | **10.0%** (평균\|err\| 3.94 → 1.43%p) |
| dQ/dV only | 99.9% | 99.8% |

**미해결로 남겨뒀던 Case 1의 LAM_PE −4.1%p 오프셋이 이것이었다** (−3.83 → −1.09%p).
`docs/RESULTS.md`의 halfcell 100%/99% 표와 "reference 효과가 모든 목적함수에 공통"이라는
일반화는 철회한다. 33p의 7% vs 62%는 33p가 원점 제공자여서 그대로 유지된다.

### F27 — `recoverable` 판정이 행별이 아니라 프레임 전체였다

`(out["reference"] != "grid").any()` — halfcell 행이 하나만 섞여도 grid 행까지
전부 복원가능이 됐다. 비교표의 분모가 소리 없이 늘어나는 실패다. 행별
`np.where`로 바꾸고, halfcell의 `True`가 측정이 아니라 가정임을
`recoverable_measured` 열로 남긴다.

### F28 — 우도비 46:1은 임계가 만든 국소 봉우리다

계산 방향(분자·분모)은 뒤집히지 않았다. 재계산으로 `46.25`가 그대로 나온다.
문제는 그 값이 **특정 임계 조합에서만** 나온다는 것이다 (복원가능군, noise=0, 33p):

```
참 격차 cutoff  ≥2%p → 2.3   ≥4%p → 4.5   ≥6%p → 46.4
복원 동일 임계  <1%p → 22.3  <2%p → 46.4  <3%p → 15.2  <4%p → 9.2
전체 격자에서는 3.69
```

- `gap_sensitivity()` 신설 — 임계 2차원 표를 항상 함께 낸다
- `gap_analysis`가 `lr_sensitivity_min/max/median`과 `lr_is_local_spike`를 자기 dict에 넣어,
  떼어 인용하지 못하게 한다
- `n_zero_gap_true` → `n_small_gap_true` (조건은 "<tol"이지 "정확히 0"이 아니었다).
  정확히 0인 수는 `n_exact_zero_gap_true`로 따로
- **결론 문구 철회**: "22p는 degeneracy가 아니라 실제로 비슷하게 열화했다는 증거" →
  "이 합성 격자의 복원가능군에서, 참 격차가 뚜렷한 조건이 '같다'로 붕괴하는 일은
  드물었다". posterior가 아님·부분집단 조건화·임계 의존 세 제약을 결론에 상시 부착

### F29 — 복원가능군 조건화가 결론 2의 방향을 바꾼다

| objective | 전체 격자 | 복원가능군 | 복원불가군 |
|---|---|---|---|
| 33p | 74.1% | 61.9% | 85.3% |
| 34p | 71.9% | 63.3% | 80.0% |

복원가능군에서는 33p가 1.4%p 낫고 **전체 격자에서는 34p가 2.2%p 낫다.**
`comparison_table(recoverable_only=False)`를 추가해 전체군 표를 항상 병기하고,
`population_sensitivity.direction_flips`로 뒤집힘을 스스로 판정해 경고한다.

또한 `pe_ne_antisym`(68→48%)은 raw 오차의 **부호**만 세므로 목적함수별 전역 편향의
부호차를 그대로 상쇄로 잡는다. 중심화하면 **33.1% → 42.9%로 방향이 뒤집힌다**
(33p 오차상관 +0.754, 34p −0.287). "34p가 상쇄를 줄였다"는 인과 해석을 철회하고,
그 경고를 결론에 붙였다.

### F30 — artifact provenance가 없었다

`grid_fine_v2`·`halfcell_v1` 둘 다 `config_hash: ''` + `git_dirty: true`였고
dirty patch가 없다. parquet은 재집계할 수 있어도 그 숫자를 만든 코드가 남아 있지 않다.

- `base_manifest(cfg_hash, out_dir=, inputs=)` — dirty diff를 `run_dirty.patch`로 저장,
  입력 파일 SHA-256 기록, `reproducible` 플래그와 `_주의` 자동 부착
- fitting은 실제 `obj_cfg` 내용을 해시해 `config_hash`에 넣는다 (빈 문자열이 아니라)
- `git_commit`을 full SHA로

### 유지되는 결론

`pocv_dvdq`의 halfcell 6.6% vs grid 61.9%(McNemar p≈1e-202)는 목적함수별 `p_ini`로
바꿔도 한 자리도 안 변한다. 다만 case 변경에는 좌표 원점·정규화·bounds·`p_ini`가
함께 들어가므로 **"곡선 범위 때문"이 아니라 "reference 생성 pipeline 때문"** 으로
좁혀 적는다. 단일 원인 귀속은 ablation 없이 성립하지 않는다.

### F26b — pristine 원점도 본 fitting과 같은 warm start 연쇄에서 (2026-08-07)

F26을 적용한 첫 실행 로그에서 잡았다. 목적함수별 pristine을 **하나씩 따로**
fit했더니 warm start 연쇄가 끊겨, `dqdv_only`만 다른 국소최소에 앉았다.

```
                단독 fit(F26 초판)                 연쇄 fit(본 fitting과 동일)
dqdv_only       1.5708, -0.4442, 1.0204, -0.0184   1.4849, -0.4102, 1.0507, -0.0507
```

`halfcell_v1`의 pristine 행을 보면 `pocv_dvdq_dqdv`와 `dqdv_only`가
`warm_started=True`다. 즉 본 fitting은 연쇄 쪽 값을 쓰는데 원점만 단독 값이
되어, **원점과 데이터 점이 서로 다른 optimizer 프로토콜에서 측정**된다.
F26이 지우려던 계통 오프셋이 그대로 다시 생긴다.

조치: `_fit_one`에 목적함수 dict 전체를 한 번에 넘기고 결과 행에서 목적함수별
`p_ini`를 뽑는다. 비용도 4번 → 1번으로 준다. 테스트로 "쪼개면 실패"를 고정.

## 2차 교차리뷰 대응 (2026-08-07, F31~F35)

1차 회답에 대한 재리뷰의 차단 항목 5건. 전부 타당했고 모두 조치했다.

- **F31** restart 출처를 `warm`/`base_init`/`random` 3종으로 기록. "warm만 제거"로는
  random-only가 성립하지 않는다 — warm을 받은 목적함수만 restart 0이 빠지고,
  나머지는 공통 결정론적 초기값(base_init)이 남아 비교 집합의 성격이 달라진다.
  `n_nonrandom_dropped`(실제 제거 수)와 목적함수 간 restart 수 편차 기반
  `비교가능` 플래그 추가.
- **F32** 실행 서명에 결과를 바꾸는 모든 설정을 포함(가중치·수치 bounds·n_restarts·
  dqdv/scaling·base config·curves SHA). 행마다 `run_sig`를 박고 병합 시 서명이
  둘 이상이면 실패시킨다. 예전에는 목적함수 *이름*만 들어가 같은 이름으로 가중치만
  바꾸고 --resume하면 옛 청크가 조용히 재사용됐다.
- **F33** 철회한 Hessian 해석을 생성기에서 제거. 핵심 결론에서 `pe_ne_coupled` 삭제,
  절 제목을 "참고용, 결론 근거 아님"으로 강등, "최적화와 무관" 표현 삭제.
  "실제 degeneracy의 하한"과 "degeneracy 특징적 지문"도 삭제 — 전자는 단조성이
  증명되지 않았고 후자는 이미 인과 해석을 철회한 지표다.
- **F34** `gap_sensitivity`가 `lt_tol`/`exact_zero` 두 정의를 모두 계산.
  `lr_is_local_spike`를 전체 중앙값이 아니라 **이웃 한 칸** 중앙값과 비교
  (이름이 local인데 구현이 global outlier였다). `∞` 개수 별도 표기, 각 칸에 분자/분모 병기.
- **F35** provenance가 불충분하면 `RESULTS.md` 맨 위에 인용 금지 배너를 자동 삽입.
  갖춰지면 사라지도록 양방향 테스트로 고정.

테스트 174 → 182. 실행 경로를 실제로 태우는 통합 테스트 2건 추가
(합성 curves.parquet으로 `run_fit`을 돌려 서명이 설정 변화에 반응하는지 확인).
