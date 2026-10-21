# 재현 안내 — Rint ② 설계·Part B 조인 검토

## 범위

검토 핀 `5dc6f7f0b91fd9db39ab595f6b8c79a8f0d2f3b5`. 원본 Git checkout·생산 파일은 수정하지 않았다. `source/`는 이 핀의 필요한 파일만 읽기 전용으로 확보한 사본이다. Git 저장소 전체가 아니므로 옛 Git객체를 읽는 시험은 그대로 실행할 수 없다.

최종 판정은 `codex_review_rint2_carbon_additive_design_20261021.md`. 하위 메모는 독립 검토 기록이고 최종 번호는 판정문 표를 따른다. 특히 설명용 조작 전압의25% 수렴 예와 실제 첫 CG가 만든0.0188593% 예를 혼동하지 않는다. 후자가 본문 반례다.

## 실행 환경

- Python3.12.14, NumPy2.5.3, SciPy1.16.3.
- 검토에서는 `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`, `MKL_NUM_THREADS=1`을 사용.
- 스크립트 일부에는 이 작업공간의 기존 `deps` 경로를 우선하는 편의 경로가 있다. 새 환경에서는 NumPy/SciPy를 설치한 Python을 사용하면 된다. 존재하지 않는 편의 경로가 설치된 라이브러리 import를 막지는 않는다.
- 라이브러리 바이너리·실행기·GPU·DEM/MPM 실행물은 배포 ZIP에 넣지 않았다. 대규모 시뮬레이션 재실행이 필요하지 않다.

## 작은 독립 반례

검토 ZIP을 풀고 이 폴더에서:

```text
python -B geometry/geometry_probes.py
python -B registration/probe_registration.py
python -B geometry/convergence_probes.py
```

기하 반례는 실제 pinned `fibre_segment_raster.segment_cells`를 호출한다. 등록 반례는 독립 양의 수동 저항망의 해석 응답/판정표이고, 재압밀 산술만 pinned 코드의 스칼라 블록을 추출한다. 수렴 반례는 실제 pinned `_solve_cg`와 `certify`를 호출한다. 결과 JSON이 각 하위 폴더에 갱신된다.

`geometry/search_cg_counterexample.py`는 고정 반례를 찾을 때 쓴 검색 기록이다. 반례 재현에는 검색을 다시 할 필요가 없다. 검색으로 고른 사례라는 사실을 숨기지 않았으며, 작성자의 실침대 결과를 본 선택은 아니다.

## Part B

`part_b/REPRODUCTION_part_b.md`와 `part_b/PART_B_REVIEW.md`를 따른다. 원 시험과 LF 픽스처 어댑터 시험은 따로 실행한다. 원본 생산 판독기와 시험 파일은 불변이며, `--lf-test-writer`는 검토 harness가 메모리/검토용 사본에서 시험용 쓰기만 바꾸는 실행이다.

전체 핀에 대해 현재 시험·이전 탐침·독립 입력을 다시 실행했다. 초기 부분 overlay 로그는 `part_b/preliminary_overlay_evidence/`이며 최종 실행과 합산하지 않는다. 과거 probe가 출력 내부에 보존한 옛 `source_pin` 문자열은 실행 harness의 실제 모듈 경로/해시 기록과 구별한다.

Windows `resource` 모듈 대체는 메모리 사용량 출력용이다. 수치 해·입력 문법·판정식을 바꾸는 어댑터가 아니다. 세부 변경은 harness에 공개돼 있다.

## 증거·무결성

- `source_manifest.json`: 원격 고정 핀 Git blob 및 파일 SHA256.
- `evidence/zip_pin_comparison.json`: 사용자 첨부 리포44파일과 핀 비교.
- `evidence/commit.json`, `evidence/tree.json`: 읽기 전용 원격 핀 메타데이터.
- `part_b/evidence/fullpin_overlay_match.json`: 초기 검토 경로와 전체 핀의21개 의존성·시험·자료 동일성.
- `geometry/*results.json`, `registration/*results.json`, `part_b/evidence/`: 독립 실행·검산 로그.
- `integrity_final.json`: 포장 직전 source 전수 재해시 결과.
- `delivery_manifest.json`: 전달 ZIP에 들어가는 파일별 SHA256(매니페스트 자체 제외).

문헌 PDF·PNG는 검토 중 직접 열람했으나 이 배포 ZIP에는 복제하지 않았다. 판정문의 원문 링크를 사용한다. 제공 카드6개는 포함하되 원문 전체 재검증과 구별한다.

## 하지 않은 것

새 실침대 재압밀·S0·8팔·GPU 런, 생산 구현 수정, 배치 제출, Git checkout/fetch 변경, 원장 상태 변경, 원고 수치 교체, 전체 check_all 통과 선언. 이 ZIP의 전달은 어느 실행 승인도 대신하지 않는다.
