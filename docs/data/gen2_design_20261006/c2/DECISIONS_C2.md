# C2 설계 요약 (Physics 접촉면적 묶음 · 에이전트 10-06 저녁 · 리포 무수정) — 1저자 결정 대기
근거 = real_14 (접촉 106,563) · case15 (182,995) 커밋 덤프 + 합성 쌍 · HEAD 재계산 비트 동일 · 제안 함수 designC2/proposed_film_area_g2.py

| 결정 | 항목 | 권고 | 근거 · 영향 |
|---|---|---|---|
| ① | L1-02 겹침 부피 | 정확 lens (lens_volume) | 옛 V 식 = lens 의 0.49 배 · δ .95 에서 음수. σ −0.04~−0.23 % |
| ② | L1-01 상·하한 충돌 | 규칙 B: A = max(A_disc, min(A_Tabor, V_lens/h, cap)) | 규칙 A 는 SE–SE 22.8 % (c15 49.7 %) 를 원판 아래로 · 비단조 7/7 · 이온 −9.6/−49.7 %. 규칙 B 연속 · 단조 7/7 |
| ②b | floor | = 원판 c_cpl[22] (= Hertz 모드 면적) | ⇒ 간선마다 R_c(Physics) ≤ R_c(Hertz) 불변식 (real_14 위반 0). πR*δ floor 면 이온 −9.3 % · 불변식 소멸 |
| ③ | L1-03 쌍별 E* | SE–SE 13.19 · AM–SE 22.41 GPa · AM–AM = 원판 + 'native_unsupported_pair' | σ 주효과: g2 = ψ곱셈 대비 이온 −15 % · 전자 −38 % · 열 −17 % (real_14) |
| ④ | L1-08 h_film 5 nm | 값 유지 + [미확인] 표지 | h 1–10 nm 에서 σ 6 자리 동일 · 20 nm −2.8 % · 50 nm −10 % |
| ⑤ | SELF-28 floor (ψ<1e-4 → R_c 0) | 동결 유지 (곱셈에선 연속 끝점) | floor on/off |Δσ|/σ ≤ 6.6e-7 |
| ⑥ | LHS-25 Coverage 분모 · 100 % 클립 | 합집합 cap 피복 (*_physics_union 새 키) | **Coverage 를 바꾸는 유일한 수정**: real_14 51.5 → 43.2 % (×0.84) · c15 ×0.87 ⇒ 덱 5장 Tabor 보정 48.9–63.4 % → 약 41–55 % (추정 · W-contact 필요) · 커밋 B (망과 독립) |
| ⑦ | LHS-26 rough 모양 인자 | HOLD | SF 값 자체가 가정 |
- DESC-03 (단위 1000 배) · DESC-10 (옛 V 경로 활성화) = ①②③ 와 같은 커밋으로 g2 함수 안에서 닫힘 (결정 불요)
- 종합 (real_14): v1.2 부록 세대 → ψ 곱셈 + g2: 이온 σ ×1.23–2.10 ⇒ tau2_ion_physics ×0.48–0.81 · 전자 ×1.97–2.32 · 열 ×1.80–1.90
- ⚠ 곱셈 + g2 뒤 Physics T<1 대량 예상: LHS 0–7/106 · LHSx 30–59/64 (외삽) — C1 의 CF bulk 수정 (TAU-07/08) 과 얽힘
- ⚠ 세대 3 (오늘 아님): Tabor 계산용 real-E 재구성 힘이 DEM 자신의 힘의 2.5–3.2 배 (SE–SE ×4.9 · AM–SE ×6.6 중앙) — DEM 힘을 쓰면 SE–SE 100 % floor · σ_ion −11 %. 모형 선택 → Physics 부록 opt-in 유지 + 한정어
- 덱 영향: 8 장 Physics σ 곡선은 세대 1 값 (지금 Hertz 아래) → 세대 2 에선 Hertz 위로 뒤집힘 · 5 장 Coverage (Tabor 보정) 은 ⑥ 에서만 바뀜
- 구현 순서 권고: 결정 ①②②b③④⑤ → 커밋 A (시험 T1–T9 먼저 · film_area_g2 · build_network µm + pair · area_rule_physics='physics_g2' · tau_flux/인계 생성기가 psi + area_rule 둘 다 확인 · 웹앱 같은 묶음 · 재봉인) → W-net 194 → 부록 세대 2 → Codex. 커밋 B (합집합 피복) → W-contact.
