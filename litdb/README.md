> ⚠ **이 브랜치(실험 파트) 안내:** 이 `litdb/`는 DEM/MPM 브랜치(`claude/stoic-knuth-NObVQ`)에서
> 이식된 문헌 지식베이스입니다. **건식 후막 bimodal 복합양극 실험** 작업에 그대로 활용하세요.
> 비교 기준은 **2개**: 실험 = `our_experiment_baseline.md`, 시뮬 = `our_dem_baseline.md`.
> 논문 에이전트(`../.claude/agents/litdb-curator.md`)가 두 기준 모두에 대해 비교합니다.
> 건식/후막/바이모달/단결정-다결정 관련 미digest 노트는 `../docs/lit_*.md` 에 다수 있음.

---

# 📚 LITDB — DEM+MPM ASSB 압밀·전달 문헌 단일 시스템

> **앞으로 (DEM/MPM/전달) 논문은 여기서만 본다.** 여러 곳(docs/lit_*.md, docs/literature_coverage/,
> docs/data/*.csv)에 흩어진 문헌을 한 곳에서 생각·참고·비교하기 위한 통합 MD 시스템.
> DFT 쪽 litdb(다른 브랜치)와 같은 형식 — 이쪽은 **DEM = 전달 / MPM = 역학** 프로젝트용.

## 폴더 구조
| 파일/폴더 | 역할 |
|---|---|
| `INDEX.md` | 전체 논문 마스터 표. "무슨 논문 있나" 한눈에. status ✅/⬜/📄 |
| `papers/<slug>.md` | **논문 1편 = digest 1개.** 표준 양식 = `papers/_TEMPLATE.md` |
| `our_dem_baseline.md` | 우리 DEM+MPM 기준값(E_eff 1.35/1.53, porosity 앵커, σ-삼중항 LOOCV) — 모든 비교의 기준점 |
| `comparison_vs_ours.md` | 문헌 ↔ 우리 DEM+MPM **차이 + 적용 인사이트** (축 A–F) |
| `data 동반` | 수치 CSV는 `docs/data/<slug>_*.csv` 에 (digest의 §3·§8이 링크) |

## 논문 "먹이는" 워크플로우  (= `litdb-curator` 에이전트)
**트리거: PDF 업로드 후 "논문 에이전트 실행해줘"** (또는 "이 논문 litdb에 넣어줘", "이 논문 정리해줘", "feed this paper")
→ 에이전트가 **(1) 백그라운드로 digest 저장** + **(2) 사용자에게 자세히·체계적으로 설명** + **(3) 질문 답변(토론)**.
digest 깊이 기준 = `papers/bazzoun2026_dem_fem_rnm_ionic.md` (논문 정독 수준, 분량 무관).
1. PDF 업로드 → 트리거 발화
2. 에이전트가 `_TEMPLATE.md` 양식으로 `papers/<slug>.md` 생성. 특히:
   - **시뮬레이션 방법** — DEM 접촉법칙·E·ν·μ·COR·bond / MPM 구성식·σ_y·grid·readout / 전달 솔버 /
     **입자 처리(구·형상, rigid vs CONTACT-소성 vs SHAPE-소성)**
   - **Figure set** — 각 그림이 무엇을 보여주나 + 우리가 참고할 점
   - **Post-processing** — Heckel/percolation/coverage/coordination/EIS-TLM 를 어떻게 적용·기록했나
   - **우리 DEM+MPM 대비** — 같은 점 / 다른 점 / 왜 (rigid·plastic, halide·LPSCl, 2D·3D)
   - **적용 인사이트** — 내 연구에 어떻게 쓰나
3. `INDEX.md` status → ✅, `comparison_vs_ours.md` 갱신
4. 사용자와 인사이트 공유 → 합의된 결론만 deck/paper로

## 통합 대상 (흩어져 있던 기존 DB → 점진 흡수)
- `docs/lit_varkey2026_multicontact_dem.md`, `docs/lit_bazzoun2026_dem_fem_rnm.md` (기존 한국어 노트 → papers/ digest로 흡수 완료)
- `docs/literature_coverage/pdfs/` : Bouvard2000, Martin-Bouvard2003, McGeary1961, So2021, Varkey2026, Bazzoun2026
- `docs/literature_coverage/` : contact_mechanics_db.json, coverage_db.json, packing_regime_db.json
- `docs/data/` : densification_porosity_db.csv, varkey2026_ionic_vs_pressure.csv, bazzoun2026_sigma_ionic.csv
> 흡수 원칙: 각 항목을 해당 `papers/<slug>.md`로 옮기고(또는 링크), 수치는 `docs/data/*.csv` 유지, INDEX에 status 표기.

## status 범례
✅ digest 완료 · ⬜ PDF만(미digest) · 📄 메타만

## 🗨️ Q&A 로깅 (recurring)
슬라이드·결과를 보며 나온 질문은 **해당 주제 MD의 "🗨️ Q&A 로그" 섹션**에 누적:
- 압밀/porosity·전달 일반 → `comparison_vs_ours.md`
- 특정 논문 관련 → 그 논문 `papers/<slug>.md` 의 §Q&A
**트리거: "Q&A 작성해줘"** → 직전 질문/답을 자동으로 해당 MD의 "🗨️ Q&A 로그"에 항목 추가.
