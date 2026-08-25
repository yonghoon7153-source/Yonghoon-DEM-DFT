# 흡수 지도 — `claude/stoic-knuth-NObVQ` 2026-08-25 변경분

> 목적: `claude/sdcp-dem-manuscript-si-pqwtv8` (미완, 사용자가 zip + Codex 계획서와 함께 전달 예정)
> 를 흡수할 때 **무엇이 충돌하고 무엇이 고유한지** 미리 갈라 두는 지도.
> ⚠ 이 문서는 stoic 쪽 변경만 적는다 — 상대 브랜치 내용은 **아직 안 읽었다**.
> 사용자 지시 (2026-08-25): *"너가 나중에 흡수할건데 아직 안닫힌 부분이 있어서 잠시만 기다려줘"*
> ⇒ 그 브랜치는 **건드리지 않는다**.

## ⚠ 겹치는 파일 (상대 브랜치도 크게 고쳤다 — kgy pull 실측)

| 파일 | 상대 브랜치 | stoic (오늘) |
|---|---|---|
| `scripts/sdcp_gain_verdict.py` | **+1082줄** | 아래 §1 |
| `scripts/check_method_discipline.py` | +723 | 변경 없음 (어제까지분만) |
| `scripts/step3_sigma.py` | +415 | 변경 없음 |
| `scripts/mpm_webapp_payload.py` | +259 | 변경 없음 (어제까지분만) |
| `scripts/sdcp_gain_vox015_8arm.sh` | +127 | 아래 §2 |
| `scripts/check_all.sh` | 수정 | **stoic 이 신설** (§3) |
| `.github/workflows/discipline.yml` | 수정 | **stoic 이 신설** (§3) |
| `docs/reviews/findings.json` | +276 | 아래 §4 |
| 신규(상대) | `run_contract.py` · `mutation_sweep_20260825.py` · `codex_absorb_verdict_20260825.md` · `docs/data/gate5_8arm_point_sg110447_20260824.md` | — |

## §1 `sdcp_gain_verdict.py` — stoic 이 오늘 넣은 것

1. **`_BED_FIELDS` 침대-정체성 분리** (FA-06).  `input_digest`·`additive_E_GPa` 를 **침대 안에서만**
   고정 검사.  침대 사이에는 대신 ⓐ digest 는 **달라야** 하고 ⓑ additive 는 **공통 키만** 같아야 한다.
   ★ 실사고: 이게 없어서 도핑 baseline 8팔이 `additive_E_GPa` 로 **오발화 HOLD** 를 맞았다
   (SBE `{PTFE,VGCF}` vs DBE `{PTFE,SDCP,VGCF}` = 실험의 독립변수를 결함으로 신고).
   음성 대조 ㉙a~d.
2. **`compare_dirs()` + `--compare-dir --expect-differ`** — 두 디렉터리를 빼는 실험의 최소 계약
   (origin 짝 · 짝별 digest 동일 · 등록 밖 인자 불변 · 등록 축이 **실제로** 다름).  음성 대조 ㉗a~e.
3. **`scan()` + `--scan`** — 결과 디렉터리를 **찾는다** (이름을 손으로 짓다 3번 틀렸고 3번 다
   "0 팔 → HOLD" 로 끝나 **없는 경로가 실패로 위장**했다).  섬유/SDCP 스탬프 두 열 다 표시. ㉘a~c.
4. **`--collect-only` 가 `--out` 을 쓴다** — 옛 판은 쓰기 **전에** exit 0 이라 파일 0개.
   kgy 백업 18건이 그렇게 **안 떠졌는데 ✓ 18번**이 찍혔다. ㉘d (서브프로세스로 파일 실재 확인).
5. ㉖ 블록 전제 수정 — 어제 판이 "두 침대 digest 가 **다르면** HOLD" 를 기대했다 = **틀린 전제를
   테스트로 박제**했다.  올바른 계약은 "침대 안에서 같고, 침대 사이에서 다르다".
6. `_FIXED_FIELDS`·`_canon`·`phys_bounds`·`_oob` (물리 경계, `structure_predictor.BOUNDS` 를 **가져다 씀**).

⇒ **흡수 시 주의**: 1·4·5 는 **결함 수정**이라 상대 브랜치에 같은 구멍이 있으면 그쪽도 고쳐야 한다.
2·3 은 기능 추가라 이름 충돌만 보면 된다.

## §2 `sdcp_gain_vox015_8arm.sh`

**`FIBRE_STAMP={point,segment}` 정식 축** (기본 segment = 기존 동작).  옛 판은 `segment` 를
**세 군데 하드코딩**(SKIP 검사 · 그 진단 · payload 주입)해서 `P2_EXTRA="--step3-fibre-stamp point"`
같은 우회가 **조용히 무력**했다 (OUTDIR 태그가 안 갈려 기존 선분 팔을 "완전"으로 SKIP → 아무것도
안 돌고 끝남).  태그 `_fspt` 로 디렉터리가 갈린다.
⚠ 상대 브랜치에 `gate5_8arm_point_sg110447_20260824.md` 가 있으니 **거기도 점 스탬프 팔을
돌렸을 가능성**이 크다 — 두 구현이 다른 방식이면 **어느 디렉터리가 어느 규약인지**부터 맞출 것.

## §3 stoic 고유 (상대에 없을 가능성)

- `.github/workflows/discipline.yml` — 검사기 4종 CI (⚠ 상대도 이 파일을 고쳤다 = **충돌 확실**)
- `scripts/check_all.sh` — 커밋 전 일괄 검사 (⚠ 상대도 고쳤다)
- `scripts/run_dem_webapp.sh` · `scripts/restore_webapp_data.py` — 웹앱 런처/복구 (윈도우 재설치 대응)
- `scripts/ml_shap_pareto.py` + 웹앱 `/predictor/structure/{shap,pareto}` + 예측기 패널
  (양수영 세미나 방법 이식 · `DOMAINS` 레지스트리로 DEM↔DFT 분리)
- `check_review_findings.py` zip/pptx 리더 + 덱 배너 슬라이드

## §4 원장 (`claims.json` · `findings.json`)

stoic 이 오늘 확정/신설한 것 — **흡수 시 이 판정들이 살아남아야 한다**:

| ID | 상태 | 핵심 |
|---|---|---|
| **CL-40** | live · `BOTH_REJECTED` | VGCF 전기적 사망, 비 **4.8956** (G +3.8956).  두 가설이 각각 반쪽만 맞다 — SDCP 는 혼자 전도하지만(4.9배) 그 독립 경로가 정상 이득의 **2.96 %** 뿐 |
| **CL-41** | live | 세 점 완주 (0.15/0.125/0.115 → 1.123191/1.143817/1.155448).  **멱법칙 불성립** (증분비 1.773 < 이론 최소 2.187) ⇒ Richardson 무의미, 보고값은 전부 **하한** |
| **CL-45** | live · `BOTH_REJECTED` | σ-치환 감소율 **30.38 %** (vox 0.4).  비례계수 0.912(0.15) → 0.763(0.4) = 수확체감.  CL-43 의 동행은 **인과 아님** |
| **CL-58** | live · measurement_record | 도핑 baseline — σ_e **1.123214** · σ_ion **0.992720** (8팔, 3게이트 통과).  **전자 +12.3 % / 이온 −0.73 %** |
| FA-06 · CDXIJ-9/12 | claimed_fixed | 침대필드 오발화 · pptx 스윕 · CI |

⚠ `findings.json` 은 상대가 **+276줄** 고쳤다 — **ID 충돌** 확인 필수 (양쪽이 같은 번호를 새로
썼을 수 있다).  `check_review_findings.py` 가 중복 ID 를 잡으므로 합친 뒤 **반드시 돌릴 것**.

## §5 흡수 순서 (제안)

1. 상대 브랜치의 `codex_absorb_verdict_20260825.md` 를 **먼저 읽는다** (그쪽 판정이 정본일 수 있다)
2. `findings.json`·`claims.json` **ID 충돌** 먼저 — `check_review_findings.py` 로
3. 결함 수정(§1 의 1·4·5)이 상대에도 필요한지 대조
4. 기능 추가(§1 의 2·3, §2, §3)는 이름 충돌만
5. 합친 뒤 `bash scripts/check_all.sh` + CI 초록 확인

## §6 대기 중 (사용자 액션)

- kgy `docs/data/sdcp_runs/*.json` 18건 — `--collect-only` 빼고 재실행 후 커밋 (아직 `_scan.txt` 만)
- kgy git 인증 (PAT) 미설정
- 게이트 ⑤ factorial 판정 — `sg100_fspt`·`sg110447_fspt` 가 `--scan` 에 보였으니 4조합이 찼을 수 있다
