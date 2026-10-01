---
source_url: https://github.com/pybamm-team/PyBaMM/releases/tag/pybamm-v26.9.0.0
ingested: 2026-10-01
sha256: 86f6a7c995c652b4937fb236e743f0f0d838a80de0f1308978bfe62922f95558
---

수집 목적: (1) 의존성 위험 감시 — 우리가 쓰는 도구(PyBaMM 등) 릴리스가 합성 truth·재현성에 주는 영향 판정 · (2) 방법 비교·경쟁 도구 — OCV/DVA 피팅 도구를 degeneracy 질문과 비교 · (3) 미세단락 도구 탐색 · (4) 실험 아이디어 저장 (착수는 별도 승인). 2026-10-01 사용자 결정 — 앞으로 매일 오는 브리핑의 처리 기준.

# GitHub 연구 브리핑 — 2026-10-01 (일일 브리핑 첫 회 · 사용자가 채팅으로 전달한 원문)

피카! ⚡ 10월 1일 GitHub 연구 브리핑이에요. 첫 회라 초기 후보 3개를 골랐어요

1. PyBaMM — 열화 모델 업데이트 확인용
9월 28일 공개된 26.9.0.0에서 반쪽전지의 리튬 재고 손실(LLI) 계산과 비균일 격자의 리튬 보존 문제가 수정됐어요. 기존 모델로 열화를 해석하신다면 버전 비교 가치가 있어요. 실제 데이터에서 원인을 자동 판별하는 도구는 아니며, ASSB 적용은 별도 검증이 필요해요. 릴리스 watch 후보로 추천해요
[릴리스·변경사항](https://github.com/pybamm-team/PyBaMM/releases/tag/pybamm-v26.9.0.0) https://github.com/pybamm-team/PyBaMM/releases/tag/pybamm-v26.9.0.0
2. PyProBE — LLI/LAM 정량화에 가장 직접적인 후보
전극 OCP와 전지 OCV·ICA·DVA를 맞춰 전극 용량과 리튬 재고를 추정해요. 예제와 합성 데이터 복원 테스트가 있어 열화 정량화 출발점으로 좋아요. 다만 적합도가 좋다고 미세단락까지 입증되는 건 아니에요. 분석 흐름을 직접 수정할 계획이면 fork 후보예요
[저장소](https://github.com/ImperialCollegeLondon/PyProBE) · [OCV 피팅 예제](https://pyprobe.readthedocs.io/en/latest/examples/ocv-fitting.html)https://github.com/ImperialCollegeLondon/PyProBE, https://pyprobe.readthedocs.io/en/latest/examples/ocv-fitting.html
3. 오늘의 작은 검증 제안 💡
PyProBE로 초기·열화 전지의 저율 곡선 한 쌍을 OCV와 DVA 방식으로 각각 피팅하고, 평활화·피팅 범위를 바꿔도 LLI/LAM 결론이 유지되는지 비교해 보세요. 미세단락 판단 전, 열화 추정 자체의 안정성을 확인하는 실험이에요
세 후보 모두 허용적 라이선스와 공개 예제·테스트를 확인했지만 직접 실행하진 않았어요. 이번 조사에서는 바로 신뢰할 만한 미세단락 전용 분류기를 찾지 못했고, 기존 보유 저장소와의 중복 여부도 확인하지 못했어요

---

## 수집 시 1차 대조 (2026-10-01 · WebFetch — 페이지를 작은 모델이 인용·요약한 결과이므로 원문 그대로라고 보장하지 않는다)

릴리스 페이지 https://github.com/pybamm-team/PyBaMM/releases/tag/pybamm-v26.9.0.0 에서 인용된 항목:
- Breaking: "`pybamm` now requires `pybammsolvers>=0.10.0`, because `IDAKLUSolver` uses IDAKLU" features (#5783) · "Bumped the pinned CasADi version from 3.7.2 to 3.8.1" (#5761)
- "`BasicDFNHalfCell` and `BasicDFNComposite` now keep the migration term `t_plus * i_e / F` inside the electrolyte flux" (#5745)
- "Positive half-cell electrolyte lithium, total-lithium losses, and electrolyte-inclusive LLI now use only the electrolyte domains present" (#5765)
- "`FiniteVolume` node-to-edge shifts now use the true node spacing instead of weights that assume a uniform mesh" (#5755)
- "Per-phase `"particle mechanics"` options now set the mechanics submodel of each phase" (#5694) · "The irreversible, reversible and hysteresis heat sources now sum over every particle phase" (#5770) · "`"open-circuit potential"` stays a plain string when it is left at its default" (#5770)
- (요약기가 날짜를 "September 28, 2024" 로 옮겼다 — 버전 번호 26.9 와 맞지 않아 연도는 신뢰하지 않는다)

PR https://github.com/pybamm-team/PyBaMM/pull/5755 에서 인용된 항목:
- 제목 "Use true node spacing for finite-volume node-to-edge shifts"
- 동기: node-to-edge 행렬이 "hard-code weights that assume uniformly spaced nodes" ([0.5, 0.5] 내부 · [1.5, −0.5] / [−0.5, 1.5] 외부). ORegan2022 가 Exponential1DSubMesh + 농도 의존 확산에서 "gains 26 % of its particle lithium over three 1C cycles".
- 범위: 변경은 "reduce to the old hard-coded values on a uniform mesh, so uniform-mesh results are bit-for-bit unchanged".
