# LHS coverage 5번 배치 — 수확 v3 재수확 + 웹앱 `--stop-after coverage` — 130 (lhs) · 64 (lhsx) · 봉인 `1e09f661d` · 2026-09-30 ~ 10-01

이 README 는 네 폴더를 함께 설명한다: `lhs_descriptors_cov_1e09f661d/` · `lhs_webapp_coverage_1e09f661d/` · `lhsx_descriptors_cov_1e09f661d/` · `lhsx_webapp_coverage_1e09f661d/`.

- **원본 (1저자 WSL `~/dem-audit`)**: `lhs_cov_1e09f661d.tar.gz` — **849,828 B · sha256 `e7d649f58fc08e0e976e1036dc43136748c0b7192fd6b77aad562fba77e08ea0`** (1저자 WSL 출력 = 업로드본에서 다시 계산한 값) ←
  이 네 폴더의 내용 그대로 (200 파일 = 수확 JSON 130 + 64 · `_batch_summary.json` 2 · `metrics_flat.csv` 2 · `status.json` 2 · 줄 끝 LF · 변경 0).
- **코드 = 봉인 `1e09f661d`** (Codex 재검증 5 GO 19 커밋 병합 뒤 · 전체 게이트 통과).  웹앱 배치 `status.json` runs:
  LHS #1 09-30T23:06:19 `dirty=false` (스모크 `lhs00_000`) · #2 23:52:45 `dirty=true` (129 건) · lhsx #1 23:07:19 `dirty=true` (`lhsx_001`) · #2 10-01T01:18:27 `dirty=true` (63 건).
  ⚠ **`dirty` 원인 = 코드 변경이 아니다** — 1저자 WSL `git status` · `git diff` 에서 바뀐 추적 파일은 `docs/figures/physics_regime/coverage_hertz_vs_physics_summary.csv` 하나였다:
  피복 단계 (`scripts/coverage_physics_vs_hertzian.py` 의 요약 CSV 쓰기) 가 **실행 위치 기준**으로 그 추적 파일을 매 케이스 덮어쓴다 → 첫 케이스 뒤부터 dirty (원장 `LHS-27`).
  수확기 `_batch_summary.json` 에는 코드 출처 필드가 없다 (디렉터리 이름만 `1e09f661d`).
- **옛 기준선 대조** (`*_20260929` · 보고서 `docs/reviews/lhs_coverage_batch5_comparison_20261001.md`): 수확기 기존 키 30,446 + 14,956 칸 중 차이 = 규칙 문자열 +
  `wall_touch` 39 칸 (정확 접선 11 입자 · 벽 규칙 통일 = 의도된 변경) 뿐 · 웹앱 공통 열 232 · 231 전부 **문자열 동일** · 수확기 ↔ 웹앱 porosity ≤ 2.5e-10 %p ·
  Hertz 계열 (기하면적) 피복 ≤ 1.4e-14 %p · 두께 · 상 개수 차이 0.
- **새 양**: 수확기 `coverage_wall_split` · `contact_area_check` · `coverage_wallexcl_*` · `contact_gate` · 웹앱 legacy Physics 40 열 · physics v2 39 열 (미검증 후보 · `LHSC-10`) ·
  7a 전체 AM–SE 배위수 분포 `am_se_cn_{std,median,max}`.
- **합리성 검사** = `docs/reviews/lhs_coverage_reasonableness_20261001.md` (계산 결함 신호 0) · 분석 스크립트 `docs/reviews/lhs_coverage_reasonableness_20261001/`
  (이 폴더들만 읽어 보고서를 바이트 그대로 다시 만든다).
- **쓰임 (J20-m · 1저자 10-01)**: 인계 coverage = 기하면적 열만 · physics v1 · v2 · rough 는 인계 안 함 (접촉별 추정 면적 합에 표면 한도가 없어 포화 · v2 분모 붕괴 · `LHS-25`).
  7c (AM 고립 · AM–SE 배위수) 는 이 폴더의 웹앱 열에서 읽는다.
- ⚠ **세대**: 봉인 뒤 바뀐 웹앱 코드 (① `a9f310769` · ②-a `f3cb141ae` · ②-b · ③ `90c6c9670`) 는 이 산출물에 **없다** — 웹앱 φ 빈칸 13 (τ 없으면 φ 안 내던 세대 · `DESC-01`) ·
  union · 숫자형 저장 등.  HEAD 웹앱으로 다시 돌리면 그 열들이 달라진다 (의도된 변경) · 세대를 한 표에 섞지 말 것.
