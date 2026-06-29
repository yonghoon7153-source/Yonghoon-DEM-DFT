# Post-porosity roadmap — DEM/모델 개선 + PTFE/VGCF/SuperP webapp + dem-analyze v3

> 작성 2026-06-29.  porosity sweep 종료 후 착수.  사용자 plan(2026-06-29):
> "porosity 모델 + DEM 개선 + PTFE/VGCF/SuperP 적용 코드/webapp 개선 → dem analyze v3.
>  webapp 각 샘플 분석요약에 PTFE/VGCF/SuperP(+ thinky/handmix mixing) 선택 → python/zip 생성
>  section + 전도도 with/without 둘 다 + 문헌 현상과 일치 검증."

★ **핵심: 인프라 ~70% 이미 존재 → 대부분 *배선*이지 신규개발 아님.**

## 0. 이미 있는 것 (재사용)
| 조각 | 위치 | 상태 |
|---|---|---|
| 첨가제 물리 (VGCF/SuperP/PTFE 밀도·phase code·개수계산·vol_frac) | `scripts/additives.py` | ✅ (DENS, recipe_counts, PHASE; PTFE fibril AR160=binder web, VGCF AR67, SuperP sphere) |
| recipe → run_mpm.sh baking | `scripts/mpm_input_from_case.py --add-recipe / --add-l-cv / --mixing{ballmill,thinky,handmix}` | ✅ (Stage-1 carbon seed + phase/fibre npy) |
| webapp **zip 생성** (am/se scaffold + run_mpm.sh + provenance) | `webapp/app.py:~5163` `[MPM input 변환]` 엔드포인트 | ✅ |
| 전달 솔버 (σ_ionic/σ_e/σ_thermal, Kirchhoff/Holm) | `scripts/network_conductivity.py` | ✅ |

## 1. 워크스트림 (porosity 종료 후)

### W1 — webapp: 첨가제 선택 → recipe zip section (배선)
- 분석요약(`generate_report`/`analyze` 출력)에 **"첨가제 적용" section** 추가:
  PTFE / VGCF / SuperP wt% 입력 + mixing(thinky=dry-coating / handmix / ballmill) 선택.
- 선택 → 기존 zip 엔드포인트(app.py:5163)에 `--add-recipe "<...>" --mixing <...>` 전달 → **recipe-baked run_mpm.sh zip** 다운로드.
- 신규개발 = UI section + 선택값을 `--add-recipe` 문자열로 직렬화 + 엔드포인트에 파라미터 추가.  나머지(zip·baking)는 재사용.

### W2 — 전도도 with/without 둘 다
- 같은 구조에서 **첨가제 有/無 두 번** 전달솔버 → σ_ionic·σ_e(·σ_thermal) 비교 출력.
- 無 = 현 production(첨가제 모름).  有 = additive phase를 네트워크에 포함(VGCF/SuperP=전자경로, PTFE=binder/차단).
- 분석요약에 "Δσ_e (+첨가제)", "Δσ_ionic (−첨가제 점유)" 나란히.

### W3 — DEM/porosity 모델 개선 (backlog 연동)
- **A3** MPM `--coh` distribution-aware (PTFE binder 양역할: 과잉=σ차단/부재=delamination, 비단조 cap).
- **A4** `se_coating_interface` carbon (SuperP가 CAM/SE 표면 film이면 coating regime — 현 additives.py는 bulk 간극만 seed).
- **A5** dispersion CV (첨가제 분산 불균일도).
- porosity 식 자체 개선(있으면): 첨가제 porosity 효과 항.

### W4 — dem analyze v3
- 위 W1-W3을 통합한 분석 파이프라인 버전.  첨가제 축이 1급 시민(porosity·σ·morphology 모두 with/without).

## 2. ★ 문헌 검증 anchors (모델 변화가 문헌과 같은 방향인가)
첨가제 적용 시 **예상 변화 + 그걸 맞춰야 할 문헌**:

| 첨가제 | 예상 모델 변화 | 문헌 anchor (litdb) | 방향 |
|---|---|---|---|
| **PTFE** (binder fibril) | **porosity ↓** (fibrillation이 void 메움) | **Hong #271** (PTFE void↓ **6.4%p**), spring-back #285 | porosity↓ |
| **PTFE** 과잉 | σ_ionic ↓ (resistive 막) / delamination(부재) | A3 비단조; #264 cross-link, #08 Bielefeld2020 binder σ-block | 비단조 |
| **VGCF/SuperP** | **σ_e ↑** BUT **σ_ionic ↓** (SE domain 점유) | **Kim2024 #19** (carbon이 SE분율↓ → σ_ion≈1/10 @>90wt%AM), **Cho2024**(VGCF 양면성) | σ_e↑/σ_ion↓ trade-off |
| **VGCF vs SuperP** | fiber > sphere (percolation 효율) | Kim2024 (fiber>sphere) | fiber 우세 |
| **SuperP coating**(thinky=dry-coat) | SE 표면 coat 시 **σ_e 3자리 붕괴** | **Kim #19** (SE-coating SuperP σ_e 3-decade collapse) | 위치-의존 |
| **고-AM(SE-poor) + 첨가제** | VGCF가 σ_ion 차단·tortuous | Cho2024 (88wt% 유해) | SE-poor서 유해 |

→ **검증 = 우리 with/without σ·porosity 변화가 위 방향·크기와 일치하나** 체크.  일치=모델 신뢰, 불일치=정량화된 한계(frame[4]).

## 3. 순서
porosity sweep 종료(통합 식 + U/E 닫기) → **W3(A3/A4/A5 모델) → W1/W2(webapp 배선) → W4(v3 통합)** → 각 단계마다 §2 문헌검증.
(W3 먼저: 모델이 맞아야 webapp가 의미.  단 W1 UI는 병렬 가능.)

## 4. 미해결/결정 필요
- recipe 직렬화 포맷(`--add-recipe` 문자열 스펙 — additives.py가 받는 형식 확인).
- with/without σ를 webapp 실시간(가벼운 네트워크 재계산) vs zip-후-GPU(MPM 포함) 어디까지.
- 첨가제 porosity 효과를 DEM(seed)에서 vs MPM(phase)에서 — 둘 다? (PTFE는 MPM binder, carbon은 둘 다 가능).
