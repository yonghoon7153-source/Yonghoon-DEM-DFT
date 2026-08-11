# Codex 독립 설계리뷰 판정 + 내 검증 (2026-08-11)

> 리뷰 좌표: `origin/claude/stoic-knuth-NObVQ @ 9fb750cb`
> 대상: `plan_vgcf_ptfe_coupling_20260811.md` · `plan_se_grad_20260811.md` ·
> `codex_review_request_…md` · `selfreview_synthesis_…md`
> Codex 는 production 코드를 수정하지 않았고 커밋도 하지 않았다.
> **이 문서는 그 판정 + 내가 직접 재검증한 결과**를 남긴다.  두 계획서는 이 판정으로 갱신됐다.

---

## §1. 최종 판정표

| 항목 | Codex | 반영 후 상태 |
|---|---|---|
| P1 VGCF grade registry | 수정 후 GO | GO — MWCNT `simulation_enabled:false`, grade ID/version 기록, 소비처 6곳 배선 |
| P2 문헌 connectivity | **context-only** GO | 검증 게이트에서 **강등** — 배수 하나를 앵커로 쓰지 않음 |
| **P3 VGCF 상관 배치** | **DROP** | ⛔ **DROP** (production·CLI·결과표에서 제외, backlog 가설로만) |
| SR-01 | 원인 verified / 크기 pending | **P1 로 승격** + 공통모드 범위 축소 |
| SE G4 문서가드 | GO | GO |
| SE G1 (a)형 | REDESIGN 후 GO | band-면적 제약 + 최종 profile 게이트로 재설계 |
| SE G2 (b)형 | **현재안 HOLD** | ⛔ HOLD — **production dead path** |
| SE G3 캠페인 | HOLD | ⛔ HOLD — 선행 3건 |

---

## §2. 내가 **직접 재검증**한 것 (Codex 를 그대로 믿지 않고)

### ① CR-01 — 내 `≤0.35·vox` 수정안 **반증 확인** ★ 가장 중요
직선 섬유 1500개, 현행과 같은 점-스탬프 + 6-face 연결성분으로 독립 재현:

| step | vox 0.4 | vox 0.2 | vox 0.141 |
|---|---|---|---|
| 현행 0.099 µm | 95.7 % 단절 (평균 4.92 성분) | 99.8 % | 100 % |
| **내 수정안 0.35·vox** | **97.5 %** | 99.5 % | 99.7 % |
| 0.10·vox | 77.3 % | — | — |
| 0.05·vox | 51.8 % | — | — |
| **0.02·vox** | **30.7 %** | — | — |

**점 재샘플링으로는 원리적으로 못 고친다** — 선이 복셀 edge/corner 를 지나면 아무리 가까운
두 점도 **face 를 공유하지 않는 대각 셀**에 찍힌다.  Codex 판정(96.35 % @0.35·vox) 과 같은
결론이고, 절대값 차이(97.5 vs 96.35)는 box 크기 등 protocol 차이다 — 그 자체가
"**정확한 % 는 production 상수가 아니다**" 를 다시 보인다.

⇒ 선행 요건 셋 중 하나: ① fibre-ID 보존 **polyline segment supercover + face bridge**
② 직경·복셀 부피분율 기반 **connected-tube rasterizer** ③ (권장) 1D 섬유 `G=σA/L` + 3D AM
복셀 **mixed-dimensional solver**.  ⚠ 26-conn 으로 라벨만 바꾸는 것은 답이 아니다 —
실제 솔버는 **6-face conductance** 를 쓴다.

### ② G2 dead path — **확인**
production `run_mpm.sh` **10개 킷 전부 `--se-dump`** 를 넘긴다 (`grep -ho '--se-dump' … | wc -l`
= 10).  그 경로는 real-SE raster 를 타고, 내 `prob(z)` 계획은 `--se-dump` **없을 때만** 도는
uniform cell-fill `else` 분기다 ⇒ **그대로 구현하면 production 킷에서 죽은 길**.

### ③ se-grad Q2 의 전제 오류 — **확인**
내가 "2D synth 의 **coverage/CN 핀**과 구배가 충돌한다" 고 물었는데, generator 에
**coordination/CN 계산도 핀도 없다** (`grep -cin "coordination|_cn\b|cn_pin|target_cn"` = 0).
**coverage 만** 있다.  질문 자체가 잘못된 전제 위에 있었다.

---

## §3. Codex 가 **내 자체리뷰의 오류**를 잡은 것 (자체리뷰도 틀렸다)

### CR-05 — `1.40–3.58 = 관측창 밴드` 는 **내 통계 렌즈의 오류**
논문은 17.1/61.2 를 "더 큰 창" 효과로 설명하지 않는다.  그것은 **representative connectivity
map** 이고 1.397 은 **같은 volume 의 전 슬라이스 평균비**다 — **집계 함수와 선택 위치가
다른 통계**이지 window-size sweep 의 양 끝이 아니다.  (원자료에서 17.1 % 는 Slurry 분포의
거의 최하단, 61.2 % 는 Dry 상단.)
⇒ 나란히, 각각의 정의와 함께: `1.397`(all-slice descriptive) · `3.579`(representative-map) ·
**둘 다 calibration/validation bound 아님**.  "effect band" 로 묶지 않는다.

### CR-04 — ESS/CI 해석이 과했다
`n_eff 37/25` 는 **lag-1 만 쓴 AR(1) 휴리스틱**.  첫 음수 lag 까지 적분하면 **26.4/17.6**,
구간도 `[1.19, 1.64]`.  더 근본적으로 workbook 에 **독립 reconstruction 수·specimen/volume ID
가 없어** 어느 ESS 로도 **공정 효과의 95 % CI 가 되지 않는다** → `[1.22, 1.60]` 은
**"AR(1) 민감도 구간"** 으로만.  그리고 "명목 n 이 정밀도를 3–5배 과장" 은 부정확 —
3–5배는 `n/n_eff` 이고 **표준오차 배율은 √ = 1.9–2.2배**.
(중앙값비 1.61 을 "Dry 우측 왜도" 로 돌린 것도 부정확 — Dry 는 평균≈중앙값이고, 원인은
**Slurry 의 평균이 중앙값보다 높은 분포형**이다.)

### CR-02 — SR-01 "공통모드 생존" 의 **범위가 너무 넓었다**
공통모드라 부를 수 있는 것은 **같은 fibre geometry 를 고정한 채 σ scalar 만 바꾸는 비교**
정도다.  다음에서는 raster 오차가 **직접 달라진다**: grade 변경(d·L·객체수·stamp inflation) ·
P3 proximity(중복 셀·유령 브릿지가 treatment 와 결합) · `n_grid`/curl/clipping/`in_am` ·
**SBE↔DBE(VGCF 섬유 vs SDCP 입자)** · raster origin/섬유 배향.
⇒ SR-01 은 코드 결함으로는 P2 여도, **grade/P3/첨가제 headline 비교의 과학적 유효성
게이트로는 P1 blocker**.  → 원장에서 **P1 로 승격**.

### CR-03 — self-nucleate 는 물리적 250 nm 노브가 아니다
`E[r] = 1.676·dx_MPM` 이라 **격자 종속**(dx 0.141 → 236 nm, n_grid 2배 → 118 nm).
게다가 **attractor 점↔새 섬유 중심의 offset** 이지 **섬유축 NN 거리**가 아니고, raw 점군에서
attractor 를 뽑아 **긴 섬유·클리핑 후 점 많은 섬유가 더 뽑힌다**(fibre-uniform 아님).
`q>0` 이면 **PTFE 양과 무관**하게 같은 상관을 준다.

### CR-06 — 반증 조건 일부가 반증 가능하지 않았다
P1 의 "기하 SSA ±20 %" = 넣은 지름을 같은 원통식에 도로 넣는 **일관성 검사**.
P2 의 f_perc 비교 = **비동등 지표 강제**.  P3 의 두-vox 부호 일치 = **reference truth 부재**
(두 격자가 같은 방향으로 틀릴 수 있다).  → 셋 다 계획서에서 교체/강등.

---

## §4. Q1–Q5 최종 답 (Codex, 내가 동의)

- **Q1 P3**: **DROP.** default-off 는 과학적 식별 문제를 풀지 않는다.  §2-① 이 닫히고
  새 물리 필요가 생길 때만 **새 설계로** 재승인.
- **Q2 VGCF 기본 등급**: **유지.**  `vgcf_h_legacy` 기본 + `vgcf_hi_ar` opt-in.
  Stage 22.5 의 LOOCV 는 **기존 표현 안의 적합도**이지 sub-voxel 기하의 물리적 타당성 증명이
  아니다 — 둘을 분리해 서술.
- **Q3 P2 앵커**: **context-only.**  검증 게이트 아님.
- **Q4 PTFE §F1**: **계속 open.**  CGMD 의 ~1 µm 는 fibrillation **이전**, 우리 0.25/40 은
  **이후** 프록시.
- **Q5 SSA↔#30**: **정성 가설로만.**  고정 문구 = *"…transferable qualitative design
  hypothesis; …not a quantitative degradation law for the resolved carbon–SE interface."*

---

## §5. 다음 실제 작업 (승인 대기)

1. **G4** se-grad 문서 가드 (무해, 즉시 가능)
2. **P1** grade registry (legacy 기본 고정 + metadata + 소비처 배선 + MWCNT 비활성)
3. **P2** 출처 기록 (1.397 / 3.579 각각의 정의, 공정 CI 없음)
4. **★ SR-01**: 실침대 A/B + **직경-aware segment 프로토타입** — 이것이 P3·grade 비교·
   첨가제 headline 전부의 잠금을 푸는 열쇠다
5. **G1 재설계** (band-면적 제약 + 최종 profile 게이트) → SG-01/03 readout·provenance 배선
6. G2 는 격리 experimental mode 스모크까지 · G3 는 wt%→vol%·finite interface·matched
   thickness 준비 후

⚠ Codex 의 GO 는 **설계 조건부 승인**이며 결과 검증이 아니다 (그쪽 문서 §8 명시).
