#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""① 계면 저항 **요청 ↔ 적용 영수증** 통합 시험 — Codex r_int 1단계 `RINT-02` · `13` · `14` · `20` (10-03 · 1저자 비준 G1).

Codex 변이 탐침: 실제 producer 에서 **주 전자 솔브의 `rint=` 만** 지우면 σ_e 는 OFF 와 비트 동일인데 CLI 기록
(model = r1) 은 남아 규칙 J 사후 단언이 PASS 했다.  wetted 호출만 지우면 주 σ · 면 · 표는 그대로라 "주 솔브 ON
시험" 도 통과하는데 wetted σ 0.0009487 → 0.0009606 · R_geom 0 → 0.0544 Ω·cm² 로 바뀐다.  ⇒ 네 솔브 각각의
**실제 적용 영수증**을 독립 보존한 요청 표에 대조하고 (`run_contract.interface_record_ok`), 그 계약을 producer
(발행 전) · `check_arm` · 최종 판정기가 같이 쓴다.  이 시험은 그 배선이 **실물에서** 무는지 본다.

  A  실물 producer — OFF · 전자 ON (집전체 포함) · 이온 ON 이 exit 0 · 계약 통과 · 영수증 상태가 기대대로
  B  AST 변이 — `solve_sigma_z(..., rint=...)` 호출 넷을 AST 로 찾아 **하나씩** `rint=` 를 지우면 producer 가
     게시를 거부한다 (exit 4 · `.failed` · 사유 `STEP3_INTERFACE` 에 그 솔브 이름)
  C  CLI 모순 요청 — 빈 `--step3-rint-e` · 반복 플래그 사이의 같은 쌍 · `--step3-rint-i` + `--no-ion` ·
     `--no-step3` · 이 채널 σ 에서 절연인 상 (`AM_S|SE` 전자) 은 GPU 작업 전에 죽는다
  D  소비자 — 정상 ON 산출물의 영수증을 하나씩 변조하면 `check_arm` 이 거부한다 (원본은 받아들인다)
  E  레지스트리 (RINT-20) — 실물 producer 매니페스트 키가 판정기 레지스트리에 **전부** 분류돼 있다
     (`manifest_unswept_keys` = 빈 목록) · OFF ↔ ON 비교에서 `interface_model` 은 표의 파생이라 HOLD 사유가 아니다
  F  G1-3 — r-ON 이면 반응 솔브 비활성 (RINT-05) · r-ON + --save-step4-grid 거부 (C) · Joule 요약 = bulk_only ·
     지도 밖 계면 몫 (RINT-04) · r = 0 표는 OFF 와 σ_e · n_dof · 입자 je 비트 동일 (Codex G1-5 OFF/zero 회귀)
  G  RGL-01 (Codex 10-05 · P1) — **적용 영수증은 수렴 증명이 아니다.**  실물 producer 를 돌리되 보조 (wetted · bare)
     또는 주 솔브 **한 호출 동안만** CG 를 프로세스 안에서 제한 (CG_MAXITER=1 · 또는 info=0 + NaN 해 주입 · 즉시 원복) —
     결과 수치는 손으로 만들지 않는다 (SELF-86).  r-OFF · r-ON 둘 다:
       · 정상 = 보조 두 솔브의 수렴 3필드가 실리고 collector complete · R_geom · jb 게시
       · wetted 만 · bare 만 미수렴 = 게시 거부 (exit 3 · `collector_geom(unconverged)`) · 진단본에 R_geom None · jb 없음 ·
         주 σ_e 는 정상 런과 비트 동일 · r-ON 영수증은 여전히 applied (적용 ≠ 수렴 — 의미 분리)
       · 비유한 잔차 (info 0 + NaN) = 미수렴 (step3 술어) · 주 솔브만 미수렴 = 기존대로 exit 3 (대조)
       · `--allow-partial-step3` 게시본 = collector unconverged · R_geom None · jb 없음 → check_arm 거부
       · 소비자 — 정상 산출물의 보조 수렴 3필드를 변조 (미수렴 · 누락 · 상충 · NaN · Inf · 문턱 위) 하면 check_arm 거부

  python3 scripts/test_rint_receipts.py
"""
import ast
import copy
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, 'scripts')
PAY = os.path.join(SCRIPTS, 'mpm_webapp_payload.py')
sys.path.insert(0, SCRIPTS)

_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))
    return cond


def rint_call_sites(src):
    """payload 소스 → `[(대입 대상 이름, 줄)]` — `solve_sigma_z(..., rint=...)` 호출 전수 (AST)."""
    tree = ast.parse(src)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            c = node.value
            f = c.func
            if isinstance(f, ast.Attribute) and f.attr == 'solve_sigma_z' \
                    and any(k.arg == 'rint' for k in c.keywords):
                tgt = node.targets[0]
                out.append((tgt.id if isinstance(tgt, ast.Name) else ast.dump(tgt), c.lineno))
    return sorted(out, key=lambda x: x[1])


def mutant_child(target):
    """`target` 에 대입하는 solve_sigma_z 호출 하나에서만 `rint=` 키워드를 지우고 producer 를 돈다."""
    import mpm_webapp_payload as payload
    with open(PAY, encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=PAY)
    hit = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) \
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id == target:
            c = node.value
            if isinstance(c.func, ast.Attribute) and c.func.attr == 'solve_sigma_z':
                n0 = len(c.keywords)
                c.keywords = [k for k in c.keywords if k.arg != 'rint']
                hit += (n0 - len(c.keywords))
    assert hit == 1, f'변이 대상 {target} 의 rint 키워드가 정확히 하나가 아니다 ({hit})'
    exec(compile(tree, PAY, 'exec'), payload.__dict__)
    payload.main()


#: RGL-01 — CG 를 제한할 솔브 (producer 호출 자리).  주 = 첫 `solve_sigma_z` (bot_allowed 없음) ·
#  wetted = bot_allowed 있고 return_field=False · bare = bot_allowed 있고 return_field=True (`mpm_webapp_payload.py`).
CGCAP_TARGETS = ('main', 'wetted', 'bare')


def cgcap_child(target, mode):
    """`target` 솔브 **한 호출 동안만** CG 를 망가뜨리고 (프로세스 안 · 호출 직후 원복) 실물 producer 를 돈다 (RGL-01).

    mode 'maxiter' = `CG_MAXITER = 1` (Codex 반례 그대로) · 'nan' = `_solve_cg` 가 NaN 해를 info 0 으로 돌려준다
    (비유한 잔차 술어 반례 — 과거 런에 NaN 이 있었다는 증거가 아니다).  σ · 잔차 · 영수증은 솔버가 낸 그대로다.
    끝에 `CGCAP {...}` 한 줄 = 제한한 호출 수와 그 호출의 솔버 기록 (부모가 주입이 정말 일어났는지 본다)."""
    import numpy as np
    import step3_sigma as S3
    import mpm_webapp_payload as payload
    orig = S3.solve_sigma_z
    seen = {'main': 0, 'wetted': 0, 'bare': 0}
    hit = {'n': 0, 'rec': None}

    def which(kw):
        if kw.get('bot_allowed') is None:
            return 'main' if seen['main'] == 0 else None    # 첫 호출만 주 솔브 (이온 등 뒤 호출은 대상 밖)
        return 'bare' if kw.get('return_field') else 'wetted'

    def wrapper(*args, **kw):
        w = which(kw)
        if w is not None:
            seen[w] += 1
        if w != target:
            return orig(*args, **kw)
        hit['n'] += 1
        old_it, old_cg = S3.CG_MAXITER, S3._solve_cg
        if mode == 'maxiter':
            S3.CG_MAXITER = 1
        else:
            S3._solve_cg = lambda L, b: (np.full(len(b), np.nan), 0)
        try:
            r = orig(*args, **kw)
        finally:
            S3.CG_MAXITER, S3._solve_cg = old_it, old_cg
        hit['rec'] = {k: (None if r.get(k) is None else
                          (float(r[k]) if isinstance(r[k], float) else r[k]))
                      for k in ('sigma_eff', 'cg_info', 'resid', 'unconverged')}
        return r

    S3.solve_sigma_z = wrapper
    try:
        payload.main()
    finally:
        print('CGCAP ' + json.dumps({'target': target, 'mode': mode, 'hits': hit['n'], 'seen': seen,
                                     'rec': hit['rec']}, allow_nan=True), flush=True)


def cgcap_record(log):
    """child 로그 → 마지막 `CGCAP` 기록 (없으면 None)."""
    for ln in reversed((log or '').splitlines()):
        if ln.startswith('CGCAP '):
            try:
                return json.loads(ln[6:])
            except ValueError:
                return None
    return None


def run_payload(args, cwd, mutant=None, timeout=900, cgcap=None):
    if mutant:
        cmd = [sys.executable, os.path.abspath(__file__), '--mutant-child', mutant, '--', *args]
    elif cgcap:
        cmd = [sys.executable, os.path.abspath(__file__), '--cgcap-child', cgcap[0], cgcap[1], '--', *args]
    else:
        cmd = [sys.executable, PAY, *args]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd,
                       stdin=subprocess.DEVNULL)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


#: RGL-01 — 보조 두 솔브의 수렴 3필드 (producer `collector_geometric` 키 = run_contract 계약 키).
AUX_CONV_KEYS = {'wetted': ('wetted_cg_info', 'wetted_unconverged', 'wetted_cg_resid'),
                 'bare': ('bare_cg_info', 'bare_unconverged', 'bare_cg_resid')}


def check_arm_rc(path, stamp, cwd):
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, 'sr01_stamp_compare.py'), '--check-arm', path,
                        '--stamp', stamp], capture_output=True, text=True, timeout=300, cwd=cwd,
                       stdin=subprocess.DEVNULL)
    return r.returncode, (r.stdout or '') + (r.stderr or '')


def load_manifest(path):
    with open(path, encoding='utf-8') as f:
        p = json.load(f)
    s3 = (p.get('mpm_metrics') or {}).get('step3') or {}
    return p, s3, (s3.get('manifest') or {})


def rgl01_section(d, runs, res, RC):
    """G — RGL-01: 보조 (wetted · bare) collector 솔브의 **수렴**이 게시 · 소비 계약에 들어갔는가 (실물 producer)."""
    print('G  RGL-01 — 보조 솔브 수렴 (적용 영수증 ≠ 수렴) · r-OFF · r-ON · 실물 producer + check_arm')

    def aux_conv(cg, which):
        ki, ku, kr = AUX_CONV_KEYS[which]
        return RC.conv_ok(cg.get(ki), cg.get(ku), cg.get(kr))

    # G0 정상 대조 — A 의 실물 산출 (r-OFF = off · r-ON = e_on).  보조 수렴 3필드 · complete · R_geom · jb 가 함께 있다.
    norm = {}
    for k in ('off', 'e_on'):
        rc0, _, out0 = res.get(k, (1, '', ''))
        if not (rc0 == 0 and out0 and os.path.exists(out0)):
            chk(f'G0 {k}: A 산출물이 있어야 정상 대조를 돈다', False)
            continue
        p0, s0, m0 = load_manifest(out0)
        cg0 = s0.get('collector_geometric') or {}
        st0 = ((m0.get('components') or {}).get('collector_geom') or {}).get('status')
        norm[k] = (p0, s0, m0)
        chk(f'G0 {k}: 보조 두 솔브의 수렴 3필드가 실리고 각각 계약 통과 · collector complete · R_geom 수 · 입자 jb 있음',
            all(kk in cg0 for kk in AUX_CONV_KEYS['wetted'] + AUX_CONV_KEYS['bare'])
            and aux_conv(cg0, 'wetted')[0] and aux_conv(cg0, 'bare')[0] and st0 == 'complete'
            and isinstance(cg0.get('R_geom_ohm_cm2'), (int, float))
            and any('jb' in q for q in (p0.get('particles') or [])),
            f'status={st0} keys={sorted(cg0)} R_geom={cg0.get("R_geom_ohm_cm2")!r}')

    # G1–G6 — 실물 producer 에 CG 제한을 한 호출만 심는다
    cases = [('G1', 'off', 'wetted', 'maxiter'), ('G2', 'off', 'bare', 'maxiter'),
             ('G3', 'e_on', 'wetted', 'maxiter'), ('G4', 'e_on', 'bare', 'maxiter'),
             ('G6', 'off', 'wetted', 'nan')]
    for tag, k, tgt, mode in cases:
        out = os.path.join(d, f'rgl01_{tag}.json')
        rc, log = run_payload(runs[k] + ['--out', out], d, cgcap=(tgt, mode))
        cap = cgcap_record(log) or {}
        lbl = f'{tag} {k} · {tgt} {mode}'
        chk(f'{lbl}: 주입이 그 호출 하나에만 일어났다 (hits 1)', cap.get('hits') == 1, repr(cap)[:200])
        if mode == 'maxiter':
            rec = cap.get('rec') or {}
            chk(f'{lbl}: 제한한 솔브가 실제로 미수렴 (cg_info > 0 · unconverged True — 솔버가 낸 그대로)',
                (rec.get('cg_info') or 0) > 0 and rec.get('unconverged') is True, repr(rec))
        chk(f'{lbl}: 게시 거부 — exit 3 · 최종 파일 없음 · .failed 있음 · STEP3_REQUIRED_INCOMPLETE · collector_geom(unconverged)',
            rc == 3 and not os.path.exists(out) and os.path.exists(out + '.failed')
            and 'STEP3_REQUIRED_INCOMPLETE' in log and 'collector_geom(unconverged)' in log,
            f'rc={rc} {log.strip()[-300:]}')
        if not os.path.exists(out + '.failed'):
            continue
        pf, sf, mf = load_manifest(out + '.failed')
        cgf = sf.get('collector_geometric') or {}
        cvt, cvo = aux_conv(cgf, tgt), aux_conv(cgf, 'bare' if tgt == 'wetted' else 'wetted')
        chk(f'{lbl}: 진단본 — R_geom None · 입자 jb 없음 · 제한한 쪽만 수렴 계약 실패 · 다른 쪽은 통과',
            cgf.get('R_geom_ohm_cm2') is None and not any('jb' in q for q in (pf.get('particles') or []))
            and not cvt[0] and cvo[0],
            f'R_geom={cgf.get("R_geom_ohm_cm2")!r} conv {tgt}={cvt} other={cvo}')
        if mode == 'nan':
            ku = AUX_CONV_KEYS[tgt][1]
            chk(f'{lbl}: info 0 + 비유한 잔차를 솔버가 미수렴으로 적는다 ({ku} True — step3 경고 술어)',
                cgf.get(ku) is True and 'STEP3 CG not converged' in log, repr({kk: cgf.get(kk) for kk in AUX_CONV_KEYS[tgt]}))
        if k in norm:
            _, s0, _ = norm[k]
            chk(f'{lbl}: 주 솔브는 그대로 — 주 σ_e 가 정상 런과 비트 동일 · 주 수렴 계약 통과',
                sf.get('sigma_e_eff_S_cm') == s0.get('sigma_e_eff_S_cm')
                and RC.conv_ok(sf.get('cg_info'), sf.get('unconverged'), sf.get('cg_resid'))[0],
                f'{sf.get("sigma_e_eff_S_cm")!r} vs {s0.get("sigma_e_eff_S_cm")!r}')
        if k == 'e_on':
            rw = (mf.get('interface_receipts') or {}).get(f'electronic_{tgt}') or {}
            chk(f'{lbl}: 적용 영수증은 여전히 applied · 계면 계약 통과 (적용 ≠ 수렴 — 의미 분리)',
                rw.get('status') == 'applied' and RC.interface_record_ok(mf)[0], repr(rw)[:200])

    # G5 대조 — 주 솔브만 미수렴은 기존 차단 그대로 (exit 3 · electronic(unconverged))
    out5 = os.path.join(d, 'rgl01_G5.json')
    rc5, log5 = run_payload(runs['e_on'] + ['--out', out5], d, cgcap=('main', 'maxiter'))
    chk('G5 e_on · main maxiter (대조): exit 3 · 최종 파일 없음 · electronic(unconverged)',
        rc5 == 3 and not os.path.exists(out5) and 'electronic(unconverged)' in log5
        and (cgcap_record(log5) or {}).get('hits') == 1, f'rc={rc5} {log5.strip()[-240:]}')

    # G7 `--allow-partial-step3` — 미완 collector 를 연 게시본은 R_geom · jb 없이 unconverged 로 서고, 소비자가 거부한다
    out7 = os.path.join(d, 'rgl01_G7.json')
    rc7, log7 = run_payload(runs['off'] + ['--allow-partial-step3', '--out', out7], d, cgcap=('bare', 'maxiter'))
    if chk('G7 off · bare maxiter · --allow-partial-step3: exit 0 · 게시됨', rc7 == 0 and os.path.exists(out7),
           f'rc={rc7} {log7.strip()[-240:]}'):
        p7, s7, m7 = load_manifest(out7)
        cg7 = s7.get('collector_geometric') or {}
        st7 = ((m7.get('components') or {}).get('collector_geom') or {}).get('status')
        chk('G7 게시본: collector_geom = unconverged · R_geom None · 입자 jb 없음',
            st7 == 'unconverged' and cg7.get('R_geom_ohm_cm2') is None
            and not any('jb' in q for q in (p7.get('particles') or [])), f'status={st7} R_geom={cg7.get("R_geom_ohm_cm2")!r}')
        rca, loga = check_arm_rc(out7, m7.get('fibre_stamp') or 'point', d)
        chk('G7 check_arm 이 그 게시본을 거부 (재사용 금지)', rca != 0, f'rc={rca} {loga.strip()[-200:]}')

    # G8 소비자 — 정상 산출물 (r-ON e_on · r-OFF off) 의 보조 수렴 3필드를 변조하면 check_arm 이 거부 · 원본은 통과
    for k in ('e_on', 'off'):
        if k not in norm:
            continue
        good = res[k][2]
        p0, _, m0 = norm[k]
        stamp = m0.get('fibre_stamp') or 'point'
        rcg, logg = check_arm_rc(good, stamp, d)
        chk(f'G8 {k}: 원본은 check_arm 통과 (정상 대조)', rcg == 0, logg.strip()[-200:])
        muts = {
            'wetted 미수렴 (cg_info 1 · unconverged True · resid 0.35)':
                {'wetted_cg_info': 1, 'wetted_unconverged': True, 'wetted_cg_resid': 0.35},
            'bare 미수렴 (cg_info 1 · unconverged True · resid 0.35)':
                {'bare_cg_info': 1, 'bare_unconverged': True, 'bare_cg_resid': 0.35},
            'bare 잔차 누락': {'bare_cg_resid': '__pop__'},
            'wetted 3필드 통째 누락': {kk: '__pop__' for kk in AUX_CONV_KEYS['wetted']},
            '상충 (bare cg_info 3 인데 unconverged False)': {'bare_cg_info': 3},
            'wetted 잔차 NaN': {'wetted_cg_resid': float('nan')},
            'bare 잔차 Inf': {'bare_cg_resid': float('inf')},
            'wetted 잔차 문턱 위 (1e-3 · 플래그는 수렴)': {'wetted_cg_resid': 1e-3},
            'bare cg_info 가 bool (타입)': {'bare_cg_info': False},
        }
        for lbl, mut in muts.items():
            p = copy.deepcopy(p0)
            cgm = p['mpm_metrics']['step3'].setdefault('collector_geometric', {})
            for kk, vv in mut.items():
                if vv == '__pop__':
                    cgm.pop(kk, None)
                else:
                    cgm[kk] = vv
            t = os.path.join(d, 'rgl01_tamper.json')
            with open(t, 'w', encoding='utf-8') as f:
                json.dump(p, f)                                   # NaN · Inf 토큰 그대로 (json.load 가 읽는다)
            rct, logt = check_arm_rc(t, stamp, d)
            chk(f'G8 {k}: {lbl} → check_arm 거부 (collector_geom 수렴 증거)',
                rct != 0 and 'collector_geom' in logt and 'conv' in logt, f'rc={rct} {logt.strip()[-200:]}')


def main():
    import check_method_discipline as cmd_
    import run_contract as RC
    import sdcp_gain_verdict as SGV
    with open(PAY, encoding='utf-8') as f:
        src = f.read()
    sites = rint_call_sites(src)
    names = [s[0] for s in sites]
    print('A0 호출 자리 (AST):', sites)
    chk('A0 rint 를 받는 solve_sigma_z 호출이 정확히 넷 (주 · wetted · bare · 이온)',
        names == ['_res3', '_res3w', '_res3b', '_res3i'], repr(names))

    with tempfile.TemporaryDirectory() as d:
        am, se, ph, fid, dia = cmd_._smoke_fixture(d)
        base = ['--scaffold', am, '--se', se, '--phase', ph, '--fibre', fid, '--fibre-dia', dia,
                '--n-vox', cmd_._SMOKE_NVOX, '--step3-vox', cmd_._SMOKE_VOX,
                '--no-pore', '--no-thermal', '--no-trackb', '--no-field', '--no-step4']
        e_on = ['--step3-rint-e', 'AM_S|AM_S=0.001', 'AM_S|VGCF=0.002']
        i_on = ['--step3-rint-i', 'SDCP|SE=0.001']
        runs = {
            'off':   base + ['--no-ion'],
            'e_on':  base + ['--no-ion'] + e_on,
            'ei_on': base + e_on + i_on,
        }
        res = {}
        print('A  실물 producer (OFF · 전자 ON · 전자+이온 ON)')
        for k, args in runs.items():
            out = os.path.join(d, f'{k}.json')
            rc, log = run_payload(args + ['--out', out], d)
            res[k] = (rc, log, out)
            if not chk(f'A1 {k}: exit 0 · 산출물 있음', rc == 0 and os.path.exists(out),
                       f'rc={rc} {log.strip()[-300:]}'):
                continue
            _, s3, man = load_manifest(out)
            ok, why = RC.interface_record_ok(man)
            chk(f'A2 {k}: 계면 계약 통과', ok, why)
            rcpt = man.get('interface_receipts') or {}
            chk(f'A3 {k}: 네 솔브 영수증', sorted(rcpt) == sorted(RC.INTERFACE_SOLVES), repr(sorted(rcpt)))
            st = {n: (rcpt.get(n) or {}).get('status') for n in RC.INTERFACE_SOLVES}
            if k == 'off':
                chk('A4 off: 전부 not_requested · model None',
                    set(st.values()) == {'not_requested'} and man.get('interface_model') is None, repr(st))
            elif k == 'e_on':
                chk('A4 e_on: 주 · wetted · bare = applied (면 > 0) · 이온 = not_requested',
                    st['electronic_main'] == st['electronic_wetted'] == st['electronic_bare'] == 'applied'
                    and st['ionic'] == 'not_requested', repr(st))
            else:
                chk('A4 ei_on: 이온 영수증이 요청 표를 받았다 (applied · absent_geometry · failed 중 하나)',
                    st['ionic'] in ('applied', 'absent_geometry', 'failed')
                    and (rcpt['ionic'].get('table') == man.get('interface_rint_i_ohm_cm2')), repr(rcpt.get('ionic')))
            print(f'      {k}: σ_e={s3.get("sigma_e_eff_S_cm")} 영수증 {st}')

        print('B  AST 변이 — 호출 하나씩 rint= 삭제 → 게시 거부')
        _mut_args = {'_res3': runs['e_on'], '_res3w': runs['e_on'], '_res3b': runs['e_on'], '_res3i': runs['ei_on']}
        _mut_name = {'_res3': 'electronic_main', '_res3w': 'electronic_wetted',
                     '_res3b': 'electronic_bare', '_res3i': 'ionic'}
        for tgt in names:
            out = os.path.join(d, f'mut{tgt}.json')
            rc, log = run_payload(_mut_args[tgt] + ['--out', out], d, mutant=tgt)
            chk(f'B1 변이 {tgt}: exit 4 · 최종 파일 없음 · .failed 있음',
                rc == 4 and not os.path.exists(out) and os.path.exists(out + '.failed'),
                f'rc={rc} {log.strip()[-240:]}')
            chk(f'B2 변이 {tgt}: 사유 STEP3_INTERFACE · {_mut_name[tgt]}',
                'STEP3_INTERFACE' in log and _mut_name[tgt] in log, log.strip()[-240:])

        print('C  CLI 모순 요청 — GPU 작업 전에 죽는다')
        bad = {
            '빈 --step3-rint-e': base + ['--no-ion', '--step3-rint-e'],
            '반복 플래그 사이 같은 쌍': base + ['--no-ion', '--step3-rint-e', 'AM_S|VGCF=1e-3',
                                      '--step3-rint-e', 'VGCF|AM_S=2e-3'],
            '--step3-rint-i + --no-ion': base + ['--no-ion'] + i_on,
            '--no-step3': base + ['--no-ion', '--no-step3'] + e_on,
            '절연 상 쌍 (AM_S|SE 전자)': base + ['--no-ion', '--step3-rint-e', 'AM_S|SE=1e-3'],
            '절연 상 쌍 (AM_S|SE 이온)': base + ['--step3-rint-i', 'AM_S|SE=1e-3'],
            #  ★ G1-3 (RINT-05) — STEP4 는 계면 막을 받지 않는다 → r-ON 그리드 저장은 다른 물리를 한 모델처럼 낸다
            'r-ON + --save-step4-grid': [x for x in base if x != '--no-step4'] + ['--no-ion'] + e_on
                                        + ['--save-step4-grid', os.path.join(d, 'g.npz')],
        }
        for lbl, args in bad.items():
            out = os.path.join(d, 'bad.json')
            rc, log = run_payload(args + ['--out', out], d, timeout=300)
            #  'STEP3: voxelizing' = 격자 작업의 첫 표지 — 그 전에 죽어야 GPU · 시간을 안 쓴다
            chk(f'C1 {lbl}: 거부 (exit ≠ 0 · 산출물 없음 · 격자 작업 전)',
                rc != 0 and not os.path.exists(out) and 'STEP3: voxelizing' not in log,
                f'rc={rc} {log.strip()[-200:]}')

        print('D  소비자 — 영수증 변조를 check_arm 이 거부한다')
        good = res.get('e_on', (1, '', ''))[2]
        if os.path.exists(good):
            chk_arm = os.path.join(SCRIPTS, 'sr01_stamp_compare.py')

            _stamp = (load_manifest(good)[2].get('fibre_stamp') or 'point')   # 실물 도장 그대로 (손으로 적지 않는다)

            def arm_rc(path):
                r = subprocess.run([sys.executable, chk_arm, '--check-arm', path, '--stamp', _stamp],
                                   capture_output=True, text=True, timeout=300, cwd=d, stdin=subprocess.DEVNULL)
                return r.returncode, (r.stdout or '') + (r.stderr or '')
            rc0, log0 = arm_rc(good)
            chk('D0 원본 ON 산출물은 check_arm 이 받아들인다', rc0 == 0, log0.strip()[-200:])
            p0, _, _ = load_manifest(good)

            def tamper(fn, lbl):
                p = copy.deepcopy(p0)
                fn(p['mpm_metrics']['step3']['manifest'])
                t = os.path.join(d, 'tamper.json')
                with open(t, 'w', encoding='utf-8') as f:
                    json.dump(p, f)
                rc, log = arm_rc(t)
                chk(f'D1 {lbl}: check_arm 거부', rc != 0 and 'IFACE' in log, f'rc={rc} {log.strip()[-200:]}')
            tamper(lambda m: m['interface_receipts'].__setitem__('electronic_wetted', {'status': 'not_requested'}),
                   'wetted 영수증을 not_requested 로')
            tamper(lambda m: m['interface_receipts']['electronic_bare'].__setitem__('table', {'AM_S|AM_S': 0.001}),
                   'bare 영수증 표를 요청과 다르게')
            tamper(lambda m: m.__setitem__('interface_model', None), 'model 을 None 으로 (표는 그대로)')
            tamper(lambda m: m.pop('interface_receipts'), '영수증 통째로 삭제')
            tamper(lambda m: m['interface_receipts']['electronic_main'].__setitem__('n_faces_rint', 0),
                   '주 영수증 면 수를 0 으로 (쌍별 합과 모순)')
        else:
            chk('D0 e_on 산출물이 있어야 소비자 시험을 돈다', False)

        print('F  G1-3 — 반응 솔브 r-ON 비활성 (RINT-05) · Joule bulk-only 범위 (RINT-04) · OFF ↔ r=0 비트 동일')
        nofld = [x for x in base if x not in ('--no-step4', '--no-field')]
        more = {
            'rxn_off': [x for x in base if x != '--no-step4'] + ['--no-ion'],
            'rxn_on': [x for x in base if x != '--no-step4'] + ['--no-ion'] + e_on,
            'joule_on': nofld + ['--no-step4', '--no-ion', '--joule-heat'] + e_on,
            'e_zero': base + ['--no-ion', '--step3-rint-e', 'AM_S|VGCF=0'],
        }
        for k, args in more.items():
            out = os.path.join(d, f'{k}.json')
            rc, log = run_payload(args + ['--out', out], d)
            res[k] = (rc, log, out)
            chk(f'F0 {k}: exit 0 · 산출물 있음', rc == 0 and os.path.exists(out), f'rc={rc} {log.strip()[-240:]}')
        if all(res[k][0] == 0 for k in more):
            p_roff, s_roff, _ = load_manifest(res['rxn_off'][2])
            p_ron, s_ron, _ = load_manifest(res['rxn_on'][2])
            rx_off, rx_on = s_roff.get('rxn') or {}, s_ron.get('rxn') or {}
            print(f'      rxn_off: {dict((k, rx_off.get(k)) for k in ("n_bv_faces", "active_am_pct", "status"))}')
            #  ⚠ 이 픽스처는 SE 망이 판에 안 닿아 반응 솔브가 원래 `missing_network` 로 건너뛴다 (양성 대조 불가) —
            #    여기서는 **r_int 때문에 꺼지지 않는다** 만 본다 (끄는 것은 r-ON 에서만).
            chk('F1 r 없음 → 반응 솔브가 r_int 사유로 꺼지지 않는다', rx_off.get('status') != 'disabled', repr(rx_off)[:200])
            chk('F2 r-ON → 반응 솔브 비활성 · 사유 RINT-05 · 입자 jrxn 없음',
                rx_on.get('status') == 'disabled' and 'RINT-05' in str(rx_on.get('reason'))
                and not any('jrxn' in q for q in (p_ron.get('particles') or [])), repr(rx_on)[:200])
            _, s_j, m_j = load_manifest(res['joule_on'][2])
            jo = s_j.get('joule') or {}
            ish = (s_j.get('dissipation_share') or {}).get('interface')
            print(f'      joule_on: scope={jo.get("scope")} · 지도 밖 계면 몫={jo.get("interface_share_outside_map")} · 분담 interface={ish}')
            chk('F3 Joule 요약 = bulk_only · 제외 = 계면 I²R · 판 결합 · 지도 밖 계면 몫 = 소산 분담의 interface (> 0)',
                jo.get('scope') == 'bulk_only' and set(jo.get('excluded') or ()) >= {'interface_I2R', 'plate_coupling'}
                and isinstance(ish, (int, float)) and ish > 0 and jo.get('interface_share_outside_map') == ish,
                repr(jo)[:240])
            p_o, s_o, _ = load_manifest(res['off'][2])
            p_z, s_z, m_z = load_manifest(res['e_zero'][2])
            st_z = (m_z.get('interface_receipts') or {}).get('electronic_main', {}).get('status')
            je_o = [q.get('je') for q in (p_o.get('particles') or [])]
            je_z = [q.get('je') for q in (p_z.get('particles') or [])]
            chk('F4 r = 0 표 → 영수증 zero_table · σ_e · n_dof · 입자 je 가 OFF 와 **비트 동일** (OFF/zero 회귀)',
                st_z == 'zero_table' and s_z.get('sigma_e_eff_S_cm') == s_o.get('sigma_e_eff_S_cm')
                and s_z.get('n_dof') == s_o.get('n_dof') and je_o == je_z and len(je_o) > 0,
                f'{st_z} σ {s_z.get("sigma_e_eff_S_cm")!r} vs {s_o.get("sigma_e_eff_S_cm")!r}')

        print('E  레지스트리 — 실물 매니페스트 키 전수 분류 (RINT-20) · 파생 model (RINT-13)')
        for k in ('off', 'e_on', 'ei_on', 'rxn_on', 'joule_on', 'e_zero'):
            out = res.get(k, (1, '', ''))[2]
            if out and os.path.exists(out):
                _, _, man = load_manifest(out)
                left = SGV.manifest_unswept_keys(man, man)
                chk(f'E1 {k}: 분류 안 된 매니페스트 키 없음', left == [], repr(left))
        fc = SGV.FIELD_CONTRACT.get('interface_model') or {}
        chk('E2 interface_model 은 계면 표 두 축의 파생 (derived_from)',
            tuple(fc.get('derived_from') or ()) == ('interface_rint_e_ohm_cm2', 'interface_rint_i_ohm_cm2'),
            repr(fc))

        rgl01_section(d, runs, res, RC)

    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for n in _fail:
            print('  -', n)
        sys.exit(1)


if __name__ == '__main__':
    if '--mutant-child' in sys.argv:
        i = sys.argv.index('--mutant-child')
        target = sys.argv[i + 1]
        j = sys.argv.index('--')
        sys.argv = [PAY] + sys.argv[j + 1:]
        mutant_child(target)
        raise SystemExit(0)
    if '--cgcap-child' in sys.argv:
        i = sys.argv.index('--cgcap-child')
        target, mode = sys.argv[i + 1], sys.argv[i + 2]
        assert target in CGCAP_TARGETS and mode in ('maxiter', 'nan'), (target, mode)
        j = sys.argv.index('--')
        sys.argv = [PAY] + sys.argv[j + 1:]
        cgcap_child(target, mode)
        raise SystemExit(0)
    main()
