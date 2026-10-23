# ULPR 독립 사전 공격 리뷰 — 2026-10-23

판정: **수정 후 재확인 필요**. 새 회귀 P2 한 건을 실제 `arm` CLI와 생성 덱 제어 흐름으로 재현했다. 기존 selftest 전체 통과만으로 이 회귀가 검출되지는 않는다.

이번에 검토한 것: 제공된 `ulpr-merged-review.diff`의 두 Python 파일, 해당 새 시험, 등록 §14-4/10/11 및 기존 생산 진입점. 닫지 않는 것: 외부 LIGGGHTS/GPU 실행, 물리 결과, 전체 저장소 게이트, 다른 트랙, 문서 패키지 최종 숫자·봉인. 구현자의 보고·노트·scratch 설명은 읽지 않았다. 검토자는 tracked 파일 수정·commit·push를 하지 않았다.

검토 기준: checkout `codex/unloading-ulpr`, HEAD `7799a2ff64ba462b42ce05edd3e63b7c2854d557` 위 제공 diff. 정확한 검토 사본은 `reviewed.diff`, `ul_reader.reviewed.py`, `ul_gates.reviewed.py`에 보존했다.

| 검토 파일 | SHA256 |
|---|---|
| `ul_reader.py` | `5d517f0ec773bb9d67479c7232aab39f43e5e326598fbc5095c8e202822ad57d` |
| `ul_gates.py` | `55945c64e9d6b3c28a6662ff12dde9d1db73c5f219c38ef96d139f8a6b6c99f8` |

## F1 — P2 / 신규 회귀: 되감길 CSV 꼬리가 없는 정상 재개를 거부

위치: `docs/data/ps45_unload_20261009/ul_reader.py:259` (`_resume_reconcile`; 250–265행 문맥).

재현 순서:

1. 실제 생성 UT 덱의 제어 흐름으로 k=0..4를 만들고 k=3 끝 checkpoint를 선택한다.
2. 첫 시도가 checkpoint 직후 다음 단의 CSV를 하나도 쓰기 전에 끊긴 상황으로 놓는다. 사건은 k=3까지 보존한다.
3. 동일한 생성 덱의 실제 `ul_resume=1` 분기를 `deck_sim`으로 실행한다. 상태 파일 k=3/step=3410000, manifest `resume_from=3410000`, RESUME 사건이 서로 일치한다.
4. 새 실행은 k=4 정상 단·RM·RM_STOP을 쓴다. 사건은 RESUME 뒤에 있고, 창·단 CSV는 무중단 대조와 완전히 같다. 원자료·덤프·S3 등 나머지 관측은 동일한 소형 fixture다.
5. 실제 `python -I ul_reader.py arm <root> ps_7_3_r45 UT`를 실행한다.

결과: 무중단 대조와 diff 전 HEAD 판독기는 `OK`, rho=0.20260778734286913. 검토판 CLI는 rc=0이지만 `UNIDENTIFIED`, rho=null, 이유는 “RESUME … 뒤 단 [4] 의 새 시도 소속을 확인할 수 없다”. 새 덱 모의 실행은 `RM_STOP`, abort 없음이다. k=0/1/2에서 같은 유형의 정상 재개도 모두 오거부했다. k=2/3의 창·단 기록은 무중단 기록과 글자 그대로 같다. k=0/1은 모의 상태 숫자 표현 차이가 있어 바이트 동일 보장 대상으로 삼지 않는다.

원인: 259행이 새 단 인증에 무조건 `b in used_rows['windows']`를 요구한다. 옛 꼬리가 없는 정상 재개는 창 step 역행이 없으므로 이 집합에 들어가지 않는다. 따라서 251행이 이미 확보한 RESUME 뒤의 정상 RM 사건도 통과 근거로 쓰이지 않는다.

영향 한정: 정상 재개의 관측을 미식별로 바꾸는 false rejection이다. 이 반례로 잘못된 과학값을 승인하거나 모든 재개가 실패한다고 주장하지 않는다. 옛 CSV 꼬리를 실제로 되감는 기존 양성대조는 통과한다.

권고: 새 완료 사건으로 인증되는 단(및 그 앞의 연속 구간)과 CSV 되감기 흔적을 구별하여 처리하고, 이 clean-resume 양성대조를 추가한다. 단순히 모호성 검사를 제거하면 R37 변이시험이 증명한 false OK/하한 오염이 다시 생긴다.

증거: `deck-probe/deck_probe.json`, `deck-probe/k3/cli.log`, `base-compare/base_compare.json`. 재현기: `deck_probe.py`.

## 기존 제한 / 새 회귀와 구별

다음은 diff 전 HEAD에서도 존재한다. 새 구현이 도입한 결함으로 집계하지 않는다. 발송 문서에서 넓은 “전부 검증”·“모든 요청 step 보장”을 쓰려면 보강하거나 보장 범위를 한정해야 한다.

| 항목 | 위치 | 실제 관찰과 영향 |
|---|---|---|
| R1 / P2 잔여: G2 머리 전체 검증 불충분 | 새 호출 `ul_gates.py:217`, 기존 `ul_lib.py:368` 및 `ul_gates.py:226` | 원자 덤프 BOX BOUNDS 첫 줄을 `nan inf`, 숫자 하나, 빈 줄로 바꾸거나 `ITEM: ATOMS`를 `ITEM: ATOMSGARBAGE`로 바꾸어도 G2 PASS → restore CLI RESTORED rc0 → UB gate rc0. 새 행/ID 검증은 작동하지만 헤더 유효성까지 보장하지 않는다. |
| R2 / P2 잔여: G2c 시점 미대조 | `ul_gates.py:299`, `ul_reader.py:1490` | G2c 시험 쌍 덤프의 TIMESTEP만 S0+1로 바꿔도 G2c PASS → RESTORED → UB gate rc0. 새 G2 원자 expected_step 보장은 접촉 덤프에 확대되지 않는다. |
| R3 / P2 잔여: RESUME k 사전 반올림 | 기존 `ul_reader.py:80`, `:276` | 실제 events CSV의 RESUME k=`3.49`가 `_i`에서 3으로 바뀌어 `(3,3410000)` 승인을 얻는다. NaN/inf/1e309는 승인 거부. 유니코드 숫자 `٣`와 공백 ` 3 `도 숫자 3으로 읽힌다. 소수 반올림을 새 guard 시험이 검증한다고 주장하지 말 것. 이 fixture의 최종 주 값은 F1 때문에 거부되어, 이 관찰로 최종 잘못된 값 승인을 주장하지 않는다. |

별도 문서 정합: 등록 §14-11②(`dem_unloading_ps45_prereg_20261009.md:937`)는 아직 “필수 열 결손 → G2c FAIL”로 되어 있다. 새 코드는 §14-10의 관측 결손 구분에 맞춰 NOT_COMPUTED/UNCONFIRMED를 낸다. 최종 문서 묶음에서 최신 분류를 명시해야 한다.

## 실행 증거

- 검토판 baseline: `ul_gates.py --selftest` 105개 통과, `ul_reader.py --selftest` 204개 통과, 각각 rc0. 로그는 `gates-baseline.log`, `reader-baseline.log`.
- 실제 restore/gate CLI fixture 12종: 정상 1, G2 머리 결함 4, G2c 잘못된 시점 1, 필수 접촉 열 c26 결손 1, 원자 중복 ID·NaN·짧은 추가 행·양쪽 같은 오시점·수치 같고 원 토큰 다른 값 5. c26 결손은 정확히 NOT_COMPUTED/UNCONFIRMED, restore/gate rc2. 마지막 원자 반례 5개도 모두 거부했다.
- ID NaN/inf/−inf/넘침/2^53+1/소수/정수로 반올림되는 소수/0/음수/유니코드 교체 및 좌표 NaN/inf/넘침을 정상 G2 파일과 대조: 13개 모두 FAIL. 유니코드 교체의 FAIL은 원 토큰 불일치이므로 “유니코드 ID 자체 금지”로 해석하지 않는다.
- 변이 12개: 12개 모두 실행 예외 없이 해당 새 시험 단언에서 실패, suite rc1. 전체 로그와 정확한 실패 문장은 `mutations/`에 있다. 모든 가능한 변이의 검출력을 뜻하지 않는다.

| 제거·변경한 guard | 깨진 새 단언 수 |
|---|---:|
| 재개 정합 전체 제거 | R37 7 |
| resume_from 밖 승인 허용 | R38 1 |
| RESUME None 검사 제거 | R38 2 |
| 상태 파일 불일치 허용 | R38 1 |
| 되감을 사건 k 경계 검사 제거 | R38 1 |
| grammar kit 목록 결합 검사 제거 | R38 3 |
| grammar subprocess rc 검사 제거 | R38 1 |
| G2 중복 ID 검사 제거 | C5 2 |
| G2 파서 ok 검사 제거 | C5 8 |
| G2 기대 step 검사 제거 | C5 1 |
| G2 원 토큰을 float 문자열로 정규화 | C5 1 |
| G2c 결손 상태를 FAIL로 복귀 | C4 52 |

변이시험은 메모리에 로드한 모듈만 바꾸었다. CLI를 호출하는 selftest 하위 프로세스는 원 검토판을 사용하므로, 표의 검출력은 각 함수 guard에 대한 인프로세스 새 단언 범위다. 독립 반례의 production CLI 실행은 별도 증거다.

## 다른 checkout에서 재현

모든 Python 재현기는 `--repo`, `--out`를 받는다. `--out`은 checkout 밖의 새 폴더를 사용한다. 아래 `$REVIEW`는 이 보고서와 재현기를 복사해 둔 폴더다. `mutations.py`는 검토판 소스 문자열을 정확히 요구하므로 수정 후 판에서는 patch 대상 미일치로 멈출 수 있다.

```bash
python -I "$REVIEW/deck_probe.py" --repo "$REPO" --out "$OUT/deck-probe"
python -I "$REVIEW/restore_probe.py" --repo "$REPO" --out "$OUT/restore-probe"
python -I "$REVIEW/edge_probe.py" --repo "$REPO" --out "$OUT/edge-probe" --fixtures "$OUT"
python -I "$REVIEW/mutations.py" --repo "$REPO" --out "$OUT/mutations"
python -I "$REVIEW/base_compare.py" --repo "$REPO" --out "$OUT/base-compare" --fixtures "$OUT"
```

`base_compare.py`는 checkout HEAD를 diff 전 기준으로 읽는다. 새 커밋 뒤에는 검토 전 HEAD를 지정하도록 스크립트의 `--base-ref`를 사용한다. 외부 실행·네트워크·GPU를 사용하지 않는다. 전체 저장소 게이트는 중복 실행하지 않았다.
