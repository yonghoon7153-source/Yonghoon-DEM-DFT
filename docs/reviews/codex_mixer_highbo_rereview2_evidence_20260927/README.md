# Codex 3차 리뷰 재현 묶음 — 믹서 고-Bo 확장 LH (2026-09-27 밤)

판정문 = `docs/reviews/codex_mixer_highbo_rereview2_verdict_20260927.md` (HOLD · HBR2 8 건 중 4 닫힘 · 4 부분 · 새 반례 HBR3-01 ~ 08).
요청서 = `docs/reviews/codex_mixer_highbo_rereview2_request_20260927.md` · 검토 스냅샷 = `20568797b`.

## 출처

- 사용자 업로드 `mixer_highbo_round3_review_20260927.zip` (187,745 B, 2026-09-27 밤 KST).  안의 `mixer_highbo_round3_evidence_20260927/` 에서 **증거 파일 여섯**만 여기 뒀다:
  `review_round3_probe.py` (새 반례 프로브 · 합성 fixture · 실제 함수 호출) · `previous_review_probe.py` (2차 프로브 — 새 드라이버가 옛 assert 를 빼고 fixture 와 호출만 다시 돈다) ·
  `run_selftests.py` (셀프테스트 다섯 묶음 실행기) · `review_round3_output.json` (Codex 환경 출력 — Python 3.12.14 · NumPy 2.5.3 · SciPy 1.18.1) ·
  `selftests_output.json` (32/32 · 23/23 · 14/14 · 7/7 · 89/89 전문) · `sources.json` (검토 스냅샷의 파일별 blob · 실행하지 않은 것 목록).
- ZIP 에 같이 든 리포 사본 17 개 (스크립트 · STL · 런처 · 문서) 는 **넣지 않았다** — 정본은 git 이다.  대조 (09-27 밤, `git hash-object`):
  **17/17 이 `sources.json` 의 blob 과 같고, 그 blob 이 전부 `20568797b` 의 것과 같다** (2차 때와 달리 줄끝 차이 없음 — Codex 가 EOF · CRLF 를 원본대로 되돌렸다고 README 에 적었다).
  HEAD `04fe95ae8` 와 다른 것은 둘뿐이다 — `scripts/mixer_restart_phase_test.py` (템플릿 · 분포 유지, `04fe95ae8`) · `docs/reviews/mixer_highbo_prereg_20260927.md` (`runs/` 경로 주석).  둘 다 아래 재현 수치에 영향 없음.
- LIGGGHTS 공식 문서 사본 (`doc/fix_move_mesh.html`) 도 넣지 않았다 — 판정문 링크 (cfdem.com) 로 대신한다.  ⚠ 그 사본의 upstream 스냅샷 (LIGGGHTS-PUBLIC 커밋 3d5c00f2…) 은
  **사용자 WSL 의 `lmp_serial` 빌드 배너의 git commit 과 같다** (`docs/data/mixer_phase_receipt_20260928/README.md`).

## 우리 쪽 재현 (HEAD `04fe95ae8`, 2026-09-27 밤)

`review_round3_probe.py` · `previous_review_probe.py` 를 **이 리포의 `scripts/` · `dem_scripts/` · `docs/`** 에 심볼릭 링크로 붙여 돌렸다 (`review_round3_output_HEAD_04fe95ae8.json`, rc 0 · 프로브 assert 10 개 전부 성립 · 리포 작업 트리 무변경).
**Codex 출력과 수치 505 개 전부 같다** (차이 0 · 임시 경로 문자열만 다름).  핵심:

| 반례 | HEAD 결과 |
|---|---|
| HBR3-01 A 대조 덤프 0 개 · B = [25000, 30000] | 영수증 `passed` **true** · 행별 A↔B 차 NaN · 요약 A↔B 차 **0 m** |
| HBR3-01 B 한 장 (25000) · A 0 개 | `passed` **true** |
| HBR3-01 A · B 모두 `mesh_0.stl` 한 장 | `passed` **true** · 오차 0° · "reset gap" 6.352978256° (관측이 아니라 두 예정식의 차) |
| HBR3-02 `load_phase_receipt` 변이 7 종 (바이너리 null · 엉터리 SHA · dt 2 배 · 다른 덱 SHA · 축 0 벡터 · 주기 NaN · `passed="false"` 문자열) | **7/7 받아들임** |
| HBR3-02 로그 · 바이너리 없이 합성 A/B 만 | `passed` true · `binary_sha256` null · 버전 빈 문자열 |
| HBR3-03 ±0.05° 구간 **내부** (θ + 0.025°) 에 최악 위상 · 실제 39 면 Drum · SE 반경 75.7 µm | 참 최대 δ/r **1.000800 %** · 검사값 (세 점) **0.999163 %** → **PASS / receipt** |
| HBR3-03 면 반폭 0.8 지점 입자 | δ/r 예정각 0.500 % · −0.05° −0.481 % · +0.05° **1.468 %** (증가 0.968 %p — 옛 "≤ 0.02 %p" 반례) |
| HBR3-04 mesh 덤프에 Drum 만 (끝판 없음) · Front 면 참 겹침 2 % | **PASS / mesh-dump** · wall_max −171.99 (드럼 거리뿐) |
| HBR3-05 기준 E0 t₀ (step 200) 존재 | S_R² 0.006944 · **M_final 0.450000** |
| HBR3-05 E0 step 200 없음 · 160 정착 프레임만 | S_R² 0.043403 · **M_final 0.529412** · `complete` · `flat` true · `tech` [] |
| HBR3-05 (부수) 계획 25 + 격자 밖 step 7301 한 장 | n 26 · expected 25 · `complete` true · M_final 0.432692 |
| HBR3-06 t₀ 뒤 프레임 id 열 없음 · 헤더 없음 · type 1.5 / 3.5 | 셋 다 **PASS** (bounded) |
| HBR3-07 같은 seed (32452843) LC/LH 쌍을 예정 세 디렉터리에 복사 + `--expect-deck` | **3/3 PASS · exit 0** (실제 고유 덱 2 개) |
| 옛 반례 재호출 (2차 HBR2-01 · 02 · 04 · 05 · 08) | 전부 새 판정 (TECH / PASS-bounded / tech_smoke [] / flat None / FAIL / REJECT) — 2차 수정은 실재 |

⇒ 반례는 Codex 환경 산물이 아니라 **우리 HEAD 코드의 성질**이다.  수정은 이 프로브의 경우들을 셀프테스트로 먼저 옮긴 뒤 한다 (규율 ②).
⚠ Codex 는 **실제 캠페인에서 이 결함들이 났다고 주장하지 않는다** — 도구가 그 경우를 거부하지 못한다는 재현이다 (판정문 §0).
