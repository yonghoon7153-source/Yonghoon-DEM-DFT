# L214-03 화면 독립 재검증 · Q1 / Q2.8 / Q3

검토 소스 `9e3ef54ca228111360bfe5f6d9dad4ebe26d54af`, 기준 `0c557e72aaffdf6cfd033c0667c643de4501c5b1`의 별도 사본. 생산코드·원장·등록·Git 수정 없음. 두 사본은 `.git` 없는 증거 사본이라 `git status / worktree list / branch / rev-parse`는 모두 not-a-repository였다. 새 214 실행 없음.

## 판정

**L214-03은 부분 해결이며 닫힘 보류. P2: 기존 CSV를 합치는 뒤 단계가 모형 한계의 이온 σ와 유도비에 옛 숫자를 복원한다.**

새 표에서 Physics FULL이 없는 기본 경로, 기존 두 열 Hertz CSV에서 Physics를 metrics로 새로 채우는 경로, 최종 전자/열 결측 제거는 실제 함수와 템플릿에서 개선을 확인했다. 그러나 현재 코드가 직접 생성하는 split CSV를 다시 보는 경우와 기존 Hertz CSV 값 보존에는 strict missing이 완결되지 않았다. 아래는 합성 작은 침대와 명시적인 stale-CSV 변이로 재현한 계약 반례다. 과거 생산 214의 어느 화면이 실제 오염됐다는 주장은 아니다.

## 실제 재현 범위

`probes/l214_display.py`는 AST 추출이 아닌 실제 `webapp/app.py`를 import한다. 외부 storage 설정을 공란으로 하고 네 데이터 폴더·임시 출력은 모두 `evidence/display_work/`로 격리했다. 원본 두 사본의 함수는 고치거나 대체하지 않았다.

- 합성 metrics 13종 × 레이아웃 4종(새 표, 기존 두 열, Hertz/Physics split, 이미 네 열) = 소스 52건·기준 52건. `_load_case_tables`와 **Flask GET `/single/<id>` 및 전체 `single.html`**을 실행했고 각각 HTTP 200, 오류 0.
- 별도 작은 실제 생산자/게시 `_run_ml` 네 침대 (`ml_physics`, `ml_hertz`, `ml_el`, `nonthrough`) 모두 `done`, 실패 단계 없음. 각 4개 레이아웃 = 소스 16건 추가. 이 16건은 실제 loader 뒤 전체 Jinja `single.html`을 직접 렌더했다. Flask GET을 했다는 주장과 구별한다. 총 소스 68건·기준 52건은 **렌더 실행 수이며 결함 검사가 모두 통과했다는 뜻이 아니다**.
- `test_network_handover_chain`의 helper와 작은 침대는 재사용했지만 본 탐침의 레이아웃·null/키 결손/0/unknown 변이는 독립적으로 추가했다. 합성 모형 한계 침대는 φ_SE > 1인 계약시험용 사슬이므로 실제 물리 침대 검증이 아니다(`source/webapp/test_pipeline_provenance.py:251`).
- 모든 실행은 지정 Python `-Xutf8 -B`, 기존 두 deps 폴더, OMP/OPENBLAS/MKL 스레드 1. 결과 `evidence/display_source.json`, `evidence/display_base.json`; 선정 HTML `evidence/display_source_*.html`.

## P2 반례 A — split Physics 절이 null을 숫자로 복원

위치: `source/webapp/app.py:2020`–`:2038` (`normalize_network_summary_layout`, Pass A). 현행 CSV 생산 형식은 `source/scripts/analyze_contacts.py:363`–`:389`에서 확인된다.

입력: 실제 생산자 `ml_physics` 게시 성공 결과. authoritative metrics의 Hertz 이온 σ = **2.386067**, Physics σ 키 없음(get 결과 None), Physics 상태 `not_computed`, 사유 `full_over_conduction`. 작은 실제 생산자 증서가 보존돼 있으며 τ는 Hertz OK / Physics `NOT_COMPUTED(full_over_conduction)`이다. 비교할 split CSV에는 명시적인 옛 표시값 Hertz 0.6 / Physics 0.9 / 비 1.50×를 넣었다.

최종 `single.html` 셀 (`evidence/display_source.json`, `cases.producer_ml_physics_split.rendered_rows`):

| 행 | Hertz | Physics | Δ |
|---|---:|---:|---:|
| σ_ionic | 0.6 | **0.9** | **+50.0%** |
| Plastic amplification | **1.50×** | **1.50×** | **0%** |
| 망 상태 | 계산됨 | FULL 모형 한계 | 공란 |
| τ 인계 상태 | OK | NOT_COMPUTED(full_over_conduction) | 공란 |

`_csv_mode_row`가 먼저 Physics 결측을 `— (모형 한계…)`로 고쳐도, Pass A가 별도 `σ_ionic [physics]` 행의 값을 다시 채우고 Δ까지 계산한다. `normalize` 뒤 결측 제거는 전자/열만 대상으로 하므로 이온은 남는다(`app.py:1920`–`:1938`, `:7431`–`:7442`). 파생비 CSV 행도 기존 행이 있으면 갱신하지 않는다(`app.py:2282`).

이미 네 열인 CSV는 `app.py:2956`–`:2957`에서 그대로 통과한다. 같은 게시 레코드에 네 열 `0.6 | 0.6 | 0%`를 주면 그대로 렌더된다(`cases.producer_ml_physics_fourcol`). 이는 추가 적대변이이며 현행 CSV 작성기가 네 열을 쓴다는 뜻은 아니다.

## P2 반례 B — Hertz 모형 한계에도 옛 Hertz 숫자 유지

위치: `source/webapp/app.py:687`–`:700`, 특히 `return [label, h_cell, ...]`. `R_brug`의 기존 행도 동일 목록에서 같은 규칙을 따른다(`:677`–`:683`).

실제 생산자 `ml_hertz`는 H0/H12/Physics FULL을 모두 모형 한계로 거부하고 정상 게시한다. 양쪽 이온 σ와 FULL 비는 미제공이다. 기존 두 열 CSV의 숫자가 있으면 최종 화면은 다음과 같다(`cases.producer_ml_hertz_csv.rendered_rows`).

| 행 | Hertz | Physics | Δ |
|---|---:|---|---|
| σ_ionic | **0.6** | — (full_over_conduction) | — |
| R_brug | **2.0×** | — (full_over_conduction) | — |
| 망 상태 | FULL 모형 한계 | FULL 모형 한계 | 공란 |

CSV 값은 본 탐침이 넣은 옛 표시값이다. 하지만 **실제 network publication 이전**에 CSV를 놓고 바이트를 해시한 뒤 `_run_ml`을 실행했으며 네 침대 전부 게시 후 바이트가 동일했다(`producer_runs.*.preexisting_csv_preserved=true`; SHA256 `c3e08eb12f28d0cc14c992b0e052a053fe3f1c8a2a301cc4fc970a2c1f638b61`). 따라서 이 경로는 게시 원자성이 거부하지 않는다. 이는 설계상 CSV가 contact 산출물이고 network 게시 목록에서 제외되기 때문이다(`source/webapp/pipeline_service.py:61`–`:67`). 상태 전환으로 옛 CSV가 남을 때의 화면 계약 반례이지 과거 실제 CSV 값의 출처를 입증한 시험은 아니다.

**최소 수정 방향:** 최종 이온 표시 행도 현재 metrics/활성 레코드의 모드별 결측과 사유를 최우선으로 적용한다. split 병합 뒤와 이미 네 열인 입력에도 적용하며, FULL에서 나온 비도 같은 규약을 적용한다. CSV 레이아웃 보존 자체를 없앨 필요는 없다. Hertz 칸 무조건 불변이라는 시험은 해당 결측 사례에 맞춰 좁혀야 한다.

## 양성·경계 확인과 한정

- `physics_null_new`, `physics_null_csv`: 기본 이온 σ/CF-FULL/R_brug는 Physics `— (모형 한계…)`, Δ `—`; Hertz 복사 없음.
- `producer_ml_el_*`: 전자 Physics 모델 한계는 네 레이아웃 최종 화면에서 결측+사유와 Δ `—`. Pass D만 보면 H 결측에 Δ0이 있지만 최종 `_suppress_phantom_sigma_rows`가 고치므로 그 단독 코드는 결함으로 보고하지 않는다.
- `producer_nonthrough_new`: 실제 비관통 생산자 상태 `valid_zero/no_through_path`, τ `NOT_PERCOLATING`을 모형 한계와 구분. 이온 σ 숫자 행은 없음. `producer_nonthrough_csv`에서는 같은 stale Hertz 0.6/2.0×가 남아 반례 B와 같은 기존 결함이 드러난다.
- null과 키 결손은 기본 두 열/새 표에서 같은 `—` 경로. unknown reason은 `full_over_conduction` 문구로 바뀌지 않는다. unknown state에 모형한계 reason 문자열만 주면 숫자 셀 문구는 reason만 보고 모형한계라고 하지만, 이는 합성 무효 metrics 렌더이며 실제 게시 관문 우회가 아니다.
- 명시 숫자 0 변이도 실행했다. 이온 0은 Physics 쪽에서 `0.0 / -100%`로 표현되지만 전자/열의 0은 기존 truthiness 규약으로 `—`; 실제 valid_zero 생산자는 null을 내므로 숫자0 변이를 유효한 현행 생산 레코드라고 해석하지 않는다.
- 새 표에서 Hertz σ가 null이면 `app.py:3120`의 조건으로 이온 σ 행 자체가 생기지 않는다. 양쪽 상태 행은 보인다. 이 항목만으로 별도 P2를 세우지는 않았다. 원 닫힘 요구는 결측 셀·Δ를 `—`로 보이고 사유를 밝히는 것이므로, 게시 가능한 H0 모형 한계를 빈 행으로 표현할지에 대한 일관된 회귀 기대는 추가하면 좋다.
- 새 표에서도 FULL 모드비가 결측이면 `Plastic amplification` 행이 `— | — | 0%`다(`app.py:2289`–`:2292`). CSV에서 숫자를 되살리는 반례보다 영향이 작으며, 같은 strict-missing 수정 시 함께 고칠 항목이다.

## Q2.8

옛 케이스의 Physics 결손과 기존 CSV에서 실제 Physics 값이 있는데 Hertz로 복사하던 표시를 함께 바로잡는 범위는 타당하다. 원 L214-03은 모형 한계 case만을 위한 특례가 아니라 모드별 missing/Δ의 표시 계약이다. 다만 현재 구현의 Hertz CSV 불변·split 합치기 예외는 이 취지와 충돌한다. 물리 target 수치 변경과 화면 오류 교정은 증거를 분리해 명시해야 한다.

## Q3 / A4 감사

`source/docs/reviews/lhs214_fix_evidence_20261015/a4_no_impact.py`를 읽어 검사했다. 본 담당은 전체 수치 A4를 재실행하지 않았으며 아래는 스크립트 감사와 독립 화면 대조다.

- N의 `first_diff`는 타입을 확인하고 float의 `hex()`로 비교한다(`:106`–`:127`). 정상 유한 float에 대해 근사오차 허용이 없고 ±0도 구별한다. NaN은 둘 다 NaN이면 같다고 처리하므로 NaN payload bit 보장을 뜻하지 않는다.
- 제외하는 키는 electronic/thermal FULL status/reason 네 이름뿐이며 재귀적으로 제거한다(`:38`, `:74`–`:85`). σ와 파생 target 수치나 기존 solve_info는 숨기지 않는다. 새 q 진단키가 정상 비교에 나오지 않았는지도 별도 검사한다(`:470`). 추가 메타는 별도 보고한다. 이 범위의 비트 동일 증거는 유의미하다.
- N은 합성 4개+real14+case15 두 모드와 별도 직접/반복 격자를 포함한다. T의 194개는 명시된 **옛 세대1** 자료이며 새214 전수 수치 비교로 확대할 수 없다. R의 48,822칸은 빈칸 사유/분류/집계 소비 비교이며 새 v1.3 파일 전체의 생성·재적합/직렬화 동등성 시험이 아니다(`:335`–`:365`).
- **W는 실제 최종 화면 대조가 아니다.** W_PROBE는 `transform_network_summary_4col`까지만 실행한다(`:370`–`:385`). `_load_case_tables`, `normalize_network_summary_layout`, `single.html`은 실행하지 않는다. 정상/비관통·Physics null만 있고 split/이미4열/주 Hertz 결측은 빠져 있다. 앞 P2 반례가 정확히 이 후처리에서 발생한다.
- 독립 base/source의 `normal_new.raw_rows`는 동일했다. 그러나 전체 loader/렌더는 정상 새 표도 `R_brug` Physics **2.0×→1.4×**, Δ **0%→−30%**로 변한다(양쪽 정상 동일 fixture). 이는 `app.py:2271`–`:2281`의 의도된 correction이며 source numeric solver drift라는 뜻은 아니다. 따라서 요청서의 “새 표 정상 = 동일”은 **transform 함수 한정**으로 쓰고 최종 화면 의도변경도 별도로 싣는 것이 정확하다.

결론: A4의 정상 수치 보호 증거 자체를 폐기할 이유는 없지만, 전체 L214-03 닫힘이나 최종 화면 무영향 증명으로는 불충분하다. 최종 loader/템플릿, 실제 split CSV, H0 결측, 전자·이온, 모드비 결측을 추가해 반례를 닫아야 한다.
