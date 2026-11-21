# Ⓑ MPM 상태와 접촉 피복 격자 연결

11-21 개발 범위는 고정 AM scaffold를 사용한 주기 3D 상태와 원 입력 사이의 좌표 대조다. 현장 파일 판독과 연구 결과는 0건이다. 측정 정의는 `docs/reviews/mpm_coverage_interface_design_memo_20261103.md` §4-1·Q5·T13과 11-16 번호 계약(`425b9d281`) §2다.

## 상태 입력

`scripts/mpm_coverage_state.py`가 `scripts/mpm3d_compaction.py`의 `write_state_npz`/save-state 형식과 `scripts/mpm_input_from_case.py`가 만든 AM·SE scaffold CSV를 읽는다. 사용 예시는 아래와 같다.

```sh
python3 -I -B scripts/mpm_coverage_state.py STATE.npz AM.csv SE.csv source_receipt.json
```

입력 JSON에는 `state`, `am_scaffold`, `se_scaffold` 세 역할과 호출자가 선언한 각 파일의 SHA256이 필요하다. CLI는 받은 바이트와 선언을 대조하고 `execution_source_identity=NOT_ESTABLISHED`, `coverage_source_scope=CONDITIONAL_ON_EXTERNAL_RUN_BINDING`으로 출력한다. 운영자가 실제 실행 당시의 영수증과 대조해 출처를 별도로 확인할 때까지 상별 피복, 씨앗·끝 비교와 증가분은 제공된 세 파일에 조건부다. 원위치·시각·권한을 가진 실행 영수증을 CLI가 검증하는 단계는 이번 범위 밖이다.

| 연결 | 처리 |
|---|---|
| 격자 | `meta_json`의 schema, n_grid, nz, lateral_box, FLOOR, um_box_um, dilate_z와 주기 경계를 대조한다. x·y는 0.04–0.96의 격자 정렬 주기 구간, z는 전체 nz이며 벗어난 SE 점은 거부한다. 셀 폭은 um_box_um/n_grid다. |
| AM | CSV의 type 1·2와 행 순서를 유지한다. 저장 AM 중심·원 반경·적용 반경을 변환된 CSV 기하와 대조한다. 겹침 셀에서 고정 생산기의 뒤 행 우선 규칙을 재현한다. 이번 범위는 적용 반경이 원 반경과 같은 scaffold다. |
| SE | 원 CSV의 type 3 구에서 AM 가림을 제외하고 셀당 8점으로 씨앗을 재생한다. 끝 점은 native x·phase에서 SE(phase 1)만 센다. 첨가제 2–6은 제외한다. 씨앗 총 점 수와 끝 SE 점 수의 일치를 확인한다. |
| 피복 | 기존 `scripts/mpm_coverage_c0.py`의 같은 분모·면 측정 함수를 사용해 C_seed, C_end, 증가분과 이음매 면을 반환한다. 강체 기준이 공급되지 않아 C_rigid·씨앗 치우침은 null이다. |
| 번호 운반 | `transport_owners`는 호출자가 제공한 불변 점 키·DEM atom ID·canonical 순위로 끝 점을 조인한다. 셀 안 4점 이상에서 다수결, 동률은 순위로 가른다. 키 결손·분할·중복과 순위 충돌을 거부한다. 64비트 정수 ID를 부동소수로 바꾸지 않는다. |

native 상태의 `se_id`는 기존 최근접 구 중심의 행 인덱스다. CLI는 이 값을 사용하지 않으며 `se_point_identity=UNESTABLISHED`를 출력한다. 동일 DEM 원천에 결속된 atom ID·공유 power 소유 함수·점별 계보가 준비되어야 생산 데이터의 번호 승계를 검증할 수 있다. 단순 5열 scaffold나 끝 좌표 `.npy` 하나로는 점 순서와 출처를 증명할 수 없다. 주기 x/y와 tall z를 지원하는 pristine frame에 한정하며 변형 반경·벽 경계·분할·강체 해석과 양의 근접 띠는 후속이다.

## 합성 확인

`scripts/test_mpm_coverage_state.py`의 최초 API 요구 10개는 모듈 추가 전 10실패·오류 0, 추가 뒤 동일 10/10 통과했다. 첨가제 5·6과 다른 AM 두 상이 같은 주기 셀에 걸치는 경우를 남긴 중간판은 11개 중 오류 3개(하위 사례 포함)였다. 보완 뒤 같은 11개, 넓은 구를 포함한 전체 격자의 독립 구 판정·행 순열 대조까지 12/12 통과했다. 추가 출처 회귀는 원본, 셀 수를 보존하며 SE를 옮긴 입력, AM 중심·반경을 보존하며 상을 바꾼 입력을 확인한다. 각각 새 선언 해시와 맞고 피복값 또는 해당 상은 달라지지만, 세 경우 모두 원 실행 신원은 미확정으로 반환한다. 이 회귀의 표지 추가 전 3개 하위 사례 실패, 추가 후 최종 13/13 통과. 기존 면 9/9, 씨앗 4/4도 별도로 통과했다. 실제 MPM·DEM 엔진과 원자료 판독은 0건이다.
