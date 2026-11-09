# Rint ② 현장 자격 점검 결과 — kgy · gabia (2026-11-09 · 핀 `db86ce9b9` · 짧은 블록)

> 출처 = 1저자가 두 기계에서 짧은 블록 (`docs/reviews/rint2_siteq_prep_20261109/README.md` §3) 을 돌린 결과 폴더를 기계마다 tgz 로 묶어 대화에 올림 (11-09 밤).  점검 도구 = `docs/reviews/rint2_siteq_prep_20261109/tools/siteq_probe.py` (sha256 a490b9adc3eeb7468b051b32bdaa0110879b71322a3a2cfb3b723505a3df8588 — 두 결과의 `probe_sha256` 칸과 같음).
> 이 폴더 = 홈 경로만 가린 사본 (§2).  받은 원본 바이트는 리포에 두지 않고 sha256 만 적는다.
> 지위 = 현장 자격 짧은 블록의 결과 기록.  rr3 수정 계획 §7 ④ "현장 자격" 칸의 증거로 쓸 수 있는지 · 그 범위 = Codex 회차 ⑥ Q4 판단 대기 (`docs/reviews/codex_rint2_rr_round6_request_20261109.md`).  등록 R · 봉인 · R 런 · 실행 GO 가 아니다 — 전체 HOLD 그대로.

## 1. 받은 것과 출처 대조

| 묶음 | 크기 | sha256 | 대조 |
|---|---|---|---|
| kgy tgz (2 파일) | 6,901 B | 3e8247f17a8644754f804b5e1c2ed8a13d27ad97804441f629f14b9026dd87fe | 1저자가 기계에서 찍어 붙여 넣은 값과 같음 |
| gabia tgz (2 파일) | 6,705 B | 7b6aa7e551ed6b46305e5dc0e8f59fd08f5706e6f2267c3b46e1b205de19df89 | 같음 |
| kgy `siteq_result.json` 원본 | 22,665 B | e997c992ff8f9ef72700d32688663ffc99ef0d36625947344f0130d3607843a0 | 블록이 화면에 찍은 값 (진행 기록 11-09 저녁 현장 자격 줄) 과 같음 |
| gabia `siteq_result.json` 원본 | 21,654 B | ad3c0ffce5339764aa196dac5f06d16366e1b5c361717b3b6ed0f280cc405380 | 같음 |
| kgy `siteq.log` 원본 | 6,060 B | f11321930a8394a060e8ad5c1c82323acdf269871af6eef7d8d115b6fd965881 | 화면 대조 없음 (블록은 로그 sha256 을 찍지 않음) |
| gabia `siteq.log` 원본 | 6,050 B | 1e5d13d358aa2f8af0ddeeca29f95734fc54084160b5af37d0014e3159448a9b | 같음 (화면 대조 없음) |

- tgz 안 = 결과 폴더 하나 (상대 경로 · 파일 둘 · 특수 파일 없음) · 받은 파일은 빈 폴더에 풀어 읽었다 (python -I).

## 2. 가림 규칙

- 바꾼 것 = 홈 폴더 경로 (kgy = 일반 사용자 홈 · gabia = root 홈) → `<HOME>` (문자열 치환 · JSON 은 키 · 값 모두).  바꾼 자리 = kgy JSON 25 · 로그 2 · gabia JSON 21 · 로그 2.
- 그대로 둔 것 = 나머지 바이트 전부 — machine-id · boot-id (사슬 기록에도 있는 칸 · 준비 문서 §3-1 5) · uid · C08 의 프로세스 이름 표본 · cgroup 경로 · 기계 별명 (kgy · gabia).  주소 · 호스트 이름 · 사용자 이름은 원본에 없다 (훑어봄).
- 대조: 가린 사본을 JSON 으로 다시 읽으면 원본의 모든 칸에 같은 치환을 한 것과 같다 (두 JSON) · 가린 사본에 홈 경로가 남지 않았다.
- 가린 사본의 sha256 = `SHA256SUMS`.

## 3. 결과

준비 문서 §3-3 의 나란히 보기 (가린 사본 · 원본 둘 다 같은 출력):

```
pin                  SAME  db86ce9b955c2aa13430680f79a431e8a580ed83 | db86ce9b955c2aa13430680f79a431e8a580ed83
env unit C02         SAME  {'numpy': '1.24.4', 'python_minor': '3.8', 'scipy': '1.10.1'} | {'numpy': '1.24.4', 'python_minor': '3.8', 'scipy': '1.10.1'}
code_key_sha256 C04  SAME  095af7ab8bcced0ca2489fe09b7cb9b48da0727ba37c9ea1eb8a8e98c987d21d | 095af7ab8bcced0ca2489fe09b7cb9b48da0727ba37c9ea1eb8a8e98c987d21d
kgy    {"INFO": 8, "PASS": 25}
gabia  {"INFO": 9, "PASS": 24}
```

| | kgy | gabia |
|---|---|---|
| 종료 코드 | rc 0 (1저자 화면) = 집계에 FAIL · ERROR 없음과 맞음 | rc 0 (같음) |
| PASS · INFO · WARN · FAIL · ERROR | 25 · 8 · 0 · 0 · 0 | 24 · 9 · 0 · 0 · 0 |
| 걸린 시간 | 14.7 s (09:54:38 – 09:54:53 UTC) | 17.5 s (09:54:47 – 09:55:05 UTC) |
| 실행 사용자 | uid 1003 (일반 사용자) | uid 0 (root) |
| 파이썬 | 3.8.10 | 3.8.10 |

결과 전 기대 (준비 문서 §3-2 "현장 기대 (추정)") 와 대조:

| 기대 | kgy | gabia |
|---|---|---|
| C02 = PASS (3.8 · 1.24.4 · 1.10.1) | PASS | PASS |
| C28 = INFO (GPU · cupy 있음) | INFO (RTX 3090 24 GB · cupy-cuda12x 12.3.0) | INFO (RTX A6000 48 GB · cupy-cuda12x 12.3.0) |
| gabia C13b = INFO (root 라 권한 기반 보호 뜻 없음) | PASS (읽기 전용 원장 .git = 배타 잠금 멈춤 · 공유 잠금은 잠금 없이 얻음) | INFO (`read-only .git is still writable for this user`) |
| C26 = 로컬 FS 면 PASS | PASS (ext4) | PASS (ext4) |

⇒ 기대와 다른 칸 0.

## 4. 기록 칸 (INFO · 판정 아님 · 1저자 · 검토자가 보는 것)

| 칸 | kgy | gabia | 뜻 (관찰) |
|---|---|---|---|
| C18 umask | 002 (새 파일 664) | 022 (644) | 사슬은 기록 · 로그를 프로세스 umask 로 쓴다 → kgy 에서는 같은 그룹 사용자가 기록을 고칠 수 있다 (그룹 구성원 미확인) |
| C08 옛 규칙 (since · runner 없음) | 판단 못 함 4 (sd-pam · sshd 셋) | 0 | 새 규칙 (새 표지) = 둘 다 빈 목록 · 옛 규칙이었으면 kgy 에서 4 개를 가르지 못했다 |
| C20 TMPDIR | ext4 · 남은 340.1 GB | ext4 · 남은 211.5 GB | 쓰지 않고 잼 |
| C22 보조 명령 시간 | nvidia-smi 0.04 s · BLAS 0.20 s · git 0.00 s | 0.04 · 0.21 · 0.00 s | 상한 (20 · 120 s) 에서 멀다 |
| C24 rlimit | NOFILE 1,024 / 1,048,576 · NPROC 256,289 · CORE 0 · 나머지 상한 없음 | NOFILE 같음 · NPROC 255,381 · CORE 0 | WARN 조건 (AS · DATA · CPU · FSIZE 상한) 없음 |
| C25 메모리 | 총 62.7 GiB · 가용 47.9 GiB · swap 2.0 GiB (남음 1.0) · cgroup v1 memory 상한 없음 | 총 62.4 GiB · 가용 55.2 GiB · swap 16.0 GiB · cgroup v2 memory.max · pids.max = max · oom.group 0 | 할당하지 않고 읽음 |
| C26 남은 공간 (홈 FS) | 340.1 GB / 982.8 GB | 211.5 GB / 452.4 GB | kgy = 준비 문서 §7 조사 기록 (98 GB · 사용 89 %) 과 다름 — 그 사이 정리했는지 미확인 |
| C26 계획 폴더 | 점검함 (ext4 · 홈과 같은 FS) | 블록의 계획 폴더 칸을 비워 보냄 → 결과 · 리포 · 홈 셋만 점검 | gabia 계획 폴더 FS 는 미점검 — 봉인 때 정하면 그 칸으로 다시 |
| C27 | /proc 기본 · pid_max 4,194,304 | 같음 | |
| C29 | Ubuntu 20.04.6 · CPU 16 (affinity 16) · NTP 동기 · nohup · setsid · tmux | Ubuntu 24.04.4 · CPU 20 (affinity 20) · NTP 동기 · nohup · screen · setsid · tmux | |

## 5. 이 결과가 말하는 것 · 말하지 않는 것

- 말하는 것: 핀 `db86ce9b9` 의 사슬 함수 (프로세스 묶음 · 신호 · 잠금 · 원자적 쓰기 · 특수 파일 · 원장 git · 복사 · 인코딩 · 권한) 가 두 기계의 실제 OS 에서, 그 블록 · 그 순간 · 그 셸 하나에서, 준비 때 합성 시험이 기대한 대로 동작했다 (FAIL · ERROR · WARN 0).  두 기계 환경 단위 · 코드 키가 같다 (같은 핀).
- 말하지 않는 것 = 준비 문서 §5 의 남는 몫 그대로: 쓰는 도중 kill · 전원 손실 · 실제 OOM · 디스크 가득 · 여러 시간 런 · 두 기계가 한 원장을 같이 쓰는 경우 · 실제 러너 · payload · GPU · 진짜 비 root · ssh · tmux · cron 아래 표지 스캔 · pid 재사용 경합 · 12 단위 끝-끝 · 숫자 칸 · 실행 정책.
- gabia = root 라 권한 기반 보호 (C13b) 는 뜻이 없다 (기대대로) · kgy umask 002 (§4).
- 핀: `db86ce9b9` 뒤 이 폴더를 넣는 커밋의 앞 커밋 `1f71b5b7c` 까지 `scripts/` · `webapp/` · 점검 도구 변경 0 (git diff --stat 빈 출력).  봉인 핀에서 사슬 · 계약 · 러너 파일이 `db86ce9b9` 와 다르면 그 핀으로 짧은 블록을 다시 돌린다 (PIN 한 줄).  코드 키는 HEAD 를 담아 핀마다 다르므로 두 기계 대조는 같은 핀끼리만 뜻이 있다.

## 6. 파일

- `kgy/siteq_result.json` · `kgy/siteq.log` · `gabia/siteq_result.json` · `gabia/siteq.log` — 홈 경로만 가린 사본 (ASCII).
- `SHA256SUMS` — 가린 사본 넷의 sha256.
