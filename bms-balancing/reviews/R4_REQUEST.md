# 적대적 리뷰 요청 — 4차 라운드 · α·β 검증 하네스 (`bms-balancing/`)

3차(대상 `a432d23`)는 **NO-GO** (P1 9, `reviews/R3_CODEX.md`). 아홉 건 전부 우리 트리에서 재현됐고
(`reviews/r3_repros/replay_ours_a432d23.json` — 8 단계 rc 일치), 반박 성립 없음. 이 판은 그 아홉 건의
대응이다 (`reviews/R3_LEDGER.md`). 목표는 R3 와 같다: **"정본이 우리 새 모델의 설계 근거로 쓸 만한가"**.
R3 §5 의 다섯 조건을 기준으로 봐 달라.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | 이 파일이 들어 있는 커밋 (`git log -1`; R3 대응 본체는 `b0f1fbe`, 그 뒤 `--precision` 오류 처리 · `ne_shape` 실측 CSV `fb62342` · provenance S-01 수정) |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 소유 |
| 범위 | `bms-balancing/` 만 |
| 정본 | `FINDINGS.md` + `out/` (+ `.meta.json`). 이 요청문의 숫자는 사본 |
| 저장소에 없는 것 | 원본 MATLAB · 원자료 xlsx · 문헌 OCP → `BMS_DATA_ROOT` (R3 와 같음) |
| 우리 환경에서만 되는 것 | `scripts/ne_shape.py` 재실행 — **완료** (fb62342, (d) 열 6 개가 `out/ne_shape_GITT_Li.csv` 에 있다) |

```bash
git clone -b claude/bms-alpha-beta-verify https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT
cd Yonghoon-DEM-DFT/bms-balancing && git checkout <이 파일이 든 커밋>
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest tests/ -q                       # 원자료 불필요. 65 passed 기대
bash matlab/tests/run_all.sh                      # Octave 없으면 4·5 단계
# R3 반례 재생 — 대상 SHA 가 a432d23 이어야 돌므로 worktree 로:
git worktree add /tmp/r3 a432d23 && python3 reviews/r3_repros/harness_r3_replay.py --target /tmp/r3/bms-balancing --output /tmp/r3.json
# 수정된 트리에서는 반례의 '재현' assertion 이 실패해야 한다:
python3 reviews/r3_repros/harness_r3_port_repros.py --target "$PWD"       # missing_anchor → partial 에서 AssertionError
python3 reviews/r3_repros/harness_r3_shape_repros.py --target "$PWD"      # "상자 안" 부재에서 AssertionError
python3 reviews/r3_repros/harness_r3_artifact_repros.py --target "$PWD"   # CSV 9.0 변조 뒤 C21 회귀가 상대차 769.8 로 실패
python3 reviews/r3_repros/harness_r3_inference_repros.py --root "$PWD" --case denominator   # 옛 문장 부재에서 AssertionError
python3 reviews/r3_repros/harness_r3_inference_repros.py --root "$PWD" --case noise         # 그대로 재현 — R3-01 의 근거 (철회의 이유)
```

## 1. 검증 — 2026-09-11, 이 트리, 작업트리 clean

| 검사 | 결과 |
|---|---|
| `pytest tests/ -q` | 65 passed (R3 신규 9 + 개정 2 + 자체 발견 S-01 의 2) |
| `matlab/tests/run_all.sh` | 4·5 단계 통과 (Octave 없음) |
| R3 반례 5 스크립트 | 위 주석대로 — 넷은 수정 뒤 assertion 실패(닫힘), noise 는 재현(철회 근거) |
| 변이 감사 | R3-04 표 변조 4 종 · §5-2 (d) 표 변조 4 종 — 전부 회귀 실패, 원본 통과 |
| RED 확인 | 신규 9 + 개정 2 테스트가 옛 코드·문서(`d60e365`)에서 11 실패 — 이유 확인(종료 코드 0, `anchors_compared` 없음, "모델 부적합" 출력, "7 적합") |

## 2. R3 아홉 건 — 대응

| R3 | 판정 | 어디서 | 테스트 |
|---|---|---|---|
| 01 잡음만으로 잔차 표 재현 | 닫힘 (철회) | §0-1 · §0-2 · §1-12 잔차 문단 제목 "관측이며 원인은 미확정" + 반례 요지 · §7-3 · WORKING_STATE · HANDOFF · INTRO. "잡음 가설과 맞지 않는다 · U3 한 칸 · 제3의 답 지지" 삭제, 모델 부적합은 **후보 가설** | `test_r3_01_*` (SCOPE_DOCS 에서 취소선·인용 밖 주장 검사) |
| 02 표현 가능한 곡선에 '블렌드 아님' | 닫힘 (코드+철회) | `ne_shape.py` 판정문 세 갈래 모두 크기의 기술만, 원인 출력 없음; §5-2 | `test_r3_02_*` (합성 Blend γ 0.15→0.45, 쌍 0.15→0.16 실행 + 판정문 소스 검사) |
| 03 "상자 안" | 닫힘 (코드+철회+**실측**) | `ne_shape.gamma_headroom`: 합법 Δγ 구간 · 합법 γ 최대 변화(γ 격자 501 · x 400) · (a) 이상을 내는 γ_ref 최근접 합법 γ 증인(없으면 없음) → 출력 + CSV 열 6 (`legal_dgamma_neg/pos`, `gamma_family_max_mV`, `gamma_at_family_max`, `gamma_witness`, `gamma_witness_delta`). §5-2: γ_ref 0.2953 → [−0.295, +0.205], 외삽 100 ±0.066 · 200 ±0.106 · 300_0009 ±0.365(양쪽 밖). **실측 (fb62342)**: 100·200 증인 γ 0.221 / 0.177 (Δ −0.074 / −0.118, 줄이는 쪽 — 적합의 −0.002 / +0.017 과 다름), 300_0009 없음 (합법 최대 86.01 @γ=0 < (a) 119.34 mV; 정규화·모양 한정어) | `test_r3_03_ne_shape_*` (증인 ≈0.45 / 100 mV 오프셋에 증인 없음), `test_r3_03_committed_*` (§5-2 (d) 표 칸별) |
| 04 분모·개수 | 닫힘 (정정) | §1-12 표: 행 이름이 분모(`/rmse_pocv (대상 적합)`, `/ref_rmse_pocv (pristine 기준 적합)` 0.0244~0.0491 vs 0.0998~0.2450 · 4.99x/4.09x/4.44x · 겹침 아니오), 머리글 "6 적합, GITT"; 본문 R3-04 문단(재척도화 민감도 기술표, 겹침으로 원인·공유값 결론 안 함) | `test_section_1_12_physical_normalization_*` (머리글 개수·분모 역할·문장) |
| 05 앵커 누락/NaN·파라미터 NaN | 닫힘 (코드) | `_compare_dd_eval`: `anchors_expected/compared/missing_anchors`; 비유한 → incomplete; 누락 앵커/열 → `partial`(성공 아님, 문구 "부분 대조") | `test_r3_05_*` |
| 06 전정밀도 열이 전부 짧음 | 닫힘 (코드) | `resolve_precision`: `--precision g17|full|fixed:N` → 파일 `# printed_format` 선언 → 추정(출력에 "추정" 표시, `result["precision_source"]`). `dd_eval.m`(`RMSE_FMT`)·`mirror_dd_eval.py`·`eval --out` 이 선언을 적음 | `test_r3_06_*` (옵션·선언·추정 표시·`%.10f` 선언의 과교정 없음·producer 소스 검사) |
| 07 종료 코드 0 | 닫힘 (코드) | `EXIT_BY_STATUS`: 0 complete · 1 anchor/model mismatch · 2 incomplete/empty/invalid option · 3 partial (`--allow-partial` 로만 0) | `test_r3_07_*` (별도 process 5 경우) |
| 08 all-failed profile 이 옛 CSV 재사용 | 닫힘 (코드) | `cmd_profile`: `.part` → `os.replace`; 행 없으면 종료 2, 옛 파일 보존. `run_states.sh run`: 시작 도장보다 새로 쓰인 파일만 OK(`find -newer`), 아니면 FAIL + "이번 실행이 새로 쓴 파일이 아니다" | `test_r3_08_profile_*`, `test_r3_08_run_states_*` (원본 shell helper 추출 실행) |
| 09 192 값 회귀가 판정문만 봄 | 닫힘 (테스트) | TXT 원시값 vs CSV 직접 재계산(앵커 16·metric 32·parameter 동일) + 같은 값으로 비교기 실행(`precision="g17"`, complete) → 판정문 숫자·§1-8 숫자 대조. §1-8 R3 정정 문단(추정이었음을 명시) | `test_section_1_8_192_values_*` |

## 3. 철회 목록 (§0-2 에 추가된 R3 행)

"부적합이 사이클과 함께 커진다 — 잡음 가설과 맞지 않는다 · U3 한 칸 · 제3의 답 지지" (R3-01) · "측정 NE 가 블렌드 모양이 아니라는 쪽을 가리킨다" (R3-02) · "같은 크기를 낼 Δγ 는 +0.07~+0.37 로 상자 안" (R3-03, 거짓) · "물리 단위(pristine 적합의 rmse) … 파우치 7 적합" (R3-04, 대상 적합·6 적합).

## 4. 지금 정본이 말하는 것 (§0-1 R3 정정판)

1. 포팅의 forward model 은 원본과 같다 — 192 값 최대 상대차 4.04e-12, **TXT 원시값에서 재계산**; 전정밀도는 R2 판 CSV 에서는 추정이었고 앞으로의 CSV 는 선언한다 (§1-8). dQ/dV 전사 함수는 원본과 줄 단위 일치 (§1-13).
2. §2-1: 강한 음수 LAM_NE 5/5 는 「대상 상한·기준 자유」의 부호 산술 (행별 임계 1.177~1.196). 경계 변경 재적합의 인과는 미확립. (변경 없음)
3. §1-10: 파우치 네 상태의 탐색 하한 폭 순위 LAM_NE 최광·LLI 최협 4/4 (절대 폭). (변경 없음)
4. §1-12: 원통형 LLI 하한 폭 raw 5~10 배; 분모에 따라 2.9(대상 rmse)~10.5(raw) — 재척도화 민감도 기술표. 파우치 PE 고정 실험은 그 폭을 만들지 않았고 LAM_PE 에서는 원통형 패턴 재현. 외곽 범위 겹침은 공유 가능값 미확정.
5. 원통형 적합 잔차는 사이클과 함께 1.5~1.6 배 커진다 — **관측**. 원인(모델 부적합·상태별 잡음/측정 조건·보상)은 미확정; 모델 부적합은 후보 가설. 선택된 풀셀 γ 쌍의 진폭비는 3~16 % — 표현력·원인 판정 아님.

## 5. 닫지 않은 것

| # | 무엇 | 상태 |
|---|---|---|
| U2 | pOCV 워크북 원자료/재표본 | 간격 균일성 검사 대기 (우리 원자료로 가능) |
| U3 | 원통형 차이의 원인 | **미확정으로 되돌림** (R3-01) — 구분 시험은 새 모델 요구서 항목 |
| U4·U5·U6·U7·U8 | R3 와 같음 (provenance 재실행 미실행 · fixedhc B축 · 폭은 하한 · 기준/대상 분리 · 옛 profile 수렴 미확인) | 그대로 |
| U9 | γ 직접 제약 적합(표현력) · 참 가족원/비가족원 대조 · 공유 가능값 증인 | 미구현 |
| U10 | INTRO·HANDOFF 숫자 무검사, `tol_percent_of_best` ×100, 한정어 삭제 | 열림 |
| ~~U11~~ | `out/ne_shape_GITT_Li.csv` 의 (d) 열 6 개 | **닫힘** — fb62342 재실행, §5-2 (d) 표 + 칸별 회귀 |
| S-01 (자체 발견) | 재생성 meta 의 `git_dirty` 가 산출물 자신의 재작성으로 늘 true (fb62342 meta 가 그렇다) | **닫힘 (코드)** — `provenance.git_state(exclude=…)`, 두 producer 가 넘김; 이미 커밋된 meta 의 true 는 그 원인으로 읽을 것 (커밋 diff = CSV·meta 만) |

## 6. 리뷰어에게 — 질문

1. R3-01 대응이 충분한가 — "관측 유지 · 원인은 후보 가설" 로 낮춘 것 외에, 현재 자료(상태당 곡선 하나)로 할 수 있는 구분 시험이 있는가.
2. R3-03 의 (d) 실측: 100·200 의 증인이 γ 를 **줄이는** 쪽에만 있고(0.221/0.177) 300_0009 는 합법 최대 86.01 mV < 119.34 mV 다. "300_0009 의 정규화 후 진폭은 γ 하나로는 닿지 않는다" 까지만 적었다 — 이 한정(정규화 −27 %, 모양 아님)이 충분한가, 격자(γ 501 · x 400)와 최근접 증인 정의가 적절한가.
3. R3-06 정책: 선언 → 옵션 → 추정 순서와 `%.Ng (N<15)` 을 추정으로 넘기는 처리, R3-07 의 `partial=3`/`--allow-partial` 정책이 "완전한 지원 범위의 일치만 0" 을 만족하는가.
4. R3-08 의 신선도 검사(`find -newer` 도장)가 놓치는 경우 — 예: 명령이 옛 파일을 touch 만 하고 내용을 안 바꾸는 경로.
5. 새 모델 요구서 초안을 R3 Q5 표(`관측 → 후보 원인 → 구분 시험 → 채택 기준 → 남는 한계`)로 쓰려 한다 — 정본 결론 5 를 그 골격의 "관측" 열에 그대로 옮겨도 되는가.

## 7. 실측 첨부

- `reviews/r3_repros/replay_ours_a432d23.json` — R3 반례 우리 재생 (a432d23 worktree, 8 단계).
- `out/recompare/dd_eval_*_r2.{csv,txt}` — 변경 없음; 회귀가 원시값에서 재계산.
- `out/ne_shape_GITT_Li.csv` (+ `.meta.json`) — fb62342 재실행분, (d) 열 6 개 (meta 의 `git_dirty: true` 는 S-01 의 증상 — 커밋 diff 는 CSV·meta 뿐).

## 8. 이후

GO: R3 §5 다섯 조건이 닫혔다고 보면 새 모델 설계 요구서(`docs/`) 초안으로 간다 — 정본의 관측 5 + 후보 가설 + 구분 시험 목록. 보존: 이 커밋의 `out/`·`reviews/`.
