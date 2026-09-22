# Phase A (6 mAh VGCF 조성 순서) — 판정 **ORDER-ROBUST** 의 정본 산출물 (2026-09-21, 104 팔)

> 인계 검증 `docs/handoff_review_20260922.md` §C-2 로 커밋 (2026-09-22).  uma 의 `~/runyourai/1/pa/` 에서
> 저자가 `pa104_20260921.tgz`(224 파일, 26 KB)로 옮겼고, **파일은 한 바이트도 고치지 않았다**.
> 사전등록 `docs/reviews/phase_a_6mah_order_prereg_20260907.md` · 판정기 `scripts/phase_a_order_verdict.py`.

## 판정 (커밋본 위에서 재실행 = uma 결과와 **같은 답**, 2026-09-22)

```
python3 scripts/phase_a_order_verdict.py --dir docs/data/phase_a_104arms_20260921/verdict_dir_20260921 --out /tmp/v.json
팔 104 (primary 96 · secondary 0 · QC 8) · δ_num = 0.04 % (상수)
판정 ORDER-ROBUST · 비교 72 쌍 · 위반 0 건
최악 팔: vox 0.25 · origin 1 · 3.0→4.0 wt% → +103.6390 %
(기술 보고 전용) 증분 최소 +103.6390 % · 최대 +775.0421 %
replay 최악 2.2e-14 % (통과)
```
`verdict_20260921.json` sha256 `a88a245a2d4ccc945bcc5475f34ff3a48a9097a66401af7cb699cd7e6f434ecc`.

★ **한정어 셋을 떼지 말 것** (prereg §0·§2, 판정기 자신이 출력에 박는다):
(i) 등록된 estimand 는 **순서**뿐 — 참 σ_e · 격자 수렴 · 하한 서술은 답하지 않는다 (CL-72).
(ii) 증분 %(+103.6 ~ +775.0)는 **기술 보고 전용** — 게이트가 아니고 크기 주장이 아니다.
(iii) QC exact replay 는 **VGCF 1 wt% · vox 0.15 · origin 8 한 셀**의 음성대조다 — 12 셀 전부의 증명이 아니다.

## 구조 (uma 의 배치를 그대로 옮김)

| 경로 | 무엇 | 봉인 축 (영수증) | `code_sha` |
|---|---|---|---|
| `verdict_dir_20260921/` | **판정기에 넣은 104 팔** = 아래 세 primary 배치의 `arms/` 96 + QC 8 — sha256 **전수 일치** 확인 | — | primary null · qc `7d24439f6` |
| `arms_primary_v015_20260921/` · `_v020_` · `_v025_` | 재실행 96 팔의 어댑터 산출 (`arms/` 32 × 3 · `_adapter_summary.json` · `run_receipt.json`) | `ptfe_stamp centerline` · `fibre_stamp segment` · `bridge_um 0.24` · `sigma_ptfe 0` · `sigma_vgcf 78.5398` | **null** (PASL-03 — 09-18 실행 셸의 git 파손; 물리축은 `.sh` 의 `--expect-physics` 선언 + 배치당 로그 대조 32/32/31 로 확인) |
| `arms_20260921/` | QC 8 팔 어댑터 산출 (`role: qc` → 파일명 `arm_qc_*`, 판정기 스키마 `qc_replay`) | 같음 | `7d24439f6` (`code_sha_status: SEALED`) |
| `phaseA_rerun_v015_20260918/` · `_v020_` · `_v025_` | 재실행 배치의 **영수증** (`derived_from: sh`, `phase_a_receipt_from_sh.py`) | 같음 | null |
| `phaseA_rerun_qc_20260921/` | QC 배치의 영수증 | 같음 | `7d24439f6` |
| `phaseA_h015_20260914/` · `_h020_` · `_h025_` | ⛔ **봉인 이탈 배치(09-14 체인)의 영수증** — `ptfe_stamp: off` · `code_sha` null (`PASL-01/02`).  **판정에 쓰이지 않았다.**  출처 기록으로만 둔다 | `ptfe_stamp off` | null |

⚠ 09-14 체인의 **팔 JSON 은 여기 없다** (그 배치는 재실행됐고, 옛 h015 32 팔은 `docs/data/phase_a_h015_arms/` 에
다른 세대(`70b9e37a`)로 따로 있다 — 그 README 대로 현행과 나란히 쓰지 말 것).

## 왜 `code_sha` null 이 판정을 막지 않았나 (그리고 무엇이 남나)

- 96 primary 는 09-18 코드(+옛 cupy)로, QC 8 은 09-21 코드 `7d24439f6`(+재설치 cupy)로 돌았다.  QC 는 primary 쌍둥이와
  **출력 경로만 다르다** (exact replay 의 정의, prereg §3).  둘의 σ_e 가 **2.2e-14 %** 안에서 같다 ⇒ 코드 동일성을
  sha 로 증명하지 못한 자리를 **재현으로** 메웠다 (`PASL-03` 의 경험적 폐쇄).
- 남는 것: 그 재현은 (iii) 대로 **한 셀**이다.  다른 11 셀의 primary 값은 sha 없이 로그 대조로만 묶여 있다.
- 원고에는 *"조성 순서가 격자(0.25·0.20·0.15)·origin(8) 교란에 강건하다"* 까지만.  σ_e 절대값·이득 크기는 `CL-41`/`CL-72`
  (격자 미수렴 · 외삽 불가)에 그대로 걸린다.

## 실측 σ_e (vox 0.15, 8 origin 범위, S/cm — 기술 보고, 크기 주장 아님)

VGCF 1 → 0.00209962 … 0.00214454 · 2 → 0.0150688 … 0.0155461 · 3 → 0.0589938 … 0.0599249 · 4 → 0.130443 … 0.131529.
(VGCF 3 wt% ≈ 59 mS/cm 는 `CL-49` 의 SBE 54.6 mS/cm 와 같은 자릿수 — 다른 캠페인·다른 침대의 독립 교차확인.)
