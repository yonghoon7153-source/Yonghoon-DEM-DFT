# repo — db/properties (401개) 중 사전등록·마감·카드 축

## 지금 무엇인가
db/properties 401개 파일 중 `schema` 가 prereg/estimand/closure/card/seal 계열인 **카드 19개**가 이 축이다 (나머지는 수치 산출물). 그중 8개는 `ratification.content_digest` 가 박혀 있고 **8개 전부 지문이 실물과 일치한다**(내가 재계산해 대조했다) — 비준 기계는 실제로 작동한다. 그런데 나머지 11개는 지문도 status 도 없거나 산문이고, 이 축 전체를 검사하는 도구는 repo 에 없다. **본 것**: 19개 카드 전부의 frontmatter·status·status_history·ratification, 그중 10개는 본문까지(cascade_d_rel_estimand · lpsocl_box331_estimand · lpsocl_box331_closure_conditions · cascade_seal_v2 · cascade_design_contract · sdcp_stageA_conformer_rule · li2s_cellconv_card · prereg_d_rel · sdcp_polaron_pilot_prereg · b2o3_uma_vs_dft_force_prereg), citation_hazards.json 25건 전량, decisions.json 22건 헤더, canonical_registry.json 스키마·changelog. **못 본 것**: sdcp_polaron_pilot_prereg_S0(66 KB)·sdcp_stageA_closure_conditions(44 KB)·prereg_sdcp_neutral_contrast(29 KB) 의 본문, canonical_registry 42 엔트리 본문, 나머지 ~380개 산출물 파일.

## 처음 오는 사람
처음 온 사람은 이 축을 **찾지 못한다**. db/properties 에 README·색인이 없고, 401개 파일 사이에 카드 19개가 이름으로만 섞여 있다. 파일명에 지위가 안 들어 있어서 `sdcp_stageA_closure_conditions_2026_08_29.json`(SUPERSEDED)과 `lpsocl_box331_closure_conditions_2026_09_07.json`(active·비준)이 이름만으로는 구분이 안 된다. 유일한 색인 후보인 `db/_index.json` 은 2026-06-02 스냅샷이라 이 축을 한 건도 담고 있지 않다. 그래서 실제 진입로는 "decisions.json 22건을 열어 card/record 필드를 역추적" 하나뿐인데, 그 역추적으로도 6개 카드(prereg_d_rel · d_rel_targets · sdcp_stageA_closure_conditions · sdcp_stageA_conformer_rule · li2s_cellconv_card · cascade_seal_v2)는 아예 안 걸린다. 반대로 잘 되는 것 하나 — `lpsocl_box331_closure_conditions_2026_09_07.json` 은 §0 에 "이것을 모르면 놀란다" 를 먼저 놓아서, 그 파일 하나만 열면 캠페인 전체가 복원된다. 이게 이 축이 가야 할 형태다.

## 건드리면 안 되는 것
- **8개 카드의 `ratification.content_digest` 와 그 아래 내용 바이트** — b2o3_cell_expansion_prereg / b2o3_md_closed_retrospective / b2o3_uma_vs_dft_force_prereg / cascade_d_rel_estimand / lpsocl_box331_closure_conditions / sdcp_c12_claim_prereg / sdcp_c12_protocol / sdcp_polaron_pilot_prereg_S0. 8개 전부 지문이 실물과 일치한다. 한 글자만 고쳐도 게이트가 재승인을 요구하도록 설계된 것이고, 그게 의도다. 표시를 붙이고 싶으면 **재비준 절차(tools/sdcp/prereg_ratify.py)를 타야지 손으로 고치면 안 된다.**
- **status_history 배열 전체 — 압축·요약·삭제 금지.** S0 21건 · sdcp_stageA 12건 · sdcp_neutral_closed 10건 · sdcp_c12_claim_prereg 8건이 있는데, 항목마다 '그때 DFT 가 0잡이었다'·'문턱은 손대지 않았다' 같은 **결과 보기 전이었다는 증거**를 담는다. 이게 사전등록의 실체다. 길다고 접으면 규율 자체가 없어진다.
- **철회·오류 자백 절** — sdcp_neutral_closed 의 `⛔_철회_접촉기전_2026_08_29`, sdcp_stageA 의 `_SUPERSEDED_2026_08_30`, b2o3_uma_vs_dft_force_prereg 의 `⚠_1판_지문`("폐기가 아니라 이력이다"), lpsocl_box331_closure 의 `⛔_2026_09_07_스키마_드리프트_정정_회신BG` 3건, cascade_d_rel 의 `0_먼저_박는_사실`. 전부 '우리가 뭘 틀렸나' 의 원본이라 지우면 같은 실수로 돌아간다.
- **SUPERSEDED 카드 파일 자체를 지우지 않는다** — prereg_d_rel_2026_08_28 · d_rel_targets_2026_08_28 · prereg_sdcp_neutral_contrast_2026_08_29 · sdcp_stageA_closure_conditions_2026_08_29 · sdcp_polaron_pilot_prereg_2026_08_31. 사전등록은 사후 편집이 금지라 **표시만 붙이고 값은 손대지 않는다.** prereg_sdcp_neutral_contrast 의 `지위` 가 이미 정답을 적어 뒀다: "이 파일의 **실측 기록**은 여전히 유효하다 — 폐기된 것은 estimand 이지 관측이 아니다."
- **`lpsocl_box331_closure_conditions_2026_09_07.json` 의 §0 `0_먼저_박는_사실_이것을_모르면_놀란다` 구조** — 카드 19장 중 처음 온 사람이 열어서 캠페인이 복원되는 유일한 파일이다. 이 배치(먼저 박는 사실 → 닫는 범위 → 닫힘 조건 → 판정 규칙 → 허용 서술 → 금지 서술 → 재개 조건)를 v3 재편의 **템플릿으로 삼아야지 균질화 대상으로 삼으면 안 된다.**
- **CLAUDE.md 용어 규율의 기계 경로** — `kind: "estimand"`, `estimand_card/v1`, `estimand_card.md`, `canary_geometry`, hazard id `HZ-…`, 결정 id `D-2026-…`. 부르는 이름(보고량 카드 · 대조 잡)만 바꾸고 **필드명·파일명·id 는 그대로 둔다** — 개서하면 원장·게이트가 끊긴다.
- **`cascade_seal_v2_2026_09_08.json` 의 sources sha256 9건** — 봉인의 전부다. 소스 파일을 고치면 sha 를 손으로 맞추는 게 아니라 **재봉인**한다(위 P0 #1 의 조치 순서가 이것이다).

## 발견

### [P0·wrong] axis-corr-emits-retracted-prereg
- **어디**: `tools/doping/axis_corr_csv.py:115,159-166,663 (+ db/properties/cascade_seal_v2_2026_09_08.json sources)`
- **근거**: axis_corr_csv.py:115 `D_REL_GATE = 0.90`, :159-166 이 생성하는 prereg 본문에 `"1_주기준": "Spearman(...) < 0 ... |ρ| ≥ 0.35 · p < 0.05"`, `"2_보조": "...게이트 통과율(D_rel ≥ {D_REL_GATE})..."`, `"3_실패로_읽는_경우": "|ρ| < 0.2 이면 이동도 기술자는 D 를 예측하지 못한다 — cascade 이동도 축의 근거가 없어진다"` 가 그대로 있다. 그런데 2026-09-08 비준된 cascade_d_rel_estimand_2026_09_08.json §1 은 `"0.90_문턱": "...물리 게이트가 아니라 임의 운영 cutoff 였다"` 로, §3 은 `"⛔_삭제": "|ρ| < 0.2 ⇒ 이동도 축 근거 없음"` 으로 셋 다 삭제했다. 더 나쁜 것: 같은 파일 :663-664 의 selftest 가 `say("3_실패로_읽는_경우" in k and "예측하지 못한다" in k["3_실패로_읽는_경우"], ...)` 로 **삭제된 문구가 있어야 통과**하도록 막고 있다. 그리고 이 파일의 sha256 `9091f920df799305134edf72d0f2e0b32c867a9589ebc3fbed07c9d39d8939af` 가 cascade_seal_v2_2026_09_08.json(2026-09-08T14:41 봉인, "이 시각 이후의 cascade 실행은 이 봉인에 귀속된다")의 sources 에 그대로 실려 있다 — 내가 실물 sha256 을 떠서 일치를 확인했다.
- **고치는 법**: axis_corr_csv.py 의 prereg 생성 블록을 비준 카드 §1·§3 으로 교체한다(0.90 게이트 삭제 · ρ̂+Fisher 95% CI+유효표본수 3분 판정 · 등가반증 n≥69 사전고지). selftest :663 의 양성 단언을 뒤집어 **삭제된 문구가 나오면 실패**하는 음성 검사로 바꾼다. 그 다음 cascade_seal_v2 를 새 sha 로 재봉인한다(봉인 규약상 소스가 바뀌면 재봉인이다).
- codex 필요: True

### [P0·wrong] d-rel-prereg-superseded-unmarked
- **어디**: `db/properties/prereg_d_rel_2026_08_28.json:10,12 · db/properties/d_rel_targets_2026_08_28.json`
- **근거**: prereg_d_rel_2026_08_28.json 은 status·status_history·ratification 이 **전부 없고**, :10 `"1_주기준": "...|ρ| ≥ 0.35 · p < 0.05"`, :12 `"3_실패로_읽는_경우": "|ρ| < 0.2 이면 ..."`, 그리고 `"⛔": "기준을 **측정 뒤에 고치지 않는다.**"` 를 살아 있는 사전등록처럼 담고 있다. d_rel_targets_2026_08_28.json 은 `"게이트": "D_rel ≥ 0.9 (Deng 2026 ...)"` 와 39 target 목록을 담는데, 비준 카드 §0 은 `"39개_target_은_실재하지_않았다": "...4축 벡터가 어느 실제 행에도 없는 합성 벡터다(35/39)"` 라고 못박았다. 두 파일 어디에도 표시가 없고, 반대로 비준 카드의 `출처` 도 이 두 파일 이름을 대지 않는다. `grep -c prereg_d_rel db/governance/decisions.json` = 0.
- **고치는 법**: 두 파일에 상단 `지위: ⛔ SUPERSEDED (2026-09-08, cascade_d_rel_estimand_2026_09_08.json)` + 무엇이 삭제됐는지(0.90 게이트 · |ρ|<0.2 · 39 target 합성벡터)를 적는다. 값은 지우지 말고 기록으로 보존한다(사전등록은 사후 편집이 금지다 — 표시만 붙인다). 비준 카드 `출처` 에 두 파일 경로를 역방향으로 넣어 결속을 양방향으로 만든다.
- codex 필요: False

### [P0·wrong] openitems-drel-half-updated
- **어디**: `kb/open_items.md:133-138 (⏭-3)`
- **근거**: ⏭-3 이 "`db/properties/prereg_d_rel_2026_08_28.json` ... D_rel 이 들어오면 그 파일의 `성공기준_사전확정` **그대로** 채점한다" 라고 지시하면서, `- 주기준 \`Spearman(predicted_rank, D_rel) < 0\` 이고 \`|ρ| ≥ 0.35 · p < 0.05\`` 를 살려 두고 다음 줄만 `- ~~실패 조건 |ρ| < 0.2 ...~~ ⛔ **회신 AL P0-4 로 삭제**` 로 취소선 처리했다. 즉 세 기준 중 하나만 갱신됐다 — 2026-09-08 비준 카드 §3 은 주기준(ρ̂ 단독 문턱)까지 CI 3분 판정으로 교체했고 §1 은 2_보조가 쓰는 0.90 게이트도 삭제했다. 같은 문단이 스스로 "⚠ ⏭-2 에는 반영돼 있었는데 여기만 남아 같은 파일 안에서 충돌했다" 라고 전과를 적어 뒀는데, 같은 사고가 한 단계 위에서 반복됐다.
- **고치는 법**: ⏭-3 의 주기준·보조기준 두 줄도 비준 카드 §1·§3 으로 교체하고, 채점 지시의 출처를 prereg_d_rel 파일이 아니라 cascade_d_rel_estimand_2026_09_08.json 으로 바꾼다.
- codex 필요: False

### [P1·broken] closed-cards-no-machine-status
- **어디**: `db/properties/sdcp_neutral_closed_2026_08_28.json · sdcp_doped_closed_2026_08_28.json · lpsocl_box331_estimand_2026_08_30.json · lpsocl_box331_amendment_2026_09_01.json · li2s_cellconv_card_2026_09_01.json · cascade_seal_v2_2026_09_08.json · prereg_sdcp_neutral_contrast_2026_08_29.json · sdcp_stageA_closure_conditions_2026_08_29.json`
- **근거**: 19개 카드의 지위 표기가 네 갈래다. ① 기계 토큰 `status: "ratified"/"proposed"` — 9개. ② `status` 에 산문 — 3개: lpsocl_box331_amendment 는 `status: "✅ **승인 (1저자 2026-09-04) — 안 B.** ..."`, li2s_cellconv_card 는 `status: "⏳ **제안 — 미승인.** ..."`. ③ 한국어 키만 — sdcp_doped_closed 는 `상태: "**active** — 1저자 재승인 2026-08-28 ..."`. ④ **아예 없음** — 6개. 그중 결정적인 것: `sdcp_neutral_closed_2026_08_28.json` 은 `"status" in d == False` 이고 `"상태" in d == False` 다(내가 직접 확인했다). status_history 10건 중 마지막이 `"state": "closed_for_scope_pending_reference_equivalence"` 인데, 기계가 지위를 읽을 자리가 없다. 이 파일은 CLAUDE.md 마감 규율이 "선례: db/properties/sdcp_neutral_closed_2026_08_28.json" 으로 지목한 본보기이자, active·ratified 결정 D-2026-08-28-closure-criteria-first 의 method_ref 다.
- **고치는 법**: 카드 전부에 기계 필드 `status` 를 어휘 하나로 통일한다(proposed / ratified / active / superseded / retracted). 산문은 `지위` 로 옮긴다 — cascade_d_rel 이 2026-09-08 에 "기계 필드 status 와 사람이 읽는 지위 줄이 어긋나 있었다" 로 이미 고친 그 형태가 정답이다. status 가 없는 6개는 status_history 마지막 state 를 승격해 채운다.
- codex 필요: False

### [P1·stale] citation-hazards-stale
- **어디**: `db/properties/citation_hazards.json:222 (`updated`) · hazards 25건`
- **근거**: `"updated": "2026-08-31"` — 8일 전이다. 그 뒤 비준된 cascade_d_rel_estimand_2026_09_08.json 이 `⛔ 300 K 전도도 · σ 비 · 0.90 게이트`, `⛔ 2온도 외삽으로 얻은 300 K 값`, `⛔ |ρ|<0.2 를 근거로 한 '축 근거 없음'`, `⛔ v1 의 front·순위`, 그리고 "과거에 쓴 '필요 산포 9%' 는 ... 철회" 를 금지·철회로 선언했는데 25건 중 한 건도 등재돼 있지 않다. lpsocl_box331_closure_conditions 의 금지 5줄도 없다. 게다가 파일 자신의 `_schema_note` 가 `claim` 과 `id` 를 "화면 결속용"·"화면·handoff 가 data-claim=\"<id>\" 로 이 위험을 선언한다 (회신 BG ②)" 라고 정의해 두었는데, 실제로 `id` 가 있는 항목은 3건(HZ-lpsocl-Ea-diffusive-gate · HZ-cross-system-Ea · HZ-beta-hard-gate), `claim` 은 1건(MD_Ea_eV@b2o3) 뿐이다 — 22건은 결속 수단 없이 목록으로만 있다.
- **고치는 법**: 09-07~08 비준 3건(LPSOCl 마감 · cascade D_rel · b2o3 힘대조)이 만든 금지·철회를 hazards 에 등재하고 `updated` 를 올린다. 등재할 때 `id`(HZ-…)와 `claim` 을 반드시 채운다 — 안 채우면 BG ② 결속이 이 축에서만 뚫린다.
- codex 필요: False

### [P1·stale] b2o3-committee-stale-next
- **어디**: `db/properties/b2o3_committee_2026_09_07.json (`next` 배열 3번째 항목)`
- **근거**: "b2o3 마감 등록 파일이 **없다** — 2026-08-25 은퇴가 마감 규율(2026-08-28) 3일 전이라 `db/properties/b2o3_md_closed_*.json` 이 만들어지지 않았다. 재개 조건이 산문으로만 존재한다. 소급 등록 필요." 그런데 `db/properties/b2o3_md_closed_retrospective_2026_08_25.json` 이 같은 날 커밋 74f174bc2 로 생성됐고 ed0ff0358 로 비준됐다(status ratified, content_digest 검증 통과). `git merge-base --is-ancestor 03d9923d7 74f174bc2` = 참 — 위원회 파일이 마감 파일보다 **먼저** 커밋됐고 그 뒤 갱신되지 않았다. 바로 앞 항목 "BH 는 그 앞에 **소급 마감 기록 + 전향적 재개 조건 봉인**을 요구했다" 도 같이 낡았다(둘 다 이행됐다). 부수 효과: validate_canonical --audit 이 이 문자열을 죽은 출처 `db/properties/b2o3_md_closed_` 로 잡는다.
- **고치는 법**: `next` 3번째 항목을 "✅ 소급 마감 등록 완료 — b2o3_md_closed_retrospective_2026_08_25.json (2026-09-07 비준)" 로 교체하고 앞 항목의 요구도 이행 표시한다.
- codex 필요: False

### [P1·wrong] estimand-before-compute-unratified
- **어디**: `db/governance/decisions.json — D-2026-08-28-estimand-before-compute`
- **근거**: 이 축 전체를 명령하는 메타 결정인데 `decision_state: "proposed"` 이고 `ratification` 키가 **아예 없다**(22개 결정 중 ratification 없는 것은 이것과 superseded 된 D-2026-08-28-30-ddE-obs 둘뿐). CLAUDE.md 는 "보고량·마감 판정은 db/governance/decisions.json 에 등록한다 (proposed → 사람이 ratify 해야 active)" 라고 규정해 놓고, 같은 파일에서 "**새 물리량을 계산하기 전에 kb/templates/estimand_card.md 를 채운다**" 를 2026-08-28 채택 규율로 쓴다. 즉 카드 9장이 이 결정에 근거해 만들어졌는데 근거 자체는 11일째 proposed 다. 대비: 바로 옆 D-2026-08-28-closure-criteria-first 는 decision_state·status 둘 다 active 이고 ratification.state=ratified 다.
- **고치는 법**: 1저자에게 비준을 받아 active 로 올린다(내용을 고칠 필요는 없다 — 도장만 없다). tools/sdcp/prereg_ratify.py 와 같은 규약으로 decision_digest 를 박는다.
- codex 필요: False

### [P1·missing] seal-rules-not-in-ledger
- **어디**: `db/properties/cascade_seal_v2_2026_09_08.json (`rules.phase_melting` · `rules.mlip_applicability` · `rules.invalid_run`)`
- **근거**: 세 규칙이 `"상태": "정해짐 (2026-09-08 결정)"`, `"정해짐 (2026-09-08 결정 — **서술 범위를 낮추는 쪽으로**)"`, `"정해짐 (2026-09-08 결정 — 신설)"` 로 **새 결정**임을 스스로 밝힌다. invalid_run 은 출처가 `"(repo 에 없어서 신설)"` 이고, 내용은 ok/partial/failed 3상태 + "재실행은 **1회만**" 같은 실질 규칙이다. 그런데 `grep -c "phase_melting\|invalid_run\|cascade_seal_v2" db/governance/decisions.json` = 0 이고, 파일 자체에 status·ratification·status_history 가 하나도 없다. 결정 원장은 22건인데 이 셋은 그 밖에 있다.
- **고치는 법**: 세 규칙을 decisions.json 에 정식 결정으로 등재하고(D-2026-09-08-cascade-…), 봉인 파일은 그 결정 id 를 참조만 하게 한다. 봉인은 '그 시점의 규칙 스냅샷' 이지 규칙의 원본 저장소가 아니어야 한다.
- codex 필요: False

### [P1·ia] registry-card-graph-disconnected
- **어디**: `db/properties/canonical_registry.json (entries 42) ↔ 카드 19개`
- **근거**: canonical_registry.json 전문을 문자열로 훑어 `"closure_conditions"` 0회, `"estimand"` 0회, `"prereg"` 0회, `"cascade_seal"` 0회, `"d_rel"` 0회. entry 스키마는 `['system','metric','value','unit','source_path','source_key','method_id','comparison_group','status','prohibitions','updated','note',...]` 로, **어느 마감·사전등록 카드가 이 값을 지배하는지 적을 칸이 없다.** 반대로 카드 쪽도 registry 항목 id 를 대지 않는다. 그래서 예컨대 lpsocl_box331_closure_conditions 가 스스로 지적한 "`canonical_registry` 의 `MD_Ea` 항목 8개가 **전부 `citable` 없음**" 이라는 상황이, registry 를 열면 어느 카드가 그걸 막고 있는지 알 길이 없다.
- **고치는 법**: entry 에 `governed_by: ["<카드 파일 또는 D-… id>"]` 한 칸을 추가하고, 카드 쪽 `4_허용_서술`/`5_금지_서술` 이 지배하는 registry 항목을 명시한다. 두 그래프를 잇는 게 이 축에서 LLM 기억 복원에 가장 크게 남는다 — 지금은 '값' 과 '값의 자격' 이 서로를 모른다.
- codex 필요: False

### [P1·missing] no-gate-verifies-digests
- **어디**: `tools/ (repo 전역) — 해당 검사기 부재`
- **근거**: content_digest 를 쓰는 db/properties 파일은 8개고 내가 전부 재계산해 대조했다 — 8/8 일치다. 그런데 이 대조를 하는 repo 도구가 없다. `grep -rn content_digest` 결과 검증 코드는 `tools/sdcp/build_v7c_trimer.py:5888`(폴라론 S0 전용)과 `tools/sdcp/c12_prereg_amend_kconv.py:269,382`(C-12 전용)뿐이고, `tools/sdcp/prereg_ratify.py` 는 쓰는 쪽이다. `tools/db/validate_canonical.py` 에는 content_digest 문자열이 하나도 없고, `tools/convention_check.py` 에는 prereg·ratif·digest·closure 가 전부 0건이다. 즉 b2o3 3장·lpsocl 1장·cascade 1장의 지문은 아무도 안 본다 — 지금 맞는 것은 운이 아니라 도구가 잘 써 준 덕이지 게이트 덕이 아니다.
- **고치는 법**: validate_canonical.py 에 `--cards` 모드를 붙인다(새 파일 금지 — CLAUDE.md 코드 규율 사다리 ③). ① 카드 계열 파일 열거 ② status 어휘 검사 ③ ratification 있으면 content_digest 재계산 대조 ④ decisions.json 과의 양방향 참조 검사. `--selftest` 에 음성 경로(지문 한 글자 바꾸면 잡히는지) 포함.
- codex 필요: False

### [P2·ia] schema-fragmentation
- **어디**: `db/properties/ — 카드 19개의 `schema` 필드`
- **근거**: 카드 19장에 schema 이름이 16개다. 사전등록만 6가지: `prospective_prereg/v1`(2) · `prereg/v1` · `claim_prereg/v1` · `estimand_prereg/v1` · `estimand_prereg/v2` · `md_estimand_prereg/v1`. 마감만 3가지: `campaign_closure/v1`(b2o3_md_closed_retrospective · sdcp_neutral_closed) · `campaign_closed/v1`(sdcp_doped_closed) · `campaign_closure_prereg/v1`(lpsocl · stageA). 카드는 `estimand_card/v1` 과 `measurement_card/v1` 두 갈래. 파일명도 `_closed_` / `_closure_conditions_` / `_estimand_` / `_prereg_` / `_card_` / `_amendment_` / `_seal_` 이 섞여, 같은 일을 하는 문서를 이름으로 모을 수가 없다.
- **고치는 법**: schema 를 3계열로 접는다 — `prereg/v2`(계산 전 봉인, prospective/claim/estimand 전부 흡수) · `closure/v2`(마감, closed/closure/closure_prereg 흡수) · `amendment/v1`. `record_kind`(prospective/retrospective) 와 `stage`(estimand/protocol/closure) 를 필드로 내려 이름 대신 필드가 구분하게 한다. ⚠ 기존 schema 문자열을 바꿀 때 그 값을 읽는 코드가 있는지 먼저 grep 한다.
- codex 필요: False

### [P2·buried] stageA-superseded-but-thresholds-live
- **어디**: `db/properties/sdcp_stageA_closure_conditions_2026_08_29.json (44 KB) `지위``
- **근거**: `지위: "⛔ **SUPERSEDED (2026-08-30)** — sdcp_c12_protocol_2026_08_30.json 이 대체했다 ... 새 실행의 정본으로 읽지 않는다. ⚠ 단, C1~C4 의 **수치 문턱**(C3 의 0.90 eV·70/30, C2 의 J_f 10/40 meV)은 분석기가 아직 이 정의를 쓴다 — **문턱의 서면 출처가 여기뿐이다.**" 즉 죽은 문서가 살아 있는 문턱의 유일한 출처다. status_history 마지막 항목이 그 전과도 적어 뒀다: "전수 조사 — SUPERSEDED 사실이 파일 맨 아래 키에만 있어 위에서부터 읽으면 살아 있는 정본으로 보였다."
- **고치는 법**: 살아 있는 문턱 3개(0.90 eV · 70/30 % · J_f 10/40 meV)를 후속 정본인 sdcp_c12_protocol_2026_08_30.json 으로 옮겨 박고, 이 파일은 순수 기록으로 강등한다. 옮기기 전에 분석기가 실제로 읽는 상수 위치를 확인한다 — 서면 출처와 코드 상수가 갈라져 있으면 옮기는 순간 갈라짐이 드러난다.
- codex 필요: False

### [P2·ia] polaron-original-no-forward-pointer
- **어디**: `db/properties/sdcp_polaron_pilot_prereg_2026_08_31.json`
- **근거**: `status: "proposed"`, `⚠_비준: "proposed 다 — 사람이 ratify 해야 active"` 인 채로 있고, `연결` 배열이 `[kb/questions/…, kb/reviews/codex_S…, db/properties/sdcp_stageA_conformer_rule…, runs/…/receipt.json]` 로 **후속판 S0 를 가리키지 않는다**. 실제로는 S0(`sdcp_polaron_pilot_prereg_S0_2026_08_31.json`, estimand_prereg/v2, ratified, status_history 21건)가 이걸 격하해 대체했고 S0 의 이력이 "회신 T 의 S0 격하를 받아 범위를 줄여 재등록. 원본은 보존." 이라고 적는다. 뒤쪽만 앞을 알고 앞은 뒤를 모른다. 결정 원장 쪽도 짝이 안 맞는다 — 이 파일을 record 로 가진 D-2026-08-31-sdcp-polaron-Fbb 는 22건 중 유일하게 `decision_state` 키가 **없고** `status: "proposed"` 만 있다.
- **고치는 법**: 원본에 `superseded_by: "db/properties/sdcp_polaron_pilot_prereg_S0_2026_08_31.json"` 과 격하 사유 한 줄을 넣는다(내용은 보존). D-2026-08-31-sdcp-polaron-Fbb 에 `decision_state` 를 채워 22건의 스키마를 맞춘다.
- codex 필요: False

### [P2·useless] audit-noise-on-prospective-cards
- **어디**: `tools/db/validate_canonical.py --audit 출력 "③ 죽은 출처" 11건 중 4건`
- **근거**: 감사가 죽은 출처로 찍는 것들: `b2o3_cell_expansion_prereg_2026_09_07.json → ['db/properties/b2o3_cell_expansion_result_']`, `b2o3_uma_vs_dft_force_prereg_2026_09_08.json → ['db/properties/b2o3_uma_vs_dft_force_result_']`, `sdcp_stageA_closure_conditions_2026_08_29.json → ['db/properties/sdcp_stageA_closed_']`, `sdcp_neutral_closed_2026_08_28.json → ['db/structures/sdcp_wave1/sdcp_neutral__']`. 앞 셋은 카드의 `결과_기록_위치` 가 명시적으로 "(아직 없음)" 이라고 선언한 **미래 경로**고, 마지막은 `db/structures/sdcp_wave1/sdcp_neutral__*.vasp` 라는 **glob** 인데 실물 24개가 존재한다(내가 세어 확인했다). 즉 11건 중 4건이 이 축에서 나오는 오탐이라 진짜 7건이 묻힌다.
- **고치는 법**: 감사에 `결과_기록_위치`·prospective record_kind 예외와 glob 해석을 넣는다. 미래 경로는 '죽은 출처' 가 아니라 '대기 중 산출물' 이라는 별도 줄로 센다.
- codex 필요: False

### [P2·missing] card-axis-has-no-index
- **어디**: `db/properties/ (README 부재) · db/_index.json`
- **근거**: db/properties 에 README 가 없다(`ls db/properties/*.md` = `_RECOVERED_2026_08_13.md`, `sdcp_wave1_job_energies_2026_08_28.md` 둘뿐이고 둘 다 색인이 아니다). 유일한 색인인 db/_index.json 은 `"built": "2026-06-02T13:45:00", "version": "v3 — adds Li adatom diffusion + anode-side interphases"` 로 3개월 전 스냅샷이고, cascade_d_rel_estimand · lpsocl_box331_closure · sdcp_neutral_closed · prereg_d_rel · cascade_seal_v2 · b2o3_uma_vs_dft_force · b2o3_md_closed_retrospective 를 **한 건도 담고 있지 않다**(문자열 검색 전부 False). webapp/data.py:560 이 이미 "_index.json 은 2026-06-02 스냅샷이라 ... 이전 값을 담고 있다" 라고 자백해 뒀다. 덤으로 tools/db/validate_canonical.py:16 docstring 은 "db/properties 는 196개다", :18 은 "(76 중 45가 그랬다)" 라고 적는데 실제는 401개 · 날짜 없음 78개다.
- **고치는 법**: db/properties/README.md 를 만들어 카드 19장만 표로 세운다(파일 · 계 · 단계(estimand/protocol/closure) · 지위 · 비준일 · 대체관계). 사람이 손으로 쓰지 말고 `validate_canonical.py --cards --index` 로 생성해 손편집을 막는다. validate_canonical docstring 의 196/76·45 를 실측으로 고친다.
- codex 필요: False

### [P2·ia] lpsocl-closure-section7-misnamed
- **어디**: `db/properties/lpsocl_box331_closure_conditions_2026_09_07.json 키 `7_미결_1저자_결정``
- **근거**: 키 이름이 "미결" 인데 하위 3건 전부 `"결정": "**A — HOLD 를 결과로 보고하고 이 축을 닫는다.** 추가 계산 0. ..."` 처럼 채워져 있고, 같은 파일 `지위` 가 "§7 결정 3건이 비준됐고 C3(δEa 0.050 eV)·C5(해상도 0.050 eV)·§6 재개조건이 확정됐다" 라고 적는다. 키만 보고 훑으면 아직 열린 결정으로 읽힌다 — 이 축에서 LLM 이 키 이름으로 상태를 판단하는 일이 잦다.
- **고치는 법**: `7_1저자_결정_2026_09_08_비준` 처럼 이름을 결과형으로 바꾼다. 같은 규칙을 카드 전체에 적용한다 — 절 제목은 '무엇이 열려 있나' 가 아니라 '무엇이 정해졌나' 를 말해야 한다.
- codex 필요: False

### [P2·ia] li2s-card-orphan
- **어디**: `db/properties/li2s_cellconv_card_2026_09_01.json`
- **근거**: `status: "⏳ **제안 — 미승인.** 1저자 승인 + 메모리 실측 통과 후에만 던진다."` 로 2026-09-01 부터 7일째 그대로다. decisions.json 참조 0건, kb 참조 0건, status_history 없음, ratification 없음. 즉 제안된 채 어디에도 걸려 있지 않아 '누가 언제 결정해야 하는가' 가 기록에서 사라진다. `sdcp_stageA_conformer_rule_2026_08_31.json` 도 같은 상태다(`status: "proposed"`, decisions 참조 0, W_conf 0.03 eV 가 `"근거": "⏳ **미확정**"`).
- **고치는 법**: proposed 카드는 decisions.json 에 proposed 결정으로 같이 등재하거나(그러면 원장 하나만 보면 대기열이 보인다), kb/open_items.md 에 대기 항목으로 올린다. 지금은 둘 다 아니라 조용히 늙는다.
- codex 필요: False
