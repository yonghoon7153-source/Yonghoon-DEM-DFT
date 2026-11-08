#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RR3-01 새 가드 변이 — 리포 밖 사본 트리 (고친 판 · 끝 시험 파일) 의 scripts/rint_r_chain.py 에서 가드를 하나씩 끄거나 약하게 하고 (정확한 글 바꿈 · 한 번) 새 시험
(RR3A–E · RR3P) + 이웃 (CT06 · PC12C · RS01) 을 돌린다 · 매번 원 바이트로 되돌리고 sha256 확인 · 무변이 = 전부 통과 확인.  잡힘 = 새 시험 하나 이상 실패.

  python3 mutate_rr3.py <사본 트리> <out.json>
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
C = TREE / 'scripts' / 'rint_r_chain.py'
NEW = ('RR3A', 'RR3B', 'RR3C', 'RR3D', 'RR3E', 'RR3P')
ONLY = 'RR3,CT06,PC12C,RS01'

K_IF = "        if not (type(f) is str and os.path.basename(f) == f and f.startswith(pref) and f.endswith(f'_a{i}.json')):\n"
S_IF = "        if not (type(h) is str and ARM_SHA256_RE.fullmatch(h)):\n"
MUTANTS = [
    ('M01_prior_old_rule', '`prior_runs_problem` = 옛 규칙 (비지 않은 목록)',
     "        if sh != 'exit_ok' or kind != 'verified':\n",
     "        if sh != 'exit_ok' or not (type(r.get('arms_read')) is list and r.get('arms_read')):\n"),
    ('M02_file_ids_as_verified', '분류: 파일 신원 꼴 = verified',
     "        return 'file_ids', f'파일 신원 {len(ar)} = 판독 실패 때 남긴 꼴'\n", "        return 'verified', None\n"),
    ('M03_keyset_off', '분류: 칸 집합 = ARM_PUBLIC 검사 끔',
     "    if any(set(a) != set(ARM_PUBLIC) for a in ar):\n        return 'bad', '칸 집합 ≠ ARM_PUBLIC (판독 완료 꼴) · ≠ 파일 신원'\n", ''),
    ('M04_dict_off', '분류: 원소 객체 검사 끔',
     "    if any(type(a) is not dict for a in ar):\n        return 'bad', '원소가 객체가 아님'\n", ''),
    ('M05_list_off', '분류: 목록 검사 끔',
     "    if type(ar) is not list:\n        return 'bad', f'목록 아님 ({type(ar).__name__})'\n", ''),
    ('M06_empty_off', '분류: 빈 목록 갈래 끔',
     "    if not ar:\n        return 'empty', None\n", ''),
    ('M07_request_off', '분류: 요청 칸 검사 끔',
     "    if type(rec) is not dict or 'arms' not in rec or request_fields_problem(rec):\n"
     "        return 'bad', '요청 칸 (arms · arm_list) 없음 · 생산자 범위 밖 = 요청 팔을 모른다'\n", ''),
    ('M08_request_range_off', '분류: 요청 칸 = 있음만 (생산자 범위 검사 끔)',
     "    if type(rec) is not dict or 'arms' not in rec or request_fields_problem(rec):\n", "    if type(rec) is not dict or 'arms' not in rec:\n"),
    ('M09_kit_type_off', '분류: kit 글 검사 끔',
     "    if type(kit) is not str:\n        return 'bad', f'kit {kit!r}'\n", ''),
    ('M10_count_off', '분류: 팔 수 = 요청 팔 수 검사 끔',
     "    if len(ar) != len(idx):\n        return 'bad', f'팔 {len(ar)} ≠ 요청 팔 {len(idx)}'\n", ''),
    ('M11_index_type_off', '분류: 번호 = 정수 (bool 아님) 검사 끔',
     "        if type(x) is not int or x != i:\n", "        if x != i:\n"),
    ('M12_index_eq_off', '분류: 번호 = 요청 팔 검사 끔',
     "        if type(x) is not int or x != i:\n", "        if type(x) is not int:\n"),
    ('M13_file_type_off', '분류: 파일 = 글 검사 끔', K_IF,
     "        if not (os.path.basename(f) == f and f.startswith(pref) and f.endswith(f'_a{i}.json')):\n"),
    ('M14_file_basename_off', '분류: 파일 = 이름만 검사 끔', K_IF,
     "        if not (type(f) is str and f.startswith(pref) and f.endswith(f'_a{i}.json')):\n"),
    ('M15_file_prefix_off', '분류: 파일 킷 앞자리 검사 끔', K_IF,
     "        if not (type(f) is str and os.path.basename(f) == f and f.endswith(f'_a{i}.json')):\n"),
    ('M16_file_suffix_off', '분류: 파일 끝 _a<번호>.json 검사 끔', K_IF,
     "        if not (type(f) is str and os.path.basename(f) == f and f.startswith(pref)):\n"),
    ('M17_sha_off', '분류: sha256 꼴 검사 끔',
     S_IF + "            return 'bad', f'[{j}].sha256 = 64 자리 소문자 hex 아님'\n", ''),
    ('M18_sha_match_not_full', '분류: sha256 fullmatch → match', S_IF,
     "        if not (type(h) is str and ARM_SHA256_RE.match(h)):\n"),
    ('M19_sha_type_off', '분류: sha256 = 글 검사 끔', S_IF, "        if not ARM_SHA256_RE.fullmatch(h):\n"),
    ('M20_gen_success_ids', '생성: 성공 = 파일 신원 칸만 (ARM_PUBLIC 투영 아님)',
     "    return [{k: a[k] for k in ARM_PUBLIC} for a in arms_]\n", "    return [{k: a[k] for k in ARM_FILE_ID_KEYS} for a in arms_]\n"),
    ('M21_gen_failure_empty', '생성: 실패 = [] (파일 신원 안 남김)',
     "    if arms_ is None:\n        return arm_file_shas(outdir)\n", "    if arms_ is None:\n        return []\n"),
    ('M22_execute_bypass', '생산자: Runner._execute 성공 = 옛 안쪽 투영 (생성 함수 우회)',
     "        rec['arms_read'] = arms_read_record(arms_)\n        a0 = arms_[0]\n",
     "        rec['arms_read'] = [{k: a[k] for k in ARM_PUBLIC} for a in arms_]\n        a0 = arms_[0]\n"),
    ('M23_merge_failure_bypass', '생산자: MergeFetch.run 실패 = arm_file_shas 직접 (생성 함수 우회)',
     "            rec['arms_read'] = arms_read_record(outdir=outdir)    # ★ 11-08 RR3-01 — 생성 한 함수 (사본 다시 읽기 실패 = 파일 신원)\n",
     "            rec['arms_read'] = arm_file_shas(outdir)\n"),
]


def run_tests():
    p = subprocess.run([sys.executable, 'scripts/test_rint_r_chain.py', '--only', ONLY], cwd=str(TREE), capture_output=True, text=True)
    res = {}
    for ln in p.stdout.splitlines():
        m = re.match(r'  (PASS|FAIL)  (\S+) ', ln)
        if m:
            res[m.group(2)] = m.group(1)
    tail = [ln for ln in p.stdout.splitlines() if ln.startswith('test_rint_r_chain:')]
    return p.returncode, res, tail[-1] if tail else p.stdout[-300:] + p.stderr[-300:]


def main():
    orig = C.read_bytes()
    sha0 = hashlib.sha256(orig).hexdigest()
    out = {'tree': str(TREE), 'chain_sha256': sha0, 'only': ONLY, 'new_checks': list(NEW), 'mutants': []}
    rc, res, tail = run_tests()
    out['sanity'] = {'rc': rc, 'checks': res, 'tail': tail, 'all_pass': rc == 0 and all(v == 'PASS' for v in res.values()) and len(res) == 9}
    print('무변이:', tail)
    for name, what, old, new in MUTANTS:
        src = orig.decode('utf-8')
        n = src.count(old)
        row = {'name': name, 'guard': what, 'sites': n}
        if n != 1:
            row['error'] = f'옛 글 {n} 번'
            out['mutants'].append(row)
            print(name, 'ERROR sites', n)
            continue
        C.write_bytes(src.replace(old, new).encode('utf-8'))
        try:
            rc, res, tail = run_tests()
        finally:
            C.write_bytes(orig)
        failed = sorted(k for k, v in res.items() if v == 'FAIL')
        row.update(rc=rc, failed=failed, failed_new=[k for k in failed if k in NEW], caught=any(k in NEW for k in failed), tail=tail)
        out['mutants'].append(row)
        print(name, 'caught' if row['caught'] else 'SURVIVED', failed, '|', tail)
    out['restored_sha256'] = hashlib.sha256(C.read_bytes()).hexdigest()
    out['restored_ok'] = out['restored_sha256'] == sha0
    out['caught'] = sum(1 for r in out['mutants'] if r.get('caught'))
    out['total'] = len(MUTANTS)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f"잡힘 {out['caught']}/{out['total']} · 되돌림 sha 같음 {out['restored_ok']} · 무변이 전부 통과 {out['sanity']['all_pass']}")
    return 0 if out['caught'] == out['total'] and out['restored_ok'] and out['sanity']['all_pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
