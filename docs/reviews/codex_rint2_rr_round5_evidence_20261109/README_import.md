# Codex Rint ② 재확인 회차 ⑤ (11-09) — 반입 기록

- 판정문 = `docs/reviews/codex_review_rint2_rr_round5_20261109.md` — 받은 묶음 안 원본 22,413 B · sha256 e25fb95f35c6b16db20f2a2612f9a22f6cb77ea2106c23771904d07169cbfdeb · CR 0 · 주소 꼴 0 → 리포 사본 = 원본과 바이트 같음.
- 리뷰 핀 = `abf0911eb` (abf0911ebc994167ac50132c78207c6c8d4421f1 · 가지 B) · 우리가 보낸 ZIP = codex_rint2_rr_round5_abf0911ebc99.zip (6,282,650 B · sha256 ba6a16dc…) · 원 S0 tgz (24,284,950 B · sha256 d48f55c1… · 1저자가 따로 첨부).
- 받은 것 = 1저자 PC 의 원 증거 ZIP (sha256 1C971E04588F9561F020CB9BA8DD121C24FA1D6AC2142D2055E9B4F52C7AFF67 = 1저자 PowerShell 값) 에서 3 MB 넘는 둘 (위 두 입력 · 이쪽 기록과 같은 크기) 을 1저자가 빼고 만든 slim ZIP · 1,994,275 B · sha256 1a051081252e88ffc398c58e140a12f49851c1e98e5573ace4c131347e7213e9 · 항목 206 · 안 SHA256SUMS 207 줄 = 205 일치 + 2 = 뺀 두 입력 (빈 폴더 · `python3 -I` 로 풀어 검사 · 위험 경로 0).
- 넣은 것 = **147 파일** (이 폴더 · ZIP 과 같은 상대 경로 · 바이트 그대로 · Codex `SHA256SUMS` 포함) · 뺀 것 = **61** — 우리 git blob 사본 28 (`baseline/repo/` = 핀 `1f9f3607e` 의 blob 과 28/28 같음) · 주소 꼴 22 (Windows 사용자 폴더 경로 21 · 합성 git 신원 메일 꼴 2 중 겹침 포함 → 이름 · sha256 만 · 회차 ④ 반입과 같은 규칙) · GitHub API 응답 8 (`remote/` · 우리 git 으로 대조 가능 · 재현 에이전트가 핀 tree 661308db… 와 806 blob 을 우리 git 으로 다시 대조) · 우리가 보낸 것 3 (`inputs/`).
- 우리 재현 = `_repro_ours_20261109/REPRO.md` (독립 에이전트 · Linux · Python 3.11.17 · 고정 트리 = 핀 git archive 830 파일 · 탐침마다 빈 작업 폴더 · 원본 스크립트는 복사본으로 실행 (sha 대조) · **판정값 차이 0**): probe_resume_focus (26 관측 화면 출력 바이트 같음) · probe_summaryless_copy (§6-2 표 그대로) · reproduce_smin_counterexample (§8-2 표 · s_face · d_face 그대로 · py3.8 + numpy 1.24.4 도 같음) · audit_s0_raw (§7-1 값 그대로) · probe_import_rc (7/7 같음) · 회차 ④ 무수정 탐침 = 181 줄 AssertionError (기대된 실패) · 기대 변경본 = rc 0 · recover 넷 rc 0 · resume_ok false.  다른 칸 = 경로 · 시각 · Python 판 · host_ident · Windows CRLF · zip 메타 · 합성 git 커밋뿐.  REPRO.md 의 컨테이너 경로 = 자리 표시 (`<스크래치>` · `<리포>`) 로 바꿈 (우리 문서).  `_repro_ours_20261109/` = REPRO.md + 작은 파일 셋 (pin/PIN.txt · runs/summaryless/digest_rebuild.txt · tools/deepcmp.py) · tools/rebuild_codex_digest.py 는 Windows 사용자 폴더 이름을 다시 만들어 넣는 도구라 뺌 (스크래치).

## 판정 요지 · 1저자 처분

`docs/reviews/rint2_rr5_fix_plan_20261109.md` §0 (판정 요지) · §1–§3 (1저자 11-09 *"셋다 권고대로 해"* = Q1 (가) 지금 범위 + 한정 · Q2 §8-2 최소 문안 · Q3 한정) — 전체 HOLD.

## 원장 변경 (이 반입 커밋 · `docs/reviews/findings.json`)

| 무엇 | 항목 |
|---|---|
| claimed_fixed → **verified** 11 (verified_by codex · verified_sha `abf0911eb` · verified_in = 판정문 · verified_scope = 판정문 §3 의 범위 문장) | PC14-02 · PC14-03 · RR4-01 · PC15-01–06 · SELF-155 · SELF-159 |
| open 그대로 · note | RCA-11 (부분 · 남은 것 = 실제 계획 s_min_um 0 봉인 · 후속 기술 보고 · 반복 · 비용) |
| 새 open 1 | RR5-01 (P2 · 문면 고침 = 다음 커밋 → claimed_fixed) |
| 원장 수 | 1043 → 1044 · verified 323 → 334 · claimed_fixed 371 → 360 · open 338 → 339 · wontfix 11 그대로 |

## 뺀 파일 (61)

| # | 경로 (받은 ZIP 상대) | 크기 B | sha256 (Codex SHA256SUMS 또는 다시 잼) | 뺀 까닭 |
|---|---|---|---|---|
| 1 | baseline/repo/scripts/additives.py | 104,659 | e22782501ddb0d2bd5ac8cce381c48ff3b0c1bbb570489f4f6345612dc79d84a | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 2 | baseline/repo/scripts/ca_ext_cjunc.py | 39,206 | 050a41f4c2f7fabf92f15b37030f02b069e4facef2c3345fbb3f6474bfbdacc7 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 3 | baseline/repo/scripts/ca_ext_svcf.py | 79,695 | 1ac218481b27e349fa2d101cb3fdd058aaa240b6e3ee65e88ec8b576409ea272 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 4 | baseline/repo/scripts/ca_s0_census.py | 112,217 | 1a775575855c46d5057d3fea28fa92361c23460d0069fe5e4f0cc739116f1ff4 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 5 | baseline/repo/scripts/cam_kinetics.py | 24,912 | 4b456793c9469a4b7fcef1fa3bb66b236c14f06c84d77b26687fdcf0cc6c30f9 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 6 | baseline/repo/scripts/carbon_junction.py | 204,952 | 679dbc383c0ae399c33be0102be76a7b1f3db9c93f16dff4eff4b5f7031791cb | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 7 | baseline/repo/scripts/check_method_discipline.py | 199,559 | fec723586389332adb438616522be1abe5e3dd77f3df17105e8ae3c25bda13b7 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 8 | baseline/repo/scripts/fibre_segment_raster.py | 16,032 | e2e94d3b955bfdb87446be03a2134d57546714d20ab3e460fd2c4edfd0eab0f0 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 9 | baseline/repo/scripts/lens_geometry.py | 5,907 | 891ac67f8b6c1b4c7978b5e806800ae74f5c8791928d6ece19a29e5f3b212b77 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 10 | baseline/repo/scripts/mpm_webapp_payload.py | 317,384 | 9e911be481285f8ab927f11ffb2c36b7d070d5ccf4ea6894c936de7f730b5609 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 11 | baseline/repo/scripts/ptfe_face_alpha.py | 56,888 | c052dbfe772de497b4f63a85b1cc9182c24c324c23464e69498b4e2246b8046e | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 12 | baseline/repo/scripts/rint_cycle_traj.py | 13,125 | 5af24077295cffe0f137bbb4724b458f3c9fd6d45ba530c57817ae9633996078 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 13 | baseline/repo/scripts/rint_first_result.py | 5,007 | 36049f80c39cd8dc026d0c11447d2c3d18b7ac50159f6dc937471303d8de36fb | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 14 | baseline/repo/scripts/rint_r_chain.py | 620,178 | 47a520e8ad300101c6f8d2660d7368eead77f0f3b425bdcf1d37c379fe0c8720 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 15 | baseline/repo/scripts/run_contract.py | 180,064 | 03668a1af58acfef139a13f108943f81bfa222b9078f6267a78b8506f52f45b2 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 16 | baseline/repo/scripts/sdcp_gain_verdict.py | 228,373 | 3aa82a4e1416f780adecd218fbc99448abe32bf4182af32164c4bff3e503eca4 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 17 | baseline/repo/scripts/sdcp_gain_vox015_8arm.sh | 80,034 | f964f3f343745b51fa49823685963fa496fb954628bb5dea17c90f25064efd93 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 18 | baseline/repo/scripts/se_material.py | 23,261 | 767a6a383d4581274b07ee79146a53fbe118f1f6eb0acb9ec0a5af21c9c9930c | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 19 | baseline/repo/scripts/sr01_stamp_compare.py | 57,303 | d66e2f1680a69b5b7882b4a5d32e21d15609fc2cecec58924a4af61093661b66 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 20 | baseline/repo/scripts/step3_conv_cert.py | 54,625 | e8f8a78fdd019d5429406869a2364fee671799526feed862ffee9f12d3a6c9e8 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 21 | baseline/repo/scripts/step3_sigma.py | 374,803 | 8d428ff5c6c214ea3479faae662341b88fa255982d69b180eaff660cda95f2ec | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 22 | baseline/repo/scripts/step4_dyn.py | 228,726 | 96443260fc12a1ccfc4a24a865e4ee3f656b53f25c50c68d5bacdde139e1f50a | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 23 | baseline/repo/scripts/test_ca_ext_b6.py | 196,270 | 535753fe09f51219f060cec5e79738a6089fbe92eb37ed9d747df03660b98548 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 24 | baseline/repo/scripts/test_ca_ext_runner.py | 64,013 | 280b85b9848dc224b0b7eb520030ea31a970474c56f419a218a78cac39b7231f | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 25 | baseline/repo/scripts/test_ca_s0_census.py | 109,337 | 72c8a1612fc25bf5b4031b2494b1063b192acdd83f413654b35384783d5b03be | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 26 | baseline/repo/scripts/test_carbon_junction.py | 465,793 | e03038021659004757169df6f8a2e7af4d660fd4d91788331f1bc72d340398f0 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 27 | baseline/repo/scripts/test_rint_r_chain.py | 1,106,125 | d5e1d9ea4001911b4a1878d1315e74e0188336e2ea66e021ac348ad0994612d0 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 28 | baseline/repo/scripts/test_rint_r_chain_e2e.py | 125,175 | 41762029110b9951016ef8d07bb5244ea5ff93c154084cce0445e872ddfdf2a1 | 우리 git blob 사본 (핀 1f9f3607e 와 같음) |
| 29 | build_evidence.py | 2,981 | 272c66138c6c9f2da7651712c30fba6a3a10e5312520e8cd94692ef96d4d7bd5 | 주소 꼴 (C:/Users) |
| 30 | inputs/CODEX_PASTE_round5_abf0911eb.md | 5,061 | e84938ea78a6c2650de28732d5f3ca44a688799846e367b11d1fe006e764dbd1 | 우리가 보낸 붙여 넣을 글 |
| 31 | inputs/codex_rint2_rr_round5_abf0911ebc99.zip | — (slim 에 없음) | ba6a16dce289cda1ea9d5a057d0bd612094cee8ff5bf6f0af40cf0690b4eb927 | 우리가 보낸 것 (slim 에 없음 = 3 MB 넘어 1저자가 뺌) |
| 32 | inputs/s0fix_1106_done.tgz | — (slim 에 없음) | d48f55c1b6884a75f011e9517d3f592c25aecf8a73d7a02ebbbee86eaede0a13 | 우리가 보낸 것 (slim 에 없음 = 3 MB 넘어 1저자가 뺌) |
| 33 | remote/blob_comparison.json | 239,864 | 815e6c3ab470d598773d04e42e5f78911db424eab4c28a92ebba68996f6cb6d2 | GitHub API 응답 (외부 URL · 우리 git 으로 대조 가능) |
| 34 | remote/commit.json | 12,985 | 773b5fa9ffe8c8e54073275e5a6ed35ae5a7151d6b0c3c29075dc45d6bab1915 | GitHub API 응답 (외부 URL · 우리 git 으로 대조 가능) |
| 35 | remote/data_tree.json | 87,949 | be58d8e1f438d6ad6da01318b00063ba9c55a007136789ff32f50a10c1a5d354 | GitHub API 응답 (외부 URL · 우리 git 으로 대조 가능) |
| 36 | remote/docs_tree.json | 79,016 | ba1611218aa084c6ab8c9af3f37f7b7b55178f4cdc1bec6e2ae5f5f889445b22 | GitHub API 응답 (외부 URL · 우리 git 으로 대조 가능) |
| 37 | remote/reviews_tree.json | 201,378 | 82da63048c1f5e9c94df511bce56deea3a348e0f7b20bfe3b5b6d4639ebcb25c | GitHub API 응답 (외부 URL · 우리 git 으로 대조 가능) |
| 38 | remote/root_tree.json | 10,188 | dddaec0f08d8625dd6f65093327a8da6f795fe57c13fdab2c03ed99079a09a7e | GitHub API 응답 (외부 URL · 우리 git 으로 대조 가능) |
| 39 | remote/scripts_tree.json | 204,396 | e8b8c3ece100506bbb00a25c4475352556aa3179aaa4db703f5dc3dc585da809 | GitHub API 응답 (외부 URL · 우리 git 으로 대조 가능) |
| 40 | remote/selective_trees.json | 578,599 | 36e882bce9c7e2cd496bd1adff2d37f7c81ae01bae736e6a2ae6f60d9b429820 | GitHub API 응답 (외부 URL · 우리 git 으로 대조 가능) |
| 41 | resume_agent/adjust_expectations.py | 1,988 | 7c662bc9cd62acd88108cd3c1166d2b6042054a14962286ebc1e9b95057cde3f | 주소 꼴 (C:/Users) |
| 42 | resume_agent/copy_boundary.log | 2,000 | 8cf9bbe06da90dd0cbfa653ae0380d269b04bb7d6c038ec0a8979381f68d5cea | 주소 꼴 (C:\\Users) |
| 43 | resume_agent/copy_boundary_results.json | 1,998 | 16e7a1b13101464ae8c9c7572565abfe5299d839cb31a3eb7936508d55d328b1 | 주소 꼴 (C:\\Users) |
| 44 | resume_agent/expectation_adjusted/probe_resume_independent.py | 17,395 | 8ded24077c8aed31042008ec201e154b35df1e536f5ef15c2893170c6e875b81 | 주소 꼴 (review@example.invalid) |
| 45 | resume_agent/expectation_adjusted/results.json | 23,396 | e3c01cbf5ea854cea4e436b5525cc6895b126335704ff817201cee4bb0b32e11 | 주소 꼴 (C:\\Users) |
| 46 | resume_agent/original_probe/probe_resume_independent.py | 17,381 | 83622e5a83bd0de7c97d4a368c0b3fe66ce4fb08def54fabe0a0bd80d79fa014 | 주소 꼴 (review@example.invalid) |
| 47 | resume_agent/original_probe/run.log | 474 | 3dbef0903896353c8d09ad282c9075b36989bf4e4cdc67ccd318a6f5bbe8fe16 | 주소 꼴 (C:\Users) |
| 48 | resume_agent/portabilize.py | 1,204 | 89585a28ad71154c95ae73a3d4d7740ab5715c031590f30466c4c52896075737 | 주소 꼴 (C:/Users) |
| 49 | resume_agent/probe_results.json | 26,340 | d725dca57bc5c907a7d33b640e697e7ee590f954b37d654b28e2e1b28fef0437 | 주소 꼴 (C:\\Users) |
| 50 | s0_agent/S0_Q5_REVIEW.md | 9,460 | 2e993cf96d7de274fa7b5be01f59a4366f163aebb36e448e7b807b80d893ade6 | 주소 꼴 (C:/Users) |
| 51 | s0_agent/audit_s0_raw.py | 5,400 | 4215e7721b0218bc59bc78019a0dcebbb4bd7005a4674b5ae1994358fe2c2e29 | 주소 꼴 (C:/Users) |
| 52 | s0_agent/audit_s0_raw_initial.py | 5,086 | 8621fc3acbf4ba0b4c9e275032eb7d9322b5f996f5ad421b2510929c48643458 | 주소 꼴 (C:/Users) |
| 53 | s0_agent/parser_cases/absent/console.txt | 220 | 98e57287e2445ae3d8cca503841634db50d6ec0db06f59121b3fb0f6244b75bb | 주소 꼴 (C:\Users) |
| 54 | s0_agent/parser_cases/cap/console.txt | 217 | 8089488cf4d7295ae8bf825125737a29b2525b45a953adb0991b37d81a1ca0f4 | 주소 꼴 (C:\Users) |
| 55 | s0_agent/parser_cases/good/console.txt | 214 | b7923870278fe2d2fb415e5120202ba30d483983bbde664f32a21253fc7190a2 | 주소 꼴 (C:\Users) |
| 56 | s0_agent/parser_cases/nonterminal/console.txt | 221 | 332a5246e192fa3d4396b6ed6765987a944a68abf7fbfed777ba05f3ee4e13e9 | 주소 꼴 (C:\Users) |
| 57 | s0_agent/parser_cases/rc1/console.txt | 214 | 220635954f30bfe936c9f38fb61960a93fb24fc50aa14e1b66b5a15c69133eca | 주소 꼴 (C:\Users) |
| 58 | s0_agent/parser_cases/two0/console.txt | 218 | 501268b59f75d5254231015507cd89d302d3eaf789dc76b2fec19f3e7b995a51 | 주소 꼴 (C:\Users) |
| 59 | s0_agent/parser_cases/wrongfile/console.txt | 219 | 0edde8dd5063e89a54761d684fc7abb273e12c5f2bbd0ed7849f54e01c357483 | 주소 꼴 (C:\Users) |
| 60 | s0_agent/parser_results.json | 3,688 | 3772e9fad2a88e6d0a14125432e4e2b3456131df4b8604a551e6395e08f22215 | 주소 꼴 (C:\\Users) |
| 61 | s0_agent/raw_audit.json | 10,158 | 2d226fd29d9852504ddac19f14a9e4112dae8679ff406f8d7712993cce64f984 | 주소 꼴 (C:\\Users) |
