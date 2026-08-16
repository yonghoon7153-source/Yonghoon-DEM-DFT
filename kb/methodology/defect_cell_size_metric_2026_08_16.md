---
title: 점결함 셀 크기의 정본 지표 — λ₁(최단 격자 병진), 면 높이 아님
date: 2026-08-16
updated: 2026-08-16
tags: [neb, sei, cell-size, finite-size, md, methodology, correction]
status: 확정 — Codex 리뷰 P0 로 지표 정정, 도구 6건 반영
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-16
verifiedBy: Codex 동결 리뷰 + 우리 repo 데이터 독립 재현 (3셀 λ₁ 일치)
explored: false
authoredBy: agent
effort: high
claimType: methodological
evidenceScope: multi-source-primary
---

## 요약

**점결함의 최근접 주기 이미지 거리는 λ₁ = min |n₁a + n₂b + n₃c| (최단 비영 격자 병진)이다.**
면 높이 `V / |aⱼ × a_k|` 는 격자 **평면** 사이 거리라 슬랩 분리에나 맞는 양이고,
점-이미지 거리가 아니며 basis 의존이다. fcc 에서 **1.22배** 차이나고, 그 차이가 판정을 뒤집는다.

| 셀 | 면 높이 | **λ₁** | min_l 10 Å |
|---|---|---|---|
| Li₃Nd 2×2×2 | 8.469 | **10.372** | ✅ 통과 |
| Li₃Nd 3×3×3 | 12.703 | **15.558** | ✅ |
| Li₂S 3×3×3 | 9.880 | **12.100** | ✅ 통과 |
| lpsocl MD 1×1×1 | 5.672 | **6.940** | — |

## 내가 틀린 경위 (2026-08-16 하루에 두 번)

1. **오전**: lpsocl MD 셀의 유한크기 여유를 `|a| = 6.948` 로 계산 → MSD/한계 **2.14×**.
2. **오후**: "삼방정계라 `|a|` 가 아니라 수직 폭이다" 라며 면 높이 5.672 로 **정정** → **3.21×**.
   같은 논리로 SEI NEB 셀도 다시 재서 *"Li₃Nd 8.47 · Li₂S 9.88 — 둘 다 10 Å 미달"* 이라 적고,
   `build_neb_inputs.py --min_l` 의 기본 기준을 면 높이로 바꿨다(`eeacc989`).
3. **Codex 리뷰**: 면 높이는 점-이미지 거리가 아니다. λ₁ 로 재면 **둘 다 통과**다.

→ **첫 숫자(2.14×)가 맞았고 "정정" 이 오답이었다.** `|a|` 를 쓴 건 우연히 맞은 것이지만
(fcc·이 셀들에서 `|a|` ≈ λ₁), 이유가 틀렸으므로 지표를 명시적으로 λ₁ 로 못박는다.

### 왜 헷갈렸나

두 양이 재는 대상이 다르다:

- **면 높이** = 격자 평면 사이 거리. **슬랩/표면**에서 진공층이나 슬랩 간 분리를 잴 때 맞다.
- **λ₁** = 최단 격자 병진. **점결함·확산 이온**의 자기 이미지가 여기 놓인다.

비직교 셀에서 면 높이 < λ₁ 이므로 면 높이는 **보수적 하한**으로는 쓸 수 있다.
다만 "실제 이미지 거리" 라고 부르면 안 되고, 그 이름으로 셀을 키우면 낭비다.

## 파급 — 셋 다 정정했다

| 대상 | 잘못된 서술 | 정정 |
|---|---|---|
| `build_neb_inputs.py --min_l` | 기본 기준 = 면 높이 | **λ₁** (배수를 키우며 탐색 — λ₁ 은 배수의 단순 함수가 아니다) |
| SEI 셀 적정성 | "Li₃Nd·Li₂S 둘 다 10 Å 미달" | **둘 다 통과.** 옛 `--min_l`(벡터 길이)이 사실상 맞았다 |
| lpsocl MD | MSD/한계 3.21× | **2.14×** — 여전히 초과라 3×3×1 확대는 유효 (0.24× 로 내려감) |

⚠ **셀 게이트 통과 ≠ 셀 수렴.** λ₁ ≥ 10 Å 는 한 셀에서의 최소 요건일 뿐,
장벽이 셀 크기에 수렴했다는 증거가 아니다. 유전·탄성·금속 장거리 응답은 별도 수렴 시험이 필요하다.

## db 지위를 넷으로 쪼갰다

`sei_neb.json` 의 `citable` 하나가 서로 다른 넷을 뭉치고 있었다:

```
path_numerically_valid    계산 자체가 유효한가 (CI·대칭·경로 수렴)
cell_size_gate_pass       λ₁ ≥ min_l 을 통과했는가        ← 한 셀의 최소 요건
cell_convergence_status   untested|tested|converged      ← **다른 셀에서 재봤는가**
absolute_citable          실험·문헌과 나란히 놓아도 되는가
```

**Li₃Nd 0.229 eV 는 `citable: true` → `false`, `scientific_status: provisional_single_cell`.**
값은 보존한다. 허용 문장은 여기까지다:

> For the ordered metallic Li₃Nd 2×2×2 model, the neutral-vacancy c→c CI-NEB barrier
> is 0.229 eV **under this finite-cell protocol**.

수렴된 Li₃Nd 고유 물성이나 상간 순위로 승격할 근거는 아직 없다.

⚠ `collect_neb.py` 에 **이월 로직**을 넣었다 — 사람이 정한 지위(`cell_convergence_status`·
`scientific_status` 등)를 자동 회수가 덮지 않는다. 오늘 아침 같은 파일에서 자동 회수가
`0.229` 를 통째로 날린 사고가 있었고, 형태만 바꿔 재발할 수 있는 구조였다.

## 같이 닫은 도구 결함 6건

| # | 결함 | 영역 | 조치 |
|---|---|---|---|
| ① | symmetry gate **fail-open 2건** — `sym=False` 를 에너지 축퇴로 뒤집음 · 실행 중 끝점 허용 | 전제 검증 | 3분기 규칙: `False`→무조건 거부 · `True`→통과(에너지 불일치는 **conflict**) · `None`→**완료·수렴** 끝점에서만 축퇴 후퇴 |
| ② | 중점 = 안장 **증명 없음** | 방법 정당성 | 끝점을 교환하는 **반전 연산** 성립 여부 + **free/frozen mask 불변성**을 기록. 얻는 것은 "홉 방향 정류점" 까지임을 명시하고, 남은 검증(구속 해제 raw force · ±δ · CI-NEB 교차)을 `still_required` 로 |
| ③ | `if_pos 0 0 0` 이 **힘 성분을 마스킹** | QE 의미론 | `relax.out` 의 `Total force` 로는 구속 원자 잔여 힘을 검증 불가(순환). **구속 없는 scf** 입력을 따로 생성 |
| ④ | 반경 5/7 Å 가 셀과 안 맞음 | 실험 설계 | 가드를 **λ₁/2** 로 (2×2×2 상한 5.19 Å). 권장: 셀 간 비교 3.5·4.0 / 스캔 3.5·4·5·6, 2회 연속 \|ΔEa\| ≤ 0.02–0.03 eV |
| ⑤ | Windows 기본 인코딩에서 도구가 죽음 | 이식성 | 모든 `open()` 에 `encoding="utf-8"` (0건 남음) + **stdout** 도 재설정, 안 되면 ASCII 표식 |
| ⑥ | selftest 가 위 다섯을 못 잡음 | 회귀 방어 | **50건** (fail-open 2건 · conflict · λ₁ vs 면높이 혼동 · 반경 상한 · 중점 근거 · raw force 안내) |

## 반증·한계

- λ₁ 계산은 `n ∈ [−3,3]³` 탐색이다. 극단적으로 기운 셀에서는 범위를 넓혀야 한다.
- ②의 반전 연산 검사는 **가장 단순한 후보 하나**만 본다. 일반 공간군 연산 탐색이 아니다.
  실제 대칭 연산이 반전이 아닌 경우(회전·나사축)는 못 잡는다.
- 고정셸의 편향 방향은 **모른다.** "절대 장벽은 조금 높고 셀 차이에서 상쇄된다" 는
  앞 판의 서술은 근거가 없어 삭제했다 — frozen boundary 가 끝점과 안장을 얼마나 다르게
  불안정화하는지는 계산 전에 부호조차 모른다.
- `min_l` 기본 변경은 **아직 신규 계산에 투입되지 않았다.** Codex 판정은 신규 투입 기준
  NO-GO 이며, v3 4종과 cc333 고정셸은 ②·③ 검증이 닫힌 뒤에 건다.

## 출처

- Codex 동결 리뷰 (`eeacc989`, 2026-08-16) — λ₁ 정의·NameError·hash 충돌·fail-open 지적
- 재현: `tools/sei/build_neb_inputs.py: cell_metrics()` · 본 카드 표의 3셀 λ₁ 는 우리 repo 에서 독립 계산
- `db/properties/sei_neb.json` — 지위 4분할 적용본
- QE `INPUT_PW`: `if_pos` 는 해당 성분의 힘을 0 으로 마스킹한다
