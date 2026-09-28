#!/usr/bin/env python3
"""mixer_smoke_blind.py — bin 0 스모크를 **M 을 보지 않고** 판독해 발사 관문용 증서만 남기는 래퍼 (Codex 6 차 Q5 · 2026-09-29).

왜 — 판독기 `measure_mixing_index.py` 의 일반 CLI 는 JSON 전에 M · S₀² · S_R² 를 화면에 쓴다.  bin 0 스모크는 기술 실패만 거르는
관문인데 (사전등록 §8 · K5) 그때 M 이 보이면 나머지 시드 발사 결정이 결과에 오염된다.  ⇒ 이 래퍼는
  ① 판독기를 **stdout · stderr 를 가로채** 부른다 (판독기의 어떤 출력도 화면에 나오지 않는다)
  ② 전체 결과를 **접근 제한 파일** (<런>/.smoke_blind/full_<시각>.json · 0600) 에 봉인한다 — "계산했지만 보지 않았다" 와 "계산 안 했다" 를
     가른다 (Codex: 감사 가능한 유일한 결과를 폐기할 이유는 없다)
  ③ 증서에는 **명시적 허용목록**만 투영한다 (삭제목록이 아니다 — 판독기에 새 필드가 생겨도 자동 노출되지 않는다):
       run · provenance · plan · t0_step · smoke.complete · smoke.tech_smoke · smoke.qc_repr.pass
     = `launch_highbo.sh rest` 관문이 읽는 전부 (`mixer_gate_reader_diff.py` 의 opaque_allowlisted_certificate 가 rc 0 을 확인)
  ④ 판독기가 거부 (SystemExit · 예외) 하면 그 문구 (S₀² · S_R² 값이 들어 있을 수 있다) 도 봉인 파일에만 두고 화면에는 사유 코드만 낸다
  ⑤ 열람 기록 <런>/.smoke_blind/blind_log.jsonl — 언제 · 누가 · 어느 도구 (sha256) 로 · 무엇을 (투영 필드 목록) 보았는지 · 전체 결과 sha256.
⛔ 이 래퍼는 증서의 plan · t0_step · provenance 를 **손대지 않는다** (판독기 값 그대로) — 그 필드는 신뢰된 주장이라 (Codex §3
  `tampered_certificate_narrows_bin0`) 투영기가 편집하면 관문의 창 정의가 무너진다.
⚠ 래퍼가 막는 것은 **화면 노출**이다 — 봉인 파일을 여는 것은 사람의 규율 (열람하면 blind_log 에 적는다 · 사전등록 §8 ⑤).

    python3 scripts/mixer_smoke_blind.py <OUT>/LH_s32452843 --ref <OUT>/E0_s32452843 --cert <OUT>/LH_s32452843/smoke_cert.json
    python3 scripts/mixer_smoke_blind.py --selftest
rc 0 = 증서 씀 (합격 여부는 관문이 판정한다 — 이 래퍼는 판정하지 않는다) · rc 2 = 판독기 거부 (증서 없음 · 사유는 봉인 파일) · rc 1 = 입력 오류.
"""
from __future__ import annotations

import argparse
import contextlib
import copy
import datetime
import getpass
import hashlib
import io
import json
import os
import socket
import sys
import tempfile
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import measure_mixing_index as mi     # noqa: E402

REG = dict(r_container=0.013138, cells=16, x_cells=4, n_min=20, axis='x')     # 사전등록 §2-3 · §8 ③ — 관문 REG 와 같다 (바꾸지 않는다)
ALLOW_TOP = ('run', 'provenance', 'plan', 't0_step')
ALLOW_SMOKE = ('complete', 'tech_smoke')
ALLOW_QC = ('pass',)
#: 결과 대리량으로 취급하는 키 — 투영 · 화면 어디에도 나오면 안 된다 (자기검사 누설 시험)
RESULT_KEYS = ('M', 'M_final', 'S0', 'SR', 'S0_sq', 'SR_sq', 'rows', 'by_rev', 'flat', 'planned', 'sd', 'M_t')


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha_file(p) -> str:
    return _sha_bytes(Path(p).read_bytes())


def project(full: dict) -> dict:
    """전체 판독 결과 → 허용목록 투영 (깊은 복사 · 값 편집 없음).  허용 키가 없으면 KeyError (모양이 다른 판독기 = 거부)."""
    e = {k: copy.deepcopy(full[k]) for k in ALLOW_TOP}
    sm = full['smoke']
    e['smoke'] = {k: copy.deepcopy(sm[k]) for k in ALLOW_SMOKE}
    e['smoke']['qc_repr'] = {k: copy.deepcopy(sm['qc_repr'][k]) for k in ALLOW_QC}
    return e


def _keys(v, out=None):
    out = set() if out is None else out
    if isinstance(v, dict):
        for k, x in v.items():
            out.add(str(k))
            _keys(x, out)
    elif isinstance(v, (list, tuple)):
        for x in v:
            _keys(x, out)
    return out


def leak_check(obj) -> list:
    """투영 안 어느 깊이에도 결과 키가 없는지 (있으면 그 키 목록)."""
    return sorted(k for k in _keys(obj) if k in RESULT_KEYS)


def run_blind(run_dir: str, ref_dir: str, cert: str, reg=REG):
    """판독 → 봉인 → 투영 → 증서.  반환 (rc, 요약 dict)."""
    run_dir, ref_dir = os.path.normpath(run_dir), os.path.normpath(ref_dir)
    vault = Path(run_dir) / '.smoke_blind'
    vault.mkdir(parents=True, exist_ok=True)
    os.chmod(vault, 0o700)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')     # µs — 같은 초의 두 호출도 다른 파일
    buf_out, buf_err = io.StringIO(), io.StringIO()
    full, refused = None, None
    with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
        try:
            full = mi.analyse(run_dir, ref_dir, reg['r_container'], cells=reg['cells'], x_cells=reg['x_cells'],
                              n_min=reg['n_min'], axis=reg['axis'])
        except SystemExit as e:                       # 판독기의 거부 — 문구에 S₀² · S_R² 가 들어 있을 수 있다 → 봉인 파일에만
            refused = dict(kind='SystemExit', message=str(e))
        except Exception as e:                        # noqa: BLE001 — 어떤 예외든 화면에 내지 않는다
            refused = dict(kind=type(e).__name__, message=str(e), traceback=traceback.format_exc())
    record = dict(schema='mixer_smoke_blind_full/1', time_utc=ts, run=run_dir, ref=ref_dir, args=dict(reg),
                  reader_sha256=_sha_file(mi.__file__), wrapper_sha256=_sha_file(__file__),
                  reader_stdout=buf_out.getvalue(), reader_stderr=buf_err.getvalue(), refused=refused, result=full)
    for k in range(1000):                              # O_EXCL — 있는 파일을 덮지 않는다 (같은 µs 면 접미사)
        full_path = vault / (f'full_{ts}.json' if k == 0 else f'full_{ts}_{k}.json')
        try:
            fd = os.open(full_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            break
        except FileExistsError:
            continue
    else:
        raise RuntimeError('봉인 파일 이름을 만들 수 없다')
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        json.dump(record, fh, ensure_ascii=False, indent=1, default=str)
        fh.write('\n')
    os.chmod(full_path, 0o600)
    full_sha = _sha_file(full_path)
    log = dict(time_utc=ts, user=getpass.getuser(), host=socket.gethostname(), tool=os.path.realpath(__file__),
               wrapper_sha256=record['wrapper_sha256'], reader_sha256=record['reader_sha256'], args=dict(reg),
               full_file=str(full_path), full_sha256=full_sha, viewed='projection only' if refused is None else 'refusal code only',
               projected_fields=None, cert=None, cert_sha256=None)
    rc, summary = 2, dict(full_file=str(full_path), full_sha256=full_sha)
    if refused is None:
        try:
            e = project(full)
        except (KeyError, TypeError) as ex:
            refused = dict(kind='ProjectionShape', message=f'{type(ex).__name__}: {ex}')
    if refused is None:
        leaks = leak_check(e)
        if leaks:                                       # 허용목록 안에 결과 키가 숨어 들어왔다 — 증서를 쓰지 않는다
            refused = dict(kind='Leak', message=f'투영 안 결과 키 {leaks}')
    if refused is None:
        body = json.dumps([e], ensure_ascii=False, indent=1) + '\n'
        Path(cert).parent.mkdir(parents=True, exist_ok=True)
        tmp = str(cert) + '.tmp'
        Path(tmp).write_text(body, encoding='utf-8')
        os.replace(tmp, cert)
        log.update(projected_fields=dict(top=list(ALLOW_TOP), smoke=list(ALLOW_SMOKE), qc_repr=list(ALLOW_QC)),
                   cert=os.path.realpath(cert), cert_sha256=_sha_bytes(body.encode('utf-8')))
        rc = 0
        summary.update(cert=str(cert), complete=e['smoke']['complete'], n_tech=len(e['smoke']['tech_smoke']),
                       qc_pass=e['smoke']['qc_repr']['pass'])
    else:
        log['refused_kind'] = refused['kind']
        summary.update(refused_kind=refused['kind'])
    with (vault / 'blind_log.jsonl').open('a', encoding='utf-8') as fh:
        fh.write(json.dumps(log, ensure_ascii=False) + '\n')
    os.chmod(vault / 'blind_log.jsonl', 0o600)
    return rc, summary


def main(argv=None):
    ap = argparse.ArgumentParser(description='bin 0 스모크 M-맹검 래퍼 (Codex 6 차 Q5)')
    ap.add_argument('run', nargs='?', help='평가 런 폴더 (예 <OUT>/LH_s32452843)')
    ap.add_argument('--ref', help='E0 기준 런 폴더')
    ap.add_argument('--cert', help='증서 경로 (관문 rest 의 입력)')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.run and a.ref and a.cert):
        ap.error('<run> --ref <ref> --cert <cert> 가 필요하다')
    for lab, p in (('run', a.run), ('ref', a.ref)):
        if not os.path.isdir(p):
            print(f'⛔ {lab} 폴더 없음: {p}')
            return 1
    rc, s = run_blind(a.run, a.ref, a.cert)
    if rc == 0:
        print(f"✓ 증서 → {s['cert']} (complete={s['complete']} · tech_smoke {s['n_tech']} 건 · qc_repr.pass={s['qc_pass']}) · "
              f"전체 결과 봉인 {s['full_file']} (0600 · sha256 {s['full_sha256'][:12]}…) — M 은 화면에 내지 않았다")
    else:
        print(f"⛔ 판독기 거부 (사유 코드 {s['refused_kind']}) — 증서 없음.  사유 문구는 봉인 파일 {s['full_file']} 에만 있다 (열면 blind_log 에 적을 것)")
    return rc


# ──────────────────────────────────────────────────────────────────────────────
def selftest():
    import shutil
    import subprocess
    from mixer_gate_reader_diff import build, REST, FIRST         # 같은 합성 폴더 · 같은 관문 (규율 ①)
    fails = []

    def chk(name, ok):
        print(('  ✓ ' if ok else '  ✗ ') + name)
        if not ok:
            fails.append(name)

    with tempfile.TemporaryDirectory(prefix='smoke_blind_') as tmp:
        td = Path(tmp)
        run, ref, cert, original, invoke = build(td)
        cert.unlink()                                                          # build 가 쓴 '전체' 증서는 버린다 — 래퍼가 다시 쓴다
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = main([str(run), '--ref', str(ref), '--cert', str(cert)])
        shown = out.getvalue() + err.getvalue()
        e = json.loads(cert.read_text(encoding='utf-8'))[0]
        chk('① 정상: rc 0 · 증서 = 허용목록 정확히 (run · provenance · plan · t0_step · smoke{complete · tech_smoke · qc_repr{pass}})',
            rc == 0 and sorted(e) == sorted(ALLOW_TOP + ('smoke',)) and sorted(e['smoke']) == sorted(ALLOW_SMOKE + ('qc_repr',))
            and list(e['smoke']['qc_repr']) == ['pass'])
        chk('①b 투영 값 = 판독기 값 그대로 (plan · t0_step · provenance 편집 없음)',
            e['plan'] == original['plan'] and e['t0_step'] == original['t0_step'] and e['provenance'] == original['provenance'])
        chk('①c ★ 화면 (stdout · stderr) 에 판독기 출력 · 결과 키 · M 값이 없다',
            not any(k in shown for k in ('M_final', 'S0', 'SR', 'by_rev')) and f"{original['M_final']:.4f}"[:5] not in shown
            and str(original['S0'])[:6] not in shown)
        chk('①d 증서에 결과 키 없음 (leak_check) · 전체 결과는 봉인 파일 (0600) 에 · 열람 기록 1 줄 (projection only · 증서 sha)',
            leak_check(e) == [] and (run / '.smoke_blind').is_dir()
            and all(oct(p.stat().st_mode)[-3:] == '600' for p in (run / '.smoke_blind').glob('full_*.json'))
            and json.loads((run / '.smoke_blind/blind_log.jsonl').read_text(encoding='utf-8').splitlines()[-1])['viewed'] == 'projection only')
        full = json.loads(next((run / '.smoke_blind').glob('full_*.json')).read_text(encoding='utf-8'))
        chk('①e 봉인 파일에는 전체 결과 (M_final · S0 · SR · rows …) 가 있다 = "계산했지만 보지 않았다" (판독기 화면 출력도 같은 파일에 갇힌다)',
            full['result']['M_final'] == original['M_final'] and full['result']['S0'] == original['S0']
            and isinstance(full['reader_stdout'], str) and full['refused'] is None)
        chk('① 관문 (launch_highbo.sh rest 블록) 이 이 증서로 rc 0', invoke()['rc'] == 0)

        src, dup = run / 'post/mix_400.liggghts', run / 'post/copy_400.liggghts'
        shutil.copyfile(src, dup)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc2 = main([str(run), '--ref', str(ref), '--cert', str(cert)])
        e2 = json.loads(cert.read_text(encoding='utf-8'))[0]
        chk('② 기술 실패 (bin 0 복제): 래퍼는 판정하지 않고 rc 0 · 증서 complete=false → 관문 rc 1',
            rc2 == 0 and e2['smoke']['complete'] is False and invoke()['rc'] == 1)
        dup.unlink()

        e0dup = ref / 'post/copy_200.liggghts'
        shutil.copyfile(ref / 'post/mix_200.liggghts', e0dup)
        cert.unlink()
        out3 = io.StringIO()
        with contextlib.redirect_stdout(out3), contextlib.redirect_stderr(io.StringIO()):
            rc3 = main([str(run), '--ref', str(ref), '--cert', str(cert)])
        logs = [json.loads(l) for l in (run / '.smoke_blind/blind_log.jsonl').read_text(encoding='utf-8').splitlines()]
        chk('③ ★ 판독기 거부 (E0 t₀ 둘): rc 2 · 증서 없음 · 화면에는 사유 코드 (SystemExit) 만 — 거부 문구 (숫자) 는 봉인 파일에',
            rc3 == 2 and not cert.exists() and 'SystemExit' in out3.getvalue() and '계획 t₀' not in out3.getvalue()
            and logs[-1]['viewed'] == 'refusal code only' and logs[-1]['refused_kind'] == 'SystemExit')
        e0dup.unlink()

        #  ④ 누설 시험 — 판독기가 허용 키 안에 결과 대리량을 숨겨 돌려주면 (합성) 증서를 쓰지 않는다
        real = mi.analyse

        def fake(*a_, **k_):
            v = real(*a_, **k_)
            v['smoke']['tech_smoke'] = list(v['smoke']['tech_smoke']) + [{'M_final': v['M_final']}]
            return v
        mi.analyse = fake
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc4 = main([str(run), '--ref', str(ref), '--cert', str(cert)])
        finally:
            mi.analyse = real
        chk('④ ★ 허용 키 (tech_smoke) 안에 결과 키가 숨어 오면 Leak 거부 · rc 2 · 증서 없음', rc4 == 2 and not cert.exists())

        #  ⑤ 판독기가 다른 모양 (허용 키 없음) 이면 거부
        mi.analyse = lambda *a_, **k_: {'run': 'x'}
        try:
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc5 = main([str(run), '--ref', str(ref), '--cert', str(cert)])
        finally:
            mi.analyse = real
        chk('⑤ 판독기 결과에 허용 키가 없으면 ProjectionShape 거부 · rc 2', rc5 == 2 and not cert.exists())

        #  ⑥ 예외 (파일 없음 → 판독기 내부 예외) 도 화면에 traceback 을 내지 않는다
        shutil.rmtree(ref / 'post')
        out6 = io.StringIO()
        with contextlib.redirect_stdout(out6), contextlib.redirect_stderr(io.StringIO()):
            rc6 = main([str(run), '--ref', str(ref), '--cert', str(cert)])
        chk('⑥ 판독기 예외/거부: rc 2 · 화면에 Traceback 없음 · 사유 코드만', rc6 == 2 and 'Traceback' not in out6.getvalue())
        #  ⑦ CLI 로도 같은 화면 규율 (서브프로세스 · 정상 폴더 재구성)
        run2, ref2, cert2, orig2, _inv = build(td / 'cli')
        cert2.unlink()
        p = subprocess.run([sys.executable, __file__, str(run2), '--ref', str(ref2), '--cert', str(cert2)],
                           capture_output=True, text=True, encoding='utf-8')
        chk('⑦ CLI 서브프로세스: rc 0 · 증서 · 화면에 M 값 · 결과 키 없음',
            p.returncode == 0 and cert2.is_file() and 'M_final' not in p.stdout + p.stderr
            and f"{orig2['M_final']:.4f}"[:5] not in p.stdout + p.stderr)
    print()
    if fails:
        print(f'✗ {len(fails)} 건 실패')
        return 1
    print('✓ 전부 통과 — 래퍼는 판독기 출력을 가로채고 허용목록만 투영하며, 거부 · 예외 · 누설을 화면에 내지 않는다.  '
          '⚠ 봉인 파일을 여는 것은 사람의 규율이다 (열람 = blind_log)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
