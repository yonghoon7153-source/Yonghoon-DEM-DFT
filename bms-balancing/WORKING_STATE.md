# 진행 상태 — α·β 검증 하네스

> **이 파일이 "지금 어디까지 왔나" 의 정본이다.** 수치의 정본은 `FINDINGS.md` + `out/`.
> 갱신 규칙: 단계가 열리거나 닫히면 **그 커밋에서 같이** 고친다.

**목표가 바뀌었다 (2026-09-11, 사용자 결정).** 코드를 준 분이 은퇴하며 사용자가
**전권**을 받았다. 규진팀에 회신하지 않고 **우리 독자 모델로 발전**시킨다.
그러므로:
- `FOR_BMS_TEAM.md` 는 더 이상 산출물이 아니다 — **보관**(배너로 표시, 갱신 안 함).
- 검증 하네스의 발견은 "남의 코드 감사" 에서 **"우리가 물려받은 코드의 감사 +
  새 모델의 설계 요구서"** 로 역할이 바뀐다. 새 모델의 출발점은 리뷰가 남긴 **관측**이다
  — PE 기준 처리가 답을 %p 단위로 바꿈 · 원통형의 적합 잔차가 사이클과 함께 커짐 ·
  선택된 γ 쌍의 진폭비 3~16 % · 블렌드 vs 측정 음극 rms 19~24 mV. "모델 부적합"
  은 그 관측들을 함께 설명할 **후보 가설**이지 확인된 원인이 아니다 (Codex R3-01·02:
  정확한 모델 + 상태별 잡음, 정확히 표현 가능한 곡선이 같은 표·같은 비를 낸다).
  새 모델의 요구서는 `관측 → 후보 원인 → 구분 시험 → 채택 기준 → 남는 한계` 로 쓴다.
- 규진팀에 물어봐야 닫히던 U1(전사 함수 2 개)·U2(pOCV 원자료 여부)는 이제 **우리가
  원본 코드·원자료를 직접 열어** 닫을 수 있다.
- 원자료는 여전히 public 저장소에 넣지 않는다 (전권 ≠ 공개). 바꾸려면 사용자 결정.
- 게이트(`degradation-degeneracy/`)는 본체 브랜치 일이다 — 이 브랜치는 R2 원장을
  끝까지 닫고 R3 를 받는다.

최종 순서(갱신): R2 원장 닫기 → R3 리뷰(GO 까지) → 새 모델 설계 요구서

---

## 지금 상태 — **자체 적대적 리뷰 35 건 닫음 (Codex 토큰 소진 → 내부 6 렌즈) · 현행 정본은 provenance-incomplete**

2026-09-13 Codex 를 더 못 쓰게 되어 `/self-review` 로 6 렌즈를 병렬로 돌렸다 (sig-완전성 · validator-우회 ·
순서-TOCTOU · 파생-보고서 · archive-이식성 · 공정성-의미). 원시 45 건 → 중복 합쳐 **35 건**, `결론이_바뀜` 14 건.
**같은 축을 여러 렌즈가 독립으로 친 것이 셋**이다 (C01·C04·C11 각 3회).

요지는 하나다 — **직전 라운드(R11)가 "닫았다" 고 적은 것의 절반이 반쪽이었다.** 입력 identity 비교는 파일당 한 벌만
만들어 마지막 행만 봤고(C01), alias 는 inode 만 봐서 `cp` 사본이 통과했고(C02), "신고된 위험을 값으로 소비" 는 실은
"키가 있을 때만" 이었고(C03), 정본 격자 검사는 본문과 한 번도 안 댔고(C04), matrix 의 모집단은 stdout 에만
있었고(C05), 유한성은 JSON 문자열을 통과시켰고(C06), 도구 봉인은 checkout filter 를 안 막았고(C07), import 격리는
bytecode 만 막았고(C08·C09), `rc 0` 인데 승격 불가인 상태를 런북이 "0 이면 교체" 로 읽었다(C11).

35 건 전부 RED(`tests/test_r12_selfreview.py` f01~f28) → 수정 → GREEN. 원장은 `reviews/R6_LEDGER.md` "자체 적대적
리뷰" 절. **fixture 는 일곱 번째로 깨졌다** — 정본과 재실행 fixture 가 같은 `run_id` 를 쓰고 있었고, C02 를 닫기
전에는 그것이 아무 의미도 없었으므로 아무도 안 봤다.

**새 규약(자체 리뷰에서 더한 것)**: 입력 identity 는 **행 key 별로** 댄다 · 독립 baseline 은 run id 가 달라야 한다 ·
부재는 안전값이 아니다 · roster 는 본문에 묶인다 (`combo_roster` 가 matrix 행에도) · 과학 값은 문자열이어도 유한해야
한다 · 도구 봉인과 snapshot 검증은 **같은 플래그**(`--no-filters`) · 러너는 `-P -E` 로 재실행해 봉인을 import 앞에
둔다 · production heredoc 은 `-I -P` · 줄끝은 catch-all 로 고정 · 승격 불가는 rc **4** (단 `--schema-only` 는 승격을
묻지 않은 진단이라 0) · 명부는 배제목록 · 러너 rc 는 `evidence_eligible` 을 반영한다.

**정본 범위 (변화 없음)**: `check_u14 --new out --schema-only` rc 2 · `promotion_eligible: false`. 새 검사가 늘면서
수치가 커졌다 — 스키마 누락 59 (sidecar `argv`·`roster` 26 + `gamma_roster` 4 + `combo_roster` 등) · 출처 열 27 ·
내용 5 · provenance 1. **숫자는 하나도 안 움직였다**; 늘어난 것은 요구하는 축이다. U18 재실행이 새 규칙으로 서명한다.

### 리뷰 3 건 결과 — **전부 NO-GO** (2026-09-13)

셋을 독립 트랙으로 본다. 서로의 판정을 이어 붙이지 않는다.

| 트랙 | 판정 | 지금 상태 |
|---|---|---|
| ① mph 마이크로 쇼츠 | NO-GO ×2 (v1·v2) | **M1 전제가 깨졌다.** `cEeqref_mat = from_mat` — 선택자가 재료값이고 사용자 식 `cs_max*dm` 은 안 쓰인다. 문서 v3 정정은 **COMSOL 값 받은 뒤**. 요청서 `docs/COMSOL_CHECK_REQUEST.md` 대기 중 |
| ② R13 하네스 | NO-GO (P1 4 · P2 5) | **P1-1~P2-5 · §5 Q6 전부 닫음** (262 passed). 남은 것: 실데이터로 shape 재생성(사용자 기계, 아래 U18 4 단계) · 단일 회신 `reviews/R13_RESPONSE.md` |
| ③ BML α·β 난간 | NO-GO (B1~B5 전부 미증명/반박) | **주장 사슬 전부 철회** → 원인은 `rng(0)` 오염(§9) → **우리가 다시 뽑는다** (전권, `BML_R1_RESPONSE.md` §10): (a) `matlab/fit_cycles_driver.m` · (b) `scripts/fit_cycles.py` · 난간 `scripts/check_rails.py` (받은 xlsx 4 개에서 §6 재현). 남은 것: 사용자 기계 실행 (아래) |

**세 라운드 공통 교훈**: 정정이 또 다른 단정이 됐다. "세 모드 붕괴" 를 고치며 "LLI 는 독립"
이라 했는데 `c_lit = C_cell·(a_PE+b_PE−b_NE)` 항등식이 그것도 무너뜨렸다. 관측과 해석의
경계를 매 라운드 다시 그어야 한다.

**①·③ 이 요구하는 외부 자료** — 이것 없이는 더 못 닫는다:
- COMSOL: `liion.pce*.pin1.cEeqref` 실효값 (현재 설정으로 새로 초기화한 것. 저장 해는 설정이 다르다)
- ~~MATLAB: 자유/고정 변수 · lb/ub · …~~ → 원본 확보로 닫힘 (§8). 이제 필요한 것은 **네 셀(ref1·ref2·PE1·PE5)의 원시
  사이클 워크북 + 그 셀들의 기준 반쪽전지** — 결과표에는 없다. 형식은 `<cycle>_capacity/<cycle>_voltage`.

**③ BML 다음 — 사용자 기계에서** (둘 다 `git pull` 뒤, `BMS_DATA_ROOT` 는 data/literature 가 있는 루트):

```bash
# (b) Python 포팅 — 셀 하나, seed 둘 (두 산출이 갈리면 시작점이 정한 적합이다: §10-2)
python3 scripts/fit_cycles.py --half-cell "$BMS_DATA_ROOT/data/half_cell/GITT/pristine.xlsx" \
    --full-cell <L_ref1 사이클 워크북.xlsx> --cell L_ref1 --si-source Li --starts 20 --seed 0 --out out_cycles/seed0
python3 scripts/fit_cycles.py ... --seed 1 --out out_cycles/seed1
python3 scripts/check_rails.py out_cycles/seed0/cycles_L_ref1_Li.csv out_cycles/seed1/cycles_L_ref1_Li.csv
python3 scripts/check_u14.py --new out_cycles/seed1 --old out_cycles/seed0     # 조건 같고 숫자 다르면 rc 1 = 그것이 발견
# (a) MATLAB — 규진팀 원본 폴더에서 (rng( 가 남아 있으면 드라이버가 거부한다)
#   cfg = struct('pipeline_dir',pwd,'data_root',pwd,'half_cell_file','data\half_cell\GITT\pristine.xlsx', ...
#                'full_cell_file','<L_ref1 사이클 워크북>','cycles',[],'si_source','Li','label','L_ref1','out_dir','results_refit');
#   fit_cycles_driver(cfg)      % → results_refit/result_L_ref1_Li.xlsx + .settings.json
python3 scripts/check_rails.py results_refit/result_L_ref1_Li.xlsx           # 2 층 repeated_values 가 사라졌는가
```

### R13 §5 Q6 닫음 — shape 전용 kind · schema · sidecar 계약 (2026-09-13)

리뷰어 실측을 그대로 RED 로 옮겼다 (`test_g25`: 실제 `ne_shape.py` → 실제 `shape_step` → `check_u14 --schema-only`):
**schema 27 · provenance_cols 3 · content 1** — 리뷰어 숫자 그대로 재현됐다. 원인은 `check_u14._kind` 와
`schema.body_roster` 가 각자 "matrix 아니면 profile" 이라 `ne_shape_*.csv` 도 모르는 이름도 profile 로 읽힌 것.
"PROFILE_ROW 에 열 19 개를 허용" 이 아니라 **종류를 하나 더 만든다**:

| 축 | 어디 | 무엇 |
|---|---|---|
| kind 라우팅 | `schema.kind_of(name)` | 한 함수 · 모르는 이름은 `ValueError` (fail-closed). `check_u14._kind`·`body_roster` 가 이것만 쓴다; gate 는 모르는 이름을 "모르는 산출 종류" content 로 센다 |
| 열 정본 | `schema.SHAPE_ROW` (22) | 기존 20 + `inputs_sha`·`consumed_inputs`. producer 의 header 가 이 tuple 에서 나온다 |
| 행 key | `schema.shape_key` = `state` · `row_key(kind)` | 중복 상태는 중복 key |
| receipt | 행마다 역할 `SHAPE_ROLES` = matrix · half_cell · half_cell_pristine · literature.gr · literature.si | `_row_receipt` 가 sidecar 의 상태별 dict 를 역할 모양으로. 짝 없는 행은 빈 칸(receipt 를 지어내지 않는다) |
| 빈 칸 허용 | `SHAPE_MAY_BE_EMPTY` = witness 둘 | R3-03 의 "격자에서 증인 없음" — 둘이 **함께** 비어야 한다 |
| coverage | `check_shape_coverage` | 본문 상태 집합 ↔ `canonical_shape_states(source)` (= `data.declared_states`, producer 와 같은 함수). 선언 밖 상태 = content · 부분집합 = 자리 규칙(`CANONICAL_SLOT_PREFIX`) |
| sidecar | `check_shape_meta` | typed `status` · `pairing` 산술(available ⊎ missing_input = requested · paired ⊎ missing = available) · 본문 결속 · authority = 정본 · status = producer 판정식 |
| meta 계약 | `_write_csv` | env · started_utc · git_commit_at_start · git_state_changed_during_run · argv · roster(잠금 안 같은 bytes) — `write_meta` 와 같은 축. 실행 조건은 `meta_controls("shape")` = half_cell_source · si_source · grid_n · grid_range · gamma_grid (state/starts/seed 가 아니다) |

회귀 `test_g18~g25`. g25 가 producer→wrapper→U14 완주(합성 원자료 + fixture matrix)와 **두 번째 독립 실행의
승격 자격**(숫자·입력 identity·조건 동일, clean 트리면 `promotion_eligible: true`)까지 잰다.
리뷰어 스크립트의 `consumed={"synthetic": True}` 는 receipt 가 아니라 **receipt 축에서만** 막힌다 (g21) — 그 호출이
통과하지 않는 것이 맞다.

정본 `out/` 의 blocked_by 는 59·27·5·1 → **40·25·6·1**: 옛 shape 가 이제 제 종류로 읽혀 "열 19 개 모름 + profile 열
21 개 누락" 이 사라지고, 대신 `inputs_sha`·`consumed_inputs` 누락 2 · `status`·`pairing` 없음 2 로 잡힌다.
**숫자는 여전히 하나도 안 움직였다.** 옛 sidecar 를 소급 보수하지 않는다 (리뷰어 §Q6 답 그대로) — 실데이터
재생성은 사용자 기계에서 아래 U18 4 단계로.

코드 `ef8e8f6` · 증거 `84ab3b3` (`reviews/r13_repros/replay_ours_after_fixes/`, leaf 별 판정은 직전 판과 동일) ·
회신 `reviews/R13_RESPONSE.md` — 발견 9 건 + Q6 · GO 조건 1~8 대응 · 열린 것(조건 6 동적 인증 · 조건 7 실데이터 재실행 · 조건 8 다섯 축).

---

### 다음 — Codex 토큰 복구, 리뷰 요청 3 건 대기 (2026-09-13)

Codex 를 다시 쓸 수 있게 되어 요청문 셋을 썼다. **보내는 순서도 이 순서다.**

| 순 | 요청문 | 대상 | 왜 이 순서 |
|---|---|---|---|
| 1 | `reviews/REQ_MPH_MICROSHORT.md` | 규진팀 마이크로 쇼츠 COMSOL 모델 분석 (`docs/MICROSHORT_MPH_REVIEW.md`) | 지금 제일 뜨겁고 반증 가능성이 명확하다 — `cEeqref` 가 SOC 분모라는 전제(A1) 하나가 무너지면 M1 이 통째로 무너진다. COMSOL 미실행 |
| 2 | `reviews/R13_REQUEST.md` | 하네스 13차 — 자체 리뷰 35 건 닫음 (`c7217c0` 코드 · `85038ee` 증거) | 쌓인 빚. R11 이후 외부 눈이 한 번도 없었다. 핵심 물음은 "§2 의 반쪽으로 닫음 패턴이 이번 35 건에도 있는가" |
| 3 | `reviews/REQ_FIT_RAILS.md` | α·β 적합 출력의 난간·축퇴 (xlsx 37 행) | MATLAB 원본을 봐야 결론이 나서 Codex 혼자로는 절반만 답한다 (B3 = `a_PE` 상한 존재가 유일한 약점) |

`reviews/R12_REQUEST.md` 는 **보내지 못한 문서**로 배너를 달아 보관했다 (R13 이 대신한다).

**1차 결과 (mph 트랙, 2026-09-13): NO-GO.** "M1 은 확정 버그이므로 `cEeqref` 두 줄부터 고친다" 가
당시 증거로 성립하지 않았다. 패키지는 `reviews/r14_repros/codex/` 에 원본 보존(zip sha256
`e2d74fb8390e…`), 대응 원장은 `reviews/MPH_R1_RESPONSE.md`, 문서는 v2 로 재작성했다.
**바뀐 결론 다섯**: (1) M1 은 조건부 진단 — 조건은 `liion.pce2.pin1.soc` t=0 값 한 번으로 끝난다
(2) 붕괴하는 것은 **두 LAM** 뿐, LLI 는 독립 (3) 휴지 후반 기울기는 쇼츠 전용축이 **아니다**
(`C_diff` 가 LLI/LAM 에 의존) (4) **Events 인터페이스 자체가 DISABLED** 였다 (5) `tau_short` 차원 오류.

**교훈**: v1 §7 의 정규식 추출기가 자식 flags 를 부모로 전파해 (4)를 틀리게 만들었다. 리뷰어가
원본 파일 없이 정적 반례만으로 잡았다. 교정 도구 `reviews/r14_repros/mph_dump.py` 는
`--self-test` 로 그 반례를 고정하고 태어났다 — `evidence_gate` 규율을 분석 스크립트에도 적용한다.

**mph 트랙 다음 순서**: ① `liion.pce2.pin1.soc` t=0 확인(30초) → ② LAM 계약 정의 → ③ M8 정리
+ MPH sha256/study/solution 기록 → ④ M3 곡선 겹쳐 그리기. ①·② 전에는 `cEeqref` 를 건드리지 않는다.

검증 재실행 (2026-09-13, `26c477c`): `236 passed in 200.29s` · `git diff c7217c0 HEAD -- '*.py' '*.sh'` **0 개** ·
`replay_codex_r7.py --expected-head 26c477c…` rc 0 · `evidence_eligible: true` · `closed: true` ·
`check_u14 --schema-only` rc 2 (59 · 27 · 5 · 1, 보관 증거와 일치).
⚠ `expected_tree` 는 커밋을 따라간다 — 보관 증거는 `ae9e4847…`, `26c477c` 재실행은 `16d44946…`. 불일치가 아니다.

---


## 직전 상태 — Codex 11차 NO-GO (P1 12 · P2 6) 열여덟 건 전부 닫음 (닫힘)

2026-09-13 Codex 11차(대상 `2add074`, `reviews/R11_CODEX.md`, 패키지 `reviews/r11_repros/codex/` sha256 13/13)의 요지:
R10 의 열다섯 수정은 **각 산출 안에서는** 참이 됐지만 세 축이 열려 있다 — (a) 두 실행 **사이**의 입력 identity 를
아무도 대지 않아 old/new 의 네 digest 가 전부 달라도 `promotion_eligible: true` 였고(P1-1), (b) caller 옵션이 권위
명부 자체를 줄여 `--only-source`·`--grid 1` 이 complete canonical 을 게시했으며(P1-2·3) 부재 allowlist 가 실제로 있는
파일을 요청에서 빼고(P1-4) hardlink 자기대조와 `--schema-only` 가 승격 증명서로 통했다(P1-5·6), (c) 증거 기계가 자기
startup 을 안 봉인해 gate 보다 먼저 load 된 위조 pyc·checkout smudge·rc 7 자식·무관한 AssertionError 가 전부
`closed: true` 를 냈다(P1-10~12). 그 밖에 production reader 가 `error` 행을 과학 입력으로 먹고(P1-7), 비유한 값이
스키마를 통과하고(P1-8), untracked `sitecustomize.py` 가 실행되는데 provenance 는 clean 이었다(P1-9). P2 는 sink 에
따라 갈리는 부분 rc(P2-1) · stale wildcard 를 읽는 `shape_step`(P2-2) · 중복 논리 역할(P2-3) · parse 안 하는
`gamma_roster`(P2-4) · 대문자 `S` skip-worktree(P2-5) · 짧은 expected head(P2-6).

열여덟 건 전부 수정 전 clean 트리에서 재현(`reviews/r11_repros/replay_ours_2add074_before/`) →
RED(`tests/test_r11_codex.py` e11_01~19) → 수정 → GREEN. 원장은 `reviews/R6_LEDGER.md` "Codex R11" 절, 요청문은
`reviews/R12_REQUEST.md`. 닫힘 재생기는 `reviews/r11_repros/replay_codex_r11.py` (case 별 **봉인한 술어**로만 닫힘을
센다 — 반례 소멸 32 · 전제 변경 2 · 환경상 불가 1).

**새 규약(11차에서 더한 것)**: 승격은 baseline↔candidate 의 `{역할: full sha256}` 이 **같아야** 하고 한쪽이 입력을 안
적었으면 "대조 불가" 로 승격 자격이 없다 · 권위 명부는 caller 옵션으로 줄지 않는다 (좁힌 실행은 `subset` rc 3 ·
`partial/`) · 정본 γ 격자는 `S.CANONICAL_GAMMA_GRID_N = 21` · 부재 allowlist 가 실제 파일과 모순되면 hard-fail ·
sidecar 는 `argv`·`roster` 를 반드시 담고 명부 유도는 `schema.body_roster` **한 자리** · production reader 는 checker 와
같은 validator 를 exact header 로 통과한 묶음만 먹는다 · 과학 값은 전부 유한해야 한다 · 산출 root **밖**의 untracked 는
코드다 · 증거 러너는 gate import **전에** bytecode 를 격리하고 materialize 한 bytes 를 blob 과 재대조하며 full 40 자
expected head 만 받고 자식 rc 0 을 강제한다 · 닫힘 판정은 case 별 반례 fingerprint 로만.

**정본 범위 (변화 없음)**: 현행 `out/` 12 개는 여전히 **provenance-incomplete** (출처 열 24 + profile `gamma_roster` 4 +
digest 규칙 변경으로 재계산과 안 맞는 degeneracy 4). 숫자는 하나도 안 움직였다 — 바뀐 것은 규칙이다. U18 재실행이
새 규칙으로 서명한다.

## 직전 상태 — Codex 10차 NO-GO (P1 8 · P2 7) 열다섯 건 전부 닫음 (닫힘)

2026-09-13 Codex 10차(대상 `bd6ba47`, 코드 정본 `554dad6`, `reviews/R10_CODEX.md`, 패키지 `reviews/r10_repros/codex/`
sha256 10/10)의 요지: R9 의 열두 수정은 허상이 아니지만 **그 문장이 게시 경계·승격 gate·증거 기계에서는 아직 참이
아니다** — `eval --out X --compare X` 가 독립 근거를 제 출력으로 덮고 자기대조를 `complete` 로 냈고(P1-1), `ne_shape
--states` 가 정본 roster 를 줄여 1 행을 complete canonical 로 게시했고(P1-2), profile 의 실패한 γ 와 matrix 의 전
조합 실패가 canonical 을 부수며 rc 0 이었고(P1-3·4), `error` 한 칸이 행 검증을 전부 껐고(P1-5), receipt 가 역할을
안 묶어 decoy 하나로 통과했고(P1-6), env·control 이 사실상 검사되지 않았고(P1-7), candidate 와 baseline 이 같은
디렉터리여도 승격 판정이 났다(P1-8). P2 는 subset 의 rc 0(P2-1) · stdout invalid rc 0(P2-2) · argv 평탄화와 production
결속 없는 회귀(P2-3) · `python -O` 에서 증거가 다 통과(P2-4) · 실행 bytes 미봉인(P2-5) · package digest 회귀 부재(P2-6)
· ne_shape typed status 를 쓰는 caller 부재(P2-7).

열다섯 건 전부 수정 전 clean 트리에서 재현(`reviews/r10_repros/replay_ours_bd6ba47_before/`) → RED(`tests/test_r10_codex.py`
d10_01~16) → 수정 → GREEN. 원장은 `reviews/R6_LEDGER.md` "Codex R10" 절, 요청문은 `reviews/R11_REQUEST.md`.

**새 규약**: 게시는 **완전성 판정 뒤에만** — matrix·profile·ne_shape 가 typed status(complete/partial/none/subset)를
내고 complete 만 canonical, 나머지는 `partial/` 에 (`PRODUCER_EXIT` 0/3/1) · 정본 roster 는 `D.declared_states(source)`
이고 caller 의 `--states` 는 좁히기만 하며 그 실행은 승격 대상이 아니다 · 알려진 부재는 `D.HALF_CELL_ABSENT` 로 명시
(실측 근거는 원장) · receipt 는 **역할**을 묶는다(`REQUIRED_ROLES`, digest 는 `(역할, sha256)`) · `error` 행이 있는
묶음은 success 가 아니다 · `check_u14` 는 env 를 값으로 대고 필수 control 이 양쪽에 있어야 하며 candidate·baseline
독립성을 요구하고 `--subset` 은 rc 3 + `PROMOTION {…}` 줄을 낸다 · degeneracy 는 sink 와 무관하게 invalid 면 rc 2 ·
증거 러너는 `reviews/evidence_gate.py` 한 자리에서 `-O` 거부 · git rc 확인 · index skip flag 거부 · `__pycache__` 격리 ·
**expected commit 의 sparse worktree 에서 대상 bytes 실행** · 도구 자신의 봉인(`instrument_sealed`)까지 본 뒤에만
`evidence_eligible: true`.

**정본 범위**: 현행 `out/` 12 개는 여전히 provenance-incomplete (출처 열 24 + profile `gamma_roster` 4). 여기에
**digest 규칙 변경**이 더해졌다 — `inputs_digest` 가 역할을 묶으면서 값이 달라져 커밋된 degeneracy 네 개의 옛
`inputs_sha` 가 재계산과 안 맞는다 ("내용 검사 실패 4"). 숫자는 하나도 안 움직였고 바뀐 것은 규칙이다; 소급해서 고쳐
넣지 않고 U18 재실행이 새 규칙으로 서명한다. `check_u14 --new out --schema-only` 가 rc 2 로 말한다.
자기 점검(`--new out --old out`)은 이제 **거부**된다 (P1-8) — 승격 대조는 독립 baseline 으로만.

## 직전 상태 — Codex 9차 NO-GO 열두 건 닫음 (닫힘)

2026-09-12 Codex 9차(대상 `29ef505`, `reviews/R9_CODEX.md`, 패키지 `reviews/r9_repros/codex/` sha256 11/11)의 요지: R8 의 여덟
수정은 허상이 아니지만 **"모집단을 먼저 세고, 검증 snapshot 만 검사하고, 부분은 부분이라 말한다" 가 아직 production 전체의
불변식이 아니다** — 같은 root label 이 앞 요청을 지우고(R9-01), `check_u14` 가 new 에 있는 파일만 세어 1/12 도 전수로 승인하며
(R9-02) 열 이름만 보고 내용·과학 열·실행 조건을 안 보고(R9-03), `ne_shape` 가 없는 반쪽전지 상태를 requested 전에 지우고(R9-04)
중복 matrix key 의 첫 행을 쓰고(R9-05) rc 3 을 내기 전에 완전 canonical 을 부분으로 덮고(R9-06), `eval --compare` 가 경로를 세 번
읽는다(R9-07). P2: 러너의 공허 성공(P2-1) · evidence identity 미집행(P2-2) · rc 2/3/4 를 CAUGHT(P2-3) · matrix sidecar 의
singular 범위(P2-4) · zero-pair 1 vs partial 3 계약(P2-5).

열두 건 전부 수정 전 HEAD 에서 재현(`reviews/r9_repros/replay_ours_29ef505_before/`) → RED(`tests/test_r9_codex.py` d9_01~12)
→ 수정 → GREEN. 원장은 `reviews/R6_LEDGER.md` "Codex R9" 절, 요청문은 `reviews/R10_REQUEST.md`. 수정 뒤 패키지 재실행과 닫힘
재생기(`reviews/r9_repros/replay_codex_r9.py`, R7 러너와 같은 `--expected-head`·dirty·digest 계약)는 `reviews/r9_repros/
replay_ours_after_fixes/`.

**새 규약**: 스키마의 정본은 `bms_balancing/schema.py` 하나 (producer 가 쓰기 직전에 assert, checker·reader 가 같은 함수) ·
`check_u14` 는 명부(정본 ∪ 새 산출)·필수 셀·receipt 내용·중복 key·실행 조건까지 보고 부분 재실행은 `--subset` 계약으로만
(k/N 표시, 승격 아님) · `compare_states` 는 중복 root label 을 판정 전에 거부 · `ne_shape` 는 requested 를 파일 존재 전에 고정하고
typed `status`(complete 0 / none 1 / partial 3) 로 complete 만 canonical 에, 나머지는 `<write>/partial/` 에 · `eval --compare`
는 한 번 읽은 `DdEvalText` snapshot 만 소비 · 두 러너(R7·R9)는 `--expected-head` 필수 + dirty 기본 거부 + 패키지 digest · 변이
감사 CAUGHT 는 rc 1 ∧ `N failed` 만 · `run_states.sh` sidecar 에 `argv`·`roster`.

**fixture 정정**: `_full_matrix_rows`·`_deg(schema=True)`·`_u14_dirs`·i6w_03 의 inline JSON 은 열 이름의 부분집합 + 가짜 receipt
였다 (checker 가 내용을 안 본다는 사실을 가려 줌 — 이 저장소 네 번째 실측). 전부 producer 스키마 + 진짜 receipt 로 다시 썼다.

**정본 범위 (변화 없음)**: 현행 `out/` 12 개는 내용·조건·자기 대조 숫자는 새 검사를 통과하지만 matrix/profile 8 개에 출처 열
3 개가 없다 — **provenance-incomplete** (`check_u14 --new out --schema-only` rc 2, 24 건). 보강은 U18 (사용자 기계, 별도 `OUT=`,
이제 `check_u14` 가 명부 12/12·스키마 내용·조건·수치 exact equality 를 강제한 뒤에만 승격). 열어 둔 것: export 공통 snapshot
계약(Codex Q3) · typed (root, state, si) identity (Q1).

## 직전 상태 — Codex 8차 NO-GO 여덟 건 닫음 (닫힘)

2026-09-12 Codex 8차(대상 `a22da33`, `reviews/R8_CODEX.md`, 패키지 `reviews/r8_repros/codex/`)의 요지: R7 반례는 닫혔지만
**"검증된 개별 묶음 → 완전한 모집단 → 전체 결론" 의 합성**이 안 이어진다 — 같은 state 의 다른 Si 가 서로 덮고 빈 요청
root 가 후보에 안 든다(R8-01), `check_u14` 가 data B/meta A 를 인증하고 출처 열을 요구하지 않는다(R8-02), `ne_shape`
요약이 γ-짝 부분집합에서 측정 최대를 잰다(R8-03), profile 의 전체 입력 identity 가 잘려 나가는 `.log` 에만 있다(R8-04).
P2: 중복 key 행 소실(R8-05) · 선택 0 을 CAUGHT(R8-06) · post-fix 재생 명령 부재(R8-07) · c6_01 의 callback 계수(R8-08).

여덟 건 전부 수정 전 HEAD 에서 재현(`reviews/r8_repros/replay_ours_a22da33_before/`) → RED(`tests/test_r8_codex.py`
d8_01~09) → 수정 → GREEN. 원장은 `reviews/R6_LEDGER.md` "Codex R8" 절, 요청문은 `reviews/R9_REQUEST.md`.

**정본 범위**: 현행 `out/` 12 개는 수치는 R7 과 바이트 동일하고 묶음 12/12 True 이지만 matrix/profile 8 개에
`ref_inputs_sha`·`consumed_inputs`·`ref_consumed_inputs` 가 없다 — **provenance-incomplete** (기준 입력의 출처는 그
묶음에서 회수되지 않는다; `check_u14 --new out --schema-only` 가 rc 2 로 말한다). 보강은 **U18**: 사용자 기계에서
`run_states.sh` 를 별도 `OUT=` 으로 돌려 수치 동일을 확인한 뒤 승격 — pathname 해시로 소급 채우지 않는다. 그때까지
인용은 "수치 그대로 · 기준 입력 출처 미기록" 으로 범위를 붙인다.

규약이 바뀐 것: `load_degeneracy` 는 Si 충돌 시 `state|si` key 로 전부 보존 · `compare_states` 는 요청 root roster 를
찍고 관측 0 인 root 가 있으면 미완 rc 2 · `check_u14` 는 검증 snapshot 만 검사하고 출처 열을 필수로 · `ne_shape` 는
`pairing` 을 남기고 짝이 빠지면 rc 3 · profile 행이 전체 입력 identity 를 실어 나른다 · 변이 감사는 선택 0 을 오류로.

## 직전 상태 — Codex 7차 NO-GO 여섯 건 닫음 (닫힘)

2026-09-12 Codex 7차(대상 `521be85`, `reviews/R7_CODEX.md`)는 **재현 패키지와 함께** 왔다 (`reviews/r7_repros/codex/`,
sha256 10/10). 판정 요지: R6 반례는 닫혔고, **올바르게 읽은 다음 단계**가 안 이어진다 — 반례 상태가 미완으로 빠지면
집계가 "아니오"를 "예"로 뒤집고(R7-01, 빈 디렉터리도 "예"), 잡음 진단이 적합과 **다른 snapshot** 으로 σ 를 재고
(R7-02), matrix/profile 행이 **기준** 입력 출처를 안 남긴다(R7-03). P2 셋은 `check_u14` 의 정책 혼선(R7-04),
우리 재생 스크립트의 baseline 기본값(R7-05), 변이 감사의 rc 0(R7-06).

여섯 건 전부 수정 전 트리에서 재현 → RED(`tests/test_r7_codex.py` d7_01~07) → 수정 → GREEN. 수정 뒤에는 패키지
probe 가 **자기 반례 assertion 에서** 멈춘다 (`reviews/r7_repros/replay_ours_*.json`). 원장은 `reviews/R6_LEDGER.md`
"Codex R7" 절, 요청문은 `reviews/R8_REQUEST.md`.

규약이 바뀐 것: 집계는 **후보/검증/제외**를 세고 제외가 있으면 전체 판정 대신 미완 + rc 2 · `cmd_noise` 는
`build` 가 소비한 원시 배열(`obj.full_cell_raw`)로만 σ 를 잰다 · matrix/profile 행이 `ref_inputs_sha`(+identity)를
남긴다 · `check_u14 --baseline-policy` 로 현행/역사 규칙을 **호출 모드로** 가른다.

## 직전 상태 — Codex 6차 NO-GO 여섯 건 닫음 (닫힘)

2026-09-12 Codex 6차 리뷰(대상 `d431404`, `reviews/R6_CODEX.md`)는 출처 결속 세 조건을 P1 으로 짚었다 — 독자가
검증한 snapshot 이 아니라 경로를 다시 읽는다(R6-01), 현행 산출에 meta 가 없으면 옛 산출로 흘러 들어간다(R6-02),
입력을 파싱한 뒤 경로를 다시 열어 해시한다(R6-03). P2 셋은 정본 선택 규칙이 옛 `_v2` 를 골랐다(R6-04), `-z`
경로를 " -> " 로 쪼갰다(R6-05), U14 판정문의 "적은 시작" 오기(R6-06 — 실제 γ당 25 회). 여섯 건 전부 우리 트리에서
RED 로 재현한 뒤 닫았다 (`tests/test_r6_internal.py` C 절 `test_c6_01`~`06` + Q3 pin). 원장은 `reviews/R6_LEDGER.md`
"Codex R6" 절, 요청문은 `reviews/R7_REQUEST.md`.

규약이 바뀐 것: 독자는 `provenance.read_unit` 이 돌려준 (data, meta) snapshot 만 소비한다 · `run_id` 가 있는
산출은 meta 없이는 미완(False) · 입력은 `data.read_input` 의 bytes 로 파싱과 해시를 같이 한다 · 정본은 unversioned
이름 하나이고 `_vN` 은 `out/archive/` 의 역사 자료다.

**Codex 재현 패키지는 닫은 뒤에 받았다** (`reviews/r6_repros/codex/`, 원본 10 파일 sha256 OK). 세 판으로 돌렸다:
대상 `d431404` 격리 worktree 에서 **일곱 probe 전부 재현** · HEAD 에서 원본 probe 는 전부 '안 재현' 이지만 넷은
hook 이 빗나간 것이라 **적응판**(hook 만 현행 코드로, 판정은 뒤집어)으로 다시 재 **6/6 닫힘** · 그 적응판을 변이로
검사해 **5/5 CAUGHT**. 적응판 변이가 두 군데를 고쳐 줬다 (R6-01a 가 한 순서만 쟀다 · R6-03b 변이를 원 결함이 아닌
자리에 넣었다). 재생 명령은 `R7_REQUEST.md` §0 의 블록.

## 직전 상태 — R6 내부 리뷰 30 건 닫음 · U13·U14·U15 실측 완료 (닫힘)

Codex 토큰 소진으로 6차는 `/self-review` 로 돌렸다 (네 렌즈 37 건 → 적대적 검증 CONFIRMED 30, 전부 RED → 수정 →
GREEN). 그 뒤 사용자 기계 실측 셋이 붙었다 — U13(scale 동치 18 build), U15(MATLAB `sprintf` 기준선), U14(네 상태
재실행). 원장은 `reviews/R6_LEDGER.md`, 요청문은 `reviews/R6_REQUEST.md`.

**U14 판정: 결론 숫자는 전부 재현됐다.** matrix 세 상태와 degeneracy 세 mode 폭이 **0.00e+00**, §5-1 문턱 표의
n 과 최악 비도 동일. 움직인 것은 γ 프로파일의 개별 행(LAM_NE 최대 2.8e-2)뿐이고 §5-1 폭은 넷째 자리에서만
바뀐다. 두 산출 모두 γ당 25 회를 썼고 **같은 예산 아래 일부 행이 달랐다 — 원인은 U16 미확정**이다 (Codex
R7 §5). 정본을 만든 라이브러리 조합은 모른다(그 산출에 `env` 가 없다) — "scipy 판 때문" 은 가설이고 U16(옛 조합
재실행)이 닫는다. **어떤 결론도 뒤집히지 않았다.**

U14 가 드러낸 다섯 건(U14-01 줄끝로 서명이 fresh clone 에서 깨짐 · 02 도구의 정본 선택 · 03 새 열을 소비 helper 가
못 읽음 · 04 충돌 표식 · 05 재실행이 §4-0 의 역사 자료를 덮음)은 전부 닫았다.

남은 것: Codex 6차 요청문 송부 (토큰 복귀) → 새 모델 설계 요구서 (문헌 입력은 `docs/LIT_19_20_FOR_NEW_MODEL.md`).
아래 명령은 실행 기록.

```bash
# ── 0. 받기 · 확인 (몇 분) ────────────────────────────────────────────────────────────────────────
cd ~/dd/bms-balancing && git pull --rebase origin claude/bms-alpha-beta-verify
source .venv/bin/activate && export BMS_DATA_ROOT='/mnt/d/가형 관련/degradation mode'
python3 -m pytest tests/ -q                       # 273 passed 기대 (원자료 불필요)

# ── 1. 배관 확인 — 새 스키마가 붙는지만 (몇 분, STARTS=6 이라 수치는 못 쓴다) ─────────────────────
STARTS=6 STATES=100 OUT=out_u14_smoke ./scripts/run_states.sh
python3 scripts/check_u14.py --new out_u14_smoke --schema-only     # 0 이어야 한다
# ↑ 0 이 아니면 여기서 멈추고 출력을 그대로 붙여 줘. 2 = 스키마 누락(옛 코드로 돈 것).
rm -rf out_u14_smoke

# ── 2. 본 실행 — 정본을 덮지 않고 **다른 디렉터리로** 받는다 (몇 시간) ────────────────────────────
#    정본(out/)을 먼저 덮으면 "숫자가 움직였나" 를 댈 대상이 사라진다. 네 상태 × 세 명령 = 12 회.
OUT=out_u14 STATES='100 200 300_0009 300_0147' ./scripts/run_states.sh 2>&1 | tee out_u14.log

# ── 3. 대조 — 새 스키마 + 정본과 같은 숫자인가 ───────────────────────────────────────────────────
python3 scripts/check_u14.py --new out_u14        # 0 = 승격 가능 · 1 = 숫자가 다름 · 2 = 계약 위반 · 3 = 부분 · 4 = 승격 불가
#    ⚠ 자체 리뷰 C11: **rc 만 보고 승격하지 말 것.** 정본이 옛 스키마라 입력 identity 를 댈 수 없으면 계약은 안
#      깨졌지만 승격 자격이 없다 (지금 `out/` 이 정확히 그 상태다). 정본은 마지막 줄의 `PROMOTION` JSON 이다:
#         python3 scripts/check_u14.py --new out_u14 --old out | tail -1 \
#           | sed 's/^PROMOTION //' | python3 -c "import json,sys;d=json.load(sys.stdin);print(d['promotion_eligible'], d['blocked_by'])"
#    out/ 을 이미 덮었으면 정본을 git 에서 읽는다 (손으로 `git show` 를 엮지 말 것 — `--name-only` 는 트리가 아니다):
#      python3 scripts/check_u14.py --new out --old-rev <재실행 커밋>^
#    ★ 1 이면 그것이 발견이다. 계산 경로는 안 고쳤으니 같아야 한다. 출력과 함께 이것도 붙여 줘:
python3 -c "import json;print(json.load(open('out_u14/matrix_100.csv.meta.json'))['env'])"

# ── 3b. U14-01 뒷수습 (2026-09-12 실행에서 드러남) — 줄끝 때문에 서명이 깨진 산출을 다시 서명 ──────
#    writer 가 CRLF 를 썼고 git 은 LF 로 저장한다 → fresh clone 에서 meta 의 sha256 이 안 맞고, reader(F07)가
#    그 상태를 표에서 뺀다. 지금 코드는 LF 로 쓰지만 **이미 게시된 것**은 이 명령으로. 기록된 해시가 지금
#    bytes 의 줄끝 변형과 맞을 때만 다시 서명하고(=내용이 같다는 증명), 아니면 손대지 않는다.
python3 scripts/check_u14.py --new out --renormalize

# ── 4. `promotion_eligible: true` 였을 때만 정본 교체 (rc 0 **이면서** 그 줄이 true, 자체 리뷰 C11) ──────
for f in out_u14/*; do mv "$f" out/; done && rmdir out_u14
python3 scripts/ne_shape.py                       # 소비 입력이 바뀌었으니 (d) 표도 다시 (초 단위)
#    ⚠ R13 §Q6 뒤: shape 도 U14 계약이다 — 아래가 shape 줄 없이 나와야 정본이다 (남는 것은 degeneracy digest 4 뿐)
python3 scripts/check_u14.py --new out --schema-only | grep -c ne_shape   # 0 이어야 한다
python3 scripts/compare_states.py out             # §1-10 표 재생 — '묶음 불일치' 경고가 없어야 한다
git add out/ && git commit -m "U14 — 새 게시·서명 스키마로 네 상태 재실행 (숫자 동일)" && git push

# ── 5. ~~MATLAB 한 줄씩~~ → **닫힘 (U15, 2026-09-11)**: 둘 다 Python 과 일치 ────────────────────
#      sprintf('%.2f', 0.125)  → '0.12'                    (half-to-even, Python 과 같다)
#      sprintf('%.17g', 1e-5)  → '1.0000000000000001e-05'  (2 자리 지수, 원래 double 로 복원)
#    기준선은 tests/test_r6_internal.py 의 MATLAB_SPRINTF 에 고정. 다른 MATLAB 판·플랫폼의 산출을 댈 때는 다시 잰다.
```
줄마다 `equiv=1` 이면 그 build 에서 scale 이 원본 설명식과 상대 1e-9 안에서 같다 (유한 · 예외 없음 · eps_rel ≤ 1e-9).
`degeneracy`/`profile`/`matrix` 를 다시 돌릴 때는 `run_states.sh` 가 이제 id 를 **필드로** 확인하고 meta 를 잠금
안에서 재확인해 bytes 해시와 함께 쓴다 (R5-04 · R5-08). matrix 행에 target/ref scale·감사가 실린다 (R5-07).

## 직전 상태 — Codex R4 (닫힘, `reviews/R4_LEDGER.md`)

2026-09-11 Codex 4차 리뷰(대상 `39a5fe0`) 일곱 건을 전부 재현·닫았다. U12 실측(사용자 기계, 274f1f8):
4 루트 × 4 상태 16 build 전부 Inf 0 · NaN 0 (`out/scale_audit_eval.txt`) — 그 증거 수준은 R5-09 로 "보고 순서의
16 줄(식별자 없음)" 로 한정했고, 동치 조건에 eps_rel 이 빠져 있던 것은 R5-06 으로 정정했다.

## 직전 상태 — Codex R3 (닫힘, `reviews/R3_LEDGER.md`)

2026-09-11 Codex 3차 리뷰(대상 `a432d23`) 아홉 건을 전부 재현·닫았다. 사용자 기계 실측(`ne_shape.py`
재실행, fb62342)으로 §5-2 (d) 표를 채웠다 — 100·200 은 (a) 진폭을 내는 합법 γ 가 있고(줄이는 쪽),
300_0009 는 합법 최대 86.01 mV < 119.34 mV 로 없다 (정규화·모양 한정어). 그 meta 의 `git_dirty: true`
로 자체 발견 S-01(산출물 재작성이 플래그를 켬)을 잡아 닫았다.

## 직전 상태 — Codex R2 (닫힘, `reviews/R2_LEDGER.md`)

2026-09-11 Codex 2차 리뷰(P1 9 · P2 1)와 내부 리뷰 L2·L5 를 합친 20 항목이
`reviews/R2_LEDGER.md` 에 있고, **닫는 순서**가 거기 적혀 있다. 여기서는 되풀이하지
않는다 — 그 파일의 "닫는 순서" 1~7 을 위에서부터 진행하고, 끝난 항목은 그 표의
"상태" 열을 갱신한다.

가장 아픈 셋: (C1) 대조 실험이 LAM_PE 쪽에서는 원통형 패턴을 **재현**한다 — "대체는
원인이 아니다" 는 LLI 에만 성립 · (C2) 측정 음극은 목적함수가 **소비하지 않는다** —
"35.77 mV 를 지웠는데도" 강도 논증 무효 · (C3·C4) MATLAB 대조기가 비교 안 한 값도
"전부 일치" 로 찍는다 — 192 값 대조를 고친 비교기로 **다시 돌려야** 한다.

Codex 반례 재생: `python3 reviews/r2_repros/harness_r2_replay.py --target $(pwd) --output /tmp/r.json`.

**2026-09-11 저녁 기준 — 원장 20 항목 중 코드·문서 쪽은 닫혔다 (a8084ec, 이 커밋).**
남은 것은 사용자 기계에서 몇 분이면 되는 실측 셋과, 그 뒤 R3 요청문이다:

```bash
cd ~/dd/bms-balancing && git pull --rebase origin claude/bms-alpha-beta-verify
source .venv/bin/activate && export BMS_DATA_ROOT='/mnt/d/가형 관련/degradation mode'
# ① PE 축 개입 강도 (§1-12 조건 7) — 초 단위
python3 scripts/ne_shape.py
# ② interp 가드가 실데이터에서 켜지는가 (L0-7) — 각 수 초. 에러가 나면 그 자체가 발견이다
python3 -m bms_balancing.verify eval --state 100 --si-source Li
BMS_DATA_ROOT=~/dd/cells/c168 python3 -m bms_balancing.verify eval --state 100 --si-source Li
BMS_DATA_ROOT=~/dd/cells/c171 python3 -m bms_balancing.verify eval --state 100 --si-source Li
BMS_DATA_ROOT=~/dd/cells/pouch_fixedhc python3 -m bms_balancing.verify eval --state 100 --si-source Li
git add out/ne_shape_GITT_Li.csv* && git commit -m "ne_shape 재실행 — PE 축 변화량 추가" && git push
```
그 결과로 §1-12 조건 7 을 채우고(PE 강도), 가드가 켜졌으면 원통형 산출을 재검토한다.

## 닫힌 것

| | 어디 | 한 줄 |
|---|---|---|
| 포팅 forward model | §1-0 · §1-8 | MATLAB↔Python 192 값, 최대 4.04e-12 |
| 툴박스 vs 우리 shim | §1-7 | `rmse_dqdv` 1.78e-12 — `sgolayfilt` 에서 생겨 dQ/dV 가 증폭 |
| 최적화 절차 | §1-9 | 자유 조합 최대 0.17 %p. 갈린 두 점에서 이긴 건 **그들** |
| 97 행 원표 | §2 · §2-1 | `out/bms97/` 커밋. 음수 LAM 이 경계 산물이라는 것을 **산술로** |
| 상태 일반화 | §1-10 | 파우치 네 상태에서 LAM_NE 최광 · LLI 최협 (4/4). **절대 폭으로 말할 때만** |
| **셀 일반화** | **§1-12** | **넘어가지 않는다** — 기술적 결과만. 원통형 LLI 하한 폭이 raw 로 max/max 10.5 배; 파우치 PE 고정 실험은 그 폭을 만들지 않았으나 LAM_PE 에서는 원통형 패턴을 재현 (R2 정정). 외곽 범위는 원통형에서 LAM_PE 분리·LAM_NE·LLI 겹침 (공유 가능값 미확정). 잔차 증가는 관측, 원인 미확정 (R3-01) |
| 문서↔산출 정합 | `cb23dbf` | 여섯 문서 중 넷이 뒤처져 있었다. drift 테스트 둘로 고정 |

## 열려 있는 것 (셀 말고)

- ~~dQ/dV 항의 로컬 함수 둘은 전사다 … 규진팀이 눈으로 맞춰 주면 닫힌다~~ → **닫힘**
  (U1, §1-13): 사용자가 원본을 직접 열어 네 로컬 함수 전부를 줄 단위로 댔다 — 일치
  (lower_half_mean 은 빈-표본 가드만 다름).
- **pOCV 가 원자료인지 필터본인지 모른다** (U2). 한 곡선으로는 원리적으로 못 가른다
  (§`verify noise`). 두 해석을 다 적어 뒀다. 이제 원자료를 우리가 갖고 있으므로 워크북의
  간격 균일성 검사로 닫을 수 있다 (사용자 기계, 선택).
- **γ 직접 적합(표현력)·공유 가능값 증인** (U9) — 미구현. 새 모델 요구서의 구분 시험 항목.
- **held-out 예측 없음.** 다른 셀의 **독립** 반쪽전지가 있어야 한다.
- **`CODEX_REVIEW_REQUEST.md` 2차 판을 아직 안 썼다.** 1차 판은 배너로
  인용 금지를 박아 뒀고 상한 자리마다 `→` 갱신을 달았다. 셀 축이 닫히면 새로 쓴다.

## 기계 쪽 사실 (잊기 쉬운 것)

- 작업본은 **`~/dd/bms-balancing`** (브랜치 `claude/bms-alpha-beta-verify`).
  `~/bms/bms-balancing` 은 본체 브랜치 체크아웃이니 **건드리지 않는다.**
- `BMS_DATA_ROOT='/mnt/d/가형 관련/degradation mode'` — 원자료는 저장소에 안 넣는다.
- MATLAB 은 `cd 'D:\가형 관련\degradation mode'` → `addpath('dd_shims','-end')`
  → `dd_verify('check')`. `-end` 없으면 진짜 툴박스 함수까지 가린다.
- 툴박스는 2026-09-10 에 전부 깔렸다. "없어서 못 한다" 는 더 이상 사유가 아니다.
- ⚠ **그 기계의 clone 루트는 `~/dd` 다.** 그래서 `~/dd/cells/` 가 **저장소 안**에
  있고, 그 안에는 규진팀 원자료 xlsx 사본이 들어간다. 저장소는 public 이다.
  `.git/info/exclude` 에 `cells/` 를 넣어 막아 뒀지만 그건 그 clone 에만
  적용된다. 루트 `.gitignore` 는 본체 소유라 못 고쳤고 `HANDOFF_TO_GATE.md`
  §2b 에 신고했다. **루트에서 `git add -A` 를 치지 않는다.**
