#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""⚡ 전류 흐름 (DEM 3D 뷰어 'net_current') — 접촉 **전류 밀도 (A cm⁻²)** 로 칠하기 · 컬러바 @1V + @1C (1저자 10-07 결정 · 웹앱 묶음 #17).

  옛 보기는 접촉 하나가 나르는 몫 |I|/I_전체 (%) 로 칠했다 → 결정: 몫 표시를 없애고 접촉 전류 밀도 j = |I_c| / A_c (A cm⁻²) 로 칠한다.
  두 틀 — @1V = 망 해의 1 V 프로브 그대로 (원고 S16 · S17 규약) · @1C = 운전 환산 (× I_1C / I_1V · 선형 · 같은 색 · 다른 숫자).
  I_1C 는 새 C-rate 식이 아니다 — 리포의 기존 규약 j_1C = 면적용량 × 1 h⁻¹ (mpm_webapp_payload j_1C_mA_cm2 · viewer3d.js "@1C 운전") 에
  케이스 표 등급의 Q_areal (grade_engine `__Q_areal_mAhcm2` — 같은 함수) 을 넣는다.

  [D1] 손으로 푸는 망 — SE 단순입방 3×3×3 (세로 접촉만 = 기둥 9 개 · 기둥마다 간선 둘이 직렬):
       I_간선 = 1 / (2 R) · R = d/(π r²) + 1/(2a) (Hertz H0: 원기둥 bulk + Maxwell 협착 · a = √(A/π)) · j = I σ₀ 10⁴ / A (A cm⁻²) ·
       ⟨J⟩_1V = I_전체 σ₀ 10⁴ / A_상자 · j / ⟨J⟩ = A_상자 / (9 A) — 해 · 단위를 손 계산과 대조.
  [D2] 합성 침대 (test_network_current_view 의 bed) — 모든 간선 j · A_c / (σ₀ 10⁴) = 덤프 |I| (이온 · 전자 · Hertz · Physics) ·
       A_c = 덤프 A_used (그 모드의 면적) · σ₀ = 게시 증서 sigma_bulk_S_cm (이온 0.003 · 전자 0.05) · ⟨J⟩_1V = 게시 σ (mS/cm) × 10 / T (µm).
  [D3] @1C — Q_areal = 케이스 표 등급 축 값 (grade_engine.axis_values 와 같은 값) · j_1C = Q × 10⁻³ A cm⁻² · 배율 = j_1C / ⟨J⟩_1V ·
       AM:SE 비 없음 = 등급 기본값 표지 · 두께 없음 = 환산 불가 (사유).
  [D4] σ₀ 출처 사다리 — 증서 → sigma_grain_S_cm (이온) → 게시 mS/cm ÷ σ/σ₀ (반올림 한계 표지) → 없음 (j 없음 · 사유).
  [D5] 뷰어 (node 로 함수를 잘라 실행) — 범례: A cm⁻² · @1V · @1C 두 눈금 · 옛 몫 문구 없음 · 컬러바 ⬇ 두 개 (1V · 1C) ·
       컬러바 스펙 (제목 · 눈금 = 1V × 배율) · 눈금 라벨 (지수 · 천 단위 콤마 없음) · @1C 불가면 단추 꺼짐 + 사유.
  [D6] check_all 배선.

  python3 webapp/test_net_current_density.py        # 종료코드 0 = PASS
"""
import copy
import json
import math
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
VIEWER_JS = os.path.join(HERE, 'static', 'js', 'viewer3d.js')
CHECK_ALL = os.path.join(SCRIPTS, 'check_all.sh')
sys.path.insert(0, HERE)
sys.path.insert(0, SCRIPTS)
from test_closed_param_labels import js_fn, js_const, run_node   # noqa: E402  (렌더된 JS 를 잘라 node 로 — 같은 도구)
import test_network_current_view as NCV                          # noqa: E402  (합성 침대 · CLI · 도구 실행 — 같은 도구)

_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f' — {extra}' if extra else ''))
    return bool(cond)


def rel(a, b):
    try:
        a, b = float(a), float(b)
    except (TypeError, ValueError):
        return math.inf
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


# ══════════════════════════════════════════════════════════════════════════════
#  손으로 푸는 망 — SE 단순입방 n × n × nz (세로 접촉만)
# ══════════════════════════════════════════════════════════════════════════════
LAT_R, LAT_A, LAT_AREA = 0.0005, 0.00098, 1e-7          # sim (scale 1000 → r 0.5 µm · 간격 0.98 µm · 면적 0.1 µm²)


def lattice(n=3, nz=3, r=LAT_R, a=LAT_A, area=LAT_AREA):
    atoms, cons, idx, k = {}, [], {}, 0
    for iz in range(nz):
        for iy in range(n):
            for ix in range(n):
                k += 1
                idx[(ix, iy, iz)] = 100 + k
                atoms[100 + k] = dict(type=3, x=(ix + 0.5) * a, y=(iy + 0.5) * a, z=r + iz * a, radius=r)
    for iz in range(nz - 1):
        for iy in range(n):
            for ix in range(n):
                cons.append(dict(id1=idx[(ix, iy, iz)], id2=idx[(ix, iy, iz + 1)], fz=5e-5, area=area, delta=2 * r - a))
    return atoms, cons, r + (nz - 1) * a + r, n * a


def publish(rd, case=None, run_id='20261007T000000-density01', thickness_um=None, porosity=20.0, am_se_ratio='80:20'):
    """웹앱 망 단계 게시 흉내 (같은 CLI · 도장) + 접촉 분석 산출 흉내 (full_metrics 두께 · 공극률 · input_params AM:SE 비) + 덤프 도구."""
    NCV.write_inputs(rd, case)
    rc, out = NCV.run_cli(rd, rd)
    if rc:
        raise RuntimeError(out[-600:])
    import pipeline_service as ps
    inputs = {n: ps.file_digest(os.path.join(rd, n)) for n in ('atoms.csv', 'contacts.csv')}
    ps.stamp_network_provenance(rd, run_id, inputs, 'success', argv={'type_map': NCV.TYPE_MAP, 'scale': '1000', 'contact_mode': 'both'})
    fm = {'network_run_id': run_id}
    if porosity is not None:
        fm['porosity'] = porosity
    if thickness_um is not None:
        fm['thickness_um'] = thickness_um
    with open(os.path.join(rd, 'full_metrics.json'), 'w') as f:
        json.dump(fm, f)
    if am_se_ratio is not None:
        p = os.path.join(rd, 'input_params.json')
        ip = json.load(open(p))
        ip['am_se_ratio'] = am_se_ratio
        with open(p, 'w') as f:
            json.dump(ip, f)
    rc, out = NCV.run_tool('dump', rd)
    if rc:
        raise RuntimeError(out[-600:])
    return rd


def payload(rd, channel='ionic', mode='hertzian', top=100000):
    import network_current as N
    return N.current_payload(rd, channel=channel, mode=mode, top=top, scale=1000)


def grade_q_areal(rd):
    """케이스 표의 Q_areal — 등급 엔진의 공개 경로 (axis_values) 로 (웹앱 _inject_input_params 와 같은 map_input_params)."""
    import grade_engine as G
    fm = json.load(open(os.path.join(rd, 'full_metrics.json')))
    ip = json.load(open(os.path.join(rd, 'input_params.json')))
    m = dict(fm)
    m.update(G.map_input_params(ip, None))
    lbl = next(ax['label'] for ax in G.AXES if ax.get('key') == '__Q_areal_mAhcm2')
    return G.axis_values(m).get(lbl)


# ══════════════════════════════════════════════════════════════════════════════
#  [D1] 손으로 푸는 망
# ══════════════════════════════════════════════════════════════════════════════
def section_analytic(tmp):
    print('[D1] 손으로 푸는 망 (SE 3×3×3 · 세로 접촉만) — j = I σ₀ 10⁴ / A · ⟨J⟩ = I_전체 σ₀ 10⁴ / A_상자')
    case = lattice()
    rd = publish(os.path.join(tmp, 'lat'), case, thickness_um=case[2] * 1000)
    st, b = payload(rd)
    chk(f'D1a 경로 200 · 간선 18 (기둥 9 × 2) ({st} · {len(b.get("edges") or [])})', st == 200 and len(b.get('edges') or []) == 18)
    r_um, d_um, A_um2 = LAT_R * 1000, LAT_A * 1000, LAT_AREA * 1e6
    R = d_um / (math.pi * r_um ** 2) + 1.0 / (2.0 * math.sqrt(A_um2 / math.pi))
    I_edge = 1.0 / (2.0 * R)
    sigma0 = 0.003
    j_hand = I_edge * sigma0 * 1e4 / A_um2
    A_box = (3 * LAT_A * 1000) ** 2
    J_hand = 9 * I_edge * sigma0 * 1e4 / A_box
    chk(f'D1b 해의 I_전체 = 손 계산 9/(2R) ({b.get("I_total")} · {9 * I_edge})', rel(b.get('I_total'), 9 * I_edge) < 1e-12)
    den = b.get('density') or {}
    E = b.get('edges') or []
    js = [e.get('j') for e in E]
    chk(f'D1c 간선마다 j (A cm⁻² @1V) = 손 계산 I σ₀ 10⁴ / A = {j_hand:.6g} (받은 {sorted(set(round(x, 9) for x in js if x))[:3]})',
        bool(js) and all(x is not None and rel(x, j_hand) < 1e-9 for x in js), repr(js[:3]))
    chk(f'D1d 간선마다 A_c = 덤프 A_used = 0.1 µm² ({sorted(set(e.get("ac") for e in E))[:3]})',
        bool(E) and all(e.get('ac') is not None and rel(e['ac'], A_um2) < 1e-12 for e in E))
    chk(f'D1e 단위 = A cm^-2 · σ₀ = 0.003 S/cm (게시 증서) ({den.get("unit")} · {den.get("sigma0_S_cm")} · {den.get("sigma0_source")})',
        den.get('unit') == 'A cm^-2' and den.get('sigma0_S_cm') == 0.003
        and 'solve_certificate_full.sigma_bulk_S_cm' in str(den.get('sigma0_source')))
    chk(f'D1f 단면 평균 ⟨J⟩_1V = I_전체 σ₀ 10⁴ / A_상자 = {J_hand:.6g} · 상자 = 증서 기하 ({den.get("j_mean_1V")} · {den.get("box_area_um2")} · '
        f'{den.get("box_source")})',
        rel(den.get('j_mean_1V'), J_hand) < 1e-9 and rel(den.get('box_area_um2'), A_box) < 1e-12
        and 'geometry' in str(den.get('box_source')))
    chk(f'D1g j / ⟨J⟩ = A_상자 / (9 A) = {A_box / (9 * A_um2):.6g} (면적 집중 — 기둥 9 개가 상자 단면을 나눠 진다)',
        bool(js) and js[0] is not None and rel(js[0] / den.get('j_mean_1V', float('nan')), A_box / (9 * A_um2)) < 1e-9)
    chk(f'D1h 범위 = 받은 간선의 j 최소 · 최대 ({den.get("j_min_1V")} · {den.get("j_max_1V")})',
        rel(den.get('j_min_1V'), j_hand) < 1e-9 and rel(den.get('j_max_1V'), j_hand) < 1e-9)
    c1 = den.get('c1') or {}
    q = grade_q_areal(rd)
    chk(f'D1i @1C — Q_areal = 케이스 표 등급 값 ({c1.get("Q_areal_mAh_cm2")} · {q}) · j_1C = Q × 10⁻³ A cm⁻² · 배율 = j_1C / ⟨J⟩_1V',
        c1.get('status') == 'ok' and q is not None and rel(c1.get('Q_areal_mAh_cm2'), q) < 1e-12
        and rel(c1.get('j_1C_A_cm2'), q * 1e-3) < 1e-12 and rel(c1.get('factor'), q * 1e-3 / J_hand) < 1e-9, repr(c1)[:300])
    chk('D1j @1C 규약 문구 = 선형 환산 · I_1C / I_1V · 전류 보존 가정 (반응 분포 없음) · Q_areal 출처 (등급)',
        all(s in str(c1.get('rule')) for s in ('I_1C', 'I_1V', '선형', '전류 보존', '반응 분포')) and 'Q_areal' in str(c1.get('source')))
    chk('D1k 전류 밀도 규약 문구 = |I_c| / A_c · 같은 풀이의 접촉 면적 (A_used) · 1 V 프로브',
        all(s in str(den.get('rule')) for s in ('|I_c|', 'A_c', 'A_used', '1 V')))
    return rd


# ══════════════════════════════════════════════════════════════════════════════
#  [D2] 합성 침대 — 항등식 (모든 간선 · 두 채널 · 두 모드)
# ══════════════════════════════════════════════════════════════════════════════
def section_identity(tmp):
    print('[D2] 합성 침대 — j · A_c / (σ₀ 10⁴) = 덤프 |I| · σ₀ = 게시 증서 · ⟨J⟩_1V = 게시 σ × 10 / T')
    rd = publish(os.path.join(tmp, 'bed'), thickness_um=7.86)
    raw = os.path.join(rd, NCV.DUMP)
    for ch, s0_want in (('ionic', 0.003), ('electronic', 0.05)):
        for mode in ('hertzian', 'physics'):
            st, b = payload(rd, ch, mode)
            den = b.get('density') or {}
            rows = NCV.read_csv_rows(NCV.dump_file(raw, f'edges_{mode}_{ch}'))
            byk = {}
            for r in rows:
                byk[(int(r['id1']), int(r['id2']))] = r
                byk[(int(r['id2']), int(r['id1']))] = r
            ok_j = ok_a = 0
            E = b.get('edges') or []
            for e in E:
                r = byk.get((e['ia'], e['ib']))
                if r is None:
                    continue
                aI, Au = abs(float(r['I'])), float(r['A_used'])
                ok_a += int(e.get('ac') is not None and rel(e['ac'], Au) < 1e-12)
                ok_j += int(e.get('j') is not None and den.get('sigma0_S_cm') and
                            rel(e['j'] * e['ac'] / (den['sigma0_S_cm'] * 1e4), aI) < 1e-12)
            chk(f'D2a {ch} · {mode}: 간선 {len(E)} 개 전부 j · A_c / (σ₀ 10⁴) = 덤프 |I| ({ok_j}) · A_c = 덤프 A_used ({ok_a})',
                st == 200 and len(E) > 0 and ok_j == len(E) and ok_a == len(E))
            chk(f'D2b {ch} · {mode}: σ₀ = 게시 증서 {s0_want} S/cm ({den.get("sigma0_S_cm")} · {den.get("sigma0_source")})',
                den.get('sigma0_S_cm') == s0_want and 'solve_certificate_full.sigma_bulk_S_cm' in str(den.get('sigma0_source')))
            pub = json.load(open(os.path.join(rd, f'network_conductivity_{mode}.json')))
            pre = '' if ch == 'ionic' else 'electronic_'
            geo = (pub.get(pre + 'solve_certificate_full') or {}).get('geometry') or {}
            T_um = float(geo.get('plate_z', 0)) * float(geo.get('scale', 0))
            J_pub = float(pub.get(pre + 'sigma_full_mScm') or 0) * 10.0 / T_um if T_um > 0 else float('nan')
            chk(f'D2c {ch} · {mode}: ⟨J⟩_1V = 게시 σ (mS/cm) × 10 / T (µm) — 케이스 표의 σ 와 같은 해 ({den.get("j_mean_1V")} · {J_pub:.6g} · '
                f'게시 반올림 6 자리)', rel(den.get('j_mean_1V'), J_pub) < 2e-5)
            jj = [e['j'] for e in E if e.get('j')]
            chk(f'D2d {ch} · {mode}: 범위 = 받은 간선 j 최소 · 최대 · 면적 없는 간선 0',
                bool(jj) and rel(den.get('j_min_1V'), min(jj)) < 1e-12 and rel(den.get('j_max_1V'), max(jj)) < 1e-12
                and den.get('n_no_area') == 0)
    st, b = payload(rd, 'ionic', 'hertzian', top=5)
    E = b.get('edges') or []
    aI = [e['s'] for e in E]
    chk('D2e 그릴 접촉 = |I| 큰 순 상위 N (옛 규칙 그대로 · 몫 s 는 자료에만 · 전류 밀도 순이 아니다)',
        st == 200 and len(E) == 5 and aI == sorted(aI, reverse=True))
    return rd


# ══════════════════════════════════════════════════════════════════════════════
#  [D3] @1C 변형
# ══════════════════════════════════════════════════════════════════════════════
def section_c1(tmp, bed_rd):
    print('[D3] @1C — Q_areal 출처 · 기본값 표지 · 환산 불가 사유')
    st, b = payload(bed_rd)
    c1 = (b.get('density') or {}).get('c1') or {}
    q = grade_q_areal(bed_rd)
    chk(f'D3a 두께 · 공극률 · AM:SE 비가 있으면 ok · 기본값 없음 ({c1.get("status")} · {c1.get("defaults_used")} · Q {c1.get("Q_areal_mAh_cm2")} = {q})',
        c1.get('status') == 'ok' and c1.get('defaults_used') == [] and rel(c1.get('Q_areal_mAh_cm2'), q) < 1e-12)
    rd2 = os.path.join(tmp, 'bed_noratio')
    shutil.copytree(bed_rd, rd2)
    p = os.path.join(rd2, 'input_params.json')
    ip = json.load(open(p))
    ip.pop('am_se_ratio', None)
    json.dump(ip, open(p, 'w'))
    st, b = payload(rd2)
    c1 = (b.get('density') or {}).get('c1') or {}
    chk(f'D3b AM:SE 비 없음 → 등급 엔진 기본값 (wt_AM 0.80) 으로 낸 값 · 표지 ({c1.get("status")} · {c1.get("defaults_used")})',
        c1.get('status') == 'ok' and any('am_se_ratio' in str(x) for x in (c1.get('defaults_used') or [])))
    rd3 = os.path.join(tmp, 'bed_nothick')
    shutil.copytree(bed_rd, rd3)
    fm = json.load(open(os.path.join(rd3, 'full_metrics.json')))
    fm.pop('thickness_um', None)
    json.dump(fm, open(os.path.join(rd3, 'full_metrics.json'), 'w'))
    st, b = payload(rd3)
    den = b.get('density') or {}
    c1 = den.get('c1') or {}
    chk(f'D3c 두께 없음 → @1C 환산 불가 (사유) · @1V 는 그대로 ({c1.get("status")} · {c1.get("reason")})',
        st == 200 and c1.get('status') == 'unavailable' and 'thickness_um' in str(c1.get('reason'))
        and c1.get('factor') is None and (b.get('edges') or [{}])[0].get('j') is not None)
    rd4 = os.path.join(tmp, 'bed_nofm')
    shutil.copytree(bed_rd, rd4)
    os.remove(os.path.join(rd4, 'full_metrics.json'))
    st, b = payload(rd4)
    c1 = ((b.get('density') or {}).get('c1') or {})
    chk(f'D3d full_metrics 없음 → 환산 불가 (사유 · 0 으로 채우지 않음) ({c1.get("status")} · {c1.get("reason")})',
        st == 200 and c1.get('status') == 'unavailable' and 'full_metrics' in str(c1.get('reason')) and c1.get('j_1C_A_cm2') is None)


# ══════════════════════════════════════════════════════════════════════════════
#  [D4] σ₀ 출처 사다리
# ══════════════════════════════════════════════════════════════════════════════
def section_sigma0(tmp, bed_rd):
    print('[D4] σ₀ 출처 — 증서 → sigma_grain_S_cm → 게시 mS/cm ÷ σ/σ₀ → 없음')

    def variant(name, edit):
        rd = os.path.join(tmp, name)
        shutil.copytree(bed_rd, rd)
        p = os.path.join(rd, 'network_conductivity_hertzian.json')
        d = json.load(open(p))
        edit(d)
        json.dump(d, open(p, 'w'))
        return rd

    def no_cert(d):
        for k in [k for k in d if k.endswith('solve_certificate_full')]:
            d[k] = {kk: vv for kk, vv in d[k].items() if kk != 'sigma_bulk_S_cm'}
    rd = variant('s0_grain', no_cert)
    _, b = payload(rd)
    den = b.get('density') or {}
    chk(f'D4a 증서에 σ₀ 없음 → 이온 = sigma_grain_S_cm ({den.get("sigma0_S_cm")} · {den.get("sigma0_source")})',
        den.get('sigma0_S_cm') == 0.003 and 'sigma_grain_S_cm' in str(den.get('sigma0_source')))
    _, b = payload(rd, 'electronic')
    den = b.get('density') or {}
    chk(f'D4b 증서에 σ₀ 없음 → 전자 = 게시 mS/cm ÷ (σ/σ₀ × 1000) · 반올림 표지 ({den.get("sigma0_S_cm")} · {den.get("sigma0_source")})',
        den.get('sigma0_S_cm') is not None and rel(den['sigma0_S_cm'], 0.05) < 1e-4 and '반올림' in str(den.get('sigma0_source')))

    def wrong_channel(d):
        c = d.get('solve_certificate_full') or {}
        c['channel'] = 'electronic'
        c['sigma_bulk_S_cm'] = 0.05
        d['solve_certificate_full'] = c
    rd = variant('s0_wrongch', wrong_channel)
    _, b = payload(rd)
    den = b.get('density') or {}
    chk(f'D4c 이온 자리 증서의 채널이 다르면 그 σ₀ 를 쓰지 않는다 → 다음 출처 ({den.get("sigma0_S_cm")} · {den.get("sigma0_source")})',
        den.get('sigma0_S_cm') == 0.003 and 'solve_certificate_full' not in str(den.get('sigma0_source')))
    rd = os.path.join(tmp, 's0_nopub')
    shutil.copytree(bed_rd, rd)
    for n in ('network_conductivity_hertzian.json', 'network_conductivity.json'):
        os.remove(os.path.join(rd, n))
    st, b = payload(rd)
    den = b.get('density') or {}
    E = b.get('edges') or []
    chk(f'D4d 게시 파일 없음 → σ₀ 없음 · j 없음 (지어내지 않는다) · 사유 ({st} · {den.get("sigma0_S_cm")} · {den.get("reason")})',
        st == 200 and den.get('sigma0_S_cm') is None and bool(E) and all(e.get('j') is None for e in E)
        and den.get('j_mean_1V') is None and bool(den.get('reason')))


# ══════════════════════════════════════════════════════════════════════════════
#  [D5] 뷰어 (node)
# ══════════════════════════════════════════════════════════════════════════════
JS_NAMES = ('netCurrentFmtJ', 'netCurrentLogRange', 'netCurrentT', 'netCurrentPct', 'netCurrentTicks', 'netCurrentFrame',
            'netCurrentColorbarSpec', 'netCurrentControlsHtml', 'netCurrentTopOptions', 'netCurrentLegendHtml', 'jeEscH', 'jetColor')


def section_viewer(pay):
    print('[D5] 뷰어 — 전류 밀도 범례 · 두 컬러바 · 눈금 (node)')
    js = open(VIEWER_JS, encoding='utf-8').read()
    parts, miss = [], []
    for n in JS_NAMES:
        try:
            parts.append(js_fn(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    for n in ('NETCUR_CHANNELS', 'NETCUR_MODES'):
        try:
            parts.append(js_const(js, n))
        except (ValueError, AssertionError):
            miss.append(n)
    m_tops = re.search(r'const NETCUR_TOPS = \[[^\]]*\];', js)
    # 10-08 조작판이 쓰는 한 줄 상수 — 굵기 (NETCUR_WIDTHS) · 전류 몫 고르기 (NETCUR_SHARES) · 색 위쪽 (NETCUR_CAPS) (옛 코드엔 없음)
    more = [m.group(0) for m in (re.search(r'const ' + n + r' = [^;]*;', js) for n in ('NETCUR_WIDTHS', 'NETCUR_SHARES', 'NETCUR_CAPS')) if m]
    if not chk(f'D5a viewer3d.js 에서 함수 · 상수를 잘라 냈다 (없음 {miss})', not miss and m_tops is not None):
        return
    if not chk('D5b 경로 자료 (전류 밀도) 가 있다', bool(pay and pay.get('edges') and pay.get('density'))):
        return
    pay = copy.deepcopy(pay)
    pay5 = dict(pay, edges=pay['edges'][:5], top=5, n_returned=5)
    nc1 = copy.deepcopy(pay5)
    nc1['density']['c1'] = {'status': 'unavailable', 'reason': 'full_metrics.json 에 thickness_um 없음 <b>x</b>', 'factor': None}
    script = '\n'.join(parts + [m_tops.group(0)] + more) + '\n' + r"""
const PAY = __PAY__, PAY5 = __PAY5__, NC1 = __NC1__;
const out = {};
out.fmt = [37.0344, 0.0123, 1.5e-5, 2.0e4, 1, 0.5, 999.6, 1e-3, 0.0998, 123.4, 0];
out.fmtS = out.fmt.map(netCurrentFmtJ);
out.range = netCurrentLogRange(PAY.edges);
out.rangeNone = netCurrentLogRange([{j: null}, {j: 0}]);
const r5 = netCurrentLogRange(PAY5.edges) || [0, 1];
out.fr1v = netCurrentFrame(PAY5, '1V');
out.fr1c = netCurrentFrame(PAY5, '1C');
out.frNo = netCurrentFrame(NC1, '1C');
out.ticks = netCurrentTicks(-3, 1, netCurrentFmtJ);
out.ticksNarrow = netCurrentTicks(Math.log10(0.31), Math.log10(1.4), netCurrentFmtJ);
out.spec1v = netCurrentColorbarSpec(PAY5, {channel: 'ionic', mode: 'hertzian', top: 5}, r5[0], r5[1], '1V');
out.spec1c = netCurrentColorbarSpec(PAY5, {channel: 'ionic', mode: 'hertzian', top: 5}, r5[0], r5[1], '1C');
out.spec1cNo = netCurrentColorbarSpec(NC1, {channel: 'ionic', mode: 'hertzian', top: 5}, r5[0], r5[1], '1C');
out.spec1vTicks = (out.spec1v.ticks || []).map(t => t.label);
out.r5 = r5;
const st = {nDrawn: 4, nWrapSkipped: 1, lo: r5[0], hi: r5[1]};
out.leg = netCurrentLegendHtml(PAY5, {channel: 'ionic', mode: 'hertzian', top: 5, arrows: false}, st);
out.legNo = netCurrentLegendHtml(NC1, {channel: 'ionic', mode: 'hertzian', top: 5, arrows: false}, st);
const ph = JSON.parse(JSON.stringify(PAY5)); ph.mode = 'physics'; ph.channel = 'electronic';
out.legPh = netCurrentLegendHtml(ph, {channel: 'electronic', mode: 'physics', top: 5}, st);
const ns = JSON.parse(JSON.stringify(PAY5)); ns.edges.forEach(e => { e.j = null; }); ns.density.sigma0_S_cm = null;
ns.density.j_mean_1V = null; ns.density.reason = '게시 파일 없음 — σ₀ 미확인';
out.legNoSigma = netCurrentLegendHtml(ns, {channel: 'ionic', mode: 'hertzian', top: 5}, {nDrawn: 5, nWrapSkipped: 0, lo: 0, hi: 1});
console.log(JSON.stringify(out));
""".replace('__PAY__', json.dumps(pay, ensure_ascii=False)).replace('__PAY5__', json.dumps(pay5, ensure_ascii=False)) \
        .replace('__NC1__', json.dumps(nc1, ensure_ascii=False))
    res = run_node(script)
    if not chk('D5c node 실행', res is not None):
        return
    chk(f'D5d 눈금 라벨 — 0.01 ≤ v < 1000 은 유효 2 자리 · 그 밖 = m×10ⁿ (지수 · 콤마 없음) {res["fmtS"]}',
        res['fmtS'] == ['37', '0.012', '1.5×10⁻⁵', '2×10⁴', '1', '0.5', '10³', '10⁻³', '0.1', '120', '0'], repr(res['fmtS']))
    jj = [e['j'] for e in pay['edges'] if e.get('j')]
    lo, hi = res['range'] or (None, None)
    chk(f'D5e 색 범위 = 받은 간선 log₁₀ j 최소 · 최대 ({lo} · {hi}) · j 없음 / 0 만이면 null',
        lo is not None and abs(lo - math.log10(min(jj))) < 1e-12 and abs(hi - math.log10(max(jj))) < 1e-12 and res['rangeNone'] is None)
    f = (pay['density'].get('c1') or {}).get('factor')
    chk(f'D5f 틀 — @1V 배율 1 · @1C 배율 = 서버 factor ({res["fr1v"]} · {res["fr1c"]}) · @1C 불가 = ok false + 사유 ({res["frNo"]})',
        res['fr1v'].get('ok') is True and res['fr1v'].get('factor') == 1 and res['fr1c'].get('ok') is True
        and f is not None and abs(res['fr1c'].get('factor') - f) < 1e-15 * max(1.0, f) and res['frNo'].get('ok') is False
        and 'thickness_um' in str(res['frNo'].get('reason')))
    tl = [t['label'] for t in res['ticks']]
    chk(f'D5g 눈금 배치 — 끝 둘 + 안쪽 10 배 간격 · 0..1 ({tl})', tl[0] == '10⁻³' and tl[-1] == '10' and '0.1' in tl
        and all(0 <= t['p'] <= 1 for t in res['ticks']))
    tn = [t['label'] for t in res['ticksNarrow']]
    chk(f'D5h 좁은 범위 (한 자릿수 안) — 끝 둘 + 안쪽 1 · 2 · 5 ({tn})', len(tn) >= 3 and tn[0] == '0.31' and tn[-1] == '1.4' and '1' in tn)
    s1, s2 = res['spec1v'] or {}, res['spec1c'] or {}
    chk('D5i 컬러바 @1V — jet · 감마 없음 · 영문 제목 (Contact current density · A cm⁻² · @1V probe · 채널 · Hertz FULL) · 한정어 (model solve · not measured)',
        s1.get('map') == 'jet' and not s1.get('gamma') and all(x in s1.get('title', '') for x in ('Contact current density', 'A cm⁻²', '@1V', 'ionic', 'Hertz FULL'))
        and 'not a measured current' in s1.get('sub', '') and '|I_c| / A_c' in s1.get('sub', ''), repr(s1)[:400])
    r5 = res['r5']
    lab1c = [t['label'] for t in (s2.get('ticks') or [])]
    chk(f'D5j 컬러바 @1C — 제목 @1C (operating) · 끝 눈금 = @1V 끝 × 배율 ({lab1c[:1]} … {lab1c[-1:]}) · 부제 = 선형 환산 · I_1C · Q_areal · 전류 보존',
        all(x in s2.get('title', '') for x in ('Contact current density', 'A cm⁻²', '@1C'))
        and bool(lab1c) and all(x in s2.get('sub', '') for x in ('I_1C', 'Q_areal', 'linear'))
        and 'conservation' in s2.get('sub', ''), repr(s2)[:400])
    # 끝 눈금 값 = 10^(lo + log10 f) · 10^(hi + log10 f) (node 의 fmt 로 같은 문자열)
    end_ok = False
    if f and lab1c:
        sc = run_node(js_fn(js, 'netCurrentFmtJ') + f'\nconsole.log(JSON.stringify([netCurrentFmtJ(Math.pow(10, {r5[0]}) * {f}), '
                      f'netCurrentFmtJ(Math.pow(10, {r5[1]}) * {f})]));')
        end_ok = sc is not None and lab1c[0] == sc[0] and lab1c[-1] == sc[1]
    chk('D5k @1C 눈금 끝 = netCurrentFmtJ(10^lo × f) · netCurrentFmtJ(10^hi × f) (같은 색 · 다른 숫자)', end_ok)
    sn = res.get('spec1cNo') or {}
    chk('D5k2 @1C 를 못 하는데 @1C 스펙을 부르면 — 제목 = @1V probe · 눈금 = @1V 그대로 · 부제 "@1C unavailable" (@1C 라고 거짓 표기하지 않는다)',
        '@1V probe' in sn.get('title', '') and '@1C (operating)' not in sn.get('title', '') and '@1C unavailable' in sn.get('sub', '')
        and [t['label'] for t in (sn.get('ticks') or [])] == res.get('spec1vTicks'), repr(sn)[:300])
    leg = res['leg']
    chk('D5l 범례 — 접촉 전류 밀도 · A cm⁻² · @1V (탐침) · @1C (운전 환산) 두 줄 · 그릴 접촉 = |I| 큰 순 상위 5',
        all(x in leg for x in ('접촉 전류 밀도', 'A cm⁻²', '@1V', '@1C', '상위 5')) and '|I|' in leg, leg[:500])
    chk('D5m 범례 — 옛 몫 표시 없음 ("전체 전류의 x %" · "log₁₀(|I_간선| / I_전체)" · 몫 눈금)',
        '전체 전류의' not in leg and 'I_전체)' not in leg and '접촉 하나가 나르는 몫' not in leg, leg[:500])
    chk('D5n 범례 — 컬러바 ⬇ 두 개 (id netcur-cbar-1v · netcur-cbar-1c) · 화살표 · 조작 (채널 · top · 모드) · 면적 규약 · σ₀',
        'id="netcur-cbar-1v"' in leg and 'id="netcur-cbar-1c"' in leg and 'id="netcur-arrows"' in leg
        and 'id="netcur-channel"' in leg and 'id="netcur-top"' in leg and 'id="netcur-mode"' in leg
        and 'A_c' in leg and 'σ₀' in leg)
    ln = res['legNo']
    chk('D5o @1C 불가 → 사유 줄 (서버 문자열 이스케이프) · @1C 컬러바 단추 꺼짐',
        '@1C' in ln and 'thickness_um' in ln and '<b>x</b>' not in ln and '&lt;b&gt;x&lt;/b&gt;' in ln
        and re.search(r'id="netcur-cbar-1c"[^>]*disabled', ln) is not None, ln[:600])
    chk('D5p Physics · 전자 범례 = 민감도 · AM–AM · Physics FULL (면적 = 세대 2)', all(x in res['legPh'] for x in ('민감도', 'AM–AM', 'Physics FULL')))
    lns = res['legNoSigma']
    chk('D5q σ₀ 없음 → 전류 밀도 계산 불가 (사유) · 두 컬러바 단추 꺼짐 (몫으로 되돌아가지 않는다)',
        '계산 불가' in lns and 'σ₀ 미확인' in lns and re.search(r'id="netcur-cbar-1v"[^>]*disabled', lns) is not None
        and '전체 전류의' not in lns, lns[:600])
    try:
        wl = js_fn(js, 'netCurrentWireLegend')
    except (ValueError, AssertionError):
        wl = ''
    chk('D5r 컬러바 단추 둘 = exportColorbarPNG(netCurrentColorbarSpec(…, \'1V\' · \'1C\')) · 파일 이름 _1V · _1C',
        "netCurrentColorbarSpec(l.pay, opt, l.st.lo, l.st.hi, '1V')" in wl and "netCurrentColorbarSpec(l.pay, opt, l.st.lo, l.st.hi, '1C')" in wl
        and any(f in wl for f in ("'_1V.png'", "'_1V' + (opt.scale === 'linear' ? '_linear' : '') + '.png'",
                                  "'_1V' + (opt.scale === 'linear' ? '_linear' : '') + netCurrentCapTag(opt) + '.png'"))
        and any(f in wl for f in ("'_1C.png'", "'_1C' + (opt.scale === 'linear' ? '_linear' : '') + '.png'",
                                  "'_1C' + (opt.scale === 'linear' ? '_linear' : '') + netCurrentCapTag(opt) + '.png'")), wl[:400])
    # ↑ 10-08 선형 눈금이면 _linear 꼬리 · 색 위쪽 p99 · p95 면 _p99 · _p95 꼬리 (netCurrentCapTag)
    try:
        rnc = js_fn(js, 'renderNetCurrent')
    except (ValueError, AssertionError):
        rnc = ''
    chk('D5s 그리기 — 색 · 굵기 축 = j (기본 log₁₀ · 10-08 선형 고르기 netCurrentTv(e.j, …, sc)) · 옛 몫 (e.s) 로 칠하지 않는다',
        ('netCurrentT(e.j, lo, hi)' in rnc or 'netCurrentTv(e.j, lo, hi, sc)' in rnc) and 'netCurrentT(e.s' not in rnc
        and 'netCurrentTv(e.s' not in rnc, rnc[:300])


def section_registration():
    print('[D6] check_all 배선')
    s = open(CHECK_ALL, encoding='utf-8').read()
    chk('D6a scripts/check_all.sh 가 이 시험을 돈다', 'webapp/test_net_current_density.py' in s)


def main():
    tmp = tempfile.mkdtemp(prefix='netcur_density_')
    try:
        for k, v in (('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_UPLOAD_FOLDER', 'uploads'),
                     ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
            os.environ[k] = os.path.join(tmp, v)
            os.makedirs(os.environ[k], exist_ok=True)
        try:
            section_analytic(tmp)
        except Exception as e:                                   # noqa: BLE001 — 옛 코드에서도 나머지 절을 돈다
            chk('D1 절 실행', False, f'{type(e).__name__}: {e}')
        bed = None
        try:
            bed = section_identity(tmp)
        except Exception as e:                                   # noqa: BLE001
            chk('D2 절 실행', False, f'{type(e).__name__}: {e}')
        pay = {}
        if bed:
            for fn in (section_c1, section_sigma0):
                try:
                    fn(tmp, bed)
                except Exception as e:                           # noqa: BLE001
                    chk(f'{fn.__name__} 절 실행', False, f'{type(e).__name__}: {e}')
            try:
                st, pay = payload(bed, 'ionic', 'hertzian', top=100000)
            except Exception as e:                               # noqa: BLE001
                chk('D5 자료', False, f'{type(e).__name__}: {e}')
        section_viewer(pay)
        section_registration()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print()
    print(f'{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        print('FAIL — ' + ' | '.join(_fail))
        return 1
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
