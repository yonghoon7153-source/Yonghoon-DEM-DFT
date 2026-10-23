# Codex 발송 전 공격 리뷰: RCA2-01·04·06·08·09 수정과 Q9 설계

> 이 파일 = 독립 에이전트 (10-23 05:41–06:41 UTC · 고친 사람 설명 안 읽음) 의 마지막 보고를 메인 세션이 옮겨 적은 것 (하네스가 하위 에이전트의 보고 `.md` 파일 쓰기를 막는다).  내용은 그대로 · §E 의 작업 폴더 경로만 이 폴더의 리포 경로로 바꿨다.  메인 재확인 (C1 · C5 · A3 · D2) = 이 폴더 `README.md`.

- **대상:** 코드 diff `49a1af626..bd0e85ce6`과 Q9 설계 문서
- **트리:** 시작 SHA `2a093e5d`로 맞춘 뒤 작업 사본에서 돌렸다. 리포는 고치지 않았고 커밋하지 않았다. 출력은 전부 scratchpad에만 남겼다.

**결론**
- **코드:** P1은 없다. P2 1건(C1)은 기록을 편집해야만 닿고, 생산자 경로에서는 생기지 않는다. 나머지는 P3 4건이다.
- **Q9 설계:** P2 4건, P3 2건, 질문 1건이다.
- **Codex 탐침:** 판정문 탐침을 무변경으로 돌렸다. 지목된 반례는 전부 뒤집혔고, 정상 경우는 그대로다.

## A. 코드 발견

### C1 [P2] 같은 런의 주 해 증서를 끝 증서로 바꿔 끼우면 계약을 통과하고 거짓 clear가 난다
- **도달 범위:** 보장 문장이 깨진다. 다만 기록을 편집해야만 닿는다. Codex RCA2-04와 같은 부류다.
- **자리:**
  - `scripts/ca_ext_svcf.py:440–460` `_pos_cert_problem`: 증서와 끝을 잇는 결합이 `I_bot == G` 하나뿐이다.
  - `scripts/ca_ext_svcf.py:516–525` `_cert_problem`의 끝 반복: 런 단위 `BIND_FIELDS`만 대조한다.
  - 끝 증서를 끊은 그래프에 묶는 칸이 없다.
- **재생:** `test_carbon_junction._qd3_svx(cert=True)`(SVX, nu 0)의 실제 생산 경로 기록을 다음처럼 고친다.
  - `G_cut_code` ← `G_full_code`
  - 두 끝의 비 ← 1.0
  - `conv_cert` ← `conv_cert_full` 사본
  - `ratio_cert_interval` ← `cert_interval`로 다시 셈
  - 스크립트: `atk_sv.py`의 'A2'
- **기대:** 거부. 그 끝 증서는 끊은 그래프가 아니라 주 그래프를 인증한다.
- **실제:**
  - `sv_cf_problem`이 None을 돌려준다.
  - 구간은 [0.9999999999998652, 1.0000000000001348], 문턱 2에서 표지는 `[]`이다.
  - 원 기록은 [10.291253935343772, 10.291253935346543], SV_DEPENDENT다.
  - read_run의 `conv_cert_full` ↔ step3 주 증서 대조도 통과한다.
- **깨지는 문장:**
  - 등록 R §5-6 SV 행의 "(다른 회로 · 다른 런의 증서 = 거부)"
  - `_pos_cert_problem` 주석의 "다른 회로의 증서 = 거부"
  - Codex의 원 반례(G는 그대로 두고 외부 증서만 붙임)는 막혀 있다.
- **보강 후보 (추정):** 증서의 `target_n_edges`를 투영해 "끊은 수 > 0이면 끝 n_edges ≤ 주 − 끊은 수"를 대조한다.
  - SVX: 주 44, 아래 끝 42 = 44 − n_sv_faces_cut 2
  - QD2-3 위 끝: 16 ≤ 23 − n_edges_cut 6 (등식은 아니고 부등식만 성립)
  - 이 대조라면 A2는 44 > 42로 걸린다. 다른 꼴에서도 확인해야 한다.

### C2 [P3, 시험] 위비를 바깥쪽으로 반올림하는지 상주 시험이 묶지 않는다
- **자리:** `scripts/ca_ext_svcf.py:592–609` `_div_dir`. 코드 자체는 맞다. 퍼즈 20,081쌍에서 위반 0건이었다.
- **변이 M7 (방향을 맞바꿈):** 아래 시험이 전부 통과한다.
  - `test_carbon_junction` QD2–QD4 42/42
  - `test_rint_r_chain` U15–U17, V28–V31 8/8
  - `test_ca_ext_b6` S 243/243
- **변이 M1 (그냥 a/b):** U16(넘침 경우) 하나만 잡는다.
- **효과 (실제 기록, `atk_m7.py`):** t = "정확한 위 몫 이하의 최대 float"로 두었을 때
  - SVX, t 10.29125393534654: 바른 판은 위비 10.291253935346543 → UNCHECKED, M7은 `[]`(거짓 clear)
  - QD2-3, t 2.289808917197574: 바른 판은 위비 2.2898089171975746 → UNCHECKED, M7은 `[]`
- **원인:** QD3 ②의 경계는 위·아래비 × (1 ± 1e-9)라서 1 ULP 칼날보다 훨씬 넓다.
- **권고:** 같은 칼날을 상주 회귀로 둔다.

### C3 [P3, 방어 범위] R 단조 검사는 최종 추정량만 본다
- **자리:** `scripts/rint_r_chain.py:464–469` `final_band`, `:1843–1862` `_r_monotone`
- **재생:** `atk_rmono.py`, `atk_rmono2.py`. 가짜 fetch를 쓰고 e = 0으로 두었다.
  - **R1:** 넘침 없는 모서리에서 arm 1 = 4.80 / 4.85 / 4.40 (R .5 / 1 / 2) → PREDICTED
  - **R1c:** 넘침 모서리(adjusted 12)에서 그 모서리의 arm 0 = 4.6 / 4.7 / 4.4 → PREDICTED
  - **R1d:** 넘침 모서리에서 origin 3 = 4.4 / 4.7 / 4.4 → PREDICTED
- **비교:**
  - Codex §8 권고: "동일 origin **및** 동일 최종 추정량"
  - 원장 RCA2-09와 주석: "같은 origin"을 arm 0 / mean8로 정의 → 문장 자체는 자기일관이다.
  - 추가 풀이 없이 할 수 있다. 이미 가진 값은 다음과 같다.
    - 모든 모서리에서 arm 1·2 × 세 R
    - adjusted 모서리에서 8 origin × 세 R

### C4 [P3, 칼날 · 멈추는 쪽] 단조 띠가 정확한 증서 구간이 아니다
- **자리:** `scripts/rint_r_chain.py:434–440` `arm_band`
  - 주석은 "정확 분수 끝"이라고 쓴다.
  - 실제로는 e = float `err_rel`, σ = 게시된 float다.
- **재생:** `atk_rmono.py` R2. 두 증서는 `target_judge`로 만들었고 R_a < R_b다.
  - a: G 1.4656500700997732, [1.4656491487242123, 1.4656880073121192], err_rel 2.588422238019952e-05
  - b: G 1.4657027350682457, [1.4656880073121192, 1.4657035569138221], err_rel 1.0048255880306897e-05
- **결과:**
  - 정확한 구간은 한 점에서 만난다. 즉 단조와 양립한다.
  - 띠는 떨어진다. 분수로 비교하면 band_hi_a < cert_hi_a, band_lo_b > cert_lo_b다.
  - 그래서 ('R_j_lo','R_j0') → R_MONOTONE_VIOLATION으로 멈춘다.
- **영향:** 거짓 멈춤뿐이다. 실무에서 일어날 확률은 매우 작다(추정).
- **닫는 방법:** 띠를 증서의 `target_lo/hi`로 직접 만들거나 주석 문장을 줄인다.

### C5 [P3, 기록 계약] SV 끊기 정의(kind · rule)가 묶이지 않는다
- **자리:**
  - `scripts/ca_ext_svcf.py:224`: kind는 접두어만 본다.
  - `scripts/ca_ext_svcf.py:90`: `_COPY`에 'rule'이 없어 투영에서 빠진다.
- **재생 (`atk_sv.py` A4):**
  - kind = 'counterfactual_cut_sv_faces_all' → 계약 None
  - rule = 'some_other_rule' → 계약 None
- **상주 고정물:** 철회된 옛 정의 이름을 쓴다. 옛 이름 `counterfactual_cut_sv_faces`는 "SV 면 전부"를 끊는 다른 양이다(`carbon_junction.py:92` 주석).
  - `scripts/test_ca_ext_b6.py:729`
  - `scripts/test_rint_r_chain.py:256`
  - `scripts/test_rint_r_chain.py:2388`
- **Codex 최소 해결과의 관계:** "등록 rule/version 결합" 중 rule이 남아 있다. 수정 문장은 괄호 규칙만 주장하므로 문장 위반은 아니다.

### 정보 (결함 아님)
- **I1 qualifiers 문장 변경:** `CJUNC_QUALIFIERS[8]` 문장이 바뀌었다(`carbon_junction.py:147–152`).
  - 고치기 전에 쓴 cjunc 매니페스트는 `cjunc_block_problem`에서 'qualifiers|'로 거부된다.
  - 끈 경로 대조 결과, σ와 증서 dict는 비트가 같다.
  - 바뀐 것은 이 문장과 SV 기록의 새 칸뿐이다.
  - 리포에 남은 기존 기록 중 영향받는 것은 미확인이다.
- **I2 넘침 퍼즈:** 극단 망 3,000개(`atk_overflow.py`)
  - 고치기 전: OverflowError 2건
  - 고친 뒤: 0건
  - POSITIVE 291 → 223. 옮겨 간 68건은 '원장 대조 넘침' 부류다. 옛 판에서 허용폭이 inf라 대조가 비어 통과하던 꼴이니 의도된 변화다.
- **I3 T24 시험의 범위:** Codex의 5노드 8e307 경우 하나만으로는 `_fsum_bound` 가드가 묶이지 않는다.
  - 가드를 빼도(M9) 새 `_ledger` 넘침 검사가 먼저 잡는다.
  - T24a의 다른 두 경우가 M9를 잡는다(하위 4 FAIL). 시험은 충분하다.

## B. 깨지지 않은 보장과 시도 방법

1. **SV 판정 = 증서 구간 (RCA2-01)**
   - 실제 생산 경로 5회로(QD2-1, QD2-2, QD2-3, QD4, 두 성분 + 다섯째 rail)를 분수로 대조했다. 아래비 ≤ 정확 몫, 위비 ≥ 정확 몫이 섰다.
   - +∞는 영값 위상 증서가 있는 끝에서만 나왔다.
   - SVX 칼날은 다섯 경우 모두 기대대로였다.
     - t = 아래비 → UNCHECKED
     - t = nextafter(아래비, −∞) → DEPENDENT
     - t = 위비 → `[]`
     - t = nextafter(위비, +∞) → `[]`
     - 사이 → UNCHECKED
2. **`_div_dir`:** 퍼즈 20,081쌍(부정규·최대값 특수쌍 81 포함), 위반 0건.
3. **기록 계약 (RCA2-04)**
   - 형·부호화 공격 16종을 전부 자기 사유 문장으로 거부했다. 예: 지위 끝 공백, 동형 문자, bool/0.0 수, 문자열 I_bot·target_lo, 뒤집힌 구간, pass_d 1, ok "true", tol 1e-3, bind_version, fp_face_plan, 구간 칸 문자열·정수, G −0.0.
   - Codex 변이 중 고치기 전에 통과하던 6건이 0건이 되었다.
4. **두 성분 괄호 (RCA2-06 F4):** 소스 변이 M6(위 끝이 첫 성분만 지움)에서 QD4 ①②③이 FAIL했다(39/42). 옳은 이유로 실패한다.
5. **census 불일치 끝-끝 (F6):** b6 SM0–SM3이 통과한다.
6. **RCA2-08:** I2, I3과 Codex `finite_subtotals_overflow` 결과가 근거다.
7. **R 단조 가드 (RCA2-09):** 변이 M8(가드 no-op)에서 U17, V31이 FAIL했다.
8. **끝 대입 변이:** M2–M5를 QD3 ①②⑤ 또는 U16이 잡는다.
9. **끈 경로:** 7꼴에서 σ와 증서 dict의 비트가 같다.

## C. Q9 설계

### D1 [P2] 등록 결과 NOT_COMPUTED가 UNIT_EXTRA로 바뀐다
- §3-2(문서 47행)와 §8(103행) 양성 시험이 충돌한다.
- **모사:** 첫 모서리를 NOT_COMPUTED로 두고 합치기를 다시 돌렸다.
  - 사슬은 쓴 런 3, 안 쓴 런 23개를 남긴다.
  - §3-2 규칙대로면 STOPPED가 된다.
  - 한 기계로 돌린 사슬은 NOT_COMPUTED, 런 3이다.
- 안 쓴 런을 `runs`에 넣으면 판정 단계의 `Replay.done`(`rint_r_chain.py:1547–1549`)이 REPLAY_MISMATCH를 낸다.
- **필요한 것:** 등록 결과에서 남은 런을 어떻게 다룰지 규칙을 정해야 한다(출처 칸에만 기록하고 판정하지 않는 식).

### D2 [P2] SBE no-op 비트 대조가 기계를 넘는다
- **자리:**
  - `rint_r_chain.py:1796`: `sigma == r0_sigma`
  - r0_sigma는 사다리 기계의 팔에서 읽는다(`:2071–2073`).
  - 등록 R §4-1(114행)과 §10-2 ⑩(411행)이 "float 같음"을 요구한다.
- 설계 §5(77행)는 기계를 넘는 비교로 W0 · same_p · 판정만 든다.
- **실측 (CPU):** 같은 코드, 스레드 1에서 `OPENBLAS_CORETYPE`만 바꿨다.
  - seed0: 0.025659646167941766 / …172737614 / …164671895
  - seed1: 0.029640438423438248 / …40621689 / …412320665
  - 상대 차이 1.3e-10–5.8e-10
- **모사:** no-op σ를 2e-10 다르게 두면 SAME_P_CONSISTENCY로 멈춘다.
- **범위:**
  - 지금 사슬을 2대로 돌리는 경우에도 해당한다. 사다리는 나누고 예측은 한 기계일 때, §6 표 "198–292 h" 행이다.
  - 생산 backend는 GPU라서 GPU 사이 동일성은 미확인이다(추정: 다를 수 있다).
- **선택지:** no-op을 그 법칙의 사다리 기계에서 돌리거나, 허용폭을 두는 등록 개정을 한다. 1저자 결정 사항이다.

### D3 [P2] 시도 채택 규칙을 합치기가 확인할 수 없다
- §3-4가 "정확히 한 번씩, 겹침 = 멈춤"(61행)과 "시도가 여럿이면 처음 완주한 시도를 채택"(65행)을 함께 요구한다. 둘은 양립하지 않는다.
- 단위당 폴더 하나만 넣을 수 있으니 어느 시도를 쓸지는 합치기 전에 사람이 고른다.
- 시도 번호는 폴더 스스로 신고한다(§3-3).
- **동기가 있다:**
  - 넘침 한 모서리 = 팔 24개, 약 87 h 추가(등록 §10-4)
  - D1의 NOT_COMPUTED
  - 결과 뒤 멈춘 단위를 다시 돌리는 것은 Q4가 금지하는데 합치기에 보이지 않는다.
- 기계마다 비트가 다르다(D2). 그래서 칼날 판정(origin 0.1·W0, SV 걸침, 단조 띠)이 배정에 따라 뒤집힐 수 있다. 실제 빈도는 작다(추정).
- **필요한 것:**
  - 결과 전에 커밋하는 추가 전용 시도 원장, 또는 단위↔기계 배정 봉인
  - 합치기가 시도 폴더 전부를 받아 규칙을 직접 적용

### D4 [P2, 문서대로 구현할 경우] 팔 파일만 복사하면 러너 기각 표지가 사라진다
- 설계 44행은 "팔 파일 = 바이트 그대로 복사"라고 쓴다.
- read_run 동작:
  - `.rejected_*` 표지가 있으면 멈춘다(`:1304–1306`).
  - 영수증이 없으면 멈춘다(`:1219–1221`).
- 팔과 영수증만 옮기면 기각된 런이 합친 폴더에서 통과한다. §4 "같은 팔 기록 → 같은 판정"이 깨진다.
- **필요한 것:** 원 단위 폴더에 같은 read_run을 돌리고 런 폴더를 통째로 복사하거나, 표지가 있으면 합치기를 거부한다.

### D5 [P3] 두 번 합치기를 자리 표시 값으로 계산하면 안 된다
- 첫 합치기에서 `Predict.run`은 첫 넘침 모서리의 origin8에서 끊긴다.
- 넘침 목록 전체를 내려면 origin 판정 직후 멈추는 따로 된 경로가 필요하다.
- 자리 표시 값으로 계속 돌리면 `_r_monotone`, mean8이 가짜 값으로 돈다.
- 둘째 합치기에서 다시 계산하면 결정 기록은 저절로 검증된다(요구보다 많으면 UNIT_EXTRA, 적으면 다시 EXPANSION_NEEDED). 설계 추론이고 구현은 없다. 이 점과 결정 기록 ↔ 단위 sha 집합 결합을 명시해야 한다.

### D6 [P3, fail-closed] 키에 절대 경로가 들어 있다
- `code_key`의 runner_path(`:1086`): 이미 알려진 항목이다(등록 513행 "Q3-b 때 다시").
- 새 사례: `check_after_main`이 `resolve()`한 dir(`:1928`, `:1938`)을 dict 전체로 비교한다.
  - `:2058` "두 변이 사다리의 주 예측 묶음이 다르다"
  - `:2120`
- 경로가 다른 기계에 감도 단위를 나누면 MAIN_NOT_DONE으로 멈춘다. 판정 단계는 sha만 본다(`:2499`).

### D7 [질문] 시간 표
- ×6.05(하한)는 필수인 ⓒ 이어 풀기(1e-14)를 빼고 센 비율이다(등록 503행: ×7.37 = cold 1e-14).
- 증서마다 다시 푼다. SV 끝 증서도 마찬가지다.
- 따라서 하한 110.1 h(2대)는 낙관적일 것이다(추정).
- 감도 단계는 표에 없고 주 판정 합치기 뒤에야 시작할 수 있다.

### Q-A – Q-F 답
| 질문 | 답 |
|---|---|
| **Q-A** 같음 논리에 빈틈이 있나 | D1, D4, D5, D2, D6 |
| **Q-B** 결정 기록 인용이면 충분한가 | 넘침 런을 더하거나 빼는 것은 다시 계산으로 막힌다. 넘침 런의 시도 선택은 막지 못한다(D3). |
| **Q-C** 12단위 vs 6단위, same_p가 기계를 넘어도 되나 | same_p는 기계를 넘어도 된다(τ_mono 1e-3 vs 실측 ≤ 5.8e-10, CPU 기준. GPU는 추정). 6단위로 해도 D2는 안 풀린다. no-op을 사다리 기계에 고정해야 풀린다. |
| **Q-D** 배정을 봉인하지 않아도 충분한가 | 충분하지 않다(D3). |
| **Q-E** cupy · CUDA · GPU는 기록만 하면 되나 | 비트 대조(D2)에는 부족하다. |
| **Q-F** 감도 단계도 같은 방식으로 나눠도 되나 | 감도 단위는 최종 주 합치기 뒤에만 시작할 수 있다(`check_after_main :1932`). D6이 걸린다. 멈춘 변이는 `<V>_UNCHECKED`(`:242`)로 처리되어 일관적이다. 재시도는 D3에 걸린다. |

## D. Codex 탐침 무변경 재실행
옛 트리와 새 트리 모두 사본(`ev_old`, `ev_new`)에서 돌렸고 출력은 `logs/`에 있다.

- **certificate:** 둘 다 rc 0.
  - 옛 트리: stderr에 `step3_conv_cert.py:344` overflow 경고
  - 차이는 `finite_subtotals_overflow` 하나: OverflowError → NOT_CERTIFIABLE('원장 대조 넘침')
- **geometry/run_review:** 둘 다 rc 0, regression 122/122, S1 44/44.
  - `actual_certified_threshold_crossing`: `[]` → SV_DEPENDENT
  - 증서를 뺀 기록 · 첫 성분만 변이 · 외부 증서: `[]` → UNCHECKED(거부)
  - mutation 4건이 새로 거부됨
  - **주의:** Codex 합성 기록에는 `census` / `solve.I_bot_code`가 없다. 그래서 몇 건은 그 결손으로 먼저 거부되어, 그 탐침 경우로는 겨냥한 검사를 따로 보지 못한다. 완전한 기록으로 하는 확인은 상주 QD3/QD4/SM/S8이 맡는다.
- **registration:** 새 트리 rc 1.
  - `dbe_nonmonotone`에서 Predict가 Stop을 던지는데 탐침은 반환값을 기대한다.
  - 함수별로 돌리면 바뀐 것은 이것 하나다(PASS_INFORMATIVE → R_MONOTONE_VIOLATION). 나머지 9개 함수는 같다.
- **provenance:** 옛 트리와 새 트리의 출력이 바이트까지 같다. RCA2-02/03/05는 이 diff 범위 밖이고 원장에서 open이다.

## E. 재현 파일 (리포 사본 = 이 폴더)
- **트리 (작업 폴더 `ATK_ROOT` · 리포에 넣지 않음):** `new_src/` = 시작 SHA `2a093e5da` 사본 · `old_src/` = `49a1af626` 사본 · `mut/` 아래 M1–M9 변이 트리.
- **도구:** `docs/reviews/rint2_rr_fix_evidence_20261023/preattack/tools/` 아래
  - C1, A1–A4: `atk_sv.py`
  - C1 보강 자료: `atk_edges.py`
  - C2: `atk_m7.py`, `atk_divdir.py`
  - C3, C4: `atk_rmono.py`, `atk_rmono2.py`
  - I2: `atk_overflow.py`
  - D2: `atk_bits.py` (끈 경로 비트 대조 = `atk_bitid.py`)
  - D1, D2 모사: `atk_q9.py`
  - 변이: `mkmut.py`, `mkmut6.py`, `mkmut9.py`, `runmut.py`, `run.py` (작업 폴더 경로 한 줄 = `ATK_ROOT`)
  - 판정문 탐침 실행: `run_probes.sh` · 등록 탐침 함수별 실행: `reg_each.py` · JSON 차이: `jdiff.py` · 셸 감싸개: `py.sh`
- **실행:** `RINT_REVIEW_SOURCE=<트리> OPENBLAS_NUM_THREADS=1 python3 -I -B <도구>`
- **로그:** `docs/reviews/rint2_rr_fix_evidence_20261023/preattack/logs/`
  - 변이 결과 `runmut1.json`, `runmut2.json`, `mut_M9_t24.log`
  - 판정문 탐침 출력 `{old,new}_*.out` · `*.err` · `{old,new}_summary.txt` · `{old,new}_reg_each.json` · `{old,new}_prov.out` · `new_s0.out`
  - 끈 경로 `bitid_{old,new}.json` · SV 공격 `atk_sv.out` (리뷰어) · `main_recheck_atk_sv.json` (메인 재확인)
- **돌리지 않은 것:** b6 'B' 묶음(`--old-scripts`), 전체 시험 묶음, GPU 경로. 실측은 전부 CPU 경로다.
