# 코드 전수 감사 (fable, 2026-08-20) — 브랜치 `claude/stoic-knuth-NObVQ`

계기: 사용자 지시 "브랜치에 있는 코드, md들 다 보고 올까".  kgy vox 0.115 8팔 대기 중
(~5–6 h) 에 브랜치 전체를 읽어, **2026-08-19~20 에 확인된 5부류 결함의 신규 사례**를 찾게
했다.  기존 12건(§D 목록)은 범위 밖으로 명시.  아래는 에이전트 보고 **원문 박제** —
`★★★`/`★★` 항목은 내가 재현·정적 증명으로 독립 확인했고, 그 확인 기록은 §확인 절에 있다.

부류: (α) 죽은 데이터흐름 · (β) 조용한 경계 도메인 불일치 · (γ) 근거 없는 상태 단정 ·
(δ) 사본 표류 · (ε) 부기가 계산을 죽임.

---

## (a) 발견 — 치명/중요

**#1 ★★★ 치명 (α) — `--fibre` 없는 모든 payload 런에서 STEP3 전체가 조용히 죽는다 (2026-08-12 이후 활성)**
- `scripts/mpm_webapp_payload.py:1008-1009` (동일 표현식 `:1033-1034`): rasterize 호출의
  `add_kind=(_kind_all[_m] if _kind_all is not None and len(_kind_all)==len(_fid_all) else None)`
  에서 `_kind_all` 은 **`:889-894` 의 `if getattr(a,'fibre','') and phase is not None:` 블록
  안에서만 대입**된다.  `--fibre` 를 안 주면(= `mpm_input_from_case.py:700` 이 `--add-recipe`
  없는 킷에는 `--phase/--fibre` 를 아예 안 넣음) `UnboundLocalError` → `:1765` blanket except
  가 삼켜 `⚠ STEP3 skipped` 한 줄 + manifest `_step3: failed` 로 적고 **payload 는 exit 0 으로
  정상 완주**.
- **오염되는 수치**: 비첨가제(plain) 킷 런의 STEP3 산출 전부 — σ_e·σ_ion·k_eff·pore-τ·PNM·
  collector σ_apparent·반응전류·필드·`step4_grid.npz`(`:1734` 도 같은 try 안) 가 **값이 틀리는
  게 아니라 통째로 소실**되고, run_mpm.sh 는 DONE 마커까지 찍는다.  도입 커밋 `60bd849e`
  (2026-08-12 07:14) — SR-01 8팔 캠페인은 전부 `--fibre` 를 넘겨서 무사했고, 그래서 8일간
  아무도 못 봤다.  자체 게이트 `check_undefined_names.py`(pyflakes) 는 조건부 바인딩을
  원리적으로 못 봐 **통과함을 실측 확인**.
- 같은 표현식에 잠복 쌍둥이 2건: ① `--fibre` 길이 불일치로 `:909` 가 `_fid_all=None` 으로
  내린 뒤(점 모드) `len(_fid_all)` → TypeError, ② kind 배열 검증 도메인이 `len(se)` 가 아니라
  `len(_fid_all)` (잘못된 비교 대상).
- **재현**: `python3 scripts/mpm_webapp_payload.py --scaffold <5줄 CSV> --se-proxy --n-vox 96
  --step3-vox 1.0 --out /tmp/p.json` → 로그에 `UnboundLocalError: _kind_all`,
  manifest status=failed, EXIT=0.

**#2 ★★ 중요 (γ) — prereg 판정기의 고정-인자 게이트에 "기록 없음" 구멍 4필드 (실측으로 h0 오판 재현)**
- `scripts/sdcp_gain_verdict.py`: `sigma_vgcf_S_cm`·`sigma_sdcp_S_cm`·`sdcp_sphere_d_um`·
  `backend` 는 **고정-인자 루프(`:174`, None 은 skip)에는 있지만 missing-게이트(`:191`, 4필드
  한정)에도 세대-혼합 게이트(`:163`, `_GEN_FIELDS` 한정)에도 없다**.  한쪽 침대 8팔 전부가 그
  필드를 기록 안 한(08-16~08-18 세대) payload 여도 판정이 그대로 난다.
- **실측**: DBE 8팔의 `sigma_vgcf_S_cm=None`(+3필드) 픽스처로 `verdict()` 를 호출하니 HOLD 가
  아니라 **`h0`** 을 반환.  러너 자신이 "옛 팔을 이어 쓰려면 `OUTDIR=` 로 옛 경로를 명시" 라고
  안내하므로(`sdcp_gain_vox015_8arm.sh:83-89`) 이 재개 경로는 실제로 권장되는 시나리오다.
  H5("기록 없으면 게이트 no-op")를 두 번 고친 바로 그 부류의 잔존.

**#3 ★★ 중요 (β/δ) — 상별 부피 원장 러너의 SKIP 캐시가 설정을 키에 안 넣는다 (H4 결함의 미전파 사본)**
- `scripts/sdcp_phase_ledger.sh:43-46`: `TAG={kit}_v{vox}_{pt|sph}` + `[ -s "$OUT" ] && SKIP` —
  **`BRIDGE_UM`·`SDCP_D` 가 태그·OUTDIR 어디에도 없다**.  σ 러너에서 2026-08-18 에 고친
  H4(설정을 디렉터리 이름에) 가 이 러너에는 전파되지 않았고, `sdcp_phase_ledger_report.py`
  (250줄) 는 ledger 안의 `bridge_um`/`sdcp_sphere_d_um` 을 아예 안 읽어 사후 게이트도 없다.
- **오염되는 수치**: CL-25/CL-43 의 SDCP 표현부피비(4.311/1.866/1.090/0.238)·VGCF-몫
  (39.8→7.2 %) 트랙 — 다른 브리지/직경으로 재실행하면 옛 원장이 새 라벨로 조용히 재사용된다
  (현재까지는 기본값만 써서 실해는 없음, 덫은 장전 상태).
- **재현**: `BRIDGE_UM=0.30 bash scripts/sdcp_phase_ledger.sh` → 기존
  `phase_ledger/ledger_*_v015_*.json`(0.48 산물)이 전부 `SKIP` 으로 재사용됨.

**#4 ★ 중요 (γ) — "사본 일치는 selftest 가 대조한다" 가 동어반복 (사본은 한 번도 검사된 적 없음)**
- `scripts/ml_design_structure.py:1122-1134` 의 패리티 검사는 `predictor_engine.derive_features(x)`
  와 모듈 `derive_features(x)` 를 비교하는데, 모듈 함수는 `:377-385` 에서 **predictor_engine 이
  import 되면 그것으로 위임**한다.  즉 검사가 도는 유일한 환경(import 성공)에서는 원본 vs 원본
  비교 = 항등식이고, `:386-399` 의 오프라인 사본(numpy-less/webapp-less 환경의 실제 실행 경로)은
  **한 번도 검증되지 않는다**.  현재 수치는 일치함을 수동 대조로 확인(math.log≡np.log)했으나,
  원본이 바뀌면(v2.1 특징 등) 능동학습 후보 생성이 조용히 옛 특징으로 돈다.

## 하위 (간결히)
- (α) `network_conductivity.py:160-162` `build_network(results_dir=)` 죽은 인자 — docstring 은
  "ionic 모드는 percolation_sets.json 으로 경계" 라고 약속하지만 본문 어디서도 안 읽음
  (호출부 `:977`·`:1135` 는 실값을 넘김).  경계는 항상 z-규칙 — 계약 표류이지 수치 오염은 아님.
- (α) `additives.py:383` `_fib_sphere_samples(seed=0)` seed 무시 → `sheath_ion_tradeoff(seed=)`
  (`:446` 전달) 를 seed 스윕하면 **완전 동일 표본** (현재 스윕하는 호출자 없음).
- (γ) `mpm_webapp_payload.py:1108` — CG **미수렴이어도** manifest component 는 `complete`
  (unconverged 플래그는 별도 기록되고 판정기는 cg_info 를 봐서 prereg 는 안전; manifest status
  만 읽는 소비자는 오독).
- (δ) `mpm_input_from_case.py` 폴백의 `_NONADD`·`_DENS`·`_parse` 사본은 규칙 I `_COPY_PARITY`
  미등록 (등록은 `_KNOWN` 1쌍뿐; 현재는 일치함을 대조 확인).
- (β) `mpm3d_compaction.py:2431` `except Exception: pass` — `--fibre-stiff` 의 VGCF strut
  binary_closing 이 scipy 부재 시 조용히 생략 (강체 마스크가 달라짐; scipy 는 사실상 필수
  의존이라 저위험).
- 미확인으로 남긴 것: `--step3-amg` 가 GPU 경로에서 no-op 인 것은 help/주석에 "CPU 전처리" 로
  명시돼 있어 결함으로 세지 않음.  `dem_scripts/*.liggghts` 는 seed 파라미터화가 실제 배선됨을
  확인 (`insert/pack seed ${seed}`).

## (c) 부류별 집계 (신규만)
α 3건 (#1 치명 · results_dir · fib seed) · β 2건 (#3 · scipy-closing) · γ 3건 (#2 · #4 ·
unconverged=complete) · δ 1건 (미등록 사본 3종) · ε 0건 (기존 수정들이 유효함을 확인 —
`_phi_prof` None-안전, manifest `_mflt` 방호, res 가 `periodic_xy` 를 자가 운반).

## (d) 구조 제안 — 규칙 J: 생산 엔트리포인트 **최소-픽스처 스모크 매트릭스**
규칙 H(`--help` 생존)의 실행 확장.  등록부에 `(스크립트, argv 변형들)` 을 두고 — payload 는
`{±--fibre, ±--phase, ±--temp-c}` 조합 — 초소형 픽스처로 실제 실행해 **exit 0 이 아니라
`manifest.status=='complete'`(선언한 component 집합)을 단언**한다.  근거: #1 은 pyflakes 류가
원리적으로 못 보는 조건부 바인딩이고, 이 부류의 기존 3사고(`_kind_all`·`float(a.temp_c)`·
`60bd849e` 선분 스탬프 무음 강등)가 전부 "옵션 입력이 빠진/붙은 기본 경로" 에서 났다 —
H 는 파서 생존만, J 는 기본 경로 생존을 증명한다.  A~I 와 비겹침 (I 는 리터럴 목록 패리티,
H 는 argparse 문자열, F 는 import 그림자).

---

## 내 독립 확인 (2026-08-20, 이 브랜치에서 실행)

**#1 — 확인 (치명, 재현 성공).**
1. 정적 증명 (AST): `main()` 안 `_kind_all` 의 **STORE 는 894·901 두 줄뿐이고 둘 다
   `if getattr(a,'fibre',…)`(889, body 890–920) 안**, LOAD 는 1008/1009/1033/1034 = 블록 밖.
   ⇒ `--fibre` 없으면 컴파일상 지역명이 미바인딩.
2. 실행 재현 (5구 scaffold + `--se-proxy --n-vox 64 --step3-vox 1.0 --no-ion --no-pore`):
   `EXIT=0` · `⚠ STEP3 skipped (UnboundLocalError: cannot access local variable '_kind_all'…)`.
3. 파급 확인: `mpm_input_from_case.py:700` 이 정확히
   `pay_phase = ' --phase … --fibre …' if a.add_recipe else ''` ⇒ **첨가제 없는 모든 킷**이
   해당.  `phase` 로드 실패(`:678-681` → `phase=None`) 시 `--fibre` 를 줘도 같은 경로.
4. 수정: `_kind_all = None` 을 `_fid_all` 옆(블록 **밖**)으로 올리고, `add_kind` 가드의 도메인을
   `len(_fid_all)` → **`len(se)`** 로 정정 (마스크 `_m` 의 도메인이 `se` 이므로 원래 이쪽이
   맞고, `_fid_all=None` 일 때의 TypeError 도 같이 사라진다).  재실행 시 STEP3 가 솔버까지
   진행함을 확인.

**#2·#3·#4** — 아래 "적용" 절 참조 (각각 재현 테스트 먼저 → 수정).
