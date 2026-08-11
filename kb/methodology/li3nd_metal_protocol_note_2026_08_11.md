---
title: "Li₃Nd 독자 계산 — 착수 전 프로토콜 점검 (금속 · frozen-4f)"
tags: [methodology/sei, methodology/nd, neb, metal, protocol]
date: 2026-08-11
status: 코드 반영 완료(dbec05fb) · **재리뷰 대기** · PP 블로커로 착수 대기
관련: kb/reviews/site_screen_codex_round3_request_2026_08_11.md · db/properties/li_nd_alloy_check.json
---

# 왜 이 문서가 먼저인가

Xu 2026 의 "Li–Nd alloy 계면상" 주장에 대해 **우리가 직접 Li₃Nd 를 계산**하기로 했다.
그런데 우리 SEI 파이프라인은 **넓은 갭 절연체 전용으로 설계돼 있어**, 그대로 돌리면
그럴듯한 숫자가 나오는데 전부 무의미하다. 착수 전에 세 곳을 고쳐야 한다.

대상: `mp-976264` Li₃Nd (Fm-3m) · hull **+0.197 eV/atom** · **theoretical=True**
(우리 P2 판정: Li–Nd 껍질 위 안정상 0개 — `db/properties/li_nd_alloy_check.json`)

---

## 0. 프레이밍 — 이 계산이 무엇을 말하는가

> **"설령 동역학적으로 생겼다 치더라도, 그 상이 계면에 도움이 되는가?"**

- 장벽이 낮으면 → 생기기만 하면 Li 전도엔 좋다. 하지만 열역학이 막는다.
  결론은 *"형성이 유일한 병목"*.
- 장벽이 높으면 → 생겨도 이온 전도에 도움이 안 된다. **이중 타격.**

⚠ **"Li₃Nd 장벽 = X eV" 를 단독으로 내면 우리 P2 판정과 모순된다.** 반드시 위 조건절과
hull 거리(+0.197 eV/atom · theoretical)를 같이 붙여 보고한다.

---

## 1. ⛔ 함정 A — fixed-occ 갭 단계가 금속에서 의미를 잃는다

`build_dft_inputs.py` 는 ③단계에서 `occupations='fixed'` + 조밀 k 로 VBM/CBM 고유값을
뽑아 갭을 낸다. 이게 우리 **갭 정본 규율**이다(DOS 문턱 판독 금지).

그런데 **금속에는 VBM/CBM 이 없다.** `occupations='fixed'` 는 `nbnd = nelec/2` 번째까지
채우므로, 금속에서도 "그 밴드와 다음 밴드의 차"라는 **숫자가 나온다**. `extract_gap.py` 가
`gap ≤ 0.02 eV` 를 "금속/반금속(겹침)" 으로 부르긴 하지만, 그건 사후 라벨이지
**계산을 막지 않는다**.

→ Li₃Nd 는 ③단계를 **돌리지 않거나**, 돌리더라도 결과를 `NOT_APPLICABLE(metal)` 로
   등재해야 한다. 숫자를 db 갭 표에 넣으면 안 된다.

## 2. ⛔ 함정 B — NEB 의 `tot_charge=+1` + jellium 이 금속에서 틀린다

`build_neb_inputs.py` 는 **Li⁺ 공공** 을 만든다:

```
tot_charge = 1.0        # Li+ 를 뺐으므로 전자도 하나 적다
occupations = 'smearing', degauss = 0.005
```

근거는 "중성 Li 를 빼면 넓은 갭 절연체의 원자가띠에 정공이 생겨 가짜 금속이 된다" 였다.
**금속에는 그 논리가 적용되지 않는다** — 금속은 공공을 만들어도 전자가 스스로 가려주고,
애초에 원자가띠 정공이라는 개념이 없다. jellium 보정은 인위적 상수를 더할 뿐이다.

게다가 `collect_neb.py` 에 이 차단이 있다:

> `tot_charge` 가 `"0"` 으로 시작하면 → *"중성 공공이라 원자가띠에 정공이 생긴다 —
> tot_charge=+1 로 다시 걸 것"*

**절연체엔 맞고 금속엔 정반대로 틀린 게이트다.** 그대로 두면 옳은 계산을 도구가 막는다.

→ 상별 `electronic_class`(metal / insulator) 를 두고 **차단 조건을 분기**해야 한다.
   금속: `tot_charge = 0`, 금속용 smearing(mv, degauss 크게), 차단 해제.

## 3. ⛔ 함정 C — Nd 4f (todo #27 과 같은 블로커)

Li₃Nd 는 Nd 를 포함하므로 **frozen-4f PP 확보가 선행**이다.
`build_neb_inputs.py` 에 이미 게이트를 넣어 뒀다 — `z_valence > 12` 면 입력을 만들지 않는다.

금속 환경에서 4f 를 원자가에 두면 E_F 에 평평한 f 다중항이 얹혀 SCF 가 안 붙거나,
붙어도 장벽이 4f 인공물에 지배된다. (2026-08-07 실측: Nd 3종 갭이 −0.021/−0.022/−0.028 로
7 meV 안에서 일치했고 E_F ±0.5 eV DOS 의 95–96% 가 Nd_f 였다.)

→ **LiNdO₂(#27)와 같은 PP 를 공유한다.** 하나 확보하면 둘 다 열린다.

---

## 4. 착수 순서 (코드 수정 후)

| 단계 | 내용 | 비용 | 선행 |
|---|---|---|---|
| ① | `mp-976264` 구조 회수 + provenance 등재 | 수 분 | MP_API_KEY (gabia) |
| ② | vc-relax | 수 시간 | **frozen-4f PP (#27)** |
| ③ | **DOS/PDOS 로 금속 여부 확인** — E_F 에 상태가 있나, Nd_f 지분은 얼마인가 | 수 시간 | ② |
| ④ | 금속용 NEB (중성 공공 · mv smearing) | 1–2일 | ③ 에서 금속 확인 |

**③ 이 분기점이다.** 금속으로 확인되면 ④ 를 금속 프로토콜로, 뜻밖에 갭이 열리면
기존 절연체 프로토콜로 간다. ③ 없이 ④ 를 걸면 어느 쪽이든 근거가 없다.

## 5. 코드 수정 목록 — ✅ **전건 반영 완료 (2026-08-11, dbec05fb)**

~~지금 손대지 않는다 — 리뷰 중이라 바꾸면 리뷰 대상이 어긋난다.~~
→ Codex 회신이 왔고 저자가 Li₃Nd 를 우선으로 요청해, NEB P0 4건과 **한 번에** 넣었다.

| # | 내용 | 상태 |
|---|---|---|
| 1 | 상별 `electronic_class` 레지스트리 — 단일 출처 JSON | ✅ `db/properties/sei_electronic_class.json` + `tools/sei/electronic_class.py` |
| 2 | `build_dft_inputs.py`: metal 이면 ③ 갭 단계 건너뜀 | ✅ 입력을 **아예 안 만들고** `03_GAP_NOT_APPLICABLE.json` 을 남긴다 |
| 3 | `build_neb_inputs.py`: metal 이면 `tot_charge=0` + 금속 smearing | ✅ `mv` · `degauss 0.02` · jellium 없음 |
| 4 | `collect_neb.py`: 전하 차단을 **insulator 에만** | ✅ metal 은 `tot_charge≠0` 을 오히려 차단 |
| 5 | `extract_gap.py`: metal 은 갭을 db 에 안 씀 | ✅ `NOT_APPLICABLE(metal)` 만 기록 |

★ 설계에서 **세 번째 class 를 추가**했다 (원 계획엔 metal/insulator 둘뿐이었다):

> `undetermined` — 우리 계산으로 아직 판정 불가. ⛔ **금속 선언이 아니다.**
> LiNdO₂·Nd₂O₃·Nd₂S₃ 가 여기 들어간다. 이들을 `metal` 로 분류했으면 NEB 이
> **틀린 전하로** 돌았을 것이다 — 4f-in-valence 의 갭 0 은 방법의 실패지 금속성이 아니다.

또 `evidence` 축을 뒀다 (`measured` / `declared` / `blocked`).
Li₃Nd 는 `metal · declared` 라서 **DOS 로 E_F 상태를 확인하기 전에는 NEB 이 안 열린다**
(§4 의 ③단계가 코드로 강제된다). 안 그러면 "금속이라 가정했더니 금속 답이 나왔다" 가 된다.

## 6. ⛔ 실제 블로커 확인 (2026-08-11 gabia)

```
/data/work/pseudo
  Nd.paw.z_14.atompaw.wentzcovitch.v1.2.upf   z = 14.0   4f-in-valence  ⛔
⛔ 전부 4f-in-valence 다 → 확보 경로 A/B/C 중 고른다
```

**코드가 다 준비돼도 PP 없이는 입력이 안 나온다.** `build_neb_inputs.py` 의
`z_valence > 12` 게이트가 Li₃Nd·LiNdO₂ 를 둘 다 막고 있다 (같은 PP 공유).

→ **Li₃Nd 의 임계 경로는 NEB 규약이 아니라 todo #27 (Nd frozen-4f PP) 이다.**
   `python3 tools/sei/nd_frozen4f.py --plan` 의 경로 A(기성품)/B(ld1.x)/C(VASP 외주).
   우리 것이 Topsakal–Wentzcovitch RE PAW 계열이므로 **같은 세트의 z≈11 짝이 있는지**를
   먼저 확인하는 게 A 의 첫 수다.
