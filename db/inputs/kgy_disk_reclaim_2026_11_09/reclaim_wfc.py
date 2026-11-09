# kgy 디스크 회수 2026-11-09 — QE 파동함수만 지운다 (.out · charge-density · xml · NEB .dat/.path 는 그대로)
# 절차: kb/methodology/qe_disk_reclaim_2026_09_12.md · 기록: db/properties/kgy_disk_reclaim_2026_11_09.json
# DRY=1 이면 지우지 않고 목록만. RECLAIM_HOME 은 시험용 (기본 ~).
import os, re, sys, time
H = os.path.realpath(os.environ.get("RECLAIM_HOME") or os.path.expanduser("~"))
DRY = os.environ.get("DRY") == "1"
NOW = time.time(); RECENT = 24 * 3600
ROOTS = ["work", "lldvar/runs/sei_neb", "Yonghoon-DEM-DFT/tmp"]     # 사용자 것 (11-09: work 전체 · bml 포함)
CLOSED = ["work/runs/" + x for x in (                                 # 원장에서 닫힘 → 미완 출력이 있어도 파동함수 전부
    "nd_scf_2026_09_08 ndo_site_dft_2026_10_15 ndo_site_dft_kprobe_2026_10_16 ndo_site_eos_2026_10_16 "
    "ndo_site_eos_v0_2026_10_23 nd_q2_decomp_2026_10_23 nd_q2_kprobe_2026_10_26 nd_q3p_1027 "
    "li2s_model_check_sp_2026_10_21 li2s_neb_cellconv_1009 smallcell_gb3 "
    "force_check_700K force_check_700K_v2 fc_control_smear").split()]
EXCLUDE = ["work/runs/cei_gap_1027", "work/runs/li2s2"]               # CEI 판독 전 · li2s-2 도는 중 (접두어)
WFC_SCR = re.compile(r"\.wfc\d+$")
QEHEAD = re.compile(rb"Program ([A-Z][A-Z0-9_\-]*) v\.")
NOTDONE = (b"convergence not achieved", b"maximum number of steps has been reached")

def rel(p): return os.path.relpath(p, H)
def under(p, base): return p == base or p.startswith(base.rstrip("/") + "/")
def pref(r, lst): return next((x for x in lst if r == x or r.startswith(x + "/") or (x.endswith("li2s2") and r.startswith(x))), None)

busy = set(); me = {os.getpid(), os.getppid()}
for pid in os.listdir("/proc"):
    if not pid.isdigit() or int(pid) in me: continue
    try: busy.add(os.path.realpath(os.readlink(f"/proc/{pid}/cwd")))
    except OSError: pass
    try:
        for fd in os.listdir(f"/proc/{pid}/fd"):
            try:
                t = os.readlink(f"/proc/{pid}/fd/{fd}")
                if t.startswith("/") and not t.startswith(("/dev", "/proc", "/sys")): busy.add(os.path.dirname(t))
            except OSError: pass
    except OSError: pass
    try:
        for tok in open(f"/proc/{pid}/cmdline", "rb").read().split(b"\0"):
            tok = tok.decode("utf-8", "replace").split("=")[-1]
            if tok.startswith("/"): busy.add(os.path.realpath(tok))
    except OSError: pass
def is_busy(*dirs): return any(under(b, d) for b in busy for d in dirs)

_recent = {}
def recent(d):
    if d not in _recent:
        hit = None
        for dp, dns, fns in os.walk(d):
            for f in fns:
                try:
                    if os.lstat(os.path.join(dp, f)).st_mtime > NOW - RECENT: hit = os.path.join(dp, f); break
                except OSError: pass
            if hit: break
        _recent[d] = hit
    return _recent[d]

_qe = {}
def qe_outputs(d):
    if d in _qe: return _qe[d]
    res = _qe[d] = []
    try: names = sorted(os.listdir(d))
    except OSError: return res
    for n in names:
        p = os.path.join(d, n)
        if n == "PW.out" or not n.endswith((".out", ".log")) or os.path.islink(p) or not os.path.isfile(p): continue
        try:
            with open(p, "rb") as f:
                head = f.read(65536); sz = os.fstat(f.fileno()).st_size
                f.seek(max(0, sz - 2_000_000)); tail = f.read().lower()
        except OSError: continue
        m = QEHEAD.search(head)
        if not m: continue                                            # QE 출력이 아니다 (slurm 로그 등)
        prog = m.group(1).decode()
        ok = b"job done" in tail and not any(x in tail for x in NOTDONE)
        if prog == "NEB": ok = ok and b"convergence achieved" in tail
        res.append((p, prog, ok))
    return res

def find_R(start, rootabs):
    d = start
    for _ in range(3):
        outs = qe_outputs(d)
        if outs: return d, outs
        if d == rootabs or not under(d, rootabs): break
        d = os.path.dirname(d)
    return None, []

units = []
for r in ROOTS:
    ra = os.path.join(H, r)
    if not os.path.isdir(ra) or os.path.islink(ra): print(f"[없음] {r}"); continue
    dev = os.lstat(ra).st_dev
    for dp, dns, fns in os.walk(ra):
        dns[:] = [x for x in dns if not os.path.islink(os.path.join(dp, x)) and os.lstat(os.path.join(dp, x)).st_dev == dev]
        w = [f for f in fns if (f.startswith("wfc") if dp.endswith(".save") else WFC_SCR.search(f))]
        w = [os.path.join(dp, f) for f in w if os.path.isfile(os.path.join(dp, f)) and not os.path.islink(os.path.join(dp, f))]
        if w: units.append((r, ra, dp, w))
for c in CLOSED:
    if not os.path.isdir(os.path.join(H, c)): print(f"[없음] {c} (닫힘 목록)")

log = open(os.path.join(H, "reclaim_wfc_2026_11_09.log"), "a")
log.write(f"# {time.strftime('%Y-%m-%d %H:%M:%S')} DRY={int(DRY)} H={H}\n")
freed = {}; skipped = []; kept_check = []; nfile = 0
for r, ra, D, w in units:
    size = sum(os.lstat(p).st_size for p in w); rd = rel(D)
    ex = pref(rd, EXCLUDE); cl = pref(rd, CLOSED)
    if ex: skipped.append((size, rd, f"제외 ({ex})")); continue
    if cl:
        ca = os.path.join(H, cl)
        if is_busy(ca): skipped.append((size, rd, "도는 잡이 이 폴더를 쓴다")); continue
        hit = recent(ca)
        if hit: skipped.append((size, rd, f"24 h 안 수정 {rel(hit)}")); continue
        why = "닫힘"; R = ca; outs = []
    else:
        R, outs = find_R(D if not D.endswith(".save") else os.path.dirname(D), ra)
        if R is None: skipped.append((size, rd, "짝 QE 출력 없음 (3 단계 안)")); continue
        bad = [rel(p) for p, prog, ok in outs if not ok]
        if bad: skipped.append((size, rd, f"미완 출력 {bad[0]}" + (f" 외 {len(bad)-1}" if len(bad) > 1 else ""))); continue
        if is_busy(R, D): skipped.append((size, rd, "도는 잡이 이 폴더를 쓴다")); continue
        hit = recent(R)
        if hit: skipped.append((size, rd, f"24 h 안 수정 {rel(hit)}")); continue
        why = "끝남"
    keep = [p for p, _, _ in outs] + [os.path.join(D, f) for f in os.listdir(D) if f.startswith("charge-density") or f == "data-file-schema.xml"]
    kept_check += keep
    k = "/".join(rd.split("/")[:4 if rd.startswith("work/bml/") else 3])
    for p in w:
        st = os.lstat(p)
        if os.path.islink(p) or not os.path.isfile(p): continue
        if not DRY: os.remove(p)
        log.write(f"{'DRY ' if DRY else ''}rm {st.st_size} {p}\n"); nfile += 1
        freed.setdefault(k, [0, 0, why]); freed[k][0] += st.st_size; freed[k][1] += 1
log.close()
miss = [p for p in kept_check if not os.path.exists(p)]
tag = "지울 예정" if DRY else "지움"
for k, (s, n, why) in sorted(freed.items(), key=lambda x: -x[1][0]):
    print(f"[{tag}] {s/1e9:7.2f} GB  {n:5d} 파일  {k}  ({why})")
skipped.sort(reverse=True)
for s, rd, why in skipped[:25]: print(f"[건너뜀] {s/1e9:7.2f} GB  {rd}  — {why}")
if len(skipped) > 25: print(f"[건너뜀] … 그 밖 {len(skipped)-25} 단위 {sum(s for s,_,_ in skipped[25:])/1e9:.2f} GB")
print(f"합계 {tag} {sum(v[0] for v in freed.values())/1e9:.1f} GB ({nfile} 파일) · 건너뜀 {sum(s for s,_,_ in skipped)/1e9:.1f} GB ({len(skipped)} 단위)"
      f" · 남겨야 할 출력·전하밀도 {len(kept_check)} 개 중 없어진 것 {len(miss)} 개" + (f" ⛔ {miss[:3]}" if miss else " ✓"))
print(f"목록: {os.path.join(H, 'reclaim_wfc_2026_11_09.log')}")
