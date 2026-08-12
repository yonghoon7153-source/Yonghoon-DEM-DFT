#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SR-01 A/B 판독 — 점 스탬프 vs 선분 스탬프 payload 두 개를 읽어 **Δσ_e 를 낸다**.

무엇을 재는가.  `scripts/sr01_realbed_ab.py` 는 실침대에서 **기하**를 쟀다 (섬유의 몇 %가
1-복셀 점 스탬프의 코너-크로싱 때문에 6-연결이 끊기나 — 킷별 20.6~75.8 %).  그런데
"끊긴다"에서 "σ_e 가 얼마나 틀리다"로 가는 다리는 **없다**: 끊긴 섬유가 어차피 전도
백본이 아니었으면 σ_e 는 안 움직이고, 반대로 자기-조각남이 병렬 경로를 지워 과대평가일
수도 과소평가일 수도 있다.  2026-08-11 자체리뷰·Codex 리뷰가 각각 부호를 **추론**했다가
서로 반대 결론에 닿은 자리다.  ⇒ 부호는 재야 안다.  이 스크립트가 그 판독기다.

왜 이 A/B 가 깨끗한가.  두 팔은 **같은 se_dump.npy·fibre.npy** 를 읽는다 — 압밀, 섬유
시딩, 난수, 상 배정, 격자(step3_vox)가 전부 바이트로 동일하고 다른 것은 래스터화뿐이다.
그래서 Δ 는 전부 스탬프 탓이다 (frame[4] 식으로 말하면 교란변수가 0인 대조).

사용:
    python3 scripts/sr01_stamp_compare.py A.json B.json [--label kit_ps_7_3] [--csv out.csv]
    python3 scripts/sr01_stamp_compare.py --selftest
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys

#: payload 안에서 STEP3 결과가 사는 자리 (mpm_webapp_payload: mpm_metrics['step3'] = step3).
_STEP3_PATHS = (('metrics', 'step3'), ('step3',))

#: 비교할 스칼라 — (키, 라벨, 상대변화를 볼 것인가)
_FIELDS = (
    ('sigma_e_eff_S_cm',   'σ_e_eff [S/cm]',      True),
    ('n_dof',              '해 자유도 (전도 복셀)', True),
    ('n_floating_dropped', '부유 노드 버림',        False),
    ('cg_resid',           'CG 잔차',              False),
)


def extract_payload_cmd(text, out_name, stamp):
    """킷 `run_mpm.sh` 본문 → payload 호출 **한 덩어리**를 뽑아 --out/스탬프를 바꾼 문자열.

    ⚠ run_mpm.sh 가 실패 안내에서 권하는 sed 한 줄
        sed -n '/mpm_webapp_payload/,/--out mpm_payload.json/p'
    은 **틀렸다** (2026-08-11 실측).  sed 의 범위는 닫힌 뒤 다시 열린다: 아래쪽
    오류 핸들러의 echo 가 그 sed 문구를 그대로 인쇄하느라 시작 패턴을 또 맞추고,
    그 두 번째 범위는 끝 패턴을 만나지 못해 **파일 끝까지** 뱉는다 (ln -sfn ·
    mpm_done.marker · DONE echo 까지 딸려 나온다 → arm B 가 latest_run 심링크를
    갈아치우고 완료 마커를 찍는다).  그래서 여기서는 첫 범위에서 **끊는다**.
    """
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith('python3') and 'mpm_webapp_payload' in ln:
            start = i
            break
    if start is None:
        raise SystemExit('ABORT — run_mpm.sh 에서 payload 호출부(python3 … mpm_webapp_payload)를 못 찾음')
    end = None
    for i in range(start, len(lines)):
        if '--out ' in lines[i]:
            end = i
            break
    if end is None:
        raise SystemExit('ABORT — payload 호출부에서 --out 을 못 찾음')
    body = lines[start:end + 1]
    tail = body[-1]
    if '--out mpm_payload.json' not in tail:
        raise SystemExit(f'ABORT — 예상과 다른 --out 줄: {tail.strip()[:120]}')
    tail = tail.replace('--out mpm_payload.json',
                        f'--step3-fibre-stamp {stamp} --out {out_name}')
    body[-1] = tail.rstrip().rstrip('\\').rstrip()      # 끝의 줄이음 제거 (EOF 에서 매달리지 않게)
    joined = '\n'.join(body) + '\n'
    # ★ payload 가 쓰는 **다른** 파일도 팔별로 갈라 놓는다.  안 그러면 두 팔이 같은
    #   step4_grid.npz 에 겹쳐 쓰고, 마지막에 run_mpm.sh 가 만든 production 산출물까지
    #   선분-팔의 것으로 바뀐다 (STEP4 를 나중에 돌리면 조용히 다른 베드의 격자를 읽는다).
    joined = re.sub(r'(--save-step4-grid\s+)(\S+?)(\.npz\b)',
                    lambda m: f'{m.group(1)}{m.group(2)}_{stamp}stamp{m.group(3)}', joined)
    stray = [t for t in joined.split() if t.startswith('--save-') and t != '--save-step4-grid']
    if stray:
        sys.stderr.write(f'  ⚠ 팔별로 안 갈라 놓은 출력 플래그: {sorted(set(stray))} '
                         '— 두 팔이 같은 파일에 겹쳐 씁니다.  extract_payload_cmd 를 확장하세요.\n')
    return joined


def dig(obj, path):
    for k in path:
        if not isinstance(obj, dict) or k not in obj:
            return None
        obj = obj[k]
    return obj


def step3_of(payload):
    """payload dict → step3 dict.  자리를 못 찾으면 None (조용히 0 을 만들지 않는다)."""
    for p in _STEP3_PATHS:
        got = dig(payload, p)
        if isinstance(got, dict):
            return got
    return None


#: 스탬프 도장이 실제로 찍히는 자리 = `step3['manifest']` (mpm_webapp_payload:1520-1531).
#   step3 바로 밑도 받아 준다 — 스키마가 평평해져도 판독기가 조용히 None 을 반환하면
#   "팔 검증 없이 Δ 만 보고" 하게 되므로 (그게 이 스크립트가 막으려는 바로 그 사고다).
_STAMP_PATHS = (('manifest', 'fibre_stamp'), ('fibre_stamp',))


def stamp_of(step3):
    """step3 dict → (스탬프 이름, 실제 적용 여부).  라벨이 아니라 **매니페스트**에서 읽는다."""
    if not isinstance(step3, dict):
        return None, None
    for p in _STAMP_PATHS:
        got = dig(step3, p)
        if isinstance(got, str):
            applied = None
            for q in (p[:-1] + ('fibre_stamp_applied',),):
                v = dig(step3, q)
                if isinstance(v, bool):
                    applied = v
            return got, applied
    return None, None


def backend_of(step3):
    """이 팔이 실제로 쓴 solve backend ('gpu'|'cpu'|None).

    ★ 왜 검사하는가 (2026-08-11, arm A 실행 중 발견): STEP3 는 `--step3-gpu` 를 줘도
    cupy 가 없으면 **조용히 CPU 로 폴백**한다 (수 분→수십 분).  느린 것 자체는 무해하고
    수치도 같다 (같은 행렬·같은 rtol 1e-8 = backend swap only).  위험한 것은 **두 팔이
    다른 backend 로 도는 것** — arm A 가 도는 동안 답답해서 cupy 를 깔면 arm B 만 GPU 가
    되고, 그러면 "스탬프만 다르다" 는 A/B 의 전제가 깨진다.  수치가 같아야 마땅하지만
    그것은 **가정**이고, 이 스크립트의 일은 가정을 검사하는 것이다."""
    if not isinstance(step3, dict):
        return None
    for p in (('manifest', 'backend_last_solve'), ('manifest', 'backend')):
        got = dig(step3, p)
        if isinstance(got, dict) and got.get('used'):
            return str(got['used'])
    return None


def precond_of(step3):
    """이 팔이 실제로 쓴 CG **전처리** ('jacobi'|'amg'|None).

    ★ backend 만 봐서는 부족하다 (SR-03, 2026-08-11): `--step3-amg` 는 backend 를 바꾸지
    않고 전처리만 바꾼다 — 두 팔이 cpu/cpu 로 일치해도 Jacobi↔AMG 면 통과해 버린다.
    전처리 교체의 σ_eff 영향은 실측 ≤0.012 % (rtol 1e-8) 로 작지만, 우리가 재려는 Δσ_e 가
    그보다 작을 수 있다 — 작다는 것이 곧 무해하다는 뜻은 아니다.  옛 payload 는 이 키가
    없으므로(None) 그때는 조용히 넘어간다."""
    if not isinstance(step3, dict):
        return None
    for p in (('manifest', 'backend_last_solve'), ('manifest', 'backend')):
        got = dig(step3, p)
        if isinstance(got, dict) and got.get('precond'):
            return str(got['precond'])
    return None


def check_arm(path, want, expect_backend=None):
    """→ None(완전) 또는 **왜 불완전한지** 문자열.  러너 재개(`SKIP`) 판정용.

    ★ 여기서 느슨하면 불완전한 팔을 "이미 됐다" 고 건너뛰어 Δ 가 조용히 거짓이 된다.
    그래서 파일 존재가 아니라 **쓸 수 있는 결과인지**를 본다: step3 블록 · 스탬프 도장이
    원한 것과 일치 · (선분이면) 실제 적용 · CG 수렴 · σ_e 가 양수.
    계기 (2026-08-11): arm A 가 5h55m 걸려 끝난 직후 터미널이 끊겨 arm B 가 시작조차 못 했다.
    러너를 그냥 다시 돌리면 **A 를 6시간 다시 돈다** — 그래서 재개가 필요하고, 재개는
    "이미 완전한가" 를 엄격히 물어야만 안전하다.

    ★★ expect_backend — 재개의 **가장 위험한 구멍**을 막는다.  킷 run_mpm.sh 는 이미
    `--step3-gpu` 를 넘기므로(mpm_input_from_case.py:688) cupy 를 깔기만 하면 다음 팔은
    **자동으로 GPU** 가 된다.  그러면 "CPU 로 끝난 arm A 를 SKIP 하고 arm B 만 GPU 로"
    라는 최악의 재개가 기본 동작이 된다.  지금 돌 backend 를 넘기면, 기존 팔이 다른
    backend 로 돌았을 때 **SKIP 하지 않고 다시 돌게** 한다."""
    if not os.path.exists(path):
        return '파일 없음'
    try:
        with open(path, encoding='utf-8') as fh:
            p = json.load(fh)
    except Exception as e:                         # noqa: BLE001 — 잘린 JSON 도 여기로 온다
        return f'JSON 읽기 실패 ({type(e).__name__})'
    s = step3_of(p)
    if s is None:
        return 'step3 블록 없음 (--no-step3 였거나 중단)'
    k, applied = stamp_of(s)
    if k is None:
        return '스탬프 도장 없음'
    if k != want:
        return f'스탬프가 {k} — 원한 것은 {want}'
    if want == 'segment' and applied is False:
        return '선분 요청이 적용되지 않음 (fibre_stamp_applied=False)'
    if s.get('unconverged'):
        return 'CG 미수렴 (σ UNRELIABLE) — 다시 돌아야 한다'
    v = s.get('sigma_e_eff_S_cm')
    if not isinstance(v, (int, float)) or isinstance(v, bool) or not v > 0:
        return f'σ_e 가 없거나 0 ({v!r})'
    if expect_backend:
        got = backend_of(s)
        if got and got != expect_backend:
            return (f'backend 가 {got} 인데 지금 돌면 {expect_backend} — 두 팔이 갈린다. '
                    '재개 대신 다시 돌아야 한다')
    return None


def compare(pa, pb):
    """→ (행 dict, 경고 리스트).  A = 점(기준), B = 선분."""
    warn = []
    sa, sb = step3_of(pa), step3_of(pb)
    if sa is None or sb is None:
        raise SystemExit('ABORT — payload 에서 step3 블록을 못 찾음 '
                         f'(A={"OK" if sa else "없음"}, B={"OK" if sb else "없음"}).  '
                         '--no-step3 로 돈 payload 는 비교 대상이 아닙니다.')
    # ★ 라벨이 아니라 매니페스트로 팔을 검증한다.  --step3-fibre-stamp 를 줬어도 --fibre 가
    #   없으면 payload 가 조용히 점 스탬프로 되돌아간다 (fibre_stamp_applied=False) —
    #   그걸 못 보면 "Δ=0 → 스탬프 무관" 이라는 **정반대 결론**을 낸다.
    ka, _aa = stamp_of(sa)
    kb, ab = stamp_of(sb)
    if ka is None or kb is None:
        warn.append('스탬프 도장(step3.manifest.fibre_stamp)이 없습니다 — 배선 이전 payload 이거나 '
                    'STEP3 가 실패한 런입니다.  어느 팔인지 **확인 불가**이므로 Δ 를 인용하지 마세요.')
    if ka and ka != 'point':
        warn.append(f'A 팔이 point 가 아닙니다: {ka}')
    if kb != 'segment':
        warn.append(f'B 팔이 segment 가 아닙니다: {kb!r}  ← --step3-fibre-stamp 가 안 먹었습니다')
    if ab is False:
        warn.append('B 팔의 fibre_stamp_applied=False — --fibre 가 없어 점 스탬프로 되돌아갔습니다 '
                    '(Δ≈0 은 "스탬프 무관"이 아니라 "적용 안 됨"입니다)')
    for k in ('vox_um',):
        if sa.get(k) != sb.get(k):
            warn.append(f'{k} 가 두 팔에서 다릅니다 ({sa.get(k)} vs {sb.get(k)}) — 공통모드 상쇄 깨짐')
    # ★ backend 가 갈리면 "스탬프만 다르다" 가 아니다 (arm A 도는 중 cupy 설치 시나리오)
    bea, beb = backend_of(sa), backend_of(sb)
    if bea and beb and bea != beb:
        warn.append(f'solve backend 가 두 팔에서 다릅니다 ({bea} vs {beb}) — 같은 행렬·같은 rtol 이라 '
                    '수치는 같아야 하지만 그건 **가정**입니다.  한쪽 팔을 같은 backend 로 다시 도세요')
    # ★ SR-03: 전처리도 갈릴 수 있다 (backend 는 둘 다 cpu 인데 Jacobi vs AMG)
    pca, pcb = precond_of(sa), precond_of(sb)
    if pca and pcb and pca != pcb:
        warn.append(f'CG 전처리가 두 팔에서 다릅니다 ({pca} vs {pcb}) — σ_eff 영향은 실측 ≤0.012 % '
                    '지만 재려는 Δ 가 그보다 작을 수 있습니다.  한쪽 팔을 같은 전처리로 다시 도세요')
    # 수렴 실패는 값 자체가 못 쓰는 것 — Δ 계산 전에 알린다
    for lab, s in (('A', sa), ('B', sb)):
        if s.get('unconverged') or (isinstance(s.get('cg_info'), int) and s.get('cg_info')):
            warn.append(f'{lab} 팔 CG 미수렴 (cg_info={s.get("cg_info")}, resid={s.get("cg_resid")}) '
                        '— 그 σ 는 UNRELIABLE, Δ 인용 금지')

    row = {'label': '', 'stamp_A': ka or 'point?', 'stamp_B': kb or '?',
           'vox_um': sa.get('vox_um'), 'backend_A': bea, 'backend_B': beb,
           'precond_A': pca, 'precond_B': pcb}
    for key, _lab, rel in _FIELDS:
        va, vb = sa.get(key), sb.get(key)
        row[key + '_A'] = va
        row[key + '_B'] = vb
        if rel and isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            row[key + '_ratio'] = (float(vb) / float(va)) if va else None
            row[key + '_pct'] = ((float(vb) / float(va) - 1.0) * 100.0) if va else None
    # 소산 분담 (어느 상이 전류를 나르나) — 탄소 몫이 스탬프로 얼마나 바뀌나가 핵심
    da, db = sa.get('dissipation_share') or {}, sb.get('dissipation_share') or {}
    for ph in sorted(set(da) | set(db)):
        row[f'share_{ph}_A'] = da.get(ph)
        row[f'share_{ph}_B'] = db.get(ph)
    return row, warn


def render(row, warn):
    out = []
    sa = row.get('sigma_e_eff_S_cm_A')
    sb = row.get('sigma_e_eff_S_cm_B')
    out.append(f"SR-01 스탬프 A/B  —  {row.get('label') or '(무라벨)'}   "
               f"[A={row['stamp_A']} · B={row['stamp_B']} · vox {row.get('vox_um')} µm]")
    out.append('─' * 78)
    for key, lab, rel in _FIELDS:
        va, vb = row.get(key + '_A'), row.get(key + '_B')
        line = f'  {lab:22s} A {va!s:>12s}   B {vb!s:>12s}'
        if rel and row.get(key + '_pct') is not None:
            line += f'   Δ {row[key + "_pct"]:+8.2f} %  (×{row[key + "_ratio"]:.3f})'
        out.append(line)
    shares = sorted({k[6:-2] for k in row if k.startswith('share_') and k.endswith('_A')})
    if shares:
        out.append('  소산 분담 (전류를 어느 상이 나르나):')
        for ph in shares:
            a, b = row.get(f'share_{ph}_A'), row.get(f'share_{ph}_B')
            if (a or 0) < 1e-4 and (b or 0) < 1e-4:
                continue
            d = (f'{(b - a) * 100:+6.2f} %p' if isinstance(a, (int, float)) and isinstance(b, (int, float)) else '')
            out.append(f'    {ph:14s} A {a!s:>8s}   B {b!s:>8s}   {d}')
    out.append('─' * 78)
    if isinstance(sa, (int, float)) and isinstance(sb, (int, float)) and sa:
        pct = (sb / sa - 1.0) * 100.0
        if abs(pct) < 1.0:
            verdict = ('점 스탬프 아티팩트가 σ_e 를 **거의 안 움직인다** (|Δ| < 1 %). '
                       '끊긴 섬유가 전도 백본이 아니었다는 뜻 — 기하 단절률(20~76 %)이 '
                       'σ 로 전이되지 않는다.')
        elif pct > 0:
            verdict = (f'선분 스탬프가 σ_e 를 **{pct:+.1f} % 올린다** → 현행 점 스탬프는 '
                       '탄소 백본을 끊어 σ_e 를 **과소평가**하고 있었다.')
        else:
            verdict = (f'선분 스탬프가 σ_e 를 **{pct:+.1f} % 내린다** → 점 스탬프의 조각남이 '
                       '오히려 σ_e 를 **과대평가**하고 있었다 (조각이 만든 여분 도통 경로 · '
                       '스탬프 부피 인플레).')
        out.append('  판정: ' + verdict)
    for w in warn:
        out.append('  ⚠ ' + w)
    if not warn:
        out.append('  (두 팔의 vox·스탬프 매니페스트 확인됨 — Δ 는 래스터화 탓이다)')
    return '\n'.join(out)


# ───────────────────────────── selftest ─────────────────────────────

def _mk(sig, stamp, applied=True, n_dof=1000, vox=0.4, share=None, backend='cpu', cg_info=0,
        precond='jacobi'):
    """★ 실제 payload 의 **중첩 그대로** 짓는다 (metrics.step3.manifest.fibre_stamp).
    평평하게 지으면 판독기가 도장을 못 찾는 것을 selftest 가 놓친다 — 실제로 처음
    구현이 한 단계 얕아서 stamp_of 가 항상 None 이었다 (2026-08-11)."""
    return {'metrics': {'step3': {
        'sigma_e_eff_S_cm': sig, 'vox_um': vox, 'n_dof': n_dof,
        'n_floating_dropped': 7, 'cg_resid': 1e-9,
        'cg_info': cg_info,
        'manifest': {'schema_version': 2, 'status': 'complete',
                     'fibre_stamp': stamp, 'fibre_stamp_applied': applied,
                     'backend_last_solve': {'requested': 'gpu', 'used': backend,
                                            'precond': precond}},
        'dissipation_share': share or {'AM_S': 0.6, 'VGCF': 0.4}}}}


def _selftest():
    ok = fail = 0

    def chk(c, m):
        nonlocal ok, fail
        ok, fail = (ok + 1, fail) if c else (ok, fail + 1)
        print(('  PASS  ' if c else '  FAIL  ') + m)

    a, b = _mk(0.010, 'point'), _mk(0.012, 'segment', n_dof=1200)
    row, warn = compare(a, b)
    chk(abs(row['sigma_e_eff_S_cm_pct'] - 20.0) < 1e-9, '1) Δ% 산술 (0.010→0.012 = +20 %)')
    chk(abs(row['sigma_e_eff_S_cm_ratio'] - 1.2) < 1e-12, '2) 비 1.200')
    chk(not warn, '3) 정상 쌍은 경고 없음')
    chk('올린다' in render(row, warn), '4) 판정 문장이 부호를 말한다')

    # ★ 가장 중요한 함정: 플래그는 줬는데 --fibre 가 없어 조용히 되돌아간 경우
    _, w2 = compare(a, _mk(0.0100001, 'point', applied=False))
    chk(any('point' in x or 'segment' in x for x in w2), '5) B 가 point 면 경고')
    _, w2b = compare(a, _mk(0.01, 'segment', applied=False))
    chk(any('applied=False' in x for x in w2b), '6) ★ applied=False 를 잡는다 (Δ≈0 오독 방지)')
    # ★ 도장 자리가 실제 payload 중첩(manifest 밑)과 맞는가 — 여기가 한 번 틀렸던 자리
    chk(stamp_of(a['metrics']['step3']) == ('point', True), '6b) ★ manifest 밑 도장을 읽는다')
    chk(stamp_of({'sigma_e_eff_S_cm': 1.0}) == (None, None), '6c) 도장 없으면 None (거짓 확신 금지)')
    _, w2c = compare({'metrics': {'step3': {'sigma_e_eff_S_cm': 0.01, 'vox_um': 0.4}}},
                     {'metrics': {'step3': {'sigma_e_eff_S_cm': 0.02, 'vox_um': 0.4}}})
    chk(any('확인 불가' in x for x in w2c), '6d) 도장 없는 쌍은 "인용하지 말라" 경고')

    # 공통모드가 깨진 쌍 (vox 가 다름) — Δ 를 스탬프 탓으로 읽으면 안 된다
    _, w3 = compare(a, _mk(0.012, 'segment', vox=0.2))
    chk(any('vox_um' in x for x in w3), '7) vox 불일치 경고 (공통모드 상쇄 깨짐)')
    # ★ backend 갈림 — arm A 도는 중 cupy 를 깔면 생기는 실제 시나리오
    chk(backend_of(a['metrics']['step3']) == 'cpu', '7b) backend 도장을 읽는다')
    _, w3b = compare(a, _mk(0.012, 'segment', backend='gpu'))
    chk(any('backend' in x for x in w3b), '7c) ★ backend 불일치 경고 (cpu vs gpu)')
    # ★ SR-03: backend 는 같은데 전처리만 갈리는 경우 (--step3-amg 를 한쪽 팔에만 준 실수)
    chk(precond_of(a['metrics']['step3']) == 'jacobi', '7p1) 전처리 도장을 읽는다')
    _, w3d = compare(a, _mk(0.012, 'segment', precond='amg'))
    chk(any('전처리' in x for x in w3d), '7p2) ★ 전처리 불일치 경고 (jacobi vs amg)')
    _, w3e = compare(a, _mk(0.012, 'segment'))
    chk(not any('전처리' in x for x in w3e), '7p3) 같은 전처리면 조용')
    old = _mk(0.012, 'segment')
    del old['metrics']['step3']['manifest']['backend_last_solve']['precond']
    chk(precond_of(old['metrics']['step3']) is None and
        not any('전처리' in x for x in compare(a, old)[1]),
        '7p4) 옛 payload(전처리 키 없음)는 조용히 통과')
    _, w3c = compare(a, _mk(0.012, 'segment', cg_info=1))
    chk(any('미수렴' in x for x in w3c), '7d) ★ CG 미수렴이면 Δ 인용 금지 경고')

    # 부호 반대 / 무변화 문장
    chk('내린다' in render(*compare(a, _mk(0.008, 'segment'))), '8) 감소 판정')
    chk('거의 안 움직인다' in render(*compare(a, _mk(0.01002, 'segment'))), '9) |Δ|<1 % 판정')

    # step3 없는 payload 는 조용히 0 을 만들지 말고 멈춘다
    try:
        compare({'metrics': {}}, b)
        chk(False, '10) step3 없으면 중단')
    except SystemExit:
        chk(True, '10) step3 없으면 중단')

    # 분담 차이 %p
    r4, _ = compare(_mk(0.01, 'point', share={'AM_S': 0.7, 'VGCF': 0.3}),
                    _mk(0.01, 'segment', share={'AM_S': 0.5, 'VGCF': 0.5}))
    txt = render(r4, [])
    chk('+20.00 %p' in txt and '-20.00 %p' in txt, '11) 소산 분담 %p 표기')

    # σ_e = 0 (비퍼콜) 인 A 에서 0 나눗셈으로 안 죽는가
    r5, _ = compare(_mk(0.0, 'point'), _mk(0.005, 'segment'))
    chk(r5.get('sigma_e_eff_S_cm_pct') is None, '12) σ_A=0 → Δ% 는 None (0 나눗셈 금지)')
    chk(isinstance(render(r5, []), str) and 'A          0.0' in render(r5, []),
        '12b) σ_A=0 여도 렌더가 죽지 않고 0 을 보여준다')
    chk(r5['sigma_e_eff_S_cm_B'] == 0.005, '13) σ_A=0 여도 B 값은 보존')

    # ── 추출기: **실제 킷 스크립트**를 fixture 로 (합성 fixture 는 이 버그를 못 잡는다) ──
    kit = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docs', 'data',
                       'kit_ps_scaffolds', 'kit_ps_7_3__run_mpm.sh')
    if os.path.exists(kit):
        txt = open(kit, encoding='utf-8').read()
        cmd = extract_payload_cmd(txt, 'mpm_payload_segstamp.json', 'segment')
        chk(cmd.lstrip().startswith('python3'), '14) 추출은 python3 로 시작')
        chk('--step3-fibre-stamp segment' in cmd and 'mpm_payload_segstamp.json' in cmd,
            '15) 스탬프·--out 치환')
        # ★ sed 버그 재발 방지 — run_mpm.sh 꼬리가 딸려오면 arm B 가 latest_run 을 갈아치운다
        for bad in ('ln -sfn', 'mpm_done.marker', 'STEP 2 (payload) FAILED', 'DONE $(date)'):
            chk(bad not in cmd, f'16) ★ 꼬리 미포함: {bad!r}')
        chk(cmd.count('mpm_webapp_payload') == 1, '17) 호출부는 정확히 1개')
        chk(not cmd.rstrip().endswith('\\'), '18) 끝의 줄이음 제거 (EOF 매달림 방지)')
        chk('mpm_payload.json' not in cmd.replace('mpm_payload_segstamp.json', ''),
            '19) 원본 --out 이 남지 않음 (arm A 산출물 보호)')
        # point 팔도 같은 덩어리에서 나와야 두 팔이 스탬프만 다르다
        chk('step4_grid_segmentstamp.npz' in cmd,
            '20) ★ step4 격자도 팔별로 갈라짐 (production step4_grid.npz 보호)')
        cp = extract_payload_cmd(txt, 'mpm_payload_pointstamp.json', 'point')
        ta, tb = cp.split(), cmd.split()
        # 규칙으로 판정한다 (하드코딩 목록이 아니라) — 나중에 출력 플래그가 더 갈라져도 유효.
        #   다른 토큰은 **앞 토큰이 출력 플래그이거나 --step3-fibre-stamp** 여야 한다.
        #   즉 "두 팔은 어디에 쓰느냐와 어떻게 찍느냐만 다르다" 를 위치로 증명한다.
        diff = [(i, x, y) for i, (x, y) in enumerate(zip(ta, tb)) if x != y]
        bad = [(x, y) for i, x, y in diff
               if not (i and (ta[i - 1] == '--step3-fibre-stamp'
                              or ta[i - 1] == '--out' or ta[i - 1].startswith('--save-')))]
        chk(len(ta) == len(tb) and diff and not bad,
            f'21) ★ 두 팔의 차이는 스탬프/출력파일명뿐 (규칙위반 {bad})')
    else:
        print('  SKIP  14-20) 킷 fixture 없음 (docs/data/kit_ps_scaffolds/)')

    # ── check_arm (러너 재개) — 느슨하면 불완전한 팔을 SKIP 해 Δ 가 조용히 거짓이 된다 ──
    import tempfile as _tf
    with _tf.TemporaryDirectory() as td:
        def w(name, obj):
            p = os.path.join(td, name)
            with open(p, 'w', encoding='utf-8') as fh:
                json.dump(obj, fh) if not isinstance(obj, str) else fh.write(obj)
            return p
        good = w('a.json', _mk(0.0051, 'point'))
        chk(check_arm(good, 'point') is None, '8a) 완전한 팔은 통과')
        chk('point' in (check_arm(good, 'segment') or ''), '8b) ★ 스탬프가 다르면 거부 (A 를 B 로 착각하지 않는다)')
        chk(check_arm(os.path.join(td, 'no.json'), 'point') == '파일 없음', '8c) 없는 파일')
        chk('JSON 읽기 실패' in (check_arm(w('t.json', '{"metr'), 'point') or ''), '8d) ★ 잘린 JSON (중단된 런)')
        chk('step3 블록 없음' in (check_arm(w('e.json', {'metrics': {}}), 'point') or ''), '8e) step3 블록 없음')
        bad = _mk(0.0051, 'point'); bad['metrics']['step3']['unconverged'] = True
        chk('CG 미수렴' in (check_arm(w('u.json', bad), 'point') or ''), '8f) ★ 미수렴은 재개 대상이 아니라 재실행 대상')
        z = _mk(0.0, 'point')
        chk('σ_e' in (check_arm(w('z.json', z), 'point') or ''), '8g) σ_e 가 0 이면 거부')
        na = _mk(0.0051, 'segment', applied=False)
        chk('적용되지 않음' in (check_arm(w('n.json', na), 'segment') or ''), '8h) ★ 선분 요청이 적용 안 된 팔은 거부 (조용한 점-되돌아감)')
        chk(main([good, '--check-arm', good, '--stamp', 'point']) == 0, '8i) CLI: 완전하면 exit 0')
        chk(main(['--check-arm', good, '--stamp', 'segment']) == 1, '8j) CLI: 불완전하면 exit 1')
        chk(check_arm(good, 'point', 'cpu') is None, '8k) backend 가 같으면 재개 허용 (cpu ≡ cpu)')
        chk('backend 가 cpu 인데' in (check_arm(good, 'point', 'gpu') or ''),
            '8l) ★★ cupy 를 깔면 다음 팔이 자동 GPU — CPU 로 끝난 팔을 SKIP 하지 않는다')
        chk(main(['--check-arm', good, '--stamp', 'point', '--expect-backend', 'gpu']) == 1,
            '8m) CLI: backend 불일치는 exit 1 (러너가 다시 돈다)')
    print(f'\nsr01_stamp_compare selftest: {ok}/{ok + fail} PASS')
    return 0 if fail == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('a', nargs='?', help='arm A payload (점 스탬프 = 현행 기본)')
    ap.add_argument('b', nargs='?', help='arm B payload (선분 스탬프)')
    ap.add_argument('--label', default='', help='CSV/출력에 붙일 이름 (예: kit_ps_7_3)')
    ap.add_argument('--csv', default='', help='한 줄 append (헤더 자동)')
    ap.add_argument('--extract-payload', default='',
                    help='킷 run_mpm.sh 경로 → payload 호출부만 stdout 으로 (러너용).')
    ap.add_argument('--out-name', default='mpm_payload_segstamp.json', help='--extract-payload 의 --out')
    ap.add_argument('--stamp', default='segment', choices=('point', 'segment'),
                    help='--extract-payload 가 박을 --step3-fibre-stamp')
    ap.add_argument('--check-arm', default='',
                    help='payload 하나가 **쓸 수 있는 팔 결과인지** 검사 (러너 재개용).  '
                         '완전하면 exit 0, 아니면 이유를 찍고 exit 1.  --stamp 로 어느 팔인지 지정.')
    ap.add_argument('--expect-backend', default='', choices=('', 'cpu', 'gpu'),
                    help='--check-arm 과 함께: 지금 돌면 쓸 backend.  기존 팔이 다른 backend 로 '
                         '돌았으면 SKIP 하지 않는다 (cupy 를 깔면 다음 팔이 자동 GPU 가 되므로).')
    ap.add_argument('--selftest', action='store_true')
    x = ap.parse_args(argv)
    if x.selftest:
        return _selftest()
    if x.check_arm:
        why = check_arm(x.check_arm, x.stamp, x.expect_backend or None)
        print(why if why else f'완전 ({x.stamp})')
        return 1 if why else 0
    if x.extract_payload:
        sys.stdout.write(extract_payload_cmd(
            open(x.extract_payload, encoding='utf-8').read(), x.out_name, x.stamp))
        return 0
    if not x.a or not x.b:
        ap.error('payload 두 개가 필요합니다 (또는 --selftest).')
    row, warn = compare(json.load(open(x.a, encoding='utf-8')),
                        json.load(open(x.b, encoding='utf-8')))
    row['label'] = x.label or os.path.basename(os.path.dirname(os.path.abspath(x.a)))
    print(render(row, warn))
    if x.csv:
        new = not os.path.exists(x.csv)
        with open(x.csv, 'a', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=list(row))
            if new:
                w.writeheader()
            w.writerow(row)
        print(f'\n  → {x.csv}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
