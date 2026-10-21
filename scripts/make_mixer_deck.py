#!/usr/bin/env python3
"""믹싱 드럼 덱 생성기 — 조성에서 치수·개수·섬유파일을 **유도**한다.

왜 생성기인가
  치수가 조성에서 유도된다 (부피분율 → 개수비 → 드럼 크기).  손으로 적으면
  조성을 바꿀 때마다 틀린다.  `docs/reviews/mixing_model_design_20260919.md` §11 의
  계산을 그대로 코드로 옮긴 것이다.

⚠⚠ 생산 압축 덱의 `scale=1000` 규약을 **쓰지 않는다**.
  그 규약은 `E_sim = E_real/scale` · `R_sim = R_real×scale` 이라 접촉력은 `scale¹`,
  중력은 `scale³` 로 스케일된다 ⇒ 중력/접촉 비가 `scale²` 만큼 틀어진다.
  압축 덱은 **플래튼 구동**이라 중력이 무시돼 무해했지만 **드럼은 중력 구동**이다.
  ⇒ 대신 문헌 방식(`lischka`·`hare`)을 쓴다: **coarse-graining(CGF) + 중력 실제값 유지**,
  점착은 무차원수 보존으로 재보정(⬜ `D11`, 지수 미측정).

⚠ 전단탄성률을 낮춘다 — `lischka` 가 *"계산비용 때문에 G=1e8 로 낮췄다, 물성이 아니다"*
  라고 명시한 것과 같은 조작이고, 튜토리얼 `Mixer` 도 `E=1e7` 을 쓴다.
  ⇒ **탄성 물성으로 인용 금지.**

usage
  python3 scripts/make_mixer_deck.py --out dem_scripts/mixer_20260919 --n-total 50000
  python3 scripts/make_mixer_deck.py --selftest
  # ★ 강성 축 (2026-09-30 · 사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §3) — SE 영률만 ×F · 쌍별 F₀ 보존 ·
  #   dt 는 같은 규칙으로 새 E 에서 · [--dt-factor 0.5 = dt 만 ½ · step ×2].  옵션 중립이면 덱은 옛것과 바이트 동일 (ST①)
  python3 scripts/make_mixer_deck.py --out <dir> --n-total 100000 --cgf 151.4 --arm LC --seed 32452843 --revolutions 2 \
          --stiffen-se 14 --hold-bo-pairwise [--dt-factor 0.5]        # → <dir>/in.mixer + deck_meta.json (봉인 가능한 메타)
  # ★ 전 정밀도 덤프 (2026-10-05 · 강성 축 사전등록 §12-4 (다) · 확인 블록 덱용) — [--dump-full-precision] = `dump dmp` 바로 뒤
  #   `dump_modify dmp format "%d %d %.17g …"` 한 줄 (기본 끔 = 덱 바이트 그대로 · ⚠ LIGGGHTS 옛 문법 · ibb 바이너리 실측 전)
"""
import argparse
import math
import os
import re
import sys
import unicodedata

#: 밀도 (g/cm³) — `scripts/additives.py` 정본과 같은 값.  여기서 다시 적는 이유는
#  이 생성기가 리포 밖(1저자 WSL)에서도 단독으로 돌 수 있어야 하기 때문이다.
DENS = {'AM': 4.80, 'SE': 2.00, 'VGCF': 2.00, 'PTFE': 2.20}
#: ★ 밀도 세대 (2026-10-14 밤 · 1저자 결정 — 랩 표준 진밀도 SE 1.64 · NCM (PC · SC) 4.85 · 범위 (가) 앞으로만 ·
#  docs/density_generations_20261014.md) — `scripts/additives.py` DENS_GENERATIONS · DENS_CARRIED_FROM_GEN1 의 **사본** (이 생성기의 네 상만).
#  사본을 두는 이유는 위 DENS 와 같다 (리포 밖 단독 실행).  ⛔ 정본과 어긋나면 셀프테스트 DG① 가 실패한다 (additives.py 를 AST 로 읽어 대조).
#  ⛔ 전역 DENS 를 바꾸지 않는다 — 세대 미지정 덱 = gen1 (옛 덱 · 판정 기록 바이트 그대로) · 새 세대는 `plan(…, dens_gen=)` · CLI `--dens-gen` 으로만.
DENS_GENERATIONS = {
    'gen1': DENS,                                         # 같은 객체
    'lab20261014': {'AM': 4.85, 'SE': 1.64, 'VGCF': 2.00, 'PTFE': 2.20},
}
DENS_CARRIED_FROM_GEN1 = {'gen1': (), 'lab20261014': ('VGCF', 'PTFE')}   # 랩 값 없음 — gen1 값을 옮김 (이 생성기의 상만)


def dens_table(gen=None):
    """밀도 세대 → 이 생성기의 밀도표.  None (지정 안 함) = gen1 `DENS` **그 객체** (옛 덱 비트 그대로) · 이름 = 그 세대 사본.
    ⛔ 모르는 이름 · 빈 문자열 · 문자열 아닌 값 = 거부 (SystemExit — 이 생성기의 fail-closed 규약)."""
    if gen is None:
        return DENS
    if not isinstance(gen, str) or gen not in DENS_GENERATIONS:
        raise SystemExit(f'⛔ 밀도 세대 {gen!r} — 등록된 세대 {sorted(DENS_GENERATIONS)} 중 하나여야 한다 '
                         f'(docs/density_generations_20261014.md)')
    return dict(DENS_GENERATIONS[gen])


def _dens_of(p):
    """계획 `p` 의 밀도표 — `plan()` 이 넣은 것 · 없으면 (옛 형식 계획) gen1 `DENS`."""
    t = p.get('dens')
    return DENS if t is None else t
#: 1저자 지시 조성 (2026-09-19) — 에너지밀도 최대 조합
WT = {'AM': 80.0, 'SE': 18.0, 'VGCF': 1.0, 'PTFE': 1.0}
PS = (7.0, 3.0)                       # P:S (wt%)
#: **소재 실측 지름** (µm) — 이 표가 유일한 출처다.  모델 지름 = 이 값 × CGF.
#  ⚠⚠ 2026-09-21 이전 판은 이 표에 `SE 1.0` 을 적어 놓고 **쓰지 않았다**.  지름은
#    `AM_P` 만 읽고 나머지는 `dP/3` · `dP×0.25` 로 깎았다.  AM_P 12 에서 우연히
#    `AM_S 4` 는 맞았지만 `SE` 는 실제로 **3 µm** 였다 = **선언과 사용이 갈린 표**.
#    AM_P 를 바꾸는 순간 나머지가 조용히 따라 움직이는 구조였다.  ⇒ 전 상을 여기서 읽는다.
#  ★ AM_P 9 · AM_S 4 는 **소재 실측** (1저자, 2026-09-21).  AM_S 는 단결정이다.
#  ★★ **SE = 1.0 µm 는 1저자 확인값이다** (2026-09-21): 전극에 들어가는 **소립** LPSCl 이다.
#    ⛔⛔ 옛 표의 `SE 3.0` 은 **소재 크기가 아니었다** — 계산비용을 맞추려고 굵힌 값이고,
#      그 때문에 **크기 비가 3배 어긋나 있었다**:
#          d_SE/d_AM_P   소재 0.111  →  옛 모델 0.333
#      ⚠ 한때 이것을 *"3 µm 응집체를 한 덩이로 본 것"* 으로 변호할 수 있나 검토했으나
#        (그 해석이면 비가 정확히 맞는다) **1저자가 1 µm 를 확인해 기각**됐다.
#    ★ 왜 비가 중요한가 — 작은 구가 큰 구 더미에서 무엇을 하는지는 비 하나가 정하고
#      문턱이 셋이다: 삼각 틈 통과 0.1547 · 사면체 공극 0.2247 · 팔면체 공극 0.4142.
#      소재 0.111 은 **자유 체질**(AM 사이로 빠져나간다) 영역인데 옛 모델 0.333 은
#      **팔면체 공극만 채우는** 영역이다 ⇒ **문턱을 가로질렀다**.  크기 기반 분리와
#      Furnas 틈 채움이 옛 덱에서는 원리적으로 안 나타났다.
#    ⚠⚠ **대가는 통계다 — 이것을 모르고 이 값을 쓰지 말 것.**  소재 비에서는 개수비
#      SE/AM_P = 562 라 원자의 **0.178 % 만 AM_P** 다.  실측(2 g · 3 상):
#          원자 2 만 → AM_P **35 개**  (혼합도를 못 잰다)
#          원자 10 만 → AM_P 176 · AM_S 859   |   원자 30 만 → AM_P 528 · AM_S 2,577
#      옛 덱(SE 3 µm · 8 천 원자)은 AM_P 276 개였다 ⇒ 같은 통계를 소재 비에서 얻으려면
#      **약 15 만 원자**가 필요하다.  ⇒ **원자 예산은 SE 지름과 같이 정해야 한다.**
#    ⚠ VGCF·PTFE 값도 **소재 실측**이다 (`CL-66`).  이 지름으로 풀면 종횡비 67 이라
#      원자 예산의 97 % 를 섬유가 먹는다 — 그래서 생산에서 뺀다 (아래 `TYPES`).
D_REAL_UM = {'AM_P': 9.0, 'AM_S': 4.0, 'SE': 1.0, 'VGCF': 0.15, 'PTFE': 0.25}
L_FIB_UM = 10.0                       # ⚠ VGCF 길이.  PTFE 길이는 출처 없음 (`CL-67`)
#: 전체 상 목록 (카탈로그).  실제로 도는 것은 `TYPES` 다.
ALL_TYPES = ('AM_P', 'AM_S', 'SE', 'VGCF', 'PTFE')
FIBRE_TYPES = ('VGCF', 'PTFE')
#: 상별 particletemplate 시드 — **소수**여야 한다.  상이 빠져도 나머지는 안 흔들린다.
TPL_SEED = {'AM_P': 10487, 'AM_S': 11887, 'SE': 13901, 'VGCF': 15101, 'PTFE': 17093}
#: 타입 순서 — 덱의 `peratomtypepair` 행렬 순서와 같아야 한다
#  ★★ 생산 기본은 **AM_P · AM_S · SE 셋**이다 (1저자 비준 2026-09-21).
#    VGCF·PTFE 를 뺀 이유는 **비용이 아니라 말이 되게 하려고**다 — 실측:
#      · 실물 VGCF 는 종횡비 L/Ø = 66.7 인데 옛 덱의 것은 **2.6** 이었다 (26배).
#        섬유가 믹싱에서 하는 일(엉킴·가교·뭉침)은 길쭉해야 생긴다 ⇒ 그건 섬유가
#        아니라 **짧은 소시지**였고, "VGCF 를 넣었다" 고 말할 수 없다.
#        ⚠ SE 와 달리 **응집체로 읽어도 구제되지 않는다** — "카본 응집 덩이" 라면
#          말은 되지만 그러면 `multisphere` 강체 사슬로 넣을 이유가 없다.
#      · 진짜 종횡비로 풀면 원자 5만 중 **97 %** 를 섬유가 먹는다 (VGCF 50.8 ·
#        PTFE 46.2) ⇒ AM_P 가 드럼을 4.8 알갱이밖에 못 가로질러 믹싱을 못 본다.
#      · 굵힌 채로 두면 9.9 % 밖에 안 먹어서 **빼도 비용은 거의 안 준다**
#        (5만 원자에서 15.3x → 15.8x).  ⇒ 판단 근거는 비용이 아니다.
#      · 헤드라인은 *"코팅하면 더 잘 섞이나"* = AM–SE 점착 축이고, 섬유는 부피로
#        1.9 %(VGCF)·1.7 %(PTFE) 다.
#    ⚠ 포기하는 것: *"카본이 잘 분산되나"* 는 이 덱으로 물을 수 없다.  그건 AM 을
#      줄인 작은 도메인에서 **진짜 종횡비**로 따로 돈다 — 그래서 섬유 기계를 지우지
#      않고 `set_phases(ALL_TYPES)` 로 되살릴 수 있게 남겨 둔다.
TYPES = ('AM_P', 'AM_S', 'SE')


def set_phases(types):
    """도는 상 집합을 바꾼다.  카탈로그 순서를 강제한다 (행렬 순서 = 타입 번호)."""
    global TYPES
    bad = [t for t in types if t not in ALL_TYPES]
    assert not bad, f'모르는 상: {bad}'
    assert 'SE' in types and ('AM_P' in types or 'AM_S' in types), 'AM 과 SE 는 있어야 한다'
    TYPES = tuple(t for t in ALL_TYPES if t in types)
    return TYPES
#: 점착 원점 (J/m³) — 튜토리얼 `cohesion` 예제값.  ⚠ 우리 소재의 물성이 아니다.
#  ── 점착 눈금 — **CED(J/m³) 가 아니라 Bond 수로 건다** (2026-09-19 실측으로 갈아엎음) ──
#
# ⛔ 초판은 `CED0 = 3.0e5` 에 ×1/×10/×100 을 걸었다.  **5 팔 중 4 팔이 접촉모델 밖으로
#    나갔다** (`scripts/check_contact_validity.py` 로 실측):
#        E0 CED 0     겹침 중앙 0.09 %              손실 0 %      ✓
#        E1 3e5 균일  겹침 중앙 3.50 %              손실 0 %      ⚠
#        E2 AM 3e6    겹침 **최대 196 %**           손실 4.8 %    ⛔ (KE 가 안 떨어짐)
#        E3 SE 3e6    겹침 중앙 **55 %**            손실 **63 %** ⛔
#        E4 AM 3e7    겹침 최대 197 %               손실 28.7 %   ⛔
#    δ/r = 1.97 은 한 구의 중심이 상대 구 **반대편 바깥**에 있다는 뜻 = 겹침이 아니라 통과.
#
# ★ 왜 그랬나 — **SJKR 은 겹침에 선형, Hertz 반발은 δ^1.5** 다.
#       (4/3)·E*·√R*·δ^1.5  =  W + CED·2π·R*·δ
#    점착 지배 극한에서 `δ = (3·CED·2π·√R* / (4E*))²` ⇒ **δ ∝ CED²**.
#    ⇒ CED 를 ×10 하면 겹침이 **×100**.  ×1/×10/×100 사다리는 겹침으로 ×1/×100/×10⁴ 다.
#    ★ 이 식이 실측을 맞힌다 — 예측 3.3~3.5 % vs E1 실측 중앙 **3.50 %**.
#      ⚠ 초판은 3.54 % 라 적었다 — 섬유 **자기 겹침**(설계상 δ/r = 0.4)이 섞인 값이다.
#        `MIX-05` 로 고쳤고, 고친 값이 예측에 **더 가깝다**.
#
# ★ 그리고 F_coh ∝ CED·δ ∝ **CED³** 이므로 Bond 수도 CED³ 다.
#    ⇒ 물리 눈금(Bo)에서 고르게 놓으려면 **CED ∝ Bo^(1/3)** 로 걸어야 한다.
#    ⇒ Bo = F_coh/W ∝ CED³/(R·ρ·E*²) — 같은 CED 라도 **작고 가벼운 상이 훨씬 점착적**이다
#      (CED 1.65e5 에서 AM_P 23 · AM_S 70 · SE 210).  그래서 **상마다 CED 를 다르게** 준다.
#    ⚠ 겹침은 그렇지 않다 — 같은 CED 에서 `δ/r` 은 **반경과 무관**하다 (ν 만 다르다).
#      ⇒ 두 축이 따로 논다: **Bo 는 크기에 민감하고 겹침은 아니다.**  섞지 말 것.
#      이것이 설계문서 §11-5 의 열린 질문 `D11`(CG 하면 점착을 어떻게 다시 주나)에 대한
#      SJKR+Hertz 계의 유도 답이다.
#
# ⚠⚠ 한정어를 지우지 말 것 — 이 유도는 ① **점착 지배 극한**(무게항 무시)이고
#    ② **단일 접촉**이다.  침대에서는 입자가 묻혀 접촉이 여럿이다.  CED 3e5 에서
#    예측이 맞았다고 낮은 CED 에서도 맞는다는 뜻이 아니다 (거기선 무게항이 지배한다).
#    ⇒ **모든 팔은 돌린 뒤 `check_contact_validity.py` 로 확인한다.**  식은 사다리를
#      고르는 도구이지 유효성의 증명이 아니다.

OVL_CEILING = 0.01          # 겹침 천장 δ/r — DEM 연질구 관례 1 %
#: 상별 (반경 m, 포아송비, 밀도 g/cm³) — 덱의 `property/global` 과 같아야 한다
PHASE_MECH = {'AM_P': (0.25, 'AM'), 'AM_S': (0.25, 'AM'), 'SE': (0.30, 'SE'),
              'VGCF': (0.30, 'VGCF'), 'PTFE': (0.30, 'PTFE')}
E_YOUNG = 1.0e7             # Pa — SE 급 연화값 (앵커 시험·하위호환).  ⚠ 물성 인용 금지
#: ★ 상별 영률 — **÷135 균일 연화** (1저자 비준 2026-09-21, A안)
#  실물 AM 1.4e11 · SE(E_eff, 18배 연화) 1.35e9 · 강철 벽 2.0e11 을 **같은 배수**로 내린다.
#  옛 "전 상 1e7" 은 AM 을 14,000배, SE 를 135배 연화해 실물 대비 104 가 1.0 으로 사라져 있었다.
#  ⛔ 기각된 안 — SE 를 9.64e4 로 내리기(÷14,000): 중력만으로 SE 겹침 5.39 % (천장 1 % 초과).
#  ⇒ SE 는 그대로 두고 **AM 을 올린다**.
#  ⛔ 정정 2026-09-30 — 이 줄의 옛 문구 (dt 는 SE 가 정하니 AM 을 올려도 비용이 그대로라는 것) 는 **틀렸다**.  AM 을 ×103.7 올리면
#    상별 Rayleigh dt 가 AM_S 0.7055 µs < SE 1.1719 µs 가 되어 AM_S 가 dt 를 정하고, A안 전 (전 상 1e7 · SE 가 정함) 대비 step ×1.661 (비용 증가)
#    (CGF 151.4 캠페인 · plan()['dt_by'] — 지름이 CGF 에 비례하므로 이 대소는 CGF 와 무관).  SE 를 ×14 이상 경화한 덱에서는 다시 SE 가
#    정한다 (강성 축 · plan() docstring · 셀프테스트 ST⑥ · ST⑭).  덱 출력은 이 주석과 무관하다 (골든 해시 그대로).
#  검증(10만 원자·2 g): 중력 겹침 AM 0.011 % · SE 0.244 % · 접촉시간 = 회전주기의 0.042 %.
#  ⛔ 물성으로 인용 금지 · 믹서에서 압밀/porosity 를 읽지 말 것 · 압연 겹침과 비교 금지.
E_PHASE = {'AM_P': 1.037e9, 'AM_S': 1.037e9, 'SE': 1.0e7, 'VGCF': 1.0e7, 'PTFE': 1.0e7,
           'WALL': 1.48e9}
#: ★ 벽 — (B) 벽 전용 타입 (1저자 비준 2026-09-21).  강철 200 GPa ÷ 135 = 1.48e9.
#  옛 판은 메시가 `type 2`(= AM_S) 의 물성을 빌려 썼다.  이제 **마지막 타입이 벽**이다.
#  벽 점착: hare2026 은 JKR `γ_pw/γ_pp = 1/6.25` = **힘비 1/6.25**.  우리는 SJKR 이라
#  `F_coh ∝ CED³` ⇒ 같은 힘비를 내려면 **CED ÷ 6.25^(1/3) = ÷1.842**.
#  ⛔ CED 를 글자 그대로 ÷6.25 하면 힘이 **244배** 사라진다.  ⚠ γ↔CED 환산이 아니라
#     "JKR 힘비를 SJKR 에서 재현" 한 것이다 — O(1) 불확실을 원고에 적을 것.
#  ⛔ 정정 2026-10-14 (원장 `MIX-12`) — 위 유도는 둘을 빠뜨렸다: ① Hare 의 γ_pw/γ_pp = 1/6.25 는 짝의 **접착 에너지** 비다 — 벽 짝은 R* 가
#     두 배 (r vs r/2) 라 Hare 의 당김힘 비는 0.32 다 (에너지 비를 당김힘 비로 읽었다) ② 벽 짝의 E* 변화.  실제로 낸 당김힘 비 = SE–벽 / SE–SE 0.162
#     (Hare 의 0.51 배) · AM–벽 / AM–AM 0.4516 (Hare 의 1.41 배).  옛 덱 · 판정 기록은 그대로 · D2 결합 규칙 팔은 Hare 비를 기하평균으로
#     옮긴 γ_W/γ = 0.0256 과 쌍별 R* · E* 로 정한다 (셀프테스트 GM⑥ · docs/mixer_d2_wall_gamma_derivation_20261014.md).
WALL = 'WALL'
WALL_NU = 0.30
WALL_CED_DIV = 6.25 ** (1.0 / 3.0)
#: ★ 마찰 — hare2026 세트 (1저자 비준 2026-09-21).  옛 μ_s 0.5 · μ_r 0.2 는 출처가 없었다.
#  ⛔ 옛 설명 (2026-09-21, 철회 09-27 R-4 · Codex HB-02): *"우리 Bo 3.0 앵커는 hare2026 의 γ 에서 오고 … Bo 만 빌리고
#  마찰을 안 빌리면 앵커가 성립하지 않는다"* — Bo 3.0 (LA) 은 **문헌 앵커가 아니라 내부 기준점**이다 (환산이 틀렸었다:
#  Bo_po 0.444 · 20.25 설명 철회 · `docs/reviews/mixer_layered_prereg_20260921.md` §0 R-4).  마찰 세트를 hare2026 에서
#  가져온 것은 그대로다 (출처 있는 값) — 그러나 그것이 Bo 를 문헌에 정박시키지는 않는다.
#  ⚠ NMC622 값을 SE 에도 쓴다 (가정).  ⚠ 압연 덱(0.5 · 0.2/0.1)과 다른 것은 결함이 아니라
#     정합이다 — 다른 공정을 다른 실험에 정박했다 (frame[4]).  원고에 "왜 다른가" 한 줄 적을 것.
MU_S = 0.9                  # 정지마찰 (pp = pw)
MU_R = 0.075                # 구름마찰 (비구형성 대리)
COR = 0.3                   # 반발계수 (변경 없음)
#: ★ Froude 앵커 — 씽키 컵프레임 밴드 (설계문서 §18-1; ⚠ 1차 출처 미확보, 원장 §11)
#  `R = C·CGF·N^(1/3)` 라 원자 예산·CGF·질량 중 하나만 바꿔도 R 이 움직이고 같은 rpm 이
#  다른 Fr 을 준다.  실측: 새 드럼 R 13.14 mm 에서 옛 기본 60 rpm 은 Fr 0.053 = **밴드 밖**.
#  ⇒ `--fr` 이 주 노브고 rpm 은 유도한다.  `--rpm` 을 직접 주면 밴드 밖일 때 **거부**한다
#    (경고가 아니라 거부 — 선언 안 한 축은 검사도 안 된다는 것이 Phase A 96팔 사고의 교훈).
FR_ANCHOR = 0.0827
FR_BAND = (0.055, 0.086)


def rpm_for_fr(fr, R):
    return 60.0 / (2 * math.pi) * math.sqrt(fr * 9.81 / R)


def fr_of(rpm, R):
    return (2 * math.pi * rpm / 60.0) ** 2 * R / 9.81


def resolve_rpm(R, fr=FR_ANCHOR, rpm=None, allow_off_band=False):
    """rpm 을 정한다.  `rpm` 이 없으면 `fr` 에서 유도, 있으면 밴드 검사 (fail-closed)."""
    if rpm is None:
        return rpm_for_fr(fr, R)
    f = fr_of(rpm, R)
    if not (FR_BAND[0] <= f <= FR_BAND[1]) and not allow_off_band:
        raise SystemExit(f'⛔ --rpm {rpm:g} → Fr {f:.4f} 가 씽키 앵커 밴드 {FR_BAND} 밖이다.  '
                         f'이 드럼(R {R*1e3:.2f} mm)에서 Fr {fr} 은 {rpm_for_fr(fr, R):.1f} rpm 이다.  '
                         f'일부러면 --allow-off-band')
    return rpm


def _estar(nu, E=None):
    E = E_YOUNG if E is None else E
    return E / (2.0 * (1.0 - nu ** 2))


def overlap_for_ced(ced, radius, nu, E=None):
    """CED → 평형 겹침 `δ/r` (점착 지배 극한).  ★ 실측 검증: 3e5·SE → 3.31 % vs 3.54 %.
    `E` 를 안 주면 SE 급 1e7 (앵커 시험·하위호환).  상별로는 `E_PHASE[t]` 를 넘긴다."""
    if ced <= 0:
        return 0.0
    rs = radius / 2.0                                   # 같은 크기 두 구의 R*
    return (3.0 * ced * 2.0 * math.pi * math.sqrt(rs) / (4.0 * _estar(nu, E))) ** 2 / radius


def bond_for_ced(ced, radius, nu, rho_gcc, g=9.81, E=None):
    """CED → Bond 수 `F_coh / W`.  **∝ CED³** 이다."""
    if ced <= 0:
        return 0.0
    rs = radius / 2.0
    delta = overlap_for_ced(ced, radius, nu, E) * radius
    f_coh = ced * 2.0 * math.pi * rs * delta
    w = (4.0 / 3.0) * math.pi * radius ** 3 * (rho_gcc * 1000.0) * g
    return f_coh / w


def ced_for_bond(bo, radius, nu, rho_gcc, g=9.81, E=None):
    """목표 Bond 수 → CED.  `Bo ∝ CED³` 이므로 한 점에서 세제곱근으로 뽑는다."""
    if bo <= 0:
        return 0.0
    ref = 1.0e5
    return ref * (bo / bond_for_ced(ref, radius, nu, rho_gcc, g, E)) ** (1.0 / 3.0)


#: 팔 — **Bond 수 배수**를 건다 (CED 배수가 아니다).  나머지는 전부 고정.
#  `mult[(a,b)]` 가 없으면 1.0.  대칭은 코드가 강제한다.
#  ★ 기준 Bond 수는 **천장에서 거꾸로 푼다** — 손으로 박지 않는다.
#    초판은 `CED0 = 3.0e5` 를 박았고 4/5 팔이 접촉모델 밖으로 나갔다.  여기서는
#    `_solve_bond0()` 가 **가장 센 팔이 겹침 천장에 딱 닿도록** 잡으므로, 나중에
#    ×1000 팔을 더해도 사다리 전체가 자동으로 내려앉는다 (시험 ㉙ 가 강제한다).
#: ★★ **모든 팔이 절대 Bo 다** (1저자 비준 2026-09-21, ⑤-1).  `abs_base` = 모든 쌍의 Bo,
#  `abs_mult` = 쌍별 덮어쓰기.  **BOND0(천장에서 거꾸로 푸는 기준)은 폐지**했다 — 지름·영률·
#  상 집합·가장 센 팔의 함수라 덱을 바꾸면 조용히 밀렸다 (실측 0.21244 → 0.28326 → 0.37412,
#  AM_P 지름에 정확히 ∝ 1/d).  천장은 이제 `ced_matrix` 끝의 **단언**이 지킨다 (fail-closed).
#  ⚠ 초판 `abs_mult` 는 목록에 적힌 쌍만 절대였고 나머지는 BOND0 을 썼다 = 반쪽.  `abs_base` 로 닫았다.
#: 사다리 기준값 — **옛 값 승계**.  측정된 H/R 사다리(Bo 0.212 → 1.573 깨끗 · 0.472 → 1.750
#  전이 · 2.124 → 2.020 뭉침 · 경계 ≈ 0.5)와 같은 Bo 를 새 덱에서 다시 재어 잇기 위해서다.
#  ⚠ 그 H/R 값들은 옛 덱(지름·상집합·영률·마찰)의 것이라 **전수 재측정** 대상이다.
BO_BASE = 0.21244


def _am_pairs(bo):
    return {('AM_P', 'AM_P'): bo, ('AM_P', 'AM_S'): bo, ('AM_S', 'AM_S'): bo}


def _se_pairs(bo):
    """SE 가 낀 세 쌍 (SE–SE · AM_P–SE · AM_S–SE) 의 Bo 덮어쓰기 — dev-u (균일 γ 배율) 용.  코팅 팔이면 AM 쌍은 SE–SE Bo 를 따라간다 (`_bo_phase`)."""
    return {('SE', 'SE'): bo, ('AM_P', 'SE'): bo, ('AM_S', 'SE'): bo}


ARMS = {
    'E0': dict(desc='음성 대조 — 점착 0.  지표가 0 을 내는가', bond=0.0),
    'E1': dict(desc='균일 Bo 0.212 (상별 CED 는 다르다 — 그래야 Bo 가 같다)',
               bond=1.0, abs_base=BO_BASE),
    'E2': dict(desc='★ AM 만 Bo 2.124 (×10) — 1저자 질문의 축', bond=1.0,
               abs_base=BO_BASE, abs_mult=_am_pairs(2.1244)),
    'E3': dict(desc='SE 만 Bo 2.124 (×10, 대조)', bond=1.0,
               abs_base=BO_BASE, abs_mult={('SE', 'SE'): 2.1244}),
    'E4': dict(desc='AM 만 Bo 21.24 (×100, 축 확장)', bond=1.0,
               abs_base=BO_BASE, abs_mult=_am_pairs(21.244)),
    #  ★★ 코팅 — **AM 표면이 황화물(SE)이 된다**.  AM 쌍의 CED 를 **SE-SE 값으로 덮는다**.
    #  ⚠ 바꾸는 것은 표면 물성(CED)이지 Bo 가 아니다 — 코팅층은 얇아 크기·질량이 안 바뀌므로
    #    `Bo = F_coh/W` 는 **따라 나오게** 둔다.  ⛔ 피복률 축 없음 = 완전 피복 (1저자 지시).
    'C1': dict(desc='★ AM 에 황화물 코팅 — AM 표면이 SE 가 된다 (완전 피복)',
               bond=1.0, abs_base=BO_BASE, coat={'AM_P': 'SE', 'AM_S': 'SE'}),
    #  ⛔ 고-G 기계 팔 `T1`(Thinky) · `T2`(볼텍스)는 **폐지** (⑤-2, 2026-09-21).  기계는 사다리
    #    위의 **점**이다 — 곡선에서 읽는다.  장비 제원이 바뀌어도(볼텍스 45 → 14.0 G 정정 등)
    #    곡선은 그대로고 화살표만 옮긴다 ⇒ 재실행 불필요.  덮개 검증은 원장 §10.
    #  균일 삽입 경계 탐침 — 층상 `LB2` 와 같은 Bo 0.5 라 **삽입 방식 효과**의 대조쌍이 된다.
    'B5': dict(desc='경계 탐침 — AM Bo 0.5 (균일 삽입)', bond=1.0,
               abs_base=BO_BASE, abs_mult=_am_pairs(0.5)),
    'B10': dict(desc='경계 탐침 — AM Bo 1.0 (균일 삽입)', bond=1.0,
                abs_base=BO_BASE, abs_mult=_am_pairs(1.0)),
    #  ★★ §24 층상 — 헤드라인 *"코팅하면 더 잘 섞이나"*.  AM 을 **아래**에, SE 를 위에.
    #  ★★ 캠페인 (원장 §10, 1저자 비준): L0 · LC · LB1 · LB2 · LB3 · LA = 6 팔, 시드 가중
    #    (LA·LC 3 시드, 나머지 1) = 11 런.  사다리가 있어야 `LA`(3.0) vs `LC` 의 **128배 Bo 차이**와
    #    "코팅" 처리를 갈라 읽을 수 있다 — LC 가 곡선 위면 "코팅 = Bo 낮추기", 벗어나면 그 이상.
    'L0': dict(desc='§24 층상 · 점착 0 — 지표 상한 (음성 대조)', bond=0.0, layered=True),
    'LB1': dict(desc='층상 사다리 · AM Bo 0.1 — 씽키 구간', bond=1.0, layered=True,
                abs_base=BO_BASE, abs_mult=_am_pairs(0.1)),
    'LB2': dict(desc='층상 사다리 · AM Bo 0.5 — 유동성 경계', bond=1.0, layered=True,
                abs_base=BO_BASE, abs_mult=_am_pairs(0.5)),
    'LB3': dict(desc='층상 사다리 · AM Bo 1.5 — 볼텍스(14 G) E4 기준', bond=1.0, layered=True,
                abs_base=BO_BASE, abs_mult=_am_pairs(1.5)),
    #  ⚠ 2026-09-27 — LA·LC 설명 문자열 정정 (R-4 · R-3 · Codex HB-01).  덱에는 **주석 한 줄**로만 들어간다
    #    (물리 명령 불변 — 셀프테스트 ㉟b 가 옛 문자열로 옛 골든 해시를 재현해 보인다).  돌고 있는 런의 덱은 옛 문자열.
    #    옛 LA: '… 무코팅 AM Bo 3.0 = 문헌 앵커 (hare2026) — 헤드라인 무코팅' (R-4 로 철회된 라벨)
    #    옛 LC: '… 코팅 (AM 표면 = SE, C1 규약) — 헤드라인 코팅' (R-3: "코팅" 은 대리일 뿐)
    'LA': dict(desc='§24 층상 · AM–AM Bo_code 3.0 (벽 CED 동반) = 내부 기준점 — 문헌 앵커 아님 (R-4)',
               bond=1.0, layered=True, abs_base=BO_BASE, abs_mult=_am_pairs(3.0)),
    'LC': dict(desc='§24 층상 · AM 표면 CED 를 SE 표면에서 JKR 환산 (C1 규약, AM_P Bo_code 0.00109) — "코팅" 의 대리 (R-3)',
               bond=1.0, layered=True, abs_base=BO_BASE, coat={'AM_P': 'SE', 'AM_S': 'SE'}),
    #  ★ 고-Bo 확장 (2026-09-27, 사전등록 `docs/reviews/mixer_highbo_prereg_20260927.md`) — **LA 와 같은 규약**
    #    (abs_base 0.212 + AM 쌍 abs_mult) 에 Bo 만 38.4.  ⇒ AM–AM **과 AM–벽** 이 함께 오른다 (벽 CED = 대각 ÷
    #    WALL_CED_DIV) = 저자 결정 **B (공동 개입)**.  38.4 = **내부 고-Bo 탐색값** — Hare 분말의 재현·문헌 앵커 아님
    #    (Codex HB-02: JKR pull-off 규약 2 배 모호 · 입경·밀도 다름).  LC 대비 달라지는 CED 는 다섯 쌍뿐이다
    #    (AM_P–AM_P · AM_P–AM_S · AM_S–AM_S · AM_P–벽 · AM_S–벽 — 셀프테스트 ㊼b · `mixer_deck_diff.py` 가 실행 덱으로 강제).
    'LH': dict(desc='고-Bo 확장 · AM–AM Bo_code 38.4 (벽 CED 동반 = 공동 개입 B) — 내부 탐색값, 문헌 재현 아님',
               bond=1.0, layered=True, abs_base=BO_BASE, abs_mult=_am_pairs(38.4)),
    #  ★ 개발 탐색 dev-bo (2026-10-02 · 강성 축 사전등록 `docs/reviews/mixer_highbo_stiffness_prereg_20260929.md` §11 v2.8 · 1저자 "ㄱㄱ") —
    #    **LH 와 같은 규약** (abs_base 0.212 + AM 쌍 abs_mult) 에 AM–AM Bo_code 만 ×10 (384) · ×30 (1152).  ⇒ AM–벽 CED 도 같은 벽 규칙
    #    (대각 ÷ WALL_CED_DIV) 으로 함께 오른다 = 공동 개입 B (AM–AM 만의 개입 아님 · 셀프테스트 BO②).  DEV seed 1 의 2 바퀴 M (LC_ref_r2 ↔
    #    LH_ref_r2 · 10-02 열람) 을 **본 뒤** 정한 개발 탐색 수준 — 확인 팔 아님 · 캠페인 목록 (CAMPAIGN · CAMPAIGN_HIGHBO · REFERENCE) 에 넣지 않는다 (BO④).
    #    정적 평형 겹침 δ/r (CGF 151.4): AM_P 0.214 · 0.445 % · AM_S 0.125 · 0.259 % — 천장 1 % 안 · 충돌 최대 겹침의 상한 아님 (BO⑤).
    'LHx10': dict(desc='개발 탐색 dev-bo · AM–AM Bo_code 384 (LH ×10 · 벽 CED 동반 = 공동 개입 B) — 10-02 개발 M 열람 뒤 정함 · 확인 팔 아님',
                  bond=1.0, layered=True, abs_base=BO_BASE, abs_mult=_am_pairs(384.0)),
    'LHx30': dict(desc='개발 탐색 dev-bo · AM–AM Bo_code 1152 (LH ×30 · 벽 CED 동반 = 공동 개입 B) — 10-02 개발 M 열람 뒤 정함 · 확인 팔 아님',
                  bond=1.0, layered=True, abs_base=BO_BASE, abs_mult=_am_pairs(1152.0)),
    #  ★ 개발 탐색 dev-u (2026-10-05 · 강성 축 사전등록 `docs/reviews/mixer_highbo_stiffness_prereg_20260929.md` §12 v2.9 · 1저자 "ㅇㅇ 그러자" ·
    #    망 수정보다 낮은 우선순위) — **LC 와 같은 규약** (abs_base 0.212 + coat AM→SE) 에 SE 낀 세 쌍 (SE–SE · AM_P–SE · AM_S–SE) 의 Bo 만 ×1000 · ×3000
    #    (212.44 · 637.32).  코팅 상 (AM) 의 목표 Bo 는 SE–SE Bo 를 JKR 기하로 따라 오르고 (`_bo_phase`) 벽은 대각 ÷ 1.842 ⇒ CED **9 비영 원소 전부
    #    같은 배율** ×10 · ×14.422496 (Bo 배수의 세제곱근 · 셀프테스트 U②) = 같은 γ 세계 (LC) 를 키운다 = "균일 γ 배율" (SE 만의 개입 아님 · 혼합쌍은
    #    min 규칙 그대로).  dev-rot · dev-bo M 을 **본 뒤** 정한 개발 탐색 수준 — 확인 팔 아님 · 캠페인 목록에 넣지 않는다 (U④).
    #    정적 평형 겹침 δ/r (CGF 151.4 · SE–SE): soft 0.402 · 0.837 % · ref ×20 0.055 · 0.114 % (U⑤).  ⚠ LU637 은 CGF 200 에서 SE–SE 1.007 % 로
    #    천장 밖 = 생성기가 거부한다 (같은 Bo 면 parcel 이 클수록 겹침이 크다 · 셀프테스트 ㉙ 의 선언 목록 · U⑥) · X = 850 (×4000) 은 151.4 에서도 거부.
    'LU212': dict(desc='개발 탐색 dev-u · 균일 γ 배율 — LC 의 9 비영 CED × 10 (SE 쪽 Bo_code 212.44 = 0.212 × 1000) — 10-02 · 10-03 개발 M 열람 뒤 정함 · 확인 팔 아님',
                  bond=1.0, layered=True, abs_base=BO_BASE, coat={'AM_P': 'SE', 'AM_S': 'SE'}, abs_mult=_se_pairs(1000.0 * BO_BASE)),
    'LU637': dict(desc='개발 탐색 dev-u · 균일 γ 배율 — LC 의 9 비영 CED × 14.422496 (SE 쪽 Bo_code 637.32 = 0.212 × 3000) — 10-02 · 10-03 개발 M 열람 뒤 정함 · 확인 팔 아님',
                  bond=1.0, layered=True, abs_base=BO_BASE, coat={'AM_P': 'SE', 'AM_S': 'SE'}, abs_mult=_se_pairs(3000.0 * BO_BASE)),
}
#: 캠페인 런 목록 — (팔, 시드).  시드는 **소수** (덱이 합성수를 거부한다).
CAMPAIGN_SEEDS = (32452843, 49979687, 67867967)
CAMPAIGN = ([('L0', CAMPAIGN_SEEDS[0]), ('LB1', CAMPAIGN_SEEDS[0]),
             ('LB2', CAMPAIGN_SEEDS[0]), ('LB3', CAMPAIGN_SEEDS[0])]
            + [('LC', sd) for sd in CAMPAIGN_SEEDS] + [('LA', sd) for sd in CAMPAIGN_SEEDS])
#: ★ 고-Bo 확장 (09-27) — **본 캠페인 목록과 분리**한다 (본 캠페인의 10 런 · 판정선은 그대로).  LC 와 같은 시드로 짝짓는다.
CAMPAIGN_HIGHBO = [('LH', sd) for sd in CAMPAIGN_SEEDS]
#: ★ 기준 런 — `measure_mixing_index.py --ref` 의 상대 (S_R² = 완전 무작위 기준).  **균일 삽입 · 점착 0
#  (`E0`) · 회전 0** = 삽입+정착만.  캠페인과 **같은 시드**로 짝짓는다 (자가 리뷰 R-2: 이것 없이는
#  캠페인에 판독기가 없다).  회전 0 이라 비용 ≈ 정착분(~3.6 h)뿐.
REFERENCE = [('E0', sd, 0) for sd in CAMPAIGN_SEEDS]


def _assert_ceiling(arm, M, d, ceiling=None, E=None):
    """모든 상·벽 쌍의 겹침이 천장 안인지 **단언**한다 (BOND0 폐지 후 유일한 안전장치).

    ⚠ 천장 1 % 는 **관례**다 — 실측으로는 δ/r 3.54 % 팔이 멀쩡했고 무너진 팔은 40 % 였다.
      1 % 는 외삽하지 않는 쪽으로 고른 값이다.  이 식은 점착 지배·단일 접촉 극한이므로
      돌린 뒤 `check_contact_validity.py` 로 **반드시** 실측 확인한다.
    `E` (2026-09-30) — 경화 덱의 행렬은 **그 덱의 영률**로 본다 (기본 = `E_PHASE`, 옛 동작 그대로).
    """
    ceiling = OVL_CEILING if ceiling is None else ceiling
    E = E_PHASE if E is None else E
    w = len(TYPES)
    for i, t in enumerate(TYPES):
        nu = PHASE_MECH[t][0]
        for j, ced in ((i, M[i][i]), (w, M[i][w])):
            ov = overlap_for_ced(ced, d[t] / 2.0, nu, E=E[t])
            if ov > ceiling * (1 + 1e-9):
                raise SystemExit(f'⛔ 팔 {arm}: {t}–{"WALL" if j == w else t} 겹침 {ov*100:.3f} % '
                                 f'> 천장 {ceiling*100:.1f} %.  Bo 를 낮추거나 천장을 논의할 것')


def worst_overlap(d):
    """모든 팔에 대해 (겹침, 팔, 상) 최악값 — 셀프테스트·보고용."""
    out = []
    for arm in sorted(ARMS):
        M = ced_matrix(arm, d)
        for i, t in enumerate(TYPES):
            out.append((overlap_for_ced(M[i][i], d[t] / 2.0, PHASE_MECH[t][0], E=E_PHASE[t]), arm, t))
    return max(out)


def _ced_matrix_min(arm, d, dens=None):
    """[옛 규칙 · min] 팔 + 상별 지름 → (n+1)×(n+1) `cohesionEnergyDensity` 행렬.  **마지막 행/열 = 벽.**

    ★ 모든 팔이 **절대 Bo** — `abs_base`(전 쌍) + `abs_mult`(쌍별 덮어쓰기).  BOND0 없음.
    ⚠ 쌍 (i, j) 는 두 상의 목표 CED 중 **작은 쪽** = 보수적인 쪽.  같은 CED 에서 `δ/r` 은
      반경과 무관(ν 만)하므로 **CED 가 낮은 쪽 = 겹침이 작은 쪽**이다.  min() 이라 (i,j)=(j,i).
      ⚠ 이제 상별 E 가 다르므로 (AM 이 104배 단단) 같은 Bo 의 CED 는 AM 이 훨씬 크다 ⇒
        AM–SE 쌍은 **SE 값**이 된다.
    ★ 코팅: 코팅된 상은 **원천 상의 표면**을 갖는다.  옛 판은 CED 를 복사했는데, 상별 E 가
      갈리자 **깨졌다** — SJKR 은 `F = CED·A` 라 힘이 접촉면적(∝ 1/E*²)에 걸려, 104배 단단한
      AM 에 SE 의 CED 를 주면 Bo 가 ~1e-6 (실측) = 코팅 팔이 음성 대조와 같아진다.
      ⇒ **JKR 힘 스케일링**으로 Bo 를 정의한다: 같은 표면에너지면 `F_pull-off = (3/2)πγR*` 이라
        `Bo_t = Bo_src · (r_src² ρ_src)/(r_t² ρ_t)`.  그 Bo 로 상별 CED 를 역산한다 (E 무관).
        AM_P(9 µm)는 SE(1 µm)의 1/81 × 2000/4800 = **1/194** → Bo 0.212 → 0.00109.
      ⚠ 이것은 규약 변경이다 (2026-09-21) — 리뷰 대상 1순위.
    ★ 벽: `M[w][i] = M[i][i] / WALL_CED_DIV` — JKR 힘비 1/6.25 를 SJKR 로 재현.  벽–벽 0.
    ★ 끝에 겹침 천장을 **단언**한다 (fail-closed).
    `dens` (2026-10-14 밤) — 그 덱의 밀도표 (`plan()['dens']`).  None = gen1 `DENS` (옛 행렬 비트 그대로).  같은 Bo_code 를 그 세대의
      무게로 CED 역산한다 (Bo = F_coh / W · W ∝ ρ).
    """
    a = ARMS[arm]
    n = len(TYPES)
    w = n
    dn = DENS if dens is None else dens
    M = [[0.0] * (n + 1) for _ in range(n + 1)]
    if a['bond'] > 0:
        if 'abs_base' not in a:                        # fail-closed (SystemExit = 프로젝트 규약)
            raise SystemExit(f'⛔ 팔 {arm}: 절대 Bo 기준(abs_base)이 없다 — BOND0 상대 팔은 폐지됐다')
        am = a.get('abs_mult') or {}
        coat = a.get('coat') or {}

        def _bo_phase(t, pair_bo):
            """상 t 의 목표 Bo.  코팅된 상은 원천 상의 Bo 를 JKR 기하로 환산한다."""
            if t in coat:
                src = coat[t]
                bo_src = am.get((src, src), a['abs_base'])
                r_s, r_t = d[src] / 2.0, d[t] / 2.0
                rho_s, rho_t = dn[PHASE_MECH[src][1]], dn[PHASE_MECH[t][1]]
                return bo_src * (r_s ** 2 * rho_s) / (r_t ** 2 * rho_t)
            return pair_bo
        for i, ti in enumerate(TYPES):
            for j, tj in enumerate(TYPES):
                pair_bo = am.get((ti, tj), am.get((tj, ti), a['abs_base']))
                cand = []
                for t in (ti, tj):
                    nu, mat = PHASE_MECH[t]
                    cand.append(ced_for_bond(_bo_phase(t, pair_bo) * a['bond'],
                                             d[t] / 2.0, nu, dn[mat], E=E_PHASE[t]))
                M[i][j] = min(cand)
        for i in range(n):
            M[i][w] = M[w][i] = M[i][i] / WALL_CED_DIV
    for i in range(n + 1):
        for j in range(n + 1):
            assert abs(M[i][j] - M[j][i]) < 1e-9, '행렬이 비대칭이다'
    _assert_ceiling(arm, M, d)
    return M


def ced_matrix(arm, d, dens=None):
    """팔 + 상별 지름 → (n+1)×(n+1) `cohesionEnergyDensity` 행렬 (마지막 = 벽).
    ★ 2026-10-14 — 팔의 `rule` 로 고른다: `geomean` = D2 결합 규칙 (`ced_matrix_geomean`) · 그 밖 = 옛 min 규칙 (`_ced_matrix_min`, 비트 그대로).
    `dens` (2026-10-14 밤) = 그 덱의 밀도표 (None = gen1 `DENS` · 옛 행렬 그대로)."""
    a = ARMS[arm]
    if a.get('rule') == 'geomean':
        return ced_matrix_geomean(a, d, dens=dens)
    return _ced_matrix_min(arm, d, dens=dens)


# ══ D2 결합 규칙 — 쌍 접착일 기하평균 (2026-10-14 · 1저자 비준 10-14 D2 (가) · docs/mixer_paper_pipeline_draft_20261013.md §4) ══════════
#  ★ W_ij = 2√(γ_iγ_j) — 혼합쌍과 **벽까지** (같은 상 = 2γ_i).  논지 docs/hetero_thesis.md §2: 비코팅 = γ_A/γ_S 한 노브 · 코팅 = 비 1.
#  ★ 힘 = JKR 스케일 — 당김힘 ∝ W·R* (상수 3π/2 는 비에서 약분) ⇒ F₀_ij = F₀_SS · √(γ_iγ_j)/γ_SE · R*_ij/R*_SS.
#  ★ 절대 수준 = SE–SE Bo_code **하나** (F₀_SS = Bo_SE × SE 무게) — D3 (유동성 실측 + 같은 시험의 DEM 보정) 이 정할 값 · 그 전에는 명시 입력.
#  ★ CED_ij = [F₀_ij · E*_ij² / ((9/2)π³R*_ij²)]^(1/3) — 생성기의 명목 소겹침 점착 힘 척도 (`f0_pair`) 를 쌍마다 맞춘다.
#    F₀ 목표가 E 와 무관하므로 경화 덱 (×F · hold_bo_pairwise) 의 쌍별 F₀ 보존 행렬과 같은 값이 된다 (셀프테스트 GM⑪).
#  ⚠ min 규칙 (옛 팔) 과 다른 점 — 혼합쌍이 작은 쪽 CED 가 아니라 그 쌍의 R* · E* · W 에서 나온다 (논지 §3 "AM–SE min 규칙이 2.2 배 약함" 의 처방) ·
#    벽 = 대각 ÷ 1.842 가 아니라 같은 기하평균 · 겹침 천장 = 대각 · 벽만이 아니라 **모든 쌍** δ₀/min(r).
#  ⚠ γ 의 절대값 · 비코팅 NCM/SE 비는 모른다 (논지 §2-8 판가름 수) — 비는 입력이다.  ⛔ 실제 코팅 · 분말의 재현이라 쓰지 않는다.
#: 벽 γ_W/γ — Hare et al., Powder Technol. 469 (2026) 121804 (litdb 정본 `hare2026_dem_pept_dry_mixing_nmc622_eirich`) Table 3 의 보정값
#  γ_pp 0.25 · γ_pw 0.04 J/m² (EDEM JKR · 짝마다 준 접착 에너지 w = 2γ · NMC622 ↔ 스테인리스) ⇒ w_pW/w_pp = 0.16 = √(γ_W/γ_p) ⇒ γ_W/γ_p = 0.16² = 0.0256.
#  검산: 구–벽 R* = 2 × 구–구 R* ⇒ 당김힘 비 0.32 (Hare 단분산과 같음 · 셀프테스트 GM⑥).  JKR 당김힘 상수 규약 (γ ↔ 2γ) 은 비에서 약분된다.
#  ⚠ 0.0256 은 Hare 의 "입자" 기준 — 그 입자는 비코팅 NMC622 이므로 γ_NCM/γ_SE = ρ ≠ 1 인 런에서는 γ_W/γ_SE = 0.0256·ρ 가 글자 그대로의 이전이다
#    (ρ = 1 = 같은 γ 기준 런에서 0.0256) · ✅ 묶는 상 = 비코팅 NCM (1저자 10-14 Q2 · docs/mixer_d2_wall_gamma_derivation_20261014.md §5) — gm_arm 이 강제한다.
#    ✅ 10-21 표기 정정 (MXD2-05): 옛 표기 "어느 상에 묶을지 = 1저자 결정" 은 10-14 결정 뒤에도 열린 질문처럼 읽혔다.
#  ⛔ 옛 제안 0.0064 (= 당김힘 비 0.16) 는 Hare 의 에너지 비를 당김힘 비로 읽은 옛 벽 규약 (`MIX-12`) 을 이은 값 — 근거 문헌 없음 · 철회 (1저자 10-14 (가)).
#  팔 · CLI 에는 **명시**해야 한다 (숨은 기본값 없음).
GM_WALL_HARE2026 = (0.04 / 0.25) ** 2
GM_WALL_RULE_NCM = 'hare2026_x_rho_uncoated_ncm'
#: ★ 명시 벽 (CLI --gm-gamma-wall · 2026-10-21 MXD2-05) — NCM 상 γ 가 전부 1 인 팔 (코팅 · 같은 γ 세계) 만.  그 벽이 함의하는 비코팅 NCM ρ = γ_W/0.0256.
GM_WALL_RULE_EXPLICIT = 'explicit_coated'
#: ★ deck_meta schema (2026-10-21 · 원장 MXD2-06) — /1 = 옛 키 (강성 · dt · 전 정밀도 덤프) · /2 = /1 + 선택 키 (dens_gen · dens_g_cm3 ·
#   dens_carried_from_gen1 · adhesion_rule).  옛 판은 선택 키를 더하고도 /1 을 적었다 — 키가 없는 메타는 /1 그대로 (바이트 그대로).
MIXER_DECK_META_SCHEMA_V2 = 'mixer_deck_meta/2'
#: ★ D2 덱의 registered (MXD2-06) — D2 덱에는 **결과 전 등록이 아직 없다** (개발).  옛 판은 강성 축 사전등록 §3 을 적었다.  결정의 출처만 적는다.
MIXER_D2_REGISTERED = ('D2 결합 규칙 덱 — 결과 전 등록 없음 (개발 · 등록 전 · 결과 0) · 규칙 = 1저자 10-14 D2 (가) '
                       'docs/mixer_paper_pipeline_draft_20261013.md §4 · 벽 = 1저자 10-14 Q2 docs/mixer_d2_wall_gamma_derivation_20261014.md §5')
#: ★ 지원 범위 (2026-10-21 · 원장 MXD2-04) — γ/γ_SE (NCM · 섬유 상 · ρ_비코팅 · γ_W) · SE–SE Bo_code.  밖이면 거부 (fail-closed).
#  범위 안이면 쌍 곱 γ_iγ_j ∈ [1e-12, 1e12] 라 곱 언더플로 (γ 1e-200 → CED 0 · 리뷰 F3) · 넘침 · 준정규수 (Bo 1e-310) 가 원리적으로 안 생긴다.
#  ⚠ 이 범위는 산술 안전선이지 물리 범위가 아니다 — 물리 쪽은 γ 비 O(10⁻²–10²) (논지 §2-3) · Bo_code 는 겹침 천장 1 % 가 먼저 막는다 (CGF 151.4 · ≈10³).
GM_GAMMA_RANGE = (1e-6, 1e6)
GM_BO_RANGE = (1e-6, 1e4)
#: 팔 이름 — ★ fullmatch 로만 쓴다 (2026-10-21 MXD2-04 · 옛 `^…$` + match 는 끝 줄바꿈 'GM\n' 을 받아 덱에 주석 아닌 줄을 만들었다).
_ARM_NAME_RE = re.compile(r'[A-Za-z][A-Za-z0-9_]{0,31}')
_NCM_PHASES = ('AM_P', 'AM_S')                       # Q2 (벽 = 비코팅 NCM) 가 다루는 상 — 섬유 상 (VGCF · PTFE) 의 γ 는 이 규칙 밖


def gm_wall_from_ncm(rho_uncoated):
    """벽 = 비코팅 NCM 에 묶기 (1저자 10-14 Q2) — γ_W = 0.0256 × γ_NCM(비코팅) ⇒ 생성기 단위 γ_W/γ_SE = 0.0256 × ρ_비코팅.
    같은 ρ 세계의 코팅 팔도 **이 값 (비코팅 ρ 로 정한 벽)** 을 쓴다 — 코팅은 NCM 표면만 바꾸고 강철 · SE 는 안 바꾼다."""
    return GM_WALL_HARE2026 * _gm_num(rho_uncoated, 'ρ_비코팅 NCM = γ_NCM/γ_SE', GM_GAMMA_RANGE)


def _gm_num(v, what, rng):
    """유한한 실수 · 지원 범위 안만 (bool · 문자열 · NaN · ∞ · 범위 밖 = 0 · 음수 · 준정규수 · 넘침 거부).  사유를 따로 낸다 (유한 / 범위)."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise SystemExit(f'⛔ D2 결합 규칙: {what} = {v!r} — 수가 아니다')
    v = float(v)
    if not math.isfinite(v):
        raise SystemExit(f'⛔ D2 결합 규칙: {what} = {v!r} — 유한하지 않다 (NaN · ∞)')
    lo, hi = rng
    if not (lo <= v <= hi):
        raise SystemExit(f'⛔ D2 결합 규칙: {what} = {v!r} — 지원 범위 [{lo:g}, {hi:g}] 밖 (0 · 음수 · 언더플로 · 넘침 거부 · MXD2-04)')
    return v


def _gm_text(s, what):
    """덱 주석 줄에 들어가는 글 — 비어 있지 않은 400 자 이하 문자열 · 제어 · 서식 문자 (줄바꿈 · CR · 탭 · NUL · DEL · 영폭 등 유니코드 C 범주) 없음."""
    if not isinstance(s, str) or not s or len(s) > 400:
        raise SystemExit(f'⛔ D2 결합 규칙: {what} {s!r} — 비어 있지 않은 400 자 이하 문자열이어야 한다')
    bad = sorted({c for c in s if unicodedata.category(c)[0] == 'C'})
    if bad:
        raise SystemExit(f'⛔ D2 결합 규칙: {what} 에 제어 문자 {bad!r} — 덱 주석 줄을 깨뜨린다 (주석 아닌 줄 · 줄 잇기 · MXD2-04)')
    return s


#: ★ CLI 수 토큰 (2026-10-21 · 원장 MXD2-04) — ASCII 십진수만.  float() 는 밑줄 ('0_3' → 3.0) · 전각 숫자 ('０.３' → 0.3) · nan · inf 를 받는다.
_ASCII_DEC_RE = re.compile(r'(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?')


def ascii_decimal(s, what):
    """CLI 수 토큰 → float — 앞뒤 공백만 허용 · ASCII 십진수 (지수 표기 허용) 가 아니면 거부 (밑줄 · 전각 · nan · inf · 부호)."""
    t = s.strip() if isinstance(s, str) else None
    if t is None or not _ASCII_DEC_RE.fullmatch(t):
        raise SystemExit(f'⛔ {what} = {s!r} — ASCII 십진수가 아니다 (밑줄 · 전각 숫자 · nan · inf · 부호 금지 · MXD2-04)')
    return float(t)


def _ascii_float_arg(s):
    """argparse type — ascii_decimal (거부는 ArgumentTypeError → argparse 가 rc 2 로 끝낸다)."""
    try:
        return ascii_decimal(s, '값')
    except SystemExit as e:
        raise argparse.ArgumentTypeError(str(e))


def gm_arm(gamma, gamma_wall=None, bo_se=None, layered=True, desc=None, rho_uncoated_ncm=None):
    """D2 결합 규칙 팔 사전을 만든다 (등록은 `register_arm`).  `gamma` = 도는 상 (`TYPES`) 전부의 γ/γ_SE (SE = 정확히 1) ·
    `gamma_wall` = γ_W/γ_SE · `bo_se` = SE–SE Bo_code (절대 수준).  셋 다 명시 — 숨은 기본값 없음 (fail-closed).
    ★ 2026-10-21 (원장 MXD2-05) — 벽 = 비코팅 NCM (1저자 10-14 Q2) 을 **강제**한다:
      · `rho_uncoated_ncm` = ρ (CLI --gm-wall-ncm) — γ_W 는 정확히 0.0256·ρ 이고 NCM 상 (AM_P · AM_S) 의 γ 는 1 (코팅) 또는 ρ (비코팅) 만
      · 안 주면 (CLI --gm-gamma-wall) NCM 상 γ 가 전부 1 인 팔 (코팅 · 같은 γ 세계) 만 — 그 벽의 비코팅 NCM ρ = γ_W/0.0256 을 함의로 기록
      · 섬유 상 (5 상 카탈로그의 VGCF · PTFE) 의 γ 는 이 규칙 밖 (Q2 는 NCM 에 대한 결정이다)
    ★ 지원 범위 (GM_GAMMA_RANGE · GM_BO_RANGE) · 설명 (desc) 의 제어 문자 = 거부 (MXD2-04)."""
    if not isinstance(gamma, dict):
        raise SystemExit(f'⛔ D2 결합 규칙: gamma 는 상 → γ/γ_SE 사전이어야 한다 ({gamma!r})')
    keys = set(gamma)
    if keys != set(TYPES):
        raise SystemExit(f'⛔ D2 결합 규칙: gamma 의 상 {sorted(keys)} ≠ 도는 상 {list(TYPES)} — 빠지거나 남는 상은 거부')
    g = {t: _gm_num(gamma[t], f'γ_{t}/γ_SE', GM_GAMMA_RANGE) for t in TYPES}
    if g['SE'] != 1.0:
        raise SystemExit(f"⛔ D2 결합 규칙: 기준 γ_SE/γ_SE 는 정확히 1 이어야 한다 ({g['SE']!r})")
    if gamma_wall is None or bo_se is None:
        raise SystemExit('⛔ D2 결합 규칙: gamma_wall (γ_W/γ_SE) 와 bo_se (SE–SE Bo_code) 를 명시해야 한다 — 숨은 기본값 없음')
    gw = _gm_num(gamma_wall, 'γ_W/γ_SE', GM_GAMMA_RANGE)
    bo = _gm_num(bo_se, 'SE–SE Bo_code', GM_BO_RANGE)
    ncm = [t for t in TYPES if t in _NCM_PHASES]
    q2 = '1저자 10-14 Q2 — 벽 = 비코팅 NCM · docs/mixer_d2_wall_gamma_derivation_20261014.md §5'
    if rho_uncoated_ncm is not None:                 # 벽 = 비코팅 NCM 에 묶음 — 값이 규칙과 정확히 같고 NCM 상은 코팅 (1) · 비코팅 (ρ) 만
        rho = _gm_num(rho_uncoated_ncm, 'ρ_비코팅 NCM = γ_NCM/γ_SE', GM_GAMMA_RANGE)
        if gw != gm_wall_from_ncm(rho):
            raise SystemExit(f'⛔ D2 결합 규칙 ({q2}): γ_W/γ_SE {gw!r} ≠ 0.0256 × ρ_비코팅 {rho!r} — 벽 규칙과 값이 어긋난다')
        off = {t: g[t] for t in ncm if g[t] not in (1.0, rho)}
        if off:
            raise SystemExit(f'⛔ D2 결합 규칙 ({q2}): ρ_비코팅 {rho:g} 세계의 NCM 상 γ/γ_SE 는 1 (코팅) 또는 ρ (비코팅) 만 — {off} '
                             f'(비코팅 NCM 의 ρ 는 하나다 · MXD2-05)')
        wall_rule, rho_world = GM_WALL_RULE_NCM, rho
    else:                                            # 명시 벽 — 코팅 팔 (NCM 상 γ 전부 1) 만 · 함의 ρ 기록
        off = {t: g[t] for t in ncm if g[t] != 1.0}
        if off:
            raise SystemExit(f'⛔ D2 결합 규칙 ({q2}): 명시 벽 (--gm-gamma-wall) 은 NCM 상 γ 가 전부 1 인 팔 (코팅 · 같은 γ 세계) 에서만 — {off} · '
                             f'비코팅 팔은 --gm-wall-ncm ρ (γ_W = 0.0256·ρ) 로 (MXD2-05)')
        wall_rule, rho_world = GM_WALL_RULE_EXPLICIT, gw / GM_WALL_HARE2026
    if desc is None:
        desc = ('D2 결합 규칙 (기하평균 W_ij = 2√(γ_iγ_j) · 혼합쌍 · 벽) · γ/γ_SE '
                + ' · '.join(f'{t} {g[t]:g}' for t in TYPES) + f' · γ_W/γ_SE {gw:g} · SE–SE Bo_code {bo:g} — 개발 · 등록 전 (결과 0)')
    _gm_text(desc, '팔 설명 (desc)')
    arm = dict(desc=desc, bond=1.0, layered=bool(layered), rule='geomean', gamma=g, gamma_wall=gw, bo_se=bo, _gm_valid=True,
               wall_rule=wall_rule, rho_world=rho_world, surface={t: ('coated' if g[t] == 1.0 else 'uncoated') for t in ncm})
    if rho_uncoated_ncm is not None:
        arm['rho_uncoated_ncm'] = rho
    return arm


def register_arm(name, arm):
    """런타임 팔 등록 (CLI `--gm-*` · 셀프테스트).  옛 팔 이름을 덮어쓰지 않는다 · 이름 형식 검사 (fullmatch) · D2 팔은 `gm_arm` 이 만든 것만."""
    if not isinstance(name, str) or not _ARM_NAME_RE.fullmatch(name):
        raise SystemExit(f'⛔ 팔 이름 {name!r} — 영문자로 시작하는 영숫자 · _ (최대 32 자)')
    if name in ARMS:
        raise SystemExit(f'⛔ 팔 {name} 은 이미 있다 — 덮어쓰지 않는다')
    if arm.get('rule') == 'geomean' and not arm.get('_gm_valid'):
        raise SystemExit('⛔ D2 결합 규칙 팔은 gm_arm 으로 만든다 (검증 우회 거부)')
    ARMS[name] = arm
    return name


def pair_overlap(ced, ti, tj, d, E):
    """쌍 (ti, tj) 의 점착 지배 평형 겹침 δ₀ = (B/A)² = (3π·CED·√R*/(2E*))² 을 **작은 반경**으로 나눈 값 (벽 = 입자 반경).
    같은 상이면 `overlap_for_ced` 와 같다 (셀프테스트 GM⑨)."""
    if ced <= 0:
        return 0.0
    rs = rstar_pair(ti, tj, d)
    es = estar_pair(ti, tj, E)
    rmin = min(d[t] / 2.0 for t in (ti, tj) if t != WALL)
    return (3.0 * math.pi * ced * math.sqrt(rs) / (2.0 * es)) ** 2 / rmin


def _assert_ceiling_pairwise(arm, M, d, E):
    """모든 쌍 (벽 포함 · 벽–벽 제외) 의 δ₀/min(r) 이 천장 안인지 단언 (fail-closed) — D2 팔 전용 (옛 팔은 `_assert_ceiling` 그대로)."""
    names = list(TYPES) + [WALL]
    for i in range(len(names)):
        for j in range(i, len(names)):
            ti, tj = names[i], names[j]
            if ti == WALL and tj == WALL:
                continue
            ov = pair_overlap(M[i][j], ti, tj, d, E)
            if not math.isfinite(ov) or ov > OVL_CEILING * (1 + 1e-9):
                raise SystemExit(f'⛔ 팔 {arm}: {ti}–{tj} 겹침 {ov*100:.3f} % > 천장 {OVL_CEILING*100:.1f} % (D2 쌍별) — Bo_SE 를 낮추거나 천장을 논의할 것')


def ced_matrix_geomean(a, d, E=None, dens=None):
    """D2 결합 규칙 — 팔 사전 `a` (`gm_arm`) + 상별 지름 → (n+1)×(n+1) CED 행렬 (마지막 = 벽).  위 절 주석이 정의다.
    `E` = 이 덱의 상별 영률 (기본 `E_PHASE`).  F₀ 목표는 E 와 무관하고 CED 만 E 를 따른다.
    `dens` (2026-10-14 밤) = 그 덱의 밀도표 — 절대 수준 F₀_SS = Bo_SE × SE 무게 (∝ ρ_SE) 에 들어간다 (None = gen1 `DENS`).
      ⚠ D2 **덱**은 세대를 명시해야 만들어진다 (`deck` · `deck_meta` 가 거부) — 이 함수 자체는 행렬 산술이라 기본값을 둔다."""
    if not (isinstance(a, dict) and a.get('rule') == 'geomean' and a.get('_gm_valid')):
        raise SystemExit('⛔ D2 결합 규칙: gm_arm 으로 만든 팔 사전이 아니다 (검증 우회 거부)')
    a = dict(a, **gm_arm(a['gamma'], gamma_wall=a['gamma_wall'], bo_se=a['bo_se'], layered=a['layered'], desc=a['desc'],
                         rho_uncoated_ncm=a.get('rho_uncoated_ncm')))
    E = E_PHASE if E is None else E
    names = list(TYPES) + [WALL]
    g = dict(a['gamma'])
    g[WALL] = a['gamma_wall']
    nu_se, mat_se = PHASE_MECH['SE']
    ced_ss = ced_for_bond(a['bo_se'], d['SE'] / 2.0, nu_se, (DENS if dens is None else dens)[mat_se], E=E['SE'])
    rss = rstar_pair('SE', 'SE', d)
    f_ss = f0_pair(ced_ss, rss, estar_pair('SE', 'SE', E))
    #  ★ 사후 단언 (2026-10-21 · 원장 MXD2-04 · 방어 깊이) — 절대 수준 F₀_SS 와 벽–벽 밖 모든 CED 는 유한한 **정규** 양수여야 한다.
    #    지원 범위 (gm_arm) 가 원인 (γ 곱 언더플로 · 준정규수 Bo) 을 먼저 막지만, 범위가 바뀌어도 0 · 준정규 CED 덱은 쓰지 않는다
    #    (옛 판: γ_AM_P 1e-200 이면 AM_P–AM_P CED 0 인데 AM_P–SE · AM_P–벽은 양수인 덱을 썼다 · 리뷰 F3).
    if not (math.isfinite(f_ss) and f_ss >= sys.float_info.min):
        raise SystemExit(f'⛔ D2 결합 규칙: F₀_SS = {f_ss!r} N — 유한한 정규 양수가 아니다 (Bo_SE {a["bo_se"]!r} · MXD2-04)')
    n = len(names)
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            ti, tj = names[i], names[j]
            if ti == WALL and tj == WALL:
                continue
            rs = rstar_pair(ti, tj, d)
            es = estar_pair(ti, tj, E)
            f = f_ss * math.sqrt(g[ti] * g[tj]) * rs / rss
            M[i][j] = M[j][i] = (f * es ** 2 / (4.5 * math.pi ** 3 * rs ** 2)) ** (1.0 / 3.0)
            if not (math.isfinite(M[i][j]) and M[i][j] >= sys.float_info.min):
                raise SystemExit(f'⛔ D2 결합 규칙: {ti}–{tj} CED = {M[i][j]!r} — 벽–벽 밖 CED 는 유한한 정규 양수여야 한다 '
                                 f'(γ 곱 언더플로 · 넘침 · MXD2-04)')
    _assert_ceiling_pairwise(a.get('desc', 'D2'), M, d, E)
    return M


# ══ 강성 축 — SE 만 경화 + 쌍별 F₀ 보존 (2026-09-30) ═══════════════════════════════════════════════════════════════════
#  사전등록 `docs/reviews/mixer_highbo_stiffness_prereg_20260929.md` §3 (Codex 6 차 HBR6-02 · 7 차 §5 조건부 동의).
#  ⛔ 왜 `ced_matrix` 를 새 E 로 다시 부르지 않나 — 그것이 **옛 동일상 규칙**이다: 상별 CED 를 `min` 으로 조립하므로 AM–SE 는 SE 의
#    CED 배수 (×14 에서 5.809) 를 그대로 받고 (E* 는 ×12.41 뿐) SE–벽은 새 대각 ÷ 1.842 로 다시 만들어진다 ⇒ F₀ 가 혼합쌍 ×1.272 ·
#    벽 ×1.182 로 어긋난다 (셀프테스트 ST⑤ 가 그 결함을 재현한다).  ⇒ **기존 soft 행렬의 각 원소**를 기준으로 쌍마다 따로 역산한다.
#  ★ 불변량 = 쌍별 **명목 소겹침 점착 힘 척도** F₀ = B³/A² = (9/2)π³R*²CED³/E*²  (A = (4/3)E*√R* · B = 2πR*·CED — 생성기의
#    점착 지배 · 고립 접촉 근사) ⇒ `CED_new,ij = CED_soft,ij · (E*_new,ij / E*_soft,ij)^(2/3)`.  R* 는 같은 쌍의 전후에서 같아 약분된다.
#  ⚠ 남기는 차이 (보존 못 함 · 사전등록 §3): 분리 일 U_sep = Bδ₀²/10 ∝ E*^(−2/3) · 접촉시간 · 접선 강성 · 감쇠 · 이력 · AM/SE 영률비
#    103.7 → 7.407 (×14) · 실제 SJKR 의 구 교차 면적 ≠ 소겹침 선형식 (메시 벽은 area_ratio 도).  F₀ 보존은 **명목 점착력 대 중력의
#    척도를 유지하며 강성을 바꾸는 민감도 경로**이지 SJKR 동역학 전체의 불변이 아니다.
def _nu_of(t):
    return WALL_NU if t == WALL else PHASE_MECH[t][0]


def estar_pair(ti, tj, E):
    """Hertz 유효 영률 E*_ij = [(1−ν_i²)/E_i + (1−ν_j²)/E_j]⁻¹ — 벽은 **선언된 벽 영률 · 포아송비** (무한 강체로 바꾸지 않는다)."""
    return 1.0 / ((1.0 - _nu_of(ti) ** 2) / E[ti] + (1.0 - _nu_of(tj) ** 2) / E[tj])


def rstar_pair(ti, tj, d):
    """유효 반경 — 입자쌍 r_i·r_j/(r_i+r_j) · 벽 (평면) 은 R* = r_입자."""
    if ti == WALL:
        ti, tj = tj, ti
    ri = d[ti] / 2.0
    if tj == WALL:
        return ri
    rj = d[tj] / 2.0
    return ri * rj / (ri + rj)


def f0_pair(ced, rs, es):
    """명목 소겹침 점착 힘 척도 F₀ = B³/A² = (9/2)π³R*²CED³/E*² (N).  δ₀ = (B/A)² 에서 F₀ = B·δ₀."""
    return 4.5 * math.pi ** 3 * rs ** 2 * ced ** 3 / es ** 2


def hold_bo_pairwise_matrix(M_soft, E_soft, E_new):
    """soft 행렬 → 쌍별 F₀ 보존 행렬.  `CED_new,ij = CED_soft,ij · (E*_new,ij / E*_soft,ij)^(2/3)`.

    ★ 원소마다 따로 — 상별 CED 를 다시 `min` 으로 조립하지 않고 SE–벽을 대각에서 다시 만들지 않는다 (HBR6-02).
    ★ 0 은 정확히 0 (0/0 비 없음) · E* 가 그대로인 쌍 (AM–AM · AM–벽) 은 배수가 정확히 1.0 이라 CED 도 비트 그대로.
    ⛔ 모양이 (상 수 + 1)² 가 아니거나 · 비대칭 · 비유한 · 음수면 거부 (fail-closed).
    """
    names = list(TYPES) + [WALL]
    n = len(names)
    if len(M_soft) != n or any(len(r) != n for r in M_soft):
        raise SystemExit(f'⛔ 쌍별 역산: soft 행렬이 {n}×{n} (상 {TYPES} + 벽) 이 아니다')
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            c = M_soft[i][j]
            if M_soft[j][i] != c:
                raise SystemExit(f'⛔ 쌍별 역산: soft 행렬이 비대칭이다 ({names[i]},{names[j]})')
            if not (math.isfinite(c) and c >= 0.0):
                raise SystemExit(f'⛔ 쌍별 역산: soft CED ({names[i]},{names[j]}) = {c!r} — 유한한 비음수여야 한다')
            if c == 0.0:
                continue
            f = (estar_pair(names[i], names[j], E_new) / estar_pair(names[i], names[j], E_soft)) ** (2.0 / 3.0)
            M[i][j] = M[j][i] = c * f
    return M


def stiffness_rows(d, M_soft, M_new, E_soft, E_new):
    """쌍별 표 (머리 주석 · deck_meta.json) — 상 쌍 (i ≤ j, 벽 포함) 마다 R* · E* · CED · F₀ (soft → new) · F₀ 비 (0 이면 None)."""
    names = list(TYPES) + [WALL]
    rows = []
    for i in range(len(names)):
        for j in range(i, len(names)):
            ti, tj = names[i], names[j]
            ww = ti == WALL and tj == WALL
            rs = None if ww else rstar_pair(ti, tj, d)
            es_s = None if ww else estar_pair(ti, tj, E_soft)
            es_n = None if ww else estar_pair(ti, tj, E_new)
            c_s, c_n = M_soft[i][j], M_new[i][j]
            f_s = None if ww else f0_pair(c_s, rs, es_s)
            f_n = None if ww else f0_pair(c_n, rs, es_n)
            rows.append(dict(pair=f'{ti}–{tj}', i=i + 1, j=j + 1, R_star_m=rs, E_star_soft_Pa=es_s, E_star_Pa=es_n,
                             CED_soft=c_s, CED=c_n, F0_soft_N=f_s, F0_N=f_n,
                             F0_ratio=(f_n / f_s) if (f_s and f_n is not None) else None))
    return rows


def _dt_k(dt_factor):
    """`--dt-factor X` → 정수 k = 1/X.  step 수 · 덤프 간격 step 을 **정확히 k 배** 해야 물리 시간 · 덤프 시각이 안 바뀌므로
    1/X 가 정수가 아닌 X (0.3 · 2 · 0 · 음수 · NaN) 는 거부한다."""
    try:
        X = float(dt_factor)
    except (TypeError, ValueError):
        raise SystemExit(f'⛔ --dt-factor {dt_factor!r} — 수가 아니다')
    if not (math.isfinite(X) and 0.0 < X <= 1.0):
        raise SystemExit(f'⛔ --dt-factor {dt_factor!r} — (0, 1] 이어야 한다 (dt 를 늘리지 않는다)')
    k = int(round(1.0 / X))
    if k < 1 or abs(k * X - 1.0) > 1e-12:
        raise SystemExit(f'⛔ --dt-factor {X:g} — 1/X = {1.0 / X:.6g} 이 정수가 아니다.  step · 덤프 간격을 정확히 정수배할 수 '
                         f'없으면 물리 시간 · 덤프 시각이 어긋난다 (예: 0.5 · 0.25)')
    return k


def volume_fractions(dens=None):
    """활성 상(`TYPES`)만의 부피분율·wt%.  **빠진 상의 질량은 재정규화한다.**

    ⚠ 그래서 VGCF·PTFE 를 빼면 AM:SE 가 80:18 → 81.63:18.37 이 된다 — 두 상 **사이의**
      비는 실물 그대로이고(1.6 g : 0.36 g), 바뀌는 것은 "전체 중 몇 %" 라는 라벨뿐이다.
    `dens` (2026-10-14 밤) = 밀도표 (None = gen1 `DENS` · 옛 값 그대로).  wt% 는 세대와 무관하고 부피분율만 바뀐다
      (1저자 레시피 80:18 · P:S 7:3 의 SE 부피 몫 gen1 0.3506 → lab20261014 0.3995 — 셀프테스트 DG③).
    """
    dn = DENS if dens is None else dens
    raw = {'AM_P': WT['AM'] * PS[0] / sum(PS), 'AM_S': WT['AM'] * PS[1] / sum(PS),
           'SE': WT['SE'], 'VGCF': WT['VGCF'], 'PTFE': WT['PTFE']}
    tot_w = sum(raw[k] for k in TYPES)
    wt = {k: raw[k] * 100.0 / tot_w for k in TYPES}
    rho = {k: PHASE_MECH[k][1] for k in TYPES}
    v = {k: wt[k] / dn[rho[k]] for k in TYPES}
    tot = sum(v.values())
    return {k: v[k] / tot for k in v}, wt


def stiffened_e(stiffen_se=1.0):
    """상별 영률 — **SE 만 ×F** (AM_P · AM_S · 벽 · 섬유 불변).  F = 1 이면 `E_PHASE` 와 같은 float 그대로.

    강성 축 (사전등록 `docs/reviews/mixer_highbo_stiffness_prereg_20260929.md` §3 · 이름 그대로 *"SE-only stiffness sensitivity"*).
    ⛔ 거부 — F 가 유한한 양수가 아니면 · 경화한 SE 영률이 덱 인쇄 (`youngsModulus … :.4g`) 에 **정확히** 안 들어가면
      (예: 15.857 → 1.5857e8 이 덱에 1.586e+08 로 찍힌다 = 쌍별 역산에 쓴 E ≠ 실제로 도는 E).  14 · 28 은 정확하다.
    """
    try:
        F = float(stiffen_se)
    except (TypeError, ValueError):
        raise SystemExit(f'⛔ --stiffen-se {stiffen_se!r} — 수가 아니다')
    if not (math.isfinite(F) and F > 0.0):
        raise SystemExit(f'⛔ --stiffen-se {stiffen_se!r} — 유한한 양수여야 한다')
    E = dict(E_PHASE)
    if F != 1.0:
        E['SE'] = E_PHASE['SE'] * F
        if float(f"{E['SE']:.4g}") != E['SE']:
            raise SystemExit(f"⛔ --stiffen-se {F:g} → SE 영률 {E['SE']!r} Pa 가 덱 인쇄 정밀도 (4 유효숫자 → "
                             f"`{E['SE']:.4g}`) 에 정확히 안 들어간다 — 쓰인 E 와 쌍별 역산에 쓴 E 가 갈린다.  "
                             f"영률이 4 유효숫자로 끝나는 배수를 고를 것 (예: 14 · 28)")
    return E


def plan(n_total, cgf=200.0, fill=0.30, pack=0.60, drum_r_over_l=2.5, stiffen_se=1.0, dens_gen=None):
    """조성 → 개수 · 드럼 치수 · 시간스텝.  **순수 함수**라 시험 가능하다.

    ★ `dens_gen` (2026-10-14 밤 · docs/density_generations_20261014.md) — 밀도 세대.  None = gen1 `DENS` **그 객체** (옛 계획 · 덱 비트
      그대로 · 기록 없음) · 이름 = 그 세대 밀도로 부피분율 → 템플릿 수 · 드럼 · Rayleigh dt (그리고 `deck` 의 Bo ↔ CED 환산 · density constant)
      를 다시 낸다.  반환에 `dens` (그 표) · `dens_gen` (None 또는 이름) 을 더한다 — 덱 머리 · deck_meta 의 기록은 이름이 있을 때만.

    ★ 지름은 전부 `D_REAL_UM` 에서 나온다 (비율 노브 없음).  옛 `d_se_over_am` ·
      `d_fib_over_am` 인자는 **삭제**했다 — 아무도 넘기지 않으면서 표를 무력화하고
      있었다 (선언 ≠ 사용).  셀프테스트 ㊵ 가 "표 = 사용" 을 강제한다.
    ★ `stiffen_se` (2026-09-30, 강성 축) — SE 영률만 ×F 로 두고 dt 를 **같은 Rayleigh 규칙**으로 새 E 에서 다시 낸다.
      치수 · 개수 · 드럼은 E 와 무관하다.  반환에 `E` (상별 영률 · 벽 포함) · `stiffen_se` · `dt_by` (dt 를 정한 상) 를 더한다.
      ⚠ soft (F = 1) 에서 dt 를 정하는 상은 SE 가 아니라 **AM_S** 다 (캠페인 계획: AM_S 0.7055 µs < SE 1.1719 µs) —
        그래서 ×14 의 step 배수는 √14 = 3.74 가 아니라 **2.2525** 다 (Codex 7 차 §5-1 산술과 같다).
    """
    dn = dens_table(dens_gen)                                 # 모르는 세대 = 거부 (덱을 쓰기 전)
    E = stiffened_e(stiffen_se)
    phi, wt = volume_fractions(dn)
    d = {k: D_REAL_UM[k] * 1e-6 * cgf for k in TYPES}        # m
    #  ⚠⚠ LIGGGHTS `particledistribution/discrete` 는 분율을 **mass%** 로 읽는다
    #    (실행으로 확인: 로그가 "distribution based on mass%" 를 먼저 찍고 number% 를 유도한다).
    #    초판은 개수분율을 넣어 AM_P 가 744 → **6개**로 들어갔다.
    #    ⇒ 우리 조성이 이미 wt% 이므로 **그대로 넣는다**.
    #  섬유 — 구 개수는 종횡비가 정한다 (길이는 CGF 로 같이 늘어난다)
    L_fib = L_FIB_UM * 1e-6 * cgf
    fibres = tuple(t for t in FIBRE_TYPES if t in TYPES)
    nsph = max(2, int(round(L_fib / d[fibres[0]]))) if fibres else 1
    NSPH = {k: (nsph if k in fibres else 1) for k in TYPES}
    rho_i = {k: dn[PHASE_MECH[k][1]] for k in TYPES}
    #  템플릿 1개의 질량 (섬유는 구 nsph 개)
    #  ★ 섬유는 구가 겹쳐 있어 nsph 개 합보다 가볍다 — 기하로 보정한다 (실측 +3.8 % 편향 제거)
    fac = {k: (chain_volume_factor(NSPH[k]) if NSPH[k] > 1 else 1.0) for k in d}
    m_tpl = {k: NSPH[k] * fac[k] * rho_i[k] * 1000.0 * (math.pi / 6) * d[k] ** 3 for k in d}
    massfrac = {k: wt[k] / 100.0 for k in wt}
    #  템플릿 개수비 = 질량분율 / 템플릿질량
    c = {k: massfrac[k] / m_tpl[k] for k in d}
    per = sum(c.values())
    #  `particles_in_region` 은 **템플릿** 수다.  목표는 원자 수로 준다.
    atoms_per_tpl = sum(c[k] / per * NSPH[k] for k in d)
    n_tpl_total = int(round(n_total / atoms_per_tpl))
    n_tpl = {k: int(round(n_tpl_total * c[k] / per)) for k in d}
    n = {k: n_tpl[k] * NSPH[k] for k in d}                    # 원자 수
    n_fib = {k: n_tpl[k] for k in fibres}
    #  드럼 — 고체 부피에서 역산
    v_solid = n['AM_P'] * (math.pi / 6) * d['AM_P'] ** 3 / phi['AM_P']
    v_drum = v_solid / (fill * pack)
    R = (drum_r_over_l * v_drum / math.pi) ** (1 / 3.0)
    L = R / drum_r_over_l
    #  시간스텝 — Rayleigh 의 20 %, 상마다 (반지름 · 밀도 · 영률 · ν) 로 내고
    #  ★ 상별 영률로 상별 Rayleigh dt 를 내고 **최소**를 쓴다 — 어느 상이 정하는지는 영률에 달렸다 (정정 2026-09-30):
    #    soft 캠페인 = **AM_S** (A안 AM 1.037e9 라 AM_S 가 SE 보다 작다) · SE ×14 이상 = SE.  반환의 `dt_by` 가 실제로 정한 상이다.
    dts = []
    for t in TYPES:
        nu_t, mat = PHASE_MECH[t]
        G = E[t] / (2.0 * (1.0 + nu_t))
        dts.append(0.2 * math.pi * (d[t] / 2) * math.sqrt(dn[mat] * 1000.0 / G)
                   / (0.1631 * nu_t + 0.8766))
    dt = min(dts)
    rpm_crit = 60 / (2 * math.pi) * math.sqrt(9.81 / R)
    return dict(phi=phi, wt=wt, d=d, n=n, n_tpl=n_tpl, n_tpl_total=n_tpl_total,
                massfrac=massfrac, n_fib=n_fib, nsph=nsph, L_fib=L_fib,
                v_solid=v_solid, v_drum=v_drum, R=R, L=L, dt=dt,
                rpm_crit=rpm_crit, cgf=cgf, stl_scale=R / 0.5, n_total=sum(n.values()),
                E=E, stiffen_se=float(stiffen_se), dt_by=TYPES[dts.index(dt)],
                dens=dn, dens_gen=dens_gen)


def chain_volume_factor(nsph, spacing_over_d=0.8):
    """겹친 구 사슬의 부피 / (구 부피 × nsph).

    ⚠ 이 보정이 없으면 섬유 질량을 **과대**평가해 LIGGGHTS 가 1 wt% 를 맞추려고
      가닥을 더 넣는다 (실측 +3.8 %).  등반경 렌즈 부피는 해석적이다:
        d = s·D,  δ = D − d,  V_lens = π δ²(d + 2D)/12
    """
    if nsph < 2:
        return 1.0
    D = 1.0
    d = spacing_over_d * D
    delta = D - d
    v_sph = (math.pi / 6) * D ** 3
    v_lens = math.pi * delta ** 2 * (d + 2 * D) / 12.0
    return (nsph * v_sph - (nsph - 1) * v_lens) / (nsph * v_sph)


def fibre_file(nsph, d_sph):
    """multisphere 구 파일 — `x y z radius` 한 줄씩 (튜토리얼 `stone1.multisphere` 형식).

    ⚠ 겹치게 둔다 (중심간 거리 = 0.8·d).  떨어뜨리면 강체가 아니라 염주가 된다.
    """
    step = 0.8 * d_sph
    x0 = -0.5 * step * (nsph - 1)
    return ''.join(f'{x0 + i*step:.8g} 0 0 {d_sph/2:.8g}\n' for i in range(nsph))


def _write_fibres(data_dir, p):
    """활성 섬유 상의 multisphere 파일만 쓴다.  섬유가 없으면 아무것도 안 쓴다.

    ⚠ 옛 판은 VGCF·PTFE 파일을 **무조건** 써서 3 상 덱에서 `KeyError: 'VGCF'` 로 죽었다.
    """
    for t in FIBRE_TYPES:
        if t in TYPES:
            with open(os.path.join(data_dir, f'{t.lower()}.multisphere'), 'w') as f:
                f.write(fibre_file(p['nsph'], p['d'][t]))


def settle_time(drop_m, restitution=0.3, g=9.81, margin=2.0):
    """정착 시간 — **유도값**이지 눈대중이 아니다.

    반발계수 e 의 공에서 튐의 총 시간은 등비급수로 `t_ff·(1+e)/(1−e)` 다.
    ★ 이 식이 실측을 맞힌다 — 튜토리얼 `cohesion` 대조쌍은 낙하 60 mm · e = 0.9 이고
      `t_ff = 0.111 s` 이므로 식이 **2.11 s** 를 준다.  실제로 250,000 step(2.5 s)
      에서 정착했고 50,000 step(0.5 s = 정착의 24 %)에서는 지표가 **부호까지 반대**로
      나왔다.  ⇒ `steps_fill = 20000` 같은 **상수는 쓰지 않는다**.
    ⚠ 이 식은 홑 입자의 튐만 센다.  무리의 재배열은 더 걸리므로 `margin` 을 곱하고,
      그래도 맞았는지는 `measure_bed_aspect.py` 의 φ(포락) 경고로 **반드시 확인**한다.
    """
    t_ff = math.sqrt(2.0 * drop_m / g)
    return margin * t_ff * (1.0 + restitution) / (1.0 - restitution)


def _next_prime(n):
    """n 이상의 첫 소수 — 층상 삽입의 둘째 insert/pack·pdd 시드용 (둘 다 소수여야 한다)."""
    n = int(n)
    while not _is_prime(n):
        n += 1
    return n


def _is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def run_steps(p, rpm, revolutions, settle_s=None, restitution=0.3, dt_factor=1.0):
    """덱의 시간 계획 — (정착 step · 회전 step · 덤프 간격 · 체크포인트 간격 · 덱에 찍히는 dt 문자열).

    기본 (`dt_factor` 1) = 옛 `deck()` 본문의 식 그대로 (정착 = 유도 정착시간 · 회전 = 바퀴 × 주기 를 `p['dt']` 로 반올림,
    덤프 간격 = max(1000, 회전 step // 200), dt 는 `:.4g`).  경화 덱 (`plan(…, stiffen_se=F)`) 은 같은 식이 **새 dt** 로 돈다
    = 물리 시간 (정착 · 회전 · 바퀴 수) 불변, step · 덤프 간격은 새 dt 로 다시 계산.
    ★ `dt_factor` X = 1/k (2026-09-30, DEV `E0_ref@dt/2`) — **dt 만** 인쇄된 dt 의 정확히 1/k 로 두고 정착 · 회전 · 덤프 간격 step 은
      기본 계획의 **정확히 k 배** (새로 반올림하지 않는다) ⇒ 물리 시간 · 덤프 시각 · 계획 t₀ 의 물리 시각이 같다.  `run 1` (삽입 한 step) 은
      배하지 않는다 (삽입 step 이지 물리 구간이 아니다 — 회전 시작 시각이 dt/2 앞당겨질 뿐).  체크포인트 간격은 새 step 으로 같은 규칙.
    """
    k = _dt_k(dt_factor)
    period = 60.0 / rpm
    if settle_s is None:
        settle_s = settle_time(2.0 * p['R'], restitution)
    steps_fill = max(1000, int(round(0.5 * settle_s / p['dt'])))   # 두 번 돈다
    steps_run = int(round(revolutions * period / p['dt']))
    dump_every = max(1000, steps_run // 200)
    if k != 1:
        steps_fill, steps_run, dump_every = k * steps_fill, k * steps_run, k * dump_every
    #  ★ 체크포인트 간격 — 잃어도 되는 시간이 기준이다.  실측 21.8 step/s 에서 500,000 스텝
    #    ≈ 6.4 h 이므로 ~1 h 손실선으로 잡는다.  회전이 없는 기준런(steps_run=0)은 정착만
    #    도는데 그 전체가 385,336 스텝(≈4.9 h)이라 같은 값이면 한 번도 안 찍힌다 ⇒ 하한을 둔다.
    restart_every = max(50_000, min(200_000, (steps_run or 2 * steps_fill) // 20))
    dt_txt = f"{p['dt']:.4g}" if k == 1 else repr(float(f"{p['dt']:.4g}") / k)
    return dict(k=k, period=period, settle_s=settle_s, steps_fill=steps_fill, steps_run=steps_run,
                dump_every=dump_every, restart_every=restart_every, dt_txt=dt_txt,
                dt_c=p['dt'] if k == 1 else float(dt_txt))       # dt_c = 주석용 (기본은 옛 식 p['dt'] 그대로)


#: ★ 전 정밀도 덤프 (2026-10-05 · 강성 축 사전등록 §12-4 (다)) — dump custom 열의 C 형식.  LIGGGHTS-PUBLIC 3.x (공개 소스 3d5c00f) 의
#:   dump_custom.cpp 가 열마다 INT (id · type · mol → `static_cast<int>` + 형식) / DOUBLE 을 정한다 — 그 표에서 우리 dump 가 쓰는 열만 옮긴다.
DUMP_INT_COLS = ('id', 'type', 'mol')
DUMP_FLOAT_COLS = ('x', 'y', 'z', 'vx', 'vy', 'vz', 'fx', 'fy', 'fz', 'radius')
DUMP_FLOAT_FMT = '%.17g'          # double 왕복 (17 유효숫자 = IEEE 754 binary64 를 정확히 되읽는 최소 자릿수)


def dump_columns():
    """생산 덱 `dump dmp` 의 열 (순서 그대로) — `mol` 은 섬유 (multisphere) 가 있을 때만 (없으면 LIGGGHTS 가 즉시 죽는다 — 리뷰 R-1)."""
    _fib = any(t in FIBRE_TYPES for t in TYPES)
    return ('id', 'type') + (('mol',) if _fib else ()) + ('x', 'y', 'z', 'vx', 'vy', 'vz', 'fx', 'fy', 'fz', 'radius')


def dump_modify_format(cols):
    """dump custom 열 이름 → `dump_modify <ID> format "<…>"` 의 형식 문자열 (따옴표 없이) — id · type · mol = `%d` · 나머지 `%.17g`.

    LIGGGHTS-PUBLIC 3.x 는 LAMMPS **옛 문법**이다: 한 줄 전체의 형식 문자열 하나를 받아 (dump.cpp:571 `format_user`) 공백으로 잘라 열마다
    하나씩 쓴다 (dump_custom.cpp:255–265 · 모자라면 `Dump_modify format string is too short`).  새 LAMMPS 의 `format line` · `format float`
    키워드는 이 판에 없다.  ⚠ 공개 소스 (3d5c00f) 판독뿐 — **ibb 바이너리에서 실측하지 않았다** (확인 블록 덱 작업에서 run 0 한 번으로 본다).
    모르는 열은 거부한다 (INT/DOUBLE 을 추정으로 정하지 않는다)."""
    cols = list(cols)
    bad = [c for c in cols if c not in DUMP_INT_COLS + DUMP_FLOAT_COLS]
    if not cols or bad:
        raise SystemExit(f'⛔ dump_modify format: 열 {cols!r} — 비었거나 모르는 열 {bad} (INT/DOUBLE 을 정할 수 없다)')
    return ' '.join('%d' if c in DUMP_INT_COLS else DUMP_FLOAT_FMT for c in cols)


def ced_for_deck(p, arm, hold_bo_pairwise=False):
    """덱의 CED 행렬 → (soft 행렬, 덱 행렬, 점착 있음?).

    soft = 현 생성기 `ced_matrix` (기준 영률 `E_PHASE`).  `p` 가 경화 계획 (`stiffen_se` ≠ 1) 이고 점착이 있으면
    `hold_bo_pairwise=True` 일 때만 쌍별 F₀ 보존 행렬을 쓴다 — **없으면 거부** (옛 동일상 규칙으로 조용히 가지 않게).
    점착이 전부 0 인 팔 (E0 · L0) 은 F₀ 대상이 없으니 허용한다 (행렬 그대로 0).
    밀도는 계획의 표 (`plan()['dens']` · 세대 미지정 = gen1 그대로) 로 Bo ↔ CED 를 환산한다.
    """
    M_soft = ced_matrix(arm, p['d'], dens=_dens_of(p))
    F = float(p.get('stiffen_se', 1.0))
    nonzero = any(v != 0.0 for row in M_soft for v in row)
    if F == 1.0 or not nonzero:
        return M_soft, M_soft, nonzero
    if not hold_bo_pairwise:
        raise SystemExit(f'⛔ 팔 {arm}: --stiffen-se {F:g} 를 --hold-bo-pairwise 없이 줬다 — 점착이 0 이 아닌 팔은 거부한다.  '
                         f'SE 영률만 올리고 행렬을 그대로 두거나 동일상 규칙 (CED ∝ E^(2/3)) 으로 다시 만들면 혼합쌍 · 벽의 '
                         f'점착 힘 척도가 어긋난다 (Codex HBR6-02: AM–SE ×1.272 · SE–벽 ×1.182).  사전등록 §3 = --hold-bo-pairwise')
    E_new = p.get('E', E_PHASE)
    M_new = hold_bo_pairwise_matrix(M_soft, E_PHASE, E_new)
    if ARMS[arm].get('rule') == 'geomean':          # D2 팔 = 모든 쌍 천장 (옛 팔은 대각 · 벽 검사 그대로)
        _assert_ceiling_pairwise(arm, M_new, p['d'], E_new)
    else:
        _assert_ceiling(arm, M_new, p['d'], E=E_new)
    return M_soft, M_new, nonzero


def _stiff_header(arm, p, M_soft, M_ced, nonzero, hold_bo_pairwise, dt_factor, st):
    """경화 · dt 인자 덱의 머리 주석 (기본 덱에는 없다 — 빈 문자열).  ⚠ 줄이 `&` 로 끝나면 LIGGGHTS 가 다음 줄과 잇는다 — 쓰지 않는다."""
    F = float(p.get('stiffen_se', 1.0))
    if F == 1.0 and st['k'] == 1:
        return '', ''
    E_new = p.get('E', E_PHASE)
    hold = ('yes' if hold_bo_pairwise else 'no') + ('' if nonzero else ' (전 점착 0 — F0 대상 없음 · 행렬 그대로 0)')
    L = [f'# ★ 강성 축 (사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §3 · Codex 6 차 HBR6-02 · 7 차 §5) — '
         f'stiffen_se {F:g} · hold_bo_pairwise {hold} · dt_factor {float(dt_factor):g}']
    if F != 1.0:
        L.append(f"#   SE 영률만 ×{F:g}: {E_PHASE['SE']:.4g} → {E_new['SE']:.4g} Pa (AM_P · AM_S · 벽 영률 · 전 상 ν 불변 · "
                 f"AM/SE 영률비 {E_PHASE['AM_P'] / E_PHASE['SE']:.4g} → {E_new['AM_P'] / E_new['SE']:.4g})")
    dt0 = plan_dt_soft(p)
    L.append(f"#   dt = 생성기 Rayleigh 규칙 (상별 최소) 을 이 덱의 E 로: {dt0[0]:.4g} s (soft · {dt0[1]}) → {p['dt']:.4g} s "
             f"({p.get('dt_by', '?')}) · 정착 · 회전 물리 시간 · 바퀴 수 불변 — step · 덤프 간격은 새 dt 로 다시")
    if st['k'] != 1:
        L.append(f"#   dt_factor {float(dt_factor):g} — dt 만 정확히 1/{st['k']} ({p['dt']:.4g} → {st['dt_txt']}) · 정착 · 회전 · 덤프 "
                 f"간격 step 정확히 ×{st['k']} (run 1 삽입 step 은 그대로) ⇒ 물리 시간 · 덤프 시각 · 계획 t0 시각 불변")
    L.append('#   점착 = 쌍별 명목 소겹침 점착 힘 척도 F0 = B³/A² = (9/2)π³R*²CED³/E*² 보존: CED_new,ij = CED_soft,ij · '
             '(E*_new,ij/E*_soft,ij)^(2/3)')
    L.append('#     soft = 현 생성기 행렬 (원소마다 역산 · min 재조립 없음) · E*_ij = [(1−ν_i²)/E_i + (1−ν_j²)/E_j]⁻¹ · '
             '벽 R* = r_입자 · 선언된 벽 E · ν · 0 은 정확히 0')
    L.append(f"#   {'쌍':<10s} {'R* (m)':>11s} {'E*_soft':>11s} {'E*':>11s} {'CED_soft':>11s} {'CED':>11s} "
             f"{'F0_soft (N)':>11s} {'F0 (N)':>11s} {'F0 비':>13s}")
    g = lambda v: '—' if v is None else f'{v:.6g}'
    for r_ in stiffness_rows(p['d'], M_soft, M_ced, E_PHASE, E_new):
        ratio = '—' if r_['F0_ratio'] is None else f"{r_['F0_ratio']:.12f}"
        L.append(f"#   {r_['pair']:<10s} {g(r_['R_star_m']):>11s} {g(r_['E_star_soft_Pa']):>11s} {g(r_['E_star_Pa']):>11s} "
                 f"{g(r_['CED_soft']):>11s} {g(r_['CED']):>11s} {g(r_['F0_soft_N']):>11s} {g(r_['F0_N']):>11s} {ratio:>13s}")
    L.append('#   ⚠ F0 보존 ≠ SJKR 동역학 전체 불변 — 분리 일 U_sep ∝ E*^(−2/3) · 접촉시간 · 접선 강성 · 감쇠 · 이력 · 영률비는 바뀐다 '
             '(§3 남기는 차이) · 이 표는 생성기 산술이다 — 실행 덱 검산은 scripts/mixer_deck_readback.py')
    note = (f"\n#   ⚠ 이 덱은 강성 축 덱이다: 위 문장의 영률 · 비는 soft 기준 — 이 덱의 SE 영률 = {E_new['SE']:.4g} (머리 블록 참조)"
            if F != 1.0 else '')
    return '\n' + '\n'.join(L), note


def _gm_header(arm, p, M_ced, layered=None):
    """D2 결합 규칙 덱의 머리 주석 (옛 팔 = 빈 문자열 → 덱 바이트 그대로).  ⚠ 줄 끝 `&` 금지 (LIGGGHTS 줄 잇기).
    ★ 2026-10-21 (MXD2-05 · 06) — 벽 줄 = 규칙별 (비코팅 NCM ρ · 명시 = 코팅 팔 · 함의 ρ) · NCM 표면 · 삽입 줄 (`layered` = 이 덱의 실제 삽입).
      `γ/γ_SE:` 선언 줄 · 쌍 표의 꼴은 그대로 둔다 (scripts/mixer_deck_readback.py 가 이 두 줄을 읽어 덱 값과 대조한다)."""
    a = ARMS[arm]
    if a.get('rule') != 'geomean':
        return ''
    E_now = p.get('E', E_PHASE)
    d = p['d']
    names = list(TYPES) + [WALL]
    lay = bool(a.get('layered')) if layered is None else bool(layered)
    if a.get('wall_rule') == GM_WALL_RULE_NCM:
        wall_ln = ('#   벽 = 비코팅 NCM 에 묶음 (1저자 10-14 Q2): γ_W/γ_SE = 0.0256 (Hare 2026 Table 3) × ρ_비코팅 '
                   + f"{a['rho_uncoated_ncm']:g} = {a['gamma_wall']:g} — 같은 ρ 세계의 코팅 팔도 같은 벽")
    else:
        wall_ln = (f"#   벽 γ_W/γ_SE = 명시 입력 {a['gamma_wall']:g} — NCM 상 γ 전부 1 (코팅 · 같은 γ 세계) 인 팔만 (1저자 10-14 Q2) · "
                   f"이 벽의 비코팅 NCM 함의 ρ = γ_W/0.0256 = {a['rho_world']:g}")
    surf = a.get('surface') or {}
    surf_ln = ('#   NCM 표면 (Q2 · 코팅 = γ 1 · 비코팅 = γ ρ): ' + ' · '.join(f"{t} {'코팅' if surf[t] == 'coated' else '비코팅'}" for t in surf)
               + f" · 삽입 = {'층상 (AM → SE · D11 (가))' if lay else '균일'}")
    L = ['# ★ D2 결합 규칙 (기하평균 · 1저자 비준 10-14 D2 (가) · docs/mixer_paper_pipeline_draft_20261013.md §4) — 개발 · 등록 전 (결과 0)',
         '#   W_ij = 2√(γ_iγ_j) (혼합쌍 · 벽까지 · 같은 상 = 2γ_i) · 힘 = JKR 스케일 F ∝ W·R* → F0_ij = F0_SS · √(γ_iγ_j)/γ_SE · R*_ij/R*_SS',
         '#   γ/γ_SE: ' + ' · '.join(f"{t} {a['gamma'][t]:g}" for t in TYPES)
         + f" · γ_W/γ_SE {a['gamma_wall']:g} · SE–SE Bo_code {a['bo_se']:g} (절대 수준 = 이 하나 · D3 앵커 전 = 명시 입력)",
         '#   CED_ij = [F0_ij·E*_ij²/((9/2)π³R*_ij²)]^(1/3) (쌍별 E* · R* · 벽 R* = r_입자) · 겹침 천장 = 모든 쌍 δ0/min(r)',
         wall_ln, surf_ln,
         f"#   {'쌍':<10s} {'R* (m)':>11s} {'E* (Pa)':>11s} {'CED':>11s} {'F0 (N)':>11s} {'F0/F0_SS':>11s} {'δ0/min r':>9s}"]
    rows, fss = [], None
    for i in range(len(names)):
        for j in range(i, len(names)):
            ti, tj = names[i], names[j]
            if ti == WALL and tj == WALL:
                continue
            rs, es, c = rstar_pair(ti, tj, d), estar_pair(ti, tj, E_now), M_ced[i][j]
            f = f0_pair(c, rs, es)
            rows.append((f'{ti}–{tj}', rs, es, c, f, pair_overlap(c, ti, tj, d, E_now)))
            if ti == 'SE' and tj == 'SE':
                fss = f
    for nm_, rs, es, c, f, ov in rows:
        L.append(f"#   {nm_:<10s} {rs:>11.6g} {es:>11.6g} {c:>11.6g} {f:>11.6g} {f / fss:>11.6g} {ov * 100:>8.4f}%")
    L.append('#   ⚠ γ 의 절대값 · 비코팅 NCM/SE 비는 모른다 (논지 §2-8) — 이 덱의 비는 입력이다 · ⛔ 실제 코팅 · 분말의 재현이라 쓰지 않는다')
    return '\n' + '\n'.join(L)


def plan_dt_soft(p):
    """soft (기준 E) 에서의 dt 와 그것을 정한 상 — 머리 주석 · 메타용 (같은 Rayleigh 식 · 그 계획의 밀도표)."""
    dn = _dens_of(p)
    dts = []
    for t in TYPES:
        nu_t, mat = PHASE_MECH[t]
        G = E_PHASE[t] / (2.0 * (1.0 + nu_t))
        dts.append(0.2 * math.pi * (p['d'][t] / 2) * math.sqrt(dn[mat] * 1000.0 / G) / (0.1631 * nu_t + 0.8766))
    return min(dts), TYPES[dts.index(min(dts))]


def _require_dens_gen(arm, p):
    """★ D2 결합 규칙 팔 (rule="geomean") 덱 = **새 세대 덱** — 계획에 밀도 세대가 명시돼 있어야 한다 (1저자 10-14 밤 · fail-closed).
    옛 팔은 그대로 (세대 미지정 = gen1 · 옛 덱 바이트 그대로)."""
    if ARMS[arm].get('rule') == 'geomean' and p.get('dens_gen') is None:
        raise SystemExit(f'⛔ 팔 {arm}: D2 결합 규칙 덱은 새 세대 덱이다 — 밀도 세대를 명시해야 한다 '
                         f'(CLI --dens-gen {"|".join(sorted(DENS_GENERATIONS))} · plan(…, dens_gen=…) · docs/density_generations_20261014.md)')


def _dens_header(p):
    """밀도 세대 머리 주석 — 세대를 **명시한** 덱에만 (미지정 = 빈 문자열 → 덱 바이트 그대로).  ⚠ 줄 끝 `&` 금지 (LIGGGHTS 줄 잇기)."""
    g = p.get('dens_gen')
    if g is None:
        return ''
    t = _dens_of(p)
    carried = DENS_CARRIED_FROM_GEN1.get(g, ())
    return ('\n# ★ 밀도 세대 dens_gen = ' + g + ' (docs/density_generations_20261014.md · 1저자 10-14 밤 랩 표준 · 앞으로만) — '
            + ' · '.join(f'{k} {t[k]:g}' for k in t) + ' g/cm³ · gen1 값을 그대로 옮긴 상: ' + (' · '.join(carried) or '없음')
            + '\n#   밀도가 들어간 곳 = 부피분율 → 템플릿 수 · 드럼 크기 · Rayleigh dt · Bo ↔ CED 환산 · 템플릿 density constant '
              '(세대 미지정 덱 = gen1 · 옛 덱 · 판정 기록 그대로)')


def deck_meta(p, rpm, revolutions, seed, arm, text, argv=None, settle_s=None, restitution=0.3,
              hold_bo_pairwise=False, dt_factor=1.0, dump_full_precision=False):
    """경화 · dt 인자 덱의 **봉인 가능한 메타** (CLI 가 `deck_meta.json` 으로 쓴다) — 덱 sha256 · 생성기 sha256 · argv · 선택 옵션 ·
    상별 E · ν · dt (soft → 규칙 → 덱) · 시간 계획 (step · 물리 시각) · 쌍별 E* · CED · F₀ 표.
    전 정밀도 덤프 (--dump-full-precision) 덱에만 `dump_modify_format` 키를 더한다 (끄면 키 집합 그대로).

    ⚠ 이 표는 **생성기 산술**이다 — 실행 덱의 독립 검산은 `scripts/mixer_deck_readback.py` (덱 텍스트만 읽는다) 가 맡는다.
    밀도 세대를 명시한 계획 (`plan(…, dens_gen=)`) 이면 `dens_gen` · `dens_g_cm3` · `dens_carried_from_gen1` 키를 더한다 (미지정 = 키 집합 그대로).
    """
    import hashlib
    _require_dens_gen(arm, p)
    st = run_steps(p, rpm, revolutions, settle_s=settle_s, restitution=restitution, dt_factor=dt_factor)
    M_soft, M_ced, nonzero = ced_for_deck(p, arm, hold_bo_pairwise)
    E_new = p.get('E', E_PHASE)
    names = list(TYPES) + [WALL]
    dt_deck = float(st['dt_txt'])
    t0 = (2 * st['steps_fill'] // st['dump_every']) * st['dump_every']
    dt_soft, by_soft = plan_dt_soft(p)
    raw = text.encode('utf-8')
    meta = dict(
        schema='mixer_deck_meta/1',
        registered='docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §3 (강성 축) · §2 · §8-2 (DEV) — Codex 6 차 HBR6-02 · 7 차 §5',
        generator='scripts/make_mixer_deck.py',
        generator_sha256=hashlib.sha256(open(os.path.abspath(__file__), 'rb').read()).hexdigest(),
        argv=list(argv or []), deck_file='in.mixer', deck_sha256=hashlib.sha256(raw).hexdigest(), deck_bytes=len(raw),
        arm=arm, arm_desc=ARMS[arm]['desc'], seed=int(seed), revolutions=revolutions, n_atoms_planned=p['n_total'],
        cgf=p['cgf'], rpm=rpm, period_s=st['period'],
        stiffen_se=float(p.get('stiffen_se', 1.0)), hold_bo_pairwise=bool(hold_bo_pairwise), dt_factor=float(dt_factor),
        cohesion_nonzero=bool(nonzero),
        types={str(i + 1): t for i, t in enumerate(names)},
        E_soft_Pa={t: E_PHASE[t] for t in names}, E_Pa={t: E_new[t] for t in names}, nu={t: _nu_of(t) for t in names},
        radius_m={t: p['d'][t] / 2.0 for t in TYPES},
        dt=dict(soft_rule_s=dt_soft, soft_set_by=by_soft, rule_s=p['dt'], rule_set_by=p.get('dt_by'),
                deck_txt=st['dt_txt'], deck_s=dt_deck, k=st['k']),
        steps=dict(insert=1, fill=st['steps_fill'], run=st['steps_run'], dump_every=st['dump_every'],
                   restart_every=st['restart_every'], t0_planned=t0, steps_per_rev=st['period'] / dt_deck),
        physical_s=dict(settle=2 * st['steps_fill'] * dt_deck, rotation=st['steps_run'] * dt_deck,
                        dump_interval=st['dump_every'] * dt_deck, t0_planned=t0 * dt_deck),
        pairs=stiffness_rows(p['d'], M_soft, M_ced, E_PHASE, E_new),
        caveat=('F0 = B³/A² 보존 = 명목 소겹침 점착 힘 척도 (점착 지배 · 고립 접촉 근사) — SJKR 동역학 전체 불변이 아니다 '
                '(U_sep ∝ E*^(−2/3) · 접촉시간 · 접선 강성 · 감쇠 · 이력 · 영률비 · 실제 SJKR 구 교차 면적 · 메시 area_ratio).'))
    if dump_full_precision:                       # 켠 덱에만 (끄면 키 집합 그대로)
        meta['dump_modify_format'] = dump_modify_format(dump_columns())
    if ARMS[arm].get('rule') == 'geomean':          # D2 팔에만 (옛 팔 = 키 집합 그대로)
        a_ = ARMS[arm]
        meta['adhesion_rule'] = dict(rule='geomean', gamma=dict(a_['gamma']), gamma_wall=a_['gamma_wall'], bo_se=a_['bo_se'],
                                     ratified='1저자 10-14 D2 (가) — docs/mixer_paper_pipeline_draft_20261013.md §4',
                                     law='W_ij = 2√(γ_iγ_j) · F0_ij = F0_SS·√(γ_iγ_j)/γ_SE·R*_ij/R*_SS · F0_SS = Bo_SE × SE 무게',
                                     ceiling=f'모든 쌍 δ0/min(r) ≤ {OVL_CEILING:g}', status='개발 · 등록 전 (결과 0)')
        #  ★ 2026-10-21 (원장 MXD2-05 · 06) — 벽 규칙 (늘) · NCM 표면 상태 · 삽입 (층상 D11 (가)) 을 기록 · 비코팅 NCM ρ (Q2) 또는 명시 벽의 함의 ρ
        meta['adhesion_rule'].update(wall_rule=a_['wall_rule'], surface=dict(a_['surface']), layered=bool(a_.get('layered')))
        if a_['wall_rule'] == GM_WALL_RULE_NCM:
            meta['adhesion_rule']['rho_uncoated_ncm'] = a_['rho_uncoated_ncm']
        else:
            meta['adhesion_rule']['rho_world'] = a_['rho_world']
        #  ★ registered = 규칙별 (MXD2-06) — 옛 판은 D2 덱에도 강성 축 사전등록 §3 만 적었다 (D2 덱은 결과 전 등록이 아직 없다)
        meta['registered'] = (MIXER_D2_REGISTERED
                              + (' · 강성 경로 (쌍별 F₀ 보존 · dt 인자) = docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §3'
                                 if (float(p.get('stiffen_se', 1.0)) != 1.0 or float(dt_factor) != 1.0) else ''))
    if p.get('dens_gen') is not None:               # 세대를 명시한 덱에만 (미지정 = 키 집합 그대로)
        meta.update(dens_gen=p['dens_gen'], dens_g_cm3=dict(_dens_of(p)),
                    dens_carried_from_gen1=list(DENS_CARRIED_FROM_GEN1[p['dens_gen']]))
        if p['dens_gen'] != 'gen1':                   # 새 세대 덱 = 결과 전 등록 없음 (gen1 명시 덱은 옛 등록 그대로)
            meta['registered'] += (f" · 밀도 세대 {p['dens_gen']} = 결과 전 등록 없음 (docs/density_generations_20261014.md · 1저자 10-14 밤 · "
                                   f"앞으로만)")
    if 'adhesion_rule' in meta or 'dens_gen' in meta:
        meta['schema'] = MIXER_DECK_META_SCHEMA_V2   # ★ 선택 키 (D2 · 세대) 를 담은 메타 = /2 (MXD2-06 · /1 의 키는 그대로 · 없으면 /1 그대로)
    return meta


def deck(p, rpm, revolutions, seed=32452843, arm='E1', settle_s=None, layered=None,
         restitution=0.3, n_baffles=0, baffle_h=0.10, hold_bo_pairwise=False, dt_factor=1.0, dump_full_precision=False):
    #  ⚠⚠ LIGGGHTS 의 `fix insert/pack` 시드는 **소수여야 한다**.
    #    합성수를 주면 런이 `random.cpp:93` 에서 **죽는다** — 그런데 죽는 자리가
    #    셋업 뒤라 덤프 디렉터리는 이미 만들어져 있고, 배치로 돌리면 "덤프 0 개" 로만
    #    보여 **조용한 실패처럼** 읽힌다 (2026-09-19 실측: 시드 57204983 으로 두 팔이
    #    그렇게 죽었다).  ⇒ 덱을 **쓰기 전에** 막는다.
    if not _is_prime(int(seed)):
        raise SystemExit(
            f'⛔ 삽입 시드 {seed} 는 소수가 아니다 — LIGGGHTS 가 거부한다.\n'
            f'   예: 15485863 · 32452843 · 32452867 · 49979687 · 91648301')
    _require_dens_gen(arm, p)                          # ★ D2 덱 = 새 세대 덱 (세대 미지정이면 거부 · 옛 팔은 그대로)
    n, d = p['n'], p['d']
    #  ★ 강성 축 (2026-09-30) — 시간 계획 · CED 행렬 · 머리 블록.  옵션이 중립이면 셋 다 옛 식 그대로 (셀프테스트 ST① 가 바이트 동일 강제).
    st = run_steps(p, rpm, revolutions, settle_s=settle_s, restitution=restitution, dt_factor=dt_factor)
    M_soft, M_ced, _nonzero = ced_for_deck(p, arm, hold_bo_pairwise)
    _stiff_hdr, _stiff_note = _stiff_header(arm, p, M_soft, M_ced, _nonzero, hold_bo_pairwise, dt_factor, st)
    if layered is None:                                # (2026-10-21 · 아래 삽입 블록에서 여기로 올렸다 — D2 머리가 실제 삽입을 적게 · 값 그대로)
        layered = bool(ARMS[arm].get('layered', False))
    _gm_hdr = _gm_header(arm, p, M_ced, layered=layered)   # D2 팔만 (옛 팔 = '' → 바이트 그대로)
    _dens_hdr = _dens_header(p)                        # 밀도 세대를 명시한 덱만 (미지정 = '' → 바이트 그대로)
    #  ★ 메시 벽 타입 주석 (2026-10-21 · 원장 MXD2-06) — D2 팔의 벽 점착은 같은 기하평균이다 (옛 문구 "점착 = 입자값 ÷ 1.842" 는 옛 팔 규약 · MIX-12).
    #    옛 팔 문구는 글자 그대로 둔다 (덱 바이트 · 골든 해시).
    _a_now = ARMS[arm]
    _wall_cmt = (f"# ★ 메시 `type {len(TYPES) + 1}` = 벽 전용 타입 (강철 ÷135, 점착 = D2 기하평균 W_iW = 2√(γ_iγ_W) · γ_W/γ_SE "
                 f"{_a_now['gamma_wall']:g} — 머리 블록).  옛 판은 type 2 = AM_S 를 빌려 썼다"
                 if _a_now.get('rule') == 'geomean' else
                 f'# ★ 메시 `type {len(TYPES) + 1}` = 벽 전용 타입 (강철 ÷135, 점착 = 입자값 ÷ {WALL_CED_DIV:.3f}).  옛 판은 type 2 = AM_S 를 빌려 썼다')
    _dn = _dens_of(p)
    E_now = p.get('E', E_PHASE)
    period = st['period']
    #  ★ 배플 — `D10(b)` 전단 축.  **원본 Drum.stl 은 안 건드린다** (별도 메시).
    #  ⚠ `n_baffles = 0` 이면 아래 두 조각이 **빈 문자열**이라 덱이 배플 이전과
    #    글자 그대로 같다 — 배플 없는 팔을 다시 돌릴 필요가 없다 (시험 ㉛ 이 강제).
    _baffle_mesh = ('' if not n_baffles else
                    f'fix Baffle all mesh/surface file Baffles.stl type {len(TYPES)+1} '
                    f'scale {p["stl_scale"]:.6g}\n')
    #  ⚠ 빈 문자열일 때 **줄이 남지 않게** 앞에 줄바꿈을 단다.  초판은 템플릿에서
    #    제 줄을 차지해 배플 0 인 덱에 **빈 줄 하나**가 더 생겼고, 그래서 이미 돌린
    #    런의 덱과 바이트가 달라졌다 (자기검사는 '지금 두 출력' 만 비교해 못 잡았다).
    _baffle_move = ('' if not n_baffles else
                    f'\nfix mvBf all move/mesh mesh Baffle rotate origin 0 0 0 '
                    f'axis 1. 0. 0. period {period:.6g}')
    #  낙하 높이 = 드럼 지름 (꼭대기에서 바닥까지) · 정착 · 회전 · 덤프 · 체크포인트 간격은 run_steps (옛 식 그대로 옮김)
    steps_fill, steps_run = st['steps_fill'], st['steps_run']
    dump_every, restart_every = st['dump_every'], st['restart_every']
    #  ── 삽입 블록 (§24 층상 vs 기존 균일) ─────────────────────────────────
    #  ⚠ 비층상 문자열은 옛 원문과 **바이트 동일**해야 한다 — 셀프테스트 ㉟ 골든 해시.
    if layered is None:
        layered = bool(ARMS[arm].get('layered', False))
    mf = p['massfrac']
    if not layered:
        _frac = ' '.join(f'pt{i+1} {mf[t]:.6f}' for i, t in enumerate(TYPES))
        _ins_block = f"""# ⚠ 분율은 **mass%** 다 (LIGGGHTS 규약 — 실행으로 확인).  우리 조성이 wt% 라 그대로 넣는다.
fix pdd all particledistribution/discrete 32452867 {len(TYPES)} &
    {_frac}

region ins_reg cylinder x 0.0 0.0 {p['R']*0.9:.6g} -{p['L']*0.45:.6g} {p['L']*0.45:.6g} units box
fix ins all insert/pack seed {seed} distributiontemplate pdd &
    maxattempt 200 insert_every once overlapcheck yes all_in yes vel constant 0. 0. -0.2 &
    region ins_reg particles_in_region {p['n_tpl_total']} ntry_mc 20000   # 템플릿 수 (섬유 1가닥 = 1)
"""
        _unfix_ins = 'unfix ins'
        _unfix_ins2 = ''
    else:
        #  층별 mass% 는 층 안에서 다시 정규화한다 (pdd 는 자기 템플릿끼리의 분율만 본다)
        _A_T = tuple(t for t in TYPES if t.startswith('AM_'))
        _B_T = tuple(t for t in TYPES if not t.startswith('AM_'))
        a_sum = sum(mf[t] for t in _A_T)
        b_sum = sum(mf[t] for t in _B_T)
        nA = sum(p['n_tpl'][t] for t in _A_T)
        nB = sum(p['n_tpl'][t] for t in _B_T)
        _fracA = ' '.join(f'pt{TYPES.index(t)+1} {mf[t]/a_sum:.6f}' for t in _A_T)
        _fracB = ' '.join(f'pt{TYPES.index(t)+1} {mf[t]/b_sum:.6f}' for t in _B_T)
        seedB = _next_prime(seed + 2)                 # insA 와 다른 소수
        pddB = _next_prime(32452867 + 2)              # pddA 와 다른 소수
        #  ★★ 순서가 물리다 (스모크 실측 2026-09-20): AM_P(Ø2.4 mm) 119 개를 작은 블록에
        #    `all_in` 으로 넣으면 중심 가용부피 대비 구 부피 59 % = RSA 잼 한계(~38 %) 초과 →
        #    삽입이 끝나지 않는다.  ⇒ AM 은 **원통 전체**(균일 삽입과 같은 영역)에 넣고 정착 ①
        #    로 바닥에 깔리게 한 뒤, SE+섬유를 **그 윗면 위 블록**에 넣는다 (정착 ②).
        #    = "AM 침대 위에 SE 를 붓는다" — 층상의 물리 그대로다.
        _v_am = sum(p['n'][k] * (math.pi / 6) * d[k] ** 3 for k in _A_T)
        _v_bed = _v_am / 0.60                          # plan() 의 pack 기본값
        _A = _v_bed / p['L']                           # 원 세그먼트 단면적
        _th = 2.0                                      # θ − sinθ = 2A/R²  (이분법)
        _lo_t, _hi_t = 0.0, 2 * math.pi
        for _ in range(60):
            _th = 0.5 * (_lo_t + _hi_t)
            if _th - math.sin(_th) < 2 * _A / p['R'] ** 2:
                _lo_t = _th
            else:
                _hi_t = _th
        _h = p['R'] * (1 - math.cos(_th / 2))          # 침대 높이 (바닥에서)
        _z_top = -p['R'] + _h
        _z_lo = _z_top + d['AM_P']                     # 여유 = AM_P 지름 하나
        _z_hi = 0.78 * p['R']                          # |y| ≤ 0.6R 이면 z ≤ 0.8R 가 원 안
        assert _z_hi - _z_lo > 4 * d['SE'], '층상 삽입: SE 층 높이가 너무 작다'
        _ins_block = f"""# ★ §24 층상 삽입 ① — AM 을 원통 전체에 넣는다 (정착 ① 로 바닥에 깔린다).  분율은 층 안 mass%.
fix pddA all particledistribution/discrete 32452867 {len(_A_T)} &
    {_fracA}
fix pddB all particledistribution/discrete {pddB} {len(_B_T)} &
    {_fracB}

region ins_reg cylinder x 0.0 0.0 {p['R']*0.9:.6g} -{p['L']*0.45:.6g} {p['L']*0.45:.6g} units box
fix insA all insert/pack seed {seed} distributiontemplate pddA &
    maxattempt 200 insert_every once overlapcheck yes all_in yes vel constant 0. 0. -0.2 &
    region ins_reg particles_in_region {nA} ntry_mc 20000   # AM 템플릿 수
"""
        _unfix_ins = f"""unfix insA
# ★ §24 층상 삽입 ② — 정착 ① 뒤, {'+'.join(_B_T)} 를 AM 침대 **위** 블록에 붓는다 (정착 ② 시작 시 삽입).
#   AM 침대 윗면 추정: V_AM {_v_am*1e9:.0f} mm³ / pack 0.60 → 세그먼트 높이 {_h*1e3:.2f} mm → z_top {_z_top*1e3:.2f} mm
#   블록 z ∈ [{_z_lo*1e3:.2f}, {_z_hi*1e3:.2f}] mm · |y| ≤ 0.6R (원 안) · x ±0.45L
region ins_hi block -{p['L']*0.45:.6g} {p['L']*0.45:.6g} -{p['R']*0.6:.6g} {p['R']*0.6:.6g} {_z_lo:.6g} {_z_hi:.6g} units box
fix insB all insert/pack seed {seedB} distributiontemplate pddB &
    maxattempt 200 insert_every once overlapcheck yes all_in yes vel constant 0. 0. -0.2 &
    region ins_hi particles_in_region {nB} ntry_mc 20000   # 층 B 템플릿 수 (섬유 1가닥 = 1)"""
        _unfix_ins2 = '\nunfix insB'
    #  ── 입자 템플릿 — 활성 상만.  multisphere `type` 은 **1 부터 연속**이어야 한다 ──
    _fib = tuple(t for t in TYPES if t in FIBRE_TYPES)
    _tpl = []
    for _i, _t in enumerate(TYPES):
        _rho = _dn[PHASE_MECH[_t][1]] * 1000.0
        if _t in _fib:
            _tpl.append(
                f'fix pt{_i+1} all particletemplate/multisphere {TPL_SEED[_t]} '
                f'atom_type {_i+1} density constant {_rho:.0f} &\n'
                f'    nspheres {p["nsph"]} ntry 1000000 spheres file '
                f'data/{_t.lower()}.multisphere scale 1.0 type {_fib.index(_t)+1}')
        else:
            _tpl.append(
                f'fix pt{_i+1} all particletemplate/sphere {TPL_SEED[_t]} '
                f'atom_type {_i+1} density constant {_rho:.0f} '
                f'radius constant {d[_t]/2:.6g}')
    if _fib:
        _tpl.insert(len(TYPES) - len(_fib),
                    '# ★ 섬유는 multisphere 강체 사슬 — 구 하나로 접지 않는다 '
                    '(sun2026: 접으면 σ_e 순위가 뒤집힌다)\n'
                    '# ⚠ 끝의 `type` 은 **원자 타입이 아니라 multisphere 템플릿 번호**이고 '
                    '**1 부터 연속**이어야 한다\n'
                    '#   (실행으로 확인: ERROR: multisphere template types have to be '
                    'consecutive starting from 1)')
    _tpl_block = '\n'.join(_tpl)
    #  ★ 강체 적분기는 섬유가 있을 때만 — 없는데 켜면 LIGGGHTS 가 빈 그룹으로 죽는다
    _integr = ('fix integrS all nve/sphere        # ★ 평범한 구 ('
               + '·'.join(t for t in TYPES if t not in _fib) + ')')
    if _fib:
        _integr += ('\nfix integr  all multisphere       # 강체 사슬 ('
                    + '·'.join(_fib) + ') — 뒤에 둬 강체를 최종 확정')
    _comp = ' · '.join(f'{t} {p["wt"][t]:.2f}' for t in TYPES)
    _nt = len(TYPES) + 1                               # ★ 마지막 타입 = 벽
    _procs = ('processors      1 1 1            # PUBLIC 판 multisphere 는 직렬만 지원' if _fib else
              '# processors — 섬유(multisphere) 없음 ⇒ MPI 가능.  `mpirun -np N` 이면 자동 분할')
    _E_line = ' '.join(f'{E_now[t]:.4g}' for t in TYPES) + f' {E_now[WALL]:.4g}'
    _nu_line = ' '.join(f'{PHASE_MECH[t][0]:.2f}' for t in TYPES) + f' {WALL_NU:.2f}'
    box = p['R'] * 1.15
    #  ★ dump 열 · 전 정밀도 덤프 (2026-10-05 · 강성 축 사전등록 §12-4 (다)) — 끄면 (기본) 조각이 빈 문자열이라 덱이 바이트 그대로 (셀프테스트 DP①).
    #    켜면 같은 dump 바로 뒤에 `dump_modify dmp format "…"` — 좌표 · 반경 (· 속도 · 힘) 이 %.17g (double 왕복) 로 찍힌다.
    _dump_cols = dump_columns()
    _dump_fmt = ('' if not dump_full_precision else
                 '\n# ★ 전 정밀도 덤프 (생성기 --dump-full-precision · 강성 축 사전등록 §12-4 (다)) — '
                 + ' · '.join(c for c in _dump_cols if c in DUMP_INT_COLS) + ' = %d · 나머지 %.17g (double 왕복).  기본 %g 6 유효숫자면 '
                 '좌표 반폭 최대 5e-8 m\n'
                 '#   LIGGGHTS-PUBLIC 3.x 옛 문법 (한 줄 형식 · 공개 소스 3d5c00f 판독) — ⚠ ibb 바이너리 실측 전 · 덤프 크기 ≈ 2 배\n'
                 f'dump_modify dmp format "{dump_modify_format(_dump_cols)}"')
    return f"""# 믹싱 드럼 — 표면에너지 스윕  (생성: scripts/make_mixer_deck.py)
# ⚠ 손으로 고치지 말 것 — 치수가 조성에서 유도된다.  조성을 바꾸면 생성기를 다시 돌린다.
#
# 조성 (활성 상만, 재정규화 wt%): {_comp}
#   ⚠ 원 배합은 AM:SE:VGCF:PTFE = {WT['AM']:.0f}:{WT['SE']:.0f}:{WT['VGCF']:.0f}:{WT['PTFE']:.0f} · P:S = {PS[0]:.0f}:{PS[1]:.0f}
#   ⚠ 빠진 상: {', '.join(t for t in ALL_TYPES if t not in TYPES) or '없음'}  (LAMMPS 단계에서 다룬다)
# CGF = {p['cgf']:.0f}  (소재 AM_P {D_REAL_UM['AM_P']:.0f} µm → 모델 {d['AM_P']*1e3:.2f} mm · SE {D_REAL_UM['SE']:.0f} µm → {d['SE']*1e3:.3f} mm)
#   ★ 크기 비는 소재 그대로다: d_SE/d_AM_P = {d['SE']/d['AM_P']:.3f}
# ⛔ 생산 scale=1000 규약을 쓰지 않는다 — 드럼은 중력 구동이라 중력/접촉 비가 깨진다.
# ⚠ 전단탄성률을 계산비용 때문에 낮췄다 (lischka 와 같은 조작) — 물성으로 인용 금지.{_stiff_hdr}{_gm_hdr}{_dens_hdr}

atom_style      granular
atom_modify     map array sort 0 0
# ⚠ LIGGGHTS 는 SI 에서 `youngsModulus > 1e9` 를 **거부**한다
#   (`ERROR: youngsModulus <= 1e9 required for SI units`, global_properties.cpp:371).
#   우리 AM 1.037e9 · 벽 1.48e9 가 그 위다 — 2026-09-21 스모크 런이 실제로 여기서 멈췄다.
#   ⇒ 공식 override 를 쓴다.  dt 는 이미 **상별 Rayleigh 최소**로 잡으므로(plan) 안전 근거는 그쪽이다.
hard_particles  yes
boundary        f f f
newton          off
communicate     single vel yes
units           si
{_procs}

region          reg block -{box:.6g} {box:.6g} -{box:.6g} {box:.6g} -{box:.6g} {box:.6g} units box
create_box      {_nt} reg
{_wall_cmt}
neighbor        {min(d.values())*0.5:.6g} bin
neigh_modify    delay 0

# --- 물성 (1:AM_P 2:AM_S 3:SE 4:VGCF 5:PTFE) ---
# ⚠ 영률은 ÷135 균일 연화값이다 (AM 1.037e9 · SE 1.0e7 · 벽 1.48e9).  물성으로 인용 금지.
#   비 104 는 실물(AM 1.4e11 / SE_eff 1.35e9)과 같다.  마지막 열 = 벽.{_stiff_note}
fix m1 all property/global youngsModulus peratomtype {_E_line}
fix m2 all property/global poissonsRatio peratomtype {_nu_line}
# ★ 마찰 = hare2026 세트 (μ_s {MU_S} · μ_r {MU_R}) — Bo 3.0 앵커를 정의한 조건.  압연 덱과 다른 것은 정합이다.
fix m3 all property/global coefficientRestitution peratomtypepair {_nt} &
{_mat(_nt, COR)}
fix m4 all property/global coefficientFriction peratomtypepair {_nt} &
{_mat(_nt, MU_S)}
fix m5 all property/global coefficientRollingFriction peratomtypepair {_nt} &
{_mat(_nt, MU_R)}
# ★ 스윕 축 — 표면에너지 대리 (SJKR, J/m³).  **팔 {arm}: {ARMS[arm]['desc']}**\n# ⚠ 이 블록만 팔마다 다르다.  나머지는 한 글자도 안 바뀐다.
fix mC all property/global cohesionEnergyDensity peratomtypepair {_nt} &
{_mat(_nt, M_ced)}
fix m9 all property/global characteristicVelocity scalar 2.0

# ⚠ cohesion 은 tangential 뒤 · rolling_friction 앞 (순서가 실재하는 제약)
pair_style      gran model hertz tangential history cohesion sjkr rolling_friction cdt
pair_coeff      * *
timestep        {st['dt_txt']}
fix             gravi all gravity 9.81 vector 0.0 0.0 -1.0

# --- 기구 (STL 은 튜토리얼 Mixer 원본을 scale 로 줄여 쓴다) ---
fix Drum  all mesh/surface file Drum.stl  type {_nt} scale {p['stl_scale']:.6g}
fix Front all mesh/surface file Front.stl type {_nt} scale {p['stl_scale']:.6g}
fix Back  all mesh/surface file Back.stl  type {_nt} scale {p['stl_scale']:.6g}
{_baffle_mesh}fix walls all wall/gran model hertz tangential history cohesion sjkr rolling_friction cdt &
    mesh n_meshes {3 + (1 if n_baffles else 0)} meshes Drum Front Back{' Baffle' if n_baffles else ''}

# --- 입자 ---
{_tpl_block}

{_ins_block}
# ⚠⚠ **적분기는 둘 다 필요하다** (2026-09-19 실측으로 확정)
#   `fix multisphere` 는 **강체만** 적분한다 — 평범한 구는 `body_[i] < 0` 로 건너뛴다.
#   이 줄 하나만 두고 돌렸더니 AM·SE 47,309 개가 **얼어붙은 조각상**이었다:
#   KE 가 삽입값에서 한 번도 안 움직였고 E0 과 E4 팔이 H/R 까지 동일했다.
#   ★ 직접 잰 것 — 평구 하나를 중력 아래 2,000 스텝 두니 z 가 0.02 그대로였다.
#   `nve/sphere` 를 얹으면 자유낙하가 정확히 복구되고(vz = −g·t),
#   섬유 결합거리는 0.48000/0.48000/0.96000 mm 로 **소수 5자리까지 불변**이며,
#   섬유 궤적은 nve 가 강체를 건드리지 않는 판과 **부동소수점까지 동일**하다
#   (`multisphere` 가 매 스텝 강체 상태를 다시 덮어쓴다 ⇒ 이중적분 피해 0).
{_integr}

compute rke all erotate/sphere
thermo_style custom step atoms ke c_rke vol
thermo 5000
thermo_modify lost ignore norm no

shell mkdir post
# ★★ 체크포인트 — 측정런은 {steps_run:,} 스텝(실측 ~21.8 step/s 에서 **5일**)인데 덱에 `restart` 가
#   한 줄도 없었다.  재부팅·OOM 한 번에 런 전체가 0 으로 돌아간다 (13 런이면 하나쯤 난다).
#   두 파일을 **번갈아** 써서 쓰다 죽어도 직전 것이 남는다 (디스크 ~40 MB/런).
#   ⚠ 궤적은 안 바뀐다 — I/O 뿐이다 (골든 해시는 그래서 재생성한다).
#   ★ 드럼은 축대칭이라 재시작 때 `fix move/mesh` 의 회전 위상이 0 으로 돌아가도 **기하가 같다**
#     — ps45 플래튼(2026-09-21, 재부양 7.8 mm)과 달리 이 덱에는 그 함정이 없다.
shell mkdir restart
restart {restart_every} restart/a.bin restart/b.bin
run 1
# ⚠ `mol` 은 `fix multisphere` 가 있어야 할당된다 (LIGGGHTS-PUBLIC fix_multisphere.cpp:175; 없으면
#   dump_custom.cpp:1058 "Dumping an atom property that isn't allocated" 로 **즉시 죽는다** — 자가 리뷰 R-1)
dump dmp all custom {dump_every} post/mix_*.liggghts {' '.join(_dump_cols)}{_dump_fmt}

# ① 채우고 정착 — ⚠ KE 가 떨어진 뒤에 회전을 시작한다 (정착 전에 돌리면 지표가 뒤집힌다)
#   정착 {2*steps_fill*st['dt_c']:.3f} s = 낙하 {2*p['R']*1e3:.1f} mm · e {restitution} 에서
#   유도한 t_ff·(1+e)/(1−e) 의 {2.0:.0f}배.  ⛔ 상수 20000 step 을 쓰지 않는다.
#   ⚠ 그래도 잰 뒤 φ(포락) 경고를 확인할 것 — 식은 홑 입자의 튐만 센다.
run {steps_fill}
{_unfix_ins}
run {steps_fill}{_unfix_ins2}

# ★ 정착 끝 상태를 남긴다 — 회전 중 죽어도 정착({2*steps_fill*st['dt_c']:.3f} s)을 다시 안 돈다
write_restart restart/settled.bin

# ② 회전 {revolutions} 바퀴 @ {rpm:.0f} rpm  (임계 {p['rpm_crit']:.0f} rpm · Fr {(2*math.pi/period)**2*p['R']/9.81:.3f})
fix mvD all move/mesh mesh Drum  rotate origin 0 0 0 axis 1. 0. 0. period {period:.6g}
fix mvF all move/mesh mesh Front rotate origin 0 0 0 axis 1. 0. 0. period {period:.6g}
fix mvB all move/mesh mesh Back  rotate origin 0 0 0 axis 1. 0. 0. period {period:.6g}{_baffle_move}
run {steps_run}
"""


def _mat(n, val):
    """peratomtypepair n×n 행렬.  `val` 이 스칼라면 균일, 2차원이면 그대로."""
    if isinstance(val, (list, tuple)):
        return ' &\n'.join('    ' + ' '.join(f'{v:g}' for v in row) for row in val)
    return ' &\n'.join('    ' + ' '.join(f'{val:g}' for _ in range(n)) for _ in range(n))


def _raises(fn):
    try:
        fn()
        return False
    except SystemExit:
        return True


def _selftest():
    ok, fail = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            fail.append(name)
        print(('  PASS  ' if cond else '  FAIL  ') + name)

    phi, wt = volume_fractions()
    chk('① 부피분율 합 = 1', abs(sum(phi.values()) - 1) < 1e-12)
    chk('② wt 합 = 100', abs(sum(wt.values()) - 100) < 1e-9)
    chk('③ AM_P:AM_S wt 비 = 7:3', abs(wt['AM_P'] / wt['AM_S'] - 7 / 3) < 1e-9)
    p = plan(50000)
    chk(f'④ 개수 합이 목표에 맞는다 ({p["n_total"]})', abs(p['n_total'] - 50000) / 50000 < 0.01)
    chk('⑤ SE 가 개수로 최다', max(p['n'], key=p['n'].get) == 'SE')
    #  ★ 변이 대조 — CGF 를 2배 하면 드럼 반경이 2배여야 한다 (부피 ∝ d³ · 개수 고정)
    p2 = plan(50000, cgf=400.0)
    chk('⑥ 변이: CGF ×2 → 드럼 R ×2', abs(p2['R'] / p['R'] - 2) < 0.02)
    chk('⑦ 변이: CGF ×2 → dt ×2', abs(p2['dt'] / p['dt'] - 2) < 0.02)
    #  ★ 섬유 파일 — 강체가 되도록 겹쳐야 한다
    txt = fibre_file(5, 1e-3)
    xs = [float(l.split()[0]) for l in txt.strip().split('\n')]
    gap = xs[1] - xs[0]
    chk('⑧ 섬유 구가 겹친다 (중심간 < 지름)', gap < 1e-3)
    chk('⑨ 섬유가 원점 대칭', abs(xs[0] + xs[-1]) < 1e-12)
    dk = deck(p, rpm=60, revolutions=5)
    chk('⑩ 덱에 cohesion 이 tangential 뒤·rolling 앞',
        'tangential history cohesion sjkr rolling_friction' in dk)
    #  ★★ 생산 기본(3 상)에는 섬유가 없다 ⇒ 강체 적분기도 **없어야** 한다 (빈 그룹이면
    #    LIGGGHTS 가 죽는다).  섬유 기계 자체는 5 상 경로로 계속 시험한다.
    _saved_types = TYPES
    try:
        set_phases(ALL_TYPES)
        dk5 = deck(plan(8000), rpm=60, revolutions=5)
    finally:
        set_phases(_saved_types)
    chk('⑪ 섬유가 있으면 multisphere 적분기를 쓴다 (5 상 경로)',
        'fix integr  all multisphere' in dk5)
    #  ⚠ `'multisphere' not in dk` 로 쓰면 안 된다 — 머리말 주석의 `processors 1 1 1
    #    # PUBLIC 판 multisphere 는 직렬만 지원` 에 걸려 **항상 실패**한다 (실제로 걸렸다).
    chk('⑪f ★ dump 열 `mol` 은 섬유가 있을 때만 (없으면 LIGGGHTS 가 즉시 죽는다 — 리뷰 R-1)',
        'id type mol x y z' in dk5 and 'id type x y z' in dk and ' mol ' not in dk.split('dump dmp')[1].split('\n')[0])
    chk('⑪a ★ 섬유가 없으면 multisphere 적분기가 **없다** (3 상 = 생산 기본)',
        'fix integr  all multisphere' not in dk
        and 'particletemplate/multisphere' not in dk
        and 'fix integrS all nve/sphere' in dk)
    #  ★⑪b 재현 시험 — 이 결함이 실제로 났다.  `multisphere` 는 강체만 적분하므로
    #     평범한 구 템플릿이 있으면 `nve/sphere` 가 **반드시** 같이 있어야 한다.
    _has_sphere_tpl = 'particletemplate/sphere' in dk
    chk('⑪b 평범한 구가 있으면 nve/sphere 적분기도 있다 (없으면 조각상이 된다)',
        (not _has_sphere_tpl) or ('fix integrS all nve/sphere' in dk))
    #  ★⑪c 순서 — nve 가 먼저, multisphere 가 나중 (강체를 최종 확정)
    chk('⑪c nve/sphere 가 multisphere 보다 먼저 정의된다 (5 상 경로)',
        dk5.index('fix integrS all nve/sphere') < dk5.index('fix integr  all multisphere'))
    #  ★⑪d 정착식 앵커 — 튜토리얼 실측을 맞히는가 (낙하 60 mm · e 0.9 → 2.1 s)
    _t = settle_time(0.060, 0.9, margin=1.0)
    chk(f'⑪d 정착식이 튜토리얼 실측 2.1 s 를 맞힌다 (식 {_t:.2f} s)',
        abs(_t - 2.1) < 0.1)
    #  ★⑪e 변이 — 정착 스텝이 **상수가 아니다** (드럼이 커지면 길어져야 한다)
    _small = deck(plan(4000), rpm=60, revolutions=1)
    _big = deck(plan(32000), rpm=60, revolutions=1)
    import re as _re
    _f = lambda t: int(_re.search(r'run (\d+)\nunfix ins', t).group(1))
    chk(f'⑪e 변이: 정착 스텝이 드럼 크기를 따라간다 ({_f(_small):,} → {_f(_big):,})',
        _f(_big) > _f(_small) * 1.3)
    chk('⑫ 생산 scale=1000 규약을 안 쓴다', 'scale 1000' not in dk)
    #  ★★ 체크포인트 (2026-09-21) — 측정런이 실측 ~21.8 step/s 에서 **5일**인데 덱에 `restart` 가
    #    없었다.  재부팅 한 번에 런 전체가 0 이 된다.  I/O 뿐이라 궤적은 안 바뀐다.
    chk('⑬a ★ `restart` 체크포인트가 있고 두 파일을 **번갈아** 쓴다 (쓰다 죽어도 직전이 남는다)',
        _re.search(r'^restart \d+ restart/a\.bin restart/b\.bin$', dk, _re.M) is not None)
    chk('⑬b ★ `shell mkdir restart` 가 `restart` 줄보다 앞이다 (디렉터리 없으면 LIGGGHTS 가 못 쓴다)',
        dk.index('shell mkdir restart') < dk.index('\nrestart '))
    chk('⑬c ★ `restart` 가 첫 `run` 보다 앞이다 (뒤면 그 run 은 체크포인트가 없다)',
        dk.index('\nrestart ') < dk.index('\nrun '))
    chk('⑬d ★ 정착 끝에 `write_restart` — 회전 중 죽어도 정착을 다시 안 돈다',
        'write_restart restart/settled.bin' in dk
        and dk.index('write_restart') < dk.index('fix mvD'))
    _re_every = int(_re.search(r'^restart (\d+) ', dk, _re.M).group(1))
    chk(f'⑬e 체크포인트 간격이 밴드 [50,000, 200,000] 안이다 ({_re_every:,})',
        50_000 <= _re_every <= 200_000)
    #  ★ 변이 — 회전 0 인 기준런도 체크포인트를 찍는다 (옛 식은 steps_run=0 이라 0 으로 죽었다)
    _dk0 = deck(p, rpm=60, revolutions=0, seed=32452843, arm='E0')
    chk('⑬f 변이: 회전 0 기준런도 `restart` 간격이 양수다 (정착만 도는 런)',
        int(_re.search(r'^restart (\d+) ', _dk0, _re.M).group(1)) > 0)
    #  ★ 실행이 가르쳐 준 제약 (2026-09-21 스모크): E > 1e9 는 LIGGGHTS 가 거부한다
    chk('⑫b ★ E > 1e9 이면 `hard_particles yes` 가 있다 (없으면 LIGGGHTS 가 거부)',
        (max(E_PHASE[t] for t in TYPES + (WALL,)) <= 1e9) or ('hard_particles  yes' in dk))
    # ⚠ 낱말 `youngsModulus` 로 찾으면 **바로 위 주석**이 먼저 걸린다 (2026-09-21 실제로 걸렸다).
    #   실제 지시어(`fix m1 … youngsModulus`)를 찾는다 — 주석은 `fix ` 로 시작하지 않는다.
    chk('⑫c ★ `hard_particles` 는 물성 선언보다 **앞**에 온다',
        dk.index('\nhard_particles') < dk.index('\nfix m1 all property/global youngsModulus'))
    #  ★ 실행으로 배운 제약 — multisphere 템플릿 번호는 1 부터 연속이어야 한다
    import re as _re
    _t = [int(m) for m in _re.findall(r'\.multisphere scale [\d.]+ type (\d+)', dk5)]
    chk(f'⑬ multisphere 템플릿 번호가 1 부터 연속 ({_t})',
        _t == list(range(1, len(_t) + 1)))
    #  변이 대조 — atom_type 은 그대로 4·5 여야 한다 (둘을 헷갈리면 상이 섞인다)
    #  ★ 겹침 보정 — 3구 사슬은 구 3개 합의 약 0.963 배여야 한다 (해석값)
    f3 = chain_volume_factor(3)
    chk(f'⑮ 3구 사슬 부피계수 {f3:.4f} ≈ 0.9627 (해석)', abs(f3 - 0.9627) < 5e-3)
    chk('⑯ 변이: nsph=1 이면 보정 없음', chain_volume_factor(1) == 1.0)
    chk('⑰ 변이: 사슬이 길수록 계수가 준다', chain_volume_factor(5) < f3)
    chk('⑭ 변이: 5 상 경로에서 atom_type 은 그대로 4·5 다 (템플릿 번호와 헷갈리면 상이 섞인다)',
        'atom_type 4' in dk5 and 'atom_type 5' in dk5)
    chk('⑭b ★ 3 상 경로는 atom_type 3 까지만 쓰고 create_box 도 3 이다',
        'atom_type 4' not in dk and 'create_box      4 reg' in dk)   # 3 상 + 벽 타입
    #  ★ 팔 — 점착 블록만 달라야 한다
    d0, d1, d2 = (deck(p, 60, 5, arm=x) for x in ('E0', 'E1', 'E2'))
    def _strip_ced(t):
        '''점착 블록과 **주석**을 뺀 실행 줄만 남긴다.

        ⚠ 주석을 빼는 이유 — 팔 이름이 주석에 들어가서 달라진다.  주석은 물리가
          아니므로 비교 대상이 아니다.  그러나 **실행되는 줄은 한 글자도 달라서는
          안 된다** — 그것이 이 시험의 계약이다.
        '''
        out, skip = [], False
        for ln in t.split('\n'):
            if 'cohesionEnergyDensity' in ln:
                skip = True
                continue
            if skip:
                if ln.startswith('    ') or ln.strip() == '&':
                    continue
                skip = False
            st = ln.strip()
            if st.startswith('#') or not st:
                continue
            out.append(ln)
        return '\n'.join(out)
    chk('⑱ 팔끼리 점착 블록 **밖**은 한 글자도 안 다르다',
        _strip_ced(d0) == _strip_ced(d1) == _strip_ced(d2))
    chk('⑲ 팔끼리 점착 블록은 실제로 다르다', d0 != d1 != d2 and d0 != d2)
    dd = p['d']
    M0, M1, M2 = (ced_matrix('E0', dd), ced_matrix('E1', dd), ced_matrix('E2', dd))
    chk('⑳ E0 는 전부 0 (음성 대조)', all(v == 0 for r in M0 for v in r))
    chk('㉑ E2 는 AM-AM 만 Bo ×10 = CED ×10^(1/3)',
        abs(M2[0][0] / M1[0][0] - 10 ** (1 / 3.)) < 1e-6
        and abs(M2[2][2] - M1[2][2]) < 1e-9)
    chk('㉒ 행렬이 대칭이다 (비대칭 입력 방지)',
        all(M2[i][j] == M2[j][i] for i in range(len(TYPES)) for j in range(len(TYPES))))
    #  변이 대조 — 대칭 강제가 장식이 아님을 보인다
    ARMS['_t'] = dict(desc='t', bond=1.0, abs_base=BO_BASE, abs_mult={('AM_P', 'SE'): 7.0 * BO_BASE})
    Mt = ced_matrix('_t', dd); del ARMS['_t']
    chk('㉓ 변이: 한쪽만 준 배수가 양쪽에 반영된다',
        Mt[0][2] == Mt[2][0] and Mt[0][2] > Mt[2][2])

    #  ★ 시드 — 판정선(§7)이 SE_시드를 요구한다.  시드는 **삽입 줄 하나만** 바꿔야 한다
    ds1 = deck(p, rpm=60, revolutions=1, arm='E1', seed=32452843)
    ds2 = deck(p, rpm=60, revolutions=1, arm='E1', seed=91648301)
    dif = [(x, y) for x, y in zip(ds1.split('\n'), ds2.split('\n')) if x != y]
    chk(f'㉓b 시드는 삽입 줄 하나만 바꾼다 (다른 줄 {len(dif)})',
        len(dif) == 1 and 'insert/pack seed' in dif[0][0])

    #  ★ 시드 소수 검사 — 합성수를 주면 LIGGGHTS 가 셋업 뒤에 죽어 '조용한 실패' 로 읽힌다
    chk('㉓c 합성수 시드를 **덱 쓰기 전에** 거부한다 (57204983 = 합성수)',
        _raises(lambda: deck(p, rpm=60, revolutions=1, seed=57204983)))
    chk('㉓d 소수 시드는 통과한다 (49979687)',
        not _raises(lambda: deck(p, rpm=60, revolutions=1, seed=49979687)))

    #  ★★ ㉛ 배플 — `n=0` 이면 덱이 **배플 이전과 글자 그대로 같아야** 한다.
    #     이게 깨지면 "배플 없는 팔" 을 다시 돌려야 하고, 그러면 배플 비교가
    #     **두 축(배플 + 재실행 잡음)** 을 동시에 바꾼 비교가 된다.
    d_none = deck(p, rpm=60, revolutions=1, arm='E1', n_baffles=0)
    d_base = deck(p, rpm=60, revolutions=1, arm='E1')          # 기본값 = 배플 없음
    chk('㉛ ★ 배플 0 개면 덱이 배플 이전과 **바이트 동일**', d_none == d_base)
    d_baf = deck(p, rpm=60, revolutions=1, arm='E1', n_baffles=6, baffle_h=0.10)
    chk('㉛b 배플을 켜면 메시가 4개가 되고 회전도 같이 받는다',
        'n_meshes 4 meshes Drum Front Back Baffle' in d_baf
        and 'mvBf all move/mesh mesh Baffle rotate' in d_baf
        and 'Baffles.stl' in d_baf)
    #  ★ 변이 — 배플 덱과 무배플 덱의 차이가 **배플 줄뿐**이어야 한다
    _drop = lambda t: '\n'.join(l for l in t.split('\n')
                                if 'Baffle' not in l and 'n_meshes' not in l)
    chk('㉛c 변이: 배플 줄을 빼면 나머지는 한 글자도 안 다르다',
        _drop(d_baf) == _drop(d_none))
    #  ★ 회전 주기가 드럼과 같아야 한다 (따로 돌면 기구가 아니라 교반기가 된다)
    import re as _re2
    #  ⚠ 덱은 정렬용으로 `Drum  rotate` 처럼 **공백 두 개**를 쓴다 — ` +` 로 받는다
    #    (초판 정규식이 공백 하나라 4개 중 2개만 잡아 시험이 실패했다 — 코드가
    #     아니라 **시험이** 틀린 경우다)
    _per = _re2.findall(r'move/mesh mesh \w+ +rotate origin 0 0 0 axis 1\. 0\. 0\. '
                        r'period ([0-9.eE+-]+)', d_baf)
    chk(f'㉛d 배플이 드럼과 **같은 주기**로 돈다 ({len(_per)} 메시, 값 {set(_per)})',
        len(_per) == 4 and len(set(_per)) == 1)
    #  ★★ ㉛e — ㉛ 이 **놓쳤던** 것.  ㉛ 은 '지금 만든 두 출력' 을 비교하므로 둘 다
    #     똑같이 망가지면 통과한다.  실제로 `{_baffle_move}` 가 제 줄을 차지해
    #     배플 0 덱에 **빈 줄 하나**가 더 생겼고, 이미 돌린 런의 덱과 바이트가
    #     달라졌는데 ㉛ 은 초록이었다.  ⇒ **구조를 직접 못 박는다.**
    _lines = d_none.split('\n')
    _mvb = next(i for i, l in enumerate(_lines) if 'move/mesh mesh Back' in l)
    chk('㉛e ★ 배플 0 덱의 회전 블록 뒤에 **빈 줄이 안 생긴다** '
        '(두 출력 비교로는 못 잡는 자리)',
        _lines[_mvb + 1].strip() != '')
    #  배플 덱은 정확히 **세 줄만** 다르다 (메시 · n_meshes · 회전)
    import difflib as _dl
    _dif = [l for l in _dl.unified_diff(d_none.split('\n'), d_baf.split('\n'), n=0)
            if l[:1] in '+-' and l[:3] not in ('+++', '---')]
    chk(f'㉛f 배플 덱은 정확히 메시·n_meshes·회전 **세 자리만** 다르다 (실제 {len(_dif)} 줄)',
        len(_dif) == 4 and sum(1 for l in _dif if l.startswith('+')) == 3)

    #  ★★ ㉜ 코팅 팔 — "AM 표면이 SE 가 된다"
    Mc = ced_matrix('C1', dd)
    M1 = ced_matrix('E1', dd)
    _i = {t: k for k, t in enumerate(TYPES)}
    #  ★ 코팅 규약 (2026-09-21 변경): CED 복사가 아니라 **JKR 힘 스케일링으로 Bo** 를 준다.
    #    옛 기대(*"AM-AM CED 가 SE-SE 값이 된다"*)는 상별 E 가 갈리면 Bo ~1e-6 으로 무너진다.
    _geo = lambda src, t: (dd[src] ** 2 * DENS[PHASE_MECH[src][1]]) / (dd[t] ** 2 * DENS[PHASE_MECH[t][1]])
    _boP = bond_for_ced(Mc[0][0], dd['AM_P'] / 2, .25, DENS['AM'], E=E_PHASE['AM_P'])
    chk(f'㉜ 코팅된 AM_P 의 Bo = SE Bo × (r_SE²ρ_SE)/(r_AM²ρ_AM) = {BO_BASE*_geo("SE","AM_P"):.5f} (실측 {_boP:.5f})',
        abs(_boP / (BO_BASE * _geo('SE', 'AM_P')) - 1.0) < 1e-6)
    chk('㉜a 변이: AM 을 104배 무르게 해도 코팅 Bo 는 **E 에 불변** (JKR 정의의 요점)',
        abs(bond_for_ced(ced_for_bond(_boP, dd['AM_P'] / 2, .25, DENS['AM'], E=E_PHASE['AM_P'] / 104),
                         dd['AM_P'] / 2, .25, DENS['AM'], E=E_PHASE['AM_P'] / 104) / _boP - 1.0) < 1e-9)
    chk('㉜b SE-SE 자신은 안 바뀐다 (코팅재를 건드리지 않는다)',
        abs(Mc[_i['SE']][_i['SE']] - M1[_i['SE']][_i['SE']]) < 1e-9)
    chk('㉜c AM-SE 는 원래 SE 값이었으므로 코팅해도 그대로',
        abs(Mc[_i['AM_P']][_i['SE']] - M1[_i['AM_P']][_i['SE']]) < 1e-9)
    chk('㉜d 코팅 행렬도 대칭이다',
        all(Mc[i][j] == Mc[j][i] for i in range(len(TYPES)) for j in range(len(TYPES))))
    #  ★ 변이 — 코팅 안 하면 AM-AM 이 SE-SE 와 **다르다** (덮어쓰기가 장식이 아님)
    chk(f'㉜e 변이: 코팅 없으면 AM-AM ≠ SE-SE '
        f'({M1[_i["AM_P"]][_i["AM_P"]]:.3g} vs {M1[_i["SE"]][_i["SE"]]:.3g})',
        abs(M1[_i['AM_P']][_i['AM_P']] - M1[_i['SE']][_i['SE']]) > 1e3)
    #  ★ 코팅은 **덜 끈적하게** 만든다 (AM 이 크고 무거워 같은 Bo 에 더 큰 CED 가 필요했다)
    chk('㉜f 코팅이 AM-AM 점착을 **낮춘다** (방향)',
        Mc[_i['AM_P']][_i['AM_P']] < M1[_i['AM_P']][_i['AM_P']])

    #  ★★ ㉝ 고-G 팔 — 중력이 아니라 **Bo 를 내려** 기계를 표현한다
    #  ⛔ 고-G 팔 T1·T2 시험(㉝·㉝b·㉝c)은 팔 폐지와 함께 제거 (기계는 사다리에서 읽는다, 원장 §10)
    #  ★ 변이 — 중력을 268배 올렸다면 Π₁ 이 268배가 되어 규약이 깨진다는 것을 못 박는다
    _P1 = lambda a, E: 4800.0 * a * (dd['AM_P'] / 2) / E
    chk(f'㉝d 변이: 중력을 268배 올리면 Π₁=ρaR/E 가 268배가 된다 '
        f'({_P1(9.81, E_YOUNG):.2e} → {_P1(9.81*268, E_YOUNG):.2e}) — 스케일 팩터 위반',
        abs(_P1(9.81 * 268, E_YOUNG) / _P1(9.81, E_YOUNG) - 268.0) < 1e-6)

    #  ★★ 점착 눈금 — **실측 앵커**.  이 다섯이 새 사다리의 근거다.
    #  실측 3.50 % — 강체 내부 쌍을 제외하고 다시 잰 값 (초판 3.54 % 는 섬유 자기겹침 포함)
    chk(f'㉔ 겹침식이 E1 실측을 맞힌다 (예측 {overlap_for_ced(3e5, 3e-4, .30)*100:.2f} % '
        f'vs 실측 3.50 %)',
        abs(overlap_for_ced(3e5, 3e-4, .30) - 0.0350) < 0.006)
    chk(f'㉕ 겹침식이 ×10 붕괴를 설명한다 (CED 3e6 → '
        f'{overlap_for_ced(3e6, 3e-4, .30)*100:.0f} % = 통과)',
        overlap_for_ced(3e6, 3e-4, .30) > 1.0)
    chk('㉖ δ/r 은 CED 의 **제곱**이다 (×10 이 ×100)',
        abs(overlap_for_ced(2e5, 3e-4, .30) / overlap_for_ced(1e5, 3e-4, .30) - 4.0) < 1e-9)
    chk('㉗ Bo 는 CED 의 **세제곱**이다 (사다리를 Bo 로 거는 이유)',
        abs(bond_for_ced(2e5, 3e-4, .30, 2.0) / bond_for_ced(1e5, 3e-4, .30, 2.0) - 8.0) < 1e-9)
    chk('㉘ ced_for_bond ↔ bond_for_ced 왕복',
        abs(bond_for_ced(ced_for_bond(7.0, 3e-4, .30, 2.0), 3e-4, .30, 2.0) - 7.0) < 1e-9)
    #  ★★ 천장 — **모든 팔이 겹침 천장 안**이어야 한다.  초판은 4/5 가 밖이었다.
    #  ★ 2026-10-05 (dev-u · 강성 축 사전등록 §12) — δ/r ∝ CED² ∝ (Bo·r)^(2/3) 라 같은 절대 Bo 면 parcel 이 클수록 겹침이 크다.  LU637 (SE 쪽
    #    Bo_code 637.32) 은 캠페인 CGF 151.4 에서 SE–SE 0.837 % 로 천장 안이지만 이 시험의 CGF 200 (dd) 에서는 1.007 % 로 밖 = 생성기가 거부한다
    #    (의도 · fail-closed).  ⇒ 그런 팔은 **선언 목록** _CGF_BOUND 로만 뺀다 — U⑥ 이 '이 CGF 에서 거부 · 캠페인 CGF 에서 수용' 을 단언하고
    #    (목록이 조용히 늘지 않게) · ㉙c 가 캠페인 CGF 의 천장을 **전 팔**로 본다.
    _CGF_BOUND = ('LU637',)
    worst = []
    for arm in sorted(set(ARMS) - set(_CGF_BOUND)):
        M = ced_matrix(arm, dd)
        for i, ti in enumerate(TYPES):
            small_r = dd[ti] / 2.0
            worst.append((overlap_for_ced(M[i][i], small_r, PHASE_MECH[ti][0], E=E_PHASE[ti]), arm, ti))
            worst.append((overlap_for_ced(M[i][len(TYPES)], small_r, PHASE_MECH[ti][0], E=E_PHASE[ti]), arm, ti + '–WALL'))
    wv, wa, wt = max(worst)
    chk(f'㉙ ★ 모든 팔이 겹침 천장 {OVL_CEILING*100:.0f} % 안 '
        f'(최악 {wa}·{wt} {wv*100:.3f} %)', wv <= OVL_CEILING * (1 + 1e-9))
    #  ★ 변이 — 옛 사다리(CED 3e5 에 ×100)를 넣으면 이 검사가 **걸려야** 한다
    chk('㉙b 변이: 옛 사다리(CED 3e7)는 천장을 넘는다',
        overlap_for_ced(3e7, 3e-4, .30) > OVL_CEILING)
    _pcd = plan(100000, cgf=151.4)['d']                 # 캠페인 조건 (gen_all.sh 기본 N_TOTAL · CGF)
    _wc = max((overlap_for_ced(_Mc_[i][_j], _pcd[ti] / 2.0, PHASE_MECH[ti][0], E=E_PHASE[ti]), arm, ti + ('–WALL' if _j == len(TYPES) else ''))
              for arm in sorted(ARMS) for _Mc_ in (ced_matrix(arm, _pcd),) for i, ti in enumerate(TYPES) for _j in (i, len(TYPES)))
    chk(f'㉙c ★ 캠페인 CGF 151.4 에서는 **전 팔** (CGF 묶인 선언 팔 {list(_CGF_BOUND)} 포함) 이 겹침 천장 안 '
        f'(최악 {_wc[1]}·{_wc[2]} {_wc[0]*100:.3f} %)', _wc[0] <= OVL_CEILING * (1 + 1e-9))
    #  ★ 상별 CED 가 실제로 다르다 (같은 Bo 를 만들려면 달라야 한다)
    chk(f'㉚ 같은 Bo 를 위해 상별 CED 가 다르다 '
        f'(AM_P {M1[0][0]:.3g} vs SE {M1[2][2]:.3g})',
        abs(M1[0][0] - M1[2][2]) / M1[2][2] > 0.1)
    #  ── §24 층상 팔 ──────────────────────────────────────────────────────────
    import hashlib as _hl
    _p8 = plan(8000)
    chk('㉞ ★ 점착이 있는 모든 팔이 절대 Bo(abs_base) 다 — BOND0 상대 팔 0 개',
        all(('abs_base' in a) == (a['bond'] > 0) for a in ARMS.values()))
    chk('㉞b ★ 상대 팔(mult 만)은 덱 생성이 **거부**된다 (fail-closed)',
        (ARMS.__setitem__('_rel', dict(desc='r', bond=1.0, mult={('AM_P', 'AM_P'): 10.})) or
         _raises(lambda: ced_matrix('_rel', _p8['d']))) and (ARMS.pop('_rel') is not None))
    chk('㉞c ★ 캠페인 6 팔이 전부 층상이고 10 런이다 (4×1 + LA·LC 3 시드, 원장 §10)',
        all(ARMS[a].get('layered') for a in ('L0', 'LC', 'LB1', 'LB2', 'LB3', 'LA')) and len(CAMPAIGN) == 10
        and sum(1 for a, _ in CAMPAIGN if a in ('LA', 'LC')) == 6)
    chk('㉞d ★ 기준 런 3 개 = E0(균일·점착 0) · 캠페인 시드 · 회전 0 (판독기 --ref 상대, 리뷰 R-2)',
        len(REFERENCE) == 3 and all(a == 'E0' and r == 0 for a, _, r in REFERENCE)
        and {sd for _, sd, _ in REFERENCE} == set(CAMPAIGN_SEEDS)
        and 'run 0\n' in deck(_p8, rpm=60, revolutions=0, arm='E0'))
    #  ★★ 진짜 "Bo 라벨이 안 밀린다" 는 **지름을 흔들어야** 보인다 — ㉞ 는 팔만 흔든다.
    #    초판(`mult = 목표Bo / 0.21244`)은 AM_P 12 → 9 µm 에서 LA 를 3.0 → **4.00** 으로
    #    밀었고 ㉞ 는 그것을 **못 잡았다** (BOND0 자체는 그 시점에 맞았으므로).
    def _bo_amp(arm, dd_):
        _nu, _mat = PHASE_MECH['AM_P']
        return bond_for_ced(ced_matrix(arm, dd_)[0][0], dd_['AM_P'] / 2.0, _nu, DENS[_mat], E=E_PHASE['AM_P'])
    chk('㊺ ★ LA 의 AM_P Bo_code 3.0 (내부 기준점 — R-4 로 앵커 라벨 철회) 이 **지름·CGF 를 흔들어도** 안 밀린다',
        all(abs(_bo_amp('LA', plan(8000, cgf=_c)['d']) - 3.0) < 1e-9
            for _c in (100.0, 200.0, 400.0)))
    chk('㊺b ★ B5·B10 경계탐침 Bo 0.5·1.0 도 CGF 에 불변',
        all(abs(_bo_amp(_a, plan(8000, cgf=_c)['d']) - _t) < 1e-9
            for _a, _t in (('B5', 0.5), ('B10', 1.0)) for _c in (100.0, 400.0)))
    #  ★ 천장은 `ced_matrix` 가 단언하지만, 여기서 값을 **보이게** 한 번 더 잰다
    chk(f"㊺c 절대-Bo 팔이 겹침 천장 {OVL_CEILING*100:.1f} % 안이다 "
        f"(LA {overlap_for_ced(ced_matrix('LA', _p8['d'])[0][0], _p8['d']['AM_P']/2, 0.25, E=E_PHASE['AM_P'])*100:.3f} %)",
        all(overlap_for_ced(ced_matrix(_a, _p8['d'])[_i][_i], _p8['d'][_t] / 2.0,
                            PHASE_MECH[_t][0], E=E_PHASE[_t]) <= OVL_CEILING
            for _a in ('B5', 'B10', 'LA') for _i, _t in enumerate(TYPES)))
    #  ⚠ 2026-09-21 3차 갱신 — 3 상 · SE 1 µm · 벽 타입 · 영률 ÷135 · 마찰 hare2026 ·
    #    전 팔 절대 Bo · 코팅 JKR 규약 · **dump `mol` 조건부(R-1)**.  T1·B5 대신 LA·LC 를 골든에 넣는다.
    #  ⚠ 2026-09-27 — LA·LC 는 **설명 문자열 (주석 한 줄) 만** 바꿨다 (R-4 · R-3 · Codex HB-01) → 새 골든.  ㉟b 가
    #    옛 문자열로 옛 골든 (LA d2ab3fc53e034cdf · LC c9d084b40c16c880) 을 재현해 '물리 명령 불변' 을 보인다.  LH 신설.
    _gold = {'E0': '8e95e2253498ce9b', 'E1': 'd5a34634afc8c88c', 'E4': '8a55492ec2404e65', 'C1': 'df1c9f0501d65711',
             'LA': '92d1e13b6844e820', 'LC': '96d67c6adea0b7c1', 'LH': '8d299fc7aaa0f858'}
    _got = {a: _hl.sha256(deck(_p8, rpm=60, revolutions=2, seed=32452843, arm=a)
                          .encode()).hexdigest()[:16] for a in _gold}
    chk('㉟ 기존 팔 덱이 편집 전과 **바이트 동일** (골든 해시, plan(8000)·2바퀴·시드 32452843; LA·LC 는 09-27 주석 정정판)',
        _got == _gold)
    _old_desc = {'LA': ('§24 층상 · 무코팅 AM Bo 3.0 = 문헌 앵커 (hare2026) — 헤드라인 무코팅', 'd2ab3fc53e034cdf'),
                 'LC': ('§24 층상 · 코팅 (AM 표면 = SE, C1 규약) — 헤드라인 코팅', 'c9d084b40c16c880')}
    _rep = {}
    for _a, (_ds, _h) in _old_desc.items():
        _new = ARMS[_a]['desc']
        try:
            ARMS[_a]['desc'] = _ds
            _old_deck = deck(_p8, rpm=60, revolutions=2, seed=32452843, arm=_a)
        finally:
            ARMS[_a]['desc'] = _new
        _nd = [(x, y) for x, y in zip(_old_deck.split('\n'), deck(_p8, rpm=60, revolutions=2, seed=32452843,
                                                                  arm=_a).split('\n')) if x != y]
        _rep[_a] = (_hl.sha256(_old_deck.encode()).hexdigest()[:16] == _h and len(_nd) == 1
                    and _nd[0][0].startswith('# ★ 스윕 축'))
    chk('㉟b ★ LA·LC 정정은 주석 한 줄뿐 — 옛 설명 문자열이면 옛 골든 해시 그대로 (돌고 있는 런의 덱 = 물리 동일)',
        all(_rep.values()) and len(_rep) == 2)
    _la = deck(_p8, rpm=60, revolutions=2, seed=32452843, arm='LA')
    chk('㊱ LA 는 insert/pack 둘(insA→원통 전체, insB→AM 침대 위 블록), pdd 둘, unfix 둘',
        _la.count('insert/pack') == 2 and 'pddA' in _la and 'pddB' in _la
        and 'unfix insA' in _la and 'unfix insB' in _la
        and 'region ins_reg particles_in_region' in _la and 'region ins_hi particles_in_region' in _la)
    _i_s1 = _la.index('run 36308') if 'run 36308' in _la else _la.index('run ', _la.index('unfix insA') - 40)
    chk('㊱b 순서: insA → 정착① → unfix insA·insB 정의 → 정착② → unfix insB → 회전',
        _la.index('fix insA') < _la.index('unfix insA') < _la.index('fix insB')
        < _la.index('unfix insB') < _la.index('fix mvD'))
    import re as _re
    _nA = int(_re.search(r'region ins_reg particles_in_region (\d+)', _la).group(1))
    _nB = int(_re.search(r'region ins_hi particles_in_region (\d+)', _la).group(1))
    #  ⚠ plan() 은 상별로 반올림하므로 상별 합이 n_tpl_total 과 ±1~2 다를 수 있다.
    #    균일 삽입은 총수(n_tpl_total)를, 층상은 상별 합을 쓴다 — 층상이 조성에 더 충실하다.
    _sum_tpl = sum(_p8['n_tpl'].values())
    chk('㊲ 두 층의 템플릿 수 합 = 상별 계획의 합 (입자를 잃지 않는다; 총수와는 반올림 ±2 안)',
        _nA + _nB == _sum_tpl and abs(_sum_tpl - _p8['n_tpl_total']) <= 2
        and _nA == _p8['n_tpl']['AM_P'] + _p8['n_tpl']['AM_S'])
    _seeds = [int(x) for x in _re.findall(r'insert/pack seed (\d+)', _la)]
    _pdds = [int(x) for x in _re.findall(r'particledistribution/discrete (\d+)', _la)]
    chk('㊳ 삽입·분포 시드 넷이 전부 소수이고 쌍끼리 다르다',
        all(_is_prime(x) for x in _seeds + _pdds) and _seeds[0] != _seeds[1] and _pdds[0] != _pdds[1])
    _hi = _re.search(r'region ins_hi block \S+ \S+ (\S+) (\S+) (\S+) (\S+)', _la).groups()
    _y, _zl, _zh = abs(float(_hi[0])), float(_hi[2]), float(_hi[3])
    _ztop = float(_re.search(r'z_top (\S+) mm', _la).group(1)) * 1e-3
    chk('㊴ SE 층 블록: 아랫면 ≥ AM 침대 윗면 + AM_P 지름, 윗면 0.78R, 모서리가 원 안(y²+z²<R²)',
        #  덱은 z_top 을 0.01 mm, 좌표를 6 유효숫자로 찍는다 → 허용오차 1e-5 m / 상대 1e-4
        _zl >= _ztop + _p8['d']['AM_P'] - 1e-5 and abs(_zh - 0.78 * _p8['R']) < 1e-4 * _p8['R']
        and _y ** 2 + _zh ** 2 < _p8['R'] ** 2 and _y ** 2 + _zl ** 2 < _p8['R'] ** 2)
    #  RSA 여유: SE 층 블록의 중심 가용부피 대비 SE+섬유 구 부피 (스모크 사고의 정량 가드)
    _dse = _p8['d']['SE']
    _vsol = sum(_p8['n'][k] * (math.pi / 6) * _p8['d'][k] ** 3 for k in TYPES if not k.startswith('AM_'))
    _vc = (0.9 * _p8['L'] - _dse) * (1.2 * _p8['R'] - _dse) * ((_zh - _zl) - _dse)
    chk(f'㊴b SE 층 삽입 밀도 {_vsol/_vc*100:.0f} % < 30 % (RSA 잼 한계 아래)', _vsol / _vc < 0.30)
    #  ★ 상 집합이 바뀌어도 성립해야 한다 — `pt3 … pt5` 를 박아 두면 3 상에서 깨진다
    _fa = [float(x) for x in _re.findall(r'pt\d+ (\S+)',
                                         _re.search(r'pddA .*?\n\s*(.+)', _la).group(1))]
    _fb = [float(x) for x in _re.findall(r'pt\d+ (\S+)',
                                         _re.search(r'pddB .*?\n\s*(.+)', _la).group(1))]
    chk('㊵ 층별 mass% 가 각각 1 로 재정규화된다',
        abs(sum(_fa) - 1) < 2e-6 and abs(sum(_fb) - 1) < 2e-6)
    _M = ced_matrix('LA', _p8['d'])
    chk('㊶ LA 의 AM_P–AM_P Bo_code 가 3.0 (내부 기준점) 이다',
        abs(bond_for_ced(_M[0][0], _p8['d']['AM_P'] / 2, .25, DENS['AM'], E=E_PHASE['AM_P']) - 3.0) < 1e-3)
    _Mc = ced_matrix('LC', _p8['d']); _M1 = ced_matrix('C1', _p8['d'])
    chk('㊷ LC 의 CED 행렬은 C1 과 같다 (코팅 규약을 두 벌 두지 않는다)', _Mc == _M1)
    _l0 = deck(_p8, rpm=60, revolutions=2, seed=32452843, arm='L0')
    chk('㊸ L0 도 층상이고 점착 0 이다', _l0.count('insert/pack') == 2 and 'cohesionEnergyDensity' in _l0)

    #  ★★ 선언 ↔ 사용 — 이 결함이 실제로 있었다 (2026-09-21).  표에 `SE 1.0` 을 적어 두고
    #     코드는 `AM_P×0.25` 를 썼다.  AM_P 12 에서 `AM_S` 만 우연히 맞아 **아무도 못 봤다**.
    #     ⇒ 표에 적힌 값이 **실제로 쓰인 값**인지 매번 확인한다.
    for _cg in (200.0, 137.0):
        _pd = plan(8000, cgf=_cg)['d']
        _bad = [k for k in TYPES if abs(_pd[k] / _cg * 1e6 - D_REAL_UM[k]) > 1e-9]
        chk(f'㊹ CGF {_cg:g}: 표의 실제 지름 = 실제로 쓰인 지름 (어긋남 {len(_bad)})', not _bad)
    #  ⚠ 변이 대조 — 표를 바꾸면 덱도 바뀌어야 한다 (표가 장식이 아님을 보인다)
    _base_s = plan(8000)['d']['AM_S']
    _orig = D_REAL_UM['AM_S']
    try:
        D_REAL_UM['AM_S'] = _orig * 1.5
        _moved = plan(8000)['d']['AM_S']
    finally:
        D_REAL_UM['AM_S'] = _orig
    chk('㊹b 변이: 표의 AM_S 를 ×1.5 하면 지름도 ×1.5 (표가 실제로 쓰인다)',
        abs(_moved / _base_s - 1.5) < 1e-9)
    #  ── 고-Bo 확장 LH (2026-09-27) ────────────────────────────────────────────
    chk('㊼ LH 의 AM_P Bo_code 38.4 가 지름·CGF 를 흔들어도 안 밀리고 겹침 천장 안이다',
        all(abs(_bo_amp('LH', plan(8000, cgf=_c)['d']) - 38.4) < 1e-9 for _c in (100.0, 151.4, 200.0))
        and all(overlap_for_ced(ced_matrix('LH', _p8['d'])[_i][_i], _p8['d'][_t] / 2.0, PHASE_MECH[_t][0],
                                E=E_PHASE[_t]) <= OVL_CEILING for _i, _t in enumerate(TYPES)))
    _MH, _MC = ced_matrix('LH', _p8['d']), ced_matrix('LC', _p8['d'])
    _nm = list(TYPES) + ['WALL']
    _chg = {tuple(sorted((_nm[i], _nm[j]))) for i in range(len(_nm)) for j in range(len(_nm))
            if abs(_MH[i][j] - _MC[i][j]) > 1e-9 * max(abs(_MC[i][j]), 1.0)}
    _allowB = {('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', 'WALL'), ('AM_S', 'WALL')}
    chk(f'㊼b ★ LH 와 LC 의 CED 행렬은 허용 다섯 쌍 (AM–AM 셋 · AM–벽 둘) 에서만 다르고 다섯 다 다르다 ({sorted(_chg)})',
        _chg == _allowB)
    _lc = deck(_p8, rpm=60, revolutions=2, seed=32452843, arm='LC').split('\n')
    _lh = deck(_p8, rpm=60, revolutions=2, seed=32452843, arm='LH').split('\n')
    _mc0 = next(i for i, l in enumerate(_lc) if l.startswith('fix mC '))
    _diff = [i for i, (x, y) in enumerate(zip(_lc, _lh)) if x != y]
    chk(f'㊼c LH 덱 = LC 덱 (줄 수 같음) · 다른 줄은 팔 설명 주석과 CED 행렬 줄뿐 ({len(_diff)} 줄)',
        len(_lc) == len(_lh) and all(_lc[i].startswith('# ★ 스윕 축') or _mc0 < i <= _mc0 + len(_nm) for i in _diff))
    chk('㊼d 확장 목록 = LH × 캠페인 시드 3 (본 캠페인 10 런과 분리)',
        CAMPAIGN_HIGHBO == [('LH', _s) for _s in CAMPAIGN_SEEDS] and ARMS['LH'].get('layered')
        and not any(_a == 'LH' for _a, _ in CAMPAIGN))

    #  ══ ST — 강성 축: SE 만 경화 + 쌍별 F₀ 보존 (2026-09-30 · 사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §3 ·
    #     Codex 6 차 HBR6-02 · 7 차 §5 · 9 차 §3/§6) ════════════════════════════════════════════════════════════════════════
    #  ★ 반례를 먼저 옮겼다 — 옛 생성기에는 쌍별 경로가 없어 ST⑤ (결함 재현) 를 뺀 전부가 FAIL 이었다.
    #    ST⑤ 가 결함 자체다: 동일상 `CED ∝ E^(2/3)` (SE 영률만 올리고 ced_matrix 를 다시 부르기) 는 min 조립 때문에 혼합쌍이 SE 의
    #    CED 배수를 그대로 받아 F₀ ×1.272 · SE–벽은 대각 ÷ 1.842 로 다시 만들어져 ×1.182 가 된다.
    import hashlib as _hs
    import json as _js
    import subprocess as _sp
    import tempfile as _tf

    def _ok(fn):
        try:
            return bool(fn())
        except (Exception, SystemExit):
            return False

    def _exit_msg(fn):
        """fn() 이 SystemExit 로 거부하면 그 문구, 아니면 None (다른 예외는 거부가 아니다 → None)."""
        try:
            fn()
        except SystemExit as e:
            return str(e)
        except Exception:
            return None
        return None

    _NM = list(TYPES) + [WALL]
    _IX = {t: k for k, t in enumerate(_NM)}
    _P9 = [('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', 'SE'), ('AM_S', 'SE'), ('SE', 'SE'),
           ('AM_P', WALL), ('AM_S', WALL), ('SE', WALL)]
    _Esoft = dict(E_PHASE)

    def _f0x(ced, ti, tj, dd_, E_):
        """★ 독립 산술 (생성기의 쌍 함수를 부르지 않는다) → (F₀, E*).  F₀ = (9/2)π³R*²CED³/E*² · 벽 R* = r_입자 · 선언된 벽 E · ν."""
        _nu = lambda t: WALL_NU if t == WALL else PHASE_MECH[t][0]
        es = 1.0 / ((1.0 - _nu(ti) ** 2) / E_[ti] + (1.0 - _nu(tj) ** 2) / E_[tj])
        ri = dd_[ti] / 2.0
        rs = ri if tj == WALL else ri * (dd_[tj] / 2.0) / (ri + dd_[tj] / 2.0)
        return 4.5 * math.pi ** 3 * rs ** 2 * ced ** 3 / es ** 2, es

    _pc = plan(100000, cgf=151.4)                       # 캠페인 조건 (gen_all.sh 기본 N_TOTAL · CGF)
    _rpmc = resolve_rpm(_pc['R'])
    _ints = lambda pat, t: [int(x) for x in _re.findall(pat, t, _re.M)]
    _one = lambda pat, t: _re.search(pat, t, _re.M).group(1)

    #  ST① 기본값 비트 동일 — 새 옵션을 안 주거나 중립값 (stiffen 1 · dt_factor 1 · hold 끔/켬) 이면 덱이 지금과 같다
    chk('ST① ★ 새 옵션 중립값 (stiffen_se 1 · hold_bo_pairwise 끔/켬 · dt_factor 1) 이면 덱이 기존과 바이트 동일 '
        '(골든 팔 일곱 × plan(8000)·2 바퀴 · 캠페인 plan·8 바퀴 · E0 0 바퀴)',
        _ok(lambda: all(deck(_pp, _rr, _rv, seed=32452843, arm=_a)
                        == deck(plan(_nn, cgf=_cg, stiffen_se=1.0), _rr, _rv, seed=32452843, arm=_a,
                                hold_bo_pairwise=_h, dt_factor=1.0)
                        for (_pp, _nn, _cg, _rr, _rv) in ((_p8, 8000, 200.0, 60, 2), (_pc, 100000, 151.4, _rpmc, 8),
                                                          (_pc, 100000, 151.4, _rpmc, 0))
                        for _a in _gold for _h in (False, True))))

    def _pair_ratios(arm, F):
        pn = plan(100000, cgf=151.4, stiffen_se=F)
        Ms = ced_matrix(arm, pn['d'])
        Mn = hold_bo_pairwise_matrix(Ms, _Esoft, pn['E'])
        rr = {(ti, tj): _f0x(Mn[_IX[ti]][_IX[tj]], ti, tj, pn['d'], pn['E'])[0]
              / _f0x(Ms[_IX[ti]][_IX[tj]], ti, tj, pn['d'], _Esoft)[0] for ti, tj in _P9}
        return rr, Ms, Mn
    _st2 = {(_a, _F): _ok(lambda: len(_pair_ratios(_a, _F)[0]) == 9
                          and all(abs(v - 1.0) <= 1e-12 for v in _pair_ratios(_a, _F)[0].values()))
            for _a in ('LC', 'LH', 'LA', 'E1') for _F in (14.0, 28.0)}
    chk(f'ST② ★ SE ×14 · ×28 에서 9 개 독립 비영 항목 (AM–AM 셋 · AM–SE 둘 · SE–SE · AM–벽 둘 · SE–벽) 의 F₀ 비 = 1 '
        f'(상대 1e-12 · 독립 산술 · LC · LH · LA · E1) — 실패 {[k for k, v in _st2.items() if not v]}',
        all(_st2.values()))
    chk('ST③ 쌍별 행렬: 정확히 대칭 · 벽–벽 = 0 · E0 는 ×14 · ×28 에서도 전 원소 0 (0 은 정확히 0 — 0/0 비 없음)',
        _ok(lambda: all(all(_M[i][j] == _M[j][i] for i in range(len(_NM)) for j in range(len(_NM)))
                        and _M[_IX[WALL]][_IX[WALL]] == 0.0
                        for _a in ('LC', 'LH') for _F in (14.0, 28.0) for _M in (_pair_ratios(_a, _F)[2],))
            and all(v == 0.0 for _F in (14.0, 28.0)
                    for row in hold_bo_pairwise_matrix(ced_matrix('E0', _pc['d']), _Esoft,
                                                       plan(100000, cgf=151.4, stiffen_se=_F)['E'])
                    for v in row)))
    #  ST④ Codex 7 차 §5 독립 산술 대조 (E* 배수 · 필요한 CED 배수) — AM–AM · AM–벽 은 E* 불변 ⇒ CED 정확히 불변
    _CODEX = {14.0: {'AM–SE': (12.412672571, 5.360971926), 'SE–SE': (14.0, 5.808785734), 'SE–벽': (12.876543210, 5.493715853)},
              28.0: {'AM–SE': (22.123962626, 7.880890212), 'SE–SE': (28.0, 9.220872584), 'SE–벽': (23.704545455, 8.251908834)}}
    _FAM = {'AM–SE': [('AM_P', 'SE'), ('AM_S', 'SE')], 'SE–SE': [('SE', 'SE')], 'SE–벽': [('SE', WALL)]}

    def _codex_ok(F):
        pn = plan(100000, cgf=151.4, stiffen_se=F)
        Ms = ced_matrix('LC', pn['d'])
        Mn = hold_bo_pairwise_matrix(Ms, _Esoft, pn['E'])
        good = True
        for fam, (e_mult, c_mult) in _CODEX[F].items():
            for ti, tj in _FAM[fam]:
                i, j = _IX[ti], _IX[tj]
                es_s, es_n = _f0x(1.0, ti, tj, pn['d'], _Esoft)[1], _f0x(1.0, ti, tj, pn['d'], pn['E'])[1]
                good &= abs(es_n / es_s / e_mult - 1.0) < 1e-9 and abs(Mn[i][j] / Ms[i][j] / c_mult - 1.0) < 1e-9
        for ti, tj in (('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', WALL), ('AM_S', WALL)):
            good &= Mn[_IX[ti]][_IX[tj]] == Ms[_IX[ti]][_IX[tj]]
        return good
    chk('ST④ ★ Codex 7 차 §5 독립 산술과 일치 — ×14: E* 배수 AM–SE 12.412672571 · SE–SE 14 · SE–벽 12.876543210 → CED 배수 '
        '5.360971926 · 5.808785734 · 5.493715853 · ×28: 22.12 · 28 · 23.70 → 7.881 · 9.221 · 8.252 (상대 1e-9) · AM–AM · AM–벽 CED 정확히 불변',
        _ok(lambda: _codex_ok(14.0) and _codex_ok(28.0)))

    def _old_rule(F):
        """옛 동일상 규칙 — SE 영률만 ×F 로 바꾸고 ced_matrix 를 다시 부른다 (현 생성기 함수만 쓴다 = 옛 코드에서도 돈다)."""
        saved = E_PHASE['SE']
        En = dict(E_PHASE)
        En['SE'] = saved * F
        try:
            E_PHASE['SE'] = saved * F
            Mo = ced_matrix('LC', _pc['d'])
        finally:
            E_PHASE['SE'] = saved
        Ms = ced_matrix('LC', _pc['d'])
        rr = {(ti, tj): _f0x(Mo[_IX[ti]][_IX[tj]], ti, tj, _pc['d'], En)[0]
              / _f0x(Ms[_IX[ti]][_IX[tj]], ti, tj, _pc['d'], _Esoft)[0] for ti, tj in _P9}
        return rr, Ms, Mo
    _or, _Ms14, _Mo14 = _old_rule(14.0)
    chk(f"ST⑤ 반례 (결함 재현 · HBR6-02): 옛 동일상 규칙 (SE 영률만 ×14 → ced_matrix 재호출) 은 혼합쌍 F₀ "
        f"×{_or[('AM_P', 'SE')]:.9f} · SE–벽 ×{_or[('SE', WALL)]:.9f} (Codex 1.272112360 · 1.182108914) · SE–SE ×1 · "
        f"SE CED {_Ms14[2][2]:.6f} → {_Mo14[2][2]:.6f} · SE–벽 {_Ms14[2][3]:.6f} → {_Mo14[2][3]:.6f} (Codex 핀)",
        abs(_or[('AM_P', 'SE')] - 1.272112360) < 1e-8 and abs(_or[('AM_S', 'SE')] - 1.272112360) < 1e-8
        and abs(_or[('SE', WALL)] - 1.182108914) < 1e-8 and abs(_or[('SE', 'SE')] - 1.0) < 1e-12
        and all(abs(_or[k] - 1.0) < 1e-12 for k in _P9 if 'SE' not in k)
        and abs(_Ms14[2][2] - 10458.232424) < 5e-6 and abs(_Mo14[2][2] - 60749.631302) < 5e-6
        and abs(_Ms14[2][3] - 5677.602066) < 5e-6 and abs(_Mo14[2][3] - 32979.973881) < 5e-6)

    def _st6():
        p14, p28 = plan(100000, cgf=151.4, stiffen_se=14.0), plan(100000, cgf=151.4, stiffen_se=28.0)
        d14 = deck(p14, _rpmc, 8, seed=32452843, arm='LC', hold_bo_pairwise=True)
        d0 = deck(_pc, _rpmc, 8, seed=32452843, arm='LC')
        e_line = lambda t: _one(r'^fix m1 all property/global youngsModulus peratomtype (.+)$', t).split()
        nu_line = lambda t: _one(r'^fix m2 all property/global poissonsRatio peratomtype (.+)$', t)
        e0_, e14 = e_line(d0), e_line(d14)
        run0, run14 = _ints(r'^run (\d+)$', d0)[-1], _ints(r'^run (\d+)$', d14)[-1]
        return (e14 == [e0_[0], e0_[1], '1.4e+08', e0_[3]] and e0_[2] == '1e+07' and nu_line(d0) == nu_line(d14)
                and abs(_pc['dt'] * 1e6 - 0.7055) < 5e-5 and abs(p14['dt'] * 1e6 - 0.3132) < 5e-5
                and abs(_pc['dt'] / p14['dt'] - 2.2525) < 5e-5 and abs(run14 / run0 - _pc['dt'] / p14['dt']) < 1e-6
                and p14['dt_by'] == 'SE' and _pc['dt_by'] == 'AM_S' and abs(_pc['dt'] / p28['dt'] - 3.1855) < 5e-5
                and _one(r'^timestep\s+(\S+)$', d14) == '3.132e-07')
    chk('ST⑥ SE 영률만 ×14 (AM · 벽 · ν 불변) · dt = 생성기 Rayleigh 최소를 새 E 로 다시 — 0.7055 µs (soft · AM_S 가 정함) → '
        '0.3132 µs (SE) · step ×2.2525 (Codex §5-1 산술) · ×28 → ×3.1855', _ok(_st6))
    _m7a = _exit_msg(lambda: deck(plan(8000, stiffen_se=14.0), 60, 2, seed=32452843, arm='LC'))
    _m7b = _exit_msg(lambda: deck(plan(8000, stiffen_se=14.0), 60, 0, seed=32452843, arm='E0'))
    chk(f'ST⑦ ★ --stiffen-se 를 --hold-bo-pairwise 없이: 점착 있는 팔 (LC) 은 **거부** · E0 (전 점착 0) 은 허용하고 머리에 기록 '
        f'({(_m7a or "")[:40]!r})',
        _m7a is not None and '--hold-bo-pairwise' in _m7a and _m7b is None
        and _ok(lambda: 'hold_bo_pairwise no' in deck(plan(8000, stiffen_se=14.0), 60, 0, seed=32452843, arm='E0')))
    _m8 = _exit_msg(lambda: plan(8000, stiffen_se=15.857))
    chk('ST⑧ ★ SE 영률이 덱 인쇄 정밀도 (4 유효숫자) 에 정확히 안 들어가는 배수 (15.857) 는 거부 — 쓰인 E ≠ 역산에 쓴 E 가 되지 않게 '
        '· 0 · 음수 · NaN 도 거부',
        _m8 is not None and '4 유효숫자' in _m8
        and all(_exit_msg(lambda: plan(8000, stiffen_se=_x)) is not None for _x in (0.0, -14.0, float('nan'), float('inf'))))

    def _st9():
        pr = plan(100000, cgf=151.4, stiffen_se=14.0)
        good = True
        for arm, rv in (('E0', 0), ('LC', 2), ('LH', 8)):
            ref = deck(pr, _rpmc, rv, seed=32452843, arm=arm, hold_bo_pairwise=True)
            half = deck(pr, _rpmc, rv, seed=32452843, arm=arm, hold_bo_pairwise=True, dt_factor=0.5)
            rr, rh = _ints(r'^run (\d+)$', ref), _ints(r'^run (\d+)$', half)
            dr, dh = int(_one(r'^dump dmp all custom (\d+) ', ref)), int(_one(r'^dump dmp all custom (\d+) ', half))
            tr, th = _one(r'^timestep\s+(\S+)$', ref), _one(r'^timestep\s+(\S+)$', half)
            t0r, t0h = (2 * rr[1] // dr) * dr, (2 * rh[1] // dh) * dh
            rsh = int(_one(r'^restart (\d+) ', half))
            strip = lambda t: [l for l in t.split('\n') if l.strip() and not l.lstrip().startswith('#')
                               and not _re.match(r'^(run|timestep|dump|restart) ', l)]
            good &= (rh[0] == rr[0] == 1 and rh[1:] == [2 * x for x in rr[1:]] and dh == 2 * dr
                     and float(th) * 2.0 == float(tr) and t0h == 2 * t0r and t0h * float(th) == t0r * float(tr)
                     and rsh == max(50_000, min(200_000, (rh[-1] or 2 * rh[1]) // 20))
                     and strip(ref) == strip(half)
                     and (float(_one(r'period (\S+)', half)) / float(th)) == 2.0 * (float(_one(r'period (\S+)', ref)) / float(tr)))
        return good and all(_exit_msg(lambda: deck(pr, _rpmc, 0, seed=32452843, arm='E0', hold_bo_pairwise=True,
                                                   dt_factor=_x)) is not None for _x in (0.3, 2.0, 0.0, -0.5, float('nan')))
    chk('ST⑨ ★ --dt-factor 0.5: dt 만 정확히 ½ (인쇄된 ref dt 의 절반) · 정착 · 회전 · 덤프 간격 step ×2 (run 1 삽입 step 은 그대로) · '
        '계획 t₀ step ×2 = 같은 물리 시각 · 바퀴당 step ×2 · E · ν · CED · 나머지 명령 동일 · restart = 생성기 규칙 · '
        '1/X 가 정수 아닌 값 (0.3 · 2 · 0 · 음수 · NaN) 거부', _ok(_st9))

    def _st10():
        good = True
        for F in (14.0, 28.0):
            pn = plan(100000, cgf=151.4, stiffen_se=F)
            settle = settle_time(2.0 * pn['R'], 0.3)
            for arm, rv in (('E0', 0), ('LC', 2), ('LH', 8)):
                t = deck(pn, _rpmc, rv, seed=32452843, arm=arm, hold_bo_pairwise=True)
                rr = _ints(r'^run (\d+)$', t)
                de = int(_one(r'^dump dmp all custom (\d+) ', t))
                good &= (abs(2 * rr[1] * pn['dt'] - settle) <= pn['dt'] * (1 + 1e-9)
                         and abs(rr[-1] * pn['dt'] - rv * 60.0 / _rpmc) <= 0.5 * pn['dt'] * (1 + 1e-9)
                         and de == max(1000, rr[-1] // 200))
        return good
    chk('ST⑩ 경화 덱의 물리 시간 불변 (정착 2F·dt = 유도 정착시간 ± 1 step · 회전 = 바퀴 × 주기 ± ½ step) · 덤프 간격 = 생성기 규칙 '
        '(max(1000, 회전 step // 200)) — ×14 · ×28 × E0 · LC 2 바퀴 · LH 8 바퀴', _ok(_st10))

    def _st11():
        dflt = deck(_pc, _rpmc, 2, seed=32452843, arm='LC')
        st = deck(plan(100000, cgf=151.4, stiffen_se=14.0), _rpmc, 2, seed=32452843, arm='LC', hold_bo_pairwise=True)
        hd = [l for l in st.split('\n') if l.startswith('#   F0 ') or l.startswith('#   F₀ ')]
        rows = [l for l in st.split('\n') if _re.match(r'^#   (AM_P|AM_S|SE|WALL)–(AM_P|AM_S|SE|WALL) ', l)]
        return ('# ★ 강성 축' not in dflt and '# ★ 강성 축' in st and 'stiffen_se 14' in st and 'hold_bo_pairwise yes' in st
                and 'dt_factor 1' in st and len(rows) == 10 and st.count('\n') > dflt.count('\n'))
    chk('ST⑪ 경화 덱 머리에 stiffen_se · hold_bo_pairwise · dt_factor · 쌍별 E* · CED · F₀ 표 (9 비영 + 벽–벽) — 기본 덱에는 없다', _ok(_st11))

    def _st12():
        me = os.path.abspath(__file__)
        base = ['--n-total', '100000', '--cgf', '151.4', '--arm', 'LC', '--seed', '32452843', '--revolutions', '2']
        with _tf.TemporaryDirectory() as td:
            a = _sp.run([sys.executable, me, '--out', os.path.join(td, 'a')] + base + ['--stiffen-se', '14', '--hold-bo-pairwise'],
                        capture_output=True, text=True)
            b = _sp.run([sys.executable, me, '--out', os.path.join(td, 'b')] + base + ['--stiffen-se', '14'],
                        capture_output=True, text=True)
            c = _sp.run([sys.executable, me, '--out', os.path.join(td, 'c')] + base, capture_output=True, text=True)
            dk_a = open(os.path.join(td, 'a', 'in.mixer'), encoding='utf-8').read()
            meta = _js.load(open(os.path.join(td, 'a', 'deck_meta.json'), encoding='utf-8'))
            gen_sha = _hs.sha256(open(me, 'rb').read()).hexdigest()
            rows = {r_['pair']: r_ for r_ in meta['pairs']}
            return (a.returncode == 0 and dk_a == deck(plan(100000, cgf=151.4, stiffen_se=14.0), _rpmc, 2, seed=32452843,
                                                       arm='LC', hold_bo_pairwise=True)
                    and meta['deck_sha256'] == _hs.sha256(dk_a.encode('utf-8')).hexdigest()
                    and meta['generator_sha256'] == gen_sha and meta['stiffen_se'] == 14.0 and meta['hold_bo_pairwise'] is True
                    and meta['dt_factor'] == 1.0 and '--stiffen-se' in meta['argv'] and len(rows) == 10
                    and all(abs(r_['F0_ratio'] - 1.0) <= 1e-12 for k, r_ in rows.items() if k != 'WALL–WALL')
                    and rows['WALL–WALL']['CED'] == 0.0
                    and b.returncode != 0 and '--hold-bo-pairwise' in (b.stderr + b.stdout)
                    and not os.path.exists(os.path.join(td, 'b', 'in.mixer'))
                    and c.returncode == 0 and not os.path.exists(os.path.join(td, 'c', 'deck_meta.json'))
                    and open(os.path.join(td, 'c', 'in.mixer'), encoding='utf-8').read()
                    == deck(_pc, _rpmc, 2, seed=32452843, arm='LC'))
    chk('ST⑫ CLI: --stiffen-se 14 --hold-bo-pairwise → in.mixer = deck() + 봉인 가능한 deck_meta.json (덱 sha256 · 생성기 sha256 · argv · '
        '쌍별 표 F₀ 비 1) · hold 없이 LC 는 rc≠0 이고 덱을 안 쓴다 · 기본 CLI 는 meta 를 안 쓰고 덱이 그대로', _ok(_st12))

    def _st13():
        allowB = {('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', WALL), ('AM_S', WALL)}
        good = True
        for F in (14.0, 28.0):
            pn = plan(100000, cgf=151.4, stiffen_se=F)
            MC = hold_bo_pairwise_matrix(ced_matrix('LC', pn['d']), _Esoft, pn['E'])
            MH = hold_bo_pairwise_matrix(ced_matrix('LH', pn['d']), _Esoft, pn['E'])
            chg = {tuple(sorted((_NM[i], _NM[j]))) for i in range(len(_NM)) for j in range(len(_NM)) if MH[i][j] != MC[i][j]}
            good &= chg == allowB and all(MH[_IX[a]][_IX[b]] > MC[_IX[a]][_IX[b]] for a, b in allowB)
        return good
    chk('ST⑬ ★ 경화해도 LC↔LH 공동 개입 B 는 그대로 — ×14 · ×28 에서 달라지는 쌍 = 허용 다섯 (AM–AM 셋 · AM–벽 둘) 이고 다섯 다 LH > LC '
        '· SE 낀 쌍은 LC = LH (정확히)', _ok(_st13))

    def _st14():
        """★ 주석 = 실측 (2026-09-30 · 강성 축 코드 선행조건 2 단계 piece 6).  옛 주석 둘은 'dt 를 정하는 상 = SE' 라 적었는데 캠페인 soft 에서는
        **AM_S** 가 정한다 (plan()['dt_by'] · Codex 7 차 §5-1 의 ×2.2525 가 그래서 √14 가 아니다).  ① 주석 줄 (소스에서 `#` 로 시작) 에 그 두 문장이
        남아 있으면 FAIL ② 고친 주석의 숫자 (AM_S · SE Rayleigh dt · A안 전 대비 step 배수) 를 **독립 산술**로 다시 내 인쇄 자릿수까지 대조."""
        src = open(os.path.abspath(__file__), encoding='utf-8').read().split('\n')
        com = [l_ for l_ in src if l_.lstrip().startswith('#')]
        stale = ('dt 는 가장 작은 SE 가 정하므로', '가장 작고 무른 SE 가 정한다')
        if any(s_ in l_ for s_ in stale for l_ in com):
            return False
        pc = plan(100000, cgf=151.4)

        def ray(t, E):                                   # 독립 산술 — Rayleigh 20 % (plan 과 같은 식을 여기서 다시 적는다)
            nu, mat = PHASE_MECH[t]
            G = E / (2.0 * (1.0 + nu))
            return 0.2 * math.pi * (pc['d'][t] / 2) * math.sqrt(DENS[mat] * 1000.0 / G) / (0.1631 * nu + 0.8766)
        now = {t: ray(t, E_PHASE[t]) for t in TYPES}
        pre = {t: ray(t, 1.0e7) for t in TYPES}          # A안 전 = 전 상 1e7 (옛 판)
        by_now, by_pre = min(now, key=now.get), min(pre, key=pre.get)
        want = (f'AM_S {now["AM_S"] * 1e6:.4f} µs', f'SE {now["SE"] * 1e6:.4f} µs', f'×{min(pre.values()) / min(now.values()):.3f}')
        hit = [l_ for l_ in com if all(w_ in l_ for w_ in want)]
        return (by_now == 'AM_S' == pc['dt_by'] and by_pre == 'SE' and abs(pc['dt'] - now['AM_S']) < 1e-18
                and len(hit) >= 1 and plan(100000, cgf=151.4, stiffen_se=14.0)['dt_by'] == 'SE')
    chk('ST⑭ ★ 주석 = 실측 — "dt 를 SE 가 정한다" 옛 주석 둘이 없고, 고친 주석의 숫자 (soft 캠페인 AM_S 0.7055 µs < SE 1.1719 µs · '
        'A안 전 (전 상 1e7 · SE 가 정함) 대비 step ×1.661) 를 독립 산술로 다시 낸 값과 인쇄 자릿수까지 같다 · ×14 는 SE 가 정한다', _ok(_st14))

    #  ══ BO — 개발 탐색 dev-bo (2026-10-02 · 강성 축 사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §11 · v2.8) ══════════
    #  ★ 반례를 먼저 옮겼다 — 옛 생성기에는 LHx10 · LHx30 팔이 없다 (KeyError → BO① ~ BO⑥ 전부 FAIL).
    #    LH 와 **같은 규약** (abs_base 0.212 + AM 쌍 abs_mult) 에 AM–AM Bo_code 만 ×10 · ×30 — 공동 개입 B (AM–AM + AM–벽) 그대로 · 확인 팔 아님.
    _BOX = {'LHx10': 10.0, 'LHx30': 30.0}

    def _bo_t(arm, dd_, t):
        i_ = TYPES.index(t)
        nu_, mat_ = PHASE_MECH[t]
        return bond_for_ced(ced_matrix(arm, dd_)[i_][i_], dd_[t] / 2.0, nu_, DENS[mat_], E=E_PHASE[t])

    def _bo1():
        lh = ARMS['LH']['abs_mult'][('AM_P', 'AM_P')]
        return (lh == 38.4
                and all(ARMS[a_]['abs_mult'] == _am_pairs(lh * k_) and ARMS[a_]['abs_base'] == BO_BASE and ARMS[a_]['bond'] == 1.0
                        for a_, k_ in _BOX.items())
                and all(abs(_bo_t(a_, plan(8000, cgf=c_)['d'], t_) / (lh * k_) - 1.0) < 1e-12
                        for a_, k_ in _BOX.items() for c_ in (100.0, 151.4, 200.0) for t_ in ('AM_P', 'AM_S')))
    chk('BO① ★ LHx10 · LHx30 = LH 의 AM–AM Bo_code 38.4 × 10 · × 30 = 384 · 1152 (abs_base · bond 같은 규약) — AM_P–AM_P · AM_S–AM_S Bo 가 '
        'CGF 100 · 151.4 · 200 에서 안 밀린다 (상대 1e-12)', _ok(_bo1))

    def _bo2():
        dd_ = _pc['d']
        MC, MH, M10, M30 = (ced_matrix(a_, dd_) for a_ in ('LC', 'LH', 'LHx10', 'LHx30'))
        allowB = {('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', WALL), ('AM_S', WALL)}

        def chg(A, B):
            return {tuple(sorted((_NM[i], _NM[j]))) for i in range(len(_NM)) for j in range(len(_NM)) if A[i][j] != B[i][j]}

        def up(A, B):
            return all(B[_IX[a]][_IX[b]] > A[_IX[a]][_IX[b]] for a, b in allowB)
        return chg(MH, M10) == chg(M10, M30) == chg(MC, M10) == chg(MC, M30) == allowB and up(MH, M10) and up(M10, M30) and up(MC, M10)
    chk('BO② ★ 공동 개입 B 그대로 — LH → LHx10 → LHx30 (그리고 LC → LHx10 · LHx30) 에서 달라지는 CED = 허용 다섯 (AM–AM 셋 · AM–벽 둘) 이고 '
        '다섯 다 증가 · SE 낀 쌍은 정확히 같다 (캠페인 CGF 151.4)', _ok(_bo2))

    def _bo3():
        p20 = plan(100000, cgf=151.4, stiffen_se=20.0)
        lh = deck(p20, _rpmc, 2, seed=32452843, arm='LH', hold_bo_pairwise=True).split('\n')
        mc0 = next(i for i, l in enumerate(lh) if l.startswith('fix mC '))
        ced_rows = set(range(mc0, mc0 + len(_NM) + 1))
        good = True
        for a_ in _BOX:
            x = deck(p20, _rpmc, 2, seed=32452843, arm=a_, hold_bo_pairwise=True).split('\n')
            diff = [i for i, (u, v) in enumerate(zip(lh, x)) if u != v]
            good &= (len(x) == len(lh) and bool(diff) and any(i in ced_rows for i in diff)
                     and all(i in ced_rows or (lh[i].lstrip().startswith('#') and x[i].lstrip().startswith('#')) for i in diff))
        return good
    chk('BO③ ★ 경화 덱 (×20 · hold · 2 바퀴 · seed 32452843) — LHx10 · LHx30 덱 = LH 덱과 줄 수 같고 주석 밖 차이는 CED 행렬 줄뿐 '
        '(timestep · run · 삽입 · 기구 · 시드 그대로 · dt 는 SE 가 정한다 ⇒ 비용 = LH_ref_r2)', _ok(_bo3))
    chk('BO④ dev-bo 팔은 캠페인 · 고-Bo · 기준 목록 밖 (개발 탐색 전용 — 확인 팔 아님) · 층상 · 설명에 "dev-bo" · "확인 팔 아님" 표지',
        _ok(lambda: all(all(x_ != a_ for x_, _ in CAMPAIGN + CAMPAIGN_HIGHBO) and all(x_ != a_ for x_, _, _ in REFERENCE)
                        and ARMS[a_].get('layered') is True and 'dev-bo' in ARMS[a_]['desc'] and '확인 팔 아님' in ARMS[a_]['desc']
                        for a_ in _BOX)))

    def _bo5():
        dd_ = _pc['d']
        want = {'LH': (0.046, 0.027), 'LHx10': (0.214, 0.125), 'LHx30': (0.445, 0.259)}
        got = {a_: tuple(round(overlap_for_ced(ced_matrix(a_, dd_)[TYPES.index(t_)][TYPES.index(t_)], dd_[t_] / 2.0, PHASE_MECH[t_][0],
                                               E=E_PHASE[t_]) * 100, 3) for t_ in ('AM_P', 'AM_S')) for a_ in want}
        if got != want:
            print(f'        정적 겹침 % {got}')
        return got == want and max(max(v) for v in got.values()) < OVL_CEILING * 100
    chk('BO⑤ ★ 등록 문서 수치 = 실측 (사전등록 §11) — 정적 평형 겹침 δ/r (CGF 151.4 · 점착 지배 · 고립 접촉 근사): AM_P 0.046 · 0.214 · 0.445 % · '
        'AM_S 0.027 · 0.125 · 0.259 % (LH · ×10 · ×30) · 천장 1 % 안 — 충돌 최대 겹침의 상한이 아니다', _ok(_bo5))

    def _bo6():
        good = True
        for a_ in _BOX:
            rr, Ms, Mn = _pair_ratios(a_, 20.0)
            good &= (all(abs(v - 1.0) <= 1e-12 for v in rr.values())
                     and all(Mn[_IX[x_]][_IX[y_]] == Ms[_IX[x_]][_IX[y_]]
                             for x_, y_ in (('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', WALL), ('AM_S', WALL))))
        return good
    chk('BO⑥ SE ×20 경화 (--hold-bo-pairwise) 에서도 9 비영 항 F₀ 비 = 1 (상대 1e-12) · AM–AM · AM–벽 CED 는 soft 값 그대로 (E* 불변) '
        '⇒ 덱의 AM–AM 점착 = 명목 Bo_code 정확히', _ok(_bo6))

    #  ══ U — 개발 탐색 dev-u (2026-10-05 · 강성 축 사전등록 docs/reviews/mixer_highbo_stiffness_prereg_20260929.md §12 · v2.9) ══════════
    #  ★ 반례를 먼저 옮겼다 — 옛 생성기에는 LU212 · LU637 팔이 없다 (KeyError · NameError → U① ~ U⑦ 전부 FAIL).
    #    LC 와 **같은 규약** (abs_base 0.212 + coat AM→SE) 에 SE 낀 세 쌍 (SE–SE · AM_P–SE · AM_S–SE) 의 Bo 만 ×1000 · ×3000 — 코팅 상 (AM) 의
    #    목표 Bo 는 SE–SE Bo 를 JKR 기하로 따라가고 벽은 대각 ÷ 1.842 ⇒ CED 9 비영 원소 전부 같은 배율 = **균일 γ 배율** (SE 만의 개입 아님 · 확인 팔 아님).
    _UK = {'LU212': 1000.0, 'LU637': 3000.0}

    def _u1():
        good = all(ARMS[a_]['abs_mult'] == _se_pairs(k_ * BO_BASE) and ARMS[a_]['abs_base'] == BO_BASE == ARMS['LC']['abs_base']
                   and ARMS[a_]['bond'] == ARMS['LC']['bond'] == 1.0 and ARMS[a_].get('layered') is True
                   and ARMS[a_].get('coat') == ARMS['LC']['coat'] == {'AM_P': 'SE', 'AM_S': 'SE'}
                   and set(ARMS[a_]) == set(ARMS['LC']) | {'abs_mult'} for a_, k_ in _UK.items())
        for a_, k_ in _UK.items():
            for c_ in ((100.0, 151.4, 200.0) if a_ not in _CGF_BOUND else (100.0, 151.4)):
                dd_ = plan(8000, cgf=c_)['d']
                good &= all(abs(_bo_t(a_, dd_, t_) / (k_ * _bo_t('LC', dd_, t_)) - 1.0) < 1e-12 for t_ in TYPES)
        return good and abs(_bo_t('LU212', _pc['d'], 'SE') - 212.44) < 1e-9 and abs(_bo_t('LU637', _pc['d'], 'SE') - 637.32) < 1e-9
    chk('U① ★ LU212 · LU637 = LC 규약 그대로 (abs_base · bond · 층상 · coat AM→SE · 다른 키 없음) + abs_mult = SE 낀 세 쌍 × 1000 · 3000 × BO_BASE — '
        '동종 쌍 Bo_code (SE–SE 212.44 · 637.32 · 코팅 AM_P · AM_S 도) = LC × 1000 · × 3000 · CGF 100 · 151.4 (· 200 은 LU212 만) 에서 안 밀린다 (상대 1e-12)',
        _ok(_u1))

    def _u2():
        dd_ = _pc['d']
        p20 = plan(100000, cgf=151.4, stiffen_se=20.0)
        MC = ced_matrix('LC', dd_)
        good = True
        for a_, k_ in _UK.items():
            r_ = k_ ** (1.0 / 3.0)
            MU = ced_matrix(a_, dd_)
            for Ma, Mb in ((MC, MU), (hold_bo_pairwise_matrix(MC, _Esoft, p20['E']), hold_bo_pairwise_matrix(MU, _Esoft, p20['E']))):
                for i in range(len(_NM)):
                    for j in range(len(_NM)):
                        if Ma[i][j] == 0.0:
                            good &= Mb[i][j] == 0.0 and _NM[i] == _NM[j] == WALL
                        else:
                            good &= abs(Mb[i][j] / Ma[i][j] / r_ - 1.0) < 1e-12
        M2, M6 = ced_matrix('LU212', dd_), ced_matrix('LU637', dd_)
        return good and all(abs(M6[i][j] / M2[i][j] / 3.0 ** (1.0 / 3.0) - 1.0) < 1e-12
                            for i in range(len(_NM)) for j in range(len(_NM)) if M2[i][j])
    chk('U② ★ 균일 γ 배율 — LU212 · LU637 의 CED **9 비영 원소 전부** (AM–AM 셋 · AM–SE 둘 · SE–SE · AM–벽 둘 · SE–벽) = LC × 정확히 10 · 14.422496 '
        '(Bo 배수 1000 · 3000 의 세제곱근 · 상대 1e-12) — soft 와 SE ×20 경화 (--hold-bo-pairwise) 둘 다 · 벽–벽 0 그대로 · LU637 / LU212 = 3^(1/3) (CGF 151.4)',
        _ok(_u2))

    def _u3():
        p20 = plan(100000, cgf=151.4, stiffen_se=20.0)
        lc = deck(p20, _rpmc, 2, seed=32452843, arm='LC', hold_bo_pairwise=True).split('\n')
        mc0 = next(i for i, l in enumerate(lc) if l.startswith('fix mC '))
        rows = set(range(mc0 + 1, mc0 + len(_NM) + 1))                  # 행렬 값 줄 (머리 줄 `fix mC …` 은 그대로여야 한다)
        good = True
        for a_ in _UK:
            x = deck(p20, _rpmc, 2, seed=32452843, arm=a_, hold_bo_pairwise=True).split('\n')
            diff = [i for i, (u, v) in enumerate(zip(lc, x)) if u != v]
            good &= (len(x) == len(lc) and rows <= set(diff)
                     and all(i in rows or (lc[i].lstrip().startswith('#') and x[i].lstrip().startswith('#')) for i in diff))
        return good
    chk('U③ ★ 경화 덱 (×20 · hold · 2 바퀴 · seed 32452843) — LU212 · LU637 덱 = LC 덱과 줄 수 같고 주석 밖 차이는 CED 행렬 값 줄뿐 · 그 넷이 전부 바뀐다 '
        '(timestep · run · 삽입 · 기구 · 시드 그대로 · dt 는 SE 가 정한다 ⇒ 비용 = LC_ref_r2)', _ok(_u3))
    chk('U④ dev-u 팔은 캠페인 · 고-Bo · 기준 목록 밖 (개발 탐색 전용 — 확인 팔 아님) · 층상 · 설명에 "dev-u" · "균일 γ 배율" · "확인 팔 아님" 표지',
        _ok(lambda: all(all(x_ != a_ for x_, _ in CAMPAIGN + CAMPAIGN_HIGHBO) and all(x_ != a_ for x_, _, _ in REFERENCE)
                        and ARMS[a_].get('layered') is True and 'dev-u' in ARMS[a_]['desc'] and '균일 γ 배율' in ARMS[a_]['desc']
                        and '확인 팔 아님' in ARMS[a_]['desc'] for a_ in _UK)))

    def _u5():
        dd_ = _pc['d']
        p20 = plan(100000, cgf=151.4, stiffen_se=20.0)
        iS, nuS = _IX['SE'], PHASE_MECH['SE'][0]

        def _vst(ced, ti, tj, E_):
            """붙는 충돌 속도 상한 (mm/s) — 등록 §11-3 식 · 독립 산술: W = (1/5)π·CED·R*·δ_eq² (δ_eq = (B/A)² · A = (4/3)E*√R* · B = 2πR*·CED) ·
            KE = ½m*v² ≤ W(1−e²)/e² (e = COR) ⇒ v = √(2W(1−e²)/(e²m*))."""
            es = _f0x(1.0, ti, tj, dd_, E_)[1]
            ri, rj = dd_[ti] / 2.0, dd_[tj] / 2.0
            rs = ri * rj / (ri + rj)
            W = 0.2 * math.pi * ced * rs * (2.0 * math.pi * rs * ced / ((4.0 / 3.0) * es * math.sqrt(rs))) ** 4
            mi, mj = ((4.0 / 3.0) * math.pi * r_ ** 3 * DENS[PHASE_MECH[t_][1]] * 1000.0 for r_, t_ in ((ri, ti), (rj, tj)))
            return math.sqrt(2.0 * W * (1.0 - COR ** 2) / (COR ** 2 * mi * mj / (mi + mj))) * 1e3
        got, want = {}, {
            'ovl_SE': {'LU212': (0.402, 0.055), 'LU637': (0.837, 0.114)},                       # SE–SE δ/r % (soft · ref)
            'v_SE': {'LC': (0.16, 0.059), 'LU212': (50.7, 18.7), 'LU637': (126.6, 46.6)},       # SE–SE mm/s (soft · ref)
            'v_PP': {'LU212': 1.1, 'LU637': 2.8, 'LH': 21.9},                                   # AM_P–AM_P mm/s (SE 경화 무관)
            'v_PS': {'LU212': 8.6, 'LU637': 21.5}}                                              # AM_P–SE mm/s (ref)
        for k_ in want:
            got[k_] = {}
        for a_ in ('LC', 'LH') + tuple(_UK):
            Ms = ced_matrix(a_, dd_)
            Mr = hold_bo_pairwise_matrix(Ms, _Esoft, p20['E'])
            if a_ in want['ovl_SE']:
                got['ovl_SE'][a_] = (round(overlap_for_ced(Ms[iS][iS], dd_['SE'] / 2.0, nuS, E=_Esoft['SE']) * 100, 3),
                                     round(overlap_for_ced(Mr[iS][iS], dd_['SE'] / 2.0, nuS, E=p20['E']['SE']) * 100, 3))
            if a_ in want['v_SE']:
                nd = 3 if a_ == 'LC' else 1
                got['v_SE'][a_] = (round(_vst(Ms[iS][iS], 'SE', 'SE', _Esoft), nd), round(_vst(Mr[iS][iS], 'SE', 'SE', p20['E']), nd))
            if a_ in want['v_PP']:
                got['v_PP'][a_] = round(_vst(Mr[_IX['AM_P']][_IX['AM_P']], 'AM_P', 'AM_P', p20['E']), 1)
            if a_ in want['v_PS']:
                got['v_PS'][a_] = round(_vst(Mr[_IX['AM_P']][iS], 'AM_P', 'SE', p20['E']), 1)
        if got != want:
            print(f'        등록 수치 {got}')
        return got == want and max(max(v) for v in got['ovl_SE'].values()) < OVL_CEILING * 100
    chk('U⑤ ★ 등록 문서 수치 = 실측 (사전등록 §12-3) — SE–SE 정적 평형 겹침 δ/r: soft 0.402 · 0.837 % · ref ×20 0.055 · 0.114 % · 붙는 충돌 속도 상한 '
        '(§11-3 식 · e 0.3 · 덱 값): SE–SE soft 50.7 · 126.6 · ref 18.7 · 46.6 mm/s (LC 0.160 · 0.059) · AM_P–AM_P 1.1 · 2.8 (LH 21.9) · AM_P–SE ref 8.6 · 21.5 mm/s — '
        '효과 예측 아님 · 충돌 최대 겹침의 상한 아님', _ok(_u5))

    def _u6():
        try:
            ARMS['_u850'] = dict(ARMS['LU637'], abs_mult=_se_pairs(4000.0 * BO_BASE))      # X = 849.76 ≈ 850 (Bo ×4000)
            m850 = _exit_msg(lambda: ced_matrix('_u850', _pc['d']))
        finally:
            ARMS.pop('_u850', None)
        bound = all((_exit_msg(lambda: ced_matrix(a_, dd)) or '').startswith(f'⛔ 팔 {a_}: SE–SE 겹침')
                    and _exit_msg(lambda: ced_matrix(a_, _pc['d'])) is None for a_ in _CGF_BOUND)
        return (m850 is not None and 'SE–SE 겹침 1.014 %' in m850 and _CGF_BOUND == ('LU637',) and bound
                and 'SE–SE 겹침 1.007 %' in (_exit_msg(lambda: ced_matrix('LU637', dd)) or '')
                and _exit_msg(lambda: ced_matrix('LU212', dd)) is None)
    chk('U⑥ ★ 생성기 천장 그대로 — X = 850 (Bo ×4000) 은 캠페인 CGF 151.4 에서 SE–SE 1.014 % 로 거부 · LU637 (×3000) 은 151.4 에서 수용 · CGF 200 (㉙ 의 dd) '
        '에서 1.007 % 로 거부 = 선언 목록 _CGF_BOUND 정확히 · LU212 는 200 에서도 수용', _ok(_u6))

    def _u7():
        good = True
        for a_ in _UK:
            rr, Ms, Mn = _pair_ratios(a_, 20.0)
            good &= (len(rr) == 9 and all(abs(v - 1.0) <= 1e-12 for v in rr.values())
                     and all(Mn[_IX[x_]][_IX[y_]] == Ms[_IX[x_]][_IX[y_]]
                             for x_, y_ in (('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', WALL), ('AM_S', WALL))))
        return good
    chk('U⑦ SE ×20 경화 (--hold-bo-pairwise) 에서도 9 비영 항 F₀ 비 = 1 (상대 1e-12) · AM–AM · AM–벽 CED 는 soft 값 그대로 (E* 불변) '
        '⇒ 경화 덱에서도 9 원소가 LC 와 같은 배율 (U②)', _ok(_u7))

    #  ══ DP — 전 정밀도 덤프 (2026-10-05 · 강성 축 사전등록 §12-4 (다) · 1저자 *"가,다 하고 나도 해당 방법으로 진행해보자"*) ═══════════
    #  ★ 시험 먼저 — 옛 생성기에는 deck(dump_full_precision=…) · dump_modify_format 이 없다 (TypeError · NameError → DP① ~ DP⑥ FAIL).
    #    덱의 `dump dmp all custom …` 에 dump_modify format 이 없어 좌표가 LIGGGHTS 기본 %g (6 유효숫자) 로 찍힌다 — 보조 판독기 (s1 · s2) 의
    #    접촉 판정이 덤프 해상도에 갇힌다 (시험 운전 docs/data/mixer_contact_reader_refs_20261005/).  플래그를 켜면 그 dump 바로 뒤에
    #    `dump_modify dmp format "<열마다 하나>"` (id · type · mol = %d · 나머지 %.17g = double 왕복).  ⛔ 기본 끔 = 덱 바이트 그대로.
    _RUN_DECKS = {('LC', 2): '5405067f8360651b34cfdcdbb07e355132f6f9cdaa6053e70f62e2560c6924a2',    # v26 LC_ref_r2 (ibb dev-rot 실행 덱)
                  ('LH', 2): '3125d2443004300f274cc8b16fa218a7d509c4b9352c125cdfaec726807605fd',    # v26 LH_ref_r2
                  ('E0', 0): '78ad92356373e00ae8eeee666256e250571fad6acfba90c7d491ccc3d6954adb',   # v26 E0_ref_s32452843 (회전 0)
                  ('LU212', 2): '8cb48a132d8a90c03da706f04dd426508a0d48418df6ac1a127ed42b9eadca8c',  # dev-u (ibb 실행 중)
                  ('LU637', 2): '57872d5d4a1c716263b8b227dbdc68e48963caf1afbbe85406b66d02d42fa849'}
    _p20 = plan(100000, cgf=151.4, stiffen_se=20.0)
    _rp20 = resolve_rpm(_p20['R'], FR_ANCHOR, None, False)

    def _run_deck(arm, rv, **kw):
        """커밋 · 실행 덱과 같은 호출 (mixer_deck_diff.expected_deck = 생성기 CLI) — ×20 · hold · seed 32452843."""
        return deck(_p20, _rp20, rv, arm=arm, settle_s=None, seed=32452843, n_baffles=0, baffle_h=0.10,
                    hold_bo_pairwise=True, dt_factor=1.0, **kw)

    def _dp1():
        return all(_hs.sha256(_run_deck(a_, rv_).encode('utf-8')).hexdigest() == h_
                   and _run_deck(a_, rv_, dump_full_precision=False) == _run_deck(a_, rv_)
                   and 'dump_modify' not in _run_deck(a_, rv_) for (a_, rv_), h_ in _RUN_DECKS.items())
    chk('DP① ★ 기본 끔 (플래그 없음 · dump_full_precision=False) = 커밋 · 실행 덱과 바이트 동일 — v26 LC_ref_r2 · LH_ref_r2 · E0_ref · '
        'dev-u LU212 · LU637 (sha256 다섯) · dump_modify 줄 없음', _ok(_dp1))

    def _fmt_line(t):
        L = [l for l in t.split('\n') if l.startswith('dump_modify')]
        m_ = _re.fullmatch(r'dump_modify dmp format "([^"]*)"', L[0]) if len(L) == 1 else None
        return None if m_ is None else m_.group(1).split(' ')

    def _dp2():
        good = True
        for a_, rv_ in (('LC', 2), ('E0', 0), ('LU637', 2)):
            off, on = _run_deck(a_, rv_).split('\n'), _run_deck(a_, rv_, dump_full_precision=True).split('\n')
            i_ = next(k for k, l in enumerate(off) if l.startswith('dump dmp '))
            cols = off[i_].split()[6:]
            ins = on[i_ + 1:i_ + 1 + (len(on) - len(off))]
            toks = _fmt_line('\n'.join(on))
            good &= (on[:i_ + 1] == off[:i_ + 1] and on[i_ + 1 + len(ins):] == off[i_ + 1:] and len(ins) >= 1
                     and ins[-1].startswith('dump_modify dmp format ') and all(l.startswith('#') for l in ins[:-1])
                     and cols == ['id', 'type', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'fx', 'fy', 'fz', 'radius']
                     and toks is not None and len(toks) == len(cols) == 12
                     and toks == ['%d' if c_ in ('id', 'type') else '%.17g' for c_ in cols]
                     and ' '.join(toks) == dump_modify_format(cols))
        return good
    chk('DP② ★ 켜면 (LC · E0 · LU637) `dump dmp` 바로 뒤에 주석 + `dump_modify dmp format "…"` 한 줄만 더해진다 (나머지 줄 그대로) · '
        '형식 토큰 수 = dump 열 수 12 · id · type = %d · x y z vx vy vz fx fy fz radius = %.17g · dump_modify_format(열) 과 같다', _ok(_dp2))

    def _dp3():
        _saved = TYPES
        try:
            set_phases(ALL_TYPES)
            t_ = deck(plan(8000), rpm=60, revolutions=5, dump_full_precision=True)
        finally:
            set_phases(_saved)
        cols = next(l for l in t_.split('\n') if l.startswith('dump dmp ')).split()[6:]
        toks = _fmt_line(t_)
        return (cols[:3] == ['id', 'type', 'mol'] and toks is not None and len(toks) == len(cols) == 13
                and toks[:3] == ['%d'] * 3 and set(toks[3:]) == {'%.17g'})
    chk('DP③ 섬유 (5 상 · dump 에 mol 열) 이면 형식 13 토큰 · id · type · mol = %d (LIGGGHTS dump_custom INT 열) · 나머지 %.17g', _ok(_dp3))

    def _dp4():
        on = _run_deck('LC', 2, dump_full_precision=True)
        off = _run_deck('LC', 2)
        de_on = _re.findall(r'^dump\s+dmp\s+all\s+custom\s+(\d+)', on, _re.M)          # 판독기 deck_plan 의 정규식 그대로
        ins = [l for l in on.split('\n') if l not in off.split('\n')]
        return (de_on == _re.findall(r'^dump\s+dmp\s+all\s+custom\s+(\d+)', off, _re.M) and len(de_on) == 1
                and all(not l.rstrip().endswith('&') and '$' not in l for l in ins)
                and all('#' not in l and l.count('"') == 2 for l in ins if not l.startswith('#')))
    chk('DP④ 판독기 deck_plan 정규식 (`^dump\\s+dmp\\s+all\\s+custom`) 은 그대로 한 줄 · 같은 덤프 간격 — 더한 줄은 `&` 로 끝나지 않고 $ 없음 · '
        'dump_modify 줄에 # 없음 · 따옴표 한 쌍 (LIGGGHTS 입력 파서)', _ok(_dp4))

    def _dp5():
        me = os.path.abspath(__file__)
        base = ['--n-total', '100000', '--cgf', '151.4', '--arm', 'LC', '--seed', '32452843', '--revolutions', '2',
                '--stiffen-se', '20', '--hold-bo-pairwise']
        with _tf.TemporaryDirectory() as td:
            a = _sp.run([sys.executable, me, '--out', os.path.join(td, 'a')] + base + ['--dump-full-precision'],
                        capture_output=True, text=True)
            b = _sp.run([sys.executable, me, '--out', os.path.join(td, 'b')] + base, capture_output=True, text=True)
            h = _sp.run([sys.executable, me, '--help'], capture_output=True, text=True)
            dk_a = open(os.path.join(td, 'a', 'in.mixer'), encoding='utf-8').read()
            dk_b = open(os.path.join(td, 'b', 'in.mixer'), encoding='utf-8').read()
            ma = _js.load(open(os.path.join(td, 'a', 'deck_meta.json'), encoding='utf-8'))
            mb = _js.load(open(os.path.join(td, 'b', 'deck_meta.json'), encoding='utf-8'))
            fmt = dump_modify_format(['id', 'type', 'x', 'y', 'z', 'vx', 'vy', 'vz', 'fx', 'fy', 'fz', 'radius'])
            return (a.returncode == 0 and b.returncode == 0 and h.returncode == 0 and '--dump-full-precision' in h.stdout
                    and dk_a == _run_deck('LC', 2, dump_full_precision=True)
                    and _hs.sha256(dk_b.encode('utf-8')).hexdigest() == _RUN_DECKS[('LC', 2)]
                    and ma['dump_modify_format'] == fmt and ma['deck_sha256'] == _hs.sha256(dk_a.encode('utf-8')).hexdigest()
                    and '--dump-full-precision' in ma['argv'] and 'dump_modify_format' not in mb)
    chk('DP⑤ CLI --dump-full-precision → in.mixer = deck(…, True) · deck_meta.json 에 dump_modify_format · 덱 sha256 · argv — 플래그 없으면 '
        '실행 덱 sha256 그대로 · meta 에 그 키 없음 · --help rc 0 (argparse % 이스케이프)', _ok(_dp5))
    chk('DP⑥ dump_modify_format 은 모르는 열 (element · 빈 목록) 을 거부 — INT/DOUBLE 을 추정으로 정하지 않는다',
        _ok(lambda: _raises(lambda: dump_modify_format(['id', 'type', 'element'])) and _raises(lambda: dump_modify_format([]))
            and dump_modify_format(['id', 'type', 'x', 'radius']) == '%d %d %.17g %.17g'))
    #  ══ GM — D2 결합 규칙 (기하평균 · 2026-10-14 · 1저자 비준 D2 (가) — docs/mixer_paper_pipeline_draft_20261013.md §4) ═══════════════
    #  ★ 시험 먼저 — 옛 생성기에는 gm_arm · ced_matrix_geomean · pair_overlap · register_arm · _ced_matrix_min · --gm-* 가 없다 (NameError → GM FAIL).
    #    규칙: W_ij = 2√(γ_iγ_j) (혼합쌍 · 벽까지) · 힘 = JKR 스케일 F ∝ W·R* · 절대 수준 = SE–SE Bo_code 하나 · CED_ij = 쌍별 F₀ 의 역산.
    #    선택형 — rule="geomean" 팔만 이 경로 · 옛 팔 (min 규칙) · 옛 덱은 비트 그대로 (GM⑩ · DP①).
    _pg = plan(100000, cgf=151.4)
    _dg = _pg['d']

    def _gm(g_p, g_s=None, rho=None, bo=BO_BASE):
        """★ 10-21 (MXD2-05) — 벽 = 비코팅 NCM (1저자 10-14 Q2) 규칙 안의 팔만 만든다: AM γ ∈ {1 (코팅), ρ (비코팅)} · γ_W = 0.0256·ρ.
        ρ 를 안 주면 AM γ 중 1 이 아닌 값 (없으면 1 = 같은 γ 세계).  옛 판은 γ_W 0.0256 고정에 AM 0.3/0.5 처럼 Q2 밖 조합을 썼다."""
        g_s = g_p if g_s is None else g_s
        if rho is None:
            rho = next((x for x in (g_p, g_s) if x != 1.0), 1.0)
        return gm_arm({'AM_P': g_p, 'AM_S': g_s, 'SE': 1.0}, gamma_wall=gm_wall_from_ncm(rho), bo_se=bo, rho_uncoated_ncm=rho)

    def _F(M, ti, tj, d=None, E=None):
        d = _dg if d is None else d
        E = E_PHASE if E is None else E
        i, j = _NM.index(ti), _NM.index(tj)
        return f0_pair(M[i][j], rstar_pair(ti, tj, d), estar_pair(ti, tj, E))

    def _gm1():
        M = ced_matrix_geomean(_gm(1.0), _dg)
        L = ced_matrix('LC', _dg)
        return all(abs(M[i][i] / L[i][i] - 1.0) < 1e-12 for i in range(len(TYPES)))
    chk('GM① γ 비 1 (코팅 세계 · 전 상 같은 γ) 의 같은 상 대각 CED = LC 대각 (JKR 기하 환산 Bo_t = Bo_SE·r_S²ρ_S/(r_t²ρ_t) 과 같은 식 · '
        '상대 1e-12) — 바뀌는 것은 혼합쌍 · 벽뿐', _ok(_gm1))

    def _gm2():
        a_ = _gm(0.3, 1.0)                                   # ρ 0.3 세계 · AM_P 비코팅 · AM_S 코팅 (10-21 Q2 안 조합 — 옛 0.3/0.5 는 Q2 밖)
        M = ced_matrix_geomean(a_, _dg)
        g = dict(a_['gamma'])
        g[WALL] = a_['gamma_wall']
        fss = _F(M, 'SE', 'SE')
        rss = rstar_pair('SE', 'SE', _dg)
        w_se = (4.0 / 3.0) * math.pi * (_dg['SE'] / 2.0) ** 3 * DENS['SE'] * 1000.0 * 9.81
        for i, ti in enumerate(_NM):
            for j, tj in enumerate(_NM):
                if ti == WALL and tj == WALL:
                    if M[i][j] != 0.0:
                        return False
                    continue
                want = fss * math.sqrt(g[ti] * g[tj]) * rstar_pair(ti, tj, _dg) / rss
                if abs(_F(M, ti, tj) / want - 1.0) > 1e-12:
                    return False
        return fss > 0 and abs(fss / (BO_BASE * w_se) - 1.0) < 1e-12
    chk('GM② 모든 쌍 (벽 포함) 의 명목 점착 힘 F₀_ij = F₀_SS · √(γ_iγ_j)/γ_SE · R*_ij/R*_SS (상대 1e-12) · F₀_SS = Bo_SE × SE 무게 · 벽–벽 0',
        _ok(_gm2))

    def _gm3():
        M = ced_matrix_geomean(_gm(0.2, 1.0), _dg)          # ρ 0.2 세계 (10-21 Q2 안 — 옛 0.2/0.7)
        P = list(TYPES)
        return all(abs((_F(M, a1, b1) ** 2 * rstar_pair(a1, a1, _dg) * rstar_pair(b1, b1, _dg))
                       / (_F(M, a1, a1) * _F(M, b1, b1) * rstar_pair(a1, b1, _dg) ** 2) - 1.0) < 1e-11
                   for a1 in P for b1 in P)
    chk('GM③ 기하평균 항등식 — 입자 쌍마다 (F₀_ij/R*_ij)² = (F₀_ii/R*_ii)(F₀_jj/R*_jj) (= W_ij² = W_ii·W_jj · 상대 1e-11)', _ok(_gm3))

    def _gm4():
        for r_ in (1.0, 0.3, 2.0):
            M = ced_matrix_geomean(_gm(r_), _dg)
            w = (lambda a1, b1: _F(M, a1, b1) / rstar_pair(a1, b1, _dg))
            dW = w('AM_P', 'AM_P') + w('SE', 'SE') - 2.0 * w('AM_P', 'SE')
            want = w('SE', 'SE') * (math.sqrt(r_) - 1.0) ** 2
            if abs(dW - want) > 1e-11 * w('SE', 'SE') or dW < -1e-11 * w('SE', 'SE'):
                return False
        return True
    chk('GM④ 논지 §2-1 — ΔW = W_AA + W_SS − 2W_AS = W_SS·(√(γ_A/γ_S) − 1)² ≥ 0 · 비 1 에서 0 (비 1 · 0.3 · 2 · 상대 1e-11)', _ok(_gm4))

    def _gm5():
        rP, rS_, rA = _dg['AM_P'] / 2.0, _dg['SE'] / 2.0, _dg['AM_S'] / 2.0
        M1 = ced_matrix_geomean(_gm(1.0), _dg)
        c1 = (abs(_F(M1, 'AM_P', 'SE') / _F(M1, 'SE', 'SE') - 2.0 * rP / (rP + rS_)) < 1e-12
              and abs(_F(M1, 'AM_S', 'SE') / _F(M1, 'SE', 'SE') - 2.0 * rA / (rA + rS_)) < 1e-12)
        rho_P, rho_S = ((rP + rS_) / (2.0 * rP)) ** 2, ((rA + rS_) / (2.0 * rA)) ** 2
        #  ★ 10-21 (MXD2-05) — 문턱마다 그 ρ 세계 하나 (두 AM 비코팅 · AM γ = ρ) — 옛 판은 한 덱에 AM_P ρ_P · AM_S ρ_S (Q2 밖)
        loP, hiP = (ced_matrix_geomean(_gm(rho_P * k_), _dg) for k_ in (0.99, 1.01))
        loS, hiS = (ced_matrix_geomean(_gm(rho_S * k_), _dg) for k_ in (0.99, 1.01))
        c2 = _F(loP, 'AM_P', 'SE') < _F(loP, 'SE', 'SE') < _F(hiP, 'AM_P', 'SE')
        c3 = _F(loS, 'AM_S', 'SE') < _F(loS, 'SE', 'SE') < _F(hiS, 'AM_S', 'SE')
        return c1 and c2 and c3 and abs(rho_P - 0.308642) < 1e-6 and abs(rho_S - 0.390625) < 1e-12
    chk('GM⑤ 논지 §2 산술 — 비 1 에서 SE 하나의 AM_P–SE / SE–SE 당김힘 = 2r_A/(r_A+r_S) (1.8 · AM_S 1.6) · SE–SE 가 이기는 비 < 0.3086 (AM_P) · '
        '0.3906 (AM_S) — 그 양쪽 1 % 에서 대소가 뒤집힌다', _ok(_gm5))

    def _gm6():
        #  ★ 10-21 (MXD2-05) — ρ 1 세계 (γ_W 0.0256 · Hare 단분산 0.32 그대로) + ρ 0.3 세계 (AM_P 비코팅 0.3 · AM_S 코팅 1 · γ_W 0.0256·0.3)
        M = ced_matrix_geomean(_gm(1.0), _dg)
        M3 = ced_matrix_geomean(_gm(0.3, 1.0), _dg)
        c1 = abs(_F(M, 'SE', WALL) / _F(M, 'SE', 'SE') - 2.0 * 0.16) < 1e-12
        c1b = abs(_F(M3, 'SE', WALL) / _F(M3, 'SE', 'SE') - 2.0 * 0.16 * math.sqrt(0.3)) < 1e-12
        c2 = abs(_F(M3, 'AM_P', WALL) / _F(M3, 'SE', WALL) - math.sqrt(0.3) * _dg['AM_P'] / _dg['SE']) < 1e-12
        c3 = abs(_F(M3, 'AM_S', WALL) / _F(M3, 'SE', WALL) - math.sqrt(1.0) * _dg['AM_S'] / _dg['SE']) < 1e-12
        return c1 and c1b and c2 and c3 and GM_WALL_HARE2026 == (0.04 / 0.25) ** 2
    chk('GM⑥ 벽 = 같은 기하평균 (W_iW = 2√(γ_iγ_W) · R* = r_입자) · Hare 2026 Table 3 의 γ_pw/γ_pp 0.16 → γ_W/γ_SE = 0.16² = 0.0256 → '
        'SE–벽 / SE–SE 당김힘 = 0.16 × 2 = 0.32 (Hare 단분산과 같음 · ρ 0.3 세계면 0.32·√0.3) · AM–벽 / SE–벽 = √(γ_A/γ_S)·r_A/r_S', _ok(_gm6))

    def _gm7():
        M = ced_matrix_geomean(_gm(0.3, 1.0), _dg)          # 10-21 Q2 안 조합 (옛 0.3/0.5)
        n = len(_NM)
        return (all(M[i][j] == M[j][i] and math.isfinite(M[i][j]) for i in range(n) for j in range(n))
                and all(M[i][j] > 0.0 for i in range(n) for j in range(n) if not (i == n - 1 and j == n - 1))
                and M[n - 1][n - 1] == 0.0)
    chk('GM⑦ 행렬 대칭 · 유한 · 벽–벽 0 · 나머지 양수', _ok(_gm7))

    #  ★ 10-21 (MXD2-04 · 05) — 거부 사례는 **겨냥한 결함 하나만** 빼고 Q2 규칙 안 (ρ 0.3 세계 · 또는 코팅 팔 + 명시 벽) 으로 둔다 —
    #    옛 판은 AM 0.3 에 명시 벽 0.0256 을 써서, 벽 규칙 검사가 생기면 다른 결함 (0 · NaN) 의 거부를 대신 내 그 결함 검사의 변이를 가린다.
    #    거부 **사유** 를 낱말로 대조한다 (거부됐는지만 보면 다른 검사가 대신 거부해도 통과한다).
    _gw3, _c1 = gm_wall_from_ncm(0.3), {'AM_P': 1.0, 'AM_S': 1.0, 'SE': 1.0}

    def _u3(**kw):
        return dict(dict(gamma_wall=_gw3, bo_se=BO_BASE, rho_uncoated_ncm=0.3), **kw)
    _gbad = [('상 누락', lambda: gm_arm({'AM_P': 0.3, 'SE': 1.0}, **_u3()), '빠지거나 남는 상'),
             ('γ 0', lambda: gm_arm({'AM_P': 0.0, 'AM_S': 0.3, 'SE': 1.0}, **_u3()), ''),
             ('γ 음수', lambda: gm_arm({'AM_P': -0.3, 'AM_S': 0.3, 'SE': 1.0}, **_u3()), ''),
             ('γ NaN', lambda: gm_arm({'AM_P': float('nan'), 'AM_S': 0.3, 'SE': 1.0}, **_u3()), ''),
             ('γ ∞', lambda: gm_arm({'AM_P': float('inf'), 'AM_S': 0.3, 'SE': 1.0}, **_u3()), ''),
             ('γ bool', lambda: gm_arm({'AM_P': True, 'AM_S': 0.3, 'SE': 1.0}, **_u3()), '수가 아니다'),
             ('γ 문자열', lambda: gm_arm({'AM_P': '0.3', 'AM_S': 0.3, 'SE': 1.0}, **_u3()), '수가 아니다'),
             ('SE ≠ 1', lambda: gm_arm({'AM_P': 0.3, 'AM_S': 0.3, 'SE': 2.0}, **_u3()), '정확히 1'),
             ('안 도는 상', lambda: gm_arm({'AM_P': 0.3, 'AM_S': 0.3, 'SE': 1.0, 'VGCF': 1.0}, **_u3()), '빠지거나 남는 상'),
             ('γ_W 없음', lambda: gm_arm(_c1, gamma_wall=None, bo_se=BO_BASE), '명시해야'),
             ('γ_W 0', lambda: gm_arm(_c1, gamma_wall=0.0, bo_se=BO_BASE), 'γ_W'),
             ('Bo 없음', lambda: gm_arm(_c1, gamma_wall=GM_WALL_HARE2026, bo_se=None), '명시해야'),
             ('Bo 0', lambda: gm_arm(_c1, gamma_wall=GM_WALL_HARE2026, bo_se=0.0), 'Bo_code'),
             ('Bo NaN', lambda: gm_arm(_c1, gamma_wall=GM_WALL_HARE2026, bo_se=float('nan')), '유한'),
             ('ρ NaN', lambda: gm_wall_from_ncm(float('nan')), '유한'),
             ('ρ ∞', lambda: gm_wall_from_ncm(float('inf')), '유한'),
             ('옛 팔 이름', lambda: register_arm('LC', _gm(0.3)), '이미 있다'),
             ('이름 형식', lambda: register_arm('bad name', _gm(0.3)), '영문자'),
             ('검증 우회', lambda: ced_matrix_geomean({'rule': 'geomean', 'gamma': {'AM_P': 0.3, 'AM_S': 0.3, 'SE': 1.0}, 'gamma_wall': 0.0064}, _dg),
              '검증 우회')]
    _gbad_got = {nm_: _exit_msg(f_) for nm_, f_, _w in _gbad}
    _gbad_bad = [nm_ for nm_, _f, w_ in _gbad if _gbad_got[nm_] is None or w_ not in _gbad_got[nm_]]
    chk(f'GM⑧ 입력 거부 (fail-closed) {len(_gbad)} 가지 — 상 누락 · 0 · 음수 · NaN · ∞ · bool · 문자열 · 기준 SE ≠ 1 · 안 도는 상 · γ_W 없음 · 0 · '
        f'Bo_SE 없음 · 0 · NaN · ρ NaN · ∞ · 옛 팔 이름 덮어쓰기 · 이름 형식 · 검증 안 된 사전 (gm_arm 우회) — 사유 낱말 대조 (어긋남 {_gbad_bad})',
        not _gbad_bad)

    def _gm9():
        c1 = (_exit_msg(lambda: ced_matrix_geomean(_gm(1.0, bo=5000.0), _dg)) or '').find('천장') >= 0   # 10-21: Bo 1e6 → 5000 (지원 범위 안 · 천장 밖)
        ced = 2.0e5
        c2 = abs(pair_overlap(ced, 'SE', 'SE', _dg, E_PHASE)
                 / overlap_for_ced(ced, _dg['SE'] / 2.0, PHASE_MECH['SE'][0], E=E_PHASE['SE']) - 1.0) < 1e-12
        rs_, es_ = rstar_pair('AM_P', 'SE', _dg), estar_pair('AM_P', 'SE', E_PHASE)
        d0 = (3.0 * math.pi * ced * math.sqrt(rs_) / (2.0 * es_)) ** 2
        c3 = abs(pair_overlap(ced, 'AM_P', 'SE', _dg, E_PHASE) / (d0 / (_dg['SE'] / 2.0)) - 1.0) < 1e-12
        rw_, ew_ = rstar_pair('SE', WALL, _dg), estar_pair('SE', WALL, E_PHASE)
        c4 = abs(pair_overlap(ced, 'SE', WALL, _dg, E_PHASE)
                 / ((3.0 * math.pi * ced * math.sqrt(rw_) / (2.0 * ew_)) ** 2 / (_dg['SE'] / 2.0)) - 1.0) < 1e-12
        return c1 and c2 and c3 and c4 and pair_overlap(0.0, 'SE', 'SE', _dg, E_PHASE) == 0.0
    chk('GM⑨ 겹침 천장 = 모든 쌍 δ₀/min(r) (같은 상 = overlap_for_ced · 혼합쌍 = 작은 반경 · 벽 = 입자 반경 · R* · E* 는 그 쌍) · Bo_SE 5000 = 천장 거부 '
        '(10-21 — 옛 1e6 은 지원 범위 밖이라 범위 검사가 먼저 거부한다)', _ok(_gm9))
    chk('GM⑩ 옛 팔 전부 — ced_matrix = min 규칙 그대로 (_ced_matrix_min · 디스패치만 추가 · 비트 동일)',
        _ok(lambda: all(ced_matrix(a_, _dg) == _ced_matrix_min(a_, _dg) for a_ in sorted(ARMS)
                        if ARMS[a_].get('rule') != 'geomean')))

    def _gm11():
        nm = register_arm('GMSELFTEST', _gm(0.3, 1.0))               # 10-21 Q2 안 조합 (옛 0.3/0.5)
        try:
            p20 = plan(100000, cgf=151.4, stiffen_se=20.0)
            Ms, Mn, nz = ced_for_deck(p20, nm, hold_bo_pairwise=True)
            En = p20['E']
            direct = ced_matrix_geomean(ARMS[nm], p20['d'], E=En)
            n = len(_NM)
            ok1 = all(abs(Mn[i][j] / direct[i][j] - 1.0) < 1e-12 for i in range(n) for j in range(n) if direct[i][j] != 0.0)
            ok2 = all(abs(_F(Mn, _NM[i], _NM[j], p20['d'], En) / _F(Ms, _NM[i], _NM[j], p20['d'], E_PHASE) - 1.0) < 1e-12
                      for i in range(n) for j in range(n) if Ms[i][j] != 0.0)
            return ok1 and ok2 and nz and _raises(lambda: ced_for_deck(p20, nm, hold_bo_pairwise=False))
        finally:
            ARMS.pop(nm, None)
    chk('GM⑪ 경화 ×20 + hold_bo_pairwise — 쌍별 F₀ 보존 행렬 = 새 E 로 직접 계산한 기하평균 행렬 (F₀ 목표가 E 와 무관 · 상대 1e-12) · hold 없으면 거부',
        _ok(_gm11))

    def _gm12():
        with _tf.TemporaryDirectory() as td:
            me = os.path.abspath(__file__)
            #  ★ 10-14 밤 — D2 덱 = 새 세대 덱 → --dens-gen 필수 (DG⑥).  같은 세대로 메모리 덱도 만든다.
            #  ★ 10-21 (MXD2-02 · 05) — Q2 안 팔 (ρ 0.3 세계 비코팅 · --gm-wall-ncm) + 기본값이 아닌 Bo 0.5 — 옛 판은 AM 0.3/0.5 + 명시 벽 0.0256
            #    (Q2 밖) · Bo = BO_BASE 라 메타에 상수 BO_BASE 를 적는 변이 (M16) 가 통과했다.
            base = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2',
                    '--stiffen-se', '20', '--hold-bo-pairwise', '--dens-gen', 'lab20261014']
            gmo = ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5']
            a = _sp.run([sys.executable, me, '--out', os.path.join(td, 'a')] + base + gmo, capture_output=True, text=True)
            b = _sp.run([sys.executable, me, '--out', os.path.join(td, 'b')] + base + gmo[:4], capture_output=True, text=True)
            c = _sp.run([sys.executable, me, '--out', os.path.join(td, 'c'), '--arm', 'LC'] + base + gmo, capture_output=True, text=True)
            h = _sp.run([sys.executable, me, '--help'], capture_output=True, text=True)
            if a.returncode != 0:
                return False
            dk = open(os.path.join(td, 'a', 'in.mixer'), encoding='utf-8').read()
            meta = _js.load(open(os.path.join(td, 'a', 'deck_meta.json'), encoding='utf-8'))
            nm = register_arm('GM', gm_arm({'AM_P': 0.3, 'AM_S': 0.3, 'SE': 1.0}, gamma_wall=gm_wall_from_ncm(0.3), bo_se=0.5,
                                           rho_uncoated_ncm=0.3))
            try:
                p20 = plan(100000, cgf=151.4, stiffen_se=20.0, dens_gen='lab20261014')
                want = deck(p20, resolve_rpm(p20['R'], FR_ANCHOR, None, False), 2, arm=nm, seed=32452843, hold_bo_pairwise=True)
            finally:
                ARMS.pop(nm, None)
            ar = meta.get('adhesion_rule') or {}
            return (dk == want and 'D2 결합 규칙' in dk and 'γ_W/γ_SE' in dk and ar.get('rule') == 'geomean'
                    and ar.get('gamma') == {'AM_P': 0.3, 'AM_S': 0.3, 'SE': 1.0} and ar.get('gamma_wall') == gm_wall_from_ncm(0.3)
                    and ar.get('bo_se') == 0.5 and b.returncode != 0 and c.returncode != 0
                    and h.returncode == 0 and '--gm-gamma' in h.stdout)
    chk('GM⑫ CLI --gm-gamma · --gm-wall-ncm · --gm-bo-se (Bo 0.5) → in.mixer = deck(같은 팔) · 머리에 규칙 · γ 표 · deck_meta.json adhesion_rule '
        '(γ · γ_W · Bo = 입력 그대로) · Bo_SE 빠지면 거부 · --arm 과 함께면 거부 · --help rc 0', _ok(_gm12))
    #  ★ GM⑬ — 벽 = 비코팅 NCM 에 묶기 (1저자 10-14 Q2 *"이렇게 진행해"* · docs/mixer_d2_wall_gamma_derivation_20261014.md §5) — 시험 먼저
    def _gm13():
        if not (gm_wall_from_ncm(0.3) == GM_WALL_HARE2026 * 0.3 and gm_wall_from_ncm(1.0) == GM_WALL_HARE2026):
            return False
        if not all(_raises(lambda v=v: gm_wall_from_ncm(v)) for v in (0.0, -1.0, float('nan'), float('inf'), True, '0.3', None)):
            return False
        Mu = ced_matrix_geomean(_gm(0.3, 0.3), _dg)                                  # 비코팅 팔 (ρ 0.3 세계)
        Mc = ced_matrix_geomean(_gm(1.0, 1.0, rho=0.3), _dg)                         # 같은 세계의 코팅 팔 (NCM 표면 = SE)
        iS, iW = _NM.index('SE'), _NM.index(WALL)
        same_wall = Mu[iS][iW] == Mc[iS][iW] and Mu[iS][iS] == Mc[iS][iS]
        with _tf.TemporaryDirectory() as td:
            me = os.path.abspath(__file__)
            base = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2',
                    '--dens-gen', 'lab20261014']                 # ★ 10-14 밤 — D2 덱 = 새 세대 덱 (DG⑥)
            ok_ = _sp.run([sys.executable, me, '--out', os.path.join(td, 'a'), '--gm-gamma', 'AM_P=1,AM_S=1', '--gm-wall-ncm', '0.3',
                           '--gm-bo-se', '0.21244'] + base, capture_output=True, text=True)
            both = _sp.run([sys.executable, me, '--out', os.path.join(td, 'b'), '--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3',
                            '--gm-gamma-wall', '0.00768', '--gm-bo-se', '0.21244'] + base, capture_output=True, text=True)
            if ok_.returncode != 0:
                return False
            meta = _js.load(open(os.path.join(td, 'a', 'deck_meta.json'), encoding='utf-8'))
            dk = open(os.path.join(td, 'a', 'in.mixer'), encoding='utf-8').read()
        ar = meta.get('adhesion_rule') or {}
        return (same_wall and ar.get('gamma_wall') == GM_WALL_HARE2026 * 0.3 and ar.get('wall_rule') == 'hare2026_x_rho_uncoated_ncm'
                and ar.get('rho_uncoated_ncm') == 0.3 and '벽 = 비코팅 NCM 에 묶음' in dk and both.returncode != 0)
    chk('GM⑬ 벽 = 비코팅 NCM 에 묶기 — gm_wall_from_ncm(ρ) = 0.0256·ρ (입력 거부 7) · 같은 ρ 세계의 비코팅 · 코팅 팔이 같은 SE–벽 · SE–SE CED · '
        'CLI --gm-wall-ncm → deck_meta wall_rule · rho_uncoated_ncm · 덱 머리 표기 · --gm-gamma-wall 과 함께면 거부', _ok(_gm13))
    #  ══ DG — 밀도 세대 (2026-10-14 밤 · 1저자 결정 — 랩 표준 진밀도 SE 1.64 · NCM (PC · SC) 4.85 · 범위 (가) 앞으로만 ·
    #     docs/density_generations_20261014.md) ════════════════════════════════════════════════════════════════════════════════
    #  ★ 시험 먼저 — 옛 생성기에는 DENS_GENERATIONS · dens_table · plan(dens_gen=) · --dens-gen 이 없다 (NameError · TypeError · rc 2 → DG FAIL).
    #    계약: 세대 미지정 = gen1 그 표 그대로 → 덱 · 메타 바이트 그대로 (㉟ · DP① · ST① 골든 + DG②) · 지정하면 덱 머리 · deck_meta 에 기록 ·
    #    D2 결합 규칙 (--gm-*) 덱 = 새 세대 덱 → --dens-gen 필수 (fail-closed · DG⑥).  이 표는 scripts/additives.py 정본의 사본 (DG①).
    import ast as _ast
    _LAB = 'lab20261014'

    def _add_tables():
        """같은 폴더 additives.py 의 DENS · DENS_GENERATIONS · DENS_CARRIED_FROM_GEN1 을 **AST 로** 읽는다 (import 안 함 · numpy 불요).
        값이 이름 (`'gen1': DENS`) 이면 이미 읽은 같은 모듈의 리터럴로 푼다.  못 읽으면 예외 (= FAIL — 조용한 초록 금지)."""
        src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'additives.py'), encoding='utf-8').read()
        lit = {}
        for node in _ast.parse(src).body:
            if not (isinstance(node, _ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], _ast.Name)
                    and node.targets[0].id in ('DENS', 'DENS_GENERATIONS', 'DENS_CARRIED_FROM_GEN1')):
                continue
            v = node.value
            lit[node.targets[0].id] = {_ast.literal_eval(k): (lit[vv.id] if isinstance(vv, _ast.Name) else _ast.literal_eval(vv))
                                       for k, vv in zip(v.keys, v.values)}
        return lit['DENS_GENERATIONS'], lit['DENS_CARRIED_FROM_GEN1']

    def _dg1():
        A, AC = _add_tables()
        if not (set(A) == set(DENS_GENERATIONS) == set(AC) == set(DENS_CARRIED_FROM_GEN1)):
            return False
        for g_ in A:
            if DENS_GENERATIONS[g_] != {k: A[g_][k] for k in DENS}:            # 이 생성기의 네 상만
                return False
            if tuple(DENS_CARRIED_FROM_GEN1[g_]) != tuple(k for k in AC[g_] if k in DENS):
                return False
        return DENS_GENERATIONS['gen1'] is DENS and DENS == {'AM': 4.80, 'SE': 2.00, 'VGCF': 2.00, 'PTFE': 2.20}
    chk('DG① 세대 표 사본 = scripts/additives.py 정본 (DENS_GENERATIONS · DENS_CARRIED_FROM_GEN1 — 이 생성기의 네 상 · AST 대조) · '
        'gen1 = DENS 그 객체 · DENS 값 옛것 그대로', _ok(_dg1))

    def _hdr_only(a_txt, b_txt):
        """b = a 에 **연속한 주석 줄 묶음 하나**를 끼운 것인가 → (예/아니오, 끼운 줄).  끼운 줄을 빼면 a 와 글자 그대로 같아야 한다."""
        al, bl = a_txt.split('\n'), b_txt.split('\n')
        k = len(bl) - len(al)
        i = next((j for j, (x, y) in enumerate(zip(al, bl)) if x != y), len(al))
        ins = bl[i:i + k]
        return (k > 0 and all(l.startswith('#') for l in ins) and bl[:i] + bl[i + k:] == al), ins

    def _dg2():
        p0 = plan(100000, cgf=151.4)
        pg = plan(100000, cgf=151.4, dens_gen='gen1')
        if not (p0['dens'] is DENS and p0['dens_gen'] is None and pg['dens_gen'] == 'gen1' and pg['dens'] == DENS):
            return False
        strip = lambda q: {k: v for k, v in q.items() if k not in ('dens', 'dens_gen')}
        rpm_ = resolve_rpm(p0['R'])
        a_, b_ = deck(p0, rpm_, 2, arm='LC'), deck(pg, rpm_, 2, arm='LC')
        only, ins = _hdr_only(a_, b_)
        return (strip(p0) == strip(pg) and 'dens_gen' not in a_ and only and any('dens_gen = gen1' in l for l in ins)
                and ced_matrix('LC', p0['d']) == ced_matrix('LC', p0['d'], dens=DENS_GENERATIONS['gen1']))
    chk('DG② 세대 미지정 = gen1 그 객체 (plan · CED 같은 수) · gen1 명시 덱 = 미지정 덱 + 머리 주석 묶음 하나 (끼운 줄을 빼면 글자 그대로)', _ok(_dg2))

    def _dg3():
        f0, _w0 = volume_fractions()
        fg, _wg = volume_fractions(dens_table('gen1'))
        fl, _wl = volume_fractions(dens_table(_LAB))
        se_g = (18 / 2.00) / (80 / 4.80 + 18 / 2.00)                    # 독립 산술 — NCM (PC · SC) 한 밀도라 P:S 7:3 이 몫에 안 들어간다
        se_l = (18 / 1.64) / (80 / 4.85 + 18 / 1.64)
        return (f0 == fg and _w0 == _wl == _wg and abs(f0['SE'] - se_g) < 1e-15 and abs(fl['SE'] - se_l) < 1e-15
                and abs(f0['SE'] - 0.35064935064935066) < 1e-15 and abs(fl['SE'] - 0.39954233409610984) < 1e-15
                and abs(fl['AM_P'] / fl['AM_S'] - 7.0 / 3.0) < 1e-12
                and plan(8000, dens_gen=_LAB)['phi'] == fl and plan(8000)['phi'] == f0)
    chk('DG③ 1저자 레시피 AM:SE 80:18 wt% · P:S 7:3 (활성 3 상) 의 SE 부피 몫 — gen1 0.3506493506 → lab 0.3995423341 (+4.89 %p · 독립 산술 대조) · '
        'wt% 는 세대와 무관 · plan 의 phi = 그 세대 부피분율', _ok(_dg3))

    def _dg4():
        pg = plan(100000, cgf=151.4)
        pl = plan(100000, cgf=151.4, dens_gen=_LAB)
        dl = deck(pl, resolve_rpm(pl['R']), 2, arm='LC')
        dg_ = deck(pg, resolve_rpm(pg['R']), 2, arm='LC')
        import re as _re4
        c1 = (_re4.findall(r'atom_type (\d) density constant (\d+) ', dl) == [('1', '4850'), ('2', '4850'), ('3', '1640')]
              and _re4.findall(r'atom_type (\d) density constant (\d+) ', dg_) == [('1', '4800'), ('2', '4800'), ('3', '2000')])
        c2 = (pg['dt_by'] == pl['dt_by'] == 'AM_S' and abs(pl['dt'] / pg['dt'] - math.sqrt(4.85 / 4.80)) < 1e-12)
        c3 = pl['n']['SE'] > pg['n']['SE'] and pl['n']['AM_P'] < pg['n']['AM_P'] and pl['d'] == pg['d']
        iS = TYPES.index('SE')
        Ml = ced_matrix('LC', pl['d'], dens=pl['dens'])
        Mg = ced_matrix('LC', pg['d'])
        bo_l = bond_for_ced(Ml[iS][iS], pl['d']['SE'] / 2.0, PHASE_MECH['SE'][0], 1.64, E=E_PHASE['SE'])
        c4 = abs(bo_l / BO_BASE - 1.0) < 1e-9 and Ml[iS][iS] != Mg[iS][iS]
        return c1 and c2 and c3 and c4
    chk('DG④ lab 덱: 템플릿 density constant 4850 · 4850 · 1640 (gen1 4800 · 4800 · 2000) · Rayleigh dt (AM_S 가 정함) ×√(4.85/4.80) · '
        'SE 개수 ↑ · AM_P ↓ · 지름 불변 · 같은 Bo_code 를 그 세대 밀도로 CED 역산 (SE–SE Bo 0.21244 유지 · CED 는 바뀜)', _ok(_dg4))

    def _dg5():
        bad = ('nope', '', ' gen1', 'GEN1', 1, b'gen1')
        lib = all(_raises(lambda b=b: plan(8000, dens_gen=b)) for b in bad) and all(_raises(lambda b=b: dens_table(b)) for b in bad)
        with _tf.TemporaryDirectory() as td:
            me = os.path.abspath(__file__)
            r1 = _sp.run([sys.executable, me, '--out', os.path.join(td, 'a'), '--n-total', '8000', '--dens-gen', 'nope'],
                         capture_output=True, text=True)
            r2 = _sp.run([sys.executable, me, '--out', os.path.join(td, 'b'), '--n-total', '8000', '--dens-gen', ''],
                         capture_output=True, text=True)
            made = os.path.exists(os.path.join(td, 'a', 'in.mixer')) or os.path.exists(os.path.join(td, 'b', 'in.mixer'))
        return lib and r1.returncode != 0 and r2.returncode != 0 and not made
    chk('DG⑤ 모르는 · 빈 · 공백 · 대소문자 · 수 · bytes 세대 = 거부 (plan · dens_table · CLI rc ≠ 0 · 덱 안 씀)', _ok(_dg5))

    def _dg6():
        with _tf.TemporaryDirectory() as td:
            me = os.path.abspath(__file__)
            base = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2']
            gmo = ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244']   # 10-21 Q2 안 (옛 AM_S 0.5)
            no = _sp.run([sys.executable, me, '--out', os.path.join(td, 'a')] + base + gmo, capture_output=True, text=True)
            yes = _sp.run([sys.executable, me, '--out', os.path.join(td, 'b')] + base + gmo + ['--dens-gen', _LAB],
                          capture_output=True, text=True)
            if yes.returncode != 0:
                return False
            no_made = os.path.exists(os.path.join(td, 'a', 'in.mixer'))
            meta = _js.load(open(os.path.join(td, 'b', 'deck_meta.json'), encoding='utf-8'))
            dk = open(os.path.join(td, 'b', 'in.mixer'), encoding='utf-8').read()
        nm = register_arm('GMDGTEST', gm_arm({'AM_P': 0.3, 'AM_S': 0.3, 'SE': 1.0}, gamma_wall=gm_wall_from_ncm(0.3), bo_se=BO_BASE,
                                             rho_uncoated_ncm=0.3))
        try:
            p0 = plan(100000, cgf=151.4)
            lib_refuse = _raises(lambda: deck(p0, resolve_rpm(p0['R']), 2, arm=nm))
            lib_meta_refuse = _raises(lambda: deck_meta(p0, resolve_rpm(p0['R']), 2, 32452843, nm, ''))
        finally:
            ARMS.pop(nm, None)
        return (no.returncode != 0 and '--dens-gen' in (no.stdout + no.stderr) and not no_made
                and meta.get('dens_gen') == _LAB and meta.get('dens_g_cm3') == DENS_GENERATIONS[_LAB]
                and meta.get('dens_carried_from_gen1') == ['VGCF', 'PTFE'] and f'dens_gen = {_LAB}' in dk
                and 'density constant 1640' in dk and lib_refuse and lib_meta_refuse)
    chk('DG⑥ ★ D2 결합 규칙 (--gm-*) 덱 = 새 세대 덱 — --dens-gen 없으면 거부 (CLI rc ≠ 0 · 덱 안 씀 · deck() · deck_meta() 도 거부) · '
        '주면 덱 머리 · deck_meta 에 dens_gen · 실제 값 · 옮긴 상 (VGCF · PTFE) 기록', _ok(_dg6))

    def _dg7():
        with _tf.TemporaryDirectory() as td:
            me = os.path.abspath(__file__)
            st = ['--n-total', '100000', '--cgf', '151.4', '--arm', 'LC', '--seed', '32452843', '--revolutions', '2',
                  '--stiffen-se', '20', '--hold-bo-pairwise']
            pl_ = ['--n-total', '8000', '--arm', 'E1', '--revolutions', '1']
            rs = {k: _sp.run([sys.executable, me, '--out', os.path.join(td, k)] + args_, capture_output=True, text=True)
                  for k, args_ in (('a', st), ('b', st + ['--dens-gen', 'gen1']), ('c', pl_), ('d', pl_ + ['--dens-gen', 'gen1']))}
            if any(r_.returncode != 0 for r_ in rs.values()):
                return False
            rd = lambda k, f: open(os.path.join(td, k, f), encoding='utf-8').read()
            has = lambda k: os.path.exists(os.path.join(td, k, 'deck_meta.json'))
            ma, mb, md = _js.loads(rd('a', 'deck_meta.json')), _js.loads(rd('b', 'deck_meta.json')), _js.loads(rd('d', 'deck_meta.json'))
            same_ab = _hdr_only(rd('a', 'in.mixer'), rd('b', 'in.mixer'))[0]
            same_cd = _hdr_only(rd('c', 'in.mixer'), rd('d', 'in.mixer'))[0]
            no_c = not has('c') and 'dens_gen' not in rd('c', 'in.mixer')
        keys = ('dens_gen', 'dens_g_cm3', 'dens_carried_from_gen1')
        vol = ('argv', 'deck_sha256', 'deck_bytes', 'schema')
        #  ★ 10-21 (MXD2-06) — 선택 키 (세대 · D2) 를 담은 메타는 schema mixer_deck_meta/2 (옛 판은 키를 더하고도 /1 그대로) · 키 없는 메타는 /1 그대로
        return (not any(k in ma for k in keys) and all(mb.get(k) is not None for k in keys) and mb['dens_gen'] == 'gen1'
                and mb['dens_g_cm3'] == DENS and mb['dens_carried_from_gen1'] == []
                and ma.get('schema') == 'mixer_deck_meta/1' and mb.get('schema') == md.get('schema') == 'mixer_deck_meta/2'
                and {k: v for k, v in ma.items() if k not in vol} == {k: v for k, v in mb.items() if k not in vol + keys}
                and same_ab and same_cd and no_c and md.get('dens_gen') == 'gen1')
    chk('DG⑦ 기록은 **요청했을 때만** — 강성 덱 (--dens-gen 없음) deck_meta 에 세대 키 없음 (schema /1) · gen1 명시 = 같은 메타 + 세대 키 (schema /2) · '
        '덱 = 머리 주석만 더함 · 기본 덱 (강성 아님) 은 deck_meta 를 안 쓰고 (파일 목록 그대로) gen1 명시면 deck_meta 를 쓴다', _ok(_dg7))

    #  ══ MX — D2 사전 공격 리뷰 반영 (2026-10-21 · 원장 MXD2-01 – 06 · 1저자 10-21 [믹서] Q1 "권고대로 해줘") ═══════════════════════════════
    #  ★ 시험 먼저 — 고치기 전 생성기는 극단 입력 (γ 1e-200 · Bo 1e-310 · '0_3' · 이름 'GM\n') 을 받고 · 벽 = 비코팅 NCM (Q2) 규칙 (AM γ ∈ {1, ρ}) 을
    #    강제하지 않고 · D2 덱의 벽 주석 · registered · schema 가 옛 값이다 ⇒ MX④ · ⑤ · ⑥a · ⑦ FAIL.  MX① – ③ · ⑥b · ⑥c 는 지금 코드가 **옳게** 내는 값을
    #    고정한다 — 사전 리뷰 변이 M04 · M05 · M06 · M07 · M15 · M16 · M18 이 셀프테스트를 그대로 통과하던 구멍 (변이 판에서 FAIL 이어야 한다).
    #    덱 수치는 **덱 텍스트에서** 다시 읽는다 (생성기 표 · 쌍 함수를 부르지 않는 독립 산술).
    import re as _re_mx
    _SEED2PH = {10487: 'AM_P', 11887: 'AM_S', 13901: 'SE'}          # 독립 사본 (TPL_SEED 를 부르지 않는다)

    def _dk(text):
        """★ 독립 되읽기 — 덱 텍스트 → 상별 type · 반지름 · 밀도 · E · ν · CED 행렬 · 중력."""
        lines, out, i = text.split('\n'), dict(tpl={}, g=None), 0
        while i < len(lines):
            buf = [lines[i]]
            while buf[-1].rstrip().endswith('&') and i + 1 < len(lines):
                i += 1
                buf.append(lines[i])
            t = ' '.join(b.rstrip().rstrip('&') for b in buf).split('#', 1)[0].split()
            i += 1
            if not t:
                continue
            if t[0] == 'create_box':
                out['n'] = int(t[1])
            elif t[0] == 'fix' and len(t) > 5 and t[3] == 'property/global' and t[4] in ('youngsModulus', 'poissonsRatio'):
                out['E' if t[4] == 'youngsModulus' else 'nu'] = [float(x) for x in t[6:]]
            elif t[0] == 'fix' and len(t) > 6 and t[3] == 'property/global' and t[4] == 'cohesionEnergyDensity':
                n_ = int(t[6])
                v_ = [float(x) for x in t[7:]]
                out['ced'] = [v_[k * n_:(k + 1) * n_] for k in range(n_)]
            elif t[0] == 'fix' and len(t) > 4 and t[3] == 'particletemplate/sphere':
                out['tpl'][_SEED2PH[int(t[4])]] = dict(at=int(t[t.index('atom_type') + 1]), rho=float(t[t.index('density') + 2]),
                                                       r=float(t[t.index('radius') + 2]))
            elif t[0] == 'fix' and len(t) > 4 and t[3] == 'gravity':
                out['g'] = float(t[4])
        return out

    def _dkF(D, a, b):
        """독립 산술 — 덱 값에서 쌍 (a, b) 의 (F₀, R*, E*, CED, δ₀/min r) · 벽 = 마지막 타입 · 벽 R* = r_입자."""
        at = {k: v['at'] for k, v in D['tpl'].items()}
        at[WALL] = D['n']
        ia, ib = at[a] - 1, at[b] - 1
        es = 1.0 / ((1.0 - D['nu'][ia] ** 2) / D['E'][ia] + (1.0 - D['nu'][ib] ** 2) / D['E'][ib])
        pa, pb = (a, b) if a != WALL else (b, a)
        ra = D['tpl'][pa]['r']
        rs = ra if pb == WALL else ra * D['tpl'][pb]['r'] / (ra + D['tpl'][pb]['r'])
        rmin = min(D['tpl'][x]['r'] for x in (a, b) if x != WALL)
        c = D['ced'][ia][ib]
        return (4.5 * math.pi ** 3 * rs ** 2 * c ** 3 / es ** 2, rs, es, c, (3.0 * math.pi * c * math.sqrt(rs) / (2.0 * es)) ** 2 / rmin)

    def _dkBo(D):
        s_ = D['tpl']['SE']
        return _dkF(D, 'SE', 'SE')[0] / ((4.0 / 3.0) * math.pi * s_['r'] ** 3 * s_['rho'] * D['g'])

    _MX_GM = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2',
              '--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5']

    def _cli_deck(td, tag, args):
        """생성기 CLI → (rc, 덱 텍스트 | None, deck_meta | None, 화면)."""
        out_ = os.path.join(td, tag)
        r_ = _sp.run([sys.executable, os.path.abspath(__file__), '--out', out_] + list(args), capture_output=True, text=True)
        pd_, pm_ = os.path.join(out_, 'in.mixer'), os.path.join(out_, 'deck_meta.json')
        return (r_.returncode, open(pd_, encoding='utf-8').read() if os.path.exists(pd_) else None,
                _js.load(open(pm_, encoding='utf-8')) if os.path.exists(pm_) else None, r_.stdout + r_.stderr)

    def _mx1():
        got = {}
        with _tf.TemporaryDirectory() as td:
            for tag, extra in (('lab_soft', ['--dens-gen', _LAB]), ('lab_ref20', ['--dens-gen', _LAB, '--stiffen-se', '20', '--hold-bo-pairwise']),
                               ('gen1_soft', ['--dens-gen', 'gen1'])):
                rc_, t_, m_, _s = _cli_deck(td, tag, _MX_GM + extra)
                if rc_ != 0 or t_ is None or m_ is None:
                    print(f'        {tag}: rc {rc_}')
                    return False
                D = _dk(t_)
                dec = _re_mx.search(r'SE–SE Bo_code (\S+) \(', t_)
                got[tag] = (_dkBo(D), float(dec.group(1)) if dec else None, (m_.get('adhesion_rule') or {}).get('bo_se'), D['tpl']['SE']['rho'])
        ok_ = (all(abs(b_ / 0.5 - 1.0) <= 3e-5 and d_ == 0.5 and mb_ == 0.5 for b_, d_, mb_, _r in got.values())
               and got['lab_soft'][3] == got['lab_ref20'][3] == 1640.0 and got['gen1_soft'][3] == 2000.0)
        if not ok_:
            print('        Bo_SE 되읽기 / 선언 / 메타 / ρ_SE: ' + ' · '.join(f'{k} {v[0]:.7g} / {v[1]} / {v[2]} / {v[3]:g}' for k, v in got.items()))
        return ok_
    chk('MX① ★ 절대 수준 · 기록 고정 (MXD2-02 · 변이 M04 · M05 · M16) — lab soft · lab ×20 · gen1 D2 덱 (CLI · ρ 0.3 세계 · Bo 0.5) 의 SE–SE Bo_code 를 '
        '**덱 텍스트에서** (SE 템플릿 r · 그 세대 ρ_SE · 중력) 되읽은 값 = 0.5 (상대 3e-5) = 덱 머리 선언 = deck_meta.adhesion_rule.bo_se', _ok(_mx1))

    def _mx2():
        pl = plan(100000, cgf=151.4, dens_gen=_LAB)
        ok_ = abs(_dkBo(_dk(deck(pl, resolve_rpm(pl['R']), 2, arm='LC'))) / BO_BASE - 1.0) <= 3e-5
        a_ = _gm(0.3, 1.0, bo=0.5)
        for g_ in ('gen1', _LAB):
            dn = DENS_GENERATIONS[g_]
            M = ced_matrix_geomean(a_, _dg, dens=dn)
            w_se = (4.0 / 3.0) * math.pi * (_dg['SE'] / 2.0) ** 3 * dn['SE'] * 1000.0 * 9.81
            ok_ = ok_ and abs(_F(M, 'SE', 'SE') / (0.5 * w_se) - 1.0) < 1e-12
        return ok_
    chk('MX② ★ 절대 수준 = 덱 세대의 ρ_SE (MXD2-02 · 변이 M04 · M05) — 옛 팔 LC 의 lab 덱도 SE–SE Bo_code 0.21244 (덱 텍스트 되읽기 · 상대 3e-5) · '
        'ced_matrix_geomean(dens = gen1 · lab) 의 F₀_SS = Bo_SE × 그 세대 SE 무게 (상대 1e-12)', _ok(_mx2))

    def _mx3():
        pl = plan(100000, cgf=151.4, dens_gen=_LAB)
        rpm_ = resolve_rpm(pl['R'])

        def _se_ov(bo, F=1.0):
            """독립 산술 — SE–SE 정적 겹침 δ₀/r (F₀_SS = Bo × lab SE 무게 · SE 영률 1e7 × F · F₀ 보존)."""
            r_ = pl['d']['SE'] / 2.0
            rs_ = r_ / 2.0
            es_ = 1.0 / (2.0 * (1.0 - 0.30 ** 2) / (1.0e7 * F))
            c_ = (bo * (4.0 / 3.0) * math.pi * r_ ** 3 * 1640.0 * 9.81 * es_ ** 2 / (4.5 * math.pi ** 3 * rs_ ** 2)) ** (1.0 / 3.0)
            return (3.0 * math.pi * c_ * math.sqrt(rs_) / (2.0 * es_)) ** 2 / r_
        res = {}
        for tag, bo, F in (('soft800', 800.0, 1.0), ('soft300', 300.0, 1.0), ('half300', 300.0, 0.5)):
            nm = register_arm('GMMX3', gm_arm({'AM_P': 10.0, 'AM_S': 10.0, 'SE': 1.0}, gamma_wall=gm_wall_from_ncm(10.0), bo_se=bo,
                                              rho_uncoated_ncm=10.0))
            try:
                p_ = pl if F == 1.0 else plan(100000, cgf=151.4, stiffen_se=F, dens_gen=_LAB)
                res[tag] = (_exit_msg(lambda: deck(p_, rpm_, 2, arm=nm, hold_bo_pairwise=(F != 1.0))), _se_ov(bo, F))
            finally:
                ARMS.pop(nm, None)
        ok_ = (res['soft800'][0] is not None and 'AM_P–SE' in res['soft800'][0] and res['soft800'][1] < OVL_CEILING
               and res['soft300'][0] is None
               and res['half300'][0] is not None and 'AM_P–SE' in res['half300'][0] and res['half300'][1] < OVL_CEILING)
        if not ok_:
            print('        ' + ' · '.join(f'{k}: {(v[0] or "수용")[-90:]} (SE–SE {v[1] * 100:.3f} %)' for k, v in res.items()))
        return ok_
    chk('MX③ ★ 혼합쌍 천장 (MXD2-03 · 변이 M06 · M07) — lab · ρ 10 세계 (비코팅 AM γ 10) · Bo 800 soft 는 AM_P–SE 로 거부 (SE–SE 0.853 % = 천장 안 · '
        '독립 산술) · Bo 300 soft 는 수용 · 같은 팔을 SE ×0.5 (F < 1) 로 무르게 하면 F₀ 보존 행렬에서 AM_P–SE 로 거부 (SE–SE 0.704 % 는 안)', _ok(_mx3))

    def _mx4():
        made = []

        def _reg(name):
            def f_():
                made.append(name)
                return register_arm(name, _gm(1.0))
            return f_
        cases = [('γ 1e-200', lambda: gm_arm({'AM_P': 1e-200, 'AM_S': 1e-200, 'SE': 1.0}, gamma_wall=GM_WALL_HARE2026 * 1e-200, bo_se=BO_BASE,
                                              rho_uncoated_ncm=1e-200), '범위'),
                 ('γ 2e6', lambda: gm_arm({'AM_P': 2e6, 'AM_S': 2e6, 'SE': 1.0}, gamma_wall=GM_WALL_HARE2026 * 2e6, bo_se=BO_BASE,
                                           rho_uncoated_ncm=2e6), '범위'),
                 ('ρ 1e-7', lambda: gm_wall_from_ncm(1e-7), '범위'),
                 ('Bo 1e-310', lambda: gm_arm(_c1, gamma_wall=GM_WALL_HARE2026, bo_se=1e-310), '범위'),
                 ('Bo 2e4', lambda: gm_arm(_c1, gamma_wall=GM_WALL_HARE2026, bo_se=2.0e4), '범위'),
                 ('이름 GM\\n', _reg('GM\n'), '영문자'), ('이름 GM\\r', _reg('GM\r'), '영문자'), ('이름 탭', _reg('GM\t'), '영문자'),
                 ('이름 NUL', _reg('G\x00M'), '영문자'), ('이름 끝 공백', _reg('GM '), '영문자'),
                 ('설명 줄바꿈', lambda: gm_arm(_c1, gamma_wall=GM_WALL_HARE2026, bo_se=BO_BASE, desc='한 줄\n둘째 줄'), '제어 문자'),
                 ('설명 CR', lambda: gm_arm(_c1, gamma_wall=GM_WALL_HARE2026, bo_se=BO_BASE, desc='a\rb'), '제어 문자'),
                 ('설명 DEL', lambda: gm_arm(_c1, gamma_wall=GM_WALL_HARE2026, bo_se=BO_BASE, desc='a\x7fb'), '제어 문자')]
        try:
            got = {nm_: _exit_msg(f_) for nm_, f_, _w in cases}
        finally:
            for n_ in made:
                ARMS.pop(n_, None)
        bad = [nm_ for nm_, _f, w_ in cases if got[nm_] is None or w_ not in got[nm_]]
        if bad:
            print(f'        어긋남 {bad}')
        return not bad
    chk('MX④ ★ 극단 입력 거부 (MXD2-04) — γ 1e-200 · 2e6 · ρ 1e-7 · Bo 1e-310 · 2e4 (지원 범위 γ · ρ · γ_W ∈ [1e-6, 1e6] · Bo ∈ [1e-6, 1e4] 밖) · '
        '팔 이름 끝 줄바꿈 · CR · 탭 · NUL · 공백 (fullmatch) · 설명의 제어 문자 (덱 주석 줄을 깨뜨린다) — 사유 낱말 대조', _ok(_mx4))

    def _mx4b():
        base = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2', '--dens-gen', _LAB]
        bad = {'밑줄 γ': ['--gm-gamma', 'AM_P=0_3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244'],
               '전각 γ': ['--gm-gamma', 'AM_P=０.３,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244'],
               'nan γ': ['--gm-gamma', 'AM_P=nan,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244'],
               '밑줄 Bo': ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0_5'],
               '전각 ρ': ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '０.３', '--gm-bo-se', '0.21244'],
               '밑줄 γ_W': ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.02_56', '--gm-bo-se', '0.21244']}
        with _tf.TemporaryDirectory() as td:
            res = {k: _cli_deck(td, f'b{i}', base + v) for i, (k, v) in enumerate(bad.items())}
            good = _cli_deck(td, 'ok', base + ['--gm-gamma', ' AM_P = 0.3 , AM_S = 0.3 ', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244'])
        miss = [k for k, r_ in res.items() if not (r_[0] != 0 and r_[1] is None and 'ASCII 십진' in r_[3])]
        if miss:
            print(f'        수용 · 사유 어긋남 {miss}')
        return not miss and good[0] == 0 and (good[2] or {}).get('adhesion_rule', {}).get('gamma') == {'AM_P': 0.3, 'AM_S': 0.3, 'SE': 1.0}
    chk('MX④b ★ CLI 수 토큰 = ASCII 십진수만 (MXD2-04) — --gm-gamma 의 0_3 (옛 판: 3.0) · 전각 ０.３ · nan · --gm-bo-se 0_5 · --gm-wall-ncm ０.３ · '
        '--gm-gamma-wall 0.02_56 → rc ≠ 0 · 덱 안 씀 · 사유 "ASCII 십진" · 앞뒤 공백만은 허용', _ok(_mx4b))

    def _mx5():
        bad = {'AM 0.3 · ρ 3': lambda: gm_arm({'AM_P': 0.3, 'AM_S': 0.3, 'SE': 1.0}, gamma_wall=gm_wall_from_ncm(3.0), bo_se=BO_BASE,
                                              rho_uncoated_ncm=3.0),
               'AM_P 0.3 · AM_S 0.6 · ρ 0.3': lambda: gm_arm({'AM_P': 0.3, 'AM_S': 0.6, 'SE': 1.0}, gamma_wall=_gw3, bo_se=BO_BASE,
                                                              rho_uncoated_ncm=0.3),
               'AM 0.5 · ρ 0.3': lambda: gm_arm({'AM_P': 0.5, 'AM_S': 0.5, 'SE': 1.0}, gamma_wall=_gw3, bo_se=BO_BASE, rho_uncoated_ncm=0.3),
               '명시 벽 · AM 0.3': lambda: gm_arm({'AM_P': 0.3, 'AM_S': 0.3, 'SE': 1.0}, gamma_wall=GM_WALL_HARE2026, bo_se=BO_BASE),
               '명시 벽 · AM_P 1 · AM_S 0.3': lambda: gm_arm({'AM_P': 1.0, 'AM_S': 0.3, 'SE': 1.0}, gamma_wall=_gw3, bo_se=BO_BASE),
               'ρ ↔ γ_W 어긋남': lambda: gm_arm(_c1, gamma_wall=GM_WALL_HARE2026, bo_se=BO_BASE, rho_uncoated_ncm=0.3)}
        msgs = {k: _exit_msg(f_) for k, f_ in bad.items()}
        miss = [k for k, m_ in msgs.items() if m_ is None or 'Q2' not in m_]
        if miss:
            print(f'        수용 · 사유 어긋남 {miss}')
        return not miss
    chk('MX⑤ ★ 벽 = 비코팅 NCM (1저자 10-14 Q2 · MXD2-05 · 변이 M13) 을 라이브러리가 강제 — --gm-wall-ncm ρ 이면 AM γ 마다 1 (코팅) 또는 ρ (비코팅) 만 · '
        '명시 벽 (--gm-gamma-wall) 은 AM γ 전부 1 인 팔만 · γ_W ≠ 0.0256·ρ 거부 — 리뷰 F4 셋 (AM 0.3 · ρ 3 / 0.3 · 0.6 · ρ 0.3 / 0.5 · ρ 0.3) 포함 · 사유 "Q2"',
        _ok(_mx5))

    def _mx5b():
        arms = {'uu': _gm(0.3, 0.3), 'cc': _gm(1.0, 1.0, rho=0.3), 'cu': _gm(1.0, 0.3), 'one': _gm(1.0),
                'exp': gm_arm(_c1, gamma_wall=GM_WALL_HARE2026 * 0.3, bo_se=BO_BASE)}
        base = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2', '--dens-gen', _LAB, '--gm-bo-se', '0.21244']
        cli = {'AM 0.3 · ρ 3': ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '3'],
               'AM_P 0.3 · AM_S 0.6 · ρ 0.3': ['--gm-gamma', 'AM_P=0.3,AM_S=0.6', '--gm-wall-ncm', '0.3'],
               'AM 0.5 · ρ 0.3': ['--gm-gamma', 'AM_P=0.5,AM_S=0.5', '--gm-wall-ncm', '0.3'],
               '명시 벽 · AM 0.3/0.5': ['--gm-gamma', 'AM_P=0.3,AM_S=0.5', '--gm-gamma-wall', '0.0256']}
        with _tf.TemporaryDirectory() as td:
            rr = {k: _cli_deck(td, f'q{i}', base + v) for i, (k, v) in enumerate(cli.items())}
        h = _sp.run([sys.executable, os.path.abspath(__file__), '--help'], capture_output=True, text=True)
        hs = ' '.join(h.stdout.split())
        src = open(os.path.abspath(__file__), encoding='utf-8').read().split('\n')
        open_q = [l_ for l_ in src if l_.lstrip().startswith('#') and '어느 상에 묶을지' in l_ and '✅' not in l_]
        cli_miss = [k for k, r_ in rr.items() if not (r_[0] != 0 and r_[1] is None and 'Q2' in r_[3])]
        if cli_miss or open_q:
            print(f'        CLI 수용 · 사유 어긋남 {cli_miss} · 열린 질문처럼 읽히는 주석 {len(open_q)} 줄')
        return (arms['uu']['surface'] == {'AM_P': 'uncoated', 'AM_S': 'uncoated'} and arms['cc']['surface'] == {'AM_P': 'coated', 'AM_S': 'coated'}
                and arms['cu']['surface'] == {'AM_P': 'coated', 'AM_S': 'uncoated'} and arms['one']['rho_uncoated_ncm'] == 1.0
                and all(arms[k]['wall_rule'] == GM_WALL_RULE_NCM for k in ('uu', 'cc', 'cu', 'one'))
                and arms['exp']['wall_rule'] == GM_WALL_RULE_EXPLICIT and abs(arms['exp']['rho_world'] - 0.3) < 1e-12
                and arms['exp']['surface'] == {'AM_P': 'coated', 'AM_S': 'coated'}
                and not cli_miss and h.returncode == 0 and '0.0256·ρ 여부' not in hs and 'Q2' in hs and not open_q)
    chk('MX⑤b 팔 사전 · CLI · 도움말이 Q2 를 따른다 (MXD2-05) — 표면 상태 (coated · uncoated) · 벽 규칙 (비코팅 NCM · 명시 = 코팅 팔만 · 함의 ρ = γ_W/0.0256) 기록 · '
        'CLI 리뷰 F4 셋 + 명시 벽 AM 0.3/0.5 → rc ≠ 0 · 덱 안 씀 · 도움말 · 주석이 열린 질문으로 읽히지 않는다', _ok(_mx5b))

    def _mx6a():
        with _tf.TemporaryDirectory() as td:
            rc_s, t_s, m_s, _x = _cli_deck(td, 'soft', _MX_GM + ['--dens-gen', _LAB])
            rc_r, t_r, m_r, _y = _cli_deck(td, 'ref', _MX_GM + ['--dens-gen', _LAB, '--stiffen-se', '20', '--hold-bo-pairwise'])
            rc_e, t_e, m_e, _z = _cli_deck(td, 'exp', ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2',
                                                       '--dens-gen', _LAB, '--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256',
                                                       '--gm-bo-se', '0.21244'])
        if not (rc_s == rc_r == rc_e == 0 and t_s and t_r and t_e and m_s and m_r and m_e):
            return False
        p0 = plan(100000, cgf=151.4)
        lc = deck(p0, resolve_rpm(p0['R']), 2, arm='LC')

        def wall_line(t):
            return next(l_ for l_ in t.split('\n') if l_.startswith('# ★ 메시 `type'))
        ar_s, ar_e = m_s.get('adhesion_rule') or {}, m_e.get('adhesion_rule') or {}
        return ('기하평균' in wall_line(t_s) and '입자값 ÷' not in wall_line(t_s) and '입자값 ÷ 1.842' in wall_line(lc)
                and m_s.get('schema') == m_r.get('schema') == m_e.get('schema') == 'mixer_deck_meta/2'
                and 'D2 결합 규칙' in m_s.get('registered', '') and '등록 전' in m_s.get('registered', '')
                and '강성' not in m_s.get('registered', '') and '강성' in m_r.get('registered', '')
                and ar_s.get('layered') is True and ar_s.get('surface') == {'AM_P': 'uncoated', 'AM_S': 'uncoated'}
                and ar_s.get('wall_rule') == 'hare2026_x_rho_uncoated_ncm' and ar_s.get('rho_uncoated_ncm') == 0.3
                and ar_e.get('wall_rule') == 'explicit_coated' and abs(ar_e.get('rho_world', 0.0) - 1.0) < 1e-12
                and '함의 ρ' in t_e and 'NCM 표면' in t_s)
    chk('MX⑥a ★ D2 덱의 기록 (MXD2-06) — 벽 주석 = D2 기하평균 (옛 "점착 = 입자값 ÷ 1.842" 는 옛 팔에만) · deck_meta schema mixer_deck_meta/2 · '
        'registered = D2 결합 규칙 (등록 전) · 경화 덱이면 강성 경로를 더함 · adhesion_rule 에 층상 · 표면 상태 · 벽 규칙 (비코팅 NCM ρ · 명시 = 함의 ρ)',
        _ok(_mx6a))

    def _mx6b():
        with _tf.TemporaryDirectory() as td:
            rc_s, t_s, _m, _x = _cli_deck(td, 'soft', _MX_GM + ['--dens-gen', _LAB])
        if rc_s != 0 or not t_s:
            return False
        D = _dk(t_s)
        rows = {}
        for l_ in t_s.split('\n'):
            tk = l_[1:].split() if l_.startswith('#') else []
            if len(tk) == 7 and '–' in tk[0] and tk[6].endswith('%') and tk[0].split('–')[0] in ('AM_P', 'AM_S', 'SE', 'WALL'):
                rows[tuple(tk[0].split('–'))] = (float(tk[3]), float(tk[5]), float(tk[6][:-1]))
        fss = _dkF(D, 'SE', 'SE')[0]
        bad = [k for k, (cc_, rr_, ov_) in rows.items()
               if not (abs(cc_ / _dkF(D, k[0], k[1])[3] - 1.0) < 1e-12 and abs(rr_ / (_dkF(D, k[0], k[1])[0] / fss) - 1.0) <= 5e-5
                       and abs(ov_ - 100.0 * _dkF(D, k[0], k[1])[4]) <= 2e-4)]
        if bad or len(rows) != 9:
            print(f'        머리 표 행 {len(rows)} · 어긋남 {bad}')
        return len(rows) == 9 and not bad
    chk('MX⑥b ★ D2 덱 머리 표 = 덱 값 (MXD2-06 · 변이 M15) — 9 쌍 행의 CED 칸 = 덱 CED · F0/F0_SS 칸 = 덱 값으로 다시 낸 F₀ 비 (상대 5e-5) · '
        'δ0/min r 칸 = 다시 낸 겹침 (±2e-4 %p)', _ok(_mx6b))

    def _mx6c():
        with _tf.TemporaryDirectory() as td:
            rc_s, t_s, m_s, _x = _cli_deck(td, 'soft', _MX_GM + ['--dens-gen', _LAB])
        return (rc_s == 0 and bool(t_s) and t_s.count('insert/pack') == 2 and 'fix insA ' in t_s and 'fix insB ' in t_s
                and gm_arm(_c1, gamma_wall=GM_WALL_HARE2026, bo_se=BO_BASE)['layered'] is True)
    chk('MX⑥c ★ D2 팔 = 층상 삽입 (D11 (가) · MXD2-06 · 변이 M18) — CLI D2 덱은 insert/pack 둘 (insA AM → insB SE) · gm_arm 기본 layered True',
        _ok(_mx6c))

    def _mx7():
        g_ = globals()
        saved = g_.get('GM_GAMMA_RANGE')
        try:
            g_['GM_GAMMA_RANGE'] = (1e-300, 1e300)                            # 범위 검사를 일부러 넓혀 사후 단언만 남긴다 (방어 깊이 시험)
            a_ = gm_arm({'AM_P': 1e-200, 'AM_S': 1e-200, 'SE': 1.0}, gamma_wall=GM_WALL_HARE2026 * 1e-200, bo_se=BO_BASE, rho_uncoated_ncm=1e-200)
            msg = _exit_msg(lambda: ced_matrix_geomean(a_, _dg))
        finally:
            if saved is None:
                g_.pop('GM_GAMMA_RANGE', None)
            else:
                g_['GM_GAMMA_RANGE'] = saved
        return msg is not None and '정규' in msg
    chk('MX⑦ 사후 단언 (MXD2-04 · 방어 깊이) — 지원 범위를 넓혀 γ 1e-200 을 넣으면 γ 곱 언더플로로 CED 0 이 생긴다 → 행렬 단계가 "벽–벽 밖 CED = 유한 · '
        '정규 양수" 로 거부 (옛 판: AM_P–AM_P 0 · 나머지 양수 덱을 썼다)', _ok(_mx7))
    print(f'\nmake_mixer_deck selftest: {ok}/{ok+len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='', help='덱을 쓸 디렉터리')
    ap.add_argument('--n-total', type=int, default=50000)
    ap.add_argument('--cgf', type=float, default=200.0)
    ap.add_argument('--fr', type=float, default=FR_ANCHOR,
                    help=f'★ 주 노브.  Froude ω²R/g.  기본 {FR_ANCHOR} = 씽키 컵프레임 밴드 중앙.  rpm 은 R 에서 유도')
    ap.add_argument('--rpm', type=float, default=None,
                    help='override.  주면 결과 Fr 을 찍고 밴드 밖이면 **거부** (--allow-off-band 로만 통과)')
    ap.add_argument('--allow-off-band', action='store_true',
                    help='Fr 스윕처럼 일부러 밴드 밖으로 갈 때만')
    ap.add_argument('--revolutions', type=int, default=5)
    ap.add_argument('--baffles', type=int, default=0,
                    help='배플 개수 (D10(b) 전단 축).  0 이면 덱이 배플 이전과 바이트 동일')
    ap.add_argument('--baffle-h', type=float, default=0.10,
                    help='드럼 반경 대비 배플 높이.  기본 0.10')
    ap.add_argument('--seed', type=int, default=32452843,
                    help='삽입 시드.  ⚠ 판정선(§7)이 SE_시드를 요구하므로 **반복이 필요하다**')
    ap.add_argument('--settle-s', type=float, default=None,
                    help='정착 시간 (s).  기본은 낙하높이·반발계수에서 유도')
    ap.add_argument('--arm', default=None, choices=sorted(ARMS),
                    help='점착 팔 (기본 E1).  `all` 대신 하나씩 — 디렉터리가 갈린다.  D2 결합 규칙 팔은 --arm 대신 --gm-* 로 (팔 이름 GM)')
    ap.add_argument('--gm-gamma', default=None,
                    help='★ D2 결합 규칙 (기하평균 W_ij = 2√(γ_iγ_j) · 1저자 비준 10-14 D2 (가)) — 상별 γ/γ_SE, 예: AM_P=0.3,AM_S=0.3 '
                         '(SE = 1 기준 · 생략하면 1 · 다른 값이면 거부 · 값 = ASCII 십진수).  --gm-wall-ncm (또는 --gm-gamma-wall) · --gm-bo-se 와 함께 '
                         '(셋 다 필수) · --arm · --all-arms 와 함께 못 씀')
    ap.add_argument('--gm-gamma-wall', type=_ascii_float_arg, default=None,
                    help=f'D2 벽 γ_W/γ_SE 를 값으로 — ✅ 1저자 10-14 Q2 = 벽은 비코팅 NCM 에 묶는다 (보통은 --gm-wall-ncm ρ 를 쓴다).  이 옵션은 '
                         f'NCM 상 γ 가 전부 1 인 팔 (코팅 · 같은 γ 세계) 에서만 받는다 — 그 벽의 비코팅 NCM ρ = γ_W/{GM_WALL_HARE2026:g} 를 함의로 기록 '
                         f'({GM_WALL_HARE2026:g} = Hare 2026 Table 3 · 당김힘 비 0.32 · docs/mixer_d2_wall_gamma_derivation_20261014.md §5)')
    ap.add_argument('--gm-wall-ncm', type=_ascii_float_arg, default=None,
                    help='★ 벽 = 비코팅 NCM 에 묶기 (1저자 10-14 Q2): 이 세계의 비코팅 NCM γ/γ_SE (ρ) 를 주면 γ_W/γ_SE = 0.0256 × ρ 로 계산 · '
                         'NCM 상 γ 는 1 (코팅) 또는 ρ (비코팅) 만 · 같은 세계의 코팅 팔에도 같은 ρ 를 준다 · --gm-gamma-wall 과 함께 못 씀')
    ap.add_argument('--gm-bo-se', type=_ascii_float_arg, default=None,
                    help=f'D2 절대 수준 = SE–SE Bo_code 하나 (명시 필수 · D3 유동성 앵커 전 = 개발 입력 · 지원 범위 '
                         f'[{GM_BO_RANGE[0]:g}, {GM_BO_RANGE[1]:g}] · ASCII 십진수)')
    ap.add_argument('--all-arms', action='store_true',
                    help='--out 아래에 팔마다 하위 디렉터리를 만든다')
    ap.add_argument('--stiffen-se', type=float, default=1.0,
                    help='★ 강성 축 (사전등록 mixer_highbo_stiffness_prereg_20260929 §3): SE 영률만 ×F (AM · 벽 · ν 불변) · '
                         'dt 는 같은 Rayleigh 규칙으로 새 E 에서 다시 · 물리 시간 불변.  1 이면 덱이 옛것과 바이트 동일.  '
                         '점착이 있는 팔은 --hold-bo-pairwise 가 없으면 거부 (E0 · L0 는 허용하고 머리에 기록)')
    ap.add_argument('--hold-bo-pairwise', action='store_true',
                    help='경화할 때 쌍별 명목 점착 힘 척도 F0 = B³/A² 보존: CED_new = CED_soft · (E*_new/E*_soft)^(2/3) '
                         '(원소마다 · 벽 = 선언된 벽 E · ν · R* = r_입자).  옛 동일상 규칙은 혼합쌍 ×1.272 · SE–벽 ×1.182 로 어긋난다 (HBR6-02)')
    ap.add_argument('--dt-factor', type=float, default=1.0,
                    help='dt 만 ×X (X = 1/k — 예: 0.5 = DEV E0_ref@dt/2).  정착 · 회전 · 덤프 간격 step 은 정확히 k 배 = '
                         '물리 시간 · 덤프 시각 불변.  1/X 가 정수 아니면 거부')
    ap.add_argument('--dump-full-precision', action='store_true',
                    help='★ (다) dump dmp 바로 뒤에 dump_modify format 한 줄 — id · type (· mol) = %%d · 나머지 %%.17g (double 왕복 · 기본 %%g 는 '
                         '6 유효숫자).  기본 끔 = 덱 바이트 그대로.  켜면 deck_meta.json 에 dump_modify_format.  ⚠ LIGGGHTS-PUBLIC 3.x 옛 문법 '
                         '(공개 소스 판독) · ibb 바이너리 실측 전 · 덤프 크기 약 2 배 (강성 축 사전등록 §12-4 (다) · 확인 블록 덱용)')
    ap.add_argument('--dens-gen', default=None, choices=sorted(DENS_GENERATIONS),
                    help='★ 밀도 세대 (2026-10-14 밤 · 1저자 랩 표준 · docs/density_generations_20261014.md) — 생략 = gen1 (AM 4.80 · '
                         'SE 2.00 · 옛 덱 · 메타 바이트 그대로 · 기록 없음).  주면 그 세대 밀도로 부피분율 → 개수 · 드럼 · dt · Bo ↔ CED · '
                         'density constant 를 다시 내고 덱 머리 · deck_meta.json 에 dens_gen · 실제 값 · 옮긴 상을 기록한다.  '
                         '--gm-* (D2) 덱은 이것이 **필수** (새 세대 덱)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    _gm = any(v is not None for v in (a.gm_gamma, a.gm_gamma_wall, a.gm_bo_se, a.gm_wall_ncm))
    if _gm:
        if a.dens_gen is None:
            raise SystemExit('⛔ --gm-* (D2 결합 규칙 덱) 는 새 세대 덱이다 — --dens-gen 을 명시해야 한다 '
                             f'({" · ".join(sorted(DENS_GENERATIONS))} · 1저자 10-14 밤 랩 표준 = lab20261014 · '
                             'docs/density_generations_20261014.md)')
        if a.arm is not None or a.all_arms:
            raise SystemExit('⛔ --gm-* (D2 결합 규칙 팔 GM) 는 --arm · --all-arms 와 함께 쓰지 않는다')
        if a.gm_gamma_wall is not None and a.gm_wall_ncm is not None:
            raise SystemExit('⛔ D2 결합 규칙: --gm-gamma-wall 과 --gm-wall-ncm 은 하나만 (벽 값을 두 번 정하지 않는다)')
        if a.gm_gamma is None or (a.gm_gamma_wall is None and a.gm_wall_ncm is None) or a.gm_bo_se is None:
            raise SystemExit('⛔ D2 결합 규칙: --gm-gamma · (--gm-gamma-wall 또는 --gm-wall-ncm) · --gm-bo-se 를 명시해야 한다 (숨은 기본값 없음)')
        _g = {}
        for _kv in a.gm_gamma.split(','):
            _k, _sep, _v = _kv.partition('=')
            _k = _k.strip()
            if not _sep or not _k or _k in _g:
                raise SystemExit(f'⛔ --gm-gamma {a.gm_gamma!r} — "상=값" 을 쉼표로 (상 중복 금지)')
            _g[_k] = ascii_decimal(_v, f'--gm-gamma {_k}')         # ★ 10-21 MXD2-04 — 옛 float() 는 '0_3' 을 3.0 으로 읽었다
        _g.setdefault('SE', 1.0)
        if a.gm_wall_ncm is not None:
            register_arm('GM', gm_arm(_g, gamma_wall=gm_wall_from_ncm(a.gm_wall_ncm), bo_se=a.gm_bo_se, rho_uncoated_ncm=a.gm_wall_ncm))
        else:
            register_arm('GM', gm_arm(_g, gamma_wall=a.gm_gamma_wall, bo_se=a.gm_bo_se))
        a.arm = 'GM'
    if a.arm is None:
        a.arm = 'E1'
    p = plan(a.n_total, cgf=a.cgf, stiffen_se=a.stiffen_se, dens_gen=a.dens_gen)
    _stiff = (a.stiffen_se != 1.0 or a.dt_factor != 1.0)
    rpm = resolve_rpm(p['R'], a.fr, a.rpm, a.allow_off_band)
    if a.dens_gen is not None:                         # 지정했을 때만 (생략 = 화면도 옛것 그대로)
        print(f'밀도 세대 dens_gen = {a.dens_gen}  ('
              + ' · '.join(f'{k} {v:g}' for k, v in p['dens'].items()) + ' g/cm³ · gen1 값을 옮긴 상: '
              + (' · '.join(DENS_CARRIED_FROM_GEN1[a.dens_gen]) or '없음') + ')')
    print(f'조성 → 개수 (N={p["n_total"]:,})')
    for k in TYPES:
        print(f'   {k:5s} φ {p["phi"][k]:.4f} · d {p["d"][k]*1e3:6.3f} mm · n {p["n"][k]:8,d}'
              + (f'  ({p["n_fib"][k]:,} 가닥 × {p["nsph"]} 구)' if k in p['n_fib'] else ''))
    print(f'\n드럼  R {p["R"]*1e3:.3f} mm (지름 {2*p["R"]*1e3:.1f} mm) · L {p["L"]*1e3:.3f} mm'
          f' · 부피 {p["v_drum"]*1e6:.0f} mL · STL scale {p["stl_scale"]:.4f}')
    print(f'시간  dt {p["dt"]:.3g} s · 임계 {p["rpm_crit"]:.0f} rpm'
          f' · {rpm:.1f} rpm 에서 Fr {fr_of(rpm, p["R"]):.4f}  (밴드 {FR_BAND})')
    steps = int(round(a.revolutions * (60/rpm) / p['dt']))
    print(f'비용  {a.revolutions} 바퀴 = {steps:,} step · 직렬 추정 '
          f'{p["n_total"]*steps/2.99e6/3600:.1f} h  (실측 처리율 2.99e6 p·step/s)')
    if _stiff:
        _st = run_steps(p, rpm, a.revolutions, settle_s=a.settle_s, dt_factor=a.dt_factor)
        _d0, _b0 = plan_dt_soft(p)
        print(f'강성  SE 영률 ×{a.stiffen_se:g} ({E_PHASE["SE"]:.4g} → {p["E"]["SE"]:.4g} Pa) · hold_bo_pairwise '
              f'{"yes" if a.hold_bo_pairwise else "no"} · dt_factor {a.dt_factor:g} → 덱 dt {_st["dt_txt"]} s '
              f'(soft {_d0:.4g} s · {_b0} → 규칙 {p["dt"]:.4g} s · {p["dt_by"]}) · 정착 {_st["steps_fill"]:,} ×2 · '
              f'회전 {_st["steps_run"]:,} · 덤프 {_st["dump_every"]:,} step  (위 비용 줄은 규칙 dt 기준)')
    if a.out:
        arms = sorted(ARMS) if a.all_arms else [a.arm]
        #  ★ 덱을 **먼저** 다 만든다 — 거부 (합성수 시드 · hold 없는 경화 · 1/X 비정수) 는 디렉터리 · 빈 in.mixer 를 남기기 전에
        _texts = {arm: deck(p, rpm, a.revolutions, arm=arm, settle_s=a.settle_s, seed=a.seed,
                            n_baffles=a.baffles, baffle_h=a.baffle_h,
                            hold_bo_pairwise=a.hold_bo_pairwise, dt_factor=a.dt_factor,
                            dump_full_precision=a.dump_full_precision) for arm in arms}
        os.makedirs(os.path.join(a.out, 'data'), exist_ok=True)
        #  ★ 섬유 파일은 **섬유가 도는 경우에만** 쓴다 (생산 3 상에는 없다)
        _write_fibres(os.path.join(a.out, 'data'), p)
        for arm in arms:
            d = os.path.join(a.out, arm) if a.all_arms else a.out
            os.makedirs(os.path.join(d, 'data'), exist_ok=True)
            _write_fibres(os.path.join(d, 'data'), p)
            with open(os.path.join(d, 'in.mixer'), 'w') as f:
                f.write(_texts[arm])
            if _stiff or _gm or a.dens_gen is not None:
                #  ★ 봉인 가능한 메타 (경화 · dt 인자 덱 · D2 결합 규칙 덱 · 밀도 세대를 명시한 덱만 — 기본 덱은 파일 목록도 옛것 그대로)
                import json as _json
                with open(os.path.join(d, 'deck_meta.json'), 'w', encoding='utf-8') as f:
                    _json.dump(deck_meta(p, rpm, a.revolutions, a.seed, arm, _texts[arm], argv=sys.argv[1:],
                                         settle_s=a.settle_s, hold_bo_pairwise=a.hold_bo_pairwise,
                                         dt_factor=a.dt_factor, dump_full_precision=a.dump_full_precision),
                               f, ensure_ascii=False, indent=1)
                    f.write('\n')
            if a.baffles:
                import importlib.util as _iu
                _sp = _iu.spec_from_file_location(
                    '_bf', os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        'make_mixer_baffles.py'))
                _bf = _iu.module_from_spec(_sp); _sp.loader.exec_module(_bf)
                with open(os.path.join(d, 'Baffles.stl'), 'w') as f:
                    f.write(_bf.to_stl(_bf.baffle_tris(a.baffles, a.baffle_h)))
            print(f'   → {d}/in.mixer   [{arm}] {ARMS[arm]["desc"]}')
        print('⬜ STL 3개(Drum·Front·Back)를 각 디렉터리에 두어야 한다')
