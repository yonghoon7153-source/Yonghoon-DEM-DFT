# 반입 — Codex 50kg 4차년도 DEM 7쪽 계획 검토 (10-30 · 수정 후 수용 · 이용률 · 최적 입도 HOLD)

- 받은 것: 1저자 10-30 업로드 `codex_kg50_report_plan_review_6d07cf79_20261030.zip` (4,029,072 B · sha256 `46b9352e9a6ff12eda55c2eedee6c5e756938e2e56c4d7552b760e141a08a611` · 항목 32 · 중복 0 · 대소문자 중복 0 · 경로 이탈 · 링크 0).
- 대상: 리뷰 핀 `6d07cf79d5b696587e37fc8f4407e9419d37b1ec` 의 요청서 2판 (`docs/50kg/codex_kg50_report_plan_request_20261030.md`) — Codex 는 1저자 승인대로 **보낸 ZIP 바이트** 를 판정했다 (원격 blob 대조는 안 함 · 그때 핀은 아직 push 전).
- 이 폴더에 푼 것: 판정문 `codex_review_kg50_report_plan_20261030.md` · Codex `README.md` · `MANIFEST.sha256` · `source/PIN.txt` · `evidence/` 의 `intake.json` · `verification.json` · `review_probes.py` · `review_probes.json` · `review_probe_run.log`.
- **리포에 넣지 않은 것** (받은 ZIP 안에만): `evidence/extracted/` 3 (이종기술 2차년도 PDF · 50kg 계획 PPTX 의 본문 텍스트) · `evidence/renders/` 13 (PDF p13–20 · PPTX 4–8 장 영상) · `source/repo/` 7 (= 리뷰 핀 `6d07cf79d` git blob 과 7/7 같음 · 메인 대조) · **받은 ZIP 자체** (앞의 두 묶음을 담고 있어서 — 1저자 10-30 Q2 *"두 원본 = Codex 묶음에만 · 리포 밖"* 과 같은 이유).  받은 ZIP 원본 = 1저자 PC (Codex outputs 폴더) · 위 sha256.
- 개행: 이 폴더의 Codex 파일 6 개 (`README.md` · `MANIFEST.sha256` · `evidence/*.json` · `evidence/review_probe_run.log`) 는 커밋 때 CRLF → LF 로 정규화된다 (git 속성 `eol=lf`) — `MANIFEST.sha256` 은 받은 ZIP 안 원본 바이트 기준이라 그 6 개는 여기서 해시가 다르다.

## 대조 (메인 · 이 컨테이너)

| 무엇 | 결과 |
|---|---|
| `MANIFEST.sha256` (받은 ZIP 안 원본 바이트) | 31 항목 · 다름 0 |
| `evidence/intake.json` 의 입력 ZIP | sha256 `893fd525…` · 15,503,366 B = 우리가 보낸 요청 ZIP |
| `source/repo/` 7 파일 | 리뷰 핀 `6d07cf79d` git blob 과 7/7 바이트 같음 |

## 판정 (요지 · 원문 = 판정문)

- **7쪽 구성 = 수정 후 수용 · 현행 *"SE 이용률 · 활성 AM"* 해석과 *"실측 결합 최적 입도"* 결론 = HOLD** · 물리 실행 · 재개 · 배포 GO 아님 (검토 대상 아님).
- P1 둘 · P2 넷 · 원장 ID = `KG50B-01`–`06` (Codex 표기 KG50P-01–06 — 원장에 Q5 dt · 감쇠 리뷰의 `KG50P-01`–`10` 이 이미 있어 접두를 바꿈 · B = 보고).

| 원장 | Codex | 등급 | 요지 |
|---|---|---|---|
| `KG50B-01` | KG50P-01 | P1 | 선형 이온 망의 전류 · 접촉률 ≠ SE/AM 전기화학 이용률 · 후막 반응 분포 |
| `KG50B-02` | KG50P-02 | P1 | 망 효율 f × 펠릿 σ = 조건부 시나리오 · 2 µm 보간으로 최적 입도 식별 불가 |
| `KG50B-03` | KG50P-03 | P2 | f 와 수송 tortuosity 는 대수적으로 한 묶음 · φ 분모 규약 |
| `KG50B-04` | KG50P-04 | P2 | 시드 1 · D3 영역 선택 결과의 적용 범위 · 결과 일부 열람 뒤 분석 계획 |
| `KG50B-05` | KG50P-05 | P2 | 껍질 분율 · 구면 지도 · 합집합 · 대표 입자 정의를 계산 전에 고정 |
| `KG50B-06` | KG50P-06 | P2 | *"모델 · 물성 = 이종기술과 같음"* ↔ 첨부 표 (SE 22 GPa) 불일치 · 옛 기전 서술 |

## 우리 트리 재현 (`_repro_ours_20261030/` · Python 3.11.15 · numpy · 새 빈 폴더 · 스크립트 = 경로 인자)

| 무엇 | 결과 | 파일 |
|---|---|---|
| Codex `review_probes.py` (`python3 -I`) | rc 0 · checks 16/16 · Codex JSON 과 다른 칸 1 (`node_weight.after_gini` 끝자리 2.8e−17 · 합 순서) | `local_probe_result.json` · `review_probes_stdout.txt` |
| 우리 독립 재계산 `independent_recompute.py` — Codex 가 상수로 적은 답을 노드 해석 · 식으로 다시 | checks 13/13 · 직렬망 전류 · 병목 전력 몫 0.98 · Gini 0 / 0.3 → 0.2077 · 손익분기 2.217 · 2.267 · 1.022 · 2 µm 최댓값 뒤집힘 · 구면 캡 / 원판 1.25 · 삼중 겹침 합집합 · 고정 계면 4/3 · 조성 φ 0.34292 · 전극 기준 0.27793 (D3 반올림값 0.27798) · 고체 기준 φ 를 쓴 수송 tortuosity 16.62 | `independent_recompute.json` · `independent_recompute_stdout.txt` · `independent_recompute.py` |
| + 무작위 3D 저항망 (노드 400 · 간선 1,463 · 아래 · 위 Dirichlet) | z 단면 9 곳의 부호 있는 순 전류 = 단자 전류 (최대 상대 차 7.2 × 10⁻¹⁵) · 단면 Σ\|I\| / I = 1.00–1.12 · z 사분위 소산 몫 0.197 · 0.314 · 0.263 · 0.226 — **두께 방향 "순 이온 전류" 는 구조상 평평** (판정문 KG50P-01 두께 방향 제약) | 같은 JSON `random_3d_network` |
| + 우리 웹앱 전류 몫 사다리 (`scripts/network_current.py` = 상위 \|I\| 접촉의 32 높이 단면 평균 순 흐름 / 단자 전류) 를 10 간선 직렬망에 | 8 간선 = 몫 0.8125 · 고른 간선이 두 단자를 잇지 않음 — 우리 정의 (단면 평균 몫 · Σ\|I\| 비율은 아님) 도 **경로 보존은 아니다** | 같은 JSON `repo_share_ladder_chain` |

- 한정: 산술 · 합성 망 · 우리 정의의 합성 대조뿐 — DEM · 네 침대 · 생산 함수 재계산이 아니다 (Codex 와 같은 범위 + 우리 사다리 정의 한 건).
- 수정 계획 = `docs/50kg/kg50_report_plan_fix_plan_20261030.md` (⬜ 1저자 비준).
