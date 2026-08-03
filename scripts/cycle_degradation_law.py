#!/usr/bin/env python3
"""cycle_degradation_law — 사이클 열화 N축을 STEP4 인자로 합성 (B, 2026-07-29).

무엇을 푸나
──────────
STEP4 는 열화 **법칙**을 갖고 있지 않다.  `--cycle-n` 도움말이 명시한다:
"N 자체가 물성을 안 바꿈 (법칙 미탑재, §6 N1)".  실제 열화는 `--i0-cycle-mult` /
`--asr-film-cycle-ohm-cm2` 로 **배수를 직접 주입**해야 하고, 그 배수를 어디서 가져오느냐가
비어 있었다.  이 모듈이 그 빈칸을 채운다.

★★ 두 채널을 절대 섞지 않는다 (이중계산 금지) ★★
──────────────────────────────────────────────
`step4_dyn --i0-cycle-mult` 도움말의 규약을 그대로 따른다:

    ln R_ct(N) = ln g_chem(N)  +  ln g_mech(N)
                 ▲ 계면상 성장     ▲ 접촉면적 손실
                 (이 모듈)         (cycle_contact_ledger.py)

  · g_chem → STEP4 `--i0-cycle-mult = 1/g_chem`  (i0 를 낮춰 R_ct 를 키운다)
  · g_mech → **STEP4 에 넣지 않는다.**  원장이 반응면적 자체를 줄여 보고하는 몫이고,
    여기서 또 i0 로 넣으면 같은 물리를 두 번 센다.

⇒ 이 스크립트는 `--i0-cycle-mult` 값으로 **g_chem 만** 내놓는다.  g_mech 는 원장 JSON 에서
  읽어 **나란히 보고**하되(합성 R_ct 총량을 보여주려고) STEP4 플래그에는 넣지 않는다.
  두 몫을 합친 값을 STEP4 에 넣고 싶다면 그건 별도 결정이고, `--merge-into-i0` 로
  **명시적으로** 요구해야 한다 (그 경우 산출물에 double_count_risk 가 박힌다).

★ 화학 몫 g_chem(N) 의 앵커 ★
─────────────────────────────
크기 (끝점):
  Yun 2023 EnSM 10.1016/j.ensm.2023.102787 TableS1 — bare SC-NMC811 + LPSCl, **30 °C**, 0.33C,
  R_ct 341.7 → 982.3 Ω·cm² @ ~100 cyc = **2.87×**  (table_verified_litdb)
  · 같은 표의 R_ion 은 126 → 156 = 1.24× 로 훨씬 작다 → 열화는 **반응면(R_ct)** 에 몰린다.
  ★★ 라벨 (2026-07-30 리뷰 HIGH-4): 이 2.87× 는 풀셀 TLM 피팅의 **측정 총 R_ct** 이지 순수
  화학몫이 아니다 — 계면화학 × 전기활성면적손실이 곱해져 있다.  다만 Yun 은 CAM 균열을
  배제하려고 **단결정 NCM 을 일부러 채택**했고(litdb:60), 우리 mono 접촉-원장 추정 g_mech ≈ 1.02
  (CT 규약)이므로 내장 기계몫은 **≈2 %** 로 작다 → g_chem ≈ 2.87/1.02 ≈ **2.82**.
  ★★ 규약 정정 (2026-07-30 리뷰 HIGH-8): 여기 쓰던 1.05 는 **Holm 규약**(1/√A) 값이었는데
  `--i0-cycle-mult` 가 건드리는 채널은 **전하이동**이라 `read_ledger` 도 `rct_ct_area_rel`
  (CT, 1/A)을 쓴다 → ledger 유무에 따라 규약이 갈리는 불일치였다.  CT 대표값 1.02 로 통일
  (docs/a10_cycle_chemomech_design.md §6.3, 밴드 [0–2 %]).  ⚠ 이 값은 **실측이 아니라**
  우리 A10 접촉-원장 시뮬(ASSUMED-FORM CZM) 추정이다.
  `--subtract-mech` 로 그 감산을 켤 수 있다 (기본 OFF = 총량 그대로, 라벨로 고지).
★★ 채널 배분 경고 (2026-07-30 리뷰 HIGH-5) ★★
shape √N 의 정당화는 Park 의 "확산제한 Wagner **필름**" 인데, 필름 저항은 **옴성**(η ∝ I)이고
i0 감소는 **로그성**(η ∝ asinh)이다.  둘은 선형 극한에서만 일치한다.  전량을 `--i0-cycle-mult`
로 내면 리포 실측 동작점(η_kin 17–64 mV)에서 사이클 셀 분극을 **1.2–3.1× 과소평가**하고,
오차가 rate 와 함께 커져 fade-vs-rate 결론이 낙관 쪽으로 편향된다.
⇒ `--film-frac F` 로 총 성장의 F 몫을 `--asr-film-cycle-ohm-cm2`(옴성 채널, step4 에 이미 있음)
  로 돌릴 수 있다.  기본 0.0 = 전량 i0 = **고율 penalty 의 하한**이며, 출력에 그렇게 낙인한다.
  ⚠ F 의 물리적 값은 앵커가 없다(§F1) — 스윕 전용이다.

모양 (끝점 사이):
  Park 2023 AEM 10.1002/aenm.202203861 —
  · 코팅/첨가제 계면상: **선형-√t** (확산제한 Wagner film) → g_chem ∝ √N †
  · bare: **파라볼릭(super-√t)** = 화학 위에 접촉손실이 얹힌 모양
  † ★★ 라벨 강등 (2026-07-30 리뷰 MED-15) — `√t → √N` 은 **문헌지지가 아니라 ASSUMED** ★★
    Park 의 기울기는 `25.73 Ω·h⁻⁰·⁵` = 명시적 **시간** 단위다.  Wagner 확산제한은 δ ∝ √t 이고
    `√N ≡ √t` 는 **사이클 소요시간이 고정일 때만** 성립한다.  이 함수에는 시간 인자가 **없다**:
      Yun 앵커 0.33C ≈ 6.06 h/cyc ↔ 2C = 1.0 h/cyc ⇒ 같은 N 에서 **√6.06 = 2.462× 과대**
                                    ↔ 0.2C = 10 h/cyc ⇒ **1.284× 과소**
    ⇒ 지금 `shape='sqrt'` 는 "Park 문헌지지" 가 아니라 **rate 가 앵커와 같을 때만 문헌지지**다.
      rate 가 다르면 ASSUMED.  올바른 형태는 N 이 아니라 Σt 인덱싱: √(N·t_cyc/t_anchor).
      → `--c-rate` 로 그 보정을 켤 수 있다 (기본 OFF = 기존 √N, bitwise 불변).
    ⚠ 그런데 우리는 접촉손실을 g_mech 로 **따로** 센다 → bare 의 super-√t 를 g_chem 에
      그대로 쓰면 접촉 몫을 두 번 센다.  그래서 이 모듈의 기본 shape 은 **√N** 이고,
      `--shape parabolic` 은 "원장 없이 총량만 보고 싶을 때" 전용이며 경고를 찍는다.

⚠ **끝점 사이는 ASSUMED-FORM** 이다.  앵커는 N=0 과 N≈100 **두 점**뿐이고, 그 사이 모양은
  Park 의 정성적 shape 진술에서 가져왔다.  N>100 외삽은 앵커 밖이다 (경고를 찍는다).

⚠ **온도 의존 없음 — 그리고 앵커의 노화온도가 우리 셀과 다르다.**
  `docs/temp_pressure_capability.md` §13: LPSCl 분해율 Eₐ 는 문헌에 없고 노화 Arrhenius 를
  구할 수도 없다.  ★★ 정정 (2026-07-30 리뷰 HIGH-2): 여기 "사용자 랩의 노화온도에서 관측된 것"
  이라고 적었던 것은 **거짓**이다.  Yun 2023 은 **30 °C 사이클**이다
  (litdb `yun2023_deciphering_degradation_halide_vs_sulfide.md:106` — "갈바노 사이클
  2.5–4.3 V vs Li/Li⁺, **30 °C**, formation 0.05C×2 → cycling **0.33C**").
  사용자 랩은 **60 °C** 노화다(§13-2).  ⇒ 이 g_chem 을 60 °C 셀에 쓰는 것은 **30→60 °C
  무라벨 이전**이고, 그것이 정확히 §13 이 "불가능"이라 선언한 바로 그 조작이다.
  ⇒ 60 °C 셀에 대해서는 **2.87×@100cyc 을 하한(lower bound)으로만** 읽어야 한다
  (더 뜨거우면 더 빨리 열화한다는 것은 방향만 알고 크기는 모른다).
  rate 도 다르다 — Yun 0.33C vs 우리 0.2C/2C.

Selftest:  python3 scripts/cycle_degradation_law.py --selftest
사용:      python3 scripts/cycle_degradation_law.py --n 100 [--ledger ledger.json]
"""

import argparse
import json
import math
import os

# ── 앵커 (docs/data/rint_eis_anchors.csv 의 yun2023_rct_growth / rion_growth 와 동일) ────
YUN_RCT_N = 100                     # ~100 cyc
YUN_RCT_FROM, YUN_RCT_TO = 341.7, 982.3
G_CHEM_AT_ANCHOR = YUN_RCT_TO / YUN_RCT_FROM        # 2.8748…
YUN_RION_FROM, YUN_RION_TO = 126.0, 156.0
G_ION_AT_ANCHOR = YUN_RION_TO / YUN_RION_FROM       # 1.238… (참고: 전송은 열화 적음)
ANCHOR_T_CYCLE_C = 30.0            # ★ Yun 2023 노화온도 (litdb:106) — 사용자 랩 60 °C 와 다름
ANCHOR_C_RATE = 0.33               # Yun cycling rate
# ★ HIGH-8 (2026-07-30 리뷰): 이 상수는 1.05 = **Holm 규약**(1/√A, 구속저항 몫) 값이었다.
#   그런데 read_ledger() 는 스스로 "`--i0-cycle-mult` 가 건드리는 채널이 전하이동이라
#   rct_holm_rel 이 아니라 **rct_ct_area_rel** 을 쓴다" 고 선언한다 → ledger 를 주면 CT,
#   안 주면 Holm 이라는 **경로별 규약 불일치**.  CT 규약 대표값은 1.02
#   (docs/a10_cycle_chemomech_design.md:150 "| mono | Holm 1.05× | **CT 1.02×(대표)** |";
#    :152 "측정 CAM-SE R_int = 전하이동 지배 → CT(area⁻¹)가 대표규약").
#   ⚠ 출처도 정정: "mono 원장 실측" 이 아니라 **우리 A10 접촉원장 시뮬 추정**이다
#   (ASSUMED-FORM CZM; 자매 헤드라인 bimodal 1.51× 는 --poly-mode shrink-proxy 아티팩트로
#    재해석 대기 — CLAUDE.md).  또한 이건 N=100 값인데 원장은 "즉시파단" 을 기록했으므로
#   기계몫은 전반부 집중이다 → 전 N 상수 divisor 는 그 자체가 또 하나의 ASSUMED-FORM.
G_MECH_BUILTIN = 1.02              # CT(area⁻¹) 규약, mono — ASSUMED-FORM (A10 접촉원장 시뮬)
G_MECH_BUILTIN_CONVENTION = 'CT_area_inverse (rct_ct_area_rel) — Holm 규약이면 1.05'
G_MECH_BUILTIN_SRC = ('docs/a10_cycle_chemomech_design.md §6.3 표 (mono, CT 대표규약).  '
                      '출처 = 우리 A10 접촉-원장 시뮬 추정 (ASSUMED-FORM CZM), 실측 아님.  '
                      '밴드 [규약×f0] = [0–2%]; 전 N 상수 divisor 는 ASSUMED-FORM '
                      '(원장은 즉시파단 = 기계몫 전반부 집중)')
ANCHOR_SRC = ('Yun 2023 EnSM 10.1016/j.ensm.2023.102787 TableS1 (bare SC-NMC811+LPSCl, '
              '★30 °C · 0.33C, R_ct 341.7→982.3 Ω·cm² @~100cyc = 2.87× = **측정 총량**'
              '(기계몫 ≈2% 내장 — CT 규약, HIGH-8), table_verified_litdb) · shape = Park 2023 AEM '
              '10.1002/aenm.202203861 (coated/additive interphase = linear-√t).  '
              '⚠ 사용자 랩은 60 °C 노화 → 이 크기는 **하한**으로만 읽을 것 (§13)')

SHAPES = ('sqrt', 'linear', 'parabolic')


def rate_time_factor(c_rate=None, anchor_c_rate=ANCHOR_C_RATE):
    """사이클-수 축 → **시간** 축 환산 배수 t_cyc/t_anchor (MED-15).

    Park 의 Wagner 확산제한 기울기는 `Ω·h⁻⁰·⁵` = **시간** 단위다.  `√N ≡ √t` 는 사이클
    소요시간이 앵커와 같을 때만 성립하고, 한 사이클 소요시간 ∝ 1/C-rate 이므로

        t_cyc / t_anchor = anchor_c_rate / c_rate

    c_rate=None → **정확히 1.0** (기존 √N 경로 bitwise 불변; 기본 OFF).
    """
    if c_rate is None:
        return 1.0
    c = float(c_rate)
    if not (c > 0.0):
        raise ValueError(f'c_rate 는 양수여야 한다 (got {c_rate!r})')
    return float(anchor_c_rate) / c


def g_chem(n, shape='sqrt', g_anchor=G_CHEM_AT_ANCHOR, n_anchor=YUN_RCT_N, c_rate=None):
    """계면상 성장 배수 g_chem(N) = R_ct(N)/R_ct(0).  N=0 → 1.0, N=n_anchor → g_anchor.

    shape 은 **끝점 사이의 ASSUMED-FORM**:
      sqrt      — Park 코팅계 선형-√t (기본).  g = 1 + (g_a−1)·√(N/N_a)
      linear    — 하한 대조 (계면상이 두께-선형).  g = 1 + (g_a−1)·(N/N_a)
      parabolic — Park bare (super-√t).  ⚠ 접촉손실을 포함한 모양이라 g_mech 와 이중계산 위험

    c_rate (MED-15) — 주면 진행좌표를 **시간**으로 인덱싱한다:
      r = (N/N_a)·(anchor_c_rate/c_rate).  Park 기울기가 h⁻⁰·⁵ 단위이므로 이쪽이 옳다.
      기본 None = 옛 √N (앵커 rate 0.33C 에서만 문헌지지; 다른 rate 에선 ASSUMED).
    """
    if shape not in SHAPES:
        raise ValueError(f'shape 은 {SHAPES} 중 하나 (got {shape!r})')
    n = float(n)
    if n <= 0:
        return 1.0
    r = (n / float(n_anchor)) * rate_time_factor(c_rate)
    f = {'sqrt': math.sqrt(r), 'linear': r, 'parabolic': r ** 1.5}[shape]
    return 1.0 + (float(g_anchor) - 1.0) * f


def i0_cycle_mult(n, shape='sqrt', **kw):
    """STEP4 `--i0-cycle-mult` 값 = 1/g_chem(N).  (i0 를 낮춰 R_ct 를 키운다; <1 = 열화)"""
    return 1.0 / g_chem(n, shape, **kw)


def read_ledger(path):
    """원장 JSON → {N: g_mech}.  g_mech = rct_ct_area_rel (전하이동 면적 몫).

    ⚠ rct_holm_rel(=구속저항 몫) 이 아니라 rct_ct_area_rel 을 쓴다 — `--i0-cycle-mult` 가
      건드리는 채널이 **전하이동**이라 짝이 맞아야 한다 (Holm 몫은 옴성 쪽).
    """
    d = json.load(open(path))
    rows = d.get('rows') or d.get('trajectory') or d.get('checkpoints')
    if rows is None:
        for v in d.values():
            if isinstance(v, list) and v and isinstance(v[0], dict) and 'rct_ct_area_rel' in v[0]:
                rows = v
                break
    if not rows:
        raise SystemExit(f'{path}: 원장 궤적(rct_ct_area_rel 을 담은 리스트)을 찾지 못했습니다 — '
                         f'cycle_contact_ledger.py 산출 JSON 인지 확인하세요 (키: {sorted(d)[:8]})')
    out = {}
    for r in rows:
        if 'rct_ct_area_rel' not in r:
            continue
        n = int(r.get('N', r.get('n', r.get('cycle', -1))))
        if n >= 0:
            out[n] = float(r['rct_ct_area_rel'])
    if not out:
        raise SystemExit(f'{path}: rct_ct_area_rel 이 있는 행이 없습니다')
    return out


def compose(n_list, shape='sqrt', ledger=None, merge_into_i0=False, subtract_mech=False,
            film_frac=0.0, r_ct0_ohm_cm2=None, c_rate=None):
    """N 목록 → 채널 분리 표.  ledger = {N: g_mech} 또는 None.

    subtract_mech=True → 앵커의 내장 기계몫(G_MECH_BUILTIN)을 나눠 순수 화학몫으로 보정
    (리뷰 HIGH-4).  기본 OFF = 측정 총량 그대로 쓰되 라벨로 고지.
    """
    # ★ LOW-3 (2026-07-30 리뷰): 범위 검증이 main() 에만 있어, 모듈로 직접 부르면
    #   film_frac=1.5 가 예외 없이 통과하고 i0_cycle_mult=15.967 (= 사이클링이 i0 를 **16배
    #   개선**) 을 돌려줬다.  1 < F < 1.53 이 위험창.  함수 자체에서 막는다.
    if not (0.0 <= float(film_frac) <= 1.0):
        raise ValueError(f'film_frac 은 0~1 (성장분의 옴성 몫 비율) 이어야 한다 (got {film_frac!r}) — '
                         '1 을 넘으면 i0 배수가 >1 이 되어 "사이클링이 반응을 개선한다" 는 '
                         '비물리 결과가 나온다 (LOW-3)')
    if r_ct0_ohm_cm2 is not None and not (float(r_ct0_ohm_cm2) > 0.0):
        raise ValueError(f'r_ct0_ohm_cm2 는 양수여야 한다 (got {r_ct0_ohm_cm2!r})')
    _ga = G_CHEM_AT_ANCHOR / (G_MECH_BUILTIN if subtract_mech else 1.0)
    rows = []
    for n in n_list:
        gc = g_chem(n, shape, g_anchor=_ga, c_rate=c_rate)
        gm = None
        if ledger:
            gm = ledger.get(int(n))
            if gm is None and ledger:                     # 가까운 체크포인트로 대체하지 않는다
                gm = 'NO_CHECKPOINT'
        gm_num = gm if isinstance(gm, float) else None
        tot = gc * gm_num if gm_num else None
        _gb = tot if (merge_into_i0 and tot) else gc      # ★ 분할 기준 (HIGH-5: i0·필름 동일 기준)
        rows.append({
            'N': int(n),
            'g_chem': gc,
            'g_mech': gm,
            'g_total_Rct': tot,
            # ★ HIGH-5 (재검증): 옛 코드는 i0 를 tot(총량) 기준, 필름을 gc(chem-only) 기준으로 써서
            #   merge+film 조합에서 성장분 21.9% 가 조용히 증발했다 (ΔR 1141.6 → 891.1).
            #   ⇒ **같은 기준(_gbase)** 으로 분할한다: i0 가 (1−F), 필름이 F.
            'i0_cycle_mult': 1.0 / ((_gb - 1.0) * (1.0 - float(film_frac)) + 1.0),
            # ★ HIGH-9: merge 를 요청했는데 g_mech 가 없어 chem-only 로 떨어진 행을 **행별로** 표기.
            #   옛 코드는 rows[0] 라벨 하나를 전체에 인쇄해, 복붙하는 두 줄이 서로 다른 규약인데
            #   구별이 안 됐다.
            'i0_mult_channel': ('chem+mech (⚠ 이중계산 위험 — 원장 면적감소를 따로 보고하지 말 것)'
                                if (merge_into_i0 and tot) else
                                ('⚠ merge 요청됐으나 이 N 에 원장 체크포인트 없음 → chem only'
                                 if merge_into_i0 else 'chem only (규약)')),
            'merge_requested_but_chem_only': bool(merge_into_i0 and not tot),
            # ★ HIGH-5: 성장의 film_frac 몫을 옴성 채널로.  ΔR = R_ct0·(g−1) 중 그 몫을 Ω·cm² 로.
            #   ★★ HIGH-1 (2026-07-30 재검증): r_ct0 기본값을 YUN_RCT_FROM(341.7)로 두었던 것이
            #     치명적이었다 — 그건 **Yun 의 셀** R_ct0 이고, 게다가 step4 의 Ω·cm² 는 두 종류다:
            #       --r-int-ohm-cm2  = footprint 기준 (nx·ny·vox²)
            #       --asr-film-cycle-ohm-cm2 = **interfacial** 기준 (A_face = vox²)
            #     남의 셀 footprint 값을 우리 셀 interfacial 플래그에 주입하면 (실측 DBE 베드
            #     면적비 ≈44×, R_ct0 128.5 vs 341.7 = 2.66×) 0.2C 첫 스텝이 3.756 V → 1.325 V
            #     (−2431 mV) 로 무너진다.  ⇒ 기본값 금지, **사용자가 자기 베드 값을 명시**해야 한다.
            'asr_film_cycle_ohm_cm2': (float(r_ct0_ohm_cm2) * (_gb - 1.0) * float(film_frac)
                                       if (film_frac > 0 and r_ct0_ohm_cm2) else 0.0),
            'asr_basis': ('interfacial (A_face=vox²) — step4 --asr-film-cycle-ohm-cm2 규약; '
                          '★footprint 기준 R_int 값을 넣지 말 것'
                          if (film_frac > 0 and r_ct0_ohm_cm2) else None),
            'r_ct0_ohm_cm2_used': (float(r_ct0_ohm_cm2) if r_ct0_ohm_cm2 else None),
            'i0_is_lower_bound_penalty': film_frac <= 0.0,
            'g_chem_is_measured_total': not subtract_mech,
            'anchor_T_cycle_C': ANCHOR_T_CYCLE_C,
            'extrapolated': bool(n > YUN_RCT_N),
            # ★ MED-15: 진행좌표가 N 인지 Σt 인지 = 앵커 rate 와 다를 때 결정적
            'progress_axis': ('cycle_count_N (√N; 앵커 rate 0.33C 에서만 Park 문헌지지, '
                              '다른 rate 에선 ASSUMED — MED-15)' if c_rate is None else
                              f'elapsed_time_Sigma_t (c_rate={float(c_rate):g}C, '
                              f't_cyc/t_anchor={rate_time_factor(c_rate):.4f}) — Park 기울기가 '
                              f'h^-0.5 단위라 이쪽이 규약-정합'),
            'rate_time_factor': rate_time_factor(c_rate),
            'c_rate': (float(c_rate) if c_rate is not None else None),
        })
    return rows


def _selftest():
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        print(f"  {'OK  ' if cond else 'FAIL'} {name}" + (f' — {extra}' if extra else ''))
        ok &= bool(cond)

    # 앵커 재현 — 끝점 고정
    chk('N=0 → g_chem 정확히 1.0 (pristine)', g_chem(0).hex() == (1.0).hex())
    for sh in SHAPES:
        chk(f'N=100 ({sh}) → 앵커 2.87× 재현',
            abs(g_chem(YUN_RCT_N, sh) - G_CHEM_AT_ANCHOR) < 1e-12,
            f'{g_chem(YUN_RCT_N, sh):.4f}×')
    chk('앵커 배수가 CSV 값에서 유도 (매직넘버 아님)',
        abs(G_CHEM_AT_ANCHOR - 982.3 / 341.7) < 1e-12, f'{G_CHEM_AT_ANCHOR:.4f}')
    # shape 순서: 같은 N<N_a 에서 sqrt 가 가장 빠르게 오른다 (확산제한 = 초기 급성장)
    chk('N=25 에서 sqrt > linear > parabolic (확산제한이 초기에 빠르다)',
        g_chem(25, 'sqrt') > g_chem(25, 'linear') > g_chem(25, 'parabolic'),
        f"{g_chem(25,'sqrt'):.3f} / {g_chem(25,'linear'):.3f} / {g_chem(25,'parabolic'):.3f}")
    chk('단조 증가', all(g_chem(a) <= g_chem(b) for a, b in ((0, 1), (1, 10), (10, 50), (50, 100))))
    # i0 배수 = 역수, <1
    chk('i0_cycle_mult = 1/g_chem 이고 열화면 <1',
        abs(i0_cycle_mult(100) - 1.0 / G_CHEM_AT_ANCHOR) < 1e-12 and i0_cycle_mult(100) < 1.0,
        f'{i0_cycle_mult(100):.4f}')
    chk('N=0 → i0 배수 정확히 1.0 (무열화)', i0_cycle_mult(0).hex() == (1.0).hex())
    # ★ 채널 분리 = 이 모듈의 핵심 계약
    r = compose([100], ledger={100: 1.51})[0]
    chk('★ 기본은 g_chem 만 i0 로 (이중계산 금지)',
        abs(r['i0_cycle_mult'] - 1.0 / G_CHEM_AT_ANCHOR) < 1e-12
        and 'chem only' in r['i0_mult_channel'], f"{r['i0_mult_channel']}")
    chk('g_mech 는 나란히 보고되고 총량도 계산된다',
        r['g_mech'] == 1.51 and abs(r['g_total_Rct'] - G_CHEM_AT_ANCHOR * 1.51) < 1e-9,
        f"총 R_ct {r['g_total_Rct']:.3f}×")
    rm = compose([100], ledger={100: 1.51}, merge_into_i0=True)[0]
    chk('--merge-into-i0 는 명시 요구 시에만 + 위험 라벨',
        abs(rm['i0_cycle_mult'] - 1.0 / rm['g_total_Rct']) < 1e-12
        and '이중계산 위험' in rm['i0_mult_channel'])
    chk('원장에 그 N 체크포인트가 없으면 보간하지 않고 NO_CHECKPOINT',
        compose([37], ledger={0: 1.0, 100: 1.51})[0]['g_mech'] == 'NO_CHECKPOINT')
    chk('앵커 밖 외삽은 플래그된다',
        compose([200])[0]['extrapolated'] and not compose([50])[0]['extrapolated'])
    # 참고 앵커: 전송(R_ion)은 반응면보다 훨씬 덜 열화
    chk('참고 — R_ion 성장(1.24×)이 R_ct(2.87×)보다 작다',
        G_ION_AT_ANCHOR < G_CHEM_AT_ANCHOR, f'{G_ION_AT_ANCHOR:.3f}× vs {G_CHEM_AT_ANCHOR:.3f}×')
    # 정본 CSV 대조
    try:
        import csv as _csv
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         '..', 'docs', 'data', 'rint_eis_anchors.csv')
        vals = {r['anchor_id']: r['value'] for r in _csv.DictReader(open(p))}
        chk('정본 rint_eis_anchors.csv 의 yun2023 값과 일치',
            vals.get('yun2023_rct_growth') == '341.7to982.3'
            and vals.get('yun2023_rion_growth') == '126to156')
    except Exception as e:
        chk('정본 CSV 대조', False, f'{type(e).__name__}: {e}')
    # ── 2026-07-30 적대리뷰 반영 회귀 ────────────────────────────────────────────────
    # [HIGH-2] 앵커 노화온도가 사용자 랩과 다르다는 사실이 코드·출력에 있는가
    chk('★[H2] 앵커 노화온도 30 °C 가 상수로 노출 (사용자 랩 60 °C 와 다름)',
        abs(ANCHOR_T_CYCLE_C - 30.0) < 1e-9 and '30 °C' in ANCHOR_SRC and '하한' in ANCHOR_SRC)
    # [HIGH-4] 끝점이 측정 총량임을 라벨 + 감산 옵션이 실제로 값을 바꾼다
    _r_tot = compose([100])[0]
    _r_sub = compose([100], subtract_mech=True)[0]
    chk('★[H4] 기본은 "측정 총량" 으로 라벨', _r_tot['g_chem_is_measured_total'] is True)
    chk('★[H4] --subtract-mech 가 내장 기계몫을 실제로 나눈다',
        _r_sub['g_chem_is_measured_total'] is False
        and abs(_r_sub['g_chem'] - G_CHEM_AT_ANCHOR / G_MECH_BUILTIN) < 1e-12,
        f"{_r_tot['g_chem']:.4f} → {_r_sub['g_chem']:.4f}")
    # ★[H8] 위 단언은 **자기 상수 대비 산술 항등식**이라 G_MECH_BUILTIN 에 어떤 값을 넣어도
    #   통과한다 (규약도 앵커도 검증 안 함).  값 자체를 설계문서와 대조하는 핀을 따로 박는다.
    _a10 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        '..', 'docs', 'a10_cycle_chemomech_design.md')
    try:
        _a10_txt = open(_a10, encoding='utf-8').read()
    except OSError:
        _a10_txt = ''
    chk('★[H8] G_MECH_BUILTIN 이 CT(area⁻¹) 규약 = 설계문서 §6.3 mono 대표값 1.02',
        abs(G_MECH_BUILTIN - 1.02) < 1e-9 and 'CT_area_inverse' in G_MECH_BUILTIN_CONVENTION
        and ('| mono | 1.05× | 1.02× |' in _a10_txt if _a10_txt else True),
        f'{G_MECH_BUILTIN} ({G_MECH_BUILTIN_CONVENTION})'
        + ('' if _a10_txt else ' — ⚠ 설계문서 미발견, 상수만 검사'))
    chk('★[H8] 출처가 "실측" 이 아니라 우리 시뮬(ASSUMED-FORM)이라고 적혀 있다',
        '실측 아님' in G_MECH_BUILTIN_SRC and 'ASSUMED-FORM' in G_MECH_BUILTIN_SRC)
    chk('★[H8] read_ledger 채널(rct_ct_area_rel)과 내장 divisor 규약이 일치',
        'rct_ct_area_rel' in (read_ledger.__doc__ or '')
        and 'rct_ct_area_rel' in G_MECH_BUILTIN_CONVENTION)
    # [HIGH-5] film_frac 이 옴성 채널로 몫을 돌리고, 0 이면 하한이라고 낙인
    _r_f0 = compose([100])[0]
    # ★[H1] r_ct0 는 **우리 베드의 interfacial 기준** 값을 명시해야 한다 (기본값 없음 — 옛 코드가
    #   Yun 셀의 footprint 값 341.7 을 기본으로 흘려 0.2C 첫 스텝을 −2431 mV 무너뜨렸다).
    _R0_IFACE = 128.5                       # 실측 DBE 베드 interfacial R_ct0 [Ω·cm²]
    _r_f5 = compose([100], film_frac=0.5, r_ct0_ohm_cm2=_R0_IFACE)[0]
    chk('★[H5] film_frac=0 은 "고율 penalty 하한" 으로 낙인 + asr 0',
        _r_f0['i0_is_lower_bound_penalty'] is True and _r_f0['asr_film_cycle_ohm_cm2'] == 0.0)
    chk('★[H5] film_frac=0.5 → 옴성 채널 값 산출 + i0 몫은 절반만',
        _r_f5['asr_film_cycle_ohm_cm2'] > 0
        and abs(1.0 / _r_f5['i0_cycle_mult'] - (1.0 + (G_CHEM_AT_ANCHOR - 1.0) * 0.5)) < 1e-12,
        f"asr {_r_f5['asr_film_cycle_ohm_cm2']:.1f} Ω·cm² · i0mult "
        f"{_r_f0['i0_cycle_mult']:.4f}→{_r_f5['i0_cycle_mult']:.4f}")
    # ★[H1] r_ct0 를 안 주면 옴성 채널은 **0 이어야 한다** (남의 셀 기본값이 새는 것 금지)
    chk('★[H1] film_frac>0 이어도 r_ct0 미지정이면 asr=0 + basis=None (기본값 유출 금지)',
        compose([100], film_frac=0.5)[0]['asr_film_cycle_ohm_cm2'] == 0.0
        and compose([100], film_frac=0.5)[0]['asr_basis'] is None)
    chk('★[H1] asr_basis 가 interfacial 규약을 명시하고 footprint 혼입을 경고',
        'interfacial' in (_r_f5['asr_basis'] or '') and 'footprint' in (_r_f5['asr_basis'] or ''))
    # ★[H5] merge+film 동시 지정에서 성장분이 증발하지 않는다 (옛 코드 −21.9%)
    _r_mf = compose([100], ledger={100: 1.51}, merge_into_i0=True, film_frac=0.5,
                    r_ct0_ohm_cm2=_R0_IFACE)[0]
    _tot = _r_mf['g_total_Rct']
    _dR_i0 = _R0_IFACE * (1.0 / _r_mf['i0_cycle_mult'] - 1.0)
    chk('★[H5] merge+film: i0 몫 + 필름 몫 = 총 성장분 (증발 0)',
        abs((_dR_i0 + _r_mf['asr_film_cycle_ohm_cm2']) - _R0_IFACE * (_tot - 1.0)) < 1e-9,
        f"{_dR_i0:.2f} + {_r_mf['asr_film_cycle_ohm_cm2']:.2f} vs {_R0_IFACE*(_tot-1.0):.2f} Ω·cm²")
    # ★[M15] √t → √N: 진행좌표가 시간이어야 한다 (Park 기울기 = Ω·h⁻⁰·⁵)
    chk('★[M15] c_rate 미지정 = 정확히 1.0 (기존 √N bitwise 불변)',
        rate_time_factor().hex() == (1.0).hex()
        and g_chem(50).hex() == g_chem(50, c_rate=ANCHOR_C_RATE).hex())
    chk('★[M15] 2C 는 앵커(0.33C)보다 사이클이 짧다 → 같은 N 에서 성장 작다',
        abs(rate_time_factor(2.0) - ANCHOR_C_RATE / 2.0) < 1e-12
        and g_chem(100, c_rate=2.0) < g_chem(100),
        f'√N {g_chem(100):.4f} vs Σt@2C {g_chem(100, c_rate=2.0):.4f}')
    chk('★[M15] 0.2C 는 반대 방향 (사이클이 길어 성장 크다)',
        g_chem(100, c_rate=0.2) > g_chem(100),
        f'Σt@0.2C {g_chem(100, c_rate=0.2):.4f}')
    _ov2 = (g_chem(100) - 1.0) / (g_chem(100, c_rate=2.0) - 1.0)
    _un02 = (g_chem(100, c_rate=0.2) - 1.0) / (g_chem(100) - 1.0)
    chk('★[M15] 리뷰가 계산한 편차와 일치 (2C 2.462× 과대 · 0.2C 1.284× 과소)',
        abs(_ov2 - math.sqrt(2.0 / ANCHOR_C_RATE)) < 1e-12
        and abs(_un02 - math.sqrt(ANCHOR_C_RATE / 0.2)) < 1e-12,
        f'{_ov2:.3f}× / {_un02:.3f}×')
    chk('★[M15] 진행좌표가 산출물에 라벨된다 (N 이면 ASSUMED 고지)',
        'ASSUMED' in compose([100])[0]['progress_axis']
        and 'elapsed_time' in compose([100], c_rate=2.0)[0]['progress_axis'])
    for _bad in (0.0, -1.0):
        try:
            rate_time_factor(_bad)
            chk(f'★[M15] c_rate={_bad} 거부', False, '통과해버림')
        except ValueError:
            chk(f'★[M15] c_rate={_bad} 거부', True)
    # ★[L3] film_frac 범위 가드 — 옛 코드는 1.5 를 통과시켜 i0 배수 15.967 (사이클링이 i0 를
    #   16배 **개선**) 을 예외 없이 돌려줬다.  main() 검증만 있어 모듈 직접호출로 뚫렸다.
    for _bad in (1.5, -0.1, 2.0):
        try:
            compose([100], film_frac=_bad)
            chk(f'★[L3] film_frac={_bad} 거부', False, '예외 없이 통과')
        except ValueError:
            chk(f'★[L3] film_frac={_bad} 거부 (비물리 i0 개선 차단)', True)
    try:
        compose([100], film_frac=0.5, r_ct0_ohm_cm2=-1.0)
        chk('★[L3] r_ct0 음수 거부', False, '예외 없이 통과')
    except ValueError:
        chk('★[L3] r_ct0 음수 거부', True)
    chk('★[L3] 경계값 0.0 / 1.0 은 정상 통과 (과잉 가드 아님)',
        compose([100], film_frac=0.0)[0]['i0_cycle_mult'] > 0
        and compose([100], film_frac=1.0)[0]['i0_cycle_mult'] == 1.0)
    # [HIGH-9] merge 요청이 체크포인트 없는 행에서 조용히 강등되지 않고 **행별로** 표기된다
    _rr = compose([37, 100], ledger={100: 1.51}, merge_into_i0=True)
    chk('★[H9] merge 요청인데 체크포인트 없는 행이 행별로 표시된다',
        _rr[0]['merge_requested_but_chem_only'] is True
        and 'merge 요청됐으나' in _rr[0]['i0_mult_channel']
        and _rr[1]['merge_requested_but_chem_only'] is False
        and 'chem+mech' in _rr[1]['i0_mult_channel'])
    print('CYCLE-DEG-LAW SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--n', default='0,10,50,100', help='사이클 번호 목록 (쉼표)')
    ap.add_argument('--shape', choices=SHAPES, default='sqrt',
                    help='끝점 사이 ASSUMED-FORM (기본 sqrt = Park 코팅계 선형-√t)')
    ap.add_argument('--ledger', default='', help='cycle_contact_ledger.py 산출 JSON (g_mech)')
    ap.add_argument('--merge-into-i0', action='store_true',
                    help='⚠ g_chem×g_mech 을 i0 배수에 합친다 — 원장 면적감소와 **이중계산** 위험. '
                         '원장을 따로 보고하지 않을 때만.')
    ap.add_argument('--subtract-mech', action='store_true',
                    help='앵커 끝점에 내장된 기계몫(≈5%%, SC-NMC 단결정)을 나눠 순수 화학몫으로 보정. '
                         '기본 OFF = 측정 총량 그대로 (라벨로 고지).')
    ap.add_argument('--r-ct0-ohm-cm2', type=float, default=None,
                    help='★--film-frac 사용 시 **필수**: 이 베드의 pristine R_ct [Ω·cm², '
                         '**interfacial** 기준 = step4 --asr-film-cycle-ohm-cm2 규약].  '
                         '⚠ footprint 기준(--r-int-ohm-cm2)값을 넣지 말 것 — 두 Ω·cm² 는 분모가 '
                         '다르다(실측 베드 면적비 ≈44×).  기본값을 두지 않는 이유: 예전엔 Yun 의 '
                         '셀 341.7 이 기본이라 남의 셀 값이 조용히 주입됐고, 0.2C 첫 스텝이 '
                         '3.756 V → 1.325 V 로 무너졌다 (2026-07-30 재검증 HIGH-1).')
    ap.add_argument('--film-frac', type=float, default=0.0,
                    help='총 성장 중 **옴성 필름** 몫 [0-1] → --asr-film-cycle-ohm-cm2 로 산출. '
                         '기본 0 = 전량 i0(로그성) = 고율 penalty **하한**.  ⚠ F 값은 앵커 없음(§F1) '
                         '— 스윕 전용 (리뷰 HIGH-5: 전량 i0 는 분극을 1.2-3.1x 과소평가).')
    ap.add_argument('--c-rate', type=float, default=None,
                    help='★MED-15: 이 셀의 C-rate.  주면 진행좌표를 N 이 아니라 **경과시간 Σt** 로 '
                         f'인덱싱한다 (앵커 {ANCHOR_C_RATE}C 대비 t_cyc/t_anchor='
                         f'{ANCHOR_C_RATE}/c_rate).  Park 기울기가 Ω·h^-0.5 = **시간** 단위라 '
                         '√N≡√t 는 rate 가 앵커와 같을 때만 성립한다 (2C 면 √N 이 2.46x 과대, '
                         '0.2C 면 1.28x 과소).  기본 미지정 = 옛 √N (bitwise 불변).')
    ap.add_argument('--out-json', default='')
    a = ap.parse_args(argv)
    if a.selftest:
        raise SystemExit(_selftest())
    if a.shape == 'parabolic':
        print('  ⚠ shape=parabolic 은 Park bare(super-√t)로, **접촉손실이 포함된** 모양입니다. '
              'g_mech 를 따로 세면 이중계산이 됩니다 — 원장 없이 총량만 볼 때 쓰세요.', flush=True)
    ns = [int(float(x)) for x in a.n.split(',') if x.strip()]
    led = read_ledger(a.ledger) if a.ledger else None
    if not (0.0 <= a.film_frac <= 1.0):
        raise SystemExit(f'--film-frac 는 0-1 (got {a.film_frac})')
    # ★ HIGH-1: film 채널을 쓰려면 **이 베드의** R_ct0 를 명시해야 한다 (기본값 금지).
    if a.film_frac > 0 and a.r_ct0_ohm_cm2 is None:
        raise SystemExit(
            '--film-frac 를 쓰려면 --r-ct0-ohm-cm2 (이 베드의 pristine R_ct, **interfacial** '
            'Ω·cm²) 를 함께 주어야 합니다.\n'
            '  이유: 옴성 필름 ASR = R_ct0·(g−1)·F 이므로 R_ct0 가 **누구의 셀인지**가 값을 정합니다.\n'
            '  예전 기본값 341.7 은 Yun 2023 의 셀이고, 게다가 step4 의 Ω·cm² 는 두 종류입니다:\n'
            '    --r-int-ohm-cm2          = footprint 기준 (nx·ny·vox²)\n'
            '    --asr-film-cycle-ohm-cm2 = interfacial 기준 (A_face = vox²)   ← 이 값\n'
            '  둘을 섞으면 실측 DBE 베드에서 면적비 ≈44×, 0.2C 첫 스텝 3.756 V → 1.325 V 로 무너집니다.\n'
            '  → STEP4 산출 npz/metrics 의 pristine R_ct (interfacial) 를 확인해 넣으세요.')
    if a.r_ct0_ohm_cm2 is not None and not (a.r_ct0_ohm_cm2 > 0):
        raise SystemExit(f'--r-ct0-ohm-cm2 는 양수여야 합니다 (got {a.r_ct0_ohm_cm2})')
    if a.c_rate is not None and not (a.c_rate > 0):
        raise SystemExit(f'--c-rate 는 양수여야 합니다 (got {a.c_rate})')
    rows = compose(ns, a.shape, led, a.merge_into_i0, a.subtract_mech, a.film_frac,
                   a.r_ct0_ohm_cm2, a.c_rate)
    if a.c_rate is None:
        print(f'  ⚠ 진행좌표 = 사이클수 N (√N).  Park 앵커는 **시간** 축(Ω·h^-0.5)이라 이 규약은 '
              f'앵커 rate {ANCHOR_C_RATE}C 에서만 문헌지지다 — 다른 rate 면 --c-rate 로 Σt '
              f'인덱싱을 켜세요 (MED-15).', flush=True)
    else:
        print(f'  ★Σt 인덱싱: c_rate={a.c_rate:g}C → t_cyc/t_anchor='
              f'{rate_time_factor(a.c_rate):.4f} (앵커 {ANCHOR_C_RATE}C)', flush=True)
    print(f'\n사이클 열화 N축 — shape={a.shape} (ASSUMED-FORM), 앵커 N={YUN_RCT_N} g={G_CHEM_AT_ANCHOR:.4f}×')
    print(f'  {ANCHOR_SRC}\n')
    print(f"  {'N':>5s} {'g_chem':>8s} {'g_mech':>10s} {'R_ct 총':>9s} {'--i0-cycle-mult':>16s}  주")
    for r in rows:
        gm = (f"{r['g_mech']:.3f}" if isinstance(r['g_mech'], float)
              else ('—' if r['g_mech'] is None else r['g_mech']))
        tot = f"{r['g_total_Rct']:.3f}" if r['g_total_Rct'] else '—'
        note = ('⚠앵커밖 외삽' if r['extrapolated'] else '')
        print(f"  {r['N']:5d} {r['g_chem']:8.4f} {gm:>10s} {tot:>9s} "
              f"{r['i0_cycle_mult']:16.5f}  {note}")
    if any(r['merge_requested_but_chem_only'] for r in rows):
        print('\n  ⚠ 일부 행은 merge 요청됐으나 원장 체크포인트가 없어 **chem only** 로 산출됐다 '
              '— 위 표의 "채널" 열을 행별로 확인할 것 (복붙 시 규약이 섞인다).')
    for r in rows:
        print(f"  N={r['N']:<4d} 채널: {r['i0_mult_channel']}"
              + (f"  · asr_film {r['asr_film_cycle_ohm_cm2']:.3g} Ω·cm² ({r['asr_basis']})"
                 if r['asr_film_cycle_ohm_cm2'] else ''))
    if rows and rows[0]['i0_is_lower_bound_penalty']:
        print('  ⚠ film_frac=0 → 전량 i0(로그성).  옴성 필름 몫이 빠져 **고율 분극의 하한**이다 '
              '(리뷰 HIGH-5: 실측 동작점에서 1.2-3.1x 과소).')
    print(f"  ⚠ 앵커 노화온도 {ANCHOR_T_CYCLE_C:g} °C · {ANCHOR_C_RATE:g}C "
          f"(사용자 랩 60 °C 와 다름 → 크기는 **하한**으로 읽을 것)")
    print('  ⚠ 끝점 사이는 ASSUMED-FORM (앵커는 N=0/100 두 점) · 온도 의존 없음 '
          '(docs/temp_pressure_capability.md §13)')
    print('\nSTEP4 주입 예:')
    for r in rows:
        if r['N'] > 0:
            _af = (f" --asr-film-cycle-ohm-cm2 {r['asr_film_cycle_ohm_cm2']:.4g}"
                   if r['asr_film_cycle_ohm_cm2'] else '')
            print(f"  N={r['N']:<4d}  --cycle-n {r['N']} "
                  f"--i0-cycle-mult {r['i0_cycle_mult']:.5f}{_af}")
    if a.out_json:
        json.dump({'shape': a.shape, 'anchor': ANCHOR_SRC,
                   'g_chem_at_anchor': G_CHEM_AT_ANCHOR, 'n_anchor': YUN_RCT_N,
                   'assumed_form': 'endpoint-anchored; shape between N=0 and N=100 from Park 2023',
                   'no_temperature_dependence': 'docs/temp_pressure_capability.md §13 — '
                                                'LPSCl degradation-rate Ea absent from literature',
                   'rows': rows}, open(a.out_json, 'w'), ensure_ascii=False, indent=2)
        print(f'\n  saved → {a.out_json}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
