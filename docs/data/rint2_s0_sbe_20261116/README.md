# kgy S0 단계 1 (SBE) 결과 반입 — 20261116

- 원본 tgz: `8bd06441-s0log_20261116T004809Z.tgz` · 24286311 B · sha256 `80e4be49ef08f70f88846dd568d98bc846d3084893c8e1e679331c2563235070` · 안 파일 16
- **판정 = ADOPT_CANDIDATE**
- 채택 조건 (S0 REPORT §12) = rc 0 ∧ 여섯 출력 전부 ∧ cjunc_plan.sha256 = cjunc_plan.json 의 sha256 · 이 판정은 도구의 자동 대조이고, rc 출처는 사람이 한 번 더 확인한다.

## 여섯 출력

| 항목 | 찾은 파일 (묶음 안 경로 → 이 폴더 사본 자리) |
|---|---|
| kit_json | `files/ca1_s0_sbe_20261116T004809Z_q14final/s0_stage1_kit_SBE_vgcf100.json` (6286674 B) |
| junctions_npz | ca1_s0_sbe_20261116T004809Z_q14final/s0_junctions_kit_SBE_vgcf100.npz (18901514 B · 사본 없음 · sha = `NPZ_SHA256.txt`) |
| instances_npz | ca1_s0_sbe_20261116T004809Z_q14final/s0_instances_kit_SBE_vgcf100.npz (29876172 B · 사본 없음 · sha = `NPZ_SHA256.txt`) |
| plan_json | `files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.json` (1485 B) |
| plan_sha | `files/ca1_s0_sbe_20261116T004809Z_q14final/cjunc_plan.sha256` (82 B) |
| payload_log | `files/ca1_s0_sbe_20261116T004809Z_q14final/payload_capture_kit_SBE_vgcf100.log` (1168 B) |

## rc 근거 (rss.log 의 `rc=` 줄 = run2.sh 15 줄 · S0 Python 자식 rc · 그 밖의 rc= 글 = 참고 · 결정에 안 씀)

- `files/s0log_20261116T004809Z/rss.log` → 0 (`rc=0`)

- 결론 rc = 0

## 기타

- cjunc_plan.sha256 선언 6346d9ed5fda248b89d1e28dbcb35c90d67264f060be345673c7da63f9924520 · 실제 6346d9ed5fda248b89d1e28dbcb35c90d67264f060be345673c7da63f9924520 → 같음
- kit JSON: 최상위 칸 16: census_preview · code · elapsed_s · inputs · junction_census · kit · ledger · notes · plan · raster · schema · stage · sv_census · threshold_inputs · thresholds_used · tool
- rss 로그 `files/s0log_20261116T004809Z/rss.log` 최대 숫자 줄: 5734112.0 — `5334 5734112` (단위 = 원문)
- 사본 6 · sha 만 2 (`NPZ_SHA256.txt`) · 전체 목록 `MANIFEST.tsv`
- 이 폴더의 파일은 읽기만 했고 아무것도 실행하지 않았다 (업로드 = 믿지 않는 자료 · python -I).

- (11-16 밤 대피 세션 덧붙임) 홈 경로를 <HOME> 으로 가린 사본 둘 = kit JSON · run.log (11 곳) · 원본 sha256 = `MANIFEST.tsv` · 더 넣은 셋 = `files/s0log_20261116T004809Z/meta.txt` · `out_sha256.txt` · `store_probe.json` (가림 없음) · 저장본 시험 (최종 핀 64e4d213e) = 인스턴스 117,583 · 목록 만들기 4,011 s · 쓰기 120 s (1,340,095,705 B) · 다시 읽기 86 s · 같음 (strict) · 이 폴더 바이트 = `SHA256SUMS`.
