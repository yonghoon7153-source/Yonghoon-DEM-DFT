---
title: 회신 BH — C-12 v32 내부 다중 감사 (7렌즈 · 3인 반박 · NO-GO · P0 1 · P1 6)
date: 2026-09-03
updated: 2026-09-03
tags: [review, internal, sdcp, c12, vasp, reply, multi-agent]
status: 회신반영
kind: review-reply
system: sdcp
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-03
verifiedBy: "Workflow wf_af6690aa-71e (7 finder · 11 P0/P1 × 3 verifier · 1 synth) · P0 이행 커밋 a0c35a1d · P1 이행 576c5b9e·32c4b730"
campaign: sdcp_c12_vasp_handoff
reviewer: 내부 다중 감사 — 7 렌즈(contract_vs_gates · runner_sim · reanalysis_sim · audit_chain · doc_consistency · physics_binding · residual_p1) → P0/P1 마다 3인 반박(repro · scope · posthoc) → 종합
target: v32 번들 (zip ae72a179… · 생성 커밋 008f1c05) · 생성기 tools/sdcp/vasp_handoff_bundle.py
verdict: NO-GO — SEAL 이 VASP 버전 아닌 줄을 봉인 → 1단계 ~300 h 뒤 ROOT_SEAL_VASP_MISMATCH 로 전건 차단 · 현장 회복 불가
---

> ⚠ **원문 소실 주의.** 이 감사는 Workflow(다중 에이전트)로 돌았고 종합 판정은 세션
> 컨텍스트로만 전달됐다. 그 직후 세션 한도 리셋으로 **컨테이너가 재생성**돼 저널
> (`journal.jsonl`)과 에이전트 전사가 전부 사라졌다. 아래는 종합 판정 본문을 세션
> 컨텍스트에서 **복원**한 것이다 — P0·P1 전문은 그대로이고, P2 목록과 "확인한 것" 은
> 전달 시 이미 일부 절단돼 있었다(그 자리를 표시했다).
>
> 교훈: 다중 감사 결과는 **받는 즉시 kb/reviews/ 에 커밋**한다. 발송 메일(SEND_MAIL_v34)이
> 이 파일을 가리키는데 실물이 없던 것을 렌즈5(v34 감사)가 P2 로 잡았다.

---

**NO-GO** — 봉인 스크립트가 `vasp_std --version 2>&1 | head -1` 의 첫 줄을 VASP 신원으로 봉인하는데, 실물 VASP 의 stdout 첫 줄은 버전 줄이 아니라서(ASE 실물 표본: 5번째 줄) 1단계(최장 잡 ~300 h) 뒤 `--gate vacconv` 가 `ROOT_SEAL_VASP_MISMATCH` 로 결정적으로 닫히고, 봉인·분석기는 files_sha256 에 결박돼 현장에서 고칠 수 없다 — 번들 재생성(v33)이 필요하다.

## P0 — 지금 발송을 막는 것

### P0-1. root 봉인의 `vasp_version_banner` 가 "stdout 첫 줄" 인데, 그 줄은 실물 VASP 에서 버전을 담지 않는다 → 1단계 완주 후 전건 게이트 · 현장 회복 불가
잡은 렌즈: reanalysis_sim(#4, 조건부 P1 로 제출) · residual_p1(#10, 같은 probe 의 stage-2 불변량 문제) — 두 렌즈가 같은 뿌리의 두 얼굴을 잡았고, 6표 중 5표가 P0 로 올렸다. 종합자도 P0 로 확정.

확인한 사슬 (번들 사본 zip sha256 `ae72a179…0c82` · MANIFEST `f30f2b27…` · SEAL `035f2cc3…` 일치):
1. 봉인 생성 — `SEAL_POTCAR_ROOT.sh:216-220` `VASP_VER=$("$VASP_BIN" --version 2>&1 | head -1 || true)` — cwd 는 번들 루트, launcher 없이 직접 기동, timeout 없음, stderr 병합, 실패도 `|| true` 로 삼킨다. 배너 내용 검증은 없다.
2. 사전 검사 어디에도 배너 **내용** 검사가 없다 — `census.py:51-58`(RECHECK_SEAL)은 키가 비어 있는지만, `run_staged.sh:258-292` 는 경로·sha256·wrapper 만, `analyze_results.py:8390`(--check_governance)은 jobs 가 비어 `_obs_ver` 가 없으므로 침묵.
3. 비용 발생 뒤 첫 판정 — `analyze_results.py:5311,5335` 가 각 잡 static OUTCAR 의 `vasp_version`(:614 정규식 `vasp\.([\w.]+)`)을 모으고, :5555-5561 이 `v not in _seal_ver` 이면 `ROOT_SEAL_VASP_MISMATCH` 를 **blocking** 에 넣는다 → `potcar_identity.pass = not blocking` → :9788-9790 "2단계를 열지 않는다" `return 2` → `run_staged.sh:407-408` exit 2, `run_staged.sh 2` 도 거부. STAGE1_PASS.json 은 절대 나오지 않고, 우리 재분석도 같은 봉인을 읽어 전건 NO_VALUE.
4. 단위 재현(배포본 analyze_results.py import · `potcar_identity_gates` 실물 픽스처): selftest_fixture blocking=0 · vasp6_real_first_line blocking=1 `ROOT_SEAL_VASP_MISMATCH(봉인 배너 ' running    1 mpi-ranks…')` · vasp544_real_first_line blocking=1 · mpi_init_error blocking=1 · empty → ROOT_SEAL_INCOMPLETE_SCHEMA.
5. **첫 줄이 실제로 무엇인가** — ASE 실물 표본 `ase/test/calculator/vasp/test_version.py:3-8`: ` running on    1 total cores` / ` distrk: …` / ` distr: …` / ` using from now: INCAR` / ` vasp.6.1.2 22Jul20 (build …) complex` — 버전은 **5번째 줄**. VASP 는 argv 를 해석하지 않으므로 `--version` 은 그냥 기동이다. ⚠ 실제 VASP 로 돌리지는 못했다(VASP 없음).
6. 왜 어떤 시험도 못 잡았나 — 생성기 selftest stub `vasp_handoff_bundle.py:19068` 은 `echo 'vasp.6.4.1 24Jul23 (build selftest)'` **한 줄**이고 :19149 가 `startswith("vasp.6.4.1")` 을 단언한다. **잘못된 가정이 시험에 박혀** 422/422 PASS 가 이 결함을 보증하지 못한다.
7. 같은 뿌리의 부속 결함: `SEAL_POTCAR_ROOT.sh:310-317` 재실행 시 배너 **정확일치** 요구(host/PID/타임스탬프 섞이는 사이트면 2단계 SEAL 재실행에서 exit 1) · `MAKE_POTCAR_ATTESTATION.sh:89-90` 은 stdout **전체**를 `vasp_version_raw` 로 담고 분석기 :5639-5644 는 그것이 배너의 **부분문자열**이길 요구 → 정직한 attestation 도 `ATTESTATION_VASP_VERSION_MISMATCH` · probe 가 번들 루트에서 기동하면 루트에 OUTCAR 가 생겨 attestation 의 `find -name OUTCAR` 가 거부할 수 있다(미검증).

**왜 P0** — 판정 질문 네 가지 전부: (a) 문서대로 하면 1단계 끝에 러너가 멈추고 2단계가 안 열린다 (b) 계약대로 반송해도 재분석이 같은 게이트에서 전건 NO_VALUE (c) 그때 고칠 것은 결과가 아니라 게이트/봉인 코드 — 여덟 번 물린 양식 (d) 고치려면 SEAL·census·analyzer 가 든 새 번들 = 해시 사슬 전부 재발급.

**해제 조건**: ① probe 를 `( cd "$(mktemp -d)" && timeout 60 "$VASP_BIN" 2>&1 )` 전체 출력에서 `grep -a -m1 -E ' vasp\.[0-9][A-Za-z0-9.]*'` 로 고르고 없으면 **봉인 거부** ② 재실행 불변량은 원문 아닌 **버전 토큰** 대조 ③ census RECHECK_SEAL 이 토큰 부재를 거부 ④ analyzer :5555/:5639 · MAKE_POTCAR_ATTESTATION :89 를 같은 토큰 규칙으로 ⑤ stub 을 실물 순서(버전 5번째)로 + 음성시험 ⑥ v33 재생성 · IDENTITY ⑦ 을 기계 대조로 확장.

## P1 — 보내도 되지만 고칠 것 (사후 게이트 수정 유발 없음 — 전부 메일·문서 수준)

### P1-1. 메일 §2 실행 블록에 `PP`·`POTCAR_ALLOWLIST` 가 없다 — 메일대로 하면 `run_staged.sh:85` 에서 즉시 멈춤 · allowlist 만드는 법은 어느 문서에도 없다
잡은 렌즈: runner_sim · doc_consistency(P0 주장). 6표 P1 / 2표 P0. 종합 P1 — VASP 실행 전, 부작용 0, 변수명을 찍고 멈추는 설계된 fail-loud 이고 번들 README/SUBMIT 에는 두 변수가 있어 정본을 보면 복구된다. 단 **이 메일 그대로는 보내지 않는다.** `diff <(grep -o '^export [A-Z_]*' SEND_MAIL) <(… README)` → 차이 정확히 `PP`, `POTCAR_ALLOWLIST`. "여섯 개" 는 오기(블록 7줄, README·SUBMIT 9줄). allowlist 레시피는 `POTCAR_ASSEMBLE.sh:55` 의 "변수 미설정" 분기에만 있고 러너 경로에선 도달 불가.

### P1-2. 메일 §4 반송 목록에 dense 2잡의 `dense/OUTCAR`·`dense/OSZICAR` 가 없다 — 메일대로 반송받으면 primary 복합체 2잡이 `NOT_RUN(dense)` 로 죽어 D 자체가 안 나온다 (rc 2)
`MANIFEST.return_contract.dense_extra` · README:193-196 · SUBMIT:84-87 렌더 일치, 메일만 static 5종 + 루트 3종. 회신 AV P0-4(반송 계약 일원화)를 손으로 쓴 메일이 다시 깼다. 수정: 메일 §4 를 손으로 쓰지 말고 README 반송 절을 그대로 붙인다.

### P1-3. 반송 계약이 "파일 목록" 만 적고 "푼 디렉터리를 통째로(배포 입력·MANIFEST 포함) 반송" 이라는 문장이 없다 — 목록만 문자 그대로 보내면 분석기가 시작도 못 하거나(MANIFEST 없음 rc 1) 115 파일 '사라짐 → 변조' 로 exit 2
`analyze_results.py:8440-8447` 이 files_sha256 115개를 전부 요구하고 :9744-9751 에서 missing>0 이면 "삭제도 변조" exit 2 — 전부-missing 과 변조를 구분하는 분기 없음.

### P1-4. `run_staged.sh` 기본 병렬도 8 → `mpirun -np $VASP_NPROC` 8개 동시(=384 랭크) — 조절 변수 `JOBS_PARALLEL` 이 메일·README·SUBMIT 어디에도 없다
`run_staged.sh:301-306 NPAR=${JOBS_PARALLEL:-…max_concurrency…}` · `:318 xargs -P "$NPAR"`. 슬롯 초과를 거부하는 MPI 면 7잡 즉시 실패 → rc 2.

### P1-5. 선택 절차(attestation)의 실행 명령이 메일·README 둘 다 맨 `bash MAKE_POTCAR_ATTESTATION.sh` — 즉시 `:?` 로 exit 1
`MAKE_POTCAR_ATTESTATION.sh:4-7` `PP`·`POTCAR_ALLOWLIST`·`RELEASE_LABEL`·`SITE`, :11 `BUNDLE_ZIP_SHA256`, :49 `VASP_EXE` 여섯 개 강제. 전체 명령은 `POTCAR_ATTESTATION_REQUEST.md:13` 에만.

### P1-6. 메일 §3 은 "attestation 을 돌리면 원고 인용" 으로 읽히지만 번들은 어떤 반송물로도 인용 불가(rc 3 고정)
README:68-77 "그것만으로 원고 인용 자격이 서지 않습니다 … '조건부로 원고 인용' 표현은 쓰지 않습니다" ↔ MANIFEST `potcar_identity_policy.manuscript_citable=false` ↔ `analyze_results.py:1469-1471`. 번들 내부도 어긋난다: MANIFEST "받아들인_대가" 연속 두 줄이 서로 반대, `POTCAR_ATTESTATION_REQUEST.md:30-31` 의 "조건부" 문구.

## P2 (미검증 — 반박 안 거침 · 제목만)
1. STAGE1_PASS.json 을 아무 스크립트도 읽지 않는다(분석기가 쓰기만; 문서는 "이것 없이 2단계 안 열림")
2. 계약이 주라는데 아무도 안 읽는 파일: static/dense OSZICAR · ZIP_SHA256.txt(선택 입력)
3. 문구 "CANARY_GEOM_UNCHECKED" 인데 실제 라벨은 CANARY_GEOM_MISMATCH
4. dense/POSCAR 가 계약에 없어 dense 기하 검증이 OUTCAR POSITION 파싱에만 의존
5. SEAL 단독 실행 시 `.lock_bundle` 잔존(trap 덮어쓰기)
6. MAKE_POTCAR_ATTESTATION.sh `_bail_self` 가 kill 을 unlock 앞에 둠
7. 러너 pid 단독 SIGTERM 은 현재 물결이 끝날 때까지 보류
8. Ni 회색구간(0.25–0.55 μB) 잡의 estimand 차단 사유가 `MAGNETIC_MOMENTS_MISSING` 으로 오진(판정은 옳게 NO_VALUE)
9. 우리 재분석이 반송 트리의 RESULTS.json·STAGE1_PASS.json 을 덮어쓴다
10. 1단계 `--gate vacconv` 화면이 미실행 2단계 6잡을 "문제 6건" 으로 나열
11. MANIFEST 에 컨테이너 임시경로·repo_root 절대경로 10줄 박힘(분석기 미독)
12. IDENTITY 계보가 낡은 판을 정본으로 가리킴(IDENTITY.json→v18 · v16~v29 superseded_by 없음)
13. "여섯 개" vs 7줄 (P1-1 흡수)
14. POTCAR 조립 지시 반대(메일 "잡별로 조립 스크립트를 돌려 주십시오" vs README "따로 조립하지 마십시오")
15. 메일에 SUBMIT 의 "672 h 권장"·"48코어/잡·동시 8잡" 이 없음
16. 기체 기준 스핀 선택 정책(NUPDOWN=0 제약 vs 자유 nzmag 대조)이 protocol/사전등록 산문에 없음
17. 슬랩 최대변위 수치가 MANIFEST 안에서 0.277/0.296 Å 로 갈리고 실측은 0.2915 Å
18. P1-5 확인: 분석기는 슬랩 a·b 절대값을 안 본다 — 실물 10/10 은 동결 슬랩과 4e-11 Å 일치
19. P1-7 확인: `closure_vacconv._one` 의 role 기본값 잔재 — 실물 16잡은 전부 role 있음
20. P1-4/P1-6 잔여: planned.meta 부재·branch≠pm1·기체 키 오류가 `--check_governance` 를 통과하고 최종 분석에서만 잡힘
21. probe 가 번들 루트에 OUTCAR 를 남길 가능성(P0 해제조건 mktemp cwd 로 함께 닫힘)

## 확인한 것 (렌즈별 · 못 본 것은 통과가 아니다)
- **contract_vs_gates**: 분석기 파일 읽기 자리 전수 grep · return_contract 4곳 렌더 일치 · stub e2e `run_staged.sh 1`(rc 0)→`2`(rc 3) · 계약대로 가지치기한 트리 16/16 rc 3 · OUTCAR.gz 변형 동일 · 필수물 ablation fail-closed 정합. **못 본 것**: 실물 VASP 6 OUTCAR 되울림 형식 · 실패 잡 포함 반송물 · attestation 경로 반송 정합.
- **runner_sim**: 문서 순서 완주 e2e · 2단계 실패 e2e(BG P1-3, 손으로) · 필수 변수 누락 8케이스 메시지 · stale lock 없음 · 계약-only 반송 재분석 rc 3 · 감사 사슬(zip/MANIFEST/스크립트 3종 sha == IDENTITY, 템플릿 바이트 동일, 008f1c05 원격 조상) · bash `set -u` 정독. **못 본 것**: 진짜 MPI 슬롯 초과 · Python 3.6 호환 · `xargs -a`/`sha256sum` 현장 존재 · walltime 적정성.
- **reanalysis_sim**: 계약 파일만 합성한 16잡 트리 rc 3 · D_raw −0.300 · rc 2/3 분리 · 1단계 8축 prereq · 변형 A~H · 실물 5.4.4 OUTCAR 로 read_outcar 전 키 파싱 · 생성기 ANALYZER 렌더 == 번들 바이트 동일. **못 본 것**: LORBIT=11 magnetization 표 **실물** 파싱(repo 실물 OUTCAR 6개 모두 LORBIT 없음 — 자기 게이트 사슬 전부가 이 파서 하나에 걸림) · VASP 6 배너/되울림 · 현장 `--version` 출력 · Ni 회색구간 실제 발생 여부.
- **audit_chain**: IDENTITY_v32 sha 5개 재계산 · 008f1c05 원격 조상 … *(이하 전달 시 절단 — doc_consistency · physics_binding · residual_p1 절은 복원 불가)*

## 이행 (2026-09-03)
- P0-1 → `a0c35a1d` (probe 전체 출력 grep · 거부 exit 1 · 토큰 불변량 · census 형식검사 · stub 실물화 · 음성 4건) + `2382b6d5` (임시폴더에 빈 INCAR — ASE 표본이 `using from now: INCAR` 뒤에 버전을 찍는다)
- P1-1·P1-4 → `576c5b9e` (`_run_env_block()` 단일 정본 · allowlist 레시피 · JOBS_PARALLEL) · P1-2·P1-3 → 메일을 README 에서 자동 렌더 (`06f1a3fd`) · P1-5·P1-6 → 메일 §3 재작성
- 1저자 결정(dense 설계 제외 · `--no_kconv` · 재개조건 |ΔE_ads|<50 meV) → `32c4b730`·`89684c77` → v33 → v34(`8fcca194`)
- ⚠ v34 감사(렌즈5)가 이 결정이 **비준 prereg §3 50행("축이 하나라도 없으면 NUMERIC_BUDGET_INCOMPLETE")과 어긋나며 원장에 없다** 를 P1 로 잡았다 — 발송 전 1저자 비준 필요.
