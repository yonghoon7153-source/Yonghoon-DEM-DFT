#!/usr/bin/env python3
"""Compare D3 reserved IDs against v1 and inspect D1/D12 source rows only."""
import argparse
import hashlib
import json
import pathlib
import re


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', required=True, type=pathlib.Path)
    ap.add_argument('--draft', required=True, type=pathlib.Path)
    args = ap.parse_args()
    sources = {
        'v1': args.repo / 'docs/reviews/mixer_d3_se_flowability_anchor_design_20261015.md',
        'D1_D12': args.repo / 'docs/mixer_paper_pipeline_draft_20261013.md',
        'revision': args.draft,
    }
    texts = {key: path.read_text() for key, path in sources.items()}

    def row(key, phrase):
        rows = [(n, text) for n, text in enumerate(texts[key].splitlines(), 1) if phrase in text]
        if len(rows) != 1:
            raise ValueError((key, phrase, 'expected one row', len(rows)))
        line, text = rows[0]
        return {'line': line, 'text': text}

    excerpts = {
        'v1_seed_reservation': row('v1', '| 시드 |'),
        'v1_new_block_reservation': row('v1', '| 동결 블록 |'),
        'D1': row('D1_D12', '| D1 |'),
        'D12': row('D1_D12', '| D12 |'),
        'existing_D1_decision_record': row('D1_D12', '> ✅ **1저자 10-14'),
        'existing_D12_decision_record': row('D1_D12', '> ✅ **1저자 10-20'),
        'revision_reservation': row('revision', '**시드 역할과 예약:**'),
    }
    old_group = re.search(r'확인 시드 셋 \(([^)]+)\)', excerpts['v1_seed_reservation']['text']).group(1)
    new_group = re.search(r'예약 확인 시드\(([^)]+)\)', excerpts['revision_reservation']['text']).group(1)
    old_ids = [int(x) for x in re.findall(r'[0-9]+', old_group)]
    new_ids = [int(x) for x in re.findall(r'[0-9]+', new_group)]
    checks = {
        'exact_ordered_numeric_ID_match': old_ids == new_ids,
        'three_distinct_reserved_IDs': len(old_ids) == len(set(old_ids)) == 3,
        'v1_excludes_D3_use': 'D3 에 쓰지 않는다' in excerpts['v1_new_block_reservation']['text'],
        'D1_reserves_for_new_block': '미사용 확인 시드 셋은 새 블록으로' in excerpts['D1']['text'],
        'D12_keeps_confirmation_seed_set': '확인 시드 셋 그대로' in excerpts['D12']['text'],
    }
    result = {
        'scope': 'Source-text provenance only; no actual run manifest, seed use, approval, or execution verified',
        'v1_reserved_IDs': old_ids, 'revision_reserved_IDs': new_ids,
        'checks': checks, 'summary': {'passed': sum(checks.values()), 'total': len(checks)},
        'sources': {key: {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                    for key, path in sources.items()},
        'source_excerpts': excerpts,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    raise SystemExit(main())
