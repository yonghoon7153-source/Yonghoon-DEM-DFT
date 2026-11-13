# kgy S0 단계 1 다시 (SBE · 핀 56f4cfbb1 · 저장본 재기) — 결과 전 기대 E1–E4 · 문턱 T1–T3 대조 (11-13 · 대피 세션)

- 기준 = 결과 전 등록 `docs/reviews/rint2_s0_store_probe_20261112/README.md` (기대 E1–E4 · 문턱 T1–T3 · 1저자 11-12 밤 채택).
- 입력 = 1저자가 kgy 에서 묶은 s0log_20261113T014726Z.tgz (24,286,271 B · sha256 bbc14f4783efd7793231a39923cecc3e24cef2c3bf248e43787c4c1a69740e48 = kgy 의 .sha256 파일과 같음 · 안 파일 16) · 실행 = 01:47:26 → 03:20:36 UTC (`files/s0log_20261113T014726Z/meta.txt`) · 핀 `56f4cfbb1d26371007b460a992d4cfc1ef68e950` · PROBE 1 · TAG q2q11.
- 대조 = 빈 scratch 폴더에 풀어 읽기만 (python -I · 아무것도 실행 안 함 · npz = allow_pickle=False 로 배열 이름 · 꼴만) · σ 칸 없음 (단계 1 = 접합 census · 계획 · 저장본 재기 · 솔브 없음).
- 지위 = **개발 자료** (1저자 11-13 Q5 · Codex 반박 1/2 Q14 — 고침이 키 · 직렬화 · 조립 · 풀이 길에 닿으면 최종 핀으로 다시).
- 판정 = **E1–E4 · T1–T3 모두 기대대로** (E4 는 등록 문구가 빠뜨린 기록 전용 칸 하나를 한정으로 적음).

## 기대 E1–E4

| | 대조 | 결과 |
|---|---|---|
| E1 | rc 0 (`files/s0log_20261113T014726Z/rss.log` 끝 `rc=0` 한 줄) · 여섯 출력 다 있음 · 반입 도구 (`docs/data/rint2_s0_sbe_20261108/tools/import_s0_tgz.py`) = ADOPT_CANDIDATE · `out_sha256.txt` = 실제 sha256 6/6 같음 · kit JSON code: git_head = 핀 (위 40 자리) · git_dirty False · Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 · 코드 지문 7 = 리포 핀 blob sha256 7/7 같음 · 감싸개 md5 86e9bf4b4cfb79fa6e4a63d69cb414b0 · 감시 셸 md5 ff385531653c294089ce58f08511b6ad = 등록 값 | ✓ |
| E2 | `store_probe.json` calls 1 · n_instances 117,583 · 접합 npz 117,583 행 · 접촉 npz 117,070 행 (11-08 과 같은 행 수) | ✓ |
| E3 | encode ok (배열 470,415 · 8.7 s) · 쓰기 built_written · 읽기 hit · 같음 strict True · registry_fp True · object_is_new True · store_start preloaded [] · error None · code_drift [] · error None · machine-id 읽음 True | ✓ |
| E4 | 배열 둘 sha256 = 11-08 (`docs/data/rint2_s0_sbe_20261108/NPZ_SHA256.txt`) 과 같음 (접합 a1d435792c60e759… · 접촉 7fc40335a233c159…) · 계획 JSON 다른 칸 1 = source/tool_sha256 (`scripts/ca_s0_census.py` 지문) — 계획 sha256 4da98863… → 80a6c0b2… 은 이 칸 때문뿐 · kit JSON 다른 칸 8 = 코드 지문 셋 (ca_s0_census · step3_sigma · mpm_webapp_payload) · git_head · tool_sha256 · elapsed_s · plan.sha256 · inputs.payload_argv_sha256 | ✓ (한정 아래) |

- E4 한정: 등록 문구 (코드 지문 · 시각 칸 빼고) 밖의 다른 칸 하나 = inputs.payload_argv_sha256 — payload 인자에 출력 폴더 경로가 들어가 런마다 다르다 (`scripts/ca_s0_census.py` 주석 = 기록만) · 사슬 대조 칸 settings_sha256 = 같음 · payload 기록 (홈 경로를 가리면) = 바이트 같음.

## 문턱 T1–T3

| | 값 | 문턱 | 결과 |
|---|---|---|---|
| T1 | 쓰기 119.8 s · 읽기 86.8 s · 읽기 / 짓기 = 86.8 / 4,016.0 = 2.2 % | ≤ 600 s · ≤ 300 s · ≤ 10 % | ✓ |
| T2 | VmHWM(②–④) 5,410,992 kB − VmRSS(① 앞) 4,886,884 kB = 524,108 kB ≈ 0.50 GiB | ≤ 4 GiB | ✓ |
| T3 | 저장본 파일 1,340,094,879 B ≈ 1.25 GiB (파일 하나) | ≤ 2 GiB | ✓ |

## 시간 · 메모리 (보고)

- S0 elapsed 5,575.0 s · 재기 몫 (encode 8.7 + 쓰기 119.8 + 읽기 86.8 = 215.3 s) 을 빼면 5,359.7 s (11-08 = 5,382.8 s).
- 원장 짓기 4,016.0 s (= ⑥ 시도 1 · 2 의 탄소 접합 준비 67 분과 같은 크기) → 저장본 적중이면 R 팔마다 짓기 − 읽기 ≈ 3,929 s (≈ 65.5 분) 를 아낀다 (어림 · 단계 1 원장 = s_min 없음 = 자기 후보 전부 → R 팔 원장은 같거나 작다 · R 은 이 저장본 파일을 읽지 않는다 — 문턱이 달라 열쇠가 다르다).
- 메모리: rss.log 5 초 표본 최대 5,690,660 kB ≈ 5.43 GiB (t 5,339 s · 11-08 표본 최대 5.43 GiB 와 같음) · 감싸개가 잰 S0 프로세스 VmHWM (원장 짓기 끝까지) 8,289,604 kB ≈ 7.91 GiB — 5 초 표본이 약 2.5 GiB 짧은 봉우리를 놓친다 [관찰 · ⑥ 시도 2 RSS 최대 32.9 GiB 도 표본이라 같은 꼴이 숨어 있을 수 있음 · 미확인].
- 저장본 폴더 (kgy · 재기 전용 · R 은 읽지 않음) = 이 기록 push 뒤 지워도 된다 (등록 README '블록이 쓰는 자리').
