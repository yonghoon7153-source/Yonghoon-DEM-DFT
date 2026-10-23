# MXD2 최종 문서·증거 패키지 독립 감사 — 2026-10-23

판정: 숫자·원시 증거·소스 신원·HOLD 범위의 실제 모순은 발견하지 않았다. 적용 문서 규율의 두 누락(MXD2-PKG-01/02)을 부모에게 전달했으며 수정 확인 전이다. 이는 내부 문서 패키지 감사이고 외부 코드 GO·전체 게이트·캠페인 승인 판정이 아니다.

입력은 `mxd2-deliverables/`의 완성된 요청서·사전 검토문·v17·새 쪽지·증거 README, 실제 raw JSON/로그/스크립트/patch/소스 사본 및 정본 원장이었다. 작성자 SUMMARY_V2나 부모 설명을 숫자의 근거로 사용하지 않았다. 독립 v1/v2 원보고를 읽고 실제 증거로 재대조했다. tracked·공유 코드·봉인·원장·Git 상태 변경 없음.

## 수와 신원

| 주장 | 독립 확인 |
|---|---|
| manifest | 최상위126, evidence116, 독립v1 4개/v2 8개: 실제 SHA-256 불일치0. source_manifest 21개도 실제 파일과 일치 |
| 소스 | 기준 6baaa04c…, v1 dada1ebb…, v2 661936b7…, full patch 2b865ee1…, delta ac13a4c4…를 실제 파일에서 계산하여 문서 표와 일치. 두 patch의 대상은 생성기 한 파일 |
| 시험 먼저 | raw 로그 PASS/FAIL 직접 집계: 기준143/0, 첫red145/9, v1green154/0, 리뷰red155/3, 최종green158/0. 독립v2 selftest도158/0 |
| 작성자 변이 | mutation-results 19행 = 기준 생존3 + 수정후 검출16. 수정후 전부 rc1·실패검사 있음. 기준3개는 rc0 |
| 독립 변이 | v1 10개 중7검출·3생존, v2 14개 모두rc1. 변이별 원로그의 실패 목록(마지막 FAILED 요약 포함)이 JSON과 일치 |
| 정상3상 | 2밀도×3CGF×2강성×4ρ×2코팅×2Bo=192. 비벽-벽/상쌍9×192=1728. Bo 최대상대오차1.2876531367167487e-5, 힘비2.5893352707528905e-5는 원시결과와 같고 사전폭2e-5/3e-5 이내 |
| 별도양성/입력 | AM_P+SE 실제 결과8행, 설명7값×3경로21개 통제거부. 정상설명4개는 재현 도구의 별도 assert. CLI32행(12+20)은 전부rc≠0·덱없음·traceback없음. 구조/helper49건은 모든 통제거부라고 과장하지 않음 |
| 바이트회귀 | prior_comparison: 192덱 바이트동일·meta source hash 외동일. 별도 감사자 재현에서도 동일 |
| 기존소비자 | diff55/55, readback24/24, smoke rc0 원로그. 이를 lab/D2 소비자 지원 완료로 승격하지 않음 |
| 웹앱 | devlog-v2-render.log 실제 PASS9행/FAIL0, scratch문서 조회를 실제 /mixer 렌더에 주입했다는 한정 유지. v17에 dens-gen·gm-wall-ncm·schema2·개발미등록·MXD2-01한정 존재 |
| MXD2-01 | raw probe의 E FAIL, A/B/U/E/EB 모두FAIL, gen1계획176/859/98965와 lab143/699/99158이 문서와 일치 |
| 기존claimed25 | 기준 원장 Git blob에서 HB3/HBR2 4/HBR3 5/HBR4 2/HBR6 2/HBR10 3/MIX6을 직접 추출해 요청서25ID와 일치. 새 시험으로 이를 verified 처리하지 않음 |

## 범위·정책

MXD2-02–06은 claimed_fixed 제안이며 외부 verified가 아니다. 01의 lab/D2 소비자·S1·코호트·정책v5는 HOLD/open, 07은 미비준 D3 설계 범위로 남는다. 실제 런0·실험0, full_gate_receipt=PENDING_PARENT_INTEGRATION, rc=null을 유지하며 전체 게이트 성공으로 쓰지 않는다. 실제 생성기 수치·벽규칙·생산중력·새실험 수준·시드를 정했다고 주장하지 않는다.

새 커밋은 <<sha:Fix mixer D2>> 자리표시이고 기준핀·소스 SHA만 확정한다. 실행 중인 root 전체 게이트와 이 패키지의 국소 검사 수를 합치지 않는다. 변조 plan·메타/외부text 결합·무하중/중력접촉 차이·일부 TypeError/KeyError·AM_S+SE의 기존 제한을 명시하고 닫았다고 하지 않는다.

구형 독립 v1 보고서의 float('0_73') 수치 오기는 실제73.0이며 INTEGRATION.md가 원본 보존 이유와 정정을 명시한다. 최신 요청서는 해당 잘못된 수치를 재인용하지 않는다. 비표준 토큰 정규화 변이가 살아 있었던 본래 finding과 v2 검출은 별도 원시증거로 유지된다.

## 실제 문서 누락

- MXD2-PKG-01: v17 CLI가 `python3 scripts/make_mixer_deck.py`로 handoff §7의 `python -I` 누락. 증거 README·독립 도구와 자식 실행은 이미 -I를 사용한다.
- MXD2-PKG-02: 새 쪽지에 원장 JSON 조각을 직접 담지 않고 별도 ledger-update-proposals.json 경로만 둔다. handoff §2·§3의 ‘쪽지에 그대로 적는다/원장 JSON 조각’을 충족하도록 실제 제안을 인라인해야 한다. 별도 사본을 유지하더라도 원장 전체 덮어쓰기·자동상태변경을 허용하는 근거로 쓰지 않는다.

부모가 두 수정을 작성자에게 요청한 상태다. 수정되면 별도 재확인 기록으로 닫는다.

## 감사자 별도 재현

실제 저장소를 수정하지 않고 보존 baseline 두 파일로 miniature base를 공백 포함 새 출력 폴더에 만들었다. `/tmp`에서 Python -I -B, BLAS한스레드로 independent/v2/reproduce.py를 실행: rc0. 신원/정상/49입력/관찰/CLI 결과는 원 JSON과 동일, 14변이 모두검출. compare_prior.py도 rc0·192덱/메타 동일 재현. 결과는 `nonrint-package-audit/mxd2 replay/`에 보관했다. 도구는 repo/patch/out 인자를 받고 cloud 절대경로를 요구하지 않는다. auxiliary_archive의 과거 도구는 portable하지 않음을 README가 명시하며 이를 재생 성공 도구에 포함하지 않았다. 이 miniature base는 전체 게이트 환경이 아니다.
