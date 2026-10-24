#!/usr/bin/env python3
"""Literal encoding of Q9 design rev 2 (9a72d65c6) §3-5 adoption + §3-1/§3-4 merge checks (rule-level probe, no chain code).

pre-result(folder)  = no arm payload (p2_*.json) INSIDE the attempt folder  AND  a runner stop record whose name is in PRE_LIST
adoption(unit)      = ledger order: first COMPLETED attempt; every earlier attempt must be pre-result; a post-result stop first → unit = that stop
folder-less entry   = ATTEMPT_LEDGER_MISMATCH (rev 2: even with a reason)
merge checks        = after adoption: machine ∈ allowed · no-op env == ladder env  (§3-1 · §3-4 — merge-time only in the doc)
"""
import json

ALLOWED = {'kgy', 'gabia', 'v100'}
LADDER_ENV = {'P0': 'E_A'}


def pre_result(f, pre_list):
    return (not f['payload_in_folder']) and (f.get('runner_stop') in pre_list)


def merge_unit(unit, ledger, folders, pre_list, noop_law=None):
    ents = [e for e in ledger if e['unit'] == unit]
    for e in ents:
        if e['id'] not in folders:
            return 'STOP ATTEMPT_LEDGER_MISMATCH (folder-less entry %s)' % e['id']
    for e in ents:
        f = folders[e['id']]
        if f['end'] == 'complete':
            if f['machine'] not in ALLOWED:
                return f'adopt {e["id"]} → STOP MACHINE_NOT_ALLOWED'
            if noop_law and f['env'] != LADDER_ENV[noop_law]:
                return f'adopt {e["id"]} → STOP NOOP_ENV_MISMATCH'
            return f'adopt {e["id"]} ({f["machine"]})'
        if pre_result(f, pre_list):
            continue
        return f'unit result = stop {f.get("runner_stop") or f.get("code")} of {e["id"]} (post-result)'
    return 'no completed attempt'


out = {}
PRE = {'ENV_SIGMA_VGCF_OVERRIDE', 'OUTDIR_NOT_EMPTY', 'TIME_LIMIT', 'KIT_MISSING', 'RUNNER_RC'}   # one reading: RUNNER_RC = resource
PRE_NO_RC = PRE - {'RUNNER_RC'}                                                                  # other reading

# A — selection without editing any file: entries #1 kgy, #2 gabia committed in that order; #2 is STARTED first.
ledger = [{'id': 'U#1', 'unit': 'U'}, {'id': 'U#2', 'unit': 'U'}]
like_gabia = {'U#1': {'end': 'stop', 'payload_in_folder': False, 'runner_stop': 'ENV_SIGMA_VGCF_OVERRIDE', 'machine': 'kgy', 'env': 'x'},
              'U#2': {'end': 'complete', 'payload_in_folder': True, 'machine': 'gabia', 'env': 'y'}}
like_kgy = {'U#1': {'end': 'complete', 'payload_in_folder': True, 'machine': 'kgy', 'env': 'x'},
            'U#2': {'end': 'complete', 'payload_in_folder': True, 'machine': 'gabia', 'env': 'y'}}
out['A_selection'] = {'operator saw #2 (gabia) result, liked it → started #1 with a forbidden env': merge_unit('U', ledger, like_gabia, PRE),
                      'operator saw #2 (gabia) result, disliked it → ran #1 normally': merge_unit('U', ledger, like_kgy, PRE)}

# B — dead end: no-op_P0 #1 completes in env E_B (e.g. a thread env var differs in a new shell); #2 re-run in E_A.
ledger = [{'id': 'N#1', 'unit': 'noop_P0'}, {'id': 'N#2', 'unit': 'noop_P0'}]
f = {'N#1': {'end': 'complete', 'payload_in_folder': True, 'machine': 'kgy', 'env': 'E_B'},
     'N#2': {'end': 'complete', 'payload_in_folder': True, 'machine': 'kgy', 'env': 'E_A'}}
out['B_noop_env_dead_end'] = {'after #1 only': merge_unit('noop_P0', ledger[:1], {'N#1': f['N#1']}, PRE, 'P0'),
                              'after correct re-run #2': merge_unit('noop_P0', ledger, f, PRE, 'P0')}
f2 = {'M#1': {'end': 'complete', 'payload_in_folder': True, 'machine': 'Kgy', 'env': 'x'},
      'M#2': {'end': 'complete', 'payload_in_folder': True, 'machine': 'kgy', 'env': 'x'}}
out['B2_machine_typo_dead_end'] = merge_unit('U', [{'id': 'M#1', 'unit': 'U'}, {'id': 'M#2', 'unit': 'U'}], f2, PRE)

# C — folder-less entry: #1 launched with a reused --out → stage_predict returns 3 BEFORE writing anything (OUTDIR_NOT_EMPTY)
ledger = [{'id': 'C#1', 'unit': 'U'}, {'id': 'C#2', 'unit': 'U'}]
f = {'C#2': {'end': 'complete', 'payload_in_folder': True, 'machine': 'kgy', 'env': 'x'}}
out['C_folderless_dead_end'] = merge_unit('U', ledger, f, PRE)

# D — out-of-folder payload: corner run CG unconverged → runner --check-arm rejects → payload left in $KIT/run_*/ → rc 1 → RUNNER_RC
ledger = [{'id': 'D#1', 'unit': 'U'}, {'id': 'D#2', 'unit': 'U'}]
f = {'D#1': {'end': 'stop', 'payload_in_folder': False, 'payload_in_kit_dir': True, 'runner_stop': 'RUNNER_RC', 'machine': 'kgy', 'env': 'x'},
     'D#2': {'end': 'complete', 'payload_in_folder': True, 'machine': 'gabia', 'env': 'y'}}
out['D_unconverged_payload_outside_folder'] = {'if RUNNER_RC ∈ pre-result list (Q4 불수렴 = 결과 뒤 contradicted)': merge_unit('U', ledger, f, PRE),
                                               'if RUNNER_RC ∉ list (then every OOM kill is post-result too)': merge_unit('U', ledger, f, PRE_NO_RC)}
print(json.dumps(out, ensure_ascii=False, indent=1))
