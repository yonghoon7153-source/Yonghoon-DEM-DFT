# 믹서 고-Bo 강성 축 — DEV 덱 v2.6 (×20 · ×40) · 되읽기 증거 (2026-09-30 밤)

**등록 개정 v2.6 (1저자 비준 *"권고하는걸로"* · `docs/reviews/mixer_highbo_stiffness_prereg_20260929.md` 개정 이력)**: E_ref = SE **×20** · E_ref2 = SE **×40** (옛 v2.5 ×14 · ×28 = `docs/data/mixer_highbo_dev_decks_20260930/` — 이력 · ibb DEV7 ① 이 실제로 돈 덱).
근거 = DEV7 (×14) E0 다섯 실측: 최대 겹침이 SE 낀 쌍 (AM_P–SE · SE–드럼) 이고 옛 soft 덱 대비 비 5.66–6.4 ≈ Hertz 평형 14^(2/3) = 5.81 → seed 67867967 이 1.018 % > 1 % (§4 a 실패) ⇒ ×20 이면 예측 0.80 % (여유 20 %).  soft 진단 범위 = 1 % × 20^(2/3) = **7.37 %** (옛 5.8).

같은 `build.sh` (경로 · 배수만 다름 · 생성기 CLI 바이트 재현 확인) — `bash docs/data/mixer_highbo_dev_decks_20260930_v26/build.sh` · `sha256sum -c …/SHA256SUMS` (55 줄).

| 폴더 | 무엇 |
|---|---|
| `decks/` 7 | DEV 실행 대상 (E0_ref ×3 seed · E0_ref2 · E0_ref_dthalf · LC_ref_r2 · LH_ref_r2) — 다음 = 런처 `dev-e0` (새 OUT) |
| `compare/` 5 | soft 대조 (E0 셋 = 09-28 실행 덱과 바이트 동일 — sha 앞 16 대조 그대로) |
| `check_only/` 2 | ×40 LC · LH 2 바퀴 검산 전용 |

| 되읽기 (`readback.md` · `readback.json`) | 13/13 표 PASS — E · E0 (soft → ×20 · soft → ×40) 의 E* 배수 · CED 배수가 **우리 산술** 표 (`mixer_deck_readback.CODEX[20.0 · 40.0]` = Codex 7 차 ×14 · ×28 값을 9 자리로 재현하는 같은 식) 와 일치 · ×20 → ×40 (F 2) 은 표 없음 = F₀ 보존만 (N/A) · DT · B PASS |
|---|---|
| 덱 비교 (`deck_diff.txt` · `deck_diff.json`) | 15/15 PASS (`--allow E · EB · B` · `--expect-deck` = 같은 명령 재생성) |
| E0 시간 계획 | ×20: dt 0.262 µs · run 518,714 × 2 → 덤프 **1,037** 장 (≈ 14.5 GB) · ×40: dt 0.1853 µs · 1,467 장 (≈ 20.5 GB) · dt/2: 2,000 step 간격 1,037 장 — 옛 ×14 867 · ×28 1,227 |

⚠ Codex 10 차 검산 대상: ×20 · ×40 배수표는 Codex 가 직접 낸 값이 아니다 (우리 식 · Codex 7 차 값 재현 근거).  이 증거는 덱 텍스트 계약이다 — 실행 · 완주 · 접촉 상태는 ibb `dev-e0` 뒤.
