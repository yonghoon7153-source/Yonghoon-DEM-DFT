---
title: "리뷰 CI 회신 — A′ V5 VASP 외주 준비본 v4: NO-GO (CG P1 3 해제 · 새 P1 1 = 포장 단계 오류를 성공으로 승격 · S1–S6 찬성 · 정리 권고 3)"
date: 2026-09-27
updated: 2026-09-27
tags: [review, codex, reply, adhesion, wad, prereg, vasp, outsourcing, uma, d3, dipole, g4, g5, pp-registry, packaging]
status: 수령 (1저자 붙여넣기 + zip 첨부 · 원문 그대로) → 대응 v5 → 재리뷰 CJ
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: single-source
---

> 원문 그대로 보존 (1저자가 대화에 붙여 넣은 전문 · 2026-09-27). 리뷰어가 본 대상 = 커밋 `c25e0ce2008b5c33dc6113b249cc8aa22097db2e` (프롬프트 CI `codex_CI_prompt_wad_aprime_v5_vasp_outsourcing_v4_2026_09_27.md`).
> 첨부: 1저자가 zip 을 함께 올렸다 (`CI_review_and_repro_c25e0ce20.zip`) — 여덟 파일을 `db/raw/codex_CI_repro_2026_09_27/` 에 **그대로** 두었다 (`REVIEW_CI.md` 회신 전문 · `README_REPRO.md` · `repro_ci.py` + `results_ci.json` + `repro_ci_run.log` · `repro_pack_ci.sh` (P1 최소 재현 · BASH_ENV 로 find 함수 주입) · `audit_metadata.py` + `metadata_ci.json`).
> ⚠ 리뷰어 환경에는 `simple-dftd3` 가 없어 selftest 155 · 돌연변이 13 은 재현했다고 주장하지 않는다고 명시했다. 리뷰어의 Windows 경로 링크(`C:/Users/Administrator/Documents/Codex/...`)는 리뷰어 쪽 스냅샷이다.

## 붙여 넣은 머리글

NO-GO — CG의 P1 세 건은 해제됐지만, 새 포장 P1 한 건이 남았어요. 새 P0는 확인하지 못했습니다.
보내기 전 필수 수정
[run_all.sh (line 25)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ci_c25e0ce20/source/db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh:25) · [생성기:334 (line 334)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ci_c25e0ce20/source/tools/wad/build_v5_vasp_package.py:334)
파일 목록 생성 실패를 무시해 잡 산출물이 빠진 묶음을 성공으로 승격해요.
배포 러너를 수정하지 않고 외부 명령 실패만 주입했습니다.

* 정상 파일럿 묶음: 25개 구성원, SHA 검사 통과.
* `find` 또는 `sort` 실패: 관리 파일 3개만 포장하고도 종료 0·✅ 성공.
* 기존 정상 묶음도 불완전한 새 묶음으로 교체됐어요.
* 같은 함수의 `tar tzf` 구성원 열람이 실패해도 성공으로 처리돼요. 이 경우 실제 금지 파일 누출까지 재현한 것은 아닙니다.

최소 수정: 목록 생성·정렬·구성원 열람의 성공을 각각 확인하고, 실패하면 종료 4·승격 금지·기존 묶음 보존으로 연결하세요. `set -e`만 추가해서는 충분하지 않아요.
해제 확인
CG의 세 항목은 실제 재현에서 정상 작동했어요.

* 정상·준비 실패·PACK_ONLY 모두 금지 파일 누출 없음.
* 파일럿 ID 또는 봉인 파일 변경 → 실제 집계 CLI 종료 3. 정상 파일럿과 정당한 r1 재사용은 유지.
* 정상 TITEL 목록 접두는 실패 시 r1 허용, 실제 종·날짜·순서 모순은 계속 차단.

S1–S6

* S1: 현재 단일점 목적에는 허용목록이 충분해요. CONTCAR 등을 추가할 필요는 없어요. 내용까지 검증한다는 보증은 제외하세요.
* S2: ID+두 파일 SHA 결속은 선언한 실수 방지 범위에 충분해요. 잡 상태 차단·종료 3으로 다른 진단을 유지하는 설계에 찬성해요.
* S3: 완전한 문자열의 목록 접두만 허용하는 보수적 규칙을 유지해도 됩니다. 반쪽 줄은 실제 모순 확정이 아니라 자동 확인 불가라는 설명을 붙이세요.
* S4: 과학 판정과 반송 위생을 분리해도 됩니다. 금지 파일은 발송에서 제외하고 수신 시 별도 처리하되, 정상 에너지까지 무조건 종료 2로 막을 필요는 없어요.
* S5: 두 번째 rename 실패가 종료 4로 드러나는 잔여 틈은 수용 가능해요. 크기를 추가해도 원자성 문제는 해결되지 않아요. 발송 직전 최종 SHA 대조가 필요해요.
* S6: 추가 필수 차단은 위 P1 하나예요. 개정문의 “cut은 기록만·게이트 아님”과 실제 게이트 설명, 원장의 남은 v3 표기는 정리 권고입니다.

SHA 14개·배포 93파일·CG 대비 입력 90파일 불변을 확인했어요. 전체 selftest는 `simple-dftd3` 부재로 완료하지 못했으며, 155건 PASS를 재현했다고 주장하지 않습니다. 실계산은 하지 않았어요.
[전체 회신](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ci_c25e0ce20/REVIEW_CI.md) · [재현 스크립트·결과 묶음 다운로드](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_ci_c25e0ce20/CI_review_and_repro_c25e0ce20.zip)
해제조건은 포장 P1의 오류 처리와 회귀시험뿐이에요. 새 계산이나 과학적 문턱 변경은 요구하지 않습니다.

## 회신 CI 본문 (REVIEW_CI.md · 원문 — 같은 내용이 `db/raw/codex_CI_repro_2026_09_27/REVIEW_CI.md` 에 파일로도 있다)

# 회신 CI — NO-GO (발송 준비본)

대상: `c25e0ce2008b5c33dc6113b249cc8aa22097db2e`.

CG P1 세 건은 독립 재현에서 해제됐어요. 새 P0는 확인하지 못했고, **포장 오류를 성공으로 처리하는 P1 한 묶음**이 남아요. 이번 판정은 준비본에 대한 것이며 외주 실행 승인이 아니에요. 결정 원장의 `decision_state`는 여전히 `proposed`예요.

## 보내기 전 필수 수정 — P1 하나

**`db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh:25` · `tools/wad/build_v5_vasp_package.py:334` — 목록 생성 실패를 검사하지 않아 잡 산출물이 빠진 압축파일을 성공으로 승격해요.**

실제 배포 러너는 수정하지 않았고, `BASH_ENV` 함수로 외부 명령 실패만 주입했어요. 합성 파일럿 두 잡을 정상 실행한 뒤 `PACK_ONLY=1`에서:

- `find`가 오류를 내고 종료 73 → 러너 **종료 0**, “✅ 포장만 다시 했다”.
- `sort`가 오류를 내고 종료 73 → 동일해요.
- 두 경우 모두 정상 25개 구성원이 **MANIFEST.sha256·run/env.txt·run/status.tsv 세 개**로 줄었어요. OUTCAR·attempt.json 등 잡 자료가 전부 빠지고, 기존 정상 반송 묶음까지 새 불완전 묶음으로 교체돼요.

이는 실제 디스크 장애를 관측했다는 뜻이 아니라, 디렉터리 열거·정렬 명령이 실패할 때의 제어 흐름을 재현한 음성시험이에요. `[ -s list ]`는 관리 파일 이름만 있어도 참이므로 누락을 잡지 못해요. 뒤의 수신 검사기가 결측을 막더라도 “포장 실패는 종료 4”라는 발송 계약은 이미 위반돼요. 과학적 PASS를 위조하는 P0로 부풀리지는 않겠어요.

**같은 오류 처리 묶음:** `run_all.sh:28` / 생성기 `:337`의 `tar tzf | grep -Eq`는 구성원 열람 실패도 “금지 이름 없음”으로 처리해요. `tar tzf`만 종료 73으로 만들면 역시 종료 0이에요. 이 시험에서 실제 금지 파일 누출까지 재현한 것은 아니에요. 허용목록이라는 첫 방어는 작동했지만, 선언한 두 번째 검사가 실패해도 승격한다는 결함이에요.

최소 수정은 다음과 같아요.

1. `find` 산출을 임시 목록에 받되 명령 성공을 명시적으로 확인하고, 필터·정렬·목록 쓰기 오류도 반환하세요. **정상적인 grep 무매치(1)**와 **명령/입출력 오류**를 구분하세요. 모든 잡이 준비 실패한 정상 반송을 무조건 금지하라는 요구는 아니에요.
2. `tar tzf`를 별도 임시 구성원 목록으로 받아 **열람 성공부터 확인**한 다음 금지 이름을 검사하세요. 열람 실패와 “없음”은 다르게 처리해야 해요.
3. 실패하면 승격하지 않고 러너 종료 4·성공 메시지 없음·기존 반송 쌍 보존을 시험하세요. 정상·준비 실패·PACK_ONLY 양성 경로도 유지하세요.

`pack`은 `if pack; then` 안에서 호출되므로 **`set -e`만 추가하는 처방은 충분하지 않아요**. `pipefail`을 켜더라도 반환값을 실제로 소비하고, 정상 무매치를 별도로 처리해야 해요.

## CG 해제조건 재현 결과

- **P1-1 해제:** 정상 파일럿 포장 25개 구성원, 금지 파일 0개, `sha256sum -c` 종료 0. Li_sv만 있는 준비 실패는 종료 1·부분 POTCAR 삭제·묶음 누출 없음. 중단 잔재 다섯 종류를 넣은 PACK_ONLY도 누출 없이 기존 시도 파일을 보존해요. 검사기 경고 목록은 다섯 파일을 정확히 보고했어요.
- **P1-2 해제:** 정상 18잡 합성 대조군은 실제 collect CLI 종료 0. 파일럿 ID만 교체하면 `PILOT_NOT_SEALED`·실제 CLI 종료 3. 같은 ID에서 OUTCAR를 바꾸고 attempt 내부 해시까지 맞춰도 동일하게 막혀요. 정당한 r1으로 새로 봉인한 파일럿은 OK, 첫 시도 봉인에 r1을 바꿔 끼우면 차단돼요.
- **P1-3 해제:** 완전한 TITEL 한 개/세 개만 출력하고 실패한 첫 시도는 정상 r1을 채택해요. 순서·날짜·추가 종 모순은 계속 차단하고, 성공 출력의 불완전 접두는 `POTCAR_UNVERIFIED`예요. ENCUT 모순+실행 실패/미수렴, 다른 PP+실패를 r1이 덮는 이전 경로도 막혔어요.
- **빈 마지막 레코드 수정 확인:** TOTEN·sigma0·Edisp는 앞값으로 돌아가지 않고 None 및 해당 차단 상태가 돼요. 무엔트로피 에너지도 None으로 남지만, 현재 필수 보고량이 아니므로 잡 상태는 OK예요. 이 차이를 별도 결함으로 세지 않았어요.
- **실물 픽스처 유지:** VASP 5.4.4 원문에서 TOTEN −1151.29778848 eV, sigma0 −1151.29228248 eV, Edisp −28.80731 eV를 읽고 min pos 520/NGZF 560 증거도 유지돼요. 다른 계의 파서 검증이며 V5 과학 결과가 아니에요.

## 선택 권고

- 개정 JSON 60행의 “도구는 기록만·게이트 아님”은 뒤에 추가한 cut 판정 설명과 충돌해요. **cut 위치의 설정 일치 검사는 게이트이고 전자밀도 검증은 수행하지 않는다**로 정리하면 돼요. 새 물리 게이트를 요구하는 것은 아니에요.
- 결정 원장 5074행 제목·5096행 method_ref에는 v3·selftest 129가 남았어요. statement/digest는 v4를 가리키므로 이번 실행 차단 사유는 아니지만 다음 독자를 위해 맞추는 편이 좋아요.
- “어느 단계에서 실패해도 옛 tar·sha가 그대로”라는 표현은 좁혀야 해요. 두 번째 rename 실패는 실제로 종료 4이지만 **새 tar + 옛 sha**가 남아요. 현재 프롬프트가 인정한 한계대로 쓰세요.

## S1–S6

**S1 — 찬성.** 현재 고정기하 단일점의 검사·집계에 필요한 이름 기반 허용목록으로 충분해요. CONTCAR/XDATCAR/PCDAT/REPORT 추가를 발송 조건으로 삼지 않아요. 허용 이름으로 바꾼 내용이나 wrapper가 stdout에 출력한 내용까지 검사한다는 보증은 하지 마세요.

**S2 — 찬성.** 현재의 run_id + attempt.json/OUTCAR SHA 결속은 선언한 실수 방지 범위에서 “봉인 파일럿 재사용”이라고 부를 수 있어요. 파일럿만 `PILOT_NOT_SEALED`, 전체 집계 종료 3, 사용 자격 false를 유지하면서 다른 잡의 진단을 보여주는 설계가 맞아요. 등록부 자체 형식·고정 SHA 오류가 종료 2인 것과 구분하면 돼요.

**S3 — 좁은 규칙 유지에 찬성.** 마지막 TITEL의 문자열 접두까지 자동 허용할 필요는 없어요. 잘린 `Ag 02Ap`는 실제 PP 모순이 확정된 증거가 아니라 자동 검증 불가 사례이므로 그 점은 설명하세요. 원문 확인·새 승인으로 풀 수 있는 보수적 차단은 이번 필수 수정이 아니에요.

**S4 — 과학 판정과 반송 위생 분리에 찬성.** 금지 파일 존재만으로 정상 에너지의 과학 판정을 종료 2로 바꿀 필요는 없어요. 다만 경고를 무시하고 재배포해도 된다는 뜻은 아니에요. 발송 묶음에서는 제외하고, 수신 시 별도 격리·처리하세요. 원본 증거를 검사기가 무조건 지우게 만들 필요도 없어요. 이는 법적 라이선스 허용 여부를 판정한 의견은 아니에요.

**S5 — 두 rename 사이 틈은 선언된 운영 한계로 수용 가능해요.** 두 번째 rename 실패를 주입하면 종료 4·성공 메시지 없음이 유지돼요. 크기 필드를 더해도 두 파일의 원자적 교체 문제가 해결되지는 않아요. 발송은 종료 성공 뒤 최종 SHA 대조까지 통과한 쌍에 한정하세요. 위 P1처럼 rename *이전* 검사 실패가 성공으로 넘어가는 경로는 별도로 고쳐야 해요.

**S6 — 새 필수 차단은 위 포장 P1 하나예요.** PP·버전 신원과 봉인 파일럿 재사용을 분리한 문구는 맞아요. 실제 업체 파일럿에서 버전·NGZF·min pos·기대 cut·격자 편차를 남기겠다는 조건도 유지하세요. 지금 합성/타계 픽스처의 성공을 업체 형식이나 전자밀도 확인으로 승격하지 마세요. 비준·업체·예산 확정은 여전히 별도 조건이에요.

## 검증 범위와 재현물

- 프롬프트의 SHA 14개 모두 일치. 배포 MANIFEST 93개 파일 대조 통과. 생성기 문자열과 배포 러너 일치.
- CG 대비 입력 90개 및 D3 기준값 불변. 18잡의 원본 구조 SHA·POSCAR 순서 일치, 좌표 차 0, 셀 반올림 차 최대 약 3.4e-11 Å.
- **원본 selftest 155/155와 mutation 13/13을 재현했다고 주장하지 않아요.** selftest는 `simple-dftd3` 부재로 완료하지 못했어요. 요청이 허용한 대로 배포본의 봉인 D3 기준값으로 독립 검사기/CLI/러너 시험을 했고 D3를 새로 계산하지 않았어요.
- VASP·QE·UMA 실계산, 서버 접속, 외주 제출, 제품 코드 수정은 없어요. Python 가짜 VASP는 합성 텍스트만 만들었고 POTCAR fixture도 원소 이름·가짜 해시용 텍스트뿐이에요.

`repro_ci.py`는 종합 재현 및 `results_ci.json` 생성, `repro_pack_ci.sh`는 P1 최소 재현이에요. `audit_metadata.py`와 `metadata_ci.json`은 신원·기하·native selftest 한계 기록이에요. 실행법은 `README_REPRO.md`에 있어요.

**해제조건은 포장 P1 하나의 오류 반환·구본 보존·양성 경로 회귀 확인이에요. 새 대형 계산이나 과학적 문턱 변경은 요구하지 않아요.**

## 부록 — `results_ci.json` 핵심 상태 발췌 (전문은 `db/raw/codex_CI_repro_2026_09_27/results_ci.json`)

| 항목 | 리뷰어 결과 (c25e0ce20) |
|---|---|
| positive_sealed · positive_cli | 정상 18 잡 + 봉인 등록부 → 실제 collect CLI 종료 0 |
| pilot_replaced_id · pilot_same_id_changed_output | PILOT_NOT_SEALED · CLI 종료 3 (해제 확인) |
| titel_paths · r1_seal_reuse · contradiction_not_rescued | 접두 → r1 채택 · 모순 → 차단 · r1 봉인 재사용 OK (해제 확인) |
| empty_final_records | TOTEN·σ→0·Edisp None → 차단 상태 (무엔트로피 None 은 필수 보고량 아님 → OK) |
| actual_raw_outcar · actual_dipol_evidence | 실물 5.4.4 판독 유지 |
| runner_positive · runner_sha_check · runner_pack_only · runner_partial_pp_failure | 25 구성원 · 금지 0 · sha -c 0 · 준비 실패 누출 0 · PACK_ONLY 누출 0 |
| **find_failure · sort_failure** | **rc 0 · 구성원 3 (MANIFEST · env.txt · status.tsv) · '✅' · old_pair_preserved false** ← P1 |
| tar_create_failure | 종료 4 (기대대로) |
| **tar_list_failure** | **rc 0** (열람 실패를 '금지 없음' 으로) ← P1 같은 묶음 |
| second_mv_failure | 종료 4 · 새 tgz + 옛 sha (S5 · 선언된 틈) |
