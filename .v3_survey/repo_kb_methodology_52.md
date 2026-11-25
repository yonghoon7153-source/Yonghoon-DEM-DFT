# repo — kb/methodology (52편)

## 지금 무엇인가
"방법론 카드" 라는 이름 아래 실제로는 여섯 종류가 섞여 있다 — 진짜 방법 규약(md_conductivity_protocol, computational_methods_canonical), 서버 런북 3편, 캠페인 진행 로그(cascade 5편), 하룻밤 인수인계 1편, 용어·에이전트·위키 규율 같은 repo 살림 카드 5편, 그리고 보고량 카드 1편. 시기는 2026-05 부터 2026-09-08 까지 넉 달이 평면 알파벳 순으로 섞여 있고, frontmatter 는 52편 중 24편만 완전하고 25편은 아예 없다(SCHEMA 의 "기존 소급 없음" 규정 때문에 위반은 아니지만, 그래서 index 에 날짜·상태가 안 찍힌다). **본문을 전문 또는 절반 이상 읽은 것은 12편**(beta_gate_seed_policy · md_conductivity_protocol · md_adaptive_v2 · md_axis_status · terminology_register · handoff_2026_08_20_night · cascade_lessons_transfer · esp_z590_setup · elastic_constants · computational_methods_canonical · electron_localization_framework · adhesion_energy), **나머지 40편은 frontmatter + 목차 + 표적 grep 만 봤다** — 특히 cascade_composition_family · defect_cell_size_metric · vanhove · ps4_libration · selftest_blind_spots · offline_archive_index · kisti_setup · li_adatom_neb_protocol · site_preference_protocol · coating_descriptor_catalog 는 본문을 안 읽었으니 여기 없는 문제가 있을 수 있다.

## 처음 오는 사람
폴더를 열면 알파벳 52줄이고 진입점(README·색인)이 없다. 그래서 질문별로 이렇게 된다. ① "MD 를 어떻게 재나" → `md_conductivity_protocol.md`(2026-06 본문 + 철회 배너)에 닿는데, 여기서 `md_adaptive_v2_protocol`(생산길이 표준을 바꿈)이나 `md_axis_status_2026_09_07`(무엇이 인용 가능한지)로 가는 링크가 **한 줄도 없다** — 역링크는 저쪽에서 이쪽으로만 있다. ② "β 게이트가 뭐냐" → `beta_gate_seed_policy.md` 가 "규칙(이대로 집행한다)" 로 폐기된 문턱을 집행 규칙으로 읽어준다. ③ "kgy 에서 pw.x 어떻게 돌리나" → `esp_z590_setup.md` 가 2026-09-08 에 **세 번 연속 틀린 그 답**(HPC-X mpirun)을 준다. ④ "우리 Ea 값이 뭐냐" → `computational_methods_canonical.md` §6 이 네 조성 Ea 를 나란한 비교표로 준다 — 레지스트리에서 그 표의 행들은 `retracted` 1건 · `provisional` 5건이고 `cross_composition_ranking` 이 금지돼 있다. 반대로 잘 되어 있는 것 하나: `md_axis_status_2026_09_07.md` 는 한 편만 읽으면 MD 축 전체(살아있는 것/죽은 것/도는 것/색인)가 나온다 — 이게 이 폴더가 가져야 할 형태의 모델이다.

## 건드리면 안 되는 것
- **md_axis_status_2026_09_07.md 는 손대지 마라(§5·§7 날짜 갱신 빼고).** 이 폴더에서 유일하게 '살아있는 것 / 죽은 것 / 도는 것 / 남은 것 / 색인' 5절 구조를 갖춘 축 지도다. 나머지 재편의 **본보기**로 삼을 문서이고, 특히 §1.5 의 자기정정(초판이 §1 에 잘못 올렸다고 적은 것)과 §8 색인 블록은 그대로 둔다.
- **md_conductivity_protocol.md 의 §5 표·§6 전체(SUPERSEDED 본문)를 지우지 마라.** kb/SCHEMA.md Update Policy 가 '철회는 원문 보존 + 반증 병기' 다. 단일시드 13.94/18.51/1.33× 는 **철회 이력의 물증**이고, md_axis_status:151 이 이 절들을 이름으로 지목해 죽은 것 표에 올려놨다. 배너만 유지하고 본문은 보존.
- **철회된 값의 원자료를 지우지 마라.** md_axis_status:83 이 `\`highT_reseed\` 구판 12런 | gen0 | ⛔ 무효 (Ea 0.199/0.197 의 원자료 — 지우지 말 것)` 라고 명시한다. 카드에서 값을 내리는 것과 원자료를 지우는 것은 다른 일이다.
- **cascade_pipeline_anatomy 의 자기정정 절(L503 · L700 · L948)은 원문 그대로 둔다.** 요약으로 끌어올리는 것은 좋지만, '앞 절 정정' · '내 오류 하나 철회' 라는 기록 자체가 이 repo 의 제일 비싼 자산이다. 분리하더라도 삭제 아님.
- **authoredBy: external 문서와 회신 원문은 고쳐 쓰지 않는다** (CLAUDE.md 용어 규율 단서). 이번 조사 대상 52편에는 external 이 없지만, 여기 카드들이 인용하는 회신(AL·BG·BH·F·N·O) 원문에 손대면 이력이 깨진다.
- **기계 경로(estimand_card.md · canary_geometry · kind: \"estimand\")는 이름을 안 바꾼다.** 용어를 '보고량 / 대조 잡' 으로 바꾸는 것은 **앞으로 쓰는 산문**에만 적용한다 — 필드명을 개서하면 db/governance/decisions.json 과 게이트가 끊긴다.
- **검증까지 끝난 카드 6편은 건드릴 이유가 없다** — estimand_before_running_2026_08_28(회신 N·O 정정이 §2.1·L109·L117 에 이미 반영) · selftest_blind_spots_2026_08_28 · defect_cell_size_metric_2026_08_16 · cascade_design_contract_2026_08_28 · vanhove_plateau_70traj_2026_08_28 · ps4_libration_dopant_2026_08_28. (뒤 두 편은 frontmatter·검증문만 봤고 본문은 안 읽었으니 '문제 없음' 이 아니라 '이번 조사에서 걸린 게 없음' 이다.)
- **서버 카드 3편의 빌드 이력(configure 플래그 · cc86 · --without-libxc · makelocalrc · UMA 캐시 rsync 절차)은 지우지 마라.** 런타임 문장만 틀렸다. 재빌드할 때 이 절들이 유일한 근거다.
- **kb/index.md 는 손편집 금지** — `python3 tools/kb_wiki.py index` 생성물이다. 순서·묶음을 바꾸려면 생성기를 고친다. 그리고 `explored:` 는 사람만 true 로 바꾼다.
- **frontmatter 없는 25편에 소급 frontmatter 를 일괄 자동 삽입하지 마라.** kb/SCHEMA.md 가 '기존 199개 소급 없음' 을 명시적으로 결정했다. 손대는 카드에 한해 그 김에 붙이는 것까지만.

## 발견

### [P0·wrong] beta-gate-retired-but-enforced
- **어디**: `kb/methodology/beta_gate_seed_policy.md:12,36,78`
- **근거**: 카드 L12 `게이트: β̄ ∈ [0.8, 1.2]`, L36 `## 규칙 (이대로 집행한다)`, L78 `| **≥ 0.80** | **(C) 느린 전이 확정** |`. 그런데 kb/methodology/md_axis_status_2026_09_07.md:155 의 '죽은 것' 표는 `**β 하드게이트 0.8–1.2** | 문헌 근거 없음 + 우리 운영점에서 **거짓탈락 50 %**. 양방향으로 틀렸다 | 2026-08-27`. db/properties/citation_hazards.json 의 HZ-beta-hard-gate 도 `level: SUPERSEDED`, `forbidden_phrases: ["β ≥ 0.80","베타 하드게이트","β 하드게이트"]`. 그 hazard 의 `file` 은 `tools/ionic/msd_diffusive_check.py (규약)` 만 가리키고 **이 카드는 안 가리킨다**. 반대로 도구 쪽은 이 카드를 선언 문서로 지목한다 — tools/ionic/watch_kgy.py:170 `# 선언: kb/methodology/beta_gate_seed_policy.md`, :863 `print("     ⚠ 시드 추가 규칙: kb/methodology/beta_gate_seed_policy.md — 정지 규칙을 먼저")`, tools/ionic/msd_diffusive_check.py:2363 동일. beta-gate.md 자신이 §7-8e 에서 `**폐기가 도구에 안 내려갔다** (2026-08-30, 회신 AK 가 잡아냈다)` 라고 적어놨는데, 같은 사고가 이 카드에서 아직 안 끝났다.
- **고치는 법**: 카드 최상단에 SUPERSEDED 배너 — '0.8–1.2 하드게이트는 2026-08-27 폐기(kb/concepts/beta-gate.md §7-5·§7-8b, 회신 F). 판정축은 D_inc plateau · 창 안정성 · 홉 수'. 본문(정지 규칙 1~5, lpsocl 600 K 선언)은 원문 보존 — 정지규칙을 결과 보고 고르지 않는다는 논지는 게이트와 독립으로 여전히 유효하니 그 부분만 살아있다고 명시. 그리고 citation_hazards.json HZ-beta-hard-gate 의 `file` 에 이 카드 경로를 추가해서 다음엔 레지스트리가 잡게 한다.
- codex 필요: False

### [P0·wrong] elf-card-forbidden-claim
- **어디**: `kb/methodology/electron_localization_framework_2026_07_08.md:16,88`
- **근거**: L16 (한눈 요약 표) `| ⑤ 균형(전도) | ... | O-penalty를 채널개방이 상쇄 (Ea 0.199=0.197) |`, L88 `**면내 BVSE 채널 개방(+45%)이 그 penalty를 상쇄** → Ea 0.199≈0.197, σ 비율 ~1.0 (완전대칭 3-seed×3-T). **"O를 넣고도 전도 보존"의 미시 수지 균형.**` — 두 곳 다 철회 배너 없이 살아있는 결론으로 적혀 있다. 반면 db/properties/canonical_registry.json 의 b2o3 MD_Ea_eV 0.199 는 `status: retracted`, prohibitions 에 `ranking`·`single_line_fit_over_600_1000K` 포함. 그리고 md_axis_status_2026_09_07.md §1.5 가 원자료 CSV 의 금지문을 축자로 옮겨놨다: `FORBIDDEN: 'statistically EQUIVALENT transport' / 'conductivity PRESERVED' / 'equivalent sigma' / any ranking or mechanism claim`. 이 카드의 "전도 보존" 은 그 금지 목록 2번을 한국어로 옮긴 것이고, "채널 개방이 상쇄" 는 mechanism claim 이다.
- **고치는 법**: L16·L88 에 철회 결속 배너: 'b2o3 Ea 0.199 는 2026-08-23 철회(곡률 145 meV) · σ 비는 citable:no(BH P0-1) — 이 절의 수지 결론은 그 위에 서 있다'. 허용 문장은 md_axis_status §1.5 에 축자로 있으니 그것으로 교체. §8 회계표의 gap/ELF/Bader 행은 DFT 라 영향 없으니 남긴다. **다만 "채널 개방이 O-penalty 를 상쇄한다" 라는 기전 주장 자체가 σ 비 잠금 이후에도 서는지는 우리가 못 정한다** — 리뷰에 붙일 것.
- codex 필요: True

### [P0·wrong] kgy-qegpu-runtime-inverted
- **어디**: `kb/methodology/esp_z590_setup.md:78,92,114`
- **근거**: L114 `6. **GPU launcher must be NVHPC's HPC-X mpirun**, not \`/usr/bin/mpirun\` (apt 4.0.3). The GPU \`pw.x\` is linked to the SDK's HPC-X OpenMPI.`, L78 `\`qegpu()\` ... sets \`OPAL_PREFIX\` (HPC-X ompi), \`MPIRUN\` (HPC-X mpirun)`, L92 `qegpu                       # sets HPC-X mpirun + NVHPC libs + QE-GPU PATH`. 이 카드가 kgy 머신이다(L3 `**Target host:** \`59.12.161.91\` (ssh \`kgy@59.12.161.91\`)`). CLAUDE.md 2026-09-08 판정과 정반대다: `③ hpcx 를 자동탐지했는데 kgy 의 pw.x 는 **~/apps/openmpi-4.1.6** 로 빌드돼 있었다 (hpcx 에서 오는 건 scalapack 뿐)`. tools/doping/run_force_check_scf.sh:72-73 도 같은 말을 실측으로 적고 있다. 또 `OMP_NUM_THREADS=1`(libnvomp+libgomp 동시 링크 회피)이 이 카드에 **없다** — 러너 L93-95 는 그걸 강제한다. kb/ 전체를 `grep -rn "ldd"` 해도 0건 — 2026-09-08 교훈은 CLAUDE.md 와 러너 스크립트에만 있고 **kb 카드에는 하나도 안 내려왔다**.
- **고치는 법**: Gotcha #6 을 철회선 처리하고 그 자리에 ldd 규칙을 적는다(`M=$(ldd <pw.x> | awk '/libmpi\.so/{print $3}')` → OPAL_PREFIX 유도). Gotcha #5 도 정정 — libgomp 는 conda 탓만이 아니라 libfftw3_omp 가 GNU 를 끌고 와서 바이너리에 **이미** 링크돼 있다는 것이 09-08 실측. kserver116_setup.md:183-188 의 hpcx 하드코딩(`export OPAL_PREFIX=$NVHPC/comm_libs/12.6/hpcx/hpcx-2.20/ompi`)도 gabia 에서 ldd 로 재확인 전까지 '그 머신 기준, 확인 필요' 표시. 정본은 tools/doping/run_force_check_scf.sh 라고 세 서버 카드에 다 적는다.
- codex 필요: False

### [P0·wrong] cmc-md-ea-table-no-citability
- **어디**: `kb/methodology/computational_methods_canonical.md:143-153`
- **근거**: L143 `**프로토콜 (고정):** ... equilib 5 ps + prod 200 ps ...`, 그 아래 표가 `| comp1 | **0.253** |`, `| modelc | 0.224 |`, `| lpsocl | 0.271±0.033 / 0.287±0.024 |`, `| comp2 | **계산중** (s2 단일 0.312, 3-seed 대기) |` 이고, 이어 L153 `> MD는 UMA라 pseudo와 무관. comp1↔comp2 비교는 같은 UMA·프로토콜·멀티시드면 성립`. 실제 레지스트리(db/properties/canonical_registry.json)는 comp1 0.2532 `provisional` + `cite_until_beta_gate_passes` + `cross_composition_ranking` 금지, lpsocl 0.2867 `provisional` + 같은 금지, comp2 0.2754/0.1512 `provisional` + `cross_composition_ranking` 금지, b2o3 0.199 `retracted`. md_axis_status_2026_09_07.md §0 은 `지금 이 축에서 원고에 넣을 수 있는 활성화에너지는 0개다` 라고 못박는다. 즉 '단일 기준' 을 자칭하는 카드가 계간 비교를 **권하고** 있고, 그게 정확히 금지된 것이다. 덧붙여 §10 의 `| **modelc 굽음 여부** | 🟡 판정 중 | 600 K 3시드 MD 완주 대기(gabia) |` 는 md_axis_status §6-① 1저자 결정(2026-09-07, "나중에 한다 · 지금은 안 연다")으로 이미 처리됐다.
- **고치는 법**: §6 표에 status/prohibitions 열을 붙이고(철회 1 · 잠정 5), 표 위에 `⛔ 이 축은 citable 0개 — 계간 비교 잠금(md_axis_status §0·§7)` 배너. `comp2 계산중` 은 레지스트리 값으로 갱신. §10 modelc 굽음 행은 '1저자 결정으로 LPSOCl 뒤로(2026-09-07)' 로 교체. 값 자체는 여전히 각 db 파일이 정본이니 이 카드는 '축과 금지' 만 말하게 남긴다.
- codex 필요: False

### [P1·stale] md-axis-lpsocl-closure-ratified
- **어디**: `kb/methodology/md_axis_status_2026_09_07.md:198,206,240`
- **근거**: L198 `- **닫힘 조건(결과 보기 전 사전등록)**: \`..._closure_conditions_2026_09_07.json\` ⏳ 1저자 결정 3건 대기`, L206 `| **C3** | 구간 Ea 양립 | ⏳ 1σ/2σ 미정 (Codex BG Q4) |`, L240 `| LPSOCl 400 ps C3 문턱 | ⏳ Codex BG Q4 |`. 실물은 이미 닫혔다 — db/properties/lpsocl_box331_closure_conditions_2026_09_07.json 의 `status: "ratified"`, 지위 필드 `✅ **active — 1저자 비준 완료 (2026-09-08).** §7 결정 3건이 비준됐고 C3(δEa 0.050 eV)·C5(해상도 0.050 eV)·§6 재개조건이 확정됐다`. 그리고 1σ/2σ 질문 자체가 폐기됐다: `⛔_이_질문은_폐기됐다 = 1σ/2σ 겹침 판정 자체를 회신 BG Q4 가 반대했고 ... C3 가 ΔEa 직접 계산 + 허용차 δEa 로 재설계됐다`. db/governance/decisions.json 에도 `D-2026-09-08-lpsocl-box331-closure-conditions | active`.
- **고치는 법**: L198·L206·L240 을 비준 결과로 갱신(C3 = ΔEa 직접계산 · δEa 0.050 eV · HOLD 는 결과로 보고하고 닫는다). 카드가 '새 판정 안 함, 어디에 뭐가 있는지만' 을 표방하니 결정 ID(D-2026-09-08-...)를 인용만 하면 된다.
- codex 필요: False

### [P1·stale] cascade-lessons-4-already-ratified
- **어디**: `kb/methodology/cascade_lessons_transfer_2026_09_08.md:100`
- **근거**: L100 `## 4. #1·#2b 에 대한 우리 안 (1저자 확인 대기)` — 이 카드는 커밋 d3a878e4b(2026-09-08 14:04). 7분 뒤 22b00e909(14:11) 이 `cascade 보고량 카드 비준 (proposed → active)`, 14:18 8c9338c96 이 `cascade Step 1 — aggregate_designs 를 **대표 행 선택**으로 교체 (비준 카드 §2)` 로 §4 제안을 그대로 구현했다. db/properties/cascade_d_rel_estimand_2026_09_08.json 지위 = `✅ **active — 1저자 비준 완료 (2026-09-08).** 해제조건 #1·#2b·#5·#6 확정`. decisions.json 의 D-2026-09-08-cascade-d-rel-estimand 는 `active` 이고 근거 목록에 이 카드 경로가 들어 있다(decisions.json:1414).
- **고치는 법**: §4 제목을 '(2026-09-08 비준 — cascade_d_rel_estimand_2026_09_08.json §2)' 로 바꾸고 §1 표의 ⑤ '신설 제안' 도 지금 지위를 적는다. 카드가 '스스로 해제하지 않는다' 는 규율은 유지 — 비준 사실만 반영.
- codex 필요: False

### [P1·missing] terminology-missing-0901-register
- **어디**: `kb/methodology/terminology_register.md (전체 100줄) · 특히 :53,:54`
- **근거**: CLAUDE.md 는 2026-09-01 1저자 결정으로 용어 규율을 박았다: `estimand → **보고량** / 정의된 측정량`, `canary·카나리 → **대조 잡**`, `claim ceiling → **허용 서술 범위**`, 그리고 '코드 필드명·과거 기록은 안 바꾼다'. 이 파일이 바로 '우리 말 → 필드 표준어' 대장인데 셋 다 **없다**(A~F 전 절 grep 0건). 게다가 §C 수송 절이 폐기된 문턱을 그대로 쓴다 — L53 `"확산영역 게이트" | **diffusive-regime criterion** ... 0.8 문턱은 우리 것이다`, L54 `"게이트 실패" | **sub-diffusive (caged) regime** | β < 0.8 이면 D 가 정의되지 않는다`. β 0.8 하드게이트는 2026-08-27 폐기(citation_hazards HZ-beta-hard-gate SUPERSEDED).
- **고치는 법**: §G 신설 — 09-01 용어 3쌍 + '기계 경로(estimand_card.md, canary_geometry, kind:"estimand")는 안 바꾼다' 단서. §C L53-54 는 폐기 표시하고 대체 판정축(D_inc plateau·창 안정성·홉 수)으로 교체. 이 파일은 발표 직전에 읽는 파일이라 여기 틀린 게 제일 비싸다.
- codex 필요: False

### [P1·missing] nd-anneal-no-card
- **어디**: `kb/methodology/ (Nd O-모티프 어닐 카드 부재) · kb/methodology/li_annealing.md:19`
- **근거**: 2026-09-08 커밋 83c868a97 `Nd2O3-LPSCl1.6 어닐 6셀 회수 — UMA 500 K 20 ps + relax (순위: distributed < free_s < bo4)` 와 51b5dec21 `--from_xyz: 완화 구조 → scf 단일점 (Nd O-모티프 UMA 순위 DFT 재채점, 4셀)` 이 캠페인 하나를 열었는데 kb 에 카드가 없다. `grep -rln "bo4\|O-모티프\|free_s" kb/` = cascade_lessons_transfer(지나가는 한 줄) · b2o3_doping_chemistry · 리뷰 프롬프트 2편뿐. 정작 Nd 방법론 카드인 nd_vs_O_isolation_campaign_2026_06_18.md 는 2026-06-18 상태 그대로다. 게다가 프로토콜이 어긋난다 — li_annealing.md:19 `2. MLIP MD at **500K** for 50-100 ps`, 실제 실행은 db/structures/ndo_lpscl16_rietveld_2026_09_07/anneal_2026_09_07/anneal_results.json 의 `time_ps = 20.0` (6셀 전부). 어느 쪽이 표준인지 아무 데도 안 적혀 있다.
- **고치는 법**: `kb/methodology/nd_o_motif_anneal_2026_09_08.md` 신설 — 무엇을 재는가(같은 n 안의 O 모티프 총에너지 차) · UMA 순위 3종 · 커밋 메시지에 있는 금지 4줄(UMA 값 인용 금지 · 시드 1개 · 셀 고정 · delta_E_anneal 은 어닐 이득 아님) · DFT 재채점 진행 상태. li_annealing.md 는 '50-100 ps 는 할로겐 치환 스크리닝 판, Nd O-모티프는 20 ps 판' 으로 판을 갈라 적거나, 20 ps 를 선택한 이유를 적는다.
- codex 필요: False

### [P1·stale] md-production-length-three-way
- **어디**: `kb/methodology/md_conductivity_protocol.md:34 (§1 표) vs CLAUDE.md vs kb/methodology/md_adaptive_v2_protocol_2026_08_27.md:45`
- **근거**: 세 곳이 다르다. md_conductivity_protocol §1 표: `| production | **≥ 50 ps** (window 상한 50 ps를 덮어야 함) |`, `| friction | 0.01–0.02 /fs (스크립트 기본) |`. CLAUDE.md: `equilib 5 ps / prod 200 ps ... friction 0.02`. md_adaptive_v2 L45: `| **\`MDadaptive-v2\`** | **200 → 400 → 800 → 1600 ps checkpoint**. 사전 기준을 만족하면 종료 |` (status: 채택). 그런데 md_conductivity_protocol 에서 md_adaptive_v2 나 md_axis_status 로 가는 링크가 0건이다(`grep -n 'md_adaptive\|md_axis' kb/methodology/md_conductivity_protocol.md` → 없음). 역방향만 있다 — md_axis_status:99 가 `파이프라인 설정 ... | \`kb/methodology/md_conductivity_protocol.md\` **§1–§4**` 로 이쪽을 정본으로 지목한다. 그래서 정본으로 지목된 문서가 자기를 감싸는 두 결정을 모른다.
- **고치는 법**: md_conductivity_protocol 상단 살아있는 것 블록에 두 줄 추가 — '생산길이 표준은 MDadaptive-v2(2026-08-27)로 대체 · 무엇이 인용 가능한지는 md_axis_status_2026_09_07 §1·§1.5'. §1 표의 production 칸은 '≥50 ps(창 하한) / 표준 판정은 MDadaptive-v2', friction 은 0.02 로 고정(CLAUDE.md 규율과 일치). 이 세 편은 어차피 한 묶음이니 파일명 앞에 `md_` 접두를 유지해 붙어 보이게 둔다.
- codex 필요: False

### [P1·buried] cascade-anatomy-append-log
- **어디**: `kb/methodology/cascade_pipeline_anatomy_2026_08_13.md (1257줄, 상단 요약 :18 / 정정 :503,:700,:948)`
- **근거**: 이 폴더 최대 문서. 최상위 절 26개가 08-13 → 08-19 로 시간순 append 됐고 별표가 계속 늘어난다(`## ★ ...` → `## ★★ ...` → `## ★★★ ...` → `## ★★★★ 전수 정독 (2026-08-19)`). 자기정정이 본문 한가운데 묻혀 있다 — L503 `## ⛔⛔ G4 의 blocking 은 도펀트 **원자 수 프록시**다 (2026-08-14 새벽, 앞 절 정정)`, L700 `## ★★★ 릴리스 감사 라운드 2 — Codex 재감사 반영 + **내 오류 하나 철회** (2026-08-14 저녁)`, L948 `## ★★★ G3 가 닫혔다 — method-comparable 0 → 270/270 (2026-08-16)`. 그런데 상단 `## 요약`(L18)과 frontmatter `status: 확정 — 원인 특정됨 (ESW 배치 커버리지). 회수 경로 있음` 은 08-13 판이라 그 정정들을 하나도 안 담는다. 위에서 아래로 읽는 사람(=LLM)은 500줄을 지나야 정정을 만난다.
- **고치는 법**: 요약(L18)을 '08-13 최초 판정 + 08-14 정정 2건 + 08-16 G3 닫힘' 으로 다시 쓰고, 각 정정 절로 가는 앵커를 요약에 건다. 정정 절 원문은 삭제하지 않는다(이력). 길이가 계속 늘 거면 08-14 이후분을 `cascade_pipeline_anatomy_appendix_2026_08.md` 로 분리하고 본편은 200줄 이하로 유지.
- codex 필요: False

### [P1·stale] cascade-cards-hide-hold
- **어디**: `kb/methodology/cascade_composition_family_2026_08_16.md · cascade_design_contract_2026_08_28.md · cascade_rerank_runbook_2026_08_25.md · microstructure_ml_transfer_to_cascade_2026_08_25.md`
- **근거**: cascade 는 2026-08-30 회신 AL NO-GO 로 hold 중이다(cascade_lessons_transfer_2026_09_08.md 서두: `cascade 는 회신 AL(2026-08-30) NO-GO 로 멈춰 있다. 해제조건 8개 중 #2 의 절반(어닐 RNG 봉인)만 끝났다`). 그런데 `grep -c "NO-GO\|회신 AL\|hold"` 결과가 composition_family 0 · design_contract 0 · rerank_runbook 0 · microstructure_ml 0 이다(pipeline_anatomy 는 2건이지만 08-14 의 다른 맥락). rerank_runbook 은 frontmatter `status: ①~⑤완료` 인데 본문 L20 은 `> ✅ **착수 조건 충족 (2026-08-25 20:58)** — AlI₃ x020/x050/x100 완주 (rc=0). ① 진행 중.` 로 자기모순.
- **고치는 법**: cascade 5편 전부 상단에 같은 한 줄 배너 — 'cascade 축은 회신 AL(2026-08-30) NO-GO hold. 해제조건 8개 · 현황은 cascade_lessons_transfer_2026_09_08.md §1 · 보고량은 cascade_d_rel_estimand_2026_09_08.json'. rerank_runbook 본문 L20 의 '① 진행 중' 은 frontmatter 와 맞춘다. 더 나은 형태는 MD 축처럼 `cascade_axis_status_<날짜>.md` 한 장을 만들고 5편을 거기서 색인하는 것이다.
- codex 필요: False

### [P1·buried] adhesion-published-convention-buried
- **어디**: `kb/methodology/adhesion_energy.md:165,206 (247줄)`
- **근거**: 실제로 인용해야 하는 절이 맨 아래다 — L206 `## ★ PUBLISHED CONVENTION — paper #1 (v30u binding curves) [2026-07-21 박제]` 이고 그 안에 `**이 관례로 논문이 이미 출판/제출됨. paper #2 등 후속 인용은 반드시 동일 관례를 따를 것.**` 이 있다. 그 위 200줄은 2026-04 디버깅 로그(`### v5 FIX: ASE atom slicing error (2026-04-12)`, `### v5 Wad Debugging Saga (2026-04-13)`)이고, L165 는 아직도 `### v5_xyshift (2026-04-13, CURRENT)` 라고 자칭한다 — 다섯 달 전 프로토콜이 'CURRENT' 로 남아 출판 관례와 충돌한다. 같은 절에 `Running on V100.` 같은 그날의 실행 상태도 그대로다.
- **고치는 법**: PUBLISHED CONVENTION 절을 문서 맨 위로 올리고, L165 의 `CURRENT` 를 `(2026-04-13, superseded by PUBLISHED CONVENTION 2026-07-21)` 로 바꾼다. 04-12~13 디버깅 사가(vacuum 30 Å vs 60 Å 10배 사고 포함)는 재현에 필요하니 '이력' 절로 내려 접는다 — 지우지 않는다.
- codex 필요: False

### [P1·wrong] elastic-card-all-deprecated
- **어디**: `kb/methodology/elastic_constants.md:4,20`
- **근거**: L4 `Two approaches: DFT 0K clamped-ion (ordered) vs MLIP 600K snapshot (disordered).` — 그 두 방법이 **둘 다 폐기됐다**. L6 이 스스로 적는다: `**UPDATE 2026-07-23:** DFT relaxed-ion (comp1 22.06 GPa)이 paper 정본. 600K MLIP elastic은 2026-07-23 db/properties/elastic.json에서 제거됨 (deprecated).` L20 `## MLIP 600K Snapshot Method (DEPRECATED — removed 2026-07-23)`. 그런데 **정본인 relaxed-ion 프로토콜의 절이 이 카드에 없다** — 절차는 computational_methods_canonical.md §2(`DFT relaxed-ion stress-strain, 12 SCF = 6 Voigt × ±h`)에만 있다. 즉 'Elastic Constants Calculation' 이라는 이름의 카드가 폐기 두 방법의 상세만 담고 있다.
- **고치는 법**: 맨 위에 '정본 = DFT relaxed-ion stress-strain(computational_methods_canonical.md §2) · clamped-ion 은 comp1 기준 2.4배 과대 · MLIP-600K 는 2026-07-23 제거' 를 놓고, relaxed-ion 절차를 여기로 옮기거나 §2 로 명시 위임. Basin A/B 표와 600K 표는 이력으로 접어 남긴다(문헌 앵커가 붙어 있어 값 자체는 쓸모 있다).
- codex 필요: False

### [P1·ia] handoff-in-methodology
- **어디**: `kb/methodology/handoff_2026_08_20_night.md`
- **근거**: 내용이 그날 밤 상태다 — `## 밤새 도는 것 (gabia, 전부 정상)`, `ETA ~2 h`, `GPU 여유 3.4 GB — **새 작업 추가 금지.**`, `## 내일 주제 \n\n연구세미나. ... **8–12장은 아직 안 봤다** (사용자가 보내주기로).` frontmatter 는 `status: 진행` 이고 lint 가 `status '진행' 인 채 19일` 로 잡고 있다. 같은 종류 문서는 전부 kb/projects 에 있다 — HANDOFF_2026_08_31_session.md · handoff_2026_09_03_zn_nd.md · restart_runbook_2026_09_07.md. 이 한 편만 methodology 에 있다.
- **고치는 법**: kb/projects/ 로 옮기고 status 를 '종료(2026-08-20 야간)' 로 닫는다. 그 안에서 아직 살아있는 판정 3건(comp1 2×2×2 밴 해제 · gap 방법 플래그 하향 · NEB 밴드 협동이동)은 각각 kb/results 카드로 이미 있는지 확인하고 없으면 옮겨 심는다. index 재생성 필수.
- codex 필요: False

### [P1·ia] estimand-cards-scattered
- **어디**: `kb/methodology/zn_cu_hull_estimand_2026_09_03.md · db/properties/*_estimand_*.json · kb/questions/sdcp_*_estimand_*.md`
- **근거**: 같은 종류(보고량 카드)가 세 군데에 세 형식으로 있다. kb/methodology 1편(zn_cu_hull_estimand_2026_09_03.md, `## 보고량 카드 — Cu–Zn convex hull`), db/properties JSON 9편(cascade_d_rel_estimand_2026_09_08 · lpsocl_box331_estimand_2026_08_30 · b2o3_uma_vs_dft_force_prereg_2026_09_08 · sdcp_polaron_pilot_prereg_S0_2026_08_31 등), kb/questions 2편(sdcp_doped_estimand_2026_08_28 · sdcp_backbone_polaron_estimand_2026_08_31). 템플릿은 kb/templates/estimand_card.md 한 개. 목록·색인은 없다. 게다가 zn 카드는 status `제안` 인데 db/governance/decisions.json 22건 어디에도 zn·hull·alzib 문자열이 **없다**(전수 grep 0건) — CLAUDE.md 의 `보고량·마감 판정은 db/governance/decisions.json 에 등록한다 (proposed → 사람이 ratify 해야 active)` 를 못 지킨 상태로 5일째다.
- **고치는 법**: ① zn 카드를 decisions.json 에 proposed 로 등록(또는 비준). ② 보고량 카드의 정본 위치를 하나로 못박는다 — 결정 원장이 db/governance 라면 카드도 db/properties JSON 을 정본으로 하고 kb 쪽은 설명 카드로만 두되, 어느 쪽이든 `db/governance/decisions.json` 이 전 카드를 가리키게 한다. ③ kb/methodology 에 '보고량 카드 목록' 한 줄짜리 색인(카드 → 결정 ID → 상태)을 두면 다음 세션이 30초에 찾는다.
- codex 필요: False

### [P1·ia] flat-alphabetical-index
- **어디**: `kb/index.md:30-82 (methodology 52줄) · kb/methodology/ (README 없음)`
- **근거**: index 는 `## methodology/ (52)` 아래 알파벳 52줄이고 각 줄은 `- \`경로\` — 제목 [○미열람]` 뿐 — **날짜도 status 도 없다**. 그래서 2026-09-08 카드(cascade_lessons_transfer)와 2026-05-16 카드(external_review_response)가 구분 없이 섞이고, 이 축의 지도인 md_axis_status_2026_09_07 은 md_conductivity_protocol 과 microstructure_ml 사이 알파벳 자리에 묻힌다. frontmatter 25편 부재라 절반은 날짜를 붙이려 해도 못 붙인다. 폴더 안에 README·00_index 도 없다(`ls -a kb/methodology/ | grep -i readme` 0건).
- **고치는 법**: kb_wiki.py index 생성기를 고쳐 methodology 를 ① 축별(MD · cascade · 서버 · 도핑/Nd · 역학/접착 · repo 규율)로 묶고 ② 각 줄에 date·status 를 찍고 ③ 6개월 이상 손 안 댄 것은 '이력' 하위 접기로 내린다. index.md 는 생성물이니 손편집 금지 — 생성기를 고쳐야 한다. 축마다 md_axis_status 같은 '현황 한 장' 을 두는 게 최종형이고, MD 는 이미 있으니 cascade·SDCP 부터 만든다.
- codex 필요: False

### [P2·broken] broken-paths-3
- **어디**: `kb/methodology/PHASE1_QUICKSTART_doping.md · md_conductivity_protocol.md · modelC_v2_slab_fix.md`
- **근거**: `python3 tools/kb_wiki.py lint --legacy` 가 셋을 찍는다: `· kb/methodology/PHASE1_QUICKSTART_doping.md: kb/literature_db/raw.json`, `· kb/methodology/md_conductivity_protocol.md: db/properties/cage_jump_b2o3_vs_modelc.csv`, `· kb/methodology/modelC_v2_slab_fix.md: tools/build_ncm_interface.py`. 셋 다 실제로 없음(직접 확인). cage_jump CSV 는 §6.1 의 실행 예시 산출물인데 §6 전체가 SUPERSEDED 라 만들 계획도 없다.
- **고치는 법**: cage_jump CSV 줄은 SUPERSEDED 절 안이므로 `<!-- lint-skip-path -->` (미생성 예정 산출물) — SCHEMA 가 허용하는 용법이다. kb/literature_db/raw.json 은 구세대 디렉터리라 litdb 로 대체 표기. tools/build_ncm_interface.py 는 후신 도구를 찾아 경로 갱신, 없으면 '구세대 스크립트, 커밋 안 됨' 으로 skip 표시.
- codex 필요: False

### [P2·duplicate] quickstart-exact-duplicate
- **어디**: `kb/methodology/PHASE1_QUICKSTART_doping.md ↔ scripts/PHASE1_QUICKSTART.md`
- **근거**: `diff scripts/PHASE1_QUICKSTART.md kb/methodology/PHASE1_QUICKSTART_doping.md` → 출력 없음(완전 동일), 둘 다 125줄. 내용은 2026-05 초기 POC 가이드(`pip install atomate2[mlff,defects,phonons] pyalex ...`, `python3 scripts/doping/site_preference.py --dopant Mg --n 2`)라 지금 캠페인과 무관하다. 참고로 site_preference.py 는 scripts/doping/ 과 tools/doping/ 양쪽에 있다.
- **고치는 법**: 한 벌만 남긴다 — 실행 가이드니 scripts/ 쪽을 남기고 kb 쪽은 삭제하거나 한 줄 포인터로 대체. 지울 때 index 재생성. (도구 이중화 자체는 tools/ 담당 조사 몫이라 여기선 지적만.)
- codex 필요: False

### [P2·broken] russian-token-in-card
- **어디**: `kb/methodology/dopant_site_preference_literature.md:3`
- **근거**: L3 `> **NOT pure literature-grounded** — это literature-ANCHORED heuristic:` — 러시아어 `это` 가 섞여 있다. 문서 제목 줄 바로 아래 첫 문장이고, 이 카드는 도판트 자리 배정의 근거 등급(cited 14 / standard 15 / analogy 24)을 정하는 문서라 그 첫 줄이 제일 많이 인용된다.
- **고치는 법**: `это` → `이것은` (또는 영문 문장이니 `this is a`). 같은 유형이 더 있는지 한 번 훑기.
- codex 필요: False

### [P2·ia] server-card-names
- **어디**: `kb/methodology/kserver116_setup.md · esp_z590_setup.md`
- **근거**: 부르는 이름과 파일명이 다르다. CLAUDE.md 는 `**gabia** (A6000 단일 GPU ...): root@121.78.116.27` 와 `**kgy** (RTX3090, QE-GPU + uma env): ssh kgy@59.12.161.91` 로 부르는데, 파일은 `kserver116_setup.md`(= gabia, L3 `**Target host:** \`121.78.116.27\``)와 `esp_z590_setup.md`(= kgy, L3 `ssh \`kgy@59.12.161.91\``)다. esp 카드 안에서조차 상대를 'gabia' 로 부른다(L31 `rsync'd from gabia`, L141 `## Comparison vs gabia (kserver116-27)`). 파일명으로 찾으면 못 찾고 본문 grep 으로만 찾힌다.
- **고치는 법**: `server_gabia_a6000.md` · `server_kgy_rtx3090.md` · `server_kisti_neuron.md` 로 rename(별칭을 본문 첫 줄에 병기). rename 하면 lint 가 인바운드 경로 인용을 잡아주니 그때 같이 고친다. 세 편을 이름으로 붙여 두면 '서버' 묶음이 index 에서도 뭉쳐 보인다.
- codex 필요: False

### [P2·ia] frontmatter-half-missing
- **어디**: `kb/methodology/ 25/52 편 (adhesion_* · argyrodite_* · b2o3_* · beta_gate_seed_policy · coating_descriptor_catalog · computational_methods_canonical · dopant_* · doping_* · elastic_constants · electron_localization_* · eos_fitting · esp_z590_setup · esw_* · external_review_* · hard_dopant_* · kisti_setup · kserver116_setup · li_annealing · md_conductivity_protocol · modelC_v2_slab_fix · nd_vs_O_* · PHASE1_* · probe_language_reference · terminology_register)`
- **근거**: 52편 중 24편만 완전 frontmatter, 3편은 구식 부분 frontmatter(li3nd_metal_protocol_note · li_adatom_neb_protocol · site_preference_protocol — title/tags/date/status 만), 25편은 아예 없다. kb/SCHEMA.md 가 `**새 문서부터 필수. 기존 199개 소급 없음** (lint 는 frontmatter 있는 문서만 깊이 검사)` 라고 명시했으니 규율 위반은 아니다. 다만 그 결과로 index 가 절반은 날짜·status 를 못 찍고, 폐기된 규칙을 담은 카드들(beta_gate_seed_policy · electron_localization · computational_methods_canonical · terminology_register)이 전부 이 25편 안에 들어 있어 lint 의 status 신선도 검사망 밖에 있다.
- **고치는 법**: 전수 소급은 하지 않는다(SCHEMA 결정 존중). 대신 **위 P0/P1 에서 손대는 카드에 한해** 그 김에 frontmatter 를 붙인다 — 그러면 다음부터 lint 의 '진행인 채 N일' 검사가 그 카드들을 봐준다. 우선순위 5편: beta_gate_seed_policy · computational_methods_canonical · electron_localization_framework · terminology_register · md_conductivity_protocol.
- codex 필요: False
