# 50kg D2-50 끝 상태 (step 4,015,002 · 판 고정 이완 끝) — 1저자 10-30 업로드

- 무엇: `kg50_d2_b50` (SE D50 2 µm · 50 × 50 µm · v3 덱) 본 런의 끝 상태 한 장씩 — atom · contact · 판 mesh (`write_restart restart_end` 뒤 `run 0` 덤프 · 덱 244–256 행) + 본 덱.  본 런 = 10-28 09:42 본 제출 (재개 도구 `-s ins1` · r4) → 10-29 끝 (1저자 화면 `Simulation Finished` · ERROR 0).
- ibb 원본 묶음 (1저자 10-30 화면): `~/kg50_d2_end_20261030.tgz` 8,905,404 B · sha256 `7454f594afd67a60b461ee82257b5d4f6af4d3e5c1562b45926545bff9082bda` · 멤버 8 = 아래 넷 + `log.liggghts` · `input_kg50_d2_b50_r4.liggghts` · `input_kg50_d2_b50_r4t.liggghts` · `input_kg50_d2_b50_insert.liggghts`.  **받은 것 = 넷 (따로 올림)** — 로그 · r4 · r4t · 삽입 덱은 안 옴 (r4 · r4t 는 `docs/data/kg50_resume_tests_20261027/d2_main_1028_0942/` 에 10-28 사본 · 이 묶음과의 바이트 대조는 못 함).
- 이 폴더 `kg50_d2_end_20261030_4files.tgz` = 받은 넷을 ibb 와 같은 경로 이름으로 다시 묶은 것 (8,732,365 B · sha256 `ead5bed68e770766a93e2f2c79899f88ff7150ec687409d220c05298add5cbfa`).

| 파일 (묶음 안 경로) | 바이트 | sha256 |
|---|---|---|
| kg50_d2_b50/input_kg50_d2_b50.liggghts | 12,785 | `f8ac9932a6cb4a0b45c9b6cb846bc637dd746ccf036f32590036c70ab6508825` |
| kg50_d2_b50/post_kg50_d2_b50/atom_end_4015002.liggghts | 2,936,830 | `e14fe38b2aa614dc61dd719aa6b7b2c4f5d40316c2f3a4f15877bced95861d52` |
| kg50_d2_b50/post_kg50_d2_b50/contact_end_4015002.liggghts | 20,824,746 | `9f476962abe59d1281d4425857d79638263b139912c2f5dc9aa0a28cdf44722b` |
| kg50_d2_b50/post_kg50_d2_b50/mesh_end_4015002.stl | 349 | `3db1e87d86b5b7df69ee94bfd4700534837734f84be85a3839e86ffb643cc9f2` |

## 대조 (메인 · 10-30)

| 무엇 | 결과 |
|---|---|
| 본 덱 | `docs/data/kg50_decks_20261027_v3_b50/kg50_d2_b50/input_kg50_d2_b50.liggghts` 와 바이트 같음 |
| atom 덤프 머리 | TIMESTEP 4015002 · 원자 22,353 (= 계획 합 · 삽입 100 %) · 상자 0–0.05 × 0–0.05 (pp) |
| 판 mesh | 두 면 모두 z = 0.122469 (덱 단위 = µm × 1/1000) → 판 높이 122.469 µm |

- 쓰임: 50kg 4차년도 보고 3판 (`docs/50kg/kg50_report_plan_fix_plan_20261030.md` §2) D2 그림 · 분석 계획 (Q4) 의 끝 상태 프레임.  압력 · 판 높이 시간 곡선 (p2) = 아래 로그.
- 로그 (1저자 10-30 업로드 · ibb 작업 폴더 `log.liggghts` = r4 재개 런 · step 20001 → 4,015,002): `kg50_d2_b50_log.liggghts` 1,102,372 B · sha256 `5d6721508615f2ffbd71a5c179a394f09c46f4993ac449496166ac08509dd198` — 4차년도 보고 초안 1 의 2쪽 보조 그림 (가압 · 고정 높이 이완) 원자료.  이완 끝 판 압력 = 마지막 정규 thermo 줄 (step 4,015,002 · 덱 열 0.27979158) · 끝 `run 0` 설정 줄 (0.32894624) 은 설정 줄 압력이라 쓰지 않는다.
