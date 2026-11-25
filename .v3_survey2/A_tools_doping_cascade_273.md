# v3_survey2 — 조사 A: tools/doping · tools/cascade (273 캐스케이드 생산 경로)

읽음 20/20 — 본문 13 · 부분 본문 4 · 도크+selftest 실행만 3 · 안 봄 0 (단, 이웃 도구 다수 안 봄 — 맨 아래)

전문 읽은 것: `tier_cascade.sh` · `master_batch_273.sh` · `run_compound_batch.sh` · `run_anneal.py` · `run_uma_screening.py` · `run_mlip_postproc.py` · `preflight.py` · `ehull_check.py` · `esw_check.py` · `rank_anneal.py` · `run_cathode_interface.py` · `convex_hull_ehull.py` · `stability_axes.py`
부분 본문: `substitute_compound.py`(640–790 + argparse) · `analyze_screening.py`(1–60 + argparse) · `build_cascade_themes.py`(1–60, 205–250) · `substitute_struct.py`(argparse)
도크 + `--selftest` 실행만: `codoping_ml.py` · `rebuild_pool_inputs.py` · `audit_label_scatter.py`

실행한 것: `run_anneal.py --selftest`(8/8 통과) · 5개 도구 selftest · `convention_check.py`(0 위반) · `substitute_compound.py` 를 canonical CIF 로 **실제 6회 구동**(Nd2O3 x0.02/0.05/0.10, Li2S, Li2O, LiCl, Li3N) → md5 대조.

---

```
[치명] 273 캠페인의 "3 농도" 는 같은 구조다 — x002/x005/x010 이 전부 실측 x=0.25
· 어디: tools/doping/substitute_compound.py:678 · master_batch_273.sh:88-93,312-319,368-369
· 무엇: 조용히 틀린다. 6.4개월짜리 배치의 축 하나가 존재하지 않는다.
  n_units = max(1, int(round(n_fu_actual * x_compound)), n_fu_actual=4 (1x1x1, 4 f.u.)
  → 0.02*4=0.08 → 1 / 0.05*4=0.20 → 1 / 0.10*4=0.40 → 1. 셋 다 n_units=1, actual_x=0.25.
· 근거: 실제로 돌려서 md5 를 맞춰봤다.
    x=0.02  Nd2O3_..cLi24gaS16e_s00.xyz  314edead34eccc12
    x=0.05  (같은 이름)                   314edead34eccc12
    x=0.10  (같은 이름)                   314edead34eccc12
  compound_summary.json 셋 다 actual_x=0.25, n_units=1. 즉 **바이트 동일 파일**이다.
  이름표(substitute_compound.py:779)는 `int(x_compound*1000)` 즉 **요청값**을 박는다 →
  파일명이 x020/x050/x100 이라 실측 0.25 와 12.5x~10x 다르다. 경고 한 줄 없다.
  master_batch_273.sh:368-369 는 그 라벨을 그대로 CSV 로 옮긴다:
    df['concentration_pct'] = float(conc_label)        # 2.0 / 5.0 / 10.0
    df['concentration_fraction'] = float(conc_label)/100
  → unified_dataset_273.csv 의 농도 열 전체가 거짓이다. v4.5.21 주석이 이 열의
  "1/10 off" 단위 버그를 고쳤다고 자랑하는데, 고친 대상 자체가 무의미한 라벨이다.
  ⚠ 이건 **이미 알려진 것**이다 — tools/cascade/audit_label_scatter.py 도크(2026-08-16)가
  "세 라벨이 전부 실측 x=0.25 로 반올림됐다. 그래서 세 점은 농도 3점이 아니다" 라고 적었다.
  그런데 master_batch_273.sh 는 그 뒤(2026-08-20)에도 안 고쳐졌고, 소비자도 안 고쳐졌다(아래).
· 고치는 법: (1) 273 을 **91 로 줄이거나**, 진짜 농도를 원하면 SUPERCELL 을 키운다
  (x=0.025 를 내려면 n_fu >= 40 → 2,2,2 이상). (2) substitute_compound.py 에
  `abs(actual_x - x_compound)/x_compound > 0.1` 이면 **경고 대신 거부**하는 가드.
  (3) 이름표를 요청값이 아니라 actual_x 로 박는다. (4) decisions.json 에 등록 —
  지금 x002/x005/x010 은 decisions.json 에 3회, citation_hazards.json 에 4회 나오는데
  "이 라벨은 농도가 아니다" 라는 항목은 **없다**.
```

```
[치명] 철회된 농도축을 두 도구가 아직 살아 있는 것처럼 쓴다 (dose_robustness · bvs_slope)
· 어디: tools/cascade/build_cascade_themes.py:13,239,302,405-407 · codoping_ml.py:308,470-472
· 무엇: 조용히 틀린다. 웹앱 테마 "도핑 농도 내성" 이 농도가 아니라
  **anneal RNG 시드 잡음 + 자리(site) 차이**를 재고 있다.
· 근거: build_cascade_themes.py:239,302
    "bvs_slope": (round(b10 - b2, 4) ...)      # b10=bvs_x010, b2=bvs_x002
    "dose_robustness": ("bvs_slope", +1, None),
    :407  "metric": "BVS proxy 기울기 (x010-x002) 상승"
  입력 CSV 를 직접 열어보니 x 라벨끼리 **자리가 다르다**:
    db/properties/cascade_v23_litransport.csv
      Ag2O_x002 → Li_24g/S_16e     Ag2O_x005 → Li_48h/S_4a     Ag2O_x010 → Li_48h/S_4a
    47종 중 **30종이 x 라벨 간 site 가 다르다** (동일 17). 중앙 |slope| 0.019.
  구조는 같은데(위 항목) 라벨마다 seed 가 달라 챔피언이 뒤집힌 것이다 —
  run_anneal.py:439 가 `seed = args.seed + crc32(winner_name)` 로 **이름에서** seed 를 뽑는데
  이름에 x020/x050/x100 이 들어 있어 동일 구조가 세 개의 다른 seed 를 받는다.
  codoping_ml.py:470-472 는 그 위에 min(bvs_x002/x005/x010) 을 쌓아 codoping_ml_v2.csv 로 낸다.
· 고치는 법: dose_robustness 테마를 **삭제하거나** 이름을 "재실행 산포(seed+site)" 로 바꾼다.
  bvs_x002/x005/x010 세 열은 하나로 합치고(집계 규칙 선언), codoping_ml 의 transport_min 을
  min-of-3 대신 단일 챔피언 값으로. citation_hazards.json 에 항목 추가.
```

```
[치명] P0-3(anneal seed) 수정이 두 곳에 안 퍼졌다 — Stage 11 이 논문 주장 경로다
· 어디: tools/doping/run_cathode_interface.py:105,110,113 · run_mlip_postproc.py:66,68
· 무엇: 조용히 틀린다. 2026-08-30 에 run_anneal.py 만 고쳤고, **같은 결함이 있는 형제 두 개**는
  안 고쳤다. run_cathode_interface 는 tier_cascade Stage 11 의 생산 경로이고,
  도크가 스스로 "Nd2O3 doping increases NCM-SE adhesion from X to Y J/m^2" 를 논문 주장으로 적어 놨다.
· 근거: run_cathode_interface.py:105-114
    MaxwellBoltzmannDistribution(atoms, temperature_K=ANNEAL_T)      # rng 없음
    dyn  = Langevin(atoms, 1*units.fs, temperature_K=ANNEAL_T, friction=0.01)   # rng 없음
    dyn2 = Langevin(atoms, 1*units.fs, temperature_K=100,      friction=0.05)   # rng 없음
  `seeds = range(42, 42+n_seeds)` 는 **xy 이동만** 바꾼다(:168-172). 즉 Wad_std 는
  "xy 자리 산포" 와 "통제 안 된 MD 난수" 를 섞은 값이고 재현되지 않는다.
  run_mlip_postproc.py:66-69 도 같다 (light_anneal 에 rng 없음). cascade 는 `--no_anneal` 로
  피해 가지만, 도구를 직접 부르는 순간 그대로 맞는다.
  대조: run_anneal.py:124-140 은 rng_v/rng_md 두 스트림을 주고 결과에 기록한다.
· 고치는 법: run_anneal.py:124-126,139 를 그대로 이식하고 `--seed` 를 required 로.
  convention_check.py 의 셸-필수인자 검사가 자동으로 부르는 쪽(tier_cascade Stage 11)을 잡아준다.
```

```
[치명] Li 양이온 화합물 7종은 치환이 no-op — Li2S 는 **무도핑 기준구조가 후보로 들어간다**
· 어디: tools/doping/substitute_compound.py (Type A 경로) · master_batch_273.sh:99-128
· 무엇: 조용히 틀린다. 도핑 안 된 LPSCl 이 "Li2S 도펀트 후보" 이름표를 달고
  screening→winner→anneal→EOS→elastic→ranking 을 다 통과한다. dE/atom ~ 0, dV ~ 0,
  converged=True 라서 게이트를 전부 무사통과하고 상위권에 앉는다.
· 근거: 실제로 돌려서 base 와 좌표 대조했다.
    Li2S_x050_cLi24gaS16e_s00.xyz   base와 동일: True
    Li2S_x050_cLi24gaS4a_s00.xyz    base와 동일: True
    Li2S_x050_cLi48haS16e_s00.xyz   base와 동일: True
    Li2S_x050_cLi48haS4a_s00.xyz    base와 동일: True     (6개 중 4개)
  또 Li→Li 는 무조건 no-op 이라 **cLi24g 와 cLi48h 가 바이트 동일**이다:
    Li2O:  cLi24gaS16e 9191a2977212 == cLi48haS16e 9191a2977212
    LiCl:  cLi24gaCl4d ecb6b6f0415f == cLi48haCl4d ecb6b6f0415f
    Li3N:  cLi24gaS16e 5c94c88cf3ad == cLi48haS16e 5c94c88cf3ad
  해당 화합물: Li2O · Li2S · LiF · LiCl · LiBr · LiI · Li3N = 91 중 7 → 273 중 21 캐스케이드.
  select_winners 는 `--group_by dopant site anion_site_label` 이라 **같은 구조를 두 winner 로**
  뽑아 anneal·EOS·elastic 을 두 번 돌린다.
  ⚠ 지금 정본 랭킹 1위가 `Li2O_x005` 다 (citation_hazards.json hazards[17].fix).
· 고치는 법: substitute_compound 에서 치환 전후 구조 해시가 같으면 **거부**(ValueError).
  cation in host 이면 그 자리 축을 열거하지 않는다. 기존 273 산출물에서 Li계 21개 재검토.
```

```
[치명] Stage 01 이 substitute 실패를 삼켜서, 죽는 자리가 Stage 04 로 밀린다
· 어디: tools/doping/run_compound_batch.sh:22,146,175,196,229
· 무엇: 조용히 틀린다 → 늦게 즉사한다. 이번 --seed 사고와 **같은 모양**의 두 번째 구멍이다.
· 근거: :22 는 `set -e` 만 있고 `set -o pipefail` 이 없다. 그런데 호출이 전부 파이프다:
    python3 "$SCRIPT" ... --out "$out" 2>&1 | tail -3 || echo "    (skipped: chemistry not allowed)"
  파이프 종료코드 = `tail` 의 것 = 0. 그래서 substitute_compound.py 가 트레이스백으로 죽어도
  (1) `|| echo` 는 안 뜨고 (2) set -e 도 안 걸리고 (3) 3줄만 로그에 남는다.
  merge 단계는 남은 compound_summary.json 만 모아 n_structures=0 인
  structures_summary.json 을 쓰고 **rc 0 으로 끝난다** → tier_cascade 가 STAGE_01.DONE 을 찍는다.
  이후 Stage 02 는 0건 처리 후 정상 종료(run_uma_screening.py:302-305, todo=[]),
  Stage 03 도 통과, Stage 04 에서 run_anneal.py:369 `raise SystemExit("No xyz files found")`.
  → 사용자는 Stage 04 실패를 보는데 원인은 Stage 01 이다.
· 고치는 법: run_compound_batch.sh 에 `set -o pipefail` 추가하고 실패를 세어
  마지막에 rc!=0. merge 뒤 `n_structures == 0` 이면 명시적으로 exit 1.
```

```
[주의] Stage 07/08 은 빈 글롭에 폴백이 없다 — Stage 05 만 있다
· 어디: tools/doping/tier_cascade.sh:232,241 (vs :204-219)
· 무엇: 즉사한다. 04_anneal 이 비면
    python3 ... run_mlip_postproc.py --xyz  --out "$OUT/07_eos" --no_anneal ...
  가 되어 argparse 가 `argument --xyz: expected at least one argument` 로 rc=2.
· 근거: 같은 argparse 형태를 재현해서 확인했다 → `SystemExit rc= 2`.
  Stage 05 는 :206 에서 `if [ -z "$xyzs" ]` 폴백을 갖고 있는데 07/08 은 없다.
· 고치는 법: Stage 05 와 같은 빈-글롭 가드를 07/08 에 넣고, 비면 "Stage 04 산출물 없음" 으로
  명시적으로 죽인다 (argparse 오류로 죽지 않게).
```

```
[주의] 실패한 구조가 resume 에서 "done" 으로 굳는다 — 일시적 OOM 하나가 영구 결측이 된다
· 어디: run_anneal.py:442-448,411-418 · run_mlip_postproc.py:417-427,386-392
· 무엇: 조용히 틀린다 (결측이 조용히 확정된다).
· 근거: run_anneal.py:444
    results.append({'name': winner_name(p), 'xyz_input': str(p), 'error': str(e)})
  이 레코드가 anneal_results.json 의 `results` 에 들어간다. 재개 시 :415
    done = {r['name']: r for r in existing.get('results', [])}
  는 **error 레코드도 done 으로 센다** → :418 `todo` 에서 영구 제외.
  run_mlip_postproc.py:419 도 동일.
  대조: run_uma_screening.py:343 은 실패를 `failed` 리스트에 따로 넣어 재개 시 다시 시도한다 —
  같은 저장소 안에서 세 도구의 관례가 갈렸다.
· 고치는 법: run_uma_screening 쪽 관례로 통일 (error 는 별도 키). 또는 resume 시
  `'error' in r` 이면 done 에서 뺀다 (한 줄).
```

```
[주의] Stage 11 이 도구 스스로 무효라고 한 교차-nx 델타를 표에 그대로 찍는다
· 어디: run_cathode_interface.py:146,318-337,364-372 · tier_cascade.sh:320-331
· 무엇: 조용히 틀린다. 논문 표로 갈 delta_Wad 숫자다.
· 근거: :146 `nx = 5 if len(se_atoms) >= 60 else 7`. 실측 원자수:
    lpscl_F43m_24G_canonical.cif 52 → nx=7 | comp2_V0.cif 52 → nx=7
    comp3/comp4/comp5_v2_V0_UMA.xyz 62 → nx=5 | modelC_DFT_EOS_V0.cif 62 → nx=5
  273 캐스케이드의 winner 는 48~52 원자(Nd2O3 48, Li2O 52) → 전부 nx=7.
  즉 **기본 6 기준선 중 4개가 모든 winner 와 다른 nx 그룹**이다.
  :330 이 "comparison valid within group" 이라고 찍어놓고, 바로 아래 :369-371 이
    for b_label, b in baseline_lookup.items():
        delta = w['Wad_mean_J_m2'] - b['Wad_mean_J_m2']
  로 **그룹 무시하고 전 기준선 델타** 를 출력한다.
  같은 함수의 :194-195 는 lbfgs 실패 시드의 Wad 도 `wads.append` 해서 평균에 넣는다
  (`n_lbfgs_ok` 은 기록만 하고 거르지 않는다).
· 고치는 법: 델타 출력·JSON 저장을 `w['ncm_nx'] == b['ncm_nx']` 로 게이트. 다른 그룹은 "n/a".
  Wad_mean 을 lbfgs_ok 시드만으로 계산하고 필터 전/후를 둘 다 남긴다.
```

```
[주의] Stage 08 주석은 "clamped-ion" 인데 코드는 relaxed-ion 이다
· 어디: tier_cascade.sh:238 ↔ run_mlip_postproc.py:213-215
· 무엇: 거짓 라벨. 논문/SI 에 "clamped-ion Cij" 로 쓰면 방법 기술이 틀린다.
· 근거: tier_cascade.sh:238  `# Stage 08 — MLIP elastic (clamped-ion Cij at 0K, then VRH average)`
  run_mlip_postproc.py:213-217 은 변형 셀에서 이온을 **이완**시킨 뒤 응력을 읽는다:
      opt = FIRE(atoms, logfile=None)
      opt.run(fmax=fmax, steps=relax_steps)
      stresses_pos_neg.append(atoms.get_stress(voigt=True))
  clamped-ion 이면 이 두 줄이 없어야 한다. 그리고 elastic_fmax=0.05 는 Cij 용으로 느슨해
  이완이 덜 끝난 채 응력을 읽을 수 있다(수렴 확인 없음).
· 고치는 법: 주석을 "relaxed-ion(static) Cij" 로 정정. 이완 수렴 실패를 기록에 남긴다.
```

```
[주의] preflight 의 --device 가 조용히 무시된다
· 어디: tools/doping/preflight.py:271 ↔ :102-105
· 무엇: 조용히 무시 → `--device cpu` 로 돌리면 UMA 로드에서 즉사.
· 근거: :271 `ok, r = check_baseline_relax(Path(args.base))`  ← device 도 calc 도 안 넘긴다.
  그러면 :102-105 가 자기 것을 만든다:
      if calc is None:
          predictor = pretrained_mlip.get_predict_unit('uma-s-1p1', device='cuda')   # 하드코딩
  같은 함수에서 `--device` 를 받는 check_uma_load(:268)·check_positive_controls(:276)와 갈렸다.
  덤으로 UMA 모델을 한 캐스케이드에서 3번 따로 로드한다 → 273 캐스케이드면 819회.
· 고치는 법: `check_baseline_relax(Path(args.base), device=args.device)` 로 넘기고,
  로드한 calc 하나를 세 검사가 공유한다.
```

```
[주의] ehull_check 는 도크가 약속한 dE_hull 을 계산하지 않는다 · 문턱 인자는 죽어 있다
· 어디: tools/doping/ehull_check.py:5-6,84-86,138-154,160-161
· 무엇: 거짓 문서 + 죽은 인자.
· 근거: 도크 :5-6 "reports dE_hull (eV/atom). dE_hull > 50 meV/atom is the standard flag".
  실제로는 hull 기준에너지와 분해상만 낸다 — 우리 구조 에너지와 비교하는 줄이 없다.
  :148-152 note 가 스스로 "Absolute dE_hull = winner_DFT_E - hull_E...; run DFT on winner.xyz" 라고
  적었다. `--metastable_threshold_meV`(:84)는 :160 에서 config 에 되찍히기만 하고
  **어떤 판정에도 안 쓰인다**.
· 고치는 법: 도크를 "hull 기준에너지 + 분해상만" 으로 정정하거나, --top 구조를
  같은 방법으로 단일점해서 진짜 dE_hull 을 낸다(convex_hull_ehull.py --mode uma 가 이미 그걸 한다 —
  아래 중복 항목 참조). 문턱 인자는 쓰거나 뺀다.
```

```
[주의] esw_check 의 보고량은 winner 에 의존하지 않는다 — 같은 chemsys 면 전부 같은 값
· 어디: tools/doping/esw_check.py:100-106
· 무엇: 조용히 무의미. 상위 10 winner 가 같은 도펀트면 10행이 전부 같은 숫자다.
· 근거:
      energies = [e.energy_per_atom for e in entries]      # chemsys 전체 MP 엔트리
      esw_eV = float(e_hi - e_lo)
  winner 구조는 `elements = sorted(set(symbols))` 를 뽑는 데만 쓰인다(:85).
  게다가 서로 다른 원소의 MP 원시 GGA E/atom 차이라 화학적으로 비교 불가능한 양이다
  (Cl2 ~ -1.8, O2 ~ -4.9 eV/atom 식). 도크가 "coarse" 라고는 하지만
  **무엇의 값인지**가 정의돼 있지 않다 — CLAUDE.md 보고량 규율의 전형적 미정의 케이스.
· 고치는 법: 보고량 카드를 쓰거나 Stage 09f 를 뺀다. 남긴다면 열 이름을
  `chemsys_MP_energy_span`(winner 무관)으로 바꾸고 winner 별 행이 아니라 chemsys 별 행으로 낸다.
```

```
[주의] stability_axes 의 합성가능성 게이트가 89/89 통과 — 진공 게이트를 고치려다 진공 게이트를 만들었다
· 어디: tools/cascade/stability_axes.py:74-90,173 · db/properties/cascade_stability_axes.csv
· 무엇: 조용히 무의미.
· 근거: 도크 :18-20 이 "우리 cascade G1 은 ... 아무도 못 떨어뜨린다(unique_kill 0, vacuous).
  근본 원인이 이것이므로 hull 축을 따로 세운다" 라고 동기를 적는다. 그런데 :85-89
      for e in pd.all_entries:
          if e.composition.reduced_formula != c.reduced_formula: continue
          h = pd.get_e_above_hull(e) * 1000.0
          best = h if best is None else min(best, h)
  같은 조성 엔트리 중 **최소** e_above_hull → 안정 다형이라 값이 작을 수밖에 없다.
  산출 CSV 실측: 89행 전부 `synthesizable_50meV = Y`, hull 최대 46.2 meV, 50 초과 0건.
· 고치는 법: 축(0~46 meV)은 살리되 **게이트를 걷어낸다** (또는 문턱을 실측 분포에서 정하고
  그 근거를 카드에 적는다). "이 컬럼은 아무도 떨어뜨리지 않는다" 를 CSV 헤더 주석에 명시.
```

```
[주의] select_winners 의 사용예가 존재하지 않는 키를 쓴다 — 따라 하면 조용히 다르게 묶인다
· 어디: tools/doping/select_winners.py:15 ↔ :42 ↔ tier_cascade.sh:167
· 무엇: 조용히 틀린다.
· 근거: 도크 :15  `--group_by dopant cation_site anion_site_label`
  묶기 :42  `g[tuple(r.get(k, 'unknown') for k in group_by)].append(r)`  ← 없는 키는 'unknown'
  실제 레코드 키를 실물로 확인했다 (내가 생성한 compound_summary.json):
    ['anion_site_label','anion_site_used','cation_site_used','charge_compensation',
     'composition','concentration','dopant','host','n_atoms','n_fu_actual','name',
     'seed','site','steps','supercell','xyz_file']
  → `cation_site` **없음**. 도크대로 부르면 자리 축이 통째로 'unknown' 으로 접혀
  도펀트당 winner 가 1개만 나온다. tier_cascade.sh:167 은 `site` 를 써서 맞다.
· 고치는 법: 도크 예시를 `site` 로 정정하고, `_group` 에서 group_by 키가 레코드에 하나도
  없으면 에러로 죽인다 (조용한 'unknown' 금지).
```

```
[주의] EOS 앙상블이 "최량 r^2 하나 고르기" 다 — 집계 규칙이 편향이다
· 어디: run_mlip_postproc.py:147-186 (tier_cascade.sh:235 `--n_eos_seeds 5`)
· 무엇: 조용히 틀린다 (B0 가 체계적으로 좋아 보이는 쪽으로 뽑힌다).
· 근거: :171  `best = dict(max(pool, key=lambda r: r.get('r2', -1.0)))`
  이 best 의 `B0_GPa` 가 최상위 키로 나가고 combine_rankings 가 그걸 읽는다.
  평균·표준편차는 `ensemble` 하위에만 남는다(:173-185). 5개 중 적합도가 제일 좋은 하나를
  고르는 것은 앙상블 집계가 아니라 선택 편향이다 — CLAUDE.md "admissible state 가 여럿인데
  선택·집계 규칙" 조항에 정면으로 걸린다.
· 고치는 법: 보고량을 `B0_GPa_median` (또는 physical 적합만의 평균 +- std)으로 바꾸고,
  max-r2 값은 `B0_GPa_bestfit` 로 이름을 바꿔 참고로만 남긴다. 결정을 decisions.json 에 등록.
```

```
[주의] 273 목록에 Li3N 이 있다 — UMA 금지 규율과 충돌한다
· 어디: master_batch_273.sh:125 · CLAUDE.md · kb/elements/Li.json:51 · kb/elements/N.json:63
· 무엇: 규율 충돌. 3 캐스케이드(Li3N_x002/x005/x010)가 screening·anneal·EOS·elastic·MD sigma 를
  전부 UMA 로 돈다.
· 근거: kb/elements/N.json:63 "UMA-Li3N-금지 규칙(CLAUDE.md)은 **향후 Li3N 방법 선택 전반에
  적용**." kb/elements/Li.json:51 "Li3N에는 UMA MLIP 금지(2026-06 결정론적 편향 판정)".
  ⚠ 다만 여기서 Li3N 은 순수 상이 아니라 LPSCl 에 넣는 **전구체**고, 위 [치명 4] 대로
  실제로 바뀌는 것은 S→N 하나뿐이다(Li→Li 는 no-op). 금지 판정의 사정거리에 이게 들어가는지는
  **내가 판정할 문제가 아니다** — 1저자 결정이 필요하다.
· 고치는 법: decisions.json 에 "Li3N-as-dopant x UMA" 를 proposed 로 올려 사정거리를 확정.
  금지면 목록에서 빼고, 허용이면 사유를 카드에 남긴다.
```

```
[주의] convex_hull_ehull --mode uma 는 우리 구조만 최소에 있고 경쟁상은 아니다 (비대칭)
· 어디: tools/doping/convex_hull_ehull.py:87-102,124-129
· 무엇: 조용히 틀린다 (E_above_hull 이 체계적으로 낮게 나온다).
· 근거: `uma_E(struct)` 는 **단일점**이다 — 이완이 없다(:87-89).
  경쟁상은 MP 의 **DFT-이완 기하**를 UMA 로 단일점하니 UMA 최소보다 위에 있고,
  우리 구조는 이미 UMA 로 이완된 CIF 를 넣으니 UMA 최소에 있다.
  → hull 이 위로 밀리고 우리 값은 그대로 → E_above_hull 이 낮게 나온다.
  도구는 "건너뛴 경쟁상" 편향은 :108-114 에서 크게 경고하는데(같은 방향의 편향이다)
  이 비대칭은 어디에도 안 적혀 있다. kb/methodology/zn_cu_hull_estimand_2026_09_03.md:89 은
  "끝점과 대상이 같은 방법인가? **예 — 전부 UMA-omat 단일점**" 이라고 통과 판정을 했는데,
  같은 *방법*이긴 해도 같은 *상태*(이완/비이완)가 아니다.
· 고치는 법: 경쟁상도 UMA 로 이완하거나(비싸다), 못 하면 결과 JSON 에
  `"bias": "경쟁상은 DFT 기하 단일점 — E_above_hull 이 하한이다"` 를 박고 카드 5 를 재판정.
```

```
[참고] 같은 dV 를 세 군데서 다른 문턱으로 거른다
· 어디: run_uma_screening.py:126 (dv_max=0.30) · tier_cascade.sh:168 (--max_dv 0.25)
        · analyze_screening.py:373 (--max_dv 기본 0.10)
· 무엇: 어느 게 정본인지 모른다. cascade 경로는 0.30 → 0.25 를 거치고,
  analyze_screening 으로 손 분석하면 0.10 이라 결과가 달라진다.
· 고치는 법: 하나로 정하고 convention_check.py EXEMPT/규약에 등록.
```

```
[참고] axis_corr_csv 가 이미 고쳐진 결함을 현재형으로 출력한다
· 어디: tools/doping/axis_corr_csv.py:904, 1056
· 무엇: 낡음. 사용자가 읽는 화면 문구다.
· 근거: :1056  `print("        비결정적이라(run_anneal.py 가 RNG·초기속도 seed 를 안 받는다)")`
  run_anneal.py 는 2026-08-30(34a400e93)에 `--seed` required + 두 스트림 주입 + 결과 기록으로
  고쳐졌다 (selftest 8/8 통과 확인).
· 고치는 법: "2026-08-30 이전 CSV 는 seed 미기록이라 …" 로 시제를 바꾼다.
  db/properties/cascade_axis_retest_2026_08_30.json 은 이력이니 **그대로 둔다**.
```

```
[참고] build_cascade_themes 는 argparse 가 없다 — 아무 argv 나 받고 db/properties 에 쓴다
· 어디: tools/cascade/build_cascade_themes.py:207,522,533 (argparse import 없음)
· 무엇: 실행하면 무조건 cascade_v23_themes.json + cascade_air_axis_lit_vs_tier.csv 를 쓴다.
· 근거: 내가 `--selftest` 를 줘 봤는데 오류 없이 **전체 경로를 돌고 CSV 를 썼다**
  (내용은 커밋본과 동일해서 git status 는 깨끗하다 — 확인함).
  CLAUDE.md 코드 규율의 `--selftest` 요건도 없다.
· 고치는 법: argparse + `--dry-run` + `--selftest`. 미지 인자는 거부.
```

```
[참고] master_batch 의 "30분 규칙" 이 방금 실패한 캐스케이드를 running 으로 가린다
· 어디: master_batch_273.sh:167-171, 305-307
· 무엇: 실패가 조용히 skip 으로 보인다.
· 근거: :306-307 이 실행 전에 `mkdir -p "$OUT"; echo $$ > "$OUT/.master_lock"` 을 쓴다.
  캐스케이드가 30분 안에 죽으면 그 파일들이 최근 수정 상태로 남고, 곧바로 재기동하면
  :168 `find "$outdir" -type f -mmin -30` 이 걸려 "running" → SKIP 된다.
  이번 --seed 사고가 딱 그 모양이었다(Stage 01–03 이 30분 돌고 04 에서 죽음).
  .master_lock 은 캐스케이드 종료 후 지워지지도 않는다.
· 고치는 법: 캐스케이드 종료 시 .master_lock 삭제. Layer 3 을 lock/PID 뒤로 내리고,
  "직전 rc!=0" 기록을 남겨 running 판정에서 제외.
```

```
[참고] preflight 의 POSITIVE_CONTROL_COMPOUNDS 는 죽은 상수인데 아직 파일에 있다
· 어디: tools/doping/preflight.py:36-41 (참조 0회) ↔ :171-172 주석
· 근거: :171 "A-5 fix (2026-05-16): replaced the dead POSITIVE_CONTROL_COMPOUNDS constant with
  this integration test." — 대체했다면서 상수는 안 지웠다. `Cl_rich` 는 :197-201 케이스에도 없다.
· 고치는 법: 지운다.
```

---

## 못 본 것 — 무엇을 안 읽었고 왜

- **`codoping_ml.py` 본문 1236행 중 ~40행만** 봤다(도크 + `grep` 로 입력 소스 + selftest 22/22 통과). ML 모형 자체(특징 구성·CV·외삽 방어)는 **안 봤다**. 위에 적은 건 입력 계보뿐이다.
- **`rebuild_pool_inputs.py`(545) · `audit_label_scatter.py`(377)** 는 도크와 selftest 결과만 봤다. 본문 안 봤다. audit_label_scatter 는 도크가 이미 [치명 1]을 적고 있어 신뢰했지만 계산이 그 말대로인지는 **확인 안 했다**.
- **`substitute_compound.py` 878행 중 ~200행**(640–790 + argparse). 치환 알고리즘 본체(`substitute_compound_at_sites`·공공 보상·전하 계산)는 **안 봤다** — no-op 판정은 코드가 아니라 **실행 결과 md5** 로 했다.
- **`analyze_screening.py` 549행 중 ~90행** (도크 + argparse + selftest). 점수식·Pareto 본체 안 봄.
- **`substitute_struct.py` 610행** 은 argparse + selftest 만. 본문 안 봄.
- **Stage 별 도구 중 배정 밖이라 안 연 것**: `select_winners.py`(1–26 만), `bvse_proxy.py`, `combine_rankings.py`, `collect_dataset.py`(grep 만), `train_predictor.py`, `generate_dft_inputs.py`, `run_md_sigma.py`, `stage_report.py`, `site_preference.py`(import 만). **Stage 05·09a–09d·10 은 계약을 실물 대조하지 못했다.**
- `tools/cascade/build_screening_funnel.py`(1435) · `build_cascade_audit_manifest.py`(851) · `cathode_reactivity.py` · `analyze_cathode_reactivity.py` · `uma_relax_check.py` · `cascade_ids.py` — 배정 밖, 안 봄.
- 형제 러너 `run_as2s3_recover.sh` · `run_dualx_highx.sh` · `master_batch_105.sh` — grep 으로 tier_cascade 를 부른다는 것만 확인, 본문 안 봄. (셋 다 tier_cascade 를 부르므로 `--seed` 는 기본값으로 자동 승계된다는 것까지만 확인.)
- **GPU 계산은 하나도 안 던졌다** (지시대로). 그래서 UMA 가 붙는 경로 — Stage 02·04·07·08·10·11 — 는 **실행으로 검증 못 했고 코드 독해뿐**이다. `pymatgen`·`fairchem`·`pandas`·`sklearn` 이 이 환경에 없어서 ehull/esw/stability_axes/codoping_ml 의 **수치 경로는 한 줄도 실행 못 했다.**
- `pymatgen.PhaseDiagram.get_hull_energy` 의 정규화 규약(per-atom 인지)을 **로컬에서 확인 못 했다**. `ehull_check.py`(나누지 않음)와 `convex_hull_ehull.py:179`(num_atoms 로 나눔)가 서로 다른 표현을 쓰는데, 문서 기억대로면 둘 다 맞다(전자는 per-atom 식을 직접 씀, 후자는 total 을 나눔). **확정 못 했으니 발견으로 올리지 않았다.** pymatgen 있는 곳에서 30초면 확인된다.

## 이 영역이 활성인가 — 어떻게 판단했나

**활성이다. 그것도 지금 이 순간 활성이다.** "끝난 캠페인" 분류는 여기 적용 안 된다.

- 커밋일: `tier_cascade.sh` **2026-09-09**(오늘, 382cb4e17 — --seed 수정) · `codoping_ml.py` 2026-09-01 · `analyze_screening.py`·`substitute_struct.py`·`convex_hull_ehull.py` 2026-08-25 · `run_anneal.py` 2026-08-30 · 나머지 대부분 2026-08-20(e748eaf7b 한 커밋).
- 호출자를 실물로 확인: `grep -rn "run_anneal.py"` → 코드에서 부르는 곳은 `tier_cascade.sh:194` **하나**뿐(나머지는 kb 문서·survey·manifest). `tier_cascade.sh` 를 부르는 곳은 `master_batch_273.sh:315` · `run_as2s3_recover.sh:108` · `run_dualx_highx.sh:15` **셋**. 즉 이 계열은 죽은 코드가 아니라 **단일 생산 경로**다.
- 산출물이 살아 있다: `db/properties/cascade_v23_litransport.csv`(47종 x 3 라벨) · `cascade_stability_axes.csv`(89행, 2026-09-03 수정) · `cascade_v23_themes.json` · `codoping_ml_v2.csv` 가 전부 이 파이프라인 산출이고, `citation_hazards.json` 이 그 위의 순위(`Li2O_x005` 1위)를 인용 위험으로 관리 중이다 → **웹앱·원고까지 이어져 있다.**
- 2026-09-09 에 273 을 다시 던지려던 참이었다. 위 [치명 1]·[치명 4]는 **지금 다시 던지면 6.4개월을 태우고 나서** 드러난다.
