# kgy GPU 확인 v8 (Q11 전처리 C 꼴 · 최종 핀 64e4d213e) — 결과 (11-16 실행 · 11-17 반입)

- 무엇: 옛 판 `scripts/step3_sigma.py` (`11a794674` · sha256 8d428ff5…) ↔ 새 판 (최종 핀 `64e4d213e` · sha256 859310da…) 의 GPU CG 풀이를 **같은 합성 계** (하네스 v8 가 만든 계 · n 26,463,592 · nnz 184,712,320 · logc 1.0 · 실침대 아님) 에서 다섯 쌍으로 비교 · 기대 = 다섯 쌍 비트 같음 · 새 판이 반복당 빠름.
- 실행 = 1저자 kgy · 폴더 `q11check_kgy_q14_20261116T010735Z` · 01:07:35Z → 01:11:59Z · `harness_rc` 0 · 하네스 md5 4eb8a6c3ed2da1039e6b0988f63db906 (= v8 블록의 하네스 · `docs/reviews/rint2_codepkg_20261113/q11_gpu_check_block_v8.txt`) · 같은 기계에서 S0 단계 1 이 도는 중이었다 (속도 = 참고값).
- 원본 = 1저자가 kgy 에서 받아 11-17 올린 tgz (307,048 B · sha256 `8b6e8e77e4e9b64fbb251a67f5cd3bdf7db5a90fbad1b311211f3739b936b579` = 진행 기록 11-16 줄의 `8b6e8e77…`) · 안 파일 32 (보통 파일만 · 링크 · 절대 경로 · `..` 0) · 새 빈 폴더에 `python3 -I` 로 풀어 읽었다.
- 이 폴더 = `check.log` · `meta.txt` (그대로) · `result.json` (홈 경로 2 곳 → `<HOME>` · 그 밖 그대로).  넣지 않은 것 = 코드 사본 넷 (`s3_old.py` = `11a794674:scripts/step3_sigma.py` · `s3_new.py` = `64e4d213e:scripts/step3_sigma.py` · `se_material.py` = `64e4d213e:scripts/se_material.py` — 셋 다 sha256 같음 대조 · `q11_gpu_check.py` = 하네스 md5 위와 같음) · `cupy_cache/` cubin 25 (GPU 컴파일 산출).  원본 32 파일의 sha256 = `ORIGINAL_SHA256.txt` · 이 폴더 바이트 = `SHA256SUMS`.

## 다섯 쌍 (`check.log`)

| 쌍 | 반복 (old · new) | 결과 |
|---|---|---|
| control old · old | 200 · 200 | 비트 같음 (이 기계 실행 사이 결정성) |
| control new · new | 200 · 200 | 비트 같음 |
| short old · new | 200 · 200 | 비트 같음 · 반복당 old 0.054892 s · new 0.017326 s |
| main old · new | 2,631 · 2,631 | info 0 둘 · 비트 같음 · old 127.939 s (0.048628 s) · new 28.766 s (0.010934 s) · **4.447 배** |
| resolve (x0 = old main 해 · rtol 1e-14) | 621 · 621 | info 0 둘 · 비트 같음 |

- `CONSUME adopt = True` (identical · converged · backend_ok · short_iters_ok · source_ok 다 참 · why 빈칸) — Codex 반박 1/2 의 Q11 소비 규칙 (`consume.adopt`).

## 11-13 (핀 `56f4cfbb1` · `docs/data/rint2_q11_gpu_check_kgy_20261113/`) 과 견줌

- 같은 합성 계 · 같은 반복 수 (main 2,631 · resolve 621) · 다섯 쌍 비트 같음 그대로.  main 반복당 배수 11-13 3.666 ↔ 11-16 4.447 — 두 날 같은 GPU 의 다른 부하가 달랐다 (참고값 · 배수 차의 원인을 가르지 않는다).

## 한정

- 합성 계 · kgy 한 기계 · 다른 부하가 있던 날 — 실침대 반복당 시간 = ⑥ 시도 3 · 4 (`docs/data/rint2_probe6_a3_20261116/` · `…a4…` · 0.0105 s) · gabia 로 일반화하지 않는다.
- 지위 = Q11 소비 규칙의 채택 근거 기록 · 봉인 · R 런 · 실행 GO 아님.  시간 다시 어림 3 판 (`docs/reviews/rint2_time_reestimate_20261111/README.md` 끝 절) 의 "Q11 4.447 배" 는 이 파일의 main 줄이다 (11-17 반입 때 초안의 "실침대 · 621 반복" 표기를 "합성 계 · 2,631 반복" 으로 고쳤다).
