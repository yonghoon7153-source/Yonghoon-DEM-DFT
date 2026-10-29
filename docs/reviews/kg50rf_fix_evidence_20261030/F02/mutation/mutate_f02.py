"""KG50R-F02 변이 시험 — 고친 도구 사본에서 새 관문을 하나씩 끄고 RB 묶음 (--only RB) 을 돌린다.

  python3 -I mutate_f02.py <작업트리> <고친 도구> <출력 폴더> [병렬 수]

변이마다: 원문 조각이 고친 도구에 정확히 한 번 있어야 (아니면 그 변이 = 잘못 만든 변이 · 거부) · 사본 = <출력>/mut/<이름>.sh ·
결과 = RB 묶음 PASS/FAIL 수 · 실패한 시험 ID · 잡힘 (FAIL ≥ 1) / 살아남음.  기대 (expect) 는 사람이 읽는 표지일 뿐 판정에 안 쓴다.
"""
import concurrent.futures as cf
import os
import re
import subprocess
import sys

WT, FIXED, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
NPAR = int(sys.argv[4]) if len(sys.argv) > 4 else 4
TEST = os.path.join(WT, 'scripts', 'test_resume_ckpt.py')
src = open(FIXED, encoding='utf-8').read()

MUT = [
    # (이름, 원문 조각, 바꿀 글, 기대)
    ('M01_shebang', "    if not L or L[0] != '#!/bin/bash':\n", "    if False:\n", 'RB22'),
    ('M02_sbatch_after_cmd', "            if ph:\n                bad(i, s, '#SBATCH 줄이 명령 줄 뒤",
     "            if False:\n                bad(i, s, '#SBATCH 줄이 명령 줄 뒤", 'RB12'),
    ('M03_sbatch_unknown_key', "            if key is None:\n                bad(i, s, '작업 수",
     "            if key is None:\n                continue\n                bad(i, s, '작업 수", 'RB10'),
    ('M04_sbatch_dup_key', "            if key in sb:\n                bad(i, s, '#SBATCH %s 가 두 번' % kn)\n                continue\n",
     "            if key in sb:\n                continue\n", 'RB11'),
    ('M05a_jobname_value', "{'--job-name=': '%s_%s' % (C, SFX), '--output=':", "{'--job-name=': v, '--output=':", 'RB17'),
    ('M05b_output_value', "'--output=': 'logs/output_%s_%s_%%j.out' % (C, SFX), '-n ': NP}", "'--output=': v, '-n ': NP}", 'RB18'),
    ('M05c_n_value', "'-n ': NP}.get(key)", "'-n ': v}.get(key)", 'RB28 RB30 (sed 를 정해진 꼴만 고치게 바꾼 뒤 닿음)'),
    ('M06_token_value', "            elif want is None and not TOK.fullmatch(v):", "            elif False:", 'RB20'),
    ('M07_env_after_cd', "            if ph >= 2:\n                bad(i, s, '환경 줄이 cd 뒤 (cd 앞에만)')\n            else:\n                ph = 1\n",
     "            if False:\n                pass\n            else:\n                ph = max(ph, 1)\n", 'RB13'),
    ('M08_cd_count', "            if ncd > 1:\n                bad(i, s, 'cd 가 두 번 (하나만)')\n            elif",
     "            if False:\n                pass\n            elif", 'RB9b'),
    ('M09_cd_safe_path', "            elif not safe_abs(s[3:]):", "            elif False:", 'RB14'),
    ('M10_cd_realpath', "            elif os.path.realpath(s[3:]) != WR:", "            elif False:", 'RB3'),
    ('M11_mpirun_count', "            if nmp > 1:\n                bad(i, s, 'MPI 실행 줄이 두 번 (하나만)')\n            elif ph != 2:",
     "            if False:\n                pass\n            elif ph != 2:", 'RB5'),
    ('M12_mpirun_before_cd', "            elif ph != 2:\n                bad(i, s, 'MPI 실행 줄이 cd 앞 (cd 다음에만)')",
     "            elif False:\n                pass", 'RB15'),
    ('M13_comment_line', "        if s.startswith('#'):\n            bad(i, s, '주석 줄 (#!/bin/bash · #SBATCH 말고는 안 받는다)')",
     "        if s.startswith('#'):\n            pass", 'RB4b'),
    ('M14_mpirun_any_in', "        if s == mpok:", "        if s.startswith(mpre) and not set(s) & META:", 'RB1 RB2'),
    ('M15_other_command', "        else:\n            bad(i, s, '허용 목록에 없는 명령 줄 (빈 줄 · 환경 줄 · cd · mpirun 한 줄만)')",
     "        else:\n            pass", 'RB6'),
    ('M16_mpirun_meta_msg', "            if set(s) & META:\n                bad(i, s, '셸 연결 · 치환 · 리디렉션 글자가 든 MPI 실행 줄')",
     "            if False:\n                pass", 'RB7a RB7b (문구 · 거부는 다른 문구로 남음)'),
    ('M16b_meta_msg', "        elif set(s) & META:\n            bad(i, s, '셸 연결 · 치환 · 리디렉션 글자 (;",
     "        elif False:\n            bad(i, s, '셸 연결 · 치환 · 리디렉션 글자 (;", '없음 (문구만 · 그 줄은 아래 "허용 목록에 없는 명령 줄" 로 거부)'),
    ('M17_required_keys', "        if need and key not in sb:", "        if False:", 'RB23'),
    ('M18_cd_missing', "    if not ncd:\n        pr.append('cd 줄 없음')", "    if False:\n        pr.append('cd 줄 없음')", 'RB8 (문구 · cd 앞 거부는 남음)'),
    ('M19_mpirun_missing', "    if not nmp:", "    if False:", 'RB25'),
    ('M20_cr', "(('\\r', 'CR 글자 (윈도 줄 끝)'), ('\\x00', 'NUL 글자'))", "(('\\x00', 'NUL 글자'),)", 'RB16 (문구)'),
    ('M21_nul', "(('\\r', 'CR 글자 (윈도 줄 끝)'), ('\\x00', 'NUL 글자'))", "(('\\r', 'CR 글자 (윈도 줄 끝)'),)", 'RB26'),
    ('M22_utf8', "        txt = raw.decode('utf-8')\n", "        txt = raw.decode('utf-8', 'replace')\n", 'RB27 (문구)'),
    ('M23_np_valid', "    if not re.fullmatch(r'[1-9][0-9]{0,5}', NP):", "    if False:", 'RB21'),
    ('M24_wr_safe', "    elif not safe_abs(WR):", "    elif False:", 'RB19'),
    ('M25_wr_consistent', "    if not WR or not os.path.isdir(WR) or os.path.realpath(W) != WR:", "    if False:",
     '없음 (WR = pwd -P 라 닿지 않음)'),
    ('M26_deck_path_safe', "        if WR and safe_abs(WR) and not safe_abs(ab[nm]):", "        if False:", 'RB24'),
    ('M27_receipt_two', 'sha256sum "$WR/${D##*/}" "$WR/${RN##*/}" "$WR/${TD##*/}" "$WR/${TR##*/}" "$CKP" > $AD/main_inputs.sha256 2>/dev/null \\\n'
                        '       || [ "$(grep -c . $AD/main_inputs.sha256)" != 5 ]; then',
     'sha256sum "$WR/${D##*/}" "$WR/${RN##*/}" > $AD/main_inputs.sha256 2>/dev/null \\\n'
     '       || [ "$(grep -c . $AD/main_inputs.sha256)" != 2 ]; then', 'RBR1 RBR2 RBR3 RBP1e RBP2e'),
    ('M28_receipt_memory', '      [ -z "$BLK" ] && [ "$(sha256sum < $AD/main_inputs.sha256 2>/dev/null | cut -c1-64)" != "$MIS" ] \\\n',
     '      [ -z "$BLK" ] && false \\\n', 'RBR4 RBR5'),
    ('M29_recheck_off', '      [ -z "$BLK" ] && ! CKO=$(sha256sum -c --quiet $AD/main_inputs.sha256 2>&1) \\\n',
     '      [ -z "$BLK" ] && false \\\n', 'RBR1 RBR2 RBR3'),
    ('M30_gate_ng_off', '  if [ $RCKC = 0 ]; then echo "  · $RCK"; else ng "$(printf \'%s\' "$RCK" | tr \'\\n\' \' \')"; fi',
     '  echo "  · $RCK"', '음성 전부 (단계 표지 · 영수증 단계가 대신 막음)'),
    ('M31_old_derivation', '  RCK=$(runnerck $RN "$C" "$SFX" "$NP" "$W" "$WR" $D $TD $RN $TR 2>&1); RCKC=$?;',
     '  sed -e "s/${C}_$SFX/${C}_${SFX}t/g" -e "s/^#SBATCH --time=.*/#SBATCH --time=01:00:00/" $RN > $TR; '
     'RCK="헬퍼 러너 엄격 대조 통과 (10-30 KG50R-F02) 변이 = 옛 sed 사본"; RCKC=0;', '음성 전부 · RBP b c d'),
    ('M32_in_relative', "'mpirun --oversubscribe --bind-to none -np %s lmp_mpi -in \"%s\"' % (NP, deck)]",
     "'mpirun --oversubscribe --bind-to none -np %s lmp_mpi -in \"%s\"' % (NP, os.path.basename(deck))]", 'RBP b c d'),
    ('M33_cd_logical_w', "            f.write(render(C, SFX, NP, WR, info, trial))", "            f.write(render(C, SFX, NP, W, info, trial))",
     'RBP1d (별칭 장면)'),
    ('M34_helper_orig_off', '  [ -f $RN ] && cp -p $RN $AD/helper_run_${C}_$SFX.sh.orig', '  true', 'RBP f'),
    ('M35_identity_off', "            'echo \"LMP_IDENTITY record-only", "            '# echo \"LMP_IDENTITY record-only", 'RBP d f g'),
    ('M36_rm_stale_trial', 'TR=$W/run_${C}_${SFX}t.sh; rm -f $TR; WR=', 'TR=$W/run_${C}_${SFX}t.sh; WR=',
     '없음 (새 루트라 옛 시험 러너가 없음 · 위생만)'),
    ('M39_loose_rewrite', r'sed -i "s/^#SBATCH -n [0-9][0-9]*\$/#SBATCH -n $NP/; s/^mpirun \(--oversubscribe \)\{0,1\}\(--bind-to none \)\{0,1\}-np [0-9][0-9]* lmp_mpi -in /mpirun --oversubscribe --bind-to none -np $NP lmp_mpi -in /" $RN',
     r'sed -i "s/^#SBATCH -n .*/#SBATCH -n $NP/; s/mpirun \(--oversubscribe \)\{0,1\}\(--bind-to none \)\{0,1\}-np [0-9]*/mpirun --oversubscribe --bind-to none -np $NP/" $RN',
     'RB28 RB29 RB30 (옛 -n · -np 고침 = 대조 전에 어긋남을 지움)'),
    ('M38_receipt_write_check', '    if ! sha256sum "$WR/${D##*/}" "$WR/${RN##*/}" "$WR/${TD##*/}" "$WR/${TR##*/}" "$CKP" > $AD/main_inputs.sha256 2>/dev/null \\\n'
                                '       || [ "$(grep -c . $AD/main_inputs.sha256)" != 5 ]; then',
     '    sha256sum "$WR/${D##*/}" "$WR/${RN##*/}" "$WR/${TD##*/}" "$WR/${TR##*/}" "$CKP" > $AD/main_inputs.sha256 2>/dev/null\n'
     '    if false; then', '없음 (러너 관문이 먼저 막아 영수증 쓰기 실패에 닿지 않음 · 겹 방어)'),
]


def build(name, old, new):
    n = src.count(old)
    if n != 1:
        return None, '원문 조각 %d 번 (1 번이어야)' % n
    p = os.path.join(OUT, 'mut', name + '.sh')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(src.replace(old, new))
    return p, ''


def run(item):
    name, old, new, expect = item
    p, err = build(name, old, new)
    if p is None:
        return name, expect, None, err, []
    r = subprocess.run([sys.executable, '-I', TEST, '--only', 'RB', '--script', p], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=1800)
    out = r.stdout.decode('utf-8', 'replace')
    with open(os.path.join(OUT, 'mut', name + '.log'), 'w', encoding='utf-8') as f:
        f.write(out)
    m = re.search(r'(\d+) PASS · (\d+) FAIL', out)
    fails = [re.match(r'FAIL (RB\S+)', l).group(1) for l in out.splitlines() if re.match(r'FAIL (RB\S+)', l)]
    if 'No space left on device' in out:      # 환경 (디스크) 실패가 잡힘처럼 보이지 않게 — 그 변이는 다시 돌린다
        return name, expect, None, '환경 오류 ENOSPC — 다시 돌릴 것', fails
    return name, expect, (int(m.group(1)), int(m.group(2))) if m else None, '' if m else '요약 줄 없음 (rc %d)' % r.returncode, fails


os.makedirs(os.path.join(OUT, 'mut'), exist_ok=True)
rows = []
with cf.ThreadPoolExecutor(NPAR) as ex:
    for res in ex.map(run, MUT):
        rows.append(res)
caught = survived = broken = 0
lines = ['# KG50R-F02 변이 시험 — 고친 도구 %s 의 새 관문을 하나씩 끄고 RB 묶음 (--only RB)' % os.path.basename(FIXED),
         '# 이름 | 결과 | RB PASS/FAIL | 실패한 시험 | 기대 (표지만)']
for name, expect, pf, err, fails in rows:
    if pf is None:
        broken += 1
        verdict = '변이 못 만듦/못 돎 (%s)' % err
    elif pf[1] > 0:
        caught += 1
        verdict = '잡힘'
    else:
        survived += 1
        verdict = '살아남음'
    lines.append('%s | %s | %s | %s | %s' % (name, verdict, '%d/%d' % pf if pf else '-', ' '.join(sorted(set(fails))) or '-', expect))
lines.append('# 합계: 변이 %d · 잡힘 %d · 살아남음 %d · 못 만듦 %d' % (len(rows), caught, survived, broken))
txt = '\n'.join(lines) + '\n'
with open(os.path.join(OUT, 'mutation_F02.txt'), 'w', encoding='utf-8') as f:
    f.write(txt)
print(txt)
