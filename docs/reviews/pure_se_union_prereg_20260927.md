# 사전등록 — 순수 SE 판정 시험: LHS 덱 프로토콜의 순수 SE union porosity (2026-09-27)

> 비준 = 사용자 09-27 (*"이거 봐보자"* — 순수 SE 침대로 판정).  **이 문서는 런 전에 커밋한다** — 판정선은 결과를 본 뒤 옮기지 않는다.

## 1. 질문

lhsx 64 (SE/고체 0.51–0.85) 의 겹침 보정 porosity (정확한 union) 는 **5.43–9.43 %** (중앙 6.55 %) 다 (`docs/data/lhs_union_20260927/`).
사용자 질문 (09-27): *"SE 만 압축될 때보다 AM 과 같이 압축될 때 더 압축되는 게 물리 아닌가"* — 이원 충전 (큰 AM = SE 기지 속 공극 없는 덩어리)
이라면 복합체가 순수 SE 보다 치밀한 것은 예상된다.  가를 것은 둘이다.

1. **이 프로토콜의 DEM 이 순수 SE 를 실험 권역보다 더 누르는가?**
2. **DEM 복합체 (lhsx) 는 DEM 자신의 순수 SE 기지를 희석한 만큼만 치밀한가?**

## 2. ⚠ 실험 기준을 바로잡는다 — *"Minnmann 순수 SE 10 %"* 는 실측값이 아니다

CLAUDE.md frame[1] 의 *"pure-SE porosity ≈ 10 % @ 300 MPa (Minnmann et al.)"* 는 **어떤 Minnmann 논문에도 없는 값이고 우리 MPM/DEM 보정 표적**이다 —
정본 카드 `minnmann2021_jes_charge_transport_bottlenecks` (*"porosity 는 복합 양극 14 % (13–17 %) @380 MPa, pure-SE 아님 — 'pure-SE 10 %' 는 이 논문이 주지 않음"*) ·
`minnmann2022_designing_cathodes_solidstate` (*"이 Perspective 엔 porosity 숫자가 하나도 없다 … pure-SE 10 % 는 우리 MPM/DEM 보정 표적"*).  원장 `SELF-52` 로 등록.
09-27 대화에서 내가 이 값을 *"Minnmann 실험값"* 이라 부른 것도 이 오귀속이다.

**이 시험의 실험 기준 (정본 카드에서 — 순수 LPSCl 냉간 성형 펠릿):**

| 출처 | 성형압 | 상대밀도 → 공극률 |
|---|---|---|
| `ohno2020_interlab_ionic_conductivity_argyrodite` (6 연구실) | 275–441 MPa | 81–95 % → **13.3 ± 5.3 %** (카드 DERIVED) |
| `doux2020_stack_pressure_assb` (Table S2, 4 펠릿) | 카드 참조 | 평균 82.1 % → 18 % |
| `adeli2019_halide_substitution_boosting_argyrodite` | 2 t · ⌀10 mm | 87 ± 1 % → 13 % |
| `ketter2025_resistor_network_models_predict_transport_properties` | 카드 참조 | ≈ 88 % → 12 % |

⇒ **실험 띠 = 8.0–18.6 %** (Ohno 연구실 간 ±1σ).  점이 아니라 띠로 쓴다 (ohno2020 카드 ⑥ 의 권고).

## 3. 침대 (4) — 모두 LHS 2-type 봉인 템플릿 `lhs00_110` 에서

| 케이스 | r_SE (µm) | volfrac | insert seed | 입자 수 (추정) |
|---|---|---|---|---|
| `pse_r050_a` | 0.50 | 0.22 | 20011 | ≈ 141 k |
| `pse_r075_a` | 0.75 | 0.22 | 20021 | ≈ 42 k |
| `pse_r100_a` | 1.00 | 0.22 | 20023 | ≈ 18 k |
| `pse_r100_b` | 1.00 | 0.22 | 20029 | ≈ 18 k (seed 반복 — 잡음 추정) |

- 생성: `scripts/lhs_ext_materialize.py --pure-se CASE:R_SE_UM:VOLFRAC:SEED … --template-2t <lhs00_110 덱>` —
  ~~AM 입자 템플릿 줄을 빼고 분포를 SE 하나 (가중 1) 로~~ ⛔ **정정 09-27 (런 전 · SELF-53)**: **AM 템플릿은 정의 · 분포에 그대로 두고 가중만 0 (SE 1)** —
  `2 pts1 0.000000 pts2 1.000000`.  줄을 빼거나 정의만 남기면 LIGGGHTS 가 `Atom types must start from 1 (properties.cpp:120)` 로 멈춘다
  (`docs/reviews/pure_se_ibb_failures_20260927.md`).
  **바꾸는 것은 그것과 r_SE · volfrac · seed · 케이스명뿐** (벽 재질 SE · 플래튼 메시 · 목표 300 MPa · E_SE 1.35 GPa · 재질 행렬 · 덤프 그대로).
  템플릿 sha256 은 봉인 상자 (`docs/data/lhs_ext_box_v2_20260829.json`) 의 `lhs00_110` 값 `aca27397…` 와 같아야 한다 (도구가 강제).
  selftest ~~42/42~~ → **61/61** (검토자 판 생성기, sha256 `43bd16216e334653…`).
- ⚠ **런 전 사후 수정 (09-27, 제출 전 — §4 판정선 불변)**: 실행 조건 두 가지를 더했다 — **15 MPI** (`--ntasks 15`: 러너 `#SBATCH -n 15` 와
  `mpirun --oversubscribe --bind-to none -np 15` 를 짝으로 · 원래 LHS 는 1 MPI) · **`processors * * 1`** (`region reg_box` 앞 — z 로만 자르던 분할을 x · y 로).
  **영역 분할만 다르고 물리는 같다** (코어 수를 바꿀 때처럼 비트 동일은 아니다).
- 두께 추정 ≈ 27 µm (volfrac 0.22 × 삽입 높이 ≈ 134 µm ÷ (1 − ε_sphere ≈ −0.08)) — r_SE 0.5 에서 ≈ 54 지름, 1.0 에서 ≈ 27 지름 (얇은 옛 순수 SE 침대
  `docs/data/esse_calibration_2mAh_real_9.csv` 7 · 8 행은 8.2 · 12.3 µm).
- 측정: `scripts/lhs_union_webapp.py --scan-root <런 폴더> --out pse_union.tsv` — sphere · 쌍 렌즈 union (웹앱 함수) · **정확한 union (MC 4×10⁶)** ·
  **내부 union** (바닥 · 플래튼에서 2 d_SE 뺀 띠 — 벽 효과 제거) · z 분포 · SE–SE δ/d · 배위수.

## 4. 판정선 (런 전 등록)

| # | 양 | 규칙 | 결과 어휘 |
|---|---|---|---|
| Q1 | 순수 SE **내부** 정확 union, 4 침대 중앙 | ≥ 8.0 % → 실험 띠 안 · 6.0–8.0 % → 띠 가장자리 (판정 보류) · < 6.0 % → **띠 아래 = 이 프로토콜은 SE 를 실험보다 더 누른다** | IN_BAND / EDGE / BELOW |
| Q2 | lhsx 64 의 정확 union − 희석 예측 ε_pSE(r_SE) × (1 − AM 부피분율), 중앙 (ε_pSE = 같은 r_SE 로 보간한 **전체 침대** 순수 SE union — lhsx 도 전체 침대 값) | \|중앙\| ≤ 1.0 %p → **DEM 복합체 = 자기 순수 SE 기지의 희석** · < −1.0 → 희석보다 더 치밀 (기전 필요) · > +1.0 → 희석보다 성김 (AM 주변 느슨함) | DILUTION / DENSER / LOOSER |
| Q3 | 순수 SE 에서 r_SE 효과: δ/d (SE–SE) 와 전체 union 의 r 0.5 → 1.0 변화 | δ/d 가 r_SE 와 함께 5 % 넘게 커지고 union 이 1.0 %p 넘게 준다 → **크기 의존 접촉 응답 (모델)** · 둘 다 잡음 안 → lhsx 의 크기 효과는 **복합체 충전** (AM 대비 크기비 · 배위수) 몫 | MODEL / PACKING |
| 잡음 | \|`pse_r100_a` − `pse_r100_b`\| (내부 · 전체 union · δ/d) | 위 차이가 이 값의 2 배를 넘지 못하면 "분해 안 됨" 으로 쓴다 | — |

- **내 사전 예상 (적어 둔다)**: Q1 = EDGE 또는 BELOW (6–7.5 %) — lhsx 가 SE/고체 0.85 에서 이미 ~6 % 이고 SE–SE δ/d 0.107 이 얇은 순수 SE 침대 (≈ 0.11)
  와 같아 SE 기지가 순수 SE 만큼 눌려 있다.  Q2 = LOOSER (+1 ~ +2 %p).  Q3 = PACKING 쪽 (lhsx 에서 SE–SE 배위수가 r_SE 와 함께 준다 — 편상관 −0.28).
- 결과가 무엇이든 **생산 기본값 · E_SE 보정은 바꾸지 않는다** — 이 시험은 LHS 인계표의 porosity 열 규약 (union 열 · 질량 보존 두께 열 · SE-rich 표지) 을
  정하는 근거다 (판단 J19 → 저자 비준).

## 5. 실행 (사용자 — WSL 에서 덱 → ibb 제출 → WSL 에서 측정)

```bash
# ⛔ 09-27 정정 — 아래가 실제로 쓴 명령이다 (옛 판: 리포 생성기 42/42 · --ntasks 없음 → 제출 ①②③ 실패, SELF-53).
# WSL: 검토자 판 생성기 (이 커밋에서 scripts/ 로 교체된 것과 같은 파일) 로 덱 생성 — 봉인 템플릿 sha 를 도구가 확인
PY=~/Yonghoon-DEM-DFT/venv/bin/python3
$PY ~/lhs_ext_materialize.py --selftest | tail -1                                                   # 61/61
$PY ~/lhs_ext_materialize.py \
  --pure-se pse_r050_a:0.5:0.22:20011 --pure-se pse_r075_a:0.75:0.22:20021 \
  --pure-se pse_r100_a:1.0:0.22:20023 --pure-se pse_r100_b:1.0:0.22:20029 \
  --template-2t ~/lhs_local/lhs00_110/input_lhs00_110.liggghts --template-run ~/lhs_local/lhs00_110/run_lhs00_110.sh \
  --box ~/dem-web/docs/data/lhs_ext_box_v2_20260829.json --ntasks 15 --outdir ~/pse_decks_20260927b
# ibb: 옛 실패 폴더는 pse_*.fail_0927 로 옮기고 (지우지 않음) 새 덱을 lhs 폴더 옆에 올려 sbatch — 러너는 도구가 만든 것 (-n 15 · mpirun 짝)
# 끝나면 원본을 WSL 로 (post_* 전체) → 측정
~/Yonghoon-DEM-DFT/venv/bin/python3 ~/dem-web/scripts/lhs_union_webapp.py --scan-root ~/pse_local --out ~/pse_union.tsv
```

## 6. 결과 (런 뒤 채운다)

### 6-0. 제출 기록 (결과 아님)

- 실패 3 회 (231852–55 · 231865–68 · 231896–99) — 원인 · 정정된 처방 = `docs/reviews/pure_se_ibb_failures_20260927.md` · 원장 SELF-53.
  세 번 모두 적분 전에 멈춰 데이터가 없다.
- **네 번째 제출 (09-27 ≈ 11:40 KST)**: job **231946 – 231949** (`pse_r050_a` · `pse_r075_a` · `pse_r100_a` · `pse_r100_b`) RUNNING · node01 · 15 MPI ·
  `3 by 5 by 1 MPI processor grid` (검토자 시험 덱은 5 by 3 by 1 — 상자 모양에 따라 LIGGGHTS 가 고른다, 둘 다 x · y 분할) · ERROR 0 ·
  삽입 **139,706 · 41,394 · 17,463 · 17,463** (§3 추정 ≈ 141 k · 42 k · 18 k · 18 k) · PHASE 1 (침강).

### 6-1. 판정 — 비어 있음 (런 뒤)
