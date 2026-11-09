# 회차 ⑤ Codex 탐침 — 우리 트리 재현 (2026-11-09)

- 검토 핀: `abf0911ebc994167ac50132c78207c6c8d4421f1` (가지 `claude/sdcp-dem-manuscript-si-pqwtv8`)
- Codex 증거: `…/scratchpad/in1109r5/x` (읽기만 · 바꾸지 않음)
- 이 폴더: `<스크래치>/in1109r5/repro`
- **결론: 판정값 차이 0.**  다른 칸은 모두 플랫폼 · 실행마다 바뀌는 값이다 (경로 · 시각 · Python 판 · host_ident · Windows CRLF · zip 메타 · 합성 git 커밋).

## 1. 환경

| 항목 | 우리 | Codex |
|---|---|---|
| OS | Linux 6.18.44 x86_64 (glibc 2.39) | Windows |
| Python | 3.11.17 · numpy 2.4.6 · scipy 1.17.1 | 3.12.14 (numpy · scipy 판 기록 없음) |
| 추가 대조 1 건 | 3.8.20 · numpy 1.24.4 · scipy 1.10.1 (s_min 탐침만) | — |
| git | 2.43.0 | — |
| 실행 꼴 | `python3 -I -B -X utf8` · 탐침마다 새 빈 작업 폴더 (`cwd/<탐침>/` · 끝난 뒤에도 비어 있음) | `python -I -B -X utf8` |
| O_NONBLOCK | 리눅스에 원래 있음 → 탐침의 호환 쐐기가 작동하지 않음 (스크립트는 그대로) | `O_NONBLOCK=0` 호환 쐐기 |

`-X utf8` 은 Codex 명령과 맞춘 것이다.  여기 Python 은 원래 UTF-8 모드라 차이가 없다.

## 2. 고정 트리 만들기

```
git -C <리포> archive abf0911ebc994167ac50132c78207c6c8d4421f1 \
    scripts docs/data/rint2_s0_sbe_20261108 docs/reviews/rint2_s0_mem_fix_20261106 | tar -x -C pin/repo
```

- 830 파일 · 31 MB.  임시 worktree 는 쓰지 않았다 (탐침이 git 정보를 요구하지 않음).
- 핵심 파일 sha256 = Codex 기록과 같다: `rint_r_chain.py` 986bbdb3… · `test_rint_r_chain.py` 98480e89… · `carbon_junction.py` 679dbc38… · `fibre_segment_raster.py` e2e94d3b… · `import_s0_tgz.py` 613107b8….
- 핀 커밋의 tree = 661308db21702ab3b344d9ad85194467336ec260 (tree 해시 · 커밋 아님) (판정문 §2 의 원격 tree 와 같음).  Codex ZIP 의 repo 806 파일 blob (input_verification.json) 이 우리 핀 blob 과 806/806 같다.
- 모든 실행 뒤 고정 트리 830/830 blob 그대로 · 덧붙은 파일 0 (`__pycache__` 없음).

## 3. 실행 전 안전 확인

- 다섯 탐침과 회차 ④ 두 판은 **스크립트가 있는 폴더**에 결과를 쓴다 (`probe_results.json` · `raw_audit.json` · `scratch_*` 등).  그래서 증거 폴더를 건드리지 않도록 스크립트를 `runs/<탐침>/` 로 복사해서 돌렸다.  복사본 sha256 = Codex `SHA256SUMS` 의 값과 같다.
- 네트워크 없음 · 저장소 쓰기 없음 · 연구 계산 · 솔버 없음.
- 재개 탐침의 실행기는 `'UNUSED'` + 기한 0 이라 러너를 띄울 수 없다.  recover CLI 는 그룹 기록이 모두 확인된 상태라 프로세스 정리 (kill) 경로를 타지 않는다 (로그: "그룹 기록 0 개 정리").
- 회차 ④ 탐침은 작은 git 원장을 scratch 에 만든다.  이 기계의 전역 git 설정에 `commit.gpgsign=true` (SSH 서명) 가 있어서, 합성 커밋에 서명이 걸리지 않게 `GIT_CONFIG_GLOBAL=<빈 파일>` 로 돌렸다.  사슬 모듈의 원장 커밋은 원래 `commit.gpgsign=false` 와 이름 · 메일을 `-c` 로 준다 → 판정값에 영향 없음.
- S0 TGZ: 24,284,950 B · sha256 `d48f55c1…0a13` 확인 (실행 전후 같음).
- 증거 폴더 그대로: `SHA256SUMS` 205/207 OK (나머지 2 = 일부러 뺀 ZIP · TGZ) · 새 파일 0.

## 4. 탐침별 결과

| # | 탐침 (명령) | rc | 우리 핵심 값 | Codex 값 | 판정 |
|---|---|---|---|---|---|
| 1 | `probe_resume_focus.py pin/repo` | 0 | 26 관측.  원 R1 · R2 · attempt-null · 3 시도 from = writer False + 다음 재개 거부 ([ⓒ] [ⓒ] [ⓐ] [ⓑ]) · 정직 · 양성 8 꼴 = True (정직한 불일치 honest_mismatch 는 False [ⓓ]) · 요약 없는 copied payload · launch 변경 = writer True (요약 있으면 False [ⓒ]) · 원천 이동 = ResultHeld → 되돌린 뒤 True · runs=5 · stop='invalid' = 두 자리 RESUME_NOT_ALLOWED [꼴] | 같음 | **같음.**  화면 출력이 Codex `probe_focus.log` 와 바이트 같다.  JSON 다른 칸 28 = host_ident 3 · platform · python · fixture 경로 23 (플랫폼만).  사유 글까지 같다 |
| 2 | `probe_summaryless_copy.py pin/repo` | 0 | 정상 중단: payload 같음 (b17effb4…) · 요약 absent · groups null · parent_dead · resume_ok true · 다음 order / presolve null / null · `_src_done(L01)` true.  단일 불일치: 복사본 05d7ef10… ≠ 원천 · 나머지 전부 같음 (parent_dead · true · null / null · true) | 같음 (§6-2 표) | **같음.**  다른 칸 6 = folder 경로 2 · utc 2 · folder_sha256 2.  folder_sha256 은 그룹 표지 (절대 경로에서 만든 sha) 와 Windows 로그 CRLF 때문이다 — 이 둘만 바꿔 Codex 값 cb1fa4da… · d5ee8e5b… 를 그대로 다시 만들었다 (`runs/summaryless/digest_rebuild.txt`) |
| 3 | `reproduce_smin_counterexample.py --repo pin/repo --out …` | 0 | 자기 후보 0/0 → 0/0 · 미등록 면 3 → 2 · 같은 조각 융합 면 0 → 1 · SV 성분 0 → 0 (V 만) · 1 → 0 (V+SDCP) · 끊는 SV 면 행 0 → 0 · 2 → 0 · s_face 0.2277607596902182 · d_face 0.058948822334846995 · s_min D/2 · D = 0 과 같음 | 같음 (§8-2 표) | **같음.**  다른 칸 1 = Python 판.  py3.8 + numpy 1.24.4 / scipy 1.10.1 에서도 같음 (추가) |
| 3b | `probe_smin.py` (발견 과정 · 추가) | 0 | 탐색 · 산술 · 원 JSON 대조 | 같음 | **같음.**  다른 칸 1 = Python 판 |
| 4 | `audit_s0_raw.py --repo pin/repo --raw <로컬 tgz>` | 0 | PASS · 18 파일 · 6 출력 · 사본 8 · 코드 7 · NPZ a1d43579… / 7fc40335… (주 117,583 / 117,070 · 보조 151,587 / 45,098) · plan 4da98863… (네 곳 같음) · rc 줄 1079 `rc=0` 하나 · CAP_TERM 0 · 표본 1,077 · 최대 5,694,360 kB (5.4306 GiB) @ t=5379 s · 마지막 표본 5384 s · elapsed 5382.8 | 같음 (§7-1) | **같음.**  다른 칸 1 = tgz 경로 |
| 5 | `probe_import_rc.py --repo pin/repo --out <새 경로>` | 0 | good 0 ADOPT · rc1 / cap / two0 / absent 2 FAILED · wrongfile 0 ADOPT · nonterminal 0 ADOPT (추가 경계 둘 수용) | 같음 (§7-2) | **같음.**  판정 줄 · rc 7/7 같음.  다른 칸 7 = 화면의 README 경로.  출력 121 파일 중 49 가 바이트 다름 = 합성 tgz 의 gzip mtime · 합성 npz 의 zip create_system (Windows 0 / Unix 3) 과 그 sha 를 적은 MANIFEST · NPZ_SHA256 · README 한 줄.  npy 내용 · 나머지 tar 내용은 같음 |
| 6 | 회차 ④ 원 탐침 (무수정 · `RINT_REVIEW_REPO=pin/repo`) | 1 | 181 행 AssertionError | 181 행 AssertionError | **같음** (기대된 실패) |
| 7 | 회차 ④ 기대 변경본 | 0 | 요약 출력 = Codex `run.log` 와 바이트 같음 · recover CLI 넷 모두 rc 0 · resume_ok False (원인 check 1 · timeout 3 · 사유 표지 R1 [ⓒ] · attempt-null [ⓐ]) · 변이 M14 · M18 · M54 = True · M47 = AttributeError | 같음 (§3 끝 문단) | **같음.**  cli 로그 4 개 바이트 같음.  JSON 다른 칸 25 = folder 15 · utc 4 · folder_sha256 4 · scratch 1 · python 1.  우리 두 번째 실행과도 같은 24 칸이 달라졌다 → 실행마다 바뀌는 값 (경로 · 시각 · 합성 원장 커밋).  변경본 = 원본 + 단언 3 줄 (우리 diff = Codex `expectation_only.diff` · CRLF 만 다름) |

모든 다른 칸을 자동으로 분류했다: 9 개 비교 모두 플랫폼 · 실행 값 밖의 칸 0 (`runs/*/deepcmp*.txt`).

## 5. 못 한 것 · 안 한 것

- `audit_root.py` · `verify_input.py`: §9 목록 밖이고 ZIP (`package/repo`) 이 필요하다 → 돌리지 않았다.  대신 핀 tree id 와 806 blob 을 대조했다 (§2).
- Codex 와 같이 합성 · 함수 수준 재현이다.  실제 flock · SIGKILL · NFS · 다른 기계 자격 검증이 아니다.  회차 ④ 탐침의 직렬 lock 대체 · 죽은 부모 모의는 스크립트 그대로 두었다.
- 실 S0 재계산 · σ 풀이 · 연구 계산은 하지 않았다.

## 6. 파일

- `pin/repo/` 고정 트리 · `pin/PIN.txt`
- `runs/<탐침>/` 복사한 스크립트 · `stdout.log` · `stderr.log` · `rc.txt` · 결과 JSON · `deepcmp*.txt`
- `runs/summaryless/digest_rebuild.txt` (Codex folder_sha256 재구성)
- `runs/r4_adjusted_rerun/` (실행마다 바뀌는 칸 확인용 두 번째 실행)
- `tools/deepcmp.py` · tools/rebuild_codex_digest.py (스크래치 · 리포에 안 넣음 = Codex 의 Windows 사용자 폴더 경로를 다시 만들어 넣는 도구)
- `_read/` 핀 소스 읽기용 사본 · 대조용 목록
