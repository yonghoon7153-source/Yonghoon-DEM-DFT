# Phase A 96팔 봉인 이탈 — 진단 기록 (2026-09-18)

> 사전등록 = `docs/reviews/phase_a_6mah_order_prereg_20260907.md`
> 발견 경로: 판정 직전 `scripts/phase_a_arms_from_payload.py` 가 **거부**했다.

## 결론 한 줄

**96팔이 `ptfe_stamp=off` 로 돌았다.  사전등록 §5 봉인은 `centerline ∧ sigma_ptfe=0`
(exact-zero DOF) 다.**  MPM 침대는 무사하고, 재실행 범위는 **STEP3 96 솔브뿐**이다.

## 1. 확정된 이탈 3건

| 축 | 봉인 (§5) | 실제 | 증거 |
|---|---|---|---|
| `ptfe_stamp` | `centerline` | **`off`** | receipt · manifest · `ptfe_cells_observed = 0` |
| `--no-ion --no-pore` (LEAN=2, σ_e 전용) | 켜짐 | **안 켜짐** | `component_plan` 5개 전부 `true`, 6 성분 `complete` |
| `code_sha` (CL-75) | 봉인 | **`null`** | receipt · manifest 전 계층 |

`fibre_stamp = segment` · `bridge_um = 0.24` · `sigma_ptfe_S_cm = 0.0` · `mpm_seed 3` ·
`periodic_xy false` 는 **통과**했다.

## 2. ⭐ 직전 32팔은 제대로 돌았다 — 그래서 원인이 좁혀진다

`docs/data/phase_a_h015_arms/_adapter_summary.json`

```
seal = {'fibre_stamp': 'segment', 'ptfe_stamp': 'centerline', 'bridge_um': 0.24}
n_arms = 32 · receipt_code_sha = 70b9e37a
```

두 receipt 를 나란히 놓으면 **다른 것이 정확히 둘**이다:

| | 32팔 (2026-09-12 이전) | 96팔 (2026-09-14) |
|---|---|---|
| `ptfe_stamp` | `centerline` | **`off`** |
| `code_sha` | `70b9e37a` | **`null`** |
| `arms` `bridge_um` `expect_backend` `fibre_stamp` `periodic_xy` `sdcp_*` `vox_um` | — | **전부 동일** |

⇒ **코드 세대도 규약 이해도 바뀌지 않았다.**  실제로 생산 파이프라인 5개 파일
(`mpm_webapp_payload.py` · `voxel_conductivity.py` · `measure_provenance.py` ·
`mpm3d_compaction.py` · `run_contract.py`)은 박스 커밋 `be0ae9568` 과 HEAD 사이
**변경이 0** 이다.  바뀐 것은 **띄운 셸**이다.

## 3. 근본 원인 — 계약 검사기가 **선언 밖 축**을 못 본다

96팔 `.sh` 의 선언:

```
--expect-physics vox_um=0.15,bridge_um=0.24,sigma_vgcf_S_cm=78.5398,
                 fibre_stamp=segment,sdcp_stamp=point,sdcp_yield_to_vgcf=False,periodic_xy=False
```

`ptfe_stamp` 이 **없다**.  러너에는 *"선언과 실제가 다르면 중단"* 하는 검사기가 **있었는데**
봉인 축이 선언 목록 밖이라 검사 대상이 아니었다.

★ **선언 안 한 축은 검사도 안 된다.**  규율 ⑤(*"후보를 고르는 코드가 곧 사각지대"*)가
**계약 선언 층**에서 재현된 것이다.

그리고 `PTFE_STAMP` env 가 없으면 러너가 `${PTFE_STAMP:-off}` 로 receipt 에 `off` 를 적고
(`sdcp_gain_vox015_8arm.sh:409`), payload 도 `--ptfe-stamp` 미전달 + `sigma_ptfe=0` 이면
`resolve_ptfe_stamp('', 0.0) == ('off', True)` 로 **실제로 off 가 된다**.
⇒ receipt 는 거짓말하지 않았다.  선언이 비어 있었을 뿐이다.

## 4. 무너지지 않은 것

- **MPM 침대 5개** — 봉인 21축 × 5킷 **전수 일치**.  달라진 넷(`dilate_z` `nz`
  `thickness_um` `bulk_density`)은 조성이 달라서 **달라야 하는 것**이다.
  `add_rng_per_phase = True` 확인 ⇒ 조성 축이 morphology 교란과 갈라져 있다.
- **생산 코드 세대** — 위 §2.
- ⇒ 재실행 = **STEP3 96 솔브뿐**.  예산 46~63 h 에서 LEAN=2 로 절감
  (실측 앵커 vox 0.4: electronic 333 s vs 부수 성분 합 ≈ 111 s).

## 5. ✅ `code_sha = null` — 원인 확정 (2026-09-18 저녁, `PASL-05`)

**`git status --porcelain --untracked-files=no` 가 23.1 s 인데 `_code_sha` 의 `timeout` 이 20 이었다.**
세 git 호출이 한 `try` 안이라 `TimeoutExpired` → `except Exception: return None` 으로
**SHA 까지 같이 버려졌다**.  git 도 리포도 멀쩡했다 — `git -C <scripts> rev-parse --short HEAD`
는 0.4 s 로 `be0ae9568` 을 낸다.

★ 설계가 거꾸로였다: **SHA 가 본체**이고 dirty 는 한정어인데, 한정어를 못 재서 본체를 버렸다.
⇒ 수리: SHA 를 먼저 확정하고, dirty 판정이 실패하면 **`+dirty-unknown`** 으로 **드러낸다**.
  타임아웃 20 → 180.  `--selftest-provenance` 5/5 · 변이 시 3/5 FAIL.

⚠⚠ **같은 날 같은 패턴을 두 번 만났다** — `check_review_findings._commit_exists`(GAP3-41)도
`mpm_webapp_payload._code_sha`(PASL-05)도 **git 서브프로세스 타임아웃을 넓은 `except` 로 삼켜
조용히 실패**했다.  서로 다른 파일, 같은 결함.  ⇒ **느린 파일시스템이 봉인을 지운다.**
이 패턴을 가진 다른 자리를 훑어야 한다 (미착수).

⚠ **이 수리는 진행 중인 96팔 재실행에 적용하지 않는다.**  박스에 보내면 그 런이
`be0ae9568+dirty` 가 되고 CL-75 는 dirty 를 명시적으로 인용 금지한다.  ⇒ 박스는 그대로 두고
코드 세대를 **밖에서 봉인**한다: `be0ae9568` · 생산 파일 5개 HEAD 와 바이트 동일(§2).
수리는 **다음 캠페인**부터 적용된다.

## 5-1. ⚠ 아직 설명되지 않은 것

**`code_sha = null` 의 원인.**  `measure_provenance.py` 는 박스와 HEAD 가 바이트 동일이고,
박스에서 `git rev-parse HEAD` 는 **지금 정상 동작**한다 (`be0ae9568` 반환).  런 시점에만
실패한 이유를 모른다.  ⇒ 재실행 전 **한-팔 검사**로 확인한다.  거기서도 `null` 이면
96팔을 띄우지 않는다 — `code_dirty`/무-sha 산출물은 **인용 금지**다 (§5 · CL-75).

## 6. 조치

| | |
|---|---|
| `scripts/phase_a_rerun_from_sh.py` (신설) | 원본 `.sh` 에서 **등록된 이탈만** 고친다.  그 외 토큰이 움직이면 거부.  selftest 21/21 (음성대조 6) |
| 러너 게이트 (미착수) | `--expect-physics` 에 봉인 축이 없으면 **ABORT** — §3 의 재발 방지 |
| 어댑터 `code_sha` 이중 fail-open (미착수) | 전부 `None` 이면 "같다" 로 통과하고, receipt 가 비면 대조 자체를 건너뛴다 |

## 7. 이 진단에서 내가 낸 오류 (기록)

- CLAUDE.md 의 **2026-08-18 시점 한 줄**을 현재형으로 읽고 *"기존 생산 규약이 off 였다"* 고
  보고했다.  실물 전수(`centerline` 119 vs 대조군 `off` 17)와 원장 `CL-60`(*"본문 규약
  (centerline)"*)이 그 반대다.  ⇒ 규율 ④ 가 경고한 실패.  CLAUDE.md 에 정정 배너를 넣었다.
- `--step3-vox` 가 한 줄에 **두 번** 나오는데 `head -1` 로 앞만 보고 *"세 격자가 전부 0.4"*
  라고 오판했다 (argparse 는 뒤를 쓴다).
- 첫 추출 명령이 격자 접두사 없이 세 디렉터리를 한 폴더에 부어 **덮어쓰게** 만들었다.
- 셸 명령의 sha256 가드를 *"불일치 — 중단"* 이라 적고 **실제로는 안 멈추게** 짰다.

★ 공통점: **측정하려고 고른 도구가 결론을 정했다.**  반대로 **코드 안의 fail-closed 가드
둘**(어댑터 봉인 검사 · 생성기 `--out` 충돌 검사)은 각각 이 사고와, `latest_run` 별칭 때문에
96팔을 **192개로 두 번 돌릴 뻔한 것**을 실제로 막았다.
