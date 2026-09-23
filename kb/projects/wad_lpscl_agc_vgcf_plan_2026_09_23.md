---
title: LPSCl | Ag–C | VGCF 점착일(W_ad) — 기존 LPSCl|NCM 워크플로 재사용 계획 · 보고량 카드 초안 (리뷰 전)
date: 2026-09-23
updated: 2026-09-23
tags: [adhesion, wad, interface, lpscl, silver, graphite, vgcf, anode, dem-input, estimand, review-pending]
status: 계획 — Codex 리뷰 + 내부(Fable) 리뷰 **전**. 계산 0. 파이프라인은 두 리뷰 뒤에 건다 (1저자 2026-09-23)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-mixed
---

# LPSCl | Ag–C | VGCF 점착일(W_ad) — 기존 LPSCl|NCM 워크플로 재사용 계획 · 보고량 카드 초안

> **요청** (DEM 쪽, 1저자 전달 2026-09-23 · **수정본 반영**): 음극 적층 LPSCl | Ag–C | VGCF 의 두 계면
> ① LPSCl↔Ag–C ② Ag–C↔VGCF 를 구성 쌍으로 나눠(P1: **LPSCl↔Ag · Ag↔흑연**) DEM 박리 시험의 입력 점착일을 달라.
> 정확도 목표 = 자릿수(물리흡착 ≲ 0.3 J/m² vs 화학결합 ≳ 1 J/m²).
> **수정본의 핵심**: 주값 정의를 **기존 LPSCl|NCM 워크플로의 isolated slab W_ad** 에 맞춘다 · W_sep 도 같이 ·
> 계면 제작 프로토콜 **v5** 와 **SE 슬랩 재사용** · **MLIP 값은 DFT 단일점으로 검증** ⇒ LPSCl|Ag 를 LPSCl|NCM 과 바로 나란히 비교.
> 1저자: *"파이프라인 걸기 전에 Codex 랑 우리 자기 Fable 리뷰도 받고 하자."*

> ⛔ **정정 (같은 날 초판)**: 초판은 *"DFT 급 LPSCl 슬랩·워크플로가 없다 · 옛 파이프라인을 물려받지 않는다"* 로 썼다.
> **틀렸다** — `kb/methodology/adhesion_energy.md` · `db/inputs/adhesion_templates/` · `db/properties/adhesion.json` 에
> 워크플로·템플릿·SE 슬랩 규약·기준값이 다 있었다. 첫 검색 결과가 60개에서 잘렸는데 확인하지 않았다.

---

## 0. 한 줄 요약

- **재사용한다**: v5 SE 슬랩(comp1 prim 2×2×3 · 624원자 · 두께 30 Å · 면적 351 Å²) · v5 제작 프로토콜 · 진공 30 Å · xy-shift 시드 · 분리 단일점.
- **Ag(111) 7×7 이 그 SE 측면 셀에 그대로 맞는다** (Ag 변형 −0.5 ~ −0.8 %, PBE 격자면 −2.2 %) — Ag 4층 196원자 + SE 624 ≈ **820원자**.
- 비교 기준값: **comp1 | NCM v5 xy-shift 20 seeds — 평균 1.153 · 중앙값 0.962 · 범위 0.555–1.85 J/m²** (UMA).
- ⚠ 결정할 것 셋: ① **v5 인가 v6 인가**(UMA 판도 다르다) ② 워크플로의 "isolated slab W_ad" 는 **조작상 W_sep** 이다 — 이름을 맞춘다
  ③ **DFT 단일점 검증을 NCM 기준값에도** 걸어야 공정하다.

---

## 1. 재사용할 워크플로 — 무엇이 있나 (repo 실측)

| 자산 | 내용 |
|---|---|
| `kb/methodology/adhesion_energy.md` | 정의 `Wad = (E_SE_iso + E_NCM_iso − E_int)/A` · v5 = 결정질 슬랩 + surface-only MQA · **xy-shift**(z-cut 폐기) · **UMA 진공 30 Å 규칙**(60 Å 면 10배 과대) · `v5_working`: **분리 후 이완 없이 단일점** · 계산기 표기 `uma-s-1p2` |
| `db/inputs/adhesion_templates/surface_mqa_v5.yaml` | v5 설정: `uma-s-1p2` · SE 2×2×1 · NCM 5×5×1 · gap 2.5 Å · MQA 800 K 2 ps → 300 K 2 ps → 500 K(Li) 3 ps → 100 K 2 ps + 이완 |
| `db/inputs/adhesion_templates/adhesion_v6_anneal_test.py` | v6: **`uma-s-1p1` · omat** · 1L NCM 고정 → SE 500 K 5 ps → 100 K 2 ps → 이완 → 분리 단일점 · 시드 42–46 |
| `tools/doping/run_cathode_interface.py` | v6 를 감싼 러너 — docstring 이 v6 를 *"verified production"* 이라 부른다 |
| `db/properties/adhesion.json` `adhesion_v5_crystalline_slab.xy_shift` | **기준값** — comp1 20 seeds: 평균 1.153 · 표준편차 0.392 · 중앙값 0.962 · 범위 0.555–1.850 J/m² · SE 624원자·30 Å·A 351 Å²(`Li6_v5_xyshift_FIX`: SE prim 2×2×3 · NCM 7×7×1 · 변형 0.2 %) |

### ⚠ 워크플로 안에서 서로 어긋나는 세 곳 (리뷰에 올린다)
1. **v5 vs v6.** 요청 수정본은 v5 를 쓰라 하는데, 러너는 v6 을 "verified production" 이라 부른다. 둘은 MQA(800 K 표면 연화 vs NCM 고정 500 K)와 **UMA 판(1p2 vs 1p1)** 이 다르다. ⇒ **기준값(comp1 v5 xy-shift 20 seeds)을 낸 바로 그 판**을 써야 비교가 선다. adhesion.json 에는 UMA 판 문자열이 **한 번도** 적혀 있지 않다.
2. **"isolated slab W_ad" 의 실제 조작.** 정의 줄은 "isolated slab" 이지만 `v5_working` 은 *"No relax after separation — single point only"* 이다. 같은 문서 247줄: *"엄밀히는 무이완 분리라 work of separation 계열 (W_ad 의 상계)"*. ⇒ 요청서 용어로 **이 값은 W_sep** 이다. 이완 슬랩 W_ad 는 워크플로에 없고 새로 낸다.
3. **슬랩 규격 표기.** yaml 은 Li6 를 `prim_2x2x1` (52원자, 변형 3.3 %)로 적었지만, 실제 기준값은 `Li6_v5_xyshift_FIX` = **prim 2×2×3 (624원자, 30 Å)** · NCM 7×7×1 · 변형 0.2 % 에서 나왔다(`prim_2x2x1` 13.6 Å 판은 *"too thin · overlap"* 으로 폐기). ⇒ **FIX 판을 재사용**한다.

### ⚠ 넷째 — "LPSCl|NCM 값" 이 하나가 아니다: 프로토콜마다 자릿수가 다르다 (같은 날 추가 · repo 실측)
리뷰 프롬프트를 쓰다가 원장에서 찾았다. **comp1(Li₆PS₅Cl)|NCM 한 계면**에 원장이 가진 숫자가 넷이다:

| 무엇 | comp1 | 근거 |
|---|---|---|
| 원장이 *"paper exp"* 로 부르는 기준 | **0.194 J/m²** (comp1–5 = 0.180–0.316) | `tools/adhesion_v30u/alpha_sensitivity_FINAL.py` 의 `PAPER` 상수(mJ/m²) · `adhesion.json` 1369줄 *"Experimental Wad is +0.18-0.32"* |
| v5 xy-shift · UMA · 분리 단일점 (= 우리가 재사용하려는 기준값) | 중앙값 **0.962** · 평균 1.153 (0.555–1.850) | `adhesion.json` 165–205줄 |
| paper #1 출판식 `WELLS_RAW − α·ΔW_strain` (α=1) | **0.075** (= 2.708 − 2.633) · comp2 **−0.064** | `db/properties/alpha_sensitivity_FINAL.json` `uniform` α=1.0 |
| v6 (`run_cathode_interface.py`, 러너가 *"verified production"* 이라 부르는 것) | **45–80** (5 seeds) | `adhesion.json` 1486–1498줄 — 원장 스스로 *"100–1000× over … rigid separation creates artificial dangling-bond energy"* |

- ⇒ **v5 기준값은 "paper exp" 의 약 5배**다. 출판식 comp1 값은 2.7 J/m² 두 개의 차라 0 근처에서 부호까지 흔들린다(comp2 음수). v6 은 절대값으로 **못 쓴다** — 1번 ⚠ 의 "v5 인가 v6 인가" 는 사실상 답이 나와 있다.
- ⇒ 요청서의 자릿수 판정(≲ 0.3 물리흡착 · ≳ 1 화학결합)에 NCM 을 넣으면 **어느 숫자를 쓰느냐에 따라 등급이 바뀐다** (0.19 → 물리흡착 급 · 0.96 → 경계). DEM 에 넘길 **절대값**을 무엇으로 할지가 새 결정이다 (§6-4).
- ⚠ **"paper exp" 의 측정 방식·출처는 repo 에서 확인하지 못했다.** `adhesion.json` 1498줄은 *"Sundar 2025: 0.2-0.4 J/m²"* 라고 적었는데 litdb 의 Sundar 2025 digest 에는 점착 값이 **없다** (`adhes|W_ad|J/m` grep 0건). 인용하지 않고 리뷰에 묻는다.

---

## 2. 계면별 셀 (재사용 SE 슬랩 기준)

| 계면 | 셀 | 변형 | 원자 |
|---|---|---|---|
| **P1-a LPSCl↔Ag** | SE prim 2×2×3 (측면 육방 20.13 Å · A 351 Å²) + **Ag(111) 7×7 · 4층** | Ag −0.46 %(a 4.086) · −0.80 %(4.10) · −2.23 %(PBE 4.16) — **Ag 를 맞춘다**(NCM 워크플로는 SE 를 NCM 에 맞췄다 — 리뷰 질문) | 624 + 196 = **820** |
| **P1-b Ag↔흑연** | Ag(111) × 흑연(0001) — 기존 워크플로 밖이라 **새로** 고른다 | (√3×√3)R30° / 흑연 2×2: −1.7 %(a 4.086) · PBE 격자면 3×3 류 68 Å² +0.5 % | 36–114 (작다) |
| P2 LPSCl↔탄소 | SE 슬랩 + 흑연 — P1 뒤 | — | — |
| P2 흑연 층간 | 문헌 대조용 기준값 | — | — |

⚠ Ag 격자상수는 **UMA 이완값**(MLIP 단계)과 **PBE+D3(BJ) 값**(DFT 검증 단계)이 다를 수 있다 → 두 단계에서 **같은 셀을 쓰도록** 변형률을 표에 적는다.

---

## 3. 단계와 비용 어림 (⚠ 규모 감각 — 약속 아님)

| 단계 | 내용 | 어림 |
|---|---|---|
| 0-a | SE 슬랩 재생성/회수 (repo 에 **파일은 없다** — 템플릿으로 `comp1_V0_k444.xyz` 에서 다시 만들거나 V100 백업 회수) · Ag·흑연 벌크 | 수 시간 |
| 0-b | **MP 반응에너지 사전검사** — LPSCl+Ag · LPSCl+LiAg · LPSCl+C · Ag+C (gabia `uma` env 의 mp_api) | 계산 0 |
| 1 | **UMA 단계 (기준값과 같은 판)** — P1-a xy-shift **20 seeds** (기준과 같은 수) · P1-b 시드 8 · v5 MQA · 분리 단일점 · 이완 슬랩 W_ad(추가) · UBER 강체 z-스캔 | GPU 수 시간–1일 |
| 2 | **DFT 단일점 검증** (PBE+D3(BJ), D3 끔 = 같은 기하에서 D3 항 분해) — E_int·E_sep 를 **P1-a 5 seeds + P1-b 4 seeds + NCM 기준값 5 seeds** | ≈ 820원자 단일점 × ~30회 — **가장 비싼 단계**. CPU 클러스터(KISTI) 권장 |
| 3 | 두께 점검 — Ag 4층 → 6층 1 seed · SE 는 30 Å(기준과 동일) | 소 |

GPU: gabia = b2o3 사건 빈도(≈5–6일) → modelc_2x 탄성 · kgy = cascade v6 + li2s. ⇒ UMA 단계는 GPU 가 비는 대로, DFT 단일점은 **KISTI**.

---

## 4. 보고량 카드 초안 (proposed — 비준 전)

### §1 무엇을 원하는가
> 기존 LPSCl|NCM 과 **같은 조작**으로 낸 LPSCl|Ag · Ag|흑연 의 분리일이, NCM 기준값과 나란히 놓았을 때 물리흡착 급인지 화학결합 급인지 — **DFT 단일점으로 검증된** 값으로.

### §1-c 답하지 않는 것
> 반응 **후** 계면(Ag–S 화합물 · LiAg 합금 뒤)의 점착 · 실험 박리강도 · 실접촉면적·구동압 효과(DEM 층의 몫) · 출판 관례(`α·ΔW_strain` 보정)와의 비교.

### §2 재는 양 (이름을 요청서 용어로 맞춘다)
```
W_sep(s)  = [E_sep(s) − E_int(s)] / A        # 워크플로 v5_working 과 같은 조작 — 분리 +30 Å, 셀 +30 Å, 이완 없음
W_ad(s)   = [E_A^rel + E_B^rel − E_int(s)] / A   # 각 슬랩을 같은 셀·같은 변형에서 이완 (워크플로에 없던 값)
W^DFT     = 같은 식, E 를 PBE+D3(BJ) 단일점으로 (UMA 기하 위) · W^noD3 = D3 항을 뺀 값 (같은 기하)
UBER E(d) = 이완 계면을 강체로 0.2–0.5 Å 간격, 평형 + 8 Å (UMA, 최저 시드 2개는 DFT 로)
```
s = xy-shift 시드(registry). A = 351 Å²(P1-a). ⛔ 출판 관례의 `− α·ΔW_strain` 보정은 **넣지 않는다** (실험 순위로 맞춘 항이고 Ag 에 대응물이 없다).

### §3 잘 정의되는가
| 물음 | 답 | 처리 |
|---|---|---|
| 상태가 하나인가 | 아니다 — xy registry 20개 · MQA 경로 의존 | 스칼라로 뭉치지 않는다: **W(s) 전부 + 평균·중앙값·범위** (기준값과 같은 요약) |
| 반응성 계면인가 | LPSCl↔Ag **그럴 수 있다** — 800 K 표면 연화에서 Ag–S 결합이 생길 수 있다 | 0-b 반응에너지가 음이면 값을 **"급격 계면·반응 전"** 으로 이름 붙인다. MQA 뒤 Ag–S 결합 수·원소 이동을 시드마다 센다 |
| MLIP 가 이 계에서 믿을 만한가 | **모른다** — UMA 는 진공에 민감했고(60 Å 10배), Ag–황화물 계면 검증 기록이 없다 | DFT 단일점 검증이 **판정의 조건**이다. UMA–DFT 차가 크면 UMA 값을 쓰지 않는다 (문턱은 리뷰 뒤 봉인) |
| 기준값과 같은 조건인가 | UMA 판 · v5/v6 · 시드 수가 **확인 전** | 기준값을 낸 판을 먼저 확정한다 (§1 ⚠1) |
| 기준값이 하나인가 | **아니다** — comp1|NCM 에 0.075 · 0.194 · 0.962 · 45–80 J/m² 넷 (§1 ⚠4) | 비교는 **같은 프로토콜 안에서만**. DEM 절대값은 §6-4 결정 전까지 **내지 않는다** |
| 참조 상태가 같은 전자 상태인가 | Ag 금속 · LPSCl 절연 — 스미어링을 모든 항에 같게 (DFT) | — |

### §4 게이트 (리뷰 뒤 봉인)
- 두께: Ag 4→6층에서 W 변화 < 0.05 J/m² (요청서) · SE 30 Å 는 기준과 동일
- DFT 검증: 시드별 |W^DFT − W^UMA| 의 허용 폭 — **리뷰에서 정한다**
- 판정: 시드 분포 **전체**가 ≲ 0.3 → 물리흡착 급 · ≳ 1 → 화학결합 급 · **0.3–1 을 걸치면 판정 보류**
- 기준값과의 비교는 **같은 조작(W_sep)·같은 검증 수준(DFT 단일점)** 끼리만

### §5 주장 / 비주장
- ✅ "기존 LPSCl|NCM 과 같은 조작(v5·xy-shift·분리 단일점)·같은 SE 슬랩에서, LPSCl|Ag 의 W_sep 분포는 … (DFT 단일점 검증 n seeds)"
- ⛔ 출판 관례 보정값과 비교 · ⛔ 계산 안 한 칸을 문헌으로 채우기 · ⛔ 시드 하나로 결론

---

## 5. 리뷰 계획 (1저자 지시)

1. **내부 리뷰 (Fable)** — 이 문서 + 워크플로 원문을 적대적으로 검토: 정의·재사용 정합·MLIP 검증 설계·반응성·통계.
2. **Codex 리뷰** — 프롬프트 `kb/reviews/` 에 작성해 1저자가 보낸다. §1–§4 가 대상.
3. 두 리뷰 반영 → 카드 봉인 → 결정 원장 proposed → 1저자 비준 → 파이프라인.

## 6. 결정 필요 (1저자) — 리뷰 전에도 답할 수 있는 것
1. **v5 인가 v6 인가** — 기준값(comp1 v5 xy-shift 20 seeds)을 낸 판을 알면 그걸 쓴다. UMA 판(1p1 · 1p2)도 같이.
2. **NCM 기준값도 DFT 단일점 검증**에 넣을지 (권고: 넣는다 — 안 넣으면 한쪽만 검증된 비교가 된다).
3. **기계** — UMA 단계(GPU) · DFT 단일점(KISTI 권고).
4. **DEM 에 넘길 절대값** (§1 ⚠4) — (a) 우리 프로토콜의 절대값 그대로(UMA 또는 DFT 단일점) · (b) 같은 프로토콜의 **Ag/NCM 비** 만 넘기고 NCM 절대 기준은 DEM 쪽이 고른다 · (c) 비 × "paper exp" NCM 값 (원장 paper #2 Option A 의 보정비 방식). (c) 는 금속(Ag) 과 산화물(NCM) 사이에 프로토콜 오차가 **같은 배수**라는 가정이라 리뷰에 묻는다(BV Q10).

## 출처
- `kb/methodology/adhesion_energy.md` · `db/inputs/adhesion_templates/{surface_mqa_v5.yaml, adhesion_v6_anneal_test.py}` · `tools/doping/run_cathode_interface.py`
- `db/properties/adhesion.json` (`adhesion_v5_crystalline_slab.xy_shift`, `cell_matching.Li6_v5_xyshift_FIX`)
- `kb/papers/adhesion_literature_review.md` · litdb: bucci2017 · bucci2018 · choi2025 · doux2020 · cronau2021 · dmt1975 · thorntonning1998 · pasha2014 · thakur2014 · luding2008 · fan2026
- 초격자 어림: 세션 scratchpad `zsl.py` (repo 도구 아님)
