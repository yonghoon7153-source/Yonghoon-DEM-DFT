#!/usr/bin/env python3
"""Korean text helpers shared by the analysis and the renderer.

* syllables(text)          -> spoken syllable count (Hangul blocks + numbers/Latin as read)
* read_number(n, unit=None) -> Sino-Korean reading of an integer (e.g. 167 -> 백육십칠)
* spoken(text)             -> text with digits / known Latin words replaced by readings
"""
import re

DIG = "영일이삼사오육칠팔구"
SMALL = ["", "십", "백", "천"]
BIG = ["", "만", "억", "조"]

# Latin words as they are actually read (extend as needed)
LATIN = {
    "anthropic": "앤트로픽", "claude": "클로드", "grh": "지알에이치", "ai": "에이아이",
    "rsa": "알에스에이", "nist": "니스트", "ncm": "엔씨엠", "se": "에스이", "afm": "에이에프엠",
    "dem": "디이엠", "mpm": "엠피엠", "ptfe": "피티에프이", "lhs": "엘에이치에스", "ml": "엠엘",
    "ax": "에이엑스", "dft": "디에프티", "igc": "아이지씨", "lpscl": "엘피에스씨엘",
}


def read_number(n):
    n = int(n)
    if n == 0:
        return "영"
    out = []
    groups = []
    while n > 0:
        groups.append(n % 10000)
        n //= 10000
    for gi in range(len(groups) - 1, -1, -1):
        g = groups[gi]
        if g == 0:
            continue
        s = ""
        for pi in range(3, -1, -1):
            d = (g // (10 ** pi)) % 10
            if d == 0:
                continue
            if d == 1 and pi > 0:
                s += SMALL[pi]          # 십, 백, 천 (not 일십)
            else:
                s += DIG[d] + SMALL[pi]
        if gi > 0 and g == 1 and gi == 1:
            s = ""                      # 만 (not 일만)
        out.append(s + BIG[gi])
    return "".join(out)


def read_decimal(txt):
    if "." in txt:
        a, b = txt.split(".", 1)
        return read_number(a) + "점" + "".join(DIG[int(c)] for c in b)
    return read_number(txt)


def spoken(text):
    def num(m):
        return read_decimal(m.group(0).replace(",", ""))
    t = re.sub(r"\d+(?:\.\d+)?", num, text)

    def lat(m):
        w = m.group(0)
        r = LATIN.get(w.lower())
        if r:
            return r
        # spell unknown capitals letter by letter, else keep (counted as ~1 syl/2 letters)
        return w
    t = re.sub(r"[A-Za-z]+", lat, t)
    return t


def syllables(text):
    t = spoken(text)
    n = len(re.findall(r"[가-힣]", t))
    rest = re.findall(r"[A-Za-z]+", t)
    n += sum(max(1, round(len(w) / 2)) for w in rest)
    return n


if __name__ == "__main__":
    for s in ["1859년부터 167년 동안", "2, 3, 5, 7, 11", "25만 쪽이", "100만 달러가", "11월 20일, Anthropic의 수학자",
              "2024년 7월", "1972년", "0.31", "삼십 퍼센트"]:
        print(s, "->", spoken(s), syllables(s))
