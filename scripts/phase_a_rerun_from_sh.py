#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase A STEP3 재실행 스크립트 생성기 — **봉인 이탈만** 고치고 나머지는 한 글자도 안 건드린다.

    python3 scripts/phase_a_rerun_from_sh.py --in <원본 .sh 들이 있는 디렉터리> \
        --out-dir <새 .sh 를 쓸 디렉터리> --payload-dir <payload 출력 디렉터리>
    python3 scripts/phase_a_rerun_from_sh.py --selftest

━━ 왜 명령을 새로 짓지 않는가 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2026-09-18 실측 — Phase A 96팔이 `ptfe_stamp=off` 로 돌았다.  사전등록 §5 봉인은
`ptfe_stamp = centerline ∧ sigma_ptfe = 0` (exact-zero DOF) 다.  ★ **직전 32팔은
`centerline` + `code_sha=70b9e37a` 로 제대로 돌았다** (`docs/data/phase_a_h015_arms/
_adapter_summary.json`) ⇒ 코드도 규약 이해도 문제가 아니었고, **띄운 셸에 `PTFE_STAMP`
가 없었다**.  두 receipt 의 차이가 정확히 `ptfe_stamp` 와 `code_sha` 둘뿐이다.

⇒ 원본 `.sh` 가 **실행 기록 그 자체**이므로 거기서 **등록된 이탈만** 고친다.
  명령을 새로 지으면 다른 축(vox·bridge·origin·sigma-vgcf·dilate-z…)이 같이 움직일
  위험이 있고, 그것이 이 리포가 반복해서 당한 사고다.

━━ 고치는 것 — **이 목록이 계약이다** ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ① + `--ptfe-stamp centerline`              사전등록 §5 봉인
  ② + LEAN=2 플래그 7개                       §5 `--no-ion --no-pore (σ_e 전용)`
  ③ − `--joule-heat`                          LEAN=2 와 모순 (STEP4 를 끈다)
  ④ − `--save-step4-grid <값>`                STEP4 를 끄므로 무의미
  ⑤ ~ `--expect-physics` 에 `ptfe_stamp`·`sigma_ptfe_S_cm` 추가
       ★ 이번 사고의 **근본 원인**이 여기다 — 러너에 계약 검사기가 있는데 봉인 축이
         **선언 목록에 없어서** 검사 대상이 아니었다.  선언 안 한 축은 검사도 안 된다.
  ⑥ ~ `--out` 을 새 디렉터리로                원본 payload 를 덮지 않는다

⛔ 그 외 토큰이 하나라도 바뀌면 **거부**한다 — 생산은 텍스트 수술로 하고 **검증은
  `shlex` 토큰 다중집합 차이**로 한다 (생산 경로와 검증 경로를 일부러 다르게 둔다;
  같은 함수로 확인하면 순환이다).
"""
from __future__ import annotations

import argparse
import difflib
import glob
import os
import re
import shlex
import sys

#  ── 등록된 변경 집합 (이 상수들이 계약이다) ────────────────────────────────
PTFE_FLAG = ['--ptfe-stamp', 'centerline']
LEAN2_FLAGS = ['--no-step4', '--no-thermal', '--no-trackb', '--no-field',
               '--no-ion', '--no-pore', '--no-collector']
DROP_BARE = ['--joule-heat']
DROP_WITH_VALUE = ['--save-step4-grid']
EXPECT_ADD = ('ptfe_stamp=centerline', 'sigma_ptfe_S_cm=0.0')
PAYLOAD_CALL = 'mpm_webapp_payload.py'


def _cmd_span(text):
    """`python3 …mpm_webapp_payload.py …` 호출의 (시작, 끝) 문자 오프셋.

    줄끝 `\\` 연속을 따라간다.  ⚠ 호출이 없거나 둘 이상이면 거부한다 — 어느 쪽을
    고칠지 모호한 채로 진행하지 않는다.
    """
    starts = [m.start() for m in re.finditer(r'^[^\n#]*\bpython3\b[^\n]*'
                                             + re.escape(PAYLOAD_CALL), text, re.M)]
    if len(starts) != 1:
        raise ValueError(f'{PAYLOAD_CALL} 호출이 {len(starts)}개다 — 정확히 1개여야 한다')
    i = starts[0]
    j = i
    while True:
        nl = text.find('\n', j)
        if nl < 0:
            return i, len(text)
        line = text[j:nl]
        if not line.rstrip().endswith('\\'):
            return i, nl
        j = nl + 1


def has_payload_call(text):
    """이 `.sh` 가 payload 호출을 담고 있나.  ⚠ **조용히 건너뛰지 않는다** — main() 이
    건너뛴 파일을 **전부 이름으로 보고**하고, `--expect-count` 가 총 개수를 계약으로
    박는다.  (2026-09-18: 킷 디렉터리에 `harvest.sh` 처럼 payload 가 아닌 `.sh` 가 있다.
    그것을 말없이 넘기면 "몇 개를 왜 안 만들었는지" 가 사라지고, 그게 규율 ⑤ 의
    false-green 이다.)"""
    return len(re.findall(r'^[^\n#]*\bpython3\b[^\n]*' + re.escape(PAYLOAD_CALL),
                          text, re.M))


def _tokens(cmd_text):
    """검증 전용 토큰화.  `\\`+개행을 지우고 shlex 로 자른다."""
    return shlex.split(cmd_text.replace('\\\n', ' '), posix=True)


def _expect_physics_value(tokens):
    for k, t in enumerate(tokens):
        if t == '--expect-physics' and k + 1 < len(tokens):
            return tokens[k + 1]
    return None


def applied_vox(text):
    """이 `.sh` 가 **실제로 적용하는** vox.  ⚠ `--step3-vox` 는 한 줄에 **두 번** 나오고
    argparse 는 **뒤를 쓴다** (2026-09-18 에 내가 `head -1` 로 앞만 보고 "세 격자가 전부
    0.4" 라고 오판했다 — 도구가 답을 정한 여섯 번째 사례)."""
    v = re.findall(r'--step3-vox[ \t]+(\S+)', text[slice(*_cmd_span(text))])
    if not v:
        raise ValueError('--step3-vox 가 없다')
    return v[-1]


def transform(text, payload_dir):
    """원본 `.sh` 전문 → 고친 전문.  **텍스트 수술**(따옴표·배열 확장 보존)."""
    i, j = _cmd_span(text)
    cmd = text[i:j]

    #  ③ 맨 플래그 제거
    for f in DROP_BARE:
        cmd = re.sub(r'[ \t]*' + re.escape(f) + r'(?=[ \t\\\n])', '', cmd)
    #  ④ 값 있는 플래그 제거
    for f in DROP_WITH_VALUE:
        cmd = re.sub(r'[ \t]*' + re.escape(f) + r'[ \t]+\S+', '', cmd)

    #  ⑤ --expect-physics 확장
    m = re.search(r'(--expect-physics[ \t]+)(\S+)', cmd)
    if not m:
        raise ValueError('--expect-physics 가 없다 — 이 러너 산출물이 아니다')
    have = m.group(2)
    add = [a for a in EXPECT_ADD if a.split('=')[0] + '=' not in have]
    if add:
        cmd = cmd[:m.start(2)] + have + ',' + ','.join(add) + cmd[m.end(2):]

    #  ⑥ --out 재지정
    m = re.search(r'(--out[ \t]+)(\S+)', cmd)
    if not m:
        raise ValueError('--out 이 없다')
    base = os.path.basename(m.group(2))
    cmd = cmd[:m.start(2)] + os.path.join(payload_dir, base) + cmd[m.end(2):]

    #  ①② 삽입 — `--out` 앞에 둔다 (읽는 사람이 바뀐 곳을 한 자리에서 본다)
    m = re.search(r'[ \t]*--out[ \t]+\S+', cmd)
    ins = ' ' + ' '.join(PTFE_FLAG + LEAN2_FLAGS)
    cmd = cmd[:m.start()] + ins + cmd[m.start():]

    return text[:i] + cmd + text[j:]


def assert_only_registered_changes(old_text, new_text):
    """⛔ 등록 밖 인자가 움직였으면 거부.  **생산과 다른 경로**(shlex)로 검증한다."""
    a, b = _tokens(old_text[slice(*_cmd_span(old_text))]), \
        _tokens(new_text[slice(*_cmd_span(new_text))])

    exp_a, exp_b = _expect_physics_value(a), _expect_physics_value(b)
    out_a, out_b = None, None
    for src, tgt in ((a, 'a'), (b, 'b')):
        for k, t in enumerate(src):
            if t == '--out' and k + 1 < len(src):
                if tgt == 'a':
                    out_a = src[k + 1]
                else:
                    out_b = src[k + 1]

    def _norm(toks, exp, out):
        """등록된 변경 자리를 같은 자리표로 치환해 **나머지만** 비교한다."""
        r = []
        skip = 0
        for k, t in enumerate(toks):
            if skip:
                skip -= 1
                continue
            if t in DROP_BARE:
                continue
            if t in DROP_WITH_VALUE:
                skip = 1
                continue
            if t in LEAN2_FLAGS:
                continue
            if t == '--ptfe-stamp':
                skip = 1
                continue
            if t == exp or (out is not None and t == out):
                r.append('<REGISTERED>')
                continue
            r.append(t)
        return r

    na, nb = _norm(a, exp_a, out_a), _norm(b, exp_b, out_b)
    if na != nb:
        d = '\n'.join(difflib.unified_diff(na, nb, '원본', '생성', lineterm='', n=1))
        raise ValueError('⛔ 등록 밖 인자가 움직였다 — 생성하지 않는다:\n' + d)

    #  등록 자리 자체도 **방향**을 확인한다 (사라지기만 하면 안 된다)
    if '--ptfe-stamp' not in b or b[b.index('--ptfe-stamp') + 1] != 'centerline':
        raise ValueError('⛔ --ptfe-stamp centerline 이 안 들어갔다')
    for f in LEAN2_FLAGS:
        if f not in b:
            raise ValueError(f'⛔ LEAN=2 플래그 {f} 가 안 들어갔다')
    for f in DROP_BARE + DROP_WITH_VALUE:
        if f in b:
            raise ValueError(f'⛔ {f} 가 안 빠졌다')
    for need in EXPECT_ADD:
        if need not in (exp_b or ''):
            raise ValueError(f'⛔ --expect-physics 에 {need} 가 없다')
    if out_a == out_b:
        raise ValueError('⛔ --out 이 그대로다 — 원본 payload 를 덮는다')
    return True


def convert(src, dst, payload_dir):
    old = open(src, encoding='utf-8').read()
    new = transform(old, payload_dir)
    assert_only_registered_changes(old, new)
    os.makedirs(os.path.dirname(dst) or '.', exist_ok=True)
    with open(dst, 'w', encoding='utf-8') as fh:
        fh.write(new)
    os.chmod(dst, 0o755)
    return old, new


# ─────────────────────────────── selftest ───────────────────────────────
_FIX = '''set -uo pipefail
KIT="/home/ubuntu/pa/kits/VGCF_PTFE_1_1"
SCR="/home/ubuntu/Yonghoon-DEM-DFT/scripts"
PSIG=()
python3 "$SCR/mpm_webapp_payload.py" \\
  --se se_dump.npy --scaffold "$KIT/am_scaffold.csv" --se-dump "$KIT/se_scaffold.csv" \\
  --n-vox 192 --tri-step 4 --smooth 1.5 --target-porosity 0.1447 --eps se_dump_eps.npy --dilate-z 1.0214 \\
  --void-max 180000 --step3-vox 0.4 --field-max-points 90000 --step3-gpu --joule-heat "${PSIG[@]}" \\
  --metrics-json mpm_metrics.json --case input_6mAh_real_4 --phase phase.npy --fibre fibre.npy \\
  --fibre-dia fibre_dia.npy --save-step4-grid step4_grid_p2_a0.npz --step3-fibre-stamp segment \\
  --sigma-vgcf 44.1786 --step3-vox 0.20 --step3-bridge-um 0.24 --step3-origin-shift 0 0 0 \\
  --step3-require-gpu --expect-physics vox_um=0.20,bridge_um=0.24,fibre_stamp=segment \\
  --out p2_VGCF_PTFE_1_1_a0.json
'''


def _selftest():
    ok = [0, 0]

    def chk(name, cond):
        ok[1] += 1
        ok[0] += bool(cond)
        print(f"  {'✓' if cond else '✗'} {name}")

    new = transform(_FIX, '/tmp/out')
    t = _tokens(new[slice(*_cmd_span(new))])

    chk('① --ptfe-stamp centerline 이 들어간다',
        '--ptfe-stamp' in t and t[t.index('--ptfe-stamp') + 1] == 'centerline')
    chk('② LEAN=2 플래그 7개가 전부 들어간다', all(f in t for f in LEAN2_FLAGS))
    chk('③ --joule-heat 가 빠진다', '--joule-heat' not in t)
    chk('④ --save-step4-grid 가 값과 함께 빠진다',
        '--save-step4-grid' not in t and not any(x.endswith('.npz') for x in t))
    exp = _expect_physics_value(t)
    chk('⑤ --expect-physics 에 봉인 2축이 추가된다',
        all(a in exp for a in EXPECT_ADD) and 'vox_um=0.20' in exp)
    chk('⑥ --out 이 새 디렉터리로 간다',
        t[t.index('--out') + 1] == '/tmp/out/p2_VGCF_PTFE_1_1_a0.json')
    chk('⑦ 등록 밖 인자는 안 움직인다 (검증기 통과)',
        assert_only_registered_changes(_FIX, new))
    for key in ('--dilate-z', '1.0214', '--sigma-vgcf', '44.1786',
                '--step3-bridge-um', '0.24', '--step3-origin-shift', '--case',
                'input_6mAh_real_4', '--step3-fibre-stamp', 'segment'):
        pass
    chk('⑧ 침대·규약 인자가 보존된다',
        all(k in t for k in ('--dilate-z', '1.0214', '--sigma-vgcf', '44.1786',
                             '--step3-bridge-um', '0.24', '--case', 'input_6mAh_real_4',
                             '--step3-fibre-stamp', 'segment')))
    chk('⑨ `"${PSIG[@]}"` 배열 확장이 따옴표째 보존된다', '"${PSIG[@]}"' in new)
    chk('⑩ `"$KIT/..."` 인용 경로가 보존된다', '"$KIT/am_scaffold.csv"' in new)
    chk('⑪ 중복 --step3-vox 순서가 보존된다 (argparse last-wins)',
        [x for x in t if x in ('0.4', '0.20')] == ['0.4', '0.20'])

    #  ── 음성 대조: 검증기가 실제로 발화하는가 (⑦ 이 장식이 아님을 보인다) ──
    def neg(name, mutate):
        try:
            assert_only_registered_changes(_FIX, mutate(transform(_FIX, '/tmp/out')))
            chk(name, False)
        except ValueError:
            chk(name, True)

    neg('⑫ ★ 등록 밖 인자(--dilate-z)를 바꾸면 거부',
        lambda s: s.replace('--dilate-z 1.0214', '--dilate-z 1.0999'))
    neg('⑬ ★ 침대 파일(--phase)을 바꾸면 거부',
        lambda s: s.replace('--phase phase.npy', '--phase other.npy'))
    neg('⑭ ★ LEAN 플래그를 하나 지우면 거부',
        lambda s: s.replace(' --no-ion', ''))
    neg('⑮ ★ --ptfe-stamp 를 off 로 바꾸면 거부',
        lambda s: s.replace('--ptfe-stamp centerline', '--ptfe-stamp off'))
    neg('⑯ ★ --out 을 원본으로 되돌리면 거부 (원본 덮기)',
        lambda s: s.replace('/tmp/out/p2_VGCF_PTFE_1_1_a0.json', 'p2_VGCF_PTFE_1_1_a0.json'))

    #  ── 호출이 0개/2개면 거부 ──
    for n, txt in (('0개', 'echo hi\n'), ('2개', _FIX + _FIX)):
        try:
            transform(txt, '/tmp/out')
            chk(f'⑰ payload 호출이 {n} 면 거부', False)
        except ValueError:
            chk(f'⑰ payload 호출이 {n} 면 거부', True)

    chk('⑱ 적용 vox 는 **마지막** --step3-vox 다 (argparse last-wins)',
        applied_vox(_FIX) == '0.20')
    chk('⑲ --payload-dir 의 {vox} 가 치환된다',
        _tokens(transform(_FIX, '/tmp/o/{vox}'.replace('{vox}', 'v020'))
                [slice(*_cmd_span(transform(_FIX, '/tmp/o/v020')))])
        [_tokens(transform(_FIX, '/tmp/o/v020')[slice(*_cmd_span(
            transform(_FIX, '/tmp/o/v020')))]).index('--out') + 1]
        == '/tmp/o/v020/p2_VGCF_PTFE_1_1_a0.json')

    chk('⑳ payload 호출 유무를 센다 (harvest.sh 류 판별)',
        has_payload_call(_FIX) == 1 and has_payload_call('echo hi\n') == 0
        and has_payload_call(_FIX + _FIX) == 2)

    print(f"\nphase_a_rerun_from_sh selftest: {ok[0]}/{ok[1]} "
          f"{'PASS' if ok[0] == ok[1] else 'FAIL'}")
    return 0 if ok[0] == ok[1] else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description='Phase A STEP3 재실행 .sh 생성기')
    ap.add_argument('--in', dest='src', help='원본 .sh 디렉터리 (재귀)')
    ap.add_argument('--out-dir', help='새 .sh 를 쓸 디렉터리')
    ap.add_argument('--payload-dir', help='새 payload 를 쓸 디렉터리 (--out 이 여기로)')
    ap.add_argument('--expect-count', type=int, default=None,
                    help='생성돼야 하는 .sh 수.  다르면 거부한다 (부분집합 방지)')
    ap.add_argument('--show-diff', action='store_true', help='첫 파일의 diff 를 찍는다')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return _selftest()
    if not (a.src and a.out_dir and a.payload_dir):
        ap.error('--in --out-dir --payload-dir 이 전부 필요하다')

    files = sorted(glob.glob(os.path.join(a.src, '**', '*.sh'), recursive=True))
    if not files:
        print(f'⛔ {a.src} 에 .sh 가 없다 — 빈 glob 로 진행하지 않는다', file=sys.stderr)
        return 2

    n, first, seen_out, skipped = 0, None, {}, []
    for p in files:
        _txt = open(p, encoding='utf-8').read()
        _k = has_payload_call(_txt)
        if _k == 0:
            skipped.append(p)
            continue
        if _k > 1:
            print(f'⛔ {p}: payload 호출이 {_k}개다 — 어느 것을 고칠지 모호하다',
                  file=sys.stderr)
            return 3
        dst = os.path.join(a.out_dir, os.path.relpath(p, a.src))
        try:
            vox = applied_vox(open(p, encoding='utf-8').read())
            pdir = a.payload_dir.replace('{vox}', 'v' + vox.replace('.', ''))
            old, new = convert(p, dst, pdir)
        except ValueError as e:
            print(f'⛔ {p}: {e}', file=sys.stderr)
            return 3
        outp = _tokens(new[slice(*_cmd_span(new))])
        outp = outp[outp.index('--out') + 1]
        #  ⛔ 같은 --out 을 두 스크립트가 쓰면 **조용히 덮어쓴다** — 원본 96팔이
        #    격자마다 같은 파일명을 쓰기 때문에 실제로 일어나는 사고다.
        if outp in seen_out:
            print(f'⛔ --out 충돌: {outp}\n  {seen_out[outp]}\n  {p}\n'
                  f'  ⇒ --payload-dir 에 `{{vox}}` 를 넣어 격자별로 가를 것',
                  file=sys.stderr)
            return 4
        seen_out[outp] = p
        if first is None:
            first = (p, old, new)
        n += 1

    if skipped:
        print(f'ⓘ payload 호출이 없어 건너뛴 .sh {len(skipped)}개 (조용히 넘기지 않는다):')
        for q in skipped:
            print(f'    - {q}')
    print(f'✓ {n} 개 생성 → {a.out_dir}   (payload → {a.payload_dir})')
    if a.expect_count is not None and n != a.expect_count:
        print(f'⛔ 생성 수 {n} ≠ --expect-count {a.expect_count} — 부분집합으로 진행하지 '
              f'않는다 (규율 ⑤).  건너뛴 목록을 확인할 것.', file=sys.stderr)
        return 5
    if a.show_diff and first:
        p, old, new = first
        print(f'\n── diff (첫 파일 {os.path.basename(p)}) ──')
        for ln in difflib.unified_diff(old.splitlines(), new.splitlines(),
                                       '원본', '생성', lineterm='', n=1):
            print(ln)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
