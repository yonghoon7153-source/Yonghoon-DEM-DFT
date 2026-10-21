#!/bin/bash
# recheck 10-21: readback meta binding when the D2 deck is compared under another file name (same folder, untouched generator meta)
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a876633abb3bfa519
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
T="$H/meta_rename"
rm -rf "$T"; mkdir -p "$T/uu" "$T/cc"
cp "$H/decks/recheck/GMuu_ref20_lab/in.mixer" "$H/decks/recheck/GMuu_ref20_lab/deck_meta.json" "$T/uu/"
cp "$H/decks/recheck/GMcc_ref20_lab/in.mixer" "$H/decks/recheck/GMcc_ref20_lab/deck_meta.json" "$T/cc/"
# M16-like meta tamper on cc (deck_file stays "in.mixer")
python3 -I -B -c "
import json,sys
p=sys.argv[1]; m=json.load(open(p,encoding='utf-8')); m['adhesion_rule']['bo_se']=0.21244; json.dump(m,open(p,'w'),ensure_ascii=False)
" "$T/cc/deck_meta.json"
cp "$T/uu/in.mixer" "$T/uu/uu.mixer"; cp "$T/cc/in.mixer" "$T/cc/cc.mixer"
export PYTHONDONTWRITEBYTECODE=1
python3 -I -B "$W/scripts/mixer_deck_readback.py" --table GM "$T/uu/in.mixer" "$T/cc/in.mixer" --json "$T/a.json" > "$T/a.out" 2>&1
echo "as in.mixer (tampered meta bound): rc=$? :: $(tail -1 "$T/a.out")"
python3 -I -B "$W/scripts/mixer_deck_readback.py" --table GM "$T/uu/uu.mixer" "$T/cc/cc.mixer" --json "$T/b.json" > "$T/b.out" 2>&1
echo "renamed copies (same folder, same tampered meta): rc=$? :: $(tail -1 "$T/b.out")"
python3 -I -B -c "
import json,sys
J=json.load(open(sys.argv[1],encoding='utf-8'))
for d in J.get('decks',[]): print('  deck', d.get('label'), 'meta_bound', d.get('meta_bound'))
" "$T/b.json"
