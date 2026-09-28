# LH 고-Bo 5차 리뷰 증거 (2026-09-28)

대상 핀: 091bb21143c426beecd196d6115666fdd49155b1
브랜치: claude/sdcp-dem-manuscript-si-pqwtv8
판정문: codex_review_mixer_highbo_round5_20260928.md
이 폴더는 리뷰 복사본이다. 생산 저장소/런 폴더가 아니다.

## 무결성과 내용

- sources.json: 대상 리포에서 GET으로 취득한 소스 23개와 Git blob SHA.
- source_hash_verification.json: 로컬 바이트로 Git blob SHA 및 SHA256 재계산, 23/23 일치.
- scripts/, dem_scripts/, docs/: 해당 핀 자료. **Back.stl은 원본대로 CRLF·EOF 개행 없음**. 자동 EOL 변환은 motion_signature를 바꿀 수 있다.
- external_sources.json: 직접 읽은 LIGGGHTS-PUBLIC C++ 고정 핀·SHA·링크. 난수/분할 규약의 근거이며, 빌드·실행하지 않았다.
- review_round5_probe.py / review_round5_output.json: 독립 합성 반례·대조.
- run_selftests.py / selftests_output.json: 원본 자체시험의 실제 출력. 전체 녹색이 아님을 아래에 명시한다.

## 재현

Python 3, NumPy, SciPy가 필요하다. 이 폴더에서:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 review_round5_probe.py
PYTHONDONTWRITEBYTECODE=1 python3 run_selftests.py
```

프로브는 tempfile 안에 합성 덱·입자/메시 덤프·로그·봉인을 만든다.
실제 검사 함수, 실제 start_check CLI, 실제 launch_highbo.sh의 rest Python 블록을 실행한다.
**LIGGGHTS, mpirun, sbatch 또는 생산 런처는 호출하지 않는다.**
가짜 바이너리 파일은 SHA 식별용 바이트이며 실행되지 않는다.
출력의 임시 경로와 시간은 재실행 때 바뀐다. 논리 결과와 숫자를 비교할 것.

성공 시 exit 0, assertions 16/16 true.
이것은 제품 PASS 수가 아니라 다음 반례가 그대로 재현됐음을 포함한 검증 수다.

| 출력 key | 의미 |
|---|---|
| nan_B, empty_seal_lists | 기존 무결성 결함이 닫힘 |
| different_binary, different_clock, resume_refused | 기존 실행 연결 결함이 닫힘 |
| translation_wall | +80 nm를 거리 경계로 전파해 TECH |
| static_e0, static_no_expected, static_end_overlap | 정적 E0 허용/거부 대조 |
| disabled_garbage_mesh | mesh dump를 판정 근거로 읽지 않음 |
| start_empty_dict, start_null, start_list, start_string | **빈/비객체 봉인의 시작 관문 rc0 반례** |
| smoke_normal, smoke_wrong_grid | 실제 rest gate 정상/잘못된 규약 대조 |
| smoke_after_duplicate, smoke_recomputed_duplicate | **stale 증서는 통과, 재판독은 bin0 incomplete** |
| np1_receipt_on_np20 | 실제 np1 증서를 합성 np20 봉인에 소비자가 수용 |
| gen_end_truncated | **봉인 덱 end보다 짧은 gen/log를 완주로 승인** |
| position_uncertainty_pct_points | 실제 거리 경계를 상별 반경으로 환산 |
| current_e0_decks | 현 생성기 E0 revolutions=0의 bytes·SHA256 |
| receipt_rows_comparison | v1/v2 선택된 208행 수치 일치, v2 파일 SHA |
| confounding_example | Bo 효과 0이어도 환경 차이로 판정선을 넘는 구성적 예 |

## 환경과 한계

Windows / Python 3.12.14 / NumPy 2.5.3 / SciPy 1.18.1.
Python 실행 파일:
C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe

NumPy/SciPy는 기존 audit_review_evidence_20260909/pydeps를 PYTHONPATH에 지정했다.
코드에는 이 환경 경로를 하드코딩하지 않았다. 다른 환경에서는 자체 설치본을 사용하면 된다.

자체시험: measure_bed_aspect 25/25, check_contact_validity 83/83,
measure_mixing_index 34/34 (실제 덱 옵션 시험 SKIP),
mixer_deck_diff 24/24, make_mixer_deck 89/89.
mixer_restart_phase_test는 26개 PASS 후 새 run.sh 시험에서
subprocess의 bash 실행 파일 미발견(WinError 2)으로 종료 1.
따라서 run_selftests.py 전체도 exit 1이다. 이를 28/28 통과라고 쓰지 않았다.
test_launcher.sh 81건 및 check_all.sh 전수는 실행하지 않았다.
Portable Bash로 launch_highbo.sh 구문 검사는 통과했다.
실제 rest 게이트와 시작 대조 CLI는 Bash 없이 독립 실행했다.

실 LC/LH/E0 덤프와 영수증 원 mesh/log는 제공되지 않았다.
실 캠페인의 최대 겹침, M, 대표성 QC 또는 MPI20 물리 차이 크기를 이 합성 자료로 추정하면 안 된다.

