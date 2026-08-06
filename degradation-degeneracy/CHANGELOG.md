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
