---
title: "리뷰 CJ 회신 — A′ V5 VASP 외주 준비본 v5: NO-GO (CI 재현 3 경로 해제 · 같은 P1 의 관리 파일 목록 쓰기 경로 1 · S1–S6 · 권고 3: sha 파이프 · 정리 실패 · 반송 문구)"
date: 2026-09-27
updated: 2026-09-27
tags: [review, codex, reply, adhesion, wad, prereg, vasp, outsourcing, uma, d3, dipole, g4, g5, pp-registry, packaging]
status: 수령 (1저자 붙여넣기 + zip 첨부 · 원문 그대로) → 대응 v6 → 재리뷰 CK
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: single-source
---

> 원문 그대로 보존 (1저자가 대화에 붙여 넣은 전문 · 2026-09-27). 리뷰어가 본 대상 = 커밋 `a2374014b625fcc827d297529a6aba8104db32c2` (프롬프트 CJ `codex_CJ_prompt_wad_aprime_v5_vasp_outsourcing_v5_2026_09_27.md`).
> 첨부: zip `CJ_review_and_repro_a2374014b.zip` 의 **열세 파일 그대로** `db/raw/codex_CJ_repro_2026_09_27/` (`REVIEW_CJ.md` · `README_REPRO_CJ.md` · `probe_pack_cj.py` + `pack_cj_results.json` + `pack_cj_run.log` · `probe_semantics_cj.py` + `semantic_cj_results.json` · CI 회귀 `repro_ci.py`·`repro_pack_ci.sh`·`results_ci.json`·`ci_regression.log` · `audit_metadata.py` + `metadata_ci.json`).
> 필수 수정 재현 = `probe_pack_cj.py --assert-fixed` 의 `mgmt_echo_error` · `manifest_echo_error` (BASH_ENV 로 `echo` 함수 주입 — 관리 파일 이름/MANIFEST 이름을 쓰는 echo 만 73).
> ⚠ 리뷰어 환경에는 `simple-dftd3` 가 없어 selftest 175 · 돌연변이 11 은 재현하지 않았다고 명시했다. Windows 경로 링크는 리뷰어 쪽 스냅샷이다.

## 붙여 넣은 머리글

NO-GO — CI의 기존 재현 경로는 해제됐지만, 같은 P1의 관리 파일 목록 쓰기 경로가 남았어요. 새 P0는 확인하지 못했습니다.
필수 수정 — P1 한 묶음
[run_all.sh (line 31)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cj_a2374014b/source/db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh:31) · [생성기:350 (line 350)](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cj_a2374014b/source/tools/wad/build_v5_vasp_package.py:350)
관리 파일명을 쓰는 명령의 실패가 뒤 명령 성공에 가려져, 필수 파일이 빠진 묶음을 정상으로 승격해요.
배포 러너를 수정하지 않고 `PACK_ONLY`에 실패를 주입했습니다.

* `echo run/env.txt`·`echo run/status.tsv` 실패 → 25개 중 23개만 포장.
* `echo MANIFEST.sha256` 실패 → 24개만 포장.
* 모두 종료 0·✅·최종 SHA 검사 통과, 기존 정상 묶음까지 교체됐어요.

`cmp`는 이미 누락된 목록과 tar를 비교하므로 통과하고, SHA도 불완전한 tar 자체에는 정확해요.
최소 수정: 관리 목록 초기화·각 파일명 쓰기·MANIFEST 이름 쓰기를 각각 검사하고, 실패를 종료 4·승격 금지·기존 쌍 보존에 연결하세요. `{ echo …; cat …; } || …`는 앞의 `echo` 실패를 잡지 못해요.
해제 확인
기존 `repro_pack_ci.sh`와 `repro_ci.py --assert-fixed`는 통과했어요. `find`·필터·정렬·tar 열람 실패 차단, 정상 포장, 빈 run/, 파일럿 결속·r1 경로도 유지됐습니다.
S1–S6

* S1: 위 관리 파일 쓰기가 필수 수정이에요. SHA 파이프도 종료값을 놓치지만, 비정상 64자리 문자열은 발송 직전 SHA 검사에서 막히므로 별도 강화 권고로 분류했어요.
* S2: grep의 0=일치·1=무매치·그 밖=오류 구분은 적절해요. [GNU grep 안내](https://www.gnu.org/s/grep/manual/html_node/Exit-Status.html)
* S3: 이름 대조는 유지하세요. 실제 Windows bsdtar 3.8.8에서는 출력 CRLF와 목록 LF 차이로 거짓 실패를 재현했어요. Linux/GNU 지원 범위를 명시하면 이번 blocker는 아니에요.
* S4: `TITEL_TRUNCATED` 경계에 찬성해요. 잘림 가능성과 확정 모순을 구분하면서 통과·r1 승격은 계속 막혔어요.
* S5: 무엔트로피를 필수로 올릴 필요 없어요. 실제 집계에서 해당 값이 없으면 −TS 진단만 None, 0.0은 실제 수로 유지됐어요.
* S6: 새 과학적 blocker는 없어요. 다만 README의 **“종료 0만 발송”과 “종료 1도 실패 기록 반송”**은 정리하세요. 종료 1 뒤 PACK_ONLY 성공·SHA 확인으로 반송하는 기존 경로를 명시해도 됩니다.

SHA 16개·배포 93파일·입력 90파일 불변을 확인했어요. 175건 selftest와 mutation 11건은 독립 재현하지 못했습니다—`simple-dftd3` 부재로, 배포 기준값을 사용한 독립 시험으로 확인했어요. 실계산·제품 수정은 없었습니다.
[전체 회신](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cj_a2374014b/REVIEW_CJ.md) · [재현 스크립트·결과 ZIP](C:/Users/Administrator/Documents/Codex/2026-08-24/dur/review_cj_a2374014b/CJ_review_and_repro_a2374014b.zip)

## 회신 CJ 본문 (REVIEW_CJ.md · 원문 — 같은 내용이 `db/raw/codex_CJ_repro_2026_09_27/REVIEW_CJ.md` 에 파일로도 있다)

# 회신 CJ — NO-GO (준비본 발송)

대상 커밋: `a2374014b625fcc827d297529a6aba8104db32c2`.

**CI의 기존 재현 세 경로는 해제됐어요. 다만 같은 P1의 관리 파일 목록 쓰기 경로가 남아 있어 최종 해제는 NO-GO예요. 새 P0는 확인하지 못했어요.** 새 계산이나 물리 문턱 변경은 요구하지 않아요. 결정 원장은 여전히 `proposed`이며 이번 리뷰는 실행 승인이 아니에요.

## 보내기 전 필수 수정 — P1 한 묶음

**`db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh:31–32` · 생성기 `tools/wad/build_v5_vasp_package.py:350–351` — 관리 목록과 MANIFEST 이름을 쓰는 명령의 실패가 뒤 명령 성공에 가려져, 필수 관리 파일이 빠진 묶음을 종료 0으로 승격해요.**

두 재현 모두 제품 러너는 무수정이고, 정상 25구성원 묶음을 만든 뒤 `PACK_ONLY=1`에 BASH_ENV 함수로 출력 명령의 실패만 주입했어요.

1. `echo run/env.txt`와 `echo run/status.tsv`만 오류 메시지와 종료 73을 반환 → **23구성원**, 두 파일 누락, **러너 종료 0·✅·최종 SHA 검사 0**, 기존 정상 묶음 교체.
2. `echo MANIFEST.sha256`만 종료 73 → 뒤 `cat` 성공이 그룹의 종료값이 되어 **24구성원**, MANIFEST 누락, **러너 종료 0·✅·최종 SHA 검사 0**, 기존 정상 묶음 교체.

실제 디스크 장애를 발생시킨 것은 아니고, 그 명령이 실패했을 때의 제어 흐름을 시험한 결과예요. 관리 파일 원본들은 여전히 디스크에 있어요. 계산 OUTCAR를 위조하거나 과학적 PASS를 만든 시험도 아니에요.

`cmp`는 **이미 누락된 목록**과 그것대로 만든 tar를 비교하므로 둘이 일치해요. SHA도 불완전한 tar 자체에 대해서는 정확하므로 추가된 발송 SHA 확인으로 잡히지 않아요. `env.txt`에는 업체 빌드·노드·peak RSS·벽시계를 받도록 해 두었으므로 단순한 보기용 텍스트 누락으로만 취급할 수 없어요.

최소 수정:

- `: > mgmt`, 각 관리 파일명 쓰기, MANIFEST 파일명 쓰기를 **각각 명시적으로 검사**하세요. `printf`로 바꾸는 것만으로는 부족하고 실패 반환을 소비해야 해요.
- 현재 32행의 `{ echo ...; cat ...; } || ...`는 첫 명령 실패를 검사하지 않아요. 쓰기별 검사 또는 `&&`로 실패를 연결하세요.
- 위 두 음성에서 종료 4·성공 메시지 없음·기존 쌍 보존·part 제거를 확인하세요. 정상 포장과 잡 파일 없는 run/도 유지하세요.

재현: `probe_pack_cj.py --assert-fixed`. **현재 커밋에서 이 스크립트의 최종 assertion이 실패하는 것이 재현 성공**이에요. 결과 키는 `mgmt_echo_error`, `manifest_echo_error`예요.

## 해제됐거나 정상 확인된 것

- 원본 `repro_pack_ci.sh`를 저장소 사본 그대로 실행: 스크립트 종료 0, 내부 러너 종료 4.
- 원본 `repro_ci.py --assert-fixed`: 종료 0. Python 스크립트 SHA도 지난 회신과 같아요. `--source`·`--bash` 인자로 Linux에서도 쓸 수 있으며 Windows 전용으로 고정된 스크립트는 아니에요.
- `find`, 허용 필터, 허용 정렬, tar 작성, **목록을 전부 출력한 뒤 실패하는 tar 열람**, 금지 검사, 양쪽 비교 정렬, cmp, 목록 cat, 빈 SHA 출력, 첫 rename 실패는 독립 시험에서도 종료 4·기존 쌍 보존·part 제거예요.
- 두 번째 rename 실패는 선언대로 종료 4, SHA 불일치. PACK_ONLY 재시도로 복구돼요.
- 정상 합성 파일럿 포장 25구성원·금지 파일 0·SHA 검사 통과. 준비 실패와 금지 파일 잔재가 있는 PACK_ONLY도 CI 시험에서 누출 없이 유지돼요.
- 잡 파일이 없는 run/은 MANIFEST+env.txt 두 구성원으로 정상 포장돼요. 정상 무매치와 오류를 구분하는 정책은 유지됐어요.
- `TITEL_TRUNCATED`: 첫 시도 실패/성공 모두 차단, 정상 r1이 있어도 자동 승격 없음. P 자리의 S 문자열은 `POTCAR_MISMATCH`. 완전한 목록 접두의 실패는 정상 r1 채택, 성공 출력의 목록 접두는 `POTCAR_UNVERIFIED`예요.
- 파일럿 ID·해시 교체 차단 및 정상 봉인/r1 재사용은 CI 회귀에서 유지됐어요.
- 무엔트로피 에너지 None → 영향을 받는 표본의 `mTS_term_J_m2=None`, W와 G5는 별도로 유지돼요. 별도 0.0 입력은 None으로 바뀌지 않고 실제 수로 처리됐어요. 모두 합성 데이터 시험이에요.

## 권고 — 필수 P1과 구분

### SHA 파이프는 아직 종료값을 검사하지 않아요

`run_all.sh:40` / 생성기 `:359`.

- SHA 명령이 올바른 해시를 출력한 뒤 종료 73 → 러너 종료 0, SHA 재검사 0.
- 64자리 비-hex 문자열 출력 → 러너 종료 0, **SHA 재검사는 실패**.

그러므로 “64자리면 SHA 명령 성공”은 아니에요. 명령 성공과 `[0-9a-fA-F]{64}` 형식을 따로 검사하는 편이 좋아요. 다만 첫 사례는 해시 자체가 맞고 둘째는 명시된 발송 직전 SHA 확인이 잡으므로, 관리 파일 누락처럼 모든 발송 조건을 통과하는 결함과 같은 필수 P1로 세지는 않았어요. 새 숨은 결함으로 다음 라운드에 미루지 않고 여기 기록해요.

### 정리 실패와 포장 실패의 설명

마지막 `rm -rf "$T"`는 “검사 안 함”이 아니라 **함수의 마지막 명령이라 그 종료값이 pack의 반환값**이에요. 여기에만 실패를 주입하면 이미 새 쌍은 승격됐고 SHA도 맞는데 러너는 종료 4예요. 안전한 방향의 거짓 실패라 차단 사유는 아니에요. 이 경우와 두 번째 rename 실패를 “옛 쌍 보존” 문구의 예외로 정확히 설명하거나, 마지막 진단 폴더 청소는 별도 경고로 분리할 수 있어요.

### 실패 잡 반송 문구

README 45행의 “종료 0 뒤에만 발송”과 46·59행의 “종료 1도 실패 기록을 반송”이 함께 있어요. 계산 결과 성공과 포장 성공을 분리해 다음 중 하나로 명확히 쓰세요.

- 일반 실행 종료 **0 또는 1**이며 SHA 확인 통과한 쌍을 반송. 종료 1은 실패 계산의 진단 묶음.
- 일반 실행 종료 1이면 계산을 다시 하지 않고 **PACK_ONLY 종료 0 + SHA 확인** 후 반송.

두 번째 경로는 이미 구현돼 있으므로 새 기능 요구가 아니에요. 지난 회신의 “성공 뒤 발송”도 계산 성공이 아니라 **포장 성공**으로 좁혀 읽어야 해요.

## S1–S6

**S1 — 관리 파일 쓰기 검사가 빠졌어요.** 위 P1이 필수 수정이에요. SHA 파이프와 마지막 rm의 실제 동작은 권고 절처럼 확인됐어요. 고정된 임시 경로만 지우는 현재 청소에 별도의 과도한 프레임워크를 요구하지 않아요.

**S2 — 0/1/그 밖의 오류 구분은 맞아요.** GNU grep도 일치 0·무매치 1·오류 2이며 다른 구현은 2보다 큰 오류값을 쓸 수 있다고 명시해요. 따라서 `==2`만 보는 것보다 현재의 `>1` 차단이 적절해요. 읽기 실패·지원하지 않는 옵션·잘못된 정규식 등은 오류가 될 수 있고, 그때 종료 4로 가는 것이 맞아요. 여기서는 `-q`도 쓰지 않으므로 일치 발견 후 오류를 숨기는 그 옵션의 예외에 기대지 않아요. [GNU grep 종료상태](https://www.gnu.org/s/grep/manual/html_node/Exit-Status.html)

**S3 — 이름 대조는 유지하되 지원 환경을 명시하세요.** 정렬 후 `cmp`는 엄밀히 중복 수도 보는 이름 목록 대조이며, 그것이 단순 set보다 약한 것은 아니에요. 추가로 **Windows bsdtar 3.8.8**을 같은 Git Bash 시험에 연결하니 실제 종료 4가 났어요. `tar tzf` 출력 25행은 CRLF, 원래 목록은 LF여서 같은 이름이어도 바이트 대조가 실패했어요. `./` 접두 차이를 관측한 것은 아니며, 이를 BSD/Linux 전반의 결함으로 일반화하지 않아요. 현재 Linux/GNU 도구를 지원 대상으로 고정하면 이 플랫폼 차이는 발송 blocker가 아니에요. 업체 도구가 다르면 계산 없이 작은 PACK_ONLY smoke test로 확인하고, 정규화가 필요해도 `../`나 임의 경로까지 무턱대고 허용하지 마세요.

**S4 — 새 상태와 차단 경계에 찬성해요.** 문자열 접두는 “잘렸을 가능성”의 분류이지 PP 신원 인증이 아니에요. `PAW_PBE Ag` 같은 짧은 관측만으로 원래 뒤에 무엇이 있었는지 알 수 없지만, 현재는 통과도 r1도 허용하지 않으므로 잘못 승인되는 경로는 안 열려요. 실제 PP 이름 전체 목록의 무충돌을 검증했다고 말하지는 않아요. 다른 자리의 종과 완전한 목록 접두도 각각 별도로 처리되는 것을 실행으로 확인했어요.

**S5 — 무엔트로피를 필수로 올릴 필요 없어요.** 등록한 W는 TOTEN 차이고 sigma0는 별도 필수 병기예요. 무엔트로피가 없으면 −TS 진단만 None으로 두는 현재 집계는 정합해요. 이때 −TS를 확인했다고 말하지 않으면 돼요. “어떤 실제 빌드에는 그 줄이 없다”는 일반적 주장은 이번 시험에서 확인한 사실은 아니에요.

**S6 — 새 과학적 blocker는 확인하지 못했어요.** cut의 설정 일치 검사를 게이트로, 전자밀도 확인은 미수행으로 구분한 정정과 결정 원장 v5/175 표기는 반영돼 있어요. 문서의 실패 잡 반송·청소 예외만 위 권고대로 명료하게 하세요. CI의 남은 P1 한 묶음 이외에 새 계산·새 문턱·V2 다리를 요구하지 않아요.

## 검증 범위

프롬프트 SHA 16개 일치, MANIFEST 93파일 통과, 생성기와 배포 러너 일치. CI 대비 입력 90개 및 D3 기준값 불변. 18잡의 구조 SHA·순서·좌표가 일치하며 셀 차는 반올림 수준이에요.

**native selftest 175/175와 mutation 11/11의 독립 재현은 아니에요.** native selftest는 이 환경의 simple-dftd3 부재로 완료하지 못했어요. 요청서가 허용한 배포 기준값·합성 출력으로 검사기/CLI/배포 러너를 독립 실행했어요. D3·VASP·QE·UMA 실계산은 없고, 계산 서버 접속·외주 제출·제품 수정도 없어요. 저장소의 기존 dirty 파일은 그대로 보존했어요.

재현 파일·결과 설명은 `README_REPRO_CJ.md`에 있어요. **최소 해제조건은 관리 목록·MANIFEST 쓰기 실패를 실제 종료 4 및 구본 보존에 연결하고 양성 경로를 유지하는 것**이에요.

## 부록 — `pack_cj_results.json` 핵심 상태 발췌 (a2374014b · 전문은 `db/raw/codex_CJ_repro_2026_09_27/pack_cj_results.json`)

| 항목 | 리뷰어 결과 |
|---|---|
| positive · recovery · empty_run | rc 0 · 25 구성원 / 복구 / MANIFEST + env.txt 2 구성원 |
| find · allow_grep · allow_sort · tar_create · tar_list_output_then_error · forbid_grep · members_sort · list_sort · cmp · list_cat · sha_empty · first_mv | rc 4 · '✅' 없음 · 옛 쌍 보존 (CI 해제 확인) |
| **mgmt_echo_error** | **rc 0 · ✅ · 23 구성원 (env.txt · status.tsv 누락) · sha -c 0 · 옛 쌍 교체** ← P1 |
| **manifest_echo_error** | **rc 0 · ✅ · 24 구성원 (MANIFEST.sha256 누락) · sha -c 0 · 옛 쌍 교체** ← P1 |
| sha_valid_output_then_error | rc 0 · ✅ (명령 실패를 놓침 · 해시는 맞음) ← 권고 |
| sha_nonhex64 | rc 0 · ✅ · sha -c 1 (발송 직전 검사가 잡음) ← 권고 |
| second_mv_error | rc 4 · sha -c 1 (새 tgz + 옛 sha · 선언된 틈) |
| post_promotion_cleanup_error | rc 4 (거짓 실패 — 묶음·sha 는 정상) ← 권고 |
| windows_bsdtar | rc 4 (tar tzf 출력 CRLF vs 목록 LF · 거짓 실패 · 누출 아님) ← S3 |
