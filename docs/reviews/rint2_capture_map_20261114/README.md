# Rint Q12 — 조립 객체에서 기록까지의 정적 연결 지도

## 1. 고정 범위

바탕 f361c62b684bf69666bfc8edc043ba2a9b97777e. 실행 소스 핀 64e4d213e8267bafaf3ae5af00a42996cefd3f33의 `scripts/carbon_junction.py`와 `scripts/cjunc_asm_compare.py`를 읽고 AST로 위치·표현을 확인했다. `source_map.json`에 두 원 blob·SHA·선택 함수 범위를 보존했다. import·조립·σ·실제 배열·현장 접근0, 소스 수정0, 전체 HOLD.

이 기록은 기존 `docs/reviews/rint2_capture_ownership_20261114/ownership_options.md`의 미정 연결 위치를 좁힌다. 소유권 O1/O2/O3 선택, 실제 수집기 구현·등록 동결·최종 핀 변경 승인은 아니다.

## 2. 찾은 연결 위치

| 항목 | 고정 소스 근거 | 구현 전 필요한 연결 |
|---|---|---|
| 원 DOF 순서 | _assemble의2789행은 np.flatnonzero(kept)를 graph 지문에 사용. 2797행은 new[kept] = np.arange(n_kept) | 같은 완료 객체의 원 DOF 목록을 보존해야 함. n_dof 개수만으로 원 번호를 복원할 수 없음 |
| 현재 반환 | 최종 out에는 L/b/Ab/gb/At/gt/cb/ct/n_dof가 있고 kept·원 DOF 배열은 없음 | 원 DOF 수집은 현재 out만 받는 후처리로 끝낼 수 없음. 명시적 노출/소유권 연결이 필요하며 소스 핀 영향 검토 대상 |
| 그래프 지문 | build는 st의 graph_fp를 self.graph_fp에 둠 | 후속 build가 갱신하기 전에 out·원 DOF·지문을 같은 시도에 결속 |
| 판 결합 별칭 | st['sys']와 out이 Abn/gbn/Atn/gtn의 같은 이름을 사용하고, build는 st['sys']를 self.sys로 보관 | 반환 dict만 별도로 소유한다고 모든 배열 writer가 차단됐다고 가정하지 않음 |
| CSR/RHS/판/DOF descriptor | assembly_record는 _arr를 순서대로9곳 호출 | 배열 각각의 지문이 있어도 전 배열이 한 시점이라는 근거는 별도 |

원 DOF 후보는 이 고정 구현의 keep→재번호화 순서에서 유도한 위치 제안이다. 조기 반환·다른 모드·새 조립기까지 전칭하지 않는다. 단락/모든 부유 제거/관통 없음 등의 reason 반환은 완결 조립 양성으로 채우지 않는다.

## 3. 기록 구간에 포함할 것

assembly_record의 _source_array는 np.asarray를 거친 검사를 하고, _arr는 배열별 dtype/shape와 연속 바이트를 차례로 해시한다. 이 코드에는 전 입력 배열을 한 번에 고정하는 명시적 사본/잠금 구간이 없다. 이것만으로 실제 동시 변경이 발생했다고 판정하지도, 호출자의 소유권이 보장됐다고 판정하지도 않는다.

O1이라면 CSR·RHS·판 결합·원 DOF뿐 아니라 해당 graph_fp와 시도 출처가 기록 종료까지 같은 완료 객체에 속하도록 writer를 제어해야 한다. O2라면 한 일관 시점에서 이 묶음을 복사해야 하며, 순차 복사 도중 변경된 혼합 묶음은 같은 snapshot이 아니다. O3는 생산자와 별칭의 불변성 증거가 있어야 한다. 어느 방식도 이번에 선택하거나 구현하지 않았다.

DOF descriptor는 현재 ids.astype(np.int64)를 사용한다. 이 정규 표현과 원 ID 배열 dtype 기록은 구분한다. 원 배열을 정렬·재합산해 환경 차이를 없애지 않는 기존 Q12 규칙도 유지한다.

## 4. 다음 연결과 미확인

권고 연결 후보는 _assemble의 완료 반환 직전 원 DOF를 확보하고, build의 같은 시도 out/graph_fp와 수집 구간을 결속하는 것이다. 실제 방식은 소유권 선택·사본 비용·예외 원본 보존·고정 핀 재검토 뒤 정한다. collector가 단순 후처리만으로 완결된다고 가정하지 않는다.

고정 핀 scripts/*.py에서 정확한 `assembly_record(` 철자를 검색한 결과, 정의 외 사용은 시험 파일에 있었다. alias·동적 import·다른 철자의 호출망까지 없다는 증명은 아니다. 전체 호출망·writer 분석·CAP01–10 실제 시험은 미완료다.

소스64e4d213e와 S0/Q11/⑥ 원 블록은 보존했다. 현장 실행·조립 결과 수령·운영자/UTC/자원·시도3/4·독립 반박2/2·봉인 GO는 이 정적 지도에서 변경하지 않는다. 원장 수정은 없다. 저장소 점검은 `check_results.json`, 변경 범위는 `scope_check.json`에 기록한다.
