# kgy GPU 확인 v8 (Q11 전처리 C 꼴 · 핀 56f4cfbb1) — 결과 (11-13 · 대피 세션 · 개발 자료)

- 무엇: 옛 판 `scripts/step3_sigma.py` (`11a794674` · sha256 8d428ff5…) ↔ 새 판 (핀 `56f4cfbb1d26371007b460a992d4cfc1ef68e950` · sha256 859310da…) 의 GPU CG 풀이를 같은 합성 계 (n_side 298 → n 26,463,592 · nnz 184,712,320 · seed 20261112 · logc 1.0 · rtol 1e-12 · maxiter 60000) 에서 다섯 쌍으로 비교 · 기대 = 다섯 쌍 비트 같음 · 새 판이 반복당 빠름.
- 실행 = 1저자 kgy (RTX 3090 · Python 3.8.10 · numpy 1.24.4 · cupy 12.3.0) · 폴더 q11check_kgy_20261113T044848Z · rc 0 · 원본 = `result.json` · `check.log` · `q11_rerun.out`.
- 블록 = `gpu_check_block_v8_as_run.txt` (md5 9182316778b3d01719a8f0219eb3601b) = v7 (md5 9655e791d5f0064d91c136561225a422) 에서 `Q11REPO` 한 줄만 바꾼 판 — v7 은 `~/dem-mt/scripts` 에 형제 모듈 `se_material.py` 가 없어 시작에서 멈췄다 (풀이 0 · 블록 결함 · 원장 등재 = 다음 고침 묶음) · v8 = S0 단계 1 이 만든 핀 작업 트리 `~/dem-s0-56f4cfbb1` 을 본다 · 안 python md5 관문 (acfeb4b4e1515d6aa7d46ddaf67e6e68) 은 그대로 · 1저자 kgy 사본의 바이트 = [미확인] (같은 sed 로 만든 글).

## 다섯 쌍

| 쌍 | 반복 (old · new) | 결과 |
|---|---|---|
| control old · old | 200 · 200 | 비트 같음 (이 기계 실행 사이 결정성) |
| control new · new | 200 · 200 | 비트 같음 |
| short old · new | 200 · 200 | 비트 같음 · 반복당 old 0.05289 s · new 0.018475 s |
| main old · new | 2,631 · 2,631 | info 0 둘 · 비트 같음 (해 sha256 64f21eae…) · old 125.077 s (반복당 0.04754 s) · new 34.116 s (0.012967 s) · 3.666 배 |
| resolve (x0 = old main 해 · rtol 1e-14) | 621 · 621 | info 0 둘 · 비트 같음 (해 sha256 b0132b4e…) · 반복당 old 0.050311 s · new 0.015067 s (3.34 배) |

## Codex 반박 1/2 Q11 GPU 소비 규칙 대조

| 규칙 | 이 결과 |
|---|---|
| 주 · 이어 풀이 info = 0 | main 0 · 0 · resolve 0 · 0 ✓ |
| 유한 | 직접 칸 없음 (schema q11-gpu-check-v1) — 비교 수치로 간접 확인: NaN 이 있으면 value_differ_count ≥ 1 (NaN ≠ NaN) · ±inf 가 있으면 max_abs_diff = NaN (inf − inf) → main · resolve 모두 0 · 0.0 ✓ · 직접 칸 = 고침 묶음의 소비 규칙 |
| backend | args.backend cupy · 풀이 넷 다 requested gpu · used gpu · fallback_reason null · precond jacobi ✓ |
| 짧은 200 반복 = 같음일 뿐 수렴 아님 | control · short = 같음 근거로만 · 수렴 근거 = main · resolve (info 0) |

## 조건 · 한정

- 부하: 1저자 DFT + 다른 계정 그래픽 앱 둘 + 화면 녹화가 같은 GPU 를 쓰는 중 (끝난 뒤 watch = 88 % · 6,229 MiB) → 반복당 시간 · 배수는 참고 (벤치 3.40–3.79 배 범위 안) · 비트 같음 판정과는 무관.
- 합성 계 · kgy 한 기계 — 실침대 · gabia 로 일반화하지 않는다 (Codex 반박 1/2 Q11) · 실침대 시간 = ⑥ 시도 3 · 4 (고침 뒤 최종 핀).
- 지위 = 개발 자료 (1저자 11-13 Q5) · 고침이 `scripts/step3_sigma.py` 의 풀이 길에 닿으면 최종 핀으로 다시 잰다.
- 가림: `result.json` 의 홈 경로 2 곳 → <HOME> · 원본 sha256 = `ORIGINAL_SHA256.txt` · 이 폴더 바이트 = `SHA256SUMS`.
