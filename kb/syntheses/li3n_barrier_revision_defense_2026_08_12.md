---
title: "Li3N(001) 장벽 — 리비전 방어 카드 (AF-ASSB 원고 v5)"
date: 2026-08-12
updated: 2026-08-12
tags: [li3n, neb, revision, manuscript, diffusion-barrier, af-assb]
status: 확정 — 2026-08-12 사용자 결정: 0.118(두 점 on-N/TS)로 그림 교체
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: mixed
evidenceScope: multi-source-primary
targetVenue: AF-ASSB AgNO3–C–PVP 원고 v5 (Manuscript/SI/Figure set) 리비전 회신
---

## Thesis

Li₃N(001) 위 Li adatom 이동장벽이 lithiated carbon(LiC₆(0001))보다 크게 낮다는 원고의 주장은
**어떤 추정치를 쓰든 성립한다** — 우리 값 4종과 문헌값이 모두 0.10–0.13 eV 대역에 모이고
LiC₆ 0.290 eV 와 2.5–3배 차이가 유지되기 때문. 리비전에서 흔들릴 수 있는 것은 결론이 아니라
**보고 수치 0.102 eV 의 계산 출처**와 **슬랩 두께 수렴 근거의 부재** 두 가지다.

## Argument

### A1. 값 대역이 네 경로에서 일치한다

| 경로 | 값 (eV) | 상태 | 출처 |
|---|---|---|---|
| DFT CI-NEB 7 images (`li3n_001_pathA_dft_full`) | 0.102 (img3↔img0) / 0.12 (forward) | fmax **0.11** eV/Å 에서 정지 — 미수렴 | `db/properties/diffusion.json` |
| 두 점 구속이완 (`li3n_001_p0_2point_...2026-07-15`) | **0.118** | 양쪽 BFGS 수렴 | `db/properties/diffusion.json` |
| 문헌 [54] Kim et al. ACS Nano 17 (2023) 3168 | 0.133 | GPAW + CatLearn **ML-NEB** | `kb/methodology/li_adatom_neb_protocol.md` |
| KISTI 직선 drag 프로파일 | 같은 대역 (상한) | p4/p5 미수렴 | `db/properties/li3n_drag_profile_kisti.csv` |

LiC₆ 는 0.290 (`db/properties/li3n_barrier_origin.csv` `LiC6_DFT_eV` 최대 0.28968;
7-image DFT-SCF on UMA 기하, `db/properties/li3n_barrier_fig_origin.csv`).
→ 비율은 2.46× (0.118) ~ 2.84× (0.102). **어느 쪽이든 결론 문장이 안 바뀐다.**

### A2. 0.102 의 정확한 계보 (2026-08-12 특정)

원고 Fig. S9 의 7단계 패널 `0 / 0.009 / 0.084 / 0.102 / 0.084 / 0.009 / 0` 은
2026-06-21 NEB 이미지 에너지 `[0, −18, −93, −102, −13, +76, +77]` meV 의
**img3→img0 반쪽을 +102 만큼 이동시켜 거울대칭한 것**. 네 숫자가 정확히 일치한다.
`kb/methodology/li_adatom_neb_protocol.md` 2026-07-09 항목이 이 구성(mirrored-spline
0.054/0.102)을 폐기했고, `db/properties/diffusion.json` 은 같은 그림의 **자리 라벨이
뒤집혀 있으며 hump 크기만 유효**하다고 기록한다.

### A3. 방어 가능한 항목 (질문 오면 즉답 가능)

- **LiC₆ 가 MLIP 기하 위 DFT 단일점인 점** → 이미 원고에서 conservative lower bound 로 명시.
  MLIP 는 TS 를 매끄럽게 만들어 장벽을 과소평가하므로 비율은 하한.
- **전자구조 세팅** → 60/480 Ry USPP/PBE, k 2×2×1, MV 0.01 Ry, `conv_thr` 1e-6 Ry
  (2026-08-12 kgy 입력파일 실측). 슬랩 셀 a=b=10.95 Å, c=28.545 Å → 진공 15.75 Å.
- **왜 NEB 대신 구속이완인가** → 흡착 유도 표면 완화가 elastic band 를 깨뜨림.
  `kb/methodology/li_adatom_neb_protocol.md` 에 실패 계보 4건 기록 — 필요 시 SI 한 문단화.
- **자리 이름** → SI/표에서 on-N·bridge 를 명명하지 않는 방침. 명명하지 않으면 노출 없음.

## Counter-arguments

### C1. "0.102 는 미수렴 NEB 에서 나왔다" — ~~유효한 반론~~ → **해소 (2026-08-12)**

**해소 경로**: 사용자가 그림을 0.118(두 점 on-N/TS 구속이완)로 교체하기로 결정.
보고 수치가 양쪽 BFGS 수렴한 계산에서 나오므로 이 반론은 성립하지 않는다.
아래 원문은 기록 보존.

`fmax_eV_per_A_at_stop: 0.11` (목표 0.05). 원고 Methods 가 "0.05 eV Å⁻¹ 기준" 이라고
쓰면 사실과 다르다. 0.118(구속이완, 양쪽 수렴)로 통일하면 이 반론 자체가 사라진다.
현재 원고 본문의 Methods 문단은 "UMA-oc20 CI-NEB → DFT 단일점" 을 기술하는데,
그 경로가 실제로 낸 Li₃N 값은 **0.049 eV(철회)** 이지 0.102 가 아니다 — 즉 기존 Methods 도
Li₃N 을 정확히 기술하지 않는다. LiC₆ 에 대해서는 정확하다.

### C2. "슬랩 두께 수렴은?" — **유효한 반론, 미해소. 가장 약한 지점**

우리 4층(Li₂N 4면 + Li 3면, 135+1 = 136 atoms) vs 문헌 [54] 6층.
`db/properties/diffusion.json` `li3n_drag_p0_site_identity_2026-07-17` 이
**결정 실험을 명시해놓고 아직 돌리지 않았다**: 243원자 6층 N-노출 슬랩에서 구속이완 2점
(on-N xy vs pocket xy). 빌더는 `tools/neb_diffusion/li3n_mlneb_gpaw.py` 의 `build_li3n_001`,
구동은 `tools/neb_diffusion/li3n_uma_investigate.py sites --layers 6 --supercell 3 3`.
243/136 → SCF 스텝당 5–6배 비용. **리비전은 보통 2–3개월 뒤이므로 지금 걸면 늦지 않다.**

### C3. "보고한 최소점이 전역 최소인가?" — **유효한 반론, 부분 해소**

우리 4층 슬랩에는 min4 보다 **0.085 eV 낮은 2N-bridge pocket** 이 있다
(drag p0, E_ads −3.073 vs −2.988 eV, `db/properties/li3n_barrier_fig_origin.csv`).
"장벽 = 최고점 − 인접 최소" 를 엄밀히 적용하면 escape barrier 는 0.2035 eV.
문헌 [54] 는 6층에서 on-N 을 우물로 보고하므로, **C2 의 6층 테스트가 C3 도 동시에 결판낸다.**

### C4. "자리 라벨이 기하와 반대다" — **내부 확인됨, 외부 노출은 차단**

업로드 구조 2종의 배위수 실측 (2026-08-12):

| 파일 | 2.45 Å 안 N | 최근접 N | 성격 |
|---|---|---|---|
| `db/structures/li3n_onN_min.vasp` (= `..._min4`) | 3 (2.170 / 2.186 / 2.379 Å) | 2.170 Å | 2N-bridge 쪽 |
| `db/structures/li3n_TS_saddle.vasp` (= `..._saddle3`) | 1 | 1.971 Å | on-N 쪽 |

TS 쪽 adatom frac (0.750, 0.250), 최근접 Li 측면거리 0.596 Å →
`kb/methodology/li_adatom_neb_protocol.md` 의 UMA PES "saddle = on-top-Li (env Li 0.54 Å)" 와 일치.
db 는 같은 뒤집힘을 이미 두 번 기록했다 (NEB img 라벨 · drag p0 2026-07-17).
**대응**: SI·Table S2 에서 자리를 명명하지 않는다. 명명하면 즉시 노출된다.

### C5. 반박된 반론 — 기록 보존

- ~~"[3] Kim et al. 은 오기, Cui 여야 한다"~~ → **틀림.** 원고 ref [54] = M. S. Kim, …, Y. Cui,
  *ACS Nano* 17 (2023) 3168. Kim 이 제1저자, Cui 가 교신. 우리 db 가 교신저자 이름으로
  "Cui 2023" 이라 부르던 내부 별칭이었다. `kb/templates/manuscript_prompts.md` 의
  "Kim/Cui 사례" 교훈이 **역방향으로** 재현된 셈.
- ~~"conv_thr 은 1e-8, etot 1e-5"~~ → **틀림.** repo 도구 기본값이었고 실제 입력은
  `conv_thr=1.0e-6`, `etot_conv_thr`/`forc_conv_thr` 미지정(QE 기본 1e-4 / 1e-3).
  kgy `~/work/li3n_dft/{p0_min4.in, p0_saddle3.in}` 실측 2026-08-12.
- 다만 "image discretization of Kim et al. 를 따랐다" 는 서술은 **여전히 부정확** —
  그 논문은 CatLearn ML-NEB 이고 우리는 2점 구속이완이다. 방법 귀속 문구는 빼는 게 맞다.

### C6. 계산된 안장점이 최근접 hop 의 안장점이 아니다 — **유효한 반론, 미해소 (2026-08-12 신설)**

`tools/neb_diffusion/li3n_hop_frames.py` 로 min/TS 주변 기하를 전수한 결과:

- **min 은 3-fold 자리**다. 자기 기판 기준 표면 N 3개가 2.170 / 2.186 / 2.379 Å.
  (atop-N 이면 N 하나가 lateral ≈ 0 이어야 하는데 1.80–2.06 Å 다.)
- **TS 는 1-N 자리**다. N 1개 1.971 Å (lateral 1.388), 다음 N 은 2.668 Å.
- min 에서 **이웃 등가 3-fold 자리까지는 2.107 Å** (primitive (−1,+1)/3),
  경로상 최소 Li–N **2.011 Å** — N 관통 없음. 중간(xi≈0.5)은 N–N 다리(2.09/2.11 Å).
- 그런데 **계산된 TS 는 그 직선 위 xi = 1.20**, 즉 도착지보다 0.43 Å 더 멀다
  (직선 이탈은 0.05 Å 뿐 — 방향은 같다).

**함의**: 0.118 eV 는 "최소점과 **이웃 자리로 가는 안장점**" 의 차이가 아니라, 최소점과
**이웃 자리를 지나쳐 있는 한 점** 의 차이다. 이 2.107 Å hop 자체의 안장점(N–N 다리)은
계산된 적이 없다.

**완화 요인**: (1) Table S2·Methods 는 "saddle-region configuration" 이라고만 쓰고
"인접 자리의 안장점" 이라고 주장하지 않는다 — 서술은 이미 방어 범위 안이다.
(2) 값 자체는 여전히 0.10–0.13 대역이고 문헌 0.133 과 정합.
**미해소**: 다리점을 계산하면 0.118 보다 낮을 가능성이 있다 (그러면 장벽이 더 낮아지고
논문 주장은 강해진다). C2 의 6층 테스트와 같이 돌리면 한 번에 정리된다.

## Gap

1. **6층 243원자 2점 테스트** — C2·C3 를 동시에 닫는 유일한 실험. 미실행. 최우선.
1b. **2.107 Å hop 의 다리점(xi≈0.5) 구속이완 1점** — C6 를 닫는다. 136원자 1런이면 된다.
   입력은 `gen_drag_points_kgy.py --path --from_xy ... --to_xy ... --xi 0.5` 로 생성.
2. ~~원고 A-4 결정~~ → **② 0.118 통일로 확정 (2026-08-12)**. C1 소멸.
3. **NEB 실패 계보의 SI 문단화** — 초안 없음. C1 후속 질문이 오면 필요.
4. **LiC₆ full DFT NEB** — 미실행(`lic6_0001_dft_full` queued). 있으면 비율 하한 주장이 실측으로 바뀐다.

## 문서별 수정 리스트 (2026-08-12 대조)

원고 3종(Manuscript_v5.docx · Supplementary_Material_v5.docx · Figure_set_KDS_v7.pdf)
전문 대조 결과. **A-4 결정과 무관하게 고쳐야 하는 것**만 ★.

| # | 문서 | 항목 | 조치 |
|---|---|---|---|
| A-1 ★ | MS Methods | Li₃N 방법이 "UMA CI-NEB → DFT 단일점" 으로 기술됨 | 그 경로의 Li₃N 값은 0.049(철회). **구속이완 문단으로 교체 확정** |
| A-2 ★ | MS Methods | 진공 ≈17 Å | → **15.7 Å** (c 28.545 − 슬랩 12.80) |
| A-3 ★ | MS Methods | "ultrasoft pseudopotentials" 총론 | LiC₆ 의 C 는 **PAW** → 원소별 병기 |
| A-4 ★ | MS Methods | 교체 문단에 **LiC₆ 방법 서술이 없음** | LiC₆(CI-NEB + DFT 단일점) 문장 유지 |
| A-5 | MS Methods | 레퍼런스 `[1][2][3]` | → 본문 번호 `[43] [44] [54]` |
| A-6 | MS Methods | "following the image discretization of [54]" | 삭제 (C5 참조) |
| A-7 ★ | MS Results | 0.102 eV / "≈65% reduction" | → **0.118 eV / ≈59%**, 비율 2.46× |
| B-1 ★ | SI | Table S2 부재 | 신규 삽입 (2열 압축판, 12행) |
| B-2 ★ | SI | Fig. S9 캡션 "nudged elastic band calculations" | → 구속이완 서술로 교체 |
| B-3 ★ | SI | Fig. S9 자리 라벨 | 자리 명명 금지 (C4) |
| C-1 | Figure set | Fig 5d/5e/S9 의 0.102 | **0.118 로 교체 결정 (2026-08-12)** — 아래 §그림 교체 지침 |
| C-2 ★ | Figure set | bar graph 라벨 "on-N (atop)" / "bridge" | 실측 배위와 반대 (C4). "adsorption minimum" / "saddle configuration" 으로 |


## 그림 교체 지침 (2026-08-12 결정 후)

### 데이터는 이미 db 에 있다 — 새로 계산할 것 없음

`db/properties/li3n_barrier_origin.csv` (Origin-ready, 401행):

| 열 | 무엇 | 최대 |
|---|---|---|
| `DFTpoint_eV` (3점, `xi_DFTpoint`) | **실제 계산한 점** — 0 / 0.11820 / 0 | 0.11820 |
| `Li3N_guide_eV` | 눈 안내선 (아래 ⚠) | 0.11820 |
| `LiC6_DFT_eV` | 7-image DFT-SCF 스플라인 | 0.28968 |
| `kT300_eV` | 상온 기준선 | 0.02585 |

구조 파일: `db/structures/li3n_onN_min.vasp`·`.xyz`, `db/structures/li3n_TS_saddle.vasp`·`.xyz`.

### ⚠ guide 곡선의 정체 (2026-08-12 검산)

`Li3N_guide_eV` == `db/properties/li3n_neb_fit_optimal.csv` 의 `Li3N_migstep_eV`
× (0.1182 / 0.10201), **편차 5e-7** — 즉 **폐기한 mirrored-spline NEB 의 모양에 진폭만
두 점 값으로 갈아끼운 곡선**이다. 우리가 계산한 것은 점 2개뿐이므로:

- 5d 에서 이 곡선을 **계산된 경로처럼 그리면 안 된다.** 실선 금지, 점선 + 캡션에
  "dashed line is a guide to the eye connecting the two computed configurations" 명시.
- 더 안전한 대안: 5d 에서 Li₃N 곡선을 빼고 **LiC₆ 실측 7점 프로파일만** 남긴 뒤,
  Li₃N 은 5e 막대와 S9 구조 2컷이 담당하게 한다.
- Fig S9 는 7단계 → **2컷(최소점 · 안장점)** 으로. 중간 이미지는 존재하지 않는다.

### ⚠⚠ 7점 경로는 보간으로 못 만든다 (2026-08-12 실측)

`tools/neb_diffusion/li3n_hop_frames.py` 로 min→TS 직선을 연장해 프레임을 만들어 봤더니
**Li 공이 N 원자를 관통**한다. 격자 병진 18방향 전수 확인:

| hop (m,n) | 길이 Å | 경로상 최소 Li–N Å |
|---|---|---|
| (0,±1) (±1,0) (±1,±1) | 3.650 | 1.43 – 1.59 |
| (∓1,±1) (±2,±1) … | 6.322 | 1.10 – 1.25 |
| (±2,0) (0,±2) (±2,±2) | 7.300 | 1.43 – 1.59 |

**모두 1.9 Å 미만** — adatom 이 N 육각망 위 1.2 Å 높이에 있어서 어떤 직선도 N 꼭짓점을
넘어간다. min 을 TS 기준으로 반사한 점(frac 0.6122, 0.3794)도 N 이 **1.495 Å** 라 자리가
아니다. 즉 min–TS 를 잇는 대칭 직선 경로는 존재하지 않는다.

**함의**: 실제 MEP 는 hollow → bridge → hollow 의 **지그재그**다. 그리고 이것이
KISTI 9점 drag 가 톱니 모양(p0 0 / p1 +185 / p2 −33 / p3 −76 meV)으로 나온 **기하학적
이유**다 — 직선 스캔이 여러 자리를 가로지른 것. 도구에 관통 가드(`CLEARANCE_A = 1.90`)를
넣어 이 실수가 재발하지 않게 막았다 (`--allow_collision` 로만 강행 가능, 진단 전용).

**그래서 Fig S9 은 계산한 2컷만.** 보간 7컷은 물리적으로 불가능한 그림이 된다.
그래프 (b) 의 ξ=1 끝점이 0.0 인 것은 **등가 자리의 에너지가 같다는 대칭 진술**이지
경로 모양 주장이 아니므로 그대로 두면 된다.

### 자리 이름은 여전히 부르지 않는다

C4 가 그대로 살아 있다 — 파일명 라벨과 실측 배위수가 반대다. "adsorption minimum" /
"saddle-region configuration" 으로만 쓴다. Table S2 도 그렇게 되어 있다.

### 산출물

`docs/manuscripts/Table_S2_DFT_parameters.docx` — 0.118 / 0.290 결과행 복구
(0.102 와의 충돌이 사라졌으므로). 생성기 `docs/manuscripts/table_s2_build.js`.
