# 적대적 리뷰 요청 — 8차 · α·β 검증 하네스 (`bms-balancing/`)

7차(대상 `521be85`)는 **NO-GO** (P1 3 · P2 3, `reviews/R7_CODEX.md` · 재현 패키지 `reviews/r7_repros/codex/`).
여섯 건 전부 우리 트리에서 재현 → RED 회귀 → 수정 → GREEN 으로 닫았다 (`reviews/R6_LEDGER.md` "Codex R7" 절).
목표는 같다: **"정본이 우리 새 모델의 설계 근거로 쓸 만한가"**. GO 기준은 R3 §5 다섯 조건 + R5 §4 + R6 출처 결속
세 조건 + R7 §6 세 조건.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | 이 파일이 든 커밋 (`git log -1`). 직전 리뷰 대상 `521be85` · 그 전 `d431404` |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 만 |
| 정본 | `FINDINGS.md` + `out/` (+ `.meta.json`). 이 요청문의 숫자는 사본 |
| 저장소에 없는 것 | 원본 MATLAB · 원자료 xlsx · 문헌 OCP → `BMS_DATA_ROOT` |
| 7차 대비 새것 | R7-01~06 닫음 (코드 4 · 재생 도구 2) · `test_c6_01`·c6_04 변이 강화 · 프로파일 예산 문구 재한정 · Q2 전제 정정 |

```bash
git clone -b claude/bms-alpha-beta-verify https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT
cd Yonghoon-DEM-DFT/bms-balancing && git checkout <이 파일이 든 커밋>
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest tests/ -q                # 146 passed 기대. 원자료 불필요
bash matlab/tests/run_all.sh               # Octave 없으면 4·5 단계만

# 과거 baseline (여러 재생이 요구한다) — 손으로 한 번 풀어 둔다
git archive --format=tar bfc4623^ bms-balancing/out | tar -x -C /tmp/r8base
export R6_OLD_OUT=/tmp/r8base/bms-balancing/out

python3 reviews/r6_repros/codex_r6_mutation_audit.py          # 8/8 CAUGHT · MISSED 0 · rc 0 (MISSED 면 rc 1)
python3 reviews/r6_repros/codex/replay_codex_r6_adapted.py --target .   # R6 적응판 — "mode": "full", 6/6 닫힘
python3 reviews/r6_repros/codex/mutation_adapted.py           # 그 적응판이 실제로 재는가 — 5/5 CAUGHT
# 7차 패키지 그대로 (수정 **전** 을 재려면 대상 커밋 521be85 worktree 에서)
python3 reviews/r7_repros/codex/harness_r7_execution_repros.py --target .
python3 reviews/r7_repros/codex/harness_r7_claims_repros.py   --target . --case noise
python3 reviews/r7_repros/codex/harness_r7_claims_repros.py   --target . --case matrix
python3 reviews/r7_repros/codex/harness_r7_inference_repros.py --target . --case baseline
python3 reviews/r7_repros/codex/harness_r7_port_repros.py     --target . --case controls
```

## 1. 검증 — 방금 실행

| 검사 | 명령 | 출력 |
|---|---|---|
| 전체 회귀 | `python3 -m pytest tests/ -q` | `146 passed in 106.26s` |
| MATLAB 스모크 (Octave) | `bash matlab/tests/run_all.sh` | `PASS — 실패 0: []` · `전부 통과` (이 컨테이너의 Octave) |
| 변이 감사 (우리 테스트) | `codex_r6_mutation_audit.py` | `8/8 CAUGHT · MISSED: 0` · 복구 뒤 `7 passed` (`codex_r6_mutation_audit.txt`) |
| 적응판 변이 감사 | `mutation_adapted.py` | `5/5 CAUGHT · MISSED: 0` · baseline 지정 시 `mode: full` 6/6 (`mutation_adapted.txt`) |
| 7차 패키지 재실행 | 위 다섯 명령 | 여섯 probe **전부 자기 assertion 에서 실패** = 반례가 사라짐 (§2 표) |

## 2. R7 여섯 건 — 재현과 수정

수정 **전**(`521be85`)에는 여섯 probe 가 전부 재현됐다. 수정 **뒤**에는 각 probe 가 *자기 반례 assertion* 에서
실패한다 — 그 실패 지점이 곧 닫힘의 증거다.

| ID | 수정 전 관측 (우리 HEAD) | 수정 | 수정 뒤 probe 가 멈추는 곳 | 회귀 |
|---|---|---|---|---|
| **R7-01** P1 | 반례 상태가 미완으로 빠지자 "아니오" → **"예" rc 0**; 빈 디렉터리도 "예" | 독자가 제외를 `excluded=` 로 보고하고, 집계가 **후보/검증/제외**를 세어 미완이면 전체 판정 대신 `미완` + **rc 2** (판정 줄 머리는 유지, 절대 "예" 로 끝나지 않는다) | `assert partial["rc"]==0 and …endswith("예")` | `test_d7_01` (아니오 → 미완 → 아니오 · 빈 디렉터리) |
| **R7-02** P1 | A 의 misfit ÷ B 의 σ = **1.59** (A/A 는 2163), 진단 문장이 바뀜 | `build` 가 소비한 원시 배열을 `obj.full_cell_raw` 로 넘기고 `cmd_noise` 는 그것만 쓴다 (정의 불변). 산출에 `consumed_inputs`·`inputs_sha` | `assert A["sigma_at_k1_V"]!=mixed[...]` | `test_d7_02` |
| **R7-03** P1 | 기준 전용 입력만 바꿔 LAM_NE 2.85→3.85 %p 인데 행 서명 동일 | matrix 행에 `ref_inputs_sha`·`ref_consumed_inputs`(+대상 `consumed_inputs`), profile 행에 `ref_inputs_sha`·summary 에 양쪽 identity | `assert not any("ref" … in A)` | `test_d7_03` |
| **R7-04** P2 | 현행 `--old` 에 역사 규칙이 걸려 `_v2` 선택 → "전부 같다" rc 0 | `--baseline-policy {auto,current,historical}` (auto = `--old-rev` 면 historical). 정책과 건너뛴 형제를 출력 | `assert p.returncode == 0` | `test_d7_04` (두 정책) · `test_i6w_03` |
| **R7-05** P2 | `R6_OLD_OUT` 없으면 `.` 를 baseline 으로 → 5/6 rc 1 | `baseline_from_env()` 가 빈 값·없는 디렉터리를 None 으로. baseline 없는 재생은 `부분` 으로 표시하고 full 과 구분 | `assert records["default_environment"]["returncode"]==1` | `test_d7_05` |
| **R7-06** P2 | 변이 감사가 `MISSED: 1` 에도 rc 0 | `main()` 이 `1 if (bad or 복구실패)`; import 만으로 감사가 돌지 않게 함수 분리 | `--case controls` | `test_d7_06` |

## 3. Codex 가 짚은 우리 증거의 한정 — 같이 고쳤다

- **`test_c6_01` 은 주입을 꺼도 통과했다.** 실측해 보니 더 나빴다: degeneracy 데이터는 **한 번만** 열리는데 k 를
  1~4 로 가정해 k≥2 인 건은 훅이 안 걸린 채 통과했다. 이제 읽기 경계 수를 **먼저 세고** 그만큼만 돌며 건마다
  `fired["v"] >= k` 로 주입을 확인한다. 관측도 정직하게 적는다 — 읽기 **직전** 주입에서 살아남는 것은 B/B 와
  명시적 미완뿐이고, A/A 는 대조군과 적응판의 `검증_후_게시` 순서에서 나온다 (세 결과를 다 요구한다).
- **c6_04 변이가 `KeyError` 로 잡히고 있었다** (파일명 때문에 state 가 사라져서). 변이를 옛 `_keep_latest` 규칙
  그대로로 바꿔 **값**으로 잡히게 했다.
- **프로파일 예산 문구를 다시 좁혔다** (R7 §5): 두 산출 모두 γ당 25 회를 썼고 같은 예산 아래 일부 행이 달랐다 —
  **원인은 U16 미확정**. "25 회였으니 예산이 충분했다"·"차이는 ULP 때문" 은 이 관측만으로 말하지 않는다.
- **Q2 전제 정정**: 7차 요청문이 물었던 "`run_states.sh` 의 **실행 직전** `inputs_sha`" 는 **없다** — 그 문자열은
  `run_states.sh` 에 0 회고, 실행 전에는 `LAST_PRE_PV` 의 git 상태·시각만 모은다. 입력 서명은 각 `build()` 가 소비
  snapshot 으로 만든다. 없는 두 해시의 충돌을 물은 질문이었다 (`test_d7_07` 이 이 사실을 고정한다).

## 4. 닫지 않은 것 — 신뢰 경계

| # | 무엇 | 왜 열어 두나 |
|---|---|---|
| F01b | crash 뒤 "마지막 온전한 묶음" 보존 | Codex Q3(R7): 미완이 독자·집계·공개 판정까지 전파되면 자동 복원은 **GO 전제가 아니다**. R7-01 로 전파를 닫았다 |
| F08 | `run_id` 는 공개 열 — 복사해 게시하는 producer | 위협 모델은 "각자 uuid 인 다른 시도" (R6 Q2 동의) |
| F2 | U13/U14 의 루트 차원은 사본으로 검증 불가 | `inputs_sha` 가 붙은 다음 실측부터 |
| U16 | γ profile 개별 행 차이의 **원인** | 같은 예산(25 회) 아래 갈렸다. 옛 라이브러리 조합 재실행으로만 닫힌다 |
| U17 | §3-3 끝점 witness (parameter·J·limit·제약 잔차·seed·입력 identity) 보존 | Codex Q5(R7): **지금 의무 실행은 아니다**. 다음 계획된 실행에서 같이 보존하고, 그때도 기존 정본을 덮지 말고 별도 위치에서 비교 |
| V6-09 · U2~U10 | 전과 같음 | — |

## 5. 지금 정본이 말하는 것 — 범위를 붙인 다섯 관측 (R7 Q6 한정어 그대로)

| 관측 | 붙인 범위 |
|---|---|
| 포팅 일치 | 192 raw 값의 경험적 일치 · 사용자 원본 식 대조 · U13 scale 상대근사는 **서로 다른 증거 층** |
| 음수 LAM_NE | 공개 5 행·고정 reference 의 부호 산술. 경계 변경 재적합의 인과는 미확립 |
| 파우치 폭 순위 | 지정 네 상태·소스·설정의 **탐색 하한** 순위. 정확도·식별성 보증 아님 |
| 원통형/PE | 집합·분모·`raw max/max 10.5` 를 명시한 기술값 |
| 잔차·γ | 선택된 쌍·고정 reference 의 표집·진폭 증인·**끝점 재확인**(독립 수렴 아님). 원인·보상 경로·모양 적합의 증명 아님 |

요구서 초안은 관측 옆에 **후보 모델 변경 · 대안 가설 · 구분 실험 · 채택/기각 기준**을 별도 항목으로 둔다 (R7 Q6).

## 6. 질문

1. **R7-01 의 전파 범위**: `compare_states` 는 이제 미완이면 rc 2 이고 전체 판정을 안 낸다. 같은 성질이 필요한 다른
   소비자(`ne_shape`·`check_u14`·문서 표 생성)에도 빠진 곳이 있는가 — 특히 "부분집합인데 전체처럼 읽히는" 표가.
2. **R7-02 의 경계**: 적합과 잡음이 같은 snapshot 을 쓰도록 `full_cell_raw` 를 들려 보냈다. 같은 모양의 두 번 읽기가
   남은 자리가 있는가 (반쪽전지 `raw_ne_capacity`·문헌 곡선·`ne_shape` 의 재적합 경로).
3. **R7-03 의 스키마**: 행에 `ref_inputs_sha`+`ref_consumed_inputs` 를 넣었다. 기준·대상이 **같은 export 여야 한다**는
   계약을 코드로 강제할지(같은 snapshot 재사용), 지금처럼 다름을 허용하되 양쪽을 기록할지 — 어느 쪽이 맞는가.
4. **정책 분기의 위험**: `--baseline-policy` 로 두 규칙을 갈랐다. 기본값 auto 가 옛 out/ 을 손으로 푼 사람에게
   조용히 틀린 짝을 줄 여지가 남는가 (경고로 충분한가, historical 을 요구해야 하는가).
5. **U16·U17 의 순서**: 요구서 초안과 병행해 U16(옛 조합 재실행)을 먼저 볼지, U17 스키마를 다음 실행에 얹을지.
6. **§5 다섯 관측 → 요구서**: R7 Q6 의 네 항목(변경·대안·구분 실험·기각 기준) 구조로 옮길 때 남는 문제.

## 7. 실측 첨부

- `reviews/R7_CODEX.md` (7차 원문) · `reviews/r7_repros/codex/` (받은 패키지 10 파일, sha256 OK) ·
  `reviews/r7_repros/replay_ours_*.json` (수정 전/후 우리 실행).
- `reviews/R6_LEDGER.md` "Codex R7" 절 — 발견별 재현 관측·수정·테스트.
- `reviews/r6_repros/codex/` (6차 패키지 + 적응판·변이 감사), `reviews/r6_repros/codex_r6_mutation_audit.{py,txt}`.

## 8. 이후

GO 면 새 모델 설계 요구서(`docs/`) 초안 — §5 다섯 행 + R7 Q6 의 네 항목 구조. 문헌 입력은
`docs/LIT_19_20_FOR_NEW_MODEL.md`. U16·U17 은 사용자 기계 실측.
