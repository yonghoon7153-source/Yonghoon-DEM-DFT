# repo — tools/ (sdcp 61 · figures 88 · electronic 35 · oxidation 40 · sei 24 · neb_diffusion 32, + cascade 11 대조)

## 지금 무엇인가
tools/ 는 캠페인 실행·회수·그림 생산을 다 하는 526개 스크립트(py 305 · sh 106 · 62k줄, 26개 하위폴더)인데 README·색인이 **3개**뿐이고 그중 둘은 특정 레시피 문서다. 규율 준수는 폴더마다 갈린다 — sdcp/sei/oxidation/cascade 는 docstring 에 "못 하는 것"·selftest 가 붙어 있고(sdcp 18/61, cascade 7/11), figures 는 88개 중 selftest 6 · 한계 docstring 7 · house_style 34 로 가장 약하다. 내가 **내용을 실제로 열어 읽은 것은 46개** (sdcp 8 · figures 12 · neb_diffusion 10 · oxidation 9 · electronic 3 · sei 3 · doping 1), 나머지 480개는 이름·날짜·grep 패턴(house_style·selftest·db 경로·철회값·중복함수)으로만 훑었다. tools/doping(58)·ionic(40)·comp1_v3·modelc_v3·litdb·vgcf_hbn·xps·elastic·adhesion_v30u 는 이번 범위 밖이라 **안 봤다**.

## 처음 오는 사람
처음 오면 `tools/` 앞에서 멈춘다. 폴더 26개 중 어디가 살아 있고 어디가 닫힌 캠페인인지 알려주는 파일이 없고, 526개 중 kb 어디에도 이름이 안 나오는 것이 **338개**다. figures 는 더 심해서 87개 중 53개가 kb·docs·webapp 어디에도 안 나온다 — "이 그림 누가 만들었나"를 물으면 grep 밖에 답이 없고, 파일명(plot_cascade.py / plot_cascade2.py / plot_cascade3.py / plot_cascade_summary.py / plot_cascade_v23.py / plot_cascade_deep.py …16개)이 뭐가 최신인지 말해주지 않는다. 막히는 지점은 셋이다 — ① 캠페인 마감이 db/properties 의 `*_closed_*.json` 에만 있고 도구 쪽엔 표시가 없어서 닫힌 phaseA/B 도구를 살아 있는 것으로 읽는다 ② `citation_hazards.json`(철회·보류 정본)을 읽는 도구가 webapp 뿐이고 그림 생산 88개는 하나도 안 본다 ③ 같은 이름 다른 물건(`extract_gap.py` ×2, `site_preference.py` ×2)이 있어서 grep 결과가 답을 안 준다. 반대로 **한 파일만 열면 이해되는 것**도 있다 — `tools/sdcp/site_screen.py`·`tools/sei/qe_env.sh`·`tools/electronic/run_gap_nscf_gabia.sh` 는 왜 이렇게 생겼는지를 사고 이력으로 다 적어 놨다.

## 건드리면 안 되는 것
- **docstring 의 '이 도구가 못 하는 것' 절 — 절대 지우지 말 것.** sdcp 18건 · sei 9건 · cascade 7건 · oxidation 7건에 있다. 예: run_force_check_scf.sh "수렴을 보장하지 않는다 — 실패한 점을 세어 보고할 뿐이고, 실패를 대체하지 않는다", fig_sei_neb_paths.py "값의 인용 자격을 만들지 않는다. 세 경로 전부 citable: false 다", vasp_handoff_bundle.py "UMA 값과 같은 표에 놓을 수 없다 (프로토콜이 다르다)". 이게 repo 에서 가장 비싼 자산이고 LLM 이 기억을 되찾는 유일한 손잡이다.
- **사고 이력 주석 — 짧게 줄이지 말 것.** tools/sei/qe_env.sh(⛔⛔ 2026-09-01 kgy 사고 · 2026-09-03 nvhpc 2차 사고), tools/doping/run_force_check_scf.sh(ldd 3연속 오진), tools/sdcp/site_screen.py(하자 5개 ①~⑤), tools/neb_diffusion/li3n_seeded_neb.py(v1/v2a/v2b 실패 계보), tools/electronic/run_gap_nscf_gabia.sh(정본 실행본 소실 경위 + 계보 확인 훅 'QE 가 다른 수를 찍으면 셋업이 정본과 다르다'). 이걸 요약하면 같은 사고를 다시 친다 — repo 가 이미 세 번 증명했다.
- **tools/sei/qe_env.sh 의 '없는 경로는 export 하지 않는다' 원칙과 그 음성 selftest 3건.** ldd 기준으로 승격하더라도 이 원칙과 selftest(①양성 ②없는 경로 배제 ③비-OpenMPI 런처면 물려받은 OPAL_PREFIX 제거)는 그대로 남겨야 한다. 이게 없으면 kgy·gabia 를 오가는 순간 다시 죽는다.
- **tools/convention_check.py 와 그 EXEMPT 5건.** 현재 0 위반이다(kB 상수 경고 11건은 상대차 1e-7 로 무해). 물리 규약(MSD 창 2–50 ps · 자유절편 D)이 여러 파일에 복사돼 있는 걸 감시하는 유일한 장치다.
- **tools/figures/house_style.py 의 DISP/DISP_LONG 표기 통일 결정.** "그림마다 LPSOCl / LPSOCl1.6 / 'LPSOCl (Li27P5S21OCl8)' 로 갈려 있었다 … 데이터 쪽에 맞춘다" — 2026-08-06 에 닫은 항목이다. 그림 재편 중에 표기를 다시 흔들면 CSV 열 이름과 범례가 또 갈린다.
- **닫힌 캠페인 도구를 삭제하지 말 것** (tools/sdcp phaseA/B 계열 16개, plot_neb_topview v1/v2, plot_cascade{,2,3}.py). 마감 원장(sdcp_*_closed_2026_08_28.json)이 '재개 조건'을 걸어 두었고, 철회된 그림도 '무엇이 왜 틀렸나'의 증거다. 배너·SUPERSEDED 표시로 접되 파일은 남긴다. 단 하나 예외 — docs/figures/cascade/cascade_conc_trends.png 은 **배포 경로에 있는 틀린 그림**이라 내려야 한다(스크립트는 남긴다).
- **citation_hazards.json / canonical_registry.json 을 그림 쪽 편의를 위해 단순화하지 말 것.** status 값 6종(canonical/provisional/superseded/source_pending/non_citable/…)과 comparison_group·protocol_generation(R9) 규칙은 각각 실제 사고에서 나왔다(2026-08-07 Codex 4라운드 · 2026-09-07 BH P0-1). 그림 도구가 여기에 붙어야지, 이쪽이 그림에 맞춰 내려오면 안 된다.
- **tools/sdcp/vasp_handoff_bundle.py 를 지금 쪼개지 말 것.** v40 까지 온 계보와 MANIFEST.files_sha256 무결성, 봉인·재개 조건 평가가 이 파일 안에서 맞물려 있다. 목차·`--map` 같은 읽기 보조부터 붙이고, 구조 수술은 외주 회차가 끝난 뒤에 한다.

## 발견

### [P0·wrong] cascade-conc-axis-fake
- **어디**: `tools/figures/plot_cascade3.py:3,20,22 → docs/figures/cascade/cascade_conc_trends.png (실물 존재)`
- **근거**: 스크립트: `X={'x002':0.02,'x005':0.05,'x010':0.10}` · `a.set_xlabel('dopant fraction x') … a.set_xticks([0.02,0.05,0.10])` · `plt.suptitle('M3+ cascade: concentration trends (x=0.02/0.05/0.10, UMA)')`. 그런데 kb/methodology/cascade_pipeline_anatomy_2026_08_13.md:409 는 **"47종 캠페인은 전부 x = 0.25 에서 돌았다 (의도는 2·5·10%, 슈퍼셀 버그로 0.25 고정)"**, 350행 "x002/x005/x010 이 전부 x=0.25 로 뭉개진 그 버그", 656행 P0-6 "x=0.05 가 아니라 x=0.25 | champions csv concentration 전부 0.25". 같은 폴더의 tools/figures/plot_cascade_v23.py:12-14 도 스스로 적어 놨다 — "the dir x002/x005/x010 are PLACEMENT REPLICATES at x=0.25, NOT a concentration sweep". 즉 세 패널 전부가 **존재하지 않는 농도축**이고, 그림은 2026-06-15 자로 docs/figures/cascade/ 에 살아 있다.
- **고치는 법**: cascade_conc_trends.png 를 배포 경로에서 내리고, plot_cascade3.py 상단에 철회 배너("x002/x005/x010 = x=0.25 배치 반복 · 농도축 아님, 근거 kb/methodology/cascade_pipeline_anatomy_2026_08_13.md:409")를 박거나 파일을 archive/ 로 옮긴다. 농도 응답이 필요하면 kb 가 가리키는 `dualx_v23`(actual_x 0.0625/0.25 실측)로 다시 그린다. plot_cascade.py·plot_cascade2.py 도 같은 세 키를 쓰지만 2는 best_by_dE 로 대표 1행만 뽑아 **반복으로 취급**하므로 축 라벨만 확인하면 된다.
- codex 필요: False

### [P0·wrong] sdcp-dextract-retracted-live
- **어디**: `tools/sdcp/site_screen.py:14 · :607 (마지막 커밋 2026-09-02, 철회는 2026-08-28)`
- **근거**: 607행 docstring: "VASP dE_extract = +0.336 eV(2026-08-08) **로 추출이 열역학적으로 불리함이 확인됐으므로**, 추출형 끝점은 결합 순위에서 빼고 따로 센다." 14행도 같은 값을 반증 근거로 쓴다. 그런데 db/properties/citation_hazards.json 의 sdcp_phaseB_dftu_v1 항목(updated 2026-08-31)은 정반대다 — "⛔ **아무것도 인용하지 않는다.** 종전 fix 였던 'dE_extract(+0.3356 eV)만 인용' 은 틀렸다 — sdcp_doped_closed_2026_08_28.json(active·ratified)이 회신 P P0 로 그 추출 부호를 **철회**하고 citable:no 로 강등했다". 마감 원장 본문도 같다: "⛔ 2026-08-28 회신 P 2번 P0: 종전 '추출 부호(+0.34, Li 추출 열역학적으로 불리)' 인용은 **철회**. 두 endpoint 가 총자화 2.378/0.518 로 자기상태가 다르고 … basin 최소 동등성이 미입증". 즉 **철회된 해석이 스크리닝 엔진의 판정 규칙 근거로 살아 있다.**
- **고치는 법**: 두 곳의 문장을 "두 labeled endpoint 의 단일점 차 ≈ +0.34 eV (citable:no · 자기상태 2.378/0.518 μB 불일치, basin 동등성 미입증 — 열역학 부호로 읽지 않는다)" 로 교체하고, 추출형 격리 규칙의 근거를 **부호가 아니라 기하 판정**(표면 Li 변위·배위 이전, 같은 함수가 이미 재는 것)으로 다시 쓴다. sdcp_doped_closed_2026_08_28.json 의 `허용_서술_이대로만` 문구를 그대로 인용한다.
- codex 필요: False

### [P1·wrong] li3n-uma-ban-vs-protocol
- **어디**: `tools/neb_diffusion/li3n_pes_uma.py:2 · li3n_figset.py:9-12 · li3n_seeded_neb.py · li3n_uma_investigate.py ↔ CLAUDE.md ↔ kb/methodology/li_adatom_neb_protocol.md:187,201-206`
- **근거**: CLAUDE.md: "**UMA는 Li₃N에 사용 금지** (2026-06 결정론적 편향 판정)". kb 카드 187행도 더 세게 적었다 — "**Li3N 장벽은 UMA로 불가** … **UMA를 path-finder로도 쓰면 안 됨**(hollow 오도)". 그런데 같은 카드의 2026-07-09 UPDATE 절은 반대로 간다 — "확보한 것 (UMA, kserver116): 12×12 구속 PES(`li3n_pes_uma.py`) → minimax MEP **barrier 0.156 eV**" 이고 표에 "구속 PES-격자 | Li₃N ✅ 0.156/0.171 eV (측정 MEP)" 로 **합격 도장**이 찍혀 있다. 도구 쪽은 그 어느 쪽도 모른다 — li3n_pes_uma.py docstring 은 "UMA 2D relaxed PES for the Li adatom on Li3N(001)" 로 시작해 금지 규율을 한 줄도 언급하지 않고, li3n_figset.py 는 `E_ads(site) = E(slab+Li@site) − E(bare slab) − E(Li atom)` 를 UMA 로 계산해 그림 패널 (a) 로 낸다. 세 도구 다 금지 판정(2026-06) **이후**인 2026-07-08/09 에 마지막으로 손댔다.
- **고치는 법**: 금지의 **범위**를 1저자가 한 줄로 확정해야 한다(장벽 절대값만 금지인가, 구속 PES 도 금지인가, 기하 정찰은 허용인가). 확정 뒤 ① CLAUDE.md 한 줄에 예외를 명시하거나 ② kb 카드 2026-07-09 절에 "CLAUDE.md 금지의 예외 — 근거" 를 박고 ③ li3n_*.py 네 개 docstring 상단에 그 판정을 복사한다. 어느 쪽이든 도구가 규율을 모른 채 남아 있으면 안 된다.
- codex 필요: True

### [P1·stale] kgy-hpcx-autodetect
- **어디**: `tools/electronic/run_comp2_saddle_check_kgy.sh:84-88`
- **근거**: 파일 이름이 `_kgy` 인데 본문은 `NV="$HOME/apps/nvhpc/Linux_x86_64/24.11"` · `HPCX="$(ls -d "$NV"/comm_libs/*/hpcx/hpcx-*/ompi … | tail -1)"` · `export OPAL_PREFIX="$HPCX"` · `MPIRUN="$HPCX/bin/mpirun"` 다. CLAUDE.md 2026-09-08 항목이 이걸 정확히 세 번째 오진으로 적어 놨다 — "③ hpcx 를 자동탐지했는데 kgy 의 pw.x 는 **`~/apps/openmpi-4.1.6`** 로 빌드돼 있었다 (hpcx 에서 오는 건 scalapack 뿐). 머신마다 다르므로 규칙이 아니라 링크가 근거다." 정답 구현은 tools/doping/run_force_check_scf.sh 의 `_setup_mpi_from_binary()`(`ldd "$PWX" | awk '/libmpi\.so/'`)에 이미 있다. tools/sdcp 의 gabia 러너 6개(run_phaseB_{gabia,refine_gabia,slabfirst_gabia,vertical_gabia,sdcp_v2,sdcp_v3}.sh)도 hpcx 절대경로 하드코딩이지만 그쪽은 gabia 전용이라 지금 당장 틀린 것은 아니다.
- **고치는 법**: run_comp2_saddle_check_kgy.sh 의 MPI 블록을 tools/doping/run_force_check_scf.sh 의 `_setup_mpi_from_binary()` 호출로 갈아끼운다(못 읽으면 시작 안 함까지 그대로). 더 나은 정리는 그 함수를 tools/sei/qe_env.sh 안으로 옮겨 `_qe_env_apply` 의 ②단계(현재는 **mpirun 트리**에서 유도)를 **pw.x 의 ldd** 기준으로 승격시키고, 두 러너가 같은 파일을 source 하게 하는 것이다.
- codex 필요: False

### [P1·stale] bundle-version-v3-in-manifest
- **어디**: `tools/sdcp/vasp_handoff_bundle.py:15356 (+ 1-8행 docstring)`
- **근거**: 외주처가 받는 MANIFEST.json 에 `"bundle_version": "v3"` 가 하드코딩돼 있다. 파일 상단 docstring 도 "VASP 외주 **원샷** 번들 v3 … v2 → v3 (2026-08-12)" 에서 멈춰 있다. 정작 본문은 훨씬 앞서 있다 — 1096행 "2026-09-08 (Codex v38 P1-2)", 1609행 "2026-09-07 Codex v37 P0-1", 1988행 "Codex v39 P1", 5772행 "v34 분석기는…", 그리고 작업기록 #27 이 "v40 재생성 + IDENTITY_v40 + SEND_MAIL_v40" 다. 즉 같은 zip 안에서 폴더명·IDENTITY·메일은 v40 을 말하고 MANIFEST 는 v3 을 말한다. 작업기록 #4 가 "bundle_version v34 표기" 를 완료로 적었지만 이 상수는 안 바뀌었다.
- **고치는 법**: `bundle_version` 을 상수에서 빼고 `out_final.name` 에서 파생시키거나(폴더명이 이미 sdcp_c12_v40), 최소한 IDENTITY_v40 이 MANIFEST.bundle_version 과 일치하는지 selftest 에 음성 케이스로 넣는다. docstring 첫 줄도 현재 판으로 올린다 — 22,785줄 파일에서 사람이 읽는 건 앞 50줄뿐이다.
- codex 필요: False

### [P1·missing] tools-no-index
- **어디**: `tools/ (전체) — md 파일은 adhesion_v30u/README.md · electronic/gabia_cdd_phx.md · figures/vesta_3d_isosurface_recipe.md 3개뿐`
- **근거**: 실측: tools 하위 py+sh 526개, 그중 kb/ 어디에서든 경로로 이름이 불리는 것은 **188개**(`grep -rho "tools/[a-z_0-9]*/[a-zA-Z_0-9.]*\.\(py\|sh\)" kb/ | sort -u | wc -l`). 338개는 kb 에서 보이지 않는다. CLAUDE.md 코드 규율은 "새 스크립트 쓰기 전 기존 것부터 찾는다 … ② tools/ 에 이미 있나(`grep -rl`)" 를 사다리 2단으로 못 박았는데, **이름을 모르면 grep 이 안 된다.** 실제로 중복이 생겼다 — `extract_gap.py`(electronic/standard_dos, sei) · `site_preference.py`(doping, sdcp) 두 쌍.
- **고치는 법**: 폴더당 한 줄짜리 `tools/<dir>/README.md`(무엇을 하는 폴더 · 살아 있는 진입점 3~5개 · 닫힌 캠페인 표시 · 정본 도구 이름)와 tools/INDEX.md 를 `kb_wiki.py` 처럼 **생성**한다(손편집 금지). 최소판은 각 파일의 docstring 첫 줄 + 마지막 커밋 날짜 + kb 참조 유무를 표로 뽑는 것이고, 그 자체가 "kb 에 안 실린 338개" 목록이 된다.
- codex 필요: False

### [P1·missing] figures-no-registry
- **어디**: `tools/figures/ (87 py) ↔ docs/figures/ (71 항목)`
- **근거**: 87개 중 **53개**가 kb/·docs/·webapp/ 어디에도 이름이 안 나온다(annot_bvse_arrows.py, fig_comp2_{arrhenius,cohp,conductivity,halide_lengths,icohp,msd}.py, plot_cascade{,2,3,_branches,_deep,_errorbars,_extra,_interactions,_litransport,_summary,_synergy,_v23,_v23_detail}.py, plot_icohp_{bars,compare}.py, plot_nd_dos_v2.py …). 반대 방향도 없다 — docs/figures/ 의 유일한 안내인 README.md(2026-06-11, 15줄)는 `slide05_dos_pdos`·`slide06_bvse_5x5x5` 두 폴더의 v100 컨테이너 경로만 적고 있는데 지금 그 폴더는 71개 항목 중 둘이고 `slide09_arrhenius` 는 README 에 없다. 원고 Figure 번호 ↔ 스크립트 대응표는 어디에도 없다.
- **고치는 법**: figures 스크립트마다 docstring 에 `Outputs:` 를 강제하고(이미 fig_* 계열은 대부분 갖고 있다), 그걸 긁어 `docs/figures/INDEX.md`(그림 파일 → 만든 스크립트 → Origin CSV → 원고/슬라이드 어디에 쓰였나)를 생성한다. docs/figures/README.md 는 그 생성물로 대체한다(현행 15줄은 삭제 대상).
- codex 필요: False

### [P1·missing] figures-bypass-hazard-registry
- **어디**: `tools/figures/*.py (88개 전부) ↔ db/properties/citation_hazards.json`
- **근거**: `grep -rln citation_hazards tools/ webapp/` 결과: tools 쪽은 tools/reports/gabia_august_evidence.sh · tools/cascade/build_cascade_audit_manifest.py **둘뿐**이고 나머지는 전부 webapp/(data.py·canonical.py·governance.html·tests). 즉 화면은 철회·보류 원장을 보는데 **그림 생산 라인은 안 본다.** citation_hazards.json 에는 BLOCKED 5건·HOLD 2건·PREVIEW 1건·CONDITIONAL 10건이 들어 있고(예: lpsocl_md_arrhenius.json Ea = HOLD "확산영역 β 게이트 미통과", sei_neb.json = 전량 철회) figures 는 그 값들을 db/properties 에서 직접 읽어 그린다. 잘 쓴 반례가 있다 — fig_sei_neb_paths.py 는 docstring 에 "세 경로 전부 `citable: false` 다 … 그림에 그 사실을 각주로 박는다" 를 **손으로** 적었다. 손으로 적은 것은 다음 그림에서 빠진다.
- **고치는 법**: house_style.py 에 `hazard_note(ax, source_files=[...])` 같은 한 함수를 추가해 citation_hazards.json 을 읽고 해당 파일이 BLOCKED/HOLD/PREVIEW 면 캡션 각주를 자동으로 박거나(CONDITIONAL) 아예 예외를 던지게(BLOCKED) 한다. 이미 house_style 을 import 하는 34개가 공짜로 게이트를 얻는다.
- codex 필요: False

### [P1·broken] origin-csv-orphan-and-dup
- **어디**: `db/properties/*_origin.csv (48개) — 특히 li3n_barrier_origin.csv vs li3n_barrier_fig_origin.csv · li3n_eads_origin.csv vs li3n_eads_manuscript_origin.csv`
- **근거**: 48개 중 **15개**는 파일명이 tools/ 어디에서도 안 나온다 = 재생성 경로가 없다(b2o3_eos_origin.csv, b2o3_pmf_{cluster,profile,segments}_T600_origin.csv, beta_vs_seed_spread_origin.csv, bvse_channel_volume_orig_origin.csv, li3n_{barrier,eads,sites}_origin.csv, lpsocl_bond_lengths_origin.csv, modelc_pmf_*_origin.csv, msd_4sys_origin.csv, msd_modelc_lpsocl_200ps_origin.csv). 그중 li3n 쌍은 더 나쁘다 — 고아 `li3n_barrier_origin.csv`(2026-07-15, 14.6 KB)의 열 머리가 `xi,Li3N_guide_eV,LiC6_DFT_eV,…` 로 **`guide`(안내 곡선)** 인데 파일명은 Origin 납품물 관례를 그대로 쓰고 있다. 현행본은 fig_li3n_barrier_v2.py 가 내는 `li3n_barrier_fig_origin.csv`(2026-07-17, 754 B, `series,x_xi_or_site,energy_eV,status`)다. 어느 쪽이 최신인지 파일만 보고는 알 수 없다.
- **고치는 법**: ① 고아 15개는 헤더에 `# SUPERSEDED_BY: <현행 csv> · 생성도구 없음(재생성 불가)` 주석을 달거나 db/properties/_archive/ 로 내린다. ② `Li3N_guide_eV` 처럼 합성 곡선이 든 csv 는 `_origin.csv` 이름을 쓰지 않는다(그 접미사가 "Origin 에 그대로 넣어도 된다"는 뜻이므로). ③ CLAUDE.md 의 "Origin-ready CSV를 동시 출력해 db/properties/에 등록" 의 '등록'을 실체화한다 — csv → 생성 스크립트 → 열 정의를 담은 한 파일(db/properties/origin_csv_index.json)을 생성물로 둔다.
- codex 필요: False

### [P1·stale] sdcp-closed-campaign-unmarked
- **어디**: `tools/sdcp/ — run_phaseB_{vertical_gabia,refine_gabia}.sh · make_phaseB_vertical.py · watch_{umascan,pbrefine}.sh · watch_phaseA_rescan.py · watch_phaseB.py · uma_hydroxyl_screen.py · build_ptfe_{c10f22,dimer_c4h2f8}.py 외`
- **근거**: sdcp 61개 중 **16개**가 repo 어디에서도(다른 스크립트·kb·docs) 이름이 안 불린다. 그중 8개는 2026-07-12~2026-08-06 사이의 phaseA/B 시절 것이다. 그런데 그 캠페인은 db/properties/sdcp_neutral_closed_2026_08_28.json · sdcp_doped_closed_2026_08_28.json 로 **닫혔고**(status_history: "재-ratify … 이 시점부터 금지 서술이 다시 구속력을 가진다 — doped 흡착 수치·추출 열역학 부호는 어디에도 나가지 않는다"), tools/sdcp 안에는 그 사실을 말하는 파일이 하나도 없다. watch 스크립트만 9개(watch_gabia_sdcp / umascan / pbrefine / phaseA_rescan / phaseB / site_screen / stage_a / polaron_pilot / n6)가 한 폴더에 있고, 살아 있는 것은 뒤의 셋뿐이다.
- **고치는 법**: tools/sdcp/README.md 한 장에 ① 살아 있는 진입점(c12_* · vasp_handoff_bundle · site_screen · afm_ledger · watch_{n6,stage_a} · reseal_polaron_S0) ② 닫힌 캠페인 도구와 그 마감 원장 경로 ③ 그래도 지우면 안 되는 이유(재현·감사)를 적는다. 파일은 지우지 말고 phaseA/B 도구 docstring 상단에 `⛔ 닫힌 캠페인 — db/properties/sdcp_*_closed_2026_08_28.json` 한 줄만 박는다.
- codex 필요: False

### [P1·ia] oxidation-results-outside-db
- **어디**: `tools/oxidation/esw_llzo_result.txt · esw_nd_result.txt · esw_nd_doped.json · interface_reactivity_nd.json · sei_product_gaps.json`
- **근거**: 결과 5건이 tools/ 안에 있고 db/properties 에 같은 이름이 **하나도 없다**(전수 확인). 내용은 인용 가능해 보이는 수치다 — esw_llzo_result.txt: "↑ oxidation (anodic) limit ≈ 2.88 V" · "Same method/hull as our LPSCl comp1 (onset 2.256 V) → directly comparable"; esw_nd_result.txt: "oxidation (anodic) limit ~ 1.92 V" + 21 breakpoints; sei_product_gaps.json: "Li3PO4 … band_gap_MP_eV: 5.728". db/properties 밖이라 canonical_registry.json 에도 citation_hazards.json 에도 안 걸리고, `prohibitions`·`comparison_group` 같은 기계 판독 가드가 붙지 않는다. sei_product_gaps.json 의 갭은 MP PBE 소환값인데 CLAUDE.md 밴드갭 규율(fixed-occ nscf 만)과 같은 표에 올라갈 위험이 있는 형태다.
- **고치는 법**: 다섯 개를 db/properties/ 로 옮기고(경로가 도구에 박혀 있으면 같이 고친다) canonical_registry 에 `status: literature`/`comparison_group` 을 달거나, 최소한 citation_hazards 에 CONDITIONAL 항목을 만든다. tools/ 밑에는 selftest 픽스처 외의 결과 파일을 두지 않는다는 규칙을 CLAUDE.md 코드 규율에 한 줄 추가한다.
- codex 필요: False

### [P1·duplicate] figures-copypaste-helpers
- **어디**: `tools/figures/ — `_csv()` ×15 · `read_cube()` ×4 · `elf_cmap()` ×4 · `parse()` ×5`
- **근거**: 동일 본문 해시로 검출: `_csv()` 8줄이 fig_cascade_radar.py · plot_cascade_{branches,deep,errorbars,esw,extra,interactions,litransport,oxidation_vs_banik,seminar_47,summary,synergy,v23,v23_detail}.py · plot_cascade_audit_2026_08.py **15개 파일**에 글자 그대로 있다(같이 딸려 온 `CASCADE_SUFFIX`/`CASCADE_FIGDIR` 회수 shim 주석도 14개 파일에 통째로 복사돼 있다 — "2026-08-14 회수분(90종) 병렬 생성 shim"). `read_cube()` 18줄은 elf_licl_montage.py · plot_elf_{licl,plane,profile}.py 에, `elf_cmap()` 6줄은 elf_licl_montage.py · plot_elf_{clean,licl,plane}.py 에 있다. CLAUDE.md 코드 규율이 정확히 이걸 경고한다 — "tools/ 에 py 305 · sh 106 · 62k줄 — **중복이 진짜 위험**", "기존 도구 확장이 새 파일보다 항상 낫다".
- **고치는 법**: `_csv()`+접미사 shim, `read_cube()`, `elf_cmap()` 을 house_style.py(또는 figures/_io.py)로 올리고 15개 파일은 import 로 바꾼다. 지금은 접미사 규칙 하나를 고치려면 15군데를 고쳐야 하고, 갈라지면 아무도 모른다(이미 plot_cascade_audit_2026_08.py 만 house_style 도 같이 쓰는 비대칭이 있다).
- codex 필요: False

### [P1·duplicate] extract-gap-two-tools
- **어디**: `tools/electronic/standard_dos/extract_gap.py ↔ tools/sei/extract_gap.py`
- **근거**: 이름이 같고 목적도 같은데 보증이 다르다. sei 판: "⚠⚠ 이것이 갭의 **정본**이다. DOS 문턱으로 읽으면 … ~0.3 eV 과소평가된다 (CLAUDE.md 규율)" + `import electronic_class as EC # 금속/절연체 단일 출처` + "★★ 2026-08-11 — 금속으로 선언된 상은 **갭을 db 에 쓰지 않는다**" + JSON 출력. electronic 판: QE 출력에서 `highest occupied, lowest unoccupied level` 한 줄을 정규식으로 긁어 print 하는 20줄짜리로, 금속 가드도 json 도 없다. `grep -rl extract_gap` 을 하면 둘이 나오는데 어느 쪽이 정본인지 파일이 말하지 않는다.
- **고치는 법**: sei/extract_gap.py 를 정본으로 선언하고 electronic/standard_dos/extract_gap.py 는 얇은 래퍼로 바꾸거나 docstring 첫 줄에 "⛔ 진단용 · 정본은 tools/sei/extract_gap.py" 를 박는다. tools/electronic/standard_dos/README.md 가 이미 있으니 거기에 한 줄 더.
- codex 필요: False

### [P1·stale] docs-figures-readme-stale
- **어디**: `docs/figures/README.md (15줄, 마지막 커밋 2026-06-11)`
- **근거**: 본문: "This dir is the vm-side landing zone for paper figures we need to embed into slides. Each subdir mirrors the source paths on v100 container" 뒤에 `slide05_dos_pdos/…  <- container:/home/ubuntu/work/runs/comp1_v3/v3_post/k444_props/…` 식 6줄이 전부다. 지금 docs/figures/ 에는 항목이 **71개** 있고(cascade·comp1·comp2·lpsocl·li3n·sei·oxidation·seminar_2026_09_07·sdcp_nseries_spin·zn …), README 가 언급하는 slide 폴더는 셋 중 둘뿐이며(`slide09_arrhenius` 누락) "v100 container" 는 2026-06 이후 캠페인 어디에도 안 나온다.
- **고치는 법**: figures-no-registry 항목의 생성형 INDEX 로 대체한다. 그 전까지는 첫 줄에 "⚠ 2026-06-11 판 — slide05/06 landing zone 시절 문서. 현재 71개 폴더의 정본 안내가 아니다" 를 박는다.
- codex 필요: False

### [P2·broken] cathode-interface-dead-default
- **어디**: `tools/oxidation/plot_cathode_interface.py:11,28`
- **근거**: docstring 사용례와 argparse 기본값이 둘 다 `db/properties/cathode_interface_b2o3.json` 인데 **그 파일이 없다**(db/properties 에 있는 것은 `anode_interface_b2o3.json` 뿐). docstring 은 "The oxidation-side counterpart to plot_anode_interface.py; together they give the both-sided interface module" 라고 짝을 약속하는데 산화쪽 절반이 실제로는 생산된 적이 없다. 문서대로 그냥 실행하면 FileNotFoundError 다.
- **고치는 법**: ① interface_reactivity_v2.py 로 cathode_interface_b2o3.json 을 만들어 넣거나 ② docstring 에 "⛔ 입력 미생산 — 먼저 `interface_reactivity_v2.py --cathodes …` 로 만들어야 한다" 를 박고 기본값을 지운다(없는 기본값이 있는 것보다 낫다). cascade_interface_*.jsonl 은 실재하므로 그쪽을 기본으로 돌리는 것도 방법이다.
- codex 필요: False

### [P2·useless] neb-topview-v1v2v3
- **어디**: `tools/neb_diffusion/plot_neb_topview.py · plot_neb_topview_v2.py · plot_neb_topview_v3.py (셋 다 2026-06-11)`
- **근거**: 같은 그림의 세 판이 나란히 있다. v1 "Top-view render of Li adatom NEB path for paper figure (g)", v2 "Top-view render v2 — paper-quality figure for (g) panel … Shaded spheres with white highlight (faux-3D look)", v3 "NEB top-view render v3 — ASE plot_atoms shaded spheres … (much closer to paper figure quality than raw matplotlib scatter or hand-drawn highlights)". v3 이 v2 를 명시적으로 깎아내리지만 v1·v2 에는 "쓰지 마라" 표시가 없다. 같은 폴더에 plot_li3n_final.py·plot_li3n_migstep.py·li3n_figset.py·li3n_mep_profile.py 도 있어 li3n 그림 진입점이 최소 7개다.
- **고치는 법**: v1·v2 docstring 첫 줄에 `⛔ SUPERSEDED by plot_neb_topview_v3.py` 를 박는다(파일은 남긴다 — 렌더 이력이다). 더 나아가면 li3n 그림 진입점을 li3n_figset.py 하나로 모으고 나머지를 그 안의 서브커맨드로 접는다.
- codex 필요: False

### [P2·ia] site-preference-name-collision
- **어디**: `tools/doping/site_preference.py ↔ tools/sdcp/site_preference.py`
- **근거**: 이름은 같은데 물건이 완전히 다르다. doping 판: "LPSCl dopant site preference filter (Tier-1) … returns compatible substitution sites in Li6PS5Cl argyrodite based on charge sign / ionic radius / charge balance. This is the FAST filter (no DFT)". sdcp 판: "Phase-A 자세들이 **어느 표면 양이온 위에 앉았나**를 집계한다 … 챔피언 두 개가 다 Li 위였다". `grep -rl site_preference` 는 둘 다 주고, 어느 쪽을 열어야 하는지는 폴더 이름으로만 알 수 있다.
- **고치는 법**: sdcp 쪽을 `surface_cation_census.py`(또는 `phaseA_site_census.py`)로 개명하거나, 최소한 두 docstring 첫 줄에 "⚠ 동명이인 있음 — tools/<다른쪽>/site_preference.py 는 <다른 것>" 을 넣는다. 개명은 참조가 각각 1건뿐이라 싸다.
- codex 필요: False

### [P2·ia] cascade-figdir-dumping-ground
- **어디**: `docs/figures/cascade/ (92 파일)`
- **근거**: 92개 중 **35개**가 cascade 그림이 아니다 — b2o3_* 26개(b2o3_pdos.png, b2o3_elf_plane_PO.png, b2o3_md_arrhenius.png, b2o3_vs_lpscl16_msd.png, b2o3_phonon_dos.png …), nd2o3_* 2, msd_* 2, bvse_* 2, md_*, label_*, dualx_*. 같은 docs/figures 밑에 lpsocl·comp2·sei·li3n·pdos·standard_dos 등 계별 폴더가 따로 있는데도 b2o3 것이 cascade 로 들어갔다. 결과적으로 "b2o3 DOS 그림 어디 있나" 의 답이 `docs/figures/cascade/` 다.
- **고치는 법**: b2o3_*·nd2o3_* 를 docs/figures/b2o3/·nd/ 로 옮기고 생성 스크립트의 출력 경로를 같이 고친다(대부분 plot_cascade_*.py 의 `CASCADE_FIGDIR` 기본값과 개별 하드코딩). 옮기기 전에 kb·원고에서 그 경로를 인용하는 곳을 grep 으로 확인한다 — 링크가 깨지면 손해가 더 크다.
- codex 필요: False

### [P2·ia] sdcp-monolith-unreadable
- **어디**: `tools/sdcp/vasp_handoff_bundle.py (22,785줄 · 1.5 MB · top-level def/class 136개) · build_v7c_trimer.py (9,993줄) · site_screen.py (3,175줄)`
- **근거**: vasp_handoff_bundle.py 한 파일 안에 번들 생성기 · 4상 러너 shell 템플릿 · census.py 임베드 문자열 · POTCAR 봉인 · 메모리 프로브 · 분석기 · selftest 가 전부 들어 있다(`CENSUS_PY = r'''…'''` 같은 임베드 스크립트가 여럿). 파일 자체가 그 위험을 적어 놨다 — "⛔⛔ 러너 안에 같은 122줄이 **두 벌** 있었다 … 지금은 바이트가 같지만 사본은 언젠가 갈린다 — 이 파일에서만 그 사고가 **세 번** 났다". LLM 이 이 파일을 통째로 읽으면 컨텍스트가 날아가고, 부분만 읽으면 앞 50줄의 docstring(=v3, 2026-08-12)이 틀린 지도를 준다.
- **고치는 법**: 지금 당장 쪼개면 v40 계보가 깨지므로 **쪼개지 말고 지도를 만든다** — 파일 상단에 §목차(줄번호 범위 → 무엇)를 두고, `--map` 플래그로 그 목차를 찍게 한다. 임베드 shell 템플릿(CENSUS_PY 등)은 번들에 파일로 나가므로 tools/sdcp/bundle_assets/ 로 빼서 read 하는 것이 다음 단계다(파일 SHA 가 이미 MANIFEST.files_sha256 에 들어가므로 무결성은 유지된다).
- codex 필요: False

### [P2·ia] figures-house-style-drift
- **어디**: `tools/figures/ — matplotlib 을 쓰면서 house_style 을 import 안 하는 47개`
- **근거**: 88개 중 house_style import 는 34개. import 안 하면서 matplotlib 을 쓰는 것이 47개다. 시기별로 갈린다 — 2026-09 판(fig_sdcp_nseries_spin.py, fig_seminar_3sys.py, fig_msd_per_composition.py, fig_c12_pose_screen.py)은 house_style+CSV+selftest 를 다 갖췄고, 2026-08-13 하루에 태어난 cascade 13종(plot_cascade_{branches,deep,errorbars,esw,extra,interactions,litransport,oxidation_vs_banik,summary,synergy,v23,v23_detail}.py, fig_cascade_radar.py)은 전부 house_style 없이 각자 색을 쓴다. 같은 폴더의 plot_cascade_seminar_47.py·plot_cascade_audit_2026_08.py 는 house_style 을 쓰므로 계열 안에서도 양식이 갈린다. CLAUDE.md 그림 규율: "`tools/figures/house_style.py` import (…) 같은 계열 그림은 기존 family 와 양식 통일".
- **고치는 법**: cascade 13종을 house_style 로 넘긴다(색·spine·dpi 만 바꿔도 대부분 끝난다 — `INK/MUT/apply_axes`). 그림 내용을 바꾸는 것이 아니라 팔레트만 갈아끼우는 작업이므로 결과 수치 위험이 없다. elf_*·recolor_*·cutout_bg 처럼 이미지 후처리만 하는 것들은 예외로 명시한다.
- codex 필요: False
