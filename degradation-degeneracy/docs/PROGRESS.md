# Progress

각 Phase 완료 시 체크하고 git tag를 남긴다. 상세는 `04_PROMPTS.md` 참조.

- [x] Phase 0 — 스캐폴딩 · 환경          `phase0-done`
- [x] Phase 1 — 코어 리팩터링             `phase1-done`
- [x] Phase 2 — 모드 중첩 · 32p 재현      `phase2-done`
- [x] Phase 3 — 조합 격자 · 병렬화        `phase3-done`  ← 2026-08-05 여기까지 완료
- [ ] Phase 4 — Fitting 이식              `phase4-done`
- [ ] Phase 5 — 축퇴 판정 · 지도          `phase5-done`
- [ ] Phase 6 — 목적함수 비교             `phase6-done`
- [ ] Phase 7 — GPU 시도 (선택)           `phase7-done`

## Phase 1~3 완료 내역 (2026-08-05)

- [x] Phase 1: src/{config,model,baseline,protocol,runner,curves,io}.py
      — C1(완방 자동산출: Gr=36.6/Si=3446.1/PE=58439.9), C2(전역 param 제거),
      C3·C4(경로 정리). slow 테스트 3종 통과.
- [x] Phase 2: src/{modes,sweep}.py + tools/plot_sweep1d.py
      — 32p 6-panel 재현 (results/sweep1d_v1), 원본 update_fn 1:1 회귀 테스트,
      reference ≡ LLI=0 (Q_ref=5621.1 mAh 일치).
      physics: lam_pe_de 프로토콜 매핑 원본 기준으로 정정(discharge_first).
- [x] Phase 3: src/grid.py — coarse 125조합 (grid_coarse_v1):
      95 solve 성공(실패 0) + 30 PE-limited 사전판정(failed.csv),
      4코어 IDAKLU ≈ 1.2분, kill 후 --resume 재개 검증 완료.
- 테스트: 51개 (fast 48 + slow 3) 전부 통과.

## Phase 0 완료 내역

- [x] 디렉터리 구조
- [x] `.gitignore`, `requirements.txt`, `requirements-gpu.txt`
- [x] `scripts/verify_env.py` — IDAKLU / composite DFN / GPU 검증 + solve 벤치마크
- [x] `run.sh` 인자 파싱 (verify만 동작, 나머지 NOT IMPLEMENTED)
- [x] `configs/base.yaml` — 원본 `initialization()` 10개 값 1:1 대조 완료 (불일치 0)
- [x] `configs/{sweep1d,grid_coarse,grid_fine,objectives}.yaml`
- [x] `reference/degrade_mode_sim_original.py` — 회귀 검증 기준본

## 남은 것 (Phase 1 진입 전 확인)

- [ ] `git init` 후 첫 커밋 + `git tag phase0-done`
- [ ] `./run.sh --mode verify` 실행 → `docs/ENV_REPORT.md` 생성
- [ ] IDAKLU 가용 여부 확인 (안 되면 casadi fallback을 매니페스트에 기록)
