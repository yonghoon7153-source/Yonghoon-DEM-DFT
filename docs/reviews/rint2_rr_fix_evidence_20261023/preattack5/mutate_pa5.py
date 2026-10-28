#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""사전 공격 5 회차 — 변이 시험 (가드 하나씩 끄고 기존 시험 부분집합이 잡나).  묶음 C 보고의 변이 207 (REPORT_C §7) 목록에 없는 가드만 골랐다.

  python3 mutate_pa5.py <원 트리> <사본 트리 (scripts 사본 · docs 링크)> <결과 json> [변이 id …]

사본 트리의 scripts/rint_r_chain.py 를 변이마다 원본에서 다시 쓰고 바꾼 뒤 `scripts/test_rint_r_chain.py --only <접두>` 를 돌린다 (rc ≠ 0 = 잡힘).
끝에 원본으로 되돌린다.  변이 = (id, 설명, 옛 글 (정확히 한 번), 새 글, 시험 접두).
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

M = [
    ('X01', '합치기 — 원장 역사 (덧붙이기만) 검사 끔',
     "        head, raw = ledger_now(repo)\n        why = ledger_history_problem(repo, head)\n        if why:\n            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장 역사: {why}')\n        st = ledger_parse(raw)\n        mg['ledger']",
     "        head, raw = ledger_now(repo)\n        st = ledger_parse(raw)\n        mg['ledger']", 'UM'),
    ('X02', '합치기 — --max-hours · 기계 · 계획 봉인 판 대조 끔',
     "        plan_doc_or_stop(a.registration, plan)\n        exec_check_or_stop(plan, a.max_hours, a.machine, s['code'])\n        if plan_sha != st['header']['plan_sha256']:",
     "        plan_doc_or_stop(a.registration, plan)\n        pass\n        if plan_sha != st['header']['plan_sha256']:", 'UM,EP'),
    ('X03', '합치기 — 등록 계획 숫자 블록 대조 끔',
     "        plan_doc_or_stop(a.registration, plan)\n        exec_check_or_stop(plan, a.max_hours, a.machine, s['code'])\n        if plan_sha != st['header']['plan_sha256']:",
     "        pass\n        exec_check_or_stop(plan, a.max_hours, a.machine, s['code'])\n        if plan_sha != st['header']['plan_sha256']:", 'UM,EP'),
    ('X04', '합치기 — 원장 머리 계획 = 사다리 계획 대조 끔',
     "        if plan_sha != st['header']['plan_sha256']:\n            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'원장 머리의 계획 {st[\"header\"][\"plan_sha256\"][:12]} ≠ 사다리 계획 {plan_sha[:12]}')\n",
     "", 'UM'),
    ('X05', '판정 — 최대 시도 수 (ATTEMPT_LIMIT) 대조 끔',
     "        if lim and lim[0] == 'ATTEMPT_LIMIT':\n            raise Stop(*lim)\n        if ad['effective'] is None or ad['effective'] != n_in:",
     "        if ad['effective'] is None or ad['effective'] != n_in:", 'AL,UM'),
    ('X06', '판정 — 같은 대상 입력 둘 (DUPLICATE_RUN) 끔',
     "        if a['target'] in want:\n            raise Stop('DUPLICATE_RUN', f'같은 대상 {a[\"target\"]} 입력 둘')\n", "", 'AL'),
    ('X07', '--add — --plan sha = 원장 머리 계획 대조 끔',
     "        if plan_sha != st['header']['plan_sha256']:\n            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'--plan sha256 {plan_sha[:12]} ≠ 원장 머리의 계획 {st[\"header\"][\"plan_sha256\"][:12]}')\n",
     "", 'AL'),
    ('X08', '--init — 봉인 전 계획 (null 칸) 거부 끔',
     "            require_plan_numbers(plan)                        # 봉인 전 계획 = 원장 없음", "            pass  # 봉인 전 계획 = 원장 없음", 'AL,EP'),
    ('X09', '결과 줄 꼴 — rejected 인데 결과 뒤 · 재실행 자격 검사 끔',
     "    if r['status'] == 'rejected' and (r['side'] != 'pre' or r['resume_ok']):\n        return '거부인데 결과 뒤 · 재실행 자격'\n", "", 'AL'),
    ('X10', '자원 낱말 — NOT_RESOURCE_WORDS (잘못된 주소) 끔',
     "        if any(w in txt for w in NOT_RESOURCE_WORDS):\n            return 'runner_rc'\n", "", 'AL19'),
    ('X11', 'recover --ledger — 시도 폴더 ↔ 원장 항목 (대상 · 시작 커밋 조상) 대조 끔',
     "            if e is None or e['target'] != a['target'] or not ledger_is_ancestor(repo, a['ledger_commit'], head):",
     "            if e is None:", 'AL13,AL14,RS02'),
    ('X12', '원장 꼴 — 항목 resume_of 꼴 (같은 대상 앞 항목) 검사 끔',
     "    if r is not None and (type(r) is not int or r not in st['entries'] or st['entries'][r]['target'] != e['target']):\n        return f'resume_of {r!r} (같은 대상의 앞 항목이어야)'\n",
     "", 'AL,RS'),
    ('X13', 'exec_policy — allowed_machines 중복 검사 끔',
     "                               and len(set(am)) == len(am)):", "                               and True):", 'EP'),
    ('X14', '재실행 복사 — 복사 자리가 이미 있음 검사 끔',
     "        if outdir.exists():\n            raise Stop('OUTDIR_NOT_EMPTY', f'{outdir} — 재실행 복사 자리가 이미 있다', name)\n", "", 'RS'),
    ('X15', '원장 읽기 — 원장 파일이 링크면 거부 끔',
     "        cur = lp.read_bytes() if not lp.is_symlink() else None", "        cur = lp.read_bytes()", 'AL'),
    ('X16', '합친 예측 판정 — 같은 단위 런 두 번 사용 검사 끔',
     "              and iname not in used[t])", "              and True)", 'UM'),
    ('X17', '합치기 — 사다리 입력 = 이 원장 채택 사다리 시도 대조 끔',
     "        ledger_inputs_check(a.ladders, repo, head, st, want_prefix='ladder:')\n", "", 'UM'),
    ('X18', 'recover --ledger — 거부 기록 (rejected.json) 폴더 = rejected 결과 줄 끔',
     "            rj = f / REJECTED_FILE\n            if rj.is_file():", "            rj = f / REJECTED_FILE\n            if False:", 'AL,RS,GR'),
    ('X19', '넘침 점 풀기 전 — 결정 기록 변이 대조 끔',
     "    if dec['variant'] != a.variant:\n        why = f'결정 기록 변이 {dec[\"variant\"]!r} ≠ {a.variant!r}'\n    elif a.point",
     "    if False:\n        why = None\n    elif a.point", 'UM'),
    ('X20', '넘침 점 풀기 전 — 결정 기록 계획 sha 대조 끔',
     "    elif dec['plan_sha256'] != e['plan_sha256']:\n        why = '결정 기록의 계획 sha256 ≠ 원장 항목'\n", "", 'UM'),
    ('X21', '끝 합치기 — 결정 기록 변이 · 계획 · 사다리 요약 sha 대조 끔',
     "            if dec['variant'] != a.variant or dec['plan_sha256'] != plan_sha \\\n                    or dec['ladders'] != {law: s['ladders'][law]['summary_sha256'] for law in LAWS}:",
     "            if False:", 'UM'),
    ('X22', '--add — 지금 코드 dirty · 환경 봉인 판 대조 끔',
     "        why = code_dirty_problem(code) or env_seal_problem(code, plan)\n        if why:\n            raise Stop('CODE_PIN_MISMATCH', why)\n        e = {'kind': 'entry'",
     "        e = {'kind': 'entry'", 'AL,EP'),
    ('X23', '--add — 허용 기계 대조 끔',
     "        if a.machine not in (plan['exec_policy'].get('allowed_machines') or ()):\n            raise Stop('MACHINE_NOT_ALLOWED', f'--machine {a.machine!r} ∉ 계획 허용 목록 {plan[\"exec_policy\"].get(\"allowed_machines\")}')\n",
     "", 'AL,EP'),
]


def main():
    wt, tree, outp = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    pick = set(sys.argv[4:])
    src = (wt / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
    dst = tree / 'scripts' / 'rint_r_chain.py'
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    res = json.loads(outp.read_text()) if outp.exists() else []
    done = {r['id'] for r in res}
    try:
        for mid, why, old, new, only in M:
            if (pick and mid not in pick) or mid in done:
                continue
            n = src.count(old)
            if n != 1:
                res.append({'id': mid, 'why': why, 'error': f'옛 글 {n} 번'})
                outp.write_text(json.dumps(res, ensure_ascii=False, indent=1))
                continue
            dst.write_text(src.replace(old, new, 1), encoding='utf-8')
            t0 = time.time()
            p = subprocess.run(['nice', '-n', '19', sys.executable, str(tree / 'scripts' / 'test_rint_r_chain.py'), '--only', only],
                               capture_output=True, text=True, env=env, cwd=str(tree))
            tail = [ln for ln in p.stdout.splitlines() if ln.startswith('test_rint_r_chain:')]
            res.append({'id': mid, 'why': why, 'only': only, 'rc': p.returncode, 'killed': p.returncode != 0,
                        'summary': tail[-1] if tail else p.stdout[-300:], 'seconds': round(time.time() - t0, 1)})
            outp.write_text(json.dumps(res, ensure_ascii=False, indent=1))
            print(mid, 'killed' if p.returncode else 'SURVIVED', tail[-1] if tail else '', flush=True)
    finally:
        dst.write_text(src, encoding='utf-8')


if __name__ == '__main__':
    main()
