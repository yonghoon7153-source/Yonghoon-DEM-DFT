"""(우리 파생 탐침 · G2RR4-01 — Codex `probes/release_gate.py` 를 바탕으로 한 것 · 원 탐침은 무변경으로 따로 돌린다)

Codex 탐침은 정상 대조를 포함한 **모든** 변이의 다시 읽기 `meta` · `cases` 를 최소 꼴 (meta 'M2 all completed' 한 줄 · 케이스마다 K1 하나) 로 덮어쓴다.
상세 계약 (필수 검사 ID 한 번씩 · 빈 checks 공집합 PASS 금지) 을 둔 고친 트리에서는 그 정상 대조까지 거부된다 — 그러면 "새 관문이 정상 기록까지 막는가" 와
"변이를 막는가" 가 갈리지 않는다.  여기서는 고친 트리의 시험 픽스처 (`scripts/test_lhs_release_v13.py` 의 `make_batch_root` — 생산자 계약 꼴 상세 reread ·
관측 객체 · 단계 결합 기록이 든 감사 · manifest `observe_imports`) 를 **덮어쓰지 않고** 그 위에 Codex 와 같은 변이만 넣어 실제 build_v13 → check_v13 를 돌린다
(상위 τ 재독해만 대역 — Codex 와 같음).  `audit_observation_inner_failed` = 같은 부류 (관측 객체는 그대로 · 내부 problems · outside 만 · 최상위 [] 유지).
합성 픽스처의 관문 반례다 — 실제 194 배치 · 값의 인증이 아니다.
"""
from pathlib import Path
import sys, json, contextlib, io, tempfile
from unittest.mock import patch
R = Path(__file__).resolve().parents[1]; S = R / ('sour' + 'ce'); E = R / 'evidence'
P = E / 'release_gate_detailed'; P.mkdir(parents=True, exist_ok=True); D = Path(tempfile.mkdtemp(prefix='run_', dir=P))
sys.path[:0] = [str(S / 'scripts'), str(S / 'webapp')]
p = S / 'scripts/test_lhs_release_v13.py'; ns = {'__file__': str(p), '__name__': 'review_fixture'}
exec(compile(p.read_text(encoding='utf8').split("print('V0  API')")[0], str(p), 'exec'), ns)
lb = ns['LRB']; hd = ns['make_g2_handover_dir'](str(D / 'handover'))
verdict = D / 'TEST_ONLY_NOT_A_GO.md'; verdict.write_text('SYNTHETIC TEST ONLY\n', encoding='utf8')
cases = []
for label in ('control', 'absent_reread', 'null_nfail', 'failed_audit', 'wrong_manifest', 'reread_checks_false', 'reread_cases_missing',
              'audit_observation_failed', 'audit_observation_inner_failed'):
    br = Path(ns['make_batch_root'](str(D / label)))
    rr = json.loads((br / 'reread.json').read_text(encoding='utf8')); aa = json.loads((br / 'seal_audit.json').read_text(encoding='utf8'))
    shape = dict(meta=len(rr.get('meta') or []), cases=len(rr.get('cases') or []),
                 checks_per_case=sorted({len(c.get('checks') or []) for c in rr.get('cases') or []}),
                 observation_keys=sorted((aa.get('import_observation') or {}).keys()))
    if label == 'absent_reread':
        (br / 'reread.json').unlink()
    if label == 'null_nfail':
        rr['n_fail'] = None
    if label == 'failed_audit':
        aa['input_problems'] = ['raw bytes mismatch']
    if label == 'wrong_manifest':
        rr['manifest_sha256'] = '0' * 64
    if label == 'reread_checks_false':                       # Codex 와 같은 모순 — M2 ok=false · n_fail 0 그대로
        next(x for x in rr['meta'] if str(x.get('name', '')).startswith('M2')).update(ok=False, detail='explicit failure')
    if label == 'reread_cases_missing':                      # Codex 와 같음 — read_n 194 그대로
        rr['cases'] = []; rr['meta'] = []
    if label == 'audit_observation_failed':                  # Codex 와 같음 — 관측 객체를 통째로 {problems · outside}
        aa['import_observation'] = {'problems': ['log truncated'], 'outside': ['scripts/unsealed.py']}
    if label == 'audit_observation_inner_failed':            # 같은 부류 — 관측 객체 그대로 · 내부 문제만 · 최상위 [] 유지
        aa['import_observation'].update(problems=['log truncated'], outside=['scripts/unsealed.py'])
    if label != 'absent_reread':
        (br / 'reread.json').write_text(json.dumps(rr), encoding='utf8')
    (br / 'seal_audit.json').write_text(json.dumps(aa), encoding='utf8')
    log = io.StringIO()
    with patch.object(lb, 'v13_reread_tau', lambda *a, **k: []), contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        try:
            rep = lb.build_v13(out_dir=str(br / 'out'), handover_dir=hd, batch_root=str(br), date='20991231', codex_verdict=str(verdict))
            check = lb.check_v13(str(br / 'out'), hd); row = dict(label=label, accepted=True, check=check)
        except Exception as ex:
            row = dict(label=label, accepted=False, error=f'{type(ex).__name__}: {ex}')
    row.update(fixture_shape=shape, out_dir_exists=(br / 'out').exists())
    cases.append(row); (br / 'build.log').write_text(log.getvalue(), encoding='utf8'); print(json.dumps(row, ensure_ascii=False)[:500], flush=True)
(E / 'release_gate_detailed.json').write_text(json.dumps(dict(scope=__doc__, artifact_root=str(D), cases=cases), ensure_ascii=False, indent=2), encoding='utf8')
