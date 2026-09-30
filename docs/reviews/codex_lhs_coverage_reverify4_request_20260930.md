# Codex 재검증 4 요청 — LHS 피복률 · LHSC-03-R4 · LHSC-04-R4-PIN · R4-DOMAIN 수정 (2026-09-30 밤)

> 대상 판정: `docs/reviews/codex_lhs_coverage_reverify3_verdict_20260930.md` (HOLD 유지 · 새 P1 없음 · P2 둘 + P3 하나).  수정은 1저자 비준 (*"다 비준"*) 뒤 · 반례를
> 셀프테스트로 먼저 옮겨 옛 코드에서 실패 확인.  실제 병합 · 재수확 · DEM 은 하지 않았다.

## §0 핀 (전부 실제 계산 값 — `codex_lhs_coverage_reverify4_request_20260930/source_manifest.json`)

| 항목 | 값 |
|---|---|
| 적용 기준 | `220b1426ea39eae13f077e9f0585388f3eb61d08` = 재검증 3 의 tip (Codex 후보 10 파일과 LF 정규화 뒤 동일) |
| 패치 | `0016-LHS-item-2-pin-False-Codex-LHSC-04-R4-PIN-R4-DOMAIN.patch` (커밋 `19c573856`) → `0017-run_pipeline-coverage-v2-Codex-LHSC-03-R4.patch` (커밋 `9ab4bc320`) |
| 결과 tip | `9ab4bc3203e6…` (로컬 검토 브랜치 · 인증 대상 = 패치 바이트 · 적용 후 파일 sha) |
| 셀프테스트 | `selftests_9ab4bc320.log` — lens · plastic · coverage · 수확기 **165** (옛 160 + ㉑⁗ 5) · 파이프라인 **214** (옛 212 + T11q · r) · 배치 — rc 전부 0 |

## §1 LHSC-04-R4-PIN (패치 0016)

- `producer_pin()` 이 세 층을 나눈다: ① **자기 신고** `claim_present` (schema · source_file · 64 hex · host · date YYYY-MM-DD · build · formula_confirmed 가 다 있어야) ② **로컬 대조** `source_hash_verified_locally` (이 기계에 있는 `hosts[].path` · 절대 `source_file` 을 다시 해시 — 전부 일치 True · 불일치 False · 로컬에 없음 None) ③ **설치 빌드 인증** `installed_build_pinned` = **늘 False** + 사유 (실행파일 sha · 실제 컴파일 명령 · 그 실행파일로 dump 를 만든 실행 영수증을 받는 경로가 없다 → "공개 식 가정하의 진단").
- `contact_area_check.producer_model` 필드 이름 = `source_claim_present` · `source_claim` · `source_hash_verified_locally` · `installed_build_pinned` (False) · `installed_build_reason`.
- 09-30 의 `docs/data/liggghts_add_pair_pin.json` 은 ① 수준 (1저자 셸 출력 + 공개 사본 대조) — `status_note` 에 명시.

## §2 LHSC-04-R4-DOMAIN (P3 · 패치 0016)

- 지원 수치영역 `PRODUCER_DOMAIN` = 네 인수 곱 1e-280–1e280 · d_min 1e-140–1e140 — 밖이면 E = ∞ (미인증).  오차 모델 문장에 정상 binary64 · round-to-nearest · 구형 경로 · 분모의 1/(1−γ₅) 팽창을 13·eps 가 1 차로 덮는다는 설명 · `n_tested` 는 "이 산술 모델로 비교한 인증 · 비음수 행 — 정밀 비교 통과 · 설치 빌드 인증과 동의어가 아니다" 를 적었다.

## §3 LHSC-03-R4 (패치 0017 · `webapp/app.py`)

불변식 넷 (Codex 최소 해제 그대로 · 재계산이 아니라 장부 구조): ① `n_cap = binding[tabor] + [volume] + [geom]` ② population std ≤ 50 %p (+ 반올림 0.0005) ③ AM–SE **결속** 0 → 피복률 평균 · std · 클립 0 (총 면적 반올림으로 역추론하지 않는다) ④ `mean_AM ≥ 100·n_clip/n_am` − 0.0005 (n_clip = n_am 이면 100 · n_am 0 분기 따로).  상별 단순 평균 비교는 하지 않는다.  옛 가짜 건전 레코드 (cap 1 인데 결속 전부 elastic) 는 이 불변식이 잡아 정정했다.

## §4 Codex 재검증 3 스크립트를 고친 트리에 무변경 실행 (`fixed_tree_reproduction/`)

| 스크립트 | 재검증 3 | 지금 |
|---|---|---|
| `audit_r4.py` pin | 가짜 둘 → installed True | **claim_present False · installed False** (둘 다 host/date/build · 날짜 결손) · 기본 (파일 없음) False |
| `audit_r4.py` 장부 4 | True · done | **False · failed 4** |
| `audit_schema.py` | 양성 8 · 옛 변이 거부 | 양성 **8/8** · 옛 10/10 거부 (그대로) |
| `audit_producer.py` | 동심 미인증 · 음수 따로 | 같음 · `installed_build_pinned` False |
| `audit_numeric_domain.py` | 1e-100: \|오차\| > E | E = ∞ (미인증) |

## §5 질문

1. R4-PIN: 세 층 분리 (자기 신고 · 로컬 재해시 · 설치 빌드 인증 늘 False) 가 "없는 인증을 True 라 부르지 않기" 를 채우는가.  `claim_present` 에 날짜 형식 · host · build 필수를 둔 것이 적절한가.
2. R4-DOMAIN: 곱 · d_min 정상 범위 검사로 충분한가 (다른 언더플로 / 넘침 경로가 있는가).
3. R4 불변식 넷에 빠진 공존 조건이 있는가 (예: 상별 개수 없이 가능한 것).
4. GO 이면 병합 순서 0001 → … → 0017 → 게이트 → 트리 해시 고정 → 새 디렉터리 재수확 — 동의하는가.

## §6 한정

- 합성 CPU 시험 · DEM · 실 130/64 · 설치 엔진 실행 없음.  설치 빌드 인증은 여전히 없다 (False — 결과는 공개 식 가정하의 진단).
- 03 · 04 status 는 open (claimed_fixed 는 GO · 병합 뒤).
