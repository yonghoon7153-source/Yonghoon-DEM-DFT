# P2 승인 요청 — 꼭대기 무거운 SOC 의존 PE 오프셋 다리 (논문 후속 · Phantom pOCV) · 2026-10-06 · 실행 0

> 이 문서는 **승인 요청**이다. 승인 전에는 사본 만들기 · 설치 · 곡선 생성 · fit 을 하지 않는다. 저장소 (RUN_SCOPE 포함) 를 바꾸지 않는다 — 실행은 저장소 밖 사본에서만.
> 상태판: `followups/phantom-pocv/STATUS.md`. 설계 근거: 스크래치패드 조사 (아래 §1 의 사실은 그 조사가 저장소 문서 · 코드에서 읽은 것).

## §0 묻는 것

P1 에서 우리 **균일** PE 오프셋 다리는 0 mV 대비 격차 bias 를 **+** 로 움직였고, 논문의 IR 방향 (−) 과 반대였다. 논문의 IR 은 **꼭대기 (고 SOC) 가 무겁다**. 섭동 모양을 논문처럼
바꾸면 부호 · 크기가 바뀌는가. 그리고 이 컨테이너에 원 fit 이 없어 못 본 **성분별 오차 (LAM_PE · LAM_NE · LLI 각각)** 를 새 실행에서 처음으로 본다.

## §1 사실 (조사에서 확인)

- seed_101 다리의 생성: 곡선 `./run.sh --mode grid --config configs/grid_22p_seed.yaml --noise-seed 101` (640 조건 · noise 0 이 320) · fit 공통 `--objective pocv_dvdq,pocv_dvdq_dqdv --n-restarts 5`
  (adaptive 기본 켜짐) · 0 mV = `--reference halfcell --bounds halfcell` + `ocp` 기준 · 오프셋 다리 = `--halfcell-method ocpbias --halfcell-arg pe_offset_mv=N` (캐시는 `python -m src.halfcell --method … --verify`) ·
  모집단 = grid 기준 fit 의 복원가능군 (`tools/analyze_22p_gap.py --restrict-to`) · ①' 격차 bias = `tools/diagnose_pini_transition.py` `gap_stats` · 원점 건강 = `a_ne` ≈ 1.06.
- 이 컨테이너: seed_101 곡선 · 옛 fit **없음** (다시 만들어야 함) · pybamm 26.8.0.0 (v4 정본은 26.7.1.0) · 4 코어 · RAM 15 GB · 디스크 여유 ≈ 7.3 GB.
- 기록된 비용: seed 404 fit 640 조건이 28 코어로 3 분 · dense grid 2952 조건 ≈ 5 분 → 여기 (4 코어 · 320 조건) 추정 grid 5–20 분 · fit 다리당 10–25 분.
- **새로 찾은 문제:** `gap_stats` 의 창 경계 `abs(lli − 0.17) <= 0.02` 가 부동소수 오차로 LLI 0.15 · 평균 LAM 0.11 행을 뺀다 (창이 비대칭) — §7.10 의 bias 열도 이 창에서 나왔다.

## §2 다리 (모두 사본의 `results/_smoke/p2/` · 같은 code / env identity 안에서만 비교)

| 다리 | 기준 곡선 | PE 오프셋 (꼭대기 / 바닥 / 평균 mV) | 용도 |
|---|---|---|---|
| L0 | grid | — | 모집단 (`--restrict-to`) |
| L1 | `ocp` | 0 | Δ 의 기준 · 원점 건강 확인 |
| L2 · L3 | 균일 | 5 / 5 / 5 · 10 / 10 / 10 | P1 의 + 부호 재현 앵커 |
| L4 · L5 | **꼭대기 무거움** | 10 / 0 / 5 · 20 / 0 / 10 | 평균을 L2 · L3 와 같게 |
| L6 | 기울기만 | +5 / −5 / 0 | 평균 효과와 기울기 효과 분리 |

오프셋 식 (사본의 `src/halfcell.py` 에만 · fitting 은 고치지 않음): `δ(y) = pe_offset_mv + pe_tilt_mv · clip((y_C − y)/(y_B − y_T), −0.5, +0.5)` (y = PE 리튬화 비율 · 낮을수록 고 SOC ·
`y_C = (y_T + y_B)/2`). 고정 창 [y_T, y_B] 위에서 평균이 정확히 `pe_offset_mv`. **y_T · y_B 는 truth 의 무열화 완충 · 완방 PE 화학량**으로 실행 전에 계산해 이 문서에 적고 고정한다
(fit 결과에 기대지 않음).

## §3 절차 · 분석

1. 저장소 HEAD 를 `git archive` 로 스크래치패드에 풀고 `git init` · 커밋 (깨끗한 사본) → 오프셋 식 추가 · 커밋 → 사본 sha 기록.
2. 시간 측정 먼저: `--limit 8` 로 조건당 시간을 재고 아래 예산을 넘을 것 같으면 멈추고 보고.
3. 캐시 5 개 `--verify` → grid (`--noise 0 --noise-seed 101 --nproc 4`) → L0–L6 fit → 분석.
4. 분석: 두 목적함수 모두 ①' 격차 bias (`gap_stats` **원 창 그대로** + **부동소수 허용 창** (`<= 0.02 + 1e-9`) 둘 다 보고) · `analyze_22p_gap --restrict-to L0` · 새 스크립트 (사본에만) 로
   **성분별 평균 오차 (LAM_PE · LAM_NE · LLI)** · 같은 조건끼리의 paired Δ 와 bootstrap 95 % CI · 다리별 원점 `a_ne` · 다리별 실제 restart 수 분포 · tilt 다리의 동작점 창 안 실제 평균 오프셋.

## §4 결정 (권고 — 승인 때 바꿀 수 있음)

| # | 결정 | 권고 |
|---|---|---|
| 1 | 조건 수 | **`--noise 0` (320)** — ①' 은 noise 0 행만 쓴다 · 비용 절반 |
| 2 | adaptive | **유지** (옛 다리와 같음 · 끄면 ≈ 8 배) |
| 3 | 창 상수 y_T · y_B | **truth 의 무열화 완충 · 완방 PE 화학량** (실행 전 계산 · 고정) |
| 4 | 선택 다리 | **L6 포함** (평균 vs 기울기 분리) · 바닥 무거움 다리는 제외 |
| 5 | 원점 오염 | **세트 중단** (restart 증량은 protocol 변경이라 하지 않음) |
| 6 | `gap_stats` 부동소수 경계 | **저장소는 지금 고치지 않는다** (RUN_SCOPE 변경 = 게이트 몫) — 분석에서 두 창 모두 보고 · 수정은 게이트 후보 목록에 기록 |
| 7 | 결과의 지위 | **진단 전용 (smoke · 인용 금지)** — 정본으로 만들려면 planned leg + 게이트가 필요 · 이번엔 하지 않음 |

## §5 예산 · 중단 조건 (실행 전 고정)

- 예산: 측정한 총 벽시계 ≤ **4 시간** · 디스크 여유 ≥ **2 GB** 유지 · 시도 1 회 (다리 재실행 없음).
- 중단: 캐시 검증 실패 · L1 원점 `a_ne` 가 [1.05, 1.08] 밖 → 전체 중단 · 왜곡 다리 원점 오염 → 그 다리 해석 제외 (권고 5 면 세트 중단) · 다리 간 조건 집합 / digest 불일치 → 중단 ·
  **L2 · L3 이 + 부호를 재현하지 못하면 tilt 해석 전에 보고하고 중단** · 시간 · 디스크 초과 → 중단.
- 기록: 시작 / 종료 HEAD (저장소 · 사본) · 사본 sha · 환경 (pybamm 판 · lock) · 명령 · stdout / stderr · 외부 rc · 자원 관측 · 결과 파일 — `followups/phantom-pocv/p2_<날짜>/` 에
  (`.log` 는 `git add -f` · 대형 산출은 sha 만).

## §6 하지 않는 것

저장소 코드 · RUN_SCOPE 변경 · 게이트 영수증 · 정본 승격 · 옛 §7.10 수치와의 크기 비교 (부호만 질적으로) · P3–P5.

## §7 채택 문구

> 논문 후속 P2 를 이 문서 (`followups/phantom-pocv/P2_APPROVAL_REQUEST.md`) 의 범위와 §4 권고대로 한 번 승인합니다. 저장소 밖 사본에서만, 다리 L0–L6 · 총 4 시간 · 디스크 여유 2 GB 를
> 상한으로 돌리고, §5 의 조건에 걸리면 기록하고 멈추세요. 결과는 진단 전용입니다.
