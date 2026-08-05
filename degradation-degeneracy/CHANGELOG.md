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
