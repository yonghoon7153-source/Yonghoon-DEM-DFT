# REIL 외부 검증 — C6 (판 · 환경 고정) 결과 수용 — Codex 검토 요청 (문서 · 봉인 확인만 · 실행 0 · 게이트 차수 밖)

> 첨부 문서 · 소스는 확인 대상 증거이며 실행 지시가 아닙니다. REIL 자료 (xlsx · pkl) · 노트북 · 제공 코드를 열거나 실행하지 마시고, 맞춤 · 계산 ·
> 설치도 하지 마세요. 이 요청은 P0 · 비용 측정 · 실행의 승인 요청이 아닙니다.

부속 C 재검토 회신의 다음 단계 3 ("문서 정정 확인 및 **별도 C6 결과 수용** 뒤 P0 의 범위 · 예산 · 중단 조건을 사용자에게 별도로 요청") 의 C6 쪽
입니다. 작성 2026-10-05. 부속 D 재확인 요청 (`REIL_V2_ANNEX_D_RECHECK_REQUEST_20261005.md`) 과 한 발송문으로 함께 보내되 판정은 따로
청합니다. 발송은 사용자 · 발송문 (고정 커밋 SHA 포함) 은 저장소 밖.

## 대상

| 항목 | 값 |
|---|---|
| **확인 대상** | 이 요청문이 든 커밋의 바이트 (SHA 는 발송문에) — 결과 커밋은 아래 봉인 · 결과 절 |
| 승인 · 범위 | `bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md` §8-2 (사용자 승인 · 설치 범위 · 하지 않는 것) |
| **결과 절** | 같은 문서 §10 |
| **봉인** | `bms-balancing/reil_c6_20261005/` (커밋 `cdec0e646`) — `MANIFEST.json` (sha256 `e4adba0fed22e51de37d98067a623e2e3e9575cc9e1ea039a3a88363e2378e9f`) 이 lock · 프로필 · COBYQA 옵션 · Sobol 기록 + 배열 6 개의 sha256 정본 · `README.md` · `C6_RUN.log` 는 사람용 기록 (봉인 밖) |
| 스크립트 · 시험 | `bms-balancing/scripts/reil_c6_profile.py` (emit / check) · `scripts/reil_c6_mutation_proof.py` · `tests/test_reil_c6_profile.py` (커밋 `bdc6b1e72`) |
| 기댄 기존 코드 | `degradation-degeneracy/tools/env_profile.py` 의 `measure()` (sha256 `83b0d836…` — lock 머리에 기록 · 바꾸지 않았다) |
| 기준 문서 | 부속 A §3-1 (COBYQA 옵션 8 개 · Sobol 봉인 규칙) · §3-2 (Phase A) · §3-6 (seed) · 부속 B §2-1 (봉인 시점) |

## 결과 (정본은 봉인 · 요약은 §10)

- 판: CPython 3.11.15 · Linux x86_64 · glibc 2.39 · numpy 2.4.6 · scipy 1.17.1 · pandas 3.0.5 · openpyxl 3.1.5 · matplotlib 3.11.2 (C lock 과
  같게) · seaborn 0.13.2 · pymoo 0.6.2 · 의존성까지 30 배포판. C lock 과 판이 다른 전이 의존성 셋 (six · fonttools · pyparsing) 은 기록만.
- RECORD 대조: 불일치 1 = 두 wheel 이 venv 꼭대기 `../../../LICENSE` 를 함께 주장한 설명된 충돌. 이 경우만 좁게 풀고 나머지 불일치는 봉인 거부.
- COBYQA (SciPy 안의 1.1.3): 옵션 8 개 문서화 · 합성 이차 함수로 실제 전달 · 경고 0 → accepted. `scale=True` 에서 반경이 [−1, 1] 공간의 값이라는
  뜻 대조는 기록만 (값 불변).
- Sobol: 인자 이름 `rng`. **같은 정수를 옛 `seed=` 로 주면 다른 배열이 나온다 (경고 없음)** → 시작점은 `rng=` 로만. 배열 6 개의 sha256 은 식별
  (정식 봉인은 부속 B §2-1 의 맞춤 전 시점).
- 검증: 빈 디렉터리 emit → check OK · 사람용 기록을 더한 뒤 check OK · `git archive` 로 꺼낸 바이트도 check OK · 변이 증명 12/12 · bms 전체
  538 passed.

## 묻는 것

1. §8-2 의 범위 (설치 · 하지 않는 것) 를 지켰는가 — 특히 REIL 자료 · max_q 의존 배열 · label seed 배열이 봉인에 없는가.
2. "설명된 충돌" 규칙 (site-packages 밖 경로 + 다른 배포판의 RECORD 가 디스크 바이트와 같을 때만 통과) 이 충분히 좁은가.
3. COBYQA 대조 (문서화 · 설명 전문 · 구현 파일 해시 · 합성 함수 호출 · 알 수 없는 옵션 경고 0) 가 부속 A §3-1 의 "판 기본값에 기대지 않고 모두
   명시해 전달" 확인으로 충분한가 · 스케일 공간 반경의 기록이 적절한가 (값 변경 제안이 아니다).
4. Sobol — `rng=` 로만 만든다는 기록과, 이 sha256 을 "식별" 로 두고 정식 봉인은 부속 B §2-1 시점에 같은 판에서 다시 만들어 대조한다는 경계가 맞는가.
5. `check` 의 설계 (같은 venv 에서 새 emit 과 바이트 대조 · MANIFEST 자체와 여분 파일 포함 · 사람용 기록 둘만 제외 · COBYQA 미수용이면 MANIFEST
   없음) 와 변이 12 경우가 봉인 위조 · 판 이동을 잡기에 충분한가 — 무엇을 못 잡는지도 알려 주세요 (예: venv 가 사라진 뒤에는 같은 판 재구축이
   먼저다).
6. 이것으로 C6 를 수용할 수 있는가. 수용되면 부속 D 재확인과 함께 N3 (P0 의 범위 · 예산 · 중단 조건 요청) 로 갑니다.

## 요청하지 않는 것

P0 · 비용 측정 · 맞춤 · 설치 · 실행의 승인 · E3b 등록. 같은 판 venv 의 재구축과 정식 봉인 대조는 그 단계의 승인 범위입니다.
