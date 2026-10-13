# Codex 요청 — [연구세미나 덱] v3 "보는 판" 재확인 (장 문법 교체 · 압축 · 믹서 3 장 · 그림 재작성 · 2026-10-13 밤 · 발송 = 1저자)

> **한 줄**: v2.1 (조건부 GO 의 P0 둘 · P1 다섯 반영 · `codex_seminar_deck_v2_1_closure_request_20261013.md`) 뒤에 1저자가 **발표물의 모양**을 바꾸라고 지시했다 — 10-13 연구세미나 덱 4 장의 문법 (한 줄 제목 + 소불릿 ≤ 2 · 핵심어 빨강 · 그림 한 띠 · 우상단 출처 줄 · 꺾쇠 캡션 없음), 3D 그림 위주, 앞 15 장 → 10 장 압축, 믹서 3 장을 Plan 앞에 따로, 믹서 팔 코드 금지 · 분야 용어.  **값 · Codex 가 닫은 문장은 그대로** (자리만 옮기고 notes 에 전문).  확인할 것 = 옮기면서 뜻이 바뀐 곳이 있는가 · 새 그림 10 이 정본값인가 · 믹서 3 장의 등록 범주 · 한정어 문구 · 판정.  새 시뮬레이션 · 새 계산 없음.  검토 핀 = 이 요청서가 든 커밋.

## 1. v2.1 → v3 장 대응

| v3 | v2.1 | 무엇이 바뀌었나 (값 · 닫힌 문장은 불변) |
|---|---|---|
| 1 | 1 | 표지 (날짜 공란) |
| 2 | 2 | 흐름도 = PPT 도형 (글은 F1 그림과 같음 · SEM-01 · SEMV2-04 문구 그대로) |
| 3 | 3 | 3D 네 단계 (리포 PNG) + porosity 다섯 값 재작성 (G1 union) — 불릿 둘 그대로 |
| 4 | 4 | 수송 tortuosity · σ(Li⁺) 두 패널 재작성 (y 축 0 부터 → "truncated" 조건 불필요) + Bazzoun 2026 Fig. 2 크롭 [8] — 불릿 둘 (SEMV2-07 문장) 그대로 · 전류 경로 빈 자리는 7 장으로 |
| 5 | 5 + 6 | 제목 한 줄 `Fixed-shape DEM limits and the material point method (MPM)` · 불릿 1 = 5 장 첫 불릿 그대로 · 불릿 2 = 6 장 두 문장 이어 붙임 (MPM 매개변수는 6 장 표로) · **notes 로**: 감쇠 58 % 문장 (DEMP-01) · 문헌 22 편 집계 · Luding 2008 Fig. 1 크롭 [1] · 오른쪽 빈 자리 = MPM 3D (1저자 캡처) |
| 6 | 7 + 8 | 불릿 1 = 7 장 문장 · 불릿 2 = 8 장 첫 문장 (SEM-02 최소안) · 입력 다섯 행 = **표 도형** (22 GPa [8] · 1.35 · 1.53/0.49/0.30 · K 25.5 ≈ 26.2 · 보정 표적 10 % 미발표 · 검증 pending) · 하단 `Tested alternatives …` 그대로 · **notes 로**: 스캐폴드 상태 3 행 전문 (`Current registered runs: DEM-seeded SE, stress-controlled servo — f = 0 completed; f(a) execution failed` 등 · SEMV2-01 문구) · So 2021 Fig. 4a 크롭 [9] |
| 7 | 9 + 10 | 불릿 1 = 9 장 두 번째 문장 (SEM-08) 그대로 · 불릿 2 = 첨가제 세 가지 + 104 팔 72/72 (10 장 두 문장 축약 · 값 불변) · σ(e⁻)–VGCF 세 복셀 재작성 (G6) · 왼쪽 빈 자리 = 3D 전류 흐름 (접촉망 · 복셀 · 1저자 캡처) · **notes 로**: 유한체적 문장 · 첨가제 모식도 둘 (생산 스탬프 아님) = 삭제 |
| 8 | 11 + 12 | 세 패널 한 그림 (a 격자 비 CL-24 · b 모델 ↔ DC 분극 · c ps45 σ_e 인자 끔) · 불릿 = 11 · 12 장 문장 그대로 (SEM-03 · SEM-09) · 해석 조건 (SEMV2-03 세 줄) = 그림 아래 한 줄 |
| 9 | 13 | 누적 막대 재작성 (plane_load.json `contribution_sigma_zz_pct` 세 몫) + SE σ_VM 4 단계 — 불릿 둘 (SEM-04) 그대로 |
| 10 | 14 + 15 | 상태표 다섯 행 = 표 도형 (SEM-05 · 06 문구) + R/Q 정의 줄 · 산점 두 패널 재작성 (배포 v1.2 CSV 직접 — a 130 + 64 · × 비관통 24 · b 130) · 해석 줄 = SEMV2-02 집단 · **notes 로**: 퍼콜레이션 106/130 · 1.3–4.2 문장 |
| 11 | 새 | **Mixing 1** 층상 캠페인 — 등록 범주 (`registered "no segregation" category` · `not "no effect"` · 방향 · 크기 미해상) · 열 런 M 막대 (G7 = mixer_final10) · 계약 한정어 (1 % 겹침 미충족 · 진단) · 숫자 (Δ · SE · 칸 셋) = notes · 오른쪽 빈 자리 = 층상 침대 전 · 후 |
| 12 | 새 | **Mixing 2** 점착 탐색 — ΔM 막대 (dev-rot · dev-bo · dev-u · 칸 셋 · QC 미달 빗금) · 한정어 (one seed · post-hoc · wall adhesion 공동 · no verdict) · 숫자 = notes · 오른쪽 빈 자리 = 침대 스냅샷 |
| 13 | 새 | **Mixing 3** 표면 에너지 — SE–SE 군집 분율 (dev-u §3 · 범위 수염) + 접착일 도식 (논지 §2-2 `ΔW = 2(√γ_A − √γ_S)² ≥ 0`) · 비율 미지 · 확인 18 런 HOLD |
| 14 | 16 | Plan 그대로 |
| 15 | 17 | Summary + Mixing 한 줄 |
| 16 | 18 | References 16 불변 |
| 17 | 19 | Thank you |

- 믹서 용어 = 분야 표준 · 팔 코드 (내부 식별자) 없음 — selftest 가 본문 · notes 를 함께 검사한다.  팔 이름 = `no cohesion (control)` · `NCM–NCM cohesion removed` · `reference cohesion` · `lower cohesion (three levels)` · `NCM–NCM ×10 / ×30` · `all pairs ×10 / ×14`.
- 그림 10 = `docs/seminar_20261013/figs_v3/make_seminar_figs.py` (`--selftest` = 정본값 대조 · 철회값 0 · 팔 코드 0 · 조성 라벨 5).  문헌 크롭 3 = litdb 정본 브랜치 `litdb/figures/` 에서 빌드 때 받는다 (리포 사본 없음).  Lee 2025 크롭 = 자리가 없어 미배치 (1저자 결정 대기).
- 단어 수 (장 위 · 출처 줄 · 꼬리표 · 표 제외): p02 87 · p03 98 · p04 86 · p05 87 · p06 52 · p07 79 · p08 98 · p09 76 · p10 77 · p11 100 · p12 87 · p13 110 · p14 74 · p15 56.
- 생성기 selftest (고치기 전 = v2.1 덱에서 실패 확인): 17 장 · 꺾쇠 캡션 0 · 빈 자리 4 장의 출처 줄 `figure: presenter` · 출처 줄 ≤ 110 자 · 제목 한 줄 · **겹침 검사** (본문 바닥 추정 (Calibri 폭 = Carlito 로 줄바꿈 측정) ≤ 그림 띠 윗선) · 단어 ≤ 100/120 · bullet ≥ 15 pt · 해석 줄 ≥ 12 pt · 10 장 해석 줄 ↔ 집단 · 11 장 등록 범주 문구 · 금지 문구 (v2.1 목록 + `real coating effect` · `Figure pending`).
- 렌더 (LibreOffice · Carlito) 17 장 겹침 0 — 동봉 PNG.

## 2. 확인 요청

- **Q-V3-1** 대응표의 "그대로" 문장이 실제로 그대로인가 · 이어 붙인 둘 (5 장 불릿 2 · 7 장 불릿 2) 에서 뜻이 바뀌지 않았는가.
- **Q-V3-2** 새 그림 10 의 값 ↔ 정본 (특히 F_dataset = 배포 CSV 직접 · F_load = plane_load.json · F_mix1 · F_mix2 · F_mix3 = 믹서 기록) · 축 · 라벨 · 글씨 크기.
- **Q-V3-3** 믹서 3 장 — 등록 범주 문구 · 계약 한정어 · 개발 자료 한정어 (one seed · post-hoc · 공동 개입 · no verdict) 가 화면에 충분한가 · 분야 용어가 맞는가 (cohesive / non-cohesive · Bond number · Lacey index) · 논지 도식 문구.
- **Q-V3-4** notes 로 옮긴 문장 (5 · 6 · 7 · 10 장) — 화면에서 빠져도 되는가 · 다시 올릴 것이 있는가.
- **Q-V3-5** 판정 — **GO / 조건부 GO / NO-GO** · 남은 P0/P1/P2 를 장 · 요소 · 구체 수정으로.

고정 조건 = 앞 요청서들 §3 그대로 (표지 날짜 공란 · 빈 자리 4 = 1저자 웹앱 캡처 · 값 · 재사용 그림 불변 · hold 값 없음 · 참고문헌 16).  회신 = 한국어 · 장 위 문구만 영어 · 리포 수정 없이 판정문 하나 (우리가 반입).

## 3. 동봉 (ZIP v6)

`seminar_20261013_v3.pptx` + 그 파일에서 내보낸 `seminar_20261013_v3.pdf` · `render/p-01…17.png` + `contact_sheet.jpg` · 리포 `docs/seminar_20261013/` (생성기 v3 · `figs_v3/` · `slide_text_v3.md` · `slide_sources_v3.json` · README) · 문헌 크롭 3 (`lit/`) · 이 요청서.
