#!/usr/bin/env python3
"""팔 payload 를 **판정에 필요한 부분만** 남겨 축소한다 (R8 Q6 ⓐ · R9 Q5 종료조건).

★ 왜: 생산 payload 는 LEAN=2(σ_e 전용)에서도 팔당 **127 MB** 다 — 시각화 배열이 함께
  들어간다.  16팔 디렉터리가 2.0 GB 이고 32팔이면 4 GB 라 **git 에 넣을 수 없다**.
  그런데 R8 Q6 [P1] 의 종료조건은 *"16팔 JSON·receipt 커밋"* 이고, 그것이 없으면
  `table_s3_data_20260827.md` §9 의 provenance 대조는 **한 기계에만 있는 파일에 대한
  서술**이라 제3자가 재실행할 수 없다.

★★ 설계 원칙 — **축소본을 판정기가 그대로 읽는다.**  출력 파일명을 `p2_*.json` 으로
  유지하고 `{'step3': {...}}` 구조로 쓴다 ⇒ `sdcp_gain_verdict.py --dir <축소본>` 이
  원본과 **똑같이** 동작한다.  커밋된 것이 **설명**이 아니라 **실행 가능한 증거**가 된다.

⚠⚠ **초판(2026-08-28 오전)은 false-green 을 만들 수 있었다** — Codex R9 Q5 [P1]:
  원본에 `.rejected_*` 가 있으면 판정기는 `REJECTED_TREE` HOLD 를 낸다.  그런데 초판은
  `p2_*.json` 만 가져가 **그 표지를 버렸다** ⇒ **원본은 HOLD 인데 축소본은 판정 가능**.
  "증거를 줄였다" 가 "증거를 유리하게 바꿨다" 가 되는 형태다.  아래 일곱이 그 대응이다:

    ① `.rejected_*` 가 있으면 **축소 자체를 실패**시킨다 (표지를 옮기지 않고 거부한다)
    ② 정확히 `--expect-arms`(기본 16) 팔 · **완전 factorial origin** 을 요구한다
    ③ `step3` 가 없는 파일은 **SKIP 하지 않고 실패**시킨다
    ④ `run_receipt.json` 을 검증·보존한다
    ⑤ 원본과 축소본의 **seal · verdict · collect** 를 canonical 비교한다
    ⑥ cohort manifest 에 파일별 SHA256(원본·축소) · 도구 SHA · 스키마 · 생략 객체 목록을 봉인
    ⑦ 축소본 + receipt + manifest + verdict receipt 를 **함께** 낸다

⚠ **이 패키지의 이름은 `scalar decision-audit package` 다** (R9).  solver·시각화 재생용
  **원자료가 아니다** — 그렇게 부르면 안 된다.

사용:
    python3 scripts/reduce_arm_payloads.py --dir <원본> --out <축소본>
    python3 scripts/reduce_arm_payloads.py --selftest
"""
import argparse
import glob
import hashlib
import json
import os
import subprocess
import sys

MAX_LIST = 64            # 이보다 긴 리스트 = 배열로 보고 버린다 (origin 3원소 등은 남는다)

#: ★ 축소본이 **살려 두는** 최상위 키 (작은 요약만).  큰 배열은 계속 버린다.
#    `econn_summary` = 집전체까지 전자 퍼콜 % · 고립 AM · **탄소 클러스터 수** —
#    웹앱 뷰어가 payload 에서 바로 읽는 값이고 원고 표의 두 행이 여기서 나온다.
TOP_LEVEL_KEEP = ('econn_summary',)
TOP_LEVEL_KEEP_MAX_BYTES = 8192

SCHEMA = 'reduced-arm/2'  # ⚠ 초판(1)은 위 일곱 검사가 없었다 — 버전으로 구분한다
EXPECT_ARMS = 16
_SCR = os.path.dirname(os.path.abspath(__file__))

#  ★★★ 2026-08-31 — **진단 모드** (`--diagnostic`).
#  왜: STEP B 류의 민감도 프로브는 `ARMS=1` 이라 침대당 origin 이 1점이다.  전량 cohort 의
#  게이트 ②③(정확히 16팔 · 침대별 완전 factorial)을 원리적으로 통과할 수 없으므로 축소기가
#  거부해 왔고, 그러면 그 런의 원자료가 **리포에 못 들어온다** = provenance 가 한 기계에만
#  남는다.  그렇다고 `--expect-arms 2` 로 숫자만 낮춰 내보내면 더 나쁘다: 축소본 파일명이
#  `p2_*.json` 이라 **cohort 판정기(`sdcp_gain_verdict.py`)가 그대로 읽고**, 그 판정기는
#  스스로 적어 둔 대로 *"팔 수를 줄인 진단 런은 막지 않는다"* — 즉 부분 cohort 에 대해
#  판정이 난다.  ⇒ 낮추는 것 자체를 **선언**으로 만들고, 산출물에 표지를 박아 cohort
#  판정기가 `DIAGNOSTIC_TREE` 로 격리하게 한다.  표지는 **둘**이다 (아래 참조).
SCHEMA_DIAG = 'reduced-arm/2-diagnostic'
DIAG_CONSUMER = 'scripts/ion_r_verdict.py'
DIAG_SENTINEL = '.diagnostic_arms'          # + <N>  (트리 표지)

#: 진단 축소본이 **비트 동일하게** 옮겨야 하는 step3 필드.
#  = `ion_r_verdict.read_arm` 이 실제로 소비하는 목록 (σ · 이온 수렴 3종).
#  ⚠ 여기에 없는 필드를 그 판정기가 읽기 시작하면 이 검사가 **조용히 약해진다** —
#    `ion_r_verdict.py` 를 고칠 때 이 튜플을 같이 볼 것 (selftest 가 목록을 대조한다).
DIAG_EQUIV_KEYS = ('sigma_ion_eff_S_cm', 'sigma_e_eff_S_cm',
                   'ion_cg_info', 'ion_unconverged', 'ion_resid')


def _step3_of(d):
    return d.get('step3') or (d.get('mpm_metrics') or {}).get('step3') or {}


def _sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def _tool_sha():
    """이 도구가 어느 커밋인가 (없으면 None) — 축소가 언제 어떻게 됐는지의 일부."""
    try:
        r = subprocess.run(['git', '-C', _SCR, 'rev-parse', 'HEAD'],
                           capture_output=True, text=True, timeout=10)
        if r.returncode:
            return None
        d = subprocess.run(['git', '-C', _SCR, 'status', '--porcelain',
                            '--untracked-files=no'], capture_output=True, text=True, timeout=20)
        return r.stdout.strip() + ('+dirty' if (d.stdout or '').strip() else '')
    except Exception:                                              # noqa: BLE001
        return None


def _prune(obj, path, dropped, max_list):
    """긴 배열을 버리고 **버린 경로와 길이를 적는다**.  스칼라·짧은 리스트는 그대로."""
    if isinstance(obj, dict):
        return {k: _prune(v, f'{path}.{k}', dropped, max_list) for k, v in obj.items()}
    if isinstance(obj, list):
        if len(obj) > max_list:
            dropped.append({'path': path, 'len': len(obj)})
            return None
        return [_prune(v, f'{path}[]', dropped, max_list) for v in obj]
    return obj


def reduce_one(path, max_list=MAX_LIST, diagnostic=None):
    """payload 하나 → 축소 dict.  ⚠ `step3` 가 없으면 **예외** (③ — SKIP 하지 않는다).

    `diagnostic` 이 dict 면 **표지 ②** 를 payload 안에 박는다
    (`step3._reduced.diagnostic`).  트리의 `.diagnostic_arms<N>` 파일이 표지 ① 인데,
    그것만 두면 `p2_*.json` 만 복사해 간 순간 표지가 사라진다 — `.rejected_*` 가 실제로
    그렇게 유실돼 false-green 을 냈던 것과 **같은 형태**다 (R9 Q5).  그래서 둘 다 박는다.
    """
    with open(path, encoding='utf-8') as fh:
        d = json.load(fh)
    s = d.get('step3') or (d.get('mpm_metrics') or {}).get('step3')
    if s is None:
        raise ValueError(f'{os.path.basename(path)}: step3 가 없다 — 축소 대상이 아니다')
    dropped = []
    #  manifest 는 통째로 보존한다 (규약 필드가 리스트일 수 있고 §9 대조가 이 블록을 쓴다).
    man = s.get('manifest')
    out = _prune({k: v for k, v in s.items() if k != 'manifest'}, 'step3', dropped, max_list)
    if man is not None:
        out['manifest'] = man
    #  ⚠⚠ `_prune` 는 **step3 안**의 긴 리스트만 적는다.  131 MB → 5.8 kB 의 대부분은
    #  **step3 밖을 통째로 안 가져와서** 줄어든 것이고, 초판은 그것을 **한 줄도 안 남겼다**
    #  — 32팔 전부 `dropped=[]` 라 "아무것도 안 버렸다" 로 읽힌다 (Codex R11 A2).
    #  ⇒ 버린 최상위 키와 그 크기를 적는다.
    top_dropped = [
        {'key': k, 'bytes': len(json.dumps(v, ensure_ascii=False, default=str))}
        for k, v in d.items() if k != 'step3']
    top_dropped.sort(key=lambda x: -x['bytes'])
    #  ★★★ 2026-08-30 — **작은 요약 키는 버리지 않는다.**
    #    `econn_summary` (집전체까지의 전자 퍼콜 % · 고립 AM 수 · **탄소 클러스터 수**)는
    #    생산 payload 가 계산해 싣고(`mpm_webapp_payload.py:1345,2867`) 웹앱 뷰어가 그대로
    #    읽는다(`viewer3d.js:2926`).  그런데 축소본은 그것을 **이름만 남기고 버렸다**
    #    ⇒ 리포만으로는 그 행을 재계산·감사할 수 없고, 적대 리뷰가 "어느 팔에도 없다" 며
    #      **원고에서 빼라고 권고**하는 사태가 났다 (R12).  없는 게 아니라 **축소기가 버렸다.**
    #  ⚠ 허용목록이다 — 큰 배열(점군·필드·삼각형)은 계속 버린다.  여기 키를 더할 때는
    #    **크기 상한**을 같이 본다 (축소본이 다시 무거워지면 커밋 못 한다).
    _kept = {}
    for k in TOP_LEVEL_KEEP:
        v = d.get(k)
        if v is None:
            continue
        _b = len(json.dumps(v, ensure_ascii=False, default=str))
        if _b > TOP_LEVEL_KEEP_MAX_BYTES:
            #  ★★★ 2026-08-30 (Codex R14 D-6) — **`continue` 가 아니라 실패다.**
            #    초판은 사유만 적고 넘어가서 `econn_summary` 가 **없는 축소본을 정상 반환**했다
            #    (내 커밋 메시지의 "거부한다" 도 그래서 거짓이었다).  그 패키지는 아래
            #    검사들을 전부 통과한다 — `check_cohort_packages` 는 `step3` 만 읽기 때문이다.
            #    ⇒ 조용히 불완전한 패키지를 만드느니 **축소 자체를 멈춘다.**
            raise ValueError(
                f'{os.path.basename(path)}: `{k}` 가 {_b} B 로 상한 {TOP_LEVEL_KEEP_MAX_BYTES} B '
                f'를 넘는다.  그것을 빼고 축소하면 **그 행이 없는 패키지**가 조용히 만들어져 '
                f'검사를 통과한다 (R14 D-6).  상한을 올리거나 그 키를 요약해서 줄일 것.')
        _kept[k] = v
    top_dropped = [x for x in top_dropped if x['key'] not in _kept]
    out['_reduced'] = {'source': os.path.basename(path),
                       'top_level_dropped': top_dropped[:40],
                       'top_level_dropped_bytes': sum(x['bytes'] for x in top_dropped),
                       'source_bytes': os.path.getsize(path),
                       'source_sha256': _sha256(path),
                       'dropped': dropped,
                       'schema': SCHEMA if diagnostic is None else SCHEMA_DIAG,
                       'tool': 'scripts/reduce_arm_payloads.py',
                       'tool_commit': _tool_sha(), 'max_list': max_list,
                       'top_level_kept': sorted(_kept)}
    if diagnostic is not None:
        out['_reduced']['diagnostic'] = dict(diagnostic)       # 표지 ② (payload 내부)
    return {'step3': out, **_kept}


def _bits(shift, vox):
    """origin → 정규화 비트 튜플 `{0,½}³` (완전 factorial 확인용)."""
    if shift is None or vox is None:
        return None
    h = float(vox) / 2.0
    out = []
    for t in shift:
        t = abs(float(t))
        if t < h * 0.25:
            out.append(0)
        elif abs(t - h) < h * 0.25:
            out.append(1)
        else:
            return None
    return tuple(out)


def preflight(src_dir, expect_arms, diagnostic=False):
    """축소 **전에** 원본이 판정 대상인지 본다.  실패하면 축소하지 않는다.

    `diagnostic=True` 면 게이트 ③(침대별 완전 8팔 factorial)만 **선언된 대로** 완화한다:
    origin 이 `{0, vox/2}³` 격자 **위**에 있을 것과 침대 안에서 **중복이 없을 것**은
    그대로 요구한다.  ①(기각 표지)·②(정확한 팔 수)·④(receipt)는 건드리지 않는다.
    """
    #  ① 기각 receipt — 표지를 옮기는 대신 **거부**한다.
    rej = sorted(glob.glob(os.path.join(src_dir, '.rejected_*')))
    if rej:
        raise SystemExit('축소 거부 — 원본에 기각 receipt 가 있다: '
                         + ', '.join(os.path.basename(x) for x in rej)
                         + '\n  판정기는 이 tree 에 REJECTED_TREE HOLD 를 낸다.  축소본이'
                           ' 그 표지를 잃으면 **원본은 HOLD 인데 축소본은 판정 가능**해진다.')
    paths = sorted(glob.glob(os.path.join(src_dir, 'p2_*.json')))
    #  ② 팔 수
    if len(paths) != expect_arms:
        raise SystemExit(f'축소 거부 — 팔 {len(paths)}개 (기대 {expect_arms}).  '
                         '불완전한 cohort 는 감사 패키지가 아니다')
    #  ② 완전 factorial origin (침대별로 8개 {0,½}³)
    seen, cnt = {}, {}
    for p in paths:
        j = json.load(open(p, encoding='utf-8'))
        s = j.get('step3') or (j.get('mpm_metrics') or {}).get('step3') or {}
        m = s.get('manifest') or {}
        vox = m.get('vox_um') or s.get('vox_um')
        b = _bits(m.get('origin_shift_um'), vox)
        if b is None:
            raise SystemExit(f'축소 거부 — {os.path.basename(p)} origin 이 {{0,½}}³ 밖이다')
        bed = 'SBE' if '_SBE_' in os.path.basename(p) else 'DBE'
        seen.setdefault(bed, set()).add(b)
        cnt[bed] = cnt.get(bed, 0) + 1
    for bed, bits in sorted(seen.items()):
        if diagnostic:
            #  ⚠ set 은 중복을 **조용히 접는다** — 팔 수와 유일 origin 수를 따로 센다.
            #    (같은 origin 을 두 번 넣어 "팔이 많다" 로 보이게 하는 것을 막는다.)
            if len(bits) != cnt[bed]:
                raise SystemExit(
                    f'축소 거부 — {bed} 의 origin 이 중복이다 (팔 {cnt[bed]} · 유일 '
                    f'{len(bits)}).  진단 모드도 origin 중복은 받지 않는다')
            continue
        if len(bits) != 8:
            raise SystemExit(f'축소 거부 — {bed} origin {len(bits)}/8 (완전 factorial 아님)')
    #  ④ run_receipt.json
    rcpt = os.path.join(src_dir, 'run_receipt.json')
    if not os.path.exists(rcpt):
        raise SystemExit('축소 거부 — run_receipt.json 이 없다 (러너 의도가 봉인되지 않았다)')
    try:
        json.load(open(rcpt, encoding='utf-8'))
    except Exception as ex:                                        # noqa: BLE001
        raise SystemExit(f'축소 거부 — run_receipt.json 을 읽을 수 없다: {ex}')
    return paths, rcpt


_VERDICT = os.path.join(_SCR, 'sdcp_gain_verdict.py')


def _verdict_out(d, mode):
    """판정기를 한 모드로 돌려 stdout 을 돌려준다 (경로는 지운다 — 반드시 다르므로)."""
    r = subprocess.run([sys.executable, _VERDICT, '--dir', d]
                       + ([mode] if mode else []),
                       capture_output=True, text=True, timeout=600)
    txt = (r.stdout or '') + (r.stderr or '')
    return r.returncode, txt.replace(os.path.abspath(d), '<DIR>')


def equivalence(src, dst):
    """⑤ 원본 ↔ 축소본의 **seal · collect · 전체 판정**을 canonical 비교한다.

    ⚠⚠ **양쪽이 똑같이 실패하는 것은 동등이 아니다** (Codex 2026-08-29 지적).
    판정기가 없으면 두 호출이 같은 `No such file` 을 내고 rc 도 같아 **차이 0 = 통과**로
    읽힌다 — 배포 zip 에 `sdcp_gain_verdict.py` 를 안 넣었을 때 실제로 그렇게 됐다.
    ⇒ ⓐ 판정기 **존재**를 먼저 확인하고, ⓑ **원본 쪽 호출이 성공**해야 비교를 인정한다.
    """
    if not os.path.exists(_VERDICT):
        raise SystemExit(
            f'판정기가 없다: {_VERDICT}\n'
            '  ⚠ 이 상태에서는 두 호출이 똑같이 실패해 **거짓 동등**이 된다.\n'
            '     축약기는 리포 안에서 돌려야 한다 (scripts/ 가 함께 있어야 한다).')
    diffs = []
    for mode in ('--seal-only', '--collect-only', None):
        rc_a, out_a = _verdict_out(src, mode)
        rc_b, out_b = _verdict_out(dst, mode)
        name = mode or '(full verdict)'
        if rc_a != 0:
            diffs.append(f'{name}: **원본 판정이 실패했다** (rc {rc_a}) — '
                         '양쪽이 같이 실패하는 것은 동등이 아니다: '
                         + ' '.join(out_a.split())[:160])
            continue
        if rc_a != rc_b or out_a != out_b:
            diffs.append(f'{name}: rc {rc_a} vs {rc_b}'
                         + ('' if out_a == out_b else ' · stdout 불일치'))
    return diffs


def diag_equivalence(paths, out_dir):
    """진단 모드 동등성 — **cohort 판정기를 기준으로 쓰지 않는다.**

    cohort 판정기는 8팔 factorial 을 전제로 하고 이 tree 는 그 전제 밖이다 (그것이 애초에
    `--diagnostic` 인 이유다).  그렇다고 검사를 **생략**하면 그것이 바로 `--skip-equivalence`
    로 가는 길이고, 그 길이 R9 Q5 의 false-green 이었다.  ⇒ 판정기 대신 **소비자
    (`ion_r_verdict.py`)가 실제로 읽는 필드**가 원본↔축소본에서 같은지 직접 본다.
    """
    diffs = []
    for p in paths:
        q = os.path.join(out_dir, os.path.basename(p))
        if not os.path.exists(q):
            diffs.append(f'{os.path.basename(p)}: 축소본이 없다')
            continue
        a = _step3_of(json.load(open(p, encoding='utf-8')))
        b = _step3_of(json.load(open(q, encoding='utf-8')))
        for k in DIAG_EQUIV_KEYS:
            va, vb = a.get(k), b.get(k)
            if (json.dumps(va, sort_keys=True, default=str)
                    != json.dumps(vb, sort_keys=True, default=str)):
                diffs.append(f'{os.path.basename(p)}: {k} {va!r} → {vb!r}')
        ma, mb = a.get('manifest') or {}, b.get('manifest') or {}
        if (json.dumps(ma, sort_keys=True, default=str)
                != json.dumps(mb, sort_keys=True, default=str)):
            diffs.append(f'{os.path.basename(p)}: manifest 불일치 '
                         f'(키 차 {sorted(set(ma) ^ set(mb))[:6]})')
    return diffs


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='팔 payload 를 step3+manifest 만 남겨 축소한다 '
                    '(scalar decision-audit package — 원자료가 아니다)')
    ap.add_argument('--dir', help='원본 팔 디렉터리 (p2_*.json 이 있는 곳)')
    ap.add_argument('--out', help='축소본을 쓸 디렉터리')
    ap.add_argument('--expect-arms', type=int, default=EXPECT_ARMS,
                    help=f'요구할 팔 수 (기본 {EXPECT_ARMS})')
    ap.add_argument('--max-list', type=int, default=MAX_LIST,
                    help=f'이보다 긴 리스트는 버린다 (기본 {MAX_LIST})')
    ap.add_argument('--skip-equivalence', action='store_true',
                    help='⑤ 판정기 동등성 비교를 건너뛴다 (진단 전용 — 커밋용에는 쓰지 말 것)')
    ap.add_argument('--diagnostic', action='store_true',
                    help='진단(팔 수를 줄인) 패키지로 만든다 — 표지를 박아 cohort '
                         '판정기가 DIAGNOSTIC_TREE 로 거부하게 한다')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if not a.dir or not a.out:
        ap.error('--dir 과 --out 이 필요하다 (또는 --selftest)')
    #  ★★ 상호 요구 — 둘 중 하나만 주는 길을 **양쪽 다** 막는다.
    #    · 표지 없이 팔 수만 낮추면 부분 cohort 가 `p2_*.json` 이름으로 리포에 들어간다.
    #    · 전량 cohort 에 표지를 박으면 진짜 cohort 가 판정 불가가 된다.
    #  ⚠ `ap.error()` 가 아니라 `SystemExit(메시지)` 다 — argparse 는 SystemExit(2) 를
    #    올리고 사유를 stderr 로만 내보내서, 호출자가 `str(ex)` 로 **사유를 못 읽는다**
    #    (실측: 이 두 계약의 회귀 시험이 그것 때문에 통과하지 못했다).
    if a.diagnostic and a.expect_arms == EXPECT_ARMS:
        raise SystemExit(f'--diagnostic 은 팔 수를 줄인 런 전용이다 — --expect-arms 가 '
                         f'{EXPECT_ARMS}(전량 cohort)면 쓰지 않는다')
    if not a.diagnostic and a.expect_arms != EXPECT_ARMS:
        raise SystemExit(
            f'--expect-arms {a.expect_arms} 는 전량 cohort({EXPECT_ARMS})가 아니다 — '
            f'--diagnostic 을 함께 주어야 한다.  그래야 축소본에 표지가 박혀 '
            f'cohort 판정기가 그 tree 를 거부한다 (표지 없는 부분 cohort 가 '
            f'`p2_*.json` 이름으로 리포에 들어가면 나중에 판정이 난다)')

    paths, rcpt = preflight(a.dir, a.expect_arms, diagnostic=a.diagnostic)
    _diag = ({'arms': a.expect_arms, 'consumer': DIAG_CONSUMER, 'schema': SCHEMA_DIAG,
              'not_a_cohort': f'cohort 판정({EXPECT_ARMS}팔 factorial)의 전제 밖이다',
              'source_dir': os.path.basename(os.path.abspath(a.dir))}
             if a.diagnostic else None)
    os.makedirs(a.out, exist_ok=True)
    files, tot_in, tot_out = [], 0, 0
    for p in paths:
        red = reduce_one(p, a.max_list, diagnostic=_diag)          # ③ 없으면 예외
        q = os.path.join(a.out, os.path.basename(p))
        with open(q, 'w', encoding='utf-8') as fh:
            json.dump(red, fh, ensure_ascii=False, sort_keys=True)
        bi, bo = os.path.getsize(p), os.path.getsize(q)
        tot_in += bi
        tot_out += bo
        files.append({'name': os.path.basename(p), 'src_bytes': bi, 'src_sha256': _sha256(p),
                      'out_bytes': bo, 'out_sha256': _sha256(q),
                      'dropped': red['step3']['_reduced']['dropped']})
        print(f'  {os.path.basename(p):28s} {bi/1e6:8.1f} MB → {bo/1e3:7.1f} kB')

    #  ④ receipt 보존
    import shutil
    shutil.copy2(rcpt, os.path.join(a.out, 'run_receipt.json'))

    #  ⑤ 동등성.  ⚠ 그 전에 출력 쪽 기각 표지를 직접 본다 — 판정기 stdout 은 이미 다른
    #    사유로 HOLD 일 때 이 표지를 **가릴 수 있어서**(selftest 에서 실측) 동등성 비교만으로
    #    잡히지 않는다.  값싼 직접 검사를 둔다.
    _ro = sorted(glob.glob(os.path.join(a.out, '.rejected_*')))
    if _ro:
        raise SystemExit('축소 실패 — 출력 디렉터리에 기각 표지가 있다: '
                         + ', '.join(os.path.basename(x) for x in _ro))
    if a.skip_equivalence:
        diffs = []
    elif a.diagnostic:
        diffs = diag_equivalence(paths, a.out)
    else:
        diffs = equivalence(a.dir, a.out)
    if diffs:
        raise SystemExit('축소 실패 — 원본과 축소본이 **다르게 읽힌다**:\n  '
                         + '\n  '.join(diffs))

    #  표지 ① — 트리 파일.  ⚠ 표지 ②(payload 내부)는 `reduce_one` 이 이미 박았다.
    if a.diagnostic:
        with open(os.path.join(a.out, f'{DIAG_SENTINEL}{a.expect_arms}'),
                  'w', encoding='utf-8') as fh:
            json.dump(_diag, fh, ensure_ascii=False, indent=1, sort_keys=True)

    #  ⑥⑦ cohort manifest + 기계 판독 판정 receipt
    rc_v, out_v = _verdict_out(a.out if a.diagnostic else a.dir, None)
    man = {'schema': SCHEMA_DIAG if a.diagnostic else SCHEMA,
           'diagnostic': _diag,
           'tool': 'scripts/reduce_arm_payloads.py',
           'tool_commit': _tool_sha(), 'source_dir': os.path.basename(os.path.abspath(a.dir)),
           'arms': len(paths), 'max_list': a.max_list,
           'equivalence_checked': not a.skip_equivalence,
           'equivalence_modes': (['ion_r_verdict 소비 필드 + manifest'] if a.diagnostic
                                 else ['--seal-only', '--collect-only', 'full']),
           'receipt_sha256': _sha256(rcpt), 'files': files,
           'note': 'scalar decision-audit package — solver/viz 재생용 원자료가 아니다 (R9 Q5)'}
    with open(os.path.join(a.out, 'cohort_manifest.json'), 'w', encoding='utf-8') as fh:
        json.dump(man, fh, ensure_ascii=False, indent=1, sort_keys=True)
    with open(os.path.join(a.out, 'verdict_receipt.txt'), 'w', encoding='utf-8') as fh:
        #  ★ 진단 패키지의 receipt 는 **축소본에 대고 돌린 cohort 판정기의 거부**를 담는다.
        #    "이 tree 로는 cohort 판정이 안 난다" 는 것이 이 패키지의 계약이므로, 그 계약이
        #    지켜지는지를 패키지 자신이 증거로 들고 다니게 한다.
        fh.write(f'# sdcp_gain_verdict.py --dir '
                 f'<{"축소본" if a.diagnostic else "원본"}>   rc={rc_v}\n' + out_v)
    if a.diagnostic and 'DIAGNOSTIC_TREE' not in out_v:
        raise SystemExit(
            '축소 실패 — 축소본에 cohort 판정기를 돌렸는데 **DIAGNOSTIC_TREE 로 거부되지 '
            '않았다**.  표지가 안 박혔거나 판정기가 표지를 안 읽는다는 뜻이고, 그러면 이 '
            f'패키지는 부분 cohort 로 판정될 수 있다.  판정기 출력: {" ".join(out_v.split())[:200]}')

    print(f'\n  {len(paths)} 팔: {tot_in/1e6:.0f} MB → {tot_out/1e3:.0f} kB '
          f'({tot_in/max(tot_out,1):.0f}배)')
    if a.diagnostic:
        print('  ✓ 기각표지 없음 · 팔 수 선언 일치 · origin 격자 위·중복 없음 · '
              'receipt 보존 · 소비 필드 동등')
        print('  ✓ cohort 판정기가 이 tree 를 DIAGNOSTIC_TREE 로 거부한다 (표지 ①②)')
        print(f'  ★ 확인: python3 {DIAG_CONSUMER} {a.out} …')
        print('  ⚠ 진단 패키지다 — cohort 판정(8팔 factorial)의 근거가 아니다')
    else:
        print('  ✓ 기각표지 없음 · 팔 수·factorial 완비 · receipt 보존 · 판정기 동등 (3 모드)')
        print(f'  ★ 확인: python3 scripts/sdcp_gain_verdict.py --dir {a.out} --collect-only')
        print('  ⚠ 이것은 scalar decision-audit package 다 — 원자료가 아니다')
    return 0


def _selftest():
    import tempfile
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(('  PASS  ' if cond else '  FAIL  ') + label)
        ok = ok and bool(cond)

    #  ★ 픽스처 manifest 는 **실제 커밋된 팔**에서 가져온다.
    #    손으로 쓰면 55키짜리 생산 계약(schema_version · component_plan · components ·
    #    backend 증거 · PTFE 기록 · 규약 id …)을 따라잡을 수 없고, 실제로 못 따라잡아
    #    봉인이 계속 깨졌다.  ⇒ 계약이 자라도 픽스처가 따라온다.
    _REF = os.path.join(_SCR, '..', 'docs', 'data',
                        'w4_ptfe_centerline_20260827', 'p2_SBE_sph_a0.json')
    _ref_man = None
    if os.path.exists(_REF):
        try:
            _ref_man = json.load(open(_REF, encoding='utf-8'))['step3']['manifest']
        except Exception:                                          # noqa: BLE001
            _ref_man = None

    def arm(bed, bits, sig):
        h = 0.075
        shift = [b * h for b in bits]
        man = dict(_ref_man) if _ref_man else {}
        man.update({'input_digest': ('d1022e090ab625a9' if bed == 'DBE'
                                     else '04b5a565ff4069f4'),
                    'code_sha': 'c2f5b047', 'vox_um': 0.15,
                    'ptfe_stamp': 'centerline', 'sdcp_bridge_um': 0.01,
                    'origin_shift_um': shift})
        #  ★ manifest 를 고쳤으면 규약 id 도 다시 계산해야 한다 — 안 하면 판정기가
        #    (정당하게) "저장된 id 가 재계산과 다르다" 로 봉인을 깬다.  생산 코드의
        #    같은 함수를 쓴다: 손으로 흉내내면 그 흉내가 검사를 통과시킨다.
        try:
            sys.path.insert(0, _SCR)
            import run_contract as _RC
            man['physics_protocol_id'] = _RC.physics_protocol_id(man)
        except Exception:                                          # noqa: BLE001
            pass
        return {'step3': {
            'sigma_e_eff_S_cm': sig, 'n_dof': 26816923, 'cg_info': 0, 'cg_resid': 1e-9,
            'unconverged': False, 'origin_shift_um': shift,
            'viz_points': list(range(200000)),  # 실제 팔은 배열이 지배한다 (131 MB → 5.8 kB)
            'manifest': man}}

    def build(td, arms=16, receipt=True, rejected=False, drop_step3=False,
              per_bed=None, dup_origin=False, sub='src'):
        """`per_bed=k` 면 **침대마다** k 팔 (진단 픽스처용).  기본은 옛 거동 (SBE 부터 채움)."""
        d = os.path.join(td, sub)
        os.makedirs(d, exist_ok=True)
        n = 0
        for bed, base in (('SBE', 0.0727), ('DBE', 0.0819)):
            if per_bed is not None:
                n = 0
            for i in range(8):
                if n >= (per_bed if per_bed is not None else arms):
                    break
                b = ((i >> 2) & 1, (i >> 1) & 1, i & 1)
                if dup_origin:
                    b = (0, 0, 0)                                  # 전부 같은 origin
                j = arm(bed, b, base + i * 1e-5)
                if drop_step3 and n == 0:
                    j = {'nothing': 1}
                json.dump(j, open(os.path.join(d, f'p2_{bed}_sph_a{i}.json'), 'w'))
                n += 1
        if receipt:
            json.dump({'code_sha': 'c2f5b047', 'arms': 8},
                      open(os.path.join(d, 'run_receipt.json'), 'w'))
        if rejected:
            open(os.path.join(d, '.rejected_20260828'), 'w').close()
        return d

    #  ★★★ 핵심 회귀 (R9 Q5 [P1]) — 기각 표지가 있으면 **축소 자체를 거부**한다.
    with tempfile.TemporaryDirectory() as td:
        d = build(td, rejected=True)
        try:
            preflight(d, 16)
            chk('regr-rejected  `.rejected_*` 가 있으면 축소 거부', False)
        except SystemExit as ex:
            chk('regr-rejected  `.rejected_*` 가 있으면 축소 거부', '기각 receipt' in str(ex))

    with tempfile.TemporaryDirectory() as td:                      # ② 팔 수
        try:
            preflight(build(td, arms=12), 16)
            chk('팔 12/16 → 거부', False)
        except SystemExit as ex:
            chk('팔 12/16 → 거부', '팔 12개' in str(ex))

    with tempfile.TemporaryDirectory() as td:                      # ④ receipt
        try:
            preflight(build(td, receipt=False), 16)
            chk('run_receipt.json 없으면 거부', False)
        except SystemExit as ex:
            chk('run_receipt.json 없으면 거부', 'run_receipt' in str(ex))

    with tempfile.TemporaryDirectory() as td:                      # ③ step3 부재
        d = build(td, drop_step3=True)
        try:
            reduce_one(os.path.join(d, 'p2_SBE_sph_a0.json'))
            chk('step3 없는 파일 → SKIP 아니라 실패', False)
        except ValueError as ex:
            chk('step3 없는 파일 → SKIP 아니라 실패', 'step3 가 없다' in str(ex))

    with tempfile.TemporaryDirectory() as td:                      # 정상 경로
        d = build(td)
        out = os.path.join(td, 'red')
        rc = main(['--dir', d, '--out', out])
        chk('정상 cohort 는 통과한다 (rc 0)', rc == 0)
        red = json.load(open(os.path.join(out, 'p2_DBE_sph_a0.json'), encoding='utf-8'))
        s = red['step3']
        chk('manifest 통째 보존', s['manifest']['input_digest'] in ('d1022e090ab625a9', '04b5a565ff4069f4'))
        chk('긴 배열 제거 + 기록', s['viz_points'] is None
            and any(x['path'] == 'step3.viz_points' for x in s['_reduced']['dropped']))
        chk('⑥ 원본 SHA256 을 남긴다', len(s['_reduced']['source_sha256']) == 64)
        chk('④ receipt 를 옮긴다', os.path.exists(os.path.join(out, 'run_receipt.json')))
        m = json.load(open(os.path.join(out, 'cohort_manifest.json'), encoding='utf-8'))
        chk('⑥ cohort manifest: 스키마·팔수·파일별 해시',
            m['schema'] == SCHEMA and m['arms'] == 16 and len(m['files']) == 16
            and all(len(f['src_sha256']) == 64 and len(f['out_sha256']) == 64
                    for f in m['files']))
        chk('⑤ 동등성 검사를 실제로 돌렸다고 기록', m['equivalence_checked'] is True)
        chk('⑦ verdict receipt 동봉', os.path.exists(os.path.join(out, 'verdict_receipt.txt')))
        #  ★ 축소본을 판정기가 원본과 동일하게 읽는다 (main 이 이미 강제하지만 명시 확인)
        chk('★ 판정기 동등 (seal·collect·full 3 모드)', equivalence(d, out) == [])
        chk('축소된다 (원본 대비 1/10 미만)',
            sum(f['out_bytes'] for f in m['files']) * 10 < sum(f['src_bytes'] for f in m['files']))

    #  ★ 음성 대조 — `equivalence()` 가 **내용을 실제로 본다**는 것 (no-op 이 아님).
    #    ⚠ 처음엔 축소본에 `.rejected_*` 를 넣어 봤는데 **안 걸렸다**: 이 픽스처는
    #      매니페스트가 최소라 전체 판정이 이미 다른 사유로 HOLD 이고, 그래서 기각 표지가
    #      stdout 을 바꾸지 못한다 (포화된 경로로 시험한 셈).  ⇒ 값을 흔들어 시험한다.
    #      기각 표지 자체는 `preflight` 의 ①(regr-rejected)이 원본 쪽에서 막는다.
    with tempfile.TemporaryDirectory() as td:
        d = build(td)
        out = os.path.join(td, 'red')
        main(['--dir', d, '--out', out])
        q = os.path.join(out, 'p2_DBE_sph_a0.json')
        j = json.load(open(q, encoding='utf-8'))
        j['step3']['sigma_e_eff_S_cm'] += 1e-6                     # 값 하나만 흔든다
        json.dump(j, open(q, 'w'))
        chk('음성 대조: σ 하나를 흔들면 동등성이 깨진다 (검사가 무는다)',
            equivalence(d, out) != [])

    #  ══════ 진단 모드 (2026-08-31) ══════════════════════════════════════════
    #  계약: 팔 수를 낮추는 것은 **선언**이어야 하고, 그 산출물은 cohort 판정기가 거부한다.
    with tempfile.TemporaryDirectory() as td:                      # 상호 요구 ①
        d = build(td, per_bed=1)
        try:
            main(['--dir', d, '--out', os.path.join(td, 'r'), '--expect-arms', '2'])
            chk('★ 표지 없이 팔 수만 낮추면 거부 (--diagnostic 강제)', False)
        except SystemExit as ex:
            chk('★ 표지 없이 팔 수만 낮추면 거부 (--diagnostic 강제)',
                '--diagnostic' in str(ex))

    with tempfile.TemporaryDirectory() as td:                      # 상호 요구 ②
        d = build(td)
        try:
            main(['--dir', d, '--out', os.path.join(td, 'r'), '--diagnostic'])
            chk('전량 cohort 에 --diagnostic 을 박으면 거부', False)
        except SystemExit as ex:
            chk('전량 cohort 에 --diagnostic 을 박으면 거부', '전량 cohort' in str(ex))

    with tempfile.TemporaryDirectory() as td:                      # origin 중복
        d = build(td, per_bed=2, dup_origin=True)
        try:
            preflight(d, 4, diagnostic=True)
            chk('진단 모드도 origin 중복은 거부', False)
        except SystemExit as ex:
            chk('진단 모드도 origin 중복은 거부', 'origin 이 중복' in str(ex))

    with tempfile.TemporaryDirectory() as td:                      # 기각 표지는 그대로 문다
        d = build(td, per_bed=1, rejected=True)
        try:
            preflight(d, 2, diagnostic=True)
            chk('진단 모드에서도 `.rejected_*` 는 거부', False)
        except SystemExit as ex:
            chk('진단 모드에서도 `.rejected_*` 는 거부', '기각 receipt' in str(ex))

    with tempfile.TemporaryDirectory() as td:                      # 정상 경로
        d = build(td, per_bed=1)
        out = os.path.join(td, 'red')
        rc = main(['--dir', d, '--out', out, '--expect-arms', '2', '--diagnostic'])
        chk('진단 패키지 정상 경로 (rc 0)', rc == 0)
        chk('표지 ① 트리 파일', os.path.exists(os.path.join(out, f'{DIAG_SENTINEL}2')))
        _r = json.load(open(os.path.join(out, 'p2_DBE_sph_a0.json'), encoding='utf-8'))
        chk('표지 ② payload 내부',
            (_r['step3']['_reduced'].get('diagnostic') or {}).get('consumer') == DIAG_CONSUMER
            and _r['step3']['_reduced']['schema'] == SCHEMA_DIAG)
        _m = json.load(open(os.path.join(out, 'cohort_manifest.json'), encoding='utf-8'))
        chk('manifest 가 진단 스키마', _m['schema'] == SCHEMA_DIAG and _m['arms'] == 2)
        #  ★★★ 이 패키지의 존재 이유 — cohort 판정기가 **실제로** 거부한다
        _rcv, _outv = _verdict_out(out, None)
        chk('★★ cohort 판정기가 축소본을 DIAGNOSTIC_TREE 로 거부', 'DIAGNOSTIC_TREE' in _outv)
        chk('⑦ 그 거부가 verdict_receipt 에 봉인된다',
            'DIAGNOSTIC_TREE' in open(os.path.join(out, 'verdict_receipt.txt'),
                                      encoding='utf-8').read())
        #  ★ 표지 ① 을 지워도 ② 가 남아 여전히 거부된다 (복사로 표지가 새는 경로)
        os.remove(os.path.join(out, f'{DIAG_SENTINEL}2'))
        _rc2, _out2 = _verdict_out(out, None)
        chk('★★ 트리 표지를 지워도 payload 표지로 거부된다',
            'DIAGNOSTIC_TREE' in _out2)
        #  ★ 소비자가 읽는 필드가 실제로 살아 있다
        chk('소비 필드 보존', all(_r['step3'].get(k) is not None
                              for k in ('sigma_e_eff_S_cm',)))

    with tempfile.TemporaryDirectory() as td:                      # 음성 대조 (진단판)
        d = build(td, per_bed=1)
        out = os.path.join(td, 'red')
        main(['--dir', d, '--out', out, '--expect-arms', '2', '--diagnostic'])
        q = os.path.join(out, 'p2_DBE_sph_a0.json')
        j = json.load(open(q, encoding='utf-8'))
        j['step3']['sigma_e_eff_S_cm'] += 1e-6
        json.dump(j, open(q, 'w'))
        _paths = sorted(glob.glob(os.path.join(d, 'p2_*.json')))
        chk('음성 대조: 진단 동등성도 값 하나에 문다', diag_equivalence(_paths, out) != [])

    #  ★ DIAG_EQUIV_KEYS 가 소비자의 실제 목록을 **덮는지** — 조용히 약해지는 것을 막는다.
    #    ⚠ 방향은 한쪽이다: 소비자가 읽는 step3 키 ⊆ DIAG_EQUIV_KEYS.
    #      역방향은 아니다 — `sigma_e_eff_S_cm` 은 ion 판정기가 안 읽지만 **전자·이온
    #      독립성 서술의 근거**라 일부러 함께 고정한다 (여분은 검사를 약화시키지 않는다).
    _ION_CONSUMED = ('sigma_ion_eff_S_cm', 'ion_cg_info', 'ion_unconverged', 'ion_resid')
    try:
        _iv = open(os.path.join(_SCR, 'ion_r_verdict.py'), encoding='utf-8').read()
        _live = [k for k in _ION_CONSUMED if k in _iv]           # 소비자에 실제로 있는 것만
        chk(f'DIAG_EQUIV_KEYS 가 ion_r_verdict 의 소비 필드를 덮는다 ({len(_live)}개)',
            len(_live) == len(_ION_CONSUMED)
            and set(_live) <= set(DIAG_EQUIV_KEYS))
    except OSError:
        chk('DIAG_EQUIV_KEYS 가 ion_r_verdict 의 소비 필드를 덮는다', False)

    print('\n✓ reduce_arm_payloads selftest PASS' if ok
          else '\n✗ reduce_arm_payloads selftest FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
