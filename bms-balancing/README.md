# bms-balancing — α·β 검증 하네스

규진팀 MATLAB electrode balancing (Si/Gr 블렌드, 5-파라미터
`[a_PE, b_PE, a_NE, b_NE, γ_Si]`) 이 내는 답이 **데이터로 정해지는 값인지**를
재기 위한 도구. 2026-09-10 에 받은 코드·데이터·결과를 대상으로 만들었다.

## 이 디렉터리가 하는 일과 안 하는 일

- **한다**: 그들 forward model 을 **고치지 않고** Python 으로 옮기고
  (`model.py`), 그 위에서 경계·축퇴·모델 선택 감도·비결정성을 잰다
  (`verify.py`).
- **안 한다**: 모델을 개선하지 않는다. 고쳐서 옮기면 "그들의 답"이 아니라
  "우리 답"을 재게 된다. 고칠 자리는 재고 나서 따로 제안한다.

## 경계 (중요)

- **RUN_SCOPE 밖이다.** `degradation-degeneracy` 의 `source_digest` 는
  `src/ tools/ configs/ scripts/ run.sh requirements*.txt` 만 본다. 이
  디렉터리는 그 밖이므로 게이트 리뷰 대상 코드 identity 를 안 건드린다.
- **원자료는 저장소에 넣지 않는다.** 반쪽전지·풀셀 xlsx, 문헌 OCP 는 규진팀
  것이다. 경로를 밖에서 받는다:

  ```bash
  export BMS_DATA_ROOT=/…/electrode_balancing_blend
  python3 -m bms_balancing.verify port --state pristine --si-source Li
  ```

## 준비

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

`openpyxl` 은 코드가 직접 import 하지 않지만 **반드시 필요하다** — pandas 가
`.xlsx` 를 읽는 엔진이고 없으면 적재에서 죽는다. 2026-09-10 에 사용자 WSL 에서
`ModuleNotFoundError: numpy` 로 대조가 멈춘 뒤에 `requirements.txt` 를 만들었다.
그전에는 무엇을 깔아야 하는지가 사람 기억에만 있었다.

## MATLAB 쪽

`matlab/` 에 사용자 기계에서 돌릴 것이 있다. 2026-09-10 에 그 기계에
**Optimization · Global Optimization · Signal Processing** 툴박스가 설치되어
(Statistics 는 원래 있었다) 규진팀 `main_blend_final.m` 이 그대로 돈다.
그전까지 쓰던 우회로(`dd_shims/` · 적합 없는 `dd_eval`)는 그대로 남겨 둔다 —
툴박스 없는 기계에서도 돌아야 하고, **둘을 번갈아 돌려 MathWorks 구현과 우리
정의의 차이를 재는 데** 쓰이기 때문이다 (`FINDINGS.md` §1-7).
절차는 `matlab/README.md`.

`matlab/tests/` 는 그 MATLAB 파일들을 GNU Octave 8.4 로 **실제 실행해 본**
검사다 (`matlab/tests/run_all.sh`). 무엇이 닫혔고 무엇이 아직 열려 있는지는
`matlab/tests/README.md` 에 표로 적혀 있다.

## 명령

| 명령 | 무엇을 묻나 |
|---|---|
| `port` | **포팅이 그들 모델인가** — 보고된 파라미터가 우리 목적함수의 최적점 근처인가 |
| `eval` | 같은 질문의 **툴박스 없는 길** — 적합 없이 주어진 p 에서 rmse 만. `--compare` 로 `matlab/dd_eval.m` 산출과 대조하고 갈린 단계를 짚는다. **종료 코드가 판정이다** (0 complete · 1 갈림 · 2 미완 · 3 부분/옛 스키마 — `--allow-partial` 로만 0). CSV 의 출력 정밀도는 **옵션 → 선언 → 추정** 순이다 (`--precision g17|full|fixed:N|sig:N` → 파일의 `# printed_format` → 값의 자리수). 추정은 탐색이라 결과가 맞아도 complete 가 아니라 partial(종료 3)이고 `--allow-partial` 로도 0 이 되지 않는다; 옵션이 선언보다 느슨해도 마찬가지다. 반올림 구간은 토큰의 반 단위이고 그 초과분만 수치 차이다. 같은 이름의 열·앵커, 두 번째 형식 선언, 숫자 아닌 앵커, 이름/순서가 다른 파라미터 열은 invalid (R3-06·07 · R4-02~04 · R5-01~03). `%g` 구간은 같은 형식으로 실제로 찍어서 정한다. 예외 하나: 해석 못 하는 선언은 `--precision` 을 명시하면 옵션이 대체한다 (R5 Q1). 세 산출 명령(degeneracy·matrix·profile)은 명령당 하나의 시도 식별자 `run_id`(`--run-id` 또는 `BMS_RUN_ID`)를 모든 행/JSON 에 박고, 게시는 `<산출>.lock` 안에서 한다; `run_states.sh` 는 그 id 를 산출물의 **필드**로 확인하고 meta 를 같은 잠금 안에서 재확인·bytes 해시와 함께 쓴다 — 산출과 meta 는 한 시도의 한 묶음이다 (R4-06 · R5-04 · R5-08) |
| `degeneracy` | 최적 목적함수의 (1+ε) 안에 드는 답들이 만드는 LAM/LLI 폭 |
| `matrix` | 문헌 Si 소스 8 × 반쪽전지 소스 2 × dQ/dV 포함 2 — **모델 선택**이 답을 얼마나 움직이나 |
| `profile` | γ_Si 를 고정하고 나머지 넷을 재적합 — γ ↔ α_NE 축퇴 |
| `scale-noise` | 목적함수 scale 의 난수 seed 가 답을 얼마나 흔드나 |

### 사이클별 재적합과 난간 — `scripts/fit_cycles.py` · `scripts/check_rails.py`

규진팀 결과표(`result_L_*.xlsx`, 11 열)를 **우리가 다시 뽑고 같은 자로 잰다** (`reviews/BML_R1_RESPONSE.md` §10).

| 도구 | 무엇 |
|---|---|
| `scripts/fit_cycles.py` | `main_blend_final.m` 의 사이클 루프를 하네스로 — 같은 모델·경계·수출 공식, 원자료는 `<cycle>_capacity/<cycle>_voltage` 워크북 + pristine 반쪽전지. 산출 `cycles_<cell>_<si>.csv` (+ sidecar) 는 `check_u14` 의 등록된 종류다. **`--objective-version` 필수** (⑥ chain rule 계약, Codex R17 §4: `legacy_matlab` = 원본 그대로·`dv_cell` 에 1/a 없음 · `chain_rule_v2` = 맞는 미분; 기본값 없음, 행·sidecar·controls·`width_report` 에 실린다). `--seed` 를 바꿔 두 번 돌리는 것이 결정 실험의 절반 |
| `scripts/check_rails.py` | 결과표 난간 4 층 (계약 → `error` · 패턴 → `warning` · 기록된 optimizer 설정 → 접촉 거리 · 잔차 존재). MATLAB xlsx 든 우리 CSV 든 **같은 검사**. rc 0/2/3 |
| `matlab/fit_cycles_driver.m` | 규진팀 파이프라인을 수정 없이 사이클별로 부르는 MATLAB 드라이버 — `rng(` 고정이 남아 있으면 거부, 결과 + `.settings.json` |

### 여러 상태를 한 번에 — `scripts/run_states.sh`

`300_0009` 에서 한 것을 다른 상태에도 **같은 설정으로** 돌린다.

```bash
export BMS_DATA_ROOT='/…/degradation mode'
nohup ./scripts/run_states.sh > out/run_states.log 2>&1 &
tail -f out/run_states.log
```

상태당 `degeneracy` · `matrix` · `profile` 셋, 기본 세 상태(100 · 200 ·
300_0147)면 아홉 번이다. **몇 시간** 걸린다. 조절은 환경변수로:

```bash
STATES=100 ./scripts/run_states.sh                    # 하나만
OUT=/tmp/smoke STARTS=6 ./scripts/run_states.sh       # 배관 확인용
SI=Kunz SRC=step_005C ./scripts/run_states.sh         # 소스 고정
```

**반쪽전지 소스는 상태마다 자동으로 고른다** — `GITT` 에 그 상태 파일이 없으면
`step_005C` 로 넘어간다. `300_0147` 이 실제로 GITT 에만 없다
(`dd_verify('check')` 의 "상태 파일 4/5" 가 이것이다). `SRC` 를 주면 그 소스로
고정하고, 없는 상태는 건너뛴다. 마지막에 상태별로 무엇을 썼는지 찍는다 —
**소스가 섞였으면 그 상태끼리 직접 비교하면 안 된다.**

**시험 실행은 `OUT` 을 반드시 바꿔라.** 2026-09-10 에 합성 데이터로 `STARTS=4`
시험을 돌렸더니 `out/matrix_300_0147.csv` 가 생겼고, **파일 이름만으로는 진짜
산출과 구별이 안 됐다.** 정본이 artifact 인 저장소에서 그건 치명적이다.
그래서 산출마다 `.meta.json` 을 옆에 쓴다 (상태 · 소스 · `starts` · `data_root`
· git 커밋 · dirty 여부 · 시각 · `run_id` · `sha256` · 계산 **전/후** git 상태(`git_commit_at_start`,
`git_state_changed_during_run`) · `env`(python·numpy·scipy·pandas·platform) — R5-04 · R6 내부 F03·F04).
산출 자체에도 소비한 입력 파일들의 digest 가 붙는다 (`inputs_sha` 열 · degeneracy JSON `consumed_inputs` ·
eval 헤더 `# inputs,…`·`# env,…`, R6 내부 F4·F3). 게시 뒤 묶음 검사는 `python3 scripts/provenance.py
--verify-unit <산출> <run id>` (meta 의 run_id·sha256·artifact 이름이 이 시도의 bytes 와 맞는가; reader 인
`compare_states.py`·`ne_shape.py` 도 섞인 묶음을 소비하지 않는다). degeneracy 는 `--out` 으로 잠금 안에서
원자적으로 게시된다 — stdout 은 로그다 (R6 내부 F01). 무엇으로 만든 값인지가 파일에 붙어 있어야 한다.

**왜 스크립트인가**: 아홉 번이 같은 설정이어야 비교가 성립한다. 손으로 아홉 줄을
치면 한 줄에서 `--starts` 를 흘리는 순간 그 행만 다른 조건이 되고, 나중에 그것을
알아챌 방법이 없다. 스크립트에 적힌 플래그가 산출의 provenance 다.

**끝났다는 말을 믿기 전에**: 이 스크립트는 각 산출을 **실제로 열어서** 확인한다
(JSON 이 파싱되나, CSV 에 행이 있나). 종료 코드만 보면 안 되기 때문이다 —
만드는 과정에서 진행 표시가 stdout 으로 새어 JSON 을 오염시켰는데 python 이
정상 종료해서 "전부 통과" 가 찍혔다 (`INTRO.md` §4-⑧).

## 측정된 것 (2026-09-10 적대적 리뷰 반영판, 요지)

정본은 `FINDINGS.md` 와 `out/` 의 실행 산출이다. 여기 적은 것은 사본이고,
조건(허용 임계·축·**분모**)을 떼고 인용하면 안 된다.

> **2026-09-10 외부 리뷰 판정: NO-GO.** 전 판의 결론 넷 중 셋이 무너졌고
> 반례는 전부 재현됐다. 무엇이 철회됐는지는 `FINDINGS.md` §0-2 에 있다.
> 아래는 정정된 판이다.

1. **포팅의 forward model 은 닫혔다** — MATLAB 원본과 **같은 p** 를 넣고
   목적함수 항만 대조했다 (적합 없이, 그래서 optimizer 차이가 안 낀다).
   4 조합(상태 × Si 소스 × 반쪽전지) × (앵커 10 + rmse 16) = **104 개 값이
   적힌 자리수 안에서 일치**. `c_cell`·`E_PE(0.5)`·`E_NE(0.5,0.25)` 는
   마지막 자리까지 동일. 단 `w_dqdv=0` 조건이다. dQ/dV 항은 2026-09-10 에
   `findpeaks` 대체품으로 대조 경로를 열고 **같은 날 사용자 기계에서
   실측했다** (§1-7 · §1-8): MATLAB 안 툴박스↔shim 이 `rmse_dqdv` **1.78e-12**,
   MATLAB↔Python 192 값이 최대 **4.04e-12**. 다만 그들 로컬 함수 둘은 파일
   밖에서 못 불러 옮겨 적은 것이라, **dQ/dV 항만은** 「우리 전사 ↔ 우리 포팅」
   대조다.

   그리고 **최적화 절차까지 댔다** (2026-09-10, §1-9): Si 8종 전수 재적합에서
   양쪽 다 경계에 안 붙은 세 조합의 최대 차이가 **0.17 %p**, γ 21 격자에서
   18 점이 0.03 %p 안이다. 절차 차이는 답을 바꾸는 크기가 아니다. 다만
   **방향은 있다** — 갈린 두 점에서 더 좋은 해를 찾은 것은 그들 쪽이다.
   그리고 **blind 재적합**(보고값을 시작점에서 뺌)이 비-blind 와 마지막
   자리까지 같은 답을 냈다 — 시작점이 답을 끌지 않았다.
2. ~~모델을 고정하면 답은 좁다~~ — **철회.** "1 % 안 LAM_NE 폭 0.87 %p" 는
   폭이 아니라 무작위 표집의 하한이었다. **우리 γ 프로파일 자신**이 같은
   설정에서 1 % 안 두 점만으로 1.5924 %p 를 보인다. 방법을 제약 최적화로
   고쳐 다시 뽑았다 — LAM_NE 3.6027 %p · LAM_PE 2.8696 · LLI 1.0832 (§3-3).
3. **모델 선택이 답을 움직인다** — 문헌 Si 소스만 8 가지로 바꾸면
   (GITT · dQ/dV 제외 · **8종 전체**) LAM_NE 폭 10.88 %p, LLI 폭 **1.02 %p**.
   (전 판이 "LLI 강건 0.53 %p" 라고 쓴 값은 반쪽전지 2종을 섞고 Si 를 4종으로
   줄인 interior 6/16 행의 값이었다 — 사후선택이다.)
4. **γ_Si ↔ a_NE 보상은 질적으로 관측된다** — γ 0.05→0.325 에서 a_NE 가
   1.209→1.021 로 정확히 반대로 움직인다. 다만 그 폭의 **숫자는 문턱이
   정한다**: pOCV RMSE 문턱 8/10/11/12 mV 에서 LAM_NE 폭이
   7.25 / 13.59 / 16.00 / **17.38** %p 로 변한다. 12 mV 는 다른 셀·다른
   목적함수에서 빌려 온 값이고, 그 문턱이 받아들이는 점 중에는 이 연구
   자신의 결합 목적함수에서 최적보다 42.9 % 나쁜 것이 있다.
   **오차막대가 아니라 분석자가 고른 민감도 절단값이다.**
