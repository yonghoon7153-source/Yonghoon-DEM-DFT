# kgy S0 단계 1 (SBE) 결과 반입 — 20261109

- 원본 tgz: `in.tgz` · 581 B · sha256 `46938b8225841c805ebcd87e3d92c01b6ed3b4da4377c5085971067778827bd7` · 안 파일 8
- **판정 = ADOPT_CANDIDATE**
- 채택 조건 (S0 REPORT §12) = rc 0 ∧ 여섯 출력 전부 ∧ cjunc_plan.sha256 = cjunc_plan.json 의 sha256 · 이 판정은 도구의 자동 대조이고, rc 출처는 사람이 한 번 더 확인한다.

## 여섯 출력

| 항목 | 찾은 파일 (묶음 안 경로 → 이 폴더 사본 자리) |
|---|---|
| kit_json | `files/output/s0_stage1_kit_SBE_vgcf100.json` (45 B) |
| junctions_npz | output/s0_junctions_kit_SBE_vgcf100.npz (266 B · 사본 없음 · sha = `NPZ_SHA256.txt`) |
| instances_npz | output/s0_instances_kit_SBE_vgcf100.npz (266 B · 사본 없음 · sha = `NPZ_SHA256.txt`) |
| plan_json | `files/output/cjunc_plan.json` (19 B) |
| plan_sha | `files/output/cjunc_plan.sha256` (82 B) |
| payload_log | `files/output/payload_capture_kit_SBE_vgcf100.log` (30 B) |

## rc 근거 (rss.log 의 `rc=` 줄 = run2.sh 15 줄 · S0 Python 자식 rc · 그 밖의 rc= 글 = 참고 · 결정에 안 씀)

- `files/run/old_rss.log` → 0 (`rc=0`)
- `files/output/payload_capture_kit_SBE_vgcf100.log` → 0 (`[참고 · 결정에 안 씀] rc=0`)

- 결론 rc = 0

## 기타

- cjunc_plan.sha256 선언 cb8daed7b30399a1c3c8b83b3b7bee4b774a30fc389afc1d375e4c23a3cc4ae8 · 실제 cb8daed7b30399a1c3c8b83b3b7bee4b774a30fc389afc1d375e4c23a3cc4ae8 → 같음
- kit JSON: 최상위 칸 2: kit · stage
- rss 로그 `files/run/old_rss.log` 최대 숫자 줄: 0.0 — `rc=0` (단위 = 원문)
- rss 로그 `files/run/rss.log` 최대 숫자 줄: 41.0 — `pid=1 cap_gb=41` (단위 = 원문)
- 사본 6 · sha 만 2 (`NPZ_SHA256.txt`) · 전체 목록 `MANIFEST.tsv`
- 이 폴더의 파일은 읽기만 했고 아무것도 실행하지 않았다 (업로드 = 믿지 않는 자료 · python -I).
