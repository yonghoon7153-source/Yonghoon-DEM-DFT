# 50kg 4차년도 DEM 보고 — 초안 2 자료 · 그림 (10-30)

- 무엇: 초안 2 쪽 그림 (PNG 300 dpi · SVG 글자 그대로 · 그린 값 CSV) + 침대별 지표 (`metrics_<침대>.json` · `metrics_all.csv`) + OVITO 사본.  1저자가 양식 (10 × 7.5 in · 4:3) 에 직접 붙인다 → 그림 = 양식 반쪽 칸 크기 · 100 % 로 붙인다 (모든 그림 같은 글자 크기 — 눈금 7 pt · 축 제목 8 pt).
- 근거: `docs/50kg/report_y4/draft2_fix_plan_20261030.md` (§2 쪽 목록 · §3 프레임) · Codex 초안 1 판정 `docs/reviews/codex_kg50_y4_draft1_review_20261030/codex_review_kg50_y4_draft1_20261030.md` (§6–§8 문구 한계) · 문헌 지도 `docs/50kg/report_y4/lit_se_size_map_20261030.md` · 보고 원칙 `docs/report_making_principles.md`.
- 비교 상태 = **판 고정 이완 끝 세트 하나** (atom_end · contact_end · mesh_end 같은 step · 1저자 10-30).  **압력 도달 순간 세트 = 자료 없음** (압축 정지 step 에 덤프 없음 · `K50Y4-01`) — 이완 끝 프레임을 300 MPa 상태로 부르지 않는다.  가압 목표 300 MPa · 끝 판 압력 D2 279.8 · D3 291.4 MPa.
- 침대: SE 2 µm (D2) · 3 µm (D3) = 자료 있음 · **SE 1 µm (D1) = 오늘 끝 세트 도착 예정 (아래 한 명령)** · SE 0.7 µm (D0.7) = 결과 대기 (모든 비교 그림에 빗금 빈 칸).
- 새 지표 정의 없음 — 값 = 검토된 웹앱 파이프라인 (`run_pipeline(stop_after='network')`) · 기존 함수 · 기존 입자 · 접촉 · 점 출력의 집계 (z 구간 · AM 하나당 · 문턱별) 뿐.  새 정의가 필요한 것 = "다음 판" (§6).

## 1. 침대별 핵심 값 (이완 끝 · 입도별 시드 1)

| 양 | SE 2 µm (D2) | SE 3 µm (D3) | 출처 |
|---|---:|---:|---|
| 끝 step (atom · contact · mesh 같음) | 4015002 | 4575002 | 끝 세트 |
| AM · SE 수 (끝 덤프) | 1481 · 20872 | 1482 · 6184 | atom_end |
| 판 높이 (µm) | 122.469 | 125.877 | mesh_end |
| **ε_sphere (%)** | **16.7379229** ✓ Codex | **18.9575565** ✓ Codex | 1 − ΣV구 / (50·50·판 높이) — 웹앱 값과 3e-11 %p 안 (합산 순서) |
| 기공률 정확 합집합 (%) | 19.60 | 22.43 | calc_porosity_union_exact (MC 4 × 10⁶ 점) |
| **이완 끝 판 압력 (MPa)** | **279.79158** ✓ Codex | **291.37440** ✓ Codex | 로그 마지막 정규 thermo × 1000 |
| 정지 직전 t = 0⁻ · 이완 첫 출력 (MPa) | 300.23909 · 287.18633 ✓ | 300.63094 · 295.59389 ✓ | 로그 |
| AM–SE 접촉 수 (AM 1개당 평균) | 24.06 | 10.31 | calc_am_isolation_risk |
| SE–SE 접촉 수 (SE 1개당 평균) | 4.04 | 3.34 | calc_se_se_cn |
| AM 피복률 Hertz 계열 / Physics 합집합 cap (%) | 21.05 / 54.23 | 19.07 / 52.63 | calc_coverage · union_coverage_bed |
| AM–SE 접촉 면적 / AM (µm², 평균) | 22.55 | 20.32 | coverage_per_am.csv (c_cpl[22]) |
| f = σ_eff/σ₀ Hertz (Physics) | 0.0334 (0.0638) | 0.0195 (0.0378) | network_conductivity → tau_flux.case_row |
| 수송 tortuosity Hertz (Physics) | 8.26 (4.32) | 13.63 (7.03) | φ_SE·σ₀/σ_eff · 제곱근 아님 · φ = 질량 보존 |
| 기하 tortuosity | 1.276 | 1.366 | calc_tortuosity_all (최단 경로 / Δz) |
| SE 망과 연결된 AM (%) (연결성 기준) | 100 | 100 | calc_ionic_active_am |
| 협착 소산 몫 (이온 · Hertz) | 0.715 | 0.710 | constriction_power_share_ion_hertz |

- ✓ = Codex 독립 재계산 (판정문 §3) 과 출력 자릿수까지 같음 — 러너가 대조하고 다르면 rc 3 으로 멈춘다 (`CODEX` 표).  D3 의 웹앱 다섯 값 (기공률 · 피복 두 갈래 · σ_ion · tau2) 은 10-27 칸 판정 (`docs/data/kg50_d3_cell_verdict_20261027/verdict.json` · 코드 판 `e65e92b7b`) 과 비트 같다 (현 HEAD `12227fa3c` 재실행).
- 전체 = `metrics_all.csv` (침대 넷 행 · 없는 침대 = 결과 대기) · 침대별 원값 · 출처 = `data/<침대>/metrics_<침대>.json`.

## 2. 그림 (`figs/` · 크기 = in · 300 dpi · 각 PNG · SVG · CSV)

양식 패널 (좌 · 우 점선 상자) = 4.63 × 4.56 in (y 2.41 → 6.97 in · 빌드 상수 `PANEL` · `PANEL_BOTTOM`) → 그림 폭 4.50 in (패널 안 여백 0.06 in) · 높이 2.3–3.0 in (패널 안에 머리 글 · 캡션 자리).

| 그림 | 쪽 | 크기 | 자료 | 캡션에 꼭 넣을 한정어 |
|---|---|---|---|---|
| `p1_bed_strip` | 1 | 4.50 × 2.95 | `data/<침대>/section_*.csv` (초안 1 단면과 6 자리 반올림 안 같음) · 덱 (SE 수 · 크기비) | 끝 상태 (판 고정 이완 끝) x–z 단면 · y = 25 µm 평면 · 같은 배율 · AM 검정 · SE 노랑 · 흰 곳 = 2D 구 기하 합집합의 빈 영역 (2쪽 ε_sphere = 3D 구 부피 합과 같은 양 아님) · 겹침 색 = 그리는 순서 (물질 소유권 아님) · 회색 선 = 끝 판 · 벽 · 판에서 자름 · 아래 글 = 덱 계획 SE 수 · D_AM/D_SE · 0.7 · 1 µm 결과 대기 |
| `p2_compaction` | 2 | 4.50 × 2.70 | `data/<침대>/curve_*.csv` (로그) · metrics | (a) **p > 1 MPa 표시 구간** (첫 접촉 아님) · ε_sphere = 1 − ΣV구 / (50 × 50 µm² × 판 높이) · 판 압력 = 로그 thermo 열 × 1000 (run 첫 setup 줄 뺌) · 점선 = 판 고정 이완 (ε 고정 · 압력만 감소) · ○ = 이완 끝 (비교 상태) · (b) 막대 = 이완 끝 ε_sphere · ◇ = 정확 합집합 (벽 밖 부피 뺌) · 가압 목표 300 MPa · 끝 판 압력 279.8 · 291.4 MPa · 언로딩 없음 · D2 ↔ D3 차 = 산술만 (정착 충전 · 시드 · 질량당 감쇠 · 실행 이력 · 끝 압력 차이 공존 → 입도 인과 아님) |
| `p2_relaxation` (보조) | 2 | 4.50 × 2.30 | `curve_*.csv` | ○ t = 0⁻ = 정지 직전 (마지막 정상 압축 출력 · PHASE 4 setup 값 아님) · 판 고정 10⁵ step · 끝 `run 0` setup 줄 (328.9 · 582.7 MPa) 안 씀 |
| `p3_contacts` | 3 | 4.50 × 2.55 | metrics | (a) AM 1개당 AM–SE 접촉 수 (b) SE 1개당 SE–SE 접촉 수 (c) AM 피복률 = SE 접촉 면적 합 / (4πr² − AM–AM 면적) · 막대 = Hertz 계열 (LIGGGHTS 접촉 면적 c_cpl[22] = 기하 교차 원판 · 주) · ○ = Physics 합집합 cap (민감도) · 기하 면적 ≠ 전도 면적 |
| `p3_overlap_threshold` | 3 | 4.50 × 2.55 | metrics (`am_frac_overlap_*`) | AM–SE 접촉 중 겹침 비가 문턱을 넘는 것이 하나라도 있는 AM 의 비율 (분모 = 전체 AM) · (a) δ / min(r₁, r₂) = 기존 `calc_overlap_ratio` 정의 (AM–SE 는 r_SE 기준) (b) δ / (r₁ + r₂) = Zhou 2025 카드 (`tailored_cathode_microstructure_low_pressure_assb`) 의 "두 입자 반경합 대비" 를 같은 δ 에 적용 · 우리 겹침은 유효 E 1.35 GPa 규약이라 크다 (AM–SE 겹침 비 중앙값 (a) 18.4 · 19.6 % (b) 4.6 · 6.5 %) → 문헌 DEM 비율과 직접 비교하지 않음 · 100 근처 막대는 값 글 생략 (CSV) |
| `p3_per_am` | 3 | 4.50 × 2.55 | `data/<침대>/per_am_*.csv` | (a) AM 1개당 AM–SE 접촉 면적 합 (Hertz 계열 · µm²) (b) AM 1개 피복률 분포 — 채움 = Hertz 계열 (주) · 빈 상자 = Physics 합집합 cap (민감도) · 상자 25–75 % · 선 5–95 % · + 평균 · 숫자 = 중앙값 |
| `p4_tortuosity` | 4 | 4.50 × 2.55 | metrics | (a) 기하 tortuosity = SE–SE 접촉 그래프 최단 경로 / Δz (바닥 관통 SE 전부 · 길이만 · 수송 τ 아님) (b) **수송 tortuosity = φ_SE·σ₀/σ_eff (전도도에서 정의한 무차원 수송 지표 · 제곱근 아님 · φ = 질량 보존 · 전극 부피)** · Hertz 주 · ○ Physics 민감도 · 두 양 = 다른 정의 (비로 묶지 않음) · 단분산 (PSD 폭 변화 없음) |
| `p4_f_connect` | 4 · 5 | 4.50 × 2.55 | metrics | (a) f = σ_eff/σ₀ (원 솔버 σ · σ₀ 약분 · Hertz 주 · Physics 민감도 · Stage-E σ_ion 안 씀) · **f 와 수송 tortuosity = 같은 해의 종속량** (독립 성공 둘로 세지 않음) (b) SE 망과 연결된 AM 비율 (연결성 기준 = 위쪽 판에 닿는 SE 성분과 접촉한 AM) |
| `p6_z_structure` | 6 | 4.50 × 2.80 | `data/<침대>/zprof_*.csv` | z 10 구간 (바닥 0 → 판 · 같은 폭 12.2–12.6 µm) · (a) 국소 기공률 = 정확 합집합 몬테카를로 점 (calc_porosity_union_exact 와 같은 씨앗 · 같은 점 · 구간당 ≈ 4 × 10⁵ 점 · 통계 오차 ≈ 0.06–0.07 %p) 의 빈 점 비율 — 벽 · 판 옆 구간이 높은 것 = 평면 벽 옆 충전 · ε_sphere 와 다른 규약 (b) SE 망과 연결된 AM 비율 (AM 중심 z · 구간당 AM 139–156 개) · 점선 = 각 판 높이 · "함께 비교" (기계 → 전기 인과 아님) |
| `p6_z_stress` | 6 | 4.50 × 2.80 | `zprof_*.csv` | Love–Weber 입자 응력 σ_VM (입자 접촉력 기반 대칭 응력 · kinetic · 벽 · couple 항 없음 · 프레임 미인증 · 이완 끝 가압 상태) · 선 = 구간 중앙값 · 띠 = 25–75 % · 벽 · 판에 닿은 입자 제외 (함수의 nowall 규칙 · 바닥 · 꼭대기 구간 AM 36–42 · SE 97–377 개) · 같은 도구 · 같은 규약끼리만 · 반응률 · 균열 · 용량 아님 |
| `p7_summary_heat` | 7 | 4.50 × 3.00 | `metrics_all.csv` | 칸 글 = 값 · 색 = SE 3 µm 대비 비의 log₂ (좋고 나쁨 아님 · ±2.5 배 포화) · 입도별 시드 1 (오차 막대 없음) · 값 표 — 방향 · 비단조 판정은 네 입도 산출 뒤 분석 계획대로 |
| `p7_lit_direction` | 7 | 4.50 × 3.00 | metrics + 정본 litdb 카드 6 | 작은 SE 쪽에서 문헌이 보인 방향 (화살표 · 카드 번호) 과 우리 값을 나란히만 — **일치 판정 아님** · 문헌 = 실험 · 다른 SE · 다른 PSD · 우리 = 단분산 대리 입도 · 시드 1 |

- 범례 · 설명 = 축 밖 (그림 위 한 줄) — 더 자세한 글은 슬라이드 글로.  SVG = 글자 그대로 (`font-family: Aptos, 맑은 고딕, Carlito, WenQuanYi Zen Hei, …`) → PowerPoint 에서 편집 가능.  ⚠ 이 기계에 Aptos · 맑은 고딕이 없어 **PNG 의 영문 = Carlito · 한글 = WenQuanYi Zen Hei** 로 박혀 있다 → 양식 글꼴로 보이려면 SVG 를 넣는다.
- 색: AM (NCM) `#1A1A1A` · SE `#CDB650` (50kg 계획 덱) · 입도 = 파랑 한 색상 밝음 → 어두움 (0.7 → 3 µm · dataviz 서열 검사 통과) · Physics = 속 빈 표지.
- 결정적 출력 — 같은 입력 · 같은 환경에서 두 번 그린 `figs/figs_meta.json` (파일별 sha256) 이 같음.
- p5 (조건부 σ 시나리오) = 초안 1 그대로 (새 숫자 없음) — f(1)/f(3) 손익분기 2.217 대조는 D1 산출 뒤 `metrics_all.csv` 의 f_ion_hertz 두 칸으로 (지금은 D2 · D3 만).

## 3. D1 끝 세트가 오면 (한 명령)

```bash
# 1) 1저자가 보낸 D1 끝 묶음 (atom_end · contact_end · mesh_end 같은 step · 덱 있으면 함께) 과 로그를 리포 기록 폴더에 넣는다 (예: docs/data/kg50_d1_end_<날짜>/)
# 2) 한 번에: 끝 세트 검사 → 웹앱 망 정지 파이프라인 → 집계 → metrics_D1.json → metrics_all.csv → 그림 전부 다시
python3 -P docs/50kg/report_y4/draft2/run_draft2_metrics.py add --bed D1 \
    --tgz docs/data/kg50_d1_end_<날짜>/<묶음>.tgz \
    --log docs/data/kg50_d1_end_<날짜>/<로그>.liggghts \
    [--prefix kg50_d1_b50/]   # 묶음 안 폴더가 다르면
```

- 묶음 안 접두 기본 = `kg50_d1_b50/` · 세 덤프가 같은 step 이어야 한다 (결손 · 엇갈림 = 거부) · 덱 멤버가 없으면 리포 v3 덱 (manifest `deck_sha256` 대조).
- 묶음 · 멤버 sha256 기록 (README 표) 이 있으면 `--record <README.md>` 로 대조 (D2 · D3 는 자동).  D1 은 Codex 기준값이 없으므로 sha256 · 값만 기록한다.
- D0.7 도 같은 명령 (`--bed D0.7`).  큰 침대 (D1 ≈ 1.7 × 10⁵ · D0.7 ≈ 4.9 × 10⁵ 입자) 는 망 단계가 길다 (D3 ≈ 1 분 · D2 ≈ 2.5 분 실측 · D1 은 더 김 — 추정).
- D2 · D3 다시 만들기: 같은 명령 (`run` = 그 침대만 · `merge` = 표만 · `add` = 셋 다) — 아래 §5.

## 4. OVITO

- `ovito/D2_end_4015002_um.xyz.gz` · `ovito/D3_end_4575002_um.xyz.gz` (확장 XYZ · µm · species = AM/SE · radius · id · dump_type) — 색 · 시점 · 단면 제안 = `ovito_render_spec.md`.

## 5. 재현 · 검사 (10-30 · 이 작업 트리 · HEAD `12227fa3c` 위)

```bash
python3 -P docs/50kg/report_y4/draft2/run_draft2_metrics.py selftest                      # 끝 세트 소비자 시험 9/9
python3 -P docs/50kg/report_y4/draft2/run_draft2_metrics.py add --bed D3 \
    --tgz docs/data/kg50_d3_cell_verdict_20261027/kg50_d3_end_20261027.tgz --log docs/data/kg50_d3_cell_verdict_20261027/kg50_d3_b50_s1_log.liggghts
python3 -P docs/50kg/report_y4/draft2/run_draft2_metrics.py add --bed D2 \
    --tgz docs/data/kg50_d2_end_20261030/kg50_d2_end_20261030_4files.tgz --log docs/data/kg50_d2_end_20261030/kg50_d2_b50_log.liggghts
python3 -P docs/50kg/report_y4/draft2/make_draft2_figs.py                                 # 그림만
```

| 검사 | 결과 |
|---|---|
| Codex 값 (ε_sphere · 이완 끝 · t = 0⁻ · 이완 첫 판 압력 · 정지 · 끝 step · AM · SE 수) | D2 8/8 · D3 8/8 출력 자릿수까지 같음 (`codex_check`) |
| 끝 세트 신원 | 묶음 sha256 = 기록 (D2 `ead5bed6…` · D3 `918394e1…`) · 멤버 4 개 sha256 = 기록 · 덱 = 리포 덱 = manifest · 덤프 머리 TIMESTEP = 파일 이름 step (세 파일 같음) |
| 집계 ↔ 웹앱 전체 값 대조 (침대마다 10 항) | D2 10/10 · D3 10/10 — 겹침 평균 (calc_overlap_ratio 재호출 · 접촉별 재계산) · AM–SE 접촉 수 평균 · top-reachable 비율 · SE 망 연결 AM 비율 · Hertz 피복 평균 · AM–SE 면적 합 · Physics 합집합 피복 평균 · Love–Weber CV · 정확 합집합 총 공극 (같은 씨앗 · 같은 점 · 비트 같음) |
| 로그 압밀 곡선 | 판 높이 복원 = 끝 mesh (덱 단위 5e-7 안) · 이완 끝 step = 끝 덤프 step · 압축 run 이음 (초안 1 `make_fig_p2_aux.branches` 그대로) |
| 1쪽 단면 | 초안 1 `docs/50kg/report_y4/figs/p1_sections.csv` 와 행 수 · 입자 · 주기 상 같음 · 좌표 차 ≤ 5e-7 µm (초안 1 CSV 6 자리 반올림) |
| 끝 세트 소비자 시험 (`selftest`) | 9/9 — 같은 step 세트 수락 · 덱 없음 → 리포 덱 · contact 결손 · mesh 결손 · contact step 엇갈림 · atom 둘 · 머리 TIMESTEP ≠ 이름 · 접두 밖만 = 거부 |
| 기존 도구 자기 시험 (이 트리) | `kg50_d3_cell_verdict.py --selftest` PASS (✓ 33 · ✗ 0) · `test_tau_flux.py` 55/55 · `coverage_physics_vs_hertzian.py --selftest` PASS · `lhs_union_webapp.py --selftest` PASS (0 실패) |
| 그림 결정성 | 두 번 그린 `figs_meta.json` 같음 |
| 문서 참조 (`scripts/check_doc_refs.py`) | 깨진 참조 없음 (이 폴더 포함 리포 전수) |
| 인용 금지 (`check_review_findings.ban_sweep` 를 이 폴더 파일에만) | 게이트 글롭 안 5 파일 (md · json) = 0 건 · 글롭 밖 CSV · SVG 의 숫자 열 · 경로 좌표 안에 등록 숫자열 (CL-33 · CL-90 항목) 이 우연히 포함된 6 건 (인용 아님 · 게이트 대상 아님) |
| 실행 시간 (이 컨테이너 · 4 코어) | D3 ≈ 1 분 · D2 ≈ 2.5 분 |

- 러너는 격리 폴더 (빈 임시 폴더 · `--work`) 에 풀고 웹앱을 Flask 시험 클라이언트로 부른다 (Supabase 끔 · 자동 DB 끔 · 그림 끔) — 리포 · 웹앱 데이터 폴더를 건드리지 않는다.  `scripts/check_all.sh` 는 돌리지 않았다 (이 작업의 범위 밖 · 메인 세션 게이트).

## 6. 하지 않은 것 · 다음 판

| 자리 | 상태 | 이유 |
|---|---|---|
| 2쪽 주 그림 (AM 표면 거리별 SE 점유 · 껍질) | 다음 판 | 새 지표 정의 (껍질 분모 · 상 겹침 소유권) — 반례 시험 먼저 (`KG50B-05`) |
| 3쪽 주 그림 (AM 구면 cap 합집합 지도) | 다음 판 | 새 지표 (지도 투영 · 대표 AM 규칙) — AM 별 합집합 피복 *값* 은 `p3_per_am` 에 있음 |
| 6쪽 ② z 구간 전위 강하 · 소산 몫 | 다음 판 | 망 해의 z 분해 = 새 정의 |
| 국소 기공률의 ε_sphere 판 (z 구간) | 안 함 | 구 · 구간 교차 부피 = 새 기하 계산 → 기존 정확 합집합 점 출력의 z 집계로 대신 (규약이 다르다고 캡션에 적음) |
| 압력 도달 순간 프레임 | 자료 없음 | 정지 step 에 덤프 없음 (`K50Y4-01` · `dump_modify first` 기본 no) |
| 5쪽 조건부 σ 시나리오 | 초안 1 그대로 | 새 숫자 없음 · f(1)/f(3) = D1 뒤 |
| 문헌 방향 그림의 Lin 2025 · Ohsaki 2026 · Calpa 2019 · Tron (Rational Optimization) · Stavola 2023 | 넣지 않음 [카드 대기] | 정본 litdb (로컬 ref `8734b9e5b`) 에 카드 없음 — 서지 · 값은 카드가 생긴 뒤 (규율 ⑥) |
| 오차 막대 · 경향 판정 | 안 함 | 입도별 시드 1 · 판정 (방향 일치 · 비단조 · 보류 · 한계) = 네 입도 산출 뒤 분석 계획대로 |

- `p3_overlap_threshold` (b) 의 δ/(r₁+r₂) = 같은 접촉 δ 의 정규화만 다른 문헌 카드 정의 — 새 물리량은 아니지만 기존 함수 (δ/min r) 밖의 식이므로 검토 때 명시 (쓰지 않으려면 (a) 만).
- 문헌 방향 그림의 카드 = `schlautmann2023_se_particle_size_composite_transport` · `minnmann2024_microstructure_porosity_visualization` · `tailored_cathode_microstructure_low_pressure_assb` · `minnmann2021_jes_charge_transport_bottlenecks` · `bazzoun2026_dem_fem_rnm_ionic` · `shi2019_high_am_loading_particle_size_assb` (정본 브랜치 로컬 ref 에서 방향 문장 확인 · 값은 옮기지 않음).

## 7. 파일

- `run_draft2_metrics.py` — 침대 러너 (`run` · `add` · `merge` · `selftest`) · `make_draft2_figs.py` — 그림.
- `data/<침대>/` — `metrics_<침대>.json` (값 · 끝 세트 · 덱 · 망 출처 · git HEAD · 도구 파일 sha256 · 함수 이름) · `per_am_*.csv` (AM 하나당: z · AM–SE 접촉 수 · 면적 · 피복 Hertz/Physics · 최대 겹침 비 둘 · SE 망 연결 · Love–Weber σ_VM · 벽 접촉) · `zprof_*.csv` (z 10 구간) · `curve_*.csv` (가압 · 이완 로그 곡선) · `section_*.csv` (1쪽 단면 원).
- `metrics_all.csv` — 침대 넷 한 표 · `figs/` — 그림 + `figs_meta.json` (크기 · dpi · sha256) · `ovito/` · `ovito_render_spec.md`.
