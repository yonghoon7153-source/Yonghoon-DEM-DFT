# Rint ② S2 — 긴 접촉 길이 비례 법칙 (1저자 10-20 밤 Q17 = 권고대로) · 시험 먼저 · 작업 트리 · push 안 함

## 결정 (1저자 10-20 밤 · *"q는 권고대로"* = Q17 (가))
- 지금 계약 J8 = "긴 접촉 (L_c > L_par) 이 하나라도 있으면 정량 거부" → **대체**.  구현 B · C 의 합성 시험에서 긴 접촉이 VV instance 의 27.6 % (touch 정의) · 꺾인 섬유 합성 572 중 73 · 꺾임 자기 접합 398 — 그대로면 실침대에서 정량이 멈춘다 (합성 · 실침대 미확인).
- **새 법칙 (v0)**: 접합 컨덕턴스 G_j = **max(1, L_c / L_par) / R_j,0** (g_code = 1e4 · max(1, L_c/L_par) / R_j) — 긴 접촉 = 점 접합 L_c/L_par 개가 나란히 붙은 것 (선 접촉 협착 컨덕턴스 ∝ 길이의 1차 근사) · **새 손잡이 없음** (R_j,0 하나 그대로) · L_par = 2 (r_fi + r_fj) = 0.30 µm (= 깊은 직교 교차의 L_c · 지금 값 그대로) · 경계에서 연속 (L_c = L_par 에서 배율 1) → B 가 봉인한 "상대 1e-9 비교 허용" 은 배율 쪽에는 필요 없다 (긴 접촉 표지 · 집계에만 남기거나 빼고 이유를 적는다).
- **L_c 정의 = touch**: 두 가닥 각각에서 중심선 거리 ≤ r_fi + r_fj 인 구간 길이의 최댓값 (B 의 지금 정의 그대로 · `carbon_junction.py`).  관통 (d < r_fi + r_fj) 포함 · 기하 근접 (MPM 은 섬유 접촉 역학을 풀지 않는다 · 한정어).
- **간선 꼴 (v0)**: instance 하나 = 간선 하나 (지금 포트 규칙 그대로 · 최근접점) 에 배율만 곱한다 (lumped) — 접촉 길이를 따라 나눠 붙이는 분산판 (k = ceil(L_c/L_par) 간선) 은 **v1 후보** (기록만).  대신 **절단 발자국이 접촉 구간 전체**를 덮어야 한다: 긴 접촉 instance 의 선분 쌍 run 전부 (d ≤ r_fi + r_fj + tol_ff + √3·h/2) 의 i · j 셀 사이 면 = 절단 — 발자국 밖에 남은 융합 i|j 면이 R_j 를 우회하지 않게 (지금 코드가 "최근접 선분 쌍" 만 보는지 먼저 확인 · 그렇다면 그것이 이번에 고칠 같은 부류).
- **꺾임 자기 접합 거르기**: 같은 fid 의 비연속 구간 instance 는 두 최근접점 사이의 **경로 호 길이 s** 를 잰다 · s < s_min = 같은 가닥의 연속 (접합 아님 · 절단 없음 · 지금 복셀 융합 그대로) · s ≥ s_min = 진짜 접힘 · 고리 접촉 (절단 + R_j 간선 · 배율 같은 법칙).  **s_min = 필수 입력 · 기본값 없음** — S0 단계 1 (새 SBE 침대) 의 분포를 본 뒤 등록 R §2-1 개정으로 고정 · 정량 모드에서 s_min 이 없으면 구조화 거부 (지금 문턱 숫자들과 같은 꼴) · 개발 · 시험에서는 명시 값으로.
- 기록 (`ca_ext.cjunc` 의 B 출력 칸에): 긴 접촉 수 · L_c 분포 요약 (최댓값 · 분위) · 배율 합 · 자기 접합 (s < s_min 으로 거른 수 · 남은 수 · s 분포 요약) · 법칙 이름 (`len_scaled_v0`) · s_min · 지문에 포함.

## 기반
- 너의 작업 트리에서 `git reset --hard 61b6a9ec5` (= 구현 B 의 끝 · 가지 `worktree-agent-a3a891444f3a490d1` · 기반 `d1768cf0c`).  `git fetch` 하지 않는다.  (다른 에이전트가 A · B · C 를 합치는 중 — 너의 커밋은 나중에 메인이 그 위로 옮긴다 · 고칠 파일은 `scripts/carbon_junction.py` · `scripts/test_carbon_junction.py` (+ 꼭 필요하면 `scripts/step3_sigma.py` 의 B 훅 몇 줄) 로 좁힌다.)
- 정본: 설계 `docs/reviews/rint_carbon_additive_design_v1_20261020.md` §1-2 #11 · #13 · §4-1–§4-5 · 계약 `docs/reviews/contact_resistance_pipeline_draft_v2_20261006.md` §3-8 · `…_v3_20261006.md` §5 · `…_v3_1_20261007.md`.
- ⛔ 봉인 32 파일 (`scripts/run_network_194_parallel.py` 의 `CODE_FILES`) 은 건드리지 않는다.

## 커밋 1 — 시험 먼저 (`scripts/test_carbon_junction.py`)
- 직교 깊은 교차 (L_c ≈ L_par) → 배율 1 = 옛 점 접합과 σ 같음 (긴 접촉 없는 침대 = 옛 결과와 비트 같음).
- 나란한 두 섬유 접촉 L_c = 3 L_par → 배율 3 → σ = 해석 회로값 (섬유 저항 + 접합 1/(3/R_j,0)) · 기계 정밀도.
- 비스듬한 교차 → 배율 (1, …) 연속 · 각도에 단조.
- 옛 동작 제거: 긴 접촉이 있어도 정량 거부하지 않는다 (집계 칸은 남는다).
- 절단 발자국 = 접촉 구간 전체 (긴 접촉 run 의 i|j 융합 면이 남지 않음 — 간선 원장 / 면 tombstone 으로 확인).
- 꺾임: U 자로 접힌 한 섬유 — s < s_min = 접합 없음 · s ≥ s_min = 접합 하나 · s_min 없음 + 정량 = 구조화 거부.
- 불변: 점 순서 뒤집기 · 원점 이동 · 섬유 번호 바꾸기 → instance 수 · 배율 · σ 같음.
- 변이: 배율 제곱 · max(1, ·) 빼기 (짧은 접촉이 약해짐) · s 거르기 끔 · 발자국 = 최근접 쌍만 → 새 시험이 **실패해야**.
- **고치기 전 코드 (61b6a9ec5) 에서 돌려** 새 시험이 실패하는 것을 확인 → 커밋 메시지 "pre-fix N/M (fails = …)" — 반례 수와 검사 수를 따로 (`SELF-124` 부류).

## 커밋 2 — 구현
- 위 법칙 · 거르기 · 발자국 · 기록 · 지문.  cjunc 끔 = 옛 경로 비트 같음 (B 의 C0 시험 그대로 통과).
- ⚠ 본 트리 게이트가 끝나기 전 (≈ 14:30 UTC) 무거운 시험 금지 — 그 뒤: `scripts/test_carbon_junction.py` 전부 · `scripts/test_step3_conv_cert.py` · `python3 scripts/step3_sigma.py --selftest` · `--selftest-rint` · `scripts/test_rint_g2_am_iface.py` · `scripts/test_rint_g2_rrm.py` · `python3 scripts/check_method_discipline.py --selftest` + 인자 없이 (오류 0).

## 규칙
- push · `scripts/check_all.sh` · `git fetch` 안 함 · 문서 · 원장 · CLAUDE.md · 진행 기록 고치지 않음 (메인) · 디스크 적게.
- 커밋 메시지 영어 · 모델 이름 없음 · 끝 두 줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_01H191Ni4xzj9H5ftstAm7Ft`.
- 보고 (한국어 · 표 · 짧게): 커밋 1 · 2 SHA · 고치기 전 → 뒤 · 해석 대조 값 · 변이 표 · 비트 같음 · 발자국을 고쳤는지 (원래 최근접 쌍만이었는지) · 설계와 다르게 한 곳 · 남은 것 (분산판 v1 · S0 도구가 같은 함수를 부르게 하는 일 등).
