# ps45 σ_e 보고 기준 검토 패키지

먼저 `codex_review_ps45_sigmae_reporting_20261013.md`를 읽는다. 목적은 보고 그림의 모델/입력 기준 검토이며, 생산 변경·194·보충20·v1.3 승인이 아니다.

## 포함 내용

- 한국어 판정문: Q1–Q6, 실제 단위 환산표, 조성 분모 재계산, 원문 비교, 재사용할 각주.
- `probes/`: 합성 실제 함수 시험, 저장된 전류/기하의 출력 재구성, 덱·scaffold 조성 재계산.
- `evidence/`: 기계 판독 결과·해시·환산 CSV. CSV는 **PC 인자 ON**의 readout-only 결과다. 인자 OFF의 다섯 새 생산값으로 사용하면 안 된다.
- `source/`: 읽기 전용 고정 코드·기존 산출물·덱·AM scaffold. 원 production checkout이 아니라 리뷰용 사본.
- `notes/`: 코드, 조성, 문헌 판독의 상세 근거와 접근 한계.
- `literature_cards/`, `literature_figures/`: 핀된 탐색 카드 및 원문 그림 사본. 카드의 주장과 독립 원문 확인을 구분한다.

외부 전체 논문·학위논문 PDF 및 임시 렌더 이미지는 배포 ZIP에 넣지 않는다. 원문 URL·판독 페이지는 판정문과 메모에, 로컬 확인 파일의 SHA-256은 `evidence/literature_access_final.json`에 기록한다. 불완전한 IOP 봇 확인 HTML은 원문으로 사용하지 않았다.

## 재현

Python 3.12에서 numpy/scipy/networkx와 사본 모듈의 관련 의존성이 필요하다. 검증 환경의 정확한 버전은 `evidence/code_scaling.json` 참고. 제공된 스크립트는 이 폴더의 `source/scripts`를 사용한다. 기존 로컬 과거 리뷰 `deps` 경로가 있으면 활용하지만, 없을 때는 설치 환경의 패키지로 import한다.

상위 디렉터리에서:

```text
python -B ps45_sigmae_review_20261013/probes/code_scaling.py
python -B ps45_sigmae_review_20261013/probes/report_arithmetic.py
python -B ps45_sigmae_review_20261013/probes/composition_basis.py
python -B ps45_sigmae_review_20261013/verify_review.py
```

첫째/셋째는 JSON을 출력하며 생산 파일을 쓰지 않는다. 둘째는 검토 폴더 내 재현 산출물 JSON/CSV만 다시 쓴다. 마지막은 원 source 해시와 시험 결과를 확인하고 `evidence/final_verification.json`만 쓴다. DEM·WSL 실침대 풀이·원 데이터 덮어쓰기는 없다.

## 한계

실침대 인자-OFF 다섯 망은 미실행. 주 그림 권고는 그 결과를 얻은 뒤 적용할 보고 규약이다. Wang의 약4 mS/cm는 원 그림으로 확인했지만 정확한4.1 및 모든 제조조건은 본문 재확인 미완료. 숫자를 문헌에 맞추기 위한 선택/재적합을 허가하지 않는다.
