---
source_url: https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/tree/claude/zip-git-gpu-setup-vdqdtd/degradation-degeneracy
ingested: 2026-08-11
sha256: cbd96bcba30734aec91ffc8f49e3c85ffbebb7cbd3cff916d1b987f12886bed9
---

# 수집 목적: 진행 중 프로젝트의 mothership satellite 등록 (guides/new-project-kickoff.md 의 기존 프로젝트 절차).

# degradation-degeneracy 저장소 감사 (등록용 스냅샷)

감사 시점: 2026-08-11, branch `claude/zip-git-gpu-setup-vdqdtd`, HEAD `c9970ebc`.
이 문서는 mothership 등록을 위한 **당시 상태의 스냅샷**이다. 이후 상태는
`entities/degradation-degeneracy.md` 가 추적한다.

## 무엇을 하는 프로젝트인가
2026-08-05 연구세미나 22p 의 결과(LAM_PE ≈ LAM_NE ≈ 13%, LLI ≈ 17%)가 실제
물리인지, full-cell 곡선 하나로는 두 전극을 가를 수 없어 생긴 fitting
degeneracy 인지 판별한다. 방법: 정답을 아는 PyBaMM 합성 곡선 격자(3,993 조건
의도, guard-feasible 3,069 + infeasible 924)를 만들고, 기존 alpha-beta fitting
이 그 정답을 복원하는지 채점한다.

## 구조 (repo-root 상대)
- `degradation-degeneracy/src/` — baseline(완방상태), modes(열화 모드 override),
  grid(곡선 생성), halfcell(Case 1 기준), fitting(다중시작 최적화), scoring
  (복원가능/degenerate 판정), weight_sweep, io(서명·봉인·validator), config
- `degradation-degeneracy/tools/` — compare_objectives, compare_cases,
  make_results(보고서), check_sweep_consistency, archive_bundle
- `degradation-degeneracy/scripts/` — smoke_e2e.sh(strict 전 구간 스모크),
  archive_results.sh(candidate 승격 보관)
- `degradation-degeneracy/run.sh` — 단일 진입점 (grid/fit/score/wsweep/report...)
- `degradation-degeneracy/docs/` — 01~19: 아키텍처, 감사, 핸드오프, 리뷰 결정,
  08_REVIEW_RESPONSE(발견 대응 원장), 1x_CODEX_*(게이트 리뷰 원문)
- `degradation-degeneracy/configs/` — base/grid_fine/objectives YAML

## 검증 체계 (13 라운드에서 자란 것)
- 서명: grid_run_spec(sig v4 — 조건 ID 집합·완방상태·replay_recipe·
  effective_solver 포함, 행별 서명), fitting run_spec(sig v5), fits_seal
- 봉인: seal_inputs → snapshot_inputs(_inputs/ content-addressed 사본만 읽음)
  → producer view 재검증
- validator: validate_curves_provenance(관측조건 ID결합·행수·x_norm 격자,
  실패라벨 guard 재평가 포함 26개 검사), validate_provenance(fit)
- 보고서: 저장 YAML 이 아니라 정본 fits 재계산 값을 렌더, 불일치는 인용 금지 배너
- 보관: bundle candidate → check → 빈 root 격리 복원 → validator 통과분만 승격,
  artifact_index.yaml(full digest)
- 테스트 277 passed (slow 포함), strict smoke 전 단계 통과

## 리뷰 프로세스 상태
외부 리뷰어(Codex)와 적대적 게이트 리뷰 루프 13 라운드, 발견 F1~F89 + 10~12차
발견들 전부 코드로 대응. 현재 13차 리뷰 요청 발신(대상 c9970ebc), GO 시 V100 에서
baseline --force → halfcell --force --verify → grid_curves_v4 생성(~28분) →
약 10시간 fitting 파이프라인.

## 실행 환경
- 개발: Claude Code 컨테이너 (이 세션), 테스트·스모크 실행 가능
- 본 실행: V100 서버 (CPU fitting, IDAKLU)
- 백업/열람: Windows (archive 복원 검증 완료 — POSIX 경로 정규화)
