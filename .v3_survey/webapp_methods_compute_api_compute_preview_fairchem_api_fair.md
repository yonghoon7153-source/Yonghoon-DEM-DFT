# webapp — 방법론 + 계산 돌리기 (/methods · /compute · /api/compute-preview · /fairchem · /api/fairchem)

## 지금 무엇인가
세 화면이다. /methods 는 `kb/methodology/computational_methods_canonical.md`(382줄) 를 doc.html 로 그대로 흘려보내는 읽기 전용 문서 페이지이고, /compute 는 조성×계산타입을 고르면 /api/compute-preview 가 QE 입력 + 러너 스크립트 붙여넣기 블록을 만들어 주는 생성기이며, /fairchem 은 2026-08-21 공식 스냅샷 번들(sha256 36/36 일치)을 읽어 "우리가 UMA 를 어디까지 써도 되나" 를 보여주는 판정 화면이다. 세 화면 다 200 으로 뜨고 내부 링크 46개 전부 살아 있다. 다만 /compute 가 내놓는 붙여넣기 블록 중 QE-GPU 러너 한 갈래만 2026-09-08 기준이고, 나머지(MD 스크립트·pseudo_dir·Nd 처방·KISTI 러너)는 그대로는 안 돈다.

## 처음 오는 사람
**/compute** — 처음 온 사람한테는 이 셋 중 제일 친절하다. 맨 위 보라색 카드가 "이 페이지가 무엇인가"를 기초/심화 배지까지 달아 설명하고, 대가를 치른 규율 5줄(--save_traj · MSD 창 · 아레니우스 3점 · Li₃N 금지 · pw.x/UMA 동시금지)을 괄호 안 사고 사례와 함께 준다. 문제는 두 가지다. ① 그 카드가 ~50줄이라 **정작 도구(조성 드롭다운·계산타입 버튼)가 첫 화면 밖으로 밀린다** — 처음 온 사람은 "규율 페이지"로 착각한다. ② 더 나쁜 건, 화면이 가르친 규율을 화면이 만든 산출물이 지킨다는 보장이 전혀 없다는 점이다. "MD 는 --save_traj 없이 돌리지 않는다"고 굵게 쓴 바로 아래에서 MD 를 고르면 궤적 저장이 한 줄도 없는, 게다가 존재하지 않는 fairchem API(`OCPCalculator`)를 부르는 스크립트가 나온다. 붙여넣으면 첫 import 에서 죽는다. 처음 온 사람은 그게 자기 환경 탓인 줄 안다.

**/methods** — 여기서 제일 막힌다. 29.5 KB · 382줄이 목차도 앵커 내비도 없이 **한 덩어리 스크롤**로 나온다(doc.html 은 TOC 를 안 그리고 md 에 `[TOC]` 마커도 없다). 게다가 페이지 헤더 h1("계산 방법 Canonical (단일 기준)") 바로 밑에 문서 자신의 h1("계산 방법 Canonical — 단일 기준 (2026-07-23 재정리 · 2026-08-20 축 4개 추가)")이 또 나와 제목이 두 번 찍힌다. "무엇부터 읽어야 하나"에 대한 안내가 없고, 화면 어디에도 **이 문서가 언제 것인지**가 배지로 안 붙어 있다 — 갱신 이력을 보려면 378줄까지 스크롤해야 하고 거기 마지막 줄이 2026-08-20 이다. 오늘(09-08) 처음 온 사람은 이걸 최신 기준으로 읽는다.

**/fairchem** — 상단 카드("우리가 고정해 쓰는 조합 uma-s-1p1 · omat")와 빨간 금지 카드는 좋다. 그런데 바로 그 위에서 "⚠ 레지스트리에 더 새 UMA 가 있다: uma-m-1p1 · uma-s-1p2 · uma-s-1p2p1" 라고 겁을 주는데 uma-m-1p1 은 같은 1p1 릴리스의 **medium 크기 변종**이지 새 버전이 아니다. 그리고 논문 절에 큰 숫자 타일 넷이 42 / **0** / **0** / **0** 으로 떠 있다 — 처음 보면 "논문 42편 중 아무것도 안 읽었구나" 로 읽히지만 실제로는 FK 매칭이 구조적으로 절대 성립하지 않아 영원히 0 이다. 또 이 화면은 "우리가 뭘 써도 되나"를 말하면서 /governance · /methods · /compute 로 나가는 링크가 **하나도 없다**(내부 링크는 `/`, `/literature`, 그리고 raw JSON API 10개뿐). 처음 온 사람이 "그럼 이 판정은 누가 언제 비준했나"를 물으면 갈 데가 없다.

## 건드리면 안 되는 것
- **/compute 의 QE-GPU ldd 러너 블록 (webapp/data.py:3549-3570) — 절대 단순화 금지.** 2026-09-08 에 같은 자리에서 세 번 죽고 얻은 것이다(① conda mpirun → MPI_Init NULL communicator ② 런처 제거 → `libgomp: TODO` ③ hpcx 추측인데 kgy pw.x 는 `~/apps/openmpi-4.1.6` 링크). 정본 tools/doping/run_force_check_scf.sh:75-99 와 유도 방식이 일치하고, webapp/tests/test_webapp.py:727-746 `test_compute_runner_does_not_guess_gpu_runtime` 이 `mpirun -np 1` 회귀를 음성으로 막고 있다. v3 재편에서 '보기 싫으니 한 줄로' 는 이 사고를 네 번째로 부른다.
- **규율 5줄의 '괄호 안 대가' 문구 (compute.html:39-59) — 문장은 지우지 말고 접기만.** `2026-07 에 12런, 2026-08 에 21런이 궤적 없이 끝났고 둘 다 화면상으로는 정상 완료였다` 같은 실측 사례가 규칙을 지키게 만드는 유일한 근거다. 규칙만 남기고 사례를 지우면 다음 사람이 규칙을 예외 처리한다.
- **compute_preview 의 fail-closed 두 갈래 (webapp/data.py:3450-3459).** sdcp/molecular → ORCA 안내만 내고 스크립트 미생성, li3n+md → Li₃N UMA 금지로 미생성. 둘 다 '틀린 스크립트보다 스크립트 없음이 낫다' 는 옳은 선택이다. 이 `_none` 갈래를 나머지 미설정 조성에도 **확장**해야지, 없애면 안 된다.
- **md_html → _bind_claims 자동 결속과 눈에 보이는 `.claim-flag` (webapp/app.py:151-192 · canonical.py:381-432).** /methods 실측으로 unbound 0 · dangling 0 이고, 철회된 b2o3 `MD_Ea_eV@b2o3` 0.199 네 곳이 전부 `data-claim` 으로 이름을 대고 사유 툴팁까지 달고 있다. 손으로 data-claim 을 심는 방식으로 되돌리면 원문 수정 때 결속이 조용히 사라진다.
- **/api/fairchem 의 fail-closed 404 (webapp/app.py:765-790).** docstring 그대로 — `알 수 없는 이름이면 빈 배열을 주지 않고 404 를 낸다. 빈 배열은 "그런 건 없다" 와 "이름을 틀렸다" 를 구분 못 하게 만든다.` 실측 확인: /api/fairchem/v1/bogus → 404. 편의를 이유로 200+[] 로 바꾸지 않는다.
- **fairchem.py 의 읽기 전용 계약과 세 축 분리 (webapp/fairchem.py:1-26, 185-200).** `우리 수치를 db/fairchem 에 복사해 두 번째 정본을 만들지 마` · `http_status / execution_status / applicability 를 하나로 뭉치지 않는다`. execution 축이 지금 전부 not_run 이라고 해서 축을 합치면, 200 인데 예제가 죽는 튜토리얼(/formation-energy·/phonons·/elastic)이 '정상' 으로 보인다.
- **verify_hashes() 무결성 게이트와 화면의 실패 문구 (fairchem.py:136-169 · fairchem.html:186-188).** 지금 36/36 일치라 초록으로 뜨지만, 실패 시 `⛔ 무결성 실패 — 이 화면을 공식 스냅샷이라고 인용하지 말 것` 이 뜨는 경로를 유지해야 한다.
- **OUR_PINNED · OUR_BANS 가 번들이 아니라 webapp 코드 상수로 있는 것 (fairchem.py:61-85).** 주석대로 `번들(공식 스냅샷)에 우리 결정을 써 넣으면 두 번째 정본이 된다`. 위치를 '정리' 한다며 db/knowledge 로 옮기면 안 된다.
- **/methods §2 elastic 표의 `?` 칸들 (computational_methods_canonical.md:50-51, comp3/4/5·b2o3 의 k-mesh·pseudo·ecut).** 모르는 것을 `?` 로 적은 정직한 표기다. 0 이나 공백으로 바꾸거나 행을 지우면 '안 잰 것' 과 '모르는 것' 이 섞인다. 마찬가지로 §10 `진행 중이라 아직 정본이 아닌 것` 과 b2o3 철회 인용블록(196-215)은 역사라 지우지 않는다 — 지우면 3일짜리 배치를 다시 돌린다.
- **/compute 의 서버별 확인 각주 (compute.html:93-110) 와 KISTI QOS 경고 (`scancel 직후 재제출 금지, 카운터 지연`).** CLAUDE.md 계산 자원 절과 1:1로 대응하는 실측 조항이다.
- **/fairchem 의 papers 4단계 분리 캡션 (fairchem.html:141-143): `⚠ 색인됨 ≠ 읽음 ≠ 그림 확인 ≠ 승인. 합치면 "읽었다" 가 과장된다.`** 지금 0/0/0 이 나오는 건 FK 배선 문제이지 이 분리가 틀려서가 아니다. 숫자를 고치되 축은 그대로 둔다.

## 발견

### [P0·wrong] compute-nd-hubbard-prescription-wrong
- **어디**: `webapp/data.py:3482 (warn) · webapp/data.py:3416 (PSEUDO_LIB) · webapp/data.py:3424 (COMPUTE_SETTINGS modelc_nd_doped)`
- **근거**: /api/compute-preview?cid=modelc_nd_doped 의 warn 이 그대로: `"Nd 4f: DFT+U (U_eff≈6 eV) + ISPIN=2 필요 (litdb Nd 교훈) — &SYSTEM에 Hubbard 블록 추가."` 세 군데가 틀렸다. ① `ISPIN=2` 는 VASP 키워드다 — QE 는 `nspin = 2` 다(tools/doping/generate_dft_inputs.py:142 `lines.append("    nspin       = 2")`). ② QE 7.x 는 &SYSTEM 이 아니라 독립 카드로 쓴다 — 같은 파일 197: `lines.append("HUBBARD (ortho-atomic)")`, selftest 550: `'HUBBARD (ortho-atomic)' in _spin and '  U Nd-4f 6.0' in _spin`. ③ 2026-09-08 커밋 cef78893a("frozen-4f PP 에 U 를 못 걸게 막는다")가 실측으로 판정했다: "gabia 실측: 거기 있는 Nd PP 는 `Nd.pbe-spdn-kjpaw_psl.1.0.0.UPF` 하나뿐이고 frozen-4f(z≈11, 4f 가 core)다. … 그대로 돌리면 U 가 걸 대상이 없다 — QE 가 죽거나 조용히 무시한다." 화면은 PP 를 따지지 않고 무조건 U 를 권한다. 덧붙여 PSEUDO_LIB 의 `"Nd": "Nd.GGA-PBE-paw.UPF"` 는 repo 전체에서 webapp/data.py:3416 한 곳에만 있는 이름이다(tools/ 에 0건). 정본은 tools/doping/generate_dft_inputs.py:52 `'Nd': ('144.242', 'Nd.paw.z_14.atompaw.wentzcovitch.v1.2.upf')`.
- **고치는 법**: warn 을 PP 조건부로 바꾼다: z_valence≈14(4f 원자가) PP 일 때만 `nspin = 2` + 독립 `HUBBARD (ortho-atomic)` / `  U Nd-4f 6.0` 을 권하고, frozen-4f(z≈11)면 U·nspin 을 빼라고 거부 문구를 낸다 — generate_dft_inputs.py:661-682 의 가드 문구를 그대로 재사용. PSEUDO_LIB['Nd'] 를 `Nd.paw.z_14.atompaw.wentzcovitch.v1.2.upf` 로 고치고, 화면에 "이 PP 가 그 서버에 있는지 확인" 한 줄을 붙인다.
- codex 필요: False

### [P0·broken] compute-md-template-dead-api
- **어디**: `webapp/data.py:3581-3597 (_md_template) · webapp/templates/compute.html:39-42 (--save_traj 규율 카드)`
- **근거**: 생성되는 `md_<cid>.py` 가 `from fairchem.core import OCPCalculator   # UMA-s-1p1` (data.py:3586) 와 `atoms.calc = OCPCalculator(model_name='uma-s-1p1', task='omat')` (3589) 를 쓴다. 이 repo 의 실제 MD 도구는 전부 다른 API 다 — tools/modelc_v3/aimd_mlip.py:145-149 · tools/modelc_v3/disorder_ensemble_diffusion.py:379-382 · tools/ionic/mlip_committee.py:93-95 가 모두 `from fairchem.core import pretrained_mlip` + `FAIRChemCalculator(predictor, task_name=...)` 다. 붙여넣으면 첫 줄에서 죽는다. 게다가 같은 화면이 compute.html:39 에서 굵게 `MD 는 --save_traj 없이 돌리지 않는다` 고 가르치는데, 생성된 스크립트에는 궤적 저장이 없다 — 3596 줄이 `# 생산 200 ps + MSD(2–50ps) 저장 …` 주석 하나로 끝난다. 그리고 3591-3595 의 이중 루프가 `atoms` 객체 하나를 600/800/1000 K × seed 1/2/3 아홉 번에 그대로 재사용해 속도 재초기화도 구조 리셋도 없다 — 시드가 독립이 아니다.
- **고치는 법**: 손으로 py 를 짜 주지 말고 **정본 러너를 그대로 낸다**: `tools/ionic/run_arrhenius_6pt.sh` 가 `tools/modelc_v3/disorder_ensemble_diffusion.py` 를 `--equilib_ps 5 --prod_ps 200 --timestep_fs 2.0 --friction 0.02 --save_fs 100 --fit_window_ps 2 50 --save_traj --seed <S> --uma_model uma-s-1p1 --uma_task omat` 로 부르는 실제 줄(run_arrhenius_6pt.sh:181-190)을 조성별로 채워 붙여넣기 블록으로 낸다. CLAUDE.md 코드 규율("기존 도구 확장이 새 파일보다 항상 낫다")과도 이쪽이 맞다.
- codex 필요: False

### [P0·broken] compute-pseudodir-comment-inside-string
- **어디**: `webapp/data.py:3487 · webapp/data.py:3520-3523 (_pseudo_dir)`
- **근거**: kgy·gabia 조성(comp1/comp2/modelc/modelc_v3)의 생성 입력이 이렇게 나온다: `pseudo_dir = './pseudo   # ← 이 서버(kgy/gabia)의 pseudo 경로로 교체'`. 주석이 Fortran 문자열 **안**에 들어가 있어서 QE 는 경로 전체를 리터럴로 읽는다. QE namelist 주석은 `!` 이고 따옴표 밖이어야 한다. KISTI 갈래는 `/scratch/x3430a02/kgy/manuscript_support/pseudo` 로 깨끗해서 이 문제가 안 보인다 — 즉 세 서버 중 둘에서만 조용히 깨진다.
- **고치는 법**: `pseudo_dir = './pseudo'` 로 닫고 안내는 다음 줄에 `! ← 이 서버(kgy/gabia)의 pseudo 경로로 교체` 로 뺀다. 회귀 시험 한 줄: 생성 입력의 따옴표 안에 `#` 이 없어야 한다.
- codex 필요: False

### [P0·wrong] methods-comp2-gap-dos-threshold-unmarked
- **어디**: `kb/methodology/computational_methods_canonical.md:120-131 (/methods §4)`
- **근거**: §4 제목이 `## 4. Band gap (DFT fixed-occ nscf **eigenvalue** = canonical)` 인데 표 안에 `| comp2 | 2.04 | \`electronic.json\` |` 가 아무 표시 없이 들어 있다. db/properties/canonical_registry.json 의 같은 항목은 `status: provisional` 이고 사유가 `"출처는 배선됐지만 **legacy DOS-threshold 판독**이다(electronic.json 이 _DEPRECATED 로 표시). fixed-occ nscf 재계산 전까지"` 다. 바로 세 줄 아래 131 이 `⚠ **DOS-threshold 판독(comp1 1.76 / modelc 1.82) 및 modelc.json:28 의 1.65 는 폐기**` 라고 같은 판독법을 금지한다 — 금지문과 위반값이 같은 절에 있다. 앱 자신의 시험도 이걸 막고 있다: webapp/tests/test_webapp.py:749-753 `test_gap_card_excludes_legacy_group` 이 `assert "comp2" not in gm`. 결속 스캐너가 못 잡은 이유는 구조적이다 — webapp/canonical.py:418-419 의 `bound_claims()` 는 `status == "retracted"` 또는 `citable is False` 만 결속 대상으로 삼고 `provisional` 은 통째로 건너뛴다. 같은 표 127 줄 `| +B2O3 | 1.9671 | |` 은 출처 칸이 **빈칸**이다(CLAUDE.md 정본은 db/properties/electronic.json).
- **고치는 법**: §4 표에서 comp2 행을 `⚠ provisional — legacy DOS-threshold` 로 표시하거나 별도 하단 절로 내린다(지우지 않는다 — "안 잰 것"으로 보인다). +B2O3 출처 칸에 `electronic.json` 을 채운다. 그리고 결속 정책을 1저자에게 물어 `provisional` 도 결속 요구 대상에 넣을지 정한다 — 지금은 provisional 값이 어느 화면에서도 이름을 대지 않는다.
- codex 필요: False

### [P1·broken] compute-unconfigured-compositions-fabricate-paths
- **어디**: `webapp/data.py:3441-3442 (COMPUTE_SETTINGS 폴백) · webapp/templates/compute.html:72-74 (드롭다운)`
- **근거**: 드롭다운은 COMPOSITIONS 14개를 전부 내는데 COMPUTE_SETTINGS(3419-3427)는 7개뿐이다. 나머지 6개(comp3·comp4·comp5·vgcf_hbn·li3n·lic6)는 폴백 `{"ecutwfc": 60, "ecutrho": 480, "k": [2,2,1], "struct": f"{cid}.cif", "server": "KISTI neuron"}` 를 타고, 실제로 돌려 보니 전부 `warn=[]` 로 경고 한 줄 없이 입력이 나온다. 예: comp3 scf → `!   db/structures/comp3.cif` (파일 없음), li3n scf → `db/structures/li3n.cif` (없음), vgcf_hbn md → `atoms = read('db/structures/vgcf_hbn.cif')` (없음). 6개 전부 db/structures 에 실물이 없다(확인함). vgcf_hbn·lic6 의 MD 는 서버가 `KISTI neuron` 으로 찍히는데 러너(_runner_uma, 3572-3579)는 `conda run -n uma` + `nvidia-smi` 를 쓴다 — KISTI 는 Slurm 이고 그 env 가 없다. 참고로 /methods:50 은 comp3/4/5 를 `⚠ **옛 방법 → 재측정 필요**` 로 이미 판정해 뒀다.
- **고치는 법**: COMPUTE_SETTINGS 에 없는 조성은 폴백을 없애고 `_none` 갈래(sdcp·li3n-md 가 쓰는 그 갈래, 3448)로 보낸다: note 에 "이 조성은 canonical 레시피가 등록돼 있지 않다 — 만들지 않는다" 를 적고 등록 방법을 알려 준다. 또는 드롭다운을 COMPUTE_SETTINGS 키로 좁힌다(단 왜 없는지는 화면에 남긴다).
- codex 필요: False

### [P1·stale] methods-stale-since-0820
- **어디**: `kb/methodology/computational_methods_canonical.md:1-7, 155-172, 300-315, 331, 378-382 (전부 /methods 에 그대로 렌더)`
- **근거**: 문서 h1 이 `계산 방법 Canonical — 단일 기준 (2026-07-23 재정리 · **2026-08-20 축 4개 추가**)` 이고 378-382 의 갱신 이력 마지막 줄이 2026-08-20 이다. 19일 지난 항목들이 아직 `🆕` 를 달고 있다(155 `### 6-1. 🆕 상자 크기도 …`, 247 `## 6b. 🆕 NEB 장벽`, 331 `## 10. 🆕 진행 중이라 아직 정본이 아닌 것`). 2026-09-07~08 에 확정된 것 중 이 문서에 반영된 게 하나도 없다 — `git log` 기준 5196c1081(LPSOCl 3×3×1 닫힘 조건 비준) · 22b00e909(cascade 보고량 카드 비준) · 83c868a97(Nd 어닐 6셀) · 5769e2328(QE-GPU 런타임). db/governance/decisions.json 에도 09-07~08 active 결정이 셋이다(D-2026-09-08-lpsocl-box331-closure-conditions · D-2026-09-08-cascade-d-rel-estimand · D-2026-09-08-b2o3-uma-vs-dft-force). 특히 §6-1(155-172)의 `**기울기(D)가 1.64 ± 0.14 배 움직인다.**` 와 `⇒ D·σ 절대값은 **상자 크기**에 묶여 있다` 는 kb/methodology/md_axis_status_2026_09_07.md 가 이미 좁혔다: `🔴 유한크기·형상 결합 효과 | 같은 T·같은 길이인데 셀이 바뀌면 D 가 1.79배 … ⚠ 크기만의 효과가 아니다 — T13 정본이 크기와 형상 차이가 함께 들어갔다고 경고한다 (BH P1, 2026-09-07 정정). 부르는 이름은 finite-size/shape-coupled effect`. 같은 09-07 카드가 §6-1 에 없는 의무도 하나 더 건다: `창 편향 | 2–50 ps 창의 D 는 늦은 창 대비 과대 (558원자 −12.7 % · 62원자 −20.5 %) — 절대 D 인용 시 병기 의무`. 문서 안 파일 참조 경로는 전부 실존한다(자동 확인, MISSING 0건) — 낡은 건 내용이지 링크가 아니다.
- **고치는 법**: ① /methods 화면 상단에 문서 mtime 또는 갱신 이력 마지막 날짜를 배지로 박는다(doc.html 이 subtitle 옆에 찍으면 라우트 하나로 끝난다). ② §6-1 의 명칭을 finite-size/shape-coupled 로 고치고 1.65 vs 1.79 병기 + 창 편향 병기 의무를 추가. ③ 09-07~08 결정 3건을 §10 에 줄로 올리고 각 카드 파일을 링크. ④ 19일 지난 `🆕` 를 걷는다.
- codex 필요: False

### [P1·duplicate] methods-md-1p65-vs-1p79
- **어디**: `kb/methodology/computational_methods_canonical.md:158-162 vs db/properties/t13_msd_length_verdict_2026_08_29.json (🔴_부수_발견_셀크기_의존성)`
- **근거**: 같은 계(LPSOCl 600 K)에 셀 크기 효과가 두 값으로 있다. /methods §6-1 표: `| MSD@50ps | 25.3 Å² | **41.7 Å²** | **1.65×** |` (출처 kb/results/lpsocl_box_size_600K_2026_08_18.md). T13 정본: `"lpsocl_small800_62원자_805ps_T600": 6.632e-06, "lpsocl_long_558원자_805ps_T600": 1.19e-05, "비": 1.79`. 그런데 T13 자신이 단서를 단다: `"⚠_미검증": "이 두 런은 원자수뿐 아니라 슈퍼셀 모양도 다를 수 있다 — 순수 크기 효과로 단정하기 전에 셀 파라미터 대조 필요."` 어느 쪽을 canonical 방법 문서의 "일관성 축" 숫자로 쓸지는 우리가 못 정한다 — 궤적 길이(50 ps 창 vs 805 ps)와 셀 형상 축이 섞여 있다.
- **고치는 법**: 두 값을 한 표에 병기하고 각각 무엇을 잰 것인지(창·길이·셀 파라미터) 명시한 뒤, 어느 것을 축 숫자로 인용할지는 외부 리뷰/1저자 판정에 올린다. 임의로 하나를 고르지 않는다.
- codex 필요: True

### [P1·missing] methods-gen0-footnote-missing
- **어디**: `kb/methodology/computational_methods_canonical.md:141-153 (/methods §6 Ea 표)`
- **근거**: §6 표가 `| comp1 | **0.253** | li_transport.json (4fu, PRIMARY) |`, `| modelc | 0.224 | li_transport.json |`, `| lpsocl | 0.271±0.033 / 0.287±0.024 | lpsocl_md_arrhenius.json |` 를 아무 지위 표시 없이 낸다. 두 원장이 이걸 막고 있다. ① db/properties/citation_hazards.json: `{"file": "db/properties/lpsocl_md_arrhenius.json", "level": "HOLD", "what": "Ea", "why": "⚠_DIFFUSIVE_GATE_2026_08_01 …"}` 과 `{"file": "db/properties/li_transport.json", "level": "HOLD", "what": "Ea", "why": "같은 확산영역 게이트"}`. ② kb/methodology/md_axis_status_2026_09_07.md: `★ 레지스트리의 MD_* 항목 11개가 전부 gen0 이다` + 슬라이드·원고에 gen0 을 넣을 때 **반드시** 함께 낼 영문 각주 `Predates the 2026-08 MTO / trajectory-retention / 4-window standard. Ea values are protocol-conditioned; not comparable to the 400 ps campaign.` /methods 화면에는 이 각주도 HOLD 표시도 없다. 결속 스캐너로도 안 잡힌다 — li_transport 위험 항목에는 `id` 필드가 없어서 webapp/canonical.py:463 `if not hid ... continue` 로 걸러진다. (참고: b2o3 0.199 철회값 4건은 정상 결속돼 있다 — unbound 0.)
- **고치는 법**: §6 표에 세대(gen0/1/2)와 HOLD 열을 붙이고, 표 밑에 md_axis_status 의 영문 각주를 그대로 실는다. citation_hazards.json 의 li_transport 항목에 `id` 를 붙여 hazard_claims 가 결속을 요구하게 만든다. 다만 lpsocl 위험 항목의 HOLD 사유(β 게이트 미통과, 2026-08-12 수집)가 §6-2 의 `LPSOCl 10런 | β −0.02–0.29 — ⭕ 전부 정상`(2026-08-20)과 어긋나므로 해제 여부를 먼저 확인한다.
- codex 필요: False

### [P1·wrong] fairchem-newer-models-mislabel
- **어디**: `webapp/fairchem.py:88-96 (newer_models) · webapp/templates/fairchem.html:70-74`
- **근거**: 화면 상단에 `⚠ 레지스트리에 더 새 UMA 가 있다: uma-m-1p1 · uma-s-1p2 · uma-s-1p2p1 — **자동으로 올리지 않는다.**` 가 뜬다. `uma-m-1p1` 은 새 버전이 아니라 같은 1p1 릴리스의 medium 크기 변종이다(models.json 에 uma-s-1p1 / uma-m-1p1 이 같은 repo `facebook/UMA` 로 나란히 등록). newer_models() 는 실제로 버전 비교를 안 한다 — `if mid.startswith("uma-") and mid != ours: out.append(mid)` 가 전부다. 같은 파일의 우리 금지 문구(OUR_BANS, fairchem.py:83-84)는 정확히 쓰여 있다: `"레지스트리에 uma-s-1p2 · 1p2p1 이 있지만 우리는 1p1 에 고정돼 있다."` — 두 문장이 같은 화면에서 서로 다른 말을 한다.
- **고치는 법**: newer_models() 를 크기축(s/m/l)과 버전축(1p1/1p2/1p2p1)으로 나눈다. 문구도 둘로: "더 새 버전"(1p2·1p2p1)과 "같은 버전 다른 크기"(m-1p1). 후자는 경고가 아니라 정보다.
- codex 필요: False

### [P1·broken] fairchem-paper-fk-never-matches
- **어디**: `webapp/fairchem.py:236-253 (papers_rows) · webapp/templates/fairchem.html:132-148`
- **근거**: 매칭 규칙이 `slug = next((h for h in have if pid and (pid in h or h in pid)), None)` 인데 번들 paper_id 는 `fc-paper-gemnet-oc-graph-neural-networks-for-large-datasets` 꼴이고 litdb 파일명은 `uma2026_family_of_universal_models_for_atoms.md` 꼴이다 — 부분문자열이 될 수가 없다. 실제 렌더 결과: 큰 숫자 타일이 `42`(색인됨) / `0`(digest 읽음) / `0`(그림 확인) / `0`(사람 승인), 그리고 접힌 표 42행의 digest 칸이 전부 `—`. `{% set linked = papers|selectattr('litdb_slug')|list %}` 도 항상 비어 "litdb 연결됨" 블록이 영영 안 뜬다. 그런데 캡션은 `digest 는 논문 에이전트가 litdb/papers/ 에 만들면 자동으로 이어진다 — 값을 복사하지 않고 파일 존재만 본다` 라고 약속한다. litdb 에는 실제로 UMA 논문 2편이 있다(`uma2026_family_of_universal_models_for_atoms.md`, `kalikadien2026_uma_tm_catalyst_conformer_ranking.md`) — 있는데 못 잇는다. 또 `human_approved` 는 코드에 `False,  # 사람만 올린다` 로 하드코딩돼 있어 영구 0 이다.
- **고치는 법**: 매칭을 doi/arxiv id 로 바꾸거나, 번들 papers 엔티티에 `litdb_slug` 를 명시 필드로 넣고 손으로 잇는다. 잇지 못하는 동안에는 `0` 대신 `원장 부재 — FK 미배선` 으로 적는다(0 은 "세어 봤는데 없다"는 뜻이라 거짓말이 된다). human_approved 는 실제 승인 원장이 생길 때까지 타일에서 빼거나 `—` 로 낸다.
- codex 필요: False

### [P1·useless] fairchem-audit-detail-never-rendered
- **어디**: `webapp/app.py:752-762 (render_template 인자) · webapp/templates/fairchem.html (전체)`
- **근거**: 라우트가 템플릿에 넘기는 인자 중 `sections`, `snap`, `techs`, `seed`, `audit` 다섯이 fairchem.html 안에서 **한 번도 안 쓰인다**(grep 결과 `audit` 은 190줄의 `summary.link_audit` 만 걸리고 원본 `audit` 은 0건). 그중 `audit`(= blob('live_link_audit'))에는 화면에 없는 실물이 들어 있다: broken_targets 19건(`{"path": "/catalysts/datasets/oc20", "http_status": 404, "reason": "obsolete nested link"}` 등), special_probes 5건(그중 `{"url": "https://fair-chem.github.io/sitemap.xml", "http_status": 200, "finding": "Contains 64 locations, but every location uses http://localhost:3000."}`), 그리고 execution_render_findings 1건(`{"pages": ["/formation-energy", "/phonons", "/elastic"], "finding": "Pages return HTTP 200 but render ModuleNotFoundError for quacc.recipes.mlp in the first code cell."}`). 화면에는 이게 전부 `깨짐 19 · 렌더 실행오류 1` 이라는 숫자 두 개로만 남는다. 특히 마지막 것은 이 페이지 docstring 이 존재 이유로 내세운 바로 그 사례("200 인데 실행 실패한 튜토리얼")인데 화면에 안 보인다.
- **고치는 법**: `<details>` 하나를 ⑦ 출처·무결성 안에 추가해 broken_targets·special_probes·execution_render_findings 를 표로 낸다. 안 쓰는 나머지 인자(sections·snap·techs·seed)는 라우트에서 뺀다 — 넘기는데 안 쓰면 다음 사람이 "어딘가 쓰이겠지" 하고 남긴다.
- codex 필요: False

### [P1·useless] fairchem-execution-axis-all-not-run
- **어디**: `webapp/templates/fairchem.html:212-220 (공식 문서 66쪽 표) · webapp/fairchem.py:198`
- **근거**: 페이지 docstring 과 화면 문구가 세 축 분리를 핵심으로 내세운다: `⚠ 세 축을 절대 한 배지로 합치지 않는다: http_status(페이지가 열리나) · execution_status(예제가 도나) · project_status(우리 계에 쓸 수 있나)`. 그런데 66쪽 실측을 세어 보면 execution_status 가 `Counter({'not_run': 66})` — 100% 한 값이다(http 는 200×64 / 404×2). 즉 축을 나눈 근거는 옳은데 그 축에 데이터가 하나도 없고, 표의 execution 열은 66행 내내 같은 글자를 반복한다. 유일한 실행 증거(quacc.recipes.mlp ModuleNotFoundError)는 위 finding 대로 다른 필드에 있고 안 보인다.
- **고치는 법**: execution 열 자리에 `not_run 66/66 — 이 축은 아직 아무것도 안 돌려 봤다` 를 표 위 한 줄로 올리고 열은 접는다(축을 없애지는 않는다 — 없애면 나중에 다시 합쳐진다). 그 자리에 execution_render_findings 3쪽을 대신 보인다.
- codex 필요: False

### [P1·stale] fairchem-snapshot-date-not-on-screen
- **어디**: `webapp/templates/fairchem.html:182-193 (⑦ 출처·무결성) · db/knowledge/fairchem/live_link_audit.json`
- **근거**: 번들은 `release_id: fairchem_official_kb_2026_08_21`, 링크 감사는 `"checked_at": "2026-08-21"` 이다(오늘 09-08 기준 18일). 화면에서 날짜라고 볼 수 있는 건 맨 아래 접힌 카드의 `공식 commit 93a03d656806 (2026-08-20T23:19:48Z)` 한 줄뿐이고, 그건 **우리가 언제 떴는지**가 아니라 **공식 repo 커밋 시각**이다. 링크 감사 문장 `공식 문서 링크 감사 — 대상 83 · 200 64 · 깨짐 19 · 렌더 실행오류 1` 에는 날짜가 아예 없어 지금 상태로 읽힌다.
- **고치는 법**: 상단 히어로 카드에 `스냅샷 2026-08-21 (N일 전)` 배지를 박고, 링크 감사 문장에 `checked_at` 을 붙인다. 30일 넘으면 색이 바뀌게 하면 갱신 트리거도 된다.
- codex 필요: False

### [P1·stale] compute-18run-in-progress-stale
- **어디**: `webapp/templates/compute.html:39-42`
- **근거**: 규율 카드 첫 줄이 `2026-07 에 12런, 2026-08 에 21런이 궤적 없이 끝났고 둘 다 화면상으로는 정상 완료였다. (지금 18런을 다시 돌리는 중 — 이틀)`. kb/methodology/md_axis_status_2026_09_07.md 의 캠페인 판정표는 이미 끝난 것으로 적는다: `| arrhenius_6pt_traj 18런 (700/900 K) | gen1 | ✅ 골격 판정용으로 유효 (실제로 b2o3 700 K creep 을 잡았다). 아레니우스 점 승격은 불가 |`. "돌리는 중" 이 아니라 완주해서 판정까지 났다.
- **고치는 법**: 괄호를 결과로 바꾼다 — "(18런 재실행 완료 · gen1 · b2o3 700 K creep 을 실제로 잡았다 — md_axis_status_2026_09_07)". 진행 상태 문구는 하드코딩하지 말고 원장에서 읽거나 아예 결과형으로만 쓴다.
- codex 필요: False

### [P1·broken] compute-kisti-runner-no-ranks
- **어디**: `webapp/data.py:3528-3540 (_runner_qe KISTI 갈래)`
- **근거**: 생성되는 Slurm 블록의 지시자가 `#SBATCH -J {prefix}` / `#SBATCH -p <파티션 확인>` / `#SBATCH --time=24:00:00` / `#SBATCH -o {prefix}.out` 넷뿐이고 그 다음이 `srun pw.x -in {prefix}.in` 이다. `-N` · `--ntasks` · `--cpus-per-task` 가 없어서 srun 이 태스크 1개로 돈다. 게다가 `-p <파티션 확인>` 은 문자 그대로 꺾쇠 자리표시자라 이 스크립트는 sbatch 에 그대로 넣으면 애초에 반려된다. QE-GPU 갈래(3549-3570)는 2026-09-08 에 ldd 유도로 제대로 고쳐졌고 시험(test_compute_runner_does_not_guess_gpu_runtime)도 붙었는데, Slurm 갈래는 그때 같이 안 봤다 — 그 시험도 `assert "srun" in rk and "ldd" not in rk` 만 본다.
- **고치는 법**: `#SBATCH -N 1` · `#SBATCH --ntasks=<노드 코어수>` · `#SBATCH --cpus-per-task=1` 을 넣고 `srun pw.x -nk <풀> -in …` 로 맞춘다. 파티션은 자리표시자 대신 화면에서 고르게 하거나 KISTI 실측 파티션명을 기본값으로 둔다. 그리고 KISTI 갈래에도 "랭크 수가 붙어 있나" 음성 시험을 단다.
- codex 필요: False

### [P1·stale] compute-nd-structures-stale
- **어디**: `webapp/data.py:3424 (modelc_nd_doped struct)`
- **근거**: 화면이 Nd 계에 쓰는 구조가 `modelc_nd_doped_DFTrelax.cif` 하나로 고정돼 있다. 2026-09-08 커밋 83c868a97("Nd2O3-LPSCl1.6 어닐 6셀 회수 — UMA 500 K 20 ps + relax (순위: distributed < free_s < bo4)")가 `db/structures/ndo_lpscl16_rietveld_2026_09_07/` 에 6셀을 넣었다 — `ndo_lpscl16_n4fu_O-{distributed,free_s,bo4}` · `n5fu` 각각 cif/vasp/xyz. 화면에는 이 폴더도, 순위도, `anneal_2026_09_07` 하위도 전혀 없다.
- **고치는 법**: COMPUTE_SETTINGS 의 Nd 항목을 6셀 선택형으로 바꾸거나(모티프 드롭다운), 최소한 note 에 "09-07 Rietveld 정수화 + 09-08 어닐 6셀이 db/structures/ndo_lpscl16_rietveld_2026_09_07/ 에 있다 (순위 distributed < free_s < bo4)" 를 적고 SUMMARY.json 을 링크한다.
- codex 필요: False

### [P1·missing] compute-estimand-card-not-mentioned
- **어디**: `webapp/templates/compute.html:18-67 (규율 카드 전체)`
- **근거**: 규율 카드 다섯 줄은 전부 **실행 규율**(궤적·창·온도점·모델금지·VRAM)이고, CLAUDE.md 가 2026-08-28 에 채택한 **계산 전 규율**은 한 줄도 없다: "새 물리량을 계산하기 전에 kb/templates/estimand_card.md 를 채운다", "검증 게이트를 결과 보기 전에 정한다", "보고량·마감 판정은 db/governance/decisions.json 에 등록한다". compute.html 에서 `보고량`·`estimand`·`닫힘`·`마감` grep 0건이고, /governance 로 나가는 건 66줄 각주 링크 하나다. 이 규율이 왜 생겼는지도 CLAUDE.md 에 적혀 있다 — "SDCP-doped 흡착에너지를 여덟 번 계산했고 여덟 번 반려됐다". 그리고 지금 이 순간 09-07~08 에 비준된 카드가 셋이다(decisions.json 의 D-2026-09-08-lpsocl-box331-closure-conditions · D-2026-09-08-cascade-d-rel-estimand · D-2026-09-08-b2o3-uma-vs-dft-force, 전부 `results_seen: false` 로 봉인).
- **고치는 법**: 규율 카드 맨 위에 0번 규율로 넣는다 — "입력을 만들기 전에: 이 양이 보고량 카드에 정의돼 있나? 게이트를 결과 보기 전에 정했나?" + /governance 의 해당 결정으로 직결 링크. 조성별로 활성 카드가 있으면 그 조성을 골랐을 때 배너로 띄운다(b2o3·lpsocl·cascade 는 지금 있다).
- codex 필요: False

### [P2·buried] methods-single-scroll-no-toc
- **어디**: `webapp/templates/doc.html:151 (`<div class="doc">{{ content|safe }}</div>`) · webapp/app.py:454-460`
- **근거**: /methods 렌더 결과가 57 KB HTML 한 덩어리다(원문 382줄 / 29.5 KB). doc.html 에는 목차·앵커 내비·검색이 없고, md_html 의 `toc` 확장은 원문에 `[TOC]` 마커가 있어야 목차를 그리는데 이 문서에는 없다. 실제 렌더를 보면 헤더 h1 `계산 방법 Canonical (단일 기준)` 바로 아래에 문서 자신의 h1 `계산 방법 Canonical — 단일 기준 (2026-07-23 재정리 · 2026-08-20 축 4개 추가)` 이 또 나온다. 값을 확인하러 온 사람이 §4 gap 표(120줄)나 §6 Ea 표(141줄)를 보려면 매번 스크롤로 찾아야 한다.
- **고치는 법**: doc.html 에 `<h2>` 를 긁어 만드는 sticky 목차를 붙인다(다른 doc 라우트 /todo·/sdcp 도 같이 좋아진다). 문서 첫 h1 은 페이지 헤더와 중복이므로 렌더에서 한 단계 내리거나 숨긴다.
- codex 필요: False

### [P2·ia] fairchem-isolated-from-ledger
- **어디**: `webapp/templates/fairchem.html:38,147,197 (내부 링크 전부) · webapp/templates/base.html:70-77 (사이드바 묶음)`
- **근거**: /fairchem 의 내부 링크는 `/`(대시보드), `/literature`, 그리고 `/api/fairchem/v1/<n>` raw JSON 10개가 전부다 — /governance · /methods · /compute 로 가는 링크가 0 이다. 반대로 /methods 도 /fairchem 을 안 부른다(/compute 만 64줄에서 링크). 그래서 화면 ③ 의 판정 행 `Catalysis transition-state tooling and general MLIP forces → diagnostic_only_until_dft` 를 보고도, 그 "until DFT" 를 실제로 집행하는 09-08 결정(D-2026-09-08-b2o3-uma-vs-dft-force, `보고량은 R = dF_frame(b2o3) / dF_frame(modelc)`)으로 갈 길이 없다. 사이드바 위치도 `문헌 · 검증` 인데 실질은 엔진 한계 = 계산 걸기 전 필독이다.
- **고치는 법**: crosswalk 행마다 관련 decision id 를 FK 로 달아 /governance#<id> 로 링크한다(수치를 복사하는 게 아니라 링크라 이 파일의 읽기전용 규율에 안 걸린다). /methods §6 상단에 /fairchem 링크를 넣고, 사이드바에서 Fair-Chem 을 `계산 돌리기` 로 옮기거나 양쪽에 둔다.
- codex 필요: False

### [P2·missing] fairchem-uma-own-paper-absent
- **어디**: `db/knowledge/fairchem/papers.json (42편) · webapp/templates/fairchem.html:131-161`
- **근거**: 42편 전수 확인 결과 카테고리가 Universal Models & Architectures(5) · Datasets(10) · Generative Models(6) · Sampling & MD(3) · Applications & Discovery(5) · Training Methods(6) · Electronic Structure(4) · Perspectives(3) 이고, **UMA 원논문이 없다**(제목에 'UMA'·'universal' 매칭 0건). 그런데 우리가 실제로 인용하는 건 그 논문이다 — /compute 의 Li₃N 금지 규율이 `UMA 원논문 **부록 G** 가 우리 버전·우리 task 의 진공/저배위 병리를 직접 지목한다` 로 근거를 대고 있고, litdb 에는 `litdb/papers/uma2026_family_of_universal_models_for_atoms.md` 로 들어와 있다. 화면은 우리와 무관한 42편(OC20 촉매·생성모형 등)을 접힌 표로 다 보여주면서 정작 유일하게 결정적인 논문은 안 보여준다.
- **고치는 법**: papers 절 맨 위에 "우리가 실제로 인용하는 UMA 논문" 고정 카드를 만들어 litdb digest(`/literature` 의 해당 slug)와 부록 G 로 직결한다. 42편 표는 지금처럼 접어 두되 우리 계 관련(Universal Models · OMat24) 만 기본 노출하고 나머지는 더 접는다.
- codex 필요: False

### [P2·missing] compute-canonical-runner-not-viewable
- **어디**: `webapp/templates/compute.html:108-109 · webapp/data.py:4801-4811 (safe_repo_path)`
- **근거**: /compute 가 `못 읽으면 **시작하지 않는다** — 정본 러너 tools/doping/run_force_check_scf.sh 가 이 전부를 강제한다` 라고 정본을 지목하는데, 그 파일을 앱에서 볼 방법이 없다. `/api/file/<rel>` 은 safe_repo_path 를 타고 그 docstring 이 `docs/ · db/ 안으로만` 이며 `_ATT_ROOTS` 에 tools/ 가 없다. /files 화면도 마찬가지다. 같은 문제가 MD 정본 러너(tools/ionic/run_arrhenius_6pt.sh · tools/modelc_v3/disorder_ensemble_diffusion.py)에도 걸린다.
- **고치는 법**: `_ATT_ROOTS` 에 `tools/` 를 읽기 전용으로 추가하고(경로 탈출 가드는 그대로), 화면의 스크립트 경로를 `/api/file/tools/...` 링크로 바꾼다. 저장소를 안 보고도 정본을 대조할 수 있어야 붙여넣기 블록을 신뢰할 수 있다.
- codex 필요: False

### [P2·broken] claimflag-tooltip-raw-markdown
- **어디**: `webapp/canonical.py (annotate_claims 가 만드는 title 속성) — 실물 확인은 /methods 렌더`
- **근거**: /methods 의 자동 결속 태그가 이렇게 나온다: `title="⛔ 철회 — 인용 금지 · … · 대신: 저온 구간만: Ea = 0.2241 ± 0.0606 eV (600→800 K, 3시드 **각각** 적합)."` — 툴팁 안에 마크다운 별표가 그대로 보인다. 2026-09-08 커밋 fc3624184 가 `webapp: 카드·메모의 마크다운이 화면에 기호로 노출되던 것 정정` 으로 같은 계열 버그를 고쳤는데 이 경로는 안 걸렸다.
- **고치는 법**: 레지스트리 문자열을 title 에 넣기 전에 `**`·`` ` `` 를 벗긴다(index.html 의 mdlite 와 같은 처리를 텍스트 전용 버전으로).
- codex 필요: False

### [P2·ia] compute-rules-push-tool-below-fold
- **어디**: `webapp/templates/compute.html:18-67 (규율 카드) vs 69-91 (실제 도구)`
- **근거**: 페이지 순서가 [보라색 '이 페이지가 무엇인가' + 규율 5줄 카드 ~50줄] → [조성 드롭다운 · 계산타입 버튼] → [출력] 이다. 카드 안 주석이 그 의도를 밝힌다: `이 페이지는 **입력을 만드는 곳**이라, 하드코딩된 규율이 여기 있어야 실제로 지켜진다.` 의도는 맞지만 결과적으로 도구가 첫 화면 밖이고, 재방문자는 매번 같은 5줄을 지나쳐야 한다.
- **고치는 법**: 도구(드롭다운+버튼+출력)를 위로, 규율은 한 줄 요약 스트립 + `<details>` 로 접는다. 단 **선택한 조성·계산에 걸리는 규율만** 자동으로 펼친다(MD 고르면 --save_traj·MSD 창·Li₃N, GPU 서버 고르면 VRAM·ldd) — 그러면 지금보다 더 지켜진다.
- codex 필요: False
