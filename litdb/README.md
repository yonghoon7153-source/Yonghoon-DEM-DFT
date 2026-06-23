# 📚 LITDB — Argyrodite SE 문헌 단일 시스템

> **앞으로 논문은 여기서만 본다.** 여러 곳(db/literature, kb/papers, db/properties, Excel)에 흩어진 문헌을 한 곳에서 생각·참고·비교하기 위한 통합 MD 시스템.

## 폴더 구조
| 파일/폴더 | 역할 |
|---|---|
| `INDEX.md` | 전체 논문 마스터 표 (Excel 자동 생성). "무슨 논문 있나" 한눈에. |
| `papers/<slug>.md` | **논문 1편 = digest 1개.** 표준 양식 = `papers/_TEMPLATE.md` |
| `our_dft_baseline.md` | 우리 comp1/modelc DFT 기준값 — 모든 비교의 기준점 |
| `comparison_vs_ours.md` | 문헌 물성 ↔ 우리 DFT **차이 + 적용 인사이트** |
| `properties/*.md` | 물성별 교차표 (ionic / oxidation / mechanical / electronic) |

## 논문 "먹이는" 워크플로우  (= `litdb-curator` 에이전트)
**트리거: PDF 업로드 후 "논문 에이전트 실행해줘"** (또는 "이 논문 litdb에 넣어줘", "이 논문 정리해줘", "feed this paper")
→ 에이전트가 **(1) 백그라운드로 digest 저장** + **(2) 사용자에게 자세히·체계적으로 설명** + **(3) 질문 답변(토론)**. digest 깊이 기준 = `papers/zuo2022_chlorination_cathode_interface.md` (논문 정독 수준, 분량 무관).
1. PDF 업로드 → 트리거 발화
2. 에이전트가 `_TEMPLATE.md` 양식으로 `papers/<slug>.md` 생성. 특히:
   - **DFT 방법** — code·functional·pseudo·k-points·supercell·U·vdW·무질서 처리
   - **Figure set** — 각 그림이 무엇을 보여주나 + 우리가 참고할 점
   - **Post-processing** — 어떤 후처리(NEB/Bader/COHP/grand-potential…)를 어떻게 적용·기록했나
   - **우리 DFT 대비** — 같은 점 / 다른 점 / 왜
   - **적용 인사이트** — 내 연구에 어떻게 쓰나
3. `INDEX.md` status → ✅, `comparison_vs_ours.md` · `properties/` 갱신
4. 사용자와 인사이트 공유 → 합의된 결론만 deck/paper로

## 통합 대상 (흩어져 있던 기존 DB → 점진 흡수)
- `db/literature/` : argyrodite_computational_littable.csv, argyrodite_dft_littable.csv, refs.json, 개별 MD 7편(damore/fadillah/lee/li/pustorino/sundar/zhao)
- `db/properties/` : **literature_tensions_audit.json**, oxidation_stability.json, electronic/elastic/eos/diffusion.json
- `kb/papers/` : verified_refs_2026_05.md, computational_methods_draft.md, narrative_with_literature_steps.md …
> 흡수 원칙: 각 항목을 해당 `papers/<slug>.md` 또는 `properties/*.md`로 옮기고, 출처 파일은 INDEX에 "통합됨"으로 표기.

## status 범례
✅ digest 완료 · ⬜ PDF만(미digest) · 📄 Excel 메타만
