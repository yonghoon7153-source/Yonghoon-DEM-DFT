"""Rint ② PC8 고침 변이 (11-04 · 사전 공격 8 회차 · 1저자 11-04 "다 권고대로") — 고친 트리 사본 (git 없는 사본) 에서 한 번에 변이 하나 · 그 가드를 끄면
새 시험이 옳은 이유로 실패하는지 (죽음 = rc ≠ 0) 본다 · 매번 원 바이트로 되돌린다.  변이 = 고친 코드의 줄 (mutate8.py 의 옛 줄이 사라진 자리 = 같은 뜻의
변이 ≈M.. 표지) · 옛 줄이 그대로인 mutate8 변이는 mutate8.py 가 그대로 돈다.

  python3 -I mutate_pc8fix.py <사본 트리> <출력.json> [변이 이름 쉼표]
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

MT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
SEL = set(sys.argv[3].split(',')) if len(sys.argv) > 3 and sys.argv[3] else None
RRF = 'scripts/rint_r_chain.py'
CJF = 'scripts/carbon_junction.py'


def T(only):
    return [['scripts/test_rint_r_chain.py', '--only', only]]


QUAL_NEW = ("    '(접점 저항 분포 미검증 · 전달 길이 = 해석 시험 통과 (분산판 = 이산 전송선 · Banerjee 식 8) 는 같은 두 곧은 나란한 레일 (축 정렬 · 이웃 셀 · '\n"
            "    'R̄sh2 = 1 · L_c = L_par 정수배 · 시험 BAN8) 에서만 — 계단 · 기운 섬유 · R̄sh2 ≠ 1 = 생산 경로 미시험 · 실침대 L_c 대조는 R 보정 뒤) · k 가 바뀌는 '\n"
            "    'L_c/L_par 정수 경계에서 σ 가 계단으로 뛴다 (이산화 오차 · 크기 ∝ h·r′/R_j)',\n")
QUAL_OLD = ("    '(접점 저항 분포 미검증 · 전달 길이 = 해석 시험 통과 (분산판 = 전송선 · 식 검증) · 실침대 L_c 대조는 R 보정 뒤) · k 가 바뀌는 L_c/L_par 정수 경계에서 "
            "σ 가 계단으로 뛴다 (이산화 오차 · 크기 ∝ h·r′/R_j)',\n")

# (이름, 고친 결함, [(파일, 옛 글, 새 글) …], [시험 argv …], 잡아야 할 시험)
M = [
    # ── PC8-05 시작 기록 사슬 부모 ──
    ('N01', 'PC8-05', [(RRF, "    if s0 is None:\n        return None, False\n    if 'chain_pid' not in s0:",
                        "    if True:\n        return None, False\n    if 'chain_pid' not in s0:")], T('PE05'), 'PE05 · PE05b · PE05o'),
    ('N02', 'PC8-05', [(RRF, "'chain_pid': os.getpid(),\n             'chain_start': (me_stat[1] if me_stat else None), ", "")], T('PE01'),
     'PE01 (시작 기록 칸)'),
    ('N03', 'PC8-05', [(RRF, "        if alive is False:\n            return None, False\n        return (f'사슬 부모 (시작 기록 pid",
                        "        if True:\n            return None, False\n        return (f'사슬 부모 (시작 기록 pid")], T('PE05'), 'PE05 · PE05b · PE05o live'),
    ('N05', 'PC8-05', [(RRF, "    if operator is not None:\n        return None, True\n    return (f'{what} — 시작 기록의 사슬 부모",
                        "    if False:\n        return None, True\n    return (f'{what} — 시작 기록의 사슬 부모")], T('PE05o'), 'PE05o other'),
    ('N06', 'PC8-05', [(RRF, "    if 'chain_pid' not in s0:\n        if operator is not None:",
                        "    if 'chain_pid' not in s0:\n        return None, False\n        if operator is not None:")], T('PE05o'), 'PE05o old'),
    ('N07', 'PC8-05', [(RRF, "        if not (type(cp) is int and cp > 0 and (cs is None or (type(cs) is int and cs >= 0))):", "        if False:")],
     T('PE05p'), 'PE05p'),
    ('N08', 'PC8-05', [(RRF, "    if set(s) not in (START_KEYS, START_KEYS_V1):", "    if set(s) != START_KEYS:")], T('PE01p,PE05p'), 'PE01p · PE05p'),
    ('N09', 'PC8-05', [(RRF, "            opx = operator if (operator is not None and f.resolve() == operator.get('folder')) else None",
                        "            opx = operator")], T('PE05o'), 'PE05o scope'),
    ('N10', 'PC8-05', [(RRF, "        n_bad, n_used = n_bad + nb, n_used + nu", "        n_bad, n_used = n_bad + nb, n_used")], T('PE05o'),
     'PE05o other · old (운영자 표지를 썼는데 rc 3)'),
    ('N11', 'PC8-05', [(RRF, "    same_boot = h.get('boot_id') is not None and h.get('boot_id') == me.get('boot_id')", "    same_boot = True")],
     T('PE05o,GR08'), 'PE05o other · GR08'),
    # ── PC8-02 끝 기록 ↔ 시작 기록 결합 ──
    ('B1', 'PC8-02', [(RRF, "             and er.get('token') == tok and L.get('name') == nm and er.get('name') == nm)",
                       "             and L.get('name') == nm and er.get('name') == nm)")], T('PE06,PE04'), 'PE06 · PE04'),
    ('B2', 'PC8-02', [(RRF, "             and er.get('token') == tok and L.get('name') == nm and er.get('name') == nm)",
                       "             and er.get('token') == tok)")], T('PE06,PE04'), 'PE06 other_name · PE04 name_chain'),
    ('B3', 'PC8-02', [(RRF, "        if not (bound and er.get('confirmed') is True):\n            return (f'그룹",
                       "        if not (er is not None and er.get('confirmed') is True):\n            return (f'그룹")], T('PE06'), 'PE06 unit'),
    ('B4', 'PC8-02', [(RRF, "        if L is None or er is None or not bound:", "        if L is None or er is None:")], T('PE06'), 'PE06 orphan_cause'),
    ('B5', 'PC8-02', [(RRF, "        if not (bound and e.get('confirmed') is True):        # ★ 11-04 PC8-02",
                       "        if not (e is not None and e.get('confirmed') is True):        # ★ 11-04 PC8-02")], T('PE06'), 'PE06 러너 그룹 (recover 가 안 죽임)'),
    ('B6', 'PC8-02', [(RRF, "        return bound and type(er.get('rc')) is int and er['rc'] == 0",
                       "        return er is not None and type(er.get('rc')) is int and er['rc'] == 0")], T('PE06'), 'PE06 _src_done'),
    ('B7', 'PC8-02', [(RRF, "        return bound and type(er.get('rc')) is int and er['rc'] == 0", "        return bound and er.get('rc') == 0")], T('PE06'),
     'PE06 _src_done rc_false · rc_float'),
    ('B8', 'PC8-02', [(RRF, "    if isinstance(prev, dict) and not bound:               # ★ 11-02 PC7-04",
                       "    if chain_end is not None and not bound:               # ★ 11-02 PC7-04")], T('PE06,PE04'), 'PE06 recover_group (chain_end 없음)'),
    ('B9≈M17', 'PC8-02', [(RRF, "    if isinstance(prev, dict) and not bound:               # ★ 11-02 PC7-04",
                           "    if False:               # ★ 11-02 PC7-04")], T('PE04,PE06'), 'PE04 · PE06'),
    # ── PC8-01 AL07 예외 = 증거 결합 ──
    ('A1', 'PC8-01', [(RRF, "                if al07_foreign_ok(k, p, r):",
                       "                if r is not None and r.get('status') == 'rejected' and (Path(p).parent / f'attempt_{k}{REJECTED_SIDE}').is_file():")],
     T('PD12u,PE02y'), 'PD12u · PE02y'),
    ('A2', 'PC8-01', [(RRF, "    if side.is_symlink() or not side.is_file() or folder_digest(side) != r.get('folder_sha256'):",
                       "    if side.is_symlink() or not side.is_file():")], T('PD12u'), 'PD12u al07_digest'),
    ('A3', 'PC8-01', [(RRF, "r.get('folder') == f'attempt_{k}{REJECTED_SIDE}'", "True"),
                      (RRF, "    side = p.parent / r['folder']", "    side = p.parent / f'attempt_{k}{REJECTED_SIDE}'")], T('PD12u'), 'PD12u al07_folder_attempt'),
    ('A4', 'PC8-01', [(RRF, "    if not (isinstance(rec, dict) and set(rec) == REJECTED_KEYS and rec.get('schema') == REJECTED_SCHEMA and type(rec.get('n')) is int\n"
                            "            and rec['n'] == k and rec.get('code') == 'OUTDIR_NOT_EMPTY' and _hex40(rec.get('ledger_commit'))):",
                       "    if not isinstance(rec, dict):")], T('PD12u'), 'PD12u al07_record_empty · n'),
    ('A5', 'PC8-01', [(RRF, "            and isinstance(r.get('stop'), dict) and r['stop'].get('code') == 'OUTDIR_NOT_EMPTY'):", "            ):"),
                      (RRF, "and rec.get('code') == 'OUTDIR_NOT_EMPTY' and _hex40", "and _hex40")], T('PD12u'), 'PD12u al07_code'),
    ('A6', 'PC8-01', [(RRF, "    return not attempt_chain_trace(p)", "    return True")], T('PD12u,PE02y'), 'PD12u 흔적 행 · PE02y bound'),
    ('A7', 'PC8-01', [(RRF, "        if any(True for _x in p.rglob(f'{GROUPS_DIR}/*.json')):", "        if False:")], T('PD12u'), 'PD12u al07_trace_groups'),
    ('A8', 'PC8-01', [(RRF, "        return folder_side(p) == 'post'\n    except OSError:\n        return True\n\n\ndef al07_foreign_ok",
                       "        return False\n    except OSError:\n        return True\n\n\ndef al07_foreign_ok")], T('PD12u'), 'PD12u al07_trace_post'),
    ('A9', 'PC8-01', [(RRF, "for nm in (ATTEMPT_FILE, REJECTED_FILE) + STAGE_SUMMARIES):", "for nm in (REJECTED_FILE,) + STAGE_SUMMARIES):")], T('PD12u'),
     'PD12u al07_trace_attempt_json'),
    ('A10', 'PC8-01', [(RRF, "    if side.is_symlink() or not side.is_file() or folder_digest(side)", "    if not side.is_file() or folder_digest(side)")],
     T('PD12u'), '— (같은 뜻 · 요약 sha 가 링크를 잡는다 = 두 겹 가드)'),
    ('A11≈M12', 'PC8-01', [(RRF, "            if a is None:\n                if al07_foreign_ok(k, p, r):",
                            "            if a is None:\n                continue\n                if al07_foreign_ok(k, p, r):")], T('PE02,PD12u,PE02x'), 'PE02 · PD12u'),
    #  보강 (첫 판 변이 목록에 없던 칸 하나씩 · PD12u 줄 넷을 더한 뒤)
    ('A12', 'PC8-01', [(RRF, "    if not (isinstance(r, dict) and r.get('status') == 'rejected' and r.get('folder') == f'attempt_{k}{REJECTED_SIDE}'",
                        "    if not (isinstance(r, dict) and r.get('folder') == f'attempt_{k}{REJECTED_SIDE}'")], T('PD12u'), 'PD12u al07_status_stopped'),
    ('A13', 'PC8-01', [(RRF, "set(rec) == REJECTED_KEYS and rec.get('schema') == REJECTED_SCHEMA and type(rec.get('n')) is int",
                        "set(rec) == REJECTED_KEYS and type(rec.get('n')) is int")], T('PD12u'), 'PD12u al07_record_schema'),
    ('A14', 'PC8-01', [(RRF, "isinstance(rec, dict) and set(rec) == REJECTED_KEYS and rec.get('schema')", "isinstance(rec, dict) and rec.get('schema')")],
     T('PD12u'), 'PD12u al07_record_extra'),
    ('A15', 'PC8-01', [(RRF, "and rec.get('code') == 'OUTDIR_NOT_EMPTY' and _hex40(rec.get('ledger_commit'))):",
                        "and rec.get('code') == 'OUTDIR_NOT_EMPTY'):")], T('PD12u'), 'PD12u al07_record_commit'),
    # ── PC8-03 · 04 · 09 바이트 까닭 · 보고 값 대조 ──
    ('J1', 'PC8-03', [(RRF, "        if kx != ky or kx == 'other':\n            return False\n        if kx == 'arr':",
                       "        if kx == 'other':\n            return False\n        if kx == 'arr':")], T('RV07,RV08'), 'RV07 · RV08'),
    ('J2', 'PC8-03', [(RRF, "            stack.extend((u, v) for kk in cx for u in cx[kk] for v in cy[kk])",
                       "            stack.extend((cx[kk][-1], cy[kk][-1]) for kk in cx)")], T('RV07,RV08'), 'RV07 dup · RV08 pub_dup'),
    ('J3≈M27', 'PC8-04', [(RRF, "        k.add('value')\n    try:\n        v0 = json.loads(old.decode('utf-8'))",
                           "        k.add('value')\n        view['kinds'] = ['value']\n        return view\n    try:\n        v0 = json.loads(old.decode('utf-8'))")],
     T('RV07'), 'RV07 value + newline · order'),
    ('J4≈M20', 'PC8-04', [(RRF, "        if _json_order_differs(v0, v1):\n            k.add('key_order')", "        if False:\n            k.add('key_order')")],
     T('RV05,RV06,RV07'), 'RV05 key_order · RV06 order · RV07'),
    ('J5≈M26', 'PC8-06', [(RRF, "    if _json_numform_differs(v0, v1):", "    if False:")], T('RV05,RV07'), 'RV07 numform_order'),
    ('J6', 'PC8-03', [(RRF, "or not all(json_same(v, cn[k]) for v in ct[k]))", "or not all(v == cn[k] for v in ct[k]))")], T('RV08'), 'RV08 keys'),
    ('J7', 'PC8-03', [(RRF, "'grade_differ': _grade_differ(t_pub, g1),", "'grade_differ': g0 != g1,")], T('RV08'), 'RV08 grade'),
    ('J8', 'PC8-09', [(RRF, "    except (UnicodeDecodeError, ValueError, RecursionError):\n        return _UNREAD",
                       "    except (UnicodeDecodeError, ValueError):\n        return _UNREAD")], T('RV07,RV09'), 'RV07 deep · RV09 res_deep'),
    ('J9', 'PC8-09', [(RRF, "    except (OSError, UnicodeDecodeError, ValueError, RecursionError) as e:   # ★ 11-04 PC8-09",
                       "    except (OSError, UnicodeDecodeError, ValueError) as e:   # ★ 11-04 PC8-09")], T('RV09'), 'RV09 pub_deep'),
    ('J10', 'PC8-09', [(RRF, "    if not isinstance(pub0, dict):                           # ★ 11-04 PC8-09",
                        "    if False:                           # ★ 11-04 PC8-09")], T('RV09'), 'RV09 pub_list'),
    ('J11', 'PC8-03', [(RRF, "or not json_same(t_res, r1), 'results_keys_differ': rkeys,", "or (t_res != r1), 'results_keys_differ': rkeys,")],
     T('RV06,RV08'), 'RV06 · RV08 results_differ'),
    # ── PC8-06 · 07 (탄소 접합) ──
    ('B01', 'PC8-06', [(CJF, "        t = (j + 0.5) * L / k", "        t = (j + 0.25) * L / k")], [['scripts/test_carbon_junction.py', '--only', 'BAN8']],
     'BAN8 ⑨'),
    ('Q1', 'PC8-07', [(CJF, QUAL_NEW, QUAL_OLD)], [['scripts/test_carbon_junction.py', '--only', 'BAN8'], ['scripts/test_ca_ext_b6.py', '--only', 'R']],
     'BAN8 ⑩ · b6 R7 11-03 판'),
]


def run(argv):
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    t0 = time.time()
    p = subprocess.run([sys.executable] + argv, cwd=str(MT), capture_output=True, text=True, env=env, timeout=3600)
    return p.returncode, p.stdout + p.stderr, time.time() - t0


res = json.loads(OUT.read_text()) if OUT.exists() else {}
for mid, finding, reps, cmds, catch in M:
    if SEL is not None and mid not in SEL:
        continue
    srcs, bad = {}, None
    for f, old, _new in reps:
        txt = srcs.get(f) or (MT / f).read_bytes().decode('utf-8')
        srcs.setdefault(f, txt)
        if txt.count(old) != 1:
            bad = f'옛 글이 {txt.count(old)} 번 ({f})'
    if bad:
        res[mid] = {'finding': finding, 'error': bad}
        OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
        print(mid, 'SKIP', bad, flush=True)
        continue
    orig = {f: (MT / f).read_bytes() for f in srcs}
    try:
        cur = {f: orig[f].decode('utf-8') for f in orig}
        for f, old, new in reps:
            cur[f] = cur[f].replace(old, new)
        for f, txt in cur.items():
            (MT / f).write_bytes(txt.encode('utf-8'))
        rcs, fails, summ, dt = [], [], [], 0.0
        for argv in cmds:
            rc, out, t = run(argv)
            rcs.append(rc)
            dt += t
            fails += re.findall(r'^\s*FAIL\s+(\S+(?: \S+)?)', out, re.M)
            summ += [ln for ln in out.splitlines() if re.search(r'test_rint_r_chain(_e2e)?:|== test_carbon_junction|PASS · \d+ FAIL', ln)][-1:]
    finally:
        for f, b in orig.items():
            (MT / f).write_bytes(b)
    killed = any(rc != 0 for rc in rcs)
    res[mid] = {'finding': finding, 'tests': [a[-1] for a in cmds], 'expected_catch': catch, 'rc': rcs, 'killed': killed,
                'failed_ids': sorted(set(fails))[:40], 'summary': summ, 'seconds': round(dt, 1)}
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
    print(mid, 'killed' if killed else 'SURVIVED', sorted(set(fails))[:8], round(dt, 1), flush=True)
