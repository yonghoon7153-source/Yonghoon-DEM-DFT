# ⤳ (통합됨) 양수영 BML 세미나 → `yang2026_ncm_radial_microstructure_ml`

> **이 slug 는 더 이상 정본이 아니다.** 같은 발표(양수영, 한양대 BML, 2026-08-18
> "Multiphysics and machine-learning-guided design of radial cathode microstructures")를
> **두 세션이 병렬로 digest 해서 파일이 둘**이 됐다. 한 발표에 digest 가 둘이면 인덱스와
> 인용이 갈라지므로 **하나로 합쳤다** (2026-08-25).
>
> ## → 정본: **`litdb/talks/yang2026_ncm_radial_microstructure_ml.md`**

## 왜 그쪽이 정본인가

1. **슬라이드 21장 전부 렌더 + 13장 이미지 실판독** (`litdb/figures/yang2026_ncm_radial_microstructure_ml/`).
   이 파일에는 그림이 0장이었다 — 축·단위·마커 위치를 그림으로 확인한 기록이 없다.
2. **`figure-read ≈` 규율** — 그림에서만 읽은 값과 덱 본문 명시값을 분리 표기.
3. **1저자가 요청한 slug 패턴** `<저자><연도>_ncm_radial_microstructure_ml` 과 일치.
4. **`axis: dem-microstructure` 태그**가 있어 `tools/litdb/build_index.py` 가
   `INDEX_DEM.md` 🎤 발표 덱 절에 자동 편입한다 (이 slug 는 태그가 없어 어느 인덱스에도 안 잡혔다).

## 이 파일에만 있던 내용은 어디로 갔나

**전부 정본 §21 "중복 digest 통합 기록" 으로 흡수했다** (방법론 6건):
대리모델 상한 = 시뮬레이션 수치 재현성 · 규칙기반 생성기(딥러닝 아님) · 근사 SHAP 의 분산 미보고 ·
hypervolume 기준점 · 최적화기의 경계 밖 선호 · TabPFN 배포 의존성.

⚠ 다만 **흡수하지 않은 것 2건**을 남긴다 (정본 §21 말미에 사유 기록):
- `scripts/ml_shap_pareto.py` (selftest 31/31) + 웹앱 라우트 `/predictor/structure/shap`·
  `/predictor/structure/pareto` **"이식 완료"** 주장 — **이 브랜치에 그 파일이 없다**
  (git 이력에도 없음, 2026-08-25 확인). 다른 워크트리 진행분으로 보인다. 확인 전 인용 금지.
- `claims.json CL-41` 포인터 — `db/knowledge/fairchem/claims.json` 에서 찾지 못했다.

⇒ **그 두 건이 실재한다면 이 stub 을 지우지 말고 정본 §21 에 검증 결과를 추가**하면 된다.
원본 전문은 git 이력에 남아 있다 — `git show 79f3e365:litdb/talks/yang2026_bml_ml_radial_cathode.md`.

## 인용 규율 (정본과 동일)

⛔ **수치 인용 전면 금지** — L&F 제공 소재 · 미출판 · **회사가 출판에 반대**.
축은 **DEM/미세구조 (sub-particle)**, 대조는 `litdb/comparison_vs_ours_DEM.md` §G.
cascade(DFT 축) 방법론 이전분은 `kb/methodology/microstructure_ml_transfer_to_cascade_2026_08_25.md`.
