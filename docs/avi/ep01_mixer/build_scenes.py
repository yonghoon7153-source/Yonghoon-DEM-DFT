#!/usr/bin/env python3
"""Episode 01 (mixer) builder -> scenes.json (the canonical renderer input).

Narration rules (see ../README.md): one idea per sentence, mostly <= 40
syllables, varied endings, numbers in reading form in `say`, no symbols in
`say`.  Every on-screen number carries a `source` element on the same shot.
Run:  python3 -I build_scenes.py   (writes scenes.json next to this file)

v2 (2026-11-24 · 1저자 "믹서 avi에 지금 내용도 추가해봐"): new S10 = our lab's comparison design only
(same start · only the active-material surface stickiness differs · two counts · why) — no result, number,
direction or simulation picture; old S10 -> S11; source-line word '판독값' -> '그림에서 읽은 값' (lint).
v1 is kept in ./v1/.
v2.1 (2026-11-24 night · 1저자 Q5 "권고대로"): S07 l07 ending, two captions over 22 chars, captions without a final
period, S11 header at line start, S09 opener without the superlative.  Text only (render after the real voice).
"""
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
from korean_text import syllables  # noqa: E402

# ------------------------------------------------------------------ episode model
EP = dict(episode="ep01_mixer",
          title="가루는 왜 끼리끼리 뭉칠까",
          subtitle="전고체 배터리 양극의 건식 혼합",
          series="전고체 배터리 연구 노트",
          fps=30, width=1920, height=1080,
          voice_model=dict(base_rate=7.2, comma_pause=0.16, lead_in=0.7, caption_lead=0.2),
          caption_max_chars=22,
          end_card_s=5.5,
          thumb=dict(lines=["가루는 왜", "끼리끼리 뭉칠까"], highlight="끼리끼리", size=90, y=[308, 440], obj_w=540, obj_h=560, obj_right=16, obj_dy=20),
          scenes=[])

_cur = {}


def scene(sid, title):
    sc = dict(id=sid, title=title, lines=[], shots=[])
    EP["scenes"].append(sc)
    _cur["sc"] = sc
    _cur["n"] = 0
    return sc


def L(text, say=None, caps=None, pause=0.45, speed=1.0, emo="차분", emph=(), memo="", hide_after=False):
    sc = _cur["sc"]
    _cur["n"] += 1
    lid = f"{sc['id']}_l{_cur['n']:02d}"
    d = dict(id=lid, text=text, say=say or text, captions=caps, pause_after=pause, speed=speed,
             emotion=emo, emphasis=list(emph), memo=memo)
    if hide_after:
        d["hide_caption_after"] = True
    sc["lines"].append(d)
    return lid


def SHOT(sid, frm, elements, pre=0.35):
    sh = dict(id=sid, **{"from": frm}, pre=pre, elements=elements)
    _cur["sc"]["shots"].append(sh)
    return sh


# ------------------------------------------------------------------ element helpers
def circle(id, x, y, r, at, fill="ink", stroke=None, sw=3, label=None, ls=30, lc=None, sub=None, anim="pop", **kw):
    d = dict(id=id, type="circle", x=x, y=y, r=r, at=at, fill=fill, stroke=stroke, sw=sw, anim=anim)
    if label:
        d.update(label=label, label_size=ls)
    if lc:
        d["label_color"] = lc
    if sub:
        d.update(sublabel=sub)
    d.update(kw)
    return d


def text(id, x, y, s, at, size=28, weight="bold", color="ink", align="center", anim="fade", **kw):
    d = dict(id=id, type="text", x=x, y=y, text=s, at=at, size=size, weight=weight, color=color, align=align, anim=anim)
    d.update(kw)
    return d


def chip(id, x, y, s, at, size=28, color="ink", stroke="ink", fill=None, **kw):
    return text(id, x, y, s, at, size=size, color=color, box=dict(stroke=stroke, fill=fill, pad_x=16, pad_y=9, radius=4, sw=2),
                **kw)


def number(id, x, y, value, at, unit="", size=84, color="indigo", decimals=0, start=0.0, display=None, **kw):
    d = dict(id=id, type="number", x=x, y=y, value=value, start=start, unit=unit, size=size, color=color,
             decimals=decimals, at=at, anim="count")
    if display:
        d["display"] = display
    d.update(kw)
    return d


def src(id, s, at, y=868, x=960, align="center"):
    return dict(id=id, type="source", x=x, y=y, text=s, at=at, align=align)


def line(id, pts, at, color="ink", sw=3, arrow=None, dash=None, anim="draw", dur=0.6, **kw):
    d = dict(id=id, type="line", points=pts, at=at, color=color, sw=sw, anim=anim, dur=dur)
    if arrow:
        d["arrow"] = arrow
    if dash:
        d["dash"] = dash
    d.update(kw)
    return d


def rect(id, x, y, w, h, at, fill=None, stroke="ink", sw=2.5, radius=0, label=None, ls=28, lc=None, anim="fade", **kw):
    d = dict(id=id, type="rect", x=x, y=y, w=w, h=h, at=at, fill=fill, stroke=stroke, sw=sw, radius=radius, anim=anim)
    if label:
        d.update(label=label, label_size=ls)
    if lc:
        d["label_color"] = lc
    d.update(kw)
    return d


def dots(id, pts, at, fill="indigo", stagger=0.03, anim="pop", **kw):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    d = dict(id=id, type="dots", points=[[round(p[0], 1), round(p[1], 1), p[2]] for p in pts], at=at, fill=fill,
             stagger=stagger, anim=anim, x=round(sum(xs) / len(xs), 1), y=round(sum(ys) / len(ys), 1))
    d.update(kw)
    return d


def keep(id, **kw):
    d = dict(id=id, keep=True)
    d.update(kw)
    return d


def area(id, pts, at, fill="lavfill", **kw):
    d = dict(id=id, type="area", points=pts, at=at, fill=fill)
    d.update(kw)
    return d


def person(id, x, y, at, size=70, color="ink"):
    return dict(id=id, type="person", x=x, y=y, at=at, size=size, color=color)


def mixer(id, x, y, r, at, spin=None, **kw):
    d = dict(id=id, type="mixer", x=x, y=y, r=r, at=at, blades=4, spin=spin or [])
    d.update(kw)
    return d


# point generators ---------------------------------------------------------
def scatter(n, box, r, seed, avoid=(), mind=2.4):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    pts = []
    tries = 0
    while len(pts) < n and tries < 20000:
        tries += 1
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if any(math.hypot(x - a, y - b) < mind * r for a, b, _ in pts):
            continue
        if any(math.hypot(x - a, y - b) < R + r + 8 for a, b, R in avoid):
            continue
        pts.append((x, y, r))
    return pts


def cluster(n, cx, cy, r, seed=1, jitter=0.12):
    rnd = random.Random(seed)
    cand = []
    step = 2 * r * 0.98
    for i in range(-8, 9):
        for j in range(-8, 9):
            x = cx + step * (i + 0.5 * (j % 2))
            y = cy + step * 0.866 * j
            cand.append((math.hypot(x - cx, y - cy) + rnd.uniform(0, r * 0.6), x, y))
    cand.sort()
    out = []
    for _, x, y in cand[:n]:
        out.append((x + rnd.uniform(-jitter, jitter) * r, y + rnd.uniform(-jitter, jitter) * r, r))
    return out


def shell(n, cx, cy, R, r, a0=0.0, a1=360.0, gap=1.0, seed=None):
    out = []
    span = a1 - a0
    full = abs(span - 360) < 1e-6
    for k in range(n):
        u = k / n if full else (k / max(1, n - 1))
        a = math.radians(a0 + span * u)
        rr = R + r * gap
        out.append((cx + rr * math.cos(a), cy + rr * math.sin(a), r))
    if seed is not None:
        random.Random(seed).shuffle(out)
    return out


def along(path, r, spacing=None):
    spacing = spacing or 2 * r * 1.02
    out = []
    acc = 0.0
    for (x0, y0), (x1, y1) in zip(path[:-1], path[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        t = acc
        while t <= L:
            u = t / L
            out.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, r))
            t += spacing
        acc = t - L
    return out


# ============================================================================
# S01  도입 — 같은 가루, 다른 결과
# ============================================================================
scene("s01", "도입 — 같은 가루, 다른 결과")
a1 = L("전고체 배터리의 양극은, 두 가지 가루를 섞어서 만듭니다.",
       caps=["전고체 배터리의 양극은", "두 가지 가루를 섞어서 만듭니다"], pause=0.45, emph=["두 가지 가루"],
       memo="첫 문장 · 또박또박 · 끝을 너무 내리지 않기")
a2 = L("리튬을 담아 두는 큰 알갱이와, 이온이 지나가는 길이 되는 작은 알갱이죠.",
       caps=["리튬을 담아 두는 큰 알갱이와", "이온이 지나가는 길이 되는", "작은 알갱이죠"], pause=0.7, speed=1.03,
       emph=["큰 알갱이", "작은 알갱이"])
a3 = L("그런데 같은 재료를, 같은 비율로 섞어도요.", caps=["그런데 같은 재료를", "같은 비율로 섞어도요"],
       pause=0.35, speed=1.05, emo="가벼움", emph=["같은"], memo="'섞어도요' 끝을 살짝 올려 다음 문장으로 잇기")
a4 = L("섞는 방법만 바꾸면, 결과가 달라집니다.", caps=["섞는 방법만 바꾸면, 결과가 달라집니다"], pause=0.6,
       emph=["방법"])
a5 = L("독일의 한 연구진이, 셀을 아홉 개씩 만들어 봤는데요.", caps=["독일의 한 연구진이", "셀을 아홉 개씩 만들어 봤는데요"],
       pause=0.35, speed=1.04)
a6 = L("평균 용량은 거의 같았지만, 들쭉날쭉한 정도가 달랐어요.",
       caps=["평균 용량은 거의 같았지만", "들쭉날쭉한 정도가 달랐어요"], pause=0.5, emph=["들쭉날쭉한 정도"])
a7 = L("손으로 섞으면 5.1 %, 기계로 흔들어 섞으면 1.4 %였습니다.",
       say="손으로 섞으면 오 점 일 퍼센트, 기계로 흔들어 섞으면 일 점 사 퍼센트였습니다.",
       caps=["손으로 섞으면 5.1 %", "기계로 흔들어 섞으면 1.4 %였습니다"], pause=0.8, speed=0.92, emo="강조",
       emph=["오 점 일", "일 점 사"], memo="숫자 두 개를 천천히 · 사이에 짧은 쉼")
a9 = L("작은 가루가 큰 가루를 덮을까요, 아니면 자기들끼리 뭉칠까요?",
       caps=["작은 가루가 큰 가루를 덮을까요", "아니면 자기들끼리 뭉칠까요?"], pause=0.85, speed=0.97, emo="궁금",
       emph=["덮을까요", "뭉칠까요"], memo="두 물음을 대비 · 끝 올림")
a10 = L("오늘은 그걸 정하는 힘과, 아직 모르는 것을 차례로 보겠습니다.",
        caps=["오늘은 그걸 정하는 힘과", "아직 모르는 것을 차례로 보겠습니다"], pause=1.5,
        emph=["정하는 힘", "아직 모르는"], memo="절 끝 · 뒤 쉼 길게 (자막 숨김)")

NCM_R = 160
se_scatter = scatter(34, (1040, 330, 1420, 690), 13, seed=3)
SHOT("s01a", a1, [
    text("t_topic", 960, 205, "전고체 배터리 · 양극", a1 + "+0.2", size=26, color="grey", weight="semibold"),
    circle("ncm1", 800, 500, NCM_R, a1 + "+0.35", label="활물질", ls=36),
    dots("se1", se_scatter, a2 + "~작은", stagger=0.025),
    text("t_ncm1", 800, 705, "리튬을 담는 큰 알갱이", a2 + "+0.2", size=26, color="grey"),
    text("t_se1", 1230, 735, "이온이 지나는 작은 알갱이", a2 + "~작은", size=26, color="grey"),
], pre=0.6)
SHOT("s01b", a3, [
    keep("ncm1", x=880, y=272, scale=0.42),
    keep("se1", x=1062, y=272, scale=0.42),
    chip("c_same", 960, 400, "같은 재료 · 같은 비율", a3 + "~같은", size=28),
    line("ar_l", [(900, 432), (735, 505)], a4 + "~방법", arrow="end", sw=3),
    line("ar_r", [(1020, 432), (1185, 505)], a4 + "~방법", arrow="end", sw=3),
    rect("card_l", 700, 668, 440, 266, a4 + "~결과", stroke="ink"),
    rect("card_r", 1220, 668, 440, 266, a4 + "~결과", stroke="ink"),
    text("t_hand", 700, 572, "손으로 섞기", a4 + "~결과", size=32),
    text("t_hand2", 700, 611, "막자 · 15분", a4 + "~결과", size=24, color="grey", weight="semibold"),
    text("t_mill", 1220, 572, "기계로 흔들어 섞기", a4 + "~결과", size=32),
    text("t_mill2", 1220, 611, "진동 밀 · 30 Hz · 30분", a4 + "~결과", size=24, color="grey", weight="semibold"),
    text("t_avg_l", 700, 650, "평균 178.0 mAh/g", a6 + "~평균", size=24, color="ink", weight="semibold"),
    text("t_avg_r", 1220, 650, "평균 179.5 mAh/g", a6 + "~평균", size=24, color="ink", weight="semibold"),
    number("n_hand", 700, 742, 5.1, a7 + "~손으로", unit="%", decimals=1, size=82, color="ink"),
    number("n_mill", 1220, 742, 1.4, a7 + "~기계로", unit="%", decimals=1, size=82, color="indigo"),
    text("t_cv_l", 700, 778, "셀 9 개 용량의 흩어짐 (변동계수)", a7 + "~손으로", size=22, color="grey", weight="semibold"),
    text("t_cv_r", 1220, 778, "셀 9 개 용량의 흩어짐 (변동계수)", a7 + "~기계로", size=22, color="grey", weight="semibold"),
    src("src_kissel", "Kissel 외, Adv. Energy Mater. 15, 2405405 (2025) · 같은 재료 · 70 : 30 : 1 · 0.1 C 방전 용량", a5),
])
cover_pts = shell(26, 620, 470, 130, 12, seed=5)
clump_pts = cluster(22, 1515, 470, 12, seed=2)
SHOT("s01c", a9, [
    keep("ncm1", x=620, y=470, scale=130 / NCM_R),
    circle("q1", 960, 470, 52, a9 + "~작은", fill=None, stroke="ink", sw=2.5, dash=[9, 7], label="?", ls=44, lc="ink"),
    dots("se_cover", cover_pts, a9 + "~덮을까요", stagger=0.02),
    circle("ncm2", 1300, 470, 130, a9 + "~아니면", label="활물질", ls=32),
    dots("se_clump", clump_pts, a9 + "~뭉칠까요", stagger=0.02),
    text("t_cover", 620, 670, "덮을까?", a9 + "~덮을까요", size=36),
    text("t_clump", 1380, 670, "뭉칠까?", a9 + "~뭉칠까요", size=36),
    chip("c_q1", 760, 790, "무엇이 정하나", a10 + "~정하는", size=28, color="indigo", stroke="indigo"),
    chip("c_q2", 1160, 790, "아직 모르는 것", a10 + "~아직", size=28, color="ink", stroke="ink"),
])

# ============================================================================
# S02  양극 안
# ============================================================================
scene("s02", "양극 안 — 큰 알갱이와 작은 알갱이")
b1 = L("먼저 양극 안을 들여다볼게요.", pause=0.4, speed=1.05, emo="가벼움")
b2 = L("큰 알갱이는 활물질입니다.", pause=0.3, emph=["활물질"])
b3 = L("니켈과 코발트, 망간이 들어간 산화물 알갱이죠.", caps=["니켈과 코발트, 망간이 들어간", "산화물 알갱이죠"], pause=0.45,
       speed=1.03)
b4 = L("작은 알갱이는 황화물 고체전해질이고요.", pause=0.45, emph=["황화물 고체전해질"])
b5 = L("한 연구에서 쓴 가루를 보면, 활물질은 4.3 µm, 고체전해질은 0.7 µm였어요.",
       say="한 연구에서 쓴 가루를 보면, 활물질은 사 점 삼 마이크로미터, 고체전해질은 영 점 칠 마이크로미터였어요.",
       caps=["한 연구에서 쓴 가루를 보면", "활물질은 4.3 µm", "고체전해질은 0.7 µm였어요"], pause=0.75, speed=0.93,
       emo="강조", emph=["사 점 삼", "영 점 칠"], memo="숫자 천천히")
b6 = L("액체 전해질이라면, 알아서 구석구석 스며들겠죠.", caps=["액체 전해질이라면", "알아서 구석구석 스며들겠죠"],
       pause=0.4, speed=1.04)
b7 = L("하지만 고체는 스며들지 않거든요.", pause=0.5, emph=["스며들지 않거든요"])
b8 = L("그래서 작은 알갱이들이 큰 알갱이 곁에 고루 자리 잡고, 서로 이어져야 합니다.",
       caps=["그래서 작은 알갱이들이", "큰 알갱이 곁에 고루 자리 잡고", "서로 이어져야 합니다"], pause=0.5,
       emph=["이어져야"])
b9 = L("이 배치의 밑그림을 그리는 단계가, 바로 가루를 섞는 과정이에요.",
       caps=["이 배치의 밑그림을 그리는 단계가", "바로 가루를 섞는 과정이에요"], pause=1.5, emph=["섞는 과정"],
       memo="절 끝")
SE_R = NCM_R * 1.075 * 0.7 / 4.3
SHOT("s02a", b1, [
    keep("ncm1", x=760, y=470, scale=1.075),
    circle("se_one", 1230, 470, round(SE_R, 1), b4 + "~작은", fill="indigo"),
    text("t_b_am", 760, 690, "활물질 (NCM)", b2 + "~활물질", size=32),
    text("t_b_am2", 760, 731, "니켈 · 코발트 · 망간 산화물", b3, size=24, color="grey", weight="semibold"),
    text("t_b_se", 1230, 690, "황화물 고체전해질", b4 + "~황화물", size=32),
    text("t_b_se2", 1230, 731, "리튬 이온이 지나는 길", b4 + "~고체전해질", size=24, color="grey", weight="semibold"),
    number("n_am", 760, 255, 4.3, b5 + "~사", unit="µm", decimals=1, size=70, color="ink"),
    number("n_se", 1230, 395, 0.7, b5 + "~영", unit="µm", decimals=1, size=70, color="indigo"),
    chip("c_ratio", 995, 575, "지름 약 6 배", b5 + "~영+0.9", size=26),        # 11-25: was "@0.95" (0.77 s on screen)
    src("src_hay_size", "Hayakawa 외, Adv. Powder Technol. 33, 103705 (2022) · 개수 기준 중앙 지름 · 6 배 = 4.3 ÷ 0.7 (산술)", b5),
], pre=0.4)
liq_c = [(530, 400), (700, 360), (640, 560), (450, 590)]
sol_c = [(1180, 400), (1400, 360), (1330, 590), (1110, 600)]
chain_path = [(1235, 800), (1250, 700), (1225, 500), (1300, 470), (1300, 330), (1345, 180)]
chain_pts = along(chain_path, 13)
sol_scatter = scatter(len(chain_pts), (1040, 200, 1520, 780), 13, seed=8, avoid=[(x, y, 72) for x, y in sol_c])
SHOT("s02b", b6, [
    rect("liq_bg", 580, 480, 420, 460, b6 + "~액체", fill="lavfill", stroke=None, radius=10),
    *[circle(f"liq{i}", x, y, 68, b6 + "~액체", label=None) for i, (x, y) in enumerate(liq_c)],
    text("t_liq", 580, 742, "액체 전해질: 스며든다", b6 + "~스며들겠죠", size=28),
    *[circle(f"sol{i}", x, y, 68, b7, label=None) for i, (x, y) in enumerate(sol_c)],
    dots("se_chain", sol_scatter, b7 + "~고체는", stagger=0.02, to=[[p[0], p[1]] for p in chain_pts],
         move_dots_at=b8 + "~이어져야", move_dur=1.0, move_stagger=0.025),
    text("t_sol", 1300, 832, "고체 전해질: 이어져야 한다", b8 + "~이어져야", size=28),
    line("ion_path", [(1265, 805), (1280, 700), (1255, 500), (1330, 470), (1328, 330), (1373, 185)], b8 + "$",
         color="indigo", sw=3, dash=[10, 8], arrow="end", dur=1.0),
    chip("c_sketch", 960, 175, "섞기 = 배치의 밑그림", b9 + "~밑그림", size=30, color="indigo", stroke="indigo"),
])

# ============================================================================
# S03  작을수록 끈적하다
# ============================================================================
scene("s03", "작을수록 끈적하다 — 본드 수")
c1 = L("그런데 아주 고운 가루는, 잘 섞이지 않습니다.", caps=["그런데 아주 고운 가루는", "잘 섞이지 않습니다"], pause=0.45)
c2 = L("입자들 사이에는, 늘 서로 당기는 힘이 있거든요.", caps=["입자들 사이에는", "늘 서로 당기는 힘이 있거든요"],
       pause=0.45, speed=1.03, emph=["당기는 힘"])
c3 = L("두 알갱이를 떼어 내는 데 드는 힘은, 알갱이의 크기에 비례합니다.",
       caps=["두 알갱이를 떼어 내는 데 드는 힘은", "알갱이의 크기에 비례합니다"], pause=0.5, speed=0.96,
       emph=["크기에 비례"])
c4 = L("반면 무게는, 크기의 세제곱에 비례하죠.", caps=["반면 무게는, 크기의 세제곱에 비례하죠"], pause=0.5,
       emph=["세제곱"])
c5 = L("그래서 지름이 열 배 작아지면, 붙는 힘은 십 분의 일이 되지만, 무게는 천 분의 일이 됩니다.",
       caps=["그래서 지름이 열 배 작아지면", "붙는 힘은 10분의 1이 되지만", "무게는 1000분의 1이 됩니다"], pause=0.45,
       speed=0.95, emo="강조", emph=["십 분의 일", "천 분의 일"], memo="대비를 살려서")
c6 = L("무게에 견준 끈적함이, 백 배로 커지는 거예요.", caps=["무게에 견준 끈적함이", "100배로 커지는 거예요"],
       pause=0.7, speed=0.95, emo="강조", emph=["백 배"])
c7 = L("이 비율을 본드 수라고 부릅니다.", pause=0.45, emph=["본드 수"], memo="'본드 수' 또박또박")
c8 = L("본드 수가 크면, 가루는 무게보다 끈적함을 따라 움직여요.",
       caps=["본드 수가 크면", "가루는 무게보다 끈적함을 따라 움직여요"], pause=0.6)
c9 = L("실제로 칼날 혼합기를 가장 느리게 돌린 조건에서는, 고체전해질이 활물질만 한 덩어리로 남아 있었습니다.",
       caps=["실제로 칼날 혼합기를", "가장 느리게 돌린 조건에서는", "고체전해질이 활물질만 한", "덩어리로 남아 있었습니다"],
       pause=1.5, speed=1.0, emph=["활물질만 한 덩어리"], memo="절 끝 · 긴 문장이니 쉼표에서 쉬기")
SHOT("s03a", c1, [
    dots("fine", cluster(34, 962, 430, 11, seed=17, jitter=0.3), c1 + "~고운", stagger=0.012, out=c2),
    text("t_fine", 962, 560, "고운 가루 · 잘 안 섞인다", c1 + "~고운", size=28, out=c2),
    circle("p_a", 900, 420, 62, c2, fill="indigo"),
    circle("p_b", 1024, 420, 62, c2, fill="indigo"),
    line("pull_l", [(826, 420), (712, 420)], c3 + "~떼어", arrow="end", sw=3),
    line("pull_r", [(1098, 420), (1212, 420)], c3 + "~떼어", arrow="end", sw=3),
    text("t_attr", 962, 320, "늘 서로 당긴다", c2 + "~당기는", size=26, color="grey", weight="semibold"),
    chip("f_jkr", 960, 615, "떼는 힘  =  3/2 × π × 접착일 × 유효 반지름", c3 + "~힘은", size=36, color="ink"),
    text("f_jkr2", 960, 688, "유효 반지름 = 두 반지름의 곱 ÷ 합   ·   크기에 비례", c3 + "~크기에", size=26, color="grey",
         weight="semibold"),
    text("t_weight3", 960, 760, "무게는 지름의 세제곱에 비례", c4 + "~무게는", size=30, color="indigo"),
    src("src_jkr", "Johnson · Kendall · Roberts, Proc. R. Soc. Lond. A 324, 301 (1971) · 매끈한 탄성 구 (JKR)", c3),
], pre=0.4)
SHOT("s03b", c5, [
    circle("sz_big", 520, 470, 120, c5 + "~지름이", fill=None, stroke="ink", sw=3, label="지름 10", ls=30, lc="ink"),
    circle("sz_small", 760, 470, 12, c5 + "~작아지면", fill="indigo"),
    text("t_sz_small", 760, 520, "지름 1", c5 + "~작아지면", size=26),
    text("t_force", 1000, 360, "붙는 힘", c5 + "~붙는", size=28, align="left"),
    rect("bar_f_big", 1340, 362, 400, 22, c5 + "~붙는", fill="ink", stroke=None, anim="grow"),
    rect("bar_f_small", 1160, 400, 40, 22, c5 + "~십", fill="indigo", stroke=None, anim="grow"),
    text("t_f_ratio", 1600, 400, "1/10", c5 + "~십", size=30, color="indigo", align="right"),
    text("t_weight", 1000, 520, "무게", c5 + "~무게는", size=28, align="left"),
    rect("bar_w_big", 1340, 522, 400, 22, c5 + "~무게는", fill="ink", stroke=None, anim="grow"),
    circle("bar_w_small", 1142, 560, 3, c5 + "~천", fill="indigo"),
    text("t_w_ratio", 1600, 560, "1/1000", c5 + "~천", size=30, color="indigo", align="right"),
    number("n_x100", 1290, 735, 100, c6 + "~백", unit="배", size=96, color="indigo", start=1),
    text("t_x100", 1290, 785, "무게에 견준 끈적함", c6 + "~백", size=26, color="grey", weight="semibold"),
    src("src_scale", "산술 예시 · 같은 물질 · 매끈한 구 · 떼는 힘은 반지름에 비례 (JKR 1971) · 무게는 반지름³에 비례", c5),
])
SHOT("s03c", c7, [
    chip("f_bond", 960, 330, "본드 수  =  떼는 힘  ÷  무게", c7 + "~본드", size=44, color="indigo", stroke="indigo"),
    dots("bond_clump", cluster(16, 760, 560, 15, seed=4), c8 + "~끈적함을", stagger=0.02),
    text("t_bond_big", 760, 680, "본드 수 > 1 : 끈적함이 이긴다", c8 + "~끈적함을", size=28),
    dots("bond_free", scatter(10, (1080, 470, 1320, 640), 15, seed=6), c8 + "~무게보다", fill="inkdim", stagger=0.02),
    text("t_bond_small", 1200, 680, "본드 수 < 1 : 무게가 이긴다", c8 + "~무게보다", size=28, color="grey"),
    src("src_bond", "정의: 떼는 힘 ÷ 가벼운 쪽 입자의 무게 — Figueroa · Li · McCarthy, Powder Technol. 195, 203 (2009) 식 22", c7),
])
lump = cluster(44, 1440, 470, 15, seed=9, jitter=0.25)
SHOT("s03d", c9, [
    mixer("mx0", 640, 470, 150, c9 + "~칼날", spin=[[c9 + "~칼날", c9 + "$", 0.35]]),
    text("t_mx0", 640, 660, "칼날 1분에 5천 번 (가장 느린 조건)", c9 + "~가장", size=26),
    circle("ncm_lump", 1150, 470, 105, c9 + "~활물질만", label="활물질", ls=30),
    dots("se_lump", lump, c9 + "~덩어리로", stagger=0.012),
    text("t_lump", 1440, 640, "고체전해질 덩어리", c9 + "~덩어리로", size=28, color="indigo"),
    text("t_lump2", 1300, 700, "전자현미경 사진에서 본 모습 (정성 관찰)", c9 + "~남아", size=24, color="grey",
         weight="semibold"),
    src("src_hay_lump", "Hayakawa 외, Adv. Powder Technol. 33, 103705 (2022) · 칼날 5천 rpm · 활물질 크기의 SE 덩어리", c9),
])

# ============================================================================
# S04  누구와 붙을까
# ============================================================================
scene("s04", "누구와 붙을까 — 힘의 비율")
d1 = L("그럼 작은 가루는, 누구와 붙을까요?", caps=["그럼 작은 가루는, 누구와 붙을까요?"], pause=0.85, speed=0.97,
       emo="궁금", memo="물음 · 끝 올림")
d2 = L("길은 두 가지입니다.", pause=0.3, speed=1.0)
d3 = L("자기들끼리 뭉치거나, 아니면 큰 알갱이 표면에 붙는 거예요.",
       caps=["자기들끼리 뭉치거나", "아니면 큰 알갱이 표면에 붙는 거예요"], pause=0.6, emph=["자기들끼리", "표면에"])
d4 = L("여기서 크기가 한 번 더 일을 합니다.", pause=0.4, speed=1.03, emph=["크기"])
d5 = L("작은 알갱이가 큰 알갱이에 닿으면, 상대 표면이 거의 평평하게 느껴지거든요.",
       caps=["작은 알갱이가 큰 알갱이에 닿으면", "상대 표면이 거의 평평하게 느껴지거든요"], pause=0.45, speed=1.0)
d6 = L("그래서 같은 끈적함이라면, 작은 알갱이끼리보다 큰 알갱이에 붙는 쪽이, 최대 두 배까지 세게 붙습니다.",
       caps=["그래서 같은 끈적함이라면", "작은 알갱이끼리보다", "큰 알갱이에 붙는 쪽이", "최대 두 배까지 세게 붙습니다"],
       pause=0.65, speed=0.95, emo="강조", emph=["최대 두 배"])
d7 = L("하지만 표면 자체의 끈적함이 다르면, 이야기가 달라지죠.",
       caps=["하지만 표면 자체의 끈적함이 다르면", "이야기가 달라지죠"], pause=0.45, emo="진지")
d8 = L("큰 알갱이 표면이 훨씬 덜 끈적하다면, 작은 알갱이는 자기들끼리 뭉치는 쪽을 고릅니다.",
       caps=["큰 알갱이 표면이 훨씬 덜 끈적하다면", "작은 알갱이는", "자기들끼리 뭉치는 쪽을 고릅니다"], pause=0.5)
d9 = L("결국 승부는, 작은 알갱이끼리 붙는 힘과, 큰 알갱이에 붙는 힘의 비율이에요.",
       caps=["결국 승부는", "작은 알갱이끼리 붙는 힘과", "큰 알갱이에 붙는 힘의 비율이에요"], pause=0.75, speed=0.95,
       emo="강조", emph=["비율"])
d10 = L("분체 과학에서는, 이런 힘의 비율로 섞일지 갈라질지를 가르는 지도를 그려 왔습니다.",
        caps=["분체 과학에서는", "이런 힘의 비율로 섞일지 갈라질지를", "가르는 지도를 그려 왔습니다"], pause=0.45)
d11 = L("다만 건식 가루에 대한 그 지도는, 컴퓨터 속 매끈한 가상 알갱이로 그린 거예요.",
        caps=["다만 건식 가루에 대한 그 지도는", "컴퓨터 속 매끈한 가상 알갱이로", "그린 거예요"], pause=0.5, emo="진지",
        emph=["가상 알갱이"])
d12 = L("작은 알갱이가 큰 알갱이의 절반 크기일 때는, 네 경우 중 두 번이 예측과 반대로 나왔고요.",
        caps=["작은 알갱이가 큰 알갱이의", "절반 크기일 때는", "네 경우 중 두 번이", "예측과 반대로 나왔고요"], pause=0.4,
        speed=0.97, emph=["두 번", "반대로"])
d13 = L("끈적함을 두 배로 키우자, 넷 중 셋이 다시 들어맞았습니다.",
        caps=["끈적함을 두 배로 키우자", "넷 중 셋이 다시 들어맞았습니다"], pause=0.55, speed=0.97)
d14 = L("비율 하나만으로는, 다 정해지지 않는다는 뜻이죠.", caps=["비율 하나만으로는", "다 정해지지 않는다는 뜻이죠"],
        pause=1.5, emph=["비율 하나만으로는"], memo="절 끝")
SHOT("s04a", d1, [
    circle("me", 960, 450, 17, d1 + "~작은", fill="indigo"),
    circle("me_q", 960, 450, 46, d1 + "~누구와", fill=None, stroke="ink", sw=2.5, dash=[8, 6]),
    circle("q_l", 560, 450, 62, d1 + "~누구와+0.2", fill=None, stroke="grey", sw=2.5, dash=[8, 6], label="?", ls=44,
           lc="grey", out=d3 + "~자기들끼리"),
    circle("q_r", 1400, 450, 120, d1 + "~누구와+0.35", fill=None, stroke="grey", sw=2.5, dash=[8, 6], label="?",
           ls=60, lc="grey", out=d3 + "~큰"),
    line("way_l", [(910, 450), (700, 450)], d2 + "~두", arrow="end"),
    line("way_r", [(1010, 450), (1220, 450)], d2 + "~두", arrow="end"),
    dots("me_clump", cluster(14, 560, 450, 15, seed=12), d3 + "~자기들끼리", stagger=0.02),
    text("t_way_l", 560, 570, "자기들끼리", d3 + "~자기들끼리", size=30),
    circle("me_ncm", 1400, 450, 120, d3 + "~큰", label="활물질", ls=30),
    dots("me_att", shell(7, 1400, 450, 120, 15, a0=150, a1=230, gap=1.0), d3 + "~표면에", stagger=0.03),
    text("t_way_r", 1400, 620, "큰 알갱이 표면에", d3 + "~표면에", size=30),
], pre=0.4)
SHOT("s04b", d4, [
    circle("g_a", 560, 430, 52, d4 + "~크기가", fill="indigo"),
    circle("g_b", 664, 430, 52, d4 + "~크기가", fill="indigo"),
    text("t_g1", 612, 535, "작은 끼리: 유효 반지름 r/2", d5, size=27),
    line("g_surf", [(1040, 520), (1150, 503), (1270, 497), (1390, 503), (1500, 520)], d5 + "~큰", sw=5, anim="draw"),
    text("t_surf", 1270, 560, "큰 알갱이 표면", d5 + "~큰", size=24, color="grey", weight="semibold"),
    circle("g_c", 1270, 443, 52, d5 + "~닿으면", fill="indigo"),
    text("t_g2", 1270, 612, "큰 상대와: 유효 반지름 ≈ r", d5 + "~평평하게", size=27),
    number("n_x2", 960, 755, 2, d6 + "~최대", unit="배", size=92, color="indigo", start=1, prefix="최대 "),
    text("t_x2", 960, 800, "같은 끈적함이라면, 떼는 힘", d6 + "~최대", size=24, color="grey", weight="semibold"),
    src("src_rstar", "JKR 1971 · 유효 반지름 = 곱 ÷ 합 · 산술: 같은 크기끼리 r/2 · 아주 큰 상대 ≈ r · 매끈한 구", d6),
])
att = shell(16, 1250, 470, 150, 15, a0=110, a1=250, gap=1.0)
clu = cluster(16, 720, 470, 15, seed=21)
SHOT("s04c", d7, [
    circle("w_ncm", 1250, 470, 150, d7 + "~표면", label="활물질", ls=30),
    text("t_wncm", 1250, 668, "덜 끈적한 표면", d8 + "~덜", size=28, color="grey"),
    dots("w_se", att, d7 + "~끈적함이", stagger=0.02, to=[[p[0], p[1]] for p in clu], move_dots_at=d8 + "~뭉치는",
         move_dur=1.1, move_stagger=0.03),
    text("t_wclu", 720, 600, "자기들끼리", d8 + "~뭉치는", size=30, color="indigo"),
    text("fr_top", 960, 175, "작은 알갱이끼리 붙는 힘", d9 + "~작은", size=30),
    line("fr_bar", [(745, 210), (1175, 210)], d9 + "~작은", sw=3, dur=0.4),
    text("fr_bot", 960, 246, "큰 알갱이에 붙는 힘", d9 + "~큰", size=30),
    text("fr_lbl", 1250, 210, "← 이 비율", d9 + "~비율이에요", size=26, color="indigo", align="left"),
], pre=0.4)
# concept map (upper boundary of the mixed state: phi = 2 / (1 + beta), Figueroa 2009 eq. 30)
mx0, my0, mx1, my1 = 560, 770, 1400, 260


def mp(beta, phi):
    return (mx0 + beta * (mx1 - mx0), my0 - phi / 2.6 * (my0 - my1))


bnd = [mp(b / 40.0, 2.0 / (1.0 + b / 40.0)) for b in range(0, 41)]
upper_poly = bnd + [mp(1.0, 2.6), mp(0.0, 2.6)]
SHOT("s04d", d10, [
    line("ax_x", [(mx0, my0), (mx1 + 40, my0)], d10 + "+0.25", arrow="end", sw=2.5, dur=0.5),
    line("ax_y", [(mx0, my0), (mx0, my1 - 30)], d10 + "+0.25", arrow="end", sw=2.5, dur=0.5),
    text("ax_xl", mx1 + 40, my0 + 34, "지름비 (작은 쪽 ÷ 큰 쪽)", d10 + "+0.55", size=24, color="grey", align="right",
         weight="semibold"),
    text("ax_yl", mx0 + 14, my1 - 32, "끈적함의 비 (작은 쪽 ÷ 큰 쪽)", d10 + "+0.55", size=24, color="grey", align="left",
         weight="semibold"),
    area("rg_up", [list(p) for p in upper_poly], d10 + "~섞일지", fill="lavfill"),
    line("bnd", [list(p) for p in bnd], d10 + "~갈라질지를", color="indigo", sw=3, dur=0.8),
    text("rg_up_t", 760, 300, "작은 알갱이끼리 뭉침", d10 + "~갈라질지를", size=28, color="indigo"),
    text("rg_lo_t", 1230, 690, "섞임 · 큰 알갱이에 붙음", d10 + "~갈라질지를", size=28),
    chip("c_virtual", 1240, 430, "가상 알갱이 계산 · 실험 없음", d11 + "~가상", size=24, color="ink"),
    line("b05", [list(mp(0.5, 0.0)), list(mp(0.5, 2.5))], d12 + "~절반", color="ink", sw=2, dash=[8, 7], dur=0.5),
    text("b05_t", mp(0.5, 0)[0], my0 + 34, "0.5", d12 + "~절반", size=24, color="ink"),
    chip("c_fail", 765, 560, "기본 끈적함: 4 중 2 반대", d12 + "~두", size=24, color="ink"),
    chip("c_fix", 765, 625, "끈적함 × 2: 4 중 3 일치", d13 + "~넷", size=24, color="indigo", stroke="indigo"),
    src("src_fig", "개념도 · 경계선 = Figueroa · Li · McCarthy, Powder Technol. 195, 203 (2009) 식 30 · 사례 = 표 3 · 지름 4 mm 가상 구 (DEM)", d10),
])

# ============================================================================
# S05  약 만드는 분야는 알고 있었다
# ============================================================================
scene("s05", "약을 만드는 분야가 먼저 판 문제 — 정렬 혼합과 힘의 비율")
e1 = L("사실 이 문제를 오래 파 온 분야가 있어요.", caps=["사실 이 문제를", "오래 파 온 분야가 있어요"], pause=0.35, speed=1.03,
       emo="가벼움")
e2 = L("바로 약을 만드는 쪽입니다.", pause=0.45, emph=["약"])
e3 = L("들이마시는 흡입약은 흔히, 아주 고운 약 가루를 훨씬 큰 유당 가루에 붙여서 만들거든요.",
       caps=["들이마시는 흡입약은 흔히", "아주 고운 약 가루를", "훨씬 큰 유당 가루에 붙여서 만들거든요"], pause=0.5)
e4 = L("작은 가루가 큰 가루 표면에 붙으면서 섞이는 이 방식을, 정렬 혼합이라고 불렀습니다.",
       caps=["작은 가루가 큰 가루 표면에", "붙으면서 섞이는 이 방식을", "정렬 혼합이라고 불렀습니다"], pause=0.4,
       emph=["정렬 혼합"])
e5 = L("나중에는, 상호작용 혼합이라는 이름이 제안됐고요.", caps=["나중에는", "상호작용 혼합이라는 이름이 제안됐고요"],
       pause=0.45, speed=1.02, emph=["상호작용 혼합"])
e6 = L("두 크기가 열 배에서 백 배쯤 차이 날 때, 작은 가루가 큰 가루에 잘 붙는다고 알려져 있죠.",
       caps=["두 크기가 10배에서", "100배쯤 차이 날 때", "작은 가루가 큰 가루에", "잘 붙는다고 알려져 있죠"], pause=0.45,
       speed=0.97)
e7 = L("앞서 본 전고체 양극 가루에서는, 그 차이가 여섯 배 정도였어요.",
       caps=["앞서 본 전고체 양극 가루에서는", "그 차이가 6배 정도였어요"], pause=0.75, speed=0.95, emo="강조",
       emph=["여섯 배"])
e8 = L("그리고 이천사 년, 영국 연구진이 그 힘을 직접 쟀습니다.",
       caps=["그리고 2004년", "영국 연구진이 그 힘을 직접 쟀습니다"], pause=0.45, emph=["직접"])
e9 = L("원자힘현미경의 아주 작은 막대 끝에, 약 가루 한 알을 붙였어요.",
       caps=["원자힘현미경의 아주 작은 막대 끝에", "약 가루 한 알을 붙였어요"], pause=0.4, speed=1.0)
e10 = L("그리고 같은 약의 결정과 유당의 결정에, 번갈아 눌렀다 떼면서 힘을 쟀죠.",
        caps=["그리고 같은 약의 결정과", "유당의 결정에 번갈아", "눌렀다 떼면서 힘을 쟀죠"], pause=0.35)
e11 = L("한 쌍마다, 사천구십육 번씩이요.", say="한 쌍마다, 사천구십육 번씩이요.", caps=["한 쌍마다, 4096번씩이요"],
        pause=0.7, speed=0.94, emph=["사천구십육 번"])
e12 = L("결과는 뚜렷하게 갈렸습니다.", pause=0.4, emo="진지")
e13 = L("한 약은, 유당에 붙는 힘이 자기끼리 붙는 힘의 열일곱 배쯤 됐어요.",
        caps=["한 약은 유당에 붙는 힘이", "자기끼리 붙는 힘의 17배쯤 됐어요"], pause=0.4, speed=0.95, emo="강조",
        emph=["열일곱 배"])
e14 = L("다른 약은 반대로, 자기끼리 붙는 힘이 많게는 네 배 가까이 셌고요.",
        caps=["다른 약은 반대로", "자기끼리 붙는 힘이", "많게는 4배 가까이 셌고요"], pause=0.45, speed=0.96,
        emph=["네 배"])
e15 = L("실제로 섞어 보니, 앞의 약은 유당 위에 고르게 퍼졌고, 뒤의 약은 덩어리로 남았습니다.",
        caps=["실제로 섞어 보니", "앞의 약은 유당 위에 고르게 퍼졌고", "뒤의 약은 덩어리로 남았습니다"], pause=0.5)
e16 = L("힘의 비율로, 섞인 모습을 미리 내다본 셈이죠.", caps=["힘의 비율로", "섞인 모습을 미리 내다본 셈이죠"],
        pause=0.8, emph=["미리"])
e17 = L("그런데 이야기가 여기서 끝나지는 않아요.", pause=0.45, speed=1.03, emo="진지")
e18 = L("이천팔 년에는, 약과 운반 입자 조합 열여섯 가지를 같은 방법으로 견줘 봤어요.",
        caps=["2008년에는", "약과 운반 입자 조합 16가지를", "같은 방법으로 견줘 봤어요"], pause=0.4)
e19 = L("그랬더니 운반 입자별로 보면 흡입 성능과는 관계가 보였지만, 섞임의 고르기와는 뚜렷한 관계가 보이지 않았습니다.",
        caps=["그랬더니 운반 입자별로 보면", "흡입 성능과는 관계가 보였지만", "섞임의 고르기와는", "뚜렷한 관계가 보이지 않았습니다"],
        pause=0.5, speed=0.97, emph=["보이지 않았습니다"])
e20 = L("힘의 비율은 중요한 단서이지만, 그것만으로 결과가 정해지지는 않는 거죠.",
        caps=["힘의 비율은 중요한 단서이지만", "그것만으로 결과가 정해지지는 않는 거죠"], pause=1.5,
        emph=["단서"], memo="절 끝")
lac_pts = shell(40, 1220, 470, 165, 7, seed=None)
SHOT("s05a", e1, [
    chip("c_field", 960, 450, "이 문제를 오래 파 온 분야", e1 + "+0.2", size=36, color="ink",
         moves=[dict(at=e1 + "$+0.05", dur=0.45, y=190, scale=0.83)]),
    rect("inh_body", 640, 470, 150, 250, e2 + "~약을", fill=None, stroke="ink", sw=3, radius=22),
    rect("inh_mouth", 640, 330, 80, 40, e2 + "~약을", fill=None, stroke="ink", sw=3, radius=8),
    text("t_inh", 640, 640, "흡입약", e2 + "~약을", size=30),
    circle("lac", 1220, 470, 165, e3 + "~유당", fill=None, stroke="ink", sw=3, label="유당", ls=32, lc="ink"),
    dots("drug", lac_pts, e3 + "~고운", fill="grey", stagger=0.015),
    text("t_drug", 1220, 690, "약 가루 1.4–1.8 µm  ·  유당 61–74 µm", e3 + "~훨씬", size=26, color="ink",
         weight="semibold"),
    src("src_jones_size", "Jones 외, Eur. J. Pharm. Biopharm. 69, 496 (2008) · 중앙 지름 (약 1.44–1.79 µm · 운반 입자 60.7–74.2 µm)", e3),
], pre=0.4)


def lx(v):
    return 560 + math.log10(v) / 2.0 * 800


SHOT("s05b", e4, [
    # 11-25 final render: the first new element came at "~정렬" (4.1 s into the line = empty picture) -> the s05a picture of
    # fine drug on a lactose carrier (what the sentence describes) slides to the middle, stays under the 1975 · 1983 names and
    # leaves before the size axis.  Same picture, no new number.
    keep("lac", x=960, y=540, scale=0.62, out=e6 + "~두-0.35"),
    keep("drug", x=960, y=540, scale=0.62, out=e6 + "~두-0.35"),
    line("tl", [(560, 290), (1400, 290)], e4 + "~정렬", sw=2.5, dur=0.6),
    circle("tl75", 680, 290, 9, e4 + "~정렬", fill="indigo"),
    text("tl75t", 680, 250, "1975", e4 + "~정렬", size=30),
    text("tl75s", 680, 334, "정렬 혼합", e4 + "~정렬", size=28, color="indigo"),
    circle("tl83", 980, 290, 9, e5 + "~상호작용", fill="indigo"),
    text("tl83t", 980, 250, "1983", e5 + "~상호작용", size=30),
    text("tl83s", 980, 334, "상호작용 혼합", e5 + "~상호작용", size=28, color="indigo"),
    line("lg_ax", [(lx(1), 620), (lx(100) + 30, 620)], e6 + "~두", sw=2.5, arrow="end", dur=0.5),
    *[text(f"lg_t{v}", lx(v), 660, f"{v}배", e6 + "~두", size=24, color="grey") for v in (1, 10, 100)],
    *[line(f"lg_k{v}", [(lx(v), 610), (lx(v), 630)], e6 + "~두", sw=2.5, anim="fade") for v in (1, 10, 100)],
    rect("lg_band", (lx(10) + lx(100)) / 2, 590, lx(100) - lx(10), 34, e6 + "~열", fill="lavfill", stroke=None),
    text("lg_band_t", (lx(10) + lx(100)) / 2, 548, "작은 가루가 잘 붙는 크기 차", e6 + "~백", size=24, color="indigo"),
    rect("lg_inh", (lx(34) + lx(52)) / 2, 590, lx(52) - lx(34), 16, e6 + "~잘", fill="grey", stroke=None),
    text("lg_inh_t", (lx(34) + lx(52)) / 2, 720, "흡입약 34–52배", e6 + "~잘", size=26, color="grey"),
    line("lg_inh_l", [((lx(34) + lx(52)) / 2, 600), ((lx(34) + lx(52)) / 2, 695)], e6 + "~잘", sw=2, color="grey",
         anim="fade"),
    circle("lg_assb", lx(6), 590, 11, e7 + "~여섯", fill="indigo"),
    text("lg_assb_t", lx(6), 720, "전고체 양극 약 6배", e7 + "~여섯", size=26, color="indigo"),
    line("lg_assb_l", [(lx(6), 603), (lx(6), 695)], e7 + "~여섯", sw=2, color="indigo", anim="fade"),
    src("src_order", "Hersey, Powder Technol. 11, 41 (1975) · Egermann · Orr, Powder Technol. 36, 117 (1983) · Pfeffer 외, Powder Technol. 117, 40 (2001: 한두 자릿수)\n"
        "배율 = 중앙 지름 비 (산술): 흡입약 Jones 외 (2008) · 전고체 양극 Hayakawa 외 (2022)", e4, y=858),
])
# AFM shot: cantilever group (pivot = tip particle)
TIPX, TIPY = 700, 330
SLAB_Y = 565


def cantilever(id, at, tipx=TIPX, tipy=TIPY, label="약 가루 한 알", part_color="grey"):
    parts = [dict(k="rect", x=tipx - 330, y=tipy - 40, w=70, h=44, fill="ink"),
             dict(k="line", points=[(tipx - 300, tipy - 30), (tipx, tipy - 18)], sw=6),
             dict(k="circle", x=tipx, y=tipy, r=17, fill=part_color, stroke=False),
             dict(k="text", x=tipx + 38, y=tipy - 52, text=label, size=24, anchor="lm")]
    return dict(id=id, type="group", x=tipx, y=tipy, at=at, parts=parts,
                bbox=[tipx - 370, tipy - 80, tipx + 230, tipy + 22])


S2X = 1050
fx0, fy0 = 1350, 420
fc_appr = [(fx0, fy0), (fx0 + 120, fy0), (fx0 + 160, fy0 + 5), (fx0 + 175, fy0 - 40)]
fc_retr = [(fx0 + 175, fy0 - 40), (fx0 + 160, fy0 + 5), (fx0 + 150, fy0 + 75), (fx0 + 146, fy0 + 2), (fx0 + 40, fy0 + 2)]
cant = cantilever("cant", e9 + "~막대")
cant["moves"] = [
    dict(at=e10 + "~번갈아", dur=0.45, x=TIPX, y=SLAB_Y - 17),
    dict(at=e10 + "~번갈아+0.55", dur=0.45, x=TIPX, y=TIPY),
    dict(at=e10 + "~번갈아+1.05", dur=0.55, x=S2X, y=TIPY),
    dict(at=e10 + "~번갈아+1.65", dur=0.45, x=S2X, y=SLAB_Y - 17),
    dict(at=e10 + "~번갈아+2.15", dur=0.45, x=S2X, y=TIPY),
]
SHOT("s05c", e8, [
    text("t_2004big", 960, 430, "2004", e8 + "~이천사", size=120, weight="extrabold", out=e9 + "-0.15"),
    text("t_2004uk", 960, 535, "영국 연구진 · 가루 사이의 힘을 직접 측정", e8 + "~영국", size=32, color="grey",
         weight="semibold", out=e9 + "-0.15"),
    text("t_2004", 960, 175, "2004 · 영국", e9, size=30, color="grey"),
    cant,
    rect("slab1", TIPX, SLAB_Y + 25, 280, 50, e10 + "~같은", fill="lavfill", stroke="ink", sw=2,
         label="같은 약 결정", ls=24),
    rect("slab2", S2X, SLAB_Y + 25, 280, 50, e10 + "~유당의", fill=None, stroke="ink", sw=2, label="유당 결정", ls=24),
    line("fc_ax", [(fx0 - 20, fy0), (fx0 + 230, fy0)], e10 + "~힘을", sw=2, color="grey", dur=0.3),
    line("fc_a", fc_appr, e10 + "~힘을", sw=3, color="ink", dur=0.5),
    line("fc_r", fc_retr, e10 + "~힘을+0.5", sw=3, color="indigo", dur=0.6),
    text("fc_t", fx0 + 105, fy0 - 85, "힘 곡선", e10 + "~힘을", size=24, color="grey", weight="semibold"),
    text("fc_po", fx0 + 150, fy0 + 108, "떼는 힘", e10 + "~힘을+0.9", size=24, color="indigo"),
    number("n_4096", 1460, 700, 4096, e11 + "~사천", unit="번", size=76, color="indigo"),
    text("t_4096", 1460, 745, "탐침 · 기판 한 쌍마다", e11 + "~사천", size=24, color="grey", weight="semibold"),
    src("src_begat1", "Begat · Morton · Staniforth · Price, Pharm. Res. 21, 1591 (2004) · 콜로이드 탐침 원자힘현미경 · 25 °C · 습도 35 %", e9),
])
lac_even = shell(28, 700, 600, 95, 6)
lac_clumpy = cluster(9, 1143, 523, 6, seed=3) + cluster(8, 1322, 637, 6, seed=4) + cluster(6, 1183, 702, 6, seed=5)
SHOT("s05d", e12, [
    text("t_drugA", 700, 205, "약 A · 살부타몰", e12 + "+0.2", size=30),
    text("t_vs", 960, 205, "↔", e12 + "~갈렸습니다", size=34, color="grey"),
    number("n_A", 700, 310, 16.9, e13 + "~열일곱", unit="배", decimals=1, size=84, color="indigo", start=1),
    text("t_A2", 700, 355, "유당에 붙는 힘 ÷ 자기끼리", e13 + "~열일곱", size=24, color="grey", weight="semibold"),
    text("t_drugB", 1220, 205, "약 B · 부데소나이드", e12 + "+0.45", size=30),
    number("n_B", 1220, 310, 3.84, e14 + "~네", unit="배", decimals=2, size=84, color="ink", start=1,
           display="2.4–3.8", anim="fade"),
    text("t_B2", 1220, 355, "자기끼리 ÷ 유당에 붙는 힘 (탐침에 따라)", e14 + "~네", size=24, color="grey",
         weight="semibold"),
    circle("lacA", 700, 600, 95, e15 + "~앞의", fill=None, stroke="ink", sw=2.5),
    dots("drugA", lac_even, e15 + "~고르게", fill="grey", stagger=0.01),
    text("t_mixA", 700, 745, "고르게 퍼짐 · 함량 편차 4.2 %", e15 + "~고르게", size=26, color="indigo"),
    circle("lacB", 1220, 600, 95, e15 + "~뒤의", fill=None, stroke="ink", sw=2.5),
    dots("drugB", lac_clumpy, e15 + "~덩어리로", fill="grey", stagger=0.01),
    text("t_mixB", 1220, 745, "덩어리로 남음 · 함량 편차 28.1 %", e15 + "~덩어리로", size=26),
    src("src_begat2", "Begat 외, Pharm. Res. 21, 1591 · 1826 (2004) — Part I 힘 비율 (원자힘현미경) · Part II 같은 조건 혼합 · 두 약 비교", e13),
])
grid = [(700 + 52 * (i % 4), 330 + 52 * (i // 4), 15) for i in range(16)]
SHOT("s05e", e18, [
    text("t_2008", 778, 230, "2008 · 16 조합", e18 + "~이천팔", size=30, color="grey"),
    dots("combos", grid, e18 + "~열여섯", fill="grey", stagger=0.04),
    text("t_combo", 778, 560, "약 4 × 운반 입자 4", e18 + "~같은", size=24, color="grey", weight="semibold"),
    chip("c_perf", 1290, 380, "흡입 성능 ↔ 힘 비율: 관계 있음", e19 + "~흡입", size=28, color="indigo", stroke="indigo"),
    text("c_perf2", 1290, 430, "운반 입자별 최고점 1.07–1.16", e19 + "~흡입", size=24, color="grey", weight="semibold"),
    chip("c_unif", 1290, 520, "섞임 고르기 ↔ 힘 비율: 뚜렷한 관계 없음", e19 + "~섞임의", size=28, color="ink"),
    text("t_clue", 960, 710, "중요한 단서 · 그러나 전부는 아님", e20 + "~단서", size=34, color="ink"),
    src("src_jones", "Jones 외, Eur. J. Pharm. Biopharm. 69, 496 (2008) · 16 이원 혼합물 · 힘 비율 = 짝 논문의 원자힘현미경 값", e18),
])

# ============================================================================
# S06  덮어 두면 — 코팅이 바꾸는 균형
# ============================================================================
scene("s06", "미리 덮어 두면 — 코팅이 바꾸는 균형")
f1 = L("이제 배터리로 돌아와 볼게요.", pause=0.35, speed=1.05, emo="가벼움")
f2 = L("큰 알갱이 표면을, 미리 고체전해질로 얇게 덮어 두면 어떨까요?",
       caps=["큰 알갱이 표면을", "미리 고체전해질로 얇게 덮어 두면", "어떨까요?"], pause=0.85, speed=0.97, emo="궁금",
       emph=["미리", "얇게"])
f3 = L("작은 알갱이 입장에서는, 큰 알갱이가 자기와 같은 물질로 보이게 됩니다.",
       caps=["작은 알갱이 입장에서는", "큰 알갱이가 자기와 같은 물질로", "보이게 됩니다"], pause=0.4)
f4 = L("표면 끈적함의 차이가 사라지는 셈입니다.", pause=0.45, emph=["사라지는"])   # 11-25 1저자 권고대로: "거죠" = 세 판 모두 이웃보다 +5–7 반음
f5 = L("그러면 크기에서 오는 이점만 남게 되고요.", pause=0.35, speed=1.02)
f6 = L("작은 알갱이가 큰 알갱이 쪽에 붙기 쉬워질 거라고 기대할 수 있습니다.",
       caps=["작은 알갱이가 큰 알갱이 쪽에", "붙기 쉬워질 거라고 기대할 수 있습니다"], pause=0.65, emph=["기대할"],
       memo="'기대' = 가설임을 살려서 단정하지 않게")
f7 = L("다만, 표면을 바꾼다고 늘 좋아지는 건 아닙니다.", caps=["다만, 표면을 바꾼다고", "늘 좋아지는 건 아닙니다"],
       pause=0.45, emo="진지", emph=["늘"])
f8 = L("세제 가루를 다룬 한 연구에서는, 한 성분을 코팅해 끈적하게 만들자, 성분이 갈라지는 정도가 줄었어요.",
       caps=["세제 가루를 다룬 한 연구에서는", "한 성분을 코팅해 끈적하게 만들자", "성분이 갈라지는 정도가 줄었어요"],
       pause=0.4, speed=1.0)
f9 = L("그런데 계산에서 끈적함을 더 키우자, 고운 가루가 들러붙은 덩어리가 생기면서, 오히려 더 갈라졌습니다.",
       caps=["그런데 계산에서 끈적함을 더 키우자", "고운 가루가 들러붙은 덩어리가 생기면서", "오히려 더 갈라졌습니다"],
       pause=0.5, speed=0.98, emph=["오히려"])
f10 = L("끈적함에도, 알맞은 정도가 있다는 뜻이죠.", caps=["끈적함에도", "알맞은 정도가 있다는 뜻이죠"], pause=1.45,
        emph=["알맞은 정도"], memo="절 끝")
SHOT("s06a", f1, [
    circle("c_ncm", 960, 470, 150, f1 + "~배터리로", label="활물질", ls=34),
    circle("c_shell", 960, 470, 159, f2 + "~얇게", fill=None, stroke="indigo", sw=11, anim="draw", dur=0.9),
    text("t_shell", 960, 668, "고체전해질 얇은 층", f2 + "~얇게", size=28, color="indigo"),
    text("t_same", 1380, 330, "작은 알갱이가 보기에: 같은 물질", f3 + "~같은", size=26, align="center"),
    chip("c_dw0", 960, 200, "표면 끈적함 차이 = 0", f4 + "~차이가", size=30, color="indigo", stroke="indigo"),
    text("t_left", 960, 255, "남는 것: 크기에서 오는 이점", f5 + "~크기에서", size=26, color="grey", weight="semibold"),
    dots("c_se", scatter(9, (560, 330, 760, 700), 14, seed=31) + scatter(9, (1170, 400, 1400, 720), 14, seed=32), f3 + "~작은", stagger=0.02,
         to=[[p[0], p[1]] for p in shell(18, 960, 470, 165, 14, seed=7)], move_dots_at=f6 + "~붙기", move_dur=1.0,
         move_stagger=0.03),
    chip("c_hyp", 1395, 770, "가설 · 기대", f6 + "~기대할", size=26, color="indigo", stroke="indigo"),
    src("src_principle", "원리 (가설): 떼는 힘은 접착일 × 유효 반지름에 비례 (JKR 1971) · 접착일 = 표면 에너지의 기하평균 (Figueroa 외 2009)", f4),
], pre=0.4)
bx = [700, 960, 1220]
vals = [1.57, 0.86, 2.58]
bar_h = [v / 2.6 * 340 for v in vals]
SHOT("s06b", f7, [
    chip("c_notalways", 960, 450, "표면을 바꿔도 늘 좋아지지는 않는다", f7 + "+0.3", size=36, color="ink",
         moves=[dict(at=f7 + "$+0.05", dur=0.45, y=195, scale=0.83)]),
    line("sb_ax", [(560, 690), (1360, 690)], f8 + "~세제", sw=2.5, dur=0.4),
    *[rect(f"sb{i}", bx[i], 690 - bar_h[i] / 2, 120, bar_h[i], (f8 + "~세제") if i == 0 else (f8 + "~줄었어요" if i == 1 else f9 + "~덩어리가"),
           fill="ink" if i != 1 else "indigo", stroke=None, anim="grow", grow_dir="y") for i in range(3)],
    *[text(f"sbv{i}", bx[i], 690 - bar_h[i] - 28, f"{vals[i]:.2f}", (f8 + "~세제") if i == 0 else (f8 + "~줄었어요" if i == 1 else f9 + "~덩어리가"),
           size=30, color="ink" if i != 1 else "indigo") for i in range(3)],
    text("sbl0", bx[0], 730, "코팅 전", f8 + "~세제", size=26),
    text("sbl1", bx[1], 730, "코팅", f8 + "~코팅해", size=26, color="indigo"),
    text("sbl2", bx[2], 730, "지나치게 끈적", f9 + "~끈적함을", size=26),
    text("sb_y", 560, 300, "분리 지수 (클수록 많이 갈라짐 · 계산)", f8 + "~갈라지는", size=24, color="grey", align="left",
         weight="semibold"),
    text("sb_exp", 1500, 520, "실험 (앞면 변동계수)\n1.33 → 0.83", f8 + "~줄었어요", size=24, color="grey",
         weight="semibold"),
    line("sb_u", [(bx[0], 690 - bar_h[0] - 62), (bx[1], 690 - bar_h[1] - 62), (bx[2], 690 - bar_h[2] - 62)], f10 + "~알맞은",
         color="indigo", sw=2.5, dash=[9, 7], dur=0.7),
    text("sb_opt", bx[1], 690 - bar_h[1] - 92, "알맞은 정도", f10 + "~알맞은", size=26, color="indigo"),
    src("src_aliz", "Alizadeh 외, Powder Technol. 339, 789 (2018) · 세제 분말 3 성분 더미 · 분리 지수 S_n (계산) · 앞면 변동계수 (실험)", f8),
])

# ============================================================================
# S07  황화물에서는 쟀을까
# ============================================================================
scene("s07", "황화물 고체전해질에서는 쟀을까")
g1 = L("그럼 황화물 고체전해질에서는, 이 힘을 재 봤을까요?",
       caps=["그럼 황화물 고체전해질에서는", "이 힘을 재 봤을까요?"], pause=0.85, speed=0.97, emo="궁금")
g2 = L("저희 연구실이 참여한 연구에서는, 조성이 다른 황화물 다섯 가지를 원자힘현미경으로 재 봤습니다.",
       caps=["저희 연구실이 참여한 연구에서는", "조성이 다른 황화물 다섯 가지를", "원자힘현미경으로 재 봤습니다"],
       pause=0.4, emph=["다섯 가지"], memo="'저희 연구실이 참여한' = 공저 밝힘")
g3 = L("실리콘 탐침을 눌렀다 떼면서, 떼어 낼 때 드는 일인 접착일과, 단단함을 함께 쟀어요.",
       caps=["실리콘 탐침을 눌렀다 떼면서", "떼어 낼 때 드는 일인 접착일과", "단단함을 함께 쟀어요"], pause=0.45,
       emph=["접착일"])
g4 = L("같은 가루로, 활물질에 건식 코팅도 해 봤어요.", caps=["같은 가루로", "활물질에 건식 코팅도 해 봤어요"],
       pause=0.35, speed=1.02)
g5 = L("그러자 접착일을 포함한 기계적 성질이, 붙지 않고 남은 고체전해질 비율과 함께 변했습니다.",
       caps=["그러자 접착일을 포함한 기계적 성질이", "붙지 않고 남은 고체전해질 비율과", "함께 변했습니다"], pause=0.4,
       emph=["함께 변했습니다"])
g6 = L("저자들은, 부착이 중요한 역할을 한다고 제안했고요.", caps=["저자들은", "부착이 중요한 역할을 한다고 제안했고요"],
       pause=0.6, emph=["제안"])
g7 = L("다만 이건 실리콘 탐침과 재료 사이의 힘입니다.", caps=["다만 이건", "실리콘 탐침과 재료 사이의 힘입니다"],
       pause=0.45, emo="진지")
g8 = L("고체전해질끼리, 그리고 고체전해질과 활물질 사이의 힘을 같은 탐침으로 견준 자료는요.",
       caps=["고체전해질끼리, 그리고", "고체전해질과 활물질 사이의 힘을", "같은 탐침으로 견준 자료는요"], pause=0.3)
g9 = L("저희가 살펴본 문헌 안에서는, 아직 보지 못했습니다.", caps=["저희가 살펴본 문헌 안에서는", "아직 보지 못했습니다"],
       pause=1.45, emph=["아직"], memo="절 끝 · 범위 한정 표현 그대로")
TX2, TY2 = 760, 330
SHOT("s07a", g1, [
    cantilever("cant2", g1 + "~힘을", tipx=TX2, tipy=TY2, label="실리콘 탐침", part_color="ink"),
    rect("pellet", 760, SLAB_Y + 25, 520, 50, g1 + "~황화물", fill="lavfill", stroke="ink", sw=2,
         label="황화물 고체전해질 펠릿", ls=24),
    *[rect(f"sw{i}", 600 + 80 * i, SLAB_Y + 105, 56, 30, g2 + "~다섯", fill="indigo" if i == 2 else "lav", stroke=None)
      for i in range(5)],
    text("t_sw", 760, SLAB_Y + 155, "다섯 조성", g2 + "~다섯", size=24, color="grey", weight="semibold"),
    src("src_ylee", "Y. Lee 외, ACS Nano (2026) · doi 10.1021/acsnano.6c09375 · 저희 연구실 공저 · 원자힘현미경 힘 분광 (실리콘 탐침)", g2),
], pre=0.4)
SH = EP["scenes"][-1]["shots"][-1]
c2 = SH["elements"][0]
c2["moves"] = [dict(at=g3 + "~눌렀다", dur=0.45, x=TX2, y=SLAB_Y - 17), dict(at=g3 + "~떼면서", dur=0.45, x=TX2, y=TY2)]
fx, fy = 1300, 360
SH["elements"] += [
    line("fc2_ax", [(fx - 20, fy), (fx + 300, fy)], g3 + "~떼면서", sw=2, color="grey", dur=0.3),
    line("fc2_a", [(fx, fy), (fx + 170, fy), (fx + 215, fy + 6), (fx + 232, fy - 60)], g3 + "~떼면서", sw=3, dur=0.5),
    area("fc2_area", [(fx + 215, fy), (fx + 200, fy + 92), (fx + 190, fy + 2), (fx + 215, fy)], g3 + "~접착일과",
         fill="lav"),
    line("fc2_r", [(fx + 232, fy - 60), (fx + 215, fy + 6), (fx + 200, fy + 92), (fx + 190, fy + 2), (fx + 40, fy + 2)],
         g3 + "~떼면서+0.4", sw=3, color="indigo", dur=0.6),
    text("fc2_wad", fx + 268, fy + 120, "접착일 = 이 넓이", g3 + "~접착일과", size=24, color="indigo"),
    text("fc2_e", fx + 300, fy - 70, "단단함 = 기울기", g3 + "~단단함을", size=24, color="ink"),
]
att2 = shell(16, 840, 480, 140, 13, a0=0, a1=360, gap=1.0)
loose = scatter(7, (1040, 360, 1230, 640), 13, seed=44)
SHOT("s07b", g4, [
    circle("g_ncm", 840, 480, 140, g4 + "+0.3", label="활물질", ls=30),          # 11-25: was "~활물질에" (1.2 s empty start)
    dots("g_att", att2, g4 + "~코팅도", stagger=0.02),
    dots("g_loose", loose, g5 + "~남은", fill="lav", stagger=0.04),
    text("t_loose", 1135, 680, "붙지 않고 남은 고체전해질", g5 + "~남은", size=26, color="grey"),
    number("n_resid", 1480, 420, 0.246, g5 + "~비율과", size=64, color="indigo", decimals=3, start=0.0,
           display="0.094 – 0.246", anim="fade"),
    text("t_resid", 1480, 466, "남은 SE 분율 · 다섯 조성", g5 + "~비율과", size=24, color="grey", weight="semibold"),
    text("t_cov", 1480, 545, "접착일 · 단단함 · 항복 강도가\n함께 변함", g5 + "~함께", size=26, color="ink"),
    chip("c_prop", 1480, 650, "저자 제안: 부착의 역할", g6 + "~부착이", size=26, color="indigo", stroke="indigo"),
    src("src_ylee2", "Y. Lee 외, ACS Nano (2026) · 저희 연구실 공저 · 공명 음향 혼합기 건식 코팅 (활물질 : SE = 100 : 2) · Table S1", g4),
])
SHOT("s07c", g7, [
    chip("c_sil", 960, 230, "실리콘 탐침 ↔ 재료", g7 + "~실리콘", size=28, color="ink"),
    rect("pr1", 560, 440, 360, 120, g8 + "~고체전해질끼리", fill=None, stroke="ink", dash=[10, 7], label="고체전해질 ↔ 고체전해질", ls=24),
    rect("pr2", 960, 440, 360, 120, g8 + "~활물질", fill=None, stroke="ink", dash=[10, 7], label="고체전해질 ↔ 활물질", ls=24),
    rect("pr3", 1360, 440, 360, 120, g8 + "~같은", fill=None, stroke="ink", dash=[10, 7], label="고체전해질 ↔ 코팅한 활물질",
         ls=24),
    *[text(f"prq{i}", x, 545, "?", g9 + "~아직", size=48, color="indigo") for i, x in enumerate((560, 960, 1360))],
    text("t_same_probe", 960, 335, "같은 고체전해질 탐침으로", g8 + "~같은", size=30, color="ink"),
    text("t_scope", 960, 650, "저희가 살펴본 문헌 안: 아직 못 봄", g9 + "~살펴본", size=26, color="grey", weight="semibold"),
])

# ============================================================================
# S08  더 세게 섞으면
# ============================================================================
scene("s08", "더 세게 섞으면 — 칼날 혼합기 실험")
h1 = L("그럼, 더 세게 섞으면 해결될까요?", caps=["그럼, 더 세게 섞으면 해결될까요?"], pause=0.85, speed=0.97, emo="궁금")
h2 = L("일본의 한 연구진은, 칼날이 빠르게 도는 혼합기로 두 가루를 섞어 봤습니다.",
       caps=["일본의 한 연구진은", "칼날이 빠르게 도는 혼합기로", "두 가루를 섞어 봤습니다"], pause=0.4)
h3 = L("칼날을 일 분에 오천 번 돌리다가, 이만 오천 번까지 올렸죠.",
       caps=["칼날을 1분에 5천 번 돌리다가", "2만 5천 번까지 올렸죠"], pause=0.4, speed=0.95, emph=["오천", "이만 오천"])
h4 = L("빠를수록 덩어리가 풀렸고, 가장 빠를 때는 작은 가루 대부분이 활물질 위에 붙었어요.",
       caps=["빠를수록 덩어리가 풀렸고", "가장 빠를 때는 작은 가루 대부분이", "활물질 위에 붙었어요"], pause=0.5)
h5 = L("그런데 일부는, 혼합기 벽에 달라붙어 버렸습니다.", caps=["그런데 일부는", "혼합기 벽에 달라붙어 버렸습니다"],
       pause=0.45, emo="진지", emph=["벽"])
h6 = L("계산해 보면, 가장 빠를 때 넣은 고체전해질의 이십칠 퍼센트쯤이 빠져나간 셈이에요.",
       caps=["계산해 보면, 가장 빠를 때", "넣은 고체전해질의 27 %쯤이", "빠져나간 셈이에요"], pause=0.7, speed=0.94,
       emo="강조", emph=["이십칠 퍼센트"])
h7 = L("그리고 이온이 통하는 정도는, 회전 속도와 상관없이 거의 그대로였죠.",
       caps=["그리고 이온이 통하는 정도는", "회전 속도와 상관없이 거의 그대로였죠"], pause=0.45, emph=["그대로"])
h8 = L("저자들은 그 이유로, 혼합물 속 고체전해질 양이 달라진 점을 들었어요.",
       caps=["저자들은 그 이유로", "혼합물 속 고체전해질 양이 달라진 점을", "들었어요"], pause=0.45)
h9 = L("세게 섞는다고, 늘 답이 되는 건 아니라는 거죠.", caps=["세게 섞는다고", "늘 답이 되는 건 아니라는 거죠"],
       pause=0.5)
h10 = L("분체 연구들에서도, 세게 저을수록 좋은지는 조건에 따라 엇갈리고요.",
        caps=["분체 연구들에서도", "세게 저을수록 좋은지는", "조건에 따라 엇갈리고요"], pause=1.45, memo="절 끝")


def panel(cx, cy, mode, seed):
    big = [(cx - 42, cy - 28, 40), (cx + 46, cy + 34, 40)]
    el = []
    if mode == 0:
        se = cluster(16, cx + 30, cy - 60, 8, seed=seed)
    elif mode == 1:
        se = cluster(8, cx + 40, cy - 66, 8, seed=seed) + shell(6, cx - 42, cy - 28, 40, 8, a0=160, a1=260)
    else:
        se = shell(8, cx - 42, cy - 28, 40, 8, a0=120, a1=330) + shell(8, cx + 46, cy + 34, 40, 8, a0=-60, a1=150)
    return big, se


pans = [(1060, 455), (1290, 455), (1520, 455)]
labels = ["5천", "1만 2천 5백", "2만 5천"]
els = [mixer("mx1", 600, 460, 175, h1 + "~세게", spin=[[h1 + "~세게", h4 + "$", 0.5]]),
       number("n_rpm", 600, 740, 25000, h3 + "~오천", unit="rpm", size=64, start=5000, color="indigo",
              display="5천 → 2만 5천", anim="fade"),
       text("t_rpm", 600, 785, "칼날 회전 (1분당)", h3 + "~오천", size=24, color="grey", weight="semibold")]
anchors = [h3 + "~오천", h3 + "~이만", h4 + "~가장"]
for k, (cx, cy) in enumerate(pans):
    big, se = panel(cx, cy, k, seed=50 + k)
    for j, (x, y, r) in enumerate(big):
        els.append(circle(f"pn{k}{j}", x, y, r, anchors[k], label=None))
    els.append(dots(f"pse{k}", se, anchors[k], stagger=0.015))
    els.append(text(f"pl{k}", cx, 580, labels[k], anchors[k], size=24, color="grey", weight="semibold"))
els.append(text("t_sem", 1290, 640, "전자현미경으로 본 모습 (정성)", h4 + "~덩어리가", size=24, color="grey", weight="semibold"))
els.append(src("src_hay_mix", "Hayakawa · Nakamura · Ohsaki · Watano, Adv. Powder Technol. 33, 103705 (2022) · 활물질 : SE = 84 : 16 · 30분", h2))
SHOT("s08a", h1, els, pre=0.4)
wall = shell(22, 600, 460, 175, 9, a0=-80, a1=200, gap=-1.05)
SHOT("s08b", h5, [
    keep("mx1", x=600, y=460),
    dots("wall_se", wall, h5 + "~벽에", stagger=0.02),
    text("t_wall", 600, 680, "벽에 붙은 고체전해질", h5 + "~벽에", size=26, color="indigo"),
    number("n_loss", 1270, 420, 27.1, h6 + "~이십칠", unit="%", decimals=1, size=96, color="indigo"),
    text("t_loss", 1270, 472, "넣은 고체전해질 대비 (가장 빠를 때)", h6 + "~이십칠", size=24, color="grey", weight="semibold"),
    text("t_loss2", 1270, 560, "혼합물 속 고체전해질 16 → 12.2 wt%", h6 + "~넣은", size=28, color="ink"),
    src("src_hay_loss", "Hayakawa 외 (2022) · 순 조성 16 → 12.2 wt% (측정) · 27.1 % = 카드 산술 (활물질 손실 0 가정)", h6),
])
sig = [4.28, 4.90, 4.25]
sd = [1.03, 0.90, 0.69]
bx2 = [640, 820, 1000]
sc2 = 300 / 6.0
bars = []
for i in range(3):
    hpx = sig[i] * sc2
    bars.append(rect(f"sg{i}", bx2[i], 700 - hpx / 2, 110, hpx, h7 + "~이온이", fill="indigo" if i == 2 else "ink",
                     stroke=None, anim="grow", grow_dir="y"))
    bars.append(line(f"eb{i}", [(bx2[i], 700 - (sig[i] + sd[i]) * sc2), (bx2[i], 700 - (sig[i] - sd[i]) * sc2)],
                     h7 + "~통하는", sw=2.5, color="grey", anim="fade"))
    bars.append(text(f"sgv{i}", bx2[i], 700 - (sig[i] + sd[i]) * sc2 - 26, f"{sig[i]:.2f}", h7 + "~통하는", size=26))
    bars.append(text(f"sgl{i}", bx2[i], 735, labels[i], h7 + "~이온이", size=22, color="grey", weight="semibold"))
SHOT("s08c", h7, [
    line("sg_ax", [(560, 700), (1080, 700)], h7 + "~이온이", sw=2.5, dur=0.4),
    *bars,
    text("sg_y", 560, 285, "이온 전도도 (× 10⁻⁵ S/cm) · 막대 = 표준편차", h7 + "~이온이", size=24, color="grey",
         align="left", weight="semibold"),
    text("sg_same", 820, 780, "오차 안에서 거의 같음", h7 + "~그대로였죠", size=26, color="ink"),
    chip("c_why", 820, 220, "분산 ↑  ·  그러나 고체전해질 양 ↓", h8 + "~달라진", size=26, color="ink"),
    chip("c_li06", 1420, 400, "느리게 저을 때 더 섞임", h10 + "~세게", size=26, color="ink"),
    text("c_li06b", 1420, 448, "액체로 적신 유리구슬 · 실험", h10 + "~세게", size=22, color="grey", weight="semibold"),
    chip("c_ch06", 1420, 560, "점착이 셀 때 빠른 회전이 조금 나음", h10 + "~엇갈리고요", size=26, color="ink"),
    text("c_ch06b", 1420, 608, "회전당 · 계산", h10 + "~엇갈리고요", size=22, color="grey", weight="semibold"),
    src("src_sig", "Hayakawa 외 (2022) 그림 5 에서 읽은 값 · Li · McCarthy, Powder Technol. 164, 58 (2006) · Chaudhuri 외, Powder Technol. 165, 105 (2006)", h7),
])

# ============================================================================
# S09  눌린 뒤에도 — 열린 질문
# ============================================================================
scene("s09", "눌린 뒤의 이온 길 — 아직 열린 질문")
i1 = L("이제 남은 질문이 하나 있습니다.", pause=0.4, speed=1.0, emo="진지",
       memo="v2.1: '가장 궁금한' (최상급) 을 뺌")
i2 = L("잘 섞인 가루는, 꾹 눌러 전극이 된 뒤에도, 더 좋은 이온 길을 만들까요?",
       caps=["잘 섞인 가루는", "꾹 눌러 전극이 된 뒤에도", "더 좋은 이온 길을 만들까요?"], pause=0.9, speed=0.96, emo="궁금",
       emph=["눌러", "이온 길"])
i3 = L("독일의 다른 연구진은, 같은 조성의 전극을 두 가지 공정으로 만들었어요.",
       caps=["독일의 다른 연구진은", "같은 조성의 전극을", "두 가지 공정으로 만들었어요"], pause=0.4)
i4 = L("한쪽에서는, 고체전해질이 활물질 표면을 납작하게 덮었는데요.",
       caps=["한쪽에서는", "고체전해질이 활물질 표면을", "납작하게 덮었는데요"], pause=0.35)
i5 = L("빈틈 비율이 같은데도, 이온 전도도가 세 배 높았습니다.", caps=["빈틈 비율이 같은데도", "이온 전도도가 세 배 높았습니다"],
       pause=0.6, speed=0.94, emo="강조", emph=["세 배"])
i6 = L("하지만 두 공정은 온도도, 시간도, 에너지도 달라서, 그 차이를 덮임 하나로 가를 수는 없었어요.",
       caps=["하지만 두 공정은", "온도도, 시간도, 에너지도 달라서", "그 차이를 덮임 하나로", "가를 수는 없었어요"], pause=0.55,
       emo="진지")
i7 = L("앞에서 본 것처럼, 분산이 좋아져도 이온 전도도는 그대로인 경우도 있었고요.",
       caps=["앞에서 본 것처럼", "분산이 좋아져도 이온 전도도는", "그대로인 경우도 있었고요"], pause=0.45)
i8 = L("그래서 덮임과 뭉침이 눌린 뒤의 이온 길을 얼마나 바꾸는지는, 아직 열린 질문입니다.",
       caps=["그래서 덮임과 뭉침이", "눌린 뒤의 이온 길을 얼마나 바꾸는지는", "아직 열린 질문입니다"], pause=1.4,
       emph=["열린 질문"], memo="절 끝 (v2: 옛 i9 · i10 은 S10 으로 옮겨 늘림)")
# v2 (11-24 · 1저자 "믹서 avi에 지금 내용도 추가해봐"): the old i9 ("저희 연구실도 이 질문을 …") and
# i10 ("그 계산을 믿으려면 …") moved to the new S10, which states WHAT is compared and WHY only —
# no result, number, direction or simulation picture (public-safety rule · results after publication).
bed_c = [(820, 600), (950, 640), (1080, 595), (885, 715), (1030, 720)]
SHOT("s09a", i1, [
    circle("q_big", 960, 450, 92, i1 + "+0.25", fill=None, stroke="indigo", sw=3, dash=[10, 8], label="?", ls=70,
           lc="indigo", out=i2 + "~가루는"),
    rect("press", 960, 300, 470, 42, i2 + "~꾹", fill="ink", stroke=None,
         moves=[dict(at=i2 + "~눌러", dur=0.8, y=500)]),
    line("press_ar", [(960, 190), (960, 260)], i2 + "~꾹", arrow="end", sw=3, moves=[dict(at=i2 + "~눌러", dur=0.8, y=190)]),
    rect("bed_box", 960, 640, 480, 230, i2 + "~가루는", fill=None, stroke="ink", sw=2.5),
    *[circle(f"bed{k}", x, y, 52, i2 + "~가루는", label=None) for k, (x, y) in enumerate(bed_c)],
    dots("bed_se", scatter(26, (730, 540, 1190, 745), 11, seed=61, avoid=[(x, y, 52) for x, y in bed_c], mind=2.2),
         i2 + "~가루는", stagger=0.01),
    line("bed_path", [(760, 750), (790, 680), (950, 670), (990, 590), (1150, 560), (1190, 532)], i2 + "~이온", color="indigo",
         sw=3, dash=[10, 8], dur=0.9),
    circle("bed_q", 1250, 520, 40, i2 + "~만들까요", fill=None, stroke="indigo", sw=2.5, dash=[8, 6], label="?", ls=38,
           lc="indigo"),
], pre=0.4)


def coated(cx, cy, r, at, k, flat=True):
    out = [circle(f"wf{k}", cx, cy, r, at, label=None)]
    if flat:
        out.append(circle(f"wfs{k}", cx, cy, r + 5, at, fill=None, stroke="indigo", sw=8))
    return out


wolfA = [(560, 430), (690, 470), (610, 560)]
wolfB = [(1230, 430), (1360, 470), (1280, 560)]
elsW = [text("t_procA", 625, 290, "공정 A · 압출 혼합", i3 + "+0.3", size=30),
        text("t_procB", 1295, 290, "공정 B · 배치 혼합", i3 + "+0.5", size=30)]
for k, (x, y) in enumerate(wolfA):
    elsW += coated(x, y, 52, i4 + "~납작하게", k, flat=True)
for k, (x, y) in enumerate(wolfB):
    elsW += [circle(f"wb{k}", x, y, 52, i3 + "+0.7", label=None)]
elsW += [dots("wb_se", scatter(14, (1150, 360, 1450, 630), 10, seed=71, avoid=[(x, y, 52) for x, y in wolfB], mind=2.2),
              i3 + "+0.9", stagger=0.02),
         text("t_poro", 960, 660, "빈틈 비율  16.1 %  ↔  16.3 %", i5 + "~빈틈", size=30),
         number("n_wA", 625, 760, 0.022, i5 + "~이온", unit="mS/cm", decimals=3, size=58, color="indigo", start=0.0),
         number("n_wB", 1295, 760, 0.0072, i5 + "~이온", unit="mS/cm", decimals=4, size=58, color="ink", start=0.0),
         text("t_x3", 960, 745, "약 3배", i5 + "~세", size=40, color="indigo"),
         chip("c_conf", 960, 200, "온도 · 시간 · 에너지도 다름 → 덮임 하나로 가를 수 없음", i6 + "~온도도", size=26, color="ink"),
         src("src_wolf", "Wolf 외, Adv. Sci. (2026) e78248 · 이온 전도도 = 그림 5 에서 읽은 값 · 같은 조성 · 압출 ≈300 ↔ 배치 7140 kJ/kg", i3)]
SHOT("s09b", i3, elsW)
nodes = [(560, "섞기"), (850, "덮임 · 뭉침"), (1140, "누르기"), (1430, "이온 길")]
elsC = []
for k, (x, lab) in enumerate(nodes):
    if k < 3:
        elsC.append(circle(f"nd{k}", x, 450, 78, i7 + "~앞에서" if k < 2 else i7 + "~분산이", fill="indigo" if k == 0 else "ink",
                           label=lab, ls=26))
    else:
        elsC.append(circle(f"nd{k}", x, 450, 78, i8 + "~이온", fill=None, stroke="indigo", sw=3, dash=[9, 7], label=lab,
                           ls=26, lc="indigo"))
for k in range(3):
    x0 = nodes[k][0] + 88
    x1 = nodes[k + 1][0] - 92
    elsC.append(line(f"ndl{k}", [(x0, 450), (x1, 450)], (i7 + "~앞에서") if k < 2 else (i8 + "~이온"), arrow="end", sw=3,
                     dash=[9, 7] if k == 2 else None))
elsC += [text("t_q", 1430, 575, "?", i8 + "~열린", size=56, color="indigo"),
         text("t_hay", 1290, 690, "분산 ↑ · 이온 전도도 그대로인 사례 (Hayakawa 외 2022)", i7 + "~그대로인", size=24,
              color="grey", weight="semibold")]
SHOT("s09c", i7, elsC)

# ============================================================================
# S10  (v2 새 장면) 같은 출발, 끈적함만 다르게 — 저희 연구실의 계산
#      WHAT is compared + WHY only.  No result · number · direction · our simulation picture.
#      Screen = newly drawn schematics.  Method background = cards already in this episode's list.
# ============================================================================
scene("s10", "같은 출발, 끈적함만 다르게 — 저희 연구실의 계산")
k1 = L("저희 연구실은 이 사슬의 앞쪽, 섞는 동안 누가 누구와 붙는지부터 따져 보고 있어요.",
       caps=["저희 연구실은 이 사슬의 앞쪽", "섞는 동안 누가 누구와 붙는지부터", "따져 보고 있어요"], pause=0.45,
       emph=["누가 누구와"], memo="우리 연구실 이야기 시작 · 담백하게 · 홍보 말투 아님")
k2 = L("입자 시뮬레이션으로, 돌아가는 원통 안에서 섞는 계산을 둘씩 짝지어 견주는데요.",
       caps=["입자 시뮬레이션으로", "돌아가는 원통 안에서 섞는 계산을", "둘씩 짝지어 견주는데요"], pause=0.35, speed=1.02)
k3 = L("짝마다 출발 배치는 똑같고, 활물질 표면의 끈적함만 다릅니다.",   # 11-25 1저자 권고대로: "다르죠" = 세 판 모두 높음
       caps=["짝마다 출발 배치는 똑같고", "활물질 표면의 끈적함만 다릅니다"], pause=0.45, emph=["끈적함만"],
       memo="끝 꼴: 앞 두 문장이 ~요 → ~죠")
k4 = L("그래야 출발 배치의 차이로 결과가 갈리는 일을 막을 수 있거든요.",
       caps=["그래야 출발 배치의 차이로", "결과가 갈리는 일을 막을 수 있거든요"], pause=0.55,
       memo="'왜 같은 출발' · 설명하는 말투")
k5 = L("그리고 고체전해질끼리 뭉친 알갱이와, 활물질에 닿은 알갱이를 따로 셉니다.",
       caps=["그리고 고체전해질끼리 뭉친 알갱이와", "활물질에 닿은 알갱이를 따로 셉니다"], pause=0.45, emph=["따로"],
       memo="'닿은' 그대로 (덮였다 · 붙어 있다로 바꾸지 않기)")
k6 = L("칸마다 고르게 섞였는지만 보면, 붙어서 고른 건지, 뭉친 채 고른 건지 가리기 어렵거든요.",
       caps=["칸마다 고르게 섞였는지만 보면", "붙어서 고른 건지, 뭉친 채 고른 건지", "가리기 어렵거든요"], pause=0.6,
       speed=0.98, emph=["가리기 어렵거든요"], memo="'왜 두 가지를 세나' · 두 '건지' 를 대비")
k7 = L("그중 한 짝은, 결과를 열기 전에 예상 방향을 먼저 적어 두었어요.",
       caps=["그중 한 짝은", "결과를 열기 전에", "예상 방향을 먼저 적어 두었어요"], pause=0.4, emph=["먼저"],
       memo="방향 자체는 말하지 않는다")
k8 = L("결과는 논문으로 공개한 뒤에 보여드릴게요.", caps=["결과는 논문으로 공개한 뒤에", "보여드릴게요"], pause=0.6,
       speed=1.02, emo="밝게")
k9 = L("다만 그 계산을 믿으려면, 끈적함 입력부터 가루 사이의 힘을 직접 재서 정해야 하죠.",
       caps=["다만 그 계산을 믿으려면", "끈적함 입력부터", "가루 사이의 힘을 직접 재서 정해야 하죠"], pause=1.4,
       emph=["직접 재서"], memo="절 끝 (v1 의 i10 을 고친 꼴)")
SHOT("s10a", k1, [
    keep("nd0"), keep("nd1"), keep("ndl0"),                       # the front of the chain stays sharp
    *[keep(f"nd{k}", state="dim") for k in (2, 3)],
    *[keep(f"ndl{k}", state="dim") for k in (1, 2)],
    keep("t_q", state="dim"),
    rect("front_box", 705, 450, 530, 220, k1 + "~앞쪽", fill=None, stroke="indigo", sw=4, radius=26),
    text("t_lab", 705, 605, "저희 연구실: 여기부터 계산으로", k1 + "~섞는", size=28, color="indigo"),
    text("t_lab2", 705, 650, "섞는 동안 누가 누구와 붙나", k1 + "~누가", size=24, color="grey", weight="semibold"),
], pre=0.3)
# two rotating drums with the SAME starting bed (identical relative coordinates)
DR = 170
DL, DRR, DY = (690, 480), (1230, 480), 480


def _bed(seed=81):
    rnd = random.Random(seed)
    am, se = [], []
    tries = 0
    while len(am) < 6 and tries < 5000:
        tries += 1
        x, y = rnd.uniform(-DR, DR), rnd.uniform(0.18 * DR, DR)
        if math.hypot(x, y) > DR - 26 - 6 or any(math.hypot(x - a, y - b) < 2 * 26 + 6 for a, b, _ in am):
            continue
        am.append((x, y, 26))
    tries = 0
    while len(se) < 46 and tries < 20000:
        tries += 1
        x, y = rnd.uniform(-DR, DR), rnd.uniform(0.10 * DR, DR)
        if math.hypot(x, y) > DR - 9 - 6:
            continue
        if any(math.hypot(x - a, y - b) < 26 + 9 + 3 for a, b, _ in am) or any(math.hypot(x - a, y - b) < 2 * 9 + 3 for a, b, _ in se):
            continue
        se.append((x, y, 9))
    return am, se


bed_am, bed_se = _bed()


def _arc(cx, cy, R, a0, a1, n=24):
    return [(round(cx + R * math.cos(math.radians(a0 + (a1 - a0) * i / n)), 1),
             round(cy + R * math.sin(math.radians(a0 + (a1 - a0) * i / n)), 1)) for i in range(n + 1)]


dr_els = [chip("c_drum", 960, 195, "회전 드럼 계산 · 둘씩 짝지어 견주기", k2 + "+0.1", size=30, color="ink")]   # at line start: no blank screen while '입자 시뮬레이션으로' is said
for tag, (cx, cy), lab, colr in (("L", DL, "활물질 표면: 덜 끈적", "ink"), ("R", DRR, "활물질 표면: 더 끈적", "indigo")):
    d0 = 0.0 if tag == "L" else 0.25          # right drum a beat later (offsets are not chained: one +x per anchor)
    dr_els += [
        circle(f"drum{tag}", cx, cy, DR, f"{k2}~원통+{d0:.2f}", fill=None, stroke="ink", sw=4, anim="fade"),
        line(f"rot{tag}", _arc(cx, cy, DR + 26, -150, -30), k2 + "~짝지어", color="grey", sw=3, arrow="end", dur=0.6),
        dots(f"bam{tag}", [(cx + x, cy + y, r) for x, y, r in bed_am], f"{k2}~원통+{d0 + 0.2:.2f}", fill="ink", stagger=0.03),
        dots(f"bse{tag}", [(cx + x, cy + y, r) for x, y, r in bed_se], f"{k2}~원통+{d0 + 0.35:.2f}", fill="indigo",
             stagger=0.008),
        text(f"t_dr{tag}", cx, 700, lab, k3 + "~끈적함만", size=28, color=colr),
    ]
dr_els += [
    text("t_eq", 960, 470, "=", k3 + "~출발", size=72, color="indigo", weight="extrabold"),
    text("t_eq2", 960, 540, "출발 배치 같음", k3 + "~출발", size=24, color="indigo", weight="semibold"),
    chip("t_nocoat", 960, 765, "코팅 과정을 계산한 것이 아니라, 끈적함 입력만 다르다", k3 + "~끈적함만+0.7", size=26,
         color="ink", stroke="grey"),          # on screen only (not spoken) -> a box, ink, readable on a phone
    src("src_drum", "개념도 (저희 계산 화면 아님 · 계산 속 공 하나 = 실제 알갱이 여러 개)\n"
        "방법의 바탕: 회전 드럼에서 점착을 바꿔 본 계산 Chaudhuri 외, Powder Technol. 165, 105 (2006) · 쌍별 본드 수 Figueroa 외 (2009)",
        k2, y=858),
]
SHOT("s10b", k2, dr_els)
# what is counted (definitions only — schematic, not a result)
cnt_touch = shell(9, 700, 470, 140, 14, a0=-55, a1=55)
cnt_clu = cluster(11, 1180, 365, 14, seed=27)
cnt_loose = [(1050, 610, 14), (1290, 585, 14), (1200, 680, 14)]
SHOT("s10c", k5, [
    circle("cn_am", 700, 470, 140, k5 + "+0.2", label="활물질", ls=32),
    dots("cn_touch", cnt_touch, k5 + "~활물질에", stagger=0.03),
    circle("cn_touch_ring", 700, 470, 172, k5 + "~닿은", fill=None, stroke="indigo", sw=2.5, dash=[9, 7], anim="fade"),
    text("t_cn2", 700, 690, "② 활물질에 닿은 알갱이", k5 + "~닿은", size=28, color="indigo"),
    dots("cn_clu", cnt_clu, k5 + "~고체전해질끼리", stagger=0.03),
    circle("cn_clu_ring", 1180, 365, 78, k5 + "~뭉친", fill=None, stroke="indigo", sw=2.5, dash=[9, 7], anim="fade"),
    text("t_cn1", 1180, 255, "① 고체전해질끼리 뭉친 알갱이", k5 + "~뭉친", size=28, color="indigo"),
    dots("cn_loose", cnt_loose, k5 + "~닿은", fill="lav", stagger=0.05),          # 11-25: was "~따로" (0.9 s on screen)
    text("t_cn0", 1180, 750, "두 가지를 따로 센다 (정의 · 개념도)", k5 + "+0.5", size=24, color="grey", weight="semibold"),  # 11-25: was "~셉니다" (0.5 s flash) — the panel note with the panel
], pre=0.4)
# why two counts: one cell with the same composition, two different insides
cellL, cellR = (720, 470), (1200, 470)
amL = [(650, 405), (790, 535)]
amR = [(1130, 405), (1270, 535)]
inL = []
for k, (x, y) in enumerate(amL):
    inL += shell(8, x, y, 46, 10, a0=k * 20, a1=360)
inR = cluster(8, 1272, 393, 10, seed=33) + cluster(8, 1128, 548, 10, seed=34)
why = [chip("c_same_comp", 960, 200, "칸 하나로 보면: 조성은 같다", k6 + "~고르게", size=28, color="ink")]
for tag, (cx, cy), ams, ins, lab, at in (("L", cellL, amL, inL, "붙어서 고름", k6 + "~붙어서"),
                                          ("R", cellR, amR, inR, "뭉친 채 고름", k6 + "~뭉친")):
    why += [rect(f"cell{tag}", cx, cy, 340, 340, k6 + "~칸마다", fill=None, stroke="ink", sw=2.5, dash=[10, 7]),
            dots(f"cam{tag}", [(x, y, 46) for x, y in ams], k6 + "~칸마다+0.3", fill="ink", stagger=0.08),
            dots(f"cse{tag}", ins, at, stagger=0.02),
            text(f"t_cell{tag}", cx, 685, lab, at, size=30, color="indigo")]
why += [text("t_cell_eq", 960, 470, "=", k6 + "~고르게", size=60, color="grey", weight="extrabold"),
        chip("c_two", 960, 765, "그래서 두 가지를 따로 센다", k6 + "~가리기", size=28, color="indigo", stroke="indigo")]
SHOT("s10d", k6, why, pre=0.4)
note_lines = [line(f"nt{k}", [(600, 375 + 32 * k), (800 - 40 * (k == 2), 375 + 32 * k)], k7 + "~예상", sw=3, color="grey",
                   dur=0.35) for k in range(3)]
SHOT("s10e", k7, [
    rect("note", 700, 410, 300, 190, k7 + "~한", fill=None, stroke="ink", sw=3),
    *note_lines,
    text("t_note", 700, 560, "한 짝: 예상 방향을 먼저 적어 둠", k7 + "~예상", size=28),
    line("ar_note", [(880, 410), (1040, 410)], k7 + "~먼저", arrow="end", sw=3),
    rect("res_box", 1220, 410, 300, 190, k8 + "~결과는", fill=None, stroke="indigo", sw=3, dash=[10, 7]),
    text("t_res_q", 1220, 410, "?", k8 + "~결과는", size=80, color="indigo", weight="extrabold"),
    text("t_res", 1220, 560, "결과 · 논문으로 공개한 뒤", k8 + "~논문으로", size=28, color="indigo"),
    chip("c_meas", 960, 700, "끈적함 입력  ←  가루 사이의 힘을 직접 재기", k9 + "~끈적함", size=30, color="indigo",
         stroke="indigo"),
    text("t_meas2", 960, 760, "(앞에서 본 원자힘현미경 측정 같은 것)", k9 + "~직접", size=24, color="grey", weight="semibold"),
], pre=0.4)

# ============================================================================
# S11  정리 · 다음 편   (v1 의 S10 · v2 에서 번호만 바뀜)
# ============================================================================
scene("s11", "정리 · 다음 편")
j1 = L("오늘 이야기를 정리해 볼게요.", pause=0.45, speed=1.0, emo="정리")
j2 = L("고운 가루는, 무게보다 끈적함을 따라 움직이고요.", caps=["고운 가루는", "무게보다 끈적함을 따라 움직이고요"],
       pause=0.4, speed=0.97, emo="정리")
j3 = L("누구와 붙을지는, 끈적함의 비율만이 아니라, 끈적함의 크기와 알갱이 크기, 그리고 섞는 방식이 함께 정합니다.",
       caps=["누구와 붙을지는", "끈적함의 비율만이 아니라", "끈적함의 크기와 알갱이 크기", "그리고 섞는 방식이 함께 정합니다"],
       pause=0.55, speed=0.95, emo="정리", emph=["함께"])
j4 = L("그리고 그 차이가 눌린 뒤의 이온 길까지 바꾸는지는, 아직 열려 있습니다.",
       caps=["그리고 그 차이가", "눌린 뒤의 이온 길까지 바꾸는지는", "아직 열려 있습니다"], pause=0.8, emo="정리")
j5 = L("여러분이라면, 가루 사이의 힘부터 재시겠어요, 아니면 일단 섞어 보시겠어요?",
       caps=["여러분이라면", "가루 사이의 힘부터 재시겠어요", "아니면 일단 섞어 보시겠어요?"], pause=1.0, speed=0.96,
       emo="궁금", memo="시청자에게 묻기 · 끝 올림")
j6 = L("다음 편에서는, 눌린 알갱이들이 맞닿은 자리에서 생기는 저항 이야기를 해 보겠습니다.",
       caps=["다음 편에서는", "눌린 알갱이들이 맞닿은 자리에서 생기는", "저항 이야기를 해 보겠습니다"], pause=0.8, speed=1.0,
       emo="밝게", memo="끝 인사 느낌으로 가볍게")
import avi_style as _S  # noqa: E402
_f = _S.font("extrabold", 92)
EX, EY1, EY2 = 300, 420, 548
_w_hl = _f.getlength("끼리끼리")
_w_sp = _f.getlength(" ")
OBJ = "assets/powder_obj.png"   # 편 폴더 기준 상대 경로 (avi_timeline.load 가 푼다 · scenes.json 에 절대 경로를 남기지 않는다)
END_CARD = [
    text("end_l1", EX, EY1, "가루는 왜", j6 + "$+0.9", size=92, weight="extrabold", align="left"),
    rect("end_band", EX + _w_hl / 2, EY2 + 30, _w_hl + 14, 46, j6 + "$+1.0", fill="lavfill", stroke=None),
    text("end_l2a", EX, EY2, "끼리끼리", j6 + "$+1.0", size=92, weight="extrabold", color="indigo", align="left"),
    text("end_l2b", EX + _w_hl + _w_sp, EY2, "뭉칠까", j6 + "$+1.0", size=92, weight="extrabold", align="left"),
    text("end_sub", EX, 650, EP["series"] + " · 1편", j6 + "$+1.2", size=30, color="grey", weight="semibold", align="left"),
    dict(id="end_obj", type="image", path=OBJ, x=1340, y=500, at=j6 + "$+1.1", anim="fade", dur=0.5),
]
SHOT("s11a", j1, [
    text("sum0", 960, 190, "오늘의 정리", j1 + "+0.1", size=34, color="grey"),   # v2.1: at line start (was ~정리 -> 0.9 s caption-only)
    chip("sum1", 960, 300, "고운 가루 : 끈적함이 무게를 이긴다", j2 + "~고운", size=32, color="ink"),
    chip("sum2", 960, 420, "누구와 붙나 : 힘의 비율 + 끈적함의 크기 + 알갱이 크기 + 섞는 방식", j3 + "~누구와", size=30,
         color="indigo", stroke="indigo"),
    chip("sum3", 960, 540, "눌린 뒤의 이온 길 : 아직 열린 질문", j4 + "~눌린", size=32, color="ink"),
], pre=0.4)
SHOT("s11b", j5, [
    circle("qq", 960, 430, 92, j5 + "~여러분이라면", fill=None, stroke="indigo", sw=3, dash=[10, 8], label="?", ls=70,
           lc="indigo"),
    text("opt1", 610, 430, "힘부터 재기", j5 + "~힘부터", size=36),
    text("opt2", 1310, 430, "일단 섞어 보기", j5 + "~일단", size=36),
])
SHOT("s11c", j6, [
    text("nx_lbl", 960, 230, "다음 편", j6 + "~다음", size=30, color="grey"),
    circle("nx_a", 870, 450, 115, j6 + "+0.35", label=None),
    circle("nx_b", 1095, 450, 115, j6 + "+0.45", label=None),
    circle("nx_c", 982, 450, 24, j6 + "~맞닿은", fill=None, stroke="indigo", sw=5),
    text("nx_t", 982, 640, "맞닿은 자리의 저항", j6 + "~저항", size=40, color="indigo"),
    *END_CARD,
])
# end card: fade the 'next' visual out shortly after the last line, title in
sh = EP["scenes"][-1]["shots"][-1]
for e in sh["elements"]:
    if e["id"] in ("nx_lbl", "nx_a", "nx_b", "nx_c", "nx_t"):
        e["out"] = j6 + "$+0.6"

# ------------------------------------------------------------------ captions: no sentence-final period
# v2.1: lines written without explicit caps fell back to the text WITH its final '.', unlike every other caption.
for sc in EP["scenes"]:
    for ln in sc["lines"]:
        if not ln.get("captions"):
            t = ln["text"].rstrip()
            if t.endswith("."):
                t = t[:-1]
            if len(t) > EP["caption_max_chars"]:
                raise SystemExit(f"{ln['id']}: caption over {EP['caption_max_chars']} chars without explicit caps: {t}")
            ln["captions"] = [t]

# ------------------------------------------------------------------ checks + write
problems = []
for sc in EP["scenes"]:
    for ln in sc["lines"]:
        s = syllables(ln["say"])
        if s > 52:
            problems.append(f"long line {ln['id']} {s} syl")
        for ch in "()/[]%·→↔=":
            if ch in ln["say"]:
                problems.append(f"symbol {ch!r} in say {ln['id']}")
        for c in ln["captions"] or []:
            if len(c) > 24:
                problems.append(f"caption >24 chars {ln['id']}: {c}")
        if any(w in ln["text"] for w in ("처음", "최초", "가장 먼저")):
            problems.append(f"banned word in {ln['id']}")
if problems:
    print("PROBLEMS:\n  " + "\n  ".join(problems))
out = os.path.join(HERE, "scenes.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(EP, f, ensure_ascii=False, indent=1)
n_lines = sum(len(sc["lines"]) for sc in EP["scenes"])
n_syl = sum(syllables(ln["say"]) for sc in EP["scenes"] for ln in sc["lines"])
print(f"wrote {out}: scenes={len(EP['scenes'])} lines={n_lines} syllables={n_syl}")
