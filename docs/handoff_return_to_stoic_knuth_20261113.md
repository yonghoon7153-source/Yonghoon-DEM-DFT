# 대피 세션 → 본 세션 (stoic) 비 Rint 인계 (2026-11-13 · 1저자 *"토큰 부족해서 다른것들은 일단 다시 origin 브랜치로 넘기고 Rint에만 집중하자 · 지금 돌던것만 딱 마무리하고 믹서등"*)

> **한 줄**: 11-12 에 본 세션에서 넘겨받은 일 가운데 **Rint ② 와 litdb 1 순위 (N-51 까지) 만 대피 세션 (pqwtv8) 에 남기고**, 나머지 (믹서 E0 · P1 G2c′ · 메모 3.2 · 그 밖) 를 본 세션 (stoic) 에 돌려준다.  돌던 조수 둘 (믹서 등록 초안 채우기 · P1 A·B 자체 리뷰 5 회차) 은 마친 뒤 결과를 묶음에 넣었다.  결과 0 건 · 실행 0 건 (이 커밋에서).

## 0. 붙여 넣을 프롬프트 (본 세션 첫 메시지)

```
대피 세션 (pqwtv8) 이 비 Rint 일을 돌려준다 (1저자 11-13). Rint ② · litdb 1 순위는 대피 세션이 계속한다.
1. git fetch origin claude/stoic-knuth-NObVQ claude/sdcp-dem-manuscript-si-pqwtv8
   → origin stoic 이 af3cce37b 그대로인지 확인 → stoic 을 origin pqwtv8 끝으로 fast-forward → push
   (게이트 = 대피 세션이 인계 커밋에서 두 조각 통과 · 다시 불필요 · 그 뒤 대피 세션이 Rint 커밋만 더 올렸으면 그것도 같이 FF 해도 된다).
2. docs/handoff_return_to_stoic_knuth_20261113.md 를 끝까지 읽고 그대로 한다.
   묶음 docs/handoff_20261113/nonrint_bundle_20261113.tgz 를 빈 scratch 폴더에 풀어 (python -I · tarfile · 보통 파일만) 이어간다.
3. Rint ② 파일 (인계 문서 §2 목록) 은 손대지 않는다. 새 SELF 번호 = 171 부터 (대피 세션 = 180 부터).
```

## 1. 무엇이 어디로

| 트랙 | 맡는 곳 (11-13 부터) | 비고 |
|---|---|---|
| **[Rint ②]** 코드 묶음 · ⑥ 다시 재기 · siteq 본 현장 확인 · gabia 킷 scripts 링크 · Codex 봉인 전 묶음 · R 런 | **대피 세션 · pqwtv8** | 1 순위 · 기한 (GPU 팔 12 월 초) |
| litdb 1 순위 (N-48 · N-49 · N-50 · N-51) → 1 순위 종합 보고 · 추가 필요 논문 정리표 | **대피 세션** (정본 가지) | 2 · 3 순위 · 보강 = 일요일 (11-15) 뒤 · 맡을 세션 = 1저자 |
| [DEM 우선] Ⓒ 믹서 E0 자격 pilot | **본 세션** | §3-1 |
| [DEM 우선] P1 G2c′ A · B (REG §15 · MPI 2 차 등록) | **본 세션** | §3-2 |
| [DEM 우선 (수영)] 메모 3.2 → Codex 재리뷰 → 계획서 페이지 · docx | **본 세션** | §3-3 |
| `SELF-170` (믹서 selftest 거짓 실패 · P3 open) | **본 세션** (믹서 재봉인 묶음과 함께) | §3-4 |
| 11-12 인계서 §5 의 나머지 (Codex 비 Rint 반입 · litdb 웹앱 '최근' 띠) | **본 세션** | 대피 세션은 손대지 않았다 |

## 2. 가지 — 두 세션이 따로 쓰고 나중에 합친다

| 가지 | 지금 | 규칙 |
|---|---|---|
| `claude/stoic-knuth-NObVQ` (stoic) | origin = `af3cce37b` (11-12 동결 그대로) | 본 세션이 pqwtv8 끝으로 **fast-forward** 한 뒤 비 Rint 커밋을 올린다 |
| `claude/sdcp-dem-manuscript-si-pqwtv8` (pqwtv8) | 이 인계 커밋 = 끝 | 대피 세션이 **Rint ② 만** 이어 올린다 (fast-forward 만) · stoic 엔 쓰지 않는다 |
| `claude/friendly-meitner-lldvar` (litdb 정본) | 두 세션 조수가 같이 push | push 전 fetch · rebase (지금처럼) |

- **다시 합치기** (1저자가 "Rint 복귀" 라 할 때): 본 세션이 `git log <FF 한 커밋>..origin/claude/sdcp-dem-manuscript-si-pqwtv8` 의 Rint 커밋을 `cherry-pick -x` (서명) 로 stoic 에 올린다 (10-27 단계 B 와 같은 꼴) → 게이트 → push.  공유 기록 (CLAUDE.md · 진행 기록 · `docs/reviews/findings.json`) 은 두 쪽 줄을 다 남겨 손으로 푼다.
- **SELF 번호가 겹치지 않게**: 본 세션 = `SELF-171` 부터 · 대피 세션 = `SELF-180` 부터 (원장 검사기는 번호 연속을 요구하지 않는다).
- **대피 세션이 고치는 파일 (Rint ②)** — 본 세션은 되도록 손대지 않는다 (고쳐야 하면 합칠 때 충돌을 손으로 푼다): `scripts/step3_sigma.py` · `scripts/run_contract.py` · `scripts/rint_r_chain.py` · `scripts/cjunc_store.py` · `scripts/ca_ext_cjunc.py` · `scripts/ca_s0_census.py` · `scripts/mpm_webapp_payload.py` · `scripts/sdcp_gain_vox015_8arm.sh` · `scripts/check_all.sh` · `scripts/check_kgy_py38.sh` · `scripts/check_method_discipline.py` · `scripts/check_review_findings.py` 와 그 시험 (`scripts/test_rint_r_chain*.py` · `scripts/test_cjunc_store*.py` · `scripts/test_ca_s0_census.py` · `scripts/test_git_env_isolation.py` · `scripts/test_step3_conv_cert.py` · `scripts/test_step3_gpu_precond.py` · `webapp/test_pipeline_provenance.py`) · `docs/reviews/rint2_*` · `docs/data/rint2_*`.  ⚠ `scripts/check_all.sh` 는 두 쪽이 다 단계를 더할 수 있다 — 합칠 때 둘 다 남긴다.

## 3. 트랙별 상태 · 다음

### 3-1. [DEM 우선] Ⓒ 믹서 E0 자격 pilot

| 항목 | 상태 | 근거 | 다음 / 1저자 결정 |
|---|---|---|---|
| 등록 초안 (2 회차 고침 판 + 보충 조회 채움) | 732 → 767 줄 · 바꾼 곳 51 · 결과 전 규칙 · 문턱 · 판정선 무변경 (문턱 값 등장 수 고치기 전 · 뒤 같음) · 확인된 [추정] 4 · 닫힌 [미확인] 8 | 묶음 mixer_e0_v2/e0_pilot_registration_draft.md · 처분 mixer_e0_v2/fill_queryb_disposition.md | 1저자 비준 → 리포 반입 (커밋 P) |
| 내부 반박 리뷰 (Codex 아님 · 11-10 운영 결정 = 이 한 팔만 Codex GO 를 대신) | 두 회 + 고침 두 회 | 묶음 mixer_e0_v2/review/ | — |
| 보충 조회 (q9b · q2b · q7b · 1저자 11-12 22:08 UTC ibb) | 판독기 rc 0 · q9b 9 로그 허용 꼴 밖 0 · 보고 쌍 표 = 덱 기대 9/9 · q2b r1 세 장 끝 개행 · 개행 = 9 + 원자 · q7b 7/7 · 11-10 과 로그 크기 · 시각 9/9 · JSON 이름 7/7 같음 · 가림 grep 0 | 원자료 (가린 사본 그대로) = 이 커밋 `docs/data/mixer_e0_queryb_ibb_20261112/` | — |
| 본 세션이 정할 메모 넷 (1저자 결정 필요는 없음) | q7b 봉인 값 = 보충 조회 기준 (넣을 자리 = 재봉인 단계) · 기준 표 9 칸 미수정 (범위 밖) · changes.md 이 회차 절 없음 · 판독기 반입 여부 (W9 대조에 쓰임) | 처분 5 절 | 커밋 P 때 정함 |
| 재봉인 (커밋 A · B · 별도 승인) | 예행 = 묶음 mixer_e0_v2/reseal_dry/ · mixer_e0_v2/fix_q5/ | — | `SELF-170` 고침을 같은 묶음에 (도구 해시를 한 번만 바꿈) · 발사 GO = 1저자 |
| ⚠ 조수 지시서 위반 1 | 리포에서 `git log --oneline -5` 한 번 (읽기만 · 상태 변경 0 · 출력 미사용) | 조수 보고 | 기록만 |

### 3-2. [DEM 우선] P1 G2c′ A · B

| 항목 | 상태 | 근거 | 다음 / 1저자 결정 |
|---|---|---|---|
| A (REG §15 · 개정 4) · B (MPI 2 차 등록) | 리포 반입 (`3daa2c48a`) · 결과 0 건 · 구현 전 | `docs/reviews/dem_unloading_ps45_prereg_20261009.md` §15 · `docs/reviews/p1_g2c_mpi_stage2_registration_20261112.md` | — |
| Codex 설계 확인 요청 | Codex 사용량 소진 (리셋 11-16 14:38 KST) → 1저자 11-13 *"그냥 자체리뷰로 우선 보내봐"* | `docs/reviews/codex_p1_g2c_ab_design_request_20261112.md` | — |
| 내부 반박 리뷰 5 회차 (Codex 아님 · 요청서 Q1–Q6 그대로) | **조건부** (11-13 · 핀 `3daa2c48a` ZIP 만 · 결과 0 건) — Q1 · Q2 · Q3 · Q5 조건부 수용 · Q4 수용 · Q6 = 들어와야 할 것 둘 (다시 읽기 산출 자리 · 30 열 덤프 ID 열) · 새 지적 P1 0 · **P2 1** (`SR5-01` 키트 restore 를 다시 돌리면 증서 restore_verdict.json 이 그대로 덮임 → A 15-5 의 '런 때 증서 그대로' 가 서지 않음 · 합성 실증 = 앞 시도 RESTORED → SYNTAX_FAIL · 정직한 흐름에서는 RESTORED → UNCONFIRMED 로 덮여 U 관문이 닫힘 (틀린 결과를 받아들이지는 않음)) · P3 7 (`SR5-02` ID 열 사전에 두 열 빠짐 · `03` 결합 줄 중복 = 뒷줄로 덮임 · `04` B 시도 셈 빈칸 셋 · `05` PFA2-03 글대로면 S0 ID 집합 바뀜 · `06` 15-5b = shear 이력 소실만 (deltaMax 어긋남 한정 한 줄) · `07` QA4 벽 관측 · post 목록 규칙 · fixture 머리 범위 10–56 · `08` 요청서 표지 · 고치기 전 판 sha 일곱) · 4 회차 고침 PFA2-01 · 02 · 03 · 04 닫힘 · 05 = A 닫힘 · 요청서 부분 · 3 회차 PFA-07 (b) 닫힘 주장 = 안 섬 (= SR5-01) · 숫자 대조 맞음 (어긋남 둘 = SR5-08) · 사본 시험 41/41 | 묶음 p1_selfreview5/review5_AB.md (+ review5/) · 지시서 p1_selfreview5/BRIEF_review5_AB.md | 구현 (시험 먼저) **전에** A · B 개정 5 회차 = `SR5-01` + `02` · `03` · `04` · `07` 규칙 문장 고침 (`05` · `06` · `08` 같은 묶음) → 짧은 재확인 여부 = 1저자 → 구현 → 건식 · 샌드박스 NP 2 · 4 (1저자 GO · ibb) |
| 실제 RJ 발사 GO | 그대로 Codex (요청서 머리 QA5) | — | 리셋 뒤 · B 결과 · 이 자체 리뷰를 붙여 한 번 |

### 3-3. [DEM 우선 (수영)] 메모 3.2

| 항목 | 상태 | 근거 | 다음 |
|---|---|---|---|
| 메모 3.2 | 내부 반박 리뷰 다섯 회 · 5 회차 반입 (`a0455e90b`) · 바뀐 권고 Q6 · Q10 · Q13 | `docs/reviews/dem_redesign_direction_20261109/memo_v3_2.md` · CLAUDE.md [DEM 우선 (수영)] 줄 | Codex 재리뷰 (리셋 뒤 · DRD 판정 대응) → 계획서 웹앱 페이지 · docx 다시 (원문 briefing_ko 3.2 반영) |

### 3-4. `SELF-170` (P3 · open)

- 원장 메모대로 — 믹서 selftest ⑮ · ⑯ · ㉓ 의 값 누출 검사가 µs 타임스탬프 숫자와 글자로 겹치면 거짓 실패 · 고칠 방향 = 바늘 앞 글자가 숫자가 아닐 때만 누출로 셈 + 합성 문자열 시험 · 시계 고정 사본 전 ✗ → 뒤 ✓.
- 재현 자료 = 묶음 self170/ (시계 고정 사본 · 진단 로그 · 메모).  고침은 믹서 재봉인 묶음과 함께 (도구 sha256 = E0 기록 봉인 도구).

### 3-5. Codex (리셋 11-16 14:38 KST) — 보낼 순서 권고

1. Rint ② 봉인 전 묶음 (대피 세션 · 1 순위 · 기한)
2. P1 RJ 발사 GO (본 세션 · B 결과 붙여)
3. 메모 3.2 재리뷰 (본 세션)

## 4. 묶음 `docs/handoff_20261113/nonrint_bundle_20261113.tgz`

- 담은 것: mixer_e0_v2/ (등록 초안 모든 판 · 기준 표 · 바뀐 것 · 리뷰 · 처분 · 지시서 · 조회 블록 둘 (시험 사본 뺌) · 재봉인 예행 (런 사본 뺌) · Q5 고침 · 채우기 재현 스크립트) · p1_selfreview5/ (지시서 · 리뷰 · 스크립트 · 출력 · 풀린 ZIP 사본 뺌) · self170/ · evac_STATE_20261113.md (대피 세션 상태 메모 사본) · MANIFEST.tsv (파일마다 바이트 · sha256).
- 가림: scratch · 홈 · lustre · 업로드 경로 = 자리표 (`<SCRATCH>` · `<HOME>` · `<LUSTRE_HOME>` · `<UPLOAD>`) · 가린 뒤 IPv4 · 포트 · ssh · 홈 · 노드 꼴 · 철회값 등록부 문자열 = 0 (흔적 검사 = 묶는 스크립트가 셈).
- sha256 = 2dc4e8af7eb37d521bd1961c1645cfb9845f9cb9f2d7ef433c5bf858f6333cc5 · 877133 B · 파일 186.
- 푸는 법: 빈 scratch 폴더에서 `python3 -I -c "import tarfile,sys; tarfile.open(sys.argv[1]).extractall(sys.argv[2], filter='data')" <tgz> <빈 폴더>`.

## 5. 그대로 지킬 규칙 (원문 = CLAUDE.md)

커밋 하나 → 게이트 두 조각 (`CHECK_ALL_RANGE=1-125` · `126-끝` · 같은 HEAD · fail 0 · Bash 배경 · timeout 7200000 · 줄이지 않음) → push · 로컬 커밋 쌓지 않기 · 받은 원자료는 기록 폴더에 먼저 넣어 push · 주소 · 포트 · 계정 · 홈 경로 = 채팅만 (리포는 공개) · 조수 지시서: 시스템 패키지 설치 · 설정 변경 금지 (`SELF-168`) · `GIT_DIR` · `GIT_WORK_TREE` · `GIT_INDEX_FILE` export 금지 (`SELF-169`) · 신호 실험 = `unshare -pf --mount-proc --kill-child` 안 (`SELF-164`) · Codex 아님 리뷰는 verified 로 올리지 않는다 (11-10 운영 결정).
