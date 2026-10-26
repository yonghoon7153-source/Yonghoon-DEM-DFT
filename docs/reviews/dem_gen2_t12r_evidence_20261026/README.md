# T12R-01 오프라인 회귀 증거

외부 수용된 소비자 해석과 ULPRI 종결은 유지한다. T12R-01은 로컬 claimed fixed / 외부 재확인 대기이며 물리 T12 NOT_RUN이다.

- `author/pre-fix/result.json`: 실제 Git 누락 commit/root-tree/kit-tree/blob 대조에서 각 fetch3회. 원본 실패 증거다.
- `author/final/result.json`: Git2.52.0 실제5조건(완전객체 안의52양성, 누락4조건), 누락 rc2/fetch0/객체DB불변. 부모 환경0에도 자식보호를 확인했다.
- 보호 전체 제거 변이는 실제 로컬 fetch3회를 노출했다. unsupported-option 호환성 검사는 명시된 mock이며 옛 Git 실물 검증이 아니다.
- `loader-report.json`: 기존 소스거부5/계약결손3. `mutants-report.json`: 기존13표적변이의 지정 의미 실패. 예전 portable harness를 변경하지 않고 새 runner를 source로 사용했다.
- `targeted-binding.json`: 실제 runner/회귀hash와 새52관측/소비자hash의 이전결과 일치. 독립52를 불필요하게 한 번 더 돌리지 않았다.

시험 수는 중첩되어 합산하지 않는다. 직접52·새오프라인회귀는 공용155/CI에 연결되지 않았다. 전체게이트는 후보커밋 뒤 별도기록하며 이 문서는 아직 그 결과를 대신하지 않는다.

합성 회귀를 다시 실행하려면 적합한 Git(전역 --no-lazy-fetch 인식), Python, 지정 소비자의 로컬 Git 객체가 필요하다. 출력은 새 경로여야 한다. 아래는 로컬 fixture 검사이며 물리/WSL/연구 실행이 아니다.

```bash
python3 -I -B scripts/test_dem_gen2_t12_offline.py --repo . --output /tmp/t12r-offline-new --check-guard-mutation
```

기존 소스/계약·변이 재현 도구는 고정 원본을 사용하고 --source에 이번 수정 runner가 있는 checkout을 준다. 이 증거의 runner와 당시 고정 소비자 소스를 구분한다. 실제 통합 소비자를 검증하는 향후 CI는 별도 조건이다.
