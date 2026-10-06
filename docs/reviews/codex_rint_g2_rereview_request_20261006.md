# Codex 재검토 요청 — Rint 2단계 (G2) 면적 규약 ①′ v3 (2026-10-06 밤)

- 직전 판정: Codex G2 (10-06 밤) = **설계 완결 HOLD** · 새 생산 P1 없음 · P2 6 · P3 4 (`docs/reviews/codex_review_rint_g2_design_20261006.md` · 증거 `docs/reviews/codex_rint_g2_design_review_evidence_20261006/` · 우리 트리 재현 숫자 키 87/92 비트 동일 · 나머지 5 = CG 끝자리).  원장 `RINTG-01`~`10` = Codex 표기 `RINTG2-01`~`10` (원장 ID 형식 때문).
- 검토 대상: 설계 v3 `docs/reviews/contact_resistance_pipeline_draft_v3_20261006.md` (**설계만 · 코드 변경 0** · v2 에 대한 개정판 — 정본 = v2 + v3, 겹치면 v3) — 이 요청서를 담은 커밋 (sha 는 1저자가 발송 때 적는다).
- 1저자 결정 (10-06 밤 · 권고대로 · CLAUDE.md Rint 절) — v3 가 그대로 적용: ID 대응 · RINTG-01 = 선택 (1) · 02 = 탄소가 덮은 막 = 면적 제거 (2 Ω) 기본 + 1 Ω 판 민감도 (물리 판단 추정) · 06 = L138 문턱을 D12 와 분리 · 10 = v1 본문 보존 + 배너 = 역사 처분 (정본 v2/v3).  v3 문서 자체의 지위 = v3 §0-2 (1저자 확인 전 초안 · 발송 = 1저자).

## 1. v2 → v3 (RINTG 별)

| 원장 (Codex) | 판정문 지적 | v3 의 답 (v3 §) | 닫힘 증거 (시험) |
|---|---|---|---|
| RINTG-01 (RINTG2-01) P2 | 순열 불변 σ 와 legacy OFF 비트 동일 충돌 (+4.740683 %) | 선택 (1): legacy OFF 비트 동일 유지 · 불변 주장 = 동결 sid · σ · BC 위 owner/support (+ owner/support 는 AM 마스크 · 입자 종류만 읽음) · raw σ 불변 주장 없음 · 중복 입자 거부 · ε_p tie · 실침대 순서 의존 크기 = 새 측정 항목 (§1) | `own_perm_frozen` · `raw_perm_legacy` (음성) · `off_bitid` · `reject_dup` · `raster_order_size` (열림) |
| RINTG-02 (RINTG2-02) P2 | 총량 정규화 ≠ 국소 막 연산자 (13.968136 %) · 탄소 가림 법칙 미정 | 생산 = **contact-normalized coarse closure (CNC)** 로 이름 · 시험 전용 **해상 기준 모형 (RRM)** 분리 · 원판 밖 support = 절단 (재구성 대안) · 막 OFF 우회 금지 · a < h 표지 · 탄소 = `remove_area` (2 Ω) 기본 · `renormalize` (1 Ω) 민감도 (§2) | `trace_jump_operator` · `disc_contact_coupled` · `carbon_cover_law` · `reject_film_off_outside` · `contact_model_bias` |
| RINTG-03 (RINTG2-03) P2 | E4 가 r′ 를 간선 저항처럼 씀 (25 배) · 다중 부류 적분 | E4′: 막 간선 저항 r′/h² · P_film,code = g_code·Δφ²·r′/(R_half + r′) · 물리 r_face/(h²·1e−8) · 직접 접합 R_j/1e4 분리 · Σ_c s_c 적분 · r = 0 · ∞ · σ = 0 상태 처리 · 해석 범위 (§3) | `class_sensitivity` (에너지 + FD) · `e4_printed_mutant` · `multiclass_integral` |
| RINTG-04 (RINTG2-04) P2 | T2-2 전역 차 → 0 이 막 삭제 오답도 통과 | 고정 상자/a h 수렴 먼저 · 상자 사다리는 β 또는 (k_eff/k_m − 1)/f · mutant 셋 실패 필수 · 내부 전위 동일 요구 안 함 (§4-1) | `sphere_film_fixedbox` · `sphere_film_boxladder` · `sphere_film_mutants` |
| RINTG-05 (RINTG2-05) P2 | 고정 ↔ 1.2h bridge 를 한 수렴 대상으로 | T3-D 이산화 (같은 모형 고운 기준) · T3-B 모형 편향 보고 (합격선 없음) · T3-P 1.2h 경로 별도 (§4-2) | `contact_discretization` · `contact_model_bias` · `bridge_scaled_path` |
| RINTG-06 (RINTG2-06) P2 | D12 결과 전/후 문장 공존 | D12-V (검증 봉인 · 결과 전) ↔ D16-dev (옛 L138 = 개발 산출 · 동결 픽스처 평가) · 독립 기준해 오차 + 관측 차수 · 단조 수렴 필수 아님 (§4-3) | 사전등록 · `seal_order` |
| RINTG-07 (RINTG2-07) P3 | ΣG_film 단위 | ΣG_film = 1e−8·A_true/r [S] 통일 (§3-1) | `units_atrue` |
| RINTG-08 (RINTG2-08) P3 | J2 괄호식 | J2a fiber–fiber · J2b fiber–sphere 분리 · J2c polyline · 순열 (§5) | `fiber_sphere_threshold` · `junction_polyline_split` · `junction_perm` |
| RINTG-09 (RINTG2-09) P3 | 직접 ↔ 면 "1e−12 일치" | 같은 리드 (0.0001 Ω) 를 넣어 비교 또는 막 성분만 (§3-3) | `units_direct_vs_face` |
| RINTG-10 (RINTG2-10) P3 | v1 본문 정정 완료 주장 · 비준 표지 충돌 | v1 = 본문 보존 + 배너 = 역사 처분 · 완료 주장 철회 · 비준 상태 = v3 §0-2 한 곳 (§6-8) | 문서 처분 (반입 때 v1 배너 정본 한 줄 · v2:L499 표지) |

판정문 §2 주의점 넷 (v3 §0-3): 중복 입자 거부 (N8) · 조인 관문 = 기하 대응 (G-geo) ↔ 같은 프레임 메타 (G-frame) 분리 + 다른 step 재사용 규약 · unresolved "제외 = fused" 금지 (③ 전 결정 D18 · N10) · `CONTACT_FREE` = 추가 계면막 없음 한정.
Q 답 반영 (v3 §0-4): Q1 이름 (청구자 제한 power 분할) · Q3 cut 문구 · 조건부 구간 · A_hi = 구간 최대 · Q4 J4 봉인 · Q5 J9–J12 · Q6 T2-1′ · Q7 해석 범위 · Q8 E6 tombstone · E7 · T0-6a/b · Q9 비교표 · Q11 `RINT-21` 문구 · Q13 순서 그대로.

## 2. 범위
- 구현 대상 = AM–AM 하나 (v2 그대로) · 섬유 (②) · SE (③) = 계약만 · ② 는 Q5 조건 등록 뒤 별도 심사.
- 이번 요청은 Q13 순서의 **2–3 단계 (반례 실패 시험 → AM–AM ①′ 구현 → T0 · T1 · N · T4) 시작** 판정이다.  ①′ 정량 **채택**은 D12-V 봉인 + T2 · T3 검증 (4 단계) 뒤.

## 3. 질문
- R1. RINTG-01 ~ 10 각각이 설계 수준에서 닫히는가 — 아니면 항목별 최소 해제 조건.
- R2. 이 v3 로 ①′ AM–AM 구현 (반례 실패 시험 먼저) 을 시작해도 되는가?  시작 전에 더 고정할 것이 있나?
- R3. (01) T0-1′ 팔 B (raw 순열에서도 owner/support 같음 · σ 는 비교 안 함) 가 선택 (1) 의 범위를 넘는 주장인가?  ε_p tie 와 중복 거부로 판정문 §2 의 tie 주의점이 닫히나?
- R4. (02) CNC 이름 · RRM 분리 · 원판 밖 절단 (D17) · `a_lt_h` / `unresolved_subgrid` 표지 · `remove_area` 의 N_c^0 (첨가제 덮어쓰기 전 support) 정의가 판정문 수정안 범위를 채우나?  탄소 경유 경로가 ② 전까지 막 없는 legacy 면으로 남는 것을 한계로 적는 것으로 충분한가?
- R5. (03) E4′ 표 · 상태 처리 · T0-3′/m/i 로 RINTG2-03 과 `RINT-16` 이 설계 수준에서 닫히나?
- R6. (04 · 05) T2-2a 의 정답 정의 (상자 경계 = 무한 매질 정확해 Dirichlet) 와 T2-2b 의 정규화 응답 · T3-D/B/P 분리가 희석 false pass 와 모델 ↔ 격자 혼동을 막나?
- R7. (06) D12-V 봉인 목록 (판별력 · CNC 편향 예산 포함) 과 D16-dev 분리가 충분한가?
- R8. (07–10) P3 정정과 v1 역사 처분 (+ 반입 때 배너 정본 한 줄) 이 RINTG2-10 과 `RINT-10` 의 남은 조건을 채우나?
- R9. v3 뒤 `RINT-06` · `08` · `09` · `16` 의 Q12 판정은 어떻게 바뀌나?

## 4. 숨기지 않는 것 (v3 §9 요약)
- 코드 · 원장 변경 0 · 시험 실행 0.  수치는 판정문 · `evidence.json` · 반입 README · v2 의 값뿐 — 손 유도 항등식 몇 개 (1/h² · Σ_c 적분 · 3β/(1 − βf) · 원판 면적 단조 범위 · tie 반올림) 만 scratchpad 에서 검산.
- **실침대 raster 순서 의존 크기 미측정** (T4-3 · 원장 `RINTG-11` · 숫자 없음) · CNC 편향 크기 미측정 · D12-V 숫자 없음 (1저자 · 실행 전).
- 탄소 가림 법칙 = 1저자 결정 · 물리 근거 자료 없음 (**추정**) — 두 판 값을 늘 함께 보고.
- 덤프 메타 (timestep · box · id) · scaffold 머리줄의 원 step · Phase A 킷 · ps45 5:5 덤프 가용성 · 생산 입력 순서가 바뀌는 경로 — **미확인**.
- 판정문의 "세 구 반례" 형상은 문서에 없어 T0-1′ 작성 때 고정한다.
- RRM 의 기울기 접점 가중은 D11 (T2 개발 결과) 에 기댄다 — T3-B 는 보고 전용이라 판정 순환은 아니라고 보았다 (추정).
- ⑤ 짝 (접촉망 세대 2) 은 재검증도 HOLD — ⑤ 는 GO 뒤.  litdb 재검색 안 함 · 재료값 `[미확인]`.
