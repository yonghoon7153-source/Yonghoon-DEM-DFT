# 적대 리뷰 — SDCP 부피-보존 구 스탬프 (`step3_sigma.rasterize` `sdcp_sphere_d_um` 경로)

- 대상: `scripts/step3_sigma.py:280–313` (HEAD `fb77dc76`, 브랜치 claude/stoic-knuth-NObVQ)
- 방법: 침대 없는 컨테이너 — 킷 스캐폴드(`docs/data/kit_ps_scaffolds`, `scripts/sr01_realbed_ab.py:44` `load_kit`)
  + `additives.seed_sdcp` 실배치 + 합성 픽스처.  추적 파일 무수정, 커밋 없음.
- 재현: scratchpad `rev_sdcp_stamp.py` / `rev_sdcp_stamp2.py` / `rev_sdcp_stamp3.py`
  (§8 에 전문 수록 — scratchpad 는 세션 휘발이므로 이 문서의 §8 이 정본).
  전제 검증: 직접 구현(셀중심-폐구 판정) == production `rasterize` — 200 랜덤 위치 불일치 0/200.
  기준 selftest: `python3 scripts/step3_sigma.py --selftest` → 전체 PASS (sdcp-prio·sdcp-gate 포함, 실행 확인).

## 0. 요약 (랭크)

| 랭크 | 결론 | 근거 절 |
|---|---|---|
| **HIGH** | **"구 스탬프 ~+11 % 계통 과대 (1.115/1.105/1.132)" 는 재현 불가이며 틀렸다** — 스탬프는 배치-평균 **무편향**(측정 1.000±0.001), 실배치 0.97~0.99.  그 세 숫자는 격자-정렬 픽스처의 위상 인공물로 재구성된다.  CL-33 verdict·`fb77dc76` 커밋 메시지 정정 필요 (+12.6 % 해석 사슬에 들어가 있다) | §2 |
| MED | 게이트 문턱 2.0 의 **서술이 틀렸다** — 전소실 절벽은 d/vox=√3=1.732 (1.74~2.0 구간 소실 0 실측).  단 1.5 는 소실 1.24 % 라 "1.5 면 충분" 도 아니다.  게이트 값 자체는 보수적 무해, 메시지와 근거를 고칠 것 | §4 |
| MED | d/vox=2.0(현행 vox 0.15 런)에서 per-입자 부피 0.48~1.91×, **origin 8팔 간 스탬프 부피 3.1 %**(n=1,658; n↑ 시 감소) — 팔간 잡음원으로 명시할 것.  앙상블 **평균**은 무편향이라 mean 인용은 안전 | §2·§3 |
| MED-LOW | payload origin-shift 는 `lo=-s`·`hi=+s` **양쪽**에 더해 시험도구보다 여분층 +1(FP 시 +2)이 생긴다.  비주기 솔브에서 불활성(빈 층 실측 0셀), **periodic_xy 병용 시 seam 이 조용히 끊긴다** (픽스처 실측).  현행 8팔 런은 비주기라 미발화 | §6 |
| LOW | AM 침식은 **h0** — 침식 = 씨앗 기하의 참 겹침부피 (스탬프 신규 인공물 아님).  단 점 51 → 구 334 셀(×6.5, AM 셀의 0.10 %)의 규약 차이가 있고, 근원은 `seed_coat` 의 off∈[0, d/2) 매장 규약이다.  문서화 필요 | §1 |
| LOW | 게이트가 SDCP 0개 침대에도 발화 (fail-closed 방향이나 대조 팔 차단 가능) · pid 마스크 누출(침식 셀의 SDCP 전류가 AM per-particle 프록시에 산입 — 점 규약에도 있던 것) | §7 |
| 검증 OK | 충돌 = **union** (이중계산 없음) · 두 경로 공통영역 **비트 동일 8/8** · `sdcp-prio` **판별력 입증** (결함판 FAIL) · 결함판의 유일 효과는 우선순위 (부피 부작용 0 — 대조 팔 해석에 중요) | §3·§5 |

---

## 1. 공격 1 — AM 침식 규약: **h0 채택** (침식 = 씨앗 기하의 참 겹침부피)

판별 검사 (h0: 침식 셀수 = (구∩AM 참부피)/vox³ ± 양자화 / h1: 계통 편차):

**픽스처** (AM Ø5 µm + 표면점 SDCP 1개, vox 0.15; `rev_sdcp_stamp.py` §B):

| 앵커 off (µm) | 점 침식 | 구 침식 | h0 = lens/vox³ |
|---|---|---|---|
| 0.000 | 1 | 4 | 2.05 |
| 0.075 | 0 | 4 | 0.63 |
| 0.150 | 0 | 0 | 0.00 |
| **0.000, 32개 서브복셀 지터 평균** | — | **2.06 ± 1.41** | **2.05** |

단일 위상은 양자화로 어긋나 보이지만(4 vs 2.05), 위상 평균이 **2.06 vs 2.05** 로 일치 — 무편향.

**실배치** (kit_ps_7_3 중앙 12 µm 크롭 AM 69개 + `seed_sdcp` 1,658점[앵커 158/벌크 1,500],
vox 0.15; h0 는 입자당 2,048-표본 MC 로 Σ(구∩AM-union)):
침식 **334 셀 vs h0 336 셀 (비 0.994)** ⇒ 계통 편차 없음.  분해(`rev_sdcp_stamp3.py`):
앵커 0.810 셀/입자(렌즈) + 벌크 0.138 셀/입자(표면 스침).  점 스탬프는 51 셀 (0.031/입자).

**판정**: 구 스탬프는 **씨앗된 기하를 충실히 굽는 것**이고 침식은 새 인공물이 아니다 (h0).
다만 두 가지를 기록할 것:
- 침식의 **근원은 시더 규약**이다 — `scripts/additives.py:204–205` 가 앵커 중심을
  `off = rng.uniform(0, shell_um)` (shell_um = d/2, `additives.py:558,568`) 에 놓아 입자가
  AM 에 최대 반부피 매장된다 (접선 배치라면 off ≡ d/2 였어야).  점 스탬프는 이것을 거의
  안 보였고(0.127 셀/앵커) 구 스탬프가 **드러낸다**(0.810 셀/앵커).  결과적으로 앵커 입자의
  AM-**외부** 부피는 참부피의 **0.81배** (666−128=538 셀/158입자 vs 4.19 셀).
- 규모는 무해: AM 셀의 **0.104 %** (점 0.016 %).  전자 σ 표(`mpm_webapp_payload.py:925–926`)
  에서 침식 셀은 0.005~0.01 → 250 S/cm; 이온 표에서 AM(차단) → σ_ion_sdcp 0.001
  (`mpm_webapp_payload.py:489–490`) — AM 표면을 감싸는 이온 도막이 생기는 방향까지 포함해
  "SDCP 는 AM 위에 드레이프된다" 는 시더 서사와 부호가 같다.
- 과제문의 "최대 ~9셀" 은 과대 — off=0 에서도 렌즈는 반부피 ≈ 2.05 셀, 위상 요동 최대 ~5셀.

## 2. 공격 2 — 부피비 위상 의존: **h1 채택** + **"+11 % 과대" 주장 반박 (HIGH)**

**단일 입자, 균일 랜덤 위상 40,000개** (`rev_sdcp_stamp.py` §A1):

| d/vox | 셀수 범위 | 부피비 평균 | 표준편차 | per-입자 범위 |
|---|---|---|---|---|
| 2.0 | 2–8 | **1.0003** | 0.259 | 0.477–1.910 |
| 2.4 | 4–10 | 0.9998 | 0.114 | 0.553–1.382 |
| 3.0 | 8–19 | 1.0007 | 0.112 | 0.566–1.344 |

셀중심-폐구 판정의 기대 셀수는 정확히 V/vox³ (지시함수 적분) — **배치-평균 무편향**이 이론이고
측정이 3격자 모두 ±0.1 % 로 확인한다.

**8 lattice-shift 팔** {0, vox/2}³ (production `rasterize` 를 payload 규약 `lo=-s` 로 호출):
- 고정 랜덤 125개(겹침 없음): 팔별 497–549 셀, **spread 10.46 %** ⇒ **h1** (팔은 동일하지 않다).
- 정격자 5×5×5 (간격 1.05 µm = 7·vox, 위상 공통모드): 팔별 250–1,000 셀 = 비 0.4775–1.9099
  (**300 % spread**) — 격자-정렬 배치의 최악 사례.
- `seed_sdcp` 실배치 1,658점: **spread 3.10 %** (0.9711–1.0011).  1/√n 스케일이므로 실런
  규모(수만~10만 점; `fb77dc76` 메시지의 도체 셀 +295,533 → n_SDCP ≈ 9×10⁴)에서는 서브-% —
  관측된 구-스탬프 4팔 origin 폭 0.34 % 와 정합.

**"+11 % 계통 과대" (1.115/1.105/1.132, "겹침 없는 125개") 재현 시도 — 실패, 반박**:
- 같은 실배치 구름을 vox 0.15/0.125/0.10 에서 재면 **0.9715/0.9744/0.9781** (경계 클리핑
  0.3 µm 제외 시 0.9813/0.9861/0.9893, 겹침까지 제외한 순수 스탬프 편향은
  **0.9921/0.9995/1.0017**).  +11 % 는 어느 층에서도 나오지 않는다.
- 그 세 숫자의 산술 재구성: **1.1052 = 8/7.2382** (d/vox 2.4 에서 셀 8개 위상),
  **1.1318 = 16/14.1372** (d/vox 3.0 에서 셀 16개 위상) — 두 값 모두 **정확히 정수 셀수**로
  풀리고, 두 조건을 **동시에** 만족하는 격자 위상이 실재한다 (26³ 스캔에서 93개; 그 위상들의
  vox 0.15 셀수는 4 또는 5 → 비 0.9549/1.1937, 125개 혼합으로 1.115 재현 가능).
  ⇒ 그 측정은 **격자에 정렬된 배치의 위상 인공물**과 정합하고, 위상-평균 참값(≈1.00)이 아니다.
- 픽스처 자체가 리포에 없다 (`grep -rn "1.115"` → 코드·문서 0건; `fb77dc76` 커밋 메시지에만
  존재).  게다가 결함판 주석(`fb77dc76~1` `step3_sigma.py:288`)은 같은 조건을 "**부피 오차
  0.8 %**" 라 적었다 — 순수 스탬프 편향 실측 −0.8 %(0.9921)와 일치하는 것은 **이쪽**이다.

**영향**: `docs/reviews/claims.json:1228` (CL-33 verdict "2.4 % 변동(1.105~1.132)" · "~+11 %
과대") 와 CL-34 해석("구 스탬프 ≈1.1배 표현")은 **표현 부피 ≈ 1.0 (실배치 0.97~0.99)** 로
정정해야 한다.  방향은 우호적이다: +12.6 % 관측을 "표현 1.1배" 로 디플레이트할 이유가 없어져
**참부피 이득 ≈ 관측치** 로 읽는 쪽이 강화된다 (우선순위 결함 대조 팔은 별도, §5).

## 3. 공격 4 — 충돌(응집): **union, 이중계산 없음** (h0)

두 입자 중심거리 s, vox 0.10, 24 위상 지터 평균 (`rev_sdcp_stamp.py` §D):

| s/d | 래스터/union | 래스터/2V |
|---|---|---|
| 0.25 | 1.028 | **0.703** |
| 0.50 | 0.971 | 0.819 |
| 0.75 | 1.007 | 0.964 |
| 1.00 | 0.984 | 0.984 |

래스터가 union 해석해를 따라가고 2V 에서 멀어진다 ⇒ 이중계산 없음.  구현상도
`step3_sigma.py:306` `np.unique(...axis=0)` + sid 격자라 원리적으로 불가능 — 실측으로 봉인.
실전형 `clump=4` (σ=d 산포, 1,062점): 비 0.980 vs 동수 singles 0.983 — **union 손실 0.3 %p**
(무해).  ⚠ 따라서 clump/응집 모드에서 래스터 부피는 n·V_true 보다 겹침만큼 작다 — 부피 원장을
점수×V_true 로 대조하지 말고 (sid==5)·vox³ 로 대조할 것.

## 4. 공격 3 — 게이트 문턱 2.0: **절벽은 √3=1.732, 메시지 정정 필요** (MED)

균일 랜덤 위치 200,000개/수준 (`rev_sdcp_stamp.py` §C):

| d/vox | 0.75 | 1.0 | 1.2 | 1.5 | 1.7 | **1.732** | 1.74 | 1.8 | 1.9 | 2.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| 소실 % | 78.02 | 47.53 | 20.14 | 1.24 | <0.005 | **0** | 0 | 0 | 0 | 0 |
| 셀수 | 0–1 | 0–1 | 0–2 | 0–4 | 0–4 | 1–4 | 1–6 | 1–8 | 1–8 | 2–8 |

- 전소실 절벽은 정확히 **√3** (최근접 셀중심 최대거리 √3/2·vox ≤ r 조건) — 게이트 메시지
  (`step3_sigma.py:284–287`) "d/vox<2 → 입자를 통째로 잃는다" 는 [1.74, 2.0) 에서 거짓.
- "1.5 에서도 소실 0 이면 과잉차단" 가설은 기각 — 1.5 는 **1.24 %** 소실.
- 87.5 % (vox 0.4) 주장 대비 균일-랜덤 실측은 **78.0 %** — 대략 같은 규모이나 정확 재현은
  불가 (실배치 위치상관 여지; 그 실측 픽스처도 리포에 없다).
- **평균 부피는 모든 d/vox 에서 무편향**(0.995–1.002, 소실 포함) — 소실을 생존자의 과대가
  정확히 상쇄한다.  ⇒ 게이트의 진짜 근거는 총부피가 아니라 **per-입자 기하/연결성**이다:
  d/vox 1.8 에서 per-입자 [0.33, 2.62]×, 2.0 에서도 [0.48, 1.91]×.  2.0 은 "소실 0 + 여유"
  로는 서 있지만 per-입자 충실도로는 1.8 과 질적으로 다르지 않다 — **임의선**임을 명시하고,
  메시지의 근거를 "통째 소실"(√3 아래에서만 참)에서 "per-입자 표현 산포"로 바꿀 것.
- FP 경계: `0.30/0.15 == 2.0` 정확히 True (이진표현상 0.3 = 2×0.15) → vox 0.15 통과는 결정적.

## 5. 공격 6 — mutation test: **`sdcp-prio` 판별력 입증** + 결함 크기 방향

`git show fb77dc76~1:scripts/step3_sigma.py` (구 스탬프가 상 루프 **뒤**에 있던 결함판, 진행 중인
원격 런의 코드)를 별도 모듈로 import 하고 `step3_sigma.py:1492–1501` 의 sdcp-prio 로직을 그대로
적용 (`rev_sdcp_stamp2.py` §F):

| 판 | PTFE(4) 점→구 sid | SWCNT(6) | VGCF(2) | sdcp-prio |
|---|---|---|---|---|
| 현행 `fb77dc76` | (7, 7) | (8, 8) | (5, 5) | **PASS** |
| 결함판 `fb77dc76~1` | (7, **5**) | (8, **5**) | (5, 5) | **FAIL** |

⇒ 시험은 실제 결함 변이를 잡는다 (형식적 통과가 아님).  부수 확인 두 가지:
- **결함판의 유일한 효과는 우선순위다**: SDCP 단독 픽스처에서 결함판(점+구 이중 스탬프)과
  현행판의 셀수가 동일 (4 == 4) — d/vox ≥ √3 이면 점 셀 ⊂ 구라서 부피 부작용이 0.
  ⇒ 진행 런(4/8팔, 비 1.1253)과 수정판 대조 팔의 차이는 **순수하게 PTFE/SWCNT 셀 귀속**이다.
- 크기 방향 픽스처 (PTFE 400점 근방 SDCP 100점, vox 0.15): 결함판이 PTFE 셀 396→305
  (**23 % 를 도체로 전환**).  실런 크기는 커밋 메시지의 dof 상계(최대 39 %)와 함께 대조 팔이
  판정할 문제 — 여기서는 방향(σ_e 부풀림)과 기전만 봉인.
- 한계: sdcp-prio 는 **중심 셀 하나**만 본다 (`step3_sigma.py:1500`) — 이웃 셀의 우선순위
  회귀는 못 잡는다.  현행 구조(사전계산 셀을 루프 (5,5) 슬롯에서 도장)에서는 중심=이웃이 같은
  배열로 찍혀 실질 커버되나, 스탬프를 셀별로 다시 쪼개는 리팩터가 오면 사각지대가 된다.

## 6. 공격 5 — 두 경로 동등성: **공통영역 비트 동일, 격자 크기 규약은 다르다**

payload (`mpm_webapp_payload.py:902–924`: `_lo3 = -s`, `_hi = hi + s`) vs 시험도구
(`step3_transport_resolution.py:72–78`: `lattice_shift`, n = round(L/vox)+1).  랜덤 40구름 ×
{s=0, h/2, rand, (h/2,0,0)} + **거리==r 동률 정렬 픽스처**(셀 중심·모서리 정렬 3점) × {s=0, h/2, …}
전수 비교 (`rev_sdcp_stamp2.py` §E): **공통영역 sid==5 diff = 0, 8/8 조합** — 셀중심-폐구
판정·FP 라운딩까지 두 경로가 일치한다 (둘 다 `(i+0.5)·vox − s` 산술).
- 격자 크기: payload n = ceil((L+2s)/vox) — s 가 lo·hi 에 **두 번** 들어간다.  L=3.05, s=h/2:
  payload 22 vs 도구 21.  L=3.0 (vox 배수): (3.15/0.15)=21.000000000000004 → ceil 22 = 주석
  "축마다 셀 하나" (`mpm_webapp_payload.py:895–896`) 보다 **+2** (FP).  여분층은 전 시험에서
  빈 층(sid5 0셀) — 비주기 솔브 불활성.
- ⚠ 지뢰: **periodic_xy 와 병용 시** 빈 wrap 층이 seam 을 조용히 끊는다.  픽스처
  (`rev_sdcp_stamp3.py` §H, seam 으로만 닫히는 회로): 여분층 없음 σ=9.081e-4 → 빈층 1개
  σ=6.0e-4 (= 남은 온전 기둥 3e-3/5 정확히 — seam 몫 소멸).  현행 8팔 런은 비주기(runner 가
  `--periodic` 를 opt-in 으로만 주입, `sdcp_gain_vox015_8arm.sh:115`)라 미발화.  origin-shift
  ×periodic 조합을 쓰기 전에 wrap 층 규약을 정리할 것 (시험도구의 +1 셀도 같은 문제를 가진다).

## 7. 부수 발견 (LOW)

- **게이트 과잉폭**: `step3_sigma.py:283` 검사가 `_p5` 추출(:289) **앞**이라 SDCP 0개 침대도
  플래그+coarse vox 면 ValueError (실측: VGCF-만 침대 + vox 0.4 → 발화).  8팔 러너는 SBE 에도
  플래그를 주므로 (`sdcp_gain_vox015_8arm.sh:118–121,131`) coarse-vox 대조 팔을 만들 때 걸린다.
  fail-closed 방향이라 무해하나, `_p5` 가 비면 게이트를 건너뛰는 것이 옳다.
- **pid 누출**: 침식 셀은 sid=5 가 되어도 pid 는 AM 을 가리킨다 (`rasterize` 는 pid 를 안
  지움).  `per_particle_current` 는 `pid >= 0` 만 마스크 (`step3_sigma.py:568`) → SDCP 셀
  전류가 AM per-particle 프록시에 산입.  점 규약에도 있던 결함의 ×6.5 확대 (334 vs 51 셀,
  AM 셀의 0.10 %) — 뷰어 프록시 한정, 무해 수준. 기록만.
- **부피 원장 규약**: 상별 부피 원장(다음 GPU ② 계획)은 SDCP 를 (sid==5)·vox³ 로 세면 침식분
  (AM→SDCP 0.10 %)과 union 손실(응집 시)이 함께 들어온다 — 레시피 대조 시 이 두 항을 분리해
  적을 것 (§1·§3 수치가 그 예산).

## 8. 재현 (하네스 전문)

실행: 각 파일을 scratchpad 에 두고 `PYTHONUTF8=1 python3 <파일>` (리포 루트 기준 경로 무관,
`REPO` 상수만 유지).  결함판은 `git show fb77dc76~1:scripts/step3_sigma.py > step3_sigma_defect.py`.

<details><summary>rev_sdcp_stamp.py (A0–A3·B·C·D·E·F·G — E 의 정렬 픽스처 s=h/2 는 shape 불일치로
중단되며, 그 자체가 §6 격자 크기 발견의 재현이다.  이후 절은 2/3 판 사용)</summary>

```python
#!/usr/bin/env python3
"""적대 리뷰 실험 하네스 — SDCP 부피-보존 구 스탬프 (step3_sigma.rasterize, fb77dc76)."""
import os
import sys
import time

import numpy as np

REPO = '/home/user/Yonghoon-DEM-DFT'
SCR = os.path.join(REPO, 'scripts')
sys.path.insert(0, SCR)
import step3_sigma as s3
from step3_transport_resolution import rasterize_spheres

D = 0.30
R = D / 2.0
V_TRUE = np.pi / 6.0 * D ** 3
EMPTY_AM = (np.zeros((0, 3)), np.zeros(0), None)
rng0 = np.random.default_rng(20260817)


def stamp_cells(pts, vox, lo, hi, d=D):
    sid, _ = s3.rasterize(*EMPTY_AM, np.asarray(pts, float), np.full(len(pts), 5, np.int8),
                          lo, hi, vox, sdcp_sphere_d_um=d)
    return np.argwhere(sid == 5), sid


def direct_count(p_frac, rvox):
    off = int(np.ceil(rvox)) + 1
    rg = np.arange(-off, off + 1)
    gx, gy, gz = np.meshgrid(rg, rg, rg, indexing='ij')
    cc = np.stack([gx, gy, gz], -1).reshape(-1, 3) + 0.5
    return int((((cc - p_frac) ** 2).sum(1) <= rvox * rvox).sum())


def lens_vol(rr, RR, dd):
    if dd >= rr + RR:
        return 0.0
    if dd <= abs(RR - rr):
        rmin = min(rr, RR)
        return 4.0 / 3.0 * np.pi * rmin ** 3
    return (np.pi * (rr + RR - dd) ** 2
            * (dd * dd + 2 * dd * (rr + RR) - 3 * (rr - RR) ** 2)) / (12.0 * dd)


print('[A0] 직접 구현 == production rasterize (200 랜덤 위치, vox 0.15)')
vox = 0.15
mism = 0
for _ in range(200):
    p = rng0.uniform(1.0, 2.0, 3)
    cells, _ = stamp_cells([p], vox, (0, 0, 0), (3., 3., 3.))
    n_direct = direct_count((p / vox) - np.floor(p / vox), R / vox)
    mism += (len(cells) != n_direct)
print(f'  불일치 {mism}/200')

print('[A1] 부피비 위상 의존 — 단일 입자 랜덤 위상 40k')
for dv in (2.0, 2.4, 3.0):
    rv = dv / 2.0
    vt = np.pi / 6.0 * dv ** 3
    cnt = np.array([direct_count(rng0.uniform(0, 1, 3), rv) for _ in range(40000)])
    ratio = cnt / vt
    print(f'  d/vox {dv:4.1f}: 셀수 {cnt.min()}–{cnt.max()} · 부피비 mean {ratio.mean():.4f} '
          f'± {ratio.std():.4f}  [min {ratio.min():.3f}, max {ratio.max():.3f}] · 소실 '
          f'{(cnt == 0).mean() * 100:.2f} %')

print('[A2] 8 lattice-shift 팔 {0, vox/2}³ (production rasterize, lo=-s)')
vox = 0.15
L = 6.0


def eight_arm(pts, tag, d=D):
    tots = []
    for sx in (0.0, vox / 2):
        for sy in (0.0, vox / 2):
            for sz in (0.0, vox / 2):
                s = np.array([sx, sy, sz])
                cells, _ = stamp_cells(pts, vox, tuple(-s), tuple(np.array([L, L, L]) + s), d)
                tots.append(len(cells))
    tots = np.array(tots, float)
    ratio = tots * vox ** 3 / (len(pts) * V_TRUE)
    print(f'  {tag}: 팔별 셀수 {tots.astype(int).tolist()}')
    print(f'      부피비 {np.array2string(ratio, precision=4)}  '
          f'spread {(tots.max() / tots.min() - 1) * 100:.2f} %')
    return ratio


pts_r = []
while len(pts_r) < 125:
    q = rng0.uniform(0.5, L - 0.5, 3)
    if all(np.linalg.norm(q - w) > D for w in pts_r):
        pts_r.append(q)
eight_arm(np.array(pts_r), '(a) 랜덤 125 (겹침 없음)')
g = (np.arange(5) * 1.05 + 0.6)
pts_g = np.stack(np.meshgrid(g, g, g, indexing='ij'), -1).reshape(-1, 3)
eight_arm(pts_g, '(b) 정격자 5×5×5 (간격 7·vox)')

print('[A3] seed_sdcp 실배치 (킷 AM 표면앵커+기공, 8팔)')
from sr01_realbed_ab import load_kit
import additives
am_c, am_r, se_c, se_r, lat, thick = load_kit('kit_ps_7_3')
ctr = np.array([lat / 2, lat / 2, thick / 2])
crop = 12.0
m = (np.abs(am_c - ctr) < crop / 2 + am_r.max()).all(1)
amc = am_c[m] - (ctr - crop / 2)
amr = am_r[m]


def in_am(q):
    return bool((np.linalg.norm(amc - q, axis=1) < amr).any())


pts_k, ids_k, info_k = additives.seed_sdcp(
    3000, (crop, crop, crop), 0.15, np.random.default_rng(7),
    am=(amc, amr), in_am=in_am, surface_frac=0.5, return_ids=True, return_info=True)
print(f'  seed_sdcp: {info_k["n_seeded"]} 점 (앵커 {info_k["n_anchored_seeded"]} / 벌크 '
      f'{info_k["n_bulk_seeded"]}), AM {len(amc)}개')
L = crop
eight_arm(pts_k.astype(float), '(c) seed_sdcp 실배치')

print('[B] AM 침식: AM Ø5 + 표면앵커 SDCP 1개 (vox 0.15, 점 vs 구)')
vox = 0.15
box = (6.0, 6.0, 6.0)
C_AM = np.array([3.0, 3.0, 3.0])
R_AM = 2.5
am1 = (C_AM[None, :], np.array([R_AM]), np.array([2]))
sid_am0, _ = s3.rasterize(*am1, None, None, (0, 0, 0), box, vox)
n_am0 = int((sid_am0 == 1).sum())
print(f'  AM-only 래스터: {n_am0} 셀 (참 {4 / 3 * np.pi * R_AM ** 3 / vox ** 3:.1f})')
for off in (0.0, 0.075, 0.15):
    p = C_AM + np.array([0, 0, R_AM + off])
    res = {}
    for tag, dd in (('점', 0.0), ('구', D)):
        sid_c, _ = s3.rasterize(*am1, p[None, :], np.array([5], np.int8), (0, 0, 0), box, vox,
                                sdcp_sphere_d_um=dd)
        eroded = int(((sid_am0 == 1) & (sid_c == 5)).sum())
        res[tag] = (eroded, int((sid_c == 5).sum()))
    dd_c = R_AM + off
    lens = lens_vol(R, R_AM, dd_c)
    print(f'  off {off:5.3f}: 점 침식 {res["점"][0]} (총 {res["점"][1]}) · '
          f'구 침식 {res["구"][0]} (총 {res["구"][1]}) · h0 {lens / vox ** 3:.2f} 셀')
er, to = [], []
for _ in range(32):
    sh = rng0.uniform(0, vox, 3)
    C2 = C_AM + sh
    p2 = C2 + np.array([0, 0, R_AM])
    am2 = (C2[None, :], np.array([R_AM]), np.array([2]))
    sid_a, _ = s3.rasterize(*am2, None, None, (0, 0, 0), box, vox)
    sid_c, _ = s3.rasterize(*am2, p2[None, :], np.array([5], np.int8), (0, 0, 0), box, vox,
                            sdcp_sphere_d_um=D)
    er.append(int(((sid_a == 1) & (sid_c == 5)).sum()))
    to.append(int((sid_c == 5).sum()))
lens0 = lens_vol(R, R_AM, R_AM)
print(f'  off=0 지터 32: 침식 {np.mean(er):.2f} ± {np.std(er):.2f} (h0 {lens0 / vox ** 3:.2f}) '
      f'· 총셀 {np.mean(to):.2f} (참 {V_TRUE / vox ** 3:.2f})')
sid_amk, _ = s3.rasterize(amc, amr, np.full(len(amc), 2), None, None,
                          (0, 0, 0), (crop, crop, crop), vox)
sid_k_pt, _ = s3.rasterize(amc, amr, np.full(len(amc), 2), pts_k.astype(float),
                           np.full(len(pts_k), 5, np.int8), (0, 0, 0), (crop, crop, crop), vox)
sid_k_sp, _ = s3.rasterize(amc, amr, np.full(len(amc), 2), pts_k.astype(float),
                           np.full(len(pts_k), 5, np.int8), (0, 0, 0), (crop, crop, crop), vox,
                           sdcp_sphere_d_um=D)
am_mask = (sid_amk == 1) | (sid_amk == 2)
e_pt = int((am_mask & (sid_k_pt == 5)).sum())
e_sp = int((am_mask & (sid_k_sp == 5)).sum())
from scipy.spatial import cKDTree
tree = cKDTree(amc)
mc = rng0.normal(size=(2048, 3))
mc /= np.linalg.norm(mc, axis=1, keepdims=True)
mc *= rng0.uniform(0, 1, (2048, 1)) ** (1 / 3) * R
tot_lens = 0.0
for q in pts_k.astype(float):
    nb = tree.query_ball_point(q, R + amr.max())
    if not nb:
        continue
    inside = np.zeros(len(mc), bool)
    for j in nb:
        inside |= (np.linalg.norm(mc + q - amc[j], axis=1) < amr[j])
    tot_lens += inside.mean() * V_TRUE
print(f'  실배치 침식: 점 {e_pt} · 구 {e_sp} · h0 {tot_lens / vox ** 3:.0f} 셀 → '
      f'구/h0 {e_sp * vox ** 3 / tot_lens:.3f} · AM 셀의 {e_sp / am_mask.sum() * 100:.3f} %')

print('[C] 게이트 문턱: 소실률 vs d/vox (각 200k)')
for dv in (0.75, 1.0, 1.2, 1.5, 1.7, 1.732, 1.74, 1.8, 1.9, 2.0):
    rv = dv / 2.0
    cnt = np.array([direct_count(rng0.uniform(0, 1, 3), rv) for _ in range(200000)])
    vt = np.pi / 6.0 * dv ** 3
    nz = cnt[cnt > 0]
    print(f'  d/vox {dv:5.3f}: 소실 {(cnt == 0).mean() * 100:6.2f} % · 셀수 [{cnt.min()}, '
          f'{cnt.max()}] · 생존 부피비 [{nz.min() / vt:.3f}, {nz.max() / vt:.3f}] '
          f'mean {cnt.mean() / vt:.4f}')

print('[D] 충돌: 두 입자 s<d → union? (vox 0.10, 24 지터)')
vox_d = 0.10
for f in (0.25, 0.5, 0.75, 1.0):
    s_ = f * D
    pts2 = np.array([[1.5, 1.5, 1.5], [1.5, 1.5, 1.5 + s_]])
    acc = []
    for _ in range(24):
        sh = rng0.uniform(0, vox_d, 3)
        cells, _ = stamp_cells(pts2 + sh, vox_d, (0, 0, 0), (3., 3., 3.), D)
        acc.append(len(cells) * vox_d ** 3)
    v_meas = np.mean(acc)
    v_union = 2 * V_TRUE - lens_vol(R, R, s_)
    print(f'  s/d {f:4.2f}: 래스터/union {v_meas / v_union:.3f} · 래스터/2V '
          f'{v_meas / (2 * V_TRUE):.3f}')
pts_c, info_c = additives.seed_sdcp(2000, (crop, crop, crop), 0.15,
                                    np.random.default_rng(11), am=(amc, amr), in_am=in_am,
                                    surface_frac=0.5, clump=4, return_info=True)
cells_c, _ = stamp_cells(pts_c.astype(float), vox_d, (0, 0, 0), (crop,) * 3, D)
v_c = len(cells_c) * vox_d ** 3
print(f'  clump=4: {info_c["n_seeded"]} 점 → 비 {v_c / (info_c["n_seeded"] * V_TRUE):.3f}')
cells_s, _ = stamp_cells(pts_k.astype(float)[:info_c['n_seeded']], vox_d,
                         (0, 0, 0), (crop,) * 3, D)
print(f'  대조 singles 동수: {len(cells_s) * vox_d ** 3 / (info_c["n_seeded"] * V_TRUE):.3f}')
```
</details>

<details><summary>rev_sdcp_stamp2.py (E-재 공통영역 대조 · B-split · F mutation · G 게이트 폭)</summary>

```python
#!/usr/bin/env python3
import os
import sys

import numpy as np

REPO = '/home/user/Yonghoon-DEM-DFT'
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import step3_sigma as s3
from step3_transport_resolution import rasterize_spheres

D, R = 0.30, 0.15
V_TRUE = np.pi / 6.0 * D ** 3
EMPTY_AM = (np.zeros((0, 3)), np.zeros(0), None)
rng0 = np.random.default_rng(20260817)

print('[E-재] payload(lo=-s, hi=L+s) vs 시험도구(lattice_shift=s) — 공통영역 비트 대조')
vox, Lb = 0.15, 3.0
cl = rng0.uniform(0.4, Lb - 0.4, (40, 3))
al = np.array([[1.575, 1.575, 1.575], [1.50, 1.50, 1.50], [1.575, 1.50, 1.575]])
for name, pts in (('랜덤 40', cl), ('정렬 3 (거리==r 동률)', al)):
    for tag, s_ in (('s=0', np.zeros(3)), ('s=h/2', np.full(3, vox / 2)),
                    ('s=rand', np.array([0.031, 0.094, 0.007])),
                    ('s=(h/2,0,0)', np.array([vox / 2, 0, 0]))):
        sidA, _ = s3.rasterize(*EMPTY_AM, pts, np.full(len(pts), 5, np.int8),
                               tuple(-s_), tuple(np.full(3, Lb) + s_), vox, sdcp_sphere_d_um=D)
        sidB = rasterize_spheres(vox, (0., 0., 0.), Lb, [(pts, np.full(len(pts), R), 5)],
                                 lattice_shift=(s_ if s_.any() else None))
        nA, nB = sidA.shape, sidB.shape
        ncom = tuple(min(a, b) for a, b in zip(nA, nB))
        dif = int(((sidA[:ncom[0], :ncom[1], :ncom[2]] == 5)
                   != (sidB[:ncom[0], :ncom[1], :ncom[2]] == 5)).sum())
        extraA = int((sidA == 5).sum()) - int((sidA[:ncom[0], :ncom[1], :ncom[2]] == 5).sum())
        extraB = int((sidB == 5).sum()) - int((sidB[:ncom[0], :ncom[1], :ncom[2]] == 5).sum())
        print(f'  {name:22s} {tag:12s}: A{nA} B{nB} 공통 diff {dif} · '
              f'A여분층 sid5 {extraA} · B여분층 sid5 {extraB}')
for Lx in (3.0, 3.05, 3.07):
    s_ = vox / 2
    print(f'   L={Lx}: payload {int(np.ceil((Lx + 2 * s_) / vox))} vs 시험도구 '
          f'{int(round(Lx / vox)) + 1}  ((L+2s)/vox={(Lx + 2 * s_) / vox:.10f})')

print('[F] mutation test — 결함판(fb77dc76~1) rasterize 에 sdcp-prio 로직 그대로')
import importlib.util as iu
spec = iu.spec_from_file_location(
    'step3_sigma_defect',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'step3_sigma_defect.py'))
old = iu.module_from_spec(spec)
sys.modules['step3_sigma_defect'] = old
spec.loader.exec_module(old)


def sdcp_prio(mod):
    pr, per = True, {}
    for oph in (4, 6, 2):
        C1 = np.array([[1.0, 1.0, 1.0]])
        pp = np.vstack([C1, C1])
        ph2 = np.array([5, oph], np.int8)
        s1, _ = mod.rasterize(np.zeros((0, 3)), np.zeros(0), None, pp, ph2,
                              (0, 0, 0), (3., 3., 3.), 0.15)
        s2, _ = mod.rasterize(np.zeros((0, 3)), np.zeros(0), None, pp, ph2,
                              (0, 0, 0), (3., 3., 3.), 0.15, sdcp_sphere_d_um=0.30)
        i = tuple((np.array([1., 1., 1.]) / 0.15).astype(int))
        per[oph] = (int(s1[i]), int(s2[i]))
        pr &= bool(s1[i] == s2[i])
    return pr, per


ok_new, per_new = sdcp_prio(s3)
ok_old, per_old = sdcp_prio(old)
print(f'  현행판: {"PASS" if ok_new else "FAIL"} {per_new}')
print(f'  결함판: {"PASS" if ok_old else "FAIL"} {per_old}')
ptfe = rng0.uniform(1.0, 5.0, (400, 3))
sdcp = ptfe[:100] + rng0.normal(0, 0.05, (100, 3))
pp = np.vstack([sdcp, ptfe])
ph = np.array([5] * 100 + [4] * 400, np.int8)
for mod, tag in ((s3, '현행'), (old, '결함')):
    sd, _ = mod.rasterize(np.zeros((0, 3)), np.zeros(0), None, pp, ph,
                          (0, 0, 0), (6., 6., 6.), 0.15, sdcp_sphere_d_um=D)
    print(f'  {tag}: sid7(PTFE) {int((sd == 7).sum())} · sid5 {int((sd == 5).sum())}')
p1 = np.array([[1.03, 1.11, 1.07]])
sd_o, _ = old.rasterize(np.zeros((0, 3)), np.zeros(0), None, p1, np.array([5], np.int8),
                        (0, 0, 0), (3., 3., 3.), 0.15, sdcp_sphere_d_um=D)
sd_n, _ = s3.rasterize(np.zeros((0, 3)), np.zeros(0), None, p1, np.array([5], np.int8),
                       (0, 0, 0), (3., 3., 3.), 0.15, sdcp_sphere_d_um=D)
print(f'  SDCP 단독 부피 부작용: 결함판 {int((sd_o == 5).sum())} vs 현행 {int((sd_n == 5).sum())}')

print('[G] 게이트 과잉폭 — SDCP 0개 침대 + coarse vox + sphere 플래그')
try:
    s3.rasterize(*EMPTY_AM, np.array([[1., 1., 1.]]), np.array([2], np.int8),
                 (0, 0, 0), (3., 3., 3.), 0.4, sdcp_sphere_d_um=0.30)
    print('  통과 (게이트 미발화)')
except ValueError as e:
    print(f'  ValueError 발화: "{str(e)[:52]}…"')
print(f'  FP: 0.30/0.15 == 2.0 → {0.30 / 0.15 == 2.0}')
```
</details>

<details><summary>rev_sdcp_stamp3.py (B-split 마스크 수정 · A3 multi-vox · periodic seam 픽스처)</summary>

```python
#!/usr/bin/env python3
import os
import sys

import numpy as np

REPO = '/home/user/Yonghoon-DEM-DFT'
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import step3_sigma as s3

D, R = 0.30, 0.15
V_TRUE = np.pi / 6.0 * D ** 3
rng0 = np.random.default_rng(20260817)

from sr01_realbed_ab import load_kit
import additives
am_c, am_r, se_c, se_r, lat, thick = load_kit('kit_ps_7_3')
ctr = np.array([lat / 2, lat / 2, thick / 2])
crop = 12.0
m = (np.abs(am_c - ctr) < crop / 2 + am_r.max()).all(1)
amc, amr = am_c[m] - (ctr - crop / 2), am_r[m]


def in_am(q):
    return bool((np.linalg.norm(amc - q, axis=1) < amr).any())


pts_k, ids_k, info_k = additives.seed_sdcp(
    3000, (crop, crop, crop), 0.15, np.random.default_rng(7),
    am=(amc, amr), in_am=in_am, surface_frac=0.5, return_ids=True, return_info=True)
n_anch = info_k['n_anchored_seeded']
AMT = np.full(len(amc), 2)          # LIGGGHTS type 2 = AM_S → sid 1 (rasterize:234 규약 주의)

print('[B-split] 침식 분해 (vox 0.15)')
sid_am0, _ = s3.rasterize(amc, amr, AMT, None, None, (0, 0, 0), (crop,) * 3, 0.15)
am_mask = (sid_am0 == 1) | (sid_am0 == 2)
for tag, sub in (('앵커만', pts_k[:n_anch]), ('벌크만', pts_k[n_anch:]), ('전체 ', pts_k)):
    for st, dd in (('점', 0.0), ('구', D)):
        sid_s, _ = s3.rasterize(amc, amr, AMT, sub.astype(float),
                                np.full(len(sub), 5, np.int8), (0, 0, 0), (crop,) * 3, 0.15,
                                sdcp_sphere_d_um=dd)
        er = int((am_mask & (sid_s == 5)).sum())
        print(f'  {tag} n={len(sub):4d} {st}: 침식 {er:3d} (입자당 {er / len(sub):.3f}) '
              f'· 총 sid5 {int((sid_s == 5).sum())}')

print('[A3-multi-vox] 같은 실배치, vox 0.15/0.125/0.10 (주장 1.115/1.105/1.132 대조)')
mi = ((pts_k > 0.3) & (pts_k < crop - 0.3)).all(1)
pin = pts_k[mi].astype(float)
keep = []
for i, q in enumerate(pin):
    if all(np.linalg.norm(q - pin[j]) > D for j in keep):
        keep.append(i)
piso = pin[keep]
for nm, pset in (('전체', pts_k.astype(float)), ('내부만', pin), ('내부+겹침없음', piso)):
    for vox in (0.15, 0.125, 0.10):
        sid_s, _ = s3.rasterize(np.zeros((0, 3)), np.zeros(0), None, pset,
                                np.full(len(pset), 5, np.int8), (0, 0, 0), (crop,) * 3, vox,
                                sdcp_sphere_d_um=D)
        v = int((sid_s == 5).sum()) * vox ** 3
        print(f'  {nm} vox {vox:5.3f}: 부피비 {v / (len(pset) * V_TRUE):.4f} (n={len(pset)})')

print('[H] periodic_xy + 여분 빈층 seam 픽스처')
sig = np.zeros(9)
sig[6] = 3.0e-3
for extra, tag in ((0, '여분층 없음 (n=4)'), (1, '빈층 1 (n=5)')):
    n = 4 + extra
    sid = np.zeros((n, 1, 4), np.int8)
    sid[0, 0, :] = 6
    sid[3, 0, :] = 6
    sid[0, 0, 2] = 0
    r_ = s3.solve_sigma_z(sid, sig, 0.4, periodic_xy=True)
    print(f'  {tag}: σ_eff = {float(r_["sigma_eff"]):.6g}')
```
</details>

<details><summary>+11 % 재구성 스캔 (정수 셀수 위상 실재 확인)</summary>

```python
import numpy as np
def cnt(p, rv):
    off=int(np.ceil(rv))+1; rg=np.arange(-off,off+1)
    gx,gy,gz=np.meshgrid(rg,rg,rg,indexing='ij')
    cc=np.stack([gx,gy,gz],-1).reshape(-1,3)+0.5
    return int((((cc-p)**2).sum(1)<=rv*rv).sum())
hits=[]
for a in np.linspace(0,0.5,26):
  for b in np.linspace(0,0.5,26):
    for c in np.linspace(0,0.5,26):
      p=np.array([a,b,c])
      if cnt(p,1.2)==8 and cnt(p,1.5)==16:
        hits.append((a,b,c,cnt(p,1.0)))
print('동시 일치 위상 수:', len(hits))           # → 93
# 그 위상들의 vox0.15 셀수 분포 → {4: 87, 5: 6}; 8/7.2382=1.1052, 16/14.1372=1.1318
```
</details>

## 9. 권고 (판정 아님 — 원장 소관)

1. CL-33 verdict·CL-34 배경의 "구 스탬프 ~+11 % 과대 / 1.105~1.132" 를 "배치-평균 무편향
   (실배치 0.97~0.99; 편차는 union·경계 클리핑)" 으로 정정하고, +12.6 % 해석에서 1.1 디플레이터를
   제거할 것.  측정 픽스처가 리포에 없으면 수치를 원장에 넣지 않는 규율 재확인.
2. 게이트 메시지(`step3_sigma.py:284–287`)의 근거를 "통째 소실"(√3 아래)이 아니라 "per-입자
   표현 산포"로 고치고, `_p5` 빈 경우 게이트 스킵.
3. origin 앙상블 보고에 "SDCP 스탬프 부피의 팔간 위상 산포" 항목을 추가 (n 에 따라 3.1 %→서브-%).
4. periodic_xy × origin-shift 조합은 wrap 층 규약 정리 전 금지 (현행 런 비주기라 무영향).
