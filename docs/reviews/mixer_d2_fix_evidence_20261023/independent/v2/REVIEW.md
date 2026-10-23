# MXD2 생성기 v2 독립 재확인

2026-10-23. **v1 R1–R4 닫힘. 이번 v2 diff에서 새로운 결함을 발견하지 못했다.** 이 판정은 아래 생성기 코드와 시험 범위에 한정한다. 전체 저장소 게이트, 되읽기·비교기 통합, LIGGGHTS 실행, 반박 세션 GO·발사 승인을 대신하지 않는다.

## 입력과 최종 코드 신원

작성자 결과·요약은 읽지 않았다. 입력은 `generator-v2.patch`, `review-delta.patch`, 실제 원본 소스와 이전 독립 검토의 반례다. 원본에 첫 패치를 적용한 결과와 v1 코드에 delta를 적용한 결과를 직접 비교했으며 **바이트가 같다**.

| 대상 | 직접 계산한 SHA-256 |
|---|---|
| 원본 `scripts/make_mixer_deck.py` | `6baaa04c13c842c2d8e486cbef83bb5cb6f6e3d5f88c5f0f0d8c0904d3949f30` |
| `input_generator.patch` | `2b865ee1e553f4ebc737599888cd22ab99c7be6fe41cd65cf440b793786ad210` |
| `input_review_delta.patch` | `ac13a4c415ab1d03985a56e12102b665a61a2746abccb1c5da795c5ae6604586` |
| **최종 생성기** | **`661936b78c3d60794714a63102f5461f7f42f581a5ad7da466c7c6fe0465bc27`** |

최종 소스 사본: `evidence/snapshot/scripts/make_mixer_deck.py`. 모든 산출물은 이 `v2/` 아래에 썼다. v1의 `MANIFEST.sha256` 네 항목은 작업 종료 시 모두 OK이며, v1 보고서·스크립트·입력 patch·결과 JSON은 바뀌지 않았다. tracked 수정·commit·push·전체 게이트·장비 실행은 하지 않았다.

## R1–R4 재현 및 역변이

| v1 항목 | 실제 재현 | 검사 유효성 | 재확인 |
|---|---|---|---|
| R1 P2 실제 중력 누락 | 출력 `gravity`를 직접 읽은 Bo는 정상 192덱에서 입력과 일치 | D2에만 중력 1.0을 출력하는 기존 생존변이 → `MXD02`와 `MXDR1` 실패. 판독기 무게를 다시 9.81 상수로 바꾸는 별도 변이 → `MXDR1` 실패 | **닫힘** |
| R2 P3 `AM_P+SE` 회귀 | 기존 원본·v2 둘 다 덱 발행. 별도 ρ 4값 × 코팅/비코팅 = **8개** 2상 덱에서 SE(type 2)의 실제 출력 Bo·메타 상 신원 확인 | AM_P/AM_S 두 값을 무조건 요구하는 옛 조건으로 복귀 → `MXDR2` 실패 | **닫힘** |
| R3 P3 desc 실행 줄 | LF·CR·CRLF·int·list·dict·bool **7종**을 생성자 및 생성 후 사전 변조에 적용. 각각 생성자 경로·deck·deck_meta = **21개** 통제된 거부. 빈 문자열·한글·일반 설명·말미 `&`의 정상 설명 4개는 발행 | 설명 guard 전체 삭제 및 CR guard만 삭제하는 두 변이 모두 `MXDR3` 실패 | **닫힘** |
| R4 P3 scalar CLI 시험 공백 | 두 scalar 옵션에 NaN/inf/넘침/subnormal/밑줄/Unicode/공백/빈값/0/음수 **20개**를 실제 CLI로 전달, 전부 거부하고 덱 없음 | `--gm-wall-ncm` 또는 `--gm-bo-se`의 type만 각각 float로 복귀 → 두 변이 모두 `MXDR4` 실패 | **닫힘** |

CR/LF는 생성자에만 넣지 않았다. 정상 팔 생성 뒤 `ARMS`의 설명을 바꿔 **실제 deck·deck_meta 함수**를 각각 호출해 재검증을 통과할 수 없는지도 확인했다. scalar 변이의 실패는 정상 세대·정상 ρ 세계에서 밑줄 입력을 발행할 수 있기 때문에 발생하며, 다른 입력 오류를 우연히 밟은 것이 아니다.

## 추가 회귀 공격과 증거

- 자체 selftest **158/158 PASS**, rc 0 (`selftest.log`).
- 정상 3상 조합: 밀도 2세대 × CGF 3값 × 강성 2값 × ρ 4값 × 코팅 2값 × Bo 2값 = **192 덱**. 실제 출력 SI 값으로 **1,728개 접촉쌍**의 F0·R*·E*·기하평균·벽·겹침을 확인했다. Bo 최대 상대오차 **1.2876531367167487e-5**, 쌍 힘비 최대 상대오차 **2.5893352707528905e-5**이며 6자리 CED 인쇄 정밀도 범위다.
- 위 192덱은 **v1과 출력 바이트가 전부 같다**. 메타는 바뀌어야 하는 `generator_sha256` 하나를 제외한 모든 값이 같다 (`prior_comparison.json`). 기존 팔 바이트는 자체 골든 시험도 통과했다.
- 실제 CLI 비정상 입력 **32개**(gamma 12 + scalar 20): 모두 rc≠0, traceback 없음, `in.mixer` 없음. 수치·구조·헬퍼 경계 **49개**도 재실행했다 (`evidence/results.json → input, cli_input`).
- 변이 **14/14 포착**. v1의 10개를 그대로 다시 실행하고, 판독기 중력 상수 복귀·옛 활성상 조건·desc guard 삭제·CR만 삭제 4개를 추가했다. 각각 관련 MXD 검사에서 실패했다. 단순 전체 rc만으로 판단하지 않았다 (`evidence/mutants/*/selftest.log`).
- 생성기 정상 경로에서 새 단위·밀도·쌍 규칙·메타값 회귀를 발견하지 못했다.

v1에서 따로 적었던 **임의 text와 `deck_meta` 입력의 결합**, **호출자가 변조한 계획의 밀도 세대 라벨↔표**, **점착 지배 무하중 δ0와 중력 하중 접촉의 구분**, **일부 비정상 사전 구조의 TypeError/KeyError**는 이번 수정 범위 밖이며 다시 같은 한계가 관찰됐다. 이를 새로 닫았다고 주장하지 않는다. 안전여유나 물리 정책은 결정하지 않았다.

## 재현

```bash
source /workspace/.cloud-setup/nonrint/activate.sh
python -I reproduce.py \
  --repo /path/to/original/repo \
  --patch /path/to/v2/input_generator.patch \
  --out /tmp/mxd2-v2-review

python -I compare_prior.py \
  --prior /path/to/v1/evidence/snapshot/scripts/make_mixer_deck.py \
  --current /tmp/mxd2-v2-review/snapshot/scripts/make_mixer_deck.py \
  --out /tmp/mxd2-v2-review/prior_comparison.json
```

`reproduce.py`는 판정 근거를 JSON과 변이별 로그로 남기는 기록기다. 성공 rc 하나를 승인으로 읽지 않고 `results.json`의 각 결과를 확인한다. 원본 저장소는 읽기만 하며 실제 시뮬레이션은 실행하지 않는다.
