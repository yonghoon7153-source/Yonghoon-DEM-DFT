#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rint ② PC6-13 · PC6-02 라이브러리 표지 고침 (11-02) — 변이 시험 (새 가드 하나씩 끄고 그 시험 접두가 잡나) · mutate_pc6fix.py (11-02) 와 같은 틀.

  python3 mutate_pc6_13.py <원 트리> <사본 트리 (scripts 사본 · 나머지 링크)> <결과 json> <로그 폴더> <묶음: pc613 | lib | all | <id,…>>

변이마다 사본 트리의 scripts/rint_r_chain.py 를 원본에서 다시 쓰고 바꾼 뒤 `scripts/test_rint_r_chain.py --only <접두>` (rc ≠ 0 = 잡힘) · 화면 전문 =
<로그 폴더>/<id>.log · 옛 글은 정확히 한 번 (아니면 ERROR) · 끝에 원본으로 되돌린다.  'BASE' = 변이 없음 (모든 접두의 합).  값 · σ 없음 (가짜 러너).
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

W9 = ("CUDA_ERROR_WORDS = ('CUDA_ERROR_', 'cudaError', 'CUDARuntimeError', 'CUDADriverError', 'CUBLAS_STATUS_', 'CUSOLVER_STATUS_', 'CUSPARSE_STATUS_', "
      "'CUFFT_',\n                    'CUDA error:')\n")


def drop(word):
    """표지 표에서 낱말 하나를 뺀 판 (나머지 차례 그대로)."""
    words = ['CUDA_ERROR_', 'cudaError', 'CUDARuntimeError', 'CUDADriverError', 'CUBLAS_STATUS_', 'CUSOLVER_STATUS_', 'CUSPARSE_STATUS_', 'CUFFT_',
             'CUDA error:']
    return 'CUDA_ERROR_WORDS = (' + ', '.join(repr(w) for w in words if w != word) + ')\n'


#: (id, 끈 가드, 옛 글 (정확히 한 번), 새 글, 시험 접두, 기대 (killed | survived:<까닭>))
PC613 = [
    ('G13a', 'PC6-13 요약 있는 길 — 그룹 미확인 + 러너 실패 rc 가드 끔 (옛 = group_unconfirmed · 재실행 자격)',
     "        if runner_rc_failed((rr or {}).get('rc')):            # ★ 11-02 PC6-13 — 러너 rc 길과 같은 규칙 (그룹 미확인이 러너 rc ≠ 0 을 가리지 않는다)\n"
     "            return words_cause(txt, 'runner_rc')\n", "", 'PD13', 'killed'),
    ('G13b', 'PC6-13 요약 있는 길 — 낱말 없을 때 기본값 runner_rc → group_unconfirmed (낱말만 보고 기본 원인은 그대로)',
     "            return words_cause(txt, 'runner_rc')\n        base = 'group_unconfirmed'\n",
     "            return words_cause(txt, 'group_unconfirmed')\n        base = 'group_unconfirmed'\n", 'PD13', 'killed'),
    ('G13c', 'PC6-13 runner_rc_failed = 같음 비교 (rc not in (0, None) — False · 0.0 = 0 으로 읽음 · 보수 반대)',
     "    return rc is not None and not (type(rc) is int and rc == 0)\n", "    return rc not in (0, None)\n", 'PD13', 'killed'),
    ('G13d', 'PC6-13 runner_rc_failed 늘 False (모든 길의 새 가드 끔)',
     "    return rc is not None and not (type(rc) is int and rc == 0)\n", "    return False\n", 'PD13', 'killed'),
    ('G13e', 'PC6-13 runner_rc_failed — None 도 실패로 (사슬이 죽인 런 · 정리 중 신호를 runner_rc 로 · 넘침)',
     "    return rc is not None and not (type(rc) is int and rc == 0)\n", "    return not (type(rc) is int and rc == 0)\n", 'PD13', 'killed'),
    ('G13f', 'PC6-13 요약 없는 길 — recover 끝 기록의 chain_end 무시 (옛 = parent_dead)',
     "            c = words_cause(txt, 'runner_rc' if chain_end_failed(er) else 'parent_dead')   # ★ 11-02 PC6-13 — 사슬 끝 기록이 남긴 러너 rc\n",
     "            c = words_cause(txt, 'parent_dead')\n", 'PD13', 'killed'),
    ('G13g', 'PC6-13 chain_end_failed — 원인 칸 무시 (사슬이 죽인 런 rc −9 · timeout · signal 을 runner_rc 로 · 넘침)',
     "    return isinstance(ce, dict) and ce.get('cause') is None and runner_rc_failed(ce.get('rc'))\n",
     "    return isinstance(ce, dict) and runner_rc_failed(ce.get('rc'))\n", 'PD13', 'killed'),
    ('G13h', 'PC6-13 recover_group — 사슬의 옛 끝 기록에서 chain_end 를 만들지 않음 (옛 = 덮어써 잃음)',
     "    if isinstance(prev, dict) and prev.get('by') == 'chain':\n        chain_end = {k: prev.get(k) for k in ('rc', 'cause', 'confirmed', 'ended_utc')}\n",
     "    if False:\n        chain_end = None\n", 'PD13', 'killed'),
    ('G13i', 'PC6-13 recover_group — 앞 recover 끝 기록의 chain_end 를 이어받지 않음 (recover 두 번 = 잃음)',
     "    elif isinstance(prev, dict) and prev.get('by') == 'recover' and isinstance(prev.get('chain_end'), dict):\n        chain_end = prev['chain_end']\n",
     "    elif False:\n        chain_end = None\n", 'PD13', 'killed'),
    ('G13j', 'PC6-13 recover_group — chain_end 를 끝 기록에 쓰지 않음',
     "    if chain_end is not None:\n        end['chain_end'] = chain_end                       # ★ 11-02 PC6-13\n", "", 'PD13', 'killed'),
    ('G13k', 'PC6-13 recover_group — chain_end 대신 새 끝 기록 rc 에 러너 rc (재실행 원천 "끝난 런" rc 0 판정을 흔듦 · 칸 없음)',
     "    if chain_end is not None:\n        end['chain_end'] = chain_end                       # ★ 11-02 PC6-13\n",
     "    if chain_end is not None:\n        end['rc'] = chain_end.get('rc')\n", 'PD13', 'killed'),
    ('G13l', 'PC6-13 멈춤 문장에 러너 rc 를 빼 (화면 · 단계 요약 · 옛 문장)',
     "· 원인 {cause} · 러너 rc {rec[\"rc\"]}) — 그 런의 '\n", "· 원인 {cause}) — 그 런의 '\n", 'PD13', 'killed'),
]
LIB = [
    ('L02a', 'PC6-02 라이브러리 표지 CUBLAS_STATUS_ 뺌', W9, drop('CUBLAS_STATUS_'), 'PD02c', 'killed'),
    ('L02b', 'PC6-02 라이브러리 표지 CUSOLVER_STATUS_ 뺌', W9, drop('CUSOLVER_STATUS_'), 'PD02c', 'killed'),
    ('L02c', 'PC6-02 라이브러리 표지 CUSPARSE_STATUS_ 뺌', W9, drop('CUSPARSE_STATUS_'), 'PD02c', 'killed'),
    ('L02d', 'PC6-02 라이브러리 표지 CUFFT_ 뺌', W9, drop('CUFFT_'), 'PD02c', 'killed'),
    ('L02e', "PC6-02 다른 꼴 표지 'CUDA error:' 뺌", W9, drop('CUDA error:'), 'PD02c', 'killed'),
    ('L02f', 'PC6-02 CUDA 표지를 자원 낱말 앞에 봄 (메모리 부족 + 라이브러리 줄 = runner_rc · 1저자 결정의 차례 반대)',
     "    if any(w in txt for w in RESOURCE_WORDS):\n        return 'resource'\n    if any(w in txt for w in CUDA_ERROR_WORDS):\n        return 'runner_rc'\n",
     "    if any(w in txt for w in CUDA_ERROR_WORDS):\n        return 'runner_rc'\n    if any(w in txt for w in RESOURCE_WORDS):\n        return 'resource'\n",
     'PD02c', 'killed'),
    ('L02g', "PC6-02 'CUDA error:' 를 대소문자 무시 판으로 ('CUDA error:' → 'CUDA Error:' — 대조 표지 · 실제 줄 꼴과 다름)", W9,
     W9.replace("'CUDA error:'", "'CUDA Error:'"), 'PD02c', 'killed'),
]
FAIL_RE = re.compile(r'^\s*FAIL\s+(\S+)\s+(.*)$')


def run_one(tree, mid, only, env, logd):
    t0 = time.time()
    p = subprocess.run(['nice', '-n', '10', sys.executable, str(tree / 'scripts' / 'test_rint_r_chain.py'), '--only', only],
                       capture_output=True, text=True, env=env, cwd=str(tree))
    (logd / f'{mid}.log').write_text(p.stdout + ('\n--- stderr ---\n' + p.stderr if p.stderr.strip() else ''), encoding='utf-8')
    tail = [ln for ln in p.stdout.splitlines() if ln.startswith('test_rint_r_chain:')]
    fails = [{'cid': m.group(1), 'line': m.group(2)[-700:]} for m in (FAIL_RE.match(ln) for ln in p.stdout.splitlines()) if m]
    return p.returncode, (tail[-1] if tail else (p.stdout[-300:] + p.stderr[-300:])), fails, round(time.time() - t0, 1)


def main():
    wt, tree, outp, logd, group = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]), sys.argv[5]
    logd.mkdir(parents=True, exist_ok=True)
    groups = {'pc613': PC613, 'lib': LIB}
    allm = PC613 + LIB
    if group in groups:
        todo = list(groups[group])
    elif group == 'all':
        todo = [('BASE', '변이 없음', None, None, 'PD13,PD02c', 'pass')] + list(allm)
    else:
        pick = set(group.split(','))
        todo = [m for m in allm if m[0] in pick]
        if 'BASE' in pick:
            todo = [('BASE', '변이 없음', None, None, 'PD13,PD02c', 'pass')] + todo
    src = (wt / 'scripts' / 'rint_r_chain.py').read_text(encoding='utf-8')
    dst = tree / 'scripts' / 'rint_r_chain.py'
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    res = json.loads(outp.read_text(encoding='utf-8')) if outp.exists() else []
    done = {r['id'] for r in res}
    try:
        for mid, why, old, new, only, expect in todo:
            if mid in done:
                continue
            if old is None:
                dst.write_text(src, encoding='utf-8')
            else:
                n = src.count(old)
                if n != 1:
                    res.append({'id': mid, 'why': why, 'only': only, 'error': f'옛 글 {n} 번'})
                    outp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
                    print(mid, 'ERROR', f'옛 글 {n} 번', flush=True)
                    continue
                mutated = src.replace(old, new, 1)
                compile(mutated, 'rint_r_chain.py', 'exec')            # 문법 검사 (변이가 문법을 깨면 그 자체가 잘못된 변이)
                dst.write_text(mutated, encoding='utf-8')
            rc, summary, fails, sec = run_one(tree, mid, only, env, logd)
            res.append({'id': mid, 'why': why, 'only': only, 'expect': expect, 'rc': rc, 'killed': (rc != 0) if old is not None else None,
                        'summary': summary, 'fails': fails, 'seconds': sec})
            outp.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
            state = ('killed' if rc else 'SURVIVED') if old is not None else ('BASE-FAIL' if rc else 'BASE-OK')
            print(mid, only, state, f'(기대 {expect})', summary, 'fails=', [f['cid'] for f in fails], flush=True)
    finally:
        dst.write_text(src, encoding='utf-8')


if __name__ == '__main__':
    main()
