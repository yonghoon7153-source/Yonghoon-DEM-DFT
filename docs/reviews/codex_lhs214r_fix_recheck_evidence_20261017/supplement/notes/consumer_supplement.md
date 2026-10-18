# a4a1e52c0 보충 증거 — 소비자·시험 집계 교차검토

## 결론

**기존 HOLD 변경 근거 없음.** 보충 자료는 원 L214R-02 등의 수정과 당시 시험 수를 뒷받침한다. 새 L214RR-01/P2 H0 라벨·게시값 복원, L214RR-02/P3 양쪽 과거 유도값의 Δ, L214RR-03/P3 긴 코드 울타리 반례를 반박하거나 수정한 자료는 아니다. P3 둘을 수치 배포의 별도 P2로 격상하지도 않는다.

이 검토는 제출 로그·JSON·드라이버의 **읽기 전용 대조**다. before/final 시험, 생산자, 새 배포 또는 Git 명령을 실행하지 않았다. 기존 독립 증거를 덮지 않았다. A4 원문 실행은 주 검토자가 별도 담당하므로 여기서 36/36을 독립 재현했다고 주장하지 않는다.

경로 약칭:

- `S` = `C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs214r_supplement_a4a1e52c0_20261017/submitted/lhs214r_recheck_a4a1e52c0/docs/reviews/lhs214r_fix_evidence_20261016`
- `O` = `C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs214r_fix_recheck_20261017`

주 검토자의 intake 검증에 따라 제출 핀은 `a4a1e52c0bc01731f4c1d00924099b56c05a055f`; `scripts/`·`webapp/`는 기존 독립검토 코드 `60ba39e224aff48a030dccfe750342f3bf9db61f`와 동일하다. 핀 확인과 소비자 동작 수정은 구별한다. 증거 폴더 실제 파일 71개는 `SHA256SUMS` 자신을 포함한 수이고, 내부 목록 70개와 모순이 아니다.

## 1. before/final 수와 종료코드

`S/README.md:25`–`:35`, `S/rc.tsv:2`–`:18`을 각 실제 로그의 줄 첫머리 `PASS`·`FAIL` 수와 다시 대조했다. 결과 행의 숫자만 복사한 것이 아니라 assertion 결과 줄을 집계했다.

| 시험 | before PASS | before FAIL | 합계 | final PASS / FAIL | before / final rc |
|---|---:|---:|---:|---:|---|
| L214R-01 | 48 | 64 | 112 | 112 / 0 | 1 / 0 |
| L214R-02 | 17 | 30 | 47 | 47 / 0 | 1 / 0 |
| L214R-03 | 5 | 9 | 14 | 14 / 0 | 1 / 0 |
| L214R-04 | 100 | 11 | 111 | 111 / 0 | 1 / 0 |
| L214R-05 | 109 | 75 | 184 | 184 / 0 | 1 / 0 |
| WEB-09 | 7 | 9 | 16 | 16 / 0 | 1 / 0 |
| L214R-06–08 | 118 | 188 | 306 | 306 / 0 | 1 / 0 |
| L214R-09–11 | 43 | 53 | 96 | 96 / 0 | 1 / 0 |
| 위 여덟 합계 | 447 | 439 | 886 | 886 / 0 | — |
| provenance 별도 | — | — | 284 | 284 / 0 | — / 0 |

제출 수와 일치한다. 이 숫자는 서로 독립적인 생산 실행 횟수가 아니라 해당 시험의 assertion 집계다. before 여덟은 모두 한 `6cb256956` 트리의 시험이 아니라 각 test-first 커밋에 대한 제출 로그다(`README.md:12`, `:25`–`:34`). 이 검토에서 그 커밋들을 다시 체크아웃하거나 실행하지 않았다. 최종 수와 달라 보이던 before 수를 최종 코드로 재실행해 해석해서는 안 된다.

`rc.tsv`는 헤더 제외 37행(8 before + 10 final + 1 A4 + 9 pre probe + 9 final probe)이고 참조 로그는 37/37 존재한다. final의 10에는 8개 시험 외 provenance와 지문 보고가 포함된다. 지문 보고·A4·probe 완주 rc를 위 886 assertion 수에 합산하지 않았다.

## 2. 재실행 드라이버의 정확한 의미

`S/probe_rerun/{pre_6cb256956,final_60ba39e22}/driver_summary.json`과 `rc.tsv:21`–`:38`의 아홉 run label·rc가 일치한다. pre는 9/9 rc0. final은 8개 rc0, 원 `receipt_identity`만 rc1이다. 해당 로그 마지막 traceback은 원 탐침 40행의 `minimal_activate_section3.bad == ['R0','D1']` assert이며, 파생 noassert 결과는 그 변이에 `rc=0`, `bad=[]`를 기록한다. 수정된 구형 반례에 대한 예상 assert 실패라는 README 설명과 맞는다.

두 가지 집계 주의:

1. `drive_l214r_probe.py:189`의 전체 return은 하위 rc2가 있을 때만 2, 그 밖에는 0이다. 따라서 전체 실행기 rc0을 모든 하위 검증 PASS의 뜻으로 쓰면 안 된다. 이번 제출은 개별 rc1을 숨기지 않았고 JSON·로그도 맞는다.
2. 원 탐침 **다섯 파일을 복사·SHA 대조**한 것과 다섯 원 탐침을 전부 실행한 것은 다르다. 드라이버 `:12`, `:30`–`:40`상 원 `l214_a4.py`는 복사만 하고 실행하지 않는다. 실행은 나머지 네 원 탐침의 여러 옵션과 receipt 파생을 합한 아홉 회이며 A4는 별도 도구다. README의 “탐침 다섯 무변경 재실행”은 이 한정을 붙여 읽어야 한다. 파생 noassert의 rc0도 제거된 assertion의 PASS를 뜻하지 않으므로 실제 변이 결과를 읽었다.

두 summary의 source/base manifest 경로 누락은 0이며, 소비자 원 탐침 SHA는 `804de03d58902862f74006afaf1e24dfed97a42a254d02b86a4cc98797de243a`로 기존 독립 패키지의 원 탐침과 같다. source 파일 수 1869→1876, base 650은 두 snapshot의 범위 설명이지 실패 수가 아니다.

## 3. 소비자 증거의 직접 교차대조

제출 final JSON을 `O/evidence/`의 동명 파일과 파싱하여 비교했다.

- `consumers_release_probe.json`: **구조적 내용 완전 동일**. ml_hertz, independent_l1_h0, independent_l2_h0 모두 실제 build 거부/HOLD. 제출 pre의 L1/L2는 실제 27파일 build, 경고 없음, check=[]였고 final은 ReleaseError다. 이는 원 L214R-02 닫힘을 추가 지지한다.
- `consumers_negative_paths.json`: **구조적 내용 완전 동일**. 일곱 변이(CF 잔차, bulk_model 결손, withheld q×1.01, thermal 실패, electronic 실패, FULL 사유 꼬리, Physics의 H12 역할)가 모두 stop=False, handover=False. 제출 pre/final의 74칸도 같다는 비교 JSON과 일치한다. **74칸은 일곱 변이의 출력 필드 수이며 74개 별도 음성 시험이 아니다.**
- `consumers_probe.json`: 다섯 case의 done·주 타깃 관문·K1–K7 판정이 기존 독립 결과와 같다. 각 case K1–K7은 7/7 True. Linux 제출과 Windows 독립 실행의 원 q에는 작은 부동소수점 차이가 있다. 예: H0 L0 `1.6231747351909949` 대 `1.6231747351909995`, L1 `8.927503013108016` 대 `8.927503013108073`, L2 `35.710012052432674`는 동일. 모두 정책 1.5보다 충분히 크며 어느 판정도 달라지지 않는다.

`S/probe_rerun/cmp_pre_vs_final.json`의 인계표 975 공통칸 동일 + 표지 10칸 추가는 다섯 행 × 두 표지이며, 독립 표지 도입과 일치한다. 비교기 `judgment_diff`에 run id·해시가 섞이므로 그 목록 길이를 결함이나 의미 변화 개수로 취급하지 않았다.

## 4. 새 P2/P3를 종결하지 못하는 이유

### L214RR-01 / P2

제출 소비자 양성 다섯·음성 일곱·build 세 사례에는 **withheld H0를 computed로 복원한 변이**가 없다. 새 반례는 숫자를 임의의 정답으로 위조한 경우가 아니라, 실제 생산자의 q·전류·기하·시도 목록·guard 진단을 그대로 두고 게시값과 상태를 복원하여 같은 1.5 정책과 모순되는 레코드를 소비자가 받는 경우다.

기존 독립 `O/evidence/consumer_h0_resurrection.json`, `O/notes/consumers.md`의 정확한 범위를 유지한다: H0 10 leaf를 3사본에 반영(30), full_metrics 6 leaf, 실제 batch writer로 CSV 투영(직렬화 값 변화 2셀). 실제 content/record/stop, K1–K7, P0–P4, 인계, 27파일 build/check=[]가 확인됐다. 반면 새 게시 프로세스 `_network_and_stage_e`를 변이 뒤 다시 실행한 결과도 아니고 실제 214 생산 감사 결과도 아니다. 선택행은 실제 원천 재독, 나머지 213행·배치 감사는 선언된 합성 어댑터다. post-build 사본/해시를 고치는 시험과 구분한다.

이번 핀의 생산 코드가 같고 그 반례를 다룬 새 입력·새 결과·변경된 계약이 없으므로 기존 P2 결론을 바꿀 이유가 없다. 기존 L214R-02 닫힘과 이 새 P2는 모순되지 않는다. 알려진 K5/K8은 기존 노트의 한정과 판정을 그대로 유지하며 제출 증거가 새 build 우회를 더 보인 것도 아니다.

### L214RR-02 / P3 및 L214RR-03 / P3

제출 display 68 case는 기존 원 탐침의 normal/valid_zero/단일 모드 결손·상태/생산자 사례다. 양쪽 현재 유도값이 함께 없는 추가 `missing_both_derived` 사례는 없다. `README.md:47`의 “Δ 두 칸 모두 숫자일 때만”은 현재 값 freshness까지 입증하지 않는다. 기존 추가 21case의 발견과 충돌하지 않는다.

제출 receipt 일곱 변이는 no_pending/minimal_activate/all_old_tokens/arbitrary_pending/two_distinct_pending/malformed_pending/redundant_identical_pending이다. `receipt_identity_noassert.py`는 같은 입력에서 assertion을 제거했을 뿐 긴 울타리 안 예시 §3을 추가하지 않았다. 따라서 원 minimal activation 수정은 입증하지만 별도 긴 울타리 P3에는 새 증거가 없다.

## 판단 갱신 범위

증거 핀 누락은 주 검토자의 새 intake 검증으로 해소된 것으로 읽되, 이를 생산 코드의 새 수정으로 해석하지 않는다. 소비자 lane에서는 원 반례 닫힘의 증거가 강화되었고 before/final 수의 모순은 발견되지 않았다. **새 P2는 계속 차단, P3 둘은 기존 범위 그대로 미해결**이다. 이번 기록은 로그를 읽어 대조한 결과이며 독립 before 재실행이나 새 정상 생산 무영향 증명으로 표시하지 않는다.
