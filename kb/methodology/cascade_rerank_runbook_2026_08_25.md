---
title: cascade 재랭킹 런북 ①~⑤ — li_mobility_score 복구 후 실행
date: 2026-08-25
updated: 2026-08-25
tags: [cascade, doping, bvse, ranking, runbook, blocked-on]
status: 진행중-①
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-25
verifiedBy: "버그는 코드에서 직접 확인(저장 뒤 계산) · 결과는 cascade_v23_all.csv 에서 0/3615 로 실측 · 이동도 정규화 항이 전 행 0.5 동일함을 재계산으로 확인"
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: multi-source-primary
---

# cascade 재랭킹 런북 ①~⑤ (2026-08-25)

> ✅ **착수 조건 충족 (2026-08-25 20:58)** — AlI₃ x020/x050/x100 완주 (rc=0). ① 진행 중.

## 1. 왜 재랭킹이 필요한가

`bvse_proxy.py` 가 `li_mobility_score` 를 **저장한 뒤에** 계산하고 있었다.
그래서 화면 순위표에만 쓰이고 json 에는 **한 번도 안 들어갔다.**

```
cascade_v23_all.csv   migration_volume_fraction   681/3615   ← 입력은 있다
                      bvs_li_proxy_score          681/3615   ← 입력은 있다
                      li_mobility_score             0/3615   ← 결과가 없다
```

그 빈 열을 `combine_rankings.py` 가 읽고, `normalize()` 의
*"전부 결측이면 0.5"* 규칙이 메웠다. 실측으로 **이동도 정규화 항이 3,615행 전원 0.5** 다.

```
score_combined = 0.4×안정성 + 0.3×탄성 + 0.3×이동도
                                          └─ 전원 0.15 상수 = 순위에 기여 0
```

**⇒ MD σ 를 비용 때문에 접고(stage 10 `TOP_K_SIGMA=0`) BVSE 프록시로 갈아탔는데,
그 BVSE 결과조차 랭킹에 들어간 적이 없다.** `score_combined` 는 사실상
**안정성 + 탄성 두 축**이었다.

⚠ 이것은 "랭킹이 틀렸다" 가 아니라 **"이동도 축이 작동한 적이 없다"** 이다.
  기존 순위는 두 축 기준으로는 유효하다 — 다만 세 축이라고 말하면 안 된다.

**도구 수정은 끝났다** (`bvse_proxy.py`, 2026-08-25). 남은 것은 **기존 데이터 복구와
재랭킹**이고, 그건 결과가 바뀌는 일이라 사람이 판단할 사안이라 자동으로 하지 않았다.

## 2. 순서 ①~⑤

```bash
# ── ① backfill — 새 계산 0. 입력 두 개가 이미 저장돼 있어 산수만 하면 된다
cd /data/work/repo && git fetch origin claude/friendly-meitner-lldvar && git reset --hard FETCH_HEAD
# ⛔ 2026-08-25 정정 — 정본 파일명은 **bvs_report.json** 이다 (bvse_proxy --out 예시
#   그대로). 원판의 'bvse*.json' 패턴은 0건 매치라 ① 이 조용한 no-op 이 될 뻔했다.
for f in $(find /data/work/runs -name 'bvs_report.json' -not -path '*bak*' 2>/dev/null); do
  python3 tools/doping/bvse_proxy.py --backfill --out "$f"
done
# 기대: "채움 N · 이미 있음 0 · 입력 부족 M". 멱등이라 두 번 돌려도 안전.

# ── ② 재랭킹 — 이제 이동도 30 % 가 실제로 일한다
#    ⚠ 실행 전에 **기존 순위를 반드시 떠 둔다** (전후 비교가 판정 근거가 된다)
cp db/properties/cascade_v23_all.csv /data/work/runs/cascade_v23_all_before_rerank.csv
python3 tools/doping/combine_rankings.py --cascade_dir <실제경로> --out <출력>

# ── ③ collect → 정본 CSV 갱신
python3 tools/doping/collect_dataset.py ...

# ── ④ A2: best-of-N 보정
python3 tools/doping/select_winners.py --results <uma_results.json> \
    --out <winners.json> --fixed_n 15
#    후보 수 15~150(10배)이 챔피언 점수와 r=+0.321 로 붙어 있던 인공물 보정.
#    표본 부족 그룹은 탈락시키지 않고 **표시**한다.

# ── ⑤ A3: 축 상관 + Pareto
python3 tools/doping/axis_corr_csv.py                       # 정본 CSV 기준
python3 tools/doping/analyze_screening.py --results <...> --out <...> \
    --axis_corr --pareto
```

## 3. ⏸ 왜 AlI₃ 완주를 기다리나

1. **AlI₃ 가 새 행을 추가한다.** 지금 재랭킹하면 AlI₃ 들어올 때 또 해야 하고,
   그 사이 **순위가 두 판 존재**하게 된다.
2. **AlI₃ cascade 는 수정 이전 코드로 돌고 있다** (gabia 가 그 전 커밋). 그쪽
   BVSE 출력도 `li_mobility_score` 가 비어 있을 것이므로 어차피 ① 대상이다.

⇒ 한 번에 처리한다.

## 4. ⚠ 재랭킹은 판정 이력에 남겨야 한다

순위가 바뀌면 그것은 **결과의 변경**이다. `db/governance/` 에 기록하지 않으면
"언제 왜 47종 순위가 달라졌나" 를 나중에 못 답한다. ② 를 돌릴 때 같이 만든다.
전후 CSV 를 떠 두라고 위에 적은 것이 그 근거 자료다.

## 5. 곁다리로 확인된 것 (재랭킹과 무관, 결함 아님)

`kb/methodology/cascade_pipeline_anatomy_2026_08_13.md` 가 이미 답을 갖고 있다:

- **stage 10(σ MD)·11(W_ad) 는 미실행이다 — 미수확이 아니다.** `TOP_K_SIGMA=0` 으로
  꺼서 돌렸다(비용). 총 투입 ~1,100 GPU-시간이지 4,600 이 아니다.
- 축 커버리지 ~20 % 는 결손이 아니라 설계 — 하류가 `--top 10` 만 처리한다.
- **47종 풀을 가른 축은 ESW 하나다.** 탄성·BVSE 는 90종 전부 있었다.

## 6. A1 실측 (2026-08-25, `axis_corr_csv.py`)

```
공선성(|ρ|≥0.85)  0건
최대 |ρ|          0.326
상충 1건          안정성(ΔE) ↔ |ΔV/V0|   ρ = −0.326
```

Yang 2026(BML)은 σ↔Q_CC 가 붙어 Pareto 가 할 일이 없었는데, **우리는 반대로 축이 거의
독립**이다 ⇒ ⑤ 의 Pareto 가 실제로 선택지를 준다. 가중합으로 뭉개면 그만큼 잃는다.

⚠ 단 지금은 이동도 축이 비어 있어 사실상 두 축짜리 결과다. ①② 뒤에 다시 재야 한다.

## 안 한 것 / 못 하는 것

- **기존 순위를 다시 계산하지 않았다.** 도구만 고쳤다.
- ②③ 의 경로 인자는 실제 디렉터리를 봐야 정해진다 — AlI₃ 완주 후 확정.
- backfill 은 **입력이 없는 행을 0 으로 메우지 않는다.** 0 은 최하점이라
  "없다" 와 다른 거짓말이 된다. 건너뛰고 개수를 보고한다.
