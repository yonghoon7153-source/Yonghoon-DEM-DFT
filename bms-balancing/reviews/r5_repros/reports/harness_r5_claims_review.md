# R5 독립 검토 — 입력 출처·γ 한정·관측 주장

대상: `0cb7b7a380a90f61c1f25cabcb28204749b88076`, `work/harness-r5-target/bms-balancing`.
`reviews/R5_REQUEST.md`를 전부 읽고 검토했다. 대상 코드는 수정하지 않았다.

재현: [harness_r5_claims_repros.py](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r5_claims_repros.py).

```text
python outputs/harness_r5_claims_repros.py --target work/harness-r5-target/bms-balancing
exit code 0
```

WSL Python 3.12.3에서 실행했다. 실제 `Blend`, `ne_shape.main()`, `fitted_pair()`, CSV/meta writer, `git_provenance()`를 사용한다. 외부 측정곡선은 합성으로 제공하고 matrix의 fit 값도 fixture로 제공한다. 실제 optimizer나 비공개 측정 자료의 결과를 재현했다고 주장하지 않는다. 모든 파일 상태 변경은 임시 저장소 안이다.

## 1. P1 — 소비한 untracked matrix 입력은 수정 목록에서도 사라진다 (Q4)

위치:

- [ne_shape.py:84](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/ne_shape.py:84): `matrix_<state>*.csv` 역순 중 첫 일치 행을 소비한다.
- [provenance.py:51](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/provenance.py:51): `--untracked-files=no`로 새 입력 파일을 제외한다.
- [ne_shape.py:144](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/ne_shape.py:144): `gamma_from`은 실제 선택 파일이 아니라 항상 같은 wildcard 설명이다.

만드는 상태: 임시 git 저장소에 `out/matrix_100.csv`를 커밋한다. GITT/Li/w=0 행의 대상 γ=.16, 기준 γ=.15를 넣는다. 실제 Blend로 합성한 측정곡선은 대상 γ=.45, pristine γ=.15이고 두 용량은 같다. 진단을 한 번 실행한다. 이어 코드·측정 자료·기준 γ는 바꾸지 않고, 대상 γ=.45인 **untracked** `out/matrix_100_v2.csv`를 추가해 같은 명령을 실행한다.

관측:

| 결과 | 최초 | v2 추가 후 |
|---|---:|---:|
| 실제 소비 파일 | matrix_100.csv | matrix_100_v2.csv |
| 출력 gamma_target | 0.160000 | 0.450000 |
| 출력 gamma_ref | 0.150000 | 0.150000 |
| 출력 ratio_b_over_a | 0.032960 | 1.000000 |
| git_commit | 동일 | 동일 |
| git_dirty | false | false |
| git_modified_code | [] | [] |
| git_modified_outputs | [] | [] |
| gamma_from | 같은 wildcard 설명 | 같은 wildcard 설명 |

이것은 `git_dirty=false`가 틀렸다는 반례가 아니다. 실행 코드는 실제로 같았다. **R4-07의 출력 수정 목록을 입력 기록 대신 쓸 수 없다는 실행 반례**다. 산출 디렉터리의 파일이 입력 역할로 바뀌어도 소비 지점과 meta 사이에 그 관계가 전달되지 않는다. 새 입력은 이름도 기록되지 않으며, 같은 source/ref/commit 설명으로 선택 γ 진폭비가 3.3%와 100%로 달라질 수 있다. 기존에 커밋된 연구 수치 자체가 틀렸다는 증명은 아니다.

양성 대조: 같은 tracked `out/matrix_100.csv`를 수정하면 `git_dirty=false`, `git_modified_outputs=["out/matrix_100.csv"]`로 정확히 구분한다. `code.py`를 수정하면 `git_dirty=true`, `git_modified_code=["code.py"]`다. 따라서 R4-07의 원래 ASCII tracked-output 순차 재생성 결함은 닫혔다고 인정한다.

최소 수정: 코드 dirty/출력 변경 필드는 유지하되 **실제로 읽은 입력 목록**을 따로 남긴다. `fitted_pair`의 반환값에 선택한 파일·행 selector·읽은 bytes의 SHA-256을 묶고, meta가 그대로 사용하게 한다. tracked/untracked 여부는 입력 존재·내용 기록의 조건이 아니어야 한다. 단순히 모든 untracked 파일을 다시 코드 dirty로 세는 것은 앞 라운드의 불필요한 dirty 문제를 되돌린다.

## 2. P2 — Git의 quoted path를 실제 경로로 오인한다

위치: [provenance.py:63](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/provenance.py:63).

임시 저장소에 `out/측정.csv`를 커밋하고 그 값 1만 2로 바꾼다. Git 기본 `core.quotePath=true`일 때 porcelain 출력은 이름을 따옴표와 octal escape로 인코딩한다.

```text
 M "out/\354\270\241\354\240\225.csv"
```

현재 코드는 이 표현 자체를 `top / rel`로 해석한다. 실제 변경은 출력 하나인데 관측값은 다음과 같다.

```json
{"git_dirty": true,
 "git_modified_outputs": [],
 "git_modified_code": ["\"out/\\354\\270\\241\\354\\240\\225.csv\""]}
```

기대값은 `git_dirty=false`, `git_modified_outputs=["out/측정.csv"]`, `git_modified_code=[]`다. 출력 전용 경로의 코드 오염 오진이며 수치가 바뀌는 결함은 아니다. 기본 산출 파일명의 ASCII 범위에서는 R4-07 양성 대조가 통과한다.

최소 수정: 사람이 읽는 quoted porcelain 문자열을 나누지 말고 NUL 구분 `git status --porcelain -z`를 사용한다. rename/copy의 추가 경로 필드도 그 형식에 맞춰 처리한다. 단순한 문자열 `split(" -> ")`는 실제 파일명과 rename 표현을 구별하지 못하므로 함께 제거하는 것이 맞다.

## 3. R4-01·S-02 닫힘 인정, Q5 문구 한정 권고

R4-01의 정확한 가족원 반례를 다시 넣었다: 실제 측정 `Blend(x,.5)`, pristine `.15`, 선택된 fit γ=0. 결과의 `>50mV` 비율은 그대로 68%지만 옛 "γ를 어떻게 고르든 남는다" 출력은 더 이상 없다. **옛 잘못된 보편 판정은 닫힘**이다.

FINDINGS 1317–1327은 현재 다음을 모두 명시한다.

- 100의 선택 Δγ와 증인 Δγ는 같은 방향이며 크기가 약 40배 다르다.
- 200은 두 Δγ 방향이 반대다.
- 300_0009의 증인 없음은 선택 γ_ref 고정·γ 501 × x 400 **표집 기준**이다.
- `(a)`는 용량 정규화와 섞여 있으며, 진폭 증인은 모양 일치가 아니다.

여기에는 새로운 숫자/부호 오류를 찾지 못했다. U9 직접 적합 미구현, S-04 반대쪽 증인 미기록을 새 발견으로 다시 세지 않는다.

다만 [ne_shape.py:326](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/work/harness-r5-target/bms-balancing/scripts/ne_shape.py:326)의 새 출력은 "다른 γ에서도 남는지는 위 (d)의 증인 열이 [말한다]"라고 연결한다. 이는 직전 주석 및 meta의 "진폭 ≠ 모양" 설명과 맞지 않는다. 이 문구는 **별도 새 P1이 아니라 Q5 한정어 정리**로 권고한다.

안전한 수치 확인: 동일한 실제 Blend와 기준 γ=.15로 다음 측정곡선 둘을 만든다.

1. `Blend(x,.5)`.
2. `Blend(x,.15) + 0.06244361590442882 V`.

둘의 측정 변화 진폭은 동일한 62.44361590442882mV이고 `gamma_headroom`의 모든 반환값도 같다(증인 .5). 하지만 γ501/x400에서 최소 max 잔차는 각각 **0mV / 60.64527380396904mV**다. 둘째는 선택 γ=.5에서 `>50mV` 비율 100%여서 위 문장을 실제로 출력한다. 따라서 그 증인 열만으로 다른 γ의 잔차 유무를 결정할 수 없다. 이는 유한 격자상의 수치 예이며 연속 γ 전역 부재나 비공개 측정자료의 반례로 확대하지 않는다.

권장 문장: "다른 γ에서의 모양 잔차와 보상 경로는 별도 시험 대상이다. (d)는 이 변화 진폭 이상을 내는 표집 γ의 존재만 말한다."

관련 설명의 정리 대상: `ne_shape.py` 214–217에는 "안 맞으면 γ로도 못 고치고 a_NE·b_NE로 밀린다"는 옛 설명 주석이 남아 있다. 실행된 수치 판정의 새 발견으로 세지 않되 다음 모델 설계에 옮기면 안 된다. FINDINGS 23–26의 "forward model은 MATLAB 원본과 같다" 첫 요약에도 §1-13의 유한-domain/보존 조합 한정을 붙이는 것이 안전하다.

## 4. 요청문 Q4/Q5의 답

Q4: **수정된 출력 목록만으로는 불충분하다.** 위 실제 입력 선택 반례가 이유다. code/output/input 세 역할을 별도로 기록해야 한다. 입력이 out/ 아래에 있다는 사실은 그 실행의 출력이라는 뜻이 아니다.

Q5: 요청문 §4의 다섯 행은 현재 붙인 한정어를 함께 보존하면 요구서의 **관측 열 초안**으로 쓸 수 있다. 본 담당 범위에서는 음수 LAM_NE의 고정-기준 산술을 경계 재적합 인과로, 폭의 탐색 하한을 정확도/식별성으로, 잔차 증가 및 γ 진폭비를 원인 판정으로 다시 바꾸는 근거를 찾지 못했다. 포팅 수치 대조의 세부 정밀도 판정은 별도 담당 검토가 필요하다. 위 출처 결함이 기존 모든 관측값을 무효화한다는 뜻은 아니지만, 같은 근거를 재생성·인용할 때 입력이 무엇이었는지 고정하는 장치는 필요하다.

여기서 GO는 새 모델 설계 요구서 작성 근거로 쓸 만한가의 판단이다. 본 실행 승인·외부 배포 승인·실제 측정자료의 전역적 표현성 증명으로 확대하지 않는다.
