# 진행 중 — litdb 정본 4편 작업 (2026-08-19, 압축 대비 스냅샷)

⚠ **커밋 안 된 상태**.  정본 워크트리에서 에이전트들이 쓰는 중이다.

## 워크트리

```
/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/litdb-canon
  = origin/claude/friendly-meitner-lldvar  (로컬 브랜치 tmp-litdb-58, 정본 168편)
```
**커밋·푸시는 `claude/friendly-meitner-lldvar` 로만** (litdb 단일 서랍 규약).  이 리포 `litdb/` 는 동결 스냅샷.
webapp 은 `scripts/litdb_sync.py` 가 `origin/<branch>` 를 **직접 읽으므로 푸시 = 반영**.

## 상태

| | 논문 | 상태 |
|---|---|---|
| A | Wang & Wang, JMCA 2026 (건식 후막 NCM94 실패기전) | ✅ **완료** `papers/wang2026_dryprocess_thick_cathode_failure_ncm94.md` (824줄) |
| B | Weitze/Franco, ESM 2024 (습식 resolved-AM) | 진행 중 — **기존 카드 심화** (`wet_processing_resolved_am_ssb_cathode_manufacturing.md`) |
| C | Alabdali/Franco, JPS 2023 (3D 습식 제조) | 진행 중 — 신규 |
| D | Joule (후막 열화 multiscale imaging + 모델) | 진행 중 — 신규 |

A 가 건드린 파일: 위 카드 · `INDEX.md`(신설 섹션) · `comparison_vs_ours_DEM.md`(+147줄, 6축) · `comparison_vs_ours.md`(+2줄).
⚠ slug 에 `dryprocess` 를 넣어야 webapp `literature_track()` 이 **dem** 으로 분류한다 (없으면 dft 로 오분류).

## A 편 — 살릴 수치 (전부 stated, 논문 실측)

| 값 | 우리 축 |
|---|---|
| **AFM Young's modulus 3.056 / 2.248 / 1.263 GPa** (건식 복합막 3점, Fig S3) | ★ E_eff 방어선 |
| R_s 9.4→8.6 · R_ct1 12.5→**55.4** · R_ct2 83.8→**939.7 Ω cm²** (50 cyc @0.1C) | R_int(N) |
| DRT τ 창: **D1 10⁻⁶–10⁻⁵ = 입자 간 고체-고체 접촉** / D2 10⁻⁵–10⁻² 계면상 이온 / D3·D4 전하이동 | ★ 접촉망 |
| in-situ 스택압 −1.95 MPa (ΔP/P₀ **1.81 %**), 비가역 **1.20 %**, 래칫 **−0.30 MPa/cyc** | A10 |
| 두께 177.3 µm → 127.1–138.9 (300 cyc) = **−21.7 … −28.3 %** | — |
| I(003)/I(104) 1.99 → 1.40 | 벌크 열화 |
| 0.1C 50 cyc **87.1 %** vs 0.5C 50 cyc **98.3 %** (3.5 V) | 시간구동 열화 |

레시피: NCM94(SC 2–4 µm) : **Li₅.₄PS₄.₄Cl₁.₆** : VGCF : PTFE = **80:18:1:1**, 177.3 µm, **6.5 mAh/cm²**, 운전압 110/200 MPa.

## ⛔ A 편이 **못 채운 것** (요청 축 기준 — 중요)

- **σ_e/σ_ion 절대값 = n/a** (복합체 전도도 실측 0건).  ⇒ 우리 SBE 73 / 54.6 mS/cm 는 **검증도 반박도 안 됐다**.
  문헌 밴드 **Lee 2025 34 · Kim 2024 38.6–65.2 그대로 유지**.
- **PTFE ↔ 전도도 = n/a** (1 wt% 한 점).  **Lee 2025 SI Fig 5 가 여전히 유일 곡선.**
- 집전체 계면 = n/a (R_s 에 섞임).  `nam2026_primer_layer` 가 계속 정본.
- porosity·다압력/Heckel·packing/bimodal·G_c/K_IC — 전부 없음.

## 세 판단 (에이전트 질의에 대한 내 답 — 원장에 넣기 전 초안)

1. **AFM 1.3–3.1 GPa 를 E_eff 서사에 어디까지?** → 에이전트가 그은 선(**자릿수 진술만**)이 **맞다, 보수적이지 않다**.
   막 압입 모듈러스와 우리 E_eff(입자 접촉강성 입력, frame[2] lumping)는 **범주가 다르다** — σ_VGCF 에서
   방금 겪은 분말↔단섬유 범주오류(CL-47)와 같은 형태다.  ⇒ "18× 연화가 자의적" 이라는 비판의 **방어선**으로만
   쓰고 **"일치/검증" 금지**.
2. **−1.95 MPa 를 스택강성 없이 A10 에 어떻게?** → **무차원·강성무관 3개만**: ΔP/P₀ 1.81 % · 비가역 1.20 % ·
   래칫 −0.30 MPa/cyc.  Δ부피 환산 금지.  **방향 앵커**(SC 는 충전에 수축)로 등록하고 크기는 안 쓴다 —
   A10 `--poly-mode` 분기(SC=계면 debond / poly=내부 void)를 **셀 레벨에서 지지**하는 것이 값어치다.
3. **시간구동 열화(0.1C 87.1 % vs 0.5C 98.3 %)를 STEP5 에?** → **값어치 있다**.  같은 사이클 수에서
   저율이 더 나쁘면 열화가 **사이클 구동이 아니라 시간(캘린더) 구동**이라는 뜻이고, 그건 STEP5 rate law 의
   **형태**를 바꾼다.  ⚠ 단 1편·1조건이므로 **가설 등록**으로만.

## 다음

1. B·C·D 완료 대기 → 4편 한 번에 검토
2. `claude/friendly-meitner-lldvar` 로 커밋·푸시 → webapp 자동 반영
3. worktree 제거 (`git worktree remove`, 브랜치 `tmp-litdb-58` 삭제)
4. 위 세 판단을 원장(claims.json)에 반영할지 결정

## 병행 — kgy STEP 4 (별개)

vox 0.125 CL-41, 11/16 팔 시점 5쌍 평균 **R = 1.14508** (SE 0.107 %p).  8팔 채우면 판정.
`python3 ~/dem-sk/scripts/sdcp_gain_verdict.py --dir prereg_v2_vox0125_sph_b048_lean2 --collect-only`
