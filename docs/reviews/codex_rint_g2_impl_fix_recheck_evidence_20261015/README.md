# Rint G2 ①′ RIMP-01–06 독립 재확인 묶음

핀: `dcb97f1ed942f622d9189eee1a1e9432dc05a655` · 2026-10-15.

결론은 `codex_review_rint_g2_impl_fix_recheck_20261015.md`.
RIMP-01·03·04·05·06 범위 한정 닫힘, RIMP-02 부분. 새 P2 RIMPR-01(입력 부분 소비), P3 RIMPR-02(float64 overflow). 정량 채택·생산 HOLD 유지.

## 내용

- `source/`: 고정 핀 원문 851파일. `source_manifest.json`은 Git blob과 SHA256.
- `evidence/`: 이번 독립 실행 결과·명령·원본 탐침의 의도된 중단 로그.
- `evidence/join_fixtures/`: 입력 파서 반례 및 양성 대조의 정확한 파일 바이트 177개.
- `probes/`, `notes/`: 검산 프로그램과 세부 검토 메모.
- `source_prior/`: OFF 비교용 수정 전 두 모듈.
- 형제 폴더 `rint_g2_impl_review_20261014/`: 기존 탐침의 재실행에 필요한 옛 Python 소스·탐침·판정문. 이전 전체 묶음이 아니라 의존 부분집합이다.
- 제출자 로그는 `source/docs/reviews/rint_g2_impl_fix_evidence_20261015/`에 있다. 이번 독립 결과와 구분한다.
- ZIP 루트 `PACKAGE_MANIFEST.json`: 전달 파일별 SHA256·크기.

## 재현

두 상위 폴더를 나란히 푼다. Python + NumPy + SciPy 필요. 검토 실행 환경은 Python 3.12.14, NumPy 2.5.3, SciPy 1.16.3, BLAS 1 thread. 다른 수치 라이브러리에서 마지막 비트까지 일치한다고 보증하지 않는다.

`rint_g2_impl_reverify_20261015/`에서:

```text
python -B reproduce.py
python -B reproduce.py --baselines
```

첫 명령은 독립 탐침, 둘째는 요청된 296개 회귀와 자체시험까지 실행한다. 작은 CPU 검산만 실행하며 DEM·MPM 캠페인/MPI·스케줄러·Git 명령은 없다. 재실행은 별도 `evidence/replayed/` 로그를 만들지만 탐침이 생성하는 결과 JSON·임시 픽스처는 같은 이름으로 갱신된다. 원 전달 증거를 보존하려면 ZIP을 새 폴더에 풀어 재현한다.

`resource` 호환 모듈은 Windows의 보고용 최대 메모리 값만 NaN으로 대체한다. 이 어댑터를 물리 계산이나 메모리 측정 증거로 쓰지 않는다. 일부 진단 JSON의 NaN/Infinity는 의도적으로 넣은 반례/미측정 진단을 보존한 Python JSON 표기다.

원본 탐침 `owner_vox_mismatch.py`는 새 차단 ValueError 때문에 rc=1, `join_original_runner.py join_synthetic.py`는 형식 REJECT 이후 옛 키 접근 때문에 rc=1이 정상 기대다. 보완 탐침은 그 뒤 양성 대조까지 이어서 확인한다.

별도 폴더에 ZIP을 풀어 독립 탐침 8개를 다시 실행해 모두 rc=0을 확인했다 (`evidence/package_portability.json`). 처음에는 이 Python 런타임에 SciPy가 기본 설치돼 있지 않아 import가 실패했고, 외부 **제3자 라이브러리 경로만** 제공한 뒤 재현했다. 원본 검토 소스 경로는 제공하지 않았다. 최초 실패 기록도 남겼다. 최종 ZIP에는 이후의 판정문 정리와 이 재현 영수증이 추가되므로 영수증의 시험 ZIP 해시와 최종 포장 해시는 다르다.

## 범위

생산 코드·Git 상태·원장 수정 없음. 정량 채택 및 생산 허가를 내리는 묶음이 아니다. 외부 기계의 실행 파일·실행 영수증·아직 하지 않은 정식 T2/T3 검증을 인증하지 않는다.
