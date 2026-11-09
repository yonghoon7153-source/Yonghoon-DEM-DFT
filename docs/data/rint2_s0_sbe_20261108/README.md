# kgy S0 단계 1 (SBE) 결과 반입 — 20261108

- 원본 tgz: `c7e17f0c-s0fix_1106_done.tgz` · 24284950 B · sha256 `d48f55c1b6884a75f011e9517d3f592c25aecf8a73d7a02ebbbee86eaede0a13` · 안 파일 18
- **판정 = ADOPT_CANDIDATE**
- 채택 조건 (S0 REPORT §12) = rc 0 ∧ 여섯 출력 전부 ∧ cjunc_plan.sha256 = cjunc_plan.json 의 sha256 · 이 판정은 도구의 자동 대조이고, rc 출처는 사람이 한 번 더 확인한다.

## 여섯 출력

| 항목 | 찾은 파일 (묶음 안 경로 → 이 폴더 사본 자리) |
|---|---|
| kit_json | `files/sdcp/ca1_s0_sbe_20261106_memfix/s0_stage1_kit_SBE_vgcf100.json` (6286674 B) |
| junctions_npz | sdcp/ca1_s0_sbe_20261106_memfix/s0_junctions_kit_SBE_vgcf100.npz (18901514 B · 사본 없음 · sha = `NPZ_SHA256.txt`) |
| instances_npz | sdcp/ca1_s0_sbe_20261106_memfix/s0_instances_kit_SBE_vgcf100.npz (29876172 B · 사본 없음 · sha = `NPZ_SHA256.txt`) |
| plan_json | `files/sdcp/ca1_s0_sbe_20261106_memfix/cjunc_plan.json` (1485 B) |
| plan_sha | `files/sdcp/ca1_s0_sbe_20261106_memfix/cjunc_plan.sha256` (82 B) |
| payload_log | `files/sdcp/ca1_s0_sbe_20261106_memfix/payload_capture_kit_SBE_vgcf100.log` (1168 B) |

## rc 근거 (rss.log 의 `rc=` 줄 = run2.sh 15 줄 · S0 Python 자식 rc · 그 밖의 rc= 글 = 참고 · 결정에 안 씀)

- `files/s0mem_1106b/rss.log` → 0 (`rc=0`)

- 결론 rc = 0

## 기타

- cjunc_plan.sha256 선언 4da9886367799c46b5426177fcba5d6e120f718b6cf7a0a9037032a36e0197bd · 실제 4da9886367799c46b5426177fcba5d6e120f718b6cf7a0a9037032a36e0197bd → 같음
- kit JSON: 최상위 칸 16: census_preview · code · elapsed_s · inputs · junction_census · kit · ledger · notes · plan · raster · schema · stage · sv_census · threshold_inputs · thresholds_used · tool
- rss 로그 `files/s0mem_1106b/rss.log` 최대 숫자 줄: 5694360.0 — `5379 5694360` (단위 = 원문)
- 사본 8 · sha 만 2 (`NPZ_SHA256.txt`) · 전체 목록 `MANIFEST.tsv`
- 이 폴더의 파일은 읽기만 했고 아무것도 실행하지 않았다 (업로드 = 믿지 않는 자료 · python -I).
