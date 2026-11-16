# P1 G2c′ A/B 개정 5 설계 확인 패킷

| 이번에 닫는 것 | 닫지 않는 것 |
|---|---|
| SR5-01–08의 설계 문구 누락·모순, 수정 위치를 보는 문서 회귀 | 생산 키트·B 구현, 엔진/MPI·현장 자격, RJ 발사·봉인·물리 자격 |

바탕 `d5cf6307fd5165732e31d9cb5e1044f42aea1a0e`; 가지 `codex/p1ab-rev5-1116`. 전체 HOLD. 연구 결과 0건. 이전 외부 설계 판정은 미수령이다. 원장·공유 기록·봉인 파일은 직접 바꾸지 않는다.

## 구성

- A = `docs/reviews/dem_unloading_ps45_prereg_20261009.md` §15.
- B = `docs/reviews/p1_g2c_mpi_stage2_registration_20261112.md`.
- 요청 = `docs/reviews/codex_p1_g2c_ab_design_request_20261112.md` Q1–Q10.
- `disposition.md`: 내부 5회차 8건의 위치별 처분.
- `historical_identity.json`: 스크래치 표지와 현재 반입된 과거 문서 8개의 SHA256.
- `check_design.py`: 활성 절·표·덱 예시·역사 바이트 신원을 직접 읽는 12메서드 문서 회귀. 정해진 문구의 퇴행을 검사하며 임의 산문의 의미나 생산 동작을 인증하지 않는다.
- 사전 공격과 검사 영수증은 이 폴더의 해당 기록을 따른다. 실제 반박 요청의 고정 핀·포장 해시는 바깥 ZIP의 PIN/목록으로 제공한다.

## 시험 먼저

같은 expected-correct 문서 회귀를 수정 전 바탕에 적용하면 12메서드 중 11실패·오류0, 수정 후에는 12/12이다. 나머지 한 메서드는 원래 보존할 문턱/시도 정책이다. 최초 준비 실행에서 코드 블록의 주석을 문서 제목으로 오인해 1오류가 났고, fenced block을 건너뛰도록 검사기만 바로잡은 뒤 **문서 수정 전에** 위 red를 다시 확보했다. 그 준비 오류를 후보 결함이나 수정 효과 수로 더하지 않는다.

재현 (ZIP의 before/ 또는 snapshot/을 ROOT로 사용):
```text
python -I -X utf8 -B snapshot/docs/reviews/p1ab_rev5_20261116/check_design.py --root before --report red-new.json
python -I -X utf8 -B snapshot/docs/reviews/p1ab_rev5_20261116/check_design.py --root snapshot --report green-new.json
```
보고 파일은 새 이름이어야 한다. 기대 rc는 수정 전 1, 수정 후 0. 시험은 키트·엔진·MPI를 import/실행하지 않는다. B의 41→49, RT 검사20, R41–43 등은 **다음 구현 시험 계획**이며 이번 실행 수가 아니다.

내부 사전 공격에서 초기 회귀의 약화9 생존이 발견되어 활성 규칙의 처분·부등식을 직접 검사하도록 보강했다. 같은 기존 변이13개와 추가2개는 모두 검출됐다. 독립 조수 결과는 **Codex 아님**이며 preattack.md와 원 JSON 두 개에 남겼다. 재현은 `python -I -X utf8 -B snapshot/docs/reviews/p1ab_rev5_20261116/mutation_check.py --root snapshot --report mutations-new.json` (rc0 = 기준 문서 통과 및 모든 약화 사본 거부)이다. 이는 후보 실패를 성공으로 포장한 검사가 아니라 정상 문서와 문구 변이를 구분하는 별도 검사다.

## 다음 순서

1. 개정 5 설계 반박: 1저자가 고정 ZIP을 별도 반박 창으로 보냄.
2. 설계 판정 수령 → 처분·필요한 고침 → 설계 GO.
3. B의 새 합성 시험에서 실패 확인 → 구현 → 회귀/변이·사전 공격·고정 핀.
4. 반박/정해진 검토 조건을 충족한 뒤 건식 NP2·4 블록, 1저자 개별 GO, 결과 수령.
5. A 구현·RT 문법 fixture·B 결과·동결된 ⑥′ 조건을 갖춰 별도 RJ 발사 GO 요청. 현재 문서는 이 단계를 열지 않는다.
