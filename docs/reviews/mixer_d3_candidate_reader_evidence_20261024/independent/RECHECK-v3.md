# D3 candidate reader independent recheck — frozen v3

판정: **입력 조건부 유한 후보 계산기 범위에서 PASS.** 유효했던 D3IR-01(P3) 오류 처리 누락이 해소됐고, 검토한 변경·추가 반례에서 새 P1/P2/P3 finding은 발견하지 못했다. D3IR-02는 수정 완료가 아니라 **검토자 오탐 철회**다(`ERRATUM-D3IR-02.md`). 이 결론은 실물 관측/통계/등록/맹검/물리 자격/외부 GO 판정이 아니다.

검토 reader SHA256: **ea4528156e8eb9762999fef0643985bebf0b0735691202fddb4a2c17814ee7f8**.
검토 tests SHA256: **12155f4e420ea3b15529501562b9fd6758c2767cbfcf4e1c79d6cdd7f4034d4c**.
검토 계약 문서 SHA256: **9e5871a4346af4cd8b1fce05845402e7ae9c05f76cee5b0bbc35683b77cd0232**.
사본·목록은 `reviewed-v3/`와 `reviewed-v3-sha256.json`, 실제 변경은 `mixer_d3_candidates.py.v1-v3.diff`다. 이후 코드/계약 변경에는 이 판정을 자동 적용하지 않는다.

| 검사 | 실행 결과·범위 |
|---|---|
| 작성자 회귀 재실행 | Python **3.11.17**, `-I -B`, **28 unittest PASS**, rc0. `v3-author-suite.stderr.log`. 독립 작성 시험으로 세지 않는다. |
| 독립 재공격 | 같은 환경에서 `probe_independent_v2.py`, **19개 명명 검사 19 PASS**. 세 점×두 보정 시험 C/I/U **729조합**은 그중 하나의 전수 검사다. `v3-results/results.json`. |
| 실제 CLI 오류 분류 | control rc0·파일 생성; 양/음 거대 지수 및 중복 JSON key는 **rc2·파일 없음·traceback 없음**. `v3-results/cli-probes.json`. 원 v1의 두 거대 지수 rc1은 보존했다. |
| 원 7개 의미 변이 재실행 | v3 reader에서 경계·교집합·격자 틈·불확도·예약 시드·raw hash·불완전 우선 guard를 각각 변경. **7/7 지정된 AssertionError**로 검출. `mutations-v3/summary.json`. |
| 수정/보고의 추가 변이 | Decimal 예외 catch 제거→실제 CLI rc 비교 단언 실패; reason 검사 제거→지정 단언 실패; Bo_po 제수6.75→6.76→정확 유리수 오차 단언 실패. **3/3**. `targeted-mutations-v3/summary.json`. 따라서 최종판 독립 변이는 합계 **10/10**, 작성자 별도 변이 수와 합산하지 않는다. |

의미 검토에서 보존된 사항:

- 관측과 폭이 유효한 평탄 `INSENSITIVE` 응답은 세 후보 모두에 남는다. 식별 가능성 주장은 없다. 실제 부적격 또는 불확도 결손은 UNASSESSED이며 그 틈을 가로질러 후보 묶음을 잇지 않는다.
- 후보별 필수 검증 미평가가 있으면 요약은 unassessed이고 이미 관찰한 incompatible 칸을 보존한다. 검증으로 S를 다시 축소하지 않는다. 빈 S를 검증 성공으로 세지 않는다.
- 0.4−0.3=0.1 동률, 64자리 경계 바로 밖, ±1e300와1e−300 계산을 검사했다. Bo_po 표시는 6.75 정의와 50자리 표시를 확인했으며 과학적으로 새 단일 대표값을 고르지 않는다.
- 실제 artifact bytes/조건 bytes/CLI 계약 입력 hash 결합을 검사한다. **원자료의 숫자 추출 일치와 eligible 선언의 과학적 타당성을 이 계산기가 확인하지 않는 범위**는 공개 계약 §3에 명시돼 있다. 원값만 바꿔도 raw hash는 같을 수 있는 작은 반례를 보존했다. 실제 관측 판독기·통계·영수증 검증의 완료로 읽지 않는다.
- C0/C1/C2 예약 세 시드 및 미선언 겹침을 거부한다. 명시한 짝은 독립 표본으로 인증하지 않는다. 역사적 미사용·누락/빈 manifest의 실행 준비를 주장하지 않는다.
- eligible 선택 reason의 잘못된 타입 거부와 유효 reason 보존을 독립 확인했다. 이 추가 수정은 D3IR-01 외 작성자 개선이며 새 독립 finding을 소급 발명하지 않았다.

재현은 보존한 reader 사본을 대상으로 새 출력 폴더를 사용한다. `probe_independent_v2.py --module <reader> --out <새 폴더>`, `mutation_probe.py --module <reader> --out <새 폴더>`를 Python3.11 `-I -B`로 실행한다. `targeted_mutations_v3.py`는 이 증거 폴더의 `reviewed-v3/`를 참조하며 이미 존재하는 출력 폴더를 덮지 않는다. 원자료 경로를 따라 외부 파일을 실행하지 않는다.

전체 저장소 게이트·웹앱 통합·실험/DEM·새 기하/정책은 이번 독립 검토에서 실행하지 않았다. root 통합 후 전체 gate와 새 스크립트 직접 시험은 각각 기록해야 한다.
