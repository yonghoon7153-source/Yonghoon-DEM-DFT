---
title: "재리뷰 요청 — SEI NEB 6종 · Li₃Nd 금속 분기 · P2 범위 축소 (착수 직전)"
tags: [review/codex, sei/neb, nd, li3nd, protocol]
date: 2026-08-11
status: 회신 대기
대상 커밋: ba3362b8 · af2947ac · dbec05fb
선행 리뷰: Codex 착수전 검토 (NEB P0 4건 · Xu 2026 계산 검토)
---

# 무엇을 봐 달라는 것인가

지난 검토에서 세 건이 ⛔ HOLD 였다.

| 항목 | 지난 판정 | 지금 |
|---|---|---|
| NEB 6종 | ⛔ HOLD — P0 4건 | **전건 반영** (§1) |
| Li₃Nd | ⛔ HOLD — NEB 규약이 먼저 | **금속 분기 신설** (§2) |
| P2 verdict | ⛔ 인용 보류 — 역할 축소 | **DB 감사로 격하** (§3) |

**아직 아무것도 안 돌렸다.** relax·NEB 착수 직전이고, 이번 회신을 받고 건다.
그래서 이 요청의 초점은 "결과가 맞나" 가 아니라 **"돌리면 의미 있는 게 나오는 설계인가"** 다.

⚠ 리뷰어에게 미리 밝히는 편향: 아래 §2 의 금속 분기는 **저자가 Li₃Nd 를 우선으로
요청**해서 급히 만든 것이다. 급하게 만든 분기가 기존 절연체 경로를 조용히 망가뜨리지
않았는지를 특히 봐 주기 바란다.

---

## §1. NEB P0 4건 — 무엇을 어떻게 고쳤나

### P0-1 전하 부호 — **진단은 맞았고 처방이 반대였다**

QE 규약: `tot_charge = +1` → 전자 **부족**, `−1` → 전자 **추가**.
옛 코드는 "Li⁺ 를 뺐으니 전자도 하나 적다" 는 이유로 `+1` 을 썼는데, QE 는 Li **원자**를
지울 때 이미 `z_valence`(=3) 만큼 전자를 뺀다. 그래서 셀은 중성이고 이온 관점으로는
**정공 1개**(V_Li⁰)가 남는다. 거기에 `+1` 을 더 걸면 정공이 **2개**가 된다.

전자 수 검산 (Li₂S 216-전자 셀):

| | 전자 | 정공 |
|---|---|---|
| Li 원자 제거 후 (tot_charge 0) | 213 | 1 (V_Li⁰) |
| **옛 코드 (+1)** | **212** | **2** ⛔ |
| 의도한 V_Li⁻ (**−1**) | 214 | 0 ✔ |

→ `CHARGE = {"minus1": -1.0, "neutral": 0.0}`, 기본 `minus1`.
→ **기존 li2s 0.272 eV 는 정공 2개짜리 계산이라 provisional 로 내렸다.**

**봐 달라는 것**: `--vacancy_charge neutral`(V_Li⁰, 정공 1개)을 남겨 둔 게 맞나?
넓은 갭 절연체에서 정공 1개는 자기포획(self-trapped hole)을 만들 수 있어 장벽을
오염시킬 수 있는데, 그렇다면 파일럿에서 q=0 을 아예 빼는 게 나은가.

### P0-2 끝점 이완 — li3p Ea=0 의 미해결 절반

지금까지 **완전 벌크만** vc-relax 하고, Li 를 뺀 두 끝점은 **미이완**으로 NEB 에 넣었다.
미이완 끝점이 경로 최고점이 되면 NEB 은 끝점을 고정하므로 내리막만 남아
`max(E) − E_first = 0` 이 된다.

→ `build()` 가 `ep_initial/relax.in` · `ep_final/relax.in` 을 먼저 쓴다
   (고정셀 relax · **같은 q·k·PP·ecut** · `forc_conv_thr = 1.0d-3`).
→ 이완본이 있으면 좌표를 승계하고, 없으면 **`neb.in` 을 아예 안 만든다**
   (`--allow_unrelaxed_endpoints` 로만 강행 가능).
→ 러너에 `endpoints` 서브커맨드 추가.

**봐 달라는 것**: 끝점 이완을 **고정셀**로 한 것. 공공이 생기면 부피가 줄어드는 게
맞지만, NEB 은 first/last 가 같은 셀이어야 해서 vc-relax 를 못 쓴다. 이 타협이
장벽에 얼마나 들어가나 — 셀 완화를 별도로 재서 보정해야 하나?

### P0-3 버전 격리 — 새 meta 와 옛 에너지의 결합

같은 WORK 에 새 입력을 쓰면 러너가 옛 `neb.out` 의 `convergence achieved` 만 보고
건너뛴다. 그러면 **새 meta.json 과 옛 에너지가 결합**된다.
(기존 li2s 는 `min_cell 8.02` 인데 새 기본이 `--min_l 10` 이라 실제로 일어날 수 있었다.)

→ `protocol_hash()` = sha256(ecut·q·images·k·nat·cell·min_l·CI·endpoints_relaxed)[:12]
   를 meta.json 에 쓰고, 러너가 `.protocol_hash` 와 대조해 다르면 **재사용 거부**.

### P0-4 홉 쌍 대칭성 — Codex 가 잡은 false positive

옛 코드는 **구조 전체의 Li orbit 수**로 "끝점이 비등가" 를 판정했다. 그런데
Li₃P 의 최단 2.5116 Å 쌍은 실제로 **f–f 동등자리**이고 b–f 는 2.7406 Å 다.
전역 orbit 2종 ≠ 선택된 쌍이 비등가.

→ `orbit_map()` + `pick_hop(at, nat0, omap)` 이 **선택된 쌍 자체**의 orbit 을 기록
   (`pair_orbits`, `pair_equivalent`, `neighbor_shells`).
→ 회수기가 `endpoints_symmetry_equivalent` 로 대칭 게이트를 켜고 끈다.

**봐 달라는 것**: `neighbor_shells` 에 최단 쌍의 1.35배 이내 다른 shell 이 보이면
"전역 최단이 대표가 아닐 수 있다" 는 경고만 찍고 **막지는 않는다**. 이게 충분한가 —
대표 홉을 하나만 재는 설계 자체가 한계인데, 상별로 2~3개 홉을 재야 하나?

### CI 단계화

QE 공식 권고대로 `--ci_scheme` 기본을 **`no-CI`** 로 내리고, 수렴 후
`--ci_scheme auto --restart` 로 2단계를 돈다. (옛 기본 `auto` 는 처음부터 CI 를 켠 것.)
회수기가 `ci_scheme == "no-CI"` 인 결과에 "장벽 과소평가" 차단을 건다.

### 회수기 차단 목록 (신설·보강)

`Ea < 0.01` (경로 붕괴) · `Ea < 0` · 비등가 쌍인데 자리 에너지 차 0 ·
`endpoints_relaxed == False` · `ci_scheme == "no-CI"` · 전하 규약 위반(§2 분기).

---

## §2. Li₃Nd — 금속 분기 신설 (**이번 판의 핵심**)

### 왜 분기가 필요했나

우리 SEI 파이프라인은 **넓은 갭 절연체 전용**으로 설계돼 있다. 금속에 그대로 돌리면
세 곳이 **조용히** 틀린다 — 셋 다 "에러가 안 나고 숫자가 나온다" 는 게 문제다.

| 곳 | 절연체 논리 | 금속에서 왜 틀리나 |
|---|---|---|
| `build_dft_inputs.py` ③ | fixed-occ 로 VBM/CBM | **금속엔 VBM/CBM 이 없다.** 그래도 `nelec/2` 번째 밴드와 다음 밴드의 차라는 **숫자는 나온다** |
| `build_neb_inputs.py` | `tot_charge=−1` + jellium | 금속은 원자가띠 정공 개념이 없고 전도전자가 스스로 가려 준다. jellium 은 인위적 상수만 더한다 |
| `collect_neb.py` | `tot_charge=0` 은 옛 규약이라 차단 | 금속엔 **0 이 정답**이다 — 옳은 계산을 도구가 막는다 |

### 어떻게 고쳤나 — 단일 출처 레지스트리

`db/properties/sei_electronic_class.json` 하나에만 판정을 두고 네 도구가 전부 읽는다
(`tools/sei/electronic_class.py`).

```
class:    insulator | metal | undetermined
evidence: measured  | declared | blocked
```

| 상 | class | evidence | 근거 |
|---|---|---|---|
| li2o·li2s·licl·li3p·li3po4g | insulator | measured | 우리 fixed-occ 갭 (4.99 / 3.44 / 6.26 / 0.71 / 5.82 eV) |
| **li3nd** | **metal** | **declared** | Li–희토류 금속간화합물. Xu 2026 §2.6 의 "전자 전도성 계면상" 주장 자체가 금속 주장 |
| lindo2 · nd2o3 · nd2s3 | **undetermined** | blocked | Nd 4f-in-valence PP (z=14) |

**⛔ `undetermined` 는 금속 선언이 아니다.** Nd 3종의 갭 0 은 **방법의 실패**지
금속성이 아니다 (화학이 전혀 다른 세 상이 −0.021/−0.022/−0.028 로 7 meV 안에서
일치했고 E_F ±0.5 eV DOS 의 95–96 % 가 Nd_f). LiNdO₂ 를 `metal` 로 분류하면
NEB 이 틀린 전하로 돈다 — 그래서 세 번째 class 를 뒀다.

**미등록 상은 절연체로 가정하지 않고 막는다** (`unregistered` → blocked).

### 분기 내용

- **metal**: `tot_charge = 0` · smearing `mv` · `degauss = 0.02` · jellium 없음
- **insulator**: `tot_charge = −1` · `gaussian` · `degauss = 0.005` (기존 그대로)
- `build_dft_inputs.py`: metal 이면 `03_nscf_gap.in` 을 **만들지 않고**
  `03_GAP_NOT_APPLICABLE.json` 에 사유를 남긴다 (사후 라벨로는 못 막으므로 입력 단계에서)
- `extract_gap.py`: metal 선언 상은 `NOT_APPLICABLE(metal)` 만 쓰고 갭 값을 db 에 안 넣는다
- `collect_neb.py`: `metal` + `evidence=declared` 면 "DOS 확인 전 인용 금지" 차단

### ⚠ 착수 순서 — ③이 분기점이다

| 단계 | 내용 | 선행 |
|---|---|---|
| ① | mp-976264 구조 회수 + provenance | MP_API_KEY |
| ② | vc-relax | **Nd frozen-4f PP (todo #27)** |
| ③ | **DOS/PDOS 로 금속 확인** — E_F 에 상태가 있나, Nd_f 지분은? | ② |
| ④ | 금속용 NEB | ③ 에서 금속 확인 |

`evidence: declared` 가 ③ 없이 ④ 로 못 가게 막는다 — 안 그러면
**"금속이라 가정했더니 금속 답이 나왔다"** 가 된다.

### ⛔ 현재 블로커 — Nd frozen-4f PP

2026-08-11 gabia 인벤토리 결과:
```
/data/work/pseudo
  Nd.paw.z_14.atompaw.wentzcovitch.v1.2.upf   z = 14.0   4f-in-valence  ⛔
⛔ 전부 4f-in-valence 다
```
`build_neb_inputs.py` 가 `z_valence > 12` 면 입력을 안 만든다 → **Li₃Nd·LiNdO₂ 둘 다 막혀 있다.**
(같은 PP 를 공유하므로 하나 확보하면 둘 다 열린다.)

**봐 달라는 것 (§2 에서 가장 중요)**:

1. **Li₃Nd 를 `metal` 로 선언한 근거가 충분한가?** 지금 근거는 조성 논거뿐이다
   (Li·Nd 둘 다 금속 · 전기음성도 차 작음 · Xu 의 주장 자체가 금속 주장).
   `declared` → `measured` 승격 조건을 "DOS 에 E_F 상태 존재" 로 잡았는데,
   Nd 4f 가 core 로 가면 E_F 근처가 Li-s/Nd-d 가 되므로 그 판정이 깨끗할 것 같다.
   이 논리에 구멍이 있나?

2. **금속 공공에 `tot_charge = 0` 이 맞나?** 금속에서는 하전 결함이라는 개념 자체가
   스크리닝되어 사라진다고 보는데, 유한 셀에서는 완전히 스크리닝되지 않을 수 있다.
   셀 크기(현재 `--min_l 10`)로 충분한가?

3. **`mv` smearing + `degauss 0.02 Ry`** 가 Li₃Nd(Fm-3m, 금속)에 적절한가.
   NEB 은 이미지마다 SCF 라 degauss 가 크면 장벽에 계통 오차가 들어갈 수 있다.

4. **frozen-4f PP 확보 경로**. 지금 계획은 A(기성품 탐색) → B(ld1.x 제작) → C(VASP 외주).
   우리가 쓰는 게 `Nd.paw.z_14.atompaw.wentzcovitch` 인데, Topsakal–Wentzcovitch
   RE PAW 세트(Comput. Mater. Sci. 95, 263 (2014))에 **z≈11 짝**이 있는지 아나?
   있으면 A 로 반나절에 끝난다.

---

## §3. P2 verdict — 역할 축소

### 무엇이 과했나

초판은 `li_nd_alloy_check.py` 를 "Li–Nd alloy 형성 여부 판정" 으로 썼다. 두 가지가 틀렸다:

1. 6원계 "interface" 계산이 그냥 **closed convex hull** 이었다 — Li 를 open reservoir 로
   두지도, μ_Li = Li metal 을 적용하지도 않았다. **0 V 계면 계산이 아니다.**
2. `ALLOY_EXISTS` / `NO_STABLE_ALLOY` 라는 이름이 고용체·비정질·준안정 나노상까지
   포함하는 것처럼 읽힌다.

### 어떻게 고쳤나

- 6원계 hull 블록 **삭제**. 도구는 이제 **"선택한 MP release 의 0 K hull 에 stable
  ordered Li–Nd 결정상이 등록돼 있는가"** 만 답한다.
- 판정 이름: `STABLE_ORDERED_LI_ND_PHASE_IN_MP` / `NO_STABLE_ORDERED_LI_ND_PHASE_IN_MP`
  / `QUERY_INCONCLUSIVE`
- 양성 대조를 **Li–Al / Li–Si 로 한정** (Li–La/Ce/Mg 는 과학 비교군이지 대조군이 아니다 —
  없어도 정상일 수 있으므로 대조로 쓰면 안 된다).
- provenance 기록: MP db version · thermo type 고정 · 패키지 버전 · UTC.
- **0 V 계면 산물 주장은 이 도구가 아니라 기존 open-Li 결과를 인용**하도록 문서에 박았다:
  `tools/oxidation/anode_interface_stability.py` · `db/properties/oxidation_stability.json`.
  그쪽 0 V 예측 산물은 Li₂O + Li₃P + Li₂S + **NdP** + LiCl — Li–Nd 금속간화합물이 아니라 **NdP** 다.

### 실측 (참고)

Li–Nd: 안정 ordered 상 **0개**. 가장 가까운 준안정상 mp-976264 Li₃Nd hull **+0.197 eV/atom**,
`theoretical=True`. Li–La·Li–Ce 도 0개 (계통적). 양성 대조 정상.

**봐 달라는 것**: Xu 2026 §2.6 반박에서 **주 근거를 open-Li 결과(NdP 예측)로 두고
이 DB 감사를 보조로 두는 구성**이 맞나. 그리고 Li₃Nd 를 직접 계산하기로 한 것과
"Li–Nd 는 열역학적으로 안 생긴다" 는 판정이 **논문 안에서 모순으로 읽히지 않게** 하는
프레이밍 — 지금은 이렇게 잡았다:

> "설령 동역학적으로 생겼다 치더라도, 그 상이 계면에 도움이 되는가?"
> · 장벽이 낮으면 → 생기기만 하면 좋다. 하지만 열역학이 막는다 → **형성이 유일한 병목**
> · 장벽이 높으면 → 생겨도 도움이 안 된다 → **이중 타격**

⚠ 어느 쪽이든 **"Li₃Nd 장벽 = X eV" 를 단독으로 내면 안 된다** — 반드시 위 조건절과
hull 거리(+0.197 eV/atom · theoretical)를 같이 붙인다. 이게 충분한 안전장치인가?

---

## §4. 착수 전 남은 판단 (리뷰어 의견 요청)

1. **파일럿 순서**. 지금 계획은 `li2s` 를 q=−1 로 다시 걸어 옛 +1 값(0.272 eV)과
   비교하는 것부터다. 6종을 한 번에 걸지 않고 **가장 싼 계 하나로 규약 변화의 크기를
   먼저 재는 것**이 맞나?

2. **li3p (todo #25)**. Ea=0 의 절반은 끝점 미이완으로 설명됐다(P0-2). 나머지 절반
   (경로 붕괴 자체)은 끝점 이완 후 다시 봐야 아는데, **이완만으로 해결됐다고 가정하지
   않고** 이미지별 최대 변위를 회수기가 검사하게 해야 하나?

3. **li3po4g (todo #26)**. 127원자 × 이미지 7 이 제일 비싸다. `--images 5` 로 내리자는
   기존 계획이 있는데, 이미지를 줄이면 CI 가 안장점을 놓칠 위험이 커진다.
   no-CI → CI 2단계로 가면 이미지 5 로도 되나?

4. **비용 총량**. 6종 × (끝점 relax 2 + no-CI + CI) 는 갭 계산의 100 배 급이다.
   협업자 요청(#43)이 6종 전부인데, **어디까지가 현실적인 약속**인가?
   (li2s·li2o·licl 은 작고, li3p 63원자, li3po4g 127원자, lindo2 는 PP 대기.)

---

## 부록 — 변경 파일

| 파일 | 변경 |
|---|---|
| `db/properties/sei_electronic_class.json` | **신규** — 금속/절연체 단일 출처 |
| `tools/sei/electronic_class.py` | **신규** — 로더 + `blocked_reason()` |
| `tools/sei/build_neb_inputs.py` | 전하 부호 · 끝점 relax · protocol_hash · 쌍 대칭성 · CI 단계 · 금속 분기 · li3nd 타깃 |
| `tools/sei/collect_neb.py` | 차단 6종 추가 · 전하 게이트를 class 로 분기 |
| `tools/sei/run_sei_neb.sh` | `endpoints` 서브커맨드 · protocol_hash 대조 |
| `tools/sei/build_dft_inputs.py` | metal → 갭 단계 미생성 + 사유 JSON |
| `tools/sei/extract_gap.py` | metal → `NOT_APPLICABLE(metal)` |
| `tools/sei/li_nd_alloy_check.py` | 역할 축소 (DB 감사) |
| `kb/methodology/li3nd_metal_protocol_note_2026_08_11.md` | 금속 함정 3종 문서 |
