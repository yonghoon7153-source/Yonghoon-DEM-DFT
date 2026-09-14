# 적대적 리뷰 요청 — 5차 라운드 · α·β 검증 하네스 (`bms-balancing/`)

4차(대상 `39a5fe0`)는 **NO-GO** (P1 6 · P2 1, `reviews/R4_CODEX.md`). 일곱 건 전부 우리 트리에서 재현됐고
(`reviews/r4_repros/replay_ours_39a5fe0.json` — 12 단계 rc 일치), 반박 성립 없음. 이 판은 그 일곱 건 + 보류
S-02 의 대응이다 (`reviews/R4_LEDGER.md`). GO 기준은 R3 §5 의 다섯 조건에 대한 R4 §5 의 재판정
("부분" 이던 1·3·4 조건)이다. 목표는 같다: **"정본이 우리 새 모델의 설계 근거로 쓸 만한가"**.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | 이 파일이 들어 있는 커밋 (`git log -1`; R4 대응 본체는 `274f1f8`) |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 소유 |
| 범위 | `bms-balancing/` 만 |
| 정본 | `FINDINGS.md` + `out/` (+ `.meta.json`). 이 요청문의 숫자는 사본 |
| 저장소에 없는 것 | 원본 MATLAB · 원자료 xlsx · 문헌 OCP → `BMS_DATA_ROOT` (R3·R4 와 같음) |
| 우리 환경에서만 되는 것 | U12 — 네 루트 × 네 상태 `eval` 의 `# scale_audit` 줄: **실행 완료**, 16 build 전부 Inf 0 · NaN 0 (`out/scale_audit_eval.txt`, GITT · Li · seed 0) |

```bash
git clone -b claude/bms-alpha-beta-verify https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT
cd Yonghoon-DEM-DFT/bms-balancing && git checkout <이 파일이 든 커밋>
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest tests/ -q                       # 원자료 불필요. 74 passed 기대
bash matlab/tests/run_all.sh                      # Octave 없으면 4·5 단계 (shell 은 .gitattributes 로 LF 고정)
# R4 반례 재생 — 대상 SHA 가 39a5fe0 이어야 돌므로 worktree 로:
git worktree add /tmp/r4 39a5fe0 && python3 reviews/r4_repros/harness_r4_replay.py --target /tmp/r4/bms-balancing --output /tmp/r4.json
# 수정된 트리에서는 반례의 '재현' assertion 이 실패해야 한다:
python3 reviews/r4_repros/harness_r4_port_repros.py --target "$PWD"        # inferred_precision_false_complete 가 model_mismatch(partial) 에서 AssertionError
python3 reviews/r4_repros/harness_r4_shape_repros.py --target "$PWD"       # 보편 판정 문구 부재에서 AssertionError
python3 reviews/r4_repros/harness_r4_execution_repros.py --target "$PWD"   # shared_profile_part: B 도 rc 0 → AssertionError
python3 reviews/r4_repros/harness_r4_inference_repros.py --target "$PWD" --case plateau   # 그대로 재현 — 차이 자체는 사실 (§2 R4-05)
```

## 1. 검증 — 2026-09-11, 이 트리, 작업트리 clean

| 검사 | 결과 |
|---|---|
| `pytest tests/ -q` | 74 passed (R4 신규 9 · R3 테스트 4 개정 · S-01 갱신) |
| `matlab/tests/run_all.sh` | 4·5 단계 통과 (Octave 없음) |
| R4 반례 4 스크립트 | 위 주석대로 — port·shape·execution 은 수정 뒤 assertion 실패(닫힘), plateau 는 재현(영역 한정으로 대응) |
| 변이 감사 | S-02 문서 변이 2 종(옛 문장 복원 · 정정 문장 삭제) 회귀 실패, 원본 통과. 첫 판 회귀는 "같은 방향" 이 다른 문장에도 있어 변이를 놓쳤고, 100 에 대한 문장으로 못 박아 고쳤다 |
| RED 확인 | 신규 9 + 개정 3 이 옛 코드·문서(`d945402`)에서 12 실패 — 이유 확인 |

## 2. R4 일곱 건 + S-02 — 대응

| R4 | 판정 | 어디서 | 테스트 |
|---|---|---|---|
| 01 (c) 갈래의 보편 판정 | 닫힘 (코드+철회) | `ne_shape.py` (c) `>30 %`: 선택된 γ 에서의 max·rms·초과 비율만; "블렌드가 이 음극의 모양이 아니다 · 어떻게 고르든 · 계통 편향" 삭제; §0-2 행 | `test_r4_01_*` (γ 0.15→0.5, 선택 쌍 0.15→0.0, 68 % fixture + 판정문 소스 검사) |
| 02 추정·`%.14g`·미지원 선언이 complete | 닫힘 (코드) | `resolve_precision`/`parse_precision_spec`/`cell_tol`: 옵션 → 선언 → 추정. 추정 = `partial`(사유 "정밀도 추정", 종료 3), `--allow-partial` 은 스키마 누락만 0; `%.Ng` 는 첫 유효자리에서 N 자리 아래 반 단위; 해석 불가 선언 = `invalid`(2); 옵션이 선언보다 느슨하면 `partial` + `precision_conflict` 기록 (Q3) | `test_r4_02_*` (helper 4 + 공개 경로 2: 추정은 `--allow-partial` 로도 3) |
| 03 fixed 허용량 두 배 | 닫힘 (코드) | 반 단위 0.5·10⁻ᴺ; 판정 = 초과분/\|p\| (자리수 안 / ≤1e-9 수치 잡음 / 모델 차이) | `test_r4_03_*` (`%.10f` 0.0123456789 vs …894 complete / …899 갈림; `%.1f` 0.149 / 0.199) |
| 04 중복 열·앵커 | 닫힘 (코드) | `dd_eval_csv_audit`: 중복 앵커·중복 열·열 수 불일치·숫자 아닌 칸 → `invalid`, 비교 0 | `test_r4_04_*` |
| 05 U1 "Inf 안 나옴·가드 둘뿐" | 닫힘 (한정+감사+**실측**) | §1-13: 동치를 scale 표본 전부 유한한 영역으로 한정, 비유한 정책 차이(원본 NaN 만 / 포팅 Inf 도) 명시, "Inf 안 나옴" 철회; `Objective.scale_audit`(n·유한·Inf·NaN) + `NONFINITE_SCALE_POLICY`; `eval` `# scale_audit` 줄, degeneracy JSON `scale_audit`/`ref_scale_audit`. 정책을 원본에 맞추는 대신 영역 한정을 택했다. 실측(U12): 4 루트 × 4 상태 16 build 전부 Inf 0 · NaN 0 → GITT · Li · seed 0 범위에서 영역 안; 다른 Si 소스·step_005C 는 실측 밖으로 명시 | `test_r4_05_*` (평탄부 forward 50 표본 중 Inf ≥ 1, 감사 개수 일치, §1-13 문구), `test_u12_*` (사본 16 줄 전부 0 + §1-13 범위 문구) |
| 06 공유 `.part` · Q4 touch | 닫힘 (코드) | `atomic_write_csv`(시도별 `NamedTemporaryFile` → `os.replace`); `run_id_of`(`--run-id`/`BMS_RUN_ID`/uuid) 가 degeneracy JSON·matrix 행·profile 행에; `run_states.sh run`: 시도마다 id 를 만들어 명령에 주고 **파일 안에 그 id** 가 있어야 OK (시각 도장 제거); `write_meta`: id 확인·기록, 없으면 거부 | `test_r4_06_concurrent_*` (실제 두 process, `os.replace` 경계 barrier: A 게시 순간 B 가 읽은 내용 = A 의 값·`run-A`; 둘 다 rc 0; 최종 = B), `test_r4_06_run_helper_*` (touch → FAIL, id → OK, meta run_id, 없으면 거부) |
| 07 (P2) 두 번째 meta dirty | 닫힘 (코드) | `provenance.git_provenance`: `git_dirty`(산출 디렉터리 밖) + `git_modified_outputs`(안, 자신 제외) + `git_modified_code` — `out/` 을 숨기지 않는다; `ne_shape`·`write_meta` 가 쓴다 | `test_r4_07_*` (100→200 차례 재생성: 둘 다 dirty False, 200 의 modified_outputs=["out/100.csv"]; 코드 수정 → True) |
| S-02 (보류) | 닫힘 (정정) | §5-2: 100 은 방향 같음·크기 40 배, 200 반대; 300_0009 = "γ_ref 고정 · γ 501 × x 400 격자에서 증인 없음 (표집 기준)" (Q2) | `test_r4_docs_*` |

S-03(용량 축이 섞인 (a) vs 순수 γ 축의 가족 최대)은 Q2 의 한정어 판정에 따라 **기록 유지** — 용량 축을 뺀 (a) 재측정은 요구서의 구분 시험. S-04(증인 한쪽·가족 최대 세 행 동일)는 개선 후보로 열어 둔다.

## 3. 철회·정정 목록 (§0-2 에 추가된 R4 행)

"(c) 30 % 넘게 50 mV → 블렌드가 이 음극의 모양이 아니다 · γ 를 어떻게 고르든 남고 · a_NE·b_NE 가 흡수 = 계통 편향" (R4-01, 철회) · "U1 닫힘 — 남은 ≠MATLAB 은 빈-표본 가드 둘뿐, rmse 는 1e6 감시값이라 Inf 는 안 나옴" (R4-05, 유한 영역으로 한정) · "100·200 모두 크기도 방향도 다르다" (S-02, 100 은 같은 방향).

## 4. 지금 정본이 말하는 것 — R4 Q5 의 범위를 붙인 다섯 행 (요구서 관측 열의 초안)

| 관측 | 붙인 범위 |
|---|---|
| 포팅 일치 | 보존된 네 조합 192 출력값의 경험적 일치 (4.04e-12, TXT 원시값 재계산, 반 단위 0 규칙으로도 complete). 네 로컬 함수의 식은 사용자 대조 기록. **비유한 영역은 제외** — scale 정책이 다르다 (R4-05); 실측 16 build(GITT · Li · seed 0)는 전부 유한 표본이라 영역 안, 다른 Si 소스·step_005C 는 미실측 |
| 음수 LAM_NE | 공개 5 행 · 고정 기준의 부호 산술, 행별 임계 1.177~1.196. 경계 변경 재적합의 인과 미확립 |
| 파우치 폭 순위 | 네 상태 · 소스 · 설정에서 찾은 탐색 하한의 순위 4/4. 식별성·정확도 보장 아님 |
| 원통형/PE 대조 · 재척도화 | 소스 집합·분모·통계량을 명시한 기술 결과 (raw 5~10x, 대상 rmse 2.85x, pristine rmse 4.99x). 원인 배제·공유 가능값 증명 아님 |
| 잔차 · γ 변화 | 상태별 RMSE 증가(원통형 1.5~1.6x, 파우치 0.77x) · 선택된 γ 쌍 진폭비 3~16 % · γ_ref 고정 격자 여유(100·200 증인 있음 — 줄이는 쪽, 300_0009 격자에서 없음). 원인·보상 경로는 가설 |

## 5. 닫지 않은 것

| # | 무엇 | 상태 |
|---|---|---|
| U2 | pOCV 워크북 원자료/재표본 | 간격 균일성만으로는 못 닫는다 (Q1) — 원시 timestamp·export 설정 필요 |
| U3 | 원통형 차이의 원인 | 미확정 — 구분 시험은 요구서 항목 |
| U4~U8 | R3 와 같음 | 그대로 |
| U9 | γ 직접 제약 적합 · 참 가족원/비가족원 대조 · 공유 가능값 증인 | 미구현 |
| U10 | INTRO·HANDOFF 숫자 무검사, `tol_percent_of_best` ×100, 한정어 삭제 | 열림 |
| ~~U12~~ | 실제 자료의 scale 표본 Inf 개수 | **닫힘** — 16 build 전부 0 (`out/scale_audit_eval.txt`); 실측 밖(다른 Si 소스 7 종 · step_005C)은 새 실행의 감사 줄로 |
| S-04 | 증인 반대쪽 도달 여부 · 가족 최대의 상태 독립성 표기 | 개선 후보 |

## 6. 리뷰어에게 — 질문

1. R4-02 정책: 추정 = partial(3, `--allow-partial` 로도 0 아님), 옵션이 선언보다 느슨 = partial, 해석 불가 선언 = invalid. "완전한 지원 범위의 일치만 0" 을 만족하는가. `sig:N` 의 반 단위를 첫 유효자리 기준으로 잡은 것에 빈틈이 있는가 (`%g` 의 지수 표기 경계 등).
2. R4-06: run id 를 파일 안에서 `grep -F` 로 확인하는 결속이 충분한가 — 같은 목적지의 동시 실행은 각자 게시하고 마지막이 남는 정책(거부하지 않음)을 택했다. 거부가 더 맞는가.
3. R4-05: 정책을 원본에 맞추지 않고 영역 한정 + 감사로 닫은 선택. 새 모델 요구서의 "평탄부/작은 기울기 dQ/dV 정의 · 비유한 scale 표본 처리" 항목에 더 넣을 것.
4. R4-07: `git_dirty`(코드) / `git_modified_outputs` 분리에서 "입력으로 쓰는 artifact" 의 역할 구분이 충분한가 — `ne_shape` 는 `matrix_*.csv` 를 입력으로 읽으므로 그 수정이 `git_modified_outputs` 에 나오면 되는가, 아니면 입력 목록을 따로 적어야 하는가.
5. §4 의 다섯 행이 요구서의 관측 열로 그대로 쓸 만한가.

## 7. 실측 첨부

- `reviews/r4_repros/replay_ours_39a5fe0.json` — R4 반례 우리 재생 (39a5fe0 worktree, 12 단계).
- `out/scale_audit_eval.txt` — U12 실측 사본 (16 줄, 사용자 기계 274f1f8). 그 외 `out/` 변경 없음.

## 8. 이후

GO 면 새 모델 설계 요구서(`docs/`) 초안 — §4 의 다섯 행을 관측 열로, 후보 원인 · 구분 시험 · 채택 기준 · 남는 한계 순.
