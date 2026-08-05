# degradation-degeneracy

**full-cell 곡선 하나로 LAM_PE와 LAM_NE를 분리할 수 있는가?**

2026-08-05 연구세미나 22p에서 `LAM_PE ≈ LAM_NE ≈ 13%`로 나온 결과가
실제 물리인지 **fitting 축퇴(degeneracy)** 인지 판별하기 위한 코드베이스.

PyBaMM으로 정답을 아는 합성 데이터를 대량 생성하고,
기존 α·β fitting 코드가 그 정답을 복원하는지 채점한다.

---

## 이 저장소는 아직 비어 있다

`reference/`의 원본 스크립트와 `docs/`의 설계 문서만 들어 있는 **시작 상태**다.
구현은 `docs/04_PROMPTS.md`의 Phase 0부터 순차적으로 진행한다.

---

## 코딩 에이전트에게

```
docs/00_START_HERE.md 를 먼저 읽어라.
```

그 파일이 읽는 순서, 환경 구축 절차, 절대 원칙, 완료 기준을 모두 담고 있다.

---

## 사람에게 — 빠른 시작

```bash
# 1) 환경
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2) 검증 (IDAKLU / composite DFN / GPU 확인)
python scripts/verify_env.py

# 3) 이후는 구현 진행에 따라
./run.sh --mode verify
./run.sh --mode sweep1d --out results/sweep1d_v1        # 32p 재현
./run.sh --mode grid --config configs/grid_coarse.yaml --dry-run
```

---

## 문서

| 파일 | 내용 |
|---|---|
| `docs/00_START_HERE.md` | 부트스트랩 — 에이전트 진입점 |
| `docs/01_CONTEXT.md` | 연구 배경, 축퇴 문제 정의 |
| `docs/02_CODE_AUDIT.md` | 원본 코드 분석 및 문제점 |
| `docs/03_ARCHITECTURE.md` | 목표 구조, run.sh 스펙, GPU 현실론 |
| `docs/04_PROMPTS.md` | Phase 0~7 단계별 프롬프트 + git 규약 |

## 참고 자료

| 파일 | 비고 |
|---|---|
| `reference/degrade_mode_sim_original.py` | 원본 스크립트. **수정 금지 — 회귀 검증 기준** |
| 발표 PDF (별도 제공) | 21·22·32·33·34p가 핵심 |

---

## 절대 원칙

1. 물리 파라미터를 임의로 바꾸지 않는다. 변경 시 `physics(...)` 커밋 + 근거 명시.
2. 하드코딩된 완방상태값(`36.7`, `3446.3`, `58439.9`)을 사용하지 않는다. 자동 산출한다.
3. 모드↔프로토콜 매핑(`discharge_first` / `charge_first`)을 보존한다.
4. Phase 완료 기준을 만족하지 못하면 다음으로 넘어가지 않는다.
5. GPU를 무리하게 적용하지 않는다. CPU 병렬이 1차 목표다.
