# 적대적 리뷰 요청 — 9차 · α·β 검증 하네스 (`bms-balancing/`)

8차(대상 `a22da33`)는 **NO-GO** (P1 4 · P2 4, `reviews/R8_CODEX.md` · 패키지 `reviews/r8_repros/codex/`). 여덟 건 전부
수정 전 HEAD 에서 재현 → RED(`tests/test_r8_codex.py`) → 수정 → GREEN 으로 닫았다 (`reviews/R6_LEDGER.md` "Codex R8").
목표는 같다: **"정본이 우리 새 모델의 설계 근거로 쓸 만한가"**. GO 기준: R3 §5 + R5 §4 + R6 출처 결속 + R7 §6 + R8 §6.

## 0. 대상

| 항목 | 값 |
|---|---|
| 커밋 | 이 파일이 든 커밋 (`git log -1`). 직전 리뷰 대상 `a22da33` |
| 브랜치 | `claude/bms-alpha-beta-verify` — `bms-balancing/` 만 |
| 정본 | `FINDINGS.md` + `out/` (+ `.meta.json`). **현행 out/ 12 개는 provenance-incomplete** (§4) |
| 저장소에 없는 것 | 원본 MATLAB · 원자료 xlsx · 문헌 OCP → `BMS_DATA_ROOT` |
| 8차 대비 새것 | R8-01~08 닫음 (코드 5 · 테스트/도구 3) · c6_04 변이를 값으로 · 현행 정본 범위 제한 · U18 등록 |

```bash
git clone -b claude/bms-alpha-beta-verify https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT
cd Yonghoon-DEM-DFT/bms-balancing && git checkout <이 파일이 든 커밋>
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python3 -m pytest tests/ -q                # 155 passed 기대. 원자료 불필요
bash matlab/tests/run_all.sh               # Octave 없으면 4·5 단계만

git archive --format=tar bfc4623^ bms-balancing/out | tar -x -C /tmp/r9base      # 과거 baseline
export R6_OLD_OUT=/tmp/r9base/bms-balancing/out

python3 reviews/r6_repros/codex_r6_mutation_audit.py            # 8/8 CAUGHT (c6_04 는 값으로) · 선택 0 이면 '오류'·rc 1
python3 reviews/r6_repros/codex/replay_codex_r6_adapted.py --target .   # R6 적응판 "mode": "full" 6/6
python3 reviews/r6_repros/codex/mutation_adapted.py             # 5/5 CAUGHT
python3 reviews/r7_repros/replay_codex_r7.py --target .         # R7 probe 닫힘 재생 — 도달·상태·멈춘_곳 (R8-07)
# 8차 패키지 그대로 (수정 **전** 을 재려면 a22da33 worktree 에서; 수정 뒤에는 각 probe 가 자기 반례 assertion 에서 멈춘다)
python3 reviews/r8_repros/codex/r8_inference_repros.py --target . --old "$R6_OLD_OUT" --case all
python3 reviews/r8_repros/codex/r8_claims_repros.py    --target . --case all
python3 reviews/r8_repros/codex/r8_port_repros.py      --target . --old "$R6_OLD_OUT" --case controls
python3 scripts/check_u14.py --new out --schema-only            # rc 2: 출처 열 누락 = provenance-incomplete (§4)
```

## 1. 검증 — 방금 실행

| 검사 | 명령 | 출력 |
|---|---|---|
| 전체 회귀 | `python3 -m pytest tests/ -q` | `155 passed in 93.02s` (이 컨테이너) |
| MATLAB 스모크 (Octave) | `bash matlab/tests/run_all.sh` | `PASS — 실패 0: []` · `전부 통과` (이 컨테이너의 Octave) |
| 변이 감사 (우리 테스트) | `codex_r6_mutation_audit.py` | `8/8 CAUGHT · MISSED: 0` · c6_04 는 **값**으로 (`codex_r6_mutation_audit.txt`) |
| 적응판 변이 감사 | `mutation_adapted.py` | `5/5 CAUGHT · MISSED: 0` · baseline 지정 시 `mode: full` 6/6 (`mutation_adapted.txt`) |
| R7 닫힘 재생 | `replay_codex_r7.py --target .` | R7-01~06 **전부 도달 True · 반례 소멸** (`replay_codex_r7_after_fixes.json`) |
| 8차 패키지 재실행 (수정 뒤) | 위 세 명령 | 여섯 probe 전부 자기 반례 assertion 에서 멈춤 (`replay_ours_after_fixes/summary.json`) |

## 2. R8 여덟 건 — 재현과 수정

| ID | 수정 전 관측 (우리 HEAD) | 수정 | 회귀 |
|---|---|---|---|
| **R8-01** P1 | 같은 state 의 Kunz·Li 정상 묶음 둘 → Li 가 Kunz 를 덮어 1/1·예; `good+empty`·`good+absent` 도 1/1·예 rc 0 | inventory 를 축소 전에; Si 충돌은 `state\|si` 로 전부 보존; 요청 root 마다 roster, 없거나 관측 0 이면 미완 rc 2 | `test_d8_01` |
| **R8-02** P1 | data B/meta A 중단 상태를 "전부 갖춤·전부 같다·rc 0"; 출처 열을 요구하지 않아 현행 out/ 이 "전부 갖췄다" | `read_unit` 검증 snapshot 만 검사, 묶음 불일치는 broken → rc 2 · `PROVENANCE_COLS` 를 필수 스키마에 · 누락은 "provenance-incomplete" 로 이름 | `test_d8_02` |
| **R8-03** P1 | 요약 "측정 최대 10 mV" 가 γ-짝 부분집합에서, rc 0 | 측정은 requested 전부에서 · `pairing{requested,paired,missing}` 을 stdout·meta 에 · missing 이면 rc 3 | `test_d8_03` |
| **R8-04** P1 | profile 전체 identity 가 `.csv.log` 에만 — 실패 재시도가 잘라낸다 | 행마다 `consumed_inputs`·`ref_consumed_inputs` (CSV 자체) | `test_d8_04` |
| **R8-05** P2 | 중복 key 행이 dict 변환에서 사라져 "전부 같다" | 변환 전 유일성·행 수 검사 → diff | `test_d8_05` |
| **R8-06** P2 | 선택된 시험 0(rc 5)을 CAUGHT | `classify()`: rc 5·선택 0·수집 오류 = 오류 → rc 1 | `test_d8_06` |
| **R8-07** P2 | post-fix 폐쇄를 재생할 명령 없음 | `replay_codex_r7.py` — 도달·상태·멈춘_곳 별도 기록 | `test_d8_07` |
| **R8-08** P2 | `fired["v"]` 는 읽기 수 — meta schedule callback 을 꺼도 통과 | `published` 계수 + schedule 별 (기대, 관측) assert | `test_d8_08` |

**c6_04 자백**: 8차 요청문의 "이제 값으로 잡힌다" 는 틀렸었다 (여전히 KeyError). 변이를 옛 규칙 **두 자리**로 되살려 이번엔
`test_d8_08` 이 사본에 변이를 적용해 key "100" 아래 222 의 소비를 직접 확인한다.

## 3. 8차 질문에 대한 답

| Q | 답 |
|---|---|
| 1 미완 전파 | roster(R8-01)·paired subset(R8-03)·묶음/스키마/중복(R8-02·05) 닫음. 정적 문서 표는 요구서에서 관측마다 모집단/roster 를 적는 것으로 (Q6) |
| 2 두 번 읽기 | receipt 내구성(R8-04) 닫음. `ne_shape` 의 옛 γ + 현재 문헌 export 는 재적합 아닌 sensitivity 경계 — 기록만, 계약은 미결 (§6 Q3) |
| 3 export 정책 | 공통 snapshot 강제는 **아직** — §6 Q3 |
| 4 `auto` | 손으로 푼 옛 out/ 은 explicit historical 을 요구 — 남긴다 (문서로) |
| 5 U16·U17 | U16 → U17 순서 동의. **U18**(출처 열 보강 재실행)이 추가됐다 (§4) |
| 6 요구서 행 | 모집단/roster·completeness·입력 receipt·범위·후보 변경·대안·구분 실험·임계값·미계산 의미·evidence version |

## 4. 정본 범위 — 현행 `out/` 은 provenance-incomplete

숫자는 R7 과 바이트 동일(matrix 2,240 칸 · degeneracy 12 span · §5 표 35 칸)이고 묶음 12/12 True. 그러나 matrix/profile 8 개에
`ref_inputs_sha`·`consumed_inputs`·`ref_consumed_inputs` 가 없어 **기준 입력의 출처는 그 묶음에서 회수되지 않는다**.
`check_u14 --new out --schema-only` 가 rc 2 로 말한다. 보강은 **U18**(사용자 기계 재실행, 별도 destination → 비교·승격;
pathname 해시로 소급 채우지 않는다). 그때까지 인용은 "수치 그대로 · 기준 입력 출처 미기록" 으로 범위를 붙인다.

## 5. 닫지 않은 것 — 신뢰 경계

| # | 무엇 | 왜 열어 두나 |
|---|---|---|
| U18 | 현행 정본의 출처 열 보강 재실행 | 사용자 기계. 별도 destination 에서 비교·승격 |
| U16 · U17 | 옛 조합 재실행 · 끝점 witness 스키마 | 전과 같음 (R8 Q5 순서) |
| export 계약 | 기준·대상 공유 입력의 **같은 snapshot** 강제 | 지금은 양쪽 identity 기록만 (R8 Q3) |
| F01b · F08 · F2 · V6-09 · U2~U10 | 전과 같음 | — |

## 6. 질문

1. **R8-01 의 key 규칙**: Si 충돌 시 `state|si` 로 보존하고 같은 (state, si) 둘은 RuntimeError 로 거부한다 — "명시적 거부"
   와 "모델 층별 관측" 의 경계를 이렇게 그어도 되는가.
2. **R8-02 의 정본 범위**: 현행 12 개를 provenance-incomplete 로 제한한 채 §5 다섯 관측을 요구서 초안에 옮겨도 되는가
   (숫자는 동일, 기준 입력 출처만 미기록).
3. **export 계약**: 같은 실험의 기본 비교에 공유 workbook/문헌의 공통 snapshot 을 **강제**하려면 어디서 (build 호출자? run_states?)
   — 다른 export 는 명시적 sensitivity 모드로만.
4. **R8-03 의 rc 3**: 부분을 rc 3 로 두고 CSV/meta 에 pairing 을 남겼다. wrapper(`run_states.sh`)가 이것을 실패로 볼지
   부분으로 볼지 — 계약이 필요한가.
5. **U18 의 승격 규칙**: 재실행 산출이 현행과 수치 동일(비트 또는 인쇄 자릿수)일 때만 승격하는가, 환경 차이로 profile 행이
   또 움직이면 어떻게 하는가 (U16 과 겹친다).

## 7. 실측 첨부

- `reviews/R8_CODEX.md` · `reviews/r8_repros/codex/` (패키지 10 파일) · `reviews/r8_repros/replay_ours_a22da33_before/`
  (수정 전 재현) · `reviews/r8_repros/replay_ours_after_fixes/` (수정 뒤).
- `reviews/r7_repros/replay_codex_r7.py` (R7 닫힘 재생기) · `reviews/R6_LEDGER.md` "Codex R8" 절.

## 8. 이후

GO 면 새 모델 설계 요구서(`docs/`) 초안 — §5 다섯 행 + R8 Q6 의 열 구조. U16·U17·U18 은 사용자 기계 실측.
