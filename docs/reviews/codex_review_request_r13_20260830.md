# Codex 적대 리뷰 요청 R13 — 이온 전도도 트랙 (2026-08-30)

브랜치 `manuscript-track`.  HEAD 에 오늘 커밋 5건이 있다.
**목적: 아래 주장들을 무너뜨려 달라.  "확인했다" 가 아니라 반례를 원한다.**

---

## 0. 이 실험이 재려는 것

원고 표의 **σ_ion 행이 비어 있다.**  원장(`docs/reviews/table_s3_data_20260827.md` §6-1)이
이유를 이렇게 적는다 — *"미측정이 아니라 **쟀는데 못 쓴다**"*.  입력 규약이 두 침대를
**비대칭**으로 만들어서다:

| | SBE | DBE |
|---|---|---|
| PTFE (이온 차단재) | **1.0 wt%** | 0.5 wt% |
| 격자에 표현되나 | ❌ (`ptfe_stamp=off`) | ❌ |
| SDCP | 없음 | 있음, `σ_ion = 0.001` 로 σ 를 깎음 |

⇒ SBE 의 약점(바인더 2배)은 **격자에 없고**, DBE 의 첨가물만 불이익을 받는다.

원고 자신의 **Figure 2f** 가 앵커를 갖고 있다 (§12): LPSCl 3.57 → +SDCP 2.86 (**×0.80**)
→ +PTFE 0.97 (**×0.27**).  즉 **SDCP 는 "이온 전도체" 가 아니라 "PTFE 보다 훨씬 덜 막는
것"** 이다.

**두 갈래로 푼다** — ①② 런 = **방향**(PTFE 를 격자에 넣고 부호를 본다) · D13 = **크기**
(σ_ion(SDCP) 재앵커).

---

## 1. 오늘 바꾼 것 — 각각 무엇을 막으려 했나

| # | 커밋 | 무엇 |
|---|---|---|
| 1 | `ea9d3b55` | B 트랙 펠릿 캘리브 **발굴** + §12 SDCP 행 **부호 정정** + 새 §14 |
| 2 | `a8b9196e` | OAT 씨앗 반복 사전등록 — 문서가 *"등록했다"* 고 적은 **파일이 없었다** |
| 3 | `a5cace9d` | **LEAN=4 신설** (필드 ON + 이온 ON + pore OFF) + LEAN 값 검증 |
| 4 | (미커밋) | 코드리뷰 4건 수정 — 아래 §2 |

### 1-1. LEAN=4 를 왜 만들었나

`--no-pore` 없이 돌면 `run_contract.required_components()` 가 `pore` 를 **required** 로 놓고,
이 침대는 pore-τ 가 `None` 을 내서 `STEP3_EVIDENCE` 로 **payload 전체가 게시 거부**된다
(2026-08-27 kit_SBE 실측: `EVID|pore|result| tau=None` → `mpm_payload.json.failed`).
그런데 **기존 LEAN 1·2·3 이 전부 `--no-field` 를 붙인다** ⇒ *"필드는 남기고 pore 는 끄는"*
조합이 **원리적으로 없었다**.  `P2_EXTRA="--no-pore"` 도 허용목록(수치 전용)이 거부한다.

**실측으로 확인됨**: 그 조합 없이 돌린 진단 런이 2시간 7분 만에 RAM 가드에 죽었다
(18:21:44, `available 4 GB < 5`).  pore·STEP4·집전체가 전부 켜져 있었다.

---

## 2. 공격 요청 — 이 주장들을 무너뜨려 달라

### C-1. *"σ_ion(SDCP) 값을 바꿔도 σ_e 는 비트 단위로 불변이다"*
근거로 든 것: 두 σ 표가 별개 순수함수(`step3_sigma.py:81,100`) · 생산 호출부가 갈려 있음
(`mpm_webapp_payload.py:1644` vs `:2008`) · `solve_sigma_z` 가 `sid` 를 안 바꿈 · 모듈 캐시 없음.
**찾아 달라**: 두 솔브가 공유하는 상태.  `sid3` in-place 수정 · dof 마스크 재사용 ·
전역/모듈 캐시 · numpy view aliasing · `a.*` 부작용.
⚠ `--step3-ptfe-block-um` 은 **내가 이미 인정한** 유일한 교차 노브다 (sid 9 가 양쪽 0) — 그건 빼고.

### C-2. *"LEAN=4 = 이온 ON + 필드 ON + pore OFF 이고, `_lean4` 산출물은 lean3 과 안 섞인다"*
**찾아 달라**: `LEAN=4` 인데 필드가 안 써지는 경로 · `_lean4` 팔이 lean3 요청에 SKIP 되는 경로 ·
`OUTDIR=` 명시로 영수증 diff 가드(`:367`)를 우회하는 법.

### C-3. *"`field_written` 은 digest 를 안 바꾸고 기존 팔에 거짓 경보가 0 이다"*
`RECEIPT_AXES_NODIGEST` 를 신설해 `receipt_digest` 밖 + `receipt_match` 안에 뒀다.
**찾아 달라**: digest 가 바뀌는 설정 · **LEAN≠4 인데** 기존 팔이 거부되는 경우 ·
`field_written` 을 선언했는데 검사를 안 지나는 경로.
⚠ 내가 인정하는 구멍: **LEAN 미지정 팔은 여전히 매니페스트로 필드 유무를 증명 못 한다**
(선언하면 오늘 이전 팔이 전부 HOLD 가 돼서 안 했다).  더 나은 설계가 있으면 말해 달라.

### C-4. *"이온 `reason` 가드가 조기반환을 전부 잡는다"*
`no_plate_contact` 가 `n_dof = cond.sum()` **양수** + `sigma_eff = 0.0` + `unconverged=False`
+ `cg_info=0` 을 돌려줘서 옛 판이 **σ_ion=0 을 `complete` 로** 찍었다 (`step3_sigma.py:706`).
**찾아 달라**: `reason` 없이 0/무의미한 σ_ion 이 `complete` 로 나가는 다른 경로.
`degenerate_thin_bed`·`no_conductive_voxels`·`all_floating_dropped` 각각의 n_dof 도 봐 달라.
그리고 센티널 `_ion_reason_marked` 가 **안 정의되는 경로**가 있는지 (NameError).

### C-5. *"`--ptfe-stamp centerline` 가드가 fail-closed 다"*
`--step3-fibre-stamp` **기본값이 `point`** 라 기본 설정으로 도달하는 fail-open 이었다.
**찾아 달라**: 가드를 지나치는 조합 · `_afid` 가 `segment` 인데도 None 이 되는 경로
(`_m.any()` 가 False 면 그렇다 — 이때 매니페스트 `fibre_stamp` 는 뭐라고 적히나?).

### C-6. *"1팔로 이온 **부호**를 판정해도 된다"* (`ion_ptfe_sign_prereg_20260830.md`)
근거: `off` cohort 팔-간 산포 0.99264–0.99292 (**±0.014 %**), 부호가 뒤집히려면 0.7 % 필요 = 50배.
**공격해 달라**: 그 산포가 **PTFE 를 안 찍은** 규약에서 잰 것인데, 찍은 규약에서도 같다는
보장이 있나?  PTFE 셀이 이온망을 끊으면 origin 위상 민감도가 **커질** 수 있지 않나?
h0 문턱 `≤ 0.9928` 의 유도도 봐 달라.

### C-7. §13 격리 논증 · §14 펠릿 캘리브 발굴
§13 = *"이온 결함이 σ_e 를 오염시키지 않는다"* (C-1 의 문서판).
§14 = 5일 전 펠릿 캘리브를 오늘 발굴 — `σ_ion(SDCP)* = 0.62e-3` (확인 런 2.8655 mS/cm, 표적
2.86, +0.19 %, 4/4 시드).  **동결 문서가 "상수로 이식 금지" 라고 못 박았고 나는 그것을 지켰다.**
**공격해 달라**: 내가 §12 에서 냈던 부호 오류(복합 펠릿 비 ×0.80 과 상 σ 비 ×0.33 을 같은
열에 놓은 것)가 **다른 곳에도** 남아 있는지.  §14 의 이식 금지가 D13 설계와 모순되지 않는지.

---

## 3. 내가 이미 아는 것 — 여기 시간 쓰지 말아 달라

- `code_sha` 가 digest 에 있어 **커밋마다 OUTDIR 이 갈린다** (지적 1의 실현 조건이 좁은 이유)
- 지적 5 미수정: `mixed_ionic_verdict` 가 `a.no_ion` 을 못 받아 `--temp-c X --no-ion` 이 hard-exit
- OAT: **판정이 아니라 측정** (문턱 미등록·씨앗 반복 미실행).  `oat_seed_prereg_20260830.md` 로 등록만 됨
- 펠릿 캘리브 원자료 JSON 이 kgy 로컬에만 있다 (`PROVISIONAL_RAW_JSON_PENDING`)
- 패널 번호 `Fig 2f` ↔ `Figure 2h` 불일치 미해소
- `quotation_ban` 값들은 `docs/reviews/claims.json` 이 정본

---

## 4. 원하는 형식

주장 번호(C-1…C-7)마다 **CONFIRMED / REFUTED / 반례** 로.  반례는 **파일:행 + 재현 명령**으로.
새로 찾은 결함은 심각도(P1/P2/P3)와 **어느 결론이 무너지는가**를 같이.
