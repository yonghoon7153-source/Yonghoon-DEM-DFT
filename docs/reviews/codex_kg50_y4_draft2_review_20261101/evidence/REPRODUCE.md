# 독립 재검토 증거 — 50kg 초안 2 (2026-11-01)

검토 핀 065ad7004c8f970243951d366e3ced8c28af9197. 실제 DEM/수송망 solve/WSL/제출/취소 없음.
원본 repo 변경 없음. ZIP의 소스와 원격 보충 소스는 읽기용이다.

## 범위와 출처

- 원 입력 codex-kg50-report-y4-draft2-065ad7004.zip SHA256:
  0851437db6d1893ba80699718fb115b99f9bb2aff870bec3e73f1b602b6b1c30
- MANIFEST 241/241, 원격 핀 Git blob 229/229 일치.
- D1/D2/D3 도구 지문 14개가 서로 같고 원격 핀 실제 파일과 14/14 일치.
- source/repo/: 공급된 229파일. preview는 레이아웃 참고라 배포에서 생략.
- remote/: 리뷰에 필요해 같은 핀에서 가져온 보충 모듈/문서.
- physics_review/cards/: 별도 문헌 핀 c431470a1의 14개 카드. 실제 primary 접근 범위는 그 리뷰 문서에 명시.
- 외부 D1 tgz 62.7 MB는 중복 배포하지 않는다. 아래 prepare_input으로 원 입력 ZIP에서 SHA 검증 후 준비한다.
- 7445/23436은 반복 행별 산술·바이트 대조 수이며 물리 시험 수가 아니다.
- Bash 78/78은 수령 기록. 독립 Bash는 Windows 초기화 오류로 미실행.
  guard의 실패 경로 증거는 소스 결속 독립 모형이며 실제 Slurm 관측이 아니다.

## 실행

이 파일이 있는 디렉터리에서 Python 3.11+로 수행한다. numpy 필요.
그림 재생성 탐침만 matplotlib/Pillow 추가 필요. 생산 코드의 본 계산 run/add는 실행하지 않는다.

```text
python -B prepare_input.py <원_입력_ZIP의_경로>
python -B raw_probe.py
python -B physics_review/analytic_probe.py
python -B guard_review/probes/verify_guard_evidence.py
python -B guard_review/probes/model_guard_failure_paths.py
python -B figures_review/audit_figures.py
python -B figures_review/probe_figure_checker.py
```

raw_probe.py는 프로젝트 모듈을 import하지 않고 D1 atom/contact와 세 로그를 직접 읽는다.
대기 pressure의 출력용 run 0은 별도 기록하며, 유한시간 이완 끝 압력과 섞지 않는다.
그림/소비자 탐침은 원본을 바꾸지 않고 메모리 복사·임시 폴더로 변이를 만든다.
load/merge의 status=ok가 원자료 무결성을 보증하지 않는 반례가 포함돼 있다.
그림용 추가 패키지 폴더를 지정하려면 REVIEW_PYDEPS 환경변수를 쓸 수 있다.

## 기대 결과

- independent/checks.json: 7445 pass, 0 fail.
- figures_review/figure_numeric_audit.json: 23436 기계적 대조 일치; 5개 소비자 변이 수락이 결함 증거.
- guard_review/evidence/verification.json: 15개 승인값/전사 대조 일치.
- physics_review/analytic_probe.json: D3 반례 ΔP=9.25654 MPa, affine=7.666 MPa.
- 그림 재생성 baseline은 검토 PC 대체 글꼴에서 p7 하단 9.9px 넘침이 있었으며 제출 PNG 결함으로 판정하지 않았다.
- 전체 raw network/Physics/Love–Weber solve와 서버 실물 -T는 미재실행.

## 산출물

판정문은 상위 디렉터리에 별도 MD로 있으며 증거 ZIP 루트에도 포함한다.
각 상세 보고는 guard_review/Q4_guard_review_20261101.md,
physics_review/physics_registration_literature_review.md,
figures_review/figures_content_review.md다.
포장 시 두 그림 탐침의 BASE만 상대 경로로 만들고 패키지 경로는 선택적 환경변수로 바꿨다.
검사 논리는 변경하지 않았고 포장 후 다시 실행했다.
