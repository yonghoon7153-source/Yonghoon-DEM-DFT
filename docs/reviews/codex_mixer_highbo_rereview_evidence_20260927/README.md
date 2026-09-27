# Codex 재리뷰 재현 묶음 — 믹서 고-Bo 확장 LH (2026-09-27)

판정문 = `docs/reviews/codex_mixer_highbo_rereview_verdict_20260927.md` (HOLD · ① 부분 · ② 닫힘 · ③ 부분 · ④ 열림 · HBR2-01 ~ 08).

## 출처

- 사용자 업로드 `mixer_highbo_rereview_20260927.zip` (199,656 B, 2026-09-27 저녁 KST).  안의 `mixer_highbo_rereview_evidence_20260927/` 에서 **증거 파일 넷**만 여기 뒀다:
  `review_probe.py` (합성 반례 프로브, 실제 함수 호출) · `review_probe_output.json` (Codex 환경 출력 — Python 3.12.14 · SciPy 1.18.1) · `selftest_output.json` (네 셀프테스트 출력 전문) · `sources.json` (검토 스냅샷 `6963632a0` 의 파일별 blob).
- ZIP 에 같이 든 리포 사본 20 개 (스크립트 · STL · 문서) 는 **넣지 않았다** — 정본은 git 이다.  ⚠ 그 사본들은 `sources.json` 의 blob 과 20/20 **불일치**했다 (CRLF 를 걷어내도 끝 빈 줄 하나가 더 있음 — `gen_all.sh` 로 확인 · 내용 차이는 아님).  **HEAD 는 20/20 일치**.  ZIP 에는 판정문 `.md` 자체는 들어 있지 않았다 (사용자 메시지 본문으로 수신).
- LIGGGHTS upstream 소스 4 개 (`src/fix_mesh.cpp` 등, `3d5c00f2…`) 는 `sources.json` 에만 있고 ZIP 에 없다 (K2 근거 — 리포 밖).

## 우리 쪽 재현 (HEAD `643e32422`, 2026-09-27)

`review_probe.py` 를 **이 리포의 `scripts/` · `dem_scripts/`** 에 심볼릭 링크로 붙여 돌렸다 (`review_probe_output_HEAD_643e32422.json`, rc 0 — 프로브의 assert 7 개 전부 성립).  Codex 값과 같다:

| 반례 | HEAD 결과 |
|---|---|
| HBR2-01 참 벽 겹침 δ/r **2.000 %** · 위상 반 면각 어긋남 | **PASS** · 예정각 계산 wall_max **−53.756 %** · 위상 **5/5 ok** (오차 0.0005°) |
| HBR2-01 참 벽 = 예정각 · δ/r 0.500 % | **TECH** · 5/5 mismatch |
| HBR2-02 정상 bin 0 스모크 (26 프레임) | `tech` = 미완주 (bin 7 불완전) · `planned.complete` false |
| HBR2-04 bin 0 → 1 · bin 6 → 2 · bin 7 → 25 프레임 | `complete` **true** · `flat` **true** · M 0.5833 · `dump_gaps` [(200, 7160)] · `tech` [] |
| (대조) 마지막 덤프 하나 없음 | `complete` false (잡힘) |
| HBR2-05 덱 비교 변이 (P–S 한 방향 ×2 · SE–SE NaN · P–P 음수 · CED fix 헤더 변경) | 넷 다 **PASS** |
| HBR2-06 `cell_stats` (조밀 혼합 2 칸 + 성긴 순상 8 칸, n_min 20) | 유지 부피 AM = SE = **0.9804** · S²_keep **0** · S²_all **0.2** |
| HBR2-08 type 교환 + 반경 절반 | **PASS** |
| HBR2-03 덤프 결손 프레임 | PASS · n_frames 2 · 빠진 순간 합성 겹침 2.000 % |
| K1 산술 | 덤프 간격 31.98 ms · SE–SE δ 1.0302 % / Hertz 22.25 µs · AM_P–SE 0.9194 % / 19.85 µs · SE–벽 0.8993 % / 19.42 µs |
| HBR2-07 | d = (−0.3, 0.9, 0.3): Δ 0.300 · SE 0.3464 · `|Δ| ≤ SE` 통과 |
| 기하 | 39 면 · 78 삼각형 · 변심거리 13.0951 mm · 처짐 0.0426 mm · 회전 시작 step 385,337 |

⇒ 반례는 Codex 환경 산물이 아니라 **우리 HEAD 코드의 성질**이다.  수정은 이 프로브의 경우들을 셀프테스트로 먼저 옮긴 뒤 한다 (규율 ②).
