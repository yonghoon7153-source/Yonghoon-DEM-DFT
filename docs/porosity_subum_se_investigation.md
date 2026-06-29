# sub-µm SE 크기효과 — 응집 sigmoid 가설 검증 (REFUTED)

**질문**: production porosity 식이 sub-µm SE(particulate_1, r_SE=0.25µm)를 못 맞힘.
Stage E Cronau처럼 **응집(cohesion) sigmoid**로 진폭을 문헌에 박아 정식화할 수 있나?

**결론**: **아니오.** 세 줄의 독립 증거가 응집-sigmoid 가설을 기각한다. sub-µm "looser"
보정을 지금 박으면 안 된다. 식은 **r_SE ≥ 0.5µm 도메인으로 유지**하고, sub-µm은 별도
고해상 재시뮬 + 스케일 재조정이 선행되어야 한다.

---

## 증거 ① — Bond number: 300MPa에서 응집은 무시 가능

van der Waals 인력 vs 인가응력의 비(granular Bond number):

| r_SE | F_vdW | F_applied(300MPa) | Bond = F_vdW/F_app |
|---|---|---|---|
| 0.25µm | 5.8 nN | 75 µN | **7.7×10⁻⁵** |
| 1.5µm | 35 nN | 2700 µN | **1.3×10⁻⁵** |

(Hamaker A≈5×10⁻²⁰ J, 접촉간격 0.3nm)

Bond ≪ 1 (10⁻⁴ 수준) → **응집은 인가응력보다 4자릿수 작다**. Yang-Zou-Yu류 응집 packing
곡선은 **중력/저응력 regime**(Bond~O(1))의 물리라 **우리 300MPa cold-press엔 적용 불가**.
Stage E Cronau가 압력-무관(재료 결정상태)인 것과 달리, 응집-packing은 압력과 경쟁하므로
고압에서 죽는다. → **응집 진폭을 박을 문헌 근거 자체가 무효.**

## 증거 ② — Schneider 2023(같은 황화물): 작은 입자 → *더 조밀* (반대 방향)

`schneider2023_particle_size_pressure_transport` (t-Li₇SiPS₈, 같은 sulfide 패밀리,
DEM+실험 EIS):
- **Heckel P_y: 작은 PSD(<50µm)=0.95 GPa < 큰 PSD(>50µm)=1.65 GPa** → 작은 입자가 **낮은
  항복압 → 소성 다짐이 더 쉬움 → 더 조밀**(Fig 2e: ρ_rel 작은입자 > 큰입자).
- 즉 문헌은 "**작은 입자 → 낮은 porosity(조밀)**"를 *실험으로* 보인다.

그런데 우리 식의 r_SE 항은 **계수 음수**(−2.1·r_SE) = "작은 SE → 높은 porosity(성김)".
→ **우리 식과 문헌이 정반대.** 응집이든 뭐든 sub-µm에서 porosity를 *올리는* sigmoid는
문헌(같은 소재계)과 충돌한다.

## 증거 ③ — 그 1점은 MPM 해상도 부족(artifact 의심)

| case | r_SE | MPM cell | r/cell | 판정 |
|---|---|---|---|---|
| **particulate_1** | 0.25µm | 0.154µm | **1.6 cells** | **UNDER-RESOLVED** |
| particulate_10 | 1.5µm | 0.183µm | 8.2 cells | ok |
| particulate_11 | 1.5µm | 0.157µm | 9.6 cells | ok |

particulate_1의 SE는 **격자 1.6셀**밖에 안 됨 → MPM이 소성 흐름을 제대로 못 풀어 **덜
다져진 채(15.97%, looser) 읽혔을** 가능성. 같은 조성(0:10, AM62)의 r1.5 짝
(particulate_10, MPM 14.10)보다 +1.87%p 성긴데, 이 차이는 **seed-noise(±1.5%p)와 해상도
artifact로 대부분 설명**된다 — 견고한 물리 신호가 아님.

---

## 종합 — 왜 "확실히 못 박나"

sub-µm sigmoid를 박으려면 **방향과 진폭**이 필요한데:
- **진폭(응집)**: Bond 검산이 기각(증거①).
- **방향(작을수록 성김)**: 같은-패밀리 문헌이 반대(증거②) — 문헌은 작을수록 조밀.
- **데이터(1점)**: 해상도 artifact 의심(증거③).

세 축이 모두 불확실/반대 → **물리적으로 정당한 sub-µm 보정을 지금 만들 수 없다.** 억지로
박으면 (Stage E Cronau가 피한) "데이터-fitting 계수"가 되어 신뢰성 0.

## 권고 (선결 작업)

1. **particulate_1 MPM 고해상 재시뮬** (n_grid↑ → r_SE=0.25를 ≥6셀로). 다져지면 15.97은
   under-resolution artifact 확정 → sub-µm 문제 자체가 소멸(식 r_SE 항으로 충분).
2. **스케일 재조정**: 우리 r_SE(0.25–1.5µm)와 Schneider(<50 vs >50µm)는 *다른 스케일*.
   우리 데이터의 "작은 SE=성김"이 진짜 µm-스케일 packing 물리인지(CLAUDE.md size-effect
   note), 아니면 모델 artifact인지 — 고해상 재시뮬이 가른다.
3. 그 전까지 **식 도메인 = r_SE ≥ 0.5µm**로 유지(검증됨, LOOCV 0.64, SE-rich RMSE 1.7).
   sub-µm은 "out-of-domain, 재시뮬 필요"로 정직 표기.

⇒ "응집 sigmoid로 확실히 잡자"의 정답은: **검증해보니 응집이 아니었고(Bond), 방향도
문헌과 반대였고(Schneider), 그 1점은 해상도 의심(1.6셀)** — 그래서 **지금은 안 박는 게
확실한 선택**. Stage E가 Cronau를 문헌에 박을 수 있었던 건 Cronau가 *압력-무관 측정*이라
그랬고, 여기 porosity-응집은 *압력-의존*이라 같은 길이 막힌다.

---

## particulate SE-rich 케이스 (참고, 모두 0:10 / r_AM_S=3)

| case | AM:SE | r_SE | DEM ε_sphere | MPM | gap | regime → use |
|---|---|---|---|---|---|---|
| particulate_1 | 62:38 | **0.25** | 16.82 | 15.97 | +0.85 | cross-val → ~16 (단 해상도 의심) |
| particulate_10 | 62:38 | 1.5 | **5.66** | 14.10 | −8.44 | SE-rich(ε_sphere 과압축) → **MPM 14.1** |
| particulate_11 | 72:28 | 1.5 | 11.39 | 17.74 | −6.35 | SE-rich → **MPM 17.7** |

particulate_10/11(r1.5)은 corpus 유지(SE-rich 정상사이즈, gate=MPM). particulate_1(r0.25)은
도메인 밖 → corpus 제외.

*기준: 300MPa, ρ_AM=4.8/ρ_SE=2.0, Bond A=5e-20 J.*
