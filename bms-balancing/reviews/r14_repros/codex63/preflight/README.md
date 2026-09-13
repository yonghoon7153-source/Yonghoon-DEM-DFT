# COMSOL 6.3 재구축 — 현지 사전 진단(preflight) 인계 문서 보존

출처: 사용자 PC `…\카카오톡 받은 파일\COMSOL63_PREFLIGHT_HANDOFF\COMSOL63_PREFLIGHT_HANDOFF\` (2026-09-13 밤, 터미널 `cat` 출력을 그대로 옮김).
`PREFLIGHT_MANIFEST.json`: `scope` + `entries` **331** (path · bytes · sha256). 인계 ZIP 자체는 그 폴더에 없었고,
`outputs/COMSOL63_VALIDATED_SHORT_HANDOFF.zip` (앞 라운드의 5초 검증 인계, sha256 `fe52f0d7…`) 이 안에 들어 있다.

| 파일 (패키지 경로) | bytes | manifest sha256 | 여기 사본 |
|---|---|---|---|
| `outputs/NEXT_RUN_PLAN.md` | 9224 | `d7dd6b644f8cd6a2a07109802de22e28a291f5c7be5c356d8a03f195c334b2d1` | **바이트 일치** (`NEXT_RUN_PLAN.md`) |
| `outputs/preflight/PREFLIGHT_RESULTS_KO.md` | 11639 | `a4303b87e3b4191dfa8fb637ef35825aabfa57eed02314ffe19575e456ffa8a0` | `PREFLIGHT_RESULTS_KO.md` — **줄끝만 다르다**: 원본은 CRLF (115 줄, 11639 B), 이 저장소는 `.gitattributes` 로 LF 정규화 (11524 B, sha `87ba751b…`). `sed 's/$/\r/' PREFLIGHT_RESULTS_KO.md \| sha256sum` → `a4303b87…` **일치 확인** (2026-09-13). 내용은 바이트 단위로 원문이다 |
| `outputs/MODEL_DECISIONS.md` | 11780 | `a9f9a0aa…` | 미보존 |
| `outputs/preflight/INDEPENDENT_PREFLIGHT_AUDIT.md` | 13792 | `d276780a…` | 미보존 |
| `outputs/preflight/NEXT_RUN_PLAN_before_preflight.md` | 1819 | `645e599c…` | 미보존 |
| `outputs/preflight/README_PACKAGE_KO.md` | 2155 | `0ffecf47…` | 미보존 |
| `outputs/preflight/results/analysis.md` · `independent_review.md` | 3478 · 5721 | `1e43bf06…` · `0350295e…` | 미보존 |
| `outputs/SHORT_TEST_INDEPENDENT_REVIEW.md` · `VALIDATION_RESULTS.md` | 7879 · 7223 | `27a589c1…` · `cefbe1c4…` | 미보존 (앞 라운드 검토는 `../COMSOL63_SHORT_REVIEW.md`) |
| `work/preflight_cdc_api.md` · `work/preflight_ocv_review.md` | 15762 · 7822 | `3ac01d2f…` · `50bdc9c1…` | 미보존 |

우리 대응: `docs/COMSOL_REBUILD_SPEC.md` §9. 판정은 원문 그대로 **전체 운전 보류** — 검증 완료도 GO 도 아니다.
