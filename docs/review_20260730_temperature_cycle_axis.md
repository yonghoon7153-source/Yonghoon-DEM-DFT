# 온도·사이클열화 축 적대리뷰 (2026-07-30, HEAD baf34936)

> 검증 대상 커밋 4개 — `028404ef`(A: i0(T) kim2025 앵커 배선 + C: 온도-열화 미배선 사유) ·
> `5cbae845`(B: 사이클 열화 N축 합성) · `3918f31b`(자체수정: i0(T) bimodal 상쇄) ·
> `baf34936`(적대리뷰 반영 H1~H10).
> 4렌즈(fixes / physics / silent / 반박) 교차검증 후 **CONFIRMED 로 살아남은 것만** 종합.
> 모든 줄번호·수치는 `baf34936` 트리에서 직접 실행해 재현한 것이다.
>
> ⚠ 검증 위생 교훈 — physics 렌즈는 컨테이너 리셋으로 **롤백된 트리(`607933c9`)** 를 읽고
> "대상 커밋 4개가 전부 존재하지 않는다"고 선언했다.  실제로는 `git cat-file -t` 로 4개 모두
> commit 이다.  **"코드에 X 가 없다" 는 관찰을 믿기 전에 `git rev-parse HEAD` 를 먼저 확인하라.**
> (`3918f31b` 커밋 메시지가 이미 이 사고를 예고해 두었다.)

---

## 0. 한 줄 요약

**H1(RT 전인자)은 물리적으로 옳고 비순환 테스트도 진짜로 버그판을 잡는다.  그러나 baf34936 의
나머지 수정은 대부분 *산문*(docstring·`docs/`)만 고치고 *실제로 방출되는 문자열*(argparse help ·
콘솔 배너 · npz provenance · 킷 `mpm_input.json`)은 남겨 두었고, H5 가 신설한 `--film-frac` 은
남의 셀 R_ct0 를 틀린 면적기준으로 내보내는 새 HIGH 를 만들었다 — 전부 크래시 없이,
selftest·`test_cli_help`(121)·webapp 2종 스위트가 GREEN 인 채로 통과한다.**

정량 요약: CONFIRMED 33건 (HIGH 10 / MED 15 / LOW 8), REFUTED·기각 10건.
**프로덕션(킷·webapp) 경로에는 i0(T) 가 아예 배선되지 않았고**, 그 경로가 배포하는 zip 은
"i0 앵커가 없다"고 세 번 진술한다 — 앵커는 같은 리포 안에 있다.

---

## 1. baf34936 수정 검증 — 각 H1~H10 이 실제로 고쳐졌는가

| # | 주장 | 판정 | 증거 |
|---|---|---|---|
| **H1** | `R_ct = RT/(F·i0·A)` → `i0 ∝ T/R_ct` → 전인자 `(T/T_ref)` 추가.  60 °C 5.5982 → 6.2545 | ✅ **완전** (단 [D1] argparse help 미수정) | `_ct`(`step4_dyn.py:864`) `g = i0A·f·(αa·e⁺+αc·e⁻)` → η=0 에서 `g = i0A·f·(αa+αc)` → `R_ct = RT/(F·i0·A·(αa+αc))`.  기본 α=0.5/0.5 ⇒ 합=1 ⇒ 정확.  **α 비대칭에서도 T-스케일링은 성립**(α 는 T-무관 → 비에서 상쇄; 실측 α=(0.7,0.5) 에서 `1/g=0.010705` vs `RT/(F i0 A)=0.012846`, 비 = 정확히 1.2 = α합).  독립 2경로 일치: `(T/T_ref)×5.5982 = 6.2554` ↔ `exp(Eₐ_i0/k_B·Δ(1/T))`, Eₐ_i0 = 0.4212 + k_B·T̄ = **0.4486 eV** → 6.2610.  실측 `i0_temperature_factor(60.0) = 6.254470329169113` |
| | 순수 Arrhenius `rct_temperature_factor` 를 1/i0 에서 분리 | ✅ 분리됨 (단 [L4] 프로덕션 소비자 0건 = 죽은 export) | `cam_kinetics.py:129` |
| | "비순환" 테스트 신설 (Kinetics 로 `1/(dI/dη)|₀` 계산 → 앵커 3점 대조) | ✅ **진짜 비순환** — 전인자를 빼면 60 °C 10.01% 오차로 3% tol 초과 CAUGHT | `cam_kinetics.py:249-277`.  실측 현행: 30 °C +0.00% / 45 °C **−2.90%** / 60 °C +0.11%.  ⚠ 여유 0.10 pp → [M11] |
| **H2** | `cycle_degradation_law` 의 "사용자 랩 노화온도" 거짓 정정 (Yun 2023 = 30 °C) + 하한 라벨 | ✅ 사실확인 부분 완전 | `litdb/papers/yun2023_*.md:106` = `갈바노 사이클 2.5–4.3 V vs Li/Li⁺, **30 °C** … cycling 0.33C` 직접 확인.  `ANCHOR_T_CYCLE_C = 30.0` (`:86`), 5중 라벨(docstring `:59-69` · `:86` · 행별 `anchor_T_cycle_C` `:187` · 배너 `:332-333` · selftest `:251-252`) |
| | | ⚠ 잔여 → [M19] | §13-2 가 "노화온도 확정 측정앵커 0건" 이라 단정하는데 그 근거를 H2 자신이 무너뜨린다 |
| **H3** | `--i0-temp-scale` 이 `KINETICS_UNSCALED` 를 무조건 strip 하던 것 제거 | ✅ **정상 경로는 안 막힌다** | 계약 있는 60 °C 그리드 + `--temp-k 333.15 --i0-temp-scale` → `errors=[]`, `state='PARTIAL_sigma_ion+i0@60C'`, `released_guards=[]`.  레거시 그리드(계약 없음)는 차단 ✅ |
| | | ⚠ 그러나 `released_guards` 기록은 **여전히 부정확** → [H9] | 계약 없는 그리드에서 σ-불일치가 `KINETICS_UNSCALED` 로 코딩되고, 해제하면 "kinetics unscaled 를 해제했다"고 영구 기록되는데 정작 동역학은 스케일돼 있다 |
| **H4** | 끝점이 측정 총량임을 라벨 + `--subtract-mech` (2.8747→2.7379) | 🔶 **부분** — 라벨·곱셈분해는 옳고, 상수 1.05 는 모듈 자신의 규약 위반 → [H8] | 실측 `compose([100])[0]['g_chem'] = 2.874743927421715` → `subtract_mech=True` → `2.737851359449252`.  기본 OFF + `g_chem_is_measured_total: True` 낙인 ✅ |
| **H5** | `--film-frac` 신설 (√N 은 옴성 필름 정당화인데 로그성 i0 채널에만 냈던 것) | ❌ **진단은 정확, 구현이 무효** → [H1] | 옴성 `η=i·δ/(σA)`, δ∝√t ⇒ η∝i·√N (율 선형) vs 전하이동 `η=(2RT/F)asinh(i/2i0)` (로그) — 분할 필요성 진단은 옳다.  그러나 방출값이 **Yun 셀의 341.7 Ω·cm² 를 footprint 기준으로 만들어 interfacial 기준 플래그에 넣는다** |
| | 기본 0 은 하한 낙인 | ✅ 정확 (반박에서 방어됨) | 선형 극한에서 `ΔR = R_ct0(g−1)` 이 두 채널 동일 ⇒ 저율 일치, 고율에서만 갈림 ⇒ `"고율 penalty 의 하한"` 라벨이 정확 |
| **H6** | `--i0-temp-ea-ev` 에 `ea>0` 강제 + override 시 밴드 재계산 + `USER_OVERRIDE` provenance | ✅ **완전** | `ea ∈ {0, −0.4212, −1}` 전부 거부 확인 (단 `ap.error` 가 아닌 raw `ValueError` traceback — 미관) |
| **H7** | `cam_kinetics` docstring 의 "코팅계 T-스윕 없음" 거짓 정정 + LNO 비-Arrhenius 를 selftest 로 고정 | 🔶 **산문만** → [H3] | docstring(`:43-50`)·`docs §12-4`(`:757-766`) 는 고쳐졌으나 **기계판독 dict `provenance()['transfer_assumption']`(`:184-186`) 은 원문 그대로**.  실측: `python3 -c "import cam_kinetics as c; print(c.provenance(60.0)['transfer_assumption'])"` → `'…LNO 코팅계 T-스윕은 논문에 없음.'` |
| | LNO 3점(30/45/60 = 22.4/8.7/7.6) 이 CSV 에 stated 로 실재 | ✅ 사실 | `docs/data/kim2025_tlm_kinetics_anchors.csv` — **세 행 모두 62 wt%** (동일 계열).  ⚠ 상수 배열은 CSV 크로스체크 없음 → [M23] |
| **H9** | `--merge-into-i0` 의 행별 채널 라벨 | ✅ 행별 라벨 자체는 정확 | `i0_mult_channel` + `merge_requested_but_chem_only` 행별 기록 |
| | | ⚠ 그러나 `--film-frac` 과 조합하면 총량 비보존 → [H5] | |
| **H10** | trust 문자열 **및 콘솔 배너** 를 i0 스케일 여부에 따라 분기 | ❌ **배너 미수정 (커밋 메시지가 거짓)** → [H2] | `_trust_str`(`:2877-2882`) 만 조건부.  배너 `step4_dyn.py:2857-2863` 는 무조건 f-string |

**기본값 불변 검증 ✅** — `cycle_degradation_law` 기본 4행 `i0_cycle_mult` 가 `5cbae845` 판과
비트 동일 (`1.0` / `0.6278070493006037` / `0.42998839807483324` / `0.34785707014150463`).
`step4_dyn` 은 `_i0_tf=1.0` 정확곱 + `_tmeta=None` (trivial) → 새 플래그 미지정 시 bitwise 동일.

---

## 2. 생존 결함 (심각도 순)

### 🔴 HIGH

#### [H1] `--film-frac` 이 **남의 셀 R_ct0** 를 **틀린 면적기준** 으로 내보낸다 — 이번 감사 최중대
- **[scripts/cycle_degradation_law.py:183-184]** `'asr_film_cycle_ohm_cm2': float(r_ct0_ohm_cm2)*(gc-1.0)*float(film_frac)`,
  기본 `r_ct0_ohm_cm2 = YUN_RCT_FROM = 341.7` (`:150`, `:82`).  **CLI 노출 없음** — `main()` 은
  6개 위치인자만 전달하므로 **어느 베드를 돌리든 Yun 의 bare SC-NMC 풀셀 값**이 쓰인다.
- **면적규약 충돌** — step4 의 같은 argparse 안에 Ω·cm² 가 **두 개, 서로 다른 분모**:
  - footprint: `step4_dyn.py:1467` `R_int_abs = r_int*1e-4 / sys_.area_m2`, `:934` `area_m2 = nx*ny*vox_m*vox_m`
  - **interfacial(면당)**: `:3002` `--asr-film-cycle-ohm-cm2 → Kinetics.asr` → `:873` `rA = self.asr / A_face`, `:1061` `A_face = vox_m*vox_m`
  `compose` 는 **footprint** 값을 만들어 **interfacial** 플래그의 주입 예로 인쇄한다(`:339-342`).
- **재현**: `python3 scripts/cycle_degradation_law.py --n 100 --film-frac 0.5`
  → `N=100  --cycle-n 100 --i0-cycle-mult 0.51616 --asr-film-cycle-ohm-cm2 320.3`
  (그대로 복붙 가능한 STEP4 명령줄).  DBE 베드
  (`docs/data/sdcp318_sigma_sdcp_sweep/step3_sdcp250.json`: `n_bv_faces=503915`, `vox_um=0.4`,
  두께 72.484 µm) 의 interfacial/footprint 비 **≈44×**.  실측 런에서 베드 자신의 선형화
  R_ct0 = 128.5 Ω·cm² (footprint) vs 하드코딩 341.7 = **2.66×**; 0.2C 첫 스텝 셀전압이
  `3.756 V → 1.325 V` (−2431 mV) 로 무너진다.  코팅계 앵커(`CSV:33` LNO 72wt% R_ct0=18.2) 대비로는
  **18.77× 과대**.
- **2차 결과 — F 스윕이 자기 계약을 깬다**: F 는 *고정 총량* 을 두 채널에 **재분배**하는 노브로
  광고되는데(H5 논거 전체가 이것), 옴성 분기는 **외부** R_ct0 를, i0 분기는 런의 **내부** i0 를 쓴다
  ⇒ 저율 총합 `= (g−1)·[R_ct0_model(1−F) + 341.7·F]` 가 **F 에 의존**한다.
  `R_ct0_model = 341.7` 일 때만 재분배다.  즉 스윕이 rate-의존성만이 아니라 **총 저항 자체를
  조용히 바꾼다** = 분리하려던 바로 그 양을 오염시킨다.
- **못 잡는 이유**: selftest `:266-270` 은 `asr_film_cycle_ohm_cm2 > 0` 과 i0 몫 산술만 본다.
  크기·단위·이 런과의 귀속을 검사하는 단언이 **없다**.
- **권장수정 (막는 쪽)**: `--r-ct0-ohm-cm2` 를 **필수 인자로 승격** (베드의 실측 R_ct0 없이는 옴성
  Ω·cm² 를 낼 수 없다) + 그 값이 **interfacial 기준**임을 명시 + step4 쪽에 "ASR_film 이 베드
  R_ct 의 O(1) 배를 넘으면 거부" 가드.  고칠 수 없으면 `--film-frac` 을 **차단**하라.

#### [H2] HIGH-10 의 "콘솔 배너도 조건부" 가 적용되지 않았다 (커밋 메시지가 거짓)
- **[scripts/step4_dyn.py:2857-2863]** 무조건 f-string:
  `f"i0/D_s/OCP/σ_e/κ 는 25°C 상수 (kinetics_T_scaling=NONE). "`.  조건분기는 `_trust_str`(`:2877-2882`) 에만.
- **재현**: `step4_dyn.py --grid g60.npz --ocp-test --out m60.npz --temp-k 333.15 --i0-temp-scale`
  → 한 줄 위 `★i0(T) 스케일: 60 °C → i0 ×6.2545`, 바로 아래
  `⚠ 온도 상태 PARTIAL_sigma_ion+i0@60C — … i0/D_s/OCP/σ_e/κ 는 25°C 상수 (kinetics_T_scaling=NONE).`
  같은 런 npz: `kinetics_T_scaling='I0_ARRHENIUS_kim2025'`, `i0_T_factor=6.254470329169113`.
- **§12 의 간판 경로에서 정확히 HIGH-10 이 표적으로 삼은 모순이 두 줄 간격으로 살아 있고,
  로그에 리터럴 `kinetics_T_scaling=NONE` 이 박힌다.**  ★ 같은 문장의 **세 번째 인스턴스**:
  `:2851-2853` 차단 메시지도 `--i0-temp-scale` 이 켜진 런에서 `⛔ T1-d 부호역전: i0/D_s/OCP 는
  25 °C 상수라 T 를 안 따릅니다` 를 인쇄한다.
- **못 잡는 이유**: selftest 는 `temperature_verdict` 의 **반환 dict** 만 검사한다 — stdout 을 보는
  단언이 없다.  조용한 표면(npz 안의 trust)은 고치고 **가장 시끄러운 표면**(터미널에 실제로 뜨는
  유일한 문장)을 남긴 것.
- **권장수정**: 배너를 `_trust_str` 와 같은 함수로 생성하고, selftest 에 stdout 캡처 단언 1개 추가.

#### [H3] HIGH-7 정정이 **기계판독 기록에 도달하지 않았다** (오히려 반대 문장이 npz 로 나간다)
- **[scripts/cam_kinetics.py:184-186]** `provenance()` 내부:
  `'transfer_assumption': ('앵커는 72 wt% uncoated 한 조성 · post-formation.  Eₐ 가 조성/코팅/사이클 상태에 무관하다고 가정.  **LNO 코팅계 T-스윕은 논문에 없음.**')`
  — HIGH-7 이 "거짓" 이라 판정하고 고쳤다고 한 그 문장 그대로.
- **재현**: `python3 scripts/cam_kinetics.py --temp-c 60 | grep transfer_assumption` (실측 확인).
  이 dict 는 `step4_dyn.py:2821` → `:3053-3054` → `:3061` 로 **모든 온도-스케일 런의 npz
  `temperature.i0_T_provenance`** 에 박힌다.
- **더 무겁다 — 같은 dict 안 자기모순**: 같은 런의 `['temperature']['trust']` 는
  `⚠ 코팅계는 Eₐ 가 다르다 (kim2025 LNO 는 비-Arrhenius)`.  **하나의 아카이브 기록이 그 스윕이
  존재한다고도, 존재하지 않는다고도 주장한다.**  반증 데이터(`anchor_points`) 는 같은 dict 세 키 옆에 있다.
- **못 잡는 이유**: selftest 5d(`:291-301`)는 `RCT_T_ANCHOR_LNO` 배열과 적합 Eₐ 만 본다 —
  **문자열을 읽는 테스트가 없다**.  `provenance` 검사 3건(`:308-311`)도 다른 키만 본다.
- **권장수정**: `:186` 문자열 교체 + selftest 에 "provenance 전 문자열에 `'논문에 없음'` 부재" 단언.

#### [H4] 프로덕션(킷·webapp) 경로는 `--i0-temp-scale` 을 모르고, 배포 zip 이 **거짓 진술** 을 굽는다
- **[webapp/app.py:6336-6377]** `_kit_apply_temperature` 직접 실행 결과:
  - `--i0-temp-scale in run_mpm.sh` → **False**; STEP4 호출에는 `--allow-grid-t-mismatch` 만.
  - `mpm_input.json` `not_applied_to['STEP4 kinetics']` = `'i0 / D_s / OCP dU/dT 앵커 없음 (§F1) — --temp-k 는 굽지 않는다…'` (`app.py:6373`)
  - `applied_to[1]` = `'★--temp-k 는 의도적으로 미주입: i0 앵커가 없어…'`
  - **[webapp/app.py:6332]** `run_mpm.sh` 자체 주석에도 `#   i0/D_s/OCP/σ_e/κ/SE-경도는 앵커 없어 25 °C 상수 유지`
  ⇒ 배포 zip 이 **세 번** "i0 앵커 없음" 을 진술하는데, 앵커(`scripts/cam_kinetics.py` +
  `docs/data/rint_eis_anchors.csv:8-9`) 는 같은 트리 안에 있다.
- **결과**: 웹앱에서 온도를 켜면 **STEP3 σ_ion 만 60 °C, STEP4 kinetics 는 25 °C** 그대로 →
  §12 가 해소했다는 부호역전이 **프로덕션엔 미적용**.
- **도달 범위 grep**: `i0-temp-scale|film-frac|cycle_degradation_law|cam_kinetics` →
  `scripts/{cam_kinetics,cycle_degradation_law,step4_dyn}.py` + `docs/temp_pressure_capability.md`
  외 **0건**.  `webapp/`·`mpm_input_from_case.py` 전무.
- **못 잡는 이유**: `webapp/test_temp_pressure_wiring.py:236` 은 `'STEP4 kinetics' in tp['not_applied_to']`
  = **키 존재만** 확인한다 (내용의 참·거짓 아님) → GREEN 유지.
- **권장수정**: 킷에 `--i0-temp-scale` 을 굽거나, 굽지 않기로 한다면 세 문장을 즉시 정정하고
  §12 헤드라인에 **"CLI 전용 — 킷 경로 미적용"** 을 단다.

#### [H5] `--merge-into-i0` + `--film-frac` 조합에서 성장분 **21.9%가 조용히 증발**
- **[scripts/cycle_degradation_law.py:172-184]** i0 항은 `(tot−1)(1−F)+1` 로 **합산 총량**에서 깎고,
  필름 항은 `(gc−1)·F` 로 **chem-only 총량**에서만 되돌린다.
  합계 `= R0·[tot + F(gc − tot)] ≠ R0·tot`; 누락분 `= F·gc·(gm−1)`.
- **재현**: `--n 0,100 --film-frac 0.5 --merge-into-i0 --ledger led.json` (ledger g_mech=1.510)
  → 의도 `R0·g_total = 1483.27` (ΔR 1141.6) / 실제 `912.49 + 320.3 = 1232.79` = **−16.89%**;
  ΔR 기준으로는 `570.8 + 320.3 = 891.1` = **−250.5 Ω·cm² (21.9%)**.  경고 0건
  (유일한 merge 경고는 `merge_requested_but_chem_only` 인데 여기선 False).
- **못 잡는 이유**: selftest `:227-230`(merge 단독)과 `:266-270`(film 단독)이 **직교로만** 검사한다.
  두 플래그는 argparse 에서 상호배제가 없다.
- **권장수정**: 필름 항을 `(tot−1)·F` 로 통일하거나, 두 플래그 동시 지정을 `ap.error` 로 거부.

#### [H6] `cycle_interphase` provenance 가 **존재하지 않는 앵커** 를 인용한다
- **[scripts/step4_dyn.py:3058-3061]** 모든 열화 런 npz 에
  `'provenance': 'ASSUMED-FORM: mult=kim2025 R_ct(N) anchor; N→mult law pending fit (§6 N1)'`.
  콘솔 쌍둥이 `:3002-3005`, help `:2703`·`:2706` 도 동일.
- **[docs/data/rint_eis_anchors.csv]** kim2025 8행 **전부** `cycle_n=post-formation`
  (30/45/60 은 `T_meas_C`).  유일한 R_ct(N) 앵커는 `yun2023_rct_growth` (`341.7to982.3`, `cycle_n=~100`).
  §13-4 는 올바르게 Yun 을 인용한다.
- **선존 결함이나 `5cbae845` 가 명백히 틀리게 만들었고 `baf34936` 의 "네 개의 거짓 진술" 정리에서도 누락.**
- **못 잡는 이유**: 문자열이라 어떤 selftest 도 대조하지 않는다.
- **권장수정**: `kim2025` → `yun2023_rct_growth (341.7→982.3 Ω·cm² @~100cyc, 30 °C)`.

#### [H7] `--i0-temp-scale` 의 `--help` 가 **반증된 물리 + 정정 전 숫자** 를 가르친다
- **[scripts/step4_dyn.py:2724-2725]** 실측 `--help` 출력:
  `R_ct∝1/i0 이라 이것이 i0 의 온도 앵커다: 60 °C 에서 i0 ×5.60.`
  — HIGH-1 이 거짓이라 선언한 바로 그 비례관계 + 10.5% 과소한 정정 **전** 배수(5.5982).
  코드는 6.2545 를 적용한다.
- **재현**: `python3 scripts/step4_dyn.py --help | sed -n '/--i0-temp-scale/,/--i0-temp-ea-ev/p'`
- **못 잡는 이유**: `test_cli_help` 는 121개 스크립트의 `--help` 가 크래시 없이 도는지만 본다.
  값 대조가 없다.  **이 help 가 플래그의 1차 사양서다.**
- **동류 2건**: `:2731-2736` `--temp-k` help (`D_s·i0·OCP…는 전부 25°C 상수라 T 를 안 따른다` +
  `T≠298.15 로 돌리려면 --allow-unscaled-t 가 필요하다`) — 두 절 모두 이제 조건부로 거짓;
  `:2743` `--allow-unscaled-t` help (`kinetics_T_scaling=NONE 으로 기록된다`) — [H9] 조합에서 거짓.

#### [H8] `G_MECH_BUILTIN = 1.05` — 모듈이 스스로 "CT 를 쓰라" 고 선언하고 Holm 을 하드코딩
- **[scripts/cycle_degradation_law.py:88]** `G_MECH_BUILTIN = 1.05  # (SC-NMC 단결정, mono 원장 실측)`
- **같은 파일의 자기모순**: `:122-125` `read_ledger` docstring —
  *"`rct_holm_rel`(=구속저항 몫)이 아니라 **`rct_ct_area_rel`** 을 쓴다 — `--i0-cycle-mult` 가 건드리는
  채널이 전하이동이라 짝이 맞아야 한다"*.  그런데 **1.05 는 Holm 값**이다
  (`cycle_contact_ledger.py:320-321` `rct_holm_rel = A0/A_` vs `rct_ct_area_rel = A0_area/A_area`;
  mono 궤적 끝점 `rct_proxy_rel = 1.05`).  CT 규약 값은 **1.02**
  (`docs/a10_cycle_chemomech_design.md:150` `| mono | Holm 1.05× | **CT 1.02×(대표)** | 2.87× | ~1% | [0–2%] |`,
  `:152` *"측정 CAM-SE R_int = 전하이동 지배 → **CT(area⁻¹)가 대표규약**"*).
  ⇒ ledger 를 주면 CT(1.02), 안 주면 Holm(1.05) — **같은 g_mech 가 경로에 따라 다른 규약**.
- **재현**: `compose([100],subtract_mech=True)[0]['g_chem'] = 2.737851…`.
  CT 규약이면 `2.8747/1.02 = 2.8184` ⇒ 곱셈분해 기준 **≈2.5× 과잉 감산**
  (가법 f0 몫 ~1% 기준으로는 ≈5×; 배율은 규약에 따라 다르나 **방향과 규약오류는 확정**).
- **부차 결함**: 주석의 `"mono 원장 실측"` 은 틀렸다 — 원장은 ASSUMED-FORM CZM **시뮬레이션**이고,
  CLAUDE.md 상 그 런의 자매 헤드라인(bimodal 1.51×)은 `--poly-mode shrink-proxy` 아티팩트로
  재해석 대기 중이다.  CLI help(`:294`)에는 출처가 우리 시뮬이라는 말이 없다.
  또한 1.05 는 N=100 값인데 원장은 "즉시파단" 을 기록했으므로 기계몫은 **전반부 집중**이다
  — 전 N 상수 divisor 는 또 하나의 미라벨 assumed-form.
- **못 잡는 이유**: selftest `:257-260` 은 `abs(g − G_CHEM/G_MECH_BUILTIN) < 1e-12` 라는
  **자기 상수 대비 산술 항등식** — 어떤 값을 넣어도 통과한다.  규약도 앵커도 검증하지 않는다.
- **권장수정**: 1.05 → 1.02(CT 규약) + 주석을 `"우리 A10 접촉원장 시뮬 추정(ASSUMED-FORM CZM)"` 로
  정정 + selftest 를 `docs/a10_cycle_chemomech_design.md:150` 대조로 교체.
- **참고 — "순환" 지적은 기각**: `subtract_mech` 는 기본 OFF, 기본 출력은
  `g_chem_is_measured_total: True` 로 낙인, 그리고 **어떤 계수도 일치를 위해 조정되지 않는다**
  (실험 1점을 모델 추정으로 *분해* 할 뿐).  frame[4] 가 금하는 교차적합은 아니다.

#### [H9] 가드 오라벨 — `KINETICS_UNSCALED` 를 성립하지 않은 조건에 대해 해제 기록
- **[scripts/step4_dyn.py:740-741]** 계약 없는 그리드의 σ↔동역학 불일치를 `KINETICS_UNSCALED` 로 코딩
  → `:757-758` 이 `--allow-unscaled-t` 로만 해제.  `:2850-2855` 차단 메시지가 그 해법을 권한다.
- **재현**:
  ```
  python3 -c "import sys;sys.path.insert(0,'scripts');import step4_dyn as S;
  e,m=S.temperature_verdict(333.15,None,True,False,True);print(e,m['kinetics_T_scaling'],m['released_guards'])"
  → [] I0_ARRHENIUS_kim2025 ['KINETICS_UNSCALED:--allow-unscaled-t']
  ```
  **동역학은 ×6.2545 로 스케일됐는데 "kinetics unscaled 를 해제했다" 를 영구 기록**한다.
  정작 안 스케일된 것은 σ_ion 인데, 그 코드(`GRID_T_MISMATCH`)와 해법(`--allow-grid-t-mismatch`)은
  이 경로에서 **절대 제시되지 않는다** (`sig_t_c is None` 이라 분기 자체를 안 탐).
- 차단 메시지 자체도 `⛔ T1-d 부호역전: i0/D_s/OCP 는 25 °C 상수라 T 를 안 따릅니다` 라며
  **사용자가 방금 켠 플래그와 정반대** 를 말한다.
- **못 잡는 이유**: selftest (A1)/(A2)(`:2600-2607`)는 **계약 있는** 그리드 두 경우만 본다.
  "계약 없음 + i0 스케일" = H3 가 새로 뚫리지 않게 만든 바로 그 경로가 테스트에 없다.
- **정상참작**: `state` 필드 자체는 정확하다.
- **권장수정**: `:741` 삼항을 `GRID_T_MISMATCH` 로 분기 + 메시지를 i0 스케일 여부로 조건부화.

#### [H10] 회귀 테스트가 **자기 사본** 을 검사한다 — `3918f31b` 수정에 대한 커버리지 0
- **[scripts/step4_dyn.py:2635-2650]** (A8) 단언들이 selftest **내부에서 새로 정의한 헬퍼**
  `_i0_face`(`:2635-2638`)를 검사한다.  프로덕션 배선은 `:3018-3022`.  `main()` 은 어떤 테스트도 호출하지 않는다.
- **직접 실증(수행 후 원복 완료)**: `:3018-3022` 를 `3918f31b` **이전 형태**(`i0_p` 대신 `i0_ref` 에만
  `_i0_tf` 곱)로 되돌리고 `--selftest` → `(A8a)…(A8d)` **네 단언 전부 PASS**,
  `temperature selftest: PASS`, `STEP4-V2 SELFTEST PASS`.
  ⇒ bimodal i0(T) 상쇄라는 HIGH 결함에 대한 실제 회귀 커버리지 = **0**.
- **권장수정**: `_i0_face` 를 `main()` 과 공유하는 모듈-레벨 헬퍼로 추출해야 핀이 생긴다.

---

### 🟠 MED-HIGH / MED

#### [M11] 비순환 테스트의 판별력이 **단일 점 · 여유 0.10 pp** 에 걸려 있다
- **[scripts/cam_kinetics.py:266-268]** tol = 3%.  실측 현행: 30 °C +0.00% / 45 °C **−2.90%** / 60 °C +0.11%.
  버그판(전인자 X): 30 °C +0.00% / 45 °C **+1.90%** / 60 °C **+10.01%** → 60 °C **한 점** 으로만 FAIL.
- **즉 45 °C 에서는 버그판(1.90%)이 정정판(2.90%)보다 앵커에 더 가깝다.**  2.90% 는 3점 적합의
  고유 잔차(구간 Eₐ 0.4049/0.4398)라 물리 오류는 아니지만, `EA_RCT_EV` 나 앵커 집합을 조금만
  건드리면 **정상 코드가 위양성 FAIL 로 뒤집힌다**.
- 커밋 메시지와 `docs/temp_pressure_capability.md:725` 둘 다 **60 °C 의 0.1% 만** 광고하고
  29배 나쁜 45 °C 는 언급하지 않는다.
- **권장수정**: tol 을 점별로 분리(45 °C 는 적합잔차 기반 4%)하거나, 판별용 앵커를 60 °C 단독으로
  명시하고 "이 테스트는 전인자 유무만 판별한다" 를 주석에 적어라.

#### [M12] `--i0-temp-ea-ev` 를 `--i0-temp-scale` 없이 주면 **조용한 no-op**
- **[scripts/step4_dyn.py:2819-2822]** `a.i0_temp_ea_ev` 는 `if a.i0_temp_scale:` 블록 안에서만 읽힌다.
- **재현**: `--temp-k 333.15 --i0-temp-ea-ev 0.4398 --allow-unscaled-t`
  → `kinetics_T_scaling=NONE`, `i0_T_factor=1.0`, `i0_T_provenance=None`.
  0.4398 과 0.4049 두 런이 **bitwise 동일** (max|Δ| = 0.0).
- **위험**: help 가 지시하는 *"구간 Eₐ 0.4049/0.4398 을 쓸어 **밴드로 보고**"* 를 따르다 활성화
  플래그를 빠뜨리면 세 런이 전부 25 °C 미스케일인데 파일명·로그에는 서로 다른 Eₐ 가 붙어
  **"밴드 폭 0 = Eₐ 불확실성 무시가능"** 으로 오독된다.
- **선례 존재**: 같은 파일 `:2791-2794` 가 `--d-s-poly/--d-s-sc`, `--i0-poly/--i0-sc` 의 반쪽 지정을
  *"반쪽 지정 = 침묵 기본값 혼입 금지"* 라며 명시 거부한다 — 이 쌍만 빠졌다.
- **권장수정**: `ap.error('--i0-temp-ea-ev 는 --i0-temp-scale 과 함께만 유효')`.

#### [M13] `--rest` 는 열화 플래그를 조용히 버리면서 온도는 적용했다고 도장을 찍는다
- **[scripts/step4_dyn.py:2935-2983]** rest 분기가 `:2983` 에서 `sys.exit(0)` — `--i0-cycle-mult`(`:2995-3000`)
  와 `_i0_tf`(`:3018-3022`) **이전**이다.  `kin_r = Kinetics(a.i0, …)` 는 raw `a.i0` 로 만들어진다.
- **재현**: `--rest --t-rest-min 5 --init-state st.npz --temp-k 333.15 --i0-temp-scale
  --allow-unscaled-t --cycle-n 100 --i0-cycle-mult 0.37447 --asr-film-cycle-ohm-cm2 320.3`
  → rest npz: `kinetics_T_scaling='I0_ARRHENIUS_kim2025'`, `i0_T_factor=6.2545`,
  **`cycle_interphase` 부재**, `★B-1 계면상(N=100)` 배너 미출력.
- 수치는 `_vw` 정규화로 상쇄돼 무해하나(rest V 는 i0-가중 혼합전위 → 균일 스케일 상쇄),
  **체인 사이클의 rest 세그먼트가 열화를 기록조차 없이 버린다.**
- **권장수정**: rest 분기에 `cycle_interphase` 기록 추가 + `_i0_tf`/`i0_cycle_mult` 적용을 exit 앞으로.

#### [M14] `Eₐ(i0) ≈ 0.39 eV` — 문서의 부호가 반대
- **[docs/temp_pressure_capability.md:86]**(행④, "현황 표") `Eₐ(i0) ≈ 0.39 eV (R_ct 에서 유도)`,
  **[:220]**(mermaid 현황도) 동일.  근원은 **[:293]**(T2-a) `Eₐ(i0) ≈ Eₐ(R_ct) − k·T̄ ≈ 0.39 eV`.
- **올바른 유도**: `i0 ∝ T·exp(−Eₐ_Rct/k_BT)` ⇒ `d ln i0/d(1/T) = −(T + Eₐ_Rct/k_B)`
  ⇒ **`Eₐ_i0 = Eₐ_Rct + k_B·T̄`** — **가산**이다.  `0.4212 + 0.0274 = 0.4486 eV`.
  코드의 정확형 `(T/T_ref)·exp[…]` 가 30→60 °C 에서 실제로 함의하는 유효 Eₐ = **0.4486 eV** ✔
- **피해**: 행④대로 구현하면 `i0(60) ×4.927` = 코드(6.2545) 대비 **−21.2%** 로 조용히 갈린다.
- **못 잡는 이유**: baf34936 은 §12(`:718-726`)만 갱신하고 행④·mermaid 를 남겼다.  코드는 정확형을
  쓰므로 "유효 Eₐ" 자체가 등장하지 않아 **어떤 selftest 도 이 숫자를 읽지 않는다.**
- **권장수정**: 행④·`:220`·`:293` 을 `0.4486 eV (= Eₐ_Rct + k_B·T̄, 가산)` 로 정정.

#### [M15] `√t → √N` — Park 앵커는 `Ω·h⁻⁰·⁵` 인데 모델은 사이클 지수로 인덱싱
- **[scripts/cycle_degradation_law.py:50]** `· 코팅/첨가제 계면상: **선형-√t** (확산제한 Wagner film) → g_chem ∝ √N`
  **[:112]** `f = {'sqrt': math.sqrt(r), …}[shape]`, `r = n/n_anchor` — **시간 인자가 함수 전체에 없다.**
  **[docs/step5_cycle_degradation.md:55-56]** 앵커 기울기를 `25.73 Ω·h⁻⁰·⁵` (명시적 시간 단위) 로
  적어놓고 다음 줄에서 `⇒ 화학 CEI 채널 = √N(우리 기본값 문헌지지)` 로 결론한다.
- Wagner 확산제한 성장은 `δ ∝ √t`.  `√N ≡ √t` 는 **사이클 소요시간이 고정일 때만** 성립.
  Yun 앵커 0.33C ≈ 6.06 h/cyc, 2C = 1.0 h/cyc ⇒ 같은 N 에서 **√6.06 = 2.462× 과대**,
  0.2C(10 h) ⇒ **1.284× 과소**.
- **정상참작**: `:69` 와 배너 `:332` 가 rate 차이를 **인쇄**한다.  그러나 정량화·보정이 없고
  √t→√N 단계는 여전히 "문헌지지" 로 남는다.
- **권장수정**: 기울기가 `h⁻⁰·⁵` 를 달고 있으므로 **수정 가능** — N 이 아니라 `Σt` 로 인덱싱하고
  `--c-rate` 를 받아 `√(N·t_cyc/t_anchor)` 로.  못 하면 "문헌지지" 라벨을 **ASSUMED** 로 내려라.

#### [M16] `docs/temp_pressure_capability.md` §9-1 현황표가 **양방향으로** 틀렸다
- **[:494]** `**T1-d 부호-역전 가드** … ⛔ **미구현** | 경고 없음 (§3-3① 위험 그대로)`
  → 실제로는 구현돼 **hard-block** 한다 ([H9] 재현).
- **[:495]** `i0(T) / R_ct(T) · D_s(T) · OCP dU/dT | ⛔ **미구현** | 25 °C 상수`
  → i0(T) 는 `028404ef` 로 구현, 같은 문서 §12 의 전부.
- **[:97-100]**(§3-3①)도 여전히 부호역전을 "가장 위험한 3개" 로 열거하며 전방 포인터가 없다.
  **세 곳이 살아있다고, 한 곳이 고쳤다고 말한다.**
- **권장수정**: §9-1/§3-3① 을 §12 기준으로 갱신.

#### [M17] §9-3② vs §12-2 — 그리고 **아이러니하게 §9-3 쪽이 프로덕션에선 여전히 참**
- **[:542]** `**STEP4 kinetics 의 부호 역전(§3-3①)은 그대로다.** … 킷은 그래서 --temp-k 를 굽지 않는다`
  ↔ §12-2(`:730-744`) `부호역전 해소`.
- [H4] 대로 **킷 경로는 실제로 미적용**이므로 §9-3② 가 참이다 ⇒ §12 헤드라인
  `⇒ --temp-k 가 비로소 쓸 수 있는 노브가 됐다` 에 **"CLI 전용"** 단서가 빠졌다.
- **권장수정**: §12 헤드라인에 단서 추가 (또는 [H4] 를 고쳐 §9-3② 를 무효화).

#### [M18] R_w → D_s(T) 경로가 함정으로 열려 있다 (행⑤ 기각 사유 불완전)
- **[docs/temp_pressure_capability.md:87]**(행⑤)·**[:303]**(T3-a) 는 `T_w` 비단조(2929→1208→2350 s)
  만 들어 D_s(T) 를 기각한다.  **그러나 같은 셀의 `R_w` 는 단조** (215.5→106.4→81.0,
  `litdb/papers/kim2025_impedance_decoupling_tlm_assb.md:363-367`) → Eₐ=0.2856 eV → `D_s(60)/D_s(25)=3.215`.
  누군가 이걸 발견해 "빠진 앵커를 찾았다" 며 배선할 것이다.
- **둘 다 못 쓰는 진짜 이유**: `α_warburg = 0.31/0.36/0.27` — **세 온도 전부 <0.5**
  (`docs/data/kim2025_tlm_kinetics_anchors.csv:43-45` 가 30 °C 에 대해 `<0.5 strong frequency dispersion`
  이라 **자기 라벨**).  α≈0.3 이면 유한공간 확산 소자가 아니라 분산 프로세스 흡수체다.
  `R_w ∝ (dU/dx)/D_s` 와 `T_w ∝ 1/D_s` 가 같이 움직여야 하는데 어긋난다 = **fit 식별불가**.
- **부차**: 45/60 °C 의 α 는 정본 CSV 에 없다(30 °C 3행만) = litdb 카드↔CSV 드리프트.
  또한 이 R_w 는 **코팅(LNO 62wt%) 셀** 데이터 — 배선하면 uncoated 앵커 모델에 코팅 Eₐ 를 섞는다.
- **권장수정**: 결론(앵커 없음)은 옳으므로 **명시 사유를 `α<0.5` 로 교체** 해 R_w 경로를 함께 봉쇄.

#### [M19] §13-2 의 전제가 **자기 litdb 카드에 의해 반증** + `ANCHOR_T_CYCLE_C` 는 매직넘버
- **[docs/temp_pressure_capability.md:793-801]** §13-2 는 `노화온도가 확정된 *측정* 앵커는 0건`
  이라 단정하며 `yun2023 … 전부 공란` 을 든다.  CSV 셀이 빈 것은 사실
  (`yun2023_rct_growth,…,~100,,,,table_verified_litdb`).
  **그러나 litdb 카드가 값을 확정한다**: `litdb/papers/yun2023_*.md:106`
  `갈바노 사이클 2.5–4.3 V vs Li/Li⁺, **30 °C** … cycling **0.33C**` (직접 확인).
  ⇒ Yun 2023 **은** 노화온도가 확정된 측정 앵커이고, §13-2 의 전제는 HIGH-2 자신의 발견에 의해 거짓.
  실제 문제는 "확정 불가" 가 아니라 **CSV 의 `T_cycle_C` 칸이 비어 있는 것**.
- **부차 결함**: `cycle_degradation_law.py:86` `ANCHOR_T_CYCLE_C = 30.0` 은 **모듈 자신의 기준으로
  매직넘버** — H2 selftest 는 자기 리터럴과만 대조(`abs(… − 30.0) < 1e-9`)한다.
  대조군: `G_CHEM_AT_ANCHOR` 는 CSV 크로스체크, `EA_RCT_EV` 는 재유도.
- **권장수정**: `yun2023_*` 행의 `T_cycle_C` 를 30 으로 채우고 상수를 그 값과 대조.
  "Eₐ_deg 를 배선하지 말 것" 이라는 §13 결론 자체는 영향 없음.
- **잔여 라벨 문제**: `:65-68`·`:93`·`:332-333` 이 매 런
  `"사용자 랩은 60 °C 노화 → 크기는 **하한**으로만 읽을 것"` 을 무조건 인쇄한다.
  정본 CSV 는 그 셀들(`lab_sbe/dbe/csus_cycled`)에 `T_cycle_C` 공란 + `⚠T_cycle 미지정(랩 30/45/60 중)`
  이라 적었다(유일한 60 은 `lab_sus_cycled`, precision `projected_literature`).
  30 °C 였다면 Yun 의 30 °C 2.87× 는 하한이 아니라 **정합값**이다.
  → 조건부 라벨(`⚠ 이 셀의 노화온도 미확정`)로 바꾸는 것이 정직하다.
  (⚠ "HIGH-2 와 HIGH-8 이 양립 불가" 라는 더 강한 주장은 **기각** — §3 참조.)

#### [M20] `--out-json` 헤더가 rows 와 모순 + 재현에 필요한 플래그 미기록
- **[scripts/cycle_degradation_law.py:344-349]** 재현:
  `--n 100 --subtract-mech --film-frac 0.3 --out-json oj.json`
  → 헤더 `g_chem_at_anchor = 2.874743927421715` vs `rows[0].g_chem = 2.737851359449252`.
  top-level 키는 `['shape','anchor','g_chem_at_anchor','n_anchor','assumed_form','no_temperature_dependence','rows']` 뿐.
- **정정(부분)**: `subtract_mech` 는 `rows[*].g_chem_is_measured_total` 로,
  `merge_into_i0` 는 `i0_mult_channel` 로, `film_frac>0` 여부는 `asr_film_cycle_ohm_cm2>0` 로 **역추적 가능**.
  **역추적 불가**: F 의 정확한 값, ledger 경로, `r_ct0_ohm_cm2` (F 를 역산하는 데 필요).
- **권장수정**: top-level 에 `flags: {film_frac, merge_into_i0, subtract_mech, ledger, r_ct0_ohm_cm2}` 추가
  + 헤더에 `g_chem_at_anchor_effective` 병기.

#### [M21] Yun SC-NMC "기계몫 작음" 정당화가 **프로젝트 자신의 형태론 정정과 반대**
- **[scripts/cycle_degradation_law.py:35-37]** *"Yun 은 CAM 균열을 배제하려고 단결정 NCM 을 일부러
  채택했고 … 기계몫은 ≈5% 로 작다"*.
- **[CLAUDE.md 2026-07-22 정정]** *"**SC(2µm)=계면 debond** / poly(6µm)=입계 내부 void"*.
  단결정은 격자 부피변화를 흡수할 내부 입계가 없어 **전량이 CAM|SE 계면으로 전달**된다 —
  SC 는 debond 가 R_ct 에 *가장 잘 보이는* 형태론이지 무시할 형태론이 아니다.
- **다만 숫자(1.05/1.02)는 그 debond 를 실제로 모델링하는 원장 출력이라 함께 무너지지는 않는다
  — 틀린 것은 붙여 놓은 *이유*다.**
- **권장수정**: `:35-37` 산문 교체 (`SC 는 계면 debond 형태론 — 기계몫이 작은 것은 CZM 원장이
  그렇게 산출했기 때문이지 SC 라서가 아니다`).

#### [M22] `RCT_T_ANCHOR_LNO` 가 CSV 크로스체크 없는 하드코딩
- **[scripts/cam_kinetics.py:79]** `RCT_T_ANCHOR_LNO = ((30,22.4),(45,8.7),(60,7.6))`.
  대조군: selftest 2단계는 `RCT_T_ANCHOR` 를 `rint_eis_anchors.csv` 에서 재읽고,
  1단계는 `EA_RCT_EV` 를 재유도한다.  이 배열만 매직넘버.
- **부차 전사충돌 위험**: 같은 표에 `R_ion,fullcell,LNO,LPSCl,62,30 = 8.7` 이 있어
  45 °C R_ct 값 8.7 과 충돌 가능성 — CSV 대조가 있으면 자동 검출된다.
- **권장수정**: selftest 에 `kim2025_tlm_kinetics_anchors.csv` 대조 추가.
- ⚠ **[REFUTED 부분]** "45 °C 행은 wt% 기저가 달라 비교불가 → 비-Arrhenius 결론이 아티팩트" 는
  **거짓** — 세 행 모두 62 wt% 다.  CSV note `temperature sweep (45C row, not same wt% base)` 는
  짝 행 `72,45,139.6 … temperature sweep **72wt%**` 와의 **대조 표기**다.  §3 참조.

---

### 🟡 LOW

- **[L1] [scripts/cam_kinetics.py:37, :30]** 정정의 헤드라인 숫자가 세 군데서 불일치.
  실측 `i0_temperature_factor(45.0) = 2.99067518922589`, `(60.0) = 6.254470329169113`.
  `:37` = `45 °C ×**2.947**` ✗ (docs `:720` 은 ×2.991 ✓ — **코드 소유 모듈만 틀렸다**;
  어떤 Eₐ 변종도 아닌 baf34936 신규 손계산 오류).  `:30` = `정합 **6.2554**` ✗ (자리 전치, 실제 6.2545).
- **[L2] [scripts/step4_dyn.py:2696-2697]** α 합 가드 없음.  `R_ct = RT/(F·i0·A)` 는 `α_a+α_c=1`
  에서만 정확 (실측 α=(0.7,0.5) → `1/g=0.010705` vs `0.012846`, 비 = 1.2 = α합).
  `--alpha-a 0.7 --alpha-c 0.5` 가 통과하고 절대 R_ct 가 20% 어긋난다.
  **T-스케일링 자체는 무해** (α 는 T-무관, 비에서 상쇄) → 수치결함이 아니라 주장/가드 결함.
- **[L3] [scripts/cycle_degradation_law.py:149-190]** `compose()` 에 `film_frac` 범위 가드 없음
  (검증은 `main():309-310` 뿐, 그것도 `read_ledger` 뒤).
  실측 `compose([100], film_frac=1.5)['i0_cycle_mult'] = 15.967` (사이클링이 i0 를 **16배 개선**),
  예외 0, `i0_is_lower_bound_penalty=False`.  step4 `:2995-2996` 은 `<=0` 만 거부.
  위험창 `1 < F < 1.53`.  **외부 소비자 0건이라 CLI 로는 도달 불가 → LOW.**
- **[L4] [scripts/cam_kinetics.py:129]** `rct_temperature_factor` 는 자기 selftest·`main()` 출력표
  외에 **프로덕션 소비자 0건**.  HIGH-1 의 핵심 구분(순수 Arrhenius ≠ 1/i0)이 실행 경로에서는
  강제되지 않고 테스트 안에서만 산다.
- **[L5] [scripts/cam_kinetics.py:187-188]** `still_unanchored` 가 `--asr-film` /
  `--asr-film-cycle-ohm-cm2`(→`Kinetics.asr`) / `--r-int-ohm-cm2`(→`:1467`) 를 빠뜨린다 —
  전부 `_i0_tf` 가 안 건드려 60 °C 에서도 25 °C 고정.
  *(이 셋은 모델 상수가 아니라 사용자 입력이라 목록 포함은 규약 논쟁 — 다만 아래는 확정.)*
  **확정 잔여**: `transfer_assumption` 에 **이중표현 경고가 빠졌다**.
  `docs/data/kim2025_tlm_kinetics_anchors.csv:57` note `uncoated R_ct ~20x coated (**oxidative
  decomposition**)` + `docs/temp_pressure_capability.md:293` *"R_ct 는 계면 화학상태도 반영 →
  순수 kinetics Eₐ 로 읽으면 **과대**"* — 리포 자신이 이미 적어 두었는데 전이가정 문구에는 없다.
- **[L6] i0_T_factor_band 가 코팅값을 배제한다.**  밴드(`cam_kinetics.py:158-165`, 실측
  `×5.851–6.749`)는 **적합-내 구간 스프레드** 로만 만들어져 코팅계 값 `4.085 ∉ [5.851, 6.749]`.
  즉 밴드가 실제 **전이 불확실성** 을 과소표현한다.  (밴드 규율 자체는 적용돼 있음 — §3 참조.)
- **[L7] [scripts/cycle_degradation_law.py:84]** `YUN_RION_FROM/TO = 126.0/156.0` (1.23810×) vs
  litdb 정본 카드 `:124-125` **126.1 → 155.6** (1.23394×), 0.34% 차.
  코드는 **선언된 정본**(`rint_eis_anchors.csv`)을 정확히 따르고 selftest `:244-246` 이 대조하므로
  코드 결함이 아니라 CSV 반올림.  `G_ION_AT_ANCHOR` 는 selftest 정성 부등식 1곳에서만 쓰여
  **영향 0**.  (수정 대상은 litdb 정본 브랜치 — 이 브랜치 `litdb/` 는 동결 스냅샷.)
- **[L8] [scripts/step4_dyn.py:2912-2914]** `meta['am_electro_split'] = {'i0_poly':3.0,'i0_sc':1.0}`
  는 **스케일 전 CLI 값**, `meta['i0'].min/max`·`i0_ref_p_Am2` 는 실효값
  (`3.0×0.37447×6.254470 = 7.026334512` ✓).  두 기록이 2.34× 어긋나고 어느 쪽이 CLI 값인지 라벨 없음.
  **다만 두 기록 모두 이름은 정확** (`am_electro_split` = 분리 설정, `meta['i0']` = 실효값)이고
  잘못된 값이 산출되지 않는다 — 모호성이지 침묵-오답 아님.

---

## 3. 기각된 지적 (재등장 방지 — 한 줄씩)

| 지적 | 판정 | 기각 사유 |
|---|---|---|
| "대상 커밋 4개가 존재하지 않는다" | ❌ REFUTED | `git cat-file -t` = commit ×4.  롤백 트리(`607933c9`) 를 읽은 것.  **"코드에 X 없다" 전에 `git rev-parse HEAD`** |
| LNO 45 °C 행은 wt% 기저가 달라 비-Arrhenius 결론이 아티팩트 | ❌ REFUTED | 세 행 모두 **62 wt%**.  CSV note 는 짝 행(`72wt%`) 과의 대조 표기.  `docs §T2-a`(커밋 **이전**)가 독립적으로 같은 결론을 적었다 |
| "생산 레시피는 LNO 코팅이라 uncoated 앵커는 1.53× 과대" | 🔶 산술 ✔ / 결함 ✗ | 기본 경로는 **bare** (`webapp/app.py:3584` `coating='none'`, `coating_presets.py:22-25`).  그리고 이 항목은 **HIGH-7 이 이미 처리** — 신규 아님.  살아남은 알갱이는 [H3](provenance 문자열) 뿐 |
| "H1 이후 D_s 동결이 최대 오차인데 가드가 없다" | ❌ 결함으로는 REFUTED | 미앵커 사실이 **4곳에 라벨**됨 (`step4_dyn.py:743` 조건부 · `:778-780` trust · `cam_kinetics.py:60`·`:187-188` · `docs:87` 행⑤).  또한 이 주장은 R_w 에서 뽑은 Eₐ=0.2856 을 쓰는데 **같은 보고서의 [M18]이 그 경로를 사용불가라 선언** = 자기모순.  (다만 "2C 가 확산지배" 라는 **함수형 논증 자체는 옳다** — `d ln η/d ln i` = 1.000(확산) vs 0.522(반응@2C) → 오케스트레이터 전제가 역전) |
| `G_MECH_BUILTIN` 이 **순환**(모델 출력으로 실험 앵커 세척) | ❌ REFUTED | `subtract_mech` 기본 OFF, 기본 출력 `g_chem_is_measured_total: True` 낙인, **어떤 계수도 일치를 위해 조정되지 않음**.  frame[4] 가 금하는 것은 두 모델의 상호 캘리브 — 여기선 실험 1점의 *분해*.  (규약오류 [H8]·형태론 정당화 역전 [M21] 은 별건으로 CONFIRMED) |
| `--film-frac` 이 §F1 위반 (앵커 없는 값) | ❌ REFUTED | `:46`·CLI help `:298-299` 가 `⚠ F 의 물리적 값은 앵커가 없다(§F1) — 스윕 전용이다` 라 명시.  §F1 은 미앵커 값의 **라벨**을 요구하고 그것은 이행됨 |
| "`--film-frac` 기본 0 은 하한이 아니다 (저율서 과대)" | ❌ REFUTED | 선형 극한에서 `R_ct = RT/(F·i0·A)` ⇒ i0 를 g 로 나누면 `ΔR = R_ct0(g−1)` = **옴성 분기와 정확히 동일**.  두 채널은 저율에서 **일치**, 고율에서만 갈림 ⇒ `"고율 penalty 하한"` 라벨이 정확 |
| "`--film-frac` 이 열화를 **키우는 것**이 버그" | ❌ REFUTED (프레이밍) | 증가는 H5 의 **의도된 산출**(ohmic η∝I vs log η∝asinh, 1.2–3.1× 과소평가 해소).  진짜 결함은 **면적규약·외부 R_ct0** = [H1] |
| TREND-only Eₐ 로 유효숫자 5자리 보고 = §F1 보고 위반 (밴드 규율 미적용) | ❌ REFUTED | 밴드가 **이미 산출·인쇄**됨 (`cam_kinetics.py:158-165`, `:304-307` selftest "단일값 보고 방지", `step4_dyn.py:2825-2828` 모든 스케일 런).  실측 `×5.851–6.749` 병기.  T_REF=25 규약도 `se_material.py:44-52` 선언 + `cam_kinetics.py:81`·`:318-319` 대조.  **살아남은 알갱이 = [L6]**(밴드가 코팅값 4.085 배제) |
| "b1_chem_fade / se_material 에 온도 인자가 없어 60 °C fade 가 30 °C 속도로 **조용히** 돈다" | ❌ REFUTED | 롤백 트리의 파일.  대상 모듈은 **5중 라벨**(`cycle_degradation_law.py:59-69`·`:86`·`:187`·`:332-333`·selftest `:251-252`).  그리고 요구된 하드블록은 이 모듈에서 **구현 불가** — 온도 인자를 애초에 받지 않으므로 게이팅할 대상이 없다.  올바른 자리는 STEP4 합성 지점 |
| "HIGH-2 와 HIGH-8 이 양립 불가한 전제 위에 있다" | ❌ REFUTED | HIGH-8 이 무너뜨린 것은 "**앵커 행**에 노화온도가 기록돼 있다" 이지 "랩 프로토콜이 60 °C 다" 가 아니다.  `docs:791` 이 정정 후에도 랩 프로토콜 60 °C 를 유지 — 둘은 양립 가능.  **살아남은 잔여 = [M19] 조건부 라벨** |
| OCP 엔트로피항 (dU/dT) | 🔶 결함 아님 | 크기는 `docs:88` 행⑥(2–14 mV) 에 이미 문서화.  상쇄 구조 분해(matched x 상쇄 / 절대 V(t)·종료용량·CV 길이 비상쇄)는 **옳고 라벨 개선 제안으로 유효**하나 결함은 아님.  또한 −0.15 mV/K 는 미앵커 0.05–0.4 밴드에서 리뷰어가 고른 단일값 |
| "LPSCl 분해율 Eₐ 문헌 부재" 재확인 | ✅ **주장 유지** | 216 카드 전수 재확인 + 근접후보 기각사유 정확 (wang2022 DSC 250–800 °C · **kim2025 0.42 eV = 전하이동 kinetics, 분해율 아님** · ma2024 = 수분 가수분해 · yang2025 · koo2025 액체계).  **Joule v2 의 Eₐ-free 재분배기 설계 유지가 정답** |
| A3 의 인용 수치 (`V=3.944409`, `10.082/16.967 mV`, `ΔR 219.3/369.0`, `R_ct0≈117`) | ❌ REFUTED | 하네스 `regress/make_grid.py` 가 **이 HEAD 에 존재하지 않는다**.  메커니즘([H1])은 살아있고 수치는 `_build_sandwich(6,12)` 기반 재측정치로 대체 |

---

## 4. 온도 축이 **프로덕션 경로에서** 실제로 무엇을 하는가 (end-to-end)

### 4-1. 경로별 도달 범위

```
[webapp UI 온도 셀렉터]
   └→ webapp/app.py:_kit_apply_temperature(td, T_C, …)
        ├─ STEP3 payload:  --temp-c <T>          → σ_ion 만 T 로 구움  ✅
        ├─ STEP4 호출   :  --allow-grid-t-mismatch  (★ --temp-k 미주입, --i0-temp-scale 없음)
        └─ mpm_input.json / run_mpm.sh:  "i0 앵커 없음" ×3   ← [H4] 거짓 진술

[손 CLI]
   └→ scripts/step4_dyn.py --temp-k <T> --i0-temp-scale      ← §12 가 고쳤다는 그 경로
        └→ cam_kinetics.i0_temperature_factor(T)  →  i0 ×6.2545 @60 °C  ✅
             + npz meta.temperature.{state, kinetics_T_scaling, i0_T_factor,
                                     i0_T_factor_band, i0_T_provenance, trust,
                                     released_guards}
```

**⇒ 결론: `--i0-temp-scale` 은 손 CLI 전용이다.  킷·webapp 어디에도 배선되지 않았고
(`grep` 결과 `scripts/{cam_kinetics,cycle_degradation_law,step4_dyn}.py` + `docs/` 외 0건),
따라서 프로덕션에서 온도를 켜면 여전히 "σ_ion 만 60 °C 인 25 °C 전극" 이며 §3-3① 부호역전이
살아 있다.  §12-2 의 "부호역전 해소" 헤드라인은 CLI 한정이다.**

### 4-2. 라벨의 도달 범위 (요청 항목)

| 키 | 헬퍼 stdout | `--out-json` | step4 npz meta | 킷 zip | webapp/뷰어 |
|---|---|---|---|---|---|
| `i0_T_factor` · `i0_T_factor_band` · `Ea_is_user_override` | — | — | ✅ `temperature.i0_T_provenance` | ❌ | ❌ 표시 코드 0건 |
| `transfer_assumption` | — | — | ⚠ **[H3] 거짓 문장으로** 도달 (같은 dict `trust` 와 자기모순) | ❌ | ❌ |
| `kinetics_T_scaling` / `released_guards` | — | — | ⚠ **[H9] 오라벨로** 도달 | ❌ | ❌ |
| `asr_film_cycle_ohm_cm2` | ✅ | ✅ | ✅ 숫자만 (`cycle_interphase`) | ❌ | ❌ |
| `cycle_interphase.provenance` | — | — | ⚠ **[H6] 없는 앵커 인용** | ❌ | ❌ |
| `merge_requested_but_chem_only` · `g_chem_is_measured_total` · `i0_is_lower_bound_penalty` · `anchor_T_cycle_C` | ✅ | ✅ | ❌ **전무** | ❌ | ❌ |

**⇒ HIGH-2/4/5/9 가 추가한 라벨은 헬퍼 화면에만 살고, STEP4 로는 float 두 개
(`i0_cycle_mult`, `asr_film_cycle_ohm_cm2`) 만 건너간다.  그 두 float 가 도착한 곳의 provenance 는
[H6] 처럼 잘못된 논문을 인용한다.**

### 4-3. 60 °C 런에서 실제로 스케일되는 것 / 안 되는 것

| | 25 °C → 60 °C | 근거 |
|---|---|---|
| **σ_ion** | ×2.500 (그리드에 구워짐) | STEP3 payload `--temp-c` |
| **BV 열전압 f=F/RT** | 자동 | `--temp-k` |
| **i0** | ×6.2545 (CLI 전용) | `cam_kinetics`, kim2025 R_ct(T) |
| D_s · OCP dU/dT · σ_e · κ · SE 경도 H/σ_y · 분해율 | **×1.00 고정** | 앵커 0건 (§F1) |
| `--asr-film` · `--asr-film-cycle-ohm-cm2` · `--r-int-ohm-cm2` | **×1.00 고정** | 사용자 입력, `_i0_tf` 미적용 → [L5] |

**신뢰 금지 (T ≠ 25 °C)**: η 분해(옴/반응/확산), R_int 분해, EIS/DRT arc 귀속, 확산 무릎·종료용량,
**그리고 반응분포/current-focusing** — `λ ∝ √(σ_ion·R_ct)` 이고 이미 선언된 Eₐ_ion 밴드로
`λ(60)/λ(25) = 0.723(0.29) / 0.925(0.41) / **1.024(0.46)**` ⇒ **밴드가 1 을 가로질러 방향조차 미결**.
(이 항목은 현행 층별 신뢰금지 표에 **없다** → 추가 필요.)

**생존 (공통모드 상쇄)**: 동일 율에서의 **SBE − DBE 차이**.

---

## 5. 다음 라운드 우선순위

### P0 — 막거나 고쳐라 (그럴듯한 값이 통과 중)
1. **[H1] `--film-frac`** — `--r-ct0-ohm-cm2` 를 **필수 인자로 승격**(베드 실측 R_ct0 없이 옴성 Ω·cm²
   금지) + interfacial 기준 명시 + step4 에 "ASR_film 이 베드 R_ct 의 O(1) 배 초과 시 거부" 가드.
   **못 하면 플래그를 차단하라.**  현재 상태로는 자기 출력의 복붙 명령줄이 셀을 3.756 V → 1.325 V 로 무너뜨린다.
2. **[H5] merge+film 비보존** — 필름 항을 `(tot−1)·F` 로 통일하거나 두 플래그 동시 지정 `ap.error`.
3. **[H4] 킷 경로** — `--i0-temp-scale` 을 굽거나, 안 굽는다면 `mpm_input.json`·`run_mpm.sh` 의
   "i0 앵커 없음" 세 문장을 즉시 정정하고 §12 헤드라인에 **"CLI 전용"** 을 달아라.
4. **[H10] 회귀 커버리지 0** — `_i0_face` 를 `main()` 과 공유하는 모듈-레벨 헬퍼로 추출.
   지금은 `3918f31b` 의 HIGH 수정을 되돌려도 전 selftest 가 PASS 한다.

### P1 — 방출 문자열 정정 (한 줄씩, 위험 낮고 효과 큼)
5. **[H2]** `step4_dyn.py:2857-2863` 배너 조건부화 (+ `:2851-2853` 차단 메시지)
6. **[H3]** `cam_kinetics.py:186` `transfer_assumption` (+ selftest 에 문자열 단언)
7. **[H6]** `step4_dyn.py:3061` / `:3002-3005` / `:2703`·`:2706` — `kim2025` → `yun2023_rct_growth`
8. **[H7]** `step4_dyn.py:2724-2725` `--i0-temp-scale` help (+ `:2731-2736` `--temp-k`, `:2743` `--allow-unscaled-t`)
9. **[L1]** `cam_kinetics.py:37` `2.947 → 2.991`, `:30` `6.2554 → 6.2545`

### P2 — 규약·가드
10. **[H8]** `G_MECH_BUILTIN` 1.05 → **1.02 (CT 규약)** + 주석 `"mono 원장 실측"` → `"ASSUMED-FORM CZM 시뮬 추정"`
    + selftest 를 `docs/a10_cycle_chemomech_design.md:150` 대조로 교체
11. **[H9]** `:741` 삼항을 `GRID_T_MISMATCH` 로 분기 + 메시지 조건부화
12. **[M12]** `--i0-temp-ea-ev` 반쪽 지정 `ap.error` (선례 `:2791-2794`)
13. **[M13]** `--rest` 분기에 열화 플래그 적용·기록
14. **[L2]** `α_a+α_c` 합 가드, **[L3]** `compose` 의 `film_frac` 범위 가드

### P3 — 문서 정합
15. **[M16]** §9-1 현황표 + §3-3① 갱신, **[M17]** §12 헤드라인에 "CLI 전용" 단서
16. **[M14]** `Eₐ(i0) 0.39 → 0.4486 eV (가산)` — 행④ `:86` · mermaid `:220` · T2-a `:293`
17. **[M18]** 행⑤·T3-a 의 D_s 기각 사유를 `α<0.5 (0.31/0.36/0.27)` 로 교체해 R_w 경로 봉쇄
18. **[M19]** `rint_eis_anchors.csv` 의 `yun2023_*` 행에 `T_cycle_C=30` 기입 + §13-2 전제 정정
    + `cycle_degradation_law` 의 랩 60 °C 라벨을 조건부화
19. **[M15]** √t→√N 을 `Σt` 인덱싱으로 고치거나 "문헌지지" → **ASSUMED** 강등
20. **[M20]** `--out-json` 에 `flags` 블록, **[M21]** SC 형태론 정당화 산문 교체,
    **[M22]** `RCT_T_ANCHOR_LNO` CSV 크로스체크

### P4 — 테스트 위생 (다음 리뷰에서 같은 결함이 또 통과하지 않게)
21. **[M11]** 비순환 테스트 tol 을 점별 분리 (현 여유 0.10 pp, 판별력이 60 °C 한 점에 걸림)
22. **자기-상수 항등식 selftest 를 앵커·규약·크기 단언으로 교체** —
    `cycle_degradation_law.py:257-260`(`G/G_MECH` 산술), `:266-270`(`asr > 0`) 은
    **어떤 값을 넣어도 통과한다.**  같은 패턴이 [H8] [H1] [L3] 를 동시에 통과시켰다.
23. **stdout 을 보는 단언 도입** — [H2] 는 반환 dict 만 보는 테스트 구조 때문에 살아남았다.
24. **문자열 회귀 핀** — `--help` · 배너 · provenance 는 현재 어떤 테스트도 값을 대조하지 않는다
    ([H3] [H6] [H7] 전부 동일 원인).

---

## 부록 — 이번 라운드의 공통 패턴

**`baf34936` 은 docstring 과 `docs/` 의 *산문* 을 고쳤지만, 실제로 *방출되는* 문자열은 고치지 않았다** —
CLI help ([H7]) · 콘솔 배너 ([H2]) · npz provenance ([H3] [H6] [H9]) · 킷 `mpm_input.json`/`run_mpm.sh` ([H4]).
그래서 반증된 주장들이 **정확히 사용자와 리뷰어가 읽는 아티팩트 안에서 살아남았고**,
그동안 전 selftest · `test_cli_help`(121) · webapp 2종 스위트는 GREEN 을 유지했다.

여기에 더해 **selftest 가 결함 상태를 적극적으로 못박고 있는 것이 5건** — [H1] [H8] [L3] [M11] [H10].
특히 `cycle_degradation_law.py:257-260` 과 `:266-270` 은 **자기 상수 대비 산술 항등식**이라
어떤 값을 넣어도 통과한다.  **앵커·규약·크기를 보는 단언으로 교체하지 않으면 다음 리뷰에서도
같은 결함이 다시 통과한다.**

프로젝트 규약 §F1("앵커 없는 값 금지") 과 "고칠 수 없으면 정직하게 막아라" 의 관점에서,
이번 라운드에서 **막아야 할 것은 `--film-frac` 하나**다 (베드 R_ct0 를 모르는 채로 옴성 Ω·cm² 를
낼 수 없다).  나머지는 전부 **문자열 정정 + 가드 추가** 로 닫힌다.

---

## ★ 조치 결과 (2026-08-03, commit `ea90f6ad`) — 16/16 CLOSED

이 리뷰가 지적한 **HIGH 10 + MED 7 + LOW 3** 을 전부 수정했다.  이 절이 정본이므로 위 본문의
"현재 상태" 기술(§4-1 배선도, §4-2 도달범위 표 등)은 **수정 전 스냅샷**으로 읽을 것.

### 규약: 고친 것마다 회귀 핀 + 그 핀의 **뮤테이션 검증**

이 리뷰의 근본 원인은 결함 자체가 아니라 **selftest 가 결함 상태를 적극적으로 못박고 있던 것**
(§ "여기에 더해 … 5건 — [H1] [H8] [L3] [M11] [H10]") 이었다.  그래서 이번엔 핀을 추가한 뒤
**일부러 수정을 되돌려 핀이 실제로 FAIL 하는지** 확인했다.  7건 전부 잡혔다:

| 뮤테이션 | 잡은 핀 |
|---|---|
| `_gb` 분할 되돌리기 (H5) | `★[H5] merge+film: 증발 0` — `214.65 + 120.45 vs 429.30` FAIL |
| `G_MECH_BUILTIN` → 1.05 (H8) | `★[H8] CT 규약 = 설계문서 §6.3 mono 1.02` FAIL |
| 배너를 리터럴 NONE 으로 (H2) | `★[H2] 거짓말하지 않는다` + `meta 와 문자 일치` 2건 FAIL |
| 삼항에서 `i0_t_scaled` 제거 (H9) | `★[H9]` 3건 FAIL |
| 킷을 `--allow-grid-t-mismatch --i0-temp-scale` 로 (H4) | `★[H4] 쌍 0개/호출 1개` 등 3건 FAIL |
| `transfer_assumption` 거짓 문장 복원 (H3) | `★[H3]` 3건 FAIL |
| help 를 정정 전 물리로 (H7) | `test_cli_help` 내용검사 5건 FAIL |

### ★ 리뷰가 못 본 것 — [H4] 수정 자체가 반쪽이었다 (자체검증에서 발견)

[H4] 권고대로 킷에 `--i0-temp-scale` 을 주입했더니 **새 거짓 진술**이 생겼다.
`--i0-temp-scale` 은 `--temp-k` 를 읽어 배수를 만드는데 킷은 `--temp-k` 를 굽지 않으므로
(옛 부호역전 규약) 실제 배수는 **정확히 1.0** 인 반면, 배너·provenance 는 ×6.2545 를 광고하고
npz 에는 `kinetics_T_scaling=I0_ARRHENIUS_kim2025` 가 찍혔다.

⇒ **두 플래그는 한 쌍이다**:

| 준 것 | 결과 | 가드 |
|---|---|---|
| `--temp-k T` + `--i0-temp-scale` | ✅ 부호 정상, i0 ×6.25 @60 °C | 통과 (해제 플래그 불필요) |
| `--temp-k T` 만 | ⛔ 부호 역전 (§3-3①) | `KINETICS_UNSCALED` 차단 |
| `--i0-temp-scale` 만 | ⛔ 배수 1.0 인데 `I0_ARRHENIUS` 로 찍힘 = 거짓 라벨 | 그리드가 다른 T 면 hard-block + `--temp-k` 안내 |

킷은 이제 쌍으로 굽고 `--allow-grid-t-mismatch` 는 **뺐다** (σ_ion·kinetics 가 같은 T 라 혼합이
아니고, 남겨두면 STEP3 가 `--temp-c` 를 못 구운 **진짜** 불일치까지 조용히 통과한다).
회귀 핀은 **인자 줄에서만** 센다 — 주석·echo 의 설명 산문은 제외해, 설명을 늘려도 카운트가
깨지지 않고 반대로 산문만 고쳐 GREEN 을 살 수도 없다.

### 부수 발견 (리뷰 목록 밖)

`--i0-temp-scale` help 에 넣은 `10.5%` 의 리터럴 `%` 가 argparse `_expand_help` 를 깨뜨려
`step4_dyn.py --help` 가 죽었다.  `test_cli_help.py` 가 잡았다 (121 스크립트 크래시 검사 — 그
테스트가 원래 하던 일).  같은 파일에 이번에 **내용** 검사를 더했다 ([H7]).

### 남은 것 (앵커 대기 — 코드 결함 아님)

- `D_s(T)` · `OCP dU/dT` · `κ(T)` · SE 경도 `H(T)/σ_y(T)` · **분해율 Eₐ** = §F1 앵커 0건.
  ⇒ 온도를 켜도 상태는 `PARTIAL_sigma_ion+i0` 다 — 전-물리 온도 스윕이 **아니다**.
- 코팅계 Eₐ: kim2025 LNO 가 비-Arrhenius 라 uncoated 앵커를 **상속**한다는 사실만 라벨했다.
  코팅 프리셋 전용 Eₐ 는 데이터 대기.
- `--c-rate` Σt 인덱싱은 켤 수 있게 했으나 **기본 OFF** (기존 √N bitwise 불변).  기본을 바꾸는
  것은 코퍼스 재해석을 동반하므로 별도 결정.
