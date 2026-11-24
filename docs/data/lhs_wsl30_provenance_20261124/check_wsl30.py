# WSL30 (lhs00_100-129) value-blind provenance check.  Read-only.  Prints counts / booleans / step numbers only:
# no pressure value, no target value, no log or deck text is printed.
#   Q-a  same execution?   banner counts, 'Finished!' count, pressure-line list equal (by hash), log.txt lines in order inside log.liggghts
#   Q-b  current deck = executed deck?  every non-blank line of the deck (and its include files) found verbatim in the log.liggghts echo
#   Q-c  harvested frame inside that run?  cohort harvest step inside both logs' step range · deck / atom sha256 = cohort (area_s2_cohort.tsv)
import bisect, hashlib, os, re, sys
from collections import defaultdict

ROOT = os.path.expanduser(os.environ.get('LHS_ROOT', '~/lhs_local'))
CASES = ['lhs00_%03d' % n for n in range(100, 130)]
# 리포 docs/data/area_s2_cohort.tsv (09-19 봉인) 의 하베스트 step · 덱 sha256 · atom 덤프 sha256
COHORT = {
    "lhs00_100": (3380000, "48e480f14adb78ffc1006db1e8fd58eca62e454bc1b07fcd939995b728a30de6", "14c5251ea9c70ea69807daffa23a307fb80672a8356f9eeb690d7441adf83e5b"),
    "lhs00_101": (2940000, "cd47ca453837893e2069120b80a96ed39017931a364fe7d769998212e27bce4b", "0fba958201786804ea88a073d2d721a20a51bfa45c55e845d120ea605ccf99c1"),
    "lhs00_102": (2300000, "7d295a3b6b64d78f7de94a2b40bb7bd731492a7e7d7d2a143d0abfe6fdf2be65", "3b0899aff15e9fdbcf4cb3b66ed559bb5dc003560d8586f5fa6dc3c49afc626e"),
    "lhs00_103": (2760000, "9f16a146c7a186a15c2ff75666da98914ca3928562f9b4de406dc950e6962bb1", "213959e79c65f1a01d48accb435a5be5ed1399d544ce6309af95d83d3f2b885b"),
    "lhs00_104": (2420000, "f447ba6c4970658a0c66e4f593e0108cb22dfaadd34dfc96a6a82d5b396f60e4", "af3720cf1519548855b04238bc51fc5c15fc8acc7340f8950470cb97d40ab0d5"),
    "lhs00_105": (2430000, "c99803be0cf6a3445cdb61c263312d342fd2c7c41b04c0a5f23f10a5f8a39562", "f011d8269c4bdfb55fe691db760ecc145dd64ed578197e20af7ed19ab04062b0"),
    "lhs00_106": (3630000, "baf3826bf9ceec3004d4358519f9deb4ce1c3417e37bdd35c5cc98a9ba98cd77", "bb689bca41368a77abdf45cb1247bdb97605b02d305e4af12ed60f4246bbc9b6"),
    "lhs00_107": (2000000, "33a5baa10595c85e557670e052cce3d6b6422507dbdb0a3d3dcd9c037d960685", "44394ed1b416dfe91be3be2cecf072fb433a3aa72990d311fd00591191fa007f"),
    "lhs00_108": (2360000, "1be9760586627f362a762cbd12b02a661b63ae59f07e74c7092bddaa97d78ccb", "e2e94296885bf261f1afd451f20a4722abddaff10731eed15002a2adf2c9b692"),
    "lhs00_109": (3800000, "3669f7b3a2b9289f7ca36f0e3ab26d9bc3be84973eb4d2f394c53367e3226031", "e9e77842d353e8b4a7a4f382545aea15b8e22cce823ad8297f70d1312cb4ba95"),
    "lhs00_110": (3020000, "aca27397e569374283876c428e4c16dd5174f0e99a5048b13d1cd82f45ee2ccf", "f8a57ed6fa31d0c4d53f637480cd5763b2368fd74ec438321e9bbfee81264a10"),
    "lhs00_111": (2140000, "6aed58192f3b1ad41c26f1213f39866d8d10761d74bc1fd49dab385458783df9", "0df9caff68865d4e4f77d576996115e58c5397181074541856aa227496b1d308"),
    "lhs00_112": (2120000, "bd4dac3d618563c00834ddddf2ed66450a727d038554623e52cc140b95db9591", "6a3c3e10d7db3b51804278662541f5e949010c75d942774050df3304b4936ef4"),
    "lhs00_113": (2190000, "1aecd6e889d0fb71afa2a943ebd40f296aec2705f03b568e76d57c0e8f418f23", "a3fc89923feb15ec12abf4cca5505f71d53f48a87904d20b3e9a3495299465be"),
    "lhs00_114": (2980000, "8b574f1ebd71eda5ed1c75e5d3f64d3f4418fc63b447ace89031103e9b484e2d", "a26681cbec8e88aeb6005299114f1105febe0b4ecda2d553737271b975228a58"),
    "lhs00_115": (2800000, "3c4d808feb030942c63409794fed8b1d1ecbfd9636ff682fe954a38b325f8720", "b38629d7efb9e5573b85fef56b52923f9d0e7b031fa7c7ae20d3bf1a86dff81c"),
    "lhs00_116": (2990000, "16acee773a885857b9cda9c0b4e5651f98998d20e09871206b15bcaab1d6f66b", "1498f6f30aea11859c680e483b70e5efb6373c48b632aadef603cec748b45f4c"),
    "lhs00_117": (2140000, "7a8ba5b91403cbba495c1a0940bc3897de18a5b42d2991686e8c244696c6154b", "2581c910a0e351a164b2b29fb1d872165bd47a98a9fe7fa3c73ace459b5766b8"),
    "lhs00_118": (3600000, "6aeb8198a19566ba9a7b0aa66feca1cd1996000b1c4757bd1931388604d191d2", "7f66cb0657652e83383898ccb4bb239c90b9cc8d8562d9b5be4110db5b8f8867"),
    "lhs00_119": (2410000, "62cdbe932129e94fadf63086a1b25997c69e9fc26caa869d22e794c03a5160e7", "a5041835a2c87bf6c6fe590287b05d0c77542c80bafa9c4d27d1eacff73abf39"),
    "lhs00_120": (2200000, "1c6b110d5922fd079caf5d6ac4d9f288381cbbad913d1798d06454da79a4c633", "9a60e3c4ca22aff05f49ec71c279f533d6bc81d0867eb1368a236113a06fb216"),
    "lhs00_121": (3390000, "9ab4fc54ec8a08a0bdf283e8ee374abcd2b055f7ecf21cf7c79d0be59ae7434b", "fc21e89f792ef542047a0d062d246e93eaecec62d5e2709733443b8b2037ad2c"),
    "lhs00_122": (2220000, "63891eb480a35f75872febee7f59202c0298d5c6d8a3ec490140a3e4962bd0ea", "13420b536bdd5e7e900335e7946168261a03293407e73d2a3ecd2bc84b515273"),
    "lhs00_123": (2070000, "42b946370ad850cb8992e6af569060e173b342148ad54c6a7b8b8718c8c6263d", "d0368ce7970dd50072549992ed603c6aa9cafb3b19180129763eece6607a847a"),
    "lhs00_124": (2220000, "fceaf300578541312956e1629dc79599afb899e0b331666a75d4ee7bbfdf7516", "080d31c724ae1d3384566cd6be3c2c1840fc802d8c10495615c5f24a5158ac8f"),
    "lhs00_125": (2770000, "0925278cc2d5866949562cbba72cc2463b9626b7a759832a8eb44f1918f56049", "a0bcc435b560c720abb2f50ff77661b01a895ee236d125b3163c3a19e0d067b0"),
    "lhs00_126": (2010000, "0627bb5f421a38bab3547cfe3a65cfc543152dd4016b627ef728d84d918ccc41", "7c1a5c1f5f676f8a78c6c1991710ba64d1bbff7c32b6fe855176ea32c724ef81"),
    "lhs00_127": (2440000, "b92f9e16aa69891873432011dd52893d075ec5a8e224ace03c05b570a20a0e79", "33041ecf81f9b4249f0be2654b9a141880b61336f6955d0561ef22cc32121843"),
    "lhs00_128": (2640000, "00ddd41898fb93164895eb46ad635ffcd95a535f5e1a282a6e4be116886e9d14", "638cb80677a69b0edf4b3f426828964944efe2301e387a2c14f4c6e93c2a0ff2"),
    "lhs00_129": (2910000, "7655bfec1e019bfbe2cf39697e18cfd27bfde090b641030258562c4b6e395d64", "75775d13e54b64c3c1bd3e6f942ae73c619cebfff65bfb101b947ef322cdcbf2"),
}
PRESS = re.compile(r"^\s*Current Pressure:\s*(\S+)\s*MPa\s*\(Target:\s*(\S+)\s*\)\s*$")   # same pattern as the sealed scanner
BANNER = re.compile(r"^\s*LIGGGHTS \(Version")
FIN = re.compile(r"Finished!")
STEPLINE = re.compile(r"^\s*(\d+)\s+\S")
CMD = re.compile(r"^\s*(variable|fix|unfix|run|if|jump|label|print|thermo|thermo_style|thermo_modify|dump|undump|dump_modify|"
                 r"include|region|group|compute|uncompute|write_restart|read_restart|restart|neighbor|neigh_modify|timestep|"
                 r"communicate|newton|units|atom_style|atom_modify|boundary|processors|create_box|create_atoms|pair_style|"
                 r"pair_coeff|shell|next|clear|log|echo|set|velocity|delete_atoms|mass|lattice|displace_atoms|"
                 r"soft_particles|hard_particles|modify_timing|reset_timestep)\b")


def lines_of(path):
    with open(path, encoding='utf-8', errors='surrogateescape') as f:
        return [ln.rstrip('\r\n').rstrip() for ln in f.read().splitlines()]


def h(seq):
    return hashlib.sha256('\n'.join(seq).encode('utf-8', 'surrogateescape')).hexdigest()[:12]


def in_order(small, big):
    # greedy: each line of `small` matched to the next equal line of `big` after the previous match; unmatched lines do not advance
    pos = defaultdict(list)
    for i, ln in enumerate(big):
        pos[ln].append(i)
    cur, used, miss = -1, set(), []
    for ln in small:
        lst = pos.get(ln)
        if not lst:
            miss.append(ln); continue
        k = bisect.bisect_right(lst, cur)
        if k == len(lst):
            miss.append(ln); continue
        cur = lst[k]; used.add(cur)
    return used, miss


def deck_lines(case_dir, deck):
    out, incs, missing_inc = [], 0, 0
    todo = [deck]
    seen = set()
    while todo:
        p = todo.pop(0)
        if p in seen:
            continue
        seen.add(p)
        if not os.path.isfile(p):
            missing_inc += 1; continue
        for ln in lines_of(p):
            if ln.strip():
                out.append(ln)
            m = re.match(r"^\s*include\s+(\S+)", ln)
            if m and '$' not in m.group(1):
                incs += 1
                todo.append(os.path.join(case_dir, m.group(1)))
    return out, incs, missing_inc


def fsha(path):
    hh = hashlib.sha256()
    with open(path, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''):
            hh.update(blk)
    return hh.hexdigest()


def steps_of(lines):
    s = set()
    for ln in lines:
        m = STEPLINE.match(ln)
        if m:
            s.add(int(m.group(1)))
    return s


rows, bad = [], 0
for c in CASES:
    d = os.path.join(ROOT, c)
    lig_p, txt_p, deck_p = os.path.join(d, 'log.liggghts'), os.path.join(d, 'log.txt'), os.path.join(d, 'input_%s.liggghts' % c)
    post = os.path.join(d, 'post_%s' % c)
    if not (os.path.isfile(lig_p) and os.path.isfile(txt_p)):
        print('%s  MISSING_LOG' % c); bad += 1; continue
    lig, txt = lines_of(lig_p), lines_of(txt_p)
    b_lig = [ln for ln in lig if PRESS.match(ln)]
    b_txt = [ln for ln in txt if PRESS.match(ln)]
    same_b7 = b_lig == b_txt
    used, miss = in_order(txt, lig)
    miss_fin = sum(1 for ln in miss if FIN.search(ln))
    miss_ok = sum(1 for ln in miss if not FIN.search(ln) and re.search(r'WARNING|mpirun|Open MPI|MPI_|orte|nohup|^\s*$', ln))
    miss_other = len(miss) - miss_fin - miss_ok
    extra = [lig[i] for i in range(len(lig)) if i not in used]
    if os.path.isfile(deck_p):
        dl, incs, miss_inc = deck_lines(d, deck_p)
        ligset = set(lig)
        found = sum(1 for ln in dl if ln in ligset)
        deck_s = '%d/%d (include %d · 없는 include %d)' % (found, len(dl), incs, miss_inc)
        deck_ok = found == len(dl) and miss_inc == 0
        dset = set(dl)
    else:
        deck_s, deck_ok, dset = 'NO_DECK', False, set()
    x_deck = sum(1 for ln in extra if ln in dset)
    x_cmd = sum(1 for ln in extra if ln not in dset and CMD.match(ln))
    x_other = len(extra) - x_deck - x_cmd
    dump_step, deck_sha_exp, atom_sha_exp = COHORT[c]
    deck_sha_ok = os.path.isfile(deck_p) and fsha(deck_p) == deck_sha_exp
    atom_p = os.path.join(post, 'atom_%d.liggghts' % dump_step)
    atom_sha_ok = os.path.isfile(atom_p) and fsha(atom_p) == atom_sha_exp
    s_lig, s_txt = steps_of(lig), steps_of(txt)
    in_lig = bool(s_lig) and min(s_lig) <= dump_step <= max(s_lig)
    in_txt = bool(s_txt) and min(s_txt) <= dump_step <= max(s_txt)
    exact = dump_step in s_lig and dump_step in s_txt
    t_lig, t_txt = os.stat(lig_p).st_mtime, os.stat(txt_p).st_mtime
    nb_lig = sum(1 for ln in lig if BANNER.match(ln)); nb_txt = sum(1 for ln in txt if BANNER.match(ln))
    nfin = sum(1 for ln in txt if FIN.search(ln))
    ok = (nb_lig == 1 and nb_txt <= 1 and nfin == 1 and same_b7 and miss_other == 0 and deck_ok and deck_sha_ok and atom_sha_ok and in_lig and in_txt)
    bad += 0 if ok else 1
    print('%s  banner %d/%d · Finished %d · 압력줄 %d/%d 같음=%s (%s) · txt⊂lig %d/%d (빠진 %d = Finished %d · 경고·MPI %d · 기타 %d) · '
          'lig 추가 %d (덱 %d · 명령 %d · 기타 %d) · 덱 %s · 덱 지문=코호트 %s · 하베스트 step %s (lig 범위 %s · txt 범위 %s · 정확히 %s) · atom 지문=코호트 %s · txt−lig %+.0f s · %s'
          % (c, nb_lig, nb_txt, nfin, len(b_lig), len(b_txt), 'Y' if same_b7 else 'N', h(b_lig), len(txt) - len(miss), len(txt),
             len(miss), miss_fin, miss_ok, miss_other, len(extra), x_deck, x_cmd, x_other, deck_s, 'Y' if deck_sha_ok else 'N', dump_step, 'Y' if in_lig else 'N',
             'Y' if in_txt else 'N', 'Y' if exact else 'N', 'Y' if atom_sha_ok else 'N', t_txt - t_lig, 'OK' if ok else 'CHECK'))
print('SUMMARY  OK %d / %d · CHECK %d  (값 출력 0 · 읽기만)' % (len(CASES) - bad, len(CASES), bad))
