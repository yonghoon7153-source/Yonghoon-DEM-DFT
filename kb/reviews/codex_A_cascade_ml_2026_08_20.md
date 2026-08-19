---
title: "교차리뷰 A — cascade 파이프라인 + 머신러닝 (codex 작업지시서)"
date: 2026-08-20
updated: 2026-08-20
tags: [codex, review, cascade, mlip, ml, uma, petmad]
status: 리뷰대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 교차리뷰 A — cascade + 머신러닝

> **분할 이유** (1저자, 2026-08-20): 하루에 쌓인 것이 두 갈래로 갈린다.
> **A = cascade 파이프라인과 그것을 떠받치는 ML/MLIP 판단** (이 카드),
> **B = NEB·MD·도구 전반** (`kb/reviews/codex_B_neb_md_tools_2026_08_20.md`).
> 두 갈래는 **서로 다른 결정을 막고 있어** 따로 리뷰해야 한다 —
> A 는 "cascade 를 다시 돌릴지", B 는 "지금 나온 장벽·Ea 를 인용할지" 를 정한다.

## 0. 리뷰어에게 — 이 카드를 읽는 순서

1. **먼저 `kb/projects/cascade_pipeline_fixes_2026_08_19.md` 를 읽는다** (595줄).
   거기에 **코드 정독으로 확인한 결함 8건 + 자기리뷰 2회 + P0-C 깔때기 구조**가 들어 있다.
   이 카드는 그것을 **대체하지 않고**, 그 위에 ML 축을 얹고 **첫 검증 단계**를 지정한다.
2. 그다음 §1(막고 있는 것) → §2(ML 축) → §3(리뷰어에게 묻는 것) 순으로 본다.

⚠ **이 카드가 말하지 않는 것**: NEB 장벽, MD 골격 검사, b2o3 아레니우스 — 전부 **B** 다.

## 1. ⛔ 첫 단계 — 미검증 전제 하나를 먼저 깬다

`cascade_pipeline_fixes_2026_08_19.md` §5-3 이 **아직 확인 안 된 전제** 위에 서 있다:
gabia `02_screen/baseline.json` 의 기준 구조가 **anneal 을 받았는지**.
받았으면 P1-F(기준만 anneal 없음)는 취소되고, 안 받았으면 **screen 단계의 모든 Δ 가
비대칭 비교**가 된다. 리뷰의 나머지 결론 여럿이 여기에 매달려 있다.

```bash
# gabia (base env) — 경로를 확정한 적이 없으므로 find 부터
find /data/work -name 'baseline.json' -path '*02_screen*' 2>/dev/null | head
# 찾은 경로로: python3 -c "import json;d=json.load(open('<경로>'));print(list(d)[:20])"
```
⇒ **이것부터 하고 리뷰를 시작한다.**

## 2. ML/MLIP 축 — 2026-08-19~20 에 새로 들어온 것

### 2-1. ✅ 확정 실측 — UMA 는 황화물에서 정확하고 보존적이다
판정 카드: `kb/results/uma_force_accuracy_li3ps4_2026_08_19.md`
값: `db/properties/mlip_bench_li3ps4_uma.json` · `mlip_engine_probe_{comp1,li3p}.json`

| 측정 | 결과 | 무엇을 닫나 |
|---|---|---|
| Li₃PS₄ 힘 MAE | **30.0 meV/Å** (전용모델 35.6 / PET-MAD 기저 63.9) | **"UMA sulfide PES softening" 알리바이 철회** |
| 보존성 | δ 의존성 6배↓ + 재실행 비재현 | "힘이 gradient 가 아니라서 D 과대" 가설 사망 |
| 셀 비용 | 416원자가 3시드×52원자보다 **통계 2.7배 / 비용 0.6배** | β 게이트 실패(홉 부족)의 처방 |
| Li₃P 잔여력 | fmax 0.0205 eV/Å | Li 금속 계면에 UMA 1차 관문 통과 |

⇒ **cascade 의 문제는 모델이 아니라 방법론이다.** 리뷰를 그쪽으로 몰 것.

### 2-2. ⬜ 미해결 — 응력은 아무것도 안 쟀다
cascade 부피 편향 **+32.7 %** 는 위 어느 측정으로도 무죄가 되지 않는다.
PET-MAD Li₃PS₄ 데이터셋에 **stress 라벨이 없어서** 잴 수가 없었다.

**후보 처방** (`litdb/papers/zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill.md`):
fairchem 이 **UMA 파인튜닝을 공식 지원**한다 —
`create_uma_finetune_dataset.py --uma-task=omat --regression-tasks efs` → `fairchem -c …yaml`.
`efs` 에 **stress 가 들어간다.** LoRA 는 fairchem 에 없고(전체 파라미터만),
`freeze_backbone` 은 head-only 라 단거리 PES 교정에 부적합.
필요한 ab initio 구조는 **O(10²)** (PET-MAD ~100–400, Zhang npj ~200 — 두 논문이 독립 수렴).

⇒ **리뷰어 질문 Q1**: cascade 는 모델을 **3,615회 이상 재사용**한다. 파인튜닝 비용이
한 번이고 수혜가 3,615회면 수지가 맞는가? (SEI 장벽 4개에는 20 d → 10–18 d 라 안 맞는다고
판단했다 — 그 판단이 맞는지 같이 봐줄 것.)

### 2-3. ⬜ cascade predictor 의 ML 위생 — 외부 기준선 대비 감사
`litdb/papers/kauwe2021_ml_materials_properties_dissertation_sparks.md` §2·§6 기준.
전문은 `litdb/comparison_vs_ours.md` **축 J-4**.

| 항목 | 문헌 기준 | 우리 | 판정 |
|---|---|---|---|
| 분할 | 종 단위 그룹 분할 필수 | 랜덤 5-fold 가 캐노니컬 | ❌ **누출**: 랜덤 상한 **0.986** → LOCO **0.220**, Pugh **0.020** |
| 특징 | CBFV | 도펀트 one-hot + 상수 2개 | ❌ 외삽 근거 이전 불가 |
| 작업 형식 | 상위 1 % 탐색은 **분류**가 우월 (precision 0.56 vs 0.39–0.44) | 6타깃 전부 회귀 | ❌ 목적–형식 불일치 |
| 베이스라인 | 무작위 → 최근접이웃 → 모델 사다리 | `DummyRegressor` 있으나 **미보고** | ⚠ |
| 불확실도 | 시드 5개 ±σ | 단일 시드 `random_state=42` | ⚠ 우리 MSD 멀티시드 규율과도 어긋남 |
| 학습↔적용 분포 | 어긋남을 **명시 보고** | winner 622–681행 학습 → 3,615행+신규 적용 | ❌ 같은 구조의 실패 위험 |

⇒ **리뷰어 질문 Q2**: `screen_de` 랜덤 CV **0.986** 은 발표에 쓸 수 있는 숫자인가?
우리 판단은 **아니다**(누출값)인데, 그러면 **어떤 숫자를 쓰나** — LOCO 0.220 을 그대로 쓰면
"예측기가 쓸모없다" 로 읽힌다. 정직하면서 유용한 보고 형식이 뭔지가 진짜 질문이다.

### 2-4. ⬜ committee 에 PET-MAD 를 넣을까
`tools/ionic/mlip_committee.py` 의 기존 3종 중 **MACE-MP-0·SevenNet-0 이 둘 다 MPtrj** 라
상관돼 있고, 상관된 멤버는 불일치를 **과소평가**한다.
PET-MAD 는 데이터(MAD)·범함수(PBEsol)·아키텍처가 전부 탈상관이고,
**`calculate_uncertainty=True` 한 줄로 LLPR 불확실도**가 나온다 —
이건 HAML 의 **γ 게이트**("모델이 모른다고 말하면 DFT 로 돌아간다")를 UMA 스택에서 흉내낼
유일한 수단이다(UMA 는 단일 모델이라 앙상블 신호가 없다).
⚠ **별도 conda env 필수**(`metatrain==2025.10` 하드핀 — gabia UMA env 오염 금지),
기준선 재교정 필수(PBEsol×PBE 혼합이라 불일치 바닥이 올라간다),
**파인튜닝본 투입 금지**(`Table S3`: LoRA 후 MAD 기저 성능 3–19배 악화).

⇒ **리뷰어 질문 Q3**: cascade 3,615행에 committee 를 돌리는 비용이 감당되나?
아니면 **외삽 의심 구간만** 골라 돌리는 게 맞나 — 고른다면 무엇으로 고르나?

## 3. 리뷰어에게 묻는 것 (요약)

| # | 질문 | 걸린 결정 |
|---|---|---|
| **Q0** | `02_screen/baseline.json` 의 기준이 anneal 을 받았나 | 리뷰 나머지의 전제 |
| **Q1** | stress 파인튜닝(efs)이 cascade 부피 편향에 수지가 맞나 | cascade 재실행 여부 |
| **Q2** | 누출된 0.986 대신 **무엇을** 보고하나 | 발표·원고 |
| **Q3** | committee 를 전수로 돌리나 부분으로 돌리나 | 비용 |
| **Q4** | `cascade_pipeline_fixes_2026_08_19.md` 의 P0-C(깔때기 구조) 처방이 타당한가 | 재설계 범위 |

## 4. 손대면 안 되는 것

- **`db/properties/sei_neb.json`** — gabia 로컬 상태가 있다. `git checkout` 금지(1저자 지시).
- **정본 D·Ea 규약**(MSD 창 2–50 ps, 자유절편 D) — 바꾸려면 `tools/convention_check.py` 0 위반을
  유지하며 전 파일을 같이 고쳐야 한다.
- **UMA 는 Li₃N 에 사용 금지**(2026-06). Li₃P 는 1차 통과했지만 **장벽은 미검증**이다.

---

# 5. 자기리뷰 — fable-5 max (2026-08-20 새벽, codex 교차검증용 선행 리뷰)

> 규칙: 위 본문(§0–4)은 **손대지 않고** 여기서 반박한다. codex 는 §0–4 와 이 절을 **각각 독립으로**
> 평가한 뒤 우리 자기리뷰가 놓친 것을 찾아 달라. 도구 수정은 교차검증 합의 뒤 일괄 반영한다
> (오늘 selftest 미실행 푸시 2회 전례 — 새벽에 코드를 더 만지지 않는다).

### A-R1. ⛔ "범용이 전용을 이겼다" 는 **힘 축에서만** 성립한다
에너지는 bespoke **1.165 meV/atom** vs 우리 보정 후 **13.5** — 자릿수로 밀린다.
(우리 잔차엔 PBE↔PBEsol 비선형 불일치가 섞여 등가 비교는 아니지만, 헤드라인의 확대 인용을
막아야 한다.) §2-1 의 결론 문장은 이 한정 없이 읽히기 쉽다 → 판정 카드에 caveat 박음(완료).
**MD/NEB 용도로는 힘 결론으로 충분**하므로 §2-1 의 실용 결론은 유지.

### A-R2. ⛔⛔ **상대에너지 RRMSE 2.4 % 는 지표 자체가 약하다** (코드 재독으로 확인)
`bench_against_dft.py` 구현: `ΔE(i) = E_i − E_0` **첫 구조 기준**, test 는 **16–64원자 혼합**
⇒ 분모(기준 ΔE RMS)가 **크기 차이라는 자명한 항**으로 부풀어 RRMSE 가 작아 보인다.
축 J-1 에서 Zhang npj 22.8 %(같은 셀 전이상태 ΔE) 옆에 놓은 것은 **오독 유도**였다
→ J-1 과 판정 카드에 경고 박음(완료). 정직한 수치는 RMSE 0.688 eV.
**도구 수정 제안(합의 후)**: 같은 조성·크기 부분집합 안의 쌍으로 재계산.

### A-R3. ⚠ 보존성 판정의 적용 범위가 본문 서술보다 좁다
프로브는 **rattle 없이 DFT-V0 근처 배치의 원자 4개**만 봤다(코드 재독 확인).
PET-MAD 의 직접힘 병리는 **고온 MD 배치**에서 드러난다. "보존적" 판정은
시험한 배치까지만이고, **MD 스냅숏/rattle 배치 재프로브(1분)** 가 남았다.
§2-1 표의 "가설 사망" 은 유지하되 근거의 사거리를 이렇게 한정한다.

### A-R4. ⛔ "416원자 1런" 처방이 **우리 자신의 멀티시드 규율과 충돌한다**
① 같은 박스의 Li 192개는 집단 운동으로 상관 — 유효 표본 < 192, "2.7배 통계"는 상한
  (`codex_stats_question_2026_08_11.md` 와 같은 논지).
② 1런 = 시드 1개 = **시드 산포 오차막대 없음** — "비율도 멀티시드 판정만"(SEMIFINAL) 위반.
⇒ 처방 정정: **2–3시드 × 416원자** (35–53 h). 판정 카드 §5-3 에 반영(완료).

### A-R5. Q0 스니펫의 경로가 추측이었다 → find 우선으로 교체(완료).

### A-종합 — §0–4 의 골자는 생존한다
"cascade 의 문제는 모델이 아니라 방법론" 방향은 A-R1~R3 뒤에도 선다 —
**힘 축 실측 + 보존성(제한적) + Li₃P 1차 통과**가 남고, 죽은 것은 확대 해석들이다.
Q1(수지)·Q2(보고 형식)·Q3(committee 범위)은 자기리뷰로 못 닫는다 — codex 몫.
