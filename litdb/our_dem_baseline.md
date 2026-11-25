# ⛔ 우리 DEM+MPM 기준값 — **이 브랜치에는 아직 없다**

> 만든 날 2026-09-09 · 상태 `⛔ 자리표시(placeholder)` · 값 0개
>
> 이 파일은 **기준값 문서가 아니다.** DEM digest 84편과
> `comparison_vs_ours_DEM.md` 가 **98곳에서** 이 경로를 기준값으로 가리키는데
> 파일이 없어서 404 였다. 없는 값을 지어내는 대신, **없다는 사실과 어디서 와야 하는지**를
> 적어 둔다.

---

## 1. 지금 무슨 상태인가

| 트랙 | 기준값 문서 | 상태 |
|---|---|---|
| SE / DFT·MLIP | `litdb/our_dft_baseline.md` | ✅ 있다 (정본) |
| DEM / MPM | `litdb/our_dem_baseline.md` | ⛔ **없다 — 이 파일이 그 빈자리다** |

**따라서 DEM digest 의 “§7 우리 DEM+MPM 대비” 절과
`comparison_vs_ours_DEM.md` 의 대조 서술은, 이 브랜치 기준으로 근거 문서가 없다.**
그 서술들이 틀렸다는 뜻이 아니라 **이 브랜치에서 확인할 수 없다**는 뜻이다.
DEM 수치를 인용하려면 아래 §3 이 먼저 끝나야 한다.

## 2. 어디서 와야 하나 (실측)

`git log --all -- litdb/our_dem_baseline.md` 로 확인한 것:

- 실물 55줄짜리 문서가 **`origin/claude/solid-state-cathode-improvement-hevry0`**
  브랜치의 커밋 **`e7b668377`** (2026-06-26) 에 있다. 이후 `eb9038f4a` 에서도 손댔다.
- 그 커밋은 **HEAD 의 조상이 아니다** (`git merge-base --is-ancestor` → false).
  2026-07-16 “stoic-knuth 브랜치에서 통합” 때 **digest 는 왔는데 기준값 파일은 안 왔다.**
- 그 판이 담고 있는 **축**(값은 여기 옮기지 않는다 — §3 참조):
  §0 소재 파라미터(E_SE real / DEM effective / MPM champion · ν_SE · E_CAM · σ_grain) ·
  §1 압밀·porosity(pure-SE / real_14 / Cronau overlap / Heckel / 강체구 floor / Furnas dip) ·
  §2 전달 삼중항(σ_ionic · σ_electronic · σ_thermal 의 LOOCV 와 형태) ·
  §3 MPM 고유(형상 소성 · scaffold 커플링 · coverage) ·
  §4 발산·한계 · §5 비교 체크리스트.

꺼내는 명령(값을 읽기만 한다 — 승격은 §3):

```bash
git show e7b668377:litdb/our_dem_baseline.md
```

## 3. 정본 승격에 필요한 것 — **1저자 판단**

⚠ **그 판을 그대로 복사해 오면 안 된다.** 두 가지 이유다.

1. **낡았다.** 그 문서는 2026-07-15 판인데 DEM digest 는 2026-09-04 까지 늘었다.
   각 행이 지금도 정본인지 행 단위로 확인해야 한다.
2. **지위가 없다.** 우리 규율상 인용되는 수는 원장(`db/properties/…`)에 status·citable·
   prohibitions 가 붙어야 한다. 그 55줄에는 그 층이 없다.

선례는 있다 — `positioning_vs_geodict.md` 가 2026-07-28 에 같은 절차(타 브랜치 →
정본 승격)를 밟았다. 같은 절차를 밟되, 승격 시점에 **각 행의 출처와 지위**를 같이 적는다.

## ⛔ 이 문서가 못 하는 것

- **값을 주지 않는다.** 한 줄도 인용할 수 없다. 축 이름만 적어 둔 것은
  “무엇이 비어 있는지”를 보이기 위한 것이지 값의 요약이 아니다.
- **DEM digest 의 기존 대조 서술을 검증하지도, 철회하지도 않는다.**
  판정은 1저자가 §3 을 끝낸 뒤에 나온다.
- 이 파일이 존재한다는 것만으로 링크가 “살았다”고 읽으면 안 된다 —
  **링크는 살았지만 값은 여전히 없다.**
