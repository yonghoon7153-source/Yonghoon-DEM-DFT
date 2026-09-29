# LHS 접촉 단계 웹앱 배치 + 수확 v3 — 130 (lhs) · 64 (lhsx) · 2026-09-29~30 · ⚠ **옛 코드 기준선** (coverage 개선 전)

이 README 는 네 폴더를 함께 설명한다: `lhs_descriptors_20260929/` · `lhs_webapp_contact_20260929/` · `lhsx_descriptors_20260929/` · `lhsx_webapp_contact_20260929/`.

- **원본 (사용자 WSL `~/dem-audit`)** — 둘 다 업로드본에서 계산:
  - 최종 `lhs_contact_20260929.tar.gz` — **499,779 B · sha256 `12a489a0518c2cdde4253f5644c8014577288cdbdde373561785c9d6a006cff3`** ← 이 폴더들의 내용 그대로
  - 기준선 `lhs_contact_20260929_baseline.tar.gz` — 464,544 B · sha256 `e08ef1d4a53fffeb2c3369a201f21ee57ad988927c521334ba26c39f798365e9` (mono REFUSED 재실행 **전**) — 커밋 안 함: 아래대로 최종본에 **그대로 들어 있다**.
- **코드** (배치 `status.json` 의 `runs` · 둘 다 `dirty False`):
  1차 `4b42179ec` (09-29 23:24 · lhsx 00:53) — 130: done 100 · REFUSED 30 · 64: done 48 · REFUSED 16 (mono 이름 규약 관문 · `SELF-66` · J20-f) →
  2차 `27933b44e` (09-30 01:52 · 02:08 · 관문 수정 `70e1203be` 포함 · done 은 건너뜀) — **130/130 · 64/64 done**.
  두 커밋 사이 웹앱 접촉 분석 · 수확기 코드 변경 **없음** (`git diff 4b42179ec 27933b44e -- webapp/app.py scripts/analyze_contacts*.py scripts/dem_analysis_core.py scripts/lhs_descriptor_harvest.py scripts/parse_liggghts.py` 빈 결과).
- **기준선 ⊂ 최종 (실측)**: 수확 JSON 차이 0 · 1차 done 행 (100 · 48) 의 공통 열 값 차이 0 · 새 열 2 (`inp.r_AM` · `inp.variables.r_AM`) = mono 전용 (bimodal 빈칸).
- **수확 v3 (20260929) ↔ v2 (20260925)**: 기존 키 값 차이 0 · `status` 기존 항목 변경 0 · 새 키 6 (`contact_scan` · `n_atom_frames` · `tau_wall_detail` · `tortuosity_dijkstra_SE_wall` · `wall_touch` · `wall_touch_rule`).
- **쓰임**: 1저자 09-30 — *"그대로 두고 … 나중에 수정한 코드로 나온 결과랑 비교"*.  수확기 coverage 개선 · cap v2 (둘 다 미병합) 뒤 같은 명령으로 다시 돌려 이 폴더와 비교한다.
- **인계표**: `../lhs_handover_20260930.csv` (130×133) · `../lhsx_handover_20260930.csv` (64×135) — 수확은 **v2 (20260925)** 로 불렀다 (v3 의 새 열 = 벽 τ · 벽 접촉 비율은 1저자와 같이 확인하기 전이라 싣지 않는다 · 기존 값은 v2 = v3).
  웹앱 열은 J20-g (같이 확인한 열만 = `area_<쌍>_n` 7 열) · J20-f (A) (mono 상별 칸 빈칸 130 에서 60 · 64 에서 32) · 같은 프레임 |Δporosity| 최대 1.2e-10 · 2.5e-10 %p · 옛 칸 변경 0.
