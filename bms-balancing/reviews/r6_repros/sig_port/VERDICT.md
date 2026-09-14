# VERDICT — sig_port 렌즈(F1…F11) 적대적 재검증 · 대상 1049894 · 격리 worktree `verify_sig/wt`

기준선(worktree, 이 세션 실측): `python3 -m pytest tests/ -q` → **87 passed in 34.74s** (`pytest.log`). 재현 스크립트: `verify_sig.py`(F1·2·4·5·7·9·10·11, 로그 `verify_sig.log`), `f3_cross_build.py`, `f6_crlf.sh`(`f6_crlf.log`), `f8_flock.sh`(`f8_flock.log`). 합성 자료는 `gen_synth_xlsx.py` 로 `data/` 에 재생성(렌즈 트리는 읽기만). 심각도 기준: 결론이_바뀜 = FINDINGS 판정 변경 · 숫자가_바뀜 = 저장된 산출/인용 숫자가 기록된 서명으로 재현 불가 · 서술만_바뀜 = 문서 문장/전제 추가 필요 · 사소 = 위생.

| ID | 판정 | 심각도 | 한 줄 이유 | 원장 겹침 |
|---|---|---|---|---|
| F1 | CONFIRMED | 사소 | `root=`가 basename: `degradation mode`→`\S+`로 `degradation`, `cells/c168`·`cells_v2/c168` 동일 라벨, `.`; 단 test_u13 head 정규식은 여전히 매치·어떤 테스트도 root 를 안 읽어 판정·숫자 영향 0 | R5-09(식별자 5 필드)의 잔여; 미기재 |
| F2 | 부분 | 사소 | 위조 사본(distinct 6줄·역순)이 실제 test_u13 통과 → **테스트**는 4 루트를 증거 못 함(재현); 그러나 §1-13·test docstring·사본 헤더 3행이 이미 "루트는 보고 순서로만" 이라 적음 → "한정 없이 적음" 주장은 반증 | R5-09 닫힘(정정)이 바로 이 증거 수준 |
| F3 | CONFIRMED | 숫자가_바뀜 (끝자리 · 결론 불변) | scipy 1.17.1↔1.11.4: savgol 13/500 ULP, dqdv scale 1 ULP, L-BFGS-B nit 25↔27 · fun 상대 1.2e-9 · x[2] 1.5e-5 차; `eval` 값 sha 동일. requirements 고정 0개, meta/JSON 에 버전 필드 0 | 미기재 |
| F4 | CONFIRMED | 서술만_바뀜 | 이름순 첫 xlsx 선택·다른 scale 재현, CSV/JSON/meta 14 키 어디에도 워크북 이름 없음, README 전제 없음; 단 **조용하지 않음** — stderr `[data] 후보 2개` 경고(`.log` 로 감), matlab 테스트가 그 규칙을 검사 | **R6 Q4 가 정확히 이 항목을 질문**(풀셀 워크북 누락?) |
| F5 | 부분 | 사소 | (a) profile_scale 이 CSV/meta 에 없음·같은 run_id 로 obj 0.8895↔1.2542 재현, 단 run_states 는 stdout→`.log` 캡처·`--profile-scale` 안 씀; (b) JSON 에 samples/grid 없음 재현(run_states 는 `--grid 21 --samples 400` 고정); (c) matrix 행에 starts 없지만 **meta 에 `starts` 있음**; (d) seed 리터럴은 세 명령줄 `--seed 0` 과 같은 파일의 상수 → 반증 | R5-07·R5-08 과 다름; 미기재 |
| F6 | CONFIRMED | 서술만_바뀜 | 274f1f8^ autocrlf 사본→1049894: run_all.sh `w/crlf`, `git status` clean, bash rc=2; 잔류 CRLF 522 파일(`*.m` 포함) 로 run_all.sh 만 고쳐도 `'bash\r'` 실패 1; fresh clone(요청문 §0 경로)은 `w/lf`·전부 통과. **렌즈 수정 힌트(`add --renormalize`)는 안 고쳐짐** | R4 원장 "CRLF → .gitattributes 닫힘" 의 잔여 |
| F7 | CONFIRMED | 사소 | cwd 3종에서 dirty False/True/None 재현; 방향이 보수적(false-dirty·unknown, false-clean 없음); run_states 는 `cd "$HERE"` 고정, ne_shape.py:162 만 노출 | R4-07 의 cwd 가장자리; 미기재 |
| F8 | CONFIRMED | 사소 | flock 부재: `.part` 고아·json 없음·오진 메시지·`.log` 에 원인 없음·rc=1(시끄러움), 대조 rc=0; flock 은 util-linux 표준 | R5-04 설계; 미기재 |
| F9 | 부분 | 사소 | (a)(b)는 `PYTHONUTF8=0 PYTHONCOERCECLOCALE=0` 까지 꺼야 재현 — `LC_ALL=C` 만으로는 PEP 538 강제로 rc=0 "일치"; (c) cp1252 stdout 은 **비ASCII basename** 에서만, 사용자 루트 basename `degradation mode` 는 rc=0·out 작성 | R5-11 과 다른 축; 미기재 |
| F10 | CONFIRMED | 사소 | ENOLCK → OSError 전파, `.part` 삭제·`.lock` 만 남음(재현); 시끄러운 실패·재계산 가능; FS 전제 문서 0(요청문 23행 "Linux/WSL" 만) | R5-04; 미기재 |
| F11 | CONFIRMED | 사소 | collect 87 · 87 passed vs 요청문 23·40행 "86 passed" · WORKING_STATE 42행; 요청문 최종 수정 커밋 = 1049894(test_u13 추가 커밋); `.gitignore` 에 `*.lock` 없음(실행마다 `<산출>.lock` 잔류), 단 provenance 는 `--untracked-files=no` 라 meta 무영향 | 미기재 |

## 발견별 실측

### F1 — `verify_sig.py` §F1
`# scale_audit,root=degradation mode state=pristine source=GITT si=Li seed=0 n=50; …` · `test_u13 head.search: ('pristine','GITT','Li','0','50')` · `root=(\S+) -> degradation` · `cells/c168 vs cells_v2/c168 label: 'c168' 'c168' SAME` · `--data-root . : # scale_audit,root=. state=…`. 코드 `verify.py:916` `root_label = Path(str(root)).name or str(root)`. 판정: 재현되나 라벨은 정보용 — 판정·숫자·테스트 어디에도 안 쓰임 → 사소. 힌트: F4 와 묶어 sha256/resolve 경로(따옴표) 로.

### F2 — `verify_sig.py` §F2 (임시 ROOT + 실제 테스트 함수)
`forged: 18 lines, distinct: 6 (GITT/Li lines = first occurrence per state, x4, reversed)` → `real test_u13 on forged copy: PASSED`. 반증 근거(원문): FINDINGS §1-13 "**루트 이름은 그 판의 줄에 없어 보고 순서의 4 블록으로만 안다** — 다음 판부터 `root=` 가 붙는다"; test docstring "루트 차원은 아직 줄에 없다 — 보고 순서로만 안다 (§1-13 이 그렇게 적어야 한다)"; 테스트가 §1-13 에 `"루트"`·`"보고 순서"` 존재를 assert; 사본 헤더 3행 `## 순서: BMS_DATA_ROOT=파우치 원자료 × (pristine 100 200 300_0009) …`. 즉 문서는 이미 한정을 달았고 발견은 "테스트가 그 한정 이상을 증거하지 못한다" 뿐 → 부분/사소. 힌트: 없음(다음 판 root= 실측 때 distinct root ≥ 4 를 세는 assert 추가).

### F3 — `f3_cross_build.py` (worktree 코드, 두 인터프리터)
```
numpy 2.4.6 scipy 1.17.1  dqdv 0x1.72ef730443448p-2  obj(P) 3cc02daadf2ba746  L-BFGS-B nit 25 fun 0.88953156550576173 x[2] 1.043783821 x[3] -0.08180187783
numpy 1.26.4 scipy 1.11.4 dqdv 0x1.72ef730443449p-2  obj(P) 3cc02daadf2ba746  L-BFGS-B nit 27 fun 0.8895315640685143  x[2] 1.043768311 x[3] -0.08180118346
savgol max|diff| 8.88e-16 n_diff 13/500 · requirements pins(==,~=,<): 0 · __version__/python_version/platform in run_states.sh·verify.py·provenance.py: 0
```
등급 근거: `eval` 계열(U13 감사 줄, `.3g` eps_rel, DD_EVAL_P 값) 은 인쇄 정밀도에서 불변; 최적화 계열(matrix·profile·degeneracy) 은 17자리 인쇄값이 버전에 따라 다르고 어떤 필드도 버전을 안 남김 → 재현 실패 시 원인 특정 불가. 차이는 tol 1% 의 1e-3 이하 → 결론 불변. 힌트: meta+JSON 에 `python/numpy/scipy/pandas/platform`, 요청문 §1 에 검증 조합 명시(pin 은 선택).

### F4 — `verify_sig.py` §F4
`candidates before: ['fullcell_states.xlsx']` → 복사본 추가 후 `chosen: 'fullcell_states - 복사본.xlsx' | stderr warning: [data] 풀셀 워크북 후보가 2개다 — 이름순 첫 것을 쓴다: fullcell_states - 복사본.xlsx (나머지: fullcell_states.xlsx)` · `scales pocv 0x1.1f09efa37f3c7p-3 -> 0x1.f7a9eeeee82d0p-4` · `eval csv header: # dd_eval  state=100  halfcell=data/half_cell/GITT/  Si=Li  w_dqdv=0`(워크북 없음) · `meta keys: artifact,state,half_cell_source,si_source,starts,seed,w_dqdv_note,data_root,run_id,git_*,created_utc` · `README/run_states/FINDINGS 워크북|workbook|xlsx 하나: False`. 반증 시도 결과: "조용히"는 아님(stderr 경고, run_states 에서는 세 명령 모두 stderr→`.log`); `matlab/tests/run_all.sh` 의 `OK 워크북 후보 여럿 → 이름순 첫 것` 이 설계된 규칙임을 보임. 그러나 `.log` 는 gitignore·미해시라 서명 밖이고 전제(폴더당 1개) 문서 0 → CONFIRMED 유지, 서술만_바뀜(§1-13/README 전제 + Q4 답). 힌트: `build()` 가 소비 파일 3종 이름+sha256 을 Objective 에 들고 JSON/CSV 헤더/meta 에; 후보 >1 이면 exit≠0 (또는 전제 문서화).

### F5 — `verify_sig.py` §F5
(a) `same header: True | run_id: RID-SAME RID-SAME | row0 obj: 0.8895315640684471 vs 1.2541806686130992 | LAM_NE_pct 2.564 vs 2.739`; `stdout SUMMARY has profile_scale: True`; run_states.sh:196 `run "profile …" … -` → stdout+stderr 가 `.log`(SUMMARY 포함), `--profile-scale` 미사용. (b) `keys differing 4 vs 40: [LAM_*_percent(_observed_cloud), n_accepted] | n_accepted 5 21`, samples/grid 키 없음; JSON 에는 `n_starts`·`seed`·`tol_percent_of_best` 있음; run_states.sh:180 `--grid 21 --samples 400` 고정. (c) `matrix has starts?: []`, 그러나 meta `"starts": int(starts)`(run_states.sh:64). (d) `seed literals: (64,'"seed": 0'), (180,'--seed 0'), (191,'--seed 0'), (200,'--seed 0')` → 같은 파일 상수 쌍, 어긋날 통로 없음. 등급: 파이프라인 산출은 스크립트 상수+meta 로 모호성 없음, 수동 실행 산출만 모호 → 사소. 힌트: profile 행에 `profile_scale`, JSON `config` 에 `n_samples`·`grid`, matrix 행에 `n_starts`.

### F6 — `f6_crlf.sh` / `f6_crlf.log`
```
stale (274f1f8^→1049894, autocrlf=true): i/lf w/crlf attr/text eol=lf  bms-balancing/matlab/tests/run_all.sh ; run_states.sh w/lf ; git status --short: (비어 있음)
bash run_all.sh: line 9: set: -: invalid option … line 15: $'\r': command not found … rc=2
git add --renormalize . && git checkout -- . → run_all.sh 여전히 w/crlf, 대신 'M am_scaffold.csv', 'M bms-balancing/out/matrix_300_0009.csv' 가 staged (렌즈 힌트 무효)
rm run_all.sh && git checkout -- run_all.sh → w/lf, 그러나 잔류 w/crlf 522 파일 → run_all.sh 실행 시 "/usr/bin/env: 'bash\r'" 로 실패 1 건
fresh clone @1049894 autocrlf=true: i/lf w/lf run_all.sh ; worktree run_all.sh: 전부 통과 rc=0
R6_REQUEST.md:24 = "bash matlab/tests/run_all.sh                      # Octave 없으면 4·5 단계" ; renormalize 언급 0
```
등급: 요청문 §0(20행) 은 `git clone` 을 지시하므로 문서 경로는 안전; R4 리뷰어의 기존 사본을 pull 하는 경로만 해당 → 서술만_바뀜(§0 에 한 줄). 힌트: "기존 autocrlf 사본은 `git rm -r --cached . && git reset --hard`(또는 새 clone)". `add --renormalize` 는 쓰지 말 것(실측 무효·CSV 오염).

### F7 — `verify_sig.py` §F7 (`--shared` clone, `out/matrix_300_0147.csv` 에 개행 추가)
`cwd=bms-balancing git_dirty=False code=[] outputs=['out/matrix_300_0147.csv']` · `cwd=repo-root git_dirty=True code=['bms-balancing/out/matrix_300_0147.csv'] outputs=[]` · `cwd=/tmp git_dirty=None`. 호출부: `run_states.sh:18 cd "$HERE"`(고정), `ne_shape.py:162 git_provenance(artifact=str(art))`(cwd 미고정, chdir 없음). 등급: 오분류 방향이 dirty 쪽(보수적) → 사소. 힌트: `base = Path(__file__).resolve().parents[1]`, `_git(cwd=base)`.

### F8 — `f8_flock.sh` / `f8_flock.log` (verify 3 명령을 run_id 박는 shim 으로 대체, PATH 에서 flock 제거)
`scripts/run_states.sh: line 181: flock: command not found` → `<OUT>/degeneracy_100_Li.json: run id (a798…) 가 산출물의 필드에 없다 — 이번 시도의 산출이 아니므로 meta 를 쓰지 않는다` · out: `.degeneracy_100_Li.part … matrix_100.csv.meta.json profile_gamma_100_Li.csv …`(json 없음) · `'flock' in degeneracy .log: 0` · `실패 1 건` rc=1; 대조(flock 있음) `전부 통과` rc=0. `command -v flock` 가드 0. 등급: 실패는 시끄럽고 진단만 오도 → 사소. 힌트: 상단 `command -v flock >/dev/null || { say 'flock(util-linux) 필요'; exit 1; }`.

### F9 — `verify_sig.py` §F9
`LC_ALL=C only (PEP538 coercion on): check_artifact rc=0 | check-run-id rc=0 일치` · `LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0: rc=1 | rc=1 UnicodeEncodeError` · `PYTHONIOENCODING=cp1252 kr basename '가형 관련': rc=1 out_written=False` · `… basename 'degradation mode': rc=0 out_written=True` · `run_states.sh sets PYTHONUTF8/LC_ALL: []`. 사용자 루트(WORKING_STATE:41) `/mnt/d/가형 관련/degradation mode` → basename ASCII. 등급: 재현에 Python 기본 보호를 명시적으로 꺼야 함 → 사소. 힌트: 두 `open()` 에 `encoding="utf-8"`, `export PYTHONUTF8=1`.

### F10 — `verify_sig.py` §F10
`raised: [Errno 37] No locks available` · `files left: ['profile.csv.lock']` · 문서 NTFS/ext4/flock 언급: README·FINDINGS·WORKING_STATE 0, R6_REQUEST:23 "(동시 실행 시험 셋은 subprocess·flock 사용, Linux/WSL)". 등급: 시끄러운 실패, 재계산 가능 → 사소. 힌트: 잠금 실패 시 `.part` 보존 + 경로 출력.

### F11 — `verify_sig.py` §F11 · `pytest.log`
`collect-only items: 87` · `87 passed in 34.74s` · `R6_REQUEST.md '86 passed' lines: [23, 40]` · `WORKING_STATE.md: [42]` · `last commit touching R6_REQUEST.md: 1049894 | test_u13 added in 1049894: True` · `.gitignore has .lock: False | .lock left: ['m.csv.lock','p_global.csv.lock','p_per-gamma.csv.lock']` · provenance `--untracked-files=no`. 본 checkout 에는 현재 untracked `.lock` 없음(렌즈의 3개는 일시적). 등급: 사소. 힌트: 세 곳 87 로, `.gitignore` 에 `out/*.lock`.

## CONFIRMED — 수정 우선순위
1. **F3** meta·JSON 에 `python/numpy/scipy/pandas/platform` 기록, 요청문 §1 에 검증 조합 명시 (숫자가 갈리는 유일한 축).
2. **F4** `build()` 소비 입력(반쪽전지·풀셀·문헌) 이름+sha256 → JSON/CSV 헤더/meta; 후보 >1 exit≠0 또는 README 전제; R6 Q4 답을 요청문에.
3. **F6** 요청문 §0: "기존 autocrlf 사본은 `git rm -r --cached . && git reset --hard` 또는 새 clone" (`add --renormalize` 아님).
4. **F11** "86 passed" 3곳 → 87; `.gitignore` `out/*.lock`.
5. **F8** `command -v flock` 가드 + 고아 `.part` 경로를 메시지에.
6. **F7** `git_provenance` 기본 cwd 를 `parents[1]` 로 고정.
7. **F1** 감사 줄 root 를 sha256/resolve 경로(따옴표) 로 (F4 와 같이).
8. **F10** 잠금 실패 시 `.part` 보존.
9. **F5(a)(b)** profile 행 `profile_scale`, JSON `n_samples`·`grid`, matrix 행 `n_starts`.

## 반증됨 / 하향
- **F2**: 테스트의 증거 한계는 재현되지만 "§1-13 이 한정 없이 4 루트로 적음" 은 반증 — §1-13·docstring·사본 헤더가 이미 "보고 순서로만" 명시(R5-09 정정 그대로) → 부분/사소.
- **F5(d)** seed 리터럴: 같은 스크립트의 `--seed 0` 상수 3곳과 쌍 → 반증. **F5(c)** matrix starts: meta 에 있음 → 부분. 전체 숫자가_바뀜 → 사소 (파이프라인 산출은 스크립트 상수+meta+`.log` 로 모호성 없음).
- **F9**: `LC_ALL=C` 단독은 통과(PEP 538); cp1252 크래시는 비ASCII basename 한정, 실제 루트 basename ASCII → 부분/사소.
- **F4** "조용히" 하향: stderr `[data]` 경고 + matlab 테스트가 규칙 검사; 숫자가_바뀜 → 서술만_바뀜 (Q4 가 이미 제기).
- **F6** 렌즈 수정 힌트 `git add --renormalize . && git checkout -- .` 는 실측 무효(run_all.sh 그대로 CRLF, CSV 2건 staged) — 힌트 교체 필요.
- **F7·F8·F10·F11·F1**: 재현되나 판정·숫자 무영향 → 사소로 하향.
