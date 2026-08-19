---
title: 부피로 떨어뜨린 100개가 "에너지로는 멀쩡한" 진짜 이유 — 조성 섞임이지 구조가 아니다
date: 2026-08-18
updated: 2026-08-18
tags: [cascade, screening, mlip, uma, volume-gate, simpson-paradox, seminar]
status: 확정
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-18
verifiedBy: self
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: single-source
---

# 부피로 떨어뜨린 100개가 "에너지로는 멀쩡한" 진짜 이유

세미나 Step 3 슬라이드의 해설 — *"100 of 3,615 changed by more than 25 %;
their energies look like the rest"* — 이 **왜** 그런지 1저자가 물었다. 앞 판의 답
("오히려 중앙값이 더 낮다, −0.619 vs −0.480")은 **사실이지만 원인 설명이 아니었고,
그대로 두면 "무너진 구조가 더 안정하다" 로 읽힌다.** 실측으로 갈랐다.

출처: `db/properties/cascade_v23_all.csv` (3,615행, `screen_dV_over_V0` ·
`screen_de_per_atom`). `screen_converged` 는 3,615개 **전부 True** — 수렴 실패는 없다.

## 1. 겉보기 차이는 **조성 섞임**이다 (Simpson 형)

| | 원값 de 중앙값 | 도펀트 중앙값을 뺀 **잔차** 중앙값 |
|---|---|---|
| dropped (100) | **−0.619** | **+0.010** |
| kept (3,515) | −0.480 | +0.000 |

⇒ **같은 도펀트끼리 비교하면 차이가 사라진다.** 원값의 0.14 eV/atom 격차는
탈락군이 *원래 de 가 낮은 몇 종*으로 채워져 있기 때문이지, 셀이 무너져서가 아니다.

탈락 100개는 **101종 중 14종**에서만 나온다. 도펀트 안에서 직접 비교하면:

```
Y2O3    dropped −0.704  vs  kept −0.915   ← 탈락 쪽이 오히려 **높다**(나쁘다)
TiO2    dropped −0.632  vs  kept −0.631   ← 같다
Nb2O5   dropped −0.962  vs  kept −0.979   ← 탈락 쪽이 높다
Sb2S3   dropped −0.332  vs  kept −0.301
LaF3    dropped −0.680  vs  kept −0.695
```

## 2. 남는 약한 상관은 **"이완은 내리막"** 이라는 당연한 것

|ΔV| 구간별 de 중앙값 — **불연속이 없다. 25 % 는 특이점이 아니라 꼬리 끝이다.**

```
 0– 5 %  n= 408  −0.338
 5–10 %  n= 648  −0.463
10–15 %  n=1134  −0.476
15–20 %  n= 979  −0.509
20–25 %  n= 346  −0.588
 >25  %  n= 100  −0.619
```

Pearson r(|ΔV|, de) = **−0.373** 전체 · **−0.259** 도펀트 내부.

de 는 **이완이 끝난 뒤**의 에너지고 |ΔV| 는 **얼마나 멀리 갔나**다. 더 멀리 내려간
것이 더 낮은 데서 끝나는 건 정의상 그렇다 — 물질에 대한 정보가 아니라 **최적화
경로에 대한 정보**다. r −0.26 은 그 크기만큼이다.

## 3. 탈락은 전부 **수축**이다 — 팽창이 아니다

```
dropped 100:  팽창 0 · 수축 100   ΔV 중앙 −26.8 %
kept  3,515:  팽창 200 · 수축 3,315   ΔV 중앙 −13.2 %
전체 분포:    −33.1 % … 중앙 −13.3 % … 최대 +14.6 %
```

⇒ "25 % 넘게 부풀었다" 가 아니라 **"25 % 넘게 쪼그라들었다"** 다. 슬라이드 문구
`changed by more than 25 %` 는 부호를 말하지 않으므로 그대로 맞지만, **말로는
"무너졌다/치밀해졌다"** 라고 해야 한다.

### ⛔ 정정 (2026-08-19) — "B₂O₃ 30/30 전멸" 은 틀렸다

초판이 *"B2O3 총 30개 · 25 % 초과 30개 · kept 0 종 — 전량 탈락한 유일한 도펀트"* 라고
적었다. **raw `dopant` 로 세는 바람에 절반만 봤다.** `convention_check.py` 의
`RAW_DOPANT_GROUP` 규칙이 정확히 이 함정을 막으라고 있는데(*"WO3 와 WO3+Clrich 가
갈린다"*), 즉석 분석 스크립트는 그 검사를 안 받는다.

```
B2O3        (plain)  n=30 · 탈락 30 · |ΔV| 26.2~33.1 % · 자리 P_4b   · 보상 compound_set
B2O3+Clrich (chain)  n=30 · 탈락  0 · |ΔV|  2.2~17.4 % · 자리 Li_24g · 보상 compound_set_chain
```

**전량 탈락한 base_species 는 하나도 없다.** 그리고 게이트 자체는 정상 작동했다 —
`|ΔV| > 25 %` 인데 `rank_combined==1` 인 행은 **0/270** 이다.

두 변형은 자리만 다른 게 아니라 **조성이 다르다** (농도는 둘 다 0.25 로 같다):

| | B2O3 (plain) | B2O3+Clrich (chain) |
|---|---|---|
| 조성 | Li28 **P2** S17 Cl4 O3 B2 | Li17 **P4** S16 **Cl5** O3 B2 |
| 양이온 자리 | **P_4b** (골격) | Li_24g |
| 전하보상 | compound_set | compound_set_chain |

⇒ plain 은 **PS₄ 골격에서 P 를 4 → 2 로 절반 빼낸다.** 그러니 무너진다.
  chain 은 골격을 안 건드리고 **Li 를 빼고 Cl 을 하나 더 넣어** 보상한다.

### ⭐ 그래서 진짜 결론 — 부피 붕괴는 **P 골격에 손을 댈 때** 일어난다

3,615행 전수:

```
양이온 자리별 탈락률     P_4b  93/ 825 (11.3 %)   ← 탈락 100개 중 93개
                      Li_24g  7/2460 ( 0.3 %)
                      Li_48h  0/ 330 ( 0.0 %)     38배 차이

전하보상별            compound_set       100/3105 (3.2 %)
                     compound_set_chain   0/ 510 (0.0 %)

음이온 자리별         S_16e 3.0 % · S_4a 2.9 % · Cl_4d 2.1 %   ← 무관
```

**음이온 자리는 아무 상관이 없고, 양이온 자리가 전부다.** 9장의 실측(자리가 바뀌는 6종)과
같은 축이고, 그 장의 "자리를 미리 정할 수 없다" 를 부피 축에서 다시 확인해 준다.

## 4. 그래서 부피 게이트가 필요한 이유가 **더 정확해졌다**

앞 판의 논리는 "탈락군이 에너지로는 오히려 좋아 보인다" 였다. 실제 논리는 더 세다:

> **에너지는 그 구조가 무너졌는지에 대해 아무 말도 하지 않는다.**
> 조성을 고정하면 탈락군과 잔류군의 de 가 통계적으로 구분되지 않는다(+0.010 vs +0.000).
> 에너지 축과 기하 축은 **거의 직교**한다 — 그래서 둘 다 봐야 한다.

같은 개수(100)를 에너지 위에서 자르면 컷은 −0.0448 eV/atom 이고, 그 100개와
부피로 뺀 100개의 **교집합은 0** 이다.

## 5. ⚠ 열린 것 — 풀 전체가 중앙값 −13 % 로 수축한다

3,615개 중 팽창은 **200개뿐**이고 중앙값이 −13.3 % 다. 이완이 이 정도로 한쪽으로
쏠리는 것은 **출발 셀 부피가 계통적으로 크다**는 뜻이다. 원인 후보(미검증):
치환을 host 격자 부피 그대로에서 시작한다 / 전하보상으로 Li 를 빼도 부피를 안 줄인다 /
생성 단계에서 겹침 방지로 셀을 부풀린다. **확인 안 했다.**

이게 사실이면 25 % 컷의 위치 자체가 "얼마나 부풀렸나" 에 딸린 값이 된다.
→ `kb/questions/` 로 올릴 후보.

## 이 카드가 말하지 않는 것

- **무너진 100개가 무엇이 되었는지** — 최종 구조를 열어 보지 않았다. 분해인지,
  비정질화인지, 다른 결정상인지 모른다. "B³⁺ 가 작아서" 는 **읽기이지 측정이 아니다.**
- **UMA 가 그 영역에서 신뢰할 만한가** — 학습 분포 밖에서 MLIP 가 무르다는 일반론은
  있으나 이 풀에서 확인하지 않았다. DFT 대조 없음.
- **de 의 기준계** — host 상대 Δe 다(hull 거리가 아니다,
  `kb/methodology/cascade_pipeline_anatomy_2026_08_13.md`). 절대값 인용 금지.
- **왜 −13 % 인가** — 위 5절. 원인 미확인.

## 재현

```bash
python3 - <<'PY'
import csv, io, statistics as st
D=[]
for r in csv.DictReader(io.open('db/properties/cascade_v23_all.csv',encoding='utf-8')):
    try: D.append(dict(v=float(r["screen_dV_over_V0"])*100,
                       e=float(r["screen_de_per_atom"]), dop=r["dopant"]))
    except Exception: pass
med={}
for x in D: med.setdefault(x["dop"],[]).append(x["e"])
med={k:st.median(v) for k,v in med.items()}
for nm,S in (("dropped",[x for x in D if abs(x["v"])>25]),
             ("kept",   [x for x in D if abs(x["v"])<=25])):
    print(nm, len(S), "de중앙 %+.3f"%st.median([x["e"] for x in S]),
          "잔차중앙 %+.3f"%st.median([x["e"]-med[x["dop"]] for x in S]))
PY
```

## 반영한 곳

| 무엇 | 어디 |
|---|---|
| 대본 정정 ("더 낮다" → 조성 섞임) | `kb/seminars/cascade_dopant_screening_story_2026_08.md` 11장 |
| 질문 대비 숫자 (14종·B₂O₃ 30/30·전부 수축) | 같은 절 `말로만` |
