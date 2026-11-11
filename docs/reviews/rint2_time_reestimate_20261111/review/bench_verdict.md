# 합성 GPU 벤치 블록 — 내부 반박 리뷰 판정 (2026-11-11 · 독립 조수 · Codex 아님)

- 대상 = (1 판 블록 · 리포 밖) (md5 52f36294… · 안의 스크립트 md5 d2528f45…) · gpu_bench_cg.py · gpu_bench_notes.md · _make_block.py
- 원천 = 본 리포 커밋 68bd2b183 의 `scripts/step3_sigma.py` · `scripts/carbon_junction.py` · `docs/data/rint2_probe6_a2_20261111/` · `docs/data/rint2_siteq_20261109/` (읽기만).
- 이 리뷰도 GPU 가 없다 → **GPU 길은 돌려 보지 못했다**. CuPy 12.3.0 소스도 이 컨테이너에 없다 → CuPy 내부 동작에 대한 말은 전부 [기억 · 미확인] 표지를 붙였다.
- 리뷰 쪽 실수 1 건 (그대로 적는다): CuPy 소스가 디스크에 있는지 찾던 명령에 pip download 한 줄이 섞여 패키지 색인에 한 번 접속했다 — 지시서의 "네트워크 없음" 을 어겼다. 받은 패키지 없음 (pip 색인 캐시 32 KB 한 건) · 리포 · 리뷰 대상 파일 무변경 (git status 0 줄).

## 판정

**고친 뒤에 준다.** 안전을 막는 문제 (P1) 는 없다 — 그대로 돌려도 킷 · R 출력 · 잠금 파일을 건드리지 않고, 붙여넣기가 깨지면 돌지 않는다. 고칠 것은 작다 (스크립트 여덟 군데 · 블록 두 줄 · 아래 §5). 고치지 않고 돌리면: 변이 A 의 반복당 시간 (s · 기계 속도 비) 은 쓸 수 있지만 (i) "해가 비트까지 같은가" 칸은 해석할 수 없고 (ii) 기계의 scipy 판에서는 행렬 꼴이 생산과 다르며 (iii) 우리 프로세스의 GPU 메모리에 상한이 없다.

## 1. 셈

| 본 것 | 수 |
|---|---|
| 안전 항목 (쓰는 곳 · 있는 폴더 · 킷 · 잠금 · 네트워크 · sudo · 설치 · git · 시간 상한 · GPU 메모리 · 호스트 메모리 · md5 관문 · 주소 · 계정) | 14 |
| 재는 것 항목 (동기화 · 예열 · 반복 수 · 미지수 수 · 행렬 꼴 · 호출 대조 · 결과 줄 · 돌려보낼 것 · s 가정) | 9 |
| 실제로 돌린 것 (가짜 홈 · CPU 길 · 작은 크기 · 스레드 1) | 원본 22 번 (블록 그대로 16 · 스크립트 직접 2 · 검산 스크립트 4) + 리뷰 제안본 블록 6 가지 |
| 문제 | P1 0 · P2 3 · P3 8 |

## 2. 돌려 본 것 (전부 가짜 홈 · numpy 길 · 한 변 20–96 칸 · 몇 초)

| # | 무엇 | 결과 |
|---|---|---|
| T1 | 빈 가짜 홈에 블록 그대로 | `[gb] STOP: venv not found` · 새 폴더에 스크립트 파일만 · 다른 파일 없음 |
| T2 | 가짜 venv (python3 을 numpy 길 · 한 변 40 으로 돌리는 심) · Python 3.11 · scipy 1.17.1 | 끝까지 (`DONE` · rc 0 · bench.json status done) · A ↔ B · A ↔ C identical True |
| T3 | 같은 것 · **Python 3.8.20 · numpy 1.24.4 · scipy 1.10.1 (두 기계의 판)** | 끝까지 · 경고 없음 → "Python 3.8 호환" 은 CPU 길에서 맞다 |
| T4 | 이미 있는 폴더 (파일이 든 폴더 · 빈 폴더 · 끊긴 심볼릭 링크) | 셋 다 `nothing run` · 있던 파일 그대로 · 화면에 mkdir 오류 줄 (전체 경로가 찍힌다 → P3-b) |
| T5 | 깨진 붙여넣기 열 가지 (본문 한 글자 · 한 줄 빠짐 · 끝 표지 뒤 공백 · CRLF · md5 한 글자 · 마지막 줄 없음 · 300 줄에서 끊김 · 이름표에 공백 · 빗금 · 빈 이름표) | 전부 풀이를 돌지 않는다 (새 폴더에 스크립트 파일만 남거나 폴더도 없음) |
| T6 | cupy 없음 (cupy 길 · 호스트 문턱만 낮춤 · 한 변 20) | **행렬을 다 만든 뒤** `import cupy` 에서 traceback · rc 1 · bench.json status 가 'started' 로 남음 · bench.log 에 오류 없음 · 화면에 스크립트 전체 경로 (→ P3-a · P3-b) |
| T7 | 기본 문턱 그대로 (이 컨테이너의 호스트 여유 14.4 GB) | `STOP: host MemAvailable 14.4 GB < 16.0 GB (nothing built)` · rc 2 — 호스트 관문은 작동 |
| T8 | nvidia-smi 없음 | `GPU before: None` 뒤 **그대로 계속 간다** (GPU 메모리 관문을 건너뜀 → P2-3) |
| T9 | 호스트 최대 메모리 (행렬 만들기만 · tracemalloc · 한 변 32 / 64 / 96) | scipy 1.17.1 = 232 B/미지수 (세 크기 같음) · **scipy 1.10.1 = 378–381 B/미지수** → 미지수 26,463,592 에서 6.1 GB / **10.1 GB** |
| T10 | 행렬 꼴 (scipy 1.10.1) | `has_sorted_indices False` — 행 안의 열 번호 순서 = 대각 · +1 · −1 · +nz · −nz … (정렬 안 됨). 생산 조립과 같은 꼴 (coo → tocsr) 은 정렬 · canonical |
| T11 | 리뷰 제안본 (§5) 의 블록 — T1 · T2 · T3 · T4 · T5 (한 글자) · T6 다시 | 전부 기대대로. cupy 없음 = 행렬 만들기 **전** 에 멈춤 · 화면 · 파일에 경로 없음 · bench.json status failed + 오류 한 줄 |

## 3. 문제 표

| 등급 | 위치 | 문서 · 코드의 글 | 원천 · 실측 | 고칠 글 |
|---|---|---|---|---|
| **P2-1** 행렬 꼴이 생산과 다르다 (기계의 scipy 에서) | gpu_bench_cg.py 153–155 줄 · 머리말 4 줄 "Times the SAME library calls" · notes §1 "같은 호출" | `sparse.diags([...], format='csr')` 로 만든 L 을 그대로 GPU 에 올린다 | 두 기계의 scipy = 1.10.1 (`docs/data/rint2_probe6_a2_20261111/env.txt` · siteq 기록). 그 판의 DIA → COO → CSR 길은 열 번호를 정렬하지 않는다 (T10 실측). 생산 L 은 `sparse.coo_matrix(...).tocsr()` (`scripts/carbon_junction.py` 2814–2816 줄 · `scripts/step3_sigma.py` 2293–2296 줄) — 중복을 합치며 정렬된 canonical CSR 이다 (T10 의 생산 꼴 확인). [기억 · 미확인] CuPy 의 CSR 곱 (`A @ v`) 은 canonical 이 아니면 GPU 에서 한 번 정렬한다 (COO lexsort) → 마지막 "한 연산" 단계 (375 줄) 에서 GPU 메모리가 몇 GB 더 튈 수 있다 (추정 9 GB 안팎) | 155 줄 앞에 한 줄: `L.sum_duplicates()` (호스트 · 제자리 · 약 2 초 · 메모리 추가 0 — T10 에서 8.7 ns/nnz). 그러면 생산과 같은 canonical CSR |
| **P2-2** "비트까지 같은가" 에 대조군이 없다 | gpu_bench_cg.py 343–358 줄 · notes §1 셋째 줄 · §3 "A ↔ B 가 다르게 나오면 C 를 본다" | A 를 한 번 돌리고 B · C 를 그것과 견준다 | GPU 의 희소 행렬 곱이 같은 입력에 늘 같은 비트를 내는지는 [미확인] (cuSPARSE 기본 알고리즘 · 기억). A 를 두 번 돌려 같은지 보는 줄이 없으면 identical False 가 전처리 꼴 때문인지 GPU 연산 자체 때문인지 가를 수 없다 → 본문 Q6 의 "해가 비트 같게 나올 때만" 을 이 벤치로 판단할 수 없다 | 349 줄 뒤에 A 를 같은 출발 · 같은 수로 한 번 더 돌려 `A_vs_A_again` 칸으로 남긴다 (§5 의 R7). 읽는 법: A_vs_A_again 이 False 면 B · C 의 identical 은 해석하지 않는다 |
| **P2-3** GPU 메모리 관문이 열려 있다 | gpu_bench_cg.py 197 · 229–236 줄 · notes §2-4 "GPU 빈 메모리 9 GB 미만이면 시작 전에 멈춘다" | `if s0 is not None and …` — nvidia-smi 표본이 없으면 검사를 건너뛴다 · 문턱 9,000 MiB · 우리 사용량 상한 없음 | T8 (표본 None → 계속). 실풀이의 우리 몫 = 주 풀이 약 5.6 GB · ⓒ 구간 약 8.3 GB (`docs/data/rint2_probe6_a2_20261111/samples.tsv` 의 전체 사용량 11,988 → 14,648 MiB − 시작 전 6,325–6,373 MiB). 벤치는 GPU 에서 한 번도 돌지 않았다 → "6–7 GB" 는 추정이고, P2-1 의 정렬이 일어나면 더 든다. 같은 GPU 의 다른 프로세스는 메모리가 모자라면 죽을 수 있다 | (가) `import cupy` 뒤 CuPy 가 주는 빈 메모리 (`cp.cuda.Device().mem_info`) 로 한 번 더 검사 — nvidia-smi 가 없어도 닫힌다 (나) 우리 풀 상한: `cp.get_default_memory_pool().set_limit(size=12 GiB)` — 넘으면 우리가 먼저 멈춘다 (다) 문턱 9,000 → 14,000 MiB (상한 12 GiB + CUDA 문맥). kgy 에서 다른 프로세스가 6.3 GB 쓰는 채로 빈 메모리 약 18,200 MiB → 통과. [두 호출 = CuPy 공개 API · 기억 · GPU 에서 미확인] |
| P3-a cupy 를 늦게 부른다 | gpu_bench_cg.py 250 · 259 줄 | 행렬 만들기 (250 줄) 뒤에 `import cupy` (259 줄) | T6 — cupy 가 없거나 CUDA 라이브러리가 어긋나면 약 1 분 · 호스트 10 GB 를 쓴 뒤에야 traceback 으로 끝난다 | `import cupy` 와 (P2-3 의) 메모리 검사를 245 줄 앞으로 올린다 (§5 의 R5) |
| P3-b 실패할 때 화면에 계정 이름 · 파일에 오류 없음 | gpu_bench_cg.py 408–409 줄 · 블록 2 줄 · notes §4 끝 줄 "멈추면 bench.log 의 마지막 줄을 보낸다" | `sys.exit(main())` · `mkdir "$GBD" && …` | T6: traceback 의 `File "<홈>/gpubench_…/gpu_bench_cg.py"` · T4: `mkdir: cannot create directory '<홈>/…'` = 홈 경로 (계정 이름) 가 화면에 찍힌다. 잡히지 않은 예외는 bench.log · bench.json 에 남지 않는다 (status 'started' 그대로) → 세 파일만 받으면 왜 멈췄는지 모른다. 선택 단계의 오류 글 (339 · 362 · 385 줄 `str(e)[:200]`) 에도 경로가 들 수 있다 | 예외를 받아 홈을 `~` 로 접은 한 줄을 화면 · bench.log · bench.json (status failed) 에 남긴다 (R2 · R8 · R9). 블록 2 줄: `mkdir "$GBD" 2>/dev/null && …` |
| P3-c B · C 에 예열이 없다 | gpu_bench_cg.py 329–331 줄 | B · C 는 바로 잰다 (예열은 A 만 · 307–308 줄) | [기억 · 미확인] C 의 벡터 곱 커널은 처음 쓸 때 컴파일된다 (0.2–1 s) → 500 반복 안에 들어가 A ÷ C 가 몇 % 낮게 나올 수 있다 (기계마다 첫 실행에서만). "한 연산" 재기 (176–183 줄) 도 첫 호출이 시간에 든다 | 331 줄 앞에 `timed_cg(cg_fn, sync, A, bb, Mx, 5)` (버림) · `timed_op` 첫 줄에 `y = fn()` (R6 · R11) |
| P3-d 설명의 숫자 | notes §2-4 "호스트 메모리 10 GB 안쪽" · §5 "약 6.6 GB" | 이 컨테이너의 scipy (1.17.1) 로 잰 값의 환산 | T9 — 기계의 scipy 1.10.1 에서는 381 B/미지수 = **10.1 GB** (+ 파이썬 · CUDA 라이브러리). 16 GB 관문 안이라 돌기는 한다 | "호스트 메모리 약 10–11 GB (scipy 1.10.1 · Python 3.8 로 잰 381 B/미지수의 환산 · 추정)" |
| P3-e "새 폴더에만 쓴다" | gpu_bench_cg.py 20 줄 · notes §2-2 · 본문 D "새 폴더 하나에만 쓴다" | Writes only inside --out | [기억 · 미확인] CuPy 는 컴파일한 커널을 홈의 캐시 폴더 (`.cupy/kernel_cache`) 에 쓴다 — 벤치만 쓰는 연산 (비교 · 벡터 곱) 의 커널이 거기 더해질 수 있다. 리포 scripts 폴더에 그 폴더를 읽는 지문 · 관문은 없다 (낱말 훑음 0 건) → 해는 없지만 문장은 틀린다 | 블록의 python3 앞에 `CUPY_CACHE_DIR="$GBD/cupy_cache"` (캐시도 새 폴더 안 · 첫 반복들이 컴파일로 수십 초 느려지나 예열에서 버린다) — 아니면 문장을 "스크립트는 새 폴더에만 쓴다 · CuPy 가 자기 캐시 폴더에 커널을 더할 수 있다" 로 |
| P3-f 벽시계 상한이 없다 | 블록 413 줄 | `python3 "$GBD/gpu_bench_cg.py" …` | 반복 수는 예열 속도로 정한다 (310 줄) → 예열 뒤 경합이 커지면 그만큼 길어진다 (끝은 난다 · 반복 수가 정해져 있음). 멈춘 nvidia-smi 는 20 s 뒤 놓는다 (49–53 줄 · 확인) | (선택) `timeout 3600 python3 …` |
| P3-g 경합 기록이 표본 하나 | gpu_bench_cg.py 229–231 줄 · notes §3 | 시작 전 nvidia-smi 한 번 | 실측: 우리 풀이 전 다른 프로세스의 gpu_util 은 73–92 % 로 흔들렸다 (표본 453 · 평균 84). 한 번 읽은 값으로는 "busy / alone" 을 못 박는다. 도는 동안의 gpu_util 은 우리 몫이 섞여 100 % 로만 보인다 | 시작 전 5 번 (1 s 간격) 을 남긴다 (R5a). kgy_busy 는 몇 분 간격으로 **두 번** 돌려 s 의 흔들림을 본다 (설명 §2 에 한 줄) |
| P3-h 이름표 줄 | 블록 1 줄 | `GBL=kgy_busy` | T5 — 이름표에 공백을 넣으면 그 줄이 실패하고, 셸에 앞서 붙여 넣은 GBL 이 남아 있으면 **옛 이름표로 돈다** (빈 셸이면 "label must use…" 로 멈춤) | 설명 §2-1 에 "이름표는 영문 · 숫자 · 밑줄만 · 공백 없음" 한 줄 |

## 4. 재는 것이 맞는가

| 물음 | 답 | 근거 |
|---|---|---|
| 시간 재기 앞뒤 동기화 | 한다 | 165 · 172 줄 `sync()` = `cp.cuda.Device().synchronize` (268 줄). [기억] CuPy 의 cg 는 반복마다 잔차를 호스트에서 견줘 어차피 반복마다 동기화된다 |
| 예열을 빼는가 | A 는 뺀다 (20 반복 두 번 · 307–308 줄) · B · C · 한 연산은 안 뺀다 | P3-c |
| 호출이 생산과 같은가 | 같다: CSR float64 올리기 (271 ↔ `scripts/step3_sigma.py` 570 줄) · b (272 ↔ 571) · `diags(1/대각)` (273–274 ↔ 572) · `cg(…, tol, maxiter, M, callback)` (168 ↔ 575) · 새 판 이름 바뀜 처리 (169–171 ↔ 576–578) | 줄 대조 |
| 다른 곳 | ① tol 0 (정해진 수만) ↔ 1e-12 ② 미지수 26,463,592 ↔ 26,529,223 (99.75 %) ③ 행마다 6.98 칸 ↔ 실제 [미확인 — 묶음에 nnz 없음] ④ 고른 띠 행렬 ↔ 고르지 않은 행렬 (접합 간선 · 멤버십 미지수) ⑤ **정렬 안 된 CSR ↔ canonical** (P2-1) ⑥ x0 없음 (ⓒ 는 x0 를 준다 · 573 줄) ⑦ 올리기 · 내려받기 (570–572 · 582 줄) 는 재지 않는다 | |
| 화면에 찍히는 것 | 만든 행렬 (n · nnz · 초) · 예열 속도와 A 반복 수 · A / B / C 의 반복당 초 · 비교 · 한 연산 · `DONE … A 0.0xxxx s per iteration` · `rc N - send back the three files in ~/gpubench_…` | T2 |
| 돌려보낼 것 | 새 폴더의 bench.json · bench.log · gpu_samples.tsv (GPU 길에서만 생긴다). 멈췄으면 화면 글도 (지금 판은 오류가 파일에 없다 · P3-b) | |

**kgy 의 두 번 (경합 / 혼자) 의 비를 s 로 옮기는 데 필요한 가정** (설명 §4 에 일부만 있다)

1. 벤치 때 다른 프로세스의 GPU 부하 = ⑥ 때의 부하 (⑥ 때 = 우리 풀이 전 gpu_util 73–92 % · 메모리 6.3 GB). 벤치의 시작 전 표본으로만 견줄 수 있다.
2. 반복 한 번의 GPU 일 구성이 실풀이와 같다 (같은 호출 · 미지수 99.75 %) — 행 길이 · 번호 배치가 달라 [미확인].
3. s 는 GPU 풀이 시간 (주 풀이 13,245 s + ⓒ 4,095 s · 관찰) 에만 건다. 준비 4,567 s · 증서 CPU 약 400 s 에는 걸지 않는다 (다른 프로세스가 CPU 도 쓰는지는 [미확인]).
4. 벤치 = 2 분 안팎 · 실풀이 = 몇 시간 → 열 · 클럭 상태가 다를 수 있다 [미확인].
5. "혼자" = 다른 계산 프로세스가 없다 (시작 전 표본의 사용 메모리 · gpu_util 로 확인).
6. 한 번씩 잰 값의 흔들림을 모른다 → busy 를 두 번.
7. R 을 도는 몇 주 동안 kgy GPU 를 정말 혼자 쓴다 (운영 가정 · 벤치가 보증하지 않는다).
8. gabia ÷ kgy_alone 은 GPU 풀이의 비일 뿐이다 — 준비 (CPU) 의 기계 비는 이 벤치로 안 나온다 (설명 §4 에 적혀 있음 · 맞다).
9. 경합 크기는 날마다 다를 수 있다 — 옛 기록 한 줄: 같은 GPU 에서 다른 작업이 12.4 GB 를 쓰던 날 반복 한도 30,000 번이 3,054 s 걸렸다 (`docs/reviews/sdcp_sigma_e_dcp_anchor_registration_v2_20261019.md` 169 · 173 줄 → 반복당 약 0.10 s [추정 — 그 3,054 s 가 풀이만의 시간이라고 볼 때] · 이번 ⑥ = 0.048 s · 미지수는 비슷). 그래서 kgy_busy 한 번의 값을 "⑥ 때의 경합" 으로 읽으려면 가정 1 의 대조가 꼭 필요하다.

덤 (제안본의 R7): A 를 두 번 돌린 대조군은 "같은 프로세스 안에서 GPU 풀이가 비트까지 되풀이되는가" 의 첫 기록도 된다 — R 사슬의 no-op 대조 (`scripts/rint_r_chain.py` 6182 줄 · 두 런의 σ 가 float 로 같아야 한다) 가 기대는 성질이다 (합성 행렬 · 한 프로세스 안 · 200 반복이라는 한정).

## 5. 고칠 글 (리뷰 제안본 — CPU 길에서만 시험 · GPU 길 미확인)

- 고친 스크립트 = (리뷰 조수의 제안 폴더 · 리포 밖 — 반영된 판 = docs/reviews/rint2_time_reestimate_20261111/bench/ 의 블록 셋) gpu_bench_cg.py (md5 6bbaa06e8f334d485d2da70262d08679)
- 원본과의 차이 = (리뷰 조수의 제안 폴더 · 리포 밖 — 반영된 판 = docs/reviews/rint2_time_reestimate_20261111/bench/ 의 블록 셋) fix.diff (184 줄)
- 그 스크립트로 만든 블록 = (리뷰 조수의 제안 폴더 · 리포 밖 — 반영된 판 = docs/reviews/rint2_time_reestimate_20261111/bench/ 의 블록 셋) gpu_bench_block.txt (473 줄 · 23,741 B · 느낌표 · 탭 · CR 0)
- 고침을 적용하는 도구 = (리뷰 조수의 제안 폴더 · 리포 밖 — 반영된 판 = docs/reviews/rint2_time_reestimate_20261111/bench/ 의 블록 셋) apply_fix.py (원본을 읽기만 한다 · 패턴마다 정확히 한 번 맞아야 한다)

| # | 원본 줄 | 바꿔 넣을 글 | 닫는 문제 |
|---|---|---|---|
| R1 | 155 줄 `return L, b, diag` 앞 | `L.sum_duplicates()` | P2-1 |
| R7 | 349 줄 `cmpd = {…}` 뒤 | `x1b, _i1b, n1b, _s1b = timed_cg(cg_fn, sync, A, bb, M_a, k)` → `cmpd['A_vs_A_again'] = {'identical': bool(xp.array_equal(x1, x1b)), 'max_abs_diff': float(xp.max(xp.abs(x1 - x1b))), 'iters': [n1, n1b]}` + log 한 줄 + `del x1b` | P2-2 |
| R3 | 197 줄 | `--min-free-gpu-mib` 기본 14000 · 새 인자 `--gpu-cap-gib` 기본 12.0 | P2-3 |
| R5 | 229–231 줄 · 244 줄 앞 · 259 줄 | 시작 전 표본 5 번 → (호스트 검사 뒤) `import cupy as cp` → `free_b, total_b = cp.cuda.Device().mem_info` → 빈 메모리 < 문턱이면 STOP (rc 2) → `cp.get_default_memory_pool().set_limit(size=cap_b)` → 그 뒤에 sampler · 행렬 만들기. 259 줄의 늦은 import 는 뺀다 | P2-3 · P3-a · P3-g |
| R2 · R8 · R9 | 35 줄 뒤 · 339 · 362 · 385 줄 · 408–409 줄 | `fold()` (홈 → `~` · 300 자) · 오류 글에 `fold(e)` · `safe_main()` (예외 → `FAILED at script line N - 종류: 글` 을 화면 · bench.log · bench.json status failed 로 · traceback 없음 · Ctrl-C 는 `[gb] interrupted` 한 줄) | P3-b |
| R6 · R11 | 331 줄 앞 · 176 줄 뒤 | `timed_cg(cg_fn, sync, A, bb, Mx, 5)` (버림) · `timed_op` 첫 줄 `y = fn()` | P3-c |
| 블록 2 줄 | `mkdir "$GBD" && GBOK=1 …` | `mkdir "$GBD" 2>/dev/null && GBOK=1 …` | P3-b |
| 블록 끝 줄 | `. "$HOME/dem-venv/bin/activate" && python3 "$GBD/gpu_bench_cg.py" …` | `. "$HOME/dem-venv/bin/activate" && CUPY_CACHE_DIR="$GBD/cupy_cache" timeout 3600 python3 "$GBD/gpu_bench_cg.py" …` (md5 값도 새 스크립트 것으로) | P3-e · P3-f |

- 스크립트를 한 글자라도 바꾸면 md5 가 바뀐다 → 블록은 `_make_block.py` 로 다시 만든다 (끝 줄의 md5 · 설명 파일의 md5 · 줄 수도 같이).
- 설명 파일에 더할 줄: P3-d 의 호스트 메모리 · P3-h 의 이름표 · "kgy_busy 는 두 번" · §4 의 가정 1 · 3 · 4 · 6 · 7 · "A_vs_A_again 이 False 면 B · C 의 identical 은 해석하지 않는다".
- 제안본의 문턱: 빈 GPU 메모리 14,000 MiB 미만이면 멈춘다 (rc 2 · 아무것도 올리지 않음). 다른 프로세스가 10 GB 넘게 쓰는 날은 여기서 멈춘다 → 그때는 블록 끝 줄의 python3 인자에 `--min-free-gpu-mib 9000 --gpu-cap-gib 8` 을 덧붙인다 (끝 줄은 md5 관문 밖이라 고쳐도 된다).
- 고치지 않고 급히 돌릴 때의 읽는 법: A 의 per_iter_s 만 쓴다 · compare · ops · B · C 는 참고 · 멈추면 화면 글을 그대로 받는다 (계정 이름이 든 줄은 지우고).

## 6. 확인하지 못한 것

| 무엇 | 까닭 |
|---|---|
| GPU 길 전체 (원본 · 제안본 모두) — 실제로 도는지 · GPU 메모리 최대 · 걸리는 시간 | 이 컨테이너에 GPU · cupy 없음 |
| CuPy 12.3.0 의 내부: cg 가 CSR 행렬에 빠른 곱 길을 쓰는지 · 대각 (DIA) 전처리를 반복마다 CSR 로 바꾸는지 · CSR 곱이 canonical 이 아니면 정렬하는지 · 커널 캐시 자리 | 소스 없음 · 기억뿐 → 표의 해당 칸은 [기억 · 미확인] |
| GPU 희소 곱이 실행마다 비트 같은 값을 내는지 | 같음 (P2-2 의 대조군이 이것을 벤치에서 직접 보게 한다) |
| 제안본의 `mem_info` · `set_limit` · `CUPY_CACHE_DIR` 이 12.3.0 에서 그 이름 · 뜻 그대로인지 | CuPy 공개 API 로 기억 · GPU 에서 미확인 → 첫 실행에서 `FAILED at script line …` 이 나오면 그 줄을 보면 된다 |
| 실제 행렬의 nnz · 행 길이 분포 | ⑥ 묶음에 없음 (팔 JSON 은 열지 않는다) |
| 큰 붙여넣기 (20 KB) 가 1저자 단말에서 온전히 들어가는지 | 단말마다 다름 — 깨지면 md5 관문이 막는다 (T5) |

## 7. 맞다고 확인한 것

| 무엇 | 근거 |
|---|---|
| 블록이 만드는 것 = 홈 아래 새 폴더 하나 (`gpubench_이름표_UTC시각`) 와 그 안의 파일 | T1–T5 · 스크립트의 쓰기 = `--out` 안 bench.json (.part 뒤 바꿔치기) · bench.log · gpu_samples.tsv 뿐 (209–221 · 244 줄) |
| 이미 있는 폴더면 돌지 않고 있던 것을 건드리지 않는다 | T4 (셋) · 스크립트도 `--out` 에 다른 파일이 있으면 멈춘다 (206–208 줄) |
| 킷 · R 출력 · 탐침 로그 폴더 · 잠금 파일을 읽지 않는다 | 스크립트가 여는 것 = `/proc/meminfo` · nvidia-smi · `--out` 안 파일뿐 (전 줄 읽음) |
| 네트워크 · sudo · 패키지 설치 · git 없음 | 블록 · 스크립트 전 줄 |
| md5 관문 | T5 열 가지 전부 안 돎 · 블록에서 꺼낸 스크립트 = 원본과 바이트 같음 (md5 d2528f45…) · `bash -n` 통과 · 느낌표 · 탭 · CR · 비 ASCII 0 · 가장 긴 줄 540 자 |
| venv 는 괄호 셸 안에서만 켠다 (1저자 셸에 남지 않는다) · 두 기계 모두 venv = 홈의 dem-venv · cupy 12.3.0 · Python 3.8 · numpy 1.24.4 · scipy 1.10.1 | 블록 413 줄 · `docs/data/rint2_siteq_20261109/kgy/siteq_result.json` · `docs/data/rint2_siteq_20261109/gabia/siteq_result.json` |
| 정상 길에서는 화면 · 파일에 홈 경로 · 계정 이름이 없다 | T2 · T3 의 화면 · bench.json · bench.log 낱말 훑음 0 건 (화면의 폴더는 `~/gpubench_…`) |
| 호스트 메모리 관문 (여유 16 GB 미만이면 만들기 전에 멈춤) | T7 |
| 24 GB GPU 에 다른 프로세스 6.3 GB 인 채로 관문 통과 | 24,576 − 6,325 = 18,251 MiB ≥ 9,000 (원본) · ≥ 14,000 (제안본) |
| nvidia-smi 를 GPU 0 번으로만 읽는 것이 두 기계에서 맞다 | 두 기계 GPU 하나씩 (siteq 기록의 gpu 목록 한 줄) · kgy 의 CUDA_VISIBLE_DEVICES = unset (`docs/data/rint2_probe6_a2_20261111/meta.txt`) · gabia 의 그 변수는 [미확인] |
| 합성 행렬 = 대칭 · 대각 양수 · 미지수 26,463,592 · nnz 184,712,320 (행마다 6.98) | T9 의 작은 크기에서 대칭 오차 0 · 대각 > 0 · 손 계산 (7n − 6·298²) |
| 생산 GPU 풀이의 줄 번호 (565–582) · 전처리 = 대각 하나 | `scripts/step3_sigma.py` 565–582 줄 |
| 실측 미지수 26,529,223 · 주 풀이 반복당 약 0.0477 s | `docs/data/rint2_probe6_a2_20261111/probe6_screen.txt` · samples.tsv (gpu_util 100 % 구간 4,567–17,807 s ÷ 277,885) |
