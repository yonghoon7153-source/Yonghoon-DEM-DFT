# MXD2R-R01 삽입 seed 범위·소수 검사 — 한정 재확인 후보

2026-11-06 · 기준 main `766e1e80cf0a26ec3368a732922a4f35b9ba74de` · 믹서 가지 이력 보존 기준 `ad7d2d555ce4c3fd50e8c3400cac70eb713c27f2`.

**R01/P2 수정 후보, 외부 재확인 대기. 전체 HOLD·실제 실행 미승인.** 이번 범위는 생성된 소형 정적 덱·메타와 소비자/CLI 회귀뿐이다. LIGGGHTS/DEM/MPI·호스트·제출·실제 관측값 열람은 없다. MXD2R-01–03 한정 CLOSED를 다시 열거나 R01을 이 창에서 종결하지 않는다. MLA-01–03과 MXD2-01 전체/물리·통계·현장 자격은 별도다.

## 1. 입력 판정과 기준 결속

1저자가 전달한 반박창 §2 최소 조건에 따라 작업했다. 별도8질문판 쪽지에도 대상 f5b00a838의 MXD2R-01/02/03 한정 CLOSED,04 PARTIAL, 잔여 R01/P2가 기록돼 있다. 이 작업에 원 반박 증거 ZIP/§2 전문이 반입된 것은 아니므로 독립 판정 원문 전체를 검증했다고 쓰지 않는다. `user_relay.md`는 이번 사용자 전달의 범위 기록이다.

readback·pair diff·smoke·기존 D2 회귀4파일 및 생성기까지5파일이 main766e1e80c, 리뷰 기준f5b00a838, 이력 보존 기준ad7d2d555에서 각각 같은 SHA256임을 확인했다(`evidence/baseline.json`). 기존 codex 공개 핀은 재작성하지 않고 main을 이력 보존 merge로 맞췄다. 이 동기화 merge는 Claude 반입용 작업 cherry-pick 대상이 아니다.

## 2. 변경

`scripts/mixer_deck_readback.py`의 `_d2_counts`가 **각 실제 insert/pack 명령**의 seed를 `_d2_insert_seed`로 확인한다. fix ID·실제 토큰을 사유에 넣고, ASCII 양의 정수→1..2147483647 범위→소수 순으로 검사한다. 범위 밖 큰 수에 소수 검색부터 하지 않는다. 첫 metadata seed·파생 규칙과 같아 보인다는 이유로 둘째 실제 seed를 생략하지 않는다. 메타/덱 hash·bytes 재결속은 이 계약의 대체가 아니다.

pair diff와 smoke plan은 같은 readback 경계를 호출하므로 세 소비자가 같은 구체 사유로 FAIL/CLI rc1을 낸다. 기존 첫 metadata seed 결속과 둘째 next-prime 생성기 꼴 대조는 그대로다. 유효 범위의 다른 소수로 둘째 seed를 바꿔도 생성기 꼴 불일치로 거부한다. wrap·truncate·다른 seed 선택은 없다.

**생성기는 이번에 바꾸지 않았다.** optional 조기 거부는 범위를 넓히지 않고 보류했다. 따라서 생성기만 호출하면 최대 seed 층상 부적격 덱을 여전히 출력할 수 있다. 소비자 거부를 우회해 그 덱을 실행할 자격은 없고, 이 수정은 생성기 자체의 seed 전역 안전성이나 실제 런 성공을 인증하지 않는다. 생성기 코드와 정상 덱 바이트는 보존했다.

`positive_extra.py`의 옛 최대 seed 층상 “양성” 기대는 음성으로 정정하고 최대 균일·near-max 층상 양성을 추가했다. 잘못된 기대 또는 예상 밖 생성기 거부가 있으면 이제 도구 자체가 rc1이다. 이전 로그/판정과 고정 핀의 원 도구는 역사 증거 그대로다. 옛18양성에는 이번 음성이 섞여 있었으므로 현재 유효 양성 수로 인용하지 않는다.

## 3. 시험 먼저와 결과

| 범위 | 관측 | 근거 |
|---|---|---|
| 수정 전 새5메서드 | rc1, 실패 단언48개. 그 중 원 반례 API6/CLI6(각3소비자×2상구성)은 PASS/rc0을 잘못 받아 실패. 나머지는 독립 seed 사유 검사 실패 | red.log와 red_sources |
| 수정 후 D2 전체 suite | Python3.12.14에서34메서드 통과(기존29+새5). subtest/버전 반복을 더하지 않음 | green_all_consumers.log |
| Python3.8 호환 | 실제3.8.20에서 새5메서드 통과 | py38_focused.log |
| 같은 원 반례 정적 파일 재대조 | 층상2147483647→insB2147483659. 세API PASS→FAIL, 세CLI rc0→rc1. 구체 사유 insB/값/상한 명시 | red_cli/green_cli/summary.json |
| 경계 양성 | 최대2147483647 균일·2147483629 층상(둘째2147483647)은 세API/CLI PASS·rc0 유지. 이 두 쌍의 덱 바이트 수정 전후 동일 | 같은 summary, evidence_summary.json |
| 변이2개 | 범위 가드 제거→원 반례가 다시 수용됨; 소수 가드 제거→독립 실제 seed 사유 검사가 실패함. 후자는 뒤 생성기 꼴 검사도 거부할 수 있어 “모든 합성수를 수용했다”는 뜻 아님 | range_guard_removed/prime_guard_removed.log |
| 보정한 extra 도구 |21조건 중19생성 양성,1층상 overflow 음성,1rpm60 예상 생성기 거부. bad0/도구rc0. 네 API호출(세소비자+bytes재호출)은 독립4제품이 아님 | positive_extra.log |
| 기존 legacy selftests | readback24/24·pair55/55 통과, smoke 자체 종료rc0. 닫힌01–03 판정을 새로 재심한 것이 아닌 호환 검사 | *_selftest.log |

새5메서드는 기존 `scripts/test_mixer_d2_consumers.py` 안에 들어 있어 공용 `scripts/check_all.sh`의 D2 단계 및 이를 실행하는 CI에 연결돼 있다. 현재 목록에서 그 단계는61이다. **이번에는 해당 suite를 직접 실행했으며 check_all 전체/분할 게이트를 실행한 것은 아니다.** LIST 모드는 목록 확인만이다. 전체 게이트 통과라고 합산하거나 보고하지 않는다. 실제코드/바이트 무결성·문서 참조 검사는 별도 validation 기록으로 전달한다.

## 4. 전달과 남은 경계

review_request.md와 PIN.txt가 가리키는 push된 새 후보를 별도 Codex 반박 창에1저자가 보낸다. 수정 전 실패/원 덱·메타, 수정 후 결과/소스, 좁은 변이와 정상 보존을 함께 동봉한다. 이 창의 시험은 독립 종결 판정이 아니다.

LHS 정본은12질문6fbd066832d3이며8질문288929658dca의 LHS 정의는 대체됐다. 정확한 제외 파일·새 선택 기록은 인계 PIN_MAP.json과 LHS 쪽지에 따로 제공한다. LHS 정의 검토 핀은 변경하지 않는다.

믹서 실행 권고 NP20·E0→N0→B1/B2/B3 U/C·자격 뒤최대2팔·GO HOLD 그대로. MLA 후보a4c78001f 외부 재확인·예약 해제/정책 전환 절차·MXD2R 범위 판단·실제 binary/MPI/100k/시간/디스크 자격은 별도다. ibb 비었다는 전달이 실행 승인은 아니다. 공유 기록은 ledger_proposal.json 제안만. Claude 반입은 Rint② 회차③ 요청서 발송 뒤1저자가 정한 시점에 cherry-pick -x.

first8의 기존 `source_seal.json`은 이전 소스 핀과 readback 해시를 가리키며 이번에 다시 묶지 않았다. 따라서 이 새 readback을 기존 봉인/승인 문서와 섞어도 되는 것은 아니다. R01·MLA 재확인 뒤 별도로 출처 봉인을 갱신·검토해야 실행 준비가 이어진다. 기존40 planned assets·옛18런·D3 SOP·소스 봉인 파일의 바이트를 이번 수정으로 바꾸지 않았다.
