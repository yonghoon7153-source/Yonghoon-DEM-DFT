# 재검증 7 증거 반입 (10-12) · 우리 트리 재현

정본 판정 = `docs/reviews/codex_review_gen2_network_reverify7_20261012.md` (리뷰 핀 `3cedd40a5` · 수정 `ec9c51149` · 부모 `821f0e151` · **G2RR6-01 닫힘 · G2RR5-03 S0b 잔여 닫힘 · 새 P1 · P2 없음 · GO = G2RR6-01 기술 차단 해제 + 기존 194 발사 승인 · 사전 점검 단계 진입** — 실제 발사 · 완료 · 인계 · 보충 20 / 214 배포 GO 아님 · 비차단 P3 `G2RR7-01`).
Codex 묶음 설명 = 이 폴더 `README_REVIEW.md` (묶음의 `README.md` 를 이름만 바꿨다).

## 1. 받은 것 · 넣은 것

| 묶음 | 크기 · 파일 | sha256 | 리포 |
|---|---|---|---|
| 원 ZIP (1저자 PC · Codex 작업 공간) | 44,096,160 B · 838 파일 | `a90d12b1c0346e7788efb2e7b231de70718ab644c75ff7fa14212c251bebd319` (`ORIGINAL_ZIP_SHA256.txt`) | 넣지 않음 |
| slim ZIP `codex_gen2_network_reverify7_20261012_slim.zip` (1저자 WSL 에서 줄임 · 10-12 첨부) | 1,086,564 B · 233 항목 (위험 경로 · 링크 없음) | `0052d36e4b4a7de4e35e18f637732e2753f86cd73d412519aa43122b95e90998` | 아래 표만 |

- 묶음 sha256 표 (`MANIFEST.sha256.json` · 837 행 · 자기 제외) 대조 = slim 에 남은 **229 / 229 같음** · 뺀 **608** 은 `SLIM_EXCLUDED.tsv` (경로 · 크기 · sha256) 에 있고 그 sha256 = 표와 같음 · 표에 있는데 남지도 빠지지도 않은 것 0.
- 판정문 = 묶음 맨 위 사본 = 묶음 폴더 안 사본 (바이트 같음).  윈도 경로 (`C:\Users\Administrator\…`) = Codex 작업 공간 경로 그대로 (비밀 아님) · 메일 주소 · 토큰 · IP 없음 (검색).

| 무엇 | 반입 | 빠진 것 (복원 방법) |
|---|---|---|
| 판정문 | `docs/reviews/codex_review_gen2_network_reverify7_20261012.md` | — |
| 묶음 README · `MANIFEST.sha256.json` · `run_checks.py` · `package_review.py` · `prepare_source.py` · `source_manifest.json` · `ORIGINAL_ZIP_SHA256.txt` · `SLIM_EXCLUDED.tsv` | 전부 | — |
| `evidence/` 203 파일 | 199 (결과 JSON · 로그 · CLI 입력 / 결과 · diff 둘) | GitHub API 응답 넷 (`commit_3cedd40a5….json` sha256 `01059e13…` · `commit_821f0e151.json` `d0796cc9…` · `commit_ec9c51149.json` `dedf3e8d…` · `compare_r6_r7.json` `97d29821…` · 합 1,645,131 B) = `git show` · `git diff a20fc1875 3cedd40a5` 로 다시 만든다 |
| `notes/` 셋 · `probes/` 여섯 | 전부 | — |
| `source/` 573 (slim 에서도 뺌) | — | 핀 `3cedd40a5` 의 리포 파일 — **우리 git 의 blob SHA-1 · SHA-256 · 크기 = `source_manifest.json` 573 / 573 같음** |
| `parent/scripts/` 2 | — | 부모 `821f0e151` 의 git blob 과 바이트 같음 |
| `baseline_r6/` (evidence 일곱 · source_manifest · source 34) | — | 10-11 반입 `docs/reviews/codex_gen2_network_reverify6_evidence_20261011/` 의 같은 파일과 바이트 같음 (source 34 = R6 핀 blob · slim 에서 뺌) |
| `submitted/request.md` | — | 리포 `docs/reviews/codex_gen2_network_reverify7_request_20261011.md` 의 핀 판과 바이트 같음 (sha256 `da1b7e63…`) |
| `tree.json` | — | 핀의 GitHub tree 응답 (slim 에서 뺌) — `git ls-tree -r 3cedd40a5` |

## 2. 우리 트리 재현 (10-12 · HEAD `23a8fa48f` · 리뷰 핀 이후 바뀐 것 = 문서뿐 (`scripts/` · `webapp/` 변경 0) · 컨테이너 Linux · Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1)

| 구동기 (`_repro_ours_20261012/`) | 무엇을 | 결과 |
|---|---|---|
| `rebuild_bundle.py` | 반입 폴더 + git 으로 Codex 묶음을 다시 세움 (source 573 · parent 2 · baseline_r6 · 요청서) | 573 / 573 blob · sha256 대조 통과 |
| Codex `run_checks.py` 무변경 (`reread r7_cli` → `r7_parent_cli` → `r7_predicates test_quality_probe` → `r7_final_qa`) | 다시 세운 묶음에서 | **전부 rc 0** · 다시 읽기 자체시험 **26 / 26** · `r7_final_qa` 의 단언 (실제 CLI 23 기대대로 · 전후 변이 25 기대대로 · 소스 무변경) 통과 |
| `compare_probe_outputs.py` → `compare_probe_outputs.json` | 우리 출력 113 JSON ↔ Codex 증거 | **판정값 차이 0** · 환경 차이만 = run id 450 · 경로 234 · 부동소수 끝자리 600 (상대 ≤ 1e-12 · 합성 게시의 CG 수치) · NaN = NaN 1 · 런타임 / 패키지 판 11 |
| `r7_contract_ours.py` → `r7_contract_ours.json` (Codex `r7_contract.py` = 윈도 `\\?\` 경로 전용이라 그대로 못 돈다 → 같은 질문을 git 에서) | 봉인 32 · 인계 도구 · case15 원자료 · 음수 면적 · 수정 범위 · 반입 입력 | **전부 Codex 와 같음** — code_fp `e8b2496b…` · R6 대비 봉인 변경 0 · `g2_network_reread.py` sha256 `248ee5c0…` (R6 `71945dab…`) · 원자료 네 파일 전체 sha256 · 풀린 바이트 = 등록 = README · 접촉 182,995 행 Decimal → 음수 `[31, 29241, −0.186036, 1.05114]` · `[38, 29241, −0.186264, 1.0512]` · 다시 읽기 +161 / −8 · 스모크 +2 / −0 · chk(…) AST 같음 |

- 재현 명령: `python3 -I -B docs/reviews/codex_gen2_network_reverify7_evidence_20261012/_repro_ours_20261012/rebuild_bundle.py <리포> <새 빈 폴더>` → 그 폴더에서 위 Codex 명령 넷 → `compare_probe_outputs.py <폴더>/evidence <원 묶음 evidence> out.json` (원 묶음 evidence = 이 폴더 `evidence/` + 빠진 API 응답 넷은 대조 대상 아님) · `r7_contract_ours.py <리포> <폴더>/baseline_r6/evidence docs/reviews/codex_gen2_network_reverify7_evidence_20261012/evidence/r7_contract.json out.json`.
- 한정: 반례 · 계약 재현이다 — 194 생산 · S3 · DEM/MPM · WSL 스모크 real 이 아니다.  스모크 fast 는 Codex 쪽에서 윈도 `os.wait4` 부재로 완주 못 했다 (판정문 §6) — 발사 핀의 fast16 + real4 는 사전 점검에서 다시 돈다 (이 반입으로 면제 아님).

## 3. 판정문이 정한 한정 (원장 `verified_scope` 와 같은 문장)

- S0b 원자료 검사 = **12 자리 접두 상세** 검증 — S0b 가 원파일을 다시 읽어 64 자리를 계산한다는 뜻 아님 (Codex 의 전체 해시 대조는 이 리뷰의 별도 확인).
- *"τ 칸 어디든 숫자 거부"* = **현행 평면 τ 의 최상위 숫자 칸** — 중첩 dict · 리스트 안 숫자는 못 본다 (현행 생산 경로에서 누설 · 과잉차단 반례 없음 · 중첩 스키마를 들이면 별도 형태 계약).
- 엄격 표시값 일치 = **이 고정 case15 fixture** 한정 — 다른 침대 · 재생성 fixture · 새 표시 정밀도 = 등록 + 양성 증거 함께 개정.
- 인계 도구 지문은 바뀌었다 (`248ee5c0…`) — 봉인 32 지문 불변과 섞지 않는다 · 옛 실행 로그를 새 도구의 증거로 옮기지 않는다.

## 4. 남은 것 (판정문 §5 — 새 조건 없음)

1. 1저자 발사 승인 (별도) · 2. 발사 핀에서 fast16 + real4 · rc · 환경 · 전후 지문 · 3. 깨끗한 트리 · 새 ROOT · 32 지문 · 기대 g2 · 입력 지문 · `--observe-imports` ON · 4. 완료 뒤 194 전수 관문 (최종 ID 전부 SEALED · 단계 결합 expected = observed · audit · `--expect-set production194` 재독해 · 인계 · 배포 검사).
- 보충 20 · 214 결합 = 이번 판정 밖 — 지원 코드를 합친 뒤 다른 핀으로 발사하면 이 판정을 그 diff 까지 승인한 것으로 쓰지 않는다 (1저자 10-12 = 보충 지원 구현 + 짧은 Codex 검토 먼저 → 두 배치 같은 날 연달아 발사 → v1.3 한 번에).
