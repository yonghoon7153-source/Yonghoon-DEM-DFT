# sdcp_poses_phaseB — Phase-B 에 들어간 **초기 자세** (표시용)

`tools/sdcp/export_phaseB_poses.py` 가 뽑은 것. 셀은 Phase-B 가 실제로 쓰는 c-shrink 셀
(a=18.272 · b=10.926 · **c=36.94 Å**) 이라 화면에서 보는 것과 계산이 같다.
CLAUDE.md 관례대로 xyz + POSCAR(.vasp) 페어.

| 파일 | 원자 | 조각 | 출처 |
|---|---:|---|---|
| `phaseB_doped_doped_sulfonate_down_r90_g22` | 226 | C₁₁H₁₅O₆S₂ (34) | `/data/work/runs/sdcp_v2/**phaseA**` = freeze_frac **1.0** |
| `phaseB_neutral_neutral_sulfonate_down_r180_g01` | 227 | C₁₁H₁₆O₆S₂ (35) | 같음 |

슬랩은 앞 192원자 (Li48 Ni48 O96), 분자는 그 뒤.

## ⚠ 출처 불일치 — 등재된 VASP 에너지와 **다른 자세다** (2026-08-11 확인)

`db/properties/sdcp_phaseB_dftu_v1.json` 의 VASP+U 단일점은
**freeze_frac 0.85 (`phaseA_top1free`)** 기하이고 자세는 `doped r0_g20` / `neutral r180_g22` 다.
이 폴더의 파일은 **freeze_frac 1.0** 의 `r90_g22` / `r180_g01` 이다.

→ **이 구조 그림과 그 JSON 의 수치를 한 슬라이드/한 표에 같이 올리면 안 된다.**
   0.85 기하는 아직 repo 에 없다 (gabia 회수 대상).

## 기하 감사 (`tools/sdcp/site_screen.py gate`, 2026-08-11)

| 자세 | 최근접 접촉 | Li 최근접 | **Ni 최근접** | 이미지 가로/세로 | 결합변화 | 판정 |
|---|---|---|---|---|---|---|
| doped r90_g22 | H···Li 2.58 Å | 2.582 Å | **없음 (>3.2 Å)** | 7.53 / 18.59 Å | 0 | 기하 게이트 전부 통과 |
| neutral r180_g01 | O···Li 2.53 Å | 2.533 Å | **없음 (>3.2 Å)** | 5.76 / 20.60 Å | 0 | 기하 게이트 전부 통과 |

두 자세 모두 2026-07 에 철회된 "샌드위치"(티오펜 S···이미지 슬랩 O 1.506 Å) 같은 문제는 없다.
다만 **3.2 Å 안에 Ni 접촉이 아예 없어** Li/Ni 경쟁이 담겨 있지 않다 —
따라서 이 자세들로는 **"Li 자리를 선호한다"고 쓸 수 없다**(재본 적이 없으므로).
자리 판정은 `kb/methodology/site_preference_protocol_2026_08_11.md` 의 대조쌍 설계로 다시 한다.

## 인용 금지

- 이 자세들의 UMA 에너지(xyz 헤더 `energy=`)는 **freeze 1.0 순위용**이다. 절대값 인용 금지.
- 개별 E_ads·Δ 는 `sdcp_phaseB_dftu_v1.json` 의 `do_not_cite_E_ads` 단서를 따른다.
