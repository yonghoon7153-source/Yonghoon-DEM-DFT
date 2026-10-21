## 4. 요청서 · 증거 README · 원장의 수 ↔ 실행 출력 (SELF-124 · 이 컨테이너 · 실물 자리 = 작업 트리에서 그 판의 도구 · 두 등록 바이트로 잠시 바꿔 `python3 -I -B scripts/supp20_input_receipt.py --selftest` · p07)

| 주장 (자리) | 실행 출력 (p07 · 경우 이름) | 판정 |
|---|---|---|
| 고치기 전 판 · 지금 (비준 전) 문서 = 122/122 (Q5 · README §3 · 원장) | `old_pending_docs` 122/122 rc 0 · 상태 pending | 같음 |
| 고치기 전 판 · 비준 사본 = 121/122 · 실패 S0b (§0 · Q5 · 묶음 §1-3) | `old_ratified_docs` 121/122 · [S0b] · registered | 같음 |
| 고치기 전 판 · 194 만 비준 = 122/122 (Q5 *"옛 판은 … 통과"*) | `old_194_only_ratified` 122/122 rc 0 · pending | 같음 |
| 새 시험 + 옛 S0b 식 = 122/123 (S11g) · 121/123 (S0b · S11g) | `oldexpr_pending_docs` 122/123 · [S11g] (registered · pending 꼴 = 거짓) · `oldexpr_ratified_docs` 121/123 · [S0b · S11g] — 옛 식 판은 우리가 다시 만들었다 (`s0b_fp` 몸만 옛 식 · README 의 sha256 `a06d4298…` 판과 바이트는 다름) | 같은 수 |
| 고친 판 = 123/123 (pending · 비준 둘 다 · 비준 커밋 트리도) | `new_pending_docs` 123/123 · `new_head_ratified` 123/123 · `new_ratify_commit_docs` 123/123 (35–41 s) | 같음 |
| 새 엄격 — 보충만 · 194 만 비준 = 122/123 (S0b) | `new_supp_only_ratified` 122/123 [S0b] (registered) · `new_194_only_ratified` 122/123 [S0b] (pending) | 같음 |
| 변이 넷 m1–m4 = 넷 다 122/123 · S11g (m1 · m2 = 비준 전 문서 · m3 · m4 = 비준 커밋 트리) | HEAD 문서 m1–m4 = 각 122/123 [S11g] · 비준 전 문서 m1 · m2 = 각 122/123 [S11g] · 잡은 꼴 ⟪p07b full⟫ | 같음 (+ 다른 상태에서도) |
| 최상위 문 59 · 바뀐 것 `_selftest` 하나 (§2 · 부록 A · 원장) | p03: 59 = 59 · `['_selftest']` | 같음 |
| 컨테이너 영수증 rc 0 · 실패 칸 없음 · 11 칸 (§0 ② · 부록 A) | p05: `receipt 0 [] 11` | 같음 |
| 비준 전 문서 영수증 rc 1 [D1] (Q1) | p08: rc 1 · [D1] · 11 칸 | 같음 |
| 영수증 selftest 35 s · reread ✓ 29 · ✗ 0 (12 s) · 실행기 139/139 · check_doc_refs · check_review_findings · check_method_discipline 0 오류 (15 경고) (§4) | ⟪p14⟫ | ⟪⟫ |
| 환경 Python 3.11.15 · NumPy 2.4.6 · SciPy 1.17.1 · networkx 3.6.1 (§6) | p08: 같음 | 같음 |
