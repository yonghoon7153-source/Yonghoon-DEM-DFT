"""발표 대본 → TTS 입력용 한글 읽기 변환 (숫자·단위·영문)."""
import re
D = "영일이삼사오육칠팔구"
NATIVE_HOUR = {1:"한",2:"두",3:"세",4:"네",5:"다섯",6:"여섯",7:"일곱",8:"여덟",9:"아홉",10:"열",11:"열한",12:"열두"}

def _four(n):  # 0..9999, 일천/일백/일십 은 '천/백/십'
    out = ""
    for unit, v in (("천", 1000), ("백", 100), ("십", 10)):
        q = n // v; n %= v
        if q: out += ("" if q == 1 else D[q]) + unit
    if n: out += D[n]
    return out

def sino(n):
    n = int(n)
    if n == 0: return "영"
    parts = []
    for unit, v in (("조", 10**12), ("억", 10**8), ("만", 10**4)):
        q = n // v; n %= v
        if q: parts.append(_four(q) + unit)
    if n: parts.append(_four(n))
    s = " ".join(parts)
    return s

def num(tok):
    tok = tok.replace(",", "")
    if "." in tok:
        a, b = tok.split(".")
        return sino(a) + " 점 " + "".join(D[int(c)] for c in b)
    return sino(tok)

def normalize(t):
    t = t.replace("톱3", "톱 쓰리")
    t = t.replace("Afresh", "애프레시").replace("AI", "에이아이").replace("(Why now)", "")
    t = re.sub(r"(\d+)시", lambda m: NATIVE_HOUR[int(m.group(1))] + " 시", t)
    t = re.sub(r"(\d[\d,]*(?:\.\d+)?)\s*%", lambda m: num(m.group(1)) + " 퍼센트", t)
    t = re.sub(r"(\d[\d,]*(?:\.\d+)?)\s*km", lambda m: num(m.group(1)) + " 킬로미터", t)
    t = re.sub(r"(\d[\d,]*(?:\.\d+)?)(만)?\s*kg", lambda m: num(m.group(1)) + (m.group(2) or "") + " 킬로그램", t)
    t = re.sub(r"\d[\d,]*(?:\.\d+)?", lambda m: num(m.group(0)), t)
    t = t.replace("→", ",").replace("·", ",")
    return re.sub(r"\s+", " ", t).strip()

if __name__ == "__main__":
    for s in ["1인 가구 36.1%", "1,393곳", "28.7조 원", "오후 5시", "29,900원", "293만 kg", "반경 3km", "1억 5천만 끼", "2,000만 명", "0%를", "100점 만점에 50.3점", "2024년", "톱3"]:
        print(s, "=>", normalize(s))
