# repo — kb/reviews (110 파일)

## 지금 무엇인가
Codex·내부 교차리뷰의 요청↔회신 원문 창고다. md 103 + docx 6 + txt 1 = 110개, md 만 18,492줄이고, 라벨 A~BI 로 도는 캠페인(SDCP doped/closure, C-12 VASP 외주, 폴라론 S0, LPSOCl MD, 웹앱 거버넌스)의 판정이 전부 여기 있다. **내가 실제로 본 것**: 103개 md 전부의 frontmatter(title/date/status/kind), INDEX.md 전문(83줄), 본문을 깊게 읽은 것 14편(BG·BH·BI 프롬프트, codex_F 부록, internal_review_AX, vasp_bundle_codex_reply, section3_compressed, self_audit, site_screen 3편, ECERD 머리말, _T_doped_parked). **못 본 것**: 나머지 ~89편의 본문(특히 AA~BF 프롬프트·회신 대부분, internal_Z/Z2/Z3/BG/BH/lens 본문, ECERD 1279줄 중 12줄만 봄)과 docx 6개(바이너리 — LLM 이 못 읽는다).

## 처음 오는 사람
폴더를 열면 `ls` 첫 줄이 `ECERD2600097_review_notes.md`(남의 심사원고 읽기노트 1279줄, 이 폴더의 최대 파일, 8월 6일자)다 — 이 폴더가 무엇인지와 무관한 장르가 맨 앞에 온다. README 가 없고, INDEX.md 는 있지만 2026-09-03 자동생성본이라 **가장 최근 세 요청(BG·BH·BI, 09-07~08)이 표에 아예 없고** internal_* 7편도 없다(103개 중 38개가 INDEX 에서 이름조차 안 나온다). status 가 55가지 자유문자열이라("발송 대기" 14 · "sent" 8 · "회신반영" 9 · "접수 — 구현 중" 3 · …) "답이 난 것 / 안 난 것"을 눈으로도 기계로도 못 가른다. 결정적으로 **막힌 것 목록이 없다** — 가장 가까운 것이 `codex_F_beta_null_model_2026_08_27.md` 256~261줄의 "회신 대기 중인 기존 건" 표인데 8월 27일자라 지금은 틀렸다. 그래서 처음 온 사람이 "지금 뭐가 안 닫혔나"를 물으면, 두 개의 서로 다른 낡은 목록을 보고 틀린 답을 얻는다.

## 건드리면 안 되는 것
- **회신 원문 본문은 한 글자도 고치지 않는다.** CLAUDE.md 용어 규율이 명시한다 — "회신 원문을 고쳐 쓰면 이력이 깨진다". codex_*_reply_*.md 14편 + internal_* 7편 전부 해당. 고치는 것은 frontmatter status 와 문서 상단 후주뿐이다.
- **발송된 프롬프트 본문도 고치지 않는다.** BH §1 의 "저희는 이걸 확인하지 못했습니다"(61줄)는 발송 시점의 진술이다 — 사실이 바뀌었어도 본문 대신 후주로 단다. AK·AL·AM 회신의 '우리가 틀렸다' 자백문도 마찬가지.
- **INDEX.md 손편집 금지.** 파일 스스로가 "⛔ 손으로 고치지 않는다. `python3 tools/kb_wiki.py reviews --write` 로 재생성한다" 고 적었고 kb 위키 규율도 같다. 고칠 것은 생성기(tools/kb_wiki.py) 쪽이다.
- **`tools/kb_wiki.py` review_chain() 의 '못 하는 것' docstring 과 라벨 재사용 경고(479-495줄, 528-536줄 주석).** 회신을 '소비'하는 3단계 매칭과 왜 그렇게 됐는지의 실물 사례(U_reply ↔ V_prompt 오탐)가 적혀 있다 — 이걸 지우면 같은 버그를 또 만든다.
- **라벨 재사용 8건(S·T·U·V·W·X·BG·BH)의 이력.** 이름을 정리하더라도 '어느 라벨이 두 캠페인에 쓰였는지' 표는 남긴다 — 과거 커밋·db 인용이 그 라벨로 되어 있다.
- **internal_Z / Z-2 / Z-3 3연속 NO-GO.** 폴라론 S0 '재비준 금지(현 판)' 의 유일한 근거다. 세 판을 하나로 합치거나 요약으로 대체하면 '왜 세 번 다 막혔나'(층위가 다르다)가 사라진다 — CLAUDE.md 가 SDCP 여덟 실패에 대해 똑같은 교훈을 적어 뒀다.
- **docx 6개.** LLM 이 못 읽고 이름이 거짓말해도 1저자 제출물 실물이다. 하위 폴더로 내리는 것까지만, 삭제는 안 된다.
- **`_T_doped_section_parked.txt`.** 고아처럼 보이지만 `codex_T_prompt_sdcp_binding_energy_path_2026_08_29.md:19` 와 `kb/questions/doped_declared_state_feasibility_2026_08_29.md:155` 두 곳이 가리킨다. 여기 담긴 실측(mol_doped mag 1.000 강제 vs complex −0.306/+3.724)은 CLAUDE.md 보고량 규율의 근거 그 자체다.
- **`self_audit_2026_08_06.md` 와 `ECERD2600097_review_notes.md`.** 장르가 달라 폴더를 옮기더라도 내용은 그대로. self_audit 의 '📌 재발 방지 4항'과 ECERD 의 3층 구분(🔵 원문 인용 / 🟢 우리 해석)은 지금도 유효한 규율이고, ECERD 는 미출판 심사원고라 인용 취급 경고문을 절대 떼면 안 된다.
- **`codex_F_beta_null_model_2026_08_27.md:252-261` 의 미회신 표.** 낡았지만 그 시점의 기록이다 — 새 '안 닫힌 것' 목록을 INDEX 에 만들되 이 표는 날짜를 명시해 남긴다.
- **status 문자열에 박혀 있는 커밋 해시.** 예: codex_AV_reply 의 "P0-1 (895af2ed) · P0-2 (1b3fbefc) · P0-3 (d29c322e) · P0-4 (4aed52ff)". 통제어휘로 정리할 때 이 정보를 버리지 말고 `note:`/`outstanding:` 로 옮긴다 — 이행 증거가 여기밖에 없다.

## 발견

### [P0·wrong] bg-bh-status-lie
- **어디**: `kb/reviews/codex_BG_prompt_webapp_aw_release_2026_09_07.md:6 · kb/reviews/codex_BH_prompt_md_axis_audit_2026_09_07.md:6`
- **근거**: 둘 다 `status: 작성 — 발송 대기`. 그런데 ① `db/governance/decisions.json:1168` 과 `:1224` 에 `"reviewed_by": "codex-BH-2026-09-07"` 인 결정 2건이 **status active** 로 올라 있다. ② `kb/reviews/codex_BI_prompt_webapp_claim_binding_2026_09_08.md:21` — "BG 회신은 **NO-GO** 였고, 그 중 외주(C-12)와 무관한 것을 전부 처리했습니다." ③ 커밋 `12e6d0c9b` "BG ②: 결속 이주 완료", `cdb86404c` "BG 5: 화면 파생 fit", `16ce6722c` "BH ③ σ 비 실행 셀 계보 **회수 성공**". ④ `db/properties/lpsocl_box331_closure_conditions_2026_09_07.json:30` "회신 BG(B-2)가 잡았다". 즉 둘 다 발송됐고 NO-GO 회신이 왔고 상당부분 이행까지 끝났는데, 파일은 아직 안 보낸 초안이라고 말한다.
- **고치는 법**: BG·BH status 를 `회신 수령 — NO-GO · 이행 중(잔여 N건)` 으로 정정. 잔여는 BI §146 이 이미 명시한다: hazard 전행·전필드 대조, P1 Q4(카드 범위).
- codex 필요: False

### [P0·missing] bg-bh-reply-missing
- **어디**: `kb/reviews/ (codex_BG_reply_*·codex_BH_reply_* 부재)`
- **근거**: `ls kb/reviews | grep -i 'BG\|BH'` 결과에 codex BG/BH **회신 파일이 없다**(internal_BG_reply_c12·internal_BH_reply_c12_v32 는 다른 캠페인). 그런데 그 회신의 판정은 db 6곳에서 이름으로 인용된다 — `citation_hazards.json:224,225`(회신 BG ②), `y_site_preference_dft_2026_09_07.json:84`(회신 BG B-1), `o2_muO_screen_lpscl_2026_09_07.json:5`(회신 BG B-3), `lpsocl_box331_closure_conditions_2026_09_07.json:54,154`(회신 BG Q4), `b2o3_cell_expansion_prereg_2026_09_07.json:8,64`(BH Q4b). 원문이 없으면 이 인용들의 근거를 나중에 못 연다. 이 repo 에는 이미 선례가 있다 — 커밋 `d8a2f7743` "BH 다중감사 C-12 v32 회신 보존 (원문 소실 → 대화 맥락에서 복원)".
- **고치는 법**: d8a2f7743 과 같은 방식으로 BG·BH 회신을 복원해 `codex_BG_reply_webapp_aw_release_2026_09_07.md`·`codex_BH_reply_md_axis_audit_2026_09_07.md` 로 보존하고, 복원본임을 frontmatter 에 명시(verifiedBy: 대화 맥락 복원).
- codex 필요: False

### [P0·wrong] label-collision-bg-bh
- **어디**: `kb/index.md:266-267 vs db/properties/citation_hazards.json:224`
- **근거**: 라벨 BG·BH 가 두 캠페인에 중복 배정됐다: `internal_BG_reply_c12_2026_09_03.md`(C-12 내부 적대적 리뷰, 09-03) ↔ `codex_BG_prompt_webapp_aw_release_2026_09_07.md`(웹앱, 09-07). kb/index.md:266 은 "회신 BG — C-12 내부 적대적 리뷰" 로 매핑하는데, db 의 "회신 BG ②"·"회신 BG B-3" 는 **웹앱 쪽**을 가리킨다. BH 도 같다(kb/index.md:267 = C-12 v32 내부 다중감사, db 의 "BH Q4b" = MD 축 감사). `grep '회신 BG'` 하면 나중의 내가 반대 문서를 집는다.
- **고치는 법**: BG/BH 중복을 이름으로 해소한다 — internal 쪽을 `internal_c12_v30_2026_09_03.md`·`internal_c12_v32_2026_09_03.md` 처럼 **라벨 없는 캠페인+판 이름**으로 바꾸고(라벨 공간은 codex 왕복 전용으로 예약), kb/reviews 규약에 그 원칙을 적는다. 파일명을 바꾸면 kb/index.md 재생성 필요.
- codex 필요: False

### [P0·stale] index-stale-and-partial
- **어디**: `kb/reviews/INDEX.md:3-4 (date/updated 2026-09-03)`
- **근거**: 표에 46행뿐인데 디스크의 프롬프트는 49개다 — **BG·BH·BI(가장 최근 세 건, 09-07~08)가 빠졌다.** 더 크게는 103개 md 중 38개가 INDEX 어디에도 이름이 없다: internal_* 7편 전부(internal_Z/Z2/Z3, internal_BG, internal_BH, internal_lens_review_c12_v34, internal_review_AX), 교차리뷰 A~N 14편, ECERD·section3·self_audit·site_screen·vasp_bundle·sei_neb·codex_stats_question. 원인은 `tools/kb_wiki.py:473-474` 의 정규식이 `^codex_<라벨>_prompt_` / `codex_..._reply_` 만 매치하는 것. 그래서 C-12·폴라론 캠페인의 **마지막 판정(internal_lens v34, internal_Z-3)** 이 색인에 없다. 지금 `python3 tools/kb_wiki.py reviews` 를 돌리면 모순도 5건→3건으로 다르다(AY·BB 가 그새 정정됨).
- **고치는 법**: REV_PROMPT/REV_REPLY 를 `^(codex|internal)_` 로 넓히고, 요청 아닌 문서(ECERD·section3·self_audit)는 별도 절로 나열(누락보다 '분류됨'이 낫다). 그다음 `kb_wiki.py reviews --write` 재생성.
- codex 필요: False

### [P0·missing] no-open-obligations-list
- **어디**: `kb/reviews/INDEX.md (미회신·미이행 절 부재)`
- **근거**: INDEX.md 는 '🔴 모순(status 는 대기인데 증거는 회신 수령)' 절만 있고 **'아직 안 닫힌 것' 절이 없다.** 그 역할을 하는 유일한 문서가 `kb/reviews/codex_F_beta_null_model_2026_08_27.md:252-261` 의 "부록 — **회신 대기 중인 기존 건** (15–16일째)" 표인데 2026-08-27 자라 이미 틀렸다(예: "vasp_bundle_v2 … 회신 대기 (발송이 이것에 막혀 있다)" — 그 사이 C-12 번들은 v15→v40 까지 갔다). 실제 미결 목록은 내가 이번에 세어야 나왔다: **(a) 회신 없이 남은 요청** codex_stats_question(08-11, Q2–Q4) · sei_neb_li3nd_rereview(08-11) · vasp_bundle_v2_rereview(08-11) · codex_A_cascade_ml(08-20) · codex_B_neb_md_tools(08-20) · AG·AH·AN(status sent, 회신 흔적 0) · AC·AD·AE(발송전) · Q·Q2·V(closure incar)·W(mlip selector)(발송 대기). **(b) 회신은 왔는데 이행이 안 닫힌 것** AW(이행 중 — BG §A ⑥ '절반', BI §146 '남은 것: hazard 전행·전필드 대조, P1 Q4') · O·P·R(접수 — 구현 중) · X_bundle(접수) · AK·AL·AM(접수) · T_polaron(이행 중) · U_polaron(이행 대기) · AV(해제조건 ⑧ 잔여) · AR(v16 재생성 대기) · H·I(반영중) · internal_lens_review_c12_v34(진행) · vasp_bundle_codex_reply(v2 구현 대기).
- **고치는 법**: INDEX.md 에 '⛔ 안 닫힌 것' 절 두 개(미회신 / 이행 미완)를 자동 생성으로 추가하고 **맨 위**에 둔다. 이행 미완은 회신 frontmatter 에 `outstanding:` 필드를 신설해 기계가 세게 한다(자유문자열 status 로는 못 센다).
- codex 필요: False

### [P1·wrong] stale-waiting-status
- **어디**: `kb/reviews/vasp_bundle_codex_request_2026_08_11.md:5 · codex_J_prereq_go_nogo_2026_08_27.md:6 · codex_K_what_next_after_seminar_2026_08_28.md:6 · codex_L_vanhove_regimes_2026_08_28.md:6`
- **근거**: 네 건 다 '아직 답 없음'이라고 쓰는데 답이 왔다. ① vasp_bundle_codex_request 는 `status: 회신 대기` 인데 **같은 폴더 같은 날짜에** `vasp_bundle_codex_reply_2026_08_11.md`("Codex 회신 접수 — VASP 번들 HOLD · v2 작업 목록")가 있다. ② J `리뷰대기` — `kb/results/branch_state_2026_08_30.md:50` "li3nd 선행검사 체인(리뷰 J ②~⑤)이 08-28 02:20 에 죽었다", `kb/methodology/selftest_blind_spots_2026_08_28.md:156` "#6 을 지적한 외부 리뷰". ③ K `리뷰대기` — `db/properties/cascade_design_contract_2026_08_28.json:3` "3,615행은 237설계였다 (리뷰 K ②)". ④ L `리뷰대기` — `kb/methodology/vanhove_plateau_70traj_2026_08_28.md:133` "L1·L2·L4 가 여기서 답을 받았다". lint 의 나이 경고는 J/K/L(11~12일)을 안 잡는다.
- **고치는 법**: 네 건 status 정정. J/K/L 은 답 받은 항목과 안 받은 항목이 갈리므로 `회신 수령 — L1·L2·L4 답 · §3-4 미해결` 식으로 부분 상태를 쓴다(L §3-4 는 `vanhove_dr_sweep_2026_08_28.json:80` 이 아직 열려 있다고 적는다).
- codex 필요: False

### [P1·duplicate] c12-chain-split-runs
- **어디**: `runs/sdcp_c12_2026_08_30/REVIEW_REPLY_v37.md · _v37_R2.md · _v38_R3.md · _v39_R4.md · CODEX_VERDICTS_v40.md`
- **근거**: C-12 외주 번들의 리뷰 왕복이 두 폴더로 갈렸다. kb/reviews 에서 이 캠페인의 마지막 문서는 `codex_BF_reply_c12_v29_2026_09_03.md`(v29)와 `internal_lens_review_c12_v34_2026_09_03.md`(v34). 그런데 실제 왕복은 v35→v40 까지 계속됐고 그 회신·판정은 runs/ 에 있다 — `CODEX_VERDICTS_v40.md` 는 "R4 (2026-09-08 · 소스 재검토) — 문의 발송 GO · 생산 실행 보류", "R5 (2026-09-08 · 배포본 실물 대조) — **배포본 대조 GO**" 를 담는다(커밋 2ff1216bc). kb/reviews 만 보는 사람은 이 캠페인이 v29/v34 NO-GO 에서 멈춘 줄 안다.
- **고치는 법**: runs/ 의 REVIEW_REPLY_v37~v39_R4 · CODEX_VERDICTS_v40 을 kb/reviews 로 옮기거나(권장) 최소한 kb/reviews 에 캠페인 포인터 문서 1장을 두어 "v30 이후는 runs/sdcp_c12_2026_08_30/ 에 있다" 를 명시한다. INDEX.md 에도 그 줄을 넣는다.
- codex 필요: False

### [P1·ia] status-kind-vocab
- **어디**: `kb/reviews/*.md frontmatter (status·kind 필드)`
- **근거**: status 값이 **55가지 자유문자열**이다 — `발송 대기`14 · `회신반영`9 · `sent`8(영어) · `리뷰대기`5 · `접수`4 · `회신 대기`3 · `접수 — 구현 중`3 · `발송전`3 · `작성 — 발송 대기`2 · 그리고 1회짜리 40여 가지(`이행 완료 — P0-1 (895af2ed) · P0-2 (1b3fbefc) …`, `v2.1 — codex 2라운드 종료 …`, `HOLD 수용 — v2 구현 대기` 등). kind 는 5가지 철자로 갈렸다 — `review-reply`14 · `review-request`13 · `review_request`8 · `review_reply`3 · `review-prompt`3 · `review`1, 그리고 **103개 중 60개는 kind 자체가 없다**. 그래서 '요청/회신'조차 기계로 못 가른다.
- **고치는 법**: status 를 통제어휘 6개로 고정(`작성중` `발송대기` `발송` `회신수령` `이행중` `종결`)하고 세부는 새 필드 `note:`·`outstanding:` 로 뺀다. kind 는 `review-request`/`review-reply` 둘로 통일하고 kb/SCHEMA.md 에 등재 후 lint 가 강제. 과거 status 문자열의 정보는 note 로 옮겨 보존(지우지 않는다).
- codex 필요: False

### [P1·missing] phantom-verdicts
- **어디**: `kb/reviews/codex_AG_prompt_stageA_go_nogo_2026_08_30.md:11 · codex_AP_prompt_c12_v14_2026_08_31.md:18 · codex_BF_prompt_c12_v29_2026_09_03.md:20`
- **근거**: 이름으로 P0/해제조건을 냈다고 인용되는 회신 넷의 원문이 repo 어디에도 없다. AG:11 "회신 AF 의 P0 다섯 중 **넷을 코드로 닫았고**", AP:18 "회신 AO(v13 제출 NO-GO)의 최종 해제조건 9건을 이행했다", BF:20 "이전 회신: 회신 BE (실행 NO-GO · P0 4건 · P1 3건 · 재승인 최소조건 4개)". `ls kb/reviews | grep -c '_AF_\|_AO_\|_BD_\|_BE_'` = 0. INDEX.md 도 별도로 AB·S·T·U 를 "회신 수령 (원문 파일 없음)" 으로 표시한다.
- **고치는 법**: AF·AO·BD·BE 를 INDEX 에 '원문 없음 — 인용만 존재' 행으로 명시적으로 세우고(빠뜨리는 것보다 '없다고 적힌 것'이 낫다), 복원 가능한 것은 d8a2f7743 방식으로 복원한다.
- codex 필요: False

### [P1·stale] bh-body-outdated
- **어디**: `kb/reviews/codex_BH_prompt_md_axis_audit_2026_09_07.md:61`
- **근거**: 본문이 "**⛔ 저희는 이걸 확인하지 못했습니다.** `modelc_2x_V0.xyz`(124원자)가 저장소에 있으니 **맞춰서 돌렸을 가능성도 똑같이 있습니다. 원장이 말을 안 해서 모릅니다.**" 라고 쓰고 Q1/Q2 를 묻는다. 그런데 그 다음 날 `db/properties/canonical_registry.json:1271` 에 답이 등재됐다 — "2026-09-08-bh3": "BH ③ 계보 회수 — … b2o3 128원자 2436 Å³ · modelc 62원자 1216 Å³ ⇒ **두 셀은 맞춰지지 않았다**(부피 2.00배)." status 가 아직 '발송 대기'라 편집 가능한 초안처럼 보이므로, 나중의 내가 이 파일을 읽고 Q1 을 다시 연다.
- **고치는 법**: 발송본 본문은 **고치지 않고**(발송 시점 기록) 문서 맨 위에 후주 한 줄 — "§1 Q1·Q2 는 2026-09-08 `canonical_registry.json` 2026-09-08-bh3 으로 답이 났다(셀 불일치 확인)" — 을 붙인다. status 정정(bg-bh-status-lie)과 같이 처리.
- codex 필요: False

### [P1·broken] lint-blind-to-bg-bh
- **어디**: `tools/kb_wiki.py:474 (REV_REPLY) · :476 (REV_VERDICT)`
- **근거**: lint 의 모순 검사가 이번 최악의 두 건(BG·BH)을 못 잡는다. 이유 둘: ① `REV_REPLY = ^codex_...` 라 `internal_*` 회신을 아예 안 본다 — 그래서 `codex_AX_prompt_lpsocl_600K_amendment_2026_09_01.md` 는 INDEX 에서 회신 '—' 인데 실제로는 `internal_review_AX_lpsocl_600K_2026_09_04.md` 가 "요청: kb/reviews/codex_AX_prompt_…" 역링크까지 달고 답해 놨다(판정 완료 · 조건부 GO). ② `REV_VERDICT = 회신 ([A-Z]{1,2}\d?)\s*(?:P0|P1|해제조건|판정|Q\d)` 라 db 에 널린 "회신 BG ②"·"회신 BG B-3"·"회신 BG(B-2)" 를 안 센다 → 인용 횟수가 임계 5 에 못 미쳐 모순 경고가 안 뜬다. 실행 결과: `python3 tools/kb_wiki.py lint` = 0 errors, 45 warnings 인데 그중 BG·BH 는 'authoredBy agent 인데 effort 없음' 뿐이다.
- **고치는 법**: REV_REPLY 에 `internal_` 접두 허용 · REV_VERDICT 에 `②③④`·`[A-Z]-\d`·괄호형 추가 · 인용 임계 5→2 로 낮추되 라벨 재사용 판정은 유지. 음성 시험(‘회신 BG ②’ 를 심고 경고가 뜨는지)을 selftest 에 넣는다 — CLAUDE.md 코드 규율의 '음성 경로 포함'.
- codex 필요: False

### [P2·useless] section3-docx-cluster
- **어디**: `kb/reviews/Review_comment_section_3_v1|v2|v3_FINAL|v4|v6|v7.docx · section3_review_comments_compressed.md:4`
- **근거**: docx 6개(약 165 KB)가 폴더 앞머리를 차지하는데 (a) **v5 가 없다**(v1,v2,v3_FINAL,v4,v6,v7), (b) `v3_FINAL` 인데 v4·v6·v7 이 뒤에 왔다 — 이름이 거짓말한다, (c) compressed.md:4 가 "원본: `Review_comment_section_3.docx` (17 comments)" 라고 가리키는 접미사 없는 파일이 **존재하지 않는다**, (d) `litdb/papers/fan2026_…:404` 는 "`kb/reviews/Review_comment_section_3_v1..v7.docx`" 라고 연속 범위처럼 쓴다(v5 없음), (e) **어느 판이 실제 제출본인지 어디에도 안 적혀 있다**(compressed.md 는 '제출용'이라고만 하고 제출 여부는 없다), (f) 바이너리라 LLM 이 못 읽는다 — 나도 못 읽었다.
- **고치는 법**: docx 는 지우지 말고 `kb/reviews/archive_section3/` 로 내리고, 그 폴더에 한 줄 README(어느 판이 제출본인지 · v5 는 없다 · 원본 docx 는 유실)를 둔다. compressed.md:4 의 깨진 원본 참조는 '유실'로 정정.
- codex 필요: False

### [P2·ia] genre-mix-no-readme
- **어디**: `kb/reviews/ (README 부재) · ECERD2600097_review_notes.md · section3_review_*.md · self_audit_2026_08_06.md · site_screen_*_2026_08_11.md`
- **근거**: 한 폴더에 장르 넷이 섞여 있다 — ① codex 왕복(요청/회신) 78편, ② 내부 적대적 리뷰 7편, ③ **남의 심사원고에 대한 우리 피어리뷰**(ECERD 1279줄 + section3 2편 + docx 6, 08-05~06), ④ 자체 코드리뷰(self_audit, site_screen 4편). ③④ 는 'codex 에게 물었다/받았다'와 방향이 반대인데 이름·frontmatter 로 구분이 안 된다(③④ 는 kind 필드 자체가 없다). 게다가 알파벳 정렬 첫 파일이 ③의 ECERD 라 처음 온 사람이 이 폴더를 잘못 이해한다. README 도 없다.
- **고치는 법**: kb/reviews/README.md 를 만들어 (1) 이 폴더가 무엇인지 (2) 장르 넷의 구분 (3) 라벨 규약과 재사용 이력 (4) '막힌 것'은 INDEX.md 상단을 보라 를 적는다. ③(남의 원고 피어리뷰)은 `kb/reviews/peer_review_ECERD2600097/` 하위로 묶는다 — 우리 캠페인 리뷰와 섞이지 않게.
- codex 필요: False

### [P2·buried] reviews-not-on-webapp
- **어디**: `webapp/data.py:313 (`REQUESTS_MD = KB / "reports" / "paper_first_author_requests_2026_08.md"`)`
- **근거**: 웹앱에 `/requests` 라우트가 있지만 그것은 **1저자 요청 대장**이고, `grep -rn 'reviews' webapp/*.py` 결과 kb/reviews 를 읽는 코드는 없다(유일한 히트는 artifact_policy.py:142 의 `docs/reviews/...` 다른 경로). 즉 18,492줄·110파일짜리 리뷰 왕복 — NO-GO 판정과 해제조건이 전부 여기 있는데 — 이 화면에 한 줄도 없다. `db/governance/decisions.json` 은 `reviewed_by: codex-BH-2026-09-07` 로 리뷰를 근거로 쓰는데, 그 근거 문서로 가는 길이 화면에 없다.
- **고치는 법**: `/reviews` 라우트를 붙이거나(캠페인별 접기 + 상단에 '안 닫힌 것'), 최소한 `/governance` 의 결정 행에서 `reviewed_by` 를 kb/reviews 파일로 링크한다. 최신·미결이 위, 종결 캠페인은 접힘.
- codex 필요: False

### [P2·broken] broken-paths
- **어디**: `kb/reviews/site_screen_codex_crossreview_2026_08_11.md (tools/sdcp/ptfe_linio2_uma/) · kb/reviews/vasp_bundle_v2_rereview_request_2026_08_11.md (runs/sdcp_phaseB_vasp_recheck_vendor_v2_2026_08_08/, tools/sdcp/ptfe_linio2_uma/vasp_stage.py) · kb/reviews/section3_review_comments_compressed.md:4 (Review_comment_section_3.docx)`
- **근거**: 내가 kb/reviews/*.md 의 백틱 repo 경로를 전수 대조했다 — 11건이 실물 부재이고 그중 진짜 4건이 위 셋. `ls tools/sdcp | grep -i ptfe` → build_ptfe_c10f22.py·build_ptfe_dimer_c4h2f8.py 뿐(ptfe_linio2_uma/ 없음; `git log --all` 로는 다른 브랜치 커밋 dde6b77cd·b9f1385c7 에 있었다). `ls runs | grep phaseB` → sdcp_phaseB_vasp_v1_2026_08_08 뿐. 나머지 7건은 `file.py:123–456` 꼴 라인번호 표기와 `…` 생략이라 오탐이다. 참고로 vasp_bundle_codex_reply_2026_08_11.md 에는 이미 `<!-- lint-skip-path: Codex 가 인용한 이 파일은 repo 에 없다 -->` 선언이 있다 — 그 관례가 나머지엔 안 붙었다.
- **고치는 법**: 세 곳에 같은 `lint-skip-path` 주석 + "이 파일은 codex 쪽/다른 브랜치 것" 한 줄. compressed.md:4 는 '원본 docx 유실'로 정정. 레거시 문서라 frontmatter 소급은 하지 않는다.
- codex 필요: False

### [P2·ia] never-sent-drafts
- **어디**: `kb/reviews/codex_AC_prompt_manuscript_v8_crosscheck_2026_08_30.md:6 · codex_AD_…:6 · codex_AE_…:6 (모두 `status: 발송전`) · codex_Q_prompt_neutral_ptfe_closure_2026_08_28.md · codex_V_prompt_closure_incar_audit_2026_08_29.md · codex_W_prompt_mlip_selector_validity_2026_08_29.md`
- **근거**: AC·AD·AE 는 `발송전` 이고 `회신 AC/AD/AE` 를 인용한 문서가 kb/ db/ 어디에도 없다 — 라벨만 소비하고 안 보낸 초안이다(라벨 AF 는 그 사이 회신으로 존재하는데 프롬프트가 없어 사슬이 끊긴 것과 짝을 이룬다). Q 는 Q2 가 `supersedes: kb/reviews/codex_Q_prompt_neutral_ptfe_closure_2026_08_28.md` 로 대체했다고 선언했는데 **Q2 자신도 `발송 대기`** 라, 대체된 것도 대체한 것도 둘 다 안 나갔다. AG·AH·AN 은 `sent` 인데 회신 인용 흔적이 0이다.
- **고치는 법**: '안 보낸 초안'과 '보냈는데 답이 없는 것'을 status 로 갈라 놓고(`작성중` vs `발송`), INDEX 에서 종결 캠페인 밑으로 접는다. 지우지는 않는다 — 안 보낸 것도 기록이다.
- codex 필요: False
