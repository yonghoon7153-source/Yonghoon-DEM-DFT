# pure-SE OAT 민감도 + E 스윕 — 실행 패키지

> 2026-08-25.  LIGGGHTS-PUBLIC 3.8.0.  **입력만 들어 있고 결과는 없다.**

## 무엇을, 왜

우리 DEM 은 LPSCl SE 의 영률을 **실물 22–24 GPa → E_eff 1.35 GPa (18× 연화)** 로 낮춰
거시 porosity(Minnmann pure-SE ~10 % @ 300 MPa)에 맞춘다.  이 절차의 정당성은
**bulk calibration approach** (Coetzee, *Powder Technol.* **310** (2017) 104–142) 에 있고,
그 리뷰 §5 가 요구하는 조건이 하나 있다:

> *"more than one experiment should be conducted and **each experiment should isolate a
> single parameter**"*

우리는 "관측량 1개(porosity@300) → 파라미터 1개(E_eff)" 라 **형식상** 유일하다.
그런데 그 형식을 떠받치는 전제 — *"구속 단축압축은 입자강성에만 반응하고 마찰에는 둔감"* —
는 **남의 계에서 빌려온 것**이다 (Coetzee & Els 의 파쇄암·옥수수, 저응력).
**우리 계(황화물 SE, 300 MPa)에서 재현된 적이 없다.**

⇒ 이 스윕은 그것을 **재는** 것이다.  `∂ε/∂μ ≈ 0` 이 나와야
*"우리 보정은 파라미터를 고립시킨다"* 고 쓸 자격이 생긴다.
안 나오면 보정이 뒤엉킨 것이고, **그것도 알아야 할 사실**이다.

## 13 런

| 런 | 표 | 무엇 |
|---|---|---|
| `orig_1type` | **대조** | 원본 1-type, 출력 경로만 변경 |
| `base` | **대조** | 생산값, 2-type |
| `oat_mu_pp{0.2,0.4,0.6}` | A | 입자-입자 마찰 |
| `oat_mu_pw{0.2,0.4,0.6}` | A | 입자-벽 마찰 |
| `oat_cor{0.2,0.4,0.6}` | A | 반발계수 |
| `esweep_E{5,24}` | B | 영률 (생산 1.35 포함 3점) |

생산값: `mu_pp 0.5 · mu_pw 0.5 · COR 0.3 · roll 0.1 · E 1.35 GPa`.
표 B 는 porosity 뿐 아니라 **배위수·접촉면적·σ 삼중항**을 함께 본다
(Ng & Asce 가 보고한 *"강성↓ → 배위수↑"* 결합이 우리 24→1.35 구간에서 미측정).

## ⚠⚠ 대조가 **둘**인 이유 — 읽어야 할 부분

원본 입력은 **atom type 이 1개**다.  LIGGGHTS 에서 벽은 `type N` 으로 재료 물성을 참조하므로,
type 이 하나면 **벽 마찰이 입자 마찰에 묶인다** → `mu_pw` 를 독립적으로 흔들 수 없다.
그래서 type 을 2로 늘리고 벽에 type 2 를 준다 (벽 물성값은 입자와 동일 = 원본 거동 보존,
마찰만 비대각으로 분리).

**그런데 대조 하나로는 부족하다.**  옛 LIGGGHTS 바이너리가 사라져 새로 빌드했으므로,
기준선이 옛 기록과 안 맞아도 원인이 **type 리팩터**인지 **다른 빌드**인지 못 가른다.

    orig_1type (새 빌드 · 1-type)  vs  docs/data/heckel_pure_se_dem.csv   → 빌드 효과
    base       (새 빌드 · 2-type)  vs  orig_1type                        → 리팩터 효과

**둘 다 0 이어야 OAT 를 믿는다.**  러너가 이 순서로 먼저 돌리고, 하나라도 실패하면 멈춘다.

## ⚠ 원본 입력은 실행 가능한 파일이 아니었다

`heckel/*.liggghts` 4개가 **Python `.format()` 템플릿이 렌더 안 된 채로** 커밋돼 있었다
(중괄호 이중 → LIGGGHTS 가 `Substitution for illegal variable (input.cpp:505)` 로 즉사).
상류 원인은 `scripts/make_heckel_inputs.py` 가 `.format()` 대신 `.replace()` 를 쓰는 것.

참조 변수 8개(`dt` `r_SE` `plate_margin` `target_press` `z_max` `plate_z` `press_speed`
`current_press`)가 **전부 같은 파일 안에 `variable … equal` 로 정의**돼 있어,
기계적 de-escape 하나로 자기완결적으로 복원된다 (**값을 지어내지 않았다**).
13런 **전부에 똑같이** 적용했으므로 대조는 유효하다.

⚠ 다만 `orig_1type` 의 성격이 *"원본과 바이트 동일"* → *"원본 + 문서화된 기계 변환"* 으로 바뀐다.
⚠ 그리고 **옛 기록을 만든 렌더가 이것과 같았다는 보장이 없다** — 값이 어긋나면
**빌드·리팩터·렌더 셋** 중 어디서 갈렸는지 다시 갈라야 한다.

## 실행

    bash run_all.sh                                              # PATH 의 liggghts
    MPI=no LIGGGHTS=/path/to/lmp_serial bash run_all.sh          # serial 빌드
    NP=8   LIGGGHTS=/path/to/lmp_auto   bash run_all.sh          # mpirun -np 8

⚠ **serial 이 더 빠를 수 있다** (실측 39.3 vs mpirun-8 28.1 step/s).
박스 z 가 입자 영역의 33배라 랭크 대부분이 빈 공간을 받는다.

진행 확인:

    watch -n 300 'bash ../../scripts/watch_oat_sweep.sh'

## 규모 (실측)

40,250 입자 · **39.3 step/s** (serial) · 런당 ~500,000 스텝
⇒ **런당 3.5–5 h**, 13런이면 **2일 이상**.  ⚠ 압축 루프가 300 MPa 도달까지라 **하한**이다.

★ **대조 2건(≈7 h)만으로 판정이 난다.**  어긋나면 나머지 11런은 돌릴 이유가 없다.

## 재현

    python3 ../../scripts/gen_dem_oat_sweep.py --check    # 계획
    python3 ../../scripts/gen_dem_oat_sweep.py --write    # 재생성
    python3 ../../scripts/gen_dem_oat_sweep.py --selftest # 35/35

⚠ `in.*.liggghts` 는 **생성물**이다.  손으로 고치지 말고 생성기를 고칠 것.

## 알려진 미해결

- 옛 기록의 **MPI 랭크 수를 모른다** → DEM 은 영역분할이 바뀌면 반올림 수준에서 궤적이 갈린다.
  **정확 일치를 기대하면 안 되고, "몇 %p 안에 드는가" 로 봐야 한다.**
- `make_heckel_inputs.py` 의 `.replace()`↔`.format()` 불일치는 **아직 안 고쳤다**
  (지금 고치면 비교 대상이 또 움직인다 — 대조 2건이 끝난 뒤에).
