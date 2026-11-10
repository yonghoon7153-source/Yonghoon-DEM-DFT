# LHS 경계 보완 — 작성측 합성 검증

**24/24 통과·오류0·rc0, 유효 보호조건 약화6/6 검출·각 오류0.** 원장 종결·외부 판정·연구 실행 GO는 아니며 전체 HOLD다. 바탕은 `6add88f264d2c651b467f3906e755824ed6e40ad`. 대상 원source3파일은 이전 c571a/f464와 같은 바이트였다.

| 항목 | 상태 | 변경과 근거 | 한정 |
|---|---:|---|---|
| L214K-05 | 1 | `scripts/g2_network_reread.py`의 case_row/row_generation_problems 예외를 K5 실패 기록으로 반환한다. 현재 case/folder/run_id를 보존하고 다른 케이스를 계속 처리해 main이 현재 실패 JSON·rc1을 낸다. | 지정 두 소비자 호출의 일반 Exception만. KeyboardInterrupt는 전파한다. 모든 CLI 예외·디스크 실패·동시작성·crash durability를 해결한 것이 아니다. |
| L214K-08 | 1 | `scripts/lhs_release_build.py`의 좁은 blank checker가 OK/MBCB τ²·τ도 각각 유한 양수로 검사한다. 기존 f/비관통/NOT_COMPUTED/모형 한계 공란 의미를 보존한다. | CSV cell 문자열을 대상으로 한 방어 중복. fresh build의52열 원천 재독은 이미 있었고 check_v13를 새 원천 재독 도구로 바꾸지 않았다. |
| L214R-S05 | 1 | `webapp/templates/single.html` 첫 header paragraph에서 유효 숫자만 포맷한다. 유효 sphere-sum 우선/legacy fallback, 부가 uncertainty·bedtop union 독립 생략, bedtop tooltip 의존값 동시 검사, RVE 두 크기·scale 및 곱 검사. | 지원 입력은 JSON 기본형 int/float/bool/null/string. bool/숫자 문자열/비수치/NaN/무한대/초대형 정수는 숫자로 표시하지 않는다. 임의 Python Number/Decimal 객체의 안전성을 보증하지 않는다. |

상태1은 작성측 후보 검증이며 원장의 open을 직접 바꾸지 않는다. K07은 선택적 문구 제안이며 이 후보는 이유 사전·reason code를 수정하지 않았다.

## 표시 범위와 보존

`_display_max`는 binary64 최대 유한값이다. 물리·과학적 허용 문턱을 새로 정하지 않는다. 유한 입력이라도 RVE 크기×scale이 무한대가 되면 해당 배지를 생략하고, float 포맷이 overflow하는 초대형 int도 표시하지 않는다. 시험은 `1e308×1e6`, `10**400`, ±1e308, 0 및 일반 수를 구분한다. ±1e308 표시는 여전히 허용하므로 임의 과학적 cutoff가 아니다.

정상 라벨·단위·정밀도·E_SE의 기존 뒤 설명·추정 두께 경고·ionic threshold를 보존했다. 결손을0으로 바꾸지 않으며 numeric string을 새로 변환하지 않는다. 과거 tooltip 설명 자체를 이번 후보가 물리적으로 검토하거나 바로잡은 것은 아니다.

## 시험과 순서

| 순서 | 메서드 / 실패 / 오류 / rc | 의미 |
|---|---|---|
| 보존 staging | 22 / 미실행 | 구현 전에 준비한 시험 |
| 표시 overflow2개 추가 뒤 첫 old red | 24 /166/66/1 | E_SE 정상 suffix를 빠뜨린 시험 기대2개와 결손 badge 진단의 IndexError1개도 포함; 원 기록 보존 |
| 기대 suffix 정정 old red2 | 24 /164/66/1 | source 미수정; fixture scale은 명시1e6 |
| 명시 len assertion 정정 old red3 | 24 /165/65/1 | 이 기록 뒤 구현 시작. 정상 controls 통과. 남은65는 구 source의 실제 consumer/표시 예외 |
| 최소 구현 + 같은 고정 시험 | 24 /0/0/0 | 최종 green |
| 유효 guard 약화6종 | 각각24 / 양수 /0/1 | K5 실패표지·현재 run_id, τ독립 검사, bool, +inf, RVE곱 |
| 별도 잘못된 변이 시도1건 | 24 /0/48/1 | Jinja1e999 literal의 undefined inf 컴파일 오류. 의미 검출수에서 제외하고 원 기록 보존 |

old red3 오류 종류는 ValueError2·OverflowError5·RuntimeError7·TypeError47·Jinja UndefinedError4다. 이들을 오류0으로 바꿔 적지 않는다. 최초 기대/진단 정정과 구현 결함을 구분했고 `verification_summary.json`에 모든 시험/source SHA와 순서를 보존했다. +inf 변이는 literal 없는 v2로 다시 만들어15 assertion 실패·오류0을 확인했다. 최종 source/test는 이 변이 준비 중 변경되지 않았다.

메서드24, 내부 assertion/subtest 실패, 예외, 반복, 변이를 합산해 새 고유 시험 수로 만들지 않는다. 이번 작성측 검증은11회 suite invocation이며 외부 독립 검토가 아니다.

## 격리와 재현 범위

- 새 시험: `scripts/test_lhs_reread_receipt_boundary.py`6, `scripts/test_lhs_tau_blank_boundary.py`6, `scripts/test_single_header_numeric_boundary.py`12메서드.
- K05/K08은 정확 AST 함수·필요 상수만 실행한다. tf/ps/LDD와 관련 소형 helper는 합성 fake이며 실제 sealed module을 import하지 않는다. IO는 임시 합성 receipt뿐이다.
- S05는 실제 Jinja2 3.1.6 및 MarkupSafe3.0.3으로 원 header 조각을 렌더한다. 앱·Flask·실제 metrics loader·ledger/base template·browser는 불러오지 않는다. 이전 wheel 준비 단계의 실행0 기록과 이번 라이브러리 사용을 구분한다.
- 고정 runner는 `-I -B`, audit를 project exec 전에 설치하고 process/network·허용 밖 파일 접근을 차단했다. 기록된11회에서 차단 시도0, source 불변. 실제 자료·원로그·실행 당시 신원·연구 계산·전체 gate·운영 재봉인은0.
- raw 묶음의 `run_boundary.py`, 각 source snapshot/report/test.log, `CHRONOLOGY.json`, `contrast_manifest.json`, `runtime_preparation_provenance.json`, `raw_manifest.json`을 따른다. 원시 증거는 리포 밖 전달 묶음에 두고 실제 외부 경로·주소를 이 문서에 적지 않는다.
- sealed core, Rint, 원장 변경 없음. 별도 D5 문서 링크 정정1건은 위 source3+tests3의 수정 범위와 구분한다.

전체 HOLD. 좁은 회귀 통과는 실제 WSL 실행 신원·압력 자격·값 열람 승인·배포 승인이 아니다.
