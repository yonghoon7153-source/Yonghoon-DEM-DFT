# N2 수신 검증 — 2026-10-07

범위: Downloads의 GATE93_N2_ORIGINAL_LOGS.zip, GATE93_N2_LOG_MANIFEST.json 및 GATE94_REQUEST.md를 데이터로만 검사. 제출 프로그램, pytest, COMSOL, replay, receipt, smoke는 실행하거나 import하지 않았어요. 리뷰어가 작성한 표준 라이브러리 ZIP·해시·텍스트 판독기만 사용했어요. 원 첨부는 수정하지 않았고, text_views는 줄 인용용 복사본이며 원본 바이트의 정본은 ZIP이에요.

판정: G93-N2의 원 로그 누락/수신 불가 문제는 해소됐어요. ZIP의 14개 로그 전부가 manifest 및 e0e9f213deecabfd50254217a428bac6a85819f8의 Git blob과 일치해요. 단, GATE94 §6와 보충 README의 ‘모두 요청 커밋 이전’은 14 docs-lint에 대해 명백한 오류라 문장 정정이 필요해요. 이 정정은 인계된 로그 바이트의 수용을 뒤집지 않아요. 스크래치 원본 동일성·mtime·재실행 0은 제출자 진술로 남겨야 하며 수신자가 독립 검증했다고 쓰면 안 돼요.

## 검증된 무결성

- ZIP: 128409 B, SHA256 b76e663dcf9fba7ce18a0381e01b1777ad7e594d341d42a74376669d37c3f7c6.
- Manifest: 11913 B, SHA256 b2ee0d56a10be75c16dcd81fd23d65c4f1814ef6426b3fddabb37e08ec577620.
- ZIP 항목 14개 = manifest의 .log 14개 정확 집합, 총 비압축 126071 B. 전 항목 실제 크기/전체 SHA256/CRC32 일치; testzip 오류 없음.
- 중복 경로, casefold 충돌, 절대/상위탈출/Windows 드라이브/ADS 경로, symlink, 특수 파일, 암호화 항목, local/central header 이름 불일치 없음. 전 항목 mode 0600(파일 종류 비트 미기록), 경로 모두 통상 .log 파일. 아카이브를 파일 시스템에 extract하지 않았어요.
- ZIP의 고정 DOS timestamp는 전부 2026-10-06 00:00:00이에요. 이를 실행 시각이나 scratch mtime으로 사용하지 않았어요.
- 원격 tree는 e0e9f213d → degradation-degeneracy tree dc241bbd7c71b7ab02e061f02d4b161269274da1의 재귀 결과 4885항목, truncated=false를 읽었어요. gate93_evidence의 14 .log blob(size, SHA1)을 SHA1('blob '+길이+'\0'+ZIP원바이트)와 대조해 14/14 일치했어요. 원격 tree mode는 모두 100644예요.
- 요청 커밋 0e3c244ea의 해당 디렉터리를 따로 읽으면 README.md 1개만 있어요. 따라서 원 회신의 '요청 commit에 로그 없음' 관측은 여전히 맞고, 후속 e0e9 추가로 보완된 것으로 판정해야 해요.

근거 파일: inspection.json, git_blob_comparison.json, remote_tree_e0e9f213d.json, provenance_remote.json. 동일성 확인은 원격 SHA1에 결속한 Git blob 확인까지이며 실제 실행 현장이나 scratch 파일을 관측했다는 뜻이 아니에요.

## 14개 파일별 바이트 및 실행 상태

아래 L은 text_views/<해당 파일명>.txt의 줄 번호예요. text view는 원문 CR/LF를 LF로 정규화했으며, 특히 smoke 진행바의 CR도 줄로 세요.

| 파일 | B | 실제 원문 상태 / 제한 |
|---|---:|---|
| 00_red_test_gate92_138nodes_41failed_97passed.log | 20540 | L1 head 4aedc78f1 dirty **1**; L175 41 failed,97 passed; L176 rc=1. clean/시작=끝 주장은 불가. |
| 03_replay_g92_emit_expect_9killed.log | 17214 | L3–11 '안 물었다'; L153 ran9; L155–164 EXPECT 미선언 문제. 관측용 emit 로그이고 검증 PASS 로그 아님. rc/HEAD/dirty/시각 없음. |
| 04a_replay_g92_verify_8of9_k07_witness_nondeterministic.log | 1491 | L3–11 8/9, L8 k07 안 물었다; L16 선언한 증인과 실제 digest 불일치. rc/HEAD/dirty/시각 없음. |
| 04b_replay_g92_k07_after_witness_fix_rc0.log | 355 | L3 k07 물었다; L5 ran1; L6 call 단계 1/1. **파일명/README와 달리 원문 rc=0 없음**; HEAD/dirty/시각 없음. |
| 05a_kext_stage3_axis_g87_plus_k08_13killed.log | 6817 | L3 node13, L5 관측 EXPECT, L41 ran1; L43–52 기대집합/증인 불일치. 13 node 관측과 검증 PASS를 구분해야 함. rc/HEAD/dirty/시각 없음. |
| 05b_kext_claim_seals_plus_k10c8_2killed.log | 1368 | L3 node2, L5 관측 EXPECT, L19 ran1; L21–23 기대집합/증인 불일치. rc/HEAD/dirty/시각 없음. |
| 06_make_receipt_683503225_rc0.log | 353 | L1 HEAD683503225 full SHA dirty0; L2/4 검사35/34; L3/5 leg별 **rc=0 실제 존재**. manifest는 이 rc 둘을 누락하고 HEAD만 발췌. 종료HEAD/시각 없음. |
| 08_env_profile_json_3ec8aadb1_mismatch34.log | 5792 | L1/4 시작=끝 full HEAD3ec8aadb1 dirty0, 13:51:29→13:51:34Z; L3 rc0; L2 MISMATCH34. rc0를 환경일치로 해석 불가. |
| 10_full_pytest_3ec8aadb1_2320passed.log | 3744 | L1/43 시작=끝 HEAD3ec8aadb1 dirty0,13:51:34→15:09:42Z; L41 2320 passed,1 xfailed; L42 rc0. |
| 11_smoke_3ec8aadb1_rc0.log | 10292 | L1/146 시작=끝 HEAD3ec8aadb1 dirty0,15:09:42→15:13:26Z; L145 rc0; L4 env MISMATCH 유지; L58 n_failed2는 내부 합성격자 값(L56–63), 뒤 smoke 결과와 구분. |
| 12_full_replay_3ec8aadb1_421_of_421_rc0.log | 54666 | L1/440 시작=끝 HEAD3ec8aadb1 dirty0,15:13:26→18:42:28Z; L437 scenario432/executable421/declared11/ran421; L438 call 단계421/421; L439 rc0. |
| 14_docs_lint_send_0e3c244ea_360passed.log | 1171 | L1/13 시작=끝 요청HEAD0e3c244ea dirty0,18:44:35→19:17:57Z; L11 360 passed; L12 rc0. 요청commit **이후** 실행. |
| aborted/run1_10_pytest_7fea9cdb7_F4_docs_lint_aborted.log | 1251 | L1 시작HEAD7fea9cdb7 dirty0 13:09:33Z; L10 F4; L13 부분 진행점에서 잘림. rc/끝HEAD/최종summary 없고 최종LF도 없음. |
| aborted/run2_10_pytest_7ae871687_F1_contract_citation_aborted.log | 1017 | L1 시작HEAD7ae871687 dirty0 13:46:43Z; L10 F1 부분 진행점에서 잘림. rc/끝HEAD/최종summary 없고 최종LF도 없음. |

완료된 08→10→11→12의 로그 시각은 순차적으로 이어지고 시작/끝 HEAD도 일치해요. 이것은 로그에 기록된 순차성 확인이며, 외부 프로세스가 전혀 없었다는 독립 관측은 아니에요. 중단 두 파일은 명시적인 중단 로그이고 rc를 채워 넣거나 통과로 바꾸면 안 돼요. 03/05a/05b emit 단계와 04a의 당시 실패도 그대로 남겨야 해요. 뒤 12 전체 replay에서는 claim-seals L14, stage3-axis L332, k07 L390이 물었고 최종 rc0이므로 이전 관측 단계의 빠진 rc를 소급 복구하지 않고도 당시 최종 회귀의 기록은 읽을 수 있어요.

## status_lines 발췌의 정확도

56개 발췌 가운데 실제 줄 완전 일치 40개, 앞뒤 공백을 없애면 일치 13개, 실제 줄의 잘린 앞부분 3개, 해당 텍스트를 찾지 못한 발췌 0개예요.

- manifest L125: 08 JSON L2를 200자에서 잘라 lock_path가 `requ`에서 끝나요. 원본 JSON 줄은 온전하며 status=MISMATCH, mismatches 34개, not_measured=[loaded_module_origin]을 포함해요.
- manifest L155: 11 smoke L4를 200자에서 잘라 `module o`에서 끝나요. 원본은 `로드된 module origin 미측정`으로 끝나요.
- manifest L174: 12 replay L430의 declared 설명을 200자에서 잘라 `caller 가 다`에서 끝나요. 원본에는 회귀 없는 방어라는 상세 설명이 있어요.
- 12 manifest status_lines에는 실제 시작HEAD L1이 없고 06의 실제 per-leg rc도 빠져 있어요. 따라서 status_lines는 완전한 실행상태 원장이나 원문 대체물이 아니며 검토자는 원본을 읽어야 해요.

권고: 기존 로그/ZIP의 바이트를 바꾸지 말고 새 metadata에 rc_present, start_head_present, end_head_present, excerpt_is_prefix를 명시하거나 발췌를 완전한 줄로 정정하면 돼요. 이 개선은 원 로그 인계 자체를 보류할 이유는 아니에요.

## [P2] 요청 커밋 전 실행이라는 문장 정정

GATE94_REQUEST.md L68 및 supplement README L18은 14개 모두 요청 커밋 전 실행이라고 적어요. 하지만 요청 commit 0e3c244ea79db1b17f09a8f8043d808ab51ff43c의 GitHub commit 객체는 author/committer 2026-10-06T18:44:27Z이고(보존한 provenance_remote.json L10/L15), 14 docs-lint 원문 L1은 같은 HEAD에서 18:44:35Z 시작, L13은 19:17:57Z 종료예요. 시작은 요청 commit보다 8초 뒤, 종료는 33분 30초 뒤예요. manifest L187의 scratch_mtime 주장도 19:17:57Z예요. 따라서 '14개 모두 요청 커밋 전'은 내부 증거 자체와 충돌해요.

정정 문안: “14개 로그 중 00–12 및 중단 두 로그의 제출 mtime은 요청 커밋 전이고, 14 docs-lint는 요청 HEAD 0e3c244ea가 만들어진 뒤 18:44:35Z–19:17:57Z에 실행됐어요. 14개 모두 후속 원 로그 추가 commit e0e9f213d(19:18:27Z)의 blob으로 보존돼 있어요.”

이 오류는 chronology/provenance 문장에 한정돼요. 14 docs-lint는 요청 HEAD를 시험한 당일의 로그이며 e0e9에 보존된 바이트와 일치하므로 원 로그 인계의 증거로 받을 수 있어요. 단, '요청커밋 이전14개'나 '수신자가 원scratch 일치까지 검증'으로 표현해서는 안 돼요.

## 수신 검증과 제출자 진술 경계

| 주장 | 현재 근거 및 판정 |
|---|---|
| 첨부ZIP/manifest 바이트 및 전체SHA | 수신자가 직접 계산해 확인 |
| 각 로그의 크기/SHA256/CRC 및 exactset | 수신자가 직접 계산해 확인 |
| 각 로그 = e0e9 Git blob | 수신자가 computed Git blob SHA1/size를 원격tree와14/14 대조 |
| 원 요청tree에 README만 존재 | 수신자가 ref0e3c244ea Contents 응답 확인 |
| 로그가 적는 rc/start/end/dirty/summary | 수신자가 텍스트 확인. 실제 실행현장 독립 재현은 아님 |
| scratch_original_byte_equal=true | 원scratch 파일을 받지 않아 독립 대조 못함; manifest 작성자 진술 |
| scratch_mtime_utc | 원scratch 메타데이터를 받지 않아 독립 확인 못함; ZIP고정시각과 무관 |
| rerun=false / 재실행0 | 제출자 진술. 검토자는 새실행0을 준수했지만 과거 무재실행의 독립증명은 아님 |
| 당시 로그의 완전성 | e0e9 blob과 수신바이트 일치는 확인. 원 실행출력 전체 무누락은 증명 못함; 알려진 중단/무rc는 위표대로 보존 |

## 전체 SHA256 목록

| 파일 | SHA256 | Git blob SHA1 |
|---|---|---|
| 00_red_test_gate92_138nodes_41failed_97passed.log | ac96f22c6c645142b7b7829b5b05e0cfa0f1c4f5290f15f086b386c374320d94 | 6b35d5fc9ddc142ae057ab64e2f98df052e49ca6 |
| 03_replay_g92_emit_expect_9killed.log | e16e1cdaa427ec70cb5285463fb1babd0ff7f4c2228d8606c131de2a79bc36b6 | 22deb0c31f17c133afcd7c67b615557e62bb7eef |
| 04a_replay_g92_verify_8of9_k07_witness_nondeterministic.log | e3a8f6d21079477535f01e427e993c30d3375458ab175b31de93c447ece212c1 | 10a80ff4dd230e51b28187059a1986c73e956f90 |
| 04b_replay_g92_k07_after_witness_fix_rc0.log | 6082742576fc4cc81b068ddcd02e311468c0a907c65a231ec8849cb24074e5df | 399e997592e1d54bad66fe86b5dca5df8707118e |
| 05a_kext_stage3_axis_g87_plus_k08_13killed.log | a86cac4cf5e571d974ad94b2f9f0b2c3964e6024c186659accca9c68f3d2b51f | 1d9de38a3f6e16610dbd1d88a9282175b9d2d4f6 |
| 05b_kext_claim_seals_plus_k10c8_2killed.log | e5e9d420c1b22bbcd62fcb8d2e7a602c21c570e18935daf066974b75d76a1b1a | 720a5f5170ba3cb447ce10bfcf48100092d543b9 |
| 06_make_receipt_683503225_rc0.log | 15e2be9b3ecbd6313d2ff431e513b4c26ff81d10eb3bfbd37a6e9f458ce067f4 | d8e3343472bcd6ba29b960f56d52ab2b6735e0e1 |
| 08_env_profile_json_3ec8aadb1_mismatch34.log | 9ae1c6027248eb3d9f2d00f076f5c1052c4554f4d81dc2d496b850b803ece898 | f9c78ae983d74bf3638a36faba31fc196a8a8e0b |
| 10_full_pytest_3ec8aadb1_2320passed.log | 2f3da06d009d0971418518f7126ba3d68b7acd5426f5aa519fcb3f405bf32a45 | 845489e091efe812e07153055fca2ef1d7ccfe9f |
| 11_smoke_3ec8aadb1_rc0.log | 83c3b9babb146fe5375ee0abc7403e3ff1580074d89c1fe932ddd98b590ae7a5 | 905f131db9c5a788b888ff6ed1ca48be48de62e7 |
| 12_full_replay_3ec8aadb1_421_of_421_rc0.log | b4cf4b6dbae68cdb41817be03c7297c69b7a3c575173c4019760d833db66f367 | fcd1ed4ebc387a6ba66c7b601b4a2f4a42bba039 |
| 14_docs_lint_send_0e3c244ea_360passed.log | 5143e92c7d62311a80ddbe555e3fc5a6d38073f629642379c67f5dccaf818cdd | 4b72c0e2a71e6ee18390e80080f3bfd19de1ea8d |
| aborted/run1_10_pytest_7fea9cdb7_F4_docs_lint_aborted.log | 0c9ac667f3796150b9a9c5171fc35d227465202b0452dc486f0ec8aff73fb990 | 43fcfc4dc801bc266d82a228f3767eec3d163fcb |
| aborted/run2_10_pytest_7ae871687_F1_contract_citation_aborted.log | 73230f551f4a6ea466f2a805951038fb5fb6c1dd64a8a923ae6f9dc0ac526cf8 | b64c3792b27bd3ab5ec69ea8b1091bf7e7e002bc |

## 보존 자료

- inspect_n2.py: 리뷰어 작성 판독기. 실행은 `python -X utf8 .../inspect_n2.py` 한정. 첫 판독 시 stdout cp949 인코딩 오류로 JSON 출력이 실패해 UTF8 모드로 재판독했으며, 이것은 제출 프로그램/시험 재실행이 아니에요.
- inspection.json: 원본에서 계산한 archive/entry/hash/CRC/status 비교 및 텍스트.
- git_blob_comparison.json: 원격 blob 14개와 크기/SHA1 비교.
- remote_tree_e0e9f213d.json: commit→subtree 관계와 nontruncated Git tree evidence.
- provenance_remote.json: 요청commit 날짜, 원요청 디렉터리, 원README/보충README, 후속commit metadata.
- request_view.md / manifest_view.json / *_readme_view.md / text_views/: 줄인용용 정규화한 자료. 원 첨부는 C:/Users/Administrator/Downloads에 그대로 있어요.

원격 읽기 출처:

- https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/git/trees/e0e9f213deecabfd50254217a428bac6a85819f8
- https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/git/trees/dc241bbd7c71b7ab02e061f02d4b161269274da1?recursive=1
- https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/git/commits/0e3c244ea79db1b17f09a8f8043d808ab51ff43c
- https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/contents/degradation-degeneracy/docs/22p_gap/gate93_evidence?ref=0e3c244ea79db1b17f09a8f8043d808ab51ff43c
