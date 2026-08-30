---
title: "회신 AJ — C-12 구현 완료 + 선언된 이탈 하나(clean slab) + 발송 승인 요청"
date: 2026-08-30
kind: review_request
status: sent
tags: [sdcp, c12, dft, review, vacuum, potcar, deviation, go-nogo]
---

# 회신 AJ

**검토 기준: `origin/claude/friendly-meitner-lldvar@c60954e79cdd38d55475f7bcc49514d1a8636f36`**
(`--selftest` **403** · `convention_check` 0 위반 · `kb_wiki lint` 0 errors)

회신 AI 의 **C** 를 구현했다. 묻는 것은 셋이다.

① 실행 전 유일한 코드 수정(POTCAR 신원 결속)이 **닫혔는가**
② **선언된 이탈 둘** — clean slab 복원 · 기체 기준 6잡 — 를 승인하는가
③ 용어 정정 둘이 타당한가

---

## 1. ① POTCAR·VASP 신원 — 지적대로 고쳤다

지적이 정확했다: *"`expected_variants`와 `titel_lines`가 같은 회신 JSON에서 오므로
자기일관적인 허위 기록이 통과한다."*

- **대조 기준을 우리 쪽으로**: TITEL 을 회신의 `expected_variants` 가 아니라
  **manifest 의 `potcar_spec`** 과 대조한다. 우리 규격이 없으면
  `POTCAR_SPEC_UNAVAILABLE` 로 **막는다** (조용히 통과 금지).
- **묶음 전체 신원** `potcar_identity_gates()` — 잡 하나씩으로는 못 잡는 것:
  원소별 원본 sha 가 잡마다 다르면 `POTCAR_SOURCE_SPLIT`, VASP 세대가 갈리면
  `VASP_VERSION_SPLIT`. 각 잡이 자기일관적이어도 **에너지를 뺄 수 없다**.
- **외부 기준** `--potcar_pin <json>` — 사전 승인된
  `{source_sha256:{원소:sha}, vasp_version}` 을 manifest 에 박고 `PIN_MISMATCH` 로 대조.

음성 시험 다섯: 자기일관적 허위(Li/Ni 로 통일) · 우리 규격 부재 · PAW 원본 갈림 ·
VASP 세대 갈림 · 사전 고정값 불일치.

⚠ **아직 못 하는 것**: 우리가 POTCAR 원본을 갖고 있지 않아 `source_sha256` 이 진짜 그
배포판인지 확인 못 한다. 그래서 `--potcar_pin` 을 **누가 채우는가**가 남는다.
**묻는 것**: 외주처가 조립기를 한 번 돌려 SHA 를 보내면 그것을 pin 에 박고 재발행하는
2단 handshake 가 맞는가? 아니면 다른 방법이 있는가?

---

## 2. ★ ② 선언된 이탈 — clean slab 을 되살렸다 (12 → 15잡)

C 는 *"clean slab 은 대비에서 소거되므로 계산하지 않으며, 개별 절대 흡착에너지도
보고하지 않는다"* 였다. **이탈한다.** 이유 둘이고, 둘째가 더 중요하다.

**(1) 절대값** — C 대로면 두 모델의 *차이* 하나만 나온다. 문헌은 절대값을 싣고
(`han2025` 등), Table S1·Figure 2e 가 다른 논문과 비교되려면 절대값이 있어야 한다.

**(2) 자기 상태의 기준 — 이게 결정적이다.** clean slab 은 모멘트 붕괴 판정의
**분모**다 (`Q/Q_clean` · `f_small`). 없으면 분석기의 `q_ref` 가 `None` 이 되어
**전 잡이 '판정 보류' 로 조용히 통과**한다. 즉 C 가 **유지하라고 한 여섯 검사 중
'실현된 Ni 자기 topology' 가 fail-open 이 된다.**

⇒ 이것은 통제를 **더하는** 이탈이지 빼는 이탈이 아니다.

| 추가 | 잡 | 왜 |
|---|---:|---|
| clean slab @ c1, 두 seed | 2 | 절대 E_ads 기준계 + 자기 대조군 |
| clean slab @ c2, 주 seed | 1 | 절대값을 보고한다면 **절대값의 진공 수렴**도 봐야 한다 (대비는 슬랩이 소거돼 무관) |

**묻는 것**: 이 이탈을 승인하는가? 승인하지 않으면 (2)의 fail-open 을 무엇으로 막나?

---

## 3. ③ 용어 정정 둘

**(a) `canary` → `vacuum-thickness convergence test`.** '카나리' 는 소프트웨어 배포
용어이고 이 분야 문헌 표현이 아니다. VASP 튜토리얼도 *"converge the vacuum thickness"*
로 쓴다. 잡 접두사도 `canary/` → `vacconv/`.

**(b) 양의 이름 — 제안하신 9단어를 쓰지 않는다.**
`reference-state-dependent fixed-geometry adsorption electronic-energy contrast` 는
우리 litdb **202편에 0회**다. 실측:

| 표현 | 등장 |
|---|---:|
| binding energy | 37 |
| adsorption energy | 16 |
| interaction / adhesion energy | 3 / 3 |
| 제안된 9단어 | **0** |

그리고 같은 계 논문 `han2025_icep_binder_ultrahigh_loading_ncm811`(바인더/NCM811 표면
DFT)은 **'결합에너지' 15회 · Binding energy 3회**로 쓴다. 문헌 관례는 **이름을
평범하게 쓰고 단서를 Methods 에 적는 것**이지 이름을 새로 만드는 것이 아니다.

⇒ **`adsorption energy`** 로 간다. `adsorption` 을 고른 이유는 우리 값에 **변형에너지가
포함**돼 있고 그것이 adsorption energy 의 **표준 정의**이기 때문이다. `binding energy`
는 ⓐ부호규약이 논문마다 반대 ⓑ**XPS 내각준위와 충돌**(이 원고에 분광 근거가 있다)
ⓒ변형 제외 상호작용에너지 로도 쓰여 모호하다.

본문 문장은 이렇게 된다:
> *"The adsorption energy of the SDCP repeat-unit model was [X] eV lower than that of the
> perfluorodecane model, evaluated as static single points on machine-learned geometries
> within a matched magnetic branch."*

**묻는 것**: 이 두 정정에 동의하는가?

---

## 4. 자세 동결 (DFT 0잡 시점 · MLIP 출처만)

`db/properties/c12_poses_2026_08_30.json` (freeze `0ac106d152b96458`)

| 조각 | primary | sensitivity | ΔE_pose | 규칙 |
|---|---|---|---|---|
| sdcp_neutral | `b00` H–O 1.83 Å | `b12` **O–Li 2.41 Å** | +0.278 eV | 앵커 원소 다름 |
| ptfe_c10 | `b00` F–Ni 2.54 Å | `b52` F–O 2.68 Å | +0.106 eV | Jaccard 최대 |

**선정 규칙** — ① 분자쪽 **앵커 원소**가 primary 와 다른 basin 중 `E_pose` 최저,
② 그런 basin 이 없으면 접촉집합 Jaccard 거리 최대 중 최저. 동률은 `(E_pose, basin_id)` 로.

⚠ **에너지 창을 쓰지 않았다.** 창(`W0=0.15 eV`) 안에서는 sdcp 후보 7개가 **전부 산성
H 앵커**라 sensitivity 가 primary 와 같은 모티프가 되어(Jaccard 0.333) 방향 재현을
시험하지 못한다. 창을 **없애는** 쪽이라 새 문턱을 만든 것이 아니다.
ptfe 는 과불화라 앵커 원소가 다른 basin 이 **하나도 없어** ②로 떨어진다.

**묻는 것**: 이 규칙과 그 결과가 "접촉형이 가장 다른 자세" 의 의도에 맞는가?

---

## 5. 발송 구성 (19잡 — 이탈 둘 포함)

| | 잡 | 비고 |
|---|---:|---|
| 복합체 2조각 × 2자세 × 2 seed @ c1 | 8 | |
| primary @ c2 (진공 수렴) | 2 | |
| clean slab @ c1 ×2 seed, @ c2 ×1 | **3** | **이탈 §2** |
| 기체 기준 (조각당 box20 · box24 · box24_nzmag) | **6** | **이탈 §5-b** — 원안은 2 |
| | **19** | |

### 5-b. 선언된 이탈 둘째 — 기체 기준이 2잡이 아니라 6잡이다

C 는 "기체 기준 2잡" 이라고 적었는데, 생성기가 실제로 내는 것은 조각당 셋이다:

| 추가 | 무엇을 보나 |
|---|---|
| `box20` (정본 `box24` 와 짝) | 기체 기준의 **상자 크기 수렴** — 값이 상자에 안 매였음을 보이는 대조군 |
| `box24__nzmag` | 기체 분자의 **자기 시작상태 대조** — 0 에서 시작한 것과 0 이 아닌 데서 시작한 것이 같은 곳으로 가는가. **wave1 을 물린 바로 그 축**이다(제약된 기준에서 자유로운 복합체를 뺐다) |

기체 분자 단일점이라 잡당 분 단위 — 계산 비용은 사실상 0 이고, 늘어나는 것은 **검토
면적뿐**이다. 둘 다 통제를 **더하는** 쪽이라 그대로 두었다.

**묻는 것**: 이 넷을 그대로 두는가, 아니면 `box24` 둘만 남기는가? 남긴다면 nzmag 없이
기준계 스핀 비대칭을 무엇으로 막나?

- `c1 = 36.6551 Å` · `c2 = 40.6551 Å` · 최소 주기영상 분리 ≥ 15 Å (게이트가 강제)
- D3-on 고정기하 static 만. D3-off 없음. dense 없음
- 비용은 `unknown` 으로 둔다 — 인용하지 않는다 (지적 수용)

**진공 수렴 판정** — 두 조각의 **대비 변화**에 적용한다:
`|D(c2) − D(c1)| ≤ 0.005 eV` **이고** 두 값의 0.01 eV 반올림이 같아야 통과.
5 meV 의 출처는 물리 상수가 아니라 **보고 최소단위(0.01 eV)의 절반**이다.
실패하면 추가 셀 탐색 없이 **Figure 2e 를 제거**한다.

**미해결로 끝내는 조건**: 같은 자기 topology 에서 primary·sensitivity 가 **같은 우열을
주지 않거나**, 최종 대비 `|D| < 0.05 eV`. 그러면 계산을 확장하지 않고 패널을 뺀다.

---

---

## 7. 실물 생성 결과 (gabia, 2026-08-30)

번들을 실제로 만들었다. 아래는 **실측**이다.

| | 값 |
|---|---|
| `candidate_set` | `c12 (frozen 0ac106d152b96458)` |
| 잡 / VASP 실행 | **19 / 19** (dense 없음) |
| 배포 파일 · 해시확인 | 119 / 119 |
| `clean_slab` sha256 | `d5f18feb15701f3fc932a1c8f64a09ed48c39ca270d8d8a8f5339658b6c43676` |
| 입력 preflight | **0건** (job.json 19개) |
| `potcar_pin` | **미고정** — §1 의 질문 |

**발송 후보 정체 (`sdcp_c12_v3`)**

| | |
|---|---|
| ZIP sha256 | `9476938f1b6500a18bb9e84c2336d5d0ed57c7f126ec4bb58265445d93bbad1b` (309,777 B) |
| MANIFEST sha256 | `bae583208868f1e426d41fe9c3882370e4d2889bc78a9075da35bdd003d3f07f` |
| generated_utc | `2026-08-30T12:58:24Z` |
| 자세 동결 | `db/properties/c12_poses_2026_08_30.json` (`0ac106d152b96458`) |

⚠ ZIP 은 **도구가 만든 것 하나**다 — verify 보고값과 `sha256sum` 이 일치한다
(§7-2 의 덧쓰기 사고는 v3 에서 해소).

**진공** — c 30.2609 → **36.6551 Å**, 최소 주기영상 분리 **15.38 → 21.773 Å**.
DIPOL 14곳 · `job.json` 13곳 되scale (슬랩 13잡 + clean slab 의 두 번째 INCAR 1).

**진공 두께 수렴 시험** — c2 = 40.6551 Å, 3잡:

| 잡 | 분리 |
|---|---|
| `vacconv/ptfe_c10__b00__afm2424_pm1__c2` | 28.138 Å |
| `vacconv/sdcp_neutral__b00__afm2424_pm1__c2` | 26.972 Å |
| `vacconv/clean_slab__afm2424_pm1__c2` | **정의되지 않음** (흡착종 없음) |

### ⚠ 7-1. 스스로 보고하는 것 — C-12 자세는 애초에 진공 문제가 없었다

원래 8.63 Å 이던 자세는 `b74`·`b75`(calibration) · `b71`·`b79`(holdout) 인데
**넷 다 C-12 집합에 없다.** C-12 의 네 자세(b00·b12 / b00·b52)는 `c = 30.2609 Å`
에서 이미 최소 **15.38 Å** 이다.

⇒ `c1 = 36.6551 Å` 은 **교정이 아니라 여유**이고, 수렴 시험은 *"36.66 에서 수렴했나"*
를 묻는 것이지 *"30.26 이 부족했나"* 를 묻는 것이 아니다. 그 구분을 원고에도 적는다.

**묻는 것**: 이 구간(21.8 → 27.0 Å)에서의 시험이 목적에 맞는가, 아니면 `c1` 을
더 낮춰(예: 원래 30.26) 실제 민감도가 보이는 구간에서 재는 것이 맞는가?

### ⚠ 7-2. 이번 라운드에 내가 만든 결함 하나

`zip` 이 그 기계에 없어 파이썬 압축을 덧붙이라고 지시했는데, **도구가 이미 zip 을
만든다.** 덧쓰기가 일어나 ZIP sha 가 둘이 됐다(도구 `e4e6065f…` / 덧쓴 것 `859df099…`).
발송본은 **도구가 만든 zip 하나**로 재생성해 sha 를 하나로 맞춘다.


## 6. 판정 형식

- ① **닫힘 / 안 닫힘** + `--potcar_pin` 을 누가 채우는가
- ② clean slab 복원 **승인 / 불승인** (불승인이면 자기 fail-open 대책)
- ③ 용어 두 정정 **동의 / 반대**
- ④ 자세 선정 규칙 **타당 / 수정**
- ⑤ 기체 기준 6잡 **유지 / 2잡으로 축소**
- ⑥ §7-1 — 수렴 시험 구간이 맞는가 (`c1` 을 낮춰야 하는가)
- **19잡 발송 GO / NO-GO**

과잉이면 과잉이라고 적어 달라. 이번에도 안심시키지 말아 달라.
