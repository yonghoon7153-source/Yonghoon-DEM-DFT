import mutate, sys, json
mutate.MUTS = [
    ('M15_success_writes_ids', "    return [{k: a[k] for k in ARM_PUBLIC} for a in arms_]\n\n\ndef arm_file_prefix", "    return [{k: a[k] for k in ARM_FILE_ID_KEYS} for a in arms_]\n\n\ndef arm_file_prefix"),
    ('M16_idx_self_ref', "    idx = arm_indices(rec)\n    if len(ar) != len(idx):", "    idx = sorted(a['index'] for a in ar if type(a['index']) is int)\n    if len(ar) != len(idx):"),
    ('M17_rec_ignored_kit', "    pref = arm_file_prefix(kit)\n    for j, (a, i) in enumerate(zip(ar, idx)):", "    pref = 'p2_'\n    for j, (a, i) in enumerate(zip(ar, idx)):"),
]
mutate.main()
