# R6 validator 렌즈 — 적대적 검증 판정 (대상 `1049894`, 격리 worktree `wt_verify_validator`, 2026-09-11)

재현: `python3 verify_r6.py [v01…v09|raw]` (이 디렉터리; worktree 를 지웠으면 `git worktree add --detach wt_verify_validator 1049894` 로 다시 만든다).
fixture 는 전부 **내가 새로 쓴 것** (`fixtures/`: 앵커 값 0.5+0.07n · dv_n 412 · MATLAB = Python × 1.015 = **상대차 1.50 %**, 32 값 전부 `%.2g` 로 `0.045`).
CLI 는 `tests/test_review_findings.py::test_r3_07` 과 같은 mock driver(`driver.py`)로 별도 process 에서 `verify.main(["eval","--compare",…])` (cwd = worktree `bms-balancing/`; 원 CLI 는 `BMS_DATA_ROOT` 없이는 SystemExit — `raw` 케이스).
전체 출력 사본: `run_output.txt`. 기존 테스트: `python3 -m pytest tests/ -q` → **87 passed (38 s)** — 아래 9 건 어느 것도 기존 테스트에 안 잡힌다.
렌즈가 인용한 "형식은 맞는데 의미가 틀린 산출물이 통과하면 안 된다" 는 README·FINDINGS 어디에도 **없는 문장**이다 (grep 0건). 실제 명문은 README:59 (invalid 목록 · 옵션→선언→추정 · R5 Q1 예외) 와 FINDINGS §1-8 R4/R5 문단 ("해석 못 하는 선언은 invalid(종료 2)", "audit 이 토큰을 선언 형식으로 다시 찍어 일치 확인").

## 표

| ID | 판정 | 내 심각도 | 한 줄 이유 | 원장 겹침 |
|---|---|---|---|---|
| V6-01 | **CONFIRMED** | **결론이_바뀜** | 헤더를 데이터 아래로 옮기면 **옵션 없이** `%.2g` 선언 + 17자리 토큰 + 1.5 % 차이가 rc 0 complete (헤더 위면 rc 2). 어떤 writer 도 그 순서로 안 쓴다 — 손으로 만든 파일이지만 R4-04·R5-01 의 반례도 전부 손으로 만든 파일이었다 | R5-01(재출력)·R4-04(열 수) 가 붙인 검사 **그 자체가 안 도는** 순서 — 미커버 (실측 rc 0) |
| V6-02 | **CONFIRMED** | 결론이_바뀜 (옵션 명시 시) | 선언 없음/`%.17e`/`17` + `--precision sig:2` → rc 0; 같은 옵션이 `%.17g` 선언 파일에선 rc 3. auto 는 rc 1 로 fail-closed. 옵션이 **선언**보다 느슨하면 막고(R4-02 ④) **토큰**보다 느슨한 건 안 막는 역전 | R4-02 ④/Q3 은 선언된 파일만 (CTRL rc 3 로 닫힘 확인); 선언 없는/못 읽는 파일 미커버. R5 Q1 예외는 "옵션이 대체" 를 명문화했지 "느슨해도 됨" 은 아님 |
| V6-03 | **CONFIRMED** | 결론이_바뀜 (`--allow-partial` 시) | 헤더 없음 + `%.2g` 선언 + 17자리 토큰 → 3 → `--allow-partial` 로 0 (열 2/4, 1.5 % 차이). 헤더 없는 산출은 첫 판 56a35a8:118 부터 **존재한 적 없다** — 죽은 경로. 정직한 `%.17g` 선언이면 rc 1 (거짓 선언이 전제) | R5-03·R4-04 는 헤더가 있어야 동작; R2-01 은 compared 16/16 라 통과. 미커버 |
| V6-04 | **CONFIRMED** | 결론이_바뀜 (`--allow-partial` 시) | rmse 열 0 개 → 3 → `--allow-partial` 로 0; 앵커까지 없으면 "앵커 0개와 rmse 0개가 전부 일치" 로 0 (`compared=0/0`). 옛 스키마 최소는 rmse 2 열 + 앵커 10 (56a35a8, §1-8) | R2-01 은 expected=compared=0 에서 공허하게 통과; R4-02 는 "스키마 누락" 으로 한정했으나 하한 없음. 미커버 |
| V6-05 | **CONFIRMED** | 숫자가_바뀜 (사후 rename 한정) | write_meta 모양 meta(`artifact=matrix_100.csv, state=100`)를 `matrix_200.csv` 옆에 복사 → `--verify-unit` rc 0 '일치'; `check_artifact` 도 통과; matrix 행에 `state` 열 없음. **실제 `out/` 쌍 31 개는 전부 pre-R5 meta 라 rc 1 '옛 meta'** — 파이프라인 안에서는 재현 불가 | R5-04 는 (run_id, sha256) 묶음만 — 이름 결속 미커버 |
| V6-06 | **CONFIRMED** | 서술만_바뀜 | `# printed_format,17` → 선언 없음으로 취급: auto rc 3 "추정"(문서는 invalid·2), `read_dd_eval_csv` 는 앵커 `printed_format=17.0` 으로 읽음, `--precision sig:2` 면 "해석 불가" 표시 없이 rc 0 (텍스트 선언 `seventeen` 은 표시함). 둘 다 fail-closed(auto) | R5-02 는 이름으로 역할을 정하되 **값 검증은 meta 리더**에 남겨 숫자 값이 새는 구멍; R4-02 "해석 불가 → invalid" 미적용 |
| V6-07 | **CONFIRMED** | 서술만_바뀜 | 없는 경로/디렉터리 → FileNotFoundError/IsADirectoryError traceback, rc 1 = README 의 "갈림". "종료 코드" 줄 없음. 성공으로는 안 읽힘 | R3-07 매핑 밖의 예외. 미커버 |
| V6-08 | CONFIRMED | 사소 | `run_id` 열 둘 → DictReader 마지막 열만 (`{'run_id': 'aaa…'}`); `atomic_write_csv` 는 dict 키라 중복 생성 불가 — 손 편집 전용 | R5-08 은 grep→필드까지; 유일성 미검사 |
| V6-09 | **부분** (함수 수준만) | 사소 | `token_excess(fixed6, 0.0, -1e-20)` = 1e-20 → eff 1 은 사실이고 강제로 넣으면 rc 1. 그러나 rmse = `sqrt(mean(r²))` (model.py:348·352·372) 라 **음수·-0.0 rmse 는 양쪽 다 생산 불가** → 비교기 수준에선 도달 불가; 현 writer 는 `%.17g`(exact 경로, 이분법 없음) | R5-01 "0 은 정확히 0 만" 의 `%f` 부호 경계 — 도달 불가라 열림 아님 |

## 발견별 실측 (명령은 전부 `verify_r6.py` 의 해당 함수; 발췌는 `run_output.txt` 그대로)

### V6-01 — `v01()`
```
header top   : rc=2   - 행 0 rmse_pocv 토큰 '0.045218249999999995' 이 선언 형식(.2g)으로 찍은 '0.045' 와 다르다 | 종료 코드 2 (invalid)
header bottom: rc=0  판정: 앵커 16개와 rmse 32개가 **적힌 자리수 안에서 전부 일치**. | 종료 코드 0 (complete)      audit(spec sig:2) = []
10-field row before 9-col header: audit = []   (비교기는 행 수 9≠8 로 incomplete — 열 수 검사가 잡은 게 아니다)
```
반증 시도: writer 순서 — `matlab/dd_eval.m:210-211` (hdr → rows), 첫 판 `56a35a8:118-119` (hdr → rows), `mirror_dd_eval.py:188` (hdr 먼저), `cmd_eval --out` (verify.py:936-941 hdr 먼저). **헤더 뒤 데이터를 쓰는 writer 는 없다.** 그래도 CONFIRMED: R5-01 의 보증("토큰을 선언 형식으로 다시 찍어 일치 확인")이 `header is not None` (verify.py:618·624) 에 걸려 스캔 순서로 무력화되고, 옵션 없이 rc 0 이다. 9 건 중 **유일하게 기본 호출로 0** 이 나오는 건 — 렌즈의 2 순위를 1 순위로 올린다.

### V6-02 — `v02()`
```
no decl, auto                 : rc=1  … rmse 가 갈린다 (최대 상대차 1.50e-02) | 종료 코드 1 (model_mismatch)
no decl, --precision sig:2    : rc=0  판정: 앵커 16개와 rmse 32개가 **적힌 자리수 안에서 전부 일치**. | 종료 코드 0 (complete)
no decl, --precision fixed:0  : rc=0   /  decl %.17e, --precision sig:2 : rc=0   /  decl '17', --precision sig:2 : rc=0
CTRL decl %.17g, --precision sig:2: rc=3 (partial)   /  CTRL decl %.17g, auto: rc=1
branch verify.py:1020  malformed = dd_eval_csv_audit(matlab_csv, spec=policy["declared_spec"])   ← 옵션 spec 은 안 넘긴다
branch verify.py:1116  if policy["conflict"] and policy["declared_spec"] is not None and token_excess(declared) > token_excess(sp): override_looser
resolve_precision(undecl,'sig:2') → source='option', declared_spec=None, conflict=False
```
반증 시도: 문서화된 규칙은 있다 — README:59 "옵션 → 선언 → 추정", "해석 못 하는 선언은 `--precision` 을 명시하면 옵션이 대체 (R5 Q1)". 그러나 같은 줄이 "옵션이 선언보다 느슨해도 complete 아님" 을 말하고, R5 Q1 원문(R5_CODEX.md:281)은 `g17` 대체 사례다. `precision_override_looser` 는 정말 `policy["conflict"]` 에서만 (1116) → 선언 없으면 conflict=False. 실측 rc 0 → CONFIRMED. 심각도는 **옵션을 명시해야** 열리고 auto 는 rc 1 이라 "(옵션 명시 시)" 한정.

### V6-03 — `v03()`
```
no header, auto            : rc=3  판정(부분 — 앵커 16/16 · 열 2/4): … 전부 일치 | 종료 코드 3 (partial)
no header, --allow-partial : rc=0  … 종료 코드 0 (partial — `--allow-partial` 로 옛 스키마의 부분 대조를 허용했다)   audit(sig:2)=[]
CTRL no header, decl %.17g, --allow-partial: rc=1 (model_mismatch)
history: first commit 56a35a8 → fprintf(fid, 'a_PE,b_PE,a_NE,b_NE,gamma_Si,rmse_pocv,rmse_dvdq\n');  committed dd_eval CSV 4/4 헤더 있음
```
"헤더 없는 아주 옛 산출" (verify.py:1064-1065) 은 git 이력에 없다. `--allow-partial` 의 문서 의미(README:59·--help)는 "옛 스키마(앵커·열 누락)" — 존재한 적 없는 스키마를 옛 스키마로 분류한다. 전제 셋(헤더 없음·거짓 선언·플래그)이 다 필요.

### V6-04 — `v04()`
```
5 param cols + 16 anchors, auto           : rc=3  (열 0/4): 앵커 16개와 rmse 0개가 … 전부 일치
5 param cols + 16 anchors, --allow-partial: rc=0
5 param cols, NO anchors,  --allow-partial: rc=0  판정(부분 — 앵커 0/16 · 열 0/4): 앵커 0개와 rmse 0개가 **적힌 자리수 안에서 전부 일치**.
direct(params only): status=partial compared=0/0 anchors=0/16
```
"0 열 → 0" 은 `--allow-partial` 로만 (auto 는 3). 옵션 문서가 허용한 건 "누락" 이지 "전부 누락" 이 아니다 — 아무것도 비교 안 한 파일에 종료 0.

### V6-05 — `v05()`
```
(a) REAL out/matrix_300_0147.csv(+meta) → matrix_200.csv : --verify-unit rc=1 '옛 meta (run_id/sha256 없음)'
(b) synthetic write_meta-shaped meta (run_states.sh:62-69 필드 그대로): --verify-unit matrix_100.csv rc=0 '일치'; 복사본 matrix_200.csv rc=0 '일치' (meta.artifact='matrix_100.csv', state='100')
(c) run_states.sh check_artifact one-liner on renamed copy → rc=0
```
`verify_unit` 은 `m["run_id"]`·`m["sha256"]` 만 (provenance.py:129); `write_meta` 는 `artifact`·`state` 를 적는다 (run_states.sh:63). 파이프라인은 같은 경로로 run→write_meta→verify-unit 이라 **안에서는 안 생기고**, 사후 `cp` 만. 그래서 숫자가_바뀜이되 한정.

### V6-06 — `v06()` (토큰 = Python, 차이 0 으로 status 만 분리)
```
resolve_precision: source='inferred' declared_raw=None; read_dd_eval_meta={}; read_dd_eval_csv anchors['printed_format']=17.0; audit=[]
auto: rc=3 (partial … 정밀도)      --precision sig:2: rc=0  label=(정밀도: --precision sig:2)
CTRL 'seventeen' auto: rc=2 (invalid)   CTRL 'seventeen' --precision sig:2: rc=0 label=(… 파일 선언 `seventeen` 은 해석 불가 — 옵션을 적용)
```
FINDINGS §1-8 R4 "해석 못 하는 선언은 invalid(종료 2)" 와 어긋난다 (3). 성공은 아니므로 서술만.

### V6-07 — `v07()`
```
missing file: rc=1  FileNotFoundError: [Errno 2] …  '종료 코드' printed: False      directory: rc=1  IsADirectoryError
```
`cmd_eval` 은 ValueError 만 (verify.py:955); `Path.read_text` (552) 의 OSError 가 traceback → Python 기본 1 = README "1 갈림".

### V6-08 — `v08()`  `check_run_id(rid=last col) → (True, '전 행 일치')`, `(rid=first col) → (False, …)`, DictReader row `{'run_id': 'aaa…', 'half_cell': 'GITT'}`. 저장소 writer 는 dict 키 → 중복 불가.

### V6-09 — `v09()`
```
token '0.000000' vs pv=-1e-20: excess=1e-20 eff=1 (MODEL_REL=1e-09);  token '-0.000000' vs +1e-20: excess=1e-20;  CTRL '0.000000' vs +1e-20: excess=0
comparator (%.6f, 한 칸 MATLAB 0.000000 vs Python -1e-20 강제): rc=1 (model_mismatch, 최대 상대차 1.00e+00)
reachability: sqrt(mean(zeros²)) → 0.0 → '0.000000'
```
산술은 맞다. 그러나 토큰 검사 대상은 rmse 열뿐이고 rmse 는 양쪽 다 `sqrt(mean(r²))`(제곱합 ≥ +0.0) 라 음수·-0.0 이 나올 수 없다 → **부분**: 함수 수준 재현, 비교기 수준 도달 불가.

## CONFIRMED — 수정 우선순위 (내 순서; 렌즈와 다른 점: V6-01 이 옵션 없이 0 이라 1 순위)

1. **V6-01 + V6-03** (audit 가 헤더 위치·유무에 의존): 원문 행을 모아 두고 헤더 확정 **뒤** 열 수·토큰 검사를 돌린다; 헤더 앞 데이터 행 → invalid; 헤더 없음 → invalid (verify.py:1064-1065 죽은 경로 제거). 회귀: 헤더 아래/없음 두 fixture 가 rc 2.
2. **V6-04** (`--allow-partial` 하한): `expected == 0 or anchors_compared == 0` → invalid; 허용 옛 스키마를 명시(`rmse_pocv`·`rmse_dvdq` 필수, 앵커 최소 10). 회귀: 열 0 / 앵커 0 fixture 가 `--allow-partial` 로도 ≠ 0.
3. **V6-02 (+V6-06)**: audit 을 유효 spec(`policy["spec"] or declared_spec`)으로 돌리고, 옵션 아래 재출력 실패면 partial "옵션이 토큰보다 느슨" (R4-02 ④ 와 대칭); `printed_format` 키는 값과 무관하게 meta 로 읽어 숫자 값도 해석 불가 → invalid.
4. **V6-05**: `verify_unit` 에 `m.get("artifact") == p.name` 한 줄 (state 는 shell 이 인자로 넘겨 대조).
5. **V6-07**: `cmd_eval` 에서 `except (ValueError, OSError)` → 2.
6. **V6-08**: `check_run_id` 헤더 `Counter` 중복 → False.

## 반증됨 / 하향

- **V6-09 → 부분·사소**: 함수 수준 산술은 재현되나 비교기에선 음수 rmse 가 필요해 도달 불가 (양쪽 구현 모두 `sqrt(mean(r²))`); 현 writer 는 `%.17g` exact 경로. 수정 불필요 (원하면 `-0.0` 토큰 정규화).
- **V6-05 하향 근거**: 실제 `out/` 31 쌍은 전부 pre-R5 meta(run_id/sha256 없음) → rc 1; 파이프라인 안에서는 재현 불가, 사후 rename 한정.
- **V6-02 한정**: auto 경로 rc 1 (fail-closed). 옵션을 명시한 조작자 경로에서만 0.
- **V6-06·V6-07 은 서술만**: 둘 다 종료 코드가 0 이 아니다 (3·1).
- 렌즈의 "README 정책 문장" 인용은 부정확 (없는 문장) — 판정에는 영향 없음 (실제 명문 README:59·§1-8 로도 같은 결론).
