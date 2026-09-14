# α·β 검증 하네스 R4 — Codex 리뷰

## 판정: NO-GO

**R3의 다섯 GO 조건이 모두 닫혔다는 판정은 내릴 수 없다. P1 6건과 P2 1건을 실행 확인했다.** 다만 원인 추론 철회, 정규화 표, 192값 회귀는 실제로 나아졌고 해당 종결은 인정한다.

이번 GO 기준은 외부 회신이나 본 실행 승인이 아니라 **“정본이 우리 새 모델의 설계 근거로 쓸 만한가”**다. 현재 정본·하네스의 성공 판정을 그대로 신뢰하는 데에는 NO-GO다. 아래처럼 관측의 적용 범위와 남는 가설을 분리한 **설계 요구서 초안 작성은 진행할 수 있다.** 비공개 자료가 없다는 이유나 이미 신고한 U항의 존재만으로 막는 판정은 아니다.

| 대상 | 확인값 |
|---|---|
| 저장소 | `yonghoon7153-source/Yonghoon-DEM-DFT` |
| 브랜치·범위 | `claude/bms-alpha-beta-verify` · `bms-balancing/`만 |
| 고정한 HEAD | `39a5fe06215710b16e9b42bf3dc3c04c63cb8663` |
| 포함된 변경 | R3 대응 `b0f1fbe`, 요청문/정밀도 오류 처리 `82c7dc8`, 실측 CSV `fb62342`, S-01 수정 |
| 요청문 | 붙여넣은 R4 요청과 해당 HEAD의 요청문을 모두 읽고 대조 |
| 변경 범위 | 대상 추적 파일 변경 없음. 별도의 리뷰 파일·임시 합성 fixture만 작성 |

## 1. 실제 실행 결과

전체 stdout/stderr·환경·대상 SHA·반례 파일 hash는 `harness_r4_replay_results.json`에 있다. 첫 실행의 환경 오류 기록도 `harness_r4_replay_initial_results.json`으로 보존했다.

| 검사 | 이번 실행 | 해석 |
|---|---|---|
| 기존 pytest 전체 | **65 passed in 9.98s**, rc 0 | 요청문 개수와 일치 |
| Windows 작업사본에서 묶음 shell 검사 | rc 2 | CRLF 때문에 shell 구문 해석 단계에서 실패. Git은 `i/lf, w/crlf`로 확인 |
| 임시 사본의 shell 줄바꿈만 LF로 정규화한 뒤 같은 검사 | rc 0 | Python 4·5단계 통과. **Octave 없음: 1~3단계 미실행** |
| 네 루트의 `compare_states` | rc 0 | 표와 혼합 소스 경고 확인 |
| 옛 R3 port/shape/artifact/denominator 반례 | 각각 rc 1 | 아래에서 멈춘 assertion의 범위를 따로 해석 |
| 옛 R3 noise 반례 | rc 0 | 철회의 근거가 여전히 성립 |
| R4 port 반례 | rc 0 | 20개 입력·정상 대조를 helper와 실제 공개 dispatcher subprocess로 실행 |
| R4 shape 반례 | rc 0 | 실제 Blend와 진단 함수를 합성 자료로 실행 |
| R4 inference 반례 | rc 0 | 산출물·회귀·평탄부/scale 경로 확인 |
| R4 execution 반례 | rc 0 | 두 process 게시 순서, 신선도, metadata, C21 확인 |

환경: WSL Ubuntu, Python 3.12.3, NumPy 2.5.3, SciPy 1.18.1, pandas 3.0.5, openpyxl 3.1.5, pytest 9.1.1. **반례 스크립트의 rc 0은 잘못된 결과와 정상 대조가 예상대로 재현됐다는 뜻이지 GO가 아니다.**

원본 MATLAB·실물 xlsx·문헌 OCP는 이 기계에서 재생하지 않았다. 새 86.01 mV 실측은 저장된 표/CSV의 산술과 새 함수의 합성 대조까지 확인했으며, 비공개 문헌곡선에서 독립 재산출했다고 주장하지 않는다. Windows 줄바꿈 오류는 코드 반례로 세지 않는다.

### 종결로 인정하는 것

- **R3-01:** 잔차 증가는 관측, 모델 오류/잡음/계측 조건은 후보라는 주요 문서 정정이 유지된다. 원인 후보를 “한 칸 좁혔다”는 주장을 다시 발견으로 세지 않는다.
- **R3-03의 계산:** 합법 Δγ와 501×400 격자 기준 최대·최근접 증인 계산은 독립적인 동일 격자 재계산과 일치한다. 옛 “상자 안” 반례는 이제 증인 없음으로 처리한다.
- **R3-04:** target/reference 분모와 GITT 6적합 집합이 일치한다. 잘못된 분모 이름·7적합 표기를 넣으면 실제 회귀가 실패한다.
- **R3-05/07의 원래 사례:** 단일 NaN 앵커·parameter는 rc 2, 누락 앵커는 rc 3, 선언된 g17 불일치는 rc 1. `--allow-partial`도 NaN 실패를 성공으로 바꾸지 않는다.
- **R3-08의 순차 all-failed 사례:** 종료 2로 바뀌고 옛 CSV를 보존한다. 그 직접 반례는 닫혔다.
- **R3-09:** 기존 CSV 한 값을 9.0으로 바꾸면 이제 원시값 대조에서 실제 상대차 769.826…으로 실패한다. C21은 더 이상 판정문의 수치만 읽지 않는다. 보존된 192값의 최대 상대차 4.042289976866168e-12는 유지된다.

12개 normalization 행의 matrix/degeneracy 대상·기준 parameter와 objective도 다시 원소별 일치했다. 현재 수치 기록이 전부 불신 대상이라는 판정은 아니다.

## 2. 재현 방법

ZIP의 다섯 Python 파일을 같은 디렉터리에 풀고, 해당 HEAD의 `bms-balancing` 절대경로를 전달한다. Linux/WSL, 대상 requirements와 pytest가 필요하며 원자료는 필요 없다.

```bash
python harness_r4_replay.py --target "$TARGET" --output r4.json
```

네 개별 반례에도 `--target "$TARGET"`을 준다. 실행 출력에는 정상 대조와 잘못된 결과를 함께 기록했다. 수정 후에는 “잘못된 결과가 재현된다”는 assertion을 새 정상 조건으로 바꿔 회귀로 사용할 수 있다. 대상 코드를 고쳐 놓고 검토한 것은 아니다.

## 3. P1 — GO 조건에 남은 반례

### R4-01 · 별도 잔차 분기가 정확한 γ 증인을 찾고도 모든 γ를 부정한다

위치: [ne_shape.py:319](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/scripts/ne_shape.py:319), [FINDINGS.md:1308](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/FINDINGS.md:1308).

재현: `python harness_r4_shape_repros.py --target "$TARGET"`의 `remaining_c_branch_counterexample`.

**입력:** 실제 Blend로 pristine γ=0.15, 측정 대상 γ=0.5를 만든다. 선택된 full-cell fitted γ라는 입력은 0으로 주고 PE와 용량은 같게 둔다. 이 fitted pair를 새 optimizer가 찾았다고 주장하지 않는다.

```text
합법적인 참 γ=0.5의 표현 오차        0.0 V
측정 변화                            62.44361590 mV
선택된 쌍의 변화                     26.24999362 mV
(b)/(a)                               0.42037914
선택된 적합의 잔차 >50mV              x 격자점의 68%
새 (d)가 실제로 찾은 증인             γ=0.5, Δ=+0.35
```

비율의 중간 분기는 이제 크기만 출력한다. 그러나 이후 `(c)`의 `worst_over > 30` 분기가 다음을 출력한다.

> “γ 를 어떻게 고르든 남고, a_NE·b_NE 가 … 흡수한다 = LAM_NE·LLI 에 계통 편향.”

**왜 실패하는가:** 현재 선택된 γ의 넓은 잔차를 모든 γ에서 제거할 수 없는 잔차로 바꿔 말한다. 같은 실행에서 얻은 정확한 증인과 모순된다. 어느 parameter가 흡수하는지도 이 진단으로 결정되지 않는다.

**시험이 놓친 이유:** 옛 저비율 fixture는 50mV 초과점이 18%라 이 `>30%` 분기에 들어가지 않는다. 소스 검사도 “모델 부적합”, “상자 안”이라는 두 표현을 보지만 잔존 문구에는 둘 다 없다.

**최소 조건:** `(c)`도 선택된 γ에서의 max/RMS/초과점 비율까지만 보고한다. 광범위 잔차가 있어도 합법 γ에서 정확히 맞는 경우를 추가하고, 증인과 반대인 보편적 결론을 내리지 않도록 검사한다. 직접 γ 적합 U9의 미착수 자체를 새 발견으로 센 것은 아니다.

### R4-02 · 정밀도 추정 경고 뒤에 다시 complete·종료 0을 내린다

위치: [verify.py:629](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/bms_balancing/verify.py:629), [751](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/bms_balancing/verify.py:751), [810](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/bms_balancing/verify.py:810).

재현: `python harness_r4_port_repros.py --target "$TARGET"`의 inferred/g14/unrecognized 사례.

CSV 열 전체를 정확한 0.125, Python 값 하나를 정확한 0.1259765625로 둔다. 절대차는 1/1024, 상대차는 약 0.775%다.

| 형식 근거 | 실제 결과 |
|---|---|
| 파일 `%.17g` 또는 명시 `--precision g17` | model_mismatch, rc 1 — 정상 |
| 선언 없음 | inferred, complete, worst_rel=0, rc 0 |
| 실제 `%.14g`로 쓴 파일의 선언 | inferred, complete, worst_rel=0, rc 0 |
| 미지원 선언 | inferred, complete, worst_rel=0, rc 0 |

**왜 실패하는가:** “추정”이라는 경고는 실제로 있다. 하지만 정밀도 근거의 불확실성이 최종 상태에 반영되지 않는다. `%.14g`에서는 Python 값을 같은 형식으로 출력해도 0.1259765625이므로 CSV의 0.125와 다르다. 이미 주어진 형식 정보를 버리고 짧은 토큰에서 넓은 허용량을 추정한다.

**최소 조건:** 정밀도 미상/미지원은 기본적으로 nonzero인 미완·별도 partial로 다룬다. 탐색적 추정을 허용해도 complete와 구별한다. `%.Ng`를 지원할 경우 해당 유효숫자의 반올림 구간을 계산하고, 지원하지 않으면 미지원이라고 멈춘다. R3 예시의 입력 경고만으로 “완전한 지원 범위의 일치만 0”은 닫히지 않았다.

### R4-03 · fixed 정밀도의 허용량이 실제 반올림 구간의 두 배다

위치: [verify.py:609](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/bms_balancing/verify.py:609), metric 판정의 [843](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/bms_balancing/verify.py:843). 같은 port 재현의 `fixed10_roundtrip_incompatible`.

```text
선언된 형식                  %.10f
CSV                           0.0123456789
Python full precision         0.01234567899
Python을 같은 형식으로 출력   0.0123456790  ← 다름
실제 절대차                   약 9e-11
반올림 반 단위                5e-11
현재 상대 수치 허용량          약 1.2346e-11
실제 판정                     complete, worst_rel=0, rc 0
```

차이는 반올림 반 단위와 수치 허용량의 합보다도 크다. `%.1f`의 0.1 대 0.199도 같은 문제로 통과했다. 실제로 같은 출력이 되는 0.01234567894와 0.149의 정상 대조도 실행했다.

**왜 실패하는가:** 한쪽 CSV만 소수 N자리로 반올림됐는데 `10^-N` 전체를 출력 반올림 허용량으로 준다. 보통의 최근접 반올림 구간은 반 단위이며 수치 차이는 별도다.

**최소 조건:** 명시된 producer의 반올림 규칙으로 토큰의 구간을 계산하고 별도의 수치 허용량을 적용한다. 전체 한 단위 안의 차이를 모두 “출력 반올림”으로 지우지 않는다. 이것은 선언이 없는 R4-02와 다른 경로다.

### R4-04 · 중복 schema가 NaN을 가리고 실제 안 읽은 열까지 비교 수로 센다

위치: [verify.py:509](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/bms_balancing/verify.py:509), [832](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/bms_balancing/verify.py:832). 같은 port 재현의 두 duplicate 사례.

1. 정상 4개 metric 뒤에 이름이 다시 `rmse_pocv`인 열을 붙이고 8개 값을 모두 NaN으로 둔다. 실제 결과는 **expected=40, compared=40, problems=[], complete, rc 0**이다.
2. 정상 앵커 앞에 같은 이름의 NaN 앵커를 한 줄 추가한다. 마지막 값이 dict에 덮어써지므로 **complete, rc 0**이다.

**왜 실패하는가:** metric은 `header.index(name)`으로 첫 번째 같은 이름의 열만 다시 읽고, 앵커는 파싱 중 중복 이력을 잃는다. 유한성 검사 전에 숫자가 사라지거나 다른 숫자로 대체된다. 유일한 NaN을 넣은 대조는 정상적으로 rc 2였다.

**최소 조건:** 앵커·metric 이름의 유일성을 파싱 단계에서 강제한다. 모호한 중복은 invalid/incomplete로 거부하고, 실제 고유 셀만 비교 수에 넣는다. `--allow-partial`이 허용하는 옛 schema와 malformed 중복을 구별한다. 현재 네 recompare 파일에 중복이 있었다는 뜻은 아니다.

### R4-05 · U1의 ‘Inf는 없고 빈 표본 가드만 다르다’는 설명이 성립하지 않는다

위치: [FINDINGS.md:921](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/FINDINGS.md:921), [925](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/FINDINGS.md:925), [model.py:353](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/bms_balancing/model.py:353), [408](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/bms_balancing/model.py:408).

재현: `python harness_r4_inference_repros.py --target "$TARGET" --case plateau`.

**입력:** 합성 forward를 유한·연속·비감소인 `V(x,p)=max(0,x-(p[0]-1.1))`로 둔다. 실제 경계에서 seed 0으로 50개 parameter를 뽑아 production의 dQ/dV·RMSE·auto-scale 경로를 실행한다. 평탄부의 0인 dV/dQ가 역도함수에 Inf를 만든다.

```text
raw RMSE:                           유한 14개, Inf 36개, NaN 0개
문서에 적힌 원본식의 유효 표본 수:   50개 — 빈 표본 아님
그 원본식의 하위 절반 평균:          Inf
현재 Python scale:                   0.9985672999510923
같은 정상 parameter의 목적함수:     Python scale 3.0014347556
                                    보고된 원본 scale 2.0
Inf parameter를 최종 wrapper로 호출: 1e6 — 이 가드는 작동
```

**왜 실패하는가:** 최종 `__call__()`의 1e6 처리가 raw RMSE 직접 호출인 `_auto_scales()`를 감싸지 않는다. 문서가 보고한 원본식은 NaN만 제거하고, Python은 모든 비유한 값을 제거한다. 따라서 일반적으로 빈 표본 가드만 다른 것이 아니다.

**증거 범위:** 원본 MATLAB을 실행한 비교가 아니다. “원본” 쪽은 정본이 제시한 `NaN 제거 → 정렬 → 하위 절반 평균` 설명식을 실행했다. 확정한 것은 **공개 Python 실행이 문서의 Inf 배제 설명과 모순되며, 보고된 알고리즘과 이 합성 입력에서 갈린다**는 것이다. 이미 저장한 192값이나 실물 셀의 결과가 바뀐다고 주장하지 않는다.

**최소 조건:** U1의 동치 주장을 확인한 자료·유한 RMSE 영역으로 한정하거나 실제 nonfinite 정책을 일치시킨다. 새 모델 요구서에는 plateau/작은 기울기의 dQ/dV 정의, nonfinite scale 표본 처리와 개수를 명시한다. 원본에 추가 방어가 있다면 정본 설명도 갱신한다. 비공개 원본 전체를 다시 요구할 필요는 없다.

### R4-06 · 두 profile이 공유하는 `.part` 때문에 A가 B의 계산값을 게시하고 성공한다

위치: [verify.py:1156](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/bms_balancing/verify.py:1156).

재현: `python harness_r4_execution_repros.py --target "$TARGET"`의 `shared_profile_part`.

**입력/순서:** 두 process가 같은 `--out profile.csv`를 사용한다. 참조·자유 적합과 각 γ의 optimizer는 범위 안의 유한한 성공 결과를 돌려주는 합성 대역으로 둔다. A의 `a_NE`는 1.1, B는 1.3이다. 실제 production CSV writer를 실행하며, 파일을 닫은 뒤 `os.replace`에 들어가는 지점에서만 barrier로 순서를 고정한다.

```text
1. A가 profile.csv.part에 A의 행을 쓰고 닫음; 교체 직전 대기
2. B가 같은 profile.csv.part에 B의 행을 쓰고 닫음
3. A가 그 경로를 profile.csv로 교체 → 실제로는 B의 행 게시
4. A: rc 0 / wrote 출력
5. B: 자기 .part가 없어 FileNotFoundError / rc 1
최종 CSV a_NE: [1.3, 1.3]  (A가 계산한 [1.1, 1.1] 아님)
```

**왜 실패하는가:** `.part` 이름이 시도 전용이 아니다. 원자적 rename은 읽는 쪽의 반쪽 파일 노출을 줄이지만, 그 파일을 누가 계산했는지는 보증하지 않는다. 이번 시도의 계산과 게시 bytes가 분리된다.

**최소 조건:** 시도별 고유 임시 파일과 결과 식별자를 사용하고, 같은 목적지에 동시 실행을 허용할 정책을 정한다. 지원하지 않는다면 두 번째 시도를 명시적으로 거부할 수 있다. 결과와 metadata가 같은 시도를 가리키도록 최종 게시를 묶는다. 이 반례에서는 metadata까지 기록했다고 주장하지 않는다.

**Q4의 touch 경계도 실행 확인했다.** 현재 `run` helper는 아무것도 안 하는 명령은 rc 1로 거부하지만, 옛 CSV를 `touch()`만 하는 명령에는 **내용 hash가 그대로인데 rc 0·OK**를 준다. `find -newer`는 최근 시각을 보지 계산·시도 식별을 보지 않기 때문이다. 이 경계 시험을 현재 optimizer가 실제로 touch한다고 과장하거나 별도 P1로 중복 집계하지 않는다. 위 공유 `.part`는 실제 producer 게시 경로에서 같은 종류의 결속 실패가 발생하는 예다.

## 4. P2 — S-01의 수정 범위

### R4-07 · 코드가 같은 채로 출력 둘을 차례로 재생성하면 두 번째 metadata는 다시 dirty다

위치: [provenance.py:40](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/scripts/provenance.py:40), [run_states.sh:42](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r4-target/bms-balancing/scripts/run_states.sh:42).

같은 execution 재현의 `sequential_provenance`. 임시 Git 저장소에 코드와 output 두 개를 추적한다. output 100을 새로 쓰고 **실제 `write_meta` helper**를 실행한 뒤, output 200도 같은 방식으로 쓴다.

```text
100 metadata: git_dirty=false
200 metadata: git_dirty=true
수정된 추적 파일: out/100.csv, out/200.csv
코드 diff: 없음
```

**원인:** 현재 output 하나만 제외하므로 이전 단계에서 다시 쓴 다른 output을 코드 변경으로 해석한다. 현재 artifact 자신의 수정만 무시하는 직접 S-01 시험은 통과하지만, “실행 코드가 해당 commit과 같았나”라는 플래그의 설명과는 여전히 다르다.

**최소 조건:** `code_dirty`와 input/output 상태를 분리하거나, 실행 시작 시점의 명시된 코드 집합을 기록한다. 단순히 모든 산출물을 무작정 제외하면 계산 입력으로 쓰는 artifact의 변경도 숨길 수 있으므로 역할을 구분해야 한다. 이 false-positive metadata 문제 단독으로 설계 초안을 막지는 않는다.

## 5. R3의 다섯 GO 조건과 아홉 발견 재판정

| R3 §5 조건 | R4 판정 | 근거 |
|---|---|---|
| 1. 원인·표현 주장 | **부분** | 주요 문서 철회와 γ 여유 계산은 인정. 별도 `(c)`에 R4-01 잔존; U1 범위에 R4-05 |
| 2. 표의 분모·역할·집합 | **닫힘** | target/reference/6 GITT 표 및 이름·개수 음성 대조가 작동 |
| 3. 비교 성공 조건 | **부분** | 원래 단일 NaN·CLI 경로는 닫힘. 추정/반올림/중복 schema에 R4-02~04 |
| 4. 이번 실행과 산출의 연결 | **부분** | 순차 all-failed는 닫힘. 공유 `.part`의 R4-06 및 touch 경계 |
| 5. 192값의 원시 수치 회귀 | **닫힘** | C21이 9.0 변경을 재계산으로 거부 |

| R3 발견 | 이번 판정 |
|---|---|
| 01 noise-only 반례 | 철회 종결 |
| 02 표현 가능한 곡선의 원인 진단 | 원래 분기는 종결, 별도 광범위 잔차 분기는 R4-01로 미종결 |
| 03 상자 여유 산술 | 고정 기준·명시된 격자 범위에서 종결 |
| 04 분모·개수 | 종결 |
| 05 앵커/parameter 누락·NaN | 원래 사례 종결, 중복 파싱 경계 R4-04 |
| 06 값 길이 정밀도 추정 | 선언/옵션 경로 진전, R4-02·03 때문에 부분 |
| 07 실패의 process 전달 | 시험한 상태 매핑과 partial 예외는 종결. 잘못된 complete 자체는 별도 문제 |
| 08 전부 실패한 profile의 옛 파일 | 원래 순차 사례 종결, 새 임시 파일 게시 구조는 R4-06 |
| 09 판정문만 보는 192값 시험 | 종결 |

옛 반례 스크립트는 첫 assertion에서 멈추므로 rc 1만으로 뒤의 모든 축이 닫혔다고 세지 않았다. 이번 판정은 분리한 정상·음성 대조와 새 경로 실행을 추가한 결과다.

## 6. 질문 5개에 대한 답

### Q1. 현재 자료로 더 구분할 수 있는가?

**관측 유지·후보 가설로 낮춘 대응은 충분하다.** 상태당 곡선 하나로 잡음과 표현 오류를 유일하게 분리한다고 약속할 수는 없다. 그래도 자료·참조·소스를 맞춘 뒤 SOC별 잔차, 전처리/평활/미분 방식에 대한 민감도, 제한된 비교 모델의 미사용 구간 예측, half-cell의 직접 제약 적합을 진단할 수 있다. 이것들은 앞으로 할 시험이지 이번 리뷰에서 실물 자료로 수행한 결과가 아니다.

인접점이 상관될 수 있으므로 임의 점 분할을 독립 자료 검증으로 부르지 않는다. 간격 균일성 검사만으로 원자료/재표본 이력(U2)을 종결할 수도 없다. 원래 일정 간격으로 계측한 자료와 재표본 자료는 둘 다 균일할 수 있다. 처리 이력에는 원시 timestamp·export 설정 같은 독립 근거가 필요하다.

### Q2. 새 γ 여유와 증인의 한정은 적절한가?

**주요 계산·표·sidecar의 격자 한정은 적절하다.** 합법 증인은 그 γ와 x 격자에서 기준 대비 진폭이 문턱 이상임을 보인다. 증인 없음은 샘플링한 γ 중 없다는 뜻이다. 연속 γ 가족의 전역 상한 또는 연속 영역의 최근접점을 자동으로 증명하지 않는다.

300_0009는 **“선택된 γ_ref를 고정하고, γ 501점·x 400점에서 정규화 후 진폭을 내는 증인을 찾지 못했다”**로 옮기는 것이 정확하다. 86.01 대 119.34를 그 범위의 관측으로 보존할 수 있다. 현재 자료의 연속 가족에 숨은 증인이 실제로 있다고 발견한 것은 아니다.

또 기록된 **최근접 증인이 음의 Δγ**라는 사실은 모든 증인이 음의 방향뿐이라는 뜻이 아니다. 100의 선택된 Δγ도 음수이므로 “100·200 모두 적합과 방향도 다르다”는 문장은 200에만 적용된다. 크기의 차이는 둘 다 남는다. 이 두 표현 정정은 별도 P1로 세지 않았다.

### Q3. 정밀도 우선순위와 partial 정책은 괜찮은가?

실제 우선순위는 **명시 옵션 → 파일 선언 → 추정**이다. 요청문 Q3의 “선언 → 옵션”과 순서가 다르다. 명시 override 자체는 사용자 선택이므로 별도 결함으로 세지 않는다. 대신 충돌한 선언·옵션과 실제 적용 정책을 함께 기록해야 한다. 느슨한 override 아래의 complete를 원래 선언된 전정밀도 일치로 읽으면 안 된다.

`partial=3`, 명시적인 `--allow-partial`만 0으로 바꾸는 경로는 시험한 옛 schema에서 작동한다. NaN은 그 옵션으로도 rc 2다. 문제는 **정밀도 추정은 예외 옵션 없이 complete·0**이 되는 R4-02다. `%.Ng, N<15`는 주어진 형식을 버릴 것이 아니라 지원하거나 미지원으로 구분해야 한다.

### Q4. 시각 도장이 놓치는 경우는?

**touch만 해도 통과함을 실행 확인했다.** 최근 수정 시각은 시도와 계산 bytes를 연결하는 증거가 아니다. 반대로 낮은 시각 정밀도나 시간을 보존한 복사에서도 한계가 있으므로 시각은 보조 진단으로 쓰는 편이 맞다. 실제로 필요한 것은 시도별 고유 산출과 게시된 bytes/metadata의 연결이다. 공유 `.part` 반례는 그 연결이 아직 없는 생산 경로다.

### Q5. 정본 결론 다섯 개를 관측 열에 그대로 옮겨도 되는가?

**그대로 복사하기보다는 다음 범위가 붙은 다섯 행으로 옮기는 것이 맞다.**

| 관측 항목 | 요구서에 붙일 범위 |
|---|---|
| 포팅 일치 | 보존된 네 조합 192 출력값의 경험적 일치. 네 함수의 원본 소스 대조는 사용자 수행 기록. 모든 입력의 동치가 아니며 R4-05의 nonfinite 영역을 구분 |
| 음수 LAM_NE | 공개 5개 행·고정 기준의 부호 산술과 행별 임계. 경계 변경 재적합의 인과는 미확립 |
| 파우치 폭 순위 | 해당 네 상태·소스·설정에서 찾은 탐색 하한의 순위. 전체 식별성 또는 정확도 보장은 아님 |
| 원통형/PE 대조·재척도화 | 각 소스 집합, 분모, max/max 등의 통계량을 명시한 기술 결과. 원인 배제나 공유 가능값 증명은 아님 |
| 잔차·γ 변화 | 상태별 RMSE 증가와 선택된 γ 쌍의 진폭비; 필요시 고정 기준의 유한 격자 여유를 추가. 원인·보상 경로는 가설 |

이 관측 뒤에 후보 원인, 구분 시험, 채택 기준, 남는 한계를 적는 작업은 진행 가능하다. 측정 NE 표현·PE 기준 선택·잡음 목적함수는 비교할 설계 후보이지 이미 확정된 해법이 아니다.

## 7. 최소 후속 조건

1. R4-01의 별도 진단 분기를 기술 통계로 낮추고 광범위 잔차의 참 가족원 대조를 추가한다.
2. R4-02~04의 정밀도 근거·반올림 구간·중복 schema를 실제 complete/종료 코드와 연결한다. 지원 범위를 좁혀 명시적으로 거부하는 것도 종결 방향이다.
3. R4-05의 소스 동치 주장을 확인한 영역으로 한정하고 nonfinite 정책을 명시한다. 비공개 원본 독립 재실행으로 바꾸어 말하지 않는다.
4. R4-06의 임시 파일을 시도별로 분리하고, 동시 목적지 사용을 지원하거나 명시적으로 차단한다. 시각만으로 계산과 게시를 연결하지 않는다.
5. P2 R4-07은 코드 상태와 산출물 상태를 분리해 후속 정리한다. 이것 하나로 요구서 초안을 막지는 않는다.

**최종 NO-GO: R3의 다섯 조건 전체 종결과 현재 하네스 성공 판정의 무조건적 채택에는 반대한다.** 닫힌 관측·표·192값 증거는 그대로 보존하고, 위 범위로 새 모델 요구서 초안을 진행할 수 있다. 알려진 미결을 새 발견으로 반복하거나 모든 추가 실험을 끝내야만 초안을 쓸 수 있다는 판정은 아니다.

## 재현 패키지

`harness_r4_replay.py`와 port/shape/inference/execution 네 probe, 최종·초기 실행 JSON, 본 보고서와 분야별 보조 보고서를 포함한다. 보조 보고서는 분야별 번호를 쓰므로 **발견 번호와 최종 집계의 정본은 이 문서의 R4-01~07**이다. 원자료·리뷰 대상 저장소 자체는 ZIP에 넣지 않았다.
