# 단면 하중 몫 — 발표 5 쪽 힘 그래프를 보존량으로 (10-07)

- **무엇**: 발표 5 쪽 "Force contribution (%)" (접촉 법선력 **크기 합**의 접촉 종류별 몫) 대신, **수평 단면을 지나는 수직 하중의 몫** — 1저자 10-07
  (리뷰 의견 *"이해하기 어렵다"* → *"힘은 보존이 되나?"* → 단면 하중 몫 권고 → *"한번 진행해봐"*).
- **왜**: 크기 합은 보존량이 아니다 — 같은 하중이 직렬로 놓인 접촉 수만큼 여러 번 세어진다 (real14: 크기 합 = 가운데 단면 하중의 **12.19 배**).
  단면 하중은 힘 평형으로 높이마다 같다 (real14: 유효 단면 21 개 최대 ÷ 최소 **1.0009**).
- **도구**: `scripts/plane_load_share.py` (읽기 전용 · 정의 · 벽 처리 · 상태 = 머리말 · `--selftest` 24/24 — 직렬 · 평행 기둥 · id 순서 · 가로 힘 · 결손 접촉 · 얇은 침대 ·
  무게 · 압력 환산 · 배치 파일 끝까지).

## 1. real14 로 확인 (`real14_validation/` · 커밋된 덤프 · 같은 hooke/hysteresis 모델의 다른 침대)

| 양 | AM–AM | AM–SE | SE–SE |
|---|---|---|---|
| 접촉 수 몫 | 0.6 % | 29.4 % | 70.0 % |
| 법선력 크기 합의 몫 (옛 5 쪽 방식) | 33.0 % | 34.6 % | 32.3 % |
| **가운데 단면 하중 몫** (z 15.14 µm · 263.17 MPa) | **74.0 %** | 22.8 % | 3.2 % |
| 유효 단면 21 개 범위 (12.0–18.3 µm) | 71.5–77.4 % | 19.3–24.6 % | 2.9–4.4 % |

- 검사: 입자 힘 평형 (벽에서 2 r_max 밖 입자 · 힘 가중 알짜 힘) **2.3e-4** · 원자 없는 접촉 0 · 힘 = 덤프 `fx·fy·fz` (법선 + 접선).
- 다시 만들기: `python3 scripts/parse_liggghts.py <atom_2060000> <contact_2060000> <mesh_2060000.stl> -o real14_res` (덤프 = `docs/data/real14_reference_20260928/` 를 푼 것) →
  그 폴더의 input_params.json = `{"box_x": 0.05, "box_y": 0.05}` · meta = `{"type_map_resolved": "1:AM_P,2:AM_S,3:SE", "scale": 1000}` →
  `python3 scripts/plane_load_share.py --case real14_res --meta <meta> --label real14 --out <폴더>` (`plane_load.json` 의 code_sha256 = 이 커밋의 스크립트).
- 관찰 (기록만): real14 덤프에 중심이 바닥 (z = 0) 아래인 입자 122 개 · 판 위 3 개 — 새어 나간 입자 (가운데 단면 값에는 무관 · 원인 미확인).
- **접선력** (`tangential_share.txt`): 접선 ÷ 법선 (합) = 0.25 · 0.27 · 0.26 (AM–AM · AM–SE · SE–SE) · 쿨롱 한계 (μ 0.5) 의 미끄럼 접촉 21–27 % · 크기 합 몫을 합력
  |Fn + Ft| 로 바꿔도 차이 ≤ 0.05 %p — 단면 하중 몫은 처음부터 합력 z 성분을 쓴다.

## 2. ps45 다섯 조성 (⬜ 1저자 WSL)

```bash
cd ~/dem-audit && pgrep -af "run_network_194_parallel|lhs_webapp_batch" || echo "실행 중인 배치 없음"
git fetch -q origin claude/stoic-knuth-NObVQ && git checkout -q --detach FETCH_HEAD && git log --oneline -1
python3 scripts/plane_load_share.py --selftest | tail -1
python3 scripts/plane_load_share.py --batch ~/ps45_network_20261006 --out ~/ps45_plane_load_20261007; echo "rc=$?"
tar -czf ~/ps45_plane_load_20261007.tgz -C ~ ps45_plane_load_20261007 && sha256sum ~/ps45_plane_load_20261007.tgz
```

- 입력 = 망 배치 폴더의 `work/results/<id>/` (atoms.csv · contacts.csv · mesh_info.json · input_params.json) + `work/uploads/<id>/meta.json` (type map · scale) — 읽기만 한다.
- 출력 = `plane_load_share_slide.csv` (Origin 머리 세 줄 · 가운데 단면 묶음 몫) · `plane_load_summary.csv` (+ 단면 평균 · 옛 방식 비교 · 하중 · 검사) · 단면별 CSV · JSON.
- ⚠ 한정: 이 프레임은 압축 뒤 이완 단계 (7:3 판 압력 165 MPa) · 단면 하중 몫은 그 프레임의 하중 경로 — 판 하중 분담 (CLAUDE.md f_AM 절) 과 같은 계열이지만 같은 정의는 아니다.
