# S0 단계 1 메모리 고침 (SELF-155) — 보고 (2026-11-06 · 작업 트리 에이전트)

- ⚠ 이 REPORT.md 는 작업 트리 에이전트가 쓰지 못해 (하네스가 하위 에이전트의 보고 파일 쓰기를 막음) 본 세션이 넣었다 (에이전트 보고 본문 그대로 · 머리 두 줄 · 본 세션 몫 메모만 보탬) · 넣은 뒤 이 폴더 SHA256SUMS 를 다시 만들었다.
- 근거 = `docs/reviews/rint2_s0_mem_probe_20261106/README.md` (kgy 측정 · 1,562 s 까지 2–3 GB → `_distinct_instances` 의 `query_pairs` 한 줄에서 30 s 에 43 GB) · 1저자 11-04 Q2 *"권고대로"* (메모리 재기 → 도구 고침 · 시험 먼저 · 출력 바이트 같게) · Codex 회차 ② 판정문 §8 Q8 확인 목록.

S0 단계 1 의 메모리 폭증을 고쳤다. 합성 입력에서 과학 값 · 정준 배열은 고치기 전 판과 비트로 같고, 다른 곳은 아래 **예외 둘**뿐이다. kgy 실침대 재실행은 아직 하지 않았으므로 실침대에서의 최대 RSS 는 아직 모른다.

## 1. 커밋 · 가지 · 바뀐 파일
- 작업 트리 커밋 하나 (가지 worktree-agent-a79fb5a8ec6b0a668 · push 안 함) → main 반입 = 본 세션 cherry-pick -x (원 커밋 번호 = 반입 커밋 메시지의 cherry picked from 줄).
  - 시작할 때 가지가 bf0dd1a32 (Initial commit) 에 있어서 그날 main 끝 판 (push 전 · 그 내용은 뒤에 `342eff6e1` 로 push) 으로 reset 했다 (그 시점에 작업 없음). 중간 커밋 둘은 amend 로 한 커밋에 흡수 · 최종 확인 판의 코드 blob 넷 = 반입한 작업 트리 커밋과 같음.
- 바뀐 파일 4 개 + 이 증거 폴더:
  - `scripts/carbon_junction.py`: `_subpieces` · `_near_seg_pairs` · `_closest_chunks` · `_distinct_from_pairs` · `_ball_seg_candidates` · `_touch_len_all` 묶음 · `_PAIR_SEARCH_LAST` (진단용 · 원장 밖).
  - `scripts/ca_s0_census.py`: `fiber_sphere_instances` · `_min_dist_to_segments` 의 후보 줄만.
  - `scripts/test_carbon_junction.py` · `scripts/test_ca_s0_census.py`: 새 시험 묶음.
- 손대지 않은 것: findings.json · CLAUDE.md · check_all.sh · mpm3d_compaction.py · rint_r_chain.py · step3_sigma.py · fibre_segment_raster.py · mpm_webapp_payload.py · 문턱 · 허용폭 · 규칙 · `CJUNC_MODEL_VERSION` · `TOOL_VERSION`.

## 2. 원인 확인 (코드 · 합성 측정)
- `rad = 2·max(선분 반 길이) + D` 를 모든 선분에 똑같이 쓴다 → 가장 긴 선분 하나가 검색 반지름 전체를 정한다.
- `_self_pairs` 도 같은 선분에 같은 `query_pairs` 호출 → `_distinct_instances` 만 고쳤다면 바로 뒤에서 다시 터졌을 것.
- 실측 (7,084 선분 · 6 µm 선분 4 개): 옛 반지름 6.2 µm 후보 = 17,701,828 쌍 (count_neighbors 로 저장 없이 셈) · 새 후보 = 61,131 쌍 · 옛 판 = 주소 공간 상한 4 GB 에서 MemoryError · 새 판 = 92 MB.

## 3. 후보 순서 의존 (옛 `_distinct_instances`)
| 단계 | 후보 순서 영향 |
|---|---|
| 쌍 방향 · `seg_seg_closest` · 근접 판정 | 없음 — 행마다 원소별 (덩어리 1 · 2 · 3 · 7 과 순열에서 norm · einsum 비트 같음 · numpy 2.4.6 · 1.24.4) |
| `keyof` 사전 | 없음 — 열쇠 유일 · 번호만 바뀜 |
| union-find 무리 | 무리 = 연결 성분 (영향 없음) · 무리 번호 순서 = 후보 순서 |
| 무리 안 접점 b · Si/Sj · d0 · L_c | 없음 — (ε 띠 · 중점 · i · j) 전순서 · np.unique · min · `_touch_len_all` 의 같은 ua 묶음 합집합 |
| 마지막 lexsort (piece_i, piece_j, Ci) | **있음** — 다섯이 비트로 같은 두 instance 는 무리 순서 = 후보 순서 (안정 정렬) |
| 그 뒤 (`by_pair` 면 배정의 `da+db < bestd` 동률 · 보고 목록 정렬 동률) | 위 동률이 있을 때만 |
- 옛 `_self_pairs` · S0 `_cand_pairs` 는 이미 (i, j) 정렬 → 순서 무관.

## 4. 선언된 예외 둘 (Codex 에 그대로 알릴 것)
1. **같은 조각 쌍 · 같은 접점 (비트) 두 instance 의 순서** — 옛 판은 query_pairs 출력 순서에 따라 바뀐다 (시험 PTIE 실측) · 새 판은 마지막 키 (최근접 쌍 선분 i, j) 로 정준화 · 그런 동률이 없는 침대에서는 옛 순서와 같다.
2. **옛 판이 놓친 참 쌍을 새 판은 찾는다** — 꼴 = 가장 긴 선분 끝 쪽에서 거리 ≈ 문턱 (옛 반지름 여유 0 → 반올림으로 놓침) · 실측 예 PEDGE: 선분 거리 0.19999999999999996 ≤ D 인데 중점 거리 1.3000000000000003 > 옛 반지름 1.3 → 옛 판 instance 0 · 새 판 1 · S0 `fiber_sphere_instances` (쌍 0 → 1) · `_min_dist_to_segments` (inf → 0.5) 에도 같은 꼴 (M5) · 구현 **뒤** 발견 → 고치기 전 판에서 그 시험이 실패하는 것은 따로 기록.
- 실침대에 그런 꼴이 있는지 = 미확인 (옛 판이 끝까지 돈 적이 없다).

## 5. 시험 수 (전 → 후)
| 묶음 | 고치기 전 코드 | 최종 시험 · 고치기 전 구현 | 최종 (깨끗한 트리) |
|---|---|---|---|
| test_carbon_junction | 500/500 (옛 시험) | 532/547 — 실패 15 = 새 동작 칸만 (PSRCH 2 · PEDGE 1 · PTIE 2 · PMEM 3 · PMUT 7) | **547/547** |
| test_ca_s0_census | 167/0 (옛 시험) | 180/6 — M3 · M5 새 판 · M4 4 | **186/0** |
- 시험 먼저 중간 기록: carbon_junction r1 528/542 (실패 14 중 1 = 제 시험 픽스처 수 오기) → r2 530/543 (실패 13) · S0 쪽 시험 먼저 180/3.
- 대조 칸 (PEQ · PREG · PS0 · CP-ORD · S0 M1/M2) = 고치기 전 구현에서도 모두 통과 (계약을 정의).
- CP-ORD 수정: 새 판이 `query_pairs` 를 안 부르므로 섞는 자리를 `_near_seg_pairs` 출력으로 옮김 · 공허 통과 막으려고 "섞은 출력 수 > 0" 확인.

## 6. 비트 대조 범위
- PEQ: 함수 단위 픽스처 9 (긴 선분 무작위 셋 · 조각 경계 + 거리 정확히 D · 바로 밖 · 빈 결과 · 같은 fid 끊긴 조각 · 나란한 띠 동률 · U · 닫힌 고리 · 점 선분 + 중점 겹침) × 덩어리 설정 4 (기본 · (1,1,1) · (2,3,5) · (7,2,13)).
- PREG: 원장 전체 (지문 포함) — 손 픽스처 7 + 생산 단위 무작위 침대 2 × s_min 2.
- PS0: `junction_census` 블록 · 배열 (SBE 꼴 · DBE 꼴).
- S0 M1/M2: 11 꼴 × 질의 덩어리 4.
- S0 끝-끝 (payload 실물 · 킷 4 · 긴 선분 킷 포함 · 옛 S0 + 옛 원장 ↔ 새 판): 파일 6 · npz 41 배열 바이트 같음 · JSON 의 뜻밖 차이 0 · 달라진 것 = 계획의 `source.tool_sha256` → 계획 해시 · `elapsed_s` (둘 다 진실한 옛 · 새 blob 해시 확인) · 계획 문턱 `values_um` 같음.

## 7. 메모리 · 후보 수 · 시간
측정 (합성 · 이 기계):
| 입력 | 옛 판 | 새 판 |
|---|---|---|
| A: 2,072 선분 | 후보 1,824,541 · 825 MB | 후보 42,566 · 83 MB |
| B: 7,084 선분 | 후보 17,701,828 · MemoryError (4 GB 상한) | 후보 61,131 · 92 MB |
| C: 긴 선분 없음 | 후보 31,804 | 31,804 (같음) |
| D: 실침대 밀도 · 36,274 선분 · 8 µm 선분 4 | 후보 193,377,451 (셈만) | 후보 170,817 · 140 MB · 0.84 s |
| E: 실침대 밀도 · 긴 선분 없음 | 118,018 | 118,018 (같음) |
| S0 fiber_sphere · SDCP 밀도 구 2,631 · D 침대 | 1.32 GB · 쌍 487 | 86 MB · 쌍 487 |
| S0 M3 · SDCP 꼴 구 2,000 | 후보 1,294,323 | 1,720 |
- 원장 전체 (새 판 · 실침대 밀도 합성): 8,857 선분 → 2.2 s · 96 MB · 36,195 선분 → 8.5 s · 164 MB · 94,072 선분 → 22.7 s · 305 MB.
- 어림 (실침대 · 확인 전): 실침대 SBE = VGCF 점 1,643,483 · 상자 50.0 × 50.0 × 72.5 µm³ (재압밀 기록) · 11-06 RSS 계단 해석으로 옛 후보 > 2.1e9 쌍 · 점 간격 0.1 µm 가정 + D 침대 부피 환산 = 새 후보 약 8e6 쌍 · 원장 RSS 약 5 GB · 원장 시간 약 7–40 분 (40 분 = PTFE 덮임 고리 (instance 수 × PTFE 선분 수) 제곱 상한) · 실침대 최대 선분 길이 = 모름 → `probe2.py` 가 `pair_search.json` 으로 남김.

## 8. 3.11 · 3.8 묶음 (최종 · 깨끗한 트리)
- 3.11 (15 묶음 통과): carbon_junction 547/547 · ca_s0_census 186/0 · run_contract 124/124 · step3_rint PASS · ptfe_face_alpha 242/0 · ca_ext_b6 502/0 · ca_ext_runner 151/0 · ca_ext_verdict 31/0 · ca_ext_z1 95/0 · ca_ext_z3 84/0 · rint_r_chain 468/468 · rint_r_chain_e2e 51/0 · step3_target_cert 264/264 · step3_conv_cert 30/30 · webapp ca_ext_labels 93/0.
- 3.8 (3.8.20 · numpy 1.24.4 · scipy 1.10.1 = kgy 판 · `check_kgy_py38.sh`): 11 묶음 ✓ — carbon_junction 547/547 · ca_s0_census 186/0 · rint_r_chain 468/468 · rint_r_chain_e2e 51/0 · step3_conv_cert 29/29 (3.8 = 29).
- 주의 (더러운 트리): 예비 실행 rint_r_chain 457/468 = R 사슬 신원 관문이 미추적 · 수정 파일을 "더러움" 으로 보고 사다리를 멈춤 · 깨끗한 트리 468/468 · 로그 `logs/prelim_dirty_worktree_py311_others/`.
- 빠른 점검: check_doc_refs ✓ · 원장 자기일관 ✓ · --ban-sweep ✓ (42 × 9,474) · 게이트 (check_all.sh) 안 돌림.

## 9. 변이
- 시험 안 PMUT: 변이 6 (반지름 = D 만 · 조각 반 길이 반 · 조각 중점 → 시작점 · 마지막 덩어리 버림 · 동률 키 뺌 · 반올림 여유 0) 모두 값 대조에 걸림.
- S0 M4: 변이 3 모두 잡힘.
- 전체 묶음 변이 (`mutation_full.py`): 7/7 잡힘 · 원본 sha256 되돌림 확인 — M1 → PSRCH · PEQ · M2 · M3 → PSRCH · PEQ · PREG KU · S0 M5 · M4 → PEQ · S0 끝-끝 R3–R5 · M5 → PTIE · M6 → PEDGE · M7 → S0 M1 · M2.
- 사전 공격 탐침: 칼날 입력 5 꼴 (퇴화 선분만 · 같은 선분 공유 · 1e6 µm 좌표 · 길이 비 1e5 · 중점 60 개 겹침) 상위집합 · 정준 순서 위반 0.

## 10. 같은 꼴 점검
- 고침 (지금): `_self_pairs` (같은 호출 · 같이 터짐) · S0 `fiber_sphere_instances` · `_min_dist_to_segments` (반지름에 전역 최대 선분 길이 · 단계 2 SDCP 구 116,532 개에서 위험 — 합성 1.32 GB → 실침대 부피 환산 약 55 GB · 어림) · 지금 고친 까닭 = R 사슬은 S0 단계 1 · 2 보고의 일곱 파일 지문이 R 런 코드와 같아야 한다 (`s0_code_problem` → CODE_PIN_MISMATCH) · 단계 2 전에 따로 고치면 단계 1 을 다시 돌려야 한다.
- 그대로 둔 것: `_cand_pairs` (vv_census · 11-06 실침대에서 끝까지 돎 · 그 구간 (1,201–1,261 s) 최대 표본 3.50 GB · 긴 꼬리 1 % 반지름에 hmax 가 아직 들어감 = 잔여 위험) · `ca_s0_census.py:1614` (AM 드묾) · `ptfe_face_alpha` (실침대 통과) · SDCP 근접 `query(k=1)`.
- ⚠ 11-06 실측 1,356 s 에 표본 하나 6.96 GB 로 튐 — 그 사이에 돈 것 (vv 끝 · 미리보기 포트 · PTFE 거리 · AM fiber_sphere) 미확인.

## 11. Codex §8 Q8 확인 칸
| 칸 | 상태 |
|---|---|
| 래스터 · instance/포트와 순서 · 동률 · 중복 · L_c · s · 분위수 · 정준 지문 · 문턱 선택 | 다룸 (PEQ · PREG · PS0 · PTIE · S0 끝-끝 · 계획 values_um 같음) |
| chunk 경계 · 마지막 조각 · 빈 부류 · 겹친 경계 | 다룸 (덩어리 1 · 2 · 3 · 5 · 7 · 13 · 37 · 50 · 변이 M4 · 빈 픽스처 · 조각 경계 접점 · 중점 겹침) · "겹친 경계" = 에이전트 해석 |
| 생산 래스터 ↔ S0 래스터 | 래스터 코드 무변경 · 끝-끝 raster 칸 같음 |
| 부분 census 채택 금지 · SBE 전용 · σ 비열람 · 입력 무쓰기 · 새 폴더 · 실패 보존 | kgy 운용 (아래) |
| 새 핀의 peak RSS · 시간 · 종료 코드 | **안 함 (kgy 필요)** |
| 핀 diff · 소비자 · S0/R 계획 해시 · 숫자 · 실행 정책 | 일부 — 소비자 묶음 통과 · S0 계획 해시 = 도구 sha 가 바뀌어 새 값 (진실한 값) · R 계획 · 숫자 · 정책 그대로 |
| "출력 바이트 동일" 범위 | 과학 값 · 정준 배열 = 같음 · 코드 출처 · 시간 = 진실한 새 값 |

## 12. kgy 재실행 (권고 · 1저자가 돌림)
- 새 핀 (이 고침이 push 된 sha) · 새 폴더 · 감시 셸 = 11-06 것 그대로에 후보 검색 기록만 보탠 판 (`tools/run2.sh` · `tools/probe2.py` · 원본 `run.sh` 와 감싸개 이름만 다름 · 상한 min(46, 여유 − 6) GB · `$HOME/dem-venv` · SBE · `--stage 1` 그대로).
- 채택 조건: rc 0 이고 출력 폴더에 `s0_stage1_kit_SBE_vgcf100.json` · `s0_junctions_*.npz` · `s0_instances_*.npz` · `cjunc_plan.json` · `cjunc_plan.sha256` · `payload_capture_*.log` 가 다 있을 때만 · 아니면 실패로 보존.

## 13. 본 세션 몫
- 원장 SELF-155 (예외 둘 · S0 쪽 같은 꼴 고침) · 시험 시간 늘어남 (carbon_junction 약 20 s → 45–85 s) · Codex 짧은 재확인에 넘길 것 = 선언된 예외 둘 · CP-ORD 섞는 자리 이동 · S0 계획 해시 변경.
