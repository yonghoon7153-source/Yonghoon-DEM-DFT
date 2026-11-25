---
title: 회신 BG — C-12 내부 적대적 리뷰 (NO-GO · P0 1 · P1 8)
date: 2026-09-03
updated: 2026-09-03
tags: [review, internal, sdcp, c12, vasp, reply]
status: 회신반영
kind: review-reply
system: sdcp
confidence: high
verificationStatus: verified
verifiedAt: 2026-09-03
verifiedBy: "내부 리뷰 원문 (변이시험 49건 · 이행 커밋 aec513c8)"
campaign: sdcp_c12_vasp_handoff
reviewer: 내부 (별도 컨텍스트 서브에이전트 · repo 무수정 · scratch)
target: 커밋 c895bbb4 (회신 BF 이행) · 생성기 SHA 73f60ceb
verdict: NO-GO — v30 그대로는 발송·Stage-1 보류. P0-1 고쳐 v31 재생성 뒤 사람 확인 7가지
---

> 회신 BF 의 재승인 조건(P0 4건 음성 회귀 + stage-2 실패를 완주로 안 부름)은 **충족**됐다(변이시험 확인).
> 새 P0 는 하나인데, 그것이 "결과 본 뒤 게이트 수정" 을 **확정적으로** 유발하는 종류다 —
> 이 캠페인이 여덟 번 물린 바로 그 모양. 아래는 원문 그대로다.

---

`NO-GO` — v30(생성기 HEAD 73f60ceb… = c895bbb4 동일) 그대로는 **발송·Stage-1 제출 보류**. 회신 BF 가 건 재승인 조건은 충족(변이시험으로 확인). 다만 새로 찾은 P0 1건(반송 계약 ↔ 상 폴더 POTCAR 실물 게이트 모순)이 "결과 본 뒤 게이트 수정" 을 **확정적으로** 유발하므로, 이것을 고쳐 v31 로 재생성한 뒤 아래 사람 확인 7가지를 거치면 Stage 1 제출 GO 입니다. VASP 는 돌리지 않았고 repo 는 건드리지 않았습니다.

## P0

**P0-1 (신규). 반송 계약은 "POTCAR 는 주고받지 않는다" 인데 분석기는 상 폴더 POTCAR 실물을 요구합니다 — 계약대로 반송하면 16/16 잡이 게이트됩니다.**
- 분석기 `:5116-5120` — receipt 9열이 hex 인데 `<잡>/<상>/POTCAR` 가 없으면 `RECEIPT_POTCAR_FILE_MISSING` → `:8445` 잡 gates → `ESTIMAND_KEY_UNUSABLE` → `NO_VALUE` · `VACCONV_JOB_GATED`. 분석기 selftest `:3601-3602` 가 이 동작을 **의도**로 못박고 있습니다.
- 그런데 반송 계약 정본 `_return_contract` 의 per_job 에 POTCAR 가 없고 번들 문서가 명시적으로 부정합니다: `README_REQUEST.md:117` "POTCAR 파일 자체는 주고받지 않습니다", `SUBMIT_CONTRACT.md:76-81` 반송 목록에도 없음. `verify_bundle` 은 POTCAR 를 `FORBIDDEN_NAMES` 로 취급합니다(라이선스).
- 결과: 외주 기계 분석은 통과(상 폴더에 사본 잔존), **우리 재분석은 전 잡 차단** → 두 RESULTS.json 이 다른 판정을 내고, 우리는 결과를 본 뒤 분석기를 고치게 됩니다.
- 해제: 1저자가 둘 중 하나를 정해야 합니다. **(a)** 상 폴더 POTCAR 를 반송 목록에 넣는다(라이선스 문제). **(b)** 파일 반송 없이 간다 — `MISSING` 은 게이트가 아니라 "계약상 미반송" 으로 내리고 `MISMATCH` 만 게이트로 남기며 README/SUBMIT/return_contract 에 결박 방식(receipt 9열 + POTCAR_PROVENANCE + root seal)을 적는다. 어느 쪽이든 `_return_contract` ↔ 분석기 필수 파일 집합을 selftest 로 결박하고 v31 재생성.

## P1

1. **decisions.json 비준 기록은 여전히 `state=="ratified"`+digest 만 봅니다.** actor/timestamp/commit 을 요구하는 것은 참조 문서뿐. 재현: 실물 decisions 사본의 두 비준 기록을 `{state, decision_digest}` 로 깎아도 strict/bytes 모두 ok.
2. **staged README/SUBMIT 실행 예시에 `LAUNCHER_BIN` 이 여전히 없습니다.** 그대로 실행하면 `run_staged.sh:63-68` exit 2. BF P1 수정은 단일 잡 예시에만 들어갔습니다.
3. **stage-2 실패 경로는 구현됐지만 e2e 가 없습니다.** 생성기 selftest 는 `run_staged.sh 1` 만 부릅니다.
4. **BF 의 새 정적 검사들이 preflight 에 없습니다.** exact map·c1/c2↔protocol·기체 절대관계·planned phases 는 전부 번들만으로 판정 가능한데 `--check_governance` 어디서도 안 돌고 최종 분석(≈300 h 뒤)에서야 돕니다. BD P0-4 "비용 발생 전에 닫는다" 와 어긋납니다.
5. **a·b 절대 셀은 아무 데도 결박되지 않습니다.** 완화 요인: 생성기가 동결 clean slab SHA 를 대조하고 files_sha256+EXPECT 가 POSCAR 를 고정. 실물 v30 10/10 슬랩 POSCAR 가 동결 슬랩 a/b 와 일치함을 확인했습니다. 그 전까지는 사람 확인 항목.
6. **변이시험 생존 17/49** — 새 가드 중 음성시험이 없는 것: planned.meta 통째 부재 · pm1 봉인 branch≠pm1 · net4/pose-alt 의 box24 강제 · c1↔c2 a/b 벡터 · 기체 최소 여백 · provenance n_files/generator/clean 재계산/64-hex · 비준 timestamp · decisions 원문 state/digest. `superseded` 는 문자열 "false" 는 막지만 **부재(None)** 음성이 없습니다.
7. **role 기본값 잔재 3곳**: `closure_vacconv._one`, `_closure_estimand._is`, 생성기 `_readme_sp`. 생성기가 role 을 항상 쓰므로 실물 영향은 없습니다.
8. POTCAR TOCTOU: 재해시로 창은 µs 급 — 나머지는 반송 실물 재해시가 닫는 설계인데 그 실물이 P0-1 때문에 안 옵니다. P0-1 결정에 종속.

## 확인한 것

- `--selftest` rc 0: 분석기 421/421 · verify 30/30 · e2e 12/12. 생성기 파일은 c895bbb4 와 바이트 동일, 작업트리 clean.
- **변이시험 49건**: BF 4건의 리뷰어 재현 가드는 전부 KILLED — exact map·role 기본값·planned 5필드·protocol 사본 부재 / 기울어진 c·protocol c1/c2·sd_flags / COM 중앙·span+margin·지문 재계산·planned phases·receipt 상 집합 / provenance 완전성·필수 입력·참조 SHA·actor·malformed·`..` 이탈·사본 SHA.
- **P0-2·P0-3·P0-4** 실물 확인: c 벡터 (0,0,c)·절대 c1/c2·3축 플래그·Cartesian 좌표 / 실제 조각으로 `_gas_bytes_check` 왕복(box20/24 지문 일치·COM (0.5,0.5,0.5)) / `_bundled_ref_path` 가 절대경로·`..`·realpath·symlink 이탈 차단.
- e2e/stage-1 러너 회귀는 외주 기계 배치(상 폴더 POTCAR 존재)에서 돌므로 **P0-1 모순을 드러내지 못합니다** — 계약대로 파일을 뺀 반송물로 분석기를 돌리는 시험이 없습니다.

**v31 재생성 뒤 Stage-1 제출 전 사람 확인** (자동화 안 된 것만): ① P0-1 결정이 return_contract·README·분석기 셋에 같은 문장으로 들어갔는가 + `--selftest` rc 0 ② `--verify_zip … --expect_jobs 16` PASS, IDENTITY_v31 기록 ③ 풀어 놓은 번들에서 `analyze_results.py . --check_governance` rc 0 ④ `governance/*.json` 4개 sha256 == repo `db/` 원본 (외부 앵커) ⑤ MANIFEST `estimand_job_keys` == protocol §2b 4경로·branch afm2424_pm1, `vacuum_convergence` 36.6551/40.6551, n_jobs 16 ⑥ 슬랩 POSCAR 10개 a/b == 동결 clean slab ⑦ 메일에 EXPECT_MANIFEST/ZIP SHA + `LAUNCHER_BIN` 포함 실행 예시. 이 판정 자체의 비준은 1저자 몫입니다.
