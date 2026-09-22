# R17 후속 3차 회신 — NO-GO, P1 1 · P2 2

대상 `e834b01e4066c5e78c06b6ed1f77878e5a27a481`, BMS 수정 `7f09804fdc6be2892746dece201b98da48aac6cd`. fix→HEAD의 BMS Python/shell 차이 없음(문서 하나만 다름).

원래 F2-01~06의 구체적 반례에 대한 수정 효과는 인정한다. 원래 재현기 47 case와 실제 producer 재현기를 바이트 수정 없이 실행했다. 실제 합성 producer 결과는 reader rc 0, row cycle만 제거한 대조군은 rc 2다. F2-04가 전 판처럼 그대로 남았다는 판정이 아니다. Linux 게시 CLI 전체는 리뷰어 Windows에서 확인하지 못했다.

새 종결 조건은 아래 셋이다. 전체 근거·실행 명령·stdout/stderr·fixture는 동봉 리뷰 패키지에 있다.

## F3-01 / P1 / 보존

`scripts/gc_partial.py:68,98,111,134,188,197`.

A→B 정상 index, 같은 artifact, `--keep 1`에서:

1. A의 경로에 다른 바이트를 넣고 index의 SHA를 그대로 두면 **rc 0으로 새 바이트 삭제**. 로그는 원래 SHA를 인쇄한다.
2. B 파일만 없애고 index를 그대로 두면 **rc 0으로 유일하게 남은 A 삭제**. 남은 index는 없는 B를 가리키고 payload는 0개다.

동시성 가정 없이, 검사 시작 전 정적 상태로 재현했다. index에 없는 다른 이름의 파일은 rc 2로 막히지만, 같은 경로의 다른 바이트/누락된 보존 파일은 보지 않는다. `rmtree` 제거는 수용하나 경로 집합이 곧 파일 동일성은 아니다.

최소 조건: 첫 삭제 전에 삭제·보존 전체 항목의 일반 파일 존재와 기록 SHA 대조. 불일치 하나라도 있으면 index 포함 변경 0·rc 2. 정상 GC와 기존 cross-artifact 보존 대조군은 유지.

## F3-02 / P2 / 정상 비교

`scripts/width_report.py:49,197,350`.

실제 합성 `fit_cycles`에서 starts 1/2만 다른 결과 두 벌을 만들었다. 각각 reader rc 0이나 `--axis starts`는 n_multistart 차이로, `--axis n_multistart`는 starts 차이로 **둘 다 rc 2**다. 같은 의미의 두 별칭을 단일 파일 안에서는 같게 강제하고, 비교에서는 독립 축으로 센다.

최소 조건: 별칭의 내부 일치는 유지하고 비교 시 한 의미 축으로 정규화. 실제 producer starts 1/2 비교 rc 0, 별칭 불일치·row n_starts 불일치·추가 seed 변경은 각각 rc 2.

## F3-03 / P2 / 오류 판정 계약

`scripts/verify_run_receipt.py:144,160,181`.

유효 receipt를 기준으로 `code=null` 또는 `instrument=["not-a-map"]`를 넣고 checksum을 다시 계산하면 typed 검사는 문제를 찾지만, 이어서 `.get`/`.items()`를 호출해 **AttributeError·rc 1, RUN_RECEIPT_VERIFY 출력 없음**이다. verified=true 수용 반례는 아니며 구조화 실패 경로 문제다.

최소 조건: 잘못된 구조의 후속 소비를 막고 수행하지 못한 검사를 성공으로 채우지 말 것. traceback 없는 구조화 실패/명시 rc, 유효 receipt·합법 materialized=None의 rc 0 유지.

## 실행과 제출

```text
python repro_followup2.py --target <bms-balancing>
python repro_producer_reader.py --target <bms-balancing>
python repro_followup3.py --target <bms-balancing> --part fast
python repro_followup3.py --target <bms-balancing> --part producer
```

재현기 rc 0은 진단 완료이지 제품 GO가 아니다. Windows 전수는 **357 passed · 110 failed · 26 errors**(493 수집). 기존 실패 108건은 그대로이며 새 비통과 28건은 모두 fcntl 부재다. 새 회귀 파일의 나머지 13건은 통과했다. 세부 분류는 TEST_STATUS.md/TEST_RESULTS.json을 그대로 인용하라. 현행 out schema-only는 rc 0이지만 promotion_eligible=false이고, legacy는 rc 2·52/25/10/1이다.

추가 관측(common receipt의 기존 cycle 덮어쓰기, git tree도 instrument로 수용, 비정상 solver 반환 주입)은 상세 보고서에서 **별도 권고**로 구분했다. solver 주입을 실제 SciPy에서 관측한 과학 오류로 확대하지 말 것. 독립 결함 건수는 위 세 건이다.

코드/회귀 수정 회신에 새 full SHA와 실행 증거를 포함하라. 실데이터 재적합·A/B 실행·과학 결과 갱신은 이번 검토/회신 범위가 아니다. **최종 NO-GO.**
