# LHS214 FULL 모형 한계 수정 재검증

검토일 2026-10-15. 검토 핀 `9e3ef54ca228111360bfe5f6d9dad4ebe26d54af`, 비교 기준 `0c557e72aaffdf6cfd033c0667c643de4501c5b1`. 대상은 요청서의 L214-01–03 수정과 §9 대기 지문이다. 같은 핀의 별건 Rint 변경은 판정 범위 밖이다.

**판정: 세 항목 모두 부분 해결, 닫힘 보류. 새 P2 세 묶음과 P3 한 건. 새 P1은 입증하지 않았다.** 정상 사례의 수치 무영향 대조는 같은 환경에서 32/32 통과했다. 그 사실과, 비정상·복합 상태의 수용 및 화면 경로에 반례가 남았다는 사실은 양립한다.

생산 코드·등록·원장·Git 상태는 수정하지 않았다. 작은 합성 회로·게시 경로, 등록된 real14/case15 대조, 읽기 검산 및 합성 배포 시험만 실행했다. 새 214 생산과 WSL 발사는 하지 않았다. 아래 재현 명령은 이 증거 묶음의 루트에서 `python`이 NumPy/SciPy/Flask 등 리포 의존성을 갖춘 Python을 가리킨다는 전제다.

## 1. Q1 닫힘 판정

| 원 항목 | 판정 | 닫힌 부분 | 남은 반례 |
|---|---|---|---|
| L214-01 수치 인증과 출력 거부 분리 | 부분 | 무효 기하 우선, 원 정밀도 1.5 경계, 적용 채널·가지 제한, accepted 값 null, 진단 q 보존, 기존 수치 사다리 불변 | 재구성 q의 무한대 및 채택 시도와 요약의 모순을 공용 증서 검사가 허용 — L214R-01 |
| L214-02 모든 소비 경로의 같은 계약 | 부분 | 세대 결손·CF 증서·다른 채널 실패 차단, 전자/열 상태 전파, L0 H0 배포 HOLD | 띠 폴백과 함께 생긴 H0 모형 한계는 배포 HOLD에서 사라짐 — L214R-02 |
| L214-03 strict missing | 부분 | 기본 새 표·두 열 표의 Physics 결측, 전자 최종 표시 개선 | 남아 있는 CSV 숫자가 최종 병합에서 복원됨 — L214R-03 |

옛 13건의 원인은 여전히 unknown으로 남겨야 한다. 이번 반례는 그 13건의 원인 판정이나 과거 214 결과의 오염 증거가 아니다.

## 2. L214R-01 P2 수치 증서가 비유한 재구성과 내부 모순을 수용

위치: 고정 핀 `scripts/network_conductivity.py:993–998`, `:1005–1015`. [재구성 검사](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9e3ef54ca228111360bfe5f6d9dad4ebe26d54af/scripts/network_conductivity.py#L1005).

### 반례 A 유한 입력에서 중간 연산이 넘침

실제 21노드 합성 생산자의 Physics 모형 한계 레코드에서 원 진단 q는 **2.593468501694396**이다. 기하와 출력 null을 유지하고 증서 전류를 `I_bottom=1e308`, `I_top=-1e308`, `sum_g=1e308`로 바꾸며 마지막 pass 시도의 전류도 맞춘다. T=20, A=1, ΔV=1이므로 재구성 `q_rec=((I_bottom/ΔV)·T)/A=+inf`다. 저장된 q는 위의 유한 값 그대로다.

현재 상대 비교는 `abs(q−inf) <= 16ε·abs(inf)`, 즉 **`inf <= inf`**로 참이다. 이어서 재구성 q와 저장 q의 `>1.5` 검사도 참이다. 실제 반환은 다음과 같다.

| 함수 | 반환 |
|---|---|
| `full_model_limit_problem` / `ion_record_problem` | `None` |
| `certificate_binding_problems` | `[]` |
| `network_generation_contract` | g2, 문제 `[]` |
| `channel_verdict` | `ok` |
| 모드 파일을 읽은 `network_content_verdict` | `True, 'ok: hertzian, physics'` |

T=A=1e308인 별도 증서에서도 같은 현상을 재현했다. 반면 실제 `solve_network`는 환산 중 q가 무한대가 되면 `non_finite`로 거부한다. **생산자와 소비자가 같은 유한성 계약을 보증한다는 결론이 무너진다.** 실제 침대에서 1e308 전류가 발생했다는 주장은 아니다. 모든 입력 필드를 유한하게 유지한 공격에서도 수용 함수가 내부적으로 불일치한 q를 받는다는 반례다.

### 반례 B 마지막 채택 시도의 실패 기록을 보지 않음

같은 실제 생산 레코드의 마지막 시도 `residual_rel`만 **1.0**으로 바꿔도 위 모든 함수가 통과한다. `conservation_rel=1.0`, `krylov_info=1`도 각각 통과했다. 상위 요약의 작은 잔차와 `outcome='pass'`만 남으면 채택 시도의 모순이 가려진다. 대조군인 outcome 변경·마지막 전류 변경은 거부된다.

이는 정상 생산자가 실패한 해를 채택한다는 증거가 아니라 **증서 내부 모순을 소비 검사가 거부하지 않는 문제**다. 앞선 실패 시도는 사다리의 정상 기록일 수 있으므로 전부 금지할 일이 아니다. 마지막 채택 시도의 수치·성공 상태가 최종 요약과 맞아야 한다.

최소 해제 증거:

- T/A와 q_rec를 비교 전에 유한 양수로 확인하고 넘침·밑넘침을 기술 실패로 정리할 것. `scale=1e200`의 `scale**2` 예외도 안전하게 사유화할 것. 이 예외 자체는 현재 상위 검사에서 실패하므로 별도 false-green은 아니다.
- 마지막 채택 시도의 잔차·보존·방법별 수렴 상태·예외 여부와 최종 요약을 결합할 것. 두 반례가 증서→모드 파일 소비에서 거부되고 정상 fallback 성공은 유지되어야 한다.

재현: `python -X utf8 -B probes/l214_numeric.py`. 증거 `evidence/numeric_probes.json`의 `records.overflow_q_reconstruction_currents`, `contradictory_attempt_residual_rel`, `certificate_mutations`. 직접 풀이 탐침 38개, 증서 변이 14개, 레코드 탐침 5개.

## 3. L214R-02 P2 띠 폴백이 H0 모형 한계 배포 차단을 숨김

위치: `scripts/tau_flux.py:1234–1236` 및 `scripts/lhs_release_build.py:666–680`, `:2231–2235`, `:2438–2440`. [상태 우선순위](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9e3ef54ca228111360bfe5f6d9dad4ebe26d54af/scripts/tau_flux.py#L1234), [배포 식별자](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9e3ef54ca228111360bfe5f6d9dad4ebe26d54af/scripts/lhs_release_build.py#L666).

L1/L2 띠 폴백이 있으면 τ가 `BAND_FALLBACK`과 공란 사유로 먼저 반환된다. 배포는 `NOT_COMPUTED + full_over_conduction`만 모형 한계로 인식한다. 따라서 **표시 우선순위가 배포 자격 사실까지 지운다.**

| 실제 생산자 합성 입력 | H0 진단 q | 게시 | 다시 읽기 | 인계 τ 상태 | 실제 빌드·대조 |
|---|---:|---|---|---|---|
| L0 대조 | 1.6231747351909995 | done | K1–K7 PASS | NOT_COMPUTED / full_over_conduction | ReleaseError, 정상 HOLD |
| L1 + H0 모형 한계 | 8.927503013108073 | done | K1–K7 PASS | BAND_FALLBACK / 공란 | 27파일 생성, 경고 `[]`, check `[]` |
| L2 + H0 모형 한계 | 35.710012052432674 | done | K1–K7 PASS | BAND_FALLBACK / 공란 | 27파일 생성, 경고 `[]`, check `[]` |

상태 문자열을 만들어 넣은 시험이 아니다. 작은 사슬의 상자 크기를 바꿔 실제 생산·게시·`load_tau_results` P0–P4·인계를 실행했다. 작은 상자의 구 부피 분율은 물리적 침대 범위를 넘는다. 따라서 이는 **허용된 소비 계약의 조합 반례**이며 실제 침대 발생률·물리 타당성 검증이 아니다.

빌드 시험의 나머지 213행과 감사·배치 기록은 기존 selftest의 합성 fixture다. 선택행은 실제로 검증한 생산·인계 칸 및 K1–K7 결과를 넣었다. τ 다시 읽기 비교 함수는 유지하고 원천 공급만 시험용 어댑터로 연결했다. `build_v13(dry_run=False, diagnostic=False)`와 `check_v13` 자체가 위 결과를 냈다. 실제 214 생산 배포가 통과했다는 뜻은 아니다.

무너지는 결론은 요청서 §5-4의 **“H0 모형 한계는 진단 게시하되 실제 v1.3 주 타깃 배포에서는 항상 HOLD”**다. 수치 null은 유지되므로 잘못된 σ가 학습 값으로 채워졌다는 반례와도 구별한다.

최소 해제: τ 앞 게이트 우선순위는 유지할 수 있으나 canonical FULL 모형 한계 사실을 독립적으로 보존해 빌드·대조가 읽어야 한다. L0/L1/L2 × H0/Physics/H12 교차 시험이 필요하다. 모든 BAND_FALLBACK 행을 새로 금지하는 처방은 요구하지 않는다.

재현: `python -X utf8 -B probes/l214_consumers.py` 후 `python -X utf8 -B probes/l214_consumers.py --release`. 증거 `consumers_probe.json`, `consumers_handover_rows.json`, `consumers_release_probe.json`, `consumers_release_verified/`. 모두 `evidence/` 아래이며 생성 묶음은 시험 전용이다.

## 4. L214R-03 P2 최종 화면이 미채택 값을 옛 CSV에서 복원

위치: `webapp/app.py:687–700`, `:2020–2038`, `:2956–2957`; CSV 생산 `scripts/analyze_contacts.py:363–389`; 게시 목록 `webapp/pipeline_service.py:61–67`. [최종 split 병합](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9e3ef54ca228111360bfe5f6d9dad4ebe26d54af/webapp/app.py#L2020).

실제 합성 Physics 모형 한계 생산 결과는 accepted Physics σ가 없고 사유가 `full_over_conduction`이다. 기존 CSV에 명시적으로 옛 표시값을 넣으면 다음처럼 최종 `single.html`에 나온다.

| 입력 형태·모드 | 최종 표시 반례 |
|---|---|
| 현행 분석기가 쓰는 Hertz/Physics split CSV | 이온 σ `0.6 / 0.9 / +50.0%`, Plastic amplification `1.50× / 1.50× / 0%` |
| H0도 모형 한계인 생산 결과 + 두 열 CSV | Hertz σ `0.6`, R_brug `2.0×`가 남음; Physics만 결측 |
| 이미 네 열인 CSV | `0.6 / 0.6 / 0%` 그대로 통과 |

같은 화면의 상태 행은 `FULL 모형 한계`, τ 행은 `NOT_COMPUTED(full_over_conduction)`이라고 표시한다. 숫자와 상태가 서로 모순된다. 특히 `_csv_mode_row`에서 한 번 가린 Physics 값도 뒤의 split 병합이 다시 채운다.

옛 CSV 값은 독립 탐침이 주입한 합성 변이다. 다만 CSV를 **실제 게시 전에** 놓고 네 작은 생산자 실행을 거쳤으며 게시 뒤 해시는 네 건 모두 그대로였다. network 게시 목록은 contact 단계의 CSV를 갱신하지 않는다. 따라서 원자적 게시가 이 상황을 막아 주지는 않는다.

실제 앱 import·loader·전체 템플릿으로 소스 68건, 기준 52건을 렌더했고 실행 오류는 0이었다. 합성 metrics 52건씩은 Flask GET까지 실행했다. 나머지 소스 16건은 실제 생산자 결과를 loader와 전체 Jinja 템플릿에 넣었다. 이 수는 렌더 실행 수이지 결함 검사가 68건 모두 통과했다는 뜻이 아니다.

최소 해제: 최종 병합 뒤에도 현재 모드별 수치·상태를 우선해 이온 σ와 FULL 유도비를 가릴 것. H0 결측, split 및 네 열 CSV를 포함해야 한다. “Hertz 칸은 무조건 CSV 그대로”라는 기대는 이 경우에 적용하면 안 된다. 비가 미제공인 `Plastic amplification`의 `— / — / 0%`도 Δ `—`로 함께 정리할 것.

재현: `python -X utf8 -B probes/l214_display.py --tree source --producers` 및 `python -X utf8 -B probes/l214_display.py --tree base`. 증거 `evidence/display_source.json`의 `producer_ml_physics_split`, `producer_ml_hertz_csv`, `producer_ml_physics_fourcol`과 같은 이름의 HTML. 과거 214 화면의 실제 오염을 입증한 것은 아니다.

## 5. L214R-04 P3 비준 전환 절차가 역사 지문과 충돌

현재 pending 때문에 발사가 통과하는 우회는 찾지 못했다. 그러나 등록 문서가 안내한 **“비준 시 §3만 새 지문으로 바꾸고 pending 선언 삭제”**를 문서 사본에 그대로 실행하면 `R0,D1` 실패가 남는다.

이유는 `supp20_input_receipt.py:118`이 §3이 아니라 문서 전체의 `` `code_fp <64hex>` ``를 읽기 때문이다. 활성 값은 보충 등록 `:42`에 있고, 역사 표 `:104`에도 옛 값이 같은 기계 구문으로 남는다. [파서](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/9e3ef54ca228111360bfe5f6d9dad4ebe26d54af/scripts/supp20_input_receipt.py#L118).

실제 함수 결과:

- 현재 문서: rc 1, 실패 `{D1}` — 의도한 대기 상태.
- §3 갱신 + pending 삭제 + 옛 표 보존: rc 1, `{R0,D1}`, `registered=None`.
- 대조용 사본에서 옛 기계 토큰까지 모두 새 값으로 치환: rc 0.

마지막 대조는 원인 분리용이지 역사 기록을 새 값으로 덮으라는 처방이 아니다. 활성 §3만 읽게 하거나, 역사 SHA는 그대로 보존하되 활성 토큰과 다른 구문으로 구별해야 한다. 비준 전환 시험도 **역사 표를 보존한 문서**로 해야 한다. 현재 selftest의 비준 쌍둥이는 전역 치환이라 이 구멍을 놓친다. false-green이 아니라 향후 불필요한 차단이다.

재현: `python -X utf8 -B probes/receipt_identity.py`. 증거 `evidence/receipt_identity/results.json`, `variants.minimal_activate_section3`.

## 6. Q2 설계 선택 열 가지

| 요청서 §5 | 답 |
|---|---|
| 1 무효 기하 우선 | 동의. 무효 입력을 증명된 0으로 읽지 않는 것이 맞다. |
| 2 q 재구성·16ε | 유한 영역에서 동의. 같은 순서와 엄격한 원 정밀도 경계 유지. L214R-01 유한성 검사를 먼저 붙여야 한다. |
| 3 Σg 증서 | 동의. 병렬 상한을 소비자가 대조할 수 있다. 다만 같은 레코드의 Σg는 원 간선에서 독립 재계산한 증거가 아니다. |
| 4 H0 진단 게시·주 배포 HOLD | 조건부 동의. 게시부터 막을 필요는 없다. L214R-02처럼 배포 자격 정보가 사라지면 안 된다. |
| 5 관통 분류 1 | 모형 한계가 실제 관통 망이라는 조건에서 동의. 정상 σ 제공·물리 정확성을 뜻하지 않는다. |
| 6 K2의 0b 실패 위임 | K4/K6/P4가 반드시 붙는 경로에서는 동의. q×1.01에서 K2 통과, K4/K6 거부를 재현했다. K2 단독을 증서 유효성 보증으로 부르지 말 것. |
| 7 띠 폴백 우선 | 표시 순서는 수용하되 **독립 모형 한계 원인 보존**이 필요하다. 현재 배포 식별과 충돌한다. |
| 8 옛 화면도 strict missing | 동의. 예전 오류 표시도 고쳐야 한다. 수치 변화가 아니라 화면 수정으로 보고하고 최종 경로를 시험할 것. |
| 9 non_finite 기술 실패 | 동의. 생산자뿐 아니라 재구성 소비자에도 같은 기준이 필요하다. |
| 10 재적합 제외·별도 집계 | 동의. L1/L2처럼 앞 상태가 덮어도 실제 모형 한계 원인 집계에서 빠져서는 안 된다. |

CF 잔차 1.0, bulk_model 결손, q×1.01, 전자/열 실패, 사유 꼬리 추가, Physics에 H12 증서의 7변이는 실제 게시/정지/다시 읽기/인계 조합에서 모두 거부됐다. 어떤 중간 함수 하나의 PASS만으로 전체 우회라고 판단하지 않았다.

## 7. Q3 A4 무영향 증거

**계산 수치에 대해서는 제출 범위 안에서 수용, 화면 닫힘에는 불충분.** 원 A4의 N/T/R/W 함수와 비교 코드를 바꾸지 않고 별도 사본에서 32/32를 재현했다. Git 읽기 호출만 SHA256·Git blob·크기가 검증된 고정 사본 공급으로 대체했다. 생산자 예외를 양쪽이 똑같이 내서 통과한 건은 0이었다.

- N16: 합성·real14·case15, 직접/반복 풀이를 포함해 기존 수치·기존 증서 동일. 추가 전자/열 상태·사유 네 키는 따로 비교. 정상 비교에 모형 한계 진단 키가 들어온 경우 0.
- T6: 구세대 τ 원천 194행 9,894칸 및 지정 레코드 대조. 이는 새 214 전수 결과 비교가 아니다.
- R2: 기존 인계표의 48,822칸에 대한 공란·관통·상태·주 타깃 관문 해석 동일.
- W8: 2개 동일성 및 6개 의도된 변화 조건을 통과. **32/32 전부가 숫자 비트 동일 비교인 것은 아니다.**

유한 float 비교는 `float.hex()`라 ±0도 구별한다. 두 NaN을 같다고 처리하므로 NaN payload 비트 보장으로 확장하지 않는다. 같은 환경의 CG 대조 G는 양쪽 모두 `0x1.16d424c7fc33ep+5`였고 제출 로그의 `…c346`과는 다르다. 운영체제·수치 라이브러리 사이 비트 동일이 아니라 **같은 환경의 전후 동일성**이다.

W는 `transform_network_summary_4col`까지만 실행한다. loader→normalize→템플릿을 넣으면 정상 새 표도 R_brug Physics가 **2.0×→1.4×**, Δ가 **0%→−30%**로 바뀐다. 이는 의도한 표시 교정이지 솔버 표류가 아니다. “정상 새 표 동일”은 변환 함수 범위로 좁히고 최종 표시의 의도 변경을 별도 등록해야 한다. L214R-03의 레이아웃·H0 결측 조합도 추가할 것.

재현: `python -X utf8 -B probes/l214_a4.py`. 결과 `evidence/a4_independent.json`. 핀의 scripts/webapp 변경 파일은 실제 트리 비교로 23개다. 요청서의 초기 A4 로그 13개 이후 영수증·별건 Rint 등이 포함됐다. 이 목록 차이를 숨기지 않되, 그 별건을 이번 검토의 승인 대상으로 넓히지는 않는다.

## 8. Q4 등록 초안과 Q6 대기 지문

**Q4: B6에 필요한 항목은 초안에 들어 있다. 활성 등록의 닫힘은 아니다.** 194 §9-8과 보충 §9-3은 코드 신원, 허용 범주, 결과 자격, 공란 의미, H0 주 타깃, 결과 열람 후 정책 개정 이력, 불변 문턱·입력, 두 배치별 관문을 담는다. 보충 자료라는 이유로 H0를 면제하지 않은 것도 맞다.

다만 앞 게이트 우선과 H0 HOLD가 동시에 지켜지도록 L214R-02의 독립 분류를 반영해야 한다. 새 pin의 해시·인계 도구 지문, 저자 비준, B7 사전 점검·손 대조·발사 승인, C8 새 실행, C9 실물 인계는 아직 남는다. S3 HOLD도 별개로 유지한다.

**Q6: pending 설계 자체는 수용. selftest PASS와 발사 PASS는 분리돼 있다.** CODE_FILES 32개를 직접 재해시했으며 바뀐 것은 요청서대로 network_conductivity·tau_flux·app·pipeline_service 네 파일이다.

| 지위 | 전체 code_fp |
|---|---|
| 활성 등록·기준 코드 | `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71` |
| 검토 코드·pending | `acc7bfa335ec8fa8a7b76eb981135f16994b084ce0746476c5d05f61488af2ed` |

현재 실제 컨테이너 영수증은 D1 실패. selftest는 pending에서 컨테이너 `{D1}`, 사전 점검 `{D1,E2}`, 발사 기록 `{D1,F5,G5}`를 정확한 집합으로 검사하며, 승인 쌍둥이에서 음성 대조를 다시 실행해 기존 실패에 가려지지 않게 했다. 의존성 경로만 공급한 동일 도구로 **99/99 PASS**를 재현했다. 문서의 pending을 다른 값으로 바꾸거나 지워도 실제 D1은 통과하지 않는다. 상충 pending은 R0도 실패한다.

남은 반례는 L214R-04의 비준 전환 문서다. 이를 추가하되 실제 발사 대조를 pending까지 허용하도록 완화하면 안 된다. 이 재검증은 입력 영수증의 통과도, 발사 승인도 아니다.

## 9. 시험 범위와 최소 해제 목록

개별 로그와 환경 적응 내역은 `README.md`, `evidence/`, `notes/`에 있다. 신규 모형 한계 시험 55/55, τ 55/55, 세대 역할 44/44, 게시→인계 체인 34/34, provenance 284/284, v1.2 다시 읽기 22/22, g2 다시 읽기 29/29, 영수증 99/99를 재현했다. 배포 회귀는 **254/256**이다. 남은 V10a는 Windows 경로 표기, V16a는 Git 없는 검토 사본의 HEAD 요구이며 봉인·인계 파일 해시는 일치한다. 이를 임의로 256 PASS로 재계수하지 않았다. 전체 check_all이나 WSL 생산 사전 점검을 모두 통과했다고 주장하지 않는다.

다음 재확인에 필요한 최소 범위:

1. L214R-01의 비유한 재구성과 마지막 채택 시도 모순을 공용 증서에서 거부. 정상 사다리·경계 대조 유지.
2. L214R-02의 독립 모형 한계 사실을 인계·빌드·check까지 전달. 띠 폴백을 통째로 금지하지 않고 실제 교차 반례 차단.
3. L214R-03의 split/네 열/H0 결측을 최종 화면에서 차단. σ뿐 아니라 FULL 유도비·Δ까지 같은 규약.
4. L214R-04의 역사 값을 보존한 비준 전환 시험. pending은 실제 발사 허용값이 되면 안 됨.
5. 수정 후 최종 코드 지문으로 등록·비준·B7을 별도로 진행. 과거 결과나 승인 핀을 소급 변경하지 말 것.

수치 계산 교정 방향과 범주 분리는 지지한다. 그러나 현재 핀으로 L214-01–03을 verified로 닫거나 새 214·v1.3 주 타깃 배포를 해제할 근거는 부족하다.

**HOLD**
