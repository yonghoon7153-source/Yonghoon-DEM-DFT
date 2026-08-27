---
title: "회신 I — 3주 NEB 는 HOLD (영구 폐기 아님). 우리 잠정판단 N3 이 기각됐고 P0 3건이 나왔다"
date: 2026-08-27
updated: 2026-08-27
tags: [review/codex, neb, li3nd, cell-convergence, vacancy, retraction]
status: 반영중
confidence: medium
verificationStatus: unverified
# ⚠ 스키마에 'partially-verified' 가 없어 unverified 로 둔다. 실제로는 갈린다:
#   ✅ 확인됨 — P0-3 코드 버그(재현·수정·selftest) · Li 부격자 산술(우리 원자 수와 일치)
#   ⏸ 미확인 — P0-1 정렬 판정(좌표가 gabia) · P0-2 pristine soft mode · dimer 운영비
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

> 회신 I 원문은 붙여넣기 그대로 아래 6절. 이 카드는 **우리가 뭘 철회하고 뭘 하기로 했나**가 본문이다.
> 보낸 질문지: `kb/reviews/codex_I_neb_cc333_worth_it_2026_08_27.md`

## 0. 한 줄

**우리 잠정판단(N3: "협동 이동이니 NEB 는 틀린 관측량이다")이 기각됐다.**
그리고 우리가 묻지 않은 곳에서 **P0 세 건**이 나왔다 — 그중 둘은 우리 코드다.

| | 우리가 물은 것 | 회신 |
|---|---|---|
| N1 | 3주 값어치 | **조건부 HOLD** — P0 통과 후 재판단 |
| N2 | 크기 vs 농도 분리 | **목표에 따라 다름** — dilute limit 이면 현 설계가 맞다 |
| N3 | 협동 이동 ⇒ 장벽 무효? | **기각** — full NEB 의 collective MEP 는 유효하다 |
| N4 | step 30 재개? | **제3안** — 좌표 유지 + Broyden history 만 초기화 |
| N5 | 금속이면? | 장벽은 정의된다. 대신 **smearing 사다리**가 필요 |

## 1. 🔴 철회 — 우리가 틀린 것 4건

### ⛔ 철회 ① "싼 우회로가 물리적으로 막혔다"

질문지 제목부터 이 문장이었다. **틀렸다.**
막힌 것은 **중점법(고정셸)과 saddle 이식** 둘뿐이고, 그 둘은 *변위장이 국소*라는 전제를 쓴다.
**dimer / minimum-mode following 은 전 원자를 자유롭게 두므로 그 전제를 안 쓴다** —
step 19 또는 30 의 최고에너지 image 와 tangent 를 출발점으로 직접 1차 안장을 찾는다.
"물리적으로 가능한 제3의 길이 없다" 는 **우리가 확인하지 않고 한 말**이다.

⚠ 다만 회신도 단서를 달았다: 실행환경 구축비가 크면 *운영상* 싸지 않을 수 있다.
"물리적으로 막혔다" 와 "우리 환경에서 비싸다" 는 다른 말이고, 우리는 앞엣말을 했다.

### ⛔ 철회 ② "1.240 Å 는 물리다" — **미확정**으로 내린다

`symmetric_saddle.build_frozen` 도 `build_neb_inputs.endpoint_displacement_max_A` 도
두 끝점을 **원자 순서대로 zip** 해서 변위를 잰다. 그 값에는 물리가 아닌 두 성분이 섞인다:

1. 두 끝점을 **독립 이완**하며 각각 얻은 **강체 표류** — 셀은 병진 불변이라 물리가 아니다
2. 같은 원소끼리의 **라벨 교환**

그리고 **우리 기록이 이미 그 지문을 갖고 있었다**:

| 우리 기록 | 문장 |
|---|---|
| `sei_cc333_nd_lattice_hop_2026_08_17.md:44` | `_r2` 에서 Nd 1.08–1.24 · **107/107 원자 이동** |
| `symmetric_saddle.parse_input_positions` docstring | *"cc333 의 relax.out 은 미수렴 BFGS 가 50스텝 밀어낸 **표류 구조**라 홉이 3.667 → 4.203 Å 로 벌어지고 이웃 하나가 1.24 Å 움직였다"* |

**107개 전부가 움직였다**는 것과 **Li 자신은 제 자리에서 0.029/0.030 Å 밖에 안 움직였는데
홉 거리가 3.667 → 4.203 으로 벌어졌다**는 것은 둘 다 *두 끝점 사이의 상대 강체 표류*의 지문이다.
우리 도구가 그걸 "표류" 라고 적어놓고, 같은 좌표에서 나온 1.240 을 **물리적 실체**라고 썼다.

⇒ **`kb/results/sei_cc333_nd_lattice_hop_2026_08_17.md` §2 와 결론 ① 을 미확정으로 내린다.**
확인 도구를 만들었다(아래 3절). 좌표는 gabia 에 있어 거기서 돌려야 한다.

### ⛔ 철회 ③ 공공 농도 분모가 틀렸다

`1/32` · `1/108` 은 **전체 원자 자리** 기준 결손률이다. Li 공공 농도는 **Li 부격자** 기준이어야 한다.

| | 우리가 쓴 값 | 옳은 값 (Li 부격자) |
|---|---|---|
| 2×2×2 | 1/32 = 3.1 % | **1/24 = 4.17 %** |
| 3×3×3 | 1/108 = 0.93 % | **1/81 = 1.23 %** |

비(3.375)는 같아서 "3.4배 다르다" 는 결론은 안 흔들리지만, DB 에 적히는 숫자가 틀렸다.
회신이 요구한 대로 다음을 **따로** 기록한다: `vacancy_fraction_li_sublattice` ·
`N_v/부피` · **최단 공공–이미지 거리** · 셀 형상 · 공공 배열.

### ⛔ 철회 ④ N3 — comp1 판정의 이식

comp1 에서 *"NEB 는 이 계의 틀린 관측량"* 이라고 한 근거는 **세 개가 같이 있었기 때문**이다:

1. 이동 Li 를 **고정해야** 100 % 홉이 유지됨
2. 나머지 Li 가 **2.41 Å** 재배열
3. 수렴 밴드가 시작점보다 **0.283 eV 낮은** basin 을 통과 ⇒ 반응좌표 붕괴

li3nd 는 **반대 증거**를 갖고 있다: 대칭 등가 c→c 끝점 · 끝점 ΔE **4.4 meV** ·
이동 Li 가 놓인 자리에서 **0.03 Å** 만 이동. **자동 이식할 수 없다.**

그리고 회신이 정확히 우리가 부탁한 곳을 봤다:

> 정적 장벽은 전체 원자의 3N 차원 PES 에서 두 metastable basin 을 잇는 경로로 정의된다.
> **여기에는 "한 원자만 움직여야 한다" 는 조건이 없다.**

Nd 집단이완이 무효화하는 것은 **중점법 · 국소 frozen-shell · saddle 이식 · "단일 Li 직선 홉"이라는 이름**이지,
전 원자를 자유롭게 둔 full NEB 의 collective MEP 자체가 아니다.

✅ 우리가 요청한 자기검증("3주가 비싸서 안 하고 싶은 것과 안 해야 하는 것은 다르다")에
회신이 답을 줬다 — **우리는 비싸서 안 하고 싶은 쪽이었다.**

## 2. ✅ 확인 — 회신이 맞은 것 / 부분적으로 맞은 것

### P0-3 은 실재하는 버그다 (생성기). 다만 러너는 이미 막고 있었다

**맞다**: `build_neb_inputs.py` 는 `ci_scheme != "no-CI" and restart` 일 때만 `restart_mode='restart'` 를
썼다. 즉 **중단된 no-CI 런을 이어달리려고 `--restart` 를 줘도 조용히 `from_scratch`** 였다.
→ 고쳤다. 이제 `--restart` 는 단독으로 존중되고, `<tag>.path` 가 없으면 **거부**한다.

**부분적으로 틀렸다**: 회신은 "gabia 가 처음부터 시작할 위험" 이라고 했는데,
러너 `run_sei_neb.sh:prep_resume` 이 **2026-08-24 부터** 실행 직전에 `neb.in` 의 `restart_mode` 를
`'restart'` 로 고쳐 쓴다(같은 사고를 한 번 겪고 넣은 장치다). 그래서 **멈춰 있는 체크포인트는 멀쩡하다.**
생성기 버그는 *다음 재빌드* 때 물었을 것이다.

**대신 러너에 세 번째 구멍이 있었다** — `prep_resume` 은 이력을 `neb.out` 에서 센다.
`ci` 단계가 `mv neb.out neb.out.noCI` 를 하고 나면 이력이 0 으로 보여 **손을 떼고**,
그러면 `from_scratch` 가 살아있는 `.path` 위에 그대로 선다. 백업에서 이력을 찾도록 고쳤다.

### P0-2 — Nd 재배열이 vacancy 때문인지 3×3×3 자체의 soft mode 인지 안 갈렸다

*"2×2×2 엔 없고 3×3×3 에만 있다"* 는 두 해석과 **모두 양립**한다:
① 공공이 넓은 셀에서 Nd 이완을 유발 ② 2×2×2 가 표현 못 하는 q≈1/3 구조 모드가 열린 것.
후자면 **Fm-3m 셀 자체가 숨은 재구성에 불안정**한 것이고, 그때는 MD 로 옮겨도 해결이 안 된다
(같은 불안정한 구조에서 낸 MD Ea 도 조건부 값이다). ← 우리가 못 본 지점이다.

싼 control: pristine 3×3×3 에 대칭 끄고 rattle 여러 개 → 이완. 같은 Nd 패턴이 나오면 끝점부터 다시.

### N5 — degauss 가 장벽과 같은 에너지 규모다

`degauss = 0.02 Ry ≈ 0.272 eV` 이고 장벽이 0.229 eV 다. **같은 자릿수다.**
그게 곧 0.272 eV 오차라는 뜻은 아니지만, 같은 k-point 밀도에서 `0.02 → 0.01 → 0.005 Ry`
사다리를 타서 장벽 변화가 사전 허용폭 안인지 봐야 한다. 우리는 이 검사를 한 적이 없다.

또 하나: NEB 가 주는 건 **이미 있는 공공의 이동 장벽 `E_m`** 이다.
intrinsic 평형 공공 수송은 `E_f^v + E_m` 이라, 0.229 를 MD 아레니우스 Ea 와 **바로 동일시하면 안 된다.**

### N1 — 두 점으로 말할 수 있는 것의 한계

수렴시켜도 얻는 것은 *"같은 one-vacancy 모델에서 2×2×2 → 3×3×3 확장에 대한 **barrier sensitivity**"* 까지다.
❌ 희박한계 수렴 · ❌ 순수 크기/순수 농도 효과 · ❌ 상한·하한 · ❌ 잔여 유한크기 오차의 상한 — 전부 못 한다.
**미수렴 step 30 의 0.128 eV 는 그 제한적 상한으로도 못 쓴다.**

## 3. 우리가 한 것 (2026-08-27)

| 항목 | 상태 |
|---|---|
| `symmetric_saddle.py --align_check` | ✅ 새로 만듦 — 병진·라벨 제거 후 잔여를 거리별로 낸다 |
| 〃 selftest (음성 4 + 양성 2 + 가드 2) | ✅ 8/8. 핵심: **순수 병진 1.10 Å → "인공물"** |
| `build_neb_inputs.py` restart_mode | ✅ 고침 + `.path` 없으면 거부 |
| `run_sei_neb.sh` prep_resume 백업 폴백 | ✅ 고침 + selftest ⑦/⑦'/⑦'' |
| 공공 농도 분모 | ✅ Li 부격자 기준으로 정정 |
| gabia 에서 `--align_check` 실행 | ⏸ **대기 — 이게 다음 관문이다** |
| pristine 3×3×3 rattle control (P0-2) | ⏸ 미착수 |
| dimer pilot | ⏸ 미착수 |

**판정 규칙(사전 등록)** — `--align_check --align_source both` 의 far-field 잔여로:

- ≤ **0.05 Å** → 1.240 은 인공물. **중점법이 되살아난다.** 3주 NEB 불필요.
- ≥ **0.30 Å** → 비국소 이완이 실제. 중점법은 계속 막힌다.
- 사이 → 어느 쪽도 주장하지 않는다.

⚠ 이 도구가 **못 하는 것**: 공간군 회전·반사는 안 뺀다 · 잔여가 물리인지 **미수렴 표류**인지 못 가른다
(그래서 `--align_source both` 로 갓 지은 좌표와 이완 좌표를 나란히 본다).

## 4. 실행 순서 (회신 결정 그대로)

1. ~~full NEB 재개~~ → **보류**
2. 끝점 PBC·대칭·permutation 재매핑 ← **여기**
3. pristine 3×3×3 rattle / soft-mode control
4. gabia 실제 입력의 `restart_mode` 와 체크포인트 완전성 확인
5. step 30 path topology 분석
6. 좌표 유지 + Broyden reset **또는** dimer pilot 을 **1–2일 예산**으로
7. 여기를 통과하고 **큰 셀 collective barrier 가 원고 결론을 실제로 바꿀 때만** 조건부 재개

### 체크포인트는 `li3nd.path` 하나가 아니다

`li3nd.path` · `li3nd.broyden` · **이미지별 SCF 상태(tmp/)** · `neb.in` · `neb.out` · protocol/meta/hash.
현재 `gabia:~/ckpt_cc333_0827/` 이 이걸 다 갖고 있는지 확인해야 한다.

### N4 재개 방법 — 제3안

`li3nd.path` 와 이미지별 SCF 는 **유지**, `li3nd.broyden` 만 따로 보존 후 활성 폴더에서 **제거**.
`restart_mode='restart'` 명시 · **`CI_scheme='no-CI'` 로 먼저** · 필요하면 `ds` 를 줄여 5–10 스텝만.
처음 선형보간으로 돌아가면 이미 찾은 collective displacement field 를 버리므로 **더 나쁘다.**

Fmax 0.200 → 0.451 은 *경로가 아직 크게 움직인다*는 증거지 **다른 골짜기로 갔다는 증거가 아니다**
(Broyden overshoot · 최대잔여력 image 교체 · auto-CI 최고점 교체 · spacing kink · SCF force noise 전부 가능).
**장벽이 내려가면서 힘이 올라가는 것도 모순이 아니다 — NEB barrier 는 최적화 중 단조 목적함수가 아니다.**

진단할 값: 최고에너지 image 번호 · 최대잔여력 image 번호 · 이동 Li 의 hop-axis 진행도 ·
인접 image 의 PBC-unwrap 거리 · tangent 각도 · Nd collective-order amplitude · site occupancy · 최소 원자거리 · SCF residual · CI image 변경 이력.
경고: `max(d_i)/median(d_i) > 2` · tangent 회전 > 60° · Li 진행도 역행 · 새 site occupancy.
중단·분할: 90° 이상 kink 또는 새 stable basin.

## 5. N2 설계 — 목표를 먼저 정한다

| 목표 | 설계 | 우리 현 상태 |
|---|---|---|
| **A. dilute one-vacancy 장벽** | 공공 1개 유지 + 셀 확대. 2점=sensitivity, **3점부터** 제한적 scaling | 현 설계가 **이것** — 정당하다 |
| **B. 고정 유한농도** | 공공 수가 부피와 함께 증가. 공공–공공 상호작용은 **제거할 잡음이 아니라 물리의 일부** | 별도 factorial 필요 |

B 의 저비용 pilot (Li 자리 기준):

| 셀 | Li 자리 | 저농도 | 고농도 |
|---|---:|---:|---:|
| 2×2×4 | 48 | N_v=1, x=1/48 | N_v=2, x=1/24 |
| 2×4×4 | 96 | N_v=2, x=1/48 | N_v=4, x=1/24 |

가장 싼 방향성 검사는 `2×2×2(N_v=1)` vs `2×2×4(N_v=2)` — 둘 다 x=1/24.
⚠ 단 이건 **c 방향 반복길이만 늘린 shape-conditional 시험**이고 등방 수렴이 아니다.
각 다중공공 corner 에서 최대분리·중간분리·clustered 를 **최소한 구분**해야 한다.

⛔ 같은 셀에서 N_v=1 vs 2 로 잰 차이를 **보편적 농도 기울기로 보고 크기 차이에서 빼는 것은 반대**다
(선형성·topology 보존·size×concentration 상호작용 0 — 근거가 없다).

## 6. 재개할 경우 사전등록 (회신 원문)

- estimand: `E‡(3×3×3, one neutral Li vacancy, specified c→c endpoints, frozen-4f/PBE protocol)`
- 비교값: 2×2×2 CI `0.228981 eV`
- 동일사건 gate: 3.667 Å c→c · 공공 수·site identity 유지 · endpoint symmetry mapping · 중간에 다른 결함/상변형 없음
- 수치 gate: `Fmax ≤ 0.05 eV/Å` · endpoint force 합격 · path continuity·image spacing 합격 · 최고 image 및 topology 안정
- 실용 허용폭: `δ_E = k_B T* ln f` — rate factor 2 면 **≈18 meV @300 K · 36 meV @600 K**
- 결과 분류: ① 같은 topology·허용폭 이내 ② 같은 topology·허용폭 초과 ③ topology 변경/intermediate basin ④ 예산 내 미수렴
- ⛔ 두 점 extrapolation 금지 · 상·하한 문구 금지 · transient barrier 인용 금지 · 추가 iteration·wall-time 상한 고정

**안전 문구 (원문 그대로 쓸 것)**

> 한 neutral Li vacancy 를 둔 주기 Li₃Nd 모델에서 2×2×2→3×3×3 확장에 따른 동일 c→c 전이의
> 민감도를 시험했다. 이 대비에는 주기영상 간 거리와 허용 이완 부피의 변화가 함께 포함된다.
> 두 크기만으로 희박한계 수렴이나 독립적 농도 효과를 주장하지 않는다.

## 7. 회신의 검증 범위 (회신이 스스로 밝힌 것)

`origin/claude/friendly-meitner-lldvar@6c738e7` 의 08-17 KB 카드와 도구는 **직접 확인**했지만,
`neb_cc333_force_history_2026_08_27.json` 과 gabia 체크포인트는 그 origin 에 없어
**힘 이력과 실제 재시작 입력은 붙여넣은 표를 전제로** 판정했다.

⇒ 우리 쪽 확인 의무: gabia 의 실제 `neb.in` echo · 체크포인트 완전성. (4절 4번)

## 8. 열린 질문

- P0-1 이 "인공물" 로 나오면 **중점법이 되살아나고 3주가 필요 없어진다.** 그 경우 08-17 카드의
  결론 ①·§2 를 전면 재작성해야 한다.
- P0-2 (pristine soft mode) 가 양성이면 **끝점 정의 자체가 무효**다 — MD 로 옮겨도 해결 안 된다.
- dimer pilot 의 실제 운영비(환경 구축 포함)를 아직 안 재봤다.
- smearing 사다리 3점 × 끝점 2 + 안장 = 최소 9회 SCF. 언제 태울지 미정.
