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
| 1 | **PVS Jacobian** — 합성 truth 격자의 곡선에서 PVS 를 계산하고, 모드 파라미터에 대한 Jacobian 특이값으로 국소 식별 가능성을 판정 | degradation-degeneracy 의 기존 dQ/dV 경로 재사용 (읽기 전용) | 미착수 |
| 2 | **SEV 시뮬레이션** — PyBaMM P2D 로 0.2C 전류 차단 프로토콜을 돌려 ΔV(1 s)·SEV 를 합성하고, (PVS, SEV) 2×3 Jacobian 으로 "부호는 같아도 감도 비가 다른가"(H2)를 판정 | 동역학 파라미터 세트 (열역학만으로는 안 됨) | 미착수 |
| 3 | **ML 라벨 degeneracy 전파** — fitted 라벨로 학습한 모드 예측 ML 이 라벨의 비식별성을 어떻게 물려받는지, 정답을 아는 합성 데이터로 정량화. 프로토콜 식별자 입력의 기여 분리 (permutation/SHAP) | Phase 1–2 의 feature + RF/GBM (sklearn) | 미착수 |

Phase 1·2 는 **본 실행 없이** 판정 가능하도록 설계한다 (Jacobian 은 국소 분석).
전역 degeneracy 는 degradation-degeneracy 의 격자 방법론을 그대로 가져온다.

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
