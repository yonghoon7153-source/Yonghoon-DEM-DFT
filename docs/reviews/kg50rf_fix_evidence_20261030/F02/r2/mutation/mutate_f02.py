"""KG50R-F02 변이 시험 — 고친 도구 사본에서 관문을 하나씩 끄고 RB 묶음 (--only RB) 을 돌린다.

  python3 -I mutate_f02.py <작업트리> <고친 도구> <출력 폴더> [병렬 수]

변이마다: 원문 조각이 고친 도구에 정확히 한 번 있어야 (아니면 그 변이 = 잘못 만든 변이 · 거부) · 사본 = <출력>/mut/<이름>.sh ·
결과 = RB 묶음 PASS/FAIL 수 · 실패한 시험 ID · 잡힘 (FAIL ≥ 1) / 살아남음.  기대 (expect) 는 사람이 읽는 표지일 뿐 판정에 안 쓴다.
묶음: M = 1 판 변이 41 (10-30 · 원문 조각을 고친 판 글에 맞춤) · N = 사전 공격 수정 변이 (PA-01–09 · 환경 줄) ·
V = 독립 사전 공격 리뷰어 변이 28 (mutate_rev.py 의 E1–E3 · R1–R25 · 원문 조각만 고친 판 글로 옮김 — 바꿀 글은 그대로 뜻).
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

RENDER_IN = "'command mpirun --oversubscribe --bind-to none -np %s lmp_mpi -in \"%s\"' % (NP, deck)]"
RECEIPT5 = ('sha256sum "$WR/${D##*/}" "$WR/${RN##*/}" "$WR/${TD##*/}" "$WR/${TR##*/}" "$CKP" > $AD/main_inputs.sha256 2>/dev/null \\\n'
            '       || [ "$(grep -c . $AD/main_inputs.sha256)" != 5 ]; then')
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
    ('M05c_n_value', "'-n ': NP}.get(key)", "'-n ': v}.get(key)", 'RB28 RB30'),
    ('M06_token_value', "            elif want is None and not TOK.fullmatch(v):", "            elif False:", 'RB20 RB34'),
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
     "            if False:\n                pass", 'RB7a RB7b'),
    ('M16b_meta_msg', "        elif set(s) & META:\n            bad(i, s, '셸 연결 · 치환 · 리디렉션 글자 (;",
     "        elif False:\n            bad(i, s, '셸 연결 · 치환 · 리디렉션 글자 (;", 'RB37 (10-30 더함 · 1 판에서 살아남음)'),
    ('M17_required_keys', "        if need and key not in sb:", "        if False:", 'RB23 RB33'),
    ('M18_cd_missing', "    if not ncd:\n        pr.append('cd 줄 없음')", "    if False:\n        pr.append('cd 줄 없음')", 'RB8'),
    ('M19_mpirun_missing', "    if not nmp:", "    if False:", 'RB25'),
    ('M20_cr', "(('\\r', 'CR 글자 (윈도 줄 끝)'), ('\\x00', 'NUL 글자'))", "(('\\x00', 'NUL 글자'),)", 'RB16'),
    ('M21_nul', "(('\\r', 'CR 글자 (윈도 줄 끝)'), ('\\x00', 'NUL 글자'))", "(('\\r', 'CR 글자 (윈도 줄 끝)'),)", 'RB26'),
    ('M22_utf8', "        txt = raw.decode('utf-8')\n", "        txt = raw.decode('utf-8', 'replace')\n", 'RB27'),
    ('M23_np_valid', "    if not re.fullmatch(r'[1-9][0-9]{0,5}', NP):", "    if False:", 'RBU5 (도구 흐름은 -n 시작 거부가 먼저)'),
    ('M24_wr_safe', "    elif not safe_abs(WR):", "    elif False:", 'RB19'),
    ('M25_wr_consistent', "    if not WR or not os.path.isdir(WR) or os.path.realpath(W) != WR:", "    if False:", 'RBU2 (1 판에서 살아남음)'),
    ('M26_deck_path_safe', "        if WR and safe_abs(WR) and not safe_abs(ab[nm]):", "        if False:", 'RBU6 (도구 흐름은 -x 시작 거부가 먼저)'),
    ('M27_receipt_two', RECEIPT5,
     'sha256sum "$WR/${D##*/}" "$WR/${RN##*/}" > $AD/main_inputs.sha256 2>/dev/null \\\n'
     '       || [ "$(grep -c . $AD/main_inputs.sha256)" != 2 ]; then', 'RBR · RBP'),
    ('M28_receipt_memory', '      [ -z "$BLK" ] && [ "$(sha256sum < $AD/main_inputs.sha256 2>/dev/null | cut -c1-64)" != "$MIS" ] \\\n',
     '      [ -z "$BLK" ] && false \\\n', 'RBR4 RBR5'),
    ('M29_recheck_off', '      [ -z "$BLK" ] && ! CKO=$(sha256sum -c --quiet $AD/main_inputs.sha256 2>&1) \\\n',
     '      [ -z "$BLK" ] && false \\\n', 'RBR1 RBR2 RBR3'),
    ('M30_gate_ng_off', '  if [ $RCKC = 0 ]; then echo "  · $RCK"; else ng "$(printf \'%s\' "$RCK" | tr \'\\n\' \' \')"; fi',
     '  echo "  · $RCK"', '음성 전부'),
    ('M31_old_derivation', '  RCK=$(runnerck $RN "$C" "$SFX" "$NP" "$W" "$WR" $D $TD $RN $TR "$CKP" 2>&1); RCKC=$?;',
     '  sed -e "s/${C}_$SFX/${C}_${SFX}t/g" -e "s/^#SBATCH --time=.*/#SBATCH --time=01:00:00/" $RN > $TR; '
     'RCK="헬퍼 러너 엄격 대조 통과 (10-30 KG50R-F02) 변이 = 옛 sed 사본"; RCKC=0;', '음성 전부 · RBP'),
    ('M32_in_relative', RENDER_IN, RENDER_IN.replace('% (NP, deck)]', '% (NP, os.path.basename(deck))]'), 'RBP b c d'),
    ('M33_cd_logical_w', "            f.write(render(C, SFX, NP, WR, info, trial))", "            f.write(render(C, SFX, NP, W, info, trial))",
     'RBP1 (별칭 장면)'),
    ('M34_helper_orig_off', '  [ -f $RN ] && cp -p $RN $AD/helper_run_${C}_$SFX.sh.orig', '  true', 'RBP f'),
    ('M35_identity_off', "            'echo \"LMP_IDENTITY (10-30", "            '# echo \"LMP_IDENTITY (10-30", 'RBP · G0 신원 관문'),
    ('M36_rm_stale_trial', 'TR=$W/run_${C}_${SFX}t.sh; rm -f $TR; WR=', 'TR=$W/run_${C}_${SFX}t.sh; WR=', 'RB36b (1 판에서 살아남음)'),
    ('M39_loose_rewrite', r'sed -i "s/^#SBATCH -n [0-9][0-9]*\$/#SBATCH -n $NP/; s/^mpirun \(--oversubscribe \)\{0,1\}\(--bind-to none \)\{0,1\}-np [0-9][0-9]* lmp_mpi -in /mpirun --oversubscribe --bind-to none -np $NP lmp_mpi -in /" $RN',
     r'sed -i "s/^#SBATCH -n .*/#SBATCH -n $NP/; s/mpirun \(--oversubscribe \)\{0,1\}\(--bind-to none \)\{0,1\}-np [0-9]*/mpirun --oversubscribe --bind-to none -np $NP/" $RN',
     'RB28 RB29 RB30'),
    ('M38_receipt_write_check', '    if ! ' + RECEIPT5, '    sha256sum "$WR/${D##*/}" "$WR/${RN##*/}" "$WR/${TD##*/}" "$WR/${TR##*/}" "$CKP" > $AD/main_inputs.sha256 2>/dev/null\n'
     '    if false; then', '없음 (겹 방어 · runnerck 가 다섯 중 덱 셋을 이미 읽고 러너 둘을 썼다)'),
    # ── N: 10-30 사전 공격 수정 (PA-01–09 · 환경 줄) ──
    ('N40_np_startup', '[[ "$NP" =~ ^[1-9][0-9]{0,5}$ ]] || { echo "⛔ -n $NP', 'true || { echo "⛔ -n $NP', 'RB21 RB49 RB49b'),
    ('N41_np_startup_loose', '[[ "$NP" =~ ^[1-9][0-9]{0,5}$ ]] || { echo', '[[ "$NP" =~ ^[0-9]+ ]] || { echo', 'RB21 RB49 RB49b'),
    ('N42_sfx_startup', '[[ "$SFX" =~ ^[A-Za-z0-9_]+$ ]] || { echo "⛔ -x $SFX', 'true || { echo "⛔ -x $SFX', 'RB24 RB50'),
    ('N43_sfx_startup_loose', '[[ "$SFX" =~ ^[A-Za-z0-9_]+$ ]] || { echo', '[[ "$SFX" =~ ^[^[:space:]]+$ ]] || { echo', 'RB24 RB50'),
    ('N44_symlink_off', '  [ -L "$S" ] && { rej "멈춘 폴더"', '  false && { rej "멈춘 폴더"', 'RB48'),
    ('N45_envlike_off', '        if ENVLIKE.match(s):', '        if False:', 'RB32'),
    ('N46_conda_dot', 'conda activate [A-Za-z0-9_][A-Za-z0-9_.-]*|', 'conda activate [A-Za-z0-9_.-]+|', 'RB32h RB32i RB32j'),
    ('N47_tok_comma', "TOK = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.:+-]*(?:,[A-Za-z0-9][A-Za-z0-9_.:+-]*)*')",
     "TOK = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.:,+-]*')", 'RB34'),
    ('N48_ckp_safe_off', '    if not safe_abs(CK):', '    if False:', 'RBU4'),
    ('N49_render_no_refuse', '- mpirun not started"; exit 1; }\'', '- mpirun not started"; true; }\'', 'RB40 RB41 RB42 RB43 · RBP d'),
    # 바꿀 글의 "${ks}" · "${ds}" 중괄호 = 꼭 (첫 판 "$ks%s" 는 bash 가 $ks<16진> 를 정의 안 된 변수 하나로 읽어 대조가 늘 실패 = 끄지 못한 변이였다)
    ('N50_render_no_ks', '[ "$ds" = "%s" ] && [ "$ks" = "%s" ] ||', '[ "$ds" = "%s" ] && [ -n "${ks}%s" ] ||', 'RB42 · RBP d'),
    ('N51_render_no_ds', '[ "$ds" = "%s" ] && [ "$ks" = "%s" ] ||', '[ -n "${ds}%s" ] && [ "$ks" = "%s" ] ||', 'RB40 RB41 RB43 · RBP d'),
    ('N52_render_cd_guard', "out += ['', 'cd \"%s\" || exit 1' % WR,", "out += ['', 'cd \"%s\"' % WR,", 'RB46 · RBP d'),
    ('N53_render_command', RENDER_IN, RENDER_IN.replace("'command mpirun ", "'mpirun "), 'RB45 · RBP d'),
    ('N54_g0_no_identity', '[ "$T" != /dev/null ] && [ $GI = 1 ] && G0=1', '[ "$T" != /dev/null ] && G0=1', 'RB44 RB44b'),
    ('N55_gi_path', '  elif [ "${BASH_REMATCH[1]}" != "$TQP" ]; then', '  elif false; then', 'RB44b'),
    ('N56_gi_sha', '  elif [ "${BASH_REMATCH[2]}" != "$TQS" ]; then', '  elif false; then', 'RB40 RB41'),
    ('N57_gi_count', '  if [ "$NLID" != 1 ]; then', '  if false; then', 'RB44'),
    ('N58_error_count_old', "E=$(grep -av '^LMP_IDENTITY ' $T | grep -ac ERROR)", 'E=$(grep -ac ERROR $T)', 'RB47'),
    ('N59_tqs_check', '    { [[ "$TQS" =~ ^[0-9a-f]{64}$ ]] && [ "${TQL:64}" = "  $TQP" ]; } || {', '    true || {',
     '없음 (겹 방어 · GNU sha256sum 셋째 줄 = 시험 덱 · 안전한 경로)'),
    ('N60_tmp_cleanup_off', '            if os.path.lexists(tmp):\n                os.remove(tmp)', '            if False:\n                os.remove(tmp)', 'RB35'),
    ('N61_isfile_off', "                if not os.path.isfile(p):\n                    raise OSError(0, '보통 파일이 아니거나 없음')\n", '',
     '없음 (없는 파일 · 폴더는 열 때 같은 OSError · FIFO 만 다름 = 막힘 — 시험 안 함)'),
    # ── V: 독립 사전 공격 리뷰어 변이 (mutate_rev.py · 도구 5f4ffb46 기준 → 원문 조각만 고친 판 글로 옮김) ──
    ('VE1_ENVL_export_any', "export (?:OMP|MKL|OPENBLAS|NUMEXPR)_NUM_THREADS=1')", "export [A-Za-z_]+=[^ ]+')", 'RB32b RB32c RB32d'),
    ('VE2_ENVL_conda_any', "conda activate [A-Za-z0-9_][A-Za-z0-9_.-]*|", "conda activate .+|", 'RB32g RB32h RB32i RB32j'),
    ('VE3_ENVL_source_any', "source ~/\\.bashrc|", "source \\S+|", 'RB32e'),
    ('VR1_cd_realpath_dropped', "            elif os.path.realpath(s[3:]) != WR:\n                bad(i, s, 'cd 실제 경로 [%s] ≠ 작업 폴더 실제 경로 [%s]' % (os.path.realpath(s[3:]), WR))\n", "", 'RB3'),
    ('VR2_mpirun_prefix', "        if s == mpok:", "        if s.startswith(mpre):", 'RB1 RB2'),
    ('VR3_realpath_W_dropped', "if not WR or not os.path.isdir(WR) or os.path.realpath(W) != WR:", "if not WR or not os.path.isdir(WR):", 'RBU2'),
    ('VR4_render_in_basename', "lmp_mpi -in \"%s\"' % (NP, deck)]", "lmp_mpi -in \"%s\"' % (NP, os.path.basename(deck))]", 'RBP'),
    ('VR5_render_cd_unquoted', "out += ['', 'cd \"%s\" || exit 1' % WR,", "out += ['', 'cd %s || exit 1' % WR,", 'RBP d'),
    ('VR6_render_no_cd', "out += ['', 'cd \"%s\" || exit 1' % WR,", "out += ['',", 'RBP'),
    ('VR7_runnerck_rc2_pass', 'if [ $RCKC = 0 ]; then echo "  · $RCK"; else ng', 'if [ $RCKC != 1 ]; then echo "  · $RCK"; else ng', 'RB35'),
    ('VR8_no_rm_TR', 'TR=$W/run_${C}_${SFX}t.sh; rm -f $TR; WR=', 'TR=$W/run_${C}_${SFX}t.sh; WR=', 'RB36b'),
    ('VR9_receipt_logical_D', 'sha256sum "$WR/${D##*/}"', 'sha256sum "$D"', 'RBP e'),
    ('VR10_receipt_count_dropped', '       || [ "$(grep -c . $AD/main_inputs.sha256)" != 5 ]; then', '       ; then', '없음 (GNU sha256sum = 성공이면 파일마다 한 줄)'),
    ('VR11_sed_n_permissive', 's/^#SBATCH -n [0-9][0-9]*\\$/#SBATCH -n $NP/;', 's/^#SBATCH -n .*/#SBATCH -n $NP/;', 'RB28'),
    ('VR12_CR_NUL_precheck', "    if fp:\n        return P + fp, None\n", "", 'RB26'),
    ('VR13_env_after_cd', "            if ph >= 2:\n                bad(i, s, '환경 줄이 cd 뒤 (cd 앞에만)')\n            else:\n                ph = 1\n                env.append(s)\n",
     "            ph = max(ph, 1)\n            env.append(s)\n", 'RB13'),
    ('VR14_premain_receipt_sha', '      [ -z "$BLK" ] && [ "$(sha256sum < $AD/main_inputs.sha256 2>/dev/null | cut -c1-64)" != "$MIS" ] \\\n        && BLK=',
     '      [ -z "$BLK" ] && false \\\n        && BLK=', 'RBR4 RBR5'),
    ('VR15_premain_recheck', '[ -z "$BLK" ] && ! CKO=$(sha256sum -c --quiet $AD/main_inputs.sha256 2>&1)', '[ -z "$BLK" ] && ! CKO=$(true)', 'RBR1 RBR2 RBR3'),
    ('VR16_trial_uses_main_deck', "    k = '시험 덱' if trial else '재개 덱'", "    k = '재개 덱'", 'RBP'),
    ('VR17_output_optional', "('--output=', 1)", "('--output=', 0)", 'RB33'),
    ('VR18_jobname_want_dropped', "want = {'--job-name=': '%s_%s' % (C, SFX), '--output='", "want = {'--output='", 'RB17'),
    ('VR19_comment_skipped', "        if s.startswith('#'):\n            bad(i, s, '주석 줄 (#!/bin/bash · #SBATCH 말고는 안 받는다)')\n        elif",
     "        if s.startswith('#'):\n            pass\n        elif", 'RB4 RB4b'),
    ('VR20_receipt_no_ckpt', '"$WR/${TR##*/}" "$CKP" > $AD/main_inputs.sha256', '"$WR/${TR##*/}" > $AD/main_inputs.sha256', 'RBP · RBR'),
    ('VR21_render_identity_dropped', "            'echo \"LMP_IDENTITY (10-30", "            '' and 'echo \"LMP_IDENTITY (10-30", 'RBP · G0 신원 관문'),
    ('VR22_sbatch_after_cmd', "            if ph:\n                bad(i, s, '#SBATCH 줄이 명령 줄 뒤 (SLURM 은 첫 명령 뒤 #SBATCH 를 안 읽는다)')\n                continue\n", "", 'RB12'),
    ('VR23_two_cd', "            if ncd > 1:\n                bad(i, s, 'cd 가 두 번 (하나만)')\n            elif not safe_abs", "            if not safe_abs", 'RB9 RB9b'),
    ('VR24_cd_safe_abs_dropped', "            elif not safe_abs(s[3:]):\n                bad(i, s, 'cd 경로가 안전한 절대 경로가 아님 (A-Z a-z 0-9 _ . + - / 만 · . .. 마디 · 따옴표 · $ · ~ · 공백 없음)')\n", "", 'RB14'),
    ('VR25_WR_logical_pwd', 'WR=$(cd -P "$W" 2>/dev/null && pwd -P)', 'WR=$(cd "$W" 2>/dev/null && pwd)', 'RBP1'),
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
        return name, expect, None, err, [], False
    r = subprocess.run([sys.executable, '-I', TEST, '--only', 'RB', '--script', p], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=1800)
    out = r.stdout.decode('utf-8', 'replace')
    with open(os.path.join(OUT, 'mut', name + '.log'), 'w', encoding='utf-8') as f:
        f.write(out)
    m = re.search(r'(\d+) PASS · (\d+) FAIL', out)
    fails = [re.match(r'FAIL (RB\S+)', l).group(1) for l in out.splitlines() if re.match(r'FAIL (RB\S+)', l)]
    tb = 'Traceback (most recent call last)' in out
    if 'No space left on device' in out:      # 환경 (디스크) 실패가 잡힘처럼 보이지 않게 — 그 변이는 다시 돌린다
        return name, expect, None, '환경 오류 ENOSPC — 다시 돌릴 것', fails, tb
    return name, expect, (int(m.group(1)), int(m.group(2))) if m else None, '' if m else '요약 줄 없음 (rc %d)' % r.returncode, fails, tb


os.makedirs(os.path.join(OUT, 'mut'), exist_ok=True)
rows = []
with cf.ThreadPoolExecutor(NPAR) as ex:
    for res in ex.map(run, MUT):
        rows.append(res)
caught = survived = broken = tbs = 0
lines = ['# KG50R-F02 변이 시험 — 고친 도구 %s 의 관문을 하나씩 끄고 RB 묶음 (--only RB)' % os.path.basename(FIXED),
         '# 이름 | 결과 | RB PASS/FAIL | 실패한 시험 | 기대 (표지만)']
for name, expect, pf, err, fails, tb in rows:
    tbs += tb
    if pf is None:
        broken += 1
        verdict = '변이 못 만듦/못 돎 (%s)' % err
    elif pf[1] > 0:
        caught += 1
        verdict = '잡힘'
    else:
        survived += 1
        verdict = '살아남음'
    lines.append('%s | %s | %s | %s | %s' % (name, verdict + (' · 시험 하네스 예외' if tb else ''), '%d/%d' % pf if pf else '-',
                                             ' '.join(sorted(set(fails))) or '-', expect))
for grp in ('M', 'N', 'V'):
    g = [x for x in rows if x[0].startswith(grp)]
    lines.append('# 묶음 %s: 변이 %d · 잡힘 %d · 살아남음 %d · 못 만듦 %d' % (
        grp, len(g), sum(1 for x in g if x[2] and x[2][1] > 0), sum(1 for x in g if x[2] and x[2][1] == 0), sum(1 for x in g if x[2] is None)))
lines.append('# 합계: 변이 %d · 잡힘 %d · 살아남음 %d · 못 만듦 %d · 시험 하네스 예외 (Traceback) 든 로그 %d' % (len(rows), caught, survived, broken, tbs))
txt = '\n'.join(lines) + '\n'
with open(os.path.join(OUT, 'mutation_F02.txt'), 'w', encoding='utf-8') as f:
    f.write(txt)
print(txt)
