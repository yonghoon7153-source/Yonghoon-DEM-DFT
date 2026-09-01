#!/usr/bin/env python3
"""웹앱이 **왜 그렇게 보이는지**를 디스크에서 그대로 읽어 말한다.

★★ 왜 이게 필요한가 (2026-08-25):  "안 뜬다" ↔ "제 쪽에선 뜹니다" 를 세 번 왕복했다.
  내 리포에서 렌더하면 배지가 나오는데 사용자 화면에는 없었다.  원인은 매번 **디스크
  상태**였고(옛 복원본 · `mpm_metrics.json` 부재 · 데이터 루트 불일치), 나는 그것을
  볼 수 없었다.  ⇒ 추측 대신 **사용자 기계에서 한 줄로 답이 나오게** 한다.

  이 스크립트는 **아무것도 고치지 않는다** — 읽고, 판정하고, 다음 명령을 찍는다.

    python3 scripts/diagnose_webapp_data.py
    python3 scripts/diagnose_webapp_data.py --case input_2mAh_real_8   # 한 건만 파고들기

⚠ 배지 판정 로직은 `webapp/app.py` 를 **베끼지 않는다** — 같은 파일을 읽고 같은 문턱을
  쓰되, 어긋나면 그것도 결과로 보고한다 (복사본이 갈라지는 것이 이 리포의 상습 결함이다).
"""
import argparse
import json
import os
import subprocess
import sys

GAP_THRESHOLD = 4.0          # app.py 와 같은 값 — |gap| ≤ 4 → cross-validated


def _data_root():
    return os.environ.get('DEM_WEB_DATA') or os.path.join(os.path.expanduser('~'),
                                                          'Yonghoon-DEM-DFT')


def _code_root():
    return os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def _read(p, default=None):
    try:
        with open(p, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default


def _git(code, *args):
    try:
        return subprocess.run(('git', '-C', code) + args, capture_output=True,
                              text=True, timeout=10).stdout.strip()
    except Exception:
        return ''


def scan(data_root):
    """케이스마다 배지 판정에 **실제로 필요한 네 가지**를 읽는다."""
    up = os.path.join(data_root, 'webapp', 'uploads')
    rs = os.path.join(data_root, 'webapp', 'results')
    out = []
    if not os.path.isdir(up):
        return out
    for cid in sorted(os.listdir(up)):
        mf = os.path.join(up, cid, 'meta.json')
        if not os.path.isfile(mf):
            continue
        meta = _read(mf, {}) or {}
        rd = os.path.join(rs, cid)
        fm = _read(os.path.join(rd, 'full_metrics.json'), {}) or {}
        mm_path = os.path.join(rd, 'mpm_metrics.json')
        mm = _read(mm_path) if os.path.exists(mm_path) else None
        dem = fm.get('porosity_spheresum')
        if dem is None:
            dem = fm.get('porosity')
        rec = {
            'cid': cid,
            'name': meta.get('name') or cid,
            'status': meta.get('status') or '',
            #  ① CSV 복원이 MPM 열을 실어 줬나 (조인 키 고치기 전이면 0개)
            'fm_mpm_keys': sum(1 for k in fm if k.startswith('mpm')),
            #  ⚠ 열이 **있다고** 박스를 만들 수 있는 건 아니다 — porosity 계열이 있어야 한다.
            #    (mpm 열 3개짜리 케이스가 있는데 전부 설정값이라 박스가 안 나온다)
            'fm_mpm_por': any(k.startswith('mpm') and 'porosity' in k for k in fm),
            #  ② 박스·배지가 읽는 파일이 있나
            'mm_exists': mm is not None,
            #  ③ 그 안에 판정에 쓰는 값이 있나
            'mpm_por': (mm or {}).get('porosity_mpm_pct'),
            #  ④ DEM 쪽 짝이 있나
            'dem_por': dem,
            'has_payload': os.path.exists(os.path.join(rd, 'mpm_payload.json')),
        }
        if rec['mpm_por'] is not None and rec['dem_por'] is not None:
            gap = float(rec['dem_por']) - float(rec['mpm_por'])
            rec['gap'] = round(gap, 1)
            rec['badge'] = ('MPM SE-poor' if gap > GAP_THRESHOLD else
                            'MPM SE-rich' if gap < -GAP_THRESHOLD else 'MPM ✓')
        else:
            rec['gap'] = None
            rec['badge'] = 'MPM ✓(payload)' if rec['has_payload'] else ''
        out.append(rec)
    return out


def source_mpm_counts():
    """**원본 CSV** 가 케이스별로 MPM 열을 몇 개 갖고 있나 (이름/ID → 개수).

    ⚠⚠ 왜 필요한가:  디스크에 mpm 열이 0개인 것에는 **두 가지**가 있다 —
      ⓐ 옛 복원본이라 빠진 것 (`--refill` 이 고친다)
      ⓑ 원본 표에 애초에 없는 것 (**무엇을 돌려도 안 생긴다**)
    이 둘을 안 갈라 놓으면 "고치는 명령" 을 찍어 놓고 아무 일도 안 일어난다 =
    이 진단기가 고치려던 바로 그 병을 자기가 저지른다.  ⇒ 원본을 읽어 갈라낸다.
    실패하면 **빈 dict** 를 돌려주고, 호출부는 "모른다" 로 낮춰 말한다 (지어내지 않는다).
    """
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from rebuild_cases_from_csv import collect
        cur = os.getcwd()
        os.chdir(_code_root())
        try:
            cs = collect()
        finally:
            os.chdir(cur)
    except Exception:
        return {}
    out = {}
    for cid, c in cs.items():
        n = sum(1 for k in (c.get('metrics') or {}) if k.startswith('mpm'))
        out[cid] = n
        out[c.get('name') or cid] = n
    return out


def _why(r, src=None):
    """배지가 없으면 **어느 고리가 끊겼는지** 한 줄로."""
    if r['badge']:
        return ''
    if r['fm_mpm_keys'] == 0:
        if src:
            n = src.get(r['name'], src.get(r['cid']))
            if n == 0:
                return '⓪ 원본 CSV 에도 MPM 이 **없다** → 고칠 것이 없다 (MPM 을 안 돌린 케이스)'
            if n:
                return (f'① 옛 복원본 — 원본 CSV 엔 mpm 열이 {n}개 있는데 디스크엔 0개 '
                        '→ `--refill` 이 고친다')
        return '① full_metrics 에 mpm_* 열이 **0개** (원본 대조 실패 — 옛 복원본일 수 있다)'
    if not r['mm_exists']:
        if not r['fm_mpm_por']:
            return ('⓪ mpm 열은 있지만 **porosity 계열이 없다** (설정값뿐) '
                    '→ 박스를 만들 수 없다.  고칠 것이 없다')
        return '② mpm_metrics.json **없음** → rebuild_tables_from_metrics.py --write 미실행'
    if r['mpm_por'] is None:
        return '③ mpm_metrics.json 에 porosity_mpm_pct **없음**'
    if r['dem_por'] is None:
        return '④ full_metrics 에 DEM porosity **없음** → 짝이 없어 gap 을 못 낸다'
    return '(알 수 없음 — 이 줄이 보이면 판정기 자체의 결함이다)'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--case', help='이 이름(또는 case id)만 자세히')
    ap.add_argument('--live', nargs='?', const='http://127.0.0.1:5002', metavar='URL',
                    help='**떠 있는 앱**이 실제로 내보내는 HTML 을 세어 본다 '
                         '(디스크는 맞는데 화면이 아닐 때 — 옛 프로세스냐 브라우저 캐시냐)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return _selftest()

    dr, code = _data_root(), _code_root()
    print('═══ 웹앱 데이터 진단 ═══')
    print(f'  코드   {code}')
    print(f'         브랜치 {_git(code, "rev-parse", "--abbrev-ref", "HEAD") or "?"}'
          f' · HEAD {_git(code, "rev-parse", "--short", "HEAD") or "?"}')
    #  ★ 코드가 최신인지 — 배지 고침이 안 들어와 있으면 데이터를 아무리 고쳐도 안 뜬다
    _has_fix = 'refill' in (_git(code, 'log', '-40', '--format=%s') or '')
    print(f'         `--refill` 커밋 있음: {"예" if _has_fix else "**아니오 — git pull 먼저**"}')
    print(f'  데이터 {dr}'
          f'{"" if os.environ.get("DEM_WEB_DATA") else "  (DEM_WEB_DATA 미설정 → 기본값)"}')
    if not os.path.isdir(os.path.join(dr, 'webapp', 'uploads')):
        print(f'\n⛔ {dr}/webapp/uploads 가 없다 — 데이터 루트가 틀렸다.')
        print('   DEM_WEB_DATA=<경로> python3 scripts/diagnose_webapp_data.py')
        return 1

    rows = scan(dr)
    print(f'\n  케이스 {len(rows)}건')
    if not rows:
        print('  ⛔ 0건 — python3 scripts/rebuild_cases_from_csv.py --write')
        return 1

    src = source_mpm_counts()

    if a.case:
        hit = [r for r in rows if a.case in (r['name'], r['cid'])]
        if not hit:
            print(f'\n⛔ `{a.case}` 를 못 찾았다')
            return 1
        for r in hit:
            print(f'\n── {r["name"]}  ({r["cid"]}) ──')
            for k in ('status', 'fm_mpm_keys', 'mm_exists', 'mpm_por', 'dem_por',
                      'has_payload', 'gap'):
                print(f'   {k:14s} {r[k]}')
            print(f'   {"원본 CSV mpm":14s} {src.get(r["name"], src.get(r["cid"], "?"))}개')
            print(f'   {"배지":14s} {r["badge"] or "(없음)"}')
            w = _why(r, src)
            if w:
                print(f'   원인           {w}')
        return 0

    #  ── 요약 — 무엇이 몇 건 ────────────────────────────────────────────────────────
    from collections import Counter
    badges = Counter(r['badge'] for r in rows if r['badge'])
    print('\n── 배지 (이 디스크대로 렌더하면) ──')
    for b, n in sorted(badges.items(), key=lambda x: -x[1]):
        print(f'   {b:18s} {n:>4}건')
    blank = [r for r in rows if not r['badge']]
    print(f'   {"(배지 없음)":18s} {len(blank):>4}건')

    if blank:
        print('\n── 배지가 없는 이유 ──')
        #  ⚠ 이유가 **부류(⓪①②③④)로** 묶여야 한다.  옛 판은 문장에 든 열 개수까지
        #    묶음 키에 들어가 같은 원인이 8줄로 쪼개졌다 — 읽는 사람이 세어야 했다.
        groups = {}
        for r in blank:
            w = _why(r, src)
            groups.setdefault(w[0], [w, []])[1].append(r['name'])
        for _, (why, names) in sorted(groups.items(), key=lambda x: -len(x[1][1])):
            print(f'   {len(names):>4}건  {why}')
            print(f'         예: {", ".join(sorted(names)[:3])}'
                  f'{" …" if len(names) > 3 else ""}')

    #  ── 처방 — **무엇을 돌려야 하는지 한 줄로** ─────────────────────────────────────
    #  ⚠ `n_stale` 은 **원본에 MPM 이 있는데** 디스크에 없는 것만 센다 — 원본에도 없는
    #    케이스까지 세면 아무 일도 안 하는 명령을 찍게 된다 (이 진단기가 잡으려는 그 병).
    n_stale = sum(1 for r in rows
                  if r['status'] == 'reconstructed' and r['fm_mpm_keys'] == 0
                  and (src.get(r['name'], src.get(r['cid'])) or 0) > 0)
    n_nomm = sum(1 for r in rows
                 if r['fm_mpm_keys'] > 0 and r['fm_mpm_por'] and not r['mm_exists'])
    n_never = sum(1 for r in blank if _why(r, src).startswith('⓪'))
    if n_never:
        print(f'\n   ⓪ {n_never}건은 **고칠 것이 없다** (MPM 을 안 돌렸거나 porosity 가 없다)')
    print('\n── 다음 명령 ──')
    if not _has_fix:
        print('   ⛔ 코드가 옛 판이다.  먼저:  git pull')
    if n_stale:
        print(f'   ① 옛 복원본 {n_stale}건 (mpm 열 0개) →')
        print('        python3 scripts/rebuild_cases_from_csv.py --refill')
    if n_nomm or n_stale:
        print('   ② mpm_metrics.json 만들기 →')
        print('        python3 scripts/rebuild_tables_from_metrics.py --write')
    if not (n_stale or n_nomm) and _has_fix:
        print('   ✓ 데이터는 맞다 — 남은 건 **디스크가 아니라 화면**이다.')
        print('     떠 있는 앱이 실제로 뭘 내보내는지 세어 본다:')
        print('        python3 scripts/diagnose_webapp_data.py --live')
    else:
        print('   ③ 그 뒤:  demstop && dem5002')
    if a.live:
        _live_check(a.live, badges)
    return 0


def _live_check(url, want):
    """**떠 있는 앱**의 HTML 에서 배지를 세어 디스크 기대치와 맞춰 본다.

    ★ 왜: 디스크가 맞는데 화면이 아닐 때 원인은 둘 뿐이고 **서로 처방이 다르다** —
      ⓐ 앱이 옛 프로세스/옛 코드로 떠 있다  → `demstop && dem5002`
      ⓑ 서버는 맞는데 브라우저가 옛 HTML 을 보여 준다 → 강력 새로고침 (Ctrl-Shift-R)
      HTML 을 직접 세면 이 둘이 **한 번에** 갈린다.  (사람이 눈으로 세지 않게)
    """
    import urllib.request
    print(f'\n── 떠 있는 앱 확인 ({url}) ──')
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            html = r.read().decode('utf-8', 'replace')
    except Exception as e:
        print(f'   ⛔ 못 붙었다: {e}')
        print('      앱이 안 떠 있다 →  demstop && dem5002')
        print('      다른 포트면 →  --live http://127.0.0.1:<포트>')
        return
    #  ⚠ **배지가 0 인 것에는 여러 뜻이 있다** — 옛 코드 / 로그인 리다이렉트 / 다른 페이지.
    #    행 자체가 있는지부터 세지 않으면 셋을 구분 못 한다 (0 을 보고 "옛 코드" 라고
    #    단정하면 또 헛다리다).
    n_rows = html.count('보관함 저장')
    print(f'   페이지 {len(html):,} 바이트 · 케이스 행 {n_rows}개')
    got = {b: html.count(b) for b in ('MPM ✓', 'MPM SE-rich', 'MPM SE-poor')}
    ok = True
    for b, n_want in sorted(want.items()):
        if not b.startswith('MPM'):
            continue
        n_got = got.get(b, 0)
        mark = '✓' if n_got == n_want else '⛔'
        if n_got != n_want:
            ok = False
        print(f'   {mark} {b:14s} 디스크 {n_want:>4}  ↔  화면 {n_got:>4}')
    if ok and any(got.values()):
        print('\n   ✓ **서버는 배지를 내보내고 있다.**  그래도 안 보이면 브라우저 캐시다:')
        print('        Ctrl-Shift-R (강력 새로고침)  ·  또는 시크릿 창으로 열어 볼 것')
        return
    if n_rows == 0:
        print('\n   ⛔ **케이스 목록 자체가 없다** — 배지 문제가 아니다.')
        print('      로그인 페이지이거나(WEBAPP_REQUIRE_AUTH) 다른 화면일 수 있다.')
    else:
        print(f'\n   ⛔ 목록은 {n_rows}건 나오는데 **배지만 0** = 앱이 옛 코드로 떠 있거나')
        print('      다른 데이터 폴더를 보고 있다.')
    _live_process(url)


def _live_process(url):
    """그 포트를 **실제로 물고 있는 프로세스**가 무엇을 보고 있는지 읽는다.

    ★ 왜: "옛 코드다" vs "다른 폴더다" 는 처방이 다른데, 지금까지는 사용자에게
      확인을 **떠넘기고** 있었다 (`WEBAPP_RESULTS_FOLDER 가 같은지 확인`).
      /proc 에서 직접 읽으면 답이 나온다 — 추측을 사람에게 넘기지 않는다.
    """
    port = url.rsplit(':', 1)[-1].rstrip('/')
    pids = []
    try:
        out = subprocess.run(('ss', '-ltnp'), capture_output=True, text=True,
                             timeout=10).stdout
        for ln in out.splitlines():
            if f':{port} ' in ln or ln.rstrip().endswith(f':{port}'):
                for tok in ln.split('pid='):
                    p = tok.split(',')[0].strip()
                    if p.isdigit():
                        pids.append(p)
    except Exception:
        pass
    #  ⚠⚠ `ss` 는 **그 포트만** 집는다 = 안전.  pgrep 은 `app.py` 를 **전부** 집는다
    #    (다른 포트의 웹앱·다른 프로젝트 포함).  그 목록으로 `kill` 을 찍어 주면
    #    엉뚱한 프로세스를 죽인다.  ⇒ 출처를 기억해 두고, 폴백이면 **kill 을 안 찍는다**.
    exact = bool(pids)
    if not pids:
        try:
            out = subprocess.run(('pgrep', '-f', 'app.py'), capture_output=True,
                                 text=True, timeout=10).stdout
            pids = [p for p in out.split() if p.isdigit()]
        except Exception:
            pass
    if not pids:
        print('\n   (그 포트를 문 프로세스를 못 찾았다 — ss/pgrep 없음)')
        print('   ⇒ 그냥 다시 띄운다:  demstop && dem5002')
        return
    if exact:
        print(f'\n── 포트 {port} 를 물고 있는 프로세스 ──')
    else:
        print('\n── ⚠ 포트를 못 짚어 `app.py` 프로세스를 **전부** 나열한다 ──')
        print('     (아래에 이 포트와 무관한 것이 섞여 있을 수 있다 — 보고 고를 것)')
    for pid in dict.fromkeys(pids):
        print(f'   PID {pid}')
        try:
            print(f'     cwd  {os.readlink(f"/proc/{pid}/cwd")}')
        except OSError:
            pass
        try:
            with open(f'/proc/{pid}/environ', 'rb') as f:
                env = dict(kv.split('=', 1) for kv in
                           f.read().decode('utf-8', 'replace').split('\0') if '=' in kv)
            got = env.get('WEBAPP_RESULTS_FOLDER')
            want = os.path.join(_data_root(), 'webapp', 'results')
            if got:
                mark = '✓' if os.path.realpath(got) == os.path.realpath(want) else '⛔'
                print(f'     {mark} WEBAPP_RESULTS_FOLDER  {got}')
                if mark == '⛔':
                    print(f'       기대  {want}')
                    print('       ⇒ **앱이 다른 폴더를 보고 있다.**  런처로 다시 띄울 것')
            else:
                print('     ⚠ WEBAPP_RESULTS_FOLDER **미설정** — 앱이 코드 폴더 안의')
                print('       빈 results 를 볼 수 있다.  런처(run_dem_webapp.sh)로 띄워야 한다.')
        except OSError:
            print('     (environ 을 못 읽었다 — 다른 사용자 소유 프로세스)')
    print('\n   ⇒ 확실하게 다시 띄우기 (alias 에 안 기대는 방법):')
    if exact:
        print(f'        kill {" ".join(dict.fromkeys(pids))}')
    else:
        #  ★ 포트를 못 짚었으면 **kill 을 만들어 주지 않는다** — 남의 프로세스를 죽인다.
        print(f'        # 위 목록에서 포트 {port} 인 것만 골라 kill 할 것 (전부 죽이지 말 것)')
        print(f'        # 포트 확인:  ss -ltnp | grep :{port}')
    print('        bash ~/dem-web/scripts/run_dem_webapp.sh --bg --open')


def _selftest():
    import tempfile
    n = [0, 0]

    def chk(m, ok):
        n[1] += 1
        n[0] += bool(ok)
        print(f'  {"PASS" if ok else "FAIL"}  {m}')

    with tempfile.TemporaryDirectory() as d:
        up = os.path.join(d, 'webapp', 'uploads')
        rs = os.path.join(d, 'webapp', 'results')

        def mk(cid, meta, fm, mm=None, payload=False):
            os.makedirs(os.path.join(up, cid), exist_ok=True)
            os.makedirs(os.path.join(rs, cid), exist_ok=True)
            json.dump(meta, open(os.path.join(up, cid, 'meta.json'), 'w', encoding='utf-8'))
            json.dump(fm, open(os.path.join(rs, cid, 'full_metrics.json'), 'w',
                               encoding='utf-8'))
            if mm is not None:
                json.dump(mm, open(os.path.join(rs, cid, 'mpm_metrics.json'), 'w',
                                   encoding='utf-8'))
            if payload:
                open(os.path.join(rs, cid, 'mpm_payload.json'), 'w').write('{}')

        base = {'status': 'reconstructed'}
        mk('A', {**base, 'name': 'xval'}, {'porosity_spheresum': 16.3, 'mpm_x': 1},
           {'porosity_mpm_pct': 17.8})                      # gap −1.5 → ✓
        mk('B', {**base, 'name': 'rich'}, {'porosity_spheresum': 5.7, 'mpm_x': 1},
           {'porosity_mpm_pct': 14.1})                      # gap −8.4 → SE-rich
        mk('C', {**base, 'name': 'poor'}, {'porosity_spheresum': 32.8, 'mpm_x': 1},
           {'porosity_mpm_pct': 3.0})                       # gap +29.8 → SE-poor
        mk('D', {**base, 'name': 'stale'}, {'porosity_spheresum': 16.0})   # mpm 열 0개
        #  E = 복원은 됐고 tables 를 안 돌린 것 (porosity 열이 **있다**) → ②
        mk('E', {**base, 'name': 'nomm'},
           {'porosity_spheresum': 16.0, 'mpm_porosity_mpm_pct': 15.0})
        mk('F', {**base, 'name': 'nodem'}, {'mpm_porosity_mpm_pct': 1},
           {'porosity_mpm_pct': 15.0})
        #  H = mpm 열은 있는데 **전부 설정값**이라 박스를 못 만드는 것 → ⓪ (고칠 것 없음)
        mk('H', {**base, 'name': 'cfgonly'}, {'porosity_spheresum': 16.0,
                                              'mpm_n_grid': 384, 'mpm_protocol': 'hold'})

        rows = {r['name']: r for r in scan(d)}
        chk(f'① 케이스를 다 읽는다 ({len(rows)}건)', len(rows) == 7)
        chk(f'② |gap| ≤ 4 → cross-validated ({rows["xval"]["badge"]})',
            rows['xval']['badge'] == 'MPM ✓')
        chk(f'③ gap < −4 → SE-rich ({rows["rich"]["badge"]} · gap {rows["rich"]["gap"]})',
            rows['rich']['badge'] == 'MPM SE-rich' and rows['rich']['gap'] == -8.4)
        chk(f'④ gap > +4 → SE-poor ({rows["poor"]["badge"]})',
            rows['poor']['badge'] == 'MPM SE-poor')
        chk('⑤ ★ 옛 복원본(mpm 열 0개)을 **①번 원인**으로 짚는다',
            rows['stale']['badge'] == '' and _why(rows['stale']).startswith('①'))
        #  ★★ 원본 대조 — 같은 "mpm 열 0개" 를 **두 가지로 갈라야** 한다.
        #     안 가르면 아무 일도 안 하는 명령을 찍는다 = 이 도구가 잡으려는 그 병.
        chk('⑤a ★★ 원본에 MPM 이 **있으면** → 옛 복원본(①, refill 이 고친다)',
            _why(rows['stale'], {'stale': 39}).startswith('①')
            and 'refill' in _why(rows['stale'], {'stale': 39}))
        chk('⑤b ★★ 원본에도 **없으면** → 고칠 것 없음(⓪) — 헛명령을 안 찍는다',
            _why(rows['stale'], {'stale': 0}).startswith('⓪')
            and 'refill' not in _why(rows['stale'], {'stale': 0}))
        chk('⑤c 원본을 못 읽으면 **모른다고 말한다** (지어내지 않는다)',
            '원본 대조 실패' in _why(rows['stale'], {}))
        chk('⑥ ★ mpm_metrics.json 부재를 **②번 원인**으로 짚는다',
            rows['nomm']['badge'] == '' and _why(rows['nomm']).startswith('②'))
        chk('⑥a ★★ mpm 열이 **설정값뿐**이면 ② 가 아니라 ⓪ — 헛명령을 안 찍는다',
            rows['cfgonly']['badge'] == '' and not rows['cfgonly']['fm_mpm_por']
            and _why(rows['cfgonly']).startswith('⓪'))
        chk('⑦ DEM 짝 부재를 **④번 원인**으로 짚는다',
            rows['nodem']['badge'] == '' and _why(rows['nodem']).startswith('④'))
        #  ★★ 음성 대조 — 진단기는 **아무것도 고치지 않는다** (읽기 전용)
        before = sorted(os.path.join(r, f) for r, _, fs in os.walk(d) for f in fs)
        scan(d)
        chk('⑧ ★★ 읽기 전용 — 진단이 파일을 만들거나 바꾸지 않는다',
            sorted(os.path.join(r, f) for r, _, fs in os.walk(d) for f in fs) == before)
        #  ★ 문턱이 app.py 와 같은가 — 복사본이 갈라지면 진단이 거짓말을 한다
        ap_src = os.path.join(_code_root(), 'webapp', 'app.py')
        txt = open(ap_src, encoding='utf-8').read() if os.path.exists(ap_src) else ''
        chk('⑨ ★ gap 문턱이 app.py 와 같다 (복사본 표류 감시)',
            f'_gap > {GAP_THRESHOLD}' in txt and f'_gap < -{GAP_THRESHOLD}' in txt)
        #  ★ payload 만 있고 metrics 가 없는 옛 실런 — 배지는 뜨되 regime 은 없다
        mk('G', {'status': 'done', 'name': 'realrun'}, {'porosity_spheresum': 16.0},
           payload=True)
        g = {r['name']: r for r in scan(d)}['realrun']
        chk(f'⑩ payload 만 있는 실런은 payload 배지 ({g["badge"]})',
            g['badge'] == 'MPM ✓(payload)' and g['gap'] is None)
        #  ★ 원본 대조표가 실제 표에서 읽히는가 (이름·ID 양쪽으로 찾을 수 있어야)
        sm = source_mpm_counts()
        chk(f'⑪ ★ 원본 CSV 에서 MPM 열 수를 읽는다 (항목 {len(sm)}개)',
            len(sm) > 200 and sm.get('input_2mAh_real_14', 0) > 0)
        chk('⑫ 이름으로도 case-id 로도 찾힌다',
            sm.get('input_S_1') is not None)

    print(f'\ndiagnose_webapp_data selftest: {n[0]}/{n[1]} PASS')
    return 0 if n[0] == n[1] else 1


if __name__ == '__main__':
    sys.exit(main())
