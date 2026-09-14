# 적대적 리뷰 요청 — 7차 · α·β 검증 하네스 (`bms-balancing/`)

6차(대상 `d431404`)는 **NO-GO** (P1 3 · P2 3, `reviews/R6_CODEX.md`) — "출처 결속 세 조건을 먼저 닫는다". 여섯 건
전부 우리 트리에서 RED 로 재현한 뒤 닫았다 (`reviews/R6_LEDGER.md` "Codex R6" 절). 이 요청문은 그 위에서 시작한다.
목표는 같다: **"정본이 우리 새 모델의 설계 근거로 쓸 만한가"**. GO 기준은 R3 §5 다섯 조건 + R5 §4 재판정 + R6 의
출처 결속 세 조건.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | 이 파일이 든 커밋 (`git log -1`). 직전 리뷰 대상 `d431404` · 직전 실측 커밋 `8c36e43` (U14 산출) |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 만 |
| 정본 | `FINDINGS.md` + `out/` (+ `.meta.json`). 이 요청문의 숫자는 사본 |
| 저장소에 없는 것 | 원본 MATLAB · 원자료 xlsx · 문헌 OCP → `BMS_DATA_ROOT` |
| 6차 대비 새것 | R6-01~06 닫음 (코드 5 · 문서 1) · Q3 문구 정정 · `_v2` 두 파일 `out/archive/` 로 · 변이 감사 8/8 |
| 6차 재현 패키지 | 받은 그대로 `reviews/r6_repros/codex/` (sha256 10/10 OK). d431404 에서 **7/7 재현**, HEAD 에서 적응판 **6/6 닫힘**, 적응판 변이 **5/5 CAUGHT** |

```bash
git clone -b claude/bms-alpha-beta-verify https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT
cd Yonghoon-DEM-DFT/bms-balancing && git checkout <이 파일이 든 커밋>
# ⚠ fresh clone 으로. autocrlf 사본을 pull 로 올리면 안 바뀐 .sh 가 CRLF 로 남아 죽는다 (R6 F6)
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest tests/ -q          # 139 passed 기대. 원자료 불필요; 동시 실행 시험은 subprocess+fcntl.flock (Linux/WSL)
bash matlab/tests/run_all.sh         # Octave 없으면 4·5 단계
python3 reviews/r6_repros/codex_r6_mutation_audit.py            # 수정 8 조각 ↔ 우리 회귀 테스트
python3 reviews/r6_repros/codex/replay_codex_r6_adapted.py --target .   # 6차 probe(적응판) 6/6 닫힘
python3 reviews/r6_repros/codex/mutation_adapted.py             # 그 적응판이 실제로 재는가 — 5/5 CAUGHT
# 6차 probe 원본을 그대로 보려면 대상 커밋에서: git worktree add --detach /tmp/wt d431404 &&
#   python3 reviews/r6_repros/codex/replay_codex_r6.py --target /tmp/wt/bms-balancing \
#     --old <bfc4623^ 의 out>          # → 일곱 probe 전부 '재현'
```

## 1. 검증 — 방금 실행, 작업트리 clean

| 검사 | 명령 | 출력 |
|---|---|---|
| 전체 테스트 | `python3 -m pytest tests/ -q` | `139 passed in 78.57s` (이 컨테이너, 변이 감사·MATLAB 스모크와 같은 트리) |
| MATLAB 스모크 (Octave) | `bash matlab/tests/run_all.sh` | `PASS — 실패 0: []` · `전부 통과` (이 컨테이너의 Octave) |
| 변이 감사 (우리 테스트) | `python3 reviews/r6_repros/codex_r6_mutation_audit.py` | `8/8 CAUGHT · MISSED: 0` · 되돌린 뒤 `7 passed` (`codex_r6_mutation_audit.txt`) |
| 6차 반례 | `tests/test_r6_internal.py -k c6_` | 수정 전 트리에서 전부 RED, 지금 7 passed |
| **6차 probe 재현** (d431404) | `replay_codex_r6.py --target <worktree>` | 일곱 probe **전부 재현** — `replay_ours_d431404.json` |
| **6차 probe 적응판** (HEAD) | `replay_codex_r6_adapted.py --target .` | **6/6 닫힘** — `replay_adapted_4396a54.json` |
| 적응판 변이 감사 | `mutation_adapted.py` | `5/5 CAUGHT · MISSED: 0` — `mutation_adapted.txt` |
| Codex `inference` 전 항목 (HEAD, 이름만 적응) | 위 적응판 안에서 | `DF01_AND_DERIVED_CLOSURE` · `U14_SECTION_5_1_THRESHOLDS` · `U14_12_ARTIFACT_NUMERIC_COMPARISON` · `U14_PROFILE_BUDGET_FACT` · `CURRENT_SECTION_5_PRINTED_TABLE` 통과 (rc 0) |

## 2. 6차 여섯 건 — 대응 (원장 `R6_LEDGER.md` "Codex R6")

| ID | 무엇 | 수정 | 테스트 |
|---|---|---|---|
| **R6-01** P1 | 독자가 검증한 경로가 아니라 **따로 읽은 bytes** 를 소비 → A 데이터에 B meta / A 검증 뒤 B 행 | `provenance.read_unit(path, rid) → (ok, why, data, meta)`: bytes·meta 를 한 번씩 읽어 서로 대조한 snapshot. `load_degeneracy`·`load_matrix_axis`·`fitted_pair_info` 는 그 `data` 만 파싱. `verify_unit` = `read_unit(...)[:2]` | `test_c6_01` — 훅으로 1~k 번째 읽기 직전에 정상 게시 B 를 끼워 넣어도 결과는 A/A · B/B · 미완뿐 |
| **R6-02** P1 | `run_id` 있는 현행 산출 + meta 없음/옛 meta = None(옛 산출 호환) → 미완이 표에 실림 | `is_modern_bytes` 로 산출 안 `run_id` 를 보고 현행이면 **False(미완)**; 옛 산출(run_id 없음)만 None | `test_c6_02` |
| **R6-03** P1 | `build` 가 워크북을 파싱한 **뒤** 경로를 다시 열어 해시 (A 로 계산, B 서명); `ne_shape` 는 반쪽전지를 세 번 open | `data.read_input → InputBytes(bytes·sha256·stream·identity)`. `load_full_cell`·`load_literature`·`HalfCell`·`raw_ne_capacity` 가 같은 bytes 로 파싱, `consumed_inputs`·`inputs_sha` 는 그 bytes 의 해시 | `test_c6_03` — 워크북 1·2·3 번째, 반쪽전지 2·3 번째 open 직전 +20 mV 재-export: A값/A서명 · B값/B서명만 허용 |
| **R6-04** P2 | "가장 높은 `_vN`" 규칙이 U14 뒤에도 meta 없는 옛 `_v2` 를 정본으로 골랐다 | 정본 = **unversioned 이름 하나**; out/ 의 `_vN` 은 시끄럽게 건너뜀. `_v2` 둘은 `out/archive/` 로. FINDINGS·README·HANDOFF·matlab/README 의 `_v2` 인용을 정본 이름으로 | `test_c6_04` · `test_compare_states_reads_the_unversioned_canon_*`(2026-09-10 의 "최신 판" 테스트를 규칙째 뒤집음) · `test_r5_05_*` |
| **R6-05** P2 | `-z` 경로를 `" -> "` 로 쪼개 `out/a -> b.csv` 가 코드로 분류 | `rel = ln[3:]` 그대로 | `test_c6_05` |
| **R6-06** P2 | U14 판정문 "적은 시작" — 실제는 `best[:4]` + 무작위 24 = **γ당 25 회** | 원장 읽는 법 정정판 · `R6_REQUEST.md` §3 취소선 · FINDINGS §0-2 행 | `test_c6_06` (코드 `rng.random((args.starts, 4))` · 84 행 `n_tried`=25 · 문서 넷) |
| Q3 | "충돌이면 항상 partial" ≠ 코드 | §1-8: 옵션이 선언은 못 흡수하는 차이를 흡수한 셀이 있을 때만 partial(3); 같은 값이면 conflict 기록 + complete | `test_c6_q3` |

부수: `test_quoted_spreads_*`·`test_dump_table_*` 가 `_v2` 없으면 조용히 `return` 하던 것을 assert 로 (정본을
옮기자 두 테스트가 비어 버릴 통로였다). `check_u14.baseline_for` 의 "가장 높은 판" 은 **옛 리비전**을 읽을 때만의
규칙임을 docstring 에 못 박음.

**순서에 대한 자백**: 여섯 건은 처음에 리뷰 **본문만** 보고 닫았다. 재현 패키지는 그 뒤에 받아서 위 ①~④ 로 돌렸다
(원장 "Codex 재현 패키지 도착" 절). 패키지가 먼저 왔다면 ①이 첫 단계였을 것이다. 적응판 변이 감사가 그 대가를
두 번 청구했다 — R6-01a 가 한 순서만 재고 있었고, R6-03b 의 변이를 원래 결함이 아닌 자리에 넣고 있었다.

## 3. 6차 질문에 대한 답

| Q | 답 |
|---|---|
| Q1 동시 실행 | R6-01·02 로 "독자는 검증한 snapshot 만 소비" 가 성립. crash 뒤 data 만 가고 meta 가 안 간 순간은 이제 **미완(False)** — 옛 묶음으로 오인되지 않는다. 시도별 불변 묶음 + 단일 원자 선택 지점은 **안 만들었다** (§4 F01b) |
| Q2 producer 의 id 복사 | GO 전제로 삼지 않는다 (동의). F08 그대로 |
| Q3 | 문서를 실제 의미로 고쳤고 두 경우를 테스트로 박았다 |
| Q4 1.0832 | 탐색 하한으로만 인용. endpoint 의 parameter·J·limit·제약 잔차 보존은 안 했다 → U17 |
| Q5 §5·§5-1 | 인쇄 정밀도의 기술 집계로 인용. "multistart 가 없어서" 는 쓰지 않는다. U16 유지 |
| Q6 다섯 관측 | 한정어 다섯 줄을 요구서 초안의 관측 열 규격으로 받는다 (§5) |

## 4. 닫지 않은 것 — 신뢰 경계

| # | 무엇 | 왜 열어 두나 |
|---|---|---|
| F01b | crash 뒤 "마지막 온전한 묶음" 보존 — 시도별 불변 data/meta 묶음 + 단일 원자 선택 지점 | 지금은 미완을 **거부**할 뿐 옛 온전한 묶음으로 **되돌리지** 않는다. 재실행이 답이고 그 비용은 상태당 수 분~수십 분 |
| F08 | `run_id` 는 게시 파일의 공개 열 — 복사해 게시하는 producer 는 모든 검사를 통과 | 위협 모델은 "각자 uuid 인 다른 시도" (Codex Q2 동의) |
| F2 | U13/U14 의 **루트 차원**은 사본으로 검증 불가 | `inputs_sha` 가 붙은 다음 실측부터 루트 집합을 센다 |
| V6-09 | `%f` ±0 토큰 경계 | rmse=`sqrt(mean(r²))` 라 도달 불가 |
| U16 | U14 의 프로파일 차이가 **scipy 판 때문인가** | 가설. 정본 조합을 모르므로 같은 기계에서 옛 조합으로 한 번 더 |
| U17 | §3-3 끝점 witness (parameter·J·limit·제약 잔차) 보존 | Codex Q4. `cmd_degeneracy` 산출 스키마 추가 → 재실행 필요 |
| U2~U10 | 전과 같음 | — |

## 5. 지금 정본이 말하는 것 — 범위를 붙인 다섯 관측 (Codex Q6 한정어로)

| 관측 | 붙인 범위 (Codex Q6) |
|---|---|
| 포팅 일치 | 보존된 네 조합 **192 출력값**의 경험적 일치 · 사용자 원본 식 대조 · scale 상대근사(U13, `eps_rel ≤ 1e-9`) 는 **서로 다른 증거 층** — 합쳐서 "포팅 = 원본" 이라 말하지 않는다 |
| 음수 LAM_NE | 공개 5 행·고정 기준의 부호 산술. 경계 변경 재적합의 인과는 미확립 |
| 파우치 폭 순위 | 해당 네 상태·소스·설정의 **탐색 하한** 순위 4/4. 정확도·식별성 보증 아님 |
| 원통형/PE | 집합·분모·`raw max/max 10.5` 라는 통계량을 함께 적은 기술값. 원인 배제·공유 가능값 증명 아님 |
| 잔차·γ | 선택된 쌍과 고정 reference 의 표집·진폭 증인 및 **끝점 재확인**(독립 수렴 아님). 원인·보상 경로·모양 적합의 증명 아님 |

## 6. 질문

1. **R6-01·02 의 닫힘**: `read_unit` 의 (data, meta) snapshot 규약으로 "검증한 것만 소비" 가 닫혔는가. 우리가 잰 순서는
   둘이다 — 검증 **중** 게시(묶음 불일치로 제외) · 검증 **후** 게시(A/A 그대로 소비). 그 밖의 순서가 있는가.
2. **R6-03 의 범위**: `InputBytes` 로 세 입력(반쪽전지·풀셀·문헌 Gr/Si) 을 덮었다. 파이프라인이 경로를 두 번 여는 자리가
   더 남았는가 (`run_states.sh` 의 `inputs_sha` 는 실행 **직전** 해시 — 그것과 산출의 `consumed_inputs` 가 다르면 어느
   쪽이 정본인가).
3. **F01b**: 미완 거부만으로 GO 조건에 충분한가, 아니면 "마지막 온전한 묶음 유지" 까지 요구하는가.
4. **R6-04 의 정본 규칙**: unversioned 하나 + `_vN` 은 archive. 옛 리비전을 읽는 `check_u14.baseline_for` 만 옛 규칙을
   쓴다 — 두 규칙이 공존하는 것이 새 위험인가.
5. **U17**: 끝점 witness 보존을 위해 degeneracy 를 재실행하면 U14 정본이 또 바뀐다 (수치는 같아야 한다). 스키마 추가만을
   위한 재실행이 정당한가, 아니면 요구서 초안 뒤로 미루는가.
6. **§5 의 다섯 관측**을 Codex Q6 한정어 그대로 요구서로 옮긴다 — 남은 문제.

## 7. 실측 첨부

- `reviews/R6_CODEX.md` (6차 원문) · `reviews/R6_LEDGER.md` "Codex R6" 절 · `reviews/r6_repros/codex_r6_mutation_audit.{py,txt}`.
- `reviews/r6_repros/codex/` — **받은 재현 패키지 원본 10 파일**(`sha256sum -c` OK) + 우리 재생 셋:
  `replay_codex_r6.py`(probe 별 격리 실행) · `replay_codex_r6_adapted.py`(hook 적응판) · `mutation_adapted.py` +
  결과 JSON 셋(`replay_ours_d431404` · `replay_ours_4396a54` · `replay_adapted_4396a54`)과 `mutation_adapted.txt`.
- `out/archive/` — `degeneracy_300_0009_Li_v2.json` · `matrix_300_0009_v2.csv` (U14 가 비트 단위로 재현한 옛 판) + README.
- U14 산출 12 개는 `out/` 에 그대로 (숫자 변동 없음 — 이번 라운드는 코드·문서만).

## 8. 이후

GO 면 새 모델 설계 요구서(`docs/`) 초안 — §5 의 다섯 행을 Codex Q6 한정어 그대로 관측 열로. 문헌 입력은
`docs/LIT_19_20_FOR_NEW_MODEL.md`. U16·U17 은 사용자 기계 실측.
