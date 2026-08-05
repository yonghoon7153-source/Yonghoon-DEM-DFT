# Progress

각 Phase 완료 시 체크하고 git tag를 남긴다. 상세는 `04_PROMPTS.md` 참조.

- [x] Phase 0 — 스캐폴딩 · 환경          `phase0-done`   ← 이 zip이 여기까지
- [ ] Phase 1 — 코어 리팩터링             `phase1-done`
- [ ] Phase 2 — 모드 중첩 · 32p 재현      `phase2-done`
- [ ] Phase 3 — 조합 격자 · 병렬화        `phase3-done`
- [ ] Phase 4 — Fitting 이식              `phase4-done`
- [ ] Phase 5 — 축퇴 판정 · 지도          `phase5-done`
- [ ] Phase 6 — 목적함수 비교             `phase6-done`
- [ ] Phase 7 — GPU 시도 (선택)           `phase7-done`

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
