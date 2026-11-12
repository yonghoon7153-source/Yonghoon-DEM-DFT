# 개정 문장 초안 — Q2 탄소 접합 원장 저장본 + Q11 GPU 전처리 C 꼴 (11-12 · 조수 · 6 판 = 2 회차 고침 (내부 반박 리뷰 재확인) + 같은 부류 시험 모듈 셋 (본 세션 결정 11-12 밤) 뒤 · 초안만 · 리포 문서는 고치지 않았다)

바탕 = 작업 트리 `/home/user/rint-codepkg` · 시험 먼저 `ebb0e9f80` → 구현 `f17ea8c6b` → 시험 보강 `2f97617ef` → (4 판) 리뷰 시험 먼저 `4557a30c2` → 리뷰 고침
`94765bed3` → 게이트 배선 `0ac6edf3c` (여섯 다 서명 없음 · push 없음 — 본 세션이 반입하며 서명하면
sha 가 바뀐다 → 아래 sha 는 반입 뒤 값으로 바꿔 적는다).  아래 문장은 본 세션이 고쳐 쓰고 1저자 · Codex 봉인 전 묶음에 싣는다.
⚠ 숫자 · 결정은 고르지 않았다 — `⬜` 자리 = 1저자 · 본 세션.  시험 수 · 시간 = 보고 (답장) 의 값 (이 초안에 베끼지 않는다).

## 0. 2 판에서 달라진 것 (대피 세션 · 넘겨받은 구현을 고친 것 — 설계 메모 `design.md` (마) 절)

- 넘겨받은 구현은 instance 가 둘 이상인 원장을 저장하지 못했다 (`instances.pair_i · pair_j` = `[빈 배열] * instance 수` = 같은 객체 → 별칭 거부 →
  저장 건너뜀 · 실침대 SBE instance 117,583).  → 저장 꼴이 별칭을 **되가리킴**으로 그대로 싣는다 (엄격 지문에 별칭 구조 포함).
- 메모리 겹침 검사 n² → n log n (실침대 원장의 배열 약 47 만 개) · 쓰기 쪽 뜻밖의 예외 = 기록만 · 읽기 내용 단의 뜻밖의 예외 = 어긋남.
- 문장에 더할 것 = 1-2 의 "별칭" · "규모" · "첫 팔 화면 줄 확인" · "옛 파일 · 임시 파일 정리" 줄.

## 0-b. 3 판 (대피 4 · 11-12) 에서 달라진 것

- 시험 보강 커밋 하나 (시험만 · 코드 그대로): 열쇠의 스키마 칸 (T4) · 저장본 폴더 다른 소유자 (T11 · `Store`) · 사슬 `--cjunc-store` 다른 소유자 (C1 여덟째) —
  2 판까지 이 셋에 시험 · 변이가 없었다 (변이 K13 · W19 · C10 = 보강 전 시험에서 안 잡힘 → 보강 뒤 잡힘).  커밋 = 작업 트리 `2f97617ef` (반입하며 sha 바뀜).
- 2 절 "줄 번호 다시 확인" = 끝 (`run_probe6.sh` 58–66 · 236–251 · 434 그대로) · 탐침 도구가 S0 단계 1 자료를 읽는 자리 = 계획 파일 하나
  (`S0PLAN_REL` 51 줄) 의 침대 이름 · tol_ff 대조뿐 (336–350 줄 · `probe6_read.py` 783–792 줄 = "identity only") — 코드 지문은 보지 않는다 →
  시도 3 자체는 S0 단계 1 다시를 앞 조건으로 요구하지 않는다 (R 사슬은 요구한다 · `rint_r_chain.s0_code_problem`).  2 절 앞 조건 줄을 그렇게 고쳤다.
- 4 절 GPU 확인 블록 = CPU 흐름 확인 끝 (아래 4 절 덧).

## 0-c. 4 판 (내부 반박 리뷰 · Codex 아님 · 11-12) 에서 달라진 것 — 처분 (리뷰 `review/review_codepkg.md` RCP-01–11)

| RCP | 등급 | 처분 | 무엇 |
|---|---|---|---|
| 01 | P1 | 고침 | 열쇠 코드 칸 = 넷 (`carbon_junction.py` · `step3_sigma.py` · **`fibre_segment_raster.py`** · `cjunc_store.py`) = 원장 짓기가 부르는 프로젝트 모듈 전부 (시험 T14 = 짓는 동안 실제로 돈 함수의 파일 ⊆ 열쇠 · 두 모듈의 프로젝트 import ⊆ 열쇠 · 반례 CE1 = 고치기 전 옛 원장 적중 → 고친 뒤 다른 열쇠). 경로 = `importlib.util.find_spec` (불러오지 않는다 → 매니페스트 exec_env 의 불러온 모듈 집합이 켬 · 끔에서 같다). (나) 사슬 `CODE_FILES` 20 통째는 고르지 않았다 (원장과 무관한 파일 편집에도 저장본 전체가 무효 · 런 단위 같은 판은 사슬이 이미 지킨다) |
| 02 | P2 | 고침 | 게이트 배선 — `scripts/check_all.sh` 세 단계 (전처리 · 저장본 · 저장본 끝-끝 = 따로 한 줄) · `scripts/check_kgy_py38.sh` 16 묶음 · CI 는 Rint `test_*.py` 줄이 없어 그대로 (같은 꼴 줄 없음) |
| 03 | P2 | 한정 + ⬜ 질문 | "저장본 밖 독립 대조" = **SV 모서리 팔만** (봉인 원천 재조립) · 다른 팔은 대조 없음 — 문장을 그렇게 줄였다 (코드 설명 · 시험 T7 보고 줄 · 아래 1-2). S0 단계 2 원장 지문 ↔ DBE arm 0 대조는 넣지 않았다 (S0 보고 `fp_use = record_only` = 등록된 결정 · 기계 사이 원장 지문 결정성 미확인) → 1저자 질문 Q-A |
| 04 | P2 | 단계 넣음 | S0 단계 1 다시 (kgy) 에 실침대 저장 · 읽기 재기 — 아래 2-b · 블록 `s0probe/s0_rerun_probe_block.txt` (실행 = 1저자) |
| 05 | P3 | 고침 | 환경 칸에 실행 자리 지문 (인터프리터 `sys.prefix` · numpy · scipy 설치 자리의 실제 경로 → blake2b 16 — 경로 글자는 싣지 않는다) |
| 06 | P3 | 고침 | 저장본 **파일** 소유자 ≠ 이 사용자 · 그룹 · 남 쓰기 = 어긋남 (멈춤) · 저장본 **폴더**가 심볼릭 링크 = 거부 (Store · 사슬 `--cjunc-store` · 러너 `CJUNC_STORE` · 끝 빗금 포함) |
| 07 | P3 | 한정 | 사슬 런 기록에 저장본 상태 · 요약 수 · 운영 정리 (옛 파일 지우기) 없음 — payload 화면 한 줄 + 단계 요약 `cjunc_store: true` 뿐 (봉인 전 묶음에 넣을지 = 본 세션) |
| 08 | P3 | 고침 | GPU 길에서 `LinearOperator` 를 `cg` 와 따로 들인다 — 없으면 따로 사유 줄 (조치 = cupy 판 확인 · GPU 를 비워도 같은 실패) · 일반 실패 문구 그대로 |
| 09 | P3 | 고침 | 시험 G4 가 비어 있었다 (−0 이 생기지 않는 입력) → ±0 · 비정규 수를 A · C 적용에 직접 넣어 바이트 차이 자리 = (C = −0 ∧ A = +0) 자리 · 실제 풀이 8 번 (씨앗 둘 × tol / rtol × 새로 / 이어) 의 잔차에 −0 없음 · 반복마다 A = C 바이트 |
| 10 | P3 | 고침 | payload — `--step3-rasterize-only` + `--step3-cjunc-store` = 거부 (`STORE_RASTERIZE_ONLY`) · 저장본 폴더 검사의 모든 예외 = 구조화 거부 (`S2_CJUNC_REFUSED|STORE_PATH|` + 예외 이름 · 옛 판 = ValueError 밖은 Traceback) |
| 11 | P3 | 고침 | 머리 JSON 의 writer = pid · utc · build_seconds (호스트 이름 뺐다) |

## 0-d. 5 판 (2 회차 · 내부 반박 리뷰 재확인 `review/rereview_codepkg.md` · Codex 아님 · 11-12) 에서 달라진 것

커밋 (작업 트리 · 서명 없음 · push 없음 · 바탕 `0ac6edf3c`): 시험 먼저 `f8077a51d` → 고침 `4e1e5b6c6` → 게이트 배선 · 결과 전 등록 `ac7e1c58d` →
변이 보강 (G5 · 사슬 F5) `8cc3fe462` → 변이 보강 (T11 상대 경로 = 절대 경로 사유) `609d78ca4` (= 끝 · 반입하며 sha 바뀜).

| RCP2 | 등급 | 처분 | 무엇 · 이 초안에서 고친 문장 |
|---|---|---|---|
| 01 | P2 | 고침 | 런 시작 코드 칸 — `cjunc_store` 를 처음 불러온 때 (`_START` · payload = 입구 계약에서 원장 모듈보다 먼저 · 시험 P6) 열쇠 코드 파일 넷의 자리 · sha256 · 시각 → 짓기 전 · 발행 직전 (`os.link` 앞) 에 다시 센다 · 다르면 (자리 · 내용 · 시작 + 1 s 뒤 다시 씀) 그 런은 저장본을 읽지도 (`disabled`) 쓰지도 (`built_write_skipped`) 않는다 · 사유 머리 `code_changed:` · 팔 결과 = 새로 지은 원장.  재리뷰 CE-A (원판 원장을 변이판 열쇠로 저장 → 정직한 런 적중) = T15 에서 재현 → 고친 뒤 저장 안 함 → 1-2 의 "열쇠 = 디스크의 코드 파일 지문" 한정 줄을 아래처럼 바꿈 |
| 02 | P3 | 고침 | 저장본 폴더 = 정규화된 꼴만 (빈 성분 `//` · `.` · `..` 없음 · 끝 빗금만 걷는다 · `run_contract.normal_path_problem` · Store · 사슬 · 러너 셋 다) — `<링크>/.` 꼴이 심볼릭 링크 거부를 비켜 가던 것 |
| 03 | P3 | 시험 | T7 파일 모드 = 그룹 쓰기만 (0464 · 0664) · 남 쓰기만 (0446 · 0646) 갈래 · T11 뿌리 남 쓰기만 (0757) — 재리뷰 변이 N9 (0o022 → 0o002) 를 잡는다 |
| 04 | P2 | 등록 | 2-b 의 결과 전 기대 E1–E4 · 문턱 T1–T3 (1저자 11-12 밤 Q-B (가) · 문턱 [제안] 그대로 채택) · 블록이 쓰는 자리 전부 → 리포 문서 `docs/reviews/rint2_s0_store_probe_20261112/README.md` + 블록 (같은 폴더 · PIN 자리표) · 감싸개 v2 (`cjunc_store` 를 먼저 불러오고 `store_start` · 호출마다 `code_drift` 를 적는다 · E3 에 `code_drift []` 더함) |
| 05 | P3 | 시험 | T14 = 원장 짓기 동안 실행된 파일 전수 분류 (표준 · numpy · scipy · 열쇠 넷 밖 = 0) · 원장 모듈 import 허용 목록 · 변이 코드 폴더 새 프로세스 (scripts/ 밖도 본다) |
| 06 | P2 | 고침 | git 을 부르는 곳이 부르는 쪽 환경의 `GIT_*` 를 물려받지 않는다 (`run_contract.git_env` · `drop_git_env` = `GIT_` 접두 전부) — 쓰기 = `run_contract --selftest` RCPT-sha 임시 저장소 (꼭대기 확인 뒤만 쓴다) · 이 묶음이 고친 시험 모듈 다섯 + 같은 부류 셋 (6 판 · 0-e) (불러올 때 지움) · 읽기 = payload `_code_sha` · `_exec_env` · 사슬 `git_identity` · F5 · 원장 git.  새 시험 `scripts/test_git_env_isolation.py` (게이트 121 단계 · kgy 17 묶음) = 일회용 피해 저장소만 가리키는 적대 환경 셋을 자식에만 넘긴다.  11-12 밤 사고 꼴 (GIT_DIR 아래 selftest 가 남의 가지에 커밋) = 고치기 전 재현 → 고친 뒤 피해 저장소 그대로 |
| RCP-03 · 04 · 06 남은 몫 | — | 한정 문장 | `scripts/cjunc_store.py` 머리 — 런 시작 칸 한정 넷 ((가) `cjunc_store` 보다 먼저 불린 열쇠 모듈이 그 전에 바뀜 · (나) 시각을 되돌린 뒤집기 · (다) 낡은 .pyc · (라) 같은 프로세스 함수 바꿔 끼우기) · 뿌리 판정 = 마지막 성분 · 경로 기준 (fd 아님) |

1-2 의 바꿀 문장 (5 판):
- "폴더 = 기계마다 하나 (절대 경로 · …)" 줄에 **"정규화된 꼴 (빈 성분 · `.` · `..` 없음 — 끝 빗금만 걷는다 · 2 회차)"** 을 더한다.
- 한정 줄 "열쇠 = 디스크의 코드 파일 지문이다 (불러온 코드 자체가 아니다 · 같은 프로세스에서 모듈을 바꿔 끼우는 것은 못 가린다 · 한정)" →
  > 열쇠 = 디스크의 코드 파일 지문이다.  런 도중 그 파일이 바뀌면 (런 시작 = `cjunc_store` 를 처음 불러온 때 · 짓기 전 · 발행 직전 다시 셈 — 자리 ·
  > sha256 · 시작 + 1 s 뒤 다시 씀) 그 런은 저장본을 읽지도 쓰지도 않는다 (화면 줄 `code_changed: …` · 팔 결과 = 새로 지은 원장 · 2 회차).
  > 못 가리는 것 (한정): 먼저 불린 열쇠 모듈의 import 전 바뀜 · 시각을 되돌린 뒤집기 · 낡은 .pyc · 같은 프로세스에서 함수를 바꿔 끼우기.
- 처분 줄 "쓰기 실패 … = 기록만" 앞에 **"런 도중 코드 바뀜 = 읽지도 쓰지도 않음 (`disabled` · `built_write_skipped` · 사유 `code_changed:` · 팔 결과 무관)"**.
- 새 줄: **"git 을 부르는 코드 (payload 코드 신원 · 사슬 신원 · 계획 출처 F5 · 원장 git · selftest 임시 저장소) 는 부르는 쪽 환경의 `GIT_*` 를
  물려받지 않는다 (훅 안 게이트 · 2 회차 · 같은 부류 시험 모듈 셋 = 6 판 · 시험 `scripts/test_git_env_isolation.py`)."**

~~⬜ 본 세션 결정 (같은 부류 · 범위 밖 · 손대지 않음): 이 묶음이 안 고친 시험 셋이 git 을 부르는 쪽 환경으로 부른다~~ → ✅ 6 판에서 닫음 (0-e · 1저자 11-12 밤 오버나잇 = 권고대로).  옛 문단 = `amend_drafts_v5.md`.

2-b → 리포 문서 `docs/reviews/rint2_s0_store_probe_20261112/README.md` 가 정본 (기대 · 문턱 · 쓰는 자리 · 멈춤 · 한정) — 이 초안의 2-b 표는 역사 (문턱 = 채택됨).

4-d (GPU 확인 블록 5 판) = 아래 4 절 끝 4-d.

## 0-e. 6 판 (같은 부류 시험 모듈 셋 · 본 세션 결정 11-12 밤 = 권고대로 · 내부 반박 리뷰 재확인 · Codex 아님) 에서 달라진 것

커밋 (작업 트리 · 서명 없음 · push 없음 · 바탕 `609d78ca4`): 시험 먼저 `c0ff22431` → 고침 `ea3b13b89` (= 끝 · 반입하며 sha 바뀜).

- 시험 먼저 = `scripts/test_git_env_isolation.py` G6 목록 넷 → 일곱 (`test_rint_r_chain_e2e` `_git` · `test_rint_r_chain_e2e12` `git` = `E._git` · `test_step3_conv_cert` = 불러온 뒤 env 없는 git 으로 고정물) — 고치기 전 = G6 실패 (새 셋 × 적대 꼴 셋 · GIT_DIR 꼴 = 고정물 git 이 일회용 V 로 감).
- 고침 = 세 모듈 맨 앞 `sys.path.insert(0, SCRIPTS)` 바로 뒤 두 줄 `import run_contract as _RCG` · `_RCG.drop_git_env()` (다른 시험 모듈과 같은 꼴 · 새 코드 없음) → 이 시험 프로세스와 자식 (고정물 init · add · commit · `pull` · 기반 판 `git show`) 이 부르는 쪽 `GIT_*` 를 물려받지 않는다.
- 봉인 대조 (고치기 전): 194 `CODE_FILES` 32 · 사슬 `CODE_FILES` 20 · 언로딩 키트 SHA256SUMS · 믹서 봉인 · 정책 — 셋 다 없음 (Codex 회차 ④ · ⑤ 증거 SHA256SUMS 의 `test_rint_r_chain_e2e.py` 한 줄 = ZIP 안 사본 · 리뷰 핀 `1f9f3607e` blob 기준 = 지금 파일과 묶이지 않음).
- 겹 방어 (한정): `test_rint_r_chain_e2e12` 는 곧이어 `test_rint_r_chain_e2e` 를 불러오므로 제 줄을 지워도 G6 이 못 가린다 (아래층이 지움 · `test_cjunc_store_e2e` 와 같은 꼴) — 두 줄을 함께 지우면 e2e12 자리도 걸린다.
- 1-2 의 git 새 줄 끝 괄호 → "(훅 안 게이트 · 2 회차 · 같은 부류 시험 모듈 셋 = 6 판 · 시험 `scripts/test_git_env_isolation.py`)".
- 4-e (GPU 확인 블록 6 판) = 아래 4 절 끝 4-e.

## 1. 등록 R (`docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md`)

### 1-1. §2-1b (같은 코드) 덧붙임
> (11-12 · 1저자 Q2 · Q11) 같은 판 대조 파일 (사슬 `CODE_FILES`) = 20 — `cjunc_store.py` (탄소 접합 원장 저장본 · payload 가 `--step3-cjunc-store` 일 때
> 원장을 읽고 쓴다) 를 더했다.  S0 일곱 파일 (`S0_SAME_FILES`) 은 그대로다 — 그러나 이 묶음은 그 일곱 가운데 `step3_sigma.py` (Q11 GPU 전처리
> 표현) · `mpm_webapp_payload.py` (Q2 배선) 를 바꿨으므로 **S0 단계 1 보고 (SBE) 를 새 코드로 다시 만든다** (CPU 약 1.5 h · kgy · 실측 5,383 s ·
> s_min 다시 고르기 금지 문장 `S0_RERUN` 그대로 — 같은 계획 · 같은 침대).  S0 단계 2 (DBE) 가 이미 돌았다면 그것도 다시 (지금 사슬은 두 보고의
> 일곱 파일 지문을 다 대조한다 · `rint_r_chain.s0_code_problem`) ⬜ 돌았는지 = 본 세션 확인.  (`carbon_junction.py` · `fibre_segment_raster.py` 는 바뀌지 않았다
> = 원장 코드 그대로 — 11-08 S0 핀 `f47bde0f6` 뒤로 일곱 파일 가운데 바뀐 것 = 이 묶음의 `step3_sigma.py` · `mpm_webapp_payload.py` 둘뿐 · 둘 다 리뷰 고침
> `94765bed3` 에서 다시 바뀌었으므로 S0 다시는 **반입 뒤 끝 핀**으로.)  (4 판) S0 단계 1 다시에 저장본 재기를 얹는 블록 = 2-b.

### 1-2. §10 (명령 꼴) 덧붙임 — 새 산출물 = 원장 저장본
> (11-12 · 1저자 Q2) ladder · predict (단위 · 넘침 점 포함 · **합치기 아님**) 명령에 `--cjunc-store <폴더>` 를 줄 수 있다 — 탄소 접합 원장 (기하) 저장본.
> · 폴더 = 기계마다 하나 (절대 경로 · 영문 · 숫자 · `. _ / -` · 이 사용자 소유 · 그룹 · 남 쓰기 없음 = 운영자가 umask 022 셸에서 만든다) · 시도 ·
>   런 폴더 밖 (시도 사이 · 재실행 사이에 쓴다) · **심볼릭 링크 아닌 실제 폴더** (Store · 사슬 · 러너 셋 다 거부 · 4 판) · 파일 `cjreg_<열쇠 sha256>.npz`
>   (0444 · 단일 작성자 = 임시 파일 → 같은 읽기 길로 다시 읽어 대조 →
>   `os.link` · 덮어쓰기 없음).
> · 열쇠 = 꼴 판 · 모델 판 · 스키마 · 코드 sha256 넷 (`carbon_junction.py` · `step3_sigma.py` · `fibre_segment_raster.py` · `cjunc_store.py` = 원장 짓기가
>   부르는 프로젝트 모듈 전부 · 시험 T14 · 경로는 불러오지 않고 찾는다) · 환경 같음 단위 (python 부 판 · numpy · scipy + 실행 자리 지문 = 인터프리터 ·
>   numpy · scipy 설치 자리 · 4 판) · 기계 지문 (`/etc/machine-id` · 못 읽으면 저장본 꺼짐 = 매번 짓기) · sid 격자 지문 · lo · vox (실수 비트) · 입력 넷
>   (VGCF · PTFE · SDCP 점 · phase · fid · kind 의 정준 값) · 원장 문턱 열 칸.  계획 (R_j · 법칙 · c · SV 노브) 은 팔마다 다시 만든다 — 한 침대 ·
>   한 origin 의 팔 (R_j · P0 / P1 · c · 바닥 · 천장 · SV 반사실 · off ↔ face_alpha) 이 저장본 하나를 같이 쓴다 (시험 T5g).  origin 이 다르면 (격자가
>   다르다) 다른 열쇠다.
> · 산출 바이트 = 끔과 같다 — 팔 JSON · 매니페스트 · 영수증 · OUTDIR · 팔 이름 (시험 `scripts/test_cjunc_store.py` P2 · P5 · R2 ·
>   `scripts/test_cjunc_store_e2e.py` Z2 · Z3 · Z6).  기록 = payload 화면 한 줄 + 단계 요약 `cjunc_store: true` (켬일 때만).
> · 저장 꼴 = 원장 dict 전체를 형 표지 트리 (뼈대 JSON) + 배열 멤버 (npy · `allow_pickle=False`) 로 · **별칭 그대로** (같은 객체가 두 자리 이상 =
>   되가리킴 — 원장의 `pair_i · pair_j`) · 읽은 원장 = 지은 원장 을 엄격 지문 (형 · dtype · 모양 · C/F · 바이트 · dict 키 차례 · 별칭 구조) ·
>   `registry_fp` 다시 셈 · sid 지문으로 대조한다.  서로 다른 배열이 메모리를 나눠 쓰는 꼴 · 읽기 전용 · 비연속 배열이 원장에 있으면 저장하지 않는다
>   (⚠ 줄 · 팔 결과 그대로).
> · 봉인 원천 (조립만 런 · 예측 · 판정 · 다시 판정 · 합치기의 `RunnerGraphSource`) 은 **저장본을 읽지 않는다** (사슬 env 에서 지움 · 러너
>   `CJUNC_GRAPH_ONLY=1` + `CJUNC_STORE` = ABORT · payload `--step3-cjunc-graph-only` + `--step3-cjunc-store` = 거부) — 저장본으로 지은 팔의 그래프
>   지문은 저장본 없이 다시 조립한 원천과 견준다 (독립 대조 그대로 · e2e Z4).  ⇒ E-2 4 번의 판정 쪽 이득 (봉인 원천 36 번 · −118.4 h 팔 전체 꼴 ·
>   −40.4 h 풀이에만 꼴) 은 **받지 않는다** (1저자 11-12 Q9 = 기준은 GPU 팔 · 판정은 그 뒤).
> · 처분: 없음 → 짓고 씀 · **못 읽음** (0 바이트 · zip 꼴 · 멤버 집합 · CRC — 끊긴 복사 · 디스크 = 정직한 흐름) → 다시 지음 · 파일은 두고 덮어쓰지
>   않음 · ⚠ 줄 (운영자가 지운다 — 지울 때까지 그 열쇠의 팔은 매번 다시 짓는다) · **어긋남** (머리 JSON · 꼴 판 · 열쇠 (이름 바꿈) · 뼈대 sha · 복원 ·
>   엄격 지문 · registry_fp · sid 지문 · 배열 뒤 남는 바이트 · 심볼릭 링크 · 폴더 · **파일 소유자 ≠ 이 사용자 · 그룹 · 남 쓰기** (4 판) · 같은 열쇠를 남이
>   다른 원장으로 먼저 씀 · 내용 대조 중 뜻밖의 오류) →
>   payload 멈춤 `S2_CJUNC_STORE|INCONSISTENT|` (rc ≠ 0 → 사슬 RUNNER_RC) · 폴더 검사 실패 (모든 예외 · 4 판) = 런 전 거부
>   `S2_CJUNC_REFUSED|STORE_PATH|` · `--step3-rasterize-only` 와 함께 = 거부 `STORE_RASTERIZE_ONLY` (4 판) · 쓰기 실패 (자리 · 권한 · link 미지원 · 디스크 여유 < 2 × 크기 + 1 GiB ·
>   저장 쪽 뜻밖의 오류) = 기록만 (팔 결과 무관) · 읽는 중 메모리 부족 = 그대로 (자원 오류).
> · 운영: ① **첫 팔의 화면 줄을 본다** — `S2 탄소 접합 원장 저장본 — 새로 지어 저장 …` 이어야 한다 (`⚠ … 저장 안 함 (unsupported …)` 이면 그 침대의
>   원장이 저장 꼴 밖 = 이득 없음 · 본 세션에 알린다) · 둘째 팔부터 `읽음 …` ② 옛 코드 판 · 옛 침대의 `cjreg_*.npz` · 끊긴 쓰기의 `.cjreg_*.tmp` 는
>   저절로 지워지지 않는다 (운영자가 지운다 · 열쇠가 달라 읽히지는 않는다).
> · 한정: 같은 열쇠 이름 아래 **자기 일관 위조** (내용 · 머리 · 지문을 모두 다시 센 파일) 는 저장본 혼자 가리지 못한다 (시험 T7 보고 줄) — 막는 것 =
>   폴더 · 파일 소유자 · 권한 검사 + 봉인 원천 재조립 대조 — **SV 모서리 팔만** · 다른 팔은 저장본 밖 대조가 **없다** (같은 코드의 결정성 가정 ·
>   재실행 바이트 대조가 같은 가정 · 4 판 = 문장을 줄였다 · 다른 팔을 대조할지 = ⬜ 1저자 Q-A).  열쇠 = 디스크의 코드 파일 지문이다 (불러온 코드 자체가
>   아니다 · 같은 프로세스에서 모듈을 바꿔 끼우는 것은 못 가린다 · 한정).
>   실침대 원장의 저장 · 읽기 (꼴 · 시간 · 메모리 = 발행 전 대조 때 원장 사본 하나 더) 는 S0 단계 1 다시의 재기 (2-b · 4 판) 전
>   [미확인] — 시험 = 픽스처 (instance ≤ 50) + 합성 꼴 (작은 배열 12 만 · zip 멤버 12 만).

### 1-3. §11 (⑥ · 개발 탐침) 덧붙임
> (11-12 · 1저자 Q5) Q2 · Q11 코드 묶음은 원장 §3 "풀이 코드 목록" (`scripts/` 통째) 을 바꾼다 → ⑥ 다시 재기 = 원장 시도 3 (아래 2 절) · 그 값만
> 계획의 maxiter · 시간 상한 숫자 재료 (채택 불가 규칙 그대로).

### 1-4. Q11 (GPU 전처리) 문장
> (11-12 · 1저자 Q11) GPU 길 Jacobi 전처리 = 같은 수 (1/diag) · 같은 정지 · **표현만** 벡터 곱 연산자 (`cupyx.scipy.sparse.linalg.LinearOperator` ·
> 옛 = dia_matrix · 적용마다 CSR 변환) · 기록 `precond` = 'jacobi' 그대로 · 새 기록 키 없음 · CPU 길 그대로 · `LinearOperator` 가 없는 cupy 판 =
> 따로 사유 줄 (`cg` 와 따로 들인다 · 4 판).  부호 있는 0 = C 꼴은 1/diag × r 의 곱이라 r 의 −0 자리에서 −0 을 낼 수 있다 (A 꼴은 CSR 곱의 합 = +0) →
> 시험 G4 가 그 자리 · 실제 풀이 잔차에 −0 이 없음 · 반복마다 바이트 같음을 본다 (4 판).  보증 = 가짜 cupy 시험
> (`scripts/test_step3_gpu_precond.py` · 옛 판 A 꼴과 해 · info · 반복 수 · LAST_BACKEND 비트 같음 · 같은 산술) + GPU 확인 블록 (실기계 · 결과 전
> 기대 = 비트 같음 · ⬜ 1저자 실행) · 실기계 비트 같음은 블록 결과 전 [미확인].

## 2. 개발 탐침 원장 (`docs/reviews/rint2_dev_probe_ledger_20261026.md`) §3 — 시도 3 줄 초안

    | 3 | ⬜ (시작 전 커밋 · 발사 직전 stoic 끝 = 핀) | 시도 2 의 명령 줄 그대로 (블록 ATTEMPT=3 · 한도 ⬜ — 권고 1500000 = 시도 2 와 같은 값 · 반복 수 · 시간을 견줄 수 있게) |
    ⬜ 핀 = Q2 · Q11 코드 묶음 반입 커밋 뒤 stoic 끝 | kgy · 같은 환경 (Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 · cupy 12.3.0) | ⬜ | ⬜ |

- 앞 조건: ~~S0 단계 1 을 새 코드로 다시 만든 뒤 (1-1 · 탐침 도구가 S0 단계 1 자료를 읽는다면 그 새 자료 · ⬜ 본 세션 확인)~~ → (3 판 · 대피 4 확인)
  탐침 도구는 S0 단계 1 계획 파일 하나 (`run_probe6.sh` 51 줄 `S0PLAN_REL`) 를 침대 이름 · tol_ff 대조에만 쓴다 (336–350 줄 · `probe6_read.py` 783–792 줄
  "identity only") — 코드 지문을 보지 않으므로 시도 3 은 S0 단계 1 다시 전에도 돈다.  다만 시도 2 짝 규칙의 "같은 코드" 경로 (`CODE_PATHS` 56 줄) 에
  `docs/data/rint2_s0_sbe_20261108/` 이 들어 있다 — S0 단계 1 다시의 자료를 그 폴더에 덮어 넣으면 도구 고침 (시도 3 짝) 때 함께 본다 ⬜ (새 폴더면 무관).
  차례 권고 = 1-1 의 S0 단계 1 다시 와 시도 3 은 서로 기다리지 않는다 (둘 다 kgy — 기계 하나면 차례로).
- **도구 고침이 먼저 필요하다** (원장 줄 둘): 지금 `run_probe6.sh` 는 시도 1 · 2 만 안다 (`p6log_a1_*` · `a2_*` · 짝 1 → 30000 · 2 → 1500000 ·
  236–251 줄 — 11-12 대피 세션에서 줄 번호 다시 확인) → 시도 3 짝 (3 → ⬜) 과 앞 조건 (끝난 시도 2) 을 더하는 고침 = 시험 먼저 · 내부 반박 리뷰.
- **시도 3 은 저장본 끔으로 돈다** — 도구가 러너 env 를 고정하고 `CJUNC*` 를 지운다 (`run_probe6.sh` 65–66 · 434 줄) → 잴 수 있는 것 = C 꼴 풀이 시간 ·
  반복 수 (+ 새 코드의 준비 시간).  저장본 쓰기 · 읽기 비용 · **실침대 원장이 저장 꼴 안인지** 는 R 의 첫 두 SBE 팔 (바닥 = 빗나감 → 짓고 씀 ·
  천장 = 같은 원장 적중) 에서 처음 나온다.
  ⬜ 1저자 결정: (가) 그대로 · (나) 도구에 `CJUNC_STORE` 를 더해 시도 3 (빗나감 = 짓고 씀) · 4 (적중) 두 줄로 잰다.  ★ 2 판 권고 = **(나) 쪽으로 기운다**
  — 1 판은 (가) 를 권했으나 넘겨받은 구현이 실침대 꼴 (instance 여럿) 에서 저장을 못 하던 결함이 픽스처로는 안 보였다 → 실침대에서 "새로 지어 저장" ·
  "읽음" 두 줄을 R 발사 전에 한 번 보는 값이 크다 (R 첫 팔에서 처음 보면 이득이 없을 때 되돌릴 틈이 없다).  비용 = 도구 고침 범위가 는다 (env 한 칸 ·
  원장 줄 하나 더) ⬜.

## 2-b. (4 판 · RCP-04) S0 단계 1 다시 + 실침대 저장본 재기 — 블록 `s0probe/s0_rerun_probe_block.txt` (실행 = 1저자 · kgy)

- 무엇: 1-1 의 S0 단계 1 다시 (SBE · kgy · CPU 약 1.5 h) 를 감싸개 (`s0_store_probe.py` · 블록 안 heredoc · md5 관문) 로 돌려, S0 가 원장을 지은
  직후 같은 프로세스에서 ① 저장 꼴 안인가 (encode_strict) ② 짓고 씀 (`Store.get_or_build` · 발행 전 다시 읽기 대조 포함) ③ 새 Store 로 다시 → 적중
  ④ 읽은 원장 = 지은 원장 (엄격 지문 · registry_fp) ⑤ ②–④ 의 메모리 최고값 (VmHWM 되돌림) 을 잰다 → 로그 폴더 `store_probe.json` · 화면 한 줄.
  S0 에는 **지은 그 원장 객체**를 그대로 돌려준다 — S0 출력 = 감싸개 없이 돈 것과 같다 (elapsed_s 만 다르다 · 재기 초가 들어간다 → 시간 표에는
  `store_probe.json` 의 초를 빼서 쓴다 · S0 보고에는 메모리 칸이 없고 감시 셸 rss.log 의 표본 최대에 재기 몫이 섞인다 → 채택 대조 때
  `store_probe.json` 의 ②–④ 구간 (VmHWM · 시각) 으로 가린다).  재기가 실패해도 (예외 · 메모리 부족) S0 는 계속한다 (사유 기록).  σ · 솔브 없음.
- 저장본 폴더 = 새 `~/sdcp/cjstore_s0probe_<UTC>` (재기 전용 · **R 은 그 파일을 읽지 않는다** — 단계 1 원장은 s_min 미등록 (None) 이라 R 팔 (봉인
  s_min) 과 열쇠가 다르다 · 보고 뒤 지워도 된다).  단계 1 원장은 R 팔 원장보다 instance 가 같거나 많다 = 크기 · 시간의 보수 쪽 어림.
- 블록 꼴 = 기존 kgy 블록 (⑥ 탐침) 과 같은 관문: PIN = 가지 끝 (fetch 뒤 대조) · BASE · 핀 작업 트리 (`~/dem-s0-<pin9>` · 깨끗함 · `cjunc_store.py` 있음) ·
  새 폴더 셋 · 앞 S0 로그 폴더가 끝 표지 없이 남아 있으면 멈춤 (동시 실행 막기) · 감싸개 · 감시 셸 md5 · 감시 셸 = 11-06 run2.sh 꼴 (5 초 RSS 표본 ·
  `rc=<n>` 한 줄 = 반입 도구 `docs/data/rint2_s0_sbe_20261108/tools/import_s0_tgz.py` 그대로 읽힘) + 끝에 `out_sha256.txt` · 로그 폴더 + 출력 폴더 묶음
  `~/s0log_<UTC>.tgz` (+ sha256) · `DONE`.  ASCII 만 · 느낌표 · 탭 · CR 없음 · nohup 없음 (setsid).  `PROBE=0` = 감싸개 없이 (11-06 꼴 그대로).
- 스크래치 확인 (이 컨테이너 · 가짜 HOME · kgy 판 Python 3.8.20 · numpy 1.24.4 · scipy 1.10.1 · S0 시험 픽스처 킷 kit_J 를 `kit_SBE_vgcf100` 이름으로 ·
  복사본 블록에서 두 줄만 바꿈 = PIN 채움 · 픽스처 격자 `--vox 0.1`): rc 0 · DONE · 묶음 → 반입 도구 = `ADOPT_CANDIDATE` (rc 0 · 여섯 출력 · 계획 sha
  대조) · S0 보고 git_head = 핀 · git_dirty False · 재기 = instance 2 · built_written → hit · 같음 (엄격 · registry_fp) · `PROBE=0` 길 rc 0 (저장본
  폴더 안 만듦) · 멈춤 셋 (PIN 안 채움 · 끝 표지 없는 앞 로그 폴더 · PIN ≠ 가지 끝) = rc 2 · 아무것도 안 띄움.  감싸개 있음 ↔ 없음 S0 출력 (같은
  `--out` 자리 · 3.11 · 3.8) = 계획 바이트 · 배열 · 보고 잎 같음 · 다른 잎 = `elapsed_s` 하나.  감싸개 실패 (폴더 0777 → ValueError) = 기록 · S0 rc 0.
  실기계 (kgy) = [미확인].

| 결과 전 기대 (먼저 적음) | 근거 |
|---|---|
| E1 S0 rc 0 · 여섯 출력 · 반입 도구 채택 후보 · git_head = PIN · git_dirty False | 11-08 실측 (5,383 s · 표본 최대 RSS 5.43 GiB) · 스크래치 모의 |
| E2 감싸개 호출 1 번 · instance **117,583** (11-08 SBE 같은 침대 · 원장 코드 `carbon_junction.py` · `fibre_segment_raster.py` 는 11-08 핀 뒤 그대로) | 11-08 S0 보고 `junction_census.census.n_instances` 117,583 · `git log f47bde0f6..` (일곱 파일 가운데 바뀐 것 = step3_sigma · payload 둘) |
| E3 encode ok · 쓰기 `built_written` · 읽기 `hit` · 같음 = 엄격 True · registry_fp True · error None | 픽스처 · 합성 꼴 시험 |
| E4 S0 의 계획 · 배열 = 11-08 과 같음 (코드 지문 · 시각 칸 빼고) | S0 계산 길 = 바뀐 두 파일의 바뀐 자리 (GPU 풀이 · 저장본 배선) 밖 · ⬜ 대조 = 본 세션 (반입 때) |

| 문턱 [제안 · ⬜ 1저자] | 넘으면 |
|---|---|
| T1 쓰기 (`seconds_write`) ≤ 600 s · 읽기 (`seconds_read`) ≤ 300 s · 읽기 ≤ 짓기 (`seconds_build`) 의 10 % | 보고 — R 팔마다 이득 = 짓기 − 읽기 가 작아진다 (근거 = 합성 어림 47 만 멤버 쓰기 ≈ 10 s · 읽기 ≈ 26 s (이 컨테이너) 의 10 배 여유) |
| T2 메모리 증가 (VmHWM(②–④) − VmRSS(① 앞)) ≤ 4 GiB | 보고 — R 팔 (⑥ 시도 2 RSS 최대 32.9 GiB) 에 더해질 몫 · kgy 총 메모리 [미확인] |
| T3 파일 크기 ≤ 2 GiB | 보고 — 기계마다 폴더 하나 · 침대 · origin · 문턱마다 파일 하나 |
| E3 어긋남 (쓰기 `built_write_skipped` = 저장 꼴 밖 · `built_write_failed` · `disabled` = `/etc/machine-id` 를 못 읽음 (기록 칸 `store_machine_id_read` False · R 에서도 저장본 꺼짐) · 읽기 ≠ hit · 같음 False · error) | ★ R 에서 `--cjunc-store` 를 쓰지 않는다 (그 침대의 이득 0 또는 결함) · 본 세션에 알림 · 고친 뒤 다시 잰다 |

- ⬜ 1저자 질문 Q-B (RCP-04): (가) 공식 S0 단계 1 다시를 감싸개로 (`PROBE=1` · 블록 기본 · CPU 1.5 h 아낌 · 선례 = 11-06 · 11-08 S0 의 `probe2.py`
  감싸개 (스택 기록) · 채택 대조 표에 감싸개 md5 · "원장 객체 그대로 돌려줌 · elapsed_s 에 재기 초" 한 줄) / (나) 공식 다시는 `PROBE=0` 으로 따로 ·
  같은 핀 · 같은 킷으로 `PROBE=1 TAG=storeprobe_dev` 개발 런 한 번 더 (CPU 약 1.5 h 더 · 공식 산출 무관 · 블록이 앞 런의 DONE 을 기다린다).
  권고 = (가) — 출력 같음은 픽스처 대조가 보이고, 메모리 여유가 크다 (5.4 GiB 표본 최대) · 커널 OOM 처럼 감싸개가 못 잡는 실패면 (나) 로 다시.

## 3. 남은 계획 (`docs/reviews/rint2_siteq_remaining_plan_20261110.md`) §10 문장 초안

> (11-12) Q2 · Q11 코드 묶음 = 작업 트리 시험 먼저 → 구현 (보고) → 내부 반박 리뷰 (독립 조수 · Codex 아님) → 고침 → 본 리포 반입 · 게이트
> (`scripts/test_step3_gpu_precond.py` · `scripts/test_cjunc_store.py` · `scripts/test_cjunc_store_e2e.py` = 게이트 세 단계 (끝-끝 = 따로 한 줄 ·
> 7–10 분) + kgy 판 스크립트 `scripts/check_kgy_py38.sh` 16 묶음 · 4 판 배선 끝) → 원장 시도 3 줄 → S0 단계 1 다시 + 저장본 재기 (kgy · CPU · 2-b) →
> ⑥ 시도 3 → GPU 확인 블록
> (1저자 · kgy · gabia) → 시간 표 다시 (B-6 · E-4 · 재사용 이득은 GPU 팔 쪽만) → Codex 봉인 전 묶음 → 계획 §10 숫자 (maxiter · 시간 상한) → 봉인 →
> R (`--cjunc-store <기계마다 폴더>`).

- ~~이 조수는 게이트 목록 (`scripts/check_all.sh` · CI yml) 과 kgy 판 스크립트를 **고치지 않았다**~~ → 4 판 (RCP-02): `scripts/check_all.sh` 세 단계 ·
  `scripts/check_kgy_py38.sh` 세 묶음 (16) 을 넣었다 (커밋 `0ac6edf3c`) · CI yml 은 Rint `test_*.py` 줄이 없어 그대로 · 규칙 K 손목록 · 자기검사 등재 무관 (규율 repo 0 오류).

## 4. GPU 확인 블록 = `gpu_check_block.txt` (같은 폴더 · 2 판 — 자리표 Q11PIN · sha256 채움 · Q11REPO = 본 세션)

- 옛 모듈 sha256 `8d428ff5…f2ec` = `11a794674:scripts/step3_sigma.py` · 새 모듈 sha256 `45d645a2…4ceb9` = `f17ea8c6b:scripts/step3_sigma.py` (대피 세션에서 `git show
  | sha256sum` 으로 다시 확인 · 넘겨받은 값과 같다 — Q11 쪽 코드는 넘겨받은 그대로).
- Q11PIN = 구현 커밋 (지금 = 작업 트리의 `f17ea8c6be8504ffdaa057e40c0c505c666fdfbe` · 반입하며 sha 가 바뀌면 그 값으로 · 새 모듈 sha256 은 파일 내용이
  같으면 그대로).

### 4-b. (3 판 · 대피 4) 블록 확인 — 돌리지 않은 것 · 돌린 것

- 블록의 하네스 글 (heredoc 사이) md5 = `acfeb4b4e1515d6aa7d46ddaf67e6e68` = 블록 관문 값 · 블록에 탭 · CR · 느낌표 0 · 두 모듈 sha256 = 블록 값
  (`git show 11a794674:` · `f17ea8c6b:` 다시 셈).
- CPU 흐름 (하네스 `--backend numpy` · n-side 24 = 13,824 미지수 · 같은 두 모듈): 3.11 · kgy 판 3.8 둘 다 다섯 짝 (대조 둘 · 짧게 · 주 풀이 · 이어 풀기)
  해 바이트 · info · 반복 수 · LAST_BACKEND 같음 · 주 풀이 267 반복 · 이어 풀기 37 반복.  ⚠ CPU 길은 Q11 이 바꾸지 않았다 = 하네스 흐름 확인일 뿐
  (C 꼴 · 반복당 시간은 GPU 에서만).
- 블록 셸 관문 모의 (HOME = 스크래치 · `$HOME/dem-mt` = 작업 트리 심볼릭 링크 · 빈 activate · 3.11 · cupy 없음): md5 · PIN 꼴 · 두 커밋 있음 ·
  git show · sha256 관문을 지나 하네스가 `import cupy` 에서 ERROR rc 1 (기대 · 결과 파일 둘 씀).  GPU · cupy 12.3.0 길은 [미확인] (1저자 실행).
- Q11PIN: 반입 (cherry-pick · 서명) 뒤 sha 로 바꿔 적는다 — 시험 보강 커밋은 `scripts/step3_sigma.py` 를 바꾸지 않으므로 그 커밋 sha 를 넣어도 같은 모듈
  (sha256 관문 값 그대로).  gabia 의 Q11REPO 자리 = [미확인] (본 세션).

### 4-c. (4 판 · 리뷰 고침 뒤) 블록 갱신

- 리뷰 고침 `94765bed3` (RCP-08) 이 `scripts/step3_sigma.py` 를 다시 바꿨다 → 새 모듈 sha256 = **`859310da…b459a`** (`94765bed3` · `0ac6edf3c` 같은 파일 ·
  `git show | sha256sum`) · Q11PIN 자리 = `0ac6edf3cf4a0631a9291e0ec7dec3cb04c18b64` (반입 뒤 sha 로 바꾼다 · 새 모듈 sha256 과 내용이 같은 커밋이면 된다).
  하네스 글 (md5 `acfeb4b4…`) 은 그대로 · 3 판 사본 = `gpu_check_block_v3.txt`.
- 다시 돌림: CPU 흐름 (`--backend numpy` · n-side 24) 3.11 · kgy 판 3.8 둘 다 다섯 짝 비트 같음 · 주 풀이 267 · 이어 풀기 37 (CPU 길 = Q11 무관 = 흐름
  확인) · 블록 셸 관문 모의 (가짜 HOME · 빈 activate) = md5 · PIN · 두 커밋 · git show · sha256 관문 통과 → cupy 없음 ERROR rc 1 (기대).  GPU 길 = [미확인] (1저자).

### 4-d. (5 판 · 2 회차 고침 뒤) GPU 확인 블록 갱신

- 2 회차는 `scripts/step3_sigma.py` 를 바꾸지 않았다 → 새 모듈 sha256 = **`859310da…b459a`** 그대로 (`git show 609d78ca4:scripts/step3_sigma.py
  | sha256sum` 다시 셈) · 옛 `8d428ff5…f2ec` 그대로 · 하네스 글 md5 `acfeb4b4…` 그대로 (heredoc 바이트 같음) · Q11PIN 자리 = 작업 트리 끝 커밋
  `609d78ca43ad472025346d3973f0c49a23ec52c5` (반입 뒤 sha 로 바꾼다 · 새 모듈 sha256 과 내용이 같은 커밋이면 된다) · 4 판 사본 = `gpu_check_block_v4.txt`.
- 다시 돌림 (5 판 · 핀 609d78ca4): CPU 흐름 (`--backend numpy` · n-side 24) 3.11 · kgy 판 3.8 둘 다 다섯 짝 비트 같음 · 주 풀이 267 · 이어 풀기 37
  (CPU 길 = Q11 무관 = 흐름 확인) · 블록 셸 관문 모의 (가짜 HOME · `$HOME/dem-mt` = 작업 트리 심볼릭 · 빈 activate) = md5 · PIN · 두 커밋 · git show ·
  sha256 관문 통과 → cupy 없음 ERROR rc 1 (기대).  GPU 길 = [미확인] (1저자).

### 4-e. (6 판 · 같은 부류 셋 뒤) GPU 확인 블록 갱신

- 같은 부류 셋은 시험 모듈 셋만 바꿨다 (`scripts/step3_sigma.py` 그대로) → 새 모듈 sha256 = **`859310da…b459a`** 그대로 (`git show ea3b13b89:scripts/step3_sigma.py
  | sha256sum` 다시 셈) · 옛 `8d428ff5…f2ec` 그대로 · 하네스 글 md5 `acfeb4b4…` 그대로 (heredoc 바이트 같음) · Q11PIN 자리 = 작업 트리 끝 커밋
  `ea3b13b893b0161dac5b863da3b315ca332d9f32` (반입 뒤 sha 로 바꾼다) · 바뀐 줄 = 머리 주석 다섯 + Q11PIN 하나 · 5 판 사본 = `gpu_check_block_v5.txt`.
- 다시 돌림 (6 판 · 핀 ea3b13b89): 블록 셸 관문 모의 (가짜 HOME · `$HOME/dem-mt` = 작업 트리 심볼릭 · 빈 activate) = md5 · PIN · 두 커밋 · git show ·
  sha256 관문 통과 → cupy 없음 ERROR rc 1 (기대).  CPU 흐름은 다시 돌리지 않았다 (하네스 · 두 모듈 바이트 = 5 판과 같음).  GPU 길 = [미확인] (1저자).
