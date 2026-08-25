# 다음에 할 일 (2026-08-25, R4 대응 직후)

정본은 `codex_absorb_verdict_20260825.md` 와 `findings.json` 이다.  이 파일은 **순서**만 정한다.

---

## A. 흡수 전 (코드 규율) — R4 잔여 5건 + 배터리 3건

★★ **A 트랙 현황 (2026-08-25 마감)**: A0 ✅ · A1 ✅ · A2 ✅ · A3 🔶(범주 오선택만 잔여) ·
A4 ⬜ · A5 ✅ · A6 ✅.  **배터리 41 돌연변이 전부 계약 만족** (기대 밖 실패 0 · harness 사고 0),
`bash scripts/check_all.sh` 전부 통과.  ⇒ **다음은 5차 Codex 리뷰**를 받고 그 다음이 B 다
(A4 는 리뷰 뒤로 미뤄도 된다 — harness 정확도 개선이지 봉인이 아니다).

### A0. 배터리 잔여 3건 — ✅ **닫힘** (2026-08-25)
셋 다 **기대집합 정정이 아니라 실제 결함**이었다:
· harness 의 crash 판정이 `'SystemExit' not in traceback` 이었는데 selftest 는 전부
  `raise SystemExit(_selftest())` 로 끝난다 ⇒ **모든 crash 가 정상 실패로 접혔다**
  (`KeyError: 'ionic'` 이 `★놓침★` 으로 보고됐다).  마지막 예외 줄을 보게 고쳤다.
· `plan_ok` 가 키 부재에서 죽었다 (`_miss` 를 우회하면) → `.get` 으로 굳혔다.
· mutant 두 개가 **불충실**했다 (`c.get(comp) or …` 는 dict 가 있으면 폴백하지 않는다).
· `조건7` 의 `L-11` 기대는 **내가 잘못 적은 것**이었다 — L-11 은 `P2_EXTRA` 검사이고
  `k_live_invocation` 과 무관하다.  배터리가 그것을 잡았다.

### A1. solver-affecting CLI **전수 생성** — ✅ **닫힘** (규칙 M, 2026-08-25)
★★ 초판이 **가짜 초록**을 냈고 그것이 이 항목의 본체였다 (원장 SELF-02):
· ⓐ payload 파일만 AST 로 훑어, `se_material.temperature_argparse(ap)` 가 **다른 모듈**
  에서 등록하는 `--temp-c`·`--ea-ion-ev` 를 못 봤다 (오히려 `--temp-c` 를 "파서에 없다"
  로 **거꾸로** 보고).
· ⓑ 이름 조각(`CLI_PHYSICS_HINT`)으로 후보를 걸러 `--dilate-z`·`--k-carbon`·
  `--i0-a-m2`·`--joule-heat` 는 후보조차 아니었다.
⇒ **부분집합 필터를 전부 버렸다**.  파서를 **실행해서**(`parse_args` 가로채기) 잡고,
  `--help` 를 뺀 **전 79 옵션**이 등재를 요구한다.  범주 9종(`protocol`/`derived`/`plan`/
  `numeric`/`solve`/`input`/`report`/`mode`/`record`) + 규약 축 **24 전수 도달** 검사.
★ 그 과정에서 실제 구멍 두 개가 나왔다 (원장 SELF-03):
  `--dilate-z` 가 침대를 z 로 늘려 rasterize 로 들어가는데 규약 축이 없었고
  (`input_digest` 는 파일 **내용**만 덮는다), `--se` 를 **빠뜨리기만 해도** SE 점구름이
  합성(proxy)으로 내려앉는데 그것도 기록되지 않았다.  ⇒ `dilate_z`·`se_source` 신설.
· 회귀 M-1~M-11 · 배터리 mutant 4종.

### A2. cross-dir raw diff-set == `expect_differ` — ✅ **닫힘** (2026-08-25)
레지스트리(`FIELD_CONTRACT`)만 보던 것을 **매니페스트 전수 훑기**로 바꿨다.
· 분류 안 된 키는 **값이 같아도** HOLD (`MANIFEST_RESULT_KEYS` · `MANIFEST_DERIVED_OF` ·
  `FIELD_CONTRACT` 셋 중 하나로 분류해야 한다) — "지금은 우연히 같다" 는 계약이 아니다.
· 등록 밖 축이 두 디렉터리에서 다르면 HOLD (이름을 댄다).
★ 즉시 적발 (원장 SELF-04): **규약 축 7개가 레지스트리 밖**이었다 —
  `periodic_xy`·`plate_rule`(R4 부터) · `sigma_superp_S_cm`·`sigma_swcnt_S_cm`·
  `swcnt_ion_block`·`dilate_z`·`se_source`(A1 부터).  해시에는 들어가는데 cross-dir
  고정 검사는 **안 지났다**.
⇒ 3겹으로 닫았다: ⓐ 일곱 등재 ⓑ **리더가 레지스트리 축을 자동으로 담는다** (손으로
  고르면 또 갈라진다 — H5·CDX-IJ-01 부류) ⓒ 구조 불변식 ㊹a `PROTOCOL_FIELDS ⊆
  FIELD_CONTRACT`.  회귀 ㊹a~d · 배터리 mutant 5종.

### A3. 선언 뒤집기 pass-mutant 봉인 (R4-CX-05 잔여) — 🔶 대부분 닫힘
· `across_dir`·`generation`·`required` 는 ㊷ 가 **레지스트리를 읽어 거동을 생성**하므로
  축을 추가하면 시험이 따라 붙는다.
· ㊹a 가 `PROTOCOL_FIELDS ⊆ FIELD_CONTRACT` 를 **구조 불변식**으로 세워 선언 누락을 닫았다.
· ㊹f 가 `계약 ∩ 면제 = ∅` 을 세워 "계약된 축을 면제 목록으로 옮기는" 우회를 닫았다.
· 배터리 mutant `A3 periodic_xy.across_dir 뒤집기` = **선언만 바꾸는** 돌연변이가 실제로
  물린다 (매니페스트 전수 훑기가 잡는다).
· **잔여**: 회계 **범주 오선택**(physics 를 `numeric`/`mode` 로 선언)은 아직 못 잡는다 —
  그것은 사람이 쓴 주장이고 코드로 반증할 방법을 아직 못 찾았다.

### A4. selftest 를 구조화 결과로 (R4-CX-06 잔여)
지금 harness 는 stdout 문자열을 읽는다.  `--selftest-json` 을 붙여 exact ID·rc·
timeout 을 기계로 읽게 하고, 배터리가 **failed-ID multiset** 을 비교한다.

### A5. standalone full bundle (R4-CX-08 잔여) — ✅ `scripts/make_review_bundle.sh`
`git bundle create --all` + **받는 쪽 검증까지 그 자리에서 한다** (빈 디렉터리에 clone 해
`HEAD`·커밋 수를 찍는다).  지난 실패는 만들 때가 아니라 **열 때** 드러났으므로, 만드는
쪽에서 여는 것까지 확인하지 않으면 같은 일이 반복된다.  더러운 작업 트리는 거부한다.

### A6. (A1 이 파생시킨 것) 합성 SE 침대 게이트 — ✅
`--se` 를 **빠뜨리기만 해도** SE 점구름이 proxy 로 합성되고 그것이 rasterize 로 들어간다.
`input_digest` 는 읽은 파일이 없어 그것을 **못 덮는다**.
⇒ producer 가 `se_source` 를 적고(`proxy:<frac>@<n_vox>` / `npy`), **판정기가 막는다**
  (`hold_code='SE_PROXY'`).  생산 경로는 안 막는다 — 만드는 것은 자유고 **그것으로 σ 를
  주장하는 것**만 막는다.  회귀 ㊹g(차단)·㊹h(정상 증인).
⚠ **C 를 돌릴 때 확인할 것**: 킷 `run_mpm.sh` 의 payload 호출이 `--se` 를 정말 넘기는지.
  넘기지 않으면 지금까지의 모든 런이 합성 침대였다는 뜻이고, `se_source` 기록이 그것을
  처음으로 말해 준다 (이 리포에는 킷이 없어 여기서 확인할 수 없다).

---

## B. 그 다음 — CPU census (GPU 아님)

R4 §7-10 이 정한 순서: **위를 닫은 한 clean SHA 에서** CPU raster-only 로
`bed × origin × side × phase` 접촉 census 를 먼저 낸다.

· 지금 있는 것은 **합성 침대** census 뿐이다 (bottom −28.7 % · top −32.8 %) —
  실침대 σ 감소율이 아니고 인용 불가.
· 이것이 GPU 를 돌리기 전에 p1→p2 가 무엇을 바꿨는지 **싸게** 아는 유일한 방법이다.
· 실침대가 필요하다 (`kit_SBE` / `kit_DBE`).  GPU 없이 CPU rasterize 로 가능.
⚠⚠ **이 컨테이너에서는 못 한다** (2026-08-25 확인) — 리포에 있는 scaffold 는 `real14` 와
  `heckel_sweep_scaffolds` 뿐이고 `kit_SBE`/`kit_DBE` 침대·`se_dump.npy` 는 **kgy 에 있다**.
  ⇒ B 는 **사용자 기계에서** 돌려야 한다.  A 트랙(코드 규율)은 여기서 닫을 수 있고 닫았다.

---

## C. 그 다음 — GPU 8팔 재실행

R4 조건 전부:
· 같은 8 origins 의 SBE/DBE **둘 다** (한쪽만 새로 돌려 옛 값과 섞지 않는다)
· 하나의 새 protocol schema (`p2-`) · **하나의 clean code SHA**
· raw manifest 재계산을 통과한 receipt
· input digest + required component/backend/convergence seal
· bed × origin × side × phase 별 p1→p2 접촉 수 · Σg_plate · plate-energy 몫 census

⚠ 옛 팔(`p1-`)과 새 팔(`p2-`)은 섞이지 않는다 — 이제 규약 해시가 **기계로 집행**한다.

---

## D. 병렬로 — 물성 앵커 (사용자 회신 대기)

· **`σ_SDCP = 250`** 출처: cast film 인가 pressed pellet 인가.  절대값·실험 앵커 주장
  전에 닫아야 한다.  지금은 scenario/assumption 으로만 라벨.
· **`ρ_SDCP`**: 코드 주석이 PROXY 라고 적고 원고 값을 요구한다.

---

## E. 원고 (이 트랙이 원래 목적)

⚠ **C 가 끝나기 전에는 σ_e 절대값·비를 원고에 쓸 수 없다.**  지금 쓸 수 있는 것:
· 기전 서술 (SDCP 표현 부피 · 격자 의존) — CL-25/33/34/41 하향판
· 방법 (STEP1~4 파이프라인 · 규약 정체성 · 계약 검사)
· 격자 미수렴을 **결과로** 적기 (세 값 나란히 + "외삽 불가")
쓸 수 없는 것: 새 σ_e 절대값 · SBE/DBE 비 · p1 시절 값(CL-33/41/58) 전부.
