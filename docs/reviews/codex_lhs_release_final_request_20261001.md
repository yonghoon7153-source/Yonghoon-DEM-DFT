# Codex 최종 리뷰 요청 — LHS 구조 디스크립터 **배포 v1.1** (ML 인계 전 마지막 점검)

> 작성 2026-10-01 · 브랜치 `claude/stoic-knuth-NObVQ` · 데이터 · 배포 커밋 **`c981d77f0`** · 원장 · 이 요청서 커밋 = 그 바로 다음 커밋 (이 문서가 있는 커밋을 본다)
> 목적 = 수영 님 ML 용 배포 표 `docs/data/lhs_release_20261001_v11/` (130 × 89 · 64 × 88) 를 **학습에 쓰기 전에** 마지막으로 적대 검토한다.
> 판정 = **묶음별 GO / HOLD** — P1 만 배포를 막고 P2 · P3 는 원장에 기록한다.
> 판단 기록 = `docs/reviews/lhs_handover_judgments_20260924.md` (J17 – J20-q) · 정본 인계표 = `docs/data/{lhs,lhsx}_handover_20261001.csv` (+ `_columns.tsv`) ·
> 결함 원장 = `docs/reviews/findings.json` · 작업 체크리스트 = `docs/lhs_handover_checklist_20260929.md`
>
> ⚠ **범위 밖**: 설계 130 · 64 점 재심 · 시뮬레이션 재실행 · 망 해석 단계 (σ · τ_Laplace) · 소성 보정 피복률 (physics v1 · v2 — 인계 제외, J20-m) ·
> 새 디스크립터 후보 (σ_VM · F1 근접쌍 · Auerbach 힘 · 접촉 면적 합 · 겹침 — **별도 요청서**) · 웹앱 화면 (배포 열은 웹앱 τ · ε_union · 평판 높이 함수를 쓰지 않는다).

---

## 0. 이 라인의 Codex 이력과 원장

| 날짜 | 대상 | 판정 | 원장 (이 요청 시점) |
|---|---|---|---|
| 09-13 | 디스크립터 추출 경로 (웹앱 출력 → 일곱 열) | HOLD | `DESC-01` ~ `09` — §2-A |
| 09-24 | 두께 · porosity · φ · 인계 계약 | HOLD | `HND-01` ~ `06` — §2-A |
| 09-30 | 피복률 (수확기 item 1–4 · 웹앱 physics v2) | 첫 판 HOLD → 재검증 5 차 **GO** | `LHSC-01` ~ `06` verified · `07` ~ `11` P3 open |

⚠ 배포 v1 (10-01, `8b84ba476`) 은 위 두 HOLD 의 14 건이 **원장에 open 인 채로** 나갔다.  우리 대조 (§2-A) 로 상태를 갱신했지만 **Codex 재확인이 없다** —
그대로 믿지 말고 반례로 확인해 달라.  대조 중에 우리 자신의 배포 결함 하나를 찾았다 (`REL-01` — v1 이 적격성 표지를 버렸다 · v1.1 에서 정정).

## 1. 배포물 v1.1 (`docs/data/lhs_release_20261001_v11/`)

| 파일 | 행 × 열 | v1 대비 |
|---|---|---|
| `lhs_release_20261001_v11.csv` · `_columns.tsv` | 130 × 89 | v1 74 열 (값 · 순서 그대로) + 15 열 |
| `lhsx_release_20261001_v11.csv` · `_columns.tsv` | 64 × 88 | v1 73 열 + 같은 15 열 |
| `README.md` | — | §0 변경표 · §3 규약 8 개 (상수 열 · 적격성 표지 · 다른 코퍼스) · §4 두 두께 · 두 "고립" · §7 AI 프롬프트 |

추가 15 열 = 이온 경로 고립 9 (`am_ionic_isolated_pct` · `ionic_dead_pct` · `ionic_no_se_pct` · `{AM_P,AM_S}_ionic_{active,dead,no_se}_pct`) ·
SE 덩어리 2 (`se_largest_comp_frac` · `se_largest_comp_wall_span_frac`) · `thickness_wall_gap_um` · 적격성 3 (`physical_target_status` · `hold_reason_codes` · `boundary_state`).

- 배포 = 정본 인계표의 **열 부분집합** — `scripts/lhs_release_build.py --check` 가 행 · 순서 · 값 · 열 사전을 대조한다 (v1 도 바이트 재현).
- 원천 (전부 커밋됨): 수확 JSON `docs/data/{lhs,lhsx}_descriptors_cov_1e09f661d/` · 웹앱 접촉 단계 `docs/data/{lhs,lhsx}_webapp_contact_d1ec42fba/` ·
  정확 union `docs/data/lhs_union_20260927/` · 퍼콜 감사 `docs/data/lhs_perc_audit_20261001/` (130 · 64 CLEAN).
- 접촉 단계 원천 교체 (5번 `1e09f661d` → `d1ec42fba`) 의 공통 열 차이는 셋뿐 (F1 · φ 13 건 · 접촉 0 쌍) — J20-q.  인계표 옛 칸 변경 0.
- ⚠ 원시 LIGGGHTS 덤프는 리포에 없다 (수확 JSON 에 sha256 만).  덤프가 있어야 답할 수 있는 질문은 판정에 그 한계를 적어 달라.
- ⚠ 원천 두 묶음 (`d1ec42fba` 접촉 단계 · 퍼콜 감사) 의 출처 표지가 dirty 다 — 작업 트리 추적 파일 변경 · 사유 확인 중 (`LHS-27` 요약 CSV 유력).

## 2. 묶음별 — 생산 경로 · 우리 검사 · Codex 이력

| 묶음 | 열 | 생산 경로 | 우리 검사 | Codex |
|---|---|---|---|---|
| 설계 · 측정 입자 수 | 20 | 설계 CSV · lhsx 어댑터 (`scripts/lhsx_design_adapter.py`) · 수확 `phase_counts` | 어댑터 시험 · 설계 ↔ 덱 ↔ 수확 모양 대조 | 없음 |
| 두께 둘 · porosity union · φ (라) | 7 | 수확기 (`lhs_descriptor_harvest.py`) · 정확 union MC · 질량 보존 두께 | 항등식 ε/100 + φ_SE + φ_AM = 1 (1e-9) | 09-24 HOLD → HND (§2-A) · **질량 보존 두께는 미검토** |
| 피복률 (기하 면적) | 3 | 웹앱 접촉 단계 c_cpl[22] | J20-m (기하만) | **GO** (LHSC) — 문구만 |
| 접촉 개수 · CN | 12 | 웹앱 접촉 단계 (`dem_analysis_core.py`) · 배치 관문 (`lhs_webapp_batch.py`) | 접촉 감사 v2 (`lhs_contact_audit.py`) · 항등식 | 없음 |
| AM–SE CN · 고립 위험 (7c) | 16 | 같음 | 관문 G1–G7 (`lhs_design_dataset.py`) | 없음 |
| 퍼콜레이션 · 벽 τ · 벽 접촉 | 17 | 웹앱 `calc_percolation` · 수확기 벽 τ (Dijkstra) · 벽 기록 | 관문 P1–P3 · T1–T3 · 퍼콜 감사 130 + 64 | 09-13 HOLD → DESC-02 · 04 (§2-A) |
| 이온 경로 고립 · SE 덩어리 (v1.1) | 11 | 웹앱 `calc_ionic_active_am` (+ 상별) · 수확 v3 `tau_detail.band_detail` | 관문 D1–D5 · C1–C3 · analyze_contacts ⑬–⑱ | 없음 |
| 적격성 표지 (v1.1) | 3 | 수확기 wall_record (`boundary_state` · HOLD 사유) | 수확기 selftest ⑮ | 09-24 HND-03 · 04 |
| 생성기 · 배포 빌더 · README · AI 프롬프트 · 열 사전 | — | `lhs_design_dataset.py --export-handover` · `lhs_release_build.py` | 게이트 (`scripts/check_all.sh`) | 없음 |

### 2-A. 원장 대조 (우리 판단 — 확인 대상)

| id | 심각도 | Codex 가 말한 결함 (한 줄) | 우리 판정 | 원장 (이 요청 시점) | 근거 | 남은 것 |
|---|---|---|---|---|---|---|
| `DESC-01` | P1 | τ 계산 실패가 φ 까지 삼킨다 | FIXED | claimed_fixed | `f3cb141ae` · 배포 φ 는 수확기 값 | — |
| `DESC-02` | P1 | τ 가 관통을 보증하지 않고 결측이 미퍼콜을 뜻하지 않는다 | 배포 경로 FIXED | claimed_fixed (범위) + `DESC-02W` open | `716850ced` · `5f3836afc` · `6870a85a5` · 관문 T1–T3 | 웹앱 `calc_tortuosity` 가 반례 둘 재현 |
| `DESC-03` | P1 | physics 피복률이 확대 DEM 길이와 미확대 5 nm 를 섞는다 | MOOT (인계 · 배포 제외) | open | J20-m · `06e8c01e2` | 코드 그대로 (`DESC-10` 순서 제약) |
| `DESC-04` | P2 | τ 이름이 통계량 · 경계 · 절단을 정하지 않는다 | 배포 경로 FIXED | claimed_fixed (범위) + `DESC-04W` open | `5f3836afc` · `6870a85a5` · `a5e181384` · 절단 0/194 | 웹앱 3 키 · `LHS-17` 띠 폴백 |
| `DESC-05` | P2 | 0 · N/A · invalid 가 한 값으로 접힌다 | 배포 경로 FIXED | claimed_fixed (범위) | `716850ced` · `514691646` · `06b24cdd0` | 웹앱 `calc_coverage:288` 분모 붕괴 → 0 |
| `DESC-06` | P2 | 덤프를 읽었다고 같은 최종 프레임이 아니다 | PARTIAL | open | 배치 관문 (timestep · 같은 step 메시 · sha · 한 프레임) | **목표 압력 도달 검사 없음** · 웹앱 파서 프레임 섞임 |
| `DESC-07` | P2 | 정의 종속 열을 독립 회귀로 세면 안 된다 | 생산자 측 FIXED | claimed_fixed (범위) | 항등식 관문 · README §3 (`c981d77f0` 문구 정정) | 다운스트림 사용 |
| `DESC-08` | P2 | 291 코퍼스와 그대로 합치면 안 된다 | OPEN | open | README §3-8 경고 (`c981d77f0`) | 291 로더가 d_am 0 인 40 행을 받는다 |
| `DESC-09` | P2 | 미실행 8 개 · 고정 상자 규약 | FIXED | claimed_fixed | 130/130 · README 상수 열 표기 (`c981d77f0`) | — |
| `HND-01` | P1 | pushback 을 단단한 바닥 보정으로 해석 | FIXED | claimed_fixed | `af528e24d` · J18 철회 · 배포는 (가)(나)(다) 를 싣지 않음 | 질량 보존 두께 미검토 (Q4) |
| `HND-02` | P2 | `check_deck_floor` 가 unfix · 재정의 · 부분 group 벽 통과 | FIXED | claimed_fixed | `af528e24d` · 수확기 ⑮ | 정적 판독 한계 |
| `HND-03` | P1 | 1.98r 9 건 = 점착–중력 평형 후보 | PARTIAL | open | 경계 상태 · HOLD 를 배포 v1.1 에 실음 | 기전은 조건부 확인 |
| `HND-04` | P1 | 생성기가 벽 진단 · 적격성을 버린다 | 생성기 FIXED · 배포에서 재발 | claimed_fixed (생성기) + `REL-01` claimed_fixed | `af528e24d` · `c981d77f0` (배포 v1.1 + 빌더) | — |
| `HND-05` | P2 | ε_union 이 쌍 렌즈만 뺀다 | 배포 FIXED | claimed_fixed (범위) | `42e3ca460` · `90c6c9670` (정확 union) | 웹앱 `calc_porosity_dual` (`SELF-72`) |
| `HND-06` | P2 | `plate_z_from_stl` 이 평판 검사 없이 평균 | FIXED (수확기) | claimed_fixed (범위) | `af528e24d` · 수확기 ⑮ | 웹앱 `parse_mesh_stl` (`SELF-49`) |

대조 원문 (항목별 근거 · 탐침 8 개 · 증거 표기) = 같은 커밋의 `docs/reviews/codex_lhs_release_final_reconcile_20261001.md`.

## 3. 질문

- **Q1 (원장)** §2-A 의 판정이 맞는가 — FIXED · MOOT · 범위 한정 claimed_fixed 에 반례가 있으면 재개방.  PARTIAL · OPEN 이 배포 열을 오염시키는가.
- **Q2 (Codex 를 안 거친 묶음)** 열 사전의 정의 ↔ 코드 ↔ 값이 맞는가 — 커밋된 원자료로 열마다 재현.  특히 CN · AM–SE CN 의 분모 (벽 · 외톨이),
  퍼콜레이션 띠 규칙 (2r · L0) 과 `n_components` 의 외톨이 포함, 벽 τ 의 표본 (200 쌍 · 절단) 과 "기하 최단경로 — 수송 τ 아님", 이온 경로 고립 (단절 · 무접촉) 의 정의.
- **Q3 (적격성 HOLD)** HOLD (130 중 59 · 64 중 62 — 벽 밖 중심 · 구 부피 합 porosity < 0) 가 **어느 배포 열을 얼마나** 흔드는가.  표지만 싣고 거르기를 쓰는 쪽에 맡기는 것 (README §3-7) 이 맞는가, 아니면 일부 열을 HOLD 행에서 비워야 하는가.
- **Q4 (두께)** 배포 두께 둘 — `thickness_wall_gap_um` (측정 판 간격 · 09-24 에 받아들인 것) 과 `thickness_mass_conserving_um` (= 벽 간격 × (1 − ε_구부피합)/(1 − ε_union) · φ 두 열과 같은 장부) 의 정의 · 용도 구분이 맞는가.  후자는 Codex 가 본 적이 없다 (HND-01 과 같은 부류의 위험인가).
- **Q5 (관문)** G1–G7 · P1–P3 · T1–T3 · D1–D5 · C1–C3 · 배치 관문 · 두 감사기 · 배포 빌더가 **적힌 실패를 실제로 거부하는가** — 변이 (값 하나 · 행 섞기 · 프레임 둘) 로.
- **Q6 (빈칸 · 0 · N/A · mono · 상수)** 열마다 README §3 규칙과 같은가 — mono 의 없는 상 칸 · 비관통 24 의 τ · `area_<쌍>_n` 의 측정된 0 · mono (B) 접기 · 상수 열 표기.
- **Q7 (문구)** README · AI 프롬프트 · 열 사전의 과장 · 빠진 한정어 · 틀린 설명.
- **Q8 (넘기지 말 것)** 정의상 중복 · 정보 없음 · 잘못 정의된 열이 있는가.

## 4. 재현

```
git checkout <이 요청서가 있는 커밋>
python3 scripts/lhs_design_dataset.py --selftest          # 207/207
python3 scripts/lhs_descriptor_harvest.py --selftest
python3 scripts/lhs_webapp_batch.py --selftest
python3 scripts/lhs_perc_audit.py --selftest              # 35
python3 scripts/lhs_contact_audit.py --selftest
python3 scripts/analyze_contacts.py --selftest            # 25/25
python3 scripts/lhs_release_build.py --selftest           # 8/8
# 인계표 재생성 → 커밋본과 바이트 비교
python3 scripts/lhs_design_dataset.py --export-handover /tmp/h130.csv --harvest docs/data/lhs_descriptors_cov_1e09f661d --union docs/data/lhs_union_20260927/lhs130_union.tsv --webapp docs/data/lhs_webapp_contact_d1ec42fba --webapp-groups contact,percolation
python3 scripts/lhs_design_dataset.py --export-handover /tmp/h64.csv --design docs/data/lhsx_design_adapted_20260929.csv --harvest docs/data/lhsx_descriptors_cov_1e09f661d --union docs/data/lhs_union_20260927/lhsx64_union.tsv --webapp docs/data/lhsx_webapp_contact_d1ec42fba --webapp-groups contact,percolation
cmp /tmp/h130.csv docs/data/lhs_handover_20261001.csv && cmp /tmp/h64.csv docs/data/lhsx_handover_20261001.csv
# 배포 ⊆ 인계표
python3 scripts/lhs_release_build.py --check --handover docs/data/lhs_handover_20261001.csv --release docs/data/lhs_release_20261001_v11/lhs_release_20261001_v11
python3 scripts/lhs_release_build.py --check --handover docs/data/lhsx_handover_20261001.csv --release docs/data/lhs_release_20261001_v11/lhsx_release_20261001_v11
```

## 5. 판정 형식

- 묶음마다 GO / HOLD · 발견은 P1 / P2 / P3 · 반례마다 재현 스크립트.
- 원장 항목은 항목마다 verified (검증자 = Codex) / 재개방 (반례).
- 증거 폴더 이름 제안: `docs/reviews/codex_lhs_release_final_evidence_<날짜>/` (반입은 우리가 한다).
