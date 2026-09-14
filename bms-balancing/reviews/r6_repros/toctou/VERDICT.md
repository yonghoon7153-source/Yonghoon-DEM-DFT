# R6 자체 리뷰 — 순서/TOCTOU 렌즈 **검증자 판정** · `bms-balancing/` @ `1049894`

- 방법: 렌즈 스크립트는 읽기만 하고 **내 하네스** `verify_toctou.py` 로 전부 다시 재현했다 (격리 worktree, tracked 파일 무변경).
  가짜 `bms_balancing.verify` 는 계산 대신 신호 대기 + **실제** `verify.py` 의 `publish_lock`·`atomic_write_csv` 원문 슬라이스;
  shell 은 `run_states.sh` 의 helpers(write_meta·say·check_run_id·check_artifact·run)와 degeneracy 176-187 / matrix 189-194 블록 원문 슬라이스.
- 재실행: `./rerun.sh` (worktree 생성→`python3 verify_toctou.py all`→`run_all.log`→worktree 제거). 개별: `WT=<checkout>/bms-balancing python3 verify_toctou.py f01`.
- 기준선: `python3 -m pytest tests/ -q -k "r5_04 or r4_06 or r5_08 or r5_05"` → **`5 passed, 82 deselected in 21.17s`** — 여덟 발견 중 어느 것도 기존 테스트가 잡지 않는다.
- 부수 관측: 커밋된 `out/` 네 산출(degeneracy·matrix·profile_300_0147, ne_shape) 전부 `verify_unit → (None, '옛 meta (run_id/sha256 없음)')` — 인용 중인 artifact 는 R4-06/R5-04 장치 **이전** 것이라 아래 어느 발견도 지금 인용 숫자를 바꾸지 않는다.

## 표

| ID | 판정 | 심각도 | 한 줄 이유 | 모순되는 원장 문장 |
|---|---|---|---|---|
| F01 | **CONFIRMED** | **결론이_바뀜** | 실제 degeneracy 블록 두 process: A "전부 통과" rc 0 뒤 B 의 stdout fd 가 게시 파일을 덮어 JSON=B/meta=A(또는 깨진 JSON) — R5-04 "마지막 온전한 묶음" 이 이 경로에서 거짓 | R5_LEDGER R5-04 "실패면 meta 를 쓰지 않는다. `provenance --verify-unit` 이 게시 뒤 묶음을 확인" · run_states.sh:42 "마지막 실행의 온전한 묶음만 남는다" · R6_REQUEST §2 04 "정책: 동시 실행 허용, "마지막 온전한 묶음" 만 남음" |
| F02 | **CONFIRMED** | 서술만_바뀜 (렌즈 숫자가_바뀜 → 하향) | CSV=B·meta(consumed_inputs)=A, rc 0/0, `verify_unit=(None, 옛 meta)` 로 검출 불가 — 재현됨. 단 ne_shape 는 수동 1회 실행 스크립트(WORKING_STATE:87)이고 인용 숫자는 안 바뀐다 | R5_LEDGER R5-05 "`consumed_inputs`: 소비한 matrix 파일 경로·sha256·행" — 끼어들기 하나로 그 identity 가 CSV 를 만든 실행의 것이 아니게 된다 |
| F03 | CONFIRMED (기전) | 사소 | 400k 행 CSV 로 재현(행=옛 run_id, sha256=새 파일); 실제 `matrix_300_0147.csv` 5987 B 파싱 0.29 ms → 창 sub-ms | 없음 |
| F04 | CONFIRMED | 서술만_바뀜 | (i) dirty 로 계산 → 실행 중 checkout → meta `git_dirty=False`; (ii) 실행 중 커밋 → meta 가 새 SHA. 시각 필드 `created_utc` 하나 | 없음 (R4-07 은 무엇을 셀지, 언제가 아님) — meta 의 git_* 는 "meta 작성 시각의 트리" 라고 적어야 한다 |
| F05a | CONFIRMED | 사소 (렌즈 서술만 → 하향) | A 의 OK `[run_id A]` + "전부 통과" rc 0 이지만 디스크는 B/B — 디스크는 정책대로 온전, wrapper 보고만 stale | 없음 (R5-04 의 "A 거부" 는 다른 schedule 의 테스트 서술) |
| F05b | CONFIRMED | 사소 | `why` 는 stdout→`/dev/null`, 요약이 가리킨 `.log` 는 B 의 "wrote … (run_id B)" — 진단만 잃음, 최종 B/B | 없음 |
| F06 | CONFIRMED | 사소 | `check-ignore` rc 1: `*.lock`, `matrix_100.csv.ab12cd.part`, `…meta.ab12cd.part`; unlink 뒤 `flock -n` rc 0 (보유자 생존) — 실행 중 수동 삭제/`git clean` 이 전제 | 없음 |
| F07 | CONFIRMED | 서술만_바뀜 | 섞인 쌍(`verify_unit=False`)이 `compare_states.py` rc 0, 경고 0 으로 §1-10 표에 들어간다 — reader 절 미구현 | R5_CODEX.md:134 최소 조건 "reader도 두 ID/해시 불일치를 성공으로 소비하지 않아야 한다" vs R5_LEDGER R5-04 "**닫힘 (코드)**" |
| F08 | 부분 | 사소 | 복사한 id 로 X 게시 → A 의 잠금 안 재확인·verify-unit 통과, 재현됨. 그러나 문서의 위협 모델("다른 시도" 각자 uuid, 우연 끼어들기) 밖 — 소유 증명을 주장한 문장이 없다 | 없음 (R5-08 은 "grep → 필드" 만 주장) |

## 발견별 근거 (`run_all.log` 원문 발췌)

### F01 — `python3 verify_toctou.py f01` / `f01b`
코드 확인: `run_states.sh:176` `tmp="$OUT/.degeneracy_${st}_${SI}.part"` (state/si 당 **고정**), `:131` `"$@" > "$redir"` (redir=그 `.part`, O_TRUNC), `:181` `flock … mv "$tmp" …json`;
`verify.py:475` `print(json.dumps(out…))` 이 `cmd_degeneracy` 의 **유일한** stdout 쓰기(399-455 에 print 없음) → 계산 끝에 한 번.
```
A 끝남 rc=0 … 전부 통과 — 산출 3개, 전부 열어서 읽히는 것을 확인했다 / 설정: STATES='100' STARTS=4
A 뒤 디스크: 게시 JSON run_id=95083f5d role=A n_starts=4 | meta run_id=95083f5d starts=4 sha 일치=True verify_unit=(True, '일치')
B 끝남 rc=1 … 실패 1 건 — 위의 .log 를 볼 것
최종 디스크: 게시 JSON run_id=6216cf8f role=B n_starts=24 (637 B) | meta run_id=95083f5d starts=4 sha256 일치=False
최종 verify_unit=(False, "meta 의 run_id 가 산출물과 다르다: JSON run_id='6216cf8f…'")  .part 잔존=False
compare_states.load_degeneracy → [('100', 'B', 24, 4)]        ← 숫자는 B(24 starts), meta 는 A(starts=4 → "시험 산출" 경고)
f01b(A 가 더 김): 최종 디스크: 게시 JSON 깨진 JSON: Extra data: line 23 column 1 (char 337) … sha256 일치=False
  compare_states.py CLI rc=0 stderr='! degeneracy_100_Li.json 이 JSON 이 아니다 — 중간에 죽은 산출인가?' → load_degeneracy [] (상태가 조용히 빠짐)
```
반대 가설(동시 실행은 금지된 시나리오인가): README/WORKING_STATE 에 금지 문장 없음; R6_REQUEST §2 04 행이 명시적으로 "정책: 동시 실행 허용";
run_states.sh 헤더 12행 `STARTS=6 STATES=100 ./scripts/run_states.sh   # 배관 확인용` — 긴 본 실행(STARTS=24) 중 빠른 배관 확인을 같은 상태에 띄우는 것이
헤더가 권하는 사용법이고 그것이 정확히 "느린 B 먼저·빠른 A 먼저 끝남" schedule 이다. 원장이 적은 보장("마지막 온전한 묶음만 남음", "실패면 meta 안 씀")이
이 경로에서 깨진다 → CONFIRMED. 기존 `test_r5_04_*` 는 profile 경로(`--out` + `atomic_write_csv`)만 보므로 초록.
(f01 의 `compare_states.py` CLI traceback 은 내 가짜 JSON 에 `best` 등 필드가 없어서 — 발견 아님; f01b 는 실제 CLI 경로로 rc 0 + 상태 누락.)

### F02 — `python3 verify_toctou.py f02` (PATH 앞 `git` shim: A 만 첫 git 호출에서 대기)
`ne_shape.py:136` `art.open("w")` 최종 경로 직접 쓰기 · `:162` `git_provenance` (git 3회) · `:164` meta `write_text` — 잠금·run_id·sha256 없음.
```
A 가 git 에서 멈춘 시점: CSV measured_shape_mV=1.100000 meta 있음=False
B 완료 rc=0: CSV measured=2.200000 meta.consumed.run_id=run-B
A 재개 뒤 rc A=0 B=0: CSV measured=2.200000 gamma_target=0.600000 | meta consumed.run_id=run-A matrix.sha256=AAAAAAAA
verify_unit(ne_shape csv)=(None, '옛 meta (run_id/sha256 없음)')
```
심각도: 섞임은 재현·검출 불가 → CONFIRMED 유지. 그러나 ne_shape 는 문서상 수동 1회 명령(`WORKING_STATE.md:87` `python3 scripts/ne_shape.py`)이고 R5-04 원장 행은
verify.py/run_states 게시만 범위로 적었다; FINDINGS §5-2 의 숫자는 이 창과 무관 → 숫자가_바뀜이 아니라 R5-05 서술("소비 입력 identity")에 한정어가 붙는다.

### F03 — `python3 verify_toctou.py f03`
`ne_shape.py:96` `csv.DictReader(f.open())` 로 행 선택 → `:102` `f.read_bytes()` 로 다시 열어 해시.
```
큰 CSV(400k 행, 파싱 0.67 s, 0.15 s 에 os.replace): gamma_target=0.4 row.run_id=run-old sha256=62f4813bc071 (옛 6dbd37b43a9c / 새 62f4813bc071)
실제 out/matrix_300_0147.csv: 5987 B, 16 행, 파싱 0.286 ms → 창은 sub-ms
```

### F04 — `python3 verify_toctou.py f04` (matrix 블록 원문 + 계산 중 git 조작)
`run_states.sh:61` `pv = git_provenance(...)` 는 write_meta 안(계산 뒤) 한 번; meta 의 시각 필드는 `created_utc` 뿐.
```
(i) 계산이 본 code.py='value=2' → meta git_dirty=False git_modified_code=[] 시각 필드=['created_utc']
(ii) 계산이 본 code.py='value=1' (시작 SHA 6fb96c49) → meta git_commit=8c7d62c5 (실행 중 커밋 8c7d62c5) git_dirty=False
```
10 시간 실행 중 트리 정리·커밋은 현실적 → "돌린 코드 = commit" 이라는 플래그 해석이 거짓일 수 있다. 숫자·결론 불변 → 서술만_바뀜.

### F05a / F05b — `python3 verify_toctou.py f05a` / `f05b` (shell `python3` 함수로 A 를 `--verify-unit` 앞에서, B 를 `python3 -` heredoc 앞에서 멈춤)
`run_states.sh:193` `python3 scripts/provenance.py --verify-unit "$OUT/matrix_${st}.csv" >/dev/null` — 인자는 경로 하나(`provenance.py:150-151` `verify_unit(sys.argv[2]); print(why)` → stdout 이 `/dev/null`);
`:129/:131` `> "$log"` 가 시도마다 같은 로그를 덮는다.
```
f05a: A 재개 rc=0:  OK (0 초) → out/matrix_100.csv [run_id 6bad7fd4…] / 전부 통과 — 산출 3개…
      최종 디스크: CSV run_id=899610e7 meta run_id=899610e7 verify_unit=(True, '일치')  (A 의 id 는 08ff8b8e)
f05b: A 재개 rc=1:  OK (0 초) → out/matrix_100.csv [run_id 46ccf005…] / 실패 1 건 — 위의 .log 를 볼 것   (그 사이 사유 줄 없음)
      A 가 가리킨 .log 내용: 'wrote out/matrix_100.csv (run_id 2a0739c7…)'   ← B 의 id
      최종 디스크: CSV run_id=2a0739c7 meta run_id=2a0739c7 verify_unit=(True, '일치')
```
둘 다 디스크는 원장이 약속한 "마지막 온전한 묶음"(B/B) 이다. 틀린 것은 wrapper 의 **보고** — F05a 는 STARTS 가 다르면 compare_states 의 `⚠ starts=… 시험 산출` 로 하류에서 드러난다 → 사소.

### F06 — `python3 verify_toctou.py f06`
```
check-ignore out/matrix_100.csv.lock: rc=1 (규칙 없음) · out/matrix_100.csv.ab12cd.part: rc=1 · out/matrix_100.csv.meta.ab12cd.part: rc=1
check-ignore out/.degeneracy_100_Li.part: rc=0 bms-balancing/.gitignore:4:out/.*.part
보유자 살아 있는 동안 flock -n rc=1; lock 파일 unlink 뒤(보유자 여전히 보유) flock -n rc=0
```
`.gitignore:4` `out/.*.part` 는 앞에 점이 있는 이름만 — `NamedTemporaryFile(prefix=out.name + ".")` 이름은 안 걸린다. 배타 소멸은 실행 중 누군가 지워야 한다 → 사소.

### F07 — `python3 verify_toctou.py f07` (실제 `out/matrix_300_0147.csv`+`degeneracy_300_0147_Li.json` 사본으로 A 묶음을 만든 뒤 CSV 만 B bytes 로 교체)
```
A 묶음(정상) 만듦: verify_unit=(True, '일치')
손으로 만든 섞인 쌍: verify_unit(matrix_100.csv)=(False, "meta 의 run_id 가 산출물과 다르다: 다른 run_id 행 16/16: ['bbbb…', 'bbbb…']")
compare_states.py rc=0 stderr=''
100 행: ['  100  step_005C  8.03 [6.67, 8.90] …  degeneracy_100_Li.json', '  100  step_005C  8  3  1.447  7.826  0.952  0.319  matrix_100.csv']
묶음 경고: 없음 (매치된 한 줄은 fixture 경로에 든 'verify' 문자열 — 헤더 줄)
```
`compare_states.py:57-61` 은 meta 를 `starts` 만 보려고 읽고 `verify_unit` 을 부르지 않는다(`ne_shape.fitted_pair_info` 도 같음). F01 이 만드는 섞인 쌍과 게시-meta 사이 crash 의 잔해가 그대로 표에 들어간다.

### F08 — `python3 verify_toctou.py f08` (A 를 heredoc 앞에서 멈추고 X 가 디스크의 run_id 를 복사해 `atomic_write_csv` 로 게시)
```
A: CSV 게시(run_id f35e58d0, a_NE=1.0) 뒤 write_meta 앞에서 멈춤
X 가 디스크의 run_id 를 복사해 게시 rc=0 … / A 재개 rc=0 요약줄=['전부 통과 — 산출 3개…']
최종 디스크: CSV role=X a_NE=51.0 run_id=c7762c61 | meta run_id=c7762c61 sha 일치=True verify_unit=(True, '일치')
```
위협 모델: run_states.sh 헤더 R4-06/R5-04 주석은 "다른 **시도**가 산출을 바꾸면" — `run` 이 시도마다 uuid4 를 만드는 세계에서의 우연 끼어들기다. id 를 파일에서 복사하는 producer 는 버그/의도 쪽이고
그것을 막는다는 문장은 R5-08("grep → 필드 검사")에도 없다 → 기전은 맞지만(부분) 보장 위반은 아니다 → 사소. 렌즈도 같은 등급.

## CONFIRMED — 수정 우선순위
1. **F01** (결론이_바뀜): `tmp=$(mktemp "$OUT/.degeneracy_${st}_${SI}.XXXXXX.part")` 만으로도 B 의 fd 가 자기 inode 에 남아 B/B 로 끝난다(마지막 온전한 묶음 회복); 근본 수정은 degeneracy 에 `--out` 을 주고 verify.py 안에서 `atomic_write_*`+`publish_lock` 게시. `mv` rc 검사 추가. 회귀 테스트는 이 하네스의 f01 schedule (stdout fd 경로).
2. **F07** (서술만): `load_degeneracy`·`load_matrix_axis`·`fitted_pair_info` 가 `provenance.verify_unit` 을 부르고 False 면 행 제외 또는 `⚠ 묶음 불일치` — Codex 최소 조건의 reader 절.
3. **F02** (서술만): ne_shape 게시를 `atomic_write_csv`+`publish_lock` 로, 행에 `run_id`, meta 에 `sha256`, meta 를 같은 잠금 안에서.
4. **F04** (서술만): `run` 전에 `git_provenance` 를 찍어 `started_utc`·시작 트리를 meta 에, write_meta 가 비교해 `git_state_changed_during_run`.
5. **F05a/F05b** (사소): `--verify-unit <art> "$LAST_RUN_ID"` 로 meta.run_id == 이 시도 요구; `why` 를 `say` 로; 로그를 시도별(`$log.$rid`).
6. **F06** (사소): `.gitignore` 에 `out/*.lock` `out/*.part`.
7. **F03** (사소): bytes 를 한 번 읽어 그 bytes 를 파싱·해시.

## 반증됨 / 하향과 이유
- 반증된 발견은 없다 — 아홉 건 모두 내 하네스에서 같은 결과가 났다.
- **F02 하향** (숫자가_바뀜 → 서술만_바뀜): 인용 숫자(FINDINGS §5-2)는 사용자 기계의 1회 수동 실행 산출이고 현재 meta 는 옛 판이라 어떤 숫자도 안 바뀐다; 바뀌는 것은 R5-05 의 "소비 입력 identity" 서술의 강도.
- **F05a 하향** (서술만_바뀜 → 사소): 디스크 상태는 원장 정책("마지막 온전한 묶음") 그대로이고 틀린 것은 wrapper 의 stale 보고 한 줄 — R5-04 의 "A 거부" 는 다른 schedule 을 서술한 테스트 문장이지 이 창의 보장이 아니다.
- **F08 부분**: 재현은 되지만 문서가 주장한 적 없는 보장(소유 증명)에 대한 발견 — 위협 모델 밖.
