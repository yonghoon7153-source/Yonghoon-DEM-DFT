# 50kg 4차년도 DEM 계획 검토 전달본

대상 핀 표기: `6d07cf79d5b696587e37fc8f4407e9419d37b1ec`. 사용자 승인에 따라 입력 ZIP 바이트를 판정했다. 원격 Git blob 검증은 포함하지 않는다.

- 판정문: `codex_review_kg50_report_plan_20261030.md`
- 결론: 7쪽 구성 수정 후 수용. 현행 이용률·최적 입도 주장 확정 HOLD. 물리 실행·재개·배포 GO와 별개.
- `source/`: 입력 ZIP의 문서 7개와 PIN 원문. PDF/PPTX 원본은 입력 ZIP의 `input/`에 있다.
- `evidence/`: 입력 해시, 검산, 원본 텍스트 및 대조 영상.
- `MANIFEST.sha256`: 이 전달본 파일의 해시. manifest 자체는 목록에서 제외.

## 산술 반례 재현

`evidence/`에서 `python -I review_probes.py --out local_probe_result.json` 실행. 16개 checks가 true여야 한다. 이는 리뷰어의 산술·기하 반례 검산이며 생산 코드나 실제 네 침대의 통과 시험이 아니다.

## 보존 범위

시뮬레이션·WSL·ibb 실행, 저장소 코드 수정, 커밋·푸시를 하지 않았다. 실험 시료 동일성이나 현재 도구 구현을 문서 신고만으로 확인했다고 쓰지 않았다. 원본 PDF/PPTX를 수정하지 않았다.
