#!/usr/bin/env python3
"""Voice stage on its own — `avi.py voice-auto EP_DIR` (1저자 11-25 "이런 권고안들은 저절로 판단되게 백그라운드 에이전트로").

  python3 -I avi.py voice-auto EP_DIR                     # preview (default): what it would do · API calls 0 · writes nothing
  nice -n 19 python3 -I avi.py voice-auto EP_DIR --run [--rounds 2 --takes 2 --budget-x 3] [--bgm music.wav]

--run, in order (every judgement = one line of EP_DIR/audio/voice_auto_report.md):
 ① Typecast 문정 · smart (previous / next sentence) · tempo 1.0 — only the sentences whose wav does not match the ledger
    (text · neighbours' text · tempo · mode · file hash).  A take that matches is never re-shot.  A ledger voice or model
    that differs from the current one = stop and ask (a voice change is the 1저자's call).
 ② audio-prep   ③ audio-qc (a joint is a jump when neighbouring sentences' F0 medians are >= 2.5 semitones apart)
 ④ while jumps remain, at most --rounds rounds: pick_targets -> retake (--takes new takes each, keep the take closest to
    the neighbours) -> prep -> qc.  A sentence whose current file already had --rounds retake rounds is not retaken again:
    it becomes an ending-fix candidate.  The command never edits the script (the assistant does, meaning unchanged only).
 ⑤ report (md + json) + one line in EP_DIR/DECISIONS.md.
 ⑥ character budget = script characters x --budget-x for the whole episode (every call in the ledger, failed ones too),
    checked before each batch — a batch that would cross it is not sent (stop · ask).  A guard also refuses any single call
    that would cross it (e.g. a retry after a server error), so the budget is never passed.
Exit code 0 = finished (left-over jumps are reported, not an error) · 2 = stopped to ask the 1저자 (budget · API failure ·
voice change).  Internal (공개 금지) episodes and a sheet that does not match scenes.json stop with SystemExit.
"""
import contextlib
import hashlib
import io
import json
import math
import os
import sys
import time
import urllib.error
import wave

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import avi_audio as A  # noqa: E402
import avi_typecast as T  # noqa: E402

ROUNDS, TAKES, BUDGET_X = 2, 2, 3.0
SMALL_JUMP_ST = 3.5          # 스킬 (1저자 11-25): 끝말 고침 뒤에도 남은 작은 뜀 (< 3.5 반음) 은 그대로 둔다
REPORT_MD, REPORT_JSON = "voice_auto_report.md", "voice_auto_report.json"

STOP = {
    "preview": "미리 보기 — API 호출 0 · 파일 안 씀",
    "no_jumps": "높이 뜀 0 — 멈춤",
    "rounds": "다시 찍기 {rounds} 회를 다 씀 — 남은 뜀은 아래 (끝말 고침 후보)",
    "no_targets": "다시 찍을 문장이 없음 (남은 뜀의 문장이 다시 찍기 {rounds} 회를 다 썼거나 손으로 넣은 판) — 끝말 고침 후보 · 손 판은 1저자",
    "budget": "글자 예산을 넘게 됨 — 보내기 전에 멈춤 · 1저자에게 묻기",
    "fail": "API 실패 — 멈춤 (prep · qc 안 함) · 1저자에게 묻기",
    "voice": "원장의 목소리 · 모델이 지금 설정과 다름 — 목소리 바꿈 = 1저자에게 묻기",
}

# sentence ending -> (label, calmer form example).  Order matters (longest first).  The command only SHOWS these:
# the assistant changes an ending in build_scenes.py when the meaning stays the same (skill §음성 단계 자동 판단).
# '~거든요' has no calmer example: turning it into '~기 때문입니다' makes a causal claim = meaning change -> S4 (1저자 · skill §7-1 6).
_ENDINGS = (("거든요", "~거든요", None), ("거죠", "~거죠", "~셈입니다"), ("잖아요", "~잖아요", "~ㅂ니다"),
            ("는데요", "~는데요", None), ("고요", "~고요", None), ("죠", "~죠", "~ㅂ니다"), ("니다", "~ㅂ니다", None),
            ("요", "~요", "~ㅂ니다"), ("다", "~다", None))
_NO_HINT = {"~거든요": "까닭 · 부연 말투 — '…때문' 꼴로 바꾸면 원인 주장 (뜻 바뀜 → S4 · 1저자) · 끝말보다 쉼 · 앞뒤를 본다",
            "~는데요": "이어지는 말 — 끝말보다 쉼 · 앞뒤를 본다", "~고요": "이어지는 말 — 끝말보다 쉼 · 앞뒤를 본다",
            "~ㅂ니다": "이미 차분한 꼴 — 앞뒤 문장의 끝말 · 쉼을 본다", "~다": "이미 차분한 꼴 — 앞뒤를 본다"}


def ending_form(say):
    """('~거죠', '~셈입니다 (뜻 그대로일 때만)') — the ending label and a calmer example (or why there is none)."""
    s = (say or "").strip()
    core = s.rstrip(" .?!…\"'”’").rstrip()
    for k, lab, calm in _ENDINGS:
        if core.endswith(k):
            if s.endswith("?"):
                return lab + " (물음)", "물음 — 끝말 그대로 (오르는 높이가 자연스러울 수 있음 · 1저자 귀)"
            return lab, (f"{calm} (뜻 그대로일 때만)" if calm else _NO_HINT.get(lab, "—"))
    return ("~" + core[-2:]) if core else "—", "—"


class BudgetStop(urllib.error.URLError):
    """Raised by the budget guard BEFORE a call goes out.  run() / retake() treat it like a network error: no call record,
    no characters counted, that sentence (or take) is skipped — voice-auto then stops and asks."""


class BudgetGuard:
    """Wraps the API caller: a call whose characters would take the episode past the budget is not sent."""

    def __init__(self, caller, budget, spent):
        self.caller, self.budget, self.spent0, self.sent, self.blocked = caller, int(budget), int(spent), 0, []

    @property
    def total(self):
        return self.spent0 + self.sent

    def __call__(self, r):
        if self.total + r["chars"] > self.budget:
            self.blocked.append(r["id"])
            raise BudgetStop(f"글자 예산 {self.budget} 을 넘게 됨 (지금 {self.total} + {r['chars']}) — 보내지 않음")
        self.sent += r["chars"]                        # counted when it goes out (a failed call may still be billed)
        return self.caller(r)

    def sleep_fn(self, base):
        return lambda s: None if self.blocked else base(s)


def _kst():
    return time.strftime("%Y-%m-%d %H:%M", time.gmtime(time.time() + 9 * 3600)) + " KST"


def _load_ledger(p):
    if not os.path.exists(p):
        return dict(lines={}, calls=[])
    d = json.load(open(p, encoding="utf-8"))
    d.setdefault("lines", {})
    d.setdefault("calls", [])
    return d


def _spent(led):
    return sum(int(c.get("chars") or 0) for c in led.get("calls", []))


def _qs(q):
    s = (q or {}).get("summary") or {}
    return dict(n=s.get("join_n"), jumps=int(s.get("join_jumps") or 0), max=s.get("join_max_st"), p95=s.get("join_p95_st"))


def _fmt_q(s):
    return f"이음매 {s['n']} · 뜀 {s['jumps']} · 최대 {s['max']} · 95 % {s['p95']} 반음"


def _sg(x):
    return f"{x:+.1f}" if isinstance(x, (int, float)) else "—"


def _tfmt(t):
    return f"{int(t // 60)}:{t % 60:04.1f}" if isinstance(t, (int, float)) else "—"


def _cell(s):
    return str(s).replace("|", "/").replace("\n", " ")


def _dec(st, what, rule, nums="—"):
    st["decisions"].append(dict(no=len(st["decisions"]) + 1, what=what, rule=rule, nums=nums))


def _rules(st):
    return dict(
        make="원장과 안 맞는 줄만 만든다 (글 · 앞뒤 문장 · 빠르기 · 방식 · 파일 해시) — 맞는 판은 다시 찍지 않는다",
        voice="목소리 · 모델 = 원장과 같아야 한다 (바뀌면 1저자)",
        budget=f"글자 예산 = 대본 {st['chars_all']} × {st['budget_x']:g} = {st['budget']} (에피소드 원장 전체 · 보내기 전에 확인)",
        jump=f"뜀 = 이웃 문장 높이 (F0 중앙) 차 ≥ {A.JOIN_JUMP_ST:g} 반음 (ep01 경험값)",
        target="뜀 이음매마다 이웃 기하평균에서 더 먼 문장 하나 (pick_targets)",
        cap=f"같은 판 (글 · 앞뒤) 에서 다시 찍기 {st['rounds']} 회까지 — 다 쓰면 끝말 고침 후보",
        pick="지금 판 + 새 판 중 이웃 기하평균 높이에 가장 가까운 판 (retake)",
        hand="원장에 없는 문장 파일 = 손으로 넣은 판 — 덮어쓰지도 다시 찍지도 않는다 (1저자)",
        stop="실패 · 예산 · 목소리 바뀜 = 멈추고 1저자에게")


def _why_make(r, e, path):
    if not os.path.exists(path):
        return "전에 실패" if (e and e.get("status") == "failed") else "새 문장"
    if not e:
        return "원장에 없음"
    if e.get("status") != "ok":
        return "전에 실패"
    w = []
    if e.get("text") != r["text"]:
        w.append("글 바뀜")
    if e.get("ctx") != r["ctx"]:
        w.append("앞뒤 문장 바뀜")
    if e.get("tempo") != r["tempo"]:
        w.append(f"빠르기 {e.get('tempo')}→{r['tempo']}")
    if e.get("mode") != r["mode"]:
        w.append(f"방식 {e.get('mode')}→{r['mode']}")
    if e.get("preset") != r["preset"]:
        w.append(f"톤 {e.get('preset')}→{r['preset']}")
    if not w and e.get("sha256") != T._sha(path):
        w.append("파일이 원장 해시와 다름")
    return " · ".join(w) or "원장과 다름"


def _group_ids(ids_why, per=8):
    by = {}
    for i, w in ids_why:
        by.setdefault(w, []).append(i)
    return " / ".join(f"{w}: " + " · ".join(v[:per]) + (f" 외 {len(v) - per}" if len(v) > per else "") for w, v in by.items())


def _dev(rows, i):
    f = {r["id"]: r.get("f0_med") for r in rows}
    order = [r["id"] for r in rows]
    if not f.get(i):
        return None
    k = order.index(i)
    nb = [f[order[j]] for j in (k - 1, k + 1) if 0 <= j < len(order) and f.get(order[j])]
    if not nb:
        return None
    return round(12.0 * math.log2(f[i] / math.exp(sum(math.log(x) for x in nb) / len(nb))), 2)


def _remaining(q, led, hand=()):
    out = []
    for j, o in T.pick_sides(q.get("rows", []), q.get("joins", [])):
        d = j.get("d_st")
        out.append(dict(a=j["a"], b=j["b"], t=j.get("t"), d_st=d, size="작은" if abs(d or 0.0) < SMALL_JUMP_ST else "큰",
                        target=o, target_rounds=T.retake_rounds(led, o), hand=o in hand))
    return out


def _log_skipped(st, skipped, hand, led, logged):
    """One decision line for targets that are not retaken: rounds used up (-> ending-fix candidate) or a hand-made file."""
    if not skipped:
        return
    logged.update(skipped)
    hs = [i for i in skipped if i in hand]
    cs = [i for i in skipped if i not in hand]
    if cs:
        _dec(st, f"다시 찍지 않음 {len(cs)}: {' · '.join(cs)}", st["rules"]["cap"],
             " · ".join(f"{i} 이미 {T.retake_rounds(led, i)} 회" for i in cs))
    if hs:
        _dec(st, f"다시 찍지 않음 {len(hs)} (손 판): {' · '.join(hs)}", st["rules"]["hand"])


def _candidates(rem, q, led, rows, rounds):
    by = {r["id"]: r for r in rows}
    out, seen = [], set()
    for x in rem:
        i = x["target"]
        if i in seen or x["hand"] or x["target_rounds"] < rounds or i not in by:
            continue
        seen.add(i)
        rd, tk = T.retake_counts(led, i)
        ending, hint = ending_form(by[i]["text"])
        jmax = max(abs(y["d_st"] or 0.0) for y in rem if i in (y["a"], y["b"]))
        out.append(dict(id=i, text=by[i]["text"], ending=ending, hint=hint, dev_st=_dev(q.get("rows", []), i),
                        jump_max_st=round(jmax, 2), size="작은" if jmax < SMALL_JUMP_ST else "큰", rounds=rd, takes=tk))
    return out


def _qc_current(ep_dir, rows, name):
    """The audio report on disk — only if it was made from the sentence files as they are now (preview)."""
    a_dir = os.path.join(ep_dir, "audio")
    qj, tj = os.path.join(a_dir, "audio_qc.json"), os.path.join(a_dir, "timing.json")
    if not (os.path.exists(qj) and os.path.exists(tj)):
        return None, "audio_qc.json · timing.json 없음 (아직 잇지 않음)"
    wavs = [os.path.join(ep_dir, "audio_in", f"{name}_{r['id']}.wav") for r in rows]
    if not all(os.path.exists(w) for w in wavs):
        return None, "문장 파일이 다 있지 않음"
    if os.path.getmtime(tj) < max(os.path.getmtime(w) for w in wavs) or os.path.getmtime(qj) < os.path.getmtime(tj):
        return None, "audio_qc.json 이 지금 문장 파일보다 옛 판"
    try:
        q = json.load(open(qj, encoding="utf-8"))
    except (OSError, ValueError):
        return None, "audio_qc.json 을 못 읽음"
    if [r.get("id") for r in q.get("rows", [])] != [r["id"] for r in rows] or "joins" not in q:
        return None, "audio_qc.json 의 문장 목록 · 이음매가 지금 대본과 다름"
    return q, "지금 문장 파일과 같은 판"


def _prep_real(bgm, bgm_lufs):
    def f(ep_dir, ep):
        return A.prep(ep, ep_dir, bgm=bgm, bgm_lufs=bgm_lufs)
    return f


def _qc_real(ep_dir, ep):
    md = A.qc(ep, ep_dir)
    return json.load(open(md[:-3] + ".json", encoding="utf-8"))


def voice_auto(ep_dir, ep, rounds=ROUNDS, takes=TAKES, budget_x=BUDGET_X, run=False, caller=None, measure=None,
               prep_fn=None, qc_fn=None, sleep=time.sleep, bgm=None, bgm_lufs=-28.0, now=None):
    """Returns the state dict (stop · ask · decisions · rounds_done · remaining · candidates · chars · report_md …)."""
    T.guard(ep_dir, ep)                                     # internal (공개 금지) = SystemExit before anything else
    if rounds < 0 or takes < 1 or not (isinstance(budget_x, (int, float)) and math.isfinite(budget_x) and budget_x > 0):
        raise SystemExit(f"--rounds ≥ 0 · --takes ≥ 1 · --budget-x = 유한한 양수 (지금 {rounds} · {takes} · {budget_x})")
    prep_fn = prep_fn or _prep_real(bgm, bgm_lufs)
    qc_fn = qc_fn or _qc_real
    rows = T.plan(ep_dir, ep, T.BASE_TEMPO, T.MODE)          # sheet ↔ scenes.json must match (else SystemExit)
    by = {r["id"]: r for r in rows}
    name = ep["episode"].split("_")[0]
    in_dir = os.path.join(ep_dir, "audio_in")
    led_path = os.path.join(in_dir, "typecast_ledger.json")

    def path(i):
        return os.path.join(in_dir, f"{name}_{i}.wav")
    led = _load_ledger(led_path)
    chars_all = sum(r["chars"] for r in rows)
    st = dict(episode=ep["episode"], when=now or _kst(), run=bool(run), rounds=rounds, takes=takes, budget_x=budget_x,
              chars_all=chars_all, budget=int(chars_all * budget_x), spent0=_spent(led), spent1=None, sent_now=0, left=None,
              decisions=[], ask=[], notes=[], stop=None, rounds_done=0, to_make=0, made=[], q_first=None, q_last=None,
              remaining=[], candidates=[], other_joins=[], hand=[], report_path=None)
    rules = st["rules"] = _rules(st)
    # voice / model as in the ledger (a voice change is not this command's decision)
    bad = [(r["id"], e.get("voice_id"), e.get("model")) for r in rows for e in [led["lines"].get(r["id"])]
           if e and e.get("status") == "ok" and os.path.exists(path(r["id"]))
           and (e.get("voice_id") != T.VOICE_ID or e.get("model") != T.MODEL)]
    if bad:
        _dec(st, f"목소리 · 모델이 원장과 다른 줄 {len(bad)} ({' · '.join(b[0] for b in bad[:8])}) — 다시 만들지 않음",
             rules["voice"], f"원장 {bad[0][1]} · {bad[0][2]} ↔ 지금 {T.VOICE_ID} · {T.MODEL}")
        st["stop"] = "voice"
        st["ask"].append("목소리 · 모델을 바꾸나? (바꾸면 그 줄들을 새 목소리로 다시 만든다 — 예산 · 톤 섞임 확인)")
        return _finish(st, ep_dir, rows, led_path)
    # ① what to make
    _, todo, stale = T.run(ep_dir, ep, run_all=True, dry=True, base_tempo=T.BASE_TEMPO, mode=T.MODE)
    st["hand"] = hand = [r["id"] for r in stale if r["id"] not in led["lines"]]     # a wav the ledger never saw
    mk = {r["id"] for r in todo + stale} - set(hand)
    make = [r for r in rows if r["id"] in mk]
    if hand:
        _dec(st, f"원장에 없는 문장 파일 {len(hand)} ({' · '.join(hand[:8])}) — 손으로 넣은 판으로 보고 그대로 둔다", rules["hand"])
        st["ask"].append(f"원장에 없는 문장 파일 {len(hand)} 개 ({' · '.join(hand[:8])}) — 손으로 넣은 판이면 그대로 · API 로 다시 "
                         f"만들려면 `avi.py typecast EP --run --lines {','.join(hand[:8])} --force`")
    need1 = sum(r["chars"] for r in make)
    st["to_make"] = len(make)
    why = [(r["id"], _why_make(r, led["lines"].get(r["id"]), path(r["id"]))) for r in make]
    _dec(st, f"① 다시 만들 줄 {len(make)}" + (f" ({_group_ids(why)})" if make else "") + f" · 그대로 {len(rows) - len(make)}",
         rules["make"], f"글자 {need1}")
    fits = st["spent0"] + need1 <= st["budget"]
    _dec(st, "예산 확인 (① 전)", rules["budget"],
         f"원장 {st['spent0']} + {need1} = {st['spent0'] + need1} {'≤' if fits else '>'} {st['budget']}")
    if not fits:
        st["ask"].append(f"① 만 해도 글자 예산 {st['budget']} 을 넘는다 (원장 {st['spent0']} + {need1}) — 예산을 늘릴까?")
    if not run:
        return _preview(st, ep_dir, ep, rows, led, led_path, name, make)
    if not fits:
        st["stop"] = "budget"
        return _finish(st, ep_dir, rows, led_path)
    guard = BudgetGuard(caller or T._call, st["budget"], st["spent0"])
    gsleep = guard.sleep_fn(sleep)
    if make:
        s1, _, _ = T.run(ep_dir, ep, ids=[r["id"] for r in make], force=True, dry=False, base_tempo=T.BASE_TEMPO,
                         mode=T.MODE, caller=guard, sleep=gsleep)
        st["made"] = list(s1.get("made") or [])
        if s1.get("failed"):
            led = _load_ledger(led_path)
            errs = [(i, ((led["lines"].get(i) or {}).get("error") or "")[:120]) for i in s1["failed"]]
            _dec(st, f"① 만들지 못한 줄 {len(errs)} ({' · '.join(f'{i} {e}' for i, e in errs[:4])}) — prep · qc 안 함",
                 rules["stop"], f"만든 {len(st['made'])} · 실패 {len(errs)}")
            if guard.blocked:
                st["stop"] = "budget"
                st["ask"].append("서버 오류 다시 시도로 글자가 늘어 예산에 닿았다 — 예산을 늘릴까?")
            else:
                st["stop"] = "fail"
                hint = " (403 = 결제 · 계정 상태 확인)" if any("403" in e for _, e in errs) else ""
                st["ask"].append(f"API 실패 {len(errs)} 줄{hint} — 원인을 풀고 다시 부르면 실패한 줄만 만든다")
            return _finish(st, ep_dir, rows, led_path, guard=guard)
    # ② ③
    prep_fn(ep_dir, ep)
    q = qc_fn(ep_dir, ep)
    st["q_first"] = _qs(q)
    _dec(st, "② ③ 음성 잇기 · 이음매 점검", rules["jump"], _fmt_q(st["q_first"]))
    logged_cap = set()
    for k in range(1, rounds + 1):
        if not _qs(q)["jumps"]:
            st["stop"] = "no_jumps"
            break
        led = _load_ledger(led_path)
        tg = T.pick_targets(q.get("rows", []), q.get("joins", []))
        go = [i for i in tg if i not in hand and T.retake_rounds(led, i) < rounds]
        _log_skipped(st, [i for i in tg if i not in go and i not in logged_cap], hand, led, logged_cap)
        if not go:
            st["stop"] = "no_targets"
            break
        need = sum(by[i]["chars"] for i in go) * takes
        if guard.total + need > st["budget"]:
            _dec(st, f"다시 찍기 {k} 회 안 함: {' · '.join(go)}", rules["budget"],
                 f"원장 {guard.total} + {need} = {guard.total + need} > {st['budget']}")
            st["stop"] = "budget"
            st["ask"].append(f"다시 찍기 {k} 회 (글자 {need}) 가 예산 {st['budget']} 을 넘는다 — 예산을 늘릴까, 남은 뜀을 둘까?")
            break
        _dec(st, f"다시 찍기 {k} 회: {' · '.join(go)} (판 {takes} 개씩)", rules["target"], f"글자 {need}")
        res = T.retake(ep_dir, ep, go, takes=takes, base_tempo=T.BASE_TEMPO, mode=T.MODE, caller=guard, measure=measure,
                       sleep=gsleep)
        st["rounds_done"] = k
        for x in res:
            if x.get("chosen") is None:
                _dec(st, f"{x['id']}: 다시 찍지 못함 — {x.get('error')}", rules["pick"])
                continue
            pick = "지금 판 그대로 (새 판이 더 멂)" if x.get("kept_current") else f"판 t{x['chosen']} 고름"
            hz = " · ".join(f"{h:g}" for h in (x.get("takes_hz") or []) if h)
            _dec(st, f"{x['id']}: {pick}" + (f" (일부 실패: {x['error']})" if x.get("error") else ""), rules["pick"],
                 f"이웃과 차 {_sg(x.get('dev_before_st'))} → {_sg(x.get('dev_after_st'))} 반음 "
                 f"(지금 판 · 새 판 {hz} Hz · 이웃 {x.get('ref_hz')} Hz)")
        prep_fn(ep_dir, ep)
        q2 = qc_fn(ep_dir, ep)
        a_, b_ = _qs(q), _qs(q2)
        _dec(st, f"이음매 다시 ({k} 회 뒤)", rules["jump"],
             f"뜀 {a_['jumps']} → {b_['jumps']} · 최대 {a_['max']} → {b_['max']} · 95 % {a_['p95']} → {b_['p95']} 반음")
        q = q2
        if guard.blocked:
            st["stop"] = "budget"
            st["ask"].append("다시 찍기 중 예산에 닿아 일부 판을 만들지 않았다 — 예산을 늘릴까?")
            break
    else:
        st["stop"] = "no_jumps" if not _qs(q)["jumps"] else "rounds"
    st["q_last"] = _qs(q)
    return _finish(st, ep_dir, rows, led_path, q=q, guard=guard, bgm=bgm)


def _preview(st, ep_dir, ep, rows, led, led_path, name, make):
    st["stop"] = "preview"
    rules = st["rules"]
    by = {r["id"]: r for r in rows}
    q, why = _qc_current(ep_dir, rows, name)
    if make:
        st["notes"].append("① 로 바뀌는 문장이 있어 이음매는 --run 이 다시 잰다 — 아래 이음매는 지금 파일 기준 (참고)")
    if q is None:
        _dec(st, "지금 이음매 = 모름", rules["jump"], why)
        return _finish(st, ep_dir, rows, led_path, write=False)
    st["q_last"] = _qs(q)
    _dec(st, f"지금 이음매 (audio/audio_qc.json · {why})", rules["jump"], _fmt_q(st["q_last"]))
    tg = T.pick_targets(q.get("rows", []), q.get("joins", []))
    go = [i for i in tg if i not in st["hand"] and T.retake_rounds(led, i) < st["rounds"]]
    _log_skipped(st, [i for i in tg if i not in go], st["hand"], led, set())
    if go:
        need = sum(by[i]["chars"] for i in go) * st["takes"]
        after1 = st["spent0"] + sum(r["chars"] for r in make)
        worst = after1 + need * st["rounds"]
        _dec(st, f"--run 이면 다시 찍기 1 회 대상: {' · '.join(go)} (판 {st['takes']} 개씩)", rules["target"],
             f"글자 {need} · {st['rounds']} 회 다 가면 원장 {worst} {'≤' if worst <= st['budget'] else '>'} 예산 {st['budget']}")
        if worst > st["budget"]:
            st["notes"].append("다시 찍기를 다 가면 예산을 넘을 수 있다 — --run 은 그 회 전에 멈추고 묻는다")
    return _finish(st, ep_dir, rows, led_path, q=q, write=False)


def _finish(st, ep_dir, rows, led_path, q=None, guard=None, bgm=None, write=True):
    led = _load_ledger(led_path)
    if q is not None:
        st["remaining"] = _remaining(q, led, st["hand"])
        st["candidates"] = _candidates(st["remaining"], q, led, rows, st["rounds"])
        st["other_joins"] = [dict(a=j["a"], b=j["b"], t=j.get("t"), why=j.get("why"))
                             for j in q.get("joins", []) if not j.get("jump") and j.get("why")]
    total = _spent(led)
    if guard is not None:
        st["sent_now"] = guard.sent
        total = max(total, guard.total)
    st["spent1"] = total
    st["left"] = st["budget"] - total
    a_dir = os.path.join(ep_dir, "audio")
    mix, narr = os.path.join(a_dir, "mix.wav"), os.path.join(a_dir, "narration.wav")
    if st["run"] and not bgm and os.path.exists(mix) and os.path.exists(narr) and os.path.getmtime(mix) < os.path.getmtime(narr):
        st["notes"].append("audio/mix.wav 가 새 narration.wav 보다 옛 판 — 음악을 쓰면 렌더 전에 `audio-prep --bgm …` 을 다시")
    st["report_md"] = _report_md(st)
    if write and st["run"]:
        os.makedirs(a_dir, exist_ok=True)
        p = os.path.join(a_dir, REPORT_MD)
        with open(p, "w", encoding="utf-8") as f:
            f.write(st["report_md"])
        with open(os.path.join(a_dir, REPORT_JSON), "w", encoding="utf-8") as f:
            json.dump({k: v for k, v in st.items() if k != "report_md"}, f, ensure_ascii=False, indent=1)
        st["report_path"] = p
        dp = os.path.join(ep_dir, "DECISIONS.md")
        head = "" if os.path.exists(dp) else "# 결정 기록\n\n"
        tail = "" if (not os.path.exists(dp) or open(dp, encoding="utf-8").read().endswith("\n")) else "\n"
        with open(dp, "a", encoding="utf-8") as f:
            f.write(head + tail + _decisions_line(st) + "\n")
    return st


def _decisions_line(st):
    qf, ql = st.get("q_first"), st.get("q_last")
    jumps = (f"높이 뜀 {qf['jumps']} → {ql['jumps']} (최대 {qf['max']} → {ql['max']} 반음)" if qf and ql else "이음매 안 잼")
    cands = " · ".join(c["id"] for c in st["candidates"]) or "없음"
    ask = (" · ⚠ 1저자에게 묻기: " + " / ".join(st["ask"])) if st["ask"] else ""
    return (f"- {st['when']} voice-auto (자동 · 문정 smart 1.0): ① 다시 만듦 {len(st['made'])} · 다시 찍기 {st['rounds_done']} 회 · "
            f"{jumps} · 글자 +{st['sent_now']} (원장 {st['spent1']} / 예산 {st['budget']}) · 끝말 고침 후보 {cands} · "
            f"멈춤 = {STOP[st['stop']].format(rounds=st['rounds']).split(' — ')[0]} · 보고 `audio/{REPORT_MD}`{ask}")


def _report_md(st):
    jst = f"{A.JOIN_JUMP_ST:g}"
    pre = st["stop"] == "preview"
    L = [f"# 음성 자동 판단 — {st['episode']} ({st['when']})", ""]
    if pre:
        L += ["> **미리 보기** — API 호출 0 · 파일 안 씀.  `--run` 을 붙이면 아래 차례대로 한다.", ""]
    L.append(f"- 설정: 목소리 문정 (`{T.VOICE_ID}` · `{T.MODEL}`) · smart (앞뒤 문장) · 빠르기 {T.BASE_TEMPO:.1f} · 톤 안 섞음 · "
             f"다시 찍기 최대 {st['rounds']} 회 × {st['takes']} 판")
    qf, ql = st.get("q_first"), st.get("q_last")
    if qf and ql and not pre:
        L.append(f"- 결과: 높이 뜀 {qf['jumps']} → {ql['jumps']} · 최대 {qf['max']} → {ql['max']} · 95 % {qf['p95']} → {ql['p95']} 반음")
    elif ql:
        L.append(f"- 지금: {_fmt_q(ql)}")
    L.append(f"- 멈춘 까닭: {STOP[st['stop']].format(rounds=st['rounds'])}")
    L.append(f"- 쓴 글자: 이번 {st['sent_now']} · 원장 전체 {st['spent0']} → {st['spent1']} / 예산 {st['budget']} "
             f"(대본 {st['chars_all']} × {st['budget_x']:g}) · 남은 예산 {st['left']}")
    L.append("- 1저자에게 물을 것: " + (" / ".join(st["ask"]) if st["ask"] else "없음"))
    L += [f"- ⚠ {n}" for n in st["notes"]]
    L += ["", "## 판단 (차례대로 · 판단마다 한 줄)", "", "| # | 무엇 | 규칙 | 숫자 전 → 뒤 |", "|---|---|---|---|"]
    L += [f"| {d['no']} | {_cell(d['what'])} | {_cell(d['rule'])} | {_cell(d['nums'])} |" for d in st["decisions"]]
    rem = st["remaining"]
    L += ["", f"## 남은 뜀 ({len(rem)})", ""]
    if rem:
        L += ["| 시각 (앞 문장 끝) | 앞 → 뒤 | 높이 차 반음 | 크기 | 다시 찍을 문장 (이웃에서 먼 쪽) · 다시 찍은 횟수 |",
              "|---|---|---|---|---|"]
        L += [f"| {_tfmt(x['t'])} | {x['a']} → {x['b']} | {x['d_st']} | {x['size']} | {x['target']} · "
              f"{'손 판 (원장 없음)' if x['hand'] else str(x['target_rounds']) + ' 회'} |" for x in rem]
        L.append(f"- 크기: 작은 = {jst}–{SMALL_JUMP_ST:g} 반음 · 큰 = ≥ {SMALL_JUMP_ST:g} — 끝말을 고친 뒤에도 남은 작은 뜀은 그대로 둔다 (스킬)")
    else:
        L.append("- 없음")
    cand = st["candidates"]
    L += ["", f"## 끝말 고침 후보 ({len(cand)}) — 다시 찍기 {st['rounds']} 회를 다 썼는데 아직 ≥ {jst} 반음", ""]
    if cand:
        L += ["| 문장 | 끝말 꼴 | 차분한 꼴 예 | 이웃과 높이 차 반음 | 뜀 최대 (크기) | 다시 찍기 회 (새 판) | 글 |",
              "|---|---|---|---|---|---|---|"]
        L += [f"| {c['id']} | {c['ending']} | {_cell(c['hint'])} | {_sg(c['dev_st'])} | {c['jump_max_st']} ({c['size']}) | "
              f"{c['rounds']} ({c['takes']}) | {_cell(c['text'])} |" for c in cand]
        L.append("- 명령은 글을 고치지 않는다 — 고침 = 스킬을 따르는 조수가 `build_scenes.py` 에서 끝말만 (뜻이 그대로일 때만) → "
                 "`avi.py tts` → `avi.py plan` → voice-auto 한 번 더 (그 문장 + 앞뒤가 원장과 안 맞게 되어 다시 만든다 · 다시 찍기 횟수는 0 부터)")
    else:
        L.append("- 없음")
    oth = st["other_joins"]
    if oth:
        L += ["", f"## 그 밖의 이음매 알림 ({len(oth)}) — 다시 찍기로는 못 고친다 (글 · 쉼)", ""]
        L += [f"- {_tfmt(j['t'])} {j['a']} → {j['b']}: {' · '.join(j['why'] or [])}" for j in oth]
    L += ["", "## 한계 (미확인)", "",
          "- 높이 차 = 귀의 대리 지표 — 듣기 확인은 1저자",
          "- 두 높이 측정법의 차 ≤ 1.05 반음 (다시 찍기에서 판을 고를 때 = 문장 파일마다 · 이음매 점검 = 이어 붙인 음성 · ep01 대조)",
          f"- 문턱 {jst} 반음 · 작은 뜀 < {SMALL_JUMP_ST:g} 반음 = ep01 경험값 (표준 아님)",
          "- 글자 = 보낸 글 (공백 포함) 의 합 · 실패한 호출도 셈 — Typecast 가 실제로 무엇을 세는지는 요금 화면으로 확인"]
    return "\n".join(L) + "\n"


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ep")
    ap.add_argument("--run", action="store_true", help="call the API and write the report (default = preview: 0 calls · nothing written)")
    ap.add_argument("--rounds", type=int, default=ROUNDS, help=f"retake rounds per sentence version (default {ROUNDS})")
    ap.add_argument("--takes", type=int, default=TAKES, help=f"new takes per retaken sentence per round (default {TAKES})")
    ap.add_argument("--budget-x", type=float, default=BUDGET_X,
                    help=f"character budget = script characters x this, whole episode (default {BUDGET_X:g})")
    ap.add_argument("--bgm", help="music bed for audio-prep (optional)")
    ap.add_argument("--bgm-lufs", type=float, default=-28.0)
    a = ap.parse_args(argv)
    ep = json.load(open(os.path.join(a.ep, "scenes.json"), encoding="utf-8"))
    st = voice_auto(a.ep, ep, rounds=a.rounds, takes=a.takes, budget_x=a.budget_x, run=a.run, bgm=a.bgm, bgm_lufs=a.bgm_lufs)
    print(st["report_md"])
    if st.get("report_path"):
        print("wrote", st["report_path"], "and DECISIONS.md (one line)")
    return 2 if st["ask"] else 0


def selftest():
    """Fake API · fake pitch measurement (same pattern as the typecast retake test) · fake prep · qc built on the real
    joins() + pick_targets().  Nothing leaves the machine; the temp folder under avi_work/selftest is removed at the end."""
    import shutil
    import struct
    import tempfile
    import avi_audio as A
    base = os.path.join(WORK, "selftest")
    os.makedirs(base, exist_ok=True)
    root = tempfile.mkdtemp(prefix="voiceauto_", dir=base)
    try:
        return _selftest_body(root, shutil, struct, A)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def _selftest_body(root, shutil, struct, A):
    ok = []

    def check(name_, fn):
        try:
            ok.append((name_, bool(fn())))
        except BaseException as ex:                                # noqa: BLE001 — a crash (or SystemExit) is a FAIL
            ok.append((f"{name_}  [{type(ex).__name__}: {ex}]", False))

    def fake_wav(sec):
        buf = io.BytesIO()
        with wave.open(buf, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(32000)
            w.writeframes(struct.pack("<h", 0) * int(sec * 32000))
        return buf.getvalue()

    texts0 = ["가 문장입니다.", "나 문장이에요.", "다 문장이죠.", "라 문장이거든요.", "마 문장인 거죠.", "바 문장입니다."]

    class Sc:
        """One fake episode: fake API (F0 per sentence per call) · measure = F0 of a file · prep / qc counters."""

        def __init__(self, name, f0_seq=None, texts=texts0, episode="ep97_test"):
            self.d = os.path.join(root, name)
            os.makedirs(self.d)
            self.episode, self.f0_seq, self.calls, self.f0_of, self.n = episode, dict(f0_seq or {}), [], {}, 0
            self.prep_n = self.qc_n = 0
            self.write(texts)

        def write(self, texts):
            self.ep = dict(episode=self.episode, title="시험", scenes=[dict(id="s01", lines=[
                dict(id=f"s01_l{k + 1:02d}", say=t, text=t) for k, t in enumerate(texts)])])
            with open(os.path.join(self.d, "scenes.json"), "w", encoding="utf-8") as f:
                json.dump(self.ep, f, ensure_ascii=False)
            with open(os.path.join(self.d, "tts_typecast.tsv"), "w", encoding="utf-8") as f:
                f.write("장면 번호\t문장 번호\t문장 (읽는 꼴)\t뒤 쉼 (초)\t빠르기 (1.0 기준 배수)\t감정\t강조 낱말\t메모\n")
                for k, t in enumerate(texts):
                    f.write(f"S01\t{k + 1:02d}\t{t}\t0.45\t1.00\t차분\t\t\n")
            return self.ep

        def api(self, r):
            self.calls.append(dict(r))
            k = sum(1 for c in self.calls if c["id"] == r["id"]) - 1
            seq = self.f0_seq.get(r["id"], [200.0])
            hz = seq[min(k, len(seq) - 1)]
            self.n += 1
            data = fake_wav(1.0 + self.n / 1e4)                       # distinct bytes per call
            self.f0_of[hashlib.sha256(data).hexdigest()] = hz
            return 200, "audio/wav", data

        def measure(self, path):
            return self.f0_of[T._sha(path)]

        def path(self, i):
            return os.path.join(self.d, "audio_in", f"{self.episode.split('_')[0]}_{i}.wav")

        def ledger(self):
            return json.load(open(os.path.join(self.d, "audio_in", "typecast_ledger.json"), encoding="utf-8"))

        def prep(self, ep_dir, ep):
            self.prep_n += 1

        def qc(self, ep_dir, ep):
            self.qc_n += 1
            sheet = T.read_sheet(ep_dir)
            rows = [dict(id=r["id"], f0_med=self.measure(self.path(r["id"])), pause_after=r["pause"]) for r in sheet]
            lid = {ln["id"]: ln for sc in ep["scenes"] for ln in sc["lines"]}
            js = A.joins(rows, lid, self.ledger().get("lines", {}), {r["id"]: 1.5 * (k + 1) for k, r in enumerate(rows)})
            dd = sorted(abs(j["d_st"]) for j in js if j["d_st"] is not None)
            return dict(summary=dict(join_n=len(js), join_jumps=sum(1 for j in js if j["jump"]),
                                     join_max_st=round(dd[-1], 2) if dd else None,
                                     join_p95_st=round(dd[min(len(dd) - 1, int(0.95 * len(dd)))], 2) if dd else None),
                        rows=rows, joins=js)

        def va(self, **kw):
            kw.setdefault("caller", self.api)
            kw.setdefault("measure", self.measure)
            kw.setdefault("prep_fn", self.prep)
            kw.setdefault("qc_fn", self.qc)
            kw.setdefault("sleep", lambda s: None)
            return voice_auto(self.d, self.ep, **kw)

        def files(self):
            return sorted((os.path.relpath(os.path.join(dp, f), self.d), T._sha(os.path.join(dp, f)))
                          for dp, _, fs in os.walk(self.d) for f in fs)

        def report(self):
            return open(os.path.join(self.d, "audio", "voice_auto_report.md"), encoding="utf-8").read()

    ids = [f"s01_l{k:02d}" for k in range(1, 7)]
    st = {}
    # A — smooth episode: preview · first run · one sentence changed
    a = Sc("a_smooth")
    st["a_files0"] = a.files()
    check("미리 보기 (기본) = API 호출 0 · prep · qc 0 · 파일 안 씀 · 할 일 6 줄",
          lambda: (st.__setitem__("a0", a.va()) or True) and not a.calls and a.prep_n == a.qc_n == 0
          and a.files() == st["a_files0"] and st["a0"]["stop"] == "preview" and st["a0"]["to_make"] == 6)
    def cli_preview():
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main([a.d])
        return rc == 0 and not a.calls and a.files() == st["a_files0"] and "미리 보기" in buf.getvalue()
    check("CLI 기본 = 미리 보기 (rc 0 · 호출 0 · 파일 안 씀)", cli_preview)
    check("첫 --run: 여섯 줄 만들고 뜀 0 → 다시 찍기 없이 멈춤 · 보고 · DECISIONS.md 한 줄",
          lambda: (st.__setitem__("a1", a.va(run=True)) or True) and len(a.calls) == 6 and st["a1"]["stop"] == "no_jumps"
          and a.prep_n == 1 and a.qc_n == 1 and st["a1"]["rounds_done"] == 0 and "## 판단" in a.report()
          and sum(1 for ln in open(os.path.join(a.d, "DECISIONS.md"), encoding="utf-8") if "voice-auto" in ln) == 1)
    st["a_sha"] = {i: (T._sha(a.path(i)) if os.path.exists(a.path(i)) else None) for i in ids}
    a.write([t if k != 2 else "다 문장을 바꿨죠." for k, t in enumerate(texts0)])
    n0 = len(a.calls)
    check("★ 멀쩡한 판은 다시 찍지 않는다 — 글 하나 바꾸면 그 문장 + 앞뒤만 (원장과 안 맞는 줄) · 까닭이 보고에",
          lambda: (st.__setitem__("a2", a.va(run=True)) or True)
          and sorted(c["id"] for c in a.calls[n0:]) == ["s01_l02", "s01_l03", "s01_l04"]
          and all(T._sha(a.path(i)) == st["a_sha"][i] for i in ("s01_l01", "s01_l05", "s01_l06"))
          and st["a2"]["stop"] == "no_jumps" and "글 바뀜" in a.report() and "앞뒤 문장 바뀜" in a.report())
    # B — one stubborn sentence (always 290 Hz between 200 Hz neighbours) until its ending is changed
    b = Sc("b_stubborn", f0_seq={"s01_l04": [290.0] * 5 + [200.0]})
    check("★ 다시 찍기는 --rounds 번까지: 늘 튀는 문장 = 2 회 × 2 판 = 호출 4 → 멈춤 (rounds) · prep · qc 3 번",
          lambda: (st.__setitem__("b1", b.va(run=True)) or True) and len(b.calls) == 10
          and sum(1 for c in b.calls if c["id"] == "s01_l04") == 5 and st["b1"]["stop"] == "rounds"
          and st["b1"]["rounds_done"] == 2 and b.prep_n == 3 and b.qc_n == 3)
    check("★ 끝말 고침 후보 = 다시 찍기 2 회를 다 썼는데 아직 ≥ 2.5 반음 · 끝말 꼴 '~거든요' (명령은 글을 안 고침)",
          lambda: [c["id"] for c in st["b1"]["candidates"]] == ["s01_l04"] and st["b1"]["candidates"][0]["ending"] == "~거든요"
          and b.ep["scenes"][0]["lines"][3]["say"] == "라 문장이거든요."
          and "라 문장이거든요." in open(os.path.join(b.d, "tts_typecast.tsv"), encoding="utf-8").read())
    check("★ 보고 파일: 판단마다 한 줄 (규칙 · 숫자 전 → 뒤) · 남은 뜀 · 끝말 후보 · 쓴 글자 · 남은 예산",
          lambda: all(s in b.report() for s in ("## 판단", "원장과 안 맞는 줄만", "이웃 기하평균", "## 남은 뜀 (2)",
                                                 "## 끝말 고침 후보 (1)", "~거든요", "쓴 글자", "남은 예산", "→"))
          and f"이번 {sum(c['chars'] for c in b.calls)}" in b.report())
    n0b = len(b.calls)
    check("★ 다시 부르면: 이미 2 회 다 쓴 문장은 다시 찍지 않는다 (호출 0) · 후보로 남김",
          lambda: (st.__setitem__("b2", b.va(run=True)) or True) and len(b.calls) == n0b and st["b2"]["stop"] == "no_targets"
          and [c["id"] for c in st["b2"]["candidates"]] == ["s01_l04"])
    b.write([t if k != 3 else "라 문장입니다." for k, t in enumerate(texts0)])
    n0b = len(b.calls)
    check("★ 끝말을 고치면 (조수가 글을 바꿈) 그 문장 + 앞뒤만 다시 · 다시 찍기 횟수는 0 부터",
          lambda: (st.__setitem__("b3", b.va(run=True)) or True)
          and sorted(c["id"] for c in b.calls[n0b:]) == ["s01_l03", "s01_l04", "s01_l05"] and st["b3"]["stop"] == "no_jumps"
          and T.retake_rounds(b.ledger(), "s01_l04") == 0)
    # C — fixed in the first round
    c = Sc("c_fixed", f0_seq={"s01_l03": [300.0, 290.0, 202.0]})
    check("★ 뜀 0 이면 멈춘다: 1 회에 고쳐지면 2 회째 없음 (호출 6 + 2) · 고른 판이 이웃 높이에 가장 가까움",
          lambda: (st.__setitem__("c1", c.va(run=True)) or True) and len(c.calls) == 8 and st["c1"]["stop"] == "no_jumps"
          and st["c1"]["rounds_done"] == 1 and c.measure(c.path("s01_l03")) == 202.0 and c.qc_n == 2)
    check("다시 찍은 문장의 숫자 전 → 뒤 (이웃과 차 반음) 가 판단 줄에",
          lambda: any(d_["what"].startswith("s01_l03") and "→" in d_["nums"] for d_ in st["c1"]["decisions"]))
    # D — budget
    d1 = Sc("d1_budget")
    check("★ 예산 넘으면 호출 없이 멈춘다 (① 이 예산보다 큼) · 묻기 · 보고에 '예산'",
          lambda: (st.__setitem__("d1", d1.va(run=True, budget_x=0.5)) or True) and not d1.calls
          and st["d1"]["stop"] == "budget" and st["d1"]["ask"] and d1.prep_n == 0 and "예산" in d1.report())
    d2 = Sc("d2_budget", f0_seq={"s01_l04": [290.0]})
    check("★ 다시 찍기 한 회가 예산을 넘게 되면 그 회 전에 멈춘다 (다시 찍기 호출 0)",
          lambda: (st.__setitem__("d2", d2.va(run=True, budget_x=1.2)) or True) and len(d2.calls) == 6
          and st["d2"]["stop"] == "budget" and st["d2"]["ask"] and st["d2"]["rounds_done"] == 0)
    d3 = Sc("d3_guard")

    def guard_blocks():
        g = BudgetGuard(d3.api, 10, 5)
        try:
            g(dict(id="s01_l01", chars=8))
            return False
        except BudgetStop:
            pass
        s_, _, _ = T.run(d3.d, d3.ep, ids=["s01_l01"], dry=False, caller=BudgetGuard(d3.api, 3, 0), sleep=lambda s: None)
        return (not d3.calls and g.sent == 0 and s_["failed"] == ["s01_l01"] and not os.path.exists(d3.path("s01_l01"))
                and d3.ledger()["calls"] == [])
    check("★ 예산 지킴이: 넘을 호출은 보내지 않는다 (API 0 · 원장 호출 기록 0 · 글자 0) · run 은 그 줄만 실패로", guard_blocks)
    d4 = Sc("d4_retry")
    hit = []

    def api503(r):                                    # the last sentence's first try = server busy -> its retry would cross
        if r["id"] == "s01_l06" and not hit:
            hit.append(1)
            d4.calls.append(dict(r))
            raise urllib.error.HTTPError(T.URL, 503, "busy", {}, io.BytesIO(b"busy"))
        return d4.api(r)
    check("★ 다시 시도가 예산을 넘게 되면 그 호출은 보내지 않는다 (voice-auto 안의 지킴이 · 원장 글자 ≤ 예산 · 멈추고 묻기)",
          lambda: (st.__setitem__("d4", d4.va(run=True, budget_x=1.0, caller=api503)) or True) and len(d4.calls) == 6
          and st["d4"]["stop"] == "budget" and st["d4"]["ask"] and T.retake_rounds(d4.ledger(), "s01_l06") == 0
          and sum(c_["chars"] for c_ in d4.ledger()["calls"]) <= st["d4"]["budget"] == 49 and d4.prep_n == 0
          and not os.path.exists(d4.path("s01_l06")))
    # E — internal
    e1 = Sc("internal")
    e2 = Sc("e_name", episode="ep97internal_test")

    def refused(sc):
        try:
            sc.va(run=True)
            return False
        except SystemExit:
            return not sc.calls
    check("내부판 거부 (폴더 이름 internal · 에피소드 이름) — 호출 0", lambda: refused(e1) and refused(e2))
    # F — API failure in ①
    f = Sc("f_fail")

    def api403(r):
        if r["id"] == "s01_l02":
            f.calls.append(dict(r))
            raise urllib.error.HTTPError(T.URL, 403, "forbidden", {}, io.BytesIO(b'{"message":"UNUSUAL_ACTIVITY_DETECTED"}'))
        return f.api(r)
    check("★ ① 에서 API 가 실패하면 prep · qc 전에 멈추고 묻는다 (403 = 결제 · 계정 확인)",
          lambda: (st.__setitem__("f1", f.va(run=True, caller=api403)) or True) and st["f1"]["stop"] == "fail"
          and f.prep_n == 0 and st["f1"]["ask"] and "403" in f.report())
    # G — old ledger (no retake counter): rounds = retake call sessions after the current file was made
    made = "2026-11-24 14:42:38"
    t_m = time.mktime(time.strptime(made, "%Y-%m-%d %H:%M:%S"))
    led_old = dict(lines={"x": dict(status="ok", made=made)}, calls=[
        dict(id="x", chars=9, status=200, t=t_m - 100, take=1), dict(id="x", chars=9, status=200, t=t_m - 99, take=2),
        dict(id="x", chars=9, status=200, t=t_m + 300, take=3), dict(id="x", chars=9, status=200, t=t_m + 301, take=4),
        dict(id="x", chars=9, status=200, t=t_m + 450, take=5), dict(id="x", chars=9, status=200, t=t_m + 451, take=6)])
    check("옛 원장 (횟수 칸 없음): 지금 판이 만들어진 뒤 다시 찍기 호출 묶음 = 횟수 (그 전 글의 판은 안 셈)",
          lambda: T.retake_counts(led_old, "x") == (2, 4) and T.retake_rounds(led_old, "x") == 2)
    # H — the ledger says another voice
    h = Sc("h_voice")

    def voice_changed():
        h.va(run=True)
        led = h.ledger()
        led["lines"]["s01_l01"]["voice_id"] = "tc_other_voice"
        with open(os.path.join(h.d, "audio_in", "typecast_ledger.json"), "w", encoding="utf-8") as fh:
            json.dump(led, fh, ensure_ascii=False)
        n_ = len(h.calls)
        r_ = h.va(run=True)
        return len(h.calls) == n_ and r_["stop"] == "voice" and r_["ask"]
    check("원장의 목소리가 지금 설정과 다르면 다시 만들지 않고 묻는다 (목소리 바꿈 = 1저자)", voice_changed)
    # I — a wav with no ledger entry (e.g. made by hand in the Typecast screen) is never overwritten or retaken
    hi = Sc("i_hand", f0_seq={"s01_l03": [290.0]})
    os.makedirs(os.path.join(hi.d, "audio_in"), exist_ok=True)
    hand = fake_wav(1.2345)
    with open(hi.path("s01_l03"), "wb") as fh:
        fh.write(hand)
    hi.f0_of[hashlib.sha256(hand).hexdigest()] = 290.0                 # it even jumps — still not touched
    st["i_sha"] = T._sha(hi.path("s01_l03"))
    check("★ 원장에 없는 파일 (손으로 넣은 판) = 덮어쓰지도 다시 찍지도 않고 묻는다 · 나머지는 진행",
          lambda: (st.__setitem__("i1", hi.va(run=True)) or True) and "s01_l03" not in [c_["id"] for c_ in hi.calls]
          and len(hi.calls) == 5 and T._sha(hi.path("s01_l03")) == st["i_sha"] and st["i1"]["ask"]
          and st["i1"]["stop"] == "no_targets" and "손" in hi.report())

    def bad_args():
        n_ = len(hi.calls)
        for kw in (dict(budget_x=float("inf")), dict(budget_x=float("nan")), dict(budget_x=0), dict(takes=0), dict(rounds=-1)):
            try:
                hi.va(run=True, **kw)
                return False
            except SystemExit:
                pass
        return len(hi.calls) == n_
    check("이상한 값 (--budget-x inf · nan · 0 · --takes 0 · --rounds -1) = 호출 전에 거부", bad_args)
    # J — the REAL audio-prep · audio-qc · per-file pitch measure on synthetic voiced audio (only the API is fake)
    jd = os.path.join(root, "j_real")
    os.makedirs(jd)
    jt = ["첫 문장은 이렇게 시작합니다.", "두 번째 문장은 조금 길게 이어서 말합니다.", "세 번째 문장이 높게 튀는 문장입니다.",
          "네 번째 문장은 다시 차분합니다.", "다섯 번째 문장도 같은 높이입니다.", "마지막 문장으로 끝을 맺습니다."]
    jep = dict(episode="ep95_real", title="시험", voice_model=dict(lead_in=0.5), end_card_s=0.5, scenes=[dict(id="s01", lines=[
        dict(id=f"s01_l{k + 1:02d}", say=t, text=t, pause_after=0.45) for k, t in enumerate(jt)])])
    with open(os.path.join(jd, "scenes.json"), "w", encoding="utf-8") as fh:
        json.dump(jep, fh, ensure_ascii=False)
    with open(os.path.join(jd, "tts_typecast.tsv"), "w", encoding="utf-8") as fh:
        fh.write("장면 번호\t문장 번호\t문장 (읽는 꼴)\t뒤 쉼 (초)\t빠르기 (1.0 기준 배수)\t감정\t강조 낱말\t메모\n")
        fh.writelines(f"S01\t{k + 1:02d}\t{t}\t0.45\t1.00\t차분\t\t\n" for k, t in enumerate(jt))
    jcalls = []

    def voiced_api(r):                                 # l03: first take ~5.6 semitones high, its second retake back in line
        import numpy as np
        jcalls.append(r["id"])
        seq = {"s01_l03": [180.0, 176.0, 131.0]}.get(r["id"], [130.0])
        y = A.synth_line(r["text"], rate=7.0, f0=seq[min(jcalls.count(r["id"]) - 1, len(seq) - 1)], seed=len(jcalls))
        tmp = os.path.join(jd, "_api.wav")
        A.write_wav(tmp, np.concatenate([np.zeros(int(0.2 * A.SR)), y, np.zeros(int(0.3 * A.SR))]), stereo=False)
        data = open(tmp, "rb").read()
        os.remove(tmp)
        return 200, "audio/wav", data
    check("★ 실제 prep · qc · 높이 측정 경로 (합성 목소리 · 가짜 API 만): 뜀 2 → 0 · 1 회에 멈춤 · narration · timing · qc · 보고",
          lambda: (st.__setitem__("j1", voice_auto(jd, jep, run=True, caller=voiced_api, sleep=lambda s: None)) or True)
          and st["j1"]["stop"] == "no_jumps" and st["j1"]["rounds_done"] == 1 and len(jcalls) == 8
          and st["j1"]["q_first"]["jumps"] == 2 and st["j1"]["q_last"]["jumps"] == 0
          and all(os.path.exists(os.path.join(jd, "audio", f_)) for f_ in
                  ("narration.wav", "timing.json", "audio_qc.json", "voice_auto_report.md", "voice_auto_report.json")))
    for name_, good in ok:
        print(("PASS " if good else "FAIL ") + name_)
    return all(g for _, g in ok)


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(0 if selftest() else 1)
    sys.exit(main())
