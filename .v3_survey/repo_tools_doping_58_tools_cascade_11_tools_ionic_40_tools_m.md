# repo — tools/doping(58) · tools/cascade(11) · tools/ionic(40) · tools/modelc_v3(21) = 실물 130개 스크립트

## 지금 무엇인가
네 디렉터리는 서로 다른 시대의 지층이다 — cascade(11개)는 2026-08~09 에 다시 쓰인 감사·게이트 도구로 docstring 에 "못 하는 것"과 사고 이력이 다 붙어 있고, doping(58개)은 2026-05~06 의 273 캐스케이드 공장 라인 + 2026-08~09 의 축·게이트 도구가 섞여 있고, ionic(40개)은 MD 판정 도구(msd_diffusive_check 2558줄 등)와 2026-06 의 일회성 슬라이드 플로터가 한 폴더에 있고, modelc_v3(21개)는 사실상 2026-06 화석(21개 중 17개가 6월 커밋이 마지막)이다. 규율 준수는 디렉터리별로 갈린다: --selftest 32/130 · "못 하는 것" 40/130 · kb 카드 역참조 22/130 · house_style 2/18(플로터). 실제로 연 것: cascade 11개 전부(head -22), modelc_v3 21개 전부(head -14) + disorder_ensemble_diffusion·nernst_einstein_300K·run_b2o3_md·run_highT_reseed 본문, ionic 22개 헤더 + 6개 전문, doping 37개 헤더 + axis_corr_csv·run_md_sigma·bvse_proxy·run_force_check_scf 부분. **못 본 것: doping 약 21개(dft_decomp_check·generate_dft_inputs·substitute_compound/struct·site_preference(_swap)·run_anneal·run_uma_screening·run_mlip_postproc·run_cathode_interface·convex_hull_ehull·preflight·b2o3_enumerate 등)의 본문, ionic 14개(aimd_jump_stats·anion_rotation_acf·make_md_supercell·pmf_path_profile·run_arrhenius_6pt·watch_lpsocl_400ps 등)의 본문, cascade 11개 전부의 본문.**

## 처음 오는 사람
막힌다. 네 디렉터리 어디에도 README·INDEX 가 없어서(tools/ 전체에서 README 는 tools/adhesion_v30u/ 하나뿐) 130개 파일 중 무엇이 정본 파이프라인이고 무엇이 2026-06 일회성인지 알 방법이 파일명뿐이다. doping 은 tier_cascade.sh 가 사실상 목차 역할을 하지만 그걸 열어봐야 알 수 있고, ionic·modelc_v3 는 그런 것도 없다 — `plot_msd_3sys.py` `plot_msd_slide.py` `plot_msd_compare.py` `msd_origin.py` `msd_refit_window.py` `msd_diffusive_check.py` 여섯이 나란히 있는데 어느 것이 인용 게이트고 어느 것이 죽은 슬라이드용인지 이름으로 안 갈린다. 반대로 잘 되는 것도 있다: cascade 는 어느 파일을 열어도 첫 20줄이 "왜 생겼나 / 무엇을 재나 / 못 하는 것"을 말해서 처음 봐도 읽힌다. 그리고 tools 파일에서 그 판정이 실린 kb 카드로 가는 링크가 130개 중 22개에만 있어서, 도구 → 결정 방향의 역추적이 거의 안 된다(나중의 LLM 이 기억을 되찾을 때 제일 아쉬운 지점이 여기다).

## 건드리면 안 되는 것
- tools/cascade/ 11개의 docstring 서술 방식 — '왜 생겼나 / 무엇을 재나 / 못 하는 것 / 실패 이력' 네 절. build_cascade_audit_manifest.py 의 '생산자는 sidecar 만 쓴다, 최종 manifest 는 이 도구만 쓴다' 나 cascade_ids.py 의 '2026-08-16 하루에 이 함정을 세 번 밟았다' 같은 사고 기록은 재편할 때 압축하거나 요약하지 말 것. 이게 이 저장소에서 제일 잘 된 부분이고, 나머지 세 폴더가 따라가야 할 본이다.
- tools/ionic/msd_diffusive_check.py (2558줄) 전체 — 크다고 쪼개지 말 것. β=0.80 하드게이트 폐기(§7-5), `_covers()` 가 생긴 이유(2026-08-29 회신 S: 창 50–200 을 요청했는데 50–100 을 맞추고 라벨만 붙였다), Haven 합성시험(독립 랜덤워크 H_R≈1 / 완전상관 H_R=1/N) — 판정 근거가 전부 코드와 같은 파일에 있다. 나누면 판정과 근거가 갈라진다.
- tools/convention_check.py 의 EXEMPT 5건 — 전부 사유가 적혀 있고 다 타당하다(beta_null_test 는 창 사다리가 목적, msd_refit_window·msd_diffusive_check 는 창 스캔 진단, md_temperature_feasibility 는 역산, b2o3_all_bond_lengths 는 Å 창). 새 위반을 EXEMPT 로 덮는 것만 막으면 된다.
- tools/modelc_v3/run_highT_reseed.sh 의 가드 두 개 — flock(왜 pgrep 이 아닌지 이유 포함)과 'msd.json 은 있는데 traj.xyz 가 없으면 즉사' resume 함정 가드. 후자는 2026-07 에 msd.json 12개·traj 0개로 조용히 끝난 사고(F9)의 재발 방지다. 이 두 블록이 다른 런처로 복사돼야지, 여기서 없어지면 안 된다.
- tools/ionic/watch_kgy.py:468-474 의 '⚠⚠ 2026-09-04 — 이 계획표는 낡았다' 자기고백 블록. 낡은 CLOSE_PLAN 을 지우지 않고 '왜 낡았는지 + 지금 감시는 watch_lpsocl_400ps.sh' 를 붙여 둔 방식이 정답이다. 정리한다고 옛 계획을 삭제하면 왜 바뀌었는지가 사라진다.
- tools/modelc_v3/nernst_einstein_300K.py 상단의 '⛔ 2026-09-07 CORRECTION' 블록 — 옛 문장이 무엇이었고 어디가 부호가 반대였는지를 원문째로 남겨 뒀다. 이런 정정 기록은 요약 금지(원문을 고쳐 쓰면 이력이 깨진다는 CLAUDE.md 용어 규율과 같은 이유).
- tools/doping/axis_corr_csv.py 의 커버리지 표시 방식 — 실행해 보면 σ(300K) 0/237 · 부착일 W_ad 0/237 · D비(vs host) 0/237 을 '· 0/237 (0.0 %)' 로 찍고 판정에서 뺀다. 없는 것을 0 으로 표시하지 않고 '원장 부재' 로 보여주는 정확한 구현이라 그대로 둘 것. 파생축(li_mobility_score)을 '📐 정의상 — 발견이 아니라 공식이다' 로 따로 표시하는 것도 유지.
- tools/doping/run_force_check_scf.sh:64-118 의 ldd 유도 블록 — CLAUDE.md 2026-09-08 규칙의 유일한 실물 구현이다. 다른 파일이 이걸 복사해 가야 하지 그 반대가 아니다.
- master_batch_273.sh · tier_cascade.sh · run_compound_batch.sh — 끝난 캠페인이지만 273 슬롯 데이터(cascade_v23_all.csv 3615행)를 어떻게 만들었는지의 유일한 기록이다. 아카이브로 접는 건 되지만 삭제 금지.
- b2o3_kisti_restage.py · make_run4_relax_input.py 같은 일회성 복구 스크립트 — 재사용 가치는 0 이지만 'V100 이 EOS 중간에 죽었을 때 무엇을 했나' 의 기록이다. 아카이브로.

## 발견

### [P0·wrong] b2o3-md-runner-off-convention
- **어디**: `tools/modelc_v3/run_b2o3_md.sh:28-31`
- **근거**: 드라이버 호출이 `--temperatures 600 800 1000 --equilib_ps 5 --prod_ps 50 --device '$DEVICE'` 로 끝난다 — `--fit_window_ps` 가 없다. 드라이버 기본값은 tools/modelc_v3/disorder_ensemble_diffusion.py:321 `ap.add_argument("--fit_window_ps", type=float, nargs=2, default=[5.0, 40.0])` 다. 즉 이 러너로 나온 D 는 **MSD 창 5–40 ps** 로 적합된 값이지 CLAUDE.md 정본 2–50 ps 가 아니다. prod 도 50 ps 로 정본 200 ps 와 다르고, `--save_traj` 도 `--seed` 도 없다. 같은 폴더의 run_highT_reseed.sh:144 는 `--save_fs 100 --fit_window_ps 2 50 --seed ${S} --save_traj` 를 다 넣는다.
- **고치는 법**: run_b2o3_md.sh 호출에 `--fit_window_ps 2 50 --save_traj --prod_ps 200 --seed <N>` 추가. 그리고 이 러너로 만든 기존 b2o3 D 가 db 어디에 들어갔는지 계보를 확인 — 5–40 창 값이 섞여 있으면 그 자리에 창을 명시한다.
- codex 필요: False

### [P0·broken] msd-window-default-blindspot
- **어디**: `tools/modelc_v3/disorder_ensemble_diffusion.py:321 · tools/modelc_v3/aimd_mlip.py:265`
- **근거**: 두 MD 드라이버의 기본 MSD 창이 정본(2,50)이 아니다 — disorder_ensemble_diffusion.py `default=[5.0, 40.0]`, aimd_mlip.py `default=[2.0, 20.0]`. 그런데 `python3 tools/convention_check.py` 는 `RESULT: 0 위반` 을 낸다. 이유는 검사기의 정규식이 `WINDOW_ASSIGN = re.compile(r"^\s*(\w*[Ww][Ii][Nn][Dd][Oo][Ww]\w*)\s*(?::[^=]+)?=\s*(.+)$")` 라 **변수 대입만** 보고 `ap.add_argument(...)` 안의 default 는 못 본다. 검사기 자신이 docstring 에 '정규식 기반이라 AST 수준 우회를 못 본다' 고 적어 뒀지만, 실제로 새는 자리가 **생산 드라이버의 기본값**이다.
- **고치는 법**: convention_check.py 에 argparse default 패턴(`add_argument(... default=[a, b] ...)` 중 이름에 window 가 든 것)을 추가하고, 두 드라이버의 default 를 [2.0, 50.0] 으로 바꾸거나 '기본값 없음(필수 인자)' 으로 강제한다. 후자가 더 안전하다 — 창을 안 적으면 시작 안 하게.
- codex 필요: False

### [P0·wrong] haven-range-retracted-still-live
- **어디**: `tools/doping/run_md_sigma.py:16-17,239-241,281 · tools/ionic/hops_per_ion.py:21,101,110`
- **근거**: db/properties/li_transport.json 이 2026-09-07 에 명시적으로 철회했다: "⛔ The former wording here quoted a literature range 'H_R ≈ 0.3-0.7' — that range is NOT ours and must not be used to rescale our σ" · 우리 실측은 H_R = 0.84 ± 0.06. 그런데 run_md_sigma.py:16 은 아직 "Real σ ≈ H_R × σ_NE (H_R ≈ 0.3-0.7 for argyrodites). Conservative reporting: divide by 2 for upper bound" 이고, :239 는 그 문장을 산출 JSON 의 `caveats` 필드에 **써 넣는다**. 방향까지 반대다 — tools/modelc_v3/nernst_einstein_300K.py 가 같은 날 '⛔ 2026-09-07 CORRECTION … The second half had the SIGN BACKWARDS … H_R < 1 makes NE an UNDER-estimate, not an upper bound' 로 고친 바로 그 오류다. hops_per_ion.py:110 은 더 나빠서 `f.write("# UPPER BOUND: back-correlated hops (Haven 0.3-0.7 < 1) are not counted,\n")` 로 db/properties/hops_per_ion.csv 헤더에 박아 놨고, 그 파일 3행에 실물로 남아 있다.
- **고치는 법**: 세 파일에서 0.3–0.7 문구를 지우고 실측 H_R = 0.84 ± 0.06(진단용·인용 불가, db/properties/haven_ratio_measured_2026_09_07.json) 로 교체 + '나누기 2' 지시 삭제(부호 반대). db/properties/hops_per_ion.csv 는 도구를 고친 뒤 재생성.
- codex 필요: False

### [P0·broken] plot-msd-3sys-dead-src
- **어디**: `tools/ionic/plot_msd_3sys.py:7,29,64-66`
- **근거**: 입력이 세션 스크래치패드에 하드코딩돼 있다: `SRC = "/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/82ea256b-.../scratchpad/msd_LPSCl_LPSCl16_b2o3.csv"` — 실측 `No such file or directory`. 출력도 같은 스크래치패드로 나간다. 게다가 적합창이 `def fit_slope(tt, msd, lo=5.0, hi=49.0)` 로 정본 2–50 이 아니고(convention_check 가 못 잡는다), 600 K 패널에 `"σ ≈ 1.3× (not a barrier effect)"` 를 찍는다. 1.33× 는 CLAUDE.md 가 '단일시드 1.33× 철회 사례, SEMIFINAL 2026-07-09' 로 못 박은 값이고, tools/ionic/build_final_conductivity.py:42 도 '# The old 1.33x rested on the single-seed 800K pair' 라고 적는다. 현행 정본은 db/properties/b2o3_vs_lpscl16_conductivity.csv 의 `ratio_b2o3/LPSCl1.6 … 1.08+/-0.18 / 0.82+/-0.15 / 1.15+/-0.12`.
- **고치는 법**: SRC 를 이미 커밋된 `docs/figures/msd_compare/msd_3sys_LPSCl_LPSCl16_b2o3.csv`(열 이름이 정확히 일치한다) 로 바꾸고, 창을 2–50 으로, 주석 상자를 '1.08±0.18 (600 K, 3-seed) — 구별 안 됨' 으로 교체. 못 고칠 거면 이 파일은 지우는 게 낫다(그림은 이미 docs 에 있다).
- codex 필요: False

### [P1·wrong] plot-arrhenius-absolute-sigma
- **어디**: `tools/ionic/plot_arrhenius.py:21,25,68-70`
- **근거**: 산출 CSV 헤더에 절대 σ 를 그대로 쓴다: `"# modelc(LPSCl1.6): Ea=0.2235 eV D0=5.80e-4 sigma300~14mS/cm | nd(Nd2O3-doped): Ea=0.2267 D0=3.78e-4 sigma300~7.3mS/cm"`. CLAUDE.md 는 'σ는 Nernst–Einstein(Haven=1) — **절대값 인용 금지**'. 같은 파일이 세 줄 뒤에 `# CAVEAT: … cite RATIO + Ea, not absolute sigma` 라고 적으면서 그 위에 절대값을 실어 보낸다. Ea 도 0.2235/0.2532 인데 db/properties/citation_hazards.json 에 `{"file":"db/properties/li_transport.json","level":"HOLD","what":"Ea","why":"같은 확산영역 게이트"}` 로 등재된 값이고, 화면·CSV 어디에도 그 HOLD 를 안 적는다. docstring 은 'Data = db/properties/li_transport.json' 이라고 하지만 실제로는 D 배열이 소스에 리터럴로 박혀 있어 json 을 읽지 않는다.
- **고치는 법**: CSV/그림에서 sigma300 두 값 삭제(비만 남긴다) · Ea 옆에 `HOLD: ⚠_DIFFUSIVE_GATE_2026_08_01` 표기 · 숫자를 li_transport.json 에서 실제로 읽도록 바꾸거나 docstring 의 'Data =' 를 '값은 아래 리터럴에 고정(2026-06-24 스냅샷)' 으로 정직하게 고친다.
- codex 필요: False

### [P1·useless] slide-scripts-no-contract
- **어디**: `tools/ionic/plot_dual_mechanism.py (22줄) · tools/ionic/plot_msd_slide.py (22줄)`
- **근거**: 둘 다 docstring 0줄·argparse 0줄·selftest 0. plot_dual_mechanism.py 는 `s0=3.4; fEa=3.2; fcar=1.41` 로 σ 절대값을 소스에 박고 `ax.axhline(14,...)` + `"observed LPSCl$_{1.6}$ σ≈14"` 를 그린다(절대 σ 금지 위반). plot_msd_slide.py 는 `fitmask=(t>=20)&(t<=90)` 으로 20–90 ps 창을 쓰고(정본 2–50), 입력을 `/home/user/Yonghoon-DEM-DFT/docs/figures/...` 절대경로로, 출력을 `/tmp/msd_slide.png` 로 고정한다. 둘 다 이 저장소 규율 이전(2026-06-21)의 발표용 낙서인데 tools/ 정식 자리에 남아 있다.
- **고치는 법**: 둘 다 삭제하거나 tools/_attic/ 같은 접힘 자리로 옮긴다. 살릴 거면 절대 σ 제거 + 창 2–50 + argparse + house_style 을 붙여야 하는데, 그러면 사실상 새로 쓰는 것이라 삭제가 맞다.
- codex 필요: False

### [P1·broken] build-final-conductivity-no-contract
- **어디**: `tools/ionic/build_final_conductivity.py:1,22,60-62`
- **근거**: 정본 CSV `b2o3_vs_lpscl16_conductivity.csv` 와 그림 `b2o3_vs_lpscl16_arrhenius_3seed.png` 를 만드는 유일한 생산자인데 1행이 `import numpy as np, csv` 다 — docstring 없음·argparse 없음·selftest 없음. 출력 경로가 `open("b2o3_vs_lpscl16_conductivity.csv","w")` 로 **현재 작업 디렉터리** 라, repo 루트에서 돌리면 db/properties/ 가 아니라 루트에 떨어진다. 자기가 그 결함을 적어 두기까지 했다: `"#   lineage binding = UNWIRED -- this script hardcodes D instead of reading upstream msd.json."` 그리고 D 9×2 개가 전부 소스 리터럴이다.
- **고치는 법**: 출력 경로를 db/properties/ 절대경로로 고정 + argparse(--out, --selftest) + 상단에 이 파일이 정본 두 개의 유일한 writer 라는 docstring. 계보 결선(msd.json 읽기)은 별건이라 지금 안 해도 되지만, 최소한 CWD 기록은 즉시 막아야 한다.
- codex 필요: False

### [P1·wrong] lpsocl-fig-seed-contradiction
- **어디**: `tools/ionic/fig_lpsocl_arrhenius.py:5-6,28-32,86-88,100-102`
- **근거**: 한 파일 안에서 세 곳이 서로 다른 말을 한다. docstring: `"LPSOCl: 600 K reseeded x4 (ladder+s2/s3/s4, 200 ps each) -> Ea error bar; 800/1000 K single-seed."` · 그림 캡션: `"ALL T = 4 seeds (dots=seeds, whisker=min-max, square=mean)"` · 자기가 쓰는 CSV 의 note 열: `"600K=4seed mean" if tt == 600 else "single seed"`. 그런데 SEEDS 배열은 4×3(세 온도 모두 4개 값)이다. 셋 중 최소 하나는 거짓이고, 산출물은 db/properties/lpsocl_arrhenius_origin.csv 로 정본 자리에 들어간다. 덧붙여 죽은 코드가 남아 있다 — `def line(D3, T3=T)` 는 아무도 안 부르고, `ax.plot(xfit, np.exp(b + s * (xfit / 1000.0) ** -1 * 0 + s * (1000.0 / xfit) / 1000.0 * 0), alpha=0)  # noop` 와 `yy = np.exp(b + s * xfit)`(미사용)가 그대로다.
- **고치는 법**: 원본 msd.json 트리에서 800/1000 K 시드 수를 확인해 세 곳을 하나로 맞추고, noop 라인과 미사용 `line()`·`yy` 삭제. 앵커로 쓰는 Ea_mod=0.2235 / Ea_b=0.2234 도 3-seed 정본(0.197±0.032 / 0.199±0.034)으로 갱신하거나 '단일시드 앵커' 라고 화면에 적는다.
- codex 필요: False

### [P1·wrong] bvse-two-parameter-sets
- **어디**: `tools/doping/bvse_proxy.py:46-58 vs tools/comp1_v3/bvse_standalone.py:21-23`
- **근거**: 같은 저장소에 Li–음이온 R0 표가 둘이다. 정본(CLAUDE.md 명시, comp1_v3): `"S": (2.105, 0.37) · "Cl": (2.249, 0.37) · "O": (1.466, 0.37)`. doping 쪽: `'S': {'R0': 1.94, 'b': 0.40} · 'Cl': {'R0': 1.91, 'b': 0.37} · 'O': {'R0': 1.466, 'b': 0.37}` (주석은 'Brown & Altermatt 1985 / Adams 2003'). BVS = Σ exp((R0−d)/b) 라 Cl 의 0.34 Å 차이는 이웃 하나당 exp(0.34/0.37) ≈ 2.5배다. 그런데 doping 쪽 표로 나온 `bvs_li_proxy_score`·`migration_volume_fraction` 이 cascade_v23_all.csv 축이 되고 build_screening_funnel.py 의 G4 게이트(`ionic_transport norm > 0.30`)를 통과시킨다. 두 파일 어디에도 상대 표의 존재가 안 적혀 있고, convention_check.py 도 R0 를 안 본다.
- **고치는 법**: 두 docstring 에 서로의 존재와 '왜 다른 표를 쓰는가'를 명시(최소). 그 위에 진짜 질문 — cascade 의 BVSE 축을 softBV 표로 다시 매겨야 하는가 — 는 47종 순위가 바뀔 수 있어 1저자/외부 판단이 필요하다.
- codex 필요: True

### [P1·stale] qegpu-hardcoded-mpi
- **어디**: `tools/doping/b2o3_stage2_dft.py:52-57 · tools/doping/b2o3_dft_eos.py:40-41 · tools/doping/b2o3_eos_kisti_short.sh:29`
- **근거**: b2o3_stage2_dft.py 가 생성하는 런처에 gabia 경로가 통째로 박혀 있다: `MPIRUN=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin/mpirun` + 같은 hpcx 의 OPAL_PREFIX/LD_LIBRARY_PATH. b2o3_dft_eos.py:40 도 같은 hpcx 를 PATH 에 밀어 넣고 `MPIRUN=${MPIRUN:-mpirun}`. CLAUDE.md 가 2026-09-08 에 못 박은 규칙과 정면으로 어긋난다 — '⛔⛔ QE-GPU 런타임은 추측하지 말고 `ldd` 로 바이너리에게 묻는다 … kgy 의 pw.x 는 hpcx 가 아니라 `~/apps/openmpi-4.1.6` 로 빌드돼 있었다'. 같은 규칙을 제대로 구현한 것은 tools/doping/run_force_check_scf.sh:85-97 하나뿐이다(`export OPAL_PREFIX="$mprefix"` 를 ldd 결과에서 유도, libnvomp+libgomp 동시 링크면 OMP_NUM_THREADS=1).
- **고치는 법**: run_force_check_scf.sh 의 ldd 유도 블록을 공용 셸 함수로 빼서 세 파일이 같이 쓰게 한다(새 파일 말고 기존 스크립트에 함수 추출 + source). 최소한 세 파일 상단에 '이 경로는 gabia 전용, 다른 기계에서는 run_force_check_scf.sh 의 ldd 유도를 쓸 것' 을 적는다.
- codex 필요: False

### [P1·stale] reseed-runner-headers-stale
- **어디**: `tools/modelc_v3/run_modelc_600K_reseed.sh:6-7,27 · tools/modelc_v3/run_highT_reseed.sh:6-7`
- **근거**: run_modelc_600K_reseed.sh 헤더: `"# WHY: b2o3 is already 3-seeded (Ea = 0.206 +0.038/-0.030). LPSCl1.6 is still a single-seed 0.2235 with no bar"`. 두 수치 다 지난 판이다 — citation_hazards.json 이 b2o3 Ea 를 '헤드라인이 3회 교체됨 (0.207 → 0.2234 단일시드 → 0.199±0.034)' 로 기록하고, 정본 CSV 는 b2o3 0.199±0.034 / LPSCl1.6 0.197±0.032(둘 다 3-seed)다. 즉 이 스크립트가 '해야 한다' 고 주장하는 일은 이미 2026-07-06/07 에 끝났다. run_highT_reseed.sh:6-7 도 같다: `"The apparent b2o3 advantage sits at the SINGLE-seed 800K (ratio 1.57) / 1000K (1.19)"` — 재시드 뒤 정본 비는 0.82±0.15 / 1.15±0.12 다. (run_highT_reseed.sh 는 2026-09-08 에 손댔는데도 WHY 문단만 7월 상태로 남았다.)
- **고치는 법**: 두 헤더 맨 위에 '✅ 이 캠페인은 2026-07-06/07 에 완료 — 결과는 db/properties/b2o3_vs_lpscl16_conductivity.csv' 한 줄을 박고, 옛 근거 수치에는 (superseded) 를 붙인다. 스크립트 자체는 재실행 가능성이 있으니 지우지 말 것.
- codex 필요: False

### [P1·wrong] held-ea-in-docstrings
- **어디**: `tools/ionic/cage_jump_descriptors.py:11-12 · tools/ionic/plot_arrhenius.py:21,25 · tools/modelc_v3/nernst_einstein_300K.py:201,205`
- **근거**: cage_jump_descriptors.py 는 자기 지표를 '정량 값과 같이 제시하라' 면서 `"the quantitative AIMD Ea (comp1 0.253 eV, modelc 0.223 eV)"` 를 쓴다. 이 둘은 db/properties/li_transport.json 값이고 citation_hazards.json 에서 level=HOLD(⚠_DIFFUSIVE_GATE_2026_08_01)다 — '정량' 이라고 부를 수 없는 상태다. 반대로 잘 적은 사례가 같은 폴더에 있다: tools/ionic/md_temperature_feasibility.py:39 `"⚠ li_transport.json 헤드라인은 Ea 0.2235(단일시드 계열). 멀티시드 0.197±0.032 를 쓴다"` · tools/ionic/run_comp1_seeds.sh:5 `"modelc Ea 정본 충돌(0.2235 단일 deck vs 0.197±0.032 3-seed)"` · tools/modelc_v3/watch_b2o3_md.sh:20 `"철회된 Ea 0.207 이 화면에 남았다"`. 즉 결속을 하는 파일과 안 하는 파일이 섞여 있다.
- **고치는 법**: HOLD/철회 값을 쓰는 자리마다 md_temperature_feasibility.py:39 형식(값 + 지위 + 정본 대체값)을 그대로 복사한다. 규칙화하려면 tools/db/ 쪽 검사기에 'tools/ 안의 0.2235/0.2234/0.2532/0.207 리터럴은 지위 표기 필수' 를 붙이는 게 싸다.
- codex 필요: False

### [P1·missing] no-tools-index
- **어디**: `tools/doping/ · tools/cascade/ · tools/ionic/ · tools/modelc_v3/ (네 폴더 모두 README/INDEX 없음)`
- **근거**: `find tools -maxdepth 2 -iname '*README*' -o -iname 'INDEX*'` 결과가 tools/adhesion_v30u/README.md 하나뿐이다. CLAUDE.md 코드 규율은 새 스크립트 전에 '② tools/ 에 이미 있나(`grep -rl`)' 를 요구하는데, 130개 파일에서 grep 만이 유일한 발견 수단이다. 실제 사고 흔적도 있다 — tools/doping 에 MSD·EOS·랭킹 도구가 중복으로 쌓였고(아래 duplicate 항목), tools/ionic 에 MSD 도구가 6개다. kb 카드로 가는 역링크도 doping 7/58 · cascade 4/11 · ionic 9/40 · modelc_v3 2/21 로 전체 22/130 뿐이다.
- **고치는 법**: 각 폴더에 20~40줄짜리 INDEX.md: (a) 정본 파이프라인 순서 3~6줄, (b) 파일별 한 줄 + 지위(정본/진단/화석), (c) 관련 kb 카드 링크. 손으로 쓰지 말고 docstring 첫 줄을 긁어 만드는 생성기 하나(기존 tools/kb_wiki.py 확장이 새 파일보다 낫다)로 재생성 가능하게.
- codex 필요: False

### [P1·useless] dead-campaign-watchers
- **어디**: `tools/doping/watch_phase1_v22.sh · watch_dualx.sh · watch_dualx_compare.sh · watch_cascade.sh · master_batch_105.sh · tools/ionic/watch_comp2_all.sh · watch_comp2_disorder.sh · watch_comp2_md.sh`
- **근거**: 전부 끝난 캠페인의 감시판이다. watch_phase1_v22.sh:14 `BATCH_DIR="${BATCH_DIR:-/data/work/runs/multi_category_2026_05_19_v22}"` — v22 는 v23 로 대체됐고 kb/open_items.md 에 v22 항목이 없다. watch_dualx*.sh 3종은 dualx_v23 전용인데 open_items 에 dualx 언급이 0건. watch_comp2_*.sh 3종은 open_items:376 에 `"### 2. 🟡 comp2 disorder ensemble — d=0.5 판정 완료 / d=1.0 측정 실패 (2026-08-01)"` 로 종료 기록만 있다. master_batch_105.sh 는 저장소 전체에서 kb/projects/external_review_prompt_digital_twin_2026_05_18.md 한 곳에서만 언급된다(273 판으로 대체). 여덟 파일이 활성 도구와 같은 평면에 섞여 있어서, 'watch 를 뭘 쓰지' 할 때마다 골라내야 한다.
- **고치는 법**: tools/doping/_archive/ · tools/ionic/_archive/ 로 옮기고 INDEX.md 에 '끝난 캠페인' 절로 접는다. 지우지는 말 것 — 감시판은 그 캠페인이 무엇을 봤는지의 기록이다.
- codex 필요: False

### [P2·broken] watch-dualx-dangling-target
- **어디**: `tools/doping/watch_dualx.sh:14`
- **근거**: `if [ "$SUF" = lowx ]; then DPID=$(pgrep -f "run_dualx.sh" | head -1)` — 그런데 `find . -name 'run_dualx*.sh'` 는 tools/doping/run_dualx_highx.sh **하나만** 낸다. run_dualx.sh 는 저장소에 없다(run_dualx_highx.sh:2 도 'companion to run_dualx.sh' 라고 참조만 한다). 즉 lowx 모드는 영원히 드라이버를 못 찾는다.
- **고치는 법**: 위 아카이브 이동과 함께 처리. 남긴다면 lowx 분기에 '드라이버 스크립트가 저장소에 없다(서버 로컬본이었다)' 한 줄.
- codex 필요: False

### [P1·missing] selftest-coverage
- **어디**: `tools/modelc_v3/ (21개 중 --selftest 는 nernst_einstein_300K.py 하나) · tools/ionic/mlip_committee.py (852줄, 2026-09-08 커밋, selftest 0)`
- **근거**: CLAUDE.md: '새 도구는 `--selftest` 를 단다 — 음성 경로 포함'. 실측 보유율 doping 13/58 · cascade 7/11 · ionic 11/40 · modelc_v3 1/21 = 32/130. 특히 mlip_committee.py 는 2026-09-08 까지 계속 손대는 활성 도구인데(최근 커밋 '힘 대조 회수·분석 경로 … 골격 힘 오차 비 R', 'bench --split_at', 'bench: softening 기울기 추가') 시험이 하나도 없다. `python3 tools/convention_check.py --selftests` 는 repo 전체 PASS 76 · FAIL 4 로 잘 돌고 있으므로, 붙이면 바로 스윕에 들어간다.
- **고치는 법**: 활성 도구부터: mlip_committee.py(불일치·기울기 계산의 음성 경로), tools/doping/collect_dataset.py(2026-09-08 에 seed·구조해시 열이 추가됐다), tools/ionic/build_final_conductivity.py. modelc_v3 의 6월 플로터들은 화석이라 우선순위 낮음.
- codex 필요: False

### [P2·missing] limits-section-coverage
- **어디**: `tools/modelc_v3/ 21개 중 '못 하는 것' 은 aimd_mlip.py · nernst_einstein_300K.py · watch_b2o3_md.sh 셋뿐`
- **근거**: CLAUDE.md: "도구 docstring 에 '이 도구가 못 하는 것' 을 적는다 (한계 은폐가 제일 비싼 버그)". 실측 보유 40/130. 디렉터리 격차가 크다 — cascade 7/11(가장 좋다: uma_relax_check.py 는 '⚠ 남는 후보 (a) 농도 는 이 시험으로 못 가른다' 까지 적는다) vs modelc_v3 3/21. 한계가 없는 쪽에는 fit_elastic_cij.py(에너지 곡률법은 C12 를 못 뽑아 BM-EOS K 를 빌려 온다 — 본문에 식으로만 있고 한계로는 안 적혀 있다), plot_dos.py, li_percolation.py 처럼 결과 해석이 걸린 것이 섞여 있다.
- **고치는 법**: 한 줄씩만 붙이면 된다. 우선순위는 '수치를 만들어 db 에 넣는 것' — fit_elastic_cij.py, fit_bm_eos.py, li_percolation.py, cage_jump_descriptors.py.
- codex 필요: False

### [P1·broken] no-duplicate-run-guard
- **어디**: `tools/modelc_v3/run_b2o3_md.sh · run_modelc_600K_reseed.sh · tools/ionic/run_lpsocl_md.sh · make_b2o3_licube.sh · run_vanhove_sweep.sh (+ doping 7개)`
- **근거**: CLAUDE.md 공통 규율: '실행 스크립트에 pgrep 중복실행 가드'. 실측: watch_* 를 뺀 런처 중 pgrep 도 flock 도 없는 것이 12개다 — b2o3_eos_kisti_short.sh · master_batch_105.sh · master_batch_273.sh · run_compound_batch.sh · run_dualx_highx.sh · run_site_preference_all.sh · tier_cascade.sh · make_b2o3_licube.sh · run_lpsocl_md.sh · run_vanhove_sweep.sh · run_b2o3_md.sh · run_modelc_600K_reseed.sh. 이 중 앞 다섯(GPU MD 런처)은 두 번 던지면 공유 GPU 를 그대로 겹쳐 문다. 정답 구현은 이미 옆에 있다 — run_highT_reseed.sh:47-52 `LOCK=${LOCK:-/tmp/highT_reseed.lock}; exec 9>"$LOCK" … flock -n 9 || { echo "⛔ 이미 도는 $SELF 가 있다"; exit 0; }` 이고, pgrep 을 안 쓰는 이유(래퍼까지 세서 자기 자신에 걸린다, 2026-08-03 chain_gpu_release.sh 선례)까지 적혀 있다.
- **고치는 법**: run_highT_reseed.sh 의 flock 블록 6줄을 GPU MD 런처 다섯에 복사(파일마다 LOCK 이름만 바꿈). CLAUDE.md 의 'pgrep 가드' 문구도 'flock 가드(pgrep 은 래퍼 오탐)' 로 갱신하는 게 실물과 맞다.
- codex 필요: False

### [P1·duplicate] duplicate-tools
- **어디**: `tools/cascade/analyze_cathode_reactivity.py ↔ cathode_reactivity.py · tools/modelc_v3/fit_elastic_cij.py ↔ fit_elastic_cij_stress.py · tools/modelc_v3/fit_bm_eos.py ↔ tools/doping/b2o3_eos_fit.py · tools/ionic MSD 플로터 5종`
- **근거**: (1) cascade 의 두 파일은 이름이 거의 같은데 관계가 docstring 한 줄에만 있다 — analyze_cathode_reactivity.py:4 `"cathode_reactivity.py 가 만든 94쌍 CSV 를 읽어"`. 생산자/소비자 관계지 중복은 아니지만 이름만 보면 못 가른다. (2) fit_elastic_cij.py 는 에너지곡률, fit_elastic_cij_stress.py 는 응력-변형인데 후자 docstring 이 `"off-diagonal C12 / C13 / C23 that the energy-curvature method cannot extract. No external bulk modulus needed."` 라고 스스로 상위 호환임을 선언한다 — 그런데 전자가 은퇴 표시 없이 남아 있다. (3) BM3 EOS 적합이 둘 — modelc_v3/fit_bm_eos.py(`v00.out…vNN.out`)와 doping/b2o3_eos_fit.py(`eos_v*.out`, 30줄, `if "JOB DONE" not in t: continue`). 글롭만 다르고 하는 일이 같다. (4) ionic 의 MSD 플로터 다섯(plot_msd_3sys/plot_msd_slide/plot_msd_compare/msd_origin/msd_refit_window)이 이름으로 안 갈린다.
- **고치는 법**: (1) 두 파일을 `cathode_reactivity_compute.py` / `cathode_reactivity_verdict.py` 로 개명하거나 최소한 서로의 docstring 첫 줄에 '① 생산자 ② 소비자' 를 명시. (2) fit_elastic_cij.py 상단에 '⛔ superseded by fit_elastic_cij_stress.py (C12 를 못 뽑는다) — 옛 결과 재현용' 한 줄. (3) b2o3_eos_fit.py 를 fit_bm_eos.py 의 `--glob` 플래그로 흡수(기존 도구 확장이 새 파일보다 낫다는 사다리 그대로). (4) INDEX.md 에서 '인용 게이트 / 재적합 진단 / 발표용' 세 묶음으로 나눈다.
- codex 필요: False

### [P1·ia] cascade-tools-live-in-doping
- **어디**: `tools/doping/axis_corr_csv.py (1143줄) · tools/doping/collect_dataset.py — cascade 보고량 카드 파이프라인`
- **근거**: 2026-09-07~08 의 cascade 작업 커밋이 건드린 코드는 전부 tools/doping/ 이다: `8c9338c96 cascade Step 1 — aggregate_designs 를 대표 행 선택으로 교체 (비준 카드 §2)` → tools/doping/axis_corr_csv.py, `46566ca64 cascade Step 2 — 어닐의 seed·구조해시를 축 CSV 까지 실어 나른다` → tools/doping/axis_corr_csv.py + collect_dataset.py. 정작 tools/cascade/ 는 build_cascade_audit_manifest.py 만 바뀌었다. axis_corr_csv.py:260 은 `"★ 비준된 정의 (db/properties/cascade_d_rel_estimand_2026_09_08.json §2, D-2026-09-08-cascade-d-rel-estimand, active)"` 로 cascade 카드를 직접 인용한다. 즉 'cascade' 라는 이름으로 찾으면 이 핵심 두 파일이 안 나온다.
- **고치는 법**: 물리적 이동은 import 경로를 깨니 하지 말고, tools/cascade/INDEX.md 에 '이 캠페인의 축 CSV·설계 집계는 tools/doping/axis_corr_csv.py · collect_dataset.py 에 있다' 를 명시하고 두 파일 docstring 첫 줄에 'cascade' 를 넣는다(grep 으로 잡히게).
- codex 필요: False

### [P2·stale] house-style-not-adopted
- **어디**: `tools/ionic/build_final_conductivity.py:87 등 — 네 폴더 플로터 18개 중 house_style 사용 2개`
- **근거**: CLAUDE.md: '그림 하우스 스타일 (모든 새 그림) tools/figures/house_style.py import'. house_style.py 는 2026-07-16 커밋('workflow: adopt lab AI-agent practices — CLAUDE.md + house style + prompts')으로 들어왔다. 실측 사용은 tools/ionic/pmf_path_profile.py · fig_lpsocl_arrhenius.py 둘뿐. 16개는 대부분 그 이전(2026-06) 화석이라 정상이지만, build_final_conductivity.py 는 2026-08-20 커밋인데도 `RED,BLUE,INK="#d1352b","#1f6fb4","#222"` 로 자기 팔레트를 새로 정의한다. plot_lobster_4panel.py(2026-07-28)도 도입 이후다.
- **고치는 법**: 도입 이후 파일 둘(build_final_conductivity.py · plot_lobster_4panel.py)만 house_style 로 옮긴다. 6월 화석은 건드리지 말고 INDEX 에 '하우스 스타일 이전' 으로 표시.
- codex 필요: False

### [P2·wrong] uma-version-inconsistency
- **어디**: `tools/doping/run_md_sigma.py:20 vs :242`
- **근거**: 같은 파일 안에서 모델 판이 다르다. docstring:20 `"UMA-s-1p2 sulfide PES has known softening (Wang 2025)"` · 산출 JSON caveats:242 `"UMA-s-1p1 sulfide PES softening (Wang 2025)"`. CLAUDE.md 표준은 UMA-s-1p1(omat) 이고 저장소 어디에도 1p2 실행 기록이 없다.
- **고치는 법**: docstring 을 UMA-s-1p1 로 통일.
- codex 필요: False

### [P2·broken] doc-example-paths-dead
- **어디**: `tools/ionic/beta_null_test.py:24 · tools/ionic/msd_refit_window.py:25 · tools/ionic/run_arrhenius_6pt.sh:206 · tools/ionic/li_percolation.py:42`
- **근거**: docstring 사용 예의 산출 경로가 실물과 안 맞는다. `--csv db/properties/beta_gate_null_vs_hops_origin.csv` → 실물은 `beta_gate_null_vs_hops_c2_origin.csv` 와 `_c4_origin.csv` 둘. `--csv db/properties/msd_window_scan.csv` · `db/properties/msd_window_sensitivity.csv` · `docs/figures/elf_licl/percolation_comp1_modelc.csv` 셋은 아예 없다. 붙여넣기 워크플로에서 그대로 복사되는 줄이라 실측 경로여야 한다.
- **고치는 법**: 네 줄을 실제 산출 파일명으로 고친다(없는 것은 '아직 생성 안 됨' 표시). 다른 tools/ 경로 참조 99개는 전수 확인했고 끊긴 것 0건이라, 이 넷만 손보면 된다.
- codex 필요: False

### [P2·stale] kb-index-3sys-note-drift
- **어디**: `docs/figures/msd_compare/msd_3sys_LPSCl_LPSCl16_b2o3.csv:2`
- **근거**: 플로터가 만든 CSV 헤더가 `"# D = slope/6 (2-50 ps). … b2o3 Ea 0.21+/-0.03; modelc 3-seed reseed pending for symmetric bar"` 라고 적는데, (a) 그 CSV 를 만든 tools/ionic/plot_msd_3sys.py 는 실제로 5–49 ps 로 적합하고, (b) 'modelc 3-seed reseed pending' 은 2026-07-06/07 에 완료돼 정본이 0.197±0.032 다. 산출물 헤더가 자기 생산자와도, 현재 원장과도 어긋난다.
- **고치는 법**: plot_msd_3sys.py 를 고치고(위 P0 항목) 재생성하면 헤더도 같이 정정된다. 재생성 안 할 거면 CSV 2행을 손으로 정정.
- codex 필요: False

### [P1·ia] kb-backlink-missing
- **어디**: `네 폴더 130개 중 kb/ 카드를 참조하는 파일 22개 (doping 7 · cascade 4 · ionic 9 · modelc_v3 2)`
- **근거**: kb 에는 이 도구들을 다루는 카드가 실재한다 — kb/methodology/md_conductivity_protocol.md · cascade_pipeline_anatomy_2026_08_13.md · cascade_rerank_runbook_2026_08_25.md · beta_gate_seed_policy.md · md_axis_status_2026_09_07.md 등. 방향이 한쪽뿐이다: kb → tools 링크는 25개 문서에 있는데, tools → kb 는 22/130. 잘 된 예 tools/doping/axis_corr_csv.py:11 `"(kb/methodology/microstructure_ml_transfer_to_cascade_2026_08_25.md)"` · tools/ionic/msd_diffusive_check.py:22 `"kb/concepts/beta-gate.md §7-5"`. 안 된 예: disorder_ensemble_diffusion.py(모든 MD 캠페인의 드라이버)에 md_conductivity_protocol.md 링크가 없다.
- **고치는 법**: 도구 docstring 끝에 `근거 카드: kb/...` 한 줄 규약을 세우고, 최소한 '물리 규약을 구현하는 도구'(MD 드라이버·MSD 게이트·BVSE·게이트 판정기)부터 붙인다. 이게 나중의 LLM 이 기억을 되찾는 데 가장 크게 먹힌다.
- codex 필요: False
