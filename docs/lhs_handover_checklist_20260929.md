# LHS 인계 체크리스트 — 확보할 것 · 넘겨줄 것 (2026-09-29 · 1저자 요청 *"체크리스트 만들어서 확보할 거 · 넘겨줄 거로 나눠서"*)

정본은 `docs/reviews/lhs_handover_judgments_20260924.md` (J19 · J20 · J20-a · J20-b · J20-c) 이고, 이 파일은 **보기 쉬운 지도**다.  상태가 바뀌면 여기 표를 같이 고친다.

## 0. 이번에 뽑는 것 (2026-09-30 · 1저자 *"porosity - union · thickness · AM · SE 분율 · 계면 개수 — 체크리스트 잘 채워나가"*)

순서 규칙 (1저자 09-30): **코드 갱신 → 같이 확인 → 그 묶음만 실행 → 표에 싣기**.  같이 확인하지 않은 열은 표에 싣지 않는다.
09-29~30 WSL 실행분 (수확 v3 · 접촉만 배치 · 코드 `4b42179ec`) 은 **옛 코드 기준선**으로 보관하고, 수정 코드 결과와 비교한다 (1저자 *"그대로 두고 … 비교"*).

| 뽑을 열 | 코드 확인 | 값 | 표 | 남은 것 |
|---|---|---|---|---|
| porosity union `porosity_union_exact_pct` (+ `se_rich`) | ✅ J19 ① | ✅ union TSV (130 + 64) | ✅ 들어 있음 | — |
| 두께 `thickness_mass_conserving_um` | ✅ J19 ② | ✅ | ✅ 들어 있음 | — |
| AM · SE 분율 `phi_am_mass_conserving` · `phi_se_mass_conserving` (라) | ✅ J20-e | ✅ (새 계산 없음 · 닫힘 ≤ 3.3e-16) | ✅ 들어 있음 | — |
| **계면 개수** `area_<쌍>_n` (쌍 종류별 접촉 **개수**) | ✅ **09-30 `calc_interface_area` 검토** (`dem_analysis_core.py:131–168` · 코드 수정 불요 · 약점 1 = 없는 id 의 행을 조용히 버림 → 64 는 재수확의 고아 행 수로 확인) | ✅ 130/130 · 64/64 done (09-30 · 1차 `4b42179ec` + mono 재실행 `27933b44e` · 원자료 `docs/data/lhs_webapp_contact_20260929/` 외 3 · README) | ✅ `lhs_handover_20260930.csv` 130×133 · `lhsx_handover_20260930.csv` 64×135 (새 열 12 = `area_<쌍>_n` 7 + 상태 2 + QC 3 · 옛 칸 변경 0 · bimodal P+S = 전체 100/100 · 48/48) | ✅ **bimodal 의 없는 쌍 = 0** (J20-h · 09-30 비준 · 웹앱은 접촉 0 인 쌍의 키를 안 만든다 → 생성기가 0 으로 채움 · 130 에서 3 · 64 에서 6 칸 · 107/107) · mono AM–AM 개수는 상별 칸이 비어 표에 없다 (`am_am_n_contacts` 검토 뒤) |
| **SE–SE 배위수** `se_se_cn` · `se_se_cn_std` | ✅ **09-30 `calc_se_se_cn` 검토** (`dem_analysis_core.py:232–344` · 코드 수정 불요 · SE 전 입자 평균 (접촉 0 · 벽 입자 포함) · 표준편차 = 모집단 · 같은 함수의 `_perc` · `_eff_area` · `_aug` 8 열은 ② · ⑦ · ⑤ 차례) | ✅ 같은 배치 130/130 · 64/64 · 평균 = 2 × `area_SE_SE_n` / SE 입자 수 — **194/194 차이 0** | ✅ `lhs_handover_20260930.csv` 130×135 · `lhsx_handover_20260930.csv` 64×137 (새 열 2 · 옛 칸 변경 0 · 배치 원값 그대로 · 생성기 항등식 관문 J20-i) | 벽 효과 주의 (열 사전 그대로) — 같이 볼 `wall_touch_frac_*` 는 수확기 item 4 병합 뒤 · ⚠ F1 근접쌍 (`_aug`) 주기 경계 결함 `LHS-22` (⑤ 차례) |
| **AM–AM 배위수** `am_am_cn` · `am_am_cn_std` · `am_am_n_contacts` | ✅ **09-30 `calc_am_am_cn` 검토** (`dem_analysis_core.py:347–375` · 코드 수정 불요 · AM 전 입자 평균 (P–S 교차 · 접촉 0 포함) · 모집단 표준편차 · 접촉 총수 = Σ/2 · 면적 둘은 ⑦ 차례) | ✅ 같은 배치 · 접촉 총수 = AM–AM 쌍 개수 합 · 평균 = 2 × 총수 / AM 입자 수 — **194/194 차이 0** | ✅ 130×138 · 64×140 (새 열 3 · 옛 칸 변경 0 · 원값 그대로 · 관문 둘 J20-j) · **mono 의 AM–AM 개수가 돌아온다** (30 · 16 행) | 벽 효과 (큰 AM_P) · 접촉 수는 총량 |

⚠ **mono (2-type) 의 쌍 이름** — 웹앱은 AM 이 한 종류인 덱의 AM 을 **반지름**으로 AM_S/AM_P 라 부른다 (J20-f) ⇒ mono 의 `area_AM_S_SE_n` 같은 **상별 쌍** 칸에 값이 들어가고,
설계 상과 이름이 다른 9 건 (130: `118 · 121 · 124 · 125 · 126` · 64 예측: `lhsx_003 · 017 · 048 · 062`) 은 설계와 다른 이름 칸에 들어간다.  **총량 쌍** `area_AM전체_SE_n` · `area_SE_SE_n` 은 이름과 무관.
~~✅ **저자 결정 09-30 = (A)** — mono 의 상별 쌍 칸은 빈칸 (coverage 상별 열과 같은 규약) · 총량 쌍만 싣는다 (구현 J20-g · 수확 JSON `n_types` 로 판별 · 없으면 거부).~~
✅ **개정 09-30 저녁 = (B) (J20-k · 1저자 *"인계할때는 중복되더라도 잘 채워서"* · 7b 구현)** — mono 의 상별 칸은 **설계 상 칸** (`block`) 에 단일 AM 값을 싣는다:
이름이 다른 9 건 (실측 130: `118 · 121 · 124 · 125 · 126` · 64: `lhsx_003 · 017 · 048 · 062` — 예측과 같다) 은 설계 이름 칸으로 옮기고 웹앱 이름을 `wa_mono_phase_name_webapp` 에 남긴다 ·
설계에 없는 상의 칸은 빈칸 (N/A) · 수확기 열 (coverage 상별 · `n_AM_*_measured` · `cov_*_n_valid` · 벽 접촉) 도 같은 규칙 · 설계 block ↔ 수확 모양이 어긋나면 거부.

## 1. 한눈에 — 지금 어디까지 있나 (2026-09-29 밤 · 09-30 갱신 표시)

저장된 파일 = **`docs/data/lhs_handover_20260930.csv` (130 행 × 139 열)** · **`docs/data/lhsx_handover_20260930.csv` (64 행 × 141 열)** + 각각의 열 사전 `*_columns.tsv` —
09-30 저녁 J20-k (B) (mono 설계 상 칸 · 7b) 로 다시 만들었다 (바뀐 옛 칸 = mono 행의 상별 칸만 240 · 128 · 새 열 `wa_mono_phase_name_webapp`).  09-29 판 (121 · 123 열 · (라) φ) ·
옛 판 `lhs_handover_20260928.csv` (119 열) 는 이력으로 둔다.
64 는 수확 (`docs/data/lhsx_descriptors_20260925/`) + union (`docs/data/lhs_union_20260927/lhsx64_union.tsv`) + 변환 설계 (`docs/data/lhsx_design_adapted_20260929.csv`) 로 같은 생성기에서 만들었다.

| 묶음 | 130 건 | 64 건 (lhsx) | 넘길까 |
|---|---|---|---|
| 설계 값 (입경 · 조성 · RVE · 하중 …) | ✅ 저장 | ✅ **변환됨** (`scripts/lhsx_design_adapter.py` · 130 전용 추정 열 10 은 없음 · lhsx 원래 값은 `lhsx_*` 열로 같이) | ✅ |
| **두께** `thickness_mass_conserving_um` (+ wall gap · envelope 는 내부) | ✅ 저장 | ✅ 저장 (25.0–44.7 µm) | ✅ |
| **porosity union** `porosity_union_exact_pct` + `se_rich` 표지 | ✅ 저장 | ✅ 저장 (5.43–9.43 % · se_rich 64/64) | ✅ **union 만** |
| φ_SE · φ_AM (구 부피 합 규약) | ✅ 저장 | ✅ 저장 (φ_SE 0.52–0.92) | ✗ **내부 표에만** (§6) — 분모가 넘기는 두께가 아니라 DEM 판 간격이라 union porosity 와 안 닫힌다 (합 > 1 : 130 중 18 · 64 중 60) |
| **φ_SE · φ_AM 질량 보존 (라)** `phi_se_mass_conserving` · `phi_am_mass_conserving` | ✅ 저장 (φ_SE 0.079–0.474 · φ_AM 0.422–0.715) | ✅ 저장 (φ_SE 0.476–0.798 · φ_AM 0.143–0.449) | ✅ **이것을 넘김** (1저자 09-29 밤 *"(라) 에 해당하는 것만"*) — union porosity 와 닫힘 잔차 ≤ 3.3e-16 · 적재량 = 레시피 |
| coverage (AM_P · AM_S · 전체 · 이름은 hertz 지만 A_dem_geometric) | ✅ 저장 (mono 30 은 ~~P · S 둘 다 빈칸~~ → 09-30 (B): 설계 상 칸에 전체 값 · 없는 상 빈칸) | ✅ 저장 (mono 16 도 같음) | ⏸ **09-30: 코드 갱신 중이라 이번 추출에서 뺀다** — 수확기 coverage 4 커밋 (벽 규칙 하나 · 벽 분할 · 면적 대조 · 접촉 행 문) · cap v2 3 커밋 모두 **미병합** · 하나씩 같이 본 뒤 (item 4 설명 끝 · 비준 대기) → ✅ 09-30 밤 **병합** (Codex 재검증 5 GO) · 값은 5번 배치 뒤 · v2 = 미검증 후보 (`LHSC-10`) |
| τ (굴곡도) | 상태 열만 · 값은 보류 (`LHS-08` 14/130) | ⬜ | ⏸ 벽 기준 τ 판정 뒤 |
| **① 접촉 위상** — z_SE-SE mean·σ · z_AM-SE · AM_P/AM_S–SE CN · surface-weighted · z_AM-AM · 접촉 수 · 벽 접촉 비율 | 09-30 WSL 접촉만 배치 (옛 코드 기준선 `4b42179ec`): done 100 · mono 30 REFUSED → 재실행 대기 | 진행 중 (mono 16 거부 예상) | **함수마다 같이 확인한 열만**: 계면 개수 ✅ (09-30) → SE–SE CN ✅ (09-30 · J20-i) → AM–AM CN ✅ (09-30 · J20-j) → AM 고립 (am_se_cn_*) 검토 ✅ · 싣기 ⏸ coverage 뒤 (J20-k) · 벽 접촉 비율은 수확기 item 4 (벽 규칙) 병합 뒤 |
| **② 퍼콜레이션** — percolation_pct · n_components · n_large · electronic_*_fraction · se_se_cn_*_perc | ⬜ 계산 전 (감사 ✅ 적격 · 비관통 24 건은 빈칸) | ⬜ | ✅ ① 다음 |
| ③ φ_SE(웹앱) · ④ 협착 저항 · σ_VM · ⑤ F1 근접쌍 · ⑥ Auerbach · ⑦ A_dem_geometric | 감사 전 | — | ⛔ 감사 끝나기 전엔 안 넘김 |
| 내부 전용 — sphere-sum porosity 4 종 · 두께 wall gap/envelope/pushback · 경계 QC · sha · 상태 열 | ✅ 저장 | ✅ 저장 (hold NEGATIVE_POROSITY 60 = 구 부피 합의 음수 · union 은 전부 양수) | ✗ 내부 표에만 |

⚠ **mono 케이스 (130 중 30 · 64 중 16)** — 2-type 덱은 AM 이 한 종류라 수확기가 상을 `AM` 으로만 라벨한다 (P · S 는 반지름으로 붙인 이름).  그래서 `coverage_AM_P` · `_AM_S` 가
**둘 다** `N_A_PHASE_ABSENT` (빈칸, 0 아님) 이고 값은 `coverage_AM_total_hertz_pct` 에 있다.  같은 이유로 `n_AM_P_measured` · `n_AM_S_measured` 가 둘 다 빈칸이라 **실측 AM 개수가 인계표에 안 실린다**
(수확 JSON `phase_counts.AM` 에는 있다) — 원장 `LHS-21` · ~~생성기에 `n_AM_measured` 열 추가~~ → ✅ **09-30 (B) 로 해소 (7b)**: 새 열 대신 설계 상 칸
(`n_AM_P_measured` 또는 `n_AM_S_measured` · `block` 이 정한다) 에 `phase_counts.AM` 을 싣는다 · coverage 상별도 같은 칸에 전체 값 (130 mono 30 · 64 mono 16 전부 채워짐).

## 2. 확보할 것 (할 일 · 순서대로)

| # | 할 일 | 누가 | 상태 |
|---|---|---|---|
| 1 | ② 감사 산출물 반입 — `~/lhs_perc_audit_20260929/perc_audit.tsv · .json` 보내기 → `docs/data/lhs_perc_audit_20260929/` 커밋 | 사용자 → 나 | ⬜ |
| 2 | **재수확 v3** (130 + 64 · 벽 τ · 벽 접촉 비율) — WSL 명령 = J20-c · **한 건 먼저** (`--case lhs00_000` · `--case lhsx_001`) | 사용자 (WSL) | ✅ 09-30 실행 130/130 · 64/64 (**옛 코드 기준선** — 수확기 coverage 수정 병합 뒤 다시 · 비교) · ⬜ 병합 코드 (09-30 밤) 로 **새 디렉터리** 재수확 = 5번 |
| 3 | **웹앱 배치 — 묶음별** (1저자 09-29 밤 *"단독적으로 하나씩"*): ① = `--stop-after contact` (접촉 분석 단계 — ⚠ 이 단계는 웹앱 분석 14 가지를 **한꺼번에** 돈다 (`run_full_analysis`) · 표에는 같이 확인한 열만) → 한 건 대조 → 130 + 64 · ② 이후는 그 묶음 차례에 | 사용자 (WSL) | ✅ 코드 · ✅ 한 건 대조 · ▶ 09-30 전 건: 130 done 100 · mono 30 REFUSED (`SELF-66` · J20-f · 관문 수정 `70e1203be`) · 64 진행 중 |
| 3b | **REFUSED 재실행** — 같은 두 배치 명령 · 같은 `--out-dir` (done 은 건너뛴다) → tgz | 사용자 (WSL) | ✅ 09-30 (인계표 `wa_status` = done 130/130 · 64/64 — 이 줄의 ⬜ 는 09-30 낮까지 낡아 있었다) |
| 4 | 생성기 코드 — ✅ `--webapp-groups contact` (09-29 밤 · 95/95) · ~~64 설계 변환 어댑터~~ ✅ (14/14) · ✅ φ (라) 두 열 · ✅ **확인된 열만 싣기** (J20-g `WA_REVIEWED` · 지금 계면 개수 `area_<쌍>_n` + SE–SE CN 두 열 (J20-i) + AM–AM CN 세 열 (J20-j) · 항등식 관문 — 함수 검토가 끝날 때마다 늘린다) · ~~✅ mono 상별 빈칸 (J20-f (A))~~ → ✅ **mono 설계 상 칸 (J20-k (B) · 7b · 09-30 · 137/137)** · 배포 프로필 (`--deliver`) ⬜ · ~~`n_AM_measured` (`LHS-21`) ⬜~~ ✅ (B) 로 해소 | 나 | 일부 ✅ |
| 4b | **접촉 단계 함수 검토 (1저자와 하나씩)** — 계면 개수 ✅ (09-30) → SE–SE CN ✅ (09-30 · `calc_se_se_cn` · J20-i) → AM–AM CN ✅ (09-30 · `calc_am_am_cn` · J20-j) → AM 고립 ✅ (09-30 · `calc_am_isolation_risk` · J20-k · 대조 전부 차이 0 · **7a ✅** 웹앱이 전체 분포 3 열을 내보냄 · **7b ✅** 생성기 (B) — 130×139 · 64×141 · 7c ⏸) · 나머지 분석 (굴곡도 · von Mises · 접촉력 · 압력 · 겹침 · 유효 전도도 · Auerbach) 은 그 묶음 차례에 | 나 → 1저자 | ✅ 4/4 검토 (싣기는 7c) |
| 4c | **coverage 코드 갱신 (에이전트 산출 · ✅ 09-30 밤 병합)** — 수확기 4 커밋 (`worktree-agent-a8425b12f9b01f5bb`) · cap v2 3 커밋 (`worktree-agent-a308bd30eb1820cd1` · 배치 selftest 번호 충돌 1 곳 · 새 결함 등재 필요: 옛 피복 스크립트가 `WEBAPP_*_FOLDER` 무시) → 하나씩 설명 · 비준 뒤 병합 → 재수확 · coverage 배치 → 기준선과 비교 | 나 → 1저자 | ▶ item 4 설명 끝 · 비준 대기 · ⛔ **Codex 판정 09-30 = 묶음 전체 HOLD · 새 P1 2 · P2 3** (`docs/reviews/codex_lhs_coverage_verdict_20260930.md` · 증거 `codex_lhs_coverage_evidence_20260930/` · 원장 `LHSC-01`~`10` · Codex 가 본 트리 = `da4670594` + 패치 7 = 우리 `64ae3cba8` 8 파일 바이트 동일 · 우리 트리 재현 네 스크립트 전부 일치) — GO 4 (0001 벽 규칙 · 0002 벽 제외 = 분모 보정 proxy 로만 · 0004 접촉 문 · 0005 v2 면적 함수 = 후보 연산자) · HOLD 3 (0006 P1 v2 분모 무효 → 0.0·ok · 0007 P1 atoms-only 가 `stop_after=coverage` 우회 · 0003 P2 허용폭 경계 + AST 우회) → ✅ 09-30 수정 4 커밋 (검토 브랜치 `aba311054` · `471ad778b` · `c125254a9` · `002cc2881` · 반례 먼저 · (a) 빈칸 계약 · (a) `lens_geometry` 분리 · Codex 스크립트 재실행 = 기대대로) → ✅ Codex 재검증 발송 → ⛔ **재판정 09-30 밤 = HOLD** (`codex_lhs_coverage_reverify_verdict_20260930.md` · P1 두 건 닫힘 · 새 P1 없음 · `LHSC-01` · `02` · `05` · `06` 닫힘 · `LHSC-03` R2 (스키마 결손 · 모순 통과) · `LHSC-04` R2 (범위 안 반올림 오탐 1.332) · 0008 · 0011 GO · 0009 · 0010 HOLD · 우리 재현 전부 일치) → R2 · R3 · R4 · R5 수정 (반례 먼저 · 패치 0012–0019) · 재검증 2–4 = HOLD (새 P1 없음 · P2 잔여 계열 · 상세 CLAUDE.md LHS 행) → ✅ **재검증 5 = GO (09-30 밤 · `docs/reviews/codex_lhs_coverage_reverify5_verdict_20260930.md`)** → ✅ **병합 (19 커밋 0001 → 0019 · `15ecbbc9a` … `9514b851a` · 검증 바이트 대조 · Codex 스크립트 병합 트리 재현 판정값 차이 0 · 원장 LHSC-01~06 verified · 07~10 · 11 (P3) 열림)** → ⬜ 5번 새 디렉터리 재수확 v3 + `--stop-after coverage` 배치 (봉인 커밋) → 옛 기준선 비교 · LHSC-08 · 09 · 10 보고 |
| 5 | 인계표 재생성 130 + 64 → 열 사전 (`*_columns.tsv`) → 커밋 · ① 열 설명을 열 사전에 그대로 | 나 | ⬜ (2 · 3 · 4 뒤) |
| 6 | 결정 셋 — `LHS-20` (top_reachable_pct · ionic_active_pct 넘길지) · ② 열 사전 문구 (J20-b ⓒ) · 배포 프로필 (§3) | 사용자 | ⬜ |
| 7 | ② 열 저장 (같은 배치 산출에서) → ③ φ_SE 감사 → ④ → ⑤ → ⑥ → ⑦ (묶음마다 감사 → 저장) | 나 | ⬜ 순서대로 |
| 8 | τ — 벽 기준 τ 새 열 판정 (`LHS-08`) → 넘길지 결정 | 나 → 사용자 | ⬜ |

## 3. 넘겨줄 것 (배포 묶음 · 제안 — ⬜ 비준 ⓒ)

| 파일 | 내용 |
|---|---|
| `lhs_handover_<날짜>.csv` (130) · `lhsx_handover_<날짜>.csv` (64) | **09-30 이번 판 = §0** (설계 + 두께 (mass-conserving) + porosity union + `se_rich` + φ_SE · φ_AM (라) + 계면 개수 + SE–SE CN + AM–AM CN).  그 뒤 같이 확인하는 대로: ① 나머지 열 → coverage (갱신 뒤) → ② 퍼콜레이션 → ③~⑦ |
| `*_columns.tsv` (열 사전) | 열마다 출처 · 판정 · 뜻 · 분모 · 주의 (벽 효과 · 파생 · 총량 · 빈칸 = N/A) |
| README | 규약 한 줄씩 — union 은 상한 규약 · 구 부피 합은 안 넘김 · τ 보류 · 64 는 SE-rich (SE/고체 0.51–0.85) |

**안 넘기는 것**: sphere-sum porosity 와 그 변형 4 종 (겹침 이중계상 · SE-rich 에서 음수) · 감사 전 묶음 ③~⑦ · τ 값 (판정 전) · 내부 QC · 상태 열.

## 4. 왜 porosity 는 union 만 넘기나 (1저자 09-29 *"union 정도만"*)

- 구 부피 합 (ε_sphere) 은 입자 겹침을 두 번 세어 SE 가 하중을 지는 침대에서 **음수**가 된다 — 130 중 음수 18 (HOLD) · se_rich 표지 21 · 64 중 음수 60.
- union (겹침을 뺀 정확한 부피) 은 194 건 **전부 양수** (`docs/data/lhs_union_20260927/`).
- 단 union 은 소성 압축에서 밀려난 재료를 고체로 안 세는 **상한 규약**이다 (CLAUDE.md E_SE 절 · ε_sphere 가 생산 규약) — 열 사전에 그대로 적고, 내부 표에는 둘 다 남긴다.

## 5. ① 접촉 위상 열 — 한 줄씩 (뜻은 생성기 `WA_DEFINE` · 상세 J20-a)

| 열 | 뜻 (쉽게) | 주의 |
|---|---|---|
| `se_se_cn` · `se_se_cn_std` | SE 한 알이 SE 몇 알과 닿아 있나 — 전 SE 평균과 산포 | 벽에 닿은 알은 그쪽 이웃이 없어 낮게 나온다 |
| `am_se_cn_mean` | AM 한 알이 SE 몇 알과 닿아 있나 — AM_P + AM_S 개수 평균 | 상별 값의 평균이라 **파생** |
| `AM_P_se_cn_*` · `AM_S_se_cn_*` | 위 값을 큰 AM · 작은 AM 따로 (mean · std · median · max) | 그 상이 없으면 빈칸 |
| `am_se_cn_surface_weighted` | AM 표면적으로 가중한 AM–SE 접촉 수 | 큰 AM 이 지배 → 벽 효과 큼 · **파생** |
| `am_am_cn` · `am_am_cn_std` · `am_am_n_contacts` | AM 한 알이 AM 몇 알과 닿아 있나 (P–S 교차 포함) · 총 AM–AM 접촉 수 | 접촉 수는 총량 |
| `area_<쌍>_n` | 쌍 종류별 접촉 **개수** (덤프 행 수) | 면적 아님 · 총량 → 입자당 · 부피당으로 나눠 쓸 것 |
| `wall_touch_frac_<상>_<floor\|plate>` | 상별로 바닥 · 플래튼에 닿은 알의 비율 | 위 벽 효과를 가르는 설명 변수 (재수확 v3) |

64 건은 SE-rich 라 `se_se_cn` 이 130 (중앙 4.75) 보다 높게 나온다 (J19 실측 9.6).

**함수 검토 (1저자와 · 09-30~)** — 표에 싣는 것은 검토가 끝난 열뿐이다.

| 열 | 내는 함수 | 검토 | 메모 |
|---|---|---|---|
| `area_<쌍>_n` | `calc_interface_area` (`dem_analysis_core.py:131–168`) → `analyze_contacts.py:405–409` | ✅ 09-30 · 수정 불요 | 한 줄 = 한 접촉 · 짝 이름은 두 상 이름을 정렬해 잇는다 · 없는 id 의 행은 **조용히 버린다** (130 은 0 — 수확기 에이전트 보고 · 64 는 재수확 고아 행 수로 확인) · 중복 · 여러 프레임은 배치가 실행 전 거부 · δ ≤ 0 행도 센다 (130 은 0) · 종류표 밖 `?` 는 AM전체-SE 에 섞일 수 있으나 배치가 종류표를 먼저 대조 · 벽 접촉은 안 센다 · mono 쌍 이름 = 반지름 이름 (위 §0 ⚠ → 7b 에서 설계 상 칸으로 옮김 · `wa_mono_phase_name_webapp`) · ⚠ **접촉 0 인 쌍은 키가 없다** → 표에서 빈칸이었다 (09-30 실측: bimodal 의 `area_AM_P_AM_P_n` 130 에서 3 · 64 에서 6 — 뜻은 0) → ✅ 생성기가 0 으로 채움 (J20-h) |
| `se_se_cn` · `se_se_cn_std` | `calc_se_se_cn` (`dem_analysis_core.py:232–344`) → `analyze_contacts.py:376–377` | ✅ 09-30 · 수정 불요 (J20-i) | SE 한 알마다 SE 와의 접촉 수를 세고 SE **전 입자**로 평균 (접촉 0 · 벽 · 플래튼 입자 포함) · 표준편차 = 모집단 (`np.std`) · 접촉 = 계면 개수와 같은 덤프 행 (원자 프레임에 없는 id 의 행은 버림 · 벽 접촉은 안 셈) · 평균 = 2 × `area_SE_SE_n` / SE 입자 수 — 130/130 · 64/64 차이 0 → 생성기 관문 (어긋나거나 SE 수를 모르면 거부) · 같은 함수의 나머지 8 열 (`_perc` 3 · `_eff_area` 1 · `_aug` 4) 은 ② · ⑦ · ⑤ 차례 · ⚠ F1 근접쌍 (`_aug`) 격자 탐색에 주기 영상이 없어 x · y 경계 너머 쌍을 못 본다 → `LHS-22` (⑤ 차례에 수정) |
| `am_am_cn` · `am_am_cn_std` · `am_am_n_contacts` | `calc_am_am_cn` (`dem_analysis_core.py:347–375`) → `analyze_contacts.py:452–458` | ✅ 09-30 · 수정 불요 (J20-j) | 두 원자가 모두 AM 종류인 행마다 두 입자에 +1 → AM **전 입자** 평균 (P–S 교차 · 접촉 0 포함) · 모집단 표준편차 · 총수 = Σ/2 · 총수 = AM–AM 쌍 개수 합 · 평균 = 2 × 총수 / AM 입자 수 — 130/130 · 64/64 차이 0 → 생성기 관문 둘 · mono 에도 값 (J20-f (A) 로 비운 AM–AM 개수가 돌아온다) · `am_am_mean_area` · `am_am_total_area` 는 ⑦ 차례 |
| `am_se_cn_mean` · `am_se_cn_surface_weighted` · `AM_P/AM_S_se_cn_*` (+ 고립 비율 3 · 전체 분포 3) | `calc_am_isolation_risk` (`dem_analysis_core.py:781–855`) → `analyze_contacts.py:452–468` | ✅ 09-30 검토 · 수정 불요 · 대조 전부 차이 0 · ✅ **7c 10-01 실림** (J20-k 7c) | ✅ **7c (10-01)**: 5번 배치 (`--stop-after coverage`) 원천 · 16 열 · 관문 G1–G7 (상별 평균 × N = 쌍 개수 · 전체 평균 × N = 쌍 개수 · 고립 개수 가중 · max · median · 합동 std · 표면 가중 = 설계 반경) + 상 있음/없음 — **130/130 · 64/64 통과** · 고립 비율 = SE 접촉 0–1 개 (census COND_cov 오분류 → ✅ 승격 · `LHS-23`) · 7a 새 키 = 배치 머리에 있을 때만 · 인계표 `lhs_handover_20261001.csv` 130×155 · `lhsx_…` 64×157 (옛 칸 변경 0) · 옛 메모: ⏸ 싣기는 coverage 닫힌 뒤 (J20-k 7c) · mono 분포는 (C) ✅ **7a 09-30** 웹앱이 전체 `am_se_cn_std` · `_median` · `_max` 를 내보냄 (`analyze_contacts.py --selftest` 12/12 · 값은 5번 coverage 배치 뒤) · mono 상별 칸은 (B) 설계 상 칸에 채움 (**7b ✅ 09-30** — 쌍 개수 · coverage · `n_AM_*_measured` · `cov_*_n_valid` · QC · 열 사전 표지 · 이름 옮김 5 · 4 건) · 고립 비율 census 오분류 `LHS-23` |
| ② `percolation_pct` · `top_reachable_pct` · `n_components` · `n_large_components` · `ionic_active_pct` · `se_se_cn_perc` · `se_se_cn_n_perc` | `calc_percolation` · `calc_ionic_active_am` · `calc_se_se_cn` 관통 부분 → `analyze_contacts.py:404–413` | ✅ J20-b 감사 (09-29 · 130/130 CLEAN) · ✅ **10-01 실림** (J20-n) | 관문 P1 (관통 일관 + 수확기 독립 재현) · P2 (범위 · 순서) · P3 (관통 SE 개수) 130/130 · 64/64 · F3 한정어 (`LHS-19`) · `top_reachable` · `ionic_active` census 오분류 → ✅ (`LHS-20`) · `electronic_active_fraction` (망 단계) · `se_se_cn_eff_area_perc` (면적 ⑦) 은 안 싣는다 · ⚠ lhsx 64 감사기 미실행 (P1 로 대신) |
| 벽 τ `tortuosity_SE_wall` · `_median` · `_status` · `tau_wall_n_*` (+ 벽 접촉 비율 8) | `lhs_descriptor_harvest.tortuosity_se` → `_tau_sample` (수확 v3) | ✅ **10-01** 검토 · 수정 불요 · 실림 (J20-n) | 기하 최단경로 (Dijkstra · 200 쌍 · [1, 20)) — **수송 τ 아님** (COMSOL 입력 = τ_Laplace,eff · 망 단계 · 나중) · 130 OK 106 · 비관통 24 (N/A) · τ 1.29–4.15 · 64 OK 64 · 1.26–1.60 · 관문 T1–T3 · 벽 접촉 문구 = 수확기 규칙 (겹침 깊이 > 0 · 접선 제외) |

## 6. φ_SE · φ_AM · coverage 점검 (2026-09-29 밤 · 1저자 요청 *"코드 다시 설명 · 실제로 넘길 수 있는 parameter 인지"*)

**어디서 오나**: 세 열 모두 **수확기** `scripts/lhs_descriptor_harvest.py` 의 값이다 (웹앱 열 아님 — J20-a 의 ①–⑦ 감사 묶음은 웹앱 열이고, 이름이 겹치는
`phi_se` · `phi_am` 은 J20 규칙대로 수확 열이 정본).

| 열 | 코드 정의 (함수) | 검사 (인계표 실측) | 판정 |
|---|---|---|---|
| `phi_se` · `phi_am` | `volumes_and_phi`: 상별 **명목 구 부피 합** Σ(4/3)πr³ ÷ (L² × (플래튼 z − 바닥 0)) · 겹친 부피를 두 번 셈 · 벽 밖으로 나간 구 부분도 셈 · `φ_SE + φ_AM + ε_sphere = 1` 정확 (재료 보존 장부) | union porosity 와의 닫힘 `φ_SE+φ_AM+ε_union−1` = 130 중앙 **+3.77 %p** (1.15–10.17) · 64 중앙 **+10.91 %p** (6.80–14.22) · 합 > 1 인 행 **130 중 18 · 64 중 60** | ⚠ **그대로 "부피분율" 로 넘기면 안 된다** — 넘기는 porosity 가 union 인데 φ 는 구 부피 합이라 셋이 닫히지 않고, SE-rich 에서 합이 1 을 넘는다 · 분모도 넘기는 두께 (H_mc) 가 아니라 DEM 판 간격 H |
| (대안) 질량 보존 φ (라) | 같은 수확 값 × H / H_mc (= 재료 부피 ÷ (L² × 넘기는 두께)) · 새 측정 불요 | union 과 닫힘 잔차 **0** (194/194) · 적재량 = 레시피 | ⬜ **저자 결정 · ★권고** (아래 대안 넷) |
| (대안) union 점유 φ (가)~(다) | union MC 점 (`lhs_union_webapp.py`, 4×10⁶ 점) 의 `mc_SE_only` · `mc_AM_only` · `mc_both` · `mc_void` (합 = 100 정확, 194/194) | AM∩SE 겹친 부피 (`mc_both`) = 130 중앙 1.73 % (0.06–6.50) · 64 중앙 2.64 % | 두께 H (DEM 판 간격) 와 짝 — 넘기는 두께와 장부가 달라 **인계용 아님** (내부 · COMSOL 형상용) |
| coverage 3 열 | `coverage_hertz`: AM 입자마다 c = min(100, 100 × Σ(AM–SE 접촉면적) ÷ (4πr² − Σ(AM–AM 접촉면적))) → 상별 입자 평균 · 전체 = 실측 입자수 가중 · 접촉면적 = 덤프 `c_cpl[22]` = LIGGGHTS **기하 교차 원판** π(rδ − δ²/4) (A_dem_geometric · Hertz πR*δ 의 약 2 배 · L1-04) | 130 전체 중앙 **21.4 %** (2.4–50.0) · 64 중앙 **52.5 %** (37.9–61.4) · 100 % 잘림 **0 건** · 분모 붕괴 **0 건** · mono 는 ~~P · S 빈칸 (전체 열에 값)~~ → (B) 설계 상 칸에 전체 값 · 없는 상 빈칸 (7b) | ✅ **넘길 수 있다 — 이름 · 정의를 열 사전에 그대로** (접촉 행 자체는 ① 감사 130/130 CLEAN) |

**coverage 의 주의 셋** (열 사전 문구): ① 이름의 hertz 는 물려받은 오해 — 값은 DEM 겹침 원판 면적 (연화 E_SE 1.35 GPa 의 겹침에 비례, 소성 · Tabor 피복률 아님)
② **벽 접촉은 덤프에 없어** 바닥 · 플래튼에 닿은 AM 표면은 "안 덮인 면" 으로 분모에 남는다 → 벽 효과로 낮게 나올 수 있다 (재수확 v3 의 `wall_touch_frac_*` 가 설명 변수)
③ 입자 평균 (상 평균의 평균 · 총면적비 · 질량가중과 다른 양) · 전체 = 입자수 가중.

**한 줄로**: φ 는 **재료 부피 ÷ 두께** 다 (DEM 구는 크기가 안 변하니 분자 = 레시피 SE · AM 부피 = 상수).  지금 열은 **넘기지 않는 두께** (DEM 판 간격 H) 로 나눴고,
넘기는 두께는 **질량 보존 두께** H_mc = H × (1 − ε_sphere)/(1 − ε_union) (J19 ② 비준 · H_mc/H 중앙 1.043 [1.015–1.114] · 64 는 1.118 [1.074–1.153]) 다.
실측 예: `lhs00_006` (130 중앙) 0.269 + 0.632 + union 13.61 % = **103.7 %** · `lhsx_015` (64 중앙) 0.630 + 0.413 = 1.043 — porosity 를 더하기 전에 이미 100 % 를 넘는다.

**φ 대안 넷** (⬜ 저자 결정 — 넷 다 union porosity 와 정확히 닫힌다 · 194/194 잔차 0):

| 안 | φ_AM | φ_SE | 같이 써야 하는 두께 | 근거 · 한계 |
|---|---|---|---|---|
| **(라) 질량 보존 ★권고** | V_AM / (L² · H_mc) = φ_AM(구) × H / H_mc | 같은 식 (SE) | **H_mc = 넘기는 두께** | 넘기는 두께 · porosity 와 **같은 장부** (J19 ② 의 논리 그대로) · 적재량 = 레시피 그대로 (φ_i · H_mc · L² = V_i) · SE/고체 = `se_of_solid_vol` (차 ≤ 3e-16 · `se_rich` 와 같은 값) · 겹친 곳 배정 규칙이 필요 없다 · 실험이 φ 를 내는 방식 (질량 ÷ 밀도 ÷ 부피) · 130 φ_SE 0.079–0.474 · φ_AM 0.422–0.715 · 64 φ_SE 0.476–0.798 · φ_AM 0.143–0.449 |
| (가) 겹친 부피 = AM | AM만 + 둘다 = V(∪AM)/V | SE만 | DEM 판 간격 H (내부 열) | DEM 상자 안 점유율 — **H_mc 와 섞으면** 적재량이 레시피와 어긋난다: AM 130 중앙 +3.2 % (최대 +10.7 %) · 64 중앙 +11.2 % (6.4–14.8 %) · SE −6.9 % · −4.8 % |
| (나) 반씩 | AM만 + 둘다/2 | SE만 + 둘다/2 | H | (가) 와 같은 문제 + 물리 근거 약함 |
| (다) 세 부피 그대로 | AM만 | SE만 | H | + `둘다` 열 — DEM 형상을 그대로 쓰는 쪽 (COMSOL 메싱 등 · 두께도 H) 에만 |

⚠ **권고 정정 (09-29 밤 · 같은 날 두 번째 점검)** — 앞 판의 ★ (가) 는 **철회**한다.  (가) 는 union 과는 닫히지만 DEM 판 간격 H 의 상자 안 점유율이라, 넘기는 두께 H_mc 와 다시
다른 장부가 된다 (받는 쪽이 φ × 두께 로 적재량을 내면 위 표대로 틀린다).  J19 ③ 의 *"union 판 φ · 겹침 배분 = 저자 결정"* 도 같은 이유로 ② (질량 보존 두께) 와 짝이 안 맞는다.
세 장부 — S 구 부피 합 (두께 H · ε_sphere · 지금 φ) · G DEM 형상 (두께 H · ε_union · (가)~(다)) · **M 질량 보존 (두께 H_mc · ε_union · (라))** — 에서 **넘기는 두께 · porosity 가 M 이니 φ 도 M**.

⇒ ✅ **결정 · 구현 (1저자 09-29 밤 *"φ 는 (라) 에 해당하는 것만"*)**: 생성기 `lhs_design_dataset.py` 에 `phi_se_mass_conserving` · `phi_am_mass_conserving` 두 열
(반례 먼저 — 새 시험 6 건이 옛 코드에서 실패 → 구현 뒤 90/90) · 런타임 관문 = 닫힘 1e-9 (넘으면 거부) · φ status ≠ OK 면 빈칸 · 실물 130 닫힘 3.3e-16 · SE/고체 ↔ union
`se_of_solid_vol` 1.7e-16.  구 부피 합 φ 는 내부 표에만.  (가)~(다) 는 만들지 않는다 (MC 부피는 union TSV 에 이미 있다).  **새로 돌린 계산은 없다** — 저장된 세 열의 곱셈이다.
웹앱 φ_SE (③ 감사 묶음) 도 같은 구 부피 합 식이다 (`network_conductivity.py:1120-1123` · 분모 = 상자 가로 × 세로 × `plate_z`) — ③ 감사 때 같은 장부 문제로 다룬다.
⚠ 130 의 열 사전 파일 (`lhs_handover_20260928_columns.tsv`) 은 리포에 없다 — 09-28 표가 열 사전 기능 이전 판이라 **다음 재생성 때** 같은 생성기로 생긴다.
