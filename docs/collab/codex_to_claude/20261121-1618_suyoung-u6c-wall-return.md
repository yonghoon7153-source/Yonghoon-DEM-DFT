| 트랙 | 계산 | 상태 | 숫자 | 다음 |
|---|---|---|---|---|
| 수영 U6(c) 설정 ① | F8·F16 벽 충격량 2회 관측 | 개발 자료 반환 판독 | 공통 변위 5,157점. 최대 아래판 반력 차이 0.565977332 MPa. 같은 점의 접촉 직후 아래판 보정 차이 2.88 × 10⁻²⁰ MPa, 전 구간 최대 3.40801 × 10⁻⁶ MPa. | 격자와 함께 달라진 시간 간격의 영향부터 따로 본다. |
| 수영 시간 간격 민감도 | F8의 시간 간격을 절반으로 줄여 기존 F16과 일치 | 1저자 WSL 실행 대기, 새 개발 결과 0건 | 새 계산 한 팔, CPU 1, 상한 12분 + 판독 2분. 과거 두 팔 재사용. | 고정 변위에서 세 궤적의 부호 있는 차이를 비교한다. |

가지 `codex/suyoung-u6c-wall-return-1122`. 바탕은 앞 인계 `fd9c167c8f73`. 반입 때 아래 순서로 cherry-pick -x 한다.

1. `263719dc16fe` — 반환 판독, 해시 결속 독립 판독기 및 판독 JSON 둘, 시간 간격 개발 비교 계획. 경로 `docs/reviews/suyoung_u6c_wall_return_20261122/README.md`, `docs/reviews/suyoung_u6c_wall_return_20261122/check_wall_return.py`, `docs/reviews/suyoung_u6c_wall_return_20261122/independent.json`, `docs/reviews/suyoung_u6c_wall_return_20261122/wall_summary.json`.
2. `c36516a26d4a` — 실행 핀. 위 README의 운영 절, 같은 문서 폴더의 dt_control.py, test_dt_control.py, run_wsl.in, test_operator.py. 원 수치 소스 세 개는 과거 고정 바이트다. 합성 판독·대조 시험 10/10, WSL 모의 1회 실행·부분 반환 시험 6/6. 1저자 WSL에서 실제 TXT의 CHECK_ONLY와 이전 반환 TAR 신원 확인 통과. 반걸음 실계산은 1저자 차례.
3. 이 쪽지. 전체 SHA·patch-id와 변경 경로는 인계 ZIP의 HANDOFF.md에 있다.

상세 판독은 `docs/reviews/suyoung_u6c_wall_return_20261122/README.md` §1–2. 운영자가 보낸 TAR·화면 밖 해시와 내부 화면·소스 목록 일치. F8·F16 원 CSV 각각 일치. 고정 판독기 재생성 JSON은 반환 JSON과 바이트 동일. 별도 CSV 집계로 두 번째 아래판 처리의 전 구간 상한 및 같은 격자 행 높이 부분집합도 확인했다.

공유 기록 제안 — F8·F16 최대 반력 차이는 이번 걸음에서 입자 간 접촉을 처리하기 전의 아래판 반력에서 나타났다. 이전 걸음까지의 접촉·전송 이력은 남는다. F8 단독 반걸음 개발 대조를 준비했다. U6(c) 자격과 단계 3은 보류.

1저자 GO 요청 — WSL에서 이전 벽 관측 반환 TAR를 지정해 `GO_SUYOUNG_F8_HALF_ONCE` 1회. TXT SHA256 `0748be9e587e79484a135182da667c9fb11dd67eacecaaf72b7321510bb16e18`. 실행 소스 ZIP SHA256 `9912d1a9601b6867c33a733d07b5c2af45bfd00390ed675ff7687782b17ae6a0`.
