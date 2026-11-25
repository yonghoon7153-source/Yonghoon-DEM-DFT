# SDCP wave1 — 계산에 실제로 들어간 기하 (VESTA 배포본)

**날짜** 2026-08-28 · **출처** wave1 VASP 회수 드롭의 `*/static/OUTCAR.gz`
**생성** `python3 tools/sdcp/scfin_to_struct.py --outcar <drop>/tier{1,2}/*/static/OUTCAR.gz --out db/structures/sdcp_wave1`

## 무엇이 들어 있나

조각 3종 × 자세 × 자기 시드 = **16 잡**, 각각 `.xyz` + `.vasp` + `.vesta`.

| 조각 | 자세 | 시드 |
|---|---|---|
| `ptfe_c10` (C₁₀F₂₂, 32 원자) | Litop · Nitop | pm1 · net4 |
| `ptfe_dimer` (C₄H₂F₈, 14 원자) | Litop · Nitop | pm1 · net4 |
| `sdcp_neutral` (C₁₁H₁₆O₆S₂, 35 원자) | Litop · Nitop · cross_Li_at_Ni · cross_Ni_at_Li | pm1 · net4 |

슬랩은 전부 LiNiO₂(104) 1×4 L4 (192 원자), 셀 18.272 × 11.512 × 30.261 Å.

## 어떻게 여나

- **`.vesta`** — VESTA 로 바로 열면 NiO₆ 팔면체 + AFM 부격자 색(NiA 파랑 / NiB 보라)이 들어간
  측면 시점으로 뜬다. 같은 폴더의 `.vasp` 와 짝이다.
- **`.vasp`** (POSCAR) — 격자가 있으므로 **Boundary 타일링**은 이쪽을 연다.
- **`.xyz`** — 격자 없음. 분자만 잘라 보거나 다른 뷰어로 넘길 때.
- `.xyz` 와 `.vasp` 는 **같은 원자 순서·같은 좌표**다 (2026-08-03 사고 재발 방지).

## 재중심 (2026-08-28 v2)

**분자가 셀 가운데(면내)에 오도록 전 원자를 평행이동해 뒀다.** 원본 OUTCAR 좌표에서는
분자가 셀 경계에 걸쳐 있어 VESTA 기본 Boundary(0–1)에서 두 조각으로 잘려 보였다.
주기 평행이동이라 **구조·에너지·거리 전부 동일**하고, 이동량은 각 파일 1행 주석에
`recentered: ... shift frac=(…)` 로 남아 있다. OUTCAR 원문 좌표가 필요하면
`--no_recenter` 로 다시 뽑는다.

## ⚠ 읽을 때 주의

1. **기하는 자세마다 하나뿐이다.** `pm1` 과 `net4` 는 좌표가 **완전히 동일**하고
   (실측: xyz 바이트 일치), `static` 과 `dense` 도 동일하다. 두 시드 파일이 다른 것은
   **수렴된 Ni 국소 모멘트 부호**뿐이고, `.vesta` 의 NiA/NiB 색이 바로 그것이다.
   → 그래서 dense 판은 배포하지 않았다 (같은 구조의 중복).
2. **이완된 최소점이 아니다.** MLIP(UMA, freeze 0.85) 이완 위의 DFT 단일점(NSW=0)이다.
   구조를 "DFT 최적화 결과" 로 부르면 안 된다.
3. **F 색은 우리가 정했다.** 기존 SDCP 분자 .vesta 에 F 가 없었고 VESTA 기본 연두는
   흰 배경에서 사라져서 진한 청록(0,160,180)으로 뒀다. 다른 그림과 맞출 때 참고.
4. 흡착 접촉 판정(`①`)은 생성 로그에 남는다. 16개 전부 2.32–2.53 Å 로 "결합거리" 대역이지만,
   sdcp_neutral 의 접촉은 **H···O / H···Ni** 라 수소결합 성격이다 — 도구의 `<2.5 Å = 화학흡착`
   라벨을 그대로 인용하지 말 것.
5. 진공 분리는 16개 전부 확보(분자↔이미지 슬랩 ≥ 16.4 Å) — 2026-07-17 샌드위치 철회 사유 없음.

## 에너지

같은 드롭에서 뽑은 잡별 총에너지·E_ads 표:
`db/properties/sdcp_wave1_job_energies_2026_08_28.csv` (+ `.json` 열 설명·단서)
