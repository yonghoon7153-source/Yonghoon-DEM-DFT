# D2 소비자 재현 자료

> 현재 canonical 전체 gate: **PASS, 155/0, rc 0**. [완료 기록](completion.md)을 따른다. 아래 작성자/초기 반입 시점의 예정·대기 문구는 원 스냅샷의 범위이며 현재 상태를 대신하지 않는다.


기준 핀: `486a57cf58d3e0d93ef79be6aae50968929099c0`. 생산 3파일의 최종 내용은 `author/snapshots/frozen-v3/`이며 v2와 같다. 신규 시험만 v2→v3에서 천장 검출을 보강했다. root의 최종 반입·전체 관문·커밋은 별도다. `full_gate_receipt.json`의 현재 상태를 따른다.

## 새 출력 폴더에서 재현

저장소의 해당 핀을 별도 scratch 폴더로 내보내고 패키지 루트 `consumers-v3.patch`를 적용한다. `scripts`의 다른 의존 모듈과 기존 자기시험의 `docs/data/mixer_highbo_dev_decks_*`, `dem_scripts/mixer_20260919`, `dem_scripts/mixer_20260921` 고정물도 그 핀에서 가져온다. 6개 frozen 파일만으로 모든 기존 자기시험을 실행할 수 있다고 가정하지 않는다.

Python 환경 활성화 뒤, 패치를 적용한 scratch 저장소에서:

```bash
python -I scripts/test_mixer_d2_consumers.py
python -I scripts/mixer_deck_readback.py --selftest
python -I scripts/mixer_deck_diff.py --selftest
python -I scripts/mixer_smoke_blind.py --selftest
```

정확한 옵션은 `--selftest`다. `--self-test`는 지원하지 않는다. 최초 전달 메시지의 표기는 오기였으며 실제 CLI와 이 절차를 따른다.

```bash
python -I <증거>/tools/baseline_reproduce.py \
  --scripts <패치된-scratch>/scripts --baseline <증거>/author/snapshots/baseline \
  --out <새-출력>/baseline.json
python -I <증거>/tools/mutation_check.py \
  --scripts <패치된-scratch>/scripts --out <새-출력>/mutations
python -I <증거>/tools/render_v18.py \
  --repo <패치된-scratch> --document <패키지>/docs/mixer_devlog/v18_20261024.md \
  --out <새-출력>/render
```

mutation 도구는 소비자 guard를 하나씩 제거한 별도 사본에서 신규 회귀를 실행한다. clean rc0, 19개 변이 모두 실제 assertion 실패이며 test ERROR는 0이다. `author/mutation-effect-details.json`이 각 검출 메서드를 연결한다. 실행기의 rc만으로 효과를 주장하지 않는다. 원 로그는 수정하지 않고 새 경로로 재현한다.

## 증거 분류

- `author/logs/baseline-reproduction.json`: 원래 3제한과 같은 입력의 새 개발 경로 결과. 실제 실행 결과가 아니다.
- `author/logs/test-first.log`: 신규 API/CLI 미구현 초기 red. 당시 8메서드의 API 부재와 물리 반례를 구분한다.
- `author/tests_first/`: 숫자/시간간격, 명령 범위, 명령 생명주기 검사를 추가한 수정 전 소스 사본. 해당 red/green은 `author/logs/`.
- `author/snapshots/frozen-v1`, `frozen-v2`, `frozen-v3`: 독립 리뷰용 고정 소스와 각 full patch·SHA. 과거 소스·보고서를 최신 결과로 덮어쓰지 않는다.
- `author/mutation-v1`: 모듈 누락으로 clean부터 실패한 환경 구성 기록. 효력 증거가 아니다. v2에서는 실제 밀도·중력 검사가 생존했고 v3에서는 정수 인쇄 반올림이 밀도 guard 효과를 가렸다. 최종은 `author/mutation-final`만 따른다.
- `author/logs/ceiling-coverage-green.log`: 최종 신규 13메서드. 정상128덱·48계획 조합·32쌍은 각각 다른 조합 설계이며 고유 덱 수로 합산하지 않는다.
- `author/logs/{readback,diff,smoke}-v2-final.log`: 생산 내용이 최종과 같은 v2의 구 계약 회귀. 이후 생산 내용 변경은 없다.
- `author/logs/render-v18-final.log`, `author/render-summary.json`: 실제 `/mixer` route를 scratch 문서/쓰기 폴더로 검증.
- 내부 독립 보고와 증거는 별도 repo-relative 경로로 원본을 함께 반입한다. 이 README에서 외부 검토·실행 GO를 새로 만들지 않는다.

첫 archive 시 존재하지 않는 문서 경로를 시도한 로그, 기존 자기시험에서 필요한 고정물을 덜 내보내 생긴 실패, 초기 CLI 로컬 이름 충돌, 최초 벡터 반례 문자열 오기 등 중간 기록도 보존했다. 최종 성공만 남겨 이전 실패를 숨기지 않는다. 이러한 준비 실패를 생산 물리 결함이나 실제 런 실패라고 읽으면 안 된다.

## 판정 경계

구체적인 S1 수치·코호트·정책 구현·등록, STL/실물 장비·관측 입자·접촉·실험 입력은 이 묶음에서 만들어지지 않았다. 제시된 설계·정책 방향은 사용자 비준 완료이며, 누락된 구체 산출물을 비준 대기로 바꿔 부르지 않는다. 개발 출력은 registered=null, execution_authorized=false다.
