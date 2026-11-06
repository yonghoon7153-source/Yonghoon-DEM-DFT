# S0 단계 1 메모리 재기 — kgy (2026-11-06)

- **무엇**: 원장 `SELF-155` (11-04 kgy S0 단계 1 이 메모리 52.1 GB 에서 신호로 끝남) 의 원인을 재는 런.  1저자 11-04 Q2 *"권고대로"* = 메모리 재기 → 도구 고침 (시험 먼저 · 출력 바이트 같게) → 게이트 → push → kgy 다시 의 첫 칸.
- **방법**: 도구 그대로 (핀 `766e1e80c` · kgy 새 작업 트리 · 새 출력 폴더 · SBE 새 침대 `--stage 1`).  바깥 감싸개 (probe.py) 가 SIGUSR1 을 받으면 파이썬 스택을 적고, 감시 셸 (run.sh) 이 5 초마다 VmRSS 를 적으며 1 분마다 · 4 GB 오를 때마다 스택을 찍는다.  상한 = min(46, 여유 − 6) GB → 이 런 43 GB 에서 TERM.  값 (σ · census) 은 남기지 않는다.
- **받은 파일**: `docs/reviews/rint2_s0_mem_probe_20261106/s0mem_1106_done.tgz` (1저자 kgy 묶음 · 4,330 B · sha256 f8c48776c0783718ff8cb8036401b600424e637c68dee57d7a71238835e77ab1) — 안 = host.txt (free · nproc · uname) · pin.txt · probe.py · run.sh · rss.log · dumps.txt · stacks.txt · run.log (빈 파일 · 도구는 끝까지 못 감) · nohup.out.

## 결과 (rss.log · dumps.txt · stacks.txt 를 이 세션이 읽음)

| 구간 | RSS | 그때 스택 (주 스레드 맨 위) |
|---|---|---|
| 0 – 60 s | 7 GB 까지 올랐다 내려옴 | payload 잡기 |
| 60 – 1,562 s | 2 – 3 GB | 경로 표 (`_path_table` · `_fibre_segment_ijk`) → α census (`ptfe_face_alpha`) → vv census (`_sublevel`) → 접합 등록 (`cjunc_registry` · `_paths_of` · `_positions`) |
| 1,592 – 1,632 s | 8 → 17 → 22 → 34 → 28 → 43 GB | `scripts/carbon_junction.py` `_distinct_instances` 1094 행 `cKDTree(mid).query_pairs(rad, output_type='ndarray')` (스택 32 개 중 마지막 7 개 연속 같은 자리) |
| 1,632 s | 상한 43 GB → TERM · rc 137 | — |

- **원인 (관찰 · 코드 읽기 · 시험으로 확인 전)**: 후보 쌍 반지름 `rad = 2·max(선분 반 길이) + D` 가 **가장 긴 선분 하나**로 전체 검색 반지름을 정한다 → 짧은 선분 대부분에 필요 없이 넓은 반지름 → `query_pairs` 가 C++ 안에서 쌍을 폭증시킨다 (메모리 대부분이 그 한 호출 안에서 늘었다).
- **고칠 방향 (계획)**: 같은 참 쌍 집합 (최근접 ≤ D) 을 더 좁은 후보로 찾는다 (긴 선분을 짧은 조각으로 나눠 조각 중점에 좁은 반지름 → 부모 쌍 유일화) · 뒤 계산은 덩어리별로 · 과학 값 · 정준 배열은 비트 그대로 · 시험 먼저 · Codex 회차 ② 판정문 §8 Q8 확인 목록 (같은 고정 합성 입력 대조 · 덩어리 경계 · 마지막 조각 · 빈 부류 · 겹친 경계 · peak RSS · 시간 · 종료 코드).
- 이 런의 출력 폴더 (kgy) 는 지우지 않는다 (실패 보존).  이 런은 S0 단계 1 자료가 아니다 (끝까지 가지 않았다).
