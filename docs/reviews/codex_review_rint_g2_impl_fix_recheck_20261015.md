# Rint G2 ①′ 수정 재확인 — RIMP-01–06

검토일: 2026-10-15  
검토 핀: **`dcb97f1ed942f622d9189eee1a1e9432dc05a655`**  
브랜치: `claude/stoic-knuth-NObVQ`  
요청서: `docs/reviews/codex_rint_g2_impl_fix_recheck_request_20261015.md`  
대조: 직전 `1087a9b2f4a93aa6a3b0debc698a14fffa13488d`의 판정·독립 탐침.

## 0. 결론

**수정 6건 중 5건은 범위 한정 닫힘, RIMP-02는 부분 닫힘이다. 새 P1은 발견하지 못했다.**

기존의 명명된 반례는 모두 막혔다. 그러나 입력을 검증하기 전에 일부를 버리는 조인 파서 때문에, **틀린 열 수의 행·중복 필수 열·뒤에 토큰이 붙은 헤더가 PASS로 인증되는 새 반례**가 남는다. 새 P2 `RIMPR-01`이다. 별도로 Decimal에서는 유한하지만 float64로 변환하면 무한대가 되는 scaffold 반경도 조인 PASS를 받는다. 이것은 뒤 원장 생성기가 차단하므로 새 P3 `RIMPR-02`로 구분한다.

여기서 새 ID는 **이번에 새로 실증한 잔여 결함**이라는 뜻이다. 이번 수정이 처음 만들어 낸 회귀라고 단정하지 않는다.

| 기존 항목 | 판정 | 실제 재실행 근거 / 한계 |
|---|---|---|
| RIMP-01 경계 반 셀 | **닫힘** | 기존 독립 교정값 재현 + 새 해석 층 32개·두 면 동시 교차 꼭짓점 24개. 정식 T2/T3·tie 등록의 닫힘은 아님 |
| RIMP-02 비유한·음수·상자·미인증 면적 | **부분** | 기존 반례 차단, 정상 두 침대 유지. 파서의 부분 소비·변환 후 비유한이 남음 (§2–3) |
| RIMP-03 정밀도 가정 | **닫힘, 지원 형식 한정** | 정상 `%g` 자료 유지, 16자리·끝 0·혼합 표현 거부. 누락된 행의 형식까지 인증하는 것은 아님 — §2로 별도 집계 |
| RIMP-04 RRM 검사 집합 비우기 | **닫힘, wrapper·신뢰된 원장 범위** | 재생성 비교를 무력화해도 확장 변이 25/25 독립 검사에서 거부. 정상·r=0·유효 거부 계획 구분 유지 |
| RIMP-05 물리 격자 간격 | **닫힘** | h=0.2 µm 계획을 0.4 µm로 호출하면 조립 전 거부·CG 호출 0. 정상 재생성 계획 유지 |
| RIMP-06 RRM 요약 | **닫힘, 조사한 소비자 범위** | 실제 RRM 행·소산 경로에 맞는 표준 요약, CNC 비교 별도, 정상 소비자 실행 |

**①′ 정량 채택·생산 HOLD는 그대로다.** 이번 요청은 그 해제를 구하지 않았으며, D11·D16-dev·D17·D19·D21 저자 결정, D12-V 봉인, 정식 T2/T3 독립 검증 및 실행 영수증을 승인하지 않는다. 생산 코드·원장·Git 상태는 수정하지 않았다. DEM/MPM 캠페인이나 스케줄러 실행도 하지 않았다.

## 1. 증거 범위와 실행

### 1-1. 핀·수정 순서

원격 Git 객체와 파일 바이트를 읽기 전용으로 대조했다.

- 시험 먼저 `e9d0cd87d` → 구현 `25aecac22` → 요청서·증거 `dcb97f1ed`의 부모 연결 일치.
- 먼저 추가한 시험 4파일의 blob은 수정 뒤 핀과 동일. 구현 커밋이 바꾼 수치·관문 모듈은 요청서의 4파일과 일치.
- 내려받은 851파일의 Git blob·SHA256을 검증. 후속 브랜치 HEAD는 이번 판정에 섞지 않음.
- `run_network_194_parallel.CODE_FILES` **32/32**, `seal_s3_prerun.NUMERIC_MODULES` **6/6**은 직전 검토 핀과 blob 동일. 봉인 목록 자체가 모든 미래 경로를 보증한다는 뜻은 아님.
- 제출된 `HASHES.txt`를 내용 바이트와 대조했다. 제출 로그를 독립 실행으로 오인하지 않았고, 아래 결과는 별도로 실행했다.

증거: `evidence/lineage_summary.json`, `integrity.json`, `reviewed_source.diff`, `source_manifest.json`.

### 1-2. 회귀·양성 대조

| 시험 | 독립 재실행 |
|---|---:|
| `test_rint_g2_am_iface.py` | 132/132 |
| `test_rint_g2_rrm.py` | 54/54 |
| `test_rint_g2_join.py` | 73/73 |
| `test_rint_t4_census.py` | 8/8 |
| `test_rint_t43_order.py` | 6/6 |
| `test_rint_t2_dev.py` | 23/23 |
| 합계 | **296/296** |
| `step3_sigma.py --selftest`, `--selftest-rint` | 각각 rc=0 |
| `rint_t41_census.py --selftest` | rc=0 |

독립 OFF 비교는 수정 직전 모듈과 **16/16**, ①′ 구현 전 모듈과 **16/16**에서 rasterize 및 전체 반환 dict·배열 바이트 동일. 두 모듈에 같은 소규모 직접 풀이를 사용한 비교이며 전 입력 공간의 동등성 증명은 아니다.

소유권 탐침도 유지됐다: 집합 오라클 550개 불일치 0, 고정 마스크 6기하×24순열 불일치 0. real14·case15·kit ps5:5의 거친 T4 기하·순열 결과 유지. 제출 Linux 요약과 일부 부동소수 분위수 끝자리 차이는 기록에 남겼으며 이를 비트 동일이라고 부르지 않는다. raw raster의 3,170↔3,171셀 사례도 그대로 관찰·격리된다.

환경: Windows, Python 3.12.14, NumPy 2.5.3, SciPy 1.16.3, BLAS 1 thread. Windows에 없는 `resource`는 **메모리 진단 필드만 NaN으로 제공**했다. 수치 함수는 대체하지 않았다. 증거 `baseline_tests.json`, `parent_probe_runs.json`, `off_compatibility.json`, `off_before_fix.json`, `owner_independent.json`.

## 2. 새 P2 — RIMPR-01: 파서가 버린 행·열·토큰은 입구 검사를 받지 않는다

**영향: “입력 전수 검사 → 유한·형식·개수 일치 → 조인 PASS”라는 보증이 무너진다.** 정상 real14·case15의 계산값이 틀렸다는 증거는 아니다. 현재 반례는 틀린 파일이 정상 부분집합으로 인증되는 문제이며, σ 값의 변화까지 주장하지 않는다.

근거 코드: [rint_iface_join.py](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g2_impl_reverify_20261015/source/scripts/rint_iface_join.py:222).

- **224,234행**: step·count 줄에서 첫 토큰만 취한다. `100 0.9`, `1 garbage`의 나머지는 검증하지 않는다.
- **250–253행**: 행 길이가 헤더 길이와 같은 것만 `rows`에 넣고, 다른 행은 오류 없이 버린다.
- **280,306행**: 필수 열 존재만 보고 `hdr.index()`의 첫 열을 사용한다. 중복 필수 이름이 있으면 뒤 열은 검사에서 사라진다.
- 후속 `n_rows`는 이렇게 걸러진 수다. 입구 유한성·형식 검사도 남은 필드만 본다.

### 실제 함수 반례

정상 합성 침대는 AM 두 구, r=1 µm, 중심 거리 1.5 µm, δ=0.5 µm, 실제 교차 원판 면적 `1.3744467859455347e−6 sim²`. 원자·접촉 덤프는 지원 `%g` 형식이다.

| 변이 | 파일의 실제 내용 | 현재 조인 / 후속 정량 관문 |
|---|---|---|
| 정상 접촉 행의 사본에 숫자 한 열을 더해 기존 행 앞에 삽입 | 선언 1행, **실제 2행**, 폭 24·23열, 헤더 23열 → 파서가 24열 행 삭제 | **PASS / ACCEPT** |
| 정상 원자 행의 사본에 숫자 한 열을 더해 기존 행들 앞에 삽입 | 선언 2행, **실제 3행**, 폭 7·6·6열, 헤더 6열 → 7열 행 삭제 | **PASS / ACCEPT** |
| `radius` 필수 열 중복 | 헤더 7열·행도 7열, 뒤 `radius` 두 값은 `nan` | **PASS / ACCEPT**, 보고 `n_nonfinite=0` |
| step 줄 `100 0.9` | 두 토큰 중 `100`만 소비 | **PASS / ACCEPT** |
| count 줄 `1 garbage` | 두 토큰 중 `1`만 소비 | **PASS / ACCEPT** |
| 양성 차단 대조: 폭이 정상인 중복 접촉 행 | 선언 1행·실제 2행 모두 소비 | **REJECT**, `count_mismatch`·`dem_duplicate_pair` |

앞의 잘못된 행은 파일 끝의 주석이 아니라 **`ITEM: ENTRIES`/`ITEM: ATOMS` 바로 아래 데이터 블록 안**에 넣었다. 정상 원장 → 변이 파일 조인 → `am_iface_plan(join=…)` → `iface_require_quantitative(vox=.25)`의 실 호출에서 통과했다. 동일한 보존 파일을 주 검토자가 별도 경로로 다시 읽어 같은 결과를 얻었다.

재현: `python probes/join_independent.py`, 이어서 `python probes/join_parent_replay.py`. 증거 `join_independent.json`의 `malformed_numeric_*_inside_block`, `duplicate_radius_column`, `step_extra_token`, `count_extra_token`, 그리고 `join_parent_replay.json`. 반례 원문은 `tmp/join_independent/`에 보존했다.

### 최소 해결·종결 증거

1. 데이터 블록의 모든 비어 있지 않은 행을 세고, 열 수 불일치를 명시 `REJECT`로 남길 것. 행을 조용히 제외하지 말 것.
2. 소비하는 필수 열 이름은 정확히 한 번이어야 할 것. 선택하지 않은 같은 이름의 열을 남기지 말 것.
3. step·count 줄 전체가 정확히 한 정수 토큰인지 검사할 것.
4. 위 반례는 조인 단계에서 실패하고, 정상 `%g` 두 침대·D19 양성은 유지돼야 한다. 후속 계획도 그 REJECT를 이어받아야 한다.

형식 검사 강화가 아니라 **형식 검사를 적용할 원본을 온전히 읽는 것**이 먼저다. 허용오차 변경이나 수치 재계산은 필요하지 않다.

## 3. 새 P3 — RIMPR-02: Decimal의 유한성과 실제 float64의 유한성이 다르다

근거 코드: [rint_iface_join.py:339](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g2_impl_reverify_20261015/source/scripts/rint_iface_join.py:339).

`read_scaffold_csv`는 339–350행에서 `Decimal.is_finite()`로 비유한 수를 세고, 353–354행에서 실제 float64 좌표·반경으로 바꾼다. 357행의 양수 검사는 `np.isfinite(rr)`인 값만 대상으로 한다. 따라서 변환 뒤 무한대가 된 반경은 **비유한 수에도, 비양수 수에도 잡히지 않는다**.

반경 하나를 `1e309`로 바꾸면 조인은 **PASS**, `n_nonfinite=0`, 반환 `r_um=[1.0, inf]`다. 지수 표현이 계약 밖이라는 반론을 피하기 위해 **`1` 뒤 0이 309개인 고정소수 문자열 + `.000000000000`**도 시험했고 같은 PASS다. 음수 고정소수 변이는 `-inf`로도 같은 문제가 난다.

**한정:** 이것이 생산 σ를 오염시켰다고 주장하지 않는다. 그 입자를 실제 원장 생성에 넣으면 `step3_sigma.py:1054`의 독립 유한성 검사로 `ValueError`가 발생한다. 유한한 정상 원장과 조합해도 입자 지문 불일치로 거부한다. 따라서 §2의 정량 관문 통과와 달리 **조인 증서의 잘못된 PASS·진단 완결성 문제**로 P3다.

최소 해결은 Decimal 검사와 별도로 **실제로 사용되는 float64 좌표·반경 및 필요한 단위변환 결과**의 유한성을 입구에서 검사하는 것이다. `±10^309` 변이는 structured REJECT, 정상 두 침대는 PASS로 회귀를 남기면 된다. int64 범위를 넘는 정수 토큰이 현재 `OverflowError`로 끝나는 경우도 같은 입구 오류 처리 정비에 포함할 수 있다. 이것은 별도 새 P2로 세지 않았다.

증거: `join_independent.json`의 `scaffold_*overflow`, `overflow_matching_ledger`, `join_parent_replay.json`.

## 4. 닫힌 수정의 수치 근거

### 4-1. RIMP-01 — 경계 반 셀

[rint_t2_dev.py:217](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g2_impl_reverify_20261015/source/scripts/rint_t2_dev.py:217)의 각 면은 교차 시 두 상의 길이와 같은 축 막 저항을 직렬로 더한다. 면 중심의 정확 φ도 그 상의 값을 쓴다. 기존 탐침의 교정은 **옛 모듈에만** 가하고, 그 old-after를 수정판의 무보정 풀이와 대조했다. 수정판에 보정을 두 번 가한 값을 근거로 삼지 않았다.

| 사례 | 옛 최대 전위 오차 | 수정판 최대 전위 오차 | 수정판 L2 |
|---|---:|---:|---:|
| 15°, n64, axis | 0.537675585605 | 0.006475555385 | 0.000449511290449 |
| 30°, n16, axis | 0.503808452664 | 0.016337040711 | 0.003087791838663 |
| 45°, n128, +0.001 µm | 0.443926287840 | 0.004030350534 | 0.000982364323869 |
| 15°, n64, L1 | 0.532474728297 | 0.020304095713 | 0.001406042364339 |

무이동 45°까지 5사례에서 old-after와 수정판의 최대오차 차 ≤`4.52e−17`, L2 차 ≤`4.34e−19`.

새 독립 오라클은 구현의 거리분할 공식을 재사용하지 않고, β=0의 알려진 상별 gradient/current에서 각 경계 g와 우변을 계산했다. 축·끝점 층 **32개** 최대 전위 오차 `5.33e−15`, 같은 꼭짓점 셀의 두 경계면이 동시에 교차하는 **24개** `4.89e−15`. 이 범위에서 누락·중복은 없다. `boundary_recheck.json`과 `notes/boundary.md`에 전 사례를 보존했다.

### 4-2. RIMP-02·03 — 기존 반례와 정상 자료

독립 옛 탐침의 real14 음수 면적·위치/δ/면적 NaN·다른 tilt·소수 step은 모두 REJECT. 16자리 전체 형식, +1 ppm 면적 변이, 끝 0 추가는 `numeric_format`으로 입구에서 거부된다. **16자리 정상 숫자도 지원 형식 밖으로 거부하는 계약**이지, 높은 정밀도가 물리적으로 틀리다는 판정이 아니다.

옛 합성 탐침은 16자리 기준부터 거부되어 `g_geo.delta_bound_um` 접근에서 KeyError로 멈춘다. 그 종료를 숨기지 않고 보존했다. 정상 합성 입력만 `%g`로 바꾼 탐침에서는 기존 변이 차단을 재확인했다. 16자리 +1 ppm 공격 자체는 16자리로 유지했다.

근동심의 원래 좌표는 `%g` 반올림으로 서로 같아지는 경우가 있어, 별도로 x 원점만 0으로 옮겨 거리 `1e−9 sim`과 면적 `100 sim²`를 유지했다. 결과 `tested=0`, `uncertified=1`, `area_all_certified=False`, **REJECT**. 숫자가 큰 거짓 면적뿐 아니라 같은 조건의 참 면적도 인증 불가능하다고 거부하는 것이 맞다.

정상 real14 AM–AM **660/660**, case15 **119/119**가 인증되고 둘 다 PASS. case15 AM–SE 음수 면적 2행은 **AM–AM 인증 밖**으로 명시해 수만 기록한다. D19 다른 step은 선언 없음·틀린 선언이면 거부, 맞는 선언과 동일 기하이면 PASS다. 이 정상 대조를 새 파서 결함과 혼동하지 않는다.

### 4-3. RIMP-04 — 메타데이터로 검사 집합 비우기

[rint_rrm_reference.py:412](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g2_impl_reverify_20261015/source/scripts/rint_rrm_reference.py:412)의 기대 접점은 r 표로 먼저 걸러지지 않는다. 빠진 r·기울기·해상도 미달을 독립 집계하고 거부 사유로 덮여야 한다. 463–479행의 같은 planner 재생성은 **추가 일관성 검사**이며 독립 물리 검증은 아니다.

이를 분리하려고 재생성 비교가 후보를 그대로 반환하도록 탐침에서 무력화했다. 그래도 **25/25 변이**가 앞의 독립 검사에서 걸렸다: cut 삭제+k 변경/r 표 비움, 행·접점 요약까지 모두 비우기, NaN/Inf/음수/미등록 0, 잘못된 k·recipe·절단 행 등. 원래 복합 변이도 실제 `rrm_solve`에서 거부됐다.

정상: film **67**, cut **85**, σ=`0.003334457143882423 S/cm`. 등록 r=0 양성은 유지. 적격 한계 `a/h=4.000346859961018`에서 k가 같으면 통과, 상대 `1e−12` 더 크면 미해상 거부. 그 거부 사유만 지우면 재생성 없이도 `excluded_without_rejection`으로 잡힌다.

유효하게 만든 **거부 계획**의 `rrm_check=[]`는 일관성 검사에 문제가 없다는 뜻이며 실행 허가는 아니다. `rrm_solve`는 이어지는 일반 관문에서 그 거부 사유를 보고 막는다. `rrm_recheck.json`에 구분해 기록했다.

### 4-4. RIMP-05 — 실제 솔버 간격 결합

[step3_sigma.py:1623](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g2_impl_reverify_20261015/source/scripts/step3_sigma.py:1623)과 실제 callsite **1857행**을 대조했다.

| 사례 | 결과 | 실제 막 G [S] |
|---|---|---:|
| 계획 h=0.2, 솔버 h=0.2 µm | σ `0.002198399678003857 S/cm` | `6.251769380643697e−7` |
| 같은 계획·sid, 솔버 h=0.4 µm | **ValueError, CG 호출 0** | 계산 안 함 |
| 크기·계획 모두 h=0.4로 재생성 | σ `0.0021331551689598217 S/cm` | `2.5007077522574787e−6` |

정상 재생성 A·G는 각각 정확히 ×4. NaN/Inf/0/음수 간격, 계획/원장 간격 불일치·결손도 조립 전 거부. `nextafter(0.2,+∞)=0.20000000000000004`도 거부하고 같은 float64 `float('0.2')`는 받는다. 이는 근사 허용이 아니라 **같은 봉인 입력값을 재사용한다는 계약**이다.

옛 탐침이 mismatch에서 잡지 않은 ValueError로 끝나는 로그도 남겼고, 보완 탐침으로 그 뒤 정상 대조까지 실행했다. 증거 `vox_binding.json`, `vox_original.log`.

### 4-5. RIMP-06 — 요약의 계산 주체

[rint_rrm_reference.py:243](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/rint_g2_impl_reverify_20261015/source/scripts/rint_rrm_reference.py:243)의 이름공간 분리와 279–307행의 행 재집계를 직접 대조했다.

| 사례 | RRM film/cut | 표준 요약 G [S] | 별도 CNC 비교 G [S] |
|---|---:|---:|---|
| 정상 A | 67 / 85 | `5.027420037705035e−6` | remove=renormalize=`5.027420037705035e−6` |
| 탄소 반쪽 | 37 / 42 | `2.7535056597827278e−6` | remove=`2.612935414333538e−6`; renormalize=`5.027420037705035e−6` |

실제 행 합·접점 기록·표준 요약이 일치. 반환 `n_*_rows_used`도 일치. `phase_current_share`, `per_particle_current`, 기록 JSON 직렬화를 정상 실행했다. 표준 G/rface는 `rrm`, CNC 비교는 별도 이름공간이며 `iface_carbon_cover=None`에는 사유 표지가 붙는다. 과거 탐침의 변수 이름 `CNC_summary_film_G_S_total`은 과거 이름일 뿐, 새 표준값은 실제로 `{rrm: …}`다.

## 5. 요청서 §4의 아홉 질문에 대한 답

| 질문 | 답 |
|---|---|
| **Q1 경계 반 셀·꼭짓점** | **이번 결함 해결에는 충분.** 평면 교차 거리분할, 같은 축 막 법칙, 각 면 상의 Dirichlet가 맞물린다. 두 면은 별도 flux 항이라 합산이 맞다. 연속 경계면 전체 cut-cell 적분, 일반 경사·3D·flux/에너지 인증까지 뜻하지는 않는다. |
| **Q2 tie 회귀 제외** | **이번 개발 회귀에서는 허용. D12-V 전에는 규약 등록 필요.** tie_count만으로 배정이 재현되지 않는다. 셀·면·정확 φ의 tie/단측 trace·원점 처리와 관측 포함 여부를 한 규약으로 묶거나, tie 없는 사례 선택과 여유를 미리 고정할 것. |
| **Q3 입구 REJECT/skipped** | **출력 상태 설계는 충족.** 미인증 면적을 REJECT로 두는 것도 적절하다. 다만 실제 파서가 빠뜨린 입력은 입구 실패가 되지 않으므로 전체 구현은 §2–3 때문에 부분이다. |
| **Q4 AM–AM만 면적 인증** | **동의, 범위 표지 조건.** 지금 ①′ 대상이 AM–AM이므로 case15의 AM–SE 음수 2행을 인증 밖으로 세는 것은 맞다. 이것을 전 접촉 덤프의 물리적 정상성 또는 향후 SE/섬유 인증으로 확대하면 안 된다. |
| **Q5 canonical `%g`** | **지원 형식의 폐쇄 계약으로 충족.** 원자·접촉 덤프의 소비 실수 열과 상자 경계 토큰은 6자리 canonical 표현과 같아야 한다. scaffold는 고정소수, 정수 식별 토큰은 별도 문법이다. 다른 표현도 같은 숫자일 수 있지만 이 계약에서는 거부한다. 실제 생산자가 어떤 printf 옵션을 썼는지까지 복원하는 증거는 아니다. 파서 전수성은 §2를 따로 고쳐야 한다. |
| **Q6 독립층+재생성층** | **공개된 RRM 범위에서 충분.** 재생성층을 무력화한 25개 변이가 독립층에서도 잡혔다. 신뢰하는 원장 자체의 물리 오류나 모든 자료를 일관되게 교체한 편집까지 검출한다고 부르지 말 것. |
| **Q7 일반 관문 finite/nonnegative** | **추가 권고.** RRM 지식 없이도 모든 막 행의 유한·비음수는 공통 불변량이다. r=0은 보존하고 조립 전에 검사할 것. 이는 이미 공개된 직접 우회의 후속 보강이지 이번 RIMP-04 wrapper 수정의 재개방 사유는 아니다. 아래 재현 참조. |
| **Q8 exact float64·vox=None** | **실제 솔버에서는 적절.** 독립적으로 다시 계산한 “비슷한 h” 대신 같은 봉인 h를 전달해야 한다. `vox=None` 직접 호출은 부분 사전검사일 뿐 물리 간격 인증으로 쓰면 안 된다. 현 솔버 callsite는 반드시 vox를 넘기므로 이번 차단을 우회하지 않는다. |
| **Q9 요약 키·carbon None** | **현재 조사한 소비자는 호환.** 핵심 소비자는 실제 행을 읽고 CNC-only 키를 강제하지 않는다. scripts Python 및 webapp 57개 Python/JS에서 해당 CNC 키를 고정 가정하는 생산 소비자를 찾지 못했다. 외부 소비자까지 보증하지 않는다. 향후 `iface_reference`/`summary_source`로 분기하고 None의 사유를 표시할 것. |

### Q2의 수치 한정

45°, n128에서 offset 0/−`1e−14`/+`1e−14` µm는 모두 `tie_count=128`이지만, tie 중 상2 셀은 106/128/0개다. L2는 `0.000920529357666` / `0.001268892525214` / `0.001271344242858`. 이는 아직 등록하지 않은 배정 규약의 민감도다. 불연속 φ의 trace가 바뀐 셀을 섞어 새로운 대오차라고 과장하지 않았고, 새 P2로 중복 등재하지 않았다.

### Q7의 남은 범위

행을 바꾸고 행 지문을 다시 만든 기존 탐침 조건에서, 일반 관문에 CNC NaN/음수 막을 직접 주면 σ가 `0.0038116099134384756 → 0.004141925781633665 S/cm`, residual `6.23e−15`, unconverged=False가 된다. RRM 직접 우회도 기존대로 `0.003334457143882423 → 0.0037299595666211234 S/cm`. **정상 planner가 이런 값을 만든다는 증거가 아니며, RRM wrapper는 같은 입력을 거부한다.** 작은 선형계 잔차가 막 값의 유효성을 대신하지 못한다는 공통 관문 보강 근거다.

## 6. 다음 재확인에 필요한 최소 묶음

1. **RIMPR-01** 파서 전수 소비·헤더 유일성·scalar 줄 문법을 시험 먼저 수정. §2 반례와 정상 두 침대·D19 대조.
2. **RIMPR-02** float64 변환 뒤 유한성 검사. 고정소수 ±overflow는 조인 REJECT, 정상 자료 유지. downstream 차단만으로 조인 PASS를 유지하지 말 것.
3. 요청서 Q7을 수용할 경우 일반 관문 유한·비음수 검사와 r=0 양성 대조를 추가할 수 있다. 승인된 wrapper 범위 밖 변경이므로 별도로 표기할 것.

새 시뮬레이션이나 기존 생산 배치 재계산은 위 두 파서 항목의 닫힘 증거에 필요하지 않다. RIMP-01·03·04·05·06을 다시 처음부터 재심할 필요도 없다. 변경 diff·두 새 반례·정상 대조를 받으면 된다.

## 7. 재현·산출물

ZIP을 풀어 두 상위 폴더의 상대 위치를 유지한다. Python에 NumPy·SciPy가 필요하다. 아래는 `rint_g2_impl_reverify_20261015/`에서 실행한다. BLAS thread는 1, bytecode 쓰기는 끈다.

```text
python -B run_review_tests.py
python -B probes/boundary_recheck.py
python -B probes/rrm_recheck.py > evidence/rrm_recheck.json
python -B probes/join_independent.py
python -B probes/join_parent_replay.py
python -B probes/vox_binding.py
python -B probes/off_compatibility.py
python -B probes/off_before_fix.py
python -B probes/owner_independent.py
```

원본 옛 탐침의 의도된 중단도 증거다: `join_original_runner.py join_synthetic.py`의 rc=1은 지원 형식 밖 입력 REJECT 뒤 옛 출력 접근의 KeyError이며, `owner_vox_mismatch.py`의 rc=1은 mismatch를 새로 거부한 ValueError다. 이것을 수정판 회귀 실패로 합산하지 않았다. 원본과 수정 탐침의 차이는 `join_synthetic_adaptation.diff`에 남겼다.

`notes/`는 세부 검토 노트, `evidence/`는 독립 실행 결과, `source/`는 고정 핀 원문이다. 제출 증거는 `source/docs/reviews/rint_g2_impl_fix_evidence_20261015/`에 있으며 독립 결과와 분리된다. ZIP의 `PACKAGE_MANIFEST.json`으로 전달 파일 해시를 확인할 수 있다.

**최종: 수정 전체 종결 HOLD — RIMP-02 부분. RIMP-01·03·04·05·06 범위 한정 닫힘. ①′ 정량 채택·생산 HOLD 유지.**
