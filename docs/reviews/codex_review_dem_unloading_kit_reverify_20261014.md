# DEM 언로딩 키트 재확인 — ULKR-01–12 · 등록 개정 3

검토일: 2026-10-14 · 고정 핀: `a30fe150e21f66aea2f1c360593e1cd781689b14` · 브랜치: `claude/stoic-knuth-NObVQ`

## 1. 판정

**전체 HOLD. 기존 반례의 수정은 실질적이다. 그러나 새 P1 3건과 파싱 P2 1건이 남는다.**

1. **ULKRR-01 / P1:** 새 문법 fixture가 단일값 `ave/time`을 벡터로 읽는다. 고정 버전 소스상 첫 창 뒤 오류가 나므로, 필요한 반복 이동·상태 복귀를 끝까지 시험할 수 없다.
2. **ULKRR-02 / P1:** RESUME가 전혀 없어도 중복 확인 단을 지워 버린다. 비정상 확인 기록이 사라진 뒤 `primary=OK → UVa 허용`을 재현했다.
3. **ULKRR-03 / P1:** 러너가 기록한 판독기 실패 `reader_rc≠0`를 다음 관문이 무시한다. 실제 Python 명령이 파일 발행 뒤 실패해도 UB를 허용했다.
4. **ULKRR-04 / P2:** 소수 ID가 정수 ID로 잘려 정상으로 사용되고, 필수 `id` 열 부재는 관측 결손 대신 `KeyError`가 된다.

이는 물리 목표·문턱을 다시 정하라는 판정이 아니다. `unload_params.json`은 이전 핀과 **내용 전체가 동일**하고, H0–H5 기존 덱 8개도 바이트 동일하다. 이전 실제 이력 증거를 새 판독기로 다시 읽어 H0–H5 PASS 및 제출 판정 전체 일치를 재현했다. 그 증거를 철회하거나 같은 시험을 다시 요구하지 않는다.

**본 R · 10:0 연장 · U 실행 해제는 아직 아니다.** 문법 fixture 수정·실제 PASS와 아래 최소 해제 조건이 남는다. 이번 검토에서는 DEM, LIGGGHTS, MPI, WSL, SSH, 스케줄러를 실행하지 않았고 대상 코드·원장·Git 상태를 바꾸지 않았다.

## 2. 핀·봉인·검증 범위

사용자가 최신 커밋 조회·고정을 승인한 뒤 위 SHA를 고정했다. 이후 브랜치 끝을 따라가며 혼합하지 않았다. `source_manifest.json`의 203개 파일을 Git blob 및 SHA256으로 대조했고, 시험 뒤에도 원본 203개 바이트가 동일하다.

| 대상 | SHA256 / 결과 |
|---|---|
| 키트 `SHA256SUMS` | `213695a0be89c7b6f8d59aea0b3132bf0cd080079a6de198a8e8c9964671aa86` — 요청서와 일치 |
| history `SHA256SUMS` | `debe83877657978cdaf87b18e08edda501e520979dd40876f5e100c24e902163` — 요청서와 일치 |
| 기존 실제 이력 archive | `be0acbd7841d0922604eee8aa31524fcddbe179a8240f937b317432dbebb0ca0` |
| 실제 이력 다시 읽기 | rc 0 · H0–H5 모두 PASS · `run_dir` 외 제출 JSON 전체 동일 |
| 생산 덱 | 64/64 커밋 바이트 = 현 생성 결과 |
| history 덱·판 | 9개 덱 및 판 생성 대조, 15파일 봉인 PASS |
| 고정 LIGGGHTS 소스 | `3d5c00f20519e6bb6eb6756f51f1ad36564e649d` · 기존 검토의 47개 원본/해시 재사용 |

기존 실제 이력 archive 안 봉인은 **옛 history 봉인**이다. 새 fixture 추가로 현재 봉인과 다른 것은 예상된 세대 차이이며, 이를 새 문법 시험 PASS로 재라벨하지 않았다. 기존 8개 덱과 실제 사용 덱의 바이트 대조로 H0–H5의 유효 범위만 보존했다.

이하 `ul_reader.py` 등 키트 경로는 `docs/data/ps45_unload_20261009/` 기준이며, 줄 번호는 위 핀 기준이다. 원본은 동봉 `source/`, 고정 LIGGGHTS 원본은 `upstream/`에 있다. 수치 반례는 따로 표시한 기존 실측 이력 외에는 **합성 입력**이다.

## 3. ULKR-01–12 닫힘 범위

여기서 ‘닫힘’은 **해당 지적의 수정·지정 반례**에 대한 뜻이다. 전체 키트 실행 인증이나 실제 분말의 물리 검증이라는 뜻이 아니다.

| 항목 | 판정 | 재검증 결과·남은 한정 |
|---|---|---|
| ULKR-01 확인 두 단 | **해당 수정 닫힘** | UNSTEADY·NaN·S3 실패·잘못된 kind/phase·누락은 주 값과 UVa를 막음. 접촉 없는 정상 확인 두 단은 통과. 중복 행 처리의 별도 결함은 ULKRR-02 |
| ULKR-02 모든 교차 합집합 | **닫힘** | 첫 A 교차 `[0,0.2]`, 여러 교차 `[0,0.5]` µm 포함. 기존 거짓 SEPARATED 사례는 OVERLAP. 뒤쪽 비유한 압력은 주 값 보존·합집합 미계산 |
| ULKR-03 UT 부모·UTc·최종 보고 | **해당 수정 닫힘** | 정상 t3 최종 ρ `0.3827035983143033 %` 보존·보조 DONE. 사용 부모 파일 변조·해시 결손·경계 중복·첫 단/창 누락·RESUME 부재는 이어 돌림 거부, UT 주 값은 보존하고 보조 SEP_INCOMPLETE |
| ULKR-04 관측 완전성 | **부분** | 기존 NaN 행 재활용·시점·정수 중복 ID·CSV 열 수·k 결손 반례는 차단. ULKRR-02/04 잔존 |
| ULKR-05 복원·다음 관문 | **부분** | 불완전 PRE/POST·UN 다른 정수 ID·잘못된 네 시점·Ut0/R/UN 기술 실패는 차단. 소수 ID와 판독기 실패 증서 재사용은 ULKRR-04/03 |
| ULKR-06 RESUME 범위 | **소스 수정 수용 / 실행 확인 부분** | 미지원 JOB 선행 거부, 같은 ALLOW 팔·첫 시도·요약 없음·한 번, 로그 분리·덱 대조가 있음. 이 환경에서 Bash 모의 러너는 시작 전 막혀 실행 인증하지 못함 |
| ULKR-07 재접촉·DONE | **원반례 및 승인된 예산 해석 닫힘** | 재접촉은 같은 k 유지, 남은 예산 종료. DONE 사건·벽 관측 불일치는 보조 미완료. 행 간격 완전성은 §6의 비차단 보강 사항 |
| ULKR-08 SYN·부호·총힘 시점 | **닫힘** | SYN 부재/실패·잘못된 부호·총힘 시점 부재·잘못된 schema 모두 복원/UB 차단. 기존 실제 이력 판정은 그대로 수용 |
| ULKR-09 UK 세 완전 창 | **새 기준 파일 생성 경로 닫힘** | 정상 3창 S2=`2.24e−6 덱 J`; 1/2창·중복·간격 누락·이동·NaN·다른 S0·기술 실패는 기준 파일 미발행. 임의로 남겨 둔 옛 파일의 폐기까지 인증한 뜻은 아님 |
| ULKR-10 중력 유지·g | **A/B 닫힘** | 20덱 전부 첫 4–12창; 이후 UB/UT3 4–12, UVa/UVb 8–24. 실제 g 배선 합성 시험은 일반 R≈`1e−6` PASS, G_* R=`1` FAIL |
| ULKR-11 오류 코드 | **원 수정 수용 / 종단 관문 부분** | G0/Ut0 실패 후 R 중단·판독 rc 기록은 소스상 구현. 그 rc를 다음 관문이 소비하지 않는 ULKRR-03 잔존. Bash 종단 실행은 미검증 |
| ULKR-12 ε·W·포장 | **판독·보고 수정 닫힘 / 포장은 소스 확인** | S0 고정부피, 끝점 불완전 시 해당 ε만 미계산, S0→M W·최종 보고 보존. EXT2/결정/기준/선택 파일 포장 분기 있음. 실제 셸 포장 실행은 이번 환경에서 미검증 |

주요 양성 대조: 정상 교차 후 보조 TIMEOUT이어도 ρ=`0.2026077873428664 %` 유지. 정상 확인 두 단의 판 접촉 부재 때문에 주 값을 지우는 과잉차단은 발견하지 않았다.

## 4. 새 결함 — 최소 해결과 검산

### ULKRR-01 · P1 — 문법 시험이 scalar를 vector로 읽음

**자리:** `history_test/make_history_decks.py:732,765`; 생성 덱 `history_test/in.hist_grammar.liggghts:77,132–133`.

```text
fix gr_av all ave/time 10 10 ${gr_W} v_Ps
...
variable gr_P equal f_gr_av[1]
variable gr_P equal ${gr_P}
```

고정 `fix_ave_time.cpp:350–368`에서 scalar 모드 입력 하나는 `scalar_flag=1`, 둘 이상만 `vector_flag=1`이다. `variable.cpp:1182,1198,1315`는 `f_ID`와 `f_ID[i]`를 구분하며, 해당 타입이 아니면 `Mismatched fix in variable formula`를 낸다. 따라서 GA의 첫 `run` 2000→2100 후 `${gr_P}`를 동결하는 자리에서 실패한다. 첫 GRAM_STEP·상태 파일·반복 이동·GB 재개에 도달할 수 없다.

**이것은 고정 C++ 소스에 의한 오류 증명이며 실제 바이너리 오류 로그를 관측한 것은 아니다.** 생산 U 덱의 `ul_av`는 P·병진 KE·회전 KE 세 값을 가진 벡터이므로, 그 `f_ul_av[1..3]`까지 같은 오류라고 확대하지 않는다.

생성기 모의기 `make_history_decks.py:813`은 `f_*` 및 인덱스 참조를 0으로 치환한다. 현재 `[1]`, 올바른 scalar 표기, 불가능한 `[999]` 모두 같은 성공 trace를 냈다. 자체시험은 이 타입 결함을 판별하지 못한다.

**무너지는 결론:** “새 fixture가 빠진 네 언어 경로를 실제 실행할 준비가 됐다.” H0–H5/SYN 실측 성공은 무너지지 않는다.

**해결 증거:** 생성기에서 scalar `f_gr_av`로 정정하거나 의도한 다중값 출력을 정의 → 재생성·재봉인 → 잘못된 타입 접근을 잡는 음성 시험 → 수정된 실제 바이너리 문법 fixture PASS. 시험 자체가 실패할 것이므로 현재 fixture를 그대로 ibb에 보내지 않는 것이 낫다.

**재현:** `probes/grammar_recheck.py`; `evidence/grammar_deck_recheck.json`의 `grammar_fixture.native_blocker`, `producer_model_blind_spot`.

### ULKRR-02 · P1 — 재개 없이 중복 행을 지워 확인 단을 정상화

**자리:** `ul_reader.py:85–94` `_supersede`, `:126` 무조건 호출, `:562–564` 소거 후 k 검사.

정상 UT의 k=3 확인 단 바로 앞에 **같은 step의 `steady=0` 행 한 개**를 추가했다. RESUME 사건은 없다. 실제 파일→팔 판독→선택→관문 결과:

```text
resume_steps=[]
n_superseded_rows=1
primary_status=OK, rho_pct=0.2026077873428664, why=[]
selection=need_UV, delta_dt=0.0, next=[UVa]
gate(UVa)=ALLOW
```

`_supersede`가 잘못된 행을 삭제한 뒤, 개선된 확인 단 검사에는 정상 행만 전달된다. 따라서 ULKR-01의 조건 자체는 고쳐졌지만, 입력 무결성이 그 조건을 우회한다.

**무너지는 결론:** “중복·비정상 원기록이 있으면 자동으로 선택 미해결이 된다.” 정상 단일 기록의 확인 논리는 무너지지 않는다.

**해결 증거:** 정식 재개 경계/시도 기록을 확인한 경우에만 해당 경계의 rollback을 허용. 그 외 중복·역행 step/k는 미식별. 승인된 진짜 RESUME 양성 대조와 본 no-RESUME 반례를 함께 선택·관문까지 검사할 것. 정상 재개를 전부 막는 단순 중복 금지는 답이 아니다.

**재현:** `probes/reader_recheck.py`; `reader_recheck.json/cases/duplicate_without_resume`.

### ULKRR-03 · P1 — 판독기 실패가 기록돼도 다음 팔 허용

**자리:** `run_unload.sh:197–203,220–222,274–278`; `ul_reader.py:863–875`, 다음 관문 `:896–913`, 파일 발행 CLI `:2387–2392`.

러너는 실패를 이제 정확히 기록한다. 그러나 `_job_restored`는 끝 줄의 `fails=0`만 읽고 `reader_rc`를 확인하지 않는다.

단순 receipt 변조만이 아니라 **수정하지 않은 실제 Python CLI**로 도달 가능한 사례를 만들었다. 완전한 합성 R/UN/UK 입력에서 표준출력 파이프를 닫으면 restore는 `RESTORED` JSON 발행 뒤 출력 flush에서 rc **120**으로 끝난다. kebase도 기준 파일을 새로 발행한 뒤 rc **120**이 된다. 원래 기준 파일은 이 합성 사례에서 제거한 상태였다.

러너 소스대로 합산되는 기록은 다음과 같다.

```text
reader_restore_rc=120
reader_kebase_rc=120
end=... fails=0 reader_rc=2
restore_verdict=RESTORED
new ul_base.in: S2=2.24e-6 (deck J)
gate(UB)=ALLOW
```

전체 Bash 러너를 실행한 결과는 아니다. **실제 CLI 실패·파일 발행·실제 다음 관문을 실행했고**, 그 사이 합산 receipt 필드만 인용한 러너 소스와 동일하게 재구성했다. 출력 오류가 수치 결과를 틀렸다고 증명하는 것은 아니지만, “기술 실패 잡을 승인 증서로 재사용하지 않는다”는 계약은 깨진다.

**해결 증거:** 완료 receipt의 `fails=0`과 **`reader_rc=0`을 모두 필수**로 대조. 누락·비정수·비영 값은 거부. 결과 파일 발행 후 명령 실패 음성 대조, 정상 `UNIDENTIFIED`/rc0 양성 대조를 함께 둔다. 단순히 판독 오류를 무조건 삼켜 rc0으로 바꾸면 안 된다.

**재현:** `probes/runner_recheck.py`; `runner_recheck.json/results/actual_restore_cli_closed_stdout`.

### ULKRR-04 · P2 — ID 타입·필수 열 오류를 끝까지 보존하지 못함

**자리:** `ul_lib.py:364` 전 열 float 파싱; `ul_reader.py:346,423–432,1020–1035,1162–1163`.

- UN 첫 ID `1→1.5`: `int(1.5)=1`로 바뀌어 **RESTORED 및 UB 허용**.
- 주 값 끝점 ID `2→2.5`: 정수 2로 사용돼 **primary OK, ρ=0.2026077873428664 %**.
- 끝점 머리 `id→not_id`: 파서가 열 결손을 이미 적었지만 `r['id']`를 먼저 읽어 **`KeyError('id')`**. 이것은 false PASS가 아니라 약속한 관측 결손 상태를 발행하지 못하는 경로다.

정상 LIGGGHTS 출력이 소수 ID를 만든다는 주장은 아니다. 손상/오형식 입력을 정상 입자로 사용하지 않겠다는 방어 계약의 결함이다. 기존 실제 H0–H5 증거의 정수 ID를 부정하지 않는다.

**해결 증거:** 필수 열/파서 오류를 먼저 반환하고, ID는 유한한 양의 정수임을 검사한 다음 변환. S0·현재 원자·복원 관측·쌍 참조에 같은 타입 규약을 적용. 소수 ID와 필수 열 결손 모두 사유 있는 미식별/미계산으로 닫히는 회귀 필요.

**재현:** reader probe의 `parsing_fractional_atom_id`, `parsing_missing_column`; runner probe의 `fractional_un_id`.

## 5. Q1–Q7 답

| 질문 | 답 |
|---|---|
| Q1 정상 확인·접촉 불필수 | **동의, 해당 수정 닫힘.** 첫 교차 끝점 자격과 뒤의 등록 정상 확인 두 단을 구분한다. 정상 S1/S2·S3·유한·순서/완료 조건은 유지하며 접촉을 추가 요구하지 않아야 한다. 확인 압력에 별도 P≤P_meas 조건까지 코드가 강제한다고 확대하지 않는다. 다만 ULKRR-02의 원기록 소거는 별도 보강 |
| Q2 같은 단·SEPARATE·이동 초기화·사건 대조 | **동의, 원반례 닫힘.** 새 물리 문턱이 아니라 등록된 동일 높이·관측 순서의 검사다. 재접촉 w4는 k5에 머물러 w9 DONE, w12/13 재접촉은 같은 k에서 SEP_INCOMPLETE. 선언 w12→완료 w15는 개정 3에서 정당함. 완전한 시간 연속성을 보증하려면 §6의 행 간격 검사 보강 |
| Q3 ε/W의 위치·구간 | **동의.** 고정 S0 `C_all`로 ε_all, 중심 포함 ε_inside는 별개, M에는 ε_all만. t3는 UT에 S0→M이 있으므로 UT 값을 보존. 합성 손 계산 C=`2.1991148575128552e−5` 덱 m, W=`4.036875e−8` 보고 J와 출력 일치. W는 정착 단 사다리꼴 대리 관측량이지 실제 판의 연속 기계적 일이 아님 |
| Q4 문법 fixture·output.cpp 가정 | **설계 범위 동의 / 실행 가능성 열림.** 빠진 네 경로를 배치했으나 ULKRR-01 때문에 실제로 도달하지 못함. 변수 every는 setup/쓰기 뒤 재평가하는 미래 절대 step; 고정 주기는 정렬 step·last_dump가 핵심이며 `first yes` 예외가 있음. 실제 바이너리 PASS 전에는 모의기만으로 닫지 못함 |
| Q5 절차 vs 코드 관문 | **명시한 절차 관문도 최소 요구를 충족할 수 있음.** 이전 판정이 특정 JSON 코드 배선을 강제한 것은 아니다. 다만 실제 PASS·키트/fixture/바이너리 출처를 본 R 전에 검토해 기록해야 함. 자동 강제하려면 **R/EXT 실행 전** preflight에 두는 편을 권고. R 뒤 `restore_verdict`에만 붙이면 ‘본 R 전’을 강제하지 못함. 현 상태에서 PASS는 없음 |
| Q6 UC의 새 시도 | **조건부 동의.** UC는 restart를 만들지 않으므로 현 RESUME는 실제 LMP 호출 전에 거부. 실패 폴더 보존·새 폴더·관문 재검사·기술 실패/승인 이력 유지로 새 시도 처리 가능. 지원 목록은 `UC=fresh-attempt-only`로 분명히 쓰는 편이 낫고, 새 폴더가 등록된 재시도 제한이나 결과 선택을 초기화하지 않음 |
| Q7 verified 범위 | **§3·§7대로 제한.** 코드·파일→판독의 특정 수정은 닫되, 실제 문법·Bash 종단 실행·새 무결성 결함까지 일괄 verified로 쓰지 말 것. 원장 파일은 이 검토에서 수정하지 않음 |

## 6. 별도 차단 finding으로 세지 않은 보강 사항

### 6-1. CSV 행 인접 ≠ 물리 창 연속

`ul_reader.py:262–300,721–744`는 남은 행 수로 분리와 post 창을 센다. 같은 k에서 w=`[1,2,4,5,6]`, SEPARATED=w2, POST_DONE=w6인 불완전 표를 주면 w2/4/5/6을 4창으로 읽어 DONE이다. **이 입력은 사건 기록까지 불완전 표와 맞춘 합성 조합**이며, 현 생성기가 정상 실행에서 그렇게 낸다는 증거는 없다. 정상 완료 기록에서 창 하나만 삭제한 모든 경우가 통과한다고 주장하지 않는다.

원 ULKR-07 반례는 닫되, Q2의 ‘연속’ 보증에는 고유·연속 w와 해당 팔 T_W에 맞는 step 간격을 대조하는 편이 정확하다. 누락 구간은 분리 연속성을 끊고, 유효한 w12 선언→w15 완료는 계속 허용해야 한다. 증거: `reader_recheck.json/cases/separation_missing_csv_window`.

### 6-2. 작은 문법 러너의 실패 후속 실행

README:136은 GA 실패 시 GB 없음이라고 하지만 `history_test/run_history.sh:130–137`은 rc보다 생성 파일 유무로 후속을 시작한다. 실패 전에 파일을 남겼다면 GB가 실행될 수 있다. **최종 reader는 실패 rc를 거부**하며 실제 함수 시험에서 GA/P rc1+모든 파일을 넣어도 FAIL/rc2였다. 거짓 PASS로 확대하지 않는다. 선행 rc와 파일을 함께 요구하고, ‘파일을 쓴 뒤 실패’ 음성 시험을 추가할 것을 권고한다.

### 6-3. EXT의 비영 rc 분류

`run_unload.sh:227–233`은 s0p의 어떤 비영 rc에도 EXT2를 시도하고 RRC를 0으로 초기화한다. 정상 연장 요청(rc2)과 예상 못 한 프로그램 오류(rc1)를 구분하는 것이 좋다. **이 분기의 Bash 실행 반례는 이번에 만들지 않았으며 새 독립 차단 항목으로 세지 않았다.** 누적 기술 오류를 성공으로 지워도 된다는 뜻은 아니다.

### 6-4. 이전 Codex 모의기의 수정

옛 `deck_control.py`는 한 dump ID의 다음 출력들을 계산하면서 공유 step을 옮긴 뒤, 다음 ID를 같은 setup 시각으로 되돌리지 않았다. 뒤 ID의 첫 프레임을 놓칠 수 있는 **검토 탐침 오류**였다. 이번 `grammar_recheck.py`는 모든 dump를 공통 시계로 처리했다. 옛 핀을 수정된 모의기로 다시 계산해도 옛 재접촉 k5→k6, w15 완료, 중력 유지 범위 결론은 그대로다. 대상 코드의 결함으로 전가하지 않는다.

고정 `output.cpp:224–245,339–355,638` 대조에서 같은 프로세스의 연속 run은 같은 step 중복 출력을 억제하지만, 새 프로세스에서 재생성한 fixed dump는 `last_dump=-1`이라 정렬된 restart step을 다시 쓸 수 있다. `first yes`는 별도 예외다. 상태 파일 복귀가 출력 객체의 last_dump까지 복원한다는 가정은 두지 않았다.

## 7. 기존 ULR1·UL 원장에 미치는 범위

| 원장 | 이번 권고 |
|---|---|
| ULR1-01 | 확인 정상성·옛 NaN 반례는 닫힘. 원기록 무결성 ULKRR-02/04 때문에 종단 보증은 부분 유지 |
| ULR1-02 · ULR1-04 | 기존 범위의 닫힘 유지: 정상 주 값/보조 TIMEOUT 분리, 물리 창 dt 연동 |
| ULR1-03 | 기존 재접촉·DONE 반례는 닫힘. 정상 생성 경로 제어와 임의 손상 관측의 완전성 보증을 구분 |
| ULR1-05 | 첫 교차 합집합·UTc 최종 주 값 보존의 지적은 닫힘. 전체 자동 선택/제출은 ULKRR-02/03 때문에 부분 |
| ULK-01 · ULK-02 | 기존 한정 닫힘 유지. 새 문법 fixture PASS를 대신하지 않음 |
| UL-01 | 복원 관측·이력 자격은 강화됨. 기술 오류 관문·타입 무결성·실제 문법 조건 때문에 전체 부분 |
| UL-02 | 실제 g 소비 수정은 닫힘. 모든 입력 파싱까지의 포괄 보증은 ULKRR-04 잔존 |
| UL-03 | 첫 교차 포함 외곽 합집합 알고리즘 닫힘. malformed 기록 일반 보증과 구분 |
| UL-04 | UT/UTc·유효 입력 결정표 개선 수용. parser/오류 관문과 셸 실행 확인은 부분 |
| UL-05 · UL-10 | 기존 문서 범위 수용 유지. 생산 결과·물리 가설·에너지 분율을 새로 측정한 것은 아님 |
| UL-06 | 원 분리/재접촉 반례 닫힘. §6-1의 창 간격 보강 권고 명시 |
| UL-07 | 유지 범위·실제 중력 g 배선 닫힘. 중력 민감도 결과는 아직 없음 |
| UL-08 | 물리 창·부모 자료 연결 개선 수용. 관측 무결성 전체는 부분 |
| UL-09 | S0 고정부피·ε/W 최종 보고 경로 닫힘. 실제 외피/연속 판 일과 동등하다는 주장은 아님 |

‘수정 파일이 있으므로 ULKR 전체 verified’ 또는 ‘새 문제가 나왔으므로 옛 수정 전부 무효’ 둘 다 이번 증거와 다르다. 새 ID와 좁은 기존 닫힘을 함께 기록하는 것이 맞다.

## 8. 실제 실행한 검증과 한계

| 검증 | 결과 |
|---|---|
| ul_lib / ul_s3 / ul_observers / ul_gates / ul_reader | 19/19 · 14/14 · 21/21 · 35/35 · 111/111, 모두 rc0 |
| seal 자체시험·파일·규칙 | 10/10 · 76파일 봉인 · 22규칙 PASS |
| 생성기 자체시험 | 289 통과, Bash 문법 호출 2개 환경 실패. **291/291로 보고하지 않음** |
| history 생성기 자체시험 | 154 통과, Bash 호출 2개 환경 실패. 모의기 통과가 ULKRR-01을 잡지 못함 |
| history reader 자체시험 | Python 부분 42 통과, shell 모의 호출 11개 환경 실패 |
| ul_runner_test | Bash 시작 불가 뒤 픽스처 폴더 미생성으로 중단. M 전체 실행 인증 불가 |
| make_unload_decks --check | 중첩 프로세스 출력 인코딩 오류. 별도 실제 렌더 64/64 바이트 대조와 독립 seal 검사는 통과 |
| 새 독립 reader probe | 56사례 중 기대 성질 52개 만족; 4개 잔여 현상은 §4·§6에 전부 공개 |
| 새 독립 복원/관문 probe | 정상 1개 + 음성 22개 기대대로; 추가 ID·rc 반례와 보강 사례 별도 보존 |
| 새 grammar reader probe | 합성 정상 PASS; GA/P 실패·벽 누락·시간 오류·복귀 높이/상태 오류·이동 중 추가 dump 등 7변형 모두 FAIL |
| 기존 실제 H0–H5 묶음 | 안전성 확인 후 206파일 읽기; 새 reader rc0, 제출 JSON과 동일 |

Windows Git Bash는 무해한 시작 명령도 `NtCreateDirectoryObject ... 0xC0000022`로 실패했다. 이것은 **검토 환경 제약**이며 새 키트 결함 수에 넣지 않았다. Linux에서의 자체시험 성공을 부정하는 것도, 대신 인증하는 것도 아니다.

옛 탐침 5개도 복사본 그대로 다시 실행했다. reader_adversarial·continuation·observer·history_restore의 rc1은 대부분 **“옛 잘못된 OK가 계속 나와야 한다”는 단언이 깨진 것**이므로 대상 회귀 실패로 세지 않았다. 특히 새 필수 복원 schema가 없는 옛 fixture의 단순 거부만으로 수정 입증을 끝내지 않고, 새 schema의 정상 양성 대조를 먼저 만든 독립 탐침으로 각 반례를 분리했다. 옛 deck interpreter 결과는 §6-4의 수정된 해석으로 교차확인했다.

## 9. 최소 해제 목록

1. ULKRR-01 수정·재봉인·타입 음성 시험 후 **수정 키트의 실제 grammar PASS**. 기존 H0–H5 재실행은 불필요.
2. ULKRR-02: 허가된 재개 경계에만 행 교체 허용. no-RESUME 중복 비정상 확인은 주 값/선택/제출 차단, 정상 재개는 유지.
3. ULKRR-03: 잡 완료·fails·reader_rc를 함께 소비. 파일 발행 후 판독 오류까지 다음 제출 차단.
4. ULKRR-04: 필수 열 오류 우선 반환·ID 정확한 정수성 검사, 두 실제 경로 음성 대조.
5. 지원되는 Linux 환경에서 수정 후 모의 러너·문법/포장 시험의 **전체 로그와 rc** 확보. 실제 원자료 없이 자기시험 숫자만으로 확대 인증하지 않을 것.

Q5의 자동 코드 관문 채택은 별도 저자 결정이다. 채택하지 않아도 실제 문법 PASS를 생략할 수 없다. §6의 비차단 보강 항목은 위 P1과 구분해 기록할 것. 물리 상수·1 MPa·0.10 %p·KE 계수·S1/S2/S4·부호·S0는 이번 반례 때문에 바꿀 이유가 없다.

## 10. 재현과 전달물

동봉 검토 폴더에서 실행. 표준 라이브러리만 사용하며 새 합성 자료와 검토 evidence만 쓴다. 실제 시뮬레이터 실행 명령은 포함하지 않았다.

```text
python -X utf8 -B probes/reader_recheck.py
python -X utf8 -B probes/runner_recheck.py
python -X utf8 -B probes/grammar_recheck.py --kit source/docs/data/ps45_unload_20261009 --out evidence/grammar_deck_recheck.json
python -X utf8 -B legacy_probes/history_actual.py
python -X utf8 -B legacy_probes/kit_byte_checks.py
python -X utf8 -B run_baselines.py
python -X utf8 -B run_legacy_probes.py
```

탐침의 프로세스 rc0은 결과 저장 성공일 수 있으므로 `reader_recheck.json.summary.failed_expectations` 등 **사례별 결과**도 읽어야 한다. 원자료 경로가 들어간 manifest는 당시 증거이며, 다른 컴퓨터에서 재현 시 탐침이 새 유효 경로로 fixture를 만든다.

- `source_manifest.json`, `upstream_manifest.json`, `evidence/source_delta.json`: 출처·바이트·물리 표 불변성.
- `evidence/*recheck.json`: 입력→함수→선택/관문 전체 결과와 사례 경로.
- `notes/`: 각 경로 상세 검산·소스 줄·한계.
- `legacy_probes/` 및 `evidence/legacy_*.log`: 이전 탐침 그대로의 실행 기록.
- `evidence/history_actual_audit.json`: 기존 실제 이력 다시 읽기 및 기존 덱 대조.
- ZIP의 `PACKAGE_MANIFEST.json`: 전달 파일별 SHA256. 합성 사례는 보고 증거이며 실제 언로딩 결과가 아니다.

**HOLD — 기존 수정의 좁은 닫힘은 인정하지만, 본 R · 연장 · U 실행 해제는 보류.**
