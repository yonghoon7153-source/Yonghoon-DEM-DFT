# 간편 전달 ZIP의 범위

이름 끝이 `_review.zip`인 간편 묶음은 판정문·요청서·독립 탐침·원본 결과·합성 입력·소스 해시 목록을 포함한다. **현재/이전 source 폴더는 생략**했다. 검토 결과를 읽고 반례·시험 상태를 확인하는 전달용이다.

독립 재실행까지 하려면 같은 이름에서 `_review`가 없는 전체 ZIP을 사용하거나, manifest에 적힌 두 핀의 소스를 해당 형제 폴더 구조로 준비해야 한다.

- 전체: `codex_rint_join_rimpr_q7_recheck_20261020.zip`
- 간편: `codex_rint_join_rimpr_q7_recheck_20261020_review.zip`

전체 묶음의 구성·실행 규약은 `README_REVIEW.md`에 적었다. 간편 묶음의 소스 미포함을 “소스 검증을 하지 않았다”로 읽지 않는다. 최종 source integrity 결과는 `evidence/final_source_integrity.json`에 있다.
