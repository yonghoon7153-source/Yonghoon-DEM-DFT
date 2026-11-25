# repo — db/governance + db/structures + 나머지 db

## 지금 무엇인가
db/governance 는 결정 22 · 판정 4 · 산출물 12 를 담은 기계 원장 셋이고, db/structures 는 최상위 85 파일 + 하위폴더 12개(총 369 파일)의 구조 저장소이며, 나머지 db(compositions·doping·external·inputs·interphases·knowledge·literature·pipelines·raw·spectra·_index.json)는 2026-06 에 멈춘 초기 스냅샷과 2026-08~09 에 활발한 external/knowledge 가 섞여 있다. 실제로 연 것 — governance 3파일 전부(결정 22건의 id·state·slot·digest·참조를 프로그램으로 전수 검사 + 6건 본문 정독, 판정 4건·산출물 12건 전부), db/structures/STRUCTURES_NOTE.md·ndo_lpscl16 SUMMARY+anneal_results·si_figure_S3 README·하위폴더 4개 실물 목록, db/_index.json·db/interphases/li3n.json·db/external/PENDING.md·db/properties/_RECOVERED md 전문, canonical_registry.json(entries 42 전수 요약 + 4건 정독 + 메타블록 전부)·citation_hazards.json(위험 25건 전부). 못 본 것 — db/properties 431 파일 중 나머지 약 420개, db/structures 의 좌표 파일 실물(헤더 2개만 봄), 하위폴더 README 12개 중 8개, db/knowledge/fairchem 19파일 중 1개 헤더만, db/spectra·db/raw·db/inputs 는 목록만.

## 처음 오는 사람
처음 온 사람은 db/ 에 들어와서 어디부터 봐야 하는지 알 방법이 없다. db/ 루트에 README 가 없고, db/properties 는 최상위에만 396 파일이 알파벳순으로 깔려 있는데 그중 진짜 입구인 canonical_registry.json(정본 42항목)과 citation_hazards.json(인용 금지 25건)이 b2o3_*.csv 200개 사이에 아무 표시 없이 섞여 있다. 원장 상태 자체는 좋아서 `python3 tools/db/validate_canonical.py` 한 방이면 42항목 대조 + 그래프 무결성이 나오는데, 그 명령이 db 안 어디에도 안내돼 있지 않아 우연히 찾아야 한다. 막히는 지점은 셋 — ① db/_index.json 은 2026-06-02 스냅샷인데 이름이 '_index' 라 목차로 오인하기 딱 좋다(안에 인용 금지된 절대 σ 값이 헤드라인으로 살아 있다) ② 같은 논문이 db/literature · kb/literature_db · litdb/papers 세 군데에 있는데 어느 것이 정본인지 파일만 봐선 모른다(정본은 litdb) ③ db/structures 의 유일한 안내문 STRUCTURES_NOTE.md 가 하위폴더 12개 중 1개만 설명해서, 92 파일짜리 neb_paths 나 71 파일짜리 ndo_lpscl16 에 들어가면 무엇이 살아 있는 값이고 무엇이 철회된 캠페인 잔재인지 판단할 근거가 없다.

## 건드리면 안 되는 것
- **결정 그래프 자체 — 손대면 깨진다.** repo 전체(db·kb·webapp·manuscript·tools·litdb)에서 `D-YYYY-MM-DD-*` 패턴을 긁으면 고유 ID 22개가 나오고 전부 decisions.json 에 등록돼 있다 — 끊긴 참조 0건. supersedes/superseded_by 4개 간선도 양방향이 서로를 정확히 가리킨다(defect-cell-metric↔face-height-gate, c12-path↔ddE-obs). 결정이 참조하는 파일 경로 52개도 전부 실물이 있다(missing 0). 이번 조사에서 발견한 것 중 제일 좋은 게 이것이다.
- **ratification.decision_digest 계약.** 22건의 digest 를 `ratification` 을 뺀 본문의 sha256 으로 직접 재계산해 대조했더니 비준된 19건이 전부 일치한다. 이 계약(webapp/canonical.py:694 · tools/sdcp/prereg_ratify.py:52 가 같은 식, 후자는 '지문은 맨 마지막에' 라는 함정까지 주석으로 남겼다)은 결정 한 글자만 고쳐도 재비준을 요구한다. 결정 본문을 '정리' 하려는 유혹을 반드시 참아야 한다 — 오탈자 하나 고쳐도 19건의 승인이 무효로 보인다.
- **철회·정정 레코드는 지우지 않는다.** A-2026-08-20-b2o3-framework-legacy(state=retracted, binding=diagnostic_unbound, "감사 추적용으로 보존한다") · D-2026-08-16-face-height-gate(retracted) · canonical_registry 의 `_original_flag_2026_08_20` 블록 · note 의 "사유가 바뀐 것이지 없어진 것이 아니다". 낡아 보이지만 무엇이 왜 틀렸는지의 유일한 기록이다. assessments 의 correction 레코드는 1·2·3차 정정을 층층이 남겼는데(`second_error_corrected`, `third_error_corrected`) 그 층위가 곧 방법론이다.
- **소급 선언 표기.** D-2026-09-07-b2o3-md-closure-retrospective 의 `record_kind: "retrospective"` + `⛔_소급_선언`("축은 2026-08-25 에 닫혔고 이 결정은 2026-09-07 에 등록한다. 당시에는 재개 조건이 등록돼 있지 않았다 ... 이 결정이 그것을 조건으로 승격시키지 않는다")과, 사전 결정 쪽의 `results_seen: false`. 언제 닫혔는지와 언제 기록했는지를 가르는 이 구분은 v3 재편에서 절대 뭉개면 안 된다.
- **MD_sigma_ratio_600K/800K/1000K 3항목(b2o3_vs_modelc).** validate 가 '출처 미배선 3개' 로 경고하지만 결함이 아니다 — `citable: false` · note `"non_citable — CSV 금지문 전파. 값 아닌 **차단**을 위한 항목이다."` 로, 값을 담으려는 게 아니라 CSV 의 금지문을 레지스트리에 못박기 위한 항목이다. '출처 없는 항목' 으로 보고 치우면 차단이 사라진다.
- **db/structures/ndo_lpscl16_rietveld_2026_09_07/anneal_2026_09_07/anneal_results.json 의 provenance 블록.** timestamp · python/ase/numpy/scipy/torch 버전 · hostname · uma_model_name · git_commit · git_dirty, 그리고 결과마다 `seed` · `rng_streams{velocities,langevin}` · `struct_sha256{input,post_md,post_relax}` · `⚠_재현`("seed 고정은 재현의 필요조건이지 충분조건이 아니다 — GPU 커널 비결정성·ASE/torch 버전·장치가 바뀌면 달라진다"). repo 전체에서 기록 품질이 가장 높다. 앞으로 만드는 결과 JSON 의 표준으로 삼되 이 파일 자체는 건드리지 말 것.
- **기계 필드명·과거 원문.** CLAUDE.md 용어 규율대로 `kind: "estimand"` · `estimand_card.md` · `canary_geometry` 같은 경로는 그대로 둔다. decisions.json 의 `_history` 항목들(2026-08-20a ~ 2026-09-01)도 회신 원문 성격이라 다시 쓰면 이력이 깨진다 — 뒤에 추가만 한다.
- **db/structures 의 xyz + vasp(+vesta) 페어.** 최상위 85개 중 23개가 '아무도 참조하지 않는다' 로 잡히는데 대부분 짝의 다른 쪽이다(CLAUDE.md: "구조 배포는 xyz + POSCAR(.vasp) 페어 — xyz는 격자 없음 → Boundary 타일링은 vasp"). 참조 수로 정리하면 배포 규약이 깨진다. si_figure_S3/n6_doped.xyz 처럼 좌표가 달라 보이는 사본도 헤더에 유래를 적어 뒀다("NON-PERIODIC molecule from .../sdcp_n6_doped_ring3.xyz ... cell below is a VIEWING BOX, NOT a calculation cell") — 그 헤더가 사본과 원본을 잇는 유일한 끈이다.
- **db/external/PENDING.md.** "여기 있는 것은 아직 못 받았고, 없이는 못 닫는 질문이 걸려 있는 것만이다" 라는 자기 규율을 지키고 있고, 못 구한 3건마다 무엇이 막혀 있는지와 대체 경로까지 적어 뒀다. TODO 목록이 아니라 차단 목록이다 — '오래됐다' 고 정리하면 안 된다.
- **litdb/ 는 문헌 정본.** db/literature 정리를 권했지만 그건 db 쪽 레거시 사본 이야기다. litdb/papers 219편 · litdb/figures 크로핑 · litdb/INDEX.md 는 CLAUDE.md 가 문서화한 유지 대상이고 이번 조사 범위 밖이니 손대지 않는다.

## 발견

### [P0·wrong] hz-b2o3-md-conditional
- **어디**: `db/properties/citation_hazards.json:54-58`
- **근거**: 위험표가 b2o3 MD Ea 를 `"level": "CONDITIONAL"` · `"fix": "FINAL_for_paper.Ea_eV_PAPER 만 인용"` 으로 적고 있다. 그런데 db/governance/decisions.json 의 D-2026-09-07-b2o3-md-closure-retrospective(active · 1저자 비준 2026-09-07T07:32:35Z)는 statement 에서 "b2o3 의 UMA-MD 전도도 축(D · Ea · σ · 구간 Ea)은 **인용 불가**다. 이 축에서 인용 가능한 수는 0개이며, 상태명은 `closed_no_action / non-citable` 이다" 라고 못박았다. citation_hazards.json 의 how_to_use 는 "원고나 그림에 db 값을 넣기 전에 이 표를 먼저 본다" 다 — 먼저 보라고 한 표가 마감된 축의 값을 인용하라고 지시하고 있다. 이 파일의 `updated` 는 2026-08-31 로 09-07 비준 이전이다.
- **고치는 법**: 이 항목을 level=BLOCKED 로 바꾸고 D-2026-09-07-b2o3-md-closure-retrospective 로 결속한다(`claim` 은 이미 `MD_Ea_eV@b2o3` 이니 `decision_id` 를 하나 더 단다). `fix` 문구 'FINAL_for_paper.Ea_eV_PAPER 만 인용' 은 삭제. 겸사겸사 09-07~08 비준 3건(b2o3 마감·LPSOCl 닫힘조건·cascade D_rel)이 위험표에 반영됐는지 한 번에 확인하고 `updated` 를 올린다.
- codex 필요: False

### [P0·wrong] li3n-retracted-value-live
- **어디**: `db/interphases/li3n.json:33, :37`
- **근거**: 33행이 `"pathD_bridge_bridge": "... deduced arithmetically as TS−bridge = 0.054 eV (UMA) / 0.049 eV (DFT SCF)"` 로 값을 그냥 서술한다. 그런데 db/properties/diffusion.json 은 같은 값을 두고 `"CAVEAT_2026-06-06": "The Li3N 0.049/0.054 values came from a thin-slab UMA path now retracted."` 라고 적었고, db/_index.json 도 관련 헤드라인을 `_RETRACTED_headline_...` 접두사로 격리했다. li3n.json 만 철회 표시가 없다. 37행 `"bridge_uma": -0.032` 도 UMA-Li3N 산출값인데 CLAUDE.md 는 "UMA는 Li₃N에 사용 금지 (2026-06 결정론적 편향 판정)" 이고 kb/projects/li_neb_anode_free.md:14 는 "인용은 항상 diffusion.json 기준" 이다. 파일 끝 `next` 는 "Fresh CI-NEB with the corrected on_N_right endpoint (old neb_ci.* used the buggy endpoint -> discard)" 로 2026-06-15 이후 3개월째 결과가 없다.
- **고치는 법**: UMA 유래 수치 두 개에 diffusion.json 과 같은 철회 딱지를 붙이거나(`_RETRACTED_` 접두사 관례) 값을 지우고 `"see": "db/properties/diffusion.json"` 한 줄로 통일한다 — diffusion_barriers 절은 이미 그렇게 돼 있으니 나머지도 같은 방식으로. UMA-Li3N 금지를 citation_hazards.json 에 한 줄 등재해 이 파일을 대상으로 결속한다.
- codex 필요: False

### [P1·duplicate] registry-two-changelogs
- **어디**: `db/properties/canonical_registry.json:1270 (`_changelog`) vs 같은 파일의 `changelog``
- **근거**: 최상위 키가 `['schema','_purpose','_rules','_history','entries','_provenance_audit','changelog','_protocol_generations','_changelog']` 로 changelog 가 둘이다. `changelog` 에는 5건(2026-08-25b ~ 2026-09-07-protocol-generation)이 있고 `_changelog` 에는 가장 최신 1건만 있다 — `"2026-09-08-bh3": "BH ③ 계보 회수 — σ 비 3항목의 실행 셀을 config.xyz(허용 출처)에서 회수... 두 셀은 맞춰지지 않았다(부피 2.00배)"`. `git log -S'"_changelog"'` 로 보면 커밋 16ce6722c 에서 한 번 생겼고, tools/·webapp/ 어디에도 `_changelog` 를 읽는 코드가 없다(grep 0건). `changelog` 만 읽는 사람은 09-08 회수 기록을 통째로 놓친다.
- **고치는 법**: `_changelog` 의 1건을 `changelog` 로 옮기고 `_changelog` 키를 없앤다. `_history`(2026-08-20 에서 멈춤)와 `changelog`(09-07 까지)도 역할이 겹치니 하나로 합칠지 정하고, `_purpose` 에 '변경 이력은 changelog 하나' 를 못박아 셋째 키가 또 생기지 않게 한다.
- codex 필요: False

### [P1·broken] provenance-open-flag-is-prose
- **어디**: `tools/db/validate_canonical.py:572,583 + db/properties/canonical_registry.json:49`
- **근거**: 검증기가 `nprov = sum(1 for e in ents if e.get("provenance_open"))` · `prov = [e for e in ents if e.get("provenance_open")]` 로 문자열의 참거짓만 본다. 그런데 comp1 항목(49행)의 값은 `"✅ comp1 해소 (2026-08-24, provenance_resolved_2026_08_24 참조). ⏳ modelc 는 재계산 진행 중. ..."` 로 시작한다. 그래서 실행할 때마다 `⚠ provenance_open 2건: gap_eV/comp1, gap_eV/modelc` + `값은 정본 파일과 일치하지만 **그 값을 만든 실행을 파일로 재현할 수 없다.**` 가 찍히는데, comp1 은 같은 파일 `provenance_resolved_2026_08_24` 에 재현 기록(VBM 2.1281 / CBM 4.1937 / gap 2.0656, irr_k 170 일치)이 있다. 게이트가 자기 원장 내용과 반대로 말한다.
- **고치는 법**: 필드를 둘로 가른다 — `provenance_state: open|resolved|permanently_unresolved`(기계 어휘)와 `provenance_note`(산문). 검증기는 state 만 세고 산문은 출력하지 않는다. 해소된 항목이 매번 경고로 뜨면 진짜 경고를 못 본다.
- codex 필요: False

### [P1·stale] gap-modelc-contradiction
- **어디**: `db/properties/canonical_registry.json:49 vs :100 (+ db/governance/artifacts.json:94)`
- **근거**: 49행(comp1)은 `⏳ modelc 는 재계산 진행 중` 이라 적고, 100행(modelc 자기 항목)은 같은 사안을 `⇒ KISTI 원본이 없으므로 이 2건은 **영구 미해소로 본다.**` 로 닫아 놨다. 한 레지스트리 안에 '진행 중' 과 '영구 미해소' 두 판정이 공존한다. modelc 항목의 `method_integrity_flag.severity` 는 아직 `⛔ 방법 불일치 의심 (재현 불가보다 심각)` 인데 comp1 쪽 같은 블록은 `✅ **해소됨 (2026-08-24)**` 로 바뀌었다. artifacts.json:94 도 `"comp1 만. modelc 는 2026-08-24 진행 중"` 이라 적고 있고 오늘이 2026-09-08 이니 15일째 미갱신이다.
- **고치는 법**: gabia 의 modelc fixed-occ nscf 가 끝났는지/죽었는지 1저자에게 한 줄 확인받고 세 곳(registry comp1·registry modelc·artifacts A-comp1-modelc-gap-run)의 문장을 하나로 통일한다. 끝났으면 comp1 과 같은 `provenance_resolved_*` 블록을, 죽었으면 '영구 미해소' 하나만 남긴다 — 둘 다 남겨 두는 게 지금의 문제다.
- codex 필요: False

### [P1·stale] artifacts-frozen-0820
- **어디**: `db/governance/artifacts.json:299 · db/governance/assessments.json:74`
- **근거**: artifacts.json 12건이 전부 `verified.date: "2026-08-20"` 이고 `_history` 도 `{"2026-08-20a": "신설..."}` 하나뿐이다. A-highT-reseed-traj(status=lost) 의 note 는 `"...**2026-08-20 재실행 중** (kgy b2o3 6런 · gabia modelc 6런, --save_traj 켬)"`, assessments.json:74 는 `"rerun_status": "2026-08-20 진행 중 — kgy(b2o3 6런) + gabia(modelc 6런), --save_traj 로."` 다. 그 재실행이 채우려던 축은 D-2026-09-07-b2o3-md-closure-retrospective 로 인용 불가 마감됐고, 그 결정의 reopen_criteria 는 "진단 목적의 재실행은 결과와 무관하게 이 마감을 바꾸지 않는다" 다. 결말이 이미 난 일이 19일째 '진행 중' 으로 남아 있다.
- **고치는 법**: A-highT-reseed-traj 와 assessments 의 rerun_status 를 09-07 마감 결정으로 결속해 종결시킨다(`decision_ids` + status_history 한 줄). artifacts.json `_history` 에 '2026-09-07: b2o3 MD 축 마감으로 이 재실행의 목적이 소멸' 을 추가한다.
- codex 필요: False

### [P1·ia] assessments-stub
- **어디**: `db/governance/assessments.json (레코드 4, claim 2) vs db/properties/canonical_registry.json entries 42`
- **근거**: assessments.json 의 _purpose 는 "게이트 판정의 **단일 원장**. canonical claim 은 판정을 품지 않고 required_assessment_refs 로 참조만 한다. **판정을 값 옆에 써 넣으면 consumer 마다 '현재 판정'을 다르게 고를 수 있다**" 다. 그런데 `required_assessment_refs` 를 가진 레지스트리 항목은 MD_Ea_eV/b2o3 와 MD_Ea_eV_singleseed/b2o3 둘뿐이고(전수 확인, dangling 0), 나머지 provisional 13건은 판정을 전부 `note` 산문에 품고 있다 — 예: MD_Ea_eV/lpsocl 의 note `"⛔ 인용 보류. Ea 0.2867 은 **게이트 탈락한 600 K 점을 포함한 3점 적합**이다..."`. _history 도 자백한다: "나머지 게이트(lpsocl·comp1 MD_Ea)는 레거시 경로 유지 — 확대는 slice 통과 뒤 별건이다." slice 는 통과했는데(validate ✅) 확대가 19일째 안 왔다.
- **고치는 법**: 판정을 품은 provisional 항목(최소 MD_Ea_eV/lpsocl · MD_Ea_eV_singleseed/comp1 · MD_Ea_eV_disorder/comp2 · SDCP_Eads_eV__* 7건)을 assessments 레코드로 뽑고 note 는 참조만 남긴다. 한꺼번에 못 하면 assessments.json _history 에 '확대 미완 — 현재 2 claim 만 배선' 한 줄을 적어 이 원장을 '전부' 로 오독하지 않게 한다.
- codex 필요: False

### [P1·wrong] estimand-decision-unratified
- **어디**: `db/governance/decisions.json — D-2026-08-28-estimand-before-compute`
- **근거**: 이 결정은 `"decision_state": "proposed"` 이고 `ratification` 블록이 아예 없다(22건 중 비준 블록 없는 것은 이것과 superseded 1건, status-only 1건뿐). 그런데 CLAUDE.md 는 같은 규율을 "## 계산 규율 — **던지기 전에 보고량 정의** (2026-08-28 채택)" 로 채택된 표준으로 서술하고, 이후 결정 5건(c12-path · kconv-axis-excluded · absolute-eads · lpsocl-closure-conditions · cascade-d-rel)이 전부 이 규율 위에 세워졌다. decisions.json 의 _rules 는 "decision_state: proposed | active | superseded | retracted. **ratification 없이 active 가 될 수 없다.**" 다. 같은 날 등록된 쌍둥이 D-2026-08-28-closure-criteria-first 는 비준돼 active 인데 이것만 11일째 proposed 다.
- **고치는 법**: 1저자 비준을 받아 active 로 올린다(tools/sdcp/prereg_ratify.py 로 digest 포함). 비준이 아직 이르면 반대로 CLAUDE.md 의 '2026-08-28 채택' 을 '제안 상태' 로 낮춰 원장과 맞춘다 — 지금은 두 문서가 서로 다른 말을 한다.
- codex 필요: False

### [P1·broken] depends-on-unchecked
- **어디**: `db/governance/decisions.json (depends_on 4건) · webapp/canonical.py validate()`
- **근거**: 결정 4건이 `depends_on` 을 쓴다(S0-four-layer→Fbb, c12-kconv-axis-excluded→c12-path, c12-absolute-eads→c12-path, lpsocl-closure-conditions→box331-400ps-uniform). 그런데 `grep -n depends_on webapp/canonical.py tools/db/validate_canonical.py webapp/app.py webapp/templates/governance.html` 이 0건이다 — supersedes/superseded_by 만 dangling 검사(canonical.py:869, :889)를 받고 depends_on 은 아무도 안 본다. _rules 7개에도 depends_on 이라는 말이 없다. 실제로 한 간선이 이미 어긋나 있다: D-2026-08-31-sdcp-polaron-S0-four-layer 는 `decision_state: active` 인데 그것이 depends_on 하는 D-2026-08-31-sdcp-polaron-Fbb 는 `status: proposed` 이고 decision_state 키 자체가 없다. ID 는 전부 원장에 있으니 끊긴 참조는 없다 — 문제는 상태 정합성을 아무도 검사하지 않는다는 것이다.
- **고치는 법**: canonical.py validate() 에 depends_on 검사 두 줄 — ① 대상이 원장에 있는가 ② active 결정이 proposed/retracted 를 depends_on 하면 오류. _rules 에 depends_on 의 뜻을 한 줄 정의한다(지금은 정의 없이 쓰이는 간선이다). S0-four-layer/Fbb 쌍은 Fbb 를 비준하거나 S0 를 proposed 로 되돌려 맞춘다.
- codex 필요: True

### [P1·missing] nd-anneal-unregistered
- **어디**: `db/structures/ndo_lpscl16_rietveld_2026_09_07/anneal_2026_09_07/anneal_results.json`
- **근거**: 커밋 83c868a97 "Nd2O3-LPSCl1.6 어닐 6셀 회수 — UMA 500 K 20 ps + relax (순위: distributed < free_s < bo4)" 의 결과가 여기에만 있다. 값도 그 순서다(n4fu: distributed −236.98 < free_s −235.15 < bo4 −234.19 eV; n5fu 도 같은 순서). 그런데 `grep -rl "nd_anneal_2026_09_07\|anneal_results" db/properties/ kb/` 는 kb/methodology/cascade_lessons_transfer_2026_09_08.md 한 줄만 나온다("Nd O-모티프 4셀 — UMA 순위(distributed < free_s < bo4)를 DFT 로 재채점 중"). db/properties 항목 없음 · canonical_registry 없음 · citation_hazards 없음 · 결정 노드 없음. 같은 repo 의 db/properties/cascade_seal_v2_2026_09_08.json:79 는 "cascade 도판트 30종에 대한 UMA 검증은 **없다** — 따라서 이 캠페인의 결과는 **'UMA 내부 순위'로만 서술한다**" 라고 못박았는데 Nd 순위에는 그 딱지가 없다.
- **고치는 법**: citation_hazards.json 에 한 줄 — level=PREVIEW, what='Nd O-모티프 UMA 순위 distributed<free_s<bo4', why='DFT 재채점 전, UMA 내부 순위', fix='커밋 51b5dec21 --from_xyz scf 4셀 결과 뒤 재판정'. 결과 JSON 을 db/properties/ 로 옮기거나(구조 폴더는 구조만) 최소한 db/properties 쪽에 포인터 파일을 둔다 — 지금은 db/properties 를 grep 하는 사람에게 이 캠페인이 안 보인다.
- codex 필요: False

### [P1·missing] db-no-entrance
- **어디**: `db/ (README 없음) · db/properties/ (최상위 396 파일, 색인 없음)`
- **근거**: `find db -iname "readme*"` 가 db/structures 하위 6개와 db/external 3개만 잡는다 — db/ 루트에도 db/properties/ 에도 README 가 없다. db/properties 는 최상위에만 396 파일(csv 217 · json 188)인데, 실질 입구인 canonical_registry.json(90 KB, entries 42)과 citation_hazards.json(how_to_use 에 "원고나 그림에 db 값을 넣기 전에 이 표를 먼저 본다" 라고 적혀 있음)이 알파벳 목록 한가운데 아무 표시 없이 놓여 있다. 검증 명령 `python3 tools/db/validate_canonical.py`(돌리면 42항목 대조 + 거버넌스 그래프 무결성이 한 화면에 나온다)도 db/ 안에서는 안내되지 않는다.
- **고치는 법**: db/README.md 를 만든다 — 10줄이면 된다. ① 값을 인용하려면 canonical_registry.json → citation_hazards.json 순서 ② 규약·판례는 db/governance/decisions.json ③ 검증은 `python3 tools/db/validate_canonical.py` ④ db/_index.json 은 2026-06-02 스냅샷이라 값의 근거가 아니다 ⑤ 문헌 정본은 litdb/, db/literature 는 레거시. 다음 세션이 이 폴더에서 되찾아야 하는 건 값이 아니라 이 다섯 줄이다.
- codex 필요: False

### [P1·stale] structures-note-covers-3-of-14
- **어디**: `db/structures/STRUCTURES_NOTE.md:32`
- **근거**: db/structures 의 유일한 안내문인데 `마지막 갱신: 2026-08-28` 이고 다루는 것은 comp1 · modelc · sdcp_wave1 셋뿐이다. 하위폴더 12개 중 README 가 없는 게 6개다: c12_frozen(5) · ndo_lpscl16_rietveld_2026_09_07(71 파일) · neb_paths(92 파일) · sdcp_orca_gs0(6) · vgcf_hbn(4) · y_site_test(README.json 만). 더 결정적인 건 09-08 비준된 D-2026-09-08-lpsocl-box331-closure-conditions 가 method_ref 에서 명시적으로 지목하는 `lpsocl_relaxV0_3x3x1.xyz(558원자)` — 지금 돌고 있는 400 ps 9런 캠페인의 바로 그 구조 — 가 이 노트에 한 번도 안 나온다.
- **고치는 법**: '어떤 구조가 지금 어느 캠페인의 정본인가' 표로 다시 쓴다. 최신·활성(lpsocl_relaxV0_3x3x1.xyz → D-2026-09-08-... / ndo_lpscl16_* → Nd 재채점)을 맨 위, 사용금지(BROKEN_PS4)와 종료 캠페인은 아래 접힘. README 없는 하위폴더 6개에 두 줄짜리 README(무엇 · 어느 결정·어느 결과 파일과 짝)를 넣는다.
- codex 필요: False

### [P1·wrong] banned-structure-only-in-filename
- **어디**: `db/structures/lpscl_relaxed_conv_52atoms.cif.BROKEN_PS4_dissociated`
- **근거**: 사용금지 판정이 파일명 확장자와 STRUCTURES_NOTE.md 산문에만 있다("❌ ... **사용 금지**. conventional-cell 변환 사고로 PS₄ 해리"). 그런데 옆 파일 db/governance/artifacts.json 의 _rules 가 정확히 이걸 금지한다 — `"★ 판정은 **파일명이나 사람 기억에 두지 않는다.** ToBeDelete_ 같은 접두사는 판정이 아니라 흔적이다 — 여기 적어야 판정이다."` 이 파일은 artifacts.json(12건)·canonical_registry·citation_hazards 어디에도 없다. 참조하는 곳은 4군데(kb/results/lpscl_vs_lpscl16_v3_comparison.md · tools/electronic/run_comp2_relax_gabia.sh · STRUCTURES_NOTE.md · db/properties/eos.json)로 흩어져 있다.
- **고치는 법**: artifacts.json 에 `status: suspect_banned` 로 등재한다(location.kind=repo, ban 근거·발견일·영향받은 소비자 4곳). 파일명은 흔적으로 그대로 두되 판정은 원장으로 옮긴다 — 이 규칙을 만든 사건(ToBeDelete_ 접두사)과 똑같은 형태가 db/structures 에 그대로 남아 있는 셈이다.
- codex 필요: False

### [P1·missing] offrepo-ledger-12-of-102
- **어디**: `db/governance/artifacts.json (12건) vs db/ 전체 텍스트의 원격 경로`
- **근거**: artifacts.json 의 _purpose 는 "**repo 밖 원자료의 기계 가독 원장.** ... 2026-08-20 에 하루 동안 같은 사고가 다섯 번 났다 — 산출물은 있는데 그 위치·지위·판정이 기계 경로 밖에 있어서 매번 다시 찾아야 했다" 다. 그런데 db/ 안의 json·md 를 `(gabia|kgy|kserver116|x3430a02)` 경로 패턴으로 훑으면 서로 다른 원격 경로 102개가 나온다(gabia:/data/work/runs/multi_category_2026_05_26_v23/, kgy:~/work/li3n_dft/, x3430a02/kgy/manuscript_support/post_relax/comp5/ACF.dat, /data/work/runs/nd_anneal_2026_09_07/ 등). 등재는 12건이다. 게다가 db/interphases/li3n.json 은 같은 머신을 `kserver116:` 로 부르는데 repo 나머지는 전부 `gabia` 라(둘이 같은 기계라는 사실은 kb/results/session_timelog_2026_06_04.md:11 에만 있다) grep 으로 안 이어진다.
- **고치는 법**: 전수 등재는 비싸니 기준을 정한다 — canonical/provisional 값의 출처인 원격 경로만 등재(registry 42항목 기준이면 수십 건 이내). 호스트 별칭을 gabia 로 통일하거나 artifacts.json _rules 에 host 어휘표(kgy · gabia(=kserver116-27) · KISTI neuron(x3430a02) · DESKTOP-K1BLBIJ)를 박아 grep 이 통하게 한다.
- codex 필요: False

### [P2·stale] index-json-stale-headline
- **어디**: `db/_index.json:140, :93 (built 2026-06-02)`
- **근거**: 140행 `"headline_modelc_v3_sigma_300K_estimate_Scm": "14e-3 (NE, MLIP overshoot factor ~3-5x vs expt)"` — CLAUDE.md 는 "σ는 Nernst–Einstein(Haven=1) — **절대값 인용 금지**" 다. 139행 `"headline_modelc_v3_Ea_eV": 0.224` 도 canonical_registry 의 MD_Ea 항목들이 전부 citable 없음인 것과 어긋난다. 93행은 `"has_neb_dft_full": "running_since_2026-06-02"` 로 3개월째 '진행 중'. webapp/data.py:97 이 이 파일을 읽고 data.py:560 주석은 "렌더 단계에서 '폐기·canonical 아님' 플래그만 붙인다" 라고 적었지만 그 플래그는 `_STALE_PATH = re.compile(r"band_?gap")` 뿐이라 밴드갭만 걸린다. 다만 화면에 뜨는 data_points 292개에는 σ 가 없어(전수 확인) 현재 화면 노출은 없다 — 위험은 이 파일을 grep 하는 다음 세션 쪽이다.
- **고치는 법**: σ 헤드라인 두 개를 같은 파일이 이미 쓰는 방식(`_RETRACTED_` 접두사 + `_retraction_note`)으로 격리하거나 삭제한다 — 올바른 선례가 바로 옆 li_adatom_diffusion_barrier 절에 있다. `has_neb_dft_full` 은 sei_neb 철회(n_citable=0)를 가리키게 바꾼다. 파일 첫머리에 `"_WARNING": "2026-06-02 스냅샷 — 값의 근거로 쓰지 말 것. 정본은 db/properties/canonical_registry.json"` 한 줄.
- codex 필요: False

### [P2·duplicate] literature-triplicate
- **어디**: `db/literature/ · kb/literature_db/ · litdb/papers/`
- **근거**: `diff -q` 결과 세 파일이 바이트 동일이다 — damore_2022_lpscl_symmetry_breaking_qha.md · pustorino_2025_lpscl_li_ordering_mechanical.md · sundar_2025_lpscl_coating.md 가 db/literature/ 와 kb/literature_db/ 양쪽에 그대로 있다(IDENTICAL ×3). sundar 는 litdb 에도 있다: db/literature/sundar_2025_lpscl_coating.md(DOI 10.1002/advs.202513191, 마지막 커밋 2026-06-11) vs litdb/papers/sundar2025_oxide_coating_screening_lpscl.md(같은 DOI, `digested 2026-06-26`, elements·methods 태그 완비). CLAUDE.md 가 문서화한 문헌 체계는 litdb 하나(digest 219편)이고 db/literature 9개 md 는 전부 2026-06-11~21 에서 멈췄다.
- **고치는 법**: 중복 3건은 litdb 로 흡수하거나(litdb 에 없는 damore·pustorino 는 digest 로 신규) 리다이렉트 한 줄만 남긴다. db/literature 의 csv 2개(argyrodite_dft_littable.csv · argyrodite_computational_littable.csv)는 표라 성격이 다르니 남기되 db/README 에 '문헌 산문은 litdb, 표만 여기' 라고 적는다.
- codex 필요: False

### [P2·broken] hazard-file-field-unresolvable
- **어디**: `db/properties/citation_hazards.json — hazards[].file 25건 중 2건`
- **근거**: `file` 이 실물 경로가 아닌 것이 둘이다 — `"db/properties/nd_icohp.json · bonds.json"`(경로 두 개를 가운뎃점으로 이어 붙임)과 `"tools/ionic/msd_diffusive_check.py (규약)"`(주석 괄호 포함). 25건을 os.path.exists 로 돌리면 이 둘만 MISS 다. how_to_use 가 기계 소비를 전제하는데 file 로 조회하면 이 두 위험이 조용히 안 걸린다. 참고로 `id`(HZ-*) 필드가 있는 항목은 25건 중 3건뿐이다.
- **고치는 법**: `file` 을 배열로 바꾸거나(`files: ["db/properties/nd_icohp.json", "db/properties/bonds.json"]`) 항목을 둘로 쪼갠다. 주석은 별도 필드(`scope: "규약"`)로 뺀다. 전 항목에 `id` 를 붙이면 file 없이도 결속이 된다.
- codex 필요: False

### [P2·broken] file-comments-dangling
- **어디**: `db/file_comments.json:2`
- **근거**: 최상위 키 20개 중 하나가 `"litdb/figures/adeli2019_halide_substitution_boosting_argyrodite/fig_20.png"` 인데 그 폴더에는 fig_2~5 · fig_S1~S10 · tab_1/2/S1/S2 만 있고 fig_20.png 는 없다(내용도 `"text": "table"` 한 줄이라 tab_* 를 잘못 가리킨 것으로 보인다). 나머지 19키와 file_highlights.json 3키는 전부 실물이 있다. 덧붙여 두 파일은 litdb 파일에 대한 주석인데 db/ 에 산다.
- **고치는 법**: dangling 키 1건 정리(실제 tab_*.png 로 옮기거나 삭제). 두 주석 저장소를 litdb/ 아래로 옮길지, db/ 를 '주석 저장소' 로도 쓰기로 명시할지 한쪽으로 정한다 — 지금은 db 를 '계산 결과' 로 알고 들어온 사람이 92 KB 짜리 파일을 만나 당황한다.
- codex 필요: False

### [P2·duplicate] cascade-duplicate-ratify
- **어디**: `db/governance/decisions.json — D-2026-09-08-cascade-d-rel-estimand.status_history`
- **근거**: status_history 3개 중 2·3번이 완전히 같다 — `{"at": "2026-09-08", "state": "active", "note": "1저자 비준 (scientific_owner). 사전등록 재봉인과 함께."}` 가 두 번 들어 있다. 비준 자체는 유효하다: 22건 전부의 decision_digest 를 재계산해 대조했고 이 건도 일치한다(sha256:edc4194b…). 중복 기록이지 무결성 문제는 아니지만 '두 번 비준받았다' 로 읽힐 수 있다.
- **고치는 법**: 지금 고치지 말 것 — decision_digest 가 status_history 를 포함한 본문의 해시라(prereg_ratify.py:52 계약) 삭제하면 재비준이 요구된다. 다음에 이 결정을 개정할 때 같이 정리한다. 대신 ratify 도구에 '같은 (at, state, note) 가 이미 있으면 추가하지 않는다' 가드를 넣어 재발을 막는다.
- codex 필요: False

### [P2·ia] june-frozen-db-dirs
- **어디**: `db/compositions/ · db/doping/ · db/pipelines/ · db/interphases/`
- **근거**: 네 폴더 15개 파일에 `updated`·`date`·`collected` 같은 날짜 필드가 하나도 없다(전수 확인). git 으로만 알 수 있는데 db/doping/*.json · db/pipelines/*.json · db/interphases/lic6.json 은 마지막 커밋이 2026-06-11(제목이 'seminar v1.8 ...' 로 이 파일들과 무관한 대량 커밋), db/interphases/li3n.json 2026-06-15, db/compositions/modelc_nd_doped.json 2026-06-17 이다. modelc_nd_doped.json 의 `compute_plan_summary` 는 "Top 20 DFT relax (~5 days) ... total_time_KISTI: ~10 days" 같은 6월 계획서인데, 실제 Nd 축은 그 뒤 Rietveld 기반 6셀 어닐(2026-09-07)로 완전히 바뀌었다. 계획서인지 결과인지 파일만 봐선 구별이 안 된다.
- **고치는 법**: 각 파일 최상위에 `"_status": "plan|current|frozen"` 와 마지막 검토일 한 줄. modelc_nd_doped.json 의 compute_plan_summary 는 `_superseded_by: "db/structures/ndo_lpscl16_rietveld_2026_09_07/"` 로 잇는다 — 다음 세션이 6월 계획을 현재 계획으로 오독하는 게 가장 비싼 실수다.
- codex 필요: False

### [P2·useless] neb-paths-92-undocumented
- **어디**: `db/structures/neb_paths/ (92 파일, README 없음)`
- **근거**: li2s 36 · li3nd 56 파일이 평평하게 깔려 있다 — initial/img1~7/final/saddle/path_local{2.8,3.2,3.6,4,5,6,8}A 가 각각 .vasp+.xyz 쌍. 이 캠페인의 결과 파일 db/properties/sei_neb.json 은 `"retracted": true, "n_citable": 0, "retraction_reason": "인용 가능한 결과가 0건이다. ... 이 파일의 어떤 값도 인용하지 말 것."` 이고 citation_hazards 에도 level=BLOCKED 로 올라 있다. 그런데 구조 폴더 쪽에는 그 사실이 한 글자도 없다. 작업 목록에도 '#8 NEB: kgy 에서 collect_neb --merge 실행 → sei_neb.json 커밋' 이 pending 이라, 재계산 대기인지 폐기물인지 폴더만 봐선 모른다.
- **고치는 법**: 세 줄짜리 README — ① 어느 캠페인 구조인지 ② db/properties/sei_neb.json 이 전량 철회 상태라는 것 ③ 구조 자체는 시각화·재계산 입력으로 유효하다는 것(값이 철회된 것이지 좌표가 틀린 게 아니다). 파일은 지우지 말 것 — 재계산 입력이다.
- codex 필요: False
