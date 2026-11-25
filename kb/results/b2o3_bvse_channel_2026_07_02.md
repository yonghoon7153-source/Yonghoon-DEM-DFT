> # ⛔⛔ b2o3 MD 축 마감 — **이 카드의 UMA-MD 수는 인용 불가** (배너 2026-09-09)
>
> b2o3 의 **UMA-MD 전도도 축 전체**(D · Ea · σ · 구간 Ea)가 **2026-08-25 에 닫혔고**
> 2026-09-07 에 소급 등록·비준됐다 — `D-2026-09-07-b2o3-md-closure-retrospective`(active) ·
> `db/properties/b2o3_md_closed_retrospective_2026_08_25.json`. **인용 가능한 수는 0개다**
> (`0.199` · `0.206` · `0.21±0.03` · `0.2234` · 구간 `0.222` 전부. `citation_hazards.json`
> `HZ-b2o3-md-ea` = **BLOCKED**, *"대체값 없음"*).
> - **사유**: 골격 게이트 실측 — 비-Li 골격의 2–50 ps MSD 로그기울기가 **700 K 이상에서
>   rigid 기준(β<0.30)을 넘었다.** 같은 포텐셜·온도·프로토콜의 modelc·lpsocl 은 1000 K 까지
>   rigid 였다. 문제는 D 가 큰 것이 아니라 **그 숫자가 무엇을 잰 것인지 정의되지 않는다**는 것.
> - ⛔ **σ 비(1.08/0.82/1.15)로 "동등"·"σ 보존" 이라고 쓰지 않는다** — 레지스트리
>   `md-sigma-ratio-v1__NON_CITABLE`(citable:false)이 `statistically_equivalent_transport` ·
>   `conductivity_preserved` · `equivalent_sigma` · 순위 · 기전 · RT 외삽을 명시적으로 금지한다.
>   원자료 축자: ***"미평가 쌍의 '같음' 은 동등이 아니라 구분 실패다."***
>   그리고 그 셋은 **600/800/1000 K** 비이지 **300 K 값이 아니다**(σ300 표기는 오표기).
>   2026-09-08 회수로 **두 계의 셀이 부피 2.00배 달랐다**는 사유가 하나 더 붙었다.
> - ✅ **살아 있는 것 — 마감 카드가 열거한 셋뿐이다**: **밴드갭 1.9671 eV** · **탄성 +13 %**
>   (무도핑 modelc 대비) · **ELF/ICOHP**(B–S 최강 · P–O 신규 motif). ⚠ 이 셋은 0 K DFT 라
>   방향이 MD 와 **반대**(강화·보존)인데, 평균 강성 ≠ 결함 이동도라 둘 다 참일 수 있다 —
>   **이 모순은 미해결이다**(마감 카드 ⚠ 축자).
> - ⚠ **convex hull(+37.5 meV/atom) · phonon 안정성은 UMA(MLIP) 산출물이지 DFT 가 아니고**,
>   BVSE 채널(+45 %)은 정적 결합원자가 기하다. 셋 다 이 마감의 **범위 밖**이지만 마감 카드가
>   살아 있다고 **열거하지도 않았다** — 인용하려면 각자의 근거로 따로 서야 한다.
> - **말할 수 있는 문장은 마감 카드의 `허용_서술_이대로만` 4개뿐이다.**
>
> ⛔ 아래 본문·값은 **이력으로 보존**한다 (kb/SCHEMA.md Update Policy) — 지우지 않는다.
> 축 전체 지도: `kb/methodology/md_axis_status_2026_09_07.md`

# B₂O₃ 도핑 → Li 채널 확장 (BVSE, b2o3 vs LPSCl1.6)

> [!warning] SUPERSEDED (2026-07-09 SEMIFINAL) — ⚠ **이 배너 자체가 2026-09-09 에 정정됐다**
> 본 문서의 **"σ 1.33×" 및 D₀-driven 향상 서사는 철회**됐다 (그 철회는 유효하다).
> ~~멀티시드(3-seed×3-T) 판정: σ비율 1.08/0.82/1.15 = **동등**~~ ·
> ~~순효과는 "σ 보존"(O의 Li–O 트랩 ↔ 채널 개방 상쇄)~~
> ⛔ **이 두 문장도 인용 금지다** — 위 마감 배너 참조. 철회를 다른 철회 대상으로 바꿔 적어 뒀었다.
> 유효하게 남는 것: **BVSE 채널 +45% 확장**(정적 기하) — 0 K 기하라 MD 축 마감 밖이다.
> ~~정본: kb/results/b2o3_SEMIFINAL_report_2026_07_09.md.~~ → SEMIFINAL 도 같은 마감 아래다.
> **정본은 `kb/methodology/md_axis_status_2026_09_07.md`(축 지도) ·
> `db/properties/b2o3_md_closed_retrospective_2026_08_25.json`(마감)** — 카드끼리 가리키면 사슬이 늙는다.

**날짜** 2026-07-02 · **방법** BVSE(Bond-Valence Site Energy) Li 이동 맵. `tools/comp1_v3/bvse_standalone.py`(pure numpy/scipy, CIF→맵, DFT 불필요). BVS(r)=Σ exp((R0−d)/b) over S/Cl/O, BVSE=(BVS−1)². 각 맵 자체 최소값 기준 상대비교.
**데이터** `db/properties/bvse_b2o3/`, `bvse_modelc/` · **그림** `docs/figures/cascade/bvse_channel_volume.png`, `bvse_channel_2p5d.png` · **VESTA cube** `docs/figures/bvse_cubes/*_bvse_aboveMin.cube`(min-subtract, 커밋X·gitignore)

> **한 줄.** B₂O₃ 도핑이 **Li 접근가능 채널 부피를 +45% 확장**(BVSE≤1.0 above-min에서 b2o3 **12.2%** vs LPSCl1.6 **8.4%**). MD(σ 1.33×↑)·Voronoi disorder↑와 같은 방향 — "도핑이 통로를 넓혀 전도 향상"의 **정적 기하 근거**.

## 결과
| | LPSCl1.6 | b2o3 |
|---|---|---|
| 채널 부피분율 (BVSE≤1.0) | 8.4% | **12.2%** (+45%) |
| Li_site BVS 평균 | — | 1.71 (이상 1.0) |
| BVSE percolation 장벽 | 참조 | 낮음(정적) |

## VESTA 시각화 (공정 비교)
- `*_bvse_aboveMin.cube`: 각 맵에서 **최소값을 빼서** 둘 다 0부터 시작 → VESTA에서 **동일 isolevel(~1.0)** 로 열면 절대스케일 차이 없이 공정.
- 노랑 isosurface = 낮은 BVSE = Li 채널. b2o3가 **더 넓고 연결**됨(정량 +45%와 정합).
- 2.5D(min-projection 지형)는 보조 — VESTA "질감"이 직관적.

## 연결·한계
- MD(`b2o3_vs_lpscl16_md`): σ 1.33×↑, D₀-driven. BVSE 채널 확장이 D₀(통로/attempt) 증가의 기하 근거.
- Voronoi(`b2o3_voronoi_disorder`): 전 종 disorder↑. 채널 확장과 같은 "도핑이 격자를 열었다" 서사.
- **한계**: BVSE는 경험적(valence² 단위, 절대 eV 아님). 상대비교·경향용. 절대 장벽은 MLIP-MD/NEB로.
