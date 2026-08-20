---
title: 2026-08-20 Codex 독립 리뷰
created: 2026-08-20
updated: 2026-08-20
type: guide
tags: [review, audit, crosscheck]
sources: [docs/reviews/codex-review-request.md]
confidence: high
explored: true
verificationStatus: verified
verifiedAt: 2026-08-20
---

# 2026-08-20 Codex 독립 리뷰

> Codex 가 `Codex/bml-crosscheck` worktree 에서 **내부 감사 결과를 보지 않은 상태로**
> 작성한 원문이다. 편집하지 않고 그대로 싣는다. 교차 판정은
> [2026-08-20-internal-audit](2026-08-20-internal-audit.md) 의 교차표에 있다.

## 요약

`wrdkit → api → web` 경로와 저장·실행 도구, 테스트, Markdown을 내부 감사 결과를 보지 않은 상태에서 교차검증했다. 확정 발견은 높음 14건, 중간 15건, 낮음 4건이며, 가장 큰 위험은 활물질 분모·기준 사이클·단위가 조용히 바뀌는 수치 오류와 run 재배정 시 사이클 번호가 깨지는 경로다. 평탄 용량열의 가짜 knee, 미인식 조성의 mAh/g 활성화, 잘린 행 수용, 합성 fixture의 누적 Q 불일치는 격리 재현으로 확인했다. 전체 의존성 기반 테스트는 이 Windows worktree에 `.venv`/`node_modules`가 없어 실행하지 못했으며, 리뷰 중 소스와 원본 데이터는 수정하지 않았다.

## 발견

| # | 심각도 | 파일:줄 | 제목 | 실패 시나리오 | 제안 수정 |
|---:|:---:|---|---|---|---|
| 1 | 높음 | `packages/wrdkit/src/wrdkit/normalize.py:102-120` | 활물질 비율을 모르면 전극 전체를 활물질로 계산한다 | `total_mass_mg=31.6`이고 조성이 `Zzz-9 100 wt%`처럼 모두 미인식 → `active_wt_percent=None`인데도 `active_mass_g=0.0316`이 생겨 5 mAh가 158.2 mAh/g로 보고됨 | 조성이 있거나 활물질 비율이 불명확하면 `active_mass_g=None`과 사유를 반환한다. 전극 전체 기준이 필요하면 별도 명시 basis로 분리한다. |
| 2 | 높음 | `packages/wrdkit/src/wrdkit/composition.py:39-77` | 짧은 별칭의 부분문자열 매치가 미인식 물질을 활물질로 만든다 | 성분명이 `Sample-X` → 문자열 안의 `am`과 매치되어 `active`가 되고 해당 wt%가 mAh/g 분모에 들어감 | 별칭은 정규화된 정확 토큰/경계로만 매치하고 모호한 이름은 `other`로 둔다. `Sample`, `separating` 같은 반례를 추가한다. |
| 3 | 높음 | `apps/api/app/schemas.py:31-115`; `apps/api/app/routers/samples.py:102-145`; `packages/wrdkit/src/wrdkit/normalize.py:99-120` | 물리 입력값의 범위·유한성 검증이 없다 | API로 `active_wt_percent=-20`, 음수 질량/면적 또는 생성 시 `reference_cycle=0` 입력 → 음수 divisor와 음수 mAh/g, 비정상 기준 사이클이 저장됨 | Pydantic 필드에 `gt/ge/le`와 finite 검증을 두고 질량·면적·두께·공칭용량은 양수, wt%는 0–100, 기준 사이클은 1 이상으로 강제한다. 조성 합계 오류는 저장 차단 또는 명시적 override로 처리한다. |
| 4 | 높음 | `apps/api/app/routers/analysis.py:349-497`; `apps/web/src/pages/Compare.tsx:63-97`; `apps/web/src/pages/Dashboard.tsx:202-245` | aggregate 화면이 mAh/g와 raw mAh를 같은 단위로 표시한다 | 질량 있는 A와 없는 B를 `basis=mAh/g`로 비교 → A는 mAh/g, B는 fallback mAh인데 같은 축/열이 mAh/g로 표시되어 200과 5가 직접 비교됨 | aggregate 요청은 모든 시리즈에 공통 basis를 강제해 422/제외 사유를 반환하거나 전체를 mAh로 일괄 fallback한다. UI는 요청값이 아니라 실제 공통 basis를 표시한다. |
| 5 | 높음 | `apps/api/app/routers/analysis.py:73-90,122-185,349-375` | 없는 기준 사이클을 조용히 첫 완료 사이클로 대체한다 | continuation이 cycle 201부터 시작하거나 cycle 3이 없음 → cycle 201을 100% 기준으로 쓰면서 응답은 여전히 `reference_cycle=3`; 비교 UI에는 대체 표시도 없음 | `build_report`와 공통 baseline resolver를 쓰고 requested/used cycle, availability, note를 응답과 시리즈마다 노출한다. 기준 부재 시 계산 불가 정책도 명시한다. |
| 6 | 높음 | `packages/wrdkit/src/wrdkit/knee.py:222-240,294-298` | 평탄·선형 용량열에도 가짜 knee가 생긴다 | cycle 3 이후 용량이 전부 100인 열 → 곡률 0인데 `curvature detected=True`, 다른 기준이 미검출이면 cycle 5가 primary knee로 보고됨 | 0 또는 노이즈 바닥 이하 곡률은 미검출하고, 열화 가속 검증 없는 curvature 단독 결과를 primary로 승격하지 않는다. 평탄·선형 열에 `primary.detected=False` 회귀 테스트를 둔다. |
| 7 | 높음 | `packages/wrdkit/src/wrdkit/schedule.py:220-250`; `apps/api/app/services.py:226-241` | 비식별 전류비에서 C-rate와 공칭용량을 사실값처럼 추정한다 | formation/cycling 전류비가 2 → 0.2C/0.1C와 0.1C/0.05C가 모두 가능한데 첫 후보 0.2C로 확정되어 0.2 mA의 공칭용량을 1 mAh로 표시함 | 장비에 명시값이 없으면 `None`을 반환하거나 후보·근거·confidence가 있는 estimate로 분리한다. 파일명/사용자 입력 같은 독립 근거가 있을 때만 확정한다. |
| 8 | 높음 | `packages/wrdkit/src/wrdkit/export.py:43-71` | raw CSV가 `UnitCoulomb`를 우회한다 | `UnitCoulomb=True` 파일의 18 C/18 J → 같은 `discharge_q`/`discharge_e` 헤더 아래 18을 출력; Ah 파일과 헤더가 같아 5 mAh/0.005 Wh로 오인됨 | Q/E 컬럼은 `charge_mah()`/`discharge_mah()`/`energy_wh()`로 공통 단위 변환하고 헤더에 mAh/Wh를 쓴다. native export가 필요하면 원단위를 명시한다. |
| 9 | 높음 | `packages/wrdkit/src/wrdkit/cli.py:78-89` | CLI 유지율이 기준 cycle 3을 우회한다 | cycle 1=6, cycle 3=5, 마지막=4 mAh → `wrdkit info`가 첫 완료 cycle을 기준으로 66.7%를 출력하지만 규칙상 80%여야 함 | `build_report(reference_cycle=3)`를 재사용하고 기준 부재 시 실제 대체 기준과 사유를 출력한다. |
| 10 | 높음 | `apps/api/app/routers/runs.py:75-91,114-123` | 중복 SHA 업로드가 기존 run을 검증 없이 다른 sample로 옮긴다 | A에 붙은 동일 bytes를 `sample_id=B`로 재업로드 → `sample_id`만 B로 바뀌고 offset·CycleRecord·양쪽 sample 재번호화가 생략됨; 존재하지 않는 ID도 검증 전 commit됨 | 대상 sample을 먼저 검증하고, 이미 다른 sample에 속한 중복은 409로 막는다. 공통 attach 서비스에서 old/new sample 재번호화와 schedule defaults를 한 transaction으로 적용한다. |
| 11 | 높음 | `apps/api/app/routers/runs.py:133-166` | run 이동·분리가 이전 sample의 연속 사이클 번호를 깨뜨린다 | A의 run1(1–8), run2(9–16) 중 run1을 B로 이동/분리 → 새 sample만 renumber되어 A의 run2가 cycle 9부터 남고 cycle 3 기준·유지율이 오염됨 | 변경 전 `old_sample_id`를 보존하고 flush 후 old/new 양쪽을 재번호화한다. attach/detach/move 순열 회귀 테스트를 추가한다. |
| 12 | 높음 | `apps/api/app/routers/runs.py:188-210` | 불변 원본을 API가 영구 삭제한다 | 유일한 run에 `DELETE /api/runs/{id}?delete_original=true` → DB commit 뒤 `data/uploads/<sha>.wrd`가 unlink되어 재파싱·감사 복구가 불가능 | `delete_original`과 unlink를 제거하고 원본은 항상 보존한다. 보존 기한이 필요하면 별도 관리자 archival 정책과 복구 절차로 다룬다. |
| 13 | 높음 | `tools/bml:93-99,258-268,658-679` | 오래된 PID 파일이 무관한 프로세스를 종료할 수 있다 | bml 서버 종료 뒤 PID가 재사용됨 → `bml stop/restart`가 생존 여부만 확인하고 그 PID와 프로세스 그룹을 kill함 | kill 직전에 cmdline·cwd·port·시작 식별자를 모두 소유 검증하고, PID 파일에 start time/nonce를 저장한다. 소유 불명은 삭제·kill하지 말고 보고한다. |
| 14 | 높음 | `tools/bml:977-990`; `docs/guides/wsl-setup.md:76-82` | CRLF 복구 안내가 다른 미커밋 변경을 지운다 | tracked 수정이 남은 checkout에서 안내된 `git rm --cached -r . && git reset --hard` 실행 → 줄바꿈과 무관한 모든 미커밋 tracked 변경이 소실됨 | clean 상태를 먼저 검사하고 commit/백업/별도 worktree를 요구한다. 비파괴적 renormalize 절차만 자동 안내한다. |
| 15 | 중간 | `packages/wrdkit/src/wrdkit/nrbf.py:388-399`; `packages/wrdkit/src/wrdkit/wrd.py:297-316,470-477` | 잘린 NRBF/마지막 raw 행을 정상 파일로 수용한다 | 두 번째 NRBF의 `MessageEnd`를 제거하거나 마지막 raw 행에서 1–4 B 삭제 → 예외 없이 앞 행만 반환하고 `trailing_bytes`만 남아 API/CSV가 부분 데이터를 정상 처리함 | 각 NRBF에 `MessageEnd`를 요구하고 ingest/convert는 `trailing_bytes==0`을 strict 기본으로 검증한다. 부분 복구는 `allow_partial` opt-in과 경고로 분리한다. |
| 16 | 중간 | `packages/wrdkit/src/wrdkit/wrd.py:359-399`; `docs/raw/specs/wrd-binary-format.md:149-151` | UTF-8 raw 문자열을 ASCII로 디코드한다 | 유효한 UTF-8 I RANGE 값 `µA` → NumPy `astype(str)`가 ASCII decode를 시도해 `UnicodeDecodeError` 발생 | 바이트 배열을 UTF-8로 명시 디코드하고 잘못된 바이트는 `WrdError`로 감싼다. 멀티바이트 문자 fixture를 추가한다. |
| 17 | 중간 | `packages/wrdkit/src/wrdkit/export.py:74-112`; `packages/wrdkit/src/wrdkit/cli.py:97-115,156-160` | 미완료 마지막 사이클의 수치가 기본 CSV에 포함된다 | 방전 중 잘린 마지막 cycle이 2 mAh/40% CE → `complete=no` 한 칸만 붙은 채 정상 수치 행으로 후속 Excel/plot에 섞임 | 기본 export는 완료 사이클만 포함하고 `--include-incomplete`를 명시 opt-in으로 둔다. 포함 시 용량·효율을 blank/진단 열로 분리한다. |
| 18 | 중간 | `packages/wrdkit/tests/synthetic.py:157-169,315-352`; `packages/wrdkit/tests/test_wrd.py:58-64` | 합성 `.wrd`가 실제 누적 Q/E와 메타데이터 규약을 다르게 만든다 | 방전 시작 시 `charge_q`가 충전 최종값에 고정되지 않고 0으로 리셋되며, 1 mA×390 s와 선언 5 mAh도 불일치 → 전 테스트가 같은 잘못된 방향으로 통과할 수 있음 | 실제 동시 누적 counter와 전류 적분을 맞추고 Schedule/StartReport/ClassWithId를 포함한다. `UnitCoulomb=True`는 메타데이터를 사후 변조하지 말고 실제 바이트로 생성한다. |
| 19 | 중간 | `apps/api/app/storage.py:42-63`; `apps/api/app/services.py:397-404`; `docs/adr/0003-timeseries-on-disk-summaries-in-db.md:26-27` | NPZ 캐시의 원본 identity·무결성을 검증하지 않는다 | 다른 백업의 valid `columns.npz`가 같은 run id 폴더에 있음 → `meta.json`의 SHA/행 수/컬럼을 읽지 않고 다른 곡선을 조용히 표시; 손상 NPZ는 fallback 대신 500 | load 시 SHA, row count, schema, `unit_coulomb`, parser/cache version을 검증하고 `np.load` 오류까지 원본 재생성 대상으로 삼는다. ADR의 `storage_ok`를 구현·노출한다. |
| 20 | 중간 | `apps/api/app/storage.py:33-52`; `apps/api/app/routers/runs.py:93-123`; `apps/api/app/services.py:175-223` | 파일·DB 저장의 부분 실패가 원자적이지 않고 재업로드가 복구하지 않는다 | 원본/NPZ write 중 disk-full 또는 `persist_parse` 중 실패 → digest 이름의 잘린 파일이나 일부 CycleRecord가 남고 catch가 rollback 없이 commit; 같은 SHA 재업로드는 existing early-return로 복구하지 않음 | 파일은 같은 디렉터리 temp+fsync+hash 확인 뒤 atomic replace하고, DB parse 결과는 transaction/savepoint로 rollback한다. incomplete parse 상태는 중복 경로에서 reparse/409 처리한다. |
| 21 | 중간 | `apps/api/app/routers/runs.py:171-185` | reparse가 뒤 run의 cycle offset을 갱신하지 않는다 | parser 개선으로 앞 run의 `cycle_count`가 변함 → 뒤 continuation run의 cycle 번호가 기존 offset에 남아 gap/overlap 발생 | reparse 후 `renumber_sample_runs(run.sample_id)`와 schedule defaults를 적용하고 cycle-count 변화 회귀 테스트를 둔다. |
| 22 | 중간 | `apps/api/app/routers/runs.py:65-73` | 업로드 크기 제한이 메모리 사용을 제한하지 못한다 | 512 MB 초과 파일 또는 동시 요청 → `await file.read()`가 전체를 RAM에 적재한 뒤에야 413을 반환해 OOM 가능 | chunk 단위로 hash/저장하며 누적 크기가 limit를 넘는 즉시 중단한다. `Content-Length`는 조기 보조 검사로 쓴다. |
| 23 | 중간 | `apps/web/src/components/CompositionEditor.tsx:52-59,243-249` | "조성 지우기"가 조성을 지우지 않는다 | 버튼이 `clear=['composition']`을 전달 → `save()`가 이를 `['active_wt_percent']`로 덮어써 composition은 그대로 남음 | caller의 clear 배열과 `active_wt_percent`를 합치거나 clear 전용 요청을 분리한다. |
| 24 | 중간 | `apps/web/src/pages/SampleDetail.tsx:46-70,402-407,491-515` | 재파싱·삭제 뒤 분석 화면이 이전 값을 계속 보여 준다 | run 재파싱/삭제 성공 → run 목록만 reload되고 cycle/report/profile 의존 key가 바뀌지 않아 삭제·변경 전 그래프와 지표가 페이지에 남음 | 관련 query를 한 번에 invalidate하거나 서버가 sample revision/`updated_at`을 갱신해 모든 분석 요청을 재실행한다. |
| 25 | 중간 | `apps/api/app/routers/analysis.py:505-539`; `apps/web/src/pages/Dashboard.tsx:59-76` | 불연속 사이클을 균등 간격으로 복원해 x축과 knee 위치를 바꾼다 | 실제 완료 cycle `[3,4,100]` → API는 값+첫/끝만 반환하고 UI가 x를 `[3,51.5,100]`으로 만들어 cycle 4 값을 51.5에 그림 | trend를 `{cycle,value}` 포인트로 반환하고 knee marker도 실제 포인트 index/cycle을 사용한다. |
| 26 | 중간 | `tools/bml:501-545,717-765` | pull 후에도 기존 프로세스가 이전 HEAD를 서비스한다 | `bml`이 새 API/web 코드를 pull했지만 기존 소유 서버가 health 200 → 즉시 "이미 돌고 있습니다"로 반환하여 전날 프로세스와 bundle을 계속 제공 | launch HEAD/build fingerprint를 상태 파일에 기록하고 변경 시 소유 확인 후 재시작한다. |
| 27 | 중간 | `Makefile:88-97` | `make check`가 Python lint 실패를 성공 처리한다 | ruff 위반 발생 → `lint-py`의 `|| true`가 exit 0으로 바꿔 필수 check가 통과함 | `|| true`를 제거하고 의도적 예외는 ruff 설정/라인 단위 noqa로 관리한다. |
| 28 | 중간 | `apps/api/app/db.py:27-70` | `_add_missing_columns`가 모델 제약과 rename/type 변화를 검증하지 않는다 | 새 non-null/unique/FK/index 필드 또는 기존 타입 변경 후 pull → 기존 DB에는 nullable·무제약 column이 생기거나 타입 차이가 조용히 남아 모델과 DB가 분기됨 | versioned migration을 도입한다. 임시 helper를 유지한다면 nullability/constraint/type을 검사하고 미지원 변화는 startup을 명확히 실패시킨다. |
| 29 | 중간 | `tools/bml:639-650` | 프론트 빌드 freshness가 의존성·설정 변경을 놓친다 | `package.json`, `package-lock.json`, `tsconfig.json`만 바뀜 → 기존 `dist/index.html`보다 새 소스가 없어 build를 건너뛰고 낡은 bundle을 서비스 | 소스 외 모든 빌드 입력을 포함한 fingerprint를 저장해 비교하거나 Vite build를 안전하게 재실행한다. |
| 30 | 낮음 | `apps/api/app/routers/analysis.py:411,429-430`; `apps/api/app/routers/exports.py:145-164` | 일부 branch 입력이 422가 아니라 500이 된다 | `branches=bogus` → 공통 validator를 거치지 않고 wrdkit `ValueError`가 서버 오류로 노출됨 | schema를 `Literal`/enum으로 제한하고 모든 profile/export 경로에서 동일 validator를 사용한다. |
| 31 | 낮음 | `docs/reviews/codex-session-bootstrap.md:73-80`; `.gitignore:14` | bootstrap이 만드는 `.venv-codex`가 ignore되지 않는다 | 안내대로 `.venv-codex` 생성 → worktree status에 대량 미추적 파일이 나타나 리뷰 문서 stage 때 실수로 포함될 수 있음 | `.venv-codex/`를 ignore하거나 bootstrap도 이미 ignore된 `.venv/`를 사용한다. |
| 32 | 낮음 | `AGENTS.md:165`; `CLAUDE.md:165`; `Makefile:26-27,50-51` | `make setup`의 bml PATH 등록 설명과 실제 target이 다르다 | 문서만 따라 `make setup` → `install-bml`이 실행되지 않아 새 셸에서 `bml` 명령을 찾지 못함 | `setup`이 `install-bml`을 의존하도록 하거나 문서를 `make install-bml` 별도 실행으로 고친다. |
| 33 | 낮음 | `README.md:7,33`; `apps/web/src/pages/Library.tsx:12-35,52-110` | README의 비교 필터 설명과 실제 UI가 다르다 | 사용자가 cutoff·temperature·C-rate로 좁힐 수 있다고 기대 → Library에는 해당 필터가 없어 수동 탐색해야 함 | 필터를 구현하거나 현재 제공하는 검색·group/cathode 필터만 문서에 명시한다. |

## 질문 / 확신 없음

- `packages/wrdkit/src/wrdkit/cycles.py:161-168`: 같은 branch의 연속 `TOTAL STEP` 구간마다 `last-first`를 합산하므로, 장비가 스텝 전환 첫 행에서 Q를 한 샘플만큼 증가시킨다면 경계 증가량이 빠진다. 실제 CC→CV 전환 행에서 두 Q 값이 같은지 원본으로 확인해야 한다.
- `apps/api/app/routers/analysis.py:92-94`: nominal capacity가 없을 때 각 cycle의 퇴화한 방전용량을 분모로 C-rate를 다시 계산한다. "프로토콜 C-rate"가 목적이면 같은 전류도 노화에 따라 0.2C→0.25C로 변하는 결함이고, "현재 실효 C-rate"라면 명칭·근거를 명시해야 한다.
- `apps/api/app/routers/analysis.py:159-185`와 cycle CSV의 `complete_only=false`: 미완료 행을 `complete=false`와 함께 진단용으로 노출하는 것이 허용되는지, "보고하지 않는다"를 모든 표·export에 적용할지 정책 확인이 필요하다.
- `apps/web/src/components/Plot.tsx:54-68`: `Set`/`Map` 병합은 같은 x의 앞선 y를 버린다. 실제 profile에서 용량 plateau/양자화로 중복 x가 생기는지 실제 파일로 확인해야 한다.
- `packages/wrdkit/src/wrdkit/schedule.py:185-187`: `planned_cycles=max(loop_count)`가 formation cycle 수와 loop count 의미를 함께 반영하는지 실제 완주 파일로 확인해야 한다. 그렇지 않으면 health가 1–2 cycle 일찍 finished로 판정할 수 있다.
- `apps/api/app/models.py:146-160`: DB에는 raw mAh/Wh 외에도 CE·에너지효율·평균전압 같은 결정론적 파생 요약이 저장된다. "정규화값만 금지"인지 "raw 외 파생값 전부 금지"인지 저장 원칙 문구를 더 좁힐 필요가 있다.

## 이상 없음을 확인한 것

- 시간 계열은 `wrd.seconds()`/`timestamps()` 또는 schedule의 동일한 `TICKS_PER_SECOND=10_000_000`을 사용하며 임의 tick 나눗셈 우회는 확인되지 않았다.
- 사이클 요약의 Q/E는 `charge_mah()`/`discharge_mah()`/`energy_wh()`를 거치고, `TOTAL STEP` run으로 분할하며, 평균전압은 E/Q로 계산한다.
- `CellStatus` 1/3/4 해석과 낯선 상태의 표시, 명시적 unknown role의 기본값 `other`, 0 wt% 성분 보존은 의도와 일치했다.
- `build_report`는 완료 cycle만 reported/reference/knee에 쓰고 기본 기준 cycle 3 및 기준 부재 표시를 구현한다.
- parser의 선언 컬럼 순서·offset·가변폭 dtype 구성은 스펙과 맞고, metadata 7-bit 문자열·잘린 header·unknown NRBF record의 기본 오류 테스트가 있다.
- DB에는 mAh/g·mAh/cm²·mAh/cm³·retention 같은 질량 의존 정규화값이 저장되지 않으며, 정상 단일-sample 조회는 현재 sample 질량/조성을 매번 resolve해 재파싱 없이 반영한다.
- SPA fallback은 resolved path가 web root 아래인지 확인하고 traversal 테스트가 있으며 경로 탈출을 확인하지 못했다.
- 프론트의 질량·조성 정상 저장 경로는 `updated_at` 변화로 cycle/report/profile을 다시 읽고, i18n 미등록 문자열·null/NaN/Infinity 숫자 포맷은 안전하게 fallback한다.
- TypeScript 주요 응답 타입은 실제 API shape와 대체로 일치하고, 단일 sample basis fallback은 실제 basis와 사유를 함께 반환한다.
- `AGENTS.md`와 `CLAUDE.md`는 허용된 제목·미러 안내 차이 외에 내용 parity가 유지된다.
- `tools/bml`은 pull 전에 workbench checkout을 검사하고 스스로 checkout/switch하지 않으며, 자기 파일이 pull로 바뀌면 인자를 보존해 재실행한다. ownership 회귀 테스트가 고정한 일반 own/foreign/other-checkout 분류도 구현과 일치했다.
- shell 파일은 LF로 저장되며 `.gitattributes`와 CI의 data/의존방향 검사도 의도와 일치했다.
