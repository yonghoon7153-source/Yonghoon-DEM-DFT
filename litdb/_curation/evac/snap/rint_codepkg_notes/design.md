# Rint ② 코드 묶음 설계 메모 — Q11 전처리 C 꼴 + Q2 탄소 접합 원장 저장본 (11-12 · 조수 · 코드 전)

- 바탕 = 작업 트리 `11a794674` (detached) · 줄 번호 = 그 커밋.  지위 = 설계 (결과 0 건 · GPU · 킷 · σ 없음).
- cupy 12.3.0 소스 (github raw · 데이터로만 읽음 · `codepkg/cupy_src_v1230/`) 대조: `cg` = `_iterative.py` 14 줄 (`tol=` 만 · `rtol=` 없음) ·
  `_make_system` 339–349 (M 이 csr 이면 빠른 spMV · 아니면 `aslinearoperator`) · dia → `MatrixLinearOperator` → 기본 `_matvec` = `matmat(x.reshape(-1,1))`
  → `dia.dot` → `__mul__` = `tocsr()` = `tocsc().tocsr()` (`_dia.py` 140–190) — **적용할 때마다 변환** (요소 커널 + cumsum + 마스크 색인 + 전치) 뒤 CSR×(n,1).
  벤치의 "반복 시간 약 75 % = 전처리 A 적용" 의 기전 = 이것 (README E-2 8 번의 [미확인] 가설 → 소스로 확인).

## (가) Q11 — GPU 길 전처리 표현만 (Jacobi · 같은 수 · 같은 정지)

| 정할 것 | 결정 | 근거 |
|---|---|---|
| 바꿀 자리 | `scripts/step3_sigma.py` `_solve_cg` GPU 길 572 줄 한 곳: `Mg = cxs.diags(1.0 / cp.asarray(diag))` → `_dinv = 1.0 / cp.asarray(diag)` · `Mg = LinearOperator(Lg.shape, matvec=lambda r: _dinv * r, dtype=np.float64)` (벤치 C 꼴 그대로 · `gpu_bench_cg.py` 302–306) | 575 · 578 두 호출 (`tol=` · `rtol=`) 이 같은 `Mg` 를 쓴다 → 두 길 다 바뀐다 · x0 (573 · ⓒ) · callback (555–559 · CONV_CERT) 은 손대지 않는다 |
| CPU 길 | **안 바꾼다** (596–602) | R 은 GPU 필수 (러너 EXPECT_BACKEND gpu · REQUIRE_GPU) · scipy dia matvec 은 변환 없이 바로 곱한다 · 바꾸면 기존 CPU 비트 대조 시험의 범위만 늘어난다 |
| `LAST_BACKEND['precond']` | **'jacobi' 그대로** (579) | 읽는 곳: `sr01_stamp_compare.precond_of` (팔 짝 대조 · 182–195) · `ca_ext_svcf` 198 (기록 복사) · `sdcp_gain_verdict` (게이트 아님 · 542) · 시험 기대값 다수 ('jacobi') — 종류는 그대로 Jacobi 라 글자를 바꾸면 옛 · 새 팔이 "전처리 다름" 으로 갈린다 |
| 새 기록 키 | **넣지 않는다** (매니페스트 · LAST_BACKEND 바이트 그대로) | C 꼴의 증명 = ① 코드 신원 (봉인 핀 · 사슬 CODE_FILES sha · S0 일곱 파일 지문 — GPU 길은 C 꼴 하나뿐 · 스위치 없음) ② 가짜 cupy 시험 (넘긴 M = 벡터 곱 연산자) ③ GPU 확인 블록 (A ↔ C 해 · 반복 · info 비트) |
| 함정 | 연산자 matvec 은 **늘 새 배열**을 내야 한다 — cupyx cg 72 줄 `p = z` (첫 반복 별칭) · 제자리 버퍼를 돌려쓰면 다음 반복에 p 가 덮인다 | 시험 + 변이 (제자리 버퍼 꼴 → 해가 달라져 시험이 잡는지) |
| 부호 있는 0 | dia→CSR 경로는 합을 +0 에서 시작할 수 있어 r = −0 자리에서 A 는 +0 · C 는 −0 을 낼 수 있다 — 그런데 b = `np.zeros` + 양수 (`_plate_couple` 2284–2286) 이고 r 은 −0 이 될 수 없다 (r − αq 의 정확 상쇄 = +0) | 시험은 값 같음과 **바이트 같음**을 따로 센다 · GPU 블록도 둘 다 적는다 |

## (나) Q2 — 탄소 접합 원장 저장본 (원장만 · 계획은 팔마다)

| 정할 것 | 결정 | 근거 |
|---|---|---|
| 무엇을 | 원장 dict 전체 (`cjunc_registry` 반환 · 지문 `fp` 포함) — 계획은 R_j · 법칙 · c · SV 노브에 달려 팔마다 그대로 만든다 | `ca_ext_cjunc.payload_prepare` 226 (원장) · 238–240 (계획) · README A-2 표 |
| 꼴 | 한 파일 `cjreg_<열쇠 sha256>.npz` (`np.savez` · 읽기 = `allow_pickle=False` · 코드 실행 없음): `header` (JSON) · `skeleton` (형 표지가 붙은 트리 JSON — dict 키 차례 · list/tuple · Python/numpy 스칼라 형 · 실수 = 8 바이트 hex · 객체 배열 원소) · 배열 (dtype · 모양 · 바이트 그대로) | 원장 안 형 (조사): dict · list (int64 배열의 목록 `pair_i` · `seg_i` · `self_A` …) · 객체 배열 (`reason` = str) · tuple (`shape`) · int · float · str · None · bool 배열 — numpy 2 는 numpy 스칼라 repr 이 다르다 (`_fp` 48 줄 · 448 줄) → 형까지 보존해야 지문이 같다 |
| 결속 (열쇠) | 저장 꼴 판 · `CJUNC_MODEL_VERSION` · `CJUNC_SCHEMA` · 코드 파일 sha256 (`carbon_junction.py` · `step3_sigma.py` (`_grid_fp`) · `cjunc_store.py` = 실제 불러온 모듈 파일) · 환경 단위 (`run_contract.env_unit_now` = python 부 판 · numpy · scipy) · 기계 지문 (`/etc/machine-id` 의 blake2b — 못 읽으면 저장본 끔 = 매번 짓기 · 기록) · sid 격자 지문 (`_grid_fp`) · lo · vox (실수 비트) · 입력 넷 (pts · phase · fid · kind 를 `_input_check` 꼴 float64/int64 로 · 모양 · 바이트) · 문턱 10 칸 (비트 · None) | 원장 입력 = `cjunc_registry(sid, lo, vox, pts, phase, fid, kind, **문턱)` (701–733) · README E-2 4 번 ④ "PTFE · SDCP 점을 묶는 지문이 없다" → 입력 넷 지문으로 닫는다 |
| 자리 | 사슬 새 선택지 `--cjunc-store <절대 경로>` (ladder · predict 만 · 없으면 끔 = 옛 거동) — 기계마다 캠페인 바탕 아래 폴더 하나 (운영자가 umask 022 셸에서 만든다 · 0755) · 시도 · 런 폴더 밖 (시도 사이 재사용 · 재실행 복사와 무관) · 파일 0444 | [남은 계획] §2-3 A1 · A5 (umask · 단일 작성자) · 사슬은 런마다 빈 폴더 (5652 · 5735) |
| 단일 작성자 | 임시 파일 (O_EXCL · 0600) → fsync → chmod 0444 → `os.link` (먼저 쓴 쪽이 이김 · 덮어쓰기 없음) → 폴더 fsync | `rint_r_chain.write_json_atomic` 꼴 + 덮어쓰기 금지 |
| 누가 | 짓고 쓰고 읽음 = 생산 팔 런 (사다리 · 끝 origin · SBE origin · no-op · DBE 모서리 · DBE origin · 넘침 origin8 — `Runner` · `ResumeRunner`) · **읽지 않음** = 봉인 원천 (`RunnerGraphSource` · 판정 · 다시 판정 · 합치기) · S0 단계 | 봉인 원천의 몫 = 독립 재조립 대조 (README E-2 4 번 "같은 저장본을 읽으면 독립성이 준다") · 판정 단계는 GPU 팔 마감 밖 (1저자 11-12 Q9) → 그 이득 (40–118 h) 은 버린다 |
| 막는 겹 | ① 사슬: `RunnerGraphSource` env 에 넣지 않고 지운다 ② 러너: `CJUNC_GRAPH_ONLY=1` + `CJUNC_STORE` = ABORT · `CJUNC=1` 없이 = ABORT · 절대 경로 · 허용 글자 · 폴더 있음 ③ payload: `--step3-cjunc-graph-only` + `--step3-cjunc-store` = 거부 · `--step3-cjunc` 없이 = 거부 · 폴더 없음 = 거부 | 세 겹 (시험 각각) |
| 상태 · 처분 | 없음 → 짓고 쓴다 · 적중 → 읽는다 · **못 읽음** (0 바이트 · 잘림 · zip/CRC · 멤버 없음 · JSON · 복원 예외 · 모르는 꼴 판) = 정직한 흐름 (끊긴 복사 · 디스크) → 다시 짓는다 · 그 파일은 두고 · 덮어쓰지 않고 · ⚠ 줄 + 기록 · **어긋남** (머리 열쇠 ≠ 지금 열쇠 · 파일 이름 ≠ 머리 열쇠 · skeleton sha ≠ 머리 · 읽은 원장의 엄격 지문 ≠ 머리 · 원장 지문 재계산 ≠ 기록 · sid 지문 ≠) = 손으로 고친 · 어긋난 기록 → **멈춤** `S2_CJUNC_STORE\|INCONSISTENT\|` (payload rc ≠ 0 → 사슬 RUNNER_RC) · 같은 열쇠 동시 쓰기 (link EEXIST) → 남의 파일을 읽어 엄격 지문 같으면 통과 · 다르면 멈춤 (같은 입력 두 원장 다름 = 비결정 또는 열쇠 결함) · 다른 기계 · 다른 코드 · 다른 침대/격자/origin/문턱 = 열쇠가 달라 없음 → 짓는다 · 쓰기 실패 (공간 · 권한 · link 미지원) = 기록만 (팔 결과 무관) · 쓰기 전 여유 < 2 × 크기 + 1 GiB = 쓰지 않음 | CLAUDE.md 재개 규칙 지적 처분 기준 (정직한 흐름 = 틀린 결과를 받지 않게 · 손으로 고친 · 어긋난 기록 = 멈춤) |
| 비트 같음 보증 | ① 같은 기계 · 환경 · 코드에서 원장 함수의 결정성 (봉인 원천 재조립 대조 · 재실행 바이트 대조가 이미 기대는 가정과 같다) ② **엄격 지문** — 쓰는 쪽이 짓자마자 메모리의 원장 전체 (노드마다 형 이름 · dtype · 모양 · 바이트 · dict 키 차례) 를 해시해 머리에 적고, 읽는 쪽이 복원한 원장을 같은 함수로 해시해 같아야 쓴다 (직렬화기가 틀려도 잡는다) ③ `registry_fp` 재계산 = 기록 ④ 시험: 저장본 켬 · 끔 · 적중 · 빗나감의 팔 JSON 이 **바이트 같음** | — |
| 기록 | 팔 JSON (`p2_*.json`) · 매니페스트 · 옆 파일에 **아무것도 싣지 않는다** — 재실행 대조 (`ResumeRunner` 5741–5747: 남은 payload 바이트 대조) 가 원 시도 = 빗나감 · 재실행 = 적중일 때 깨지지 않게 · 옆 파일은 `.unchecked` · read_run · 재실행 복사 규칙을 건드린다 → **화면 한 줄만** (`cjunc_store.outcome_line` · probe6 FAIL_MARK 낱말 없음 · 경고 다섯 상태만 ⚠) · 사슬 요약 = `cjunc_store: True` (켬일 때만 · 끔 = 칸 없음 = 옛 바이트) · CLI 회계 = `mode` · 사슬 CODE_FILES += `cjunc_store.py` · 규율 검사기 `_RUNNER_AXES` += `CJUNC_STORE` (`RUNNER_CA_EXT_ENV` 는 그대로 — 영수증 · digest 밖) | 매니페스트 키 0 · 영수증 · OUTDIR · 팔 이름 그대로 |
| S0 단계 1 다시 | **필요** — 고칠 자리 `step3_sigma.py` (Q11) · `mpm_webapp_payload.py` (Q2 배선) 가 둘 다 S0 일곱 파일 안 (`rint_r_chain.S0_SAME_FILES` 344–345) · `carbon_junction.py` 는 안 바꾼다 | CPU 약 1.5 h · kgy (실측 5,383 s) |
| ⑥ 시도 3 | 탐침 도구 (`run_probe6.sh` 58–66 · 434 줄 env 고정 · CJUNC* 지움) 는 저장본 env 를 안 준다 → 도구 그대로면 시도 3 = 저장본 끔 · C 꼴 풀이 시간만 잰다 · 쓰기 · 읽기 비용은 R 의 첫 두 팔 (바닥 = 빗나감 · 천장 = 같은 원장 적중) 에서 처음 나온다 — 시도 3 에서 재려면 도구 고침 (원장 줄 둘) | 1저자 · 본 세션 몫 (개정 초안 §3) |

- 시험 고리 (단원 시험이 바꿔 끼우는 이름 · 모듈 전역): `_statvfs` (여유) · `_link` (발행) · `_write_zip` (쓰기) — 생산 동작 그대로.
- 못 읽음 ↔ 어긋남 경계: **CRC 로 확인한 멤버 바이트를 손에 넣기 전** 의 실패 (없음 · 0 바이트 · zip 꼴 · 멤버 집합 · CRC) = 못 읽음 (다시 짓기) · 그 뒤 (머리 JSON · 꼴 판 · 열쇠 · 뼈대 sha · 복원 · 엄격 지문 · registry_fp · sid 지문 · 심볼릭 링크 · 폴더) = 어긋남 (멈춤).

## (다) 개정 문장 초안 = `codepkg/amend_drafts.md` · (라) GPU 확인 블록 = `codepkg/gpu_check_block.txt` (설계 · 결과 전 기대 = 그 파일 머리)

## (마) 대피 세션 덧붙임 (11-12 · 이어받은 조수 · 구현 커밋 전 고침 — 위 표의 해당 칸을 이 절이 고친다)

| 칸 | 넘겨받은 설계 · 구현 | 고친 것 | 까닭 (근거) |
|---|---|---|---|
| 꼴 — 별칭 | 같은 객체가 두 자리 = `Unsupported` (저장 안 함) | **받는다** — 변하는 객체 (ndarray · dict · list) 를 처음 만난 차례로 번호를 매기고 다시 만나면 되가리킴 (뼈대 `['r', 번호]` · 엄격 지문 `b'R'` + 번호) · `decode` 가 같은 차례로 같은 객체를 그 자리에 둔다 | `carbon_junction._merge_instances` 1620–1621 줄 = `[np.zeros(0)] * nI` → instance 가 둘 이상인 원장은 **늘** 별칭이 있다 → 넘겨받은 판은 실침대 (SBE instance 117,583 · `docs/data/rint2_s0_sbe_20261108`) 에서 저장본을 영영 쓰지 못한다 (built_write_skipped · Q2 이득 0).  픽스처 넷 · b6 · e2e 킷이 모두 instance 1 개라 시험이 못 잡았다.  `carbon_junction.py` 는 안 바꾼다 (원장 코드 그대로). |
| 꼴 — 메모리 겹침 | 배열 쌍마다 `np.shares_memory` (n²) · 객체 배열은 안 봄 | 주소 구간 `[자료 주소, + nbytes)` 정렬 뒤 앞 구간 끝과 견줌 (n log n) · 객체 배열도 봄 | 실침대 원장 = instance 마다 작은 배열 넷 (seg_i · seg_j · self_A · self_B) ≈ 47 만 배열 → n² 는 끝나지 않는다.  받는 배열이 연속 (C · F) 뿐이라 구간이 정확하다. |
| 그릇 | (그대로) zip STORED · 멤버 = 머리 · 뼈대 · a<i>.npy | 그대로 — 멤버 > 65,535 (zip64 끝 기록) 를 시험 (T13c 12 만 멤버 · 쓰기 2.5 s · 읽기 6.6 s) | 어림 [추정]: 47 만 멤버 = 쓰기 약 10 s · 읽기 약 26 s + 큰 배열 해시 — 짓기 4,040 s 에 견주어 작다.  묶어 싣기 (작은 배열 한 멤버) 는 넣지 않았다. |
| 처분 — 쓰기 쪽 뜻밖의 예외 | `Unsupported` · `OSError` · 발행 전 대조 실패만 기록 · 그 밖은 팔로 샘 (ValueError 면 payload 가 `S2_CJUNC_REFUSED\|PLAN\|` 으로 오인) | 싣기 · 발행의 모든 예외 (메모리 부족 포함) = `built_write_failed` (기록만 · 임시 파일 지움) — `StoreInconsistent` (같은 열쇠 다른 원장) 만 올린다 | "쓰기 실패 = 팔 결과 무관" 을 예외 형에 기대지 않게. |
| 처분 — 읽기 내용 단의 뜻밖의 예외 | 일부 형만 어긋남으로 · 나머지는 팔로 샘 | CRC 를 지난 뒤의 모든 예외 = 어긋남 (`StoreInconsistent` code content · 멈춤) · `MemoryError` 만 그대로 올린다 (자원) | 발행된 파일은 쓰는 쪽이 같은 길로 읽어 봤다 → 여기서 걸리면 그 뒤에 바뀐 것. |
| 쓰기 — 걸음 수 | `strict_digest` + `encode` (두 번) | `encode_strict` (한 번) · 발행 전 대조 사본은 발행 전에 놓는다 | 큰 원장의 해시 · 메모리. |
| 자리 어림 | 멤버당 4096 B | 512 B | 47 만 멤버 × 4096 = 1.9 GB 헛 어림 (자리 검사가 헛되이 건너뜀). |
| 시험 | T3 = "별칭 = 거부" | T1 (원장 F5 · 조밀 침대 둘 · 별칭 모둠 · 고리 · 별칭 서명) · T2 (별칭 ↔ 사본 지문) · T3 (보기 겹침 · 객체 배열 겹침) · T5f · g · h (instance 여럿 · 팔 여덟이 저장본 하나 · 원장 지은 횟수 1 · 문턱 다른 팔 = 다른 열쇠) · T6 (npy 머리 = CRC 가 먼저) · T7 (뼈대 바이트만 · 배열 뒤 남는 바이트 · T7b 뜻밖의 예외) · T11 (뜻밖의 예외 둘 · 있는 상대 폴더) · T13a · b · c (규모) · P5 (세 가닥 직렬 payload) · C1 (합치기 · 허용 밖 글자 · 갈래마다 사유 글) | 시험 먼저 커밋의 T3 기대 (별칭 거부) 를 바꿨다 — 설계가 바뀐 것 (이 절). |
| 시험 — 열쇠 칸 · 폴더 소유자 (대피 4) | T4 가 스키마 칸만 안 바꿈 · Store · 사슬의 폴더 소유자 검사에 시험 없음 | T4 스키마 갈래 · T11 다른 소유자 · C1 여덟째 (root = chown · 아니면 os.getuid 를 잠깐 바꿈) — 커밋 `2f97617ef` (시험만) | 변이 목록 대조에서 빈틈 셋 (K13 · W19 · C10 = 보강 전 시험에서 안 잡힘 → 보강 뒤 잡힘) |

- 한정 (그대로 + 덧): 실침대 원장이 저장 꼴 안인지 (서로 다른 배열의 메모리 겹침 · 읽기 전용 · 비연속 없음) 는 픽스처 · `test_carbon_junction` 의 원장 488 개 (스크래치 왕복) 로만 봤다 — 실침대 첫 팔의 화면 줄 (`새로 지어 저장` 이어야 한다 · `⚠ … 저장 안 함` 이면 저장본이 안 생긴다) 로 확인한다 (S0 뒤 첫 SBE 팔).  실침대 쓰기 · 읽기 시간 · 메모리 (발행 전 대조 = 원장 사본 하나 더) = 미확인.
