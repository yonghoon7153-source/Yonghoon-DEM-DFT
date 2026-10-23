# MXD2 소비자 독립 리뷰 증거

이 묶음은 2026-10-24 KST에 합성 덱과 메모리 내 검증 조건 변이를 실행한 기록이다. 실제 DEM·WSL·발사 결과가 아니다. [리뷰](../codex_review_mxd2_consumers_independent_20261024.md)의 최종 해시와 일치하는 소스에서 재현한다.

저장소 루트와 새 출력 위치를 명시한다. `EVIDENCE_OUT` 아래의 각 마지막 디렉터리는 없어야 한다. 환경에는 이 리포의 기존 Python 의존성이 필요하다. 실행은 `python -I`로 하며 세 도구는 `--repo`에 지정한 `scripts/`만 명시적으로 import한다. main checkout이나 git refs를 수정하지 않는다.

```bash
export REPO_ROOT="$PWD"
export EVIDENCE_OUT="${TMPDIR:-/tmp}/mxd2-independent-reproduction"
export REVIEW_TOOLS="$REPO_ROOT/docs/reviews/codex_mxd2_consumers_independent_evidence_20261024/tools"
python -I "$REVIEW_TOOLS/attack_consumers.py" --repo "$REPO_ROOT" --out "$EVIDENCE_OUT/matrix"
python -I "$REVIEW_TOOLS/command_order_attacks.py" --repo "$REPO_ROOT" --out "$EVIDENCE_OUT/lifecycle"
python -I "$REVIEW_TOOLS/mutation_effectiveness.py" --repo "$REPO_ROOT" --out "$EVIDENCE_OUT/mutations"
python -I "$REPO_ROOT/scripts/test_mixer_d2_consumers.py"
python -I "$REPO_ROOT/scripts/mixer_deck_readback.py" --selftest
python -I "$REPO_ROOT/scripts/mixer_deck_diff.py" --selftest
python -I "$REPO_ROOT/scripts/mixer_smoke_blind.py" --selftest
```

최종 소스의 기대 rc는 모두 0이다. 최초 v1 소비자에서는 `command_order_attacks.py`가 4개 결함을 보고 rc 1을 내는 것이 red 증거다. 최종 변이 도구는 `_d2_lifecycle`이 추가된 v2 이후를 대상으로 한다.

`attack_consumers.py`는 90사례·249호출을 기록한다. 이 중 `second_insert_seed`, `common_geometry_unregistered` 두 사례는 관찰 전용이다. 88개의 판정 사례와 관찰 2개를 모두 정답을 부여한 90개 시험으로 읽지 않는다.

`command_order_attacks.py`는 정상 1개와 음성 5개를 세 소비자에 보낸다. 생성 fixture를 출력 디렉터리에 남기므로 리포에 커다란 fixture 사본을 반입할 필요가 없다.

`mutation_effectiveness.py`는 독립 fixture를 자체 생성하고, frozen 소스의 검증 함수를 메모리에서만 바꾼다. 아홉 반례의 정상 FAIL→변이 PASS와 canonical unittest 실패를 함께 검사한다. 각 변이 실행 후 원래 함수를 복구한다. CLI subprocess 시험은 변경하지 않은 디스크 소스를 보므로 변이 검출 수의 근거는 in-process 회귀다. 수량 변이의 101 failures는 반복 하위 시험 실패 수이며 서로 다른 101개 변이가 아니다.

## 보존 파일

- `source_manifest.json`: 기준 핀, 실제 검토 소스 및 설계 blob 해시. `results/frozen-v*-sha256.json`은 단계별 frozen manifest 원본이다.
- `results/matrix-v1.json`, `matrix-v2.json`: 독립 덱 행렬. 최종 v3의 소비자 코드는 v2와 같은 해시다.
- `results/lifecycle-v1-red.json`, `lifecycle-v2-green.json`: 네 구조 반례의 전후 결과. 숫자는 fixture 실행이 아니라 덱 문자열 검사다.
- `results/mutations-v1-gravity-gap.json`, `mutations-v2-ceiling-gap.json`: 실제 효과가 있는 변이가 당시 시험에서 살아남은 기록.
- `results/mutations-v3.json`: 원래 독립 fixture 사본을 읽은 최종 변이 실행. `results/mutations-v3-portable.json`과 `logs/mutations-portable/`은 fixture 고정 경로 의존을 제거한 현 도구의 별도 재실행이다. 기존 로그를 새 도구 실행으로 소급하지 않았다.
- `logs/`: 최종 frozen v3의 13개 방법 및 세 자체시험 원본 로그와 실제 argv·rc·시각.
- `historical/`: 초기 누락 fixture로 실패한 기존 자체시험과 정확한 기준 fixture 보충 후 재실행. 이 실패를 생산 코드 결함으로 분류하지 않았다. `historical/mutations-initial/`은 최초 audit harness의 효과 없는 해시 메시지 오기를 보존한다.
- `MANIFEST.sha256`: 이 증거 폴더에서 manifest 자신을 제외한 파일의 SHA256. 원본 로그 안의 실행 당시 절대 경로는 역사 기록이며 재현 명령의 고정 경로가 아니다.

실제 simulator, 등록, launch 또는 외부 GO를 생성하는 도구는 포함하지 않는다.
