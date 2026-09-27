---
title: "리뷰 CJ 프롬프트 — A′ V5 VASP 외주 준비본 v5 재리뷰 (CI NO-GO 대응: 포장 단계별 성공 확인 · TITEL_TRUNCATED · 정리 권고 3)"
date: 2026-09-27
updated: 2026-09-27
tags: [review, codex, adhesion, wad, prereg, vasp, outsourcing, lpscl, silver, uma, d3, dipole, g4, g5, pp-registry, packaging, re-review]
status: 발송 대기 (1저자) — 도구·패키지·개정 3 v5 는 커밋 a2374014b 에 고정 (원격)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 CJ — A′ V5 VASP 외주 **준비본 v5** 재리뷰 (CI NO-GO 대응 확인)

> 트랙 W_ad (점착) → 1저자 = 사용자. 정본 브랜치 `claude/friendly-meitner-lldvar` · **커밋 `a2374014b625fcc827d297529a6aba8104db32c2`** (아래 해시는 전부 이 커밋의 트리에서 `tools/review_manifest.py --require_pushed` 로 뽑았다 · 원격에 있음).
> 앞 리뷰: CE → v2 → CF → v3 → CG → v4 (c25e0ce20) → **CI NO-GO** (CG P1 3 해제 확인 · 새 P0 없음 · **P1 1 = 포장 단계 오류를 성공으로 승격**) — 회신 원문 `kb/reviews/codex_CI_reply_wad_aprime_v5_vasp_outsourcing_v4_2026_09_27.md` · 첨부 zip 8 파일 그대로 `db/raw/codex_CI_repro_2026_09_27/` (`repro_pack_ci.sh` 최소 재현 포함 — 고맙습니다, **그 스크립트를 우리 selftest 가 그대로 돌립니다**).
> 이번 요청은 **CI 해제조건**(포장 P1 의 오류 반환 · 기존 쌍 보존 · 양성 경로 회귀)이 채워졌는지, S3 의 설명 요구와 정리 권고 3 이 맞게 반영됐는지, **새로 생긴 구멍**을 보는 것이다.
> 상황은 그대로: V5 는 RESOURCE_BLOCKED · 업체·예산 미정 · **준비본** · 결정 `D-2026-09-27-wad-aprime-v5-vasp-route` 는 proposed. 판정: GO / 조건부 GO / NO-GO.
> ⚠ selftest 는 합성 패키지 build 단계에서 **simple-dftd3** 가 필요하다 — CF·CG·CI 환경엔 없었다. 안 되면 배포본 기준값으로 독립 시험해 주면 된다. 배포본 입력(90 파일 · D3 기준값)은 v3·v4 와 **같다** — 93 파일 중 `jobs.json`·`run_all.sh` 만 바뀌었다.

## §0. CI P1 → v5 대응 → 음성시험 (한 장)

| CI | 지적 (요지) | v5 대응 | selftest 음성 (이름 요지) |
|---|---|---|---|
| P1 | `pack()` 이 `find`/`sort` 실패를 무시해 관리 파일 3 개만 담은 묶음을 종료 0 · '✅' 로 승격 · 기존 정상 묶음까지 교체 · `tar tzf` 열람 실패도 '금지 없음' 으로 처리 · `[ -s list ]` 는 누락을 못 잡음 · `set -e` 만으로는 부족 | `pack()` 을 **단계마다 성공을 확인하는 직선 코드**로 바꿨다 (파이프 없음): ① `find … > tmp/found \|\| pack_fail` ② 허용 필터 `grep … tmp/found > tmp/allowed; g=$?` — **`g ≤ 1` 만 통과** (1 = 정상 무매치 = 잡 파일이 하나도 없는 run/ 은 관리 파일만 포장 · ≥ 2 = 오류 → 실패) ③ `sort … \|\| pack_fail` ④ 목록 = `MANIFEST.sha256` + 관리 파일(있는 것) + 정렬 목록 (`cat … \|\| pack_fail`) ⑤ `tar czf .part -T list \|\| pack_fail` ⑥ **`tar tzf .part > tmp/members \|\| pack_fail`** (열람 실패는 '없음' 이 아니다) ⑦ 금지 검사 `grep … tmp/members; g=$?` — 0 = 금지 파일 있음 → 실패 · 1 = 없음 → 통과 · **≥ 2 = 오류 → 실패** ⑧ **묶음 구성원 집합 = 목록 집합** (`LC_ALL=C sort` 둘 + `cmp -s`, 실패/불일치 → 실패 — tar 가 조용히 빠뜨리는 경우) ⑨ `sha256sum` 64 자리 확인 ⑩ sha 파일 쓰기 ⑪ `mv` 둘. `pack_fail` 은 메시지 + **`.part` 삭제** + 1 반환 → 러너 종료 4 · '✅' 없음 · **기존 tgz/sha 쌍 불변** (승격은 마지막 두 mv 뿐 · 진단용 `V5_vasp_return.tmp/` 는 남김). README 에 "보낼 것은 종료 0 뒤 `sha256sum -c` 까지 통과한 쌍만" 명시 | **리뷰어 방식 그대로** (BASH_ENV 함수 주입 · 제품 러너 무수정 · PACK_ONLY=1 · 정상 25 구성원 묶음이 있는 상태에서) 11 종: `find` 73 · `sort` 73 · `sort` 가 **허용 목록 정렬만** 73 (뒤 정렬은 정상) · `grep` 2 · `grep` 이 **허용 필터만** 2 · `grep` 이 **구성원 금지 검사만** 2 · `tar tzf` 73 · `tar tzf` 가 **목록은 다 찍고** 73 · `cmp` 불일치 · `sha256sum` 빈 출력 → 전부 **종료 4 · '✅' 없음 · 기존 tgz/sha 쌍(바이트) 보존 · `.part` 없음** · 두 번째 `mv` 실패 → 종료 4 · 옛 sha 그대로(새 tgz + 옛 sha · `sha256sum -c` 실패 → PACK_ONLY 재시도로 복구) · **양성**: 주입 없는 PACK_ONLY 종료 0 · 구성원 수 불변 · **잡 파일이 하나도 없는 run/**(env.txt 만) 의 PACK_ONLY → 종료 0 · 구성원 = MANIFEST + env.txt (grep 무매치는 오류가 아니다) · **리뷰어 `repro_pack_ci.sh` 를 저장소에서 그대로 실행 → 종료 0** (`runner exit = 4`) |
| S3 | 잘린 반쪽 TITEL 은 "모순 확정" 이 아니라 "자동 확인 불가" 라고 설명하라 | 새 상태 **`TITEL_TRUNCATED`**: 앞 항목은 다 맞고 마지막 관측 TITEL 이 그 자리 기대 TITEL 의 **앞부분 문자열**이면 (`titel[k].startswith(ot[k])`) `conflicts` 에 이 이름으로 넣는다 — `why` = "잘린 줄일 수 있어 자동 확인 불가 (모순 확정 아님 · 통과·재시도 자격 없음 · 원문 확인·새 승인으로만 해제)". fail-closed 는 그대로 (r1 자격 없음 · 성공 시도여도 통과 아님). 그 자리 기대 종이 아니면(예: P 자리에 `PAW_PBE S`) 여전히 `POTCAR_MISMATCH` | `tl[:2] + ['PAW_PBE S 06']` + rc 1 + 정상 r1 → `TITEL_TRUNCATED` · `r1_ignored` · why 에 "자동 확인 불가" · 같은 것 + rc 0 종료 → `TITEL_TRUNCATED` (통과 아님) · `[tl[0], 'PAW_PBE S']` (P 자리에 S 의 앞부분) → `POTCAR_MISMATCH` · 돌연변이 "startswith 를 항상 참으로" → CE P0-3 시험(TITEL 다름 → MISMATCH)이 빨간불 |

## §1. CI 정리 권고 3 대응

- **cut '기록만 · 게이트 아님' 충돌** — 개정 3 `바뀌는_것_QE→VASP.쌍극자` 를 정정했다: "**cut 위치의 설정 일치 검사(DIPOL 줄 또는 min pos/NGZF · ±2 격자)는 게이트다** (SETTINGS_MISMATCH/UNVERIFIED) · 전자밀도가 cut 에서 작은지는 검증하지 않는다 (물리 게이트 아님 · 파일럿에서 버전·NGZF·min pos·기대 cut·격자 편차를 기록)". 새 물리 게이트는 없다.
- **결정 원장 v3 · selftest 129 표기** — 제목 `(초안 v5)` · `method_ref` v5 · selftest 175 · 돌연변이 CF 38 · CG 13 · CI 11 · `rationale` 에 CG·CI 사슬 · `reopen_criteria` 를 CJ 로. `statement` 는 v5 digest · MANIFEST `85bfebdb…` 로.
- **'어느 단계에서 실패해도 옛 tar·sha 그대로' 표현** — CI 프롬프트(발송본)의 그 문장은 넓었다. 개정 3 `러너(v5)` 와 러너 `pack_fail` 메시지는 좁혀 적었다: "두 번째 mv 실패는 종료 4 로 드러나지만 **새 tgz + 옛 sha** 가 남을 수 있다 (선언된 틈) → 발송은 종료 0 뒤 `sha256sum -c` 까지 통과한 쌍만". README 도 같은 문장. selftest 가 그 상태에서 `sha256sum -c` 가 **실패**하는 것과 PACK_ONLY 재시도로 복구되는 것을 확인한다.
- (CI 가 세지 않은 차이) 빈 '무엔트로피' 레코드 → None 인데 잡 상태 OK — 무엔트로피는 필수 보고량이 아니고 `mTS_term_J_m2` 진단에만 쓰이며 None 이면 그 항이 None 으로 남는다. 그대로 두었다 (필수로 올리면 5.4.4 실물에 없는 빌드에서 막힐 수 있다).

## §2. CI 해제조건 대응

1. **포장 P1 의 오류 반환** — §0 P1 행 (11 주입 전부 종료 4 · 메시지 · '✅' 없음).
2. **기존 쌍 보존** — 같은 시험이 주입 전후 tgz sha · sha 파일 내용을 바이트로 대조한다 · `.part` 잔재 없음.
3. **양성 경로 회귀** — 정상 실행 25 구성원 · 준비 실패(Li_sv 만) · PACK_ONLY 누출 · 주입 없는 PACK_ONLY · 잡 파일 없는 run/ · r1 · tar 실패 shim (기존 시험 전부 유지) + **실제 재생성 패키지 v5** 끝-끝 (§3).

## §3. 시험

- `python3 tools/wad/build_v5_vasp_package.py --selftest` → **175/175** (v4 155 + CI 20 · 실물 원본 대조 1 건과 리뷰어 스크립트 1 건은 저장소 경로가 있을 때만 — 없으면 SKIP 을 찍고 통과로 세지 않는다).
- **돌연변이 11/11 빨간불** (제품 코드만 깨고 selftest 재실행 · 각 7 초): find 검사 제거 · 허용 필터 grep 오류(2)를 통과시킴 · 허용 필터 무매치(1)를 실패로 (양성 시험이 잡는다) · sort 검사 제거 · tar tzf 검사 제거 · 구성원 grep 오류(2)를 '없음' 으로 · cmp 제거 · sha 길이 검사 제거 · pack_fail 의 .part 삭제 제거 · TITEL_TRUNCATED 분기 제거 · startswith 를 항상 참으로.
  ⚠ **첫 판은 8/11 이었다** — 'find 검사 제거' · 'sort 검사 제거' · 'tar tzf 검사 제거' 가 살아남았다. 이유: 내 주입(`sort` 전부 실패 · `tar tzf` 출력 없이 실패)은 **뒤 단계**(구성원↔목록 cmp · 뒤 sort 검사)가 대신 잡아서 결과가 같았다. 첫 검사만 골라 깨는 주입 셋(허용 목록 정렬만 실패 · 허용 필터만 오류 · `tar tzf` 가 목록은 다 찍고 73)을 더해 11/11. **뒤 검사가 앞 검사를 가리는 구조**라, 앞 검사 자체가 붙어 있는지는 이 표적 주입으로만 확인된다고 적어 둔다.
- **리뷰어 재현물 그대로** — `db/raw/codex_CI_repro_2026_09_27/repro_pack_ci.sh` (원문 · sha `d96c0a6d…`) 를 selftest 가 합성 패키지에, 우리가 실제 패키지에 돌렸다: 둘 다 **종료 0** (`runner exit = 4 (expected 4 on enumeration failure)`). `repro_ci.py --assert-fixed` 는 Windows Git Bash 가정이 있어 여기서 돌리지 않았다 — 그쪽에서 돌려 주면 좋다.
- **실제 재생성 패키지 v5 끝-끝** (bash 러너 + 가짜 VASP · 파일럿 2 잡): 묶음 25 구성원 · 금지 0 · `sha256sum -c` 0 · `V5_vasp_return.tmp/` 정리됨 → PACK_ONLY 에 `find` 73 / `sort`(허용 목록만) 73 / `tar tzf` 목록 뒤 73 / `grep`(허용 필터만) 2 주입 → **전부 종료 4 · '✅' 없음 · 쌍 보존 · `.part` 없음** → 주입 없는 PACK_ONLY 종료 0 · 25 구성원 → 리뷰어 `repro_pack_ci.sh` 종료 0.
- 패키지 v4→v5: **입력 90 파일 + D3 기준값 불변** · `run_all.sh` (pack() 단계별 확인 · `pack_fail` · 머리말 v5 · 발송 조건) · `jobs.json` (schema v5 · 도구 sha) · README (포장 실패 문구 · 발송 조건).

## §4. 질문 (보내기 전 필수 수정만 P0/P1 · 나머지는 권고)

- **S1 단계별 확인의 빈틈** — 남은 파이프는 `h=$(sha256sum … | cut …)` 하나다 (64 자리 검사로 받는다). `tr` (금지 파일 이름 나열 · 실패해도 이미 실패 경로) · `mkdir "$T"` 실패 → 1 · `rm -rf` 는 검사 안 함. 빠진 단계가 있는가.
- **S2 grep 종료코드 규약** — 허용 필터·금지 검사에서 `1` 을 정상 무매치로, `≥ 2` 를 오류로 본다 (POSIX grep). busybox/BSD grep 도 같다고 보는데, 업체 노드가 다른 grep 이면 `2` 가 나올 수 있는 경우가 있는가 — 그 경우 러너는 fail-closed (종료 4) 로 간다.
- **S3 구성원↔목록 대조** — `tar tzf` 출력과 `-T` 목록을 집합으로 대조한다 (이름이 같아야 한다 · 경로에 공백·개행 없음 전제 · 우리 이름은 전부 ASCII). GNU tar 외의 tar 가 이름을 다르게 찍는 경우(`./` 접두 등)를 아는가 — 그러면 정상 묶음이 종료 4 가 된다 (거짓 실패 · 누출 아님).
- **S4 TITEL_TRUNCATED 의 경계** — `startswith` 로 "그 자리 기대 TITEL 의 앞부분" 만 본다. 다른 종의 TITEL 이 우연히 우리 기대의 앞부분 문자열이 되는 실제 PP 이름이 있는가 (예: `PAW_PBE Ag` vs `PAW_PBE Ag_pv` 는 공백/밑줄에서 갈린다). 있어도 막히는 쪽(통과 아님)이라 누출은 아니지만, 이름이 '잘림' 으로 잘못 붙는다.
- **S5 무엔트로피 None** — 위 §1 마지막 항. 필수로 올려야 한다고 보는가.
- **S6 그 밖에 보내기 전 막는 것** — README(포장 실패 · 발송 조건) · 개정 3 v5 (cut 게이트 문구 · 러너 v5) · 결정 원장 표기.

## §5. 첨부 (커밋 a2374014b · sha256)

```
db/properties/wad_aprime_pilot_prereg_v5_amendment_3_vasp_v5_2026_09_27.json                        c3f0bbfab8c3100cde82378b511368b152000874ee6dbbe0f28483a1003144fa
db/inputs/wad_aprime_v5_vasp_2026_09_27/jobs.json                                                   03bdd5b55f57271480b5fb86a62fe9e26edbf0cddbaeff19ccda13cf933fd7d7
db/inputs/wad_aprime_v5_vasp_2026_09_27/MANIFEST.sha256                                             85bfebdb1c6c4c6a42649f5ae8ae0dfe1ba8e2405ba572c875e4c38bc7ecf623
db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh                                                  7c822e9b4a5bdd0bb2da0cbfe4e45cecc58e13263d52a8b6f43a317d8a36b79a
db/inputs/wad_aprime_v5_vasp_2026_09_27/README.md                                                   2efa41dcb0303c2eacc2cc2d9e379b4954b4e325041d83f7926b7f6c271aebe6
tools/wad/build_v5_vasp_package.py                                                                  f0a83c76fb3e99c9e6b99fd547b779e841dffb54ff08935d71b4a7f2e2ffaf84
db/governance/decisions.json                                                                        5c4baa4a61fd416181c8e2d675ffe50e7ad2231c48ce40c49b3073484765442b
kb/reviews/codex_CI_reply_wad_aprime_v5_vasp_outsourcing_v4_2026_09_27.md                           b71bf94a72d3d152dc23c7f93e1dded4549ee12b0485b03525864f4aede29ba9
db/raw/codex_CI_repro_2026_09_27/REVIEW_CI.md                                                       d64517462d2c30fba0cb43354164bd1cbafef77a774460bfc07affb51e5302df
db/raw/codex_CI_repro_2026_09_27/repro_pack_ci.sh                                                   d96c0a6d09beffdb48e7d8aca521c50053c794cec2f74ea0d77bd007036ce5ab
db/raw/codex_CI_repro_2026_09_27/results_ci.json                                                    ef2e06c749d36aa264e6c4b23cd0b097bf63a082ecda9c761aa59ad260aa87b6
db/pipelines/adhesion_pipeline.json                                                                 86cf96e173e6da44cbe53185a890057429400cd6d8b77e4039defbdb8571801a
db/properties/sdcp_c12_v41_partial_raw/prospective/sdcp_neutral__b00__afm2424_pm1/static/OUTCAR.gz  a168ffd15d6657f2e2272fbe3a6f2af416150abb0690cbcd200825af710dee72
db/properties/sdcp_c12_v41_partial_raw/prospective/sdcp_neutral__b00__afm2424_pm1/static/INCAR      a83650c276dce85e5caa570537a439cab1e557254fad3ee8f37174e29f005a7a
db/properties/wad_aprime_s3v2_seal_2026_09_26.json                                                  8862a8e97d007361ee778ff0b643abea870701caabc1429d89c90c20f8b268c2
db/properties/wad_aprime_pilot_prereg_v5_2026_09_25.json                                            3d35dfb9e8fbcbc79c757fe9205fa78437f8e250d9c16522ac14f5ef1f2f0059
```

개정 3 v5 content_digest `sha256:2b3a0ad4f2eeb5768d270a7aa63ec48888e7e07a34b4b940dd93b3ac0cc860b8` · 도구 sha 는 jobs.json 의 `tool_sha256` 과 같다 (`f0a83c76…`). v4 MANIFEST `ccbc0988…` → v5 `85bfebdb…` (jobs/* 90 파일 sha 는 두 MANIFEST 에서 같다). 리뷰어 재현물 세 파일의 sha 는 받은 zip 의 것과 같다 (원문 무수정). 실물 OUTCAR·INCAR 두 줄은 픽스처 출처 확인용이다.

## §6. 회신 형식

판정 (GO / 조건부 GO / NO-GO) → **보내기 전 필수 수정** (P0 · P1, 재현 가능한 근거와 함께 — 재현 스크립트는 CI 처럼 첨부해 주면 우리 selftest 가 그대로 돌린다) → 권고 (선택) → S1–S5 에 대한 명시 의견.
