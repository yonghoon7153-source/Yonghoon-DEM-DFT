# 적대적 리뷰 요청 — 12차 · α·β 검증 하네스 (`bms-balancing/`)

> ## ⚠ 이 요청문은 **보내지 못했다** — `reviews/R13_REQUEST.md` 가 대신한다
>
> Codex 토큰이 끊겨 12차를 외부로 못 보냈다. 대신 `/self-review` 6 렌즈를 내부에서 돌려
> **35 건**을 찾아 닫았고 (`결론이_바뀜` 14), 그 라운드가 **이 문서가 "닫았다" 고 적은 것의
> 절반이 반쪽이었음**을 드러냈다 (`R13_REQUEST.md` §2 표).
>
> **아래 본문의 검증 숫자를 인용하지 마라.**
> `202 passed` → 지금 **236 passed** · `blocked_by 28·24·4` → 지금 **59·27·5·1**
> (숫자가 커진 것은 요구 축이 늘었기 때문이고 산출 숫자는 안 움직였다 — `R13_REQUEST.md` §4).
> 러너 계약도 둘 바뀌었다 (rc 가 `evidence_eligible` 반영 · `-O` 는 재실행 전에 거부).
>
> 이 문서는 **R11 대응의 기록**으로 남긴다. 현행 요청문은 `reviews/R13_REQUEST.md`.

11차(대상 `2add074`)는 **NO-GO** (P1 12 · P2 6, `reviews/R11_CODEX.md` · 패키지 `reviews/r11_repros/codex/` sha256 13/13).
열여덟 건 전부 수정 전 clean 트리에서 재현 → RED(`tests/test_r11_codex.py` e11_01~19) → 수정 → GREEN 으로 닫았다
(`reviews/R6_LEDGER.md` "Codex R11"). 목표는 같다: **"정본이 우리 새 모델의 설계 근거로 쓸 만한가"**.
GO 기준: R3 §5 + R5 §4 + R6 출처 결속 + R7 §6 + R8 §6 + R9 최소 조건 6 항 + R10 최소 조건 7 항 + R11 최소 조건 5 항.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | 이 파일이 든 커밋 (`git log -1`). 직전 리뷰 대상 `2add074` |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 만 |
| 정본 | `FINDINGS.md` + `out/` (+ `.meta.json`). **현행 out/ 12 개는 provenance-incomplete** (§4) |
| 저장소에 없는 것 | 원본 MATLAB · 원자료 xlsx · 문헌 OCP → `BMS_DATA_ROOT` |
| 11차 대비 새것 | P1-1~12 · P2-1~6 닫음 · **두 실행 사이의 입력 identity 비교** · caller 가 못 줄이는 권위 명부(matrix·profile·ne_shape) · 정본 γ 격자 21 · 부재 allowlist 모순 hard-fail · 파일 단위 alias · production reader 가 checker 와 같은 validator · 유한성 · untracked 코드 · gate 의 pre-import 격리와 snapshot bytes 재대조 · 자식 rc · case 별 반례 fingerprint |
| 증거 커밋 규약 | 러너는 **expected commit 을 materialize** 해서 돈다. 도구 자신도 그 커밋의 blob 이어야 `evidence_eligible: true` 이므로 증거는 **코드 커밋에서** 만들어 그 다음 커밋에 얹는다. 코드 커밋 SHA 와 `git diff <코드 커밋> HEAD --name-only -- '*.py' '*.sh'` 결과는 §7 에 적었다 |

```bash
git clone -b claude/bms-alpha-beta-verify https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT
cd Yonghoon-DEM-DFT/bms-balancing && git checkout <이 파일이 든 커밋>
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest tests/ -q                # 202 passed 기대. 원자료 불필요
bash matlab/tests/run_all.sh               # Octave 없으면 4·5 단계만

HEAD=$(git rev-parse HEAD)                 # ⚠ 러너는 **40 자 full object id** 만 받는다 (R11 P2-6)

python3 reviews/r6_repros/codex_r6_mutation_audit.py                              # 8/8 CAUGHT · MISSED 0
python3 reviews/r6_repros/codex/mutation_adapted.py                               # 5/5 CAUGHT
python3 reviews/r7_repros/replay_codex_r7.py  --target . --expected-head "$HEAD"  # 6 슬롯 (5 소멸 + 1 전제 변경)
python3 reviews/r9_repros/replay_codex_r9.py  --target . --expected-head "$HEAD"  # 12/12
python3 reviews/r10_repros/replay_codex_r10.py --target . --expected-head "$HEAD" # 22 슬롯 (20+1 우리 코드 밖+1 전제 변경)
python3 reviews/r11_repros/replay_codex_r11.py --target . --expected-head "$HEAD" # 35 슬롯 (§3)
python3 scripts/check_u14.py --new out --schema-only            # rc 2: provenance-incomplete (§4)
```

11차 패키지를 **그대로** 돌리려면 (수정 전을 재려면 `2add074` worktree 에서):

```bash
python3 reviews/r11_repros/codex/r11_root_repros.py          --target .
python3 reviews/r11_repros/codex/r11_data_contract_repros.py --target . --case <7 개 중 하나>
python3 reviews/r11_repros/codex/r11_evidence_gate_repros.py --target . --case <8 개 중 하나>
# publish 스크립트는 인자를 안 받고 `../work/harness-r11-target-wsl/bms-balancing` 를 본다 —
# `reviews/r11_repros/replay_codex_r11.py` 가 그 자리를 **그 단계에서만** 만들고 지운다 (자기참조 symlink 를
# 트리에 남기면 다른 probe 의 copytree 가 무한히 돈다 — 실측).
```

## 1. 검증 — 방금 실행

| 검사 | 명령 | 출력 |
|---|---|---|
| 전체 회귀 | `python3 -m pytest tests/ -q` | `202 passed in 157.98s` (`replay_ours_after_fixes/pytest_full.txt`) |
| MATLAB 스모크 (Octave) | `bash matlab/tests/run_all.sh` | `전부 통과` (`matlab_smoke.txt`) |
| 변이 감사 (우리 테스트) | `codex_r6_mutation_audit.py` | `8/8 CAUGHT · MISSED: 0` |
| 적응판 변이 감사 | `mutation_adapted.py` | `5/5 CAUGHT · MISSED: 0` · baseline·복구 6/6 닫힘 |
| R6 적응판 재생 | `replay_codex_r6_adapted.py` | `"mode": "full"` 6/6 닫힘 |
| R7 · R9 · R10 닫힘 재생 | `replay_codex_r{7,9,10}.py --expected-head <코드 커밋>` | 반례 소멸 5+1 전제 변경 · 12 · 20+1 우리 코드 밖+1 전제 변경. 전부 `evidence_eligible: true` · `instrument_sealed: true` · `ran_in: 격리 snapshot` · `expected_tree efa727fac821…` |
| **11차 패키지 재실행 (수정 뒤)** | `replay_codex_r11.py` | **반례 소멸 32 · 전제 변경 2 · 환경상 불가 1** (§3), `evidence_eligible: true` |
| 현행 정본 점검 | `check_u14 --new out --schema-only` | rc 2 · `promotion_eligible: false` — 새 스키마 누락 28 (sidecar `argv` 12 + `roster` 12 + profile `gamma_roster` 4) · 출처 열 24 · 내용 4 (§4) |

## 2. R11 열여덟 건 — 재현과 수정

수정 전 재현은 `reviews/r11_repros/replay_ours_2add074_before/` (sparse worktree at `2add074`, dirty 0). 발견별 수정과
테스트 이름은 원장의 표가 정본이다 (`reviews/R6_LEDGER.md` "Codex R11"). 축만 적으면:

| 축 | 무엇이 바뀌었나 |
|---|---|
| **입력 identity (P1-1)** | `check_u14` 가 baseline↔candidate 의 `{역할: full sha256}` 을 target·ref 양쪽으로 정규화해 비교한다. 다르면 `blocked_by.inputs` 로 rc 2 — 숫자 비교 전에 막는다. 한쪽이 입력을 아예 안 적었으면(정본이 옛 스키마) **"대조 불가"** 로 적고 rc 는 안 바꾸되 `promotion_eligible: false` (`inputs_uncomparable`). 답변 1 의 "path 는 빼도 되지만 role→SHA map 은 반드시 비교" 를 그대로 구현했다 |
| **권위 명부 (P1-2·3·4)** | matrix 는 `HALF_FILE × SI_SOURCES × w_dqdv`(알려진 부재 제외)를 먼저 세고 caller 가 좁히면 `subset` rc 3 · `partial/`. profile 은 `S.CANONICAL_GAMMA_GRID_N = 21` 이 정본 격자이고 다르면 subset. 부재 allowlist 가 **실제 파일과 모순되면 hard-fail rc 2** (답변 2) |
| **승격 증명서 (P1-5·6)** | 디렉터리뿐 아니라 **파일 단위** `samefile` 로 hardlink 자기대조를 막고, `--schema-only` 는 구조상 언제나 `promotion_eligible: false`, sidecar 는 `argv`·`roster` 필수이며 명부는 본문에서 유도한 `S.body_roster` 와 대조한다 |
| **과학 입력 (P1-7·8)** | `ne_shape.fitted_pair_info` 가 checker 와 **같은** `S.check_rows` 를 exact header 로 돌린다. 숫자 열은 제외로 유도해 전부 `math.isfinite`, 게시는 `allow_nan=False` |
| **실행 identity (P1-9·10, P2-5·6)** | provenance 가 untracked 를 보되 산출 root **밖**만 코드로 센다. 러너는 gate 를 **import 하기 전에** bytecode 를 격리하고, materialize 뒤 `verify_snapshot_bytes` 로 풀린 tracked bytes 를 blob object id 와 재대조하며, skip-worktree 는 대문자 `S` 도 잡고, expected head 는 40 자만 받고 `expected_tree` 를 같이 적는다 |
| **증거 판정 (P1-11·12)** | 자식 rc 0 을 payload 읽기 **전에** 강제하고(`child_ok`), 닫힘은 case 별 **반례 assertion fingerprint** 와 맞을 때만 인정한다(`COUNTEREXAMPLE_LINES`) |
| **typed status (P2-1·2)** | profile 의 rc 는 sink 와 무관하다. producer 가 `SHAPE_RESULT {json}` 로 자기가 쓴 경로·run_id·status 를 말하고 `shape_step` 이 rc ↔ status ↔ namespace ↔ run_id 를 대조한다 (못 대조하면 실패). 바깥 wrapper 는 partial 을 따로 세고 종료 코드 3 |
| **receipt·roster 모양 (P2-3·4)** | dotted top-level 역할과 중복 논리 역할을 거부하고 `receipt_map`·`receipt_paths` 로 역할별 path 를 드러낸다. `gamma_roster` 는 exact JSON schema 로 parse 해 행마다 같은지·산술이 맞는지 본다 |

## 3. 11차 패키지 재실행 — 닫힘 재생기의 세 가지 판정

`reviews/r11_repros/replay_codex_r11.py` 는 네 스크립트를 계약 그대로 돌리되 **case 마다 봉인한 술어**로만 닫힘을
센다 (표에 없는 case 는 닫힘이 아니다 — P1-12 가 R10 러너에서 지적한 규율을 처음부터 적용). 35 슬롯:

- **반례 소멸 32** — root 5 (assert 계약: 자기 반례 assertion 에서 멈춤) · data 6 · check 12 · publish 1(`shape_step`) ·
  evidence 8. (자체 리뷰 C20: 전 판은 root/data 를 뒤집어 적었고 같은 절의 다음 불릿과 모순이었다.)
- **전제 변경 2** (fingerprint 를 봉인해 아무 예외나 이렇게 읽히지 않게 했다):
  - `publish:*` — 좁힌 matrix 를 canonical 자리에 안 쓰므로 원본 probe 가 그 파일을 열다 죽는다
    (`FileNotFoundError: …/publish/matrix_100.csv`). 같은 축은 `data:matrix_subset`·`data:profile_grid`·
    `root:matrix_authority` 가 따로 본다.
  - `root:profile_grid` — 원본의 "완전" 대조군이 `--grid 3` 이라 그것도 subset 이 되어 canonical 자리에 파일이 없다.
    같은 축은 `data:profile_grid`(`canonical_written: false`) 와 회귀 `test_d10_03`.
- **환경상 불가 1** — `data:shape_wrapper` 는 원본이 `wsl.exe` 로 wrapper 를 부른다 (리뷰어는 Windows). 같은 축을
  `publish:shape_step` 이 native 로 재생하고 회귀 `test_e11_14` 가 고정한다. **닫힘으로 세지 않았다.**

## 4. 정본 범위 — 현행 `out/` 은 여전히 provenance-incomplete

`check_u14 --new out --schema-only` 는 rc 2 · `promotion_eligible: false` 다 (실측):

- **새 스키마 누락 28** = sidecar `argv` 12 + sidecar `roster` 12 (이번 라운드 P1-6 이 필수로 만들었다) +
  profile `gamma_roster` 4
- **기준/대상 입력 출처 열 누락 24** (R7-03·R8-04 스키마 이전 실행)
- **내용 검사 실패 4** — degeneracy 의 옛 `inputs_sha` 가 역할 결속 digest 로 재계산되지 않는다 (R10 에서 규칙이
  바뀌었고 **숫자는 하나도 안 움직였다**)

소급해서 값을 채워 넣지 않는다 — 그러면 그 digest 가 무엇을 증명하는지 사라진다. U18 재실행이 새 규칙으로 서명한다.

## 5. 닫지 않은 것 — 신뢰 경계 (11차 답변이 지목한 것을 그대로 적는다)

| # | 무엇 | 지금 상태 |
|---|---|---|
| export 공통 snapshot (답변 3 · 최소 조건 3) | full-cell + 문헌 gr/si 는 **한 공통 immutable snapshot**, half-cell 은 `(source,state,sha)` role snapshot + cohort manifest | **미구현.** 이번 라운드는 identity 를 *대는* 쪽(P1-1)만 넣었고 *주입하는* 쪽은 안 넣었다. 패키지의 `shared_full_cell_mismatch_accepted` 는 여전히 `true` 다 |
| 부재 allowlist 를 dataset manifest 로 (답변 2) | 코드 상수 `D.HALF_CELL_ABSENT` 는 과도기 | 모순 hard-fail 은 넣었다 (P1-4). versioned manifest 로 옮기는 것은 다음 |
| run receipt (답변 4) | code commit/tree + runner/gate digest + package + runtime 을 한 receipt 로 묶고 consumer 가 ancestry 를 검증 | 조각은 다 있다 (`expected_head`·`expected_tree`·`instrument`·`package_digest`·`materialized`) — **한 receipt 로 묶어 서명하고 consumer 가 검증하는 부분이 없다** |
| partial 수명 (답변 5) | `partial/<producer>/<attempt-id>/` immutable unit + retention/GC/index | **미구현.** 지금은 같은 이름의 다음 부분 실행이 그 자리를 덮는다 (canonical 은 안 건드린다). wildcard 소비는 P2-2 로 없앴다 |
| locator 무결성 필드 (답변 1) | 확장자·sheet·parser 선택처럼 **해석을 바꾸는** locator 는 semantic identity | receipt 에 role→path 는 드러냈지만(`receipt_paths`) parser selector 를 별도 필드로 묶지는 않았다 |
| typed `(root, state, si)` identity | 문자열 `state\|si` 유지 | R9 Q1 이후 그대로 |
| U16 · U17 · U18 | 사용자 기계 실측 | 전과 같음 |

## 6. 질문

1. **`inputs_uncomparable` 의 등급**: 정본이 옛 스키마라 입력을 안 적었을 때, 역할별 mismatch 로 세면 "16 건 다르다" 는
   거짓말이 된다. 그래서 **rc 는 안 바꾸고**(정본의 스키마 공백은 candidate 의 계약 위반이 아니므로) `promotion_eligible`
   만 false 로 두고 별도 blocker 로 적었다. 이 분리가 맞는가, 아니면 rc 2 로 올려야 하는가.
2. **locator 무결성 필드의 경계**: parser selector 를 어디까지 identity 로 볼 것인가 — (a) 확장자·sheet 이름, (b) 그 위에
   header 행 수·열 매핑 같은 **parser 설정**, (c) 그 위에 parser 코드 자체의 digest. (c) 까지 가면 code identity 와
   겹치는데, 셋 중 어디가 최소선인가.
3. **run receipt 의 소비자**: 답변 4 의 "consumer 가 뒤의 evidence blob 과 허용된 ancestry 를 검증" 에서 consumer 는
   무엇인가 — (a) 다음 라운드의 리뷰어(사람), (b) 저장소 안의 검사 스크립트, (c) CI. 우리는 (b) 를 만들 생각인데,
   그 스크립트 자신의 봉인은 어느 커밋 기준이어야 하는가 (자기참조를 어떻게 끊는가).
4. **partial 의 attempt-id**: `attempt-or-content-id` 중 어느 쪽이 정본인가. run_id(시도)로 하면 같은 bytes 가 여러 번
   쌓이고, content id 로 하면 "몇 번 시도했는가" 가 사라진다. 둘 다 적고 index 로 잇는 것이 맞는가.
5. **정본 격자의 위치**: `CANONICAL_GAMMA_GRID_N = 21` 을 코드 상수로 뒀다 (부재 allowlist 와 같은 종류의 문제다).
   이것도 dataset-side manifest 로 가야 하는가, 아니면 **계산 계약**이라 코드가 정본인 것이 맞는가.

## 7. 실측 첨부

- `reviews/R11_CODEX.md` · `reviews/r11_repros/codex/` (패키지 14 파일 = 서명된 13 + `HARNESS_R11_SHA256SUMS.txt`, sha256 13/13) ·
  `reviews/r11_repros/replay_ours_2add074_before/` (수정 전 재현) · `reviews/r11_repros/replay_ours_after_fixes/` (수정 뒤).
- `reviews/r11_repros/replay_codex_r11.py` (닫힘 재생기 — case 별 봉인 술어) · `reviews/evidence_gate.py` (러너 공용 봉인) ·
  `bms_balancing/schema.py` (스키마·역할·환경·명부 정본) · `reviews/R6_LEDGER.md` "Codex R11" 절.
- 코드 커밋은 `4185955` 다. `git diff 4185955 HEAD --name-only -- '*.py' '*.sh'` 는 **0 개** — 뒤 커밋은 증거 파일과
  그 결과를 적은 문서뿐이다. 자세한 것은 `reviews/r11_repros/replay_ours_after_fixes/README.txt`.

## 8. 이후

GO 면 새 모델 설계 요구서(`docs/`) 초안. NO-GO 면 §5 의 다섯 축(export 공통 snapshot · dataset manifest · run receipt ·
partial 수명 · locator 무결성)을 다음 라운드의 작업 목록으로 삼는다. U16·U17·U18 은 사용자 기계 실측.
