# 50kg/batch 4차년도 — D3 칸 판정 기록 (10-27)

- 등록 = `docs/data/kg50_decks_20261026_v2/README.md` §3 (결과 전 고정 · 판정 모드 **Hertz** · AM coverage **Physics · Hertz 둘 다** · 판정 순서 ①–④ · 지표 다섯).
- 결과 = **불합격** — 수송 tortuosity · σ_ion 두 지표가 문턱 5 % 를 넘는다 → 등록대로 비교 덱 D0.7 · D1 · D2 = **50×50** (`--fallback50`) · 1저자 10-27 *"50 50으로 하자 어쩔 수 없네"* → 덱 v3 `docs/data/kg50_decks_20261027_v3_b50/`.
- 판독기 = `scripts/kg50_d3_cell_verdict.py` (읽기 전용 · 값 새로 계산 안 함) · 이 폴더의 `verdict.json` = 그 판독기 출력 (같은 명령 재실행 = 바이트 같음 · 10-27).

## 1. 지표 (시드 3 평균 · s = 표본 표준편차 · 상대 차 분모 = 50×50 평균)

| 지표 | 40×40 평균 (s) | 50×50 평균 (s) | Δ | SE_Δ | 문턱 | 판정 |
|---|---|---|---|---|---|---|
| porosity ε_sphere (%) | 18.95 (0.21) | 18.95 (0.072) | 0.00546 %p | 0.129 %p | 0.5 %p | 통과 |
| AM coverage Physics (%) | 53.25 (0.49) | 52.81 (0.37) | 0.438 %p | 0.355 %p | 1 %p | 통과 |
| AM coverage Hertz (%) | 19.27 (0.22) | 19.09 (0.069) | 0.183 %p | 0.132 %p | 1 %p | 통과 |
| 수송 tortuosity Hertz | 14.5 (0.97) | 13.47 (0.15) | +7.62 % | 4.23 % | 5 % | **불합격** |
| σ_ion Hertz (mS/cm) | 0.05767 (0.0039) | 0.06191 (0.00069) | −6.84 % | 3.67 % | 5 % | **불합격** |

- 케이스별 값 = `verdict_table.md` · 전체 = `verdict.json` (망 코드 판 `e65e92b7b` · 여섯 모두 같음 · 이온 전극 `dirichlet_exact` · 면적 규칙 `hertz_ccpl22`).
- 수송 tortuosity = φ_SE·σ₀/σ_eff (`tau2_ion_hertz` · 제곱근 아님).  σ_ion 절대값 = 솔버 σ₀ 3.0 기준 (보고 기준 1.5 면 × 0.5) — 이 판정은 상대 차라 기준과 무관.

## 2. 원자료

- `kg50_d3_end_20261027.tgz` — 15,172,051 B · sha256 `918394e1c1531a7a83f793234cf56fba845d347f4f88d4724dc1434e701d2de3` · 1저자가 hit 에서 받아 올린 그대로 · 24 파일 = 침대마다 덱 1 + 끝 상태 (`atom_end` · `contact_end` · `mesh_end`) · 파일별 sha256 = `inputs_sha256.txt`.
- hit 실행 = v2 덱을 NP 1 로 처음부터 끝까지 (재개 없음) · 끝 step b40 4,540,002 · 4,620,002 · 4,385,002 / b50 4,575,002 · 4,605,002 · 4,570,002 · 원자 4906 · 7666.

## 3. 다시 계산하기

환경 = `env.txt` (python 3.11.15 · numpy 2.4.6 · scipy 1.17.1 · networkx 3.6.1) · 코드 판 = `e65e92b7b` 체크아웃.

```bash
mkdir -p IN WEB && tar -xzf kg50_d3_end_20261027.tgz -C IN          # 빈 폴더에 푼다
python3 -P upload_cases.py <체크아웃> IN WEB    # 웹앱 /upload 경로 (Flask 시험 클라이언트 · 격리 폴더 · Supabase 끔 · 이름 = 침대 · mode auto · type_map 빈칸 → 덱에서 1:AM_P,3:SE)
python3 -P run_cases.py <체크아웃> WEB          # run_pipeline(stop_after='network', figures=False, auto_db=False) — 웹앱 망 배치와 같은 호출
python3 <체크아웃>/scripts/kg50_d3_cell_verdict.py --uploads-root WEB/uploads --results-root WEB/results --json verdict.json
```

- `scripts/webapp_network_batch.py` 를 쓰지 않은 이유 = 그 도구의 파일 고르기가 `atom_<step>` 이름만 받아 `atom_end_*` 를 거부한다 → 같은 호출 규약으로 `run_pipeline` 을 직접 부른다 (`run_cases.py`).
- `-P` = 사용자 site 패키지가 필요해서 (`-I` 는 그것까지 뺀다).

## 4. 한정 · 판정에 쓰지 않은 관찰

- 수송 지표 산포: 40×40 CV 6.7 % · 50×50 CV 1.1 % (tau2 · σ_ion 둘 다).
- 사후 (판정 미사용 · 등록 밖): 40×40 시드 하나를 빼면 tau2 Δ = +9.19 % (s1 뺌) · +10.19 % (s2 뺌) · +3.48 % (s3 뺌) · σ_ion Δ = −8.14 · −9.11 · −3.27 % — 시드 하나가 문턱 넘고 안 넘고를 가른다 = 40×40 의 시드 산포가 크다.  등록 판정 (시드 셋 평균) 은 그대로 불합격.
- 작은 SE (D0.7) 에서 40×40 이 괜찮은지는 재지 않았다 (1저자 *"작은 SE에서 40*40 괜찮은지도 보고 싶은데 시간 없는게 문제네 / 빨리 50 50 으로 하자"*) — 이 판정은 D3 (SE 3 µm) 칸 하나로 영역을 고른 것이다.
- D0.7-40 침대 (ibb 삽입 끝 · `kg50_d07_b40.ins1`) = 쓰지 않는다 (v2 계획 "40×40 불합격이면 버림") · 폴더는 그대로 둔다.
- 본 비교의 D3 자리 = `kg50_d3_b50_s1` (등록 §3 "본 비교 (D0.7 · D1 · D2 · D3 시드 1)" 그대로 · 새 결정 아님).
