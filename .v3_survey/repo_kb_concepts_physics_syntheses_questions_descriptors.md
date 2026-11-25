# repo — kb/concepts + physics + syntheses + questions + descriptors

## 지금 무엇인가
37개 문서다(concepts 13 · physics 6 · syntheses 6 · questions 11 · descriptors 1, 총 8,463줄). **전문을 끝까지 읽은 건 14편**(bandgap · msd_reading · beta-gate · md · bvse · ordered_vs_disordered · vacancy_effects · li_ordering_sensitivity · br_substitution · lpsocl_low_beta · nd_doping_two_axis · li3nd_pristine · xu2026 · md_sampling_variance), 나머지 23편은 frontmatter + 목차 + 「우리 캠페인 적용」·수치표·Status Log 같은 값이 박히는 절만 봤다 — cohp · elastic · neb 본문의 수식 전개부와 sdcp 카드 5편의 중반부(§B~§F 설계표)는 안 봤다. 성격은 두 층으로 갈린다: 2026-08 이후 카드는 자기정정·반론절·인용금지까지 갖춘 상급 문서인데, 2026-06 이전 legacy(physics 4편 + descriptors)는 frontmatter도 출처 경로도 없이 지금은 철회된 값을 그대로 말하고 있다.

## 처음 오는 사람
개념 하나를 처음 배우기엔 아주 좋다 — bandgap · dft · bvse · ordered_vs_disordered · oxidation_vs_mechanical 은 정의→식→우리 실측→한계 순서라 그대로 읽힌다. 막히는 데는 세 군데다. ① **어느 게 현행인지 알 방법이 없다.** kb/index.md 가 폴더별 가나다순이고 날짜도 status 도 안 찍는다(questions 만 [open] 표시). 그래서 `br_substitution_effects.md`(2026-06-11, 폐기된 DOS 갭)와 `nd_4f...`(2026-09-03 교정본)가 같은 목록에 나란히 있다. ② **개념 카드 첫머리가 옛 판정이다.** `beta-gate.md` 는 §1 표가 "β 0.8–1.2 = ✅ 인용 가능"으로 시작하는데 폐기 선언은 265줄 아래 §7-5 에 있고, §12 「실무 순서」는 아직도 β≥0.80 으로 시작한다. 처음 읽는 사람은 폐기된 게이트를 배우고 나간다. ③ **정본으로 가는 다리가 없다.** 문서가 `db/properties/canonical_registry.json`·`citation_hazards.json` 을 가리키지 않아서, 카드에 적힌 숫자가 canonical 인지 provisional 인지 retracted 인지 카드 안에서는 확인이 안 된다.

## 건드리면 안 되는 것
- **자기정정·철회 블록은 한 글자도 지우지 마라.** beta-gate.md §7-2("🔴 자기정정 — 내가 근거 없이 '문헌은 0.9·0.95 도 쓴다' 고 썼다 … 철회한다") · §7-8("⛔ 자기정정 — '그럼 셀을 키우면 되나'에 '그렇다'고 답하면 안 된다") · §7-8c(R2 철회) · bvse.md §10-2 의 두 [!warning](랩 아티팩트 · 봉우리 간격 2.9 → 1.5–2.4) · binder_adsorption 의 '우리가 저 논문을 비판한 바로 그 방식으로 우리가 틀렸다' · neb_intermediate_minimum 의 '⛔ 2026-09-01 정정' — 이게 이 repo 에서 제일 비싼 정보다. 정리한다고 뭉치면 왜 틀렸는지가 사라진다.
- **syntheses 의 Counter-arguments 절.** SCHEMA 가 '반론 보존 — 삭제 금지' 라고 명시한다. md_sampling_variance §5 의 `⛔ **이 절을 지우지 말 것.** 우리 쪽 대가를 적는 자리다` 는 그 자체가 규율문이다. 카드 내용을 고칠 때도 반론절은 건드리지 않는다.
- **msd_reading.md 전체(2026-09-07).** 1저자 질문 5개에 답하는 최신 판독 카드고, §5 예비 스캔·§6.5 기전 미확정·§8 '이 카드가 못 하는 것'까지 갖춰 이 폴더의 모범이다. 오히려 이걸 다른 카드의 틀로 삼아라.
- **bandgap.md §7(b2o3 CBM = B, 2026-09-07)** — §7.2 의 '이 분해는 엄밀하지 않다', §7.6 의 '허용/조건부/⛔ 금지' 3단 문구, l-분해 회수 사다리 3단계까지 있는 최신 절이다. 요약하거나 줄이지 마라.
- **법정 문구·인용 규율 문장.** xu2026 의 영문 cite_with 블록("Even if Li₃Nd were to form kinetically …"), why_so3h §0 의 리뷰어 대응 문장, sdcp_doped_closed 의 허용_서술/금지_서술 — 리뷰 왕복에서 합의된 축자 표현이라 다시 쓰면 합의가 깨진다. (xu2026 은 citable 상태 표기만 고치고 문안은 그대로 둔다.)
- **kb/physics/nd_4f_...md §1 교정 로그(C1~C7)와 260617 의 목차 구조.** 3월 개념노트 → 6월 실측으로 무엇이 유지되고 무엇이 교정됐는지 표로 남긴 것이라, '옛 문서를 지우지 않고 위에 교정을 얹는' 이 repo 의 표준례다. 두 카드를 합치거나 옛 주장을 삭제하지 마라 — 배수 5× → 5.8× 같은 개별 수치만 고친다.
- **questions 카드의 Evidence For / Evidence Against / 결정 실험 / Status Log 4절 구조.** lpsocl_low_beta 가 '이 카드가 미리 못 박은 기준: … 실측 β(MTO) = 0.70' 으로 선언한 기준에 스스로 걸린 기록이 남아 있다. status 를 강등하더라도 이 4절은 그대로 둔다.
- **db/properties/canonical_registry.json · citation_hazards.json 자체.** 이번 조사의 판정 근거가 전부 여기서 나왔다. kb 문서를 고칠 때 이 두 파일을 kb 쪽 서술에 맞추는 방향은 금물 — 원자료가 이긴다(registry `_history.2026-09-07-bh` 가 같은 취지).

## 발견

### [P0·wrong] md-beta-gate-still-live
- **어디**: `kb/concepts/md.md:86 · :150-164 (§4b·§4d)`
- **근거**: md.md 는 아직 β 표를 `| **0.8–1.2** | **확산 (게이트 통과)** |` 로, §4d 제목을 `### 4d. 게이트 판정 현황 (2026-08-04, 200 ps · 창 2–50 ps)` 로 두고 있다. 그런데 db/properties/citation_hazards.json 의 `HZ-beta-hard-gate` 는 level `SUPERSEDED` · what `β ≥ 0.80 하드게이트 — **판정으로 인용 금지**. β 는 경보로만` · forbidden_phrases `["β ≥ 0.80", "베타 하드게이트", "β 하드게이트"]` 다. md.md 는 2026-09-07 에 Haven 절을 넣으며 커밋됐는데(§6) β 절은 그대로 뒀다.
- **고치는 법**: §4b 표의 '게이트 통과' 판정 열을 빼고 D_inc plateau·창 안정성·홉 수(2026-08-30 도구 판정축)로 교체. §4d 판정현황표는 '2026-08-04 당시 기록'으로 접고 맨 위에 폐기 배너. 정본은 kb/concepts/beta-gate.md §7-8b·§7-8e 로 한 줄 링크.
- codex 필요: False

### [P0·wrong] md-ea-table-superseded-and-mixed
- **어디**: `kb/concepts/md.md:327 · :329`
- **근거**: 표에 `| LPSOCl (+O) | lpsocl | **0.271** | O 도핑, 장벽 상승 |`, 아래 줄에 `$E_a$ 순서: **modelc(0.224) < comp1(0.253) < +O(0.271)**`. db/properties/lpsocl_md_arrhenius.json 은 0.271 을 `_SUPERSEDED_mixed_seed_fit` 블록 안에 넣고 `_HEADLINE_PROMOTED_2026_07_27` 에 "CLAUDE.md: 멀티시드 판정만 — mixed-seed fit 인용 금지" 라고 적는다(현행 헤드라인은 0.2867). 게다가 0.224/0.253 은 registry 의 `MD_Ea_eV_singleseed`(group `md-ea-singleseed-anchor-v1`)이고 0.271 은 다른 group 이라 순위 자체가 group 을 넘나든다 — canonical_registry.json `_history.2026-08-07` 이 "단일시드(comp1 0.253 / modelc 0.224)와 4-seed(lpsocl 0.287)가 한 딕셔너리에 섞여 있던 것을 발견 ... group 을 나눠 분리했다" 로 registry 에서는 이미 고친 바로 그 버그다. 추가로 `HZ-cross-system-Ea`(BLOCKED, 2026-08-30)가 계간 Ea 직접 비교 자체를 막는다.
- **고치는 법**: 표를 registry 에서 읽은 값으로 교체(modelc 0.197 canonical / lpsocl 0.2867 provisional / b2o3 0.199 retracted / 단일시드 앵커는 별도 표), 순위 문장은 삭제하고 `HZ-cross-system-Ea` 인용. protocol_generation `gen0_pre_gate` 표기 병기.
- codex 필요: False

### [P0·wrong] beta-gate-procedure-contradicts-itself
- **어디**: `kb/concepts/beta-gate.md:616 (§12) vs :453 (§7-8e)`
- **근거**: §12 「실무 순서」 첫 두 줄이 `① β̄ 를 MTO 시드평균 곡선으로, 창 2–50 ps 에서 잰다` → `↓ β̄ ≥ 0.80 →  ✅ D 인용` 이다. 같은 파일 §7-8e 는 `**2026-08-30 이행**: 도구 판정축을 **`D_inc` plateau · 창 안정성 · 홉 수**로 교체. β 는 표에 남기되 판정에서 뺐다` 라고 적는다. 즉 사람이 실제로 따라 하는 절(§12)이 폐기된 문턱을 아직 발행한다 — §7-8e 스스로 진단한 "카드만 고치면 도구가 옛 판정을 계속 발행한다" 의 거울상이다.
- **고치는 법**: §12 를 D_inc plateau 기준으로 다시 쓰고 §1 표 위에 '⛔ 이 문턱은 2026-08-26 폐기 — §7-5 부터 읽으시오' 배너. 문서 순서를 뒤집어 폐기 판정(§7)을 §1 로 올리고 옛 doctrine 은 접힘.
- codex 필요: False

### [P0·wrong] bvse-90meV-forbidden-phrase
- **어디**: `kb/concepts/bvse.md:123 · :135 · :156 · :172`
- **근거**: 네 곳이 `MD Eₐ +90 meV`(123), `0.18 (Eₐ +90 meV 의 Boltzmann 항)`(135), `ΔEₐ 90 meV`(156), `MD 멀티시드 Eₐ +90 meV`(172) 로 쓴다. citation_hazards.json `HZ-cross-system-Ea` = level `BLOCKED`, forbidden_phrases `["90 meV", "+90 meV"]`, why "세 계(LPSOCl·modelc·b2o3)가 각자 다른 셀·다른 수렴상태다. 회신 AK(2026-08-30) Q2=C 판정: 세 계 Ea 직접 비교는 철회·보류". 같은 파일 :219-221 표는 `LPSCl1.6 | 0.228 | 0.197`·`B₂O₃@LPSCl1.6 | 0.281 | 0.199` 로 b2o3 0.199 도 쓰는데 registry 는 그 값이 `status: retracted`(2026-08-23 아레니우스 굽음)다.
- **고치는 법**: 네 곳의 +90 meV 를 '계간 Ea 비교는 HZ-cross-system-Ea 로 보류' 문구로 교체하고 D₀/Eₐ 분해 논지는 계 내부 서술로 좁힌다. §9·eV 보정판 표의 b2o3 0.199 에 retracted 표기.
- codex 필요: False

### [P0·wrong] physics-legacy-dos-gaps-live
- **어디**: `kb/physics/br_substitution_effects.md:48 · kb/physics/li_ordering_sensitivity.md:24`
- **근거**: br_substitution 은 `### Band Gap` 아래 `- 2.28 → 2.04 → 2.10 → 1.96 → 2.06 eV` 를 아무 표시 없이 적고, li_ordering 은 `| Band gap (eV) | 1.77 | 2.06 | -0.29 | 14% |` 를 적는다. db/properties/electronic.json 은 그 계열을 `"gap_range_SUPERSEDED_DOS_threshold": "1.77-2.28 eV"` 와 `"gap_range": "legacy DOS-threshold 1.77–2.28 eV (폐기). eigenvalue_gap_range 키 참조 — 두 계열을 섞지 말 것."` 로, 개별 항목마다 `"_DEPRECATED": "legacy DOS-threshold 판독. canonical = fixed-occ eigenvalue gap ... CLAUDE.md: DOS-threshold 판독 금지"` 로 못박는다. comp1 은 canonical 2.066 인데 이 카드는 2.28 이라고 말한다.
- **고치는 법**: 두 표에 `⛔ legacy DOS-threshold (폐기) — canonical 은 electronic.json eigenvalue_gap_range` 배너를 붙이고 comp1 2.066 / modelc 2.099 를 병기. comp2~comp5 는 'eigenvalue 재계산 미완'이라고 적는다(0 으로 채우지 않는다).
- codex 필요: False

### [P0·wrong] xu2026-neb-citable-claim-false
- **어디**: `kb/syntheses/xu2026_li_nd_rebuttal.md:6 (frontmatter status) · :46-47`
- **근거**: frontmatter status 가 `방어 중 — Li₃Nd c→c NEB **완료·인용 가능** (0.229 eV, CI, db 등록 2026-08-16)`, 본문은 "`db/properties/sei_neb.json` 의 `v2_ccpath/li3nd` (`citable: true`, 4개 루트 중 유일)" 이라고 쓴다. 실제 파일은 `"n_citable": 0, "retracted": true, "retraction_reason": "인용 가능한 결과가 0건이다. ... 이 파일의 어떤 값도 인용하지 말 것."` 이고, `results["v2_ccpath/li3nd"]` 의 `"citable": false` 다. citation_hazards 도 `db/properties/sei_neb.json | BLOCKED | 전량 철회 (retracted=true, n_citable=0)`. 미결 작업 #8 ("kgy 에서 collect_neb --merge 실행 → sei_neb.json 커밋")이 아직 pending 이라 병합이 안 됐다.
- **고치는 법**: status·본문을 'NEB 계산은 끝났으나 sei_neb.json 병합 전이라 ledger 상 citable:false — merge 후 인용 개방' 으로 정정. 0.229 를 쓰는 인용 문안(:78-82)에도 같은 단서.
- codex 필요: False

### [P0·wrong] sampling-defense-defends-retired-gate
- **어디**: `kb/syntheses/md_sampling_variance_defense_2026_08_25.md:2 (title) · :83 · :104`
- **근거**: 리뷰어 대응용 방어 카드인데 §4 표가 `| 확산영역 β 게이트 | 대개 미보고 | **필수** (β<0.8 = 케이지) |` 이고 §6 「원고에 쓸 문장」이 "우리가 3시드·200 ps·확산영역 게이트를 쓰는 이유는…" 이다. 그 게이트는 이 카드 **다음 날**(2026-08-26, beta-gate.md §7-5) 폐기됐고 `HZ-beta-hard-gate`(SUPERSEDED)로 등재됐다. 같은 파일 :104 `**절대값은 여전히 못 쓴다**: MLIP overshoot(≈3–5×) + Haven=1 가정(≈2×)` 두 항목도 kb/concepts/md.md §6(2026-09-07)이 각각 철회했다 — "*\"UMA 가 D 를 3–5× 과대\"* 라는 종전 서술은 … 그 비교 안에 위 두 오염이 섞여 있다", "Haven 보정은 19 % 다", "'상한' 의 근거로 Haven 을 대면 안 된다".
- **고치는 법**: 제목·§4·§6 의 β 게이트를 '멀티시드 + D_inc plateau + 고정 창'으로 교체. :104 를 실측 H_R 0.84(±0.06, 1.19×)와 '서로 반대인 보정 둘이라 순 방향 미정' 으로 갈아끼우고 db/properties/haven_ratio_measured_2026_09_07.json 인용. 원고에 나가는 카드라 우선순위가 높다.
- codex 필요: False

### [P1·stale] sdcp-cards-status-vs-ratified-closure
- **어디**: `kb/questions/sdcp_doped_estimand_2026_08_28.md (status: active) · sdcp_doped_reopen_v2_2026_08_28.md (answered) · sdcp_doped_reopen_v3_2026_08_28.md (active) · sdcp_site_preference.md (active)`
- **근거**: 본문은 이미 사형선고다 — v1 은 "## 🔴 회신 O 판정 (2026-08-28) — **P0 전면 반려. 슬랩 NO-GO.**", v2 는 제목이 "⛔SUPERSEDED (회신 R NO-GO)", v3 은 "R4 대기". 그런데 frontmatter status 는 active/answered 라 kb/index.md 에도 `[active]`·`[answered]` 로 뜬다. 캠페인 자체는 `db/properties/sdcp_doped_closed_2026_08_28.json` (상태 `**active** — 1저자 재승인 2026-08-28`, `D-2026-08-28-sdcp-doped-scope-closure`)로 닫혔고 kb/open_items.md:879 도 "neutral·doped 둘 다 마감이고 남은 것은 **재개 조건뿐**" 이라 적는다. v3 은 :24 heading 이 아직 "R3 대기" 인데 :53 이 "R3 판정 … R4 대기" 라 한 문서 안에서도 갈린다.
- **고치는 법**: v1·v2 status 를 abandoned/superseded 로, v3 을 `status: blocked-on-R4`, site_preference 를 closed-scope 로. 네 카드 frontmatter 전부에 `feedsInto: db/properties/sdcp_doped_closed_2026_08_28.json` 를 넣어 마감 문서로 한 번에 가게 한다. v3 :24 heading 정정.
- codex 필요: False

### [P1·ia] questions-folder-no-longer-tracks-live-questions
- **어디**: `kb/questions/ (11편, 최신 2026-09-06) vs db/governance/decisions.json (2026-09-04~08 active 6건)`
- **근거**: decisions.json 최근 6건 — `D-2026-09-04-lpsocl-box331-400ps-uniform`, `D-2026-09-07-b2o3-md-closure-retrospective`, `D-2026-09-07-b2o3-cell-expansion-diagnostic`, `D-2026-09-08-b2o3-uma-vs-dft-force`, `D-2026-09-08-lpsocl-box331-closure-conditions`, `D-2026-09-08-cascade-d-rel-estimand` — 전부 active 인데 kb/questions 에 대응 카드가 하나도 없다. cascade 보고량 카드는 kb/methodology/cascade_lessons_transfer_2026_09_08.md 에, LPSOCl 닫힘 조건은 db/properties/lpsocl_box331_closure_conditions_2026_09_07.json 에 흩어져 있고, 그 json 을 참조하는 kb 문서는 `kb/projects/restart_runbook_2026_09_07.md` · `kb/concepts/msd_reading.md` 둘뿐이다. 반면 questions/ 11편 중 7편이 2026-08-28~31 SDCP 동결본이다.
- **고치는 법**: kb/questions 를 '살아있는 보고량·미결' 로 되돌린다: decisions.json 의 active 결정마다 얇은 카드 1장(질문 1문장 + feedsInto: 결정 ID + Status Log)만 만들고, SDCP 7편은 `kb/questions/archive/` 또는 status 강등으로 접는다. 카드↔결정 ID 를 lint 로 대조.
- codex 필요: False

### [P1·missing] nd-anneal-no-interpretation-card
- **어디**: `kb/physics/ (해당 카드 없음) — 원자료 db/structures/.../anneal_2026_09_07/anneal_results.json (커밋 83c868a97, 2026-09-08)`
- **근거**: 커밋 83c868a97 "Nd2O3-LPSCl1.6 어닐 6셀 회수 — UMA 500 K 20 ps + relax (순위: distributed < free_s < bo4)" 와 51b5dec21 "--from_xyz: 완화 구조 → scf 단일점 (Nd O-모티프 UMA 순위 DFT 재채점, 4셀)" 가 Nd O 자리(speciation) 순위를 새로 만들었다. `grep -rln "O-bo4\|free_s\|anneal_2026_09_07" kb/` 는 kb/methodology/cascade_lessons_transfer_2026_09_08.md 한 줄(`⑤ MLIP 순위는 DFT 재채점 전엔 값이 아니다 | Nd O-모티프 4셀`)만 잡는다. 정작 O speciation 을 다루는 kb/physics/nd_4f_...md §C2("O가 PS₄(16e)에 실제 치환됨 검증")와 kb/physics/260617_...md §8("실제 구조 팩트체크 (O speciation, Nd 자리)")는 이 결과를 모른다.
- **고치는 법**: kb/physics 에 O-모티프 순위 카드 1장(UMA 순위 + ⛔ DFT 재채점 전 값 인용 금지 + 시드 1개·셀 고정 한계). 기존 Nd 카드 두 편의 O speciation 절에서 상호참조.
- codex 필요: False

### [P1·wrong] descriptor-catalog-sei-gaps-guessed-wrong
- **어디**: `kb/descriptors/coating_descriptor_catalog.md:440-455 (§8 SEI 산물 catalog)`
- **근거**: 표의 `E_g (예상)` 열이 전부 추정치다 — `| Li₃P | 가능 | ~3 eV | 매우 높음 (Li-rich) | ★ Li 전도 좋음 |`, `| Li₂O | ~7 eV |`, `| LiCl | ~10 eV |`, `| Nd₂S₃ | ~2 eV |`. kb/physics/nd_4f_...md §C5 는 같은 상들을 MP 표준값으로 통일해 놓았다: `LiCl 6.65 · Li₃PO₄ 5.73 · Li₂O 5.24 · Li₂S 3.90 · **Li₃P 0.70**`. Li₃P 가 ~3 이 아니라 0.70 인 것은 사소하지 않다 — kb/syntheses/nd_doping_two_axis_verdict.md:49 의 논지(`**Nd₂S₃** | **0.770** | **좁은 갭 — Li₃P(0.709) 옆자리**`)가 통째로 그 값에 걸려 있다. 카탈로그는 그 상을 '★ 전도 좋음' 이라 칭찬한다.
- **고치는 법**: §8 표를 nd_4f §C5 / db/properties/sei_electronic.json 실측·MP 값으로 교체하고 '예상' 열은 삭제. 최소한 표 전체를 '2026-06 추정 — 실측으로 대체됨' 으로 접는다.
- codex 필요: False

### [P1·useless] descriptor-catalog-phantom-scripts
- **어디**: `kb/descriptors/coating_descriptor_catalog.md:102 · :527-532`
- **근거**: :102 `자세한 건 \`scripts/descriptors/elastic.py\` (구현 예정)`, :527 `\`scripts/descriptors/\` 에 다음 구현 예정:` 아래 `compute_tier1_descriptors.py · compute_elastic.py · compute_neb_barrier.py · compute_surface_gamma.py · compute_madelung.py` 5개. 실제로는 `scripts/` 아래에 `adhesion / automation / doping / heckel_analysis.py / make_heckel_manifest.py / oat_sensitivity.py` 뿐이고 `scripts/descriptors/` 자체가 없다 — 3개월째다. 덤으로 `scripts/adhesion/bond_density_36reg_FAST.py` 와 `tools/adhesion_v30u/bond_density_36reg_FAST.py` 가 같은 파일로 두 곳에 있다(CLAUDE.md 코드 규율의 '중복이 진짜 위험').
- **고치는 법**: '다음 단계' 절 삭제 또는 kb/open_items 로 이관. §2 의 `Band gap (Eg) | DFT DOS | VASP/QE (HSE06)` 행도 같이 고친다 — DOS 판독은 CLAUDE.md 금지 항목이고, §3 의 `Ionic conductivity (σ) | NEB + Arrhenius | NEB → KMC` 도 현행 MLIP-MD 규약과 다르다.
- codex 필요: False

### [P1·wrong] neb-hbn-7meV-number-cited
- **어디**: `kb/concepts/neb.md:117 · :121`
- **근거**: :117 `| hBN 표면 | **~0.007** | near-flat, 거의 무장벽 표면 확산 |`, :121 `- **hBN 표면 ~0.007 eV**: 사실상 평탄`. citation_hazards.json: `db/properties/vgcf_hbn_neb.json | CONDITIONAL | 표면 확산 배리어 7 meV | why: 수치 분해능(20–46 meV) **아래**다 | fix: '< 0.01 eV, 사실상 barrierless' 로만 서술 — **숫자로 인용 금지**`.
- **고치는 법**: 두 줄의 0.007 을 '< 0.01 eV (분해능 20–46 meV 아래 — 사실상 barrierless)' 로 교체.
- codex 필요: False

### [P1·stale] elastic-comp2-remeasuring-but-registered
- **어디**: `kb/concepts/elastic.md:137-138`
- **근거**: :137 `**comp1 ↔ comp2만** 같은 cubic-52 조건의 완전 비교쌍 (comp2는 현재 USPP·k444로 재측정 중)`, :138 `**Br 치환은 결합을 약화**시켜 **comp2 < comp1** 예상`. canonical_registry.json 은 `E_VRH_GPa | comp2 | 20.03 | canonical | elastic-dft-relaxedion-comp1comp2-v1` 로 comp1 22.06 과 **같은 comparison_group** 에 이미 등재해 뒀다. 즉 '예상'이 아니라 실측이고(20.03 < 22.06), 표(:130-134)는 comp2 행을 아예 빼 놓았다.
- **고치는 법**: 표에 comp2 20.03 canonical 행 추가, '재측정 중'·'예상' 삭제, ICOHP 정합 문장은 사후 확인으로 다시 쓴다.
- codex 필요: False

### [P1·broken] bandgap-esw-pointer-dead
- **어디**: `kb/concepts/bandgap.md:119`
- **근거**: `band-edge는 분해창을 2–3× 과대평가한다(Schwietert 2020; …). → \`kb/concepts/esw\` 계열 문서 참조.` — kb/concepts/ 에 esw 로 시작하는 파일이 없다. 실제 ESW 개념 문서는 `kb/methodology/esw_grandpotential_staircase_explained.md` 와 `kb/concepts/oxidation_vs_mechanical.md` §1 두 곳에 있다. 개념 문서가 methodology/ 에 앉아 있는 것 자체가 SCHEMA 의 디렉터리↔타입 대응(concepts=개념)과 어긋난다.
- **고치는 법**: 포인터를 `kb/concepts/oxidation_vs_mechanical.md` §1 + `kb/methodology/esw_grandpotential_staircase_explained.md` 로 고치고, 후자를 kb/concepts/esw.md 로 옮기는 것을 v3 재편 때 검토.
- codex 필요: False

### [P1·broken] webapp-only-links-unfollowable
- **어디**: `kb/concepts/dft.md:254-255 · bvse.md:368 · md.md:336 · neb.md:129 · beta-gate.md:164 · neb_intermediate_minimum.md:25`
- **근거**: 여섯 곳이 `**[DFT](/concept/dft) §12**`, `**[β 게이트](/concept/beta-gate)**` 같은 **웹앱 절대경로**로 링크하고, neb_intermediate_minimum 은 이미지를 `![Li2S / Li3Nd 이동 경로](/api/file/docs/figures/sei_neb_paths.png)` 로 건다. webapp/app.py:1201 `@app.route("/concept/<cid>")` 가 있으니 브라우저에서는 열리지만, repo 에서 파일을 직접 읽는 사람·LLM 에게는 죽은 링크고 SCHEMA 의 lint 경로검사도 절대경로라 건너뛴다. 같은 repo 안에서 repo-상대경로와 웹앱 라우트 두 관례가 섞여 있다.
- **고치는 법**: 본문 링크는 `kb/concepts/dft.md` 형식으로 통일(웹앱은 렌더 시 라우트로 바꾸면 된다). 이미지도 `docs/figures/sei_neb_paths.png` 상대경로로.
- codex 필요: False

### [P1·stale] dft-12-4-beta-gate-mandatory
- **어디**: `kb/concepts/dft.md:249 · :252`
- **근거**: :249 `| **MLIP-MD** | **$E_a$·$D$·조성 순위 = 정본.** β 게이트 + 멀티시드 오차막대 필수 |`, :252 `… 게이트 탈락 점은 적합에서 제외.` 둘 다 폐기된 하드게이트를 전제한다(`HZ-beta-hard-gate`). 이 절(§12)은 dft.md 안에서 가장 자주 참조되는 곳이다 — bvse.md:368 · md.md:336 · neb.md:129 이 전부 여기를 가리킨다.
- **고치는 법**: β 게이트를 D_inc plateau·창 안정성·홉 수로 교체. 세 문서가 이 절을 참조하므로 한 곳만 고치면 전파된다.
- codex 필요: False

### [P1·duplicate] beta-gate-md-duplicated-and-diverged
- **어디**: `kb/concepts/md.md:77-167 (§4b·4b-2·4b-3·4c·4d) ≒ kb/concepts/beta-gate.md:19-133 (§1-§5)`
- **근거**: β 정의 표, R² 반례(`LPSOCl 600 K: R² 0.975인데 β 0.61`), n_hop 표(`≥ 10 / 3–10 / < 3`), 600 K 예측·실측 표(`LPSCl1.6 13.9 0.87 / LPSOCl1.6 8.4 0.61 / B₂O₃ 13.9 0.81`), 적합 규율 3건, 게이트 판정현황표가 **양쪽에 거의 축자 중복**이다. 그런데 beta-gate.md 만 §7~§12 로 폐기·정정을 받았고 md.md 사본은 2026-08-04 판 그대로다 — 복사본이 갈라지면서 md.md 가 폐기 이전 판정을 계속 발행한다. 같은 패턴이 msd_reading.md 와도 있다(§3 이 md.md §4 를 다시 설명).
- **고치는 법**: md.md 의 β 절을 3~5줄 요약 + `kb/concepts/beta-gate.md` 링크로 축약(중복 90줄 제거). CLAUDE.md 코드 규율의 '물리 규약 복사본' 검사(tools/convention_check.py)를 kb 문서에도 확장 검토.
- codex 필요: False

### [P1·ia] index-alphabetical-no-recency
- **어디**: `kb/index.md:7-28 (concepts 13 · physics 6) · :329-336 (syntheses 6)`
- **근거**: 생성기가 폴더별 **가나다순**으로만 찍고 날짜도 status 도 안 넣는다(questions 만 `[open]`/`[active]`, 그리고 `○미열람` 배지). 그래서 `- \`kb/physics/br_substitution_effects.md\` — Br Substitution Effects on Argyrodite Mechanical Properties`(2026-06-11, 폐기 갭 인용)와 `- \`kb/physics/nd_4f_doping_consolidated_corrected_2026_06_24.md\``(2026-09-03 교정본)가 구분 없이 나란하다. 조사 목표인 '최신·중요한 것이 앞, 옛것은 접힘' 과 정반대다.
- **고치는 법**: tools/kb_wiki.py index 에 `updated`(없으면 git 마지막 커밋일) 표시 + 최신순 정렬 + `status`/`verificationStatus` 배지 추가. 90일 이상 손 안 댄 legacy 는 접힘 블록으로.
- codex 필요: False

### [P2·ia] physics-legacy-no-frontmatter-no-sources
- **어디**: `kb/physics/{br_substitution_effects,li_ordering_sensitivity,vacancy_effects,vacancy_mechanism_corrected_2026_05_08}.md · kb/descriptors/coating_descriptor_catalog.md`
- **근거**: 다섯 편 모두 frontmatter 가 없어 lint 의 깊이 검사(`문서 365개 (frontmatter 180 · 레거시 185 — 소급 없음)`)를 통째로 비껴간다. br_substitution·li_ordering·vacancy_effects 는 **db/ 경로를 한 개도 인용하지 않는다** — SCHEMA 「문서마다 관련 경로 2개 이상을 인용한다」 미충족. 그래서 `- Li₆ average: ~26 GPa / Li₅.₄ average: ~21 GPa`, `γ_SE ≈ 1.2 / 0.5 J/m²`, `comp5 … C44 39.9 vs 27.2` 같은 값이 어디서 왔는지 문서 안에서 추적 불가다(B0 는 registry 26.233/21.71 과 일치하지만 확인은 밖에서 해야 했다).
- **고치는 법**: legacy 소급은 안 한다는 규율은 지키되, 이 다섯 편에는 최소 frontmatter(date/updated/status/verificationStatus)와 출처 경로 2줄만 얹는다. 아니면 `kb/physics/legacy/` 로 옮겨 접는다.
- codex 필요: False

### [P2·stale] frontmatter-updated-behind-git
- **어디**: `kb/questions/li3nd_pristine_reconstruction_2026_09_02.md:4 · sdcp_site_preference.md · lpsocl_low_beta_mechanism.md · xu2026_li_nd_rebuttal.md · sdcp_self_doping_explainer_2026_08_26.md`
- **근거**: `updated:` 가 마지막 커밋일보다 이르다 — li3nd 2026-09-02 vs git 09-06(본문에 `⚠⚠ **2026-09-06 정정**` 블록이 있는데 Status Log 에는 09-02 항목만 있다), sdcp_site_preference 08-11 vs 08-28, lpsocl_low_beta 08-12 vs 08-17, xu2026 08-13 vs 08-16, sdcp_self_doping 08-26 vs 08-28. SCHEMA: `updated: YYYY-MM-DD  # 마지막 실질 수정 (고치면 bump)`. 반대 방향도 하나 — polaron_seed 는 updated 09-06 인데 마지막 커밋이 09-05 다.
- **고치는 법**: 다섯 건 bump. 그리고 lint 에 'updated < 마지막 커밋일' 경고를 추가하면 기계로 잡힌다(지금 lint 는 이 축을 안 본다).
- codex 필요: False

### [P2·broken] binder-card-duplicate-yaml-key
- **어디**: `kb/syntheses/binder_adsorption_charge_state_2026_08_29.md:9 · :11`
- **근거**: frontmatter 에 `verifiedAt: 2026-08-29` 가 9행과 11행 두 번 나온다(사이에 `verifiedBy:` 가 끼어 있다). YAML 중복 키라 파서에 따라 조용히 하나가 버려진다. lint 는 0 errors 로 통과했다 — 중복 키를 안 본다.
- **고치는 법**: 11행 삭제. tools/kb_wiki.py lint 에 중복 키 검사 추가(다른 문서에도 있을 수 있다).
- codex 필요: False

### [P2·stale] 1600ps-still-in-progress
- **어디**: `kb/concepts/beta-gate.md:101 · kb/concepts/md.md:146-147`
- **근거**: 두 곳 모두 `comp1 600 K 를 200 → **1600 ps** 로 늘리는 게 정확히 이 검사다 (진행 중)` 라고 적는데, 같은 beta-gate.md §11-1(:557-563)이 결과를 이미 싣는다: `| 600 K | 0.64 | **0.37** | −31 % |` 와 `**600 K 가 더 나빠졌다.**`. 한 문서 안에서 '진행 중'과 '결과'가 공존한다.
- **고치는 법**: 두 곳을 '완료 — §11-1 참조, 시간 연장은 처방이 아니었다' 로 교체.
- codex 필요: False

### [P2·duplicate] nds4-size-multiplier-two-values
- **어디**: `kb/physics/260617_Nd2O3_doping_bandgap_narrowing_mechanism.md:214 vs kb/physics/nd_4f_doping_consolidated_corrected_2026_06_24.md §2-6`
- **근거**: 260617 의 **원고용 SI 문장**이 `Placing Nd on the P site (NdS₄) is chemically unfavorable (≈5× cation-size mismatch; +1–3 eV/Nd)` 이다. nd_4f 는 2026-09-03 에 같은 논증을 고쳤다: `Shannon(4배위) **P⁵⁺ 0.17 ≪ Nd³⁺ 0.98 Å** … (**5.8× 큼**)` + `⚠ **2026-09-03 정정**: 여기 적혀 있던 \`0.38 Å\` 은 Shannon 표에 없는 값이었다 … **옛 배수를 원고에 인용하지 말 것** (⚠ 비교는 같은 척도끼리만: crystal 끼리면 … 3.6×)`. 같은 주장이 두 카드에 있고 배수가 다르며, 260617 은 정정을 모른다.
- **고치는 법**: 260617 :214 의 ≈5× 를 5.8×(effective, 같은 척도 명시)로 고치고 nd_4f §2-6 상호참조 한 줄. 장기적으로 NdS₄ 불가 논증은 한 카드에만 두고 나머지는 링크.
- codex 필요: False

### [P2·buried] esw-reduction-limit-question-buried
- **어디**: `kb/questions/esw_reduction_limit_field_2026_08_28.md (status: open, 11일)`
- **근거**: 카드는 `reduction_limit = max(s["V_vs_Li"] for s in pos)  # ← 1.24` 가 문헌의 환원한계(Zhu 2015 1.71 / Wang 2026 1.78)가 아니라 breakpoint 하나 아래를 집는다는 것을 소스까지 확인해 놓고 `⛔ **사람 승인 대기**: 필드 이름/분할을 바꾸는 것은 cascade 하류 전체에 걸리므로 1저자 판단 없이 손대지 않는다` 로 멈춰 있다. 그 사이 `tools/oxidation/esw_grand_potential.py` 는 2026-08-28 이후 **네 번** 커밋됐다(230a222e8·77a4adf03·c648e7e4f·e3735dd56, 마지막은 09-07 O₂ landmark). 정본 필드 의미가 미결인 채 그 파일만 계속 고쳤다.
- **고치는 법**: 1저자 결정 1건(필드 3분할: reduction_onset_V / last_reduction_step_V / ocv_self_decomposition_V)을 받아 닫는다. 그 전까지 `tools/oxidation/esw_grand_potential.py` 상단 docstring 과 db/properties/oxidation_stability.json 에 '이 필드는 미결' 표시를 걸어 파일을 여는 사람이 보게 한다.
- codex 필요: False

### [P1·ia] beta-gate-doc-shape
- **어디**: `kb/concepts/beta-gate.md (629줄, §1→§12 연대순 append)`
- **근거**: 문서가 시간순으로 쌓여서 **옛 판정이 위, 현행 판정이 아래**다. §1-§6 = 2026-08-04 하드게이트 doctrine, §7-5(:230) 폐기, §7-8b(:338) 회신 F, §7-8e(:436) 도구 반영, §12(:612) 실무 순서(아직 옛 판). 폐기 사실을 알려면 265줄을 내려가야 하고, 실무 절차를 보려면 다시 350줄을 더 내려가 옛 판을 만난다. 같은 형태가 kb/concepts/md.md(§6 Haven 정정이 인용 규율 안 [!warning] 블록 안에 중첩)에도 있다.
- **고치는 법**: 카드 맨 위에 '현재 판정 3줄' 상자(β 는 경보, 판정축은 D_inc plateau·창 안정성·홉 수, 근거 §7-8b/§7-8e)를 두고 §1-§6 을 '2026-08 이전 판정 이력' 으로 접는다. 새 개념 카드 공통 규약으로: **현행 판정 → 근거 → 이력** 순서.
- codex 필요: False
