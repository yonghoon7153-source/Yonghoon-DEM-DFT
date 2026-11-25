---
title: "리뷰 요청 BG — AW(웹앱 NO-GO) 해제 판정 + 그날 새로 만든 판정 셋"
date: 2026-09-07
updated: 2026-09-07
tags: [review, codex, prompt, webapp, governance, lpsocl, y-site, oxidation]
status: 작성 — 발송 대기
kind: review-prompt
system: repo
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 요청 BG

> 앞 회신: `codex_AW_reply_webapp_audit_2026_09_01.md` (**NO-GO** · P0 4 · P1 6 · 해제조건 6)
> 대상 브랜치: `claude/friendly-meitner-lldvar`
> 이 요청은 **둘**입니다 — §A 해제 판정, §B 그날 새로 만든 판정 셋의 사전 검토.

---

## 0. 먼저 자백할 것 — 이 요청의 제일 약한 고리

AW 의 **이행 기록이 오래 `⏳` 로 멈춰 있었습니다.** 그런데 코드로 대조해 보니
**문서가 낡은 것**이었고 P0 넷은 이미 이행돼 있었습니다. 즉 그동안 우리는
**"안 한 것"과 "기록을 안 한 것"을 구분하지 못한 채** NO-GO 를 들고 있었습니다.

⇒ **§A 의 ①–④ 는 우리 자체 grep 대조입니다.** 리뷰어가 확인해 주셔야 할 것은
"고쳤다는 말이 맞나" 이고, 특히 **우리가 "됐다" 고 잘못 본 것이 있는지**입니다.
자체 대조로 해제하는 것은 AW 가 지적한 방법론적 실패(*"실화면 대조를 하지 않았다"*)를
문서 층에서 반복하는 것이라, 그 판정을 우리가 하지 않겠습니다.

---

## A. AW 해제조건 6건 — 이행 주장과 근거

| # | 해제조건 | 우리 주장 | 근거 |
|---|---|---|---|
| ① | `/sdcp` 를 citable·closure·hazard 에서 **파생** | ✅ | `data.py` `_wave1_gate`·`_wave1_status`. 추가로 **basin 불일치 우선순위** 정정(⚠ 아래) · 결과 원장 fail-closed |
| ② | 5표면 철회 결속 | ✅ | `test_retracted_canonical_values_are_bound_on_every_surface` — `/`·`/todo`·`/log`·`/compare`·`/glossary`·`/sdcp`·`/methods` **7표면**, 레지스트리 구동, ±140자 창 |
| ③ | C-12 → 전역 closure-policy 간선 제거 | ✅ | `D-2026-08-30-sdcp-c12-path` 의 `supersedes` 는 `ddE_obs` **하나**뿐. 전역 `D-2026-08-28-closure-criteria-first` 는 **active** |
| ④ | 상태 enum/중복 ID/중복 canonical fail-closed | ✅ | `canonical._by_id` · `index()` 충돌 표시 · `validate_canonical.py` 음성시험 7건 |
| ⑤ | 파생 fit 출처 + signed-drift/base-T 음성시험 | ✅ **2026-09-07** | 아래 §A-5 |
| ⑥ | hazard 전행 + **동적 라우트 fixture** | ⚠ **절반** | 동적 라우트는 했고(§A-6), **hazard 전행·전필드 대조는 안 했습니다** |

### A-1 ①에 딸린 실물 하나 (자진 신고)

`sdcp_wave1_rows()` 가 basin 이 갈린 쌍에도 **조각 수준 사유**를 남겨서,
`sdcp_neutral/net4` 가 **−40.7 meV** 를 보이면서 사유는 *"판정바닥 30 meV 아래"* 였습니다.
**40.7 > 30 이라 화면이 거짓말을 한 것**입니다. basin 불일치를 판정바닥보다 **앞**에 두고,
그 행은 *"부호도 못 읽는다"* 로 바꿨습니다.

### A-5 ⑤ 상세 — 두 개가 진짜로 안 돼 있었습니다

`tools/ionic/committee_sweep_verdict.py`

1. **부호 있는 max.** `drift = max((rel[T]/rel[bT]-1)*100 ...)` 였습니다.
   `(−30 %, −5 %)` 가 오면 **−5 %** 가 뽑혀 `abs(drift) < 10` 을 통과합니다 —
   **30 % 표류가 "열적 스케일링" 초록으로 나갑니다.** `max(..., key=abs)` 로 고쳤고,
   상단 문턱도 `drift > 25` → `abs(drift) > 25` 로 맞췄습니다(음의 큰 표류가 그 갈래를
   못 탔습니다). **부호는 화면·JSON 에 남깁니다** — 방향은 진단 정보라서요.
2. **기준 온도 조용한 대체.** `bT = a.base_T if a.base_T in rows else sorted(rows)[0]`.
   *"600 K 대비 표류"* 라고 찍힌 숫자가 실은 800 K 대비인데 **어디에도 안 남았습니다.**
   대체를 중단하고 멈춥니다. 다른 기준은 `--base_T` 로 **선언**합니다.
3. 판정 조각을 순수 함수로 빼고 `--selftest` 를 신설했습니다(10건, 음성 4건 —
   `(−30,−5)` 선택 · 음의 30 % 검출 · 잔차 문턱 · 부호 혼합).

⚠ **문턱 값(10 / 25 / 잔차 10 %)은 종전 그대로**입니다. 이번 변경은 **부호 처리만**입니다.

### A-6 ⑥ 상세 — 동적 라우트는 닫았고, hazard 는 안 닫았습니다

라우트 시험이 `"<" not in r.rule` 로 **동적 라우트 14개를 통째로** 빼고 있었습니다
(AW: *"GET 42개 패턴 중 14개가 빠진다"*). fixture 11 + EXEMPT 3(사유 명시)으로 덮고,
**새 동적 라우트가 fixture·EXEMPT 없이 생기면 그 사실로 실패**하게 했습니다.
**404 를 통과로 세지 않습니다** — 라우트는 밟았어도 렌더 경로를 안 탄 것이라서요.

⛔ **hazard 전행·전필드 대조는 못 했습니다.** AW 가 *"헤더의 25건만 확인해 tbody 가
0행이어도 통과한다"* 고 지적한 그 시험이 **그대로**입니다.

---

## B. 그날 새로 만든 판정 셋 — 결과를 보기 전에 봐 주십시오

### B-1 ⚠ Y 자리 선호 — 우리가 **논문과 반대 부호**를 냈습니다

`db/properties/y_site_preference_dft_2026_09_07.json`

QE 두 슈퍼셀의 조성이 다릅니다(100 vs 108원자, 차이 `+10 Li, −2 P`). 그 조성차가
5상 기저 중 둘로 **정확히 닫혀서**(`+10 Li − 2 P = −2 Li₃PS₄ + 8 Li₂S`) 화학퍼텐셜로
균형을 잡았습니다:

```
ΔG = [E(P_4b) − E(Li_24g)] − [−2 E(Li₃PS₄) + 8 E(Li₂S)] = +3.756 eV
   → Y 하나당 +1.878 eV,  Li 자리 유리
   → 뒤집는 데 필요한 μ_Li 이동 = 0.376 eV
```

UMA antisite 스크린(+0.47~+2.51 eV/dopant, Li)과 **같은 부호**이고 QE 값이 그 범위에
듭니다. Wang 2025(Angew, Fig S3)의 **Y@4b** 와는 반대입니다.

**여쭙는 것**
- **Q1.** 저장소를 `Li₃PS₄/Li₂S` 평형으로 고른 것이 이 계에서 **정당한 한 점**입니까?
  다른 자연스러운 선택(Li 금속 · Li₂S 단독 · P 원소)에서 부호가 유지됩니까?
  우리는 μ 민감도(0.376 eV)만 냈지 **다른 저장소를 실제로 계산하지 않았습니다.**
- **Q2.** 두 셀의 조성차를 5상 기저로 닫은 것이 **유일한 분해**입니까? 다른 조합이
  가능하면 값이 달라집니다 — 우리는 Y·Cl·O 를 0으로 강제하니 자동으로 닫혔다고 봤습니다.
- **Q3.** 우리 카드가 *"논문의 두 모델은 같은 조성이라 기준항이 상쇄된다"* 고 적었는데,
  Fig S3 캡션대로면 (a)Y→P·O→S 와 (b)Y→Li·O→S 는 **조성이 다릅니다.** 그러면 고립원자
  기준항이 안 상쇄되고 결과가 기준 선택에 끌려갑니다. **이 지적이 맞습니까?**
  (SI 실제 셀 조성은 아직 확인 못 했습니다 — 단정하지 않고 예고만 달아 뒀습니다.)

### B-2 LPSOCl 닫힘 조건 — **C3 판정식을 우리가 처음 만들었습니다**

`db/properties/lpsocl_box331_closure_conditions_2026_09_07.json` (proposed)

400 ps 9런 중 3런만 끝난 시점, 아레니우스를 한 번도 그리기 전에 커밋했습니다.
C1(궤적 무결성)·C2(4창 plateau ≤10 %·홉 ≥3.0)·C4(시드 지배)는 기존 사전등록에서 **승계**한
것이고 문턱도 그대로입니다. **C3 만 새로 만들었습니다.**

- **Q4.** 구간 Ea(600–800) 와 Ea(800–1000) 의 **"양립"** 을 **시드 bootstrap 1σ 겹침**으로
  정의하려 합니다. 1σ 가 맞습니까, 2σ 입니까? 참고 눈금으로 b2o3 는 두 구간이
  **145 meV** 벌어져 철회됐습니다. 느슨하게 잡으면 그 145 meV 도 "양립" 이 됩니다.
- **Q5.** HOLD(정밀도 부족)가 나왔을 때 **A: 그대로 보고하고 닫는다** / **B: 미리 정한
  한 번의 확장만** 중 어느 쪽이 맞습니까? 우리는 A 를 권합니다 — b2o3 는 굽은 아레니우스를
  그대로 보고했고 그게 옳았다고 보기 때문입니다. B 를 고르면 확장 횟수를 **지금** 박아야 합니다.

### B-3 O₂ 스크리닝 설계 — **μ_O 앵커가 P0 라고 봅니다**

LPSCl 이 O₂ 를 만나면 어떻게 되는지를 **grand potential 을 O 로 열어**(`get_element_profile`
의 열린 원소를 Li→O) 전방향으로 훑으려 합니다. 계산 전 단계입니다.

- **Q6.** PBE 의 O₂ 과결합 때문에 μ_O 축이 통째로 밀립니다. MP 는 anion correction 으로
  보정하고, UMA(omat)는 **기체 O₂ 가 분포 밖**입니다. 우리는 **μ_O 를 O₂ 분자로 잡지 않고
  고체 기준반응(예: Li₂O 생성)에 앵커**하고, **pO₂·온도 환산은 도구가 하지 않게** 막을
  생각입니다. 이 처방이 충분합니까? 아니면 열역학표(Reuter–Scheffler)로 가야 합니까?
- **Q7.** 이 축에서 **MD 로 무엇을 주장할 수 있습니까?** 우리 판단은
  *"반응 자체는 UMA 로 못 믿는다(검증 게이트 통과 전엔 정성 그림)"* 이고,
  낼 수 있는 것은 **화학종 계수 · 잔존 PS₄ 층수 vs 시간 · z-binned 밀도**,
  ⛔ **반응 중 궤적에서 D·Ea 는 못 뽑는다**(상이 바뀌는 중이라 확산이 정의되지 않음) 입니다.

---

## C. 확인 방법 (재현)

```bash
python3 -m pytest webapp/tests -q                    # 158 passed, 2 skipped
python3 tools/ionic/committee_sweep_verdict.py --selftest   # ⭕ 10 · ⛔ 0
python3 tools/db/validate_canonical.py               # 그래프 무결성 · 배선 일치
python3 tools/convention_check.py                    # 0 위반
python3 tools/kb_wiki.py lint                        # 0 errors
```

⚠ **시험이 전부 초록인 것은 근거가 아닙니다.** AW 가 정확히 그 상태에서 P0 넷을 찾았습니다.
가능하면 **실화면 대조**와 **P0 별도 주입**을 다시 해 주십시오.

## D. 우리가 답을 못 내는 것 (판단 요청 아님 — 사실 보고)

- **`[19]`** = Kang 2025 (Adv. Mater. 37, 2416872). 원고 Figure 2e 의 삭제 대상 문장에
  붙어 있는데, 원문 확인 결과 **술포네이트가 0회**이고 카복실레이트(CMC/PAA)·NMC622·
  **액체 전해질 코인셀**·NNP(PFP) 입니다. 그 문장을 뒷받침하지 않습니다.
  원고 참고문헌 목록이 repo 밖이라 **다른 곳에서도 인용되는지는 못 셌습니다.**
- **hazard 전행 대조(⑥ 나머지)** 와 **P1 Q2/Q5/Q7/Q4** 는 미이행입니다.
