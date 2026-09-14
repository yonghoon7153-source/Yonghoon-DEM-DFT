# `out/archive/` — 얼어붙은 역사 자료 (현재 산출이 **아니다**)

여기 있는 파일은 문서가 "고치기 **전**에는 이랬다" 를 말할 때 근거로 쓰는 옛 산출이다. 현재 파이프라인이
만들지 않으며, `compare_states.py`·`ne_shape.py`·`check_u14.py` 의 glob(`out/*.csv` — 비재귀)에 걸리지 않는다.

| 파일 | 무엇 | 누가 인용하나 |
|---|---|---|
| `matrix_300_0009_premultistart.csv` | `multistart` 가 **비정상 종료한 optimizer 결과를 성공으로 채택**하던 판의 `matrix_300_0009.csv` (커밋 `bfc4623^` 의 것) | `FINDINGS.md` §4-0 (수정이 답을 최대 5.9 %p 움직였다) · §3-3 각주 |
| `degeneracy_300_0009_Li_v2.json` · `matrix_300_0009_v2.csv` | multistart 수정 **후** 첫 재실행 (2026-09-10, meta·run_id 없음). U14 재실행이 이 둘을 **비트 단위로 재현**해 정본은 unversioned `degeneracy_300_0009_Li.json`·`matrix_300_0009.csv` (meta·env·inputs_sha 포함) 로 넘어갔다 (Codex R6-04) | 역사 대조용. FINDINGS 의 인용은 unversioned 로 옮겼다 |
| `legacy_r6_u14/` (26 파일) | **U18 승격 전의 정본** — 게시·서명 계약이 R13 이전이라 receipt·env·argv·roster 가 없다 (`check_u14 --new out --schema-only` 가 rc 2 로 말하던 그 묶음). U18b 재실행이 **같은 숫자**를 새 계약으로 다시 서명해 정본이 됐고, 이것은 조건 7 의 보존 요구("기존 provenance-incomplete out/ 는 보존")대로 얼려 둔다 | `R13_RESPONSE.md` §8 · `WORKING_STATE.md` U18 런북 |

## 왜 여기로 왔나 (U14-05, 2026-09-12)

U14 재실행(`STATES='100 200 300_0009 300_0147'`)이 `out/matrix_300_0009.csv` 를 새로 썼는데, 그 자리에 있던 것이
바로 그 **수정 전** 산출이었다. 재실행은 수정된 코드로 도니 `_v2` 를 비트 단위로 재현했고(최대 상대차 0.00e+00),
§4-0 이 재던 "전 ↔ 후" 의 **전** 이 사라졌다 (새 파일 ↔ 옛 v1 최대 상대차 4.17e-01).

교훈: **파이프라인이 덮어쓰는 이름에 역사 자료를 두면 안 된다.** 재실행은 언제든 다시 일어난다.
