# 재검증 4 증거 묶음

한국어 판정문: `codex_review_gen2_network_reverify4_20261007.md`.

핀 `87f0906a2674e7d4e8ec31ca98aed5b14babc293`. `source/`는 Git blob과 대조한 448개 파일의 검토 사본이며 Git checkout이 아니다. 생산 코드는 수정하지 않았다. 실제 WSL 전달물은 `submitted/`, 원 tar.gz는 `source/docs/reviews/codex_gen2_network_reverify4_precheck_20261007/`에 보존했다.

## 재현

이 디렉터리에서, NumPy/SciPy/NetworkX/Flask/Matplotlib 등 리포 시험 의존성이 있는 Python을 사용한다. 이번 환경은 Python 3.12.14, NumPy 2.5.3, SciPy 1.16.3, NetworkX 3.7이다. `run_checks.py`는 이 PC의 기존 로컬 의존성 디렉터리를 우선 사용한다. 다른 PC에서는 해당 경로를 자신의 환경에 맞추거나 일반 Python 환경에 같은 의존성을 준비한다.

```bash
python run_checks.py reread publication role release
python run_checks.py submitted_evidence scope194 case15_channels release_gate
python run_checks.py observation_cli
python verify_evidence.py
```

- **194 생산 배치, DEM/MPM, 등록 S3를 실행하는 명령이 아니다.** `case15_channels`는 보존 원덤프의 CPU 저항망 후처리다.
- `release_gate`는 상위 τ 재독해만 대역으로 두고 실제 배포 생성·검산을 부른다. 정상·변이 모두 같은 대역이다. 제품 전체 우회 또는 194 수치 정확도 시험으로 읽지 않는다.
- `observation_cli`는 과거 리뷰에서 만든 게시 합성1케이스 fixture와 이번 WSL의 로그 형식을 사용한다. 실물 WSL 194 audit를 여기서 다시 돌린 것이 아니다. `fixtures/seal_baseline/`에 그 픽스처를 동봉했다.
- `submitted_evidence`는 별도 복사본에서만 WSL 경로를 Windows 검토 경로로 번역한다. 원 전달물은 바꾸지 않으며 번역본을 실행 증서로 발행하지 않는다.
- `scope194`는 기존 감사/수확 JSON 재집계다. 이 PC에 없는 194 원덤프를 새로 읽는 시험이 아니다.
- `prepare_source.py`, `source_plan.json`, `extra_plan.json`은 취득 이력이다. 검증된 source를 이미 동봉했으므로 다른 PC에서 취득 스크립트를 먼저 실행할 필요가 없다.
- 초기 탐침 준비 중 STL 미반입·인자 순서·재실행 출력 폴더 충돌을 수정한 이력이 일부 `runs_*.json`에 남아 있다. 최종 판정은 `verification.json`이 대조하는 각 개별 최신 로그/JSON을 기준으로 한다. 이것들은 제품 결함으로 세지 않았다.

`release.log`의 133 PASS / 2 FAIL은 의도적으로 숨기지 않았다. 두 실패는 Windows 경로와 `.git` 부재이며 판정문 §1-2에 명시했다.

## 핵심 증거

- `evidence/release_gate.json`: 성공 대조·원 반례 차단·상세 결손/모순 수용. `artifact_root` 아래 실제 build 로그/출력.
- `evidence/observation_cli.json`: 실제 audit CLI 5/5 정상, 5/4 거부, 4/4·2/2 잘못된 수용.
- `evidence/submitted_evidence.json`: 전달 영수증/코드/manifest 해시 대조와 함수 수준 변이.
- `evidence/case15_channels.json`: 원덤프 직접 6조합, 경계 ID, 음수 면적 두 행, 전류보존 증서.
- `evidence/scope194.json`: 194 기존 레코드의 전수 재집계·범위 한정.
- `evidence/wsl_code_identity.json`: WSL 커밋과 리뷰 핀의 관련 Git blob 일치.
- `source_manifest.json`: 448파일의 바이트 신원.

`verification.json`은 **검토 증거의 일관성 검산**이다. 제품 전체 통과/194 실행 GO가 아니다.
