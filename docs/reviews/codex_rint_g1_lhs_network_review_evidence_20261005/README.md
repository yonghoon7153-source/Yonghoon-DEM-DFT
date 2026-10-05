# 검토 증거 패키지

고정 커밋: 30c8205c5efb3873ae6fa856881fa184bd041d4d
리포: yonghoon7153-source/Yonghoon-DEM-DFT
작성: 2026-10-05

먼저 codex_review_rint_g1_lhs_network_20261005.md를 읽으십시오.
판정: HOLD. G3의 새 지표·경계 추출만 한정 GO이며, 194건 실행 허가는 아닙니다.

생산 코드/기존 Git 상태/원 배포본을 바꾸지 않았습니다.
source/는 독립 취득한 읽기 전용 부분 스냅샷입니다. 모든 223파일의 Git blob 일치:
source_manifest.json. 각 파일의 SHA-256도 포함합니다.

findings_review.json은 검토용 별도 원장입니다. 원 리포 findings.json에 쓰지 않았습니다.

재현
----
본문 §5의 명령과 §6 환경 한정을 따르십시오. 합성 fixture·소형 CPU 검산만 포함하며 대형 캠페인이 아닙니다.
반례 프로브의 rc=0은 현재 결함을 성공적으로 재현했다는 뜻이지 대상 코드 GO가 아닙니다.
probe_contracts.py는 실제 helper/merge/validator/grade를 호출하고 solver의 파일 작성만 fixture로 대신합니다.
probe_actual_zero.py는 실제 소형 비관통 수치 생산 결과를 그 helper에 전달합니다.
environment_adapters.py의 두 모드는 native Git/WSL/symlink 시험의 대체 인증이 아닙니다.
실제 real14 압축 dump와 r_int 역사적 NPZ 셋은 독립 재실행하지 않았습니다.

주요 증거
---------
evidence_g1: baseline 90/49/9, 실제 payload+check-arm CG 반례, AM mask 및 Spearman.
evidence_g23: 실제 LW parser/함수 반례, power circuit, 18 raw old/new 비교, 최종 CLI 메타데이터.
evidence_g4: build_handover 입력 변이, 194행 커밋 CSV 산술 정합, 233/13 baseline.
evidence_g56: helper/게시/정지/τ 온도 짝 반례, 실제 nonpercolation integration, 원 시험 및 환경 적응판.
각 디렉터리 독립 보고서는 검토 작업 노트이며 최종 ID/심각도는 루트 판정문이 정본입니다.

패키지 무결성
-------------
package_manifest.json은 ZIP에 넣은 파일별 SHA-256입니다(자기 자신 제외).
ZIP CRC와 모든 manifest hash를 작성 후 다시 읽어 검사했습니다.
ZIP 자체 SHA-256과 크기는 ZIP 옆 package_receipt.json 및 .sha256 파일에 있습니다.
의존성 설치물, 캐시, 비밀키, .git는 넣지 않았습니다. 소스 전체 리포가 아니므로 import에 필요한 외부 패키지는 별도입니다.

