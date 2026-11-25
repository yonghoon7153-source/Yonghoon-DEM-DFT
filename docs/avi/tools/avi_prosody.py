#!/usr/bin/env python3
"""S7 강약 · 이어지는 말 · 숨 — 대리 지표 (듣기 확인 = 1저자).

1저자 11-25: *"보이스 강약이나 이음 등이 아직 부족"*.  smart · 빠르기 1.0 이라 대본의 강조 · 빠르기 칸은 음성에 가지 않는다
(강약은 글과 쉼으로만 정해진다) — 그래서 만든 음성이 실제로 그렇게 됐는지를 따로 잰다.  `avi_audio.qc()` 가 부른다.

(i)  emphasis()  — 대본 '강조 낱말' (scenes.json 줄의 emphasis) 자리의 목소리 높이 · 세기를 같은 문장의 이웃 낱말 (앞뒤 둘씩)
                   과 견준다.  낱말 자리 = 음절 비례 어림 (쉼표 자리의 쉼과 문장 안 쉼은 건너뜀) — 오차 ±0.3–0.5 s
                   (낱말 하나 길이와 비슷) 라 한 낱말 판정은 흔들린다 · 편 전체의 비율로 읽는다.
(ii) cont_joins() — 한 생각을 잇는 문장 쌍 (대본 표지 `joins_prev` · 앞 문장 끝이 '…요.' 로 이어지는 꼴) 사이의 쉼이
                   JOIN_PAUSE_MAX_S 보다 길면 '끊겨 들림'.  뒤 문장의 대본 표지 `new_thought` (새 생각) 는 끝 꼴 어림을 끈다.
(iii) breaths()  — BREATH_SYL 음절 이상인데 BREATH_PAUSE_S 넘는 문장 안 쉼이 하나도 없으면 '숨 없음'.

문턱은 ep01 v2 최종 음성 (11-25 · 113 문장) 에서 정한 경험값이다 — 표준이 아니고, 소리를 듣지 않은 수치다.
"""
import re

import numpy as np

from korean_text import syllables

#: (i) 도드라짐 점수 = (이웃 낱말 대비 높이 차 반음) / EMPH_PK_SCALE + (세기 차 dB) / EMPH_DB_SCALE — 두 척도 = ep01 v2 최종 음성의
#: 강조 표지 없는 낱말 763 개 (이웃 대비 · 세기 = 유성 프레임만 · 문장마다의 쉼 문턱) 의 사분위 폭 (5.72 반음 · 2.74 dB) ·
#: 문턱 EMPH_Z = 그 낱말들 점수의 위 4 분의 1 자리 (0.75) → '힘 받음' = 보통 낱말 넷 중 셋보다 도드라짐.  ep01 v2: 강조 표지 낱말
#: 103 개 중 37 % 가 넘음 (보통 낱말 25 % · AUC 높이 0.58 · 세기 0.60 · 점수 0.60) — smart 는 대본의 강조 칸을 읽지 않는다는
#: 것과 맞는다.  문장 평균과 견주면 (문장 끝으로 갈수록 내려가는 높이 때문에) 높이 AUC 0.48 로 못 가렸다 → 이웃 (앞뒤 둘씩) 과 견준다.
EMPH_PK_SCALE = 5.7
EMPH_DB_SCALE = 2.7
EMPH_Z = 0.75
WORD_ERR = "±0.3–0.5 s"
MIN_VOICED = 4                        # 낱말 창 안 유성 프레임 (10 ms) 이 이보다 적으면 판정 못 함
#: (ii) 레퍼런스 문장 끝 쉼 중앙 0.335 s (80 % 가 0.24–0.46) · ep01 v3 의 이음 쉼 0.15–0.35 s · v2 문장 끝 쉼 중앙 0.45 s —
#: 이어지는 생각인데 0.40 s 를 넘으면 문장 끝만큼 쉬는 것 (끊겨 들림).
JOIN_PAUSE_MAX_S = 0.40
#: (iii) 대본 규칙 (스킬 §4 의 1: 40 음절 넘으면 쉼 자리) · 0.15 s = 쉼표 숨의 아래 끝 (ep01 v2: 쉼표 자리 쉼 대부분 0.16–0.35 s).
BREATH_SYL = 40
BREATH_PAUSE_S = 0.15
GAP_MIN_S = 0.06                      # 문장 안 '쉼' 으로 셀 가장 짧은 무음 (음절 사이 틈은 이보다 짧다)
EDGE_S = 0.05
CONT_END = re.compile(r"(도요|는데요|인데요|고요|지만요|면요|서요|니까요|거든요|데요|는요|은요)[.]?$")
PROXY = "대리 지표 · 듣기 확인 = 1저자"


# ------------------------------------------------------------------ helpers
def line_threshold(seg_lev):
    """Pause threshold of ONE sentence (same rule as avi_audio._quiet_threshold, on the sentence's own frames).
    The episode-wide threshold sits ~35 dB under speech when the file has digital silence between sentences
    (ep01 v2: −47.7 dB) — comma pauses inside a sentence never get that low (they sit near −40 dB), so a
    whole-file threshold finds almost no breath; the sentence's own floor does (the old qc 'internal_pauses' rule)."""
    ref = np.percentile(seg_lev, 90)
    floor = np.percentile(seg_lev, 5)
    return min(ref - 22.0, max(floor + 10.0, ref - 35.0))


def internal_gaps(lev, hop, thr, a, b, min_dur=GAP_MIN_S):
    """Silences inside [a, b] — frames below the sentence's own pause threshold (thr is ignored: kept for the call
    signature) — [(g0, g1)] in seconds, edges excluded."""
    i0, i1 = max(0, int(a / hop)), min(len(lev), int(b / hop) + 1)
    if i1 - i0 < 3:
        return []
    q = (lev[i0:i1] < line_threshold(lev[i0:i1])).astype(int)
    d = np.diff(np.concatenate([[0], q, [0]]))
    st, en = np.where(d == 1)[0], np.where(d == -1)[0]
    out = []
    for s_, e_ in zip(st, en):
        g0, g1 = (i0 + s_ + 1.5) * hop, (i0 + e_ + 1.5) * hop
        if g1 - g0 >= min_dur and g0 > a + EDGE_S and g1 < b - EDGE_S:
            out.append((round(g0, 3), round(g1, 3)))
    return out


def _speech_time(a, b, gaps):
    return (b - a) - sum(g1 - g0 for g0, g1 in gaps)


def _at(a, b, gaps, frac):
    """Absolute time at fraction `frac` of the speech time in [a, b] (gaps skipped)."""
    target = max(0.0, min(1.0, frac)) * _speech_time(a, b, gaps)
    t, acc = a, 0.0
    for g0, g1 in sorted(gaps):
        seg = g0 - t
        if acc + seg >= target:
            return t + (target - acc)
        acc += seg
        t = g1
    return t + (target - acc)


def word_window(say, pos, length, a, b, gaps):
    """Estimated (t0, t1) of say[pos:pos+length] in the sentence spoken over [a, b].
    Comma chunks are pinned to the longest internal gaps when there are enough of them (one per comma);
    inside a chunk (or the whole line) the time is syllable-proportional over the speech time."""
    commas = [m.start() for m in re.finditer(",", say)]
    n_tot = max(1, syllables(say))
    s0 = syllables(say[:pos])
    s1 = s0 + max(1, syllables(say[pos:pos + length]))
    if commas and len(gaps) >= len(commas):
        pins = sorted(sorted(gaps, key=lambda g: g[1] - g[0], reverse=True)[:len(commas)])
        bounds = [0] + [syllables(say[:c]) for c in commas] + [n_tot]
        runs = [(a if k == 0 else pins[k - 1][1], b if k == len(pins) else pins[k][0]) for k in range(len(pins) + 1)]
        out = []
        for s_ in (s0, s1):
            k = max(0, min(len(runs) - 1, next((j for j in range(len(runs)) if s_ < bounds[j + 1]), len(runs) - 1)))
            if s_ == s1 and k > 0 and s_ == bounds[k]:
                k -= 1                                    # a word ending exactly at a comma ends in the chunk before it
            ra, rb = runs[k]
            inner = [g for g in gaps if ra < g[0] and g[1] < rb]
            span = max(1, bounds[k + 1] - bounds[k])
            out.append(_at(ra, rb, inner, (s_ - bounds[k]) / span))
        return out[0], out[1]
    return _at(a, b, gaps, s0 / n_tot), _at(a, b, gaps, s1 / n_tot)


def _stats(t0, t1, tf, f0, voiced, lev, hop, med_hz, ref_db):
    """(높이 반음 vs 문장 중앙 · 세기 dB vs 문장 유성 중앙) of the voiced frames in [t0, t1) — None if too few voiced frames.
    Level = voiced frames only (a window that leaks into a pause would otherwise read 'quiet')."""
    m = (tf >= t0) & (tf < t1) & voiced
    if int(m.sum()) < MIN_VOICED or not med_hz:
        return None
    pk = float(12 * np.log2(np.percentile(f0[m], 90) / med_hz))
    db = float(np.mean(np.interp(tf[m], np.arange(len(lev)) * hop + 0.015, lev))) - ref_db
    return pk, db


def _ref_db(a, b, tf, voiced, lev, hop):
    m = (tf >= a) & (tf < b) & voiced
    if int(m.sum()) <= 8:
        return None
    return float(np.median(np.interp(tf[m], np.arange(len(lev)) * hop + 0.015, lev)))


# ------------------------------------------------------------------ (i) emphasis
def emphasis(lines, lid, tf, f0, voiced, lev, hop, thr):
    out = []
    for d in lines:
        ln = lid.get(d["id"]) or {}
        emph = [w for w in (ln.get("emphasis") or []) if str(w).strip()]
        if not emph:
            continue
        say = (ln.get("say") or ln.get("text") or "").strip()
        a, b = d["t0"], d["t1"]
        gaps = internal_gaps(lev, hop, thr, a, b)
        m = (tf >= a) & (tf < b) & voiced
        med = float(np.median(f0[m])) if int(m.sum()) > 8 else None
        ref_db = _ref_db(a, b, tf, voiced, lev, hop) or 0.0
        words = [(mm.start(), mm.end()) for mm in re.finditer(r"\S+", say)]
        wstat = []
        for p0, p1 in words:
            w0, w1 = word_window(say, p0, p1 - p0, a, b, gaps)
            wstat.append(((p0, p1), (w0, w1), _stats(w0, w1, tf, f0, voiced, lev, hop, med, ref_db)))
        for w in emph:
            pos = say.find(w)
            rec = dict(id=d["id"], word=w, t0=None, t1=None, d_peak_st=None, d_db=None, n_nb=0, got=None, why="")
            if pos < 0:
                rec["why"] = "읽는 꼴에 이 낱말이 없음"
                out.append(rec)
                continue
            t0, t1 = word_window(say, pos, len(w), a, b, gaps)
            rec.update(t0=round(t0, 2), t1=round(t1, 2))
            s = _stats(t0, t1, tf, f0, voiced, lev, hop, med, ref_db)
            if s is None:
                rec["why"] = "낱말 창에 유성음이 적음 (높이를 못 잼)"
                out.append(rec)
                continue
            # neighbours = up to two words before and after that do not overlap the emphasised span
            idx = [k for k, ((p0, p1), _, _) in enumerate(wstat) if p1 > pos and p0 < pos + len(w)]
            lo, hi = (min(idx), max(idx)) if idx else (0, -1)
            nb = [wstat[k][2] for k in list(range(max(0, lo - 2), lo)) + list(range(hi + 1, min(len(wstat), hi + 3)))
                  if wstat[k][2] is not None]
            if len(nb) >= 2:
                base_pk = float(np.median([x[0] for x in nb]))
                base_db = float(np.median([x[1] for x in nb]))
            else:
                base_pk, base_db = 0.0, 0.0                    # short sentence: against the sentence itself
            dpk, ddb = s[0] - base_pk, s[1] - base_db
            z = score(dpk, ddb)
            got = z >= EMPH_Z
            rec.update(d_peak_st=round(dpk, 2), d_db=round(ddb, 2), z=round(z, 2), n_nb=len(nb), got=bool(got),
                       why="" if got else f"이웃 낱말보다 높이 {dpk:+.1f} 반음 · 세기 {ddb:+.1f} dB → 점수 {z:+.2f} < {EMPH_Z:g}")
            out.append(rec)
    return out


def score(dpk, ddb):
    return dpk / EMPH_PK_SCALE + ddb / EMPH_DB_SCALE


def baseline(lines, lid, tf, f0, voiced, lev, hop, thr):
    """Same score for every word WITHOUT an emphasis mark (neighbours = unmarked words) — the episode's own yardstick:
    if marked words do not pass clearly more often than these, the voice is not putting force on the marks."""
    zs = []
    for d in lines:
        ln = lid.get(d["id"]) or {}
        say = (ln.get("say") or ln.get("text") or "").strip()
        a, b = d["t0"], d["t1"]
        gaps = internal_gaps(lev, hop, thr, a, b)
        m = (tf >= a) & (tf < b) & voiced
        if int(m.sum()) <= 8:
            continue
        med = float(np.median(f0[m]))
        ref_db = _ref_db(a, b, tf, voiced, lev, hop) or 0.0
        emph = [w for w in (ln.get("emphasis") or []) if str(w).strip() and say.find(w) >= 0]
        words = [(mm.start(), mm.end()) for mm in re.finditer(r"\S+", say)]
        marked = [any(p1 > say.find(w) and p0 < say.find(w) + len(w) for w in emph) for p0, p1 in words]
        st = [_stats(*word_window(say, p0, p1 - p0, a, b, gaps), tf, f0, voiced, lev, hop, med, ref_db) for p0, p1 in words]
        for k, s_ in enumerate(st):
            if s_ is None or marked[k]:
                continue
            nb = [st[j] for j in list(range(max(0, k - 2), k)) + list(range(k + 1, min(len(st), k + 3)))
                  if st[j] is not None and not marked[j]]
            if len(nb) < 2:
                continue
            zs.append(score(s_[0] - float(np.median([x[0] for x in nb])), s_[1] - float(np.median([x[1] for x in nb]))))
    return zs


# ------------------------------------------------------------------ (ii) continuing thoughts
def cont_joins(lines, lid, rows):
    by = {r["id"]: r for r in rows}
    out = []
    for x, y in zip(lines, lines[1:]):
        la, lb = lid.get(x["id"]) or {}, lid.get(y["id"]) or {}
        say = (la.get("say") or la.get("text") or "").strip()
        m = CONT_END.search(say)
        marker = bool(lb.get("joins_prev"))
        if lb.get("new_thought") and not marker:
            continue                                      # 대본 표지 '새 생각' = 끝 꼴 어림을 끈다 (예: '…거든요.' 다음 '또 하나,')
        if not (marker or m):
            continue
        pause = round(max(0.0, y["t0"] - x["t1"]), 2)
        long_ = pause > JOIN_PAUSE_MAX_S
        fin = (by.get(x["id"]) or {}).get("final_st")
        why = []
        if long_:
            why.append(f"쉼 {pause:.2f} s > {JOIN_PAUSE_MAX_S:g} s")
        if la.get("_scene") and lb.get("_scene") and la["_scene"] != lb["_scene"]:
            why.append("장면이 바뀌는 자리 (앞 장면의 끝 문장이 이어지는 꼴)")
        out.append(dict(a=x["id"], b=y["id"], t=round(x["t1"], 2), pause=pause, marker=marker,
                        ending=m.group(1) if m else None, final_st_a=fin, long=bool(long_), why=" · ".join(why)))
    return out


# ------------------------------------------------------------------ (iii) breaths
def breaths(lines, lid, lev, hop, thr):
    out = []
    for d in lines:
        ln = lid.get(d["id"]) or {}
        say = (ln.get("say") or ln.get("text") or "").strip()
        syl = syllables(say)
        if syl < BREATH_SYL:
            continue
        gaps = internal_gaps(lev, hop, thr, d["t0"], d["t1"])
        durs = [round(g1 - g0, 2) for g0, g1 in gaps]
        mx = max(durs) if durs else 0.0
        out.append(dict(id=d["id"], t0=round(d["t0"], 2), syl=syl, commas=say.count(","), pauses=durs, max_pause=mx,
                        no_breath=bool(mx < BREATH_PAUSE_S)))
    return out


# ------------------------------------------------------------------ all three + summary + markdown
def analyze(lines, lid, rows, tf, f0, voiced, lev, hop, thr):
    em = emphasis(lines, lid, tf, f0, voiced, lev, hop, thr)
    zb = baseline(lines, lid, tf, f0, voiced, lev, hop, thr)
    jn = cont_joins(lines, lid, rows)
    br = breaths(lines, lid, lev, hop, thr)
    judged = [e for e in em if e["got"] is not None]
    summ = dict(emph_n=len(em), emph_got=sum(1 for e in em if e["got"] is True),
                emph_missed=sum(1 for e in em if e["got"] is False), emph_unknown=sum(1 for e in em if e["got"] is None),
                emph_pass_rate=round(sum(1 for e in judged if e["got"]) / len(judged), 3) if judged else None,
                plain_n=len(zb), plain_pass_rate=round(float(np.mean(np.array(zb) >= EMPH_Z)), 3) if zb else None,
                join_cont_n=len(jn), join_cont_marker=sum(1 for j in jn if j["marker"]),
                join_cont_long=sum(1 for j in jn if j["long"]), breath_n=len(br),
                breath_missing=sum(1 for b in br if b["no_breath"]))
    rules = dict(emph_pk_scale=EMPH_PK_SCALE, emph_db_scale=EMPH_DB_SCALE, emph_z=EMPH_Z, word_err=WORD_ERR,
                 join_pause_max_s=JOIN_PAUSE_MAX_S,
                 breath_syl=BREATH_SYL, breath_pause_s=BREATH_PAUSE_S, proxy=PROXY)
    return dict(emphasis=em, joins=jn, breath=br, summary=summ, rules=rules)


def flags(pro):
    s, out = pro["summary"], []
    if s["emph_missed"]:
        rate = "" if s["emph_pass_rate"] is None or s["plain_pass_rate"] is None else \
            f" · 힘 받은 비율 {s['emph_pass_rate'] * 100:.0f} % ↔ 강조 표지 없는 낱말 {s['plain_pass_rate'] * 100:.0f} %"
        out.append(f"강조 낱말 {s['emph_missed']} / {s['emph_n'] - s['emph_unknown']} 곳이 이웃 낱말보다 도드라지지 않는다{rate} "
                   f"('## 강약' · {PROXY})")
    if s["join_cont_long"]:
        out.append(f"한 생각을 잇는 문장 쌍 {s['join_cont_long']} / {s['join_cont_n']} 곳의 쉼이 {JOIN_PAUSE_MAX_S:g} s 를 넘는다 "
                   f"(끊겨 들림 · '## 숨')")
    if s["breath_missing"]:
        out.append(f"{BREATH_SYL} 음절 이상 문장 {s['breath_missing']} / {s['breath_n']} 곳에 {BREATH_PAUSE_S:g} s 넘는 숨 (쉼) 이 없다 "
                   f"({', '.join(b['id'] for b in pro['breath'] if b['no_breath'])} · '## 숨')")
    return out


def _pc(x):
    return "—" if x is None else f"{x * 100:.0f} %"


def _t(t):
    return f"{int(t // 60)}:{t % 60:04.1f}" if isinstance(t, (int, float)) else "—"


def md(pro):
    s = pro["summary"]
    em = pro["emphasis"]
    L = ["", "## 강약", "",
         f"> {PROXY} · 낱말 자리 = 음절 비례 어림 (오차 {WORD_ERR} · 낱말 하나 길이와 비슷 — 한 곳 판정보다 편 전체 비율로 읽는다) · "
         f"도드라짐 점수 = 이웃 낱말 (앞뒤 둘씩) 대비 높이 차 ÷ {EMPH_PK_SCALE:g} 반음 + 세기 차 ÷ {EMPH_DB_SCALE:g} dB · "
         f"'힘 받음' = 점수 ≥ {EMPH_Z:g} (= ep01 보통 낱말 넷 중 셋보다 도드라짐 · ep01 경험값)", "",
         f"- 대본 강조 낱말 {s['emph_n']} · 힘 받음 {s['emph_got']} · 못 받음 {s['emph_missed']} · 판정 못 함 {s['emph_unknown']}",
         f"- 견줄 잣대: 힘 받은 비율 강조 낱말 {_pc(s['emph_pass_rate'])} ↔ 강조 표지 없는 낱말 {_pc(s['plain_pass_rate'])} "
         f"({s['plain_n']} 개) — 앞이 뒤보다 뚜렷이 높지 않으면 목소리가 강조 표지에 힘을 싣지 않는 것"]
    if em:
        L += ["", "| 시각 | 문장 | 강조 낱말 | 높이 (이웃 대비 반음) | 세기 (dB) | 점수 | 판정 | 까닭 |", "|---|---|---|---|---|---|---|---|"]
        for e in sorted(em, key=lambda e: (e["got"] is not False, e["got"] is not None, e["t0"] or 0))[:60]:
            v = "받음" if e["got"] else ("못 받음" if e["got"] is False else "판정 못 함")
            L.append(f"| {_t(e['t0'])} | {e['id']} | {e['word']} | {e['d_peak_st'] if e['d_peak_st'] is not None else '—'} | "
                     f"{e['d_db'] if e['d_db'] is not None else '—'} | {e.get('z', '—') if e.get('z') is not None else '—'} | {v} | "
                     f"{e['why'] or '—'} |")
    jn, br = pro["joins"], pro["breath"]
    L += ["", "## 숨", "",
          f"> {PROXY} · 문턱 = ep01 경험값 (이어지는 쌍 쉼 ≤ {JOIN_PAUSE_MAX_S:g} s · {BREATH_SYL} 음절 이상이면 {BREATH_PAUSE_S:g} s 넘는 안 쉼 ≥ 1)", "",
          f"- 한 생각을 잇는 문장 쌍 {s['join_cont_n']} (대본 표지 {s['join_cont_marker']} · 나머지 = 앞 문장 끝 '…요.' 꼴) · "
          f"쉼이 {JOIN_PAUSE_MAX_S:g} s 넘음 {s['join_cont_long']}"]
    if jn:
        L += ["", "| 시각 (앞 문장 끝) | 앞 → 뒤 | 쉼 s | 근거 | 앞 문장 끝 억양 반음 | 판정 | 까닭 |", "|---|---|---|---|---|---|---|"]
        for j in sorted(jn, key=lambda j: (not j["long"], j["t"])):
            src = " · ".join(x for x in (("대본 표지" if j["marker"] else ""), (f"'~{j['ending']}.'" if j["ending"] else "")) if x)
            L.append(f"| {_t(j['t'])} | {j['a']} → {j['b']} | {j['pause']} | {src} | "
                     f"{j['final_st_a'] if j['final_st_a'] is not None else '—'} | {'김' if j['long'] else '—'} | {j['why'] or '—'} |")
    L += ["", f"- {BREATH_SYL} 음절 이상 문장 {s['breath_n']} · {BREATH_PAUSE_S:g} s 넘는 안 쉼 없음 {s['breath_missing']}"]
    if br:
        L += ["", "| 시각 | 문장 | 음절 | 쉼표 | 문장 안 쉼 s | 판정 |", "|---|---|---|---|---|---|"]
        for b in sorted(br, key=lambda b: (not b["no_breath"], b["t0"])):
            L.append(f"| {_t(b['t0'])} | {b['id']} | {b['syl']} | {b['commas']} | {' · '.join(str(p) for p in b['pauses']) or '없음'} | "
                     f"{'숨 없음' if b['no_breath'] else '—'} |")
    return L
