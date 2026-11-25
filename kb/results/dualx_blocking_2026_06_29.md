# dual-x 도핑 농도 스크리닝: Li-channel blocking_fraction (x=0.0625 vs 0.25)

**날짜** 2026-06-29 · **계** LPSCl1.6 + MO_x 도펀트 10종 · **방법** dual-x tier_cascade (mobility-only, STAGE_04에서 종료)
**데이터** `db/properties/dualx_blocking.{csv,json}` · **그림** `docs/figures/cascade/dualx_blocking.png`

> **한 줄.** 도펀트가 Li 이동망을 막는 정도(blocking_fraction)를 **두 농도(x=0.0625, 0.25)** 에서 apples-to-apples 비교. **HfO₂가 두 농도 모두에서 최저 blocking(=Li 수송에 가장 덜 방해)**, V₂O₅/Nb₂O₅/Ta₂O₅가 최악. 모든 도펀트가 농도↑에 따라 blocking **2.5~5× 증가**.

---

## 1. 결과

| 도펀트 | x=0.0625 (low) | x=0.25 (high) | Δ | ratio |
|---|---|---|---|---|
| **HfO₂** | **0.109** | **0.563** | 0.454 | 5.2× |
| La₂O₃ | 0.244 | 0.652 | 0.408 | 2.7× |
| TiF₄ | 0.247 | 0.860 | 0.613 | 3.5× |
| Sc₂O₃ | 0.267 | 0.694 | 0.428 | 2.6× |
| Gd₂O₃ | 0.267 | 0.694 | 0.428 | 2.6× |
| Cr₂O₃ | 0.267 | 0.750 | 0.483 | 2.8× |
| Y₂O₃ | 0.287 | 0.710 | 0.423 | 2.5× |
| Ta₂O₅ | 0.333 | 0.896 | 0.562 | 2.7× |
| Nb₂O₅ | 0.354 | 0.896 | 0.542 | 2.5× |
| **V₂O₅** | **0.375** | **0.927** | 0.552 | 2.5× |

(blocking_fraction = 도펀트 + 전하보상 결함이 막는 Li 이동망 분율. **높을수록 Li 수송에 나쁨.**)

## 2. 해석

- **순위(낮을수록 좋음)**: HfO₂ ≪ La₂O₃ < TiF₄ < Sc/Gd/Cr₂O₃ < Y₂O₃ < Ta₂O₅ < Nb₂O₅ < V₂O₅. **저·고농도에서 순위 거의 보존.**
- **HfO₂가 명확한 1등** — Hf⁴⁺(isovalent에 가깝고 등전자 보상 적음)이라 Li 채널을 가장 덜 막음 → **conductivity 관점 최우선 후보.**
- **+5 산화물(V₂O₅·Nb₂O₅·Ta₂O₅) 최악** — 고전하라 전하보상 결함↑ + 강한 음이온 끌림 → Li 채널 다수 차단.
- **농도 의존성**: 전부 x↑에 blocking↑ (2.5~5×). **TiF₄는 점프 최대(0.25→0.86, ×3.5)** — 저농도 양호하나 고농도에서 급격히 나빠짐 → 저농도 한정 후보.
- **희토류(+3, La/Y/Sc/Gd)** 중간 — La₂O₃가 그중 최선.

## 3. 정직한 한계
- blocking_fraction은 **상대적 mobility proxy** (기하·전하 기반 descriptor), 절대 σ 아님. 최종 전도도는 **BVSE/MD**로 확인 필요.
- mobility-only 스크리닝(STAGE_04 종료) — 안정성(e_hull)·ESW·SEI는 별도 (B₂O₃ 사례처럼 trade-off 존재 가능).
- 농도 2점(0.0625, 0.25)만 — 중간 농도 거동(최적 도핑량)은 보간/추가 필요.

## 4. 다음
- **HfO₂**(최저 blocking) → full pipeline(BVSE·MD σ·e_hull·ESW·SEI)로 champion 검증 권장.
- 농도-blocking 곡선이 단조이므로 **저농도(x≈0.0625) 도핑이 수송 보존에 유리** — 고농도는 V/Nb/Ta 제외.

## 참고
- `db/properties/dualx_blocking.{csv,json}`, `docs/figures/cascade/dualx_blocking.png`
- 도구: `tools/doping/run_dualx*.sh`, `watch_dualx_compare.sh`
