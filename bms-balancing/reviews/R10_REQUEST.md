# 적대적 리뷰 요청 — 10차 · α·β 검증 하네스 (`bms-balancing/`)

9차(대상 `29ef505`)는 **NO-GO** (P1 7 · P2 5, `reviews/R9_CODEX.md` · 패키지 `reviews/r9_repros/codex/` sha256 11/11). 열두 건 전부
수정 전 HEAD 에서 재현 → RED(`tests/test_r9_codex.py` d9_01~12) → 수정 → GREEN 으로 닫았다 (`reviews/R6_LEDGER.md` "Codex R9").
목표는 같다: **"정본이 우리 새 모델의 설계 근거로 쓸 만한가"**. GO 기준: R3 §5 + R5 §4 + R6 출처 결속 + R7 §6 + R8 §6 + R9 "GO 를 위한
최소 조건" 6 항.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | 이 파일이 든 커밋 (`git log -1`). 직전 리뷰 대상 `29ef505` |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 만 |
| 정본 | `FINDINGS.md` + `out/` (+ `.meta.json`). **현행 out/ 12 개는 provenance-incomplete** (§4, 변화 없음) |
| 저장소에 없는 것 | 원본 MATLAB · 원자료 xlsx · 문헌 OCP → `BMS_DATA_ROOT` |
| 9차 대비 새것 | R9-01~07 · P2-1~5 닫음 (코드 7 · 러너/감사 3 · wrapper 1 · 계약 1) · 스키마 정본 `bms_balancing/schema.py` · fixture 4 종을 producer 스키마로 · R9 닫힘 재생기 · 두 러너에 `--expected-head` 필수 + dirty 거부 + 패키지 digest |
| 증거 커밋 규약 | 두 닫힘 재생기(R7·R9)는 dirty 트리를 거부한다. 그 JSON 은 **코드 커밋 뒤 clean 트리에서** 만들어 다음 커밋에 얹는다 — JSON 의 `expected_head` 는 코드 커밋, 이 파일이 든 커밋은 그 증거를 담은 커밋 (코드는 둘 사이에 안 바뀐다: `git diff <expected_head> HEAD --stat` 로 확인) |

```bash
git clone -b claude/bms-alpha-beta-verify https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT
cd Yonghoon-DEM-DFT/bms-balancing && git checkout <이 파일이 든 커밋>
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest tests/ -q                # 167 passed 기대. 원자료 불필요
bash matlab/tests/run_all.sh               # Octave 없으면 4·5 단계만

git archive --format=tar bfc4623^ bms-balancing/out | tar -x -C /tmp/r10base      # 과거 baseline
export R6_OLD_OUT=/tmp/r10base/bms-balancing/out
HEAD=$(git rev-parse HEAD)                 # 두 러너는 --expected-head 필수 · dirty 트리 거부 (Codex R9 P2-2)

python3 reviews/r6_repros/codex_r6_mutation_audit.py            # 8/8 CAUGHT · MISSED 0 — CAUGHT 는 rc 1 ∧ 'N failed' 만 (P2-3)
python3 reviews/r6_repros/codex/replay_codex_r6_adapted.py --target .   # R6 적응판 "mode": "full" 6/6
python3 reviews/r6_repros/codex/mutation_adapted.py             # 5/5 CAUGHT
python3 reviews/r7_repros/replay_codex_r7.py --target . --expected-head "$HEAD"   # R7 6 probe 도달·반례 소멸 · package_digest_ok
python3 reviews/r9_repros/replay_codex_r9.py --target . --expected-head "$HEAD"   # R9 12 probe 도달·반례 소멸 · package_digest_ok
# 9차 패키지 그대로: main 은 29ef505 를 pin 한다 (러너가 함수를 직접 부른다). 수정 **전** 을 재려면 29ef505 worktree 에서 —
# 수정 뒤에는 자기 반례 assertion 에서 멈추거나(roots·provenance·shape-overwrite) 전제(partial 위치·러너 거부)가 바뀌어 그 앞에서
# 죽는다(shape-roster·replay-vacuity·aggregation) — 원장 "수정 뒤 패키지 재실행" 표.
python3 reviews/r9_repros/codex/r9_evidence_classify_probe.py .            # rc=1 CAUGHT · rc=2·3·4·5 오류
python3 reviews/r8_repros/codex/r8_inference_repros.py --target . --old "$R6_OLD_OUT" --case all   # 8차 반례 유지 확인
python3 reviews/r8_repros/codex/r8_claims_repros.py    --target . --case all
python3 reviews/r8_repros/codex/r8_port_repros.py      --target . --old "$R6_OLD_OUT" --case controls
python3 scripts/check_u14.py --new out --schema-only            # rc 2: 출처 열 24 건 = provenance-incomplete (§4)
python3 scripts/check_u14.py --new out --old out                # 명부 12/12 · 내용·조건 통과 · 숫자 자기 대조 같음 · rc 2 (출처 열만)
```

## 1. 검증 — 방금 실행

| 검사 | 명령 | 출력 |
|---|---|---|
| 전체 회귀 | `python3 -m pytest tests/ -q` | `167 passed in 100.23s` (`replay_ours_after_fixes/pytest_full.txt`; `tests/` + `matlab/tests/` 수집 167 = `tests/` 만의 수집 수와 같다) (이 컨테이너) |
| MATLAB 스모크 (Octave) | `bash matlab/tests/run_all.sh` | `PASS — 실패 0: []` · `전부 통과` (`replay_ours_after_fixes/matlab_smoke.txt`) |
| 변이 감사 (우리 테스트) | `codex_r6_mutation_audit.py` | `8/8 CAUGHT · MISSED: 0` · 복구 뒤 `7 passed` (`replay_ours_after_fixes/codex_r6_mutation_audit.txt`) |
| 적응판 변이 감사 | `mutation_adapted.py` (R6_OLD_OUT 지정) | `5/5 CAUGHT · MISSED: 0` · baseline·복구 6/6 닫힘 (`replay_ours_after_fixes/mutation_adapted.txt`) |
| R6 적응판 재생 | `replay_codex_r6_adapted.py --target .` | `"mode": "full"` 6/6 닫힘 — R6-03a 는 합성 소스의 선언 상태를 명시하는 hook 적응 뒤 (`replay_ours_after_fixes/replay_codex_r6_adapted.json`, 원장 표) |
| R7 닫힘 재생 | `replay_codex_r7.py --target . --expected-head <코드 커밋>` | R7-01~06 **전부 도달 True · 반례 소멸** · `package_digest_ok: true` · `dirty: false` (`replay_ours_after_fixes/replay_codex_r7_after_fixes.json`) |
| **R9 닫힘 재생** | `replay_codex_r9.py --target . --expected-head <코드 커밋>` | R9-01~07 · P2-1~5 **12/12 도달 True · 반례 소멸** (원본 함수 직접 5 · 적응 7) · `package_digest_ok: true` · `dirty: false` (`replay_ours_after_fixes/replay_codex_r9_after_fixes.json`) |
| 9차 패키지 재실행 (수정 뒤) | `r9_root_repros.py --case …` · aggregation · provenance | root: roots·provenance·shape-overwrite 는 **자기 반례 assertion** 에서 rc 1, shape-roster·replay-vacuity 는 전제 변경으로 그 앞에서 종료; aggregation: `shape_missing_input_state` 에서 canonical 부재로 종료; provenance(기록형): `read_count` 3→**1**, `raced_status` complete→**invalid**, U18 gate 세 case rc 0→**2** (`replay_ours_after_fixes/`) |
| 8차 패키지 재실행 (수정 뒤) | 위 세 명령 | inference: R8-01 `assert selected["100"]…` 줄에서 `KeyError: '100'` (key 가 `100\|Li`·`100\|Kunz` 로 보존된다 — R8 때와 같은 줄) · claims: R8-04 `assert "consumed_inputs" not in rows[0]` 에서 rc 1 · port: `a22da33` SHA pin 에서 멈춤 (pin 우회 러너 없음; controls 는 `test_d8_06`·R9 P2-3 이 덮는다) |
| 현행 정본 점검 | `check_u14 --new out --schema-only` / `--old out` | 출처 열 누락 24 · 내용·조건·중복 검사 통과 · 숫자 자기 대조 같음 · rc 2 (provenance-incomplete) |

## 2. R9 열두 건 — 재현과 수정

| ID | 수정 전 관측 (우리 HEAD) | 수정 | 회귀 |
|---|---|---|---|
| **R9-01** P1 | `same=<빈> same=<정상>` → 1/1·예 rc 0; label 없는 둘도 전부 `out` | 인자를 순서 있는 목록으로, 중복 label(암묵적 `out` 포함)은 판정 전에 거부 rc 2 | `test_d9_01` |
| **R9-02** P1 | old 12 · new 1 → "산출 1 개 · 전부 같다" rc 0 | 명부 = 정본 ∪ 새 산출 canonical 이름; 없으면 "명부 불일치" rc 2; 부분은 `--subset` 계약으로만 (k/N, 승격 아님) | `test_d9_02` |
| **R9-03** P1 | `LLI_pct` 삭제·출처 셀 비움·가짜 receipt·조건 변경 전부 rc 0; schema-only 는 중복 안 봄 | `bms_balancing/schema.py` 한 정본: producer assert + checker 가 필수 셀·숫자·receipt(역할·path·64-hex·재계산 digest)·중복 key·`DEGENERACY_CONTROLS`/meta 조건 대조 (schema-only 에서도) | `test_d9_03` |
| **R9-04** P1 | 200 반쪽전지 없으면 requested 에서 사라져 1/1 rc 0 | requested 를 파일 존재 전에 고정; `available/missing_input/paired/missing` 분리 | `test_d9_04` |
| **R9-05** P1 | 중복 (GITT,Li,0) 행 → 행 순서가 γ 결정 | reader 가 `schema.unique_rows`/`matrix_key` 로 유일성 강제, 중복이면 RuntimeError | `test_d9_05` |
| **R9-06** P1 | rc 3 인데 canonical 을 부분으로 교체 | 완전성 판정 → 게시: typed `status`; complete 만 canonical, partial/none 은 `<write>/partial/` | `test_d9_06` |
| **R9-07** P1 | 경로 3 회 read → A 셀을 B precision/audit 로 승인 complete | `load_dd_eval` 한 번 → `DdEvalText(text, sha256)` 를 parse·precision·audit·compare 전부에; `matlab_sha256` 기록 | `test_d9_07` |
| **P2-1** P2 | `--probes DOES_NOT_EXIST` → `{}` rc 0 | 빈/오타/중복/valid+unknown 거부 rc 2, JSON 없음, 출력 key == 요청 | `test_d9_08` |
| **P2-2** P2 | SHA·clean·패키지 bytes 미대조 | `--expected-head` 필수 · dirty 기본 거부 · SHA256SUMS 대조 · 재현/오류/mismatch 면 rc ≠ 0 (R7·R9 러너 둘 다) | `test_d9_08` |
| **P2-3** P2 | rc 2·3·4 도 CAUGHT | CAUGHT = rc 1 ∧ `N failed`; MISSED = rc 0 ∧ `N passed`; 나머지 오류 | `test_d9_09` |
| **P2-4** P2 | matrix sidecar 가 singular `Li` | `run` 의 `LAST_ARGV` + 잠금 안 한 번 읽은 bytes 로 id·sha256·`roster`(본문 유도)·`argv` 봉인 | `test_d9_10` |
| **P2-5** P2 | zero-pair rc 1 이 rc 3 보다 먼저, 계약 미명시 | `EXIT_BY_STATUS = {complete: 0, none: 1, partial: 3}` 를 코드·meta `status` 로; wrapper 는 status 로 가른다 | `test_d9_11` |

**fixture 자백 (네 번째)**: `_full_matrix_rows`·`_deg(schema=True)`·`_u14_dirs`·i6w_03 의 inline JSON 은 열 이름의 부분집합 + 가짜
receipt 였다 — checker 가 내용을 안 본다는 사실을 fixture 가 가려 줬다. 전부 producer 스키마 + 진짜 receipt 로 다시 썼고, c6_03·
d8_03 은 짝 없는/부분 실행의 산출을 `partial/` 에서 읽는다 (R9-06 의 결과).

## 3. 9차 질문에 대한 답

| Q | 답 |
|---|---|
| 1 `state\|si` | 유지하되 중복 root label 을 판정 전에 거부한다 (R9-01). typed `(root, state, si)` identity 는 미구현 — §5 |
| 2 다섯 관측 | "provenance-incomplete 탐색적·잠정" 으로만 요구서 초안에 — GO·승격·원인·출처 주장의 근거로 쓰지 않는다 |
| 3 공통 snapshot | build 경계 채택에 동의 — **미구현**, §5·§6 Q5 |
| 4 rc 3 | typed `PARTIAL`(meta `status`) 로 보존, canonical 을 덮지 않는다 (R9-06); zero-pair 는 rc 1 + `none` (P2-5) |
| 5 U18 승격 | 명부 12/12 · receipt 내용 · 조건/env · 수치 exact equality 를 `check_u14` 가 그 순서로 강제; 움직인 profile 행은 승격 안 함 (rc 1) — "후보 evidence version 보존 + pinned 옛 환경 재현 + U16 attribution" 은 절차 |

## 4. 정본 범위 — 현행 `out/` 은 provenance-incomplete (변화 없음)

새 검사(명부 12/12 · 필수 셀 · receipt · 중복 · 조건 · 자기 대조 숫자)는 전부 통과하고 matrix/profile 8 개의 출처 열 3 개(24 건)만
빠진다. 보강은 **U18** (사용자 기계 재실행, 별도 `OUT=` → `check_u14 --new out_u18 --old out` 가 명부·내용·조건·숫자를 강제한 뒤
승격). 그때까지 인용은 "수치 그대로 · 기준 입력 출처 미기록".

## 5. 닫지 않은 것 — 신뢰 경계

| # | 무엇 | 왜 열어 두나 |
|---|---|---|
| export 계약 (R9 Q3) | 기준·대상 공유 workbook/문헌의 **같은 snapshot** 강제 | 아직 양쪽 identity 기록만 — 패키지 `production_paths.shared_full_cell_mismatch_accepted` 가 그대로 `true` 다 (숨기지 않는다). 위치는 build 경계로 합의, 다음 라운드 |
| typed identity (R9 Q1) | `(root, state, si)` 3-tuple | 문자열 `state\|si` 유지; 중복 label 은 사전 거부로 막았다 |
| U18 | 현행 정본의 출처 열 보강 재실행 | 사용자 기계. 승격 규칙은 이제 코드가 강제 |
| U16 · U17 | 옛 조합 재실행 · 끝점 witness 스키마 | 전과 같음 |
| F01b · F08 · F2 · V6-09 · U2~U10 | 전과 같음 | — |

## 6. 질문

1. **`--subset` 계약**: 부분 재실행을 명시적 계약으로 허용하되(k/N 표시) 승격 불가 — 이 경계가 맞는가, 아니면 부분 재실행 자체를
   거부해야 하는가.
2. **degeneracy schema guard 의 위치**: `--out` 게시 경계에서만 assert 하고 stdout 모드는 경고다 (시험용 objective 가 stdout 모드를
   쓴다). stdout 을 파일로 받는 옛 wrapper 는 없다 — 이 경계가 우회로로 보이는가.
3. **`ne_shape --states`**: requested 명부를 명시하는 옵션을 뒀다 (기본은 `D.HALF_FILE[source] ∩ D.STATES`). meta 의
   `requested_from` 기록으로 충분한가, "알려진 의도적 부재" 를 source 별 allowlist 로 코드에 둬야 하는가.
4. **러너의 dirty 계약**: `--allow-dirty` 는 목록을 기록하고 rc 를 바꾸지 않는다 (개발 중 실행용). 증거로 인정되는 것은 clean 실행뿐
   이라고 §0 규약으로 두면 되는가, dirty 면 항상 rc ≠ 0 이어야 하는가.
5. **export 계약의 구현**: build 호출자(`cmd_*`)가 공유 입력을 한 번 읽어 typed snapshot 을 ref/target `build` 에 주입하고, 다른
   export 는 `--sensitivity` 모드 + A/B digest 로만 — 이 설계로 가도 되는가 (다음 라운드 전에 합의하고 싶다).

## 7. 실측 첨부

- `reviews/R9_CODEX.md` · `reviews/r9_repros/codex/` (패키지 11 파일) · `reviews/r9_repros/replay_ours_29ef505_before/` (수정 전
  재현: root json+stdout · aggregation stdout · provenance stdout · rc) · `reviews/r9_repros/replay_ours_after_fixes/` (수정 뒤:
  root case 별 stderr · aggregation stderr · provenance stdout + before/after diff · classify · 변이 감사 · MATLAB 스모크 · 두 러너 JSON).
- `reviews/r9_repros/replay_codex_r9.py` (R9 닫힘 재생기) · `bms_balancing/schema.py` · `reviews/R6_LEDGER.md` "Codex R9" 절.

## 8. 이후

GO 면 새 모델 설계 요구서(`docs/`) 초안 — §5 다섯 행 + R8 Q6 의 열 구조 (다섯 관측은 provenance-incomplete 잠정 관측으로 표시).
U16·U17·U18 은 사용자 기계 실측. export 계약(Q5)은 합의 뒤 구현.
