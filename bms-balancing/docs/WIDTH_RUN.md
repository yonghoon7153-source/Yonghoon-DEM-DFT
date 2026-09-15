# 실데이터 폭 측정 런북 — `--w-dqdv 0 ↔ 1` (사용자 기계)

2026-09-15. **이 문서는 명령서다.** 숫자는 하나도 없다 — 돌리면 나온다. 정본은 그때
사용자 기계에 생기는 `cycles_HD_knee_Li.csv` + `.meta.json` 이다.

> **파일럿은 돌았다 (2026-09-15, HD_knee `--cycles 0,1,2`).** 결과와 영수증은
> `reviews/BML_R1_RESPONSE.md` **§14** 에 있다 — 한 줄로: **dQ/dV 항은 폭을 안 좁히고
> LAM_NE 는 2.9 배가 됐으며, `w_dqdv 1` 의 cycle 1 에서 LAM_NE 부호 식별을 잃었다.**
> 이 문서는 **전 사이클 실행**과 다음 사람을 위해 남긴다.

## 0. 왜 이걸 재나

`BML_R1_RESPONSE.md` §12-5 가 **"이 데이터에서 LAM 분할은 점추정으로 보고할 수 없고 폭과
함께 보고해야 한다"** 로 닫혔고, §13 이 그 결론을 도구에 넣었다 (`--widths` 가 아홉 열을
점추정과 **같은 행에** 붙인다).

남은 질문 하나가 **아직 실데이터에서 안 물어졌다** — **목적함수에 dQ/dV 항을 넣으면 그 폭이
달라지는가.** `w_dqdv` 는 원본 기본값이 0("방법 3")이고, 1 로 올리면 dQ/dV 봉우리가 적합을
더 끌어당긴다. 폭이 줄면 "그 항이 축퇴를 깬다" 는 뜻이고, 안 줄면 **축퇴가 목적함수의
문제가 아니라 데이터의 문제**라는 근거가 하나 더 붙는다.

> ⚠ **폭이 좁아졌다고 그 설정이 옳다는 뜻이 아니다.** 좁은 답이 참에 가깝다는 근거는
> 따로 필요하다. 도구가 출력 끝에 이 문장을 직접 찍는다.

## 1. 저장소 쪽 배관은 **여기서 돌렸다** (2026-09-15, 합성 데이터)

명령을 넘기기 전에 이 컨테이너에서 **끝에서 끝까지** 한 번 돌렸다. 합성 원자료
(`matlab/tests/gen_synth_xlsx.py`)로 만든 3 사이클 워크북 · `--starts 4` · `--width-starts 2`.

| 확인한 것 | 실측 |
|---|---|
| `fit_cycles.py --widths` (`--w-dqdv 0`) | rc 0 · 3 행 · **37.2 s** |
| `fit_cycles.py --widths` (`--w-dqdv 1`) | rc 0 · 3 행 · **104.8 s** |
| `width_report.py A B --axis w_dqdv` | **rc 0** — 표 둘 + 비교 표 |
| `check_rails.py` (폭 열이 붙은 산출) | **rc 0** (error 0 · warning 7 · info 11) |
| `check_u14.py --schema-only` | **rc 0** · `새 스키마: 전부 갖췄다` |
| meta 의 비교 대상 설정 20 개 | **전부 기록됨** (`lb`…`cycles`) |

**여기서 나온 숫자는 합성이라 인용 불가다.** 확인한 것은 오직 **배관이 돈다**는 것 —
사용자 기계에서 처음 만나는 오류가 우리 코드의 것이 아니게 하려고 먼저 돌렸다.

### 1-1. 가드 셋이 **실제로 문다** (실측 rc)

`width_report.py` 는 두 실행이 **축 하나만** 달라야 비교한다. 세 갈래를 다 걸어 봤다.

| 상황 | 실측 |
|---|---|
| 두 실행의 `w_dqdv` 가 **같다** (A vs A) | **rc 2** — `! 두 실행의 w_dqdv 가 같다 (0.0)` |
| `--axis` 를 엉뚱한 것으로 (A vs B, `--axis seed`) | **rc 2** — `! 두 실행의 seed 가 같다 (0)` |
| 축 말고 **다른 설정이 또 다르다** (`--seed` 도 다른 C) | **rc 2** — `! 축(w_dqdv) 말고 다른 설정이 다르다` + `seed: 0 ↔ 1` |

> **이 가드가 이 작업의 핵심이다.** 두 실행이 두 군데 다르면 그 비교는 **아무것도 뜻하지
> 않는데 눈으로는 안 보인다.** 그래서 기계가 막는다. 아래 명령에서 플래그 하나라도
> 흘리면 3 번째 줄이 뜬다 — 그건 고장이 아니라 **작동한 것**이다.

세 갈래는 회귀로도 고정돼 있다 (`tests/test_widths.py` **W-16·W-17·W-18**). 이번 실행은
그 회귀가 **실제 산출에서도** 같게 도는지 본 것이다.

## 2. 명령 — 두 실행은 `--w-dqdv` **하나만** 다르다

세트는 **HD_knee** 다 (`L_*` 원자료는 없다 — `BML_R1_RESPONSE.md` §10-4).
`D` = 규진팀 `degradation mode` 폴더 · `H` = 이 하네스. 둘 다 `git pull` 뒤.

```bash
export D='/mnt/d/…/degradation mode'          # 규진팀 원자료 루트
export H=~/…/Yonghoon-DEM-DFT/bms-balancing   # 이 저장소

# ── A: w_dqdv 0 (원본 기본 = "방법 3")
python3 $H/scripts/fit_cycles.py --data-root "$D" \
  --half-cell "$D/data/half_cell/GITT/pristine.xlsx" \
  --full-cell "$D/experiment/HD_ICA/300cycle knee point large cell.xlsx" \
  --cell HD_knee --si-source Li \
  --starts 20 --seed 0 --scale-seed 0 \
  --w-dqdv 0 \
  --widths --width-tol 0.01 --width-starts 4 \
  --out ~/out_widths/w0

# ── B: w_dqdv 1 — 위와 **이 한 줄만** 다르다
python3 $H/scripts/fit_cycles.py --data-root "$D" \
  --half-cell "$D/data/half_cell/GITT/pristine.xlsx" \
  --full-cell "$D/experiment/HD_ICA/300cycle knee point large cell.xlsx" \
  --cell HD_knee --si-source Li \
  --starts 20 --seed 0 --scale-seed 0 \
  --w-dqdv 1 \
  --widths --width-tol 0.01 --width-starts 4 \
  --out ~/out_widths/w1

# ── 읽기
python3 $H/scripts/width_report.py \
  ~/out_widths/w0/cycles_HD_knee_Li.csv \
  ~/out_widths/w1/cycles_HD_knee_Li.csv --axis w_dqdv

# ── 난간 (두 산출 다)
python3 $H/scripts/check_rails.py ~/out_widths/w0/cycles_HD_knee_Li.csv ~/out_widths/w1/cycles_HD_knee_Li.csv

# ── 스키마 (각각 따로 — 서로 견주지 않는다)
python3 $H/scripts/check_u14.py --new ~/out_widths/w0 --schema-only
python3 $H/scripts/check_u14.py --new ~/out_widths/w1 --schema-only
```

> ⚠ **`check_u14 --new w1 --old w0` 를 쓰지 않는다** (2026-09-15 정정 — 이 런북의 첫 판이 그렇게
> 적었다). u14 는 **승격 게이트**이고 "계산 경로를 안 고쳤으니 같아야 한다" 를 묻는다. 우리는 축을
> **일부러** 바꿨으므로 `numbers N` 은 결함이 아니라 의도한 차이다. 두 실행이 한 축만 달랐는지는
> `width_report.py` 가 이미 판정한다 (`COMPARED_SETTINGS` 20 개, 어긋나면 rc 2).
>
> 그래도 굳이 걸어 보면 `blocked_by.controls` 에 **`w_dqdv` 가 이름과 함께** 뜬다 —
> W-19 로 `CYCLES_META_CONTROLS` 에 더했다 (`BML_R1_RESPONSE.md` §14-6). 첫 실행 때는
> `controls 0` 이라 **일부러 바꾼 축이 "설명 없는 숫자 변화" 로** 보고됐다.

`--seed 0 --scale-seed 0` 은 **둘 다 같아야 한다.** 여기를 흘리면 §1-1 의 세 번째 가드가 문다.

### 2-1. 먼저 **파일럿** 한 번 — 시간부터 잰다

전 사이클로 바로 가지 말고 세 사이클만:

```bash
# 두 실행 **양쪽 다** --cycles 를 똑같이 준다 (cycles 도 비교 대상 설정이다)
… --cycles 0,1,2 --out ~/out_widths/pilot_w0
… --cycles 0,1,2 --out ~/out_widths/pilot_w1
python3 $H/scripts/width_report.py ~/out_widths/pilot_w0/cycles_HD_knee_Li.csv \
                                    ~/out_widths/pilot_w1/cycles_HD_knee_Li.csv --axis w_dqdv
```

> ⚠ **한쪽만 `--cycles` 를 주면 비교가 거부된다** — `cycles` 는 `COMPARED_SETTINGS` 20 개
> 안에 있다. 파일럿과 본 실행을 섞어 견주지도 않는다.

**시간 예상은 하지 않는다 — 파일럿이 잰다.** 위 §1 의 37 s / 105 s 는 `--starts 4`
`--width-starts 2` 짜리 **합성 3 사이클**의 값이고, 본 실행은 시작점이 5 배(4→20)·폭
시작점이 2 배(2→4)에 사이클 수도 다르다. 파일럿의 실제 벽시계에 사이클 비를 곱해서
본 실행을 걸지 말지 정한다. **`--w-dqdv 1` 쪽이 확실히 더 느리다** (실측 2.8 배).

## 3. 결과를 읽는 법

`width_report.py` 가 셋을 찍는다 — A 표 · B 표 · 비교 표. 비교 표의 판정은 기계가 정한다:
**B/A < 0.9 = 좁아졌다 · > 1.1 = 넓어졌다 · 그 사이 = 거의 그대로.**

| 무엇을 말할 수 있나 | 무엇을 말할 수 없나 |
|---|---|
| 이 셀·이 사이클 집합·이 허용(`--width-tol 0.01`)에서 그 축의 폭이 어떻게 움직였나 | 다른 셀·다른 허용으로의 일반화 |
| 폭이 **하한**이라는 것 (`width_is_lower_bound` 가 행마다 True) | 참 폭 — 국소 해법 + 격자라 이보다 넓을 수 있다 |
| **모델 고정 축**의 폭 | **문헌 곡선 선택이 만드는 폭** — 그쪽이 더 크고 여기 **안 들어간다.** 두 축을 합치지 않는다 |
| 좁아졌다/넓어졌다는 **사실** | 좁은 쪽이 **옳다**는 것 |

`width_status` 가 전 행 `measured` 가 아니면 `width_report.py` 가 **rc 2 로 멈춘다** —
안 잰 행이 섞인 표는 모집단을 말할 수 없기 때문이다. `not_requested`(안 켬)와
`failed`(재다 실패)와 `measured` 는 **서로 다른 상태**이고, 빈 칸을 0 으로 읽지 않는다
(0 은 "폭이 0 = 완벽히 식별됐다" 가 되고 그건 §12-5 가 반박한 주장이다).

## 4. 산출을 어떻게 다루나

**`~/out_widths/` 를 저장소에 커밋하지 않는다.** 규진팀 원자료와 같은 이유다 (`FINDINGS.md`
의 원자료 규칙). 저장소로 오는 것은 **숫자와 영수증**이지 원자료에서 파생된 전체 산출이
아니다.

보고할 때 같이 넘길 것:

1. `width_report.py` 의 **출력 전문** (세 표 전부 — 비교 표만 옮기면 허용·seed·starts 가 사라진다).
2. 두 `.meta.json` 의 `run_id` · `inputs_sha` · `env` · `git` — 어느 코드·어느 입력이었는지.
3. `check_rails.py` 의 RAILS 줄과 `check_u14.py --schema-only` 의 PROMOTION 줄 (rc 포함).
4. 두 실행의 **벽시계 시간** (다음 사람이 예산을 세울 수 있게).

그 넷이 오면 `BML_R1_RESPONSE.md` 에 §14 로 적고 **폭이 인용 가능한 형태**가 된다.

## 5. 이것이 닫지 **않는** 것

- 문헌 곡선 축의 폭 (`matrix_*`) — **다른 축이고 합치지 않는다.**
- `mode_profile_extrema`(도달 가능성 격자)는 **붙었다** (§15-1, `--width-grid N`). 다만 우리가 잰 세
  자리에서 **합집합 이득이 0** 이었고 벽시계만 +64 % 였다 → **기본은 꺼짐**이고, 위 명령은 기본값
  이므로 §14 와 같은 축에서 잰다. 켜면 `width_method` 가 달라져 §14 와 **비교가 거부된다.**
- γ 사전 적합이 하한 0.02 에 붙는 열린 항목 (§13-5 → §15-3) — 가르는 도구는
  `scripts/gamma_prefit_report.py` 다 (읽기만 한다). 합성 실측으로 **방향 규약은 배제**됐고
  남는 둘은 실데이터에서 가른다. 5 파라미터 적합이 초기값과 무관하게 같은 곳에 앉으므로
  LAM 결론은 안 바뀐다.
- 게이트 리뷰(63·64차) · COMSOL 갈래와 **무관**하다 — 판정을 섞지 않는다.
