# repo — kb/results (94개 결과 카드)

## 지금 무엇인가
우리가 낸 계산 결과를 사람이 읽는 산문으로 해석해 둔 카드 94장이고, 웹앱 /log 의 "Session Handoffs" 가 이 폴더만 통째로 읽어 `/api/handoff/<파일명>` 으로 띄운다. 실제로는 결과 해석(b2o3·comp1/modelc·sdcp·nd·adhesion) 말고도 세션 타임로그·발표대본·figure plan·litdb 인덱스가 섞여 있어서 "결과 카드"라는 이름이 내용을 안 덮는다. 이번에 94장 전부의 머리(제목+출처줄)와 frontmatter 가 있는 24장의 frontmatter 를 다 봤고, 그중 22장을 본문까지 읽었다 — 나머지 72장은 본문을 안 읽었으니 "전수 검증했다"고 읽지 마라.

## 처음 오는 사람
웹앱 /log 로 들어오면 "Session Handoffs · kb/results (94)" 아래에 카드 94개가 3열 격자로 깔린다. 이름은 파일명에서 밑줄만 공백으로 바꾼 것("b2o3 md 600K multiseed 2026 07 02")이고, 정렬은 날짜가 아니라 **파일명 역알파벳**이라 맨 앞에 vgcf·uma·slide 가 오고 제일 최근 것(branch_state_2026_08_31)은 중간에 파묻힌다. 날짜·상태·살았나 죽었나 표시가 하나도 없어서, 처음 온 사람이 "지금 유효한 결론이 뭐냐"를 알려면 94장을 하나씩 눌러 보는 수밖에 없다. 그리고 눌러서 나오는 것 중 상당수가 이미 철회된 값을 굵은 글씨로 "최종"이라고 말한다 — 그게 제일 위험한 지점이다. repo 쪽으로 들어와도 kb/results 에 README 도 index 카드도 없고, kb/index.md 의 results 절은 94줄 알파벳 나열이라 사정이 같다.

## 건드리면 안 되는 것
- **철회 배너가 이미 달린 카드의 본문** — b2o3_vs_lpscl16_md_2026_07_02.md · b2o3_bvse_channel_2026_07_02.md · b2o3_anode_interface_MD_dynamics_2026_07_06.md. kb/SCHEMA.md 의 Update Policy 가 '철회는 원문 보존 + 반증 병기' 다. 배너를 갱신하는 건 되지만 아래 본문(σ 1.33× 서사, 6× 억제 예비 결과)을 지우면 왜 틀렸는지가 사라진다.
- **b2o3_arrhenius_curvature_2026_08_23.md 전체** — kb/results 에서 유일하게 인공물 가설 3개를 각각 반증하고, 자기 정정(2026-09-07 두 건)을 취소선이 아니라 명시로 남기고, '이 카드가 못 하는 것' 절까지 가진 문서다. 나머지 93장을 이 형식에 맞추는 게 목표지 이 카드를 줄이는 게 아니다.
- **음성 결과 카드 5장** — single_li_neb_invalid_argyrodite_2026_08_21.md(무질서계 단일 Li NEB 불성립) · sdcp_slab_plateau_broken_2026_08_03.md · md_beta_estimator_disagreement_2026_08_25.md(MTO/STO 가 순위를 뒤집음) · champion_pool_size_bias_2026_08_18.md(best-of-N 편향) · halogen_wad_refutation.md(저자 mechanism 3가정 반박). 다시 유도하는 데 제일 비싼 지식이고, 없으면 같은 계산을 또 던진다.
- **adhesion 9장 전부**(v5 · v9~v22 · v23~v25 · v26 · 100seeds · final · methodology_detail · troubleshooting). 2026-04~05 paper #2 캠페인의 유일한 방법 반복 기록이다. 낡았다고 지우면 v15 Cl-O descriptor(R=−0.91)가 어떤 6개 방법 변형을 견뎠는지가 통째로 없어진다. 아카이브 표시만 붙이고 접어라.
- **doping_273_qa_log.md** — 273 cascade 완주분의 QA 판정 원장이고 기계 경로(`/data/work/runs/multi_category_2026_05_26_v23`)를 담고 있다. 산문처럼 보여도 원장이라 요약하거나 재작성하면 안 된다.
- **sdcp_wave1_citable_2026_08_25.md** — '논문에 쓰는 값 한 장'. 원자료 총에너지에서 재유도(손 전사 0)했다고 verifiedBy 에 적혀 있다. 이 카드는 손대지 말고, 다른 sdcp 카드들이 여기를 가리키게 만들어라.
- **카드 안의 `<!-- ⛔ 2026-08-26 정정 -->` 같은 인라인 정정 주석**(예: sdcp_master_summary_2026_07_16.md:29-33 의 조성 오기 정정). 잘못된 원문과 정정을 같이 보여 주는 형식이라 정리한답시고 원문 줄만 고쳐 쓰면 '무엇을 틀렸었나'가 없어진다.
- **db/properties/*_closed_*.json · citation_hazards.json · canonical_registry.json 은 정본이다.** 이번 조사에서 나온 수정은 전부 kb/results 쪽(산문)에서 하고, 결속을 넓히는 변경만 db 쪽 `id`/`forbidden_phrases` 추가로 한다 — 기존 필드명(`kind: estimand`, `canary_geometry` 등 기계 경로)은 CLAUDE.md 대로 건드리지 않는다.

## 발견

### [P0·wrong] sigma-x4-cross-comp-unbound
- **어디**: `kb/results/MASTER_structure_property_logic_2026_06_21.md:25,28,71 · kb/results/ionic_conductivity_full_explained_2026_06_21.md:13,55-59 · kb/results/ionic_conductivity_synthesis_comp1_modelc.md:3 · kb/results/deck_ionic_section_additions.md:28,34 · kb/results/lpscl_vs_lpscl16_v3_comparison.md:313`
- **근거**: db/properties/canonical_registry.json 의 comp1 앵커는 `"metric":"MD_Ea_eV_singleseed","value":0.2532,"n_seed":1,"status":"provisional"` 이고 `prohibitions` 에 **`absolute_sigma`, `cross_composition_ranking`, `cite_until_beta_gate_passes`** 가 명시돼 있다. 그런데 MASTER:71 은 `| σ₃₀₀ (mS/cm) | ~3.4 | ~14 | **×4** | AIMD+NE |`, ionic_full:13 은 `σ_Li ~4배 (3.35 → 13.96 mS/cm, AIMD-MLIP)`, ionic_synthesis:3 은 `Headline: σ(LPSCl1.6) ≈ 4× σ(LPSCl)` 로 **절대 σ와 조성간 순위를 둘 다** 헤드라인으로 쓴다. 결속도 안 걸린다 — `webapp/canonical.py:bound_claims()` 는 `status=="retracted"` 또는 `citable is False` 만 claim 으로 내보내는데 comp1 앵커는 `provisional`+`prohibitions` 라서 목록에 안 든다. 실제로 렌더해 보니 MASTER·ionic_full·ionic_synthesis 모두 `claim-flag` **0개**다.
- **고치는 법**: canonical_registry 에 `MD_sigma_ratio_300K@modelc_vs_comp1` 을 `citable:false`(사유: 단일시드·cross_composition_ranking 금지)로 신설하고, `bound_claims()` 가 `prohibitions` 에 `absolute_sigma`/`cross_composition_ranking` 이 있는 항목도 claim 으로 내보내게 조건을 넓혀라. 그러면 이 다섯 장이 렌더에서 자동으로 결속된다. 카드 본문은 지우지 말고 각 헤드라인 위에 한 줄 배너("이 비는 단일시드 · 조성간 순위 금지")만 얹는다.
- codex 필요: False

### [P0·wrong] b2o3-ea-0206-unbound
- **어디**: `kb/results/b2o3_md_600K_multiseed_2026_07_02.md:1,6,21,27`
- **근거**: 카드 제목이 `# B₂O₃ MD 이온전도도 — 600K 다중시드 error bar (Ea = 0.21 ± 0.03 eV)` 이고 본문 27행이 `**Ea = 0.21 ± 0.03 eV** 를 논문값으로.` 다. db/properties/b2o3_md_arrhenius.json 은 같은 값을 `Ea_eV_PAPER_SUPERSEDED_600K_only = 0.206 (+0.038/-0.030)` 로 두고, `⛔_RETRACTED_2026_08_23.what` 이 **"0.206 ... 및 ... 0.199 ± 0.034 까지 셋 다 철회한다"** 라고 이름을 대서 철회했다. 그런데 결속되는 문자열은 `0.199` 하나뿐이라(`bound_claims()` 실측 4건) 이 카드는 렌더에서 `claim-flag` **0개**로 나온다 — 즉 화면에서 철회 표시 없이 "논문값"이라고 말한다.
- **고치는 법**: canonical_registry 의 `MD_Ea_eV@b2o3` 철회 블록에 대체 문자열 목록(`0.206`, `0.21 ± 0.03`, `0.2234`, `0.223`)을 추가하거나 citation_hazards 에 `id: HZ-b2o3-single-Ea` + `forbidden_phrases` 로 넣어 같은 스캐너에 태워라. 카드 맨 위에는 b2o3_vs_lpscl16_md 와 같은 형식의 SUPERSEDED 배너를 달고 kb/methodology/md_axis_status_2026_09_07.md 를 가리킨다.
- codex 필요: False

### [P0·stale] b2o3-md-axis-retired-not-reflected
- **어디**: `kb/results/b2o3_champion_status_2026_07_03.md:15 · kb/results/b2o3_SEMIFINAL_report_2026_07_09.md:13,24,48,216 · kb/results/b2o3_anode_interface_campaign_2026_07_07.md:61 · kb/results/b2o3_anode_interface_MD_dynamics_2026_07_06.md:41`
- **근거**: db/properties/b2o3_md_arrhenius.json 의 `⛔⛔_MD_AXIS_RETIRED_2026_08_25.what` = **"b2o3 의 UMA-MD 전도도 축 전체를 인용 불가로 내린다 (D · Ea · σ · 구간 Ea 전부)"**, `still_usable` = "0 K DFT 축만". 이 마감은 db/properties/b2o3_md_closed_retrospective_2026_08_25.json 으로 2026-09-07 07:32Z 에 1저자 비준까지 끝났다. 그런데 champion_status:15 는 아직 `| 이온 | MD σ / Ea | ✅ **최종** (3-seed×3-T 완전대칭) | **Ea 0.199±0.034** ...` 이고, SEMIFINAL:24 는 `| Ea (MD, 3-seed×3-T) | 0.197±0.032 eV | 0.199±0.034 eV | **동등** ✅ |` 다. kb/results 94장 중 축 은퇴를 언급한 카드는 b2o3_arrhenius_curvature_2026_08_23.md **한 장뿐**이다(grep `MD_AXIS_RETIRED|축 은퇴|md_axis_status` 결과).
- **고치는 법**: b2o3 MD 를 말하는 6장(champion_status·SEMIFINAL·md_600K_multiseed·vs_lpscl16_md·bvse_channel·anode_interface_MD_dynamics) 머리에 같은 문안의 배너를 달고 전부 kb/methodology/md_axis_status_2026_09_07.md + db/properties/b2o3_md_closed_retrospective_2026_08_25.json 로 보낸다. 표의 ✅ 는 ⛔ 로 바꾸되 값은 지우지 않는다(SCHEMA: 원문 보존 + 반증 병기).
- codex 필요: False

### [P0·wrong] sdcp-dE-extract-0336-unbound
- **어디**: `kb/results/sdcp_ptfe_site_screen_summary_2026_08_11.md:58`
- **근거**: 카드 본문: `뽑아 올린 끝점이고, VASP+U 가 \`dE_extract = +0.336 eV\`(불리)로 이미 반증한 과정이다.` 인데 db/properties/citation_hazards.json 의 sdcp_phaseB_dftu_v1 항목은 level BLOCKED 에 **"⛔ 아무것도 인용하지 않는다. 종전 fix 였던 'dE_extract(+0.3356 eV)만 인용' 은 틀렸다 — sdcp_doped_closed_2026_08_28.json(active·ratified)이 회신 P P0 로 그 추출 부호를 철회하고 citable:no 로 강등했다"** 라고 적혀 있다(updated 2026-08-31). 이 hazard 항목에는 `id` 가 없어서 `hazard_claims()` 의 `if not hid: continue` 에 걸려 claim 으로 안 나가고, 렌더 실측 `claim-flag` **0개**다.
- **고치는 법**: citation_hazards 의 sdcp_phaseB_dftu_v1 항목에 `id: HZ-sdcp-phaseB-dE-extract` 와 `forbidden_phrases: ["dE_extract", "+0.336", "+0.3356"]` 를 붙여 스캐너에 태우고, 카드 58행 문장은 "철회된 값이라 이 반증 논거는 더 이상 쓰지 않는다"로 고쳐 쓴다.
- codex 필요: False

### [P1·ia] handoff-94-flat-list
- **어디**: `webapp/app.py:1245-1251 (`_handoffs()`) · webapp/templates/log.html:61-68`
- **근거**: `_handoffs()` 는 `for f in sorted(rd.glob("*.md"), reverse=True)` 로 kb/results 의 md 를 **전부** 담고 `{"id": f.stem, "name": f.stem.replace("_", " ")}` 만 준다. 템플릿은 그걸 `grid grid-3` 카드로 94개 깐다. 정렬이 파일명 역순이라 실제 순서는 `vgcf_hbn_gallery... → vgcf_hbn_figure_plan → uma_force_accuracy... → slide2_lit_summary...` 이고 제일 최근 카드(branch_state_2026_08_31)는 중간에 있다. 날짜·status·frontmatter 를 하나도 안 읽는다. /sdcp 의 "3D 구조 파일 버튼 95개"와 정확히 같은 유형이다.
- **고치는 법**: `_handoffs()` 가 frontmatter(date/updated/status/kind)를 읽어 (1) updated 내림차순 정렬, (2) 최근 90일 + status 가 진행/사용중인 것만 기본 노출, (3) 나머지는 `<details>` 접힘, (4) 카드에 날짜와 status 배지 표시로 바꿔라. frontmatter 없는 70장은 파일명 끝 `_YYYY_MM_DD` 를 폴백으로 쓴다.
- codex 필요: False

### [P1·stale] results-frozen-since-0831
- **어디**: `kb/results/ (폴더 전체) — 최신 카드 kb/results/branch_state_2026_08_31.md · 비교: kb/projects/restart_runbook_2026_09_07.md · kb/methodology/md_axis_status_2026_09_07.md · kb/papers/self_doping_dft_paragraph_2026_09_08.md`
- **근거**: `ls kb/results | grep -c 2026_09` = **0**. 본문에 2026-09 날짜가 한 번이라도 나오는 카드는 site_preference_findings·b2o3_arrhenius_curvature·sdcp_wave1_explainer **3장뿐**이다. 반면 9월 지식은 전부 다른 폴더로 갔다 — kb/methodology/md_axis_status_2026_09_07.md(23 KB), kb/concepts/md.md, kb/methodology/cascade_lessons_transfer_2026_09_08.md, kb/projects/restart_runbook_2026_09_07.md, kb/projects/handoff_2026_09_03_zn_nd.md. 즉 화면에서 "Session Handoffs" 라고 부르는 폴더는 **더 이상 handoff 가 안 쌓이는 폴더**고, 진짜 handoff(HANDOFF_2026_08_31_session.md · handoff_2026_09_03_zn_nd.md · restart_runbook_2026_09_07.md)는 kb/projects 에 있는데 화면에 안 나온다.
- **고치는 법**: 두 갈래 중 하나를 고른다. ① `_handoffs()` 가 kb/results + kb/projects 의 handoff/runbook 계열을 같이 읽고 종류 배지를 붙인다. ② kb/results 를 "결과 해석 아카이브"로 이름을 고정하고, handoff 화면은 kb/projects 를 읽게 바꾼다. 나중의 내가 기억을 되찾을 때 제일 먼저 보는 화면이라 ①이 낫다.
- codex 필요: False

### [P1·stale] semifinal-pointer-chain
- **어디**: `kb/results/b2o3_vs_lpscl16_md_2026_07_02.md:6 · kb/results/b2o3_bvse_channel_2026_07_02.md:6 → kb/results/b2o3_SEMIFINAL_report_2026_07_09.md`
- **근거**: 두 카드 모두 배너 끝에 `> 정본: kb/results/b2o3_SEMIFINAL_report_2026_07_09.md.` 라고 적어 독자를 넘긴다. 그런데 SEMIFINAL 은 git 이력상 2026-07-21(bdc5f3211)이 마지막 실질 개정이고, 본문 24행이 `| Ea (MD, 3-seed×3-T) | 0.197±0.032 eV | 0.199±0.034 eV | **동등** ✅ |` 로 **철회된 0.199 를 그대로 정본처럼** 싣는다(렌더 claim-flag 4개가 붙긴 하나 문서 자체는 '정본'을 자처한다). 화살표를 따라가면 더 낡은 곳에 도착한다.
- **고치는 법**: '정본' 포인터를 SEMIFINAL 이 아니라 kb/methodology/md_axis_status_2026_09_07.md(MD 축) / db/properties/b2o3_md_closed_retrospective_2026_08_25.json(마감) 으로 갈아끼우고, SEMIFINAL 머리에도 같은 배너를 단다. 앞으로 '정본:' 줄은 kb/results 안을 가리키지 말고 db/properties 나 kb/methodology 를 가리키게 규칙을 정하는 게 낫다(카드끼리 가리키면 사슬이 늙는다).
- codex 필요: False

### [P1·stale] beta-hard-gate-live
- **어디**: `kb/results/mlip_md_diffusive_gate_2026_08_01.md:8,45-52,99`
- **근거**: 8행 `**판정량** log-log 기울기 β = d(log MSD)/d(log t). β≈1 확산 · β<0.8 케이지 · β>1.2 드리프트`, 99행 `**권장**: 셀 확대 우선, 그래도 β<0.8 이면 시간도 연장. 어느 쪽이든 **게이트를 통과한 뒤에만**`. citation_hazards 의 `HZ-beta-hard-gate` 는 level **SUPERSEDED**, what = "β ≥ 0.80 하드게이트 — 판정으로 인용 금지. β 는 경보로만", why = "우리 운영점에서 고정문턱 0.8 은 거짓탈락률 50 %", fix = "판정축은 D_inc plateau · 창 안정성 · 홉 수". 그런데 forbidden_phrases 가 `["β ≥ 0.80","베타 하드게이트","β 하드게이트"]` 라 카드가 쓰는 `β<0.8` 표기를 못 잡는다 — 렌더 claim-flag 1개는 71행의 `0.199` 에 붙은 것이지 게이트 문구가 아니다.
- **고치는 법**: HZ-beta-hard-gate 의 forbidden_phrases 에 `β<0.8`·`β < 0.8`·`0.8-1.2`·`0.8–1.2` 를 추가하고, 카드 8행/99행에 "이 문턱은 2026-08-27 폐기, 현행 판정축은 D_inc plateau (kb/concepts/beta-gate.md §7-8b)" 를 병기한다. 카드의 결론(저이동도 계 Ea 인용보류)은 살아 있으니 결론을 지우면 안 된다 — 판정 **기준**만 낡았다.
- codex 필요: False

### [P1·wrong] b2o3-ea-0207-0223-live
- **어디**: `kb/results/b2o3_bond_lengths_2026_06_29.md:35,78 · kb/results/b2o3_phonon_stability_2026_06_30.md:6,36`
- **근거**: bond_lengths:35 `MD에서 b2o3가 modelc보다 더 잘 전도(Ea 0.207<0.226)한 것과 정합.`, :78 `**MD**(b2o3 D↑, Ea 0.207): 4d Cl anti-site 분율 25%...= site-disorder↑ → 전도↑와 정합.` — 0.207 은 db/properties/b2o3_md_arrhenius.json 의 `SUPERSEDED/highT_5_40/Ea_eV = 0.207` 로, 5-40 ps 창 인공물이라 이미 폐기된 값이다(`SUPERSEDED.note`: "(5-40) window faked a b2o3 Ea advantage"). phonon_stability:6 는 그 폐기를 알고 `아래의 Ea 0.207은 철회된 값` 이라 적으면서 대체값으로 `b2o3 Ea = 0.223 = 무도핑과 동일` 을 내세우는데, 0.223(=0.2234 단일시드)도 그 뒤 굽음 판정으로 함께 죽었다. bond_lengths 는 배너조차 없고 두 카드 다 렌더 claim-flag **0개**다.
- **고치는 법**: bond_lengths 머리에 "§MD 정합 논거는 폐기된 5-40 ps Ea 에 기댄 것 — 결합길이 결론(P–S 2.065 · B–S 1.827 · 4a/4d Δ0.17 Å)은 그대로 유효" 배너를 달고 35·78행 괄호를 지운다. phonon_stability:6·36 의 '0.223 = 무도핑과 동일' 은 "단일 Ea 자체가 철회, MD 축 은퇴"로 갱신한다. 두 카드의 0 K 결론(허수모드 0 · 결합길이)은 손대지 않는다.
- codex 필요: False

### [P1·stale] curvature-card-stale-line
- **어디**: `kb/results/b2o3_arrhenius_curvature_2026_08_23.md:274-280 · frontmatter 3-4행`
- **근거**: 본문 276-278행: `b2o3 에는 **등록된 재개 조건 자체가 없다** — \`db/properties/b2o3_*_closed_*.json\` 이 없다. MD 축 은퇴가 08-25 인데 마감 규율 채택이 08-28 이라 **사흘 차이로 안 걸렸다.**` — 그 파일은 지금 **있다**: `db/properties/b2o3_md_closed_retrospective_2026_08_25.json` (written_on 2026-09-07, ratify at 2026-09-07T07:32:35Z) + `db/properties/b2o3_cell_expansion_prereg_2026_09_07.json`(sealed 2026-09-07). 같은 문단이 "BH 에 어느 순서로 할지 물어 뒀다" 로 끝나는데 그 답(retrospective 로 소급 등록 후 전향적 prereg)은 이미 왔고 실행됐다. 덧붙여 frontmatter 는 `date: 2026-08-23 / updated: 2026-08-23` 인데 본문에 `⛔ **정정 (2026-09-07)**` 이 두 군데 있고 파일 mtime 도 Sep 7 06:20 이다 — kb/SCHEMA.md 의 "updated: 마지막 실질 수정 (고치면 bump)" 위반.
- **고치는 법**: 274-280 문단을 "재개 조건은 2026-09-07 에 소급 등록·비준됐다 (db/properties/b2o3_md_closed_retrospective_2026_08_25.json), 전향적 재개 카드는 b2o3_cell_expansion_prereg_2026_09_07.json" 으로 갈아끼우고 frontmatter `updated: 2026-09-07` 로 bump. 이 카드는 kb/results 에서 제일 잘 관리된 문서라 나머지를 이 형식에 맞추는 게 목표다.
- codex 필요: False

### [P1·stale] sdcp-master-status-stale
- **어디**: `kb/results/sdcp_master_summary_2026_07_16.md:5,15`
- **근거**: frontmatter 5행 `status: phaseB-5of5-DONE_verdict-PENDING-v2 (doped v1 retracted 2026-07-17; see open_items #4)`, 본문 15행 `**v2 = same-pose 설계**: ... ★VERDICT는 v2로 확정 예정.` — `tools/kb_wiki.py lint` 도 "status ... 인 채 **54일**" 로 잡는다. 그 사이 캠페인은 닫혔다: db/properties/sdcp_neutral_closed_2026_08_28.json · sdcp_doped_closed_2026_08_28.json(둘 다 active·ratified), 인용 확정본은 kb/results/sdcp_wave1_citable_2026_08_25.md 다. 'v2 로 확정 예정' 은 더 이상 계획이 아니다.
- **고치는 법**: status 를 `superseded — kb/results/sdcp_wave1_citable_2026_08_25.md + db/properties/sdcp_{neutral,doped}_closed_2026_08_28.json` 로 바꾸고 §0 문서 계보 절에 두 마감 파일을 추가한다. 본문 헤드라인 4개(폴라론 백본화·사슬 내부 선호·자기도핑 용이·DFT 앵커링)는 분자 축이라 살아 있으니 지우지 않는다.
- codex 필요: False

### [P1·duplicate] cbm-composition-conflict
- **어디**: `kb/results/redox_orbital_control_PS4_vs_BS3_2026_07_08.md:5,20 ↔ db/properties/b2o3_cbm_character_2026_09_07.json §1`
- **근거**: 카드 20행: `CBM 바닥 1.2 eV 조성: b2o3 **S 46% P 27%** Li 15% B 10% **O 0%**`. db(2026-09-07) `b2o3_비중_pct`: `B 46.3 · P 36.8 · S 12.3 · Li 2.8 · O 0.9 · Cl 0.8` 이고 별표가 **"원자 2개짜리 B 가 CBM 성분 1위다"** 라고 못박는다. 같은 이름의 양(b2o3 CBM 조성 %)이 두 곳에서 1등이 뒤바뀐 채로 있고, 서로를 안 가리킨다. 차이는 정규화다 — db 는 `원소별 총량은 원자수에 끌려가므로 정규화 필수` 라며 **원자당**으로 냈고 카드는 총량으로 냈다. 창도 1.2 eV vs ~1.0 eV 로 다르다.
- **고치는 법**: 양쪽에 정규화와 창을 이름에 박아라 — 카드는 `CBM 총 성분(비정규화, 0~1.2 eV)`, db 는 `CBM 원자당 성분(0~1.0 eV)`. 그리고 카드 20행에 db 파일 경로를 링크로 걸어 두 값이 모순이 아니라 다른 양임을 보이게 한다. 카드의 σ* 논거(결합당 무게 P–S 3.7×)는 원자당 지표와 충돌하지 않지만 지금 표기로는 독자가 반대로 읽는다.
- codex 필요: False

### [P1·wrong] sigma-vs-expt-contradiction
- **어디**: `kb/results/ionic_conductivity_full_explained_2026_06_21.md:13 ↔ db/properties/li_transport.json:64-65`
- **근거**: 카드 13행: `**modelc(LPSCl₁.₆)는 comp1(LPSCl)보다 σ_Li ~4배** (3.35 → 13.96 mS/cm, AIMD-MLIP). 실험 x=0.6 = 11.34 mS/cm와 일치.` 그런데 정본 db 는 `"sigma_300K_expt_LPSCl_Scm": "2e-3 to 5e-3"`, `"sigma_300K_calc_Scm": "~14e-3 (3-5× higher than expt)"` 로 **같은 ~14 를 실험보다 3–5배 높은 값**이라고 적는다. 카드는 다른 조성(x=0.6)의 실험값을 골라 "일치"라고 결론지어 db 의 계통오차 단서를 지운다. CLAUDE.md 의 "σ 절대값 인용 금지" 와도 정면으로 어긋난다.
- **고치는 법**: 13행에서 절대값 두 개와 '실험과 일치' 문장을 빼고 "MLIP N-E 절대 σ 는 실험 대비 3–5× 상한이라 인용하지 않는다(li_transport.json:caveats)" 로 바꾼다. 55-59행 표의 σ(300K) 열은 남기되 열 제목에 ⛔ 표기를 단다.
- codex 필요: False

### [P1·missing] no-frontmatter-70
- **어디**: `kb/results/ 94장 중 70장 (예: MASTER_structure_property_logic_2026_06_21.md · adhesion_*.md 9장 · b2o3_*.md 14장 중 13장 · ionic_*.md 3장)`
- **근거**: `head -1` 이 `---` 인 파일을 세면 **24장뿐**이고 70장은 frontmatter 가 없다. kb/SCHEMA.md 는 "새 문서부터 필수. 기존 199개 소급 없음 (lint 는 frontmatter 있는 문서만 깊이 검사)" 라 규칙 위반은 아니지만, 결과가 이렇다 — status·updated·verificationStatus 가 없으니 lint 도 웹앱도 "이 카드가 살았나"를 기계적으로 못 판정하고, `_handoffs()` 가 날짜 정렬조차 못 하는 근본 원인이 이것이다.
- **고치는 법**: 전부 소급하지 말고 **아직 인용되는 카드부터** frontmatter 를 붙여라 — 최소 `title/date/updated/status/supersedes` 다섯 줄. 우선순위: MASTER · ionic 3장 · lpscl 3장 · b2o3 13장 · adhesion 은 `status: 아카이브(paper #2)` 한 줄만. 나머지(세션로그·발표대본)는 IA 로 옮기면서 자연스럽게 처리한다.
- codex 필요: False

### [P1·missing] no-entry-card
- **어디**: `kb/results/ (README·index 카드 없음) · kb/index.md:84-178`
- **근거**: `ls -a kb/results` 에 .md 94개 말고 아무것도 없다. kb/index.md 의 `## results/ (94)` 절은 파일명 알파벳 순으로 94줄, 각 줄이 `- \`경로\` — H1 제목` 뿐이고 날짜·상태가 없다. 그래서 "지금 b2o3 에 대해 말할 수 있는 게 뭐냐" 를 알려면 14장을 다 열어야 하고, 열어도 그중 6장이 철회된 값을 말한다.
- **고치는 법**: kb/results/README.md 를 계(system)별 한 장 지도로 만든다 — 계마다 [지금 유효한 카드 1장 / 마감·철회 근거 파일 / 접힌 역사 카드들] 세 줄. b2o3 를 예로 들면: 유효 = 0 K DFT 축(elf/icohp/hull/phonon), 마감 = db/properties/b2o3_md_closed_retrospective_2026_08_25.json, 역사 = MD 6장. 이 파일이 나중의 내가 제일 먼저 읽을 문서다.
- codex 필요: False

### [P2·duplicate] argyrodite-review-duplicate
- **어디**: `kb/results/argyrodite_literature_review_2026_06_26.md ↔ kb/results/argyrodite_review_comprehensive_2026_06_26.md`
- **근거**: 같은 날짜·같은 소재. 앞은 `이번 세션에 litdb로 정리한 ~24편을 **과학 섹션별로 분류**하고`, 뒤는 `2026-06 세션에 litdb로 정밀 정리한 28편(...)을 **6개 과학 축**으로 종합하고` 로, 둘 다 litdb 같은 묶음의 6축 리뷰다(215줄 + 별도 1장). CLAUDE.md 는 "문헌은 litdb/ 가 정본 (digest + INDEX.md + comparison_vs_ours.md)" 이라 하고 kb/SCHEMA.md 는 kb/literature_db 를 구세대로 못박는데, 이 둘은 results/ 에 있는 문헌 리뷰다.
- **고치는 법**: comprehensive 쪽을 남기고 literature_review 는 litdb/surveys/ 로 옮기거나 comprehensive 안으로 흡수한다. 어느 쪽이든 litdb/comparison_vs_ours.md 와의 관계를 한 줄로 적어라 — 지금은 같은 비교가 세 곳에 있다.
- codex 필요: False

### [P2·ia] drafts-misfiled-in-results
- **어디**: `kb/results/{deck_ionic_section_additions,presentation_script_BVSE_ionic_2026_06_19,presentation_script_LPSCl_vs_LPSCl16_2026_06_18,slide2_lit_summary_revised_2026_06_21,paper_figure_plan_v3,vgcf_hbn_figure_plan,section1_system_design,section2_bader_cross_comp,session_timelog_2026_06_04,litdb_session_map_2026_06_26,doping_273_qa_log}.md`
- **근거**: kb/SCHEMA.md 의 디렉터리 ↔ 타입 표는 `results`(우리 결과 해석) · `reports`(대외 문서) · `seminars` · `papers` 를 나눈다. 그런데 results/ 안에 발표 대본 2장(`# Slides 4–7 (Ionic conductivity) — 추가 슬라이드 콘텐츠`), figure plan 2장(`마지막 업데이트: 2026-06-03`), 원고 섹션 초안 2장(section1/section2), 세션 타임로그(`마지막 갱신: 2026-06-05 (작업 중)`), litdb 인덱스, QA 로그가 섞여 있다. 결과 11장이 결과가 아니다 — 그래서 handoff 목록 94개 중 12%가 처음부터 잡음이다.
- **고치는 법**: deck/presentation/slide → kb/seminars, paper_figure_plan·section1·section2·vgcf_hbn_figure_plan → kb/papers, session_timelog·doping_273_qa_log → kb/projects, litdb_session_map → litdb/. 옮길 때 kb/index.md 는 `tools/kb_wiki.py index` 로 재생성하고 lint 0 errors 를 확인한다(경로 인용이 깨질 수 있다).
- codex 필요: False

### [P2·useless] stale-status-docs
- **어디**: `kb/results/elastic_0K_protocol_status.md:3-6 · kb/results/session_timelog_2026_06_04.md:3-4 · kb/results/paper_figure_plan_v3.md:5`
- **근거**: elastic_0K_protocol_status:3-6 = `> **Status as of 2026-05-01** / **comp1 v2**: VERIFIED ... **comp3-5, modelC v2**: 0K Cij not yet recomputed with verified protocol.` — 4개월 전 상태를 현재형으로 말한다. session_timelog:3-4 = `여러 트랙 동시 진행으로 헷갈림 방지용 전체 스냅샷. ... 마지막 갱신: 2026-06-05 (작업 중)` — 3개월 전 스냅샷이 '작업 중'이다. paper_figure_plan_v3:5 = `마지막 업데이트: 2026-06-03` 인데 원고 작업은 kb/papers/self_doping_dft_paragraph_2026_09_08.md 로 넘어갔다. 상태 문서는 낡으면 없는 것보다 나쁘다 — 사람이 현재로 읽는다.
- **고치는 법**: 셋 다 머리에 `⚠ 이 문서는 <날짜> 스냅샷이다 — 현재 상태는 <경로>` 를 박고 status 를 아카이브로 내린다. elastic 은 db/properties/elastic.json + citation_hazards 의 elastic 조건부 항목을, paper_figure_plan 은 kb/papers/ 를 가리킨다. 지우지는 마라 — 당시 판정 이력이다.
- codex 필요: False

### [P2·broken] broken-figure-path
- **어디**: `kb/results/b2o3_anode_interface_MD_dynamics_2026_07_06.md (인용 경로 `docs/figures/oxidation/interface_decomp_b2o3_vs_undoped.png`)`
- **근거**: `python3 tools/kb_wiki.py lint --legacy` 출력에 `· kb/results/b2o3_anode_interface_MD_dynamics_2026_07_06.md: docs/figures/oxidation/interface_decomp_b2o3_vs_undoped.png` — kb/results 안의 깨진 경로는 이 한 건뿐이다(레거시 20건 중).
- **고치는 법**: 파일이 이름을 바꿨는지 확인해 경로를 고치거나, 이 카드가 SUPERSEDED 문서라 그림이 폐기된 것이면 그 줄에 `<!-- lint-skip-path -->` 대신 "그림은 후속 campaign(2026-07-07)으로 대체" 라고 적고 경로를 지운다.
- codex 필요: False

### [P2·wrong] aimd-label-for-mlip
- **어디**: `kb/results/MASTER_structure_property_logic_2026_06_21.md:70-71 · kb/results/ionic_conductivity_full_explained_2026_06_21.md:47 · db/properties/li_transport.json:description`
- **근거**: MASTER 마스터 비교표의 근거 열이 `| Ea (eV) | 0.253 | 0.224 | ↓ | AIMD |`, `| σ₃₀₀ (mS/cm) | ~3.4 | ~14 | **×4** | AIMD+NE |` 다. 실제 방법은 UMA-s-1p1(omat) MLIP-MD 다 — li_transport.json 의 method_notes.aimd_mlip 자신이 `Born-Oppenheimer MD with foundation MLIP (UMA-s-1p1, task=omat)` 라고 적는다. db 가 'AIMD-MLIP' 라는 합성어를 쓰고 카드가 그걸 'AIMD' 로 줄이면서, 표만 보는 사람에게는 ab initio MD 로 읽힌다. 원고로 새면 방법 오기다.
- **고치는 법**: repo 전역 용어를 `MLIP-MD (UMA-s-1p1/omat)` 하나로 통일하고 'AIMD' 단독 표기를 카드·db description 에서 없앤다. CLAUDE.md 가 이미 'MLIP-MD' 를 쓰므로 그쪽이 기준이다.
- codex 필요: False

### [P2·stale] branch-state-superseded-chain
- **어디**: `kb/results/branch_state_2026_08_31.md (frontmatter status: 진행)`
- **근거**: 08-30 판은 `status: superseded — kb/results/branch_state_2026_08_31.md` 로 제대로 넘겼는데, 08-31 판이 `status: 진행` 인 채 8일이 지났고 그 사이에 LPSOCl 마감 비준·cascade 보고량 카드 비준·cascade 봉인 v2·Nd 어닐 6셀·claim 결속 이주·QE-GPU ldd 규율이 전부 들어왔다(git log 0b6451b54..83c868a97). '지금 살아 있는 것과 죽어 있는 것' 을 표방하는 문서라 낡으면 그대로 오답이 된다.
- **고치는 법**: branch_state 는 날짜별 새 파일을 만드는 대신 **한 파일을 갱신**하고 이력은 git 에 맡기는 게 낫다(지금 방식이면 3일마다 한 장씩 늘어 handoff 목록이 계속 붓는다). 당장은 08-31 판 status 를 `아카이브` 로 내리고 현재 지도를 kb/projects/restart_runbook_2026_09_07.md 로 가리킨다.
- codex 필요: False
