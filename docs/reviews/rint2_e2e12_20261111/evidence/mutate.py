#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""변이 확인 (작업 트리 밖) — 작업 트리 scripts/ 의 사본에서 사슬 (`rint_r_chain.py`) 의 검사 하나를 끄고 새 시험을 다시 돌려 그 단언이 실패하는지 본다.
사본은 변이마다 만들고 지운다 (작업 트리 · 본 리포는 건드리지 않는다).

  python3 mutate.py <작업 트리> <남긴 세계 폴더> <결과 JSON> [변이 이름 …]

  꼴 redo = 끝까지 간 세계 (--reuse) 에서 음성 대조만 다시 (--redo · 30 s 쯤)
  꼴 upto = 새 세계에서 D3 묶음까지 (--upto D3 · 3–4 분) — 재실행 규칙 (D6i) 처럼 --redo 에 없는 단언
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time

TREE, WORLD, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
ONLY = sys.argv[4:]
HERE = os.path.dirname(os.path.abspath(__file__))
EXTRA = ['.gitignore', 'docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md', 'docs/reviews/sdcp_gain_prereg_v2_20260816.md']

DIGEST1 = ("        if folder_digest(p) != r['folder_sha256']:\n            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{p.name}: 폴더 요약 sha ≠ 원장 결과 줄 {k}')",
           "        if False and folder_digest(p) != r['folder_sha256']:\n            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'{p.name}: 폴더 요약 sha ≠ 원장 결과 줄 {k}')")
SRCBASE = ("        if read_attempt(src) is None or r is None or r['folder'] != src.name or folder_digest(src) != r['folder_sha256']:\n"
           "            return ('RESUME_NOT_ALLOWED', f'재실행 원천 {src}",
           "        if False and (read_attempt(src) is None or r is None or r['folder'] != src.name or folder_digest(src) != r['folder_sha256']):\n"
           "            return ('RESUME_NOT_ALLOWED', f'재실행 원천 {src}")

#: (이름, 꼴, 무엇을 끄나, [(옛 글, 새 글)], 실패해야 하는 단언 머리)
MUT = [
    ('base', 'redo', '변이 없음 (대조 — 사본에서 그대로 · 전부 통과해야)', [], []),
    ('M1', 'redo', 'MergeFetch._open — 채택 시도 없는 단위의 멈춤 (UNIT_MISSING) 을 끔 (넘침 점처럼 "다음 단계 필요" 로 흘림)',
     [("            if kind == 'point':                            # 넘침 점이 아직 없다", "            if True:                                       # 넘침 점이 아직 없다")], ['D5a']),
    ('M4', 'redo', 'MergeFetch.finish — 다시 계산이 끝까지 간 뒤 남는 채택 런 (UNIT_EXTRA) 멈춤을 끔',
     [("        if extra:\n            raise Stop('UNIT_EXTRA', f'다시 계산이 끝까지 갔는데", "        if False and extra:\n            raise Stop('UNIT_EXTRA', f'다시 계산이 끝까지 갔는데")],
     ['D5b']),
    ('M2', 'redo', 'target_ledger_problem — 시도 폴더 요약 sha ↔ 원장 결과 줄 대조를 끔 (첫 방어선만)', [DIGEST1], ['D5c']),
    ('M2b', 'redo', 'M2 + MergeFetch._copy — 사본 요약 sha ↔ 원장 결과 줄 대조도 끔 (둘째 방어선까지)',
     [DIGEST1, ("        if folder_digest(dst) != self.st['results'][k]['folder_sha256']:",
                "        if False and folder_digest(dst) != self.st['results'][k]['folder_sha256']:")], ['D5c']),
    ('M8', 'redo', 'attempt_order_problem — 채택 뒤 같은 대상의 새 항목 (ATTEMPT_AFTER_ADOPTED) 거부를 끔',
     [("        if ad['adopted'] is not None:\n            return ('ATTEMPT_AFTER_ADOPTED', f'{target} 은 이미 채택 시도",
       "        if False and ad['adopted'] is not None:\n            return ('ATTEMPT_AFTER_ADOPTED', f'{target} 은 이미 채택 시도")], ['D5d']),
    ('M9', 'redo', 'stage_ledger --add — 계획 봉인 판 ↔ 환경 같음 단위 대조 (env_seal_problem) 를 끔',
     [("        why = code_dirty_problem(code) or env_seal_problem(code, plan)\n        if why:\n            raise Stop('CODE_PIN_MISMATCH', why)\n        e = {'kind': 'entry'",
       "        why = code_dirty_problem(code)\n        if why:\n            raise Stop('CODE_PIN_MISMATCH', why)\n        e = {'kind': 'entry'")], ['D5d']),
    ('M3', 'redo', 'unit_summary_problem — 단위 요약의 출처 칸 ↔ 합치기 대조를 끔',
     [("    if diff:\n        return f'출처 칸 {diff} ≠ 합치기 (Q9 §3-4)'", "    if False and diff:\n        return f'출처 칸 {diff} ≠ 합치기 (Q9 §3-4)'")], ['D5e']),
    ('M5', 'redo', 'recover_ledger — 시작 기록의 바탕 ↔ 이 폴더의 바탕 대조를 끔',
     [("            if s0 is not None and s0['base'] != fb:", "            if False and s0 is not None and s0['base'] != fb:")], ['D6d']),
    ('M6', 'redo', 'target_ledger_problem — 한 항목 = 폴더 하나 (같은 이름 둘) 멈춤을 끔',
     [("        if len(hit) > 1:                                      # ★ 10-27 묶음 C2d — 한 항목 = 폴더 하나",
       "        if False and len(hit) > 1:                            # ★ 10-27 묶음 C2d — 한 항목 = 폴더 하나")], ['D6e']),
    ('M7', 'redo', 'target_ledger_problem — 폴더 없는 시도 (엄격 · 결과 뒤로 봄) 멈춤을 끔 (그 시도를 건너뜀)',
     [("            raise Stop('ATTEMPT_LEDGER_MISMATCH', f'항목 {k} ({target}) 의 시도 폴더 · 거부 기록 {r[\"folder\"]} 이 없다 (엄격 — 결과 뒤로 본다 · 그 대상 '\n"
       "                                                  f'판정 없음 · 다른 곳에 둔 시도 = 판정 --attempt-dirs · 합치기 --merge 경로)')",
       "            continue")], ['D6e']),
    ('M10', 'redo', 'found_attempts_problem — 시도 폴더 attempt.json ↔ 원장 항목 (대상 · 기계 · 재실행 원 시도) 대조를 끔',
     [("            d = attempt_entry_diff(a, k, e)                     # ★ 11-09 Codex 회차 ④ — 대조 = 공통 검증 ⓐ 와 한 함수 (사유 글 · 동작 그대로)\n            if d is not None:",
       "            d = attempt_entry_diff(a, k, e)                     # ★ 11-09 Codex 회차 ④ — 대조 = 공통 검증 ⓐ 와 한 함수 (사유 글 · 동작 그대로)\n            if False and d is not None:")],
     ['D6j']),
    ('M11', 'upto', 'attempt_order_problem — 재실행 항목의 기계 · 환경 지문 = 원 시도 대조를 끔',
     [("    if e['machine'] != o['machine'] or e['env'] != o['env']:\n        return ('RESUME_NOT_ALLOWED', f'재실행 기계 · 환경 지문",
       "    if False and (e['machine'] != o['machine'] or e['env'] != o['env']):\n        return ('RESUME_NOT_ALLOWED', f'재실행 기계 · 환경 지문")], ['D6i']),
    ('M12', 'upto', 'attempt_presolve_problem — 재실행 원천 = 같은 바탕의 사슬 끝 시도 폴더 대조를 끔 (첫 방어선만)', [SRCBASE], ['D6i']),
    ('M12b', 'upto', 'M12 + resume_chain_problem — 재실행 사슬 시도의 폴더가 같은 바탕에 하나 대조도 끔 (없으면 건너뜀)',
     [SRCBASE, ("        if len(cand) != 1:\n            return ('RESUME_NOT_ALLOWED', f'재실행 사슬 시도 {k} 의 폴더",
                "        if not cand:\n            continue\n        if len(cand) != 1:\n            return ('RESUME_NOT_ALLOWED', f'재실행 사슬 시도 {k} 의 폴더")], ['D6i']),
]


def main():
    res = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
    for name, mode, what, edits, want in MUT:
        if ONLY and name not in ONLY:
            continue
        d = os.path.join(HERE, 'mut', name)
        shutil.rmtree(d, ignore_errors=True)
        shutil.copytree(os.path.join(TREE, 'scripts'), os.path.join(d, 'scripts'), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for rel in EXTRA:
            os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
            shutil.copy2(os.path.join(TREE, rel), os.path.join(d, rel))
        p = os.path.join(d, 'scripts', 'rint_r_chain.py')
        s = open(p, encoding='utf-8').read()
        bad = [o[:60] for o, _n in edits if s.count(o) != 1]
        if bad:
            res[name] = {'what': what, 'mode': mode, 'error': f'고칠 자리를 하나로 못 찾음 {bad}'}
            print(name, res[name]['error'], flush=True)
            shutil.rmtree(d, ignore_errors=True)
            continue
        for o, n in edits:
            s = s.replace(o, n)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(s)
        t0 = time.time()
        tmp = os.path.join(HERE, 'tmp_mut')
        os.makedirs(tmp, exist_ok=True)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', TMPDIR=tmp)
        argv = ['--reuse', WORLD, '--redo', name.lower()] if mode == 'redo' else ['--upto', 'D3']
        r = subprocess.run([sys.executable, os.path.join(d, 'scripts', 'test_rint_r_chain_e2e12.py')] + argv, capture_output=True, text=True, env=env)
        so = r.stdout + r.stderr
        fails = sorted(set(re.findall(r'^  FAIL  (\S+)', so, re.M)))
        passes = sorted(set(re.findall(r'^  PASS  (\S+)', so, re.M)))
        why = {}
        for ln in so.splitlines():
            m = re.match(r'  FAIL  (\S+).*?  \((.*)$', ln)
            if m:
                why[m.group(1)] = m.group(2)[:1500]
        ok = (not fails and r.returncode == 0) if not want else (r.returncode != 0 and all(w in fails for w in want))
        res[name] = {'what': what, 'mode': mode, 'want_fail': want, 'rc': r.returncode, 'fail': fails, 'pass': passes, 'why': why, 'caught': ok,
                     'seconds': round(time.time() - t0, 1), 'tail': so[-400:]}
        print(name, mode, 'rc', r.returncode, 'FAIL', fails, 'PASS', passes, f'{res[name]["seconds"]} s', '→',
              ('대조 통과' if ok else '대조 실패') if not want else ('잡음' if ok else '못 잡음'), flush=True)
        with open(OUT, 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=1)
        shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
