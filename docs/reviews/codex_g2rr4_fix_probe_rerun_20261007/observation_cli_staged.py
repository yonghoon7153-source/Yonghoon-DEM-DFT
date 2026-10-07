"""(우리 파생 탐침 · G2RR4-02 — Codex `probes/observation_cli.py` 를 바탕으로 한 것 · 원 탐침은 무변경으로 따로 돌린다)

Codex 탐침의 합성 1 케이스 픽스처 (`fixtures/seal_baseline` — 재검증 3 의 옛 실행기 ROOT · 케이스 기록에 단계 기록 `stages` 가 없다) 는
고친 실행기에서 네 행 모두 "완료 시도의 실행 단계 기록이 없다" 로 거부된다 — 그것만으로는 단계 ↔ 영수증 결합이 **쌍 결손 자체**를 잡는지 갈리지 않는다.
여기서는 픽스처에 **단계 기록만** 더한다: 워커 케이스 기록 (`cases/<c>/out/status.json`) · merged 사본에 생산 워커 (`lhs_webapp_batch.py`) 가 싣는 꼴의
`stages` (stop_after='network' bimodal 경로의 단계 이름 — 10-07 WSL 스모크의 lhs00_055 기록과 같은 목록) · `mode` 를 넣고, 시도 봉인 `record_sha` 를
실행기 함수 `_rec_sha` 로 다시 맞춘다 (옛 실행기 ROOT 의 대체 경로 = 지금 기록을 쓴 시도의 기록에서 단계 계획).  영수증 · 네 변이 · 실제 audit CLI 는
Codex 탐침과 같다 (5/5 · 파서 끝만 없음 · 파서 쌍 없음 · 워커 + 솔버만).  생산 워커 · 시뮬레이션 없음 · 결과 = evidence/observation_cli_staged.json.
"""
from pathlib import Path
import sys, json, shutil, subprocess
R = Path(__file__).resolve().parents[1]; S = R / ('sour' + 'ce'); E = R / 'evidence'
sys.path[:0] = [str(S / 'scripts'), str(S / 'webapp')]
import run_network_194_parallel as rn                    # noqa: E402

base = R / 'fixtures/seal_baseline'
source = E / 'receipt_path_translation/import_obs/log'
case = 'lhs00_000'
STAGES = [dict(step=s, rc=0, ok=(None if s == 'Network Merge' else True)) for s in (
    'Parse', 'Bimodal Contact Analysis', 'Coverage Physics vs Hertzian', 'Network Solver (both modes)',
    'Network channel verdict (ionic/electronic/thermal)', 'Network stop contract (stop_after=network)',
    'Network ionic record check (승격 전 공용 기술 검사 · RGLR2-01)', 'Network Merge')]
receipts = []
for p in source.glob('*.start.json'):
    j = json.loads(p.read_text(encoding='utf8'))
    if j['identity']['case'] == 'lhs00_055':
        receipts.append(p.name[:-len('.start.json')])
out = []
for label in ('all5', 'helper_final_missing', 'helper_pair_missing', 'only_worker_and_solver'):
    root = E / 'observation_cli_staged' / label
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(base, root)
    m = json.loads((root / 'manifest.json').read_text(encoding='utf8'))
    m.update(repo_root=str(S), worker_script=str(S / 'scripts/lhs_webapp_batch.py'), observe_imports=True, import_obs_run_id='81dc4ccc995152e9f06cfbc45d1cae8e')
    m['plan']['cohorts'][0].update(harvest_dir=str(root / 'harvest'), cohort=str(root / 'cohort.tsv'))
    (root / 'manifest.json').write_text(json.dumps(m), encoding='utf8')
    for stp in (root / 'cases' / case / 'out' / 'status.json', root / 'merged' / 'lhs' / 'status.json'):   # ← Codex 탐침에 없는 줄 (단계 기록만)
        st = json.loads(stp.read_text(encoding='utf8'))
        st['cases'][case].update(stages=STAGES, mode='bimodal')
        stp.write_text(json.dumps(st), encoding='utf8')
    rec = json.loads((root / 'cases' / case / 'out' / 'status.json').read_text(encoding='utf8'))['cases'][case]
    wp = root / 'cases' / case / 'worker.json'
    w = json.loads(wp.read_text(encoding='utf8'))
    w['attempts'][-1]['seal']['record_sha'] = rn._rec_sha(rec)                                             # ← 같은 함수로 봉인 다시 맞춤
    wp.write_text(json.dumps(w), encoding='utf8')
    logs = root / 'import_obs/log'; logs.mkdir(parents=True, exist_ok=True)
    for tok in receipts:
        for suffix in ('.start.json', '.txt'):
            p = source / (tok + suffix)
            (logs / p.name).write_text(p.read_text(encoding='utf8').replace('lhs00_055', case), encoding='utf8')
    obs = rn.import_observation(root / 'import_obs', S)
    other = [p for p in obs['processes'] if p['role'] == 'other']
    if label == 'helper_final_missing':
        (logs / (other[0]['proc'] + '.txt')).unlink()
    if label in ('helper_pair_missing', 'only_worker_and_solver'):
        for p in (other[:1] if label == 'helper_pair_missing' else other):
            for suffix in ('.start.json', '.txt'):
                (logs / (p['proc'] + suffix)).unlink()
    p = subprocess.run([sys.executable, '-B', str(S / 'scripts/run_network_194_parallel.py'), 'audit', '--root', str(root), '--json', str(root / 'audit.json')],
                       capture_output=True, text=True, encoding='utf8')
    (root / 'audit.log').write_text(p.stdout + p.stderr, encoding='utf8')
    a = json.loads((root / 'audit.json').read_text(encoding='utf8'))
    io_ = a.get('import_observation') or {}
    rel = lambda x: Path(x['main']).name                                                                   # noqa: E731
    row = dict(label=label, rc=p.returncode, verdicts=a.get('verdicts'), merged=a.get('merged'), input_problems=a.get('input_problems'),
               generation_problems=a.get('generation_problems'), import_problems=a.get('import_observation_problems'),
               n_start=io_.get('n_started'), n_final=io_.get('n_finalized'),
               removed=([rel(x) + ' (시작 · 끝)' for x in other] if label == 'only_worker_and_solver' else
                        [rel(other[0]) + (' (끝만)' if label == 'helper_final_missing' else ' (시작 · 끝)')] if label != 'all5' else []),
               stage_binding=(io_.get('stage_binding') or {}).get('attempts'))
    out.append(row); print(json.dumps(row, ensure_ascii=False)[:600], flush=True)
(E / 'observation_cli_staged.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf8')
