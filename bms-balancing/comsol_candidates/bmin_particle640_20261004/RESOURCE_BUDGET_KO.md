# B-min 단발 실행 예산 제안 — 아직 미승인

이 표는 **제안**이다. 문서 · 검토 · 이 후보로 승인된 값이 아니며, native 실행은 별도 사용자 승인 (`NATIVE_BMIN640_APPROVAL_DRAFT_KO.md` — 비활성) 뒤에만 쓴다. 근거와
시나리오는 B-min v2 §7 (`docs/COMSOL_BMIN_SCOPE_v2_20261004.md` l.162–205) 그대로이고, 여기서는 그 제안을 NORMAL480 후보의 예산 키에 옮겼다.

| 키 (CONTRACT `budgets_seconds`) | NORMAL480 | B-min 제안 | 근거 |
|---|---:|---:|---|
| `preflight_and_input` (사전 확인 · 같은 Python 의 새 두 직접 입력 · 기준 9 파일 해시) | 180 | **180** | 그대로 |
| `compile_batch` (compile + batch 공유) | 9,000 | **9,000** | v2 §7 높은 비용 가정 ≈5,916 s 의 약 1.5 배 (낮은 가정 ≈3,824 s) |
| `process_cleanup_total` (소유 Job 정리 합계) | 120 | **120** | 그대로 |
| `analysis` (부모 분석 호출) | 1,800 | **900** | v2 §7 높은 가정 ≈250 s 의 3.6 배 (NORMAL480 분석 실측 234.6 s · 이번에 읽는 프로파일 행 수는 NORMAL480 분석보다 적다 — 아래) |
| `delivery` (부모 로컬 전달) | 300 | **300** | NORMAL480 실측 4.9 s |
| **`overall` (부모 최종 기록까지)** | 11,400 | **10,500** | 위 다섯의 합 (= v2 §7 의 9,000 + 900 + 300 + 준비 · 정리 300) |

- 부모 (`PARENT_COMMAND.ps1`) 의 상수 — 전체 10,500 (`GDecision` · 시작 기록 · 예산 초과 판정 · PRE / POST_WRITE 두 관측) · 분석 900 · 전달 300 — 는
  이 표와 같다 (정적 대조 `STATIC_AUDIT.json` "budgets equal …").
- 시작 전 디스크 여유 **≥ 15 GiB** (`resource_proposal.disk_start_gib` 50 → 15 — entry 의 기존 `DISK_START` 검사가 쓴다). v2 §7: 동시 보관 추정
  ≈8.2 GiB (MPH 높은 가정 6.66 GiB · 출력 표 0.19 · 콘솔 로그 0.25 · 결과 ZIP 0.19 · NORMAL480 기준 ZIP + 기준 표 0.77 · 포장 · 전달 사본 0.19 GiB) 의 약 1.8 배.
  NORMAL480 의 50 GiB 를 자동 재사용하지 않은 새 제안이다.
- 요청 16 코어 그대로 (실제 사용률 UNVERIFIED). RAM 은 시작 관측만 — 새 RAM 문턱 · 감시기 없음 (기존 `memory_note` 그대로). 계획상 최대 메모리
  ≈2.5 GB 는 NORMAL480 1.27 GB × 자유도 배의 산술이지 측정이 아니다.
- 시도 1 회. 한도를 넘거나 실패하면 멈추고 보존한다 — 자동 재시도 · 자동 연장 · 미사용분 전용 없음. 예산 초과는 세 필드에서 `evidence_validity`
  INVALID (I-8) · `mesh_comparison` INCONCLUSIVE 다.

**분석 시간의 규모 (우리 산술 · 측정 아님):** consumer 는 후보 프로파일 (저장 ≈2,440 시각 × 241 ≈ 0.59 M 행 / 전극) 과 NORMAL480 프로파일 (5,740 × 241 =
1.38 M 행 / 전극) 을 모두 읽고 검사한다 — 합 ≈3.9 M 행. NORMAL480 분석은 자기 프로파일 (2 × 1.38 M) + NORMAL240 (저장 3,340 × 241 = 2 × 0.80 M) + B020
(파일 크기 ÷ 행당 ≈147 B ≈ 2 × 0.25 M) ≈4.9 M 행을 234.6 s 에 읽었다. 그래서 900 s 를 제안하지만 실제 시간은 실행에서만 관측된다.

**이 문서가 하지 않는 것:** 실행 환경의 RAM · 코어 · 디스크 측정 · 새 기준 해 · 성능 probe · 예산 승인.
