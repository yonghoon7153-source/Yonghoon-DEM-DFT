# mode-observability — 관측을 늘리면 열화 모드가 갈리는가

`degradation-degeneracy` 의 다음 질문을 다루는 satellite 프로젝트.

- 그쪽 질문: full-cell OCV **하나**로 LLI/LAM_PE/LAM_NE 를 가를 수 있는가
  (답의 조건까지 나옴 — 19라운드 게이트 리뷰 + 본 실행 완료).
- **이쪽 질문: 관측을 늘리면 갈리는가.** 2026-09-02 BML 세미나(김시원)가 제안한
  physics-inspired feature 2종(PVS·SEV)이 구체적 후보다. 두 feature 의 모드별
  부호 패턴이 동일하다는 관측({LLI, LAM_PE} ↑ vs {LAM_NE} ↓)이 출발점이다 —
  근거와 반론은 `wiki/questions/pvs-sev-lli-lampe-separability.md`.

## Phases

| # | 내용 | 필요한 것 | 상태 |
|---|---|---|---|
| 1 | **PVS Jacobian** — 합성 truth 격자의 곡선에서 PVS 를 계산하고, 모드 파라미터에 대한 Jacobian 특이값으로 국소 식별 가능성을 판정 | degradation-degeneracy 의 기존 dQ/dV 경로 재사용 (읽기 전용) | ○ `phase1_pvs_jacobian.py` · `docs/PHASE1_NOTES.md` |
| 1b | **연속 추적 PVS** — Phase 1 의 비단조가 물리가 아니라 창내 극값 갈아타기였다 | 위와 같음 | ○ `phase1b_tracked_pvs.py` · `docs/PHASE1B_NOTES.md` |
| **1c** | **Lin 의 해석적 null 방향을 우리 좌표에서 수치 검증** — `JᵀJ` 최소 고유벡터가 `(1,1,1)/√3` 과 **12.04°** 안에서 일치. 조건수는 18.2 뿐이라 **구조적 축퇴가 아니라 잡음 제한 축퇴**다 | 위와 같음 | ○ `phase1c_null_direction.py` · **`docs/PHASE1C_NOTES.md`** |
| **1d** | **점검 B1 — 우리 4-파라미터 창 모델의 유효 자유도.** σ3/σ1 ≈ 0.05 · σ4/σ1 ≈ 0.03 이고 스텝에 안정. **rank 는 4 이고 2 가 아니다** — Lin 의 redundancy 지적은 틀린 게 아니라 **크기가 과장**된 것으로 읽힌다 | 위와 같음 (정방향이 보간뿐이라 ~5초) | ○ `phase1d_window_dof.py` · **`docs/PHASE1D_NOTES.md`** |
| **1e** | **컷오프 등식 제약을 창 좌표에서 재다** — 제약 gradient 가 **강한** 특이쌍과 **1.5°·2.0°**. 즉 그 제약은 여분이 아니라 **정보를 지운다** (접공간 잔여 감도가 원래 σ1·σ2 의 0.13~0.49 배) | 위와 같음 | ○ `phase1e_cutoff_constraint.py` · **`docs/PHASE1E_NOTES.md`** |
| 1f | **Birkl 식 (7)–(12) 를 우리 좌표로** — Phase 1e 의 한계 ②("제약이 대리물") 를 **철회**했다 (식 11·12 는 글자 그대로 `U_full(EoC)=E_high`). 그러나 Table 5 모델로 식 (12) 를 pristine 에서 풀면 **근이 없다** — 두 `x` 정규화 사이 환산이 인쇄돼 있지 않다 | Birkl ref [33] | ◐ **미완 (일부러 실패한 채 남김)** · `phase1f_birkl_exact.py` · `docs/PHASE1F_NOTES.md` |
| **1g** | **무전류 OCV 로 Phase 1c 재계산** — A(시뮬) → B(순수 창 대수) 가 `12.04° → 10.56°`, **Δ −1.48°**. 모드→곡선 경로에 동역학이 없는데도 null 이 그 자리다 → **12° 는 동역학 산물이 아니다.** C 판(평형 OCP)은 좌표계가 바뀌어 **기각** | 봉인 half-cell 캐시 (fail-closed) | ○ `phase1g_zero_current.py` · **`docs/PHASE1G_NOTES.md`** |
| **1h** | **Mohtat 의 컷오프 등식을 모드 좌표에서, 참값으로** — 두 등식이 pristine 에서 `(1,1,1)` 과 **83.95°·83.59°** (Lin 의 예언 90° 근처), 끝점을 관측에 얹어도 σ_min **+3~6 %**. 그리고 **22p 에서 `u_min` 이 Lin 방향과 4.61°** — Phase 1c 한계 (a) 를 닫는다. 부수: **12.04° 는 점이 아니라 4.6°~21.9° 의 띠** | PyBaMM 구현본 (`_ElectrodeSOH`) · 원전 PDF 미확보 | ○ `phase1h_mohtat_cutoff.py` · **`docs/PHASE1H_NOTES.md`** |
| **1i** | **22p 삼중항의 오차막대 — 그리고 세 막대가 하나라는 것.** σ = 5 mV 에서 `LLI ± 0.44 · LAM_PE ± 0.40 · LAM_NE ± 0.50 %p`. **그런데 총 분산의 94.6 % 가 한 축**(`(1,1,1)` 과 4.61°)에 있어 셋을 따로 인용하면 안 된다. 그리고 **제약 처방의 대가를 수로** 냈다 — 정밀도 −88 %, 편향 **+8.9 %p**(최대 σ 의 173배) | Phase 1c/1h 의 `J` (새 시뮬 불필요) | ○ `phase1i_mode_error_bars.py` · **`docs/PHASE1I_NOTES.md`** |
| **1j** | **두 `x` 정규화를 잇는 환산을 세우고 1g 의 C 판을 다시 지었다.** 셀의 창이 봉인 캐시 양 끝에 이미 있었다 — **PE 는 전극의 65.61 %, NE 는 96.70 %**. 재구성 오차 **475 → 54 mV**, 남는 18.7 mV 는 288점 **전부 한쪽 부호**(과전압). 무전류 판 D 의 각이 **12.54°** → **"12° 는 전류와 무관"** 으로 문장이 올라갔다 (1g 경계 ① 철회) | 봉인 완방·평형 OCP 캐시 (fail-closed) | ○ `phase1j_normalization_bridge.py` · **`docs/PHASE1J_NOTES.md`** |
| **1k** | **축퇴가 어느 층인가 — 그리고 그 층은 우리 것이 아니다.** 창 대수 판을 `J = W·M` 으로 쪼개니 **cond(M) = 2337 대 cond(W) = 31.5** — 축퇴는 **모드→창** 층이다. 그런데 그 `M`(`modes_to_params`)은 `src/fitting.py` 가 **"진단용·'paper' 규약"** 이라 못 박은 것이고 **production 에는 그 층이 아예 없다**. 반사실로 **PE 창 비대칭 가설은 기각**(창을 1.4배 넓혀도 각이 0.05° 안). 부수: 각의 띠가 **1.2°~21.9°** 로 넓어짐 | Phase 1j 의 환산 (새 시뮬 불필요) | ○ `phase1k_tilt_decomposition.py` · **`docs/PHASE1K_NOTES.md`** |
| **1l** | **팽창(부피) 축은 통한다 — 이 계보에서 유일하게 안 기각된 처방.** 전극 팽창 파라미터가 파라미터셋에 없어 교정은 못 하지만, 팽창이 **화학량론의 선형범함수**라는 구조만으로 **모형 족 전체**를 판정했다. **순수 NE 팽창이 `(1,1,1)` 과 70.53°** — 전압(4.61°)이 못 보는 방향을 **본다**. σ_min **+103.7 %** (컷오프 등식은 +3~6 %). 이유: 전압은 음극의 움직임을 양극으로 **상쇄**해 못 보고, 팽창은 음극만 크게 반영해 그 상쇄를 깬다 | 봉인 OCP 표 + 격자 `v_pe`·`v_ne` (새 시뮬 불필요) | ○ `phase1l_expansion_axis.py` · **`docs/PHASE1L_NOTES.md`** |
| 2 | **SEV 시뮬레이션** — PyBaMM P2D 로 0.2C 전류 차단 프로토콜을 돌려 ΔV(1 s)·SEV 를 합성하고, (PVS, SEV) 2×3 Jacobian 으로 "부호는 같아도 감도 비가 다른가"(H2)를 판정 | 동역학 파라미터 세트 (열역학만으로는 안 됨) | 미착수 — **2026-09-03 실측 대조 층의 제약 확정** (아래) |
| 3 | **ML 라벨 degeneracy 전파** — fitted 라벨로 학습한 모드 예측 ML 이 라벨의 비식별성을 어떻게 물려받는지, 정답을 아는 합성 데이터로 정량화. 프로토콜 식별자 입력의 기여 분리 (permutation/SHAP) | Phase 1–2 의 feature + RF/GBM (sklearn) | 미착수 |

Phase 1·2 는 **본 실행 없이** 판정 가능하도록 설계한다 (Jacobian 은 국소 분석).
전역 degeneracy 는 degradation-degeneracy 의 격자 방법론을 그대로 가져온다.

## Phases (원전 흡수에서 나온 것)

2026-09-03 에 원전([[birkl-ocv-degradation-diagnostic]], Birkl et al. 2017 —
`wiki/raw/papers/birkl2017_degradation-diagnostics-ocv.md`)을 해체분석한 결과
**우리가 재고 있는 절차가 원전과 자유도부터 다르다**는 것이 확인됐다. 그
차이가 곧 값싼 실험 3건이다.

| # | 실험 | 왜 | 비용 |
|---|---|---|---|
| 4 | **컷오프 제약 실험** | 원전은 자유 파라미터 **3개**이고 stoichiometric offset 2자유도를 고정 컷오프(4.2/2.7 V) **등식으로 소거**한다. 우리 창 모델은 `p = [α_PE, β_PE, α_NE, β_NE]` **4개**이고 그 제약이 없다 (`src/fitting.py:60`). 우리가 본 degeneracy 의 일부가 **원전에 없는 자유도**에서 올 수 있다 | 기존 곡선 재사용, 본 실행 불요 |
| 5 | **기울기 마스크 on/off** | 원전은 `\|ΔE/ΔSoC\| < 0.1` 구간만 목적함수에 넣는다 — 즉 **모드를 가장 잘 가르는 급경사(EoD) 구간을 버린다.** 임계 0.1 의 근거도 민감도 분석도 원문에 없다. paired 비교로 "정보 많은 구간을 버리는 대가" 를 직접 잰다 | 기존 곡선 재사용 |
| 6 | **li/de 축퇴 재현** | 원전이 스스로 진술한 축퇴("LLI + LAM_NE,de 조합이 같은 양의 LAM_NE,li 와 **같은 OCV 시그니처**를 낸다")를 우리 합성 truth 에서 재현한다. 우리 격자는 `de` 만 돌렸으므로 `li` 를 새로 시뮬레이션해야 한다 — Phase 1b 가 발견한 **LAM_PE 부호 불일치**의 유력 원인이기도 하다 | PyBaMM 소규모 스윕 필요 |

**Phase 4·5 는 원전이 안 한 비교**다. Phase 6 은 원전이 말로만 한 것을
수치로 확인하는 것이고, 동시에 세미나 p.8 과 우리 Phase 1b 의 LAM_PE 부호
불일치를 설명할 후보다.

## Phase 2 의 실측 대조 층 — 원전 확인으로 확정된 제약 (2026-09-03)

Phase 2 가 대조에 쓰려던 EIS 데이터의 **원전**을 흡수했다
(Zhang et al., *Nat. Commun.* **11**:1706 (2020), DOI 10.1038/s41467-020-15235-7;
digest `wiki/raw/papers/zhang2020_eis-gpr-capacity-rul.md`, 좌표계는
`wiki/concepts/zhang2020-eis-aging-dataset.md`, 매니페스트 판정은
`manifests/README.md`). 설계에 직접 걸리는 것 넷:

1. **평형 SOC 는 2점뿐이다.** `state I~IX` 중 **II·III·VI·VII 은 DC 전류가
   흐르는 중에** 측정된다 (SI Fig. 1 의 적·녹 점). 전류 없이 잰 SOC 는
   **0 %(I·VIII·IX)** 와 **100 %(IV·V)** 뿐이므로, SEV 의 실측 대응물은
   "SOC 곡선" 이 아니라 **양 끝점 대비**다. 합성 쪽도 비교 지점을 이 두 곳에
   맞춘다.
2. **state VI 는 쓰지 않는다.** 원전의 per-state 용량 추정 R² 가
   V 0.88 · VII 0.86 · IX 0.81 · VIII 0.68 · II 0.66 · I 0.61 · IV 0.60 ·
   III 0.53 · **VI 0.28** 이다 (SI Fig. 2).
3. **모드 라벨은 없다 (원전에서 확정).** `LLI`·`LAM`·`half-cell` 이 원전
   본문·SI 에 각 0회. → Phase 2 는 "SEV 가 모드를 가르는가" 가 아니라
   **"SEV 축이 셀 간에 재현되는가"** 만 묻는다. 무대는 **동일 조건 8셀**
   (25C01–08)이고, 그 8셀의 EoL 이 **12~234 사이클로 20배** 흩어지므로 가혹한
   시험대다.
4. **`state IV vs V`, `VIII vs IX` 라는 미개척 축**이 있다 — 같은 SOC 에서
   **휴지 15분 전/후**. SOC 가 아니라 완화 시간만 다른 대비이며 원전도 Su 도
   쓰지 않았다.

## 경계 (하드 룰)

1. **RUN_SCOPE 불가침**: `degradation-degeneracy/` 의 `src/ tools/ configs/
   scripts/ run.sh requirements*.txt` 를 import 는 해도 **수정은 절대 하지
   않는다** — 게이트 리뷰 code identity 가 움직인다. 이 프로젝트의 코드는 전부
   이 폴더 안에.
2. 수치의 정본 규칙은 mothership 과 같다: 결과는 이 폴더의 artifact + docs 가
   정본, 위키에는 참조만.
3. push 는 루트 `CLAUDE.md` 하드룰 1의 브랜치로만.

## 관련 자료

- 세미나 해체분석: `wiki/raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md`
- 크롭 그림: `wiki/raw/figures/2026-09-02-siwon-kim-degradation-mode-ml-seminar/`
- feature 정의: `wiki/concepts/pvs-sev-degradation-mode-features.md`
- 질문 카드(이 프로젝트가 feedsInto 대상): `wiki/questions/pvs-sev-lli-lampe-separability.md`
