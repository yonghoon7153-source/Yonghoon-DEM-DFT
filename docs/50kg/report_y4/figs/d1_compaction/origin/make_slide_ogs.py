"""슬라이드 칸 크기 (3.50 × 3.85 in · 1저자 11-03 *"이 사이즈로 origin 도 만들꺼니까"*) 용 .ogs — 같은 폴더의 .ogs 를 읽어
그림 영역 · 글씨 · 선 굵기만 바꿔 slide_350x385/ 에 쓴다 (값 · 범위 · 경계선 · 색 = 그대로).
크기 = 생성기 --figsize 3.5 3.85 그림에서 잰 그림 영역: 폭 2.713 in (6.89 cm) · 패널 높이 0.943–0.947 in (2.40 cm) · 패널 사이 0.17 in.
글씨 = 눈금 9 pt · 축 이름 9.5 pt (1:1 로 붙였을 때 9 pt) · 선 0.8 × 2 pt.  ⚠ Origin 이 이 기계에 없어 실행 확인 안 함 (기존 .ogs 와 같은 명령만 씀 · fsize 두 줄 추가).
usage: python3 -I make_slide_ogs.py"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'slide_350x385'
W_CM, H_CM = 6.89, 2.40
REP = [(r'layer\.width = 10; layer\.height = 8;', 'layer.width = %.2f; layer.height = %.2f;' % (W_CM, H_CM)),
       (r'label\.pt = 28', 'label.pt = 9'),
       (r'set %C -w 1500', 'set %C -w 800'),
       (r'\.ticklength = 6', '.ticklength = 4'),
       (r'\.mticklength = 3', '.mticklength = 2')]


def convert(text):
    for pat, new in REP:
        text, n = re.subn(pat, new, text)
        assert n >= 1, pat
    text = re.sub(r'(label -xb [^;]*;)', r'\1 xb.fsize = 9.5;', text)
    text = re.sub(r'(label -yl [^;]*;)', r'\1 yl.fsize = 9.5;', text)
    return text


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for f in sorted(HERE.glob('*.ogs')):
        t = convert(f.read_text(encoding='utf-8'))
        head = ('// [슬라이드 칸 3.50 × 3.85 in 판 · make_slide_ogs.py 가 %s 에서 만듦 · 그림 영역 %.2f × %.2f cm · 눈금 9 pt · 축 이름 9.5 pt]\n'
                % (f.name, W_CM, H_CM))
        (OUT / f.name).write_text(head + t, encoding='utf-8')
        print('wrote', (OUT / f.name).relative_to(HERE))
