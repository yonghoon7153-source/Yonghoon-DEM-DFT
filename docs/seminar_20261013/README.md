# 연구세미나 덱 (2026-10 · 1저자 비준 개요 v1) — 생성기 · 그림 · 출처

- **덱 pptx 는 리포에 없다** (사용자 덱 미반입 규약) — 1저자에게 전달 · Codex 검토 ZIP 으로.  글의 정본 사본 = `slide_text_draft3.md` (장별 전문 + 발표자 메모).
- 흐름 (1저자 지정) = ① 파이프라인 → ② DEM 한계 → ③ MPM · SE 물성 · DEM↔MPM → ④ voxelization → ⑤ 첨가제 → ⑥ 문제 셋 → ⑦ 진행 → ⑧ 계획 · 본문 15 장 (2–16) + 표지 · 요약 · 참고문헌 · 끝 = 19 장.
- 양식 = 1저자 10-13 연구세미나 덱 (Codex 리뷰를 거친 밀도 · 리포 밖) 의 장을 프로토타입으로 복제 — 표지 · 그림 본문 · 두 칸 · 점선 틀 · 요약 · 참고문헌 · Thank you.

| 파일 | 내용 |
|---|---|
| `build_seminar.py` | 생성기 — `python3 build_seminar.py --template <10-13 덱.pptx> --repo <리포> --figs figs --out <out.pptx>` · 끝에 selftest (철회값 42 패턴 0 · 본문 내부 용어 0 · 19 장) |
| `figs/make_seminar_figs.py` | 새 그림 4 (파이프라인 · 격자 비 · 모델 vs 실험 σ_e · ps45 σ_e) — `--selftest` = 정본값 대조 + 철회값 스윕 · png + svg + csv |
| `slide_sources.json` | 장별 수치 출처 (생성기가 쓴다) |
| `slide_text_draft3.md` | 장별 글 전문 (자리 표시 글 · notes 포함) |
| `outline_v1.md` | 비준 개요 (10-13) |

## 재사용한 리포 그림 (덱 안 그대로 · 값 세대)

| 장 | 그림 | 출처 |
|---|---|---|
| 3 | ps73 네 단계 3D (porosity exact union) · G1 | `docs/data/ps73_compaction_curve_20261006/stages_20261012/aligned_ckpt/t1_geometry/` · `docs/report_20261021/previews/G1.png` |
| 4 | p14 수송 tortuosity (Hertz) · p15 σLi⁺ (σ₀ 1.5) | `docs/data/ps45_r45_network_g2_20261007/deck_p14p15_20261012/` |
| 5 | 이력 법선력 (코드 재현) | `docs/data/dem_governing_equations_report_20261011/fig2_hysteresis_cycle.png` |
| 10 | 첨가제 모식도 둘 · G6 | `docs/figures/additive_seed_vgcf_ptfe.png` · `additives_preview.png` · `docs/report_20261021/previews/G6.png` |
| 13 | 단면 하중 몫 · SE σ_VM 4 단계 (0–150 MPa 선형) | `docs/data/ps45_plane_load_20261007/slide/contribution_sigma_zz.png` · `docs/data/ps73_compaction_curve_20261006/stages_20261012/aligned_ckpt/t3_vm_se/…_4panel_nowall_linear_0_150_preview.png` |
| 15 | G5a · G5b · G3 | `docs/report_20261021/previews/` |

## 자리 표시 (리포에 없는 그림 — 1저자 10-13 *"공백에 글 포함해서 나중에 검토할 때 추가되게"*)

| 장 | 무엇 | 출처 · 명령 |
|---|---|---|
| 4 | 7:3 침대 실제 전류 경로 3D (이온 · Hertz · 전류 몫 50 %) | `scripts/network_current.py dump <ps45 7:3 결과 폴더>` → 웹앱 DEM 3D "⚡ 전류 흐름" 캡처 (WSL) |
| 6 | MPM 2D champion morphology (E 1.53 · σy 0.15) · 3D scaffold x–z 단면 | uma `~/work/mpm/vis_/viszoom_E1.53_sy0.15.png` · `scripts/viz_mpm_morphology.py <mpm run dir> --slice xz` |
| 8 | DEM-scaffold MPM 응력 정지 단면 ↔ DEM 침대 나란히 | 같은 스크립트 (real_14 · n_grid 384) + `docs/data/real14_reference_20260928` 덤프 |
| 9 | 복셀 상 격자 단면 · 전류 밀도 (원고 S16/S17) | STEP3 phase grid (`scripts/step3_sigma.py`) · 원고 SI 그림 (리포 밖) |

## 지킨 것

- 철회값 (`docs/reviews/claims.json` `quotation_ban`) 0 · 8팔 계열 비 · 이득 (CL-33 · CL-41 hold) 안 씀 — 절차 · 판정만 · 순수 SE 10 % = 보정 표적 (외부 앵커 아님 · CL-94) · 격자 비는 CL-24 공개값만.
- 수치는 전부 정본 문서에서 — `slide_sources.json` · 각 장 notes.  참고문헌 14 = litdb 정본 카드 서지 그대로.
- Codex 검토 요청서 = `docs/reviews/codex_seminar_deck_review_request_20261013.md` (발송 = 1저자).

## v2 (2026-10-13 · Codex NO-GO 판정 반영 · 1저자 Q1–Q6)

- 판정 = `docs/reviews/codex_review_seminar_deck_20261013.md` (첫 판 · SEM-01~14) + `codex_review_seminar_deck_v3_20261013.md` (통합 판정) · 계획 `docs/reviews/seminar_deck_fix_plan_20261013.md` · 재확인 요청서 `docs/reviews/codex_seminar_deck_v2_recheck_request_20261013.md` (대응표 SEM ↔ v2 · 발송 = 1저자).
- 1저자 결정: Q1 7 장 E ≈ **22 GPa** (우리 DFT E_VRH · DEM 문헌 입력 22.1 GPa [8]; Sakuda 24 GPa 유리값 = notes) · Q2 8 장 30.7 비교 삭제 (상태표 · 새 숫자 없음) · Q3 자리 표시 = 한 줄 라벨 + 명령 notes · Q4 14 장 상태표 다섯 행 · Q5 `transport tortuosity` + 정의식 · Q6 v2 → Codex 재확인.
- 생성기 v2: ■ 제목 18 pt (상속) · 본문 15 pt (125 % · 뒤 5 pt) · 캡션 12 pt · 그림 위로 · Codex §9 좌표.  **selftest (고치기 전 덱에서 실패 확인 뒤 고침)** = 지적 문구 16 본문 금지 · F4 조성 라벨 5 (svg) · 장당 단어 ≤ 100 (두 칸 · 점선 장 ≤ 120 · 자리 표시 제외) · bullet ≥ 15 pt · 캡션 ≥ 12 pt · 금지값 42 · 내부 용어 (`uma` · `WSL` 포함) 0 · 19 장.
- 새 그림 v2: F2–F4 글씨 = 최종 배치 기준 ≈ 12 pt · F4 라벨 5/5 (`_fmt` 의 x locator 를 범주 축에 안 씀 — 옛 판 결함 SEM-09) · F1 상자 문구 축약 + 띠 = 보정 **표적**.  값 불변 (selftest 정본 대조).
- 글 전문 v2 = `slide_text_v2.md` (덱에서 추출 · notes 포함) · `slide_text_draft3.md` = 초안 4 (역사).  참고문헌 16 (+ [15] Sakuda 2013 · [16] Wang 2018 — 정본 카드).
- 덱 pptx · PDF · 렌더 = 리포 밖 (ZIP v4) — Codex 재확인은 **수정 PPT + 그 PDF** 로.
- **v2.1 (10-13 · Codex 재확인 = 조건부 GO · `docs/reviews/codex_review_seminar_deck_v2_recheck_20261013.md`)**: P0 = p8 현재 등록 런 = **stress-controlled servo** (fixed-platen hold 오기 · SEMV2-01) · p15 캡션 집단 정정 (왼쪽 G5a = 130 + 64 · 오른쪽 G3 = 130 · SEMV2-02) · P1 = p12 축 제목 두 줄 + 조건 캡션 3 줄 · p2 F1 상자 안 줄바꿈 · p5 notes E_VRH = Young's modulus (K/B0 별도) · p7 미확인 σy 범위 삭제 · 철회 이력 · 중복 → notes · p4 `[8]` = 방법 · σ₀ 1.5 = chosen reference · p14 소개 문장 축약.  selftest 에 `fixed-platen hold` · `σy 0.05–0.30` 금지 + p15 캡션 ↔ 집단 검사 추가 (v2 덱에서 실패 확인).  글 전문 = `slide_text_v2.md` (v2.1 로 갱신).
