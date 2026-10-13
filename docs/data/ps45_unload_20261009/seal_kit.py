#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 언로딩 키트 K8 — 봉인 (SHA256SUMS) · 활성 규칙 목록 · 폐기 규칙 부재 검사 (REG §13-5 · ULR1-05).  표준 라이브러리만.

    python3 seal_kit.py --write      # SHA256SUMS + active_rules.json 다시 쓰기 (make_unload_decks.py 가 부른다)
    python3 seal_kit.py --check      # 파일 = SHA256SUMS · 덱 목록 = 생성기 · 폐기 규칙 0 건 · 활성 규칙 증인 (rc 0 · 1)
    python3 seal_kit.py --rules      # 활성 규칙 목록 (사람이 읽는 꼴)
    python3 seal_kit.py --selftest

봉인 대상 = 러너가 ibb 로 복사하는 묶음 (README 는 빼고 — 문서는 자주 고친다):  표 · 공용 · 판정 모듈 · 생성기 · 러너 · 래퍼 · 시험 · 덱 64.
폐기 규칙 (ULR1-05 ① ②) — 키트 어디에도 없어야 한다:
  ① 옛 띠 b (2 δ_num + r_int · "띠 > b 이면 미식별") — 덱 · 러너 글자 전부 · 파이썬은 AST (이름 · 속성 · 문자열 — selftest 함수 안은 뺀다:
     부재를 단언하는 시험 글자가 걸리지 않게) 에서 delta_num · band_b · b_pp · r_int · bband · δ_num
  ② 동시 UV 제출 — 러너 · 래퍼 · README 의 `for <X> in … UB … UV…` 꼴 고리 · 한 줄에 sbatch 두 번 이상
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT_FILES = ('unload_params.json', 'ul_lib.py', 'ul_s3.py', 'ul_observers.py', 'ul_gates.py', 'ul_reader.py', 'ul_runner_test.py',
             'make_unload_decks.py', 'seal_kit.py', 'run_unload.sh', 'run_unload_ibb.sbatch', 'active_rules.json')
OLD_B_NAMES = ('delta_num', 'band_b', 'b_pp', 'r_int', 'bband', 'δ_num')
TEXT_FILES = ('run_unload.sh', 'run_unload_ibb.sbatch')


# ── 구현 (아래 selftest 를 먼저 썼다) ─────────────────────────────────────────

RULES = (
    ('selection', '유효한 δ 두 개면 결정표 한 행 (§12-4) · 필요한 끝점이 무효 · 결손 · 무교차 · NaN 이면 SELECTION_UNRESOLVED — 다음 팔 · 본 런 없음 (§13-1)',
     'ul_reader.py', 'selection', ('ul_reader R2', 'ul_reader R3')),
    ('submission_order', 'UB · UT · UC 먼저 (서로 독립) → UB · UT 끝점 판독 → dt* → 그 dt* 의 UV 하나만 → 최종 튜플의 팔만 본 런 (§13-5 ② · 동시 UV 제출 없음)',
     'ul_reader.py', 'gate', ('ul_reader R5', 'ul_runner_test M5')),
    ('ut_rm_stop', 'UT = 첫 교차 + 확인 두 단 → R_M restart + 상태 파일 → 멈춤 (RM_STOP) · UB · UV = 전체 멈춤 규칙 (§13-5 ③)',
     'make_unload_decks.py', '_machine', ('make_unload_decks GD7',)),
    ('utc', '결정표 3 행 → UTc = U_UT3 덱을 UT 의 R_M (restart + 상태) 에서 이어 돌림 · 7:3 은 S0 에서 새 UT3 없음 (§13-5 ③)',
     'ul_reader.py', 'gate', ('ul_reader R5', 'ul_runner_test M9')),
    ('nonmonotone_union', '첫 교차 = 점 추정 + 비단조 표지 · 보고 괄호 = 모든 교차 괄호의 합집합 · 7:3 b 재이식 없음 (§13-5 ①)',
     'ul_reader.py', 'arm_verdict', ('ul_reader R8',)),
    ('separation', '창 접촉 상태 CONTACT · TENSION · ZERO · OBS_MISSING (≠ 0) · 분리 = 연속 두 0 창의 둘째 창 끝 · 재접촉 = 계수 · 분리 뒤 창 초기화 (§13-3)',
     'ul_reader.py', 'separation', ('ul_reader R6',)),
    ('timeout', '측정 뒤 TIMEOUT = 유효 ρ + 실제 괄호 · 교차 전 = 정상 · 접촉 · 단조일 때만 하한 · 아니면 미식별 (§13-2)',
     'ul_reader.py', 'arm_verdict', ('ul_reader R1',)),
    ('cancellation', '교차 끝점 인장 합 ≥ 0.5 · P_meas · A → 상쇄 표지 · 처분 = 진단값 (순위 · 10 쌍 표 밖) · 접촉 상태 · 자격과 세 칸 (§13-3 Q2 (가))',
     'ul_reader.py', 'arm_verdict', ('ul_reader R7',)),
    ('physical_windows', '창 W(dt) = T_W / dt (T_W = dt₀ · 5,000) · 유지 · 이동 · 표본 · thermo = 물리 시간 — 생성된 덱에서 다시 계산 (§13-4)',
     'make_unload_decks.py', 'arm_numbers', ('make_unload_decks GD6', 'ul_reader R9')),
    ('s3_total_force', 'S3 = 입자별 총힘 ‖F_i‖ 합 ÷ (접촉 크기 합 + 무게) ≤ 1e-3 · 이중 가산 없음 · 결손 = NOT_COMPUTED (§12-2 · choice C1 · C2)',
     'ul_s3.py', 's3_residual', ('ul_s3 selftest',)),
    ('sigma_p', 'σ_P = k* 마지막 두 창 thermo 정규 줄 (ul_Ps) · ddof 1 · 최소 10 · NOISE_FLOOR = P_meas < 3 σ_P (choice C3)',
     'ul_observers.py', 'sigma_P', ('ul_observers O1–O4b',)),
    ('resume_once', '기계 실패 이어 돌림 = 마지막 restart_unload_* + 짝 상태 파일에서 한 번 · 두 번째 = 거부 (§4-4 · §13-1)',
     'run_unload.sh', 'screen_a2.txt', ('ul_runner_test M7',)),
)


def kit_list(base=HERE):
    decks = []
    dd = os.path.join(base, 'decks')
    for bed in sorted(os.listdir(dd)) if os.path.isdir(dd) else []:
        for name in sorted(os.listdir(os.path.join(dd, bed))):
            if name.startswith('in.') and name.endswith('.liggghts'):
                decks.append(f'decks/{bed}/{name}')
    return list(KIT_FILES) + decks


def _sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sums_text(base=HERE):
    return ''.join(f'{_sha(os.path.join(base, rel))}  {rel}\n' for rel in kit_list(base))


_OLD_B = re.compile(r'(?<![A-Za-z0-9_])(?:delta_num|band_b|b_pp|r_int|bband)(?![A-Za-z0-9_])|δ_num')
_LOOP_UV = re.compile(r'\bfor\s+\w+\s+in\b[^\n;]*(?:\bUB\b[^\n;]*\bUV\w*|\bUV\w*[^\n;]*\bUB\b)')
_SBATCH_CMD = re.compile(r'(?:^|[;&|]\s*|\$\(\s*)sbatch\s')


def _py_strings_names(src):
    """AST — selftest 함수 (와 그 안) 를 뺀 이름 · 속성 · 인자 · 함수 이름 · 문자열 상수."""
    tree = ast.parse(src)
    out = []

    def walk(node, in_test=False):
        for ch in ast.iter_child_nodes(node):
            t = in_test or (isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)) and ch.name == 'selftest')
            if not t:
                if isinstance(ch, ast.Name):
                    out.append((ch.lineno, ch.id))
                elif isinstance(ch, ast.Attribute):
                    out.append((ch.lineno, ch.attr))
                elif isinstance(ch, ast.arg):
                    out.append((ch.lineno, ch.arg))
                elif isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    out.append((ch.lineno, ch.name))
                elif isinstance(ch, ast.Constant) and isinstance(ch.value, str):
                    out.append((ch.lineno, ch.value))
            walk(ch, t)
    walk(tree)
    return out


def scan_forbidden(base=HERE, extra_text=None):
    """폐기 규칙 (옛 띠 b · 동시 UV 제출) 이 남은 자리 → [{'rule', 'file', 'line', 'text'}]."""
    hits = []
    for rel in kit_list(base):
        p = os.path.join(base, rel)
        if not os.path.exists(p) or rel in ('seal_kit.py', 'active_rules.json'):
            continue
        txt = open(p, encoding='utf-8', errors='replace').read()
        if rel.endswith('.py'):
            for ln, s in _py_strings_names(txt):
                if _OLD_B.search(s):
                    hits.append({'rule': 'old_b', 'file': rel, 'line': ln, 'text': s[:80]})
            continue
        for n, line in enumerate(txt.splitlines(), 1):
            if _OLD_B.search(line):
                hits.append({'rule': 'old_b', 'file': rel, 'line': n, 'text': line.strip()[:80]})
            if rel in TEXT_FILES:
                code = line.split('#', 1)[0] if not line.lstrip().startswith('#') else ''
                if _LOOP_UV.search(code) or (len(_SBATCH_CMD.findall(code)) >= 2):
                    hits.append({'rule': 'simultaneous_UV', 'file': rel, 'line': n, 'text': line.strip()[:80]})
    for name, txt in (extra_text or {}).items():
        for n, line in enumerate(txt.splitlines(), 1):
            if _LOOP_UV.search(line) or len(_SBATCH_CMD.findall(line)) >= 2:
                hits.append({'rule': 'simultaneous_UV', 'file': name, 'line': n, 'text': line.strip()[:80]})
    return hits


def _where_exists(base, fname, sym):
    p = os.path.join(base, fname)
    if not os.path.exists(p):
        return False
    src = open(p, encoding='utf-8', errors='replace').read()
    if fname.endswith('.py'):
        return any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == sym for n in ast.walk(ast.parse(src)))
    return sym in src


def active_rules(base=HERE):
    rules = [{'id': i, 'rule': r, 'where': f'{f}:{s}', 'where_exists': _where_exists(base, f, s), 'witness': list(w)} for i, r, f, s, w in RULES]
    readme = os.path.join(base, 'README.md')
    extra = {'README.md': open(readme, encoding='utf-8').read()} if os.path.exists(readme) else None
    return {'schema': 'ps45_unload_active_rules_v1', 'rules': rules, 'forbidden': scan_forbidden(base, extra),
            'forbidden_rules': {'old_b': 'REG §13-5 ① — 옛 띠 b (2 δ_num + r_int) 판정 폐기 · 비단조 = 교차 괄호 합집합',
                                'simultaneous_UV': 'REG §13-5 ② — 동시 UV 제출 폐기 · UB · UT · UC 먼저 → dt* 의 UV'}}


def _rules_core(R):
    return [{k: r[k] for k in ('id', 'rule', 'where', 'witness')} for r in R['rules']]


def check(base=HERE):
    out = {'rc': 1, 'sums_ok': False, 'forbidden': [], 'problems': [], 'n_files': 0, 'n_rules': 0, 'rules_ok': False}
    sp = os.path.join(base, 'SHA256SUMS')
    want = kit_list(base)
    out['n_files'] = len(want)
    if not os.path.exists(sp):
        out['problems'].append('SHA256SUMS 없음')
    else:
        listed = {}
        for ln in open(sp, encoding='utf-8').read().splitlines():
            if ln.strip():
                h, rel = ln.split(None, 1)
                listed[rel.strip()] = h
        miss = [r for r in want if r not in listed]
        extra = [r for r in listed if r not in want]
        bad = [r for r in want if r in listed and (not os.path.exists(os.path.join(base, r)) or _sha(os.path.join(base, r)) != listed[r])]
        out['problems'] += [f'목록 밖 {r}' for r in extra] + [f'봉인 안 됨 {r}' for r in miss] + [f'sha256 다름 {r}' for r in bad]
        out['sums_ok'] = not (miss or extra or bad)
    R = active_rules(base)
    out['forbidden'] = R['forbidden']
    out['n_rules'] = len(R['rules'])
    out['rules_ok'] = all(r['where_exists'] for r in R['rules'])
    ap = os.path.join(base, 'active_rules.json')
    fresh = os.path.exists(ap) and _rules_core(json.load(open(ap, encoding='utf-8'))) == _rules_core(R)
    if not fresh:
        out['problems'].append('active_rules.json 이 지금 규칙 목록과 다르다 (seal_kit.py --write)')
    out['rc'] = 0 if (out['sums_ok'] and not out['forbidden'] and out['rules_ok'] and fresh) else 1
    return out


def write(base=HERE):
    R = active_rules(base)
    with open(os.path.join(base, 'active_rules.json'), 'w', encoding='utf-8') as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
        f.write('\n')
    for rel in kit_list(base):
        if not os.path.exists(os.path.join(base, rel)):
            raise SystemExit(f'⛔ 봉인할 파일이 없다: {rel}')
    with open(os.path.join(base, 'SHA256SUMS'), 'w', encoding='utf-8') as f:
        f.write(sums_text(base))
    print(f'✓ SHA256SUMS ({len(kit_list(base))} 파일) · active_rules.json (규칙 {len(R["rules"])} · 폐기 규칙 {len(R["forbidden"])} 건)')


# ── selftest ─────────────────────────────────────────────────────────────────

def selftest() -> int:
    import shutil
    import tempfile
    fails = []

    def chk(name, cond, detail=''):
        try:
            ok = bool(cond() if callable(cond) else cond)
        except Exception as e:  # noqa: BLE001 — 빈 구현 · 예외도 실패
            ok, detail = False, f'{type(e).__name__}: {e}'
        print(('  ✓ ' if ok else '  ✗ ') + name + ('' if ok else f'  — {detail}'))
        if not ok:
            fails.append(name)

    td = tempfile.mkdtemp(prefix='ul_seal_')
    try:
        k = os.path.join(td, 'kit')
        shutil.copytree(HERE, k, ignore=shutil.ignore_patterns('__pycache__', 'history_test', 'SHA256SUMS', 'active_rules.json', 'decks'))
        sys.path.insert(0, HERE)
        import make_unload_decks as mk   # 덱 = 생성기 결과 (커밋본 decks/ 와 무관하게)
        for rel, text in mk.generated_files().items():
            os.makedirs(os.path.dirname(os.path.join(k, rel)), exist_ok=True)
            open(os.path.join(k, rel), 'w', encoding='utf-8').write(text)
        try:
            write(k)
        except Exception:  # noqa: BLE001
            pass
        chk('K1 봉인 목록 = 표 · 모듈 · 생성기 · 러너 · 래퍼 · 시험 · active_rules.json + 덱 64 (README · 이력 시험 폴더 제외)',
            lambda: (lambda L: len([x for x in L if x.startswith('decks/')]) == 64 and set(KIT_FILES) <= set(L)
                     and not any(x.startswith(('README', 'history_test')) for x in L))(kit_list(k)))
        chk('K2 깨끗한 키트 = check rc 0 · 폐기 규칙 0 건', lambda: check(k)['rc'] == 0 and check(k)['forbidden'] == [])
        p = os.path.join(k, 'decks', 'ps_7_3_r45', 'in.U_UB.liggghts')
        open(p, 'a').write('# 고침\n')
        chk('K3 덱 한 줄 고침 → check 실패 (SHA256SUMS)', lambda: check(k)['rc'] != 0)
        try:
            write(k)
        except Exception:  # noqa: BLE001 — 빈 구현
            pass
        rp = os.path.join(k, 'ul_reader.py')
        src = open(rp, encoding='utf-8').read()
        open(rp, 'w', encoding='utf-8').write(src.replace('def pair_table(verdicts):', 'def pair_table(verdicts, band_b=None):', 1))
        chk('K4 판독기 코드 (시험 밖) 에 옛 b 이름 (band_b) 을 넣으면 폐기 규칙 위반으로 걸린다',
            lambda: any(h['rule'] == 'old_b' and h['file'] == 'ul_reader.py' for h in scan_forbidden(k)))
        open(rp, 'w', encoding='utf-8').write(src)
        chk('K4 판독기 selftest 안의 부재 단언 ("band_b" not in …) 은 걸리지 않는다 (AST · selftest 제외)',
            lambda: not any(h['file'] == 'ul_reader.py' for h in scan_forbidden(k)))
        rn = os.path.join(k, 'run_unload.sh')
        rsrc = open(rn, encoding='utf-8').read()
        open(rn, 'w', encoding='utf-8').write(rsrc + '\nfor A in UB UVa UT UC; do sbatch x $A; done\n')
        chk('K5 러너에 동시 UV 제출 고리 (for A in UB UVa UT UC) 를 넣으면 걸린다',
            lambda: any(h['rule'] == 'simultaneous_UV' for h in scan_forbidden(k)))
        open(rn, 'w', encoding='utf-8').write(rsrc + '\nsbatch a.sbatch k ps_7_3_r45 UB; sbatch a.sbatch k ps_7_3_r45 UVa\n')
        chk('K5 한 줄에 sbatch 둘 (UB 와 UV 를 같이) 도 걸린다', lambda: any(h['rule'] == 'simultaneous_UV' for h in scan_forbidden(k)))
        open(rn, 'w', encoding='utf-8').write(rsrc)
        dk = os.path.join(k, 'decks', 'ps_5_5_r45', 'in.U_UB.liggghts')
        dsrc = open(dk, encoding='utf-8').read()
        open(dk, 'w', encoding='utf-8').write(dsrc + '# 2 δ_num + r_int 띠\n')
        chk('K6 덱 주석이라도 옛 b (δ_num · r_int) 글자가 있으면 걸린다', lambda: any(h['rule'] == 'old_b' and 'decks/' in h['file'] for h in scan_forbidden(k)))
        open(dk, 'w', encoding='utf-8').write(dsrc)
        chk('K6 README 의 동시 제출 꼴 (for A in UB UV UT UC) 도 걸린다 (명령 꼴을 사람이 붙여 넣는다)',
            lambda: any(h['rule'] == 'simultaneous_UV' for h in scan_forbidden(k, extra_text={'README.md': 'for A in UB UV UT UC; do sbatch …; done'})))
        R = None
        try:
            R = active_rules(k)
        except Exception:  # noqa: BLE001
            R = None
        chk('K7 활성 규칙 목록: 선택 (SELECTION_UNRESOLVED) · 제출 순서 (UB · UT · UC → UV) · UT R_M 멈춤 · UTc · 비단조 합집합 · 분리 · TIMEOUT 세 경우 · '
            '상쇄 진단값 · 물리 창 · S3 총힘 · σ_P — 규칙마다 코드 자리 (실재) · 증인 시험 이름 · 폐기 규칙 0 건',
            lambda: R is not None and len(R['rules']) >= 11 and all(r['where_exists'] for r in R['rules']) and R['forbidden'] == []
            and {'selection', 'submission_order', 'ut_rm_stop', 'utc', 'nonmonotone_union', 'separation', 'timeout', 'cancellation',
                 'physical_windows', 's3_total_force', 'sigma_p'} <= {r['id'] for r in R['rules']})
    finally:
        shutil.rmtree(td, ignore_errors=True)
    print(f'selftest: {"PASS" if not fails else "FAIL"} ({len(fails)} 실패)')
    return 1 if fails else 0


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ['--selftest']:
        return selftest()
    if argv[:1] == ['--write']:
        write()
        return check()['rc']
    if argv[:1] == ['--check']:
        r = check()
        print(('✓' if r['rc'] == 0 else '⛔') + f' seal — 파일 {r["n_files"]} · SHA256SUMS {"일치" if r["sums_ok"] else "불일치"} · 폐기 규칙 {len(r["forbidden"])} 건 · '
              f'활성 규칙 {r["n_rules"]} (증인 실재 {r["rules_ok"]})')
        for h in r['forbidden'][:10]:
            print('   ·', h)
        for p in r['problems'][:10]:
            print('   ·', p)
        return r['rc']
    if argv[:1] == ['--rules']:
        R = active_rules()
        for r in R['rules']:
            print(f'{r["id"]:<18} {r["rule"]}\n{"":18} 자리 {r["where"]} · 증인 {", ".join(r["witness"])}')
        print(f'폐기 규칙 {len(R["forbidden"])} 건')
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main())
