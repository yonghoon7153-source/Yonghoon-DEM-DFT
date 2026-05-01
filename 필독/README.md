# 🚨 필독 — Verified Production Code 모음

**검증된 production code의 local mirror.**
KISTI/gabia 의 production folder가 cleanup 되어도 여기에 남음.

> [!important] 사용 규칙
> 1. 이 폴더의 .py 가 **paper-quality verified** — `CODE_INVENTORY.md` 와 cross-reference.
> 2. 새 code 작성 금지 — 여기 있는 것 사용/수정.
> 3. KISTI/gabia 의 원본과 ==**diverge되면 안 됨**== — 변경 시 양쪽 update.

---

## 구조

```
필독/
├── pipeline_v2/
│   ├── comp1_lpscl/
│   │   └── step3_dft_eos.py        (ntyp=4 fixed)
│   ├── comp2_lpscbr/
│   │   ├── step1_v2.py             (Stage 1 halogen + Stage 2 Li + Stage 3 anneal)
│   │   ├── anneal_champion.py      (best 하드코딩 + 100ps anneal)
│   │   ├── step2_mlip_eos.py       (MLIP EOS + BM3 fit + V0 grid 추천)
│   │   └── step3_dft_eos_comp2.py  (DFT 11 vol .in 생성)
│   └── modelC_lpsc16/              (TODO scp from KISTI)
├── tools/
│   └── bm3_fit_eos.py              (BM3 fit DFT EOS, V0 + closest grid 자동)
└── README.md
```

---

## TODO

- comp1 v2 step1_v2.py, anneal_top1.py, anneal_top2to5.py, step2_mlip_eos.py
- modelC v2 production code 전체
- Post-processing scripts (Bader, PDOS run shells)
- step4 BM3 fit script (사용 사례) + V0 structure extraction

KISTI / gabia에서 ==scp 또는 cat==으로 채워야 함.

---

## KISTI 원본 위치 reference

| comp | path |
|---|---|
| comp1 | `kisti:/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp1_lpscl/` |
| comp2 | `kisti:/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr/` |
| modelC | `kisti:/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/modelC_lpsc16/` |
